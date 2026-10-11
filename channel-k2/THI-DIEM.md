# Đề xuất tập thí điểm và mục tiêu đo 7 ngày (mốc 2)

> Đề xuất, chờ chủ dự án duyệt. **Chưa dựng tập.**
> Số ở mục 1 và phần "Cơ sở của các con số" là **tự tính, không phải chỉ số YouTube**. Chỉ các mục tiêu trong bảng mục 2 là chỉ số YouTube Studio.

## 0. Cập nhật sau "Cầu hiện hành" (11/10/2026), thay mục 1
Số đo là **tự tính, không phải chỉ số YouTube** (`current.py`, xem `HANG-DOI.md`).
- **Container không còn hợp lệ làm thí điểm** theo chuẩn chính: trong 90 ngày, 0 video ≥ 50 nghìn lượt đúng đề tài (nhãn "Không").
- **Luật quyết định ra nhánh 3–5/12 (5/12 Mạnh).** Nhánh này **không quy định cách chọn thí điểm**; chỉ nhánh ≥ 6/12 nói "đề tài Mạnh có điểm cao nhất". Vì vậy dưới đây là **đề xuất** dùng cùng công thức điểm. Chủ dự án quyết.
- **Công thức điểm:** số video ≥ 50 nghìn đúng đề tài × hợp 3D (1–3) × rủi ro pháp lý thấp (1–3). Hai thang định tính đặt trong `current.py` trước khi có số.

| Đề tài Mạnh | Video ≥ 50 nghìn đúng đề tài | Hợp 3D | Pháp lý thấp | **Điểm** | Điểm ở chuẩn rộng |
|---|---|---|---|---|---|
| **Factory town** ("How a Single Factory Holds Up a Small Town") | 3 | 3 | 3 | **27** | 27 |
| Malls | 4 | 2 | 3 | 24 | **48** |
| Jet airliner | 2 | 3 | 2 | 12 | 18 |
| Chips | 2 | 3 | 2 | 12 | 36 |
| Retailers abroad | 3 | 1 | 2 | 6 | 6 |

- **Đề xuất thí điểm: factory town** (điểm cao nhất ở chuẩn chính); **phương án thay: malls** (cao nhất ở chuẩn rộng).
  - *Ưu:* cầu hiện hành có ở 3 kênh khác nhau; pháp lý thấp vì không xoay quanh một công ty; dùng bộ cảnh thị trấn sa bàn và nhà máy (lõi `kit.js`).
  - *Nhược:* một video 1,10 triệu (RocaNews) chiếm phần lớn cầu; **chưa có hồ sơ cầu** (bình luận, số neo).
  - *Tác động:* trước kịch bản phải có `de-tai/factory-town.md` (khoảng 6 search.list + 50 bình luận/video). Mục tiêu 7 ngày ở mục 2 giữ nguyên ngưỡng; thời lượng đổi sang khung thắng của đề tài, sẽ đo ở hồ sơ.
  - *Rủi ro:* chọn thí điểm theo cầu 90 ngày có thể thiên về mảng đang nóng tạm thời; malls có 3/4 video đúng đề tài từ kênh trẻ, dấu hiệu mảng đang đông dần.

