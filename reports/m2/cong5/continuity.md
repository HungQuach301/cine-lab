# Rà continuity — Cổng 5 (layout) "Last Round" · 52 shot, 3 420 khung

Người rà: agent continuity (phiên con của P). Chỉ báo lỗi, không sửa file nào khác. Không đọc `checks/`.

## Đầu vào và cách làm
- Hình: `/var/tmp/cine-out/final/video.mp4` (960×540, 24 fps, 3 420 khung, chưa phụ đề). Mốc shot: `assemble.json` (`film_frames` [f0, f1)).
- Trích khung đầu, giữa, cuối của **cả 52 shot** (156 khung, `select=eq(n\,N)`). Trích thêm khung ở các chỗ nghi vấn bằng seek chính xác (đã đối chiếu: khung seek f1600 trùng khung `select` f1600, sai khác trung bình 0,0).
- So từng **cặp shot kề nhau** theo: đạo cụ, trang phục, thời điểm, đèn L1–L11 và cột điện, nguồn sáng, vị trí, hướng màn hình, trục 180°, hướng nhìn. Đối chiếu với `shots/layout/continuity/canh-1…6.md`, `LAYOUT-W1.md`, `LAYOUT-W2.md`, `bible/characters.md` v1.3, `bible/world-rules.md` v0.5.
- Mọi toạ độ chiếu vào khung ở báo cáo này là **tính tay** từ vị trí máy / điểm nhìn ghi trong sheet (ống 28 mm: nửa góc ngang ≈ 32,7°). Chỗ nào chỉ nhìn bằng mắt thì ghi rõ.
- Số khung trong báo cáo là số khung toàn cục của phim (bắt đầu từ 0).
- Bằng chứng: `reports/m2/cong5/continuity/*.jpg` (mỗi ảnh ≤ 83 KB, có nhãn shot và số khung).

## Bảng lỗi

