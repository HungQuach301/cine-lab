# Tập thử K2G-01 — ngách G "Quyền lực kinh tế qua ba tầng" — báo cáo G1 (11/10/2026)

> Phiên P kênh 2. Nhánh `k2g-ep01` (từ `origin/channel-k2` @ `1174239`). **DỪNG ở G1, chờ chủ dự án duyệt.**
> **Ngách G chưa chốt** (vòng đo 5 ngách ra ~14:00 ngày 12/10). Theo lệnh: **không** thu giọng ElevenLabs (0 ký tự), **không** chọn nhạc, **không** gọi YouTube Data API (0 lượt), **không** dựng 1080p (ngoại lệ đo giờ máy, xem §8).
> Mọi chỉ số giữ chân, điểm chấm trong tài liệu này là **tự đo bằng người đọc mô phỏng (AI), không phải chỉ số YouTube**.

Tệp của mốc: `channel-k2/LUAT-NOI-DUNG-G.md` · `channel-k2/k2g-ep01/script.md` (lời khoá ứng viên v3.7) · `k2g-ep01/claims.md` (nguồn + 75 claims) · `k2g-ep01/kiem-mu/` (toàn bộ kết quả kiểm mù, REVIEWER, sổ chi phí) · `k2g-ep01/khung/` (6 khung mẫu) · `design/ll-hero/k2g01.js` (6 cảnh 3D) · `k2g-ep01/ai.py` (mã kiểm mù).

---

## 1. Luật nội dung bổ sung cho G — `LUAT-NOI-DUNG-G.md`
Bổ sung (không thay) `LUAT-NOI-DUNG.md`. Bảy mục:
- **§0 Cấu trúc ba tầng** thay bảng 6 phần của HIEN-CHUONG: móc ≤ 0:15 → bối cảnh + miễn trừ → tầng 1 (~35 %) → tầng 2 (~30 %) → tầng 3 (~20 %, chỉ khi có nguồn) → sợi dây + kết (~8 %).
- **§1 Không thuyết âm mưu**: cụm từ cấm; nhân quả chỉ khi nguồn nêu; văn bản mật thì nói "has not been made public", không đoán.
- **§2 Không gán động cơ/quyền lực ngầm cho nhóm sắc tộc, tôn giáo, gia tộc, quốc gia**; chủ thể là tổ chức/người có tên; lời tự thuật đánh dấu "he wrote".
- **§3 Nhịp "huyền thoại vs hồ sơ"**: nêu lời đồn trung tính, đặt tài liệu gốc cạnh nó, kết luận đúng mức; phải ghi lời đồn **thấy ở đâu** (chống người rơm); 1–3 nhịp/tập.
- **§4 Sản phẩm tài chính/kinh tế mới**: chỉ cơ chế, câu miễn trừ ở **mọi** tập G, phép tính minh hoạ gắn nhãn và nói khác gì số thực trả.
- **§5 Sự kiện đang diễn ra**: "as of" trong lời và trên hình; không dự đoán; tra lại trạng thái trước khi thu và trước khi đăng.
- **§6 Người còn sống, công ty đang hoạt động**: chỉ sự kiện có nguồn; trích nguyên văn kèm người nói và ngày; chính sách thì ghi **ai** đánh giá.
- **§7** 5 luật máy kiểm được, đề xuất gửi K (chưa sửa `checks/`).

**Ưu:** khoá trước rủi ro lớn nhất của ngách (âm mưu, định kiến, YMYL); REVIEWER dùng được ngay (đã dùng 9 lượt). **Nhược:** loại các góc "ai giật dây" hút view. **Tác động:** đặc tả tập G cần trường `as_of`, `myth/record`. **Rủi ro:** nhắc lời đồn để bác vẫn có thể lan; tập lỗi thời nhanh khi chính sách đổi.

