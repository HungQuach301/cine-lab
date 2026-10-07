# Hướng dẫn đăng tập 2 lên YouTube Studio · Last Lamplighters

P soạn ngày 05/10/2026, sau khi chủ dự án duyệt cổng G2. Cổng G3 (bấm phát hành) do chủ dự án làm.
- Làm theo cách của tập 1 (`reports/m3/HUONG-DAN-DANG-TAP1.md`). Các bước giống hệt nhau chỉ ghi tóm tắt; mục nào khác tập 1 có ghi rõ.
- Tên nút theo giao diện YouTube Studio tiếng Anh.

## 0. Lấy tệp (nhánh `release-ll-ep02-v1`, Git LFS)
- **Nơi lấy:** nhánh **`release-ll-ep02-v1`** của repo `HungQuach301/cine-lab` (public), commit `0334728`.
  - Nhánh chỉ có gói tải lên, `SHA256SUMS.txt` và `.gitattributes`. Master và 3 Short đi qua Git LFS.
  - **Kiểm sau khi đẩy (05/10/2026):** P tải ngược cả **11 tệp** từ các link công khai bên dưới (LFS qua `media.githubusercontent.com`) và chạy `sha256sum -c`: **cả 11 OK**.
- Trang nhánh: https://github.com/HungQuach301/cine-lab/tree/release-ll-ep02-v1

