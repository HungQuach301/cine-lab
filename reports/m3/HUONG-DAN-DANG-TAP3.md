# Hướng dẫn đăng tập 3 lên YouTube Studio · Last Lamplighters

P soạn ngày 05/10/2026, sau khi chủ dự án duyệt cổng G2. Cổng G3 (bấm phát hành) do chủ dự án làm.
- Làm theo cách của tập 1 (`reports/m3/HUONG-DAN-DANG-TAP1.md`). Các bước giống hệt nhau chỉ ghi tóm tắt; mục nào khác tập 1 có ghi rõ.
- Tên nút theo giao diện YouTube Studio tiếng Anh.

## 0. Lấy tệp (nhánh `release-ll-ep03-v1`, Git LFS)
- **Nơi lấy:** nhánh **`release-ll-ep03-v1`** của repo `HungQuach301/cine-lab` (public), commit `a26b828`.
  - Nhánh chỉ có gói tải lên, `SHA256SUMS.txt` và `.gitattributes`. Master và 3 Short đi qua Git LFS.
  - **Kiểm sau khi đẩy (05/10/2026):** P tải ngược cả **9 tệp** trong `SHA256SUMS.txt` từ link công khai (LFS qua `media.githubusercontent.com`, tệp thường qua `raw.githubusercontent.com`) và chạy `sha256sum -c`: **cả 9 OK**.
- Trang nhánh: https://github.com/HungQuach301/cine-lab/tree/release-ll-ep03-v1

