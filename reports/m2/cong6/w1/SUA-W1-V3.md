# SỬA W1-v3 — Cổng 6, sửa nhỏ sau kiểm mù vòng 2 (30/09/2026)

Phiên P · nhánh `ccr-af7a498d-ss3snk`. Xưởng: `cong6-w1-v3 @08ce93a`, gộp vào nhánh P ở `2ba73f6`. **Chưa merge main; chờ chủ dự án xem và duyệt.**
Căn cứ: chỉ thị chủ dự án "W1 SAU KIỂM MÙ VÒNG 2: PHƯƠNG ÁN A", mục 2 (AUTHORSHIP "Cổng 6 — diễn hoạt"). Không kiểm mù, theo chỉ thị.
Báo cáo xưởng: `BAO-CAO-W1-V3.md`.

## 0. Tóm tắt
| Hạng mục | Kết quả |
|---|---|
| Việc a–e | 4/4 đã sửa. Mặt, ánh sáng, thân Cas không đổi |
| Lệch 0 px (ảnh dò nguồn, 53 shot, 159 ảnh) | **Chỉ 12 ảnh của 4 shot cố ý đổi** (s05, s22, s24, s24c). s23 và **30 shot W2: 0 px** |
| Lệch trên mp4 toàn phim (v21 → v22, PSNR theo khung) | 4 shot đổi: s05 39,4 dB, s24c 34,6, s24 32,6, s22 20,0. **Mọi shot khác ≥ 42,6 dB**, là nhiễu mã hoá (như v19); không có shot nào ngoài ý muốn |
| Luật v22 (LOCK `8d55b6ad…` khớp) | Không lỗi mới ở luật chặn đã đạt. **C3 Cas s24c: không đo được → ĐẠT.** H1b 8 → 9 track không đo được (§3) |
| Clip | **`screening/w1-cong6-v22.mp4`** (s01–s24c, tiếng tạm + phụ đề, 19,3 MB) |
| Bảng trước/sau | `sua-v3/<shot>_truoc.jpg`, `_sau.jpg` (s05, s22, s24, s24c) và 4 ảnh cận `sua-v3/can_*.jpg` |
| Token | Xưởng ≈ 50–59 nghìn (hạn 150 nghìn) |

## 1. Bảng việc
| Mục | Làm gì | Số đo / kiểm của P |
|---|---|---|
| **a. s05 tay "vuốt"** | Tay riêng s05: xoè 0, gập 0,62 (v2: 0,3 / 0,3). Tay nghỉ nắm thân cột thấp, nên ra khỏi khung từ ≈ 2,8 s. Không đụng `S05.hands` của s24 | P xem `can_s05_tay.jpg`: ngón khép, khum, hết "vuốt"; ngón còn hơi dày. ⚠ **Kiểm mù gói THỬ MẶT (dựng trên mã v3) đọc: "Bàn tay biến mất… 3,0–3,5 s… chỉ còn một mẩu nhỏ màu cam lơ lửng"**, tức lúc tay ra khỏi khung bị đọc thành mất hình (§4) |
| **b. s22 mũ, tóc** | Gốc: mũ gắn cứng vào đầu, không trễ. "Lộ tóc/hói" là do đầu ngẩng 14° trước máy thấp. Sửa: `hat_back` −0,35 (vành chúc trước ≈ 5°), ngẩng −8° thay −14°. Không sửa tài sản mũ/tóc | P xem `can_s22_mu-toc.jpg`: vành phủ chân tóc cả lúc ngẩng. ⚠ **Kiểm mù THỬ MẶT vẫn đọc: "mũ như lơ lửng… quá to… trán và đỉnh đầu dưới mũ là da trơn, gần như hói"** (thái dương trơn là thiết kế tóc, §4) |
| **c. s24c quả bông, cổ (K2)** | Đầu cúi nhẹ (cổ +10°) thay ngả vào tường | Quả bông thấy **đủ 36/36 khung** (v2 mất từ khung 1391). Cằm khép lên cổ áo, hết khe. **C3 Cas s24c ĐẠT** (3 mẫu, lệch tối đa 1,25 %). "Dựa tường" nay đọc nhờ lưng và bóng, không còn đầu tựa |
| **d. s24 đếm ba (L4)** | Ba nhịp tách bạch: khép 0,12 s → giữ áp kính 0,12 s → mở 0,18 s; nghỉ ≈ 0,18 s giữa nhịp. Lòng tay nâng ngang lồng kính L11 | Tay trái ở 55,70 / 56,30 / 56,90 s: Δngang 29,6–29,7 px, Δdọc 8,1–8,7 px. Lúc áp, lòng tay cao hơn đáy lồng ≈ 20 px (v2: thấp hơn). P xem `can_s24_ba-nhip.jpg`: tay ở ngang lồng, ba nhịp đọc rõ |
| **e. Không đổi phần khác** | — | 0 px nguồn; PSNR mp4 như §0 |

