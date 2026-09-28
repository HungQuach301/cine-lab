# Rà continuity v2 — Cổng 5 v2 (layout) "Last Round" · 52 shot, 3 372 khung (2:20,5)

Người rà: agent continuity (phiên con của P). Chỉ báo lỗi, không sửa file nào ngoài báo cáo này và thư mục ảnh bằng chứng. Không đọc `checks/`. Không commit.

## Đầu vào và cách làm
- Hình: `/var/tmp/cine-out/final/video.mp4` (960×540, 24 fps, 3 372 khung, chưa phụ đề). Mốc shot: `assemble.json` (`film_frames` [f0, f1)).
- Trích khung đầu, giữa, cuối của **cả 52 shot** (156 khung, `select=eq(n\,N)`). Trích thêm khung quanh các mốc sự kiện: cột sân trước (f1540–1556), P5 (f2378–2395), L11 tắt (f2612–2630), mồi đèn lồng ở s04 (f262–287).
- So từng **cặp shot kề nhau** theo: đạo cụ, trang phục, thời điểm, trạng thái đèn L1–L11 / P0–P5 / cột sân trước, nguồn sáng, vị trí, hướng màn hình, trục 180°, hướng nhìn. Đối chiếu với `shots/layout/continuity/canh-1…6.md`, `LAYOUT-W1.md`, `LAYOUT-W2.md`, `bible/characters.md` v1.4, `bible/world-rules.md` v0.5.
- Tính chiếu: hiệu chỉnh theo hình thật. Máy render dùng khổ phim dọc 24 mm, nên với 28 mm nửa góc ngang ≈ **37,3°** (báo cáo v1 dùng 32,7°, sai). Kiểm trên s23: cột sân trước (17,0; −5,9) tính ra x ≈ 857 px, trên hình 855 px; Cas ở casSpot (14,3; −7,15) tính ra 808 px, trên hình 808 px.
- Số khung là số khung toàn cục (bắt đầu từ 0). Màu đo bằng trung bình / trung vị trên JPEG trích từ video (4:2:0), nên chỉ dùng để so tương đối.
- Bằng chứng: `reports/m2/cong5/continuity-v2/*.jpg` (mỗi ảnh ≤ 150 KB, có nhãn shot + khung).

## Bảng lỗi

