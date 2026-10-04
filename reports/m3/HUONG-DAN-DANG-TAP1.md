# Hướng dẫn đăng tập 1 lên YouTube Studio · Last Lamplighters

P soạn ngày 04/10/2026, sau khi chủ dự án duyệt cổng G2. Cổng G3 (bấm phát hành) do chủ dự án làm.
Tên nút ghi theo giao diện YouTube Studio tiếng Anh. YouTube có thể đổi chỗ nút; nếu không thấy đúng chỗ, tìm theo tên.

## 0. Lấy tệp (nhánh `release-ll-ep01-v1`, Git LFS)
- **Nơi lấy:** gói tải lên nằm trên nhánh **`release-ll-ep01-v1`** của repo `HungQuach301/cine-lab` (public). Nhánh chỉ có 9 tệp của gói, `SHA256SUMS.txt` và `.gitattributes`. Commit `4a66386`.
  - Master và 3 Short đi qua **Git LFS**.
  - P đã tải ngược cả 10 tệp từ đúng các link "tải thẳng" bên dưới và chạy `sha256sum -c` vào ngày 04/10/2026: **cả 10 OK**. Vì vậy không cần cắt master thành mảnh.
- GitHub Release không tạo được trong loại phiên này (HTTP 403); nhánh LFS thay cho Release.
- Trang nhánh: https://github.com/HungQuach301/cine-lab/tree/release-ll-ep01-v1

