# design/pt/cpu — NC-CPU (19/10/2026): đo "bước nhảy chất lượng" chỉ bằng CPU

| Tệp | Vai |
|---|---|
| `../../k2v/tl/nc/ncA.js`, `up.js`, `bake.js` | Cách A: bọc cảnh t3tl (V7B) + vân CC0 theo lớp phủ, bụi cây, nước, sương, đọc lightmap nướng |
| `nc_export.js` | xuất hình học khung k2v (cảnh ncA) sang Blender (bản sao chế độ export của scripts/k2tl/export6.js + ẩn bụi theo năm) |
| `nc_topo.js` | albedo nền nhìn thẳng xuống từ k2v (cho B/C) · `--campath`: máy + trạng thái mỗi khung |
| `nc_blend.py` | cảnh Blender đứng riêng: `nuong` (A), `cycles` (B), `eevee` (C) |
| `nc_exr.py`, `nc_grade.js` | EXR → chỉnh màu bằng đường ống k2v (`gradeHDR`) |
| `nc_ghep_lan.py` | ghép cú lặn A ↔ B (hoà chéo) |
| `dive-opt.json`, `fires-1782.json`, `gates.json` | đặc tả cú lặn, 10 đám cháy pin nổi, 6 khung cổng |
| `chay/` | các lệnh đã chạy thật trong phiên (đường dẫn worktree V7B / scratchpad tạm — đổi biến trong `env.sh` khi chạy lại) |

Chạy lại: worktree đọc-chỉ của nhánh V7B + symlink `design/k2v/tl/nc`, `design/pt/cpu` vào đó; bộ đệm k2tl (`scripts/k2tl/v7p_cache.sh` + v7b_mau_nha + v7b_faden); vân CC0 vào `$K2TL_CACHE/nc/tex` (danh sách + SHA: `reports/nc-cpu/RIGHTS-NC.md`). Báo cáo: `reports/nc-cpu/NC-CPU-BAO-CAO.md`.