## 2. Chọn đề tài thử — **chốt "Steel"**
| Tiêu chí | **Steel** (Carnegie/Pittsburgh → thép là sức mạnh quốc gia → thuế 232, Nippon–U.S. Steel → CBAM, thép hydro) | **The Dollar** (Morgan/1907 → Bretton Woods → trừng phạt/dự trữ → stablecoin/CBDC) |
|---|---|---|
| Nguồn chính thức có sẵn | **Đã đọc toàn văn 21 nguồn** trong phiên: USGS DS140, worldsteel 2026, 5 tuyên bố Federal Register, CRS R48872, OECD Steel Outlook 2026, EUR-Lex (2026/1384, 2023/956), 2 trang Uỷ ban châu Âu, SEC 10-K, hồi ký Carnegie (1920) | Có (Fed History về 1907, Office of the Historian về Bretton Woods, IMF COFER: dollar 56,70 % dự trữ Q2 2026 theo bản tin IMF 30/09/2026 — **chỉ thấy qua kết quả tìm kiếm, chưa đọc toàn văn**); luật stablecoin Mỹ **chưa tra** trong phiên |
| Hợp 3D (NHAN-DIEN "mô hình kỹ thuật sống") | **Rất hợp**: lò, quặng, tàu hồ, ray, thỏi thép — vật chất, có số nổi trên vật thể | Trừu tượng (sổ sách, mạng thanh toán); bộ "đường ống tiền" trùng hình với đề tài card-networks đã có trong hàng đợi |
| Rủi ro âm mưu / định kiến | **Thấp**: lời đồn chính là "thép Mỹ đã chết", "chính phủ sở hữu U.S. Steel" | **Rất cao**: Jekyll Island/Fed "cuộc họp bí mật", định kiến về gia tộc ngân hàng, "petrodollar", "BRICS thay dollar" — chạm thẳng luật G §1–2 |
| YMYL | **Thấp–vừa** (CBAM là cơ chế thuế biên giới, không phải sản phẩm đầu tư) | **Cao** (stablecoin/CBDC dễ bị đọc thành lời khuyên tiền mã hoá; dự báo "phi dollar hoá") |
| Pháp lý | Vừa: U.S. Steel, Nippon Steel, Stegra đang hoạt động → chỉ sự kiện có nguồn | Vừa–cao: tổ chức phát hành stablecoin, đối tượng bị trừng phạt cụ thể |
| Tốc độ lỗi thời | Nhanh (thuế 232 đổi 4 lần trong 16 tháng; Stegra đổi trạng thái giữa lúc làm) | Nhanh (COFER theo quý; luật stablecoin đang triển khai) |

**Lý do chốt Steel:** nguồn chính thức đọc được toàn văn ngay trong phiên; hợp 3D nhất; rủi ro âm mưu và YMYL thấp nhất — đúng điều kiện để thử khung ba tầng mà không vướng luật G §1–2. **Dự phòng The Dollar** giữ cho tập sau, khi luật G đã chạy qua một tập.
- **Ưu:** đi được trọn ba tầng có nguồn; hình mạnh. **Nhược:** tầng 2 nặng văn bản pháp lý (dễ dày số). **Tác động:** tập đầu G làm sẵn bộ cảnh công nghiệp dùng lại cho các đề tài ngành khác. **Rủi ro:** thuế quan đổi trước khi đăng → bắt buộc tra lại (§5 luật G).

## 3. Nguồn và claims — `k2g-ep01/claims.md`
- **22 nguồn** (bảng §1), truy cập 11/10/2026, ghi rõ cách đọc. Ngoại lệ đã ghi: oecd.org trả 403 → đọc PDF y nguyên ở bản sao (ISBN, DOI khớp); tin Stegra 30/09/2026 chỉ có qua Tech.eu + Finwire (chưa tìm thấy thông cáo gốc).
- **75 dòng claims** `fact / opinion / calc`, có `src`; 7 dòng gạch bỏ (đã cắt khỏi lời) giữ lại để truy vết; mục §3 ghi **nơi thấy 3 lời đồn**.
- Tra trạng thái "as of" thật: Federal Register API (tuyên bố thép mới nhất 01/06/2026), EUR-Lex, trang giá CBAM (Q3 2026 = 82,32 €/t CO₂, công bố 05/10/2026), tin Stegra.
- **Phát hiện khi làm**: (a) Stegra đổi trạng thái 30/09/2026 (cần thêm vốn, đổi CEO) — lời v2 dựa trên thông cáo tháng 6 đã **lỗi thời**; (b) phép tính €/tấn ở v1–v3.3 nhân cường độ CO₂ của worldsteel với giá CBAM là **trộn cơ sở** (CBAM tính thép chỉ theo phát thải trực tiếp — Phụ lục II quy định 2023/956) → đã bỏ, thay bằng câu cơ chế.

