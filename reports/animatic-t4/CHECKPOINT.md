# CHECKPOINT — ANIMATIC-T4 (K2C-T4-02 London, mốc M3: animatic cả tập 640×360 có giọng)

> Nhánh thật: `ccr-21ab5d6f-7l1yln` (harness buộc tên này; lệnh ghi `k2c-t4-02-animatic`). Gốc `origin/main` @2414d1d3 + merge (không squash) `origin/claude/k2c-t4-02-giong-a24udn` @5e5e02ce → merge commit `b0ff47c9`.

## Trạng thái
- 24/10 ≈ 01:35 UTC: khởi động; verify.sh 10 ĐẠT/5 TRƯỢT → cài OpenEXR/tifffile/pyshp, npm ci (cong3, k2v), pyproj 3.8.0 + OSTN15 (SHA 5d6ed64d…) → 14 ĐẠT/1 TRƯỢT (Freesound, tuỳ chọn). Hook pre-commit/pre-push cài trước lần đẩy đầu. `lock.py --verify` KHỚP 08486eb2….
- ≈ 01:52: dữ liệu nền tái tạo (OSM, vector, LiDAR, tư liệu, vân, atlas lửa, hình học V2, 14 lightmap) — `scripts/k2ldn/anim/du_lieu.sh`.
- Việc 1: master giọng tái tạo bit-trùng (`tai_tao.sh`, 0 ký tự): WAV `b9cec467…` OK, FLAC `e5d49871…` OK.
- Việc 2: `BANG-SHOT-v2.{md,json}` (K1-C1 730,083 s; 74 shot; M-d 20,92 %; tấm nền 5,14 %; AI 26,06 %; bản đồ 4,58 %; tư liệu+khắc+thẻ 8,90 %; góc cao ước 67,2 %).
- Việc 3–4: tệp máy 53 (kiem_may.py: mọi cú máy đạt §19 a trên khoá); tốc độ đo 640×360 spp 2 P = 2: 3,24 s/khung mỗi tiến trình (1,62 s/khung thông lượng). Hàng dựng 3D 47 shot đang chạy (PGID 6774).
- Chi phí đến giờ: Gemini 0 · OpenAI 0 · Claude API 0 · ElevenLabs 0 · RunPod 0.

## Lệnh bổ sung đã áp
- (chưa có)
