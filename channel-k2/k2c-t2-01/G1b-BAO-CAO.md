# K2C-T2-01 "Shipbuilding" — BÁO CÁO CỔNG G1b (phiên T2, 15/10/2026). DỪNG, chờ chủ dự án rà tờ khung

> Làm theo lệnh duyệt G1 (15/10): J1–J6 ghi vào AUTHORSHIP; người đọc mù vòng 4 trên lời v3.2, sửa một lần rồi khoá; tra lại phí Section 301; tờ khung 540p. Nhánh **`k2c-t2`**, đẩy cả `ccr-bef6f172-fcqat9`. Không sửa `docs/BIBLE-KENH2.md` (J2), không sửa và không đọc mã `checks/`.

## 0. Tóm tắt một màn hình
| Hạng mục | Kết quả |
|---|---|
| AUTHORSHIP | Thêm dòng "Kênh 2 K2C-T2-01 "Shipbuilding" (G1 — DUYỆT)", ghi J1–J6 cùng phần đóng góp của chủ dự án |
| Người đọc mù vòng 4 (v3.2) | 3 vai, model ghim. Móc **7/7/7** (v3: 6/8/6) · nhân vật **4/4/4** (v3: 5/6/5) · tin cậy **8/7/6** (v3: 7/8/7). 3/3 xem tiếp sau 15 s; 3/3 thấy phần kết trả lời câu hỏi mở đầu; 3/3 không thấy nghiêng phe |
| Sửa sau vòng 4 | 7 lỗi được ≥ 2/3 người đọc nêu, mỗi lỗi sửa **một lần, theo đúng chữ góp ý**; không chạy thêm vòng (§2) |
| **Lời KHOÁ v3.3** | 1 588 từ, ≈ 10:30 ở tốc độ đọc, ước timeline **10:42,5**. `script.md` SHA-256 **`4554b697…20473`**, `loi-khoa.txt` `9bf318c2…`. `make_spec.py` dừng nếu lời lệch SHA |
| Phí Section 301 (tra 15/10) | **Không đổi** so với C01: tạm hoãn tới 9/11/2026 (90 FR 50947). Chưa có văn bản gia hạn hay chấm dứt. Lời ghi "As of October fifteenth, 2026" (§3) |
| Tờ khung 540p | `g1b/TO-KHUNG-G1b.jpg`: 22 cửa sổ 6 s, gồm Đ1–Đ3 và ≥ 1 khung cho mỗi chương 00–06 (§4) |
| Nhịp thị giác (rhythm.py, trên đặc tả) | **ĐẠT**: trung bình **2,42 s**/biến cố (ngưỡng 3,5), khoảng dài nhất **5,56 s** (ngưỡng 6; cách ngưỡng −7,3 %) |
| Footage (đặc tả) | **0 %** (ngưỡng ≤ 20 %): G1b không nối footage (§6) |
| API `claude -p` | **$4,03** luỹ kế / trần $11 (G1b thêm $0,24 cho vòng 4) |
| YouTube Data API | ≈ 216 / 300 (G1b không dùng) · ElevenLabs: 0 ký tự |

## 1. AUTHORSHIP (việc 1)
Đã thêm dòng `2026-10-15 | Kênh 2 K2C-T2-01 "Shipbuilding" (G1 — DUYỆT)` vào `AUTHORSHIP.md`, ghi nguyên ý J1–J6 và phần đóng góp biểu đạt của chủ dự án: chọn đề tài trong 3 ứng viên, chọn thứ tự móc, chọn cách đặt câu miễn trừ, chọn tiêu đề và thumbnail, đặt hạn đăng.

## 2. Người đọc mù vòng 4 trên lời v3.2 (việc 2, J4)
- **Cách chạy:** 3 vai, `claude -p` ghim `claude-sonnet-5-5`, mỗi vai chạy trong thư mục trống, cùng đề bài với vòng 1–3. Kết quả ở `kiem-mu/bien-kich_v4-R{1,2,3}.json`. Chi phí $0,24.

