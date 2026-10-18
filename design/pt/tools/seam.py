"""Kiểm vân lát: tỉ số chênh lệch qua đường nối (cột cuối↔cột đầu, hàng cuối↔hàng đầu) / chênh lệch giữa hai cột (hàng) kề nhau bên trong.
≈ 1 → không lộ đường nối; > 1,5 → lộ. Tuỳ chọn --fix: làm liền bằng hoà chéo bản dịch nửa ô (phép toán tất định, ghi lại), ghi <tên>_seam.png.
  python -I seam.py [--fix] <ảnh…>"""
import sys, json, numpy as np
from PIL import Image
fix = '--fix' in sys.argv; files = [a for a in sys.argv[1:] if a != '--fix']
def ratio(a):
    a = a.astype(np.float32)
    inx = np.abs(np.diff(a, axis=1)).mean(); iny = np.abs(np.diff(a, axis=0)).mean()
    sx = np.abs(a[:, 0] - a[:, -1]).mean(); sy = np.abs(a[0] - a[-1]).mean()
    return round(float(sx / inx), 2), round(float(sy / iny), 2)
out = []
for f in files:
    im = Image.open(f).convert('RGB'); a = np.asarray(im)
    rx, ry = ratio(a); rec = {'file': f, 'px': im.size, 'seam_x': rx, 'seam_y': ry}
    if fix and max(rx, ry) > 1.3:
        h, w = a.shape[:2]; b = np.roll(np.roll(a, w // 2, 1), h // 2, 0).astype(np.float32)
        yy, xx = np.mgrid[0:h, 0:w]; mx = 1 - np.abs(xx / (w - 1) * 2 - 1); my = 1 - np.abs(yy / (h - 1) * 2 - 1)
        m = np.clip(np.minimum(mx, my) * 4, 0, 1)[..., None]   # 1 ở giữa, 0 ở mép → mép lấy từ bản dịch (vốn liền)
        c = (a * m + b * (1 - m)).clip(0, 255).astype(np.uint8); g = f.rsplit('.', 1)[0] + '_seam.png'; Image.fromarray(c).save(g)
        rec['fixed'] = g; rec['after'] = ratio(c)
    out.append(rec); print(json.dumps(rec, ensure_ascii=False))
