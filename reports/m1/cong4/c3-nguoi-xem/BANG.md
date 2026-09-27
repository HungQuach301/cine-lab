# C3 — bảng so sánh cho người xem (Cổng 4 vòng v2, Q-C3r B)

Nguồn: `design/cong4/animatic/out/v2/video.mp4` (960×540, 24 fps), mặt nạ `animatic.parts` (4×), `design/cong3/model-sheet/ida.json` → `c3_views`, `MS-ida.png`, `bible/characters.md`. Không đọc mã trong `checks/`.

## Cách làm

- Mỗi đoạn: chọn khung chia hết cho 12 có mặt nạ đầu lớn nhất. Hai đoạn không có mặt nạ đầu (s14, s38): chọn khung có tổng mặt nạ lớn nhất.
- Ảnh: trái là khung phim (cắt quanh Ida nếu vùng Ida cao dưới 300 px); phải là hình hàng trên của `MS-ida.png` ở góc gần nhất. Góc âm: lật ngang hình sheet.
- Số đo: bề dài theo trục chính PCA của điểm ảnh ≥128, +1 px; tỷ lệ = bộ phận / đầu; so với `c3_views` ở góc gần nhất trong 8 góc. Chỉ nêu thân, tay trên, cẳng tay; đùi (null) và cẳng chân (đã bỏ trong bible) không dùng.
- Luật cờ: (a) mắt thấy khác model sheet theo cách người xem nhận ra; hoặc (b) lệch > 10% ở bộ phận không bị che (≤ 10%), không gập (|co ngắn − 1| ≤ 2%), không chạm mép khung. Với (b), tỷ lệ được hiệu chỉnh theo co ngắn của đầu khi đầu cúi/ngẩng (đã biết từ `views`).
- Số đo chỉ là tham khảo, không phải phán quyết.

## Lưu ý trước khi đọc

1. **`MS-ida.png` là bản Cổng 3 vòng 1** ("đề xuất của Claude, chưa duyệt"). Hình này chưa có khăn len, váy, hoa tai, mặt vẽ tay (C′), cổ áo cao tới cằm của bible v1.2. Vì vậy khăn, hoa tai, mặt chi tiết trên phim **không** tính là lệch; phần trang phục và màu được so với bible v1.2 (`ida.json` → `costume`, `local_colors`).
2. **Danh sách `khong_do_duoc` đầu vào bị cắt ở 300 mục** (khung cuối 2208). Với 8 đoạn từ khung 2232 trở đi (s36, s37, s38, s39, s40 ×2, s42a, s44, s47), cột lý do ghi *"suy từ views"*: tôi áp các tiêu chí máy đã nêu ở phần còn lại (che > 10%, co ngắn > 2%, độ sâu > 2%, chạm mép, null) lên `parts.json`. Đây không phải lời máy.
3. Số lệch rất lớn (−40…−76%) ở cận cảnh là do thân bị cắt ở mép khung, không phải lỗi tỷ lệ.

## Bảng

