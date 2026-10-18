Nhánh thật: `pt3-van-nuong` (đẩy được đúng tên lệnh) — cùng commit đẩy song song lên `ccr-7dba50bc-8tnqaq` (nhánh harness gán). Tạo từ `origin/claude/pt-khung-neo-ab-test-njr9wp` @ `7adb88fa`.

# PT3 — Chi tiết AI cho cảnh MÁY CHUYỂN ĐỘNG: vân nướng (HC7) và tấm chiếu (HC8) — BÁO CÁO

> Phiên R&D PT3, 18/10/2026, theo lệnh chủ dự án (duyệt HC1–HC6, N1–N4, HC7–HC9 ngày 18/10). **Không merge. DỪNG chờ chủ dự án.**
> Mọi số là số đo thật trong phiên (tệp ở `reports/pt3/`) hoặc ghi rõ **(ước)**. Không có email, không có khoá API trong repo/báo cáo.

## 0. Khối điều lệ (lệnh + thực tế)
| Trường | Lệnh | Thực tế |
|---|---|---|
| Loại phiên | R&D PT3 | đúng |
| Nhánh | `pt3-van-nuong` từ `origin/claude/pt-khung-neo-ab-test-njr9wp` @7adb88f | đúng; thêm bản đẩy lên nhánh harness `ccr-7dba50bc-8tnqaq` |
| Tệp được sửa | CHỈ `design/pt3/**` + `reports/pt3/**` | chỉ hai vùng này. `design/pt/` chỉ **đọc + chép** (bản sao có ghi nguồn trong `design/pt3/scene/build_pt3.py`, `pt_site.py`); ghost SH đọc bằng `git show` ra `/var/tmp/pt3/ghost/`; `scripts/`, `checks/`, `docs/`, `channel-*` chỉ đọc; không đọc mã `checks/` |
| Trần API | Claude ≤ $3 · OpenAI ≤ $15 · YouTube 0 · ElevenLabs 0 | **$1,170** (15 phiếu chấm mù) · **$8,906** (133 lệnh) · **0** · **0** |
| Giờ máy | ≤ 6 h | **≈ 3,4 h** (2,71 h có sổ `log/gio-may.jsonl` + ≈ 0,7 h ước cho dựng thử/nướng/đo không ghi sổ) — §8 |
| Preflight | bắt buộc; che email; không in/ghi khoá | hook pre-commit (`tools/preflight.sh`) cài đầu phiên; mọi commit **ĐẠT**; khoá OpenAI do proxy gắn (mã không đọc biến khoá); khoá Claude chỉ qua biến môi trường cho `claude -p` |
| Video / ảnh | 540p ≤ 15 MB, không LFS; ảnh ≤ 40 MB | 5 video 960×540 **7,3 MB**; ảnh **39,47 MB** (trong đó ảnh AI gốc bắt buộc lưu 33,5 MB) — sát trần, §10 |
| Dừng | không dừng hỏi giữa chừng | không dừng; các quyết định không chặn đã tự quyết, liệt kê §11 |

