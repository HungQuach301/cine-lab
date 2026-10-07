# Hướng dẫn đăng tập 6 lên YouTube Studio · Last Lamplighters

P soạn ngày 07/10/2026, sau khi Claude kiểm bản sửa tập 6 v2: ĐẠT. Cổng G3 (bấm phát hành) do chủ dự án làm.
- Làm theo cách của tập 1 (`reports/m3/HUONG-DAN-DANG-TAP1.md`) và tập 5 (`HUONG-DAN-DANG-TAP5.md`). Các bước giống hệt nhau chỉ ghi tóm tắt; mục nào khác có ghi rõ.
- Tên nút theo giao diện YouTube Studio tiếng Anh.
- **Bản v1 không phát hành.** Nhánh `release-ll-ep06-v1` chỉ giữ làm đối chiếu; đừng đăng tệp ở đó.

## 0. Lấy tệp (nhánh `release-ll-ep06-v2`, Git LFS)
- **Nơi lấy:** nhánh **`release-ll-ep06-v2`** của repo `HungQuach301/cine-lab` (public), commit **`ac607c9`**.
  - Nhánh chỉ có gói tải lên, `SHA256SUMS.txt` và `.gitattributes`. Master và 3 Short đi qua Git LFS.
  - Commit `ac607c9` sửa dòng ghi công nhạc trong chữ Shorts. Bản trước ghi nhầm "Immersed"; Shorts v2 chỉ dùng "Reawakening".
  - **Kiểm sau khi đẩy (07/10/2026):** P tải ngược cả **11 tệp** trong `SHA256SUMS.txt` từ link công khai (LFS qua `media.githubusercontent.com`, tệp thường qua `raw.githubusercontent.com`) và chạy `sha256sum -c`: **cả 11 OK**.
- Trang nhánh: https://github.com/HungQuach301/cine-lab/tree/release-ll-ep06-v2

