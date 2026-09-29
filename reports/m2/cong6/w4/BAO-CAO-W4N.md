# Cổng 6 — gói W4 nhân vật (W4N): mắt, mũ, tay MPFB, cổ lật cao Cas, nghiên cứu thân MPFB

- Worktree W4 (phiên mới), đã gộp nhánh tích hợp `claude/cine-lab-m2-cong5-layout-24o5fp` @b0c4844.
- Chạy 29/09/2026, 01:33 → khoảng 02:25 UTC.
- Căn cứ: AUTHORSHIP "Cổng 6 — mở"; CONG-6-MO.md mục 2 và 4; MAT-IDA-BLENDER-L3.md; nháp v1.6 mục 5; lệnh gói của P.
- **Không tự chạy kiểm mù.**

## 0. Tóm tắt
- **Qua điều kiện dừng.** Cả bốn mục mắt, mũ, tay, cổ Cas đều **sửa rõ rệt**, có ảnh trước/sau (mục 2).
  - Tôi tự xem ảnh EEVEE 4 góc Ida và Cas, và ảnh three.js s37 chính diện. Kết quả tự xem ở mục 2; đây không phải kiểm mù.
- **Mặc định:**
  - Ida 'bl' đổi hình (mắt, mũ), đúng như lệnh cho phép.
  - Cas vẫn 'v14'. Tay vẫn tay cũ.
  - Cas 'bl' và tay MPFB nằm sau cờ.
- **Dò layout:**
  - s24c lệch **0 px** ở cả 3 khung.
  - s02 và s42 có Ida ở hậu cảnh. Mọi điểm lệch nằm trong vùng quanh đầu Ida; vùng Cas lệch 0 px (mục 3).
  - s05, s37, s39 đổi hình do Ida.
- **Tệp đã khoá SHA không bị ghi đè:** `ida_bl.glb`, `ida_bl.json` v1.5 giữ nguyên. Ida v1.5.1 là tệp mới `ida_bl_v151.*`.
- **RIGHTS.md:** ghi dòng **W4-MPFB-A3** (tay MPFB, rig/weights `default`, thân cho nghiên cứu) và commit **trước** khi dùng (commit b89ebe5).

## 1. Cách bật cờ
| Cờ | Mặc định | Bật |
|---|---|---|
| `IDA_STYLE` | `'bl'`, nay dùng `ida_bl_v151.glb` | — |
| `CAS_STYLE` | `'v14'` | `casStyle:'bl'` hoặc `globalThis.CINE_CAS_STYLE='bl'` (như cũ) |
| **`HANDS_STYLE`** (mới) | `'v14'` (tay cũ) | `buildCharacter(sheet, { handsStyle: 'bl' })` hoặc `globalThis.CINE_HANDS_STYLE='bl'`. Phải `await preloadHandsBL()` trước khi dựng; `page.js` đã có dòng nạp khi cờ bật. Trang thử: `"handsStyle":"bl"` trong `--args` của `page_l2.js` |
| API mới | — | `ch.gripPoint(s)`: điểm nắm, thế giới. `ch.reachGrip(s, {point, axis, radius})`: IK vai–khuỷu đưa lòng tay tới vật hình trụ |

## 2. Danh sách sửa a–e kèm bằng chứng

