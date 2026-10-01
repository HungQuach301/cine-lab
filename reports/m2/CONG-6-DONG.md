# CỔNG 6 — DIỄN HOẠT: ĐÓNG (01/10/2026)

Chủ dự án duyệt đóng W1 có điều kiện luật v22 sạch (AUTHORSHIP "Cổng 6 — diễn hoạt", 01/10/2026). Luật v22 sạch, nên P merge nhánh P `ccr-af7a498d-ss3snk` vào `main`.
- Main trước khi mở W1: `00a4ead` (W2 đã đóng).
- Bản phim hiện hành: **`screening/layout.mp4` = layout-v22** (140,5 s, 53 shot, 16:9, 24 fps, tiếng tạm + phụ đề).

## 1. Tóm tắt W2 (cảnh 4–6, s25 → s48): đóng 30/09/2026 sau clip v19
- **Các lượt:**
  - Vòng 1 và vòng 2 (vòng cuối) đều TRƯỢT kiểm mù 2/10; theo chỉ thị không làm vòng 3.
  - W2-v3 sửa nhỏ, không kiểm mù: bỏ cột điện khỏi khung s27, s39 môi–má–cằm, s45 quay đầu, s37b.
  - Gói B3–B4: hướng ánh cảnh 4; M1, M3, M5, N7; bắp tay Cas lún vào áo ở s42a/s42b là hình sai thật, đã sửa.
- Chủ dự án tự xem clip: "còn lại okay", kể cả nhịp cười buồn ở s37.
- Luật thế giới v0.6: cột điện luôn ở mé đường đối diện dãy đèn khí.
- Báo cáo: `reports/m2/CONG-6-W2.md`, `reports/m2/cong6/w2/SUA-V3.md`. Clip: `screening/w2-cong6-v19.mp4`.

## 2. Tóm tắt W1 (cảnh 1–3, s01 → s24c)
- **W1 v1** (B1 tư thế đứng, s24c, s22 3/4; B2 bỏ cột điện ở s23): kiểm mù TRƯỢT 2/10 (mặt Ida cận). Báo cáo `CONG-6-W1.md`.
- **W1-v2** (phương án A, việc a–k):
  - s05 tay vỡ hình; s06 ngón gõ kính khớp tiếng (L3 đạt);
  - s24 đếm ba; s22 trục máy cùng phía s21 và mẩu tay;
  - s13, s15, s03; Cas dựa tường ở s24c;
  - Đ1 `gripAt` đưa vào cast3d, Đ2 `watchInHand` theo gripPoint (mặc định giữ cách cũ).
  - Kiểm mù vòng 2 TRƯỢT 4/10, mặt Ida cận lặp ở s03, s05, s22. Theo chỉ thị DỪNG, không mở vòng 3. Báo cáo `cong6/w1/SUA-W1-V2.md`.
- **W1-v3** (sửa nhỏ, không kiểm mù):
  - s05 tay khum;
  - s22 mũ đội sụp che chân tóc;
  - s24c giữ quả bông mũ, cổ áo khép;
  - s24 ba nhịp tách bạch, tay ngang lồng kính.
  - Báo cáo `cong6/w1/SUA-W1-V3.md`. Clip `screening/w1-cong6-v22.mp4`.
- **Lệch 0 px:** mọi lượt W1 đều dò toàn phim (53 shot); chỉ shot cố ý đổi mới đổi pixel, **W2 0 px** trong mọi lượt.
- **Gốc lỗi mặt Ida** (thái dương không tóc, thiếu nếp nhăn tuổi, tai to): gói THỬ MẶT 2 đã mở rồi **dừng ngày 01/10/2026** do chủ dự án chuyển hướng (§6). Phần đã làm lưu ở `reports/m2/cong7/thu-mat-2/ma-dung-do.patch`, không áp vào phim.

