# BÁO CÁO W1 — Cổng 6, DIỄN HOẠT cảnh 1–3 (s01 → s24c, 0,0–59,0 s), VÒNG 1

Phiên xưởng W1 · nhánh `cong6-w1-v1` (worktree từ main `00a4ead`) · 30/09/2026 · căn cứ: lệnh giao của P; AUTHORSHIP "Cổng 6 — diễn hoạt" (MỞ W1, B2 s23, 30/09/2026).
Đã sửa: `design/cong5/layout/shots_w1.js`; `shots/layout/shots_w1.json` (trường mới `cong6_w1`), `LAYOUT-W1.md` (mục 15, dòng s22 mục 2), `continuity/canh-1.md`, `canh-2.md`, `canh-3.md`; thư mục này.
**Không** sửa: `bible/`, `checks/` (không đọc mã checks), tài sản khoá, `order_w1.js` (không cần), `sets.js` (không cần), `sets_end.js`, `shots_w2.js`, mã dùng chung. Không chạy kiểm mù, không chạy `checks/run.py`, không render toàn phim.

## 0. Tóm tắt
- **s22 (quyết định cố định):** máy lệch **45°** khỏi hướng mặt (đo 42,2–46,5° suốt shot; Cổng 5: 7,0–11,3°), **giữ MCU 85 mm**, 1,2 m, tĩnh. Mắt v1.5.1: mí che bớt tròng (lidDrop 0,2), glint 0,5 → 0,35, không còn nhìn thẳng máy. Khẩu hình L2 lẩm bẩm.
- **Khẩu hình + biểu cảm L1 (s05), L2 (s22):** 16 kênh + 6 viseme, mốc đo trên tệp take; miệng nói có môi–má–cằm cùng động (richLip của W2 v3).
- **Cầm nắm theo tay MPFB (IK điểm):** thang trên vai (s02, s07, s08, s15, s23), thanh thang khi trèo/tụt (s03, s15, s21, s23), van (s03, s04, s19, s22, s23), thanh móc thang + thân cột khi nghỉ (s03, s05, s11–s15, s21), đồng hồ (s06, s09w), cửa đèn lồng (s04). Trước: lòng tay cách vật 7,8–55 cm (tư thế FK); sau: −2,3 mm … +2,5 cm (bảng §3).
- **s24c Cas dựa tường:** lòng tay phải MPFB áp phẳng lên mặt vôi (IK điểm, +2,6 mm); cậu dựa lưng vào tường chim. Trước: lòng tay cách mặt tường 0,82 m (phải) / 1,09 m (trái).
- **B2 s23:** cột điện tường chim (17,0; −5,9) **không còn trong khung**; PointLight của cột dời sang vỉa hè nam ngoài khung; cột P5 (10,8; +3,9) mé nam giữ nguyên.
- **Đứng tự nhiên:** Ida s06, s09w, s15 (settle); thở trên thang mọi shot thang; Cas s23, s24, s24c (dồn chân, thở, dựa tường).
- **Nhịp Cổng 6 ghi trong manifest đã làm:** mồi đèn lồng ở s04 (tay trái xuống cửa đèn), dựng thang ở s23 (thang rời vai, xoay vào cột, không còn đổi tức thì).
- Tổng phim **140,5 s** không đổi; W1 23 shot, 59,0 s, 1 416 khung. Lệch 0 px ngoài phạm vi: **102 ảnh, lệch 0** (30 shot W2 + s01, s09, s10e, s10).

