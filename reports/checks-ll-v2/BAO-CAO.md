# Báo cáo phiên K — khoá bộ kiểm Last Lamplighters v2 (06/10/2026)

**Kết quả:** đã khoá. VERSION 1.6.0. `TREE_SHA256: 0973478b6493722f3812862238c0d31752ef8062102711299e8adefc13b63908` (`checks/lock.py --verify` cho KHỚP).
Nhánh `checks/ll-v2`, lấy từ đỉnh `ccr-8a2b38d7-rk5x31` (ec0a342). Tự kiểm: **52/52 ca đúng kỳ vọng** (`selftest.txt`).
Phán quyết từng luật ghi ở `checks-appeal.md`, mục "Phán quyết K — checks LL v2". Định nghĩa luật: `checks/ll/RULES-LL.md`.

## 1. Đã làm
| Việc | Kết quả |
|---|---|
| Xét và khoá Q13, Q14–Q18, Q19, Q20, Q21, Q22, va chạm chữ–isotype | Giữ nguyên ngưỡng. Sửa 6 điểm khi khoá: Q13 kiểm dấu, đọc "k", bỏ "?"; Q19 vá danh sách trắng; Q20 đo `zones`; Q21 không tin riêng `capsrc`; Q22 TRƯỢT khi không có log |
| Q7 và Q12 (cần cho ca lỗi tập 2) | Khoá. Q7 siết thêm: bản cũ không bắt được lỗi S2 tập 2 |
| Luật mới Q23: câu hoặc thẻ ghép nhiều số | Khoá. Thêm Q24 (nhãn phân loại khớp số) và Q25 (thẻ khoảng số không đếm qua số trung gian) để phủ hai bài học còn lại |
| Nối vào qc | `scripts/ll/qc.py` gọi `checks/ll` cho Q7, Q12–Q25, thêm dòng **LOCK**. Q1–Q6, Q8–Q11 giữ nguyên là luật của P |
| Hàm nền | `checks/ll/base.py` chép các hàm đọc dữ liệu từ ll.py, để P sửa ll.py không làm đổi nghĩa luật khoá |

## 2. Tự kiểm: bắt lỗi thật, không báo nhầm
| Lỗi thật | Luật | Bắt được | Khung đạt (bản G3) |
|---|---|---|---|
| Tập 2, S2: −5,3 % (dự báo) hiện nhãn ACTUAL | Q7 | có (log và đặc tả) | tập 2–5: sạch |
| Tập 2, T1: chữ S của "OPERATORS" bị cắt | Q12 | có (hộp vượt 1216; thiếu `.boxes.json`) | 8 thumbnail tập 2–5: sạch |
| Tập 2: thẻ 50–80 % đếm qua số trung gian | Q25 | có ("63%") | hiện thẳng "50–80% fewer": sạch |
| Tập 3: nhãn HSUS 135 nghìn sai phân loại | Q24, Q23(d) | có | tập 3 G3 "135,000 (1970 classification)": sạch |
| Tập 3: thẻ +87 % ↔ −13 % (đặc tả v1, 4833ac1) | Q23 | có (khác nguồn, trộn loại, khác kỳ) | tập 3, 5: 0 |
| Tập 5: câu 1966 gán nguồn OOH | Q21 | có (cả khi `capsrc` bỏ trống nguồn) | tập 5 G3: 0 |
| Tập 5: chữ tràn khung Shorts 9:16 (hộp −338…1418) | Q22 | có (cả dòng nguồn 16:9 đoạn 07) | `short9` gọn: sạch |
| Q13: số dự báo không nhãn, sai dấu, số không có | Q13 | có | bề mặt phát hành tập 2–5: 0 |
| Q14–Q18: tập 3 làm trước luật nhịp | Q14–18 | trượt cả 5 mục, khớp tổng kết lô 3–5 | tập 4, 5: đạt |
| Q19: thiếu `rid`, thiếu `credit` | Q19 | có | tập 5 (84,5 s, 4 dòng RIGHTS): sạch |
| Q20: chữ giao vùng isotype; cờ `hit` | Q20 | có | chú thích dưới vùng hình: sạch |

