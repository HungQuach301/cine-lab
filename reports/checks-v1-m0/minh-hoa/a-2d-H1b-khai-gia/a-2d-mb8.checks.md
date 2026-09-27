# Báo cáo kiểm L1 — a-2d-mb8.mp4

- Kết luận: **TRƯỢT**
- Profile: `shot` · Công cụ: cinecheck 1.0.0 · Thời điểm (UTC): 2026-09-27T01:32:24Z
- LOCK: khớp (`b86c5d75f14abe5cba7b08c58c95c36e0c1fc49f73af030357f9cc95db7268f8`)
- Đếm: ĐẠT 1, TRƯỢT 1

| Mã | Luật | Cấp | Kết quả | Số đo chính |
|---|---|---|---|---|
| H1 | Không chuyển động tuyến tính ở bộ phận nhân vật | Chặn | **ĐẠT** | đoạn tuyến tính ở bộ phận nhân vật = 0 đoạn (ngưỡng <= 0); kênh 'mechanical' thiếu lý do = 0 kênh (ngưỡng <= 0); kênh có lớp không hợp lệ = 0 kênh (ngưỡng <= 0) |
| H1b | Chuyển động khai báo khớp hình render (luồng quang học ở vùng nhân vật) | Chặn | **TRƯỢT** | nhân vật có kênh bộ phận nhưng không có screen track = 0 nhân vật (ngưỡng <= 0); tỷ lệ cặp khung khớp luồng quang học, track tệ nhất = 0 % (ngưỡng >= 90) ✗; track không đo được cặp khung nào (toàn null/ngoài khung) = 0 track (ngưỡng <= 0) |

## Chỉ số nằm trong ±5% quanh ngưỡng
- Không có.

## Chi tiết từng luật

### H1 — Không chuyển động tuyến tính ở bộ phận nhân vật (4.H — Hoạt hình, cấp Chặn): ĐẠT
- Định nghĩa đo: Dữ liệu chuyển động bake theo từng khung xuất từ phần mềm dựng (không phải khoá khai báo). Với mỗi kênh lớp 'character_part': tốc độ = chuẩn hiệu giá trị giữa 2 khung kề; đang chuyển động khi tốc độ > 2% tốc độ lớn nhất của kênh. Đoạn tuyến tính = chuỗi bước liên tiếp có mọi tốc độ trong ±3% trung bình chuỗi, và (a) dài ≥ 8 bước và bắt đầu ngay sau hoặc kết thúc ngay trước một lần đứng yên (khởi/dừng không easing), hoặc (b) dài ≥ 24 bước ở bất kỳ đâu.
- Ngưỡng: 0 đoạn tuyến tính ở kênh bộ phận nhân vật. Kênh 'mechanical' được miễn nhưng phải có lý do và được liệt kê trong báo cáo.
- Bằng chứng: `{"kenh_kiem": 7, "kenh_mien": [{"id": "lamplighter/root.loc", "lop": "character_root", "ly_do": ""}]}`

### H1b — Chuyển động khai báo khớp hình render (luồng quang học ở vùng nhân vật) (4.H — Hoạt hình, cấp Chặn): TRƯỢT
- Định nghĩa đo: <video>.motion.json phải có 'screen_tracks': toạ độ điểm ảnh từng khung của khớp nhân vật, chiếu từ rig bake qua máy quay render (null khi bị che). Luồng quang học DIS (OpenCV, preset medium, tính ở ≤ 1280 px rộng) giữa khung n và n+1 của file render; tại mỗi điểm lấy trung vị luồng trong đĩa bán kính 4 px. Cặp khung khớp khi |luồng − (p(n+1) − p(n))| ≤ max(1,5 px, 25% độ dài dịch chuyển). Tối đa 480 cặp khung rải đều.
- Ngưỡng: Mọi nhân vật có kênh 'character_part' có ≥ 1 screen track; mỗi track khớp ở ≥ 90% cặp khung đo (nội bộ).
- Ghi chú: 2 track, 158 cặp khung đo. Khớp khi |luồng − khai báo| ≤ max(1.5 px, 25% × độ dài dịch chuyển).
- Bằng chứng: `{"theo_track": {"lamplighter/head": {"cap_khung": 158, "khop_pct": 0.0, "epe_trung_vi": 10.06, "lech_lon_nhat": {"khung": 186, "epe": 25.7, "khai": [8.96, 0.68], "luong": [-2.9, -22.12]}}, "lamplighter/chest": {"cap_khung": 158, "khop_pct": 0.0, "epe_trung_vi": 10.05, "lech_lon_nhat": {"khung": 225, "epe": 18.61, "khai": [8.96, 0.1], "luong": [-1.04, -15.6]}}}}`