## 1. Bảng việc
| Việc (lệnh P) | Trạng thái | Ghi chú |
|---|---|---|
| B1-1 Tư thế đứng tự nhiên mọi shot Ida đứng | **Đã làm** | Ida đứng trên đất chỉ ở s06, s09w, s15 (0,8–1,5 s): `settle` (dồn chân, lệch hông 3°, thở). Shot trên thang: `breathe` (không đụng chân — chân khoá bậc). Shot đi (s02, s07, s08, s23 chạy) giữ chu kỳ đi — ngoài phạm vi "đứng". |
| B1-2 s24c Cas dựa tường, tay đặt đúng lên tường (IK điểm), số đo trước/sau | **Đã làm** | §4. Cas dời sát tường ở s23, s24, s24c (đồng nhất cảnh 3). |
| B1-3 s22 3/4 > 30°, giữ MCU; kiểm mắt v1.5.1 | **Đã làm** | §2. |
| B1-4 Mục 11 phần Ida: sai lệch đã chấp nhận trên clip; cầm nắm thang/van/sào/đồng hồ theo tay MPFB | **Đã làm phần cầm nắm; kiểm clip: §6** | Sào (s21): tâm lòng tay cách trục sào 2,2 cm — đạt, không sửa. |
| B1-5 Khẩu hình + biểu cảm L1 (s05), L2 (s22) | **Đã làm** | §2, §5. |
| B1-6 Tồn đọng Cổng 5 thuộc shot W1 | **Đã làm 2, còn 1 đề xuất** | Làm: nhịp mồi đèn lồng s04, dựng thang s23. Còn: sào mồi không có chỗ để khi đi (cần sheet đạo cụ — P). G1, G7, G8, G16: Cổng 7, không làm. |
| B2 s23 bỏ cột điện tường chim khỏi khung | **Đã làm** | §4. Làm trong `shots_w1.js`, không sửa `sets_end.js`. |
| Không làm việc Cổng 7 (mức sáng, grade, bóng tiếp đất, đèn lồng rọi) | **Giữ** | Không thêm/bớt nguồn sáng; chỉ dời vị trí PointLight cột (đang tắt) ở s23 theo lệnh. |

## 2. s22 — 3/4, MCU, mắt, L2
- **Máy:** `faceCam` lệch **+45°** (phía phố, +x) thay −12°; vẫn 85 mm, 1,2 m, đặt MỘT lần từ tư thế t = 0 (hàm thuần). Thử −40° (phía nhà): thân cột đèn che nửa mặt — loại. Thử lia trái 3,5° để đưa tay nắm van vào khung: góc trái thành khối ống + van đồng — loại (tham số `S22.pan = 0`).
- **Góc mặt so với trục máy** (hướng đầu nằm ngang so với hướng đầu → máy, đo mỗi 6 khung bằng `--dbg '{"log":1}'`): **42,2–46,5°** (Cổng 5: 7,0–11,3°). Đầu ngẩng ở 1,6–2,4 s vẫn > 30°.
- **Mắt v1.5.1 trên khung** (probe 960×540, khung 49,75 · 51,17 · 52,46 s): mí trên che mép trên tròng (lidDrop 0,2), lòng trắng không lộ vòng quanh tròng, ánh mắt không nhìn thẳng máy; glint 0,35. Viền nước: ở 960 px không phân biệt được — cần P xem bản 1080 (đề xuất §8). Đánh giá của tôi: không còn kiểu "búp bê nhìn thẳng" của khung chính diện cũ; vẫn là hình tự chấm, chưa kiểm mù.
- **Diễn:** nét 'strained' (press, browKnit, browDown, chinRaise) + mí sụp; L2 lẩm bẩm biên độ 0,6, miệng có môi–má–cằm (richLip); chớp 50,45 · 50,92 (chậm) · 52,12 s; ngước nhìn lồng 1,5–2,4 s (nhãn cầu −0,24 rad + cổ); lửa bắt ở 52,45 s → mày giãn, môi thả. Thở gấp (chu kỳ 2,6 s). Tay phải nắm ống khí ngay dưới van (IK, −2,3 mm); trên hình chỉ một mẩu đồng ở góc dưới trái.
- Bảng khung: `bang-khung_s22.jpg`.

