# CHECKPOINT — THU-B-T4 (vòng thử B + D chống "đồ chơi", K2C-T4-02)

> Nhánh thật: `ccr-ce664665-996oyl` (harness buộc; lệnh gọi `k2c-t4-02-thu-b`). Gốc origin/main @2414d1d3 + merge (không squash) origin/checks-1-17-5 @1dc8be60 → merge `ea15a120`.

## Trạng thái
- 24/10 04:35 UTC: bắt đầu. Đọc tài liệu nền (K1175 §5–§7, RULES 1.17.5, Kinh thánh §11.3/§11.4/§14.7/§15/§19, LOOK-T4-V2 §1/§4, BAI-HOC-K2, BAI-HOC-LL). Hook pre-commit + pre-push cài (trước lần đẩy đầu).
- 04:37–04:48: container mới, `/var/tmp` trống → dựng lại dữ liệu nền bằng đúng lệnh LOOK (`scripts/k2ldn/thu-b/dung_lai_du_lieu.sh`): OSM, LiDAR, Doornick, vân CC0, atlas lửa, hình học look2, nướng 1666.6/2026.7. `ldn2.bin` SHA `bd776509…` ≠ LOOK-T4-V2 `73e68223…` (OSM sống đổi: lô 42 951 → 42 947) — ghi sự cố.
- 04:50: đang dựng hình học look3b (mã nhà/mặt phẳng) + nướng 1938.7; viết `look3.js` (sinh từ look2.js bằng `tao_look3.py`), máy thử `channel-k2/k2c-t4-02/thu-b/may/`.
- Chi phí đến giờ: OpenAI 0 · Claude API 0 · Gemini 0 (không gọi) · ElevenLabs/RunPod/YouTube 0.

- 05:25: look3.js ≡ look2.js từng điểm ảnh (M4-trung 640×360, sai khác 0). Hình học look3b SHA = look2 (`bd776509…`); look3d (D) 4 777 768 tam giác (V2 2 275 896), 95 548 nhà thường, số lô giữ nguyên 42 947. Nướng look3d 1666.6/2026.7, look2 1938.7.
- Sự cố đã sửa: mã nhà 24 bit lệch −1 ở mã bội 256 (nội suy varying) → làm tròn trong shader; dựng lại mặt nạ 3/4 khung B.
- AI: D2 4 atlas (mặt tiền 1666/gạch/2026 + mái) $0,303; B lượt 1 cả 3 khung $0,228. Ảnh AI + ảnh vào trong `channel-k2/k2c-t4-02/thu-b/ai/`.
- Đang: dựng khung D (V2/D/mặt nạ), timelapse V2 khung B, rồi mặt nạ 3/4 khung B; tiếp: ghép B, chiếu 3D, k2check.

- 06:05: k2check 1.17.5 chạy được trên tấm BMN (khai `channel: k2`, `khung_sach`, log shot tối thiểu). Kết quả lượt 1/2: BE-MAT-NHA (a) 0 Chặn ở cả 3 khung; (b) 0/255; (w) B3 l2 1, M1 l1 1, M1 l2 2; M4 0. Hai lỗi phía K: N2P-* KeyError 'so_doan_lan' khi khung không có nước (M4, B3); N2P-1 (a) tính vùng BMN là lớp (a) → `reports/thu-b-t4/khieu-nai-K.md`. Chọn lượt 2 (bmn-v2b) cả 3 khung.
- Chiếu 3D (B ii): B3 khung 0 ΔE 2,36 / p95 9,77 sau 3 vòng; M4 4,62 / 14,06 → thêm vòng 3–4 đang chạy. Đang: timelapse chiếu B3, vòng thêm M4; tiếp: M1 chiếu, D dựng lại (hình học D bỏ lan can/thiết bị ở toà OSM có tên — 4 601 432 tam giác), D2, đo ước tác động (P1/P3/P5/P6/P8).

## Lệnh bổ sung đã áp
- (chưa có)