| Tệp | Dùng cho | Link | SHA-256 |
|---|---|---|---|
| `ll-ep01-v1-master-1080p.mp4` | video chính (852,9 MB, LFS) | [trang tệp](https://github.com/HungQuach301/cine-lab/blob/release-ll-ep01-v1/ll-ep01-v1-master-1080p.mp4) · [tải thẳng](https://github.com/HungQuach301/cine-lab/raw/release-ll-ep01-v1/ll-ep01-v1-master-1080p.mp4) | `9c3825387345ec0af6c035ec3f94809644ca7767d1ecbafcaed4710480113942` |
| `ll-ep01-short-S1.mp4` | Short 1 (7,3 MB, LFS) | [trang tệp](https://github.com/HungQuach301/cine-lab/blob/release-ll-ep01-v1/ll-ep01-short-S1.mp4) · [tải thẳng](https://github.com/HungQuach301/cine-lab/raw/release-ll-ep01-v1/ll-ep01-short-S1.mp4) | `b13b66c7442041c218b5c0ec6eb6cf58cefe96a4e6d53e51ce81d35e49c2c0e3` |
| `ll-ep01-short-S2.mp4` | Short 2 (21,9 MB, LFS) | [trang tệp](https://github.com/HungQuach301/cine-lab/blob/release-ll-ep01-v1/ll-ep01-short-S2.mp4) · [tải thẳng](https://github.com/HungQuach301/cine-lab/raw/release-ll-ep01-v1/ll-ep01-short-S2.mp4) | `253bda06c2692525d9080be30f2e2ab0f420e523dc99f459a77d42a7798a0eb6` |
| `ll-ep01-short-S3.mp4` | Short 3 (29,4 MB, LFS) | [trang tệp](https://github.com/HungQuach301/cine-lab/blob/release-ll-ep01-v1/ll-ep01-short-S3.mp4) · [tải thẳng](https://github.com/HungQuach301/cine-lab/raw/release-ll-ep01-v1/ll-ep01-short-S3.mp4) | `233eef545c0878fa4338ae4689fb66c029e0a407b9f13da73e051d760d13f606` |
| `ll-ep01-thumb-T3.jpg` | thumbnail chính | [trang tệp](https://github.com/HungQuach301/cine-lab/blob/release-ll-ep01-v1/ll-ep01-thumb-T3.jpg) · [tải thẳng](https://github.com/HungQuach301/cine-lab/raw/release-ll-ep01-v1/ll-ep01-thumb-T3.jpg) | `e7f5e7a918a90678da83c49054e704c0331bc15ab5862cc73bc157b922a6f24e` |
| `ll-ep01-thumb-T1.jpg` | thumbnail thử A/B | [trang tệp](https://github.com/HungQuach301/cine-lab/blob/release-ll-ep01-v1/ll-ep01-thumb-T1.jpg) · [tải thẳng](https://github.com/HungQuach301/cine-lab/raw/release-ll-ep01-v1/ll-ep01-thumb-T1.jpg) | `323c0d4124a344790859d19f120bed365f449e0d7614989d59072d918ec2a653` |
| `ll-ep01.en.srt` | phụ đề tiếng Anh | [trang tệp](https://github.com/HungQuach301/cine-lab/blob/release-ll-ep01-v1/ll-ep01.en.srt) · [tải thẳng](https://github.com/HungQuach301/cine-lab/raw/release-ll-ep01-v1/ll-ep01.en.srt) | `e737c18c8477e9fc1df0218e77fb119d0744b2e34bdcb8e1bf7446f09c6cf4fb` |
| `ll-ep01-youtube-description.txt` | tiêu đề và mô tả video chính | [trang tệp](https://github.com/HungQuach301/cine-lab/blob/release-ll-ep01-v1/ll-ep01-youtube-description.txt) · [tải thẳng](https://github.com/HungQuach301/cine-lab/raw/release-ll-ep01-v1/ll-ep01-youtube-description.txt) | `59f4ab5c91e513ce2befd6bbc4b321d9704ebcfe36f5cb1526a93aacb9021267` |
| `ll-ep01-shorts-text.txt` | tiêu đề và mô tả 3 Short | [trang tệp](https://github.com/HungQuach301/cine-lab/blob/release-ll-ep01-v1/ll-ep01-shorts-text.txt) · [tải thẳng](https://github.com/HungQuach301/cine-lab/raw/release-ll-ep01-v1/ll-ep01-shorts-text.txt) | `3eaf298203f06e3ad3f3ae45924ed2289f8a6e95c5a353285f353be92ba1b218` |
| `SHA256SUMS.txt` | danh sách SHA-256 của 9 tệp trên | [trang tệp](https://github.com/HungQuach301/cine-lab/blob/release-ll-ep01-v1/SHA256SUMS.txt) · [tải thẳng](https://github.com/HungQuach301/cine-lab/raw/release-ll-ep01-v1/SHA256SUMS.txt) | `—` |

**Cách tải từng tệp:**
- **Tải thẳng (nhanh nhất):** bấm link "tải thẳng", trình duyệt tải ngay. Với tệp LFS, GitHub tự chuyển sang `media.githubusercontent.com`, nên tải được bản gốc chứ không phải tệp con trỏ LFS.
- **Từ trang tệp:** mở link "trang tệp", bấm nút **Download raw file** (biểu tượng mũi tên xuống ↓ ở góc trên phải khung xem tệp, cạnh nút "Copy raw file").
  - Với master 852,9 MB, GitHub báo không xem trước được, nhưng nút Download raw file vẫn có (hoặc bấm liên kết **"View raw"**).
- **Không dùng** nút **Code → Download ZIP** của nhánh. ZIP chỉ chứa tệp con trỏ LFS (~130 byte) thay cho video.
- **Tải cả nhánh bằng dòng lệnh** (cần cài Git LFS):

  ```
  git lfs install
  git clone --branch release-ll-ep01-v1 --single-branch https://github.com/HungQuach301/cine-lab.git ll-ep01-v1
  ```

**Kiểm SHA sau khi tải**, chạy trong thư mục chứa các tệp:
- **macOS** (Terminal): `shasum -a 256 -c SHA256SUMS.txt`. Mọi dòng phải có `OK`.
- **Windows** (PowerShell): `Get-FileHash .\ll-ep01-v1-master-1080p.mp4 -Algorithm SHA256`. Giá trị phải bằng `9C3825387345EC0AF6C035EC3F94809644CA7767D1ECBAFCAED4710480113942` (PowerShell in chữ hoa). Làm tương tự cho từng tệp, đối chiếu cột SHA-256 ở bảng trên.
- **Windows** (cmd): `certutil -hashfile ll-ep01-v1-master-1080p.mp4 SHA256`.
- **Nếu lệch SHA:** tải lại tệp đó; không đăng tệp lệch.

**Lưu ý:**
- Repo để **public** theo quyết định chủ dự án ngày 04/10/2026, nên ai có link cũng tải được gói này trước ngày phát hành.
- GitHub tính băng thông LFS: tài khoản miễn phí có hạn mức tải hằng tháng, mỗi lần tải master tốn ≈ 0,85 GB. Sau khi đăng xong, có thể xoá nhánh này. P không tự xoá.

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
- **Quyết định chủ dự án (04/10/2026, AUTHORSHIP): chọn No.** (P đã đề xuất No.) Minh bạch đã có ở đoạn "How this film was made" trong mô tả.
- Giữ đoạn "How this film was made" trong mô tả, như tiết lộ tự nguyện.
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

## Trạng thái các quyết định trước G3 (cập nhật 04/10/2026)
1. **Cách lấy tệp:** nhánh `release-ll-ep01-v1` qua Git LFS (mục 0). Đã kiểm SHA sau khi đẩy.
2. **Repo giữ PUBLIC:** chủ dự án chấp nhận rủi ro lộ phim trước ngày phát hành.
3. **Altered content: No.** Giữ đoạn "How this film was made".
4. **Còn lại cho G3:** chủ dự án tải tệp, kiểm SHA, làm theo mục 1–6 và bấm Schedule hoặc Publish.
