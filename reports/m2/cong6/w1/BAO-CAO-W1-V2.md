# BÁO CÁO W1-v2 — Cổng 6, sửa sau kiểm vòng 1 (layout v20), phương án A

Phiên xưởng W1 · nhánh `cong6-w1-v2` (từ `387a7fa` của P) · 30/09/2026 · căn cứ: lệnh W1-v2 của P (chủ dự án duyệt, AUTHORSHIP "Cổng 6 — diễn hoạt") + bổ sung C3 lượt Cas.
Đã sửa: `design/cong5/layout/shots_w1.js`; **mã dùng chung theo lệnh (Đ1, Đ2):** `design/cong3/v2/char3d/cast3d.js` (thêm `ch.gripAt`), `design/cong5/layout/common.js` (`watchInHand` tuỳ chọn `grip`), `design/cong5/layout/shots_w2.js` (CHỈ đổi thân hàm `gripAt` thành lời gọi `ch.gripAt`); `shots/layout/continuity/canh-3.md`, `canh-4.md`; `reports/m2/cong6/w1/sua-v2/`.
Không sửa: `bible/`, `checks/` (không đọc mã), tài sản khoá, `sets*.js`, `order_w1.js`. Không chạy kiểm mù / luật. Thời lượng shot và tổng phim (140,5 s) không đổi.

