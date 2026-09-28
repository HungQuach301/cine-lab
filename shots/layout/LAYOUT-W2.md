# LAYOUT W2 — Cảnh 4–6 (s25 → s48, 0:59,00–2:20,50) · Cổng 5, giai đoạn A

Gói W2. Nguồn: `design/cong5/layout/shots_w2.js`, `sets2.js`, `sets_end.js` (`order_w2.js`: s33 5,0 s theo A2). Kiểm bằng probe (3 khung/shot, 960×540, SwiftShader).
Continuity: `continuity/canh-4.md`, `canh-5.md`, `canh-6.md`. Manifest Cổng 6: `shots_w2.json`. Ảnh trước/sau: `reports/m2/cong5/w2/`.

## 0. Cập nhật A2 (quyết định chủ dự án sau Cổng 5)
| Mục | Sửa | Số đo |
|---|---|---|
| **B1** | Cột điện phố chính vào sân (17,0; −5,9), tầm 8,5 m; casSpot (14,3; −7,15); dãy bắc từ x = 18,5; bộ tường dời mọi dấu cảnh 4 +3,95 m; bỏ trắng tràn toàn cục. `endInfo.wallPost = {x, z, range, ry, set, group, light}`, `endInfo.casSpot`. | đầu đèn → tường chim 5,2 m (trong vũng); → lửa L11 9,5 m (ngoài tầm 8,5) |
| **(a)** | s33 7,0 → 5,0 s (tổng phim 140,5 s); dolly 0,9 m + dịch ngang (v3: trái 0,4 m); phơi sáng s33/s34 1,5. | lệch tổng −2,0 s (trong ±5 s) |
| **(b)** | Kính L11 sau khi tắt: tối đục ở s40w, s41, s42a. | vùng lồng đèn s40w: TB độ sáng 73,5 → 54,7 (/255) |
| **(c)** | Đá lát bộ tường, hốc cửa (phố ngoài), phố rẽ, sân: trải 2,4 m/tile (trước 3 m); ngõ (bộ khoá s6) lặp 1,25×. | viên 0,09–0,14 m, TB 0,11 m ≈ 1/14,5 chiều cao Ida (1,62 m); s46: đổi máy (hướng (−0,6; 0,1; 0,8)) → nền là tường ngõ, không còn đá lát trong khung (`v2_c_s46.jpg`) |
| **v3 C5** | s33, s34 (trước P5): ngoài vòm góc tối lạnh — tràn điện xa × 0,05 (như s35), hổ phách L11 từ phải, trời lạnh 0,22. | mặt tường quanh vòm s33: (217, 217, 221) → trái (48, 46, 52), phải (91, 69, 61); trong hốc (146–166, 90–98, 44–46) |
| **v3 N3** | `BAY` đèn (0,2; 3,0), Ida (−0,62; 1,45), Cas (0,9; 0,8); máy s33 dịch trái 0,4 m. | bóng Ida lệch trái bà 0,77 m (v2 0,53), bóng Cas lệch phải 0,25 m |
| **v3 N2/N7** | `casHug` chặt (vai −12°, khuỷu −112°) ở s41, s42a, s42b; s42b thêm nhịp quay ra vòm + ngồi xổm + đặt đèn xuống nền (1,45–2,0 s), tư thế cuối = tư thế mở s42. | — |
| **v3 N8** | s43: mọi ô cửa khác kính lạnh; một ô hổ phách nhìn thấy (tia máy–ô không vướng), nền tối, gần giữa khung. | ô nhà Cas cách máy 130,9 m, khung (0,555; 0,453) |
| **v3 N6** | Đèn lồng Ida cháy liên tục; s30 bỏ nhịp "mở cửa": hắt sáng tăng liên tục 0,012 → 3,0 (0,8–1,85 s), không bật cóc. | — |
| **v4 B-i** | Mọi shot W2 là hàm thuần theo t: bản bọc `makeChar` trong `shots_w2.js` đặt gốc (vị trí + hướng) TRƯỚC `setPose` (rig tính hướng đèn lồng thắt lưng theo ma trận gốc đang có → trước đây mang hướng của khung trước). s33 cũng đặt gốc trước. | mặt nạ C3 thẳng vs nối tiếp: s26 133 px → 0, s35 2 px (khung 2136) và 1 px (2148, ×1) → 0; ảnh RGB (> 2/255): s26 301 px (max 99) → 0, s35 145 px (max 192) → 0; 29/29 shot = 0 (cách sửa trùng `mkChar` của W1 @04a738b) |
| **v4 C-i** | s43: dolly 12 m về ô cửa nhà Cas + 28 → 45 mm, nhìn trôi 70 % về ô. | lõi ô hổ phách ≈ 5 × 9 px → ≈ 10 × 15 px (960 px) |
| **v4 (c)** | Thứ tự s39 (Ida) → s38 (Cas): câu cuối L4 bắt đầu trên mặt Ida; cắt sang Cas ở 106,0 s (giữa "…ones / who need it"). | s39 101,6–106,0; s38 106,0–107,4; tổng không đổi |
| **v4 (d)** | Thứ tự s45 → s46 → s45c; kim giờ bỏ túi ăn khớp kim phút. Giờ trên hình chỉ tiến. | xem `continuity/canh-6.md` bảng (d) |
Ảnh: `reports/m2/cong5/w2/v2_B1_…`, `v2_a_…`, `v2_b_…`, `v2_c_…`, `v3_…`, `v4_…`. Bảng dưới đã mang mốc hiện hành (v4).

