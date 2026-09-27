# Hướng A — "Tin & Felt" (diorama thủ công thu nhỏ quay bằng ống kính thật)

Cổng 3 vòng 1 · phiên xưởng hướng A · trạng thái: **đề xuất, chưa duyệt**.

File nộp: `scene.js` (trang render), `lib.js` (vật liệu thủ tục, tiện ích), `out/` (32 mẫu, 48 khung), `out8/` (8 mẫu, 1 khung).

## 1. Ngôn ngữ hình ảnh

**Ý tưởng:** thành phố là một mô hình làm tay trên bàn xưởng, được quay bằng máy quay thật. Nhân vật là búp bê dạ/nỉ và len đan. Nhà cửa là bìa cứng và thạch cao sơn tay, cạnh vát tròn. Đèn lồng làm bằng thiếc gò có vết hàn. Ánh sáng và ống kính giữ đúng vật lý: thứ duy nhất "thu nhỏ" là chất liệu và độ sâu trường ảnh.

**Hình khối.** Mọi khối kiến trúc gần máy quay đều bo cạnh (RoundedBox) và hơi "mập": gờ mái dày, ống khói to, mái là tấm dày 15 cm, đá vòm và đá góc nhô ra rõ. Đá lát là **từng viên thật** (khoảng 4 900 instance ở s5, kích thước và cao độ ngẫu nhiên). Tỷ lệ nhân vật giữ nguyên `cast.js`/model sheet (luật C3). Phần tôi thêm chỉ là chi tiết gắn khớp không đổi đường bao:
- lớp tóc len sau gáy cho cả hai nhân vật (nhìn từ sau không còn lộ "đầu trọc" màu da);
- khung thiếc, đai và bản lề cho đèn lồng;
- vết hàn trên đèn lồng.

**Chất liệu** (sinh bằng shader, không dùng texture ngoài, `lib.js`):
- **Dạ/nỉ** (áo khoác, mũ, quần, da mặt và tay): `MeshPhysicalMaterial` có *sheen* (lông tơ sáng ở rìa theo góc nhìn), nhiễu sợi mịn, loang màu mảng, bump theo mét. Đường may chạy lược nổi ở gấu áo, eo và cổ áo.
- **Len đan** (áo len, mũ Cas): hàng mắt chữ V theo UV. **Len thô** dùng cho quả bông, tóc và chỉ thêu mắt (mắt mờ, không bóng, không phải mắt nút).
- **Thiếc** gò búa có lõm, xỉn loang. **Da** ủng sần mịn.
- **Vữa vôi** có vệt bay, vệt ẩm chân tường, mảng vôi bong nhẹ. **Gạch quét vôi** có mạch lõm, vôi bong lộ gạch.
- **Đá** lốm đốm. **Mái** là ngói/đá phiến xếp lớp, có rêu.
- **Mặt tiền s1**: vữa sơn hoặc gạch, cửa sổ kính bóng phản chiếu trời qua IBL, khoảng 6 % ô có đèn ấm, gờ tầng, bậu cửa.
- Họa tiết nhỏ hơn điểm ảnh tự lọc về màu trung bình (khử moiré).

**Bảng màu (sRGB):**

| Mã | Vai trò |
|---|---|
| `#1c223e` → `#3f3556` → `#62536a` / `#b2766a` | Trời s1: thiên đỉnh xanh thẫm → tím → chân trời tím bụi / hồng phía mặt trời lặn |
| `#63566c` | Sương khí quyển s1 (tím xám), làm lùi xa |
| `#ffb66c` | Đèn khí 1 900–2 200 K (hổ phách), nguồn sáng + hào quang |
| `#ffc281` | Đèn lồng s5 (hổ phách, hơi nhạt hơn đèn khí vì cháy nhỏ) |
| `#daedff` | Ánh điện ~6 000 K ngoài phố s5 (trắng lạnh hơi xanh) |
| `#ece6d9` / `#e8e3d8` | Vách vôi trong hốc / tường gạch quét vôi nhà kho |
| `#959390`–`#aaa49e` | Đá lát granite |
| `#5d636e`, `#4f5560`, `#8e604c` … | Mái đá phiến xám lạnh xen ngói nâu nhạt |
| `#b8a27f`, `#a88579`, `#8b9486`, `#cbc2ab` … | Sơn mặt tiền trầm: đất vàng, hồng bụi, xám lục, vôi |
| `#3f5552`, `#2f2826`, `#b9b3aa` | Ida: áo dạ xanh rêu, mũ nâu đen, tóc xám (giữ màu gốc model sheet) |
| `#8a4a3c`, `#d6c9ae`, `#a8483a` | Cas: áo len đỏ gạch, mũ len kem, quả bông đỏ |

