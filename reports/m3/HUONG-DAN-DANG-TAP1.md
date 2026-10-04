# Hướng dẫn đăng tập 1 lên YouTube Studio · Last Lamplighters

P soạn ngày 04/10/2026, sau khi chủ dự án duyệt cổng G2. Cổng G3 (bấm phát hành) do chủ dự án làm.
Tên nút ghi theo giao diện YouTube Studio tiếng Anh. YouTube có thể đổi chỗ nút; nếu không thấy đúng chỗ, tìm theo tên.

## 0. Lấy tệp
**Release GitHub `ll-ep01-v1` chưa tạo được.** GitHub trả HTTP 403: "Creating, editing, or deleting releases is not permitted for this session type." Đây là giới hạn của loại phiên Claude Code, không phải do thiếu quyền repo.

Các tệp đã sẵn sàng ở `/var/tmp/cine-out/ep01/release/` trên máy phiên, kèm `SHA256SUMS.txt`:

| Tệp | Dùng cho | SHA-256 | Có trong git? |
|---|---|---|---|
| `ll-ep01-v1-master-1080p.mp4` (852,9 MB) | video chính | `9c3825387345ec0af6c035ec3f94809644ca7767d1ecbafcaed4710480113942` | **Không** (quá lớn) |
| `ll-ep01-short-S1.mp4` | Short 1 | `b13b66c7…c2c0e3` | `screening/` |
| `ll-ep01-short-S2.mp4` | Short 2 | `253bda06…0a0eb6` | `screening/` |
| `ll-ep01-short-S3.mp4` | Short 3 | `233eef54…3f606` | `screening/` |
| `ll-ep01-thumb-T3.jpg` (1280×720, 141 KB) | thumbnail chính | `e7f5e7a9…a6f24e` | `reports/m3/m2-3/thumb/T3-con-5.jpg` |
| `ll-ep01-thumb-T1.jpg` (1280×720, 196 KB) | thumbnail thử A/B | `323c0d41…2ec2a653` | `reports/m3/m2-3/thumb/T1-den-bung.jpg` |
| `ll-ep01.en.srt` | phụ đề tiếng Anh | `e737c18c…cf4fb` | `reports/m3/m2-3/` |
| `ll-ep01-youtube-description.txt` | tiêu đề và mô tả video chính | `59f4ab5c…021267` | `reports/m3/m2-3/` |
| `ll-ep01-shorts-text.txt` | tiêu đề và mô tả 3 Short | `3eaf2982…b1218` | `reports/m3/m2-3/` |

- SHA đầy đủ của mọi tệp có trong `reports/m3/m2-3/SHA256SUMS-ll-ep01-v1.txt`.

- Master 1080p **chưa có đường tải về máy anh/chị**. Cần chủ dự án chọn cách lấy (xem phần cuối). Sau khi tải về, kiểm SHA trên máy:
  - macOS/Linux: `shasum -a 256 ll-ep01-v1-master-1080p.mp4`
  - Windows: `certutil -hashfile ll-ep01-v1-master-1080p.mp4 SHA256`
  - Kết quả phải đúng `9c3825387345ec0af6c035ec3f94809644ca7767d1ecbafcaed4710480113942`.

## 1. Tải video chính lên
1. Mở studio.youtube.com, đăng nhập đúng kênh Last Lamplighters.
2. Bấm **Create** (góc trên phải), chọn **Upload videos**, chọn `ll-ep01-v1-master-1080p.mp4`.
3. Trong lúc tải, điền bước **Details** (mục 2). Đừng bấm Publish.

## 2. Details: tiêu đề, mô tả, thumbnail, Test & Compare
1. **Title:** dán đúng `London Still Has 5 Lamplighters. Who Are the Last of Our Time?` (62 ký tự).
2. **Description:** mở `ll-ep01-youtube-description.txt`, chép **toàn bộ phần sau dòng `DESCRIPTION`**. Gồm:
   - chapter bắt đầu từ `0:00`;
   - mục Sources;
   - ghi công nhạc Kevin MacLeod: **bắt buộc theo giấy phép CC BY 4.0, không được bỏ hay sửa**;
   - đoạn "How this film was made".
3. **Thumbnail:**
   - Bấm **Test & compare** dưới mục Thumbnail. Nếu không thấy, xem ghi chú ở mục 2.4.
   - Tải **T3** (`ll-ep01-thumb-T3.jpg`) làm phương án 1, **T1** (`ll-ep01-thumb-T1.jpg`) làm phương án 2.
   - Bấm **Done**.
   - YouTube chia lượt hiển thị giữa các thumbnail và chọn bản thắng theo thời lượng xem. Kết quả thường có sau vài ngày tới khoảng 2 tuần.