## 1. Bảng việc a–k
| Mục | Trạng thái | Làm gì · số đo |
|---|---|---|
| **a** s05 bàn tay vỡ hình 0–2,5 s; "cánh tay lạ mép phải" | **Đã sửa (gốc: tư thế + góc máy)** | Gốc: sheet `warm_hands_ladder` xoè ngón 0,9 / gập 0 — với tay MPFB, lòng tay nhìn NGHIÊNG từ máy cũ (lệch ~49°) thành các ngón nhọn tách rời "vuốt/sừng"; vệt đỏ loang là bóng khung lồng đèn trên lòng tay nhìn nghiêng. Không phải IK (s05 không IK tới 2,6 s) hay trọng số da. Sửa: lòng tay khép nhẹ (xoè 0,3, gập 0,3 — `S05.hands`, cũng dùng cho s24) + máy mới (mục h) thấy MU bàn tay phải trước thân cột; tay trái khuất sau cột/lồng → hết "tay lạ" ở mép phải. |
| **b** s06 xuyên mặt đồng hồ; ngón gõ kính (CHẶN L3) | **Đã sửa** | Máy insert KHOÁ ở tư thế 2,3 s khi bà cất đồng hồ (v1 bám đồng hồ → đầu/tai lọt giữa máy và mặt số ở 2,5 s). Gõ kính: đồng hồ đưa vào giữa ngực (vai phải [−40, 0, 10], khuỷu −104 — trước: tay trái hụt 10 cm, đo IK) rồi lòng tay trái IK tới cạnh đồng hồ phía vai trái, ngón duỗi; đỉnh chạm **đúng 16,80 / 17,20 s** (gauss 0,06 s): lòng tay cách mặt kính 1,2 cm, đầu ngón chạm vòng số 12 (probe khung 16,79 và 17,21 s: thấy ngón + móng chạm mặt kính; 17,00 s ngón nhấc khỏi khung. Bảng `s06_sau` lấy mỗi 0,5 s nên không trùng đỉnh gõ). |
| **c** s13 xuyên cột; s15 thang nhảy + xuống từng bậc; s03 tốc độ leo | **Đã sửa** | s13: cúi nhìn đá lát với cổ 18°/quay −14° + thân 10° (v1 cúi thẳng 30° → mũ/mặt lẫn vào thân cột), tay trái giữ nhánh thanh móc cả shot (v1 chuyển về thân cột → cẳng tay quét qua cột). s15: bắt đầu giữa thang (u 0,55), xuống **3 bậc từng nhịp** 0–0,9 s (v1: 1,55 m trong 0,8 s đều); chạm đất lùi một bước 0,9–1,3 s; **nhấc thang 0,95–1,3 s** nội suy vị trí/hướng từ chỗ tựa cột lên vai, tay phải nắm thanh (v1: nhảy 1 khung 1070 → 1071). s03: leo **2 bậc từng nhịp**, 0,37 m / 0,55 s (v1: 0,70 m / 0,55 s). |
| **d** L1: máy s22 cùng phía s21 | **Đã sửa** | s21 máy ở phía −x trước mặt bà; s22 v1 lệch +45° (phía +x). Nay lệch **−62°** (phía −x), lia trái 4° đẩy thân cột ra mép phải. Góc mặt so với trục máy đo mỗi 6 khung: **54,2–59,1°** (> 30°). |
| **e** L2 mẩu tay góc dưới-trái s22 | **Đã sửa** | Ở máy mới tay phải trên van nằm ngoài khung (bảng `s22_sau`, 7 khung: không còn mẩu tay). |
| **f** s24 nhịp đếm ba đọc được (CHẶN L4) | **Đã sửa** | Máy s24 nhìn trước mặt bà → áp tay tới kính là chuyển động DỌC trục máy (v1 ≤ 3 px; thử đẩy tay tới trước: vẫn không thấy). Nay mỗi nhịp hai lòng tay **dang ra hai bên (vai dạng ±24°) rồi khép áp vào hai mặt kính** — chuyển động ngang khung. Đo chiếu tâm lòng tay lên khung 960×540 (mỗi khung): tay trái dịch **30,9 px** ngang / 7,4 px dọc, tay phải **21,2 px** / 7,9 px. |
| **g** s24c dựa tường đọc được, hết "ma-nơ-canh" + C3 Cas | **Đã sửa** | Lưng + vai tựa tường (cách mặt tường 0,16 m, ngả 6°), đầu ngả tựa (cổ −9°, nghiêng 5°), gối phải co, **hai lòng tay áp tường sau hông** (IK, −3 mm tới mặt tường), dồn chân trái, thở, **chớp 57,62 / 58,62 s**, mắt dẫn trước đầu khi quay về Ida; máy lia 9° cho khoảng trống phía cậu nhìn. Cùng tư thế ở s23, s24. **C3 Cas s24c** (tư thế MỚI, `export_c3 --who cas`, khung 1380/1392/1404): cánh tay trên `foreshorten` 0,573–0,579, hidden 0 — co ngắn THẬT (tay vòng ra sau lưng); chồng mặt nạ: không lún vào thân áo/tường, chỉ vai áo phồng (sai lệch đã chấp nhận) → ghi số, không chỉnh. |
| **h** Mặt Ida cỡ cận s05, s22 bằng dàn dựng như PA1; 1 khung s22 1080 | **Đã làm** | s05: máy nghiêng **80°** khỏi hướng mặt, 85 mm, 2,1 m, lia/ngóc nhẹ: ngọn L4 + lồng kính TRONG khung là đèn chính trước mũi, nửa mặt phía máy chìm, mắt nhìn xuống ngọn lửa, mí che bớt (lidDrop 0,22), glint 0,45 → 0,2; khẩu hình L1 biên độ 0,62, "old" bớt chu môi (kiểm mù: "méo 1,0–1,5 s"). s22: giữ **MCU 85 mm** (không cần nới MS), 3/4 ≈ 55–59°, lidDrop 0,3, glint 0,35 → 0,2, khẩu hình L2 0,6 → **0,85** (kiểm mù: "miệng hầu như không đổi hình"), môi–má–cằm (richLip). **Không có key đèn khí ở s22** trước khung cuối (L10 bắt lửa 52,45 s; ánh điện phẳng — luật thế giới) → không tạo nguồn giả. Khung 1920×1080: `sua-v2/s22_1920x1080_49.79s.jpg` (mí dưới có viền hồng mảnh — chủ dự án chấm viền nước). |
| **i** Đ1 gripAt vào cast3d; Đ2 watchInHand theo gripPoint; Đ3 sào mồi | **Đ1, Đ2 đã làm; Đ3 đề xuất §4** | Đ1: `ch.gripAt(s, g)` trong `cast3d.js` = đúng thuật toán `gripAt` của W2 (+ `g.zFix` chỉ khi có); `shots_w2.js`, `shots_w1.js` thay thân hàm bằng `return ch.gripAt(s, g)` (không đổi tham số). Đ2: `watchInHand(scene, { grip: true, lift })` đặt theo `ch.gripPoint('R')`; **mặc định giữ cách cũ** để s45/s46/s45c (W2 đã duyệt) không đổi — W2 bật `grip` cần duyệt riêng. W1 s09w dùng bản chung (bỏ `watchInPalm`), 0 px. |
| **j** Không sửa s30, s14, nối s24c → s25; L5 → Cổng 7 | **Giữ** | — |
| **k** continuity canh-3, canh-4 số cũ | **Đã sửa** | canh-4: mục "Cập nhật hiện trạng" (cột điện tường chim không trong khung cảnh 3–4, nguồn vỉa hè nam (17,4; 6,2; 4,1); Cas s23–s24c dựa tường 0,16 m; đổi chỗ 0,75 m qua cắt đã duyệt); canh-3: chỗ Cas, tư thế, máy s24c, bảng trạng thái cuối. |

**C3 lượt Ida (luật v20):** kiểm `views` + chồng mặt nạ (`sua-v2/c3_kiem_s19-1128_s23-1308_s24c-1392.jpg`):
- s19 khung 1128, cánh tay trên trái −37,7 %: `foreshorten` 0,9965, hidden 0; tư thế `warmLadder` như Cổng 5 (s19 không IK sau 1,0 s). Mặt nạ không lún/xuyên — phần vai bị cổ áo/khăn che làm đoạn tay thấy ngắn. **Ghi số, không chỉnh.**
- s23 khung 1308, cẳng tay +45,8 %: `foreshorten` 1,003; Ida cách máy ≈ 12 m, mặt nạ cẳng tay **29 px** (cánh tay 27 px) — sai số đo ở cỡ quá nhỏ; không thấy kéo/xuyên. **Ghi số, không chỉnh.**

