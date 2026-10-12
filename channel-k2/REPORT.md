# Gói kênh 2: báo cáo mốc 1 (định vị) và mốc 2 (hồ sơ cầu), 11/10/2026

> Nhánh `channel-k2`, tách từ `origin/market-k2`. **Chưa dựng tập.**
> Đầu vào: chủ dự án chọn hướng B, *cơ chế kinh tế của một ngành*, ngày 11/10. Khoảng 1/4 đề tài là tài chính–thanh toán, chỉ giải thích cơ chế, không khuyên đầu tư/tài chính cá nhân.
> Mọi chỉ số trong gói là **tự tính, không phải chỉ số YouTube**, trừ các mục tiêu Studio trong `THI-DIEM.md`.

> **Vòng 2 "Cầu hiện hành" (11/10/2026):** 5/12 đề tài đạt Mạnh, nên theo luật của chủ dự án ra nhánh **3–5/12: TIẾP B**, hàng đợi chỉ giữ 7 đề tài Mạnh/Yếu.
> - Container rơi xuống "Không" (0 video ≥ 50 nghìn đúng đề tài trong 90 ngày), nên thí điểm đề xuất đổi sang **factory town**.
> - Ở chuẩn liên quan rộng, kết quả là 10/12 Mạnh. TIẾP B vững ở cả hai chuẩn.
> - Kiểm nhãn bộ lọc kênh cũ: sai "không lộ mặt" 10 %, lệch ngách B 44 %.
> - Xem mục "Cầu hiện hành" ở cuối.

## Kết quả chính (vòng 1)
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

## Đang chờ chủ dự án (vòng 1; xem danh sách cập nhật ở mục "Cầu hiện hành")
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

---
## Cầu hiện hành (vòng 2, 11/10/2026)
Mọi chỉ số trong mục này là **tự tính, không phải chỉ số YouTube**. Mã: `current.py` (dùng lại cache/API/AI của `collect.py`).

### 1. Model: kiểm ghim và model thực chạy
- **Ghim mọi lệnh `claude -p`** theo chủ dự án:
  - lọc kênh + liên quan/khoảng trống: `claude-sonnet-5-5`;
  - phân loại bình luận: `claude-haiku-5-5`;
  - REVIEWER: `claude-opus-5-5`.
  - `collect.ai()` nay **bắt buộc** truyền model và ghi thêm trường `served` (model thực chạy, đọc từ `modelUsage` của CLI).
- **Kiểm thật (gọi thử):** `--model` haiku, sonnet, opus đều chạy đúng model ghim. **Không ghim → CLI mặc định `claude-sonnet-5-5`.** Lệnh Sonnet/Opus còn ghi thêm `claude-haiku-5-5` trong `served`, do CLI dùng Haiku cho tác vụ phụ nội bộ; model chính vẫn đúng.
- **Trước đây:**
  - Mọi lệnh trong mã market-k2 và channel-k2 đều có `--model`; không lệnh nào chạy model mặc định.
  - `cost.jsonl` cũ (33 dòng: 30 Haiku, 3 Sonnet) **chỉ ghi model yêu cầu**, không ghi model thực chạy. Vì CLI tôn trọng `--model` (đã kiểm), model thực chạy suy ra là đúng model ghi.
  - **Lệch so với luật mới:** kiểm khoảng trống vòng 1 (nhãn "0/5 có số liệu thật") chạy **Haiku**, không phải Sonnet. Nay `gap_check` dùng Sonnet. Nhãn khoảng trống vòng 1 chưa chạy lại.
  - Hai lượt REVIEWER channel-k2 vòng 1 ghim Sonnet (luật lúc đó), chạy từ shell nên không vào `cost.jsonl`.
  - REVIEWER market-k2 (Haiku theo báo cáo market-k2): lệnh không nằm trong mã và `cost.jsonl` của market-k2 đã mất cùng container cũ, nên **không kiểm được**.
- **Phân bổ chi phí vòng 2** (theo `cost.jsonl`, model yêu cầu → served):

