# KẾ HOẠCH MỞ W1/W2 — Cổng 6, diễn hoạt (P soạn 29/09/2026). **CHƯA MỞ**, chờ chủ dự án quyết

Nền: characters v1.5.1 (Ida) và v1.6 (Cas) đã khoá. Mặc định: Ida 'bl' v1.5.1, Cas 'bl', thân MPFB, tay MPFB.
Tài sản phải có trên `main` trước khi mở, vì worktree của phiên xưởng tạo từ `main`.

## 1. Tổ chức
| Gói | Phạm vi | Nhánh / worktree | Ghi chú |
|---|---|---|---|
| **W1** | Cảnh 1–3, s01–s24c (22 shot, `shots_w1.js`, `order_w1.js`) | worktree tạo từ `main` sau khi merge khoá | Diễn hoạt Ida: đi, trèo thang, van, sào, đồng hồ; s22 và s24c |
| **W2** | Cảnh 4–6, s25–s48 (`shots_w2.js`, `order_w2.js`) | như trên | Diễn hoạt Cas: chim bóng, thang, đèn lồng. Hai người: PA1 s36–s39, trao đèn s41. Cảnh 6 |
| **P** | Ghép, render toàn phim, luật máy, kiểm mù, continuity, merge | nhánh P | P không sửa `checks/` |
| **Kiểm** | Kiểm mù (subagent mới mỗi khung) + cine-continuity | — | Cách chấm ở mục 2 |

Nhịp: W1 và W2 chạy song song → P ghép + luật → kiểm mù + continuity → báo cáo → DỪNG chờ duyệt.
Mỗi gói có điều kiện dừng và hạn token riêng (mục 5).

## 2. Cách chấm kiểm mù mới (AUTHORSHIP 29/09/2026, áp từ W1/W2)
- Mỗi lần kiểm **≥ 6 khung** nhân vật, cộng **2 khung đối chứng** Sprite Fright (đối chứng chạy mỗi lần để cập nhật nhiễu nền).
- Mỗi lời chê có từ khoá xếp vào **cột HÌNH** (mặt, đầu, thân, quần, áo, tay, vật liệu) hoặc **cột TƯ THẾ** (dáng, cứng đơ…). Câu nói cả hai tính vào HÌNH.
- **ĐẠT khi:**
  - tỉ lệ khung có từ khoá chỉ vào nhân vật, cột HÌNH, **≤ nhiễu nền đối chứng đo được** (hiện 2/20 = 10 %); **và**
  - không có lời chê **cùng một chỗ** lặp ở ≥ 2 khung.
- Lời chê chỉ đúng chỗ thật trên hình **vẫn phải sửa**, dù đã đạt ngưỡng.
- Trên clip đã diễn hoạt, cột TƯ THẾ nay được tính: đó là việc của W1/W2.

**P tính thêm để anh/chị biết (không tự đổi luật):**
- Với 6 khung và ngưỡng 10 %, "≤ 10 %" nghĩa là **0/6 khung**.
- Nếu nhân vật tốt thật và chỉ có nhiễu 10 %, xác suất đạt:

  | Số khung | Số khung trúng được phép | Xác suất đạt |
  |---|---|---|
  | 6 | 0 | **53 %** |
  | 8 | 0 | 43 % |
  | 10 | 1 | **74 %** |
  | 12 | 1 | 66 % |

- **Đề xuất:** mỗi lần kiểm dùng 10 khung, để ngưỡng 10 % cho phép 1 khung. Chủ dự án quyết.

