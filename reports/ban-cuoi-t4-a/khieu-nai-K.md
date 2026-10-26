# Khiếu nại / đề xuất gửi phiên K — BAN-CUOI-T4-A (26/10/2026)

> Phiên xưởng không đọc mã `checks/`, chỉ CHẠY `checks/ll/k2check.py`, `q_thoi_dai.py`, `lock.py --verify` (LOCK 1.17.8 `045b7bb7…` KHỚP mọi commit). Phiên P chuyển các mục dưới vào `checks-appeal.md` nếu thấy đúng. Không mục nào xin nới ngưỡng do chủ dự án đặt.

## KN-1 · K1178-D2 — báo "bờ sông bị vẽ lại" của mô hình trên tấm E (đề xuất `ngoai_le`)
- **Tái hiện:** `channel-k2/k2c-t4-02/ban-cuoi/e/kiem/E-P9-ngay-l1-thap/k2check.md` — N2P-1 (b) "BỚT/ĐỔI vật lớp (a)-E — gpt: cong_trinh «At the extreme lower-left edge, the projecting dark quay or pier surface…» @[0.0, 0.972, 0.078, 1.0] dải (a)" và N2P-3 (b) "gpt báo đổi loại vùng «Apparent land/pier-to-water conversion at the extreme lower-left corner…»" → 2 lỗi Chặn (G2).
- **Số đo máy cùng tấm:** N2P-1 (a) lệch lớp (a) **0/255**; T9b **0,00 %**; T9c **0 đoạn bờ lấn, sâu 0,0 px**, giữa nước ≤ 0,0 %. Cùng ảnh AI với mặt nạ "đủ" (`E-P9-ngay-l1`): mô hình **không** báo (góc đó thuộc toà có tên → giữ render).
- **Soi bằng mắt** (ô phóng ×2 trong `reports/ban-cuoi-t4-a/e/so-E-P9-ngay-l1-thap.jpg`, ô dưới trái; khung `/var/tmp/bc/soi1.jpg` ghi ở báo cáo): ngoài dải bờ ±8 px, AI vẽ mép kè + mặt nước nâu ở dải ≈ 10 × 190 px sát mép dưới khung (0,09 % khung) nơi render là mặt kè/nhà xám. Đây là **thay đổi thật nhưng nằm ngoài lớp (a)-E** (dải bờ ±8 px và mặt nước render giữ 0/255).
- **Đề xuất:** tấm này khai `ngoai_le: {hang: [N2P-1 (b), N2P-3 (b)], ly_do: "K1178-D2 — vùng ngoài dải bờ 8 px, máy 0/255 + T9b/T9c 0", nguoi_ky: chu_du_an}` **chỉ khi chủ dự án duyệt E1** (phiếu A). Khuyến nghị K1178-D2 phương án B ở phiên K kế: (b) của mô hình trên tấm E chỉ Chặn khi hộp chạm lõi (a)-E.

## KN-2 · Q37 / NHIP-K2 / Q37 (1.13) — beats khai không được nhận, biến cố đo T4 không cộng (D4)
- **Tái hiện:** `ban-cuoi/dac-ta-v4/k2check-1.17.8-dac-ta-v4.md` — Q37 TRƯỢT: biến cố khai 143 (gộp 134), **TB 5,75 s > 3,5 s**, dài nhất **20,17 s** (H2-03b, DAY timelapse 1667.05 → 1667.45). Lượt đầu tôi khai beats `bien_co_tl` mỗi 4 s cho shot timelapse có thời gian chạy → (a) "không khớp mốc nào trong đặc tả (±0,3 s)" (đúng RULES 1.17.7 A4: beats tự do không được nhận) → đã bỏ.
- **Vấn đề:** T4 BIEN-CO-V chưa hiệu chuẩn (K1178 §5) nên biến cố thấy được của timelapse (nắng, lửa lan, nhà mọc) không có đường khai nào được nhận ngoài `lop_chong` và ranh shot. Muốn đạt Q37 phải thêm cắt góc / lớp chồng — tức là thêm phần tử chủ yếu để vượt chỉ số (luật cứng CLAUDE.md).
- **Đề xuất:** (A) K hiệu chuẩn lại BIEN-CO-V trên bản 1080p của phiên B (đủ bitrate + log máy tách thị sai — K1178-D4); hoặc (B) nhận `beats` loại `bien_co_tl` khi có neo log máy (`thoi_gian` của shot đổi ≥ ngưỡng giữa hai mốc). Phiên này không thêm cắt/lớp chồng để vượt Q37.

