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
