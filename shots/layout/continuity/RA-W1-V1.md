# RÀ CONTINUITY — Cổng 6 · W1 v1 + NỐI W1–W2 (s01 → s32; s39, s41, s42a, s42b, s42) — MỘT LƯỢT

Người rà: agent continuity. Việc này chỉ báo lỗi, không sửa gì. Ngày 30/09/2026, theo chỉ thị của chủ dự án: chỉ rà một lượt. Nhánh P (HEAD `a06362a`, đã merge W1 v1 @d8f6ffb và B3–B4 @56b5b2f). Không đọc mã trong `checks/`.
Căn cứ: `CLAUDE.md`, `bible/characters.md` (v1.6), `bible/world-rules.md` (v0.6), `design/cong3/model-sheet/ida.json`, `cas.json` (costume, props, local_colors, silhouette_keys, _v1_5_1, _v1_6), `shots/layout/continuity/canh-1.md` … `canh-6.md`, `shots/layout/LAYOUT-W1.md` §15, `reports/m2/cong6/w1/BAO-CAO-W1-V1.md`, `reports/m2/cong6/b34/BAO-CAO-B34.md`, `shots/layout/continuity/RA-W2-V2.md`, AUTHORSHIP.md mục "Cổng 6 — diễn hoạt".
Hình: bản ghép toàn phim `design/cong5/layout/out/layout-v20.mp4` (960×540, 24 fps, 3 372 khung, 140,5 s, 53 shot, có phụ đề). Trích từng khung 0–1919 và 2430–2900. Số đo lấy từ `layout-v20.motion.json` (gốc nhân vật, vị trí máy, vết bàn tay trên màn hình) và stem `sfx.flac`.
Quy ước: "khung" là khung toàn cục (giây phim × 24). Ảnh bằng chứng nằm ở `reports/m2/cong6/w1/ra-continuity/` (tạm, **không commit**; tên tệp ghi ở từng dòng). Hỏi P nếu cần chép vào repo.

> **Đường dẫn:** lệnh giao muốn nộp ở `shots/layout/continuity/RA-W1-V1.md`. Cấu hình phiên này chỉ cho ghi `reports/continuity.md` và cấm sửa tệp khác, nên báo cáo nằm ở đây, thay nội dung cũ. P chép sang nếu cần.

## 0. Tóm tắt
- **Chặn: 0 · Nên sửa: 7 (L1–L7) · Ghi nhận: 9 (L8–L16).**
- W1 đạt phần lớn: s22 là 3/4 và vẫn MCU; s23 không còn cột điện cùng mé với đèn khí; đèn L1–L11 bật đúng thứ tự; giờ đồng hồ chỉ tiến; thang vác vai phải, đầu chúc về trước; đèn lồng tắt ở s02–s04 và cháy từ s07.
- **Hai hành động lặp lại then chốt của bible không đọc được trên hình:** gõ kính đồng hồ ở s06 (L3) và hơ tay đếm ba ở s24 (L4). P xét có nâng lên mức chặn không, vì cả hai là căn cứ của rubric C1.
- B3–B4 đạt: M1, M3, M5 và N7 đã sửa trên hình; ánh điện cảnh 4 đến từ mé đối diện và không có cột trong khung; bắp tay Cas tách khỏi thân. **Có lỗi mới do M1 gây ra:** mặt nghiêng và bàn tay Ida đen đặc ở s42b (L5).
- **Nối s24c → s25:** Cas đổi chỗ đúng **0,75 m**. Tôi xếp mức **ghi nhận** (lý do ở §2).

## 1. Bảng lỗi

