# TIỀN KỲ T4 — "Why Las Vegas grew in a desert" (K2C-T4-01)

> Phiên Tiền kỳ T4, 15/10/2026. Lệnh chủ dự án duyệt 15/10 (U2, U3); bổ sung 22:47 (ngôn ngữ hình xương sống) và điều chỉnh 22:54 (footage là kho lựa chọn).
> Nhánh `k2c-t4-tienky` từ `origin/main` @ `7255aa4`. **Không merge.**
> Mọi lượt xem là **số công khai YouTube Data API, đọc ngày 15/10/2026 (UTC)**. Mọi tỷ lệ, xếp hạng, trọng số và bội số là **tự tính, không phải chỉ số YouTube**.
> Mọi trích dẫn đều chép **nguyên văn** từ tệp tải bằng curl rồi tách chữ (trừ 2 claim gắn cờ OCR/ảnh quét). SHA-256 ghi trong `tienky/neo.json`, `claims.json`, `nguon-tep.json`, `tai-san.json`. Tệp thô để ngoài git.

## 0. Khối điều lệ (chép lệnh, thêm cột thực tế)
| Trường | Lệnh | Thực tế |
|---|---|---|
| Loại phiên | Tiền kỳ (tập T4, bước Đóng gói) | như lệnh |
| Nhánh | `k2c-t4-tienky` từ `origin/main` | `7255aa4`; đã đẩy nhiều lần (stop-hook đòi đẩy tệp mới) |
| Tệp được sửa | `channel-k2/k2c-t4-01/TIEN-KY.md`, `tienky/*.json`, `licenses/` | như lệnh: 1 tệp md, 14 tệp `tienky/*.json`, 43 tệp `licenses/`. Không sửa mã, `checks/`, `design/`, `scripts/`, tệp T2/T3. **Không ghi COST-LEDGER, RIGHTS, AUTHORSHIP** (ngoài vùng; §13) |
| Trần | YouTube ≤ 300 đơn vị · Claude API ≤ $2 (ghim model) · ElevenLabs 0 | **292 đơn vị** · **$0,0213** (`claude-haiku-5-5`, 4 lượt, model thực chạy = haiku cả 4) · **0 ký tự** |
| Preflight | bắt buộc; che email trong giấy phép | `verify.sh`: 9 PASS, 4 FAIL không liên quan (three.js, tifffile/pyshp, k2v node_modules, Freesound). `tools/preflight.sh --range origin/main..HEAD`: **ĐẠT**; `lock.py --verify`: **KHỚP**. 0 email trong 43 tệp giấy phép (§14) |
| Điều kiện dừng | xong việc → đẩy → dừng; không dừng hỏi giữa chừng | (1) xong việc |

## 1. Tóm tắt và khuyến nghị
**Khuyến nghị: ĐI TIẾP Las Vegas / lưu vực Colorado ở mức XANH, nhưng ĐỔI GÓC.** Không làm câu hỏi "vì sao Las Vegas tồn tại giữa sa mạc" theo nghĩa đen. Lý do: góc này đã có ba người làm, và một trong ba vừa làm đúng dạng hình của mình 8 ngày trước:

| Đã có | Kênh · ngày · lượt xem | Trùng với mình ở đâu |
|---|---|---|
| "How Las Vegas Exists in America's Driest Desert" | RealLifeLore · 07/2022 · **4 143 198** · 18,6 phút | trùng **câu hỏi**; hạng 1 của S1 |
| "Las Vegas Shouldn't Exist — Here's Why It Does" | Geography Effect · 04/2026 · 47 675 · 8,3 phút | trùng **câu hỏi** (khung "đập + luật cờ bạc + gần LA") |
| "EVOLUTION OF LAS VEGAS \| 3D CITY TIMELAPSE (1855–2026)" | Cornerstone Timelapse · **07/10/2026** · **494 376** sau 8 ngày | trùng **hình xương sống** (casino mọc/phá theo năm). Không có nước, Lake Mead hay cơ chế |
| "Las Vegas Isn't the Real Lake Mead Problem — California Is" | US Weather Alert · 26/09/2026 · 452 111 · 23 phút | trùng **cặp tương phản** Las Vegas ↔ nông nghiệp California (theo mô tả; kênh không nêu nguồn) |

**Góc đề xuất (chưa ai làm có nguồn):** *thành phố mọc lên, cái hồ tụt xuống, trong cùng một khung hình, cùng một bộ đếm năm.* Câu hỏi là vì sao cả hai cùng xảy ra. Câu trả lời nằm ở **cơ chế chia nước**: tờ giấy 1922, cái đập 1931–1936, ống nước 1971, nước thải được tính lại, và quyết định 21/08/2026.

**Lý do đi tiếp (không đổi đề tài):**
- **Neo thời sự mạnh hơn mong đợi**, và đều có nguồn gốc:
  - Lake Mead xuống **1 037,54 ft ngày 14/10/2026**. Hồ phá kỷ lục 2022 (1 040,58 ft) từ ngày 06/08/2026. Lần gần nhất hồ thấp hơn mức này là **21/04/1937**, khi hồ còn đang tích nước lần đầu (dữ liệu HDB của USBR; P đã tự kiểm tệp).
  - ROD ngày 21/08/2026 áp khung 2027–2036. Từ 2027 Nevada còn **250 000 af** (cắt 50 000). Nevada và SNWA kiện ngày 24/08/2026.
  - Lệnh cấm tưới "cỏ không chức năng" bằng nước Colorado (AB 356) có hiệu lực **01/01/2027**.
  - Từ đó có hai **"điều cần theo dõi"** có ngày cụ thể: mức cắt có hiệu lực ngày 01/01/2027, và vụ kiện.
- **Cầu đạt, và đang nóng:**
  - Cầu-bền: 4,14 triệu lượt.
  - Nhiều video dài ≥ 500 nghìn lượt trong 90 ngày (Sin City Outdoors 726 nghìn; The Infographics Show 512 nghìn; Cornerstone 494 nghìn).
  - Cầu-ngách: 7 video dài cỡ 10–100 nghìn lượt trong 90 ngày.
- **Khoảng trống đạt rõ:**
  - 0/5 video đầu dẫn nguồn số liệu. Haiku đánh 1/5, nhưng đó là ghi công footage, không phải nguồn số.
  - Cung 2026 dày đặc kênh giật gân ("DROPS TO 20%", "DEAD POOL", "RUNS OUT"), không nguồn.
  - Đây đúng là chỗ lợi thế "with the receipts" phát huy.
- **Tranh luận số 1 của khán giả là món quà cho góc mới.** Bình luận nặng nhất dưới video RealLifeLore (trọng số 5 824): đừng đổ cho Vegas, lỗi ở tuyết và nông nghiệp California. Mình trả lời bằng số kế toán nước của USBR (C30, C47), không bằng ý kiến.
- **Dữ liệu xương sống đủ để dựng "vùng đô thị mọc theo năm" 1905 → 2026** với giấy phép sạch (CC0/PD), và có chuỗi mực hồ hằng ngày 1935 → 2026. "Mỗi toà nhà mọc đúng năm" thì **không** dựng được cho cả thung lũng (§10).

**Điểm yếu cần biết:**
- **Rủi ro bị xem là bản sao** của Cornerstone (hình) và RealLifeLore/Geography Effect (câu hỏi). Giảm bằng ba cách:
  1. Không dựng chuỗi casino mọc/phá kiểu Cornerstone.
  2. Tiêu đề không dùng "exists / shouldn't exist".
  3. Bộ đếm kép (dân số + mực hồ) và cảnh hồ cùng khung là thứ không ai có.
