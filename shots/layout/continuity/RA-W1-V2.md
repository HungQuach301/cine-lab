# RÀ CONTINUITY — Cổng 6 · W1-v2 (phạm vi hẹp) — layout-v21

Người rà: agent continuity. Việc này chỉ báo lỗi, không sửa. Ngày 30/09/2026. Nhánh P, HEAD `ce70d4d` (đã merge W1-v2 @bff70cc). Không đọc mã trong `checks/`. Không commit.
**Phạm vi (chỉ thị chủ dự án, AUTHORSHIP 30/09 dòng "MỞ W1-v2"):** chỉ các shot W1-v2 đã sửa (s03, s05, s06, s13, s15, s22, s23, s24, s24c), nối s21 → s22 và s24 → s24c → s25.
Căn cứ: `shots/layout/continuity/RA-W1-V1.md` (L1–L16), `reports/m2/cong6/w1/BAO-CAO-W1-V2.md`, `bible/characters.md`, `bible/world-rules.md` (chỉ đọc), `shots/layout/continuity/canh-1.md` … `canh-4.md`, AUTHORSHIP mục "Cổng 6 — diễn hoạt".
Hình: `design/cong5/layout/out/layout-v21.mp4` (960×540, 24 fps, 3 372 khung, 140,5 s, có phụ đề); đối chứng `layout-v20.mp4`; bảng trước/sau `reports/m2/cong6/w1/sua-v2/`. Số đo: `layout-v21.motion.json` (vết tay/đầu trên màn hình) và stem `layout-v21.stems/sfx.flac`.
Quy ước: "khung" là khung toàn cục (giây × 24). **Ảnh bằng chứng ở `reports/m2/cong6/w1/ra-continuity-v2/`** (tạm, ngoài repo; tên tệp ghi từng dòng). P chép vào repo nếu cần.

> **Đường dẫn:** lệnh giao muốn nộp ở `shots/layout/continuity/RA-W1-V2.md`. Cấu hình phiên này chỉ cho ghi `reports/continuity.md` và cấm sửa tệp khác, nên báo cáo nằm ở đây. P chép sang nếu cần.

Mốc shot trong v21 (từ `camera/*.loc`): s03 204–251 · s05 288–383 · s06 384–455 · s13 948–995 · s15 1044–1079 · s21 1140–1187 · s22 1188–1259 · s23 1260–1331 · s24 1332–1379 · s24c 1380–1415 · s25 từ 1416.

## 0. Tóm tắt
- **L3 (CHẶN) ĐẠT:** ngón trỏ chạm mặt kính ở khung 403 (16,79 s) và 413 (17,21 s); tiếng gõ trong stem ở 16,800 và 17,200 s (đỉnh −13,8 / −14,6 dB). Không còn đầu hoặc tai xuyên mặt đồng hồ. **Nhưng W1-v2 gây lỗi mới ngay trong nhịp này:** khung 398 hiện một bàn tay khác trong đúng một khung (K1).
- **L4 (CHẶN) CHƯA ĐẠT ĐỦ:** nhịp ba đọc được (ba lần dang ra rồi khép vào ở 55,71 / 56,29 / 56,92 s), nhưng hai bàn tay ở ngang cằm, **dưới đáy lồng kính L11** khoảng 40–47 px (gần hai đầu người). Vì vậy trên hình chỉ thấy "dang tay, khép tay ba lần", chưa thấy "hơ tay vào đèn".
- L1, L2, s05, s13, s15 (L6), s03: đạt. L7 (s24c): chưa đạt rõ.
- **Lỗi mới:** 1 chặn đề xuất (K2: quả bông mũ Cas tan vào tường giữa s24c, sang s25 lại có), 3 nên sửa, 3 ghi nhận.

## 1. Đối chiếu L1–L7 của RA-W1-V1

