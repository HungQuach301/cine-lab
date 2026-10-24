# P-2410b: sửa docs/BIBLE-KENH2.md theo K1175-D1…D7 (chủ dự án 24/10/2026, "Duyệt K1175-D1…D7 theo khuyến nghị").
# Mỗi chuỗi gốc phải xuất hiện đúng 1 lần; không chép luật 1.17.5, chỉ trỏ tới checks/ll/RULES-LL.md mục 1.17.5.
import hashlib, sys
P = 'docs/BIBLE-KENH2.md'
s = open(P, encoding='utf-8', newline='').read()
print('trước', hashlib.sha256(s.encode()).hexdigest())
DUYET = '24/10/2026, tin nhắn ngay trước lệnh P-2410b, "Duyệt K1175-D1…D7 theo khuyến nghị"'
E = []
# 0. tiêu đề
E.append(('thêm §15 (j) — 24/10/2026)',
          'thêm §15 (j) — 24/10/2026; sửa §13.6, §15 (a)(b)(c)(d)(j) theo K-1.17.5 (K1175-D1…D7) — 24/10/2026)'))
# 1. §13.6 cách khai thêm trường 1.17.5 (sau dòng "Cách khai T4")
a = 'giữ `log_may` (log.json của `render_ldn.js`, lưu cùng shot, không để ở `/var/tmp`) (duyệt 23/10/2026 23:45 ngân sách $35; 24/10/2026, K1174-D4 = A).\n'
E.append((a, a +
 '- Cách khai thêm từ 1.17.5 (theo `reports/k1175/K1175-BAO-CAO.md` §7; định nghĩa, trường đọc và ngưỡng: `checks/ll/RULES-LL.md` mục 1.17.5, LOCK 1.17.5 `c7630b4a…`; Kinh thánh không chép luật): '
 '**mọi tấm N2+** khai `n2p.tam[]` {id, shot, render (render-khớp), ghep (PNG), mat_na (PNG đúng độ phân giải khung — không thu/phóng), nam}; mặt nạ ID + tấm ghép + JSON kiểm lưu vào git (PLAN.md, K1175-D6); '
 '**lớp sống** (khói bếp, vật bán trong suốt) khai `song: {render_co, render_khong, nen}` — `nen` là tấm đã ghép lớp (a), chưa cộng lớp sống; '
 '**khớp màu cục bộ vòng bảo vệ** khai `khop_mau_cuc_bo: true`; '
 '**phủ bề mặt nhà (BE-MAT-NHA)** khai `be_mat_nha_ai: true`, `mat_na_nha` (PNG 24 bit mã nhà), `mat_na_mat` (PNG mã mặt phẳng), `bong` (pass bóng: cùng máy/giờ, vật liệu xám đều 0,6, không vân), `nha` (JSON [{id, lo, px_m}], px_m = độ dài chiếu 1 m ngang ở tâm nhà), lớp `nha_thuong` (215,215,215) trong mặt nạ lớp, `nen_ai: true` nếu tấm cũng là tấm nền N2+; '
 'timelapse khai `be_mat_nha_video: {ghep, render, cach: anh_tinh | chieu_3d, tam}` (`tam` = tấm AI đã duyệt, cho `chieu_3d`) '
 f'(duyệt {DUYET}: K1175-D2…D7).\n'))
# 2. §15 (a) ngoại lệ D3 (dòng mới ngay sau (a))
a = '**LỚP NỀN — AI tự do về bề mặt** (vân đất, nước, trời, sương, ánh sáng), không tự do về hình học.\n'
E.append((a, a +
 '- (a) ngoại lệ — khớp màu cục bộ vòng bảo vệ (từ T4): khi tấm khai `khop_mau_cuc_bo: true`, vòng bảo vệ (phần nở 1 px / 3 px quanh mặt nạ (a)) được = render-khớp + **MỘT độ lệch màu cho mỗi vật** '
 '(trung vị AI − trung vị render-khớp ở dải ngoài), thay cho "vùng bảo vệ = render"; lõi mặt nạ (a) vẫn 0/255; không vẽ lại mép vật. K kiểm bằng N2P-1 (d) (RULES-LL 1.17.5) '
 f'(duyệt {DUYET}: K1175-D3 = A; thay V4 = b).\n'))
