# CHECKPOINT — ANIMATIC-T3-V2 (nhánh `k2c-t3-anim-v2`, gốc `origin/ccr-d189108f-6mcz9k` @41e0c8fd)

Phiên sửa animatic T3 theo nhận xét chủ dự án 21/10 21:05–21:15 (phương án A + 5 đoạn minh hoạ Omni M1–M5).

<!-- TRANG-THAI -->
## Trạng thái tự động (21/10/2026 19:29 UTC) — `scripts/k2tl/anim_ckpt.py`

- Cảnh đinh XONG: **10/43** (4619 khung) · CÒN: **33** (14469 khung chưa dựng).
- s/khung TB 12 cảnh gần nhất (mỗi tiến trình, P = 3): 4.71 → ước còn **≈ 6.3 h** dựng cảnh đinh; sau đó: ghép cú lặn → render đoạn → ghép master → LOOK-4 → xuất (≈ 1,5 h).
- Dòng cuối log vòng: `19:22 dựng anim_N2_8 (26.3 s, 960×540)`
- Xong: H1, KA2026, KB2026, KC2026, N1_1, N1_3, N2_11, N5_2, N5_3, N5_4
- Còn: C1 (0/595), C2 (0/343), C3 (0/394), C4 (0/379), C5 (0/355), H2 (0/439), H2T (0/175), H3 (0/314), KA1782 (0/247), KB1943 (0/247), KC1910 (0/223), N1_2 (541/698), N1_4 (0/391), N1_5 (0/754), N1_6 (0/667), N2_10 (0/497), N2_6 (0/403), N2_7 (0/401), N2_8 (172/631), N2_9 (452/727), N3_1 (0/710), N3_2 (0/259), N3_3 (0/295), N3_4 (0/703), N3_5 (0/278), N4_1 (0/667), N4_2 (0/737), N4_3 (0/252), N4_4 (0/461), N4_5 (0/708), N5_1 (0/626), N5_5 (0/523), N5_6 (0/535)

| Tệp ngoài git | SHA-256 | Tái tạo |
|---|---|---|
| `/var/tmp/cine-out/k2c-t3-anim/mix.wav` (tiếng cả tập) | `805432b5c7e92bfb007be9e08a8780c40099502e33703fbafc55360d504c4acd` | `anim_mix.py channel-k2/k2c-t3-01/animatic/anim-loi.json <ra.wav>` |
| cảnh đinh `/var/tmp/cine-out/hero/k2c-t3-anim-anim_*-d/` | (theo stamp từng cảnh) | `bash scripts/k2/build.sh …/animatic/episode.yaml prep` (K2_DRAFT=1 MW=960, chặn mạng) → `P=3 bash scripts/k2tl/anim_vong.sh …/animatic/episode.yaml` |
| lightmap 7 mốc `$K2TL_CACHE/nc/bake/b*/` | meta `reports/animatic-t3/do/nuong-*.json` | `bash scripts/k2tl/anim_nuong.sh` |
<!-- /TRANG-THAI -->

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
