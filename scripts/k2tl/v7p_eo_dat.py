#!/opt/cine/bin/python
"""V7-PILOT · NỘI DUNG EO ĐẤT CÓ NGUỒN 1730–1783 (+ mốc vây hãm 1309–1783, cờ, hàng rào 1909) cho bộ máy timelapse (design/k2v/tl/tl7.js, scenes/t3tl.js).
Ra: design/k2v/tl/data/eo-dat-v7.json — mỗi vật: hình học ENU (m, gốc gói gib), cửa sổ năm {on, full, off0, off1}, nguồn + bậc (Kinh thánh §12.2) + sai số.
· TRẠI VÂY HÃM 1779–83: số hoá tay các dãy trại (dải vàng = trại TBN, dải lam = trại Pháp) trên bản Faden 1783 (Yale 2046612, PD; ảnh xem trước 1600 px trong
  vay-ham/ref, SHA ref b927ec6d…) → điểm ảnh gốc (× 10313/1600) → phép ĐỒNG DẠNG 3 điểm khống chế của phiên SH (ghost/gcp-1782-faden-doi-chieu.json, RMS 12,5 m trong vùng
  khống chế) → UTM 30N → ENU. Ngoài vùng khống chế (trại cách 2–4 km) sai số ước ≤ 250 m (đối chiếu: Point Mala lệch ≈ 250 m so bờ DEM). Đối chiếu độc lập: Drinkwater 1786
  'A Chart of the Bay of Gibraltar' (IA leaf 87): "CAMP of the ALLIES" / "E The Old Camp" cùng vị trí (giữa Point Mala và đồi Buena Vista).
· Số lều: dải trại sâu ≈ 100 m (bề rộng dải vàng trên Faden ≈ 10 px xem trước ≈ 120 m) → 14 hàng lều cách 7 m, lều cách 8 m dọc hàng ≈ 7 500 lều đủ trại 1782 (≈ 40 000 quân, S065, ≈ 5–6 người/lều — bậc 5);
  10/1779 (≈ 14 000 quân, S048) → 35 % số lều.
· Ngày: lập trại sau khi chiến tranh bắt đầu (6/7/1779, S041), đủ 10/1779 (S048); quân Pháp tới 1782 (S049 Crillon 7/1782; S065); rút sau hoà ước sơ bộ 2/1783 (S045–S047) — ngày
  đầu/cuối là ƯỚC TÍNH trong khoảng nguồn cho (ghi 'uoc').
· CÔNG SỰ TIỀN PHƯƠNG (lines1782_tp / fort1782_tp của gói — ghost SH, do_tin thấp, sai số ≥ 160 m): đang đào 12/9/1779 (S043: đồn trú bắn vào công sự TBN lần đầu) → đủ khi
  pháo TBN khai hoả 12/4/1781 (S062, 114 khẩu) — nội suy ước tính; rút 2–3/1783.
· LÍNEA DE CONTRAVALACIÓN: ghost SH (Drinkwater 1786, do_tin cao); 1730 → 1735 (TIEN-KY T3); phá huỷ 14/2/1810 (lời ch.3; G1b 3b).
· 14 CUỘC VÂY (claims-vay-ham.json 'dem_so_lan_vay', Sayer 1862 …): năm giữa mỗi cuộc → nhịp khói trên lâu đài/phố khi bộ đếm đi qua (vị trí khói: MINH HOẠ trong phố/lâu đài).
· CỜ: Cruz de Borgoña (cờ quân TBN 1506–1843) → Union (mẫu 1606/1707) từ 4/8/1704 (lời ch.1) — props.js; trước 1506 KHÔNG có cờ (chưa có nguồn mẫu cờ).
· HÀNG RÀO 1909 (lời ch.3): dựng theo ranh giới OSM 2026 (lines.json 'border') — vị trí 1909 coi như trùng ranh hiện nay (ước tính, chưa có bản đồ 1909 trong repo).
Dùng: /opt/cine/bin/python -I scripts/k2tl/v7p_eo_dat.py"""
import json, sys
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts/k2tl'))
import geo  # noqa: E402

G = json.loads((ROOT / 'channel-k2/k2c-t3-01/ghost/gcp-1782-faden-doi-chieu.json').read_text())
S = 10313 / 1600   # xem trước 1600 px → điểm ảnh gốc 10313 × 6960
OE, ON = geo.utm(-5.3487, 36.1513)
P = np.array([g['px'] for g in G['gcp']], float); U = np.array([[g['utm'][0] - OE, g['utm'][1] - ON] for g in G['gcp']], float)
pz = P[:, 0] - 1j * P[:, 1]; uz = U[:, 0] + 1j * U[:, 1]
A = np.vstack([pz, np.ones(len(P))]).T; (a, b), *_ = np.linalg.lstsq(A, uz, rcond=None)
RMS = float(np.sqrt(np.mean(np.abs(A @ [a, b] - uz) ** 2)))
def enu(x, y): z = a * (x * S - 1j * y * S) + b; return [round(z.real, 1), round(z.imag, 1)]

