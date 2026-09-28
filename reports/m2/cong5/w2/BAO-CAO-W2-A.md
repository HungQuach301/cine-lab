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
  - Bằng chứng: `s42_keo-mu_khung2914-2936.jpg` (khung toàn cục 2914, 2922, 2930, 2936 = 1,92 · 2,25 · 2,58 · 2,83 s trong s42).
  - Bảng `hat_back` từng shot: `continuity/canh-5.md`.
- **Ảnh 4 kiểm mù:** khung toàn cục **2554** (106,40 s, khung 34 của s39), giữa cụm "keep a little dark…".
  - Mốc câu đo từ take L4: "Just…" 104,32–104,84 s; "keep a little dark for the ones who need it" 105,87–109,08 s.
  - Video nhóm: `/var/tmp/cine-out/W2/full/video_s33-s34-s35-s36-s37-s37w-s38-s39-s40-s40w-s41-s42a-s42b-s42.mp4`, khung thứ 634 (đếm từ 0).
  - Ảnh: `anh4_s39_khung2554.jpg`. s39 máy tĩnh, mặt gần chính diện suốt shot (chưa có khẩu hình).
- **Rủi ro:**
  - các shot mặt Ida (s26, s31, s36, s37, s39, s40) sẽ render lại khi có A3;
  - s31 có vệt sáng cứng từ đèn lồng trên má (cần xem lại khi có mặt A3);
  - chim s32, s48 còn mờ (R4).

# Giai đoạn D — sửa lỗi continuity (báo cáo rà `reports/m2/cong5/continuity.md`)
Đã merge nhánh tích hợp @c1479af. ORDER không đổi. Render lại 7 shot (516 khung) qua hàng đợi, một nhóm `sua-continuity`:
- chờ 0 s, chạy 549 s, 1,06 s/khung;
- `/var/tmp/cine-out/W2/full/timing_s27-s33-s34-s41-s42a-s42b-s43.json`, `video_s27-s33-s34-s41-s42a-s42b-s43.mp4`.
Ảnh trước (trên) / sau (dưới): `D_C1_s27_thang.jpg`, `D_C3-N2_s41-s42a-s42b.jpg`, `D_C4_s43_troi.jpg`, `D_N3-N4_s33-s34.jpg`.

| Lỗi | Sửa | Shot render lại |
|---|---|---|
| C1 thang mất ở s27 | Bộ tường chim đặt thang tựa phía bắc L11: (−2,2; 3,35), nghiêng 0,36 rad = `ladderAt(11)` của bộ phố. Thang có mặt suốt cảnh 4; ở các shot khác của cảnh 4 nó nằm ngoài khung. | s27 |
| C3 nhảy trục ở s41, s42a | s41: Ida ở chân thang phía tây (7,9; −4,4), Cas phía đông (8,9; −4,6). s42a: Ida lùi ra lòng phố (6,8; −2,5). Cả hai shot: Ida trái, Cas phải, như s40w và s42. | s41, s42a |
| C4 trời s43 | Bộ thành phố đêm dùng trời sao `nightSky` như s10, sương xa tối xanh; bỏ trời vẽ xám lilac. Dải trời trên cùng đo RGB (85, 98, 137) → **(13, 25, 68)**. | s43 |
| N2 cách cầm đèn | Cas ôm đèn sát ngực bằng hai tay (`casHug`), cùng tư thế ở s41 (cuối), s42a, s42b. Ở s42b máy nhìn nghiêng nên đèn vẫn thấy ở phía trước thân (xem rủi ro). | s41, s42a, s42b |
| N3 V2 | Đèn lồng (−0,05; 3,0). Ida (−0,62; 1,45): bóng ×1,94, đỉnh ≈ 3,2 m, nằm trong vùng vách được đèn rọi nên vành mũ của bóng hiện ra; lệch trái 0,53 m. Cas (0,75; 0,8): bóng ×1,36, ≈ 1,8 m. Tỷ lệ bóng bà / bóng cậu 1,77. Nửa tối: PCF radius 4, giả lập nguồn ~12 cm ở render 1 mẫu. s34 đổi 26 mm, thấy nền: vệt bóng nối chân mỗi người với bóng của họ trên vách. | s33, s34 |
| N4 cột lạ ở s33 | Là cột điện gang của bộ khoá Cổng 3 s5 (x 3,45; z 4,9). Không có trong địa lý chốt → ẩn trong lớp bọc `addBayStreet`. | s33 (s42b cũng render lại) |
| N5 tài liệu | Sửa `canh-4.md` (s24c nhìn **trái**; cột phố chính có ở cả hai bộ; thang), `canh-5.md` (trục s41/s42a, BAY mới, s34, s35 mép phải là hông nhà kho, cách cầm đèn), `LAYOUT-W2.md` (bảng shot, R2, Q-W2-3). | — |

Rủi ro còn lại:
- s42b: đèn nhìn nghiêng vẫn ở trước thân. Tư thế đã đồng nhất; nếu vẫn đọc là "chìa xa" thì cần đổi máy s42b.
- N3 cần kiểm mù xác nhận.
- s33: Ida vẫn chồng một phần lên mép bóng mình (khoảng 0,15 m).

