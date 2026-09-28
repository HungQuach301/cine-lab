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

# Giai đoạn continuity v3 — sửa theo rà continuity v2 (C5, N2, N3, N6, N7, N8, N9)
Đã merge nhánh tích hợp @dee0bd3 (kèm báo cáo rà @67691da). Làm đúng trình tự P yêu cầu: `node --check` và probe sau lần sửa mã cuối, rồi mới render. Sau render chỉ sửa chữ mô tả trong `S({...})` (why/light/action/move); probe lại s33, s42b: ảnh trùng từng điểm ảnh với bản render.

| Mục | Trước (v2) | Sau (v3) |
|---|---|---|
| **C5** (chặn) s33 | Ngoài vòm trắng phẳng: mặt tường quanh vòm TB (217, 217, 221) | `addBayStreet({dark})`: tràn điện xa × 0,05 (như s35), hổ phách L11 từ phải (nguồn điểm thật ở chỗ L11), trời lạnh 0,22. Mặt tường TB: trái (48, 46, 52), phải (91, 69, 61); trong hốc (146–166, 90–98, 44–46). Trong hốc vàng, ngoài vòm đêm lạnh tối. s34 dùng cùng ánh sáng; không thấy ngoài vòm. s42b, s42 (sau P5) giữ ngoài vòm trắng. |
| **N3** s33 | Ida đứng chồng lên nửa phải bóng của bà | Quang học thật: đèn lồng dời từ x −0,05 sang 0,2; Cas từ 0,75 sang 0,9; máy dịch trái 0,4 m (trước: phải 0,6 m). Bóng Ida lệch trái bà 0,77 m (trước 0,53 m), ×1,94. Bóng Cas lệch phải 0,25 m, ×1,36. Trên khung c: đầu và vành mũ của bóng nằm trên-trái người, tách khỏi thân. |
| **N2** s41 → s42b | s42a ôm ngực; s42b chìa ra trước, rồi xách bên hông | `casHug` chặt (vai −12°, khuỷu −112°): cổ tay trước ngực, đèn áp bụng. Dùng chung cho s41, s42a, s42b (khi đi). |
| **N7** s42b → s42 | Cuối s42b đứng xách đèn, đầu s42 đã ngồi xổm với đèn trên nền | s42b: đi 0–1,3 s; quay ra vòm 1,1–1,5 s; ngồi xổm 1,45–2,0 s về `warm_hands_copy` (đúng tư thế mở s42); đặt đèn xuống nền 1,6–2,0 s tại (−0,38; 3,10), đúng chỗ đèn ở s42. Khung c: Cas ngồi, đèn trên nền, bóng lớn trên vách. |
| **N6** s30 | "Mở cửa đèn" 0,012 → 0,8 bật cóc ở 0,95 s rồi lên 3,0 | P chọn đèn cháy liên tục. Hình s26/s27 để nguyên: kính đèn ở hông sáng, hông khuất máy. Chỉ s30 bị lệch trên hình vì vũng sáng bật cóc khi tháo đèn. Nay hắt sáng tăng liên tục 0,012 → 3,0 trong 0,8–1,85 s: đèn ra khỏi thân bà rồi hạ sát tường. Sheet bỏ mọi chữ "mở/đóng cửa". |
| **N8** s43 | Ô được chọn bị nhà phía trước che; mặt tiền có hàng chục ô "nâu cam" (ô tối bị quầng tường vôi ấm nhuộm) | Ô cửa khác đều là kính lạnh: ô gần (< 70 m) trắng lạnh, ô xa từng sáng trắng lạnh, ô xa tối xanh xám. Một ô hổ phách được chọn theo điều kiện: nhìn thấy (tia máy–ô không vướng), xa chấm đèn điện trắng, mặt nhà ngoài tầm đèn điện (nền tối), cách máy 55–140 m. Ô được chọn cách máy 130,9 m, tại khung (0,555; 0,453). |
| **N9** sheet | Số cũ sau A2 | `canh-4.md` viết lại bảng toạ độ theo B1: casSpot (14,3; −7,15), cột trong sân (17,0; −5,9), đầu hồi x 18,5, Cas → L11 7,1 m. Máy s25–s32 đã cộng DX. Bỏ "ống thoát nước" ở s25 (không có trên hình). Lịch đèn lồng theo N6. `canh-5.md`: 1:20,0–2:00,5; P5 1:39,2; L11 tắt 1:49,2; nhịp s33 5 s; bảng "ai giữ đèn lồng, cầm thế nào"; C5. `canh-6.md`: 2:00,5–2:20,5; L11 tắt 1:49,2; N8. `LAYOUT-W2.md`: §0 thêm các dòng v3; §1 140,5 s; §2 cột thời gian và máy; §5 `houseX0N` 18,5, `casSpot`, `wallPost`; §7 R1/R2/R6. `shots_w2.json` sinh lại (29 shot, 1956 khung). |

