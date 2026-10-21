#!/usr/bin/env python3
"""P-2010 · sửa docs/BIBLE-KENH2.md theo quyết định 19–20/10/2026: thêm §14 (14.1–14.6), sửa §11.3 (câu KHÔNG), §12.2 (phép thử bỏ AI),
§12.3 (KHÔNG video AI), §12.5 (Cycles chỉ khung tĩnh → trừ cú lặn §14.2), tiêu đề.
Mỗi thay thế kiểm "đúng 1 lần xuất hiện" trước khi áp; §14 chỉ thêm khi tệp chưa có "## 14.". Chạy một lần."""
import hashlib, os, sys
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
P = os.path.join(R, 'docs/BIBLE-KENH2.md')
SHA_TRUOC = '5014eb8e3793f864b47fef330d14209554f1e1f4971b60cd5a713b2638a0618b'
s = open(P, encoding='utf-8').read()
assert hashlib.sha256(s.encode()).hexdigest() == SHA_TRUOC, 'Kinh thánh không phải bản P-1910'
assert '## 14.' not in s

SUA = [  # (nhãn, cũ, mới)
    ('tieu-de', '§13 + sửa 19/10)', '§13 + sửa 19/10; §14 + sửa 20/10)'),
    ('§11.3 KHÔNG',
     '- KHÔNG: AI video sinh từng khung (nhấp nháy, trôi hình; API video OpenAI ngừng 24/9/2026); AI cho cảnh bay trên không tầm cao, bản đồ chiến lược; ước độ sâu bằng AI;',
     '- KHÔNG: AI sinh, xoá hoặc đổi LỚP DỮ KIỆN (§14.1) ở mọi loại cảnh; khung AI (ảnh hay video) chưa qua cổng kiểm §14.1 (e) — nhấp nháy, trôi hình, vật bịa; AI cho bản đồ chiến lược; ước độ sâu bằng AI;'
     ' (sửa 20/10: AI video và cảnh bay trên không tầm cao được dùng cho LỚP NỀN theo N1/N2 — §14.1);'),
    ('§12.2 phép thử',
     '- AI chỉ được TÌM, ĐỌC, ĐỐI CHIẾU, PHỤC CHẾ, LÀM SỐNG cái đã có nguồn; không sinh dữ kiện (vị trí, công trình, cờ, quân phục, ngày, số). Phép thử: bỏ AI ra mà dữ kiện trên hình đổi → không được dùng.',
     '- Với LỚP DỮ KIỆN (§14.1): AI chỉ được TÌM, ĐỌC, ĐỐI CHIẾU, PHỤC CHẾ, LÀM SỐNG cái đã có nguồn; không sinh dữ kiện (vị trí, công trình, cờ, quân phục, ngày, số). Phép thử áp cho lớp dữ kiện: bỏ AI ra mà lớp dữ kiện trên hình đổi → không được dùng. LỚP NỀN: AI được vẽ lại theo N1/N2 (§14.1, sửa 20/10).'),
    ('§12.3 KHÔNG video',
     'tô màu khi không có nguồn màu; video AI.',
     'tô màu khi không có nguồn màu; video AI ngoài N1/N2 (§14.1, sửa 20/10).'),
    ('§12.5 Cycles',
     'Cycles chỉ cho khung tĩnh, poster, thumbnail.',
     'Cycles chỉ cho khung tĩnh, poster, thumbnail (sửa 20/10: và cú lặn/cận cảnh đêm có lửa dựng trọn bằng Cycles GPU — §14.2).'),
]
for nhan, cu, moi in SUA:
    n = s.count(cu)
    if n != 1: sys.exit(f'DỪNG: "{nhan}" xuất hiện {n} lần (cần đúng 1)')
    s = s.replace(cu, moi)

