# Báo cáo kiểm L1 — shotB.mp4

- Kết luận: **TRƯỢT**
- Profile: `shot` · Công cụ: cinecheck 1.1.0 · Thời điểm (UTC): 2026-09-27T03:07:08Z
- LOCK: khớp (`d97f9b017ea2efd89be98dbecfeeb0e3d57ff44f9cfe26172703da3f1b975c3f`)
- Đếm: TRƯỢT 1

| Mã | Luật | Cấp | Kết quả | Số đo chính |
|---|---|---|---|---|
| C3 | Đúng model: tỷ lệ bộ phận so với model sheet, có tính nhiễu đo | Chặn | **TRƯỢT** | hệ số phân giải mặt nạ/khung đo từ kích thước PNG (nhỏ nhất) = 1 × (ngưỡng >= 2) ✗; hệ số phân giải mặt nạ/khung đo từ kích thước PNG (lớn nhất) = 1 × (ngưỡng <= 4); mặt nạ cùng kích thước, hệ số ngang = dọc = True  (ngưỡng == True); 'scale' khai báo khớp hệ số đo (bỏ trống được) = True  (ngưỡng == True); biên trên |lệch| + U lớn nhất = 1.83 % (ngưỡng <= 3); bộ phận–khung lệch chắc chắn > 3% = 0  (ngưỡng <= 0); bộ phận–khung không chứng minh được ≤ 3% (nhiễu đo) = 0  (ngưỡng <= 0); khung mẫu (mỗi 12 khung) thiếu mặt nạ = 0  (ngưỡng <= 0); độ khớp biên mặt nạ–cạnh ảnh render thấp nhất = 4.4  (ngưỡng >= 1.5) |

## Chỉ số nằm trong ±5% quanh ngưỡng
- Không có.

## Chi tiết từng luật

### C3 — Đúng model: tỷ lệ bộ phận so với model sheet, có tính nhiễu đo (4.C — Nhân vật, cấp Chặn): TRƯỢT
- Định nghĩa đo: <video>.parts/parts.json: mặt nạ từng bộ phận xuất từ render cho mọi khung chia hết cho 12. v1.1 (Q-C3): mặt nạ bắt buộc ở độ phân giải gấp s = 2–4 lần khung; s đo từ kích thước PNG (rộng/rộng và cao/cao phải bằng nhau, mọi mặt nạ cùng cỡ), trường 'scale' nếu có phải khớp s đo. Chống phóng to mặt nạ thấp hơn: tập vị trí biên phân biệt (x chuyển tiếp ngang, y chuyển tiếp dọc) quy về pha lưới s (k = round(s) ngăn); tỷ lệ dồn vào 1 pha phải ≤ 1/k + (1 − 1/k)/2 (s=2: 0,75; s=3: 0,67; s=4: 0,625) với ≥ 40 vị trí (render thật ≈ 1/k; phóng to từ mặt nạ nhị phân ≈ 1,0). Độ dài = bề dài chiếu lên trục chính PCA của tâm điểm ảnh + 1 px; tỷ lệ = độ dài bộ phận / độ dài đầu; lệch = tỷ lệ / tỷ lệ model sheet − 1. Nhiễu đo U(s) = √((δ/(s·L_bộ phận))² + (δ/(s·L_đầu))²), L theo px video, δ = 1 px mặt nạ; hiệu chuẩn Monte Carlo trong selftest ở s = 1, 2, 4 (phủ 100% sai số ở đầu 40–146 px video). Quyết định kiểu ISO 14253-1: đạt khi |lệch| + U ≤ 3%; trượt chắc chắn khi |lệch| − U > 3%; giữa hai mức = không chứng minh được. Chống khai man: biên bóng nhân vật (hợp các mặt nạ) phải nằm trên cạnh ảnh render: độ lớn cạnh trên biên / trung vị trên biên dịch ±6 px theo 8 hướng.
- Ngưỡng: Hệ số mặt nạ/khung đo được trong [2, 4], ngang = dọc, khớp số khai; pha biên ≤ 1/k + (1 − 1/k)/2; 0 bộ phận–khung trượt chắc chắn; 0 bộ phận–khung không chứng minh được; 0 khung mẫu thiếu mặt nạ; độ khớp biên ≥ 1,5 (ngưỡng 3% theo khung mục 4.C, nội bộ; 1,5 và ngưỡng pha nội bộ).
- Ghi chú: Model sheet: model-sheet.json. Mặt nạ 1920×1080 px trên khung 1920×1080 → hệ số đo ×1 (khai báo: 1). Đầu cao 146.0–146.0 px video. Lệch lớn nhất 0.84%. 757 vị trí biên phân biệt; tỷ lệ dồn 1 pha — (trải đều ≈ 1.00).
- Ghi chú: Q-C3: mặt nạ phải render ở độ phân giải gấp 2–4 lần khung video (đo từ kích thước PNG).
- Bằng chứng: `{"do": [{"khung": 0, "bo_phan": "torso", "ty_le": 1.9041, "sheet": 1.9, "lech_pct": 0.22, "U_pct": 0.77, "ket_qua": "đạt"}, {"khung": 0, "bo_phan": "upper_arm", "ty_le": 0.958, "sheet": 0.95, "lech_pct": 0.84, "U_pct": 0.99, "ket_qua": "đạt"}, {"khung": 0, "bo_phan": "forearm", "ty_le": 0.8559, "sheet": 0.85, "lech_pct": 0.7, "U_pct": 1.05, "ket_qua": "đạt"}, {"khung": 0, "bo_phan": "thigh", "ty_le": 1.2079, "sheet": 1.2, "lech_pct": 0.66, "U_pct": 0.89, "ket_qua": "đạt"}, {"khung": 0, "bo_phan": "shin", "ty_le": 1.1571, "sheet": 1.15, "lech_pct": 0.62, "U_pct": 0.91, "ket_qua": "đạt"}], "do_khop_bien": {"0": 4.4}}`
