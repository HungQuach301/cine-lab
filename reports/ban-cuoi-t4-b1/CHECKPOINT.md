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
