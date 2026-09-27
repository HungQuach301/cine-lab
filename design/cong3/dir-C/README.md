# Hướng C — "Painted Glow" (tranh sơn ánh sáng, luminist/tonalist)

Cổng 3 vòng 1 · Last Round · phiên xưởng hướng C. Trạng thái: **bản đề xuất, chưa duyệt**.

## Nộp
| File | Nội dung |
|---|---|
| `scene.js` | trang cho `shared/render_still.js` (setup, renderFrame, finalize, đo key : tràn) |
| `s1.js`, `s5.js` | dựng hai khung |
| `paint.js` | lớp "vẽ" chạy sau `accumulate`, trước pass cuối của `shared/post.js` |
| `common.js` | kết cấu sinh bằng canvas, sprite quầng sáng, UV phẳng, máy quay có lens shift |
| `out/s1_opening.png`, `out/s5_shadows.png` (+ `.rgb` 48 khung, `.timing.json`) | chất lượng cuối, 32 mẫu, 1920×1080 |
| `out8/*.png`, `out8/*.timing.json` | thiết lập sản xuất, 8 mẫu, 1 khung |
| `out/extra/s5_shadows_briefcam.png` | tham khảo: s5 đặt máy **đúng chữ brief** (1,5 m sau đèn), 16 mẫu, chưa tinh chỉnh |

Lệnh: `cd design/cong3 && PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers node shared/render_still.js --page dir-C/scene.js --frame <s1_opening|s5_shadows> --out dir-C/out --samples 32 --frames 48`.
Tuỳ chọn `--args`: `{"nopaint":1}` bỏ lớp vẽ; `{"measure":1}` in tỷ lệ key : tràn tại vách (s5); `{"prof":1}` in thời gian từng pass; `{"dbg":{"briefcam":1}}` dựng s5 theo máy của brief.

## 1. Ngôn ngữ hình ảnh

**Ý tưởng.** Hình là một bức tranh về *ánh sáng và không khí*, không phải về đồ vật. Mảng rộng, ít chi tiết, cạnh lúc mất lúc hiện; nhiệt độ màu ấm/lạnh là nhân vật chính. Tham chiếu tinh thần là trường phái luminism/tonalism thế kỷ 19 (phạm vi công cộng), không chép tranh cụ thể nào.

**Hình khối.** Kiến trúc giản lược thành khối hộp, mái dốc hai mái hoặc bốn mái, ống khói có chóp sành: mái và ống khói tạo nhịp. Không cây, không trang trí nhỏ. Hai khung đều bố cục theo mảng lớn:
- s1: mảng trời (tím → hồng → đào) trên một dải sương sáng, thành phố xếp lớp nhạt dần theo độ sâu, tiền cảnh là các khối tối. Phố Ostler là dải sáng dẫn mắt từ quảng trường vào giữa khung.
- s5: "tranh trong tranh". Mặt tường trắng phẳng, giữa là lòng vòm tối ấm, trong đó có hai bóng người lớn. Chọn khung này vì nó kể trọn ý "ngoài trắng, không bóng; trong ấm, có bóng" trong một hình.

Nhân vật dùng `buildCharacter` chung, **không đổi tỷ lệ**. Tôi chỉ thêm hai thứ:
- một vỏ tóc phủ gáy, gắn vào khớp đầu, to bằng 1,02× sọ;
- ở s5, hạ giá trị màu tóc Ida xuống 0,45×, thành xám trung bình.

Lý do: khi Ida quay lưng dưới ánh đèn thấp, búi tóc sáng cộng với gáy màu da làm người xem đọc nhầm thành một khuôn mặt nhìn vào máy.

**Chất liệu (lớp vẽ, `paint.js`, mỗi khung chạy một lần, toàn bộ trong Float32 tuyến tính):**
1. G-buffer ghi độ sâu và mặt nạ "quan trọng" (nhân vật, đèn).
2. Tensor cấu trúc ở nửa độ phân giải.
3. Lớp lót:
   - nét "tay vẽ": lệch toạ độ lấy mẫu ±3–4 px theo nhiễu chậm, để cạnh thẳng hình học thành cạnh vẽ tay;
   - nhiễu nét cọ **thẳng**, kéo dài theo hướng cấu trúc; ở vùng phẳng thì trộn 3 hướng cố định, không xoay toạ độ theo điểm ảnh nên không xoáy;
   - điều chế độ sáng ±16 % và nhiệt độ màu ±6 % ("màu vỡ").
4. **Kuwahara dị hướng, trọng số đa thức 8 cung** (Kyprianidis 2010), 28 mẫu thưa trong elip, xuất ở nửa độ phân giải.
   - Bán kính tăng theo độ sâu và giảm ở vùng quan trọng, để chi tiết dồn về nhân vật và nguồn sáng.
   - Lớp lót ở bước 3 biến thành các mảng cọ có biên.