| Chỉ số (R1/R2/R3) | v3 | **v3.2 (vòng 4)** |
|---|---|---|
| Móc | 6/8/6 | **7/7/7** |
| Nhân vật | 5/6/5 | **4/4/4** |
| Tin cậy | 7/8/7 | **8/7/6** |
| Cơ chế nối nhau | — | 6/7/6 |
| Xem tiếp sau 15 s | 3/3 | 3/3 |
| Kết trả lời câu hỏi mở đầu | — | 3/3 |
| Nghiêng phe | không (3/3) | không (3/3) |

- **Lỗi ≥ 2/3 cùng nêu → sửa MỘT lần bằng đúng chữ góp ý (v3.3), không chạy thêm vòng:**

| Lỗi (số người nêu) | Góp ý | Sửa trong lời |
|---|---|---|
| Không nêu tên trợ cấp (3/3) | "Never named or explained" | "…a federal subsidy, **the Construction Differential Subsidy**, meant to let American owners buy American ships at the world price" (C20) |
| "four hundredths of one percent" khó hiểu (3/3) | "Say '0.04 percent'" | "**0.04 percent**" |
| Không rõ phí để làm gì (3/3) | mục đích phí không được nói | thêm "The stated aim: to discourage the use and purchase of Chinese-built ships, and to press China to drop the practices the Trade Representative had found." (C57, trích FR-ACT) |
| Dồn ngày tháng ở chương 05 (3/3) | "Lots of dates, notices and fee mechanics before the point" | "From October 2025," thay cụm "Under an action … April seventeenth"; "In March 2024", "In September," |
| Khung "lương" (3/3) | nhấn quy mô mạnh hơn bằng chứng | thêm "Our emphasis on scale is a position the evidence only partly supports." |
| Thuật ngữ TFP (2/3) | "Jargon with no explanation" | bỏ câu năng suất các nhân tố tổng hợp (TFP) |
| Dồn số ở chương 01 (2/3) | "Stat dump" | bỏ câu 2 710 tàu và câu 702 000 người |

- **So với v3:** móc đều hơn (7/7/7). Điểm nhân vật giảm 5–6 → 4. Cả 3 người đọc nói chương 04 chậm vì rào đón ("by the company's account", lore tờ 500 won). **Không sửa phần này trong lời**, vì nhãn nguồn tự thuật và nhãn lore là luật nội dung (LUAT-NOI-DUNG-G); tờ khung xử lý bằng hình (§4), và người chấm mù ở bước Dựng sẽ đánh dấu lại. Điểm nhân vật giảm có thể do bỏ chi tiết ở chương 01; chưa có số đo để tách hai nguyên nhân.
- **Lời KHOÁ v3.3:** `script.md` (bản sao `script-v3.3-KHOA.md`; v3.2 lưu ở `script-v3.2.md`). 1 588 từ, 7 đoạn, 57 claim. SHA ở `LOI-KHOA.sha256`:
  - `script.md` `4554b69708a1ab08a7ffbe7ef3fb0f7e92aaac8a04fb8d57d2325dbb11d20473`
  - `loi-khoa.txt` (chuỗi gửi ElevenLabs, đã bỏ mã claim) `9bf318c282f83cab3ea9013617f4c1ef55f0e647d585f04a4b7bb8168a74906a`

## 3. Trạng thái phí Section 301, tra trước khi khoá lời (việc 3)
- **Tra ngày 15/10/2026:**
  - Federal Register API, cơ quan USTR, văn bản từ 01/09/2026: 8 văn bản, không văn bản nào về hàng hải hay đóng tàu.
  - Tìm "maritime logistics shipbuilding section 301" từ 01/11/2025: chỉ có 2 văn bản ngày 10/11 và 13/11/2025.
  - Danh mục công khai (public inspection) ngày 15/10: không có thông báo USTR nào về phí này.
- **Kết luận: không đổi so với C01.** Phí vẫn tạm hoãn tới 11:59 p.m. ngày 9/11/2026 (90 FR 50947, govinfo FR-2025-11-13). Lời ghi "As of October fifteenth, 2026, no extension had been published." Nhật ký tra ở `claims.md` §3.
- **Rủi ro còn mở (J6, đích đăng trước 9/11):** phải tra lại một lần nữa ngay trước khi thu giọng. Nếu USTR ra văn bản mới, cần sửa 3 câu (00, 05, 06) và khoá lại SHA.

