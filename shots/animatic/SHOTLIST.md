# SHOT LIST — ANIMATIC "Last Round" (Cổng 4 · v2)

Sinh tự động từ `design/cong4/animatic/film.js` (nguồn duy nhất; sửa ở đó rồi chạy lại `make_shotlist.py`). Kịch bản: `scripts/last-round.fountain` nháp 3. Luật thế giới v0.4.

**52 shot · tổng 142.5 s (2:22,50) · 24 fps · 16:9.** Tiêu cự: mm tương đương full-frame 35 mm (FOV dọc = 2·atan(12/f)).

## Quy ước địa lý và luật 180°
- Phố Ostler chạy theo trục x. Quảng trường và đồng hồ nằm ở **phải khung**; nhà kho và ngọn thứ 11 nằm ở **trái khung**. Máy luôn đặt ở phía nam phố.
  - Cảnh 1–3: Ida đi **phải → trái**; sóng trắng tới từ **phải**.
  - Khi bà quay nhìn quảng trường (s11), bà nhìn sang **phải**; s15 bà quay về dốc xuống (**trái**).
- Cảnh 4–5 (tường, hốc cửa): máy luôn ở **sau-phải** hai người; Ida **trái**, Cas **phải**.
  - Cận Ida nói L3 (s31) chụp qua vai phải Cas, vẫn ở cùng phía đường nối Ida–Cas.
- Cận thoại trên thang (s36–s39): Ida nhìn **lên phố (phải khung)**. Cas dưới chân thang nhìn **lên** (s38, máy cao gần mắt Ida).
- Cảnh 5 cuối (s42a–s42): Cas đi từ phố trắng (ngoài) vào vòm hốc cửa (trong); s42 máy đặt TRONG hốc nhìn ra vòm, Ida đứng ở miệng vòm.

## Ba nhịp đồng hồ (giờ tiến; lý do từng nhịp ở cột "Lý do chọn")
- **Nhịp 1 (s06, 0:16):** đồng hồ bỏ túi 7:31 — gieo mô-típ chậm 7 phút, gõ kính.
- **Nhịp 2 (s09 → s09w, 0:25–0:30) = lúc bật điện:** đồng hồ quảng trường sáng đúng 8:00 + chuông; cắt sang đồng hồ bỏ túi 7:53.
- **Nhịp 3 (s45 → s45c → s46, 2:09–2:15):** đồng hồ bỏ túi 9:53, đồng hồ quảng trường 10:00; bà vặn lên 10:00, gập lại không gõ.

## Nguồn sáng điện thấy được và góc tối (chỉ đạo chủ dự án)
- Bóng đèn điện nhấp hai lần rồi đứng trong khung: s10e (quảng trường), s12 (x=85), s19 (x=57), s27 (cột phố chính cạnh nhà kho), s37w (cột góc — đoạn cáp cuối).
- Góc ngọn 11 tối từ s23 tới giữa s37w (luật thế giới v0.4, "đoạn cáp cuối").

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

## Cảnh 1 — Vòng đèn (0:00,00–0:25,00, 8 shot)

