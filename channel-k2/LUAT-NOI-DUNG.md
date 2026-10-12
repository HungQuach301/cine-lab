# Luật nội dung (mốc 1, bước 4)

Áp cho kịch bản, hình, tiêu đề, thumbnail, mô tả, Shorts và phần trả lời bình luận. REVIEWER headless kiểm các luật này trước khi kịch bản được khoá.

## 1. Khẳng định về công ty thật
- **Mọi khẳng định về một công ty, tổ chức hay người thật đều có nguồn**: hồ sơ nộp cơ quan quản lý (SEC 10-K/20-F, hồ sơ phá sản), số liệu cơ quan nhà nước, báo cáo thường niên, hoặc báo chí có biên tập kèm ngày. Nguồn ghi trong `sources:` của đặc tả và hiện trên hình khi câu có số.
- Khẳng định về **hành vi sai trái** (vi phạm, gian lận, nguy hiểm) chỉ được nêu khi có **phán quyết, quyết định xử phạt hoặc thoả thuận công bố chính thức**. Nêu đúng tình trạng ("was fined by…", "settled without admitting…"). Cáo buộc chưa phân xử không làm trục tập.
- Không dùng logo, sản phẩm có nhãn hiệu hay giao diện thật trong cảnh 3D. Tên công ty xuất hiện bằng chữ trung tính.
- Tiêu đề và thumbnail không gán tính từ đạo đức cho công ty ("evil", "scam", "destroyed").

## 2. Sự kiện và nhận định
- **Sự kiện** là điều nguồn xác nhận. **Nhận định** là cách kênh diễn giải. Lời dẫn đánh dấu nhận định bằng từ rõ ràng: "our read is…", "one explanation is…", "economists disagree on…".
- Khi nguồn bất đồng, nêu cả hai, ghi nguồn từng bên.
- **Mô hình số liệu riêng** của kênh luôn gắn nhãn "our calculation", có giả định đi kèm, không trình bày như số chính thức.
- Đặc tả tập có khối `claims:` (đề xuất cho nhà máy): mỗi câu khẳng định về thực thể thật khai `type: fact | opinion | calc`, `src:` (bắt buộc với `fact`, `calc`).

## 3. Không suy đoán động cơ
- Không nói công ty hay người "muốn", "cố tình", "giấu", "lừa" nếu nguồn không ghi chính lời đó.
- Thay bằng cơ chế: "the incentive structure rewards…", "this fee structure means…".

## 4. Không persona chuyên gia tài chính
- Người dẫn là **giọng kể**, không tự giới thiệu là analyst, advisor, banker, economist hay bất kỳ nghề có chứng chỉ nào.
- Không dùng các câu "as a financial expert", "trust me", "I recommend".
- Tên kênh, mô tả kênh và giọng không gợi ý tư vấn tài chính. Giọng chọn **khác hẳn** giọng "crux-analyst-f1" của dự án Crux (xem `NHAN-DIEN.md`).

## 5. Đề tài tài chính–thanh toán
- **Chỉ giải thích cơ chế:** hệ thống, dòng tiền, phí, luật, lịch sử. Không bàn sản phẩm nào tốt hơn cho người xem, không nói nên mở/đóng thẻ, không bàn mua/bán cổ phiếu, không dự báo giá.
- **Câu miễn trừ ngắn**, nói ở 30 s đầu và ghi ở đầu mô tả:
  > "This video explains how the system works. It isn't financial advice."