## 3. Luật máy v22 toàn phim (checks v1.5, LOCK `8d55b6ad…` khớp; P không sửa checks/)
| Luật | v21 | **v22** | Ghi chú |
|---|---|---|---|
| N1, N2, P0, P1, G4, G3, M3, J1, J1b, H1, O3 | ĐẠT | **ĐẠT** | N3, M1 không áp cho profile 'shot' |
| G3b | TRƯỢT | **TRƯỢT** | layout chưa có grain; σ nhỏ nhất 0,699 (≥ 0,8), CV 0,181 (≤ 0,2) → Cổng 7 |
| H1b | TRƯỢT (8) | **TRƯỢT (9 track không đo được)** | tăng ở shot W1-v3 cố ý đổi (s05 tay ra khỏi khung, s22 đầu; s24 tay lướt trước đầu) → Cổng 7 / K |
| C3 lượt Ida | 6 · 60 · 48 | **6 · 60 · 48** | không shot nào đổi kết quả; 20 shot cần người xem |
| C3 lượt Cas | 4 · 31 · 86 | **7 · 31 · 86** | s24c ĐẠT; s23, s24 ghi số (che khuất do tư thế, cỡ nhỏ); 9 shot cần người xem |
| Kiểm toán | ĐẠT | **ĐẠT** | Ida hạt giống 3971412076296412155 [636, 1752], bóng [990]; Cas 3861284491023571045 [564] |

**Kết luận:** kết luận từng luật trùng v21, C3 không xấu đi, không có lỗi mới. Điều kiện đóng đã đủ.
**Chỉ số trong ±5 % quanh ngưỡng:** C3 hệ số mặt nạ 4 (≤ 4); C3 hệ số khi đầu nhỏ 4 (≥ 3,98).
Báo cáo đầy đủ: `reports/checks/layout-v22/`, `reports/checks/layout-v22-c3-cas/`.

## 4. Sai lệch đã chấp nhận và việc chuyển sang Cổng 7
| Mục | Nguồn | Chuyển |
|---|---|---|
| Ánh sáng phẳng (mặt dưới ánh điện; kiểm mù chê "sáp", "mặt nạ") | kiểm mù W1/W2 | Cổng 7 (ánh sáng + vật liệu da; THỬ MẶT) |
| s27, s45 nền cháy trắng; quầng L11 mất ở s27 | chủ dự án, Claude rà | Cổng 7 |
| s40 khi L11 tắt cảnh không tối đi; gáy "cục len trắng" | Claude rà | Cổng 7 |
| L5: s42b mặt Ida đen | continuity | Cổng 7 |
| Thân Cas phồng (vai "bướu", "ống phồng") | kiểm mù vòng 2, chủ dự án | giữ sai lệch; xem lại ở Cổng 7 |
| Grain (G3b) | luật | Cổng 7 |
| H1b (track không đo được, khớp luồng) | luật | Cổng 7; cần K xem cách đo khi tay che đầu |
| Mặt Ida cận (búp bê/sáp/mặt nạ) | kiểm mù W1 v1, v2; THỬ MẶT V1 | **không sửa tiếp** — chủ dự án bỏ hướng mặt bán tả thực (§6) |
| Tiếng tách gập nắp đồng hồ (Đ4) | chủ dự án | Cổng 8 |

**Tồn đọng nhỏ ghi nhận (chưa giao; đóng W1 không kèm):**
- continuity K1 (bàn tay lạ 1 khung s06, khung 398), K3 (đồng hồ vụt khỏi khung s06, 441–442);
- K4/L7 (tay Cas s24c khuất sau lưng); K6 (canh-1/2/3 còn số cũ); K7 (s22 thành CU);
- s05 tay rời khung ở 2,8 s bị một người xem đọc "biến mất";
- s22 mũ còn bị đọc "lơ lửng", gốc là thái dương, đã vào THỬ MẶT 2;
- C3 Cas s23, s24 (ghi số);
- Đ3 sào mồi (chờ duyệt sheet đạo cụ); Đ2 bật cho W2 (P đề xuất giữ cách cũ);
- khiếu nại C3 một nhân vật mỗi thư mục parts (chờ K; P đã bắc cầu bằng lượt Cas riêng).

P đề xuất xử lý nhóm này trong lượt render Cổng 7, khi các shot liên quan phải render lại.