| Mã | Shot | Khung / giây | Mô tả | Mức | Bằng chứng |
|---|---|---|---|---|---|
| **L1** | s21 → s22 | 1187 → 1188 (49,46 → 49,50) | **Vượt trục 180° của đường Ida → lồng đèn ở hai MCU kề nhau.** Ở s21, máy đứng phía −x của cột (20,1; −2,3): cột và lồng đèn ở PHẢI khung, bà nhìn và giơ sào sang phải. Ở s22, máy đứng phía +x (23,2; −3,97): bà nhìn sang TRÁI khung về lồng đèn. Hai shot không có shot trên trục chen giữa. Montage nén thời gian làm lỗi nhẹ đi nhưng không xoá được. Nếu phía +x của s22 thuộc quyết định cố định thì chỉ cần đổi máy s21 sang +x (s21 là shot W1). | nên sửa | `E_L1_s21_s22_truc.jpg` |
| **L2** | s22 | 1188–1259 (49,5–52,46), suốt shot | **Mẩu tay ở góc dưới-trái.** Cạnh ống/van đồng còn thấy một khối **da hồng, măng sét đỏ sẫm và tay áo xanh** (bàn tay phải nắm ống khí), khoảng 110×50 px. BAO-CAO-W1 §2 chỉ khai "một mẩu đồng". Lỗi cùng dạng với M3 (s39) mà tiêu chí PA1 của chủ dự án cấm. | nên sửa (nhẹ) | `E_L2_s22_goc_duoi_trai.jpg` |
| **L3** | s06 | 400–416 (16,67–17,33); 440–455 | **Không thấy nhịp gõ kính đồng hồ.** Stem SFX có hai tiếng gõ ở 16,80 và 17,20 s (−25 dB, nền −180 dB), nhưng trên hình không có ngón tay nào chạm mặt kính: 8 khung liên tiếp quanh hai mốc chỉ có mặt đồng hồ nằm trên lòng tay. Theo `characters.md`, "gõ kính (cảnh 1) → gập không gõ (cảnh 6)" là hành động lặp lại thể hiện Điểm yếu (rubric C1). Ngoài ra nhịp cất đồng hồ (18,3–18,9 s) cũng không đọc: đồng hồ nằm yên giữa khung tới khung cuối, nền quanh nó thành đen, mảnh tay rời ra, trông như **đồng hồ lơ lửng**. W1 đã tự khai phần gõ (R5). | nên sửa (P xét nâng chặn) | `E_L7_s06_go_kinh.jpg`, `E_L7_s06_cat_dong_ho.jpg` |
| **L4** | s24 | 1332–1379 (55,5–57,46) | **Không thấy nhịp hơ tay đếm ba ở L11.** Hai bàn tay gần như đứng yên: vết tay trên màn hình dịch ≤ 3 px (s05 dịch 80–180 px), khuỷu chỉ đổi 0,21 rad. Tay phải chìa ngang sang trái cột ở tầm thanh móc, **dưới** đáy lồng kính, ngón xoè, trông như chỉ trỏ ra khoảng trống. Bible ghi "hơ tay đếm ba nhịp ở đèn của mình (cảnh 1, 3)" và nhịp này đối xứng với cảnh 5. | nên sửa (P xét nâng chặn) | `E_L3_s24_dem_ba.jpg`, `E_s24_s24c.jpg` |
| **L5** | s42b | 2772–2819 (115,5–117,46) | **Lỗi mới sinh ra khi sửa M1:** máy mới ở phía +x thấy nghiêng mặt Ida. Mặt nghiêng và bàn tay phải của bà **đen đặc như bóng cắt**, trong khi tóc bạc, khăn và áo ngay cạnh vẫn sáng dưới cùng nguồn. Bàn tay đen đã có ở bản trước (`b34/s42b_truoc.jpg`); mặt đen lộ ra vì đổi góc máy. Đọc thành mặt nạ hoặc hình nhân. Đây là việc ánh sáng mặt/da (Cổng 7 hoặc facelight trong shot); P quyết giao cho ai. | nên sửa | `E_L5_s42b_mat_tay_Ida.jpg` |
| **L6** | s15 | 1070 → 1071 (44,583 → 44,625) | **Thang đổi chỗ tức thì:** chỉ trong một khung, thang đang tựa cột biến mất và thang trên vai hiện ra. Ở WS này thấy rõ. W1 đã làm nhịp dựng thang cho s23 nhưng s15 còn đổi tức thì (W1 §6 tự khai). | nên sửa (nhẹ) | `E_L4_s15_thang_nhay.jpg` |
| **L7** | s24c | 1380–1415 (57,5–58,96) | **Tay áp tường không đọc được:** lòng tay phải chạm tường (đo −3 mm), nhưng từ máy 3/4 trước ta thấy nó như bàn tay buông cạnh đùi, phía trước tường. Chỉ đọc được "dựa tường" nhờ bóng sát người. W1 đã khai là R7. Việc B1-2 ("tay đặt đúng lên tường") đạt về số đo nhưng chưa đạt về hình. | nên sửa (nhẹ) / chủ dự án chấp nhận | `E_s24_s24c.jpg`, `E_noi_s24c_s25.jpg` |
| L8 | s24c → s25 | 1415 → 1416 (58,96 → 59,00) | **Nối W1 → W2:** Cas đổi chỗ **0,75 m** (gốc (14,3; −7,90) bộ phố → (4,1; 0,95) hệ tường chim = (14,3; −7,15) bộ phố; Δz = 0,75 m đúng bằng khoảng lùi khỏi tường), quay 180° và giơ tay làm chim. Độ sáng cũng nhảy: s24c hồng ấm, sáng → s25 tím, tối (Cổng 7). Đánh giá ở §2. | ghi nhận | `E_noi_s24c_s25.jpg` |
| L9 | s08 | 588–599 (24,5–25,0) | L6 (x = 78) bắt lửa ngoài khung ở 24,5 s (nền đá tiền cảnh sáng lên từ 13,8 lên 18,8/255) khi Ida còn ở x ≈ 86,7, cách cột 8,7 m và đang đi tới. Như vậy đèn sáng trước khi người thắp tới nơi. Rất khó thấy; lịch này có từ Cổng 5. Đề xuất dời mốc L6 sang sau cắt s08 → s09 (25,0 s, nhảy sang đêm). | ghi nhận | `E_L8_s08_L6.jpg` |
| L10 | s21 → s22 | 1187 → 1259 | Sào mồi ở tay phải cuối s21, sang s22 thì không còn thấy (quy ước "sang tay trái, ngoài khung"). L10 bắt lửa ở 52,45 s mà không thấy sào. Chỗ hở đã ghi (canh-3 "Chỗ hở" 1). | ghi nhận | `E_L1_s21_s22_truc.jpg` |
| L11 | s11 → s12 → s13 | 887 → 888 → 948 | Máy s11 ở phía −x của cột L7 (cột ở PHẢI Ida), máy s13 ở phía +x (cột ở TRÁI). Có s12 là shot **trên trục** (qua vai, máy ở phía bắc) làm cầu nên hợp lệ. Chỉ ghi để P biết chỗ đổi phía. | ghi nhận | `E_tong_canh2.jpg` |
| L12 | s04 | 272–287 (11,3–11,96) | Nhịp mồi đèn lồng: ở WS cao không thấy đèn lồng hông bắt lửa (W1 R6). Đèn lồng sáng thấy được từ s07. | ghi nhận | `E_tong_canh1.jpg` |
| L13 | s22, s12 (và N17 của W2) | 1188–1259; 888–947 | Tóc bạc ở đỉnh đầu và búi có vân chéo như len đan (giống N17 ở s37b/s39). | ghi nhận (Cổng 7 / tài sản) | `E_L1_s21_s22_truc.jpg`, `E_cot_dien_me_duong.jpg` |
| L14 | s42b | 2772–2819 | Một vòng tròn mảnh không có khối trên mặt tường phải hốc cửa (≈ 25 px, ở khoảng (876; 328)). Đã có từ bản trước. Nếu là vòng sắt buộc ngựa thì cần có khối và sáng tối; hiện tại trông như dấu đánh dấu. | ghi nhận | `E_L5_s42b_mat_tay_Ida.jpg` |
| L15 | s26 | 1488–1535 (62–64) | Mặt tiền trắng sau lưng Ida sáng lạnh trước khi cột điện cảnh 4 bật (64,4 s), trong khi luật ghi góc cuối phố còn tối. Là việc mức sáng (Cổng 7). | ghi nhận | `E_s26_s28.jpg` |
| L16 | tài liệu | — | (a) Trong `canh-3.md`, các mục s23, s24, s24c và "Chỗ hở 3" vẫn ghi Cas ở casSpot (14,3; −7,15), cách tường 0,95 m; hình và motion là (14,3; −7,90), cách tường 0,20 m (chỉ mục Cổng 6 đầu tệp đúng). Bảng "Trạng thái cuối" ghi cột điện "trong sân trước (17,0; −5,9)" mà không nói cột đã ẩn và nguồn đã dời. (b) Trong `canh-4.md`, bảng toạ độ và mục s27 ("cột điện + bóng đèn") chưa theo B3; chỉ mục B3–B4 cuối tệp đúng. (c) `cas.json` silhouette_keys ghi "tay áo trùm tới đốt ngón", trong khi v1.6 là măng sét trùm cổ tay 0,09 H (hình đúng v1.6). (d) Hình học `wallPost` ở mé bắc (cùng mé đèn khí) vẫn nằm trong `sets_end.js` và chỉ ẩn theo từng shot; mọi shot mới nhìn về phía đó sẽ thấy lại cột. | ghi nhận | — |