**Render** (1 lệnh qua hàng đợi, 960×540, 1 mẫu). Chỉ render các shot đổi: s30, s33, s34, s41, s42a, s42b, s43. s42 không đổi mã nên không render lại.
| Nhãn | Khung | Chờ | Chạy | Theo shot (s) |
|---|---|---|---|---|
| W2/cv3 | 444 | 0 s | 569 s | s30 131 · s33 112 · s34 55 · s41 46 · s42a 64 · s42b 49 · s43 110 |

- Tệp mới ở `/var/tmp/cine-out/W2/full/`: `timing_s30-s33-s34-s41-s42a-s42b-s43.json` và `video_s30-s33-s34-s41-s42a-s42b-s43.mp4` (27,6 MB). Tệp timing mới hơn thắng khi ghép.
- **Làm lại: 0.** Probe trung gian: 4 vòng cho s43 (chọn ô), 2 vòng cho s33 (mức tối). Kết quả probe cuối trùng bản render.

**Lệnh kiểm của K** (`checks/run.py <video> --profile shot`, qua hàng đợi W2/cv3-kiem: chờ 0 s, chạy 18 s) trên video nhóm mới. Kết quả chép ở `reports/m2/cong5/w2/kiem-v3/`. Không sửa luật.
- ĐẠT: N1, N2, P0, G3.
- TRƯỢT: G3b (grain). σ shot lớn nhất / nhỏ nhất = 1,713 (ngưỡng ≤ 1,3); tương quan khung kề cao nhất 0,603 ở s34 (ngưỡng ≤ 0,5). s41 0,541 và s42a 0,538 cũng vượt. Đây là lỗi sẵn có của layout, chưa có khâu grain; bản ghép của P (`reports/checks/layout-cong5`) cũng trượt G3b. Việc này thuộc khâu hoàn thiện, không phải lỗi mới của v3.
- Chỉ số trong ±5 % quanh ngưỡng: không có.
- THIẾU (thiếu đầu vào, như bản ghép): P1, G4, J1, J1b, H1, H1b, C3, O3.

**Ảnh trước/sau** (`reports/m2/cong5/w2/`): `v3_C5-N3_s33.jpg`, `v3_N2-N7_s42a-s42b-s42.jpg`, `v3_N6_s30.jpg`, `v3_N8_s43.jpg` (có ảnh phóng vùng ô cửa).

**Rủi ro**
- N8: ô hổ phách chỉ khoảng 6–8 px ở 960 px (12–16 px ở 1080p), cộng quầng nhỏ. Đọc được khi xem kỹ, nhưng ở EWS có thể vẫn nhỏ với khán giả. Nếu cần ô lớn hơn (chọn ô gần hơn hoặc thêm dolly vào ô) thì đó là quyết định khung hình. Đã ghi thành đề xuất Q-W2-5 trong `LAYOUT-W2.md` §6 (PLAN.md do P giữ), W2 không tự đổi.
- N8: các ô gần (< 70 m) nay trắng lạnh, hoà vào mặt tường bị điện rọi loá. Mặt tiền gần gần như không còn thấy ô cửa.
- C5: s33 dùng nguồn điểm ấm 7 cd ở chỗ L11 để thay ánh L11 của bộ phố. Mức này căn bằng mắt theo s35, chưa đo cùng máy với s35.
- N3: s34 (máy riêng) vẫn có bóng Ida sau-phải bà, chạm mép thân. Báo cáo rà đã chấm s34 đạt; W2 không đổi máy s34.
- N6: W1 s23–s24c cần giữ đèn hông sáng; hình W2 đã khớp. s26 vẫn ở mức hắt 0,012 (đèn khuất sau thân), không đổi mặt đã duyệt C2.

**Đang chờ P / chủ dự án:** duyệt các mục v3; quyết định cỡ ô hổ phách s43 (rủi ro N8); ghép tệp timing mới.