| # | Mức | Khung (toàn cục) | Shot | Mô tả | Bằng chứng | Gói sửa |
|---|---|---|---|---|---|---|
| C1 | **chặn** | 1536–1607 | s27 (so với s24, s35, s37w, s41, s42a) | **Thang biến mất khỏi L11.** s24 (f1379): thang tựa phía bắc cột L11. Sheet cảnh 4 (bảng trạng thái đầu cảnh) ghi "Thang tựa L11 phía bắc". s27 là WS 3 s thấy rõ cả cột L11 từ chân tới đầu, nhưng **không có thang**. Từ s35 thang lại có (s37w f2485, s41, s42a). Đây là đạo cụ chính: khán giả thấy nó mất rồi hiện lại. | `C1_thang_s24-s27-s37w.jpg` | W2 |
| C2 | **chặn** | 2136–2428 (s35, s36, s37, s37w tới trước 1:41,2) so với 1546–2135 | s27–s34 ↔ s35–s37w | **Ánh sáng góc L11 / tường chim đảo ngược giữa cảnh 4 và cảnh 5.** Sau khi cột phố chính (13,5; −4,2) bật lúc 1:04,4, hông nhà kho quanh L11 và chỗ Cas làm chim **trắng phẳng** (s27 f1600, s28–s32). s33/s34 (1:20–1:29): mặt ngoài hốc cửa cũng trắng. Nhưng từ s35 (1:29) **cùng góc đó lại tối**: chỉ còn L11, bóng Ida dài trên đúng mảng tường chim (f2231). s37w f2419 (1:40,8) vẫn tối cho tới khi P5 bật. Nguyên nhân: các shot W2 ở bộ phố (s35–s42a) render **trước khi** có cột này nên thiếu cả ánh của nó. Tính chiếu: **thân cột không lọt khung** ở shot nào của W2 (s35: lệch ≈ 36° so với nửa góc 32,7°, sát mép phải; s37w/s40w ≈ 57°; s41 ≈ 50°; s42a ≈ 87°). Vì vậy chỉ cần thêm **ánh sáng**, không cần thêm hình cột. **Gốc mâu thuẫn:** luật v0.4 nói góc L11 "ngoài tầm vũng sáng của cột đó (~20 m)". Nhưng địa lý chốt ở Cổng 5 đặt cột cách L11 ≈ 5,6 m và cách casSpot ≈ 3,2 m. Hai điều này không cùng đúng được: nếu góc L11 vẫn tối ở cảnh 5 thì chim bóng ở cảnh 4 không thể bị ánh cột xoá. Nhịp "…brighter…" (P5 bật ở s37w) cần góc còn tối. | `C2_anh-sang-goc_s27-s35-s37w.jpg` | **P** (chủ dự án chọn cách hoà giải: dời cột phố chính / che sáng / sửa luật v0.4), rồi **W2** render lại s35–s37w (hoặc s27–s32) |
| C3 | **chặn** | 2736–2819 | s40w → s41 → s42a → s42b/s42 | **Nhảy trục 180° ở nhịp trao đèn.** Sheet cảnh 5 ghi: "Ida TRÁI, Cas PHẢI trong mọi shot hai người". s40w (f2735): Ida trái, Cas phải. s41 (f2754): **Cas trái, Ida phải**. s42a (f2796): **Cas trái–giữa, Ida ở mép phải**. s42 (f2912): lại Ida trái, Cas phải. Tính theo toạ độ sheet: ở s41 và s42a Ida nằm bên phải Cas (tích vô hướng với vector phải của máy lần lượt ≈ +6,1 và +7,2). Tức là cả toạ độ vị trí lẫn góc máy đều đặt hai người ngược quy ước, và trục bị nhảy **hai lần** ở nhịp chính của cảnh 5. | `C3_truc-180_s40w-s41-s42a-s42.jpg` | W2 |
| C4 | **chặn** | 2940–3035 | s43 (so với s10, cùng bộ s1 đêm) | **Trời sáng ở cảnh toàn, trái quyết định (b) và world-rules v0.5.** Dải trời trên cùng đo trung bình RGB (85, 93, 135) → (110, 121, 157): xám lilac sáng, không thấy sao, sáng dần về chân trời. s10 cùng bộ, cùng góc đo (10–18, 15–24, 51–60): xanh đen, có sao. Cùng một thành phố đêm mà hai cảnh toàn không khớp. | `C4_troi_s10-s43.jpg` | W2 |
| N1 | nên sửa | 1331 → 1332 | s23 → s24 | **Cas "hiện ra" ở chỗ nối.** Khung cuối s23 thấy trọn chân tường chim, cạnh phải cột phố chính, ngay sau bóng lớn. Ở đó **không có Cas**. Một khung sau (s24 f1332), Cas đứng ở casSpot (10,35; −7,15), áo đỏ bắt ánh L11. Tính chiếu cho máy S23_CAM: casSpot lệch khoảng +1,9° (≈ 24 px) sang phải trục cột, nên lẽ ra lọt khung. Có thể cột che một phần; W1 kiểm bằng probe. Sheet canh-3 mục s23 cũng không nhắc Cas. | `N1_cas_s23-s24.jpg` | W1 |
| N2 | nên sửa | 2819 → 2820 | s42a → s42b | **Cách cầm đèn lồng đổi ở chỗ cắt.** s42a: Cas ôm đèn giữa hai cổ tay trước ngực. s42b khung đầu: cầm **một tay**, chìa xa ra trước thân. Sheet s42b ghi "đèn lồng treo giữa hai cổ tay", nên sheet cũng khác hình. | `N2_den-long_s42a-s42b.jpg` | W2 |
| N3 | nên sửa | 1920–2087; 2088–2135 | s33, s34 (V2) | **V2 chưa đạt trọn.** s33 (f2004, f2087): Ida đứng **chồng lên bóng mình**, áo tối trên nền bóng tối, đọc thành một khối. Sheet ghi tâm bóng lệch 0,46 m sang trái bà, nhưng trên hình gần như trùng. s34 (f2112): người (có màu) và bóng (phẳng) phân biệt được. Nhưng bóng Cas sắc, đậm, cao ngang đầu bóng Ida, có quả bông và tay, nên vẫn đọc như "cậu bé thứ hai" đứng nắm tay Cas. Bóng Ida mờ, không ra vành mũ, nên "hers, tall… his, small" không đọc được. | `N3_V2_s33-s34.jpg` | W2 (kiểm mù lần 4 quyết) |
| N4 | nên sửa | 1920–2087 | s33 (so với s27, s35, s41, s42b) | **Cột lạ cạnh vòm hốc cửa.** s33 có một cột xám dày, có đế, đứng khoảng 3–4 m bên phải vòm, gần mặt tường. Cùng mặt hông đó, s27/s35/s41 không có cột nào giữa vòm và L11; L11 (đen, cách vòm 5,8 m, ra phố 4,2 m) không thể lọt khung s33 theo toạ độ sheet. Sheet s33 ghi "L11 ngoài khung, bên phải". Không thấy ánh hổ phách L11 ở mép phải. | `N4_cot-la_s33-s27.jpg` | W2 |
| N5 | nên sửa | — | sheet | **Continuity sheet ghi khác hình (và khác nhau):** (1) `canh-4.md` bảng trạng thái đầu cảnh ghi "s24c: nhìn về L11 (**phải** khung)". Hình và `canh-3.md` là **trái** khung (Cas quay sang trái, f1380–1415). (2) `canh-4.md` bảng toạ độ, cùng `LAYOUT-W2.md` R2 và Q-W2-3, ghi cột phố chính "chỉ có ở bộ tường chim". Điều này đã lỗi thời: W1 đã thêm cột vào bộ phố, thấy rõ ở s23 và s24. (3) `canh-4.md` bảng đầu cảnh ghi "Thang tựa L11" nhưng s27 không có thang (C1). (4) `canh-5.md` ghi "Ida TRÁI, Cas PHẢI trong mọi shot hai người", sai với s41 và s42a (C3). (5) `canh-5.md` s35 ghi khung có "dãy bắc (phải)". Hình mép phải là hông nhà kho; theo tính chiếu, dãy bắc (x ≥ 15) nằm ngoài khung. | — | W2 (sheet); P cập nhật R2 |
| G1 | ghi nhận | 1260–1331 | s23 | Đầu đèn P5 (trái) và cột phố chính (phải) **đang tắt đúng lịch**, nhưng kính mờ đọc thành đĩa xám sáng (≈ 150/255) trên nền trời tối (≈ 25/255), dễ đọc thành "đã sáng". Cổng 7 nên hạ độ sáng kính khi tắt. | `G1_s23_dau-den-tat.jpg` | W1 / Cổng 7 |
| G2 | ghi nhận | 2626–2687 | s39 → s40 | s39: mũ hất 0,35, lộ trán. s40 máy cao nên vành che tới lông mày, **mũ đọc như đội thẳng** dù sheet ghi 0,35. Đúng hình học, nhưng dễ đọc thành lỗi nối. | `G2_mu_s39-s40.jpg` | W2 / Cổng 6 |
| G3 | ghi nhận | 2900–2939 | s42 | Quyết định (a) **đạt**: f2918 tay trái lên vành, f2930–2936 kéo mũ xuống, f2939 hạ tay. Cảnh 6 đội ngay (s44, s45). Riêng nhịp "quay người +0,5 rad (2,8–3,0 s)" chưa thấy ở khung cuối f2939 (bà vẫn đứng chính diện). | `G3_s42_keo-mu.jpg` | W2 / Cổng 6 |
| G4 | ghi nhận | 2868–2939 | s42 (V1) | V1 **đạt phần chính**: mũ len và quả bông in rõ trên nền phố trắng; tay chìa ra cỡ khoảng ½ đầu, không còn to bất thường. Còn lại: thân dưới dáng xổm thành một khối tối khó đọc; chỉ thấy một tay hơ (nghi thức đếm ba cần hai lòng tay); đèn lồng bị thân che, chỉ thấy quầng sáng. s42b: mũ và quả bông còn nguyên (f2820). | `N2_den-long_s42a-s42b.jpg`, `G3_s42_keo-mu.jpg` | Cổng 6 |
| G5 | ghi nhận | 2280–2418; 2520–2625 | s37, s39 | Sheet ghi Ida "nhìn lên phố (phải khung)". Trên hình mắt nhìn xuống, hơi sang trái. (Nhìn bằng mắt.) | — | Cổng 6 |
| G6 | ghi nhận | 3096–3143 | s45 | Sheet ghi "tay trái đỡ". Trên hình tay trái giơ ngang vai, tách khỏi đồng hồ. | — | W2 / Cổng 6 |
| G7 | ghi nhận | 1600; 2912 | s27, s42 | Mũ Ida dưới ánh điện đo ra **#58464a** (s27) và **#4a2f35** (s42): sắc 347°, đỏ tía. Theo D2 phải là đen xanh; s31 đo #413e4f, s44 đo #292a2e. Vùng đo nhỏ (20–60 px) trên JPEG 4:2:0 nên có thể lẫn màu khăn hoặc mặt; cần đo lại trên khung render gốc. | `G7_mau-mu.jpg` | W2 / Cổng 7 |
| G8 | ghi nhận | 3144–3179 | s45c ↔ s09 | Kim và vạch đồng hồ quảng trường ra màu hồng nâu (do quầng loá). Ở s09 chúng đen, luật yêu cầu hai kim đen. Giờ đúng: 8:00 (s09), 10:00 (s45c). | — | Cổng 7 |
| G9 | ghi nhận | 2452–2735 | s37w, s40w | Quầng loá của bóng P5 phủ một mảng trời góc trên trái. Không phải quầng chân trời, nhưng làm sáng trời. | `C3_truc-180_s40w-s41-s42a-s42.jpg` (ô 1) | Cổng 7 |

