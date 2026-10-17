#!/opt/cine/bin/python
"""PT · CHẤM MÙ BA NHÁNH A | B | C cùng khung (lệnh 18/10): như blind_pt.py — `claude -p` ghim claude-sonnet-5-5, chỉ Read, thư mục tạm chỉ có X/Y/Z.jpg,
3 vai nguyên văn blind_v2.py, nhãn nhánh ẨN, hoán vị X/Y/Z theo hạt giống 20261018. Không khung đối thủ. Sổ chi phí chung reports/pt/kiem-mu/cost.jsonl:
trần Claude của phiên $3 (gồm $1,467 vòng A|B) → dừng khi tổng ≥ $2,9; chạy theo khung (đủ 3 người mỗi khung rồi mới sang khung sau), khung ngày trước.
  blind_abc.py set · run · score"""
import importlib.util, json, os, random, re, shutil, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
OUT = os.path.join(REPO, 'reports', 'pt', 'kiem-mu-abc'); LOG = os.path.join(REPO, 'reports', 'pt', 'kiem-mu', 'cost.jsonl')
spec = importlib.util.spec_from_file_location('bv2', os.path.join(REPO, 'channel-k2', 'k2v2-mau', 'blind_v2.py')); BV2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(BV2)
RATERS, MODEL = BV2.RATERS, BV2.MODEL; assert MODEL == 'claude-sonnet-5-5'
STOP = 2.9
FR = ['1782-dau', '1943-dau', '1782-giua', '1943-giua', '1782-cuoi', '1943-cuoi']     # ngày trước
YEAR = {'1782': 'Gibraltar (Grand Parade by Main Street) in 1782', '1943': 'Gibraltar (Commercial Square by Main Street) in 1943'}
PROMPT = """{persona}

In the current folder there are three still frames, X.jpg, Y.jpg and Z.jpg (open all three with the Read tool). All three come from history documentaries and are meant to show {year}, from the same camera position. Judge only what you see. Be honest and specific; do not be polite.

For EACH frame score:
- craft (1–10): composition, lighting, materials, overall visual quality (10 = top-tier broadcast documentary, 5 = typical faceless YouTube history video, 1 = broken)
- detail (1–10): amount and quality of believable detail in buildings, objects and people
- period (1–10): does everything look right for the stated year (architecture, objects, clothing, flags, technology)? 10 = fully convincing, 1 = clearly wrong
- ai_look (0–10): does this frame look like an AI-generated image? 0 = not at all, 10 = obviously AI-generated
- flags: any of "broken_render", "cluttered", "empty_frame", "flat_slide_look", "toy_like", "anachronism", "text_issue", or [].

Return ONLY JSON:
{{"X": {{"craft": <int>, "detail": <int>, "period": <int>, "ai_look": <int>, "flags": [..], "note": "<short>"}},
 "Y": {{...same keys...}}, "Z": {{...same keys...}},
 "best": "X|Y|Z", "worst": "X|Y|Z", "why": "<one sentence>", "anachronisms_seen": ["<short>", ...]}}"""
SRC = {'A': '/var/tmp/pt/c_in/{f}-A-notext.jpg', 'B': '/var/tmp/pt/c_in/{f}-B-notext.jpg', 'C': '/var/tmp/pt/c_out/{f}.png'}
def spent(): return sum(json.loads(l)['usd'] for l in open(LOG)) if os.path.exists(LOG) else 0.0
def setup():
    os.makedirs(OUT, exist_ok=True); R = random.Random(20261018); key = {}
    for f in FR:
        perm = ['A', 'B', 'C']; R.shuffle(perm); d = os.path.join(OUT, f); os.makedirs(d, exist_ok=True)
        for slot, br in zip('XYZ', perm):
            Image.open(SRC[br].format(f=f)).convert('RGB').resize((1280, 720), Image.LANCZOS).save(os.path.join(d, f'{slot}.jpg'), quality=90)
        key[f] = {'X': perm[0], 'Y': perm[1], 'Z': perm[2], 'year': YEAR[f[:4]]}
    json.dump(key, open(os.path.join(OUT, 'key.json'), 'w'), indent=1, ensure_ascii=False); print(key)
