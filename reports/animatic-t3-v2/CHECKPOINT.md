# CHECKPOINT — ANIMATIC-T3-V2 (nhánh `k2c-t3-anim-v2`, gốc `origin/ccr-d189108f-6mcz9k` @41e0c8fd)

Phiên sửa animatic T3 theo nhận xét chủ dự án 21/10 21:05–21:15 (phương án A + 5 đoạn minh hoạ Omni M1–M5).

## Xong
- Bước 0: nhánh mới từ @41e0c8fd. `verify.sh`: cài OpenEXR, tifffile/pyshp, npm ci k2v + cong3.
- Tệp ngoài git của ANIMATIC-T3 (master v1, lightmap, cảnh đinh, bộ đệm) **đã mất theo container** (BAI-HOC #117) → dựng lại bộ đệm + nướng 7 mốc + dựng cả tập (dù sao mọi cảnh cũng đổi dấu do sửa mã `tl/*.js`).
- Chép bộ kiểm NC-N2P vào `reports/animatic-t3-v2/ma/` (omni_goi.py, kiem_n2p.py, vision_kiem.py, cam_thoi_dai.json, n2p_lib.py).
- Omni bước 0 (21/10/2026 ≈ 14:40 UTC): https://ai.google.dev/gemini-api/docs/omni (Last updated 2026-09-23 UTC) — `gemini-omni-1.1-flash`, CÓ image-to-video (`generation_config.video_config.task = "image_to_video"`, ảnh = khung đầu), 360p/720p (1080p/4K là phóng); https://ai.google.dev/gemini-api/docs/pricing (Last updated 2026-10-19 UTC) — ra video $17,50/1M token, 5 792 token/s 720p ≈ $0,10/s.

## Đang chạy (ngoài git)
- Dựng lại bộ đệm cảnh: `/var/tmp/cine-out/log/chuan-bi.sh` (v7p_cache → mau_nha → faden → anim_tex), log `/var/tmp/cine-out/log/chuan-bi.log`.

## Sự cố
- Lần 1 dựng bộ đệm lỗi: thiếu `origin/v5a` (LUT) trong bản sao mới → `git fetch origin v5a p-1810 main`, chạy lại.