## 1. Tóm tắt
- **Thời lượng:** 29 shot, 81,5 s (1956 khung), tổng phim 140,5 s (2:20,5). Không đổi id; mốc thoại L3 1:14,0, L4 1:33,0; P5 bật 1:39,2; gạt van 1:47,7; L11 tắt 1:49,2.
- **V1–V4 đã sửa bằng dàn dựng, máy, bối cảnh và quang học thật** — không đổi tỷ lệ sheet, không thêm nguồn ngoài truyện, không bóng giả (mục 3).
- **Địa lý cuối phố chốt một lần cho cả hai bộ cảnh** (bộ phố W1 và bộ tường chim W2): nhà kho chữ L. Tường chim là **hông nam** nhà kho, có hốc cửa bốc hàng; mặt cuối phố chắn cuối phố; phố rẽ trái, cong, dốc xuống. Sau B1: `casSpot` (14,3; −7,15) — Cas cách tường 0,95 m, cách L11 7,1 m; L11 cách tường 4,2 m → `casSpot` cho s24/s24c của W1.
- **D2:** mũ #262a33 đo trên probe: dưới lửa **nâu xám**, dưới điện **đen xanh** (mục 4).
- Thêm các lỗi tự phát hiện khi probe và đã sửa: chim s28 còn xám (trái luật 3.3); đèn lồng tự che nguồn nên chim s32 không hiện; Cas s38 không cầm thang; Ida còn đèn lồng ở cảnh 6 (s47); s45 không thấy đồng hồ; mũ Ida bật về vị trí cũ sau s37w; chim s48 lẫn vào bóng đầu.

## 2. Bảng shot cuối (thay đổi so với animatic v2 + lý do)
Máy: vị trí → điểm nhìn (m). Hệ toạ độ: cảnh 4 = hệ tường chim; s33, s34, s42b, s42 = hệ hốc cửa; còn lại = bộ phố (xem continuity).

