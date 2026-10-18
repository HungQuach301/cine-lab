#!/opt/cine/bin/python
"""V6 · CHẤM MÙ 3 BẢN CÙNG LOẠI CẢNH: TỐT NHẤT (Cycles) · SẢN XUẤT (llvmpipe V6) · V5b-2d — giao thức như blind_v5b2d.py: `claude -p` ghim claude-sonnet-5-5,
chỉ công cụ Read, thư mục tạm chỉ chứa A.jpg/B.jpg/C.jpg (khung SẠCH 1280 px), 3 vai RATERS nguyên văn channel-k2/k2v2-mau/blind_v2.py, thứ tự A/B/C hoán vị theo hạt giống
20261018 (mỗi loại một lần), mô tả TRUNG TÍNH theo loại cảnh (không nói bản nào mới). KHÔNG khung đối thủ (điều phối chấm cổng trong chat).
Thang: craft, detail 1–10; toy_like, ai_look 0–10; period 1–10 (đúng thời kỳ 1782); xếp hạng. Chấm mù KHÔNG thay kiểm dữ kiện (Kinh thánh §11.3).
  blind_v6.py set <thư mục tot> <thư mục khung sx> · run · score        (tot: tot-<k>.png; sx: sach-<k>/*.jpg; V5b-2d: reports/v5b2d/khung/d-*.jpg)"""
import glob, importlib.util, json, os, random, re, shutil, subprocess, sys, tempfile, itertools
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
OUT = os.path.join(HERE, 'kiem-mu'); LOG = os.path.join(OUT, 'cost.jsonl')
spec = importlib.util.spec_from_file_location('bv2', os.path.join(REPO, 'channel-k2', 'k2v2-mau', 'blind_v2.py')); BV2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(BV2)
RATERS, MODEL = BV2.RATERS, BV2.MODEL
assert MODEL == 'claude-sonnet-5-5'
OLD = os.path.join(REPO, 'reports', 'v5b2d', 'khung')
TYPES = {1: ('siege', 'a siege scene: the besiegers\' lines and troops on the isthmus in front of a fortified rock and town, 1782', 'd-1-vay-ham.jpg'),
         2: ('harbour', 'a harbour / waterfront scene of an 18th-century fortified port town with ships', 'd-2-cang-bo.jpg'),
         3: ('dense_street', 'a dense old-town scene of an 18th-century fortified port town (partly in ruins after bombardment), seen from low altitude', 'd-3-pho-day.jpg'),
         4: ('hero_fort', 'a hero shot of one 18th-century gun bastion during a battle', 'd-4-hero.jpg'),
         5: ('panorama', 'a crowded panorama of an 18th-century fortified town with its garrison', 'd-5-toan-canh.jpg'),
         6: ('shore_battle', 'a shore-and-battle scene: floating gun batteries attacking a fortified town from the sea, 1782', 'd-6-bo-chien-su.jpg')}
PROMPT = """{persona}

In the current folder there are three still frames, A.jpg, B.jpg and C.jpg: three versions of the same shot type from a stylised 3D animated history documentary — {kind}. Open all three with the Read tool. Judge only what you see. Be honest and specific; do not be polite.

For EACH version score:
- craft (1–10): composition, lighting, colour, materials, overall visual quality (10 = top-tier cinematic 3D history animation, 5 = typical faceless YouTube 3D explainer, 1 = broken)
- detail (1–10): amount and quality of believable detail (buildings, troops, people, ships, smoke, terrain)
- toy_like (0–10): do the people, troops, ships or buildings look like toys / game pieces? 0 = not at all, 10 = clearly toy-like
- ai_look (0–10): does it look AI-generated? 0 = not at all, 10 = obviously
- period (1–10): does everything look right for 1782 (architecture, uniforms, ships, objects)? 10 = fully convincing
- flags: any of "broken_render", "empty_frame", "flat_slide_look", "toy_look", "cluttered", "confusing", "unreadable_scale", "anachronism", or [].

Return ONLY JSON:
{{"A": {{"craft": <int>, "detail": <int>, "toy_like": <int>, "ai_look": <int>, "period": <int>, "flags": [..], "note": "<short>"}},
 "B": {{...same keys...}}, "C": {{...same keys...}},
 "rank": ["<best letter>", "<second>", "<third>"], "why": "<one sentence>", "top_fix_for_best": "<concrete>"}}"""


