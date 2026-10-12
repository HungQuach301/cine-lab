# Luật chọn đề tài (mốc 1, bước 2)

Một đề tài chỉ vào `HANG-DOI.md` khi **đủ cả 5 điều kiện**. Mỗi điều kiện có phép đo hoặc phép kiểm cụ thể. Thiếu một điều kiện thì đề tài ở lại danh sách chờ, kèm lý do.
Mọi chỉ số trong luật này là **tự tính, không phải chỉ số YouTube**.

## Năm điều kiện
| # | Điều kiện | Phép đo / phép kiểm | Ngưỡng vào hàng đợi | Người kiểm |
|---|---|---|---|---|
| 1 | **Có cầu** | Nhãn cầu theo định nghĩa `market-k2/REPORT.md`: **[Nổ-mẫu]** cùng mẫu tiêu đề với video ≥ 500 nghìn lượt trong 90 ngày; **[Cầu-ngách]** video dài 10–50 nghìn lượt trong 90 ngày (bổ sung: tới 100 nghìn ghi rõ số); **[Cầu-tìm]** nhiều video mới nhưng chưa video nào nổ. Bổ sung 11/10: **[Cầu-bền]** top 5 video dài **toàn thời gian** theo độ liên quan (search.list không giới hạn ngày) có ≥ 1 video ≥ 500 nghìn lượt; hồ sơ cầu ở mốc 2 ghi thêm số bình luận câu hỏi/yêu cầu | Nổ-mẫu, Cầu-ngách, hoặc Cầu-bền. **Cầu-tìm đơn độc không đủ**: phải kèm Cầu-bền từ hồ sơ cầu | Mã (`collect.py`), ghi nhãn kèm số |
| 2 | **Có khoảng trống** | Top 5 video theo câu hỏi chính: Haiku đọc tiêu đề + mô tả, đếm video có dấu hiệu dùng số liệu thật có nguồn. Ở mốc 2 đọc thêm bình luận phản bác/chỉnh sai | ≤ 1/5 video đầu có dấu hiệu số liệu thật, **hoặc** bình luận chỉnh sai chỉ ra lỗi lặp lại | Mã + người soạn hồ sơ |
| 3 | **Có số liệu nguồn công khai** | Liệt kê ≥ 3 số neo, mỗi số ghi **loại nguồn** công khai đọc được toàn văn: BTS, Census (CBP, Monthly Retail Trade), BLS (QCEW, OES), SEC filings (10-K, 20-F), Federal Reserve (Payments Study, Regulation II), BIS/CPMI, UNCTAD, WTO, FAA/ICAO, báo cáo thường niên công ty, hiệp hội ngành có phương pháp công khai. Không Wikipedia làm nguồn số | ≥ 3 số neo có loại nguồn công khai xác định trước khi viết kịch bản | Người soạn hồ sơ; P duyệt |
| 4 | **Dựng được 3D** | Có ít nhất một cỗ máy hình 3D trung tâm theo trụ (`TRU-NOI-DUNG.md`) dựng được bằng bộ đồ nghề `design/ll-hero/kit.js` hoặc phần mở rộng trong gói kênh, không cần mặt người, logo hay sản phẩm có nhãn hiệu | ≥ 1 cảnh 3D trung tâm + ≥ 2 cảnh phụ mô tả được bằng khối giản lược | Người soạn hồ sơ |
| 5 | **Rủi ro pháp lý thấp** | Câu hỏi trung tâm là **cơ chế của ngành**, không phải **lỗi, tội hay động cơ của một công ty hoặc một người cụ thể**. Không đề tài đang có vụ kiện là trục chính. Tên công ty chỉ xuất hiện như ví dụ có nguồn | Câu hỏi mở đầu trả lời được mà không cần quy lỗi cho ai | Người soạn + REVIEWER headless |

