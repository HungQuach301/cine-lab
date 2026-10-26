# CHECKPOINT — BAN-CUOI-T4-B1 (K2C-T4-02 bản cuối, phần B1: sửa 3D chung D-A4 + dựng 1080p HỒI 1 + HỒI 3 + H3-05c)

> Nhánh thật: `claude/k2c-t4-02-final-b1-t9ekhx` (harness buộc; lệnh ghi `k2c-t4-02-final-b1`). Gốc origin/main @5453a8b2 (khớp lệnh).
> Căn cứ: chủ dự án 26/10/2026 10:08 "Duyệt PHIẾU-A theo khuyến nghị điều phối" (D-A1…D-A9); **D-B1** = chủ dự án dán lệnh phiên này — giờ dán (giờ tạo phiên) ghi ở báo cáo §0.

## Trạng thái
- 03:44 UTC (10:44 Asia/Saigon): khởi động; origin/main = 5453a8b2 (khớp). verify.sh 10 PASS / 5 FAIL → cài OpenEXR, tifffile, pyshp, npm ci (k2v, cong3), pyproj 3.8.0 + OSTN15 (SHA 5d6ed64d… KHỚP). Hook pre-commit + pre-push → tools/preflight.sh (LFS: `git lfs push` trước `git push`, K33).
- 03:50: tái tạo dữ liệu LDN `scripts/k2ldn/anim/du_lieu.sh` nền PGID 1422 (NAM 1666.6 1667.3 1700.5 1711.5 1938.5 1940.98 1955.5 1975.5 2026.7), log /var/tmp/bc/log/du_lieu.log.
- D-B1: thêm mẫu `channel-k2/k2c-t4-02/ban-cuoi/dung/*-1080p.mp4` vào tools/lfs-allow.txt + .gitattributes.

