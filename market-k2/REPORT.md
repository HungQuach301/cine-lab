# Kênh 2: chọn ngách bằng YouTube Data API v3 (11/10/2026)

**Kết luận:** chọn **B, lịch sử doanh nghiệp/ngành**, đi theo góc *cơ chế kinh tế của một ngành*. **A, lịch sử tiền/ngân hàng**, làm dự phòng. B đứng đầu ở cả 12 kịch bản độ nhạy (mỗi trọng số ±5 điểm). Dự phòng là A trong 11 kịch bản, và là D khi trọng số e giảm 5 điểm.
**Đang chờ chủ dự án:** duyệt ngách, ghi vào `AUTHORSHIP.md`.

**Phương pháp.** Mọi chỉ số là **tự tính, không phải chỉ số YouTube**.
- 48 lượt `search.list` (8 câu hỏi khán giả Mỹ × 6 ngách, 25 kết quả/lượt), regionCode=US, đăng trong 90 ngày. Quota khoảng 5 100 đơn vị.
- "Video dài" = video ≥ 8 phút. Haiku lọc kênh không lộ mặt, dạng giải thích/tài liệu. Haiku cũng đọc tiêu đề và mô tả để chấm cờ thời sự (a), khoảng trống (c) và trùng khán giả (f).
- Lấy ≤ 15 kênh/ngách, mỗi kênh 50 video dài gần nhất. Bỏ video đăng chưa đủ 14 ngày.
- **Video nổ:** lượt xem ≥ 3× trung vị kênh trong ±90 ngày, hoặc ≥ 3× số người đăng ký. Cột "nổ" bên dưới thêm điều kiện ≥ 10 nghìn lượt xem; tỷ lệ theo đúng định nghĩa gốc ghi trong ngoặc.
- Chi phí AI: Haiku $0,12 (phân loại) + reviewer $0,16, tổng ≈ $0,30 / trần $5. Mã nằm ở `collect.py` và `analyze.py`. Số liệu thô để ngoài git (`~/.cache/cine-market-k2`), tự xoá sau 30 ngày.

## Bảng 6 ngách
| | A Tiền/NH | **B Doanh nghiệp** | D Bản đồ | E Công cụ & AI | J Nhà ở | L Năng lượng |
|---|---|---|---|---|---|---|
| a. Nổ (gốc) / cờ thời sự | 13 % (22) / 18 % | **23 % (27) / 8 %** | 19 % (21) / 8 % | 5 % (27) / 25 % | 22 % (29) / 15 % | 18 % (31) / 28 % |
| b. Kênh < 2 năm có nổ / top 5 chiếm | 4/7 / 91 % | **4/5 / 71 %** | 3/4 / 91 % | 2/8 / 100 % | 11/12 / 88 % | 6/11 / 98 % |
| c. Top 10 thiếu dữ liệu thật + hình công phu | 100 % | 100 % | 100 % | 100 % | 90 % | 90 % |
| d. Trung vị phút video nổ | 17 | 25,6 (top 25: 17) | 29,7 | 30,7 | 21,8 | 13,9 |
| d. Số tập tới 4 000 h (8 000 h) | 1,1–1,4 (2,2–2,8) | 1,8–2,3 (3,5–4,5) | 0,7–0,9 (1,5–1,9) | 126–162 | 1,5–1,9 (2,9–3,7) | 5,5–7,1 (11–14) |
| e. CPM công khai, USD (ghép) | 11,5–28,5 | 9,5–23,5 | 4–10 | 8–20 | 8,5–21 | 6,5–16 |
| e. Video nổ có tài trợ/affiliate | 5 % | **28 %** | 19 % | 6 % | 17 % | 16 % |
| f. Trùng Crux / trùng LL / kênh trẻ ra hàng loạt | 20 / 7 / 33 % | **0 / 0 / 27 %** | 0 / 0 / 13 % | 7 / 27 / 27 % | 13 / 13 / 53 % | 13 / 7 / 47 % |
| Điểm thành phần e·d·(a+c)·nhà máy·b·f | 7,0·9,2·7,0·7·3,9·3,2 | 8,1·8,3·10·6·9,1·1,4 | 1,9·10·8,8·9·5,2·1,1 | 3,9·0·5,0·7·0·2,8 | 5,8·8,7·4,4·8·7,1·3,2 | 3,8·6,1·3,1·9·2,6·2,4 |
| **Tổng /100** | 61,1 | **73,6** | 59,9 | 27,5 | 56,4 | 41,4 |

