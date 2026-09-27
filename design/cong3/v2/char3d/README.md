# Cổng 3 vòng 2: Cách (1), nhân vật 3D nâng cấp (hướng C "Painted Glow")

Người làm: phiên xưởng nhân vật (Claude). Trạng thái: **bản nộp cho P**, chưa được chủ dự án duyệt. Chưa commit.

## File đã nộp
| File | Vai trò |
|---|---|
| `cast3d.js` | Module dựng nhân vật, **cùng API** `shared/cast.js`: `buildCharacter(sheet, opts)` trả `{ root, joints, props, hands, parts, H, sheet, setPose }`. Không xuất `update()` vì không cần. |
| `sdf.js` | Công cụ điêu khắc SDF (lưới hình sao, mảng tóc, ống), nhiễu, da CPU (`CpuSkin`). |
| `tex3d.js` | Kết cấu sinh bằng mã: map loang nét cọ và normal map (len đan, bo len, tóc). |
| `dev_page.js` | Trang thử riêng: turnaround, cận mặt, cận tay, nhìn từ đèn. Không dùng cho shot so sánh. |
| `test/*.png` | 4 shot ở 960×540, 8 mẫu: `a_close_ida`, `b_cas_bird`, `c_s5_wide`, `walk_000/048/095`, kèm file thời gian. |
| `dev/*.png` | Ảnh tham chiếu dưới đèn studio trung tính: `ida_sheet`, `cas_sheet`, `ida_body`, `cas_body`, `ida_face`, `cas_face`, `ida_hands`, `cas_light` (tay chim bóng nhìn từ vị trí đèn khí). |

Không có tài sản ngoài: mọi hình, kết cấu và màu đều sinh bằng mã trong ba file trên. Không font, không ảnh, không tải mạng. Vì vậy không phát sinh dòng mới cho `RIGHTS.md`.

## Cách làm
1. **Giữ nguyên khung xương gốc.** `cast3d.js` gọi `buildCharacter` của `shared/cast.js` để lấy khung xương, `applyPose`, nhóm vạt áo và đạo cụ (lồng đèn, thang, sào). Sau đó gỡ toàn bộ hình khối cũ và dựng hình mới gắn vào đúng các khớp đó. Tên khớp, quy ước góc, JSON tư thế, `lantern.userData.lightAnchor/handleY` đều không đổi.
2. **Khối điêu khắc SDF.** Đầu, thân áo, ủng, mũ, búi tóc, lòng bàn tay và từng đốt ngón được mô tả bằng hàm khoảng cách (hợp mềm `smin`, khoét `smax`, rãnh nếp nhăn). Từ hàm đó module dựng một lưới liền: mỗi đỉnh của lưới cầu UV được bắn tia từ ngoài vào tới mặt (sphere tracing, rồi chia đôi). Pháp tuyến lấy từ gradient nên không có đường nối. Lưới đầu dày ở vùng mặt (warp φ, θ).
3. **Ống liền da CPU qua khuỷu, gối và hông.** Tay áo, chân và váy là ống liền. Trọng số được trộn quanh khớp, và phép da tuyến tính được tính trên CPU sau mỗi `setPose`. Module dùng mesh thường (không dùng `SkinnedMesh`), nên G-buffer của lớp vẽ `dir-C/paint.js` (có vertex shader riêng) và bóng đổ đều thấy đúng hình đã uốn. Riêng shot walk gọi `setPose` 8 lần mỗi khung; chi phí CPU không đáng kể.
4. **Bề mặt hợp tranh sơn.** Mọi vật liệu đi qua `opts.material(role, color, part, extra)`, nên ánh sáng do cảnh quyết định (Lambert, không bóng nhựa). Phần `extra` truyền `map` (nền gần trắng có mảng loang và nét cọ lệch sắc nóng lạnh, nhân với màu model sheet nên giữ quan hệ sáng tối), `vertexColors` (AO tính từ SDF làm tối nếp và hốc, bóng AO hơi tím; má và mũi ấm; hốc mắt lạnh; nét mi trên như nét cọ) và `normalMap`. Normal map chỉ dùng cho len và tóc; da, dạ và vải chỉ dùng map loang, vì vi chi tiết kiểu CG không sống qua lớp vẽ và làm chậm.

