#!/opt/cine/bin/python
"""Last Lamplighters · nhà máy — thumbnail 1280×720 có lề an toàn (G2 tập 2: "OPERATORS" bị cắt chữ S ở mép phải).

make(img, lines, out, align='left'|'center', top=None)
  img   : PIL.Image nền (tự co về 1280×720)
  lines : [(chữ, cỡ px mong muốn, màu RGB, 'serif'|'sans')]
  - Mỗi dòng (gồm cả nền chữ) phải nằm trong lề an toàn SAFE = 5 % mỗi cạnh; dòng quá rộng thì tự thu cỡ chữ cho vừa.
  - Ghi <out>.boxes.json: hộp nền chữ từng dòng (toạ độ ảnh) → qc.py mục Q12 kiểm chữ không chạm/vượt lề an toàn.
"""
import json
from PIL import Image, ImageDraw, ImageFont

W, H, SAFE, PAD = 1280, 720, 0.05, 18
FONTS = {'serif': '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf', 'sans': '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'}
X0, X1, Y0, Y1 = W * SAFE, W * (1 - SAFE), H * SAFE, H * (1 - SAFE)


def make(img, lines, out, align='left', top=None):
    im = img.convert('RGB').resize((W, H)); d = ImageDraw.Draw(im, 'RGBA')
    maxw = (X1 - X0) - 2 * PAD - 12  # bề rộng chữ tối đa trong lề (trừ nền chữ, 1 px đệm mỗi bên)
    y, boxes = (top if top is not None else Y0 + PAD + 2), []
    for s, px, col, kind in lines:
        while px > 20:
            F = ImageFont.truetype(FONTS[kind], px); l, t, r, b = d.textbbox((0, 0), s, font=F)
            if r - l <= maxw: break
            px -= 2
        w = r - l; x = X0 + PAD + 6 - l if align == 'left' else (W - w) / 2 - l
        box = [x + l - PAD, y + t - PAD / 2, x + r + PAD, y + b + PAD / 2]
        d.rectangle(box, fill=(20, 26, 46, 215)); d.text((x, y), s, font=F, fill=col)
        boxes.append(dict(s=s, px=px, box=[round(v, 1) for v in box])); y = box[3] + 22
    im.save(out, quality=90)
    json.dump(dict(size=[W, H], safe=SAFE, boxes=boxes), open(out + '.boxes.json', 'w'), indent=1, ensure_ascii=False)
    return boxes


def check(path):
    """Trả danh sách lỗi: ảnh khác 1280×720, hoặc hộp chữ chạm/vượt lề an toàn 5 %."""
    err = []; im = Image.open(path)
    if im.size != (W, H): err.append(f'{path}: kích thước {im.size} ≠ 1280×720')
    try: B = json.load(open(path + '.boxes.json'))['boxes']
    except FileNotFoundError: return err + [f'{path}: thiếu .boxes.json (dựng bằng scripts/ll/thumb.py)']
    for b in B:
        x0, y0, x1, y1 = b['box']
        if x0 <= X0 or y0 <= Y0 or x1 >= X1 or y1 >= Y1: err.append(f'“{b["s"]}” hộp {b["box"]} chạm/vượt lề an toàn ({X0:.0f}–{X1:.0f} × {Y0:.0f}–{Y1:.0f})')
    return err