## 4. Tờ khung 540p (việc 4)
- **Tệp:** `g1b/TO-KHUNG-G1b.jpg`: 23 cửa sổ 6 s, mỗi cửa sổ 3 khung ở 15/50/85 %. Đặc tả con: `g1b/tokhung.yaml`, sinh bằng `est.py --sub … --max 6`. Dựng bằng `vshot.py --draft --spp 2`.
  - Đ1 (01-2-6), Đ2 (03-2-4 xu "world price" ↔ "≈ 4×", 03-4-6 vòng lặp), Đ3 (04-2-8 phiếu đơn hàng rơi xuống bãi trống, 04-2-36 cẩu và tài liệu ở Ulsan, 05-8-8/36 Philadelphia trên ảnh NAIP).
  - Mỗi chương 00–06 có ≥ 2 cửa sổ.
- **Đo số trên khung thật (không ước lượng bằng mắt):**
  - `anchors.json` của từng cảnh: tỉ lệ khung có điểm neo của mỗi thẻ/nhãn/sticker nằm trong vùng an toàn (x 4–96 %, y 6–80 %).
  - Kết quả đo neo từng cửa sổ: `g1b/neo-tokhung.txt` (công cụ `g1b/anc_check.py`). Các mục 0 % còn lại là chủ ý: nhãn "Alaska" hiện sau cửa sổ (khi máy lia tới), thẻ trích dẫn "higher prices" hiện sau cửa sổ, thẻ "world price" đã tắt (`out`) khi máy chuyển sang cột 1970s.
  - `vshot`: chữ nhỏ 0 lần; tương phản thấp 12 lần ở lượt đầu, **0** ở lượt cuối.
- **Các lỗi chủ dự án nêu ở G1, đã sửa và kiểm lại trên khung:**

| Lỗi | Sửa | Kết quả trên tờ khung |
|---|---|---|
| (a) nhãn "Richmond, Calif." bị cột che hoặc cắt chữ; cột Đ1 che nhau theo chiều sâu | Cột cách 0,05° cùng vĩ độ; nhãn địa danh dùng chung bộ né vật (`side: auto`). Máy Đ1 lùi (dist 28 → 25, tâm nhìn dời bắc 37,84°) để đỉnh cột 122 ngày không chạm mép trên | Nhãn và 3 cột tách hẳn; neo cột 122 ngày nằm trong vùng an toàn **0 % → 100 %** khung |
| (b) Đ3 Ulsan: cẩu, tàu, phiếu quá nhỏ ở tầm máy | Hạ máy (dist 120 → 13–22 km); đạo cụ px 150–210 | Phiếu, cẩu, tài liệu đọc rõ ở 540p (04-2-8, 04-2-36) |
| (c) dải trắng ở bờ Ulsan (đường bờ Natural Earth lệch SRTM) | `relief_build.py --coast dem`: biển suy từ DEM (ô ≤ 0 m nối với biển NE); lệch 997 396 ô so với NE ở ppd 1800 | Không còn dải trắng ở mọi khung Ulsan |
| (d) relief `pnw`/`eastus`, đạo cụ truck | Dựng `pnw` (SRTM, ppd 150) và `eastus` (3DEP, bờ DEM, tuyến Delaware); đạo cụ `truck`/`train`/`pipeline` | Có trên tờ khung (02-1-5, 02-4-8, 03-3-28) |

