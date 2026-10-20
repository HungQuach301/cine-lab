#!/opt/cine/bin/python -I
"""NC-V2V3 · (iii) ĐƯỜNG NỐI chế độ C: ở mỗi biên cửa sổ b (khung đầu phần MỚI của cửa sổ k ≥ 1), ΔE76 TB (640×360, Lab) khung b−1 ↔ b,
so với nền = trung vị ΔE khung kề TRONG cửa sổ (không gồm biên) và ΔE nguồn cùng chỗ; tỉ số > 3 → nối thấy được (cùng quy ước noi.py NC-V2V).
Thêm: bước nhảy chi tiết |Laplace| và bão hoà tại biên; độ trôi màu giữa khung 0 và khung 480 (ΔE TB ra so với ΔE nguồn).
  noi3.py <thư mục khung ra final/> <thư mục khung nguồn rgb/> <ra.json>"""
import json, sys, os
import cv2, numpy as np
STARTS, N = [0, 72, 144, 216, 288, 360, 400], 81
B = [STARTS[k - 1] + N for k in range(1, len(STARTS))]   # khung đầu phần mới: 81, 153, 225, 297, 369, 441
rd = lambda p: cv2.resize(cv2.imread(p), (640, 360), interpolation=cv2.INTER_AREA)
def lab(b):
    x = cv2.cvtColor(b, cv2.COLOR_BGR2LAB).astype(np.float32); x[..., 0] *= 100 / 255; x[..., 1:] -= 128; return x
dE = lambda a, b: float(np.sqrt(((lab(a) - lab(b)) ** 2).sum(-1)).mean())
det = lambda b: float(np.abs(cv2.Laplacian(cv2.cvtColor(b, cv2.COLOR_BGR2GRAY).astype(np.float32), cv2.CV_32F, ksize=1)).mean())
sat = lambda b: float(np.median(cv2.cvtColor(b, cv2.COLOR_BGR2HSV)[..., 1]) / 255)
O = [rd(os.path.join(sys.argv[1], f'{i:05d}.png')) for i in range(481)]; S = [rd(os.path.join(sys.argv[2], f'{i:05d}.jpg')) for i in range(481)]
adj_o = [dE(O[i - 1], O[i]) for i in range(1, 481)]; adj_s = [dE(S[i - 1], S[i]) for i in range(1, 481)]
inner = [adj_o[i - 1] for i in range(1, 481) if i not in B]; base = float(np.median(inner))
rows = [dict(khung=b, giay=round(b / 24, 2), dE_noi=round(adj_o[b - 1], 3), dE_nguon=round(adj_s[b - 1], 3), ti_so_nen=round(adj_o[b - 1] / base, 2), chi_tiet_sau_truoc=round(det(O[b]) / det(O[b - 1]), 3), bao_hoa=(round(sat(O[b - 1]), 3), round(sat(O[b]), 3))) for b in B]
R = dict(bien=rows, nen_trung_vi=round(base, 3), nen_p95=round(float(np.percentile(inner, 95)), 3), nguon_trung_vi=round(float(np.median(adj_s)), 3), ti_so_max=max(r['ti_so_nen'] for r in rows),
         troi_mau_0_480=dict(ra=round(dE(O[0], O[480]), 2), nguon=round(dE(S[0], S[480]), 2)), noi_thay_duoc=sum(r['ti_so_nen'] > 3 for r in rows))
json.dump(R, open(sys.argv[3], 'w'), ensure_ascii=False, indent=1); print(json.dumps(R, ensure_ascii=False))
