# Cổng 5 · Gói W3 — Mặt Ida, phương án A1 (báo cáo cho P)

Phiên: W3 (xưởng). Nhánh worktree: `worktree-agent-a83d4075f6a9542ef` (fast-forward từ `claude/cine-lab-m2-cong5-layout-24o5fp` @ 085fd31). Chưa push, chưa merge.
Phạm vi: A1 mục 1–4 theo quyết định chủ dự án. **Không làm A3.** Không sửa `bible/`, `checks/` (không đọc mã trong `checks/`), `ida.json`, hay file layout của W1/W2/P.
W3 **không tự chạy kiểm mù** — P gửi từng ảnh cho subagent mới.

## 0. Tóm tắt
| Mục | Kết quả | Số đo thật |
|---|---|---|
| 1. Cổ áo | Bỏ trụ trơn. Mép trên cong theo đường hàm (tính từ chính hình đầu), có nếp vải dồn dưới hai góc hàm, mép cuộn dày, lót tối. Phần trên cổ áo theo khớp đầu 0,9. Giữ màu áo/lót, giữ ý "dựng cao che cổ trần" | B1 0°: không đổi (thân 2,668 vs 2,667) nếu giữ lọn tóc v1.2; xem mục 4 về lọn tóc |
| 2. Nếp mũi–má | Hai nét mảnh đậm nối nhau thành một vệt từ cánh mũi tới cằm → nay là dải bóng mềm dừng trên khoé miệng + vệt sáng má; rãnh khoé miệng ngắn, nhạt, tắt trước cằm | — (đánh giá bằng mắt, mục 3) |
| 3. Ánh sáng cận mặt | `design/cong5/layout/facelight.js`: fill/under/rim là ánh dội và viền của nguồn có thật, tỷ lệ theo độ rọi nguồn chính; `exposure()` không cháy da | Khung mặt: điểm ảnh cháy 28–29 % (lần 3) → **2,4–2,7 %**; p99,5 độ sáng 0,866 → 0,769 |
| 4. Chính diện = nghiêng | Cùng lưới đầu, cùng texture; s31 dựng lại với nhân vật mới giữ nguyên mặt nghiêng | Ảnh so sánh `so-sanh_nghieng_s31.jpg` |
| Thêm (tự rà) | Lọn tóc bạc thái dương (A1) ở góc nghiêng đọc như vết xước → rút về thái dương, dày hơn. **Làm B1 0° giảm 3,0 %**: cần P/chủ dự án chọn | mục 4, mục 5 |

## 1. Thay đổi theo từng mục (file, hàm, tham số)

### Mục 1 — Cổ áo (`design/cong3/v2/char3d/cast3d.js`, `buildCharacter`, nhánh Ida, khối "Cổ áo đứng")
- **Bỏ** `tube` trụ tròn cũ (bán kính 0,225–0,26 H, mép phẳng ở tL + 0,44 H, gắn cứng vào khớp thân).
- **Mép trên theo đường hàm** (`RIM[φ]`, 180 hướng): với mỗi φ, lấy điểm thấp nhất của SDF đầu (`headSDF`) ở cùng x, trên mọi độ sâu từ mép ra trước (nửa trước), hoặc tia dọc (nửa sau); mép = điểm đó − 0,01 H, chặn trên ở `CL.side` = tL + 0,50 (hai bên) / `CL.back` = tL + 0,46 (sau gáy), chặn dưới `CL.low` = tL + 0,24. Ở trước cộng `CL.tuck` = 0,10·gauss(|φ|, 0,45) để mép luồn **sau** cằm (cằm che mép). Sau đó co (min ±16°) rồi làm mượt Gauss (±24°) để mép dâng đều, không gãy khúc, không vượt lên trên đường hàm. `CL.gap` = 0,035 H.
- **Loe và mặt cắt:** chân `CL.rb` = 0,228 H (dưới khăn), mép trước `rf` = 0,28, hai bên `rs` = 0,325, sau `rbk` = 0,29; loe theo t^1,4.
- **Nếp vải** `clFold(φ, t)`: 0,012·sin 8φ + 0,007·sin 13φ, biên độ dồn ở hai góc hàm (0,35 + 0,9·gauss(|φ| − 0,85, 0,45)), tăng dần lên mép; màu đỉnh tối ở đáy nếp (hệ số 14). Mép gợn 0,1 × nếp.
- **Mép cuộn** (strand bán kính 0,022 × 0,017 H) giữa vỏ ngoài và lót; **lót** (`clLin`) tối 0,28–0,52 (mép lót sáng từng đọc thành "lỗ").
- **Đường nối** của ống và mép cuộn đặt ra sau gáy (bản đầu có vết đứt ở giữa cằm).
- **Da CPU:** trọng số khớp đầu `CL.wHead` = 0,9 × sstep(tL + 0,02, tL + 0,26, y) (chân: thân). Khi quay/cúi đầu, chỗ trũng trước vẫn nằm dưới cằm. Đã thử: quay 35° (face_ida), ngửa −25°/quay −30°, quỳ (s30, s31), nhìn xuống (s13), đẩy mũ (s36).
- **Cổ (da)** Ida: màu đỉnh tối 0,42–0,54 (nằm trong lòng cổ áo, dưới bóng cằm) — khe dưới cằm đọc là bóng, không còn "cột cổ hồng" (thấy ở s39).
- **Mặt dưới hàm/cằm** (`skinTone`): tối dần tới 30 % ở vùng pháp tuyến quay xuống (y < 0,34 H) — che khuất bởi cổ áo; mặt không còn sáng đều tới tận mép hàm.

### Mục 2 — Nếp mũi–má (`design/cong3/v2/char3d/facepaint.js`, `paintFace`, mục 7)
| Nét | Trước | Sau |
|---|---|---|
| Rãnh mũi–má | 1 nét cọ 5 px, α 0,66, màu 120,76,72, từ (0,07; 0,43) tới **khoé miệng** (0,118; 0,275) | Dải bóng mềm 11 px, α 0,26, dừng ở (0,108; 0,318) — **trên** khoé miệng; lõi rãnh 4 px α 0,22; vệt sáng ấm má sệ 10 px α 0,16 phía ngoài |
| Rãnh khoé miệng xuống cằm | 3,6 px, α 0,55, **nối tiếp** từ khoé tới (0,108; 0,13) gần cằm | 7 px, α 0,18, bắt đầu **dưới** khoé (y = my − 0,03), tắt ở y = 0,175 (trước cằm) → có khe giữa hai rãnh |
| Nét tóc vẽ ở thái dương | kéo từ y 0,84 xuống 0,60 | dừng ở y 0,71 (phần dưới chiếu lên má ở góc nghiêng, đọc như vết xước) |

### Mục 3 — Ánh sáng cận mặt (`design/cong5/layout/facelight.js`, file mới của W3)
**API** (cùng quy ước `design/cong5/layout/*.js`, import three từ `/cong3/shared/node_modules/...`):
```js
import { createFaceLight } from './facelight.js';
const fl = createFaceLight(scene, { mode: 'gas' | 'lantern' | 'elec' /*, fill:{…}, under:{…}, rim:{…} ghi đè preset */ });
// mỗi khung, SAU setState của bộ cảnh và SAU khi đặt tư thế Ida + máy quay:
fl.update(ida, cam, { key /* Light|Light[] tuỳ chọn; bỏ trống = tự chọn đèn rọi mạnh nhất vào mặt */, keyE /* ánh tràn phẳng, vd. whiteHemi.intensity */, level /* 0…1 */ });
exposure: fl.exposure()   // = K / độ rọi tổng tại mặt; K = { gas: 4, lantern: 4, elec: 6 }
fl.faceE() // { key, fill, under, rim, total }   fl.lights // { fill, under, rim }   fl.dispose()
```
- Ba đèn phụ đều là **PointLight không đổ bóng**, có tầm 1,6 × khoảng cách đặt (≤ 1,6 m): chỉ chạm vùng đầu–vai (bản đầu tầm 2,4× làm sáng tường sau lưng ở s37 — đã sửa).
- Vị trí tính theo mặt: **fill** phía máy, đối xứng với nguồn chính qua trục mặt–máy (ánh dội từ phía không có đèn); **under** dưới-trước (dội từ đá lát/áo/khăn, nhấc bóng dưới cằm, nối cằm với cổ áo); **rim** sau đầu, ngược máy, cao 30–40°.
- Cường độ = tỷ lệ × độ rọi nguồn chính tại mặt (tự đo theo mô hình suy giảm của three.js, `illuminanceAt`) → đúng với mọi khoảng cách và theo mức lửa/điện từng khung.
- Nguồn trong truyện: `gas` = L11 + dội vôi tường/đá lát + viền trời đêm; `lantern` = đèn lồng thấp + dội trên-trước (L11, vôi) + viền ấm L11; `elec` = trắng phẳng cột điện + L11 đang nhạt (không thêm viền). Không có mắt phát sáng: không đèn nào phát xạ, glint giữ nguyên của shot.

