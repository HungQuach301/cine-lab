"""PT3 · ĐO cú máy (máy chuyển động, cảnh tĩnh):
  nhấp nháy  — mỗi cặp khung liền kề (t, t+1): điểm ảnh của khung t+1 có vị trí thế giới P (lượt 'pos') được chiếu vào máy khung t,
               chỉ giữ điểm THẤY ĐƯỢC ở khung t (lượt 'pos' khung t tại đó trùng P ≤ 0,10 m + 0,2 %·khoảng cách); sai khác |Y(t+1) − Y(t)(warp)|
               (0..255) trên vùng TĨNH = mặt có vân AI (cờ 'ai' của lần dựng HC7 — cùng tập điểm cho A, HC7, HC8) và trên mọi mặt toà;
               báo TB + p95 + tỉ lệ điểm |Δ| > 12 ("chớp"); A là đường gốc (nhiễu dựng + đổi góc nhìn), so A.
  nhất quán  — cùng điểm bề mặt ở khung đầu và khung cuối (thấy ở cả hai): |ΔY| TB và ΔE trung bình màu theo vùng.
  chuẩn hình — cách điều phối: thu 640×360 (INTER_AREA), cắt y 60–300 (cả bề ngang): trung vị bão hoà HSV, colorfulness (Hasler–Süsstrunk),
               FIND_EDGES (PIL) trên độ sáng; thêm |Laplace| (cổng 16/10) để đối chiếu.
  do_pt3.py <site> <thư mục khung (PNG)> <thư mục pos/aux> <thư mục aux có cờ ai (HC7)> <ra.json> [--step 1]"""
import sys, os, json, glob
import numpy as np, cv2
from PIL import Image, ImageFilter
from scipy.ndimage import map_coordinates
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..', 'scene'))
import exr, cams as CM
site, DF, DP, DAI, OUT = sys.argv[1:6]; STEP = int(sys.argv[sys.argv.index('--step') + 1]) if '--step' in sys.argv else 1

def Y(im): return 0.2126 * im[..., 0] + 0.7152 * im[..., 1] + 0.0722 * im[..., 2]
def load(f):
    im = np.asarray(Image.open(os.path.join(DF, f'{f:04d}.png')).convert('RGB'), np.float32)
    pos = exr.read(os.path.join(DP, f'{f:04d}_pos.exr'))[..., :3]; aux = exr.read(os.path.join(DP, f'{f:04d}_aux.exr'))
    ai = exr.read(os.path.join(DAI, f'{f:04d}_aux.exr'))[..., 1] > 0.5 if os.path.exists(os.path.join(DAI, f'{f:04d}_aux.exr')) else np.zeros(im.shape[:2], bool)
    return im, pos, np.rint(aux[..., 0]), ai

def warp(f_src, src, pos_src, P):
    """lấy mẫu ảnh khung f_src tại chiếu của các điểm P; trả (giá trị, hợp lệ)."""
    cpos, clook, mm = CM.cam_at(site, f_src); H, W = src.shape[:2]
    fwd, r, u = CM.basis(cpos, clook); d = P - np.array(cpos); z = d @ np.array(fwd); fpx = mm / 36.0 * W
    px = W / 2 + fpx * (d @ np.array(r)) / z - 0.5; py = H / 2 - fpx * (d @ np.array(u)) / z - 0.5
    ok = (z > 0.5) & (px >= 0) & (px <= W - 1) & (py >= 0) & (py <= H - 1); q = np.stack([np.clip(py, 0, H - 1), np.clip(px, 0, W - 1)])
    Pq = np.stack([map_coordinates(pos_src[..., c], q, order=0) for c in range(3)], 1)
    ok &= np.linalg.norm(Pq - P, axis=1) < 0.10 + 0.002 * np.linalg.norm(d, axis=1)
    v = np.stack([map_coordinates(src[..., c], q, order=1) for c in range(src.shape[-1])], 1) if src.ndim == 3 else map_coordinates(src, q, order=1)
    return v, ok