## 3. Cầm nắm — tâm lòng tay MPFB (`ch.gripPoint`) → mặt vật (m)
Đo bằng `--dbg '{"meas":1}'` (bọc `S1` trong `shots_w1.js`, không đổi hình), mỗi 3 khung. "Trước" = tư thế FK của shot (= tư thế Cổng 5 + thở) — khoảng cách tới CÙNG đích; "Sau" = sau IK. Chỉ tính khung tay đã nắm hẳn (trọng số IK ≥ 0,99); khung đang chuyển (trộn) không tính. Âm −0,0023 = lòng tay úp sát mặt vật (như W2). Khi một tay nắm chồng hai đích trong cùng khung (s11, s13: thân cột rồi nhánh thanh móc), cột "Trước" là khoảng cách FK tới đích ĐẦU.

| Shot | Tay | Vật | Giây shot (nắm hẳn) | Trước — tư thế FK (m), trung vị [min–max] | Sau IK (m) [min…max] | Khung mẫu |
|---|---|---|---|---|---|---|
| s02 | Ida P | thang trên vai | 0,00–4,46 | 0,161 [0,161–0,161] | -0,0023…-0,0023 | 37 |
| s03 | Ida T | thanh thang | 0,00–0,00 | 0,316 [0,316–0,316] | +0,0192…+0,0192 | 1 |
| s03 | Ida P | thanh thang | 0,00–0,00 | 0,444 [0,444–0,444] | +0,0192…+0,0192 | 1 |
| s03 | Ida T | thân cột | 0,50–1,25 | 0,214 [0,210–0,216] | -0,0023…-0,0023 | 7 |
| s03 | Ida P | thanh móc | 0,50–0,50 | 0,155 [0,155–0,155] | +0,0210…+0,0210 | 1 |
| s03 | Ida P | van | 0,75–1,25 | 0,280 [0,279–0,283] | -0,0023…-0,0023 | 5 |
| s05 | Ida T | thân cột | 3,12–3,96 | 0,212 [0,208–0,214] | -0,0023…-0,0023 | 8 |
| s05 | Ida P | thanh móc | 3,12–3,96 | 0,154 [0,151–0,156] | +0,0147…+0,0198 | 8 |
| s06 | Ida P | đồng hồ | 0,00–2,25 | 0,078 [0,078–0,078] | -0,0023…-0,0023 | 19 |
| s07 | Ida P | thang trên vai | 0,00–3,96 | 0,161 [0,161–0,161] | -0,0023…-0,0023 | 33 |
| s08 | Ida P | thang trên vai | 0,00–1,96 | 0,161 [0,161–0,161] | -0,0023…-0,0023 | 17 |
| s14 | Ida T | thân cột | 0,00–0,38 | 0,205 [0,203–0,207] | -0,0023…-0,0023 | 4 |
| s14 | Ida P | thanh móc | 0,00–1,96 | 0,148 [0,146–0,154] | +0,0166…+0,0252 | 17 |
| s15 | Ida T | thân cột | 0,00–0,00 | 0,208 [0,208–0,208] | -0,0023…-0,0023 | 1 |
| s15 | Ida P | thanh móc | 0,00–0,00 | 0,152 [0,152–0,152] | +0,0192…+0,0192 | 1 |
| s15 | Ida T | thanh thang | 0,38–0,75 | 0,300 [0,223–0,344] | -0,0023…+0,0063 | 4 |
| s15 | Ida P | thanh thang | 0,38–0,75 | 0,360 [0,220–0,472] | -0,0023…-0,0001 | 4 |
| s15 | Ida P | thang trên vai | 1,25–1,46 | 0,162 [0,140–0,162] | -0,0023…-0,0023 | 3 |
| s19 | Ida T | thân cột | 0,00–0,50 | 0,212 [0,208–0,215] | -0,0023…-0,0023 | 5 |
| s19 | Ida P | van | 0,00–0,50 | 0,356 [0,355–0,357] | -0,0023…-0,0023 | 5 |
| s21 | Ida T | thân cột | 0,50–1,96 | 0,208 [0,208–0,220] | -0,0023…-0,0023 | 7 |
| s22 | Ida P | van | 0,00–2,96 | 0,357 [0,354–0,371] | -0,0023…-0,0023 | 25 |
| s04 | Ida T | thân cột | 0,00–0,00 | 0,208 [0,208–0,208] | -0,0023…-0,0023 | 1 |
| s04 | Ida P | van | 0,00–0,00 | 0,355 [0,355–0,355] | -0,0023…-0,0023 | 1 |
| s04 | Ida P | thanh móc | 1,00–1,25 | 0,206 [0,206–0,207] | +0,0052…+0,0073 | 2 |
| s04 | Ida T | cửa đèn lồng | 1,25–1,25 | 0,837 [0,837–0,837] | -0,0023…-0,0023 | 1 |
| s12 | Ida T | thanh móc | 0,00–2,46 | 0,389 [0,384–0,397] | -0,0023…-0,0023 | 11 |
| s12 | Ida P | thanh móc | 0,00–2,46 | 0,223 [0,218–0,226] | -0,0023…-0,0023 | 11 |
| s11 | Ida T | thân cột | 0,00–0,25 | 0,201 [0,201–0,201] | -0,0023…-0,0023 | 3 |
| s11 | Ida P | thanh móc | 0,00–1,96 | 0,211 [0,127–0,221] | -0,0023…+0,0252 | 17 |
| s11 | Ida T | thanh móc | 1,12–1,96 | 0,450 [0,446–0,451] | -0,0023…-0,0023 | 8 |
| s13 | Ida T | thanh móc | 0,00–0,50 | 0,447 [0,444–0,449] | -0,0023…-0,0023 | 5 |
| s13 | Ida P | thanh móc | 0,00–1,96 | 0,156 [0,133–0,222] | -0,0023…+0,0198 | 17 |
| s13 | Ida T | thân cột | 1,38–1,96 | 0,211 [0,208–0,215] | -0,0023…-0,0023 | 6 |
| s23 | Cas P | tường | 0,00–2,96 | 0,200 [0,197–0,202] | +0,0026…+0,0026 | 25 |
| s23 | Ida P | thang trên vai | 0,00–0,75 | 0,161 [0,161–0,161] | -0,0023…-0,0023 | 7 |
| s23 | Ida T | thanh thang | 1,12–1,50 | 0,304 [0,240–0,352] | -0,0023…-0,0023 | 4 |
| s23 | Ida P | thanh thang | 1,12–1,50 | 0,428 [0,321–0,552] | -0,0023…+0,0077 | 4 |
| s23 | Ida T | thân cột | 1,88–2,00 | 0,207 [0,203–0,210] | -0,0023…-0,0023 | 2 |
| s23 | Ida P | van | 1,88–2,00 | 0,353 [0,352–0,354] | -0,0023…-0,0023 | 2 |
| s24c | Cas P | tường | 0,00–1,46 | 0,202 [0,198–0,202] | +0,0026…+0,0026 | 13 |
| s24 | Cas P | tường | 0,00–1,96 | 0,199 [0,197–0,202] | +0,0026…+0,0026 | 17 |

