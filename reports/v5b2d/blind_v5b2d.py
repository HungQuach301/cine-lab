#!/opt/cine/bin/python
"""V5b-2d · CHẤM MÙ 6 CẶP KHUNG CÙNG LOẠI CẢNH: V5b-2d ↔ V5b-2c (giao thức blind_v5b2c: `claude -p` ghim claude-sonnet-5-5, chỉ công cụ Read, thư mục tạm chỉ
chứa 2 ảnh, 3 vai RATERS nguyên văn của channel-k2/k2v2-mau/blind_v2.py). KHÔNG đưa khung đối thủ (CITYTONS/Barcelona) vào repo hay API — điều phối chấm cổng riêng.
Khung SẠCH (không lớp chữ) 1080p → 1280 px cả hai bản; nhãn phiên bản ẩn (X/Y theo hạt giống 20261018, mỗi cặp một lần tung).
Mô tả cho người chấm TRUNG TÍNH theo loại cảnh (không nói bản nào mới). Sổ chi phí kiem-mu/cost.jsonl; trần $2, dừng $1,8.
  blind_v5b2d.py set <thư mục khung v5b2d_khung.sh> · blind_v5b2d.py run · blind_v5b2d.py score"""
import importlib.util, json, os, random, re, shutil, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
OUT = os.path.join(HERE, 'kiem-mu'); LOG = os.path.join(OUT, 'cost.jsonl')
spec = importlib.util.spec_from_file_location('bv2', os.path.join(REPO, 'channel-k2', 'k2v2-mau', 'blind_v2.py')); BV2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(BV2)
RATERS, MODEL = BV2.RATERS, BV2.MODEL
assert MODEL == 'claude-sonnet-5-5'
CAP, STOP = 2.0, 1.8
OLD = os.path.join(REPO, 'reports', 'v5b2c', 'khung')
PAIRS = {1: ('siege', 'a siege scene: the besiegers\' lines on the isthmus in front of a fortified rock and town, 1782', 'v0-1-vay-ham.jpg'),
         2: ('harbour', 'a harbour / waterfront scene of an 18th-century fortified port town with ships', 'v0-2-cang-bo.jpg'),
         3: ('dense_street', 'a dense old-town street scene of an 18th-century fortified port town, seen from low altitude', 'v0-3-pho-day.jpg'),
         4: ('hero_fort', 'a hero shot of one 18th-century gun bastion during a battle', 'v0-4-hero.jpg'),
         5: ('panorama', 'a crowded panorama of an 18th-century fortified town', 'v0-5-toan-canh.jpg'),
         6: ('shore_battle', 'a shore-and-battle scene: floating gun batteries attacking a fortified town from the sea, 1782', 'v0-6-bien-chien-su.jpg')}
PROMPT = """{persona}

In the current folder there are two still frames, X.jpg and Y.jpg: two versions of the same shot type from a stylised 3D animated history documentary — {kind}. Open both with the Read tool. Judge only what you see. Be honest and specific; do not be polite.

For EACH version score 1–10:
- craft: composition, lighting, colour, overall visual quality (10 = top-tier cinematic 3D city/history animation, 5 = typical faceless YouTube 3D explainer, 1 = broken)
- richness: how full and alive the frame is with meaningful content for this shot type (troops, ships, buildings, people, smoke, detail) versus empty ground/water/sky
- fit: how well the frame delivers this shot type ({short})
- flags: any of "broken_render", "empty_frame", "flat_slide_look", "toy_look", "cluttered", "confusing", "unreadable_scale", or [].

Return ONLY JSON:
{{"X": {{"craft": <int>, "richness": <int>, "fit": <int>, "flags": [..], "note": "<short>"}},
 "Y": {{"craft": <int>, "richness": <int>, "fit": <int>, "flags": [..], "note": "<short>"}},
 "better": "X|Y|tie", "why": "<one sentence>", "top_fix_for_weaker": "<concrete>", "top_fix_for_better": "<concrete>"}}"""


def spent():
    return sum(json.loads(l)['usd'] for l in open(LOG)) if os.path.exists(LOG) else 0.0