| Shot | Thời gian | Cỡ · mm | Máy (cuối) | Chuyển máy | Thay đổi so với v2 · lý do |
|---|---|---|---|---|---|
| s25 | 0:59,0–1:02,0 | MS · 45 | (6,15; 1,3; 3,6) → (5,95; 1,3; 3,3), nhìn (4,25; 1,1; 0) | dolly vào 0,3 m | Giữ khung. Tường = hông nhà kho thật (V3). |
| s26 | 1:02,0–1:04,0 | MS · 50 | (−2,1; 1,5; 6,55) → đầu Ida | tĩnh | **V4:** Ida dời tới (−3,8; 7,3): L11 gần chính trước mặt, ngẩng 25°. Máy 3/4 phía +x trục. facelight `gas`. Phơi sáng 2,6 → 3,4. Nền: phố chính đã trắng + cuối phố. |
| s27 | 1:04,0–1:07,0 | WS · 21 | (−1,0; 0,85; 13,0) → (1,2; 3,0; 1,0) | tĩnh | B1: máy từ vỉa hè nam. **V3:** hốc cửa trái khung, Ida trái, L11 + thang, tường chim với Cas, cột trong sân, đầu dãy bắc (phải). Phơi sáng 3,6 → 1,1 theo công tắc. |
| s28 | 1:07,0–1:09,0 | MS · 45 | (6,15; 1,3; 3,6) → (4,25; 1,1; 0) | tĩnh | **Luật 3.3:** vũng sáng cột trong sân (tầm 8,5 m) + tràn nền 0,054 → không còn chim xám. Phơi sáng 1,0. |
| s29 | 1:09,0–1:12,0 | MCU · 85 | (5,65; 1,1; 2,8) → (4,05; 1,05; 1,0) | tĩnh | Cas quay về vị trí mới của Ida (trái khung). |
| s30 | 1:12,0–1:14,0 | MS · 35 | (6,55; 1,4; 4,0) → (3,85; 0,8; 0,7) | tĩnh | Ida **đi vào khung** (0,7 s) rồi tháo đèn, quỳ (`kneelHold`). **N6 (v3):** đèn cháy liên tục, không nhịp mở cửa — hắt sáng tăng liên tục 0,012 → 3,0 (0,8–1,85 s). Đèn lồng không tự đổ bóng. |
| s31 | 1:14,0–1:17,0 | MCU · 85 | đầu Ida + (1,6; 0,05; 1,25) | tĩnh | Máy lùi sang bên để đầu Cas không che mặt bà (probe v2-sửa: đầu Cas che nửa mặt). |
| s32 | 1:17,0–1:20,0 | WS · 35 | (5,85; 1,35; 4,1) → (3,7; 1,45; 0) | tĩnh | Đèn lồng ở `LAN_T`, cách tường 0,60 m, dưới-sau tay Cas, thân Cas sau đèn → chim to, ấm, mềm; Cas nhích tới `CAS_S32`, tư thế cục bộ `birdReach`. |
| s33 | 1:20,0–1:25,0 | WS · 32 | bộ khoá (0,25; 1,35; 10,5) → +(−0,4; 0; −0,9) | dolly vào 0,9 m | **V2/N3 (v3):** đèn lồng (0,2; 3,0); Ida (−0,62; 1,45) ×1,94, bóng lệch trái 0,77 m; Cas (0,9; 0,8) ×1,36, bóng lệch phải 0,25 m; PCF 4. **C5 (v3):** ngoài vòm góc tối lạnh (P5 chưa bật). Ẩn cột gang cạnh vòm (N4). |
| s34 | 1:25,0–1:27,0 | MS nghiêng · 26 | (1,35; 1,15; 4,0) → (−0,2; 1,35; 0,4) | tĩnh | **V2:** thấy cả nền: bóng nối chân mỗi người. Trái → phải: Ida, bóng Ida, Cas, bóng Cas. `BAY` v3; ánh sáng C5 (không thấy ngoài vòm). |
| s35 | 1:27,0–1:31,0 | WS · 28 | (16,5; 1,7; 2,6) → (5,5; 2,3; −3,8) | tĩnh | **V3:** cuối phố có khối; Ida đi ra từ phía hốc cửa (hông nhà kho). Cas chạy 1,43 m/s tới `CAS_LAD`. |
| s36 | 1:31,0–1:33,0 | MCU · 85 | `faceCam` 1,9 m | tĩnh | facelight `gas`, EK 1,3 (C2). |
| s37 | 1:33,0–1:38,8 | CU · 85 | `faceCam` 1,10 → 0,97 m | đẩy vào rất chậm | như s36 (EK 1,3), máy lệch +10° (C2). |
| s37w | 1:38,8–1:41,6 | WS · 28 | (17; 1,6; 1,2) → (8,8; 3,6; 0,6) | tĩnh | **V3:** hết tường trống: mặt cuối phố + phố rẽ ở giữa, hông + hốc cửa ở phải. |
| s39 | 1:41,6–1:46,0 | CU · 85 | `faceCam` 0,95 m | tĩnh | **(c) v4:** đứng TRƯỚC s38 — "Just…" (1:42,33) bắt đầu trên mặt Ida. facelight `elec`; phơi sáng × 0,8 (C2). Ảnh 4 kiểm mù: khung toàn cục 2510 (khung 72). |
| s38 | 1:46,0–1:47,4 | MS · 50 | (8,75; 2,45; −3,55) → (8,0; 0,95; −5,0) | tĩnh | **(c) v4:** đứng SAU s39 — Cas phản ứng từ giữa câu ("…who need it."). Cas ở `CAS_LAD` (8,0; −4,98): hai tay trên hai thanh thang. |
| s40 | 1:47,4–1:50,0 | CU insert · 50 | theo cần van | tĩnh | Nền thấy **hốc cửa ngay sau L11**. `hat_back` 0,35 (liên tục từ s36). |
| s40w | 1:50,0–1:52,0 | WS · 28 | như s37w | tĩnh | `hat_back` 0,35. |
| s41 | 1:52,0–1:53,5 | WS · 28 | (12,8; 1,5; 0,6) → (8,2; 1,2; −4,6) | tĩnh | Nền: hông nhà kho + hốc cửa. `hat_back` 0,35. **C3:** Ida (7,9; −4,4) trái, Cas (8,9; −4,6) phải; Cas ôm đèn (`casHug`). |
| s42a | 1:53,5–1:55,5 | MS · 45 | (10,4; 1,0; −0,6) → (7,6; 0,9; −3,3) | tĩnh | Hốc cửa ở ngay nền (Cas nhìn về nó, trái khung). **C3:** Ida lùi ra (6,8; −2,5), trái khung. **N2:** Cas ôm đèn sát ngực. |
| s42b | 1:55,5–1:57,5 | WS · 32 | (0,9; 1,25; 8,2) → (0,3; 1,1; 2,0) | tĩnh | Cas ôm đèn (`casHug`, như s41/s42a) đi vào `CAS_BAY` (−0,35; 2,55), quay ra vòm; **N7 (v3):** 1,45–2,0 s ngồi xổm, đặt đèn xuống nền (−0,38; 3,10) — tư thế cuối = tư thế mở s42. |
| s42 | 1:57,5–2:00,5 | MS · 40 (v2: 32) | (0,55; 0,66; 0,45) → (−0,15; 0,75; 4,5) | tĩnh | **V1:** Cas quay ra vòm, máy sau lưng lệch phải; Ida trái (x +1,25 miệng vòm), Cas phải. Ngoài vòm là phố trắng (bộ khoá cũ: nền đen). |
| s43 | 2:00,5–2:04,5 | EWS · 28 → 45 | bộ khoá s1 | dolly 12 m + zoom chậm về ô cửa | **C4:** trời đêm xanh đen có sao. **N8:** một ô hổ phách nhìn thấy, nền tối. **C-i (v4):** dolly 12 m về ô + 28 → 45 mm → ô lớn dần (≈ 10 × 15 px cuối shot). |
| s44 | 2:04,5–2:07,0 | WS · 21 | bộ khoá s6 + 0,5 m | đẩy vào | Ida không đạo cụ đèn lồng. |
| s45 | 2:07,0–2:09,0 | MS · 50 | 3/4 trước-phải bà, 1,75 m, thấp hơn mắt 0,3 m | tĩnh | Thấy **đồng hồ trong tay + mặt dưới vành mũ** (v2: máy sau vai, không thấy đồng hồ). |
| s46 | 2:09,0–2:12,0 | CU insert · 100 | theo lòng bàn tay | tĩnh | **(d) v4:** đứng TRƯỚC s45c; 9:53 → 10:00, kim giờ ăn khớp kim phút (chỉ tiến). A2 (c): nền tường ngõ. |
| s45c | 2:12,0–2:13,5 | CU · 200 | (150; 6,2; 0,4) → mặt đồng hồ | tĩnh | **(d) v4:** POV sau s46 — quảng trường 10:00:00, khớp giờ bà vừa vặn. |
| s47 | 2:13,5–2:15,5 | WS · 28 | (0,1; 1,45; −2,6) → (0; 1,3; 6) | tĩnh | **Bỏ đèn lồng ở hông Ida** (đã trao ở s41; v2 vẫn còn). |
| s48 | 2:15,5–2:20,5 | WS · 28 | (−1,45; 1,35; −1,55) → (0,45; 1,65; 1,6) | tĩnh; mờ về đen 1,5 s | Render mới. Cas vẫn gần đèn hơn vách (z −0,35; v2 −0,5), tay giơ cao (vai −150°, v2 −98°) → chim nằm TRÊN bóng đầu (v2: chim lẫn vào bóng đầu–thân). |