- Đề tài **lai** có phần tài chính–thanh toán (ví dụ #6 hãng bay) cũng phải có câu miễn trừ.
- Số phí, lãi suất, ngưỡng pháp lý: chỉ từ văn bản luật/quy định (ví dụ Regulation II của Federal Reserve) hoặc hồ sơ công ty, ghi năm hiệu lực. Không nói "you will pay X".
- Không dùng biểu đồ giá cổ phiếu.
- Tiêu đề không hứa lợi ích tài chính cá nhân ("save money", "get rich", "the secret banks hide").

## 6. Quy trình sửa / gỡ khi bị chỉ ra sai
| Bước | Việc | Thời hạn (tính từ lúc kênh nhận được báo sai) |
|---|---|---|
| 1 | Ghi báo sai vào `channel-k2/SUA-LOI.md`: tập, mốc thời gian, nội dung báo, người báo (ẩn danh nếu là bình luận công khai) | Ngay khi đọc |
| 2 | Kiểm lại với nguồn gốc. Phân loại: **(a)** sai sự thật có thể gây hại cho công ty/người · **(b)** sai số không đổi kết luận · **(c)** không sai | Trong 48 giờ |
| 3a | Loại (a): **ẩn video ngay** (đặt riêng tư), sửa và đăng lại hoặc gỡ hẳn, ghim bình luận đính chính, sửa mô tả | Ẩn trong 24 giờ kể từ khi xác nhận |
| 3b | Loại (b): ghim bình luận đính chính, sửa mô tả (thêm mục "Corrections"). Nếu số sai nằm ở móc hoặc kết luận thì xử như (a) | Trong 72 giờ |
| 3c | Loại (c): trả lời kèm nguồn, giọng trung tính | Tuỳ chọn |
| 4 | Ghi bài học vào `SUA-LOI.md`, cập nhật luật kiểm nếu lỗi có thể bắt bằng máy | Trước tập kế tiếp |
- Yêu cầu pháp lý chính thức (thư luật sư, khiếu nại phỉ báng) chuyển **chủ dự án** ngay. Claude không trả lời thay.

## 7. Ranh giới với vùng Crux: nhà ở cá nhân và tài chính hộ gia đình (chủ dự án, 12/10/2026)
- **Không làm:** mua hay thuê nhà, thế chấp, giá nhà "có nên mua", chi phí sinh hoạt của một hộ, ngân sách cá nhân, so sánh sản phẩm tài chính cho người tiêu dùng. Đây là vùng của kênh Crux.
- **Được làm ở tầm thành phố:** luật xây dựng và zoning như cơ chế định hình thành phố; nguồn thu thuế của thành phố; chi phí hạ tầng trên mỗi người dân; nguồn cung nhà ở như số neo của cơ chế đô thị (Census ACS, giấy phép xây dựng).
- **Câu kiểm:** câu hỏi của tập trả lời được mà không cần nói người xem nên làm gì với nhà hay tiền của họ.
- **Tiêu đề, thumbnail** không dùng "afford", "buy a home", "your rent", "save".

## 8. Đề tài nhạy cảm của thành phố: zoning, đường cao tốc, khu dân cư theo chủng tộc (chủ dự án, 12/10/2026)
- **Chỉ nêu cơ chế, kèm nguồn chính thức hoặc học thuật:** văn bản luật hay quy định (bộ luật zoning, Federal-Aid Highway Act), hồ sơ cơ quan (FHWA, HUD, hồ sơ thành phố), bản đồ lưu trữ công (HOLC/NARA), nghiên cứu bình duyệt hoặc của cơ quan nghiên cứu nhà nước (CRS, GAO). Ghi năm và phạm vi của nguồn.
- **Không khung đảng phái:** không gắn chính sách với đảng hay chính khách đương thời làm trục; không dùng từ ngữ chiến dịch ("woke", "war on cars", "socialist", "MAGA"…). Khi nêu đánh giá chính sách, ghi **ai** đánh giá (LUAT-NOI-DUNG-G §6).
- **Không quy lỗi cho nhóm người:** chủ thể là cơ quan, văn bản, quyết định có tên và ngày ("the 1956 Act funded…", "the city council voted…"), không phải chủng tộc, tôn giáo, thế hệ hay cư dân một vùng. Hậu quả lên một cộng đồng được nêu bằng số và nguồn, không bằng tính từ đạo đức.
- **Tranh luận học thuật:** khi các nghiên cứu bất đồng (tác động của zoning lên giá, của đường cao tốc lên khu dân cư), nêu cả hai kèm nguồn (§2).
- **Hình:** không biếm hoạ người, không biểu tượng đảng phái; bản đồ lưu trữ dùng nguyên bản có dòng nguồn.
- **REVIEWER Opus** kiểm §8 ở mỗi bản lời T1.

## 9. Dùng `LUAT-NOI-DUNG-G.md` cho "huyền thoại vs hồ sơ" và "as of"
- `LUAT-NOI-DUNG-G.md` (chủ dự án duyệt ở G1 K2G-01, 11/10/2026, "dùng cho cả ngách B") áp cho mọi tập kênh 2:
  - §3 nhịp "huyền thoại vs hồ sơ" (1–3 nhịp/tập, có ghi lời đồn thấy ở đâu);
  - §5 "as of" cho sự kiện đang diễn ra;
  - §1–§2 không thuyết âm mưu, không gán động cơ cho nhóm.
- Cấu trúc ba tầng (§0) chỉ dùng cho tập T2 dạng "ba tầng". Tập T1 dùng cấu trúc 6 phần của `HIEN-CHUONG.md` §2.
- Hai luật khác nhau thì luật chặt hơn thắng.

## Ưu, nhược, tác động, rủi ro
- **Ưu:** luật cụ thể đến mức máy kiểm được một phần (`claims:` có `src:`, câu miễn trừ có trong lời, từ cấm trong tiêu đề). Quy trình sửa lỗi có thời hạn rõ.
- **Nhược:** viết kịch bản chậm hơn vì mỗi câu về công ty cần nguồn. Một số góc hấp dẫn (động cơ lãnh đạo) bị loại.
- **Tác động:** cần thêm trường `claims:` và kiểm câu miễn trừ vào nhà máy (gửi K khi mở; chưa sửa `checks/`).
- **Rủi ro:** luật không loại hết rủi ro phỉ báng vì cách diễn đạt vẫn có thể ngụ ý. Vì vậy REVIEWER headless đọc cả kịch bản, và chủ dự án duyệt trước khi đăng.

## Phép thử F1
- **Dùng chung lõi LL:** `sources:` đọc toàn văn, dòng nguồn tự sinh, "không lời khuyên tài chính hay nghề nghiệp cá nhân" (chuẩn LL §4).
- **Riêng gói kênh:** `claims:`, luật hành vi sai trái, câu miễn trừ T3, quy trình sửa/gỡ, `SUA-LOI.md`.