5. Ghép ở độ phân giải đầy đủ:
   - vân cọ ngắn sau lọc;
   - bloom 6 tầng (13 mẫu xuống, lều lên);
   - halation cam quanh vùng rất sáng.
6. Trỏ `outMat.uniforms.tAcc` sang kết quả. Tone map, `grade()`, grain và dither vẫn là của `shared/post.js`. **GRAIN không đổi**, không sửa file nào trong `shared/`.

`gradeGLSL` làm ba việc:
- nâng vùng tối về tím-lam, vùng sáng hơi lạnh;
- thêm vân canvas rất nhẹ (±1,2 %, tĩnh theo khung);
- làm tối mép khung theo elip mềm.

**Lớp 2D (`overlayCanvas`):** không dùng. Chất liệu nằm trong lớp vẽ và `grade()`.

**Bảng màu**
| Hex | Vai trò |
|---|---|
| `#292b5c` → `#544a8c` | thiên đỉnh, trời cao (tím chàm) |
| `#946ea8` | trời giữa (tím hoa cà) |
| `#db8f9e` | trời thấp, đáy mây (hồng) |
| `#fab899` | ráng sát chân trời (đào) |
| `#d99aa0` / `#a386ad` / `#6a679c` | màu sương theo độ cao trên khung: đỉnh / giữa / đáy (không khí dày, nhạt dần theo sâu) |
| `#4a4c5c`, `#55505a`, `#5e4640` | mái đá đen, mái ngói sẫm (khối tối tạo nhịp) |
| `#8a5a48`, `#a88a6e`, `#c2ad90` | tường gạch và vữa (bị sương tím nuốt dần theo độ sâu) |
| `#ffa24f` (sáng), `#ffc070` (lõi quầng), `#ff9448` (quầng rộng) | đèn khí: tâm hổ phách |
| `#b8b4d8` (kính), `#b8b6c4` (tấm kính mờ) | đèn khí chưa thắp, cột điện chưa bật: bắt ánh trời, lạnh và tắt |
| `#ffae5c`, kính `#ffb85a`, lửa `#fff2d0` | đèn lồng (s5): nguồn ấm duy nhất trong hốc |
| `#ff9a52` (dội), `#ff8a40` (không khí) | ánh dội và không khí ấm trong hốc |
| `#d4e2f4` | ánh điện: trắng lạnh hơi xanh, phẳng |
| `#ece6da`, `#e6e1d8` | vôi quét trên gạch (vách hốc, mặt tiền nhà kho) |
| `#c9c1b4`, `#8d877f` | đá vòm cuốn, gờ chân tường |
| `#4a4e57`, `#565b66` | gang (ống nước, cột điện) dưới ánh phẳng: xám lạnh, không đen |
| `#ffb060` (mờ) | vài cửa sổ có người: rất ít, để đèn khí vẫn là tâm |

**Ánh sáng và bóng (đúng luật thế giới mục 2–3)**

s5, đèn lồng:
- `SpotLight` có bóng, nón hướng vào vách, cộng phần bù omni **không bóng** ngoài nón (tiêm vào shader). Tổng lại là một nguồn điểm.
- Vị trí nguồn jitter trong khối kính 12 cm theo từng mẫu (Halton 2,3,5), nên rìa bóng mềm thật, không phải làm mờ trong hậu kỳ.
- Đèn cách vách 3,0 m, người cách vách 1,0 m, nên bóng phóng đại 1,5× và vươn cao (đỉnh bóng Ida ≈ 2,6 m).
- Lửa thở ±4 % theo số khung (`flickAt`).

s5, ánh điện:
- Là ánh tràn phẳng, không bóng đổ, chỉ có bóng tiếp xúc rất nhẹ.
- Lọt vào hốc theo hàm mũ độ sâu (0,32 m), cộng một nền lạnh rất yếu dội sâu vào trong. Nhờ vậy vùng tối của bóng hơi tím, không đen.
- Dội ấm 6,5 % từ vách và nền.

**Tỷ lệ key : tràn đo tại vách**, tuyến tính, trước tone map, `{"measure":1}`, 16 mẫu:
| Điểm đo | Tỷ lệ |
|---|---|
| vách sáng hai bên | 33 : 1 và 36 : 1 |
| vách giữa-cao | 20 : 1 |
| đỉnh vách | 14,5 : 1 |
| đỉnh vách, nếu tính cả dội ấm vào "tràn" | ≈ 5,8 : 1 |

Tất cả ≥ 4 : 1 và không điểm nào nằm trong ±5 % quanh ngưỡng. Trong bóng, ở đầu Ida, sáng / bóng ≈ 8,5 : 1.

