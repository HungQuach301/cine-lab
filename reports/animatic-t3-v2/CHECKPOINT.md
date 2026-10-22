# CHECKPOINT — ANIMATIC-T3-V2 (nhánh `k2c-t3-anim-v2`, gốc `origin/ccr-d189108f-6mcz9k` @41e0c8fd)

Phiên sửa animatic T3 theo nhận xét chủ dự án 21/10 21:05–21:15 (phương án A + 5 đoạn minh hoạ Omni M1–M5).

<!-- TRANG-THAI -->
## Trạng thái cuối (22/10/2026 03:40 UTC) — HOÀN TẤT, DỪNG chờ chủ dự án

- Cảnh đinh: **43/43** xong. Master v2 dựng xong, 761,000 s, SHA `a9a35a128225bbf0ab8cce3de3a361e16dc95002170235ef6fd574465ff59b74` (ngoài git).
- Minh hoạ Omni: M2, M3, M4, M5 đạt và đã chèn; M1 giữ 3D sau 3 lần LOẠI.
- Đã xuất: 8 tệp xem trong `xem/`, `to-khung.jpg`, `to-so/`, `PHIEU-XEM-V2.md`. Đã chạy k2check 1.16.1 và xem câm 3 AI.
- Báo cáo: `ANIM-V2-BAO-CAO.md`. Vòng CHECKPOINT tự động đã dừng.

| Tệp ngoài git | SHA-256 | Tái tạo |
|---|---|---|
| `/var/tmp/cine-out/k2c-t3-anim/k2c-t3-anim-v2-master.mp4` | `a9a35a128225bbf0ab8cce3de3a361e16dc95002170235ef6fd574465ff59b74` | xem `ANIM-V2-BAO-CAO.md` mục 6 |
| `/var/tmp/cine-out/k2c-t3-anim/mix.wav` (tiếng cả tập) | `805432b5c7e92bfb007be9e08a8780c40099502e33703fbafc55360d504c4acd` | `anim_mix.py channel-k2/k2c-t3-01/animatic/anim-loi.json <ra.wav>` |
| lightmap 7 mốc `$K2TL_CACHE/nc/bake/b*/` | meta `reports/animatic-t3-v2/do/nuong-*.json` | `bash scripts/k2tl/anim_nuong.sh` |
<!-- /TRANG-THAI -->

## Lệnh bổ sung 22/10: cứu 4 video gốc Omni 720p — XONG

- `omni/goc720/` gồm M2.mp4 (CRF 19), M3.mp4 (CRF 17), M4.mp4 (CRF 16), M5.mp4 (CRF 16), tất cả 1280×720, 24 fps, không tiếng, mỗi tệp ≤ 4,9 MB. Kèm `SHA256SUMS` và `GHI-CHU.md`.
- Không tệp gốc nào MẤT. Riêng M5-l3 lấy từ `omni/ra/` vì `omni-goc/` không có; SHA khớp sổ AI.


