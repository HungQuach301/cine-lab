# CHECKPOINT K2G-01 → G2 (phiên P kênh 2)

Cập nhật ở mỗi mốc. Phiên sau đọc tệp này trước.

| Mốc | Trạng thái | Commit |
|---|---|---|
| Bước 1 giọng (Eric, nghe mù 3/3), lời 14 đoạn, ASR khớp số | xong | dcd2f40 |
| Bước 2 nhạc Kevin MacLeod CC BY 4.0 ×4, SFX Work With Sounds CC BY 4.0 ×15, RIGHTS | xong | dcd2f40 |
| Bước 3 8 bộ cảnh 3D (`design/ll-hero/k2g01.js`), lớp 2D K2 (`scripts/k2/lib/k2.js`), đặc tả (`ep-src.yaml` → `make_spec.py` → `episode.yaml`) | xong; luật bối cảnh ĐẠT (`scripts/k2/settings.py`) | (commit này) |
| Bước 4 nháp 960×540: cảnh 3D (`heroes_par.sh`, SPP1, P=3) | đang chạy | — |

## Lệnh
- Nháp: `K2_DRAFT=1 /opt/cine/bin/python scripts/k2/prep.py prep channel-k2/k2g-ep01/episode.yaml` → `SPP=1 P=3 setsid nohup bash scripts/k2/heroes_par.sh <yaml> >> <out>/heroes-par.log 2>&1 &` → `K2_DRAFT=1 MW=960 J=3 bash scripts/k2/build.sh <yaml> render mix ghep`
- 1080p: bỏ `K2_DRAFT`/`MW`, `SPP=4`.
- Dựng tiếp sau ngắt: chạy lại heroes_par.sh (tự `--resume` theo `<dir>.new/pending`).