| Model yêu cầu | Served | Số lượt | Chi phí |
|---|---|---|---|
| Sonnet | haiku + sonnet | 19 | $0,98 |
| Sonnet | sonnet | 6 | $0,27 |
| Haiku | haiku | 9 | $0,09 |
| Opus | haiku + opus | 1 | $0,46 |

  - Gọi thử model: khoảng $0,12.
  - REVIEWER Opus cho tài liệu: 1 lượt, $0,51, served `claude-opus-5-5` (+ Haiku phụ).
  - R1 phỉ báng, R2 YMYL, R3 luật dữ liệu, R5 khớp số với dữ liệu gốc: **PASS**.
  - R4 tính toàn vẹn luật quyết định: 2 FAIL, đã sửa. (1) Danh sách đổi nhãn ở chuẩn rộng thiếu card networks. (2) Bảng ứng viên bổ sung chưa nói rõ phần lớn ứng viên là đề tài vừa bị loại, viết lại góc.
  - Không chạy lượt 2.
- **Tổng chi phí AI phiên vòng 2:** $1,79 theo `cost.jsonl` (bộ lọc cũ, liên quan, độ nhạy, chấm lại, Opus kiểm nhãn) + $0,12 gọi thử model + $0,51 REVIEWER ≈ **$2,42**. Trần $5.

### 2. Kiểm nhãn bộ lọc kênh cũ
- **Không còn danh sách kênh đã lọc của market-k2:** số liệu thô vòng đó đã mất cùng container cũ, và channel-k2 vòng 1 không lọc kênh. Tôi **tái lập đúng bộ lọc cũ**: cùng prompt nguyên văn, Haiku, 1 video mẫu là video nhiều lượt xem nhất của kênh trong mẫu.
- **Mẫu:** áp lên toàn bộ kênh có video ≥ 8 phút trong 72 lượt tìm kiếm của mục 3 (cùng thiết lập market-k2: 90 ngày, US, ≥ 8 phút; đề tài đều thuộc B).
  - 659 kênh ứng viên → bộ lọc cũ cho qua **533 (81 %)**, khớp tỷ lệ 81–93 % market-k2 ghi.
  - Chọn ngẫu nhiên **50** kênh đã qua lọc (seed 20261011).
- **Chấm lại:**
  - Sonnet 5.5 đọc khoảng 10 tiêu đề video dài gần nhất, mô tả kênh và 2 mô tả video.
  - REVIEWER Opus 5.5 ra nhãn cuối từ cùng bằng chứng.
  - Sonnet và Opus khớp **48/50**.

| Nhãn cuối (Opus) | Sai so với bộ lọc cũ | KTC 90 % (Wilson) |
|---|---|---|
| Không phải kênh giải thích không lộ mặt | **5/50 = 10 %** | 5,0–19,2 % |
| Không thuộc ngách B (lịch sử/kinh tế doanh nghiệp–ngành) | **22/50 = 44 %** | 33,1–55,6 % |
| Sai ít nhất một trong hai (5 kênh sai mặt đều nằm trong 22 kênh lệch ngách) | 22/50 = 44 % | 33,1–55,6 % |

- Kênh lệch ngách điển hình: kỹ thuật/siêu dự án, địa chính trị Trung Quốc, tài chính cá nhân, hoài niệm văn hoá, "giải thích chung".
- **Bộ lọc cũ chỉ hỏi "không lộ mặt", không hỏi ngách.** Vì vậy mẫu B của market-k2 nhiều khả năng cũng lẫn kênh ngoài ngách ở mức tương tự. Đây là suy luận; tập kênh gốc đã mất.

**Ảnh hưởng lên chỉ số "kênh trẻ có nổ" của B** (đo trên mẫu 50; kênh trẻ < 730 ngày):

| Tập kênh trẻ | Nổ, định nghĩa gốc (≥ 3× trung vị ±90 ngày hoặc ≥ 3× người đăng ký) | Nổ + ≥ 10 nghìn lượt |
|---|---|---|
| Bộ lọc cũ cho qua (35) | 25/35 = **71 %** (KTC 58–82 %) | 2/35 = 6 % (2–16 %) |
| Đúng "không lộ mặt" (31) | 24/31 = 77 % | 2/31 = 6 % |
| Đúng "không lộ mặt" + đúng ngách B (19) | 14/19 = **74 %** (KTC 55–87 %) | **0/19 = 0 %** (0–12,5 %) |