| Shot máy | Shot phim | Khung (đoạn → chọn) | Góc view / elev; tham chiếu | Số đo lệch chính (tỷ lệ/đầu so với `c3_views`) | Lý do máy loại | Kết luận | Cái thấy |
|---|---|---|---|---|---|---|---|
| 3 | s03 | 204–221 → **216** | 33,6° / -17,6°; c3 45°, sheet "3/4" | thân +14,8%, tay trên +0,4%, cẳng tay +28,8% | thân: gập: co ngắn do tư thế > 2% (foreshorten 1.063); tay trên: gập: co ngắn do tư thế > 2% (foreshorten 0.862); cẳng tay: bị che > 10% (55%) | không cờ | Khung trước khi thắp đèn: Ida gần như bóng đen, không thấy lệch dáng. [3_s03.jpg](3_s03.jpg) |
| 4 | s03 | 222–251 → **228** | 33,6° / -17,7°; c3 45°, sheet "3/4" | thân +8,5%, tay trên -1,8%, cẳng tay +24,3% | thân: gập: co ngắn do tư thế > 2% (foreshorten 1.063); tay trên: gập: co ngắn do tư thế > 2% (foreshorten 0.864); cẳng tay: bị che > 10% (55%) | **CẦN CHỦ DỰ ÁN XEM** (màu) | Dưới đèn vừa thắp, áo khoác đọc thành xanh lá sáng và mũ thành nâu vàng nhạt (mũ RGB ≈ 164,90,41), trái quan hệ "mũ tối nhất, áo tối trung bình" của sheet. [4_s03.jpg](4_s03.jpg) |
| 5 | s04 | 252–287 → **276** | 40,5° / 14,7°; c3 45°, sheet "3/4" | thân +16,7%, tay trên -25,5%, cẳng tay -1,8% | thân: gập: co ngắn do tư thế > 2% (foreshorten 0.918); tay trên: bị che > 10% (16%); cẳng tay: bị che > 10% (36%) | **CẦN CHỦ DỰ ÁN XEM** (màu) | Cùng cảnh đèn với s03: áo xanh lá sáng, mũ nâu nhạt; hình nhoè mạnh nên dáng khó đọc. [5_s04.jpg](5_s04.jpg) |
| 6 | s05 | 288–383 → **360** | 47,4° / 12,5°; c3 45°, sheet "3/4" | thân -47,1%, tay trên -28,5%, cẳng tay khuất | thân: chạm mép khung (bị cắt); tay trên: chạm mép khung (bị cắt); cẳng tay: bị che > 10% (100%) | **CẦN CHỦ DỰ ÁN XEM** (màu) | Cận mặt dưới đèn cam: mũ nâu đất (RGB ≈ 83,35,11), không tối hơn áo (độ sáng 44 so với 52); áo đọc thành xanh ô liu, khăn thành cam. [6_s05.jpg](6_s05.jpg) |
| 9 | s08 | 552–599 → **588** | -11,4° / 1,1°; c3 0°, sheet "Chính diện" | thân -0,1%, tay trên -11,0%, cẳng tay +19,1% | thân: đầu cúi/ngẩng/nghiêng: co ngắn > 2% (foreshorten 0.974); tay trên: đầu cúi/ngẩng/nghiêng: co ngắn > 2% (foreshorten 0.974); cẳng tay: đầu cúi/ngẩng/nghiêng: co ngắn > 2% (foreshorten 0.974) | **CẦN CHỦ DỰ ÁN XEM** (số đo) | Bóng đen trong sương, đọc đúng dáng (mũ, thang, đèn lồng); cờ vì cẳng tay (không che, không gập) dài hơn tham chiếu 0° 19,1%, còn +16,0% sau hiệu chỉnh đầu cúi 0,974. [9_s08.jpg](9_s08.jpg) |
| 15 | s12 | 888–916 → **888** | 108,4° / 24,9°; c3 90°, sheet "Nghiêng" | thân -22,7%, cẳng tay khuất | thân: góc nhìn lệch > 30° mọi góc tham chiếu (lệch 30.6° so với 90° (view 108.38°, ngẩng 24.85°)); tay trên: góc nhìn lệch > 30° mọi góc tham chiếu (lệch 30.6° so với 90° (view 108.38°, ngẩng 24.85°)); cẳng tay: góc nhìn lệch > 30° mọi góc tham chiếu (lệch 30.6° so với 90° (view 108.38°, ngẩng 24.85°)) | không cờ | Cận gáy từ sau-bên, thấy búi tóc xám, khăn, mũ nâu sẫm (độ sáng 26); góc thật gần 135° hơn 90°. [15_s12.jpg](15_s12.jpg) |
| 18 | s14 | 996–1043 → **1008** | 25,3° / 44,9°; c3 45°, sheet "3/4" | không có mặt nạ đầu | thân: không có mặt nạ đầu (khuất hoặc ngoài khung); tay trên: không có mặt nạ đầu (khuất hoặc ngoài khung); cẳng tay: không có mặt nạ đầu (khuất hoặc ngoài khung) | không cờ | Máy nhìn từ trên xuống 45°, đầu bị đèn che, chỉ thấy vai, hai tay, áo; không đủ để so model. [18_s14.jpg](18_s14.jpg) |
| 22 | s21 | 1140–1187 → **1164** | 41,9° / 10,6°; c3 45°, sheet "3/4" | thân -34,6%, tay trên -22,7%, cẳng tay +20,4% | thân: chạm mép khung (bị cắt); tay trên: bị che > 10% (34%); cẳng tay: bị che > 10% (19%) | không cờ | Cận vai: mũ đen, tóc bạc, hoa tai, khăn đỏ mận, áo xanh sẫm, khớp bible v1.2. [22_s21.jpg](22_s21.jpg) |
| 23 | s22 | 1188–1259 → **1188** | -18,1° / 15,2°; c3 0°, sheet "Chính diện" | thân -61,2%, tay trên khuất, cẳng tay khuất | thân: bị che > 10% (38%); tay trên: bị che > 10% (100%); cẳng tay: bị che > 10% (100%) | không cờ | Cận mặt chính diện: mắt nâu, hoa tai, khăn, cổ áo cao, mũ đen, khớp bible v1.2. [23_s22.jpg](23_s22.jpg) |
| 29 | s27 | 1536–1607 → **1536** | 99,4° / -1,3°; c3 90°, sheet "Nghiêng" | thân -12,3%, tay trên khuất, cẳng tay khuất | thân: phối cảnh: độ sâu lệch đầu > 2% (depth 0.960); tay trên: khuất ở góc tham chiếu (c3_views ghi null) (90°); cẳng tay: khuất ở góc tham chiếu (c3_views ghi null) (90°) | **CẦN CHỦ DỰ ÁN XEM** (số đo) | Gần như bóng đen trên nền tối, không đánh giá được bằng mắt; cờ vì thân (không che, không gập) ngắn hơn tham chiếu 90° 12,3%; máy loại do phối cảnh (độ sâu 0,960), nếu trừ phần này còn khoảng −8,7%. [29_s27.jpg](29_s27.jpg) |
| 33 | s31 | 1776–1847 → **1776** | 69,7° / 20,1°; c3 90°, sheet "Nghiêng" | thân -76,1%, tay trên khuất, cẳng tay khuất | thân: chạm mép khung (bị cắt); tay trên: khuất ở góc tham chiếu (c3_views ghi null) (90°); cẳng tay: khuất ở góc tham chiếu (c3_views ghi null) (90°) | không cờ | Cận mặt nghiêng: mũ đen, búi tóc, lọn tóc thái dương, hoa tai, khăn, khớp bible v1.2. [33_s31.jpg](33_s31.jpg) |
| 36 | s34 | 2088–2135 → **2088** | 148,7° / 1,8°; c3 135°, sheet "Sau lưng" (lệch 31°, > 30°) | thân +13,7%, tay trên -59,3%, cẳng tay khuất | thân: đầu cúi/ngẩng/nghiêng: co ngắn > 2% (foreshorten 0.898); tay trên: đầu cúi/ngẩng/nghiêng: co ngắn > 2% (foreshorten 0.898); cẳng tay: đầu cúi/ngẩng/nghiêng: co ngắn > 2% (foreshorten 0.898) | không cờ | Sau lưng chếch dưới ánh cam: dáng thẳng, búi tóc, mũ phớt; góc sheet cách 31°. [36_s34.jpg](36_s34.jpg) |
| 38 | s36 | 2232–2279 → **2268** | -24,9° / 9,3°; c3 -45°, sheet "3/4" (lật) | thân -43,0%, tay trên -58,3%, cẳng tay khuất | *suy từ views:* thân: bị che 40%, phối cảnh 1.038, chạm mép; tay trên: bị che 28%, gập 0.862, phối cảnh 0.945, chạm mép; cẳng tay: bị che 100%, gập 0.359, phối cảnh 0.845 | **CẦN CHỦ DỰ ÁN XEM** (màu) | Cận mặt dưới đèn: mũ nâu vàng sáng hơn áo (độ sáng 87 so với 76); mặt, hoa tai, khăn khớp bible v1.2. [38_s36.jpg](38_s36.jpg) |
| 39 | s37 | 2280–2418 → **2412** | -24,5° / 18,2°; c3 -45°, sheet "3/4" (lật) | thân khuất, tay trên khuất, cẳng tay khuất | *suy từ views:* thân: bị che 100%, phối cảnh 1.059; tay trên: bị che 100%, gập 0.860, phối cảnh 0.887; cẳng tay: bị che 100%, gập 0.370, phối cảnh 0.696 | **CẦN CHỦ DỰ ÁN XEM** (màu) | Cận mặt: vành mũ nâu vàng (RGB ≈ 152,68,25), đọc thành mũ màu khác hẳn mũ đen ở s21, s22, s31. [39_s37.jpg](39_s37.jpg) |
| 41 | s38 | 2486–2519 → **2496** | -56,9° / -9,4°; c3 -45°, sheet "3/4" (lật) | không có mặt nạ đầu | *suy từ views:* thân: không có mặt nạ đầu; tay trên: không có mặt nạ đầu; cẳng tay: không có mặt nạ đầu | không cờ | Shot của Cas; Ida chỉ là mảng áo tối ở mép trái, không có đầu trong hình. [41_s38.jpg](41_s38.jpg) |
| 42 | s39 | 2520–2625 → **2520** | -24,4° / 18,5°; c3 -45°, sheet "3/4" (lật) | thân khuất, tay trên khuất, cẳng tay khuất | *suy từ views:* thân: bị che 100%, phối cảnh 1.059; tay trên: bị che 100%, gập 0.860, phối cảnh 0.885; cẳng tay: bị che 100%, gập 0.369, phối cảnh 0.690 | **CẦN CHỦ DỰ ÁN XEM** (màu) | Cận mặt dưới đèn: vành mũ nâu nhạt (RGB ≈ 141,79,45), gần bằng độ sáng cổ áo (90 so với 97). [42_s39.jpg](42_s39.jpg) |
| 43 | s40 | 2626–2668 → **2652** | -6,5° / 22,3°; c3 0°, sheet "Chính diện" | thân -46,9%, tay trên khuất, cẳng tay khuất | *suy từ views:* thân: gập 0.958, phối cảnh 1.069, chạm mép; tay trên: bị che 100%, gập 0.917, phối cảnh 0.970; cẳng tay: bị che 100%, gập 0.388, phối cảnh 0.871 | không cờ | Cận mặt dưới vành mũ khi đèn đang tắt: mũ nâu sẫm (độ sáng 52), khớp dáng và trang phục. [43_s40.jpg](43_s40.jpg) |
| 44 | s40 | 2669–2687 → **2676** | -6,5° / 22,3°; c3 0°, sheet "Chính diện" | thân -46,9%, tay trên khuất, cẳng tay khuất | *suy từ views:* thân: gập 0.958, phối cảnh 1.069, chạm mép; tay trên: bị che 100%, gập 0.917, phối cảnh 0.970; cẳng tay: bị che 100%, gập 0.388, phối cảnh 0.871 | không cờ | Cùng khung hình s40 sau khi đèn tắt: mũ đen, khăn, hoa tai, khớp bible v1.2. [44_s40.jpg](44_s40.jpg) |
| 47 | s42a | 2772–2819 → **2772** | -65,6° / -0,3°; c3 -45°, sheet "3/4" (lật) | thân -6,8%, tay trên khuất, cẳng tay khuất | *suy từ views:* thân: chạm mép; tay trên: bị che 100%, phối cảnh 0.958; cẳng tay: bị che 100%, phối cảnh 0.952 | không cờ | Ida ở mép phải khung, nghiêng đầu xuống: mũ đen, khăn đỏ, thắt lưng, áo xanh, khớp. [47_s42a.jpg](47_s42a.jpg) |
| 51 | s44 | 3036–3095 → **3084** | 48,2° / -0,3°; c3 45°, sheet "3/4" | thân +1,7%, tay trên -8,9%, cẳng tay +43,7% | *suy từ views:* thân: gập 0.979, đầu cúi/ngẩng 0.865, phối cảnh 0.951; tay trên: gập 0.915, đầu cúi/ngẩng 0.865; cẳng tay: gập 1.037, đầu cúi/ngẩng 0.865, phối cảnh 0.968 | không cờ | Toàn thân 3/4 ngược sáng, tay giơ chào: dáng chữ A, mũ, khăn, khớp. [51_s44.jpg](51_s44.jpg) |
| 55 | s47 | 3252–3299 → **3252** | 176,8° / 7,1°; c3 180°, sheet "Sau lưng" | thân +16,2%, tay trên +17,5%, cẳng tay +17,5% | *suy từ views:* thân: đầu cúi/ngẩng 0.972, phối cảnh 0.978; tay trên: gập 0.977, đầu cúi/ngẩng 0.972, phối cảnh 0.975; cẳng tay: đầu cúi/ngẩng 0.972, phối cảnh 0.968 | **CẦN CHỦ DỰ ÁN XEM** (số đo) | Sau lưng vác thang, đọc đúng dáng; cờ vì thân +16,2% và cẳng tay +17,5% (không che, không gập; +12,9% và +14,2% sau hiệu chỉnh đầu 0,972): đầu đọc nhỏ so với thân. Thang dựng gần đứng thay vì 28° như sheet. [55_s47.jpg](55_s47.jpg) |