s1:
- Trời là shader gradient có dải mây tầng mỏng ửng hồng.
- Ánh chạng vạng gồm bán cầu tím + ráng hồng thấp (không bóng).
- Đèn khí số 1–3 là `PointLight` hổ phách. Đèn số 3 (vừa thắp) là `SpotLight` có bóng, jitter theo mẫu, nên Ida đổ bóng mềm.
- Đèn 4–11 chưa thắp. 6 cột điện (5 cột xen giữa từng cặp đèn khí, 1 cột cạnh nhà kho) chưa bật. Có dây điện võng.
- Sương đổi màu theo độ cao trên khung. Tôi ghi đè `THREE.ShaderChunk.fog_fragment`; chỉ ảnh hưởng vật liệu có fog, và s5 không có fog.

## 2. Thời gian render

**Cảnh báo: số dưới đây đo khi 3 hướng chạy song song**, tải máy 6–9 trên 4 vCPU, nên bị phóng đại khoảng 2–3 lần và dao động mạnh. P cần đo lại tuần tự.

Tôi dựng cảnh, biên dịch shader và chạy khởi động 1 mẫu trong `setup` (`setup_s` 6–16 s, chi phí một lần mỗi shot). `render_frame_s` là thời gian một khung: tích luỹ + lớp vẽ + pass cuối.

| Khung | 32 mẫu (`out/`) | 8 mẫu (`out8/`) | 8 mẫu, lần tốt nhất trong 3 lần đo `prof` |
|---|---|---|---|
| s1_opening | 24,5 s | 6,5 s | 4,5 s (tích luỹ 2,9 s, lớp vẽ 1,2 s) |
| s5_shadows | 25,8 s | 4,4 s | 3,5 s (tích luỹ 2,0 s, lớp vẽ 1,2 s) |

Lớp vẽ tốn khoảng 1,2–1,6 s dưới tải, trong đó riêng Kuwahara 0,8–1,1 s. Pass cuối cho mỗi khung grain thêm: 0,3–0,6 s.

**So với ngưỡng 2,5 s/khung:** ở thiết lập sản xuất (8 mẫu), số đo dưới tải vượt 1,4–1,8× (s5) và 1,8–2,6× (s1). Tôi chưa đo được trên máy rảnh, nên chưa biết có vượt hay không.

**8 mẫu so với 32 mẫu:** khi soi phóng to gần như không phân biệt được. Lớp Kuwahara che răng cưa; rìa bóng ở 8 mẫu hơi bậc hơn một chút, khó thấy.

**Cách hạ, theo thứ tự nên thử:**
1. Hạ xuống 4 mẫu (tích luỹ giảm khoảng 1/2).
2. Kuwahara 28 → 16 mẫu, hoặc chạy ở 1/3 độ phân giải (lớp vẽ giảm khoảng 40 %).
3. s1: nướng vũng sáng đèn khí thành decal thay cho 3 point light (mỗi light cộng khoảng 15 % chi phí điểm ảnh), bớt sprite quầng ở các phố xa.

## 3. Tự phê bình

**Chỗ còn "trông như CG rẻ tiền"**
- **Nhân vật** là khối nguyên thuỷ của bộ dựng chung (trụ, cầu, nón). Ở khung rộng s5 và ở s1 (Ida ≈ 15 px) thì chấp nhận được. Xem `out/extra/s5_shadows_briefcam.png`: ở cỡ trung cận, chúng lộ rõ là đồ chơi, và lớp vẽ chỉ làm mờ chứ không cứu được. Muốn đạt chuẩn chuyên nghiệp cần: mô hình điêu khắc lại (nếp áo, bàn tay), texture vẽ tay, bậc sáng tối vẽ tay (ramp) cho da và vải.
- **Thành phố s1** là hộp sinh thủ tục. Lưới cửa sổ đều răm rắp, mái cùng độ dốc, vài khoảng đất trống vô nghĩa ở phía trong khúc cong (chỗ tôi hạ nhà xuống một tầng để thấy phố). Sương và lớp vẽ che được ở xa; tiền cảnh bên phải vẫn lộ.
- **Mặt tường trắng s5** chiếm khoảng 60 % khung. Nó phẳng đúng luật, nhưng về hội hoạ còn trống: vân gạch lặp và đều, đá cuội thành hoa văn chấm đều. Cột điện bên phải hơi nặng.
- **Lớp vẽ tính trong không gian màn hình.** Nhiễu nét cọ, độ lệch cạnh và vân canvas gắn vào khung hình, không gắn vào vật. Khi máy hay nhân vật chuyển động, hình sẽ bị hiệu ứng "kính tắm" (shower-door), và Kuwahara có thể nhấp nháy giữa các khung. **Đây là rủi ro lớn nhất của hướng C, và tôi chưa thử trên chuyển động.** Cách sửa: gắn nét vào không gian vật (texture nét cọ theo UV hoặc theo toạ độ thế giới), hoặc làm ổn định theo thời gian bằng luồng quang học. Cả hai đều tốn thêm công và thời gian render.

