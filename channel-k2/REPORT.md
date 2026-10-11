# Gói kênh 2: báo cáo mốc 1 (định vị) và mốc 2 (hồ sơ cầu), 11/10/2026

> Nhánh `channel-k2`, tách từ `origin/market-k2`. **Chưa dựng tập.**
> Đầu vào: chủ dự án chọn hướng B, *cơ chế kinh tế của một ngành*, ngày 11/10. Khoảng 1/4 đề tài là tài chính–thanh toán, chỉ giải thích cơ chế, không khuyên đầu tư/tài chính cá nhân.
> Mọi chỉ số trong gói là **tự tính, không phải chỉ số YouTube**, trừ các mục tiêu Studio trong `THI-DIEM.md`.

## Kết quả chính
1. **Định vị (mốc 1):** đủ 7 tài liệu:

| Tài liệu | Nội dung |
|---|---|
| `TRU-NOI-DUNG.md` | 4 trụ, tỷ lệ 25/25/42/8 % |
| `LUAT-CHON-DE-TAI.md` | 5 điều kiện, thêm nhãn Cầu-bền |
| `HIEN-CHUONG.md` | Lời hứa, cấu trúc 6 phần, giá trị con người |
| `LUAT-NOI-DUNG.md` | Nguồn, sự kiện/nhận định, không persona, miễn trừ tài chính, quy trình sửa/gỡ |
| `NHAN-DIEN.md` | Sa bàn 3D, bảng màu ≥ 7:1, Inter, 3 giọng ứng viên khác Bill, nhạc |
| `TEN-KENH.md` | Đề xuất Moving Parts / Throughput / Load Bearing |
| `HANG-DOI.md` | 12 đề tài, thứ tự phát |

2. **Hồ sơ cầu (mốc 2):** `de-tai/container.md`, `de-tai/jet-airliner.md`, `de-tai/card-networks.md`. Cả ba đạt **Cầu-bền** nhưng mạnh yếu rất khác nhau:

| Hồ sơ | Video đầu | Video 2026 cao nhất | Bình luận được dùng |
|---|---|---|---|
| Container | 4,83 triệu | 329 | 150 |
| Jet | 3,85 triệu | 565 nghìn | 116 |
| Thẻ | 1,04 triệu | 363 | 44 |

3. **Thí điểm đề xuất: container**, 16–18 phút (`THI-DIEM.md`). Mục tiêu 7 ngày:

| Chỉ số Studio | Mục tiêu | Sàn |
|---|---|---|
| CTR hiển thị | ≥ 4,0 % | 2,5 % |
| Tỷ lệ xem trung bình | ≥ 35 % | 25 % |
| Giữ chân ở 0:30 | ≥ 70 % | 55 % |
| Lượt xem/ngày | ≥ 140 | 30 |

4. **Phát hiện ngược kỳ vọng: nhánh tài chính–thanh toán chỉ có cầu ở cụm thẻ.**
   - Trong 90 ngày, video mới về Visa/Mastercard cao nhất 93 lượt, SWIFT 414, ATM 2 276 (tự tính): nhiều video mới cùng chủ đề, lượt xem rất thấp.
   - Toàn thời gian, chỉ cụm thẻ đạt ngưỡng 500 nghìn: Visa/Mastercard 1,04 triệu, "who pays for rewards" 1,51 triệu.
   - Trượt: SWIFT, ATM, bảo hiểm, chuyển tiền liên ngân hàng. Lệch sang tài chính cá nhân/đầu tư: ngân hàng, sở giao dịch.
   - Tỷ lệ ~1/4 hiện giữ bằng 2 đề tài thẻ + 1 đề tài lai (hãng bay).

## Phương pháp, quota, chi phí
- **YouTube Data API v3** qua credential môi trường; mã không chứa khoá và không in URL.
  - **26 search.list:**

