# Cổng 3 vòng 2 — Cách (2): nhân vật tranh 2D có khung xương, nhận ánh sáng thật của cảnh

Module: `cast2d.js` (API giống `shared/cast.js`: `buildCharacter(sheet, opts)` + `update(ch, camera)`).
File phụ: `paint2d.js` (bộ vẽ tranh bằng mã), `designs.js` (thiết kế Ida, Cas).
Công cụ gỡ lỗi (không dùng khi render phim): `dbg_sheet.js` (bày tranh đầu/thân ở nhiều góc), `dbg_page.js` (bản sao `v2/page.js` có thêm cờ ẩn lớp, đặt máy quay).
Ảnh thử 960×540, 8 mẫu: `test/a_close_ida.png`, `test/b_cas_bird.png`, `test/c_s5_wide.png`, `test/walk_000.png`, `test/walk_048.png`, `test/walk_095.png`.

Không sửa `shared/`, `v2/*.js`, `model-sheet/`, `bible/`, `checks/`. Không dùng mạng, không tài sản ngoài: mọi tranh sinh bằng mã (canvas và mảng điểm ảnh).

## 1. Cách làm

1. **Khung xương, tư thế, đạo cụ** lấy thẳng từ `shared/cast.js`: cùng tên khớp, cùng `applyPose`, cùng đạo cụ. **Độ dài các bộ phận đo C3 (head, torso, upper_arm, forearm, thigh, shin) không đổi.** Module đã nhận bản sửa dấu `spread` của P mà không phải sửa gì, vì chỉ ghi đè độ gập ngón (`rotation.z`) chứ không ghi đè độ xoè.
2. **Thân 3D gốc giữ làm vật đổ bóng vô hình.** Vật liệu `colorWrite:false, depthWrite:false` nên không hiện trong hình nhưng vẫn đổ bóng, và vẫn có mặt trong G-buffer của lớp vẽ C. Nhờ vậy bóng người trên tường và nền luôn đúng hình dù lớp tranh quay về máy. Tôi thêm vật đổ bóng cho các chi tiết mới để bóng khớp với tranh: váy (nón cụt), khăn choàng, búi to, ngón 3 đốt, quả bông xù gai sợi, tai vểnh của Cas.
3. **Lớp tranh** (lưới động, dựng lại trong `update()` trước **mỗi mẫu**):
   - **Đầu và thân: tranh theo góc nhìn.**
     - Khối được phác bằng các elip, có mặt phẳng cắt và hợp mềm trong nhóm. Một bộ rasterize trực giao trên CPU vẽ tranh cho đúng góc nhìn, bước 4° ngang và 6° dọc, và lưu đệm tối đa 18 tranh cho mỗi lớp.
     - Màu là trường màu theo vị trí 3D: vùng màu kiểu họa sĩ (trán vàng, má–mũi–tai đỏ, hàm lạnh) cộng nét cọ neo vào khối.
     - Nét mặt (mắt, mí, mi, mày, nếp nhăn, môi, tai, hoa tai, nơ mũ, tóc mai) vẽ bằng canvas 2D qua phép chiếu affine của khung tiếp tuyến tại điểm neo, nên nét co theo góc quay. Mỗi điểm ảnh của nét được kiểm độ sâu, nên mắt xa bị sống mũi che đúng.
     - Chọn tranh **gần nhất, có trễ**, không trộn hai tranh: máy tĩnh (kể cả rung khẩu độ DOF) dùng đúng một tranh, không nhoè đôi.
   - **Tay, chân, cổ, lòng/mu bàn tay, ngón, ủng, vạt áo + váy: dải tranh.** Mỗi dải chạy liền dọc chuỗi khớp (vai → khuỷu → cổ tay, hông → gối → cổ chân), nên không hở khớp. Bề rộng lấy từ mặt cắt elip của bộ phận chiếu theo hướng nhìn. Vạt áo và váy của Ida ôm theo hai chân khi bước. Lòng hay mu bàn tay được chọn theo phía nhìn.