S14 = '''## 14. Bổ sung 19–20/10/2026 (chủ dự án duyệt; nới luật AI tới N2 20/10 21:15, duyệt tất cả khuyến nghị 20/10 21:22)

### 14.1 Luật AI mới N1/N2 (thay các câu trái ngược ở §11.3, §12.2, §12.3 — sửa 20/10)
- (a) Hai lớp. LỚP DỮ KIỆN = công trình, phố (bố cục), cờ, tàu, pin nổi, lửa, khói trận, người/quân, đèn, chữ, ngày, số — phải có nguồn (5 bậc §12.2); AI không được sinh, xoá hay đổi. LỚP NỀN = đất, nước, trời, mây, thảm thực vật, vân tường/mái/mặt đất, sương, ánh sáng — AI được vẽ lại ở mọi loại cảnh, kể cả bay cao và VIDEO.
- (b) N1 "nền tự do, dữ kiện khoá": mọi vùng lớp dữ kiện ghép lại điểm ảnh nguồn theo mặt nạ ID (sai khác < 1/255 trong vùng bảo vệ, viền mềm ≤ 3 px); cấm vật thuộc lớp dữ kiện xuất hiện mới ở vùng trống; cấm đổi loại vùng (đất ↔ nước).
- (c) N2: thêm tối đa 20 % thời lượng tập là "minh hoạ" toàn khung AI cho khoảnh khắc không mang dữ kiện vị trí (móc mở đầu, cú lặn, chuyển cảnh); dữ kiện của đoạn đó kể bằng lời/bản đồ/chú thích; nhãn "Illustration" trên hình suốt đoạn (ngoại lệ của §12.1).
- (d) Tổng khung có AI (N1 + N2) ≤ 20 % thời lượng ở T3; mở rộng theo lộ trình M1–M4 (g) khi cổng đạt.
- (e) CỔNG KIỂM BẮT BUỘC cho mọi khung AI: bộ đo bịa NC-V2V (T1–T6; thêm T7–T9 của NC-V2V3 khi nhánh đó được duyệt; thêm phép "đốm sáng mới bền ≥ 1 s") có đối chứng không AI + người đọc tờ so; chấm mù KHÔNG thay kiểm dữ kiện; sổ AI ghi mọi lệnh gọi (model, prompt nguyên văn, % mặt nạ, chi phí, C2PA/SynthID). Phiên K biến bộ đo thành công cụ trong `checks/` (V2V-D4).
- (f) Công bố: bật khai báo nội dung AI trên YouTube; mô tả §10.6 viết lại theo N1/N2 (câu hiện hành ở §10.6 giữ tới khi chủ dự án duyệt bản viết lại); giữ đo bình luận chê AI ≤ 2 % (§11.3).
- (g) Lộ trình: M1 luật + bố cục (không AI) → M2 thumbnail + móc mở đầu 30 s + cú lặn (≈ $5–15/tập) → M3 shot hero ≤ 20 % (≈ $15–80/tập) → M4 nền N1 cả tập (≈ $110–330/tập, chủ dự án duyệt chi). Mỗi mốc qua cổng: 0 vật bịa; chấm mù thắng bản không AI; không nhấp nháy/đường nối lộ; M3: làm lại ≤ 3 lượt/đoạn. Công cụ chọn theo kết quả NC-V2V3: Cosmos-Transfer nếu đạt, không thì Gemini Omni có ghép mặt nạ.

### 14.2 Đường dựng G0 (NC-D1, NG-D1, NG-D3)
- Phần cao dựng bằng cách A: three.js + nướng Cycles theo mốc + vân CC0 theo lớp phủ + bụi + nước mới + sương e^(−σd).
- Cú lặn/cận cảnh đêm có lửa (10–20 % thời lượng) dựng TRỌN bằng Cycles GPU thuê (RunPod); không ghép A↔B trong một cú máy. Chưa chuyển cả tập sang Cycles (NG-D3).
- Bỏ Eevee/llvmpipe (NC-D3). Cycles: 16 spp + OIDN đủ cho cảnh cao ban ngày (NC-D4); ánh trời khuếch tán `--skydif` = 1/1,15π, sương chỉ trên tia máy (NG-D2).
- Sau T3: đưa sprite khói/lửa thể tích dựng sẵn + nướng lightmap trên GPU vào A (NG-D5).

### 14.3 Cú lặn (GPU-3, duyệt 19/10 22:58) — bổ sung §13.6
- Một cú liền: cao timelapse → hạ lướt phố/mặt nước → ngược lên cao; thời gian chạy tiếp suốt cú.
- Phần thấp trong cú lặn không tính vào trần lướt thấp TL-2 10 %.
- Mỗi cú lặn phải có vai truyện ghi trong bảng shot.

### 14.4 Look
- Giữ bão hoà trung vị ≥ 0,40 (§11.4; NG-D4).
- Ảnh Omni chỉ là ĐÍCH LOOK đo bằng số (sương, phối cảnh khí quyển), không chép hình (V2V-D2).
- Mật độ bụi trước 1900 = 0,45 × hiện nay là bậc 5 TẠM (NC-D5); kết quả tra nguồn: `reports/p2010/P2010-BAO-CAO.md` §4.

### 14.5 Đóng gói
- Khuôn tiêu đề series (c) "<Nơi>: <lời hứa> | 3D Timelapse", ≤ 60 ký tự; mọi dữ kiện trong tiêu đề phải đúng lời khoá (cấm kiểu "14 Sieges in 3D" khi chỉ dựng 2 cuộc).
- Thumbnail do phiên dựng làm từ render của ta (DG-1), được AI tăng cường theo N1; góc máy thumbnail PHẢI có trong phim.
- Test & Compare là "tính năng nâng cao", không đòi YPP.

### 14.6 Âm thanh
- Nhạc T3 = phương án B (Scott Buckley, CC BY 4.0), trừ tấm im lặng KA2026 = phương án A.
- Chỉ nhạc miễn phí có giấy phép rõ; không phát tán bản nhạc riêng (soundtrack).
- Master âm thanh phát hành (giọng, nhạc, stem) PHẢI vào LFS kèm SHA.
'''
s = s.rstrip('\n') + '\n\n' + S14
open(P, 'w', encoding='utf-8').write(s)
open(os.path.join(R, 'reports/p2010/s14-ban-chep.md'), 'w', encoding='utf-8').write(S14)
print('SHA trước', SHA_TRUOC); print('SHA sau  ', hashlib.sha256(s.encode()).hexdigest())
