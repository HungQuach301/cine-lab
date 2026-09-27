# Hướng B — "Ink & Lamplight" (đồ hoạ mực, sáng tối phân tầng)

Cổng 3 vòng 1 · phiên xưởng hướng B · 27/09/2026. Trạng thái: **đề xuất, chưa duyệt**.

Nộp: `scene.js` (trang cho `shared/render_still.js`), `out/s1_opening.png|.rgb|.timing.json`, `out/s5_shadows.png|.rgb|.timing.json` (32 mẫu, 48 khung), `out8/*.png|.timing.json` (8 mẫu, 1 khung). Mỗi file `.rgb` nặng 299 MB (1920×1080×3×48): để nguyên trong `out/`, không gửi qua giao diện.

Lệnh render (đúng như brief):
```
cd design/cong3 && PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers node shared/render_still.js --page dir-B/scene.js --frame s5_shadows --out dir-B/out --samples 32 --frames 48
```
Tuỳ chọn gỡ lỗi qua `--args` (không dùng khi render chính thức): `{"only":"s1_opening"}` chỉ dựng một cảnh; `inkN`, `noInk`, `noShadow`, `cam`, `dbgIda`.

## 1. Thiết kế

**Ngôn ngữ hình khối.** Góc cạnh, vuốt nhọn, kiến trúc nghiêng nhẹ kiểu tranh minh hoạ sách: mỗi ngôi nhà được xô (shear) ngẫu nhiên ±1,5° ngang và hơi ngả ra phố; mái dốc 46–62°, đầu hồi nhọn quay ra phố (≈40% số nhà), cửa sổ mái nhọn, ống khói mảnh và cao, nắp loe. Cửa sổ cao, hẹp. Hốc cửa bốc hàng là **vòm nhọn** (chân vòm 2,2 m, đỉnh 4,0 m), vành đá vòm chia 19 viên, đá góc so le. Thành phố xa là các **lớp bìa cắt** (4 dải chân trời ở 0,8–2,3 km, mái nhọn, ống khói, tháp chuông) mờ dần vào sương tím. Nhân vật giữ nguyên khung xương và tỷ lệ của `shared/cast.js` (luật C3); chỉ đổi vật liệu và thêm một lớp tóc phủ nửa sau sọ (gắn khớp đầu, nằm trong đường bao) để nhìn từ lưng đọc ra gáy chứ không ra mặt.

**Chất liệu.** Tô phẳng lượng tử hoá: tổng độ rọi (mọi nguồn, kể cả bóng đổ và suy giảm theo khoảng cách) được lượng tử hoá theo **log-độ rọi, bậc ~1 stop**, nên mỗi mặt vật liệu hiện 2–3 tầng phẳng; mép tầng khử răng cưa bằng `fwidth`. Tầng sáng nhân sắc ấm, tầng tối nhân sắc chàm lạnh. Kết cấu vẽ bằng mực theo toạ độ thế giới (tắt dần khi mạch nhỏ hơn ~3 px): gạch quét vôi loang, viên đá vòm, đá lát hốc, đá hộc lát phố, hàng ngói, nét tóc toả từ búi tóc Ida.

**Viền mực.** Hậu kỳ riêng: G-buffer (pháp tuyến bát diện + độ sâu tuyến tính + mã vật liệu) → dò cạnh 4 hướng: Laplace của nghịch đảo độ sâu (bắt đường bao, không bắt mặt phẳng nghiêng), góc pháp tuyến (nếp gấp), đổi vật liệu (biên màu). Độ dày nét = K / độ sâu (gần đậm, xa mảnh), biến thiên ±28% theo nhiễu; đường nét "run tay" bằng dịch chuyển nhiễu tần thấp ±0,8–0,9 px; đứt nét nhẹ kiểu bút khô; nét mờ dần theo sương. Mực pha 30% màu nền (mực in đè lên màu). Tích luỹ theo jitter dưới điểm ảnh: 4 lượt ở 32 mẫu, 1 lượt ở 8 mẫu.