## Shot bị cờ: CẦN CHỦ DỰ ÁN XEM (9 đoạn máy, 8 shot phim)

**Nhóm màu (6 đoạn): mũ và áo đổi màu dưới đèn khí.** Mắt người xem sẽ thấy mũ đen ở s21, s22, s31, s40 (sau khi đèn tắt) nhưng nâu vàng ở các shot dưới đây. Quan hệ sáng–tối của sheet ("mũ tối nhất, áo tối trung bình") bị đảo. Nhiều khả năng do ánh sáng/grade chứ không do hình học, vì albedo mũ đã cố định #2b2a2a (v1.2). Chủ dự án quyết: chấp nhận như hiệu ứng ánh đèn, hay yêu cầu chỉnh ánh sáng/grade.
- **s03** (máy 4, khung 228): áo xanh lá sáng, mũ nâu vàng nhạt (RGB ≈ 164,90,41).
- **s04** (máy 5, khung 276): như s03, hình nhoè mạnh.
- **s05** (máy 6, khung 360): mũ nâu đất, không tối hơn áo; áo xanh ô liu, khăn cam.
- **s36** (máy 38, khung 2268): mũ sáng hơn áo (87 so với 76).
- **s37** (máy 39, khung 2412): vành mũ nâu vàng (RGB ≈ 152,68,25).
- **s39** (máy 42, khung 2520): vành mũ nâu nhạt, gần bằng độ sáng cổ áo.

