# G1b T3 — CHECKPOINT (nhánh thật: `ccr-6189ede9-lpjwe0`; lệnh yêu cầu `k2c-t3-g1b`)

## Xong
- Bước 0: main ff → p-1810c 5253ba2b, lock 1.15.0 f4fa0349 KHỚP, preflight 6c16e548..main trượt đúng 1 mục (v5b2d-t-540p.mp4 338cef97…a4a8f), push main thường (hook container chỉ là LFS — không cần --no-verify).
- VL1: 5j 17,0 → 18,5 s, tổng 721,2 s, tu_kiem ĐẠT.
- Khung sạch §12.1: cờ shot `p.sach` trong scripts/k2/lib/k2.js (đang thử).
- Bộ đệm cảnh tl dựng lại: /var/tmp/cine-out/k2tl-cache (fetch_sources KHỚP SHA V5b-1 → build_* → pack_1782.sh origin/main). Cần pip: imagecodecs, shapely, OpenEXR, tifffile, pyshp.

## Đang dở
- Animatic 74 shot (đặc tả sinh tự động), SM1–SM3 (phiên con), nguồn mô tả + AI đọc nguồn (phiên con), người + phục chế (phiên con, worktree).

## Tệp ngoài git
| Đường dẫn | Tái tạo |
|---|---|
| /var/tmp/cine-out/k2tl-cache (≈ 1,1 GB) | fetch_sources.py → fetch_osm.py --name gib --bbox=-5.385,36.105,-5.320,36.185 → build_rasters/vectors/scene(--ao --far --cls)/border → pack_1782.sh origin/main |
