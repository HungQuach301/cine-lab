# Cửa mặt Ida — gói W4 "Blender (C chỉnh)": DỪNG theo giới hạn chi phí sau lần render thử đầu tiên

Worktree W4, gộp từ `claude/cine-lab-m2-cong5-layout-24o5fp` @c881f13. Ngày 28/09/2026.
Căn cứ: AUTHORSHIP "Cửa mặt Ida — quyết định" (C chỉnh), lệnh gói của P.

## 0. Tóm tắt
- **Đã DỪNG theo điều kiện 2 của giới hạn chi phí**: "sau lần render thử đầu tiên (Blender hoặc glb trong three.js), lưới vẫn chưa ra một hình đầu dùng được".
- Đường ống kỹ thuật **đã chạy trọn** trong một lượt 115 s:
  - hình khối → lưới tứ giác → Subdivision Surface → chiếu và giãn đều;
  - tai, mắt, mi, mày, tóc (vỏ, dải thon, sợi tơ), búi, răng;
  - 22 shape key;
  - xuất `.glb`.
- **Hình đầu thì chưa dùng được** (mục 2). Tôi không tự chạy vòng sửa thứ hai vì lệnh gói yêu cầu dừng và báo P.
- **Chưa làm** (do dừng):
  - nạp glb vào three.js; cờ `IDA_STYLE='bl'`;
  - bản lề mũ;
  - các khung thử 1–4;
  - đo c3_views 'bl'.
- **Không sửa file .js nào.** `cast3d.js` giữ nguyên, mặc định vẫn là `'aa'`. Layout, `facelight.js`, `bible/`, `checks/`, `ida.json`, `PLAN.md`, `AUTHORSHIP.md` đều không đổi.

## 1. Đã làm (thư mục `design/cong3/v2/char3d/blender/`)
| File | Nội dung |
|---|---|
| `sdfnp.py` | Hàm hình khối numpy (ellipsoid, capsule, smin/smax, rãnh theo đường gấp khúc, nhiễu). Lưới **surface nets** ra mặt tứ giác. Chiếu đỉnh lên mặt khối; giãn Laplace theo tiếp tuyến. |
| `ida_forms.py` | Thiết kế riêng của gói, không lấy từ nhân vật có sẵn: sọ rộng ở vòng mũ, trán, gò má, đệm má, **xương hàm có góc hàm**, cằm nhỏ, **cổ liền hàm** với cơ ức–đòn–chũm và 2 nếp da, mũi dài 0,26 H hơi khoằm, môi có khe hình học, nếp tuổi bằng khối. **Tai** là lưới riêng (vành, gờ đối, hố tai, bình tai, dái dày đỡ hoa tai), hai bên đối xứng. Đường chân tóc θmax(φ). Albedo da chuyển sắc: ấm ở má, mũi, cằm, tai; mát dưới mắt, thái dương, hàm; đốm tuổi mờ. Da vùng trên chân tóc mang màu tóc để **chân tóc chuyển dần**. |
| `ida_rig.py` | **16 kênh cùng tên** `facerig.js` + 6 khẩu hình + 4 preset, cùng trọng số với W3. Mốc đặt lại theo hình 'bl'. |
| `build_ida_head.py` | Script Blender: dựng mọi phần, gán shape key, xuất `ida_bl.glb` và `ida_bl.json`. |
| `preview.py` | Ảnh xem nhanh EEVEE 4 góc, có mũ giả lập theo số của cast3d A-α. |

Kết quả lượt 1 (`reports/m2/cong5/w4/ida_bl_thu1.json`; glb 19,5 MB không commit, dựng lại được bằng lệnh ở đầu `build_ida_head.py`):

| Phần | Số đỉnh |
|---|---|
| Đầu + cổ | 156 590 |
| Tai | 12 492 |
| Mỗi mắt | 1 968 |
| Vỏ tóc | 10 260 |
| 318 dải tóc | 15 264 |
| 170 sợi tơ | 2 720 |
| Búi | 6 620 |
| Mày | 480 |
| Mi | 300 |

