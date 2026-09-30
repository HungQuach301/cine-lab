# SỬA W1-v2 — Cổng 6, phương án A (30/09/2026)

Phiên P · nhánh `ccr-af7a498d-ss3snk`. W1-v2 của phiên xưởng: `cong6-w1-v2 @bff70cc`, gộp vào nhánh P ở `ce70d4d`. **Chưa merge main.**
Căn cứ: chỉ thị chủ dự án "W1: MỞ LƯỢT SỬA W1-v2 (phương án A)" và AUTHORSHIP "Cổng 6 — diễn hoạt".
Tài liệu gốc:
- báo cáo xưởng `BAO-CAO-W1-V2.md`;
- kiểm mù `kiem-mu-v2/CHAM-W1-V2.md`;
- continuity `shots/layout/continuity/RA-W1-V2.md`;
- luật `reports/checks/layout-v21/`, `reports/checks/layout-v21-c3-cas/`.

## 0. Tóm tắt
| Hạng mục | Kết quả |
|---|---|
| Việc a–k | 10 mục đã làm. Đ3 (chỗ để sào mồi) chỉ là đề xuất, chờ duyệt (§6) |
| Lệch 0 px toàn phim | 159 ảnh / 53 shot: chỉ **9 shot W1 cố ý đổi** (25 ảnh). **W2: 0 px.** Các shot W1 có IK không đổi: 0 px, nên Đ1 `ch.gripAt` trùng từng bit với bản sao cũ |
| Luật v21 (LOCK `8d55b6ad…` khớp) | **Không lỗi mới ở luật chặn đã đạt.** Vẫn trượt như v20: G3b, H1b, C3 (§3) |
| Kiểm mù vòng 2 | **TRƯỢT.** HÌNH 4/10; mặt Ida bị chê lặp ở 3 dải (s03, s05, s22). Theo chỉ thị: DỪNG, không tự mở vòng 3 |
| Continuity | L3 (chặn) **đạt**. L4 (chặn) **chưa đủ**. Có lỗi mới K2 (quả bông mũ Cas), đề xuất xếp chặn |
| Clip | `screening/w1-cong6-v21.mp4` (s01–s24c, tiếng tạm + phụ đề, 19,4 MB) |
| Sau khi báo cáo | Chủ dự án đã quyết phương án A (W1-v3 + gói THỬ MẶT). W1-v3 đang chạy trên nhánh `cong6-w1-v3` |

## 1. Bảng việc a–k (tóm từ `BAO-CAO-W1-V2.md`, P kiểm lại)
| Mục | Trạng thái | Số đo / kiểm của P |
|---|---|---|
| a. s05 tay vỡ hình | Đã sửa gốc: tư thế ngón + góc máy | Continuity: đạt. Kiểm mù v2 vẫn chê tay "như móng vuốt… trôi" ở 3,0–3,5 s → giao W1-v3 (a) |
| b. s06 xuyên đồng hồ; ngón gõ kính (L3) | Đã sửa | Continuity: **L3 đạt**. Ngón chạm kính ở khung 403 và 413; tiếng gõ ở 16,800 / 17,200 s. Lỗi mới nhẹ: K1 (bàn tay lạ 1 khung ở 398), K3 (đồng hồ vụt khỏi khung 441–442) |
| c. s13, s15, s03 | Đã sửa | Continuity: đạt. C3: xem §3 |
| d. L1 trục s21 → s22 | Đã sửa | Góc mặt so với trục máy 54,2–59,1°. Continuity: đạt. K7: s22 thành CU chặt hơn MCU |
| e. L2 mẩu tay s22 | Đã sửa | Continuity: đạt |
| f. s24 đếm ba (L4) | Đã sửa một phần | Biên độ ngang 30,9 / 21,2 px (v1 ≤ 3 px). Continuity: **chưa đủ**, vì lòng tay thấp hơn đáy lồng L11 40–47 px → giao W1-v3 (d) |
| g. s24c Cas dựa tường | Đã sửa | Continuity: L7 chưa rõ (tay giấu sau lưng), K4 "như không có tay", **K2 quả bông mũ lún vào tường rồi mất từ khung 1391** → giao W1-v3 (c) |
| h. Mặt Ida cận bằng dàn dựng | Đã làm | Kiểm mù v2: **vẫn chê** (s05 "con rối", s22 "sáp/búp bê", s03 "mặt nạ") → gói THỬ MẶT |
| i. Đ1, Đ2 | Đã làm (Đ2 mặc định giữ cách cũ) | 0 px toàn phim (§2) |
| j. Giữ s30, s14, nối s24c → s25 | Giữ | — |
| k. continuity canh-3, canh-4 | Đã sửa | K6: `canh-1.md`, `canh-2.md`, `canh-3.md` còn ghi s22 ở phía +x, nhìn trái |