## 1. Tóm tắt (đọc 2 phút)
1. **HC7 (vân nướng gắn hình học) giữ được tính nhất quán tuyệt đối khi máy bay.** Nhấp nháy đo bằng chiếu ngược khung t → t+1 trên vùng có vân AI: orbit **A 2,56 / HC7 2,71** (thang 0–255; +6 %), phố **A 2,17 / HC7 2,20** (+1,5 %); tỉ lệ điểm "chớp" (|Δ| > 12) orbit 0,90 % → 1,52 %, phố 2,05 % → 2,16 %. Phần tăng nhỏ đến từ vân chi tiết hơn (răng cưa lấy mẫu), không phải vân đổi giữa khung. Nhất quán đầu↔cuối orbit: HC7 ΔY 5,8–5,9 (A 4,6–7,0).
2. **HC8 (chiếu 3 tấm C từ góc chính) KHÔNG đạt.** (a) **Kiểm dữ kiện trượt**: cả 3 tấm C ở cả 2 lần thử đều **xoá tường chắn + lỗ châu mai** của bastion (Drinkwater 1786 có), xoá dãy khối Line Wall + pháo, **dời/phóng đường bao** (chân tường lệch TB **39–60 px**, p90 91–123 px ở 1080p). (b) Nhấp nháy **5,61** (2,2× A), **9,5 %** điểm chớp; nhất quán giữa↔cuối ΔY **58** (A 5,5). (c) Cung máy còn đứng (lộ mặt khuất ≤ 1 %): **241,7°–299,3°** (≈ ±29° quanh góc chính 270°, tức cung chiếu ±25° + 4°); ≤ 5 %: 226,8°–318,1°; ngoài đó lộ tới 69–97 %.
3. **HC7 có rủi ro "AI bịa bố cục" phải chặn bằng máy + rà mắt.** Gặp và chặn được 5 kiểu lỗi chắc: AI **vẽ cửa sổ/cửa/đá góc giả lên tường trơn** (khi ảnh mẫu là mặt tiền có cửa, và cả khi prompt nói "mặt tiền nhà 3–4 tầng"); **xoá đá góc, gờ, bậu + vẽ ống thoát nước** (khi mặt nạ gồm phần nhô); **co/dời khung + vẽ thêm tường chắn** (bastion); **tô đen nửa tường** (8 khúc phố); **bịa cả mặt bằng mái/ngõ** ở **15/15 ô nhìn-từ-trên của phố**. Sau khi sửa quy trình: dùng **47/55 khúc tường phố**, **13/13 khúc bastion** (3 khúc nắn khung 1,13–1,14×, 1 ô vá cục bộ 5,6 %); **mái + mặt đường phố giữ A**.
4. **Kiểm dữ kiện (§6): ảnh AI được DÙNG có 0 lỗi chắc**; nghi vấn ghi lại: dải rong chân bastion cao ~1–1,5 m, địa y dày, một ô sàn pháo lát đá tấm; bong tróc vữa 1943 **chưa có ảnh nguồn mặt tiền để đối chiếu** (NARA 342-FH trong TIEN-KY không chụp phố cận).
5. **Chấm mù (3 người, ẩn nhãn, 5 khung khai trước): orbit HC7 thắng 6/9 phiếu, A thua 9/9 hoặc 6/9.** Craft TB orbit **HC7 5,67 · HC8 5,00 · A 4,22**; chi tiết HC8 7,33 > HC7 5,33 > A 2,67. Phố: **gần như không phân biệt** (craft 4,67 = 4,67; HC7 thắng 4/6 phiếu "best", lý do "slightly richer facade weathering"). Ở khung giữa cung (f72) **3/3 chọn HC8** và **3/3 nói HC8 "có tường chắn hoàn chỉnh"** — sai (HC8 đã xoá tường chắn): **chấm mù không thay được kiểm dữ kiện** (lặp lại bài học PT §15.5). Nhấp nháy theo người chấm: 0/30 "có" — khung tĩnh không đủ để chấm nhấp nháy; số đo máy ở mục 1–2 là căn cứ.
6. **Hiệu quả nhìn thấy:** bastion HC7 rõ hơn hẳn A (khối xây, mạch vữa, rong chân tường) — craft +1,45; phố bay 20–60 m: **55 % khung là mái/mặt đường** (đo ở probe), mặt tường chỉ 19 % → HC7 chỉ đổi phần nhỏ khung; mái AI lại thất bại → khác biệt nhỏ.
7. **Đề xuất (§9):** HC7 **dùng được cho công trình điểm nhấn** (đá/công sự, mặt tiền gần) với quy trình 5 chốt (mặt nạ chỉ mặt phẳng, prompt chỉ vật liệu, ảnh mẫu không bố cục, thước trôi + cấu trúc, rà mắt 100 %); **không dùng** cho nhìn-từ-trên (mái/phố) và **không dùng HC8** dạng sửa cả khung.

## 2. Việc đã làm
### 2.1 Chọn cảnh (HC7)
- **Đoạn phố: Main Street 1943** (ghost SH 1943: OSM + AMS), Commercial Square → nam 160 m. **Lý do:** 570 footprint toà riêng có số tầng ước (1782: 22 khối phố + 13 toà, RMS nắn 21 m, nửa số lô đổ nát) — cần nhiều toà riêng biệt để thử "một bộ vân mỗi toà"; 1943 có tim phố rõ (đo khoảng trống giữa hai dãy toà, 8–12 m).
- **Điểm nhấn: King's Bastion 1782**, footprint OSM way 952588383 + 256821558 (như V5b-2b), tường đá từ mặt biển (−5,5 m) tới sàn pháo (+1,2 m), tường chắn dày 2,4 m cao +3,2 m, 20 lỗ châu mai, 12 pháo; Line Wall nối theo ghost C1782-06/07. Phố 1782 quanh bastion: A (chỉ một công trình nhận HC7).
- **Cú máy** (`design/pt3/scene/cams.py`): (a) phố 8 s, 192 khung, cao 55 → 22 m, 26 mm; (b) orbit 6 s, 144 khung, R 95 m, cao 34 m, phương vị 200° → 340° (140°), 30 mm. Mặt trời 16:12 giờ biểu kiến, 12/9 (như PT lượt d3: cao 30,8°, phương vị ≈ 250°). Cycles CPU 960×540 @16 spp + OIDN.