- **Định nghĩa gốc:** nhãn sai **gần như không đổi** tỷ lệ (71 % → 74 %, KTC chồng nhau). Chỉ số b của market-k2 (B gộp 16/26 = 62 %) không bị thổi phồng đáng kể vì lỗi nhãn.
- **Thêm ngưỡng ≥ 10 nghìn:** hai kênh trẻ có video nổ đều **lệch ngách** (kỹ thuật, siêu dự án). Kênh trẻ đúng ngách B trong mẫu: **0/19**. Đây là tín hiệu xấu cho kỳ vọng "kênh trẻ B dễ nổ".
- **Giới hạn:**
  - Mức nổ chỉ tính trên 50 lượt tải lên gần nhất (trung vị 12,5 video dài/kênh); market-k2 đọc tới 6 trang. Tỷ lệ nổ ở đây vì vậy thấp hơn cách đo cũ.
  - Quần thể kênh là kênh của 12 đề tài channel-k2, không phải kênh của câu hỏi market-k2.
  - Không tính lại được đúng con số 16/26.

### 3. Cầu hiện hành 12 đề tài
- **72 câu hỏi** (12 × 6). **69 search.list mới**; 3 câu trùng nguyên văn lượt `labels` dùng lại cache. Thêm 151 lệnh đọc khác (khoảng 7 050 đơn vị). Vừa trong ngày, không cần chia ngày.
- Video ≥ 8 phút đăng trong 90 ngày, `regionCode=US`.
- **Bảng đầy đủ:** `HANG-DOI.md`, mục "Cầu hiện hành".
- **Mạnh (5):** factory town, malls, jet airliner, chips, retailers abroad.
- **Yếu (2):** supermarkets, card rewards.
- **Không (5):** container, card networks, Amazon warehouse, airlines, Dollar General.
- **Bước lọc liên quan là quyết định:** search trả nhiều video lạc đề (game show, Peppa Pig, động cơ tự chế). Không lọc thì 10/12 Mạnh.
  - **Chuẩn chính:** Sonnet chấm theo "đối thủ trực tiếp", viết trước khi có số.
  - **Chuẩn rộng** ("cùng ngành, cùng khán giả", chạy sau để đo độ nhạy) cũng ra **10/12**. Đổi nhãn ở chuẩn rộng: 5 đề tài lên Mạnh (container, Amazon, airlines, Dollar General, card rewards); card networks từ Không lên Yếu.

### 4. Kết quả luật quyết định (ghi nguyên, không đổi luật)
- **5/12 Mạnh → nhánh 3–5/12: TIẾP B.**
  - Hàng đợi chỉ giữ 7 đề tài Mạnh/Yếu.
  - Bổ sung đề tài mới cùng trụ có cầu hiện hành: 6 ứng viên có bằng chứng sơ bộ (`HANG-DOI.md`), **chờ đo đủ 6 câu ở ngày quota tới** (khoảng 36 search.list).
- **Chọn thí điểm:** nhánh 3–5/12 không quy định cách chọn. Tôi đề xuất **factory town**, điểm 27, theo cùng công thức của nhánh ≥ 6. Malls đạt 24 (`THI-DIEM.md` mục 0).
- **Độ nhạy:** ở chuẩn rộng, 10/12 thuộc nhánh ≥ 6, và thí điểm theo luật sẽ là **malls** (điểm 48).

### 5. Ưu, nhược, tác động, rủi ro
- **Ưu:**
  - Quyết định TIẾP B có hai phép đo độc lập ủng hộ (chuẩn chính và chuẩn rộng).
  - Hàng đợi và thí điểm nay dựa trên cầu đang có người xem.
  - Kiểm nhãn cho thấy chỉ số b theo định nghĩa gốc không bị lỗi nhãn làm lệch.
- **Nhược:**
  - Nhãn đề tài nhạy với chuẩn liên quan (5 so với 10).
  - Container, đề tài có cầu toàn thời gian lớn nhất, rời hàng đợi vì cầu nằm ở video cũ.
  - Tài chính–thanh toán chỉ còn 1/7.
  - Kênh trẻ đúng ngách B có nổ ≥ 10 nghìn: 0/19.
- **Tác động:**
  - Thí điểm đổi sang factory town; cần hồ sơ cầu `de-tai/factory-town.md` trước kịch bản.
  - Bộ cảnh ưu tiên: thị trấn sa bàn + nhà máy (thay cảng).
  - Ba hồ sơ container/jet/card networks: chỉ jet còn trong hàng đợi.