### a. Mắt Ida và Cas (bằng chứng: `W4N_truoc-sau_mat.jpg`, `W4N_ida_s37_neutral.jpg`, `W4N_ida_s37_choked.jpg`, ảnh 4 góc)
| Việc | Đã làm | Số đo / ghi chú |
|---|---|---|
| Mí trên che bớt tròng | `blender/eyelid.py`: đo mép mí bằng tia trên lưới da đã chia, nướng đơn vị MPFB `eye-closure` vào trung tính; kênh `blink` co lại (1 − c0) | Ida: 0,34 → **0,27 R** (closure 0,138). Cas: 0,30 → 0,27 R (0,045). Đích: che 1/4 bán kính tròng. Mí dưới đã chạm đáy tròng (0,47 / 0,45 R), không nướng slit |
| Viền nước mí dưới | Màu đỉnh da: dải hồng ở mép trong mí dưới, độ nhám thấp (bóng ướt) | Đi theo shape key |
| Chân mi trên | Trước đây `lash` tính mà **không dùng** (lỗi cũ); nay làm tối mép mí trên | Cả hai nhân vật |
| Bóng mềm, nhỏ | `bl_head.js` `eyeMaterial`: clearcoat 1,0 → 0,45; nhám clearcoat 0,05 → 0,20; nhám 0,4 → 0,5 | Điểm sáng nhỏ, mềm; hết đốm trắng tròn |
| Bóng mí trên nhãn cầu | Nửa trên nhãn cầu và hai góc mắt tối dần theo vị trí trên nhãn cầu | Che khuất, **không thêm đèn** |
| Mắt đọc được ở PA1 nghiêng | squint eye-slit 0,6 → **0,35**; cheekRaise eye-slit 0,25 → **0,12** (Ida) | Lần dựng đầu với mí hạ thì PA1_goodnight (sad_smile) thành khe. Đã sửa, xem hàng 3 của `W4N_truoc-sau_mat.jpg` (trái L3, phải W4N): thấy nhãn cầu và mép mí |

Tự xem: nhìn chính diện s37, mí trên che đỉnh tròng, không còn vòng lòng trắng trên tròng, điểm sáng nhỏ. Trông mắt người già mí nặng. Ở PA1_keep (máy −96°) mắt vẫn nhỏ vì góc máy, như L3.

### b. Mũ ôm đầu (bằng chứng: `W4N_truoc-sau_mu.jpg`, ảnh 4 góc)
**Ida (mũ phớt):**
- miệng mũ ngồi thấp hơn: y 0,80 → **0,775**;
- miệng mũ đo **riêng hai trục** theo khối tóc: rx 0,3893 / rz 0,4172. Trước dùng rz = rx × 1,12 cố định nên hở một trục. Vành theo cùng tỷ lệ;
- tóc dưới băng bị ép;
- **bỏ 57/260 sợi tơ** mọc ngay dưới băng, vì chúng thành "viền diềm" trắng xù;
- tóc sát dưới vành tối dần (bóng tiếp xúc bằng màu đỉnh).

**Cas (mũ len, chỉ 'bl'):**
- vỏ mũ **ôm sọ**: cách da đầu glb 0,052 H, chùng 0,03 H ở đỉnh. Hết chóp cao 0,48 H kiểu "nồi úp";
- **gấu nghiêng**: trước y 0,685, hai bên 0,60, sau 0,515;
- tóc nằm trong mũ, không xuyên len. Có hai lớp: lúc dựng, kéo đỉnh tóc vượt vỏ về tâm sọ; trong build, tóc bị ép.

**Tóc gáy Cas:** chân tóc sau tai và gáy hạ (θ 1,94/2,30/2,55/2,60 → 2,15/2,45/2,75/2,85 rad); mái hạ 1,30 → 1,45.

**Tự xem:** Ida (4 góc EEVEE) mũ tỳ lên tóc ở mọi góc, không còn khe. Chính diện s37 vẫn thấy một dải tóc bạc dưới vành, nhưng hết viền xù. Cas (4 góc) mũ ôm đầu, gáy có tóc.

### c. Tay MPFB (bằng chứng: `W4N_truoc-sau_tay.jpg`, `W4N_hai-nguoi.jpg`)
- **Dựng:** `blender/build_hands_bl.py`, 2 s → `hands_bl.json`, 3,8 MB, 4 bàn tay.
  - Người MPFB như đầu 'bl'; Ida thêm target ngón thon 0,25.
  - Rig `default` và trọng số CC0; lấy đỉnh có trọng số tay ≥ 0,12; chia 1 cấp, khoảng 6 620 đỉnh mỗi tay.
  - Đưa về hệ bàn tay cast3d; co giãn đều theo sheet.
  - Màu đỉnh: móng, khớp đốt, lòng tay.