| Mã | Shot | Yêu cầu | Kết quả trên v21 | Khung / bằng chứng |
|---|---|---|---|---|
| **L3** (CHẶN) | s06 | Ngón chạm hoặc gõ kính thấy rõ, khớp tiếng 16,80 / 17,20 s; đầu không xuyên mặt đồng hồ | **ĐẠT.** Ngón trỏ đi vào từ mép trên, móng thấy rõ, đầu ngón chạm vòng số 12. Có ngón ở khung 401–405 và 411–415, sâu nhất ở 403 và 413. Stem SFX: 16,800 và 17,200 s → khung 403,2 và 412,8, **lệch ≤ 0,2 khung**. Giữa hai lần gõ (406–410) ngón nhấc hẳn khỏi khung. Máy khoá: không thấy đầu hoặc tai lọt giữa máy và mặt số ở bất kỳ khung nào 384–455. Giờ 7:31, kim chỉ tiến. Lỗi phụ mới: K1, K3 | 398–416 · `E_L3_s06_go_kinh_day.jpg`, `E_L3_s06_cham_kinh_395_398_403_413.jpg` |
| **L4** (CHẶN) | s24 | Nhịp hơ tay đếm ba đọc được | **CHƯA ĐẠT ĐỦ.** (a) **Nhịp ba: đạt.** Hai tay dang ra rồi khép ba lần, đỉnh khép ở khung 1337, 1351, 1366 (55,71 / 56,29 / 56,92 s, khớp `canh-3.md` 55,7 / 56,3 / 56,9). Vết tay trên màn hình dịch khoảng 20 px ngang (tay trái 196–221, tay phải 135–155) so với ≤ 3 px ở v1; phóng to thì thấy rõ ba nhịp. (b) **"Hơ vào đèn": chưa đọc.** Tay ở y = 155–162, đầu ở y = 142, đáy lồng kính L11 ở y ≈ 115–122 (khung 960×540), nên hai tay ở ngang cằm, thấp hơn kính khoảng 40–47 px, không chạm và không ôm lấy kính. `canh-3.md` ghi "hai tay ngang kính", còn hình thì không như vậy. (c) Ở WS này Ida cao khoảng 110 px, biên độ 20 px, nên ở cỡ màn hình thường nhịp chỉ vừa đủ thấy. Mặt Ida cháy trắng (Cổng 7, có từ v1). **Đề xuất:** chủ dự án xem clip và chấm; nếu "hơ tay" là điều kiện của motif thì cần nâng hai tay lên ngang lồng kính | 1332–1379 · `E_L4_s24_dem_ba_zoom.jpg`, `E_L4_s24_toan_khung.jpg` |
| **L1** | s21 → s22 | Máy s22 cùng phía với s21 | **ĐẠT.** s21: Ida giữa-phải, cột và lồng đèn ở PHẢI, bà nhìn và giơ sào sang phải. s22: bà nhìn sang PHẢI, thân cột L10 ở mép phải khung. Cùng phía trục, không vượt trục | 1187 → 1188 · `E_L1_L2_s21_s22.jpg` |
| s22 3/4, MCU | s22 | Mặt 3/4 > 30°, giữ MCU | **ĐẠT góc (> 30°):** thấy mắt gần và một phần mắt xa, sống mũi phủ má xa; W1 đo 54–59°. **Cỡ cảnh: ghi nhận (K7).** Khung chỉ từ chóp mũ (đã cắt) tới khăn cổ, không thấy vai, nên đọc như **CU chặt** hơn là MCU | 1188–1259 · `E_s22_1080.jpg` |
| **L2** | s22 | Hết mẩu tay góc dưới-trái | **ĐẠT.** Góc dưới-trái chỉ có khăn và nền; không có da, măng sét hay tay áo ở mọi khung đã xem (1188, 1200, …, 1259) | `E_L1_L2_s21_s22.jpg` |
| s05 tay | s05 | Bàn tay không vỡ hình; hết tay lạ ở mép phải | **ĐẠT.** Bàn tay phải khép nhẹ, đủ năm ngón có khớp, nằm cạnh phải thân cột dưới lồng đèn. Không còn ngón nhọn tách rời như vuốt; mép phải không còn tay lạ. Ida nhìn PHẢI về đèn, khớp s04 (Ida trái cột) | 288–383 · `E_s05.jpg`, `E_s05_tay.jpg` |
| s13 xuyên cột | s13 | Tay không xuyên cột | **ĐẠT.** Tay trái giữ nhánh thanh móc suốt shot; đầu cúi xuống nhưng mũ và mặt vẫn ở bên phải thân cột, không lẫn vào cột. Nhấp trắng 948–958 là ý đồ (`canh-2.md`, "nhấp 2 lần"), có từ v20. Tài liệu lệch: K6 | 948–995 · `E_s13.jpg` |
| **L6** | s15 | Xuống từng bậc; thang lên vai không nhảy | **ĐẠT.** Xuống thang trong khoảng 1044–1064 (thấy rõ bậc, không trượt); chạm đất, lùi bước; thang nghiêng dần từ chỗ tựa cột lên vai trong 1067–1075 (khoảng 8 khung, xoay liên tục). Không còn nhảy một khung như 1070 → 1071 của v1 | `E_L6_s15_nhac_thang.jpg`, `E_s15.jpg` |
| s03 tốc độ leo | s03 | Leo chậm lại | **ĐẠT.** Đầu dịch 49 px trong 204–216 rồi dừng (v1 nhanh gần gấp đôi). Nhịp "hai bậc" chỉ thấy như một đoạn leo chậm dần; chấp nhận được. L4 bắt lửa sau khi bà tới đầu thang (tối ở 216, sáng ở 222): đúng thứ tự | 204–251 · `E_s03.jpg` |
| **L7** | s24c | Cas dựa tường đọc được | **CHƯA ĐẠT RÕ.** Đọc được khoảng cách sát tường nhờ bóng Cas nằm ngay sau người, và đầu ngả nhẹ. Nhưng thân gần thẳng đứng trên màn hình (ngả 6° gần như dọc trục máy); tay phải (bên trái khung) vẫn thấy buông cạnh hông, phía trước tường; tay kia khuất hẳn. Cả khung đọc thành "đứng trước tường, tay giấu sau lưng" chứ chưa ra "tựa lưng". Lỗi mới cùng chỗ: K2, K4 | 1380–1415 · `E_L7_s24c_s25.jpg` |

