#!/opt/cine/bin/python
"""PT2 · CHẤM MÙ LAI (A+C) vs A-thuần, cùng khung neo × cùng giờ ảo (giao thức PT/V5b-2b): `claude -p` GHIM claude-sonnet-5-5, chỉ công cụ Read,
thư mục tạm chỉ có X.jpg/Y.jpg (không chữ), 3 vai nguyên văn channel-k2/k2v2-mau/blind_v2.py, nhãn bản ẨN, thứ tự X/Y theo hạt giống 20261018.
Thang: craft / detail / period 1–10, ai_look 0–10, toy_like 0–10 (người/vật trông như đồ chơi) + cờ. KHÔNG khung đối thủ (điều phối tự so trong chat).
KHÔNG dùng để kiểm dữ kiện (HC4d) — chỉ đo cảm nhận. Sổ chi phí reports/pt2/kiem-mu/cost.jsonl; trần phiên Claude $3, dừng khi ≥ $2,7.
  blind_lai.py set <thư mục khung> · run · score"""
import importlib.util, json, os, random, re, shutil, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
OUT = os.path.join(REPO, 'reports', 'pt2', 'kiem-mu'); LOG = os.path.join(OUT, 'cost.jsonl')
spec = importlib.util.spec_from_file_location('bv2', os.path.join(REPO, 'channel-k2', 'k2v2-mau', 'blind_v2.py')); BV2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(BV2)
RATERS, MODEL = BV2.RATERS, BV2.MODEL; assert MODEL == 'claude-sonnet-5-5'
STOP = 2.7
PROMPT = """{persona}

In the current folder there are two still frames, X.jpg and Y.jpg (open both with the Read tool). Both come from history documentaries and show {year}, from the same camera position at the same time of day. Judge only what you see. Be honest and specific; do not be polite.

For EACH frame score:
- craft (1–10): composition, lighting, materials, overall visual quality (10 = top-tier broadcast documentary, 5 = typical faceless YouTube history video, 1 = broken)
- detail (1–10): amount and quality of believable detail in buildings, objects and people
- period (1–10): does everything look right for the stated year (architecture, objects, clothing, flags, technology)? 10 = fully convincing, 1 = clearly wrong
- ai_look (0–10): does this frame look like an AI-generated image? 0 = not at all, 10 = obviously AI-generated
- toy_like (0–10): do the people or objects look like toys, dolls or game assets? 0 = not at all, 10 = clearly toy-like
- flags: any of "broken_render", "cluttered", "empty_frame", "flat_slide_look", "toy_like", "anachronism", "text_issue", or [].

Return ONLY JSON:
{{"X": {{"craft": <int>, "detail": <int>, "period": <int>, "ai_look": <int>, "toy_like": <int>, "flags": [..], "note": "<short>"}},
 "Y": {{"craft": <int>, "detail": <int>, "period": <int>, "ai_look": <int>, "toy_like": <int>, "flags": [..], "note": "<short>"}},
 "better": "X|Y|tie", "why": "<one sentence>", "top_fix_for_weaker": "<concrete>", "anachronisms_seen": ["<short>", ...]}}"""
YEAR = {'1782': 'a narrow lane in the town of Gibraltar in September 1782, during the Great Siege', '1943': 'Commercial Square by Main Street, Gibraltar, in September 1943'}
# khai TRƯỚC khi chấm: 4 thời điểm khai trước trong live2.py (sáng 10,0 · trưa 12,8 · chiều vàng 17,55 · đêm 21,8) × 2 khung neo
FR = [f'{e}-{t}' for t in ('trua', 'sang', 'chieu', 'dem') for e in (1782, 1943)]
def spent(): return sum(json.loads(l)['usd'] for l in open(LOG)) if os.path.exists(LOG) else 0.0
def setup(d):
    os.makedirs(OUT, exist_ok=True); R = random.Random(20261018); key = {}
    for f in FR:
        swap = R.random() < 0.5; X, Y = ('A', 'LAI') if swap else ('LAI', 'A'); od = os.path.join(OUT, f); os.makedirs(od, exist_ok=True)
        for b, n in ((X, 'X.jpg'), (Y, 'Y.jpg')):
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', os.path.join(d, f'{f}-{b}-notext.png'), '-vf', 'scale=1280:-2', '-q:v', '3', os.path.join(od, n)], check=True)
        key[f] = {'X': X, 'Y': Y, 'year': YEAR[f[:4]]}
    json.dump(key, open(os.path.join(OUT, 'key.json'), 'w'), indent=1, ensure_ascii=False); print(key)
