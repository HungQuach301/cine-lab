# Hiệu chuẩn thước cầu bằng Last Lamplighters (12/10/2026)

Mọi chỉ số là **tự tính, không phải chỉ số YouTube**. Lượt xem LL là số công khai của kênh mình, đọc bằng `videos.list`. Mã: `calib.py`. Cách làm học theo `crux-lab/market/CALIBRATION.md`: nhãn hồi tố, so với lượt xem 28 ngày, và chỉ sửa cách tính khi đủ mẫu.

## Phương pháp
- **Kênh:** `@lastlamplighters` (`UCeOPI-1MkTwFFhUw63EaaZg`), lấy bằng `channels.list forHandle`. Danh sách video lấy từ uploads, không đoán ID.
- **Nhãn cầu hồi tố:** dùng đúng thước cầu hiện hành, hàm `current.search_topic` và `current.relevance`:
  - video ≥ 8 phút, đăng trong 90 ngày, khán giả US;
  - Sonnet 5.5 chấm "đối thủ trực tiếp" trên các video ≥ 50 nghìn lượt;
  - ≥ 2 video → Mạnh, 1 → Yếu, 0 → Không.
  - Mỗi đề tài chỉ dùng **3 câu**, trong khi current.py dùng 6. Nhãn vì vậy có thể thấp hơn một bậc so với thước đầy đủ.
- **Quota:** 24 search.list + 19 lệnh đọc, khoảng 2 420 đơn vị. Tìm kênh tối 11/10 tốn thêm 5 đơn vị.

## Kết quả
| Tập | Đề tài | Nhãn cầu (hồi tố 12/10) | Video ≥ 50 nghìn (thô → đúng đề tài) | Trung vị phút: video dài / video đúng đề tài | Video LL trên kênh | Lượt xem / ngày từ khi đăng |
|---|---|---|---|---|---|---|
| 1 | Lamplighters, nghề bị thay | Không | 9 → 0 | 14,3 / – | 10,1 phút, 5 lượt, 5,6 ngày | 0,9 |
| 2 | Tổng đài viên điện thoại | Không | 0 → 0 | 15,5 / – | chưa đăng | – |
| 3 | ATM và giao dịch viên | Không | 0 → 0 | 12,1 / – | chưa đăng | – |
| 4 | Máy chữ và phụ nữ | Không | 1 → 0 | 20,3 / – | chưa đăng | – |
| 5 | Giám định bảo hiểm | Không | 2 → 0 | 30,1 / – | chưa đăng | – |
| 6 | Thợ sắp chữ → nhà thiết kế → AI | **Yếu** | 1 → 1 | 12,4 / **13,9** | 8,6 phút, 206 lượt, 4,3 ngày | **48,2** |
| 7 | Người làm "computer" | Không | 3 → 0 | 20,4 / – | 10,3 phút, 11 lượt, 2,8 ngày | 3,9 |
| 8 | Phiên dịch, biên dịch | Không | 0 → 0 | 15,7 / – | 10,1 phút, 6 lượt, 2,0 ngày | 3,0 |

- **Tương quan hạng** (Spearman, nhãn so với lượt xem/ngày): **ρ = 0,77, n = 4 — mẫu rất nhỏ.**
  - Ba trong bốn tập có cùng nhãn Không, nên ρ chỉ phản ánh **một** quan sát: đề tài duy nhất có cầu (Yếu, tập 6) cũng là tập có lượt xem/ngày cao gấp hơn 10 lần các tập còn lại.
  - Đây là dấu hiệu cùng chiều, **không** phải bằng chứng thống kê.
- **Độ dài:**
  - Video dài cùng đề tài trong 90 ngày có trung vị 12–30 phút, còn LL khoảng 10 phút.
  - Video đúng đề tài duy nhất ≥ 50 nghìn lượt (tập 6) dài 13,9 phút.
  - Thị trường các đề tài LL nghiêng về video dài hơn LL 2–20 phút. Riêng tập 6, đề tài có cầu, chỉ lệch khoảng 4 phút.
- **Giới hạn:**
  - Kênh mới có 4 tập dài, không phải 8. Tập 2–5 chưa có trên kênh lúc đo.
  - Các tập đăng 2–6 ngày trước, chưa tới mốc 28 ngày.
  - Lượt xem/ngày của kênh mới phụ thuộc nhiều vào tiêu đề, thumbnail và Shorts. Tập 6 có Short cùng tiêu đề (31 lượt). Đề tài không phải biến duy nhất.
  - Tiêu đề trên kênh khác tiêu đề trong gói release; tập 6 trên kênh mang dạng câu hỏi tìm kiếm ("Will AI Replace Graphic Designers?").

## Kết luận
1. **Mức tin cậy của thước khi chọn ngách: THẤP–CHƯA KIỂM ĐƯỢC.**
   - Hiệu chuẩn bằng LL chưa xác nhận cũng chưa bác bỏ thước, vì n = 4 và chưa tới 28 ngày.
   - Quyết định chọn ngách ở `REPORT.md` mục "Vòng cuối" vì vậy dựa trên thước *chưa hiệu chuẩn*. Nên coi đó là thứ hạng tương đối, không phải dự báo.
2. **Có nên dùng hồ sơ cầu khi chọn đề tài LL tập 9: CÓ, ở vai trò bộ lọc phụ.**
   - *Ưu:* rẻ (khoảng 300 đơn vị/đề tài với 3 câu). Đề tài duy nhất có cầu cũng là tập chạy tốt nhất. Hồ sơ còn chỉ ra câu hỏi người xem thật sự gõ ("will ai replace X").
   - *Nhược:* 7/8 đề tài LL đều là Không, nên nếu dùng như cổng cứng sẽ loại gần hết hướng LL.
   - *Tác động:* ưu tiên đề tài nghề có câu hỏi "will AI replace [nghề]" với video ≥ 50 nghìn đúng đề tài, và đặt tiêu đề theo câu hỏi đó.
   - *Rủi ro:* chạy theo câu hỏi thời sự về AI, làm loãng góc lịch sử của LL.
3. **Luật tự hiệu chỉnh (như Crux):**
   - Ghi thêm một dòng sau mỗi tập LL, lấy lượt xem tại mốc 28 ngày.
   - Khi có ≥ 3 tập "Mạnh/Yếu" và ≥ 3 tập "Không" mà trung vị nhóm có cầu không hơn nhóm Không, sửa cách tính trên nhánh `channel-k2`.
   - Các mốc 28 ngày gần nhất: tập 1 ngày 03/11, tập 6 ngày 05/11, tập 7 ngày 06/11, tập 8 ngày 07/11.

## Lần sửa cách tính
- (chưa có)
