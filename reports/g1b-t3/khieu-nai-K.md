# Khiếu nại luật — G1b T3 → phiên K (cho checks 1.16)

Phiên G1b T3 (nhánh thật `ccr-6189ede9-lpjwe0`). Không đọc mã `checks/`; chỉ dựa trên kết quả `k2check.py … --cap` 1.15.0 trên animatic toàn tập (`reports/g1b-t3/do/k2check-1.15-animatic.txt`) và báo cáo K đã công bố. Căn cứ luật mới: Kinh thánh §12.1 (KHUNG SẠCH, CHU-1 = A, chủ dự án duyệt 18/10 23:15) — §12 thắng khi trái.

## A-G1B-1 · K-LAI-2 đòi nhãn AI trên hình suốt shot — trái §12.1
- **Hiện tượng:** K-LAI-1…6 TRƯỢT ("—"). Tập có `ai_image` (khung neo KA1782, KB1943) và `ai_texture` (2m — vân HC7 King's Bastion). §12.1 bỏ nhãn "Surface detail AI-assisted" khỏi hình; công bố chuyển sang mô tả + bình luận ghim + thẻ "How this film was made" + trường "AI use = Yes" của YouTube (P10C-2).
- **Đề xuất:** K-LAI-2 đổi thành: (a) cờ `ai_image`/`ai_texture` có trong log khung và đặc tả shot; (b) tập có thẻ phương pháp cuối (đoạn khai `the_phuong_phap`, 4–5 s) nêu cách dùng AI; (c) `phat-hanh/nguon-mo-ta.md` có câu "AI use = Yes". Bỏ đo cỡ chữ nhãn trên hình.
- **Ghi thêm:** K-LAI-3…6 TRƯỢT vì đặc tả animatic không khai khối `lai:` (chưa nối sổ kiểm dữ kiện của V6/PT3) — đó là việc của tập (sẽ khai ở bản sản xuất), không phải khiếu nại.

## A-G1B-2 · NC-H5 (b) nhãn nguồn ghost ≥ 38 px, ≥ 3 s lần đầu — trái §12.1
- §12.1 bỏ "dòng nguồn cho mọi cảnh 3D/bản đồ". Kết quả lượt này: NC-H5 "không áp (tập không có bộ đếm năm/timelapse)" — bộ kiểm không nhận ra bộ đếm năm của cảnh tl/t3s (bộ đếm vẽ ở lớp 2D qua `_tl.chrome`). Khi K sửa nhận diện, (b) sẽ TRƯỢT theo cấu trúc.
- **Đề xuất:** NC-H5 (b) đổi thành: lớp ghost có `src` trong log/đặc tả + nguồn có trong mô tả/bình luận ghim. Giữ nguyên (a) năm xây ≤ bộ đếm (Chặn).

## A-G1B-3 · BD-3 nhãn "approx. borders c. YYYY — nguồn" + inset "Map: Natural Earth" — trái §12.1
- Lượt này BD-3 "không có lớp bien_gioi_lich_su hiện" (ĐẠT vì không vẽ nhãn); BD-8 "không có log inset". Khi lớp ranh khai đầy đủ ở bản sản xuất, BD-3 sẽ đòi nhãn trên hình.
- **Đề xuất:** BD-3 xét nhãn trong log (vai `bien_gioi`, alpha 0 được) + nguồn ranh trong mô tả; không đòi hiện trên hình.

## A-G1B-4 · Q26b đếm bối cảnh theo `scene_id` — cảnh tổng quát `tl/t3s` thành MỘT bối cảnh
- **Hiện tượng:** Q26b TRƯỢT "lớn nhất tl/t3s 57,6 % · liên tục dài nhất tl/t3s 165 s". `tl/t3s` là MỘT mô-đun dựng mọi cảnh 3D của tập (37 vùng, 12 mốc năm: 1704 → 2026). Q26b-K2 (theo `vung`) ĐẠT: lớn nhất eo-dat 22,4 %, nửa sau 22 vùng.
- **Đề xuất:** với cảnh tl, Q26b dùng `vung` (như Q26b-K2) hoặc (scene_id, vung, mốc năm), không dùng scene_id đơn thuần.

## A-G1B-5 · Q37 — khung neo và tấm im lặng 8–10 s
- Q37 "dài nhất 10,0 s" = các khung neo (KA1782 8 s, KB1943 8 s, KC1910 7 s, KB2026 9,5 s, KC2026 10 s, KA2026 8 s — tấm im lặng). Kinh thánh §11.2: "chỉ khung neo giữ 6–10 s"; §11.2 tấm im lặng 8–10 s.
- **Đề xuất:** Q37 "dài nhất ≤ 6 s" miễn shot khai `neo: true` / `im_lang: true` trong 6–10 s; vẫn tính TB.
- Ngoài khung neo: mọi shot 3D chia cú ≤ 6 s (khoảng dài nhất ngoài khung neo = 6,0 s); TB biến cố 3,95 s > 3,5 s — đó là số thật của tập, không khiếu nại.

## A-G1B-6 · Thước "cạnh mới > 5 %" cho phục chế ảnh (§12.3)
- Phiên con phục chế đo: chỉ phóng bicubic đã ra 3,95–6,40 % "cạnh mới" trên 3 ảnh NARA 342-FH (do hạt phim). Ngưỡng 5 % nằm trong vùng nhiễu nền của thước (`reports/g1b-t3/phuc-che/KQ.md`). Đề xuất K hiệu chuẩn thước (trừ nền bicubic, hoặc chỉ tính cạnh dài ≥ N px) trước khi đưa vào bộ kiểm.

## A-G1B-7 · A1–A13 khi tập chưa có lời
- Animatic chỉ có nhạc nền tạm (ElevenLabs 0 theo lệnh): A1 −18,0 LUFS, A4 "không có stem". Như A-V6-2: đề xuất A* KHÔNG ÁP khi tập không khai `vo` và đặc tả ghi `animatic: true`.
