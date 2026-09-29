# ĐỀ XUẤT characters v1.5.1 — Ida: mắt, mũ, tay (Cổng 6, gói W4 nhân vật)

Đây là **đề xuất để P soạn và chủ dự án duyệt**. W4 không sửa `bible/characters.md`, `design/cong3/model-sheet/ida.json`, LIBRARY hay LOCK.
- v1.5 đã khoá SHA gồm `ida_bl.glb` (`31d13052…`) và `ida_bl.json` (`256d9652…`). **Hai tệp này giữ nguyên, không ghi đè.**
- Bản v1.5.1 là tệp mới: `design/cong3/v2/char3d/blender/ida_bl_v151.glb` và `ida_bl_v151.json`. SHA-256 đầy đủ ghi trong BAO-CAO-W4N.md, mục 7.
- `bl_head.js` trỏ `BL_URL` sang tệp v1.5.1, vì lệnh gói cho phép đổi hình mặc định Ida ở nhánh 'bl'.
- Dựng lại bằng lệnh: `BL_NAME=ida_bl_v151 /opt/bpy/bin/python design/cong3/v2/char3d/blender/build_ida_l2.py -- <mpfb2> design/cong3/v2/char3d/blender` (khoảng 7 s).

## 1. Mắt
| Hạng mục | v1.5 | v1.5.1 (đề xuất) | Cách làm, số đo |
|---|---|---|---|
| Mí trên | Mép mí cách tâm nhãn cầu 0,34 R. Nhìn chính diện, lòng trắng lộ trên tròng ("mắt búp bê") | Mép mí ở **0,27 R**, che khoảng 1/4 bán kính tròng phía trên | Đo mép mí bằng tia trên lưới da đã chia (`blender/eyelid.py`). Nướng đơn vị MPFB `eye-closure` **0,138** vào tư thế trung tính (CC0, W4-MPFB-A) |
| Mí dưới | 0,47 R | Giữ 0,47 R, vì đã chạm đáy tròng (đích 0,478 R) | Không cần nướng `eye-slit` (0,000) |
| Kênh `blink` | eye-closure ×1 | eye-closure ×**0,862** | Chớp kín vẫn đúng 1,0 = nhắm hẳn |
| Kênh `squint` | eye-slit ×0,6 | eye-slit ×**0,35** | Mí trên đã hạ sẵn. Nếu giữ 0,6 thì PA1_goodnight (sad_smile) thành khe khi nhìn nghiêng |
| Kênh `cheekRaise` | khối má thủ tục + eye-slit ×0,25 | khối má thủ tục + eye-slit ×**0,12** | Cùng lý do |
| Chân mi trên | Tính trong `skin_albedo` nhưng **không dùng** (lỗi cũ) | Tối thật sự (r −0,45, g −0,48, b −0,45 × hệ số) | Mép mí có nét, đi theo mí khi chớp |
| Viền nước mí dưới | Không có | Dải hồng ướt ở mép trong mí dưới (r +0,06, g −0,16, b −0,10). Độ nhám thấp: kênh alpha × (1 − 0,95·wl), tức nhám về khoảng 0,45 | Màu đỉnh da, đi theo shape key |
| Độ bóng nhãn cầu (three.js) | clearcoat 1,0, nhám clearcoat 0,05, nhám 0,4: đốm trắng gắt | clearcoat **0,45**, nhám clearcoat **0,20**, nhám **0,5**: điểm sáng nhỏ, mềm | `bl_head.js` `eyeMaterial`; ghi đè bằng `opts.eyeCoat`, `eyeCoatRough` |
| Bóng mí trên nhãn cầu | Không có | Nửa trên nhãn cầu và hai góc mắt tối dần (tối đa −55 % ở đỉnh, −25 % ở góc; sàn 0,3) | Che khuất theo vị trí trên nhãn cầu, không thêm đèn. `opts.eyeAO` (mặc định 1) |
| Tròng, con ngươi, hội tụ | như v1.5 | Không đổi | — |

Áp dụng cho cả Cas 'bl' (nháp v1.6): Cas nướng eye-closure 0,045, mí trên 0,30 → 0,27 R, mí dưới 0,45 R. Vật liệu mắt dùng chung.

