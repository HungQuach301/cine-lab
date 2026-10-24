#!/opt/cine/bin/python
"""ANIMATIC-T4 · BẢNG SHOT v2 — sinh channel-k2/k2c-t4-02/BANG-SHOT-v2.{json,md} (bản nâng của bang_shot.py; v1 giữ nguyên).
Căn cứ: PHIẾU GIỌNG 24/10/2026 "Duyệt G-1, G-2, G-3 theo khuyến nghị" → G-1 = (c) K1-C1 (730,083 s; độ dài nhóm lời theo scripts/k2ldn/anim/k1c1.py);
GIAN-SHOT §6 (đổi H1-11 ↔ H1-12; gán lại cột lời theo khoa-loi/doan-shot.json; M-d > 8 s tách; thẻ Pepys → H1-05; thẻ Hooke → H2-02; H3-02 năm 1758; tách H5-05);
Q1 (minh hoạ Omni 20–23 % thời lượng), V1/V7 (tấm nền chỉ 2026 ban ngày, 5–15 %), V5 (P1 fov 36°), L3, L4, §19 (a)(b)(c), §15 (d)(f), K1174 §5 (trường log shot).
Mỗi shot thuộc một NHÓM LỜI = shot v1 mang đoạn lời (cột `nhom`); lời của nhóm đặt tại đầu nhóm + 0,2 s; ranh hình trong nhóm/giữa hai nhóm kề có thể lệch (ghi `chuyen_s`).
Lớp: A cách A · N2P tấm nền N2+ · MD minh hoạ M-d (Omni) · MAP bản đồ cổ · MAP3D 3D kiểu bản đồ · KHAC tranh khắc · THE thẻ nhân vật/bộ đếm · TL tư liệu · PP thẻ phương pháp.
Máy (tham số dựng): `may` — dùng bởi scripts/k2ldn/anim/may_v2.py (tệp máy channel-k2/k2c-t4-02/animatic/may/<ma>.json)."""
import json, os, sys, collections
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'anim'))
import k1c1  # noqa: E402
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOME = [532118, 181150, 111]
# điểm máy (EPSG:27700; h = m trên ODN). P1 đọc lại đúng CHON-V2.json + V5 fov 36° (§19 a luật 3). P2/P3/P9 nâng ≥ 120 m (GOC-CAO-60, V7B-D1); P4b gần đồi Ludgate cho THAP.
DM = {
 'P1': {'ten': 'BANKSIDE-CAO (xương sống; CHON-V2 + V5 fov 36°)', 'p': [532330, 180250, 230], 'l': [532420, 180980, 15], 'fov': 36},
 'P2': {'ten': "ST-SAVIOUR (trên tháp Southwark Cathedral, hướng Hollar 1647)", 'p': [532690, 180290, 125], 'l': [532420, 180800, 15], 'fov': 50},
 'P3': {'ten': 'TRÊN MONUMENT nhìn tây (125 m)', 'p': [532990, 180750, 125], 'l': [532150, 181120, 40], 'fov': 50},
 'P4': {'ten': 'FLEET-STREET (trục nhìn đông lên mái vòm, 40 m)', 'p': [531300, 181160, 40], 'l': [532118, 181150, 118], 'fov': 35},
 'P4b': {'ten': 'LUDGATE HILL gần (THAP, 32 m)', 'p': [531640, 181150, 40], 'l': [532050, 181140, 82], 'fov': 42},
 'P5': {'ten': 'CRIPPLEGATE-CAO (bắc nhìn nam ra sông)', 'p': [532300, 181900, 260], 'l': [532350, 180800, 0], 'fov': 50},
 'P6': {'ten': 'SÔNG-CẦU (giữa sông phía đông cầu London, 35 m, nhìn tây)', 'p': [533250, 180480, 35], 'l': [532300, 180850, 30], 'fov': 45},
 'P7': {'ten': 'THIÊN-ĐỈNH (nhìn thẳng xuống City)', 'p': [532350, 180950, 2200], 'l': [532350, 180951, 0], 'fov': 40},
 'P8': {'ten': 'TOWER-HILL (đông nhìn tây dọc Tower Street)', 'p': [533800, 180600, 120], 'l': [532900, 180800, 10], 'fov': 50},
 'P9': {'ten': 'BANKSIDE gần Cầu Millennium (bờ nam, 130 m) nhìn mái vòm — tầm nhìn LVMF', 'p': [532080, 180380, 130], 'l': DOME, 'fov': 32},
}
# (mã, phần, nhóm lời v1, giây, điểm máy, cú máy, thời gian, vai truyện, lớp {loại: giây}, thêm)
# thời gian: ('d', [Y,M,D,h], [Y,M,D,h], tz) ngày giờ · ('h66', h0, h1) giờ kể từ 2/9/1666 00:00 (Julius) · ('y', y0, y1, [M, D, h], tz) năm chạy, giờ trong ngày cố định
#            · ('h40', h0, h1) giờ kể từ 29/12/1940 18:00 (GMT) · ('khop', <tg A>, <tg B>, giây cắt) · None (MD/PP/MAP)
S = [
 ('M01', 'MÓC', 'M01', 17.875, 'P1', 'CODINH', ('d', [2026, 9, 2, 14.0], [2026, 9, 2, 21.5], 1), 'nhận ra nơi chốn: ngày → đêm từ giây 0 (TL-5, §14.7); mái vòm giữa toà cao', {'A': 17.875, 'N2P': 11.0}, {'tam_nen': [0, 11.0], 'gio': [[0, 14.0], [11.0, 14.83], [17.875, 21.5]], 'tieu_diem_en': DOME}),
 ('M02', 'MÓC', 'M02', 10.083, 'P1', 'KEO', ('y', 2026.67, 1666.66, [9, 2, 15.0], 0), 'luận đề: tua ngược — toà cao lún, mái vòm tan, Old St Paul\'s hiện lại', {'A': 10.083}, {'lo_ra': "Old St Paul's + City gỗ 1666 trên cùng lưới phố", 'tieu_diem_en': DOME}),
 ('M03', 'MÓC', 'M03', 11.0, 'P1', 'DAY', ('h66', 21.0, 22.5), 'KHOẢNH KHẮC GIÁ TRỊ NHẤT ≤ 30 s: "one entire arch of fire" từ chỗ Pepys đứng', {'A': 11.0}, {'tieu_diem_en': [532700, 180900, 20]}),
 ('M04', 'MÓC', 'M04', 12.0, 'P1', 'LAN', ('h66', 0.80, 1.15), 'cú lặn từ Bankside xuống Pudding Lane trước lửa — "a bakery about a kilometre from here"', {'A': 12.0}, {'lan': {'cuoi_p': [532880, 180690, 26], 'cuoi_l': [532905, 180810, 6]}, 'tieu_diem_en': [532905, 180810, 6]}),
 ('H1-01a', 'HỒI 1', 'H1-01', 6.0, '—', 'MD', None, 'M-d (1) Pudding Lane 01:00 — lò bánh bén lửa, tàn lửa', {'MD': 6.0, 'THE': 3}, {'md': 1, 'the': ['Thomas Farriner (thợ làm bánh nhà vua)']}),
 ('H1-01b', 'HỒI 1', 'H1-01', 5.875, '—', 'MD', None, 'M-d (1) tàn lửa bay lên con hẻm gỗ; hàng xóm thức dậy cầm đèn', {'MD': 5.875}, {'md': 1}),
 ('H1-02', 'HỒI 1', 'H1-02', 8.0, '—', 'MD', None, 'M-d (1) hẻm nhà khung gỗ tầng nhô gần chạm nhau, lửa liếm mái hiên', {'MD': 8.0}, {'md': 1, 'chuyen_s': -0.917}),
 ('H1-03', 'HỒI 1', 'H1-03', 16.792, 'P2', 'TRUOT', ('y', 1647.0, 1647.0, [9, 1, 15.0], 0), 'Hollar vẽ London từ tháp St Saviour\'s (1647): tranh khắc góc khung ≤ 1/3 rồi tan', {'A': 16.792, 'KHAC': 6}, {'khac': 'met-360649-0', 'tieu_diem_en': [532786, 180554, 10], 'chuyen_s': 0.917}),
 ('H1-04', 'HỒI 1', 'H1-04', 10.583, 'P2', 'CODINH', ('h66', 7.0, 12.0), 'St Magnus + Fish Street cháy; gió đông (khói sang tây)', {'A': 10.583}, {'tieu_diem_en': [532800, 180700, 10]}),
 ('H1-05a', 'HỒI 1', 'H1-05', 5.5, '—', 'MD', None, 'M-d (2) bậc lên xuống bờ sông gần cầu sáng 2/9: ném đồ xuống sà lan', {'MD': 5.5, 'THE': 3}, {'md': 2, 'the': ['Samuel Pepys (người viết nhật ký)']}),
 ('H1-05b', 'HỒI 1', 'H1-05', 5.167, '—', 'MD', None, 'M-d (2) sà lan đầy đồ đạc rời bến, khói trên mái', {'MD': 5.167}, {'md': 2}),
 ('H1-06', 'HỒI 1', 'H1-06', 13.542, 'P5', 'CAU', ('h66', 12.0, 17.0), 'Thị trưởng bất lực ở Cannon Street; lửa vượt sức phá nhà', {'A': 13.542, 'THE': 3}, {'cau_dz': -52, 'the': ['Sir Thomas Bludworth (Thị trưởng)'], 'tieu_diem_en': [532600, 180900, 10]}),
 ('H1-07', 'HỒI 1', 'H1-07', 15.458, 'P2', 'VONG', ('h66', 17.0, 18.0), 'khoảng trống 1633 trên cầu chặn lửa sang Southwark; gió đẩy lửa sang tây', {'A': 15.458}, {'vong_deg': 36, 'tam': [532786, 180554, 10], 'tieu_diem_en': [532786, 180554, 10]}),
 ('H1-08a', 'HỒI 1', 'H1-08', 6.0, '—', 'MD', None, 'M-d (9) quán bia nhỏ bên Bankside chạng vạng: người đứng xem ánh lửa bên kia sông (nhìn từ sau, không nhân vật chính)', {'MD': 6.0}, {'md': 9}),
 ('H1-08b', 'HỒI 1', 'H1-08', 12.208, 'P1', 'CODINH', ('h66', 18.0, 22.0), 'P1 tái xuất: chạng vạng → vòng cung lửa (cùng khung M03)', {'A': 12.208}, {'tieu_diem_en': [532700, 180900, 20]}),
 ('H1-09', 'HỒI 1', 'H1-09', 9.0, 'P7', 'XUONG', ('h66', 38.0, 40.0), 'BẢN ĐỒ CỔ HOẠT HOÁ Doornick 1666: lửa lan theo ngày 2→3/9 → chuyển 3D cùng toạ độ, nhìn xuống → xiên', {'MAP': 5.0, 'MAP3D': 4.0}, {'ban_do': {'s': 5.0, 'h0': 1.0, 'h1': 40.0}, 'xuong': {'tu': 5.0}, 'chuyen_s': -4.167, 'tieu_diem_en': [532800, 181050, 10]}),
 ('H1-10', 'HỒI 1', 'H1-10', 7.083, '—', 'MD', None, 'M-d (4)+(6) Watling Street / Cheapside 3/9: xe chất đồ, người khiêng người bệnh', {'MD': 7.083}, {'md': 4, 'chuyen_s': 4.167}),
 ('H1-12', 'HỒI 1', 'H1-12', 6.458, '—', 'MD', None, 'M-d (3) Thames đêm 3/9: sà lan, đồ trôi, bờ bắc rực lửa (đổi chỗ với H1-11 theo thứ tự lời)', {'MD': 6.458}, {'md': 3}),
 ('H1-11', 'HỒI 1', 'H1-11', 14.417, 'P8', 'CODINH', ('h66', 38.0, 47.0), 'Royal Exchange cháy; trời "như miệng lò" — Evelyn', {'A': 14.417, 'THE': 4}, {'the': ['John Evelyn (người viết nhật ký)'], 'tieu_diem_en': [532800, 181120, 15]}),
 ('H1-13', 'HỒI 1', 'H1-13', 11.875, 'P4b', 'THAP', ('h66', 90.0, 93.0), "lửa leo đồi Ludgate tới Old St Paul's bọc giàn giáo gỗ; nhà thờ bốc cháy", {'A': 11.875, 'KHAC': 4}, {'khac': 'ycba-266-0', 'chuyen_s': -0.583, 'tieu_diem_en': [532050, 181140, 78]}),
 ('H1-14', 'HỒI 1', 'H1-14', 6.0, '—', 'MD', None, "M-d (5) chì chảy thành dòng trên phố quanh St Paul's đêm 4/9", {'MD': 6.0}, {'md': 5, 'chuyen_s': 0.583}),
 ('H1-15', 'HỒI 1', 'H1-15', 21.5, 'P8', 'CAU', ('h66', 92.0, 95.0), 'lửa vượt sông Fleet; nổ nhà bằng thuốc súng mở khoảng chặn (lớp a, render); Navy Office', {'A': 21.5}, {'cau_dz': 84, 'cau_h0': 150, 'tieu_diem_en': [533000, 180800, 10]}),
 ('H1-16', 'HỒI 1', 'H1-16', 7.25, 'P1', 'CODINH', ('h66', 94.0, 102.0), 'P1: gió dịu, lửa tàn → bình minh 6/9', {'A': 7.25}, {'tieu_diem_en': [532420, 180980, 15]}),
 ('H1-17a', 'HỒI 1', 'H1-17', 6.0, '—', 'MD', None, 'M-d (7) Moorfields: lều, chòi, đống đồ cứu được', {'MD': 6.0}, {'md': 7}),
 ('H1-17b', 'HỒI 1', 'H1-17', 6.292, '—', 'MD', None, 'M-d (7) Moorfields chạng vạng: gia đình quanh lửa nấu', {'MD': 6.292}, {'md': 7}),
 ('H1-18', 'HỒI 1', 'H1-18', 16.292, 'P7', 'XUONG', ('h66', 124.0, 130.0), 'phế tích bốc khói 7/9: ranh vùng cháy + bộ đếm 13 200 nhà / 87 nhà thờ', {'A': 16.292, 'MAP3D': 5, 'THE': 4}, {'xuong': {'tu': 0.0}, 'dem': ['13,200 houses', '87 churches'], 'tieu_diem_en': [532350, 181050, 10]}),
 ('H1-19', 'HỒI 1', 'H1-19', 6.0, '—', 'MD', None, 'M-d (8) phế tích bốc khói, ống khói gạch còn đứng', {'MD': 6.0}, {'md': 8}),
 ('H2-01a', 'HỒI 2', 'H2-01', 6.5, '—', 'MD', None, 'M-d (8) lối đi giữa tro còn nóng; tháp nhà thờ cháy dở làm mốc', {'MD': 6.5}, {'md': 8}),
 ('H2-01b', 'HỒI 2', 'H2-01', 6.667, '—', 'MD', None, 'M-d (8) người bới tro tìm lối, khói mỏng', {'MD': 6.667}, {'md': 8}),
 ('H2-02', 'HỒI 2', 'H2-02', 14.625, 'P7', 'XUONG', ('y', 1666.72, 1666.72, [9, 20, 12.0], 0), 'phương án Wren (bản in LoC) đặt khớp lên City cháy — không được dựng', {'A': 14.625, 'TL': 8, 'MAP3D': 4, 'THE': 7}, {'tl': 'loc-wren-plan-0', 'xuong': {'tu': 8.0}, 'the': ['Christopher Wren', 'Robert Hooke'], 'tieu_diem_en': [532350, 181000, 10]}),
 ('H2-03a', 'HỒI 2', 'H2-03', 8.0, '—', 'MD', None, 'M-d (10) 1667: thợ đo căng dây, cắm cọc chia lô giữa tro; chủ đất tranh cãi', {'MD': 8.0}, {'md': 10}),
 ('H2-03b', 'HỒI 2', 'H2-03', 12.167, 'P5', 'CODINH', ('y', 1667.15, 1667.45, [3, 10, 13.0], 0), 'lô đất rối trên đúng lưới phố cũ', {'A': 12.167}, {'tieu_diem_en': [532300, 181000, 10]}),
 ('H2-03c', 'HỒI 2', 'H2-03', 6.0, '—', 'MD', None, "M-d (19) Toà Cháy 1667: phiên xử ở một sảnh gỗ, thẩm phán vô danh, chủ đất và người thuê trình giấy (mới)", {'MD': 6.0}, {'md': 19}),
 ('H2-04a', 'HỒI 2', 'H2-04', 6.0, 'P4', 'TRUOT', ('y', 1667.6, 1668.4, [6, 1, 11.0], 0), 'Rebuilding Act: nhà gạch mọc dọc Fleet Street (M-d (11) trượt 3 lượt — mũ lỗi thời đại → 3D)', {'A': 6.0}, {'md_truot': 'H2-04a 3/3 lượt LOẠI (mũ bowler/chóp tròn — lỗi thời đại) → 3D', 'tieu_diem_en': [531700, 181150, 20]}),
 ('H2-04b', 'HỒI 2', 'H2-04', 5.708, '—', 'MD', None, 'M-d (11) xe chở gạch, giàn giáo gỗ trên mặt phố', {'MD': 5.708}, {'md': 11}),
 ('H2-05', 'HỒI 2', 'H2-05', 18.833, 'P1', 'CODINH', ('y', 1668.0, 1671.0, [9, 1, 15.0], 0), 'P1: timelapse xây lại bằng gạch trên đúng lô cũ (≈ 6 000 nhà cuối 1670)', {'A': 18.833}, {'tieu_diem_en': [532420, 180980, 15]}),
 ('H2-06', 'HỒI 2', 'H2-06', 12.0, 'P3', 'VONG', ('y', 1671.0, 1677.0, [9, 1, 15.0], 0), 'Monument mọc; 202 ft = khoảng cách tới lò bánh', {'A': 12.0, 'THE': 2.5, 'KHAC': 3}, {'khac': 'rijks-monument-0', 'vong_deg': 30, 'tam': [532923, 180761, 30], 'p': [533190, 180600, 125], 'dem': ['202 ft'], 'tieu_diem_en': [532923, 180761, 30]}),
 ('H2-07', 'HỒI 2', 'H2-07', 7.917, '—', 'MD', None, 'M-d (13) 1680: phố gạch mới, dấu bảo hiểm cháy kim loại gắn trên cửa (Fire Office, Barbon)', {'MD': 7.917, 'THE': 4}, {'md': 13, 'the': ['Nicholas Barbon']}),
 ('H2-08', 'HỒI 2', 'H2-08', 5.708, 'P2', 'NGHIENG', ('y', 1670.0, 1700.0, [9, 1, 15.0], 0), 'chóp nhà thờ Wren mọc quanh City; nghiêng lên kết ở chóp', {'A': 5.708}, {'nghieng_deg': 8, 'tieu_diem_en': [532500, 181050, 40]}),
 ('H2-09', 'HỒI 2', 'H2-09', 7.667, 'P1', 'CODINH', ('y', 1675.0, 1708.0, [9, 1, 15.0], 0), "P1: St Paul's mới mọc từ nền Old St Paul's", {'A': 7.667}, {'tieu_diem_en': DOME}),
 ('H2-10', 'HỒI 2', 'H2-10', 18.042, 'P4b', 'THAP', ('y', 1708.0, 1711.0, [9, 1, 17.5], 0), 'đèn lồng hoàn tất; 365 ft — mái vòm anh hùng giờ vàng', {'A': 18.042, 'THE': 2.5}, {'dem': ['365 ft'], 'tieu_diem_en': [532118, 181150, 100]}),
 ('H2-11', 'HỒI 2', 'H2-11', 6.0, 'P7', 'XUONG', ('y', 1676.0, 1676.0, [9, 1, 14.0], 0), 'nhìn xuống → xiên 1676: City gạch trên cùng tuyến phố 1666 (thay Ogilby — D13 không lên hình)', {'A': 6.0}, {'xuong': {'tu': 0.0}, 'tieu_diem_en': [532350, 181000, 10]}),
 ('H2-12', 'HỒI 2', 'H2-12', 12.0, 'P2', 'KHOP', ('khop', ('y', 1647.0, 1647.0, [9, 1, 15.0], 0), ('y', 1711.0, 1711.0, [9, 1, 15.0], 0), 6.0), 'then–now: cùng khung St Saviour 1647 ↔ 1711', {'A': 12.0, 'KHAC': 3}, {'khop_voi': 'H1-03', 'hoa_s': 1.0, 'khac': 'met-360649-0', 'tieu_diem_en': [532420, 180800, 15]}),
 ('H2-13', 'HỒI 2', 'H2-13', 6.0, '—', 'MD', None, 'M-d (12) Thames 1711: thuyền chèo chở khách, City gạch + mái vòm mới phía xa', {'MD': 6.0}, {'md': 12}),
 ('H2-14', 'HỒI 2', 'H2-14', 6.0, 'P5', 'CAU', ('y', 1709.0, 1711.0, [9, 1, 15.0], 0), 'cần cẩu hạ: City gạch đã kín lô, mái vòm hoàn tất', {'A': 6.0}, {'cau_dz': -24, 'tieu_diem_en': [532350, 180900, 10]}),
 ('H3-01', 'HỒI 3', 'H3-01', 6.167, 'P1', 'CODINH', ('y', 1711.0, 1860.0, [9, 1, 15.0], 0), 'P1: mái vòm cao nhất > 250 năm', {'A': 6.167}, {'tieu_diem_en': DOME}),
 ('H3-02', 'HỒI 3', 'H3-02', 10.125, 'P6', 'TRUOT', ('y', 1756.0, 1832.0, [9, 1, 15.0], 0), 'nhà trên cầu London dỡ (1758, LMA); cầu mới (1831) thay cầu cổ', {'A': 10.125}, {'tieu_diem_en': [532800, 180600, 10]}),
 ('H3-03', 'HỒI 3', 'H3-03', 12.458, 'P7', 'XUONG', ('y', 1860.0, 1871.0, [9, 1, 14.0], 0), 'Victoria Embankment đẩy bờ bắc ra sông (bờ 1666 ↔ nay)', {'A': 12.458, 'MAP3D': 4}, {'xuong': {'tu': 0.0}, 'tieu_diem_en': [531600, 180800, 0]}),
 ('H3-04a', 'HỒI 3', 'H3-04', 3.958, 'P5', 'CODINH', ('y', 1900.0, 1937.0, [9, 1, 15.0], 0), 'toà văn phòng 1930 cao dần quanh nhà thờ', {'A': 3.958}, {'tieu_diem_en': DOME}),
 ('H3-04b', 'HỒI 3', 'H3-04', 7.0, '—', 'MD', None, 'M-d (14) 1930s: hẻm City hẹp, người làm văn phòng đội mũ đi bộ — phố bên dưới không đổi', {'MD': 7.0}, {'md': 14}),
 ('H3-05', 'HỒI 3', 'H3-05', 19.708, 'P4b', 'THAP', ('y', 1937.0, 1938.5, [9, 1, 16.0], 0), "St Paul's Heights: mặt phẳng trần cao độ hiện mờ quanh mái vòm", {'A': 19.708, 'THE': 4}, {'the': ['Godfrey Allen (kiến trúc sư nhà thờ)'], 'tieu_diem_en': [532118, 181150, 100]}),
 ('H3-06', 'HỒI 3', 'H3-06', 8.0, 'P1', 'KHOP', ('khop', ('y', 1938.5, 1938.5, [9, 1, 15.0], 0), ('y', 1666.66, 1666.66, [9, 1, 15.0], 0), 4.0), 'P1 KHOP 1938 ↔ 1666', {'A': 8.0}, {'khop_voi': 'H3-01', 'hoa_s': 1.0, 'tieu_diem_en': DOME}),
 ('H4-01a', 'HỒI 4', 'H4-01', 6.0, 'P1', 'CODINH', ('d', [1940, 12, 29, 15.5], [1940, 12, 29, 16.6], 0), 'P1: Chủ nhật 29/12/1940 chạng vạng mùa đông', {'A': 6.0}, {'tieu_diem_en': DOME}),
 ('H4-01b', 'HỒI 4', 'H4-01', 6.0, '—', 'MD', None, 'M-d (15) phố City vắng chiều Chủ nhật 1940, khí cầu phòng không trên trời', {'MD': 6.0}, {'md': 15}),
 ('H4-02', 'HỒI 4', 'H4-02', 10.875, 'P5', 'CAU', ('h40', 0.6, 3.0), 'bom cháy rơi; ≈ 1 500 đám cháy; bộ đếm 100 000', {'A': 10.875, 'THE': 3}, {'cau_dz': -42, 'dem': ['100,000 incendiaries'], 'chuyen_s': 0.292, 'tieu_diem_en': [532300, 181100, 10]}),
 ('H4-03', 'HỒI 4', 'H4-03', 8.0, '—', 'MD', None, 'M-d (16) lính cứu hoả kéo vòi trên bãi bùn Thames triều thấp, ống nước vỡ', {'MD': 8.0}, {'md': 16, 'chuyen_s': -0.292}),
 ('H4-04a', 'HỒI 4', 'H4-04', 8.5, 'P4b', 'THAP', ('h40', 4.0, 4.8), 'Paternoster Row cháy cạnh mái vòm', {'A': 8.5}, {'tieu_diem_en': [532118, 181150, 90]}),
 ('H4-04b', 'HỒI 4', 'H4-04', 6.5, '—', 'MD', None, "M-d (17) đội canh St Paul's Watch dập bom cháy trên mái chì bằng bơm tay, cát", {'MD': 6.5}, {'md': 17}),
 ('H4-04c', 'HỒI 4', 'H4-04', 13.25, 'P3', 'CODINH', ('h40', 5.0, 6.0), 'cả City cháy; mái Guildhall; mái vòm còn đứng giữa khói', {'A': 13.25}, {'tieu_diem_en': DOME}),
 ('H4-05', 'HỒI 4', 'H4-05', 4.542, 'P1', 'DAY', ('h40', 13.0, 13.5), 'P1: sáng ra mái vòm còn đứng giữa vòng phế tích', {'A': 4.542}, {'tieu_diem_en': DOME}),
 ('H4-06', 'HỒI 4', 'H4-06', 10.208, 'P1', 'CODINH', ('h40', 14.0, 40.0), 'P1: vòng phế tích; bộ đếm 160', {'A': 10.208, 'THE': 2.5}, {'dem': ['160 killed'], 'tieu_diem_en': DOME}),
 ('H4-07', 'HỒI 4', 'H4-07', 5.458, 'P7', 'XUONG', ('y', 1941.3, 1941.3, [3, 1, 13.0], 0), 'vùng bom nặng Cripplegate / Paternoster (ước lượng)', {'A': 5.458, 'MAP3D': 5}, {'xuong': {'tu': 0.0}, 'tieu_diem_en': [532300, 181300, 10]}),
 ('H4-08', 'HỒI 4', 'H4-08', 12.0, 'P2', 'KHOP', ('khop', ('h66', 130.0, 132.0), ('y', 1941.3, 1941.3, [3, 1, 13.0], 0), 6.0), 'hai khoảng trống cùng một khung: 1666 ↔ 1941', {'A': 12.0}, {'khop_voi': 'H2-12', 'hoa_s': 1.0, 'tieu_diem_en': [532420, 180800, 15]}),
 ('H5-01', 'HỒI 5', 'H5-01', 12.542, 'P5', 'CODINH', ('y', 1946.0, 1951.0, [9, 1, 15.0], 1), 'Holden–Holford: quy hoạch lại vùng bom', {'A': 12.542, 'THE': 4}, {'the': ['Charles Holden', 'William Holford'], 'tieu_diem_en': [532300, 181300, 10]}),
 ('H5-02', 'HỒI 5', 'H5-02', 14.875, 'P5', 'CAU', ('y', 1957.0, 1976.0, [9, 1, 15.0], 1), 'London Wall (Route 11) + Barbican mọc trên Cripplegate', {'A': 14.875}, {'cau_dz': -58, 'tieu_diem_en': [532300, 181600, 10]}),
 ('H5-03', 'HỒI 5', 'H5-03', 6.458, 'P7', 'XUONG', ('y', 2026.67, 2026.67, [9, 2, 13.0], 1), 'lưới phố Doornick 1666 chồng lên 3D 2026: cùng tuyến', {'A': 6.458, 'MAP': 6.458}, {'ban_do_chong': True, 'xuong': {'tu': 0.0}, 'tieu_diem_en': [532350, 181000, 10]}),
 ('H5-04', 'HỒI 5', 'H5-04', 10.417, 'P1', 'CODINH', ('y', 1985.0, 2026.67, [9, 2, 14.0], 1), 'P1: khoảng trống lấp dần; cụm toà cao phía đông mọc (thế kỷ này)', {'A': 10.417, 'N2P': 6.0}, {'tam_nen': [4.417, 10.417], 'tam_nen_tu': 'M01', 'nam': [[0, 1985.0], [4.417, 2026.67], [10.417, 2026.67]], 'tieu_diem_en': [533150, 181150, 120]}),
 ('H5-05a', 'HỒI 5', 'H5-05', 16.5, 'P9', 'CODINH', ('d', [2026, 9, 2, 17.0], [2026, 9, 2, 17.3], 1), 'tầm nhìn bảo vệ từ bờ nam: toà cao mọc trên phố cũ, mái vòm vẫn có nền trời', {'A': 16.5, 'N2P': 16.5}, {'tam_nen': [0, 16.5], 'tieu_diem_en': DOME}),
 ('H5-05b', 'HỒI 5', 'H5-05', 9.125, 'P4', 'THAP', ('d', [2026, 9, 2, 17.5], [2026, 9, 2, 17.6], 1), 'từ Fleet Street: Leadenhall vát — mái vòm còn nền trời', {'A': 9.125}, {'tieu_diem_en': DOME}),
 ('H5-06', 'HỒI 5', 'H5-06', 6.0, 'P3', 'CODINH', ('d', [2026, 9, 2, 16.0], [2026, 9, 2, 16.2], 1), 'từ phía đông: mái vòm giữa cụm toà cao', {'A': 6.0}, {'tam_nen_truot': 'P3-2026 trượt (iii) cả 3 lượt → 3D V2 (lệnh việc 5)', 'tieu_diem_en': DOME}),
 ('H5-07a', 'HỒI 5', 'H5-07', 6.0, 'P9', 'CODINH', ('d', [2026, 9, 2, 22.0], [2026, 9, 2, 22.1], 1), 'bờ nam đêm 2026: City sáng đèn quanh mái vòm (M-d (18) trượt 3 lượt ở ảnh đầu → 3D)', {'A': 6.0}, {'md_truot': 'H5-07a ảnh đầu LOẠI 3/3 lượt → 3D', 'tieu_diem_en': DOME}),
 ('H5-07b', 'HỒI 5', 'H5-07', 15.333, 'P1', 'KHOP', ('khop', ('h66', 22.0, 22.5), ('d', [2026, 9, 2, 22.0], [2026, 9, 2, 22.3], 1), 7.5), 'KHÉP VÒNG: cùng khung Bankside — vòng cung lửa 1666 ↔ đèn City 2026', {'A': 15.333}, {'khop_voi': 'M03', 'hoa_s': 1.0, 'tieu_diem_en': DOME}),
 ('H5-08', 'HỒI 5', 'H5-08', 18.0, 'P1', 'KEO', ('d', [2026, 9, 2, 22.3], [2026, 9, 2, 22.8], 1), 'kéo lùi cuối: mái vòm giữa toà cao, sông, Bankside', {'A': 18.0}, {'lo_ra': 'bờ Bankside + sông + toàn cụm toà cao quanh mái vòm', 'tieu_diem_en': DOME}),
 ('H5-09', 'HỒI 5', 'H5-09', 16.0, '—', 'PP', None, 'hai thẻ "How this film was made" × 8 s (§12.1 b)', {'PP': 16.0}, {}),
]
MD_MOC = {1: 'Pudding Lane 01:00 2/9', 2: 'bờ sông gần cầu sáng 2/9', 3: 'Thames sà lan + đồ trôi, bờ bắc rực lửa', 4: 'Watling Street xe/người khiêng/người bệnh (+ (6) Cheapside cứu đồ lên xe)',
          5: "chì chảy quanh St Paul's đêm 4/9", 7: 'Moorfields lều/chòi/đống đồ', 8: 'phế tích bốc khói 7/9 (+ tro còn nóng 9/1666)',
          9: 'quán bia Bankside 2/9 chạng vạng (mới)', 10: 'chia lô giữa tro 1667 (mới)', 11: 'xây tường gạch 1667–68 (mới)', 12: 'Thames 1711 (mới)', 13: 'phố gạch 1680 + dấu bảo hiểm cháy (mới)',
          14: 'hẻm City 1930s (mới)', 15: 'City vắng chiều 29/12/1940 (mới)', 16: 'vòi rồng trên bãi bùn triều thấp 29/12/1940 (mới)', 17: "St Paul's Watch trên mái (mới)", 18: 'Bankside đêm 2026 (mới)', 19: 'Toà Cháy 1667 (mới)'}