## 2. Nối W1 → W2 (s24c → s25), trạng thái và đánh giá

| Mục | Cuối s24c (khung 1415) | Đầu s25 (khung 1416) | Kết quả |
|---|---|---|---|
| Vị trí Cas | (14,3; −7,90), cách tường 0,20 m | (14,3; −7,15), cách tường 0,95 m | **Đổi chỗ 0,75 m** (đo từ motion) |
| Hướng / tư thế Cas | quay ra phố, nhìn TRÁI khung về Ida, hai tay buông | quay lưng về máy, mặt vào tường, hai tay giơ vỗ chim | đổi qua cắt (M11 của RA-W2-V2) |
| Trục (đường Ida–Cas) | máy s24, s24c cùng một phía (tích chéo +50,5 / +8,6) | máy s25 cùng phía đó (+34) | **đạt**: Ida TRÁI, Cas PHẢI |
| Ánh | L11 từ trái, bóng Cas bên phải, sát người | L11 từ trái, bóng chim bên phải | **đạt** |
| Trang phục | mũ len kem có quả bông đỏ, áo len đỏ cổ lật cao, quần tối | như trái | **đạt** |
| Ida | trên thang L11, ngoài hình | ngoài hình; s26 (62,0 s) đã đứng ở IDA_W, cách chân thang ≈ 3,7 m | xuống thang ngoài hình |
| Đèn | L11 cháy; P5 và cột cảnh 4 tắt | như trái (cột bật 64,4 s) | **đạt** |