# Giai đoạn A2 — quyết định chủ dự án sau Cổng 5 (B1 + C2 (a)(b)(c)); chỉ probe, chưa render
Đã merge nhánh tích hợp @633a217. Chi tiết và số đo: `shots/layout/LAYOUT-W2.md` mục 0. Ảnh trước/sau: `v2_B1_s25-s27-s35-s37w.jpg`, `v2_a_s33-s34.jpg`, `v2_b_s40-s40w-s41.jpg`, `v2_c_s30-s46-s38.jpg`.
- **Probe:** 3 lần (p19: 22 shot, gồm W1 s23, s24, s24c; p20: s25, s27). Không render nặng.
- **Tổng phim:** 140,5 s (s33 −2,0 s). Mốc sau 1:25,0 lùi 2,0 s. Ảnh 4 kiểm mù đổi sang khung toàn cục 2506.
- **Cần render lại khi P mở giai đoạn C2** (tổng 1628 khung):
  - s25–s32 (504 khung): B1, bộ tường;
  - s33, s34 (168 khung): (a);
  - s35, s36, s37, s37w, s38, s39, s40, s40w, s41, s42a (≈ 572 khung): B1 (vũng sáng cột); (b) ở s40w, s41, s42a;
  - s42b, s42 (120 khung): thời gian dời, đá lát phố ngoài;
  - s44–s47 (264 khung): (c) đá lát ngõ; cảnh 6 dời mốc.
  - s43, s45c, s48 chỉ dời mốc, hình không đổi.
- **Ước thời gian chạy:** bộ tường 2,45 s/khung, bộ phố/hốc 1,1 s/khung, ngõ 0,95 s/khung → ≈ 1234 + 185 + 630 + 100 + 250 ≈ **40 phút**, chưa kể thời gian chờ hàng đợi.

# Giai đoạn C2 — render đầy đủ với mặt Ida A-α (sheet v1.4)
Đã merge nhánh tích hợp @b378416; P đã sửa lỗi cú pháp s46 của tôi. Bài học: sau lần sửa cuối phải probe lại (và `node --check`) trước khi commit.

**Phơi sáng cận mặt:** theo bảng W3. Tỷ lệ cháy mặt đo trên probe là % điểm ảnh có kênh ≥ 250 trong vùng mặt.
| Shot | Chỉnh | Cháy mặt |
|---|---|---|
| s31 | phơi sáng 1,0 → 0,45 | 0,07 % |
| s36 | EK 2,0 → 1,3 | 0,52 % |
| s37 | EK 2,0 → 1,3 | 0,61 % |
| s39 | EK 1,0 → 0,8 | 0,15 % |

- Các shot cận mặt đều ≤ 3 %. Nền không quá tối nên giữ nguyên bảng W3.
- `shadowLamps: [11]` cho faceShot: **dùng**. Bóng vành mũ thật rơi lên trán. Nền sau L11 tối nên bóng đầu không lọt khung ở s36, s37, s39.
- s37: máy lệch +10° (trước −10°). Thanh thang không còn sáng ở mép trái; chỉ còn một đoạn tối nhỏ ở góc dưới trái.

**Render:** 3 nhóm qua hàng đợi, 1956 khung. Tất cả 29 shot đều render lại, vì mặt và tóc mới xuất hiện ở mọi shot có Ida và mốc thời gian đã dời. Số liệu từ `log.tsv`:
| Nhóm | Khung | Chờ | Chạy | s/khung |
|---|---|---|---|---|
| c2-canh4 (s25–s32) | 504 | 713 s | 1067 s | 2,12 |
| c2-canh5 (s33–s42) | 972 | 427 s | 1280 s | 1,32 |
| c2-canh6 (s43–s48) | 480 | 0 s | 465 s | 0,97 |

- Tệp timing ở `/var/tmp/cine-out/W2/full/`:
  - `timing_s25-s26-s27-s28-s29-s30-s31-s32.json`
  - `timing_s33-s34-s35-s36-s37-s37w-s38-s39-s40-s40w-s41-s42a-s42b-s42.json`
  - `timing_s43-s44-s45-s45c-s46-s47-s48.json`
- Bản render giai đoạn D (s27, s33, … theo mốc cũ) đã chuyển vào `full/cu_giai-doan-D/` để không lẫn khi ghép.
- **Làm lại: 0.** Đã xem thumbs a/b/c cả 29 shot; không lỗi mới.

**Ảnh 4 kiểm mù:** khung toàn cục **2531** (105,46 s, khung 59 của s39), giữa cụm "keep a little dark for the ones who need it" (103,87–107,08 s).
- Trong video nhóm canh5 là khung thứ 611 (đếm từ 0).
- Ảnh: `anh4_s39_khung2531.jpg`. Máy tĩnh, mặt gần chính diện, vành mũ đổ bóng lên trán.
- Khung 2506 báo ở A2 cũng nằm trong câu (104,42 s) nhưng gần đầu cụm hơn.
