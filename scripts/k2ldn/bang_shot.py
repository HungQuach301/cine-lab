#!/opt/cine/bin/python
"""TIEN-KY-T4 · BẢNG SHOT v1 — sinh channel-k2/k2c-t4-02/BANG-SHOT-v1.{json,md} từ đặc tả dưới + kiểm trần (§15 (d), §17, §11.1, lệnh 23/10) và luật cú máy đề xuất (§19 (a)).
Lớp (giây trong shot; có thể chồng): A = cách A three.js · B = Cycles GPU · N2P = tấm nền N2+ (chỉ shot máy cố định) · MD = minh hoạ M-d (Omni) ·
MAP = bản đồ cổ hoạt hoá · MAP3D = 3D kiểu bản đồ · KHAC = tranh khắc chồng cảnh · THE = thẻ nhân vật/bộ đếm · TL = tư liệu ảnh/bản in · PP = thẻ phương pháp."""
import json, os, collections
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# điểm máy xương sống (EPSG:27700; h = m trên ODN) — vị trí đo trên OSM 2026
DM = {
 'P1': {'ten': 'BANKSIDE-CAO (điểm xương sống chính, T4-G3; ≈ quán bia Pepys đối diện Three Cranes)', 'p': [532330, 180250, 230], 'l': [532420, 180980, 15], 'fov': 50, 'cao': True},
 'P2': {'ten': "ST-SAVIOUR (tháp Southwark Cathedral — góc Hollar 1647)", 'p': [532690, 180290, 70], 'l': [532300, 180900, 20], 'fov': 55, 'cao': True},
 'P3': {'ten': 'PUDDING-LANE / ĐỈNH MONUMENT (61 m) nhìn tây', 'p': [532990, 180750, 80], 'l': [532100, 181130, 40], 'fov': 50, 'cao': True},
 'P4': {'ten': 'FLEET-STREET / LUDGATE (trục nhìn đông lên mái vòm — tầm nhìn Leadenhall)', 'p': [531300, 181160, 40], 'l': [532100, 181140, 60], 'fov': 35, 'cao': False},
 'P5': {'ten': 'CRIPPLEGATE-CAO (bắc nhìn nam ra sông)', 'p': [532300, 181900, 260], 'l': [532350, 180800, 0], 'fov': 50, 'cao': True},
 'P6': {'ten': 'SÔNG-CẦU (giữa sông phía đông cầu London, thấp 35 m, nhìn tây)', 'p': [533250, 180480, 35], 'l': [532300, 180850, 30], 'fov': 45, 'cao': False},
 'P7': {'ten': 'THIÊN-ĐỈNH (nhìn thẳng xuống City — chuyển bản đồ ↔ 3D cùng toạ độ)', 'p': [532350, 180950, 2200], 'l': [532350, 180951, 0], 'fov': 40, 'cao': True},
 'P8': {'ten': 'TOWER-HILL (đông nhìn tây dọc Tower Street)', 'p': [533800, 180600, 120], 'l': [532900, 180800, 10], 'fov': 50, 'cao': True},
}
LOAI = {'CODINH': 'cố định/trôi ≤ 2 %/s', 'DAY': 'đẩy vào chậm', 'KEO': 'kéo lùi lộ cảnh', 'CAU': 'cần cẩu lên/xuống', 'VONG': 'vòng cung ≤ 30–45°', 'TRUOT': 'trượt ngang có tiền cảnh',
        'NGHIENG': 'nghiêng lộ cảnh', 'THAP': 'góc thấp anh hùng', 'XUONG': 'nhìn thẳng xuống → xiên', 'LAN': 'cú lặn (§14.3)', 'KHOP': 'khớp cắt cùng khung khác năm', 'MD': 'minh hoạ M-d (máy tầm người)', 'PP': 'thẻ phương pháp'}
