Nhánh thật: `ccr-f96ee5b5-2ec2i5` (harness buộc) — bản sao đẩy thêm ở `v7-pilot`.

# V7-PILOT — KẾ HOẠCH ĐIỂM MÁY CẢ TẬP (ngữ pháp TL-1…TL-6)

Sinh bởi `scripts/k2tl/v7p_diem_may.py` từ bảng 74 shot G1b (`g1b/episode.yaml`, lời khoá không đổi). Toạ độ máy: `design/k2v/tl/data/diem-may-v7.json` (ENU m, gốc = giao đường băng × Winston Churchill Ave; cao = tuyệt đối).

## 1. Tám điểm máy

| Điểm | Mô tả | Vị trí máy p0 [E, cao, N] | Nhìn tới l0 | FOV dọc | Tiêu cự tương đương (FF) | Dùng ở bản thử | Giây cả tập |
|---|---|---|---|---|---|---|---|
| A | Bắc — đồi Campamento/San Roque nhìn Rock + eo đất + La Línea | [-1900, 115, 4150] | [-1350, 0, 0] | 42° | ≈ 31 mm | C1 | 106.5 |
| Ba | Vịnh — trên mặt nước tây-bắc phố, nhìn phố + Old Mole + Line Wall + Rock | [-2500, 300, -500] | [-450, 60, -1300] | 40° | ≈ 33 mm | H2, C4 | 141.5 |
| Bb | Vịnh — trên mặt nước tây-bắc phố, nhìn phố + Old Mole + Line Wall + Rock | [-2350, 250, -1950] | [-520, 50, -1150] | 40° | ≈ 33 mm | H2, C4 |  |
| Ca | Trên phố — sườn tây trên Grand Parade / King's Bastion | [-170, 300, -1700] | [-760, 0, -920] | 50° | ≈ 26 mm | C3, C5 | 78.8 |
| Cb | Trên phố — sườn tây trên Grand Parade / King's Bastion | [-200, 310, -1760] | [-520, 0, -520] | 52° | ≈ 25 mm | C3, C5 |  |
| D | Cổng biên giới + đường băng — trên mép nam La Línea nhìn nam | [450, 320, 950] | [-100, 0, -180] | 44° | ≈ 30 mm | H1, H3 | 193.5 |
| E | Phía Algeciras — trên vịnh 2,8 km ngoài bờ Algeciras nhìn sang Rock (tele) | [-6300, 170, -1950] | [-500, 150, -1500] | 30° | ≈ 45 mm | C2 | 12.0 |
| F | Đông — trên biển ngoài Catalan Bay nhìn vách đông + eo đất phía Địa Trung Hải (chương 4: đất lấy đá vách bắc/đường hầm) | [1900, 260, -900] | [100, 120, -700] | 40° | ≈ 33 mm | — | 27.0 |
| G | Đỉnh Rock (O'Hara/Signal Hill) nhìn bắc xuống phố bắc + đường băng + eo đất + La Línea | [-60, 520, -1900] | [-50, 0, 600] | 46° | ≈ 28 mm | — | 86.5 |
| H | La Línea — trên phố trung tâm nhìn nam về cổng + Rock (chương 3, 5) | [250, 160, 2300] | [0, 40, 300] | 42° | ≈ 31 mm | — | 32.9 |

Trôi máy: p0 → p1 tuyến tính cả shot; đo bằng `tl7.driftPct` (bản thử: xem V7P-BAO-CAO §5).

## 2. Bảng 74 shot cũ → 42 shot mới

| Shot mới | Điểm | Loại | Shot cũ (loại cũ) | Giây | Thời gian chạy trong shot | Khoảnh khắc chính |
|---|---|---|---|---|---|---|
| H1 | D | tl | 0a (scene3d), 0b (scene3d) | 12.0 | 18/10/2026 23:52 → 19/10 08:20 | đêm biên giới, đèn đường + đèn đường băng, người đi bộ qua đường băng; đêm → bình minh |
| H2 | B | tl | 0c (photo), 0d (card), 0e (scene3d), 0f (photo) | 21.0 | 2026 → TUA NGƯỢC 1309 → 1704 (cờ đổi) → 1779 → 13–14/9/1782 đêm | 14 nhịp vây hãm trên phố/lâu đài; phố 1704 → 1782; pin nổi cháy đêm (≤ 30 s) |
| H3 | D | tl | 0g (scene3d), 0h (scene3d) | 11.5 | 1938 → 1943 → 2026 | mặt đường băng mọc qua đường (1939–41), lấn vịnh (1941–43); dòng người qua cổng 2026 |
| N1.1 | B | tl | SM1 (strategic), 1a (scene3d), 1b (photo) | 19.5 | 2/1704 → 1/8/1704 | hạm đội Rooke vào vịnh (thay bản đồ chiến lược SM1: lời mang ý liên minh) |
| N1.2 | C | tl | 1c (photo), 1d (scene3d) | 24.0 | 7/1704 → 3/8/1704 | plan 1705 phủ khớp lên phố ≤ 3 s rồi tan; phố 1704 dưới pháo hạm (khói) |
| N1.3 | C | tl | 1e (scene3d), 1f (card) | 15.12 | 3/8 → 6/8/1704 | cờ Borgoña → Union trên lâu đài (4/8/1704); không tấm số "100 / 500" |
| N1.4 | A | tl | 1g (scene3d) | 14.0 | 8/1704 → 1705 | dòng người rời phố lên bắc về San Roque dọc eo đất |
| N1.5 | G | tl | 1h (card), 1i (scene3d) | 25.0 | 1713 → 2015 | từ đỉnh Rock nhìn eo đất trống (điều 10 không nhắc); 2015: ranh hiện nay hiện lên (không thẻ trích) |
| N1.6 | A | tl | 1j (scene3d), 1k (scene3d) | 24.5 | 1704 → 1727 → 1730–35 | chiến hào 1704–05, 1727; Línea mọc tây → đông 1730–35 |
| C1 | A | tl | 2a (scene3d), 2b (photo) | 22.5 | 20/6 → 28/10/1779 | cổng đóng 21/6; trại TBN dựng (Faden 1783); thẻ chương "1779 — The Great Siege" |
| C2 | E | tl | 2c (scene3d) | 12.0 | 12/7 → 20/12/1779 | hải đội rời Algeciras ra hàng chặn; thuyền châu Phi quay lại |
| C3 | C | tl | 2d (card), 2e (photo) | 14.12 | 14 → 15/1/1780 (ngày–đêm) | người hái rau dại trên sườn; đồn trú tập; vịnh bị chặn (không tấm "trứng 6 xu") |
| C4 | B | tl | SM2 (strategic), 2f (scene3d) | 13.5 | 16/1 → 30/11/1780 | đoàn Rodney vào/ra; tàu Đan Mạch chở chanh (thay SM2) |
| C5 | C | tl | 2g (scene3d) | 12.5 | 12/4 09:20 → 14/4/1781 11:00 | đoàn Darby thả neo 10:45, pháo TBN bắn phố, dân chạy nam, 5 nhà cháy đêm 13→14/4 |
| N2.6 | C | tl | 2h (photo), 2i (card) | 13.0 | 14/4/1781 → 9/1782 | phố sập dần thành "RUINS" (plan 1786); khói pháo hai phía (không tấm 205 328 / 258 387) |
| KA1782 | neo | neo | KA1782 (scene3d) | 8.0 | 9/1782 | khung neo then/now phố hẹp 1782 (TL-2: vai "then/now") |
| N2.7 | G | tl | 2j (scene3d) | 12.5 | 8/9/1782 07:00 → 18:00 | đạn nung đỏ từ pháo bắc: ụ Mahon + tuyến song song cháy (S059) |
| N2.8 | B | tl | 2k (photo), 2l (photo) | 24.0 | 11 → 12/9/1782 | hạm đội liên quân 47–50 tàu vào vịnh; 10 pin nổi rời Algeciras |
| N2.9 | B | tl | 2m (scene3d), 2n (card) | 28.0 | 13/9 06:45 → 14/9/1782 15:00 | pin nổi vào vị trí → bắn → cháy đêm → nổ rạng sáng (bản dài của H2) |
| N2.10 | D | tl | 2o (scene3d), 2p (photo) | 20.5 | 5 → 7/1782 | vách bắc: lỗ thông hầm Ince nổ thủng (khói) — mặt cắt hầm cần M11 (D2 G1b) |
| N2.11 | A | tl | 2q (scene3d), 2r (card) | 23.0 | 1/1783 → 3/1783 | phát súng cuối 5/2/1783; trại + công sự rút dần (không thẻ trích Versailles) |
| N3.1 | A | tl | 3a (scene3d), 3b (scene3d) | 22.5 | 1783 → 14/2/1810 | đất trung lập trống; Línea + 2 pháo đài nổ tung 1810 |
| N3.2 | G | tl | 3c (photo) | 8.5 | 1810 → 1860 | mép đất Anh tiến dần (doanh trại, vườn) — cần lớp có nguồn 1810–60 |
| N3.3 | H | tl | 3d (scene3d) | 10.0 | 1849 → 1870 → 1905 | La Línea mọc theo năm xây (Catastro) |
| KC1910 | neo | neo | KC1910 (scene3d) | 7.0 | 1910 | khung neo phố La Línea then/now |
| N3.4 | G | tl | 3e (photo), 3f (scene3d), 3g (photo) | 27.0 | 1900 → 1909 → 1930 | dải trung lập; hàng rào 1909 mọc dọc ranh; trại, vườn, trường bắn, trường đua (cần nguồn bậc 1–3) |
| N3.5 | D | tl | 3h (scene3d) | 9.5 | 1933 → 1938 | đường băng cỏ 1934 (dải cắt cỏ) trên dải trung lập |
| N4.1 | D | tl | 4a (photo), 4b (scene3d) | 25.5 | 3/1939 → 1941 | phản đối 1939 (lời); mặt cứng mọc, cắt qua đường (1941) |
| N4.2 | F | tl | 4c (scene3d), 4d (scene3d), 4e (card) | 27.0 | 1941 → 7/1943 | đá vách bắc + đất hầm đổ ra vịnh, đường băng kéo dài (không tấm "55 km") |
| N4.3 | B | tl | 4f (photo) | 9.0 | 1943 | bản đồ AMS 1943 phủ khớp lên phố ≤ 3 s rồi tan; phố 1943 |
| N4.4 | G | tl | SM3 (strategic), 4g (scene3d) | 13.5 | 5/1940 → 11/1942 | tàu sơ tán phụ nữ–trẻ em rời cảng (5/1940); máy bay tụ trên đường băng (thay SM3) |
| KB1943 | neo | neo | KB1943 (scene3d) | 8.0 | 1943 | khung neo phố 1943 (không phụ nữ/trẻ em) |
| N4.5 | D | tl | 4h (card), 4i (scene3d) | 27.5 | 1942 → đêm 7/11/1942 | ≥ 650 máy bay xếp đường băng ban đêm (mô hình máy bay — D3 G1b) |
| N5.1 | D | tl | 5a (scene3d), 5b (card) | 22.0 | 1946 → 6/1969 → 1985 | cổng đóng: dòng người/xe dừng hẳn 1969; mở lại 1985 |
| KB2026 | neo | neo | KB2026 (scene3d) | 9.5 | 2026 | khung neo "the same square, today" |
| N5.2 | D | tl | 5c (scene3d), 5d (scene3d) | 13.0 | 2026 sáng → trưa | dòng người qua cổng giờ cao điểm |
| KC2026 | neo | neo | KC2026 (scene3d) | 10.0 | 2026 | khung neo phố La Línea "remember this street?" |
| N5.3 | H | tl | 5e (card), 5f (scene3d) | 22.92 | 2026 ngày | La Línea ↔ Gibraltar: dòng người sáng đi chiều về (không tấm £85 000) |
| N5.4 | D | tl | 5g (card), 5h (scene3d), 5i (card) | 32.0 | 7/2026 → 18/10/2026 | kiểm tra dừng; hàng rào cũ gỡ, hàng mới lùi vài mét (cần nguồn vị trí); không thẻ dòng thời gian |
| N5.5 | B | tl | 5j (scene3d), KA2026 (scene3d) | 26.5 | 2026 → tua ngược 1704 → 2026 | bookend H2: "why did everyone fight over this place?" |
| N5.6 | D | tl | 5k (scene3d) | 20.0 | 1730 → đêm 2026 | bookend H1: Línea 1730 → đêm biên giới hôm nay |
| PP | the | the | PP (card) | 5.0 | — | thẻ "How this film was made" (§12.1 b) — không phải tấm số |

## 3. Tỷ lệ dự kiến cả tập (726.2 s)

- Timelapse góc cao/toàn cảnh có thời gian chạy: **93.5 %** (ngưỡng TL-1 ≥ 75 %).
- Khung neo tầm mắt (then/now, TL-2): **5.9 %**; lướt thấp ngoài khung neo: **0 %** (TL-2 ≤ 10 % gồm cả khung neo → 5,9 %).
- Thẻ phương pháp cuối: 0.7 %. Tấm số / tấm tư liệu đứng riêng: **0** (TL-4; 9 thẻ số + 4 thẻ trích + 3 bản đồ chiến lược của G1b bỏ, nội dung do lời + phụ đề CC).
- **42 shot** (G1b: 74 shot + cú con) → **3.47 cắt/phút**, shot TB **17.3 s** (ngưỡng TL-1 ≤ 5 cắt/phút, ≥ 12 s).
- Mỗi điểm máy quay lại ở năm khác: D (2026 đêm → 1938 → 1782 → 1934 → 1942 → 1969 → 2026), B (1704 → 1780 → 1782 → 1943 → bookend), A (1704 → 1730 → 1779 → 1783 → 1810), C (1704 → 1780 → 1781 → 1782), G (1713 → 1782 → 1810–1930 → 1940–42).
- **Rủi ro nêu tên:** điểm D chiếm 193.5 s = 26.6 % thời lượng — vượt luật BAI-HOC #96 "không bối cảnh 3D nào > 25 %" (trong ±5 % quanh ngưỡng: 26,6 % vs 25 %). Mỗi lần quay lại D là một năm khác (cảnh khác hẳn) nhưng cùng khung → đề xuất chuyển N5.2 (13 s) sang H để về 24,8 %.
- Shot cần nội dung chưa có trong máy dựng: N2.10 (mặt cắt hầm M11), N3.2/N3.4 (lớp 1810–1930 có nguồn), N4.5 (máy bay 1942), N5.4 (vị trí hàng rào mới 2026), N1.2/N4.3 (bản đồ phủ khớp ≤ 3 s — bộ máy có `phaseMaps`, chưa thử).