def setup(kdir):
    os.makedirs(OUT, exist_ok=True); R = random.Random(20261018); key = {}
    for k, (short, kind, old) in PAIRS.items():
        d = os.path.join(OUT, f'P{k}'); os.makedirs(d, exist_ok=True); new_is_x = R.random() < 0.5
        import glob
        new = glob.glob(os.path.join(kdir, f'sach-{k}', '*.jpg'))[0]
        for src, lab in ((new, 'X' if new_is_x else 'Y'), (os.path.join(OLD, old), 'Y' if new_is_x else 'X')):
            Image.open(src).convert('RGB').resize((1280, 720), Image.LANCZOS).save(os.path.join(d, f'{lab}.jpg'), quality=92)
        key[f'P{k}'] = dict(short=short, kind=kind, v5b2d='X' if new_is_x else 'Y', v5b2c='Y' if new_is_x else 'X', moi=os.path.relpath(new, kdir), cu=old)
    json.dump(key, open(os.path.join(OUT, 'key.json'), 'w'), indent=1); print(json.dumps(key, indent=1))


def call(pid, rk):
    if spent() > STOP: raise SystemExit(f'dừng: đã tiêu ${spent():.2f}')
    key = json.load(open(os.path.join(OUT, 'key.json')))
    prompt = PROMPT.format(persona=RATERS[rk], kind=key[pid]['kind'], short=key[pid]['short'].replace('_', ' '))
    env = dict(os.environ, ANTHROPIC_API_KEY=os.environ['CONSOLE_API_KEY'])
    with tempfile.TemporaryDirectory() as cwd:
        for f in ('X.jpg', 'Y.jpg'): shutil.copy(os.path.join(OUT, pid, f), cwd)
        for _ in range(2):
            r = subprocess.run(['claude', '-p', '--model', MODEL, '--output-format', 'json', '--allowedTools', 'Read'], input=prompt, capture_output=True, text=True, env=env, cwd=cwd, timeout=900)
            try: d = json.loads(r.stdout)
            except Exception: continue
            with open(LOG, 'a') as f: f.write(json.dumps({'tag': f'v5b2d:{pid}-{rk}', 'model': MODEL, 'served': sorted(d.get('modelUsage', {})), 'usd_by_model': {m: round(u.get('costUSD', 0), 5) for m, u in d.get('modelUsage', {}).items()}, 'usd': d.get('total_cost_usd', 0)}) + '\n')
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
    key = json.load(open(os.path.join(OUT, 'key.json'))); R = {}
    for pid, k in key.items():
        J = {rk: json.load(open(os.path.join(OUT, pid, f'{rk}.json'))) for rk in RATERS if os.path.exists(os.path.join(OUT, pid, f'{rk}.json'))}
        row = dict(loai=k['short'], nguoi=len(J))
        for lab in ('v5b2d', 'v5b2c'):
            v = k[lab]; row[lab] = {m: [J[r][v][m] for r in J] for m in ('craft', 'richness', 'fit')}
            for m in ('craft', 'richness', 'fit'): row[lab]['tb_' + m] = round(sum(row[lab][m]) / max(1, len(J)), 2)
            row[lab]['flags'] = sorted({f for r in J for f in J[r][v].get('flags', [])}); row[lab]['note'] = [J[r][v].get('note') for r in J]
        row['chon_v5b2d'] = f"{sum(1 for r in J if J[r].get('better') == k['v5b2d'])}/{len(J)}"; row['hoa'] = sum(1 for r in J if J[r].get('better') == 'tie')
        row['why'] = [J[r].get('why') for r in J]; row['sua_ban_tot'] = [J[r].get('top_fix_for_better') for r in J]; row['sua_ban_yeu'] = [J[r].get('top_fix_for_weaker') for r in J]
        R[pid] = row
    R['chi_phi'] = round(spent(), 3)
    json.dump(R, open(os.path.join(OUT, 'score.json'), 'w'), indent=1, ensure_ascii=False)
    for pid, row in R.items():
        if pid == 'chi_phi': continue
        print(pid, row['loai'], 'craft 2d', row['v5b2d']['tb_craft'], '2c', row['v5b2c']['tb_craft'], '| giàu', row['v5b2d']['tb_richness'], row['v5b2c']['tb_richness'], '| hợp', row['v5b2d']['tb_fit'], row['v5b2c']['tb_fit'], '| chọn 2d', row['chon_v5b2d'])
    print('chi phí', R['chi_phi'])