# 3. §15 (b) D1 + D4 (dòng mới ngay sau (b))
a = 'Vật chuyển động và lớp dữ kiện luôn từ render từng khung; chuyển giữa hai tấm nền chỉ bằng hoà ≥ 2 s.\n'
E.append((a, a +
 '- (b) phản chiếu (từ T4): phản chiếu trên mặt nước **chỉ lấy từ render 3D** (đối chứng render giữ tự động); muốn có phản chiếu thì dựng trong 3D; lệnh AI tấm nền ghi rõ **không vẽ phản chiếu**; phản chiếu AI tự vẽ không được miễn '
 f'(duyệt {DUYET}: K1175-D1 = A).\n'
 '- (b) lớp sống (từ T4): khói bếp và vật bán trong suốt chuyển động ghép bằng **cộng hiệu**: ghép = clip(nền + (render có − render không)) ngoài vùng bảo vệ; không dán nguyên điểm ảnh render; tấm khai `song` (§13.6); K kiểm N2P-1 (e) và mô hình (iv) soi `nen` '
 f'(duyệt {DUYET}: K1175-D4 = A; V3 = a).\n'))
# 4. §15 (c) (iii) chiều nước→đất bằng T9c
a = '(iii) đổi loại vùng T9b ≤ 2 % mỗi chiều và 0 báo của mô hình;'
E.append((a, '(iii) đổi loại vùng: chiều đất→nước T9b ≤ 2 %, chiều nước→đất đo bằng **T9c** (đường bờ đo, đối chứng render — định nghĩa và ngưỡng ở `checks/ll/RULES-LL.md` mục 1.17.5; '
 f'duyệt {DUYET}: K1175-D2 = A), và 0 báo của mô hình;'))
# 5. §15 (d) tiếp — ghi chú cập nhật (chữ cũ giữ để còn lịch sử; tránh mâu thuẫn với (a)(b)(c) mới)
a = 'tới khi K-1.17.5 xong (duyệt 24/10/2026, V1 = d + b, V3 = a, V4 = b, V7 = b; K1174-D1 = A).\n'
E.append((a, a +
 '- (d) cập nhật sau K-1.17.5 (24/10/2026): "phép (iii) giữ T9b ≤ 2 % mỗi chiều" ở dòng trên thay bằng (c) (iii) mới (nước→đất = T9c); phản chiếu theo (b) phản chiếu; khói bếp theo (b) lớp sống; khớp màu cục bộ theo (a) ngoại lệ. '
 f'Mở tấm nền cho cảnh 1666 ban ngày: chưa có quyết định — chờ chủ dự án (V1 giữ tới lúc đó) (duyệt {DUYET}: K1175-D1…D4).\n'))
# 6. §15 (j) theo D5 + D7
a = 'Đạt đủ ba điều kiện thì áp ở bản cuối; tới lúc đó nhà thường thuộc lớp (a) như (a)(b) ở trên. Animatic T4 dựng bằng look V2 (§14.7 Look T4) không chờ vòng thử này (phương án A) (duyệt 24/10/2026 06:21, "A+B theo khuyến nghị").\n'
E.append((a, a +
 '- (j) cập nhật sau K-1.17.5: điều kiện (1) đã có — hàng BE-MAT-NHA (RULES-LL 1.17.5); phép (a) hình khối chưa đạt "bắt 100 %" nên: **AI chỉ phủ nhà ĐO ĐƯỢC** (≥ 2 px/m và ≥ 40 điểm cạnh — chủ yếu khung trung/cận); '
 '**nhà không đo được (nhà xa) giữ render** (khoá (b) của BE-MAT-NHA); **toàn cảnh xa giữ render và nâng bằng 3D** (phương án A) '
 f'(duyệt {DUYET}: K1175-D5 = A + D). Lời nhắc phủ bề mặt nhà dùng bản v2 có **năm bắt buộc** + q_thoi_dai cho phép (c) (duyệt {DUYET}: K1175-D7 = A). '
 'Vẫn **ĐANG THỬ, CHƯA ÁP** tới khi vòng thử THU-B-T4 đạt (điều kiện 2) và chủ dự án duyệt kết quả (điều kiện 3).\n'))
for a, b in E:
    n = s.count(a)
    if n != 1: sys.exit(f'chuỗi gốc xuất hiện {n} lần: {a[:80]}')
    s = s.replace(a, b)
open(P, 'w', encoding='utf-8', newline='').write(s)
print('sau', hashlib.sha256(s.encode()).hexdigest())
