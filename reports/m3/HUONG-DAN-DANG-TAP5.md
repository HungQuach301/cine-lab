# Hướng dẫn đăng tập 5 lên YouTube Studio · Last Lamplighters

P soạn ngày 06/10/2026, sau khi chủ dự án duyệt cổng G2. Cổng G3 (bấm phát hành) do chủ dự án làm.
- Làm theo cách của tập 1 (`reports/m3/HUONG-DAN-DANG-TAP1.md`) và tập 4 (`HUONG-DAN-DANG-TAP4.md`). Các bước giống hệt nhau chỉ ghi tóm tắt; mục nào khác có ghi rõ.
- Tên nút theo giao diện YouTube Studio tiếng Anh.

## 0. Lấy tệp (nhánh `release-ll-ep05-v1`, Git LFS)
- **Nơi lấy:** nhánh **`release-ll-ep05-v1`** của repo `HungQuach301/cine-lab` (public), commit `@REL@`.
  - Bản này đã gồm hai sửa sau G2:
    - nguồn câu 1966 ở đoạn mở đầu và 5 dòng nguồn còn thiếu (qc Q21);
    - dòng nguồn tràn khung trên 3 Shorts (qc Q22).
  - Nhánh chỉ có gói tải lên, `SHA256SUMS.txt` và `.gitattributes`. Master và 3 Short đi qua Git LFS.
  - **Kiểm sau khi đẩy (06/10/2026):** P tải ngược cả **11 tệp** trong `SHA256SUMS.txt` từ link công khai (LFS qua `media.githubusercontent.com`, tệp thường qua `raw.githubusercontent.com`) và chạy `sha256sum -c`: **@VER@**.
- Trang nhánh: https://github.com/HungQuach301/cine-lab/tree/release-ll-ep05-v1

@TABLE@
| `*.boxes.json` (2 tệp) | hộp chữ thumbnail cho qc Q12; **không tải lên YouTube** | trên nhánh | trong `SHA256SUMS.txt` |

**Cách tải và kiểm:** như tập 1, mục 0.
- Bấm "tải thẳng"; không dùng Code → Download ZIP (ZIP chỉ chứa tệp con trỏ LFS).
- Hoặc dùng dòng lệnh: `git lfs install && git clone --branch release-ll-ep05-v1 --single-branch https://github.com/HungQuach301/cine-lab.git ll-ep05-v1`.
- **Kiểm SHA:**
  - macOS: `shasum -a 256 -c SHA256SUMS.txt`, mọi dòng phải `OK`.
  - Windows (PowerShell): `Get-FileHash .\ll-ep05-v1-master-1080p.mp4 -Algorithm SHA256` phải bằng `@MSHAU@`.
- Lệch SHA thì tải lại; không đăng tệp lệch.
- Repo public: ai có link cũng tải được gói trước ngày phát hành (đã chấp nhận ở tập 1). P không tự xoá nhánh.

## 1. Tải video chính lên
**Create → Upload videos**, chọn `ll-ep05-v1-master-1080p.mp4`. Điền mục 2 trong lúc tải. Đừng bấm Publish.

## 2. Details
1. **Title** (chủ dự án đặt ở G1, phương án A): `In 1966, Computers Couldn't Judge an Insurance Claim. Now Software Prices the Wreck`
2. **Description:** chép toàn bộ phần sau dòng `DESCRIPTION` của `ll-ep05-youtube-description.txt`. Gồm:
   - 14 chapter từ `0:00`, mốc lấy từ timeline thật;
   - Sources (5 dòng nguồn, không Wikipedia) và dòng **Photographs** ghi nguồn 4 ảnh Library of Congress;
   - câu "Projections are forecasts…";
   - **ghi công nhạc Kevin MacLeod CC BY 4.0: bắt buộc, không sửa**;
   - đoạn "How this film was made".
3. **Thumbnail: Test & compare.** Phương án 1 là **T1** (`ll-ep05-thumb-T1.jpg`, bản chính: giám định viên chụp xe móp), phương án 2 là **T2** (`ll-ep05-thumb-T2.jpg`: biển hiệu "−9 %" + "BLS PROJECTION").
   - Cả hai kiểm lề an toàn ≥ 5 % mỗi cạnh (qc Q12 ĐẠT); số trên T2 truy được về nguồn và có nhãn dự báo (qc Q13 ĐẠT).
   - Nếu không có Test & compare: tải T1 trước, thêm A/B sau (như tập 1, mục 2.4).
4. **Playlist:** "Last Lamplighters".
5. **Audience:** "No, it's not made for kids"; Age restriction: không giới hạn.
6. **Show more:**
   - Paid promotion: không.
   - Altered content: mục 3.
   - Automatic chapters: bật.
   - **Tags (tuỳ chọn):** `claims adjusters, auto damage appraisers, insurance, office automation, AI estimates, BLS projections, history of work, Library of Congress, animation`
   - Video language = English; caption certification "never aired on television in the U.S."
   - License: Standard; embedding bật; Category **Education**; Comments On, giữ bình luận có thể không phù hợp để duyệt.

