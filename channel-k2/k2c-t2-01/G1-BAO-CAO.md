# K2C-T2-01 "Shipbuilding" — BÁO CÁO CỔNG G1 (phiên T2, 15/10/2026) — DỪNG chờ chủ dự án

> Tập kênh 2 "Moving Parts" thứ hai theo Kinh thánh (`docs/BIBLE-KENH2.md`), tập bóng; áp Mốc A (Đóng gói) và Mốc B (Đạo diễn; Dựng chạy sau G1). Nhánh **`k2c-t2`** (đẩy cả `ccr-bef6f172-fcqat9`). Mọi chỉ số thị trường là **tự tính, không phải chỉ số YouTube**. Mức rủi ro đề tài: **VÀNG** (địa chính trị gần đây).

## 0. Tóm tắt một màn hình
| Hạng mục | Kết quả |
|---|---|
| Bước 0 | `origin/main` đúng @650f05b → fast-forward `k2-visual4` @b9a1368 vào `main`; AUTHORSHIP "V4 DUYỆT 15/10 (H1–H6)" (`main` @f5ea7726); nhánh `k2c-t2` từ `main` mới |
| Bước 0b | Kinh thánh sửa **đúng 3 chỗ** nguyên văn lệnh (footage ≥ 720p/khung trong khung + DVIDS; xu có độ dày; §8 cổng hình G2) — diff 3 dòng |
| Bước 0c | Hàng xu dày 0,42 r + cạnh khía + gờ mặt; máy thấp (tilt ≥ 55°) ở shot số liệu; hộp né nhãn theo mép trước đồng xu; footage **khung trong khung** (nguồn < 720p: giữ tỉ lệ, phóng ≤ 1,5×, viền + bóng, nền là clip mờ tối). `test_k2v.py` **25/25 ĐẠT** (+2 test mới) |
| Đề tài khuyến nghị | **A. Đóng tàu Mỹ ↔ Hàn Quốc ↔ Trung Quốc** — "America once built three cargo ships a day; why so few now?" |
| Tiêu đề chính đề xuất | **Why America Builds So Few Ships (It's Not Just Wages)** (REVIEWER: ĐẠT nguyên văn) |
| Lời | **v3.2**: 1 616 từ ≈ **10:41** (Eric 151,2 từ/phút), móc ≈ 31 s, 7 đoạn, 6 nhân vật/nhóm có hồ sơ; 56 claim (≥ 50 ✔P trên tệp gốc) |
| Kiểm | 3 vòng người đọc mù (3 vai Sonnet) + 3 vòng REVIEWER Opus: major 23 → 6 → 5, block 2 → 0 → 0; 5 major vòng 3 sửa bằng **đúng chữ REVIEWER** (K8), không chạy vòng 4 |
| Chấm "xem tiếp" (Mốc A) | **3/3 xem tiếp** (tự tin 6/7/6), bấm tiêu đề 8/8/7; 3/3 chọn motif "phiếu đơn hàng" + bãi Ulsan + vòng lặp xu là điểm hay nhất; đã sửa 1 vòng theo góp ý 3/3 |
| Khoảnh khắc đinh | 3, có khung phác 540p dựng thật bằng k2v (`phac/`) |
| Chi phí API (`claude -p`, cùng định nghĩa T1) | **$3,79** tới G1 (trần T2 $11; T1 G1a $7,74) — Đóng gói $0,62 · Biên kịch $3,16 · Đạo diễn $0 |
| YouTube Data API | **≈ 216 / 300 đơn vị** |
| ElevenLabs | 0 ký tự (chưa thu) |

## 1. Bước 0 – 0c
- **Merge:** `origin/main` = 650f05b0 (đúng điều kiện), `git merge --ff-only origin/k2-visual4` → b9a13682; thêm dòng AUTHORSHIP (commit f5ea7726, đã đẩy `main`). Nhánh tập `k2c-t2`, thư mục `channel-k2/k2c-t2-01/`.
- **Kinh thánh:** 3 chỗ, nguyên văn lệnh; `git diff` chỉ 3 dòng (commit trên `k2c-t2`). Không sửa gì khác.
- **0c — hàng xu** (`design/k2v/relief.js`): xu trong `layout: row` dày 0,42 r (chồng xu giữ 0,24 r), cạnh khía 96 răng (bumpMap), gờ nổi trong mặt; đặc tả shot số liệu dùng tilt 58–61° (thấp hơn V4 40–43°). Lỗi phụ phát hiện khi rà khung thử và đã sửa: nhãn "1/10" chạm hàng xu khi máy thấp (hộp né tính từ điểm neo, chưa tính mép trước đồng xu). So sánh: `phac/0c-hang-xu-v4-vs-t2.jpg`. Giờ dựng 1080p SPP2: **2,77 s/khung** (T2) vs 2,55 (V4, cùng máy, đều có tải song song) → **+8,6 %** — trong phạm vi nhiễu chưa xác định, đo lại ở 1080p tập thật.
- **0c — footage khung trong khung** (`scripts/k2/hero.js`): `frame: 'auto'` (mặc định) bật khi chiều cao nguồn sau crop < 720; phóng ≤ `maxScale` 1,5; viền giấy `#f1e4c6` + bóng; nền = chính clip phủ kín, mờ + tối; chỉnh màu kênh áp sau cùng (cả viền). Test bằng clip tổng hợp 480×360 (ra khung 720×540, ×1,5) và 1280×720 (phủ kín như cũ).
- **Sửa thêm trong bộ công cụ (cần cho tập, ghi ở VERSIONS):** `relief_build.py --dem skadi` (SRTM 1″ ngoài Mỹ, USGS tài sản công — nền Hàn Quốc dựng được); đệm NaN cho ô 3DEP ven biển lệch cỡ (lỗi chặn khi dựng nền Vịnh SF); **`lib/k2.js` nhãn ESTIMATE** — trước đây mọi loại số không phải "projection" đều in **ACTUAL** (lỗi nhãn sai loại, cùng họ BAI-HOC LL #4; phát hiện ở khung phác); 3 đạo cụ mới `freighter`, `crane`, `order`.
- **`checks/lock.py --verify`: KHỚP** (`c598467f…`); không sửa, không đọc mã `checks/`.

## 2. Đóng gói — đề tài (`DONG-GOI.md`)
- **Hồ sơ cầu:** 1 `search.list` cho đề tài khuyến nghị + quét kho 3 788 video của 10 kênh cùng dạng + toàn bộ 55 video của 2 đối thủ trong Kinh thánh (lý do chỉ 1 search: 3 lượt sẽ vượt 300 đơn vị — ghi rõ ở hồ sơ).
- **Loại trừ:** GoDocs đã làm Panama, Suez; Fortune of Nations đã làm Ireland, Thuỵ Sĩ, Mỹ–Mỹ Latin…; Wendover vừa làm Botswana (30/09/2026, ≈ 1,02 triệu).
- **Ba ứng viên:** A **đóng tàu** (VÀNG, cầu đo được: Cầu-bền 3,21 triệu; neo: phí cảng tạm hoãn tới **9/11/2026**) · B ca cao Tây Phi (VÀNG; neo EUDR 30/12/2026; cầu chưa đo) · C Houston–Galveston (XANH; trùng trụ thành phố với T1; cầu chưa đo).
- **Khuyến nghị A**, vì: cầu đo được + khoảng trống đọc từ bình luận (phản bác "lương rẻ" trọng số 17 301; "Hàn Quốc bắt đầu khi còn nghèo" 2 717; đòi bàn tài chính 277); hạn chót có thật trong 4 tuần; đúng lời hứa kênh (Richmond, Ulsan là **nơi** giàu lên nhờ xưởng tàu); nhân vật có hồ sơ; hình tài sản công dồi dào.

## 3. Gói — tiêu đề, brief, Test & Compare (`PACKAGING-BRIEF.md`, `titles-thumbs.md`)
| # | Tiêu đề | REVIEWER (Opus) |
|---|---|---|
| 1 | **Why America Builds So Few Ships (It's Not Just Wages)** — khuyến nghị chính | ĐẠT nguyên văn |
| 2 | In 1943, America Launched 3 Ships a Day. Why Does It Build So Few Now? | ĐẠT sau khi thêm "In 1943", "launched" |
| 3 | From Richmond to Ulsan: Why America Builds So Few Ships | bản sửa của REVIEWER (bản cũ hứa quá, khung đối đầu quốc gia) |
- **Tham chiếu:** 6 thumbnail thắng trong ngách mô tả bằng lời (ảnh chỉ xem tạm ở scratch, không vào repo).
- **Thumbnail của mình:** T-B (khuyến nghị, REVIEWER chọn; không chữ, ảnh OWI 1943 cắt theo thân tàu/đèn hàn, mặt không làm tiêu điểm ↔ ụ tàu 3D) · T-A (hai số đều đặt ở bờ Mỹ, ghi rõ cơ sở) · T-A′ (phiếu đơn hàng rơi xuống bãi trống). Bỏ T-C (4× là ước của một hãng cho một loại tàu).
- **Test & Compare:** tiêu đề 1 + 3 thumbnail; thước = chỉ số YouTube chọn + CTR 7 ngày so T1; vòng 2 thử tiêu đề 1 ↔ 2 (nếu có).
- **Mô tả nháp** 2 235 ký tự (≤ 5 000), nguồn đầy đủ ở bình luận ghim (`MO-TA-NHAP.md`); giờ chương là ước, khớp lại sau thu giọng.
- **Ý 1 Short:** "The order comes first" — 3 nhịp, 3 bờ biển (Richmond 1940 · Ulsan 1972 · Philadelphia 2026), cùng góc máy, mọi câu có claim.

## 4. Biên kịch + kiểm chứng (`script.md` v3.2, `claims.md`)
- **Cấu trúc:** 00 Móc · 01 Kaiser (Richmond; thợ hàn **Josie Lucille Owens**, ảnh OWI 1943) · 02 Jones (Jones Act; phía ủng hộ AMP ↔ phản đối Lee–McClintock; trợ cấp chấm dứt 1980s) · 03 Huyền thoại "lương" vs hồ sơ (vòng lặp giá cao → ít đơn → không có quy mô) · 04 Chung Ju-yung (Ulsan, "theo lời công ty"; truyện tờ 500 won gắn nhãn **lore**; chính sách 1973 của nhà nước Hàn Quốc + phát hiện TFP không tăng) · 05 Hiện tại (5 công đoàn kiến nghị → USTR → phí → tạm hoãn sau thoả thuận Trump–Xi; Bộ Thương mại TQ phản hồi; Hanwha Philly) · 06 Kết (3 điều cần theo dõi, bảng điểm, quay về Richmond, dẫn tập sau "containers").
- **Kiểm chứng:** 56 claim; nguồn gốc tải bằng curl/pdftotext và **grep nguyên văn** (✔P): Federal Register (3 thông báo), CRS (3 báo cáo), Maritime Commission 1945, NPS (4 trang), LoC, World Bank, HHI, KEIA, báo có biên tập. Hai tác tử Sonnet tra sơ bộ; mọi trích then chốt P kiểm lại. Không dùng: tổng 5 777 tàu (OCR hỏng), số đếm tàu 2022 (khác định nghĩa), GRDP Ulsan (chưa đọc KOSIS), $2 tỷ hợp đồng MRIV (ước), "70 ships a year 1975" của USTR (khác định nghĩa CRS).
- **Kiểm mù + REVIEWER:**

| Vòng | Móc (R1/R2/R3) | Nhân vật | Tin cậy | Nghiêng phe | REVIEWER block / major / minor |
|---|---|---|---|---|---|
| v1 | 8/8/8 | 6/6/5 | 7/7/6 | không (3/3) | 2 / 23 / 19 |
| v2 | 6/7/6 | 4/5/5 | 8/8/7 | không | 0 / 6 / 35 |
| v3 | 6/8/6 | 5/6/5 | 7/8/7 | không | 0 / 5 / 27 |
- Sửa lớn theo ≥ 2/3: v1→v2 bỏ đoạn "honest part" đứng riêng (đưa giới hạn vào chỗ từng số), thêm hỗ trợ nhà nước Hàn Quốc cho cân xứng với TQ; v2→v3 thêm nhân vật Owens, chương TQ gộp vào "hiện tại" với chủ thể 5 công đoàn; v3.1 áp đúng chữ REVIEWER cho 5 major; v3.2 rút móc theo chấm "xem tiếp".
- **Móc giảm 8 → 6–7 khi thêm thủ tục** (miễn trừ, chi tiết phí) theo REVIEWER; v3.2 đã chuyển miễn trừ + "as of" lên chữ trên hình 0:03–0:12 (xem việc chờ #3). Lời v3.2 **chưa** qua người đọc mù lần nữa (hết ngân sách 1 vòng sửa theo chấm "xem tiếp").

## 5. Đạo diễn — treatment (`TREATMENT.md`, Mốc B)
- **Ý đồ:** ba bờ biển cùng cách quay (Richmond · Ulsan · Philadelphia). **Motif xuyên tập:** "đơn hàng đến trước xưởng" — phiếu `order` (kem, dấu đỏ) rơi xuống bản đồ trước khi cẩu và tàu mọc (1940 Anh → Richmond; 1944 phiếu cuối tan; 1972 Livanos → bãi trống Ulsan; 2026 Lầu Năm Góc → Philadelphia). Motif phụ: vòng lặp nét đứt. Mã màu: Mỹ ngọc · Hàn hổ phách · TQ tím xám (tránh đỏ). Sepia 1920–1974 ↔ tự nhiên 1999–2026.
- **Đường cong cảm xúc:** 7 → 8 (đỉnh Peary) → 4 → 6 → 8 (Ulsan) → 7 → 5 (bảng ở `TREATMENT.md` §2).
- **Bảng hình theo câu:** ~64 biến cố/656 s ≈ 1 biến cố/2,6 s; footage ước ≈ 3,4 % (≤ 20 %); hồ sơ thật ≈ 11 % (Kinh thánh 10–15 %). Sau chấm "xem tiếp" (2/3): bỏ hai màn chia đôi tĩnh ủng hộ/phản đối, thay bằng trích dẫn bám vật trên bản đồ.
- **Khoảnh khắc đinh (khung phác 540p, dựng thật bằng k2v):**

| | Mô tả | Khung |
|---|---|---|
| Đ1 "Bốn ngày rưỡi" | Vịnh SF sepia, máy thấp; 3 cột thép tỉ lệ thật 122 → 39 → 4½ ngày; tàu Liberty 3D hạ thuỷ | `phac/D1-bon-ngay-ruoi.jpg` |
| Đ2 "Vòng lặp" | hàng xu dày (bản 0c): 1 "world price" ↔ 4 "U.S.-built tanker" (nhãn ESTIMATE, "one firm's estimate"); vòng nét đứt chảy nối xu → phiếu mỏng → cẩu đứng | `phac/D2-vong-lap.jpg` |
| Đ3 "Bãi biển trống" | relief Hàn Quốc (SRTM) sepia; phiếu Livanos rơi xuống bãi trống Ulsan → cẩu → tàu; (G1b: chuyển sepia → tự nhiên + tầng ảnh xưởng hôm nay) | `phac/D3a-phieu-roi-bai-trong.jpg`, `phac/D3b-xuong-moc.jpg` |
- **Đạo diễn tự rà khung phác** (sửa ở G1b): nhãn "Richmond" che một phần cột 39 ngày; dải trắng ở bờ Ulsan do đường bờ Natural Earth lệch DEM SRTM ở tầm ~30 km; cột Đ1 còn che nhau một phần theo chiều sâu.

## 6. Chấm mù "xem tiếp" (Mốc A; `kiem-mu/dong-goi_xt1-J*.json`)
- 3 người chấm (Sonnet ghim, thư mục trống) đọc móc ~45 s (v3.1) + treatment 1 trang tiếng Anh (`xemtiep/treatment-en.md`) + tiêu đề 2.
- **Kết quả:** xem tiếp **3/3** (tự tin 6/7/6); bấm tiêu đề 8/8/7. Hay nhất: motif "đơn hàng đến trước xưởng" (3/3 nêu, J1 kèm bãi Ulsan + vòng lặp xu, J2 kèm cột ngày Richmond, J3 phiếu rơi + chuyển sepia → màu).
- **Chỗ muốn bỏ (≥ 2/3):** câu miễn trừ + "facts as of" + đoạn hạn phí trong 45 s đầu (**3/3**) → **đã sửa** (v3.2); màn chia đôi ủng hộ/phản đối "như giờ công dân" (2/3) → **đã sửa** ở treatment. Một vòng sửa, đúng giới hạn lệnh.

## 7. Rủi ro
- **Trạng thái mở có thể đổi trước khi thu giọng (BAI-HOC-K2 K2):** phí Section 301 hết tạm hoãn 9/11/2026 — nếu video đăng sau 9/11, chương 00/05/06 phải viết lại theo trạng thái mới. federalregister.gov và congress.gov chặn phiên (403) → tra lại bằng govinfo trước khoá lời và trước thu.
- **VÀNG:** chủ đề Mỹ–TQ, Mỹ–Hàn; giảm bằng hai phía có nguồn riêng ở mọi điểm tranh chấp, "as of", không đánh giá chính sách/công ty, không cờ/logo/mặt làm tiêu điểm.
- **Lời kể công ty:** câu chuyện Hyundai dựa chủ yếu vào lịch sử tự thuật (HHI) — đã gắn nhãn "by the company's account"; truyện tờ 500 won gắn nhãn lore.
- **Móc lệch Kinh thánh §3:** thứ tự "nghịch lý trước, tin sau" (theo 3/3 người chấm) và câu miễn trừ chuyển lên chữ trên hình — cần chủ dự án quyết (việc chờ #2, #3).
- **Bản đồ ngoài Mỹ:** SRTM + Natural Earth lệch bờ ở tầm gần; tầng ảnh hàng không Ulsan/Philadelphia phải là ảnh có giấy phép (Commons CC0/CC BY-SA, kiểm biển hiệu từng tệp).
- **Footage:** NARA Liberty 640×480 → khung trong khung (đã có công cụ); clip Bancroft "prefabricated ship" bản quyền chưa rõ → **không dùng**.
- **Chỉ số trong ±5 % quanh ngưỡng:** thời lượng lời 10:41 (ngưỡng 11:00, −2,9 %) và v3.1 10:59 (−0,1 %); móc v3 46,4 s (ngưỡng 45 s, +3 %) — đã rút còn ~31 s ở v3.2.

## 8. Chi phí đến G1 theo vai (sổ `so-vai.jsonl`, `kiem-mu/cost.jsonl`; `vai.py sum`)
| Vai | API `claude -p` (USD, đo) | Lượt | Token phiên (sinh ra / ghi cache / đọc cache) | Quy đổi giá niêm yết phiên (ước) |
|---|---|---|---|---|
| Đóng gói | **$0,62** (gắn nhãn bình luận Haiku $0,03, tổng hợp Sonnet $0,11, REVIEWER tiêu đề Opus $0,32, chấm "xem tiếp" $0,16) | 9 | 64 k / 146 k / 24,8 M | ~$14,9 |
| Biên kịch + kiểm chứng | **$3,16** (3 vòng × [3 người đọc + REVIEWER]) | 12 | 57 k / 296 k / 21,6 M (gồm 2 tác tử tra nguồn) | ~$12,8 |
| Đạo diễn | **$0** (làm trong phiên) | 0 | 72 k / 147 k / 34,1 M | ~$19,8 |
| Dựng | — (sau G1) | — | — | — |
| P (điều phối, Bước 0–0c) | $0 | — | 30 k / 174 k / 9,3 M | ~$6,5 |
| **Tổng** | **$3,79 / trần $11** | 21 | | ~$54 |
- **So mốc gốc T1:** T1 tính $9,06 cho cả tập chỉ gồm `claude -p` (G1a $7,74). T2 đến G1: **$3,79** (−51 % so T1 G1a) dù thêm Đóng gói + chấm "xem tiếp".
- **Giới hạn phép đo:** cửa sổ vai đánh dấu bằng giờ (`vai.py mark`) nên phần việc công cụ (0c, SRTM, đạo cụ, khung phác) rơi vào cửa sổ Đóng gói/Đạo diễn; token phiên chủ yếu là **đọc cache** nạp lại ngữ cảnh mỗi lượt. Quy đổi phiên là ước theo bảng giá, không phải hoá đơn; T1 không đo phần này nên **chưa so được**. Đề xuất: từ G1b tách công cụ thành cửa sổ riêng "công cụ".
- **Giữ/bỏ vai (luật lệnh: bỏ nếu +25 % chi phí không đo được lợi):** chưa đủ dữ liệu ở G1. Lợi đo được: Đóng gói (chọn đề tài có cầu đo; REVIEWER tiêu đề bắt 2/3 tiêu đề và 3/3 thumbnail có lỗi cơ sở số); chấm "xem tiếp" phát hiện 3/3 lỗi móc mà REVIEWER không bắt (REVIEWER đẩy theo hướng thêm thủ tục). Quyết ở G2 khi có CTR/thời gian xem.
- **Giờ máy:** nền bản đồ 3 vùng (~10 phút), shot thử xu 2 × 8 phút (1080p SPP2), khung phác 540p 2 lượt (~12 + ~10 phút).

## 9. VERSIONS (`VERSIONS.md`)
checks **1.10.2** + LOCK `c598467f…` (KHỚP); bộ k2v sau 0c tại commit G1 của `k2c-t2`; model: phiên (claude-opus-5-5 theo cấu hình), kiểm `claude -p` ghim (Sonnet/Opus/Haiku 5.5, model chạy thật ghi ở `served`); Claude Code 2.1.300; giọng Eric `cjVigY5qzO86Huf0OWal`, `eleven_multilingual_v2` (như T1).

## 10. Việc đang chờ chủ dự án (G1)
1. **Duyệt đề tài A (đóng tàu), mức VÀNG.** (Thay thế: B ca cao, C Houston.)
2. **Thứ tự móc:** giữ v3.2 (nghịch lý số → công ty Hàn ở Philadelphia → câu hỏi → một câu nhắc hạn 9/11; 31 s) theo 3/3 người chấm, **lệch** công thức Kinh thánh §3 (tin mới trước) — duyệt lệch, hay quay về "tin trước".
3. **Câu miễn trừ:** chuyển từ lời sang **chữ trên hình 0:03–0:12** + đầu mô tả (LUAT-G §4 yêu cầu "trong 30 s đầu"; §5 cho "as of" trong lời hoặc trên hình). T1 nói bằng lời. Duyệt cách này, hay giữ lời nói (móc yếu hơn theo 3/3).
4. **Lời v3.2 làm lời khoá ứng viên** — hoặc yêu cầu thêm một vòng người đọc mù trên v3.2 (≈ $0,25) trước khi khoá.
5. **Tiêu đề chính:** đề xuất tiêu đề 1; thumbnail T-B làm mặc định Test & Compare.
6. **Ghi AUTHORSHIP** các quyết định G1 (P ghi sau khi chủ dự án duyệt).
7. Sau duyệt: G1b tờ khung 540p (gồm Đ1–Đ3, sửa 3 lỗi tự rà), relief `pnw`/`eastus`, đạo cụ `truck`; tra lại trạng thái phí cảng trước khoá lời và trước thu giọng.