## 3. V1–V4 — trước / sau
### V1 — 2:00 (s42b/s42): Cas "mất mũ", tay to, ngồi xổm méo
- **Nguyên nhân (đo trên probe + hình học, không đoán):**
  1. Mũ **không rơi**: mũ len gắn khớp đầu (`cast3d.js`, `capG` con của `headG`); ở s42b (1:58) mũ đọc đúng.
  2. s42 v2: máy **chính diện** cậu, thấp 0,72 m, cách 2,5 m; đèn lồng nằm **giữa** máy và cậu.
     - Mặt và mũ ở ngoài nón sáng của đèn lồng (nắp chắn tia > 49°, luật 5A): mặt tối.
     - Mũ len màu kem #d6c9ae chỉ nhận dội ấm; quầng sprite đèn lồng phủ lên người.
     - Quả bông đỏ khuất sau đỉnh đầu vì máy thấp hơn đỉnh mũ → mũ đọc thành **"tóc vàng"**.
  3. Hai lòng bàn tay xoay 70° về phía kính, tức **về phía máy**: chính diện, xoè, gần máy hơn đầu 0,4–0,5 m → **tay to bất thường** (tay đã 1,30× theo sheet — trần đã duyệt, không đổi).
  4. Dáng xổm `warm_hands_copy` (hông −96°, gối 124°) nhìn thẳng từ trước → hai gối dồn giữa khung, thân ngắn lại → "méo".