## Kiểm theo danh mục được giao

### Chỗ nối W1 → W2: s24 → s24c → s25 → s26
| Mục | Kết quả |
|---|---|
| Vị trí Cas | Khớp. Cas ở chân tường chim, bên phải L11 (s24 f1332–1379). s24c: cùng chỗ, bóng Cas đổ sang phải. s25: cùng tường, ống thoát nước ở bên trái Cas như s24. |
| Hướng nhìn Cas | s24c nhìn **trái** khung, về Ida/L11 (khớp canh-3; canh-4 ghi sai, xem N5). Sang s25 cậu đã quay vào tường làm chim: nhảy hành động qua cắt, chấp nhận được. |
| Ida | s24/s24c: trên thang L11, đèn lồng cháy ở hông trái (s24: đèn ở phía phải khung khi bà quay mặt về máy, tức hông trái). s25: ngoài hình. s26: đứng dưới đất, nhìn **phải** khung về Cas. Nhịp xuống thang ngoài hình nằm trong s25 (3 s): chấp nhận. |
| Mũ / khăn | hat_back 0 ở s22, s24, s26 (khớp). Khăn một đuôi trước ngực. |
| Đèn | L11 hổ phách là nguồn chính ở s23 cuối, s24, s24c, s25. P5 tắt. **Cột phố chính (13,5; −4,2): có trong bộ phố W1, thân tối ở s23 và ở tiền cảnh phải s24; tắt đúng lịch**; s24c ở sau máy. Bật ở s27: f1536 tắt, f1572 đã trắng (mốc 1:04,4 = f1545,6). |
| Thang | s24: tựa phía bắc L11. **s27 mất thang (C1).** |
| Trục | Ida trái, Cas phải: s24, s27, s30, s32 khớp. |