**Đánh giá độ lệch 0,75 m: ghi nhận, chấp nhận được.** Lý do:
1. Trên màn hình, khoảng lùi này không đọc riêng được. Hai máy khác nhau và Cas quay 180°, nên cái người xem thấy là **nhảy hành động** (tay buông → tay giơ), không phải nhảy vị trí.
2. Cắt này là ranh giới cảnh 3 → cảnh 4. Ở s26, Ida đã xuống thang và đi khoảng 3,7 m (ngoài hình), tức là bản thân cắt đã ngầm lược vài giây. Cas bước ra 0,75 m trong khoảng thời gian đó là hợp lý.
3. Đề xuất (không bắt buộc): P ghi rõ "lược thời gian vài giây ở ranh cảnh 3/4" vào `canh-3.md` và `canh-4.md` để lần rà sau không mở lại. Nhảy độ sáng (hồng ấm → tím tối) giao Cổng 7.
4. Không cần dùng hai phương án Đ4 (a) hoặc (b) của W1.

## 3. Đối chiếu mục treo W2 sau B3–B4

| Mã | Shot | Yêu cầu | Kết quả trên v20 | Khung | Ảnh |
|---|---|---|---|---|---|
| **M1** | s42a → s42b → s42 | trục s42b khớp s42a và s42 | **ĐẠT.** s42a: Ida TRÁI, Cas PHẢI. s42b: Ida trái-giữa ở miệng vòm, Cas bên PHẢI bà đi vào hốc. s42: Ida TRÁI ngoài vòm, Cas PHẢI ngồi xổm. Lỗi phụ mới: L5 | 2771/2772; 2819/2820 | `E_M1_M5_s41_s42.jpg` |
| **M3** | s39 | không còn "mẩu tay" | **ĐẠT.** Góc dưới-trái chỉ còn cần van cam, không có mảng da ở 2438, 2470, 2500, 2510 (khung kiểm mù), 2520, 2543 | 2438–2543 | `E_M3_s39.jpg` |
| **M5** | s42b | Cas không trong suốt | **ĐẠT.** 2790 thân và chân đặc, sáng mặt trước; 2806 và 2812 bóng dáng đặc có đèn bên hông; 2819 ngồi xổm, dáng đặc. Không còn thấy đèn xuyên qua chân, không còn "bàn tay lơ lửng". Ghi thêm: ống quần ra xám nhạt ở 2806–2812 (ánh sáng) | 2772–2819 | `E_L5_s42b_mat_tay_Ida.jpg` |
| **Bắp tay Cas** | s41, s42a, s42b | thấy cánh tay trên dọc thân khi ôm đèn | **ĐẠT ở s42a.** Từ vai tới khuỷu thấy ống tay tách khỏi sườn, có rãnh tối ở cả hai bên, khuỷu ra ngoài thân. Cánh tay trên dài khoảng 0,5–0,55 thân nhìn thấy, khớp `cas.json` (0,196 / 0,379 m). Còn: khối sáng nhạt giữa ngực trên hai bàn tay (M12 cũ). s41 (WS) và s42b (ngược sáng) không đủ lớn để kết luận | 2724, 2748, 2771 | `E_bap_tay_Cas_s42a.jpg` |
| **N7** | s27, s30 | đèn lồng hông thấy cháy | **ĐẠT.** s27: kính đèn sáng ló sau hông bà ở 64,00, 65,00 và 66,67 s. s30: đèn cháy ở tay phải bà ngay từ khung đầu 1728 | 1536, 1560, 1600, 1728 | `E_canh4_s27_s30.jpg` |
| **B3** | s25–s32 | ánh điện từ mé đối diện, không thấy cột | **ĐẠT.** Không có cột điện trong khung nào. Đường thẳng đứng mảnh ở s24, s27, s30, s32 là **ống thoát nước trên tường**: chạy từ máng mái xuống chân tường, cùng vị trí ở mọi shot. Sau 64,84 s tường trắng phẳng, không còn bóng đổ dài, hốc cửa tối (nguồn cao, ở phía trước bên phải), nhất quán ở s28–s32. Chim L11 tan ở s27, không còn ở s28; chim đèn lồng ở s32 hướng lên phải, khớp vị trí đèn | 1416–1919 | `E_canh4_tong.jpg`, `E_canh4_s27_s30.jpg` |