## 2. Mũ phớt
| Hạng mục | v1.5 | v1.5.1 (đề xuất) |
|---|---|---|
| Độ cao miệng mũ (hệ đầu) | y 0,80 | y **0,775** (ngồi thấp hơn 0,025 H) |
| Miệng mũ | rx 0,3798 / rz 0,4254 (rz = rx × 1,12 cố định). Bị hở theo trục không khớp | Đo **riêng hai trục** theo khối tóc ở dải băng, ép 2,5 %: rx **0,3893** / rz **0,4172**, tâm z −0,034 |
| Vành mũ (cast3d) | Tỷ lệ elip 1,12 cố định | Theo rz/rx đo được. Với json v1.5 thì rz = rx × 1,12, nên các kiểu 'aa'/'ai' không đổi |
| Tóc dưới băng | Ép 0,010 H | Giữ luật ép, áp theo miệng mũ mới. **Bỏ 57/260 sợi tơ** mọc ngay dưới băng (chúng thành "viền diềm" trắng xù dưới vành) |
| Bóng tiếp xúc | Không có | Tóc sát dưới băng và vành tối dần (tối đa −60 % trong dải 0,10 H dưới băng). Là màu đỉnh che khuất, không phải đèn |
| Bản lề, đẩy mũ | Tâm sọ, 0,26 rad | Không đổi |

## 3. Tay (sau cờ, mặc định chưa đổi)
| Hạng mục | v1.5 | v1.5.1 (đề xuất, cần chủ dự án duyệt trước khi thành mặc định) |
|---|---|---|
| Lưới bàn tay | Lòng tay SDF + 4 ngón × 3 đốt + ngón cái 2 đốt, dạng "ống" | **Bàn tay MPFB2** (lõi CC0, W4-MPFB-A3): nữ 74 tuổi, ngón thon (target fingers-diameter-decr 0,25). Chia 1 cấp, khoảng 6 620 đỉnh mỗi tay. Móng, khớp đốt ửng và lòng tay sáng tô bằng màu đỉnh |
| Khung xương ngón | 3 khớp theo `curl`/`spread` | 16 xương MPFB `default` (wrist + finger1–5 × 3). Da tính trên CPU. Cùng ánh xạ `curl`/`spread`/`thumb_cross` như cũ |
| Gắn vào rig | Nhóm `hand_*` ở khớp `wrist_*` | **Giữ khớp cổ tay** và HAND_SCALE 1,15. Co giãn đều để cổ tay → đầu ngón giữa = (palm 0,36 + finger 0,30) × H |
| Nắm | Không có va chạm: ngón úp phẳng, xuyên cột | **Nắm có va chạm**: mỗi đốt gập tới khi chạm vật gần tay (cột, van, quai, sào, bậc thang), nên ôm quanh vật, không xuyên. Nếu `curl` ≥ 0,5 và có vật trong tầm thì nắm kín tới khi chạm |
| Đưa tay tới cột | — | API `ch.reachGrip(s, {point, axis, radius})`: IK 2 xương vai–khuỷu, cổ tay xoay cho lòng tay úp vào trục. Dùng khi diễn hoạt Cổng 6 (W1/W2) |
| Cách bật | — | `buildCharacter(sheet, { handsStyle: 'bl' })` hoặc `globalThis.CINE_HANDS_STYLE = 'bl'`, **kèm** `await preloadHandsBL()` trước khi dựng. Trang layout: đặt `globalThis.CINE_HANDS_STYLE='bl'` trước khi `page.js` chạy |

## 4. Tác động
- **c3_views Ida:** không đổi. Mũ thấp hơn làm "đầu nhìn thấy" ngắn đi một chút; tay không thuộc C3. Chưa đo lại vì lệnh gói không yêu cầu. Nên để P đo lại khi khoá v1.5.1.
- **Shot layout mặc định đổi hình:** mọi shot có Ida (mắt và mũ). Danh sách ở BAO-CAO-W4N.md, mục 3.
- **Việc cần duyệt:**
  - (1) hình mắt và mũ v1.5.1;
  - (2) hệ số squint 0,35 / cheekRaise 0,12. Đây là hiệu chỉnh kênh biểu cảm, ảnh hưởng nhịp cười buồn;
  - (3) tay MPFB làm mặc định, sau kiểm mù.