## 2. Lệch 0 px toàn phim
- Gốc: `387a7fa`, tạo trước mọi sửa.
- Sau: mã `56b834a`.
- Kết quả: 159 ảnh (3 ảnh/shot × 53 shot), **lệch 25 ảnh, đúng 9 shot cố ý đổi**: s03, s05, s06, s13, s15, s22, s23, s24, s24c.
- **30 shot W2: 0 px.** s09w (Đ2) và các shot W1 có IK không đổi: 0 px.
- P kiểm probe 27/27 khớp giữa thumbs và mp4 của xưởng.

## 3. Luật máy v21 (layout-v21; checks v1.5, LOCK khớp; P không sửa checks/)
| Luật | v20 | **v21** | Ghi chú |
|---|---|---|---|
| N1, N2, P0, P1, G4, G3, M3, J1, J1b, H1, O3 | ĐẠT | **ĐẠT** | — |
| G3b | TRƯỢT | **TRƯỢT** | σ nhỏ nhất 0,70 (≥ 0,8 ✗), CV lớn nhất 0,180 (≤ 0,2; sát ngưỡng −10 %, ngoài ±5 %), σ lớn/nhỏ 3,19, tương quan 0,895. Layout chưa có grain (Cổng 7) |
| H1b | TRƯỢT (7 track) | **TRƯỢT (8 track)** | 8 track không đo được |
| **C3 lượt Ida** | 6 · 60 · 46 | **6 · 60 · 48**; 20 shot cần người xem | `so_sanh_c3.py v20 v21`: **không shot nào đổi kết quả**. Trong các shot W1 đã sửa: s13 thân +20,3 % (v20 +13,2 %); s15 cẳng tay −18,0 % ở khung 1068 (v20 −7,1 %); s19, s23 giữ nguyên |
| **C3 lượt Cas** | 4 · 28 · 108 | **4 · 31 · 86**; 10 shot cần người xem | Đổi: **s23 KCM → TRƯỢT** (cánh tay trên +15,6 đến +19,8 %); **s24 KCM → TRƯỢT** (cẳng tay −56,6 đến −60,9 %, cánh tay trên foreshorten 0,62); **s24c TRƯỢT → không đo được** |
| Kiểm toán | ĐẠT | **ĐẠT** | Ida: hạt giống 16668428273237913651, khung [276], bóng [1770]. Cas: 10692223967103721179, khung [660] |

**P kiểm C3 mới** bằng `views` và chồng mặt nạ lên khung render (ảnh `sua-v2/c3_v21_*.png`):
- **Cas s24 (1356, 1368):** tư thế W1-v2 có hai tay vòng sau lưng áp tường. Cẳng tay chỉ lộ **6 px** cạnh thân; phần còn lại bị chính thân che. Đây là che khuất do tư thế, không lún, không xuyên. Cánh tay trên foreshorten 0,62 là co ngắn thật. **Ghi số, không chỉnh.**
- **Cas s23 (1260–1320):** Cas cao khoảng 26 px trong khung. Cánh tay trên dài 8 px, nên lệch 16–20 % tương ứng 1–2 px. Đây là sai số đo ở cỡ quá nhỏ; không thấy kéo hay xuyên. **Ghi số.**
- **Ida s13 (948):** mặt nạ thân khớp áo gilê trên hình, không xuyên. Thân đọc dài hơn vì bà cúi (thân 10°) và máy cao; foreshorten 1,02. **Ghi số.**
- **Ida s15 (1068):** đèn lồng che cẳng tay trái khi nhấc thang. **Ghi số.**
- Với W1-v3 (c), P sẽ kiểm lại C3 Cas ở s24c sau khi đổi tư thế đầu.

**Chỉ số trong ±5 % quanh ngưỡng:**
- C3 hệ số mặt nạ 4 (≤ 4);
- C3 hệ số khi đầu nhỏ 4 (≥ 3,98).

## 4. Kiểm mù vòng 2 (`kiem-mu-v2/`)
| Tiêu chí | Kết quả |
|---|---|
| HÌNH ≤ 1/10 | **4/10**: s03 "mặt nạ", s05 "con rối", s22 "búp bê/sáp", s24c "con rối, ma-nơ-canh" (khối thân/vai Cas) → **TRƯỢT** |
| TƯ THẾ ≤ 1/10 | 0–1/10 → đạt |
| Không lặp cùng vị trí | **Mặt Ida cận bị chê ở 3 dải** → **TRƯỢT** |
| Nhiễu nền cộng dồn | 5/28 = 17,9 %; đối chứng lần này 0 từ khoá |