- **Lỗi mới, chỉ lộ khi xem khung thật (đã sửa trong G1b):**
  1. **`vshot.py` bỏ qua `frame0`.** Cảnh 3D của mọi cửa sổ giữa shot luôn chạy từ giây 0, còn chữ 2D chạy đúng giờ: chữ trỏ vào khoảng trống, xu Đ2 không hiện, Đ3 đứng ở tầm xa. Sửa:
     - vshot dựng đúng khung `frame0…` (`--only`) và lớp 2D đọc `p.off`;
     - `render.js` đếm khung theo chỉ số;
     - `prep.lift_props` quy mốc sticker theo frame0/speed (lỗi này cũng có trong pipeline tập thật cho cảnh dùng lại).
  2. **Mép nước bậc thang** ở tầm 5–20 km: điểm ảnh nền 100–185 m. Dựng lại `eastus`, `korea`, `sfbay` ở **ppd 1800** (≈ 50 m). Hằng số vẽ quy theo ppd, mặt nạ nước làm mượt. Giữ nguyên số đỉnh lưới (mesh 12/12/8) để giờ dựng không tăng vì lưới.
  3. **Nét sông và ranh giới bang trùng lệch mặt nước**, ví dụ sông Delaware và ranh giới PA–NJ chạy song song cách sông 1–2 km. Cắt các đoạn chạy dọc mặt nước dài hơn 3 km; nối đầu sông nhánh tới mặt nước (sông Schuylkill trước đó hụt ~300 m).
  4. **Lộ mép bản đồ** ở các cảnh Hàn Quốc tầm 100–300 km. Thêm nền `koreaw` (124–132,6°E, ppd 600) cho r04_chung, r04_state, r04_abroad; bỏ vùng tô quốc gia ở r04_state, vì mép Natural Earth 1:50m lệch bờ DEM thành dải trắng trên biển.
  5. **Khung lệch:**
     - Alaska: tách thành hai cảnh `r02_alaska`/`r02_alaska2`. Cảnh dùng lại với speed 0,6 làm tuyến Seattle → Juneau không bao giờ hiện trong shot.
     - Trích dẫn ở Seattle: Seattle từng nằm ngoài khung; thêm điểm ghim tàu.
     - Xu 1970s, toa tàu/xe tải, cảng Philadelphia: chỉnh máy theo số neo.
     - Thêm `out` cho thẻ "world price", "$100M", "$5B", "1.5 → 20" để không quá 2–3 thẻ cùng lúc.
  6. **Bảng điểm (06):** hàng giá trị chồng lên chân bảng. Rút gọn giá trị ("3 / day", "~5 / year"); chuyển chân bảng thành dải chú thích "Different ships, different eras".
- **Ảnh hàng không:**
  - Chỉ NAIP 2022 (tài sản công, `licenses/naip-philly-richmond.txt`).
  - Ở 0,9 m/điểm ảnh, trên khung 05-8 và 06-3 không có biển hiệu hay logo đọc được.
  - Không dùng ảnh Commons (Philadelphia là CC BY-SA). Ulsan không có ảnh hàng không có giấy phép rõ, nên Đ3 dùng nền SRTM + đạo cụ.
- **Ảnh lưu trữ:** Owens và Jones giữ dạng ảnh in. Mặt nạ tách nền (BiRefNet, lệch p95 0,41 px) đã làm nhưng không dùng: ảnh cắt rời làm chân ngồi (Owens) và ghế (Jones) lơ lửng, kém hơn bản in.
- **4c. Còn lại, chờ chủ dự án rà:**
  - Chương 04 (Ulsan) dày thẻ: "LORE", "500-won note", nhãn Ulsan cùng lúc ở 04-2-36.
  - Thẻ "$36,227" hiện mờ dần ở mép trên phải (04-4-2).
  - Shot Alaska (02-1-5): khi máy lia lên phía bắc, nhãn "Vancouver, B.C." còn kéo dây xuống mép dưới khoảng 1 s rồi mới tắt; nền `pnw` (ppd 150) vùng nội địa phẳng và nhạt.
  - Chất lượng khung đo ở 540p, SPP 2 (nháp). Bản 1080p dựng một lần sau Dựng.
  - Chữ trên hình nhiều: 69 dòng chú thích + 37 thẻ số trong 10:42 (T1: 93 dòng chú thích / 12 đoạn). Kinh thánh muốn chữ tối thiểu; người chấm mù ở bước Dựng sẽ đánh dấu chỗ thừa.

