# Hướng dẫn đăng tập 4 lên YouTube Studio · Last Lamplighters

P soạn ngày 05/10/2026, sau khi chủ dự án duyệt cổng G2. Cổng G3 (bấm phát hành) do chủ dự án làm.
- Làm theo cách của tập 1 (`reports/m3/HUONG-DAN-DANG-TAP1.md`). Các bước giống hệt nhau chỉ ghi tóm tắt; mục nào khác tập 1 có ghi rõ.
- Tên nút theo giao diện YouTube Studio tiếng Anh.

## 0. Lấy tệp (nhánh `release-ll-ep04-v1`, Git LFS)
- **Nơi lấy:** nhánh **`release-ll-ep04-v1`** của repo `HungQuach301/cine-lab` (public), commit `ab9d3bb`.
  - Nhánh chỉ có gói tải lên, `SHA256SUMS.txt` và `.gitattributes`. Master và 3 Short đi qua Git LFS.
  - **Kiểm sau khi đẩy (05/10/2026):** P tải ngược cả **9 tệp** trong `SHA256SUMS.txt` từ link công khai (LFS qua `media.githubusercontent.com`, tệp thường qua `raw.githubusercontent.com`) và chạy `sha256sum -c`: **cả 9 OK**.
- Trang nhánh: https://github.com/HungQuach301/cine-lab/tree/release-ll-ep04-v1

