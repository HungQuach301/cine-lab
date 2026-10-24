#!/opt/cine/bin/python
"""THU-B-T4 · (việc 5) ƯỚC TÁC ĐỘNG CẢ TẬP theo BANG-SHOT-v1 (animatic T4 chưa đẩy bảng v2 — kiểm git ls-remote lúc chạy).
  uoc_thub.py → reports/thu-b-t4/do/uoc-tac-dong.json + bảng markdown in ra
Số đo % nhà ĐO ĐƯỢC theo điểm máy: $THUB/bp/<khung>/prep.json (cùng định nghĩa K-1.17.5) — uoc-P1/P3/P5/P6/P8 (1666; P1, P5 thêm 2026), M1-trung (P2 1666, fov 50),
B3-p4-1938 (P4 1938), M4-trung (P4b 2026, 19 m). P7 (thiên đỉnh 2200 m, fov 40°): px/m ≤ 0,7 < 2 → 0 nhà đo được (tính hình học, không dựng).
Luật áp B cho một shot (đặt trước khi đếm): (1) shot dựng 3D lớp A (không MD/MAP/TL/PP/B-Cycles); (2) ban ngày suốt shot (không đêm/chạng vạng); (3) không trong thời gian cháy
1666 (2/9–7/9) hay đêm bom 29–30/12/1940 (nhà đang cháy/sập — lớp (a) lửa theo ngày); (4) không có nhà mọc/mất trong shot (tua năm qua xây lại/đổi khối) — ảnh AI tĩnh hay chiếu
đều không theo được hình học đổi; shot KHOP hai mốc tính mỗi mốc nửa thời lượng."""
import importlib.util, json, os
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
THUB = os.environ.get('THUB', '/var/tmp/ldn/thub')
spec = importlib.util.spec_from_file_location('bang_shot', os.path.join(REPO, 'scripts/k2ldn/bang_shot.py')); BS = importlib.util.module_from_spec(spec); spec.loader.exec_module(BS)
DO = {}
for k in ('uoc-P1-1666', 'uoc-P1-2026', 'uoc-P3-1666', 'uoc-P5-1666', 'uoc-P5-2026', 'uoc-P6-1666', 'uoc-P8-1666', 'M1-trung', 'B3-p4-1938', 'M4-trung'):
    p = f'{THUB}/bp/{k}/prep.json'
    if os.path.exists(p): DO[k] = json.load(open(p))
CAM = {('P1', '1666'): 'uoc-P1-1666', ('P1', '2026'): 'uoc-P1-2026', ('P2', '1666'): 'M1-trung', ('P3', '1666'): 'uoc-P3-1666', ('P5', '1666'): 'uoc-P5-1666',
       ('P5', '2026'): 'uoc-P5-2026', ('P6', '1666'): 'uoc-P6-1666', ('P8', '1666'): 'uoc-P8-1666', ('P4', '1666'): 'B3-p4-1938', ('P4', '2026'): 'M4-trung'}
# phân loại từng shot (đặt TRƯỚC khi đếm, theo cột "Mốc" của BANG-SHOT-v1) — lý do ghi kèm
DEM = {'M01': 'đêm (14:00 → 21:30: nửa sau tối)', 'M03': 'đêm lửa', 'M04': 'đêm', 'H1-02': 'đêm → bình minh, cháy', 'H1-04': 'đang cháy', 'H1-06': 'đang cháy', 'H1-07': 'đang cháy',
       'H1-08': 'đêm, cháy', 'H1-11': 'cháy', 'H1-13': 'đêm cháy', 'H1-15': 'đêm cháy', 'H1-16': 'đêm → tàn lửa', 'H1-18': 'phế tích bốc khói', 'H2-01': 'phế tích (nhà mất)',
       'H4-01': 'chạng vạng 15:30 → 18:15', 'H4-02': 'đêm bom', 'H4-03': 'đêm bom', 'H4-04': 'đêm bom', 'H4-06': 'phế tích 1940 → 1941', 'H4-05': '30/12/1940 07:00 trước bình minh (mặt trời mọc ≈ 08:06), khói sau bom', 'H5-07': 'đêm', 'H5-08': 'đêm'}