## 4. Lời — `k2g-ep01/script.md` (khoá ứng viên v3.7)
**Móc (0:00–0:13):** *"In 1950, America made about eighty-eight million tonnes of steel — almost half the world's. In 2025: about eighty-two million. Just about four percent. So why is steel now guarded like a weapon?"* → **kết** trả lời: quyền lực thép là tỷ phần + kiểm soát con đường, không chỉ tấn; đóng vòng hình ở nhà máy Edgar Thomson (Braddock).

| Phần | Đoạn | Từ | Tỷ lệ | Đích luật G §0 |
|---|---|---|---|---|
| Móc | 00 | 32 | 1,2 % | ≤ 0:15 → **12,4 s** @155 từ/phút; **14,5 s** @133 (sát trần 15 s, nêu theo luật ±5 %) |
| Bối cảnh + miễn trừ | 01 | 100 | 3,9 % | 6–8 % (thấp hơn 2,1–4,1 điểm, trong ±5) |
| Tầng 1 lịch sử · cơ chế · địa lý | 02–06 | 838 | 32,4 % | ~35 % |
| Tầng 2 địa chính trị 2018–2026 | 07–09 | 787 | 30,4 % | ~30 % |
| Tầng 3 CBAM + thép hydro | 10–11 | 538 | 20,8 % | ~20 % |
| Sợi dây + kết | 12–13 | 291 | 11,3 % | ~8 % (cao hơn 3,3 điểm, trong ±5) |

- **Tổng 2 586 từ → 16,7 phút ở 155 từ/phút** (nhịp kể thường gặp); **18,5 phút ở 140 từ/phút**; 19,5 phút ở nhịp Bill (133). Khung 14–18 phút: **đạt nếu giọng ≥ 144 từ/phút**. Giọng kênh 2 chưa chọn → đo khi thu mẫu. Nếu giọng chậm hơn: cắt dự phòng ~80 từ (đoạn 06 câu bối cảnh OECD 1970s 24 từ, đoạn 08 câu "echoes" 12 từ, đoạn 09 hai câu "Our read: Carnegie's firm…" 35 từ, đoạn 03 câu đá vôi 11 từ) — mỗi câu cắt được mà không đổi số neo; cần REVIEWER xác nhận lại sau cắt.
- **Câu miễn trừ** ở 0:12–0:16 (≤ 30 s).
- **3 nhịp huyền thoại vs hồ sơ**: "thép Mỹ đang chết" (06), "golden share = chính phủ sở hữu" (09), "thép xanh đã có / chỉ là quảng cáo" (11).
- **Phép tính riêng của kênh** (nhãn "our calculation"): tỷ phần 46 % → 4 %; 4 tấn vật liệu/tấn thép; thế giới ×9,8; xuất khẩu TQ (131 Mt) > sản lượng Mỹ (82 Mt) theo khối lượng; Mỹ −7 % so với 1950.
- **Chính trị trung lập**: lệnh Biden và Trump nêu ngày, không đánh giá; kết quả thuế quan quy cho chính văn bản ("the proclamation credits…") và cho CRS (hai phía nghiên cứu).

## 5. Kiểm mù và REVIEWER
**Cách làm:** `ai.py` gọi `claude -p` ghim model, chạy trong thư mục trống (người đọc không thấy repo), không subagent. 3 người đọc mù `claude-sonnet-5-5` (R1 khán giả phổ thông, R2 người hoài nghi "agenda", R3 người hiểu ngành thép) chỉ nhận lời. REVIEWER `claude-opus-5-5` nhận lời + 2 bộ luật + bảng claims. Model thực chạy ghi trong `cost.jsonl` (đúng model ghim; CLI thêm Haiku cho tác vụ phụ).