- Khung đang chuyển (trộn IK, trọng số < 1 — không tính vào bảng), theo (shot, tay): {('s03', 'Ida T'): 7, ('s03', 'Ida P'): 8, ('s05', 'Ida T'): 4, ('s05', 'Ida P'): 4, ('s06', 'Ida P'): 3, ('s14', 'Ida T'): 2, ('s15', 'Ida T'): 2, ('s15', 'Ida P'): 3, ('s19', 'Ida T'): 3, ('s19', 'Ida P'): 3, ('s21', 'Ida T'): 6, ('s04', 'Ida T'): 3, ('s04', 'Ida P'): 3, ('s11', 'Ida T'): 6, ('s13', 'Ida T'): 6, ('s23', 'Ida P'): 7, ('s23', 'Ida T'): 5}

- Tâm lòng tay còn +1,5…+2,5 cm tới thanh móc thang ở s05, s11, s13, s14 (tay phải): IK hết tầm với (thanh ở 0,58 m trước ngực, cánh tay gần duỗi thẳng). Ngón vẫn ôm thanh (bộ tay MPFB gập ngón tới khi chạm) — trên MS 50 mm đọc là đang nắm. Muốn 0 thì phải dời bà sát cột 0,1 m như W2 (`ON_Z1`) — đổi bố cục đã duyệt, không làm.
- Đo cũ (Cổng 5, trước khi sửa, gần nhất trong mọi vật): s06 đồng hồ 9,2 cm; s09w đồng hồ 7,9 cm → sau **3,0 cm** (đồng hồ đặt trên lòng tay, dày ngón + vỏ); s21 sào 2,2 cm (không sửa).
- **s06:** thử đặt đồng hồ vào lòng tay MPFB (như s09w): tay trái (đang gõ) nằm chắn giữa máy insert và mặt số → giữ đồng hồ + máy đúng Cổng 5, IK lòng tay phải lên đáy đồng hồ.
- **s04:** tay phải nắm thanh móc sát thân cột (x − 0,1) khi bà cúi xuống đèn lồng (nhánh x − 0,2: hụt 7 cm).
- **s11–s13:** khi thân quay về quảng trường (turnSquare), thân cột ngoài tầm tay trái 3–4 cm → tay trái chuyển sang **nhánh trái thanh móc** (s11 0,35–1,15 s; s12 cả shot), về lại thân cột khi cúi (s13 0,5–1,3 s).