## 2. Lệch 0 px
- **Nguồn (xưởng):**
  - gốc: ảnh dò v2 (`56b834a`), riêng s24c dò lại từ `f2ec9f3`;
  - sau: mã `1c903b1`. Lượt dò bị dừng khi container khởi động lại, nên đã dò nốt s41–s48 và so gộp bằng cùng phép so;
  - kết quả: 159 ảnh, lệch đúng 12 ảnh của 4 shot cố ý đổi.
- **MP4 toàn phim (P):** so `layout-v21.mp4` và `layout-v22.mp4` bằng PSNR từng khung (log: `/var/tmp/cine-out/psnr_v21_v22.log`).
  - Shot không đổi: thấp nhất 42,6 dB (s29), trung bình 43,6–78,6 dB.
  - Mã hoá x264 khác bit ở mọi khung nên không dùng md5 được; đây là nhiễu đã biết (G3b v19: 41 dB cùng nguồn).

## 3. Luật máy v22 (checks v1.5; P không sửa checks/)
| Luật | v21 | **v22** | Ghi chú |
|---|---|---|---|
| N1, N2, P0, P1, G4, G3, M3, J1, J1b, H1, O3 | ĐẠT | **ĐẠT** | — |
| G3b | TRƯỢT | **TRƯỢT** | σ nhỏ nhất 0,699 (≥ 0,8 ✗); CV 0,181 (≤ 0,2; −9,5 %, ngoài ±5 %). Layout chưa có grain (Cổng 7) |
| H1b | TRƯỢT (8) | **TRƯỢT (9 track không đo được)** | Thay đổi đúng ở shot đã sửa: **s05 `hand_R`** không còn track (tay ra khỏi khung); **s22 `head`** không còn cặp khung đo được. **s24:** `head` khớp 100 → 42,9 % (khung 1354, luồng 5,1 px trong khi đầu khai báo đứng yên; tay nay lướt ngang trước vùng đầu); `hand_R` 100 → 71,4 %; `hand_L` giữ 57,1 %, EPE lớn nhất 11,5 px ở khung 1334 (khai báo 14,3 px, luồng 3,6 px). **P ghi số, không chỉnh để lách.** Luật này đã trượt từ trước; cần K hoặc chủ dự án xem H1b đo vùng đầu khi tay che |
| C3 lượt Ida | 6 · 60 · 48 | **6 · 60 · 48** | Không shot nào đổi. s05, s22, s24 không có mẫu đo được (cỡ/góc), như v21 |
| **C3 lượt Cas** | 4 · 31 · 86 | **7 · 31 · 86** | **s24c: không đo được → ĐẠT** (3 mẫu, lệch tối đa 1,25 %). "Cần người xem" 10 → 9. s23, s24 giữ số v21 (che khuất do tư thế, cỡ nhỏ; xem `SUA-W1-V2.md` §3) |
| Kiểm toán | ĐẠT | **ĐẠT** | Ida: hạt giống 3971412076296412155, khung [636, 1752], bóng [990]. Cas: 3861284491023571045, khung [564] |

**Chỉ số trong ±5 % quanh ngưỡng:**
- C3 hệ số mặt nạ 4 (≤ 4);
- C3 hệ số khi đầu nhỏ 4 (≥ 3,98).

## 4. Điểm chủ dự án nên xem khi duyệt clip
Nguồn: kiểm mù gói THỬ MẶT, dựng trên mã W1-v3. Đây là phát hiện phụ, không phải kiểm mù W1-v3.
1. **s05 (≈ 15,0–15,5 s phim):** tay rời khung ở 2,8 s bị một người xem đọc thành "bàn tay biến mất, còn mẩu cam lơ lửng".
   - Phương án sửa nhỏ: cho tay hạ hẳn ra ngoài khung sớm hơn, trong 2 khung. Hoặc giữ tay nắm cột trong khung tới hết shot.
2. **s22:** mũ và thái dương vẫn bị đọc "lơ lửng / hói". Đặt mũ trong shot đã hết cách. Gốc là thiết kế tóc (thái dương trơn dưới vành), trùng đề xuất (B) của THU-MAT.md §10.
3. **s24c:** Cas cúi nhẹ thay vì tựa đầu vào tường; chủ dự án xem "dựa tường" còn đọc được không.
4. **Continuity chưa giao** (từ `SUA-W1-V2.md` §7): K1, K3 ở s06; K4/L7 tay s24c; K6 tài liệu; K7 cỡ s22.

## 5. Token và thời gian (số công cụ báo)
| Việc | Token | Thời gian (UTC 30/09/2026) |
|---|---|---|
| Xưởng W1-v3 | ≈ 50 nghìn theo xưởng tự đếm; ≈ 59 nghìn theo chênh lệch bộ đếm của harness (hạn 150 nghìn) | 16:41 → 17:50 (có 1 lần container khởi động lại) |
| Pipeline v22 (ghép → C3 Cas) | — (máy) | 17:56 → 19:37 (mặt nạ Ida 1 657 s, luật 441 s, C3 Cas 1 338 s + luật 241 s) |
| Cộng dồn W1 (v1 + v2 + v3, bộ đếm harness) | ≈ 714 nghìn | — |
