# V6 — CHECKPOINT CUỐI 15:58 UTC 18/10/2026 (nhánh thật: `ccr-0e3bf8dd-nst2mv`) — DỪNG chờ chủ dự án

Báo cáo: `reports/v6/V6-BAO-CAO.md`. Lock 1.15.0 KHỚP. Không merge.

## Dừng phiên
- Dừng ≈ 10:35 → 13:01 UTC (worker khởi động lại); không mất tệp, không dựng lại phần nào.

## Đã xong
Toàn bộ bước 1–9 của lệnh V6 (xem báo cáo §0). Chưa đạt: toy_like người ≤ 4; P3/P5 thua V5b-2d (bố cục theo lệnh) — chờ chủ dự án.

## Tệp lớn NGOÀI git
| Đường dẫn | Cỡ | SHA-256 (16) | Tái tạo |
|---|---|---|---|
| /var/tmp/cine-out/k2tl-cache | 1,1 GB | nguồn thô KHỚP sha256.txt V5b-1 | fetch_sources/osm → build_* → pack_1782.sh (≈ 4 phút) |
| /var/tmp/cine-out/v6/v6-t-540p.mp4 | 13,7 MB | 3ed8c316266c3d7e | MIX=audio K2_DRAFT=1 MW=960 bash scripts/k2/build.sh reports/v6/doan-thu/episode.yaml → ffmpeg 960×540 2,5 Mb/s 2 lượt |
| /var/tmp/cine-out/v6-t/v6-t-v1-master.mp4 | 138 MB | — | như trên (≈ 55 phút, P=1) |
| /var/tmp/cine-out/v6/tot/tot-1…6.png | 5 MB/khung | (bản PNG RGB tối ưu trong reports/v6/khung/) | bash scripts/k2tl/v6_tot.sh (≈ 50 phút) |
| /var/tmp/cine-out/v6/cy/x*-cy.exr (+aux) | 42 MB/khung | — | cy6.py (xem v6_tot.sh) |
| /var/tmp/cine-out/v6/khung/sach-*, chu-*, mask* | ≈ 1 MB/khung | bản sạch trong reports/v6/khung/sx-*.jpg | bash scripts/k2tl/v6_khung.sh (≈ 25 phút) |
| /var/tmp/cine-out/v6/khung-neo-chu/*.jpg (4 khung neo có chữ sáng/chiều) | 0,6 MB/khung | reports/v6/khung-neo/khung/NGOAI-GIT.txt | design/pt/song (phiên con) |
| /var/tmp/v6kn (khung neo, PNG 1080p SX + TỐT NHẤT) | ≈ 0,7 GB | — | design/pt/song/*6.py (≈ 2–2,5 h) |

## Chi phí lũy kế
Claude $5,202 (vượt mốc theo dõi $5 lúc 14:33, ghi trong báo cáo) · OpenAI $0,0632 · YouTube 0 · ElevenLabs 0 · giờ máy ≈ 7,5 h đồng hồ tường + phiên con ≈ 8 h tiến trình.