| Tệp | Dùng cho | Link | SHA-256 (đầy đủ trong `SHA256SUMS.txt`) |
|---|---|---|---|
| `ll-ep04-v1-master-1080p.mp4` | video chính (308,7 MB, LFS; 8:34,67) | [trang tệp](https://github.com/HungQuach301/cine-lab/blob/release-ll-ep04-v1/ll-ep04-v1-master-1080p.mp4) · [tải thẳng](https://github.com/HungQuach301/cine-lab/raw/release-ll-ep04-v1/ll-ep04-v1-master-1080p.mp4) | `856971a3b29ecea9…` |
| `ll-ep04-short-S1.mp4` | Short 1 (7,5 MB, LFS; 32,6 s) | [trang tệp](https://github.com/HungQuach301/cine-lab/blob/release-ll-ep04-v1/ll-ep04-short-S1.mp4) · [tải thẳng](https://github.com/HungQuach301/cine-lab/raw/release-ll-ep04-v1/ll-ep04-short-S1.mp4) | `48d0ae9eeebf370d…` |
| `ll-ep04-short-S2.mp4` | Short 2 (6,9 MB, LFS; 26,6 s) | [trang tệp](https://github.com/HungQuach301/cine-lab/blob/release-ll-ep04-v1/ll-ep04-short-S2.mp4) · [tải thẳng](https://github.com/HungQuach301/cine-lab/raw/release-ll-ep04-v1/ll-ep04-short-S2.mp4) | `188053dc04f4339b…` |
| `ll-ep04-short-S3.mp4` | Short 3 (6,4 MB, LFS; 23,7 s) | [trang tệp](https://github.com/HungQuach301/cine-lab/blob/release-ll-ep04-v1/ll-ep04-short-S3.mp4) · [tải thẳng](https://github.com/HungQuach301/cine-lab/raw/release-ll-ep04-v1/ll-ep04-short-S3.mp4) | `f1fd20d185ec37ff…` |
| `ll-ep04-thumb-T1.jpg` | thumbnail chính | [trang tệp](https://github.com/HungQuach301/cine-lab/blob/release-ll-ep04-v1/ll-ep04-thumb-T1.jpg) · [tải thẳng](https://github.com/HungQuach301/cine-lab/raw/release-ll-ep04-v1/ll-ep04-thumb-T1.jpg) | `ce63b99d836100c5…` |
| `ll-ep04-thumb-T2.jpg` | thumbnail thử A/B | [trang tệp](https://github.com/HungQuach301/cine-lab/blob/release-ll-ep04-v1/ll-ep04-thumb-T2.jpg) · [tải thẳng](https://github.com/HungQuach301/cine-lab/raw/release-ll-ep04-v1/ll-ep04-thumb-T2.jpg) | `83454185dac3058e…` |
| `ll-ep04.en.srt` | phụ đề tiếng Anh (195 khối) | [trang tệp](https://github.com/HungQuach301/cine-lab/blob/release-ll-ep04-v1/ll-ep04.en.srt) · [tải thẳng](https://github.com/HungQuach301/cine-lab/raw/release-ll-ep04-v1/ll-ep04.en.srt) | `f9658089fb4df805…` |
| `ll-ep04-youtube-description.txt` | tiêu đề và mô tả video chính | [trang tệp](https://github.com/HungQuach301/cine-lab/blob/release-ll-ep04-v1/ll-ep04-youtube-description.txt) · [tải thẳng](https://github.com/HungQuach301/cine-lab/raw/release-ll-ep04-v1/ll-ep04-youtube-description.txt) | `699f64fe9e749e85…` |
| `ll-ep04-shorts-text.txt` | tiêu đề và mô tả 3 Short | [trang tệp](https://github.com/HungQuach301/cine-lab/blob/release-ll-ep04-v1/ll-ep04-shorts-text.txt) · [tải thẳng](https://github.com/HungQuach301/cine-lab/raw/release-ll-ep04-v1/ll-ep04-shorts-text.txt) | `6045b1458511d5a5…` |
| `*.boxes.json` (2 tệp) | hộp chữ thumbnail cho qc Q12; **không tải lên YouTube** | trên nhánh | trong `SHA256SUMS.txt` |

**Cách tải và kiểm:** như tập 1, mục 0.
- Bấm "tải thẳng"; không dùng Code → Download ZIP (ZIP chỉ chứa tệp con trỏ LFS).
- Hoặc dùng dòng lệnh: `git lfs install && git clone --branch release-ll-ep04-v1 --single-branch https://github.com/HungQuach301/cine-lab.git ll-ep04-v1`.
- **Kiểm SHA:**
  - macOS: `shasum -a 256 -c SHA256SUMS.txt`, mọi dòng phải `OK`.
  - Windows (PowerShell): `Get-FileHash .\ll-ep04-v1-master-1080p.mp4 -Algorithm SHA256` phải bằng `856971A3B29ECEA9CA5EBB52827BFAE36E792F7428A8835249DFD8129D5255BE`.
- Lệch SHA thì tải lại; không đăng tệp lệch.
- Repo public: ai có link cũng tải được gói trước ngày phát hành (đã chấp nhận ở tập 1). Mỗi lần tải master tốn ≈ 0,5 GB băng thông LFS. P không tự xoá nhánh.

## 1. Tải video chính lên
**Create → Upload videos**, chọn `ll-ep04-v1-master-1080p.mp4`. Điền mục 2 trong lúc tải. Đừng bấm Publish.

## 2. Details
1. **Title** (chủ dự án đặt ở G1, 74 ký tự): `The Typewriter Opened a Door for Millions of Women. Who Gets the Next One?`
2. **Description:** chép toàn bộ phần sau dòng `DESCRIPTION` của `ll-ep04-youtube-description.txt`. Gồm:
   - 14 chapter từ `0:00`, mốc lấy từ timeline thật;
   - Sources (6 nguồn, không Wikipedia);
   - câu "Projections are forecasts…";
   - **ghi công nhạc Kevin MacLeod CC BY 4.0: bắt buộc, không sửa**;
   - đoạn "How this film was made".
3. **Thumbnail: Test & compare.** Phương án 1 là **T1** (`ll-ep04-thumb-T1.jpg`, bản chính), phương án 2 là **T2** (`ll-ep04-thumb-T2.jpg`).
   - Cả hai kiểm lề an toàn ≥ 5 % mỗi cạnh (qc Q12 ĐẠT); số trên T2 truy được về nguồn, có nhãn "BLS PROJECTION" (qc Q13 ĐẠT).
   - Nếu không có Test & compare: tải T1 trước, thêm A/B sau (như tập 1, mục 2.4).
4. **Playlist:** "Last Lamplighters" (cùng playlist với tập 1).
5. **Audience:** "No, it's not made for kids"; Age restriction: không giới hạn.
6. **Show more:**
   - Paid promotion: không.
   - Altered content: mục 3.
   - Automatic chapters: bật.
   - **Tags (tuỳ chọn):** `typing pool, typists, secretaries, stenographers, women at work, office automation, AI and writing, BLS projections, history of work, animation`
   - Video language = English; caption certification "never aired on television in the U.S."
   - License: Standard; embedding bật; Category **Education**; Comments On, giữ bình luận có thể không phù hợp để duyệt.

## 3. Altered content: **No** (chủ dự án quyết 05/10/2026, AUTHORSHIP)
- **Đối chiếu tập 4:**
  - hoạt hình phong cách hoá 2.5D, không có cảnh quay thật;
  - phố Ostler và người thắp đèn vô danh là hư cấu;
  - người thật chỉ được nêu tên khi dẫn nguồn (các nhà kinh tế), không có hình hay giọng của họ;
  - giọng kể là giọng thư viện ElevenLabs;
  - nhạc của Kevin MacLeod.
- Phòng đánh máy, màn hình "WORD PROCESSOR" và người đánh máy ở thumbnail T1 là hình cách điệu, không phải cảnh quay thật. Tập này không dùng ảnh tư liệu.
- Giữ đoạn "How this film was made". **Kiểm lại trang chính sách YouTube ngay trước khi bấm Publish.**

## 4. Phụ đề
- **Video elements → Add subtitles → Upload file → With timing**, chọn `ll-ep04.en.srt`.
- 189 khối phụ đề. Câu đầu "What happened to the typing pool?" ở 0:00,6. Câu cuối "…millions still keep an office running." ở 8:30.
- Tập này không có thoại nhân vật, chỉ lời dẫn.
- **End screen (tuỳ chọn):** thẻ kết là 4,7 s cuối (8:30,0–8:34,7). Thêm "Subscribe" và video tập 3 ("Best for viewer" hoặc chọn thẳng tập 1). Đặt ở góc trên để không che chữ thẻ kết.

## 5. Kiểm và lịch đăng
- **Checks:** chờ kiểm bản quyền.
  - Nhạc "Immersed" và "Reawakening" dùng giấy phép CC BY 4.0, có ghi công.
  - Nếu có claim: không xoá nhạc; báo P và tranh chấp kèm câu ghi công.
- **Visibility → Schedule.** Gợi ý giữ nhịp với tập 1: thứ Ba–Thứ Năm, 9:00–11:00 sáng giờ New York (ET).
- **Đây là cổng G3: chỉ chủ dự án bấm.**
- Sau khi YouTube xử lý bản HD, xem lại trên điện thoại: chapter, phụ đề, thumbnail.

## 6. Ba Shorts
- Cách tải như tập 1 (mục 6): tệp 9:16, dưới 60 s, YouTube tự xếp vào Shorts.
- Title và mô tả chép từ `ll-ep04-shorts-text.txt`. Ghi công nhạc giữ nguyên.
- Thay "Full film … on the channel" bằng link video chính.
- **Related video:** chọn video chính. **Altered content:** No, như video chính.

| Thời điểm (N = ngày video chính lên) | Short | Lý do |
|---|---|---|
| N, sau 2–3 giờ | **S1 "Stenographers, typists & secretaries: 134,000 to 3.9 million"** | câu chuyện lịch sử chính của phim |
| N + 2 | **S2 "The job AI names directly: medical transcription"** | BLS nêu thẳng AI là lý do; có nhãn dự báo |
| N + 5 | **S3 "37% faster with AI — but not typists"** | góc AI và viết, kéo dài vòng đời phim |

- Không đăng Short trước video chính.

## 7. Sau khi đăng (P theo dõi khi được giao)
- **Ngày 2 và ngày 7:** ghi CTR (T1/T2), thời lượng xem trung bình, giữ chân 30 s đầu, lượt xem từ Shorts. So với tập 1.
- **Kết quả Test & compare:** ghi bản thắng vào AUTHORSHIP.
- Nếu BLS cập nhật số OOH trước ngày đăng: báo chủ dự án. Đính chính bằng bình luận ghim và mô tả; chỉ dựng lại nếu số sai nằm trên hình.

## Trạng thái trước G3 (05/10/2026)
1. **Bản cuối và Shorts:** chủ dự án duyệt nguyên trạng ở G2. Sai lệch đã chấp nhận ghi trong AUTHORSHIP.
2. **Tệp:** nhánh `release-ll-ep04-v1` (Git LFS), commit `ab9d3bb`, tải ngược 9/9 SHA OK.
3. **Thumbnail:** T1 chính, A/B T2.
4. **Altered content: No.** Giữ "How this film was made".
5. **Còn lại cho G3:** chủ dự án tải tệp, kiểm SHA, làm theo mục 1–6, bấm Schedule hoặc Publish.