| # | Shot | Thời điểm | Dài (s) | Cỡ | Góc | mm | Chuyển máy | Nguồn sáng trong truyện | Thoại / âm | Hành động | Lý do chọn | Nguồn khung |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | s01 | 0:00,00–0:04,00 | 4.0 | EWS | cao, chúc ~20° | 28 | dolly vào rất chậm | trời chạng vạng hồng–tím; đèn khí các phố (chấm hổ phách) | nhạc tạm (ACE-Step M0) vào nhẹ; room tone gió cao | Các chấm hổ phách xuất hiện từng cái một khắp thành phố. | Mở phim đúng lựa chọn 1C: thành phố cuối chạng vạng, đèn khí hiện dần như những tâm hổ phách; đặt thế giới trước khi vào người. | tái dùng v1:s01 |
| 2 | s02 | 0:04,00–0:08,50 | 4.5 | WS | ngang tầm mắt (1,5 m) | 35 | tĩnh | trời chạng vạng + đèn khí L1–L3 | room tone phố chạng vạng; bước chân; nhạc tạm | Ida vác thang đi từ phải sang trái về cột L4. | Đặt địa lý phố: đèn đã thắp ở phải (sau lưng Ida), phố chưa thắp phía trái — hướng đi phải→trái giữ suốt cảnh 1–3. | render v2 |
| 3 | s03 | 0:08,50–0:10,50 | 2.0 | MS | thấp, hất lên | 50 | tĩnh | đèn khí L4 vừa mồi (nguồn chính), trời chạng vạng | kẽo kẹt thang; tiếng xì khí; "phụp" (9,2 s) | Ida lên nốt bậc thang, tay phải mở van; ngọn L4 bắt lửa. | Góc thấp cho nghi thức: tay mở van, "phụp", hổ phách nở trên mặt bà. | render v2 |
| 4 | s04 | 0:10,50–0:12,00 | 1.5 | WS | cao, từ bên kia phố | 28 | tĩnh | đèn khí L4 (có bóng) | room tone; lửa thở rất khẽ | Ida trên thang, hai tay đưa lên kính; bóng người + thang đổ dài lên tường nhà. | Cho thấy BÓNG của bà (bóng = dấu vết con người, luật thế giới mục 2): bóng dài, mềm trên mặt tiền và đá lát. | render v2 |
| 5 | s05 | 0:12,00–0:16,00 | 4.0 | MCU | ngang mắt, 3/4 trước-trái | 85 | tĩnh (khung style frame a_close_ida) | đèn khí L4 ngay trước mặt (ấm), trời lạnh viền | THOẠI L1 "Evening, old street." (12,0–14,16); lửa thở | Hai lòng tay áp gần kính: một, hai, ba (12,3 / 12,9 / 13,5); nói L1; hạ tay. | Thói quen hơ tay đếm ba là mô-típ sẽ trả lại ở 2:07 (Cas). Cận đủ để đếm được ba nhịp tay và nghe lời chào con phố. | render v2 |
| 6 | s06 | 0:16,00–0:19,00 | 3.0 | CU (insert) | chúc nhẹ, góc nhìn của Ida | 100 | tĩnh | đèn khí L4 phía trên; trời chạng vạng | hai tiếng gõ kính; tích tắc rất khẽ | Dưới chân thang, Ida mở đồng hồ bỏ túi (7:31 — giờ thật 7:38), gõ kính hai lần bằng móng tay, cất đi. | ĐỒNG HỒ NHỊP 1 — gieo mô-típ đồng hồ chậm 7 phút (4A): đồng hồ bỏ túi chỉ 7:31; gõ kính hai lần là thói quen thân thương. Mặt chỉ có vạch, không chữ số. | render v2 |
| 7 | s07 | 0:19,00–0:23,00 | 4.0 | WS | ngang tầm mắt | 35 | dolly ngang theo Ida (phải→trái) | đèn khí L4, L5 (vừa thắp — lược thời gian) | bước chân, thang kẽo kẹt; nhạc tạm | Ida vác thang đi qua cột L5; bóng đổ ngang đá lát, xoay theo vị trí cột. | Nhịp sáng–tối của phố đèn khí; bóng bà quét từ trước ra sau khi đi qua cột — cái sẽ mất ở cảnh 2. | render v2 |
| 8 | s08 | 0:23,00–0:25,00 | 2.0 | WS (tele) | ngang tầm mắt | 135 | tĩnh | đèn khí dọc phố; đồng hồ quảng trường còn tắt | rơ-le "tách" xa; room tone | Ida đi về phía máy; xa sau lưng là quảng trường. | Tele nén phố: Ida nhỏ ở tiền cảnh, quảng trường và cột đồng hồ (chưa sáng) ở xa. Tiếng rơ-le "tách" báo điều sắp đến; bà không để ý. | render v2 |

## Cảnh 2 — Bật điện (đêm) (0:25,00–0:43,50, 8 shot)