# dãy trại trên Faden 1783 (điểm ảnh bản xem trước 1600 px, đọc trên lưới 10 px phóng ×5): dải vàng = trại TBN, dải lam = trại Pháp
CAMP_PX = {
    'E1': [(1180, 672), (1263, 697)], 'E2': [(1163, 690), (1263, 720)], 'E3': [(1226, 637), (1262, 649)], 'E4': [(1271, 675), (1285, 667)],
    'E5': [(1238, 739), (1297, 748)], 'E6': [(1209, 756), (1245, 754)], 'E7': [(1208, 769), (1238, 766)], 'FR1': [(1311, 752), (1311, 790)]}
W_ES = dict(on=1779.53, full=1779.80, off0=1783.17, off1=1783.30)   # 13/7/1779 → 10/1779; rút 3/1783 (ước tính trong khoảng nguồn)
W_ES2 = dict(on=1782.40, full=1782.70, off0=1783.17, off1=1783.30)  # phần lều thêm 1782 (≈ 40 000 quân, S065)
W_FR = dict(on=1782.45, full=1782.62, off0=1783.17, off1=1783.30)

def main():
    camps = []
    for k, px in CAMP_PX.items():
        fr = k.startswith('FR'); pts = [enu(*p) for p in px]
        camps.append(dict(id=f'TRAI-{k}', pts=pts, rows=14, gap=8.0, rowGap=7.0, color='#f3efe4' if not fr else '#ecebe6', side='fr' if fr else 'es',
                          w=W_FR if fr else W_ES, w2=None if fr else W_ES2, frac=1.0 if fr else 0.35,
                          nguon='Faden 1783 (Yale 2046612, PD) — dải trại; đối chiếu Drinkwater 1786 Chart of the Bay ("CAMP of the ALLIES", "E The Old Camp")',
                          bac='vị trí: bậc 1 (sai số ước ≤ 250 m ngoài vùng khống chế); số lều: bậc 2 (S048 ≈ 14 000 quân 10/1779; S065 ≈ 40 000 9/1782) + bậc 5 (≈ 6 người/lều); hình lều: bậc 4 (bản khắc thời đó); ngày: bậc 2 + ước tính',
                          px_xem_truoc=px))
    sieges = []
    cl = json.loads((ROOT / 'channel-k2/k2c-t3-01/vay-ham/claims-vay-ham.json').read_text())
    ds = cl['dem_so_lan_vay']['cac_cach_dem'][0]['danh_sach'] if isinstance(cl, dict) else None
    import re
    for i, s in enumerate(ds):
        ys = [int(x) for x in re.findall(r'\d{4}', s)][:2]; y0 = ys[0]; y1 = ys[1] if len(ys) > 1 else y0
        mid = (y0 + y1) / 2 + (0.15 if '(Feb' in s else 0.55 if '(Jun' in s else 0.5)
        sieges.append(dict(stt=i + 1, nhan=s, nam=round(mid, 2)))
    out = dict(
        tao_boi='scripts/k2tl/v7p_eo_dat.py', phep_dong_dang=dict(m_px_goc=round(abs(a), 4), rms_m_vung_khong_che=round(RMS, 1), gcp='ghost/gcp-1782-faden-doi-chieu.json', sai_so_ngoai_vung_m=250),
        trai=camps,
        cong_su_tien_phuong=dict(lop=['lines1782_tp', 'fort1782_tp'], w=dict(on=1779.70, full=1781.278, off0=1783.15, off1=1783.40), nguon='ghost SH (Drinkwater 1786 Plan of the Batteries; đối chiếu Faden 1783 lệch 99–157 m)',
                                 bac='vị trí: bậc 1 do_tin thấp (sai số ≥ 160 m); ngày: S043 (12/9/1779 đang đào) → S062 (12/4/1781 khai hoả) nội suy — ước tính'),
        linea=dict(w=dict(on=1730.0, full=1735.0, off0=1810.12, off1=1810.13), nguon='ghost SH lines1782 chien_tuyen T1782-01 (Drinkwater 1786, do_tin cao)', bac='vị trí: bậc 1; ngày xây 1730–35: TIEN-KY T3; phá 14/2/1810: lời ch.3 + G1b 3b'),
        hang_rao_1909=dict(w=dict(on=1909.0, full=1909.6, off0=None, off1=None), nguon='ranh OSM 2026 (lines.json border)', bac='vị trí: ước tính (coi ranh 1909 trùng ranh hiện nay; chưa có bản đồ 1909); ngày: lời ch.3 (1908 báo, 1909 dựng)'),
        vay_ham=dict(danh_sach=sieges, nguon='claims-vay-ham.json dem_so_lan_vay (Sayer 1862; Stephens 1870; GNM; García Sanz 2022)', vi_tri_khoi='minh hoạ (lâu đài Moor + phố) — chỉ đánh dấu THỜI ĐIỂM'),
        co=dict(burgundy=dict(on=1506.0, off=1704.59), union=dict(on=1704.59), cot='Tower of Homage (heroes.json tower) — cột cờ minh hoạ', nguon='props.js (RIGHTS-V6: Cruz de Borgoña 1506–1843; Union 1606/1707)'),
    )
    p = ROOT / 'design/k2v/tl/data/eo-dat-v7.json'; p.write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n')
    n = sum(1 for _ in camps); print(f'{p} · {n} dãy trại · RMS {RMS:.1f} m · {len(sieges)} cuộc vây')
    for c in camps: print(c['id'], c['pts'])

if __name__ == '__main__': main()