## 3. Việc chuyển W1/W2 (đầy đủ)
| # | Việc | Gói | Căn cứ |
|---|---|---|---|
| 1 | **Tư thế đứng**: hết "cứng đơ, chân thẳng, trọng tâm không rõ" (Ida và Cas). Dồn trọng tâm, hơi lệch hông, thở | W1 + W2 | Kiểm mù W4T2, cột TƯ THẾ |
| 2 | **Shot cầm nắm theo tay mới** (tay Cas ngắn hơn 15,8 %; tâm lòng tay lệch đo thật): s24c dựa tường 7,0 cm · s25 chim bóng 6,4 · s28 vỗ tay 6,4 · s32 chim bóng 7,0 · s37w, s38, s40w giữ thang 6,7 · s41, s42a đèn lồng khoảng 4 (đã nắm quai bằng `gripRing`) · s42 áp tay 6,6 · s42b ôm đèn, s48 chim trên cao (chưa đo, trang thử lỗi) | s24c → W1; còn lại W2 | BAO-CAO-W4T2 mục 4. Chủ dự án ghi "11 shot": danh sách đo được 10 shot, thêm 2 shot chưa đo, tổng 12 |
| 3 | **s41 khoảng cách Cas–Ida**: Cas phải duỗi hết tay mới chạm đèn, nên đặt Cas gần Ida hơn hoặc Ida chìa ngắn lại | W2 | AUTHORSHIP khoá v1.6 |
| 4 | **Ida nhìn xuống Cas ở s42a** (kiểm mù: "ánh mắt đi qua trên đầu đứa trẻ") | W2 | Kiểm mù W4T2 |
| 5 | **Dàn dựng lại PA1 s36–s39** (máy, cỡ; mắt đọc được khi quay nghiêng) | W2 | PLAN Cổng 6 b(3), c |
| 6 | **s22 3/4** (xoay Ida > 30°, giữ MCU) | W1 | PLAN c′, `shots_w1.json` trường `cong6` |
| 7 | **s40: mặt Ida chìm tối** đúng lúc L11 tắt (1:49,2), cố định | W2 | PLAN c′, `shots_w2.json` |
| 8 | **Nhịp cười buồn** s37 ("That's the last one, then.", "Goodnight, old street.") đo trên **clip có tiếng**. Chủ dự án tự chấm; AI mù đọc bảng khung mỗi 0,5 s kèm phụ đề. Tiêu chí: kể ra cả "cười" lẫn "buồn/tiếc" | W2 (dựng) + P/kiểm | PLAN Cổng 6 a |
| 9 | **Mắt cận chính diện**: s22 MCU, s36 MCU, s37 CU, s39 CU, s40 CU. Kiểm lại với mắt v1.5.1 | W1 (s22), W2 | PLAN Cổng 6 c |
| 10 | **Van đồng ở PA1**: Ida nắm van bằng tay MPFB (`reachGrip`), gạt van s40 | W2 | PLAN Cổng 6 b(4) |
| 11 | Sai lệch đã chấp nhận, kiểm lại trên clip: vai áo Cas phồng tròn; tay Cas thô khi nhìn gần (không có shot cận; phát sinh thì sửa riêng shot); mép cổ tay áo Ida răng cưa nhẹ (s41); chân/tay có thể bị chê ở khung tĩnh | W2 (+ W1 phần Ida) | AUTHORSHIP khoá |
| 12 | Tồn đọng từ Cổng 5 (PLAN): B1 cảnh 6 (hướng mặt Ida s45, đồng hồ); G2 mũ s39 → s40; G5/G6 tay s44, s45; G10 Ida xuống thang s40w; G11 s32 → s33 quỳ → đứng; khẩu hình câu cuối L4 s39; nắp đồng hồ | W1/W2 theo shot | PLAN "Việc cho Cổng 6 (từ Cổng 5)" |

## 4. Việc chuyển Cổng 7 (không làm ở Cổng 6)
- **Đèn lồng chiếu sáng xung quanh** (mặt đường, tường, người bên cạnh). Kiểm mù W4T nhắc 3/3 khung.
- **Bóng tiếp đất** dưới chân nhân vật (kiểm mù: "trôi", "dán vào cảnh").
- **Người/bóng X = 2,0** (s32–s34): mỗi người sáng hơn bóng của chính mình trên vách ≥ 2,0 lần luma hiển thị.
- Các mục Cổng 7 sẵn có trong PLAN: G1, G7, G8, G9, G12, G16, G17; phơi sáng s11; màu mũ dưới đèn khí; lấy nét s06, s09w; cửa sổ ấm cho s24c.

## 5. Ước tính token theo gói (từ số đo thật tới nay)
Số công cụ báo là kích thước ngữ cảnh tích luỹ cuối lượt, không phải tiêu thụ thật. Hạn mức gói Claude P không đo được.

| Gói | Căn cứ thật | Ước Cổng 6 | Hạn đề xuất |
|---|---|---|---|
| **W1** | Cổng 5: W1 v2 567–634 nghìn mỗi lượt; W1 v3 689 nghìn (1 lượt, 56 phút) | 1 lượt diễn hoạt khoảng 650–750 nghìn + 1 lượt sửa khoảng 300 nghìn | **khoảng 1,0 triệu** |
| **W2** | Cổng 5: W2 v2 725–770 nghìn mỗi lượt; v3/v4 393 nghìn; v5 419 nghìn | Nhiều việc hơn W1 (PA1, 11 shot cầm nắm, trao đèn, cảnh 6): 2 lượt khoảng 750 nghìn + 1 lượt sửa khoảng 400 nghìn | **khoảng 1,3–1,5 triệu** |
| **P** | Ghép + đóng gói + mặt nạ + luật: khoảng 3 200–3 800 s hàng đợi mỗi vòng; P lượt W4T2 khoảng 285 nghìn, W4T3 khoảng 40 nghìn | 2 vòng ghép và luật, báo cáo | **khoảng 400 nghìn** |
| **Kiểm** | Subagent kiểm mù 45–50 nghìn mỗi khung (đo 30 lần); continuity 221–222 nghìn mỗi lần | Mỗi lần: 10 khung + 2 đối chứng ≈ 12 × 48 nghìn ≈ 580 nghìn (6 + 2 ≈ 390 nghìn). 2 lần (W1, W2) + 1 continuity | **khoảng 1,0–1,4 triệu** |
| **Tổng** | — | — | **khoảng 3,7–4,3 triệu** |

Rủi ro chi phí: một vòng kiểm mù trượt thêm khoảng 0,4–0,6 triệu token; một lượt sửa shot khoảng 0,3–0,4 triệu.

## 6. Điều kiện dừng đề xuất cho mỗi gói
- Hết hạn token → báo cáo phần đã làm.
- Render toàn phim có shot hỏng (thiếu khung, nhân vật xuyên vật lớn) → dừng, sửa trước khi kiểm mù.
- Dò mặc định các shot ngoài phạm vi gói: lệch ≠ 0 px → dừng.