| # | Shot | Thời điểm | Dài (s) | Cỡ | Góc | mm | Chuyển máy | Nguồn sáng trong truyện | Thoại / âm | Hành động | Lý do chọn | Nguồn khung |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 9 | s09 | 0:25,00–0:28,00 | 3.0 | MS | thấp, hất lên cột đồng hồ | 50 | tĩnh | mặt đồng hồ kính mờ phát trắng (nguồn điện đầu tiên); trời đêm | rơ-le; mặt kính bật; chuông điện "DING"; rè điện bắt đầu | Mặt đồng hồ bật sáng trắng; hai kim đứng đúng 8:00; chuông đánh một tiếng. | ĐỒNG HỒ NHỊP 2a — thứ sáng đầu tiên của lưới điện là đồng hồ (luật thế giới mục 1): mặt kính sáng trắng đúng 8:00, chuông đánh. Nền trời đêm có sao: đây là ĐÊM, ánh trắng sắp tới là đèn điện, không phải bình minh. | render v2 |
| 10 | s09w | 0:28,00–0:30,00 | 2.0 | CU (insert) | POV của Ida, tay giơ | 105 | tĩnh | đèn khí L6 (ấm) trên tay; trời đêm | dư âm chuông; tích tắc gần | Ida (dưới cột L6) giơ đồng hồ bỏ túi ngang tầm mắt: 7:53. | ĐỒNG HỒ NHỊP 2b — cắt khớp ngay sau tiếng chuông: đồng hồ bỏ túi của bà chỉ 7:53. Giờ mới đã tới mà giờ của bà còn 7 phút: "trễ" đọc bằng hình, không chữ. | render v2 |
| 11 | s10e | 0:30,00–0:32,00 | 2.0 | MS (chèn) | thấp, hất lên đầu cột điện | 35 | tĩnh | bóng đèn điện quảng trường (trắng lạnh, loá) — nguồn thấy trong khung | tách rơ-le gần; bóng đèn rít; rè điện 50 Hz | Bóng đèn tối → sáng → tắt → sáng → đứng trắng; vũng trắng phẳng tràn xuống đá lát. | NGUỒN ĐIỆN THẤY ĐƯỢC: bóng đèn điện trên cột quảng trường nhấp hai lần rồi đứng trắng (kịch bản dòng 48), loá lạnh, gắt, trên nền trời đêm có sao. Đồng hồ vừa sáng ở hậu cảnh. | render v2 |
| 12 | s10 | 0:32,00–0:35,00 | 3.0 | EWS | cao, sau quảng trường | 28 | tĩnh | đèn điện (trắng phẳng) lan khỏi quảng trường; đèn khí còn lại | rè điện lớn dần; các tiếng "tách" nối tiếp | Sóng trắng lăn xuống dốc theo phố Ostler; một đoạn cuối phố còn hổ phách. | Toàn cảnh lặp khung mở đầu để đo thay đổi, nay là ĐÊM (trời xanh đen, không hồng): tấm kính quanh quảng trường đứng trắng, từng khối phố bật lan xuống dốc. Khối cuối cạnh nhà kho CHƯA bật (đoạn cáp cuối). | render v2 |
| 13 | s11 | 0:35,00–0:37,00 | 2.0 | MS | ngang, 3/4 trước-trái | 50 | tĩnh | đèn khí L7 vừa thắp (ấm), ánh trắng lờ mờ phía xa | rè điện từ xa; tách | Ida trên thang ở cột L7, quay đầu và vai về phía quảng trường. | Phản ứng: bà quay về phía quảng trường (phải khung = hướng sóng tới). | render v2 |
| 14 | s12 | 0:37,00–0:39,50 | 2.5 | WS (qua vai) | cao ngang vai Ida, nhìn lên phố | 35 | tĩnh | cột điện x=85 bật; đèn khí L5, L6 chìm trong trắng | tách; rè điện | Lưng/vai Ida tiền cảnh trái; phía xa bóng đèn điện bật, phố trắng dần. | Qua vai bà: bóng đèn cột điện x=85 nhấp hai lần rồi đứng (nguồn thấy được); trắng nuốt những ngọn bà vừa thắp (L5, L6) — vũng hổ phách mỏng dần. Trời đêm phía trên. | render v2 |
| 15 | s13 | 0:39,50–0:41,50 | 2.0 | MS | thấp nhẹ, 3/4 trước-phải | 50 | tĩnh | trắng tràn tới (nhấp 2 lần), đèn khí L7 còn đó nhưng chìm | rè điện gần; tách | Trắng tràn lên người Ida; bà cúi nhìn xuống đá lát. | Sóng tới chính bà (0:40, câu hỏi c1): mặt bà đổi từ ấm sang trắng phẳng; bà nhìn xuống. | render v2 |
| 16 | s14 | 0:41,50–0:43,50 | 2.0 | MS (chúc) | cao, chúc xuống đá lát | 28 | tĩnh | trắng phẳng (không bóng); vệt tối mờ dưới chân thang | rè điện đều; im | Ida giơ tay trái lên; nền đá không có bóng. | Hình then chốt cảnh 2: bóng dài đã mất; bà giơ tay — không gì động trên đá lát. | render v2 |

## Cảnh 3 — Chạy đua (0:43,50–0:59,00, 7 shot)

