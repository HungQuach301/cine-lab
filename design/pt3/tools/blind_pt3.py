#!/opt/cine/bin/python
"""PT3 · CHẤM MÙ A vs HC7 (vs HC8) trên CÙNG khung/cú máy — giao thức như PT (blind_abc.py): `claude -p` GHIM claude-sonnet-5-5, chỉ Read,
thư mục tạm chỉ chứa ảnh của mục, 3 vai nguyên văn channel-k2/k2v2-mau/blind_v2.py, nhãn nhánh ẨN, hoán vị theo hạt giống 20261018.
Mỗi nhánh 2 ảnh: <slot>.jpg = khung tĩnh 1280×720; <slot>_seq.jpg = 4 khung LIỀN NHAU (t..t+3) cắt cùng vùng giữa, phóng 2× → hỏi nhấp nháy có/không.
Khung khai TRƯỚC: phố 60, 150; orbit 30, 72, 120. Không khung đối thủ (điều phối tự so trong chat). Sổ chi phí reports/pt3/kiem-mu/cost.jsonl, trần $3, dừng $2,8.
  blind_pt3.py set · run · score"""
import importlib.util, json, os, random, re, shutil, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
OUT = os.path.join(REPO, 'reports', 'pt3', 'kiem-mu'); LOG = os.path.join(OUT, 'cost.jsonl')
spec = importlib.util.spec_from_file_location('bv2', os.path.join(REPO, 'channel-k2', 'k2v2-mau', 'blind_v2.py')); BV2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(BV2)
RATERS, MODEL = BV2.RATERS, BV2.MODEL; assert MODEL == 'claude-sonnet-5-5'
STOP = 2.8
RUN = '/var/tmp/pt3/run'
ITEMS = {'pho-060': ('street', 60, ['A', 'HC7']), 'pho-150': ('street', 150, ['A', 'HC7']),
         'kb-030': ('kb', 30, ['A', 'HC7', 'HC8']), 'kb-072': ('kb', 72, ['A', 'HC7', 'HC8']), 'kb-120': ('kb', 120, ['A', 'HC7', 'HC8'])}
DIRS = {('street', 'A'): 'stA', ('street', 'HC7'): 'stH7', ('kb', 'A'): 'kbA', ('kb', 'HC7'): 'kbH7', ('kb', 'HC8'): 'kbH8'}
YEAR = {'street': 'Main Street, Gibraltar, in 1943, seen from a camera drone flying low along the street',
        'kb': "King's Bastion, Gibraltar, in 1782, seen from a camera drone orbiting the bastion"}
PROMPT = """{persona}

In the current folder there are {n} versions of the same shot, labelled {slots}. For each label L there are two images: L.jpg (one still frame of the shot) and L_seq.jpg (four CONSECUTIVE frames of the same shot, 1/24 s apart, cropped to the same central region and enlarged, left to right then top to bottom). Open every image with the Read tool. All versions are meant to show {year}. Judge only what you see. Be honest and specific; do not be polite.

For EACH version score:
- craft (1–10): composition, lighting, materials, overall visual quality (10 = top-tier broadcast documentary, 5 = typical faceless YouTube history video, 1 = broken)
- detail (1–10): amount and quality of believable surface and material detail on the buildings
- period (1–10): does everything look right for the stated year and place? 10 = fully convincing, 1 = clearly wrong
- ai_look (0–10): does this look like AI-generated imagery? 0 = not at all, 10 = obviously AI-generated
- flicker (yes/no): across the four consecutive frames, does any surface texture or detail visibly flicker, shimmer, swim or change instead of staying fixed to the buildings while the camera moves?
- flags: any of "broken_render", "stretched_texture", "seams", "cluttered", "flat_slide_look", "toy_like", "anachronism", "text_issue", or [].

Return ONLY JSON:
{{{slotjson}, "best": "<label>", "worst": "<label>", "why": "<one sentence>", "anachronisms_seen": ["<short>", ...]}}"""

def spent(): return sum(json.loads(l)['usd'] for l in open(LOG)) if os.path.exists(LOG) else 0.0

