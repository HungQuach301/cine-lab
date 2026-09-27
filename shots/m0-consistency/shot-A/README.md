# SHOT A — M0-W-CONS-A (thử nhất quán nhân vật, Cổng 0)

Toàn cảnh 1920×1080, nhân vật thắp đèn nhìn nghiêng quay sang phải, đang bước đi, tay gần máy quay cầm sào chếch lên; nền trời chạng vạng và dải nhà xa. Phong cách 2D vector phẳng, dựng bằng Python + Pillow (đa mẫu phụ).

## Lệnh chạy lại

Chạy từ gốc repo (hoặc worktree):

```
/opt/cine/bin/python shots/m0-consistency/shot-A/render.py
```

Tuỳ chọn thêm: `--sheet /đường/dẫn/model-sheet.json` và `--out <thư mục>`. Nếu không truyền `--sheet`, script tìm `reports/m0/consistency/model-sheet.json` lần lượt ở gốc worktree hiện tại, rồi ở gốc checkout chính (thư mục cha của `git-common-dir`). Lúc dựng, file này chưa có trong commit nên script dùng bản ở checkout chính:
`/home/user/cine-lab/reports/m0/consistency/model-sheet.json` (sha256 `d097fae9604f68bbc766d377a4dcf9144417c80a82f4e30ef17c154c0007fa20`).

Đầu ra:
- `frame.png`: khung hình 1920×1080.
- `masks/{head,torso,upper_arm,forearm,thigh,shin}.png`: 1920×1080, trắng (255) trên nền đen (0), ảnh nhị phân. Mỗi file chỉ có một bộ phận, dùng cùng phép biến đổi và tư thế như `frame.png`, không bị bộ phận nào che. Tay và chân lấy bên **gần máy quay**.
- `render-meta.json`: số px của 1 H, gốc toạ độ, tư thế, hệ số đa mẫu phụ.

## Tỷ lệ

- **1 H = 320 / total_height_H = 320 / 5.60 = 57.142857 px.** Chiều cao mục tiêu 320 px là số của đề bài; còn 5.60 đọc từ `total_height_H` trong model sheet.
- Mọi độ dài và độ rộng bộ phận (head, hat, neck, torso với top_width và bottom_width, upper_arm, forearm, hand, thigh, shin, foot, pole) và `joints.shoulder_from_torso_top` đều đọc từ model sheet rồi nhân với H_px. Trong mã không có số gõ tay nào cho kích thước bộ phận.
- Số gõ tay chỉ gồm góc tư thế, vị trí trong khung, nền, và ba tham số hình dáng của mũ mà model sheet không định nghĩa (xem mục dưới).
- Màu các bộ phận lấy từ `color` trong sheet. Bộ phận phía xa máy quay được tối đi 28% để tách lớp. `id_color` không được dùng, vì mặt nạ vẽ trắng trên đen theo yêu cầu gói việc.
- Mặt nạ được rasterize ở 8× rồi thu nhỏ theo trung bình vùng và cắt ngưỡng 50%, nên biên sai khoảng dưới nửa pixel. `frame.png` dựng ở 4× rồi thu nhỏ bằng LANCZOS.

## Cách diễn giải chỗ model sheet mơ hồ

1. **Độ dài chi "từ khớp gốc đến đầu mút".** Mỗi chi (upper_arm, forearm, thigh, shin) có đầu gốc phẳng nằm đúng tại khớp gốc, thân thẳng rộng `width`, và đầu mút là nửa hình tròn đường kính `width`. **Phần bo tròn tính vào độ dài**, tức là từ khớp gốc tới điểm xa nhất của chóp đúng bằng `length`. Vì thế mặt nạ đo dọc trục phải cho đúng `length`.
2. **Vị trí khớp kế tiếp.** Khuỷu và gối đặt tại **tâm nửa tròn đầu mút** của đoạn trước, tức ở `length − width/2` dọc trục, không đặt tại chóp. Nhờ vậy đầu gốc phẳng của đoạn sau (hẹp hơn) luôn nằm lọt trong nửa tròn của đoạn trước ở mọi góc gập, và không hở khớp. Hệ quả: khoảng cách khớp–khớp ngắn hơn `length` một lượng `width/2`. Tổng chiều cao khi đứng thẳng vì thế thấp hơn 5.60 H khoảng 0.33 H (0.18 ở gối, 0.15 ở cổ chân). Tôi vẫn lấy 5.60 để quy đổi H_px, vì đề bài chỉ yêu cầu "khoảng 320 px" và chỉ số được kiểm là tỷ lệ bộ phận chứ không phải tổng chiều cao.
3. **Đầu.** Là ellipse có trục đứng; `length` = 1.00 H là chiều cao ellipse (tính cả hai cực), `width` = 0.86 H. Đầu thẳng đứng, không nghiêng, để trục đo trùng với trục dọc. Mắt và tai vẽ bên trong ellipse, không làm đổi đường viền. Không vẽ mũi nhô ra, để hình bóng đầu đúng là ellipse như sheet.
4. **Cổ.** Là hình chữ nhật `neck.width` × `neck.length` đứng trên đỉnh thân (`neck_on_torso_top`); đáy ellipse đầu chạm đỉnh cổ. Cổ lấn xuống thân 0.05 H chỉ để che khe răng cưa; phần này bị thân che nên không đổi hình học nhìn thấy.
5. **Mũ.** `hat.length` = 0.55 H là tổng chiều cao vành cộng chóp; `hat.width` = 1.30 H là bề ngang vành. Sheet không định nghĩa ba điều sau, nên tôi tự quyết:
   - Độ dày vành = 18% của `hat.length`.
   - Bề ngang chóp = 90% của `head.width`.
   - Mũ **lún xuống đầu**: đáy vành nằm dưới đỉnh đầu 0.15 × `head.length`.
   Vì vậy trong `frame.png` mũ che phần đỉnh đầu, nhưng `masks/head.png` vẫn là ellipse đầy đủ, không bị che. Mũ không tính vào `total_height_H` (theo `_total_check`).
