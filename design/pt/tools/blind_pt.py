#!/opt/cine/bin/python
"""PT · CHẤM MÙ khung neo (giao thức như blind_g2/V5b-2b): `claude -p` GHIM claude-sonnet-5-5, chỉ công cụ Read, thư mục tạm trống chỉ chứa X.jpg/Y.jpg,
3 vai (RATERS nạp nguyên văn từ channel-k2/k2v2-mau/blind_v2.py), ẩn nhãn nhánh, thứ tự X/Y theo hạt giống cố định 20261017.
Câu hỏi riêng của lệnh PT: craft, chi tiết công trình/vật/người, đúng thời kỳ, "khung này có trông như ảnh AI không? (0–10)".
Cặp: A vs B mỗi mốc (1782, 1943) + mỗi nhánh (khung 1782 trưa) vs 3 khung cùng nơi của kênh (gib20 ×2, V5b-2b-T 21,0 s).
KHÔNG có khung đối thủ trong repo hay trong API. Sổ chi phí reports/pt/kiem-mu/cost.jsonl; trần $3, dừng $2,7.
  blind_pt.py set <thư mục khung> · blind_pt.py run · blind_pt.py score"""
import importlib.util, json, os, random, re, shutil, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
OUT = os.path.join(REPO, 'reports', 'pt', 'kiem-mu'); LOG = os.path.join(OUT, 'cost.jsonl')
spec = importlib.util.spec_from_file_location('bv2', os.path.join(REPO, 'channel-k2', 'k2v2-mau', 'blind_v2.py')); BV2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(BV2)
RATERS, MODEL = BV2.RATERS, BV2.MODEL
assert MODEL == 'claude-sonnet-5-5'
CAP, STOP = 3.0, 2.7
PROMPT = """{persona}

In the current folder there are two still frames, X.jpg and Y.jpg (open both with the Read tool). Both come from history documentaries that show what a real place looked like in a past year. Frame X is meant to show {yx}; frame Y is meant to show {yy}. Judge only what you see. Be honest and specific; do not be polite.

For EACH frame score:
- craft (1–10): composition, lighting, materials, overall visual quality (10 = top-tier broadcast documentary, 5 = typical faceless YouTube history video, 1 = broken)
- detail (1–10): amount and quality of believable detail in buildings, objects and people
- period (1–10): does everything look right for the stated year (architecture, objects, clothing, technology)? 10 = fully convincing, 1 = clearly wrong
- ai_look (0–10): does this frame look like an AI-generated image? 0 = not at all, 10 = obviously AI-generated
- flags: any of "broken_render", "cluttered", "empty_frame", "flat_slide_look", "toy_like", "anachronism", "text_issue", or [].

Return ONLY JSON:
{{"X": {{"craft": <int>, "detail": <int>, "period": <int>, "ai_look": <int>, "flags": [..], "note": "<short>"}},
 "Y": {{"craft": <int>, "detail": <int>, "period": <int>, "ai_look": <int>, "flags": [..], "note": "<short>"}},
 "better": "X|Y|tie", "why": "<one sentence>", "top_fix_for_weaker": "<concrete>"}}"""
YEAR = {'1782': 'Gibraltar (Grand Parade by Main Street) in 1782', '1943': 'Gibraltar (Commercial Square by Main Street) in 1943',
        'g1753': 'Gibraltar old town in 1752', 'g1885': 'Gibraltar old town in 1884', 'v1782': 'Gibraltar, Main Street area, in 1782'}
REF = {'g1753': '/var/tmp/pt/ref/pho-day-pho-co-1753.jpg', 'g1885': '/var/tmp/pt/ref/can-hero-3-thap-pho-quanh-1885.jpg', 'v1782': '/var/tmp/pt/ref/v5b2b-21s.jpg'}
# khai TRƯỚC khi chấm: khung PT = khung tĩnh khai trước trong live.py (trưa = lượt d2, giờ ảo 12,8)
PAIRS = {
    'AB1782': ('A:1782-trua-A-notext.jpg', 'B:1782-trua-B-notext.jpg', '1782', '1782'),
    'AB1943': ('A:1943-trua-A-notext.jpg', 'B:1943-trua-B-notext.jpg', '1943', '1943'),
    'Ag1753': ('A:1782-trua-A.jpg', 'R:g1753', '1782', 'g1753'), 'Ag1885': ('A:1782-trua-A.jpg', 'R:g1885', '1782', 'g1885'), 'Av1782': ('A:1782-trua-A.jpg', 'R:v1782', '1782', 'v1782'),
    'Bg1753': ('B:1782-trua-B.jpg', 'R:g1753', '1782', 'g1753'), 'Bg1885': ('B:1782-trua-B.jpg', 'R:g1885', '1782', 'g1885'), 'Bv1782': ('B:1782-trua-B.jpg', 'R:v1782', '1782', 'v1782'),
}

