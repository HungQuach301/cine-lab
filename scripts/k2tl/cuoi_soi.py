#!/opt/cine/bin/python
"""BAN-CUOI-T3 · SOI SHOT (bố cục + R2 mắt): mỗi shot dựng khung màu + mặt nạ ID mỗi `every` khung (tắt cách A, 480×270) bằng design/k2v/v7c/do_bocuc.js,
rồi tờ soi có nhãn % TRỐNG = 'bang' + 'suon' (cùng định nghĩa trong_pct khai cho K — 23/10: bản cũ chỉ 'bang' nên bỏ sót C1), % chủ thể; đánh dấu khung trống > 40 % (ngưỡng mắt 1b). Ghi <ra>/<shot>/do.json + <ra>/<shot>/to.jpg.
  cuoi_soi.py <thư mục opt> <ra> N3_1,N3_3 [--every 48] [--P 2] [--cot 6]"""
import json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from PIL import Image, ImageDraw
REPO = Path(__file__).resolve().parents[2]; CT = ['nguoi', 'trai', 'congsu', 'nha', 'pho', 'lua', 'tau', 'pin', 'co', 'khac']
a = sys.argv; od, out, shots = Path(a[1]), Path(a[2]), a[3].split(',')
ev = int(a[a.index('--every') + 1]) if '--every' in a else 48; P = int(a[a.index('--P') + 1]) if '--P' in a else 2; COT = int(a[a.index('--cot') + 1]) if '--cot' in a else 6
def one(sid):
    o = json.loads((od / f'anim_{sid}.json').read_text()); o.pop('nc', None); d = out / sid; d.mkdir(parents=True, exist_ok=True)
    r = subprocess.run(['node', str(REPO / 'design/k2v/v7c/do_bocuc.js'), '--opt', json.dumps(o), '--every', str(ev), '--out', str(d / 'do.json'), '--jpg', str(d / 'jpg'), '--w', '480', '--h', '270', '--scale', '1'],
                       capture_output=True, text=True, env=dict(os.environ, K2TL_CACHE=os.environ.get('K2TL_CACHE', '/var/tmp/cine-out/k2tl-cache')))
    if r.returncode: return sid, 'LỖI ' + r.stderr[-800:]
    D = json.loads((d / 'do.json').read_text())['frames']; W, H = 480, 270; n = len(D); rows = (n + COT - 1) // COT
    sh = Image.new('RGB', (W * COT, (H + 18) * rows), (20, 20, 20)); g = ImageDraw.Draw(sh)
    for i, x in enumerate(D):
        p = d / 'jpg' / f"{x['f']:05d}.jpg"; X, Y = (i % COT) * W, (i // COT) * (H + 18)
        if p.exists(): sh.paste(Image.open(p).convert('RGB'), (X, Y + 18))
        b = x['pct'].get('bang', 0) + x['pct'].get('suon', 0); ct = sum(x['pct'].get(k, 0) for k in CT)
        g.text((X + 4, Y + 3), f"{sid} t{x['f'] / 24:5.1f} trong {b:.0f}% ct {ct:.1f}% troi {x['pct'].get('troi', 0):.0f}%", fill=(255, 80, 80) if b > 40 else (255, 230, 120))
    sh.save(d / 'to.jpg', quality=82)
    return sid, ' '.join(f"{x['f'] / 24:.0f}:{x['pct'].get('bang', 0) + x['pct'].get('suon', 0):.0f}" for x in D)
with ThreadPoolExecutor(P) as ex:
    for sid, s in ex.map(one, shots): print(sid, s, flush=True)
