# CỔNG 6 — W2 DIỄN HOẠT CẢNH 4–6 (s25 → s48). **DỪNG, chờ chủ dự án**

Ngày 29–30/09/2026. Chỉ thị: AUTHORSHIP "Cổng 6 — diễn hoạt" (W2 một mình, tối đa 2 vòng, kiểm mù 10 dải, C3 cả Ida và Cas; Đ3–Đ6; vòng 2 là vòng cuối).
Nhánh P: `ccr-af7a498d-ss3snk`. Gói W2: `cong6-w2-v1` @3dc9148 → `cong6-w2-v2` @25547c1 (merge vào nhánh P: b8409f6, 5794bc3). **W1 CHƯA mở.**

## 0. Tóm tắt
- **W2 xong 2 vòng** (vòng cuối), tổng phim giữ **140,5 s**, 53 shot (s37 tách thành s37 + s37b). Dò lệch 0 px ngoài phạm vi (s02, s24c): 0 sau cả hai vòng. Dò lại toàn bộ 30 shot W2 từ mã đã merge: **90/90 khung khớp** mp4 W2 nộp (PSNR ≥ 37,2 dB) ở cả v17 và v18.
- **Clip W2 có tiếng tạm:** `screening/w2-cong6-v18.mp4` (81,5 s, 28,5 MB). **Chủ dự án đã tự xem và chấm (30/09): "còn lại okay", kể cả nhịp cười buồn**; một lỗi cột đèn điện 1:03–1:05 → lượt sửa nhỏ W2-v3 (mục 7).
- **Kiểm mù 10 dải + 2 đối chứng:** vòng 1 TRƯỢT (2/10 "mặt nạ" s32, s34, lặp cùng chỗ; s37 nhịp 1 thiếu "cười") → vòng 2 **TRƯỢT 2/10** (s39 "con rối", s41 "đồ chơi"; không lặp cùng chỗ; s37 nhịp 1 có "nụ cười buồn", sát biên). Nhiễu nền đối chứng cộng dồn **4/24 = 16,7 %**. Theo chỉ thị: **không làm vòng 3**.
- **Continuity:** vòng 1: chặn 1 (N1 s40), nên sửa 9 → vòng 2: N1 **đạt**; lỗi mới **chặn 1 (M5 s42b Cas trong suốt — nguồn ở bộ hốc, ngoài phạm vi W2)**, nên sửa 5 (M1–M4, M6), còn mở N3, N7, N9 (một phần).
- **Luật v1.5 (layout-v18):** xem mục 2 (điền khi pipeline xong).
- **C3 lượt Cas:** P phát hiện mức trượt lớn ở s42a/s42b **là hình sai thật** (cánh tay trên bị khối áo len nuốt khi ôm đèn), không phải co ngắn phối cảnh như W2 báo → **không chuyển K**; trình chủ dự án (mục 5).

## 1. Việc P đã làm trước W2 (29/09)
| Việc | Kết quả |
|---|---|
| Khôi phục three.js | `npm ci` (three 0.180.0, integrity khớp lock); `setup.sh` bước 5 + `verify.sh` kiểm (chủ dự án: dán vào môi trường sau W2) |
| Dò lệch với layout-v16 | Mặt nạ C3 + bóng s02, s24c, s37, s41, s42, s42a: **254 ảnh, lệch 0 px**; khung probe so mp4 PSNR 35,7–38 dB (s37 khác ở phụ đề) |
| C3 cả hai nhân vật | `export_c3.js --who ida|cas --offset`; `scripts/p/c3_hai_nv.sh` (luật đọc MỘT nhân vật mỗi thư mục parts → lượt Cas trên `<X>.cas.mp4` liên kết cứng). Mặt nạ Ida sau sửa khớp v16 từng điểm ảnh. **Khiếu nại "C3 một nhân vật" chờ K** (`checks-appeal.md`). Mốc v16 lượt Cas: 21 shot có Cas, đo được 141/565, lệch lớn nhất 19,11 %, 7 shot cần người xem |
| Kiểm mù dạng dải | `kiem_mu.py dai / doi-chung-dai / chuan-bi-dai / chon`; đối chứng lấy trọn một shot (Ellie 104,0–106,3 s; Victoria 330,9–332,08 s) |

## 2. Luật checks v1.5
*(điền sau khi pipeline v18 xong)*