# (mã, phần, giây, câu lời, điểm máy, loại, mốc, vai truyện, {lớp: giây}, ghi chú)
S = [
 ('M01', 'MÓC', 12, 'L01–L03', 'P1', 'CODINH', '2026 14:00 → 21:30', 'nhận ra nơi chốn: ngày → đêm từ giây 0 (TL-5, §14.7)', {'A': 12, 'N2P': 12}, 'hai tấm nền ngày/đêm hoà ≥ 2 s; cửa sổ sáng theo giờ'),
 ('M02', 'MÓC', 8, 'L04–L05', 'P1', 'KEO', '2026 → 1666 (tua ngược)', 'luận đề: toà cao lún xuống, mái vòm tan, Old St Paul\'s hiện lại', {'A': 8}, 'thời gian chạy suốt cú máy'),
 ('M03', 'MÓC', 11, 'L06 + lặng 3 s', 'P1', 'DAY', '2/9/1666 21:00 → 22:30', 'KHOẢNH KHẮC GIÁ TRỊ NHẤT ≤ 30 s: "one entire arch of fire" nhìn từ chỗ Pepys đứng', {'B': 11}, 'Cycles hay A theo kết luận T1'),
 ('M04', 'MÓC', 12, 'L07', 'P3', 'LAN', '2/9/1666 00:50 (tua lại trước lửa)', 'cú lặn từ cao xuống Pudding Lane — "a bakery about a kilometre from here"', {'B': 12}, 'cú lặn đêm = Cycles (§14.2)'),
 ('H1-01', 'HỒI 1', 8, 'L08', '—', 'MD', '2/9 01:00', 'M-d (1) Pudding Lane 01:00 — đốm lửa trong lò bánh', {'MD': 8, 'THE': 4}, 'kẹp giữa M04 và H1-02 (§15 f); thẻ Farriner'),
 ('H1-02', 'HỒI 1', 12, 'L09–L10', 'P6', 'CODINH', '2/9 01:00 → 07:00', 'lửa lớn dần ở chân cầu; nhà gỗ sát nhau; gió đông (khói sang tây)', {'A': 12, 'N2P': 12}, 'tấm nền N2+ đêm → bình minh'),
 ('H1-03', 'HỒI 1', 10, 'L11', 'P2', 'TRUOT', '1647 → 1666', 'Hollar vẽ từ St Saviour\'s: tranh khắc hoà vào 3D cùng góc (chú thích ≤ 6 từ thay thẻ)', {'A': 10, 'KHAC': 6}, 'Met 360649/56.581.8 (CC0) nếu Long View chưa xác nhận PD'),
 ('H1-04', 'HỒI 1', 12, 'L12–L13', 'P2', 'CODINH', '2/9 07:00 → 12:00', 'St Magnus + Fish Street cháy; tới Steelyard trưa', {'A': 12, 'N2P': 12}, ''),
 ('H1-05', 'HỒI 1', 8, 'L14', '—', 'MD', '2/9 sáng', 'M-d (2) bờ sông gần cầu: ném đồ xuống sà lan', {'MD': 8}, 'kẹp giữa H1-04 và H1-06 cùng giờ'),
 ('H1-06', 'HỒI 1', 12, 'L15–L16', 'P5', 'CAU', '2/9 12:00 → 17:00', 'Pepys gặp Thị trưởng ở Cannon Street; lửa vượt sức phá nhà', {'A': 12, 'THE': 6}, 'thẻ Pepys + Bludworth (3 + 3 s)'),
 ('H1-07', 'HỒI 1', 8, 'L17–L18', 'P2', 'VONG', '2/9 17:00', 'khoảng trống 1633 trên cầu chặn lửa sang Southwark; gió đẩy lửa sang tây', {'A': 8}, 'vòng 30° quanh tháp St Saviour\'s'),
 ('H1-08', 'HỒI 1', 16, 'L19–L20 + lặng 3 s', 'P1', 'CODINH', '2/9 18:00 → 22:00', 'Pepys ở quán bia Bankside: chạng vạng → vòng cung lửa', {'A': 16, 'N2P': 16}, 'cùng khung M03 (điểm tái xuất)'),
 ('H1-09', 'HỒI 1', 14, 'L21–L22', 'P7', 'XUONG', '2/9 → 4/9', 'BẢN ĐỒ CỔ HOẠT HOÁ: Doornick 1666, lửa lan theo ngày, chuyển 3D cùng toạ độ', {'MAP': 9, 'MAP3D': 5}, 'thử T2; ≤ 3 tên nơi'),
 ('H1-10', 'HỒI 1', 8, 'L23', '—', 'MD', '3/9', 'M-d (4) Watling Street: xe, người khiêng, người bệnh', {'MD': 8}, ''),
 ('H1-11', 'HỒI 1', 12, 'L24', 'P8', 'CODINH', '3/9 14:00 → 23:00', 'Royal Exchange cháy; trời "như miệng lò"', {'A': 12, 'N2P': 12, 'THE': 4}, 'thẻ Evelyn'),
 ('H1-12', 'HỒI 1', 8, 'L23 (sông)', '—', 'MD', '3/9 đêm', 'M-d (3) Thames: sà lan, đồ trôi, bờ bắc rực lửa', {'MD': 8}, ''),
 ('H1-13', 'HỒI 1', 16, 'L25–L26', 'P4', 'THAP', '4/9 18:00 → 21:00', "lửa leo đồi Ludgate tới Old St Paul's có giàn giáo; nhà thờ bốc cháy", {'B': 16}, 'cận đêm lửa = Cycles'),
 ('H1-14', 'HỒI 1', 7, 'L26 (chì)', '—', 'MD', '4/9 đêm', 'M-d (5) chì chảy quanh St Paul\'s', {'MD': 7}, ''),
 ('H1-15', 'HỒI 1', 12, 'L27–L29', 'P8', 'CAU', '4/9 20:00 → 23:00', 'nổ nhà bằng thuốc súng ở Tower Street (lớp a, render); Pepys chôn rượu + phô mai', {'A': 12}, 'nổ nhà là lớp (a) — KHÔNG giao AI (LUAT b34) → §15 f (6) đề xuất đổi'),
 ('H1-16', 'HỒI 1', 10, 'L30–L31', 'P1', 'CODINH', '4/9 22:00 → 6/9', 'gió dịu; lửa tàn; bình minh 5/9', {'A': 10, 'N2P': 10}, ''),
 ('H1-17', 'HỒI 1', 7, 'L32', '—', 'MD', '5/9', 'M-d (7) Moorfields: lều, chòi, đống đồ', {'MD': 7}, ''),
 ('H1-18', 'HỒI 1', 9, 'L33–L34 + lặng', 'P7', 'XUONG', '7/9', 'phế tích bốc khói: ranh vùng cháy + bộ đếm 13 200 nhà / 87 nhà thờ', {'A': 9, 'MAP3D': 5, 'THE': 3}, 'bộ đếm §17 (3)'),
 ('H1-19', 'HỒI 1', 6, '(lặng)', '—', 'MD', '7/9', 'M-d (8) phế tích bốc khói', {'MD': 6}, ''),
 ('H2-01', 'HỒI 2', 10, 'L35', 'P3', 'LAN', '9/1666', 'Evelyn đi trên phế tích: chỉ nhận ra nơi nhờ tháp còn đứng', {'B': 10}, 'cú lặn ngày'),
 ('H2-02', 'HỒI 2', 12, 'L36–L38', 'P7', 'XUONG', '9/1666', 'phương án Wren (bản in LoC 1767) đặt khớp lên City cháy — không được dựng', {'A': 4, 'TL': 8, 'MAP3D': 4, 'THE': 4}, 'thẻ Wren (NGA)'),
 ('H2-03', 'HỒI 2', 12, 'L39–L40', 'P5', 'CODINH', '1667', 'lô đất rối; Toà Cháy ở Clifford\'s Inn (vùng không cháy)', {'A': 12, 'N2P': 12}, ''),
 ('H2-04', 'HỒI 2', 12, 'L41–L42', 'P4', 'TRUOT', '1667–1668', 'Rebuilding Act: tường gạch, 4 hạng nhà theo hạng phố', {'A': 12}, 'trượt dọc Fleet Street, tiền cảnh mái'),
 ('H2-05', 'HỒI 2', 14, 'L43–L45', 'P1', 'CODINH', '1668 → 1671', 'timelapse xây lại bằng gạch trên đúng lô cũ (≈ 6 000 nhà cuối 1670)', {'A': 14, 'N2P': 14, 'THE': 3}, 'thẻ Hooke'),
 ('H2-06', 'HỒI 2', 12, 'L46', 'P3', 'VONG', '1671 → 1677', 'Monument mọc; vạch 202 ft nối tới lò bánh Pudding Lane', {'A': 12, 'THE': 2}, 'bộ đếm "202 ft"'),
 ('H2-07', 'HỒI 2', 8, 'L47', 'P8', 'CODINH', '1680', 'Barbon lập Fire Office — dấu bảo hiểm trên mặt nhà [vật minh hoạ: cần kiểm]', {'A': 8, 'THE': 4}, 'thẻ Barbon'),
 ('H2-08', 'HỒI 2', 12, 'L48', 'P2', 'NGHIENG', '1670 → 1700', 'chóp nhà thờ Wren trắng mọc quanh City', {'A': 12, 'KHAC': 4}, 'tranh khắc Monument (Rijks) góc khung'),
 ('H2-09', 'HỒI 2', 12, 'L49', 'P1', 'CODINH', '1675 → 1708', "St Paul's mới mọc từ nền Old St Paul's", {'A': 12, 'N2P': 12}, ''),
 ('H2-10', 'HỒI 2', 10, 'L50 + lặng 4 s', 'P4', 'THAP', '1708 → 1711', 'đèn lồng hoàn tất; 365 ft — mái vòm anh hùng giờ vàng', {'B': 10}, ''),
 ('H2-11', 'HỒI 2', 10, '(nối)', 'P7', 'XUONG', '1676', 'Ogilby & Morgan 1676 đặt trùng lưới phố 1666: cùng tuyến phố', {'MAP': 10}, 'rủi ro VỪA (BL Crace qua Commons PD) — chờ xác nhận'),
 ('H2-12', 'HỒI 2', 12, '(lặng/nhạc)', 'P2', 'KHOP', '1647 ↔ 1711', 'then–now: khung Hollar ↔ cùng khung 1711', {'A': 12, 'KHAC': 3}, 'khớp cắt cùng khung'),
 ('H2-13', 'HỒI 2', 10, '(nối)', 'P8', 'TRUOT', '1711', 'từ phía đông: City gạch + mái vòm, sông có thuyền tiền cảnh', {'A': 10}, ''),
 ('H2-14', 'HỒI 2', 12, '(nối)', 'P5', 'CAU', '1700 → 1711', 'cần cẩu hạ: City gạch đã kín lô, mái vòm hoàn tất', {'A': 12}, ''),
 ('H3-01', 'HỒI 3', 14, 'L51–L53', 'P1', 'CODINH', '1711 → 1860', 'mái vòm cao nhất > 250 năm; chóp Wren', {'A': 14, 'N2P': 14}, ''),
 ('H3-02', 'HỒI 3', 10, 'L52', 'P6', 'TRUOT', '1757 → 1832', 'nhà trên cầu dỡ (1761); cầu mới 1831', {'A': 10}, ''),
 ('H3-03', 'HỒI 3', 14, 'L54–L55', 'P7', 'XUONG', '1860 → 1871', 'Victoria Embankment đẩy bờ bắc ra sông (bờ 1666 ↔ 2026)', {'A': 10, 'MAP3D': 4}, ''),
 ('H3-04', 'HỒI 3', 12, 'L56–L57', 'P5', 'CODINH', '1900 → 1937', 'toà văn phòng chen quanh nhà thờ; phố bên dưới không đổi', {'A': 12, 'N2P': 12}, ''),
 ('H3-05', 'HỒI 3', 10, 'L58', 'P4', 'THAP', '1937–1938', 'St Paul\'s Heights: mặt phẳng trần cao độ hiện mờ quanh mái vòm', {'A': 10, 'THE': 4}, 'thẻ Godfrey Allen'),
 ('H3-06', 'HỒI 3', 12, '(nối)', 'P1', 'KHOP', '1938 ↔ 1666', 'cùng khung Bankside: 1938 ↔ 1666', {'A': 12}, ''),
 ('H4-01', 'HỒI 4', 12, 'L59–L60', 'P1', 'CODINH', '29/12/1940 15:30 → 18:15', 'chạng vạng mùa đông; Chủ nhật', {'A': 12, 'N2P': 12}, ''),
 ('H4-02', 'HỒI 4', 14, 'L61–L62', 'P5', 'CAU', '29/12 18:15 → 21:00', 'bom cháy rơi thành tia; ≈ 1 500 đám cháy; bộ đếm 100 000', {'A': 14, 'THE': 3}, ''),
 ('H4-03', 'HỒI 4', 8, 'L63–L64', 'P6', 'TRUOT', '29/12 21:00', 'triều thấp: bãi bùn, vòi rồng không tới nước [cần kiểm]', {'A': 8}, ''),
 ('H4-04', 'HỒI 4', 16, 'L65–L67', 'P4', 'THAP', '29/12 22:00 → 23:30', "KHOẢNH KHẮC MÁI VÒM giữa khói lửa (dựng 3D thay ảnh Mason — T4-G1); Paternoster Row cháy", {'B': 16}, 'Cycles GPU'),
 ('H4-05', 'HỒI 4', 8, 'L68', 'P1', 'DAY', '30/12 07:00', 'sáng ra: mái vòm còn đứng; 1 ảnh MOI 1940 (Crown PD) góc khung', {'A': 8, 'TL': 6}, 'ảnh MOI chưa chốt (việc 5)'),
 ('H4-06', 'HỒI 4', 14, 'L69–L70 + lặng 4 s', 'P1', 'CODINH', '30/12/1940 → 1941', 'vòng phế tích quanh mái vòm; bộ đếm 160', {'A': 14, 'N2P': 14, 'THE': 2}, ''),
 ('H4-07', 'HỒI 4', 16, 'L71', 'P7', 'XUONG', '1941', 'vùng bom nặng Cripplegate / Paternoster (ước lượng — KHÔNG dùng LCC Bomb Damage Maps)', {'A': 10, 'MAP3D': 6}, 'ranh 1940 chưa có nguồn mở → bậc 5'),
 ('H4-08', 'HỒI 4', 20, '(lặng/nhạc)', 'P2', 'KHOP', '1666 ↔ 1941', 'hai khoảng trống cùng một khung', {'A': 20}, 'chia 2 góc (R3)'),
 ('H5-01', 'HỒI 5', 12, 'L72–L73', 'P5', 'CODINH', '1946 → 1951', 'Holden–Holford: quy hoạch lại vùng bom', {'A': 12, 'N2P': 12, 'THE': 4}, 'thẻ Holden + Holford'),
 ('H5-02', 'HỒI 5', 16, 'L74', 'P5', 'CAU', '1957 → 1976', 'London Wall (Route 11) + Barbican mọc trên Cripplegate', {'A': 16}, ''),
 ('H5-03', 'HỒI 5', 12, 'L75', 'P7', 'XUONG', '1666 ↔ 2026', 'lưới phố Doornick 1666 chồng lên 3D 2026: cùng tuyến', {'MAP': 8, 'MAP3D': 4}, ''),
 ('H5-04', 'HỒI 5', 14, 'L76–L78', 'P1', 'CODINH', '1980 → 2026', 'cụm toà cao phía đông mọc lên', {'A': 14, 'N2P': 14}, ''),
 ('H5-05', 'HỒI 5', 14, 'L79–L82', 'P4', 'THAP', '2026 17:30', 'từ Fleet Street: Leadenhall vát — mái vòm còn nền trời', {'A': 14}, ''),
 ('H5-06', 'HỒI 5', 12, '(nối)', 'P3', 'VONG', '2026 18:30', 'vòng 30° quanh mái vòm từ phía đông', {'A': 12}, ''),
 ('H5-07', 'HỒI 5', 20, 'L83–L86', 'P1', 'KHOP', '2/9/1666 22:00 ↔ 2026 22:00', 'KHÉP VÒNG: cùng khung Bankside — vòng cung lửa ↔ đèn City', {'B': 10, 'A': 10}, 'chia 2 góc: B (1666) / A (2026)'),
 ('H5-08', 'HỒI 5', 28, '(nhạc + lặng 6 s)', 'P1', 'KEO', '2026 đêm', 'kéo lùi cuối: mái vòm giữa toà cao', {'A': 28}, ''),
 ('H5-09', 'HỒI 5', 16, '—', '—', 'PP', '—', 'hai thẻ "How this film was made" × 8 s (§12.1 b)', {'PP': 16}, ''),
]
CAP = {'AI': 70, 'N2P': 50, 'MD': 20, 'MAP_ALL': 12, 'TL_KHAC_THE': 10, 'B': 20}
def main():
    rows, t = [], 0.0
    for (ma, phan, dur, loi, dm, loai, moc, vai, lop, ghi) in S:
        rows.append({'ma': ma, 'phan': phan, 'bat_dau_s': t, 'giay': dur, 'loi': loi, 'diem_may': dm, 'may': DM.get(dm), 'loai_may': loai, 'moc': moc, 'vai': vai, 'lop': lop, 'ghi_chu': ghi}); t += dur
    T = t; L = collections.Counter()
    for r in rows:
        for k, v in r['lop'].items(): L[k] += v
    pct = {k: round(100 * v / T, 2) for k, v in L.items()}
    tong = {'thoi_luong_s': T, 'lop_s': dict(L), 'lop_pct': pct,
            'AI_pct': round(100 * (L['N2P'] + L['MD']) / T, 2), 'MAP_ALL_pct': round(100 * (L['MAP'] + L['MAP3D']) / T, 2),
            'TL_KHAC_THE_pct': round(100 * (L['TL'] + L['KHAC'] + L['THE']) / T, 2), 'B_pct': pct.get('B', 0), 'N2P_pct': pct.get('N2P', 0), 'MD_pct': pct.get('MD', 0)}
    kiem = []
    for k, cap in (('AI_pct', CAP['AI']), ('N2P_pct', CAP['N2P']), ('MD_pct', CAP['MD']), ('MAP_ALL_pct', CAP['MAP_ALL']), ('TL_KHAC_THE_pct', CAP['TL_KHAC_THE']), ('B_pct', CAP['B'])):
        v = tong[k]; kiem.append({'chi_so': k, 'gia_tri': v, 'tran': cap, 'dat': v <= cap, 'trong_5pct': abs(v - cap) <= 0.05 * cap})
    # N2+ chỉ trên shot máy cố định
    kiem.append({'chi_so': 'N2P_chi_codinh', 'dat': all(r['loai_may'] == 'CODINH' for r in rows if 'N2P' in r['lop'])})
    kiem.append({'chi_so': 'N2P_va_MD_khong_chong', 'dat': all(not ('N2P' in r['lop'] and 'MD' in r['lop']) for r in rows)})
    kiem.append({'chi_so': 'MAP_moi_lan_le_10s', 'dat': all(r['lop'].get('MAP', 0) <= 10 for r in rows)})
    # luật cú máy đề xuất §19 (a): mỗi chương ≥ 4 loại; ≤ 2 shot liền cùng loại; điểm xương sống tái xuất mỗi hồi
    by = collections.defaultdict(list)
    for r in rows: by[r['phan']].append(r)
    for ph, rs in by.items():
        loai = {r['loai_may'] for r in rs if r['loai_may'] not in ('MD', 'PP')}
        run, mx = 1, 1
        for a, b in zip(rs, rs[1:]):
            run = run + 1 if a['loai_may'] == b['loai_may'] else 1; mx = max(mx, run)
        kiem.append({'chi_so': f'{ph}: số loại cú máy ≥ 4', 'gia_tri': len(loai), 'dat': len(loai) >= 4 or ph == 'MÓC'})
        kiem.append({'chi_so': f'{ph}: chuỗi cùng loại ≤ 2', 'gia_tri': mx, 'dat': mx <= 2})
        kiem.append({'chi_so': f'{ph}: P1 tái xuất', 'dat': any(r['diem_may'] == 'P1' for r in rs) or ph == 'HỒI 1'})
    cao = sum(r['giay'] for r in rows if r['may'] and r['may']['cao'] and r['loai_may'] not in ('MD',))
    tong['goc_cao_pct'] = round(100 * cao / T, 2); tong['so_shot'] = len(rows); tong['shot_tb_s'] = round(T / len(rows), 2)
    kiem.append({'chi_so': 'TL-1: góc cao/toàn cảnh có thời gian chạy ≥ 75 %', 'gia_tri': tong['goc_cao_pct'], 'dat': tong['goc_cao_pct'] >= 75, 'ghi': 'TL-1 sẽ được thay bằng luật §19 (a) nếu chủ dự án duyệt'})
    out = {'tap': 'K2C-T4-02', 'phien': 'TIEN-KY-T4', 'ngay': '2026-10-23', 'diem_may': DM, 'loai_may': LOAI, 'shot': rows, 'tong': tong, 'kiem': kiem}
    json.dump(out, open(os.path.join(REPO, 'channel-k2/k2c-t4-02/BANG-SHOT-v1.json'), 'w'), ensure_ascii=False, indent=1)
    md = ['# BẢNG SHOT v1 — K2C-T4-02 London (TIEN-KY-T4, 23/10/2026) — NHÁP, chờ G1', '',
          '> Sinh bằng `scripts/k2ldn/bang_shot.py` (nguồn thật của bảng; sửa ở đó rồi chạy lại). Bản máy đọc: `BANG-SHOT-v1.json`. Thời điểm theo lời nháp v1 (1 593 từ + nhịp lặng).',
          '> Lớp: A cách A · B Cycles GPU · N2P tấm nền N2+ · MD minh hoạ M-d · MAP bản đồ cổ hoạt hoá · MAP3D 3D kiểu bản đồ · KHAC tranh khắc · THE thẻ nhân vật/bộ đếm · TL tư liệu · PP thẻ phương pháp. Số trong ngoặc = giây.', '',
          '## Điểm máy xương sống', '', '| Mã | Tên | Vị trí E, N, h (m) | Nhìn tới | FOV dọc |', '|---|---|---|---|---|']
    for k, v in DM.items(): md.append(f"| {k} | {v['ten']} | {v['p']} | {v['l']} | {v['fov']}° |")
    md += ['', '## Bảng', '', '| Mã | t (s) | Dài | Lời | Điểm máy | Cú máy | Mốc | Vai truyện | Lớp | Ghi chú |', '|---|---|---|---|---|---|---|---|---|---|']
    for r in rows:
        m, s_ = divmod(r['bat_dau_s'], 60)
        md.append(f"| {r['ma']} | {int(m)}:{s_:04.1f} | {r['giay']} | {r['loi']} | {r['diem_may']} | {r['loai_may']} | {r['moc']} | {r['vai']} | {', '.join(f'{k} ({v})' for k, v in r['lop'].items())} | {r['ghi_chu']} |")
    md += ['', '## Tổng + kiểm trần', '', f"- Thời lượng **{T:.0f} s** · **{len(rows)} shot** · shot trung bình {tong['shot_tb_s']} s · góc cao/toàn cảnh {tong['goc_cao_pct']} %.",
           f"- Lớp (s): {dict(L)}", '', '| Chỉ số | Giá trị | Trần | Đạt | Trong ±5 % quanh ngưỡng |', '|---|---|---|---|---|']
    for k in kiem: md.append(f"| {k['chi_so']} | {k.get('gia_tri', '')} | {k.get('tran', '')} | {'ĐẠT' if k['dat'] else '**TRƯỢT**'} | {('**CÓ**' if k.get('trong_5pct') else 'không') if 'tran' in k else ''} |")
    open(os.path.join(REPO, 'channel-k2/k2c-t4-02/BANG-SHOT-v1.md'), 'w').write('\n'.join(md) + '\n')
    print(json.dumps(tong, ensure_ascii=False)); [print(k) for k in kiem if not k['dat']]
if __name__ == '__main__': main()
