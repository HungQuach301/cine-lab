# CHECKPOINT K2G-01 → G2 (phiên P kênh 2)

Cập nhật ở mỗi mốc. Phiên sau đọc tệp này trước.

| Mốc | Trạng thái | Commit |
|---|---|---|
| Bước 1 giọng (Eric, nghe mù 3/3), lời 14 đoạn, ASR khớp số | xong | dcd2f40 |
| Bước 2 nhạc Kevin MacLeod CC BY 4.0 ×4, SFX Work With Sounds CC BY 4.0 ×15, RIGHTS | xong | dcd2f40 |
| Bước 3 8 bộ cảnh 3D (`design/ll-hero/k2g01.js`), lớp 2D K2 (`scripts/k2/lib/k2.js`), đặc tả (`ep-src.yaml` → `make_spec.py` → `episode.yaml`) | xong; luật bối cảnh ĐẠT (`scripts/k2/settings.py`) | (commit này) |
| Bước 4 nháp 960×540: 37 cảnh (88 phút, P=3), ghép 14 đoạn + 2 Short; master nháp −14,0 LUFS / −1,6 dBTP; QC nháp `qc-nhap.md` | xong | (commit này) |
| Bước 4 một lượt sửa (26 mục, `SUA-NHAP.md`) | xong | (commit này) |
| Bước 4 1080p: 37 cảnh SPP4 P=3 (bắt đầu 18:20, ước 9–10 giờ máy) → render → mix → ghép → Shorts | đang chạy (`/var/tmp/cine-out/k2g-ep01/heroes-1080.log`) | — |

## Lệnh
- Nháp: `K2_DRAFT=1 /opt/cine/bin/python scripts/k2/prep.py prep channel-k2/k2g-ep01/episode.yaml` → `SPP=1 P=3 setsid nohup bash scripts/k2/heroes_par.sh <yaml> >> <out>/heroes-par.log 2>&1 &` → `K2_DRAFT=1 MW=960 J=3 bash scripts/k2/build.sh <yaml> render mix ghep`
- 1080p: `/opt/cine/bin/python scripts/k2/prep.py prep <yaml>` → `SPP=4 P=3 setsid nohup bash scripts/k2/heroes_par.sh <yaml> >> <out>/heroes-1080.log 2>&1 &` → `J=3 V=v1 bash scripts/k2/build.sh <yaml> render mix ghep shorts`. Chọn SPP4 (đo 1080p: SPP2 2,68 s/khung, SPP4 4,15 s/khung trên valley; khác biệt tĩnh nhỏ, SPP4 bớt nhấp nháy nét mảnh khi chuyển động).
- Dựng tiếp sau ngắt: chạy lại heroes_par.sh (tự `--resume` theo `<dir>.new/pending`).