## 4. s24c Cas dựa tường · B2 s23
**Cas (s23, s24, s24c):**
| | Cổng 5 | Cổng 6 W1 v1 |
|---|---|---|
| Chỗ đứng (bộ phố) | casSpot (14,3; −7,15), cách mặt tường 0,95 m | **(14,3; −7,90)**, cách mặt tường **0,20 m** (lưng tựa tường) |
| Hướng | mặt về L11 | thân −25° (ra phố, lệch về L11), cổ quay nốt về L11/Ida |
| Tay | trong tay áo, lòng tay cách mặt tường **0,82 m (phải) / 1,09 m (trái)** | **lòng tay phải áp phẳng lên mặt vôi** cạnh hông, cao 0,62 m, lệch 0,13 m sang phải thân, ngón chúc xuống — IK điểm: tâm lòng tay cách điểm đích **+2,6 mm**, cách mặt phẳng tường **−3 mm** (úp sát; FK trước IK ở chỗ mới: 0,20 m); tay trái buông |
| Cách L11 | ≈ 7,1 m | ≈ 7,5 m |
- Thử (probe, loại): tay áp tường ngang vai với tường ở bên phải cậu → từ máy s24c đọc thành "vẫy tay chào"; ngón hướng lên cạnh hông → "xoè tay"; áp cách hông 0,2 m, ngón xoè → "chìa tay ra" (đã render một lượt, thay ở lượt `c6v1-cas`). Chốt: lưng tựa tường, lòng tay áp tường ngón chúc xuống; bóng cậu sát người trên tường (đọc được "sát tường").
- `gripAt` bản W1 thêm `zFix` (chiều trục cố định) để quyết ngón chúc xuống khi áp phẳng — chỉ trong `shots_w1.js`.

**B2 s23 (chỉ đạo chủ dự án, luật v0.6):**
| Mục | Trước | Sau |
|---|---|---|
| Cột điện tường chim (sets_end `wallPost`) | thế giới (17,0; −5,9), mé BẮC (cùng mé L11 (8; −3,9)), thấy ở phải khung, u ≈ 0,89 | **ẩn trong shot**: nhóm cột + 12 vật trong 1,6 m quanh đầu đèn (bóng đèn, quầng, loá) = 13 vật |
| PointLight của cột | tại đầu đèn trên cột (17,0; −5,9), tầm 8,5 m | **(17,4; 6,2; 4,1)** thế giới = (7,2; 6,2; 12,2) hệ tường chim — vỉa hè nam, cùng chỗ W2 s27; ngoài khung (trên mép trên ≈ 3° so với nửa FOV dọc 23,2°); bỏ giới hạn tầm như W2. Ở s23 (52,5–55,5 s) cột **TẮT** (bật 64,4 s) → không có ánh; cường độ/ mức sáng: Cổng 7 |
| Cột phố chính P5 | (10,8; +3,9), mé NAM, thấy ở trái khung | **giữ nguyên** — đúng luật v0.6 (đối diện dãy đèn khí) |
- Không sửa `sets_end.js`. Ảnh trước/sau: `s23_B2_truoc-sau.jpg`.