Lời chê không có từ khoá nhưng chỉ đúng chỗ thật:
- tay s05 "như móng vuốt";
- mũ s22 xê dịch; chân tóc lùi như hói;
- quả bông mũ Cas mất; khe cổ Cas;
- bóng lạ ở s04, s03, s23;
- ánh sáng nhảy ở s12, s19 (Cổng 7);
- s23 chỉ thấy một người (Cas quá nhỏ ở cỡ WS).

## 5. Continuity (`shots/layout/continuity/RA-W1-V2.md`, ảnh `ra-continuity-v2/`)
- **Chặn:**
  - L4 chưa đủ;
  - K2 quả bông mũ Cas (đề xuất chặn).
- **Nên sửa:**
  - L7, K4: s24c đọc như Cas đứng trước tường, tay giấu;
  - K1: bàn tay lạ 1 khung ở s06 (khung 398);
  - K3: đồng hồ vụt khỏi khung (441–442);
  - K5: tay s24 thấp hơn lồng kính.
- **Ghi nhận:**
  - K6: tài liệu canh-1, canh-2, canh-3 còn số cũ;
  - K7: s22 thành CU;
  - K8: nối s24 → s24c → s25 đúng trục.
- Ba mục của chủ dự án (a, b, c, d của W1-v3) đã phủ L4, K2, K5 và cổ Cas. **K1, K3, K4/L7, K6, K7 chưa được giao**: P trình ở §7.

## 6. Đề xuất Đ3 của xưởng (sheet đạo cụ trong `bible/`, chờ duyệt)
**Nội dung:** sào mồi móc dọc thanh trái của thang bằng hai khuyên da (ở 1/3 và 2/3 thang). Đầu có bấc hướng lên, cao hơn đầu thang 0,4 m. Bà gỡ sào ở bậc trên cùng trước khi mồi (s21).

| | |
|---|---|
| Ưu | Lấp chỗ hở continuity cảnh 1–3 (sào chỉ thấy ở s21) |
| Nhược | Render lại 5 shot đi (s02, s07, s08, s15, s23); thang trên vai rậm hơn ở tele s08 |
| Rủi ro | Sửa sheet khoá, cần chủ dự án duyệt |

**Đề xuất của P:** để sau W1-v3, gộp vào lượt đóng W1 nếu chủ dự án duyệt.

**Đ2 cho W2** (`watchInHand` theo gripPoint ở s45, s46, s45c): mặc định chưa bật. Nếu bật sẽ đổi pixel các shot W2 đã đóng, cần duyệt riêng. **P đề xuất giữ như cũ tới Cổng 7.**

## 7. Việc đang chờ chủ dự án
1. Xem và duyệt W1-v3 (đang làm).
2. Mục continuity chưa giao: K1, K3 (s06), K4/L7 (s24c tay), K6 (tài liệu), K7 (cỡ s22 CU). **P đề xuất:**
   - K6: P tự sửa trong lượt đóng W1;
   - K1, K3: gộp vào W1-v3 nếu còn hạn, vì sửa nhỏ và chỉ ở s06;
   - K4/L7, K7: nhận như hiện trạng.
   Cần chủ dự án quyết.
3. Đ3 sào mồi; Đ2 cho W2.
4. C3 Cas s23, s24 (che khuất và cỡ nhỏ): chủ dự án nhận ghi số, hoặc giao K xem.

## 8. Token và thời gian thật (số công cụ báo)
| Việc | Token | Thời gian (UTC 30/09/2026) |
|---|---|---|
| Xưởng W1-v2 (sửa) | ≈ 135–142 nghìn (hạn 400 nghìn) | 13:42 → 15:45 |
| Pipeline v21: ghép, đóng gói, mặt nạ, bóng, luật, C3 Cas | — (máy) | 15:38 → 17:22 (mặt nạ Ida 1 698 s, luật 442 s, C3 Cas 1 375 s + luật 235 s) |
| Kiểm mù vòng 2 (12 dải) | ≈ 535 nghìn (hạn 600 nghìn) | ≈ 15:50 → 16:40 |
| Rà continuity W1-v2 | ≈ 134 nghìn | ≈ 16:10 → 16:20 |
| Cộng dồn W1 (sửa v1 + v2) | ≈ 655 nghìn | — |
