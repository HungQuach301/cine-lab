# ĐỀ XUẤT KINH THÁNH §19 — chữ đề xuất cho phiên P (TIEN-KY-T4, 23/10/2026) — CHƯA ÁP vào `docs/`

> Căn cứ: nâng cấp chất lượng T4 chủ dự án duyệt 23/10 13:06 (điểm 6, 7, 8 — "đã từng có nhưng đã bị mờ đi"); số đo bản thử T2/T3/T4 của phiên này (`reports/tien-ky-t4/TIEN-KY-T4-BAO-CAO.md` §6). Số tốc độ dưới đây là **đề xuất ban đầu**, hiệu chỉnh lại sau khi chủ dự án xem bản thử T4 (`xem/T4-cu-may.mp4`).
> Phiên P chép nguyên văn khối trích dẫn vào Kinh thánh nếu được duyệt; phiên K biến thành chỉ số trong `checks/` (đo từ log máy `render_ldn.js` — mỗi khung có ma trận máy).

---

> **§19. Ngữ pháp máy điện ảnh cho timelapse cùng nơi + chất liệu tư liệu sống (áp từ T4; chủ dự án duyệt …/10/2026).**
>
> **(a) Bộ cú máy.** Trong một shot timelapse, máy được dùng MỘT trong các cú sau; **thời gian chạy suốt cú máy** (không dừng thời gian để "khoe" chuyển động máy):
>
> | Mã | Cú máy | Thông số đề xuất (đo tại tiêu điểm, khung 16:9) |
> |---|---|---|
> | CODINH | cố định / trôi nhẹ | ≤ 2 % khung/giây (giữ TL-1 cũ) — **bắt buộc** cho shot dùng tấm nền N2+ |
> | DAY | đẩy vào chậm | tiêu điểm phóng ≤ 1,5 %/s chiều rộng; tiến ≤ 1,5 % khoảng cách tới tiêu điểm mỗi giây |
> | KEO | kéo lùi lộ cảnh | lùi ≤ 2 % khoảng cách/giây; phải lộ ra vật mang nghĩa mới (không kéo lùi chỉ để "rộng") |
> | CAU | cần cẩu lên/xuống | 2–6 m/s ở độ cao 150–300 m; góc chúc đổi ≤ 1,5°/s |
> | VONG | vòng cung quanh tiêu điểm | tổng ≤ 30–45°, ≤ 3°/s; tiêu điểm giữ trong vùng 1/3 |
> | TRUOT | trượt ngang có tiền cảnh (thị sai) | tiêu điểm dịch ≤ 3 % khung/s; tiền cảnh 8–15 %/s; tiền cảnh là vật đúng mốc năm |
> | NGHIENG | nghiêng lộ cảnh | ≤ 2°/s, kết thúc ở vật mang nghĩa |
> | THAP | góc thấp anh hùng | máy 20–60 m, ngửa 5–15°; chỉ cho công trình có vai truyện; tổng ≤ 12 % thời lượng tập |
> | XUONG | nhìn thẳng xuống → xiên | từ −90° về −20…−35° trong 4–8 s; dùng cho chuyển bản đồ ↔ 3D |
> | LAN | cú lặn | theo §14.3 |
> | KHOP | khớp cắt cùng khung khác năm (then–now) | cùng máy, cùng FOV (sai khác 0 px ở điểm neo); cắt hoặc hoà ≤ 1 s |
>
> **Luật:** (1) mỗi chương ≥ 4 loại cú máy (không tính M-d và thẻ); (2) ≤ 2 shot liền nhau cùng loại; (3) **điểm máy xương sống chính tái xuất mỗi hồi với khung y hệt** (lưu tham số máy một lần, mọi lần dùng đọc lại đúng tham số) để khớp cắt; (4) TL-1 sửa thành: *"6–8 điểm máy cao; trong shot máy dùng bộ cú máy §19 (a) với giới hạn tốc độ trên; shot có tấm nền N2+ phải CODINH; ≥ 75 % thời lượng là góc cao/toàn cảnh có thời gian chạy (phần cao của cú lặn tính vào)"*; trần cắt/phút TL-1 không áp cho cắt góc trong shot (như §14.7 V2-D7).
>
> **(b) Bản đồ cổ hoạt hoá.** Chỉ dùng bản đồ thời đó có bằng chứng PD/CC0 lưu ở `licenses/` (URL, ngày, JSON/ảnh trang). Hoạt hoá được phép: vẽ lan lửa, hướng, ranh theo **dữ kiện có nguồn** (tên nơi theo ngày bậc 2 × vị trí bậc 1; đoạn nội suy ghi "ước lượng" bậc 5 trong log); máy đẩy/trượt; chuyển bản đồ ↔ 3D **cùng toạ độ** (khớp điểm khống chế, ghi sai số đo được). **Không** dùng AI vẽ lại, tô màu, làm nét hay "phục chế" bản đồ/tranh khắc. Mỗi lần ≤ 10 s, ≤ 1–2 lần/hồi, ≤ 3 tên nơi trên hình; tổng bản đồ (cổ + 3D kiểu bản đồ) ≤ 12 % thời lượng. Lớp vẽ thêm (lửa, ranh) dùng màu/nét không lẫn với nét khắc gốc.
>
> **(c) Tranh khắc công trình/nhân vật.** Khớp vào 3D **cùng góc** (hoà ≥ 1 s: tranh → 3D hoặc ngược lại) hoặc đặt ở góc khung (≤ 1/3 khung). Chỉ thị sai 2,5D thủ công (tách lớp bằng tay theo nét vẽ, không ước độ sâu bằng AI — §12.3) hoặc đẩy nhẹ ≤ 1,5 %/s; không AI lên tư liệu. Chú thích ≤ 6 từ. Mỗi mục ghi RIGHTS (nguồn, giấy phép, bằng chứng). Tính chung trần tư liệu + tranh khắc + thẻ ≤ 10 % thời lượng.

---

## Ghi chú cho phiên P / K
- Tham số máy từng shot của bản thử T4 + tốc độ đo được: `reports/tien-ky-t4/do/t4-may.json` (sinh từ `log.json` của `render_ldn.js`).
- Chỉ số máy đo được cần K: % khung/giây của tiêu điểm (chiếu điểm neo qua ma trận máy), °/s, m/s, sai khác điểm neo giữa hai lần dùng cùng khung (KHOP).
- Xung đột phải ghi: §15 (f) liệt kê M-d (6) "nổ nhà bằng thuốc súng Tower Street", nhưng LUAT-N2P-T4 (b34, B2) xếp nổ nhà là lớp dữ kiện (không giao AI). Đề xuất: bỏ (6) khỏi danh sách M-d, dựng 3D; thay bằng "người cứu đồ lên xe ở Cheapside sáng 3/9" (b21/b24, lớp chi tiết minh hoạ) — chủ dự án quyết ở phiếu G1.