| # | Shot | Thời điểm | Dài (s) | Cỡ | Góc | mm | Chuyển máy | Nguồn sáng trong truyện | Thoại / âm | Hành động | Lý do chọn | Nguồn khung |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 17 | s15 | 0:43,50–0:45,00 | 1.5 | WS | ngang tầm mắt | 35 | tĩnh | trắng phẳng (cột x=85); đèn khí L7 chìm | bước xuống thang; rè điện | Ida tụt nhanh xuống thang, vác thang, quay về phía dốc xuống. | Chuyển cảnh: bà xuống thang, quay người về phía dốc xuống (trái khung) — đuổi theo phần phố chưa có điện. Trời đêm trên mái. | render v2 |
| 18 | s19 | 0:45,00–0:47,50 | 2.5 | WS | ngang | 35 | tĩnh | đèn khí L8 vừa thắp (có bóng) → bóng đèn cột điện nhấp hai lần, đứng trắng | "phụp" L8; tách + rè khi cột điện bật | Ida trên thang ở L8: hổ phách nở, bóng dài; vài giây sau cột điện bật, trắng phủ, bóng tan trong 0,5 s. | Montage: ngọn thứ 8 nở hổ phách, bóng bà đổ dài — rồi bóng đèn cột điện x=57 (trong khung, phải) nhấp hai lần, đứng trắng, xoá bóng. | render v2 |
| 19 | s21 | 0:47,50–0:49,50 | 2.0 | MCU (tay) | ngang, 3/4 | 85 | tĩnh | trắng phẳng; L10 chưa thắp | thang rung; sào gỗ va; hơi thở gấp | Ida trèo nhanh lên L10, sào mồi trượt khỏi tay (58,9), chụp lại (59,4). | Vội: trèo quá nhanh, tuột sào mồi rồi chụp lại — lần đầu thấy tay bà không vững. | render v2 |
| 20 | s22 | 0:49,50–0:52,50 | 3.0 | MCU | ngang mắt, 3/4 | 85 | tĩnh | trắng phẳng; đèn khí L10 bắt lửa ở khung cuối (ấm lên mặt) | THOẠI L2 "Not yet... not yet." (60,0–62,88); "phụp" (62,95, sau câu thoại, tràn qua điểm cắt) | Ida lẩm bẩm, mở van; lửa bắt ngay khi câu dứt; hổ phách chìm trong trắng. | Lời thoại duy nhất của cảnh chạy đua; ngọn L10 bắt lửa ấm lên mặt bà rồi bị trắng dìm ngay. | render v2 |
| 21 | s23 | 0:52,50–0:55,50 | 3.0 | WS | ngang, nhìn xuôi dốc về nhà kho | 28 | tĩnh | L11 bắt lửa; cột điện góc (x=11) còn tắt; phố trắng ở xa sau lưng | bước chạy; thang; "phụp" | Ida hối hả tới L11, trèo, thắp. Hổ phách. | Góc ngọn cuối cạnh bức tường vôi nhà kho thuộc ĐOẠN CÁP CUỐI (luật thế giới mục 1, v0.4): cột điện góc còn TẮT, góc còn tối; phố sau lưng bà đã trắng. Chỉ đạo chủ dự án 0:40. | render v2 |
| 22 | s24 | 0:55,50–0:57,50 | 2.0 | MS | hơi cao, 3/4 trước-phải | 35 | tĩnh | đèn khí L11 (ấm) — góc cuối phố chưa có điện | lửa thở; im lặng tương đối | Ida áp tay vào kính: một, hai, ba. Xa phía sau, Cas nhìn. | Nhịp đếm ba lần thứ hai; góc cuối phố chỉ còn hổ phách. Ở nền, cậu bé đứng ở tường nhìn bà — bà không thấy (gieo cảnh 4). | render v2 |
| 23 | s24c | 0:57,50–0:59,00 | 1.5 | MS | ngang mắt Cas, 3/4 trước-phải | 50 | tĩnh | đèn khí L11 (ấm, bên phải khung); góc tối | lửa thở xa; im | Cas đứng dựa tường vôi, nhìn về phía cột đèn (phải khung), tay giấu trong tay áo. | Giới thiệu Cas rõ (AI mù v1: "Cas 1:04–1:06 chỉ là một chấm"): cậu bé áo len quá khổ, một mình ở chân tường nhà kho, mặt ấm lên vì ngọn L11 vừa thắp; cậu nhìn bà. | render v2 |

## Cảnh 4 — Bức tường (0:59,00–1:20,00, 8 shot)