| Vòng | Móc (R1/R2/R3) | Nối 3 tầng | Tin cậy | Kết trả lời móc | Thấy âm mưu | Thấy lời khuyên tài chính | REVIEWER |
|---|---|---|---|---|---|---|---|
| v1 | 6 / 7 / 7 | 7 / 7 / 7 | 7 / 6 / 7 | 3/3 | 0/3 | 0/3 | lock_with_fixes · **13 major**, 21 minor |
| v2 | 7 / 7 / 7 | 7 / 6 / 7 | 7 / 7 / 7 | 3/3 | 0/3 | 0/3 | lock_with_fixes · 6 major |
| v3 | 7 / 7 / 8 | 7 / 6 / 7 | **8 / 7 / 7** | 3/3 | 0/3 | 0/3 | 4 major |
| v3.1 → v3.5 | — | — | — | — | — | — | 3 → 3 → 4 → 1 → 2 major (mỗi lượt sửa lộ lỗi câu mới, giảm dần) |
| **v3.6** | — | — | — | — | — | — | **0 major**, 17 minor → đã áp hết thành **v3.7** |

**Sửa chính theo người đọc mù (≥ 2/3 cùng nêu):** câu móc "nearly as much" mơ hồ (3/3) → nói thẳng hai số; thiếu mặt chi phí của thuế (3/3) → thêm hai phía nghiên cứu CRS; thiếu đoạn suy thoái 1973–82 (2/3) → thêm USGS 137 → 68 Mt + bối cảnh OECD; "veto" quá rộng → "consent rights"; ẩn dụ "path" không hợp carbon (2/3) → tách "path" và "toll".
**Sửa chính theo REVIEWER:** nhân quả không nguồn (thuế ← tỷ phần giảm; Homestead ← tích hợp dọc); golden share "was used" → Nhà Trắng nói đã dùng *đe doạ*; mốc "as of" cho mọi sự kiện mở; bỏ tự chấm đạt/trượt mục tiêu 80 %; bỏ phép tính €/tấn trộn cơ sở; Stegra quy lời cho báo; "Carnegie bought the path" → chỉ nguồn cốc (có nguồn).
**Còn nhắc lại (cả 3 vòng mù):** đoạn 07, 08, 10 vẫn **dày số** → xử ở hình: mỗi số neo một khung riêng, dòng thời gian thuế quan thành một đồ hoạ, số phụ lên hình thay vì lời. Điểm "lệch" người đọc nêu đi **cả hai chiều** (chống Carnegie / chống TQ / hoài nghi thuế quan) — dấu hiệu cân bằng, không phải một phía.
**Chưa chạy mù lại trên v3.7** (chỉ đổi câu chữ sau v3); đề xuất chạy 1 vòng mù cuối khi chủ dự án duyệt lời.

## 6. Khung 3D mẫu — `k2g-ep01/khung/` (960×540, SPP1), mã `design/ll-hero/k2g01.js`
| Khung | Cảnh | Dùng cho | Ghi chú |
|---|---|---|---|
| `01-valley` | Thung lũng sông chạng vạng: 3 lò cao + lò gió nóng, nhà xưởng mái răng cưa, ống khói có khói động, sông phản chiếu ánh lò, cầu giàn, thị trấn trên đồi, đoàn toa quặng | móc, đoạn 02, kết | xưởng/thành phố công nghiệp chạng vạng |
| `02-ingots` | Sa bàn thỏi thép (1 thỏi = 10 Mt): 1950 (19 thỏi, Mỹ 9 cam) cạnh 2025 (185 thỏi, Mỹ 8 cam); nhãn số và nguồn trên khung | móc, huyền thoại #1 | số nổi trên vật thể |
| `03-chain` | Bản đồ tuyến giản lược Hồ Lớn: quặng → ray → tàu hồ → ray → Pittsburgh; cốc Connellsville; tuyến vẽ dần | đoạn 03 | **bản đồ tuyến thương mại**; ghi "Simplified map", nguồn Carnegie 1920 |
| `04-furnace` | Xưởng Bessemer: lò chuyển nghiêng rót thép lỏng, tia lửa, cầu trục, bóng người ánh viền | đoạn 02–04 | không mặt người |
| `05-trade` | Sa bàn thương mại 2025–26: bệ sản lượng TQ/EU/Mỹ, cung xuất khẩu 131,2 Mt, tường thuế 50 % (as of Oct 2026), cổng hạn ngạch EU 18,3 Mt, khối nét đứt hổ phách 745 Mt **PROJECTION** | đoạn 07–08 | nhãn dự báo đúng NHAN-DIEN |
| `06-north` | Phương bắc giờ xanh: tháp khử hydro, nhà điện phân, xưởng lò hồ quang, tua-bin gió, rừng thông tuyết; nhãn CO₂ theo tuyến | đoạn 10–11 | xanh lục lam = dòng "sạch" |