**Cách W2 dùng cho từng shot (đã thử trên shot layout thật bằng trang `design/cong5/mat/page_layout_fl.js`, không sửa file W2):**
| Shot | Gọi | Phơi sáng hiện tại → đề xuất | Ảnh |
|---|---|---|---|
| s26 | `mode:'lantern'`, key tự chọn (L11 sau lưng) | giữ 2,6 | `facelight_s26_truoc-tren_sau-duoi.jpg` |
| s36 | `mode:'gas'`, key tự chọn (L11) | 0,36 → `fl.exposure()` ≈ 0,082 | `facelight_s36_…jpg` |
| s37 | `mode:'gas'` | 0,36 → ≈ 0,083 | `facelight_s37_…jpg` |
| s39 | `mode:'elec'`, `keyE: st.whiteHemi.intensity` | 0,9 → ≈ 0,36 | `facelight_s39_…jpg` |
Lưu ý cho W2/P: đổi phơi sáng làm **cả khung** tối đi (s36/s37 tối hơn ~4×, nền chuyển tím theo grade; s39 tường từ trắng sang trắng xám). Nếu muốn giữ độ sáng nền, dùng `Math.max(fl.exposure(), …)` hoặc nâng `K` — đổi lại da sẽ cháy lại. Đây là lựa chọn sáng tạo của P/chủ dự án.

### Mục 4 — Cùng một khuôn mặt chính diện và nghiêng
- Mặt chính diện và nghiêng dùng **cùng một lưới đầu SDF và cùng một texture vẽ tay** (C′); A1 không đổi hình đầu, mũi, tỷ lệ đầu/cổ.
- Chỗ làm hai góc trông khác người trong lần 3 là **ánh sáng** (cháy sáng, bóng mũi cứng vắt qua miệng ở chính diện) và **đường nối cằm–cổ**, không phải hình mặt. Sửa bằng mục 1–3.
- s31 dựng lại (probe 960×540) với nhân vật mới: mặt nghiêng giữ nguyên (mũi dài khoằm, má hóp, búi), chỉ khác cổ áo nay ôm tới hàm. Xem `so-sanh_nghieng_s31.jpg` (trái: animatic v2 1:14; giữa: s31 layout với nhân vật A1; phải: ảnh nghiêng A1 dưới đèn khí).

## 2. Ảnh
Ảnh gốc PNG 1920×1080, 3 mẫu (không commit, theo `design/cong5/mat/.gitignore`): `design/cong5/mat/a1/<tên>/face_ida.png`. Bản JPEG (≤ 300 KB) trong `reports/m2/cong5/w3/`:
| Tên | Nội dung | JPEG |
|---|---|---|
| neutral | trung tính, vành mũ đã đẩy, góc gần chính diện (khung lần 3) | `a1_neutral.jpg` (92 KB) |
| sad_smile | cười buồn | `a1_sad_smile.jpg` (92 KB) |
| choked | nghẹn | `a1_choked.jpg` (92 KB) |
| nghieng | mặt nghiêng (máy lệch 80°), cười buồn — so với s31 | `a1_nghieng.jpg` (104 KB) |
| co-ao_cu-chi | cổ áo cận trong cử chỉ đẩy mũ (hat_push_b) | `a1_co-ao_cu-chi.jpg` (99 KB) |
| trước/sau | trên: lần 3 (k2, m7, w4); dưới: A1 | `so-sanh_lan3-tren_a1-duoi.jpg` |
| nghiêng | s31 v2 / s31 A1 / nghiêng A1 | `so-sanh_nghieng_s31.jpg` |
| facelight | s26, s36, s37, s39: trên = layout hiện tại, dưới = + facelight | `facelight_s{26,36,37,39}_truoc-tren_sau-duoi.jpg` |

Cách render: `bash design/cong5/mat/run_mat.sh design/cong5/mat/a1` (bản chép từ `design/cong4/mat/run_mat.sh`: cùng khung face_ida, cùng tham số máy/đầu/ánh mắt, 3 mẫu, 1920×1080; khác: trang `design/cong5/mat/page_mat.js` = face_ida + facelight `gas` + `expose:"auto"`; driver `design/cong5/mat/still.js` = `render_still.js` với gốc phục vụ `design/`; mỗi ảnh là một việc trong hàng đợi). Ảnh lần 3 không có cử chỉ riêng cho cổ áo; ảnh "cổ áo cận" dùng tư thế `hat_push_b`, `faceY −0,13`, `faceDist 1,25`.

## 3. Tự rà (không phải kiểm mù)
| Câu hỏi | Tự đánh giá | Còn lại |
|---|---|---|
| Ranh giới cằm/cổ còn cứng? | Mềm hơn rõ: cằm nằm **vào** cổ áo, mép cổ áo đi theo đường hàm và dâng lên tới góc hàm; khe dưới cằm tối (bóng), không còn trụ trơn | Mép hàm vẫn là đường rõ trên nền lót tối ở góc gần chính diện (đó là đường viền mặt thật, không phải đường ghép) |
| Vệt nào đọc thành vết nứt/sẹo? | Rãnh mũi–má không còn nối tới cằm; lọn tóc thái dương không còn áp trên má ở góc nghiêng | Nét nếp dọc môi trên (4 nét mảnh, tuổi) và nếp cằm của "nghẹn" vẫn là nét; ở s39 (trắng phẳng) còn thấy rõ hơn dưới đèn khí |
| Mặt có tách khỏi thân? | Bớt: không còn 29 % điểm ảnh cháy; cổ áo nhận ánh dội dưới (under); cổ áo ôm tới hàm | Mặt vẫn là mảng sáng nhất khung (đúng nguồn: đèn khí cách 0,5 m). Người xem có thể vẫn thấy "sáng như có đèn trước mặt" |
| Chính diện và nghiêng cùng người? | Có — cùng lưới, cùng texture; s31 giữ nguyên | Ở chính diện mũi ngắn lại do phối cảnh (85 mm) — không đổi được mà không đổi hình |
| Cổ áo có đọc lạ? | Ở ánh trắng phẳng (s39) cổ áo loe nhẹ có thể đọc như "cổ lọ"; đã giảm loe (0,36 → 0,325 H) | Nếp vải chỉ thấy rõ ở ánh xiên (đèn khí), gần như mất dưới ánh điện phẳng |

## 4. B1 — đo lại (công cụ `design/cong4/tools/b1_measure.py`, mặt nạ nhìn thấy 4×, turnaround, trực giao)
Đo "trước" chạy lại bằng `cast3d.js` gốc (085fd31) trong worktree này: khớp đúng số sheet (thân 2,667; cánh tay trên 1,600; cẳng tay 0,994; cẳng chân 0,293; head 435,66 px) → công cụ và máy ổn định.