**Giới hạn dữ liệu (nêu rõ):**
- Log render và video không có trong repo (`/var/tmp/cine-out` không còn).
- Timeline tập 2–5 được K dựng lại bằng `ll.prep` từ giọng đã lưu, không gọi ElevenLabs. Tổng thời lượng khớp bản G2 (tập 5: 512,54 s = 8:32,5).
- Các ca cần log dùng log tối thiểu, dựng lại đúng chữ và hộp của lỗi. Hộp tràn Shorts tập 5 lấy từ tự kiểm của P. Hộp T1 tập 2 và chữ "63%" là dựng lại theo mô tả lỗi trong BAI-HOC #8 và #9, không phải số đo gốc.
- Ca HSUS 135 nghìn tái tạo theo dạng lỗi: K không tìm được khung G2 gốc.

## 3. Chạy thử trên 4 tập đã đăng: Q23 tìm thấy 2 chỗ
1. **Tập 2, thẻ so sánh đoạn 11:** −16,1 % (thợ tổng đài, đếm 1930–40, Feigenbaum) ↔ −5,3 % (CSR, dự báo 2025–35, BLS). Cùng dạng với thẻ +87 % ↔ −13 % mà chủ dự án đã bỏ ở tập 3. Tập 2 làm trước bài học này.
2. **Tập 4, hook Short S1:** "134,000 to 3.9 million" nối số 1900 (phân loại 1950, chỉ là ước lượng) với số 1970 (phân loại 1970) trong một dòng, không ghi cơ sở. Q13 không bắt được vì cả hai số đều truy được về `numbers`.

Hai chỗ này là phát hiện thật, không phải báo nhầm. Tự kiểm khẳng định Q23 chỉ bắt đúng hai chỗ đó. Xử lý: Q-L23b ở mục 5.

## 4. Chỉ số sát ngưỡng (±5 %) và rủi ro
- Không có số đo nào trong ±5 % quanh ngưỡng của Q12–Q25 trên dữ liệu chạy thử.
- Q15 tập 5: quãng dài nhất 7,9 s, ngưỡng 8 s, lệch 1,25 %. **Sát ngưỡng.** Tập 4: 8,0 s, đúng bằng ngưỡng.
- **Rủi ro Q23:**
  - Số trong lời được nhận bằng cụm `say`. Số không khai `say`, hoặc đọc khác cụm đã khai, sẽ lọt.
  - Ở thẻ và chú thích, K chỉ tính số có khai `num`. Số chỉ nằm trong chữ thì Q21 và Q13 chặn ở bước khác.
  - K đã bỏ việc nhận số theo chữ trong thẻ, vì gây báo nhầm: "BLS rounds to −5%" trùng chữ với một số khác.
- **Rủi ro Q12:** hộp chữ do `thumb.py` tự khai. K chưa đo trên điểm ảnh.
- **Rủi ro Q20:** cho tới tập 5, chỉ có cờ `hit` (render tự khai). Phép đo độc lập cần `zones` từ tập 6.
- Khi qc chạy không có render (chỉ có timeline), Q22 TRƯỢT. Đây là chủ ý: `qc-ep05-timeline.md` cho mọi mục khác ĐẠT, LOCK ĐẠT.

## 5. Việc đang chờ chủ dự án
Bốn câu hỏi có phương án và khuyến nghị ở `checks-appeal.md`:
- **Q-L23a**, nghĩa của "cùng đối tượng". Khuyến nghị A: cùng cơ quan nguồn, cùng loại, cùng kỳ. Đang khoá theo A.
- **Q-L23b**, hai chỗ ở tập đã đăng. Khuyến nghị A: không sửa video đã đăng, ghi bài học.
- **Q-L20**, bắt buộc `zones` từ tập 6. Khuyến nghị A: có; P sửa render.js.
- **Q-L13**, bỏ "?" khỏi dấu hiệu dự báo. Khuyến nghị A: bỏ. Đang khoá theo A.

Còn mở từ trước: mục 1–7 và Q1–Q6, Q8–Q11 của mục 8. Bản này không xử lý.

## 6. Việc cho P (sau khi chủ dự án duyệt)
- Merge `checks/ll-v2`. Từ nay qc có dòng LOCK.
- Khai `basis` cho số theo phân loại nghề. Giữ `say` đúng như lời.
- Nếu Q-L20 chọn A: thêm `zones` vào log render từ tập 6.

## 7. Token phiên K
Ước tính khoảng 150 nghìn token (đầu vào mới cộng sinh ra), dưới trần 200 nghìn. Số này là ước tính, không đo từ log.

**DỪNG:** đã khoá xong. Chờ chủ dự án duyệt.
