# CẬP NHẬT NHÁP characters v1.6 — Cas (Cổng 6, gói W4 nhân vật)

Tài liệu này bổ sung `reports/m2/cong5/w4/characters-v1.6-NHAP.md`. Bản nháp đó không bị sửa. Các mục dưới đây vẫn **chưa duyệt**.
Mọi thay đổi chỉ có hiệu lực khi `CAS_STYLE='bl'`, riêng tay khi `HANDS_STYLE='bl'`. Mặc định layout vẫn là Cas v1.4.

| Hạng mục | Nháp v1.6 (gói Cas MPFB) | Cập nhật W4N |
|---|---|---|
| **Cổ áo len** | Cổ tròn rộng, bo len bán kính 0,19 H | **Cổ lật cao**, theo mục 5 của nháp:<br>• ống cổ cao **0,20 H** từ chân cổ;<br>• phần lật gập **0,09 H**;<br>• bán kính ngoài phần lật 0,200 H, tức **Ø 0,40 H**; ống đứng 0,186 H;<br>• mép gập tròn (dày 0,02 H) và mép dưới phần lật (0,009 H);<br>• nếp mềm ở mép lật; cùng màu `C.sweater`, vân len 'rib'.<br>Sau gáy ống cổ dâng thêm tối đa **0,055 H** theo đường gáy.<br>Da CPU: phần trên theo khớp cổ (tối đa 0,85), nên khi cúi hoặc ngửa ống cổ đi theo |
| **Mũ len** | Chóp elip rộng 0,454 × sâu 0,475 H, gấu ngang ở y 0,69. Kiểm mù chê "đậu trên đỉnh như nồi úp" | **Ôm sọ:**<br>• vỏ mũ cách da đầu glb **0,052 H** (một lớp tóc cộng len), chùng thêm 0,03 H ở đỉnh;<br>• **gấu nghiêng**: trước y 0,685 (ngang trên mày), hai bên 0,60 (chạm đỉnh tai), sau 0,515 (phủ chẩm);<br>• gấu lật dày 0,15 H ôm theo mép mũ;<br>• quả bông đặt theo đỉnh mũ đo được.<br>Hình, màu, quả bông giữ theo sheet |
| **Tóc gáy** | Chân tóc sau (θ theo φ): 2,55 / 2,60 rad; sau tai 1,94 / 2,30 | Sau tai **2,15 / 2,45**, gáy **2,75 / 2,85** rad. Tóc phủ kín sau đầu xuống gáy. Mái hạ (φ 0: 1,30 → 1,45) để lộ dưới gấu mũ mới. Màu #5a4034 giữ |
| **Mắt** | Nhãn cầu clearcoat 1,0 | Như Ida v1.5.1:<br>• nướng eye-closure **0,045**, mí trên 0,30 → **0,27 R**;<br>• chân mi trên tối; viền nước mí dưới;<br>• điểm sáng mềm (clearcoat 0,45 / 0,2); bóng mí trên nhãn cầu |
| **Tay** | Tay cast3d cũ (phóng 1,3×) | **Bàn tay MPFB2** (nam 10 tuổi, CC0, W4-MPFB-A3), cờ `HANDS_STYLE='bl'`:<br>• giữ HAND_SCALE 1,3 và khớp cổ tay;<br>• nắm có va chạm (ngón ôm quai đèn lồng, bậc thang);<br>• `thumb_cross` / `spread` cho chim bóng giữ nguyên ánh xạ |
| Cầm đèn lồng (s41, s42a) | Đèn treo giữa hai cổ tay, tay chắp phía trên đèn | Đề xuất cho W2: treo quai đèn vào `ch.gripPoint('R')` (hoặc giữa hai nắm tay) thay cho `hangFromHands` theo cổ tay. Khung `W4N_hai-nguoi.jpg` đã dời đèn đúng như vậy trong trang thử (+5 cm lên, +3 cm ra trước); layout W2 chưa đổi |

## c3_views Cas 'bl' đo lại (hình đổi: mũ ôm sọ, cổ lật cao)
- Cách đo như `b1_measure.py`: mặt nạ 4×, turnaround, trực giao, PCA + 1 px.
- Chạy `c3_cas.py`, làn nặng, 124 s. Số thô: `reports/m2/cong6/w4/W4N_c3_cas_bl.json`.

| Góc | thân / cẳng tay / đùi / cẳng chân | Đầu nhìn thấy (px, 4×) | Thân nháp v1.6 | Lệch thân so với v1.4 |
|---|---|---|---|---|
| 0° | **1,383** / 0,782 / 0,987 / 0,938 | 797 | 1,379 | −17,1 % ² |
| 45° | 1,697 / 0,940 / 1,171 / 1,112 | 673 | 1,711 | −0,6 % |
| −45° | 1,700 / 0,927 / 1,155 / 1,112 | 673 | 1,715 | −0,5 % |
| 90° | 1,787 / —¹ / — / — | 612 | 1,724 | +7,6 % |
| −90° | 1,776 / 1,005 / 1,155 / 1,217 | 614 | 1,732 | +7,4 % |
| 135° | 1,903 / 1,049 / 1,158 / 1,255 | 591 | 1,811 | +11,4 % |
| −135° | 1,891 / 1,035 / 1,320 / 1,245 | 593 | 1,821 | +11,0 % |
| 180° | **1,373** / 0,783 / 0,895 / 0,915 | 798 | 1,370 | −17,1 % ² |

¹ 0,053: mẩu cổ tay ló sau thân; ghi null như v1.4.
² Vẫn lật trục PCA như nháp: đầu nhìn thấy rộng hơn cao vì tai vểnh. Cần P/K quyết cách đo, như đã nêu.

Đọc số:
- Mũ ôm sọ và cổ lật cao làm "đầu nhìn thấy" ở góc nghiêng và sau (±90°, ±135°) **nhỏ lại** (612–593 px, trước 620–603 px). Lý do: gấu mũ thấp hơn và cổ áo che phần dưới. Nên tỷ lệ thân/đầu tăng: ±90° từ +3,8/+4,7 % lên **+7,6/+7,4 %**; ±135° từ +6,0/+6,9 % lên **+11,4/+11,0 %**.
- **Trong ±5 % quanh ngưỡng 3 %:** chỉ còn ±45° (−0,6 / −0,5 %). ±90° đã ra ngoài vùng này (trước ở trong).
- Nếu khoá v1.6 với cổ lật cao và mũ ôm sọ, P phải lấy bảng này làm `c3_views` Cas, không lấy bảng của nháp.