4. **Ánh sáng.** Mọi lớp dùng `opts.material(...)` của cảnh (kể cả vá shader dội vách của `s5.js`, vá của tôi được nối sau) cộng `normalMap` suy từ bản đồ độ cao vẽ kèm. Đèn khí, đèn lồng, ánh điện, viền dội chiếu lên tranh như lên khối.
5. **Độ sâu từng điểm ảnh.** Kênh alpha của normalMap là độ nhô, và shader ghi `gl_FragDepth` bằng mặt thẻ cộng độ nhô, nên các lớp cắt nhau như khối (tay trước hay sau thân đúng chỗ).
6. **Rìa mềm.** Ngưỡng alpha đổi theo từng mẫu (0,3–0,7). Sau tích luỹ 8 mẫu, rìa mềm theo dốc alpha đã vẽ. Mép tranh tối nhẹ ("mép quay đi") để khối tròn cả khi ánh sáng phẳng.

## 2. Đã thêm (chi tiết thứ cấp, để sửa lỗi đọc giới tính và tuổi) — **chờ chủ dự án duyệt**

- **Ida (74, nữ).**
  - Búi tóc to, xoắn lọn, đặt thấp dưới vành mũ. Tóc xám chải ngược, hai lượn tóc che thái dương và nửa trên tai làm khung mặt.
  - Mặt: hàm thon, cằm nhỏ, mí sụp, bọng mắt, vết chân chim, rãnh mũi–má, nếp trán, môi mỏng hồng phai, vài sợi mi. Đồi mồi nhạt.
  - Hoa tai ngọc nhỏ, **nơ vải nhỏ trên băng mũ phớt**. Mũ, vành, chóp giữ đúng số đo đã duyệt; nơ là chi tiết mới, xin duyệt riêng.
  - Khăn choàng len thắt nút trước ngực, có tua. Vòng khăn quấn cổ và cổ áo đứng 0,35 H (theo model sheet) để che cổ dài của khung xương.
  - Váy dài màu mận xám lộ dưới gấu áo tới gần mắt cá.
- **Cas (10, nam).**
  - Tóc ngắn lởm chởm lộ ở gáy và thái dương, tai vểnh to, má tròn ửng lạnh, tàn nhang, mắt to.
  - Mũ len kem có gờ gấp và gân đan. Quả bông len đỏ, xù sợi, đặt cao và tách khỏi chỏm, vật đổ bóng cũng có gai sợi.
  - Áo len quá khổ có bo cổ, bo gấu, bo tay trùm qua cổ tay, và một miếng vá mạng ở ngực. Quần hụt lộ cổ chân.

## 3. Bàn tay — **có phóng to, chờ duyệt**

- **Cas 1,30×** (đúng **trần** cho phép; nêu tên vì nằm trong ±5% quanh ngưỡng). **Ida 1,15×.** Chỉ phóng to bàn tay và ngón, không đổi chiều dài cẳng tay.
- Ngón có 3 đốt (tổng độ gập như bản gốc nhưng chia cho 3 đốt, nên cong mềm), ngón cái 2 đốt. Tranh lòng bàn tay có đường chỉ tay; mu bàn tay có gân, khớp và móng. Ngón thuôn, đầu tròn.
- **`thumb_cross` (chim bóng):** hai ngón cái nghiêng vào giữa khoảng 35°, đốt ngoài hơi quặp, để đầu hai ngón chạm nhau thành **một** đầu chim có mỏ. Các ngón xoè làm lông cánh. Đây là cách diễn giải khớp ngón (không thuộc khung đo C3); tư thế JSON và mọi khớp khác giữ nguyên. P nên xem bóng trong `test/b_cas_bird.png`: vòng 1 hai ngón cái đứng tách như hai sừng.

## 4. Tự phê bình thẳng thắn

- **Còn "ma-nơ-canh" ở thân và chi.**
  - Tay áo, ống chân là dải trơn đều. Nếp vải chỉ là nhiễu và vài nếp ở khuỷu, chưa có nếp gãy lớn hay vạt áo bay.
  - Thân áo Ida vẫn là khối elip ghép, gọn gàng quá.
  - Vạt áo theo chân nhưng không có quán tính.
