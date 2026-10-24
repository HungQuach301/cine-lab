# CHECKPOINT — THU-B-T4 (vòng thử B + D chống "đồ chơi", K2C-T4-02)

> Nhánh thật: `ccr-ce664665-996oyl` (harness buộc; lệnh gọi `k2c-t4-02-thu-b`). Gốc origin/main @2414d1d3 + merge (không squash) origin/checks-1-17-5 @1dc8be60 → merge `ea15a120`.

## Trạng thái
- 24/10 04:35 UTC: bắt đầu. Đọc tài liệu nền (K1175 §5–§7, RULES 1.17.5, Kinh thánh §11.3/§11.4/§14.7/§15/§19, LOOK-T4-V2 §1/§4, BAI-HOC-K2, BAI-HOC-LL). Hook pre-commit + pre-push cài (trước lần đẩy đầu).
- 04:37–04:48: container mới, `/var/tmp` trống → dựng lại dữ liệu nền bằng đúng lệnh LOOK (`scripts/k2ldn/thu-b/dung_lai_du_lieu.sh`): OSM, LiDAR, Doornick, vân CC0, atlas lửa, hình học look2, nướng 1666.6/2026.7. `ldn2.bin` SHA `bd776509…` ≠ LOOK-T4-V2 `73e68223…` (OSM sống đổi: lô 42 951 → 42 947) — ghi sự cố.
- 04:50: đang dựng hình học look3b (mã nhà/mặt phẳng) + nướng 1938.7; viết `look3.js` (sinh từ look2.js bằng `tao_look3.py`), máy thử `channel-k2/k2c-t4-02/thu-b/may/`.
- Chi phí đến giờ: OpenAI 0 · Claude API 0 · Gemini 0 (không gọi) · ElevenLabs/RunPod/YouTube 0.

## Lệnh bổ sung đã áp
- (chưa có)