## 4. Kết quả rà cảnh 1–3 theo lệnh (ngoài bảng lỗi)
- **Đèn khí đúng thứ tự:** L4 tối ở 204–220 và sáng từ 221 (9,2 s). L5 thắp ngoài hình. L6: xem L9. L7 thắp ngoài hình, sáng ở s11. L8 tối ở 1080 và sáng ở 1109 (45,05 s). L9 thắp ngoài hình. L10 ở khung cuối s22. L11 tối ở 1262–1290 và sáng từ 1308 (54,5 s). **Đạt.**
- **Cột điện so với mé đường (luật v0.6):** s02, s08, s12, s19 có đèn khí ở mé bắc và cột điện ở mé nam. **s23 không còn cột ở mé đèn khí**: bên phải khung chỉ có L11 và ống nước trên tường nhà kho; P5 ở mé nam, bên trái khung, bóng đèn tắt (đỉnh sáng ≤ 171/255). s24, s24c không có cột. **Đạt.** Ảnh: `E_s23_B2.jpg`, `E_cot_dien_me_duong.jpg`.
- **Giờ chỉ tiến:** s06 7:31 (16–19 s) → s09 quảng trường 8:00 (25–28 s) → s09w bỏ túi 7:53 (28–30 s), chậm đúng 7 phút. **Đạt.** Ảnh: `E_gio_dong_ho.jpg`.
- **Đèn lồng:** tắt, tối ở s02 (khung 100–203). Không đọc được lúc mồi ở s04 (L12). Cháy ở hông trái từ s07 tới s24 (s07, s08, s11, s13, s14, s15, s23, s24). **Đạt.**
- **Thang:** vác vai phải, đầu chúc về trước ở s02, s07, s15 và s23. Tựa phía bắc cột khi trèo. Không còn hai cái thang. Đổi chỗ tức thì ở s15 (L6). **Đạt, trừ L6.**
- **Mũ:** `hat_back` = 0 suốt cảnh 1–3. Mũ không có nơ. Ra nâu dưới lửa gần (s05, s13; D2 đã biết), đen xanh dưới điện (s21, s22). **Đạt.**
- **Cầm nắm:** tay phải trên thanh thang (s02, s07, s08, s15). Tay trên thanh móc và thân cột (s05 cuối, s11, s13, s14). Đồng hồ trong lòng tay (s06, s09w). Sào ở tay phải (s21, xác nhận bằng vết `hand_R@s21`). Tay trái giơ ngang (s14). **Đạt**, trừ L2, L3 và L7.
- **s22:** 3/4 khoảng 45°, nhìn TRÁI khung, **vẫn MCU** (đầu, mũ, vai, khăn), máy tĩnh, mắt không nhìn thẳng ống kính. **Đạt**, trừ L1 và L2.
- **Trục 180°:** s24 → s24c → s25 đạt. L1 vượt trục. L11 có shot cầu nên hợp lệ.