- **Rủi ro:**
  - Chọn theo cầu 90 ngày kéo kênh về thời sự: chips nghiêng tin EUV/nhà máy chip; retailers abroad dựa vào video phản ứng.
  - Factory town phụ thuộc một video 1,10 triệu.
  - Mẫu B của market-k2 có thể lẫn 44 % kênh ngoài ngách, nên các chỉ số khác của B ở market-k2 (top 5 chiếm, tài trợ) cũng mang sai số chưa đo.

### 6. Đang chờ chủ dự án
1. **Chuẩn liên quan:** "đối thủ trực tiếp" (5/12, cắt hàng đợi) hay "cùng ngành" (10/12, thí điểm ngay theo nhánh ≥ 6).
2. **Thí điểm:** factory town (đề xuất) hay malls.
3. Duyệt đo đủ 6 câu cho 6 ứng viên bổ sung (khoảng 36 search.list, ngày quota tới), và hồ sơ cầu factory town.
4. **Tài chính–thanh toán còn 1/7:** chấp nhận, hay ưu tiên đo "Tap to Pay".
5. Các mục chờ vòng 1 còn nguyên: tên kênh, giọng, nhạc, nhận diện.

---
## Vòng cuối: một thước "kênh mới có bật được không" cho A, B, D, J (11–12/10/2026)
Mọi chỉ số là **tự tính, không phải chỉ số YouTube**. Mã: `final.py`. Chỉ dùng một project/khoá YouTube của môi trường (Developer Policies III.D.1.c), không mượn khoá dự án khác.

**Thước**
- **Thước chính:** % kênh trẻ đúng ngách, không lộ mặt, có ≥ 1 video ≥ 8 phút đạt ≥ 10 nghìn lượt.
  - Kênh trẻ: tạo < 730 ngày trước 11/10/2026, lấy từ `publishedAt` của API.
  - Video tính: đăng 14–90 ngày trước 11/10/2026.
  - Mẫu số: chỉ kênh **có ít nhất một video dài** trong cửa sổ đó.
- **Thước phụ:** tỷ lệ có video ≥ 50 nghìn; trung vị lượt xem/video. KTC 90 % Wilson.
- **Tập kênh:** kênh có video ≥ 8 phút trong kết quả search.list 90 ngày, US.
  - B: 659 kênh của 72 câu cầu hiện hành, lấy từ cache.
  - A, D, J: 10 câu khán giả mới mỗi ngách.
- **Nhãn:**
  - Sonnet 5.5 gắn "không lộ mặt" và "đúng ngách" từ khoảng 10 tiêu đề gần nhất cộng mô tả kênh.
  - Opus 5.5 kiểm ngẫu nhiên 20 kênh trẻ mỗi ngách.

### B (đo ngay, 11/10, 528 đơn vị, 0 search.list)
| | Giá trị |
|---|---|
| Kênh ứng viên → kênh trẻ → trẻ đúng ngách + không lộ mặt → có video dài trong cửa sổ | 659 → 471 → 222 → **188** |
| **Thước chính: có video ≥ 10 nghìn** | **18/188 = 9,6 %** (KTC 90 % 6,6–13,7 %) |
| Có video ≥ 50 nghìn | 11/188 = 5,9 % (3,6–9,3 %) |
| Trung vị lượt xem/video (2 222 video) | **70,5**; trung vị của trung vị từng kênh: 45,8 |
| Opus khớp Sonnet (20 kênh) | 19/20 cả hai nhãn; 19/20 nhãn gộp "đúng ngách + không lộ mặt" |

- **n = 188 kênh**, vượt mục tiêu ≥ 30.
- **Sát ngưỡng:** 9,6 % nằm trong ±5 % quanh mốc 10 % của luật "cả 4 ngách < 10 %" (khoảng 9,5–10,5 %). Tôi nêu tên chỉ số này theo luật cứng của dự án.
- **Bỏ bước mở rộng** "kênh xuất hiện ≥ 2 lần": hạn mức hôm nay đã dùng khoảng 8 500/10 000 đơn vị trước vòng này, nên tôi giữ dự phòng.
- **Chi phí AI vòng cuối đến đây:** $2,56 (Sonnet $1,93; Opus $0,63).
- **Trần vòng:** chủ dự án nâng lên **$10** ngày 11/10; mã dừng ở $9. Ngày 11/10 lúc 20:00, chủ dự án nâng tiếp lên **$12**; mã dừng ở $11. A, D, J được gắn nhãn y như B: Sonnet 5.5, lô 25 kênh, Opus kiểm 20 kênh/ngách.
- **Không đổi** thước, luật hay model.
- **Ngách có dưới 30 kênh trẻ đúng ngách:** ghi n thật và nêu ảnh hưởng lên KTC. Không mở rộng quá 30 search.list.