CAP = {'AI': 70, 'N2P': 50, 'MAP_ALL': 12, 'TL_KHAC_THE': 10, 'THAP': 12}
GOC_CAO = {'P1', 'P2', 'P3', 'P5', 'P7', 'P8', 'P9'}   # ≥ 120 m (V7B-D1); P4/P4b/P6 thấp


def main():
    K = k1c1.bang(); nhom_s = collections.OrderedDict()
    for ma, v in K.items(): nhom_s[ma] = v['dai_k1c1']
    # kiểm: tổng giây mỗi nhóm = K1-C1 (cộng phần chuyển hình sang nhóm kề)
    tong_nhom = collections.Counter(); chuyen = collections.Counter()
    for s in S: tong_nhom[s[2]] += s[3]; chuyen[s[2]] += s[9].get('chuyen_s', 0)
    loi_nhom = []
    for k, v in nhom_s.items():
        if abs(tong_nhom[k] - chuyen[k] - v) > 1e-3: loi_nhom.append(f'{k}: {tong_nhom[k]:.3f} − chuyển {chuyen[k]:+.3f} ≠ K1-C1 {v:.3f}')
    rows, t = [], 0.0
    # mốc lời mới (trong phim): mỗi nhóm đặt ở đầu nhóm + 0,2 s
    nhom_t0 = collections.OrderedDict()
    for s in S:
        if s[2] not in nhom_t0: nhom_t0[s[2]] = round(t, 4); t += nhom_s[s[2]]
    T = round(sum(s[3] for s in S), 4); t = 0.0
    for (ma, phan, nhom, dur, dm, cu, tg, vai, lop, them) in S:
        v = K[nhom]; cau = [c for c in v['cau'] if not c['bo']]
        Ls = sorted({c['L'] for c in cau if c['L']}, key=lambda x: int(x[1:])) if cau else []
        r = {'ma': ma, 'phan': phan, 'chuong': phan, 'nhom_loi': nhom, 'bat_dau_s': round(t, 4), 'giay': dur, 't0': round(t, 4), 't1': round(t + dur, 4), 'dur': dur,
             'loi': (f"{Ls[0]}–{Ls[-1]}" if len(Ls) > 1 else (Ls[0] if Ls else ('(lặng)' if cu != 'PP' else '—'))) if not any(x['ma'] != ma and x[2] == nhom for x in [] ) else '',
             'cau_loi': [c['khoa'] for c in cau], 'diem_may': dm, 'may': DM.get(dm), 'cu_may': cu, 'loai_may': cu, 'thoi_gian': tg, 'vai': vai, 'lop': lop,
             'goc': 'cao' if dm in GOC_CAO else ('md' if cu == 'MD' else ('pp' if cu == 'PP' else 'thap')), 'tl': cu not in ('MD', 'PP'),
             'minh_hoa': cu == 'MD', 'ai_nen': 'N2P' in lop, 'tieu_diem_en': them.get('tieu_diem_en'), 'them': them}
        r['loi_bd_s'] = round(nhom_t0[nhom] + 0.2, 4) if cau else None
        if cu == 'KHOP': r.update(khop_voi=them['khop_voi'], hoa_s=them['hoa_s'], diem_neo=them.get('tieu_diem_en'))
        if cu == 'KEO': r['lo_ra'] = them['lo_ra']
        if cu == 'MD': r['md_moc'] = them['md']; r['md_ten'] = MD_MOC[them['md']]
        rows.append(r); t += dur
    # cột lời: nhóm tách nhiều shot → mỗi shot ghi nhóm (lời chảy qua ranh hình trong nhóm)
    for r in rows:
        anh_em = [x['ma'] for x in rows if x['nhom_loi'] == r['nhom_loi']]
        if len(anh_em) > 1: r['loi'] = f"{r['loi']} (nhóm {r['nhom_loi']}: {', '.join(anh_em)})"
    L = collections.Counter()
    for r in rows:
        for k, v in r['lop'].items(): L[k] += v
    pct = {k: round(100 * v / T, 2) for k, v in L.items()}
    than = T - L['PP']
    cao = sum(r['dur'] for r in rows if r['goc'] == 'cao' and r['tl'] and r['cu_may'] != 'XUONG' or (r['cu_may'] == 'XUONG' and r['goc'] == 'cao' and 'ban_do' not in r['them']))
    cao -= sum(r['them']['ban_do']['s'] for r in rows if 'ban_do' in r['them'])
    cao += sum(r['dur'] - r['them']['ban_do']['s'] for r in rows if 'ban_do' in r['them'])
    thap = sum(r['dur'] for r in rows if r['cu_may'] == 'THAP')
    tong = {'thoi_luong_s': T, 'k1c1_s': round(sum(nhom_s.values()), 4), 'so_shot': len(rows), 'shot_tb_s': round(T / len(rows), 2), 'lop_s': {k: round(v, 3) for k, v in L.items()}, 'lop_pct': pct,
            'MD_pct': pct.get('MD', 0), 'N2P_pct': pct.get('N2P', 0), 'AI_pct': round(100 * (L['N2P'] + L['MD']) / T, 2), 'MAP_ALL_pct': round(100 * (L['MAP'] + L['MAP3D']) / T, 2),
            'TL_KHAC_THE_pct': round(100 * (L['TL'] + L['KHAC'] + L['THE']) / T, 2), 'THAP_pct': round(100 * thap / T, 2), 'goc_cao_than_phim_pct': round(100 * cao / than, 2), 'than_phim_s': than,
            'md_clip': sum(1 for r in rows if r['cu_may'] == 'MD'), 'md_moc': len({r['md_moc'] for r in rows if r['cu_may'] == 'MD'})}
    kiem = []
    def k_(ten, v, cap=None, duoi=None, dat=None, ghi=''):
        d = dat if dat is not None else ((cap is None or v <= cap) and (duoi is None or v >= duoi))
        nguong = cap if cap is not None else duoi
        kiem.append({'chi_so': ten, 'gia_tri': v, 'tran': cap, 'san': duoi, 'dat': d, 'trong_5pct': (nguong is not None and isinstance(v, (int, float)) and abs(v - nguong) <= 0.05 * nguong) or
                     (cap is not None and duoi is not None and isinstance(v, (int, float)) and abs(v - duoi) <= 0.05 * duoi), 'ghi': ghi})
    k_('Tổng = K1-C1 730,083 s', T, dat=abs(T - tong['k1c1_s']) < 1e-3 and not loi_nhom, ghi='; '.join(loi_nhom))
    k_('Omni M-d % (Q1: 20–23 %)', tong['MD_pct'], cap=23, duoi=20)
    k_('Tấm nền N2+ % (V7: mục tiêu 5–15 %)', tong['N2P_pct'], cap=15, duoi=5, ghi='P3-2026 (H5-06) trượt (iii) 3/3 lượt → 3D')
    k_('Tổng AI % (≤ 70)', tong['AI_pct'], cap=CAP['AI'])
    k_('BAN-DO-12: MAP + MAP3D % (≤ 12)', tong['MAP_ALL_pct'], cap=CAP['MAP_ALL'])
    k_('TU-LIEU-10: TL + KHAC + THE % (≤ 10)', tong['TL_KHAC_THE_pct'], cap=CAP['TL_KHAC_THE'])
    k_('GOC-CAO-60: góc cao có thời gian chạy / thân phim % (≥ 60)', tong['goc_cao_than_phim_pct'], duoi=60, ghi='ước trước dựng theo điểm máy; số đo thật theo log khung V7B-D1 ở k2check')
    k_('THAP % (≤ 12)', tong['THAP_pct'], cap=CAP['THAP'])
    k_('M-d mỗi clip ≤ 8 s', max(r['dur'] for r in rows if r['cu_may'] == 'MD'), cap=8.0)
    k_('MAP mỗi lần ≤ 10 s', max([r['lop'].get('MAP', 0) for r in rows]), cap=10.0)
    k_('N2P chỉ trên CODINH', '', dat=all(r['cu_may'] == 'CODINH' for r in rows if r['ai_nen']))
    k_('N2P chỉ 2026 ban ngày (V1)', '', dat=all(r['thoi_gian'][0] in ('d', 'y') and (r['thoi_gian'][2] if r['thoi_gian'][0] == 'd' else [r['thoi_gian'][2]])[0] >= 2026 for r in rows if r['ai_nen']),
       ghi='H5-04: tấm nền chỉ ở 6 s cuối (năm 2026, ban ngày) — hoà ≥ 2 s')
    k_('N2P và MD không chồng', '', dat=all(not (r['ai_nen'] and r['minh_hoa']) for r in rows))
    k_('M-d kẹp giữa hai shot 3D (§15 f)', '', dat=all(rows[i - 1]['cu_may'] != 'PP' and i + 1 < len(rows) for i, r in enumerate(rows) if r['cu_may'] == 'MD'))
    by = collections.defaultdict(list)
    for r in rows: by[r['phan']].append(r)
    for ph, rs in by.items():
        loai = {r['cu_may'] for r in rs if r['cu_may'] not in ('MD', 'PP', 'THE')}
        run, mx, prev = 0, 0, None
        for r in rs:
            if r['cu_may'] in ('MD', 'PP', 'THE'): run, prev = 0, None; continue
            run = run + 1 if r['cu_may'] == prev else 1; prev = r['cu_may']; mx = max(mx, run)
        k_(f'{ph}: số loại cú máy ≥ 4', len(loai), duoi=4)
        k_(f'{ph}: chuỗi cùng loại ≤ 2', mx, cap=2)
        k_(f'{ph}: P1 tái xuất (fov 36°)', '', dat=any(r['diem_may'] == 'P1' for r in rs))
    out = {'nhom_loi_t0': nhom_t0, 'tap': 'K2C-T4-02', 'phien': 'ANIMATIC-T4', 'ngay': '2026-10-24', 'phuong_an_g1': 'K1-C1', 'diem_may': DM, 'shot': rows, 'tong': tong, 'kiem': kiem, 'md_moc': MD_MOC,
           'mo_ta_lop': 'giây trong shot; THE/KHAC/TL/MAP3D chồng trên A'}
    EP = os.path.join(REPO, 'channel-k2/k2c-t4-02')
    json.dump(out, open(os.path.join(EP, 'BANG-SHOT-v2.json'), 'w'), ensure_ascii=False, indent=1)
    md = ['# BẢNG SHOT v2 — K2C-T4-02 London (ANIMATIC-T4, 24/10/2026)', '',
          '> Sinh bằng `scripts/k2ldn/bang_shot_v2.py` (nguồn thật của bảng). Bản máy đọc: `BANG-SHOT-v2.json`. v1 giữ nguyên (`BANG-SHOT-v1.md`).',
          '> Căn cứ: G-1 = (c) K1-C1 (730,083 s), G-2 = (a), G-3 giữ St Saviour\'s/Wenceslaus, alias Evelyn "Eevlin" (chủ dự án 24/10/2026); GIAN-SHOT §6; Q1 (Omni 20–23 %); V1/V7 (tấm nền chỉ 2026 ban ngày, 5–15 %); V5 (P1 fov 36°); §19 (a)(b)(c).',
          '> Lời của mỗi **nhóm** (shot v1) đặt tại đầu nhóm + 0,2 s; nhóm tách nhiều shot thì lời chảy qua ranh hình. Lớp: A cách A · N2P tấm nền · MD minh hoạ Omni · MAP bản đồ cổ · MAP3D 3D kiểu bản đồ · KHAC tranh khắc · THE thẻ/bộ đếm · TL tư liệu · PP thẻ phương pháp.', '',
          '## Điểm máy', '', '| Mã | Tên | Vị trí E, N, h (m) | Nhìn tới | FOV dọc |', '|---|---|---|---|---|']
    for k, v in DM.items(): md.append(f"| {k} | {v['ten']} | {v['p']} | {v['l']} | {v['fov']}° |")
    md += ['', '## Bảng', '', '| Mã | t | Dài (s) | Lời | Máy | Cú máy | Góc | Thời gian | Vai truyện | Lớp | Ghi |', '|---|---|---|---|---|---|---|---|---|---|---|']
    def tgs(tg):
        if not tg: return '—'
        if tg[0] == 'd': return f"{tg[1][2]}/{tg[1][1]}/{tg[1][0]} {tg[1][3]:g}h → {tg[2][3]:g}h"
        if tg[0] == 'h66': return f"lửa 1666 giờ {tg[1]:g} → {tg[2]:g} (kể từ 2/9 00:00)"
        if tg[0] == 'h40': return f"29/12/1940 18:00 + {tg[1]:g} → {tg[2]:g} h"
        if tg[0] == 'y': return f"{tg[1]:g} → {tg[2]:g}" if tg[1] != tg[2] else f"{tg[1]:g}"
        if tg[0] == 'khop': return f"KHOP: {tgs(tg[1])} ↔ {tgs(tg[2])} (cắt ở {tg[3]:g} s)"
    for r in rows:
        m, s_ = divmod(r['t0'], 60); g = []
        if r['them'].get('the'): g.append('thẻ: ' + '; '.join(r['them']['the']))
        if r['them'].get('dem'): g.append('bộ đếm: ' + ' / '.join(r['them']['dem']))
        if r['them'].get('tam_nen'): g.append(f"tấm nền {r['them']['tam_nen'][0]:g}–{r['them']['tam_nen'][1]:g} s")
        if r.get('khop_voi'): g.append(f"KHOP với {r['khop_voi']}, hoà {r['hoa_s']:g} s")
        if r.get('lo_ra'): g.append('lộ ra: ' + r['lo_ra'])
        if r['them'].get('chuyen_s'): g.append(f"chuyển hình {r['them']['chuyen_s']:+.3f} s với nhóm kề")
        md.append(f"| {r['ma']} | {int(m)}:{s_:04.1f} | {r['dur']:.3f} | {r['loi']} | {r['diem_may']} | {r['cu_may']} | {r['goc']} | {tgs(r['thoi_gian'])} | {r['vai']} | {', '.join(f'{k} ({v:g})' for k, v in r['lop'].items())} | {'; '.join(g)} |")
    md += ['', '## Tổng + kiểm trước dựng', '', f"- Thời lượng **{T:.3f} s** (K1-C1 {tong['k1c1_s']:.3f} s) · **{len(rows)} shot** · TB {tong['shot_tb_s']} s · M-d {tong['md_clip']} clip / {tong['md_moc']} khoảnh khắc.",
           f"- Lớp (s): {tong['lop_s']}", '', '| Chỉ số | Giá trị | Trần | Sàn | Đạt | ±5 % quanh ngưỡng | Ghi |', '|---|---|---|---|---|---|---|']
    for k in kiem: md.append(f"| {k['chi_so']} | {k['gia_tri']} | {k['tran'] if k['tran'] is not None else ''} | {k['san'] if k['san'] is not None else ''} | {'ĐẠT' if k['dat'] else '**TRƯỢT**'} | {'**CÓ**' if k['trong_5pct'] else ''} | {k['ghi']} |")
    md += ['', '## Khoảnh khắc M-d', '', '| # | Khoảnh khắc | Shot | Giây |', '|---|---|---|---|']
    for n, ten in MD_MOC.items():
        sh = [r for r in rows if r.get('md_moc') == n]
        if sh: md.append(f"| {n} | {ten} | {', '.join(r['ma'] for r in sh)} | {sum(r['dur'] for r in sh):.3f} |")
    open(os.path.join(EP, 'BANG-SHOT-v2.md'), 'w').write('\n'.join(md) + '\n')
    print(json.dumps(tong, ensure_ascii=False)); [print('TRƯỢT', k) for k in kiem if not k['dat']]
    [print('±5 %', k['chi_so'], k['gia_tri']) for k in kiem if k['trong_5pct']]


if __name__ == '__main__': main()