| Bước | Số lượt |
|---|---|
| Nhãn 90 ngày | 5 |
| Cầu-bền toàn thời gian | 7 |
| Hồ sơ cầu (3 đề tài × 3 câu) | 9 |
| Kiểm tên kênh (trong giới hạn ≤ 3) | 3 |
| Thăm dò quota | 2 |

  - Thêm khoảng 57 lệnh đọc khác (21 videos.list, 3 channels.list, 6 forHandle, 27 commentThreads). Tổng khoảng 2 660 đơn vị.
  - Hạn mức search.list của ngày đã cạn sau vòng market-k2. Phần mốc 2 chạy sau khi hạn mức đặt lại; mã chờ khi gặp 429, không bỏ dở.
- **AI:** `claude -p` với `ANTHROPIC_API_KEY=$CONSOLE_API_KEY`, không subagent.
  - Haiku: phân loại bình luận và kiểm khoảng trống.
  - Sonnet: tổng hợp hồ sơ và REVIEWER.
  - Chi phí thu và tổng hợp **$0,51**, REVIEWER **$0,79** (2 lượt); tổng **≈ $1,30** / trần $5.
- **Luật dữ liệu (như market-k2):**
  - Số liệu thô, kể cả bình luận nguyên văn, ở `$K2C_DATA` (mặc định `~/.cache/cine-channel-k2`), ngoài git (`.gitignore` chặn `*.json`, `*.jsonl`).
  - Mỗi lần chạy `collect.py` (kể cả `collect.py purge`) tự xoá file > 30 ngày; `cost.jsonl` được giữ để trần $5 không bị đặt lại. **Không có lịch xoá khi mã không chạy** (cùng ngoại lệ như market-k2); trên thực tế số liệu mất cùng container phiên. Phiên sau dùng lại dữ liệu phải chạy `collect.py purge` trước.
  - Hồ sơ trong git chỉ có ý tóm tắt do Haiku diễn đạt lại, không tên người bình luận.
- **Mã:** `collect.py` (labels · durable · names · demand), `report.py` (bảng hồ sơ).