### A, D, J, G: đo 12/10 (chủ dự án 11/10 20:00, thước không đổi)
| Ngách | Kênh ứng viên → trẻ → trẻ đúng ngách + không lộ mặt → có video dài trong cửa sổ | **Thước chính ≥ 10 nghìn** (KTC 90 %) | ≥ 50 nghìn | Trung vị lượt xem/video | Opus khớp Sonnet (20 kênh): cả hai nhãn / nhãn gộp |
|---|---|---|---|---|---|
| A Tiền/NH | 149 → 117 → 34 → 29 | 1/29 = **3,4 %** (0,8–14,1) | 0 % | 32 | 20/20 · 20/20 |
| B Doanh nghiệp (11/10) | 659 → 471 → 222 → 188 | 18/188 = **9,6 %** (6,6–13,7) | 5,9 % | 70,5 | 19/20 · 19/20 |
| D Bản đồ | 48 → 30 → 9 → 7 | 1/7 = **14,3 %** (3,3–45,2) | 0 % | 98,5 | **14/20** · 17/20 |
| G Ba tầng | 88 → 59 → 16 → 14 | 0/14 = **0 %** (0–16,2) | 0 % | 50 | 17/20 · 18/20 |
| **J Nhà ở & đô thị** | 94 → 65 → 8 → **6** | 3/6 = **50 %** (22,1–77,9) | 16,7 % | 415,5 | 19/20 · 20/20 |

- **Quota 12/10:**
  - A 1 130, D 1 041, J 1 075, G thêm 320 (3 câu mới; 7 câu cũ dùng cache), hiệu chuẩn khoảng 2 420.
  - Tổng khoảng **5 990/10 000** đơn vị; 57 search.list.
- **AI vòng cuối:** **$5,36** theo sổ: $2,56 của phiên trước, $1,92 đo A, D, J, G, Opus kiểm 6 kênh J, và REVIEWER Opus lượt 1 $0,79. Hiệu chuẩn chỉ dùng Sonnet, chi phí nhỏ, đã gồm trong sổ. Trần $12, mã dừng ở $11.

**Luật chọn (5 ngách A, B, D, G, J): J THẮNG theo luật.**
- *Điều kiện 1:* J có thước chính cao nhất, 50 %. J hơn B 40,4 điểm %, tức ≥ 10 → đạt.
- *Điều kiện 2:* cận dưới KTC của J là 22,1 %, lớn hơn cận trên KTC của B trừ 5 (13,7 − 5 = 8,7) → đạt.
- Luật "cả 5 ngách < 10 %" không áp dụng, vì J và D vượt 10 %.
- **Sát ngưỡng ±5 %:** B 9,6 % so với mốc 10 % (đã nêu ở vòng trước). Các so sánh của luật đều cách xa ngưỡng: 40,4 so với 10; 22,1 so với 8,7.
- **Cờ độ tin cậy, chủ dự án cần cân nhắc trước khi duyệt:**
  1. **n = 6.** Kết quả J dựa trên 3 kênh: CityWise (89,6 nghìn lượt, kênh 18 tháng tuổi, 10,6 nghìn người đăng ký), Harlan Braddock (47,2 nghìn) và Klyron (12,8 nghìn). Bớt một kênh là tỷ lệ còn 33 %, bớt hai còn 17 %. Wilson đã tính cỡ mẫu nhỏ, nhưng KTC vẫn rộng 22–78 %.
  2. **J đúng ngách chặt:** chỉ 11/65 kênh trẻ được chấm đúng ngách, và 8/65 đúng ngách + không lộ mặt. Mẫu tìm kiếm lẫn nhiều kênh nhà di động, tour căn hộ Tokyo và kể chuyện, nên phần "cầu" nằm ở vài kênh giải thích làm tốt.
  3. **Thước chưa hiệu chuẩn** (`CALIBRATION.md`): LL chỉ có n = 4 và chưa tới 28 ngày.
  4. **D:** Opus chỉ khớp Sonnet 14/20, nhãn D nhiễu nhất; n = 7.
  5. **Opus kiểm kênh quyết định:** mẫu Opus 20 kênh ngẫu nhiên chỉ trúng 1 trong 3 kênh có video ≥ 10 nghìn của J. Vì vậy tôi cho Opus kiểm thêm **cả 6 kênh J đang hoạt động**, kết quả khớp Sonnet **6/6** (cả hai nhãn).
  6. **Khung lấy mẫu khác nhau:** tập kênh của B lấy từ 72 câu cầu hiện hành theo đề tài; J (như A, D, G) lấy từ 10 câu khán giả. Phép so J với B không hoàn toàn cùng điều kiện.
  7. **Nhà máy:** vòng 1 chấm J 8 điểm, B 6. J có rủi ro chính trị hoá (zoning, đường cao tốc và khu dân cư da màu) và trùng Crux 13 % (market-k2 vòng 1).
