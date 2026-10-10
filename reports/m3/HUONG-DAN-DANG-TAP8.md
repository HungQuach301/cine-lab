# Hướng dẫn đăng tập 8 lên YouTube Studio · Last Lamplighters

**"From Headphones to Machine Drafts: How Translators' Work Changed"** · bản v1 · **chờ duyệt G2** (`reports/m3/TAP8-G2.md`).

> Hướng dẫn này chỉ dùng **sau khi chủ dự án duyệt G2**. Trước đó tệp video chỉ nằm ngoài repo (`/var/tmp/cine-out/ll-ep08/`); nhánh phát hành chưa được tạo.

## 0. Lấy tệp (nhánh `release-ll-ep08-v1`, Git LFS — tạo sau khi duyệt G2)

- **Nơi lấy:** nhánh **`release-ll-ep08-v1`** của repo `HungQuach301/cine-lab` (nhánh mồ côi, như tập 7).
  - Nhánh chỉ chứa gói tải lên, `SHA256SUMS.txt`, `SHA256-v1.txt` và `.gitattributes`; mọi `.mp4` qua Git LFS.
- Trang nhánh (sau khi tạo): https://github.com/HungQuach301/cine-lab/tree/release-ll-ep08-v1
- Sau khi đẩy, P tải ngược mọi tệp từ link công khai và chạy `sha256sum -c`; kết quả ghi ở mục 8.