## 2. Lỗi MỚI do W1-v2 gây ra (trong phạm vi)

| Mã | Shot | Khung / giây | Mô tả | Mức | Bằng chứng |
|---|---|---|---|---|---|
| **K2** | s24c → s25 | 1387–1391 (57,79–57,96 s); mất tới 1415 | **Quả bông đỏ trên mũ Cas tan dần rồi biến mất giữa shot.** Ở 1380–1386 quả bông còn nguyên. Khi Cas ngả đầu tựa tường (tường cách 0,16 m), quả bông lún vào mặt tường: 1387–1390 còn vài mảnh đỏ lơ lửng tách khỏi đỉnh mũ, từ 1391 tới hết shot thì mũ trơn. Sang s25 (1416) quả bông có lại. Kết quả là đạo cụ nhận diện của Cas (`cas.json`: quả bông #a8483a) nhảy qua cắt và vỡ hình ngay trong một MS. v1 không có lỗi này (`sua-v2/s24c_truoc.jpg`: quả bông còn suốt shot) | **chặn (đề xuất)**: trang phục nhận diện, thấy rõ ở MS | `E_K2_s24c_qua_bong_1380-1391.jpg`, `E_L7_s24c_s25.jpg`, `E_noi_s24_s24c_s25.jpg` |
| **K1** | s06 | 398 (16,58 s), đúng 1 khung | **Một bàn tay khác bật ra trong một khung:** ngón cái hoặc ngón trỏ lớn che nửa trên mặt số, thêm một khối ngón ở mép phải; 397 và 399 không có. Chênh sáng 9,5/255 mỗi chiều, trong khi hai khung 397 ↔ 399 chỉ chênh 0,8. v20 không có (0,4). Nằm ngay trước nhịp gõ thứ nhất, nên người xem dễ thấy một chớp da trước khi gõ | nên sửa (sửa trước khi đóng L3) | `E_K1_s06_khung398.jpg` |
| **K3** | s06 | 440–455 (18,33–18,96 s) | **Nhịp cất đồng hồ (máy khoá) đọc kém:** đồng hồ vụt ra khỏi đáy khung chỉ trong 3 khung (440 → 443). Ở 441–442, một khối da phẳng, cạnh cắt thẳng (cổ tay hoặc cẳng tay sát máy) chiếm nửa khung, trông như lưới bị cắt. 444–455 gần đen, còn kính đèn lồng và một vòng tròn nhỏ lơ lửng bên trái. W1 đã khai rủi ro "đồng hồ rời khung" (§5), nhưng chưa khai khối da bị cắt. Chỗ tối cuối shot vẫn còn (tương tự phần phụ của L3 v1) | nên sửa | `E_K3_s06_cat_dong_ho.jpg` |
| **K4** | s24c | 1380–1415 | **Bóng dáng Cas như không có tay:** hai tay vòng ra sau lưng, vai áo phồng tròn, nên bên phải khung chỉ còn khối áo đỏ, không có cánh tay. v1 thấy cả hai cánh tay dọc thân (`sua-v2/s24c_truoc.jpg`). W1 đã khai "vai áo phồng rõ hơn một chút" (§5). Trên hình, mức lệch lớn hơn vậy và gần với lời chê "ma-nơ-canh" mà việc g muốn gỡ | nên sửa (hoặc chủ dự án chấp nhận) | `E_L7_s24c_s25.jpg` |
| **K5** | s24 | 1332–1379 | Hai tay đếm ba ở ngang cằm, dưới đáy lồng kính (chi tiết ở L4 (b)). Ghi riêng thành mã vì hình mâu thuẫn với `canh-3.md` ("hai tay ngang kính sau lần đếm ba") và với BAO-CAO-W1-V2 mục f ("khép áp vào hai mặt kính") | nên sửa (gắn với L4) | `E_L4_s24_dem_ba_zoom.jpg` |
| **K6** | tài liệu | — | (a) `canh-3.md` dòng 10 vẫn ghi s22 "máy 3/4 — lệch 45°… phía phố (+x) … bà nhìn sang **TRÁI** khung". Hình và báo cáo W1-v2 đều là phía −x, lệch −62°, bà nhìn **PHẢI**. (b) `canh-2.md` dòng 8 vẫn ghi "khi cúi (s13 0,5–1,3 s) về lại thân cột"; v2 giữ tay trái trên nhánh thanh móc cả shot. (c) `canh-1.md` s06 vẫn ghi "máy insert giữ đúng vị trí Cổng 5"; v2 khoá máy ở tư thế 2,3 s | ghi nhận (P sửa tài liệu) | — |
| **K7** | s22 | 1188–1259 | Cỡ cảnh chặt hơn MCU: chóp mũ bị cắt, đáy khung ở khăn cổ, không thấy vai. Góc gần nghiêng hẳn. Quyết định của chủ dự án là "3/4, giữ MCU"; W1 khai là MCU 85 mm. Chủ dự án chấm trên clip | ghi nhận | `E_s22_1080.jpg` |
| **K8** | s24 → s24c → s25 | 1379 → 1380; 1415 → 1416 | **Nối và trục: đạt.** s24: Ida và L11 TRÁI, Cas PHẢI sát tường. s24c: Cas ở phải khung, nhìn TRÁI về Ida (lia 9° để trống phía nhìn). s25: Cas cùng phía, quay lưng làm chim. Đổi chỗ 0,75 m qua cắt đã được chủ dự án duyệt (L8 cũ). Còn lại: K2 (quả bông) và độ sáng hồng ấm → tím (Cổng 7, đã biết) | ghi nhận | `E_noi_s24_s24c_s25.jpg` |

Kiểm thêm, không có lỗi mới:
- **Chớp một khung:** quét toàn bộ 9 shot đã sửa. Chỉ khung 398 là chớp thật (K1); 403–413 là chuyển động gõ.
- **Đèn đúng thứ tự:** L4 tối ở 216, sáng ở 222 (s03). L10 ở khung cuối s22. L11 tối ở 1260–1304, sáng từ khoảng 1308–1316 (s23). Như v1.
- **Giờ chỉ tiến:** s06 7:31.
- **Mũ Ida:** không nơ, không `hat_back`; mũ phớt đen ở s21, s22; nâu dưới lửa gần ở s05, s13 (D2 đã biết).
- **Trục s04 → s05 → s06, s15 → s19:** không đổi phía.
- **s23:** không có cột điện ở mé đèn khí; Cas ở phải, sát tường, khớp s24.

## 3. Tờ so nhân vật với model sheet (shot đã sửa, bằng mắt)

| Shot | Lệch thấy được |
|---|---|
| s05, s22 (Ida cận) | Mũ phớt không nơ, khăn đỏ sẫm quấn cao, hoa tai vàng ở dái tai, búi tóc bạc: đúng. s22 thấy vân tóc như len đan (L13 cũ) |
| s06 (tay Ida) | Đồng hồ 12 vạch, không chữ số, 2 kim, khuyên đồng: đúng |
| s13, s15, s23, s24 (Ida trung/xa) | Thang vác vai phải, đầu chúc về trước (s15); đèn lồng hông trái cháy: đúng |
| s24c (Cas) | Mũ len kem, tóc nâu ở gáy, áo len đỏ cổ lật cao: đúng. **Quả bông mất từ 1391 (K2); không thấy cánh tay (K4)** |

## 4. Số lỗi theo mức
- **Chặn:** L4 (còn mở, chưa đạt đủ) + K2 (mới, đề xuất chặn) = **2**
- **Nên sửa:** L7, K1, K3, K4, K5 = **5**
- **Ghi nhận:** K6, K7, K8 = **3**
- **Đạt:** L3, L1, L2, L6, s05, s13, s03, s22 3/4 (> 30°)

## 5. Việc đang chờ
- **Chủ dự án:** (1) chấm L4: nhịp ba đã đọc được nhưng tay chưa ở lồng kính, có tính là đạt motif "hơ tay" không; (2) nhận K2 là chặn hay không (quả bông mất giữa s24c); (3) L7 và K4: nhận s24c như hiện tại hay sửa; (4) cỡ s22 (K7).
- **P:** giao K1, K2, K3 (và L4/K5, L7/K4 nếu chủ dự án không nhận) cho W1; sửa tài liệu theo K6; chép báo cáo sang `shots/layout/continuity/RA-W1-V2.md` và ảnh bằng chứng từ `reports/m2/cong6/w1/ra-continuity-v2/` nếu cần.
- Không có chỉ số nào tôi tự đo nằm trong ±5 % quanh ngưỡng. Tôi không chạy luật máy.
