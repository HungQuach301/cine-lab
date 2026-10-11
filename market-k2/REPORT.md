# Kênh 2: chọn ngách bằng YouTube Data API v3 (11/10/2026)

> **Vòng xác nhận B vs A (11/10/2026), xem mục cuối: KHÔNG xác nhận B. Kết quả là DỪNG.** Trên mẫu gộp, B − A = **+0,7 điểm**, KTC 90 % [−9,5; +12,7]. Hai điều kiện "≥ 5 điểm" và "cận dưới > 0" đều trượt, nên chưa soạn gói kênh `channel-k2/`. Kết luận "B thắng" ở vòng 1 không còn đứng.

**Kết luận vòng 1 (đã bị vòng xác nhận thay thế, xem banner):** chọn **B, lịch sử doanh nghiệp/ngành**, đi theo góc *cơ chế kinh tế của một ngành*. **A, lịch sử tiền/ngân hàng**, làm dự phòng. B đứng đầu ở cả 12 kịch bản độ nhạy (mỗi trọng số ±5 điểm). Dự phòng là A trong 11 kịch bản, và là D khi trọng số e giảm 5 điểm.
**Đang chờ chủ dự án:** xem mục cuối.

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
  - *Nhược:* các đề tài kể lại kiểu "Kodak/Blockbuster sụp đổ ra sao" hay "Nvidia lớn lên thế nào" đã ngập video AI làm hàng loạt, video đầu chỉ vài chục đến vài nghìn lượt xem. Cầu nằm ở góc *cơ chế ngành*: vì sao chỉ vài nước hay vài hãng làm được X, một cửa hàng thay đổi kinh tế địa phương ra sao, một mô hình kinh doanh sụp vì đâu.
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

---
## Vòng xác nhận: B vs A trên mẫu gộp (11/10/2026)

Mọi chỉ số là **tự tính, không phải chỉ số YouTube**.

**Quyết định: DỪNG.** B 64,9 · A 64,2 → **B − A = +0,7**. Bootstrap theo kênh (1 000 lần, seed 20261011): KTC 90 % **[−9,5; +12,7]**, P(B > A) = 54 %. Điều kiện cần là ≥ 5 điểm và cận dưới > 0; cả hai đều trượt. Không có chỉ số nào nằm trong ±5 % quanh ngưỡng: 0,7 cách xa 5, và −9,5 cách xa 0.
**Đang chờ chủ dự án:** chọn hướng tiếp theo (gợi ý ở cuối mục).

**Mẫu**
- **Mẫu mới:** 16 câu hỏi khán giả mới mỗi ngách, không trùng 8 câu cũ (`collect2.py`, `NEW_Q`). Tổng 32 search.list. Giữ nguyên bộ lọc cũ: video ≥ 8 phút, Haiku lọc kênh không lộ mặt, luật chọn kênh cũ. Mỗi ngách tối đa 30 kênh.
- **Mẫu cũ phải thu lại.** Số liệu thô vòng 1 ở ngoài git và đã mất cùng container cũ. Tôi chạy lại đúng 8 câu cũ, cùng mốc thời gian (NOW, cửa sổ 90 ngày), cùng luật chọn ≤ 15 kênh. Tốn thêm 16 search.list. Haiku phân loại lại nên tập kênh không chắc trùng 100 %.
  - *Điểm tổng tái lập khớp:* A 60,8 (vòng 1: 61,1), B 73,3 (vòng 1: 73,6).
  - *Thành phần của B lệch:* kênh trẻ có nổ 4/7 (vòng 1: 4/5); top 5 chiếm 59 % (71 %); số tập phân vị 75 là 0,7 (2,3); tài trợ 31 % (28 %); thời sự 7,5 % (8 %). Các lệch bù trừ nhau nên điểm tổng gần như không đổi.
- **Mẫu gộp:** A có 42 kênh (15 cũ + 30 mới, trùng 3); B có 45 kênh (15 + 30, trùng 0).
- **Kênh trẻ (< 2 năm) đạt lọc:** A 22, B 26. Cả hai đều vượt mục tiêu ≥ 12 mỗi ngách.
- **Chuẩn hoá:** vẫn trên 6 ngách. D, E, J, L giữ đầu vào vòng 1, lấy từ bảng trên. Kiểm mốc: tính lại từ bảng, lệch ≤ 0,2 điểm do làm tròn.
- **Quota và chi phí:** 49 search.list (32 mới + 16 thu lại + 1 lượt thử kết nối) và 282 lệnh đọc khác, khoảng 5 200 đơn vị. Haiku phân loại/chấm nhãn $0,17, reviewer headless $0,04; tổng ≈ $0,21 (trần $2).

| Mẫu gộp | A Tiền/NH | B Doanh nghiệp |
|---|---|---|
| a. Nổ ≥ 10 nghìn (gốc) / cờ thời sự | 12 % (21 %) / 20 % | 18 % (24 %) / 18 % |
| b. Kênh trẻ có nổ / top 5 chiếm | 12/22 / 77 % | 16/26 / 49 % |
| c. Top 10 thiếu dữ liệu thật + hình công phu | 100 % | 100 % |
| d. Trung vị phút video nổ | 20,7 | 25,4 |
| d. Số tập tới 4 000 h, kênh trẻ **phân vị 75** | 4,2–5,5 | 1,8–2,3 |
| d. Số tập tới 4 000 h, kênh trẻ **trung vị** | 39–50 | 13–17 |
| e. Video nổ có tài trợ/affiliate | 26 % | 15 % |
| f. Trùng Crux / trùng LL / kênh trẻ ra hàng loạt | 19 / 2 / 33 % | 7 / 0 / 36 % |
| Điểm thành phần e·d·(a+c)·nhà máy·b·f | 10·6,5·7,1·7·4,5·3,1 | 6,5·8,2·8,7·6·7,7·1,8 |
| **Tổng /100** | **64,2** (KTC 90 % 53,6–71,1) | **64,9** (58,1–70,1) |