def setup():
    os.makedirs(OUT, exist_ok=True); R = random.Random(20261018); key = {}
    for it, (site, f, br) in ITEMS.items():
        perm = list(br); R.shuffle(perm); d = os.path.join(OUT, it); os.makedirs(d, exist_ok=True); slots = 'XYZ'[:len(perm)]
        for s, b in zip(slots, perm):
            src = os.path.join(RUN, DIRS[(site, b)]); im = Image.open(os.path.join(src, f'{f:04d}.png')).convert('RGB'); W, H = im.size
            im.resize((1280, 720), Image.LANCZOS).save(os.path.join(d, f'{s}.jpg'), quality=90)
            seq = Image.new('RGB', (W, H))
            for k in range(4):
                c = Image.open(os.path.join(src, f'{f + k:04d}.png')).convert('RGB').crop((W // 4, H // 4, 3 * W // 4, 3 * H // 4))
                seq.paste(c, ((k % 2) * W // 2, (k // 2) * H // 2))
            seq.resize((1280, 720), Image.LANCZOS).save(os.path.join(d, f'{s}_seq.jpg'), quality=92)
        key[it] = {'site': site, 'f': f, **dict(zip(slots, perm))}
    json.dump(key, open(os.path.join(OUT, 'key.json'), 'w'), indent=1, ensure_ascii=False); print(key)

def call(it, rk):
    if spent() >= STOP: return 'dung-tran'
    k = json.load(open(os.path.join(OUT, 'key.json')))[it]; slots = [s for s in 'XYZ' if s in k]
    sj = ', '.join(f'"{s}": {{"craft": <int>, "detail": <int>, "period": <int>, "ai_look": <int>, "flicker": "yes|no", "flags": [..], "note": "<short>"}}' for s in slots)
    prompt = PROMPT.format(persona=RATERS[rk], n=len(slots), slots=', '.join(slots), year=YEAR[k['site']], slotjson=sj)
    env = dict(os.environ, ANTHROPIC_API_KEY=os.environ['CONSOLE_API_KEY'])
    with tempfile.TemporaryDirectory() as cwd:
        for s in slots:
            for suf in ('.jpg', '_seq.jpg'): shutil.copy(os.path.join(OUT, it, s + suf), cwd)
        for _ in range(2):
            r = subprocess.run(['claude', '-p', '--model', MODEL, '--output-format', 'json', '--allowedTools', 'Read'], input=prompt, capture_output=True, text=True, env=env, cwd=cwd, timeout=900)
            try: d = json.loads(r.stdout)
            except Exception: continue
            with open(LOG, 'a') as fh: fh.write(json.dumps({'tag': f'pt3:{it}-{rk}', 'model': MODEL, 'served': sorted(d.get('modelUsage', {})), 'usd': d.get('total_cost_usd', 0)}) + '\n')
            open(os.path.join(OUT, it, f'{rk}.raw.txt'), 'w').write(d.get('result', ''))
            m = re.search(r'\{.*\}', d.get('result', ''), re.S)
            if m:
                try: j = json.loads(m.group(0)); json.dump(j, open(os.path.join(OUT, it, f'{rk}.json'), 'w'), indent=1); return True
                except Exception: pass
    return False

def run():
    for it in ITEMS:
        jobs = [rk for rk in RATERS if not os.path.exists(os.path.join(OUT, it, f'{rk}.json'))]
        if spent() >= STOP: print('DỪNG trần', round(spent(), 3)); break
        with ThreadPoolExecutor(3) as ex: res = list(ex.map(lambda rk: call(it, rk), jobs))
        print(it, res, round(spent(), 3), flush=True)

def score():
    key = json.load(open(os.path.join(OUT, 'key.json'))); rows = {}; tot = {}
    for it, k in key.items():
        J = {rk: json.load(open(os.path.join(OUT, it, f'{rk}.json'))) for rk in RATERS if os.path.exists(os.path.join(OUT, it, f'{rk}.json'))}
        row = {}
        for s in [s for s in 'XYZ' if s in k]:
            b = k[s]; T = tot.setdefault((k['site'], b), {m: [] for m in ('craft', 'detail', 'period', 'ai_look', 'flicker')})
            for m in ('craft', 'detail', 'period', 'ai_look'):
                v = [J[r][s][m] for r in J]; row[f'{b}_{m}'] = v; T[m] += v
            fl = [str(J[r][s].get('flicker', '')).lower().startswith('y') for r in J]; row[f'{b}_flicker_yes'] = sum(fl); T['flicker'] += fl
            row[f'{b}_flags'] = sorted({x for r in J for x in J[r][s].get('flags', [])})
        row['best'] = {r: k.get(J[r].get('best'), '?') for r in J}; row['worst'] = {r: k.get(J[r].get('worst'), '?') for r in J}
        row['why'] = {r: J[r].get('why') for r in J}; row['anachronisms'] = {r: J[r].get('anachronisms_seen') for r in J}; rows[it] = row
    tb = {f'{s}/{b}': {m: (round(sum(v) / len(v), 2) if m != 'flicker' else f'{sum(v)}/{len(v)}') for m, v in d.items() if v} for (s, b), d in tot.items()}
    R = {'muc': rows, 'tb': tb, 'chi_phi': round(spent(), 3)}
    json.dump(R, open(os.path.join(OUT, 'score.json'), 'w'), indent=1, ensure_ascii=False); print(json.dumps(tb, ensure_ascii=False), R['chi_phi'])

if __name__ == '__main__':
    {'set': setup, 'run': run, 'score': score}[sys.argv[1]]()