**Ida, hai phương án lọn tóc thái dương (cổ áo mới ở cả hai):**
| Góc | Sheet (trước) thân / tay trên / cẳng tay / cẳng chân | Sau — lọn **'long'** (v1.2) | Sau — lọn **'temple'** (W3 đề xuất) |
|---|---|---|---|
| **0°** | **2,667 / 1,600 / 0,994 / 0,293** | **2,668 / 1,600 / 0,994 / 0,293** (head 435,60 px) | **2,586 / 1,551 / 0,963 / 0,284** (head 449,41 px) |
| 45° | 2,314 / 1,483 / 0,914 / 0,282 | 2,310 / 1,480 / 0,912 / 0,281 | 2,297 / 1,472 / 0,907 / 0,280 |
| −45° | 2,315 / 1,466 / 1,299 / 0,282 | 2,310 / 1,463 / 1,296 / 0,281 | 2,295 / 1,453 / 1,287 / 0,279 |
| 90° | 2,137 / — / — / — | 2,124 | 2,120 |
| −90° | 2,153 / 1,408 / 1,009 / 0,275 | 2,137 / 1,396 / 1,000 / 0,273 | 2,133 / 1,393 / 0,998 / 0,272 |
| 135° | 2,386 / 1,465 / 0,825 / 0,272 | 2,392 / 1,468 / 0,826 / 0,273 | 2,395 / 1,470 / 0,827 / 0,273 |
| −135° | 2,354 / 1,455 / 1,087 / 0,270 | 2,361 / 1,459 / 1,089 / 0,271 | 2,364 / 1,461 / 1,091 / 0,271 |
| 180° | 2,510 / 1,578 / 1,193 / 0,284 | 2,512 / 1,578 / 1,193 / 0,284 | 2,512 / 1,578 / 1,193 / 0,284 |
Cas: không đổi ở mọi góc (lưới Cas không bị đụng).

Giải thích: ở 0° phần đầu nhìn thấy (dưới mũ, cổ áo che cằm) **rộng hơn cao**, nên trục chính PCA là **bề ngang**. Lọn 'long' buông tới má che hai mép đầu → bề ngang đo ngắn hơn. Lọn 'temple' không che → đầu đo dài hơn 3,2 %, mọi tỷ lệ 0° giảm ~3,0 %. Đầu thật không đổi. Cổ áo mới tự nó chỉ đổi 0° 0,04 % và các góc khác ≤ 1 %.

**Chỉ số trong ±5 % quanh ngưỡng (luật cứng):** với 'temple', tỷ lệ 0° lệch **−3,0 %** so với sheet v1.3, **đúng bằng** mức 3 % mà sheet ghi cho C3 → nếu không cập nhật `c3_views`, các shot gần chính diện có thể bị cờ C3. Với 'long', lệch 0,04 % (0°) và ≤ 0,8 % (các góc khác).

## 5. Đề xuất đổi sheet / bible (gửi P — W3 KHÔNG sửa `ida.json` hay `bible/`)
Trong worktree W3, `design/cong3/model-sheet/ida.json` **không đổi** (không trường nào).
1. **Chọn lọn tóc thái dương** (hằng `IDA_WISPS` đầu `cast3d.js`, mặc định `'temple'`; `opts.idaWisps` ghi đè):
   | | 'temple' (W3 đề xuất) | 'long' (v1.2) |
   |---|---|---|
   | Ưu | Góc nghiêng (s31, s34) không còn "vệt xước" trên má; đúng chữ "ở thái dương" của v1.2 | Không đổi B1/sheet |
   | Nhược | Đổi B1 0° −3 % | Góc nghiêng: 3 nét xám áp trên má (rủi ro "sẹo") |
   | Tác động | Sheet `c3_views.0°`: thân 2,667 → **2,586**, cánh tay trên 1,600 → **1,551**, cẳng tay 0,994 → **0,963**, cẳng chân 0,293 → **0,284**; các góc khác theo bảng mục 4; P khoá lại SHA | 0 |
   | Rủi ro | Thấp (đổi số đo, không đổi hình) | Trung bình (kiểm mù có thể nêu vệt ở góc nghiêng) |
   Ảnh A1 đã render với 'temple'. Nếu chọn 'long', P chỉ cần đổi hằng; ảnh chính diện gần như không đổi.
2. **`c3_views`** các góc khác (±45°, ±90°, ±135°, 180°): số mới theo bảng mục 4 (lệch ≤ 1,1 % nếu 'long'; ≤ 1,0 % so với 'long' nếu 'temple'). Không bắt buộc với 'long'.
3. **Bible `characters.md` (v1.4, chữ, không đổi số):** dòng "Mặt nữ tính (v1.2)": "Cổ áo đứng dựng cao tới cằm" → "Cổ áo đứng dựng cao, **mép cong theo đường hàm, có nếp vải, mép cuộn, lót tối**; cằm tựa vào cổ áo". Nếu chọn 'temple': "3 lọn tóc bạc mềm ở mỗi thái dương (**ngắn, không buông xuống má**)". Chủ dự án duyệt, ghi `AUTHORSHIP.md`.
4. **Tỷ lệ đầu/cổ trong sheet:** không đổi (đầu rộng 0,78 H, cổ 0,30 H). Lưới cổ không đổi hình, chỉ tối màu đỉnh.

## 6. Thời gian render thật (hàng đợi `/var/tmp/cine-queue/log.tsv`; `design/cong5/mat/a1/thoi-gian.txt`)
| Việc (nhãn hàng đợi) | Chờ (s) | Chạy (s) | thoi-gian.txt (s) |
|---|---|---|---|
| b1-truoc-0deg (Ida + Cas, 0°) | 0 | 32,5 | — |
| b1-sau-8goc (lần 1, cổ áo bản 1) | 0 | 316,7 | — |
| mat-a1 lần 1: neutral / sad_smile / choked / nghieng / co-ao_cu-chi | 0 | 18,7 / 18,5 / 14,1 / 16,1 / 18,2 | 18,7 / 18,5 / 14,2 / 16,2 / 18,3 |
| thu-coao-1s (1920×1080, 1 mẫu, thử mép) | 0 | 12,5 | — |
| mat-a1 lần 2 | 0 | 18,7 / 21,2 / 25,9 / 18,8 / 19,6 | 18,8 / 21,3 / 25,9 / 18,9 / 19,7 |
| b1-sau2-8goc (cổ áo cuối, lọn 'long') | 0 | 264,1 | — |
| **mat-a1 lần 3 (bản nộp)** | 0 | **12,5 / 12,9 / 12,3 / 13,0 / 12,3** | **12,5 / 12,9 / 12,3 / 13,1 / 12,3** |
| b1-sau3-8goc (lọn 'temple') | 0 | 287,6 | — |
Mỗi ảnh 1920×1080, 3 mẫu ≈ 12–13 s khi máy rảnh (lần 1–2 chậm hơn do tải máy chung). Tổng việc nặng W3 trong hàng đợi ≈ 17 phút.
Thử nhanh ngoài hàng đợi: 50 thư mục thử (`/var/tmp/cine-out/W3/q`, `ql`), 960×540 hoặc nhỏ hơn, 1 mẫu, 5–12 s mỗi lần; probe layout s31/s39/s37/s13/s05/s30 (≤ 3 khung/shot, 960×540).
**Sai quy trình (tự khai):** 1 lần render 1920×1080, 1 mẫu (~15 s, xong lúc 00:31:17) chạy **ngoài** hàng đợi; hàng đợi khi đó rỗng (không việc nào chồng giờ trong log). Các lần sau đã qua hàng đợi.

## 7. Số lần làm lại
- Cổ áo: 9 vòng thử nhanh (mép thấp lộ cổ → nâng trước → mép tính từ SDF đầu → luồn sau cằm → quét theo độ sâu để mép không cắt ngang má → giảm loe/nếp → cổ tối + luồn 0,10 → dời đường nối ra sau + co/làm mượt mép → co ±16°).
- facelight: 4 vòng (fill quá phẳng → giảm tỷ lệ; lan ra cột/tường → tầm 1,6×; hiệu chỉnh K; elec bỏ viền + K riêng).
- Nét mặt: 1 vòng. Lọn tóc: 2 vòng (tách khỏi da → rút về thái dương).
- Ảnh bản nộp: **3 lần render** (lần 1 lộ vết gãy mép + vết đứt giữa cằm + "lỗ" sáng ở lót khi xem 1080p; lần 2 lọn tóc đọc như vết xước ở ảnh nghiêng; lần 3 nộp).
- B1: 4 lần đo (trước; sau cổ áo bản 1; sau cổ áo cuối; sau lọn 'temple').