## 1. (Vòng 1, **thay bằng mục 0**) Chọn tập thí điểm: **#1 "The Steel Box That Rewired World Trade"** (16–18 phút)
| | Container (#1) | Jet airliner (#2) | Card networks (#3) |
|---|---|---|---|
| Cầu toàn thời gian (video đầu) | **4,83 triệu**; 4/12 ≥ 500 nghìn | 3,85 triệu; 4/8 ≥ 500 nghìn | 1,04 triệu; 1/7 ≥ 500 nghìn |
| Cầu năm 2026 (video mới cao nhất) | 329 | **565 nghìn** | 363 |
| Bình luận được dùng / phản bác | 150 / 55 | 116 / 87 | 44 / 23 |
| Rủi ro pháp lý | **Thấp** | Trung bình (dễ trượt sang lỗi một hãng) | Trung bình–cao (YMYL, có thể có tranh chấp pháp lý, cần kiểm) |
| Độ hợp 3D | **Cao nhất** (cảng, tàu, cẩu, bản đồ tuyến) | Cao (xưởng lắp ráp) | Trung bình (đường ống tiền là hình trừu tượng) |
| Bộ cảnh dùng lại cho tập sau | Cảng → #9 thị trấn nhà máy, bản đồ tuyến → #5, #12 | Xưởng → #5 chip | Đường ống → #10, #6 |

- **Ưu:** cầu bền lớn nhất; rủi ro thấp nhất cho tập đầu, khi quy trình soát pháp lý chưa chạy thật lần nào; bộ cảnh dùng lại nhiều; cung mới yếu (video 2026 cao nhất 329).
- **Nhược:**
  - Cầu chủ yếu ở video cũ, nên YouTube có thể ưu tiên đề xuất video cũ đã có tín hiệu.
  - Jet có cầu "nóng" hơn năm 2026.
- **Tác động:** tập đầu buộc dựng bộ cảnh cảng–tàu–cẩu và bản đồ tuyến, rồi đo thời gian dựng SwiftShader với cảnh nhiều container (`InstancedMesh`).
- **Rủi ro:** khán giả trong ngành bắt lỗi thuật ngữ (nhóm hoàn cảnh lớn nhất). Giảm bằng đọc soát kỹ thuật và hiện cả hai hệ đơn vị.
- **Phương án thay:** jet airliner, nếu chủ dự án ưu tiên cầu năm 2026 hơn rủi ro pháp lý.

## 2. Mục tiêu đo 7 ngày đầu (số YouTube Studio)
Bốn chỉ số dưới đây **là chỉ số YouTube Studio** (số đo thật sau khi đăng), khác các chỉ số tự tính trong hồ sơ.

| Chỉ số (Studio, ngày 1–7) | **Mục tiêu** | **Sàn** (dưới sàn thì đổi) | Việc khi dưới sàn |
|---|---|---|---|
| **CTR hiển thị** (impressions click-through rate) | **≥ 4,0 %** | 2,5 % | Đổi thumbnail trước, tiêu đề sau, mỗi lần một biến; đo lại sau 48 giờ |
| **Giữ chân:** tỷ lệ xem trung bình (average percentage viewed) | **≥ 35 %** (≈ 6 phút trên tập 17 phút) | 25 % | Xem đường giữ chân; nếu rơi > 30 % trong 0:30 đầu thì sửa móc ở tập sau |
| **Giữ chân ở 0:30** | **≥ 70 %** | 55 % | Như trên |
| **Lượt xem/ngày** (trung bình ngày 1–7) | **≥ 140** (≈ 1 000 lượt/7 ngày) | 30 (≈ 210 lượt/7 ngày) | Không đổi đề tài vì một tập. Ghi nguồn lưu lượng (search, browse, suggested) để so tập 2 |

**Cơ sở của các con số (giả định, chưa phải dự báo):**
- **Tỷ lệ xem 35 %** là cận dưới của giả định 35–45 % dùng trong market-k2 cho chỉ số d.
- **Lượt xem:** market-k2 vòng xác nhận cho thấy một kênh trẻ trung vị của B cần 13–17 tập để tới 4 000 giờ, tức khoảng 235–310 giờ mỗi tập.
  - Ở 17 phút × 35–45 %, mỗi lượt xem đóng góp khoảng 6–7,7 phút.
  - Vậy một tập của kênh trẻ trung vị đạt khoảng **1 800–3 100 lượt suốt đời**.
  - Mục tiêu 1 000 lượt trong 7 ngày nghĩa là khoảng 1/3–1/2 con số đó ngay tuần đầu: mức "kênh mới làm tốt", không phải mức trung bình.
  - **Sàn 210 lượt** là mức mà dưới đó tập không đóng góp đáng kể vào 4 000 giờ.
- **CTR 4,0 %:** trang trợ giúp YouTube nói phần lớn kênh có CTR hiển thị trong khoảng 2–10 %. *Tôi chưa trích nguyên văn ở phiên này; cần kiểm lại.* Chọn mức giữa dưới của khoảng vì kênh mới chưa có người đăng ký *(giả định, chưa kiểm)*.
- **Giới hạn:** các số trên dựa trên mẫu kênh do search chọn ra (đã sống sót), nên **lạc quan**, đúng như market-k2 đã cảnh báo. Một tập không đủ để kết luận về kênh. Kết luận cần ít nhất 3 tập ở 3 trụ khác nhau.

## Phép thử F1
- **Dùng chung lõi LL:** quy trình đăng và đo sau đăng của LL (`HUONG-DAN-DANG-TAP*.md`), `thumb.py` + kiểm Q12.
- **Riêng gói kênh:** ngưỡng mục tiêu/sàn ở trên, bảng so trụ sau 6 tập.
