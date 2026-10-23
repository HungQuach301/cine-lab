# CHECKPOINT — LOOK-T4 (K2C-T4-02 London, mốc M1b)

> Nhánh thật: `k2c-t4-02-look` (gốc `origin/k2c-t4-02-tienky` @888de179). Nhánh mặc định của bộ khung `ccr-32b90b5c-vzo2m7` KHÔNG dùng (lệnh gọi tên nhánh).

## Trạng thái
- 23/10 ≈ 14:40 UTC: ĐANG LÀM — soát T3 thấy sân nhà thờ St Paul's bị lấp + cửa sổ hoa hồng sai hướng → sửa hình học, nướng lại, DỰNG LẠI TOÀN BỘ (24 khung, tờ mù, 4 clip, đo 1080p, T3) bằng `/var/tmp/ldn/r/lai_het.sh` (dự kiến xong ≈ 15:50). Báo cáo đang điền số.
- 23/10 ≈ 14:55 UTC: dựng lại xong 24 khung + tờ mù + khoá trên hình học bản cuối (nướng lại 14:37–14:41); đang dựng clip + đo 1080p + T3.
- Chi phí: Claude API 0 · OpenAI 0 · RunPod 0 (nướng Cycles CPU đủ nhanh, không thuê GPU) · Gemini/ElevenLabs/YouTube 0.
- Không pod GPU nào bật. Tiến trình nền: PID trong `/var/tmp/ldn/log/*.pid`.

## Lệnh bổ sung đã áp
- (chưa có)

## Nhật ký
- 10:53 UTC khởi động; verify.sh 10 PASS/5 FAIL → cài OpenEXR/tifffile/pyshp, npm ci (cong3, k2v), pyproj 3.8.0 + lưới OSTN15 (SHA 5d6ed64d…); hook preflight pre-commit + pre-push cài.
- Sự cố: `khop-doornick.json`, `ranh-chay-1666-cuoi.json` của tiền kỳ không có trong git (`channel-k2/.gitignore` chặn `*.json`) → đọc lại điểm khống chế; thêm `channel-k2/k2c-t4-02/.gitignore` mở `mo-hinh/*.json`, `look/**/*.json`.
- Sự cố: `kill $(pgrep -f …)` giết chính shell (exit 144) — lặp BAI-HOC #112; từ đó chỉ dừng theo PID ghi tệp.
- Sự cố: hai chuỗi nền chạy chồng (PID ghi nhầm tiến trình cũ) 2 lần → nướng trên hình học cũ; đã dừng theo PID, chạy lại.
- 11:35 nướng: mặt đất pháp tuyến úp xuống (Blender trục Y = −z đảo vòng) → nướng ra "không che khuất"; sửa thứ tự đỉnh.
- 11:50 Doornick: số 1–93 là tên PHỐ (bảng chú giải), không phải nhà thờ → vị trí nhà thờ từ toạ độ Wikipedia (78) + OSM (30).