## 8. File đã thêm/sửa
- Sửa: `design/cong3/v2/char3d/cast3d.js` (cổ áo, cổ, bóng dưới hàm, lọn tóc + `IDA_WISPS`), `design/cong3/v2/char3d/facepaint.js` (rãnh mũi–má, rãnh khoé miệng, nét tóc thái dương).
- Thêm: `design/cong5/layout/facelight.js`; `design/cong5/mat/{run_mat.sh, still.js, page_mat.js, page_layout_fl.js, .gitignore}`; `design/cong5/mat/a1/*/face_ida.timing.json`, `a1/thoi-gian.txt`; `reports/m2/cong5/w3/*`.
- `cast3d.js` có tuỳ chọn gỡ lỗi `opts.dbgRim` (in đường mép cổ áo ra console; mặc định tắt).
- `RIGHTS.md`: không có tài sản mới (mọi hình, kết cấu, ánh sáng sinh bằng mã) → không thêm dòng.
- Lệnh kiểm của phiên K: không được giao cho gói này; W3 không chạy luật máy (P chạy ở bước D). Không đọc `checks/`.

## 9. Rủi ro
1. **B1 0° −3 %** nếu giữ 'temple' mà không cập nhật `c3_views` → C3 có thể cờ shot chính diện (s36, s37, s39).
2. **Phơi sáng `fl.exposure()`** làm tối cả khung s36/s37 (~4×) và s39 (~2,5×); đổi cảm giác màu đêm (nền sang tím theo grade). Cần P/chủ dự án chấp nhận hoặc chọn K khác.
3. Nếp cổ áo gần như mất dưới ánh điện phẳng (s39) → cổ áo có thể vẫn đọc "trơn" ở ảnh 4 lần kiểm mù (lấy từ s39).
4. Mặt vẫn là vùng sáng nhất khung dưới đèn khí sát mặt; tiêu chí "mặt nạ" có thể còn bị nêu dù ranh giới cằm/cổ đã sửa. Nếu trượt, bước tiếp theo là A3 (chờ lệnh P).
5. Chưa xem chuyển động liên tục của cổ áo (chỉ khung tĩnh và probe ≤ 3 khung): da CPU 0,9 theo đầu có thể làm cổ áo "vặn" khi quay đầu nhanh.

## 10. Việc đang chờ
- **P:** chọn lọn tóc 'temple'/'long'; nếu 'temple' thì cập nhật `c3_views` và khoá SHA; gửi 3 ảnh biểu cảm + ảnh s39 (sau khi W2 gắn facelight) cho kiểm mù lần 4; báo W2 API facelight.
- **Chủ dự án:** duyệt hình cổ áo mới (mép cong theo hàm, nếp, lót tối) và cách dùng phơi sáng không cháy da cho cận mặt; câu chữ bible v1.4 (mục 5.3); ghi `AUTHORSHIP.md`.

---

# A3 — dựng lại nửa dưới mặt (sau kiểm mù lần 4 TRƯỢT tiêu chí "mặt nạ/búp bê")

Căn cứ: `reports/m2/cong5/kiem-mu-mat/lan4.md` (h5, r2, t8: tuổi/giới/cảm xúc đạt; "mặt nạ/búp bê" 3/3). Chỉ đạo chủ dự án qua P: A3, không hạ tiêu chí, sau A3 chỉ 1 lần kiểm mù (3 ảnh dưới + khung s39 của layout).
Đã merge `claude/cine-lab-m2-cong5-layout-24o5fp` (187d4ca, không xung đột). **Đính chính nhỏ cho biên bản lần 4:** ảnh A1 lần 4 ĐÃ dùng facelight `gas` + `expose:"auto"` (xem `design/cong5/mat/run_mat.sh`), nhưng vẫn là khung thử `face_ida` với đèn khí sát mặt và quầng sáng lớp vẽ mặc định — nên nhận xét "tự phát sáng" vẫn đúng. A3 đổi hẳn sang khung phim thật (mục A3.3).

## A3.1 Ảnh (1920×1080, 3 mẫu)
PNG (không commit): `design/cong5/mat/a3/{neutral,sad_smile,choked,nghieng}/face_ida.png`. JPEG: `reports/m2/cong5/w3/a3_{neutral,sad_smile,choked,nghieng}.jpg` (122–156 KB), `a3_so-sanh_lan4-tren_a3-duoi.jpg`, `a3_so-sanh_nghieng_s31.jpg` (s31 animatic v2 | s31 layout với đầu A3 | ảnh nghiêng A3).
Lệnh: `bash design/cong5/mat/run_a3.sh design/cong5/mat/a3` — dựng **đúng shot s37 của layout** (bộ cuối phố, Ida trên thang ở L11, faceCam 85 mm, khung giữa shot f 2350) qua `design/cong5/mat/page_layout_fl.js`, chỉ ghi đè biểu cảm Ida; ảnh nghiêng = cùng khung, máy lệch 80°.

## A3.2 Thay đổi theo 4 nhóm lời chê
| Lời chê lần 4 | Thay đổi (file / chỗ) | Làm được? |
|---|---|---|
| **1. Mặt trứng úp ngược, cằm nhọn, hàm/má không khối, da sáp, nếp như vẽ** | `cast3d.js` `headSDF` nhánh `LOWER_FACE === 'a3'` (hằng `IDA_LOWER_FACE = 'a3'`, `opts.lowerFace` ghi đè; `'a1'` = bản cũ): xương hàm dưới (cành đứng + thân hàm, góc hàm), khối cơ nhai lấp thung lũng gò má–hàm, cằm rộng bo vuông + hõm môi–cằm, má xệ nhẹ dọc đường hàm, đệm mỡ má sát rãnh mũi–má (rãnh là ranh giới KHỐI). Hàm dưới rộng hơn cằm. Đã thử và bỏ: khối dưới cằm (đọc thành cằm đôi/cột cổ), hõm dưới gò má (đọc thành vết bầm). **Biến dạng** (`exprDisp`, nhánh A3): cười buồn — đệm má dồn lên–ra (+0,016/+0,014 H), má xệ nhấc; nghẹn — ụ cằm đẩy lên–ra, môi dưới bĩu, cơ hạ khoé kéo da dưới khoé xuống. **Da:** `facepaint.js` `paintBump` — bản đồ cao độ cùng vị trí nét nhăn (trán, chân chim, dưới mắt, mí, rãnh mũi–má, khoé miệng, dọc môi trên, cằm "da cam" khi nghẹn) + ~9 000 lỗ chân lông/gợn; gắn `bumpMap` (bumpScale 1,2) cho da mặt Ida A3; má hồng nhạt/rộng hơn | Có (hình học + biến dạng + cao độ da). Lưu ý bible C′ ghi "không khắc nếp nhăn vào hình học": A3 **không khắc rãnh**, chỉ thêm khối (xương, mô mềm); nếp nhăn vẫn là nét vẽ, nay có cao độ bump — cần chủ dự án xác nhận cách hiểu này |
| **2. Không thấy cổ, cằm cắm vào cổ áo, mép "lượn sóng như cao su"** | Cổ áo nhánh A3 (`A3C`): mép thấp hơn (hai bên tL + 0,40 thay 0,50; trước ≈ ngay dưới cằm, khe SDF 0,015–0,05 H theo hướng) → dải bóng dưới đường hàm và một đoạn cổ ngắn lộ ra; trọng số theo đầu 0,75; **bỏ gợn sin**, thay 8 nếp GÃY hình chữ V thưa (dạ dày), mép cuộn dày 0,026 × 0,021 H. Cổ da trở lại màu da (0,82–0,96), bóng dưới hàm đậm hơn (che khuất 45 %) | Một phần: có khe bóng + đoạn cổ ngắn; **không** mở cổ dài hơn vì cổ sheet 0,30 H mảnh so với hàm A3 → lộ nhiều đọc thành "đầu to trên que" (đã thử, bỏ). Nếp gãy thấy rõ ở góc nghiêng, ít thấy ở chính diện |
| **3. Mặt sáng rực như tự phát sáng** | Ảnh thử chiếu sáng **như phim**: shot s37 thật + `facelight.js` 'gas' + `fl.exposure()` + **quầng sáng lớp vẽ thấp** `FACE_PAINT = { halation: 0.04, bloomWide: 0.02 }` (mới, xuất từ `facelight.js`; quầng cam dưới vành mũ là nguồn chính của cảm giác "tự phát sáng"). Số đo khung mặt → cả khung: trung vị độ sáng **cả khung 0,019 (lần 4) → 0,154**; mặt 0,49 → 0,31; tỷ lệ mặt/cả khung ≈ **26× → 2×**; điểm ảnh cháy trong mặt 2,0–2,2 % → **0 %** | Có một phần. **Vành mũ đổ bóng lên trán: KHÔNG làm được trong s37 hiện tại** — ngọn L11 ngang tầm mắt, mũ đã đẩy ra sau (quyết định C4), ánh sáng luồn dưới vành. Đã thử bật bóng đèn khí: mặt không đổi đáng kể nhưng in bóng đầu khổng lồ lên tường sau (ám xanh do grade) → không dùng. Thử hạ Ida 0,2 m: tay đèn cắt ngang khung → không dùng. Xem đề xuất A3.5 |
| **4. Tai không thấy; khuyên "dính má"; tóc mảng dẹt; mắt lệch** | Tai Ida vểnh 0,36 rad (0,18 cũ) → thấy mép tai từ chính diện; khuyên: nụ trên dái tai + móc mảnh + giọt thả tự do dưới dái (không đổ bóng — bóng giọt in vết tròn tối trên má); lọn tóc thái dương = bó 5 sợi tròn mảnh tách nhau (thay dải dẹt); `EXPR.asym` giảm một nửa (cười buồn 0,3→0,15, nghẹn 0,2→0,1, gắng 0,15→0,1) | Tai, khuyên, lọn tóc, lệch biểu cảm: **làm được**. Mũ tóc chính (mảng tóc dưới mũ) vẫn là khối liền có rãnh sợi — **không làm** trong A3 (cần dựng lại tóc) |