| Tệp | Dùng cho | Link | SHA-256 (đầy đủ trong `SHA256SUMS.txt`) |
|---|---|---|---|
| `ll-ep02-v1-master-1080p.mp4` | video chính (493,9 MB, LFS; 9:01,38) | [trang tệp](https://github.com/HungQuach301/cine-lab/blob/release-ll-ep02-v1/ll-ep02-v1-master-1080p.mp4) · [tải thẳng](https://github.com/HungQuach301/cine-lab/raw/release-ll-ep02-v1/ll-ep02-v1-master-1080p.mp4) | `8b3c0be618dd291e…` |
| `ll-ep02-short-S1.mp4` | Short 1 (21,0 MB, LFS; 40,3 s) | [trang tệp](https://github.com/HungQuach301/cine-lab/blob/release-ll-ep02-v1/ll-ep02-short-S1.mp4) · [tải thẳng](https://github.com/HungQuach301/cine-lab/raw/release-ll-ep02-v1/ll-ep02-short-S1.mp4) | `d3521bbf8969f6f7…` |
| `ll-ep02-short-S2.mp4` | Short 2 (18,3 MB, LFS; 30,7 s) | [trang tệp](https://github.com/HungQuach301/cine-lab/blob/release-ll-ep02-v1/ll-ep02-short-S2.mp4) · [tải thẳng](https://github.com/HungQuach301/cine-lab/raw/release-ll-ep02-v1/ll-ep02-short-S2.mp4) | `7e4400eb3607bcce…` |
| `ll-ep02-short-S3.mp4` | Short 3 (13,3 MB, LFS; 27,9 s) | [trang tệp](https://github.com/HungQuach301/cine-lab/blob/release-ll-ep02-v1/ll-ep02-short-S3.mp4) · [tải thẳng](https://github.com/HungQuach301/cine-lab/raw/release-ll-ep02-v1/ll-ep02-short-S3.mp4) | `11d8b3282ef71f45…` |
| `ll-ep02-thumb-T1.jpg` | thumbnail chính | [trang tệp](https://github.com/HungQuach301/cine-lab/blob/release-ll-ep02-v1/ll-ep02-thumb-T1.jpg) · [tải thẳng](https://github.com/HungQuach301/cine-lab/raw/release-ll-ep02-v1/ll-ep02-thumb-T1.jpg) | `ea01a8cf21a38b27…` |
| `ll-ep02-thumb-T2.jpg` | thumbnail thử A/B | [trang tệp](https://github.com/HungQuach301/cine-lab/blob/release-ll-ep02-v1/ll-ep02-thumb-T2.jpg) · [tải thẳng](https://github.com/HungQuach301/cine-lab/raw/release-ll-ep02-v1/ll-ep02-thumb-T2.jpg) | `2e7b9e2c6fe83813…` |
| `ll-ep02.en.srt` | phụ đề tiếng Anh (195 khối) | [trang tệp](https://github.com/HungQuach301/cine-lab/blob/release-ll-ep02-v1/ll-ep02.en.srt) · [tải thẳng](https://github.com/HungQuach301/cine-lab/raw/release-ll-ep02-v1/ll-ep02.en.srt) | `d8d9b016c8e12666…` |
| `ll-ep02-youtube-description.txt` | tiêu đề và mô tả video chính | [trang tệp](https://github.com/HungQuach301/cine-lab/blob/release-ll-ep02-v1/ll-ep02-youtube-description.txt) · [tải thẳng](https://github.com/HungQuach301/cine-lab/raw/release-ll-ep02-v1/ll-ep02-youtube-description.txt) | `5c015750e61e4b92…` |
| `ll-ep02-shorts-text.txt` | tiêu đề và mô tả 3 Short | [trang tệp](https://github.com/HungQuach301/cine-lab/blob/release-ll-ep02-v1/ll-ep02-shorts-text.txt) · [tải thẳng](https://github.com/HungQuach301/cine-lab/raw/release-ll-ep02-v1/ll-ep02-shorts-text.txt) | `ed071db7c9073e90…` |
| `*.boxes.json` (2 tệp) | hộp chữ thumbnail cho qc Q12; **không tải lên YouTube** | trên nhánh | trong `SHA256SUMS.txt` |

**Cách tải và kiểm:** như tập 1, mục 0.
- Bấm "tải thẳng"; không dùng Code → Download ZIP (ZIP chỉ chứa tệp con trỏ LFS).
- Hoặc dùng dòng lệnh: `git lfs install && git clone --branch release-ll-ep02-v1 --single-branch https://github.com/HungQuach301/cine-lab.git ll-ep02-v1`.
- **Kiểm SHA:**
  - macOS: `shasum -a 256 -c SHA256SUMS.txt`, mọi dòng phải `OK`.
  - Windows (PowerShell): `Get-FileHash .\ll-ep02-v1-master-1080p.mp4 -Algorithm SHA256` phải bằng `8B3C0BE618DD291EB2692472EFEA9DF8109F9CBA66353034E55CC4B1B94383C9`.
- Lệch SHA thì tải lại; không đăng tệp lệch.
- Repo public: ai có link cũng tải được gói trước ngày phát hành (đã chấp nhận ở tập 1). Mỗi lần tải master tốn ≈ 0,5 GB băng thông LFS. P không tự xoá nhánh.

## 1. Tải video chính lên
**Create → Upload videos**, chọn `ll-ep02-v1-master-1080p.mp4`. Điền mục 2 trong lúc tải. Đừng bấm Publish.

## 2. Details
1. **Title** (chủ dự án đặt ở G1, 76 ký tự, dưới giới hạn 100): `Automation Hurt the Phone Operators. Not the Next Generation. What About Us?`
2. **Description:** chép toàn bộ phần sau dòng `DESCRIPTION` của `ll-ep02-youtube-description.txt`. Gồm:
   - 16 chapter từ `0:00`, mốc lấy từ timeline thật;
   - Sources (6 nguồn, không Wikipedia);
   - câu "Projections are forecasts…";
   - **ghi công nhạc Kevin MacLeod CC BY 4.0: bắt buộc, không sửa**;
   - đoạn "How this film was made".
3. **Thumbnail: Test & compare.** Phương án 1 là **T1** (`ll-ep02-thumb-T1.jpg`, bản chính), phương án 2 là **T2** (`ll-ep02-thumb-T2.jpg`).
   - Cả hai đã sửa và kiểm lề an toàn ≥ 5 % mỗi cạnh (qc Q12 ĐẠT). Chữ "OPERATORS" không còn bị cắt.
   - Nếu không có Test & compare: tải T1 trước, thêm A/B sau (như tập 1, mục 2.4).
4. **Playlist:** "Last Lamplighters" (cùng playlist với tập 1).
5. **Audience:** "No, it's not made for kids"; Age restriction: không giới hạn.
6. **Show more:**
   - Paid promotion: không.
   - Altered content: mục 3.
   - Automatic chapters: bật.
   - **Tags (tuỳ chọn):** `telephone operators, switchboard, customer service, automation, AI and jobs, BLS projections, history of work, future of work, animation`
   - Video language = English; caption certification "never aired on television in the U.S."
   - License: Standard; embedding bật; Category **Education**; Comments On, giữ bình luận có thể không phù hợp để duyệt.

## 3. Altered content: **No** (chủ dự án quyết 05/10/2026, AUTHORSHIP)
- **Đối chiếu tập 2:**
  - hoạt hình phong cách hoá 2.5D, không có cảnh quay thật;
  - phố Ostler và người thắp đèn vô danh là hư cấu;
  - người thật chỉ được nêu tên khi dẫn nguồn (các nhà kinh tế), không có hình hay giọng của họ;
  - giọng kể là giọng thư viện ElevenLabs;
  - nhạc của Kevin MacLeod.
- Màn hình "AUTOMATED VOICE" trong cảnh truyện là hình cách điệu có dán nhãn, không phải giọng giả người thật.
- Giữ đoạn "How this film was made". **Kiểm lại trang chính sách YouTube ngay trước khi bấm Publish.**

## 4. Phụ đề
- **Video elements → Add subtitles → Upload file → With timing**, chọn `ll-ep02.en.srt`.
- Câu đầu "At dusk, the last lamp on the street still…" ở 0:10. Câu cuối "Some of them answer the phone." ở 8:50.
- Tập này không có thoại nhân vật, chỉ lời dẫn.
- **End screen (tuỳ chọn):** thẻ kết là 8,6 s cuối (8:52,8–9:01,4). Thêm "Subscribe" và video tập 1 ("Best for viewer" hoặc chọn thẳng tập 1). Đặt ở góc trên để không che chữ thẻ kết.

## 5. Kiểm và lịch đăng
- **Checks:** chờ kiểm bản quyền.
  - Nhạc "Immersed" và "Reawakening" dùng giấy phép CC BY 4.0, có ghi công.
  - Nếu có claim: không xoá nhạc; báo P và tranh chấp kèm câu ghi công.
- **Visibility → Schedule.** Gợi ý giữ nhịp với tập 1: thứ Ba–Thứ Năm, 9:00–11:00 sáng giờ New York (ET).
- **Đây là cổng G3: chỉ chủ dự án bấm.**
- Sau khi YouTube xử lý bản HD, xem lại trên điện thoại: chapter, phụ đề, thumbnail.

## 6. Ba Shorts
- Cách tải như tập 1 (mục 6): tệp 9:16, dưới 60 s, YouTube tự xếp vào Shorts.
- Title và mô tả chép từ `ll-ep02-shorts-text.txt`. Ghi công nhạc giữ nguyên.
- Thay "Full film … on the channel" bằng link video chính.
- **Related video:** chọn video chính. **Altered content:** No, như video chính.

| Thời điểm (N = ngày video chính lên) | Short | Lý do |
|---|---|---|
| N, sau 2–3 giờ | **S2 "How many U.S. customer service jobs could disappear?"** | câu hỏi có nhu cầu tìm kiếm cao; số BLS có nhãn "a projection, not a count" trên hình |
| N + 2 | **S1 "Automation hurt the operators — not the next generation"** | ý chính của phim, trùng tiêu đề |
| N + 5 | **S3 "The night the switchboard went quiet"** | chuyện lịch sử, kéo dài vòng đời phim |

- Không đăng Short trước video chính.

## 7. Sau khi đăng (P theo dõi khi được giao)
- **Ngày 2 và ngày 7:** ghi CTR (T1/T2), thời lượng xem trung bình, giữ chân 30 s đầu, lượt xem từ Shorts. So với tập 1.
- **Kết quả Test & compare:** ghi bản thắng vào AUTHORSHIP.
- Nếu BLS cập nhật số OOH hoặc Canaries ra bản mới trước ngày đăng: báo chủ dự án. Đính chính bằng bình luận ghim và mô tả; chỉ dựng lại nếu số sai nằm trên hình.

## Trạng thái trước G3 (05/10/2026)
1. **Bản cuối và Shorts:** chủ dự án duyệt nguyên trạng ở G2. Sai lệch đã chấp nhận ghi trong AUTHORSHIP.
2. **Tệp:** nhánh `release-ll-ep02-v1` (Git LFS), tải ngược 11/11 SHA OK.
3. **Thumbnail:** T1 chính, A/B T2; đã sửa lề.
4. **Altered content: No.** Giữ "How this film was made".
5. **Còn lại cho G3:** chủ dự án tải tệp, kiểm SHA, làm theo mục 1–6, bấm Schedule hoặc Publish.