## 3. Kiểm mù (nguyên văn: `reports/m2/cong6/w2/kiem-mu/NGUYEN-VAN.md` vòng 1, `kiem-mu-v2/NGUYEN-VAN.md` vòng 2 — gồm cả đối chứng)
| | Vòng 1 (v17) | Vòng 2 (v18) |
|---|---|---|
| Dải có từ khoá (ngưỡng ≤ 1/10) | **2/10**: s32 "mặt nạ" ×2, s34 "mặt nạ" ×2 (mặt Ida cỡ rộng) | **2/10**: s39 "con rối" (chỉ hàm cử động), s41 "đồ chơi" (WS, không chi tiết mặt) |
| Lặp cùng chỗ ≥ 2 dải | **TRƯỢT** (mặt Ida cỡ rộng) | ĐẠT (hai chỗ khác nhau) |
| s37 kể cả "cười" lẫn "buồn/tiếc" | Nhịp 1 thiếu "cười"; nhịp 2 đạt | Nhịp 1 "một nụ cười buồn… rất khó chắc chắn" (**sát biên**); nhịp 2 đạt |
| Đối chứng có từ khoá | Victoria "ma-nơ-canh" (1/2) | Victoria "ma-nơ-canh" (1/2) |
| Nhiễu nền cộng dồn | 3/22 = 13,6 % | **4/24 = 16,7 %** |
| **Kết luận** | **TRƯỢT** | **TRƯỢT** |
Chi tiết, bảng so vòng 1 ↔ 2 và lời chê không có từ khoá: `kiem-mu/CHAM-V1.md`, `kiem-mu-v2/CHAM-V2.md`. Ghi nhận chính còn lại (vòng 2): Ida cỡ rộng vẫn bị đọc "ông cụ" 3/4 dải; s39 miệng "méo, như bị rách"; s45 quay đầu giật, tay như vuốt; s37b vệt tối trên môi đọc thành ria; s40 bà quay gáy lúc L11 tắt thành "khối trắng vân len" (→ Cổng 7, chủ dự án 30/09).

## 4. Continuity (`shots/layout/continuity/RA-W2-V1.md`, `RA-W2-V2.md` + ảnh bằng chứng)
| | Vòng 1 | Vòng 2 |
|---|---|---|
| Chặn | N1 s40 mặt khuất sớm 6 khung | N1 **đạt** (khung 2621 lửa tắt = mặt khuất); **M5 mới: s42b 2806–2819 Cas trong suốt rồi gần biến mất** (có từ v1, v1 bỏ sót; nguồn đèn/bóng bộ hốc `s5.js` ngoài phạm vi W2) |
| Nên sửa | N2–N10 (9) | Đã sửa: N2, N4 (Đ6), N5, N6, N8, N10, N14. Một phần: N3, N9. **Chưa trên hình: N7** (đèn lồng hông s27/s30 — báo cáo W2 ghi đã làm). Mới: **M1** s42b Ida PHẢI – Cas TRÁI ngược s42a/s42; **M2** s40w đèn lồng đè mặt Cas; **M3** "mẩu tay" s39 suốt shot; **M4** hướng đầu nhảy s40 → s40w; **M6** s42 không đọc được nhịp hơ tay (Đ3 chưa kiểm được trên hình) |
| G/B1 | — | G2, G5, G6, G11, G13, B1 đạt; G10 một phần |

## 5. C3 lượt Cas — sai hình thật ở Cas ôm đèn (P tự đo)
- W2 đo độ dài xương sau IK đúng sheet (vai→khuỷu 0,1957 m, khuỷu→cổ tay 0,1794 m) và kết luận "co ngắn phối cảnh".
- P đo trên chính bộ xuất: `views` của cánh tay trên ở s42a có **foreshorten 0,996–0,997, hidden 0** (không co, không bị vật ngoài che). Chồng mặt nạ lên khung 2736: **cánh tay trên bị khối áo len (thân) nuốt**, trên hình chỉ còn vai phồng + bàn tay trước ngực. Agent continuity vòng 2 xác nhận bằng mắt. → Đây là **hình sai thật** (tay lún vào thân áo khi ôm), gắn với sai lệch đã chấp nhận "vai áo len Cas phồng tròn". **Không** chuyển K.
- Vùng mặt nạ thân trùm lên đèn lồng là thân nhìn qua kính trong suốt (bộ xuất bỏ vật trong suốt không thuộc nhân vật — đúng quy tắc), không phải đèn bị gắn nhãn thân.