### 2.2 Quy trình HC7 (`design/pt3/tools/`)
1. **Probe** 16/15 khung mẫu (mã nhóm mặt) → chọn nhóm: phố ≥ 0,2 % khung ở ≥ 1 khung (77 nhóm, 37 toà, phủ **84,3 %** điểm ảnh tường); bastion mọi mặt thấy được trừ tường thấp phía đất (45 nhóm, 319,6 m).
2. **Dựng trực giao** albedo (nhánh phát sáng = màu nền, không ánh sáng) + mặt nạ cho từng mặt phẳng tường; ghép **dải mỗi toà** theo thứ tự cạnh (góc nhà liền trong dải) → chia khúc ≤ 2,5–3:1 (64 px/m phố, 80 px/m bastion; chồng 2 m). Mặt nạ (bản cuối): **chỉ mặt vữa nằm trên mặt phẳng tường** (|lệch| < 3 cm) — đá góc, gờ, bậu, cửa, chớp, ban công **ngoài mặt nạ = A**.
3. **Sửa ảnh** `POST /v1/images/edits`, **`gpt-image-2.5-sunburst-2026-09-08`**, `quality high`, JPEG q82, stream; ảnh mẫu phong cách = một mảng vữa trơn (phố) / đá (bastion). Prompt cố định theo loại mặt (nguyên văn trong `ai/goi-api.jsonl`).
4. **Nướng** (`bake_hc7.py`): kiểm trôi (điểm gần đen mới trong mặt nạ ≤ 1 %); **nắn khung** nếu AI co/dãn ≤ 15–20 % (hộp bao); **vá cục bộ** nếu 1–5 %; **đều sáng + neo màu** σ = 1 m (out × G(in)/G(out) — bỏ bóng/nắng nướng sẵn + kéo màu tầm lớn về bảng màu A); ghép cứng theo mặt nạ; hoà khúc theo tâm gần nhất, mép Gauss 10/16 px; độ nhám + bump suy từ độ sáng (phép toán, như PT §6).
5. **Gắn UV** từng mặt vào atlas của đúng toà (mặt quay ra ≥ 45° theo mặt phẳng nhóm); dựng A và HC7 cùng mã, cùng hạt giống, cùng hình học (272 824 / 21 519 mặt).

### 2.3 HC8 (`design/pt3/tools/hc8.py`)
3 tấm A 1920×1080 @32 spp ở phương vị 245°/270°/295° (cung máy chính ±25°) → sửa ảnh, mặt nạ = bastion → ghép cứng → chiếu ngược theo lượt vị trí thế giới từng khung orbit, kiểm thấy-được bằng lượt vị trí của tấm (≤ 0,12 m + 0,2 %·d), hoà theo góc nhìn w = exp(−(θ/12°)²); không tấm nào thấy = "lộ" (giữ A).

### 2.4 Thay đổi quy trình giữa phiên (theo lỗi đo được, không theo cảm nhận)
| Lần | Hiện tượng | Đo/thấy | Sửa |
|---|---|---|---|
| 1 | bastion: AI co tường, vẽ tường chắn + lỗ châu mai + gờ không có | 28 % điểm đen mới | prompt bỏ mô tả bố cục, thêm luật "phủ kín đúng khung, không bịa băng/gờ/lỗ" |
| 2 | phố: AI xoá đá góc/gờ/bậu, vẽ ống thoát nước | rà mắt | mặt nạ chỉ mặt phẳng vữa (thuộc tính `flat`), dựng trực giao lại |
| 3 | ảnh mẫu là mặt tiền có cửa → cửa giả trên tường trơn (b54, b65, b71, b78…) | rà mắt 6/6 tường trơn | **dừng lô** (39 ảnh bỏ), đổi ảnh mẫu |
| 4 | không ảnh mẫu, prompt "facade of a 3–4-storey building" → vẫn vẽ cửa lên tường trơn | rà mắt | prompt chỉ vật liệu ("ONLY a wall surface… keep blank walls blank") |
| 5 | mái/phố nhìn từ trên: AI bịa thị trấn mới | tương quan cấu trúc σ 1 m **−0,11…+0,14** (tường: trung vị 0,57) | loại 15/15, mái/phố giữ vật liệu A; thêm thước tương quan cấu trúc |
| 6 | nắn khung "cứu" nhầm khúc đen 99 % (kéo dải hẹp ra cả tường) | rà số | giới hạn hệ số nắn 0,85–1,2 |

