# CỔNG 6 — THÂN CAS LƯỢT 3 (sửa tham số): ẢNH CHỜ CHỦ DỰ ÁN XEM. CHƯA KHOÁ, CHƯA MERGE

Nhánh `claude/cine-lab-m2-cong5-layout-24o5fp`. Ngày 29/09/2026.
Quyết định gốc: AUTHORSHIP "Cổng 6 — nhân vật" (sửa tham số, không kiểm mù, chủ dự án tự xem ảnh).
Người làm: **P**, trên nhánh P. Không dùng phiên xưởng, vì worktree của phiên xưởng tạo từ `main`.

**Mặc định layout không đổi.** Mọi thay đổi nằm sau cờ thân 'bl' và tay 'bl'.
- Dò s02, s24c, s37, s42, s41, s42a: **18 ảnh nhỏ, lệch 0 px** so với bản lượt 2.
- s41 và s42a được dò riêng vì lượt này có sửa mã hai shot đó.

## 1. Việc đã làm
| Việc | Lượt 2 → lượt 3 | Kết quả tự kiểm |
|---|---|---|
| a. Gấu áo | 2,10 H → **2,17 H** (cách đáy đũng 3,9 cm) | Chân dài ra trong hình bóng: C3 đùi/đầu 1,494 → 1,604 (0°); thân/đầu 2,723 → 2,618. **Không hở da ở eo**, kiểm bằng EEVEE 0°/90°/180° ở s42a (cầm đèn lồng) và s25 60,5 s (tay giơ cao nhất) |
| b. Ống quần | bán kính tối thiểu 4,6 → **5,1 cm** | Chân đọc đầy hơn, vẫn ống thẳng, gấu thẳng |
| c. Tay nắm quai | Treo đèn giữa hai cổ tay → **hai tay nắm hai điểm chéo trên vòng quai**. IK `reachGrip` đặt lòng tay lên ống quai; bộ giải tay MPFB gập ngón quanh ống. s42a: dời đèn cho vòng quai nằm giữa hai nắm tay. s41: đèn vẫn ở tay Ida, Cas nắm hai bên vòng quai từ 0,7 s | Chỉ chạy khi tay 'bl' (`shots_w2.js`: `gripRing`), nên tay cũ không đổi |
| Không đổi | Mặt, đầu, cổ lật, gáy, ngực, lưng, măng sét, da tay | — |

## 2. Ảnh cho chủ dự án xem (`reports/m2/cong6/w4t3/`)
| Ảnh | Nội dung |
|---|---|
| **`W4T3_truoc-sau.jpg`** | Cas toàn thân s42a 114,5 s, lượt 2 và lượt 3 cạnh nhau (3 mẫu, 1920×1080, cắt) |
| `W4T3_cas_eevee_4goc.jpg` | Cas lượt 3, EEVEE 0°/60°/180°/−120°, tư thế sheet |
| `W4T3_hai-nguoi_s42a.jpg` | Khung hai người s42a 114,5 s (MS), 3 mẫu |
| `W4T3_hai-nguoi_WS.jpg` | Khung hai người s41 112,8 s (WS), 3 mẫu |
| `W4T3_can-tay-nam-quai.jpg` | Cận tay nắm quai, cắt từ render 4K: s42a (hai nắm tay trên vòng quai) và s41 (Cas nắm vòng quai khi Ida trao) |

## 3. P tự xem (chưa kiểm mù, theo quyết định)
- **Được:**
  - chân không còn ngắn so với thân;
  - quần ống thẳng và đầy;
  - eo kín ở mọi tư thế đã thử;
  - hai tay nắm quai trên đầu đèn lồng (s42a); tay không còn đặt hai bên quai.
- **Còn có thể bị chê ở khung tĩnh** (sai lệch sẽ ghi khi khoá, theo chỉ thị):
  1. **s41:** Ida chìa đèn khá xa, nên tay Cas **duỗi hết tầm** mới chạm quai (tay đã ngắn theo MPFB). Việc cho W2: đặt Cas gần Ida hơn, hoặc Ida chìa ngắn lại.
  2. **Tay ở khung tĩnh:** khối nắm vẫn to và ít chi tiết khi nhìn từ xa. Mặt trên ngón tay vẫn nhạt dưới ánh trời lạnh.
  3. **Ngay dưới gấu áo** còn bóng tối nhẹ ở đũng quần (s42a, bị đèn lồng rọi từ trên).
  4. **Đế đèn lồng sáng** nằm trước bụng (s42a).

## 4. C3 Cas theo 'doc' (tay MPFB, thân lượt 3; `c3_w4t.py`, làn nặng 166 s)
| Góc | thân | tay trên | cẳng tay | đùi | cẳng chân | đầu doc (px, 4×) | thân so với lượt 2 |
|---|---|---|---|---|---|---|---|
| 0° | 2,618 | 1,564 | 1,051 | 1,604 | 1,464 | 487,0 | −3,9 % |
| 45° | 2,706 | 1,608 | 1,047 | 1,697 | 1,443 | 478,7 | −3,8 % |
| −45° | 2,700 | 1,548 | 1,087 | 1,620 | 1,604 | 479,6 | −3,9 % |
| 90° | 2,723 | —¹ | —¹ | 1,633 | 1,384 | 474,2 | −3,8 % |
| −90° | 2,725 | 1,540 | 1,114 | 1,688 | 1,620 | 474,1 | −3,8 % |
| 135° | 2,803 | 1,554 | 1,132 | 1,672 | 1,599 | 467,8 | −4,4 % |
| −135° | 2,871 | 1,636 | 1,162 | 1,651 | 1,654 | 457,1 | −4,0 % |
| 180° | 3,886 | 2,280 | 1,634 | 2,376 | 2,278 | 328,3 | −3,9 % |

¹ Tay khuất sau thân, ghi null như v1.4.

- Nháp v1.6 mục 6 đã cập nhật: bảng `c3_views` và JSON, gấu 2,17 H, quần 5,1 cm, cách nắm quai.
- Số thô: `W4T3_c3_cas_doc.json`.
- Chỉ số nằm trong ±5 % quanh ngưỡng: không áp dụng, vì đây là số khai mới của v1.6. Luật chưa chạy lần mới nào.

## 5. Token, thời gian, hàng đợi
- **Token:** khoảng **40 nghìn** theo bộ đếm phiên P, từ khi nhận chỉ thị tới khi viết báo cáo (hạn khoảng 80 nghìn).
- **Thời gian:** khoảng 07:30–07:55 UTC.
- **Hàng đợi (gói W4):**
  - 11 việc: 5 nặng, 6 nhanh; chờ 0 s; chạy tổng 525,9 s; 0 lỗi.
  - 2 việc dò (6 shot) chạy 76 s ở làn nhanh, bị gắn QUA-60S.
- **Làm lại:** 0. Dựng thân 1 lượt (2 s); nắm quai 1 lượt.

## 6. Việc đang chờ chủ dự án
1. **Xem ảnh mục 2, duyệt hoặc không duyệt khoá.**
2. Khi duyệt, P sẽ làm một mạch:
   - khoá v1.5.1 (Ida) và v1.6 (Cas) một lần, ghi sai lệch đã chấp nhận: "chân/tay có thể còn bị chê ở khung tĩnh; kiểm lại trên clip W1/W2";
   - đặt mặc định Cas 'bl', thân mới, tay mới;
   - render layout-v16 kèm silhouettes, chạy luật v1.5 (theo dõi s33 P0);
   - merge main, ghi SHA.
