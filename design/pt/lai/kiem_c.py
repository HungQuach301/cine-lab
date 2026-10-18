"""PT2 · HC4 kiểm dữ kiện tấm C — công cụ RÀ (không tự kết luận): (a) bản đồ khác biệt A↔C theo vùng + ứng viên VẬT THÊM/ĐỔI
(khác biệt cấu trúc cục bộ sau khi bỏ tần thấp, ở dải sát mặt đất ≤ 2,6 m theo hình học cảnh, và mọi vùng có màu bão hoà lạ trên tường/mái),
(b) xuất ảnh A|C phóng 400 % từng ứng viên + tờ rà 200 % toàn khung để NGƯỜI rà (phiên) phân loại vào reports/pt2/kiem-du-kien.json.
  /opt/cine/bin/python -I kiem_c.py <nền A dir> <ảnh C png> <ra dir>"""
import sys, os, json, math, numpy as np, cv2
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lai_common as LC
BG, CP, OUT = sys.argv[1:4]; os.makedirs(OUT, exist_ok=True)
A = cv2.imread(os.path.join(BG, 'd2.png'), cv2.IMREAD_UNCHANGED)[..., :3]; A = (A / 257.0 + 0.5).astype(np.uint8)
H, W = A.shape[:2]
C = cv2.imread(CP, cv2.IMREAD_UNCHANGED)[..., :3]
C = (C / 257.0 + 0.5).astype(np.uint8) if C.dtype == np.uint16 else cv2.resize(C, (W, H), interpolation=cv2.INTER_AREA)   # nền LAI d2 (16 bit) hoặc ảnh C thô
edit = ~LC.protected_mask(BG, reveals=True)
meta = json.load(open(os.path.join(BG, 'meta.json'))); cam = meta['camera']; dep = LC.exr(os.path.join(BG, 'depth.exr'))
# độ cao thế giới của từng điểm ảnh (hình học cảnh A)
fpx = cam['fpx']; yy, xx = np.mgrid[0:H, 0:W].astype(np.float32); p = math.radians(cam['pitch'])
dx, dy = (xx - W / 2) / fpx, -(yy - H / 2) / fpx
dirz = (dy * math.cos(p) + math.sin(p)) / np.sqrt(dx * dx + dy * dy + 1)
zw = cam['pos'][2] + np.minimum(dep, 5000) * dirz
band = edit & (zw < 2.6)
gA = cv2.cvtColor(A, cv2.COLOR_BGR2GRAY).astype(np.float32) + 4; gC = cv2.cvtColor(C, cv2.COLOR_BGR2GRAY).astype(np.float32) + 4
r = np.log(gC / gA); r = r - cv2.GaussianBlur(r, (0, 0), 25)
eA = cv2.Canny(A, 60, 150) > 0; eC = cv2.Canny(C, 60, 150) > 0
newedge = eC & ~(cv2.dilate(eA.astype(np.uint8), np.ones((5, 5), np.uint8)) > 0)
dens = cv2.GaussianBlur(newedge.astype(np.float32), (0, 0), 6)
cand = band & ((np.abs(r) > 0.5) | (dens > 0.18))
hsvC = cv2.cvtColor(C, cv2.COLOR_BGR2HSV); hsvA = cv2.cvtColor(A, cv2.COLOR_BGR2HSV)
hue = hsvC[..., 0].astype(int)   # màu cờ/biển hiệu/sơn: đỏ, lam, lục bão hoà mạnh
colour = edit & (hsvC[..., 1] > 150) & (hsvC[..., 2] > 50) & ((hue < 8) | (hue > 170) | ((hue > 95) & (hue < 130)) | ((hue > 45) & (hue < 85)))
cand |= colour
cand = cv2.morphologyEx(cand.astype(np.uint8), cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
cand = cv2.dilate(cand, np.ones((15, 15), np.uint8))
n, cc, st, _ = cv2.connectedComponentsWithStats(cand)
boxes = [tuple(int(v) for v in s[:4]) for s in st[1:] if s[4] >= 900]
items = []
for k, (x, y, w, h) in enumerate(sorted(boxes, key=lambda b: (b[0], b[1]))):
    cx, cy = x + w // 2, y + h // 2; s = max(w, h, 60); x0, y0 = max(0, cx - s // 2 - 8), max(0, cy - s // 2 - 8); x1, y1 = min(W, x0 + s + 16), min(H, y0 + s + 16)
    a = cv2.resize(A[y0:y1, x0:x1], None, fx=4, fy=4, interpolation=cv2.INTER_NEAREST); c = cv2.resize(C[y0:y1, x0:x1], None, fx=4, fy=4, interpolation=cv2.INTER_NEAREST)
    if a.shape[0] > 900: f = 900 / a.shape[0]; a = cv2.resize(a, None, fx=f, fy=f); c = cv2.resize(c, None, fx=f, fy=f)
    sep = np.full((a.shape[0], 8, 3), 255, np.uint8)
    cv2.imwrite(os.path.join(OUT, f'ung-vien-{k:02d}.jpg'), np.hstack([a, sep, c]), [cv2.IMWRITE_JPEG_QUALITY, 88])
    items.append({'id': k, 'hop_px_1080p': [x0, y0, x1 - x0, y1 - y0], 'z_tb_m': round(float(np.median(zw[y0:y1, x0:x1])), 2), 'mau_bao_hoa': bool(colour[y0:y1, x0:x1].any())})
# tờ rà 200 %: 16 ô 480×270 → mỗi ô phóng 2×, A trên C dưới
for t in range(16):
    ty, tx = divmod(t, 4); x0, y0 = tx * 480, ty * 270
    if not edit[y0:y0 + 270, x0:x0 + 480].any(): continue
    a = cv2.resize(A[y0:y0 + 270, x0:x0 + 480], None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC); c = cv2.resize(C[y0:y0 + 270, x0:x0 + 480], None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    cv2.imwrite(os.path.join(OUT, f'o-{t:02d}.jpg'), np.vstack([a, np.full((6, 960, 3), 255, np.uint8), c]), [cv2.IMWRITE_JPEG_QUALITY, 85])
json.dump({'ung_vien': items, 'pct_duoc_sua': round(float(edit.mean() * 100), 2), 'pct_dai_mat_dat': round(float(band.mean() * 100), 2)}, open(os.path.join(OUT, 'ung-vien.json'), 'w'), indent=1, ensure_ascii=False)
print(len(items), 'ứng viên')
