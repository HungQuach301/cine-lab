#!/opt/cine/bin/python
"""V5b-2b · CHẤM MÙ ĐOẠN THỬ V5b-2b-T (giao thức blind_g2 — channel-k2/k2c-t2-01/blind_g2.py): `claude -p` GHIM claude-sonnet-5-5, chỉ công cụ Read,
thư mục tạm trống chỉ chứa X.jpg/Y.jpg, 3 vai (PROMPT/RATERS nạp nguyên văn từ channel-k2/k2v2-mau/blind_v2.py), thang tuyệt đối (5 = video faceless thường).
6 cặp: khung V5b-2b-T (master 1080p, giây KHAI TRƯỚC khi có master — CAP dưới đây) ↔ khung gib20 V5b-2a CÙNG LOẠI CẢNH (ảnh 1080p đã commit
channel-k2/k2c-t3-01/v5b1-thu/v5b2a/khung/, thu về 1280 px như grab). Thứ tự X/Y: hạt giống cố định 20261017. Không sửa sau khi chấm.
Sổ chi phí reports/v5b2b/kiem-mu/cost.jsonl; trần phiên $2, dừng $1,8. Khung đối thủ không có trong repo — phần so đối thủ do Claude điều phối ở chat.
  blind_v5b2b.py set <master.mp4> · blind_v5b2b.py run · blind_v5b2b.py score"""
import importlib.util, json, os, random, re, shutil, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
OUT = os.path.join(HERE, 'kiem-mu'); LOG = os.path.join(OUT, 'cost.jsonl')
spec = importlib.util.spec_from_file_location('bv2', os.path.join(REPO, 'channel-k2', 'k2v2-mau', 'blind_v2.py')); BV2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(BV2)
PROMPT, RATERS, MODEL, grab = BV2.PROMPT, BV2.RATERS, BV2.MODEL, BV2.grab
assert MODEL == 'claude-sonnet-5-5'
CAP, STOP = 2.0, 1.8
G20 = os.path.join(REPO, 'channel-k2', 'k2c-t3-01', 'v5b1-thu', 'v5b2a', 'khung')
# khai 17/10 TRƯỚC khi có master V5b-2b-T (giây theo đặc tả reports/v5b2b/doan-thu/episode.yaml)
PAIRS = {
    'P1': dict(kind='low aerial flight toward a place (route flight)', t=2.0, g20='eo-dat-1-bay-tuyen-wca-1907.jpg'),
    'P2': dict(kind='orbit around a landmark at a frozen key date', t=8.3, g20='can-hero-2-moc-dinh-1941-orbit.jpg'),
    'P3': dict(kind='close view of a historic landmark structure', t=6.4, g20='can-hero-1-thap-homage.jpg'),
    'P4': dict(kind='wide reveal of the whole place', t=16.6, g20='toan-canh-2-ket-2026.jpg'),
    'P5': dict(kind='3D street view of a dense old town with buildings', t=21.0, g20='pho-day-pho-co-1753.jpg'),
    'P6': dict(kind='3D town overview with landmark', t=24.6, g20='can-hero-3-thap-pho-quanh-1885.jpg'),
}


def spent():
    return sum(json.loads(l)['usd'] for l in open(LOG)) if os.path.exists(LOG) else 0.0


def setup(master):
    os.makedirs(OUT, exist_ok=True); R = random.Random(20261017); key = {}
    for pid, P in PAIRS.items():
        new_is_x = R.random() < 0.5; d = os.path.join(OUT, pid); os.makedirs(d, exist_ok=True)
        grab(master, P['t'], os.path.join(d, 'X.jpg' if new_is_x else 'Y.jpg'))
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', os.path.join(G20, P['g20']), '-vf', 'scale=1280:-2', '-q:v', '3', os.path.join(d, 'Y.jpg' if new_is_x else 'X.jpg')], check=True)
        key[pid] = dict(kind=P['kind'], moi='X' if new_is_x else 'Y', gib20='Y' if new_is_x else 'X', moi_s=P['t'], gib20_khung=P['g20'])
    json.dump(key, open(os.path.join(OUT, 'key.json'), 'w'), indent=1); print(json.dumps(key, indent=1))


def call(pid, rk):
    if spent() > STOP: raise SystemExit(f'dừng: đã tiêu ${spent():.2f}')
    key = json.load(open(os.path.join(OUT, 'key.json'))); prompt = PROMPT.format(persona=RATERS[rk], kind=key[pid]['kind'])
    env = dict(os.environ, ANTHROPIC_API_KEY=os.environ['CONSOLE_API_KEY'])
    with tempfile.TemporaryDirectory() as cwd:
        for f in ('X.jpg', 'Y.jpg'): shutil.copy(os.path.join(OUT, pid, f), cwd)
        for _ in range(2):
            r = subprocess.run(['claude', '-p', '--model', MODEL, '--output-format', 'json', '--allowedTools', 'Read'], input=prompt, capture_output=True, text=True, env=env, cwd=cwd, timeout=900)
            try: d = json.loads(r.stdout)
            except Exception: continue
            with open(LOG, 'a') as f: f.write(json.dumps({'tag': f'v5b2b:{pid}-{rk}', 'model': MODEL, 'served': sorted(d.get('modelUsage', {})), 'usd_by_model': {m: round(u.get('costUSD', 0), 5) for m, u in d.get('modelUsage', {}).items()}, 'usd': d.get('total_cost_usd', 0)}) + '\n')
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
    key = json.load(open(os.path.join(OUT, 'key.json'))); rows = []; allm = []
    for pid, k in key.items():
        J = [json.load(open(os.path.join(OUT, pid, f'{rk}.json'))) for rk in RATERS if os.path.exists(os.path.join(OUT, pid, f'{rk}.json'))]
        if not J: continue
        cm = [j[k['moi']]['craft'] for j in J]; cg = [j[k['gib20']]['craft'] for j in J]; allm += cm
        rows.append(dict(cap=pid, kind=k['kind'], moi=round(sum(cm) / len(cm), 2), gib20=round(sum(cg) / len(cg), 2), moi_tung_nguoi=cm, gib20_tung_nguoi=cg,
                         chon_moi=f"{sum(1 for j in J if j.get('better') == k['moi'])}/{len(J)}", co_moi=sorted({f for j in J for f in j[k['moi']].get('flags', [])}),
                         doc_moi=round(sum(j[k['moi']]['readability'] for j in J) / len(J), 2), ro_moi=round(sum(j[k['moi']]['clarity'] for j in J) / len(J), 2),
                         sua_yeu_hon=[j.get('top_fix_for_weaker') for j in J], thua=sum(cm) < sum(cg)))
    R = dict(cap=rows, tb_moi=round(sum(allm) / max(1, len(allm)), 2), tb_gib20=round(sum(r['gib20'] for r in rows) / max(1, len(rows)), 2), thua_cap=[r['cap'] for r in rows if r['thua']], chi_phi=round(spent(), 2))
    json.dump(R, open(os.path.join(OUT, 'score.json'), 'w'), indent=1, ensure_ascii=False); print(json.dumps(R, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    a = sys.argv[1]
    if a == 'set': setup(sys.argv[2])
    elif a == 'run': run()
    elif a == 'score': score()