## 5. Khẩu hình, mốc thoại
Mốc đo trên chính tệp take (`reports/m1/cong2/tableread-d2/lines/L1.mp3`, `L2.mp3`): bao năng lượng 50 ms (> −38 dB so với đỉnh) + onset librosa + faster-whisper small.en; mix đặt câu ở đầu shot (lệch 0,000 s như W2 đo) → giây phim = mốc thoại + giây trong tệp.
- **L1** "Evening, old street." (tệp 2,16 s): Evening 0,15–0,95 · old 1,00–1,30 · street 1,35–2,05 → phim 12,15–14,05. Viseme: E-FV-E-L-E-L · O-O-L · E-L-O-E-E-L; miệng đi trước tiếng 0,04 s; biên độ 0,75.
- **L2** "Not yet... not yet." (tệp 2,88 s): Not 0,15–0,35 · yet 0,50–0,72 · (hơi thở 0,85–0,95) · not 1,55–1,80 · yet 1,95–2,50 → phim 49,65–52,00. Biên độ 0,6 (lẩm bẩm).
- Whisper đặt "old" ở 1,22 s và "not" (lần 2) ở 1,38 s; bao năng lượng + onset cho 1,00 và 1,55 — tôi dùng bao năng lượng (whisper lệch ≤ 0,2 s ở từ ngắn).

## 6. Kiểm clip (mục 11 phần Ida, tự xem bảng khung — chưa kiểm mù)
Tự xem bảng khung 0,5 s + thumbs a/b/c của mọi shot đã đổi (960×540). Không phải kiểm mù.
- **s02, s07, s08:** tay phải nằm trên thanh thang suốt shot (trước: hở 16 cm — thấy ở khối bóng người). Chu kỳ đi giữ nguyên (H1b ngoài phạm vi).
- **s03, s04, s19, s23:** tay trên van → lên kính; khi nghỉ tay nằm trên cột/thanh móc. s04 nhịp mồi đèn lồng nhỏ ở 28 mm (R6).
- **s05:** miệng động theo L1 có môi và má; nét cười nhẹ. **Ghi nhận (không phải lỗi mới):** vệt tối trên hai lòng tay khi áp gần kính (có từ Cổng 5, bóng khung lồng/ngọn lửa lên tay) — ánh sáng, để Cổng 7.
- **s06:** đồng hồ nằm trong lòng tay (hết "lơ lửng trên ngón"). Nhịp gõ kính của tay trái không thấy trong khung insert — như Cổng 5 (R5).
- **s09w:** đồng hồ trong lòng tay, ngón phía sau đồng hồ, đọc 7:53.
- **s11–s13:** hai tay trên thanh móc/thân cột, không còn tay lơ lửng. **s14:** tay trái giơ ngang ra trên vỉa hè — đọc được từ máy cao (Cổng 5: như tay buông).
- **s15:** tụt thang hai tay trên thanh, thang lên vai 1,1 s (đổi thang vẫn tức thì ở đây — chỉ tay được sửa).
- **s21:** tay trái trên thanh/thân cột; sào tay phải như cũ.
- **s22:** xem §2 và `s22_truoc-sau.jpg`.
- **s23:** cột điện tường chim không còn; Ida nhỏ (≈ 12 m) nên nhịp dựng thang (0,85–1,1 s) khó thấy ở 960 px. Cas nhỏ ở chân tường phải khung.
- **s24c:** bóng Cas nằm sát người trên tường (đọc "đứng sát tường"); tay phải cạnh hông áp tường — từ máy 3/4 trước đọc là tay buông sát hông, **không rõ là đang chạm tường** (R7).
- **Chân/tay ở khung tĩnh (mục 11):** không thấy xuyên vật lớn; chân trên bậc thang giữ như Cổng 5 (không đo). Mép cổ tay áo Ida (răng cưa, s41) không thuộc W1.

