# KẾ HOẠCH TẬP THỬ (Mốc 2) — Last Lamplighters · "The Last Lamplighters"

Gói: KẾ HOẠCH TẬP THỬ (P giao theo chỉ thị chủ dự án 01/10/2026) · Người lập: phiên lập kế hoạch sản xuất · Trạng thái: **nháp, chờ P và chủ dự án duyệt**. Chỉ lập kế hoạch: không render, không sửa mã, không gọi API tính phí, không đọc `checks/` (chỉ `checks/RUN.md`), không commit.

Đầu vào: `CLAUDE.md`, `PLAN.md`, `AUTHORSHIP.md` (các mục 01/10/2026), `RIGHTS.md`, `reports/m3/KICH-BAN-TAP-THU-V2.md`, `SERIES-LAST-LAMPLIGHTERS.md`, `THU-PHONG-CACH.md` (§1.2, §4, §6, §7, §9), `shots/animatic/SHOTLIST.md` (sinh từ `make_shotlist.py`), `order_w1.js`, `order_w2.js`, `design/cong5/layout/audio/mix.py`, `scripts/p/layout_full.sh`, `scripts/render/queue.sh`, `scripts/p/kiem_mu.py`, `checks/RUN.md`.

---

## 0. Tóm tắt

- **78 shot, tổng 571 s = 9:31**, khớp kịch bản V2.
  - 28 shot dùng lại shot Last Round (148 s, 26 %).
  - 10 shot dùng lại tài sản nhưng dàn dựng mới (68 s, 12 %).
  - 40 shot mới (355 s, 62 %), gồm 32 shot đồ hoạ 2D (299 s) và 8 shot minh hoạ 3D mới (56 s).
  - **Tỉ lệ dùng lại: 38 % thời lượng (216 s), 49 % số shot.** Kịch bản V2 §7 ước 3:58; số của bảng này thấp hơn (3:36) vì trong đoạn 03 và 05 có phần đồ hoạ mới.
- **Token (ước):**
  - xưởng khoảng 1,2 triệu, tức 0,13 triệu mỗi phút phim;
  - cả tập, gồm kiểm mù, kiểm số và P: **khoảng 1,9–2,2 triệu, tức 0,20–0,23 triệu mỗi phút**. Đạt tiêu chí 2 (≤ 0,3) và không nằm trong vùng ±5 % quanh ngưỡng.
- **Giờ render (ước, chưa đo chuỗi 1080p):** khoảng 14–34 giờ máy trên một làn nặng, trung tâm khoảng 20 giờ.
- **Giọng:** phương án A là ElevenLabs, dùng **giọng thư viện cho người kể** (đề xuất) và mô hình đọc ổn định cho bài dài. Ước **12 400 ký tự** ở kịch bản cơ bản, tối đa khoảng 27 900, so với 29 400 ký tự còn lại. **Chưa cần nâng gói.** Phương án tạm: bộ lọc `flite` của ffmpeg (đã có sẵn) để làm bản nháp nhịp.
- **Chỉ số nằm trong ±5 % quanh ngưỡng (nêu theo luật cứng):**
  - thời lượng 9:31 cách trần 10:00 là 4,8 %;
  - ký tự ElevenLabs ở kịch bản rất xấu: 27 900 / 29 400, cách trần 5,1 % (sát vùng);
  - đoạn 08 và 13: lời dẫn ở 150 từ/phút dài đúng bằng thời lượng đoạn, không còn dư.

**Số đo lời dẫn (máy đếm, chỉ các dòng `>` của V2):** 1 309 từ, khoảng 7 380 ký tự. P ghi 1 373 từ và 7 750 ký tự, có thể do cách đếm khác. Kế hoạch dùng **7 750** để có biên. Ở 150 từ/phút, 1 309 từ là 8:44. Nếu người kể đọc 140 từ/phút, lời dẫn thành 9:21 và cả tập khoảng 10:08, vượt trần. Khi đó **cắt đoạn 07** (27 s), như V2 đã định.

---

## 1. Danh sách shot (V2, 9:31)

**Quy ước**
- **Loại:** **R** là dùng lại shot Last Round (giữ set, rig và diễn hoạt; đổi máy sang cỡ B3, kéo dài hoặc cắt lại nhịp, hậu kỳ B3). **A** là dùng lại tài sản (set, rig, đạo cụ) với dàn dựng mới. **N** là mới.
- **Cỡ cảnh:** EWS, WS, MWS, MS là cỡ cảnh. "Insert" là cận **vật hoặc bàn tay**, không bao giờ cận mặt. Người luôn là bóng hoặc ở cỡ trung–xa.
- **Nhãn đoạn:** STORY / DATA / SHORTS lấy theo nhãn đoạn của V2. Thoại Ida chỉ có L1 và L2, dùng lại take C4-D1.
- **Mẫu đồ hoạ:** D-MAP, D-BAR, D-TL, D-NUM, D-SRC, D-GRID (xem mục 2).

### 01 · STORY · Cold open (45 s)
| Mã | Loại | Cỡ | s | Dùng lại | Mới | Ghi chú hình |
|---|---|---|---|---|---|---|
| 01-01 | R | EWS | 7 | s01 (thành phố, đốm hổ phách) | kéo dài giữ khung | VO vào ở giây 2 |
| 01-02 | R | WS | 6 | s02 (Ida vác thang phải → trái) | — | bóng dài trên đá lát |
| 01-03 | R | WS 3/4 thấp | 5 | s03 bản B3_CAM | — | L4 bắt lửa có thời gian bắt lửa 0,3–0,5 s (B3 v2) |
| 01-04 | R | MS nghiêng (bóng) | 5 | s05 bản B3 (profile) | — | hơ tay ba nhịp; **L1 "Evening, old street."** (C4-D1) |
| 01-05 | R | WS | 4 | s04 (bóng người + thang trên tường) | — | — |
| 01-06 | R | WS | 6 | s07 (đi qua L5) | — | "Ida isn't real…" |
| 01-07 | A | WS tele | 6 | s08 + bóng Cas (s24c) ở xa | dàn dựng Cas xa | Cas chỉ là bóng |
| 01-08 | A | EWS đẩy chậm | 6 | set s01/s43 | giờ chạng vạng, chừa chỗ chữ | nối sang thẻ tựa |

