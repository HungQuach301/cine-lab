#!/opt/cine/bin/python
"""K2C-T2-01 · RÀ GU trước G2 (Kinh thánh §8, cổng hình G2: chấm mù ≥ 7,0/10 và KHÔNG THUA T1 ở cặp nào).
CÙNG GIAO THỨC channel-k2/k2v2-mau/blind_v2.py và vòng 5 (k2v4-mau/blind_v4.py): `claude -p` GHIM claude-sonnet-5-5, chỉ công cụ Read,
thư mục tạm trống chỉ chứa X.jpg/Y.jpg, 3 vai (PROMPT/RATERS nạp nguyên văn từ blind_v2.py), thang tuyệt đối (5 = video faceless thường).
KHUNG T1 = đúng khung T1 đã dùng ở vòng 5 (ảnh đã commit k2v4-mau/kiem-mu/blind/P*/X|Y.jpg, phía T1 theo key.json, trích từ master
release-k2c-t1-06-v1 SHA 4f2d280b…) → cùng tham chiếu với các vòng trước. Khung T2 = master 1080p của tập (giây khai TRƯỚC khi dựng 1080p,
ghi ở g2/rague-cap.json và commit trước lượt dựng). Thứ tự X/Y: hạt giống cố định 20261015. Không sửa sau khi chấm.
Sổ chi phí kiem-mu/cost.jsonl (tag "ragu:…"), trần tập $11, dừng $10.
  blind_g2.py set <master_t2.mp4>   · blind_g2.py run [P1 …]   · blind_g2.py score"""
import importlib.util, json, os, random, re, shutil, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'kiem-mu'); B = os.path.join(OUT, 'ragu'); LOG = os.path.join(OUT, 'cost.jsonl')
spec = importlib.util.spec_from_file_location('bv2', os.path.join(HERE, '..', 'k2v2-mau', 'blind_v2.py')); BV2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(BV2)
PROMPT, RATERS, MODEL, grab = BV2.PROMPT, BV2.RATERS, BV2.MODEL, BV2.grab
assert MODEL == 'claude-sonnet-5-5'
CAP, STOP = 11.0, 10.0
V5 = os.path.join(HERE, '..', 'k2v4-mau', 'kiem-mu', 'blind')
CAPS = os.path.join(HERE, 'g2', 'rague-cap.json')   # {"P1": giây T2, …} — khai trước lượt dựng 1080p


def spent():
    return sum(json.loads(l)['usd'] for l in open(LOG)) if os.path.exists(LOG) else 0.0


def setup(master):
    os.makedirs(B, exist_ok=True); K5 = json.load(open(os.path.join(V5, 'key.json'))); T2 = json.load(open(CAPS)); R = random.Random(20261015); key = {}
    for pid in sorted(T2):
        t1_is_x = R.random() < 0.5; d = os.path.join(B, pid); os.makedirs(d, exist_ok=True)
        shutil.copy(os.path.join(V5, pid, K5[pid]['t1'] + '.jpg'), os.path.join(d, 'X.jpg' if t1_is_x else 'Y.jpg'))
        grab(master, T2[pid], os.path.join(d, 'Y.jpg' if t1_is_x else 'X.jpg'))
        key[pid] = dict(kind=K5[pid]['kind'], t1='X' if t1_is_x else 'Y', t2='Y' if t1_is_x else 'X', t1_s=K5[pid]['t1_s'], t2_s=T2[pid])
    json.dump(key, open(os.path.join(B, 'key.json'), 'w'), indent=1); print(json.dumps(key, indent=1))


def call(pid, rk):
    if spent() > STOP: raise SystemExit(f'dừng: đã tiêu ${spent():.2f}')
    key = json.load(open(os.path.join(B, 'key.json'))); prompt = PROMPT.format(persona=RATERS[rk], kind=key[pid]['kind'])
    env = dict(os.environ, ANTHROPIC_API_KEY=os.environ['CONSOLE_API_KEY'])
    with tempfile.TemporaryDirectory() as cwd:
        for f in ('X.jpg', 'Y.jpg'): shutil.copy(os.path.join(B, pid, f), cwd)
        for _ in range(2):
            r = subprocess.run(['claude', '-p', '--model', MODEL, '--output-format', 'json', '--allowedTools', 'Read'], input=prompt, capture_output=True, text=True, env=env, cwd=cwd, timeout=900)
            try: d = json.loads(r.stdout)
            except Exception: continue
            with open(LOG, 'a') as f: f.write(json.dumps({'tag': f'ragu:{pid}-{rk}', 'model': MODEL, 'served': sorted(d.get('modelUsage', {})), 'usd_by_model': {m: round(u.get('costUSD', 0), 5) for m, u in d.get('modelUsage', {}).items()}, 'usd': d.get('total_cost_usd', 0)}) + '\n')
            open(os.path.join(B, pid, f'{rk}.raw.txt'), 'w').write(d.get('result', ''))
            m = re.search(r'\{.*\}', d.get('result', ''), re.S)
            if m:
                try: j = json.loads(m.group(0)); json.dump(j, open(os.path.join(B, pid, f'{rk}.json'), 'w'), indent=1); return True
                except Exception: pass
    return False


def run(only=None):
    key = json.load(open(os.path.join(B, 'key.json')))
    jobs = [(p, rk) for p in key for rk in RATERS if (not only or p in only) and not os.path.exists(os.path.join(B, p, f'{rk}.json'))]
    with ThreadPoolExecutor(3) as ex: res = list(ex.map(lambda a: call(*a), jobs))
    print(dict(zip([f'{a}-{b}' for a, b in jobs], res)), f'chi phí tập ${spent():.2f} / trần ${CAP}')


def score():
    key = json.load(open(os.path.join(B, 'key.json'))); rows = []; t2all = []
    for pid, k in key.items():
        J = [json.load(open(os.path.join(B, pid, f'{rk}.json'))) for rk in RATERS if os.path.exists(os.path.join(B, pid, f'{rk}.json'))]
        c1 = [j[k['t1']]['craft'] for j in J]; c2 = [j[k['t2']]['craft'] for j in J]; t2all += c2
        pick = sum(1 for j in J if j.get('better') == k['t2']); flags = sorted({f for j in J for f in j[k['t2']].get('flags', [])})
        rows.append(dict(cap=pid, kind=k['kind'], t1=round(sum(c1) / len(c1), 2), t2=round(sum(c2) / len(c2), 2), t2_tung_nguoi=c2, chon_t2=f'{pick}/{len(J)}', co_t2=flags,
                         doc_t2=round(sum(j[k['t2']]['readability'] for j in J) / len(J), 2), ro_t2=round(sum(j[k['t2']]['clarity'] for j in J) / len(J), 2), thua=sum(c2) < sum(c1)))
    tb = round(sum(t2all) / len(t2all), 2); ok = tb >= 7.0 and not any(r['thua'] for r in rows)
    R = dict(cap=rows, tb_t2=tb, tb_t1=round(sum(r['t1'] for r in rows) / len(rows), 2), thua_cap=[r['cap'] for r in rows if r['thua']], ket_qua='ĐẠT' if ok else 'TRƯỢT', chi_phi_tap=round(spent(), 2))
    json.dump(R, open(os.path.join(OUT, 'ragu-score.json'), 'w'), indent=1, ensure_ascii=False); print(json.dumps(R, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    a = sys.argv[1]
    if a == 'set': setup(sys.argv[2])
    elif a == 'run': run(sys.argv[2:] or None)
    elif a == 'score': score()