**Chỗ chưa đúng hoặc chưa rõ theo luật thế giới và brief**
- **s5 lệch brief về máy quay (quyết định có chủ ý, chờ P và chủ dự án):**
  - Với máy 1,5 m sau đèn (tức 0,5 m ngoài miệng vòm) và FOV dọc 35–42°, khung nằm trọn trong lòng vòm rộng 3,2 m: nửa bề ngang khung tại mặt tiền chỉ ≈ 0,33 m. Vì vậy **không thể thấy "phố trắng ở mép khung"**.
  - Muốn thấy mặt tiền ở hai mép thì máy phải lùi ≥ 2,5 m ra ngoài vòm. Tôi đặt máy ở 7,5 m sau đèn (6,5 m ngoài vòm), cao 1,35 m, FOV 42°, dịch ống kính lên 0,25 để đường đứng vẫn thẳng.
  - Bản đúng chữ brief nằm ở `out/extra/`.
- **s1:**
  - Đồng hồ quảng trường chỉ ≈ 30 px và bị nhìn từ trên cao gần như xiên cạnh, nên **không đọc được là mặt đồng hồ** (vạch và kim có trong mô hình).
  - Đèn 4–11 chưa thắp và cột điện quá mảnh ở khoảng cách này, gần như không thấy.
  - Nhịp "tâm hổ phách – khoảng tối" chỉ rõ ở 3 ngọn gần.
  - Phố chỉ lộ khúc đầu; khúc cong phía xa bị mái nhà che.
- **Bóng tường nhà ở s1:** chỉ Ida đổ bóng (spot đèn số 3). Nhà cửa không đổ bóng từ đèn khí; ở cỡ này không thấy lỗi, nhưng cận cảnh thì phải bật.
- **File `.rgb` 48 khung:** grain đổi theo khung như yêu cầu, nhưng lửa **không** thở, vì cả 48 khung dùng chung một lần tích luỹ. Hàm `flickAt(f)` đã có sẵn cho khi render thật từng khung.

**Còn thiếu để đạt mức chuyên nghiệp**
- Họa sĩ vẽ tay texture cho nhân vật, đá và tường.
- Bố cục s1 cần một nét vẽ tay (matte painting) cho tiền cảnh và đường chân trời.
- Kiểm chuyển động (xem rủi ro "kính tắm" ở trên).
- Đo banding bằng `checks` (tôi không đọc `checks/`). Sương, bầu trời và quầng sáng đều đi qua Float32 + dither + grain chung, nhưng tôi chưa đo.

## 4. Đã tránh gì để không giống IP có sẵn
- **Ghibli / nền Kazuo Oga:** không cây lá, không mây tích lớn, không nền chi tiết hiện thực bằng gouache. Trời là dải tầng mỏng, bảng màu tím–đào đơn sắc theo lối tonalist.
- **Loving Vincent / Van Gogh:** không nét cọ xoáy, không impasto dày. Nét thẳng, ngắn, biên độ thấp, chỉ 3 hướng cố định. Tôi đã bỏ bản thử đầu vì nhiễu xoay theo trường hướng tạo vân xoáy như vân gỗ.
- **The Flying Sailor:** không có mảng màu phẳng trừu tượng hay biến dạng hình học kiểu phim đó.
- **Ice Merchants, Hair Love, Alike, Sprite Fright, Laika, Aardman, Pixar:** không nét viền đồ hoạ, không chất liệu đất sét, không nhân vật tỷ lệ kiểu Pixar. Nhân vật giữ nguyên model sheet chung.
- **Không có chữ đọc được:** mặt đồng hồ chỉ có 12 vạch và 2 kim, không biển hiệu nào.
- Tháp chuông và ống khói nhà máy ở xa chỉ là khối chung chung, không mô phỏng công trình có thật.
- Mọi tài sản sinh bằng mã (canvas, shader). Không tải gì từ ngoài, không dùng font.

## Ghi chú cho P
- `shared/cast.js` dòng 139: lệnh `brow.position.set(...); tag(brow…); headG.add(brow)` nằm **sau** dấu `//` của chú thích, nên lông mày không bao giờ được gắn. Tôi không sửa vì ngoài phạm vi.
- `scene.js` dựng **cả hai cảnh** trong `setup`, vì driver không truyền tên khung cho `setup`. Hệ quả là `setup_s` bị cộng dồn.
