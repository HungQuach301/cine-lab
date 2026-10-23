# BẢNG SHOT v1 — K2C-T4-02 London (TIEN-KY-T4, 23/10/2026) — NHÁP, chờ G1

> Sinh bằng `scripts/k2ldn/bang_shot.py` (nguồn thật của bảng; sửa ở đó rồi chạy lại). Bản máy đọc: `BANG-SHOT-v1.json`. Thời điểm theo lời nháp v1 (1 593 từ + nhịp lặng).
> Lớp: A cách A · B Cycles GPU · N2P tấm nền N2+ · MD minh hoạ M-d · MAP bản đồ cổ hoạt hoá · MAP3D 3D kiểu bản đồ · KHAC tranh khắc · THE thẻ nhân vật/bộ đếm · TL tư liệu · PP thẻ phương pháp. Số trong ngoặc = giây.

## Điểm máy xương sống

| Mã | Tên | Vị trí E, N, h (m) | Nhìn tới | FOV dọc |
|---|---|---|---|---|
| P1 | BANKSIDE-CAO (điểm xương sống chính, T4-G3; ≈ quán bia Pepys đối diện Three Cranes) | [532330, 180250, 230] | [532420, 180980, 15] | 50° |
| P2 | ST-SAVIOUR (tháp Southwark Cathedral — góc Hollar 1647) | [532690, 180290, 70] | [532300, 180900, 20] | 55° |
| P3 | PUDDING-LANE / ĐỈNH MONUMENT (61 m) nhìn tây | [532990, 180750, 80] | [532100, 181130, 40] | 50° |
| P4 | FLEET-STREET / LUDGATE (trục nhìn đông lên mái vòm — tầm nhìn Leadenhall) | [531300, 181160, 40] | [532100, 181140, 60] | 35° |
| P5 | CRIPPLEGATE-CAO (bắc nhìn nam ra sông) | [532300, 181900, 260] | [532350, 180800, 0] | 50° |
| P6 | SÔNG-CẦU (giữa sông phía đông cầu London, thấp 35 m, nhìn tây) | [533250, 180480, 35] | [532300, 180850, 30] | 45° |
| P7 | THIÊN-ĐỈNH (nhìn thẳng xuống City — chuyển bản đồ ↔ 3D cùng toạ độ) | [532350, 180950, 2200] | [532350, 180951, 0] | 40° |
| P8 | TOWER-HILL (đông nhìn tây dọc Tower Street) | [533800, 180600, 120] | [532900, 180800, 10] | 50° |

## Bảng