- **Cửa sổ ngắn.** Latos Charts (3D timelapse thành phố, Prague 1,14 triệu trong 10 ngày) vừa sang thành phố Mỹ (New York 15/10). Cung Lake Mead đổi theo tuần. Nên phát hành trước 01/01/2027.
- **Ảnh LoC chưa tải được bản gốc.** Quyền đã đọc qua JSON cho 17 item, nhưng `tile.loc.gov` trả 520 từ 16:20 UTC tới lúc kết phiên. Ảnh NARA, USGS, Landsat, NAIP và 2 phim đã tải thật, có SHA.
- **Vụ kiện đang mở.** Không làm trục tập; nhắc một lần, có "as of" và lập trường hai phía (§8).

**Đề tài XANH dự phòng** (chỉ dùng nếu chủ dự án không muốn đổi góc): **đường sắt cao tốc Tây Ban Nha** (Teardown #5, XANH).
- 0/13 kênh trong kho có video về đề tài này (§3).
- Xương sống thời gian tự nhiên: mạng AVE mọc theo năm 1992 → 2026, bộ đếm khách.
- Chưa đo search.list: cần một phiên tiền kỳ riêng (~200 đơn vị).

## 2. Bước 1 — Neo nguồn gốc (chi tiết: `tienky/neo.json`)
| # | Neo (lệnh) | Kết luận | Nguồn gốc · as of | Trích nguyên văn |
|---|---|---|---|---|
| N1 | ROD Interior/USBR 21/08/2026, khung 2027–2036 | **ĐÚNG.** Bộ trưởng Burgum ký 21/08/2026. Khung 10 năm 2027–2036; hướng dẫn vận hành ra theo từng đợt 2 năm, đợt đầu 2027–2028. Lower Basin bị cắt 1,25 maf/năm: AZ −760 000, CA −440 000, NV −50 000 | DOI ROD (P26_RecordofDecision_Final.pdf) + Operating Guidelines 2027–2028 §5.3.A.2 · 21/08/2026 | "Unfortunately, as of the publication of this Record of Decision (ROD), consensus on long-term operations has not been reached." · "250,000 acre-feet (af) shall be apportioned for use in Nevada, reflecting reductions of 760…" |
| N2 | Compact 1922: 7,5 triệu af/năm mỗi lưu vực | **ĐÚNG.** Ký ở Santa Fe 24/11/1922. Điều III(a), (b) thêm 1 triệu cho Lower Basin, (c) Mexico. Hoover "participated in", **không phải "chủ trì"** | crcompct.pdf (USBR) · 24/11/1922 | "(a) There is hereby apportioned from the Colorado River System in perpetuity to the Upper Basin and to the Lower Basin, respectively, the exclusive beneficial consumptive use of 7,500,000 acre-feet of water per annum" |
| N3 | Nevada 300 000 af (BCPA / Arizona v. California) | **ĐÚNG về số, SỬA về nguồn ấn định.** BCPA 1928 §4(a) chỉ "authorized" một hiệp định ba bang, và hiệp định này không thành. Con số được Toà Tối cao xác định (373 U.S. 546, 1963) và ấn định ở Decree 376 U.S. 340 (1964), Điều II(B)(1). Consolidated Decree 2006 giữ nguyên | GovInfo 43 U.S.C. 617c; U.S. Reports (LoC) | BCPA: "there shall be apportioned to the State of Nevada 300,000 acre-feet and to the State of Arizona 2,800,000 acre-feet" |
| N4 | Mực Lake Mead mới nhất | **ĐÚNG. Kỷ lục thấp mới năm 2026 (neo thời sự chính)**: 1 037,54 ft ngày 14/10/2026. Lần đầu dưới kỷ lục 2022 là ngày 06/08/2026 (1 040,50). Đỉnh đo được 1 225,83 ft (24/07/1983). Dead pool 895 ft (SNWA). Lake Powell cũng lập kỷ lục thấp: 3 516,62 ft ngày 15/09/2026 | USBR HDB lchdb SDI 1930 (CSV 1935–2026, SHA `26cc8533…`) · 14/10/2026 | "10/14/2026 00:00, 1037.54" |
| N5 | Hoover Dam 1931–1936 | **SAI MỘT PHẦN theo cách nói thường gặp.** Khởi công 20/04/1931; FDR khánh thành 30/09/1935; mọi hạng mục xong 01/03/1936. Số chết "chính thức" là 96, không phải 112 (112 gộp cả các ca từ 1922). Tên Hoover Dam chính thức trở lại năm 1947 | USBR fatal.html, FAQ; Census "History: Hoover Dam" | "The "official" number of fatalities involved in building Hoover Dam is 96." |
| N6 | Hiệp ước 1944 với Mexico | **ĐÚNG.** Điều 10(a): 1 500 000 af/năm. Minute 334 ký 02/09/2026, thay Minute 323 và 330; Mexico nhận ít hơn 250 000 af/năm trong 2027–2028 | mx1944.pdf; thông cáo IBWC · 09/09/2026 | "Minute 334 … "Colorado River Basin Cooperative Measures through December 31, 2028," was signed on September 2, 2026" |

**Kiểm các tin địa phương thấy trong hồ sơ cầu:**
- Mưa bão: NHC ghi là **Hurricane Rachel (EP18)**. Advisory cuối ngày 11/10/2026 là cho tàn dư ở 35,8N 114,6W. Mực hồ chỉ tăng **+0,06 ft** (C46). Thiệt hại lũ ở Las Vegas chưa có nguồn NWS, nên không dùng.
- "California's first water cut in history": không có văn bản chính quyền nào nói "first". Chỉ dùng con số −440 000 af.

## 3. Bước 2 — Hồ sơ cầu (`tienky/cau.json`, `kho-kenh.json`, `binh-luan.json`, `khoang-trong.json`)
**Cách đo:**
- 2 lượt `search.list` (type=video, order=relevance, 50 kết quả, en/US, không giới hạn ngày):
  - S1 "why is las vegas in the desert";
  - S2 "las vegas water|lake mead": câu hỏi thứ hai và thứ ba của lệnh gộp bằng toán tử `|` để giữ trần 300 đơn vị, như T3.
- `videos.list` cho 99 + 43 video.
- Video timelapse và lưu vực ngoài search lấy mã qua WebSearch giới hạn youtube.com, không tốn quota.

| Nhãn (LUAT-CHON-DE-TAI) | S1 "why … desert" | S2 "water \| lake mead" | Kết luận |
|---|---|---|---|
| Cầu-bền (top 5 video dài có ≥ 500 nghìn) | **4 143 198** (RealLifeLore, 2022) | lớn nhất 20 646 (top 5 dài toàn là video 2026 vài nghìn tới 20 nghìn) | **ĐẠT** (S1) |
| Nổ-mẫu (≥ 500 nghìn trong 90 ngày) | Storm-HQ 1,36 triệu (lũ, 2 ngày; khác mẫu) | **Sin City Outdoors 726 369** (39,6 phút, 23 ngày); Eric Hanson 1,72 triệu (Short) | **ĐẠT** (S2) |
| Nổ-mẫu ngoài search (cùng lưu vực) | Cornerstone 494 376 (8 ngày) | The Infographics Show 512 350 (11 ngày); US Weather Alert 452 111 (19 ngày) | củng cố |
| Cầu-ngách (video dài 10–100 nghìn trong 90 ngày) | 0 | 7 video (10 472 – 74 518) | **ĐẠT** |

- **Chỉ số nằm trong ±5 % quanh ngưỡng:**
  - Cornerstone **494 376** thấp hơn ngưỡng Nổ-mẫu 500 nghìn **1,1 %**.
  - The Infographics Show **512 350** cao hơn ngưỡng **2,5 %**.
  - Khoảng trống: Haiku đánh **1/5**, đúng bằng ngưỡng ≤ 1/5. P đọc lại thì 0/5.
- **Bình luận** (100 + 20 + 100 bình luận hàng đầu; Haiku gắn nhãn 220/220):
  - RealLifeLore: 10 bình luận thuộc loại hỏi/yêu cầu/sửa sai/tranh luận (3 hỏi hoặc yêu cầu thuần). Trọng số lớn nhất là **tranh luận nguyên nhân 5 824**: "đổ cho Vegas là sai; tuyết và nông nghiệp California mới là nguyên nhân". Tiếp theo là khen "Vegas tiết kiệm nước bất ngờ" (4 856, 2 323).
  - Geography Effect: chỉ có 20 bình luận. Ý nặng nhất là **cảm ơn vì không dùng giọng AI** (28). Có câu sửa sai: "Vegas dùng nước ngầm là chính". Câu này **sai** (C27, C29).
  - The Fault Line (685 nghìn): 24 bình luận thuộc loại hỏi/yêu cầu/sửa sai/tranh luận. Chủ đề nặng nhất là **quá tải dân số / "sao vẫn xây"** (1 007), tiếp theo là nước và mực hồ, cuối cùng là đòi khử mặn và đường ống (256).
- **Kiểm kho** (toàn bộ uploads, 13 kênh, 3 847 video):
  - **Trùng:** RealLifeLore (2022) và Geography Effect (04/2026, cùng loạt Phoenix 92,8 nghìn và "Los Angeles nước của người khác" 45 nghìn).
  - **Kề:** Wendover "California's Water Problem" (03/2026, 873 nghìn); RealLifeLore "Why California is Running Out of Water" (2022, 3,23 triệu). Half as Interesting có 3 video Vegas khác góc (giao thông, quận không người, sổ cấm cờ bạc).
  - **0 video Las Vegas:** FoN, GoDocs, Wendover, PolyMatter, Economics Explained, CaspianReport, Business Casual, Real Engineering, Asianometry, **Latos Charts**. Latos Charts có 15 video 3D timelapse, toàn châu Âu, Dubai và New York.
  - **Ngoài kho:** Cornerstone Timelapse (07/10/2026), InfoGeek 3D 1855–2025 (2,4 phút, 195 nghìn), các timelapse vệ tinh 2013–2022 (≤ 60 nghìn).
  - **Giới hạn:** Modern MBA và Uncover History không quét, giống T3.

## 4. Bước 3 — Nghịch lý, cặp tương phản, nhân vật, chương

### 4.1 Nghịch lý một câu
> **"Since 2002, Las Vegas has added about 876,000 people and cut its water use per person by more than half — and this summer Lake Mead still fell lower than at any time since it first filled. The city everyone blames gets less than two percent of the river; one farm district in California uses eleven times what all of Nevada does."**

- **Vế 1:** SNWA, giảm 58 % mỗi người từ 2002 đến 2025, dân số tăng ~876 000 (C32). Chỉ dùng **tỷ lệ %**, không dùng số GPCD tuyệt đối vì các nguồn mâu thuẫn.
- **Vế 2:** 1 037,54 ft ngày 14/10/2026; "lowest since it first filled" (C40).
- **Vế 3:** 300 000 af trên 16,5 triệu af đã hứa (7,5 + 7,5 + 1,5; C08, N6) **= 1,8 % (tự tính)**. IID tiêu thụ 2 187 165 af, Nevada 197 570 af năm 2025, gấp **11,07 lần** (cùng báo cáo kế toán USBR 2025; C30, C47).

### 4.2 Cặp tương phản (mã màu cố định cả tập — đề xuất, chờ V/chủ dự án)
| Phía | Ai | Số neo | Màu đề xuất |
|---|---|---|---|
| A | Thung lũng Las Vegas (Clark County: 2 407 226 dân, ước 2025) | tiêu thụ 197 570 af (2025); nghèo 12,5 %; thu nhập hộ trung vị $80 047 (2024) | vàng neon ấm (đô thị) |
| B | Imperial Valley (Imperial Irrigation District, Imperial County CA) | tiêu thụ 2 187 165 af (2025); nghèo 18,8 %; $60 477 (2024; Census SAIPE) | xanh lục ruộng → nâu đất |
| Dòng nối | Lake Mead và sông Colorado (một nguồn cho cả hai) | 1 037,54 ft (14/10/2026) | xanh nước, vạch "bathtub ring" trắng |

- Đây là cặp **mạnh nhất bằng số**: đúng tranh luận số 1 của khán giả, và cả hai số đều nằm trong một văn bản của chính phủ.
- **Đã cân nhắc:**
  - Cộng đồng bộ lạc: Colorado River Indian Tribes có quyền chuyển nước theo phán quyết tới 719 248 af/năm (C49) và tiêu thụ nhiều hơn Nevada. Hướng này nhạy cảm, nên chỉ dùng **một câu có số và nguồn**, không làm trục.
  - Navajo "7 gallons/ngày" (C50) nằm trong ý kiến bất đồng trích hồ sơ vụ án. **Đề xuất không dùng**.
  - Châu thổ ở Mexico: dùng làm cảnh chuyển, không làm cặp chính (C51: xung nước 2014).
- Khác US Weather Alert: họ dừng ở câu "California mới là vấn đề". Mình nêu đủ ba điều:
  - (a) IID dùng nước theo quyền hợp pháp có trước, không phải "lãng phí" (giọng trung tính);
  - (b) Imperial lại **nghèo hơn**, tức nhiều nước không đồng nghĩa với giàu;
  - (c) gốc là tờ giấy 1922 chia nhiều hơn lượng sông thực có.

### 4.3 Nhân vật người thật có hồ sơ (5)
| # | Nhân vật | Vai trong mạch | Hồ sơ | Ảnh | Ghi chú rủi ro |
|---|---|---|---|---|---|
| 1 | **Helen J. Stewart** (chủ trại Las Vegas Ranch) | Ch.1: bán đất trại cho đường sắt năm 1902; mảnh đất đó thành downtown | C05 | chưa tìm được ảnh có quyền rõ → A-lite (đạo cụ: ngựa, sổ địa bạ) | người đã mất; trung tính |
| 2 | **Herbert Hoover** (đại diện liên bang, 1922) | Ch.2: có mặt khi bảy bang chia sông trên giấy; cái đập về sau mang tên ông | C09, C21 | LoC 92501271 ("điều kiện" — rights chưa đánh giá; chủ dự án đối chiếu) | nói "participated", không nói "chaired" |
| 3 | **Nhóm "high-scalers"** (21 000 người làm đập; 5 218 người vào ngày đông nhất 06/1934; 96 người chết) | Ch.3: muốn việc làm thời Đại suy thoái; gặp vách hẻm và cái nóng; kết cục: đập xong sớm | C15–C18 | NARA 293766 "High-scalers working on Arizona abutment" (1932, Unrestricted) | không mặt cá nhân làm tiêu điểm; số chết dùng 96 |
| 4 | **Pat Mulroy** (GM SNWA 1991–2014, **còn sống**) | Ch.5: năm 2002, sau 2 năm hạn, "from a reliable 50-year plan" thành thiếu hụt → gỡ cỏ, intake thứ ba | C53 (lời khai Thượng viện 2013) | không dùng ảnh (chưa có ảnh chính thức có điều khoản rõ) | LUAT-NOI-DUNG-G §6: chỉ trích nguyên văn, không suy động cơ |
| 5 | **John Entsminger** (GM SNWA hiện nay, **còn sống**) | Ch.7: "a slow-motion train wreck…" (Thượng viện 2022); đơn vị của ông đang kiện liên bang | C52 (C55 CHỜ XÁC MINH GỐC) | không dùng ảnh | vụ kiện: nêu lập trường hai phía, không đoán kết quả |

- William A. Clark (C02: chọn Las Vegas làm ga chia tuyến vì có suối) chỉ là nhân vật phụ một câu.
- Ảnh LoC 2005688458 của Clark: "điều kiện".

### 4.4 Chương đề xuất (Kinh thánh §3: 9–11 phút, tới 12; ~150 từ/phút) — cấu trúc xương sống thời gian
Một cảnh 3D liên tục: thung lũng + Lake Mead cùng khung (hai tile 3DEP n37w116 và n37w115). Bộ đếm năm, chỉ số lớn **kép**: dân số Clark County (trái) và mực Lake Mead tính bằng ft (phải; trống trước 1935). Mỗi chương máy "lặn" vào một cơ chế rồi **quay về đúng năm đang chạy**.

| # | Tên chương (EN) | Năm của xương sống | Nhân vật | Nhịp lặn cơ chế | Claim chính | Thời lượng |
|---|---|---|---|---|---|---|
| 0 | *The Lowest Line Since 1937* (móc ≤ 45 s) | 2026 → tua về 1905 | — | — | C40 (1 037,54 ft) → nghịch lý (C32, C47) → 2 sự thật bất ngờ (90 % nước từ Lake Mead C29; Nevada < 2 % sông) → một con số (11×) → câu hỏi trùng tiêu đề → hứa cú lật ("the problem was written down in 1922") | 0:45 |
| 1 | *A Spring, a Railroad, a Land Sale* | 1902 → 1930 | Helen J. Stewart; W. A. Clark (phụ) | **Đường sắt 1905**: đầu máy hơi nước cần nước → ga chia tuyến đặt ở suối → đấu giá 15/05/1905 | C01–C07 (945 người năm 1910) | 1:20 |
| 2 | *Splitting a River on Paper* | dừng ở 1922 → 1928 | Herbert Hoover | **Compact 1922**: 7,5 + 7,5; 300 000 "more than enough" (C12); BCPA 1928 → Toà Tối cao 1964 | C08–C12 | 1:20 |
| 3 | *The Dam and the Six-Week City* | 1931 → 1936 | high-scalers | **Đập Hoover**: thầu $48,9 triệu; 21 000 người; hồ tích nước từ 01/02/1935 → bộ đếm ft **bắt đầu chạy**; AB 98 hợp pháp hoá cờ bạc (C13, C14) | C13–C21 | 1:40 |
| 4 | *The Valley Fills In* | 1941 → 1971 | — (nhóm du khách/công nhân A-lite) | **Ống nước 1971**: nước ngầm cạn dần (C27) → Lake Mead chảy vào thung lũng 16/06/1971 (C26) | C22–C24, C26–C27 (16 414 → 127 016 dân) | 1:20 |
| 5 | *Using the Same Water Twice* | 1991 → 2022 | Pat Mulroy | **Tái chế + gỡ cỏ**: return-flow credit (C31); 250 triệu ft² cỏ (C36); −58 % (C32); hồ tụt 2002–2022 → intake thứ ba 2015, trạm bơm 2020 (C34, C35) | C28–C36, C53 | 1:45 |
| 6 | *The Valley With Eleven Times the Water* | 2025 (giữ) | — | **Kế toán nước**: IID 11× Nevada (C47); Imperial nghèo hơn (C48); Mexico 1,5 maf + Minute 334 (N6, C45); châu thổ 2014 (C51); CRIT một câu (C49) | C47–C49, C51 | 1:30 |
| 7 | *The Honest Part — and What to Watch* | 2026 → 01/01/2027 | John Entsminger | **ROD 2026**: không đồng thuận (N1); NV 250 000 từ 2027 (C39); AB 356 01/01/2027 (C37); tuyết thấp kỷ lục, Powell 36 % (C42, C43); Rachel +0,06 ft (C46); vụ kiện "as of" (C44); bảng điểm | C37–C46, C52, C54, C56 | 1:35 |

- **Tổng ≈ 11:15.** 8 chương (0–7). Lời mời đăng ký nhẹ ở cuối ch.2 (~3:25).
- **Kết:** quay về vạch nước năm 2026, bảng điểm, câu chốt nghịch lý. Câu dẫn sang tập kế: chuỗi "who gets the river": Imperial Valley hoặc Phoenix. Lưu ý Geography Effect đã làm Phoenix, nên Imperial an toàn hơn.

### 4.5 Nêu trước các nguyên nhân khán giả hay cãi (`tienky/binh-luan.json`)
| Khán giả sẽ nói | Trọng số (tự tính) | Trả lời trong lời bằng |
|---|---|---|
| "It's California's farms, not Vegas" | RLL 5 824 | đồng ý một phần, bằng số: IID 2,19 triệu af so với Nevada 0,198 triệu (C47). Thêm: IID dùng theo quyền hợp pháp; gốc là 1922 chia quá tay (C08, C12) |
| "Why do they keep building?" / "overpopulation" | Fault Line 1 007 | dân số tăng nhưng tổng tiêu thụ dưới hạn mức (C30, C32). "The honest part": hạn mức chính nó đang bị cắt (C39) |
| "Vegas uses groundwater" | GE (sửa sai) | sai từ 1971: 90 % từ Lake Mead (C29); nước ngầm là nguồn trước 1970s (C27) |
| "Indoor water goes back to the lake" | GE, RLL | đúng: return-flow credit (C31), cảnh lặn ch.5 |
| "Build desalination / a pipeline" | Fault Line 256 | không có trong claims → không hứa; nếu nói thì cần nguồn (việc G1) hoặc bỏ |
| "Golf courses, fountains, pools" | RLL 1 083 | AB 356: cỏ không chức năng (C37); chương trình gỡ cỏ (C36). Không nêu tên casino |
| Giọng AI | GE 28 (khen người thật đọc) | giữ chuẩn giọng; không ép phụ đề cháy |

## 5. Bước 4 — Danh mục claims (`tienky/claims.json`: **56 claim**, 52 XÁC MINH, 2 MÂU THUẪN, 2 CHỜ XÁC MINH GỐC; 20 claim nhạy cảm)
| Nhóm | Claim | Nguồn chính |
|---|---|---|
| 1905–1930 đường sắt, thị trấn | C01–C07 | City of Las Vegas Timeline CO-14073; Nevada State Parks (Mormon Fort); Census 1910 (ảnh quét) |
| Compact, luật | C08–C12 | crcompct.pdf; 43 U.S.C. 617c (GovInfo); U.S. Reports 373 U.S. 546, 376 U.S. 340, 547 U.S. 150; SNWA |
| Cờ bạc, đập Hoover | C13–C21 | Nevada Legislature LCB; USBR Hoover Dam (FAQ, fatal.html, history); Census |
| Bùng nổ, ống nước | C22–C29 | City timeline; Census 1940/1960; USBR Robert B. Griffith Project; SNWA |
| Tái chế, hồ tụt, intake | C30–C36 | USBR Water Accounting Report 2025; SNWA; HDB |
| 2026 | C37–C46, C54, C56 | AB 356; ROD + OG 2027–2028; HDB; 24-Month Study 07/2026; complaint 2:26-cv-02665; IBWC; NHC; Văn phòng Thống đốc |
| Tương phản | C47–C51 | USBR 2025; Census SAIPE 2024; Consolidated Decree; SCOTUS 2023; IBWC Minute 319 |
| Người còn sống | C52, C53, C55 | lời khai Thượng viện 2022, 2013 |

**Claim nhạy cảm và cách nói:**
- **CHÍNH TRỊ-BANG** (C38, C39, C44, C54): luôn đặt hai câu cạnh nhau. Interior nói "consensus … has not been reached"; Nevada nói ROD đe doạ cắt tới 213 556 af, đó là **kịch bản tối đa theo lời bang**. Còn mức cắt thực tế năm 2027 là 50 000 af. Không đoán kết quả vụ kiện.
- **THỜI SỰ** (C40–C43, C45, C46, C56): bắt buộc "as of 14 October 2026" trong lời, trên hình và trong mô tả. Mực hồ đổi hằng ngày, nên cập nhật ở G1 và trước khi đăng.
- **BỘ LẠC** (C49, C50): chỉ dùng C49 làm một câu có số decree. Bỏ C50.
- **CỜ BẠC** (C13, C14, C22, C25): luật và năm. Không nêu tên casino làm chủ thể, không logo. Bỏ C25 (Flamingo 26/12/1946) cho tới khi có nguồn gốc.
- **NGƯỜI CÒN SỐNG** (C52, C53, C55): chỉ trích nguyên văn có nguồn.

**Không dùng** (18 mục, lý do trong `claims.json` → `khong_dung`). Các mục chính:
- "112 workers died" → nói 96;
- "buried in the concrete";
- "lowest ever" → nói "lowest since it first filled";
- "160 ft since 2000" → số đúng ≈ 177 ft (HDB);
- "Hoover chaired";
- "BCPA gave Nevada 300 000";
- "dedicated 1936" → khánh thành 1935, xong hết 1936;
- "California's first water cut";
- "Nevada loses 70 %" như sự thật;
- "75 gallons/person";
- "Imperial 3,1 triệu af" (chưa trích được nguồn gốc);
- "largest reservoir in the world";
- lũ Rachel ở Las Vegas (chưa có nguồn NWS).

## 6. Bước 5 — Tài sản hình có giấy phép (`tienky/tai-san.json`: 32 mục; `licenses/`: 43 tệp)
| Tầng hình | Tài sản dùng được | Giấy phép · ghi công | Content ID |
|---|---|---|---|
| Bản đồ nổi | **USGS 3DEP 1″** n37w116 (thung lũng) + n37w115 (Lake Mead, đập, Black Canyon) — đã tải, có SHA | USGS public domain; ghi "USGS 3DEP" | THẤP |
| Vệ tinh theo năm | **Landsat**: đủ **55/55 năm 1972–2026** có cảnh mây < 10 %. MSS 1973 (LM01 042/035, mây 0 %) và Landsat 9 ngày 02/10/2026 đã tải | USGS public domain | THẤP |
| Ảnh hàng không | **NAIP 2022** 0,6 m (Strip + downtown, 2 335 × 3 600 px; `identify` xác nhận NAIP USDA 2022) | USDA FSA, PD | THẤP |
| Bản đồ lịch sử | **USGS topo 1907** (GeoTIFF), **1952** (GeoPDF); **Sanborn 1923** (LoC, rights sạch) | PD | THẤP |
| Ảnh lưu trữ | **NARA DOCUMERICA 1972**: 548975 (đập + hồ), 548989 (hồ), 549008 (phố; có logo → "điều kiện"). **NARA RG115 1932–33**: 293901, 293766, 293834 (chỉ có GIF ≤ 600 px). **LoC** (rights đọc qua JSON, chưa tải bản gốc): nhà ga ~1910, toàn cảnh ~1910, Rothstein 1940 (Main St), Glaha 1934 (ca đêm), HAER NV-27, Elwood Mead, Highsmith Lake Mead 2022 | NARA "Unrestricted"; LoC "No known restrictions" | THẤP |
| Footage | **NARA 37058 "The story of Hoover Dam"** (USBR, CC0); **archive.org BoulderD1931** (Prelinger, PD; "điều kiện" vì đồng sản xuất với Six Companies) | PD / CC0 | **TRUNG BÌNH** (newsreel PD hay bị khai) |
| **KHÔNG dùng** | Getty/AP/Reuters; YouTube Audio Library; mọi archive.org NC/ND; PBS/CSPAN; Heldorado 1946; LoC 89708444 ("Do not publish"), LOOK 1953; NARA 548970, 7720017–41; **UNLV Special Collections** (403; thường không cấp phép xuất bản); Nevada DWR parcels; Google Earth/Maps/Apple 3D | — | — |

- **Ảnh "NOW":** chỉ dùng render 3DEP + NAIP + Landsat của mình. Không dùng Google.
- **Commons:** 429 liên tục. Ảnh "bathtub ring 2026" CC BY-SA 4.0 đang CHỜ XÁC MINH, chưa có tệp giấy phép.

## 7. Bước 6 — Mức rủi ro (QUAN-TRI-RUI-RO)
**Đề xuất: XANH**, kèm 4 điều kiện viết vào lời. Thứ tự: T2 VÀNG → T3 VÀNG → T4 bắt buộc XANH. Đề tài này đạt XANH.

**Lý do XANH:**
- Câu hỏi trung tâm là **cơ chế chia nước**, không quy lỗi cho người hay công ty nào.
- Nguồn đều là chính quyền; không đảng phái.
- Cờ thời sự có mốc "as of".
- Không yếu tố ĐỎ.

**Bốn điều kiện giữ XANH:**
1. **Vụ kiện Nevada v. Interior** (đang mở) không làm trục. Nhắc một lần, có "as of", kèm lập trường hai phía (C38 + C44/C54). Nếu tới G1 vụ kiện thành tin lớn và kéo tập lệch sang tranh cãi chính trị giữa các bang, nâng VÀNG.
2. **Imperial Valley**: không dùng chữ "waste", "greedy farmers", "hay for export". Chỉ nói quyền nước, mức tiêu thụ, thu nhập, tất cả có nguồn.
3. **Bộ lạc**: một câu có số decree (C49). Không dùng C50.
4. **Cờ bạc**: luật và năm; không tên hay logo casino làm chủ thể.

**Câu chữ cần tránh (lời, tiêu đề, thumbnail, mô tả):**
| Tránh | Dùng thay |
|---|---|
| "Las Vegas shouldn't exist" / "How Las Vegas exists" | (trùng Geography Effect / RealLifeLore) — "Why Las Vegas keeps growing as Lake Mead keeps falling" |
| "Lake Mead is at its lowest ever" / "dead pool" như sắp xảy ra | "the lowest since the lake first filled, as of 14 October 2026"; dead pool 895 ft chỉ như mốc đo |
| "Las Vegas is running out of water" | "Nevada's share drops to 250,000 acre-feet in 2027" (C39) |
| "California is the real problem" | "one district uses eleven times what Nevada does — under rights written decades ago" |
| "112 men died" / "buried in the dam" | "officially, 96" (C18) |
| "Hoover chaired the deal" | "Hoover represented the federal government" (C09) |
| tên/biển casino làm điểm nhấn | khối 3D không logo |
| cờ bang/quốc gia trên thumbnail | không cờ |

## 8. Bước 7 — Gói sơ bộ
**Tiêu đề** (Why + nơi + tương phản, ≤ 60 ký tự):

| # | Tiêu đề | Ký tự | Ghi chú |
|---|---|---|---|
| 1 | **Why Las Vegas Keeps Growing as Lake Mead Keeps Falling** | 54 | đề xuất chính; nơi + tương phản thời gian; trả lời được (C23, C32, C40). Khác hẳn "exists" |
| 2 | Why Las Vegas Grew While Its Water Use Fell | 43 | nghịch lý cơ chế (C32); cho Test & Compare |
| 3 | Why One Farm Valley Uses 11x the River Nevada Does | 50 | tương phản NƠI (C47); dễ bị đọc là "đổ lỗi" → chỉ dùng nếu lời giữ giọng trung tính |

**Thumbnail** (mẫu Teardown §9; yêu cầu: năm → 2026 + một con số móc, không cờ):
```
THUMBNAIL BRIEF — K2C-T4-01
[A] BẢN ĐỒ TƯƠNG PHẢN
- Nền: relief 3DEP thung lũng Las Vegas + Lake Mead cùng khung (render của mình), tầm vùng, hồ nhận ra ở 168×94.
- Chủ thể: vùng đô thị 2026 tô vàng neon ấm (từ HISDAC/NLCD), Lake Mead xanh nước với vạch "bathtub ring" trắng dày.
- Tương phản: một mũi tên trắng từ hồ tới thành phố (dòng nước 1971 → nay).
- Chữ (1 hộp, nền tối): A1 "1905 → 2026" (dải năm nhỏ) + "−58%" đặt cạnh thành phố (C32)
                     | A2 "1905 → 2026" + "1,037 FT" đặt cạnh vạch nước (C40, as of 14/10/2026).
- Biểu tượng (≤ 2): sticker đầu máy hơi nước 1905 ở điểm ga cũ; sticker vòi nước/ống ở cửa lấy nước.
[B] CƠ CHẾ LỘ RA (không chữ)
- Chia đôi: trái sepia — đập Hoover + hồ đầy (khớp góc ảnh NARA 548975, 1972); phải tự nhiên 2026 — cùng góc, render 3DEP+NAIP,
  mặt hồ đặt ở 1 037,54 ft → vạch trắng cao trên vách đá lộ ra. Một đường cong thành phố sáng ở chân trời phía tây.
- Không mặt người, không logo casino, không cờ.
Chung: tiêu đề hỏi, thumbnail cho thấy; mọi số có trong video; lề 5 %; tránh góc dưới-phải.
Ghi: nền = 3DEP n37w116+n37w115, NAIP 2022, Landsat 2026-10-02; mã màu A vàng neon / B xanh lục-nâu / nối xanh nước.
Test & Compare: A1, A2, B.
```

**Short đi kèm (1/tập):** *"Las Vegas added 876,000 people and used less water. So why is Lake Mead at a record low?"*
- 40–50 s, dựng trên xương sống: bộ đếm 2002 → 2026, dân số đi lên, nước/người −58 %, vạch hồ đi xuống.
- Cú lật cuối: "one farm district uses eleven times what Nevada does" (C47), rồi dẫn về video dài.
- Theo BAI-HOC-LL #6–#7: mỗi thẻ ≤ 12 từ, mỗi ≤ 2,5 s có một nhịp mới; không nhãn góc trên ở 9:16.

## 9. Ngôn ngữ hình xương sống thời gian (bổ sung chủ dự án 15/10 22:47, điều chỉnh 22:54) — `tienky/hinh-xuong-song.json`, `tuyen-bay.json`
### 9.1 Bảy mốc đinh 1905 → 2026
| Mốc | Năm | Sự kiện | Công trình/địa điểm (lat, lon) | Claim | Tư liệu trong kho lựa chọn (loại · giá trị) |
|---|---|---|---|---|---|
| M1 | 1905 | Đấu giá đất 15/05/1905 của SP, LA & SL Railroad; ga chia tuyến đặt ở suối | nhà ga / đầu Fremont St (36,1717, −115,1466) | C01–C07 | LoC 2007662544 nhà ga ~1910 (a · cao); LoC 91729072 Fremont nhìn từ ga (a · cao · **điều kiện**); LoC 2007662533 toàn cảnh ~1910 (a · cao); USGS topo 1907 (a · cao) |
| M2 | 1931 | AB 98 hợp pháp hoá cờ bạc (19/03); khởi công đập (20/04) | Boulder City / Black Canyon (35,9786, −114,8325) | C13–C17 | LoC 97517305 đào móng (c · cao); NARA 293834 Boulder City từ trên không 1932 (a · cao); phim BoulderD1931 (a · cao · **điều kiện**) |
| M3 | 1935–36 | Hồ tích nước từ 01/02/1935; FDR khánh thành 30/09/1935; xong 01/03/1936 | đập Hoover (36,016, −114,7377) | C18–C21 | LoC 96516913 mặt thượng lưu ca đêm, Glaha 1934 (d · cao); NARA 293901 đổ bê tông (c · cao); NARA 293766 high-scalers (b · cao) |
| M4 | 1941–1960 | El Rancho Vegas, Last Frontier (1941–42); Clark County 16 414 → 127 016 | Strip (36,144, −115,157) | C22–C24 | LoC 2017779911 Main St, Rothstein 1940 (b · cao) |
| M5 | 1971 | Nước Lake Mead vào thung lũng 16/06/1971 (SNWP giai đoạn 1) | Saddle Island / cửa lấy nước (36,068, −114,7994) | C26–C29 | NARA 548989 Lake Mead 5/1972 (a · trung bình); NARA 549008 phố 1972 (b · trung bình · **điều kiện**, logo) |
| M6 | 2002–2022 | Hạn hán; kỷ lục thấp 28/07/2022; intake thứ ba 2015, trạm bơm 2020 | intake 3 (36,06, −114,80) | C30–C36 | LoC 2023697161 Highsmith 2022, vạch bathtub (a · cao); Commons bathtub 2026 (a · trung bình · CHỜ) |
| M7 | 2026 | ROD 21/08; kỷ lục thấp mới 1 037,54 ft; AB 356 từ 01/01/2027 | toàn thung lũng + hồ (36,15, −115,15) | C37–C46 | Landsat 9 ngày 02/10/2026 (a · cao); NAIP 2022 (c · cao) — **không ảnh lưu trữ; 3D + vệ tinh** |

- Mỗi mốc có ≥ 1 claim XÁC MINH (`claims.json` → `moc_index`).
- Điểm đấu giá 1905 không có toạ độ chính thức; dùng toạ độ nhà ga. Ảnh **không bắt buộc** cho mọi mốc (điều chỉnh 22:54).

### 9.2 Cặp THEN/NOW (chỉ giữ khi góc khớp tốt)
| Cặp | THEN | NOW | Hướng | Kết luận |
|---|---|---|---|---|
| TN1 | NARA 548975 (5/1972, nhìn từ máy bay: đập + Lake Mead) | render 3DEP n37w115 + NAIP; mặt hồ đặt theo cao trình USBR từng năm; kiểm bằng Landsat 2026 | **ước**: từ phía bắc/tây bắc đập, nhìn nam–đông nam, cao 600–900 m trên mặt hồ. Phải giải camera trên DEM | **GIỮ.** Địa hình hẻm cố định nên khớp góc được. Vạch nước 1972 so với 2026 chính là "bathtub ring". Đây là cảnh đặc trưng của tập |
| TN2 | LoC 91729072 (Fremont St nhìn từ nhà ga, thập niên 1910) | render 3D dọc tuyến OSM Fremont + NAIP | **ước** ~118° (ĐĐN), tầm mắt người | **ĐIỀU KIỆN:** chỉ giữ nếu bản lớn (khi `tile.loc.gov` hoạt động) đúng hướng và rights được chủ dự án đối chiếu. Không khớp thì bỏ, không tìm thêm |

### 9.3 Tuyến bay (hình học OSM, ODbL — ghi "© OpenStreetMap contributors"; GeoJSON nhúng trong `tuyen-bay.json`)
| Tuyến | Đường | Độ dài · số điểm | Dùng ở | Ghi chú |
|---|---|---|---|---|
| TB-fremont | Fremont St: nhà ga cũ / Main St → đông tới Eastern Ave | 2,83 km · 64 điểm | ch.1 (1905–1930) | Fremont lịch sử chỉ ~0,6 km đầu (Main → 5th St); đoạn này phủ Sanborn 1923 |
| TB-strip | Las Vegas Blvd S: Sahara → Mandalay Bay | 6,54 km · 127 điểm | ch.4 (1941 → 1971) | bay thấp, khối giản lược không logo; **không** dựng chuỗi mọc/phá từng casino (khác Cornerstone) |
| TB-water | Intake #3 (Lake Mead) → Saddle Island → hầm River Mountains → thung lũng | 16,82 km · 32 điểm | ch.4 (1971), ch.5 (2015/2020) | có **đoạn nối giả định 4,55 km** (hầm không có trong OSM) → trên hình vẽ nét đứt và ghi "approximate route" |

### 9.4 Mở đầu từng chương
| Ch. | Kiểu mở | Đề xuất |
|---|---|---|
| 0 | **reveal toàn cảnh** | mở thẳng ở vạch nước 2026 sát vách đá, máy kéo lui thành toàn cảnh hồ + thành phố ở chân trời; bộ đếm tua về 1905 |
| 1 | **glide → zoom-in** | trượt theo đường ray từ phía nam vào thung lũng trống (topo 1907 sepia), hạ xuống nhà ga, rẽ theo TB-fremont |
| 2 | **reveal toàn cảnh** | kéo lên thật cao thành bản đồ cả lưu vực; sông tách thành hai nửa Upper/Lower như hai cột nước |
| 3 | **glide → zoom-in** | trượt dọc Black Canyon về hạ lưu, rồi lặn vào mặt cắt đập; hồ bắt đầu dâng và bộ đếm ft bật |
| 4 | **glide → zoom-in** | bay thấp theo TB-strip, vùng đô thị loang ra theo năm HISDAC; cuối chương rẽ sang TB-water |
| 5 | **reveal toàn cảnh** | từ trên cao, hồ thu lại từng năm 2002 → 2022, vạch trắng dày lên; rồi lặn vào intake thứ ba |
| 6 | **reveal toàn cảnh** | kéo ra khỏi Lake Mead xuống tới Imperial Valley và châu thổ ở Mexico: hai cột "11×" dựng trên bản đồ |
| 7 | **glide → zoom-in** | quay về đúng khung mở đầu (TN1 NOW), trượt tới vạch 1 037,54 ft; bảng điểm hiện lên |

- Xen kẽ reveal và glide để không lặp khung (BAI-HOC-LL bài học gốc lô 6–8).

### 9.5 Tư liệu lịch sử: lý do dùng và tỷ lệ footage đề xuất (điều chỉnh 22:54)
- Mỗi tư liệu trong `tai-san.json` / `hinh-xuong-song.json` có `loai_ly_do` (a bằng chứng sự việc · b con người/đời sống · c quy mô/chất liệu · d khoảnh khắc biểu tượng) và `gia_tri`.
- Tư liệu không thuộc a–d thì đã loại, hoặc ghi "không dùng, 3D làm tốt hơn":
  - chân dung Hoover và Mead: giá trị thấp → chỉ dùng nếu lời cần nhận diện;
  - toà/khung cảnh hiện đại: dùng 3D + NAIP.
- **Đề xuất tổng tỷ lệ tư liệu thật toàn khung: ≈ 6 % (~40 s / 11:15), trần 20 % là tối đa, không phải chỉ tiêu.**

| Phần | Thời lượng | Nội dung |
|---|---|---|
| Ảnh lưu trữ (Ken Burns 2.5D) | ~28 s | ~6 ảnh × 4–5 s: nhà ga ~1910 (M1, a), Boulder City 1932 (M2, a), high-scalers 1932 (M3, b), ca đêm 1934 (M3, d), Main St 1940 (M4, b), Lake Mead 1972 (TN1, a) |
| Footage phim 1931–36 | ~12 s | 2–3 đoạn ≤ 6 s từ NARA 37058 (CC0) — quy mô công trường (c), người làm đập (b) |
| Stock hiện đại | **0 s** | giai đoạn 1971–2026 dựng bằng 3D + Landsat/NAIP |
| Hồ sơ văn bản (không tính là footage) | ~60–75 s | Compact Điều III, Decree II(B)(1), ROD câu "consensus…", OG 2027 dòng Nevada, AB 356 Sec. 39, bảng IID trong báo cáo USBR → đủ 10–15 % "hồ sơ thật" của Kinh thánh |

- **Lý do mức 6 %:**
  - (1) Tư liệu chỉ có giá trị cao ở 1905–1936. Đó là nơi 3D không thay được người thật và quy mô thật.
  - (2) Từ 1971 trở đi, chính 3D + vệ tinh là bằng chứng (hồ tụt, đô thị loang). Footage hiện đại chỉ là lấp chỗ trống.
  - (3) Newsreel PD có rủi ro Content ID TRUNG BÌNH; dùng ít thì ít điểm bị khai.
  - (4) Bản quét NARA RG115 chỉ có GIF ≤ 600 px. Dùng nhiều sẽ làm điểm tay nghề tụt (bài học V4: 368×480 → P6 6,0).

## 10. Bước 8 — Dữ liệu xương sống thời gian (`tienky/xuong-song.json`, `dan-so.json`, `lake-mead.json`)
| Chuỗi | Nguồn · giấy phép | Độ phủ | Kết luận |
|---|---|---|---|
| **Dân số** | Census thập niên 1910–2020 (ảnh quét + PL 94-171) + Vintage 2025 | Clark County 3 321 (1910) → 16 414 (1940) → 127 016 (1960) → 2 265 461 (2020) → **2 407 226** (2025). City: 2 304 (1920) → 641 903 (2020) → 679 817 (2025). 1910 thành phố chưa hợp nhất: precinct 945 | **ĐỦ** cho bộ đếm. Nội suy giữa các mốc thập niên phải ghi "interpolated" trên hình |
| **Mực Lake Mead** | USBR HDB, hằng ngày 02/02/1935 → 14/10/2026 (33 493 dòng) | đỉnh 1 225,83 (1983); 2022: 1 040,58; 2026: 1 037,54 | **ĐỦ**, theo ngày. Bộ đếm ft chạy từ 1935 |
| **Vùng đô thị theo năm** | HISDAC-US FBUY v2 (CC0, 250 m, 1901–2020): 152 ô (1940) → 2 749 (1970) → 15 819 (2020). Annual NLCD (PD, 30 m, 1985–2025). GHSL (ghi công EU, 86 → 293 km², 1975 → 2025) | 1905 → 2025 | **DỰNG ĐƯỢC.** Nối HISDAC → NLCD ở năm 1985 phải chuyển mềm |
| **Landsat theo năm** | USGS PD | 55/55 năm 1972–2026 có cảnh mây < 10 % | lớp kiểm chứng và then/now |
| **Năm xây từng toà** | CLV parcels CONSTYR: 90 % của 302 313 dòng có năm, sớm nhất 1901, **chỉ City of Las Vegas**, giấy phép chỉ là disclaimer (VÀNG). Clark County Assessor: phải mua ($2 500), điều khoản "not resold…", chưa chắc có year built. OSM: 66 toà có start_date. MTBF-33: **không có** Clark County | — | **KHÔNG đủ cho cả thung lũng** |
| **Footprint hiện nay** | Microsoft (CDLA-Permissive 2.0) 663 154; Overture (ODbL) 665 106; OSM 321 611; 830 474 thửa | — | dùng cho cảnh NOW và đùn khối |

**Trả lời câu hỏi bước 8:** **không dựng được "mỗi toà nhà mọc đúng năm"** cho thung lũng. Lý do:
1. Năm xây chỉ có miễn phí cho City of Las Vegas. Strip (Paradise), Henderson và North Las Vegas thì không.
2. Năm của assessor là năm của **toà hiện có**. Các toà đã phá (El Rancho 1941–1960, Sands, Dunes, Stardust…) không có, nên Strip sẽ trông như mọc sau 1990. Dựng theo dữ liệu này là **sai lịch sử**.

**Đề xuất: phương án C (lai), đã điều chỉnh để tránh giống Cornerstone:**
- **Nền** (toàn thung lũng): vùng đô thị bật theo năm HISDAC (1905–1985) → Annual NLCD (1985–2025). Trong vùng đã bật, đùn khối thủ tục từ footprint Overture/MS theo mật độ hiện nay.
- **Lớp từng toà ở hai nơi:**
  - downtown/Fremont 1905–1950: số hoá Sanborn 1923, vài trăm toà;
  - **≤ 10 resort Strip làm mốc tham chiếu** (năm mở/phá phải có nguồn — việc G1). Không phải 20–40 như đề xuất gốc của phiên phụ, để không thành chuỗi casino kiểu Cornerstone.
- **Khối tự động:** ~4 878 toà ≥ 2 000 m² (≥ 10 000 m²: 640).
- **Tổng ước:** ~4,9 nghìn khối tự động + ~300 toà downtown + ≤ 10 resort dựng tay; phần còn lại là vùng tô/khối thủ tục.
- **Ưu:** giấy phép sạch (CC0/PD/ODbL/CDLA-P); phủ 1905–2026; đúng lịch sử.
- **Nhược:** thấy "vùng mọc" nhiều hơn "toà mọc".
- **Tác động:** cần ~6 GB đĩa cho 6–8 năm NLCD (chưa tải); số hoá Sanborn là việc tay.
- **Rủi ro:**
  - HISDAC thiên lệch vì chỉ có toà còn tồn tại; 1905–1930 gần như trống (2 ô) → giai đoạn này dựa vào Sanborn + topo 1907.
  - Giờ render cảnh 2 tile 3DEP lớn hơn cuộn K2V4; đo ở G1.

## 11. Chi phí (`tienky/cost.json`)
| Mục | Trần | Thực tế |
|---|---|---|
| YouTube Data API | 300 | **292**: search 200 · playlistItems 83 · videos 5 · commentThreads 3 · channels 1 (94 lượt, 0 lỗi HTTP; sổ `quota.jsonl` ngoài git) |
| Claude API | $2 (ghim `claude-haiku-5-5`) | **$0,0213** · 4 lượt (khoảng trống 1, bình luận 3) · model thực chạy = `claude-haiku-5-5` cả 4 |
| ElevenLabs | 0 | **0** |
| WebSearch | — | 5 lượt (không thuộc quota YouTube) |
| Token | trần mềm | 2 phiên phụ Claude Code: nguồn gốc 366 615 token / 210 lượt công cụ; tài sản + dữ liệu 341 664 token / 170 lượt. **Vượt mức thường của một tiền kỳ** để kiểm 81 tệp nguồn và 32 tài sản; không qua API trả tiền |
| Đĩa ngoài git | — | nguồn 346 MB + tài sản 543 MB (scratchpad; mất khi container thu hồi; SHA đã ghi) |

## 12. Kiểm nhanh các con số của phiên phụ (P tự chạy lại từ tệp gốc)
- HDB Lake Mead: min sau 1937 → lần cuối < 1 037,54 ft là 21/04/1937. Ngày 28/07/2022 = 1 040,58; ngày 06/08/2026 = 1 040,50; ngày 14/10/2026 = 1 037,54. **KHỚP.**
- Báo cáo USBR 2025: dòng "Total IID Consumptive Use … 2,187,165"; Nevada "197,570". **KHỚP.**
- ROD: câu "Unfortunately, as of the publication…" có trong `p26_rod.txt`. **KHỚP.**

## 13. Tệp đã ghi và đề xuất ngoài vùng
- **Đã ghi:**
  - `TIEN-KY.md`;
  - `tienky/`: `neo`, `claims`, `cau`, `kho-kenh`, `binh-luan`, `khoang-trong`, `dan-so`, `lake-mead`, `tai-san`, `xuong-song`, `hinh-xuong-song`, `tuyen-bay`, `nguon-tep`, `cost` (14 tệp `.json`). Thêm bằng `git add -f` vì `channel-k2/.gitignore` chặn `*.json`, giống T3;
  - `licenses/`: 43 tệp, mọi email thay bằng "[email đã che — xem URL gốc]".
- **Đề xuất cho P** (chưa ghi):
  1. `COST-LEDGER.csv` dòng `T4-01`: tiền kỳ, YouTube 292, Claude $0,0213 (haiku), ElevenLabs 0.
  2. `RIGHTS.md`: 3DEP, NAIP, Landsat, USGS topo, NARA, LoC, HISDAC, NLCD, GHSL, Overture/OSM (ODbL), MS footprints (CDLA-P) — ghi khi tài sản được dùng thật (G1).
  3. `channel-k2/.gitignore`: thêm `!k2c-t4-01/tienky/*.json`.
  4. `HANG-DOI.md`: thêm K2C-T4-01 mức XANH.
- **Ghép thử:** nhánh chỉ thêm tệp mới trong `channel-k2/k2c-t4-01/`, không đụng `main`, `k2c-t2` hay `k2c-t3-tienky`.

## 14. Preflight
- `bash scripts/env/verify.sh`: 9 PASS, 4 FAIL (three.js, tifffile/pyshp, k2v node_modules, Freesound). Không liên quan việc tiền kỳ.
- `bash tools/preflight.sh --range origin/main..HEAD`: **ĐẠT** ở mọi lần đẩy; `checks/lock.py --verify`: **KHỚP**. Lần cuối chạy ngay trước lần đẩy cuối.
- Không dùng `--no-verify`.

## 15. Việc đang chờ chủ dự án
1. **Duyệt khuyến nghị:** đi tiếp Las Vegas ở mức XANH với **góc mới** "thành phố mọc / hồ tụt", tiêu đề 1. Hoặc chọn đề tài dự phòng (đường sắt cao tốc Tây Ban Nha; cần tiền kỳ riêng).
2. **Chọn cặp tương phản:** Las Vegas ↔ Imperial Valley (đề xuất). Duyệt việc bỏ C50 (Navajo) và chỉ dùng một câu về CRIT.
3. **Duyệt cách nói** "the lowest since the lake first filled, as of 14 October 2026" (không nói "lowest ever").
4. **Vụ kiện Nevada v. Interior:** đồng ý nhắc một lần với lập trường hai phía, hay bỏ hẳn.
5. **Cửa sổ phát hành:** đề xuất **trước 01/01/2027** (mức cắt và AB 356 có hiệu lực). Lý do: cung Lake Mead đổi theo tuần, Latos Charts vừa sang thành phố Mỹ. Mực hồ cập nhật trước khi đăng.
6. **Tài sản "điều kiện" cần đối chiếu bằng mắt:**
   - LoC 91729072 (Fremont từ nhà ga; quyết định cặp TN2);
   - LoC 2005677820, 2005688458 (Clark), 92501271 (Hoover);
   - phim BoulderD1931;
   - NARA 549008 (logo);
   - ảnh Commons bathtub 2026.
   Thêm: xin bản quét lớn NARA RG115 (CAN-TAI-HO hoặc đặt NARA). Thử tải lại ảnh LoC khi `tile.loc.gov` hết lỗi 520.
7. **Dữ liệu xương sống:**
   - duyệt phương án C (≤ 10 resort dựng tay);
   - duyệt dùng CLV CONSTYR dù giấy phép chỉ là disclaimer;
   - **không** mua dữ liệu Clark County (C không cần);
   - cấp ~6 GB đĩa cho Annual NLCD ở G1.
8. **UNLV Special Collections:** có muốn xin phép bằng văn bản không. Trang trả 403 cho máy; theo thông tin đọc được, UNLV thường không cấp phép xuất bản.
9. **Nguồn còn thiếu trước G1:**
   - năm mở/phá ≤ 10 resort mốc (nguồn gốc);
   - Flamingo 1946 (C25);
   - số bốc hơi Lake Mead của SNWA (C55);
   - thất nghiệp Imperial County (CA EDD lỗi TLS, BLS 403);
   - đơn kiện bản PACER;
   - văn bản Minute 334 có lớp chữ;
   - nếu giữ ý "khử mặn/đường ống" thì cần nguồn.
10. **P chép các đề xuất §13** vào COST-LEDGER, RIGHTS, `.gitignore`, HANG-DOI.