- **Lệch chất tranh sơn.**
  - Mặt và thân dưới ánh sáng thật vẫn loang mượt kiểu CG. Nét cọ trong tranh nhỏ và đều; phần "sơn" chủ yếu do lớp Kuwahara chung của hướng C.
  - Chưa có mảng màu phẳng, dứt khoát như bối cảnh. Nét mặt (đường mí, vết chân chim) còn giống nét mực minh hoạ hơn nét sơn.
- **Mặt Ida ở cận cảnh** đã đọc được là bà già, nhưng chất tranh chưa có độ tinh của họa sĩ. Hình khối đầu vẫn hơi "đất nặn".
- **Không nhận bóng.** Lớp tranh không nhận bóng đổ (thân vô hình nằm ngay trong thẻ sẽ tự che). Tay không đổ bóng lên mặt hay thân, và vật khác không đổ bóng lên người. Bóng người ra tường và nền thì đúng.
- **Cảnh 5, nhìn từ sau:** người nhỏ, tối. Búi của Ida không lộ trong bóng (bị đầu che theo hướng chiếu). Tín hiệu nữ trong bóng chỉ còn váy loe, vai khăn và mũ.

## 5. Rủi ro khi chuyển động

- **Đổi tranh góc nhìn (đầu, thân):** bước 4° gây nhảy nét khoảng 1 px ở cỡ khung đi bộ; không thấy trong 8 khung liên tiếp (40–47). Ở cận cảnh mà đầu quay nhanh, bước nhảy có thể thấy (nét mắt dịch khoảng 14 px mỗi 4° ở 1080p). Cách xử lý: bước nhỏ hơn cho cận cảnh động, đổi lại tốn thời gian vẽ tranh.
- **Dải nhìn dọc trục** (chi chĩa thẳng vào máy) bị thu hẹp. Chưa có nắp tròn ở khớp; bốn shot hiện tại chưa gặp.
- **Nhấp nháy, gãy khớp:** chưa thấy. Dải liền qua khuỷu và gối. Độ sâu từng điểm ảnh tránh thứ tự lớp nhảy.
- **Xuyên hình:**
  - Vạt áo và váy ôm theo chân nên có lúc che một phần **đèn lồng ở thắt lưng** (khung 45–47).
  - Khuỷu gập mạnh (tay vác thang, −105°) gấp dải vào trong, chấp nhận được ở cỡ nhỏ.
  - Khăn và cổ áo có thể chạm cằm khi cúi sâu.

## 6. Thời gian (máy chạy song song với agent khác, số nhiễu)

| 8 mẫu | 2D | Nhân vật cũ (base), cùng lúc đo |
|---|---|---|
| 1920×1080 a_close | 7,35 s | 7,40 s |
| 1920×1080 b_cas_bird | 4,47 s | 4,27 s |
| 1920×1080 walk (khung 48–49) | ≈ 7,0 s | ≈ 7,2 s |
| 960×540 (a/b/c/walk) | 2,7 / 1,6 / 1,2 / 2,2–2,6 s | 2,8 / 1,7 / 1,2 / 2,2 s |

- **Ước tính: nhân vật 2D tốn ngang nhân vật cũ (chênh −2 % đến +5 %).**
- Vượt ngân sách 5 s ở 1080p là do bộ cảnh chung trên máy đang tải, không do nhân vật. P đo lại tuần tự để có số sạch.
- Vẽ tranh góc nhìn chạy khi dựng hoặc khi đổi góc: 512² khoảng 0,1 s, 1024² khoảng 0,3–0,5 s mỗi tranh. Ở shot đi bộ, khoảng mỗi 4° có một tranh mới, dồn vào vài khung.
- Độ phân giải tranh theo `opts.detail`: ≥ 34 (cận cảnh) → đầu 1024 và thân 1024; còn lại 512.