def look(im):
    s = cv2.resize(im.astype(np.uint8)[..., ::-1], (640, 360), interpolation=cv2.INTER_AREA)[60:300]
    hsv = cv2.cvtColor(s, cv2.COLOR_BGR2HSV); sat = float(np.median(hsv[..., 1]) / 255)
    b, g, r = [s[..., k].astype(np.float64) for k in range(3)]; rg, yb = r - g, 0.5 * (r + g) - b
    col = float(np.sqrt(rg.std() ** 2 + yb.std() ** 2) + 0.3 * np.sqrt(rg.mean() ** 2 + yb.mean() ** 2))
    fe = float(np.asarray(Image.fromarray(s[..., ::-1]).convert('L').filter(ImageFilter.FIND_EDGES), np.float64)[1:-1, 1:-1].mean())
    lap = float(np.abs(cv2.Laplacian(cv2.cvtColor(s, cv2.COLOR_BGR2GRAY).astype(np.float32), cv2.CV_32F, ksize=1)).mean())
    return sat, col, fe, lap

fr = sorted(int(os.path.basename(p)[:4]) for p in glob.glob(os.path.join(DF, '[0-9][0-9][0-9][0-9].png')))
fr = [f for f in fr if os.path.exists(os.path.join(DP, f'{f:04d}_pos.exr'))]
rows = []; L = []; prev = None
for f in fr:
    cur = load(f); im, pos, bid, ai = cur; L.append(look(im))
    if prev is not None and f - prev[0] == 1 and (f % STEP == 0):
        pim, ppos = prev[1][0], prev[1][1]; Yc = Y(im); Yp = Y(pim)
        for name, m in (('ai', ai), ('toa', (bid > 0) & (bid < 9000))):
            ys, xs = np.nonzero(m)
            if len(ys) < 200: continue
            v, ok = warp(prev[0], Yp, ppos, pos[ys, xs]); dlt = np.abs(Yc[ys, xs][ok] - v[ok])
            rows.append({'f': f, 'vung': name, 'n': int(ok.sum()), 'tb': float(dlt.mean()), 'p95': float(np.percentile(dlt, 95)), 'chop': float((dlt > 12).mean())})
    prev = (f, cur)
def agg(name):
    r = [x for x in rows if x['vung'] == name]
    if not r: return None
    return {'cap': len(r), 'tb': round(float(np.mean([x['tb'] for x in r])), 3), 'p95_tb': round(float(np.mean([x['p95'] for x in r])), 2),
            'chop_pct': round(100 * float(np.mean([x['chop'] for x in r])), 3), 'cap_xau_nhat_tb': round(float(max(x['tb'] for x in r)), 3)}
# nhất quán đầu ↔ cuối (và giữa ↔ cuối)
cons = {}
for (fa, fb) in ((fr[0], fr[-1]), (fr[len(fr) // 2], fr[-1]), (fr[0], fr[len(fr) // 2])):
    a = load(fa); b = load(fb); m = b[3] if b[3].any() else (b[2] > 0) & (b[2] < 9000); ys, xs = np.nonzero(m)
    v, ok = warp(fa, a[0], a[1], b[1][ys, xs]); cb = b[0][ys, xs][ok]
    if ok.sum() < 200: cons[f'{fa}-{fb}'] = {'diem_chung': int(ok.sum())}; continue
    cons[f'{fa}-{fb}'] = {'diem_chung': int(ok.sum()), 'dY_tb': round(float(np.abs(Y(cb) - Y(v[ok])).mean()), 2), 'dRGB_tb': round(float(np.abs(cb - v[ok]).mean()), 2)}
La = np.array(L)
res = {'site': site, 'khung': DF, 'so_khung': len(fr), 'nhap_nhay': {'ai': agg('ai'), 'toa': agg('toa')}, 'nhat_quan': cons,
       'chuan_hinh_trung_vi': {'sat': round(float(np.median(La[:, 0])), 3), 'colorful': round(float(np.median(La[:, 1])), 1), 'find_edges': round(float(np.median(La[:, 2])), 2), 'laplace': round(float(np.median(La[:, 3])), 2)},
       'theo_cap': rows}
json.dump(res, open(OUT, 'w'), indent=1, ensure_ascii=False); print(json.dumps({k: v for k, v in res.items() if k != 'theo_cap'}, ensure_ascii=False))