# Vòng v4 — chốt layout (Cổng 5 v2, quyết định chủ dự án @e850c0f: B-i, C-i, (c), (d); (e) dời Cổng 7)
Đã merge nhánh tích hợp @e850c0f. Trình tự: sửa mã, `node --check`, kiểm trạng thái ẩn (mặt nạ C3), probe cả 29 shot sau lần sửa mã cuối, rồi render qua hàng đợi.

## a) B-i — trạng thái ẩn
**Nguyên nhân (s35 và cả gói W2).** `util.makeChar.place` gọi `setPose` TRƯỚC khi đặt gốc nhân vật. Rig (`shared/cast.js applyPose`) tính hướng đèn lồng thắt lưng theo ma trận gốc ĐANG CÓ, cụ thể là nghịch đảo hướng xương chậu trong hệ thế giới. Vì vậy ở mọi khung đổi hướng, đèn lấy hướng người của khung TRƯỚC. Ở khung đầu mỗi shot, đèn lấy hướng 0 của nhân vật vừa dựng. Hệ quả: render thẳng một khung khác render nối tiếp. s35 khung 2148 là khung đầu Ida trèo thang (hướng đổi từ lúc đi sang 0).

**Sửa.** Trong `shots_w2.js`, bọc `makeChar`: đặt gốc (vị trí + hướng) TRƯỚC, rồi mới gọi `place` gốc. Không đụng `util.js` và `common.js`. s33 dựng bằng bộ khoá (gọi `setPose` trực tiếp) nên cũng được đổi sang đặt gốc trước. Các chỗ `setPose` trực tiếp khác (s42b, s42, s44–s47) không có đạo cụ phụ thuộc hướng gốc; kiểm ra 0 lệch.

**Cách kiểm.** Chạy `export_c3.js --audit-dir … --scale 1`, làn nhanh, lô 4–5 shot. Mỗi shot lấy khung giữa F (bội 12), xuất thẳng (`--frames F`) và nối tiếp (`--frames F-12,F`), rồi so điểm ảnh 6 mặt nạ và `views.json`. Mặt nạ C3 chỉ có Ida. Với shot không có Ida, dùng kiểm thứ hai: probe (khung đầu/giữa/cuối, nhảy cóc) so với thumbnail bản render nối tiếp. Hai bản trùng từng điểm ảnh ở mọi shot không đổi nội dung.

| Shot | Khung F | Ida trong khung | Lệch trước (px, ×1) | Lệch sau | Nguyên nhân | Sửa |
|---|---|---|---|---|---|---|
| s26 | 1512 | có (46 k px) | **133** | 0 | đèn lồng thắt lưng lấy hướng gốc cũ (khung đầu: hướng 0) | bọc `makeChar` |
| s35 | 2136 | có | **2** | 0 | như trên (đi) | bọc `makeChar` |
| s35 | 2148 (khung P kiểm toán) | có | **1** (×1; P đo ×4: 19 px, 3,21 %) | 0 | như trên (đổi hướng đi → trèo) | bọc `makeChar` |
| s27, s30, s31, s32, s33, s34, s36, s37, s37w, s39, s40, s40w, s41, s42a, s42, s44, s45, s46, s47 | giữa shot | có | 0 | 0 | — | (s33: đặt gốc trước, phòng xa) |
| s25, s28, s29, s38, s42b, s43, s45c, s48 | giữa shot | không (mặt nạ rỗng) | 0 | 0 | kiểm thêm: probe ≡ render (thumb a/b/c trùng điểm ảnh) | — |

Sau sửa, probe cả 29 shot so với render: khác ở s26 (khung a), s35 (khung a) — đúng chỗ sửa. s39, s38, s46, s45c khác vì dời mốc (lửa, hạt theo khung). s43 khác vì máy mới. 22 shot còn lại trùng từng điểm ảnh, nên không render lại.

### a2) So ảnh RGB (bổ sung theo P, nhánh tích hợp @04a738b — W1 cùng lỗi, cùng cách sửa)
Mặt nạ C3 không chứa đèn lồng, nên P yêu cầu so ảnh RGB thô 960×540 (`renderFrame` + `finalize`). Lệch tính là điểm ảnh có kênh bất kỳ lệch > 2/255.
- Công cụ `rgbaudit.js` nằm trong nhật ký phiên (`/var/tmp/cine-out/W2/tools/`), không thuộc repo. Chạy qua hàng đợi (rgb-moi, rgb-cu, rgb-cu2).
- Mã cũ = cây `design/` ở ea7a318 (v3, trước sửa). Mã mới = v4.
- Đã merge @04a738b (chỉ đổi tệp W1); cách sửa của W2 (bọc `makeChar` trong `shots_w2.js`) trùng cách `mkChar` của W1. Không sửa `util.js`.