- **three.js:** `blender/hands_bl.js`.
  - Gắn vào `ch.hands[s].hand`, tức **khớp cổ tay giữ nguyên**, HAND_SCALE 1,15 / 1,3.
  - Da tính trên CPU (LBS 16 xương), để lớp vẽ và mặt nạ C3 thấy đúng hình.
  - Cùng ánh xạ `curl`/`spread`/`thumb_cross`.
  - Vật liệu: da `skinMaterial` của đầu 'bl', nên tay và mặt cùng cách tô.
- **Nắm có va chạm:** lúc cảnh cập nhật ma trận trước khi vẽ, mỗi ngón gập dần tới khi đốt chạm vật. Vật hợp lệ: lưới ≤ 20 000 tam giác, bán kính bao ≤ 2,5 m, không thuộc thân nhân vật. Kết quả: ngón **ôm quanh** vật, không xuyên. Có cache theo ma trận cổ tay và vật.
- **Phát hiện quan trọng:** ở layout hiện tại (PA1_last), lòng bàn tay Ida cách trục cột **0,17–0,19 m**, tức **tay không chạm cột**. Lời chê "tay xuyên cột / úp phẳng" là do ngón dài của tay cũ đè lên cột khi nhìn từ máy.
  - Vì vậy tôi thêm **`ch.reachGrip`** (IK vai–khuỷu + xoay cổ tay cho lòng tay úp vào trục).
  - Khung thử gọi `grips` tự tìm trụ gần nhất. Sau IK: khoảng cách điểm nắm → mặt trụ **−0,002 m** cả hai tay.
  - Khung `W4N_truoc-sau_tay.jpg`, hàng 1: mu bàn tay trái trước cột, ngón vòng qua cột và lộ đầu ngón ở phía bên kia.
