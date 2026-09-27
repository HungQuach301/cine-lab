# SHOT LIST — ANIMATIC "Last Round" (Cổng 4)

Sinh tự động từ `design/cong4/animatic/film.js` (nguồn duy nhất; sửa ở đó rồi chạy lại `make_shotlist.py`). Kịch bản: `scripts/last-round.fountain` nháp 2.

**48 shot · tổng 150.0 s (2:30,00) · 24 fps · 16:9.** Tiêu cự: mm tương đương full-frame 35 mm (FOV dọc = 2·atan(12/f)).

## Quy ước địa lý và luật 180°
- Phố Ostler chạy theo trục x. Quảng trường và đồng hồ nằm ở **phải khung**; nhà kho và ngọn thứ 11 nằm ở **trái khung**. Máy luôn đặt ở phía nam phố.
  - Cảnh 1–3: Ida đi **phải → trái**; sóng trắng tới từ **phải**.
  - Khi bà quay nhìn quảng trường (s11, s15), bà nhìn sang **phải**.
- Cảnh 4–5 (tường, hốc cửa): máy luôn ở **sau-phải** hai người; Ida **trái**, Cas **phải**.
  - Cận Ida nói L3 (s31) chụp qua vai phải Cas, vẫn ở cùng phía đường nối Ida–Cas.
- Cận thoại trên thang (s36–s39): Ida nhìn **lên phố (phải khung)**. Cas dưới chân thang nhìn **lên** (s38, máy cao gần mắt Ida).
- Match cut 8B (s16 → s17): hai mặt đồng hồ ở **cùng vị trí, cùng cỡ** trong khung.

## Sai khác previs so với thiết kế khoá (cần xử lý ở layout/Cổng 5)
- **Phố thẳng và phẳng.** Bản khoá (s1) là phố cong, dốc nhẹ. Khoảng cách: đèn khí 14 m; cột điện đặt theo chỉ số của s1.
- **Cảnh 3 là montage nén thời gian.** Nhịp bật cột điện chọn cho từng shot đọc được "nở hổ phách → trắng phủ", không theo một đồng hồ vật lý liên tục.
- **Các đạo cụ previs chưa có trang thiết kế:**
  - đồng hồ bỏ túi (theo kích thước sheet);
  - cột đồng hồ quảng trường (chép bố cục s1);
  - phòng Cas (s48).
- **Thang:**
  - khi Ida trèo, thang dựng ở phía bắc cột (như a_close_ida);
  - khi Ida đi, thang vác trên vai;
  - ở ngõ (s47), thang xuất hiện trên vai không qua nhịp nhặt.
- **Không có khẩu hình.** Thoại đặt đúng mốc nhưng môi không mấp máy (C′ chưa có rig miệng nói).
- **Tư thế ngoài sheet** (IDA_POSES_C4, film.js: đẩy mũ, xem đồng hồ, trao đèn…) là previs. Cần duyệt thành tư thế sheet trước khi animate thật.

## Cảnh 1 — Vòng đèn (0:00,00–0:26,00, 8 shot)