## Luật phụ
- **Tỷ lệ trụ** (định vị 12/10/2026, `TRU-NOI-DUNG.md`) trong 12 đề tài kế tiếp: T1 thành phố ≈ 60 %, T2 ngành ≈ 25 %, T3 mô hình kiếm tiền ≈ 15 %. Lệch quá ±1 đề tài thì ghi lý do. Sau 2 tập thí điểm, áp luật ở `THI-DIEM.md` (trụ thắng ≥ 2/3 hàng đợi 6 tập kế). *Tỷ lệ 11/10 (T1–T4, tài chính ≈ 25 %) hết hiệu lực.*
- **Điều kiện 5 thêm** (12/10): đề tài không thuộc vùng Crux (`LUAT-NOI-DUNG.md` §7). Đề tài chạm zoning, đường cao tốc hay khu dân cư phải nêu trước nguồn chính thức/học thuật sẽ dùng (§8).
- **Không hai tập liền cùng trụ** trong 6 tập đầu, để đo được trụ nào kéo người xem.
- **Cờ thời sự** (nới 12/10/2026, `QUAN-TRI-RUI-RO.md`): đề tài mà cầu chủ yếu đến từ tin tức dưới 90 ngày **được vào hàng đợi**. Mức XANH nếu có mốc "as of <ngày>"; VÀNG nếu tin sát chính trị hay địa chính trị. Vẫn ưu tiên đề tài sống lâu, và không quá 2 tập VÀNG liền nhau. Tai nạn có người chết hay vụ việc đang điều tra quy trách nhiệm cá nhân vẫn không làm trục tập (vùng phỉ báng).
- **Mức rủi ro:** mỗi đề tài trong `HANG-DOI.md` ghi mức XANH/VÀNG/ĐỎ theo `QUAN-TRI-RUI-RO.md` §7; ĐỎ không vào hàng đợi.
- **Đề tài tài chính–thanh toán** thêm 2 kiểm: (a) câu hỏi là "hệ thống vận hành thế nào", không phải "bạn nên làm gì"; (b) không cần số liệu lợi suất, giá cổ phiếu hay so sánh sản phẩm cho người tiêu dùng.
- **Loại bỏ từ danh sách market-k2:** "What Really Happened to Sears" và "Kodak Built the Digital Camera. Why Did It Lose?" trượt điều kiện 5, vì câu hỏi trung tâm là quyết định của ban lãnh đạo một công ty cụ thể (có người còn sống). Kodak còn trượt điều kiện 2 (market-k2 ghi cung video mới dày, video đầu ít lượt xem).

## Ưu, nhược, tác động, rủi ro
- **Ưu:** mỗi điều kiện có phép đo, nên P hoặc phiên khác áp được mà không cần đoán ý. Điều kiện 5 chặn rủi ro phỉ báng ngay ở khâu chọn, rẻ hơn sửa ở khâu kịch bản.
- **Nhược:** điều kiện 2 chỉ đọc chữ (tiêu đề, mô tả, bình luận), không xem hình đối thủ. Điều kiện 1 cần quota search.list (100 đơn vị/lượt) cho mỗi đề tài mới.
- **Tác động:** loại 2/10 đề tài market-k2. Thêm nhãn Cầu-bền cho đề tài có cung mới dày nhưng cầu cũ lớn.
- **Rủi ro:** ngưỡng "≤ 1/5 có số liệu thật" có thể quá dễ, vì market-k2 thấy 100 % top 10 thiếu dữ liệu thật ở mọi ngách. Đề xuất: sau 6 tập, so điều kiện 2 với giữ chân thực tế và siết ngưỡng nếu cần.

## Phép thử F1
- **Dùng chung lõi LL:** luật nguồn của `ll.py` (chặn Wikipedia, bắt đọc toàn văn, tách actual/projection) dùng thẳng cho điều kiện 3.
- **Riêng gói kênh:** điều kiện 1 (nhãn cầu, `channel-k2/collect.py`), điều kiện 5 (pháp lý), tỷ lệ trụ.