- **Sửa (máy + dàn dựng):**
  - Cas quay mặt **ra vòm** (về phía Ida và phố trắng), đèn lồng trước mặt cậu.
  - Máy **sau lưng lệch phải**, lùi 2,3 m, thấp ngang vai (0,66 m), 40 mm.
  - Đầu + mũ len + **quả bông in trên nền phố trắng** qua vòm; tay thấy từ sau-bên; dáng xổm thấy từ sau.
  - Ida ở mép vòm (trái khung), Cas phải khung.
  - s42b: Cas dừng rồi quay người ra vòm để nối.
- **Bằng chứng:** `reports/m2/cong5/w2/V1_s42b-s42_truoc-tren_sau-duoi.jpg`.

### V2 — 1:20–1:29 (s33, s34): người và bóng lẫn nhau ("hai cậu bé")
- **Nguyên nhân (hình học v2):**
  - Cas sát vách (0,45 m) → bóng ×1,18: gần bằng người, rìa sắc, nằm gần như ngay sau lưng cậu (đèn x 0,05, Cas x 0,40 → lệch 0,06 m).
  - Ida đứng trùng bóng mình (lệch 0,18 m), áo tối trên nền bóng tối.
- **Sửa bằng quang học thật** (phóng đại = đèn → vách ÷ đèn → người). Đèn lồng cách vách 3,0 m, lệch trái (x −0,3); hai người tách ra hai bên đèn → bóng bị đẩy ra ngoài, lệch = (x người − x đèn) × (phóng đại − 1):

| | Cách vách | Đèn → người | Phóng đại | Cao bóng | Lệch bóng so với người |
|---|---|---|---|---|---|
| Ida v2 | 1,4 m | 1,6 m | ×1,88 | ≈ 3,0 m | 0,18 m (trùng) |
| **Ida W2** | 1,6 m | 1,4 m | **×2,14** | ≈ 3,5 m | **0,46 m trái** |
| Cas v2 | 0,45 m | 2,55 m | ×1,18 | ≈ 1,5 m | 0,06 m (ngay sau lưng) |
| **Cas W2** | 0,9 m | 2,1 m | **×1,43** | ≈ 1,9 m | **0,40 m phải** |

  - Tỷ lệ bóng bà / bóng cậu 1,87 → vẫn "hers, tall… his, small" (luật 3.2, 3.5).
  - Bóng cậu nay to hơn cậu 1,43× và mềm hơn: vùng nửa tối tăng 0,9/2,1 so với 0,45/2,55, tức ≈ 2,4× ở render nhiều mẫu.
  - Viền sáng: đèn lồng sau lưng + dội vách bên (uSide).
  - s34: máy lùi (30 mm). Trái → phải: Ida, bóng Ida, Cas, bóng Cas; người có màu, bóng phẳng.
