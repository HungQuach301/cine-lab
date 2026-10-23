# PHIẾU CHỌN LOOK — K2C-T4-02 London (LOOK-T4, mốc M1b, 23/10/2026)

> Chủ dự án chấm mù. Phiên này **không** tự chấm mù bằng AI và không chọn hộ. Khoá giải mã `khoa.json` — chỉ mở sau khi chọn xong.

## 1. Cách chọn
1. Mở `reports/look-t4/to-chon-mu.jpg` (8 hàng × 3 cột X/Y/Z; thứ tự cột đã xáo theo từng hàng). Xem kỹ từng ô ở 1080p: `reports/look-t4/khung/<hàng>-<X|Y|Z>.jpg`.
2. Mỗi hàng chọn **một cột**, hoặc ghi **"không cột nào đạt"** (kèm một dòng lý do). Có thể chọn cột khác nhau giữa các hàng — phiên sau sẽ đề xuất một look hợp nhất nếu các lựa chọn lệch nhau.
3. **Sau khi đã chọn**, xem 4 clip 8 s (biến thể A cho mọi mốc theo lệnh — xem trước sẽ lộ một cột; thời gian chạy trong khung, cú máy theo §19 đề xuất): `reports/look-t4/clip/clip-M1-A.mp4` … `clip-M4-A.mp4` — đánh giá chuyển động, không dùng để chọn cột.

| Hàng | Khung | Chọn (X / Y / Z / không đạt) | Ghi chú |
|---|---|---|---|
| 1 | M1-rong — 1666 trước cháy, toàn cảnh Bankside | | |
| 2 | M1-trung — 1666, tháp St Saviour (cầu London có nhà) | | |
| 3 | M2-ngay — 3/9/1666 15:00, ngày khói | | |
| 4 | M2-dem — 2/9/1666 23:00, đêm lửa từ giữa sông | | |
| 5 | M3-rong — 29/12/1940 21:30, toàn cảnh Bankside | | |
| 6 | M3-trung — 29/12/1940 22:30, mái vòm từ Fleet Street | | |
| 7 | M4-rong — 2026 ngày, chân trời City | | |
| 8 | M4-trung — 2026 ngày, mái vòm từ Fleet Street (gần mặt phố) | | |

## 2. Câu hỏi kèm (trả lời ngắn)
- Q1. Thành phố còn **"đồ chơi"** không? (Hàng nào, chỗ nào: mái/tường, mật độ, khoảng trống, cây, thuyền.)
- Q2. **Khói/lửa** đọc rõ không? (Ngày khói 3/9: cột khói theo gió đông; đêm 2/9: mặt tiền cháy + phản chiếu sông; 1940: các đám cháy rời quanh mái vòm.)
- Q3. **Nhận ra London** không — tắt tiếng vẫn hiểu là London? (Sông, cầu, Old St Paul's / mái vòm, cụm tháp.)
- Q4. (tuỳ chọn) Khung nào nên làm mẫu chuẩn cho §14.7 "Look T4"?

## 3. Quyết định đề xuất
| # | Quyết định | Phương án | Ưu | Nhược | Tác động | Rủi ro | Khuyến nghị |
|---|---|---|---|---|---|---|---|
| L1 | Look T4 | theo kết quả chọn mù §1 | chủ dự án chấm hình cuối | — | khoá look trước animatic (bài học T3 số 1) | thấp | chọn theo tờ mù |
| L2 | Ngưỡng bão hoà trung vị ≥ 0,40 (BIBLE §14.4) với London | (a) giữ ngưỡng → đẩy màu (trời xanh đậm, nước xanh, ngói bão hoà, bỏ sương) · (b) ngưỡng theo tập: lấy trung vị của khung chủ dự án chọn làm mốc, giữ ΔE shot kề · (c) đo chỉ vùng thành phố (bỏ trời/nước/khói) | (b) giữ đúng không khí London (sương, khói than, trời xám) mà vẫn có số để giữ liền mạch | (a) dễ thành "đồ chơi", trái căn cứ không khí (Evelyn, *Fumifugium* 1661) · (b) đổi luật kênh | màu cả tập | vừa | **(b)**; nếu giữ (a): không ô ngày nào đạt (cao nhất 0,37 — báo cáo §3), phải đẩy màu ở bước sản xuất |
| L3 | Người / xe / thuyền nhỏ ở cận | (a) thêm ở sản xuất cho khung ≤ 60 m (người theo tranh Hollar/Luyken bậc 4, mật độ theo Pepys/Evelyn bậc 2) · (b) bỏ, chỉ thuyền | (a) phố sống, đúng §11.2 "sự sống" | thêm giờ dựng, cần nguồn trang phục | khung trung/cận | vừa | **(a)** cho khung trung, thuyền giữ như look |
| L4 | Thành phố 1940 | (a) khối Victoria–Edward thay nhà 1667 trên cùng lô (bậc 5, như look) · (b) thêm toà có tên còn lại (OSM start_date < 1940, bậc 1) — đã có trong look | (a)+(b) City 1940 dày như ảnh thời đó | (a) là ước lượng hình khối | H3–H4 | vừa | **(a)+(b)**, ghi "ước lượng" trong thẻ phương pháp |
| L5 | Lửa đêm cận (D5) | (a) giữ cách A cho cảnh rộng + Cycles GPU 3–4 cận đêm · (b) chỉ cách A | xem báo cáo §2 (đêm 2/9 từ sông đọc được bằng cách A) | (a) thêm ≈ $5–8 GPU | H1-13, H4-04 | thấp | **(a)** như G1 |
| L6 | "Estimated infill" (BIBLE §11.4) cho lõi khối 1666 | (a) tông hơi khác + dòng chú thích như luật · (b) chỉ ghi trong thẻ phương pháp + bản đồ % diện tích lấp | (b) không lộ "mảng màu lạ" trên toàn cảnh | (b) lệch chữ luật §11.4 | toàn cảnh 1666 | vừa | **(b)** — xin chủ dự án duyệt ngoại lệ cho T4 |

## 4. Việc chờ chủ dự án
- Chọn mù 8 hàng (§1) + trả lời Q1–Q3.
- Quyết định L2–L6.
- Sau khi chọn: phiên P ghi look vào `LOOK-KHOA.md` T4 + Kinh thánh §14.7 (T4), chép nguồn mới (`channel-k2/k2c-t4-02/look/van-cc0.json`, `licenses/met-3360*.json`, `met-757299.json`) vào `RIGHTS.md`.
