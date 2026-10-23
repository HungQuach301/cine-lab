# Gói phát hành T3 Gibraltar — `release-k2-t3-g2` (bản cuối 1080p, chờ chủ dự án duyệt G2)

Phiên BAN-CUOI-T3, 23/10/2026. Nhánh này = `k2c-t3-cuoi` (commit `ad124ee1`) + gói phát hành ở gốc. **Không merge.** Báo cáo: `reports/ban-cuoi-t3/BAN-CUOI-BAO-CAO.md`.

| Tệp | Nội dung |
|---|---|
| `k2-t3-v1-master.mp4` (LFS) | master 1920×1080 H.264 High 24 fps, 762,000 s (18 288 khung), hình 18,5 Mb/s (crf 17, trần 19 Mb/s), AAC LC 48 kHz 310 kb/s; −14,0 LUFS · LRA 3,1 · đỉnh thật −1,4 dBTP; LUT kênh `k2c-t3-kenh-v030.cube` |
| `k2-t3-v1-p1/p2/p3.mp4` (LFS) | 3 phần 1080p chia ở ranh chương **262,208 s** (hết ch.2a vây hãm) và **471,625 s** (hết ch.3): 262,2 / 209,4 / 290,4 s; hình **sao chép luồng từ master** (khung ranh khớp MD5), tiếng −1,2 dB + alimiter 0,75, AAC 256 kb/s |
| `k2-t3-v1-en.srt`, `.vtt` | phụ đề CC tiếng Anh, 129 câu, thứ tự mới (không ghép cứng) |
| `k2-t3-v1-thumb-1…6.jpg` | 6 ứng viên thumbnail 1920×1080 (≤ 2 MB), **không chữ**, cú máy X01/X08 (H2T Cycles GPU, khung EXR 0/6/12/48/96/119: chạng vạng → đêm) — chủ dự án chọn |
| `SHA256SUMS.txt` | SHA-256 mọi tệp trên |

Ngoài git (quá lớn / chưa có mẫu LFS — đề xuất D4): `mix.wav` `b0eb636a…`, `stem-giong.wav` `0cbe4556…`, `stem-nhac.wav` `c85fbff6…`, `stem-sfx.wav` `7547d960…` (48 kHz, 219 MB/tệp; SHA đầy đủ trong báo cáo §10). Tái tạo: `scripts/k2tl/cuoi_mix.py`, master/phần: `LUT=channel-k2/k2c-t3-01/mau/k2c-t3-kenh-v030.cube bash scripts/k2tl/cuoi_xuat.sh master|phan|xem` từ các đoạn `sec/*.mkv` (`scripts/k2tl/cuoi_doan.sh`).

Công bố AI: không chữ AI trên hình/thẻ (quyết định 22/10); `episode.yaml` khai `giong_tong_hop: true`, `phat_hanh: {cong: phat_hanh, youtube_altered_content: true}`. **Mô tả YouTube + bình luận ghim (câu AI/synthetic) do phiên đóng gói viết** — chưa có trong gói này.
