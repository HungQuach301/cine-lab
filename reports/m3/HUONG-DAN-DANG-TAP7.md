# Hướng dẫn đăng tập 7 lên YouTube Studio · Last Lamplighters

**"When Computers Were People: One Word, Three Jobs"** · bản v1 · G2 DUYỆT 09/10/2026 (chủ dự án, nguyên trạng).

## 0. Lấy tệp (nhánh `release-ll-ep07-v1`, Git LFS)

- **Nơi lấy:** nhánh **`release-ll-ep07-v1`** của repo `HungQuach301/cine-lab`.
  - Nhánh chỉ chứa gói tải lên, `SHA256SUMS.txt`, `SHA256-v1.txt` và `.gitattributes`.
  - Mọi tệp `.mp4` đi qua Git LFS.
- Trang nhánh: https://github.com/HungQuach301/cine-lab/tree/release-ll-ep07-v1
- **Kiểm sau khi đẩy (09/10/2026):** commit `6adb15c`, tải ngược 14/14 SHA OK (mục 8).

| Tệp | Dùng cho | Tải thẳng | SHA-256 (đầu; đầy đủ trong `SHA256SUMS.txt`) |
|---|---|---|---|
| `ll-ep07-v1-master.mp4` | video chính (973 MB, LFS; 10:17,7) | [tải](https://github.com/HungQuach301/cine-lab/raw/release-ll-ep07-v1/ll-ep07-v1-master.mp4) | `ec203d6304b0aed1…` |
| `ll-ep07-v1-p1/p2/p3.mp4` | 3 phần bản xem (74–77 MB), **không tải lên YouTube** | [p1](https://github.com/HungQuach301/cine-lab/raw/release-ll-ep07-v1/ll-ep07-v1-p1.mp4) · [p2](https://github.com/HungQuach301/cine-lab/raw/release-ll-ep07-v1/ll-ep07-v1-p2.mp4) · [p3](https://github.com/HungQuach301/cine-lab/raw/release-ll-ep07-v1/ll-ep07-v1-p3.mp4) | `6516bda7…` · `1c46b4de…` · `86c36e9a…` |
| `ll-ep07-short-S1.mp4` | Short 1 (22,4 s) | [tải](https://github.com/HungQuach301/cine-lab/raw/release-ll-ep07-v1/ll-ep07-short-S1.mp4) | `d6ad2ed38885dca3…` |
| `ll-ep07-short-S2.mp4` | Short 2 (33,7 s) | [tải](https://github.com/HungQuach301/cine-lab/raw/release-ll-ep07-v1/ll-ep07-short-S2.mp4) | `9025ee94d7255bfa…` |
| `ll-ep07-short-S3.mp4` | Short 3 (17,3 s) | [tải](https://github.com/HungQuach301/cine-lab/raw/release-ll-ep07-v1/ll-ep07-short-S3.mp4) | `723d3374c02ffb23…` |
| `ll-ep07-thumb-T1.jpg` | thumbnail chính | [tải](https://github.com/HungQuach301/cine-lab/raw/release-ll-ep07-v1/ll-ep07-thumb-T1.jpg) | `6a0eb63ff1688762…` |
| `ll-ep07-thumb-T2.jpg` | thumbnail thử A/B | [tải](https://github.com/HungQuach301/cine-lab/raw/release-ll-ep07-v1/ll-ep07-thumb-T2.jpg) | `6d92715c8e2e8929…` |
| `ll-ep07-youtube-description.txt` | tiêu đề, mô tả, chương | [tải](https://github.com/HungQuach301/cine-lab/raw/release-ll-ep07-v1/ll-ep07-youtube-description.txt) | `b7f67b593efca67b…` |
| `ll-ep07-shorts-text.txt` | tiêu đề và mô tả 3 Short | [tải](https://github.com/HungQuach301/cine-lab/raw/release-ll-ep07-v1/ll-ep07-shorts-text.txt) | `15c73a46b014bd77…` |
| `*.boxes.json` (2 tệp) | hộp chữ thumbnail cho qc Q12, **không tải lên YouTube** | trên nhánh | trong `SHA256SUMS.txt` |

**Cách tải:**
- Bấm "tải"; không dùng Code → Download ZIP, vì ZIP chỉ chứa tệp con trỏ LFS.
- Hoặc dùng dòng lệnh: `git lfs install && git clone --branch release-ll-ep07-v1 --single-branch https://github.com/HungQuach301/cine-lab.git ll-ep07-v1`.

**Kiểm SHA:**
- macOS: `shasum -a 256 -c SHA256SUMS.txt`, mọi dòng phải `OK`.
- Windows (PowerShell): `Get-FileHash .\ll-ep07-v1-master.mp4 -Algorithm SHA256` phải bằng `EC203D6304B0AED13C5DD7F7F3A1649A44255AD03BBC850C68839FA83B3DDFB4`.
- Lệch SHA thì tải lại; không đăng tệp lệch.

## 1. Thứ tự và giờ đăng

Chủ dự án quyết: một Short trước, tập chính sau. Giờ theo nhịp các tập trước: thứ Ba–thứ Năm, 9:00–11:00 sáng giờ New York (ET).

| Thời điểm (N = ngày video chính lên) | Đăng gì | Lý do |
|---|---|---|
| **N − 1, 9:00 ET** | **S1 "'Computer' used to be a job title"** | Câu móc tò mò ("máy tính từng là một chức danh") khớp tựa tập chính, chỉ dùng sự thật lịch sử (5 người, 1935; NASA), không có số dự báo cần ngữ cảnh. Nó dọn đường cho tập chính mà không lộ phần "hôm nay". |
| **N, 9:00 ET** (thứ Ba–thứ Năm) | **Tập chính** | Sau khi S1 có 24 giờ gom lượt xem, người xem S1 thấy video chính ngay trên kênh. |
| N + 2 | S2 "Programmers vs. developers, 2025–35" | Số dự báo BLS (1,72 → 1,89 triệu); cần ngữ cảnh của tập chính nên đăng sau. |
| N + 5 | S3 "1990: AI as 'just additional tools'" | Đối chiếu lịch sử, kéo dài vòng đời phim. |

**Sửa chữ S1 khi đăng trước tập chính:**
- Khi đăng S1 (N − 1): thay câu cuối "Full film: … on the channel." bằng `Full film "When Computers Were People: One Word, Three Jobs" comes out tomorrow on the channel.`
- Khi tập chính đã lên: sửa lại mô tả S1 thành link video chính, và đặt **Related video** của S1 là video chính.
- S2, S3: thay "Full film on the channel" bằng link video chính; Related video là video chính.

## 2. Tải video chính và Details

1. Tải `ll-ep07-v1-master.mp4`. Tệp nặng hơn các tập trước (973 MB, 10:17,7, cảnh 3D 1080p), nên tải lên có thể lâu.
2. **Title** (chủ dự án chọn A′ ở G1): `When Computers Were People: One Word, Three Jobs`
3. **Description:** chép toàn bộ phần sau dòng `DESCRIPTION` của `ll-ep07-youtube-description.txt`. Phần này gồm:
   - 17 chương theo mốc thật (0:00 … 9:51);
   - nguồn;
   - ghi công nhạc (Kevin MacLeod, CC BY 4.0), SFX (Work With Sounds CC BY 4.0; radio aporee, Public Domain Mark; Freesound CC0);
   - câu "their use does not imply endorsement by NASA";
   - mục "How this film was made".
4. **Thumbnail: chọn T1 làm chính, bật Test & compare với T2.**
   - **Lý do chọn T1:**
     - Ảnh là dải cửa sổ phòng tính toán ấm sáng cạnh cột đèn khí. Đây là kiểu hình người chấm mù Q27 cho điểm cao nhất ở mọi lần (cảnh đèn ấm trên nền chạng vạng).
     - Chữ "WHEN COMPUTERS WERE PEOPLE / ONE WORD, THREE JOBS" lặp đúng tựa, gợi tò mò, không có số dễ hiểu sai.
     - Tông ấm khác hẳn các thumbnail tối của tập trước.
   - **T2** (màn hình mã trong văn phòng đêm, "SOFTWARE DEVELOPERS: +10.2% PROJECTED, 2025–35 / PROGRAMMERS: PROJECTED TO SHRINK"):
     - giữ làm bản thử, vì có thể kéo người quan tâm việc làm ngành phần mềm;
     - nhưng tối và nhiều chữ, đúng kiểu khung bị chấm thấp;
     - dù đã gắn nhãn dự báo, số trên thumbnail vẫn có rủi ro bị hiểu thành con số đã xảy ra.
5. **Playlist:** "Last Lamplighters".
6. **Audience:** "No, it's not made for kids"; Age restriction: không giới hạn.
7. **Show more:**
   - Paid promotion: không.
   - Automatic chapters: bật.
   - **Tags (tuỳ chọn):** `human computers, NASA Langley, West Area Computers, history of computing, software developers, computer programmers, BLS projections, AI and jobs, animation`
   - Video language: English. Caption certification: "never aired on television in the U.S."
   - License: Standard. Embedding: bật. Category: **Education**. Comments: On.

## 3. Altered content: **No** (theo quyết định đã áp từ tập 6, AUTHORSHIP 06/10/2026)

- Phim là hoạt hình phong cách hoá: cảnh 3D dựng riêng cho phim (phòng thí nghiệm bên sân bay, phòng tính toán, phòng máy rơ-le, phòng tính toán JPL, văn phòng hôm nay, cái thang).
- Người trong phim là **bóng người vô danh, không mặt**. Phố và người thắp đèn là hư cấu. Không mô phỏng người thật, không có cảnh quay thật bị dựng giả.
- **Có 7 ảnh tư liệu thật NACA/NASA** (Langley Research Center, 1943–1959), tổng 51,5 s (8,3 % thời lượng); đều có trong `RIGHTS.md` (NASA-LRC-*).
  - Ảnh không bị sửa nội dung. Chỉ có chuyển động máy, phủ tông màu, cắt bỏ dải chú thích; mỗi ảnh có dòng ghi nguồn trên hình.
  - Không dùng logo NASA và không ngụ ý NASA bảo trợ.
- Giọng kể là giọng thư viện ElevenLabs.
- Lời dẫn không nói phim làm bằng AI (CHUAN-KENH §10). Việc này chỉ nêu ở mục "How this film was made" trong mô tả.
- **Kiểm lại trang chính sách YouTube ngay trước khi bấm Publish.**

## 4. Phụ đề và màn hình kết

- **Phụ đề:** gói phát hành theo danh sách chủ dự án duyệt **không gồm tệp .srt**. Dùng phụ đề tự động của YouTube, hoặc báo P để bổ sung `ll-ep07.en.srt` (đã dựng sẵn ngoài repo).
- **End screen (tuỳ chọn):** thẻ kết ở cuối phim ghi "Last Lamplighters · Episode 7" và "Next: The Translator's Desk". Thêm "Subscribe" và video tập 6, đặt ở góc trên để không che chữ thẻ kết.

## 5. Kiểm bản quyền và lịch

- **Checks:** chờ kiểm bản quyền.
  - Nếu Content ID nhận nhầm ảnh NASA: tranh chấp, kèm ghi chú "NACA/NASA photograph, U.S. government work, NASA Image and Video Library".
  - Nếu có claim nhạc: không xoá nhạc; báo P và tranh chấp kèm câu ghi công CC BY 4.0.
- **Visibility → Schedule** theo bảng ở mục 1. **Đây là cổng G3: chỉ chủ dự án bấm.**
- Sau khi YouTube xử lý bản HD, xem lại trên điện thoại:
  - chương, thumbnail, dòng nguồn ảnh;
  - các cảnh đêm của phần "hôm nay", độ sáng trên màn hình nhỏ.

## 6. Ba Shorts

- Tệp 9:16, dưới 60 s, YouTube tự xếp vào Shorts.
- Title và mô tả chép từ `ll-ep07-shorts-text.txt`. Sửa câu cuối theo mục 1.
- Dòng ghi công nhạc "Reawakening" (CC BY 4.0) và các SFX giữ nguyên.
- **Altered content:** No, như video chính.

## 7. Sau khi đăng (P theo dõi khi được giao)

- Ngày 2 và ngày 7: ghi vào `reports/m3/ep07/KHAN-GIA.md`:
  - CTR của T1/T2;
  - thời lượng xem trung bình;
  - giữ chân 30 s đầu;
  - lượt xem từ S1 (đăng trước) sang tập chính.
- So với tập 6, để thấy tác động của "Short trước": thứ tự đăng mới.
- **Kết quả Test & compare:** ghi bản thắng vào AUTHORSHIP.
- Nếu BLS cập nhật số OOH 2025–35 trước ngày đăng: báo chủ dự án. Đính chính bằng bình luận ghim và mô tả; chỉ dựng lại nếu số sai nằm trên hình.

## 8. Kết quả kiểm SHA sau khi đẩy nhánh phát hành

- Nhánh `release-ll-ep07-v1`, commit **`6adb15c`**.
- 09/10/2026: P tải ngược cả **14 tệp** trong `SHA256SUMS.txt` từ link công khai (`https://github.com/HungQuach301/cine-lab/raw/release-ll-ep07-v1/<tệp>`) vào thư mục trống, rồi chạy `sha256sum -c`: **cả 14 OK**.
- Master tải về đủ 973 019 139 byte, đúng tệp thật chứ không phải con trỏ LFS.