- **"Mẩu tay cam lơ lửng sau cột" ở PA1 KHÔNG phải tay.** Đó là **van đồng + tay gạt** của cột đèn (`props.js`, #8a6a3a, ở cageY − 0,2). Tia từ lòng bàn tay đo được tay gần nhất cách đó hơn 0,2 m. Vật này còn trong mọi khung PA1. Việc sửa thuộc đạo cụ/bible, ngoài quyền W4 (mục 6).
- **Cas cầm đèn lồng (s42a):**
  - trang thử dời đèn để quai nằm giữa hai nắm tay (`grips:[{who:'cas', lantern:1}]`: +3,3 / +4,9 / +3,2 cm); ngón nắm quanh quai;
  - layout W2 (`hangFromHands` treo theo cổ tay) **chưa đổi**. Đề xuất W2 dùng `ch.gripPoint`.

### d. Cas cổ áo len lật cao (bằng chứng: `W4N_truoc-sau_co-Cas.jpg`, `W4N_cas_chinhdien.jpg`, 4 góc)
- Theo nháp v1.6 mục 5: ống cổ **0,20 H**, lật **0,09 H**, Ø ngoài **0,40 H** (phần lật 0,200 H, ống 0,186 H).
- Mép gập tròn, nếp mềm; cùng màu, vân len áo.
- Sau gáy dâng thêm 0,055 H.
- Phần trên theo khớp cổ (da CPU). Chỉ nhánh `CAS_STYLE='bl'`.

### e. Nghiên cứu khả thi thân MPFB cho Cas (CHỈ BÁO CÁO) — mục 5.

## 3. Shot layout mặc định đổi hình và kết quả dò
Dò `render_film.js --only s02,s24c,s42,s05,s37,s39 --probe`, 960×540, 18 ảnh nhỏ. "Trước" lúc 01:33, trước mọi sửa. "Sau" lúc 02:16, sau lần sửa .js cuối.

| Shot | Kết quả | Ghi chú |
|---|---|---|
| **s24c** (Cas) | **0 px** ở cả 3 khung | — |
| s02 (WS, Cas + Ida) | 1 541–4 105 điểm ảnh lệch mỗi khung, **chỉ quanh Ida** | Mọi điểm lệch nằm trong hộp quanh Ida (hợp 3 khung: x 64–471, y 152–527 ở 960×540). Vùng Cas 0 px |
| s42 (Cas + Ida hậu cảnh) | 4 761–5 617 điểm ảnh lệch mỗi khung, **chỉ quanh Ida** | Mọi điểm lệch quanh đầu Ida (hợp 3 khung: x 8–343, y 0–223). Cas (bên phải) 0 px |
| s05, s37, s39 (Ida) | đổi hình (mắt, mũ) | Ảnh trước/sau: `W4N_truoc-sau_mat.jpg`, `W4N_truoc-sau_mu.jpg`; ảnh dò trong scratchpad |

**Shot mặc định đổi hình:** mọi shot có Ida (Ida 'bl' = v1.5.1: mắt, mũ). Không đổi: shot không có Ida, và mọi phần của Cas.

## 4. Khung nộp (`reports/m2/cong6/w4/`, 1920×1080, 3 mẫu, làn nặng, layout thật)
| Tệp | Nội dung |
|---|---|
| `W4N_ida_s37_neutral.jpg` · `W4N_ida_s37_choked.jpg` | s37 f2302 chính diện, trang `page_fl_bl.js` (đèn, facelight như các vòng trước), Ida v1.5.1 |
| `W4N_cas_chinhdien.jpg` | s38 106,7 s, Cas 'bl' + tay MPFB |
| `W4N_hai-nguoi.jpg` | s42a 114,5 s, Ida + Cas 'bl', tay MPFB, quai đèn lồng trong nắm tay (dời đèn trong trang thử) |
| `W4N_truoc-sau_mat.jpg` · `_mu.jpg` · `_tay.jpg` · `_co-Cas.jpg` | Trái: trước (L3, Cas MPFB cũ). Phải: W4N |
| `W4N_ida_eevee_4goc.jpg` · `W4N_cas_eevee_4goc.jpg` | EEVEE 4 góc, lưới xuất từ khung (PA1_goodnight / s42), đèn studio |
| `W4N_PA1_last_tay.jpg`, `W4N_PA1_goodnight.jpg`, `W4N_s24c_cas.jpg` | Khung phụ cho ảnh trước/sau (không bắt buộc kiểm mù) |
| `W4N_than-MPFB_so-sanh.jpg`, `than-MPFB_so-lieu.json` | Nghiên cứu (e) |
| `W4N_c3_cas_bl.json` | c3_views Cas đo lại |

## 5. Nghiên cứu khả thi thân MPFB cho Cas (không thay vào phim)
- **Ảnh:** `W4N_than-MPFB_so-sanh.jpg`, EEVEE, trực giao, đèn studio. Trái: thân Cas hiện tại (cast3d, xuất từ khung s24c, Cas 'bl'). Phải: người MPFB nam 10 tuổi + rig `default`, mặc áo len và quần do W4 dựng. Script: `blender/study_cas_body.py`, khoảng 15 s.
- **Giấy phép quần áo:** repo lõi MPFB **không có quần áo**.
  - `LICENSE.md` mục C liệt kê "Clothes (any MHCLO-based asset)" là CC0 **khi được kèm theo** ("bundled assets").
  - Nhưng thư mục `src/mpfb/data` chỉ có `3dobjs` (base.obj), `targets`, `rigs`, `poses`, `expressions`, `textures` (mặt nạ nhỏ), `mesh_metadata`, `node_trees`, `settings`, `uv_layers`.
  - Tệp `.mhclo` duy nhất là tệp thử `test/testdata/better_socks_low.mhclo`, không dùng.
  - Quần áo MPFB đến từ **asset pack tải riêng** (makehumancommunity.org), mỗi tệp có trường `license` riêng (tài liệu `docs/ui/create_assets/makeclothes.md`: "License string (e.g. `CC0`)"). Nằm ngoài phạm vi, **không dùng**.
  - Áo len và quần trong ảnh là **vỏ lệch theo pháp tuyến từ lưới thân CC0**: áo +12 mm, quần +8 mm.
  - Nếu làm thật, áo len phải tự dựng: Blender + mô phỏng vải, hoặc điêu khắc. Không có tài sản CC0 sẵn trong repo lõi.
- **Số liệu:** lưới thân 13 380 đỉnh (13 378 mặt, trước chia); rig `default` 163 xương (gồm mặt, ngón, ngón chân); cao 1,289 m. Thân Cas hiện tại: 75 lưới, 115 160 đỉnh (gồm đầu 'bl').
- **Đưa vào three.js cùng rig cast3d được không:** được, với chi phí vừa.
  - **Cách A:** chỉ lấy hình, bỏ rig MPFB. Xuất lưới thân, áo, quần tư thế nghỉ, gán lại trọng số theo khung cast3d (spine, shoulder, elbow, hip, knee…). Dùng CpuSkin như ống tay áo hiện tại. Giữ nguyên toàn bộ layout và tư thế.
    - Ước: 1 script build + 1 bảng ánh xạ xương (163 → 20 khớp cast3d), khoảng 150–250 nghìn token, 2–3 lượt chỉnh.
    - Rủi ro: vai, nách, háng xẹp khi tay giơ cao (LBS), vì cast3d không có xương đòn và vai phụ. Cần shape key sửa lỗi hoặc giữ khối vai cứng như hiện nay.
  - **Cách B:** thay khung cast3d bằng rig MPFB. Phải viết lại `applyPose` và mọi tư thế trong `common.js`, `shots_w*.js`, tức **đổi layout W1/W2**. Chi phí lớn (ước trên 0,6 triệu token), đụng continuity 52 shot. **Không khuyến nghị** ở Cổng 6.
- **Rủi ro chính (thấy ngay trong ảnh):**
  - (1) **Tỷ lệ:** thân MPFB là tỷ lệ người thật (đầu nhỏ, chân dài). Sheet Cas cách điệu (tổng cao 5,0 H, đầu to). Muốn giữ thiết kế phải co giãn xương hoặc dùng target `proportions`. Nếu không, C3 và nhận diện đổi hẳn: đây là **quyết định sáng tạo**.
  - (2) Lệch phong cách có thể **tăng** ở chiều ngược lại: thân "thật" cạnh cảnh vẽ.
  - (3) Áo len phải tự dựng, không có tài sản CC0 sẵn.
  - (4) Da CPU thêm khoảng 13–50 nghìn đỉnh mỗi khung.
- **Khuyến nghị:** nếu làm, chọn **cách A** và chỉ cho **áo len và tay áo** (phần bị chê "phồng như bóng bay", "ống"). Giữ tỷ lệ sheet bằng co giãn theo khớp cast3d. Đầu tiên nên có 1 lượt thử khả thi riêng (khoảng 100 nghìn token), dừng nếu vai/nách xẹp.

## 6. Rủi ro và việc chưa làm
1. **Tay trong layout:** tay MPFB và nắm có va chạm chỉ đúng khi tư thế đưa tay tới vật. Ở layout hiện tại tay Ida cách cột khoảng 0,2 m. W1/W2 cần gọi `ch.reachGrip` hoặc sửa tư thế (s03, s11, s13, s37, PA1), và dùng `ch.gripPoint` cho đèn lồng (s41, s42a, s42b). Nếu chỉ bật cờ mà không sửa tư thế thì ngón nắm quanh không khí.
2. **Van đồng ở PA1** đọc thành "mẩu tay cam". Cần P/chủ dự án quyết đổi màu, đổi độ sáng van, hoặc khuôn hình (bible/props, ngoài quyền W4).
3. **Hiệu năng tay:** da CPU khoảng 6,6 nghìn đỉnh × 16 xương mỗi tay, cộng tia va chạm (khoảng 1–2 nghìn tia mỗi tay mỗi lần giải), có cache theo ma trận. Chưa đo trên render cả shot.
4. **c3_views Cas:** ±90°, ±135° lệch nhiều hơn (+7,4…+11,4 %), do mũ thấp và cổ lật che bớt "đầu nhìn thấy" (xem cập nhật v1.6). C3 Ida chưa đo lại với mũ thấp hơn 0,025 H.
5. **Mắt Ida hơi "nặng mí":** có thể đọc thành mệt hoặc buồn ở trung tính. Nhịp cười buồn cần đo trên clip có tiếng (AUTHORSHIP).
6. **EEVEE Cas:** đường mờ dưới cằm do đầu xuất hai mảnh, như gói trước.
6b. **Lỗi còn thấy ở ảnh 4 góc Cas, CHƯA SỬA vì đã gần hết hạn token:**
   - vài khe tối nhỏ trên vòm mũ len gần đỉnh. Nghi là lỗi dựng lưới vỏ mũ khi dò tia (`sculpt`) quanh gờ vân len, chưa kiểm. Ở khung three.js cỡ MS (`W4N_hai-nguoi.jpg`, `W4N_cas_chinhdien.jpg`) không thấy rõ;
   - góc 180°: vẫn còn một mảng da gáy nhỏ giữa tóc và cổ lật, có một gai mảnh ở gáy (mép kẹp cổ glb). Nhỏ hơn trước, nhưng chưa hết.
   - Lượt sau nên sửa cả hai trước kiểm mù khung Cas nhìn sau lưng.
7. **Chỉ số trong ±5 % quanh ngưỡng:** C3 Cas ±45° (−0,6 / −0,5 %, ngưỡng 3 %). Không có chỉ số nào khác được đo trong gói.

## 7. Tệp, SHA-256
| Tệp | SHA-256 |
|---|---|
| `design/cong3/v2/char3d/blender/ida_bl_v151.glb` (12,4 MB) | d15eec30dff49276cf89edd95989d881ed5728dd881b76677805f153b40a5ef4 |
| `ida_bl_v151.json` | ca06762082994c9b0931e985bede2b6b042d0c35ce94cf3561870398b7e721cc |
| `cas_bl.glb` (11,2 MB, ghi đè; không khoá) | fb48ef1cfb6a6d915c0273352786a3f691352d5782474a9fb62dfbbdf0e8043e |
| `cas_bl.json` | d279ec78f2ba25a73cd74ed48792c9359363cd87e15610fb8da616e18e284439 |
| `hands_bl.json` (3,8 MB) | e344cc1ca6a146ddc73ff30b5785bf8b0ed292d0fd270f5911a00383127b76d3 |

Mã sửa hoặc thêm:
- `cast3d.js`: cờ HANDS_STYLE, tay, `reachGrip`, `gripPoint`, mũ len ôm sọ, cổ lật cao, rz mũ phớt;
- `blender/bl_head.js`: vật liệu mắt, `BL_URL` v1.5.1, xuất `skinMaterial`;
- `blender/hands_bl.js`, `blender/build_hands_bl.py`, `blender/eyelid.py`, `blender/study_cas_body.py` (mới);
- `blender/build_ida_l2.py`, `blender/build_cas_bl.py`: mí, viền nước, chân mi, mũ, tóc, kênh squint, `BL_NAME`;
- `blender/page_l2.js`: `handsStyle`, `grips`, máy theo khớp, gỡ lỗi tay;
- `design/cong5/layout/page.js`: **+1 dòng** nạp tay khi cờ bật.

`node --check` đạt ở mọi tệp .js đã sửa.

## 8. Thời gian thật, làm lại, hàng đợi, token
| Bước | Giờ UTC | Thời gian |
|---|---|---|
| Gộp nhánh, đọc báo cáo và tài liệu, dò "trước" | 01:20 → 01:35 | khoảng 15 phút |
| RIGHTS, dựng tay MPFB, tích hợp, gỡ lỗi nắm và IK | 01:35 → 01:44 | khoảng 9 phút |
| Mí, viền nước, vật liệu mắt, mũ Ida, dựng lại glb | 01:44 → 01:48 | khoảng 4 phút |
| Mũ len ôm sọ, cổ lật cao, tóc gáy Cas | 01:48 → 01:52 | khoảng 4 phút |
| Nghiên cứu thân MPFB (e) | 01:52 → 01:55 | khoảng 3 phút (4 lượt render, 14–26 s) |
| Bộ khung lượt 1–3, EEVEE, c3, dò "sau" | 01:54 → 02:18 | — |
| Báo cáo, commit | → 02:28 | — |

- **Làm lại:**
  - tay dựng 2 lượt (bỏ đoạn cẳng tay rời → cổ tay liền);
  - IK 1 lần sửa dấu khuỷu;
  - glb Ida dựng 3 lượt (mí và mũ → bỏ sợi tơ → squint/cheekRaise vì mắt thành khe ở PA1);
  - glb Cas 3 lượt (mí và tóc → gáy);
  - mũ len 2 lượt (đỉnh bị cắt phẳng ở mép lưới SDF và tóc xuyên len → nối dài SDF, kéo tóc vào trong);
  - ảnh nghiên cứu 4 lượt;
  - bộ khung 3 lượt (lượt 2, 3 sau các sửa trên).
- **Hàng đợi** (`/var/tmp/cine-queue/log.tsv`, gói W4, từ 01:33): 42 việc, chờ 0 s, mã 0 ở mọi việc. Làn nặng 20 việc, chạy 681,8 s: 15 khung 1920×1080 3 mẫu (14–30 s mỗi khung), 2 lượt c3 Cas (khoảng 124 s mỗi lượt). Làn nhanh 22 việc, chạy 627,3 s: thử 480–1920 px 1 mẫu, xuất lưới khung cho EEVEE, 4 lượt dò 74–79 s (gắn cờ QUA-60S như các lượt dò trước). Blender dựng glb và tay (2–7 s mỗi lượt) và ảnh nghiên cứu chạy ngoài hàng đợi
- EEVEE 4 góc chạy ngoài hàng đợi, khoảng 100 s mỗi nhân vật.
- **Token:** ngữ cảnh tích luỹ khi kết thúc khoảng 455 nghìn (hạn khoảng 500 nghìn). Riêng nghiên cứu (e) khoảng 20 nghìn (hạn 100 nghìn).

## 9. Việc đang chờ
- **P:** kiểm mù bộ khung ở mục 4 (6 subagent như kế hoạch: 2 Ida chính diện, 2 Cas, 2 đối chứng).
- **P / chủ dự án:**
  - duyệt đề xuất v1.5.1 (`characters-v1.5.1-DE-XUAT.md`) và cập nhật v1.6 (`characters-v1.6-CAP-NHAT-W4N.md`);
  - quyết tay MPFB làm mặc định;
  - quyết van đồng ở PA1 (mục 6.2);
  - quyết hướng thân MPFB (mục 5).
- **W1/W2 (sau duyệt):** dùng `ch.reachGrip` và `ch.gripPoint` khi diễn hoạt các shot cầm cột, van, đèn lồng.
- **P/K:** cách đo C3 Cas 0°/180° (còn treo từ gói trước).