def call(f, rk):
    if spent() >= STOP: return 'dung-tran'
    k = json.load(open(os.path.join(OUT, 'key.json')))[f]; prompt = PROMPT.format(persona=RATERS[rk], year=k['year'])
    env = dict(os.environ, ANTHROPIC_API_KEY=os.environ['CONSOLE_API_KEY'])
    with tempfile.TemporaryDirectory() as cwd:
        for s in ('X.jpg', 'Y.jpg'): shutil.copy(os.path.join(OUT, f, s), cwd)
        for _ in range(2):
            r = subprocess.run(['claude', '-p', '--model', MODEL, '--output-format', 'json', '--allowedTools', 'Read'], input=prompt, capture_output=True, text=True, env=env, cwd=cwd, timeout=900)
            try: d = json.loads(r.stdout)
            except Exception: continue
            with open(LOG, 'a') as fh: fh.write(json.dumps({'tag': f'pt2:{f}-{rk}', 'model': MODEL, 'served': sorted(d.get('modelUsage', {})), 'usd': d.get('total_cost_usd', 0)}) + '\n')
            open(os.path.join(OUT, f, f'{rk}.raw.txt'), 'w').write(d.get('result', ''))
            m = re.search(r'\{.*\}', d.get('result', ''), re.S)
            if m:
                try: json.dump(json.loads(m.group(0)), open(os.path.join(OUT, f, f'{rk}.json'), 'w'), indent=1); return True
                except Exception: pass
    return False
def run():
    for f in FR:
        if spent() >= STOP: print('DỪNG trần', round(spent(), 3)); break
        jobs = [rk for rk in RATERS if not os.path.exists(os.path.join(OUT, f, f'{rk}.json'))]
        with ThreadPoolExecutor(3) as ex: res = list(ex.map(lambda rk: call(f, rk), jobs))
        print(f, res, round(spent(), 3), flush=True)
def score():
    key = json.load(open(os.path.join(OUT, 'key.json'))); rows = {}; M = ('craft', 'detail', 'period', 'ai_look', 'toy_like')
    tot = {b: {m: [] for m in M} for b in ('LAI', 'A')}; per = {e: {b: {m: [] for m in M} for b in ('LAI', 'A')} for e in ('1782', '1943')}
    for f, k in key.items():
        J = {rk: json.load(open(os.path.join(OUT, f, f'{rk}.json'))) for rk in RATERS if os.path.exists(os.path.join(OUT, f, f'{rk}.json'))}
        if not J: continue
        row = {}
        for slot in 'XY':
            b = k[slot]
            for m in M:
                v = [J[r][slot].get(m) for r in J if isinstance(J[r][slot].get(m), (int, float))]; row[f'{b}_{m}'] = v; tot[b][m] += v; per[f[:4]][b][m] += v
            row[f'{b}_flags'] = sorted({x for r in J for x in J[r][slot].get('flags', [])})
        row['better'] = {r: k.get(J[r].get('better'), 'tie') for r in J}; row['why'] = {r: J[r].get('why') for r in J}
        row['anachronisms'] = {r: J[r].get('anachronisms_seen') for r in J}; rows[f] = row
    avg = lambda d: {b: {m: round(sum(v) / len(v), 2) for m, v in dd.items() if v} for b, dd in d.items()}
    R = {'khung': rows, 'tb': avg(tot), 'tb_theo_moc': {e: avg(d) for e, d in per.items()},
         'phieu_better': {b: sum(1 for r in rows.values() for v in r['better'].values() if v == b) for b in ('LAI', 'A', 'tie')}, 'chi_phi': round(spent(), 3)}
    json.dump(R, open(os.path.join(OUT, 'score.json'), 'w'), indent=1, ensure_ascii=False); print(json.dumps({k: R[k] for k in ('tb', 'phieu_better', 'chi_phi')}, ensure_ascii=False))
if __name__ == '__main__':
    {'set': lambda: setup(sys.argv[2]), 'run': run, 'score': score}[sys.argv[1]]()
