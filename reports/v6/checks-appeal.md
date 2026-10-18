# Khiếu nại luật — V6 (phiên P/xưởng V6 → phiên K). Không đọc mã checks/; chỉ dựa trên kết quả k2check 1.15 và reports/K-1.15-BAO-CAO.md §3.1/§8b.

## A-V6-1 · K-LAI-3…6 áp cho VÂN AI HC7 (ai_texture) như tấm C khung neo
- **Hiện tượng** (reports/v6/do/k2check-1.15-doan-thu.txt): đoạn thử V6 có shot a khai `ai_texture` (vân chi tiết King's Bastion lấy từ khối AI PT3, quy trình 5 điểm PT3 §9, Q-PT3-1). Khối `lai:` khai `kiem_du_kien` + `goi_api` của PT3 → K-LAI-3 "0 tấm dùng", K-LAI-5 "133 lệnh sinh > 1 + 2", K-LAI-6 "thiếu mask.pct_duoc_sua" ×133, K-LAI-4 THIẾU `bao_ve`.
- **Lý do khiếu nại:** K-LAI-3…6 được viết cho **tấm C khung neo** (PT2: 1 tấm/khung neo × mốc, mặt nạ sửa, vùng bảo vệ = A). Vân HC7 là **bản đồ chi tiết bề mặt** (D = I/Gσ(I)) nhân lên tường đá trong cảnh 3D; không có "tấm dùng", không có mặt nạ sửa trên khung, không có khung A để so. Sổ PT3 hợp lệ theo luật của nó (133 khối, C2PA 133/133, kiểm dữ kiện 0 lỗi chắc).
- **Đề xuất:** K tách nhánh `ai_texture` (vân bề mặt) khỏi `ai_image` (tấm C): với `ai_texture` chỉ áp K-LAI-1 (≤ 20 % thời lượng — đo được: 19,5 %, ĐẠT, trong ±5 % ngưỡng), K-LAI-2 (nhãn suốt shot ≥ 38 px — ĐẠT, 40 px, 36/36 mẫu kể cả khung hoà đen), và kiểm sổ nguồn (C2PA + kiểm dữ kiện của khối AI) thay cho K-LAI-3…6.
- **Tác động nếu giữ nguyên:** mọi tập dùng HC7 đều TRƯỢT K-LAI-3/5/6 dù không có tấm C.

## A-V6-2 · A4 (SMR) TRƯỢT khi đoạn không có lời
- Đoạn thử V6 không lời (ElevenLabs 0 theo lệnh). Chuỗi âm thanh mới (`MIX=audio`) ghi `smr: null` → A4 TRƯỢT "không có stem". Đề xuất: A4 KHÔNG ÁP khi tập không có lời (không có `vo`).
