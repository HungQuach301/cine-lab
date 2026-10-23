# Đăng T3 Gibraltar lên YouTube — hướng dẫn từng bước (phiên PHAT-HANH-T3, 23/10/2026)

Mọi tệp nằm ở **gốc nhánh `release-k2-t3-g2`** của repo `HungQuach301/cine-lab`. Chữ dán vào YouTube là tiếng Anh; hướng dẫn này tiếng Việt.
Ký hiệu: **[BẮT BUỘC]** = phải làm đúng như ghi, sai là lệch luật kênh/giấy phép/chính sách YouTube. **[NÊN]** = khuyến nghị. **[TUỲ]** = chủ dự án quyết.

## 0. Tải tệp về máy
| Tệp | Link tải công khai | Kiểm |
|---|---|---|
| Master `k2-t3-v1-master.mp4` (1,79 GB, LFS) | https://media.githubusercontent.com/media/HungQuach301/cine-lab/release-k2-t3-g2/k2-t3-v1-master.mp4 | SHA-256 `5b9f0bccd88830ab212a6747259ac597328ae87bb964addc953bf1928fd7b682` (phiên này tải lại ngày 23/10 qua link trên: KHỚP) |
| Phụ đề `k2-t3-v1-en.srt` | https://github.com/HungQuach301/cine-lab/raw/release-k2-t3-g2/k2-t3-v1-en.srt | 129 câu |
| Tiêu đề / mô tả / tags / bình luận ghim | `k2-t3-v1-title.txt`, `k2-t3-v1-youtube-description.txt`, `k2-t3-v1-tags.txt`, `k2-t3-v1-pinned-comment.txt` (+ trả lời dự phòng `k2-t3-v1-pinned-replies.txt`) | mở bằng trình xem "Raw" trên GitHub rồi chép nguyên khối |

Trên Windows kiểm SHA: `certutil -hashfile k2-t3-v1-master.mp4 SHA256`; macOS: `shasum -a 256 k2-t3-v1-master.mp4`.

## 1. Tải lên (YouTube Studio → Create → Upload videos)
1. **[BẮT BUỘC]** Chọn tệp `k2-t3-v1-master.mp4` (không dùng 3 phần p1–p3; đó là bản xem).

## 2. Trang "Details"
2. **[BẮT BUỘC] Title:** dán nguyên dòng trong `k2-t3-v1-title.txt`: `Gibraltar: From 14 Sieges to a Runway | 3D Timelapse` (52 ký tự).
3. **[BẮT BUỘC] Description:** dán NGUYÊN KHỐI `k2-t3-v1-youtube-description.txt` (4 245 ký tự, giới hạn 5 000). Không sửa phần CREDITS: ghi công nhạc CC BY 4.0 (Scott Buckley yêu cầu ghi trong mô tả YouTube; nhạc có Content ID — thiếu dòng này dễ bị khiếu nại), dòng NPS "No claim to original U.S. Government works", dòng OpenStreetMap (ODbL), Copernicus, Catastro và Open Parliament Licence đều là điều kiện giấy phép. Sau khi dán, kiểm YouTube đã tự nhận 7 chương (dòng `0:00 …` đầu tiên).
4. **[BẮT BUỘC] Thumbnail:** chủ dự án tự tạo bằng AI (quyết định 23/10 10:45). Khuyến nghị khi tạo:
   - **[NÊN]** dùng một khung CÓ TRONG PHIM làm gốc (ví dụ 6 ứng viên `k2-t3-v1-thumb-1…6.jpg` ở cùng nhánh: H2T pin nổi cháy, chạng vạng → đêm; hoặc một khung bất kỳ chụp từ master) — Kinh thánh §14.5 "góc máy thumbnail phải có trong phim".
   - **[BẮT BUỘC]** không thêm sự kiện/vật phim không có (ví dụ không thêm trận đánh 1704 trong cảnh 1782, không máy bay hiện đại trong cảnh 1782, không tàu/đường băng sai năm); không logo thương hiệu (hãng hàng không, công ty), không chữ của AI tự sinh.
   - **[BẮT BUỘC]** luật hình chiến tranh §10.6: không vũ khí chĩa vào người, không lửa có người, không cờ làm điểm nhấn, không biểu tượng cực đoan/tôn giáo, không máu/thi thể.
   - **[NÊN]** 1280×720 trở lên, 16:9, JPG/PNG ≤ 2 MB; chữ trên thumbnail (nếu có) ≤ 4 từ, đúng lời khoá (ví dụ "14 sieges" đúng; "15 sieges" sai).
   - **[BẮT BUỘC sau khi đăng]** gửi lại cho phiên P: tên công cụ/mô hình AI, ngày tạo, tệp gốc đã dùng (nếu là khung phim thì mốc thời gian) → ghi vào `RIGHTS.md` dòng T3-THUMB (hiện để "chờ chủ dự án").