## A3.3 Đề xuất cho W2/P để phim khớp ảnh thử (W3 không sửa file của họ)
- s36/s37: `const fl = createFaceLight(st.scene, { mode: 'gas' })`, gọi `fl.update(ida, cam)` sau `ctl.update`, `exposure: () => fl.exposure()`, `paintP: { ...PAINT_CLOSE, ...FACE_PAINT }`.
- s39: như trên với `mode: 'elec'`, `keyE: st.whiteHemi.intensity`.
- Không bật bóng L11 trong faceShot (giữ `shadowLamps: []`).

## A3.4 B1 (8 góc, `b1_measure.py`, sau A3 — đầu A3, lọn 'temple', tai vểnh, cổ áo A3)
| Góc | Sheet v1.3 (thân / tay trên / cẳng tay / cẳng chân) | A3 | Lệch thân |
|---|---|---|---|
| **0°** | 2,667 / 1,600 / 0,994 / 0,293 | **2,589 / 1,553 / 0,964 / 0,284** | **−2,9 %** |
| 45° | 2,314 / 1,483 / 0,914 / 0,282 | 2,235 / 1,432 / 0,883 / 0,272 | −3,4 % |
| −45° | 2,315 / 1,466 / 1,299 / 0,282 | 2,233 / 1,414 / 1,253 / 0,272 | −3,5 % |
| 90° | 2,137 | 2,140 | +0,1 % |
| −90° | 2,153 / 1,408 / 1,009 / 0,275 | 2,154 / 1,407 / 1,009 / 0,275 | 0,0 % |
| 135° | 2,386 / 1,465 / 0,825 / 0,272 | 2,355 / 1,446 / 0,814 / 0,269 | −1,3 % |
| −135° | 2,354 / 1,455 / 1,087 / 0,270 | 2,324 / 1,436 / 1,072 / 0,267 | −1,3 % |
| 180° | 2,510 / 1,578 / 1,193 / 0,284 | 2,452 / 1,540 / 1,164 / 0,277 | −2,3 % |
Cas: không đổi. Nguyên nhân: đầu nhìn thấy dài hơn (hàm rộng, tai vểnh, lọn tóc không che mép) — đầu 0° 435,7 → 448,9 px, 45° 470 → 489 px. **Chỉ số trong ±5 % quanh ngưỡng 3 % của C3:** 0°, ±45°, 180° lệch 2,3–3,5 % → P cần cập nhật `c3_views` (P đã nói sẽ đo lại một lần sau A3; số trên sẵn để dùng).

## A3.5 Việc cần P/chủ dự án quyết
1. **Bóng vành mũ lên trán** (lời chê r2): cần đổi layout s37 (hạ Ida so với ngọn L11 và dời tay đèn khỏi khung) hoặc kéo vành mũ xuống trước câu thoại (đụng quyết định C4 "đẩy mũ ra sau"). W3 không tự quyết.
2. Áp `FACE_PAINT` + `fl.exposure()` cho s36/s37/s39 (đổi độ sáng khung và cảm giác lớp vẽ ở cận mặt).
3. Cách hiểu C′ với A3 (khối xương/mô mềm thật + nếp nhăn có cao độ bump, không khắc rãnh) — ghi AUTHORSHIP nếu duyệt; bible v1.4: "hàm dưới rộng hơn cằm, má xệ nhẹ; tai lộ; khuyên treo".
4. `c3_views` mới (A3.4).

## A3.6 Tự rà theo 4 nhóm lời chê (không phải kiểm mù)
| Nhóm | Tự đánh giá | Còn lại / rủi ro |
|---|---|---|
| 1 Mặt/hàm/da | Hàm, góc hàm, cằm, má có khối và bóng khối thật; rãnh mũi–má sâu lên khi cười; cằm co khi nghẹn; da có gợn, nếp có rãnh | Mặt đầy/tròn hơn — có thể đọc "mặt to"; **một mảng bóng xám mềm ở má phải (trái khung)** là bóng khối thật nhưng có thể vẫn bị đọc là vết bầm; nếp dưới mắt vẽ hình chữ V (từ trước) có thể đọc lạ |
| 2 Cổ/cổ áo | Có khe bóng dưới hàm, đoạn cổ ngắn, mép cổ áo dày, không gợn | Chính diện: cổ áo là một đai trơn (nếp gãy chỉ thấy ở góc nghiêng) |
| 3 Ánh sáng | Không còn quầng cam, không cháy, cảnh quanh đọc được (tỷ lệ mặt/khung ~2×) | Mặt vẫn sáng nhất khung (đúng nguồn); **không có bóng vành mũ trên trán** |
| 4 Tai/khuyên/tóc/mắt | Tai thấy từ chính diện, khuyên treo, lọn tóc là sợi, biểu cảm cân hơn | Tóc chính dưới mũ vẫn là khối liền |

## A3.7 Thời gian thật (hàng đợi `/var/tmp/cine-queue/log.tsv`; `design/cong5/mat/a3/thoi-gian.txt`)
| Việc | Chờ (s) | Chạy (s) |
|---|---|---|
| mat-a3 lần 1 (có bóng L11): neutral / sad_smile / choked / nghieng | 0 / 0 / 0 / 0 | 21,8 / 21,7 / 22,4 / 23,8 |
| b1-a3-8goc | 0 | 277,6 |
| **mat-a3 lần 2 (bản nộp)**: neutral / sad_smile / choked / nghieng | **1 009,7 / 1 955,7 / 486,8 / 447,3** (xếp sau W1/W2 canh1–6) | **18,6 / 18,6 / 18,3 / 20,3** |
Chạy thật mỗi ảnh ≈ 18–20 s; tổng thời gian tường lần 2 ≈ 66 phút, gần hết là chờ khoá (khoá `flock` không theo thứ tự đến trước — việc W1/W2 xếp sau vẫn chen trước; P nên biết khi lập lịch). Thử nhanh ngoài hàng đợi (960×540, 1 mẫu, ≤ 12 s): khoảng 35 lần (studio `dev_page`, khung s37, s31/s39 probe).