| # | Shot | Thời điểm | Dài (s) | Cỡ | Góc | mm | Chuyển máy | Nguồn sáng trong truyện | Thoại / âm | Hành động | Lý do chọn |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | s01 | 0:00,00–0:04,00 | 4.0 | EWS | cao, chúc ~20° | 28 | dolly vào rất chậm | trời chạng vạng hồng–tím; đèn khí các phố (chấm hổ phách) | nhạc tạm (ACE-Step M0) vào nhẹ; room tone gió cao | Các chấm hổ phách xuất hiện từng cái một khắp thành phố. | Mở phim đúng lựa chọn 1C: thành phố cuối chạng vạng, đèn khí hiện dần như những tâm hổ phách; đặt thế giới trước khi vào người. |
| 2 | s02 | 0:04,00–0:08,50 | 4.5 | WS | ngang tầm mắt (1,5 m) | 35 | tĩnh | trời chạng vạng + đèn khí L1–L3 | room tone phố chạng vạng; bước chân; nhạc tạm | Ida vác thang đi từ phải sang trái về cột L4. | Đặt địa lý phố: đèn đã thắp ở phải (sau lưng Ida), phố chưa thắp phía trái — hướng đi phải→trái giữ suốt cảnh 1–3. |
| 3 | s03 | 0:08,50–0:10,50 | 2.0 | MS | thấp, hất lên | 50 | tĩnh | đèn khí L4 vừa mồi (nguồn chính), trời chạng vạng | kẽo kẹt thang; tiếng xì khí; "phụp" (9,2 s) | Ida lên nốt bậc thang, tay phải mở van; ngọn L4 bắt lửa. | Góc thấp cho nghi thức: tay mở van, "phụp", hổ phách nở trên mặt bà. |
| 4 | s04 | 0:10,50–0:12,00 | 1.5 | WS | cao, từ bên kia phố | 28 | tĩnh | đèn khí L4 (có bóng) | room tone; lửa thở rất khẽ | Ida trên thang, hai tay đưa lên kính; bóng người + thang đổ dài lên tường nhà. | Cho thấy BÓNG của bà (bóng = dấu vết con người, luật thế giới mục 2): bóng dài, mềm trên mặt tiền và đá lát. |
| 5 | s05 | 0:12,00–0:16,00 | 4.0 | MCU | ngang mắt, 3/4 trước-trái | 85 | tĩnh (khung style frame a_close_ida) | đèn khí L4 ngay trước mặt (ấm), trời lạnh viền | THOẠI L1 "Evening, old street." (12,0–14,16); lửa thở | Hai lòng tay áp gần kính: một, hai, ba (12,3 / 12,9 / 13,5); nói L1; hạ tay. | Thói quen hơ tay đếm ba là mô-típ sẽ trả lại ở 2:07 (Cas). Cận đủ để đếm được ba nhịp tay và nghe lời chào con phố. |
| 6 | s06 | 0:16,00–0:20,00 | 4.0 | CU (insert) | chúc nhẹ, góc nhìn của Ida | 100 | tĩnh | đèn khí L4 phía trên | hai tiếng gõ kính (16,9 / 17,3); tích tắc rất khẽ | Dưới chân thang, Ida mở đồng hồ bỏ túi (7:52 — chậm 7 phút), gõ kính hai lần bằng móng tay, cất đi. | Gieo mô-típ đồng hồ chậm 7 phút (4A): gõ kính hai lần là thói quen thân thương; mặt chỉ có vạch, không chữ số. |
| 7 | s07 | 0:20,00–0:24,00 | 4.0 | WS | ngang tầm mắt | 35 | dolly ngang theo Ida (phải→trái) | đèn khí L4, L5 (vừa thắp — lược thời gian) | bước chân, thang kẽo kẹt; nhạc tạm | Ida vác thang đi qua cột L5; bóng đổ ngang đá lát, xoay theo vị trí cột. | Nhịp sáng–tối của phố đèn khí; bóng bà quét từ trước ra sau khi đi qua cột — cái sẽ mất ở cảnh 2. |
| 8 | s08 | 0:24,00–0:26,00 | 2.0 | WS (tele) | ngang tầm mắt | 135 | tĩnh | đèn khí dọc phố; đồng hồ quảng trường còn tắt | rơ-le "tách" xa (24,3); room tone | Ida đi về phía máy; xa sau lưng là quảng trường. | Tele nén phố: Ida nhỏ ở tiền cảnh, quảng trường và cột đồng hồ (chưa sáng) ở xa. Tiếng rơ-le "tách" báo điều sắp đến; bà không để ý. |

## Cảnh 2 — Bật điện (0:26,00–0:44,00, 6 shot)