**Ánh sáng và bóng** (đúng luật thế giới mục 2–3):
- **s5.** Đèn lồng là nguồn điểm ấm có bóng. Vị trí đèn jitter trong hộp 12 × 8 × 12 cm theo từng mẫu tích luỹ, nên bóng mềm thật. Chỉ đế đèn đổ bóng; nắp coi như có lỗ thông hơi, nên bóng nắp không cắt đỉnh bóng người trên vách (xem mục 3).
  - Ánh điện ngoài phố là đèn hướng trắng lạnh, jitter trong nón rộng (±40° dọc phố, 3–25° vào tường), tức một nguồn rộng, cao, nhiều hướng. Kết quả là ánh sáng phẳng, chỉ còn bóng tiếp xúc rất nhẹ. Khối nhà kho che thật (shadow map), nên ánh điện chỉ lọt vào miệng hốc khoảng 1–2 m trên nền.
  - Ánh dội lạnh từ mặt phố trắng là một đèn diện (RectAreaLight) rất yếu ở miệng vòm.
  - **Đo thật** tỷ lệ key : tràn tại vách trong, trong không gian tuyến tính: `s5_measure` render riêng đèn lồng / riêng tràn, đọc 7 điểm ngoài vùng bóng. Kết quả **5,6 – 8,3 : 1**, đạt ngưỡng ≥ 4 : 1. Không điểm nào nằm trong ±5 % quanh ngưỡng. Phóng đại bóng theo hình học: đèn → người 2 m, đèn → vách 3 m, nên bóng lớn gấp 1,5 lần.
- **s1.** Trời chạng vạng thủ tục làm IBL (PMREM), có dải mây mỏng bắt hồng. Ánh hồng cuối trời là đèn hướng thấp phía tây, jitter rộng, bóng rất mềm, chỉ chạm mái và tầng trên.
  - 4 đèn khí đầu phố đã thắp. Đèn số 4 cạnh Ida là spot có bóng jitter, nên Ida có bóng mềm. 7 đèn còn lại chưa thắp; cột điện và đồng hồ chưa sáng (mặt kính mờ, 12 vạch, 2 kim, không số).
  - Đèn khí ở các phố khác được kiểm tầm nhìn bằng độ sâu GPU. Ngọn nào thấy được thì hiện thành chấm hổ phách + hào quang. Ngọn bị mái che chỉ còn một quầng sương rất nhạt phía trên mái.
- **Ống kính:**
  - DOF thật bằng jitter khẩu độ (đĩa Vogel) trong tích luỹ.
  - s1: khẩu 0,8 m so với cảnh 37 m, cho hiệu ứng tilt-shift "mô hình". Nét ở Ida và đèn số 4; tiền cảnh mái nhà và chân trời nhoè.
  - s5: nét ở nhân vật và vách, đèn lồng tiền cảnh nhoè nhẹ.
- **Tone map:** ACES như post.js nhưng trộn 70 % bản giữ sắc độ ở vùng sáng (`toneGLSL`), để vũng sáng đèn giữ hổ phách thay vì cháy trắng. **Không đổi GRAIN.**

**Lớp 2D:** không dùng overlay. Trong `grade()` chỉ có vignette ống kính tự nhiên, bóng tối hơi lạnh (split-tone nhẹ) và chân đen phim. Hào quang quanh đèn là sprite cộng sáng trong 3D (halation/sương), không phải lớp vẽ tay.

## 2. Thời gian render (1920×1080, SwiftShader, máy 4 vCPU **đang chạy song song 3 hướng**, số bị nhiễu, P cần đo lại tuần tự)

| Khung | 32 mẫu `render_frame_s` | 8 mẫu `render_frame_s` | setup_s |
|---|---|---|---|
| s1_opening | TBD_S1_32 | TBD_S1_8 | TBD_SET |
| s5_shadows | TBD_S5_32 | TBD_S5_8 | |

(Setup gồm dựng cả hai cảnh, PMREM, biên dịch shader, không tính vào khung.)

**So với ngân sách ≤ 2,5 s/khung: VƯỢT RẤT XA** (xem tỷ lệ ở bảng). Đo tay khi tải máy thấp hơn: s5 khoảng 1,6 s/mẫu, s1 khoảng 6–9 s/mẫu ở 1080p. Nguyên nhân chính:
1. **s1:** khoảng 660 k tam giác × 3 lượt (chính + 2 shadow map) mỗi mẫu. Shader mặt tiền/mái thủ tục nặng, chạy trên toàn khung. Khoảng 1 200 sprite hào quang chồng lớp.
2. **s5:** đèn điểm có bóng = 6 lượt cube shadow mỗi mẫu. Shader vôi/đá nhiều octave. RectAreaLight.
3. SwiftShader tốn theo tam giác và fragment. Tôi đã gộp mesh nhân vật (hàng trăm draw call → khoảng 15) và cắt nhà ngoài khung.

**Cách hạ (đề xuất, chưa làm):**
- Bake ánh sáng tĩnh và kết cấu thủ tục ra texture một lần mỗi shot. Kết cấu không đổi theo khung, nên có thể bake ra lightmap/texture atlas.
- s1: nền xa dùng matte painting 2.5D (ảnh render trước chiếu lên tấm); chỉ dựng 3D phố Ostler.
- Tích luỹ tạm thời qua khung (TAA) thay cho 32 mẫu/khung.
- DOF/bóng mềm dùng 8 mẫu + lọc sau.

