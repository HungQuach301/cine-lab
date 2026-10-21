#!/opt/cine/bin/python
# V7C · biến thể của v7c_cham_mu.py: thêm phiên bản "V7C-lai" (khung xiên có chân trời) cho 3 loại cảnh vây hãm / cảng / phố dày → reports/v7c/cham-mu-lai
"""V7C · CHẤM MÙ khung cổng V7B ↔ A-NC-CPU ↔ V7C (bản sao reports/nc-cpu/blind_nc.py — chỉ đổi thư mục ra, hạt giống, nhãn chi phí) — giao thức blind_v6.py: `claude -p` ghim claude-sonnet-5-5, chỉ công cụ Read, thư mục tạm chỉ chứa các ảnh
(640×360 theo lệnh), 3 vai RATERS nguyên văn channel-k2/k2v2-mau/blind_v2.py, nhãn hoán vị theo hạt giống 20261019, mô tả TRUNG TÍNH theo loại cảnh.
KHÔNG khung đối thủ (điều phối tự so trong chat). Chấm mù không thay kiểm dữ kiện.
  blind_nc.py set <json {ban: thư mục có cong-<k>.png|jpg}> · run · score"""
import glob, importlib.util, json, os, random, re, shutil, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
OUT = os.path.join(REPO, 'reports', 'v7c', 'cham-mu-lai'); LOG = os.path.join(OUT, 'cost.jsonl')
spec = importlib.util.spec_from_file_location('bv2', os.path.join(REPO, 'channel-k2', 'k2v2-mau', 'blind_v2.py')); BV2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(BV2)
RATERS, MODEL = BV2.RATERS, BV2.MODEL
assert MODEL == 'claude-sonnet-5-5'
TYPES = {'vay-ham': 'a siege scene: the besiegers\' camps and lines on the isthmus in front of a fortified rock, 1779',
         'cang': 'a harbour scene: a relief convoy of 18th-century sailing ships arriving at a fortified port town, 1780',
         'pho-day': 'a dense old-town scene of an 18th-century fortified port town seen from above, 1780',
         'hero': 'a hero shot of a modern city on a famous rock with an airport, 2026',
         'toan-canh': 'a panorama of an 18th-century fortified town along a bay with a fleet, 1781',
         'bo-chien-su': 'a shore-and-battle scene: floating gun batteries attacking a fortified town from the sea, 1782'}
TYPES = {k: v for k, v in TYPES.items() if k in ('vay-ham', 'cang', 'pho-day')}
L = 'ABCD'
PROMPT = """{persona}

In the current folder there are {n} still frames, {files}: {n} versions of the same shot type from a stylised 3D animated history documentary — {kind}. Open all of them with the Read tool. Judge only what you see. Be honest and specific.

For EACH version score:
- craft (1–10): composition, lighting, colour, materials, overall visual quality (10 = top-tier cinematic 3D history animation, 5 = typical faceless YouTube 3D explainer, 1 = broken)
- realism (1–10): surface realism — does the ground, water, vegetation, buildings and atmosphere read as a real place (10) or as flat untextured blocks/colour fields (1)?
- detail (1–10): amount and quality of believable detail (buildings, troops, people, ships, smoke, terrain)
- toy_like (0–10): do the people, troops, ships or buildings look like toys / game pieces? 0 = not at all, 10 = clearly toy-like
- ai_look (0–10): does it look AI-generated? 0 = not at all, 10 = obviously
- flags: any of "broken_render", "empty_frame", "flat_slide_look", "toy_look", "cluttered", "confusing", "unreadable_scale", "washed_out", "noisy", or [].

Return ONLY JSON:
{{{schema}, "rank": [<letters best→worst>], "why": "<one sentence>", "top_fix_for_best": "<concrete>"}}"""
def spent(): return sum(json.loads(l)['usd'] for l in open(LOG)) if os.path.exists(LOG) else 0.0
def find(d, k):
    for p in [f'{d}/cong-{k}.png', f'{d}/cong-{k}.jpg'] + sorted(glob.glob(f'{d}/{k}/*.jpg')) + sorted(glob.glob(f'{d}/{k}/*.png')):
        if os.path.exists(p): return p
def setup(js):
    src = json.load(open(js)); os.makedirs(OUT, exist_ok=True); R = random.Random(20261020); key = {}
    for k, kind in TYPES.items():
        have = {v: find(d, k) for v, d in src.items()}; have = {v: p for v, p in have.items() if p}
        order = list(have); R.shuffle(order); lab = dict(zip(order, L)); d = os.path.join(OUT, k); os.makedirs(d, exist_ok=True)
        for v, p in have.items(): Image.open(p).convert('RGB').resize((640, 360), Image.LANCZOS).save(os.path.join(d, lab[v] + '.jpg'), quality=92)
        key[k] = dict(kind=kind, nhan=lab, tep={v: os.path.relpath(p, REPO) if p.startswith(REPO) else p for v, p in have.items()})
    json.dump(key, open(os.path.join(OUT, 'key.json'), 'w'), indent=1); print(json.dumps(key, indent=1))
