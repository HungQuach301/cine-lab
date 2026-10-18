"""NC-AI · AI-1 thử vector hoá khối phố TỰ ĐỘNG trên Drinkwater 1786 "Plan of the Batteries" (SHA 476cb89b…) và so với khối dò tay của SH (so-hoa-1782-px.json).
Phương pháp cổ điển, không học máy (OpenCV): mực → mật độ chấm (khối phố tô chấm) → ngưỡng → đóng/mở hình thái → thành phần liên thông → đa giác.
Vùng so: hộp bao các khối dò tay vùng 'pho' + lề 60 px (cùng ô với ảnh kiểm SH). Đo: IoU hợp toàn vùng, IoU từng khối (ghép theo IoU lớn nhất), khối thừa/thiếu.
Dùng: python3 -I ai1_vector.py <anh.jpg> <so-hoa-1782-px.json> <thu_muc_ra> [ngưỡng_mật_độ]"""
import sys, json, cv2, numpy as np
img, sh, out = sys.argv[1:4]; T = float(sys.argv[4]) if len(sys.argv) > 4 else 0.10
CACH = sys.argv[5] if len(sys.argv) > 5 else 'matdo'  # matdo | vien (vùng kín bởi nét viền, lọc theo mật độ chấm bên trong)
im = cv2.imread(img); g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
F = [f for f in json.load(open(sh))['features'] if f['vung'] == 'pho' and f['loai'] == 'khoi_pho']
allp = np.vstack([np.array(f['px']) for f in json.load(open(sh))['features'] if f['vung'] == 'pho' and f['loai'] in ('khoi_pho', 'nha')])
x0, y0 = allp.min(0) - 60; x1, y1 = allp.max(0) + 60
G = g[y0:y1, x0:x1]; H, W = G.shape
ink = cv2.adaptiveThreshold(G, 1, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 25, 12).astype(np.float32)
# nét dài (đường viền khối, chữ lớn, tường) không phải chấm: bỏ thành phần mực có diện tích > 60 px
n, lab, st, _ = cv2.connectedComponentsWithStats(ink.astype(np.uint8), 8)
dots = np.isin(lab, np.where((st[:, cv2.CC_STAT_AREA] <= 60) & (np.arange(n) > 0))[0]).astype(np.float32)
dens = cv2.blur(dots, (21, 21))
if CACH == 'matdo':
    m = (dens > T).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((7, 7), np.uint8))
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
else:
    # nét = thành phần mực > 60 px (viền khối, tường, chữ); nối khe nhỏ bằng giãn 2 px; vùng nền kín = ứng viên
    lines = (~np.isin(lab, np.where((st[:, cv2.CC_STAT_AREA] <= 60) & (np.arange(n) > 0))[0]) & (lab > 0)).astype(np.uint8)
    lines = cv2.dilate(lines, np.ones((5, 5), np.uint8))
    nb, lb, sb, _ = cv2.connectedComponentsWithStats(1 - lines, 4)
    m = np.zeros_like(lines)
    for k in range(1, nb):
        a = sb[k, cv2.CC_STAT_AREA]; x, y, w, h = sb[k, :4]
        if a < 1200 or a > 60000 or x == 0 or y == 0 or x + w >= W or y + h >= H: continue
        if dens[lb == k].mean() > T: m[lb == k] = 1
    m = cv2.dilate(m, np.ones((5, 5), np.uint8))  # trả lại bề dày nét đã giãn
n, lab, st, _ = cv2.connectedComponentsWithStats(m, 8)
auto = []
for k in range(1, n):
    if st[k, cv2.CC_STAT_AREA] < 1200: continue
    cs, _ = cv2.findContours((lab == k).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    c = max(cs, key=cv2.contourArea); c = cv2.approxPolyDP(c, 3, True)
    auto.append(c.reshape(-1, 2))
def rast(polys):
    r = np.zeros((H, W), np.uint8)
    for p in polys: cv2.fillPoly(r, [np.asarray(p, np.int32)], 1)
    return r
hand = [np.array(f['px']) - [x0, y0] for f in F]
RH, RA = rast(hand), rast(auto)
iou_all = float((RH & RA).sum() / max(1, (RH | RA).sum()))
def iou(a, b): A, B = rast([a]), rast([b]); return float((A & B).sum() / max(1, (A | B).sum()))
per = []
for i, h in enumerate(hand):
    best = max(((iou(h, a), j) for j, a in enumerate(auto)), default=(0, -1))
    per.append({'id': F[i]['id'], 'iou': round(best[0], 3), 'auto': best[1]})
matched = {p['auto'] for p in per if p['iou'] >= 0.5}
thua = [j for j, a in enumerate(auto) if j not in matched and (rast([a]) & RH).sum() / max(1, rast([a]).sum()) < 0.5]
res = {'cach': CACH, 'nguong_mat_do': T, 'o': [int(x0), int(y0), int(x1), int(y1)], 'so_khoi_tay': len(hand), 'so_khoi_tu_dong': len(auto),
       'iou_hop_toan_vung': round(iou_all, 3), 'khoi_tay_iou_ge_0_5': sum(p['iou'] >= 0.5 for p in per),
       'khoi_tay_iou_ge_0_7': sum(p['iou'] >= 0.7 for p in per), 'iou_tung_khoi_trung_vi': round(float(np.median([p['iou'] for p in per])), 3),
       'khoi_thieu_iou_lt_0_5': [p['id'] for p in per if p['iou'] < 0.5], 'khoi_thua_tu_dong': len(thua),
       'dien_tich_tay_px': int(RH.sum()), 'dien_tich_tu_dong_px': int(RA.sum()), 'tung_khoi': per}
json.dump(res, open(f'{out}/ket-qua-{CACH}-T{T:.2f}.json', 'w'), ensure_ascii=False, indent=1)
vis = im[y0:y1, x0:x1].copy()
for p in hand: cv2.polylines(vis, [p.astype(np.int32)], True, (0, 0, 255), 2)
for j, p in enumerate(auto): cv2.polylines(vis, [p.astype(np.int32)], True, (0, 160, 0) if j not in thua else (255, 0, 255), 2)
cv2.imwrite(f'{out}/so-sanh-{CACH}-T{T:.2f}.jpg', vis, [cv2.IMWRITE_JPEG_QUALITY, 85])
print({k: v for k, v in res.items() if k != 'tung_khoi'})