- **Theo chỉ dẫn, ngách đổi nên HANG-DOI và THI-DIEM có thêm mục *nháp* J.** Mục này chờ chủ dự án duyệt và ghi vào `AUTHORSHIP.md`. Phần B giữ nguyên bên dưới.

**G, đủ 10 câu (gộp mẫu 11/10):**
- **Thước chính:** 0/14 (0 %, KTC 0–16,2 %).
- **Khung âm mưu:** 3/59 kênh trẻ (đếm riêng). Video top 20 khung âm mưu chiếm **1/20 = 5 %** (KTC 1,1–19,6 %). Opus khớp Sonnet về khung âm mưu 19/20. G không thắng nên cờ "> 50 %" không cần bật.
- **Cầu theo tầng:**
  - **Tầng 2** có 7/20 video top với 2,9 triệu lượt (một video 1,22 triệu), nhưng là tin Nga, trừng phạt và đồng đô la, rất thời sự.
  - **Tầng 1** có 8/20 video top với 232 nghìn lượt, chủ yếu cụm Rothschild. 14/16 kênh trẻ đúng ngách nằm ở tầng này nhưng chưa kênh nào có video ≥ 10 nghìn.
  - **Tầng 3** yếu: 4/20 video top, video cao nhất 14,6 nghìn lượt.
- **Kênh trẻ làm hàng loạt:** 5/16 kênh có nhịp ≥ 12 video/28 ngày; 2/16 có khuôn tiêu đề lặp; 6/16 có ít nhất một trong hai.
- **CPM công khai** (ghi là CPM, xem mục đo nhanh): Personal Finance 18–45, History 5–12, Crypto 12–25 USD. Không có dòng địa chính trị.

**Hiệu chuẩn bằng LL:** xem `CALIBRATION.md`.
- 8 đề tài, chỉ tập 6 có nhãn Yếu; tập 6 cũng có lượt xem/ngày cao nhất (48 so với ≤ 4).
- ρ = 0,77 với n = 4, mẫu rất nhỏ. Mức tin cậy của thước: thấp, chưa kiểm được.
- Khuyến nghị dùng hồ sơ cầu làm **bộ lọc phụ** khi chọn tập 9 của LL.

**Đang chờ chủ dự án:**
1. **Duyệt hoặc không duyệt J làm ngách kênh 2.** Luật chọn J; các cờ n = 6 và thước chưa hiệu chuẩn nêu ở trên. Có thể duyệt kèm điều kiện đo cầu 6 câu cho hàng đợi J (khoảng 3 600 đơn vị), hoặc giữ B.
2. Ghi quyết định vào `AUTHORSHIP.md`.
3. Dùng hồ sơ cầu cho tập 9 của LL ở vai trò bộ lọc phụ hay không.

### G "Quyền lực kinh tế qua ba tầng": đo nhanh tối 11/10 (mẫu nhỏ, chưa so luật)
> **Đã có số mới hơn:** mục "A, D, J, G: đo 12/10" bên dưới (G đủ 10 câu, có Opus kiểm) thay cho số tầng và khung âm mưu ở mục này.

Mọi chỉ số là **tự tính, không phải chỉ số YouTube**. Mã: `final.py G --nq 7 --noaudit`.

**Câu hỏi:** 7/10 câu (3 câu tầng 1, 2 câu tầng 2, 2 câu tầng 3). Câu hỏi nằm trong `G_Q`, không trùng câu của A.

