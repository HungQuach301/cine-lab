# Báo cáo kiểm L1 — shotB.mp4

- Kết luận: **ĐẠT**
- Profile: `shot` · Công cụ: cinecheck 1.0.0 · Thời điểm (UTC): 2026-09-27T01:32:29Z
- LOCK: khớp (`b86c5d75f14abe5cba7b08c58c95c36e0c1fc49f73af030357f9cc95db7268f8`)
- Đếm: ĐẠT 1

| Mã | Luật | Cấp | Kết quả | Số đo chính |
|---|---|---|---|---|
| C3 | Đúng model: tỷ lệ bộ phận so với model sheet, có tính nhiễu đo | Chặn | **ĐẠT** | biên trên |lệch| + U lớn nhất = 1.83 % (ngưỡng <= 3); bộ phận–khung lệch chắc chắn > 3% = 0  (ngưỡng <= 0); bộ phận–khung không chứng minh được ≤ 3% (nhiễu đo) = 0  (ngưỡng <= 0); khung mẫu (mỗi 12 khung) thiếu mặt nạ = 0  (ngưỡng <= 0); độ khớp biên mặt nạ–cạnh ảnh render thấp nhất = 4.4  (ngưỡng >= 1.5) |

## Chỉ số nằm trong ±5% quanh ngưỡng
- Không có.

## Chi tiết từng luật

### C3 — Đúng model: tỷ lệ bộ phận so với model sheet, có tính nhiễu đo (4.C — Nhân vật, cấp Chặn): ĐẠT
- Định nghĩa đo: <video>.parts/parts.json: mặt nạ từng bộ phận xuất từ render cho mọi khung chia hết cho 12 (được phép render mặt nạ ở độ phân giải gấp 'scale' lần). Độ dài = bề dài chiếu lên trục chính PCA của tâm điểm ảnh + 1 px; tỷ lệ = độ dài bộ phận / độ dài đầu; lệch = tỷ lệ / tỷ lệ model sheet − 1. Nhiễu đo U = √((1 px/L_bộ phận)² + (1 px/L_đầu)²), hiệu chuẩn Monte Carlo trong selftest (phủ 100% sai số ở đầu 40–146 px; M0 đo ~1,3% ở đầu 57 px). Quyết định kiểu ISO 14253-1: đạt khi |lệch| + U ≤ 3%; trượt chắc chắn khi |lệch| − U > 3%; giữa hai mức = không chứng minh được. Chống khai man: biên bóng nhân vật (hợp các mặt nạ) phải nằm trên cạnh ảnh render: độ lớn cạnh trên biên / trung vị trên biên dịch ±6 px theo 8 hướng.
- Ngưỡng: 0 bộ phận–khung trượt chắc chắn; 0 bộ phận–khung không chứng minh được; 0 khung mẫu thiếu mặt nạ; độ khớp biên ≥ 1,5 (ngưỡng 3% theo khung mục 4.C, nội bộ; 1,5 nội bộ).
- Ghi chú: Model sheet: model-sheet.json. Đầu cao 146.0–146.0 px video (mặt nạ ×1). Lệch lớn nhất 0.84%.
- Bằng chứng: `{"do": [{"khung": 0, "bo_phan": "torso", "ty_le": 1.9041, "sheet": 1.9, "lech_pct": 0.22, "U_pct": 0.77, "ket_qua": "đạt"}, {"khung": 0, "bo_phan": "upper_arm", "ty_le": 0.958, "sheet": 0.95, "lech_pct": 0.84, "U_pct": 0.99, "ket_qua": "đạt"}, {"khung": 0, "bo_phan": "forearm", "ty_le": 0.8559, "sheet": 0.85, "lech_pct": 0.7, "U_pct": 1.05, "ket_qua": "đạt"}, {"khung": 0, "bo_phan": "thigh", "ty_le": 1.2079, "sheet": 1.2, "lech_pct": 0.66, "U_pct": 0.89, "ket_qua": "đạt"}, {"khung": 0, "bo_phan": "shin", "ty_le": 1.1571, "sheet": 1.15, "lech_pct": 0.62, "U_pct": 0.91, "ket_qua": "đạt"}], "do_khop_bien": {"0": 4.4}}`