# --- SM3 tách: độ rõ (giao thức V5b-2c PROMPT_ONE + đáp án khai trước KEYS['SM3'] của blind_v5b2c.py) — 8 khung: X1–X4 = SM3a, X5–X8 = SM3b ---
def sm3(master):
    sp = importlib.util.spec_from_file_location('b2c', os.path.join(REPO, 'reports', 'v5b2c', 'blind_v5b2c.py')); B = importlib.util.module_from_spec(sp); sp.loader.exec_module(B)
    d = os.path.join(OUT, 'SM3tach'); os.makedirs(d, exist_ok=True); T = [0.8, 1.8, 2.8, 3.3, 4.3, 5.2, 6.0, 6.6]
    for i, t in enumerate(T, 1): subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{t:.2f}', '-i', master, '-frames:v', '1', '-vf', 'scale=1280:-2', '-q:v', '3', os.path.join(d, f'X{i}.jpg')], check=True)
    prompt0 = B.PROMPT_ONE.replace('four still frames from one short animated map ({kind}): X1.jpg–X4.jpg, in time order over about 7 seconds. Open all four',
        'eight still frames from two consecutive short shots of an animated map ({kind}): X1.jpg–X4.jpg are shot 1 and X5.jpg–X8.jpg are shot 2, each in time order over about 3.5 seconds. Open all eight')
    prompt0 = prompt0.replace('Finally say whether the two periods shown would be clearer as two separate shots ("split": true/false) and why.', 'Finally say whether splitting the two periods into these two shots works ("split": true/false = keep split / merge back) and why.')
    env = dict(os.environ, ANTHROPIC_API_KEY=os.environ['CONSOLE_API_KEY']); res = {}
    for rk in RATERS:
        if os.path.exists(os.path.join(d, f'{rk}.json')): continue
        if spent() > 1.9: break
        with tempfile.TemporaryDirectory() as cwd:
            for i in range(1, 9): shutil.copy(os.path.join(d, f'X{i}.jpg'), cwd)
            r = subprocess.run(['claude', '-p', '--model', MODEL, '--output-format', 'json', '--allowedTools', 'Read'], input=prompt0.format(persona=RATERS[rk], kind=B.KIND['SM3']), capture_output=True, text=True, env=env, cwd=cwd, timeout=900)
            dd = json.loads(r.stdout)
            with open(LOG, 'a') as f: f.write(json.dumps({'tag': f'v5b2d:SM3tach-{rk}', 'model': MODEL, 'served': sorted(dd.get('modelUsage', {})), 'usd': dd.get('total_cost_usd', 0)}) + '\n')
            m = re.search(r'\{.*\}', dd.get('result', ''), re.S); j = json.loads(m.group(0)); json.dump(j, open(os.path.join(d, f'{rk}.json'), 'w'), indent=1)
    J = {rk: json.load(open(os.path.join(d, f'{rk}.json'))) for rk in RATERS if os.path.exists(os.path.join(d, f'{rk}.json'))}
    R = dict(nguoi=len(J), craft=[J[r]['X']['craft'] for r in J], clarity=[J[r]['X']['clarity'] for r in J], readability=[J[r]['X']['readability'] for r in J],
             dung=[B.right('SM3', J[r]['X']) for r in J], tra_loi=[{q: J[r]['X'].get(q) for q in ('from', 'route', 'when', 'where')} for r in J], flags=sorted({f for r in J for f in J[r]['X'].get('flags', [])}),
             giu_tach=[J[r].get('split') for r in J], why=[J[r].get('why_split') for r in J], top_fix=[J[r].get('top_fix') for r in J], chi_phi=round(spent(), 3), so_v5b2c=dict(craft=[6, 6, 6], clarity=[4, 4, 4]))
    json.dump(R, open(os.path.join(d, 'score.json'), 'w'), indent=1, ensure_ascii=False); print(json.dumps(R, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    a = sys.argv[1]
    if a == 'sm3': sm3(sys.argv[2])
    if a == 'set': setup(sys.argv[2])
    elif a == 'run': run()
    elif a == 'score': score()