## Những gì đã thêm
**Ida (74, nữ)**
- Mặt có cấu trúc: hốc mắt, cung mày, gò má cao với má hóp dưới gò, mí trên nặng và da chùng trên mí, mũi dài có gồ và đầu khoằm. Nếp nhăn gồm 3 nếp trán, nếp cau mày, vết chân chim, bọng dưới mắt, rãnh mũi–má, rãnh khoé miệng xuống cằm và hàm hơi sệ. Có đồi mồi nhạt. Nhãn cầu tách riêng, tròng vẽ bằng canvas, nhìn hơi xuống.
- Tóc bạc chải ngược về búi, lộ ở thái dương và gáy dưới vành mũ. **Búi xoắn to**, phóng 1,3× so với sheet (xem mục phóng to).
- Khăn quàng len (hồng đất) quấn hai vòng, có nút và đuôi buông trước ngực. **Váy dài** lộ 0,5 H dưới gấu áo khoác, xếp nếp dọc, da theo chậu và hai hông. Tất tối màu.
- Dáng người già: vai xuôi, lưng trên hơi tròn, gồ gáy–vai. Cổ có gân và nếp.
- Áo khoác: thân có nếp phồng trên thắt lưng, loe dưới thắt lưng, nếp dọc lưng, nếp chéo nách, nẹp và mép khép áo, 4 khuy, thắt lưng có khoá. Bốn vạt áo mới có nếp dọc sâu dần xuống gấu và lót màu, giữ nguyên cơ chế vạt của bản gốc. Tay áo có nếp nén trong khuỷu, nếp xoắn và măng sét lật. Cổ áo đứng.
- Mũ phớt giữ silhouette đã duyệt, thêm rãnh đỉnh, hai vết bóp trước, vành có mép cuộn và gợn, băng mũ có nơ.

**Cas (10, nam)**
- Đầu tròn, má phúng phính, mũi nhỏ tròn, mắt to nâu, mày ngắn hơi xếch trong (rụt rè).
- **Tai vểnh thật**: bản lề ở mép trước, vểnh theo góc 38° của sheet. Bản gốc xoay tai quanh tâm nên nửa tai chìm vào đầu; bản này đọc được từ sau lưng.
- **Tóc ngắn nâu** lộ ở gáy và thái dương dưới mũ, mép lởm chởm.
- Mũ len có sọc đan, vòm hơi thuôn, bo mép gấp. **Quả bông đặt cao, tròn, xù len, có eo túm len bên dưới** để tách khỏi vòm, nhằm không bị đọc thành búi.
- Áo len quá khổ (vai xệ, gấu và cổ bo, len chùng trên gấu), mắt len đan dạng normal map. Tay áo trùm quá cổ tay, bo và miệng loe.
- Quần cũn **lộ cổ chân**. Ủng hạ thấp cho khớp sheet: bản gốc có ủng cao 0,41 H che mất phần cổ chân mà sheet yêu cầu.

**Bàn tay (cả hai)**: lòng bàn tay điêu khắc có gò ngón cái, gò út, khớp đốt ở mu và gân mu (Ida). Có 4 ngón × 3 đốt và ngón cái 2 đốt, móng tay. Gập tay phân bổ qua 3 khớp (MCP, PIP, DIP). Ngón của Cas dẹt rộng (tỷ lệ 1,5 trong mặt phẳng lòng tay) để bóng các ngón liền thành cánh có mép lông.

## Phóng to (cần chủ dự án duyệt)
| Mục | Hệ số | Lý do |
|---|---|---|
| Bàn tay và ngón **Cas** | **1,30×** (đúng trần cho phép) | Để chim bóng thành hình cánh. **Chỉ số nằm đúng ngưỡng trần 1,3×.** |
| Bàn tay và ngón **Ida** | 1,15× | Đọc được ngón trong cận cảnh hơ tay. |
| Búi tóc Ida | 1,30× so với sheet (0,42 → 0,55 H) | Đọc rõ búi trong silhouette nghiêng (shot walk). |

Hằng số nằm ở `HAND_SCALE` và `BUN_SCALE` đầu `cast3d.js`. Phóng to là phép co giãn đều nhóm `hand_L/R`; C3 không đổi.

**Màu thứ cấp mới** (`EXTRA_COLORS`, chờ duyệt): khăn `#8e5c5a`, váy `#4a3a44`, tất `#3a3235`, tóc Cas `#5a4034` (tóc Cas đã có trong bản gốc).