## Giới hạn
- **Nhãn 6/12 đề tài** (#4, #5, #6, #7, #8, #12) chỉ dựa trên market-k2 vòng 1. Số liệu thô vòng đó đã mất, và vòng xác nhận không lặp lại lợi thế của B trên câu hỏi mới. Nên đo lại toàn thời gian trước khi viết hồ sơ các đề tài này.
- **Lấy mẫu:** "top 5" là 5 video ≥ 8 phút đầu tiên trong 15 kết quả theo độ liên quan.
  - Năm câu có ít hơn 5 video dài, vì Shorts chiếm kết quả: container câu 3 (2), jet câu 1 (3) và câu 3 (2), thẻ câu 2 (2) và câu 3 (0).
  - Thứ tự liên quan của API có thể khác trang tìm kiếm người dùng thấy.
- **Bình luận:** 50 bình luận "relevance" mỗi video, nên bình luận cũ và nhiều like được ưu tiên.
  - Hồ sơ thẻ có 74/84 bình luận đến từ một video.
  - Haiku có thể gán nhầm loại; độ phủ nhãn đủ 100 % sau khi tự gắn lại phần sót.
- **Khoảng trống:** vẫn chỉ đọc chữ (tiêu đề, mô tả, bình luận), không xem hình đối thủ.
- **Tên kênh:** chưa kiểm nhãn hiệu, và chưa kiểm được handle có đặt được hay không.
- **Ngưỡng:** không có chỉ số nào nằm trong ±5 % quanh ngưỡng.
  - Cầu-bền thấp nhất là 1,04 triệu so với ngưỡng 500 nghìn.
  - Khoảng trống: 0/5 so với ngưỡng ≤ 1/5.
  - Phủ nhãn 100 % so với ngưỡng 95 %.
  - Lần chạy đầu của jet chỉ phủ 78 %. Mã dừng đúng luật và chạy lại.

## Phép thử F1: lõi nhà máy LL dùng chung và phần riêng gói kênh
| Dùng chung lõi LL | Riêng gói kênh 2 |
|---|---|
| `scripts/ll/ll.py` (đặc tả, nguồn đọc toàn văn, `numbers`/`say`, ACTUAL/PROJECTION, cache TTS) | Trường mới đề xuất: `pillar:`, `claims:` (fact/opinion/calc + src) |
| `render.js`, `lib/charts.js`, `lib/shot.js` (24 fps tất định, cột/đường/so sánh, chuyển cảnh) | Mặt nền bảng kỹ thuật thay giấy B3; bảng màu + `GRADES` mới; Inter |
| `design/ll-hero/kit.js` (three.js headless, `camRig`, `box/cyl`, `dust`, `canvasTex`, hậu kỳ); tham chiếu khối nhà chứa/hầm gió `ep07.js` | 4 bộ cảnh: cảng–tàu–cẩu, xưởng lắp ráp, thị trấn sa bàn, đường ống tiền; bản đồ tuyến thương mại |
| `mix.py` (−14 LUFS, TP ≤ −1 dBTP), `build.sh`, `qc.sh` (khung trống, judder, chữ, Q12 thumbnail), `thumb.py` | Giọng mới (khác Bill), nhạc/SFX mới; kiểm câu miễn trừ T3 tài chính và kiểm `claims:` (gửi K, chưa sửa `checks/`) |
| Luật RIGHTS, luật nguồn, kiểm mù màu | Hiến chương 6 phần thay STORY/HISTORY/TODAY; luật chọn đề tài; luật nội dung pháp lý; quy trình sửa/gỡ |

## Đang chờ chủ dự án
1. **Tên kênh:** chọn một trong ba (đề xuất Moving Parts `@movingpartsecon`), rồi kiểm handle trực tiếp và kiểm nhãn hiệu USPTO.
2. **Tập thí điểm:** container (đề xuất) hay jet.
3. **Tỷ lệ tài chính–thanh toán:** giữ ~1/4 bằng cụm thẻ + hãng bay lai, hay hạ xuống ~1/6.
4. **Giọng:** duyệt thu mẫu mù 3 giọng (Eric, Matilda, River), khoảng 900 ký tự ElevenLabs.
5. **Nguồn nhạc:** Freesound bị chặn ở môi trường này (403). Chọn giữa thư viện CC0 khác và đặt nhạc sĩ.
6. **Đọc soát kỹ thuật:** có mời người làm ngành hàng hải đọc kịch bản thí điểm không.
7. **Bộ nhận diện:** duyệt NHAN-DIEN (bảng màu, sa bàn 3D) trước khi dựng bộ cảnh cảng.

## REVIEWER headless (Sonnet, 2 lượt, $0,79)
Soát 5 nhóm luật: R1 phỉ báng · R2 YMYL/tài chính · R3 luật dữ liệu · R4 khẳng định chưa có nguồn · R5 nhất quán số.

**Lượt 1: 16 FAIL, đã sửa hết.**
- **R1:**
  - Nhận định "ngập video AI/hàng loạt" về kênh khác bị viết như sự thật, có chỗ kèm tên kênh.
  - Đã đổi thành mô tả số đo, gắn nhãn suy luận, và bỏ tên kênh khỏi chỗ phê phán.
  - Điểm yếu đối thủ của jet nay ghi là ý kiến người bình luận.
- **R3:**
  - HIEN-CHUONG và THI-DIEM thiếu nhãn "tự tính"; đã thêm.
  - Đã ghi rõ ngoại lệ xoá dữ liệu khi mã không chạy.
  - `purge` không còn xoá sổ chi phí AI, để trần $5 không bị đặt lại.
- **R4:**
  - Tranh chấp pháp lý ngành thẻ, nội dung Regulation II/EU, nghiên cứu của Fed, giả định CTR kênh mới: đã gắn [cần kiểm] hoặc "giả định".
  - Đã bỏ câu "meme internet".
- **R5:** đã sửa các số lệch:
  - 5 câu thiếu video dài (trước ghi 3);
  - 6 đề tài tài chính đã đo (trước ghi 8);
  - 6/12 nhãn chỉ dựa trên market-k2 (trước ghi 7/12);
  - 4 chỉ số Studio (trước ghi 3);
  - 57 lệnh đọc khác (trước ghi khoảng 40).

**Lượt 2: R1, R2, R3, R5 PASS.** Còn 2 FAIL R4 mức nhẹ, đã sửa sau lượt 2: "UPI là hạ tầng công" và cơ chế bán dặm của hãng bay nay gắn [cần kiểm]. Không chạy lượt 3.
