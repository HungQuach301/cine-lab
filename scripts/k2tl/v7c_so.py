#!/opt/cine/bin/python
"""V7C · TỜ SO V7B ↔ V7C 8 cặp cùng câu lời (bản xem V7B có phụ đề trong git ↔ bản 540p có phụ đề kiểm của V7C). Cùng nhịp lời G1 → cùng giây phim.
  v7c_so.py [<bản V7C có phụ đề>]   → reports/v7c/so/to-so-8-cap.jpg"""
import subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
ROOT = Path(__file__).resolve().parents[2]; V7B = ROOT / 'reports/v7b/ban-thu/v7b-a-xem-phude.mp4'
V7C = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('/var/tmp/cine-out/k2c-t3-v7c/k2c-t3-v7c-540p-phude.mp4')
PAIRS = [('0a', 'Midnight at the Gibraltar frontier…', 3.0), ('0d', 'Historians on both sides count fourteen sieges…', 18.6), ('0f', 'In 1782, ten floating batteries came to break it.', 29.6),
         ('0g', 'In 1941, a runway was laid across the only road…', 36.0), ('2a', 'Half a century later… can you starve a rock?', 47.0), ('2d', 'By January 1780, thistles, dandelions…', 80.0),
         ('SM2', 'Britain sent three relief fleets: 1780, 1781, 1782.', 96.5), ('2g', 'On the twelfth of April 1781… opened fire on the town.', 109.0)]
try: F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 15)
except Exception: F = ImageFont.load_default()
def grab(src, t, out): subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{t:.3f}', '-i', str(src), '-frames:v', '1', str(out)], check=True); return Image.open(out).convert('RGB')
tmp = Path('/var/tmp/cine-out/v7c/so'); tmp.mkdir(parents=True, exist_ok=True); w, h = 640, 360
S = Image.new('RGB', (2 * w + 30, len(PAIRS) * (h + 30) + 40), 'white'); D = ImageDraw.Draw(S)
D.text((10, 10), 'TRÁI: V7B (bản xem 360p, phụ đề kiểm) · PHẢI: V7C (540p → 360p, phụ đề kiểm) — cùng câu lời, cùng giây (nhịp G1 v4.2)', fill='black', font=F)
for i, (k, cau, t) in enumerate(PAIRS):
    a = grab(V7B, t, tmp / f'v7b-{k}.png').resize((w, h), Image.LANCZOS); b = grab(V7C, t, tmp / f'v7c-{k}.png').resize((w, h), Image.LANCZOS)
    y = 40 + i * (h + 30); D.text((10, y), f'{k} · "{cau}" · {t:.1f} s', fill='black', font=F); S.paste(a, (10, y + 22)); S.paste(b, (20 + w, y + 22))
(ROOT / 'reports/v7c/so').mkdir(parents=True, exist_ok=True); S.save(ROOT / 'reports/v7c/so/to-so-8-cap.jpg', quality=85); print(ROOT / 'reports/v7c/so/to-so-8-cap.jpg')
