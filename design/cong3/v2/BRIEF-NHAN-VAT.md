# Cổng 3 vòng 2 — Giao việc: hai cách làm nhân vật (phiên P)

Phim **Last Round**, hướng mỹ thuật đã chọn: **C "Painted Glow"** (tranh sơn ánh sáng). Chủ dự án đánh giá độc lập vòng 1:
- Bối cảnh C tốt, có không khí điện ảnh.
- **NHÂN VẬT LÀ ĐIỂM YẾU LỚN NHẤT**: trông như ma-nơ-canh ghép khối, tay chân cứng, mặt sơ sài, lệch hẳn chất tranh sơn của bối cảnh.
- Kiểm silhouette mù (P đo, 2 lượt, agent không biết dự án): hành động đúng 85% (cần ≥ 90%).
  - **Chim bóng trượt**: tay Cas nhỏ, ngón là que mảnh, không thành hình cánh.
  - **Ida bị đọc là "đàn ông đội mũ"** ở mọi hình; **Cas bị đọc là "bé gái búi tóc"** (quả bông mũ trông như búi).

## Việc
Viết **một module dựng nhân vật** thay cho `design/cong3/shared/cast.js`, **cùng API**, trong thư mục của bạn:
- Cách (1) 3D nâng cấp → `design/cong3/v2/char3d/cast3d.js`
- Cách (2) tranh 2D có khung xương → `design/cong3/v2/char2d/cast2d.js`

Bối cảnh, ánh sáng, máy quay của 4 shot đã dựng sẵn và **dùng chung** cho cả hai cách (so sánh công bằng): `v2/shots.js`, `v2/s5.js`, `v2/page.js`. **Không sửa** các file đó, `shared/`, `model-sheet/`, `bible/`, `checks/` (không đọc `checks/`). Không commit.

### API bắt buộc (xem `shared/cast.js` làm mẫu)
```js
export function buildCharacter(sheet, opts)   // sheet = model-sheet/ida.json | cas.json
  // opts.material(role, colorHex, part, extra) → Material  (BẮT BUỘC dùng cho mọi bề mặt nhận sáng: cảnh quyết định cách chiếu sáng;
  //   truyền map/normalMap/alphaTest/transparent... qua extra). opts.detail = mức chia lưới gợi ý.
  // trả về { root, joints, props: {lantern, ladder, pole}, hands, parts, H, sheet, setPose(pose) }
export function update(ch, camera)            // TUỲ CHỌN: gọi trước mỗi mẫu tích luỹ (ví dụ xoay thẻ 2D theo máy quay)
```
- Tên khớp, quy ước góc, tư thế (JSON), đạo cụ (`lantern` có `userData.lightAnchor` và `userData.handleY`; `ladder`; `pole`) giống hệt `shared/cast.js`. Cách đơn giản nhất: **import và mở rộng** `shared/cast.js` (dùng khung xương, `applyPose`, đạo cụ của nó), thay phần hình khối/vẽ.
- **Luật C3:** không đổi độ dài các bộ phận đo (head, torso, upper_arm, forearm, thigh, shin — giữa hai tâm khớp). Bàn tay và ngón không thuộc C3: **được phóng to tối đa 1,3×** nếu cần cho chim bóng (ghi rõ trong README để chủ dự án duyệt).
- Chủ dự án đã duyệt tỷ lệ, trang phục, silhouette Cổng 1 (mũ phớt, áo dài xẻ tà, thang; mũ len quả bông, áo len quá khổ). **Được thêm chi tiết thứ cấp** (chủ dự án nêu: búi tóc, khăn, găng) để sửa lỗi đọc giới tính và tuổi:
  - **Ida (74, nữ):** váy dài lộ dưới gấu áo, khăn choàng/khăn quàng, búi tóc to rõ, dáng vai và cổ người già, mặt có nếp nhăn.
  - **Cas (10, nam):** tóc ngắn lộ ở gáy và thái dương dưới mũ, tai vểnh, quần, tay áo len quá khổ; quả bông mũ không được đọc thành búi (đặt cao, tròn, xù len rõ).
