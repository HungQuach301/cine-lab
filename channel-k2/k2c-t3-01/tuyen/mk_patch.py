"""T3 · gói TUYẾN · dựng tuyen/treatment-patch.json (SM1–SM3 `type: strategic` + 4 inset B4) — KHÔNG sửa vay-ham/treatment.json.
Dùng: /opt/cine/bin/python -I channel-k2/k2c-t3-01/tuyen/mk_patch.py  → treatment-patch.json"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
W, H = 1920, 1080
INSET_W, INSET_H = 600, 340                      # 9,84 % khung (trần B4 12 %); nhắm ≤ 11 % theo NC-BD
INSET_XY = (round(W * 0.05), round(H * 0.05))   # góc TRÊN TRÁI trong vùng an toàn 5 %

SM = [
 {'op': 'insert_before', 'ref': '1a', 'shot': {
   'id': 'SM1', 'ch': 1, 'dur': 6.0, 'loai': 'bản đồ chiến lược', 'type': 'strategic', 'noi': 'luc_dia', 'vung': 'tay-au', 'goc': 'strategic-1704', 'moc_nam': '1704',
   'agl_km': 0.0, 'agl_max_km': 0.0, 'khung_rong_km': 2500, 'bbox': [-12.0, 35.0, 8.0, 52.5],
   'claims': ['T001', 'T002', 'T003', 'T004', 'T005', 'S012', 'S013'], 'vai': 'co-che',
   'tuyen': ['R1704-GIB'], 'tuyen_phu': ['R1704-LIS'], 'ranh': '1704', 'nhan_ranh': 'approx. borders c. 1704 — OpenHistoricalMap, IGN',
   'chu_giai': ['Grand Alliance (England & allies)', 'France', 'Spain (Philip V)'],
   'bo_dem': [{'t': 0.0, 'hien': 'Feb 1704'}, {'t': 2.0, 'hien': 'Jun 1704'}, {'t': 4.2, 'hien': '21 July (O.S.) / 1 Aug (N.S.) 1704'}],
   'nhip': [{'t': 0.0, 'su_kien': 'mở trên Tây Âu c. 1704, tô 3 phe + Gibraltar là điểm (màu TBN) + nhãn nguồn ranh'},
            {'t': 0.8, 'su_kien': 'R1704-LIS vẽ mờ (nét đứt mảnh, 1,0 s) — St Helens → Lisbon, bộ đếm "Feb 1704"'},
            {'t': 2.0, 'su_kien': 'R1704-GIB vẽ đậm: ngoài khơi Algarve → ngoài khơi Tetuan → vịnh; bộ đếm chạy tới "1 Aug (N.S.)"'},
            {'t': 4.4, 'su_kien': 'Gibraltar đổi điểm sang màu Đại Liên minh; nhãn phụ "taken in the name of \'Charles III\'"'},
            {'t': 5.2, 'su_kien': 'máy lặn liên tục xuống vịnh → hoà vào 1a (3D vịnh), giữ bộ đếm'}],
   'may': 'push-in chậm Tây Âu → eo biển (2 500 → ~400 km), không dừng; hoà vào 1a', 'engine': 'M13-lite', 'du_lieu_nha': '', 'hero': 'hạm đội 1704 (sticker tàu buồm theo tuyến)',
   'mo_ta': 'Ai đứng về phía nào năm 1704 và hạm đội Anh–Hà Lan đến eo biển bằng đường nào.'}},
 {'op': 'update', 'id': '1a', 'set': {'dur': 5.0}, 'ghi_chu': '1a 11 → 5 s (6 s đầu thành SM1; NC-BD §2.3, B2). Bộ đếm "21 July (O.S.) / 1 Aug (N.S.) 1704" nối từ SM1.'},
 {'op': 'insert_before', 'ref': '2f', 'shot': {
   'id': 'SM2', 'ch': 2, 'dur': 7.0, 'loai': 'bản đồ chiến lược', 'type': 'strategic', 'noi': 'bien', 'vung': 'iberia-eo-bien', 'goc': 'strategic-1780-82', 'moc_nam': '1780–82',
   'agl_km': 0.0, 'agl_max_km': 0.0, 'khung_rong_km': 1500, 'bbox': [-11.5, 34.0, 5.0, 41.5],
   'claims': ['T006', 'T007', 'T009', 'T011', 'T013', 'T014', 'T015', 'T016', 'T020', 'S054', 'S055', 'S056'], 'vai': 'co-che',
   'tuyen': ['R1780-RODNEY', 'R1781-DARBY', 'R1782-HOWE'], 'vung_ve': ['Z1779-BLOCKADE'], 'ranh': '1780–82', 'nhan_ranh': 'approx. borders c. 1782 — Cliopatria (Seshat)',
   'chu_giai': ['Britain', 'Spain', 'France'],
   'bo_dem': [{'t': 0.0, 'hien': 'Jan 1780'}, {'t': 2.6, 'hien': 'Apr 1781'}, {'t': 4.2, 'hien': '5 Feb 1782'}, {'t': 4.8, 'hien': 'Oct 1782'}],
   'nhip': [{'t': 0.0, 'su_kien': 'mở trên Iberia–eo biển c. 1780; vòng phong toả nét đứt quanh Algeciras–Cabrita–Ceuta (T006, T007)'},
            {'t': 0.6, 'su_kien': 'Rodney: mũi tên vào từ mép bắc-tây "from England" → qua mũi St Vincent → vịnh (bộ đếm Jan 1780)'},
            {'t': 2.6, 'su_kien': 'tuyến Rodney mờ còn 30 % (ba đoàn đi cùng hành lang — xem xem-truoc/SM2.png); Darby: vào từ mép bắc (St Helens/Cork ngoài khung) → Cap Spartel → vịnh (Apr 1781)'},
            {'t': 4.2, 'su_kien': 'Minorca đổi đỏ → vàng đúng lúc bộ đếm qua 5 Feb 1782 (T020); nhãn nhỏ "Minorca → Spain"'},
            {'t': 4.8, 'su_kien': 'tuyến Darby mờ còn 30 %; Howe: vào từ mép bắc → St Vincent → eo → TRÔI vào Địa Trung Hải tới ngoài khơi Fuengirola → quay lại vịnh (Oct 1782; dừng ở 18 Oct)'},
            {'t': 6.5, 'su_kien': 'hoà vào 2f (3D eo biển, chanh Malaga)'}],
   'khong_ve': {'R1780-PATROL': 'không có lời tương ứng', 'Z1780-MOONLIGHT': 'không có lời tương ứng (MÂU THUẪN vị trí, T012)', 'R1782-ALLIED': 'tới 12/9/1782 — trước cú liên hoàn 2m; đưa vào SM2 sẽ lộ cao trào',
                'Z1782-SPARTEL': '20/10/1782 — sau cao trào 13/9; không có lời'},
   'may': 'trượt chậm bắc → nam theo tuyến đang vẽ; không zoom quá 1 lần', 'engine': 'M13-lite', 'du_lieu_nha': '', 'hero': 'sticker tàu buồm theo tuyến',
   'mo_ta': 'Ba đoàn tiếp tế phá vòng phong toả: đi đường nào, khi nào; Minorca mất giữa đoàn 2 và 3.'}},
 {'op': 'update', 'id': '2f', 'set': {'dur': 4.0}, 'ghi_chu': '2f 11 → 4 s, giữ 3D eo biển cho chanh Malaga (S053).'},
 {'op': 'insert_before', 'ref': '4g', 'shot': {
   'id': 'SM3', 'ch': 4, 'dur': 7.0, 'loai': 'bản đồ chiến lược', 'type': 'strategic', 'noi': 'luc_dia', 'vung': 'tay-au-bac-phi', 'goc': 'strategic-1941', 'moc_nam': '1940–42',
   'agl_km': 0.0, 'agl_max_km': 0.0, 'khung_rong_km': 2500, 'bbox': [-17.5, 31.0, 6.0, 49.5],
   'claims': ['T021', 'T022', 'T023', 'T024', 'T026', 'S114', 'S115', 'S117', 'S118', 'S120', 'S122'], 'vai': 'he-qua',
   'tuyen': ['R1940-EV-CASA', 'R1940-EV-LON', 'R1940-EV-MAD', 'R1940-EV-JAM', 'R1942-AIR-ORAN', 'R1942-SEA-WEST', 'R1942-SEA-ORAN', 'R1942-SEA-ALG'], 'ranh': '1941',
   'nhan_ranh': 'approx. borders c. 1941 — Cliopatria (Seshat)', 'chu_giai': ['Britain & Allies', 'Spain (non-belligerent)', 'France: Vichy / German-occupied (hatched)'],
   'bo_dem': [{'t': 0.0, 'hien': 'May 1940'}, {'t': 1.0, 'hien': '12–14 Jun 1940'}, {'t': 2.2, 'hien': 'Jul–Oct 1940'}, {'t': 5.0, 'hien': '8 Nov 1942'}],
   'nhip': [{'t': 0.0, 'su_kien': 'mở c. 1941; cung sơ tán đầu tiên (kem) Gibraltar → Casablanca (22/5–24/6/1940)'},
            {'t': 1.0, 'su_kien': 'nhãn "Spain (non-belligerent)" hiện (12/6, T021); Tangier đổi gạch vàng + nhãn (14/6, T022)'},
            {'t': 2.2, 'su_kien': 'cung sơ tán London (lên mép bắc), Madeira, Jamaica (ra mép tây) — màu kem trung tính, không mũi tên quân sự'},
            {'t': 5.0, 'su_kien': 'Torch: mũi tên KHÔNG Gibraltar → Tafaraoui (đỏ, nét đứt) + ba mũi tên biển từ mép tây vào Casablanca/Oran/Alger, KHÔNG ghi nơi đi (T025 CHƯA XÁC MINH)'},
            {'t': 6.5, 'su_kien': 'hoà vào 4g (3D vịnh 1940)'}],
   'may': 'trượt nhẹ nam → bắc rồi giữ; một lần zoom ra cho cung Jamaica/London ra mép', 'engine': 'M13-lite', 'du_lieu_nha': '', 'hero': '—',
   'mo_ta': 'Sơ tán dân 1940 (trung tính) trong bối cảnh Tây Ban Nha "không tham chiến" + Tangier; hai năm sau Gibraltar là bàn đạp Torch.'}},
 {'op': 'update', 'id': '4g', 'set': {'dur': 2.0, 'claims': ['S114', 'S117', 'S118', 'S120']}, 'ghi_chu': '4g 9 → 2 s (NC-BD §2.3). 4g giữ claim sơ tán; lời SM3 chảy qua 4g.'},
]


def inset(shot, t_vao, dur, ten_khu, bbox, nhan, agl_km, note):
    return {'op': 'update', 'id': shot, 'set': {'inset': {
        'vi_tri': 'tren-trai', 'x_px': INSET_XY[0], 'y_px': INSET_XY[1], 'w_px': INSET_W, 'h_px': INSET_H, 'ty_le_khung': round(INSET_W * INSET_H / (W * H), 4),
        't_vao_s': t_vao, 'dur_s': dur, 'mo_s': 0.3, 'khu': ten_khu, 'bbox': bbox, 'lop': ['bờ biển (Natural Earth 1:10m)', 'hộp đỏ = dấu chân khung máy (lấy từ campath.json khi dựng)'],
        'nhan': nhan, 'khong_ve': ['ranh giới', 'tuyến', 'chú giải'], 'nguon_tren_hinh': 'Map: Natural Earth', 'chip_noi': 'chuyển sang góc TRÊN PHẢI khi inset hiện',
        'dau_chan_uoc_km': round(2.7 * agl_km, 2), 'ghi_chu': note}}}


INSETS = [
 inset('1d', 0.6, 3.0, 'eo biển Gibraltar ~120 km', [-6.2, 35.6, -4.8, 36.5], ['Gibraltar', 'Strait of Gibraltar'], 0.3, 'lần đầu ở phố 1704 (máy ≤ 3 km tại nơi có tên); hộp đỏ ≈ 0,8 km → ≈ 4 px ở 5 px/km: vẽ đúng tỉ lệ + vòng định vị 16 px'),
 inset('2a', 0.6, 3.0, 'eo biển Gibraltar ~120 km', [-6.2, 35.6, -4.8, 36.5], ['Gibraltar', 'Spain'], 0.8, 'chương mới, máy ≤ 3 km; hộp ≈ 2,2 km ≈ 11 px'),
 inset('3d', 0.6, 3.0, 'eo biển Gibraltar ~120 km', [-6.2, 35.6, -4.8, 36.5], ['La Línea', 'Gibraltar'], 0.11, 'chương mới; hộp ≈ 0,3 km → vòng định vị'),
 inset('5d', 0.6, 3.0, 'eo biển Gibraltar ~120 km', [-6.2, 35.6, -4.8, 36.5], ['La Línea', 'Gibraltar'], 0.15, 'chương mới; hộp ≈ 0,4 km → vòng định vị'),
]

LOI = {
 'note': 'LỜI MỚI cho SM1–SM3 — CHỜ DUYỆT Ở G1. Không viết lại lời chỗ khác. Ước đọc 2,5 từ/s (Kinh thánh §3: ~150 từ/phút); năm đọc thành chữ được tính theo số từ nói.',
 'SM1': {'cau': "England, the Dutch and Portugal backed a rival for Spain's crown; France backed Madrid's king.", 'so_tu': 15, 'uoc_s': 6.0, 'cua_so_s': 6.0,
         'claims': ['T004', 'T005'], 'ghi_chu': 'Hai phía trung tính: không gọi Philip V là "claimant"; "Madrid\'s king" đúng vị thế 1704. Phương án ngắn: "1704. Europe is at war over Spain\'s crown — and an Anglo-Dutch fleet is heading south." (16 từ, T004 + T001/T002 + S012).',
         'trang_thai': 'CHỜ G1'},
 'SM2': {'cau': 'To break the blockade, Britain sent three relief fleets: 1780, 1781, 1782.', 'so_tu': 13, 'so_tu_noi': 19, 'uoc_s': 7.6, 'cua_so_s': 11.0,
         'claims': ['T006', 'T009', 'T013', 'T015', 'S054', 'S055', 'S056'], 'tuy_chon': "Between the second and the third, Spain took back Minorca. (10 từ, T020 — chỉ dùng nếu lời 2f còn chỗ)",
         'ghi_chu': 'Ba năm đọc thành chữ ("seventeen-eighty…") ≈ 19 từ nói ≈ 7,6 s → chảy sang 0,6 s đầu 2f (cửa sổ SM2 + 2f = 11 s). Không nói số tàu (lệch giữa nguồn).', 'trang_thai': 'CHỜ G1'},
 'SM3': {'cau': "June 1940: Spain turns 'non-belligerent' and occupies Tangier. Gibraltar sends its women and children away. By 1942, it launches an invasion.", 'so_tu': 21, 'so_tu_noi': 23, 'uoc_s': 9.2, 'cua_so_s': 9.0,
         'claims': ['T021', 'T022', 'S114', 'T023', 'T024', 'S122'], 'ghi_chu': '"women and children" theo S114 ("women, children, the elderly and the infirm"); "it launches an invasion" = Gibraltar là chỉ huy sở + sân bay Torch (T024, S122) — KHÔNG nói đoàn tàu xuất phát từ Gibraltar (T025). Ước 9,2 s so cửa sổ 9,0 s (SM3 + 4g) = +2,2 % (trong ±5 %). Nếu bản giọng dài hơn 9,0 s: tăng SM3 lên 8 s (trần B3) và 4g còn 1 s — không cắt chữ (mỗi cụm đều gắn claim và gắn hình).',
         'trang_thai': 'CHỜ G1'},
}


def main():
    doc = {'note': 'Bản vá bảng shot T3 (gói TUYẾN 17/10/2026; B2–B4 chủ dự án duyệt 17/10). Áp lên BẢN SAO vay-ham/treatment.json bằng ap_patch.py; KHÔNG sửa bản gốc. op: insert_before (chèn shot mới trước ref) · update (đặt trường).',
           'loai_moi': {'bản đồ chiến lược': {'type': 'strategic', 'luat_de_xuat_B3': '≤ 15 % thời lượng; ≤ 8 s/lần; ≤ 2 lần/chương; không hai shot strategic liền nhau; KHÔNG tính vào NC-H2; bắt buộc chuyển động + nhãn nguồn ranh + bộ đếm'}},
           'ops': SM + INSETS, 'loi': LOI,
           'inset_B4': {'vi_tri': 'TRÊN TRÁI (chip nơi chuyển TRÊN PHẢI)', 'khung_px': [INSET_W, INSET_H], 'ty_le_khung': round(INSET_W * INSET_H / (W * H), 4), 'tran': 0.12, 'dur_s': '2,5–4 (đặt 3,0)', 'mo_s': 0.3,
                        'bo_bien': 'Natural Earth 1:10m — đo quanh Gibraltar: đỉnh cách nhau TB 2,7 km → ở khu 120 km (5 px/km) ≈ 13 px/đoạn; ở khu ≤ 30 km sẽ lộ gãy khúc (> 50 px/đoạn) → KHÔNG dùng khu nhỏ hơn ~100 km với NE',
                        'phuong_an_du_phong': 'khu 20–30 km với bờ biển OSM (ODbL) + nhãn "Map: © OpenStreetMap contributors" — cần chủ dự án duyệt đổi nhãn (B4 ghi "Map: Natural Earth")'}}
    (HERE / 'treatment-patch.json').write_text(json.dumps(doc, ensure_ascii=False, indent=1) + '\n')
    print(len(doc['ops']), 'ops; inset tỉ lệ khung', doc['inset_B4']['ty_le_khung'])


if __name__ == '__main__':
    main()