## 3. Số đo bằng máy
### 3.1 Nhấp nháy + nhất quán (`do/do-*.json`; chiếu ngược theo lượt vị trí, chỉ điểm thấy được ở cả hai khung)
| Cú | Nhánh | Nhấp nháy vùng vân AI: TB / p95 / % chớp | Vùng mọi toà: TB / % chớp | Nhất quán đầu↔cuối ΔY | giữa↔cuối | đầu↔giữa |
|---|---|---|---|---|---|---|
| orbit | A | 2,564 / 6,92 / 0,90 % | 2,49 / 1,50 % | 4,57 | 5,50 | 7,02 |
| | **HC7** | **2,710 / 7,88 / 1,52 %** | 2,62 / 2,03 % | 5,83 | 5,75 | 5,91 |
| | HC8 | 5,611 / 19,86 / **9,52 %** | 4,74 / 7,80 % | 11,57 | **58,38** | **55,56** |
| phố | A | 2,169 / 7,52 / 2,05 % | 2,07 / 1,72 % | 7,71 | 5,62 | 6,72 |
| | **HC7** | **2,202 / 7,69 / 2,16 %** | 2,08 / 1,75 % | 8,37 | 5,93 | 7,06 |
- Đường gốc A ≠ 0 vì nhiễu Cycles 16 spp + khử nhiễu và đổi góc nhìn (bóng, phản xạ). HC7 − A = +0,15 (orbit), +0,03 (phố): **cùng mức nhiễu dựng**; HC8 gấp 2,2×. Khung xấu nhất: HC7 2,98 vs A 2,88 (orbit); HC8 17,5.
- Nhất quán HC8 giữa↔cuối 58: phần giữa cung hiện tấm C, cuối cung lộ A → bề mặt "đổi chất liệu" trong cùng một cú.

### 3.2 Cung máy còn đứng được (orbit, `do/hc8-cung-may.json`)
| Cách | Lộ mặt khuất ≤ 1 % | ≤ 5 % | Kéo giãn > 2× texel | Ghi chú |
|---|---|---|---|---|
| HC7 | **cả 140°** (200°–340°) — mọi mặt bastion thấy được đều có vân trong atlas; vân theo UV nên không lộ/không kéo giãn | — | 0 (texel 80 px/m cố định) | mặt thấp phía đất (2,2 m) giữ A |
| HC8 | **241,7°–299,3°** (57,6°) | 226,8°–318,1° (91,3°) | 0,6–2,7 % điểm bastion | lộ TB cả cú 22,4 %; 200° lộ 96,5 %, 330° lộ 68,8 % |

### 3.3 Chuẩn hình (cách điều phối: 640×360 INTER_AREA, cắt y 60–300; trung vị theo khung)
| Cú | Nhánh | Bão hoà | Colorfulness | FIND_EDGES | |Laplace| |
|---|---|---|---|---|---|
| orbit | A | 0,063 | 29,7 | 11,21 | 8,54 |
| | HC7 | 0,055 | 30,0 | **16,09** | 12,73 |
| | HC8 | 0,188 | 34,6 | 21,96 | 18,34 |
| phố | A | 0,165 | 32,3 | 13,15 | 10,17 |
| | HC7 | 0,165 | 32,2 | 13,45 | 10,45 |
- HC7 bastion +44 % FIND_EDGES; bão hoà HC7 không tăng vì neo màu về A (bastion A trắng-xám). HC8 bão hoà gấp 3 do màu ấm tấm C không neo.
- Đối thủ (CITYTONS/Barcelona/Timelapse Studio): không có trong repo/API — điều phối tự so trong chat (gợi ý `khung/to-khung-orbit-A-HC7-HC8.jpg`, `khung/to-khung-pho-A-HC7.jpg`).

### 3.4 Vân nướng: đường nối, lệch màu, số vân (`do/nuong-*.json`, `do/lap-van-street.json`)
| Chỉ số | Bastion | Phố |
|---|---|---|
| Khúc gọi / dùng / loại | 13 / 13 / 0 (+ 2 lần thử 2) | 70 / 47 / 23 (15 ô mái + 8 khúc tường đen/trôi) |
| Số vân / toà | 1 atlas 16 719 × 696 (9 khúc) + 1 bản ghép sàn (4 ô) | 37 atlas; TB 1,5 khúc/toà (1–3) |
| Đường nối khúc (tỉ số, ≈ 1 liền, > 1,5 lộ) | TB 0,80, max 0,90; 0/8 lộ | TB 0,78, max 1,12; 0/18 lộ |
| Nối góc nhà liền kề | HC7 TB 1,02 (1/41 > 1,5) · A 1,25 (9/41) | HC7 1,12 (1/17) · A 1,47 (6/17) |
| Lệch màu AI thô so với A (ΔE76) | TB 12,2, max 26,6 | TB 16,2 (khúc), max 21,8 |
| Sau neo màu σ 1 m | TB 3,7 | TB 0,16 |
| Độ trải màu giữa các toà (std a*, b*) | — | A 3,5 / 4,7 · **AI thô 0,6 / 1,1** · HC7 3,5 / 4,7 |
| Mức chỉnh đều sáng (median \|ln tỉ số\|) | 0,35 | 0,54 |
- **Lệch màu giữa toà kề:** AI thô **đồng phục hoá** mọi toà về cùng tông be (độ trải a*/b* giảm 6×) — bảng màu sơn khác nhau của các lô 1943 bị xoá nếu không neo. Neo σ 1 m trả lại đúng bảng màu A (do người đặt) — đồng thời bỏ phần lệch phong cách giữa toà.
- **Lặp vân:** không có chép điểm ảnh giữa toà (NCC cao tần AI TB 0,023, max 0,05; A lát CC0: 0,26, 6,8 % cặp > 0,5). Nhưng rà mắt thấy **họa tiết lặp** (mảng xám mép phải, vệt chảy) ở nhiều tường trơn — ảnh hưởng ảnh mẫu; thước bố cục tầm lớn AI 0,65 vs A 0,92 (cả hai bị chi phối bởi dải ẩm chân tường) → ghi là nghi vấn thẩm mỹ, chưa thành lỗi.

