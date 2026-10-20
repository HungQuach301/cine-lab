# NC-CPU — CHECKPOINT (nhánh thật: `claude/clever-franklin-daez5k`, harness buộc; lệnh yêu cầu `nc-cpu`; gốc origin/main 3176ad1b)

## Lượt 1 (≈ 17:15 UTC 19/10)
- Bộ đệm k2tl dựng lại từ nguồn (2 phút) trong worktree đọc-chỉ của V7B (`origin/ccr-ef2b66f0-9639kq`); khung cổng V7B tái tạo khớp (lệch TB 4,7/255, JPEG + hạt).
- Mã mới: `design/k2v/tl/nc/{ncA.js, up.js, bake.js}` (cách A: bọc t3tl, vân CC0 theo lớp phủ, bụi cây instanced, nước mới, sương khí quyển, đọc lightmap nướng),
  `design/pt/cpu/{nc_topo.js, nc_export.js, nc_blend.py}` (albedo nhìn thẳng xuống, xuất cảnh, cảnh Blender: nướng / Cycles / Eevee).
- Eevee chạy được trong container (llvmpipe/EGL, có cảnh báo EGL_BAD_MATCH) — cảnh rỗng 34 s (biên dịch shader).
- Lỗi đã gặp: lọc dị hướng (anisotropy 8) trên sampler2DArray ở llvmpipe → khối đen NaN dọc mép lớp phủ → tắt (aniso 1).
- Đang chạy: thử nướng Cycles mốc 1782 (hộp phố 2 × 3 km, 2 m/texel, 32 spp).

## Lượt 2 (≈ 17:50 UTC 19/10)
- Nướng b1782 xong: hộp E −3000…1000, N −3000…3500, 3 m/texel (1333 × 2167), 24 spp, 4 lượt (trời 481 s, nảy nắng 267 s, nắng thẳng 327 s, lửa 395 s) = **1 481 s** (máy có tải song song). Đang nướng b2026.
- Cảnh Blender đứng riêng chạy cả Cycles và **Eevee** (llvmpipe, 480×270 8 mẫu 110 s có tải). Cú lặn: đường máy `design/pt/cpu/dive-opt.json`, đang dựng phần A (khung 0–227, 336–479).

## Lượt 3 (≈ 18:50 UTC 19/10)
- 6 khung cổng 1080p: A (`khung/A`), B nhanh 16 spp (`khung/B-nhanh`), C Eevee 32 mẫu (`khung/C`), V7B (bản sao JPG `khung/V7B`). Tờ so `to-so-khung.jpg`.
- Chấm mù 640×360 (3 vai × 6 loại, $1,10): hạng 1 — A 11, V7B 3, B 2, C 2.
- Đang dựng: cú lặn phần B (khung 216–348, Cycles 12 spp 1080p, lửa + khói thể tích), rồi B đẹp 128 spp 6 khung.

## Lượt 4 (≈ 20:05 UTC 19/10)
- Báo cáo nháp `NC-CPU-BAO-CAO.md` (§0–§9, còn ô [..] chờ số cú lặn B, B đẹp, đo lại Eevee/chuỗi A). Cú lặn B: 29/97 khung (khung 216–312), ≈ 130–145 s/khung.
- Lỗi vận hành: một tiến trình `chain.sh` cũ (nohup) chạy chồng lượt Eevee + cú lặn B (18:27–19:22) → số Eevee 6 khung và khung lặn 216–227 có tải chồng; sẽ đo lại Eevee khi máy rảnh.

## CUỐI (≈ 23:25 UTC 19/10) — DỪNG chờ chủ dự án
- Cú lặn ghép xong: `reports/nc-cpu/lan/nc-lan-xem.mp4` (4,39 MB) + master ngoài git (SHA trong báo cáo §0). B đẹp 2 khung, Eevee đo lại, chuỗi t3tl ↔ ncA (+36 %).
- Báo cáo hoàn chỉnh `reports/nc-cpu/NC-CPU-BAO-CAO.md`.