def call(k, rk):
    if spent() > 7.5: raise SystemExit(f'dừng: đã tiêu ${spent():.2f}')
    key = json.load(open(os.path.join(OUT, 'key.json'))); labs = sorted(key[k]['nhan'].values()); files = ', '.join(f'{x}.jpg' for x in labs)
    schema = ', '.join(f'"{x}": {{"craft": <int>, "realism": <int>, "detail": <int>, "toy_like": <int>, "ai_look": <int>, "flags": [..], "note": "<short>"}}' for x in labs)
    prompt = PROMPT.format(persona=RATERS[rk], kind=key[k]['kind'], n=len(labs), files=files, schema=schema)
    with tempfile.TemporaryDirectory() as cwd:
        for x in labs: shutil.copy(os.path.join(OUT, k, x + '.jpg'), cwd)
        for _ in range(2):
            r = subprocess.run(['claude', '-p', '--model', MODEL, '--output-format', 'json', '--allowedTools', 'Read'], input=prompt, capture_output=True, text=True, cwd=cwd, timeout=900)
            try: d = json.loads(r.stdout)
            except Exception: continue
            with open(LOG, 'a') as f: f.write(json.dumps({'tag': f'v7c-lai:{k}-{rk}', 'model': MODEL, 'served': sorted(d.get('modelUsage', {})), 'usd': d.get('total_cost_usd', 0)}) + '\n')
            open(os.path.join(OUT, k, f'{rk}.raw.txt'), 'w').write(d.get('result', ''))
            m = re.search(r'\{.*\}', d.get('result', ''), re.S)
            if m:
                try: j = json.loads(m.group(0)); json.dump(j, open(os.path.join(OUT, k, f'{rk}.json'), 'w'), indent=1); return True
                except Exception: pass
    return False
def run():
    key = json.load(open(os.path.join(OUT, 'key.json')))
    jobs = [(p, rk) for p in key for rk in RATERS if not os.path.exists(os.path.join(OUT, p, f'{rk}.json'))]
    with ThreadPoolExecutor(3) as ex: res = list(ex.map(lambda a: call(*a), jobs))
    print(dict(zip([f'{a}-{b}' for a, b in jobs], res)), f'chi phí ${spent():.3f}')
def score():
    key = json.load(open(os.path.join(OUT, 'key.json'))); R = {}; Mm = ('craft', 'realism', 'detail', 'toy_like', 'ai_look'); vs = sorted({v for k in key.values() for v in k['nhan']})
    for k, kk in key.items():
        J = {rk: json.load(open(os.path.join(OUT, k, f'{rk}.json'))) for rk in RATERS if os.path.exists(os.path.join(OUT, k, f'{rk}.json'))}
        row = dict(nguoi=len(J))
        for v, lab in kk['nhan'].items():
            row[v] = {m: round(sum(J[r][lab][m] for r in J) / max(1, len(J)), 2) for m in Mm}
            row[v]['flags'] = sorted({f for r in J for f in J[r][lab].get('flags', [])}); row[v]['note'] = [J[r][lab].get('note') for r in J]
            row[v]['hang1'] = sum(1 for r in J if J[r].get('rank', [None])[0] == lab)
        row['why'] = [J[r].get('why') for r in J]; row['sua_ban_tot'] = [J[r].get('top_fix_for_best') for r in J]; R[k] = row
    for v in vs:
        ks = [k for k in key if v in R[k]]; R['tb_' + v] = {m: round(sum(R[k][v][m] for k in ks) / len(ks), 2) for m in Mm}; R['tb_' + v]['hang1'] = sum(R[k][v]['hang1'] for k in ks)
    R['chi_phi'] = round(spent(), 3); json.dump(R, open(os.path.join(OUT, 'score.json'), 'w'), indent=1, ensure_ascii=False)
    for k in key: print(k, {v: (R[k][v]['craft'], R[k][v]['realism'], R[k][v]['hang1']) for v in vs if v in R[k]})
    print({k: v for k, v in R.items() if k.startswith('tb_')}, 'chi phí', R['chi_phi'])
if __name__ == '__main__':
    a = sys.argv[1]
    if a == 'set': setup(sys.argv[2])
    elif a == 'run': run()
    elif a == 'score': score()
