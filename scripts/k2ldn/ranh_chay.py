#!/opt/cine/bin/python
"""TIEN-KY-T4 · ranh vùng cháy CUỐI 1666 từ bản đồ Doornick 1666 (vùng để trắng = đã cháy; bậc 1) → đa giác EPSG:27700.
  ranh_chay.py  → channel-k2/k2c-t4-02/mo-hinh/ranh-chay-1666-cuoi.json (+ diện tích, so "over 400 acres")
Cách: mật độ mực (ngưỡng < 150, hộp 45 px) < 0,30 → cắt theo bờ sông vẽ tay → thành phần chứa tâm City → đóng 41 px → đường viền → TPS/affine theo khop-doornick.json."""
import json, os, cv2, numpy as np
from scipy.interpolate import RBFInterpolator
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
K = json.load(open(os.path.join(REPO, 'channel-k2/k2c-t4-02/mo-hinh/khop-doornick.json')))
D = [d for d in K['diem'] if d.get('dung', True)]
PX = np.array([d['px'] for d in D], float); EN = np.array([d['en'] for d in D], float)
tps = RBFInterpolator(PX, EN, kernel='thin_plate_spline', smoothing=0.0)
c = np.array(K['ket_qua']['affine']['he_so'])
aff = lambda p: np.stack([np.ones(len(p)), p[:, 0] / 1000, p[:, 1] / 1000], 1) @ c
im = cv2.imread(os.environ.get('LDN_SRC', '/var/tmp/ldn/tu-lieu') + '/rijks-doornick-0.jpg', 0)
d = cv2.blur((im < 150).astype(np.float32), (45, 45)); m = (d < 0.30).astype(np.uint8)
bank = np.array([[1800, 1760], [1950, 1700], [2120, 1655], [2390, 1612], [2600, 1616], [2900, 1612], [3230, 1602], [3450, 1600], [3700, 1625], [4400, 1625], [4400, 4650], [1800, 4650]], np.int32)
cv2.fillPoly(m, [bank], 0); m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((9, 9), np.uint8))
n, lab, st, _ = cv2.connectedComponentsWithStats(m, 8); mask = (lab == lab[1200, 2850]).astype(np.uint8) * 255
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((41, 41), np.uint8))
cs, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE); cnt = max(cs, key=cv2.contourArea)
cnt = cv2.approxPolyDP(cnt, 3, True)[:, 0, :].astype(float)
def area(p): x, y = p[:, 0], p[:, 1]; return 0.5 * abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))
out = {'nguon': K['ban_do'], 'bac': 1, 'cach': __doc__.split('\n')[2].strip(), 'px': cnt.astype(int).tolist()}
for name, f in (('tps', tps), ('affine', aff)):
    P = f(cnt); a = area(P); out[name] = {'en': np.round(P, 1).tolist(), 'dien_tich_ha': round(a / 1e4, 1), 'acre': round(a / 4046.86, 0)}
    print(name, 'diện tích %.1f ha = %d acre' % (a / 1e4, a / 4046.86), 'đỉnh', len(P))
json.dump(out, open(os.path.join(REPO, 'channel-k2/k2c-t4-02/mo-hinh/ranh-chay-1666-cuoi.json'), 'w'))
cv2.imwrite('/var/tmp/ldn/crop/chay-mask.png', mask)