| # | Shot | Thời điểm | Dài (s) | Cỡ | Góc | mm | Chuyển máy | Nguồn sáng trong truyện | Thoại / âm | Hành động | Lý do chọn |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 9 | s09 | 0:26,00–0:30,00 | 4.0 | MS | thấp, hất lên cột đồng hồ | 50 | tĩnh | mặt đồng hồ kính mờ phát trắng (nguồn mới) | rơ-le; mặt kính bật; chuông điện "DING" (27,0); rè điện bắt đầu | Mặt đồng hồ sáng trắng; hai kim đứng đúng giờ (8:00); chuông đánh một tiếng. | Thứ sáng đầu tiên của lưới điện là đồng hồ (luật thế giới mục 1): giờ mới, đúng giờ, lạnh. Góc thấp cho nó uy thế nhưng không phản diện. |
| 10 | s10 | 0:30,00–0:34,00 | 4.0 | EWS | cao, sau quảng trường | 28 | tĩnh | đèn điện (trắng phẳng) lan khỏi quảng trường; đèn khí còn lại | rè điện lớn dần; các tiếng "tách" nối tiếp | Sóng trắng lăn xuống dốc theo phố Ostler. | Toàn cảnh lặp lại khung mở đầu để đo thay đổi: tấm kính quanh quảng trường nhấp hai lần rồi đứng; từng khối phố bật lan xuống dốc. |
| 11 | s11 | 0:34,00–0:37,00 | 3.0 | MS | ngang, 3/4 trước-trái | 50 | tĩnh | đèn khí L7 vừa thắp (ấm), ánh trắng lờ mờ phía xa | rè điện từ xa; tách | Ida trên thang ở cột L7, quay đầu và vai về phía quảng trường. | Phản ứng: bà quay về phía quảng trường (phải khung = hướng sóng tới). |
| 12 | s12 | 0:37,00–0:40,00 | 3.0 | WS (qua vai) | cao ngang vai Ida, nhìn lên phố | 35 | tĩnh | cột điện x=85 bật; đèn khí L5, L6 chìm trong trắng | tách (38,2); rè điện | Lưng/vai Ida tiền cảnh trái; phía xa phố trắng dần. | Qua vai bà: thấy trắng nuốt những ngọn bà vừa thắp (L5, L6) — vũng hổ phách mỏng dần, dải tối giữa các cột biến mất. |
| 13 | s13 | 0:40,00–0:42,00 | 2.0 | MS | thấp nhẹ, 3/4 trước-phải | 50 | tĩnh | trắng tràn tới (nhấp 2 lần), đèn khí L7 còn đó nhưng chìm | rè điện gần; tách | Trắng tràn lên người Ida; bà cúi nhìn xuống đá lát. | Sóng tới chính bà: mặt bà đổi từ ấm sang trắng phẳng; bà nhìn xuống. |
| 14 | s14 | 0:42,00–0:44,00 | 2.0 | MS (chúc) | cao, chúc xuống đá lát | 28 | tĩnh | trắng phẳng (không bóng); vệt tối mờ dưới chân thang | rè điện đều; im | Ida giơ tay trái lên; nền đá không có bóng. | Hình then chốt cảnh 2: bóng dài đã mất; bà giơ tay — không gì động trên đá lát. |

## Cảnh 3 — Chạy đua (0:44,00–1:08,00, 10 shot)