| # | Shot | Thời điểm | Dài (s) | Cỡ | Góc | mm | Chuyển máy | Nguồn sáng trong truyện | Thoại / âm | Hành động | Lý do chọn | Nguồn khung |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 24 | s25 | 0:59,00–1:02,00 | 3.0 | MS | ngang ngực, 3/4 sau-phải Cas | 45 | dolly vào rất chậm (0,3 m) | đèn khí L11 (key, có bóng) — cột điện cạnh tường còn tắt | lửa thở; vải sột soạt; im | Cas giơ hai tay làm chim; chim vỗ cánh chậm trên tường vôi. | Giới thiệu Cas bằng việc cậu làm: chim bóng từ đèn khí L11 (khung style frame b_cas_bird). | render v2 |
| 25 | s26 | 1:02,00–1:04,00 | 2.0 | MS | ngang, 3/4 trước-trái Ida | 50 | tĩnh | đèn khí L11 sau lưng Ida; đèn lồng thắt lưng | lửa thở | Ida đứng cạnh cột L11 nhìn Cas. | Ida xuống thang, đứng xem, không gọi. Đèn lồng ở thắt lưng vẫn cháy (gieo cho 1:26). | render v2 |
| 26 | s27 | 1:04,00–1:07,00 | 3.0 | WS | thấp, sau-phải, hất lên | 21 | tĩnh | cột điện cạnh tường bật — trắng phẳng; đèn khí L11 còn nhưng chìm | rơ-le "tách"; bóng đèn rít; rè điện | Bóng đèn điện bật; chim bóng xám dần rồi mất; tay Cas vẫn vỗ. | Cột điện PHỐ CHÍNH cạnh góc nhà kho bật: bóng đèn thấy trong khung, nhấp hai lần rồi đứng trắng trên nền trời đêm có sao. Trắng phủ tường; chim nhạt dần trong 12 khung (luật 3.3) — tay vẫn còn, chỉ mất bóng. Góc ngọn 11 lùi sau góc nhà, vẫn tối (chỉ đạo chủ dự án). | render v2 |
| 27 | s28 | 1:07,00–1:09,00 | 2.0 | MS | ngang ngực, 3/4 sau-phải Cas | 45 | tĩnh | trắng phẳng | rè điện; vải | Cas vỗ tay nhanh, mạnh; tường trắng trơn. | Cas vỗ mạnh hơn vào bức tường trống — không gì cả. | render v2 |
| 28 | s29 | 1:09,00–1:12,00 | 3.0 | MCU | ngang mắt Cas, 3/4 trước-phải | 85 | tĩnh | trắng phẳng; phản ánh ấm rất nhẹ của đèn lồng | rè điện; im | Cas hạ tay, xoay người về phía Ida (trái khung), nhìn xuống đèn lồng. | Cas hạ tay, quay lại, thấy bà — rồi thấy đèn lồng hổ phách ở thắt lưng bà. Cậu không xin. | render v2 |
| 29 | s30 | 1:12,00–1:14,00 | 2.0 | MS | ngang, sau-phải | 35 | tĩnh | đèn lồng tới gần tường (ấm) trong nền trắng | kim loại quai đèn; vải | Ida tháo đèn lồng, quỳ một gối bên trái Cas. | Ida tháo đèn lồng, quỳ cạnh cậu, cầm thấp sau tay cậu, cách tường một sải tay (≤ 0,7 m — luật 3.3). | render v2 |
| 30 | s31 | 1:14,00–1:17,00 | 3.0 | MCU | ngang mắt Ida (quỳ), 3/4 sau-phải | 85 | tĩnh | đèn lồng ấm dưới mặt bà; trắng phẳng từ trên | THOẠI L3 "Go on, then." (88,0–90,3) | Ida quỳ, quay đầu về Cas, nói L3. | Lời mời, không dạy: bà đưa ánh sáng, cậu tự làm. | render v2 |
| 31 | s32 | 1:17,00–1:20,00 | 3.0 | WS | ngang, sau-phải | 35 | tĩnh | đèn lồng thấp sau tay Cas (key ấm, có bóng) trong nền trắng | Cas cười khẽ (chờ SFX có giấy phép — để trống); nhạc tạm vào | Cas giơ tay vào quầng hổ phách; chim to hiện trên tường và bay. | Chim trở lại, TO hơn, ấm, rìa mềm (tay gần nguồn — luật 3.2, 3.3) và bay. | render v2 |

## Cảnh 5 — Ngọn cuối (1:20,00–2:02,50, 14 shot)