def spent(): return sum(json.loads(l)['usd'] for l in open(LOG)) if os.path.exists(LOG) else 0.0

def src(tag, d):
    k, v = tag.split(':', 1)
    return (REF[v], v) if k == 'R' else (os.path.join(d, v), k)

def setup(d):
    os.makedirs(OUT, exist_ok=True); R = random.Random(20261017); key = {}
    for pid, (a, b, ya, yb) in PAIRS.items():
        pa, la = src(a, d); pb, lb = src(b, d); swap = R.random() < 0.5
        X, Y = ((pb, lb, yb), (pa, la, ya)) if swap else ((pa, la, ya), (pb, lb, yb))
        od = os.path.join(OUT, pid); os.makedirs(od, exist_ok=True)
        for (p, _, _), n in ((X, 'X.jpg'), (Y, 'Y.jpg')):
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', p, '-vf', 'scale=1280:-2', '-q:v', '3', os.path.join(od, n)], check=True)
        key[pid] = {'X': X[1], 'Y': Y[1], 'yx': YEAR[X[2]], 'yy': YEAR[Y[2]], 'file_X': os.path.basename(X[0]), 'file_Y': os.path.basename(Y[0])}
    json.dump(key, open(os.path.join(OUT, 'key.json'), 'w'), indent=1, ensure_ascii=False); print(json.dumps(key, indent=1, ensure_ascii=False))

def call(pid, rk):
    if spent() > STOP: raise SystemExit(f'dừng: đã tiêu ${spent():.2f}')
    k = json.load(open(os.path.join(OUT, 'key.json')))[pid]; prompt = PROMPT.format(persona=RATERS[rk], yx=k['yx'], yy=k['yy'])
    env = dict(os.environ, ANTHROPIC_API_KEY=os.environ['CONSOLE_API_KEY'])
    with tempfile.TemporaryDirectory() as cwd:
        for f in ('X.jpg', 'Y.jpg'): shutil.copy(os.path.join(OUT, pid, f), cwd)
        for _ in range(2):
            r = subprocess.run(['claude', '-p', '--model', MODEL, '--output-format', 'json', '--allowedTools', 'Read'], input=prompt, capture_output=True, text=True, env=env, cwd=cwd, timeout=900)
            try: d = json.loads(r.stdout)
            except Exception: continue
            with open(LOG, 'a') as f: f.write(json.dumps({'tag': f'pt:{pid}-{rk}', 'model': MODEL, 'served': sorted(d.get('modelUsage', {})), 'usd': d.get('total_cost_usd', 0)}) + '\n')
            open(os.path.join(OUT, pid, f'{rk}.raw.txt'), 'w').write(d.get('result', ''))
            m = re.search(r'\{.*\}', d.get('result', ''), re.S)
            if m:
                try: j = json.loads(m.group(0)); json.dump(j, open(os.path.join(OUT, pid, f'{rk}.json'), 'w'), indent=1); return True
                except Exception: pass
    return False

def run():
    key = json.load(open(os.path.join(OUT, 'key.json')))
    jobs = [(p, rk) for p in key for rk in RATERS if not os.path.exists(os.path.join(OUT, p, f'{rk}.json'))]
    with ThreadPoolExecutor(3) as ex: res = list(ex.map(lambda a: call(*a), jobs))
    print(dict(zip([f'{a}-{b}' for a, b in jobs], res)), f'chi phí ${spent():.2f} / trần ${CAP}')

def score():
    key = json.load(open(os.path.join(OUT, 'key.json'))); rows = {}
    for pid, k in key.items():
        J = {rk: json.load(open(os.path.join(OUT, pid, f'{rk}.json'))) for rk in RATERS if os.path.exists(os.path.join(OUT, pid, f'{rk}.json'))}
        row = {'X': k['X'], 'Y': k['Y']}
        for side in ('X', 'Y'):
            lab = k[side]
            for m in ('craft', 'detail', 'period', 'ai_look'):
                v = [J[r][side][m] for r in J]; row[f'{lab}_{m}'] = v; row[f'{lab}_{m}_tb'] = round(sum(v) / len(v), 2)
            row[f'{lab}_flags'] = sorted({f for r in J for f in J[r][side].get('flags', [])})
        row['better'] = {r: (k[J[r]['better']] if J[r].get('better') in ('X', 'Y') else 'tie') for r in J}
        row['fix'] = {r: J[r].get('top_fix_for_weaker') for r in J}; rows[pid] = row
    R = {'cap': rows, 'chi_phi': round(spent(), 3)}
    json.dump(R, open(os.path.join(OUT, 'score.json'), 'w'), indent=1, ensure_ascii=False); print(json.dumps(R, ensure_ascii=False, indent=1))

if __name__ == '__main__':
    a = sys.argv[1]
    if a == 'set': setup(sys.argv[2])
    elif a == 'run': run()
    elif a == 'score': score()