| # | Shot | Thời điểm | Dài (s) | Cỡ | Góc | mm | Chuyển máy | Nguồn sáng trong truyện | Thoại / âm | Hành động | Lý do chọn |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 15 | s15 | 0:44,00–0:46,00 | 2.0 | WS | ngang tầm mắt | 35 | tĩnh | trắng phẳng (cột x=85); đèn khí L7 chìm | bước xuống thang; rè điện | Ida xuống thang, quay người nhìn về phía đồng hồ. | Bà xuống thang, quay nhìn ngược dốc về quảng trường (phải khung) — dẫn vào nhịp đồng hồ. |
| 16 | s16 | 0:46,00–0:48,50 | 2.5 | CU | tele, góc nhìn của Ida (POV) | 200 | tĩnh | mặt đồng hồ phát trắng | rè điện; tích tắc | Mặt đồng hồ điện: 8:00:30, kim phút lệch phải đỉnh 3°. | Match cut 8B, vế 1: mặt đồng hồ quảng trường, kim phút vừa qua đỉnh. |
| 17 | s17 | 0:48,50–0:51,00 | 2.5 | CU (insert) | POV của Ida, tay duỗi | 105 | tĩnh | trắng phẳng | tích tắc gần | Đồng hồ bỏ túi giơ ngang tầm mắt: 7:53:30. | Match cut 8B, vế 2: cùng vị trí, cùng cỡ — đồng hồ bỏ túi, kim phút còn cách đỉnh 42° (7 phút). "Trễ" đọc bằng hình, không chữ. |
| 18 | s18 | 0:51,00–0:52,40 | 1.4 | MS | ngang | 50 | tĩnh | trắng phẳng | hơi thở cười khẽ (chờ SFX/giọng có giấy phép — để trống); bước nhanh | Ida hạ đồng hồ, quay người về phía dốc xuống (trái khung). | Lần đầu sau bốn mươi năm bà trễ: một hơi cười khô, rồi vác thang đi nhanh. |
| 19 | s19 | 0:52,40–0:55,40 | 3.0 | WS | ngang | 35 | tĩnh | đèn khí L8 vừa thắp (có bóng) → trắng phủ | "phụp" L8 (52.4 s); tách + rè khi cột điện bật | Ida trên thang ở L8: hổ phách nở, bóng dài; vài giây sau trắng phủ, bóng tan trong 0,5 s. | Montage: ngọn thứ 8 nở hổ phách, bóng bà đổ dài — rồi cột điện x=57 bật, trắng xoá bóng. |
| 20 | s20 | 0:55,40–0:58,00 | 2.6 | WS | thấp | 28 | tĩnh | đèn khí L9 vừa thắp (có bóng) → trắng phủ | "phụp" L9 (55.4 s); tách + rè khi cột điện bật | Ida trên thang ở L9: hổ phách nở, bóng dài; vài giây sau trắng phủ, bóng tan trong 0,5 s. | Montage: ngọn thứ 9, góc thấp khác để nhịp lặp không nhàm; trắng tới nhanh hơn. |
| 21 | s21 | 0:58,00–1:00,00 | 2.0 | MCU (tay) | ngang, 3/4 | 85 | tĩnh | trắng phẳng; L10 chưa thắp | thang rung; sào gỗ va; hơi thở gấp | Ida trèo nhanh lên L10, sào mồi trượt khỏi tay (58,9), chụp lại (59,4). | Vội: trèo quá nhanh, tuột sào mồi rồi chụp lại — lần đầu thấy tay bà không vững. |
| 22 | s22 | 1:00,00–1:03,00 | 3.0 | MCU | ngang mắt, 3/4 | 85 | tĩnh | trắng phẳng; đèn khí L10 bắt lửa ở khung cuối (ấm lên mặt) | THOẠI L2 "Not yet... not yet." (60,0–62,88); "phụp" (62,95, sau câu thoại, tràn qua điểm cắt) | Ida lẩm bẩm, mở van; lửa bắt ngay khi câu dứt; hổ phách chìm trong trắng. | Lời thoại duy nhất của cảnh chạy đua; ngọn L10 bắt lửa ấm lên mặt bà rồi bị trắng dìm ngay. |
| 23 | s23 | 1:03,00–1:06,00 | 3.0 | WS | ngang, nhìn xuôi dốc về nhà kho | 28 | tĩnh | L11 bắt lửa; cột điện x=11 còn tắt; trắng từ phía sau | bước chạy; thang; "phụp" (65,0) | Ida hối hả tới L11, trèo, thắp. Hổ phách. | Ngọn cuối cùng cạnh bức tường vôi nhà kho; cột điện khối cuối còn TỐI (khe thời gian — luật thế giới mục 1). |
| 24 | s24 | 1:06,00–1:08,00 | 2.0 | MS | hơi cao, 3/4 trước-phải | 35 | tĩnh | đèn khí L11 (ấm) — vùng cuối phố chưa có điện | lửa thở; im lặng tương đối | Ida áp tay vào kính: một, hai, ba (66,2 / 66,8 / 67,4). Xa phía sau, Cas nhìn. | Nhịp đếm ba lần thứ hai; ở nền, cậu bé đứng ở tường nhìn bà — bà không thấy (gieo cảnh 4). |

## Cảnh 4 — Bức tường (1:08,00–1:34,00, 8 shot)