## Lệnh bổ sung đã áp
- (chưa có)
- 04:00: dừng du_lieu.sh sau bước flipbook (bước hình học look2 + nướng look2 không dùng ở B1) → hình học B1 `scripts/k2ldn/bc/hinh_hoc_b1.py` (THU-B d + sửa niên đại toà OSM, Q-A5) nền PID 3352; nướng look3d 10 mốc `scripts/k2ldn/bc/nuong_b1.sh` nền PGID 3742 (chờ hình học).
- 04:10: trang dựng B1 `design/k2v/ldn/bc/look3-b1.js` sinh bằng `scripts/k2ldn/bc/tao_look3_b1.py` (look3 + D-A4 (i)–(iv)); máy + danh sách việc `scripts/k2ldn/bc/may_b1.py` → `channel-k2/k2c-t4-02/ban-cuoi/may/b1/` (HỒI 1: 19 việc 3 547 khung; HỒI 3: 7 việc 1 127 khung; M00 VONG; H3-05c thử 3 phương án; MAY-19 H2-10/H5-05b; soi năm biên 10 máy 24 khung).
- 04:10–04:16: hình học B1 xong (4 618 074 tam giác; 327 toà đổi năm, 182 khối tiền nhiệm hậu chiến); nướng look3d 10 mốc xong (≈ 30 s/mốc).
- 04:11–04:15: thử M00 960×540 (trang cũ ↔ B1): mặt sông hết mảng cát phẳng, vòng lửa liền; tăng phản chiếu lửa trên nước (Fq) → thử lại; M01: hết đốm elip đen (sà lan 2026).
- 04:16: lượt kiểm 1080p (mẫu sau sửa + H3-05c 3 phương án + soi năm biên 24 khung + mặt nạ 2) nền PGID 5662.
- Phát hiện: BANG_NAM ghi năm HOÀN THÀNH nhưng lớp 4 mọc 2,5 năm → sửa hinh_hoc_b1.py (năm xuất hiện = hoàn thành − 2,5); dựng lại hình học trước ảnh đầu Omni (vi). HỒI 1/HỒI 3 (≤ 1938) không đổi.
- 04:47: (vi) phát hiện quy tắc (c) gán nhầm năm cho công trình lịch sử có tên (nhà thờ St Giles/St Alban/St Botolph, hội quán phường hội) → sửa hinh_hoc_b1.py (loại trừ + bảng năm hội quán). HỒI 1/HỒI 3 không đổi; dựng lại hình học + ảnh đầu Omni H5-02b/H5-02s dời sang SAU khi dựng sản xuất (không chạy chồng vòng nặng).
- 05:12 UTC dựng xong **H1-02h**: 48 khung (f 0..47), 23.04 s/khung/tiến trình (P = 2), 9 MB, SHA `8a705c9ff61842f8…` → LFS + đẩy
- 05:14: H1-02h dựng + LFS đẩy THÀNH CÔNG (Uploading LFS objects 1/1, 8,5 MB; tải công khai media.githubusercontent.com SHA khớp) nhưng bước kiểm `git lfs ls-files | grep -q` trả lỗi giả do `pipefail` + SIGPIPE → hàng dừng đúng thiết kế; sửa xong_b1.sh (lưu đầu ra trước khi grep), chạy tiếp sản xuất.
- 05:15: trang look3-b1 đổi LỊCH vỏ vòm (1707,3 → 1708,0) + đèn lồng (1707,95 → 1708,0) sau soi lại H2-09 1707,86 (q_thoi_dai vẫn đọc vòm hoàn chỉnh). Chỉ đổi khung năm 1705–1708 → không ảnh hưởng shot HỒI 1/HỒI 3 đang dựng.
- 05:41 UTC nhịp: 1 tệp 1080p đã đẩy LFS; đang dựng: H1-01h 51 khung; H1-03 76 khung; ; RAM trống 4693 MB, đĩa trống 13G
- 05:50 UTC dựng xong **H1-01h**: 72 khung (f 0..71), 29.61 s/khung/tiến trình (P = 2), 12 MB, SHA `d19fbc571d647c68…` → LFS + đẩy
- 05:51 UTC: H1-01h xong 29,6 s/khung/tiến trình (đêm, fov 50°, máy P8 120 m) — nặng hơn mẫu ngày phiên A (14–19 s). Ước lại thông lượng HỒI 1 đêm ≈ 11–12 s/khung (P = 2) → dựng B1 ≈ 14–15 h máy (> 12 h dự kiến); tiếp tục dựng đủ (chất lượng trước), báo vượt giờ ở báo cáo.
- 06:06 UTC nhịp: 2 tệp 1080p đã đẩy LFS; đang dựng: H1-03 153 khung; H1-04 37 khung; ; RAM trống 4975 MB, đĩa trống 13G
- 06:31 UTC nhịp: 2 tệp 1080p đã đẩy LFS; đang dựng: H1-03 228 khung; H1-04 101 khung; ; RAM trống 4931 MB, đĩa trống 13G
- 06:56 UTC nhịp: 2 tệp 1080p đã đẩy LFS; đang dựng: H1-03 304 khung; H1-04 164 khung; ; RAM trống 4960 MB, đĩa trống 13G
- 07:21 UTC nhịp: 2 tệp 1080p đã đẩy LFS; đang dựng: H1-03 378 khung; H1-04 227 khung; ; RAM trống 4892 MB, đĩa trống 13G
- 07:22 UTC dựng xong **H1-03**: 381 khung (f 0..380), 19.97 s/khung/tiến trình (P = 2), 80 MB, SHA `aedd457e707b3702…` → LFS + đẩy
- 07:31 UTC dựng xong **H1-04**: 254 khung (f 0..253), 23.66 s/khung/tiến trình (P = 2), 55 MB, SHA `2bc3ac580acfc4df…` → LFS + đẩy
- 07:45 UTC dựng xong **H1-05h**: 48 khung (f 0..47), 27.26 s/khung/tiến trình (P = 2), 11 MB, SHA `111018185915fc08…` → LFS + đẩy
- 07:46 UTC nhịp: 5 tệp 1080p đã đẩy LFS; đang dựng: H1-06 39 khung; H1-07 1 khung; ; RAM trống 5431 MB, đĩa trống 13G
- 08:11 UTC nhịp: 5 tệp 1080p đã đẩy LFS; đang dựng: H1-06 106 khung; H1-07 75 khung; ; RAM trống 4936 MB, đĩa trống 13G
- 08:36 UTC nhịp: 5 tệp 1080p đã đẩy LFS; đang dựng: H1-06 176 khung; H1-07 150 khung; ; RAM trống 4839 MB, đĩa trống 13G
- 09:01 UTC nhịp: 5 tệp 1080p đã đẩy LFS; đang dựng: H1-06 243 khung; H1-07 220 khung; ; RAM trống 4899 MB, đĩa trống 13G
- 09:04 UTC dựng xong **H1-07**: 227 khung (f 0..226), 20.74 s/khung/tiến trình (P = 2), 45 MB, SHA `3c419fcf12e8019c…` → LFS + đẩy
- 09:26 UTC nhịp: 6 tệp 1080p đã đẩy LFS; đang dựng: H1-08b 60 khung; ; RAM trống 4741 MB, đĩa trống 12G
- 09:31 UTC dựng xong **H1-06**: 324 khung (f 0..323), 21.9 s/khung/tiến trình (P = 2), 67 MB, SHA `399ea8bd4bafdb14…` → LFS + đẩy
- 09:51 UTC nhịp: 7 tệp 1080p đã đẩy LFS; đang dựng: H1-08b 134 khung; H1-09 44 khung; ; RAM trống 5120 MB, đĩa trống 12G
- 10:17 UTC nhịp: 7 tệp 1080p đã đẩy LFS; đang dựng: H1-08b 210 khung; H1-09 101 khung; ; RAM trống 4967 MB, đĩa trống 12G