### Cùng góc phố s23 ↔ s35 / s37w
- Hình khối nhà kho chữ L khớp giữa W1 và W2: mặt cuối phố ở giữa, hông và hốc cửa ở phải, L11 trước vòm (s23, s35, s37w, s40w). **Quyết định (c) đạt.**
- Cột điện tường chim (13,5; −4,2): tính chiếu cho thấy thân cột **không lọt khung** ở s35 (sát mép, khoảng 3° ngoài), s37w, s40w, s41, s42a, s38. Cũng không thấy trên hình. Vì vậy không có lỗi "thiếu cột" về hình. Lỗi thật là **thiếu ánh của cột** (C2).
- P5: tắt ở s23, s35, s37w f2419. Bật ở s37w (f2428,8 theo lịch; f2452 đã trắng). Sáng tiếp ở s40w, s41, s42a. Khớp.
- L11: thắp ở s23 (54,5 s). Sáng tới s40. Tắt ở s40 (f2657 còn sáng, f2687 tắt; mốc 1:51,2 = f2668,8). Tối ở s40w, s41, s42a. Khớp.

### Quyết định chủ dự án
- (a) Mũ Ida: s36 đẩy ra (f2232 → f2279), giữ 0,35 ở s37–s39 và s41. s40 đọc như đội thẳng vì góc máy (G2). s42 kéo lại (G3). Cảnh 6 đội ngay. **Đạt.**
- (b) Không quầng trắng chân trời: s10, s23, s27, s35, s37w đạt. **s43 không đạt (C4).**
- (c) Cuối phố là hông nhà kho chữ L: **đạt** (s23, s24, s27, s35, s37w, s41).

