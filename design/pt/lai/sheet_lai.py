"""PT2 · tờ khung so sánh: (1) LAI | A-thuần cùng khung neo × 4 giờ khai trước; (2) chuỗi HC: A d2 → mặt nạ → C thô → LAI d2 (vùng bảo vệ tô viền).
  /opt/cine/bin/python -I sheet_lai.py <thư mục khung> <ra dir>"""
import sys, os, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
D, OUT = sys.argv[1:3]; os.makedirs(OUT, exist_ok=True)
F = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-SemiBold.otf', 26)
def lab(im, t, col=(240, 236, 220)):
    d = ImageDraw.Draw(im); bb = d.textbbox((0, 0), t, font=F); d.rectangle([0, 0, bb[2] + 16, bb[3] + 12], fill=(14, 14, 16)); d.text((8, 4), t, font=F, fill=col); return im
W, H = 800, 450
rows = []
for e in (1782, 1943):
    for t in ('sang', 'trua', 'chieu', 'dem'):
        cells = [lab(Image.open(os.path.join(D, f'{e}-{t}-{b}-notext.png')).convert('RGB').resize((W, H), Image.LANCZOS), f'{e} · {t} · {n}', c)
                 for b, n, c in (('LAI', 'LAI (A + C)', (255, 190, 150)), ('A', 'A-thuần', (170, 210, 255)))]
        r = Image.new('RGB', (2 * W + 8, H), (20, 20, 22)); r.paste(cells[0], (0, 0)); r.paste(cells[1], (W + 8, 0)); rows.append(r)
sh = Image.new('RGB', (2 * W + 8, len(rows) * (H + 8)), (20, 20, 22))
for i, r in enumerate(rows): sh.paste(r, (0, i * (H + 8)))
sh.save(os.path.join(OUT, 'to-khung-LAI-A.jpg'), quality=86)
BG = '/var/tmp/pt2/bg'; CD = '/var/tmp/pt2/c'
row2 = []
for e, c in ((1782, '1782-d2-lan2'), (1943, '1943-d2')):
    a = (cv2.imread(f'{BG}/{e}A/d2.png', -1)[..., :3] // 257).astype(np.uint8)[..., ::-1]
    m = cv2.imread(f'{CD}/{c}-matna.png', -1)[..., 3]; m = cv2.resize(m, (1920, 1080), interpolation=cv2.INTER_NEAREST) > 127
    am = a.copy(); am[m] = (am[m] * 0.35 + np.array([200, 30, 30]) * 0.65).astype(np.uint8)
    cr = np.asarray(Image.open(f'{CD}/{c}.png').convert('RGB').resize((1920, 1080), Image.LANCZOS))
    l = (cv2.imread(f'{BG}/{e}L/d2.png', -1)[..., :3] // 257).astype(np.uint8)[..., ::-1].copy()
    pv = cv2.imread(f'{BG}/{e}L/bao_ve.png', 0) > 127; edge = cv2.morphologyEx(pv.astype(np.uint8), cv2.MORPH_GRADIENT, np.ones((3, 3), np.uint8)) > 0
    l[edge] = (60, 230, 255)
    ims = [lab(Image.fromarray(x).resize((W, H), Image.LANCZOS), t) for x, t in ((a, f'{e} · A lượt d2'), (am, 'mặt nạ gửi AI (đỏ = giữ)'), (cr, 'C thô (gpt-image-2.5-sunburst)'), (l, 'LAI d2 (viền xanh = vùng bảo vệ = điểm ảnh A)'))]
    r = Image.new('RGB', (4 * W + 24, H), (20, 20, 22))
    for i, im in enumerate(ims): r.paste(im, (i * (W + 8), 0))
    row2.append(r)
s2 = Image.new('RGB', (4 * W + 24, 2 * H + 8), (20, 20, 22)); s2.paste(row2[0], (0, 0)); s2.paste(row2[1], (0, H + 8))
s2.save(os.path.join(OUT, 'to-chuoi-HC.jpg'), quality=86)
print('ok')
