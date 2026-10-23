#!/opt/cine/bin/python
"""LOOK-T4-V2 · TỜ SO trước/sau (KHÔNG mù — chủ dự án so trước/sau) → reports/look-t4-v2/to-so-v2.jpg + ô 1080p reports/look-t4-v2/khung/<hàng>-<cột>.jpg (JPG ≤ 2 MB).
Cột: 'LOOK-T4 đã chọn' (ô A của tờ mù LOOK-T4, giải theo reports/look-t4/khoa.json) · 'V2 3D' · 'V2 + tấm nền Gemini' · 'V2 + tấm nền OpenAI' (chỉ 4 khung rộng)
· 'Cycles' (chỉ khung lửa có dựng Cycles). Ô AI = tấm TỐT NHẤT của công cụ đó (lượt đạt cổng sớm nhất; không lượt nào đạt → lượt cuối, nhãn 'TRƯỢT cổng').
  to_so_v2.py <cấu hình json>   (cấu hình: {"o": {"<hàng>": {"<cột>": "<đường ảnh>", …}}, "nhan": {"<hàng>/<cột>": "<nhãn phụ>"}})"""
import json, os, sys
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RD = os.path.join(REPO, 'reports/look-t4-v2'); KH = os.path.join(RD, 'khung'); os.makedirs(KH, exist_ok=True)
ROWS = [('M1-rong', '1666 trước cháy · toàn cảnh P1 Bankside'), ('M1-trung', '1666 · tháp St Saviour (cầu London)'), ('M2-ngay', '3/9/1666 15:00 · ngày khói (P1)'),
        ('M2-dem', '2/9/1666 23:00 · đêm lửa từ giữa sông'), ('M3-rong', '29/12/1940 21:30 · toàn cảnh P1'), ('M3-trung', '29/12/1940 22:30 · mái vòm từ Fleet St'),
        ('M4-rong', '2026 ngày · chân trời City (P1)'), ('M4-trung', '2026 · mái vòm từ Fleet St (mặt phố)')]
COLS = [('look-t4', 'LOOK-T4 đã chọn (A)'), ('v2-3d', 'V2 3D'), ('v2-gemini', 'V2 + tấm nền Gemini'), ('v2-openai', 'V2 + tấm nền OpenAI'), ('cycles', 'Cycles GPU (cùng máy/giờ)')]


def font(n):
    for f in ('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'):
        if os.path.exists(f): return ImageFont.truetype(f, n)
    return ImageFont.load_default()


def luu_1080(src, dst):
    im = cv2.imread(src); im = cv2.resize(im, (1920, 1080), interpolation=cv2.INTER_AREA) if im.shape[:2] != (1080, 1920) else im
    for q in (93, 90, 86, 82, 78):
        cv2.imwrite(dst, im, [cv2.IMWRITE_JPEG_QUALITY, q])
        if os.path.getsize(dst) <= 2_000_000: return q
    return q


def main(cfg):
    C = json.load(open(cfg)); O = C['o']; NH = C.get('nhan', {})
    cols = [c for c in COLS if any(c[0] in O.get(r, {}) for r, _ in ROWS)]
    cw, ch, lw, hh = 640, 360, 300, 46; W = lw + cw * len(cols); H = hh + ch * len(ROWS)
    sheet = Image.new('RGB', (W, H), (18, 18, 20)); dr = ImageDraw.Draw(sheet); f1, f2 = font(20), font(17)
    for j, (c, t) in enumerate(cols): dr.text((lw + j * cw + 10, 12), t, fill=(235, 235, 235), font=f1)
    for i, (r, t) in enumerate(ROWS):
        y = hh + i * ch; dr.text((10, y + 10), r, fill=(255, 220, 160), font=f1)
        for k, line in enumerate([t[x:x + 26] for x in range(0, len(t), 26)]): dr.text((10, y + 40 + 22 * k), line, fill=(210, 210, 210), font=f2)
        for j, (c, _) in enumerate(cols):
            p = O.get(r, {}).get(c)
            if not p:
                dr.text((lw + j * cw + 230, y + 170), '—', fill=(90, 90, 90), font=f1); continue
            q = luu_1080(p, os.path.join(KH, f'{r}-{c}.jpg'))
            th = Image.open(os.path.join(KH, f'{r}-{c}.jpg')).convert('RGB').resize((cw - 4, ch - 4), Image.LANCZOS); sheet.paste(th, (lw + j * cw + 2, y + 2))
            lab = NH.get(f'{r}/{c}')
            if lab: dr.rectangle([lw + j * cw + 2, y + ch - 30, lw + j * cw + 2 + 9 * len(lab) + 12, y + ch - 4], fill=(0, 0, 0)); dr.text((lw + j * cw + 8, y + ch - 28), lab, fill=(255, 210, 120), font=f2)
    out = os.path.join(RD, 'to-so-v2.jpg')
    for q in (90, 85, 80, 75):
        sheet.save(out, quality=q)
        if os.path.getsize(out) <= 4_500_000: break
    print(out, sheet.size, os.path.getsize(out))


if __name__ == '__main__': main(sys.argv[1])
