# CHECKPOINT — TIEN-KY-T4 (K2C-T4-02 London)

> Nhánh thật: `k2c-t4-02-tienky` (gốc `origin/main` @9852adf5). Nhánh mặc định của bộ khung `ccr-a4d35b28-j7pwch` KHÔNG dùng (lệnh gọi tên nhánh).

## Trạng thái
- 23/10 ≈ 06:00 UTC: khởi động; verify.sh 10 PASS/5 FAIL → cài npm ci (k2v, cong3), OpenEXR/tifffile/pyshp; hook preflight pre-commit + pre-push đã cài.
- 10:05 UTC: pod T1 TẮT (1,62 h, $1,90; đủ 120 + 120 khung + 2 khung 1080). Kết luận T1: A tốt hơn (Cycles lộ mép miền thể tích ban ngày). Sửa lỗi hạt lửa trên sông (page.js) → hàng E dựng lại T1 A (PGID 5107). T3 v2: máy giải 9 điểm + uốn tranh lên mặt đông (PGID 6418 đang dựng). Báo cáo + tờ so + phiếu G1 (D1–D18) đang hoàn thiện.

## Lệnh bổ sung nhận được
- (chưa có)

## Nhật ký
- 06:55 UTC: tư liệu 12 mục tải + bằng chứng (JSON nguyên văn nơi giữ, chụp trang Rijks/Commons; trang Met/YCBA/LoC/NGA chặn trình duyệt → bằng chứng = API/manifest JSON); Leake (TAMU IIIF) bị Cloudflare chặn 403 → dùng Doornick 1666 (Rijks PDM). Khớp Doornick ↔ OSM 13 điểm: affine RMS 44,2 m (LOO 58,8 m). Ranh cháy cuối từ Doornick: TPS 161,9 ha = 399 acre. OSM 2026 + LiDAR EA DTM/DSM 1 m tải xong (ngoài git, lệnh tái tạo trong scripts/k2ldn).
- 07:40 UTC: dựng hình học London (scripts/k2ldn/hinh_hoc.py: 60 552 nhà 1666, 14 540 trong vùng cháy, 17 815 toà 2026, 1,72 tr tam giác) + trang dựng three.js design/k2v/ldn/page.js (lửa/khói billboard + bản đồ ánh lửa) — khung thử 1280×720 ≈ 4,8 s/khung spp 2. LỜI NHÁP v1 1 593 từ (86 câu, 22 mục [cần kiểm]); DU-KIEN-MOI N1–N25.
- 08:05 UTC: T1 (i) cách A xong 2 × 120 khung 1280×720 (ngày 6,44 s/khung, đêm 5,32 s/khung, spp 4; lửa/khói = atlas thể tích nướng sẵn bằng mô phỏng numpy — Mantaflow trong bpy lỗi 2/2 lần). Cycles thử CPU: hình học/máy khớp; pod RTX 5090 `v4oswun6979dgd` BẬT 08:04 cho T1 (ii) (đo thử 2 s rồi mới chạy hết). Hàng dựng A (PGID 16284): T5 ảnh đầu, T6 tấm + mặt nạ, T2, T3, T4, T6 timelapse.
- 09:15 UTC: T4 xong (4 đoạn, đo t4-may.json); T6 3 lượt OpenAI ($0,23): lượt 1–2 (iii) trượt (màu nước / dải biển giả ở chân trời cảnh dựng — đã sửa cảnh), lượt 3 trượt nặng (đổi vùng 20 %) → 0/3 đạt máy; ghép timelapse 6 s trên tấm lượt 2 (nhấp nháy (c) 0,078 so render 2,42). T5 Omni lượt 1 ĐẠT máy ($1,02). T1 Cycles: hộp thể tích theo ô ≈ 3 phút/khung → đổi sang miền thể tích duy nhất (bản đồ giờ bén lửa) 12,4 s/khung 960×540 spp 32; pod đang dựng hết. T2/T3 đang dựng lại (lỗi xoay máy thiên đỉnh; PnP tranh Hollar). RIGHTS-NHAP viết.
- 09:40 UTC: PHIEU-G1 nháp; tờ so T1 (scripts/k2ldn/t1_so.sh); xem/T6-timelapse-n2p.mp4 640×360. Ghi nhận kiểm T5: ảnh đầu đọc như hoàng hôn (không ra 01:00 đêm) + một khối toà OSM sáng (năm bắt đầu sai) — đã kẹp ≥ 1667,5 trong hinh_hoc.py.
- 10:05 UTC: báo cáo nháp, tờ so, UOC cập nhật số đo Cycles 1080p (ngày 45,6 s, đêm 15,3 s); T1 lỗi lửa trên sông sửa; T3 v2 (t3_may.py)