| Tệp | Dùng cho | Link | SHA-256 (đầy đủ trong `SHA256SUMS.txt`) |
|---|---|---|---|
| `ll-ep03-v1-master-1080p.mp4` | video chính (477,6 MB, LFS; 9:04,50) | [trang tệp](https://github.com/HungQuach301/cine-lab/blob/release-ll-ep03-v1/ll-ep03-v1-master-1080p.mp4) · [tải thẳng](https://github.com/HungQuach301/cine-lab/raw/release-ll-ep03-v1/ll-ep03-v1-master-1080p.mp4) | `7ba5d66da42ae01b…` |
| `ll-ep03-short-S1.mp4` | Short 1 (20,4 MB, LFS; 33,4 s) | [trang tệp](https://github.com/HungQuach301/cine-lab/blob/release-ll-ep03-v1/ll-ep03-short-S1.mp4) · [tải thẳng](https://github.com/HungQuach301/cine-lab/raw/release-ll-ep03-v1/ll-ep03-short-S1.mp4) | `7623775e74525667…` |
| `ll-ep03-short-S2.mp4` | Short 2 (17,6 MB, LFS; 27,5 s) | [trang tệp](https://github.com/HungQuach301/cine-lab/blob/release-ll-ep03-v1/ll-ep03-short-S2.mp4) · [tải thẳng](https://github.com/HungQuach301/cine-lab/raw/release-ll-ep03-v1/ll-ep03-short-S2.mp4) | `27fc020e56f01e2c…` |
| `ll-ep03-short-S3.mp4` | Short 3 (19,7 MB, LFS; 29,0 s) | [trang tệp](https://github.com/HungQuach301/cine-lab/blob/release-ll-ep03-v1/ll-ep03-short-S3.mp4) · [tải thẳng](https://github.com/HungQuach301/cine-lab/raw/release-ll-ep03-v1/ll-ep03-short-S3.mp4) | `c638c7409ecb79c5…` |
| `ll-ep03-thumb-T1.jpg` | thumbnail chính | [trang tệp](https://github.com/HungQuach301/cine-lab/blob/release-ll-ep03-v1/ll-ep03-thumb-T1.jpg) · [tải thẳng](https://github.com/HungQuach301/cine-lab/raw/release-ll-ep03-v1/ll-ep03-thumb-T1.jpg) | `5d3d62dcc1fac8e1…` |
| `ll-ep03-thumb-T2.jpg` | thumbnail thử A/B | [trang tệp](https://github.com/HungQuach301/cine-lab/blob/release-ll-ep03-v1/ll-ep03-thumb-T2.jpg) · [tải thẳng](https://github.com/HungQuach301/cine-lab/raw/release-ll-ep03-v1/ll-ep03-thumb-T2.jpg) | `66c10dcb46d05d36…` |
| `ll-ep03.en.srt` | phụ đề tiếng Anh (195 khối) | [trang tệp](https://github.com/HungQuach301/cine-lab/blob/release-ll-ep03-v1/ll-ep03.en.srt) · [tải thẳng](https://github.com/HungQuach301/cine-lab/raw/release-ll-ep03-v1/ll-ep03.en.srt) | `d6650182a2ab377d…` |
| `ll-ep03-youtube-description.txt` | tiêu đề và mô tả video chính | [trang tệp](https://github.com/HungQuach301/cine-lab/blob/release-ll-ep03-v1/ll-ep03-youtube-description.txt) · [tải thẳng](https://github.com/HungQuach301/cine-lab/raw/release-ll-ep03-v1/ll-ep03-youtube-description.txt) | `45ac6ab322bba13b…` |
| `ll-ep03-shorts-text.txt` | tiêu đề và mô tả 3 Short | [trang tệp](https://github.com/HungQuach301/cine-lab/blob/release-ll-ep03-v1/ll-ep03-shorts-text.txt) · [tải thẳng](https://github.com/HungQuach301/cine-lab/raw/release-ll-ep03-v1/ll-ep03-shorts-text.txt) | `5333c071b98c2cd4…` |
| `*.boxes.json` (2 tệp) | hộp chữ thumbnail cho qc Q12; **không tải lên YouTube** | trên nhánh | trong `SHA256SUMS.txt` |

**Cách tải và kiểm:** như tập 1, mục 0.
- Bấm "tải thẳng"; không dùng Code → Download ZIP (ZIP chỉ chứa tệp con trỏ LFS).
- Hoặc dùng dòng lệnh: `git lfs install && git clone --branch release-ll-ep03-v1 --single-branch https://github.com/HungQuach301/cine-lab.git ll-ep03-v1`.
- **Kiểm SHA:**
  - macOS: `shasum -a 256 -c SHA256SUMS.txt`, mọi dòng phải `OK`.
  - Windows (PowerShell): `Get-FileHash .\ll-ep03-v1-master-1080p.mp4 -Algorithm SHA256` phải bằng `7BA5D66DA42AE01B63006D04F5B6D510DA2C39C6126BAD1FBAA6032215CEEB92`.
- Lệch SHA thì tải lại; không đăng tệp lệch.
- Repo public: ai có link cũng tải được gói trước ngày phát hành (đã chấp nhận ở tập 1). Mỗi lần tải master tốn ≈ 0,5 GB băng thông LFS. P không tự xoá nhánh.

## 1. Tải video chính lên
**Create → Upload videos**, chọn `ll-ep03-v1-master-1080p.mp4`. Điền mục 2 trong lúc tải. Đừng bấm Publish.

## 2. Details
1. **Title** (chủ dự án đặt ở G1, 45 ký tự): `The ATM Didn't Kill the Bank Teller. Will AI?`
2. **Description:** chép toàn bộ phần sau dòng `DESCRIPTION` của `ll-ep03-youtube-description.txt`. Gồm:
   - 15 chapter từ `0:00`, mốc lấy từ timeline thật;
   - Sources (6 nguồn, không Wikipedia);
   - câu ghi rõ đoạn "A banker's view" là góc nhìn của tác giả kênh, không phải số liệu;
   - câu "Projections are forecasts…";
   - **ghi công nhạc Kevin MacLeod CC BY 4.0: bắt buộc, không sửa**;
   - đoạn "How this film was made".
3. **Thumbnail: Test & compare.** Phương án 1 là **T1** (`ll-ep03-thumb-T1.jpg`, bản chính), phương án 2 là **T2** (`ll-ep03-thumb-T2.jpg`).
   - Cả hai kiểm lề an toàn ≥ 5 % mỗi cạnh (qc Q12 ĐẠT); số trên T2 truy được về nguồn, có nhãn "BLS PROJECTION" (qc Q13 ĐẠT).
   - Nếu không có Test & compare: tải T1 trước, thêm A/B sau (như tập 1, mục 2.4).
4. **Playlist:** "Last Lamplighters" (cùng playlist với tập 1).
5. **Audience:** "No, it's not made for kids"; Age restriction: không giới hạn.
6. **Show more:**
   - Paid promotion: không.
   - Altered content: mục 3.
   - Automatic chapters: bật.
   - **Tags (tuỳ chọn):** `bank tellers, ATM, banking jobs, loan officers, credit analysts, automation, AI and jobs, BLS projections, history of work, animation`
   - Video language = English; caption certification "never aired on television in the U.S."
   - License: Standard; embedding bật; Category **Education**; Comments On, giữ bình luận có thể không phù hợp để duyệt.

## 3. Altered content: **No** (chủ dự án quyết 05/10/2026, AUTHORSHIP)
- **Đối chiếu tập 3:**
  - hoạt hình phong cách hoá 2.5D, không có cảnh quay thật;
  - phố Ostler và người thắp đèn vô danh là hư cấu;
  - người thật chỉ được nêu tên khi dẫn nguồn (các nhà kinh tế), không có hình hay giọng của họ;
  - giọng kể là giọng thư viện ElevenLabs;
  - nhạc của Kevin MacLeod.
- Màn hình "ATM" và cảnh quầy giao dịch là hình cách điệu, không phải cảnh quay hay ngân hàng có thật.
- Giữ đoạn "How this film was made". **Kiểm lại trang chính sách YouTube ngay trước khi bấm Publish.**

## 4. Phụ đề
- **Video elements → Add subtitles → Upload file → With timing**, chọn `ll-ep03.en.srt`.
- 195 khối phụ đề. Câu đầu "At dusk, the lamplighter starts the round." ở 0:10. Câu cuối "…and many still do." ở 8:51.
- Tập này không có thoại nhân vật, chỉ lời dẫn.
- **End screen (tuỳ chọn):** thẻ kết là 13,3 s cuối (8:51,2–9:04,5). Thêm "Subscribe" và video tập 2 ("Best for viewer" hoặc chọn thẳng tập 1). Đặt ở góc trên để không che chữ thẻ kết.

## 5. Kiểm và lịch đăng
- **Checks:** chờ kiểm bản quyền.
  - Nhạc "Immersed" và "Reawakening" dùng giấy phép CC BY 4.0, có ghi công.
  - Nếu có claim: không xoá nhạc; báo P và tranh chấp kèm câu ghi công.
- **Visibility → Schedule.** Gợi ý giữ nhịp với tập 1: thứ Ba–Thứ Năm, 9:00–11:00 sáng giờ New York (ET).
- **Đây là cổng G3: chỉ chủ dự án bấm.**
- Sau khi YouTube xử lý bản HD, xem lại trên điện thoại: chapter, phụ đề, thumbnail.

## 6. Ba Shorts
- Cách tải như tập 1 (mục 6): tệp 9:16, dưới 60 s, YouTube tự xếp vào Shorts.
- Title và mô tả chép từ `ll-ep03-shorts-text.txt`. Ghi công nhạc giữ nguyên.
- Thay "Full film … on the channel" bằng link video chính.
- **Related video:** chọn video chính. **Altered content:** No, như video chính.

| Thời điểm (N = ngày video chính lên) | Short | Lý do |
|---|---|---|
| N, sau 2–3 giờ | **S1 "The ATM didn't kill the bank teller"** | ý chính của phim, trùng tiêu đề |
| N + 2 | **S2 "Bank tellers: 13% fewer by 2035?"** | câu hỏi có nhu cầu tìm kiếm; nhãn "a projection, not a count" trên hình |
| N + 5 | **S3 "AI and the essence of a credit rating"** | góc AI trong tín dụng, kéo dài vòng đời phim |

- Không đăng Short trước video chính.

## 7. Sau khi đăng (P theo dõi khi được giao)
- **Ngày 2 và ngày 7:** ghi CTR (T1/T2), thời lượng xem trung bình, giữ chân 30 s đầu, lượt xem từ Shorts. So với tập 1.
- **Kết quả Test & compare:** ghi bản thắng vào AUTHORSHIP.
- Nếu BLS cập nhật số OOH trước ngày đăng: báo chủ dự án. Đính chính bằng bình luận ghim và mô tả; chỉ dựng lại nếu số sai nằm trên hình.

## Trạng thái trước G3 (05/10/2026)
1. **Bản cuối và Shorts:** chủ dự án duyệt nguyên trạng ở G2. Sai lệch đã chấp nhận ghi trong AUTHORSHIP.
2. **Tệp:** nhánh `release-ll-ep03-v1` (Git LFS), commit `a26b828` (master mới sau sửa biểu đồ HSUS), tải ngược 9/9 SHA OK.
3. **Thumbnail:** T1 chính, A/B T2.
4. **Altered content: No.** Giữ "How this film was made".
5. **Còn lại cho G3:** chủ dự án tải tệp, kiểm SHA, làm theo mục 1–6, bấm Schedule hoặc Publish.