## A3.8 Số lần làm lại
Hình đầu: 6 vòng (khối đầu → giảm cục → bỏ khối dưới cằm → hõm môi–cằm, thu má xệ/cằm → dời đệm má → thêm khối cơ nhai). Cổ áo: 4 vòng. Ánh sáng: 5 thử (bóng L11, hạ Ida, giới hạn tầm bóng — hỏng, quầng sáng, K = 3). Ảnh nộp: 2 lần render (lần 1 có bóng L11 → vết tròn do bóng khuyên trên má + bóng đầu lớn trên tường).

## A3.9 File
Sửa: `design/cong3/v2/char3d/cast3d.js` (A3: `IDA_LOWER_FACE`, hình đầu, biến dạng, cổ áo `A3C`, cổ, tai, khuyên, lọn tóc bó sợi, bump), `design/cong3/v2/char3d/facepaint.js` (`paintBump`, `EXPR.asym`, má hồng A3), `design/cong5/layout/facelight.js` (`FACE_PAINT`), `design/cong5/mat/page_layout_fl.js` (ghi đè biểu cảm, `charOpts`, `cam`, `K`, `paint`, `shadowKey`, `idaDy`, `hide` — chỉ để thử). Thêm: `design/cong5/mat/run_a3.sh`, `a3/*/face_ida.timing.json`, `a3/thoi-gian.txt`, JPEG A3. Không sửa `PLAN.md`, `bible/`, `ida.json`, `checks/`. `RIGHTS.md`: không có tài sản mới.

---

# A-α — cách điệu mặt–cổ (quyết định chủ dự án sau Cổng 5; A3 không dùng, lưu ở `a3-ma-nguon.patch`)

Làm theo từng bước; cuối mỗi bước 1 ảnh `neutral` (khung phim thật s37), P kiểm mù rồi gửi lại. Worktree đã `reset --hard` về nhánh tích hợp @633a217 (có A1 + layout + facelight trong s36/s37/s39 của W2 + làn nhanh hàng đợi).
Công tắc: `IDA_STYLE = 'aa'` đầu `cast3d.js` (`opts.idaStyle: 'a1'` = bản A1 để so sánh).

## Bước 1 — cổ lộ, cổ áo bẻ thấp mở, khăn thấp, tỷ lệ sọ–mũ
Ảnh: `design/cong5/mat/aa/buoc1/neutral/face_ida.png` (JPEG: `reports/m2/cong5/w3/aa_buoc1_neutral.jpg`). Lệnh: `bash design/cong5/mat/run_aa.sh design/cong5/mat/aa/buoc1 neutral` — dựng đúng shot s37 như layout (facelight 'gas' × EK 2,0, PAINT_CLOSE của W2), chỉ ghi đè biểu cảm; không thêm đèn.

| Mục | Thay đổi (file / chỗ) |
|---|---|
| Cổ lộ thật | `ida.json` (thử trong worktree): **`parts.neck.width_front` 0,30 → 0,46 H** (0,40 vẫn đọc "que" dưới đầu rộng 0,78 H). `cast3d.js` cổ: chân cổ loe ra vai (cơ thang, +0,07 H), gân cổ nhẹ hơn, bỏ lệch trước 0,03 H; màu đỉnh theo độ cao thật: tối sát dưới hàm (bóng hàm, 0,36) sáng dần xuống chân cổ (0,96). Mặt dưới hàm tối hơn (che khuất 0,50). Độ dài cổ giữ 0,30 H |
| Cổ áo thấp, mở | Bỏ cổ áo đứng (nhánh A1 giữ nguyên để so sánh). Cổ áo **bẻ nằm rạp trên vai**: bám mặt thân áo (SDF thân), bán kính trong 0,235 → ngoài 0,43 H, mép trong dựng nhẹ quanh chân cổ, **mở chữ V trước ±0,42 rad**, hai lớp dạ (mặt + lót) + mép ngoài cuộn dày; không theo khớp đầu |
| Khăn thấp | Hai vòng khăn hạ xuống chân cổ, lỏng hơn: (tL + 0,03, r 0,31) và (tL + 0,11, r 0,29), trước thấp hơn sau — che chỗ nối cổ–thân; đuôi và nút giữ nguyên |
| Sọ–mũ | Mũ **ngồi thấp ôm đầu**: gốc mũ 0,86 → **0,80 H** (quanh vòng đầu rộng nhất), miệng mũ 0,56 → **0,52 × bề rộng đầu** (vừa đầu + tóc), vành trước cụp ít hơn (0,13 → 0,05) để không che mắt khi mũ không đẩy. Búi tóc giờ nằm ngay dưới vành sau (đỡ mũ). **Trán sát vành tối dần** (che khuất bởi vành, 0,38 ở y 0,70–0,80 H) |
| Ánh sáng | `facelight.js` 'gas': under 0,12 → **0,04** (dội từ dưới từng xoá bóng hàm trên cổ) |

Tự rà: cổ đọc là cổ (có bóng hàm, loe ra vai), khăn không còn quấn tới cằm, mũ ôm đầu và búi đỡ dưới vành; ở s05 (đèn khí phía trên) vành mũ **đổ bóng thật lên trán**. Còn lại: ở s37 ngọn L11 ngang tầm mắt và shot không bật bóng (file W2) → vành không đổ bóng thật, chỉ có tối che khuất; mặt vẫn sáng nhất khung (phơi sáng của shot × 2,0); mặt, da, tóc chưa đổi (bước 2).
Thời gian (làn nhanh, chờ 0 s): 4 lần render (31,6 / 35,4 / 36,9 / 32,8 s) — làm lại 3 lần (under-fill, bóng dưới hàm, thang màu cổ đặt sai chỗ trong đầu). Thử nhanh ngoài hàng đợi ~14 lần (960×540, 1 mẫu).
Chờ P: kiểm mù ảnh bước 1.

## Bước 2 — cách điệu mặt, da, tóc trắng (+ sửa theo kiểm mù bước 1, `kiem-mu-mat/aa-tung-buoc.md` g3)
Ảnh: `design/cong5/mat/aa/buoc2/neutral/face_ida.png` (JPEG `reports/m2/cong5/w3/aa_buoc2_neutral.jpg`). Lệnh: `EK=1.3 bash design/cong5/mat/run_aa.sh design/cong5/mat/aa/buoc2 neutral` — shot s37 như layout, **chỉ khác hệ số phơi sáng EK 1,3 (layout W2 đang 2,0)**, xem đề xuất ánh sáng dưới.