| # | Shot | Thời điểm | Dài (s) | Cỡ | Góc | mm | Chuyển máy | Nguồn sáng trong truyện | Thoại / âm | Hành động | Lý do chọn | Nguồn khung |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 32 | s33 | 1:20,00–1:27,00 | 7.0 | WS | ngang 1,35 m, "tranh trong tranh" | 32 | dolly vào chậm (0,9 m) | đèn lồng trên nền đá (nguồn thấp, có bóng); ngoài vòm: điện phẳng | nhạc tạm; bước chân vào hốc; rè điện xa | Ida đặt đèn lồng, hai người bước vào; Ida dừng giữa hốc, Cas đi tới sát vách; hai bóng một cao một nhỏ. | Hình trung tâm (7A, khung style frame c_s5_wide): trong hốc cửa khuất điện, đèn lồng dưới đất; Ida dừng gần đèn nên bóng bà vươn CAO lên vách, Cas đi tới sát vách nên bóng cậu NHỎ, đứng ngay cạnh cậu ("hers, tall…; his, small"). Ngoài vòm phố trắng không bóng. | render v2 |
| 33 | s34 | 1:27,00–1:29,00 | 2.0 | MS (nghiêng) | ngang ngực, từ phía phải, cạnh đèn lồng | 35 | tĩnh | đèn lồng dưới đất sau lưng hai người (key thấp, có bóng); viền má và mép mũ | lửa thở; nhạc tạm | Ida ngửa nhìn bóng, tay đặt lên ngực; Cas giơ nửa tay nhìn bóng mình. | Ida ngửa nhìn bóng mình cao vút; bên phải, Cas đứng sát vách cạnh cái bóng nhỏ của chính cậu — người và bóng cùng một khung, đọc được bóng nào của ai (AI mù v1 đọc "ba cái bóng"). | render v2 |
| 34 | s35 | 1:29,00–1:33,00 | 4.0 | WS | ngang, xuôi dốc | 28 | tĩnh | đèn khí L11 (ấm, có bóng); phố trắng ở xa sau lưng máy | bước chân; thang; rè điện xa | Ida bước ra khỏi hốc, tới thang, trèo; Cas chạy theo giữ thang. | Góc ngọn cuối vẫn TỐI (đoạn cáp cuối chưa bật): ngọn L11 là nguồn duy nhất, bóng dài. Bà trèo lên lần cuối; Cas theo và giữ thang bằng hai tay. | render v2 |
| 35 | s36 | 1:33,00–1:35,00 | 2.0 | MCU | ngang mắt, gần chính diện | 85 | tĩnh | đèn khí L11 ngay trước mặt (ấm) — góc chưa có điện | vải dạ; hơi thở | Tay trái đưa lên vành mũ (hat_push_a), đẩy vành lên, mũ ngả ra sau (hat_push_b). | Quyết định C4 của chủ dự án: bà TỰ đẩy vành mũ ra sau trước câu thoại — mặt thoáng ra cho lời từ biệt. Góc còn tối: mặt ấm một bên. | render v2 |
| 36 | s37 | 1:35,00–1:40,80 | 5.8 | CU | ngang mắt, gần chính diện | 85 | đẩy vào rất chậm | đèn khí L11 (ấm) — góc chưa có điện | THOẠI L4 "That's the last one, then. Goodnight, old street." | Ida nhìn lên phố (phải khung), tay đặt trên van. | Lời từ biệt, vế đầu: cười buồn, còn trong hổ phách của ngọn cuối. Máy đẩy vào không nhận ra được. | render v2 |
| 37 | s37w | 1:40,80–1:43,60 | 2.8 | WS | ngang, từ lòng phố, hơi hất | 28 | tĩnh | cột điện góc bật (nhấp 2 lần, đứng) — trắng phẳng tràn góc; L11 nhạt dần | THOẠI L4 (ngoài hình) "…You'll be brighter now."; tách rơ-le gần; bóng đèn rít; rè điện | Ida trên thang, Cas giữ thang; bóng đèn điện bật, bóng dài của hai người trên đá lát tan. | CHỈ ĐẠO CHỦ DỰ ÁN (1:50 v1): ngay quanh "You'll be brighter now", bóng đèn cột góc (đoạn cáp cuối) nhấp hai lần rồi đứng trắng; trắng tràn vào góc, bóng dài và bóng tối biến mất. Câu thoại khớp với hình. | render v2 |
| 38 | s38 | 1:43,60–1:45,00 | 1.4 | MS | cao, chúc xuống (gần mắt Ida) | 50 | tĩnh | trắng phẳng (cột góc vừa bật); ấm rất yếu từ L11 trên cao | L4 tiếp (ngoài hình) | Cas giữ thang, ngửa mặt nhìn lên. | Phản ứng của Cas: cậu giữ thang, ngước nhìn bà trong ánh trắng mới — người nghe câu nói thay khán giả. | render v2 |
| 39 | s39 | 1:45,00–1:49,40 | 4.4 | CU | ngang mắt, gần chính diện | 85 | tĩnh | trắng phẳng (cột góc); L11 nhạt | THOẠI L4 "Just... keep a little dark for the ones who need it." | Ida nghẹn, một giọt nước mắt; mắt vẫn nhìn lên phố. | Vế cuối, giọng vỡ, nay trong ánh trắng phẳng: "keep a little dark for the ones who need it" — chủ đề phim trong một câu. | render v2 |
| 40 | s40 | 1:49,40–1:52,00 | 2.6 | CU (insert) | ngang lồng đèn, từ lòng phố | 50 | tĩnh | ngọn L11 co lại → xanh → tắt; trắng phẳng không đổi | van kim loại; lửa xì nhỏ dần; "phụt" tắt; im | Tay phải Ida gạt van; ngọn lửa co lại, chuyển xanh, tắt; lồng kính tối. | NGỌN CUỐI (AI mù v1: "thắp hay tắt?"): tay bà gạt van; lửa co lại, ngả xanh, tắt; máy giữ im 0,8 s trên lồng kính tối. Rõ là TẮT. | render v2 |
| 41 | s40w | 1:52,00–1:54,00 | 2.0 | WS | ngang, từ lòng phố, hơi hất | 28 | tĩnh | trắng phẳng; lồng kính L11 tối | rè điện đều; im | Ida trên thang, tay rời van; Cas giữ thang; không gì đổi. | "Nothing else changes": ngọn cuối đã tắt, phố trắng y nguyên — không một đèn nào nhấp. Máy tĩnh, giữ 2 s. | render v2 |
| 42 | s41 | 1:54,00–1:55,50 | 1.5 | WS | ngang | 28 | tĩnh | trắng phẳng; đèn lồng ấm trong tay | rè điện đều; quai đèn | Ida chìa đèn lồng; Cas đón bằng hai tay. | Dưới chân thang bà trao đèn lồng; cậu nhận bằng hai tay. | render v2 |
| 43 | s42a | 1:55,50–1:57,50 | 2.0 | MS | ngang ngực Cas, 3/4 trước | 45 | tĩnh | trắng phẳng khắp khung; đèn lồng ấm dưới cằm Cas | rè điện; lửa đèn lồng thở; nhạc tạm vào lại | Cas cầm đèn lồng bằng hai tay, quay đầu nhìn trái, nhìn phải, rồi nhìn về phía hốc cửa (trái khung). | CHỈ ĐẠO CHỦ DỰ ÁN (2:07 v1): Cas ôm đèn lồng, nhìn quanh phố giờ trắng khắp nơi — không còn chỗ nào cho ngọn lửa nhỏ. Cậu tìm một góc tối. | render v2 |
| 44 | s42b | 1:57,50–1:59,50 | 2.0 | WS | ngang 1,3 m, ngoài vòm | 32 | tĩnh | ngoài vòm: điện phẳng; trong hốc: chỉ đèn lồng Cas mang theo | bước chân trẻ con; rè điện xa dần | Cas đi từ phố vào vòm, dừng giữa hốc. | Cas mang đèn lồng rời phố trắng, bước qua vòm vào hốc cửa khuất điện (nơi hai cái bóng đứng lúc trước): ánh hổ phách đi theo cậu vào trong bóng tối. | render v2 |
| 45 | s42 | 1:59,50–2:02,50 | 3.0 | MS | thấp, từ trong hốc nhìn ra vòm | 32 | tĩnh | đèn lồng trên nền đá (nguồn duy nhất trong hốc); ngoài vòm: điện phẳng | lửa đèn lồng thở; nhạc tạm | Cas ngồi xổm, áp tay: một, hai, ba. Ida ở miệng vòm. | Trả mô-típ: trong góc tối cậu tự chọn, không ai bảo, Cas đặt đèn xuống, hơ hai lòng tay trên kính đếm ba — đúng như bà. Qua vòm: phố trắng; Ida đứng ở miệng vòm nhìn vào, không nói. | render v2 |

