# BÁO CÁO W2 — Cổng 6, DIỄN HOẠT cảnh 4–6, VÒNG 2 (vòng cuối)

Phiên xưởng W2 · nhánh `cong6-w2-v2` (từ `cong6-w2-v1` @3dc9148) · 29–30/09/2026.
Căn cứ: kết quả P trên layout-v17 (kiểm mù 10 dải, continuity, luật v1.5 C3 lượt Cas), quyết định chủ dự án 30/09 (Đ3 duyệt, Đ6 xác nhận → N4 là việc W2, Đ4 = gập nắp ngoài hình, Đ5 không làm).
Phạm vi: chỉ `shots_w2.js` (+ tài liệu layout/continuity/manifest). Không sửa bible, checks, tài sản khoá, mã dùng chung, và không đọc `checks/`.
Lệch 0 px ngoài phạm vi (s02, s24c): **6 ảnh; lệch 0**. Tổng phim **140,5 s** (không đổi thời lượng shot nào).

## 1. Bảng việc — A (kiểm mù)
| Mục | Trạng thái | Nguyên nhân đo được | Sửa (trong phạm vi W2) |
|---|---|---|---|
| **A1** s32, s34 "mặt nạ" | Đã làm | Khung 1920: **s34** — "mảng trắng không chi tiết" là **búi tóc** trắng (bà quay lưng máy, mặt khuất), không phải mặt. **s32** — mặt nghiêng rất nhỏ, xám phẳng dưới trắng tràn, mắt trong bóng vành mũ, mặt không biểu cảm. | s34: bà nhìn bóng mình rồi quay đầu 58° + thân 8° về phía Cas (0,3–1,2 s) → mặt nghiêng thấy được, búi lui ra sau; cười nhẹ, chớp. s32: bà ngẩng nhìn chim (cổ thêm 12°), mắt ngước 0,12 rad, cười nhẹ kinh ngạc, chớp 77,45 / 79,3. Thử facelight 'lantern' ở s32: đèn dội rọi cả tường sau đầu bà thành vầng sáng lạ → **bỏ** (không thêm ánh không có nguồn trên hình). "Đàn ông lớn tuổi" ở WS: do trang phục/tóc (tài sản khoá) — ghi nhận, không sửa. |
| **A2** s37 cười buồn nhịp 1 | Đã làm | Mặt nhỏ (MS 50 mm, 1,35 m, ≈ 60 px), EK 2,2 tối; 95,75 có **chớp chậm ×2,2** + cúi 6° → khung ≈ 96,0 mắt nhắm, mặt quay khỏi lửa. | MCU 60 mm, 1,30 m, EK 2,8, ngọn lửa vẫn trong khung; nụ cười rõ hơn (smile 1,0, jawOpen 0,07 — thấy mép răng như preset sad_smile; lidDrop 0,38 → 0,32); bỏ chớp chậm, thay chớp thường 95,55 + chớp 96,25 (×1,3); cúi 6° → 3°; khẩu hình ×0,9. Bảng khung `bang-khung_s37_v2.jpg`: 95,5–96,4 cười + mắt cụp đọc rõ, mặt sáng. |
| **A3** mặt/dáng tĩnh | Đã làm | s39: biên độ khẩu hình 0,7 quá nhỏ ở CU nghiêng; s41, s42a: `settle` biên độ nhỏ, không hành động phụ. | s39 khẩu hình ×1,15 (mặc định PA1 0,7 → 0,85); s41: bà nghiêng người theo đèn, gật khi buông; Cas cúi nhìn đèn trong tay (1,0 s) rồi ngẩng nhìn bà (1,45 s); dồn chân ×1,3; s42a: bà nghiêng đầu dịu (7°), gật nhẹ khi cậu quay nhìn, tay phải đưa về phía cậu, thở rõ (×1,6), cười nhẹ, chớp 113,95 / 115,05; cổ 26°, nhãn cầu 0,14 rad xuống — ánh mắt vào cậu. |
| **A4** bàn tay | Đã làm (s45, s37/s37b, s40); s39 một phần | s45: tay trái IK đỡ dưới đồng hồ → hai tay chồng, ngón xoắn/xuyên. s37b/s39: tay nắm sát dưới van nằm ở mép khung CU. s40: tay theo cần sau khi gạt → cổ tay vặn. | s45: tay trái thả lỏng bên hông; đồng hồ nằm trong lòng tay phải. PA1: nắm ống khí thấp hơn (0,045 → 0,12 m dưới tâm van) → tay ra khỏi khung s37b; s39 máy hạ 0,12 → 0,03 m; s40 buông cần sau khi gạt (từ v1). **s39 còn mảng da ở góc dưới-trái 101,6–103,6 s** (đầu ngón tay khi bà cúi). |
| **A5** giật | Đã làm | s45 quay 50° trong 0,8 s (easeIO); s42b easeIO từ (1,9; 5,3) — đỉnh ≈ 4 m/s; s37b cúi 7° trong 0,4 s; s41 đèn riêng chép **tỉ lệ thế giới** của đèn trong tay bà → co nhỏ. | s45 quay 0,9–1,95 s, cổ 42°; s42b đi đều 1,6 m/s từ (0,7; 4,4); s37b cúi 0 → 6° trong 0,75 s; s41 đèn tỉ lệ 1. **Chưa sửa:** vòng tối đồng tâm trên vách hốc và Cas "trong suốt" ở s42b 1,5 s — do bóng/đèn spot của bộ hốc (`s5.js`, ngoài phạm vi) khi đèn lồng áp sát vách; đề xuất Cổng 7. |