**Bảng màu (hẹp, có chủ đích).**

| Vai trò | Hex |
|---|---|
| Mực viền, vạch và kim đồng hồ | `#161a2b` |
| Chàm đêm: thiên đỉnh / mái đá phiến | `#2e3868` / `#3a3d58` `#34384e` `#413b54` `#2f3448` `#453f5c` |
| Tím chạng vạng: trời tầng giữa, sương xa | `#6c5e9e`, `#b27f9e` |
| Hồng chân trời (chỉ ở trời, mây) | `#eaa697`, mây `#f0a898` / `#7e6597` |
| Trắng xương: vôi mặt tiền / vách trong hốc | `#e9e6de` / `#f0e8d6`; tường nhà phố `#b3aca4` `#a39fb0` `#9a95aa` `#bab2a6` `#c4bcb0` |
| Trắng lạnh ánh điện (nguồn tràn cảnh 5) | `#d9e3ef` |
| Hổ phách: đèn khí / đèn lồng / kính / lõi lửa / quầng | `#ffa04a` / `#ffb366` / `#ffb04a` / `#fff1cc` / `#ff9a3a`, `#ffd29a` |
| Nhấn 1 — đỏ gạch, **chỉ áo len Cas** | `#a2412f` (quả bông `#b8452f`) |
| Nhấn 2 — xanh rêu, **chỉ áo khoác Ida** | `#58663c` |

Đỏ gạch và xanh rêu không dùng ở kiến trúc (thành phố chỉ chàm – tím – xương – hổ phách) để hai nhân vật là hai điểm màu duy nhất.

**Ánh sáng và bóng.**
- Cảnh 1: trời chạng vạng (bán cầu tím trên, chàm dưới) + dư quang hồng thấp từ phía tây + 4 đèn khí đã thắp (điểm, suy giảm 1/d²) — tất cả tính giải tích trong shader. Suy giảm 1/d² qua lượng tử hoá thành **vòng hổ phách đồng tâm** trên mặt đá và mặt tường: "tâm hổ phách, giữa là khoảng tối". Đèn 5–11 tắt, 6 cột điện chưa bật (tấm kính mờ chữ nhật nhạt), đồng hồ quảng trường chưa sáng (mặt kính nhạt, 12 vạch, 2 kim, không số). Đèn khí các phố khác: chấm hổ phách có quầng mượt.
- Cảnh 5: nguồn duy nhất trong hốc là đèn lồng (`buildLantern`), đèn điểm có bóng, **jitter 3 vị trí trong khoảng kính 12 cm** theo mẫu tích luỹ; mỗi mẫu bóng cứng (BasicShadowMap) nên rìa bóng thành **mềm hai bậc** (1/3, 2/3). Phân bố sáng của đèn lồng: nắp thiếc chắn tia hướng lên trên ~49°, đế chắn tia thẳng xuống → vòm trần tối, vách sau sáng thành vùng. Chỉ hai người đổ bóng (đèn lồng, thang, móc sắt không đổ bóng). Ánh điện ngoài vòm: tràn phẳng, gần như không hướng, **không bóng đổ**; bị che trong hốc theo hàm tắt mũ theo độ sâu (còn ~2% ở vách sau). Có hắt sáng ấm yếu từ đèn lồng. Rung sáng ±4%: khung tĩnh lấy một pha (−1,5%).
- **Đo tỷ lệ key : tràn tại vách trong** (ảnh `out/s5_shadows.png`, độ chói tuyến tính sau tone): vách sáng 0,42 / trong bóng 0,012 ≈ **34 : 1** (giải tích: key ≈ 1,28, tràn điện + hắt ≈ 0,035 → ~37 : 1). Ngưỡng 4 : 1 đạt, không nằm trong vùng ±5%. Bóng phóng đại 3 m / 2 m = **1,5×** đúng hình học.

