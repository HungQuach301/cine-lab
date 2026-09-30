# BÁO CÁO B3–B4 — cảnh 4 (hướng ánh) + mục treo W2 (30/09/2026)

Nhánh `cong6-b34` (từ main `00a4ead`). Chỉ sửa `design/cong5/layout/shots_w2.js` + `shots/layout/continuity/canh-4.md`, `canh-5.md` + thư mục này. Không sửa `sets_end.js`, mã dùng chung, tài sản khoá, bible, checks. Không làm việc Cổng 7.
Bảng khung 0,5 s trước/sau: `reports/m2/cong6/b34/{s25…s32, s39, s41, s42a, s42b}_{truoc,sau}.jpg` ("trước" từ mp4 v2/v3 đã duyệt v19, "sau" từ mp4 B34).

## 1. B3 — ánh điện cảnh 4 từ mé đối diện
- Cột sân (sets_end `wallPost`) **ẩn ở mọi shot s25–s32** (thân, bóng đèn, quầng, loá). **Chính** PointLight của cột dời tới (7,2; 6,2; 12,2) hệ tường chim — vị trí đã dùng ở s27 v3, mé đường đối diện dãy đèn khí, ngoài khung. Cùng nhịp bật 64,4 s, cùng màu; không thêm nguồn.
- **Chỉ đổi hướng, giữ mức:** nguồn cũ rọi xiên mặt tường (cos ≈ 0,26), nguồn mới gần vuông góc (cos ≈ 0,9) → nếu giữ hệ số 2,7 của s27, tường ở các shot cận sáng hơn ≈ 3,5×. Chọn hệ số **0,85** cho s25, s26, s28–s32 (s27 giữ 2,7 như bản đã duyệt). Đo độ sáng trung bình (luma /255, khung 960×540) cũ → mới: **s28** (68,0 s) nửa trên 137,2 → 143,4; vùng tường phải 150,6 → 145,5; **s32** (79,0 s) nửa trên 147,4 → 150,3; vùng chim 179,8 → 177,2; vùng giữa 152,8 → 160,9 (lệch ≤ 5,3 %).
- Luật chim bóng: nhịp nhạt dần khi điện bật chỉ ở s27 (giữ nguyên hàm switchOn). s32: chim từ đèn lồng ≤ 0,7 m vẫn rõ, tường quanh chim sáng như cũ (±1,5 %) nên tỷ lệ đèn lồng : tràn không đổi đáng kể (không đo lại tỷ lệ 4 : 1 bằng máy — P chạy luật).

## 2. B4 — mục treo W2
| Mục | Nguyên nhân | Sửa | Số đo |
|---|---|---|---|
| **M5** s42b Cas "trong suốt" (≈ 2806–2819) | v2 bật lại quầng sprite của đèn lồng ở 1,9 s → quầng phủ lên Cas ngồi xổm cạnh đèn; thêm: tư thế ôm cũ ép đèn vào ngực (nguồn nằm trong khối thân → mặt trước tối). | Tắt quầng sprite suốt s42b; tư thế ôm mới (dưới). | Bảng `s42b_sau`: Cas đặc, có sáng mặt trước ở 116,0 s; ngồi xổm 117,46 s là bóng dáng tối có đèn trước mặt, không còn trong suốt. |
| **M1** trục s42b | Máy v2 (0,9; 1,25; 8,2) ở phía −x của đường Ida–Cas; s42a/s42 ở phía +x. | Máy (3,6; 1,3; 7,4) → nhìn (−1,1; 1,05; 3,2). Ida vẫn ở miệng vòm (N5). | Ida TRÁI, Cas PHẢI như s42a/s42. |
| **M3** s39 "cuống tay" | Tay trái nắm ống khí dưới van, lộ ở góc dưới-trái khi bà cúi. | Bà buông van suốt vế cuối (tay nghỉ dưới khung CU). | Bảng `s39_sau`: không còn mảng da ở góc khung; chỉ van đồng. |
| **Bắp tay Cas lún vào áo** (s41, s42a, s42b) | `casHug` v2: vai −12°, khép −18°, khuỷu −112° → khuỷu nằm TRONG khối thân. | Vai đưa trước 34°, dang 14°, khuỷu −78°; IK tay vẫn nắm vòng quai. Độ dài xương không đổi (0,1957 / 0,1794 m). | s42a 114,5 s: khuỷu cách trục thân sang bên **1,5–3,2 → 6,0–7,1 cm**, ra trước **−1,0…−1,7 → +8,8 cm**; tâm vòng quai trước cổ **0,187 → 0,270 m**. P chạy C3 lượt Cas. |
| **N7** đèn lồng hông s27, s30 | Móc ở hông TRÁI, máy ở sau-phải → thân bà che. | s27: đèn lùi ra sau 9 cm (vẫn ở hông) → ló khỏi thân; s30: bà đi vào đã cầm đèn tay phải (phía máy), tháo móc ngoài hình. | Bảng `s27_sau`, `s30_sau`: kính đèn sáng thấy từ khung đầu. |

## 3. Lệch 0 px
Gốc probe tạo TRƯỚC khi sửa (`/var/tmp/cine-out/W2/lech4/goc`), so sau (`…/lech4/sau`): s02, s23, s24c + s33, s34, s35, s36, s37, s37b, s37w, s38, s40, s40w, s42, s43, s44, s45, s46, s45c, s47, s48 — **63 ảnh; lệch 0**.

## 4. MP4 mới (`/var/tmp/cine-out/W2/`, 960×540, kèm `timing_*.json`)
| Shot | MP4 |
|---|---|
| s25–s32 (gồm s27) | `video_s25-s26-s27-s28-s29-s30-s31-s32.mp4` (B34, 30/09 ≈ 11:40; thay bản v2 và `video_s27.mp4` v3) |
| s39, s41 | `video_s39-s41.mp4` |
| s42a | `video_s42a-s42b.mp4` (s42b trong tệp này là bản trung gian) |
| s42b | `video_s42b.mp4` (bản cuối, máy nhìn vào giữa vòm) |
Mọi shot khác giữ mp4 đã merge ở main.

## 6. Token, thời gian
- Bộ đếm công cụ ≈ 60 nghìn cho gói B3–B4 (hạn 250 nghìn).
- Thời gian thật 08:13 → ≈ 11:45 UTC 30/09/2026 (≈ 3,5 giờ; phần lớn chờ hàng đợi render dùng chung với phiên W1).

## 5. Rủi ro
- s30: bà cầm đèn tay phải ngay từ đầu (thay nhịp tháo móc ở 0,95 s) — đổi diễn nhỏ; hắt sáng đèn lồng vẫn tăng dần 0,8–1,85 s như cũ.
- s42b: vòm nhìn chéo từ phía +x, bức tường nhà kho chiếm phần phải khung; Cas đi vào sâu nhỏ hơn bản v2.
- s27 và các shot cận cảnh 4 dùng hệ số khác nhau (2,7 / 0,85) cho cùng một nguồn — theo lệnh "giữ mức gần như hiện có"; hiệu chỉnh mức thống nhất là việc Cổng 7.
