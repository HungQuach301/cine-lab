# CHECKPOINT — LOOK-T4-V2 (K2C-T4-02 London, vòng look thứ hai)

> Nhánh thật: `k2c-t4-02-look2` (gốc `origin/k2c-t4-02-look` @5123bebf). Nhánh mặc định của bộ khung (`claude/practical-mendel-u8qqn3`) KHÔNG dùng (lệnh gọi tên nhánh).

## Trạng thái
- 23/10 ≈ 17:25 UTC: ĐANG LÀM. Dữ liệu nền tải lại (container mới: /var/tmp trống) — OSM, LiDAR, tư liệu, vân, atlas lửa (138 s); hình học look v2 dựng lại (SHA khác bản LOOK-T4 vì OSM sống đổi: lô 42 898 → 42 951, toà 2026 +1 — ghi sự cố); hình học V2 (`hinh_hoc_v2.py` + `cong_trinh_v2.py`: St Paul's, Monument tại vị trí OSM, White Tower chi tiết cao); nướng 1666/1940/2026 (84/98/… s).
- Trang dựng `design/k2v/ldn/look2.js` (lửa có lõi + quầng + tàn lửa theo gió, khói ngày đặc khối/tách tầng, chân khói hắt đỏ, vật liệu công trình có tên, chống 'đồ chơi', mặt nạ mã công trình). Đang: đo công trình ở P1, rồi dựng 8 khung V2.
- Chi phí đến giờ: Gemini 0 · OpenAI 0 · Claude API 0 · RunPod 0.

- 23/10 ≈ 17:35 UTC: 8 khung V2 3D (spp 24) + mặt nạ + LUT xong; đo công trình xong (`reports/look-t4-v2/do/cong-trinh.json`); Cycles GPU 2 khung M2-dem (RTX 5090 74 s, RTX 4090 117 s; pod đã tắt, HTTP 204); tấm nền: Gemini Batch lượt 1 (4 tấm, chờ 146–209 s), OpenAI lượt 1 (4) + lượt 2 (3); cổng kiểm đang chạy; timelapse 3/8 s đang dựng.
- Chi phí đến giờ (sổ): Gemini ≈ $0,14 · OpenAI ≈ $0,53 (ảnh) + kiểm · Claude (kiểm) xem `cost.jsonl` · RunPod ≈ $0,05.

## Lệnh bổ sung đã áp
- (chưa có)