## Cảnh 6 — Ô cửa (2:02,50–2:22,50, 7 shot)

| # | Shot | Thời điểm | Dài (s) | Cỡ | Góc | mm | Chuyển máy | Nguồn sáng trong truyện | Thoại / âm | Hành động | Lý do chọn | Nguồn khung |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 46 | s43 | 2:02,50–2:06,50 | 4.0 | EWS | cao (cùng khung mở đầu) | 28 | dolly vào rất chậm | đèn điện khắp nơi; một ô cửa đèn lồng | rè điện toàn thành phố; nhạc tạm | Toàn cảnh tĩnh; một ô vàng. | Lặp khung mở đầu để đo cái đã mất: thành phố trắng đều, không ngủ; giữa khung một ô cửa hổ phách. | tái dùng v1:s43 |
| 47 | s44 | 2:06,50–2:09,00 | 2.5 | WS | thấp, hất lên ô cửa | 21 | đẩy vào chậm | đèn lồng trên bậu cửa sổ (qua ô kính); điện chỉ lọt miệng ngõ | rè điện xa, nghẹt; im | Ida đứng dưới cửa sổ, ngửa nhìn ô vàng. | Trong ngõ khuất điện, dưới ánh cửa sổ nhà Cas, bóng bà — ngắn, nhạt — nằm lại trên đá lát (khung style frame d_s6_alley). | render v2 |
| 48 | s45 | 2:09,00–2:11,00 | 2.0 | MS | ngang | 50 | tĩnh | ánh cửa sổ ấm từ trên | tích tắc; rè điện xa | Ida lấy đồng hồ, nhìn nó, rồi ngẩng nhìn về phía miệng ngõ. | ĐỒNG HỒ NHỊP 3a — hai giờ sau (10:00): bà lấy đồng hồ ra (9:53, vẫn chậm 7 phút), rồi ngẩng nhìn về phía mặt đồng hồ quảng trường trên mái. | render v2 |
| 49 | s45c | 2:11,00–2:12,50 | 1.5 | CU | tele, POV của Ida qua miệng ngõ | 200 | tĩnh | mặt đồng hồ phát trắng; trời đêm | rè điện xa; tích tắc | Mặt đồng hồ quảng trường: 10:00. | ĐỒNG HỒ NHỊP 3b — mặt đồng hồ điện trên nền trời đêm chỉ đúng 10:00 (cùng vị trí, cùng cỡ với nhịp 2a): giờ của thành phố. | render v2 |
| 50 | s46 | 2:12,50–2:15,50 | 3.0 | CU (insert) | chúc nhẹ | 100 | tĩnh | ánh cửa sổ ấm | núm vặn lách cách; tách gập | Ngón cái vặn núm; kim phút chạy từ 9:53 lên 10:00; bàn tay khép lại. | ĐỒNG HỒ NHỊP 3c (9B): bà vặn kim từ 9:53 lên đúng 10:00 — nhận giờ mới. Gập đồng hồ, KHÔNG gõ kính (ngược với nhịp 1). | render v2 |
| 51 | s47 | 2:15,50–2:17,50 | 2.0 | WS | ngang, sau lưng Ida | 28 | tĩnh | ánh cửa sổ (sau lưng) → điện phẳng ở miệng ngõ | bước chân; thang; rè điện lớn dần ở miệng ngõ | Ida vác thang đi từ dưới cửa sổ ra miệng ngõ. | Bà vác thang đi ra miệng ngõ; bóng mờ của bà mỏng dần rồi tan trong trắng (luật 3.5). | render v2 |
| 52 | s48 | 2:17,50–2:22,50 | 5.0 | WS | ngang, sau lưng Cas | 28 | tĩnh; mờ dần về đen (148,5–150) | đèn lồng trên bậu (nguồn duy nhất, hổ phách trọn khung) | nhạc tạm (kết); lửa thở | Cas làm chim; chim bay ngang tường; FADE OUT. | Kết 2B: đèn lồng trên bậu, Cas quay lưng, chim to và mềm mở cánh bay ngang tường. Ida đã đi trước. | tái dùng v1:s48 |