## KN-3 · TU-LIEU-OMNI đọc ranh shot gộp, bỏ qua `tu_lieu_lan` đã khai
- **Tái hiện:** cùng tệp, TU-LIEU-OMNI (b) "H1-06 (125.9–145.4 s) ↔ clip M-d H1-06b … (không khai tu_lieu_lan: lần tư liệu tính phủ cả shot)". Trong `dac-ta-v4/log-shot.json`: H1-06 **125,8747–139,3747 s**, `tu_lieu_lan: [{t0: 126.875, t1: 130.475, lop: THE}]`; H1-06x (M-d) 139,3747–145,3747. Khoảng 125,9–145,4 = H1-06 + H1-06x (ranh v3). Tương tự H1-09 (MAP/MAP3D khai), H1-11, H3-05, H4-02.
- **Đề xuất:** K kiểm hàm đọc ranh shot (có thể gộp segment theo nhóm lời) và cách nhận `tu_lieu_lan` với lớp MAP/MAP3D/THE. Cảnh báo ở animatic — không chặn phiên này.

## KN-4 · NHAN-VAT-TEN — YuNet báo "mặt" trên trời/tán cây
- **Đo của phiên** (chỉ dùng tệp mô hình `checks/models/face_detection_yunet_2023mar.onnx`, không đọc mã): H1-15b-l1-360p (168 khung) — hộp > 1/8 cao ở khung 71 (0,265; điểm 0,62), 113–139 (0,148–0,206; điểm 0,60–**0,78**). Soi khung 50/71/124: mọi hộp nằm trên **trời/tán cây phía trên tường vườn**; mặt hai người thật ≈ 3 % khung.
- **Đã làm theo A1** (chủ dự án 26/10 00:12 duyệt phiếu v2 theo khuyến nghị — "cắt khung mặt > 1/8"): bảng v4 dùng khung 0–110 (4,625 s).
- **Đề xuất:** hiệu chuẩn thêm ca báo nhầm nền (hộp không giao vùng người) hoặc (w) cho hộp mà mô hình nhìn không xác nhận là mặt người.

## KN-5 · LUẬT E (f) — "toà có tên OSM" gồm cả tên cửa hàng/văn phòng thấp
- **Số đo:** mặt nạ đủ (mọi toà OSM có `name`): P9 **151** toà, lớp (a)-E **13,96 %** khung; P1 **247** toà, **38,16 %**. Phần lớn là tên điểm (Superdrug, H&M, Wasabi, Pret…) gắn vào toà thấp. Kết quả: tấm ghép loang lổ 3D ↔ AI (tờ so `reports/ban-cuoi-t4-a/e/so-*-l1.jpg`).
- Biến thể "tháp" (đỉnh ≥ 75 m ODN + Guildhall, Royal Exchange, Bank of England, Mansion House, Tower of St Mary Somerset): P9 10 toà / (a)-E **5,74 %**; P1 17 toà / **28,36 %** — đúng chữ §15 (k) "toà THÁP có tên".
- **Đề xuất:** K định nghĩa "toà có tên" cho LUẬT E (ngưỡng cao hoặc danh mục công trình mốc) — chờ chủ dự án chọn ở E1 (phiếu A). Phiên này nộp cả hai, kiểm cả hai.

## KN-6 · Đề xuất ngoài luật (lệnh việc 1 (d)) — đẩy máy 2D chậm trên tấm E
- Luật 1.17.8 chỉ cho chuyển động của lớp (a)-E ghép lại từ 3D + nhấp nháy N2P-5. Đề xuất: cho phép **đẩy/trượt 2D ≤ 1,5 %/s** trên tấm E (như ảnh thật §19 (c) cập nhật 25/10 mục (3)) với điều kiện lớp (a)-E dựng 3D cùng quỹ đạo máy. **KHÔNG dùng** trong bảng v4 (H5-05a giữ CODINH tĩnh). Ứng viên nếu duyệt: M01 (P1 2026 chiều, DAY), H5-05a.

## Ghi chú (không khiếu nại)
- N2P-6 TRƯỢT trên các episode thử 1 tấm (100 % AI trong 3 s tổng hợp) — do khuôn thử, không phải tập.
- K-LAI-3 THIẾU 27 trên đặc tả v4: tệp `*-kiem.json` / `*-kiem-moc.json` khai trong `animatic2/log-shot.json` (v3) **không có trong git** (`channel-k2/.gitignore *.json`) — lỗi khai kế thừa; phiên B sinh lại từ `qtd-moc-*.json` (không gọi mô hình) và `git add -f`.
