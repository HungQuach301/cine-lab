#!/opt/cine/bin/python
"""ANIMATIC-T3-V2 · THỬ MÁY ỨNG VIÊN (R1/R2) trên cùng trạng thái khung của một shot: mặt nạ ID (do_bocuc.js) → % 'bang' (cỏ/cát trống), % chủ thể, nhìn xuống, AGL
+ khung màu 480×270 (tắt cách A) → tờ soi có nhãn. Chọn máy theo số đo + mắt.
  v2_thu_may.py <thư mục opt> <mã shot> '<json [{id, p, l, fov}]>' <thư mục ra> --only 0,120 [--sua '<json ghi đè opt>']"""
import json, os, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw
REPO = Path(__file__).resolve().parents[2]
CT = ['nguoi', 'trai', 'congsu', 'nha', 'pho', 'lua', 'tau', 'pin', 'co', 'khac']
a = sys.argv; od, sid, cams, out = Path(a[1]), a[2], json.loads(a[3]), Path(a[4]); out.mkdir(parents=True, exist_ok=True)
only = a[a.index('--only') + 1]; o = json.loads((od / f"anim_{sid.replace('.', '_')}.json").read_text()); o.pop('nc', None)
if '--sua' in a: o.update(json.loads(a[a.index('--sua') + 1]))
r = subprocess.run(['node', str(REPO / 'design/k2v/v7c/do_bocuc.js'), '--opt', json.dumps(o), '--only', only, '--cams', json.dumps(cams), '--out', str(out / 'do.json'),
                    '--jpg', str(out / 'jpg'), '--w', '480', '--h', '270', '--scale', '1'], capture_output=True, text=True, env=dict(os.environ, K2TL_CACHE=os.environ.get('K2TL_CACHE', '/var/tmp/cine-out/k2tl-cache')))
if r.returncode: sys.exit(r.stderr[-1500:])
D = json.loads((out / 'do.json').read_text())['frames']; fr = [int(x) for x in only.split(',')]
W, H = 480, 270; sheet = Image.new('RGB', (W * len(fr), (H + 30) * len(cams)), (20, 20, 20)); g = ImageDraw.Draw(sheet)
for i, c in enumerate(cams):
    for j, f in enumerate(fr):
        row = [x for x in D if x.get('ung_vien') == c['id'] and x['f'] == f][0]; p = out / 'jpg' / f"{c['id']}-{f:05d}.jpg"
        if p.exists(): sheet.paste(Image.open(p).convert('RGB'), (j * W, i * (H + 30) + 30))
        ct = sum(row['pct'].get(k, 0) for k in CT)
        s = f"{c['id']} f{f} bang {row['pct'].get('bang', 0):.0f}% chu_the {ct:.1f}% troi {row['pct'].get('troi', 0):.0f}% xuong {row['xuong']} agl {row['agl']:.0f}"
        g.text((j * W + 4, i * (H + 30) + 4), s, fill=(255, 230, 120)); print(s)
sheet.save(out / 'to.jpg', quality=85); print('TO', out / 'to.jpg')
