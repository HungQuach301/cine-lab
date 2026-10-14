#!/opt/cine/bin/python
"""KÊNH 2 · chấm MÙ vòng 5 (phiên V4, 14/10/2026) — CÙNG GIAO THỨC channel-k2/k2v2-mau/blind_v2.py:
`claude -p` GHIM model claude-sonnet-5-5, chỉ công cụ Read, thư mục tạm trống, 3 vai chấm, cùng đề bài (PROMPT/RATERS nạp nguyên từ blind_v2.py),
thang tuyệt đối (5 = video faceless thường); khung T1 trích từ master release-k2c-t1-06-v1 (SHA 4f2d280b…).
Cặp và mốc giây KHAI TRƯỚC khi dựng 1080p (commit trước lượt dựng). Không sửa sau khi chấm.
  5 cặp cũ: cùng khung T1, cùng thứ tự X/Y như vòng 1–4 (key.json của k2v2-mau); khung mới = khung tương ứng của cuộn K2V4.
  2 cặp mới: P6 footage mới ↔ khung footage T1 (f_chicago_aerial 2:56.4 + 2,6 s); P7 tầng gần của zoom ↔ ảnh lưu trữ T1 (loc_det_buffalo 2:49.5 + 1,5 s);
             thứ tự X/Y bằng hạt giống cố định 20261014 như blind_v2.py.
Trần API phiên V4 $5 (lệnh chủ dự án), dừng ở $4,5 tính trên sổ riêng kiem-mu/cost.jsonl của k2v4-mau.
  blind_v4.py set <master_t1.mp4> · blind_v4.py run · blind_v4.py score"""
import importlib.util, json, os, random, shutil, subprocess, sys, tempfile, re
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'kiem-mu'); B = os.path.join(OUT, 'blind'); LOG = os.path.join(OUT, 'cost.jsonl')
spec = importlib.util.spec_from_file_location('bv2', os.path.join(HERE, '..', 'k2v2-mau', 'blind_v2.py')); BV2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(BV2)
PROMPT, RATERS, MODEL, grab = BV2.PROMPT, BV2.RATERS, BV2.MODEL, BV2.grab
assert MODEL == 'claude-sonnet-5-5'
CAP, STOP = 5.0, 4.5
NEW = '/var/tmp/cine-out/k2v-shots/K2V4-reel/shot.mp4'
OLDKEY = os.path.join(HERE, '..', 'k2v2-mau', 'kiem-mu', 'blind', 'key.json')
# Cuộn K2V4 (64 s): Z 0–10 · H 10–25 · J 25–35 · N 35–42 · F 42–50 · P 50–58 · S 58–64
# (cặp, loại nội dung — nguyên văn vòng 1–4 cho P1–P5, khung T1 (F## bộ Q27 hoặc giây), giây khung mới)
PAIRS = [('P1', 'a terrain map that sets up the story (where it happens)', 'F08', 23.0),     # = H 13,0 s như vòng 1–4
         ('P2', 'a map showing a route or movement across a region', 'F12', 31.0),      # = J 6,0 s như vòng 1–4
         ('P3', 'numbers shown as 3D objects in a scene', 'F03', 39.6),                 # N: hàng 10 xu + 1 xu, đủ hai nhãn số (G2)
         ('P4', 'a historical portrait or archival image with a caption', 'F01', 53.0), # P: chân dung tách nền DeWitt Clinton, Ken Burns 2.5D (F2)
         ('P5', 'a summary / comparison screen', 'F09', 62.5),                          # S: bảng điểm chữ ≥ 34 px (G3) — = 4,5 s trong đoạn như vòng 1–4
         ('P6', 'real video footage used in a documentary explainer', 179.0, 44.0),     # F: footage tư liệu (F3)
         ('P7', 'an archival photograph shown full screen', 171.0, 8.6)]                # Z: tầng gần của zoom nhiều tầng (F4)


def spent():
    return sum(json.loads(l)['usd'] for l in open(LOG)) if os.path.exists(LOG) else 0.0


def setup(master):
    os.makedirs(B, exist_ok=True); old = json.load(open(OLDKEY)); K1 = json.load(open(os.path.join(HERE, '..', 'k2c-t1-06', 'kiem-mu', 'blind-g2', 'q27', 'key.json')))
    R = random.Random(20261014); key = {}
    for pid, kind, f, tn in PAIRS:
        old_is_x = (old[pid]['t1'] == 'X') if pid in old else R.random() < 0.5
        t1s = K1[f] if isinstance(f, str) else f; d = os.path.join(B, pid); os.makedirs(d, exist_ok=True)
        grab(master, t1s, os.path.join(d, 'X.jpg' if old_is_x else 'Y.jpg')); grab(NEW, tn, os.path.join(d, 'Y.jpg' if old_is_x else 'X.jpg'))
        key[pid] = dict(kind=kind, t1='X' if old_is_x else 'Y', moi='Y' if old_is_x else 'X', t1_frame=f if isinstance(f, str) else f't1@{f}', t1_s=t1s, moi_s=tn)
    json.dump(key, open(os.path.join(B, 'key.json'), 'w'), indent=1); print(json.dumps(key, indent=1))


def call(pid, rk):
    if spent() > STOP: raise SystemExit(f'dừng: đã tiêu ${spent():.2f} (dừng ở ${STOP}, trần ${CAP})')
    key = json.load(open(os.path.join(B, 'key.json'))); prompt = PROMPT.format(persona=RATERS[rk], kind=key[pid]['kind'])
    env = dict(os.environ, ANTHROPIC_API_KEY=os.environ['CONSOLE_API_KEY'])
    with tempfile.TemporaryDirectory() as cwd:
        for f in ('X.jpg', 'Y.jpg'): shutil.copy(os.path.join(B, pid, f), cwd)
        for _ in range(2):
            r = subprocess.run(['claude', '-p', '--model', MODEL, '--output-format', 'json', '--allowedTools', 'Read'], input=prompt, capture_output=True, text=True, env=env, cwd=cwd, timeout=900)
            try: d = json.loads(r.stdout)
            except Exception: continue
            with open(LOG, 'a') as f: f.write(json.dumps({'tag': f'{pid}-v5-{rk}', 'model': MODEL, 'served': sorted(d.get('modelUsage', {})), 'usd': d.get('total_cost_usd', 0)}) + '\n')
            open(os.path.join(B, pid, f'{rk}.raw.txt'), 'w').write(d.get('result', ''))
            m = re.search(r'\{.*\}', d.get('result', ''), re.S)
            if m:
                try: j = json.loads(m.group(0)); json.dump(j, open(os.path.join(B, pid, f'{rk}.json'), 'w'), indent=1); return True
                except Exception: pass
    return False


def run(only=None):
    jobs = [(p[0], rk) for p in PAIRS for rk in RATERS if (not only or p[0] in only) and not os.path.exists(os.path.join(B, p[0], f'{rk}.json'))]
    with ThreadPoolExecutor(3) as ex: res = list(ex.map(lambda a: call(*a), jobs))
    print(dict(zip([f'{a}-{b}' for a, b in jobs], res)), f'chi phí V4 ${spent():.2f} / trần ${CAP}')


if __name__ == '__main__':
    a = sys.argv[1]
    if a == 'set': setup(sys.argv[2])
    elif a == 'run': run(sys.argv[2:] or None)
    else: BV2.B, BV2.OUT, BV2.LOG = B, OUT, LOG; BV2.CAP = CAP; BV2.score()
