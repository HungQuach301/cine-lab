# Báo cáo kiểm L1 — SO-SANH-PHONG-CACH.mp4

- Kết luận: **TRƯỢT**
- Profile: `shot` · Công cụ: cinecheck 1.0.0 · Thời điểm (UTC): 2026-09-27T01:31:59Z
- LOCK: khớp (`b86c5d75f14abe5cba7b08c58c95c36e0c1fc49f73af030357f9cc95db7268f8`)
- Đếm: TRƯỢT 1

| Mã | Luật | Cấp | Kết quả | Số đo chính |
|---|---|---|---|---|
| P0 | Máy dò chữ độc lập: mọi chữ trong hình phải có matte | Chặn | **TRƯỢT** | vùng chữ dò được không có matte = 84 vùng·khung (ngưỡng <= 0) ✗ |

## Chỉ số nằm trong ±5% quanh ngưỡng
- Không có.

## Chi tiết từng luật

### P0 — Máy dò chữ độc lập: mọi chữ trong hình phải có matte (4.P — Chữ, tiêu đề, phụ đề, cấp Chặn): TRƯỢT
- Định nghĩa đo: Lấy mẫu 2 khung/giây (tối đa 240 khung) từ file render. Máy dò PP-OCRv4 det (DB, ONNX ghim SHA trong checks/models/) tìm vùng nghi là chữ (điểm hộp ≥ 0,6); mô hình nhận dạng PP-OCRv4 rec đọc từng vùng, chỉ giữ vùng đọc ra ≥ 2 ký tự Latin/số, chiếm ≥ 60% ký tự, độ tin ≥ 0,8, và độ đặc nét < 0,85 (trung vị diện tích/hộp bao của các thành phần sau ngưỡng Otsu; ký tự đo được 0,4–0,7, ô cửa sổ ≈ 1,0) — loại cửa sổ, lưới, hoa văn. Vùng có matte = ≥ 50% diện tích hộp nằm trong nét matte (alpha ≥ 0,02) của các phần tử đang hiện ở khung đó, nới 0,35 × chiều cao hộp. Không cần matte để chạy: thiếu thư mục chữ thì mọi chữ dò được đều trượt.
- Ngưỡng: 0 vùng chữ dò được mà không có matte (ngưỡng hộp 0,6, độ tin 0,8, độ đặc 0,85, độ phủ 50%: nội bộ).
- Ghi chú: Lấy mẫu 21 khung (≈ 2 khung/giây). Vùng máy dò nghi là chữ nhưng nhận dạng không xác nhận chữ Latin (cửa sổ, lưới, hoa văn): 0 (bỏ qua).
- Ghi chú: Không có matte chữ (thiếu <video>.text/ hoặc elements rỗng): mọi chữ dò được đều trượt.
- Bằng chứng: `{"chu_khong_matte": [{"khung": 0, "hop": [15, 13, 463, 43], "chu": "(a) 2D Canvas - blur 8 mau - 42 s/s", "do_tin": 0.99, "phu_matte": 0.0}, {"khung": 0, "hop": [975, 12, 1386, 44], "chu": "(b) three.js - blur 8 mau - 45 s/s", "do_tin": 0.98, "phu_matte": 0.0}, {"khung": 0, "hop": [15, 553, 600, 582], "chu": "(c1) Blender Workbench - khong blur - 43 s/s", "do_tin": 0.98, "phu_matte": 0.0}, {"khung": 0, "hop": [976, 553, 1528, 582], "chu": "(c2) Blender EEVEE - chi 1 s (4-5 s) - 408 s/s", "do_tin": 0.99, "phu_matte": 0.0}, {"khung": 12, "hop": [15, 13, 463, 43], "chu": "(a) 2D Canvas - blur 8 mau - 42 s/s", "do_tin": 0.99, "phu_matte": 0.0}, {"khung": 12, "hop": [974, 12, 1386, 44], "chu": "(b) three.js - blur 8 mau - 45 s/s", "do_tin": 0.98, "phu_matte": 0.0}, {"khung": 12, "hop": [16, 553, 600, 582], "chu": "(c1) Blender Workbench - khong blur - 43 s/s", "do_tin": 0.99, "phu_matte": 0.0}, {"khung": 12, "hop": [976, 553, 1528, 582], "chu": "(c2) Blender EEVEE - chi 1 s (4-5 s) - 408 s/s", "do_tin": 0.99, "phu_matte": 0.0}, {"khung": 24, "hop": [15, 13, 463, 43], "chu": "(a) 2D Canvas - blur 8 mau - 42 s/s", "do_tin": 0.99, "phu_matte": 0.0}, {"khung": 24, "hop": [974, 12, 1386, 44], "chu": "(b) three.js - blur 8 mau - 45 s/s", "do_tin": 0.98, "phu_matte": 0.0}, {"khung": 24, "hop": [15, 553, 601, 582], "chu": "(c1) Blender Workbench - khong blur - 43 s/s", "do_tin": 0.97, "phu_matte": 0.0}, {"khung": 24, "hop": [976, 553, 1528, 582], "chu": "(c2) Blender EEVEE - chi 1 s (4-5 `