def spent(): return sum(json.loads(l)['usd'] for l in open(LOG)) if os.path.exists(LOG) else 0.0


def setup(tot, sx):
    os.makedirs(OUT, exist_ok=True); R = random.Random(20261018); key = {}
    for k, (short, kind, old) in TYPES.items():
        d = os.path.join(OUT, f'P{k}'); os.makedirs(d, exist_ok=True)
        src = {'tot': os.path.join(tot, f'tot-{k}.png'), 'sx': glob.glob(os.path.join(sx, f'sach-{k}', '*.jpg'))[0], 'v5b2d': os.path.join(OLD, old)}
        order = list(src); R.shuffle(order); lab = dict(zip(order, 'ABC'))
        for v, p in src.items(): Image.open(p).convert('RGB').resize((1280, 720), Image.LANCZOS).save(os.path.join(d, lab[v] + '.jpg'), quality=92)
        key[f'P{k}'] = dict(short=short, kind=kind, nhan=lab, tep={v: os.path.relpath(p, REPO) if p.startswith(REPO) else p for v, p in src.items()})
    json.dump(key, open(os.path.join(OUT, 'key.json'), 'w'), indent=1); print(json.dumps(key, indent=1))


def call(pid, rk):
    if spent() > 4.5: raise SystemExit(f'dừng: đã tiêu ${spent():.2f}')
    key = json.load(open(os.path.join(OUT, 'key.json'))); prompt = PROMPT.format(persona=RATERS[rk], kind=key[pid]['kind'])
    with tempfile.TemporaryDirectory() as cwd:
        for f in ('A.jpg', 'B.jpg', 'C.jpg'): shutil.copy(os.path.join(OUT, pid, f), cwd)
        for _ in range(2):
            r = subprocess.run(['claude', '-p', '--model', MODEL, '--output-format', 'json', '--allowedTools', 'Read'], input=prompt, capture_output=True, text=True, cwd=cwd, timeout=900)
            try: d = json.loads(r.stdout)
            except Exception: continue
            with open(LOG, 'a') as f: f.write(json.dumps({'tag': f'v6:{pid}-{rk}', 'model': MODEL, 'served': sorted(d.get('modelUsage', {})), 'usd': d.get('total_cost_usd', 0)}) + '\n')
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
    print(dict(zip([f'{a}-{b}' for a, b in jobs], res)), f'chi phí ${spent():.3f}')


def score():
    key = json.load(open(os.path.join(OUT, 'key.json'))); R = {}; M = ('craft', 'detail', 'toy_like', 'ai_look', 'period')
    for pid, k in key.items():
        J = {rk: json.load(open(os.path.join(OUT, pid, f'{rk}.json'))) for rk in RATERS if os.path.exists(os.path.join(OUT, pid, f'{rk}.json'))}
        row = dict(loai=k['short'], nguoi=len(J))
        for v, lab in k['nhan'].items():
            row[v] = {m: round(sum(J[r][lab][m] for r in J) / max(1, len(J)), 2) for m in M}
            row[v]['flags'] = sorted({f for r in J for f in J[r][lab].get('flags', [])}); row[v]['note'] = [J[r][lab].get('note') for r in J]
            row[v]['hang1'] = sum(1 for r in J if J[r].get('rank', [None])[0] == lab)
        row['why'] = [J[r].get('why') for r in J]; row['sua_ban_tot'] = [J[r].get('top_fix_for_best') for r in J]; R[pid] = row
    for v in ('tot', 'sx', 'v5b2d'):
        R['tb_' + v] = {m: round(sum(R[p][v][m] for p in key) / len(key), 2) for m in M}; R['tb_' + v]['hang1'] = sum(R[p][v]['hang1'] for p in key)
    R['chi_phi'] = round(spent(), 3)
    json.dump(R, open(os.path.join(OUT, 'score.json'), 'w'), indent=1, ensure_ascii=False)
    for p in key: print(p, R[p]['loai'], {v: (R[p][v]['craft'], R[p][v]['toy_like'], R[p][v]['hang1']) for v in ('tot', 'sx', 'v5b2d')})
    print({k: v for k, v in R.items() if k.startswith('tb_')}, 'chi phí', R['chi_phi'])


if __name__ == '__main__':
    a = sys.argv[1]
    if a == 'set': setup(sys.argv[2], sys.argv[3])
    elif a == 'run': run()
    elif a == 'score': score()