### 3.5 Giây/khung (Cycles CPU 4 lõi, 960×540 @16 spp + OIDN; `log/giay-khung.json`)
| Lượt | orbit A | orbit HC7 | phố A | phố HC7 |
|---|---|---|---|---|
| Khung đẹp (TB) | 11,77 s | **9,64 s** | 12,27 s | **11,86 s** |
| Lượt vị trí / mã toà | 0,29 / 0,28 s | — / 0,23 s | 0,99 / 0,98 s | — / 0,98 s |
- HC7 không chậm hơn A (một ảnh atlas thay 3 ảnh PBR + nút bẩn thủ tục). HC8: 3 tấm 1080p @32 spp 84 s/tấm + chiếu ngược 0,85 s/khung (numpy).
- 1080p @16 spp ≈ 4× (ước): ~45–50 s/khung → 8 s phim ≈ 2,5 giờ máy.

## 4. Chi phí thật từng lệnh gọi (OpenAI — `ai/goi-api.jsonl`, 133 dòng; giá $8/M ảnh vào, $30/M ảnh ra, $5/M chữ vào + 100 token/ảnh tạm)
| Nhóm | Lệnh | Token ra | $ | Dùng được | Ghi chú |
|---|---|---|---|---|---|
| Bastion tường | 10 | 8 470 | 0,476 | 9 khúc (c1 = lần 2) | ~$0,042–0,049/khúc 2208×768 |
| Bastion sàn | 5 | 9 785 | 0,398 | 4 ô | $0,080/ô 1120² |
| Phố tường | 97 | 130 177 | 6,130 | 47 | 41 lệnh lần 1 bị bỏ (mặt nạ cũ 1 + ảnh mẫu sai 39 + mẫu 1); 56 lần 2 |
| Phố mái/đường (top) | 15 | 39 300 | 1,531 | **0** | bịa bố cục — lỗi chắc |
| HC8 tấm C | 6 | 9 132 | 0,371 | **0** | trôi hình — lỗi chắc |
| **Tổng** | **133** | 196 864 | **8,906** | 60 vân dùng | HTTP 200: 133/133; **C2PA 133/133** (đoạn APP11/JUMBF trong JPEG); TB 31 s/lệnh |
- Chi phí "ròng" nếu quy trình đúng ngay từ đầu (ước): bastion 13 lệnh ≈ $0,9; phố tường 55 lệnh ≈ $3,5.
- Claude: 15 phiếu chấm mù **$1,170** (`kiem-mu/cost.jsonl`; ghim `claude-sonnet-5-5`, CLI còn gọi phụ `claude-haiku-5-5` — ghi đúng như log `served`).

## 5. Chấm mù (`design/pt3/tools/blind_pt3.py`, `kiem-mu/`)
Giao thức như PT: `claude -p` ghim `claude-sonnet-5-5`, chỉ Read, 3 vai nguyên văn `blind_v2.py`, nhãn ẩn, hoán vị hạt giống 20261018, khung khai trước (phố f60, f150; orbit f30, f72, f120). Mỗi nhánh: khung tĩnh + tờ 4 khung liền nhau (hỏi nhấp nháy).

| Cú | Nhánh | craft | chi tiết | đúng thời kỳ | ai_look | nhấp nháy "có" | "Đẹp nhất" |
|---|---|---|---|---|---|---|---|
| orbit (9 phiếu) | A | 4,22 | 2,67 | 3,89 | 4,00 | 0/9 | 0 |
| | **HC7** | **5,67** | 5,33 | **5,44** | 3,67 | 0/9 | **6** (f30 3/3, f120 3/3) |
| | HC8 | 5,00 | **7,33** | 5,11 | 3,67 | 0/9 | 3 (f72 3/3) |
| phố (6 phiếu) | A | 4,67 | 3,50 | 5,33 | 4,17 | 0/6 | 1 |
| | HC7 | 4,67 | 4,00 | 5,33 | 4,17 | 0/6 | 5 |
- "Kém nhất": orbit f30, f72: A 6/6; f120: **HC8 3/3** ("broken geometry and pop-in slabs"). Phố: cả 3 người nói hai bản "nearly identical", HC7 "slightly richer facade weathering".
- **Lỗi người chấm:** f72 cả 3 người nói HC8 "complete parapet" và HC7 "no parapet" — **ngược với hình học** (HC7 giữ tường chắn đúng; HC8 tấm C đã xoá). ⇒ chấm mù không dùng để kiểm dữ kiện.
- Nhấp nháy: 0/30 — giới hạn của chấm bằng khung tĩnh; căn cứ là §3.1.