## 7. Thời lượng, render, lệch 0 px
**Thời lượng:** không đổi id/thứ tự/thời lượng. W1 = 23 shot, 1 416 khung, 59,0 s; tổng phim 140,5 s (`render_film.js --events`: FILM_S = 140,5). Shot đã render lại (19): s02 108 · s03 48 · s04 36 · s05 96 · s06 72 · s07 96 · s08 48 · s09w 48 · s11 48 · s12 60 · s13 48 · s14 48 · s15 36 · s19 60 · s21 48 · s22 72 · s23 72 · s24 48 · s24c 36 = 1 176 khung. Không đổi: s01, s09, s10e, s10 (không nhân vật).

**Render (hàng đợi nặng, 960×540, 24 fps; nguồn `/var/tmp/cine-queue/log.tsv`):**
| Nhãn | Shot | Khung | Chờ (s) | Chạy (s) | s/khung render |
|---|---|---|---|---|---|
| c6v1-canh1 | s02–s08 | 504 | 1 362,8 | 1 690,9 | 1,53–4,68 (TB ≈ 3,3) |
| c6v1-canh2 | s09w, s11–s14 | 252 | 514,1 | 794,5 | 2,08–4,01 |
| c6v1-canh3 | s15, s19, s21–s24c | 372 | 1 187,7 | 1 834,5 | 2,19–7,97 |
| c6v1-s14 (làm lại: tay giơ mới) | s14 | 48 | 4 149,1 | 99,4 | 1,89 |
| c6v1-cas (làm lại: tay Cas trên tường) | s23, s24, s24c | 156 | 0,0 | 1 398,0 | 8,19–9,39 |
| **Tổng** | | 1 332 | 7 213,7 | 5 817,3 | |
- Lượt `c6v1-canh3` đầu tiên bị hệ thống dừng khi đang CHỜ khoá (lệnh chờ nền hết hạn 2 giờ lúc W2 giữ làn nặng) — không có dòng log, không khung nào render; xếp hàng lại 11:0x.
- Chậm hơn Cổng 5 C2 (1,33 s/khung) vì IK tay MPFB (mỗi lần nắm 4 vòng lặp cập nhật tay) và mặt nhân vật: s23 7,97–9,39 s/khung (Ida + Cas đều IK).

**MP4 hiện hành theo shot** (`/var/tmp/cine-out/W1/`, không tiếng, mỗi tệp có `timing_*.json` cùng tên; `shots/<id>.timing.json`, `thumbs/<id>_{a,b,c}.jpg` là bản cuối):
| Shot | MP4 hiện hành |
|---|---|
| s02, s03, s04, s05, s06, s07, s08 | `video_s02-s03-s04-s05-s06-s07-s08.mp4` |
| s09w, s11, s12, s13 | `video_s09w-s11-s12-s13-s14.mp4` (**s14 trong tệp này là bản cũ**) |
| s14 | `video_s14.mp4` |
| s15, s19, s21, s22 | `video_s15-s19-s21-s22-s23-s24-s24c.mp4` (**s23, s24, s24c trong tệp này là bản cũ**) |
| s23, s24, s24c | `video_s23-s24-s24c.mp4` |
| s01, s09, s10e, s10 | không đổi — dùng bản Cổng 5 (P đang giữ) |

**Lệch 0 px (shot không đổi):** gốc tạo TRƯỚC khi sửa: `bash scripts/p/do_lech_0px.sh /var/tmp/cine-out/W1/lech0/goc <53 shot>` (159 ảnh, 08:22–08:48). So sau khi sửa (mã cuối trừ lượt đổi tay Cas — chỉ s23/s24/s24c, không thuộc nhóm so): `…/lech0/sau2` với 34 shot s01, s09, s10e, s10 + 30 shot W2 (s25…s48) → **102 ảnh; lệch 0**. Lần so đầu (`…/lech0/sau`, mã commit ef3d69e) cũng 102 ảnh; lệch 0. `sets.js` không đổi.

