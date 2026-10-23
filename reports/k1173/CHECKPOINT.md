# CHECKPOINT — phiên K-1.17.3 (nhánh `checks-1-17-3`, gốc origin/main @9852adf5, LOCK 1.17.2 aca05e60…)

| Giờ UTC | Việc | Trạng thái |
|---|---|---|
| 06:10 | Đọc khiếu nại A1–A6 (`reports/ban-cuoi-t3/checks-appeal.md`), BAN-CUOI §9/§14, k2check-1.17.2-cap-l3, K117 §4/§10, K1171 §10, K1172 §6, Kinh thánh §12.1, §13, §14.7, §17, §18, AUTHORSHIP 19–23/10 | xong |
| 06:20 | Tái hiện mã: A1 `q_k116.tl3` ép `float()`; A2 `q_nhip.spec_times` không đọc `opt.time`/cửa sổ năm cảnh tl (thử: 207 → 76 lỗi (a)); A3 `q_k117` R3 (b) không đếm `goc_may`; A5 `q33_mien` dùng bao năm log [min, max] (N1_6 nhảy năm 1705 → 1727 → 2026); A6 `sach1` chỉ nhận chữ thẻ theo tên vai | xong |
| 06:26 | Cài hook pre-commit + pre-push (preflight, `set -o pipefail`) | xong |
| — | Sửa luật + selftest_k1173 + chạy k2check 1.17.2 ↔ 1.17.3 + bảng QUYET-DINH-TREO + khoá | đang làm |
| 06:47 | Mã 1.17.3 (A1 TL-3, A2 Q37 (a) mốc tl, A3 R3 (b) + ngoại lệ (a) có khai, A5 Q33 năm hiện, A6 SACH-1 thẻ theo đặc tả) + `selftest_k1173.py` 42/42 + fixtures; selftest cũ k112 75/75 · k1121 48/48 · k1122 37/37 · k113 64/64 · k114 126/126 · k115 105/105 · k116 144/144 · k117 130/130 · k1172 74/74 · k2 129/129 · ll 317/317. Mã chưa khoá → đẩy dạng bản vá `reports/k1173/wip/checks-1173-wip.patch` (checks/ cất bằng stash khi commit). `checks-appeal.md` mục phán quyết + `QUYET-DINH-TREO.md` bản nháp | xong |
| 06:47 | k2check 1.17.2 trên đầu vào bản cuối T3 (master thật SHA 5b9f0bcc…, timeline tổng hợp từ đặc tả, log chữ tổng hợp) xong (10 m 39 s); 1.17.3 kế tiếp | đang làm |
| 06:58 | `lock.py` (không `--verify`, một lần) → 1.17.3 `d99af8f2…`; `--verify` KHỚP; commit mã + đẩy 07:00 | xong |
| 07:11 | Trên cây đã khoá: selftest k112…k1173, k2, ll đạt hết; k2check 1.17.3 cuối (LOCK KHỚP) — so 1.17.2: 9 hàng đổi, 44/53 giống hệt | xong |
| 07:14 | Báo cáo `K1173-BAO-CAO.md`, `QUYET-DINH-TREO.md` (14 còn cần + 3 hết hiệu lực), `do/` | xong — DỪNG chờ chủ dự án |