## 6. Kiểm dữ kiện từng vân (HC4) — `ai/kiem-du-kien.json` (133 tệp)
Cách kiểm: rà mắt **mọi** tệp AI (tờ so sánh ảnh vào/ra; phóng 1:1 các khúc có cờ), sàng tự động `kiem_van.py` (đường thẳng ≥ 1 m sâu trong mặt nạ, vùng đen mới) + `bake_hc7.py` (trôi, tương quan cấu trúc). Đối chiếu TIEN-KY T3: **Drinkwater 1786** "View of the Grand Attack" và "Plan of the Batteries" (Line Wall/bastion = khối xây đá, tường chắn có lỗ châu mai), **NARA 342-FH 000757/759/761** (1943 — không có mặt tiền phố cận), hình học A (ghost SH, OSM).

| Nhóm | Tệp | Lỗi chắc | Nghi vấn | Chi tiết AI thêm (đã liệt kê từng tệp) |
|---|---|---|---|---|
| Bastion tường (dùng) | 9 | **0** | dải rong/ẩm chân tường cao ~1–1,5 m (thuỷ triều Gibraltar nhỏ); địa y trắng dày | khối đá có mạch vữa, địa y, vệt muối/nước, rong ở mực nước, sứt mẻ |
| Bastion sàn (dùng) | 4 | **0** | 1 ô AI lát đá tấm một phần sàn (nguồn không đủ chi tiết để xác nhận/loại) | đất nện + sỏi, vết bánh xe toả tia, mảng đá vá; đá đỉnh tường chắn mòn |
| Phố tường lần 2 (dùng 47) | 55 | **0** trong 47 khúc dùng; 8 khúc tô đen → loại bằng máy | họa tiết lặp giữa toà; mức bong tróc 1943 chưa có ảnh nguồn đối chiếu | vữa vôi sơn bong, nứt chân chim, vệt mưa dọc, ố ẩm chân tường, mảng trát vá |
| Phố tường lần 1 (bỏ) | 41 | cửa/đá góc giả trên tường trơn (39 ảnh mẫu sai + 1 prompt "mặt tiền"); xoá đá góc/gờ/bậu + vẽ ống (1) | — | — |
| Phố mái/đường | 15 | **bịa mặt bằng mái/ngõ/sân mới** (15/15) | — | — |
| HC8 tấm C | 6 | xoá tường chắn + lỗ châu mai; dời/phóng đường bao; xoá khối Line Wall + pháo | — | — |
| Bastion tường lần 1 c1 | 1 | vẽ thêm tường chắn + lỗ châu mai + gờ, thu nhỏ khung | — | — |
- **Không có** chữ, cờ, người, xe, vật hiện đại trong mọi tệp được dùng. Tổng lỗi chắc phát hiện: **63 tệp** (sổ `kiem-du-kien.json`) — **tất cả nằm ngoài tập dùng**; thêm 8 khúc phố lần 2 bị máy loại (tô đen/trôi) trước rà mắt.
- Giờ rà (ước): ≈ 1–1,5 phút/khúc ở tờ tổng + 3–5 phút/khúc có cờ; phiên này ≈ 2 giờ cho 133 tệp.

## 7. Ước cho một tập (ước, máy 4 lõi CPU)
Giả định tập 9–11 phút có **4 cú bay phố** (~150 m mỗi cú) + **3 công trình điểm nhấn** (orbit/cận).
| Khoản | Mỗi cú phố | Mỗi điểm nhấn | Một tập |
|---|---|---|---|
| Toà/công trình cần vân | ~37 toà (≥ 0,2 % khung) | 1 | ~150 toà + 3 công trình |
| Lệnh OpenAI (gồm ~15 % thử lại) | ~65 | ~15 | ~305 |
| Chi phí OpenAI | ~$4,1 | ~$1,0 | **~$19** (vượt trần $15 của phiên — cần duyệt trần tập) |
| Giờ kiểm dữ kiện (người/Claude rà mắt) | ~1,5 h | ~0,5 h | **~7,5 h** |
| Giờ máy chuẩn bị (probe + trực giao + nướng) | ~0,2 h | ~0,1 h | ~1,1 h |
| Giờ máy dựng 540p @16 spp (8 s) | ~0,65 h | ~0,45 h (6 s) | ~4 h; **1080p ×4 ≈ 16 h** |
- Mái nhìn từ trên: **không** có cách AI nào đạt trong phiên → giữ A (CC0) hoặc thủ tục; chi phí trên đã bỏ ô mái.