**Chỉ số ±5 % quanh ngưỡng:** không chạy luật (P chạy). Số tự đo gần ngưỡng: góc mặt s22 42,2–46,5° (ngưỡng > 30°, ngoài dải ±5 %). Tổng phim 140,5 s đúng mốc.

## 8. Đề xuất (P chuyển chủ dự án / P xử lý mã dùng chung) — W1 không tự làm
- **Đ1 (mã dùng chung, như W2 Đ1):** đưa `gripAt` (IK tới một điểm, có `zFix` cho áp phẳng) vào `cast3d` thay bản sao trong `shots_w1.js` và `shots_w2.js`.
- **Đ2 (mã dùng chung):** `common.watchInHand` đặt đồng hồ theo lòng tay SHEET cũ (lệch 7,8–9,2 cm với tay MPFB). Nên đổi sang `ch.gripPoint('R')` cho mọi gói; s06 hiện bù bằng IK tay.
- **Đ3 (sheet đạo cụ, P):** chỗ để **sào mồi** khi đi/chạy (tồn đọng Cổng 5). Nhịp mồi đèn lồng s04 hiện làm bằng tay trái mở cửa đèn, không thấy sào.
- **Đ4 (continuity, chủ dự án/P):** nối s24c → s25: Cas dựa tường (0,20 m) → s25 đứng làm chim cách tường 0,95 m (đổi chỗ 0,75 m qua cắt, cùng lúc quay người như Cổng 5). Nếu không nhận: (a) W2 dời CAS_W về 0,20 m + bước ra trong s25 (đụng shot W2 đã đóng), hoặc (b) W1 chỉ cho Cas dựa tường ở s24c và bước ra cuối shot (1,5 s — không đủ để diễn một bước rõ).
- **Đ5 (kiểm mắt):** P xem s22 ở 1920×1080 để chấm viền nước (960 px không đủ). Không render still 1080 trong vòng này (hàng đợi nặng dành cho render W1).

## 9. Rủi ro
- R1: tay phải hụt thanh móc 1,5–2,5 cm ở s05, s11, s13, s14 (§3).
- R2: s24c → s25 đổi chỗ Cas 0,75 m (Đ4).
- R3: kiểm mù chưa chạy — cột TƯ THẾ (settle trên đất chỉ 3 shot; trên thang chỉ thở) có thể vẫn bị chê "cứng" ở khung tĩnh MS/WS.
- R4: IK nhiều tay làm render chậm hơn Cổng 5 (1,33 → 1,5–9,4 s/khung, §7).
- R5: s06 nhịp gõ kính (tay trái) vẫn không đọc rõ trên insert — như Cổng 5 (§6).
- R6: s04 nhịp mồi đèn lồng ở toàn cảnh cao 28 mm, 0,35 s — nhỏ, khó đọc.
- R7: s24c tay Cas áp tường cạnh hông — đo chạm (−3 mm) nhưng trên khung 3/4 trước đọc là tay buông sát hông; "dựa tường" đọc chủ yếu nhờ lưng + bóng sát tường.
- R8: s14 đổi tư thế giơ tay (tư thế cục bộ liftHigh) — thay đổi dàn dựng nhỏ ngoài danh sách việc; P/chủ dự án có thể bác (trả về bằng `--dbg '{"lift":[-62,0,34,-12]}'` để so).

## 10. Token, thời gian
- Thời gian thật: 08:13 → ≈ 12:30 UTC 30/09/2026 (≈ 4,3 giờ; chờ khoá hàng đợi nặng cộng dồn 7 214 s — các lượt chờ chồng nhau — chủ yếu sau render W2 cảnh 4 và s39/s41).
- Token: bộ đếm công cụ ≈ 500 nghìn ngữ cảnh tích luỹ khi viết báo cáo (hạn vòng 1 ≈ 800 nghìn; hạn gói ≈ 1,0 triệu).
- Mọi ảnh trong thư mục này < 200 KB.