| Mã | t (s) | Dài | Lời | Điểm máy | Cú máy | Mốc | Vai truyện | Lớp | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|
| M01 | 0:00.0 | 12 | L01–L03 | P1 | CODINH | 2026 14:00 → 21:30 | nhận ra nơi chốn: ngày → đêm từ giây 0 (TL-5, §14.7) | A (12), N2P (12) | hai tấm nền ngày/đêm hoà ≥ 2 s; cửa sổ sáng theo giờ |
| M02 | 0:12.0 | 8 | L04–L05 | P1 | KEO | 2026 → 1666 (tua ngược) | luận đề: toà cao lún xuống, mái vòm tan, Old St Paul's hiện lại | A (8) | thời gian chạy suốt cú máy |
| M03 | 0:20.0 | 11 | L06 + lặng 3 s | P1 | DAY | 2/9/1666 21:00 → 22:30 | KHOẢNH KHẮC GIÁ TRỊ NHẤT ≤ 30 s: "one entire arch of fire" nhìn từ chỗ Pepys đứng | B (11) | Cycles hay A theo kết luận T1 |
| M04 | 0:31.0 | 12 | L07 | P3 | LAN | 2/9/1666 00:50 (tua lại trước lửa) | cú lặn từ cao xuống Pudding Lane — "a bakery about a kilometre from here" | B (12) | cú lặn đêm = Cycles (§14.2) |
| H1-01 | 0:43.0 | 8 | L08 | — | MD | 2/9 01:00 | M-d (1) Pudding Lane 01:00 — đốm lửa trong lò bánh | MD (8), THE (4) | kẹp giữa M04 và H1-02 (§15 f); thẻ Farriner |
| H1-02 | 0:51.0 | 12 | L09–L10 | P6 | CODINH | 2/9 01:00 → 07:00 | lửa lớn dần ở chân cầu; nhà gỗ sát nhau; gió đông (khói sang tây) | A (12), N2P (12) | tấm nền N2+ đêm → bình minh |
| H1-03 | 1:03.0 | 10 | L11 | P2 | TRUOT | 1647 → 1666 | Hollar vẽ từ St Saviour's: tranh khắc hoà vào 3D cùng góc (chú thích ≤ 6 từ thay thẻ) | A (10), KHAC (6) | Met 360649/56.581.8 (CC0) nếu Long View chưa xác nhận PD |
| H1-04 | 1:13.0 | 12 | L12–L13 | P2 | CODINH | 2/9 07:00 → 12:00 | St Magnus + Fish Street cháy; tới Steelyard trưa | A (12), N2P (12) |  |
| H1-05 | 1:25.0 | 8 | L14 | — | MD | 2/9 sáng | M-d (2) bờ sông gần cầu: ném đồ xuống sà lan | MD (8) | kẹp giữa H1-04 và H1-06 cùng giờ |
| H1-06 | 1:33.0 | 12 | L15–L16 | P5 | CAU | 2/9 12:00 → 17:00 | Pepys gặp Thị trưởng ở Cannon Street; lửa vượt sức phá nhà | A (12), THE (6) | thẻ Pepys + Bludworth (3 + 3 s) |
| H1-07 | 1:45.0 | 8 | L17–L18 | P2 | VONG | 2/9 17:00 | khoảng trống 1633 trên cầu chặn lửa sang Southwark; gió đẩy lửa sang tây | A (8) | vòng 30° quanh tháp St Saviour's |
| H1-08 | 1:53.0 | 16 | L19–L20 + lặng 3 s | P1 | CODINH | 2/9 18:00 → 22:00 | Pepys ở quán bia Bankside: chạng vạng → vòng cung lửa | A (16), N2P (16) | cùng khung M03 (điểm tái xuất) |
| H1-09 | 2:09.0 | 14 | L21–L22 | P7 | XUONG | 2/9 → 4/9 | BẢN ĐỒ CỔ HOẠT HOÁ: Doornick 1666, lửa lan theo ngày, chuyển 3D cùng toạ độ | MAP (9), MAP3D (5) | thử T2; ≤ 3 tên nơi |
| H1-10 | 2:23.0 | 8 | L23 | — | MD | 3/9 | M-d (4) Watling Street: xe, người khiêng, người bệnh | MD (8) |  |
| H1-11 | 2:31.0 | 12 | L24 | P8 | CODINH | 3/9 14:00 → 23:00 | Royal Exchange cháy; trời "như miệng lò" | A (12), N2P (12), THE (4) | thẻ Evelyn |
| H1-12 | 2:43.0 | 8 | L23 (sông) | — | MD | 3/9 đêm | M-d (3) Thames: sà lan, đồ trôi, bờ bắc rực lửa | MD (8) |  |
| H1-13 | 2:51.0 | 16 | L25–L26 | P4 | THAP | 4/9 18:00 → 21:00 | lửa leo đồi Ludgate tới Old St Paul's có giàn giáo; nhà thờ bốc cháy | B (16) | cận đêm lửa = Cycles |
| H1-14 | 3:07.0 | 7 | L26 (chì) | — | MD | 4/9 đêm | M-d (5) chì chảy quanh St Paul's | MD (7) |  |
| H1-15 | 3:14.0 | 12 | L27–L29 | P8 | CAU | 4/9 20:00 → 23:00 | nổ nhà bằng thuốc súng ở Tower Street (lớp a, render); Pepys chôn rượu + phô mai | A (12) | nổ nhà là lớp (a) — KHÔNG giao AI (LUAT b34) → §15 f (6) đề xuất đổi |
| H1-16 | 3:26.0 | 10 | L30–L31 | P1 | CODINH | 4/9 22:00 → 6/9 | gió dịu; lửa tàn; bình minh 5/9 | A (10), N2P (10) |  |
| H1-17 | 3:36.0 | 7 | L32 | — | MD | 5/9 | M-d (7) Moorfields: lều, chòi, đống đồ | MD (7) |  |
| H1-18 | 3:43.0 | 9 | L33–L34 + lặng | P7 | XUONG | 7/9 | phế tích bốc khói: ranh vùng cháy + bộ đếm 13 200 nhà / 87 nhà thờ | A (9), MAP3D (5), THE (3) | bộ đếm §17 (3) |
| H1-19 | 3:52.0 | 6 | (lặng) | — | MD | 7/9 | M-d (8) phế tích bốc khói | MD (6) |  |
| H2-01 | 3:58.0 | 10 | L35 | P3 | LAN | 9/1666 | Evelyn đi trên phế tích: chỉ nhận ra nơi nhờ tháp còn đứng | B (10) | cú lặn ngày |
| H2-02 | 4:08.0 | 12 | L36–L38 | P7 | XUONG | 9/1666 | phương án Wren (bản in LoC 1767) đặt khớp lên City cháy — không được dựng | A (4), TL (8), MAP3D (4), THE (4) | thẻ Wren (NGA) |
| H2-03 | 4:20.0 | 12 | L39–L40 | P5 | CODINH | 1667 | lô đất rối; Toà Cháy ở Clifford's Inn (vùng không cháy) | A (12), N2P (12) |  |
| H2-04 | 4:32.0 | 12 | L41–L42 | P4 | TRUOT | 1667–1668 | Rebuilding Act: tường gạch, 4 hạng nhà theo hạng phố | A (12) | trượt dọc Fleet Street, tiền cảnh mái |
| H2-05 | 4:44.0 | 14 | L43–L45 | P1 | CODINH | 1668 → 1671 | timelapse xây lại bằng gạch trên đúng lô cũ (≈ 6 000 nhà cuối 1670) | A (14), N2P (14), THE (3) | thẻ Hooke |
| H2-06 | 4:58.0 | 12 | L46 | P3 | VONG | 1671 → 1677 | Monument mọc; vạch 202 ft nối tới lò bánh Pudding Lane | A (12), THE (2) | bộ đếm "202 ft" |
| H2-07 | 5:10.0 | 8 | L47 | P8 | CODINH | 1680 | Barbon lập Fire Office — dấu bảo hiểm trên mặt nhà [vật minh hoạ: cần kiểm] | A (8), THE (4) | thẻ Barbon |
| H2-08 | 5:18.0 | 12 | L48 | P2 | NGHIENG | 1670 → 1700 | chóp nhà thờ Wren trắng mọc quanh City | A (12), KHAC (4) | tranh khắc Monument (Rijks) góc khung |
| H2-09 | 5:30.0 | 12 | L49 | P1 | CODINH | 1675 → 1708 | St Paul's mới mọc từ nền Old St Paul's | A (12), N2P (12) |  |
| H2-10 | 5:42.0 | 10 | L50 + lặng 4 s | P4 | THAP | 1708 → 1711 | đèn lồng hoàn tất; 365 ft — mái vòm anh hùng giờ vàng | B (10) |  |
| H2-11 | 5:52.0 | 10 | (nối) | P7 | XUONG | 1676 | Ogilby & Morgan 1676 đặt trùng lưới phố 1666: cùng tuyến phố | MAP (10) | rủi ro VỪA (BL Crace qua Commons PD) — chờ xác nhận |
| H2-12 | 6:02.0 | 12 | (lặng/nhạc) | P2 | KHOP | 1647 ↔ 1711 | then–now: khung Hollar ↔ cùng khung 1711 | A (12), KHAC (3) | khớp cắt cùng khung |
| H2-13 | 6:14.0 | 10 | (nối) | P8 | TRUOT | 1711 | từ phía đông: City gạch + mái vòm, sông có thuyền tiền cảnh | A (10) |  |
| H2-14 | 6:24.0 | 12 | (nối) | P5 | CAU | 1700 → 1711 | cần cẩu hạ: City gạch đã kín lô, mái vòm hoàn tất | A (12) |  |
| H3-01 | 6:36.0 | 14 | L51–L53 | P1 | CODINH | 1711 → 1860 | mái vòm cao nhất > 250 năm; chóp Wren | A (14), N2P (14) |  |
| H3-02 | 6:50.0 | 10 | L52 | P6 | TRUOT | 1757 → 1832 | nhà trên cầu dỡ (1761); cầu mới 1831 | A (10) |  |
| H3-03 | 7:00.0 | 14 | L54–L55 | P7 | XUONG | 1860 → 1871 | Victoria Embankment đẩy bờ bắc ra sông (bờ 1666 ↔ 2026) | A (10), MAP3D (4) |  |
| H3-04 | 7:14.0 | 12 | L56–L57 | P5 | CODINH | 1900 → 1937 | toà văn phòng chen quanh nhà thờ; phố bên dưới không đổi | A (12), N2P (12) |  |
| H3-05 | 7:26.0 | 10 | L58 | P4 | THAP | 1937–1938 | St Paul's Heights: mặt phẳng trần cao độ hiện mờ quanh mái vòm | A (10), THE (4) | thẻ Godfrey Allen |
| H3-06 | 7:36.0 | 12 | (nối) | P1 | KHOP | 1938 ↔ 1666 | cùng khung Bankside: 1938 ↔ 1666 | A (12) |  |
| H4-01 | 7:48.0 | 12 | L59–L60 | P1 | CODINH | 29/12/1940 15:30 → 18:15 | chạng vạng mùa đông; Chủ nhật | A (12), N2P (12) |  |
| H4-02 | 8:00.0 | 14 | L61–L62 | P5 | CAU | 29/12 18:15 → 21:00 | bom cháy rơi thành tia; ≈ 1 500 đám cháy; bộ đếm 100 000 | A (14), THE (3) |  |
| H4-03 | 8:14.0 | 8 | L63–L64 | P6 | TRUOT | 29/12 21:00 | triều thấp: bãi bùn, vòi rồng không tới nước [cần kiểm] | A (8) |  |
| H4-04 | 8:22.0 | 16 | L65–L67 | P4 | THAP | 29/12 22:00 → 23:30 | KHOẢNH KHẮC MÁI VÒM giữa khói lửa (dựng 3D thay ảnh Mason — T4-G1); Paternoster Row cháy | B (16) | Cycles GPU |
| H4-05 | 8:38.0 | 8 | L68 | P1 | DAY | 30/12 07:00 | sáng ra: mái vòm còn đứng; 1 ảnh MOI 1940 (Crown PD) góc khung | A (8), TL (6) | ảnh MOI chưa chốt (việc 5) |
| H4-06 | 8:46.0 | 14 | L69–L70 + lặng 4 s | P1 | CODINH | 30/12/1940 → 1941 | vòng phế tích quanh mái vòm; bộ đếm 160 | A (14), N2P (14), THE (2) |  |
| H4-07 | 9:00.0 | 16 | L71 | P7 | XUONG | 1941 | vùng bom nặng Cripplegate / Paternoster (ước lượng — KHÔNG dùng LCC Bomb Damage Maps) | A (10), MAP3D (6) | ranh 1940 chưa có nguồn mở → bậc 5 |
| H4-08 | 9:16.0 | 20 | (lặng/nhạc) | P2 | KHOP | 1666 ↔ 1941 | hai khoảng trống cùng một khung | A (20) | chia 2 góc (R3) |
| H5-01 | 9:36.0 | 12 | L72–L73 | P5 | CODINH | 1946 → 1951 | Holden–Holford: quy hoạch lại vùng bom | A (12), N2P (12), THE (4) | thẻ Holden + Holford |
| H5-02 | 9:48.0 | 16 | L74 | P5 | CAU | 1957 → 1976 | London Wall (Route 11) + Barbican mọc trên Cripplegate | A (16) |  |
| H5-03 | 10:04.0 | 12 | L75 | P7 | XUONG | 1666 ↔ 2026 | lưới phố Doornick 1666 chồng lên 3D 2026: cùng tuyến | MAP (8), MAP3D (4) |  |
| H5-04 | 10:16.0 | 14 | L76–L78 | P1 | CODINH | 1980 → 2026 | cụm toà cao phía đông mọc lên | A (14), N2P (14) |  |
| H5-05 | 10:30.0 | 14 | L79–L82 | P4 | THAP | 2026 17:30 | từ Fleet Street: Leadenhall vát — mái vòm còn nền trời | A (14) |  |
| H5-06 | 10:44.0 | 12 | (nối) | P3 | VONG | 2026 18:30 | vòng 30° quanh mái vòm từ phía đông | A (12) |  |
| H5-07 | 10:56.0 | 20 | L83–L86 | P1 | KHOP | 2/9/1666 22:00 ↔ 2026 22:00 | KHÉP VÒNG: cùng khung Bankside — vòng cung lửa ↔ đèn City | B (10), A (10) | chia 2 góc: B (1666) / A (2026) |
| H5-08 | 11:16.0 | 28 | (nhạc + lặng 6 s) | P1 | KEO | 2026 đêm | kéo lùi cuối: mái vòm giữa toà cao | A (28) |  |
| H5-09 | 11:44.0 | 16 | — | — | PP | — | hai thẻ "How this film was made" × 8 s (§12.1 b) | PP (16) |  |

