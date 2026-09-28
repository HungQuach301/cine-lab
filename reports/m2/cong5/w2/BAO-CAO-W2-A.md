# Báo cáo W2 — Cổng 5, giai đoạn A (layout cảnh 4–6, s25 → s48)

Chi tiết layout, V1–V4, D2, API và đề xuất: `shots/layout/LAYOUT-W2.md`. Continuity: `shots/layout/continuity/canh-4.md`, `canh-5.md`, `canh-6.md`. Manifest Cổng 6: `shots/layout/shots_w2.json` (29 shot, 2004 khung).

## Kết quả
- Thời lượng giữ 83,5 s; tổng phim 142,5 s; id không đổi; mốc thoại và sự kiện không đổi.
- V1, V2, V3, V4 sửa bằng máy, dàn dựng, bối cảnh, quang học thật. Ảnh trước (trên) / sau (dưới) ở thư mục này:
  - `V1_s42b-s42_…`;
  - `V2_s33-s34_…`;
  - `V3_s27-s35-s37w_…`, `V3_noi-W1_s23-s24-s24c_sau.jpg`;
  - `V4_s26_…`;
  - `them_…` (sửa thêm s28, s32, s38, s45, s47, s48).
- D2: mũ dưới lửa #5a3f39 (nâu xám), dưới điện #1b1e2c (đen xanh), đo trên cùng khung s40 trước/sau khi tắt lửa.
- Đã merge nhánh tích hợp hai lần (W1 96f35af; W3 0f09602). Đã tích hợp `facelight.js` cho s26, s36, s37, s39.
- Chỗ nối W1 đã probe (s23, s24, s24c): `casSpot` (10,35; −7,15), cách L11 4,0 m.

## Số đo vận hành (thật)
- **Probe:** 17 lần chạy, tổng 135 shot-probe (3 khung/shot, 960×540), không render đầy đủ, không dùng hàng đợi (việc nhẹ).
  - Lần gốc (29 shot): 413 s.
  - Lần cuối (32 shot, gồm 3 shot W1 để kiểm chỗ nối): 528 s.
  - Probe mỗi khung: 1,4–8,7 s tuỳ bộ và tải máy (máy 4 vCPU dùng chung với W1, W3; load 4–9).
- **Thời gian thật của phiên:** 23:54 → 01:15 UTC (≈ 1 giờ 21 phút).
- Không có tài sản ngoài mới (mọi hình dựng thủ tục từ thư viện Cổng 3) → không thêm dòng `RIGHTS.md`.
- Lệnh kiểm của phiên K: giai đoạn A không có lệnh kiểm cho W2 (P chạy luật máy ở giai đoạn D). Không đọc, không sửa `checks/`.

## Chỉ số gần ngưỡng
Không có chỉ số luật máy nào được đo ở giai đoạn A.

## Đang chờ
- **P:** Q-W2-3 (cột điện phố chính trong bộ phố); kiểm chỗ nối s24c → s25 (Ida xuống thang trong s25, ngoài hình).
- **Chủ dự án:**
  - Q-W2-1: tường chim là hông nhà kho;
  - Q-W2-2: mũ Ida ở cảnh 6;
  - Q-W2-4: quầng trắng chân trời.
