# CỔNG 6 — W1 DIỄN HOẠT CẢNH 1–3 (s01 → s24c) + B2–B4. **KIỂM MÙ TRƯỢT → DỪNG, chờ chủ dự án**

Ngày 30/09/2026. Chỉ thị: AUTHORSHIP "Cổng 6 — diễn hoạt" (đóng W2, mở W1; B1–B4; kiểm; hạn; DỪNG khi kiểm mù trượt).
Main trước khi mở W1: **`00a4ead`** (merge W2 đã đóng). Nhánh P: `ccr-af7a498d-ss3snk`. Gói: `cong6-w1-v1` @d8f6ffb (merge a06362a), `cong6-b34` @56b5b2f (merge 92c5d07). **W1 chưa merge vào main** (chờ duyệt).

## 0. Tóm tắt
- **W1 v1 xong** (B1 + B2), **gói B3–B4 xong**. Tổng phim giữ **140,5 s**, 53 shot, không đổi id/thời lượng. Lệch 0 px ở shot không đổi: W1 102 ảnh / 34 shot, B3–B4 63 ảnh — **0**. P dò lại mọi shot đổi từ mã đã merge: W1 57/57 khung (PSNR ≥ 36,7 dB), B3–B4 36/36 (≥ 37,2 dB) khớp mp4 nộp.
- **Kiểm mù W1: TRƯỢT** — cột HÌNH 2/10 (s05 "con rối", s22 "búp bê" ×2), lặp cùng vị trí (mặt Ida cỡ cận); TƯ THẾ 1/10 (s24c "ma-nơ-canh"). Nhiễu nền cộng dồn 5/26 = 19,2 %. **Theo chỉ thị: DỪNG, không làm lượt sửa W1.**
- **Continuity W1 + nối W1–W2:** chặn 0 · nên sửa 7 (L1–L7) · ghi nhận 9. B4 (M1, M3, M5, N7, bắp tay Cas) **đạt** trên hình; B3 không còn cột điện trong khung cảnh 4.
- **Luật máy toàn phim (layout-v20):** mục 3 (điền khi pipeline xong).
- Clip: `screening/w1-cong6-v20.mp4` (s01–s24c, 59 s, 19,2 MB); `screening/canh4-s42b-truoc-sau.mp4` (trái v19, phải v20; cảnh 4 + s42b, 12,7 MB).

