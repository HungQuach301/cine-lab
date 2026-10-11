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

## Ưu, nhược, tác động, rủi ro
- **Ưu:** luật cụ thể đến mức máy kiểm được một phần (`claims:` có `src:`, câu miễn trừ có trong lời, từ cấm trong tiêu đề). Quy trình sửa lỗi có thời hạn rõ.
- **Nhược:** viết kịch bản chậm hơn vì mỗi câu về công ty cần nguồn. Một số góc hấp dẫn (động cơ lãnh đạo) bị loại.
- **Tác động:** cần thêm trường `claims:` và kiểm câu miễn trừ vào nhà máy (gửi K khi mở; chưa sửa `checks/`).
- **Rủi ro:** luật không loại hết rủi ro phỉ báng vì cách diễn đạt vẫn có thể ngụ ý. Vì vậy REVIEWER headless đọc cả kịch bản, và chủ dự án duyệt trước khi đăng.

## Phép thử F1
- **Dùng chung lõi LL:** `sources:` đọc toàn văn, dòng nguồn tự sinh, "không lời khuyên tài chính hay nghề nghiệp cá nhân" (chuẩn LL §4).
- **Riêng gói kênh:** `claims:`, luật hành vi sai trái, câu miễn trừ T3, quy trình sửa/gỡ, `SUA-LOI.md`.
