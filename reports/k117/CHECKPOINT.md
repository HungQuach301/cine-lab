# K-1.17 — CHECKPOINT
- Nhánh: `checks-1-17` từ `origin/main` @ `bc7e96d1`.
- 14:40 UTC: đã đọc NC-N2P (§2, §6, mã `reports/nc-n2p/ma/`, đáp án), ANIMATIC-T3 §8.3 + log-shot, V7C-D5, RULES-LL 1.16.1, Kinh thánh §13.6/§14.1. Kinh thánh §14.7 và §15 **chưa có trên nhánh nào** (đã quét mọi nhánh origin) → làm theo nội dung trong lệnh.
- Đang làm: dựng lại k2check 1.16.1 trên animatic T3 (timeline dựng từ đặc tả, `reports/k117/do/tl_tu_dac_ta.py`) để phân loại 8 hàng Chặn; tiếp theo: `checks/ll/q_n2p.py`, `q_k117.py`, selftest.
- Chưa sửa `checks/`. LOCK vẫn 1.16.1.
- 14:47 UTC: mã 1.17 đang viết (bản vá việc dở `reports/k117/wip/checks-wip.patch`, áp bằng `git apply`): `q_n2p.py` + `q_n2p_vision.py` + `data/cam_thoi_dai.json` (N2P-1…6), `q_k117.py` (MINH-HOA, EO-DAT-R1…R3), sửa Q33 (miễn năm khác — TL-1), ML1 (`cau: ""`), NC-H1 (lớp nhà tl/* — V7C-D5), SACH-1 (nhãn Illustration), cap112, k2check. Tái hiện k2check 1.16.1 trên animatic T3: 11 hàng TRƯỢT khớp báo cáo animatic (Q33 cần bản xem ghép 8 chương). Chưa chạy selftest, chưa khoá.