## 6. Token và thời gian (số công cụ báo = ngữ cảnh tích luỹ cuối lượt)
| Phần | Token | Thời gian thật |
|---|---|---|
| W2 vòng 1 | 500 811 | ≈ 7,7 giờ (gồm ≈ 3,2 giờ mất do container khởi động lại) |
| W2 vòng 2 | 641 060 tích luỹ (≈ 140 nghìn thêm) | ≈ 3,7 giờ (container khởi động lại lần 2) |
| Continuity vòng 1; vòng 2 | 195 943; 202 511 | 13 phút; 15 phút |
| Kiểm mù vòng 1; vòng 2 (12 subagent mỗi vòng) | ≈ 548 nghìn; ≈ 537 nghìn (44–46 nghìn mỗi dải) | < 1 phút mỗi vòng (song song) |
| P | không đo được chính xác (bộ đếm phiên P reset mỗi lượt chủ dự án) | — |
| **Tổng subagent** | **≈ 2,12 triệu** (ước KE-HOACH cho W2 + kiểm: 1,3–1,5 + ≈ 1,2 triệu) | |
Container khởi động lại **4 lần** trong gói (mất render/lệnh nền; đĩa còn). Pipeline v18 phải chạy lại 2 lần.

## 7. Việc còn lại / chờ chủ dự án
1. **W2-v3 (chủ dự án giao 30/09, hạn ≈ 150 nghìn):** bỏ cột điện khỏi khung s27 (1:04), ánh trắng tràn từ mé đối diện; s39 môi–má–cằm cùng động; s45 quay đầu mượt, tay không vuốt; s37b bỏ vệt trên môi. Rà toàn phim cột điện (mục 8). Báo cáo riêng `reports/m2/cong6/w2/SUA-V3.md`.
2. **Chờ quyết:** M5 (s42b Cas trong suốt — nguồn bộ hốc; Cổng 7 hay sửa riêng), M1 (trục s42b sau khi thêm Ida), M3 (có tính "mẩu tay" PA1 không), cánh tay trên Cas khi ôm đèn (mục 5), N7.
3. Khiếu nại "C3 một nhân vật mỗi thư mục parts" chờ K.
4. `setup.sh` dán vào môi trường (sau W2, cùng ghim phiên bản gói).
5. **W1 chưa mở.**

## 8. Rà cột đèn điện toàn phim (chủ dự án 30/09/2026; luật thế giới v0.6)
Máy: `scripts/p/do_cot_dien.js` — mỗi shot 3 khung (đầu/giữa/cuối), tìm thân cột điện (street.js `electricLamp`) và cột đèn khí (`buildGasLamp`), chiếu 9 điểm dọc thân, **có kiểm che khuất** bằng tia từ máy. Dữ liệu: `reports/m2/cong6/w2/cot-dien/do_cot_dien.jsonl` (53 shot, 159 khung).
| Shot (gói) | Cột điện thấy trong khung (x; z thế giới) | Đèn khí thấy | Mé đường | Kết luận |
|---|---|---|---|---|
| s02, s08, s12, s19 (W1) | phố chính z = **+3,9** (mé nam) | z = −3,9 (mé bắc) | đối diện | **đúng luật** |
| s10e (W1) | quảng trường (166; ±8), (188; −9) | không | — | quảng trường, không có dãy đèn khí trong khung — ghi nhận |
| **s23 (W1)** | (10,8; +3,9) mé nam **và (17,0; −5,9) cột tường chim — mé bắc** | (8; −3,9) L11 mé bắc | **cột (17,0; −5,9) CÙNG MÉ** với đèn khí | **VI PHẠM** — chỉ liệt kê, để W1 |
| **s27 (W2)** | (6,8; 2,2) hệ tường chim = **cột tường chim (17,0; −5,9)** | L11 | **cùng mé** | **VI PHẠM** — sửa ở W2-v3 |
| s37w, s40w (W2) | (10,8; +3,9) mé nam | (8; −3,9) L11 | đối diện | đúng luật |
| 44 shot còn lại | không thấy cột điện | | | — |
- Gốc duy nhất: **cột điện tường chim** (B1 Cổng 5, dựng trong `sets_end.js`, sân trước hông nhà kho, mé bắc). Sửa gốc (dời cột sang mé nam) trong `sets_end.js` sẽ đổi luôn **s23 của W1** → trái lệnh "cảnh 1–3 chỉ liệt kê" và lệch 0 px. Vì vậy W2-v3 chỉ xử lý **s27 trong `shots_w2.js`**; việc dời cột gốc + s23 ghi cho W1 (chủ dự án quyết khi mở W1).
