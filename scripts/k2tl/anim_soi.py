#!/opt/cine/bin/python
"""ANIMATIC-T3 · SOI BỐ CỤC trước khi dựng: mỗi shot dựng vài khung (mặc định đầu · giữa · cuối) ở cỡ nhỏ, có thể tắt cách A (nhanh, cùng máy/bố cục),
rồi ghép tờ soi có mã shot + giây. Dùng để soát LOOK-2/LOOK-4 (Rock trong khung, trời 8–20 %, không nhìn thẳng xuống) trước khi dựng cả tập.
  anim_soi.py <thư mục opt (mk_ep_anim.py --opt-dir)> <thư mục ra> [--shots H1,N1.1] [--w 480] [--nc 0|1] [--t 0,0.5,1] [--spp 1]"""
import json, os, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw
REPO = Path(__file__).resolve().parents[2]
OD, OUT = Path(sys.argv[1]), Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True)
arg = lambda k, d: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
W = int(arg('--w', '480')); H = W * 9 // 16; NC = arg('--nc', '0') == '1'; TS = [float(x) for x in arg('--t', '0,0.5,1').split(',')]; SPP = int(arg('--spp', '1'))
only = arg('--shots', ''); only = set(only.split(',')) if only else None
rows = []
for f in sorted(OD.glob('anim_*.json'), key=lambda p: json.loads(p.read_text())['shot']):
    o = json.loads(f.read_text()); sid = o['shot']
    if only and sid not in only: continue
    if not NC: o.pop('nc', None)
    N = int(round(o['dur'] * 24)); fr = sorted(set(min(N - 1, max(0, int(round(t * (N - 1))))) for t in TS)); d = OUT / sid; d.mkdir(exist_ok=True)
    r = subprocess.run(['node', str(REPO / 'scripts/k2tl/render.js'), '--scene', 't3tl', '--pack', 'gib', '--opt', json.dumps(o), '--only', ','.join(map(str, fr)), '--override', '[{"noText":true}]',
                        '--tech', json.dumps({'spp': SPP}), '--w', str(W), '--h', str(H), '--out', str(d)], capture_output=True, text=True)
    ok = [d / f'{x:05d}.jpg' for x in fr]
    if r.returncode or not all(p.exists() for p in ok): print('LỖI', sid, (r.stderr or r.stdout)[-400:], flush=True); continue
    rows.append((sid, o['dur'], fr, ok)); print('xong', sid, fr, flush=True)
if rows:
    n = max(len(r[3]) for r in rows); per = 8
    for b in range(0, len(rows), per):
        R = rows[b:b + per]; sheet = Image.new('RGB', (W * n, (H + 18) * len(R)), (20, 20, 20)); g = ImageDraw.Draw(sheet)
        for i, (sid, dur, fr, ps) in enumerate(R):
            for j, p in enumerate(ps): sheet.paste(Image.open(p).convert('RGB'), (j * W, i * (H + 18) + 18)); g.text((j * W + 4, i * (H + 18) + 3), f'{sid}  t={fr[j] / 24:.1f}s / {dur:.1f}s', fill=(255, 230, 120))
        sheet.save(OUT / f'to-soi-{b // per + 1:02d}.jpg', quality=82)
    print('TO-SOI-XONG', len(rows))