**Nhãn:** Sonnet 5.5 gắn như các ngách khác, thêm ba trường:
- *khung âm mưu*: kênh này không tính là đúng ngách, đếm riêng;
- *tầng*: 1, 2, 3 hoặc nối tầng;
- *khuôn tiêu đề*.
Opus chưa kiểm; sẽ kiểm 20 kênh ở lượt đủ 10 câu.

**Quota:** 7 search.list + 51 lệnh đọc = 751 đơn vị. Thêm 5 đơn vị tìm kênh LL. Theo ước tính (phiên trước ghi khoảng 9 030 đơn vị đã dùng), ngày 11/10 còn khoảng 210, tức vẫn trên mức dự phòng 100.

**Chi phí AI:** $0,26. Sổ vòng cuối $2,82, gồm $2,56 phiên trước ghi theo REPORT. Trần $12, mã dừng ở $11.

| | G (7 câu) |
|---|---|
| Kênh ứng viên → kênh trẻ → kênh trẻ đúng ngách, không lộ mặt, không khung âm mưu → có video dài trong cửa sổ | 59 → 40 → **15** → 14 |
| Thước chính: kênh có video ≥ 10 nghìn | **0/14 = 0 %** (KTC 90 % 0–16,2 %) |
| Trung vị lượt xem/video (137 video) | 50 |
| Kênh trẻ mang khung âm mưu (đếm riêng) | 2/40 |
| Video top 20 mang khung âm mưu (Sonnet) | **1/20 = 5 %** (1,1–19,6 %) |
| Kênh trẻ đúng ngách theo tầng 1 / 2 / 3 / nối tầng | 13 / 1 / 0 / 1 |
| Video top 20 theo tầng 1 / 2 / 3 / nối tầng (tổng lượt xem) | 10 (233 nghìn) / 6 (722 nghìn) / 3 (27 nghìn) / 1 |
| Kênh trẻ làm hàng loạt: nhịp ≥ 12 video/28 ngày / khuôn tiêu đề / cả hai | 5 / 2 / 1 trên 15 |

- **Cầu theo tầng.** Tầng 2 có lượt xem lớn nhất, nhưng gần như toàn tin thời sự Nga và trừng phạt. Tầng 1 có cầu vừa và nằm gần hết ở cụm Rothschild (95 và 90 nghìn lượt). Kênh trẻ dồn vào tầng 1 nhưng chưa kênh nào đạt 10 nghìn. Tầng 3 yếu: cao nhất 14,6 nghìn lượt.
- **Nhãn âm mưu cần Opus kiểm.** Vài tiêu đề ở cụm Rothschild ("The Secret World of…", "…Owns No Country But Bankrolled Them All") được Sonnet chấm *không* âm mưu, nên con số 5 % có thể thấp hơn thực tế.
- **CPM công khai** (ghi là CPM, không phải RPM; G là ngách ghép, chưa có dòng riêng):
  - [OutlierKit 13/09/2026](https://outlierkit.com/resources/youtube-niches-guide/): Personal Finance & Investing 18–45 USD, History & True Crime 5–12 USD, khán giả Mỹ.
  - [upGrowth, sửa 17/09/2026](https://upgrowth.in/youtube-cpm-overview-highest-paying-niches-2026/): Cryptocurrency & digital assets 12–25 USD (ước tính, không nêu vùng).
  - Không nguồn nào có dòng tin tức/địa chính trị.

**REVIEWER Opus (lượt 1, $0,79, served `claude-opus-5-5` + Haiku phụ):**
- R1 phỉ báng, R2 YMYL/âm mưu, R3 dữ liệu, R4 áp luật, R6 hiệu chuẩn: **PASS**. R5 khớp số: **FAIL**.
- **Đã sửa:**
  - Số search.list: 67 → 57.
  - "8/65 đúng ngách": nay là 11/65 đúng ngách, 8/65 đúng ngách + không lộ mặt.
  - Thêm cờ: Opus chưa kiểm 2/3 kênh quyết định của J, nên đã cho Opus kiểm cả 6 kênh (khớp 6/6).
  - Thêm cờ khung lấy mẫu B khác J.
  - Ghi nguồn trần $12.
  - Đánh dấu mục G đo nhanh đã có số mới hơn.
  - Lưu danh sách video tìm kiếm của J làm bằng chứng cho hàng đợi nháp, ở `final_J_search_long.json`, ngoài git.
- Không chạy lượt 2.