| # | Mức | Khung (toàn cục) | Shot | Mô tả | Bằng chứng | Gói sửa |
|---|---|---|---|---|---|---|
| C5 | **chặn** | 1920–2039 (so với 2088–2183) | s33 ↔ s35 (cặp s32 → s33 → s34 → s35) | **Ngoài vòm hốc cửa sáng trắng phẳng trước khi P5 bật. Đây là phần còn lại của C2.** s33 (1:20,0–1:25,0): mặt hông nhà kho quanh vòm và nền sân đo trung bình (217, 217, 221), tức trắng lạnh phẳng như sau khi điện phủ. Theo B1, góc L11 và hốc cửa phải **tối** tới khi P5 bật ở 1:39,2 (f2381). Hốc cửa (2,2; −8,1) cách đầu đèn cột sân trước ≈ 13,6–15,1 m, ngoài tầm 8,5 m. s35 (1:29,0, sau s34 đúng 4 s) thấy **cùng vòm đó** ngay sau L11 (tính chiếu x ≈ 553 px, trên hình ≈ 550 px) trên mảng tường tối, ấm (tường quanh L11 đo (151, 98, 59)). Khán giả thấy góc phố đang trắng chuyển sang tối rồi 10 s sau lại trắng khi P5 bật. Sheet `canh-5.md` s33 vẫn ghi "ngoài vòm điện phẳng", trái với mục "A2 B1" ngay đầu cùng file. s42b/s42 (sau P5) ngoài vòm trắng là **đúng**. | `C5_s33-ngoai-vom-sang_s32-s33-s34-s35.jpg` | **W2** render lại s33: ngoài vòm là góc tối, chỉ có hổ phách L11 từ bên phải và tràn ≈ 0,05–0,06 như s35. Đèn lồng trong hốc vẫn là key. Kiểm lại N3 sau khi đổi. Sửa sheet s33. |
| N2 | nên sửa (cũ, **còn mở**) | 2771 → 2772 → 2819 | s42a → s42b | **Cách cầm đèn lồng đổi qua cắt, và đổi tiếp trong s42b.** s42a f2771: ôm sát ngực, hai tay đỡ trên. s42b f2772: đèn chìa ra trước, thấp ngang bụng. s42b f2819: xách một bên hông. Sheet s42b ghi "ôm sát ngực, treo giữa hai cổ tay (`casHug`, cùng cách cầm với s42a — sửa N2)", nên sheet khác hình. | `N2_den-long_s42a-s42b-s42.jpg` | W2 |
| N3 | nên sửa (cũ, **còn một phần**) | 1980–2039 | s33 | s33 5 s, máy dolly + dịch ngang: **đạt** phần thời lượng và chuyển máy. Lưng hai người có ánh vàng ở f1920. Từ giữa shot, Ida đứng chồng lên nửa phải bóng mình: áo tối trên nền bóng tối, đầu đọc thành một đốm sáng, vành mũ không tách khỏi bóng (f1980, f2039). s34 (f2064) đọc được: Ida, bóng Ida, Cas, bóng Cas. Khi sửa C5 thì độ tương phản nền trong hốc sẽ đổi, nên kiểm lại. | `N3_V2_s33-s34.jpg` | W2 (kiểm mù quyết) |
| N6 | nên sửa (mới) | 1332–1415 → 1488–1751 | s24/s24c → s26–s30 | **Đèn lồng thắt lưng tối đi ở chỗ nối W1 → W2 mà không có nhịp đóng cửa trên hình.** W1 s23–s24c: đèn lồng hông trái sáng rõ (f1332). W2 cảnh 4: sheet s26 ghi "đèn lồng thắt lưng 0,012 (đóng cửa)". s27 (f1536) và s30 (f1728) không thấy quầng. s30 có nhịp "mở cửa 0,012 → 3,0". Từ s35 đèn lại sáng ở hông (f2136). Lưu ý: ở s27 và đầu s30, hông trái ở phía khuất máy, nên riêng hình chưa đủ kết luận. Nhưng sheet W2 chủ ý để đèn gần tắt, trái với `canh-3.md` "đèn lồng cháy" ở khung cuối s24c. | `N6_den-long_s24-s27-s30-s35.jpg` | **P** chọn: (1) cảnh 4 để đèn sáng như W1, nhịp s30 chỉ là tháo đèn; hoặc (2) thêm nhịp đóng cửa đèn (Cổng 6), rồi W1 hoặc W2 theo |
| N7 | nên sửa (mới) | 2819 → 2820 | s42b → s42 | **Nhảy hành động qua cắt.** Cuối s42b Cas đứng, xách đèn. Khung đầu s42: Cas đã ngồi xổm, đèn lồng đã đặt trên nền, tay đang hơ. Cắt ngược 180° (ngoài vòm → trong hốc) làm nhảy đỡ lộ hơn, nhưng mất nhịp đặt đèn và ngồi xuống. Sheet s42b / s42 đặt đúng như vậy (cắt nén). | `N2_den-long_s42a-s42b-s42.jpg` | W2 (cuối s42b bắt đầu cúi đặt đèn, hoặc đầu s42 Cas còn đang hạ người) |
| N8 | nên sửa (mới) | 2892–2987 | s43 | **"Một ô cửa hổ phách" không đọc được.** Trời đạt (C4). Nhưng mọi mặt tiền trắng có hàng chục ô cửa màu nâu cam đều nhau. Điểm ảnh bão hoà nhất là (192, 112, 101). Không có ô nào nổi lên thành ô cửa nhà Cas như sheet s43 ("một ô cửa hổ phách, gần giữa khung, 60–130 m") và luật v0.5 mục 5 ("toàn cảnh trắng, một ô vàng"). Nhịp nối s43 → s44 (ô cửa → Ida dưới cửa sổ) mất điểm neo. | `N8_s43_o-cua.jpg` | W2 |
| N9 | nên sửa (mới, sheet) | — | sheet | **Continuity sheet còn số cũ sau A2:** (1) `canh-5.md`: tiêu đề cảnh (1:20,00–2:02,50), tiêu đề shot s33 (1:20,00–1:27,00) và nhịp 7 s của s33 (1,2 / 3,2 / 4,4 / 5,8 s) trái với mục A2 (5 s). Bảng lịch vẫn ghi P5 1:41,2 và L11 tắt 1:51,2; hình là **1:39,2 (f2381)** và **1:49,2 (f2621)**. Các tiêu đề s34–s42 vẫn lệch +2 s. s33 "ngoài vòm điện phẳng" (C5). (2) `canh-6.md`: tiêu đề 2:02,50–2:22,50 (thật 2:00,5–2:20,5), "L11 tắt từ 1:51,2". (3) `canh-3.md` dòng 15: "P5 chỉ bật ở 1:41,2"; mục "Chỗ hở 3" còn casSpot (10,35; −7,15). s24c ghi "bóng lớn của bà + thang đổ lên tường ở trái khung", nhưng f1380–1415 không có. s24 ghi "bóng Cas đổ lên tường chim", nhưng f1332–1379 không thấy. (4) `canh-4.md`: bảng toạ độ vẫn ghi cột (13,5; −4,2) "có ở cả hai bộ", casSpot (10,35; −7,15), Cas → L11 4,0 m (mục A2 ở đầu file đè lên, nhưng bảng chưa sửa). s25 ghi "ống thoát nước ở trái khung", nhưng f1416–1487 không có ống: ống ở x ≈ 9,5, ngoài khung sau khi dời +3,95 m. (5) `LAYOUT-W1.md` dòng 62 (máy s24 cũ), dòng 89 (casSpot cũ). `LAYOUT-W2.md` §1 (142,5 s, P5 1:41,2, L11 1:51,2), §2 cột thời gian s34–s48, §5 `casSpot` [10,35; −7,15] và `houseX0N` 15. | — | W1 (`canh-3`, LAYOUT-W1); W2 (`canh-4/5/6`, LAYOUT-W2) |
| G1 | ghi nhận (cũ, còn) | 1260–1331 | s23 | Đầu đèn P5 và cột sân trước **tắt đúng lịch**, nhưng kính mờ đọc thành đĩa xám sáng (đỉnh 152 và 139 / 255) trên trời ≈ 27. | `OK_B1_noi-W1-W2_s23-s27.jpg` (ô 1–2) | Cổng 7 |
| G2 | ghi nhận (cũ, còn) | 2578–2639 | s40 | Mũ đọc như đội thẳng dù sheet ghi hat_back 0,35 (máy cao, vành che trán). | `OK_d_toc-bac_trang-phuc.jpg` (s40) | Cổng 6 |
| G5/G6 | ghi nhận (cũ, còn) | 3018; 3048–3095 | s44, s45 | s44: sheet ghi "tay đặt ngực", hình tay trái giơ lên phía cửa sổ. s45: sheet ghi "tay trái đỡ", hình tay trái giơ ngang vai, tách khỏi đồng hồ. Đồng hồ quay mặt ra máy. | `OK_d_toc-bac_trang-phuc.jpg` (s44, s45) | Cổng 6 |
| G7 | ghi nhận (cũ, mở rộng) | 864; 918; 972; 2525; 2820 | s11, s12, s13, s39, s42 | **Màu mũ Ida nhảy theo nguồn sáng.** s11: nâu vàng sáng (L7 sát đầu). s12: đen (#161015). s13: #773e22 (sắc 20°, bão hoà 0,71). s12 và s13 cùng thời điểm (0:37–0:41), hai shot liền nhau. s39 dưới điện: #2b140e. s42: #4e3338. Theo D2, dưới điện phải đọc đen xanh. s40 f2639 (#191925) đúng. Có thể do L11/L7 ở rất gần. Đo lại trên render gốc. | `G7_mau-mu_s12-s13-s39-s42.jpg` | Cổng 7 |
| G8 | ghi nhận (cũ, còn) | 3096–3131 | s45c | Kim và vạch đồng hồ quảng trường màu hồng nâu (quầng loá). Giờ đúng 10:00. | — | Cổng 7 |
| G9 | ghi nhận (cũ, còn) | 2381–2687 | s37w, s40w | Quầng loá bóng P5 phủ mảng trời góc trên trái. | `OK_goc-L11_s27-s35-s37w.jpg` (ô 4) | Cổng 7 |
| G10 | ghi nhận (mới) | 2687 → 2688 | s40w → s41 | Ida từ đỉnh thang (s40w cuối) xuống đất đang trao đèn (s41 đầu), qua cắt giữa hai WS cùng nhóm nhân vật (góc máy đổi ≈ 45°). Sheet chủ ý cắt nén ("s40w: không gì đổi"). Có thể đọc thành nhảy. Đề xuất Cổng 6 cho Ida bắt đầu xuống thang trong 2 s của s40w. | `G10_s40w-s41_xuong-thang.jpg` | Cổng 6 |
| G11 | ghi nhận (mới) | 1919 → 1920 | s32 → s33 | Cuối s32 Ida quỳ. Khung đầu s33 bà đã đứng thẳng, trong khi sheet ghi "0–0,6 s đứng dậy từ tư thế quỳ". Chỗ đổi bối cảnh (cắt nén) nên ít lộ. | `N3_V2_s33-s34.jpg` (ô 1) | Cổng 6 |
| G12 | ghi nhận (mới) | 3018; 3048–3095 | s44, s45 | (d) tóc: mọi shot khác đọc bạc trắng. s45 tóc đọc **xám tối** (ánh ngõ yếu). s44 nhỏ, ngược sáng. Không phải lỗi nối, nhưng lệch với ý đồ "tóc bạc mọi shot". | `OK_d_toc-bac_trang-phuc.jpg` | Cổng 7 |
| G13 | ghi nhận (mới) | 2988–3047 → 3204 | s44 → s47 | s44 WS 21 mm thấy gần trọn con ngõ, không có thang. s47 bà vác thang. Sheet s44 đã ghi "thang ngoài hình — Cổng 6 cần đặt". | — | Cổng 6 |

## Kiểm theo danh mục được giao

### B1 — chỗ nối W1 ↔ W2 (s23 → s24 → s24c → s25 → s26 → s27)
| Mục | Kết quả |
|---|---|
| Một cột, không hai cột | **Đạt.** s23 thấy hai cột điện: P5 (10,8; 3,9) ở trái–giữa (x ≈ 328) và cột sân trước (17,0; −5,9) ở mép phải (x ≈ 855). Chỗ cột cũ (13,5; −4,2) phải hiện (tính ra x ≈ 677) **không có cột**. Vạch dọc ở x ≈ 722 là ống thoát nước trên hông kho (x ≈ 9,5). s27: một cột ở sân trước, trước đầu hồi dãy bắc. |
| Cột sân trước tắt trước 1:04,4 | **Đạt.** Tắt ở s23, s24 (ngoài khung), s24c, s25, s26, s27 f1536–1544. Bật ở **f1546** (1:04,42), nhấp (f1548 tắt, f1550 sáng, f1552 nửa), đứng ở f1556. Khớp lịch. |
| Vị trí Cas mới | **Đạt.** s23 f1260: Cas ở chân tường, x = 808 px, khớp tính chiếu casSpot (14,3; −7,15) (N1 cũ đã sửa). s24: Cas phải, nhỏ, Ida trái. s24c: Cas nhìn trái. s25/s28: Cas quay vào tường. s27: Cas giữa ống thoát nước và cột sân trước. |
| Hướng / trục | Ida trái, Cas phải ở s24, s27, s30, s32. s26 Ida nhìn phải khung. s29 Cas quay trái khung. Khớp. |
| Đạo cụ | Thang tựa phía bắc L11 ở s23 cuối, s24, **s27** (C1 cũ đã sửa), s35, s37w, s40w, s41, s42a. Đèn lồng: xem N6. |

### Góc L11 — s27 và s35–s37w (B1)
- s27: vũng sáng cột bao tường quanh Cas (≈ 216/255). Tường cạnh L11 vẫn hổ phách, tối. Ranh vũng sáng ở khoảng ống thoát nước. **Đạt.**
- s35 (1:29–1:33): góc tối, chỉ L11 (có bóng dài). Mép phải khung là hông kho ở x ≈ 9,6–12,1, đúng rìa vũng sáng: đo (157, 132, 122), ít bão hoà hơn tường L11 (151, 98, 59). Khớp với dải tường cùng chỗ ở s27 f1607 (140, 125, 125). **Đạt.**
- s36, s37: nền tối, key L11. **Đạt.**
- s37w: f2371–2380 tối. P5 bật **f2381** (1:39,2), nhấp f2383, đứng f2385. **Đạt.** Theo tính chiếu, mép phải khung là hông kho ở x ≈ 6,5, ngoài vũng cột sân trước, nên không cần thấy ánh cột.
- **Ngoại lệ:** s33 (C5).

### (a) s33
- 120 khung = 5,0 s. Máy dolly + dịch ngang (vòm trôi từ x 240–600 sang 180–570). Lưng hai người bắt vàng ở đầu shot: **đạt.**
- Người/bóng còn dính ở nửa sau (N3). Ngoài vòm sáng sai (C5).

### (b) L11 sau khi tắt
- L11 tắt ở ≈ **f2621** (1:49,2): s40 f2616 còn sáng, f2622 tắt.
- s40w, s41, s42a: kính tối, không lửa, không quầng. **Đạt.**
- Bằng chứng: `OK_b_L11-tat_s40-s42a.jpg`.

### (c) Đá lát, nền
- s06, s09w: nền nhoè, hết "chấm bi". **Đạt.**
- s46: nền sau đồng hồ là mặt tường sáng ấm, không còn đá lát. **Đạt.**
- Kích thước viên đá ~0,11 m: **không đo lại** ở vòng này (cần probe có thước).

### (d) Tóc Ida và trang phục v1.4
- Tóc bạc trắng ở s05, s11, s12, s13, s21, s22, s26, s30, s31, s36, s37, s39, s40, s42a, s42, s47 (xem G12 cho s44, s45).
- Cổ lộ đoạn ngắn, cổ áo bẻ thấp, khăn quấn thấp: nhất quán ở s05, s22, s26, s31, s39, s42a.
- Khăn một đuôi trước ngực. Hoa tai có mặt ở mọi cận.
- Màu khăn đổi theo nguồn: đỏ dưới lửa, hồng tím dưới điện. Màu mũ: G7.
- Bằng chứng: `OK_d_toc-bac_trang-phuc.jpg`.

### Đèn lồng thắt lưng (cảnh 1 → 3)
- s02 (f96–203) và s03 (f204–251): **tắt**.
- s04: f262, f276 tắt; **f283 đã cháy** (lịch 11,7 s = f280,8).
- Từ s07 trở đi cháy ở hông trái (s07, s08, s13, s14, s23, s24).
- **Đạt.** Chỗ nối sang cảnh 4: N6.

### Mũ Ida
- s36: đẩy mũ ra sau (f2184 → f2231).
- s37–s39: giữ, lộ trán.
- s40: đọc như đội thẳng (G2).
- s42: đội lại ở khung cuối.
- Cảnh 6 (s44, s45, s47): đội thẳng.
- Khớp bảng mũ `canh-5.md`.

### Các cặp khác (không lỗi)
- **Cảnh 1–3:**
  - Hướng đi phải → trái nhất quán.
  - Thang trên vai phải, đầu chúc về trước (s02, s07, s15, s23; s47 vai phải).
  - s06 7:31. s09 8:00, đồng hồ sáng từ f607. s09w 7:53.
  - s10e bóng quảng trường bật trong shot.
  - s12 P2 bật, s13 trắng tới Ida. s19 P3 bật.
  - Sào mồi tay phải ở s21.
- **Cảnh 5:**
  - Trục Ida trái / Cas phải ở s34, s35, s37w, s40w, **s41, s42a** (C3 cũ đã sửa), s42.
  - s38 hai tay trên thang. Trao đèn ở s41.
- **Cảnh 6:**
  - s43 trời đêm xanh đen, trung bình dải trên (13, 21, 63), gần s10 (13, 18, 53). Không quầng chân trời (C4 cũ đã sửa).
  - s45 9:53 → s46 9:53 → 10:00 → s45c 10:00.
  - Không đèn lồng ở s44, s45, s47.
  - s48 Cas có mũ len và quả bông.

## Tổng theo mức
| Mức | Số | Mã |
|---|---|---|
| Chặn | **1** | C5 |
| Nên sửa | **6** | N2, N3, N6, N7, N8, N9 |
| Ghi nhận | **10** | G1, G2, G5/G6, G7, G8, G9, G10, G11, G12, G13 |

Theo gói:
- **W2:** C5, N2, N3, N7, N8, N9 (canh-4/5/6, LAYOUT-W2).
- **W1:** N9 (canh-3, LAYOUT-W1).
- **P:** N6 (chọn trạng thái đèn lồng cảnh 4).
- **Cổng 6/7:** các mục G.

## Trạng thái lỗi cũ (báo cáo `continuity.md`)
| Mã | Trạng thái | Căn cứ |
|---|---|---|
| C1 thang mất ở s27 | **Đã sửa** | f1536, f1607: thang tựa phía bắc L11 |
| C2 ánh sáng góc L11 đảo ngược | **Đã sửa phần lớn** (B1). **Còn s33 → C5 (chặn)** | s27 / s35 / s37w đúng B1; s33 ngoài vòm vẫn trắng |
| C3 nhảy trục s41, s42a | **Đã sửa** | f2706, f2771: Ida trái, Cas phải |
| C4 trời sáng ở s43 | **Đã sửa** | dải trời (13, 21, 63), không quầng |
| N1 Cas hiện ra ở s23 → s24 | **Đã sửa** | f1260: Cas ở casSpot mới, khớp tính chiếu |
| N2 cách cầm đèn s42a → s42b | **Còn mở** | f2771 / f2772 / f2819 |
| N3 V2 s33–s34 | **Còn một phần** | s34 đạt; s33 Ida chồng bóng |
| N4 cột lạ cạnh vòm s33 | **Đã sửa** | s33 chỉ còn ống thoát nước mép trái và vòng sắt nhỏ (khớp s42b) |
| N5 sheet khác hình | **Đã sửa các mục cũ** (s24c TRÁI, thang, trục canh-5, cột). **Phát sinh mục mới → N9** | xem N9 |

## Đang chờ chủ dự án / P
1. **N6:** chọn trạng thái đèn lồng ở cảnh 4. Phương án 1: sáng như W1, s30 chỉ tháo đèn. Phương án 2: thêm nhịp đóng cửa đèn.
2. **C5:** W2 render lại s33 với ngoài vòm tối. Nếu chủ dự án muốn giữ ngoài vòm trắng thì phải đổi lại B1 (góc L11 tối tới P5). P xác nhận.
3. P commit báo cáo này (agent không commit).
