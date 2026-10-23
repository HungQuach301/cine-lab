# TỜ SO SÁNH 6 BẢN THỬ — TIEN-KY-T4 (23/10/2026)

> Mọi bản xem 640×360 (≤ 10 s, ≤ 5 MB) + một khung 1080p trong `reports/tien-ky-t4/xem/`. Số đo lấy từ log của chính phiên (s/khung = đồng hồ, gồm khử răng cưa/tích luỹ). Tiền = chi thật.

## T1 — Lửa/khói thể tích, ngày + đêm: A (atlas nướng sẵn) vs Cycles GPU
| | Cách A (three.js + llvmpipe, atlas thể tích numpy) | Cycles GPU (Blender 5.2.2, RTX 5090, miền thể tích đơn theo bản đồ giờ bén lửa) |
|---|---|---|
| Tệp xem | `T1-lua-A-vs-Cycles.mp4` (màn chia đôi cùng cú máy: trái A, phải Cycles; ngày 5 s + đêm 5 s) · `T1-to-so-2x2.jpg` (khung đầy đủ) | như trái |
| 1080p | `T1-A-ngay-1080.jpg`, `T1-A-dem-1080.jpg` | `T1-Cycles-ngay-1080.jpg`, `T1-Cycles-dem-1080.jpg` |
| s/khung | @@T1A@@ | 960×540: ngày 12,36 (đo thử 48 khung) / 16,1 (72 khung còn lại) · đêm 6,38 (48 spp) · 1080p: ngày 45,6 / đêm 15,3 |
| Tiền | 0 (CPU container) | pod 1,62 h × $1,19 = **$1,93** (số dư RunPod 23,08 → 21,18) — gồm cài đặt, đo thử, dựng 240 khung + 2 khung 1080 |
| Đọc hình | khói cột xám đậm bốc theo gió đông → tây (b39), lửa theo giờ trên mặt phố, ánh lửa phủ mặt tiền; đêm: bầu trời nhuộm cam, khói đỏ phía dưới | đêm: vành lửa sáng đúng ranh giờ, ánh phản chiếu sông tốt; **ngày: khói nhạt như sương, lộ mép hộp miền thể tích (vách đứng trên sông), không thành cột** |
| Lỗi thấy | hạt lửa rơi trên mặt sông (ô lưới giờ cháy phủ lòng sông) → **đã sửa** trong `page.js` (bỏ ô có nền 1666 < 1,2 m) và dựng lại; bờ sông bậc thang, nền bến bãi màu cát nhạt | mép miền thể tích; khói thiếu mật độ/đổ bóng; mức tối đêm quá sâu so A |
| Kết luận | **A tốt hơn ở bản thử này** cho cảnh rộng | cần sửa mép (mờ dần biên miền theo khoảng cách tới ô cháy) + mật độ khói rồi thử lại (≈ $2) trước khi dùng cho 3–4 cận đêm |

## T2 — Bản đồ cổ hoạt hoá → 3D cùng toạ độ (Bankside)
- Tệp: `T2-ban-do-hoat-hoa.mp4` (10 s) · `T2-ban-do-1080.jpg`.
- Bản đồ Doornick 1666 (Rijks PDM) uốn TPS lên EPSG:27700 (13 điểm, affine RMS 44,2 m / LOO 58,8 m); ranh cháy theo ngày (Chủ nhật → thứ Năm) phủ màu nhân lên nét khắc, nét khắc gốc vẫn đọc được; nhãn chỉ 3 tên + ngày (§17 "rất ít ký tự"). 0–6 s bản đồ, 6–7,5 s hoà sang 3D cùng ma trận máy (không nhảy hình).
- Đo: nhãn "St Paul's" (toạ độ mái vòm) lệch hình vẽ nhà thờ trên bản khắc ≈ 85 m (≈ 2 × RMS) — bản khắc vẽ nhà thờ kiểu tượng hình; sản xuất: thêm St Paul's làm điểm khống chế hoặc đặt nhãn theo hình vẽ.
- Pha 3D thiên đỉnh còn phẳng (nhà xám đồng màu) — đúng mức bản thử, chưa đạt chuẩn điện ảnh.
- s/khung A 4,3 (1280×720); 0 $.

## T3 — Tranh Hollar Old St Paul's → 3D cùng góc (không AI)
@@T3@@