| Tệp | Dùng cho | Tải thẳng (sau khi tạo nhánh) | SHA-256 (đầu; đầy đủ trong `reports/m3/ep08/SHA256-v1.txt`) |
|---|---|---|---|
| `ll-ep08-v1-master.mp4` | video chính (901 MB, LFS; 10:07,3) | [tải](https://github.com/HungQuach301/cine-lab/raw/release-ll-ep08-v1/ll-ep08-v1-master.mp4) | `a1202dbdb0cda982…` |
| `ll-ep08-v1-p1/p2/p3.mp4` | 3 phần bản xem (68–83 MB), **không tải lên YouTube** | [p1](https://github.com/HungQuach301/cine-lab/raw/release-ll-ep08-v1/ll-ep08-v1-p1.mp4) · [p2](https://github.com/HungQuach301/cine-lab/raw/release-ll-ep08-v1/ll-ep08-v1-p2.mp4) · [p3](https://github.com/HungQuach301/cine-lab/raw/release-ll-ep08-v1/ll-ep08-v1-p3.mp4) | `a7a343d7…` · `78045316…` · `3a3abee9…` |
| `ll-ep08-short-S1.mp4` | Short 1 (26,1 s) | [tải](https://github.com/HungQuach301/cine-lab/raw/release-ll-ep08-v1/ll-ep08-short-S1.mp4) | `a94d174a35752da7…` |
| `ll-ep08-short-S2.mp4` | Short 2 (34,2 s) | [tải](https://github.com/HungQuach301/cine-lab/raw/release-ll-ep08-v1/ll-ep08-short-S2.mp4) | `e874d6d330a1ca5e…` |
| `ll-ep08-short-S3.mp4` | Short 3 (24,2 s) | [tải](https://github.com/HungQuach301/cine-lab/raw/release-ll-ep08-v1/ll-ep08-short-S3.mp4) | `b30e5259b5be1652…` |
| `ll-ep08-thumb-T1.jpg` | thumbnail chính | [tải](https://github.com/HungQuach301/cine-lab/raw/release-ll-ep08-v1/ll-ep08-thumb-T1.jpg) | `d62a7e9570f98cec…` |
| `ll-ep08-thumb-T2.jpg` | thumbnail thử A/B | [tải](https://github.com/HungQuach301/cine-lab/raw/release-ll-ep08-v1/ll-ep08-thumb-T2.jpg) | `b4fd085c031c9e6d…` |
| `ll-ep08-youtube-description.txt` | tiêu đề, mô tả, 17 chương | [tải](https://github.com/HungQuach301/cine-lab/raw/release-ll-ep08-v1/ll-ep08-youtube-description.txt) | `cb693f70b47d6005…` |
| `ll-ep08-shorts-text.txt` | tiêu đề và mô tả 3 Short | [tải](https://github.com/HungQuach301/cine-lab/raw/release-ll-ep08-v1/ll-ep08-shorts-text.txt) | `aa4ee5bf7062719e…` |
| `*.boxes.json` (2 tệp) | hộp chữ thumbnail cho qc Q12, **không tải lên YouTube** | trên nhánh | trong `SHA256-v1.txt` |

**Cách tải:**
- Bấm "tải"; không dùng Code → Download ZIP, vì ZIP chỉ chứa tệp con trỏ LFS.
- Hoặc: `git lfs install && git clone --branch release-ll-ep08-v1 --single-branch https://github.com/HungQuach301/cine-lab.git ll-ep08-v1`.

**Kiểm SHA:**
- macOS: `shasum -a 256 -c SHA256SUMS.txt`, mọi dòng phải `OK`.
- Windows (PowerShell): `Get-FileHash .\ll-ep08-v1-master.mp4 -Algorithm SHA256` phải bằng `A1202DBDB0CDA98295242F771ACFA7774F42EB73D3C91FAD77C88703DC656A45`.
- Lệch SHA thì tải lại; không đăng tệp lệch.

## 1. Thứ tự và giờ đăng

Giữ nhịp tập 7: một Short trước, tập chính sau; thứ Ba–thứ Năm, 9:00–11:00 sáng giờ New York (ET).

| Thời điểm (N = ngày video chính lên) | Đăng gì | Lý do |
|---|---|---|
| **N − 1, 9:00 ET** | **S1 "The trial that changed interpreting"** | Chuyện Nuremberg 1945 là sự thật lịch sử thuần (Dostert, dịch song song, IBM tặng thiết bị), không có số dự báo cần ngữ cảnh. Gợi tò mò về nghề phiên dịch mà không lộ phần "hôm nay". |
| **N, 9:00 ET** (thứ Ba–thứ Năm) | **Tập chính** | S1 có 24 giờ gom lượt xem; người xem S1 thấy video chính ngay trên kênh. |
| N + 2 | S2 "1954: a machine that translated 250 words" | Câu móc "a few years" của tập chính; xem sau tập chính giữ được bất ngờ "more than fifty". |
| N + 5 | S3 "A 1966 word for translators is back" | Nối 1966 với hôm nay (post-editing); kéo dài vòng đời phim. |

**Sửa chữ S1 khi đăng trước tập chính:**
- Khi đăng S1 (N − 1): thay câu "Full film: … on the channel." bằng `Full film "From Headphones to Machine Drafts: How Translators' Work Changed" comes out tomorrow on the channel.`
- Khi tập chính đã lên: sửa mô tả S1 thành link video chính, đặt **Related video** của S1 là video chính.
- S2, S3: thay "Full film on the channel" bằng link video chính; Related video là video chính.

## 2. Tải video chính và Details

1. Tải `ll-ep08-v1-master.mp4` (901 MB, 10:07,3, 1080p 24 fps).
2. **Title** (chủ dự án chọn A ở G1): `From Headphones to Machine Drafts: How Translators' Work Changed`
3. **Description:** chép toàn bộ phần sau dòng `DESCRIPTION` của `ll-ep08-youtube-description.txt`. Phần này gồm:
   - 17 chương theo mốc thật (0:00 … 9:41);
   - nguồn (ALPAC 1966, Bowen & Bowen, Hutchins, Frey & Llanos-Paredes, BLS OOH 2025–35);
   - câu "Projections are forecasts, not counts. The Oxford figure is an estimate of jobs not created, not a count of jobs lost.";
   - ghi công ảnh Library of Congress (FSA/OWI, no known restrictions), nhạc (Kevin MacLeod, CC BY 4.0), SFX (Work With Sounds CC BY 4.0; radio aporee public domain; Freesound CC0);
   - mục "How this film was made".
4. **Thumbnail: chọn T1 làm chính, bật Test & compare với T2.**
   - **T1:** buồng phiên dịch ấm sáng, tai nghe, đèn cảnh báo; chữ "FROM HEADPHONES / TO MACHINE DRAFTS / HOW TRANSLATORS' WORK CHANGED" lặp đúng tựa, không có số. Kiểu khung đèn ấm được chấm mù cao nhất qua các tập (BAI-HOC).
   - **T2:** màn hình duyệt bản nháp máy, chữ `1954: "A FEW YEARS"` / `IT TOOK MORE THAN FIFTY`. Giữ làm bản thử: câu móc mạnh, nhưng tối hơn và nhiều chữ hơn.
5. **Playlist:** "Last Lamplighters".
6. **Audience:** "No, it's not made for kids"; Age restriction: không giới hạn.
7. **Show more:**
   - Paid promotion: không. Automatic chapters: bật.
   - **Tags (tuỳ chọn):** `translators, interpreters, Nuremberg trials, simultaneous interpretation, Georgetown-IBM experiment, ALPAC report, machine translation, post-editing, BLS projections, AI and jobs, animation`
   - Video language: English. Caption certification: "never aired on television in the U.S."
   - License: Standard. Embedding: bật. Category: **Education**. Comments: On.

## 3. Altered content: **No** (theo quyết định áp từ tập 6, AUTHORSHIP 06/10/2026)

- Phim là hoạt hình phong cách hoá: cảnh 3D dựng riêng (phố thư viện và người thắp đèn, phòng đọc 1942, buồng dịch Nuremberg, phòng máy IBM 1954, phòng 1966, bàn người dịch hôm nay, phòng phiên dịch video).
- Người trong phim là **bóng người vô danh, không mặt**. Phòng xử Nuremberg giữ hình trung tính (buồng dịch, tai nghe, lưng và bóng người), **không cận mặt, không nhắc bị cáo** (chỉ đạo G1 v2).
- **Có ảnh tư liệu thật Library of Congress** (FSA/OWI, Red Cross, Washington, D.C., 1942), tổng 21,1 s (3,5 % thời lượng); có trong `RIGHTS.md` (LOC-8d21281, LOC-8d21282, đã cắt dải mép).
  - Ảnh không bị sửa nội dung: chỉ chuyển động máy, phủ tông, cắt mép; dòng nguồn hiện trên hình.
- Không dùng ảnh .gov Nuremberg (chưa đủ hồ sơ quyền Q19).
- Giọng kể là giọng thư viện ElevenLabs. Lời dẫn không nói phim làm bằng AI (CHUAN-KENH §10); chỉ nêu ở "How this film was made".
- **Kiểm lại trang chính sách YouTube ngay trước khi bấm Publish.**

## 4. Phụ đề và màn hình kết

- **Phụ đề:** gói phát hành không gồm `.srt` (như tập 7). Dùng phụ đề tự động, hoặc báo P để bổ sung `ll-ep08.en.srt` (đã dựng sẵn ngoài repo).
- **End screen (tuỳ chọn):** thẻ kết cuối phim ghi "More from Last Lamplighters". Thêm "Subscribe" và video tập 7, đặt ở góc trên để không che chữ thẻ kết.

## 5. Kiểm bản quyền và lịch

- **Checks:** chờ kiểm bản quyền.
  - Nếu Content ID nhận nhầm ảnh LoC: tranh chấp, kèm ghi chú "Library of Congress, FSA/OWI Collection, no known restrictions on publication".
  - Nếu có claim nhạc: không xoá nhạc; báo P và tranh chấp kèm câu ghi công CC BY 4.0.
- **Visibility → Schedule** theo bảng mục 1. **Đây là cổng G3: chỉ chủ dự án bấm.**
- Sau khi YouTube xử lý bản HD, xem lại trên điện thoại: chương, thumbnail, dòng nguồn ảnh, các cảnh đêm (phố thư viện, phòng phiên dịch video).

## 6. Ba Shorts

- Tệp 9:16, dưới 60 s, YouTube tự xếp vào Shorts.
- Title và mô tả chép từ `ll-ep08-shorts-text.txt`; sửa câu cuối theo mục 1.
- Dòng ghi công nhạc "Reawakening" (CC BY 4.0), SFX và "Narration: synthetic voice" giữ nguyên.
- **Altered content:** No, như video chính.

## 7. Sau khi đăng (P theo dõi khi được giao)

- Ngày 2 và ngày 7: ghi vào `reports/m3/ep08/KHAN-GIA.md` CTR T1/T2, thời lượng xem trung bình, giữ chân 30 s đầu, lượt xem từ S1 sang tập chính. So với tập 7.
- Kết quả Test & compare: ghi bản thắng vào AUTHORSHIP.
- Nếu BLS cập nhật số OOH 2025–35 (73 900 → 75 400, +2 %; mọi nghề +3,5 %) trước ngày đăng: báo chủ dự án; đính chính bằng bình luận ghim và mô tả; chỉ dựng lại nếu số sai nằm trên hình.

## 8. Kết quả kiểm SHA sau khi đẩy nhánh phát hành

- Chưa làm: chờ chủ dự án duyệt G2 và cho phép tạo `release-ll-ep08-v1`.
