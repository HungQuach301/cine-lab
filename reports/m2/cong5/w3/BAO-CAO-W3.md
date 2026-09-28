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