**Lớp 2D (trong `gradeGLSL`, tĩnh theo khung).** Giấy: răng giấy + loang thô + thớ sợi nghiêng (nướng một lần vào texture lúc setup, biên độ ±7%); chấm lưới in 45°, chu kỳ 5,5 px, chỉ ở vùng tối (L < 0,26), sâu 20%; tối mép giấy nhẹ; viền mực. Grain và dither của `shared/post.js` giữ nguyên, không đổi. Mọi dải chuyển mượt (trời, sương, quầng đèn) đi qua đường ống chung có dither/grain. Tone map riêng: tuyến tính tới 0,78 rồi vai mềm, giữ sắc độ (để hex bảng màu ra đúng), chỉ bạc về trắng khi rất sáng (lõi lửa).

## 2. Thời gian render (1920×1080, 4 vCPU, SwiftShader)

Đo khi máy chạy 3 hướng song song (load 4,5–8,8 trên 4 lõi) → **số nhiễu, phóng đại**; P cần đo lại tuần tự.

| Khung | 32 mẫu, `out/` (load 5,8–6,6) | 8 mẫu, `out8/` (load 6,2–6,6) | 8 mẫu, lần đo trước (load 7–8,8) |
|---|---|---|---|
| s1_opening | 29,4 s | 10,8 s | 14,3 s |
| s5_shadows | 21,4 s | 9,2 s | 9,9 s |
| Tham chiếu: `model-sheet` cas_pose_half_raised, 8 mẫu | — | 2,3 s (đo ngay sau, cùng tải) | lúc máy nhẹ hơn: 1,5 s |

Quy đổi theo tham chiếu đo cùng lúc: s1 ≈ 4,7×, s5 ≈ 4,0× trang model sheet. Ước lượng chạy tuần tự: **s1 ~5–7 s, s5 ~4–6 s ở 8 mẫu → vượt ngưỡng 2,5 s/khung khoảng 2–3 lần.** Pass cuối cho mỗi khung grain thêm: 0,3–0,4 s.

Chất lượng ở 8 mẫu so với 32: mảng phẳng và viền mực gần như không đổi (tô phẳng không cần nhiều mẫu); khác biệt là viền mực chỉ 1 lượt jitter nên răng cưa nhẹ ở nét chéo mảnh, rìa bóng hai bậc vẫn đủ (3 vị trí đèn), quầng và dải trời không đổi.

Cách hạ (chưa làm hết): (a) 4 mẫu là đủ cho hướng này (3 vị trí đèn + khử răng cưa); (b) đèn lồng tính giải tích + một shadow map 2D thay cube map (hiện 3 lần render 6 mặt); (c) nướng thêm ánh sáng tĩnh của nhà gần theo đỉnh như đã làm cho phố xa; (d) viền mực nửa độ phân giải rồi nâng cấp có định hướng. Đã làm: trời vẽ một lần mỗi khung thay vì mỗi mẫu; phố xa nướng màu theo đỉnh trên CPU; nhà xa rút còn 14–24 tam giác; đèn cảnh 1 tính giải tích thay vòng đèn three.js; giấy nướng sẵn; bóng đổ chỉ render lại khi vị trí đèn đổi (3 lần/khung).

## 3. Tự phê bình

