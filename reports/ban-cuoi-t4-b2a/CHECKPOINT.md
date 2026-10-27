# BAN-CUOI-T4-B2a — CHECKPOINT

**Nhánh thật:** `claude/adoring-wright-i76iay` (harness buộc; lệnh ghi `k2c-t4-02-final-b2a`). Gốc B1 @6f6c2636 + merge origin/main @75e94b98 (commit 64a304ee, LOCK 1.17.9 `9eddaf24…` KHỚP).

## Trạng thái
- **XONG 08:35 UTC — DỪNG chờ chủ dự án.** Báo cáo: `reports/ban-cuoi-t4-b2a/BAN-CUOI-T4-B2a-BAO-CAO.md`.
- Dựng 1080p: 11 shot B2a + H1-01h (3 018 khung) + thử E M01 — 13/13 tệp trong LFS; không còn tiến trình nền.
- k2check 1.17.9 v5b: GOC-CAO ĐẠT 0, MAY-19 lỗi (a)–(f) 0. Soi năm biên lượt 2: 17/18 ĐẠT (1 ghi).

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
- 05:33 UTC nhịp: 30 tệp 1080p đã đẩy LFS; đang dựng: M03 92 khung; M04 268 khung; ; RAM trống 4541 MB, đĩa trống 6.4G
- 05:36 UTC dựng xong **M04**: 288 khung (f 0..287), 11.44 s/khung/tiến trình (P = 2), 63 MB, SHA `3e557552f8f7e462…` → LFS + đẩy
- 05:58 UTC nhịp: 32 tệp 1080p đã đẩy LFS; đang dựng: H2-02 88 khung; M03 216 khung; ; RAM trống 4850 MB, đĩa trống 6.1G
- 06:08 UTC dựng xong **M03**: 264 khung (f 0..263), 13.43 s/khung/tiến trình (P = 2), 52 MB, SHA `f6a3a7912a96a104…` → LFS + đẩy
- 06:21 UTC dựng xong **H2-00**: 72 khung (f 0..71), 10.84 s/khung/tiến trình (P = 2), 13 MB, SHA `c2978e1b9a5d387b…` → LFS + đẩy
- 06:23 UTC nhịp: 34 tệp 1080p đã đẩy LFS; đang dựng: H2-03b 6 khung; ; RAM trống 5917 MB, đĩa trống 5.8G
- 06:48 UTC nhịp: 34 tệp 1080p đã đẩy LFS; đang dựng: H2-03b 144 khung; ; RAM trống 5816 MB, đĩa trống 5.6G
- 07:03 UTC dựng xong **H2-02**: 351 khung (f 0..350), 14.58 s/khung/tiến trình (P = 2), 71 MB, SHA `d3f4480ee6aa1c10…` → LFS + đẩy
- 07:13 UTC nhịp: 35 tệp 1080p đã đẩy LFS; đang dựng: H2-03b 289 khung; H2-04h 46 khung; ; RAM trống 5902 MB, đĩa trống 5.3G
- 07:16 UTC dựng xong **H2-04h**: 60 khung (f 0..59), 13.14 s/khung/tiến trình (P = 2), 14 MB, SHA `aeed4a4926c83406…` → LFS + đẩy
- 07:38 UTC nhịp: 36 tệp 1080p đã đẩy LFS; đang dựng: H2-05 116 khung; ; RAM trống 5192 MB, đĩa trống 5.1G
- 07:48 UTC dựng xong **H2-03b**: 484 khung (f 0..483), 10.56 s/khung/tiến trình (P = 2), 93 MB, SHA `814b4738c325a072…` → LFS + đẩy
- 08:03 UTC nhịp: 37 tệp 1080p đã đẩy LFS; đang dựng: H2-04a 62 khung; H2-05 244 khung; ; RAM trống 5130 MB, đĩa trống 4.8G
- 08:07 UTC dựng xong **H2-05**: 264 khung (f 0..263), 11.48 s/khung/tiến trình (P = 2), 44 MB, SHA `b194073a85186098…` → LFS + đẩy
- 08:09 UTC dựng xong **H2-04a**: 84 khung (f 0..83), 14.64 s/khung/tiến trình (P = 2), 16 MB, SHA `7957075968b6bd7f…` → LFS + đẩy