DOI = {'M02': '2026 → 1666 tua ngược (nhà mất/mọc)', 'H2-02': 'phương án Wren chồng (TL)', 'H2-03': '1667 lô rối (phế tích + dựng lại)', 'H2-04': '1667–1668 xây lại (nhà mọc)',
       'H2-05': '1668 → 1671 xây lại', 'H2-06': '1671 → 1677 Monument mọc (nhà quanh ổn định?) — tính không áp', 'H2-08': '1670 → 1700 chóp Wren mọc', 'H2-09': '1675 → 1708 St Paul\'s mọc',
       'H2-14': '1700 → 1711', 'H3-01': '1711 → 1860 (Victoria thay nhà)', 'H3-02': '1757 → 1832 nhà trên cầu dỡ', 'H3-03': '1860 → 1871 Embankment', 'H3-04': '1900 → 1937 toà văn phòng chen',
       'H4-07': '1941 vùng bom', 'H5-01': '1946 → 1951 quy hoạch lại', 'H5-02': '1957 → 1976 Barbican mọc', 'H5-04': '1980 → 2026 toà cao mọc', 'H1-03': '1647 → 1666 (giả định nhà ổn định — TÍNH áp)'}


def era(moc):
    for y in ('2026', '1940', '1938', '1937', '1711', '1710', '1700', '1680', '1666', '1667', '1647'):
        if y in moc: return '2026' if y == '2026' else '1666'
    return '1666'


def main():
    rows = []; tong = 0; ap_s = 0.0; dt_s = 0.0
    for (ma, phan, giay, loi, dm, loai, moc, vai, lop, gc) in BS.S:
        a3 = float(lop.get('A', 0)); tong += giay
        ly = None
        if loai in ('MD', 'PP') or dm == '—' or a3 <= 0: ly = 'không phải shot 3D lớp A'
        elif ma in DEM: ly = 'đêm/cháy: ' + DEM[ma]
        elif ma in DOI and 'TÍNH áp' not in DOI[ma]: ly = 'nhà đổi trong shot: ' + DOI[ma]
        elif dm == 'P7': ly = 'P7 thiên đỉnh 2 200 m: px/m ≤ 0,7 → 0 nhà đo được'
        k = CAM.get((dm, era(moc))) or CAM.get((dm, '1666'))
        d = DO.get(k) if k else None
        s_ap = a3 if ly is None else 0.0
        pa = (d['pct_dien_tich_nha_do_duoc'] if d else None); pn = (d['pct_nha_do_duoc'] if d else None); pk = (d['px_nha_do_duoc_pct'] if d else None)
        if ly is None and d is None: ly = f'chưa đo điểm máy {dm}'; s_ap = 0.0
        ap_s += s_ap; dt_s += s_ap * (pk or 0) / 100.0
        rows.append(dict(shot=ma, giay=giay, giay_A=a3, diem_may=dm, moc=moc, ap_B=ly is None, ly_do=ly or 'áp được', so_do=k, pct_nha_do_duoc=pn, pct_dien_tich_nha_do_duoc=pa, pct_khung_nha_do_duoc=pk))
    out = dict(bang='BANG-SHOT-v1 (không có v2 trên remote lúc chạy)', tong_s=tong, giay_shot_ap_B=round(ap_s, 1), pct_thoi_luong=round(100 * ap_s / tong, 1),
               giay_x_dien_tich_khung=round(dt_s, 1), so_shot_ap=sum(1 for r in rows if r['ap_B']), so_shot=len(rows), so_do=DO, hang=rows)
    os.makedirs(os.path.join(REPO, 'reports/thu-b-t4/do'), exist_ok=True); json.dump(out, open(os.path.join(REPO, 'reports/thu-b-t4/do/uoc-tac-dong.json'), 'w'), ensure_ascii=False, indent=1)
    print(f"| Shot | s | Điểm máy | Mốc | Áp B? | % nhà đo được (số · diện tích nhà · khung) |\n|---|---|---|---|---|---|")
    for r in rows:
        if r['ap_B'] or r['diem_may'] not in ('—',):
            print(f"| {r['shot']} | {r['giay']} | {r['diem_may']} | {r['moc']} | {'CÓ' if r['ap_B'] else 'không — ' + r['ly_do']} | " + (f"{r['pct_nha_do_duoc']} · {r['pct_dien_tich_nha_do_duoc']} · {r['pct_khung_nha_do_duoc']}" if r['pct_nha_do_duoc'] is not None else '—') + ' |')
    print(json.dumps({k: out[k] for k in ('tong_s', 'giay_shot_ap_B', 'pct_thoi_luong', 'giay_x_dien_tich_khung', 'so_shot_ap', 'so_shot')}, ensure_ascii=False))


if __name__ == '__main__': main()