| Tệp | Dùng cho | Link | SHA-256 (đầy đủ trong `SHA256SUMS.txt`) |
|---|---|---|---|
| `ll-ep06-v2-master-1080p.mp4` | video chính (588,1 MB, LFS; 8:36,75) | [trang tệp](https://github.com/HungQuach301/cine-lab/blob/release-ll-ep06-v2/ll-ep06-v2-master-1080p.mp4) · [tải thẳng](https://github.com/HungQuach301/cine-lab/raw/release-ll-ep06-v2/ll-ep06-v2-master-1080p.mp4) | `ddabaec5a6e1f975…` |
| `ll-ep06-short-S1.mp4` | Short 1 (23,6 MB, LFS; 25,5 s) | [trang tệp](https://github.com/HungQuach301/cine-lab/blob/release-ll-ep06-v2/ll-ep06-short-S1.mp4) · [tải thẳng](https://github.com/HungQuach301/cine-lab/raw/release-ll-ep06-v2/ll-ep06-short-S1.mp4) | `c3c403f370d7f459…` |
| `ll-ep06-short-S2.mp4` | Short 2 (5,5 MB, LFS; 21,8 s) | [trang tệp](https://github.com/HungQuach301/cine-lab/blob/release-ll-ep06-v2/ll-ep06-short-S2.mp4) · [tải thẳng](https://github.com/HungQuach301/cine-lab/raw/release-ll-ep06-v2/ll-ep06-short-S2.mp4) | `56223d3381d47a03…` |
| `ll-ep06-short-S3.mp4` | Short 3 (21,6 MB, LFS; 25,2 s) | [trang tệp](https://github.com/HungQuach301/cine-lab/blob/release-ll-ep06-v2/ll-ep06-short-S3.mp4) · [tải thẳng](https://github.com/HungQuach301/cine-lab/raw/release-ll-ep06-v2/ll-ep06-short-S3.mp4) | `906874078ec71bd3…` |
| `ll-ep06-thumb-T1.jpg` | thumbnail chính | [trang tệp](https://github.com/HungQuach301/cine-lab/blob/release-ll-ep06-v2/ll-ep06-thumb-T1.jpg) · [tải thẳng](https://github.com/HungQuach301/cine-lab/raw/release-ll-ep06-v2/ll-ep06-thumb-T1.jpg) | `64f7201d2d703fbc…` |
| `ll-ep06-thumb-T2.jpg` | thumbnail thử A/B | [trang tệp](https://github.com/HungQuach301/cine-lab/blob/release-ll-ep06-v2/ll-ep06-thumb-T2.jpg) · [tải thẳng](https://github.com/HungQuach301/cine-lab/raw/release-ll-ep06-v2/ll-ep06-thumb-T2.jpg) | `747410009dca881f…` |
| `ll-ep06.en.srt` | phụ đề tiếng Anh (182 khối) | [trang tệp](https://github.com/HungQuach301/cine-lab/blob/release-ll-ep06-v2/ll-ep06.en.srt) · [tải thẳng](https://github.com/HungQuach301/cine-lab/raw/release-ll-ep06-v2/ll-ep06.en.srt) | `9886a5ce37579ddb…` |
| `ll-ep06-youtube-description.txt` | tiêu đề và mô tả video chính | [trang tệp](https://github.com/HungQuach301/cine-lab/blob/release-ll-ep06-v2/ll-ep06-youtube-description.txt) · [tải thẳng](https://github.com/HungQuach301/cine-lab/raw/release-ll-ep06-v2/ll-ep06-youtube-description.txt) | `49a795dbe10adfe0…` |
| `ll-ep06-shorts-text.txt` | tiêu đề và mô tả 3 Short | [trang tệp](https://github.com/HungQuach301/cine-lab/blob/release-ll-ep06-v2/ll-ep06-shorts-text.txt) · [tải thẳng](https://github.com/HungQuach301/cine-lab/raw/release-ll-ep06-v2/ll-ep06-shorts-text.txt) | `b05b52f42f0fd6bf…` |
| `*.boxes.json` (2 tệp) | hộp chữ thumbnail cho qc Q12; **không tải lên YouTube** | trên nhánh | trong `SHA256SUMS.txt` |

**Cách tải và kiểm:** như tập 1, mục 0.
- Bấm "tải thẳng"; không dùng Code → Download ZIP (ZIP chỉ chứa tệp con trỏ LFS).
- Hoặc dùng dòng lệnh: `git lfs install && git clone --branch release-ll-ep06-v2 --single-branch https://github.com/HungQuach301/cine-lab.git ll-ep06-v2`.
- **Kiểm SHA:**
  - macOS: `shasum -a 256 -c SHA256SUMS.txt`, mọi dòng phải `OK`.
  - Windows (PowerShell): `Get-FileHash .\ll-ep06-v2-master-1080p.mp4 -Algorithm SHA256` phải bằng `DDABAEC5A6E1F9751A9ECBBFC0DFD998B978176583ED27A6002F1A0C9353AB13`.
- Lệch SHA thì tải lại; không đăng tệp lệch.
- Master nặng hơn các tập trước (588 MB) vì có cảnh 3D, hạt phim và tập dài 8:37. Tải lên YouTube có thể mất lâu hơn.

## 1. Tải video chính lên
**Create → Upload videos**, chọn `ll-ep06-v2-master-1080p.mp4`. Điền mục 2 trong lúc tải. Đừng bấm Publish.

## 2. Details
1. **Title** (chủ dự án đặt ở G1, phương án A): `The Computer Replaced the Typesetter and Made the Designer. Now AI Can Draw`
2. **Description:** chép toàn bộ phần sau dòng `DESCRIPTION` của `ll-ep06-youtube-description.txt`. Gồm:
   - 13 chapter từ `0:00`, mốc lấy từ timeline thật;
   - Sources (5 nguồn, không Wikipedia) và dòng **Photographs** ghi 4 ảnh Library of Congress (phòng sắp chữ New York Times, 1942);
   - câu "Projections are forecasts, not counts…";
   - **ghi công nhạc Kevin MacLeod CC BY 4.0 cho 3 bài "Reawakening", "Gymnopedie No. 1", "Clean Soul": bắt buộc, không sửa**;
   - dòng ghi công SFX Freesound (CC0, không bắt buộc nhưng giữ);
   - đoạn "How this film was made".
3. **Thumbnail: Test & compare.**
   - Phương án 1 là **T1** (`ll-ep06-thumb-T1.jpg`, bản chính): ô cửa sáng của người vẽ trong xưởng in đêm. Đây cũng là khung mở đầu của phim, nên thumbnail, tiêu đề và 15 s đầu giữ cùng một lời hứa.
   - Phương án 2 là **T2** (`ll-ep06-thumb-T2.jpg`): tường bản nháp, kèm "−1.7% PROJECTED, 2025–35" và "BLS: AI 'REDUCE THE NEED'".
   - Cả hai kiểm lề an toàn ≥ 5 % (qc Q12 ĐẠT); số trên T2 truy được về nguồn và có nhãn dự báo (qc Q13 ĐẠT).
   - Nếu không có Test & compare: tải T1 trước, thêm A/B sau.
4. **Playlist:** "Last Lamplighters".
5. **Audience:** "No, it's not made for kids"; Age restriction: không giới hạn.
6. **Show more:**
   - Paid promotion: không.
   - Altered content: mục 3.
   - Automatic chapters: bật.
   - **Tags (tuỳ chọn):** `typesetters, graphic designers, desktop publishing, generative AI, BLS projections, history of work, printing, Library of Congress, animation`
   - Video language = English; caption certification "never aired on television in the U.S."
   - License: Standard; embedding bật; Category **Education**; Comments On, giữ bình luận có thể không phù hợp để duyệt.

## 3. Altered content: **No** (chủ dự án quyết, AUTHORSHIP 06/10/2026)
- **Đối chiếu tập 6 v2:**
  - hoạt hình phong cách hoá: cảnh 3D dựng riêng cho phim (xưởng in, hầm khay chữ, phòng Linotype, tường bản nháp) và cảnh 2D cắt giấy;
  - không có cảnh quay thật bị dựng giả, không mô phỏng người thật;
  - phố và người thắp đèn là hư cấu;
  - thợ sắp chữ, người vẽ, người thiết kế là **bóng người vô danh, không mặt**;
  - tường "bản nháp" là áp phích hình học trừu tượng tự sinh, không mô phỏng tác phẩm có thật;
  - giọng kể là giọng thư viện ElevenLabs; nhạc của Kevin MacLeod; SFX là ghi âm CC0.
- **Có 4 ảnh tư liệu thật** của Library of Congress, cùng loạt FSA/OWI 1942, tổng 25,1 s (4,9 % thời lượng):

  | Mã RIGHTS | Nội dung | Trang LoC |
  |---|---|---|
  | `LOC-8d22721` | phòng sắp chữ New York Times | https://www.loc.gov/pictures/item/2017837923/ |
  | `LOC-8d22724` | tay thợ Linotype | https://www.loc.gov/pictures/item/2017837926/ |
  | `LOC-8d22743` | sắp chữ bằng tay | https://www.loc.gov/pictures/item/2017837945/ |
  | `LOC-8d22748` | dàn trang | https://www.loc.gov/pictures/item/2017837950/ |

  - Cả 4 ghi "No known restrictions. For information, see U.S. Farm Security Administration/Office of War Information Black & White Photographs" (qc Q19 ĐẠT).
  - Ảnh không bị sửa nội dung. Chỉ có chuyển động máy (Ken Burns), phủ tông màu, vignette và cắt bỏ viền phim/số âm bản. Mỗi ảnh có dòng ghi nguồn trên hình.
  - Ảnh thật, có ghi nguồn, không làm người xem tưởng sự việc giả là thật, nên vẫn chọn **No**.
- Lời dẫn không nói về việc phim được làm bằng AI (CHUAN-KENH §10). Việc này chỉ nêu ở đoạn "How this film was made" trong mô tả.
- **Kiểm lại trang chính sách YouTube ngay trước khi bấm Publish.**

## 4. Phụ đề
- **Video elements → Add subtitles → Upload file → With timing**, chọn `ll-ep06.en.srt`.
- 182 khối phụ đề. Câu đầu "Who made this: a hand, or a machine?" ở 0:00,3. Câu cuối "Some of them set type by hand." ở 8:29,3.
- Không có thoại nhân vật, chỉ lời dẫn.
- **End screen (tuỳ chọn):** thẻ kết là 4,1 s cuối (8:32,6–8:36,75; "Episode 6 · The Hand That Drew It" / "Next: When Computers Were People"). Thêm "Subscribe" và video tập 5. Đặt ở góc trên để không che chữ thẻ kết.

## 5. Kiểm và lịch đăng
- **Checks:** chờ kiểm bản quyền.
  - Ba bài nhạc dùng CC BY 4.0, có ghi công; "Gymnopedie No. 1" là bản thu của Kevin MacLeod, bản nhạc gốc của Satie (1888) thuộc phạm vi công cộng.
  - Ảnh LoC thuộc phạm vi công cộng. Nếu Content ID nhận nhầm ảnh: tranh chấp, kèm link trang LoC ở mục 3.
  - Nếu có claim nhạc: không xoá nhạc; báo P và tranh chấp kèm câu ghi công.
- **Visibility → Schedule.** Gợi ý giữ nhịp với các tập trước: thứ Ba–Thứ Năm, 9:00–11:00 sáng giờ New York (ET).
- **Đây là cổng G3: chỉ chủ dự án bấm.**
- Sau khi YouTube xử lý bản HD, xem lại trên điện thoại: chapter, phụ đề, thumbnail, dòng nguồn ảnh, các cảnh đêm (độ sáng trên màn hình nhỏ).

## 6. Ba Shorts
- Cách tải như tập 1 (mục 6): tệp 9:16, dưới 60 s, YouTube tự xếp vào Shorts.
- Title và mô tả chép từ `ll-ep06-shorts-text.txt`. Dòng ghi công nhạc ("Reawakening") giữ nguyên.
- Thay "Full film … on the channel" bằng link video chính.
- **Related video:** chọn video chính. **Altered content:** No, như video chính.

| Thời điểm (N = ngày video chính lên) | Short | Lý do |
|---|---|---|
| N, sau 2–3 giờ | **S3 "BLS: AI will reduce the need for graphic designers"** | số neo −1,7 % (dự báo 2025–35) và câu BLS; khớp lời hứa của tiêu đề |
| N + 2 | **S1 "1990: 'more are certain to disappear'"** | đối chiếu lịch sử chính của phim |
| N + 5 | **S2 "Image work posts −17% after image AI"** | góc nghiên cứu nền tảng việc tự do, kéo dài vòng đời phim |

- Không đăng Short trước video chính.

## 7. Sau khi đăng (P theo dõi khi được giao)
- **Ngày 2 và ngày 7:** ghi CTR (T1/T2), thời lượng xem trung bình, giữ chân 30 s đầu, lượt xem từ Shorts vào `reports/m3/ep06/KHAN-GIA.md`. So với tập 5 để thấy tác động của bản dựng lại (cảnh 3D, nhạc theo hồi, bản đồ liền mạch).
- **Kết quả Test & compare:** ghi bản thắng vào AUTHORSHIP.
- Nếu BLS cập nhật số OOH (đợt 2025–35) trước ngày đăng: báo chủ dự án. Đính chính bằng bình luận ghim và mô tả; chỉ dựng lại nếu số sai nằm trên hình.

## Trạng thái trước G3 (07/10/2026)
1. **Bản cuối:** tập 6 v2, dựng lại theo NGUYÊN TẮC TỐI CAO, sửa 5 điểm lời sau G2 lần 2. Claude kiểm bản sửa: **ĐẠT** (5 câu lời đúng; 79 khung nhìn, lớn nhất 4 %; judder 0; LOCK 1.7.1 KHỚP).
2. **Tệp:** nhánh `release-ll-ep06-v2` (Git LFS), commit `ac607c9`, tải ngược 11/11 SHA OK.
3. **Thumbnail:** T1 chính, A/B T2.
4. **Altered content: No.** RIGHTS cho 4 ảnh LoC, 3 bài nhạc, 8 SFX đã có.
5. **Còn lại cho G3:** chủ dự án tải tệp, kiểm SHA, làm theo mục 1–6, bấm Schedule hoặc Publish.