def call(f, rk):
    if spent() >= STOP: return 'dung-tran'
    k = json.load(open(os.path.join(OUT, 'key.json')))[f]; prompt = PROMPT.format(persona=RATERS[rk], year=k['year'])
    env = dict(os.environ, ANTHROPIC_API_KEY=os.environ['CONSOLE_API_KEY'])
    with tempfile.TemporaryDirectory() as cwd:
        for s in ('X.jpg', 'Y.jpg', 'Z.jpg'): shutil.copy(os.path.join(OUT, f, s), cwd)
        for _ in range(2):
            r = subprocess.run(['claude', '-p', '--model', MODEL, '--output-format', 'json', '--allowedTools', 'Read'], input=prompt, capture_output=True, text=True, env=env, cwd=cwd, timeout=900)
            try: d = json.loads(r.stdout)
            except Exception: continue
            with open(LOG, 'a') as fh: fh.write(json.dumps({'tag': f'pt-abc:{f}-{rk}', 'model': MODEL, 'served': sorted(d.get('modelUsage', {})), 'usd': d.get('total_cost_usd', 0)}) + '\n')
            open(os.path.join(OUT, f, f'{rk}.raw.txt'), 'w').write(d.get('result', ''))
            m = re.search(r'\{.*\}', d.get('result', ''), re.S)
            if m:
                try: j = json.loads(m.group(0)); json.dump(j, open(os.path.join(OUT, f, f'{rk}.json'), 'w'), indent=1); return True
                except Exception: pass
    return False
def run():
    out = {}
    for f in FR:
        jobs = [rk for rk in RATERS if not os.path.exists(os.path.join(OUT, f, f'{rk}.json'))]
        if spent() >= STOP: print('DỪNG trần', round(spent(), 3)); break
        with ThreadPoolExecutor(3) as ex: res = list(ex.map(lambda rk: call(f, rk), jobs))
        out[f] = res; print(f, res, round(spent(), 3), flush=True)
def score():
    key = json.load(open(os.path.join(OUT, 'key.json'))); rows = {}; tot = {b: {m: [] for m in ('craft', 'detail', 'period', 'ai_look')} for b in 'ABC'}
    for f, k in key.items():
        J = {rk: json.load(open(os.path.join(OUT, f, f'{rk}.json'))) for rk in RATERS if os.path.exists(os.path.join(OUT, f, f'{rk}.json'))}
        if not J: continue
        row = {}
        for slot in 'XYZ':
            b = k[slot]
            for m in ('craft', 'detail', 'period', 'ai_look'):
                v = [J[r][slot][m] for r in J]; row[f'{b}_{m}'] = v; tot[b][m] += v
            row[f'{b}_flags'] = sorted({x for r in J for x in J[r][slot].get('flags', [])})
        row['best'] = {r: k.get(J[r].get('best'), '?') for r in J}; row['worst'] = {r: k.get(J[r].get('worst'), '?') for r in J}
        row['anachronisms'] = {r: J[r].get('anachronisms_seen') for r in J}; rows[f] = row
    R = {'khung': rows, 'tb': {b: {m: round(sum(v) / len(v), 2) for m, v in d.items() if v} for b, d in tot.items()}, 'chi_phi_tong_phien': round(spent(), 3)}
    json.dump(R, open(os.path.join(OUT, 'score.json'), 'w'), indent=1, ensure_ascii=False); print(json.dumps(R['tb'], ensure_ascii=False), R['chi_phi_tong_phien'])
if __name__ == '__main__':
    {'set': setup, 'run': run, 'score': score}[sys.argv[1]]()