### 02 · DATA · Pall Mall 1807 (56 s)
| Mã | Loại | Cỡ | s | Dùng lại | Mới | Ghi chú hình |
|---|---|---|---|---|---|---|
| 02-01 | N | đồ hoạ | 6 | lớp mái nhà `data_frame.py b3` | thẻ tựa THE LAST LAMPLIGHTERS | — |
| 02-02 | N | D-MAP | 10 | — | bản đồ London cách điệu; đường hổ phách Pall Mall | nhãn "Pall Mall · 1807" (D1) |
| 02-03 | N | WS (minh hoạ) | 6 | — | bóng đám đông cắt giấy đứng ngắm đèn (vẽ lại theo phong cách riêng, không chép Rowlandson) | Illustrative |
| 02-04 | N | D-TL | 9 | — | 1807 → 1812 royal charter → 1813 Westminster Bridge | D2, D3 |
| 02-05 | N | D-MAP | 12 | bản đồ 02-02 | mạng phố sáng như rễ; bộ đếm lên 40,000; "1820s · 215 miles" | D4 |
| 02-06 | N | D-NUM | 7 | — | **40,000+** gas lamps · London, 1820s | thẻ nguồn: English Heritage |
| 02-07 | A | MS | 6 | mô hình đèn khí + bóng Ida đi (lp20) | dàn dựng | "…needed a person" |

### 03 · STORY + DATA · The round (45 s)
| Mã | Loại | Cỡ | s | Dùng lại | Mới | Ghi chú hình |
|---|---|---|---|---|---|---|
| 03-01 | R | MS sau-phải | 6 | s03, đặt máy mới (tay, van, sào) | — | không thấy mặt |
| 03-02 | R | MS (bóng) | 5 | s24 (hơ tay ở L11), máy nghiêng | — | kiểm không lộ mặt |
| 03-03 | N | D-MAP lồng góc khung | 8 | nền phố s07 | tuyến đèn gấp khúc, không ghi số | Illustrative (D5, định tính) |
| 03-04 | A | Insert tay | 5 | mô hình đèn khí, rig tay Ida | tư thế lau kính | — |
| 03-05 | A | WS | 7 | set phố (s07) | lớp sương / mưa | — |
| 03-06 | A | WS | 6 | s40 (gạt van), set phố | màu bình minh | vòng tắt đèn lúc sáng |
| 03-07 | A | EWS | 8 | set s01 + rig Ida (bóng vô danh nhân bản) | nhân bản bóng | "a small army"; Illustrative |