## Thời gian render thật (960×540, 1 mẫu, không DOF)

| Shot | Khung | Dựng cảnh (s) | s/khung (TB) | s/khung (max) | Tổng (s) |
|---|---|---|---|---|---|
| s02 | 108 | 2.7 | 1.81 | 10.35 | 202 |
| s03 | 48 | 2.6 | 2.63 | 10.52 | 131 |
| s04 | 36 | 3.5 | 2.06 | 10.12 | 79 |
| s05 | 96 | 2.1 | 2.00 | 5.88 | 197 |
| s06 | 72 | 2.8 | 2.56 | 10.29 | 189 |
| s07 | 96 | 2.1 | 1.25 | 7.16 | 124 |
| s08 | 48 | 2.2 | 1.15 | 7.61 | 58 |
| s09 | 72 | 0.4 | 1.22 | 7.45 | 90 |
| s09w | 48 | 2.7 | 1.75 | 8.62 | 89 |
| s10e | 48 | 0.5 | 1.35 | 7.93 | 67 |
| s10 | 72 | 2.7 | 2.05 | 4.72 | 153 |
| s11 | 48 | 2.0 | 1.60 | 6.86 | 80 |
| s12 | 60 | 2.6 | 2.44 | 11.50 | 151 |
| s13 | 48 | 2.6 | 2.59 | 13.69 | 129 |
| s14 | 48 | 3.2 | 2.60 | 14.40 | 130 |
| s15 | 36 | 3.0 | 2.35 | 13.12 | 90 |
| s19 | 60 | 2.7 | 2.63 | 12.88 | 163 |
| s21 | 48 | 2.5 | 2.34 | 11.54 | 117 |
| s22 | 72 | 3.5 | 1.88 | 12.47 | 141 |
| s23 | 72 | 1.5 | 0.73 | 5.79 | 55 |
| s24 | 48 | 2.8 | 1.92 | 10.22 | 97 |
| s24c | 36 | 2.9 | 2.65 | 12.17 | 101 |
| s25 | 72 | 1.2 | 1.74 | 8.11 | 128 |
| s26 | 48 | 2.4 | 3.68 | 15.33 | 182 |
| s27 | 72 | 1.6 | 3.55 | 13.94 | 261 |
| s28 | 48 | 1.4 | 2.55 | 9.84 | 125 |
| s29 | 72 | 1.8 | 3.30 | 13.27 | 242 |
| s30 | 48 | 1.7 | 2.76 | 10.91 | 136 |
| s31 | 72 | 1.7 | 3.22 | 10.65 | 236 |
| s32 | 72 | 1.4 | 2.71 | 11.11 | 199 |
| s33 | 168 | 2.2 | 1.40 | 6.64 | 241 |
| s34 | 48 | 2.3 | 1.64 | 6.85 | 82 |
| s35 | 96 | 2.8 | 2.31 | 14.89 | 229 |
| s36 | 48 | 3.0 | 2.33 | 12.32 | 118 |
| s37 | 139 | 3.4 | 2.37 | 13.14 | 340 |
| s37w | 67 | 3.5 | 2.23 | 14.29 | 155 |
| s38 | 34 | 2.8 | 2.21 | 10.74 | 80 |
| s39 | 106 | 3.5 | 2.38 | 11.28 | 261 |
| s40 | 62 | 2.9 | 2.13 | 11.91 | 138 |
| s40w | 48 | 2.9 | 2.60 | 13.76 | 130 |
| s41 | 36 | 2.9 | 2.39 | 13.38 | 91 |
| s42a | 48 | 3.0 | 1.86 | 13.36 | 94 |
| s42b | 48 | 2.3 | 1.54 | 6.90 | 78 |
| s42 | 72 | 2.2 | 1.59 | 6.74 | 119 |
| s44 | 60 | 2.5 | 1.90 | 10.05 | 119 |
| s45 | 48 | 2.7 | 1.85 | 9.56 | 94 |
| s45c | 36 | 0.4 | 1.34 | 7.49 | 50 |
| s46 | 72 | 2.2 | 1.77 | 7.49 | 132 |
| s47 | 48 | 2.3 | 1.79 | 9.52 | 90 |
