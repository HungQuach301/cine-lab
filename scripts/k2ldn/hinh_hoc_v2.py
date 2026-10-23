#!/opt/cine/bin/python
"""LOOK-T4-V2 · hình học London v3 = hình học look v2 (hinh_hoc_look.py, từng tam giác giữ nguyên) + CÔNG TRÌNH BIỂU TƯỢNG chi tiết cao (cong_trinh_v2.py)
+ vật liệu riêng cho hai toà có tên dễ nhận (30 St Mary Axe: lưới kim cương xoắn — mt 15; The Leadenhall Building: khung giằng chéo lộ — mt 16).
  hinh_hoc_v2.py   → $LDN_DATA/look2/ldn2.bin + ldn2.json (+ cls66/cls26, cay, thuyen, khoi_bep, luoi_chay, luoi_1940 — giống look v2)
Bộ sinh ngẫu nhiên chung (RNG) của thành phố KHÔNG lệch: hàm công trình cũ vẫn được gọi trên một lưới bỏ đi để tiêu thụ đúng chuỗi số như v2."""
import os, sys, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hinh_hoc_look as HL
import cong_trinh_v2 as V2

HL.OUT = os.path.join(HL.H0.DATA, 'look2'); os.makedirs(HL.OUT, exist_ok=True)
_orig = {k: getattr(HL, k) for k in ('st_pauls_wren', 'monument', 'tower_of_london')}
def _wrap(k):
    def f(m):
        _orig[k](HL.M())            # tiêu thụ RNG như v2 (lưới bỏ đi)
        return getattr(V2, k)(m)
    return f
for k in _orig: setattr(HL, k, _wrap(k))

_arr = HL.M.arr
def arr2(s):
    P, C, T, K, UV, MT, FL = _arr(s)
    E = P[:, 0] + HL.E0; N = -P[:, 2] + HL.N0
    g = (K == 4) & (np.hypot(E - 533301, N - 181252) < 30) & (P[:, 1] > 20); MT[g & (MT == 7)] = 15     # 30 St Mary Axe
    l = (K == 4) & (np.hypot(E - 533166, N - 181190) < 40) & (P[:, 1] > 40); MT[l & (MT == 7)] = 16     # The Leadenhall Building
    print(json.dumps({'mt15_dinh': int((MT == 15).sum()), 'mt16_dinh': int((MT == 16).sum())}))
    return P, C, T, K, UV, MT, FL
HL.M.arr = arr2
_main_meta = HL.json.dump
if __name__ == '__main__':
    HL.main()
    J = os.path.join(HL.OUT, 'ldn2.json'); meta = json.load(open(J)); meta['phien_ban'] = 'look-v2 + cong-trinh-v2 (LOOK-T4-V2)'
    meta['bac']['wren'] = '3 (Gilbertson qua Gutenberg #48491: 515/250/180/112/102/221/365 ft) + 4–5 (tầng trống, gác, đèn lồng, tháp tây)'
    meta['bac']['monument'] = '1 vị trí (OSM r3374550) + 3 (London and Its Environs 1761, Gutenberg #60008: 15/120/40/42/32 ft; bệ 21,5 ft Strype qua lookup.london)'
    meta['bac']['white_tower'] = '1 vị trí/hướng (OSM w369135772) + 3 (Wikipedia: 36 × 32 m, 27 m, tháp góc) + 4 (mũ chì, Hollar)'
    json.dump(meta, open(J, 'w'), ensure_ascii=False, indent=1)