5. **[TUỲ] Playlists:** "Contested Places" (nếu đã lập).
6. **[BẮT BUỘC] Audience:** chọn **"No, it's not made for kids"**. Age restriction: **No** (phim không có máu/thi thể; thương vong nói bằng số).
7. Bấm **Show more**:
   - **[BẮT BUỘC] AI use / Altered or synthetic content = Yes.** Trang trợ giúp YouTube "Disclosing use of GenAI content" (https://support.google.com/youtube/answer/14328491, phiên này đọc ngày 23/10/2026) hiện gọi mục này là **"AI use"** trong phần **Attributes** (tên cũ "Altered or synthetic content"). Lý do Yes: 4 cảnh minh hoạ AI giống thật (Gemini Omni, 27,4 s: 0:04, 1:48, 3:27, 4:01) — trang nêu ví dụ phải khai "AI generated extra footage of a real place"; và lời đọc là giọng tổng hợp (ElevenLabs). Kinh thánh §14.1 (f) bắt buộc bật khi tập có khung AI giống thật hoặc giọng tổng hợp. Nếu Studio hỏi thêm loại: chọn mục có "realistic scene"/"altered footage of a real place" và mục giọng/âm thanh tổng hợp.
   - **[BẮT BUỘC] Paid promotion:** không đánh dấu (không có tài trợ).
   - **[BẮT BUỘC] Automatic chapters:** bỏ chọn (dùng chương trong mô tả).
   - **[NÊN] Featured places:** để trống.
   - **[BẮT BUỘC] Tags:** dán `k2-t3-v1-tags.txt` (20 thẻ; 428 ký tự kể cả dấu ngoặc YouTube tự thêm cho thẻ có dấu cách; giới hạn 500).
   - **[BẮT BUỘC] Language and captions certification:** Video language = **English**; Caption certification = "This content has never aired on television in the U.S."
   - **[NÊN] Recording date / location:** để trống (phim tái dựng, không quay thật).
   - **[BẮT BUỘC] License:** Standard YouTube License (KHÔNG chọn Creative Commons — nhạc CC BY và dữ liệu Copernicus không cho cấp phép lại). Distribution: Everywhere. Allow embedding: bật. Publish to subscriptions feed: bật.
   - **[NÊN] Category:** **Education**.
   - **[NÊN] Comments:** On; sắp "Top"; kiểm duyệt cơ bản (Basic).
   - **[NÊN] Shorts remixing:** cho phép chỉ phần hình (tuỳ).

## 3. Trang "Video elements"
8. **[BẮT BUỘC] Add subtitles:** Upload file → **With timing** → chọn `k2-t3-v1-en.srt` → ngôn ngữ English. Phim không ghép cứng phụ đề nên tệp này là phụ đề CC duy nhất.
9. **[TUỲ] End screen:** 20 s cuối là hai thẻ "How this film was made" (12:25–12:42) — phần tử màn hình kết thúc sẽ che chữ thẻ. Khuyến nghị: chỉ 1 nút Subscribe đặt góc trên-phải, 5 s cuối (12:37–12:42); xem lại bản xem trước, nếu che dòng chữ thẻ PP2 thì bỏ màn hình kết thúc. Không thêm "Next video" tới tập chưa có.
10. **[TUỲ] Cards:** không cần.

## 4. Trang "Checks" và "Visibility"
11. Chờ Copyright check. Nếu có khiếu nại Content ID về nhạc Scott Buckley/Kevin MacLeod: dòng ghi công đã có trong mô tả — dùng "Dispute → I have a license" và dán dòng ghi công; báo phiên P.
12. **[TUỲ]** Public ngay hoặc Schedule.

## 5. Sau khi công khai
13. **[BẮT BUỘC] Bình luận ghim:** đăng NGUYÊN KHỐI `k2-t3-v1-pinned-comment.txt` (6 558 ký tự) dưới tài khoản kênh → ⋮ → **Pin**. Nếu YouTube báo quá dài, tách tại các dòng `SOURCES 1/5 … 5/5`: phần mở đầu làm bình luận ghim, 5 phần nguồn đăng thành 5 trả lời ngay dưới nó.
14. **[TUỲ]** Trả lời dự phòng `k2-t3-v1-pinned-replies.txt` (4 khối) chỉ dùng khi người xem hỏi đúng ý đó.
15. **[NÊN]** Ghi lại cho phiên P: link video, giờ đăng, trạng thái nhãn AI YouTube hiện (trong trình phát hay trong mô tả), mọi khiếu nại bản quyền. Đo bình luận chê giọng/AI ≤ 2 % (Kinh thánh §10.1, mẫu 100 bình luận).

## 6. Mục nào bắt buộc (tóm tắt)
Tệp master · tiêu đề · mô tả nguyên khối (ghi công) · thumbnail theo 3 điều cấm · Not made for kids · AI use = Yes · tags · English + phụ đề .srt · Standard License · bình luận ghim. Còn lại là khuyến nghị/tuỳ.
