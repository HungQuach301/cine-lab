# CHECKPOINT — ANIMATIC-T3 (nhánh thật `ccr-d189108f-6mcz9k`, harness buộc; lệnh gọi `k2c-t3-animatic`)

Cập nhật: 21/10/2026 ≈ 04:20 UTC

<!-- TRANG-THAI -->
## Trạng thái tự động (21/10/2026 12:49 UTC) — `scripts/k2tl/anim_ckpt.py`

- Cảnh đinh XONG: **43/43** (20253 khung) · CÒN: **0** (0 khung chưa dựng).
- s/khung TB 12 cảnh gần nhất (mỗi tiến trình, P = 3): 4.42 → ước còn **≈ 0.0 h** dựng cảnh đinh; sau đó: ghép cú lặn → render đoạn → ghép master → LOOK-4 → xuất (≈ 1,5 h).
- Dòng cuối log vòng: `10:48 VONG-XONG`
- Xong: C1, C2, C3, C4, C5, H1, H2, H2T, H3, KA1782, KA2026, KB1943, KB2026, KC1910, KC2026, N1_1, N1_2, N1_3, N1_4, N1_5, N1_6, N2_10, N2_11, N2_6, N2_7, N2_8, N2_9, N3_1, N3_2, N3_3, N3_4, N3_5, N4_1, N4_2, N4_3, N4_4, N4_5, N5_1, N5_2, N5_3, N5_4, N5_5, N5_6
- Còn: 

| Tệp ngoài git | SHA-256 | Tái tạo |
|---|---|---|
| `/var/tmp/cine-out/k2c-t3-anim/mix.wav` (tiếng cả tập) | `805432b5c7e92bfb007be9e08a8780c40099502e33703fbafc55360d504c4acd` | `anim_mix.py channel-k2/k2c-t3-01/animatic/anim-loi.json <ra.wav>` |
| cảnh đinh `/var/tmp/cine-out/hero/k2c-t3-anim-anim_*-d/` | (theo stamp từng cảnh) | `bash scripts/k2/build.sh …/animatic/episode.yaml prep` (K2_DRAFT=1 MW=960, chặn mạng) → `P=3 bash scripts/k2tl/anim_vong.sh …/animatic/episode.yaml` |
| lightmap 7 mốc `$K2TL_CACHE/nc/bake/b*/` | meta `reports/animatic-t3/do/nuong-*.json` | `bash scripts/k2tl/anim_nuong.sh` |
<!-- /TRANG-THAI -->

## Xong
- Bước 0: fetch; `origin/main` = `bc7e96d1` (có P-2010b). Nhánh từ V7C `47a0f55a` + `merge --no-ff origin/main` (0 xung đột). `lock.py --verify` KHỚP 1.16.1 `a3c39873…`; `LOI-KHOA.sha256` 3/3 OK.
- LOOK-KHOA.md (commit `ANIMATIC-T3 bước 0`, đã đẩy).
- Bộ đệm cảnh k2tl dựng lại (`v7p_cache.sh`), màu nhà V7B, Faden, vân CC0 36/36 khớp SHA (`anim_tex.py`), `imageio` cho `/opt/bpy`.
- Giọng master LFS `T3-loi-G1-v42-14LUFS.wav` tải được, SHA `ba50fba7…` khớp; nhạc `assets/k2/music/` 14 tệp, `SHA256SUMS` khớp.
- Đặc tả 43 shot + 2 thẻ: `channel-k2/k2c-t3-01/animatic/mk_ep_anim.py` → `episode.yaml`, `log-shot.json`, `bang-shot.{json,md}`, `anim-loi.json`, `phu-de.srt`.
- Mã dựng mới: `design/k2v/tl/san_bay.js` (dải cỏ 1934, máy bay 1942, đường lệch), `tl7.js camps({tuNhien})`, `t3tl.js` (campTuNhien, fenceOff, fenceNew, grassStrip, mayBay).
- Q3: `reports/animatic-t3/q3_trich.py` → `q3-trich.json` (8/8 khớp nguyên văn).