**Cách tính các chỉ số**
- **Chấm điểm:** mỗi chỉ số chuẩn hoá min–max về 0–10. Trọng số: e 25 · d 20 · a+c 20 · nhà máy 15 · b 10 · trừ f 10. Riêng d dùng thang log, để E không ép dẹt các ngách còn lại.
- **a:** cờ thời sự trừ nửa trọng số của tỷ lệ nổ.
- **d:** số tập = 4 000 h ÷ (lượt xem/tập × phút × tỷ lệ xem 35–45 %, giả định). Lượt xem/tập lấy phân vị 75 trong trung vị lượt xem của các kênh < 2 năm; mục tiêu là "kênh mới làm tốt", không phải kênh trung bình. Con số này **lạc quan**, vì các kênh trẻ trong mẫu đã được search chọn ra, tức là kênh sống sót. Còn phải đạt 1 000 người đăng ký. Mức 8 000 h là giả định của chủ dự án cho kênh mở sau 1/2/2027; tôi chưa kiểm được chính sách này.
- **e:** CPM (**không phải RPM**), khán giả Mỹ, lấy trung bình các dòng gần nhất: [OutlierKit 13/09/2026](https://outlierkit.com/resources/youtube-niches-guide/) cho Personal Finance 18–45, Business 14–35, Real Estate 12–30, AI & Tech 8–20, History 5–12; [VloggingPro 2026](https://vloggingpro.com/youtube-cpm/) cho Travel 3–8. Không có dòng riêng cho địa lý hay năng lượng. [AIR Media‑Tech 2025](https://air.io/en/monetization/how-much-can-creators-make-with-adsense-in-2025) ghi mức trung bình toàn cầu thấp hơn nhiều (Business & Finance 4,70), vì vậy chỉ nên tin vào **thứ hạng** giữa các ngách, không tin vào mức tuyệt đối.
- **Nhà máy (định tính):** D 9, L 9, J 8, A 7, E 7, B 6.

## Ưu, nhược, tác động, rủi ro
- **B (thắng).**
  - *Ưu:*
    - tỷ lệ nổ cao nhất kèm ít thời sự nhất, nên nội dung sống lâu;
    - top 5 kênh chỉ chiếm 71 % lượt xem, thị trường ít tập trung nhất;
    - 4/5 kênh trẻ đã có video nổ;
    - 28 % video nổ có tài trợ, đây là nguồn thu thứ hai;
    - không trùng khán giả Crux hay LL.
  - *Nhược:* các đề tài kể lại kiểu "Kodak/Blockbuster/Nvidia sụp đổ ra sao" đã ngập video AI làm hàng loạt, video đầu chỉ vài chục đến vài nghìn lượt xem. Cầu nằm ở góc *cơ chế ngành*: vì sao chỉ vài nước hay vài hãng làm được X, một cửa hàng thay đổi kinh tế địa phương ra sao, một mô hình kinh doanh sụp vì đâu.
  - *Tác động:* dùng lại được quy trình nguồn xác minh và bộ kiểm. Phần 3D dùng cho nhà máy, tàu, chuỗi cung ứng, nhưng ít hơn D hoặc L.
  - *Rủi ro:* phát ngôn về công ty thật dễ sai sự thật hoặc thành phỉ báng, nên mọi khẳng định phải có nguồn. Tránh giọng "công ty đáng bị thế". Dễ trượt sang dạng video AI hàng loạt.
- **A (dự phòng).**
  - *Ưu:* CPM cao nhất; ra tiền nhanh (1,1–1,4 tập, theo giả định lạc quan).
  - *Nhược:*
    - lượt xem rất phân cực: kênh trẻ điển hình chỉ khoảng 730 lượt/video;
    - top 5 kênh chiếm 91 %;
    - chỉ 5 % video nổ có tài trợ.
  - *Rủi ro:* nhóm YMYL, nên persona AI "nhà phân tích" là rủi ro chính sách cao nhất. Trùng 20 % kênh với tài chính cá nhân (Crux).
- **D.**
  - *Ưu:* ra tiền nhanh nhất; 3D bản đồ hợp nhà máy nhất.
  - *Nhược:* CPM thấp nhất (4–10).
  - *Rủi ro:* top 5 chiếm 91 %; doanh thu trên mỗi lượt xem có thể chỉ bằng ½ của A hoặc B.
- **J.**
  - *Ưu:* kênh mới dễ vào nhất (11/12 kênh trẻ có video nổ).
  - *Nhược:* 53 % kênh trẻ ra video hàng loạt, nguồn cung AI dày nhất.
  - *Rủi ro:* chính trị hoá (zoning); trùng Crux 13 %.
- **L.**
  - *Ưu:* hợp 3D.
  - *Nhược:* 28 % video mang tính thời sự (data center, giá điện); kênh trẻ điển hình chỉ khoảng 470 lượt/video; cần 5,5–7 tập trở lên.
  - *Rủi ro:* top 5 chiếm 98 %.
- **E (loại).**
  - Chỉ 18/57 kênh đạt lọc không lộ mặt; video nổ ≥ 10 nghìn lượt chỉ 5 %; top 5 chiếm 100 %.
  - Trùng LL 27 %, tức là ăn vào khán giả của chính Last Lamplighters.

## 10 đề tài đầu của B
Thời lượng thắng: **12–20 phút**. Top 25 video nổ có trung vị 17 phút; trung vị 25,6 phút của cả ngách bị kéo lên bởi vài phim tài liệu trên 40 phút.
- **Nhãn cầu:**
  - **[Nổ-mẫu]:** cùng mẫu tiêu đề với video nổ trên 500 nghìn lượt trong 90 ngày;
  - **[Cầu-tìm]:** câu hỏi có nhiều video mới nhưng chưa video nào nổ (khoảng trống chất lượng);
  - **[Cầu-ngách]:** nổ vừa, khoảng 10–50 nghìn lượt.
- **Mẫu tiêu đề:** M1 "Why Only [N] [Countries/Companies] Can Still Build [X]" · M2 "How a Single [Store] Changes Its [Town]" · M3 "The (Overdue) Collapse of [Model]" · M4 "The Rise and Fall of [X]" · M5 "Why [X] (Usually) Fails in [Y]". Mẫu tiêu đề chỉ là khung; không chép tiêu đề.

| # | Đề tài (EN) | Nhãn cầu | Mẫu | Phút |
|---|---|---|---|---|
| 1 | Why Only Two Companies Can Still Build a Jet Airliner | Nổ-mẫu | M1 | 16–18 |
| 2 | How a Single Amazon Warehouse Changes Its Town | Nổ-mẫu | M2 | 14–16 |
| 3 | Why Only a Handful of Countries Can Make Advanced Chips | Nổ-mẫu | M1 | 16–18 |
| 4 | The Collapse of the American Shopping Mall | Nổ-mẫu | M3 | 15–18 |
| 5 | How Airlines Really Make Money (It's Not the Seats) | Cầu-ngách + CPM thẻ tín dụng | M5 biến thể | 14–17 |
| 6 | The Steel Box That Rewired World Trade | Nổ-mẫu (vận tải biển) | M4 | 16–20 |
| 7 | What Really Happened to Sears | Cầu-tìm | M4 | 17–20 |
| 8 | How a Single Dollar General Changes a Rural Town | Nổ-mẫu | M2 | 13–15 |
| 9 | Why American Retailers Usually Fail Abroad | Nổ-mẫu (chiều ngược) | M5 | 14–16 |
| 10 | Kodak Built the Digital Camera. Why Did It Lose? | Cầu-tìm, cung AI dày, chỉ đáng làm nếu vượt chất lượng | M4 | 15–18 |

**Giới hạn**
- Bộ lọc "không lộ mặt" chỉ đọc chữ, nên còn lọt vài kênh có người dẫn hoặc kênh đăng lại.
- Chỉ số c gần như không phân biệt giữa các ngách, vì chỉ đọc được tiêu đề và mô tả, không xem hình.
- Mức chỉ số sát ngưỡng ±5 %: không có. B hơn A 12,5 điểm.
