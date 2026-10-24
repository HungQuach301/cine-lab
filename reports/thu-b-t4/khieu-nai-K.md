# Khiếu nại cho phiên K (THU-B-T4 → P chuyển vào `checks-appeal.md`; phiên xưởng không sửa `checks/`, không đọc mã `checks/`)

> Căn cứ: chạy `checks/ll/k2check.py` 1.17.5 (LOCK `c7630b4a…` KHỚP) trên các tấm BE-MAT-NHA của vòng thử. Bằng chứng: `channel-k2/k2c-t4-02/thu-b/kiem/*/k2check.md` (nguyên văn đầu ra + stderr).
> Ghi chú minh bạch: dòng mã trích dưới đây là **traceback Python in ra khi chạy** `q_n2p.py` (không mở tệp mã để đọc).

## KN-1 · N2P-1/2/3/4/5/6 "không chạy được: 'so_doan_lan'" khi khung KHÔNG có nước
- Hiện tượng: tấm M4-trung (2026, mặt phố Fleet St) và B3-p4-1938 (Ludgate Hill) — khung không có điểm nước nào trong mặt nạ lớp. Cả 6 hàng N2P đều "không chạy được: 'so_doan_lan'" (Chặn ở G2). Chạy riêng `q_n2p.py episode.yaml --tl timeline.json` ra traceback: `q_n2p.py, line 276, in tong_tam … sum(c['so_doan_lan'] for c in c9s) … KeyError: 'so_doan_lan'`.
- Tách theo nguyên nhân (BAI-HOC-K2 K48): cùng cách khai, tấm M1-trung (CÓ sông) chạy đủ N2P-3 (T9c: 0 đoạn bờ lấn, giữa nước 0 %). Lỗi chỉ xuất hiện khi một tấm không có nước → bản tóm tắt T9c gộp kết quả không có khoá `so_doan_lan`.
- Đề nghị: T9c trả `so_doan_lan = 0, sau_lon_nhat_px = 0, giua_pct = 0` (hoặc "KHÔNG ÁP — không có nước") cho khung không nước; thêm 1 ca selftest khung không nước.

## KN-2 · N2P-1 (i) tính vùng nhà ĐO ĐƯỢC của tấm `be_mat_nha_ai` là lớp (a) → mọi tấm BMN trượt N2P-1 (a)
- Hiện tượng: M1-trung lượt 1/2 — N2P-1 (a) "lớp (a) sau ghép lệch tối đa 192/255 (l1), 218/255 (l2) ở 566 433 / 566 426 điểm". Số điểm này trùng vùng AI được phép của BE-MAT-NHA: vùng ghép AI = nhà đo được nở 1 px = **27,67 % khung = 573 766 điểm** (`tam/M1-trung/l*/ghep.json`); 566 433 = số điểm trong vùng đó có giá trị khác render (phần còn lại trùng ngẫu nhiên).
- Đo của phiên (ngoài k2check): trong mặt nạ (a) TRỪ lớp `nha_thuong` (215, 215, 215): max |ghép − render| = **0/255** ở cả 3 khung; BE-MAT-NHA (b) của chính k2check: **0/255** ở mọi tấm.
- Thử khai `lop_a` (danh sách lớp (a) không gồm `nha_thuong`, trường có trong RULES 1.17.0): KHÔNG đổi kết quả (`kiem/M1-l1-lopa/`). Phiên không thử thêm cách khai nào khác (không đoán).
- Đề nghị: với tấm `be_mat_nha_ai: true`, N2P-1 (i) loại vùng "nhà đo được nở 1 px" khỏi mặt nạ (a) (vùng đó do BE-MAT-NHA (a)(b) kiểm), giữ (i) cho mọi điểm (a) còn lại — đúng chữ RULES 1.17.5 "BE-MAT-NHA (b) mọi điểm ngoài nhà đo được (nở 1 px) = render 0/255".

## KN-3 · Mô hình nhìn Claude "không đọc đủ ảnh" ngẫu nhiên → (c) THIẾU (Chặn)
- Số lần: B3 lượt 1 (lần chạy 2: đọc 6/10 ảnh), M4-trung lượt 1 và 2, M1-trung lượt 2 — cùng một lời gọi, có lần đọc đủ 10/10 (B3 lượt 2, M1 lượt 1). Chi phí mỗi lần ≈ $0,04–0,07.
- Đúng thiết kế fail-closed (K-1.17.5 §5.2). Đề nghị: tự gọi lại 1 lần khi thiếu ảnh (như Q27/Q31 "sau 1 lần gọi lại"), ghi cả hai lần vào `n2p-cost.jsonl`.

## KN-4 (ghi nhận, không phải lỗi mã) · (a) hình khối KHÔNG bắt vật AI vẽ thêm TRONG bóng nhà
- B3 lượt 1: k2check (a) 0 Chặn, 0 (w); nhưng gpt-6.1-sol báo 10 (w) "thêm ống khói/chụp ống, đổi đầu hồi" và ô phóng (`tam/B3-p4-1938/l1/soi-a.jpg`) thấy ống khói AI vẽ thêm. Đỡ cạnh hình học (biên nhà ∪ mặt phẳng) không giảm khi AI THÊM chi tiết bên trong bóng nhà. Hiện chỉ mô hình nhìn (w) + người đọc bắt được. Đề nghị K xét phép "cạnh màu MỚI không có ở render và pass bóng" trong lòng nhà (như (c) cụm ΔE của N2P-1) — chỉ báo.
