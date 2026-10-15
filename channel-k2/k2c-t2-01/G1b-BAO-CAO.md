# K2C-T2-01 "Shipbuilding" — BÁO CÁO CỔNG G1b (phiên T2, 15/10/2026). DỪNG, chờ chủ dự án rà tờ khung

> Làm theo lệnh duyệt G1 (15/10): J1–J6 ghi vào AUTHORSHIP; người đọc mù vòng 4 trên lời v3.2, sửa một lần rồi khoá; tra lại phí Section 301; tờ khung 540p. Nhánh **`k2c-t2`**, đẩy cả `ccr-bef6f172-fcqat9`. Không sửa `docs/BIBLE-KENH2.md` (J2), không sửa và không đọc mã `checks/`.

## 0. Tóm tắt một màn hình
| Hạng mục | Kết quả |
|---|---|
| AUTHORSHIP | Thêm dòng "Kênh 2 K2C-T2-01 "Shipbuilding" (G1 — DUYỆT)", ghi J1–J6 cùng phần đóng góp của chủ dự án |
| Người đọc mù vòng 4 (v3.2) | 3 vai, model ghim. Móc **7/7/7** (v3: 6/8/6) · nhân vật **4/4/4** (v3: 5/6/5) · tin cậy **8/7/6** (v3: 7/8/7). 3/3 xem tiếp sau 15 s; 3/3 thấy phần kết trả lời câu hỏi mở đầu; 3/3 không thấy nghiêng phe |
| Sửa sau vòng 4 | 7 lỗi được ≥ 2/3 người đọc nêu, mỗi lỗi sửa **một lần, theo đúng chữ góp ý**; không chạy thêm vòng (§2) |
| **Lời KHOÁ v3.3** | 1 588 từ, ≈ 10:30 ở tốc độ đọc, ước timeline **10:42,5**. `script.md` SHA-256 **`4554b697…20473`**, `loi-khoa.txt` `9bf318c2…`. `make_spec.py` dừng nếu lời lệch SHA |
| Phí Section 301 (tra 15/10) | **Không đổi** so với C01: tạm hoãn tới 9/11/2026 (90 FR 50947). Chưa có văn bản gia hạn hay chấm dứt. Lời ghi "As of October fifteenth, 2026" (§3) |
| Tờ khung 540p | `g1b/TO-KHUNG-G1b.jpg`: 22 cửa sổ 6 s, gồm Đ1–Đ3 và ≥ 1 khung cho mỗi chương 00–06 (§4) |
| Nhịp thị giác (rhythm.py, trên đặc tả) | **ĐẠT**: trung bình **2,43 s**/biến cố (ngưỡng 3,5), khoảng dài nhất **5,56 s** (ngưỡng 6; cách ngưỡng −7,3 %) |
| Footage (đặc tả) | **0 %** (ngưỡng ≤ 20 %): G1b không nối footage (§6) |
| API `claude -p` | **$4,03** luỹ kế / trần $11 (G1b thêm $0,24 cho vòng 4) |
| YouTube Data API | ≈ 216 / 300 (G1b không dùng) · ElevenLabs: 0 ký tự |

## 1. AUTHORSHIP (việc 1)
Đã thêm dòng `2026-10-15 | Kênh 2 K2C-T2-01 "Shipbuilding" (G1 — DUYỆT)` vào `AUTHORSHIP.md`, ghi nguyên ý J1–J6 và phần đóng góp biểu đạt của chủ dự án: chọn đề tài trong 3 ứng viên, chọn thứ tự móc, chọn cách đặt câu miễn trừ, chọn tiêu đề và thumbnail, đặt hạn đăng.

## 2. Người đọc mù vòng 4 trên lời v3.2 (việc 2, J4)
- **Cách chạy:** 3 vai, `claude -p` ghim `claude-sonnet-5-5`, mỗi vai chạy trong thư mục trống, cùng đề bài với vòng 1–3. Kết quả ở `kiem-mu/bien-kich_v4-R{1,2,3}.json`. Chi phí $0,24.