## 5. Nhịp thị giác (`rhythm.py` trên đặc tả đã giải mốc; `g1b/rhythm-g1b.json`)
- **Cách đo:**
  - Timeline ước trước khi thu giọng: Eric 151,2 từ/phút, cùng `build_seg` với prep.
  - Mọi mốc "@từ" được giải ra giây; biến cố lấy từ **mốc thật** của đặc tả: đầu shot, nhãn, thẻ, sticker, chú thích, năm, máy đổi hướng/tầm, tuyến, cột, đạo cụ, bảng.
- **Kết quả:** **ĐẠT**. 266 biến cố (đã gộp các biến cố cách nhau < 0,25 s) trong 642,5 s: trung bình **2,42 s** (ngưỡng 3,5 s); khoảng dài nhất **5,56 s** ở 05 (Philadelphia, "…before any report we found of the new capacity"), ngưỡng 6 s.
  - **Chỉ số trong ±5 % quanh ngưỡng:** không có. 5,56 s cách ngưỡng −7,3 %; hai khoảng 5,5 s (05 China) và 5,6 s (05 Philadelphia) ở −8 %.
- **Sửa ở G1b:**
  - Trước khi chèn biến cố: dài nhất 17,8 s, 40 khoảng > 5,2 s.
  - Chèn biến cố **gắn vào từ đang nói**, mỗi biến cố mang nội dung: tên trợ cấp khi nói tên, "LORE" khi nói "lore", "$5B" khi nói "five billion", tuyến tàu khi nói "voyages", máy đổi tầm khi chuyển ý.
  - Sửa mốc khớp nhầm lần xuất hiện đầu (BAI-HOC #10): "@By#2", "@High#2", "@hundred#2", "@Three#2", "@abroad#2", "@ships#2", "@yard#2", "@shipbuilding#4".
  - Mốc số ở lớp 2D của shot không mở đầu đoạn được đổi thành mốc theo lời của shot (`make_spec.py`). Trước đó vật hiện sẵn khi cắt vào.
- **Sửa công cụ đo (`scripts/k2/rhythm.py`):** mốc của cảnh dùng lại được quy theo frame0/speed của shot; mốc ngoài khung shot không tính. Trước đó các mốc này bị đếm sai chỗ. Đã thêm test.
- **Câu miễn trừ (J3):** dải chú thích 44 px (≥ 38 px) từ 0:03 đến 0:12, vắt qua hai shot đầu (`seg: true`). 19 từ ≈ 7,5 s đọc ở 151 từ/phút, hiện 9 s. Kiểm trên tờ khung (00-0 khung 4,5 s).

## 6. Footage (`footage_share.py`; `g1b/footage-g1b.json`)
- **0 %** trên đặc tả (ngưỡng ≤ 20 %). G1b chưa nối đoạn phim NARA Liberty (gov.archives.arc.39018, 640×480, tài sản công): chưa tìm được mốc thời gian đúng đoạn hạ thuỷ Liberty, và nguồn dưới 720p phải đặt dạng khung trong khung.
- Đề xuất: giữ 0 % cho bản đầu; hoặc dò đoạn NARA ở bước Dựng (≤ 8 s, ≈ 1,2 %) nếu chủ dự án muốn có một khoảnh khắc phim thật ở chương 01 (việc chờ #4). Đã bỏ NARA khỏi danh sách nguồn của tập cho tới khi dùng.

## 7. Giấy phép và RIGHTS
- `channel-k2/k2c-t2-01/licenses/`: ảnh LoC ×2 (trích JSON loc.gov 15/10), NAIP Philadelphia/Richmond, địa hình SRTM/3DEP (+ OGL–Canada, NOAA ETOPO1; bản sao trang ghi công Tilezen), Federal Register/USTR, thư NFTC.
- `RIGHTS.md` thêm mục "K2C-T2-01" (T2-PHO-1/2, T2-AER-1, T2-DEM-1, T2-DOC-1/2, T2-STK-1). Mô tả nháp thêm dòng ghi công NAIP, địa hình, OGL–Canada.

## 8. Chi phí theo vai (sổ `so-vai.jsonl`, `vai.py sum`; `g1b/vai-sum-g1b.json`)
| Vai | API `claude -p` (đo) | Token phiên sinh ra / ghi cache / đọc cache (luỹ kế) | Quy đổi giá niêm yết phiên (ước, luỹ kế) | Phần G1b (ước) |
|---|---|---|---|---|
| Đóng gói | $0,62 | 64 k / 146 k / 24,8 M | ~$14,9 | $0 |
| Biên kịch + kiểm chứng | $3,40 (G1b +$0,24: vòng mù 4) | 60 k / 301 k / 24,7 M | ~$14,5 | ~$1,7 |
| **Công cụ** (cửa sổ riêng từ G1b) | $0 | 140 k / 321 k / 55,9 M | ~$33,4 | ~$33,4 |
| Đạo diễn (G1b: đặc tả, tờ khung, rà khung, chỉnh máy) | $0 | 163 k / 379 k / 83,4 M | ~$48,2 | ~$28,4 |
| P (điều phối) | $0 | 44 k / 200 k / 12,3 M | ~$8,5 | ~$2,0 |
| **Tổng** | **$4,03 / trần $11** | | ~$119,5 | ~$65,5 |
- **Giới hạn phép đo:**
  - Cửa sổ "công cụ" (00:47–01:18) gồm cả phần dựng đặc tả.
  - Các sửa công cụ phát sinh khi rà khung (nền ppd 1800, vshot frame0, sông/ranh giới) rơi vào cửa sổ Đạo diễn, vì phát hiện và sửa đan xen.
  - Quy đổi phiên là ước theo bảng giá (chủ yếu đọc cache), không phải hoá đơn.
- **Giữ/bỏ vai:** vẫn chưa đủ dữ liệu, quyết ở G2 như đề xuất ở G1. Lợi đo được ở G1b: vòng mù 4 bắt 7 lỗi ≥ 2/3, trong đó 3 lỗi 3/3 mà REVIEWER v3 không bắt (tên trợ cấp, "four hundredths", mục đích phí); chi phí $0,24.
- **Giờ máy:**
  - Tờ khung 540p SPP2: 3 lượt toàn bộ (~45–55 phút mỗi lượt, 1,1–2,3 s/khung 3D) + 2 lượt một phần.
  - 4 lượt dựng nền (~6 phút mỗi lượt cho 3 vùng).
  - Riêng lượt đầu dựng hỏng do lỗi frame0 (~50 phút).

## 9. VERSIONS
`VERSIONS.md` thêm các dòng G1b: bộ công cụ, đặc tả, nền mới, lời khoá. `test_k2v.py` **26/26 ĐẠT** (+1 test nhịp cảnh dùng lại). `checks/lock.py --verify` **KHỚP** (`c598467f…`); không sửa, không đọc mã `checks/`.

## 10. Việc đang chờ chủ dự án (G1b)
1. **Rà tờ khung** `g1b/TO-KHUNG-G1b.jpg` (J6): duyệt hướng hình Đ1–Đ3 và các khung chương, hoặc chỉ chỗ cần sửa trước khi thu giọng.
2. **Mật độ chữ trên hình:** 69 dòng chú thích + 37 thẻ (một phần được thêm để đạt luật nhịp, mỗi dòng gắn vào câu đang nói). Giữ để người chấm mù ở bước Dựng đánh dấu chỗ thừa, hay yêu cầu cắt bớt ngay (sẽ phải thay bằng biến cố máy/vật để giữ nhịp ≤ 6 s).
3. **Thư NFTC (T2-DOC-2):** một câu trích của văn bản tư nhân, dùng theo sử dụng hợp lý. Xác nhận cho bản bán phim, hoặc thay bằng chú thích chữ (không hiện trang thư).
4. **Footage:** giữ 0 %, hay dò đoạn NARA Liberty (≤ 8 s, khung trong khung) ở bước Dựng.
5. **Lịch (J6, đăng trước 9/11/2026):** sau khi duyệt G1b: tra lại phí Section 301 → thu giọng (9 849 ký tự) → nháp 540p → Dựng (bản đồ nhịp, J/L, nhạc theo nhịp, người chấm mù đánh dấu chỗ muốn bỏ, sửa 1 lượt) → 1080p một lần → RÀ LUẬT + RÀ GU (§8) → G2.