## 1. Bảng việc
| Mục | Việc | Kết quả | Số đo / ghi chú |
|---|---|---|---|
| B1 | Tư thế đứng (dồn trọng tâm, lệch hông, thở) | Đã làm | Ida s06, s09w, s15; thở trên thang mọi shot thang; Cas dồn chân + thở. Kiểm mù: s24c Cas vẫn đọc "đứng im… ma-nơ-canh" |
| B1 | s24c cầm nắm (dựa tường) | Đã làm (một phần trên hình) | Lòng tay phải → tường 0,82 m → **−3 mm**; Cas đứng (14,3; −7,90) ở s23–s24c (cũ −7,15). Continuity L7: trên hình vẫn đọc như tay buông |
| B1 | s22 xoay 3/4 > 30°, giữ MCU, kiểm mắt v1.5.1 | Đã làm | Góc mặt 7,0–11,3° → **42,2–46,5°**; MCU 85 mm, máy tĩnh; mí che bớt tròng, glint 0,5 → 0,35. **Kiểm mù: mắt "hạt cườm… búp bê"**. Viền nước không thấy ở 960 px (Đ5: xem 1080). Continuity L1: s21 → s22 vượt trục |
| B1 | Khẩu hình + biểu cảm L1 (s05), L2 (s22) | Đã làm | 16 kênh + 6 viseme, mốc từ tệp take L1/L2. Kiểm mù: s05 "miệng méo khi nói", s22 "miệng hầu như không đổi hình" |
| B1 | Cầm nắm Ida (thang, van, sào, đồng hồ, cửa đèn lồng) | Đã làm | Lòng tay → vật 7,8–55 cm → −2,3 mm … +2,5 cm (IK điểm). Còn hụt 1,5–2,5 cm tay phải ở s05, s11, s13, s14 (phải đổi bố cục đã duyệt → không làm). **Kiểm mù: s05 bàn tay "biến dạng nặng… như cái vuốt hay cái sừng, hình khối vỡ" 0–2,5 s**; s13 tay xuyên cột; s06 đầu xuyên mặt đồng hồ |
| B1 | Tồn đọng Cổng 5 thuộc W1 | Một phần | Continuity L3: s06 **không thấy ngón gõ kính** (tiếng gõ 16,80/17,20 s vẫn có); L4: s24 nhịp **hơ tay đếm ba** không đọc được (tay dịch ≤ 3 px) — hai motif bible, căn cứ rubric C1 |
| B1 | (ngoài danh sách) s14 tay trái giơ ngang | W1 tự đổi | Tư thế cũ đọc thành tay buông từ máy cao; chủ dự án có thể bác |
| **B2** | s23 bỏ cột điện khỏi khung (chỉ đạo chủ dự án) | **Đã làm** | Ẩn 13 vật của cột tường chim trong shot; PointLight của cột dời sang vỉa hè nam ngoài khung (17,4; 6,2; 4,1) — cùng chỗ s27; ở s23 cột vẫn tắt nên không có ánh. Cột P5 (10,8; +3,9) mé nam giữ (đúng v0.6). `sets_end.js` không đổi |
| B3 | Hướng ánh cảnh 4 từ mé đối diện | **Đã làm** | Cột sân ẩn s25–s32; nguồn (7,2; 6,2; 12,2) như s27; hệ số 0,85 (s27 giữ 2,7) để giữ mức cũ: tường s28 137 → 143 và 151 → 146, s32 147 → 150 … 153 → 161 (/255, lệch ≤ 5,3 %). Chim bóng s28 tắt khi điện bật; s32 chim đèn lồng vẫn rõ |
| B4 | M5 s42b Cas trong suốt | **Đã làm — continuity đạt** | Gốc: quầng sprite đèn lồng bật lại 1,9 s + tư thế ôm ép đèn vào ngực → tắt quầng + tư thế mới |
| B4 | M1 trục s42b | **Đã làm — đạt** | Máy (3,6; 1,3; 7,4): Ida trái, Cas phải như s42a/s42. **Mới L5:** mặt nghiêng + bàn tay Ida đen đặc như bóng cắt (ánh sáng → Cổng 7) |
| B4 | M3 "mẩu tay" s39 | **Đã làm — đạt** | Bà buông van suốt vế cuối. (Continuity L2: lỗi cùng dạng ở **s22** góc dưới-trái) |
| B4 | Bắp tay Cas lún vào áo khi ôm đèn | **Đã làm — đạt trên hình (s42a)** | Vai trước 34°, dang 14°, khuỷu −78° (cũ −12°, −18°, −112°); khuỷu ra ngoài trục thân 1,5–3,2 → 6,0–7,1 cm, ra trước −1,7 → +8,8 cm; quai trước cổ 0,187 → 0,270 m; độ dài xương không đổi. C3 lượt Cas: mục 3 |
| B4 | N7 đèn lồng hông s27, s30 | **Đã làm — đạt** | s27 lùi đèn 9 cm; **s30: bà bước vào đã cầm đèn tay phải (nhịp tháo móc ngoài hình) — thay đổi diễn nhỏ, chờ chủ dự án xem** |

## 2. Kiểm mù W1 (`reports/m2/cong6/w1/kiem-mu/`: CHAM-W1.md, NGUYEN-VAN.md gồm cả đối chứng)
10 dải: s02, s03, s05, s22, s23, s24c (cố định) + s06, s07, s13, s15 (hạt giống `d425369e852f43fa`).
| Tiêu chí | Kết quả |
|---|---|
| HÌNH ≤ 1/10 | **2/10 — TRƯỢT** (s05 mặt "cứng, giống con rối"; s22 mắt "hạt cườm… búp bê", "búp bê sáp", da "nhựa hoặc sáp") |
| TƯ THẾ ≤ 1/10 | 1/10 (s24c Cas "đứng im… ma-nơ-canh") |
| Không lặp cùng vị trí ≥ 2 dải | **TRƯỢT** (mặt Ida cỡ cận: s05, s22) |
| Đối chứng / nhiễu nền | Victoria trúng lần thứ 3 ("búp bê" về miệng); cộng dồn **5/26 = 19,2 %** |
Lời chê không có từ khoá, chỉ đúng chỗ thật: s05 bàn tay vỡ hình; s06 đầu xuyên đồng hồ; s13 tay xuyên cột, mặt thành "khối nâu"; s15 xuống thang ~1 s "như trượt hoặc rơi"; s03 leo nhanh bất thường; ánh sáng đèn bật tràn quá mạnh (Cổng 7).

## 3. Luật checks v1.5 toàn phim (layout-v20)
*(điền khi pipeline xong)*

