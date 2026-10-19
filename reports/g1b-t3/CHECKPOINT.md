# G1b T3 — CHECKPOINT (nhánh thật: `ccr-6189ede9-lpjwe0`; lệnh yêu cầu `k2c-t3-g1b`)

## Xong
- Bước 0: main ff → p-1810c 5253ba2b, lock 1.15.0 f4fa0349 KHỚP, preflight 6c16e548..main trượt đúng 1 mục (v5b2d-t-540p.mp4 338cef97…a4a8f), push main thường (hook container chỉ là LFS — không cần --no-verify).
- VL1: 5j 17,0 → 18,5 s, tổng 721,2 s, tu_kiem ĐẠT.
- Khung sạch §12.1: cờ shot `p.sach` trong scripts/k2/lib/k2.js (đang thử).
- Bộ đệm cảnh tl dựng lại: /var/tmp/cine-out/k2tl-cache (fetch_sources KHỚP SHA V5b-1 → build_* → pack_1782.sh origin/main). Cần pip: imagecodecs, shapely, OpenEXR, tifffile, pyshp.

## Xong thêm (18:10 UTC)
- Đặc tả toàn tập: channel-k2/k2c-t3-01/g1b/mk_ep_g1b.py → episode.yaml (75 đoạn = 74 shot + thẻ phương pháp 5 s; 72 cảnh), ray-loi.srt, log-shot.json. Soi 1 khung/cảnh (g1b_probe.sh).
- Cảnh tổng quát design/k2v/tl/scenes/t3s.js; người thời kỳ sau trong people.js; nguồn mô tả YouTube + thẻ phương pháp + AI đọc nguồn (phat-hanh/, g1b/ai-doc-nguon.*).

## Đang dở
- Dựng animatic 540p toàn tập: `P=2 J=2 bash scripts/k2tl/g1b_animatic.sh render` (bắt đầu 18:09 UTC; log /var/tmp/cine-out/g1b/render.log), sau đó `… mix ghep ray`.
- SM1–SM3 (phiên con), người + phục chế (phiên con, worktree).

## Tệp ngoài git
| Đường dẫn | Tái tạo |
|---|---|
| /var/tmp/cine-out/k2v-cache/g1b (ảnh ref + 3 ảnh tải: rooke 7f24f0bb…, capture1704 710731a6…, loc 2020680546 57fbdfc5…) | cp vay-ham/ref/*.jpg + curl Special:FilePath (UA CineLab) |
| /var/tmp/cine-out/hero/k2c-t3-g1b-* , /var/tmp/cine-out/k2c-t3-g1b | bash scripts/k2tl/g1b_animatic.sh |
| /var/tmp/cine-out/k2tl-cache (≈ 1,1 GB) | fetch_sources.py → fetch_osm.py --name gib --bbox=-5.385,36.105,-5.320,36.185 → build_rasters/vectors/scene(--ao --far --cls)/border → pack_1782.sh origin/main → pack_g1b.sh |

## Dừng phiên (worker khởi động lại)
- Tiến trình dựng chết ≈ 19:40 UTC (máy khởi động lại; phát hiện 22:22). /var/tmp còn nguyên: 10 cảnh đã xong giữ nguyên (stamp), 2 cảnh dở dựng tiếp `--resume`. Chạy lại 22:23 UTC cùng lệnh. Không mất tệp.
- SM1–SM3 xong (phiên con, commit 0deffd63); người + phục chế xong (phiên con, commit d9c496c0).

## CUỐI (≈ 04:40 UTC 19/10) — DỪNG chờ chủ dự án
- Xong mọi bước 0–8; báo cáo `reports/g1b-t3/G1B-BAO-CAO.md`.
- Ngoài git: master `/var/tmp/cine-out/k2c-t3-g1b/k2c-t3-g1b-v1-master.mp4` (688 MB, e186dbb2…) · bản ray 540p `…/k2c-t3-g1b-animatic-540p-ray.mp4` (216 MB, 2b8ed11f…) · cảnh đinh 540p `/var/tmp/cine-out/hero/k2c-t3-g1b-*` · đo 1080p `/var/tmp/cine-out/g1b/bench1080` · O2 `/var/tmp/cine-out/g1b/o2`. Tái tạo: `bash scripts/k2tl/g1b_animatic.sh` (sau khi dựng bộ đệm như bảng trên + bộ đệm SM theo log-SM*.json khoá `dung`).