**Nhóm số đo (3 đoạn): lệch > 10% ở bộ phận không che, không gập, không chạm mép.** Bằng mắt cả ba đều đọc đúng Ida; cần chủ dự án xác nhận.
- **s08** (máy 9, khung 588): cẳng tay +19,1% (+16,0% sau hiệu chỉnh đầu). Bóng đen trong sương.
- **s27** (máy 29, khung 1536): thân −12,3% (khoảng −8,7% nếu trừ phối cảnh). Gần như bóng đen, mắt không kiểm được.
- **s47** (máy 55, khung 3252): thân +16,2%, cẳng tay +17,5%; đầu đọc nhỏ so với thân ở góc sau lưng, ngẩng 7°. Thang dựng gần đứng, khác góc 28° của sheet.

## Không cờ (12 đoạn máy)
s03 (máy 3), s12, s14, s21, s22, s31, s34, s38, s40 (máy 43 và 44), s42a, s44. Lý do chính: cận cảnh thân bị cắt ở mép, bộ phận bị che/gập, hoặc không có đầu trong hình (s14, s38). Mặt, hoa tai, khăn, tóc khớp bible v1.2.

## Chỉ số gần ngưỡng (±5%)
- s34 (máy 36): góc thật cách hình "Sau lưng" 31° (ngưỡng 30°). Máy tính gần nhất là 135° của `c3_views`, nhưng sheet chỉ có 4 hình.
- s12 (máy 15): máy nêu lệch góc 30,6° (ngưỡng 30°).
- Không số đo tỷ lệ nào nằm trong 9,5–10,5%.

## Giới hạn
- `MS-ida.png` là bản Cổng 3 vòng 1, chưa phản ánh thiết kế đã khoá v1.2; so sánh trang phục dựa thêm vào `ida.json` và `bible/characters.md`.
- Lý do máy cho 8 đoạn từ khung 2232 là suy từ `views`, do danh sách đầu vào bị cắt ở 300 mục.
- Màu đo trên video đã grade, lấy trung bình ô vuông nhỏ chọn tay; chỉ để tham khảo.
- Mỗi đoạn chỉ xem 1 khung; lệch thoáng qua ở khung khác có thể bị bỏ sót.

## Việc đang chờ chủ dự án
1. Xem 9 ảnh bị cờ và quyết định cho nhóm màu mũ/áo dưới đèn khí.
2. Xác nhận 3 shot cờ theo số đo là đúng model.
3. Cân nhắc cập nhật `MS-ida.png` theo bible v1.2 để các vòng sau có hình chuẩn đúng.