## Xong
- Bước 0: nhánh mới từ @41e0c8fd. `verify.sh`: cài OpenEXR, tifffile/pyshp, npm ci k2v + cong3.
- Tệp ngoài git của ANIMATIC-T3 (master v1, lightmap, cảnh đinh, bộ đệm) **đã mất theo container** (BAI-HOC #117) → dựng lại bộ đệm + nướng 7 mốc + dựng cả tập (dù sao mọi cảnh cũng đổi dấu do sửa mã `tl/*.js`).
- Chép bộ kiểm NC-N2P vào `reports/animatic-t3-v2/ma/` (omni_goi.py, kiem_n2p.py, vision_kiem.py, cam_thoi_dai.json, n2p_lib.py).
- Omni bước 0 (21/10/2026 ≈ 14:40 UTC): https://ai.google.dev/gemini-api/docs/omni (Last updated 2026-09-23 UTC) — `gemini-omni-1.1-flash`, CÓ image-to-video (`generation_config.video_config.task = "image_to_video"`, ảnh = khung đầu), 360p/720p (1080p/4K là phóng); https://ai.google.dev/gemini-api/docs/pricing (Last updated 2026-10-19 UTC) — ra video $17,50/1M token, 5 792 token/s 720p ≈ $0,10/s.

- Mã (một lượt, chưa dựng): `mk_ep_anim.py` — H1 ngày→đêm (15:00 → 23:52), H2 nối 23:53; R1/R3/R4 cho N1.4, N1.5 (cảng → lâu đài → eo đất/2015), N1.6 (vách bắc + khói → cận Línea → 2026), C1 (3 góc), N2.10 (2 góc), N2.7 (hạ 70 m), N2.11 (3 góc); C4 máy thấp từ vịnh; N5.4 khung lai thấp + phố 2026 (cây/đèn/xe); `nc/up.js` sửa nước đất lấn (AT-D1, bờ theo mốc 0/1941/1987/2026 + ô chưa nổi = nước); `life.js` tuỳ chọn `dir` (dòng người cùng chiều).
- Công cụ: `scripts/k2tl/v2_do_r2.py` (đo R2/R1 bằng mặt nạ ID), `v2_thu_may.py` (thử máy), `anim_minh_hoa.py` (chèn M1–M5 + nhãn Illustration); `reports/animatic-t3-v2/ma/omni_i2v.py`, `kiem_minh_hoa.py`; lệnh Omni `omni/lenh/`.

## Đang chạy (ngoài git)
- Nướng 7 lightmap: `NUONG_META=reports/animatic-t3-v2/do bash scripts/k2tl/anim_nuong.sh …` (PGID `/var/tmp/cine-out/log/nuong.pgid`, log `nuong.log`). Lần 1 hỏng (thiếu `imageio` trong /opt/bpy) → cài, chạy lại.
- Soi bố cục shot đổi (tắt cách A, 480×270) + ảnh đầu M1–M5 (1280×720, cách A không lightmap).
- Dựng lại bộ đệm cảnh: `/var/tmp/cine-out/log/chuan-bi.sh` (v7p_cache → mau_nha → faden → anim_tex), log `/var/tmp/cine-out/log/chuan-bi.log`.

## Omni (gemini-omni-1.1-flash, image-to-video 720p, ~10 s/lượt, ≈ $1,02/lượt) — sổ `so-ai-gemini.jsonl`
- M3-l1 ĐẠT (chọn) · M4-l1 ĐẠT (chọn, bỏ 2 s đầu) · M2: l1 LOẠI (tàu, tháp chuông, đê bịa ở vịnh) → đổi ảnh đầu nhìn lên sườn; l2 LOẠI (nét giống chữ trên bụi cọ); l3 ĐẠT (chọn, bỏ 1 s đầu)
- M1: l1 LOẠI (tàu có cột buồm), l2 LOẠI (cờ trên cột), l3 LOẠI (cọc buộc tàu sắt "≈ 1800") → **giữ bản 3D** (3 lượt hết)
- M5: l1 LOẠI (logo giày, biển vàng sân bay, logo đuôi máy bay) → l2 đang chạy
- Video gốc Omni (> 5 MB) để ngoài git `/var/tmp/cine-out/omni-goc/` (SHA trong sổ); bản xem 640×360 `omni/xem/`.

## Đang dựng
- Vòng dựng cảnh đinh P=3 (`scripts/k2tl/anim_vong.sh`, log `/var/tmp/cine-out/log/vong.log`) theo lightmap đã nướng.

## Sự cố
- Commit "chốt máy" lần đầu lọt 9 video > 5 MB (preflight báo TRƯỢT nhưng `| tail -1 &&` không chặn) → sửa commit trên nhánh của phiên (amend + force-with-lease), video gốc ra ngoài git + `.gitignore`.
- Lần 1 dựng bộ đệm lỗi: thiếu `origin/v5a` (LUT) trong bản sao mới → `git fetch origin v5a p-1810 main`, chạy lại.