## 5. Tờ so nhân vật với model sheet (cảnh 1–3, bằng mắt)
Chuẩn Ida (`ida.json` v1.5.1): cao 6,27 H; mũ phớt #262a33 không nơ; khăn #8e5c5a quấn cao 4 vòng, một đuôi trước ngực; áo khoác dài #3f5552; váy #4a3a44; tóc bạc #e2dfda, búi 1,3×; hoa tai #c9a466; đèn lồng móc hông trái; thang vác vai phải 28°, đầu chúc về trước; tay MPFB 1,15×.
Chuẩn Cas (`cas.json` v1.6): cao 5,0 H; mũ len #d6c9ae, quả bông #a8483a; hai tai vểnh; tóc #5a4034 lộ ở gáy; áo len #8a4a3c cổ lật cao, gấu 2,17 H; măng sét trùm cổ tay; quần #3a3d48 ống thẳng.

| Shot | Ai / cỡ | Tỷ lệ | Trang phục, đạo cụ | Lệch thấy được |
|---|---|---|---|---|
| s02, s07, s08 | Ida WS (bóng dáng) | Khối chữ A cao, vai hẹp: đúng | Mũ phớt, thang vai phải chúc trước, đèn lồng hông: đúng | — |
| s03, s04 | Ida MS/WS trên thang | Đúng | Mũ, khăn nhiều vòng, áo xanh lục: đúng | L12 |
| s05 | Ida MCU (lửa gần) | Đầu MPFB, búi 1,3×: đúng | Mũ ra nâu (D2 đã biết), khăn 4 vòng và đuôi trước ngực, hoa tai, tóc bạc: đúng | Vệt tối trên lòng tay (đã khai, Cổng 7) |
| s06, s09w | Tay Ida (insert) | Tay 1,15× hợp lý ở s09w | Đồng hồ 12 vạch, không chữ số, 2 kim: đúng | s06: mép lưới tay lộ gãy khúc ở cận cảnh; L3 |
| s11–s14 | Ida MS trên thang | Đúng | Khăn, hoa tai, búi, đèn lồng hông: đúng | L13 (vân tóc ở s12) |
| s15, s19 | Ida WS | Đúng | Thang, đèn lồng: đúng | L6 |
| s21 | Ida MCU (tay) | Tay có khớp, cầm sào: đúng | Mũ đen xanh, khăn đỏ sẫm, áo xanh: đúng | — |
| s22 | Ida MCU 3/4 | Mặt MPFB, tai, hoa tai ở dái tai: đúng | Mũ không nơ, khăn 4 vòng: đúng | L2, L13 |
| s23, s24 | Ida + Cas WS/MS | Ida khoảng 6 H, Cas khoảng 5 H: hợp lý | Mũ phớt, đèn lồng hông; mũ quả bông, áo đỏ: đúng | L4 |
| s24c | Cas MS | Đầu MPFB, cổ lật cao 0,2 H, vai phồng (đã chấp nhận), cánh tay trên thấy dọc thân: đúng | Mũ kem, quả bông đỏ, tai vểnh, tóc gáy nâu, măng sét ở cổ tay: đúng v1.6 | L7; L16 (c) |

**Kết luận tờ so:** trong cảnh 1–3 không thấy lệch màu, trang phục hay tỷ lệ so với model sheet. Chỉ số C3 bằng máy vẫn cần P chạy cho các shot đo được.

## 6. Việc đang chờ
- **Chủ dự án:** (1) có nâng L3 (gõ kính s06) và L4 (đếm ba s24) lên mức chặn không, vì đây là hai hành động lặp lại then chốt của bible; (2) nhận hay sửa L1 (vượt trục s21 → s22); (3) duyệt đánh giá "ghi nhận" cho nối s24c → s25 (L8) và cách ghi "lược thời gian ở ranh cảnh"; (4) chấp nhận L7 (tay áp tường không đọc) hay sửa.
- **P:** chép báo cáo sang `shots/layout/continuity/RA-W1-V1.md` nếu cần; giao L1, L2, L3, L4, L6 cho W1 (vòng 2, nếu mở); giao L5 và L15 cho Cổng 7; sửa tài liệu theo L16; xét dời mốc L6 (L9); chạy C3 và luật máy toàn phim.
- Không có chỉ số nào tôi tự đo nằm trong ±5 % quanh ngưỡng. Tôi không chạy luật.
