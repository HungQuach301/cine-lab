#!/opt/cine/bin/python -I
"""NC-V2V3 · CHẤM MÙ — giao thức NC-GPU (reports/nc-gpu/blind_ncg.py @claude/eloquent-dijkstra-kemr8j: PROMPT + 3 vai RATERS nguyên văn
channel-k2/k2v2-mau/blind_v2.py, `claude -p` ghim claude-sonnet-5-5, chỉ công cụ Read, thư mục tạm chỉ chứa ảnh, nhãn hoán vị theo hạt), ở HAI cỡ 640×360 và 320×180.
 Bộ CỔNG (cùng điểm máy NC-CPU/NC-GPU): V7B · A (NC-CPU) · Cycles GPU 256 spp (NC-GPU) · V2V3-B · V2V3-A.
 Bộ CLIP (khung 120 của clip NC-V2V = khung 40 của cửa sổ): V7B nguồn · V2V3-A · V2V3-B · Omni-a (NC-V2V; CHỈ để đo khoảng cách "độ thật" — Omni CÓ vật bịa, không phải ứng viên).
 Không khung đối thủ. Chấm mù không thay kiểm dữ kiện (K-LAI-3 e).
  cham3.py set <cfg.json> · run · score        (thư mục ra: reports/nc-v2v3/cham-mu/)"""
import importlib.util, json, os, random, re, shutil, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
OUT = os.path.join(REPO, 'reports/nc-v2v3/cham-mu'); LOG = os.path.join(OUT, 'cost.jsonl')
spec = importlib.util.spec_from_file_location('bv2', os.path.join(REPO, 'channel-k2', 'k2v2-mau', 'blind_v2.py')); BV2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(BV2)
RATERS, MODEL = BV2.RATERS, BV2.MODEL
assert MODEL == 'claude-sonnet-5-5'
L = 'ABCDE'
# PROMPT nguyên văn NC-GPU blind_ncg.py
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
MM = ('craft', 'realism', 'detail', 'toy_like', 'ai_look')


def spent(): return sum(json.loads(l)['usd'] for l in open(LOG)) if os.path.exists(LOG) else 0.0


def setup(cfg):
    C = json.load(open(cfg)); R = random.Random(20102026); key = {}
    for s in C['sets']:
        vs = list(s['ban']); R.shuffle(vs); lab = dict(zip(vs, L))
        for size, (w, h) in (('640', (640, 360)), ('320', (320, 180))):
            d = os.path.join(OUT, s['id'], size); os.makedirs(d, exist_ok=True)
            for v, p in s['ban'].items():
                p = p.get(size, p['640']) if isinstance(p, dict) else p
                Image.open(p).convert('RGB').resize((w, h), Image.LANCZOS).save(os.path.join(d, lab[v] + '.jpg'), quality=92)
        key[s['id']] = dict(kind=s['kind'], nhan=lab, tep={v: (p if isinstance(p, str) else p) for v, p in s['ban'].items()})
    json.dump(key, open(os.path.join(OUT, 'key.json'), 'w'), indent=1, ensure_ascii=False); print(json.dumps({k: v['nhan'] for k, v in key.items()}))


def call(sid, size, rk):
    if spent() > 7.5: raise SystemExit(f'dừng: đã tiêu ${spent():.2f}')
    key = json.load(open(os.path.join(OUT, 'key.json'))); labs = sorted(key[sid]['nhan'].values()); files = ', '.join(f'{x}.jpg' for x in labs)
    schema = ', '.join(f'"{x}": {{"craft": <int>, "realism": <int>, "detail": <int>, "toy_like": <int>, "ai_look": <int>, "flags": [..], "note": "<short>"}}' for x in labs)
    prompt = PROMPT.format(persona=RATERS[rk], kind=key[sid]['kind'], n=len(labs), files=files, schema=schema); d0 = os.path.join(OUT, sid, size)
    with tempfile.TemporaryDirectory() as cwd:
        for x in labs: shutil.copy(os.path.join(d0, x + '.jpg'), cwd)
        for _ in range(2):
            r = subprocess.run(['claude', '-p', '--model', MODEL, '--output-format', 'json', '--allowedTools', 'Read'], input=prompt, capture_output=True, text=True, cwd=cwd, timeout=900)
            try: d = json.loads(r.stdout)
            except Exception: continue
            with open(LOG, 'a') as f: f.write(json.dumps({'tag': f'v2v3:{sid}-{size}-{rk}', 'model': MODEL, 'served': sorted(d.get('modelUsage', {})), 'usd': d.get('total_cost_usd', 0)}) + '\n')
            open(os.path.join(d0, f'{rk}.raw.txt'), 'w').write(d.get('result', ''))
            m = re.search(r'\{.*\}', d.get('result', ''), re.S)
            if m:
                try: j = json.loads(m.group(0)); json.dump(j, open(os.path.join(d0, f'{rk}.json'), 'w'), indent=1); return True
                except Exception: pass
    return False


def run():
    key = json.load(open(os.path.join(OUT, 'key.json')))
    jobs = [(s, z, rk) for s in key for z in ('640', '320') for rk in RATERS if not os.path.exists(os.path.join(OUT, s, z, f'{rk}.json'))]
    with ThreadPoolExecutor(3) as ex: res = list(ex.map(lambda a: call(*a), jobs))
    print(dict(zip(['-'.join(a) for a in jobs], res)), f'chi phí ${spent():.3f}')


def score():
    key = json.load(open(os.path.join(OUT, 'key.json'))); R = {}
    for z in ('640', '320'):
        for sid, kk in key.items():
            J = {rk: json.load(open(os.path.join(OUT, sid, z, f'{rk}.json'))) for rk in RATERS if os.path.exists(os.path.join(OUT, sid, z, f'{rk}.json'))}
            row = dict(nguoi=len(J))
            for v, lab in kk['nhan'].items():
                row[v] = {m: round(sum(J[r][lab][m] for r in J) / max(1, len(J)), 2) for m in MM}
                row[v]['hang1'] = sum(1 for r in J if J[r].get('rank', [None])[0] == lab)
                row[v]['hang_tb'] = round(sum(J[r]['rank'].index(lab) + 1 for r in J if lab in J[r].get('rank', [])) / max(1, len(J)), 2)
                row[v]['flags'] = sorted({f for r in J for f in J[r][lab].get('flags', [])}); row[v]['note'] = [J[r][lab].get('note') for r in J]
            row['why'] = [J[r].get('why') for r in J]; R[f'{sid}@{z}'] = row
    json.dump(dict(R, chi_phi=round(spent(), 3)), open(os.path.join(OUT, 'score.json'), 'w'), indent=1, ensure_ascii=False)
    for k, row in R.items(): print(k, {v: (row[v]['craft'], row[v]['realism'], row[v]['ai_look'], row[v]['hang1'], row[v]['hang_tb']) for v in row if isinstance(row[v], dict)})
    print('chi phí', round(spent(), 3))


if __name__ == '__main__':
    a = sys.argv[1]
    if a == 'set': setup(sys.argv[2])
    elif a == 'run': run()
    elif a == 'score': score()