| # | Shot | Thời điểm | Dài (s) | Cỡ | Góc | mm | Chuyển máy | Nguồn sáng trong truyện | Thoại / âm | Hành động | Lý do chọn |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 25 | s25 | 1:08,00–1:13,00 | 5.0 | MS | ngang ngực, 3/4 sau-phải Cas | 45 | dolly vào rất chậm (0,3 m) | đèn khí L11 (key, có bóng) — cột điện cạnh tường còn tắt | lửa thở; vải sột soạt; im | Cas giơ hai tay làm chim; chim vỗ cánh chậm trên tường vôi. | Giới thiệu Cas bằng việc cậu làm: chim bóng từ đèn khí L11 (khung style frame b_cas_bird). |
| 26 | s26 | 1:13,00–1:16,00 | 3.0 | MS | ngang, 3/4 trước-trái Ida | 50 | tĩnh | đèn khí L11 sau lưng Ida; đèn lồng thắt lưng | lửa thở | Ida đứng cạnh cột L11 nhìn Cas. | Ida xuống thang, đứng xem, không gọi. Đèn lồng ở thắt lưng vẫn cháy (gieo cho 1:26). |
| 27 | s27 | 1:16,00–1:20,00 | 4.0 | WS | ngang, sau-phải | 28 | tĩnh | cột điện cạnh tường bật (76,3) — trắng phẳng; đèn khí L11 còn nhưng chìm | rơ-le "tách" (76,0); rè điện | Chim bóng xám dần rồi mất; tay Cas vẫn vỗ. | Khối cuối bật: tách, nhấp hai lần, đứng. Trắng phủ tường; chim nhạt dần trong 12 khung (luật 3.3) — tay vẫn còn, chỉ mất bóng. |
| 28 | s28 | 1:20,00–1:23,00 | 3.0 | MS | ngang ngực, 3/4 sau-phải Cas | 45 | tĩnh | trắng phẳng | rè điện; vải | Cas vỗ tay nhanh, mạnh; tường trắng trơn. | Cas vỗ mạnh hơn vào bức tường trống — không gì cả. |
| 29 | s29 | 1:23,00–1:26,00 | 3.0 | MCU | ngang mắt Cas, 3/4 trước-phải | 85 | tĩnh | trắng phẳng; phản ánh ấm rất nhẹ của đèn lồng | rè điện; im | Cas hạ tay, xoay người về phía Ida (trái khung), nhìn xuống đèn lồng. | Cas hạ tay, quay lại, thấy bà — rồi thấy đèn lồng hổ phách ở thắt lưng bà. Cậu không xin. |
| 30 | s30 | 1:26,00–1:28,00 | 2.0 | MS | ngang, sau-phải | 35 | tĩnh | đèn lồng tới gần tường (ấm) trong nền trắng | kim loại quai đèn; vải | Ida tháo đèn lồng, quỳ một gối bên trái Cas. | Ida tháo đèn lồng, quỳ cạnh cậu, cầm thấp sau tay cậu, cách tường một sải tay (≤ 0,7 m — luật 3.3). |
| 31 | s31 | 1:28,00–1:31,00 | 3.0 | MCU | ngang mắt Ida (quỳ), 3/4 sau-phải | 85 | tĩnh | đèn lồng ấm dưới mặt bà; trắng phẳng từ trên | THOẠI L3 "Go on, then." (88,0–90,3) | Ida quỳ, quay đầu về Cas, nói L3. | Lời mời, không dạy: bà đưa ánh sáng, cậu tự làm. |
| 32 | s32 | 1:31,00–1:34,00 | 3.0 | WS | ngang, sau-phải | 35 | tĩnh | đèn lồng thấp sau tay Cas (key ấm, có bóng) trong nền trắng | Cas cười khẽ (chờ SFX có giấy phép — để trống); nhạc tạm vào | Cas giơ tay vào quầng hổ phách; chim to hiện trên tường và bay. | Chim trở lại, TO hơn, ấm, rìa mềm (tay gần nguồn — luật 3.2, 3.3) và bay. |

## Cảnh 5 — Ngọn cuối (1:34,00–2:10,00, 10 shot)

