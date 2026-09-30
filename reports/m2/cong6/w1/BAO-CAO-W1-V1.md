# BÁO CÁO W1 — Cổng 6, DIỄN HOẠT cảnh 1–3 (s01 → s24c, 0,0–59,0 s), VÒNG 1

Phiên xưởng W1 · nhánh `cong6-w1-v1` (worktree từ main `00a4ead`) · 30/09/2026 · căn cứ: lệnh giao của P; AUTHORSHIP "Cổng 6 — diễn hoạt" (MỞ W1, B2 s23, 30/09/2026).
Đã sửa: `design/cong5/layout/shots_w1.js`; `shots/layout/shots_w1.json` (trường mới `cong6_w1`), `LAYOUT-W1.md` (mục 15, dòng s22 mục 2), `continuity/canh-1.md`, `canh-2.md`, `canh-3.md`; thư mục này.
**Không** sửa: `bible/`, `checks/` (không đọc mã checks), tài sản khoá, `order_w1.js` (không cần), `sets.js` (không cần), `sets_end.js`, `shots_w2.js`, mã dùng chung. Không chạy kiểm mù, không chạy `checks/run.py`, không render toàn phim.

## 0. Tóm tắt
- **s22 (quyết định cố định):** máy lệch **45°** khỏi hướng mặt (đo 42,2–46,5° suốt shot; Cổng 5: 7,0–11,3°), **giữ MCU 85 mm**, 1,2 m, tĩnh. Mắt v1.5.1: mí che bớt tròng (lidDrop 0,2), glint 0,5 → 0,35, không còn nhìn thẳng máy. Khẩu hình L2 lẩm bẩm.
- **Khẩu hình + biểu cảm L1 (s05), L2 (s22):** 16 kênh + 6 viseme, mốc đo trên tệp take; miệng nói có môi–má–cằm cùng động (richLip của W2 v3).
- **Cầm nắm theo tay MPFB (IK điểm):** thang trên vai (s02, s07, s08, s15, s23), thanh thang khi trèo/tụt (s03, s15, s21, s23), van (s03, s04, s19, s22, s23), thanh móc thang + thân cột khi nghỉ (s03, s05, s11–s15, s21), đồng hồ (s06, s09w), cửa đèn lồng (s04). Trước: lòng tay cách vật 7,8–44 cm; sau: −2,3 mm … +2,5 cm (bảng §3).
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
Đo bằng `--dbg '{"meas":1}'` (bọc `S1` trong `shots_w1.js`, không đổi hình), mỗi 3 khung. "Trước" = tư thế FK của shot (= tư thế Cổng 5 + thở) — khoảng cách tới CÙNG đích; "Sau" = sau IK. Chỉ tính khung tay đã nắm hẳn (trọng số IK ≥ 0,99); khung đang chuyển (trộn) không tính. Âm −0,0023 = lòng tay úp sát mặt vật (như W2).

__GRIP_TABLE__

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
| Tay | trong tay áo, lòng tay cách mặt tường **0,82 m (phải) / 1,09 m (trái)** | **lòng tay phải áp phẳng lên mặt vôi** cạnh hông, cao 0,56 m, ngón chúc xuống — IK điểm: **+0,0026 m** (FK trước IK ở chỗ mới: 0,17–0,18 m); tay trái buông |
| Cách L11 | ≈ 7,1 m | ≈ 7,5 m |
- Thử (probe, loại): tay áp tường ngang vai với tường ở bên phải cậu → từ máy s24c đọc thành "vẫy tay chào"; ngón hướng lên cạnh hông → đọc là "xoè tay". Chốt: lưng tựa tường, lòng tay áp tường ngón chúc xuống; bóng cậu sát người trên tường (đọc được "sát tường").
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
__CLIP_NOTES__

## 7. Thời lượng, render, lệch 0 px
__RENDER_TABLE__

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
- R4: IK nhiều tay làm render chậm hơn Cổng 5 (1,33 → xem §7 s/khung).
- R5: s06 nhịp gõ kính (tay trái) vẫn không đọc rõ trên insert — như Cổng 5 (§6).
- R6: s04 nhịp mồi đèn lồng ở toàn cảnh cao 28 mm, 0,35 s — nhỏ, khó đọc.

## 10. Token, thời gian
__TOKENS__
