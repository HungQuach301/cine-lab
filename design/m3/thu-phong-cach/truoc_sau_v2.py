"""Cine Lab · M3 B3 v2 — ảnh 1080 trước (B3, Mốc 1) / sau (B3 v2) cho s03, s05, s22 và khung dữ liệu: mỗi cặp một ảnh 3840×1080 (trái B3, phải B3v2).
/opt/cine/bin/python design/m3/thu-phong-cach/truoc_sau_v2.py <reports/m3/thu-phong-cach/B3v2>
"""
import os, sys
from PIL import Image, ImageDraw, ImageFont
R = sys.argv[1]; B = os.path.join(os.path.dirname(R.rstrip('/')), 'B3')
f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 34)
pairs = [(f'{B}/khung1080-{s}-b3.png', f'{R}/khung1080-{s}-b3v2.png', s) for s in ('s03', 's05', 's22')] + [(f'{B}/khung-du-lieu.png', f'{R}/khung-du-lieu-b3v2.png', 'du-lieu')]
for a, b, n in pairs:
    im = Image.new('RGB', (3840, 1080)); d = ImageDraw.Draw(im)
    for i, (p, lab) in enumerate([(a, 'B3 (Mốc 1)'), (b, 'B3 v2')]):
        im.paste(Image.open(p).convert('RGB').resize((1920, 1080)), (i * 1920, 0)); d.rectangle([i * 1920, 0, i * 1920 + 300, 50], fill=(0, 0, 0)); d.text((i * 1920 + 12, 6), lab, fill=(255, 255, 255), font=f)
    out = f'{R}/truoc-sau-1080-{n}.jpg'; im.save(out, quality=88); print(out)
