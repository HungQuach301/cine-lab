# CHECKPOINT — BAN-CUOI-T3 (nhánh `k2c-t3-cuoi`)

Gốc: `origin/k2c-t3-anim-v2` @72e3f0fe ("cứu 4 video gốc Omni") + merge --no-ff `origin/checks-1-17-1` @39d01859 (→ 622a1c27) + `origin/claude/laughing-ptolemy-u7xlwe` @0a10d1fc (→ 170e55ce). 0 xung đột.

## Trạng thái (cập nhật 22/10 05:15 UTC)
- Bộ đệm cảnh gib dựng lại (`scripts/k2tl/cuoi_cache.sh`); 2 tệp nguồn bị proxy cắt giữa chừng (Catastro, LoC) → tải lại, SHA KHỚP sổ V5B1.
- Hook preflight + LFS pre-push đã cài.
- Nướng 7 lightmap đang chạy nền (PGID trong `/var/tmp/cine-out/log/nuong.pgid`): b1779 xong 1 160 s.
- Việc 1b: module mới `design/k2v/tl/doisong.js` (vật đời sống chung bậc 5) + `cuoi/mk_ep_cuoi.py` (bản sao mk_ep_anim.py có sửa). Soi 480×270: N3.1, N3.3, N3.4, N4.1 cỏ ≤ 40 % (trừ ≤ 2 s đầu N3.3).
- Chưa: C4 (1a), H1 (1c), 1969 (1d), nhịp (1e), nhãn (1f); GPU; 1080p; Omni; màu; âm thanh; thẻ; kiểm; xuất.

## Tệp ngoài git
| Tệp | Tái tạo |
|---|---|
| `/var/tmp/cine-out/k2tl-cache/` | `bash scripts/k2tl/cuoi_cache.sh` |
| lightmap `$K2TL_CACHE/nc/bake/b*/` | `NUONG_META=reports/ban-cuoi-t3/do bash scripts/k2tl/anim_nuong.sh` |
