#!/opt/cine/bin/python
"""G1b-T3 · CHẤM MÙ toy_like (1–10, thấp = ít giống đồ chơi) — giao thức như reports/v6/blind_v6.py: `claude -p` ghim claude-sonnet-5-5, chỉ công cụ Read,
thư mục tạm chỉ chứa ảnh đã đổi tên ngẫu nhiên (1280 px, khung sạch). 3 vai (người xem YouTube lịch sử · hoạ sĩ dựng 3D · sử gia quân sự).
Mỗi lượt: một vai thấy 6 ảnh (khung neo 1782, khung neo 1943, P4 trước/sau, P5 trước/sau) với tên và thứ tự hoán vị riêng (hạt 20261018 + lượt), chấm TỪNG ảnh.
  blind_toy.py set · run · score"""
import json, os, random, re, shutil, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
OUT = os.path.join(HERE, 'cham-mu'); LOG = os.path.join(OUT, 'cost.jsonl'); MODEL = 'claude-sonnet-5-5'
G = '/var/tmp/cine-out/g1b/nguoi'
SRC = {'neo1782': os.path.join(REPO, 'reports/v6/khung-neo/khung/1782-trua-LAI-notext.jpg'),
       'neo1943': os.path.join(REPO, 'reports/v6/khung-neo/khung/1943-trua-LAI-notext.jpg'),
       'P4_truoc': f'{G}/truoc-4/00192.jpg', 'P4_sau': f'{G}/sau-4/00192.jpg',
       'P5_truoc': f'{G}/truoc-5/00072.jpg', 'P5_sau': f'{G}/sau-5/00072.jpg'}
RATERS = {
  'R1': "You are a regular YouTube viewer who watches history documentaries (military history, empires, sieges) on a TV and a phone, and you have seen many 3D-animated history channels.",
  'R2': "You are a senior 3D artist (characters and environments) who has shipped work on animated feature films and high-end documentary CGI; you judge models, proportions, materials and lighting.",
  'R3': "You are a military historian specialising in 18th- and 20th-century armies who consults on historical films; you judge whether soldiers and civilians look like real people of their period or like miniatures.",
}
ROUNDS = 2
PROMPT = """{persona}

In the current folder there are {n} still frames ({names}) from stylised 3D/composited history documentaries (Gibraltar in 1782 and in 1943). Open every one with the Read tool. Judge each frame ON ITS OWN, only from what you see. Be honest and specific; do not be polite.

For EACH frame score:
- toy_like (1–10): do the PEOPLE (soldiers, civilians, crews) look like toys / miniatures / game pieces? 1 = they read as real people, 10 = clearly toy figurines
- people_craft (1–10): quality of the people (proportions, poses, clothing, how they sit in the light and on the ground)
- note: what most makes the people look toy-like or real (short)

Return ONLY JSON: {{"<file name>": {{"toy_like": <int>, "people_craft": <int>, "note": "<short>"}}, ...one entry per file...}}"""


def spent(): return sum(json.loads(l)['usd'] for l in open(LOG)) if os.path.exists(LOG) else 0.0


def setup():
    os.makedirs(OUT, exist_ok=True); key = {}
    for rd in range(ROUNDS):
        for rk in RATERS:
            R = random.Random(f'20261018-{rd}-{rk}'); ids = list(SRC); R.shuffle(ids); names = R.sample(range(10, 99), len(ids))
            d = os.path.join(OUT, f'L{rd}-{rk}'); os.makedirs(d, exist_ok=True); m = {}
            for v, nm in zip(ids, names):
                fn = f'frame_{nm}.jpg'; Image.open(SRC[v]).convert('RGB').resize((1280, 720), Image.LANCZOS).save(os.path.join(d, fn), quality=92); m[fn] = v
            key[f'L{rd}-{rk}'] = {'order': list(m), 'map': m}
    json.dump({'key': key, 'src': {k: os.path.relpath(v, REPO) if v.startswith(REPO) else v for k, v in SRC.items()}}, open(os.path.join(OUT, 'key.json'), 'w'), indent=1)


def call(job):
    if spent() > 3.0: raise SystemExit(f'dừng: đã tiêu ${spent():.2f}')
    key = json.load(open(os.path.join(OUT, 'key.json')))['key'][job]; rk = job.split('-')[1]
    prompt = PROMPT.format(persona=RATERS[rk], n=len(key['order']), names=', '.join(key['order']))
    with tempfile.TemporaryDirectory() as cwd:
        for f in key['order']: shutil.copy(os.path.join(OUT, job, f), cwd)
        for _ in range(2):
            r = subprocess.run(['claude', '-p', '--model', MODEL, '--output-format', 'json', '--allowedTools', 'Read'], input=prompt, capture_output=True, text=True, cwd=cwd, timeout=900)
            try: d = json.loads(r.stdout)
            except Exception: continue
            with open(LOG, 'a') as f: f.write(json.dumps({'tag': f'g1b-t3:{job}', 'model': MODEL, 'served': sorted(d.get('modelUsage', {})), 'usd': d.get('total_cost_usd', 0)}) + '\n')
            open(os.path.join(OUT, job, 'raw.txt'), 'w').write(d.get('result', ''))
            m = re.search(r'\{.*\}', d.get('result', ''), re.S)
            if m:
                try: j = json.loads(m.group(0)); json.dump(j, open(os.path.join(OUT, job, 'phieu.json'), 'w'), indent=1); return True
                except Exception: pass
    return False


def run():
    key = json.load(open(os.path.join(OUT, 'key.json')))['key']
    jobs = [j for j in key if not os.path.exists(os.path.join(OUT, j, 'phieu.json'))]
    with ThreadPoolExecutor(3) as ex: res = list(ex.map(call, jobs))
    print(dict(zip(jobs, res)), f'chi phí ${spent():.3f}')


def score():
    key = json.load(open(os.path.join(OUT, 'key.json')))['key']; S = {v: {'toy_like': [], 'people_craft': [], 'by': {}} for v in SRC}
    for job, k in key.items():
        p = os.path.join(OUT, job, 'phieu.json')
        if not os.path.exists(p): continue
        ph = json.load(open(p))
        for fn, v in k['map'].items():
            e = ph.get(fn) or ph.get(fn.replace('.jpg', ''))
            if not e: continue
            S[v]['toy_like'].append(e['toy_like']); S[v]['people_craft'].append(e['people_craft']); S[v]['by'][job] = [e['toy_like'], e['people_craft'], e.get('note', '')]
    res = {v: {'toy_like_tb': round(sum(s['toy_like']) / len(s['toy_like']), 2), 'people_craft_tb': round(sum(s['people_craft']) / len(s['people_craft']), 2), 'n': len(s['toy_like']), 'phieu': s['by']} for v, s in S.items() if s['toy_like']}
    res['_chi_phi_usd'] = round(spent(), 4)
    json.dump(res, open(os.path.join(OUT, 'score.json'), 'w'), indent=1, ensure_ascii=False)
    for v, r in res.items():
        if not v.startswith('_'): print(v, r['toy_like_tb'], r['people_craft_tb'], r['n'])
    print('chi phí', res['_chi_phi_usd'])


if __name__ == '__main__':
    {'set': setup, 'run': run, 'score': score}[sys.argv[1]]()