## Phát hiện: lỗi dấu "spread" trong `shared/cast.js` (P cần biết)
`applyPose` đặt `finger.rotation.x = (1,5 − i)·0,30·spread`. Ngón 0 nằm ở phía +z (cạnh ngón cái), nên góc dương làm nó quay về −z, tức về phía các ngón kia. Vì vậy **"xoè" thực chất là KHÉP**. Đây là nguyên nhân chính khiến cánh chim bóng vòng 1 thành que. `cast3d.js` đảo dấu trong phần tư thế ngón của mình, không sửa `shared/`. Cách (2) nếu dùng góc ngón của `applyPose` gốc sẽ gặp đúng lỗi này. Chủ dự án hoặc P quyết định có sửa gốc hay không.

Kết quả ở `test/b_cas_bird.png` và `dev/cas_light.png`: bóng hai bàn tay thành hai cánh rộng có mép lông, hai ngón cái dựng. Giới hạn còn lại nằm ở **tư thế**, không ở bàn tay: tư thế đặt hai tay tách nhau với hai ngón cái, nên bóng đọc thành "hai cánh, hai đầu". Tôi gợi ý P thử biến thể bắt chéo cổ tay, một ngón cái làm đầu (đó là sửa JSON tư thế, ngoài phạm vi của tôi).

## C3 (độ dài bộ phận)
Khung xương không đổi, nên khoảng cách tâm khớp giữ nguyên. Mesh mang tên bộ phận đo chỉ phủ đoạn giữa hai tâm khớp; phần kéo dài được tách thành `*_joint`, `sleeve_cuff`, `thigh_skin`, `shin_trouser`. Đo bbox dọc ở tư thế turnaround (dev page, `dbg`):
- Ida: thigh 0,374 m = **1,45 H**; shin 0,361 m = **1,40 H**. Thân từ −0,06 H tới +0,02 H quanh [chậu, cổ], cắt bằng SDF về đúng khoảng của bản gốc (−0,05 … tL + 0,02 H).
- Cas: thân từ −0,06 H tới tL + 0,02 H; thigh 1,05 H; shin 1,15 H.
- Đầu: đỉnh sọ đặt ở 1,0 H, cằm ở khoảng 0 (đầu nghiêng 8° trong turnaround làm bbox dọc hơi lớn hơn).

Tôi chưa chạy bộ đo C3 chính thức (thuộc `checks/`, phiên K). Đề nghị P hoặc K đo lại.

## Thời gian (máy đang chạy song song, số nhiễu)
| Shot | Gốc (`base`) | 3D mới | Ghi chú |
|---|---|---|---|
| a_close_ida 960×540 | 2,8–4,3 s | 3,9–4,1 s | hai lượt xen kẽ: base 4,33 / 2,95; 3d 6,54 / 4,04 |
| b_cas_bird 960×540 | 1,66 s | 2,0 s | |
| c_s5_wide 960×540 | 1,17 s | 1,45 s | |
| walk 960×540 | khoảng 2,1 s (P đo) | 2,6–2,75 s/khung | |
| **a_close_ida 1920×1080** | **10,5 s** | **12,6 s** | cùng đợt tải |
| **walk 1920×1080** (3 khung) | **7,05 s** (trung vị) | **7,4 s** (trung vị) | tải 3,4 |

**Ước tính:** nhân vật mới làm tăng khoảng **+5 %** mỗi khung ở shot rộng (walk) và khoảng **+20 %** ở cận mặt, so với nhân vật gốc trong cùng điều kiện. Ngay bản gốc cũng vượt 5 s/khung ở 1080p trên máy đang tải, nên ngân sách 5 s phải được P đo sạch. Nếu cần giảm: hạ `opts.detail` (lưới co theo `detail/32`), hoặc bỏ normal map len. Số đỉnh: Ida khoảng 54 k, Cas khoảng 40 k ở `detail` 36; ở `detail` 20 (s5) khoảng 60 %.