- **d chỉ dùng để xếp hạng.** Số tập không phải dự báo. Ở mức trung vị, một kênh trẻ điển hình cần 13–17 tập (B) hoặc 39–50 tập (A) mới tới 4 000 giờ. Vòng 1 không báo con số này; điểm d vẫn dùng phân vị 75 như vòng 1.
- **Tách theo mẫu** (`analyze2.py`, trường `split`): mẫu cũ cho A 60,8, B 73,3. Mẫu mới riêng cho **A 64,6, B 60,0**. Lợi thế của B ở vòng 1 không lặp lại trên câu hỏi mới. Các khác biệt thành phần quan sát được dưới đây là *giả thuyết giải thích*: chưa phân rã và chưa có khoảng tin cậy cho từng mẫu con.
  - Tỷ lệ video nổ có tài trợ của B giảm từ 31 % xuống 4 %, còn của A tăng từ 5 % lên 34 %. Chỉ số e có trọng số 25.
  - Cờ thời sự của B tăng từ 7,5 % lên 25 %.
  - Số tập theo phân vị 75 của A tăng từ 1,4 lên 5,1 (tệ đi).
  Trên mẫu gộp, B vẫn hơn ở độ tập trung (top 5 chiếm 49 % so với 77 %) và ở số tập theo trung vị.
- **Độ nhạy (mỗi trọng số ±5 điểm, trường `sens_AB` tính theo dấu B − A):** B − A dao động từ −1,0 đến +2,4. B dẫn trong 7/12 kịch bản, A dẫn trong 4/12, hoà 1/12. Thứ hạng giữa hai ngách phụ thuộc vào trọng số, nghĩa là hai ngách ngang nhau.

**Giới hạn**
- Bộ lọc Haiku cho qua 81–93 % số kênh ứng viên, nhiều hơn hẳn vòng 1 ở ngách E (32 %). Mẫu B có lọt kênh ngoài ngành hoặc có lộ mặt, ví dụ kênh lịch sử ru ngủ, kênh đá quý có người dẫn, kênh tiếng Anh nhắm khán giả Nam Á. Tôi giữ nguyên bộ lọc theo yêu cầu và không sửa tay.
- Câu hỏi mới là do tôi viết. Vài câu bám thời sự (Boeing, SVB) làm tăng cờ thời sự ở cả hai ngách.
- Bootstrap chỉ lấy mẫu lại kênh. Khoảng tin cậy chưa tính ba nguồn bất định: chọn câu hỏi tìm kiếm, nhiễu nhãn Haiku, và đầu vào cố định của D/E/J/L. Khoảng thật vì vậy còn rộng hơn.
- **Độ phủ nhãn** đã kiểm bằng assert trong mã: thời sự 161/161 (A) và 233/233 (B); khoảng trống 80/80; trùng khán giả đủ mọi kênh; phân loại kênh 99 %. Không có video nào trong 80 video dẫn đầu được chấm "có dữ liệu thật + hình công phu", nên chỉ số c bằng 1,0 trong mọi lần bootstrap.
- Số liệu thô (kể cả `metrics_v2.json`) tự xoá khi chạy lại mã sau 30 ngày. Không có lịch xoá tự động khi mã không chạy.

**Hướng tiếp theo, chờ chủ dự án chọn**
1. **Chọn B theo lý do định tính.** B có độ tập trung thấp, kênh trẻ trung vị cần ít tập hơn, và không trùng khán giả LL hay Crux. *Ưu:* đi tiếp ngay. *Nhược:* dữ liệu không chứng minh B hơn A. *Rủi ro:* tài trợ ít hơn dự kiến, kèm rủi ro phỉ báng.
2. **Chọn A.** *Ưu:* CPM và tài trợ cao. *Nhược:* top 5 chiếm 77 %; kênh trẻ trung vị cần 39–50 tập. *Rủi ro:* YMYL, trùng Crux 19 %.
3. **Thêm một vòng đo** với câu hỏi do chủ dự án chọn, kèm lọc kênh bằng ảnh thumbnail. *Ưu:* giảm sai lệch do câu hỏi và bộ lọc. *Nhược:* thêm khoảng 3 200 đơn vị quota và một vòng làm việc. *Rủi ro:* kết quả có thể vẫn ngang nhau, vì hai ngách có lẽ thật sự tương đương.

**Reviewer headless (Haiku, $0,04).** Soát 7 luật dữ liệu. Lần đầu có 4 mục FAIL, đã sửa hết:
- Số tách mẫu và độ nhạy trước đó không truy được về mã; nay `analyze2.py` sinh ra chúng.
- Đã ghi rõ thành phần mẫu cũ thu lại lệch so với vòng 1.
- Đã sửa câu vòng 1 hàm ý "Nvidia sụp đổ".
- Cache nhãn Haiku và phân loại kênh nay báo lỗi khi rỗng hoặc thiếu; lỗi playlist dừng hẳn, không ghi dở dang. Danh sách tự xoá đã gồm cả file vòng này.

Phần soát phỉ báng trong hàng đợi đề tài không áp dụng, vì bước 4 không chạy.
