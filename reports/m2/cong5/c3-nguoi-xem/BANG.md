# C3 — tờ so sánh cho người xem (Cổng 5 layout, Q-C3r B)

Nguồn: `/var/tmp/cine-out/final/video.mp4` (960×540, 24 fps, 3420 khung; cùng hình với `design/cong5/layout/out/layout.mp4` mà K đã kiểm, lệch trung bình ≈ 1 mã/kênh do nén), mốc shot `/var/tmp/cine-out/final/assemble.json`, mặt nạ + `views` trong `design/cong5/layout/out/layout.parts/` (4×), kết quả luật `reports/checks/layout-cong5/layout.checks.json` (C3: `theo_shot`, `do`, `khong_do_duoc`), `design/cong3/model-sheet/ida.json` → `c3_views`, `costume`, `local_colors`, `bible/characters.md` v1.3, `MS-ida.png`. Không đọc mã trong `checks/`.

## Cách làm (giữ như Cổng 4)

- Mỗi đoạn: chọn khung chia hết cho 12. Ưu tiên khung có mặt nạ đầu lớn nhất; với cận mặt (s22, s37) chọn khung đầu nhỏ hơn để thấy cả mũ và cổ áo.
- Ảnh: trái là khung phim (cắt quanh Ida khi vùng Ida cao dưới 300 px); phải là hình hàng trên của `MS-ida.png` ở góc gần nhất (0° → "Chính diện", ±45° → "3/4", ±90° → "Nghiêng", ≥ 112,5° → "Sau lưng"). Góc âm: lật ngang hình sheet.
- Số đo tay: bề dài theo trục chính PCA của điểm ảnh mặt nạ ≥ 128, +1 px; tỷ lệ = bộ phận / đầu; so với `c3_views` ở góc gần nhất trong 8 góc. Chỉ nêu thân, tay trên, cẳng tay (đùi null, cẳng chân đã bỏ).
- Luật cờ: (a) mắt thấy khác model sheet/bible theo cách người xem nhận ra; hoặc (b) lệch > 10% ở bộ phận không bị che (≤ 10%), không gập (|co ngắn − 1| ≤ 2%), không chạm mép khung; tỷ lệ được hiệu chỉnh theo co ngắn của đầu (`views.head.foreshorten`).
- Số đo chỉ là tham khảo, không phải phán quyết.

## Lưu ý trước khi đọc

