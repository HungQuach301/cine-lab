# BAN-CUOI-T4-B2a — CHECKPOINT

**Nhánh thật:** `claude/adoring-wright-i76iay` (harness buộc; lệnh ghi `k2c-t4-02-final-b2a`). Gốc B1 @6f6c2636 + merge origin/main @75e94b98 (commit 64a304ee, LOCK 1.17.9 `9eddaf24…` KHỚP).

## Trạng thái
- 01:43 dữ liệu nền xong (18 phút; SHA `reports/ban-cuoi-t4-b2a/SHA-du-lieu-ngoai-git.txt`; OSM API sống → khác SHA B1, đã ghim `ban-cuoi/may/b2a/osm2026-b2a.json.gz` + `thuyen-b2a.json`).
- Việc 1 xong phần máy: M00 kp 0 (165 → 155 m), H1-01h kp 1 (160 m); k2check 1.17.9 v5b GOC-CAO ĐẠT 0 (a). H1-01h 1080p đã LFS (02:18).
- Tấm E-M01 (2304×1296, look3-b1) + ghép bo_dat + che bóng cầu AI xong; k2check (a) máy: N2P-E chỉ Chặn (u) (chưa duyệt tấm).
- Soi năm biên lượt 1 → lỗi phế tích (khối đen trơn đọc thành toà hiện đại) → sửa `tao_look3_b1.py` (chỉ năm 1666,69–1700) → đang soi lượt 2.
- Hàng dựng: hàng chính PGID 11487 (M00 đang chạy, thoát sau M00 vì cờ dừng tạm 02:03); hàng phụ PGID 16973 P = 1 (M01 → E-M01-tl). Còn lại (M02…H2-05) chạy sau soi lượt 2.

## Lệnh bổ sung đã áp
- (không có)

## Nhật ký dựng
- 02:17 UTC dựng xong **H1-01h**: 72 khung (f 0..71), 17.87 s/khung/tiến trình (P = 2), 12 MB, SHA `1565579256b56989…` → LFS + đẩy
- 02:20 UTC nhịp: 27 tệp 1080p đã đẩy LFS; đang dựng: M00 138 khung; ; RAM trống 5078 MB, đĩa trống 13G
- 02:26 UTC **SỰ CỐ:** OOM (cgroup) giết Chromium của M00 ở khung 178/408 — do chạy tiến trình thử thứ 3 (khung phế tích) cạnh 2 tiến trình dựng; M00 dựng lại từ đầu 02:38 (hàng C). Từ đây không chạy tiến trình dựng thứ 3.
- 02:38 soi năm biên lượt 2 (trang đã sửa phế tích): 17/18 ĐẠT; M02 k214 ghi (Monument ngoài khung). Hàng: B (M01 → E-M01-tl), C (M00, M02, M04, H2-02, H2-04h, H2-05), D sau B (M03, H2-00, H2-03b, H2-04a).
- 03:03 UTC nhịp: 27 tệp 1080p đã đẩy LFS; đang dựng: M00 131 khung; M01 207 khung; M02 0 khung; ; RAM trống 5406 MB, đĩa trống 13G
- 03:28 UTC nhịp: 27 tệp 1080p đã đẩy LFS; đang dựng: M00 270 khung; M01 347 khung; M02 0 khung; ; RAM trống 5424 MB, đĩa trống 13G
- 03:43 UTC dựng xong **M01**: 429 khung (f 0..428), 10.71 s/khung/tiến trình (P = 2), 128 MB, SHA `373f74c283f660fc…` → LFS + đẩy
- 03:53 UTC nhịp: 28 tệp 1080p đã đẩy LFS; đang dựng: E-M01-tl 46 khung; M00 406 khung; M02 0 khung; ; RAM trống 5193 MB, đĩa trống 12G
- 03:53 UTC dựng xong **M00**: 408 khung (f 0..407), 10.92 s/khung/tiến trình (P = 2), 77 MB, SHA `7d4468fbcaaa270d…` → LFS + đẩy
- 04:18 UTC nhịp: 29 tệp 1080p đã đẩy LFS; đang dựng: E-M01-tl 174 khung; M02 125 khung; ; RAM trống 4909 MB, đĩa trống 12G
- 04:41 UTC dựng xong **M02**: 242 khung (f 0..241), 11.49 s/khung/tiến trình (P = 2), 74 MB, SHA `04d3f672b0c9541e…` → LFS + đẩy
- 04:43 UTC nhịp: 30 tệp 1080p đã đẩy LFS; đang dựng: M04 7 khung; ; RAM trống 5053 MB, đĩa trống 12G
- 05:08 UTC nhịp: 30 tệp 1080p đã đẩy LFS; đang dựng: M04 141 khung; ; RAM trống 9735 MB, đĩa trống 11G
