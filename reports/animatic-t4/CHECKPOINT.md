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

### Lượt ĐO Omni (Q4) — 24/10 ≈ 02:30 UTC
- Ảnh đầu: render 3D tầm người KHÔNG dùng được (mô hình look2 dựng cho máy ≥ 60 m; ở 2–3 m máy nằm trong khối tường — H1-02, H4-04b, H1-12). → ảnh đầu = ảnh tĩnh hoàn thiện OpenAI `gpt-image-2.5-sunburst-2026-09-08` (generations 2560×1440 high, $0,064/ảnh) + kiểm tầng 1 trước khi gửi Omni (Q3 điểm 2, "minh hoạ tĩnh có kiểm lỗi thời đại").
- 3 khoảnh khắc khó nhất, 360p (Q3 điểm 6), khung giờ trong lệnh: **H1-02** hẻm gỗ cháy đêm 8,0 s **$0,279** — tầng 1 ĐẠT, tầng 2 (gpt-6.1-sol 3 khung + q_thoi_dai) ĐẠT; **H1-12** sông đêm bờ bắc cháy 6 s — tầng 1 ĐẠT; **H4-04b** mái 1940 6 s **$0,209** — tầng 1 LOẠI (tay/xô méo).
- Số đo: Omni 360p **1 931 token video/s ≈ $0,034/s** (720p theo bảng giá $0,10/s); clip đúng độ dài yêu cầu (8,000 s / 6 s); thời gian chờ 25–27 s. Flash tầng 1 ≈ $0,003–0,008/lượt; tầng 2 ≈ $0,068 (OpenAI) + $0,10 (Claude qua q_thoi_dai) mỗi clip.
- Gemini phiên đến giờ **$0,72** (≤ $3 lượt ĐO); tổng T4 **$2,16** / $35 (mốc $30).
- **Chốt danh sách:** cả 24 clip / 17 khoảnh khắc của BANG-SHOT-v2 (152,7 s ≈ 21,2 %) ở 360p: ước 1 lượt $5,3, ≤ 3 lượt/khoảnh khắc → trần ước ≈ $9 + Flash ≈ $0,3 → tổng T4 ước ≈ $12 ≪ $30. Bản cuối: sinh lại 720p các lệnh đã chọn (Q3 điểm 8) ≈ 155 s × $0,10 ≈ $16.

- 02:37 UTC: dựng 3D 5/53 tệp máy xong (M01–M04, H1-04…), ước còn ≈ 5,3 h (P = 2, spp 2, 1,62 s/khung). M-d: 7/24 clip chọn (md-so-giay.jsonl). Tấm nền: P1-2026 l1 ĐẠT (i)–(v) (M01, H5-04), P9-2026 l2 ĐẠT (i)–(iv) (iii 1,98 % — sát ngưỡng 2 %), P3-2026 TRƯỢT (iii) 3/3 lượt → H5-06 dùng 3D V2; tấm nền còn 4,59 % (dưới mục tiêu 5 %). Âm thanh nháp −14,0 LUFS / −1,9 dBTP. Bộ ghép, xuất, khai k2check, XEM CÂM: mã sẵn sàng.
- Chi phí đến giờ: Gemini T4 tổng $4.2047 (phiên này $2.77) · OpenAI $2.04 (ảnh + kiểm) · Claude (kiểm) $0.76 + q_thoi_dai.

- 03:27 UTC: **SỰ CỐ** — commit "M-d 22/24…" (đã đẩy) mang theo ≈ 244 MB ảnh lát trung gian của bộ kiểm (`animatic/omni/kiem2/qtd-*/`, khung PNG). Mỗi tệp < 5 MB (preflight ĐẠT) nhưng không cần cho git. Không force-push/amend (K18): commit sau gỡ khỏi theo dõi (`git rm --cached`) + thêm .gitignore; lịch sử nhánh vẫn mang ≈ 244 MB — ghi vào báo cáo.
- M-d: 22/24 đạt 2 tầng; H2-04a (mũ bowler/chóp tròn — lỗi thời đại, 3/3) và H5-07a (ảnh đầu 2026 có chữ/biển, 3/3) → 3D; thêm M-d (19) Toà Cháy 1667 (H2-03c, tách từ H2-03b) để giữ M-d ≥ 20 % (Q1). TRUOT hạ hệ số (1,4 %/s; H1-03 đo 2,99 %/s sát trần 3 → dựng lại).