## 5. Bài học chính
1. **Mặt người bán tả thực dựng bằng mã không qua được kiểm mù sau 3 vòng.**
   - Kiểm mù W1 v1, W1 v2 và THỬ MẶT V1 đều trượt ở cùng chỗ: mặt Ida cỡ cận bị đọc "búp bê / sáp / mặt nạ / con rối".
   - Diễn hoạt và dàn dựng (PA1: tránh chính diện, mí che, key từ đèn) đã giảm lời chê, nhưng không hết.
   - Vật liệu và ánh sáng (V1) đổi được số đo (s03 mặt cháy sáng 86,9 % → 3,5 %) nhưng không đổi được cách người xem đọc: lời chê chuyển sang màu da, rồi sang hình khối (thái dương "hói", không nếp nhăn tuổi, tai to).
   - Mỗi vòng sửa tốn ≈ 0,15–0,5 triệu token cho xưởng, cộng ≈ 0,5 triệu cho kiểm mù.
2. **Kiểm mù bằng dải khung tĩnh rất nhạy với mặt và hình khối, nhưng kém với chuyển động.**
   - Vi chuyển động mặt, nhịp diễn và tiếng không được đo.
   - Nhiễu nền đối chứng (Sprite Fright) ổn định ở 16–19 %, nên ngưỡng "≤ 1/10" vẫn có ≈ 0,4–0,5 xác suất trượt oan với nhân vật tốt.
3. **Cái đã chạy tốt:**
   - nhân vật ở cỡ trung–xa hoặc thành bóng;
   - ánh đèn khí làm mảng ấm;
   - ngôn ngữ cảnh phố;
   - đường ống máy: luật v1.5, dò lệch 0 px toàn phim, kiểm toán C3.
   - Đây là cơ sở cho hướng mới: không cận mặt người, hoạt hình tiết chế 2.5D.
4. **Chi phí và nhịp:**
   - một vòng sửa + kiểm cho 1/3 phim tốn ≈ 1–1,5 triệu token;
   - pipeline luật toàn phim ≈ 1,7 giờ máy mỗi phiên bản;
   - container khởi động lại ≥ 6 lần, nên mọi bước dài phải chạy tách nền và commit ngay.

## 6. Chuyển hướng (01/10/2026)
- Chủ dự án quyết không hoàn thiện Last Round thành phim nghệ thuật riêng, mà phát triển kênh lai: truyện cách điệu + số liệu, tên tạm **Last Lamplighters**.
- Làm tập thử có tiêu chí dừng (AUTHORSHIP "Định hướng", 01/10/2026). Tài sản Last Round được dùng lại cho cảnh truyện.
- Mốc tiếp theo: bài thử phong cách (B1 toon + viền nét, B3 2.5D cắt giấy) và kịch bản tập thử "The Last Lamplighters".

## 7. Token và thời gian (số công cụ báo)
| Gói | Token | Thời gian thật |
|---|---|---|
| W2 vòng 1 + vòng 2 | ≈ 641 nghìn tích luỹ | ≈ 11,4 giờ (gồm ≈ 3,2 giờ mất do container khởi động lại) |
| W2-v3; B3–B4 | ≈ 40 nghìn; ≈ 67 nghìn | ≈ 50 phút; ≈ 3,5 giờ (chờ hàng đợi) |
| W1 v1; W1-v2; W1-v3 | ≈ 513 nghìn; ≈ 142 nghìn; ≈ 59 nghìn (tích luỹ harness ≈ 714 nghìn) | ≈ 4,3 giờ; ≈ 2,1 giờ; ≈ 1,2 giờ |
| Kiểm mù (W2 v1, v2; W1 v1, v2; 12 dải mỗi lượt) | ≈ 548 + 537 + 536 + 535 = ≈ 2,16 triệu | < 1 giờ mỗi lượt |
| Continuity (W2 v1, v2; W1 v1, v2) | ≈ 196 + 203 + 233 + 134 = ≈ 766 nghìn | 13–17 phút mỗi lượt |
| **Tổng subagent Cổng 6** | **≈ 4,3 triệu** | 29/09 → 01/10/2026 |
| P | không đo chính xác (bộ đếm phiên P reset mỗi lượt chủ dự án) | — |
Pipeline toàn phim mỗi phiên bản (ghép → C3 Cas): ≈ 1,7 giờ máy (mặt nạ Ida ≈ 1 650–1 850 s, luật ≈ 440–490 s, C3 Cas ≈ 1 340–1 390 s + luật ≈ 240 s). Container khởi động lại ≥ 6 lần trong Cổng 6.