## 8. Giờ máy + API thật
| Khoản | Trần | Thực tế |
|---|---|---|
| Claude API | $3 | **$1,170** (15 phiếu; 39 %) |
| OpenAI API | $15 | **$8,906** (133 lệnh; 59 %) |
| YouTube / ElevenLabs | 0 / 0 | 0 / 0 |
| Giờ máy | ≤ 6 h | **≈ 3,4 h**: có sổ 2,71 h (probe 47 s · trực giao 5,3 ph · tấm chiếu 4,4 ph · orbit A 29,7 ph · phố A 45,7 ph · orbit HC7 ≈ 25 ph · phố HC7 41,2 ph · HC8 chiếu ngược 2,1 ph · dựng thử 10 ph) + ước ≈ 0,7 h (dựng thử hình học bastion ~12 khung, nướng atlas 5 lượt × 2–6 ph, đo, video) |
| Video | 15 MB | 7,3 MB (5 tệp 960×540) |
| Ảnh | 40 MB | 39,47 MB |

## 9. Quyết định đề xuất
### Q-PT3-1 — HC7 (vân nướng gắn hình học) cho máy chuyển động
| Phương án | Ưu | Nhược | Tác động | Rủi ro |
|---|---|---|---|---|
| **A. Dùng HC7 cho công trình điểm nhấn + mặt tiền gần (KHÔNG cho mái/nhìn từ trên) — đề xuất** | nhấp nháy ≈ A (+0,03…+0,15); vân cố định mọi khung, cả 140° orbit; craft orbit +1,45, 6/9 "đẹp nhất"; FIND_EDGES +44 %; không chậm dựng; ~$1/công trình | quy trình 5 chốt bắt buộc; 25–33 % khúc phố trượt (đen/trôi); bảng màu phải neo → mất "tông ấm" AI; lặp họa tiết khi dùng ảnh mẫu | thêm ~2 h rà/tập + ~$19/tập (ước); bỏ nhãn "No AI imagery" ở cú có vân AI, thêm dòng "Surface detail AI-assisted…" | công bố AI (C2PA 133/133 → YouTube có thể tự gắn nhãn, PT §15.8); AI bịa chi tiết nhỏ không có nguồn (vết ố, rong) |
| B. Giữ A (CC0) | 0 rủi ro công bố; $0 | bastion "trắng như đồ chơi" (3/3 phiếu f72: "toy-like white shell"); chi tiết 2,67 | không đổi | thua khung đối thủ ở công trình |
| C. HC7 mọi bề mặt kể cả mái | phủ 55 % khung phố | **15/15 ô mái bịa bố cục** | — | lỗi dữ kiện chắc |

### Q-PT3-2 — HC8 (chiếu tấm C, hoà theo góc nhìn)
| Phương án | Ưu | Nhược | Tác động | Rủi ro |
|---|---|---|---|---|
| **A. Không dùng — đề xuất** | — | — | — | — |
| B. Dùng trong cung ±25–29° | chi tiết cao nhất (7,33), đẹp nhất ở giữa cung (3/3) | **lỗi chắc mọi tấm** (xoá tường chắn, dời đường bao 39–60 px); nhấp nháy 2,2×; ngoài cung lộ/chắp vá ("broken geometry" 3/3 ở f120) | phải khoá cung máy; mỗi tấm 2 lần thử vẫn trôi | sai dữ kiện công sự — người chấm còn đánh giá ngược |

### Q-PT3-3 — Luật K đề xuất (P/K ghi; phiên không sửa `checks/`)
1. **`ai_texture`**: khung có vân AI ghi `ai_texture: true` trong log khung (đã làm: `log/video-*.jsonl`); thiếu → TRƯỢT.
2. **Nhãn**: khung `ai_texture: true` phải có dòng "Surface detail AI-assisted · layout, landmarks & flags from sources" (dưới-trái, ≥ 15 px @540p) suốt đoạn; khung A giữ "No AI imagery".
3. **Kiểm dữ kiện**: mỗi vân AI dùng phải có dòng trong `kiem-du-kien.json` với `ket_luan` "dùng (0 lỗi chắc)" + danh sách chi tiết thêm + nguồn đối chiếu; tệp có lỗi chắc không được tham chiếu bởi atlas (kiểm bằng `nuong-*.json` → `dung`).
4. **Trôi/bố cục** (máy, trước rà mắt): điểm gần đen mới ≤ 1 % trong mặt nạ; nắn khung chỉ 0,85–1,2; **tương quan cấu trúc σ 1 m ≥ 0,2** cho khúc có cấu trúc (độ lệch chuẩn tầm thấp của ảnh vào > ngưỡng) — chặn được 15/15 ô mái bịa.
5. **Nhấp nháy**: đo chiếu ngược trên vùng `ai`; HC − A ≤ +0,5 (thang 0–255) và % chớp ≤ A + 1 điểm % (HC7 đạt: +0,15/+0,62 orbit; +0,03/+0,11 phố; HC8 trượt +3,05/+8,6).