## Tổng + kiểm trần

- Thời lượng **720 s** · **60 shot** · shot trung bình 12.0 s · góc cao/toàn cảnh 75.56 %.
- Lớp (s): {'A': 513, 'N2P': 190, 'B': 85, 'MD': 52, 'THE': 43, 'KHAC': 13, 'MAP': 27, 'MAP3D': 28, 'TL': 14, 'PP': 16}

| Chỉ số | Giá trị | Trần | Đạt | Trong ±5 % quanh ngưỡng |
|---|---|---|---|---|
| AI_pct | 33.61 | 70 | ĐẠT | không |
| N2P_pct | 26.39 | 50 | ĐẠT | không |
| MD_pct | 7.22 | 20 | ĐẠT | không |
| MAP_ALL_pct | 7.64 | 12 | ĐẠT | không |
| TL_KHAC_THE_pct | 9.72 | 10 | ĐẠT | **CÓ** |
| B_pct | 11.81 | 20 | ĐẠT | không |
| N2P_chi_codinh |  |  | ĐẠT |  |
| N2P_va_MD_khong_chong |  |  | ĐẠT |  |
| MAP_moi_lan_le_10s |  |  | ĐẠT |  |
| MÓC: số loại cú máy ≥ 4 | 4 |  | ĐẠT |  |
| MÓC: chuỗi cùng loại ≤ 2 | 1 |  | ĐẠT |  |
| MÓC: P1 tái xuất |  |  | ĐẠT |  |
| HỒI 1: số loại cú máy ≥ 4 | 6 |  | ĐẠT |  |
| HỒI 1: chuỗi cùng loại ≤ 2 | 1 |  | ĐẠT |  |
| HỒI 1: P1 tái xuất |  |  | ĐẠT |  |
| HỒI 2: số loại cú máy ≥ 4 | 9 |  | ĐẠT |  |
| HỒI 2: chuỗi cùng loại ≤ 2 | 1 |  | ĐẠT |  |
| HỒI 2: P1 tái xuất |  |  | ĐẠT |  |
| HỒI 3: số loại cú máy ≥ 4 | 5 |  | ĐẠT |  |
| HỒI 3: chuỗi cùng loại ≤ 2 | 1 |  | ĐẠT |  |
| HỒI 3: P1 tái xuất |  |  | ĐẠT |  |
| HỒI 4: số loại cú máy ≥ 4 | 7 |  | ĐẠT |  |
| HỒI 4: chuỗi cùng loại ≤ 2 | 1 |  | ĐẠT |  |
| HỒI 4: P1 tái xuất |  |  | ĐẠT |  |
| HỒI 5: số loại cú máy ≥ 4 | 7 |  | ĐẠT |  |
| HỒI 5: chuỗi cùng loại ≤ 2 | 1 |  | ĐẠT |  |
| HỒI 5: P1 tái xuất |  |  | ĐẠT |  |
| TL-1: góc cao/toàn cảnh có thời gian chạy ≥ 75 % | 75.56 |  | ĐẠT |  |