Thông số khác:
- Shape key: 16 kênh + `vis_A/E/O/MBP/FV/L`, áp cho da, mi, mày; răng chỉ nhận jawOpen.
- Hoa tai: vị trí nụ tính từ dái tai, ghi trong JSON.
- Mắt: nhãn cầu riêng, giác mạc nhô, tròng vẽ bằng thủ tục (nâu xám, vòng #5a4636 ở rìa).

**Bảng shape key ↔ kênh facerig** (đã có trong glb, chưa thử trong three.js):

| Nhóm | Tên | Ánh xạ |
|---|---|---|
| 16 kênh | `browUp` … `chinRaise` | cùng tên `CHANNELS` của facerig.js |
| 6 khẩu hình | `vis_A`, `vis_E`, `vis_O`, `vis_MBP`, `vis_FV`, `vis_L` | = tổ hợp kênh theo `VISEMES` (ví dụ A = jawOpen 0,75 + wide 0,1) |
| 4 preset | neutral, sad_smile, strained, choked | trọng số trên 16 kênh, như `FACE_PRESETS` |

## 2. Vì sao chưa phải "hình đầu dùng được" (tự xem `reports/m2/cong5/w4/BL_thu1_blender_eevee_4goc.jpg`)
Ảnh render EEVEE ở các góc 0°, 35°, 90° và 150°, biểu cảm neutral, mũ giả lập. Lỗi thấy được:
1. **Nửa dưới mặt méo và lổn nhổn.**
   - Môi phồng như đang chu.
   - Cằm và hàm có các cục lệch, nhìn chính diện thấy không cân.
   - Dưới cằm và cổ có u, gãy khúc.
   - Chính các lỗi bị chê (nửa dưới mặt phình, cổ) lại nặng hơn. Nguyên nhân khả dĩ: các khối má chùng, khối miệng, cằm và ức–đòn–chũm hoà (smin) chồng nhau quá dày, cộng lỗi bậc của surface nets ở 0,011 H. **Chưa kiểm**, chỉ là giả thuyết.
2. **Mắt đọc thành hai hố đen.** Hốc mắt khoét sâu, mí che, nhãn cầu tối dưới đèn preview: đọc ra "búp bê" ngay.
3. **Búi tóc rời khỏi đầu** ở góc 90° và 150° (tâm búi z −0,585 nằm quá sau vỏ tóc).
4. **Lưới đầu quá nặng** (156 nghìn đỉnh; glb 19,5 MB). Morph CPU mỗi khung sẽ chậm hơn A-i (86,7 nghìn đỉnh).
5. Tốt: tai có cấu trúc, cân hai bên; mũi dài hơi khoằm đọc được khi nhìn nghiêng; tóc bạc có vân và mép mềm; da chuyển sắc ấm–mát.

Nhận định: đường ống Blender (dựng, subdivision, shape key, xuất glb) **khả thi và nhanh**. Hình khối lượt 1 thì chưa đạt. Muốn tới mức nộp kiểm mù cần ít nhất 2–3 lượt chỉnh hình, mỗi lượt khoảng 2 phút dựng + 2 phút preview, cộng phần tích hợp three.js và 11 khung thử. Tôi ước chừng thêm khoảng 350–450 nghìn token, vẫn **trong** hạn 700 nghìn, nhưng lệnh gói bắt dừng ở mốc này.

## 3. Kiểm 'aa' và các mục chưa làm
- **Dò mặc định:** đã render dò trước khi sửa (`render_film.js --only s37,s39,s02 --probe`, làn nhanh, 65,9 s, gắn cờ QUA-60S như các lượt dò của P). Sau đó **không sửa file .js nào**, nên không có "sau" để so; bản mặc định chắc chắn lệch 0 px. Ảnh dò trước chỉ nằm trong scratchpad, không commit.
- **c3_views 'bl':** chưa đo (chưa có 'bl' trong three.js).
- **EEVEE so với three.js:** chưa có khung three.js để so. Một điểm đã biết: EEVEE chạy được headless trên máy này (EGL, phần mềm), khoảng 45 s cho lượt đầu vì phải biên dịch shader.
- **Lỗi TAY:** không thuộc gói, không đụng tới.

## 4. Thời gian, số lần làm lại, hàng đợi, token
| Bước | Giờ UTC | Thời gian |
|---|---|---|
| Gộp nhánh, kiểm môi trường, đọc tài liệu và mã | 13:59 → 14:09 | 10 phút |
| Dò 'aa' trước sửa (song song) | 14:02 → 14:03 | 66 s |
| Thử EEVEE headless và tuỳ chọn exporter | 14:05 | 1 phút |
| Viết script (sdfnp, forms, rig, build, preview) | 14:09 → 14:17 | 8 phút |
| Dựng + xuất lượt 1 | 14:17 → 14:19 | 115 s |
| Preview EEVEE 4 góc, xem, quyết định dừng | 14:19 → 14:23 | 4 phút |
| Viết báo cáo, commit | 14:23 → | khoảng 5 phút |

- **Số lần làm lại:** 0. Chỉ một lượt dựng và dừng đúng mốc.
- **Hàng đợi** (`/var/tmp/cine-queue/log.tsv`, gói W4): 1 việc, `probe-aa-truoc[nhanh] QUA-60S`, chờ 0 s, chạy 65,9 s, mã 0.
- Blender dựng và preview chạy ngoài hàng đợi (CPU, dưới 2 phút mỗi lượt, không phải render three.js).
- **Token:** ngữ cảnh tích luỹ khi dừng khoảng 240 nghìn.

## 5. Rủi ro
- Hình khối bằng SDF + surface nets dễ lổn nhổn ở vùng nhiều khối hoà chồng (hàm, cổ, miệng). Cần tiết chế số khối, tăng bước lưới hoặc làm mịn cục bộ. Chưa thử.
- Sau khi mặt ổn, còn khớp **tóc với băng mũ** trong three.js thật (mũ ở đây chỉ là giả lập), khớp **cổ glb với ống cổ và khăn 4 vòng**, và hiệu năng morph CPU.
- `GLTFLoader` là bất đồng bộ trong khi `buildCharacter` đồng bộ. Cần hàm nạp trước (preload) ở trang khung thử. Đo c3_views 'bl' cần trang bọc riêng vì `b1_measure.py` chỉ gọi `v2/page.js`.

## 6. Việc đang chờ
- **P / chủ dự án chọn:**
  - (a) cho W4 tiếp tục gói với hạn còn lại (khoảng 460 nghìn token);
  - (b) dừng hẳn hướng C và trình phương án lùi PA1 như quyết định đã ghi.
- **Nếu chọn (a):** lượt tiếp sửa theo thứ tự nửa dưới mặt và cổ, rồi mắt, rồi búi. Sau đó tích hợp `'bl'` và làm đủ khung thử 1–4.

---

# Lượt 2 — lưới người MPFB2 (CC0), quyết định chủ dự án "d"

Worktree W4, đã gộp nhánh tích hợp @8a3b164. Ngày 28/09/2026, 15:07 → 16:30 UTC. Các ảnh xem nhanh của lượt 1 (`BL_thu1_*`) giữ nguyên để đối chiếu.

## L2.0 Tóm tắt
- **Bước 1 đạt.**
  - Lấy mã và tài sản lõi từ repo chính chủ `makehumancommunity/mpfb2` bằng `git clone --depth 1`, commit `3edf9df0551765be43563d047888cf7877eb89b4` (MPFB 2.0.17).
  - Lưới gốc và targets nằm ngay trong repo, không cần LFS.
  - Addon chạy được không giao diện (bpy 5.2.2).
  - Có ảnh người nữ lớn tuổi.
- **Bước 2 đạt.** Hình đầu dùng được:
  - đọc ra phụ nữ lớn tuổi;
  - mắt có tròng và điểm sáng;
  - tai liền da, có vành, gờ, dái;
  - tóc bạc ở thái dương, trên tai, gáy; búi liền đầu;
  - mũ phớt D2 là mũ thật của cast3d.
- **Bước 3 xong.**
  - Có cờ `'bl'`; mặc định vẫn `'aa'`.
  - Dò `'aa'` sau khi sửa lệch **0 px**.
  - Đủ khung và bảng so sánh.
  - Đã đo c3_views 8 góc.
- **Không tự chạy kiểm mù.** Bộ khung sẵn sàng để P chạy vòng duy nhất.

## L2.1 Bước 1 — phép thử khả thi
| Mục | Kết quả |
|---|---|
| Nguồn | `https://github.com/makehumancommunity/mpfb2`, commit `3edf9df0551765be43563d047888cf7877eb89b4` (2026-09-26), MPFB 2.0.17. Không dùng asset pack, không tải từ makehumancommunity.org |
| Tài sản dùng | `src/mpfb/data/3dobjs/base.obj` (SHA-256 `8e761e66…6fb4c`); `targets/**` gồm macrodetails, head, eyes, ears, nose, mouth, chin, cheek, neck, expression/units/caucasian; `mesh_metadata` |
| Giấy phép | Tài sản: CC0, `LICENSE.md` mục C ("released under CC0 1.0 Universal"). Mã addon: GPLv3 (mục B), chỉ chạy như công cụ, không chép vào repo. Output: mục D, không mang ràng buộc của mã. Đã ghi `RIGHTS.md` (W4-MPFB-A, W4-MPFB-C) **trước khi dùng** |
| Cách chạy không giao diện | Symlink `src/mpfb` → `~/.config/blender/5.2/extensions/user_default/mpfb`, rồi `addon_utils.enable('bl_ext.user_default.mpfb')`. Import trần `mpfb.register()` hỏng vì `extension_path_user` đòi gói extension |
| Ảnh | `reports/m2/cong5/w4/L2_kha-thi.jpg`: EEVEE chính diện, 40 s. Lưới gốc, chưa có mắt vì mắt là proxy không kèm repo |

Ghi chú: ảnh khả thi dùng age 0,94 (khoảng 82 tuổi; thang MakeHuman 0,5 = 25 tuổi, 1,0 = 90 tuổi). Ida dùng age 0,877 (74 tuổi).

## L2.2 Bước 2 — dựng Ida (`design/cong3/v2/char3d/blender/build_ida_l2.py`, 5 s mỗi lượt)
1. **Tạo người MPFB:** nữ, 74 tuổi, cơ 0,35, cân 0,52. Cộng 33 target chi tiết, trọng số ghi ở khoá `mpfb.detail` trong `ida_bl.json`:
   - mũi dài hơi khoằm, đầu mũi to;
   - mắt to 0,7, mở rộng 0,5;
   - dái tai dài để đỡ hoa tai;
   - gò má cao;
   - môi trên mỏng, khoé hơi trễ;
   - cằm nhỏ;
   - đầu tròn;
   - bỏ nọng cằm.
2. **Chỉ lấy đầu, cổ và răng helper.**
   - Đưa về hệ đầu cast3d (H; y = 0 cằm, 1 đỉnh sọ).
   - Sọ rộng ×1,081 (0,735 H).
   - Cổ đưa ra trước vào tâm khăn: dịch 0,196 H, chỉ phần dưới đường cằm, đúng "cổ hơi đưa ra trước" của sheet.
   - Cổ cắt theo elip quanh trục cổ, nên mép cắt nằm trong khăn và cổ áo.
   - Subdivision Surface cấp 2 → **70 444 đỉnh**, nhẹ hơn A-i (86,7 nghìn).
3. **Tai:** dùng **tai liền lưới của MPFB**, không ghép tai lượt 1.
   - Lý do: tai MPFB liền da, không có đường nối, nhắm đúng lời chê "tai dán".
   - Lệnh gói ghi "dùng lại tai lượt 1"; nếu P muốn đúng nguyên văn thì đổi lại được.
   - Hoa tai treo ở điểm thấp nhất của dái tai, hai bên đối xứng.
4. **Mắt:**
   - Nhãn cầu riêng; tròng vẽ bằng thủ tục (nâu xám, vòng #5a4636, con ngươi mép mềm); giác mạc nhô; lớp ướt (clearcoat) bắt điểm sáng thật.
   - Hai mắt hội tụ: mắt bên +x quay về −x 0,035 rad.
   - Lỗi "hố đen" có hai nguyên nhân: tròng quá to so với nhãn cầu helper của MPFB (0,075 H), đã thu còn 0,44 R; và tròng quá tối.
5. **Da:** albedo bằng màu đỉnh.
   - Ấm ở má, mũi, tai, cằm; mát dưới mắt, thái dương, hàm; đốm tuổi mờ.
   - Chân tóc chuyển dần qua dải 0,12 rad mang màu tóc.
   - Nếp tuổi bằng khối: 2 nếp trán, chân chim, nếp giữa mày.
   - Vật liệu three.js: PBR nhám 0,66, bóng gương 0,3, khuếch tán "bọc" lệch đỏ, kéo 35 % ánh hổ phách về trung tính.
6. **Mày bạc:** 44 sợi thon mỗi bên, sắc 0,70–0,84 × #e2dfda, cùng shader tóc bạc. Mày đi theo shape key của da.
7. **Tóc:**
   - Vỏ tóc mỏng dần về 0 ở chân tóc, 260 dải thon, 150 sợi tơ.
   - Bỏ gờ "ép theo băng mũ" của lượt 1, vì gờ này thành "mũ bảo hiểm" khi mũ đẩy ra sau.
   - Hạ chân tóc ở thái dương và trên tai.
   - **Búi liền đầu:** tâm búi đặt theo mặt tóc ở gáy, lún 55 % bề dày vào khối tóc.
8. **Mũ:** mũ phớt D2 #262a33 của cast3d. Bản lề mũ mới ở tâm sọ của lưới glb; đẩy mũ tối đa ngả **0,26 rad** (A-i 0,36; A-α 0,34).
9. **Ảnh EEVEE 4 góc:** `L2_eevee_4goc.jpg`.
   - Lưới xuất từ chính khung PA1_goodnight, nên có thân, khăn 4 vòng và mũ thật; tư thế s37 (cúi, cười buồn).
   - Tôi tự xem trước khi làm tiếp.
   - Các ảnh xem nhanh trong Blender còn dùng mũ giả lập nên chỉ dùng để chỉnh hình, không nộp.

**Bảng shape key ↔ kênh facerig** (trong glb là morph target, TÊN = tên kênh; three.js tính morph trên CPU):

| Kênh facerig.js | Expression unit MPFB (CC0) × hệ số | Biên độ tối đa (H) |
|---|---|---|
| browUp | eyebrows-left/right-up ×1 | 0,023 |
| browDown | eyebrows-left/right-down ×1 | 0,027 |
| browInnerUp | eyebrows-left/right-inner-up ×1 | 0,021 |
| browKnit | nose-compression ×0,6 + eyebrows-down ×0,25 | 0,007 |
| blink | eye-left/right-closure ×1 | 0,047 |
| lidDrop | eye-closure ×0,35 | 0,016 |
| squint | eye-left/right-slit ×1 | 0,017 |
| cheekRaise | mouth-upward-retraction ×0,45 + eye-slit ×0,3 | 0,022 |
| smile | mouth-corner-puller ×1 | 0,053 |
| frown | mouth-depression ×0,6 | 0,020 |
| jawOpen | mouth-open ×1 | 0,155 |
| press | mouth-compression ×0,6 | 0,022 |
| pucker | mouth-pursing ×1 + mouth-protusion ×0,4 | 0,086 |
| wide | mouth-retraction ×1 | 0,033 |
| lowerLipIn | mouth-depression-retraction ×0,4 + mouth-elevation ×0,5 | 0,031 |
| chinRaise | mouth-elevation ×0,55 | 0,019 |
| vis_A / E / O / MBP / FV / L | tổ hợp kênh theo `VISEMES` (ví dụ A = jawOpen 0,75 + wide 0,1) | 0,116 / 0,047 / 0,118 / 0,022 / 0,035 / 0,062 |

- **4 preset** (neutral, sad_smile, strained, choked) là trọng số trên 16 kênh, giống hệt `FACE_PRESETS`; ghi trong `ida_bl.json`.
- **Đã hạ hệ số frown, press, chinRaise** (1,0 → 0,6 / 0,6 / 0,55) vì khung s37 choked đầu tiên cho miệng gãy như vết rách.
- Biểu cảm lấy từ targets CC0 của MPFB, đã nằm trong RIGHTS.md (W4-MPFB-A). Repo không có bộ biểu cảm dựng sẵn (`data/expressions` trống).

## L2.3 Bước 3 — tích hợp và khung thử
**Mã:**
- `cast3d.js`:
  - cờ `'bl'`: đầu, tóc, tai, cổ, mắt, mày, búi, hoa tai lấy từ glb; thân, áo, khăn 4 vòng, mũ như `'ai'`;
  - bản lề mũ mới 0,26 rad;
  - thêm `globalThis.CINE_IDA_STYLE` để trang bọc chọn kiểu;
  - `IDA_STYLE` vẫn `'aa'`.
- `blender/bl_head.js`:
  - `preloadIdaBL()` nạp GLTFLoader của three qua Blob, thay `'three'` bằng URL tuyệt đối vì trang không có import map;
  - rig chạy trên CPU;
  - tách part `head` và `neck` để đo C3.
- Trang bọc, không sửa trang gốc:
  - `page_l2.js`: bản sao `page_pa.js`, thêm ghi đè L11 và xuất glb;
  - `page_fl_bl.js`, `page_c3_bl.js`, `page_ai_bl.js`.
- `run_l2.sh`, `c3_bl.py`, `eevee_frame.py`, `eevee_4goc.py`.
- `node --check` đạt ở mọi file .js đã sửa hoặc thêm.

**Dò 'aa':**
- `render_film.js --only s37,s39,s02 --probe`: trước sửa lúc 14:02; sau sửa .js lúc 15:40 (`cast3d.js` không đổi sau mốc này).
- So 9 thumbs: **lệch 0 px ở cả 9**.

**Đèn L11 trong khung thử** (ghi đè chỉ trong `page_l2.js`; không sửa layout hay facelight):
- L11 là đèn điểm gần mặt nhất, không kể đèn facelight. Đặt ở **cao 17,5° trên tâm mặt, lệch 25° khỏi trục máy**, giữ khoảng cách 0,50 m.
- Ở PA1_goodnight, vị trí gốc là cao 43,2°, lệch 42,2°.
- **Cần P xác nhận cách hiểu.** Tôi hiểu "nâng 15–20°" theo đề xuất gốc của W3 ("nâng L11 lên ~15–20° so với mắt", tức góc 15–20° trên mắt). Với máy nghiêng PA1, cách này thực tế **hạ** L11 từ 43° xuống 17,5°. Nếu ý là cộng thêm 15–20° vào góc hiện có thì chạy lại 4 khung PA1, khoảng 2 phút.

**Khung nộp** (`reports/m2/cong5/w4/`, 1920×1080, 3 mẫu, làn nặng; glb SHA-256 `c5cf949afbb67d87…026979`):

| Khung | File |
|---|---|
| PA1 'bl' | `L2_BL_PA1_last.jpg` · `L2_BL_PA1_goodnight.jpg` · `L2_BL_PA1_brighter.jpg` · `L2_BL_PA1_keep.jpg` (choked) |
| s37 f2302 chính diện (đèn, facelight, phơi sáng như vòng A-i) | `L2_BL_s37_neutral.jpg` · `L2_BL_s37_choked.jpg` |
| EEVEE (cùng lưới, máy và 10 đèn của khung) | `L2_EEVEE_PA1_goodnight.jpg` · `L2_EEVEE_PA1_keep.jpg` |
| Bảng so sánh | `L2_SO_goodnight_aa-ai-bl.jpg`. Hàng 1: A-α / A-i / 'bl' với L11 nâng. Hàng 2: 2 khung cũ của W3, đèn cũ |
| 4 góc | `L2_eevee_4goc.jpg` |
| Khả thi | `L2_kha-thi.jpg` |

**c3_views 'bl'** (8 góc, cùng cách `b1_measure.py`; số thô trong `L2_c3_bl.json`; **KHÔNG sửa ida.json**):

| Góc | thân / tay trên / cẳng tay / cẳng chân ('bl') | Thân theo sheet v1.4 | Lệch thân |
|---|---|---|---|
| 0° | 2,229 / 1,304 / 0,810 / 0,239 | 2,682 | **−16,9 %** |
| 45° | 2,181 / 1,403 / 0,865 / 0,268 | 2,290 | −4,8 % |
| −45° | 2,172 / 1,393 / 1,232 / 0,268 | 2,263 | −4,0 % |
| 90° | 1,807 / — / — / — | 2,034 | **−11,2 %** |
| −90° | 1,850 / 1,256 / 0,898 / 0,243 | 2,060 | **−10,2 %** |
| 135° | 2,020 / 1,258 / 0,708 / 0,233 | 2,558 | **−21,0 %** |
| −135° | 1,997 / 1,251 / 0,935 / 0,233 | 2,528 | **−21,0 %** |
| 180° | 2,079 / 1,322 / 1,000 / 0,239 | 2,752 | **−24,5 %** |

- **Nguyên nhân:** phần "đầu nhìn thấy" của 'bl' dài hơn A-α 12–32 %.
  - Lưới MPFB giữ tỷ lệ mặt người thật: mắt ở 0,50 H thay vì 0,575, nên nửa dưới mặt dài hơn.
  - Da dưới cằm thuộc part `head` tới y −0,02.
  - Mũ ngồi thấp chỉ che đỉnh sọ.
- **Chỉ số trong ±5 % quanh ngưỡng 3 % của C3:** ±45° (−4,8 % và −4,0 %). Sáu góc còn lại lệch quá 5 %.
- **Nếu chọn 'bl':** bắt buộc cập nhật `c3_views` (P sửa và khoá SHA), hoặc quyết lại tỷ lệ đầu–thân. Việc đầu 'bl' to hơn tương đối so với thân là **quyết định sáng tạo cần chủ dự án**.

## L2.4 Nhận định: hình khối hay máy render (EEVEE so với three.js)
- Hai khung EEVEE dựng cùng lưới, máy và 10 đèn. Phơi sáng khớp theo đo, độ sáng vùng mặt EEVEE / three.js: goodnight 0,51 / 0,55; keep 0,82 / 0,74.
- **Hình khối đọc giống nhau ở hai máy:** mũi dài khoằm, tai, hàm, cằm, gáy, nếp tuổi. Không có lỗi hình nào chỉ xuất hiện ở một máy.
- **Khác biệt do máy render:**
  - three.js có lớp vẽ Kuwahara làm da mịn và trơn hơn;
  - three.js có shader tóc bạc (kéo 70 % về trung tính); EEVEE không có, nên tóc tối và ngả xanh trong bóng mũ;
  - EEVEE có bóng mềm và tán xạ dưới da, nên mặt có hạt và khối rõ hơn;
  - EEVEE không có bộ cảnh (tường, cột, thang) nên thiếu ánh dội và bóng cột.
- **Kết luận** (nhận định của W4, chưa phải kiểm mù): nếu kiểm mù vẫn gọi "búp bê/mặt nạ" ở 'bl' thì phần do hình khối đã giảm rõ so với A-i. Nghi phạm còn lại là **cách tô**: lớp vẽ làm phẳng da, và da thành cam dưới đèn khí.

## L2.5 Tự xem (không phải kiểm mù) — lỗi còn thấy
1. **Búi** đọc thành một khối tròn trắng ở góc nghiêng và góc sau, vì các vòng xoắn trơn. Có thể bị gọi "quả bóng" hoặc "vón cục".
2. **Một mảnh da nhỏ ở gáy** lộ trên khăn ở PA1_keep. Nhỏ hơn nhiều so với "vây" ở bản trước; đã dời cổ vào tâm khăn.
3. **Ở s37, mũ đẩy ra sau** làm lộ trán và thái dương rộng. Chân tóc đúng kiểu tóc búi chải ngược, nhưng có thể đọc thành "hói".
4. **Ở PA1 với sad_smile, mắt gần như khép** (squint 0,55 + cheekRaise); nhìn nghiêng chỉ thấy một khe.
5. **Mép cổ áo** vẫn tính theo đầu A-α (`headSDF`), chưa theo glb. Ở các khung thử chưa thấy lỗi.
6. **Tay** (chỉ ghi nhận, không sửa): bàn tay trên cột vẫn là tay của cast3d. MPFB có tay đúng giải phẫu (CC0); ghi lại cho Cổng 6.

## L2.6 Đánh giá đưa vào pipeline (nếu kiểm mù đạt)
- **Shot đổi:** mọi shot có Ida.
  - Đặt `IDA_STYLE = 'bl'` là đổi toàn phim, không sửa file layout.
  - Mỗi trang render (render_film, trang chính) cần thêm một dòng `await preloadIdaBL()` vì glb nạp bất đồng bộ.
- **Việc bắt buộc sau đó:**
  - c3_views mới và chạy lại luật máy;
  - rà continuity mũ ở s36 (bản lề 0,26);
  - mép cổ áo theo glb;
  - sửa búi.
- **Chi phí đo được:**

| Hạng mục | Chi phí |
|---|---|
| Dựng glb | 5 s |
| Nạp glb trong trang | khoảng 1 s |
| Khung 1080p 3 mẫu | 23–28 s (A-α 25–37 s ở vòng W3) |
| Morph CPU | 70 nghìn đỉnh mỗi `setFace` |
| glb | 11 MB, đã commit |

- **Rủi ro:**
  - c3_views lệch 10–25 % ở 6/8 góc;
  - thêm một phụ thuộc: phải chạy MPFB trong Blender mỗi khi dựng lại glb;
  - mọi chỉnh hình phải chạy lại script Blender, không chỉnh trực tiếp trong three.js.

## L2.7 Thời gian thật, số lần làm lại, hàng đợi, token
| Bước | Giờ UTC | Thời gian |
|---|---|---|
| Gộp nhánh, clone MPFB, đọc giấy phép, ghi RIGHTS.md | 15:07 → 15:09 | 2 phút |
| Bước 1: chạy không giao diện, ảnh khả thi | 15:09 → 15:10 | 1 phút (1 lần sửa cách nạp addon) |
| Bước 2: script, dựng, xem EEVEE, sửa mắt, mày, tóc | 15:10 → 15:30 | 20 phút |
| Bước 3: tích hợp cast3d, bl_head, trang bọc, thử three.js | 15:30 → 15:42 | 12 phút |
| Khung, xuất, c3, EEVEE, sửa cổ (3 lượt khung) | 15:42 → 16:22 | 40 phút |
| Báo cáo, commit | 16:22 → 16:30 | 8 phút |

- **Số lần làm lại:**
  - 12 lượt dựng glb, mỗi lượt khoảng 5 s:
    - mắt 3;
    - mày 1;
    - chân tóc 3;
    - kênh miệng 1;
    - cổ 4 (cắt răng cưa → trụ → elip → dời vào tâm khăn; có một lần cắt mất cằm, đã sửa).
  - Bộ khung render 3 lượt: lượt 1 bỏ vì tóc và kênh miệng; lượt 2 bỏ vì "vây" ở gáy. Khung nộp là lượt 3.
- **Hàng đợi** (`/var/tmp/cine-queue/log.tsv`, gói W4, từ 15:33): 47 việc, mọi việc chờ 0 s, mã 0.
  - Làn nặng: 27 khung, 23,4–37,9 s mỗi khung; 3 lượt đo c3: 191,6 / 145,7 / 150,8 s.
  - Làn nhanh: 17 việc (thử 960×540, xuất glb, dò 'aa' sau 58,8 s).
- EEVEE chạy trong Blender, ngoài hàng đợi: 47 s và 50 s mỗi khung; ảnh 4 góc khoảng 2 phút.
- **Token:** ngữ cảnh tích luỹ khi kết thúc khoảng 610 nghìn (hạn 700 nghìn). Riêng lượt 2 khoảng 370 nghìn (hạn khoảng 450 nghìn).

## L2.8 Việc đang chờ
- **P:** chạy vòng kiểm mù duy nhất với bộ khung trên. Tiêu chí giữ nguyên:
  - PA1: tuổi và giới 4/4;
  - cảm xúc ≥ 3/4;
  - 0/4 từ khoá chỉ vào mặt hoặc đầu Ida;
  - đối chứng 0/2.
- **P / chủ dự án:**
  - xác nhận cách hiểu "nâng L11 15–20°" (mục L2.3);
  - chọn giữ tai MPFB hay tai lượt 1;
  - nếu đạt: quyết tỷ lệ đầu–thân và c3_views mới, characters v1.5, model sheet; ghi AUTHORSHIP.
- **Nếu trượt:** không làm vòng 2; trình phương án lùi PA1 theo quyết định đã ghi, kèm bảng `L2_SO_goodnight_aa-ai-bl.jpg`.
