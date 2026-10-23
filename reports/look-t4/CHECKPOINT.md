# CHECKPOINT — LOOK-T4 (K2C-T4-02 London, mốc M1b)

> Nhánh thật: `k2c-t4-02-look` (gốc `origin/k2c-t4-02-tienky` @888de179). Nhánh mặc định của bộ khung `ccr-32b90b5c-vzo2m7` KHÔNG dùng (lệnh gọi tên nhánh).

## Trạng thái
- 23/10 ≈ 11:30 UTC: ĐANG LÀM. Xong: tải lại dữ liệu (OSM, LiDAR, tư liệu — mất theo container), đọc lại 11 + 3 điểm khống chế Doornick (tệp tiền kỳ bị `.gitignore` chặn → mất), ranh cháy, nguồn Old St Paul's (Met 336039/336038/757299 CC0), 16 vân CC0, hình học v2 (`hinh_hoc_look.py`), trang dựng `look.js`, nướng Cycles CPU (đo: 102 s/mốc ở 1 m, 32 spp — không cần GPU), LUT B/C, khai 24 khung + 4 clip. Đang: dựng lại hình học (khối Victoria trên lô, nhà thờ theo toạ độ), nướng 3 mốc, chỉnh look.
- Không pod GPU nào đang bật. Tiến trình nền ghi PID ở `/var/tmp/ldn/log/*.pid`.

## Lệnh bổ sung đã áp
- (chưa có)

## Nhật ký
- 10:53 UTC khởi động; verify.sh 10 PASS/5 FAIL → cài OpenEXR/tifffile/pyshp, npm ci (cong3, k2v), pyproj 3.8.0 + lưới OSTN15 (SHA 5d6ed64d…); hook preflight pre-commit + pre-push cài.
- Sự cố: `khop-doornick.json`, `ranh-chay-1666-cuoi.json` của tiền kỳ không có trong git (`channel-k2/.gitignore` chặn `*.json`) → đọc lại điểm khống chế; thêm `channel-k2/k2c-t4-02/.gitignore` mở `mo-hinh/*.json`, `look/**/*.json`.
- Sự cố: lệnh `kill $(pgrep -f …)` giết chính shell (exit 144) — lặp BAI-HOC #112; từ đó chỉ dừng theo PID ghi tệp.