| # | Shot | Thời điểm | Dài (s) | Cỡ | Góc | mm | Chuyển máy | Nguồn sáng trong truyện | Thoại / âm | Hành động | Lý do chọn |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 33 | s33 | 1:34,00–1:42,00 | 8.0 | WS | ngang 1,35 m, "tranh trong tranh" | 32 | dolly vào chậm (1 m) | đèn lồng trên nền đá (nguồn thấp); ngoài vòm: điện phẳng | nhạc tạm; bước chân vào hốc; rè điện xa | Ida đặt đèn lồng, hai người bước qua, đứng giữa đèn và vách; hai bóng hiện. | Hình trung tâm (7A, khung style frame c_s5_wide): trong hốc cửa khuất điện, đèn lồng dưới đất, hai bóng người vươn cao lên vách; ngoài vòm phố trắng không bóng. |
| 34 | s34 | 1:42,00–1:44,00 | 2.0 | MS (qua vai) | 3/4 sau-phải, cạnh đèn lồng | 35 | tĩnh | đèn lồng sau lưng, viền má và mép mũ | lửa thở; nhạc tạm | Ida ngửa nhìn bóng, tay đặt lên ngực. | Ida nhìn hai cái bóng một lúc lâu (khung style frame c_s5_medium). |
| 35 | s35 | 1:44,00–1:48,00 | 4.0 | WS | ngang, xuôi dốc | 28 | tĩnh | đèn khí L11 nhạt (vệt vàng yếu); điện phẳng khắp phố | bước chân; thang; rè điện | Ida bước ra khỏi hốc, tới thang, trèo; Cas chạy theo giữ thang. | Ngọn cuối còn cháy nhạt trong trắng; bà trèo lên lần cuối, Cas theo và giữ thang bằng hai tay. |
| 36 | s36 | 1:48,00–1:50,00 | 2.0 | MCU | ngang mắt, gần chính diện | 85 | tĩnh | đèn khí L11 nhạt + trắng phẳng | vải dạ; hơi thở | Tay trái đưa lên vành mũ (hat_push_a), đẩy vành lên, mũ ngả ra sau (hat_push_b). | Quyết định C4 của chủ dự án: bà TỰ đẩy vành mũ ra sau trước câu thoại — mặt thoáng ra cho lời từ biệt. |
| 37 | s37 | 1:50,00–1:57,00 | 7.0 | CU | ngang mắt, gần chính diện | 85 | đẩy vào rất chậm | đèn khí L11 nhạt (ấm yếu một bên mặt) + trắng phẳng | THOẠI L4 (110,0–…) "That's the last one, then. Goodnight, old street." | Ida nhìn lên phố (phải khung), tay đặt trên van. | Lời từ biệt, vế đầu: cười buồn. Máy đẩy vào không nhận ra được, để khán giả lại gần bà. |
| 38 | s38 | 1:57,00–1:59,50 | 2.5 | MS | cao, chúc xuống (gần mắt Ida) | 50 | tĩnh | trắng phẳng; ấm rất yếu từ L11 trên cao | L4 tiếp (ngoài hình) | Cas giữ thang, ngửa mặt nhìn lên. | Phản ứng của Cas: cậu giữ thang, ngước nhìn bà — người nghe câu nói thay khán giả. |
| 39 | s39 | 1:59,50–2:04,10 | 4.6 | CU | ngang mắt, gần chính diện | 85 | tĩnh | đèn khí L11 nhạt + trắng phẳng | THOẠI L4 (…–124,08) "You'll be brighter now. Just... keep a little dark for the ones who need it." | Ida nghẹn, một giọt nước mắt; mắt vẫn nhìn lên phố. | Vế cuối, giọng vỡ: "keep a little dark for the ones who need it" — chủ đề phim trong một câu. |
| 40 | s40 | 2:04,10–2:05,60 | 1.5 | CU (insert) | ngang van | 100 | tĩnh | ngọn L11 tắt (124,6); trắng phẳng không đổi | van kim loại; tiếng xì tắt | Tay phải Ida gạt van; lửa co lại và tắt. | Hành động không lời: tay vặn van, ngọn đèn khí cuối cùng của thành phố tắt. |
| 41 | s41 | 2:05,60–2:07,00 | 1.4 | WS | ngang | 28 | tĩnh | trắng phẳng; đèn lồng ấm trong tay | rè điện đều | Ida chìa đèn lồng; Cas đón bằng hai tay. | "Không gì khác thay đổi": phố trắng y nguyên. Dưới chân thang bà trao đèn lồng; cậu nhận bằng hai tay. |
| 42 | s42 | 2:07,00–2:10,00 | 3.0 | MS | thấp (ngang đèn lồng), 3/4 trước-phải Cas | 45 | tĩnh | đèn lồng ấm trên nền đá (dưới mặt Cas); trắng phẳng | lửa đèn lồng thở; nhạc tạm vào lại | Cas đặt đèn xuống, ngồi xổm, áp tay: một, hai, ba (127,5 / 128,1 / 128,7). | Trả mô-típ: không ai bảo, Cas hơ hai lòng tay trên kính đếm ba — đúng như bà. Ida (nền) thấy, không nói. |