## T4 — Ba cú máy ở Bankside 1666 → 2026 + khớp cắt
- Tệp: `T4-cu-may.mp4` (10 s: đẩy vào 3 s · vòng cung 3 s · cẩu lộ 2,5 s · khớp cắt 1,5 s) · `T4-a-day-1080.jpg`. Đo `do/t4-may.json` (neo = mái vòm St Paul's):

| Đoạn | Tiêu điểm %/s khung (TB/max) | Máy m/s | Quay °/s (TB/max) | Năm/s | Ghi chú |
|---|---|---|---|---|---|
| a đẩy vào | 0,85 / 1,06 | 27,5 | 0,23 / 0,29 | 14,9 | đạt ≤ 1,5 %/s, ≤ 3°/s |
| b vòng cung | 1,08 / 1,66 | 148 | **10,6 / 12,6** | 74,3 | **vượt ≤ 3°/s** vì nén vào 3 s cho bản thử; sản xuất cần ≥ 11 s cho cùng cung |
| c cẩu lộ | 0,96 / 1,27 | 106 | 3,74 / 4,77 | 34,9 | vượt nhẹ ≤ 3°/s → kéo dài ≥ 3,2 s |
| d khớp cắt (máy đứng, timelapse) | 0 | 0 | 0 | 240 | lệch neo 0,0 px giữa khung đầu/cuối |
- Khung 1080 (≈ 1704): mức chi tiết nhà/mái còn đồng dạng, nền cát nhạt, bờ sông bậc thang — **chưa đạt chuẩn điện ảnh**, ghi vào việc sản xuất (vật liệu, mái đa dạng, bờ mịn, ánh sáng nướng như T3).
- s/khung A ≈ 5 (1280×720); 0 $.

## T5 — M-d Omni: Pudding Lane ≈ 01:00 2/9/1666 (ảnh đầu = render)
- Tệp: `T5-md-omni.mp4` (10 s) · `T5-omni-khung-720.jpg`. Gemini `gemini-omni-1.1-flash` i2v, **1/3 lượt dùng**, $1,02; bộ kiểm (gpt-6.1-sol + claude-sonnet-5-5 + `checks/ll/q_thoi_dai.py` chỉ chạy): **ĐẠT máy** (0 lỗi mô hình, 0 nghi vấn thời đại; 1 ghi chú tin 0,2 "cột nhọn trên chân trời có thể là Monument" — kiểm lại: là tháp nhà thờ trong cảnh dựng, không có Monument trước 1671 trong hình học).
- **Điểm yếu về liền mạch (tự soi):** ảnh đầu render quá thô và ánh sáng đọc như hoàng hôn (phơi sáng 6 để thấy nhà trong đêm) → mô hình "nhảy" sang cảnh trăng chi tiết trong ≈ 1 s đầu. Sản xuất: ảnh đầu = tấm N2+ đêm dựng từ render (cùng hình học, đủ chi tiết), rồi mới i2v; hoặc cắt bỏ ≈ 1 s đầu. Đề xuất D18 ở phiếu G1.

## T6 — Một tấm N2+ cho shot timelapse máy cố định
- Tệp: `T6-timelapse-n2p.mp4` (6 s, 640×360) · `T6-tam-nen-so.mp4` (trên: render, dưới: ghép tấm — 640×720 để so) · `T6-tam-l2-ghep-1080.jpg` · `T6-render-1080.jpg`.
- OpenAI `gpt-image-2.5-sunburst-2026-09-08` `/v1/images/edits` không mặt nạ, 3 lượt ($0,23) + kiểm 2 mô hình ($0,60): **0/3 ĐẠT máy**.

| Lượt | (i) lớp (a) | (ii) thời đại | (iii) đổi vùng nước↔đất | (iv) đóng băng | Ghi chú |
|---|---|---|---|---|---|
| 1 | trượt (mặt nạ JPEG nhiễu) → ghép lại bằng PNG (1b): đạt | đạt | **trượt** 46,8 % nước → đất (dải "biển" giả ở chân trời cảnh dựng) | đạt | sửa cảnh: bỏ mặt nước ngoài hộp địa hình |
| 2 | đạt | đạt | **trượt** 4,8 % (T9b 2,42 % so ngưỡng 2 %) | đạt | lệnh thêm câu màu nước; nhìn mắt đạt — tấm dùng cho timelapse |
| 3 | trượt (1 vật thể lớp (a)) | đạt | **trượt** 20,6 % đất → nước | đạt | tệ hơn → dừng ở 3 lượt |
- Timelapse: nền = tấm lượt 2 tĩnh; lớp (a) + bóng nắng render từng khung, ghép theo mặt nạ ID PNG; khớp màu Reinhard Lab k 0,7 tính một lần → nhấp nháy vùng (c) **0,078** (đối chứng render 2,42) — không nhấp nháy màu.
