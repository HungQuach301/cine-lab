"""NC-GPU · số đo MÀU + SƯƠNG để so với "đích look" Omni (V2V-D2: CHỈ số đo, không chép hình). Mọi ảnh thu về 640×360 (INTER_AREA) như measure_look.py.
  sat_med, colorful, detail: như measure_look.py (vùng giữa 15–85 %)
  dark_med: trung vị "kênh tối" (min RGB, lọc min 15×15) /255 trên vùng giữa — càng cao càng nhiều sương/màn sáng (He 2009)
  rms_con: độ lệch chuẩn / trung bình độ sáng Y (tương phản toàn cục)
  sat_xa_gan: bão hoà trung vị dải trên (y 15–40 %) ÷ dải dưới (y 60–85 %) — < 1 = xa nhạt hơn gần (phối cảnh khí quyển)
  do_look.py <ảnh…> [--grid tl|tr|bl|br] [--json ra]   (--grid: lấy một phần tư của khung lưới 2×2 của NC-V2V)"""
import sys, json, cv2, numpy as np
a = sys.argv[1:]; js = a[a.index('--json') + 1] if '--json' in a else None; gr = a[a.index('--grid') + 1] if '--grid' in a else None
fs = [x for x in a if x.lower().endswith(('.png', '.jpg')) and x != js]
def m(p):
    im = cv2.imread(p)
    if gr: h, w = im.shape[:2]; y0 = 0 if gr[0] == 't' else h // 2; x0 = 0 if gr[1] == 'l' else w // 2; im = im[y0:y0 + h // 2, x0:x0 + w // 2]
    im = cv2.resize(im, (640, 360), interpolation=cv2.INTER_AREA); c = im[54:306, 96:544]
    hsv = cv2.cvtColor(c, cv2.COLOR_BGR2HSV); S = hsv[..., 1] / 255.0; b, g, r = [c[..., k].astype(float) for k in range(3)]; rg, yb = r - g, 0.5 * (r + g) - b
    Y = cv2.cvtColor(c, cv2.COLOR_BGR2GRAY).astype(np.float32); dk = cv2.erode(c.min(2), np.ones((15, 15), np.uint8)) / 255.0
    Sf = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)[..., 1] / 255.0
    return dict(sat_med=float(np.median(S)), colorful=float(np.sqrt(rg.std() ** 2 + yb.std() ** 2) + 0.3 * np.sqrt(rg.mean() ** 2 + yb.mean() ** 2)),
                detail=float(np.abs(cv2.Laplacian(Y, cv2.CV_32F, ksize=1)).mean()), dark_med=float(np.median(dk)), rms_con=float(Y.std() / max(1, Y.mean())),
                sat_xa_gan=float(np.median(Sf[54:144]) / max(1e-3, np.median(Sf[216:306]))))
rows = {p: {k: round(v, 3) for k, v in m(p).items()} for p in fs}
med = {k: round(float(np.median([r[k] for r in rows.values()])), 3) for k in next(iter(rows.values()))}
print(json.dumps(med))
if js: json.dump(dict(grid=gr, rows=rows, trung_vi=med), open(js, 'w'), indent=1, ensure_ascii=False)