## Cảnh 6 — Ô cửa (2:10,00–2:30,00, 6 shot)

| # | Shot | Thời điểm | Dài (s) | Cỡ | Góc | mm | Chuyển máy | Nguồn sáng trong truyện | Thoại / âm | Hành động | Lý do chọn |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 43 | s43 | 2:10,00–2:14,00 | 4.0 | EWS | cao (cùng khung mở đầu) | 28 | dolly vào rất chậm | đèn điện khắp nơi; một ô cửa đèn lồng | rè điện toàn thành phố; nhạc tạm | Toàn cảnh tĩnh; một ô vàng. | Lặp khung mở đầu để đo cái đã mất: thành phố trắng đều, không ngủ; giữa khung một ô cửa hổ phách. |
| 44 | s44 | 2:14,00–2:17,00 | 3.0 | WS | thấp, hất lên ô cửa | 21 | đẩy vào chậm | đèn lồng trên bậu cửa sổ (qua ô kính); điện chỉ lọt miệng ngõ | rè điện xa, nghẹt; im | Ida đứng dưới cửa sổ, ngửa nhìn ô vàng. | Trong ngõ khuất điện, dưới ánh cửa sổ nhà Cas, bóng bà — ngắn, nhạt — nằm lại trên đá lát (khung style frame d_s6_alley). |
| 45 | s45 | 2:17,00–2:19,00 | 2.0 | MS | ngang | 50 | tĩnh | ánh cửa sổ ấm từ trên | tích tắc; rè điện xa | Ida lấy đồng hồ, nhìn nó, rồi ngẩng nhìn về phía miệng ngõ. | Bà lấy đồng hồ ra, nhìn từ đồng hồ sang mặt đồng hồ quảng trường trên mái (qua miệng ngõ). |
| 46 | s46 | 2:19,00–2:22,00 | 3.0 | CU (insert) | chúc nhẹ | 100 | tĩnh | ánh cửa sổ ấm | núm vặn lách cách; tách gập | Ngón cái vặn núm; kim phút chạy từ 318° lên 360°; bàn tay khép lại. | 9B: kim phút tiến 42° lên trùng 12 — bà nhận giờ mới. Gập đồng hồ, KHÔNG gõ kính. |
| 47 | s47 | 2:22,00–2:25,00 | 3.0 | WS | ngang, sau lưng Ida | 28 | tĩnh | ánh cửa sổ (sau lưng) → điện phẳng ở miệng ngõ | bước chân; thang; rè điện lớn dần ở miệng ngõ | Ida vác thang đi từ dưới cửa sổ ra miệng ngõ. | Bà vác thang đi ra miệng ngõ; bóng mờ của bà mỏng dần rồi tan trong trắng (luật 3.5). |
| 48 | s48 | 2:25,00–2:30,00 | 5.0 | WS | ngang, sau lưng Cas | 28 | tĩnh; mờ dần về đen (148,5–150) | đèn lồng trên bậu (nguồn duy nhất, hổ phách trọn khung) | nhạc tạm (kết); lửa thở | Cas làm chim; chim bay ngang tường; FADE OUT. | Kết 2B: đèn lồng trên bậu, Cas quay lưng, chim to và mềm mở cánh bay ngang tường. Ida đã đi trước. |