### 04 · DATA · Across the ocean (28 s)
| Mã | Loại | Cỡ | s | Dùng lại | Mới | Ghi chú hình |
|---|---|---|---|---|---|---|
| 04-01 | N | D-MAP | 8 | — | bản đồ Đại Tây Dương; cung London → Baltimore | "1816 · Peale's museum" (D7) |
| 04-02 | N | WS (minh hoạ) | 6 | — | mặt tiền bảo tàng Peale cắt giấy, cửa sổ sáng | — |
| 04-03 | A | WS | 7 | mô hình đèn khí | mặt phố Market St phẳng | "Feb 7, 1817 · first U.S. public gas street lamp" (D6) |
| 04-04 | N | D-MAP | 7 | bản đồ 04-01 | cung sang Paris | "Paris · mid-1800s" (nguồn [16]; **không có dòng D# trong V2 §4**, xem rủi ro R6) |

### 05 · STORY + DATA · The white wave (63 s)
| Mã | Loại | Cỡ | s | Dùng lại | Mới | Ghi chú hình |
|---|---|---|---|---|---|---|
| 05-01 | R | MS | 5 | s09 (đồng hồ quảng trường 8:00, chuông) | — | — |
| 05-02 | R | Insert | 4 | s09w (đồng hồ bỏ túi 7:53) | — | chỉ tay và đồng hồ |
| 05-03 | R | MS (đèn) | 4 | s10e (bóng điện nháy hai lần) | — | — |
| 05-04 | R | EWS | 6 | s10 (sóng trắng xuống dốc) | — | — |
| 05-05 | R | WS | 6 | s19 (L8 nở hổ phách, cột điện xoá bóng) | — | — |
| 05-06 | R | MWS thấp | 5 | s22 bản B3_CAM | — | **L2 "Not yet… not yet."** (C4-D1) |
| 05-07 | N | D-MAP | 10 | — | Avenue de l'Opéra 1878, 64 chấm trắng | D8 |
| 05-08 | N | D-MAP / D-TL | 7 | — | Broadway 1880, một hàng chấm trắng | D9 (qua tóm tắt) |
| 05-09 | R | WS qua vai | 6 | s12 (phố trắng dần) | nhịp chậm hơn | "a slow tide" |
| 05-10 | R | Insert | 5 | s06 (đồng hồ 7:31, gõ kính) | — | "seven minutes slow" |
| 05-11 | R | WS | 5 | s15 (xuống thang, vác thang đi) | — | — |

### 06 · DATA · New York, April 1907 (41 s)
| Mã | Loại | Cỡ | s | Dùng lại | Mới | Ghi chú hình |
|---|---|---|---|---|---|---|
| 06-01 | N | D-MAP | 10 | — | Manhattan cách điệu; đèn tắt thành mảng | "New York · April 1907"; mảng tối là Illustrative (D10) |
| 06-02 | N | đồ hoạ | 8 | — | trang báo **vẽ lại**, tiêu đề diễn đạt lại "Lamplighters strike" | thẻ nguồn Chronicling America (LOC) |
| 06-03 | N | EWS | 8 | set phố, đèn khí | bóng cảnh sát đội mũ leo cột, que diêm loé | nhân vật bóng mới |
| 06-04 | N | WS | 7 | set phố | nhóm bóng người ở góc phố (bộ bóng đám đông của 02-03) | — |
| 06-05 | A | WS | 8 | set phố + bóng điện s27 | đèn thắp lại rồi một cột trắng mọc | "…a little more without them" |

### 07 · DATA · The great switch-off (27 s; đoạn cắt trước nếu quá giờ)
| Mã | Loại | Cỡ | s | Dùng lại | Mới | Ghi chú hình |
|---|---|---|---|---|---|---|
| 07-01 | N | D-TL | 14 | — | các mốc hổ phách chuyển trắng; "New York — 2 gas-era lampposts left"; "Paris — 1962" | D13, D12 (**D12 mức chắc chắn trung bình–thấp**) |
| 07-02 | N | D-BAR | 9 | — | cột 40,000 (1820s) cạnh ~1,100 (2023), cùng thang | D4, D14 |
| 07-03 | N | D-MAP | 4 | bản đồ 02-02 | lùi xa, còn lại vài đốm hổ phách | chuyển sang 08 |

### 08 · SHORTS · London's last lamplighters (49 s)
| Mã | Loại | Cỡ | s | Dùng lại | Mới | Ghi chú hình |
|---|---|---|---|---|---|---|
| 08-01 | N | EWS 2.5D | 7 | mô hình đèn khí (đổi sang kiểu Covent Garden) | **set Covent Garden** (đèn khí giữa đèn LED trắng) | không logo, không biển hiệu thật |
| 08-02 | N | D-NUM | 7 | — | "~1,500 lamps (2015) → ~1,100 (2023)" | D14 |
| 08-03 | N | WS (bóng) | 7 | rig Ida làm khung xương | **bóng người thắp đèn hiện đại** (áo phản quang, thang nhôm) | hư cấu, không vẽ theo người thật |
| 08-04 | N | D-NUM | 6 | — | **5 lamplighters** | D15 |
| 08-05 | N | Insert vật | 7 | — | cơ cấu đồng hồ trong đèn, chìa lên dây | "wound every 2 weeks" (D16) |
| 08-06 | N | WS | 8 | set 08-01 | mặt tiền nhà hát / phố Mall | nhãn "2022 · LED plan opposed", "4 lamps · listed 2024" (D17, D18) |
| 08-07 | N | D-NUM | 7 | — | "40,000 → ~1,100 → 5 people" | D4, D14, D15 |

### 10 · STORY · The last lamp (52 s)
| Mã | Loại | Cỡ | s | Dùng lại | Mới | Ghi chú hình |
|---|---|---|---|---|---|---|
| 10-01 | R | WS | 6 | s35 (ra khỏi hốc, trèo; Cas chạy giữ thang) | — | — |
| 10-02 | R | WS ngược sáng | 6 | s37w (bỏ thoại L4) | — | — |
| 10-03 | R | MS từ sau lưng | 4 | s38 (Cas giữ thang), đặt máy mới | — | s38 gốc thấy mặt Cas nên phải đổi máy |
| 10-04 | R | Insert tay | 5 | s40 (gạt van, lửa tắt) | — | — |
| 10-05 | R | WS | 6 | s40w (không gì đổi) | — | khoảng lặng không lời 10–12 s (10-04 và 10-05) |
| 10-06 | R | WS | 5 | s41 (trao đèn lồng) | — | — |
| 10-07 | R | WS → MS | 6 | s42b + s42 (Cas vào vòm, hơ tay ba nhịp) | — | — |
| 10-08 | R | EWS | 6 | s43 (thành phố trắng, một ô vàng) | — | — |
| 10-09 | R | Insert | 5 | s46 (vặn 9:53 → 10:00, gập lại) | — | không gõ kính |
| 10-10 | R | WS | 3 | s48 (chim bóng của Cas) | — | — |

### 11 · DATA · One job in 270 (34 s)
| Mã | Loại | Cỡ | s | Dùng lại | Mới | Ghi chú hình |
|---|---|---|---|---|---|---|
| 11-01 | N | đồ hoạ | 4 | — | biểu tượng đèn thu thành một ô lưới | — |
| 11-02 | N | D-GRID | 12 | — | lưới 270 biểu tượng nghề chao nhẹ | "1950 U.S. Census → 2010" (D21) |
| 11-03 | N | D-GRID | 8 | — | một ô tắt: cửa thang máy có tay gạt | "elevator operators" |
| 11-04 | N | D-NUM | 10 | — | **1 in 270** | nguồn Bessen (2016), ghi "271 occupations" |

### 12 · SHORTS · Today's shortest rounds (47 s)
| Mã | Loại | Cỡ | s | Dùng lại | Mới | Ghi chú hình |
|---|---|---|---|---|---|---|
| 12-01 | N | D-NUM | 7 | — | **−34%** (5 s đầu) · "word processors & typists" | D23 |
| 12-02 | N | D-BAR | 22 | hình cột đèn khí | 5 cột đèn mang biểu tượng nghề, ngắn lại theo %, cùng thang | D23–D27 |
| 12-03 | N | D-BAR (chú thích) | 8 | — | nhấn "telephone operators −27.6% · ~3,500 jobs (2025)" | D24 |
| 12-04 | N | D-SRC | 10 | — | "Forecasts, not verdicts" + nguồn BLS Table 1.5 | D28 (D29 tuỳ chọn) |

### 13 · DATA · AI in the forecast (51 s)
| Mã | Loại | Cỡ | s | Dùng lại | Mới | Ghi chú hình |
|---|---|---|---|---|---|---|
| 13-01 | N | D-BAR | 15 | — | nghề giảm (trắng lạnh) / software developers +17.9 (hổ phách); nhãn **2023–33** | D32–D35 |
| 13-02 | N | D-BAR | 12 | — | dải đèn hổ phách: NP +41.0, solar +36.5, data sci +34.6, wind +29.5; nhãn **2025–35** | D30; khung riêng, không chung trục với 13-01 |
| 13-03 | N | D-BAR | 16 | — | hai thanh ngang "expected" và "actual"; chữ "**~19% below expected**" · "ages 22–25 · most AI-exposed jobs · U.S. payroll data to June 2026" · "early signal · not proof of cause" | D36; **đề xuất không in số "81"** (số suy ra, không phải số của nguồn) |
| 13-04 | N | D-SRC | 8 | — | thẻ nguồn Stanford DEL (8/2026), BLS MLR (2/2025) | — |

### 14 · STORY + DATA · The question (33 s)
| Mã | Loại | Cỡ | s | Dùng lại | Mới | Ghi chú hình |
|---|---|---|---|---|---|---|
| 14-01 | A | EWS | 9 | set s43/s01 | lớp thành phố hiện đại (màn hình, cửa sổ văn phòng), một ô hổ phách | — |
| 14-02 | N | D-NUM (xếp dọc) | 8 | — | 40,000 · 5 · 1 in 270 · −34% | bốn số neo |
| 14-03 | R | WS xa | 6 | s44 (Ida dưới cửa sổ) | — | **L1 (off, distant)**: take C4-D1, xử lý xa trong mix, không thu mới |
| 14-04 | N | đồ hoạ | 10 | — | thẻ kết: Last Lamplighters · *Every era has its last lamplighters.* | câu hỏi kết đọc đè trên thẻ kết |

**Kiểm tổng**

| Đoạn | 01 | 02 | 03 | 04 | 05 | 06 | 07 | 08 | 10 | 11 | 12 | 13 | 14 | Tổng |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| s | 45 | 56 | 45 | 28 | 63 | 41 | 27 | 49 | 52 | 34 | 47 | 51 | 33 | **571 = 9:31** |
| Lời dẫn ở 150 từ/phút (s) | 38 | 52 | 40 | 25 | 58 | 41 | 25 | **49** | 40 | 32 | 46 | **51** | 26 | 523 |

**Shot Last Round phải đổi máy vì lộ mặt:** s05, s22 (đã có B3_CAM), s24, s38. Shot không dùng: s05 bản cận, s21, s31, s37, s37b, s39 và các shot của cảnh 4 tường (s25–s34), để dành cho tập sau.

---

## 2. Bộ mẫu dữ liệu B3 (một ngôn ngữ hình)

**Chung**
- Khung 1920×1080, 24 fps.
- Sinh thủ tục theo nền `data_frame.py b3`: giấy ngà, mép xé, bóng đổ giấy.
- Lề an toàn chữ: 96 px ngang, 54 px dọc.
- Biểu đồ dựng theo skill `dataviz`: cùng thang trong mỗi biểu đồ, trục số bắt đầu từ 0, ghi nhãn trực tiếp. **Không mã hoá bằng màu đơn thuần**: luôn kèm dấu +/− và tên.
- Mỗi phần tử chữ phải xuất matte vào `elements.json` **tự động từ mẫu** (P0, P1, G4; RUN.md §3.1).

**Font**
- RIGHTS hiện chỉ có **DejaVu Sans** (C4-F1).
- Đề xuất thêm ba tệp cùng gói `fonts-dejavu-core`, cùng giấy phép Bitstream Vera / public domain, mỗi tệp một dòng RIGHTS kèm SHA-256:
  - `DejaVuSans-Bold.ttf`;
  - `DejaVuSerif.ttf`;
  - `DejaVuSerif-Bold.ttf`.
- Vai trò:
  - Serif Bold cho số lớn và tiêu đề (chất "bản in");
  - Sans cho nhãn và nguồn.
- Cỡ chữ (1080p): tối thiểu 30 px, vì 16–18 px của bài thử không đọc được trên điện thoại (R4 của THU-PHONG-CACH); số lớn 160–220 px; tiêu đề 64 px.
- Số theo kiểu Anh: 40,000; −34% với dấu trừ U+2212.

**Bảng màu** (tương phản đo bằng công thức WCAG trên màu phẳng)

| Token | Hex | Trên nền đêm #141B2D | Trên giấy #EFE6D2 | Vai trò |
|---|---|---|---|---|
| Nền đêm | #141B2D | — | — | nền khung số liệu |
| Giấy ngà | #EFE6D2 | 13,8:1 | — | chữ chính trên nền đêm; nền bản đồ |
| Hổ phách | #F0A94A | 8,6:1 | 1,6:1 (**cấm dùng làm chữ trên giấy**) | đèn khí, nghề tăng |
| Trắng lạnh | #DCE6F0 | 13,6:1 | — | đèn điện, nghề giảm |
| Xám chú thích | #A7B1C2 | 7,9:1 | — | dòng nguồn |
| Mực nâu | #2E2219 | — | 12,4:1 | chữ trên bản đồ giấy |
| Hổ phách đậm | #8A4F0E | — | 5,3:1 | chữ hổ phách trên giấy |
| Lam mực | #2B4A6F | — | 7,3:1 | đường, nhãn phụ trên giấy |

- G4 đo trên ảnh render (vân giấy và grain làm giảm tương phản). **Mục tiêu thiết kế ≥ 7:1, sàn 4,5:1.** Chữ đặt trên mảng phẳng, không đặt trên vũng sáng.
- Hổ phách và trắng lạnh chỉ chênh độ sáng 1,59:1, nên luôn ghi nhãn trực tiếp.
- Tránh dải chuyển màu mịn diện rộng (G3 banding); dùng vân giấy và dither.

**Mẫu**
| Mẫu | Mô tả | Chuyển động |
|---|---|---|
| **D-MAP** | bản đồ giấy phẳng, đường mực lam, tuyến và chấm hổ phách hoặc trắng; nhãn địa danh và năm | đường vẽ dần 1–2 s (ease-out); chấm "bắt lửa" 0,3–0,5 s, đồng bộ với ánh sáng B3 v2 |
| **D-BAR** | cột là cột đèn cắt giấy (cột, thanh ngang), cùng thang, mốc 100 = năm gốc | mọc từ đáy 18–24 khung, so le 6 khung; không nảy |
| **D-GRID** | lưới biểu tượng đơn vị (270 ô) | ô chao ±2 %; ô tắt mờ trong 12 khung |
| **D-TL** | dòng thời gian ngang trên nền đêm, mốc có năm | trượt ngang, mỗi mốc giữ ≥ 3 s |
| **D-NUM** | thẻ số neo: số lớn, một dòng giải nghĩa, nguồn | bộ đếm chạy 1,5–2,5 s, **dừng đúng số thật**, giữ ≥ 2 s |
| **D-SRC** | thẻ nguồn: tên ngắn + năm; tham chiếu đầy đủ đặt ở mô tả video | — |

- **Vào và ra:** trượt 20 px kèm bóng giấy hiện dần trong 12 khung (ease-out); ra trong 8–10 khung (ease-in).
- **Thời gian đọc:** mỗi số đứng trên màn hình ≥ 3 s, cộng 0,3 s cho mỗi từ chú thích.

**Số thật và minh hoạ**
- **Số thật có nguồn:** không gắn nhãn minh hoạ. **Dòng nguồn luôn hiện khi số còn trên màn hình**, góc dưới trái, 30 px, màu xám chú thích. Ví dụ: "Source: U.S. BLS Employment Projections 2025–35".
- **Hình không đúng tỉ lệ dữ liệu** (mảng tối Manhattan, tuyến đèn 03-03, "đội quân" 03-07, đám đông): gắn thẻ "**Illustrative**" ở góc trên phải, 30 px. Bản đồ gắn thêm "Not to scale".
- **Mọi số BLS** phải ghi "U.S. projection" và kỳ dự báo. Không đặt số 2023–33 và 2025–35 trên cùng một trục.

**Ứng với số liệu V2 §4**

| Mẫu | Số liệu (shot) |
|---|---|
| D-MAP | D1 (02-02), D4 (02-05), D6, D7 (04-01, 04-03), [16] Paris (04-04), D8 (05-07), D9 (05-08), D10 (06-01) |
| D-TL | D2, D3 (02-04), D12, D13 (07-01) |
| D-NUM | D4 (02-06), D14 (08-02), D15 (08-04), D4 + D14 + D15 (08-07), D21 (11-04), D23 (12-01), 4 số neo (14-02) |
| D-BAR | D4 với D14 (07-02), D23–D27 (12-02, 12-03), D32–D35 (13-01), D30 (13-02), D36 (13-03) |
| D-GRID | D21 (11-02, 11-03) |
| Nhãn trên hình | D16 (08-05), D17, D18 (08-06), D28 (12-04) |
| Chỉ có trong lời dẫn | D5, D22; không dùng D11, D31 |

---

## 3. Ngân sách

### 3.1 Token (ước)
Gốc ước: THU-PHONG-CACH §4.4–4.5. Shot truyện mới khoảng 10–15 nghìn token mỗi shot; đoạn `lp20` tốn 0,14 triệu mỗi phút.

| Hạng mục | Cách tính | Token |
|---|---|---|
| W-A truyện R (28 shot) | 28 × 6 nghìn (đổi máy, nhịp, B3) | 170 nghìn |
| W-B truyện A và N 3D (18 shot) | 10 × 12 nghìn + 8 × 15 nghìn + tài sản mới (Covent Garden 40 nghìn, bộ bóng cảnh sát / người hiện đại / đám đông 35 nghìn, mặt tiền Peale và Market St 15 nghìn, đồng hồ 10 nghìn) | 340 nghìn |
| W-D số liệu (32 shot 2D) | 6 mẫu, một lần, 150 nghìn + 32 × 6 nghìn | 340 nghìn |
| W-S âm | VO 40 + nhạc 60 + SFX 20 + mix / stem / phụ đề 40 + RIGHTS 10 (nghìn) | 170 nghìn |
| Shorts ×3 | 3 × 15 nghìn | 45 nghìn |
| Dự phòng sửa (một lượt cho khoảng 30 % shot) | — | 150 nghìn |
| **Xưởng** | | **≈ 1,22 triệu → 0,13 triệu/phút** |
| Kiểm mù | 6 dải + 2 đối chứng, khoảng 45 nghìn mỗi dải (số thật vòng trước: 45 nghìn/dải) | 360 nghìn |
| Kiểm số liệu độc lập | một phiên | 80 nghìn |
| P điều phối | animatic, hàng đợi, đóng gói, luật, báo cáo, merge | 250 nghìn |
| **Cả tập** | | **≈ 1,9 triệu → 0,20 triệu/phút** |
| Kịch bản xấu | thêm một lượt sửa và kiểm mù lại 3 dải | ≈ 2,2 triệu → 0,23 triệu/phút |

Lượt B3 v2 đang chạy song song **không tính** vào đây. Không tính K, vì không đổi luật.

### 3.2 Giờ render (ước; đo thật ở M2.0)
- **Khung hình:**
  - 3D B3 (R + A + N 3D, 272 s): 6 528 khung;
  - 2D số liệu (299 s): 7 176 khung.
- **Tốc độ đã đo** ở 960×540: 0,96–2,36 s mỗi khung (B3).
- **Ước 1080p:** 3,5–9,6 s mỗi khung, tức gấp 2,5–4 lần với 4 lần số điểm ảnh. Đây là **ước**; chưa có chuỗi 1080p nào được đo.

| Việc | Giờ máy |
|---|---|
| Thử 960×540 cho animatic (một lượt 3D) | 1,8–4,4 |
| Render 1080p 3D | 6,3–17,4 |
| Render lại cho các sửa (khoảng 30 % shot) | 2–5 |
| Đồ hoạ 2D 1080p (numpy; ước 0,2–0,5 s/khung) | 0,4–1,0 |
| Shorts 3D bằng máy dọc (08: khoảng 29 s) | 0,7–1,9 |
| Mặt nạ C3, bóng nhân vật, kiểm toán | 1–2 |
| Luật máy (khoảng 60 s cho mỗi 8 s phim, RUN.md §5) × 2 lượt master | 2–3 |
| **Tổng** | **≈ 14–34 giờ, trung tâm ≈ 20 giờ** trên một làn nặng (`queue.sh`) |

### 3.3 Số lượt kiểm
- Luật máy, profile `shot`: theo gói, mỗi gói tối đa 2 lượt.
- Profile `youtube` cho master: 1–2 lượt.
- Shorts: 3 lượt.
- Kiểm số liệu: 1 lượt, cộng 1 lượt xác nhận sau khi sửa.
- Kiểm mù: 1 lượt 8 dải; nếu trượt thì lặp lại tối đa 3 dải.
- Chủ dự án duyệt: 3 điểm dừng (mục 7).

### 3.4 Đối chiếu tiêu chí
- **Tiêu chí 2** (≤ 0,3 triệu token mỗi phút): ước 0,20–0,23. **Đạt, dư khoảng 25–33 %.** Không nằm trong vùng ±5 %.
- **Tiêu chí 3** (một tập 8–10 phút trong một chu kỳ hạn mức tuần, làm mới Chủ nhật 17:00): **đang sát.**
  - Token 1,9–2,2 triệu là khả thi; Cổng 6 dùng khoảng 4,3 triệu trong 3 ngày. **P cần điền số hạn mức tuần thật** để tính tỉ lệ.
  - Giờ máy 14–34 giờ trên một làn là vừa.
  - Điểm nghẽn thật nằm ở ba chỗ: thời gian chờ chủ dự án duyệt (3 điểm dừng); hàng đợi chỉ một render nặng mỗi lúc; tốc độ 1080p chưa đo.
- **Đề xuất:**
  - mở M2.1 ngay sau một lần làm mới Chủ nhật 17:00;
  - xong M2.0 trước mốc đó, vì M2.0 rẻ, không render nặng và không tính vào chu kỳ;
  - xếp render theo thứ tự: 2D chạy song song ở làn nhanh khi mỗi việc < 60 s, 3D chạy làn nặng liên tục;
  - mỗi gói tự chạy luật `shot` trên chuỗi của mình để P không phải sửa vòng sau.

### 3.5 Chia gói và mốc nhỏ
| Mốc | Gói | Token (phần chu kỳ) | Render | Phụ thuộc |
|---|---|---|---|---|
| **M2.0 Chuẩn bị** (ngoài chu kỳ) | P + W-D (một khung mẫu mỗi loại) + W-S (thử giọng, nháp `flite`) | ≈ 120 nghìn | đo 1 shot 1080p trọn (khoảng 0,2 giờ) | — |
| **M2.1 Animatic nhịp** | P; W-S thu VO trọn | ≈ 200 nghìn (10 %) | khoảng 2–4 giờ (960×540) | M2.0 duyệt |
| **M2.2 Sản xuất** | W-A, W-B, W-D, W-S song song | ≈ 1,0 triệu (50 %) | 10–25 giờ | W-A chờ B3 v2 được duyệt |
| **M2.3 Master + Shorts + luật** | P | ≈ 150 nghìn | 2–4 giờ | M2.2 |
| **M2.4 Kiểm và duyệt** | phiên kiểm số, kiểm mù (P), chủ dự án | ≈ 450 nghìn | — | M2.3 |

---

## 4. Giọng đọc

### 4.1 Phương án A — ElevenLabs (đề xuất)

**Người kể**
- Giọng phải khác hẳn Ida (bà lão).
- Gợi ý: giọng trưởng thành, ấm, trung tính, tốc độ 140–155 từ/phút. Khẩu âm (Anh hay trung–Đại Tây Dương) do chủ dự án chọn: truyện xoay quanh London, còn số liệu chủ yếu của Mỹ.
- **Nguồn đề xuất: Voice Library.**
  - Lọc tiếng Anh, use case narration, `notice_period` ≥ 730 ngày.
  - Sàng sơ bằng bản nghe mẫu có sẵn của thư viện (không tốn ký tự).
  - Sau đó thử 2 giọng thư viện và 1 giọng Voice Design trên cùng đoạn văn của tập.
  - Ưu: tránh rủi ro "Beta" còn mở của Voice Design (RIGHTS M1-V3). Nhược: chủ giọng có thể rút giọng; thời hạn báo trước bảo vệ 730 ngày.
- Giấy phép: "All paid plans include a commercial license, provided you're not using Beta Services." (đã trích trong RIGHTS M1-V3).
- Khi chọn giọng, ghi một dòng RIGHTS **E1-VO-N1**: voice_id, nguồn, chủ giọng, notice_period, câu điều khoản kèm link, phạm vi YouTube / bán phim, SHA của từng take.

**Mô hình**
- Đề xuất dùng mô hình đa ngôn ngữ ổn định cho bài dài (`eleven_multilingual_v2`), có nối ngữ cảnh giữa các đoạn (previous_text / next_text), để giữ giọng đều suốt 9 phút.
- Hoặc dùng `eleven_v3` (GA, đang dùng cho Ida) nếu bản thử cho thấy đủ đều.
- **Chọn bằng bản thử**, không chọn theo cảm nhận.
- Đơn giá ký tự của từng mô hình: P kiểm lại trên trang usage, không đoán.
- Thoại Ida dùng lại L1 và L2 (C4-D1), **0 ký tự**.

**Ước ký tự**
| Hạng mục | Ký tự |
|---|---|
| Thử 3 ứng viên × khoảng 500 ký tự (đoạn 02 và 10) | 1 500 |
| Đọc trọn lần 1 (máy đếm 7 380; dùng 7 750) | 7 750 |
| Làm lại theo câu (khoảng 25 %) | 1 950 |
| Sửa sau animatic (khoảng 10 %) | 800 |
| Câu mở riêng cho 3 Shorts | 400 |
| **Cơ bản** | **12 400 (42 % của 29 400)** |
| Xấu: thêm 1 lần đọc trọn (đổi giọng hoặc mô hình) | 20 150 (69 %) |
| Rất xấu: thêm 2 lần đọc trọn | 27 900 (95 %; **trong ±5 % quanh trần**) |

**Luật dùng ký tự**
- Mọi lần đọc trọn thứ hai phải được chủ dự án đồng ý trước.
- Nếu còn dưới 10 000 ký tự trước lượt làm lại cuối: chờ kỳ làm mới **23/10/2026** hoặc nâng gói.

**Khi nào nâng gói**
- **Hiện chưa cần.**
- Chỉ nâng khi một trong ba điều xảy ra:
  - (a) phải xong tập trước 23/10 mà cần hơn một lần đọc trọn thêm;
  - (b) định dạng đầu ra của gói Starter (bitrate, PCM) không đạt yêu cầu master. P kiểm định dạng trên một take ngắn;
  - (c) sản xuất tập 2–6 dồn vào một kỳ.

**Việc chủ dự án cần làm**
1. **Không cần gắn khoá.** Proxy của môi trường đã gắn khoá cho `api.elevenlabs.io`.
2. **Duyệt giọng người kể** (nghe 3 mẫu ở M2.0) và ghi vào AUTHORSHIP.
3. **Quyết có nâng gói không.** Đề xuất: chưa.
4. Nếu muốn dùng khoá ở phiên hoặc môi trường khác: vào cài đặt môi trường cloud (**Environment settings → environment variables / credentials**). **Khoá không bao giờ commit vào repo.**

### 4.2 Phương án tạm — TTS có sẵn trong môi trường (chỉ để nháp nhịp)

**Đã kiểm, chỉ liệt kê:**
- **ffmpeg có bộ lọc `flite`** (libflite 2.2; giọng `awb`, `kal`, `kal16`, `rms`, `slt`).
- `sox` có sẵn để chỉnh tempo cho khớp 150 từ/phút.
- **Không có** piper, espeak, Coqui hay kokoro, trong `/opt/cine` cũng như trên hệ thống.
- `faster_whisper` đã cài nhưng chưa có mô hình trong cache (`/opt/hf-cache` rỗng); không tải.

**Cách dùng:**
- dựng nháp nhịp animatic M2.1, đo thời lượng từng đoạn trước khi tiêu ký tự;
- **không phát hành**;
- nếu tệp nháp nằm trong repo, ghi RIGHTS là "chỉ nội bộ".

---

## 5. Nhạc

**Tài sản đã có:** C4-M1 / M0-M1 (ACE-Step 1.5) là **nhạc tạm**, không được dùng cho YouTube hay bán: dữ liệu huấn luyện chưa rà, giấy phép MIT chỉ áp cho mã. SFX tự tổng hợp C4-S1 **được dùng mọi phạm vi** và dùng lại được: phụp, rơ-le, rè điện, chuông, bước chân, van.

| Phương án | Giấy phép | Ưu / nhược | Ghi vào RIGHTS |
|---|---|---|---|
| **1. Tự sinh bằng mã (đề xuất)** | tác phẩm của dự án | Ưu: sạch quyền, không bị Content ID nhận nhầm; chủ dự án đặt motif và giai điệu (đóng góp biểu đạt, ghi AUTHORSHIP). Nhược: âm sắc tổng hợp dễ "rẻ" | mã sinh, hạt giống, SHA bản xuất, "Được mọi phạm vi" |
| 1b. Bản nhạc tự viết, phát bằng bộ mẫu nhạc cụ: **VSCO 2 Community Edition** (CC0) hoặc **Salamander Grand Piano** (CC BY 3.0) | CC0 / CC BY | Ưu: âm thật hơn. Nhược: phải tải bộ mẫu (khoảng vài trăm MB), nằm ngoài gói này | URL, câu giấy phép kèm link, SHA tệp mẫu, dòng ghi công cho CC BY (mô tả video và credit cuối) |
| 2. Thư viện: Freesound (lọc CC0), Free Music Archive (chỉ CC BY / CC0), incompetech (CC BY 4.0), Musopen (bản thu public domain, kiểm từng bản) | CC0 / CC BY | Ưu: nhanh. Nhược: rủi ro bị Content ID nhận nhầm, nhạc nghe "kho" | như 1b; **loại mọi NC, ND; tránh SA** (SA có thể buộc giấy phép lên phim); **không dùng YouTube Audio Library** |

**Thủ tục ghi RIGHTS**
- Mỗi tệp một dòng, mã E1-MU-xx hoặc E1-SX-xx, gồm: tài sản, loại, URL nguồn, tác giả, câu giấy phép trích nguyên văn kèm link, phạm vi (YouTube / bán phim), dòng ghi công, SHA-256, ngày thêm.
- Ảnh chụp trang giấy phép lưu ở `reports/m3/rights/`.

**SFX mới:** cửa thang máy có tay gạt, máy đánh chữ, giắc tổng đài, đám đông, giấy báo. Tự tổng hợp như C4-S1, hoặc lấy Freesound CC0.

---

## 6. Shorts (9:16, 1080×1920, 24 fps, < 60 s)

**Quy ước chung**
- Vùng chữ an toàn (ước theo giao diện Shorts, kiểm lại trên điện thoại): x 60–960, y 240–1500. Tránh mép phải khoảng 140 px và đáy khoảng 420 px.
- Phụ đề cháy vào hình, chữ ≥ 44 px.
- Dòng nguồn luôn hiện.
- Đồ hoạ dựng lại bằng mẫu ở bố cục dọc (không cắt từ 16:9). Shot 3D render bằng máy dọc riêng.

| Short | Nguồn | Dài | 2 giây đầu | Khung dọc | Chữ trên màn hình |
|---|---|---|---|---|---|
| S1 "London still has 5 lamplighters" | đoạn 08 (bỏ câu Westminster nếu cần) | khoảng 42–49 s | số **5** lớn trên nền Covent Garden đêm; VO mở mới: "London still has gas street lamps, and five people to look after them." | 08-01 và 08-03 render dọc; 08-05 insert đồng hồ | "5 lamplighters" · "~1,500 (2015) → ~1,100 (2023)" · nguồn NPR 2015 / British Gas 2023 |
| S2 "Which jobs are shrinking fastest in America?" | đoạn 12 (câu mở đổi theo V2 §7) | khoảng 47 s | **−34%** + biểu tượng máy đánh chữ | 5 cột đèn xếp dọc thành thanh ngang, cùng thang | "U.S. BLS projections, 2025–35" luôn hiện; "Forecasts, not verdicts" |
| S3 "One job in 270" | đoạn 11 + hai câu đầu của đoạn 12 | khoảng 44 s | lưới biểu tượng, một ô tắt + "**1 in 270**" | lưới dọc khoảng 15 × 18 ô | "1950 → 2010 · Bessen (2016)" |

---

## 7. Kiểm và điểm dừng

**Luật máy** (theo `checks/RUN.md` v1.5)
- **Profile `shot`:** mỗi gói chạy cho chuỗi của mình.
- **Profile `youtube`:** cho master.
  - N1: 24 fps CFR.
  - N2: BT.709, dải limited.
  - N3: bitrate ≥ 30 Mbps vì có grain.
  - P0: mọi chữ có matte. Chữ diegetic (biển phố) không được trùng phụ đề.
  - P1: không chữ đè chữ.
  - G4: tương phản ≥ 4,5:1.
  - G3 / G3b: banding, grain.
  - M1: −14 LUFS ±1, true peak ≤ −1 dBTP.
  - M3: tương thích mono.
  - J1 / J1b: `X.script.txt` gồm **cả lời dẫn và thoại Ida**, mỗi câu một dòng. Stem `dialogue` chứa VO và Ida, không có gì khác.
  - H1 / H1b, C3, O3: áp cho shot có nhân vật.
- **Hai điểm cần K xác nhận** (P ghi vào `checks-appeal.md`, không lách luật):
  - (a) C3 cho nhân vật bóng mới chưa có model sheet (cảnh sát, người thắp đèn hiện đại, đám đông) sẽ cho kết quả THIẾU hoặc CẦN NGƯỜI XEM;
  - (b) Shorts 9:16 không hợp N3 (16:9). Tạm thời: chạy profile `shot` và đo loudness riêng; đề nghị K thêm profile `shorts`.
- Bản sao báo cáo luật phải chép danh sách chỉ số trong ±5 % vào báo cáo gói.

**Kiểm số liệu và nguồn**
- Do một phiên độc lập làm: không phải xưởng W-D, không phải phiên biên kịch.
- Đầu vào:
  - `numbers.json` do P lập từ V2 §4: D#, chuỗi hiển thị cho phép, quy tắc làm tròn, nhãn kỳ, nguồn;
  - chuỗi chữ lấy thẳng từ `elements.json` của từng shot.
- Bảng kết quả gồm: shot, chữ trên màn hình, D#, nguồn, khớp hay không, nhãn kỳ, nhãn Illustrative, khớp với lời dẫn.
- **Mọi lệch là DỪNG.**
- Mục cần chú ý:
  - D12 (Paris 1962, trung bình–thấp);
  - D9 (Broadway, chỉ qua tóm tắt);
  - [16] Paris giữa thế kỷ, chưa có D#;
  - 13-03 không in số suy ra.

**Kiểm mù 6 dải** (`scripts/p/kiem_mu.py dai`, mỗi dải một subagent mới, cộng 2 đối chứng Sprite Fright)

| Dải | Shot | Nhằm kiểm |
|---|---|---|
| 1 | 01-03 → 01-04 | bóng Ida, tay hơ kính (lời chê R1 cũ) |
| 2 | 05-05 → 05-06 | ánh sáng bám nguồn, sóng trắng (lời chê lặp 4/4 dải) |
| 3 | 08-01 → 08-05 | set mới và bóng người hiện đại |
| 4 | 10-04 → 10-07 | hiểu truyện (tắt ngọn cuối, trao đèn) |
| 5 | 02-05 → 02-06 | nhớ số (40,000) |
| 6 | 12-01 → 12-03 | nhớ số (−34 %), độ đọc của cột |

**Câu hỏi**
- Giữ nguyên văn câu hỏi các vòng trước.
- Thêm: "Chấm chất lượng hình ảnh 1–10 so với phim hoạt hình chuyên nghiệp, nêu một lý do."
- Dải 5 và 6 thêm: "Bạn nhớ được những số liệu nào?"
- Dải 1–4 thêm: "Chuyện gì xảy ra trong đoạn này?"

**Ngưỡng**
- 0 dải có từ khoá chê "búp bê / mặt nạ / sáp / rẻ tiền" chỉ vào nhân vật.
- Không có lời chê lặp cùng một chỗ ở ≥ 2 dải.
- Mỗi dải số liệu nhớ được ≥ 2 số.
- Điểm 1–10 chỉ dùng để tham khảo. Mục tiêu mềm ≥ 6, gần đối chứng 6,5.

**Chủ dự án duyệt:** xem bản dựng master, chấm ≥ 8/10 (tiêu chí 1).

**Điểm dừng**
| Mốc | Đi tiếp khi | DỪNG khi |
|---|---|---|
| M2.0 | chủ dự án duyệt giọng người kể, bộ mẫu dữ liệu (5 khung mẫu), bảng shot; có số đo 1080p thật | tốc độ 1080p > 9,6 s mỗi khung (giờ máy vượt khoảng 34 giờ), nên phải tính lại tiêu chí 3 |
| M2.1 | animatic ≤ 10:00 (nếu quá thì cắt 07); chủ dự án duyệt nhịp; ký tự đã dùng ≤ 15 000 | quá 10:00 sau khi cắt 07; người kể bị chê |
| M2.2 | mỗi gói qua profile `shot`; lượt B3 v2 đã duyệt trước khi W-A render | đã tiêu 60 % token của M2.2 mà xong < 50 % số shot; luật trượt lặp ở cùng một luật |
| M2.3 | master qua `youtube` (hoặc chỉ còn các mục chờ K đã ghi rõ); 3 Shorts < 60 s | luật Chặn trượt |
| M2.4 | kiểm số khớp 100 %; kiểm mù đạt ngưỡng; chủ dự án ≥ 8/10, ghi AUTHORSHIP | bất kỳ số nào lệch nguồn; lặp lời chê; tổng token > 2,85 triệu (0,3 triệu/phút) |

---

## 8. Rủi ro

| # | Rủi ro | Mức | Xử lý |
|---|---|---|---|
| R1 | Thời lượng sát trần 10:00 (4,8 %). Đoạn 08 và 13 không còn dư; tốc độ người kể chưa biết | cao | đo trong animatic M2.1; cắt 07 trước |
| R2 | B3 v2 chưa xong. Nếu lời chê ánh sáng hoặc "bóng phẳng" còn, tiêu chí 1 trượt | cao | W-A chờ B3 v2; W-D và W-S không phụ thuộc nên chạy trước |
| R3 | Tiêu chí 3: chờ duyệt, một làn render, tốc độ 1080p chưa đo | vừa–cao | M2.0 ngoài chu kỳ; render 2D song song ở làn nhanh |
| R4 | Nhân vật bóng mới không có model sheet, nên C3 không đo được | vừa | K xác nhận phạm vi trước M2.2 |
| R5 | Đồ hoạ nhiều chữ cần nhiều matte cho P0 | vừa | mẫu tự xuất `elements.json` |
| R6 | Sai số hoặc nhãn: lẫn kỳ 2023–33 với 2025–35; D12 và D9 yếu; [16] chưa có D#; số 81 suy ra | vừa | kiểm số độc lập; đề nghị biên kịch bổ sung D# cho [16] |
| R7 | Giọng: Beta Voice Design (Ida) phải đóng trước Cổng 9 (bán); chủ giọng thư viện có thể rút giọng | vừa | thư viện có notice ≥ 730 ngày; lưu take gốc kèm SHA |
| R8 | Chưa có nhạc phát hành được; nhạc sinh bằng mã có thể nghe rẻ | vừa | phương án 1b; chủ dự án duyệt motif sớm (M2.1) |
| R9 | Master khoảng 9,5 phút ở ≥ 30 Mbps, cỡ khoảng 2 GB, không đưa vào git được | vừa | chủ dự án chọn nơi lưu; git chỉ giữ bản xem trước < 50 MB |
| R10 | Shorts không hợp N3 | thấp | profile `shorts` (K) |
| R11 | Tên "Last Lamplighters" chưa tra nhãn hiệu; sách London Encyclopaedia tr. 838 chưa đọc | vừa (trước khi mở kênh) | tồn đọng từ V2 |
| R12 | Hình gợi đến người hoặc thương hiệu thật (nhân viên British Gas, logo) | thấp | bóng hư cấu, không logo, không tên người |

## 9. Việc chủ dự án cần quyết

1. Duyệt bảng shot 78 shot, dùng lại 38 % thời lượng. Duyệt các tài sản mới: Covent Garden, bóng cảnh sát, đám đông, người thắp đèn hiện đại.
2. **Duyệt giọng người kể** (3 mẫu ở M2.0): giới, tuổi, khẩu âm; thư viện hay Voice Design. Ghi vào AUTHORSHIP.
3. **Nâng gói ElevenLabs hay không.** Đề xuất: chưa; xem lại nếu còn dưới 10 000 ký tự trước 23/10.
4. Duyệt bộ mẫu dữ liệu: bảng màu; thêm 3 font DejaVu vào RIGHTS; quy ước "Illustrative"; 13-03 ghi "~19% below" thay vì "81".
5. Chọn hướng nhạc (đề xuất 1 hoặc 1b) và đặt motif (đóng góp biểu đạt).
6. Nơi lưu master và quy ước `out/`.
7. Cho phép cắt đoạn 07 nếu animatic vượt 10:00.
8. Đồng ý để P gửi K hai điểm: C3 cho nhân vật bóng mới, profile Shorts.
9. Thời điểm mở chu kỳ M2.1 (ngay sau một lần làm mới Chủ nhật 17:00).
10. Tồn đọng: tra nhãn hiệu tên kênh; có đọc bản giấy London Encyclopaedia tr. 838 trước khi thu giọng hay không.

**Đang chờ chủ dự án:** các mục 1–10 ở trên; trước hết là các mục 2, 4 và 9 để mở M2.0 và M2.1.
