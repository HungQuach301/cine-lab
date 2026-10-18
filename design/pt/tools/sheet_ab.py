"""Tờ khung A|B cạnh nhau (cùng máy, cùng ánh sáng, cùng lớp sống): python -I sheet_ab.py <thư mục khung> <ra.jpg> [tên khung…]"""
import sys, os
from PIL import Image, ImageDraw, ImageFont
d, out = sys.argv[1], sys.argv[2]; names = sys.argv[3:] or ['1782-trua', '1782-chieu', '1782-dem', '1943-trua', '1943-chieu', '1943-dem']
F = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-SemiBold.otf', 26); w, h = 960, 540
sh = Image.new('RGB', (2 * w + 30, len(names) * (h + 44) + 50), (22, 22, 24)); dr = ImageDraw.Draw(sh)
dr.text((10, 10), 'A = không điểm ảnh AI (vân CC0 Poly Haven)        B = vân vật liệu AI (gpt-image-2.5-flare), mọi thứ khác y hệt A', font=F, fill=(240, 236, 220))
for i, n in enumerate(names):
    for j, t in enumerate('AB'):
        p = os.path.join(d, f'{n}-{t}-notext.jpg')
        if not os.path.exists(p): continue
        sh.paste(Image.open(p).convert('RGB').resize((w, h), Image.LANCZOS), (10 + j * (w + 10), 50 + i * (h + 44) + 34))
        dr.text((10 + j * (w + 10), 50 + i * (h + 44) + 2), f'{n} · {t}', font=F, fill=(250, 210, 120) if t == 'B' else (200, 230, 255))
sh.save(out, quality=86); print(out, sh.size)