## 4. Continuity (`shots/layout/continuity/RA-W1-V1.md` + ảnh `reports/m2/cong6/w1/ra-continuity/`)
| Mã | Shot | Lỗi | Mức |
|---|---|---|---|
| L1 | s21 → s22 | Vượt trục (máy s21 phía −x cột, s22 phía +x) | nên sửa |
| L2 | s22 | "Mẩu tay" góc dưới-trái suốt shot (da, măng sét cạnh van) | nên sửa |
| L3 | s06 | Không thấy ngón gõ kính đồng hồ (motif bible) | nên sửa — **agent đề nghị chủ dự án xét nâng lên chặn** |
| L4 | s24 | Nhịp hơ tay đếm ba không đọc được (motif bible) | nên sửa — **xét nâng lên chặn** |
| L5 | s42b | Mặt nghiêng + tay Ida đen đặc (sau M1) | nên sửa → Cổng 7 (ánh sáng) |
| L6 | s15 | Thang nhảy từ tựa cột lên vai trong 1 khung (1070 → 1071) | nên sửa |
| L7 | s24c | Tay Cas chạm tường (−3 mm) nhưng đọc như tay buông | nên sửa |
| — | s24c → s25 | Cas đổi chỗ **0,75 m** qua cắt (đo motion) | ghi nhận (ranh cảnh 3/4, cắt vốn lược vài giây; trục, ánh sáng, trang phục khớp) — **chờ chủ dự án duyệt** |
Đạt: M1, M3, M5, N7, bắp tay Cas s42a, B3; L1–L11 bật đúng thứ tự; giờ đồng hồ chỉ tiến; s23 không còn cột điện cùng mé; s22 3/4 ≈ 45° MCU; model sheet cảnh 1–3 khớp. Ghi nhận khác: L6 bắt lửa khi Ida còn cách 8,7 m; `canh-3.md`/`canh-4.md` còn số cũ (casSpot 0,95 m, cột sân trước) — cần sửa tài liệu.

## 5. Đề xuất của W1 (chờ quyết)
- **Đ1:** đưa `gripAt` (IK điểm) vào `cast3d` (mã dùng chung) thay bản sao ở W1/W2.
- **Đ2:** `watchInHand` (`common.js`) đặt đồng hồ theo `gripPoint` tay MPFB (hiện lệch 7,8–9,2 cm; s06 bù bằng IK).
- **Đ3:** sheet đạo cụ quy định chỗ để sào mồi khi đi.
- **Đ4:** nối s24c → s25 (Cas đổi chỗ 0,75 m) — chấp nhận hay sửa.
- **Đ5:** xem s22 ở 1080 để chấm viền nước mắt.

## 6. Token và thời gian (số công cụ báo)
| Phần | Token | Thời gian thật |
|---|---|---|
| W1 v1 (B1 + B2) | 512 966 (hạn vòng 1 ≈ 800 nghìn; hạn W1 1,0 triệu) | 08:13 → ≈ 12:30 UTC (≈ 4,3 giờ, phần lớn chờ hàng đợi render) |
| B3–B4 (phiên W2 cũ) | ≈ 67 nghìn thêm (752 520 tích luỹ) — hạn 250 nghìn | ≈ 3,5 giờ (chờ hàng đợi) |
| Kiểm mù W1 (12 subagent) | ≈ 536 nghìn (43,7–46,3 nghìn mỗi dải) — hạn 600 nghìn | < 1 phút |
| Continuity W1 + nối | 233 409 | 17 phút |
| P | không đo được chính xác | — |
Render W1 qua hàng đợi nặng: 1 332 khung, 5 817 s.

## 7. Việc đang chờ chủ dự án
1. **Kiểm mù W1 trượt** → quyết có mở lượt sửa W1 không (ưu tiên P đề xuất: bàn tay s05; mắt/mặt s22 và s05; xuyên hình s06, s13; nhịp thang s15, s03).
2. Continuity: nâng L3 (gõ kính s06), L4 (đếm ba s24) lên chặn? Nhận hay sửa L1 (vượt trục s21 → s22), L7; duyệt mức ghi nhận nối s24c → s25 (Đ4).
3. s30 thay đổi diễn (bà vào đã cầm đèn); s14 tay giơ ngang.
4. Đ1, Đ2, Đ3, Đ5.
5. L5 (s42b mặt Ida đen) → Cổng 7.
6. W1 chưa merge vào main; khiếu nại "C3 một nhân vật" vẫn chờ K; `setup.sh` chưa dán vào môi trường.