- Nhận diện: bảng màu và chữ Inter theo NHAN-DIEN; hậu kỳ riêng (`GRADE_K2`, không vân vải giấy) truyền dạng object — **không sửa `kit.js`/`page.js`** của LL. Đã soát từng khung (3 lượt dựng thử: sửa máy quay sau đồi, khối trụ che lò, nhãn quá nhỏ).
- **Còn yếu (đưa vào bước dựng):** nhãn nhỏ ở `trade`/`north` khi xem 960×540; nội thất và mặt nhà còn khối trơn (BAI-HOC #97: cần vân vật liệu); `valley` cần thêm chi tiết bờ sông. Hình chưa có dòng "Facts as of" và nhãn nguồn USGS/worldsteel ở đoạn 00, 13 (REVIEWER yêu cầu).
- **Chưa thêm Inter vào `RIGHTS.md`**: khung mẫu nội bộ, chưa là sản phẩm (NHAN-DIEN §3: thêm khi dùng lần đầu trong sản phẩm).

## 7. Ước giờ máy bản đầy đủ (đo thật)
| Đo | Kết quả |
|---|---|
| 960×540 SPP1, 24 khung/cảnh, 6 cảnh | 0,27 (chain) – 0,48 (valley) s/khung; trung bình **0,36** |
| 1920×1080 SPP4, 12 khung/cảnh, 2 cảnh | **2,08** (furnace) – **3,19** (valley) s/khung |
Giả định: tập 16,7 phút = 24 048 khung; ~85 % thời lượng là cảnh 3D (≈ 20 400 khung).
- **Nháp 960×540:** cảnh 3D ≈ 2,0 giờ + ghép/render chữ ≈ 0,5–1 giờ → **≈ 2,5–3 giờ máy**.
- **Bản 1080p SPP4:** cảnh 3D ≈ 15 giờ một luồng (11,8–18,1 theo cảnh nhẹ/nặng); chạy 2 luồng (`heroes_par.sh` trên `main`) ước 8–10 giờ; + ghép, mã hoá ≈ 1,5–2 giờ → **≈ 10–17 giờ máy**. Cảnh thật chi tiết hơn mẫu (BAI-HOC #97) có thể +20–40 %. Chạy bằng `setsid nohup` (BAI-HOC #102).

## 8. Chi phí đo và tuân thủ
| Hạng mục | Số đo |
|---|---|
| AI `claude -p` (sổ `kiem-mu/cost.jsonl`) | **$6,12 / trần $10** (dừng ở $9): Sonnet 9 lượt $0,75 · Opus REVIEWER 9 lượt **$5,37** |
| ElevenLabs | **0 ký tự** (không thu) |
| YouTube Data API | **0 lượt** |
| Token phiên P (log phiên, khử trùng theo mã tin nhắn, đo lúc viết báo cáo) | sinh ~0,16 triệu; ghi cache ~0,37 triệu; đọc cache ~34 triệu (sẽ tăng thêm ít ở bước commit) |
| Giờ máy dựng | 6 cảnh × (3 lượt thử + 24 khung đo) ở 960×540 + 24 khung 1080p đo giờ |
- **Ngoại lệ cần chủ dự án biết:** (1) đã dựng **24 khung 1080p SPP4** (2 cảnh × 12) **chỉ để đo giờ máy**, không dùng vào sản phẩm, đã bỏ — nếu lệnh "không dựng 1080p" bao gồm cả việc này thì đây là sai lệch của tôi; (2) một lần gọi SEC EDGAR (tra 10-K) tôi đã để **email chủ dự án trong User-Agent** — sai, các lần sau đổi sang chuỗi chung; (3) `channel-k2/.gitignore` thêm ngoại lệ để commit kết quả kiểm mù (`kiem-mu/*.json`, không có dữ liệu YouTube hay khoá); (4) mã cảnh đặt ở `design/ll-hero/k2g01.js` vì driver `hero.js` chỉ đọc thư mục này (không sửa driver).
- Không in khoá; khoá chỉ nằm trong môi trường tiến trình con.

## 9. Đề xuất (chờ duyệt)
| # | Đề xuất | Ưu | Nhược | Tác động | Rủi ro |
|---|---|---|---|---|---|
| D1 | **Chốt đề tài Steel** cho tập thử G (nếu ngách G thắng vòng đo) | nguồn đủ, hình mạnh, rủi ro thấp | tầng 2 dày văn bản | mở bộ cảnh công nghiệp dùng lại | thuế quan đổi trước khi đăng |
| D2 | **Duyệt lời v3.7** làm lời khoá; chạy 1 vòng mù cuối + tra lại trạng thái (FR, EUR-Lex, CBAM, Stegra, U.S. Steel) ngay trước khi thu | đã qua 9 lượt REVIEWER, 0 major | 16,7 phút chỉ đạt nếu giọng ≥ 144 từ/phút | khoá được bảng shot | sự kiện đổi giữa lúc dựng |
| D3 | **Ban hành `LUAT-NOI-DUNG-G.md`** và gửi K 5 luật máy (§7) khi K mở | bắt lỗi âm mưu/định kiến/mốc thời gian bằng máy | thêm việc cho K | REVIEWER bớt việc lặp | regex bắt nhầm |
| D4 | **Dựng 8 bộ cảnh** (6 mẫu + 2 mới: cảng/hải quan cho thuế quan, nhà máy hiện đại ban ngày cho Granite City) để đạt luật #96 (không cảnh > 25 % hay > 90 s liên tục; nửa sau ≥ 2 bối cảnh) | đa dạng hình | +~1 ngày làm cảnh | nháp 2,5–3 giờ máy | SwiftShader chậm hơn ước nếu thêm chi tiết |
| D5 | **Viết lời từ đầu kèm danh sách lỗi REVIEWER hay gặp** (nhân quả, "as of", quy chủ thể, khác cơ sở) để bớt vòng Opus | Opus chiếm 88 % chi phí AI ($5,37); 9 lượt mới hội tụ | — | rút còn ~3–4 lượt | REVIEWER mỗi lượt vẫn sinh minor mới (không về 0) → tiêu chí dừng: **0 major** |
| D6 | **3 bài học mới** đề xuất thêm BAI-HOC: (a) giá CBAM × cường độ worldsteel là khác cơ sở; (b) sự kiện "đang diễn ra" có thể đổi trong 3 tuần (Stegra) → tra lại ngay trước khi khoá; (c) REVIEWER không hội tụ một lượt — dừng ở 0 major | tránh lặp lỗi | — | — | — |

## 10. Việc đang chờ chủ dự án
1. Kết quả vòng đo 5 ngách (~14:00 12/10): ngách G có được chốt không.
2. Duyệt đề tài **Steel** (D1) và **lời v3.7** (D2) — quyết định sáng tạo then chốt, cần ghi `AUTHORSHIP.md` kèm đóng góp biểu đạt của chủ dự án (chưa ghi, chờ duyệt).
3. Duyệt `LUAT-NOI-DUNG-G.md` (D3).
4. Sau khi chốt ngách: chọn giọng (3 ứng viên trong NHAN-DIEN §4, cần đo tốc độ đọc cho khung 14–18 phút), nguồn nhạc, cho phép dựng 1080p.
5. Xác nhận việc dựng 24 khung 1080p chỉ để đo (§8) có chấp nhận được không.