| Shot | Thẳng F vs nối tiếp F−12→F, TRƯỚC (px; max) | SAU | Khung đầu f0: mã cũ vs mới (px; max) | Render lại? |
|---|---|---|---|---|
| s26 | **301; 99** | 0; 0 | **299; 96** | **có** |
| s35 | **145; 192** | 0; 0 | **198; 181** | **có** |
| s30 (thêm khung 0,83 s: tháo đèn thắt lưng giữa lúc xoay; mã cũ nối tiếp vs mã mới thẳng) | 0 | 0 | 0 | không |
| 22 shot còn lại có đo cả hai bản (s25, s27–s29, s31–s34, s36, s37, s37w, s40, s40w, s41, s42a, s42b, s42, s43, s44, s45, s47, s48) | 0 | 0 | 0 | không (vì lỗi này) |
| s38, s39, s45c, s46 (dời mốc — không so bản cũ) | — | 0 | — | có (vì dời mốc) |

Kết luận: 29/29 shot có ảnh thẳng = nối tiếp (0 điểm ảnh > 2/255). Chỉ s26, s35 có khung đầu đổi so với bản render đầy đủ cũ, và cả hai đã render lại.

## b) C-i — s43 máy đẩy rất chậm
- **Trước (v3):** máy lerp 4 % về điểm nhìn cố định. Ô hổ phách giữ cỡ ≈ 5 × 9 px (960 px), đọc được khi xem kỹ.
- **Sau:** t = 0 đúng khung mở đầu. Trong 4 s: dolly 12 m dọc tia máy → ô (tia đã kiểm không vướng, ô luôn thấy), tiêu cự 28 → 45 mm, hướng nhìn trôi 70 % về ô. Lõi ô cuối shot ≈ 10 × 15 px, gần giữa khung. Không thêm nguồn.
- Bản thử đầu (dolly 46 m, không zoom) hạ máy quá thấp, mất khung mở đầu; đã bỏ.

## c) Câu "Just… keep a little dark for the ones who need it."
- Đo trên stem `reports/m1/cong2/tableread-d2/lines/L4.mp3` bằng faster-whisper small.en (word timestamps). Tính từ đầu L4: Just 9,68 · keep 10,36 · a 11,04 · little 11,22 · dark 11,54 · for 12,08 · the 12,64 · ones 12,76 · who 13,00 · need 13,38 · it 13,66–14,00. Mốc phim với L4 = 93,0 s: lời thật từ 102,33 (P đo; whisper 102,68), "for" 105,08, hết câu 107,00.
- **Trước:** s37w → **s38 (Cas) 101,6–103,0** → s39 (Ida) 103,0–107,4. Câu bắt đầu trên Cas.
- **Sau:** `order_w2.js` đổi thứ tự s37w → **s39 (Ida) 101,6–106,0** → **s38 (Cas) 106,0–107,4** → s40. Câu bắt đầu 0,73 s sau khi vào mặt Ida. Cắt sang Cas ở **106,0 s (1:46,0)**, sau "for" và "the ones", đúng lúc vào "who need it". Tổng thời lượng, mốc thoại, P5 99,2 s, van 107,7 s, L11 tắt 109,2 s không đổi. Không đổi id; s37, s37w, s40 giữ nguyên chỗ.
- Ảnh 4 kiểm mù đề xuất mới: khung toàn cục **2510** (104,58 s, khung 72 của s39, chữ "dark").

## d) Đồng hồ cảnh 6 — chỉ tiến
- **Đọc giờ trên hình (trước):** s45 9:53 (nhỏ, hai kim cùng quanh số 10) → s45c **10:00** → s46 mở ở **9:53** rồi lên 10:00. Người xem thấy 10:00 rồi 9:53 mà không có nhịp "đồng hồ bà chậm" đọc được, nên AI mù thấy thời gian chạy lùi.
- **Cách dựng (sau):** thứ tự **s45 → s46 → s45c**.
  - s45: bà xem đồng hồ mình, rồi ngẩng về phía quảng trường (ngoài hình).
  - s46: insert, 9:53 giữ 0,3 s, vặn lên 10:00.
  - s45c: POV quảng trường 10:00:00, xác nhận giờ bà vừa nhận.
  - Giữ ý đồ 9B (vặn 9:53 → 10:00 = nhận giờ mới).