4. **Nếu không có Test & compare:**
   - Tính năng này cần **Advanced features** đã bật (xác minh kênh) và chỉ có trên máy tính.
   - Tạm thời: chọn **Upload thumbnail**, tải T3. Sau khi bật được tính năng, vào lại video (Content → video → Details) để thêm thử A/B với T1.
5. **Playlist:** tạo hoặc chọn playlist "Last Lamplighters" (không bắt buộc).
6. **Audience:** chọn **"No, it's not made for kids"**. Phim nói về lao động và dự báo việc làm, dành cho người lớn; không nhắm tới trẻ em theo COPPA.
   - Mục **Age restriction (advanced):** để **"No, don't restrict…"**.
7. Bấm **Show more** và điền tiếp:
   - **Paid promotion:** không đánh dấu (không có tài trợ).
   - **Altered content:** xem mục 3.
   - **Automatic chapters:** để bật. Chapter thủ công trong mô tả sẽ được ưu tiên.
   - **Tags (tuỳ chọn):** `lamplighters, gas lamps, London, history of work, automation, jobs, BLS projections, future of work, animation`
   - **Language and captions certification:** Video language = **English**. Caption certification: **"This content has never aired on television in the U.S."**
   - **Recording date / location:** để trống.
   - **License:** Standard YouTube License.
   - **Allow embedding:** bật. **Publish to subscriptions feed:** bật.
   - **Category:** **Education**.
   - **Comments:** On. Chọn "Hold potentially inappropriate comments for review".

## 3. Mục "Altered content" (nội dung tạo hoặc sửa bằng AI)
- **Chính sách hiện hành** (trang YouTube "Disclosing use of altered or synthetic content", P đọc ngày 04/10/2026):
  - **Phải** chọn **Yes** khi nội dung **trông như thật** mà được tạo hoặc sửa bằng AI. Ví dụ: người thật nói hay làm điều họ không làm; sửa cảnh quay sự kiện hoặc địa điểm có thật; cảnh như thật chưa từng xảy ra.
  - **Không bắt buộc** với nội dung rõ ràng không thật hoặc hoạt hình, với hiệu ứng nhỏ, và với AI dùng để hỗ trợ sản xuất (kịch bản, thumbnail, tiêu đề, infographic).
- **Đối chiếu với tập 1:**
  - hình là hoạt hình phong cách hoá, không có cảnh quay thật;
  - nhân vật là hư cấu;
  - không có người thật bị làm giả;
  - giọng kể là giọng thư viện ElevenLabs, không nhái người thật;
  - nhạc do người sáng tác (Kevin MacLeod).
- **Khuyến nghị của P:** chọn **No**. Minh bạch đã có ở đoạn "How this film was made" trong mô tả.
- **Phương án thận trọng:** chọn **Yes** nếu anh/chị muốn có nhãn. Theo trang chính sách, bật nhãn không giới hạn người xem và không ảnh hưởng điều kiện kiếm tiền. Quyết định là của chủ dự án ở G3.
- **Kiểm lại trang chính sách ngay trước khi bấm Publish,** vì YouTube có thể đổi quy định.

## 4. Phụ đề
1. Sang bước **Video elements**, bấm **Add** ở mục **Add subtitles**.
2. Nếu được hỏi ngôn ngữ, chọn **English**.
3. Chọn **Upload file**, chọn **With timing**, bấm Continue, chọn `ll-ep01.en.srt`.
4. Xem nhanh vài câu: câu đầu "IDA: Evening, old street." ở 0:11; câu cuối "Who are the last lamplighters of our time?" ở 9:52. Bấm **Done**.
5. **End screen (tuỳ chọn):** thẻ kết của phim là 6 s cuối (9:56–10:02). Có thể thêm "Subscribe" và "Best for viewer" trong 6 s đó. Đặt ở góc trên để không che chữ thẻ kết (chữ nằm giữa khung).
6. **Cards:** không cần ở tập 1.

## 5. Kiểm và lịch đăng video chính
1. Ở bước **Checks**: chờ kiểm bản quyền (Copyright) xong.
   - Nhạc Kevin MacLeod dùng giấy phép CC BY 4.0 và có ghi công, nên thường không có khiếu nại.
   - Nếu có claim, **đừng xoá nhạc**. Báo P và gửi tranh chấp kèm câu ghi công và link giấy phép.
2. Ở bước **Visibility**:
   - Chọn **Schedule**, đặt ngày giờ phát hành. Gợi ý: thứ Ba–Thứ Năm, 9:00–11:00 sáng giờ New York (ET), vì đối tượng chính nói tiếng Anh.
   - Hoặc chọn **Private** để xem lại lần cuối trên YouTube rồi đổi sau.