- Tên file, `root.userData.imp` do cảnh đặt; bạn không cần.

### Yêu cầu của từng cách
- **(1) 3D nâng cấp:** khối điêu khắc mềm (không còn trụ + cầu ghép), mặt có cấu trúc (hốc mắt, gò má, cằm, nếp nhăn tuổi 74 cho Ida, má tròn trẻ con cho Cas), bàn tay có ngón rõ (2–3 đốt, khớp), nếp vải áo khoác, chi tiết thứ cấp. Chất bề mặt hợp tranh sơn C (không bóng nhựa). Cách dựng gợi ý: lưới liền (skinning theo khung xương hoặc khối mềm ghép kín), displacement/normal map sinh bằng mã.
- **(2) Tranh 2D có khung xương:** vẽ nhân vật dạng **tranh sơn** theo từng lớp bộ phận (đầu, thân, cánh tay, cẳng tay, bàn tay, chân, vạt áo…), mỗi lớp là một thẻ gắn vào khớp của cùng khung xương, **quay về phía máy quay quanh trục xương** (`update(ch, camera)`). Tranh sinh bằng mã (canvas: mảng màu, nét cọ, rìa mềm). Mỗi lớp có **normal map** (suy từ bản đồ độ cao vẽ kèm) để đèn khí, đèn lồng, đèn điện của three.js chiếu lên, cùng chất liệu với bối cảnh C. **Bóng đổ phải đúng hình người** dù thẻ quay về máy quay: gợi ý giữ thân 3D gốc làm **vật đổ bóng vô hình** (không ghi màu vào khung, vẫn đổ bóng), hoặc cách khác đúng hơn.

## Bốn shot dùng để so (đã dựng; render bằng driver chung)
| Khung | Nội dung | Lệnh thử (960×540, nhanh) |
|---|---|---|
| `a_close_ida` | Cận mặt Ida trên thang, hơ tay trên lồng đèn khí | `node shared/render_still.js --page v2/page.js --frame a_close_ida --out v2/charXd/test --samples 8 --w 960 --h 540 --args '{"char":"Xd","shot":"a_close_ida"}'` |
| `b_cas_bird` | Trung cảnh Cas làm chim bóng trên tường | như trên, `b_cas_bird` |
| `c_s5_wide` | Cảnh 5 khung rộng, đã thêm viền sáng (dội từ vách bên) | như trên, `c_s5_wide` |
| `walk` | Ida vác thang đi qua 2 cột đèn, 96 khung | `node shared/render_seq.js --page v2/page.js --shot walk --from 0 --to 96 --out ... --samples 8 --w 960 --h 540 --args '{"char":"Xd"}' --pngs 0,48,95` |

Chạy trong `design/cong3` với `PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers`. Thay `Xd` bằng `3d` hoặc `2d`.

**Tránh render thừa:** bạn chỉ render thử ở 960×540 (vài khung walk, không cần đủ 96). **P sẽ render bản chính thức 1920×1080 tuần tự** (để đo thời gian sạch) sau khi bạn nộp. Máy đang chạy 2 cách song song nên thời gian bạn đo bị nhiễu.

## Ngân sách
Chủ dự án duyệt **≤ 5 s/khung** ở 1920×1080, 8 mẫu, kể cả lớp vẽ. Mốc: bộ cảnh chung với nhân vật cũ đo khoảng 2,1 s/khung ở 960×540, nên nhân vật mới không được làm chậm quá nhiều. Ghi ước tính của bạn.

## Nộp (trong thư mục của bạn)
- Module + file phụ; `test/*.png` (4 shot ở 960×540).
- `README.md` (tiếng Việt): cách làm; những gì đã thêm (chi tiết thứ cấp, tay); có phóng to tay không (bao nhiêu); tự phê bình thẳng thắn (chỗ nào còn "ma-nơ-canh", còn lệch chất tranh sơn); rủi ro khi chuyển động (thẻ 2D quay, nhấp nháy, xuyên hình); ước tính s/khung.
- Không sao chép thiết kế nhân vật của phim hay IP có sẵn.