Ước lượng các cách trên có thể hạ 10–30 lần, nhưng vẫn khó chạm 2,5 s ở 1080p trên SwiftShader CPU. **Cần P quyết lại ngân sách hoặc đổi GPU.**

**Chất lượng ở 8 mẫu:**
- DOF lộ "bóng ma" rời (tiền cảnh s1 thấy rõ 8 bản chồng).
- Bóng mềm có vân bậc thang.
- Dây điện, mép mái lấm tấm răng cưa.
- s5 chịu được hơn s1 vì DOF nhẹ.

## 3. Tự phê bình thẳng thắn

**Còn "CG rẻ tiền":**
- Nhân vật vẫn là khối trụ/cầu trơn của khung chung. Dạ/nỉ có sheen và nhiễu sợi nhưng ở khoảng cách s5 đọc gần như nhựa mờ; đường may gần như không thấy.
- Đá góc (quoin) hai mép khung s5 lặp khối, quá to và đều.
- Đèn lồng s5 nhỏ (đúng model sheet 0,245 m) và vũng sáng sát chân đèn cháy trắng, nên đèn chưa đọc là "thiếc".
- Thành phố nền s1 vẫn là lưới khối nhà giống nhau (đã xoay 19° và thêm cây dạ, khối cao hơn). Mái xa lấp lánh. Dải sương/đồi chân trời phẳng như tấm phông.
- Quảng trường s1 là mảng tối trống ở tiền cảnh. Đồng hồ điện có đúng kích thước 1,2 m nhưng ở 50 m chỉ là một chấm nhỏ, chưa thành điểm nhìn.

**Chưa đúng hoặc đã nới luật:**
- **Vị trí máy quay s5 lệch brief.** Brief muốn máy sau đèn lồng ~1,5 m. Tôi đặt máy ngoài miệng vòm 3,3 m (sau đèn ~4,3 m), FOV dọc 37°. Lý do hình học: với vòm rộng 3,2 m và FOV 35–42°, máy phải lùi ≥ 2,5 m khỏi mặt tường thì mép khung mới thấy được **phố trắng ngoài vòm**. Ở 1,5 m sau đèn, khung chỉ thấy lòng hốc. Hệ quả: đèn lồng là trung cảnh, không còn là tiền cảnh lớn nhoè. **Cần chủ dự án chọn:** giữ "phố trắng ở mép khung" hay "đèn lồng tiền cảnh lớn".
- Nắp đèn lồng không đổ bóng (coi như nắp có lỗ thông hơi). Nếu bật, nắp cắt một vệt tối ngang vách ở độ cao khoảng 2,3–2,6 m, đè lên đỉnh bóng mũ Ida. Đây là một nới lỏng quang học nhỏ, cần duyệt.
- Rung sáng ±4 % của lửa chưa thể hiện: khung tĩnh chỉ đổi grain qua 48 khung. Hào quang đèn đặt lệch 1,2 m về phía máy quay để không bị chính mũ đèn che.
- s1 khó thấy bóng dài của Ida (nhân vật chỉ khoảng 17 px); có bóng nhưng không đọc được ở cỡ này.

**Thiếu để đạt chuyên nghiệp:**
- Mô hình nhân vật chi tiết hơn (nếp dạ, mép vải dày, tay áo gấp), trong phạm vi luật C3.
- Kết cấu vải thật hơn (xơ nổi ở silhouette: shell/fin fur).
- AO thật cho khe nhà và đá.
- Bake ánh sáng.
- Phá lưới nền bằng dựng tay các mảng phố.
- Một lượt chỉnh màu có chủ đích với color script.
- Bụi/xơ dạ bay trong quầng đèn lồng.

## 4. Đã tránh để không giống IP có sẵn

- **Laika / Aardman:** không mặt đất sét, không miệng/má nặn, không vân vân tay. Mắt là chỉ thêu dẹt, không mắt nút hay mắt bi bóng. Chất liệu chủ đạo là dạ, len và thiếc, không phải đất sét hay silicone.
- **Sprite Fright / phim Blender:** không nhân vật cách điệu kiểu "rubber-hose", không rừng nấm, không bảng màu bão hoà.
- **Ice Merchants, Hair Love, Alike, The Flying Sailor:** không dùng nét phẳng 2D đồ hoạ, không bố cục hay nhân vật tương tự. Kiến trúc là thành phố gạch/thạch cao hư cấu, không địa danh, không cờ.
- Không chữ đọc được: không biển hiệu; mặt đồng hồ chỉ có 12 vạch và 2 kim.
- Mọi texture, hình học và ánh sáng sinh bằng mã. Không tải tài sản ngoài. Không dùng font.
- Addon three.js (RoundedBoxGeometry, RectAreaLightUniformsLib) nạp từ `shared/node_modules` có sẵn.

## Việc chờ chủ dự án / P
1. Chọn vị trí máy s5 (mục 3).
2. Duyệt nới lỏng "nắp đèn không đổ bóng".
3. P đo lại thời gian tuần tự và quyết cách hạ ngân sách render.