- Kim giờ ở s46 nay ăn khớp kim phút (1/12). Trước đây kim giờ đi từ 0 s trong khi kim phút còn đứng tới 0,3 s.
- Bảng giờ theo khung ghi ở `continuity/canh-6.md` mục (d): 9:53 → 9:53:44 → 9:55:35 → 9:57:25 → 9:59:16 → 10:00:00 → quảng trường 10:00:00–10:00:01. Đã kiểm bằng mắt trên khung a/b/c: s46 9:53 / ≈ 9:58 / 10:00, s45c 10:00.
- Âm: `audio/mix.py` của P đặt tiếng núm và tiếng "tách" theo `T0['s46']`, tiếng tích tắc theo `T0['s45']…T1['s46']`, nên tự theo thứ tự mới. P cần trộn lại.
- Sheet cũng bỏ chi tiết không có trên hình ("gập nắp"). "Tách" là âm, không phải hình.

## e) Người/bóng hốc vòm
Không sửa ở layout (dời Cổng 7 theo PLAN.md).

## Render (qua hàng đợi, 960×540, 1 mẫu) và tệp
| Nhãn | Shot | Khung | Chờ | Chạy |
|---|---|---|---|---|
| W2/v4 | s26 158 s · s35 149 s · s38 54 s · s39 273 s · s43 144 s · s45c 40 s · s46 110 s | 488 | 217 s (sau việc nặng của W1) | 932 s |
- Tệp: `/var/tmp/cine-out/W2/full/timing_s26-s35-s39-s38-s43-s46-s45c.json` và `video_s26-s35-s39-s38-s43-s46-s45c.mp4` (26,3 MB). Trong mp4 và `summary`, shot xếp theo thứ tự định nghĩa (s26, s35, s38, s39, s43, s45c, s46). `assemble.py` cộng khung theo `summary` nên khớp.
- 22 shot khác không render lại. Ảnh probe mã mới trùng từng điểm ảnh với thumbnail bản render cũ ở khung a/b/c, và kiểm RGB ở trên cho 0.
- Kiểm trạng thái ẩn qua hàng đợi:
  - Mặt nạ C3, làn nhanh: 16 lô trước sửa + 16 lô sau sửa, mỗi lô 24–73 s. Có lô vượt 60 s một chút (được đánh dấu QUA-60S), vì máy dùng chung.
  - RGB, làn nặng: rgb-moi chạy 1313 s; rgb-cu chạy 367 s (lần đầu hỏng vì cây cũ thiếu liên kết `node_modules`); rgb-cu2 chạy 778 s.
- Làm lại: 0 lần render đầy đủ. s43 thử 2 phương án máy trên probe (dolly 46 m bị loại).

**Ảnh trước/sau:** `v4_b_s43.jpg`, `v4_c_s37w-s39-s38.jpg`, `v4_d_dong-ho.jpg`.

**Rủi ro**
- (c) Ở s39, miệng Ida không mấp máy trong lúc câu thoại chạy. Khẩu hình thuộc cửa mặt A-i. Cắt ở 106,0 s nằm đúng ranh "ones / who" (whisper). Nếu P muốn cắt sau hết câu (107,0 s) thì s38 chỉ còn 0,4 s, quá ngắn; khi đó nên chia s39.
- (d) Âm tiếng núm, tiếng "tách" và tích tắc trong `audio/mix.py` tự theo `T0` mới, nhưng P cần trộn lại và nghe kiểm. POV s45c nay đứng sau insert chứ không ngay sau cái ngẩng đầu ở cuối s45. Nhịp nhìn → insert → POV cần kiểm mù lại.
- (b) Cuối s43 máy đã đẩy khá sâu: khung cuối khác rõ khung mở đầu. Tuy vậy t = 0 vẫn đúng khung mở đầu.
- Ảnh 4 kiểm mù đổi sang khung 2510 vì s39 dời lên 1,4 s.

**Đang chờ P / chủ dự án:** ghép bằng tệp timing mới; trộn lại âm cảnh 6; duyệt thứ tự (c), (d); kiểm mù lần sau dùng khung ảnh 4 = 2510.