## 2. Bảng việc — N (continuity)
| Mục | Trạng thái | Số đo trước → sau |
|---|---|---|
| **N1** s40 (chặn) | Đã làm | Quay mặt đi 108,75 → 109,20 (cúi 30°, quay 72°) → **109,08 → 109,32** (cúi 16°, quay 80°, thân 16°). Trên mp4: khung 2619 (109,125) còn mặt nghiêng, 2620 (109,17) còn mép má, **2621 (109,21) = lửa tắt + kính tối, mặt khuất**. Cúi giảm để mũ không "lơ lửng". |
| **N2** s40w → s41 | Đã làm | Cuối s40w: Cas buông thang 1,55–1,85 s, bước 0,26 m tới `CAS_41` (8,50; −4,85), quay về bà; bà ở `IDA_41` (7,95; −5,00) cầm đèn tay phải nhấc về phía cậu (`IDA_LIFT`) = tư thế mở s41 (hai shot cùng vị trí, hướng, đèn). |
| **N3** s40w xuống thang | Đã làm | Đảo nhịp trèo (tay −120°, thân đổ) → **4 bậc × 0,3 s** (75 % đi, 25 % dừng), thân thẳng nghiêng vào thang 5°, chân so le; tay nắm hai thanh (IK) khi gốc < 0,9 m. Không chồng lên Cas (cậu đứng cạnh phía đông). |
| **N4** s39 ↔ s38 nhìn nhau (Đ6) | Đã làm | s39: cổ quay 25° → 52° về phía Cas (phía máy), cúi 24°, mắt liếc phải-xuống (+0,15; +0,10 rad); máy vẫn tính từ tư thế gốc cũ → mặt còn cách chính diện ≈ 69°. s38: Cas quay đầu 24° + ngửa 46° về phía bà. |
| **N5** s42b → s42 | Đã làm | Ida đứng ở miệng vòm (1,25; 5,25) **trong khung s42b**, dõi theo cậu; + Đ3 (mục 4). |
| **N6** s33 đứng dậy | Đã làm | v1 lerp `crouch_lantern` không hạ gốc (đỉnh mũ đứng yên) → `kneelOf` (root_y_m) → đứng dậy 0–0,7 s thấy được; đi từ 0,7 s. |
| **N7** đèn lồng hông s27, s30 | Đã làm | Kính + lửa đạo cụ tự sáng (cùng vật liệu đèn lồng Cas) ở s25–s32; mức hắt lên tường/nền không đổi. |
| **N8** s37b tay mép khung | Đã làm | Nắm thấp 0,12 m dưới van → tay ra khỏi khung CU (bảng khung `s37b_v2`). |
| **N9** s47 thang | Đã làm | Giữ góc 28° của sheet, xoay chéo ra ngoài vai phải 0,5 rad → từ sau lưng đọc là thang vác chéo bên phải bà, không cắt qua mũ/gáy (thử máy lệch trái: vách ngõ chắn nửa khung → bỏ). |
| **N10** s45 đồng hồ | Đã làm | Đồng hồ trong lòng tay phải, mặt số ngửa về mắt bà, thấy từ khung đầu; tay trái không che. |
| **N14** tài liệu s40 | Đã làm | canh-5.md, shots_w2.json ghi số thật (v1 và v2). |