## Tự phê bình (thẳng thắn)
- **Mặt vẫn "búp bê sáp" ở cận cảnh.** Hình khối đúng tuổi (nếp, mí, mũi), nhưng da mịn đều. Dưới ngọn lửa sát mặt (phơi sáng 0,30) mặt Ida gần như cháy sáng, nên nếp nhăn chỉ còn nhờ bóng. Vùng miệng ở cận cảnh 1080p còn một vệt sáng tối đọc gần như "hé miệng thấy răng", do môi dưới bắt đèn đặt thấp. Mí và môi bị giới hạn bởi cách chiếu hình sao: các chỗ khuất tia (dưới mí trên, kẽ môi) không biểu diễn được, nên tôi phải làm mí và môi mềm, nông.
- **Bàn tay đọc được ngón, nhưng mu tay trơn như găng cao su.** Gân và đốt của Ida chỉ thấy khi nhìn gần.
- **Chỗ còn "ma-nơ-canh"**: khuỷu và gối uốn bằng LBS nên xẹp khi gập mạnh; tôi lấp bằng khối tròn cứng (chỏm vai, khuỷu), và khi gập hơn 100° khuỷu thành "cùi chỏ tròn". Cổ vẫn là ống chui dưới khăn hoặc cổ áo, chưa liền với thân. Thân áo liền một khối, không có nách tách.
- **Lệch chất tranh sơn**: bề mặt vẫn là shading 3D liên tục. Chất "tranh" chủ yếu đến từ lớp vẽ chung. Map loang và màu đỉnh chỉ giúp mảng màu có nhiệt độ; lớp Kuwahara xoá gần hết vi chi tiết. Len đan (normal map) có lúc đọc thành lưới đều kiểu CG ở cận cảnh (khăn Ida).
- **Silhouette ở khung rộng s5 thay đổi ít** vì nhân vật quay lưng, ngược sáng và nhỏ. Búi Ida bị đầu che trong bóng trên vách (đèn phía trước), vì thế vẫn đọc bằng mũ phớt. Cas: quả bông đã tách khỏi vòm bằng eo túm, tai vểnh ra, nhưng bóng mờ vẫn có thể đọc là "búi". Việc này cần P kiểm silhouette mù lại, tôi không tự đo.

## Rủi ro khi chuyển động
- **Xuyên hình váy, chân và vạt áo**: váy da theo hông tới 85 %, vạt trước theo hông 60 % (cơ chế gốc). Tôi chỉ xem walk ở khung 0/48/95, chưa xem đủ 96 khung, nên có thể gối hoặc ống chân chọc qua váy ở pha đưa chân và váy chọc qua vạt trước. Cần P xem clip đủ.
- **LBS khuỷu và gối**: xẹp thể tích khi gập mạnh (tay phải vác thang gập 105°), khối khuỷu cứng có thể lộ gờ.
- **Nhấp nháy**: hình học tất định (nhiễu có hạt giống), UV dính theo bề mặt kể cả phần da CPU, nên không có kết cấu "bơi". Nguồn nhấp nháy tiềm năng là nếp nhỏ (rãnh mặt, sọc len) dưới Kuwahara ở độ phân giải thấp; cần đo bằng `{"nopaint":1}` so với có lớp vẽ.
- **Motion blur walk**: da CPU tính lại cho mỗi mẫu nên đúng với jitter thời gian của shot; tôi đã kiểm tra nó không vỡ hình ở 3 khung.
- Không có thẻ 2D quay nên không có rủi ro xoay thẻ.

## Lệnh thử
```
cd design/cong3; export PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers
node shared/render_still.js --page v2/page.js --frame a_close_ida --out v2/char3d/test --samples 8 --w 960 --h 540 --args '{"char":"3d","shot":"a_close_ida"}'
node shared/render_seq.js --page v2/page.js --shot walk --from 48 --to 49 --out v2/char3d/test --samples 8 --w 960 --h 540 --args '{"char":"3d"}' --pngs 48
node shared/render_still.js --page v2/char3d/dev_page.js --frame cas_light --out v2/char3d/dev --samples 4 --w 960 --h 540 --args '{"who":"cas","view":"light","pose":"shadow_bird","ry":3.29159,"fov":5}'
```

## Việc đang chờ chủ dự án
1. Duyệt phóng to tay (Cas 1,3×, đúng trần; Ida 1,15×) và búi 1,3×.
2. Duyệt màu thứ cấp mới (khăn, váy, tất) và các chi tiết thứ cấp (khăn, váy, búi, tai vểnh, tóc gáy).
3. Quyết định sửa lỗi dấu `spread` ở `shared/cast.js` hay không (ảnh hưởng cả cách (2)), và có thử tư thế chim bóng bắt chéo cổ tay hay không.