| Lời chê bước 1 / yêu cầu | Thay đổi |
|---|---|
| Mặt dài, nhọn, cằm "khiên"; giới tính trung tính | `headSDF` nhánh A-α: khối giữa mặt ngắn lại, **má đầy mềm liền gò má** (±0,155; 0,33; 0,21 / 0,10 × 0,14 × 0,10), **cằm tròn nhỏ và cao hơn** (tâm 0,155 H, đáy ≈ 0,06 H → nửa dưới mặt ngắn ~0,04 H), hoà rộng má–cằm (không nếp gãy). Không hàm vuông, không má bạnh |
| Cổ to, dài "ma-nơ-canh" | `ida.json` (thử): cổ **0,46 → 0,40 H**; loe chân cổ 0,07 → 0,05; nếp cổ ngang rõ hơn; vòng khăn trên nâng lên tL + 0,145 → đoạn cổ lộ ngắn lại |
| Tóc "dán", "đầu hói đội mũ", mũ lơ lửng | **Khối tóc bạc**: vỏ tóc bám mặt đầu thật (ở thái dương mặt nhô ra ngoài elip sọ → tóc từng nằm dưới da), dày 0,057 H, phồng thêm ở thái dương–trên tai (+0,05) và gáy (+0,03), giữ độ dày tới chân tóc (chải ra sau); đường chân tóc hạ ở thái dương tới đỉnh tai, nối liền búi; 3–4 lọn chải lớn trong khối. **Bỏ lọn dải dán** (A-α: lọn là một phần khối tóc). Sợi tóc mềm hơn (normal 0,9 → 0,35; gân sợi 0,0045 → 0,0025) |
| Tóc trắng hơn (mục 4) | Màu gốc thử **#b9b3aa → #e2dfda** + **cách điệu "tóc bạc"** trong shader tóc Ida: ánh sáng tới tóc kéo 70 % về trung tính (giữ độ sáng), `opts.hairSilver`. Đo (25 % điểm ảnh tóc sáng nhất, 960×540): **s05** #b9b3aa: sRGB (206,137,68), hue 30°, S 0,58 → chỉ đổi màu #e2dfda: (225,167,98), S 0,68 → **#e2dfda + bạc: (204,174,157), hue 22°, L 0,71, S 0,31**; **s26** (100,64,53) S 0,31 → (133,89,65) S 0,34 → **(112,96,91) S 0,10**. Kết luận: chỉ đổi albedo KHÔNG đủ (ánh lửa hổ phách áp đảo); cần cả cách điệu shader |
| Da nhựa, nếp nhăn nét bút, lông mày một nét, mảng tối trên má, môi vệt mỏng | `facepaint.js` (`o.aa`): **sắc độ** — ~90 loang ấm/lạnh/vàng mềm, thái dương và cằm hơi lạnh, trán vàng nhẹ, má hồng nhạt cao rộng, mũi ấm; vệt cọ cũ nhạt 60 %. **Ít nét**: trán 3 → 2 nếp mềm (α 0,22), chân chim 4 → 2 nét mềm, dưới mắt 2 → 1, bỏ nếp dọc môi trên, bỏ rãnh khoé miệng, bỏ lõi rãnh mũi–má. **Mày** dày mềm hai lớp (12 px + 7 px) + sợi 3D dày hơn. **Môi** đầy hơn (khối môi dưới lớn hơn, sáng giữa môi dưới, bóng dưới môi, khoé môi). Hết mảng tối trên má (má liền gò má, bỏ hõm) |
| Mắt lệch, nhìn trống | Hai nhãn cầu **hội tụ** nhẹ (±0,025 rad; bản cũ phân kỳ 0,1 rad) |
| Hoa tai lơ lửng, tai bị che | Tai vểnh 0,18 → 0,30 (lộ qua tóc); khuyên: nụ trên dái tai + móc + giọt treo dưới dái |
| Mặt sáng rực | **Đề xuất cho W2: EK s36/s37 2,0 → 1,3.** Đo s37 (điểm ảnh mặt có kênh ≥ 250): EK 2,0 **22,9 %**; 1,4 3,2 %; 1,0 0 %. `facelight.js` under 0,04 (từ bước 1). Cột thang cháy sáng bên trái khung s37 là của layout (W2) — ghi lại, không sửa |

Tự rà: mặt tròn–mềm, nửa dưới ngắn, cằm tròn nhỏ; tóc bạc là khối quanh đầu dưới vành, trắng dưới lửa; tai và khuyên treo thấy được; da có sắc độ, ít nét. Còn lại: đầu mày trái còn vài vệt nét ngắn (nếp mí + sợi mày); cổ vẫn là ống đều ở chính diện; mép tóc là một đường đều (hơi "mũ tóc"); mặt vẫn sáng nhất khung (nguồn thật sát mặt).
Thời gian (làn nhanh, chờ 0 s): 2 lần render (32,7 / 29,8 s); làm lại 1 lần (nếp gãy má–cằm, nếp mí). Thử nhanh ngoài hàng đợi ~20 lần (studio + s37/s05/s26, đo màu tóc, đo EK).
Chờ P: kiểm mù ảnh bước 2.

## Bước 3 (cuối) — sửa theo kiểm mù bước 2 (v5) và bộ ảnh cuối
Ảnh (1920×1080, 3 mẫu, shot s37 như layout, **EK 1,3**): `design/cong5/mat/aa/cuoi/{neutral,sad_smile,choked,nghieng}/face_ida.png`; JPEG `reports/m2/cong5/w3/aa_cuoi_{neutral,sad_smile,choked,nghieng}.jpg` (116–134 KB). Lệnh: `EK=1.3 bash design/cong5/mat/run_aa.sh design/cong5/mat/aa/cuoi neutral sad_smile choked nghieng`.

| # | Lời chê v5 | Thay đổi | Làm được? |
|---|---|---|---|
| 1 | Cổ ống, cằm nối cổ gãy gọn | Khối dưới cằm (da chùng nhẹ) dốc mềm về sau–xuống vào cổ; má chùng nhẹ trên đường hàm; cổ **thon lên trên** (−0,022 H), đầu cổ chúi ra trước 0,035 H (dáng người già) nối vào khối dưới cằm; hai dải cơ cổ mờ, nếp ngang; khăn nâng lên (tL + 0,06 / 0,165) → đoạn cổ lộ ngắn | Có — nghiêng: cằm → dưới cằm → cổ liền một đường cong; chính diện: cổ ngắn, thon |
| 2 | Da sáp/nhựa, má–cằm–cổ căng như người trẻ | Cao độ da (bumpMap 0,8): ~12 000 lỗ chân lông + 260 gợn da mỏng ngắn theo chiều chảy xệ (má, dưới mắt, cằm) — **không thêm nét bút**; quầng dưới mắt, đồi mồi nhạt, má chùng hơi sậm (sắc độ) | Có (mức vừa; da vẫn sạch vì cách điệu) |
| 3 | Tóc khối cứng "giấy xếp nếp", mép quanh tai cắt thẳng | Gân sợi đều → gợn lọn không đều (fbm); mép tóc vòng lên quanh tai, phủ sau tai nối búi; mép hơi lởm chởm nhẹ và mỏng dần ở chân tóc; 16 sợi mềm mỗi bên bám mép thái dương–tai | Phần lớn; khối tóc vẫn đọc là "khối" ở ánh sáng mạnh |
| 4 | Tai phải không thấy, khuyên lơ lửng | Tai vểnh 0,40 rad (0,30), tóc vòng lên quanh tai; khuyên nụ + móc + giọt treo ở dái tai | Tai gần thấy rõ; **tai xa bị đầu che ở góc s37 (đầu quay 35°) — không đổi được mà không đổi bố cục** |
| 5 | Mũ lơ lửng, vành không đổ bóng lên trán | Tóc trước hạ xuống dưới băng mũ (mũ **tỳ lên tóc**, không còn khe da giữa vành và trán); dải trán sát vành tối (che khuất 0,38). s37: L11 ngang tầm mắt, mũ đẩy ra sau (C4) → **không có bóng vành thật**; ở s05 (đèn trên đầu) có bóng thật | Một phần — **đề xuất W2: faceShot `shadowLamps: [11]`** (bóng mũi/hàm/tóc thật; vành chỉ đổ bóng khi mũ không đẩy) |
| 6 | Mắt, mày không cân | Nét vẽ đôi dùng **cùng dãy ngẫu nhiên hai bên** (trước đây rung riêng từng bên → hai mày/mắt khác nhau); **bỏ mày sợi 3D** (thành thanh xám, lệch mày vẽ khi nghẹn) — mày vẽ đi theo lưới biến dạng | Có (lệch còn lại do phối cảnh: đầu quay 35°) |
| 7 | Mắt búp bê, thiếu ẩm | Tròng có vân và viền tối; đốm sáng phụ; **bóng mí trên đổ lên nhãn cầu** (màu đỉnh); mí dưới luôn có viền ẩm nhẹ | Có |
| 8 | Cột gỗ cháy cam bên trái | Của layout s37 — **ghi cho W2**, không sửa | — |