| Chỉ số (R1/R2/R3) | v3 | **v3.2 (vòng 4)** |
|---|---|---|
| Móc | 6/8/6 | **7/7/7** |
| Nhân vật | 5/6/5 | **4/4/4** |
| Tin cậy | 7/8/7 | **8/7/6** |
| Cơ chế nối nhau | — | 6/7/6 |
| Xem tiếp sau 15 s | 3/3 | 3/3 |
| Kết trả lời câu hỏi mở đầu | — | 3/3 |
| Nghiêng phe | không (3/3) | không (3/3) |

- **Lỗi ≥ 2/3 cùng nêu → sửa MỘT lần bằng đúng chữ góp ý (v3.3), không chạy thêm vòng:**

| Lỗi (số người nêu) | Góp ý | Sửa trong lời |
|---|---|---|
| Không nêu tên trợ cấp (3/3) | "Never named or explained" | "…a federal subsidy, **the Construction Differential Subsidy**, meant to let American owners buy American ships at the world price" (C20) |
| "four hundredths of one percent" khó hiểu (3/3) | "Say '0.04 percent'" | "**0.04 percent**" |
| Không rõ phí để làm gì (3/3) | mục đích phí không được nói | thêm "The stated aim: to discourage the use and purchase of Chinese-built ships, and to press China to drop the practices the Trade Representative had found." (C57, trích FR-ACT) |
| Dồn ngày tháng ở chương 05 (3/3) | "Lots of dates, notices and fee mechanics before the point" | "From October 2025," thay cụm "Under an action … April seventeenth"; "In March 2024", "In September," |
| Khung "lương" (3/3) | nhấn quy mô mạnh hơn bằng chứng | thêm "Our emphasis on scale is a position the evidence only partly supports." |
| Thuật ngữ TFP (2/3) | "Jargon with no explanation" | bỏ câu năng suất các nhân tố tổng hợp (TFP) |
| Dồn số ở chương 01 (2/3) | "Stat dump" | bỏ câu 2 710 tàu và câu 702 000 người |

- **So với v3:** móc đều hơn (7/7/7). Điểm nhân vật giảm 5–6 → 4. Cả 3 người đọc nói chương 04 chậm vì rào đón ("by the company's account", lore tờ 500 won). **Không sửa phần này trong lời**, vì nhãn nguồn tự thuật và nhãn lore là luật nội dung (LUAT-NOI-DUNG-G); tờ khung xử lý bằng hình (§4), và người chấm mù ở bước Dựng sẽ đánh dấu lại. Điểm nhân vật giảm có thể do bỏ chi tiết ở chương 01; chưa có số đo để tách hai nguyên nhân.
- **Lời KHOÁ v3.3:** `script.md` (bản sao `script-v3.3-KHOA.md`; v3.2 lưu ở `script-v3.2.md`). 1 588 từ, 7 đoạn, 57 claim. SHA ở `LOI-KHOA.sha256`:
  - `script.md` `4554b69708a1ab08a7ffbe7ef3fb0f7e92aaac8a04fb8d57d2325dbb11d20473`
  - `loi-khoa.txt` (chuỗi gửi ElevenLabs, đã bỏ mã claim) `9bf318c282f83cab3ea9013617f4c1ef55f0e647d585f04a4b7bb8168a74906a`

## 3. Trạng thái phí Section 301, tra trước khi khoá lời (việc 3)
- **Tra ngày 15/10/2026:**
  - Federal Register API, cơ quan USTR, văn bản từ 01/09/2026: 8 văn bản, không văn bản nào về hàng hải hay đóng tàu.
  - Tìm "maritime logistics shipbuilding section 301" từ 01/11/2025: chỉ có 2 văn bản ngày 10/11 và 13/11/2025.
  - Danh mục công khai (public inspection) ngày 15/10: không có thông báo USTR nào về phí này.
- **Kết luận: không đổi so với C01.** Phí vẫn tạm hoãn tới 11:59 p.m. ngày 9/11/2026 (90 FR 50947, govinfo FR-2025-11-13). Lời ghi "As of October fifteenth, 2026, no extension had been published." Nhật ký tra ở `claims.md` §3.
- **Rủi ro còn mở (J6, đích đăng trước 9/11):** phải tra lại một lần nữa ngay trước khi thu giọng. Nếu USTR ra văn bản mới, cần sửa 3 câu (00, 05, 06) và khoá lại SHA.