1. **`MS-ida.png` vẫn là bản Cổng 3 vòng 1** (chưa có khăn, váy, hoa tai, mặt vẽ tay C′, cổ áo A1 mép cong theo hàm). Khăn, hoa tai, mặt chi tiết, cổ áo A1 trên phim **không** tính là lệch; trang phục và màu được so với bible v1.3 (`ida.json` → `costume`, `local_colors`; mũ #262a33 theo D2).
2. **`khong_do_duoc` lại bị cắt ở 300 mục** (khung cuối 2196). 9 đoạn từ khung 2232 trở đi (s36, s37, s39, s40, s41, s44, s45, s47): cột lý do ghi *"suy từ views"* — tôi áp các tiêu chí máy đã nêu ở phần còn lại lên `parts.json`. Đây không phải lời máy.
3. **Màu mũ dưới đèn khí**: nhóm cờ màu của Cổng 4 (s03, s04, s05, s36, s37, s39) đã được chủ dự án xử lý bằng **D2** (#262a33, chọn không grade — loại D3). Vòng này tôi **không cờ lại** mũ nâu dưới lửa; chỉ nêu ở mục "Để biết" cuối bảng những chỗ mũ đọc nâu cam, sáng hơn áo (vượt mô tả "nâu xám" của D2).
4. Số lệch rất lớn (−35…−61%) ở cận cảnh là do thân bị cắt ở mép khung, không phải lỗi tỷ lệ.

## Bảng (20 đoạn CẦN NGƯỜI XEM)

| Máy | Shot | Khung (đoạn → chọn) | Góc view / elev; tham chiếu | Số đo tay (tỷ lệ/đầu so với `c3_views`) | Lý do máy không đo | Kết luận | Cái thấy |
|---|---|---|---|---|---|---|---|
| 3 | s03 | 204–221 → **216** | 33,6° / −17,6°; c3 45°, sheet "3/4" | thân +12,6%, tay trên −1,4%, cẳng tay +26,5% | thân: gập (foreshorten 1,063); tay trên: gập (0,862); cẳng tay: bị che 55% | không cờ | Bóng đen trước khi thắp đèn; đọc đúng mũ phớt, dáng thẳng, tay giơ sào. Không có bộ phận nào đo được hợp lệ. [3_s03.jpg](3_s03.jpg) |
| 4 | s03 | 222–251 → **228** | 33,6° / −17,7°; c3 45°, sheet "3/4" | thân +7,9%, tay trên −2,4%, cẳng tay +23,5% | thân: gập (1,063); tay trên: gập (0,864); cẳng tay: bị che 55% | không cờ | Đèn vừa thắp: áo đọc xanh vàng, mũ sáng lên dưới lửa (xem "Để biết"); váy, thắt lưng, tay giơ đúng model. [4_s03.jpg](4_s03.jpg) |
| 5 | s04 | 252–287 → **264** | 40,5° / 14,7°; c3 45°, sheet "3/4" | thân +16,5%, tay trên −16,5%, cẳng tay −11,2% (đầu chỉ 12,7 px) | thân: gập (0,918); tay trên: bị che 26%; cẳng tay: bị che 40% | không cờ | Toàn cảnh xa, Ida trên thang cao ≈ 60 px, hình nhoè; không đọc được lệch dáng. [5_s04.jpg](5_s04.jpg) |
| 6 | s05 | 288–383 → **336** | 47,4° / 12,5°; c3 45°, sheet "3/4" | thân −42,5% (cắt mép), tay trên −7,9%, cẳng tay +43,4% | thân: chạm mép; tay trên: gập (0,850); cẳng tay: bị che 54% | không cờ | Cận vai dưới lửa: búi tóc, hoa tai, khăn, cổ áo A1, bàn tay 1,15× đúng bible; mũ đọc nâu (xem "Để biết"). [6_s05.jpg](6_s05.jpg) |
| 9 | s08 | 552–599 → **588** | −11,4° / 1,1°; c3 0°, sheet "Chính diện" | thân +0,0%, tay trên −10,8%, **cẳng tay +19,3%** (+16,2% sau hiệu chỉnh đầu 0,974) | cả 3: đầu cúi/ngẩng (foreshorten 0,974) | **CỜ** (số đo) | Bóng đen trong sương, đọc đúng dáng (mũ, thang, đèn lồng). Cẳng tay không che (0%), không gập (1,011), không chạm mép vẫn dài hơn tham chiếu 0°. Xem mục "Đo lại". [9_s08.jpg](9_s08.jpg), [mặt nạ](matna_s08_588_552.jpg) |
| 15 | s12 | 888–916 → **900** | 108,4° / 24,9°; c3 90°, sheet "Nghiêng" | thân −22,4% (cắt mép), tay trên (90° null), cẳng tay khuất | cả 3: góc nhìn lệch 30,6° > 30° | không cờ | Cận gáy từ sau-bên: búi tóc bạc, lọn tóc, khăn đỏ mận, cổ áo, mũ tối; khớp bible. [15_s12.jpg](15_s12.jpg) |
| 18 | s14 | 996–1043 → **996** | −41,9° / 34,2°; c3 −45°, sheet "3/4" (lật) | đầu chỉ 7 px, co ngắn 0,716 → tỷ lệ vô nghĩa (+456…+490%) | cả 3: góc nhìn lệch 34,3° > 30° | không cờ | Máy nhìn từ trên xuống, mặt bị vành mũ và đèn che; áo xanh, khăn, thang, đèn lồng đúng. [18_s14.jpg](18_s14.jpg) |
| 22 | s21 | 1140–1187 → **1164** | 41,9° / 10,6°; c3 45°, sheet "3/4" | thân −34,9% (cắt mép), tay trên −23,0%, cẳng tay +20,0% | thân: chạm mép; tay trên: bị che 34%; cẳng tay: bị che 19% | không cờ | Cận vai dưới điện: mũ đen xanh (D2 đúng hướng), tóc bạc, hoa tai, khăn, áo xanh sẫm. [22_s21.jpg](22_s21.jpg) |
| 23 | s22 | 1188–1259 → **1188** | −18,1° / 15,2°; c3 0°, sheet "Chính diện" (lật) | thân −61,3% (cắt mép), tay khuất | thân: bị che 37%; tay trên, cẳng tay: bị che 100% | không cờ | Cận mặt chính diện: mắt nâu, hoa tai, cổ áo A1, khăn, mũ đen xanh; khớp bible v1.3. [23_s22.jpg](23_s22.jpg) |
| 28 | s26 | 1488–1535 → **1488** | 34,3° / 14,4°; c3 45°, sheet "3/4" | thân −10,0% (cắt mép), tay trên −5,3%, cẳng tay −36,1% (cắt mép) | thân: chạm mép; tay trên: phối cảnh (depth 1,079); cẳng tay: chạm mép | không cờ | Trung cảnh: mặt sáng, nhận ra Ida (V4 đã sửa), mũ đen, khăn buông trước ngực, hàng cúc, thắt lưng. [28_s26.jpg](28_s26.jpg) |
| 33 | s31 | 1776–1847 → **1800** | 53,0° / 13,2°; c3 45°, sheet "3/4" | thân −48,9% (cắt mép), tay trên −59,8%, cẳng tay khuất | thân: chạm mép; tay trên: phối cảnh (1,066); cẳng tay: bị che 100% | không cờ | Cận mặt 3/4 cạnh Cas: mũ đen xanh, lọn tóc thái dương, hoa tai, cổ áo, khăn; khớp. [33_s31.jpg](33_s31.jpg) |
| 36 | s34 | 2088–2135 → **2088** | 159,3° / 2,3°; c3 180°, sheet "Sau lưng" | thân +36,1% thô; +15,1% sau hiệu chỉnh đầu 0,846; +10,2% nếu trừ thêm độ sâu 1,045. Tay trên −4,4%, cẳng tay khuất | cả 3: đầu cúi/ngẩng (foreshorten 0,846) | không cờ | Sau lưng dưới ánh cam, tay đưa lên mặt. Mặt nạ đầu chỉ là một vệt lưỡi liềm 89 px (mép má lộ giữa búi tóc và bàn tay), không phải chiều dài đầu → số đo thân không dùng được. Bằng mắt: dáng, mũ, váy, xẻ tà đúng. [36_s34.jpg](36_s34.jpg), [mặt nạ](matna_s34_2088.jpg), [đầu](matna_s34_2088_dau.jpg) |
| 38 | s36 | 2232–2279 → **2244** | −24,9° / 9,3°; c3 −45°, sheet "3/4" (lật) | thân −43,2%, tay trên −55,9%, cẳng tay −14,6% | *suy từ views:* thân: che 39%, chạm mép; tay trên: che 46%, gập 0,360, chạm mép; cẳng tay: chạm mép, phối cảnh 0,854 | không cờ | Cận mặt dưới lửa, tay chạm vành mũ: hoa tai, cổ áo A1, khăn đúng; mũ nâu sáng hơn áo (xem "Để biết"). [38_s36.jpg](38_s36.jpg) |
| 39 | s37 | 2280–2418 → **2280** | −24,6° / 16,4°; c3 −45°, sheet "3/4" (lật) | thân, tay: khuất | *suy từ views:* thân, tay trên, cẳng tay: che 100% | không cờ | Cận mặt: lọn tóc bạc, hoa tai, cổ áo, khăn; vành mũ nâu sẫm dưới lửa. [39_s37.jpg](39_s37.jpg) |
| 42 | s39 | 2520–2625 → **2568** | −24,4° / 18,5°; c3 −45°, sheet "3/4" (lật) | thân, tay: khuất | *suy từ views:* che 100% cả 3 | không cờ | Cận mặt buồn: vành mũ tối, hoa tai, cổ áo A1, khăn; khớp. [42_s39.jpg](42_s39.jpg) |
| 43 | s40 | 2626–2687 → **2652** | −6,5° / 22,3°; c3 0°, sheet "Chính diện" (lật) | thân −48,6% (cắt mép), tay khuất | *suy từ views:* thân: chạm mép, gập 0,958, phối cảnh 1,069; tay trên, cẳng tay: che 100% | không cờ | Ida dưới đèn, cúi đầu: mũ đọc nâu trung bình (xem "Để biết"), hoa tai, khăn, cổ áo đúng. [43_s40.jpg](43_s40.jpg) |
| 45 | s41 | 2736–2771 → **2736** | 56,9° / 3,9°; c3 45°, sheet "3/4" | thân −5,8%, tay trên −10,1%, cẳng tay +7,6% | *suy từ views:* đầu bị che 29% (> 10%) → cả 3; tay trên còn bị che 15% | không cờ | Toàn cảnh cạnh Cas: mũ, áo xanh, váy, thang, đèn lồng; tỷ lệ Ida/Cas đúng. [45_s41.jpg](45_s41.jpg) |
| 50 | s44 | 3036–3095 → **3084** | 48,2° / −0,3°; c3 45°, sheet "3/4" | thân +1,2%, tay trên −9,3%, cẳng tay +43,1% | *suy từ views:* đầu cúi/ngẩng 0,865 → cả 3; thân gập 0,979, tay trên gập 0,915, cẳng tay gập 1,037 | không cờ | Toàn thân trong ngõ, ngược sáng, tay giơ chào (cẳng tay giơ lệch trục nên dài): dáng chữ A, mũ, khăn, váy đỏ mận đúng. [50_s44.jpg](50_s44.jpg) |
| 51 | s45 | 3096–3143 → **3096** | 34,5° / 1,0°; c3 45°, sheet "3/4" | thân +6,0% (+2,5% sau hiệu chỉnh đầu 0,967), tay trên −3,0%, cẳng tay +40,8% | *suy từ views:* đầu cúi/ngẩng 0,967 → cả 3; tay trên gập 0,956, cẳng tay gập 0,810 | không cờ | Trung cảnh, đồng hồ trong lòng bàn tay: mũ đen, hoa tai, khăn, hàng cúc, thắt lưng khoá tròn; khớp. [51_s45.jpg](51_s45.jpg) |
| 54 | s47 | 3252–3299 → **3252** | 176,8° / 7,1°; c3 180°, sheet "Sau lưng" | **thân +16,7%** (+13,4% sau hiệu chỉnh đầu 0,972), tay trên +18,0% (gập 0,977), **cẳng tay +16,4%** (+13,1%) | *suy từ views:* đầu cúi/ngẩng 0,972 → cả 3; tay trên gập 0,977 | **CỜ** (số đo, 1/4 khung) | Sau lưng vác thang trong ngõ, đọc đúng dáng; thang dựng gần đứng. Chỉ khung 3252 lệch; 3 khung còn lại trong ±4,1%. Xem mục "Đo lại". [54_s47.jpg](54_s47.jpg), [mặt nạ](matna_s47_3252_3264.jpg) |

## Shot CỜ: chủ dự án xem (3 shot)

- **s08** (máy 9, khung 588): cẳng tay +19,3% (+16,2% sau hiệu chỉnh đầu), lặp lại ở 3/4 khung mẫu. Bóng đen trong sương; mắt không thấy lệch.
- **s47** (máy 54, khung 3252): thân +16,7%, cẳng tay +16,4% ở khung đầu shot; 3 khung sau về trong ±4,1%. Nhiều khả năng do đầu nhìn từ sau chỉ là dải hẹp 29×15 px (bề dài trục chính = bề ngang dải dưới vành mũ), nhưng tôi không chứng minh được.
- **s27** (ngoài danh sách 20, khung 1536–1607): **Ida có trong hình ở cả 6 khung mẫu** (đứng trái khung, cao ≈ 130 px, đèn lồng ở hông) nhưng mặt nạ mọi bộ phận rỗng và `views` ghi hidden = 1. Hệ quả: C3 coi s27 là "không có nhân vật", không đo và cũng không đưa vào CẦN NGƯỜI XEM. Bằng mắt: áo xanh, mũ, dáng thẳng, không thấy lệch model ở cỡ hình này. Cờ vì **thiếu mặt nạ**, không phải vì sai model. [s27_layout_1572.jpg](s27_layout_1572.jpg)

## Đo lại 3 shot bị cờ ở Cổng 4 v2

| Shot | Cổng 4 v2 | Layout Cổng 5 (số đo tay) | Còn cờ? |
|---|---|---|---|
| s08 | cẳng tay +19,1% | Khung 552 / 564 / 576 / 588: cẳng tay +21,5% / +17,5% / +34,4% (gập 0,911, loại) / +19,3%; sau hiệu chỉnh đầu (≈ 0,972–0,974): +18,0% / +14,3% / — / +16,2%. Thân +6,6 / +0,1 / −3,7 / +0,0%. Tay trên −1,4 / −7,1 / −4,7 / −10,8% (gập 0,885). | **Còn cờ**: cẳng tay dài hơn 0° khoảng 14–18%, cả 3 khung hợp lệ. Hình gần như y hệt Cổng 4. |
| s27 | thân −12,3% | **Không đo được.** Mặt nạ rỗng ở cả 6 khung mẫu (1536…1596, 0 điểm ảnh mọi bộ phận), `views` hidden = 1 mọi bộ phận (view 139,6°, elev −1,5°). Video thì có Ida rõ. | **Còn cờ, đổi lý do**: không còn lệch thân để đo; cờ vì mặt nạ thiếu làm C3 bỏ sót shot. Cần xưởng/P xuất lại mặt nạ s27 rồi cho K chạy lại. |
| s47 | thân +16,2%, cẳng tay +17,5% | Khung 3252 / 3264 / 3276 / 3288: thân +16,7 / +2,5 / +2,9 / +4,1%; cẳng tay +16,4 / +3,7 / −9,1% (gập 0,914) / +4,1%; tay trên +18,0 (gập) / +0,2 (gập) / +2,3 / −2,6% (gập). | **Còn cờ, nhẹ**: chỉ khung 3252 vượt 10%; khuyến nghị chủ dự án chấp nhận nếu thấy ảnh đúng dáng. |

Ghi chú s27: chuỗi sáng tối ở khung 1536–1554 (Y trung bình 48 → 117 → 48 → 117 → 67 → 117) là cột điện "nhấp hai lần" theo SHOTLIST, không phải lỗi.

## So sánh với Cổng 4 (`reports/m1/cong4/c3-nguoi-xem/BANG.md`)

- **Hết cờ (6):** s03 (máy 4), s04, s05, s36, s37, s39 — nhóm màu mũ/áo dưới đèn khí; chủ dự án đã quyết D2 (#262a33, không grade), nên vòng này không cờ lại. Hình học các shot này không có số đo hợp lệ vượt 10%.
- **Còn cờ (3):** s08 (như cũ), s47 (nhẹ hơn: 1/4 khung), s27 (đổi lý do: từ "thân −12,3%" sang "mặt nạ rỗng").
- **Cờ mới:** không có ở 20 đoạn máy nêu. s27 là cờ quy trình mới.
- **Đoạn mới vào danh sách CẦN NGƯỜI XEM:** s26 (máy 28), s41 (máy 45), s45 (máy 51) — đều không cờ. **Rời danh sách:** s42a (máy 46, đo được 4/12 mẫu ở layout) và s38 (mặt nạ rỗng; khung 2496, 2508 chỉ thấy mép váy Ida, đúng như Cổng 4 ghi "không có đầu trong hình").
- s34: số đo thân thô tăng từ +13,7% (Cổng 4) lên +36,1% vì mặt nạ đầu co thành vệt nhỏ khi tay che mặt; không cờ (lý do ở bảng).

## Để biết (không cờ): mũ dưới đèn khí

Màu lấy trung vị một dải ngay trên mặt nạ đầu (sRGB video đã grade; độ sáng Rec.709):
- s05 khung 336: mũ ≈ (135,63,28) độ sáng 76, nâu cam; áo trong vùng tối độ sáng 22.
- s36 khung 2244: mũ ≈ (105,40,19) độ sáng 52; áo 38.
- s40 khung 2652: mũ ≈ (83,56,54) độ sáng 62, nâu trung bình dưới đèn trên đầu.
- s03 khung 228 và s37 khung 2280: vành mũ nâu đỏ (độ sáng 48 và 58).

Các chỗ này đọc **nâu cam**, sáng hơn áo, trong khi D2 mô tả "dưới lửa ra nâu xám" và `local_colors` giữ quan hệ "mũ tối nhất". Dưới điện (s21, s22, s26, s31, s39, s45) mũ đọc đen xanh, đúng hướng. LAYOUT-W1 mục 6 đã ghi hiện tượng này là vật lý nguồn hổ phách mạnh. Chủ dự án không cần xem nếu giữ nguyên D2.

## Chỉ số gần ngưỡng (±5%)

- s12 (máy 15): máy nêu góc lệch 30,6° (ngưỡng 30°).
- s26 (máy 28): thân −10,0% (chạm mép, đã loại).
- s41 (máy 45): tay trên −10,1% (bị che 15%, đã loại); khung 2748: −10,3%.
- s08 (máy 9): tay trên −10,8% (gập 0,885, đã loại).
- s34 (máy 36): thân +10,2% sau khi trừ cả co ngắn đầu và độ sâu (số đo không dùng được, xem bảng).
- s47 khung 3276: cẳng tay −9,1% (gập, đã loại).

## Giới hạn

- `MS-ida.png` là bản Cổng 3 vòng 1; so trang phục dựa thêm vào `ida.json` và `bible/characters.md` v1.3.
- Lý do máy cho 9 đoạn từ khung 2232 là suy từ `views`, do danh sách bị cắt ở 300 mục.
- Hiệu chỉnh co ngắn đầu là cách của tôi, máy không dùng.
- Màu đo trên video đã grade, lấy trung vị một dải nhỏ; chỉ để tham khảo.
- s27 chỉ kiểm bằng mắt vì không có mặt nạ.
- Mỗi đoạn chỉ xem kỹ 1 khung (riêng s08, s47, s34, s41 đo mọi khung mẫu); lệch thoáng qua ở khung khác có thể bị bỏ sót.

## Việc đang chờ chủ dự án

1. Xem 3 shot CỜ: s08 và s47 (xác nhận đúng model hay yêu cầu chỉnh tay), s27 (biết rằng C3 chưa kiểm shot này).
2. P/xưởng: xuất lại mặt nạ + `views` cho s27, sau đó K chạy lại C3 (tôi không sửa gì).
3. Tuỳ chọn: xác nhận mũ nâu cam dưới lửa (s05, s36, s40) vẫn nằm trong ý D2.
4. Tuỳ chọn: cập nhật `MS-ida.png` theo bible v1.3 để các vòng sau có hình chuẩn đúng.

## Bổ sung của P (sau khi tờ này nộp) — s27 đã đo được
Nguyên nhân mặt nạ rỗng ở s27: **lỗi bộ xuất mặt nạ của P** (`design/cong5/layout/page.js`, `exportC3`): mọi vật không phải nhân vật được tô đen **hai mặt**; ở s27 máy đặt sau một mặt phẳng một mặt (ảnh render cắt mặt sau nên không thấy), bản tô đen hai mặt che kín Ida. Đã sửa (giữ đúng mặt hiển thị; vật trong suốt không che), xuất lại toàn bộ mặt nạ, phát kiểm toán lần 3 (hạt giống 2226881257325565179, khung 2964, 3276 — ĐẠT, lệch 0).
Luật máy lần 3, s27 (khung 1536–1596): thân **−5,73 %**, cánh tay trên −5,12 %, cẳng tay −5,99 % → "không chứng minh được" (17 mẫu); riêng khung 1536 cẳng tay −11,06 % "trượt chắc chắn" (1 mẫu). So với Cổng 4 v2 (thân −12,3 %): lệch giảm một nửa. **s27 còn cờ nhẹ** (một mẫu cẳng tay −11 % ở khung đầu). Các shot khác không đổi kết quả.