### B1 sau A-α (8 góc, `b1_measure.py`, @ bản cuối) — đề xuất `c3_views` Ida
| Góc | Sheet v1.3 thân / tay trên / cẳng tay / cẳng chân | **A-α (đề xuất)** | Lệch thân |
|---|---|---|---|
| 0° | 2,667 / 1,600 / 0,994 / 0,293 | **2,682 / 1,571 / 0,976 / 0,288** | +0,6 % (tay −1,8 %) |
| 45° | 2,314 / 1,483 / 0,914 / 0,282 | 2,290 / 1,474 / 0,909 / 0,281 | −1,0 % |
| −45° | 2,315 / 1,466 / 1,299 / 0,282 | 2,263 / 1,451 / 1,284 / 0,279 | −2,2 % |
| 90° | 2,137 | 2,034 | −4,8 % |
| −90° | 2,153 / 1,408 / 1,009 / 0,275 | 2,060 / 1,398 / 1,000 / 0,270 | −4,3 % |
| 135° | 2,386 / 1,465 / 0,825 / 0,272 | 2,558 / 1,592 / 0,897 / 0,295 | **+7,2 %** |
| −135° | 2,354 / 1,455 / 1,087 / 0,270 | 2,528 / 1,583 / 1,183 / 0,295 | **+7,4 %** |
| 180° | 2,510 / 1,578 / 1,193 / 0,284 | 2,752 / 1,750 / 1,323 / 0,316 | **+9,6 %** |
Cas: không đổi ở mọi góc. Nguyên nhân: mũ ngồi thấp + khối tóc/búi che thêm đầu → phần đầu nhìn thấy (dưới mũ) ngắn đi ở góc sau (180°: 448 → 408 px) và dài ra ở góc nghiêng (±90°: tai vểnh, tóc phồng). **Chỉ số trong ±5 % quanh ngưỡng 3 % của C3:** 0°, ±45° (±2,2 %), ±90° (−4,3/−4,8 %) — cần cập nhật; ±135°, 180° lệch > 5 % → **bắt buộc cập nhật `c3_views`** trước khi chạy luật máy.

### Đề xuất đổi `ida.json` (W3 đã sửa trong worktree các trường đánh dấu ✎ để thử; P sửa bản chính và khoá SHA)
| Trường | Hiện (v1.3) | Đề xuất | Ghi chú |
|---|---|---|---|
| ✎ `parts.neck.width_front` | 0,30 | **0,40** | 0,46 đọc "cổ to"; độ dài 0,30 giữ |
| ✎ `local_colors.hair` | #b9b3aa | **#e2dfda** | cùng cách điệu shader "tóc bạc" (70 %) trong `cast3d.js` (`opts.hairSilver`); chỉ đổi màu không đủ (đo bước 2) |
| `costume.coat.collar` | "cổ đứng cao 0,35 H" | **"cổ bẻ thấp nằm trên vai, mở chữ V trước"** | hình dựng trong `cast3d.js` (A-α), số không đổi |
| `costume.scarf.style` | "khăn len đan quấn cổ, một đuôi buông trước ngực" | + **"quấn thấp ở chân cổ, lỏng"** | |
| `costume.hat` (mới) | — | `seat_H: 0.80`, `fit: 0.52` (miệng mũ / bề rộng đầu), `brim_droop_front` giảm | mũ ngồi thấp ôm đầu, tỳ lên tóc |
| `costume.hair` (mới) | — | `style: "khối tóc bạc chải ra sau quanh đầu, lộ dưới vành ở thái dương–trên tai–gáy, nối búi; lọn thái dương là một phần khối tóc"` | thay 'temple' (lọn dải dán) |
| `c3_views` (Ida) | bảng v1.2 | bảng trên | Cas giữ nguyên |

### Câu chữ đề xuất cho `bible/characters.md` v1.4 (P sửa; chủ dự án duyệt, ghi AUTHORSHIP)
- Dòng **"Mặt nữ tính (v1.2)"** → "**A-α (v1.4):** mặt tròn–mềm cách điệu (má đầy liền gò má cao, cằm tròn nhỏ, nửa dưới mặt ngắn, khối dưới cằm da chùng nhẹ), ít nét nhăn vẽ (2 nếp trán, 2 vết chân chim, 1 nếp dưới mắt, dải rãnh mũi–má mềm), da có sắc độ ấm/lạnh và kết cấu mịn; lông mày dày mềm; môi có khối. Tóc bạc #e2dfda là một khối chải ra sau quanh đầu, lộ dưới vành mũ ở thái dương, quanh tai và gáy, nối búi; tai lộ; hoa tai nụ + giọt treo ở dái tai (vàng cũ #c9a466). Cổ lộ một đoạn ngắn, thon lên trên (rộng 0,40 H). Cổ áo bẻ thấp nằm trên vai, mở chữ V trước; khăn quấn thấp ở chân cổ."
- Dòng **Mũ**: thêm "ngồi thấp ôm đầu, tỳ lên tóc (không đậu trên đỉnh sọ)".
- Dòng **Mặt**: "Không khắc khe miệng/nếp nhăn vào hình học" giữ nguyên (A-α không khắc rãnh; khối má/cằm/dưới cằm là hình khối, không phải nếp).
- Ghi chú cách điệu ánh sáng: "Tóc Ida đọc bạc dưới mọi nguồn (shader kéo sắc ánh sáng về trung tính 70 %)".

### Bảng phơi sáng / facelight đề xuất cho cận mặt (đo 960×540, 1 mẫu, khung giữa shot, bản mặt A-α; "cháy" = % điểm ảnh mặt có kênh ≥ 250)
| Shot | Phơi sáng hiện tại | Cháy hiện tại | Đề xuất | Cháy sau | Ghi chú |
|---|---|---|---|---|---|
| s05 | 0,42 | 20,7 % | **× 0,4 → 0,17** | 2,2 % | đèn khí trên–trước, gần; nền 0,24 → 0,11 (tối hơn) — hoặc thêm facelight 'gas' và dùng `fl.exposure()` |
| s22 | 0,80 | 0,0 % | giữ | 0,0 % | |
| s26 | 3,4 (facelight 'gas') | 0,0 % | giữ | 0,0 % | mặt nhỏ trong khung (MS) |
| s31 | 1,0 | 21,1 % | **× 0,45 → 0,45** | ~1 % (×0,5: 1,6 %; ×0,4: 0,1 %) | đèn lồng sát mặt + trắng; nền 0,73 → ~0,56 |
| s36 | fl.exposure() × EK 2,0 | 16,1 % | **EK 1,3** | ~1,4 % | |
| s37 | fl.exposure() × EK 2,0 | 20,3 % | **EK 1,3** | ~2,9 % (×0,65) | ảnh cuối dùng EK 1,3 |
| s39 | fl.exposure() × EK (elec) | 3,7 % | **× 0,8** | 0,5 % | |
Kèm: `facelight.js` 'gas' under 0,12 → 0,04 (bước 1, đã trong file); **faceShot s36/s37/s39: `shadowLamps: [11]`** (bóng thật); cột thang cháy sáng trái khung s37 (W2).

### Tự rà cuối (4 nhóm lời chê)
Nửa dưới mặt tròn–mềm, nữ, cằm nối cổ liền; da có kết cấu và sắc độ; tóc bạc là khối có lọn, quanh tai; tai gần và khuyên treo thấy được; mắt có chiều sâu và ẩm. Còn lại: mặt vẫn là vùng sáng nhất (nguồn thật sát mặt); không có bóng vành mũ thật ở s37; tai xa khuất; một mảnh tóc nhỏ lẻ ở gáy (góc nghiêng); tóc vẫn hơi "khối" dưới ánh mạnh.

### Thời gian và làm lại (A-α bước 3)
Làn nhanh, chờ 0 s: 2 ảnh thử (24,0 / 23,0 s) + lần 2 (≈ 23 s ×2) + bộ cuối lần 1 (23,5 / 22,8 / 22,7 / 23,1 s) + **bộ cuối nộp (23,1 / 22,9 / 23,3 / 23,1 s)**; B1 8 góc (hàng nặng) 321 s. Làm lại: 3 (mép tóc răng cưa + sợi dựng đứng; mảng hói sau tai; mày sợi 3D thành thanh xám khi nghẹn). Thử nhanh ngoài hàng đợi ~40 lần (studio, s37, bảng phơi sáng 7 shot × 4–6 mức). Lỗi công cụ tự sửa: `rng3` thiếu sau reset; số `bc` không có số 0 đầu làm JSON hỏng (bảng phơi sáng chạy lại).
Tổng A-α: 3 bước, 8 lần render ảnh nộp/thử 1080p, ~75 lần thử nhanh.