- **Bằng chứng:** `V2_s33-s34_truoc-tren_sau-duoi.jpg`. Rủi ro còn lại: xem R1.

### V3 — cuối phố là tường trống (0:52 s23, 1:04 s27, 1:40 s37w)
- **Sửa:** dựng lại `sets_end.js`: nhà kho chữ L có khối (mục 5).
  - Mặt cuối phố x = −5, góc nam z = +2; hông nam z = −8,1 = tường chim + hốc cửa vòm sâu 4 m.
  - Gờ mái + máng nước, mái đá đen, 2 chòi thông gió, cửa kéo hàng + xà tời, cửa sổ cao có song, ống thoát nước, gờ chân tường.
  - Phố rẽ trái sau góc nam, cong (R 16 m), dốc xuống 5 %, hai dãy nhà theo cung.
  - Hậu cảnh: 5 dải mái xa (35–230 m) sau nhà kho + 3 dải cuối phố rẽ (hạ thấp dần); sương sáng lạnh sát mặt phố (sprite, không làm sáng trời).
  - Bộ tường chim (s25–s32) dùng **cùng** hàm → hết chân trời phẳng. Bộ hốc cửa có phố trắng bọc ngoài vòm.
- **Hồi quy đã bắt và bỏ:** phương án trung gian dời mặt nhà kho về x = 3,8 làm s37w thành tường trống lần nữa (probe p11), nên đã đổi sang nhà kho chữ L.
- **Bằng chứng:**
  - `V3_s27-s35-s37w_truoc-tren_sau-duoi.jpg`;
  - chỗ nối W1: `V3_noi-W1_s23-s24-s24c_sau.jpg`. Ảnh trước của s23 nằm ở `reports/m2/cong5/w1/s23_truoc-sau.jpg`.

### V4 — 1:02 (s26): mặt Ida tối, mắt ánh cam
- **Nguyên nhân:** v2 đặt bà ở (−0,6; 5,2).
  - L11 ở sau-bên, cách 1,9 m, góc ngẩng ≈ 40°: vành mũ che hết mặt.
  - Đèn lồng thắt lưng rọi từ dưới lên, cổ áo che cằm → chỉ tròng mắt bắt ánh ("mắt phát sáng").
- **Sửa (dàn dựng, nguồn có thật):**
  - Bà đứng ở (−3,8; 7,3), cách L11 3,5 m. L11 gần chính trước mặt (lệch ≈ 4°), góc ngẩng ≈ 25° → key trước lên mặt, vành chỉ che trán.
  - Máy 3/4 ở phía +x trục (Ida nhìn phải khung về Cas).
  - Hàm `facelight` của W3, chế độ `gas`: dội tường/đá, dưới, viền — tỷ lệ theo độ rọi L11 tại mặt. Probe: key 0,59–0,62; fill 0,12; under 0,07; rim 0,13; tổng 0,78–0,82.
  - Phơi sáng 3,4 (fl.exposure đề xuất 4,9–5,1 làm cháy nền trắng; chọn 3,4 để nền phố trắng còn chi tiết).
- **Bằng chứng:** `V4_s26_truoc-tren_sau-duoi.jpg`. Mắt không còn tự sáng; mặt đọc là bà cụ đội mũ, hoa tai, khăn.

## 4. D2 — mũ Ida #262a33 trên probe
Cách đo như W1: hộp chọn tay, 60 % điểm ảnh tối nhất, trung vị sRGB (`hat.py`).

