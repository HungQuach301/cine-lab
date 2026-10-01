"""Cine Lab · M3 THỬ PHONG CÁCH — ảnh trước (layout v22, cờ tắt) / sau (biến thể) cùng khung, 3 hàng s03 · s05 · s22.
/opt/cine/bin/python design/m3/thu-phong-cach/truoc_sau.py <thư mục v22> <thư mục biến thể> <nhãn biến thể> <ra.jpg>
"""
import sys
from PIL import Image, ImageDraw, ImageFont

a, b, lab, out = sys.argv[1:5]
F = [('s03', 222), ('s05', 324), ('s22', 1224)]
W, H, pad = 640, 360, 6
f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 18)
sheet = Image.new('RGB', (2 * W + 3 * pad, 3 * H + 4 * pad), (24, 24, 24)); d = ImageDraw.Draw(sheet)
for r, (s, fr) in enumerate(F):
    for c, (dd, t) in enumerate([(a, 'v22'), (b, lab)]):
        im = Image.open(f'{dd}/{s}_f{fr}.png').convert('RGB').resize((W, H), Image.LANCZOS)
        x, y = pad + c * (W + pad), pad + r * (H + pad); sheet.paste(im, (x, y))
        d.rectangle([x, y, x + 190, y + 26], fill=(0, 0, 0)); d.text((x + 6, y + 3), f'{s} khung {fr} · {t}', fill=(255, 255, 255), font=f)
sheet.save(out, quality=88); print(out)
