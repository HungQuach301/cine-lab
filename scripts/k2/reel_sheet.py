#!/opt/cine/bin/python
"""Tờ khung cuộn mẫu: mỗi đoạn một hàng, khung ở 15 % / 50 % / 85 % thời lượng đoạn (+ mốc khai thêm), chú thích đoạn + giây.
  reel_sheet.py <shot.mp4> <timeline.json> <out.jpg> [--w 640]"""
import json, subprocess, sys, tempfile, os
from PIL import Image, ImageDraw, ImageFont
mp4, tl, out = sys.argv[1:4]; W = int(sys.argv[sys.argv.index('--w') + 1]) if '--w' in sys.argv else 640
T = json.load(open(tl)); F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 20)
rows = []
with tempfile.TemporaryDirectory() as d:
    for sg in T['segments']:
        ims = []
        for k in (0.15, 0.5, 0.85):
            t = sg['t0'] + k * (sg['t1'] - sg['t0']); f = os.path.join(d, f'{sg["id"]}{k}.jpg')
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{t:.3f}', '-i', mp4, '-frames:v', '1', '-vf', f'scale={W}:-2', '-q:v', '3', f], check=True)
            im = Image.open(f).convert('RGB'); ImageDraw.Draw(im).text((10, 8), f'{sg["id"]} · {t:.1f}s', fill=(255, 255, 255), font=F, stroke_width=2, stroke_fill=(0, 0, 0)); ims.append(im)
        rows.append(ims)
H = rows[0][0].height; sheet = Image.new('RGB', (W * 3, H * len(rows)))
for r, ims in enumerate(rows):
    for c, im in enumerate(ims): sheet.paste(im, (c * W, r * H))
sheet.save(out, quality=82); print(out, sheet.size)