| Khung | Nguồn trên mũ | Màu thấy | Sắc | Bão hoà | Kết luận |
|---|---|---|---|---|---|
| s40_a (L11 còn cháy, cạnh mũ) | lửa | #5a3f39 | 11° | 0,37 | **nâu xám** ✔ |
| s40_c (L11 tắt, chỉ điện) | điện | #1b1e2c | 229° | 0,39 | **đen xanh** ✔ |
| s36_b (L11 sát trên, 0,5 m) | lửa gần | #471d0d | 17° | 0,82 | nâu ấm, bão hoà cao (nguồn quá gần) |
| s26_b (L11 trước mặt, mũ ngược sáng trên nền tối) | lửa xa | #0a0407 | — | — | gần đen |

Cùng một khung s40 trước/sau khi tắt lửa cho đúng cặp "nâu xám / đen xanh" của D2. s36 bão hoà cao vì đèn cách mũ 0,5 m: ghi cho Cổng 7 (ánh sáng).

## 5. API `sets_end.js` cho W1 (s23) và cho P
- `buildStreetEnd(scene, o)` — `sets.js` gọi khi `x0 < 0`, **trước** khi dựng hai dãy nhà. Trả `endInfo`:
  - `houseX0N` = 18,5 (dãy bắc bắt đầu), `houseX0S` = −4;
  - `casSpot` = [14,3; −7,15]: sát tường 0,95 m, cách L11 7,1 m (B1);
  - `wallPost` = {x 17,0; z −5,9; range 8,5; ry; set(e); group; light}: cột điện trong sân (B1);
  - `bayWorld` {x 2,2; z −8,1}, `cornerWorld` {x −5; z 2}, `faceX` −5, `flankZ` −8,1;
  - `toWorld(v)`: hệ tường chim → thế giới; `group`, `warehouse`.
- Tuỳ chọn `o.endOpts = { far: false, fogGlow: 0…2 }`: tắt hậu cảnh xa (tiết kiệm) hoặc chỉnh sương sáng.
- `buildEndWallFrame(W, kit, o)`: toàn bộ cuối phố trong hệ tường chim.
- `buildWarehouse`, `buildLane`, `buildFarCity`, `makeKit`, `wallFromWorld`, `END` (hằng số địa lý).
- **Giữ nguyên:** L11 (8; −3,9), P5 (10,8; 3,9), `LAMP_X`, `POST_X`, `WALK_Z`, `ladderAt`. Không đụng `sets.js`.
- Đo khung s23 của W1 (máy W1, probe `after/s23_c`):
  - mặt vôi nhìn thấy: mặt cuối phố (tối, có cửa sổ, cửa kéo) + hông nhà kho trong bóng L11;
  - phố rẽ + dãy nhà cong ở mép trái; mái xa sau mặt cuối phố.
  - **Chưa đo** tỷ lệ diện tích vôi theo tiêu chí ≤ 20 % của W1 (ước lượng bằng mắt ≈ 20–25 %) → W1/P kiểm lại (R3).

## 6. Đề xuất gửi P / chủ dự án (hàng chờ, W2 không tự quyết)
- **Q-W2-1 — ĐÃ DUYỆT (world-rules v0.5):** tường chim là **hông nam** nhà kho (song song phố), không phải mặt chắn cuối phố như kịch bản gợi ("Cuối phố là bức tường…").
  - Ưu: một địa lý thống nhất cho cảnh 3–5; Cas cách L11 4 m; hốc cửa "vài bước dọc tường"; s37w hết tường trống.
  - Nhược: đổi cách hiểu "cuối phố"; bible mục 1 nên ghi rõ "nhà kho ở cuối phố; tường chim là mặt nhà kho nhìn ra đoạn cuối phố".
  - Cần P sửa `bible/world-rules.md` (v0.5) nếu duyệt.
- **Q-W2-2 — ĐÃ QUYẾT (chủ dự án):** bà kéo mũ lại khi rời đi; W2 dựng ở cuối s42 (2,2–2,8 s, 0,35 → 0), cảnh 6 giữ 0. Nội dung đề xuất gốc: sau s36 bà đẩy vành mũ (C4); W2 giữ `hat_back` 0,35 tới hết cảnh 5. Cảnh 6 (2 giờ sau) đang để 0.
  - Chọn: (a) giữ 0 (bà đã chỉnh lại mũ); (b) giữ 0,35 tới hết phim.