## Sự cố
- 01:17 UTC container khởi động lại (worker restart): đĩa `/var/tmp/cine-out` CÒN, tiến trình mất (nướng b1782 dở, dựng C3 dở, soi 2). Đã chạy lại: nướng bỏ qua b1779 đã xong; C3 dựng tiếp `--resume`.

## Đo sớm (960×540, spp 4, cách A, máy có nướng song song + P=2) — `<out>/heroes-gio.log`
| Shot | Loại | Khung | Giây đồng hồ | s/khung |
|---|---|---|---|---|
| C2 | lai ngày (vịnh) | 288 | 623 | 2,16 |
| C3 | cận phố/người → cẩu | 339 | 1 167 | 3,44 |
| H2T | đêm lửa (góc thumbnail) | 120 | 372 | 3,10 |
| KA1782 | neo phố 1782 | 192 | 699 | 3,64 |
| C1 | lai vây hãm (dài) | 540 | 2 561 | 4,74 |
Đợt 1 (10 shot, ≈ 4 300 khung) = 1 h 52 đồng hồ → ≈ 0,64 khung/s. Còn ≈ 14 000 khung → **≈ 6 h** dựng + render đoạn/ghép ≈ 1 h. Giờ máy cả phiên ước ≈ 11–12 h (mốc 16 h).
Lưu ý: mọi sửa mã `design/k2v/tl/*.js` đổi dấu MỌI cảnh (prep băm cả thư mục) → đã chốt mã trước đợt dựng 02:25; lần dựng 01:36–02:20 (C1–C4) bỏ vì sửa nước LOOK-4.

## Soi bố cục (3 đợt, tắt cách A, 480×270)
Đợt 1 bắt: Rock cắt mép (N1.5, N3.1, N4.1, N4.2, N5.1, N5.5, N1.6), người/Línea/hạm đội quá nhỏ (N1.4, N1.6, N2.8, N2.7), đêm tối sớm (N4.5, N5.3 — giờ mặt trời), khung neo tầm mắt chỉ thấy tường (KA, KB), C4 cận Old Mole nhìn xuống 45°, C1 lều thành khối. Đã sửa máy; đợt 2–3 kiểm lại đạt (C1: lều bớt "bàn cờ", chưa hết).

## Đang chạy (ngoài git)
- Nướng lightmap: `bash scripts/k2tl/anim_nuong.sh` (PGID trong `/var/tmp/cine-out/log/nuong.pgid`), log `/var/tmp/cine-out/log/nuong.log` → `$K2TL_CACHE/nc/bake/b*/`.
- Vòng dựng cảnh đinh theo lightmap sẵn có: `bash scripts/k2tl/anim_vong.sh channel-k2/k2c-t3-01/animatic/episode.yaml` (PGID `/var/tmp/cine-out/log/vong.pgid`, log `vong.log`, giờ từng cảnh `<out>/heroes-gio.log`).
- Tiếng XONG: `/var/tmp/cine-out/k2c-t3-anim/mix.wav` (−14,0 LUFS, −1,5 dBTP, −1,3 sau AAC; SMR p10 19,7 dB) — tái tạo `anim_mix.py channel-k2/k2c-t3-01/animatic/anim-loi.json <ra.wav>`.

## Tệp ngoài git + tái tạo
| Tệp | Nơi | Tái tạo |
|---|---|---|
| bộ đệm cảnh | `/var/tmp/cine-out/k2tl-cache/` | `bash scripts/k2tl/v7p_cache.sh` → `v7b_mau_nha.py` → `v7b_faden.py` → `anim_tex.py` |
| lightmap 7 mốc | `$K2TL_CACHE/nc/bake/b{1704,1779,1781r,1782,1900,1940,2026}/` | `bash scripts/k2tl/anim_nuong.sh` (meta → `reports/animatic-t3/do/nuong-*.json`) |
| nguồn Q3 | `/var/tmp/cine-out/nguon/*.txt` (SHA khớp đăng ký) | tải `https://archive.org/download/<id>/<id>_djvu.txt` |

## Còn lại
Đo sớm 3 shot → dựng 43 shot → ghép → LOOK-4 → xuất chương → tự đo → báo cáo.