3. Bấm **Schedule** (hoặc **Save**). Đây là **cổng G3**: chỉ chủ dự án bấm.
4. Sau khi YouTube xử lý xong bản HD, xem lại trên điện thoại:
   - chapter hiện đúng;
   - phụ đề bật được;
   - thumbnail hiện đúng.

## 6. Ba Shorts: tải lên và lịch đăng
**Cách tải lên mỗi Short:**
1. **Create → Upload videos**, chọn tệp `ll-ep01-short-S*.mp4`. Tệp là 9:16 và dưới 60 s, nên YouTube tự xếp vào Shorts.
2. **Title/Description:** chép từ `ll-ep01-shorts-text.txt`. Mỗi Short có tiêu đề, mô tả có nguồn, ghi công nhạc Kevin MacLeod (bắt buộc) và câu tiết lộ giọng tổng hợp.
3. Thay dòng "Full film: … (link to the main video)" bằng link video chính khi video đã có link. Video đã đặt lịch vẫn có link.
4. **Related video:** chọn video chính "London Still Has 5 Lamplighters…". Short sẽ có nút dẫn sang phim dài.
5. **Audience:** "No, it's not made for kids". **Altered content:** chọn giống video chính.
6. **Phụ đề Short:** không bắt buộc. YouTube tự tạo phụ đề tự động; Short đã có chữ trên hình.
7. **Thumbnail:** Short không dùng thumbnail tải lên. Có thể chọn khung bìa trong app YouTube trên điện thoại.

**Lịch đăng đề xuất** (N = ngày video chính lên):

| Thời điểm | Short | Lý do |
|---|---|---|
| N, cùng giờ hoặc sau 2–3 giờ | **S2 "Which American Jobs Are Shrinking Fastest?"** | Câu hỏi có nhu cầu tìm kiếm cao nhất; đẩy lượt xem về phim ngay ngày đầu |
| N + 2 | **S1 "London Still Has Lamplighters. Five of Them."** | Chi tiết lạ, dễ chia sẻ; trùng tên phim, kéo người xem mới |
| N + 5 | **S3 "One Job in 270"** | Kéo dài vòng đời phim sang tuần đầu |

- Đặt lịch cho Short giống video chính (**Visibility → Schedule**).
- Đừng đăng Short trước video chính, vì nút Related video cần video chính đã công khai mới dẫn sang được.

## 7. Sau khi đăng (P theo dõi khi được giao)
- Ngày 2 và ngày 7: ghi CTR thumbnail, thời lượng xem trung bình, tỷ lệ giữ chân ở 30 s đầu (để đánh giá đoạn móc 6 s), lượt xem đến từ Shorts.
- Kết quả Test & compare: ghi bản thắng vào AUTHORSHIP và chuẩn kênh.
- Nếu K (`checks-appeal.md`) phát hiện lệch số HSUS hoặc BLS sau khi đăng: sửa theo quy trình đính chính (ghim bình luận và sửa mô tả). Chỉ tải lại video nếu số sai nằm trên hình.

## Cần chủ dự án quyết trước G3
1. **Cách lấy master 852,9 MB về máy**, vì Release không tạo được trong loại phiên này:
   - (a) chủ dự án tự tạo Release `ll-ep01-v1` trên github.com, còn P giữ tệp trên máy phiên. Nhưng máy phiên không đẩy tệp ra được, nên cách này chỉ khả thi nếu có đường tải khác;
   - (b) P đẩy master lên một nhánh git riêng bằng Git LFS (cần bật LFS cho repo);
   - (c) dùng bản xem 720p ba phần đã có trong git. **Không nên** dùng cho YouTube vì chất lượng thấp;
   - (d) chủ dự án cấp một đích lưu trữ khác (ví dụ Google Drive).
   - P không tự chọn đường nào khi chưa có quyết định.
2. **Repo `HungQuach301/cine-lab` đang ở chế độ PUBLIC**, không phải private (GitHub API: `"visibility": "public"`).
   - Release tạo trên repo này sẽ công khai; chỉ dạng **draft** mới riêng tư.
   - Các bản xem `screening/*.mp4` (720p cả tập và 3 Short) đã nằm công khai trên nhánh `ccr-a27221d7-0iwsne`.
   - Nếu muốn giữ phim kín tới ngày phát hành: đổi repo sang Private (Settings → General → Danger Zone → Change visibility).
3. Lựa chọn "Altered content" (mục 3): P khuyến nghị **No**.