**Còn "trông như CG rẻ tiền":**
- Nhân vật: khối trụ, cầu của rig chung đọc như búp bê gỗ; tô phẳng + viền làm lộ rõ hơn. Cần hình khối vẽ tay (lớp phủ 2D hoặc mô hình riêng theo hướng) — ngoài phạm vi vòng này vì luật C3.
- Vòng sáng đồng tâm quanh đèn khí (cảnh 1) quá đều, hơi giống sơ đồ; hoạ sĩ thật sẽ vẽ lệch, vỡ theo mặt đá.
- Rìa bóng hai bậc (cảnh 5) đọc hơi giống "viền dán" quanh bóng hơn là bán dạ; bóng lõi chàm hơi lạnh so với hốc ấm.
- Quầng đèn khí các phố xa không bị mái che (tắt kiểm tra độ sâu) nên vài chấm "nổi" trên mái; chấp nhận như sáng loang trong sương, nhưng không đúng tuyệt đối.
- Chấm lưới và giấy là mẫu tĩnh theo khung: khi máy quay chạy sẽ thành "lưới dính màn hình"; phải gắn vào không gian vật thể hoặc chỉ dùng ở shot tĩnh.
- Viền mực ở dải chân trời xa và mái xa vẫn hơi nhiều nét nhỏ.

**Chưa đúng brief / luật thế giới:**
- Cảnh 5, **máy quay lùi xa hơn brief**: brief ghi sau đèn lồng ~1,5 m (tức 0,5 m ngoài miệng vòm); ở vị trí đó mép khung nằm trọn trong hốc (FOV ngang 66° chỉ phủ ±0,3 m ở miệng vòm), không thể thấy "phố trắng ở mép khung". Tôi đặt máy 1,35 m cao, **6,2 m sau đèn lồng (5,2 m ngoài miệng)**, FOV dọc 38°, ngước 3,5°: thấy vòm, mặt tiền trắng hai bên, dải đá phố dưới đáy. Cần chủ dự án chọn: giữ khung này, hay đổi hốc/đèn để đúng số đo brief.
- Cảnh 1 dùng **dịch ống kính dọc** (trục chúc 21°, khung dịch lên) để có ~24% trời; nếu hiểu "chúc 20–30°" là hướng giữa khung thì khung này chúc ~12°.
- Phân bố sáng đèn lồng (nắp chắn tia lên) là giả định của tôi, hợp quang học nhưng chưa có trong luật.
- Con phố cong chỉ thấy rõ ~6 ngọn đầu; đoạn cuối và tường nhà kho bị mái che (nhìn từ 37 m không thấy lòng phố cắt ngang). Ida ở ngọn 4 chỉ cao ~15 px.
- Rung sáng ±4% không thể hiện được trong 48 khung (khung tĩnh chỉ đổi grain).

**Còn thiếu để đạt mức chuyên nghiệp:** hình khối nhân vật vẽ tay; nét mực có độ nhọn đầu–cuối nét (hiện là dải đều); vỡ nét theo chất liệu; nhiều tầng không khí hơn ở trung cảnh cảnh 1; chi tiết đời sống (dây phơi, biển hiệu không chữ, vết ố tường); ánh sáng hắt màu giữa các mặt; thời gian render trong ngân sách.

## 4. Đã tránh để không giống IP có sẵn

- *Ice Merchants* (phim tham chiếu, bảng màu hẹp phẳng **không viền**): hướng B **có viền mực và giấy in**, bảng màu chàm–tím–hổ phách thay vì bảng màu của phim; không dùng bố cục vách đá, nhà treo hay nhân vật cha–con của phim.
- Mignola/Hellboy: không dùng mảng đen đặc khối lớn, không bóng đen tuyền; bóng tối là chàm có chấm lưới và bậc hắt.
- *Klaus*: không dùng ánh sáng thể tích mềm kiểu 2D-được-tô-sáng; ánh sáng ở đây là mảng lượng tử hoá cứng.
- *Hair Love, Alike, The Flying Sailor, Sprite Fright*, Laika, Aardman, Ghibli, Pixar: không mượn thiết kế nhân vật (dùng rig chung của Cine Lab), không mượn kiến trúc nhận diện, không chữ, không cờ, không biển hiệu. Thành phố, đồng hồ, đèn và cột điện đều dựng bằng mã theo `bible/world-rules.md`.
- Không tải tài sản ngoài: mọi hình, kết cấu, giấy đều sinh bằng mã; không font, không texture.
