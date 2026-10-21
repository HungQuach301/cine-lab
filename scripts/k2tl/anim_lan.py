#!/opt/cine/bin/python
"""ANIMATIC-T3 · GHÉP CÚ LẶN GIỮ CHỖ vào khung cảnh đinh N2.9 (sau bước dựng cảnh đinh, TRƯỚC bước render đoạn):
khung f ≥ t*24 của N2.9 thay bằng clip reports/nc-gpu/lan/ncg-lan-xem.mp4 (từ giây ss, 960×540 24 fps, Cycles GPU của NC-GPU — 0 AI),
GIỮ hộp bộ đếm của khung cách A (mặt nạ = chỗ khung có chữ khác khung không chữ ở cùng khung, nở 6 px) → bộ đếm chạy liền theo đường thời gian của clip.
Ghi "giữ chỗ — bản cuối dựng Cycles GPU (G0)" vào log. Chạy lại được (giữ bản gốc ở <dir>/goc-lan/).
  anim_lan.py <timeline.json của build> <log ra.json>"""
import json, shutil, subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter
REPO = Path(__file__).resolve().parents[2]
TL = json.loads(Path(sys.argv[1]).read_text()); LOGP = Path(sys.argv[2])
LOG = json.loads((REPO / 'channel-k2/k2c-t3-01/animatic/log-shot.json').read_text()); sh = [x for x in LOG if x.get('lan')][0]; L = sh['lan']
H = TL['heroes']['anim_N2_9']; d = Path(H['dir']); W, Hh = H['size']
fr = sorted(p for p in d.iterdir() if p.suffix in ('.jpg', '.png') and p.stem.isdigit()); f0 = int(round(L['t'] * 24)); n = len(fr) - f0
bk = d / 'goc-lan'; bk.mkdir(exist_ok=True)
for p in fr[f0:]:
    if not (bk / p.name).exists(): shutil.copy2(p, bk / p.name)
# mặt nạ hộp bộ đếm: dựng khung f0 không chữ, so với khung có chữ
o = dict(H['opt']); tmp = Path('/var/tmp/cine-out/k2c-t3-anim/lan-mask'); tmp.mkdir(parents=True, exist_ok=True)
subprocess.run(['node', str(REPO / 'scripts/k2tl/render.js'), '--scene', 't3tl', '--pack', 'gib', '--opt', json.dumps(o), '--only', str(f0), '--override', '[{"noText":true}]', '--tech', '{"spp":4}',
                '--w', str(W), '--h', str(Hh), '--out', str(tmp)], check=True, capture_output=True)
a = np.asarray(Image.open(bk / fr[f0].name).convert('RGB'), np.int16); b = np.asarray(Image.open(sorted(tmp.glob('*.jpg'))[0]).convert('RGB'), np.int16)
m = (np.abs(a - b).max(-1) > 24); m[:int(Hh * 0.55)] = False   # chỉ nửa dưới (hộp năm dưới-trái)
ys, xs = np.nonzero(m); box = [int(xs.min()) - 8, int(ys.min()) - 8, int(xs.max()) + 8, int(ys.max()) + 8] if len(xs) else None
mask = Image.new('L', (W, Hh), 0)
if box: mask.paste(255, box)
mask = mask.filter(ImageFilter.GaussianBlur(1.5))
clip = Path('/var/tmp/cine-out/k2c-t3-anim/lan-clip'); shutil.rmtree(clip, ignore_errors=True); clip.mkdir(parents=True)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(L['ss']), '-i', str(REPO / L['clip']), '-frames:v', str(n), '-vf', f'scale={W}:{Hh}:flags=lanczos,fps=24', '-q:v', '2', str(clip / '%05d.jpg')], check=True)
cf = sorted(clip.glob('*.jpg'))
for i, p in enumerate(fr[f0:]):
    c = Image.open(cf[min(i, len(cf) - 1)]).convert('RGB'); h = Image.open(bk / p.name).convert('RGB'); c.paste(h, (0, 0), mask)
    c.save(p, quality=95) if p.suffix == '.jpg' else c.save(p)
LOGP.write_text(json.dumps(dict(shot='N2.9', khung=[f0, f0 + n - 1], clip=L['clip'], tu_giay=L['ss'], hop_bo_dem=box, ghi='giữ chỗ — bản cuối dựng Cycles GPU (G0)'), ensure_ascii=False, indent=1))
print('LAN-XONG', f0, n, box)
