"""PT3 · HC4 — sàng tự động trước khi rà mắt từng vân AI (KHÔNG thay rà mắt; chỉ xếp ưu tiên):
  duong_thang — số đoạn thẳng ≥ 1 m (HoughP trên Canny) nằm SÂU trong vùng mặt nạ (cách mép mặt nạ ≥ 0,25 m): mép cửa/đá góc/bậu/ống vẽ thêm
                tạo đường thẳng dài; vữa nứt, vết ố hiếm khi thẳng ≥ 1 m. So với cùng thước trên ảnh vào (A) cùng vùng.
  den_moi     — tỉ lệ điểm gần đen trong mặt nạ (AI tô đen / dời khung).
  kiem_van.py <ai_in/site> <thư mục ảnh AI> <ra.json>"""
import sys, os, json
import numpy as np, cv2
from PIL import Image
DI, DA, OUT = sys.argv[1:4]
man = json.load(open(os.path.join(DI, 'chunks.json'))); ppm_e = {'street': 64, 'kb': 80}[man['site']]; res = []
def lines(g, interior, ppm):
    e = cv2.Canny(g, 50, 140); e[~interior] = 0
    L = cv2.HoughLinesP(e, 1, np.pi / 180, threshold=int(ppm * 0.6), minLineLength=int(ppm * 1.0), maxLineGap=int(ppm * 0.05))
    return 0 if L is None else len(L)
for c in man['chunks']:
    if 'bo_qua' in c: continue
    for t in ('-thu2', ''):
        p = os.path.join(DA, c['name'] + t + '.jpg')
        if os.path.exists(p): break
    else: continue
    ppm = (ppm_e if c['kind'] == 'elev' else man['top']['ppm']) * c['W_api'] / max(1, c['x1'] - c['x0'])
    inp = np.asarray(Image.open(os.path.join(DI, c['name'] + '.png')).convert('L')); out = np.asarray(Image.open(p).convert('L').resize(inp.shape[::-1]))
    m = np.asarray(Image.open(os.path.join(DI, c['name'] + '_mask.png')))[..., 3] == 0
    interior = cv2.erode(m.astype(np.uint8), np.ones((int(ppm * 0.5) | 1,) * 2)) > 0
    r = {'khuc': c['name'], 'tep': os.path.basename(p), 'duong_thang_AI': lines(out, interior, ppm), 'duong_thang_A': lines(inp, interior, ppm),
         'den_moi_pct': round(100 * float(((out < 20) & m).sum()) / max(1, m.sum()), 2)}
    r['co'] = (['duong_thang'] if r['duong_thang_AI'] > r['duong_thang_A'] + 3 else []) + (['den'] if r['den_moi_pct'] > 1 else [])
    res.append(r)
json.dump(res, open(OUT, 'w'), indent=1, ensure_ascii=False)
print(len(res), 'khúc;', sum(1 for r in res if 'duong_thang' in r['co']), 'cờ đường thẳng;', sum(1 for r in res if 'den' in r['co']), 'cờ đen')
for r in res:
    if r['co']: print(r)
