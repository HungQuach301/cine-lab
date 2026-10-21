#!/opt/cine/bin/python
"""ANIMATIC-T3 · GHÉP CÚ LẶN GIỮ CHỖ vào khung cảnh đinh N2.9 (sau bước dựng cảnh đinh, TRƯỚC bước render đoạn):
khung f ≥ t*24 của N2.9 thay bằng clip reports/nc-gpu/lan/ncg-lan-xem.mp4 (từ giây ss, 960×540 24 fps, Cycles GPU của NC-GPU — 0 AI),
khung cảnh đinh không có chữ; bộ đếm vẽ ở bước render đoạn theo đường thời gian N2.9 (sau t: nối đúng giờ của clip) → chạy liền.
Ghi "giữ chỗ — bản cuối dựng Cycles GPU (G0)" vào log. Chạy lại được (giữ bản gốc ở <dir>/goc-lan/).
  anim_lan.py <timeline.json của build> <log ra.json>"""
import json, shutil, subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image
REPO = Path(__file__).resolve().parents[2]
TL = json.loads(Path(sys.argv[1]).read_text()); LOGP = Path(sys.argv[2])
LOG = json.loads((REPO / 'channel-k2/k2c-t3-01/animatic/log-shot.json').read_text()); sh = [x for x in LOG if x.get('lan')][0]; L = sh['lan']
H = TL['heroes']['anim_N2_9']; d = Path(H['dir']); W, Hh = H['size']
fr = sorted(p for p in d.iterdir() if p.suffix in ('.jpg', '.png') and p.stem.isdigit()); f0 = int(round(L['t'] * 24)); n = len(fr) - f0
bk = d / 'goc-lan'; bk.mkdir(exist_ok=True)
for p in fr[f0:]:
    if not (bk / p.name).exists(): shutil.copy2(p, bk / p.name)
# khung cảnh đinh KHÔNG có chữ (bộ đếm do render đoạn — scripts/k2/render.js + lib/k2.js — vẽ sau theo đường thời gian của cảnh) → thay nguyên khung
box = None
clip = Path('/var/tmp/cine-out/k2c-t3-anim/lan-clip'); shutil.rmtree(clip, ignore_errors=True); clip.mkdir(parents=True)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(L['ss']), '-i', str(REPO / L['clip']), '-frames:v', str(n), '-vf', f'scale={W}:{Hh}:flags=lanczos,fps=24', '-q:v', '2', str(clip / '%05d.jpg')], check=True)
cf = sorted(clip.glob('*.jpg'))
for i, p in enumerate(fr[f0:]):
    c = Image.open(cf[min(i, len(cf) - 1)]).convert('RGB')
    c.save(p, quality=95) if p.suffix == '.jpg' else c.save(p)
LOGP.write_text(json.dumps(dict(shot='N2.9', khung=[f0, f0 + n - 1], clip=L['clip'], tu_giay=L['ss'], hop_bo_dem=box, ghi='giữ chỗ — bản cuối dựng Cycles GPU (G0)'), ensure_ascii=False, indent=1))
print('LAN-XONG', f0, n, box)