### Các cặp khác (không có lỗi)
- Cảnh 1–3: Ida đi **phải → trái** nhất quán (s02, s07, s15, s23 chạy vào chiều sâu về −x); s08 đi về máy; s12 và s19 là shot trên trục.
  - Thang: trên vai phải, đầu chúc về trước (s02, s07, s15 cuối, s23).
  - Đèn lồng: ở hông trái.
  - Sào mồi: tay phải ở s21 (đã biết là chỗ hở, xem canh-1/3).
- Giờ:
  - s06: đồng hồ bỏ túi 7:31;
  - s09: đồng hồ quảng trường 8:00, mặt bật giữa f600 và f636 (lịch f607);
  - s09w: đồng hồ bỏ túi 7:53;
  - s46: 9:53 → 10:00;
  - s45c: 10:00.
- Đèn điện:
  - s10e: bóng quảng trường bật (tắt ở f720, sáng ở f744);
  - s12: P2 bật (f917);
  - s19: P3 tắt ở f1110, sáng ở f1139 (lịch f1116).
- Cảnh 4:
  - Cas: s25 và s28 cùng khung với ống thoát nước; s28 hết chim bóng;
  - hướng nhìn: s29 Cas quay trái khung về Ida, s30 Ida vào từ trái; s31 Ida nhìn phải;
  - đèn lồng: tay phải ở s30–s32.
- Cảnh 5:
  - đèn lồng: trên nền ở s33–s34, ở hông ở s35–s40w (có giải thích cắt nén trong sheet), trao cho Cas ở s41;
  - s38: Cas cầm hai thanh thang.
- Cảnh 6:
  - Ida không đèn lồng ở s44 (điểm cam ở hông là bàn tay, đã phóng to kiểm), s45, s47;
  - s47: thang trên vai phải;
  - s48: Cas có mũ len và quả bông.

## Tổng số lỗi theo mức
| Mức | Số | Mã |
|---|---|---|
| Chặn | **4** | C1, C2, C3, C4 |
| Nên sửa | **5** | N1, N2, N3, N4, N5 |
| Ghi nhận | **9** | G1–G9 |

Theo gói:
- **W2:** C1, C3, C4, N2, N3, N4, N5.
- **P:** C2 (quyết địa lý và ánh sáng với chủ dự án), N5 (R2).
- **W1:** N1.
- **Cổng 6/7:** các mục G.

## Đang chờ chủ dự án / P
1. **C2:** chọn cách hoà giải giữa luật v0.4 ("góc L11 ngoài vũng sáng cột phố chính ~20 m") và địa lý Cổng 5 (cột cách L11 ≈ 5,6 m). Các phương án:
   - dời cột phố chính xa góc;
   - che sáng bằng khối nhà;
   - chấp nhận góc sáng từ 1:04 và dựng lại nhịp "…brighter…".
2. P commit báo cáo này (agent không commit).