## Thời gian render thật (960×540, 1 mẫu, không DOF)

| Shot | Khung | Dựng cảnh (s) | s/khung (TB) | s/khung (max) | Tổng (s) |
|---|---|---|---|---|---|
| s01 | 96 | 1.9 | 0.73 | 2.50 | 73 |
| s02 | 108 | 1.4 | 0.68 | 4.92 | 77 |
| s03 | 48 | 1.5 | 0.75 | 4.09 | 38 |
| s04 | 36 | 1.3 | 0.69 | 4.13 | 27 |
| s05 | 96 | 1.6 | 0.90 | 4.09 | 89 |
| s06 | 96 | 1.5 | 0.78 | 4.04 | 77 |
| s07 | 96 | 1.3 | 0.60 | 4.13 | 60 |
| s08 | 48 | 1.3 | 0.71 | 4.46 | 36 |
| s09 | 96 | 0.2 | 0.40 | 2.46 | 39 |
| s10 | 96 | 1.6 | 0.71 | 2.11 | 71 |
| s11 | 72 | 1.4 | 0.69 | 4.12 | 52 |
| s12 | 72 | 1.4 | 0.67 | 4.09 | 50 |
| s13 | 48 | 1.4 | 0.72 | 4.09 | 37 |
| s14 | 48 | 1.4 | 0.65 | 4.06 | 33 |
| s15 | 48 | 1.3 | 0.51 | 3.59 | 27 |
| s16 | 60 | 0.2 | 0.41 | 2.57 | 25 |
| s17 | 60 | 1.3 | 0.62 | 3.17 | 39 |
| s18 | 34 | 1.3 | 0.54 | 3.44 | 20 |
| s19 | 72 | 1.3 | 0.65 | 4.10 | 49 |
| s20 | 62 | 1.4 | 0.68 | 4.11 | 45 |
| s21 | 48 | 1.5 | 0.56 | 3.06 | 29 |
| s22 | 72 | 2.1 | 0.67 | 4.82 | 52 |
| s23 | 72 | 1.4 | 0.67 | 4.74 | 51 |
| s24 | 48 | 1.5 | 0.67 | 4.31 | 35 |
| s25 | 120 | 0.8 | 0.94 | 4.14 | 115 |
| s26 | 72 | 0.9 | 0.98 | 4.43 | 72 |
| s27 | 96 | 0.8 | 0.93 | 4.16 | 91 |
| s28 | 72 | 0.8 | 0.98 | 4.33 | 72 |
| s29 | 72 | 0.8 | 1.08 | 4.29 | 79 |
| s30 | 48 | 0.8 | 1.05 | 4.80 | 52 |
| s31 | 72 | 0.9 | 1.21 | 4.56 | 89 |
| s32 | 72 | 0.8 | 1.13 | 5.08 | 83 |
| s33 | 192 | 1.5 | 0.55 | 3.55 | 109 |
| s34 | 48 | 1.5 | 0.69 | 3.61 | 36 |
| s35 | 96 | 1.5 | 0.54 | 4.29 | 54 |
| s36 | 48 | 1.9 | 0.65 | 4.16 | 34 |
| s37 | 168 | 1.9 | 0.72 | 4.06 | 126 |
| s38 | 60 | 2.9 | 0.74 | 7.13 | 49 |
| s39 | 110 | 2.0 | 0.64 | 4.09 | 74 |
| s40 | 36 | 1.5 | 0.58 | 3.84 | 23 |
| s41 | 34 | 1.6 | 0.63 | 4.30 | 24 |
| s42 | 72 | 2.1 | 0.64 | 5.06 | 49 |
| s43 | 96 | 1.7 | 0.80 | 2.50 | 79 |
| s44 | 72 | 1.6 | 0.72 | 5.04 | 55 |
| s45 | 48 | 1.6 | 0.68 | 4.38 | 35 |
| s46 | 72 | 1.6 | 0.69 | 3.81 | 52 |
| s47 | 72 | 1.6 | 0.70 | 4.91 | 53 |
| s48 | 120 | 0.6 | 0.57 | 2.13 | 70 |