## 2. Lệch 0 px toàn phim (Đ1/Đ2 đụng mã dùng chung)
Gốc tạo TRƯỚC mọi sửa (`/var/tmp/cine-out/W1/lech0v2/goc`, 53 shot, 159 ảnh, từ `387a7fa`); so sau khi sửa (`…/lech0v2/sau`, mã `56b834a`): **159 ảnh; lệch 25 — đúng 25 ảnh của 9 shot W1 cố ý đổi** (s03, s05, s06, s13, s15, s22, s23, s24, s24c). **30 shot W2: 0 px.** s09w (Đ2) và 10 shot W1 có IK không đổi (s02, s04, s07, s08, s11, s12, s14, s19, s21 + s01, s09, s10e, s10): **0 px** → `ch.gripAt` trùng từng bit với bản sao cũ. Lượt sửa sau so (s24c lia 9°) chỉ đổi s24c.

## 3. Render, mp4 hiện hành
| Nhãn | Shot | Khung | Chạy (s) |
|---|---|---|---|
| v2-render | s03, s05, s06, s13, s15, s22, s23, s24, s24c | 528 | 2 596,7 |
| v2-s24c (lia 9°) | s24c | 36 | 353,2 |
| v2-s22-1080 | 1 khung s22 1920×1080 | 1 | 17,1 |
**MP4 hiện hành theo shot** (`/var/tmp/cine-out/W1/`, 960×540, có `timing_*.json`):
| Shot | MP4 |
|---|---|
| s03, s05, s06, s13, s15, s22, s23, s24 | `video_s03-s05-s06-s13-s15-s22-s23-s24-s24c.mp4` (s24c trong tệp này là bản cũ) |
| s24c | `video_s24c.mp4` |
| s02, s04, s07, s08 | `video_s02-s03-s04-s05-s06-s07-s08.mp4` (v1; s03, s05, s06 trong tệp là bản cũ) |
| s09w, s11, s12 | `video_s09w-s11-s12-s13-s14.mp4` (v1; s13, s14 trong tệp là bản cũ) |
| s14 | `video_s14.mp4` (v1) |
| s19, s21 | `video_s15-s19-s21-s22-s23-s24-s24c.mp4` (v1; các shot khác trong tệp là bản cũ) |
| s01, s09, s10e, s10 | bản Cổng 5 (P giữ) |
| W2 | không shot nào đổi (0 px) → giữ mp4 W2 hiện hành |
Bảng khung 0,5 s trước/sau: `reports/m2/cong6/w1/sua-v2/<shot>_truoc.jpg`, `_sau.jpg` cho 9 shot (trước = mp4 v1).

## 4. Đề xuất Đ3 (sheet đạo cụ trong `bible/` — P trình chủ dự án, W1 không sửa)
> **Sào mồi — chỗ để khi đi/chạy:** sào (6 H) móc dọc thanh thang trái bằng hai khuyên da ở 1/3 và 2/3 chiều dài thang, đầu có bấc hướng lên trên (cao hơn đầu thang 0,4 m, không chạm vai). Khi trèo, sào ở lại trên thang; bà gỡ sào bằng tay phải ở bậc trên cùng trước khi mồi (s21). Đèn lồng thắt lưng giữ ở hông trái như sheet.
Ưu: giải chỗ hở continuity cảnh 1–3 (sào chỉ thấy ở s21). Nhược: thêm một vật trên thang ở mọi shot đi (s02, s07, s08, s15, s23) → render lại 5 shot, hình thang trên vai rậm hơn ở tele s08. Rủi ro: sheet đạo cụ khoá — cần chủ dự án duyệt trước khi W1 dựng.

## 5. Rủi ro còn lại
- s22 không có key đèn khí (L10 chưa cháy tới khung cuối) — mặt vẫn dưới ánh điện phẳng; nếu kiểm mù vẫn chê "búp bê sáp" ở s22 thì cần quyết của chủ dự án (đổi cỡ MS hoặc để Cổng 7 xử lý chất liệu da).
- s24c: hai tay vòng ra sau lưng — ít thấy tay; vai áo phồng khi tay vòng sau (sai lệch đã chấp nhận của Cas) rõ hơn một chút.
- s06: khung cuối (2,5–3,0 s) máy khoá → đồng hồ rời khung, còn tay áo + kính lồng đèn (tối).
- s05 góc gần nghiêng hẳn: khẩu hình L1 đọc qua môi–cằm ở nghiêng, ít thấy miệng hơn v1.

## 6. Token, thời gian
- Thời gian thật: 13:42 → ≈ 15:45 UTC 30/09/2026 (≈ 2,1 giờ; render + dò lệch ≈ 1,6 giờ).
- Token lượt W1-v2: bộ đếm công cụ ≈ 135 nghìn (hạn 400 nghìn).
