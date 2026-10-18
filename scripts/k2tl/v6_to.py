#!/opt/cine/bin/python
"""V6 bước 9 · TỜ SO 6 KHUNG: mỗi hàng một loại cảnh P1–P6, ba cột TỐT NHẤT (Cycles lai) | SẢN XUẤT (llvmpipe V6) | V5b-2d — khung SẠCH, cùng số khung.
  v6_to.py <thư mục tot> <thư mục khung sx> <ra.jpg> [--cot 800]"""
import glob, os, sys
from PIL import Image, ImageDraw, ImageFont
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
TOT, SX, OUT = sys.argv[1:4]; CW = int(sys.argv[sys.argv.index('--cot') + 1]) if '--cot' in sys.argv else 800; CH = CW * 9 // 16
OLD = {1: 'd-1-vay-ham.jpg', 2: 'd-2-cang-bo.jpg', 3: 'd-3-pho-day.jpg', 4: 'd-4-hero.jpg', 5: 'd-5-toan-canh.jpg', 6: 'd-6-bo-chien-su.jpg'}
TEN = {1: 'P1 siege', 2: 'P2 harbour', 3: 'P3 dense street', 4: 'P4 hero fort', 5: 'P5 panorama', 6: 'P6 shore battle'}
COT = ('BEST (Cycles hybrid)', 'PRODUCTION (llvmpipe V6)', 'V5b-2d')
TOP, LW = 40, 215
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 22)
sheet = Image.new('RGB', (LW + 3 * CW, TOP + 6 * CH), (18, 18, 18)); d = ImageDraw.Draw(sheet)
for j, t in enumerate(COT): d.text((LW + j * CW + 12, 8), t, fill=(235, 235, 235), font=F)
for i in range(1, 7):
    src = [os.path.join(TOT, f'tot-{i}.png'), (glob.glob(os.path.join(SX, f'sach-{i}', '*.jpg')) or [None])[0], os.path.join(REPO, 'reports', 'v5b2d', 'khung', OLD[i])]
    y = TOP + (i - 1) * CH; d.text((10, y + CH // 2 - 12), TEN[i], fill=(235, 235, 235), font=F)
    for j, p in enumerate(src):
        if p and os.path.exists(p): sheet.paste(Image.open(p).convert('RGB').resize((CW, CH), Image.LANCZOS), (LW + j * CW, y))
        else: d.text((LW + j * CW + 20, y + CH // 2), '(missing)', fill=(200, 80, 80), font=F)
sheet.save(OUT, quality=88); print(OUT, sheet.size, round(os.path.getsize(OUT) / 1e6, 2), 'MB')
