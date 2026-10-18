"""PT2 · HC4: tờ phóng 400 % (A | C thô | LAI cuối) cho các vật bị loại/ngoại lệ — ra reports/pt2/kiem/bang-chung-400.jpg."""
import sys, os, cv2, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lai_common as LC
from PIL import Image, ImageDraw, ImageFont
F = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-SemiBold.otf', 22)
def ld(p):
    a = cv2.imread(p, -1); return ((a[..., :3] // 257).astype(np.uint8) if a.dtype == np.uint16 else a[..., :3])[..., ::-1]
rows = []
def crop(e, cname, box, title, k=4):
    x, y, w, h = box
    A = ld(f'/var/tmp/pt2/bg/{e}A/d2.png'); Ls = ld(f'/var/tmp/pt2/bg/{e}L/d2.png')
    C = np.asarray(Image.open(f'/var/tmp/pt2/c/{cname}.png').convert('RGB').resize((1920, 1080), Image.LANCZOS))
    ims = []
    for im, t in ((A, 'A'), (C, 'C thô'), (Ls, 'LAI cuối')):
        c = Image.fromarray(np.ascontiguousarray(im[y:y + h, x:x + w])).resize((w * k, h * k), Image.NEAREST)
        d = ImageDraw.Draw(c); d.rectangle([0, 0, 120, 30], fill=(14, 14, 16)); d.text((6, 3), t, font=F, fill=(240, 236, 220)); ims.append(c)
    r = Image.new('RGB', (sum(i.width for i in ims) + 16, ims[0].height + 34), (20, 20, 22)); ImageDraw.Draw(r).text((6, 4), title, font=F, fill=(255, 200, 150))
    xo = 0
    for i in ims: r.paste(i, (xo, 34)); xo += i.width + 8
    rows.append(r)
reg, mat, mc, _ = LC.load_cls('/var/tmp/pt2/bg/1782A'); ys, xs = np.where(reg == 9510); sel = ys > np.percentile(ys, 60)
crop(1782, '1782-d2-lan2', (int(xs[sel].min() - 10), int(ys[sel].min() - 10), 130, 110), 'V6 (1782): AI thay 2 thùng A bằng gạch vụn → bóng ma khi chiếu sáng → ghép lại thùng A')
crop(1943, '1943-d2', (440, 0, 260, 120), 'W3 (1943): AI đổi mép mái thành gờ đá chạm trổ → XOÁ (ghép lại ngói + gờ A)', k=3)
crop(1943, '1943-d2', (1250, 580, 260, 90), 'W5 (1943): công-xon dưới ban công do AI vẽ (không bóng) → NGOẠI LỆ chờ duyệt', k=3)
W = max(r.width for r in rows); sh = Image.new('RGB', (W, sum(r.height + 10 for r in rows)), (20, 20, 22)); yo = 0
for r in rows: sh.paste(r, (0, yo)); yo += r.height + 10
sh.save('/home/user/cine-lab/reports/pt2/kiem/bang-chung-400.jpg', quality=85); print(sh.size)
