#!/opt/cine/bin/python
"""BAN-CUOI-T4-B1 · tờ so / tờ khung (JPG ≤ 2 MB, vào git) — lưới ảnh có chú thích.
  to_b1.py <ra.jpg> "<tiêu đề>" <số cột> <ô rộng px> <ảnh1>::<chú thích1> <ảnh2>::<chú thích2> …   (ảnh "-" = ô trống)"""
import os, sys
from PIL import Image, ImageDraw, ImageFont
F = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'


def font(n):
    try: return ImageFont.truetype(F, n)
    except Exception: return ImageFont.load_default()


def main():
    out, title, nc, cw = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]); items = [a.split('::', 1) + [''] for a in sys.argv[5:]]
    cells = []
    for it in items:
        p, cap = it[0], it[1]
        im = Image.open(p).convert('RGB') if p != '-' and os.path.exists(p) else None
        if im is not None: im = im.resize((cw, round(im.height * cw / im.width)), Image.LANCZOS)
        cells.append((im, cap))
    ch = max([c[0].height for c in cells if c[0] is not None] or [cw * 9 // 16]); cap_h = 30; th = 44
    nr = (len(cells) + nc - 1) // nc; W = nc * cw + (nc + 1) * 6; H = th + nr * (ch + cap_h + 6) + 6
    S = Image.new('RGB', (W, H), (18, 18, 20)); d = ImageDraw.Draw(S); d.text((10, 10), title, fill=(235, 235, 235), font=font(22))
    for i, (im, cap) in enumerate(cells):
        r, c = divmod(i, nc); x = 6 + c * (cw + 6); y = th + r * (ch + cap_h + 6)
        if im is not None: S.paste(im, (x, y))
        else: d.rectangle([x, y, x + cw, y + ch], outline=(80, 80, 80))
        d.text((x + 4, y + ch + 5), cap, fill=(230, 230, 210), font=font(17))
    q = 90
    while True:
        S.save(out, quality=q, optimize=True)
        if os.path.getsize(out) <= 2_000_000 or q <= 40: break
        q -= 6
    print(out, S.size, os.path.getsize(out), 'q', q)


if __name__ == '__main__': main()