## 10. Chỉ số trong ±5 % quanh ngưỡng
- **Ảnh 39,47 MB / trần 40 MB (−1,3 %)** — đã bỏ 3 khung lẻ trùng và thu nhỏ bản xem ảnh bị loại để vào trần.
- **Hệ số nắn khung bastion 1,139 / 1,143 / 1,134 vs giới hạn 1,2** (−5,1 %, −4,75 %, −5,5 %): khúc c6 (1,143) trong ±5 %.
- Ô sàn bastion y0_x320: **vá cục bộ ở 4,64 % điểm tối vs giới hạn 5 %** (−7,2 %, ngoài ±5 % nhưng sát — nêu).
- Không chỉ số nào khác trong ±5 %: nhấp nháy HC7 phố +1,5 % so A (không có ngưỡng khoá); nối khúc max 1,12 vs 1,5; trôi dùng max 0,77 % vs 1 %; Claude 39 %, OpenAI 59 %, giờ máy ≈ 57 %, video 49 %.

## 11. Việc chờ chủ dự án
1. **Q-PT3-1** (HC7 cho điểm nhấn + mặt tiền gần, không cho mái) và **Q-PT3-2** (bỏ HC8).
2. **Q-PT3-3**: K cân nhắc 5 luật (ai_texture, nhãn, kiểm dữ kiện, trôi/cấu trúc, nhấp nháy).
3. **Trần OpenAI cho một tập** nếu chọn HC7: ước ~$19/tập (> $15 của phiên).
4. **Công bố AI**: nếu dùng HC7 thì cú đó không còn "No AI imagery"; mọi ảnh có C2PA (YouTube có thể tự gắn nhãn, PT §15.8). Chủ dự án quyết cách ghi trên hình/mô tả.
5. **Nguồn mặt tiền 1943** (ảnh PD phố cận) để kiểm mức bong tróc/phong hoá — hiện chỉ "chưa kiểm được bằng nguồn".
6. **Mái nhìn từ trên**: chưa có cách đạt — cần phiên riêng (vân CC0 theo vật liệu + bẩn thủ tục, hoặc ảnh hàng không PD) nếu muốn mái giàu chi tiết.
7. **Việc NẾU còn giờ chưa làm:** nạp atlas HC7 vào dây chuyền three.js/llvmpipe (`design/k2v/tl`) — chưa làm (ưu tiên dựng đủ A/HC7/HC8 + kiểm dữ kiện); atlas + manifest sẵn ở dạng PNG + UV theo mặt phẳng nhóm, chuyển được (ước 1 phiên ngắn).
8. **Ghi ngoài vùng (P):** RIGHTS.md — 60 vân AI dùng được (OpenAI, quyền đầu ra theo Services Agreement §4.1, C2PA) + OSM ODbL đã có dòng; AUTHORSHIP — quyết định Q-PT3-1/2 + chọn Main Street 1943/King's Bastion; COST-LEDGER dòng PT3: `PT3-01,vân nướng HC7 + tấm chiếu HC8,R&D,2026-10-18,,,,,1.17,3,claude-sonnet-5-5,0,0,≈ 3,4,,0,15,OpenAI $8.91 (gpt-image-2.5-sunburst-2026-09-08 ×133),reports/pt3/PT3-BAO-CAO.md,YouTube 0; không merge`.
9. Ảnh AI bị loại: tệp gốc giữ trong container phiên (`/var/tmp/pt3/loai_ref/`) — repo có bản xem 320 px + SHA (`ai/loai-xem-nho/`). Mất khi container bị thu hồi; nếu cần lưu gốc, P cấp chỗ ngoài trần 40 MB.

## 12. Tệp
- Mã: `design/pt3/{README.md, scene/{build_pt3.py, cams.py, pt_site.py, passes.json}, data/osm-kings-bastion.json, tools/{exr.py, select_groups.py, prep_ai.py, gen_ai.py, kiem_van.py, bake_hc7.py, lap_van.py, hc8.py, do_pt3.py, video.py, blind_pt3.py}}`.
- Báo cáo: `reports/pt3/{PT3-BAO-CAO.md, ai/ (60 dùng + bị loại thuộc lần 2/HC8/top; goi-api.jsonl; kiem-du-kien.json; loai-xem-nho/), do/ (nuong-*, do-orbit-*, do-pho-*, hc8-*, lap-van-street, kiem-van-street, loai-ra-mat-street, groups_*, khuc-*), video/ (5 × 540p), khung/ (2 tờ khung), kiem-mu/, log/, giay-phep/ (openai-pt3.md, osm.md)}`.
- Preflight: mọi commit qua hook pre-commit `tools/preflight.sh` — **ĐẠT**; `checks/lock.py --verify` **KHỚP**.
