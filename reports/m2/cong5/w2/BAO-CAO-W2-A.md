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

# Giai đoạn C — render đầy đủ (960×540, 1 mẫu, qua hàng đợi)
Nhánh gốc: merge `claude/cine-lab-m2-cong5-layout-24o5fp` @ce40df1. ORDER không đổi. Đầu ra ở `/var/tmp/cine-out/W2/full/` (không commit).

| Nhóm | Shot | Khung | Chờ (s) | Chạy (s) | s/khung (thật, gồm dựng) | Video |
|---|---|---|---|---|---|---|
| canh4 | s25–s32 | 504 | 241 | 1237 | 2,45 | `video_s25-…-s32.mp4` (28 MB) |
| canh5 | s33–s42 | 1020 | 832 | 1128 | 1,11 | `video_s33-…-s42.mp4` (55 MB) |
| canh6 | s43–s48 | 480 | 489 | 447 | 0,93 | `video_s43-…-s48.mp4` (26 MB) |

Tổng 2004 khung, chạy 2812 s, chờ 1562 s (theo `/var/tmp/cine-queue/log.tsv`); trung bình 1,40 s/khung.

- **Làm lại: 0 shot.** Đã xem thumbs a/b/c cả 29 shot; không lỗi mới so với probe giai đoạn A.
  - s32 thử phơi sáng 0,7 bằng probe: chim không rõ hơn đáng kể → giữ 1,0.
- **Mũ Ida (quyết định chủ dự án):** bà kéo mũ lại ở cuối s42. Đã sửa **trước khi** nhóm canh5 chạy tới s42, nên không phải render lại.
  - Bằng chứng: `s42_keo-mu_khung2926-2950.jpg` (khung toàn cục 2926, 2934, 2942, 2948).
  - Bảng `hat_back` từng shot: `continuity/canh-5.md`.
- **Ảnh 4 kiểm mù:** khung toàn cục **2554** (106,40 s, khung 34 của s39), giữa cụm "keep a little dark…".
  - Mốc câu đo từ take L4: "Just…" 104,32–104,84 s; "keep a little dark for the ones who need it" 105,87–109,08 s.
  - Video nhóm: `/var/tmp/cine-out/W2/full/video_s33-s34-s35-s36-s37-s37w-s38-s39-s40-s40w-s41-s42a-s42b-s42.mp4`, khung thứ 634 (đếm từ 0).
  - Ảnh: `anh4_s39_khung2554.jpg`. s39 máy tĩnh, mặt gần chính diện suốt shot (chưa có khẩu hình).
- **Rủi ro:**
  - các shot mặt Ida (s26, s31, s36, s37, s39, s40) sẽ render lại khi có A3;
  - s31 có vệt sáng cứng từ đèn lồng trên má (cần xem lại khi có mặt A3);
  - chim s32, s48 còn mờ (R4).
