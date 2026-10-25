# CHECKPOINT — BAN-CUOI-T4-A (K2C-T4-02, phần thử + chuẩn bị)

> Nhánh thật: `claude/k2c-t4-02-final-a-0pb0bh` (harness buộc; lệnh ghi `k2c-t4-02-final-a`). Gốc origin/main @e97fc214 + merge no-ff origin/claude/k1178-t4-london-rules-pdjfmz @297eb070 → `00a2f096` (91 tệp, 0 xung đột; LOCK 1.17.8 `045b7bb7…` KHỚP).

## Trạng thái
- 25/10 23:30 UTC (26/10 06:30 Asia/Saigon): khởi động; SHA khớp lệnh (main e97fc214, K-1.17.8 297eb070); verify.sh 10 PASS/5 FAIL → cài OpenEXR/tifffile/pyshp, npm ci (cong3, k2v), pyproj 3.8.0 + OSTN15 (SHA 5d6ed64d… KHỚP). Hook pre-commit + pre-push cài trước lần đẩy đầu.
- 23:33: merge K-1.17.8 `--no-commit` + preflight "91 tệp — ĐẠT · lock KHỚP · PREFLIGHT ĐẠT" → commit `00a2f096`.
- 23:35: dựng lại dữ liệu LDN (`scripts/k2ldn/anim/du_lieu.sh`, NAM 1666.6 1667.3 1700.5 1711.5 1938.5 1940.98 1955.5 1975.5 2026.7) nền, PGID 2328, log `/var/tmp/ldn/log/du_lieu.log`.
- 23:50: tải IWM D 6418 gốc qua Commons (`scripts/k2ldn/bc/commons_bc.py`, ≤ 1 yêu cầu/5 s, 429 → chờ) — đang chờ 429.
- 23:51: dữ liệu LDN xong (OSM, LiDAR, tư liệu — 2 lỗi tải không dùng: Ogilby 429, NGA Wren; atlas lửa; hình học look2; nướng 9 mốc). Chuỗi nền 1 (`scripts/k2ldn/bc/chuoi_1.sh`, PGID 4833): hình học look3d (THU-B d: 95 393 nhà thường, 4 599 255 tam giác) + look3e (mã 3 485 toà OSM có tên) xong 23:59 → nướng look3d 9 mốc → dựng (ảnh đầu M-d, E, P1, B, mẫu, video E).
- Commons: 429 liên tục từ 23:37 (chờ theo Retry-After/600 s, ≤ 1 yêu cầu/5 s) — IWM D 6418 gốc chưa về. Europeana/LoC thử: không có ảnh hiện đại CC BY/PD phù hợp (LoC "rights not evaluated", Europeana chủ yếu BY-SA/trước 1900).
- H1-15b: YuNet (mô hình checks/models, chỉ dùng tệp mô hình) — các hộp "mặt > 1/8" (khung 113–139, điểm 0,6–0,78) nằm trên trời/tán cây (báo nhầm; mặt người thật ≈ 3 % khung). Theo A1: cắt clip còn khung 0–110 (4,625 s).
- Chi phí đến giờ: Gemini 0 · OpenAI 0 · Claude API 0 · ElevenLabs 0 · RunPod 0.

## Lệnh bổ sung đã áp
- (không có)