## 3. C — C3 lượt Cas (s42a, s42b, s35)
- Đo độ dài xương thế giới của Cas ở s42a **sau IK**, mỗi 12 khung: vai → khuỷu **0,1957 m**, khuỷu → cổ tay **0,1794 m** (hai tay) = đúng cas.json (0,764 H × 0,256 = 0,19566 m; 0,701 H × 0,256 = 0,17943 m) và `cas_body_bl.json` (mpfb_m forearm 0,1794). IK (reachGrip/gripAt) **chỉ xoay khớp**, không đổi độ dài, không kéo lưới tay MPFB.
- Vậy cánh tay trên ngắn đi trên mặt nạ (s42a −38,6 %, s42b −30,3 %) là **co ngắn phối cảnh**: ở s42a/s42b cậu ôm đèn, cánh tay trên gần như chĩa về phía máy (máy 3/4 trước ở s42a; ngoài vòm ở s42b); s35 đùi −21,2 % là bước chạy. **Không chỉnh tư thế để lách luật.** P chuyển số đo này cho K (khiếu nại cách đo C3 ở tư thế co ngắn).

## 4. Đ3 (chủ dự án duyệt) — đèn lồng 0,55 → 0,38 m trước mặt Cas (s42b, s42)
| | Lòng tay → mặt kính (FK) | Sau IK ở đỉnh nhịp đếm |
|---|---|---|
| v1 (0,55 m) | 0,350–0,371 m | 0,182–0,190 m |
| v2 (0,38 m) | 0,377–0,383 m | 0,134–0,142 m (tầm với chạm giới hạn) |
| **v2 + cúi người theo nhịp** (thân 26° → 56°, cổ −38° ở đỉnh nhịp) | 0,172–0,217 m | **0,026–0,034 m** |
Mục tiêu 0,015 m (áp sát); đạt 2,6–3,4 cm — tay "hơ" sát kính. Không duỗi thêm (khuỷu đã thẳng giới hạn IK).

## 5. Không làm (theo lệnh)
Đ4 (nắp đồng hồ — chủ dự án chọn gập ngoài hình), Đ5 (nước mắt); việc Cổng 7: s40 cảnh không tối khi đèn tắt, đèn lồng không hắt sáng quanh, tóc/búi như mũ len, da "đất sét". Vòng tối đồng tâm s42b → đề xuất Cổng 7.

## 6. Render hiện hành (`/var/tmp/cine-out/W2/`, 960×540, không tiếng — mp4 lẻ mới hơn thắng)
Xem mục 9 (điền sau khi render xong).

## 7. Bảng khung 0,5 s (vòng 2)
`reports/m2/cong6/w2/bang-khung_{s32,s34,s37,s37b,s38,s39,s40,s40w,s41,s42,s42a,s42b,s45}_v2.jpg`.

## 8. Rủi ro
- s39 góc dưới-trái còn đầu ngón tay (101,6–103,6 s) khi bà cúi.
- s34 mặt bà vẫn nhỏ (WS 26 mm, ≈ 40 px ở 1920): hết "mảng trắng" nhưng chưa chắc hết "mặt nạ" ở kiểm mù.
- s42 dáng cúi 56° nhìn từ sau lưng có thể đọc là "khom" hơn là "hơ tay".
- Render chậm do IK (s41 ≈ 20 s/khung).
- Container khởi động lại hai lần trong vòng 2 (render nhóm bị ngắt) — đã render lại.

## 9. Token, thời gian
(điền khi nộp)
