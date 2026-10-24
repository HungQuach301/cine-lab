#!/opt/cine/bin/python
"""THU-B-T4 · TỜ SO (không mù — nhãn rõ) + ô 1080p JPG ≤ 2 MB.
  to_so_thub.py <cấu_hình.json>   cấu hình: {"ra": "reports/thu-b-t4/to-so-thu-b.jpg", "o_dir": "reports/thu-b-t4/khung",
                                      "hang": [{"ten": "...", "vai": "...", "o": [{"anh": <đường dẫn>, "nhan": "...", "ghi": ["dòng kết quả", …], "ten_tep": "<khung>-<cột>"} …],
                                                "phu": [{"anh": …, "nhan": …}]  (dải phụ nhỏ: khung cuối timelapse)}]}
Mỗi ô 960×540 trên tờ (thu từ 1080p, INTER_AREA); dòng kết quả dưới ô; dải phụ 480×270."""
import json, os, sys
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
FONT = next((f for f in ('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf') if os.path.exists(f)), None)
FB = next((f for f in ('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',) if os.path.exists(f)), FONT)
f = lambda s, b=False: ImageFont.truetype(FB if b else FONT, s) if FONT else ImageFont.load_default()
CW, CH, PAD, TXT = 960, 540, 16, 150


def jpg_le_2mb(im, p):
    q = 92
    while True:
        im.save(p, 'JPEG', quality=q, optimize=True)
        if os.path.getsize(p) <= 2_000_000 or q <= 60: return q
        q -= 4


def main():
    C = json.load(open(sys.argv[1])); od = os.path.join(REPO, C['o_dir']); os.makedirs(od, exist_ok=True)
    nc = max(len(h['o']) for h in C['hang']); W = PAD + nc * (CW + PAD)
    blocks = []
    for h in C['hang']:
        ph = (270 + 40) if h.get('phu') else 0
        B = Image.new('RGB', (W, 70 + CH + TXT + ph + PAD), (18, 18, 20)); d = ImageDraw.Draw(B)
        d.text((PAD, 14), h['ten'], fill=(255, 220, 120), font=f(30, True)); d.text((PAD + 520, 22), h.get('vai', ''), fill=(200, 200, 200), font=f(20))
        for j, o in enumerate(h['o']):
            x = PAD + j * (CW + PAD); im = Image.open(o['anh']).convert('RGB')
            if o.get('ten_tep'): q = jpg_le_2mb(im.resize((1920, 1080), Image.LANCZOS) if im.size != (1920, 1080) else im, os.path.join(od, o['ten_tep'] + '.jpg'))
            B.paste(im.resize((CW, CH), Image.LANCZOS), (x, 70))
            d.rectangle([x, 70, x + 430, 70 + 40], fill=(0, 0, 0)); d.text((x + 10, 76), o['nhan'], fill=(255, 255, 255), font=f(24, True))
            for i, g in enumerate(o.get('ghi', [])[:6]): d.text((x + 4, 70 + CH + 8 + i * 23), g, fill=(220, 230, 220), font=f(18))
        for j, o in enumerate(h.get('phu', [])):
            x = PAD + j * (480 + PAD); y = 70 + CH + TXT; im = Image.open(o['anh']).convert('RGB').resize((480, 270), Image.LANCZOS); B.paste(im, (x, y + 30))
            d.text((x, y + 4), o['nhan'], fill=(255, 220, 160), font=f(18, True))
        blocks.append(B)
    S = Image.new('RGB', (W, sum(b.size[1] for b in blocks)), (18, 18, 20)); y = 0
    for b in blocks: S.paste(b, (0, y)); y += b.size[1]
    ra = os.path.join(REPO, C['ra']); q = 90
    while True:
        S.save(ra, 'JPEG', quality=q, optimize=True)
        if os.path.getsize(ra) <= 4_500_000 or q <= 60: break
        q -= 5
    print(ra, S.size, os.path.getsize(ra) // 1024, 'KB', 'q', q)


if __name__ == '__main__': main()