- **Q-W2-3 — đã xử lý hình (W1 thêm cột vào bộ phố, thấy ở s23, s24).** Còn lại mâu thuẫn ÁNH SÁNG C2 (chờ chủ dự án, phương án ở báo cáo giai đoạn D). Nội dung đề xuất gốc: cột bật 1:04 đặt ở (13,5; −4,2).
  - Đề xuất P thêm cột này vào `POST_X` hoặc `sets.js` (bật `WALL_POST_ON`), để s35–s42a thấy nó sáng.
  - Hoặc duyệt dùng P4 (x = 29) làm "cột phố chính cạnh nhà kho" và W2 dời cột trong bộ tường chim ra ngoài khung.
- **Q-W2-4 — ĐÃ QUYẾT: không quầng trắng chân trời.** luật v0.4 "ánh điện không làm sáng trời". Sương W2 đặt sát mặt phố, không chạm trời. W1 đề xuất "quầng trắng hắt lên trời ở chân trời" — **W2 không làm** vì trái luật; chờ chủ dự án nếu muốn.
- **Q-W2-5 — ĐÃ QUYẾT (chủ dự án, AUTHORSHIP @e850c0f): C-i máy đẩy rất chậm** (đã dựng ở v4: dolly 12 m + 28 → 45 mm). Nội dung đề xuất gốc — cỡ "một ô hổ phách" ở s43: ô nhà Cas hiện cách máy 130,9 m, ≈ 6–8 px ở 960 px (≈ 12–16 px ở 1080p), có quầng nhỏ; đọc được khi xem kỹ. W2 không tự đổi khung.
  - (a) Giữ như v3. Ưu: đúng tinh thần EWS lặp khung mở đầu. Nhược: khán giả có thể không bắt được ô. Chi phí 0.
  - (b) Chọn ô gần hơn (30–80 m) trên mặt nhà không bị điện rọi. Ưu: ô to gấp 2–3 lần. Nhược: bộ khoá s1 hầu như không có mặt nhà gần mà nền tối (probe v3: ô 75 m nằm trên tường hồng bị rọi, tương phản kém). Chi phí: 1–2 probe + render s43 (≈ 110 s).
  - (c) Giữ ô, thêm dolly/zoom rất chậm về phía ô trong 4 s. Ưu: dẫn mắt. Nhược: đổi chuyển máy đã duyệt ("cùng khung mở đầu"). Chi phí như (b).

- **(e) người/bóng hốc vòm (s33, s34, 1:18–1:26): không sửa ở layout** — dời Cổng 7 theo tiêu chí trong PLAN.md (quyết định chủ dự án).

## 7. Rủi ro
- **R1 (V2 còn lại):** bóng Cas vẫn là dáng một cậu bé (đúng kịch bản "his, small, standing right beside him"). Nay to hơn cậu 1,36×, lệch phải 0,25 m, mềm hơn; bóng Ida lệch trái bà 0,77 m (v3). Cần kiểm mù lần 4 (giai đoạn D) để xác nhận hết đọc "hai cậu bé".
- **R2 (v3):** C2 đã giải bằng B1 (cột trong sân, góc L11 tối tới P5); phần còn lại ở s33 (C5) đã sửa ở v3 — ngoài vòm tối lạnh.
- **R3:** tỷ lệ vôi ở s23 (tiêu chí W1 ≤ 20 %) chưa đo bằng số.
- **R4:** chim s32 và s48 đọc là "bóng to, mềm" nhưng hình chim chưa gọn (tay đơn giản ở previs). Cổng 6 cần tư thế tay chim thật (ngón xoè, cổ tay chéo) cho nguồn thấp.
- **R5:** thời gian render/khung tăng ở bộ tường chim (5,1 → 5,5–8 s/khung probe, máy dùng chung). Bộ phố cuối +20–30 % do hậu cảnh. Có `endOpts.far = false` cho shot không thấy xa.
- **R6:** mặt Ida đang đổi (W3 làm A3). Máy và ánh sáng s26/s36/s37/s39 đã chốt, không phụ thuộc hình mặt. Hệ số phơi sáng hiện hành (C2): s36/s37 EK 1,3; s39 × 0,8; s31 × 0,45.
