# NC-CPU — CHECKPOINT (nhánh thật: `claude/clever-franklin-daez5k`, harness buộc; lệnh yêu cầu `nc-cpu`; gốc origin/main 3176ad1b)

## Lượt 1 (≈ 17:15 UTC 19/10)
- Bộ đệm k2tl dựng lại từ nguồn (2 phút) trong worktree đọc-chỉ của V7B (`origin/ccr-ef2b66f0-9639kq`); khung cổng V7B tái tạo khớp (lệch TB 4,7/255, JPEG + hạt).
- Mã mới: `design/k2v/tl/nc/{ncA.js, up.js, bake.js}` (cách A: bọc t3tl, vân CC0 theo lớp phủ, bụi cây instanced, nước mới, sương khí quyển, đọc lightmap nướng),
  `design/pt/cpu/{nc_topo.js, nc_export.js, nc_blend.py}` (albedo nhìn thẳng xuống, xuất cảnh, cảnh Blender: nướng / Cycles / Eevee).
- Eevee chạy được trong container (llvmpipe/EGL, có cảnh báo EGL_BAD_MATCH) — cảnh rỗng 34 s (biên dịch shader).
- Lỗi đã gặp: lọc dị hướng (anisotropy 8) trên sampler2DArray ở llvmpipe → khối đen NaN dọc mép lớp phủ → tắt (aniso 1).
- Đang chạy: thử nướng Cycles mốc 1782 (hộp phố 2 × 3 km, 2 m/texel, 32 spp).