## 3. Altered content: **No** (chủ dự án quyết 06/10/2026, AUTHORSHIP)
- **Đối chiếu tập 5:**
  - hoạt hình phong cách hoá cắt giấy (Thư viện HÌNH v2), không có cảnh quay thật được dựng giả;
  - phố và người thắp đèn là hư cấu; giám định viên và nhân viên bàn bồi thường là **nhân vật vô danh cách điệu**, không mô phỏng người thật;
  - giọng kể là giọng thư viện ElevenLabs; nhạc của Kevin MacLeod.
- **Khác tập 4: có 4 ảnh tư liệu thật** của Library of Congress (1936, 1941, 1943, 1967), tổng 84,5 s (16,5 %).
  - Ảnh không bị sửa nội dung. Chỉ có chuyển động máy (Ken Burns), phủ tông màu và vignette. Mỗi ảnh có dòng nguồn trên hình.
  - Cả 4 ghi "No known restrictions on publication". Hồ sơ quyền ở `RIGHTS.md`: `LOC-8d27894`, `LOC-8c01946`, `LOC-8b28380`, `LOC-89395` (qc Q19 ĐẠT).
  - Ảnh tư liệu thật, ghi nguồn, không làm người xem tưởng sự việc giả là thật, nên vẫn chọn **No**.
- Giữ đoạn "How this film was made". **Kiểm lại trang chính sách YouTube ngay trước khi bấm Publish.**

## 4. Phụ đề
- **Video elements → Add subtitles → Upload file → With timing**, chọn `ll-ep05.en.srt`.
- 178 khối phụ đề. Câu đầu "Who decides what a damaged car is worth?" ở 0:00,6. Câu cuối "Some of them sat at the claims desk." ở 8:23,9.
- Tập này không có thoại nhân vật, chỉ lời dẫn.
- **End screen (tuỳ chọn):** thẻ kết là 6,1 s cuối (8:26,4–8:32,5, "Next: The Hand That Drew It"). Thêm "Subscribe" và video tập 4. Đặt ở góc trên để không che chữ thẻ kết.

## 5. Kiểm và lịch đăng
- **Checks:** chờ kiểm bản quyền.
  - Nhạc "Immersed" và "Reawakening" dùng giấy phép CC BY 4.0, có ghi công.
  - Ảnh LoC thuộc phạm vi công cộng. Nếu Content ID nhận nhầm ảnh: tranh chấp, kèm link trang LoC trong `RIGHTS.md`.
  - Nếu có claim nhạc: không xoá nhạc; báo P và tranh chấp kèm câu ghi công.
- **Visibility → Schedule.** Gợi ý giữ nhịp với các tập trước: thứ Ba–Thứ Năm, 9:00–11:00 sáng giờ New York (ET).
- **Đây là cổng G3: chỉ chủ dự án bấm.**
- Sau khi YouTube xử lý bản HD, xem lại trên điện thoại: chapter, phụ đề, thumbnail, dòng nguồn ảnh.

## 6. Ba Shorts
- Cách tải như tập 1 (mục 6): tệp 9:16, dưới 60 s, YouTube tự xếp vào Shorts.
- Title và mô tả chép từ `ll-ep05-shorts-text.txt`. Ghi công nhạc giữ nguyên.
- Thay "Full film … on the channel" bằng link video chính.
- **Related video:** chọn video chính. **Altered content:** No, như video chính.

| Thời điểm (N = ngày video chính lên) | Short | Lý do |
|---|---|---|
| N, sau 2–3 giờ | **S1 "Software that drafts the estimate for a wrecked car"** | số neo −9 % và câu BLS về phần mềm định giá ảnh |
| N + 2 | **S2 "1966: the computer couldn't judge. 2026?"** | đối chiếu lịch sử chính của phim |
| N + 5 | **S3 "88% of auto insurers — use, plan, or explore AI"** | góc khảo sát NAIC, kéo dài vòng đời phim |

- Không đăng Short trước video chính.

## 7. Sau khi đăng (P theo dõi khi được giao)
- **Ngày 2 và ngày 7:** ghi CTR (T1/T2), thời lượng xem trung bình, giữ chân 30 s đầu, lượt xem từ Shorts vào `reports/m3/ep05/KHAN-GIA.md`. So với tập 4 (tập đầu áp luật nhịp) để thấy tác động của HÌNH v2.
- **Kết quả Test & compare:** ghi bản thắng vào AUTHORSHIP.
- Nếu BLS cập nhật số OOH trước ngày đăng: báo chủ dự án. Đính chính bằng bình luận ghim và mô tả; chỉ dựng lại nếu số sai nằm trên hình.

## Trạng thái trước G3 (06/10/2026)
1. **Bản cuối và Shorts:** chủ dự án duyệt ở G2. Sau G2 có hai sửa:
   - nguồn đoạn mở đầu, theo chỉ đạo, kèm 5 dòng nguồn thiếu do Q21 bắt;
   - dòng nguồn tràn khung trên Shorts, do Q22 bắt.
   - Lời phim không đổi. Câu chú thích S2 "…declined" thành "…fell".
2. **Tệp:** nhánh `release-ll-ep05-v1` (Git LFS), commit `@REL@`, tải ngược 11/11 SHA OK.
3. **Thumbnail:** T1 chính, A/B T2.
4. **Altered content: No.** Giữ "How this film was made". RIGHTS cho 4 ảnh LoC đã có.
5. **Còn lại cho G3:** chủ dự án tải tệp, kiểm SHA, làm theo mục 1–6, bấm Schedule hoặc Publish.
