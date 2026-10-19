#!/usr/bin/env python3
"""P-1910 · sửa docs/BIBLE-KENH2.md theo quyết định 18–19/10/2026: thêm §13 (13.1–13.6), sửa §4, §10.6, §11.2 (D8), §11.6, §12.1, tiêu đề.
Mỗi thay thế kiểm "đúng 1 lần xuất hiện" trước khi áp; §13 chỉ thêm khi tệp chưa có "## 13.". Chạy một lần."""
import hashlib, os, sys
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
P = os.path.join(R, 'docs/BIBLE-KENH2.md')
SHA_TRUOC = '3307185e3e51a78f57088aa74ae575c828fd9d80fe4f04514451a70d1a24eaaf'
s = open(P, encoding='utf-8').read()
assert hashlib.sha256(s.encode()).hexdigest() == SHA_TRUOC, 'Kinh thánh không phải bản P-1810c'
assert '## 13.' not in s

SUA = [  # (nhãn, cũ, mới)
    ('tieu-de', 'bổ sung 18/10/2026 tối — §12)', 'bổ sung 18/10/2026 tối — §12; §13 + sửa 19/10)'),
    ('§4 giọng', 'giọng Eric eleven_multilingual_v2',
     'giọng G1 (Voice Design `VDLncRBHDjLHBqLhQ1Qt`, chọn qua nghe mù 18/10 và 19/10) eleven_multilingual_v2, speed 1,03; điều khoản chờ thư Đ5'),
    ('§10.6 D7', 'on marked street frames', 'on two street frames'),
    ('§11.2 D8', 'khung neo phố ban ngày 30–80 người ở 10–60 m',
     'khung neo phố ban ngày 30–80 người ở 10–60 m (1782: theo bảng gác Spilsbury 7/9/1782 + dân thường từ danh-sach-9-1782 — D8)'),
    ('§11.6', '540p ≤ 15 MB', '540p ≤ 5 MB (§12.5)'),
    ('§12.1 TL-4', 'số liệu hoặc câu trích khi lời đang nói tới, kèm tên nguồn ngắn cỡ nhỏ, ≤ 3 s.', '(bỏ — theo §13.6 TL-4).'),
    ('§12.1 D6', 'thẻ "How this film was made" 4–5 s ở cuối video', 'thẻ "How this film was made" 2 thẻ × ≈ 8 s cuối phim (D6)'),
]
for nhan, cu, moi in SUA:
    n = s.count(cu)
    if n != 1: sys.exit(f'DỪNG: "{nhan}" xuất hiện {n} lần (cần đúng 1)')
    s = s.replace(cu, moi)

S13 = '''## 13. Hiểu hai đường (chủ dự án duyệt HC-1, HC-2 ngày 19/10/2026 06:44)

13.1 Mục tiêu: có lời hay tắt lời, người xem vẫn hiểu câu chuyện chính. Lời cho chiều sâu; hình cho mạch chính.

13.2 Mỗi nhịp chính của lời khoá có ít nhất một vật mang nghĩa bằng hình: cờ hoặc chủ quyền đổi trên công trình, bộ đếm năm, ranh giới hoặc mũi tên động trên bản đồ, sự kiện thấy được (tàu, lửa, xây, phá, đám đông), hoặc thẻ chương. Bảng nhịp → vật mang nghĩa phủ ≥ 90 % nhịp chính.

13.3 Thẻ chương (ngoại lệ của §12.1): kiểu A, góc dưới trái, hiện và tắt mờ dần trên cảnh đang chạy; tối đa 8 thẻ/tập; dạng "năm — cụm ≤ 6 từ"; ≤ 3 s; lời trung tính giữa các phía tranh chấp ("changes hands", không "captured/liberated"); không thẻ trong móc mở đầu.

13.4 Cổng XEM CÂM (bắt buộc từ T3): animatic tắt tiếng + 8 câu hỏi hiểu cốt truyện; 3 người chấm AI xem chuỗi khung + chủ dự án xem tắt tiếng ≈ 2 phút; đạt ≥ 6/8. Trượt → sửa bằng hình, không thêm chữ ngoài §13.3, rồi chấm lại.

13.5 Phụ đề CC tiếng Anh chuẩn từ lời khoá cho mọi tập; bật lồng tiếng tự động YouTube khi có cho kênh.

13.6 Ngữ pháp hình timelapse (duyệt TL-1…TL-6 ngày 19/10/2026 12:45)
- TL-1 Xương sống timelapse: 6–8 điểm máy cao cố định (hoặc trôi ≤ 2 % khung/giây); trong shot, thời gian chạy (nhà mọc/cháy/sập, công trình có ngày đầu/cuối, tàu, ngày–đêm, khói); mỗi phần phim quay lại cùng điểm máy ở năm khác. Mục tiêu ≥ 75 % thời lượng là góc cao/toàn cảnh có thời gian chạy; ≤ 5 cắt/phút (shot trung bình ≥ 12 s). Số hiệu chỉnh sau bản thử V7.
- TL-2 Lướt thấp ≤ 10 % thời lượng, chỉ cho khung neo phố và khoảnh khắc người, có vai truyện ghi log.
- TL-3 Không shot trống: mỗi shot ≥ 1 thay đổi theo thời gian hoặc biến cố thấy được; nội dung từ nguồn bậc 1–3, chỗ ước tính ghi `bac`.
- TL-4 Không tấm tư liệu và tấm số/câu trích đứng riêng; tư liệu chỉ phủ khớp lên địa hình rồi tan vào cảnh ≤ 3 s; số liệu và câu trích do lời + phụ đề CC mang.
- TL-5 Mở đầu là timelapse từ giây 0, dài theo lời móc; khoảnh khắc giá trị nhất xuất hiện trong 30 s đầu.
- TL-6 Thẻ chương theo §13.3.
'''
s = s.rstrip('\n') + '\n\n' + S13
open(P, 'w', encoding='utf-8').write(s)
open(os.path.join(R, 'reports/p-1910/s13-ban-chep.md'), 'w', encoding='utf-8').write(S13)
print('SHA trước', SHA_TRUOC); print('SHA sau  ', hashlib.sha256(s.encode()).hexdigest())