6. **Thân.** Là hình thang đứng thẳng, cao `torso.length`, cạnh trên `top_width` 0.90, cạnh dưới `bottom_width` 1.30. Trường `width` 1.10 được coi là bề ngang trung bình và không dùng trực tiếp. Tôi dựng thân như hình thang cân nhìn nghiêng, tâm trùng trục thân. Đây là diễn giải đáng chú ý: ở góc nhìn nghiêng, thân người thật sẽ hẹp hơn, nhưng sheet chỉ có một bộ số nên tôi dùng nguyên.
7. **Khớp vai.** Nằm trên trục giữa thân, dưới đỉnh thân `shoulder_from_torso_top` = 0.12 H. **Khớp hông** nằm tại tâm cạnh đáy thân (`hip_at_torso_bottom`). Hai chân cùng xuất phát từ một điểm hông vì là góc nhìn nghiêng.
8. **Bàn tay.** Là hình tròn đường kính 0.26 H, **tâm đặt tại chóp cẳng tay** (điểm cách khuỷu đúng `forearm.length`), nên nửa bàn tay chồng lên đầu mút cẳng tay. Bàn tay không nằm trong mặt nạ forearm.
9. **Bàn chân.** Là chữ nhật bo góc dài `foot.length`, dày `foot.width`. Mép trên đi qua cổ chân, gót lùi sau cổ chân một bán kính ống chân. Chân sau ở tư thế nhón (bàn chân nghiêng 28°). Toàn nhân vật được hạ sao cho điểm thấp nhất của hai bàn chân chạm mặt vỉa hè (y = 738).
10. **Sào.** Dài `pole.length` 3.20 H, rộng 0.07 H, nghiêng 58° so với phương ngang, đi qua tâm bàn tay gần máy quay; tay nắm ở 30% chiều dài tính từ đầu dưới. Móc đèn và ngọn lửa ở đầu sào là chi tiết trang trí, sheet không có kích thước cho chúng.
11. **Bên gần và bên xa máy quay.** Tay gần máy quay là tay cầm sào (giơ về trước và lên); tay xa vung ra sau. Chân gần máy quay bước về trước; chân xa ở sau. Mặt nạ tay và chân là của bên gần. Lưu ý: tay gần và chân gần cùng ở phía trước, không đối xứng chéo như dáng đi tự nhiên, vì tay cầm sào không vung theo nhịp bước. Đây là lựa chọn dàn dựng, không ảnh hưởng tỷ lệ.
12. **Thứ tự lớp trong frame.** Tay xa, chân xa, chân gần, cổ, thân, đầu, mũ, sào, tay gần. Chân nằm sau thân, nên phần gốc đùi bị mép dưới thân che trong `frame.png`, nhưng mặt nạ `thigh` vẫn đầy đủ.

## Tư thế (góc, độ; 0 = hướng phải, 90 = thẳng xuống)

| Bộ phận | Đùi / cánh tay trên | Ống chân / cẳng tay | Bàn chân |
|---|---|---|---|
| Chân gần (trước) | 68 | 82 | −2 |
| Chân xa (sau) | 110 | 128 | 28 |
| Tay gần (cầm sào) | 52 | −18 | – |
| Tay xa (vung sau) | 120 | 108 | – |

## Quyền tài sản

Không dùng tài sản ngoài nào: không có font, ảnh, nhạc hay tham chiếu. Mọi hình đều sinh bằng mã trong `render.py`, nền dựng theo thủ tục với seed cố định. Vì vậy không có mục mới nào cần thêm vào `RIGHTS.md`.
