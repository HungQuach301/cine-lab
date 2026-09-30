# Cổng 7 — THỬ MẶT Ida cận (phiên xưởng, 30/09/2026)

Câu hỏi: *với da và ánh sáng mức Cổng 7, mặt Ida ở cỡ cận còn đọc là búp bê / sáp / mặt nạ không?*
Nhánh `thu-mat` (từ `2ba73f6`, đầu nhánh P đã gộp W1-v3). **Không merge.** Mọi thay đổi chỉ bật qua cờ `dbg.thuMat = 'v1'`; không đặt cờ thì kết quả **0 px** (mục 4).

## 1. Tóm tắt
- **V1 (three.js trong đường ống hiện có): xong.** Có mp4 3 shot, dải kiểm mù cùng mốc và cùng số khung như vòng 2, ảnh trước/sau, số đo.
- **V2 (EEVEE có SSS): DỪNG trước khi dựng** vì hạn token (mục 7). Không có sản phẩm V2.
- Số đo chính: **s03 mặt cháy 86,9 % → 3,5 %**; điểm ảnh trắng bệch 5,5 % → 0 %. s22 bớt cam: C* 16,1 → 12,4. s05 vệt đỏ ở má giảm, nhưng mặt tối đi (L* 40,6 → 29,9; đây là rủi ro).
- Nhận định của xưởng, **chưa qua kiểm mù**: s03 cải thiện rõ nhất, vì mặt hết là "mảng trắng hồng" và đọc được mắt, mũi. s05 và s22 ở cỡ 480 px chỉ đổi vừa phải. Phần "sáp / búp bê" ở s22 có lẽ đến một phần từ **hình khối** (không nếp nhăn tuổi, thái dương trơn), mà phần này xưởng không được đổi (xem đề xuất ở mục 8).

## 2. Cách làm V1 và lý do chọn thông số
Phát hiện khi đọc mã: đầu Ida trong phim là **'bl'** (`IDA_STYLE='bl'`, glb v1.5.1). Vật liệu da thật nằm ở `design/cong3/v2/char3d/blender/bl_head.js` (`skinMaterial`), không phải `facerig.js` (facerig.js là đầu 'ai' cũ, phim không dùng). Tệp này không có trong `LOCK-THIET-KE.sha256`; glb và json vẫn giữ nguyên.

**2.1 Da (`skinMaterialV1`, chỉ cho da đầu và cổ Ida; tay dùng vật liệu cũ):**
- *Bọc sáng hẹp, lệch đỏ:* `wr = (0,20; 0,06; 0,04)`, mũ 1,5 (bản cũ `(0,30; 0,14; 0,10)`, tuyến tính). Bản cũ bọc cả độ sáng nên da đọc như sáp. Bản mới chỉ để kênh đỏ tràn qua vùng chuyển sáng–tối và giữ vùng tối sâu hơn.
- *Xuyên sáng theo bề dày:* mặt nạ vùng trong hệ toạ độ lưới (đơn vị H, lấy từ đo glb): tai (|x| > 0,37; y 0,20–0,62), chóp và cánh mũi (z > 0,43), mí. Mỗi đèn cảnh thật cộng thêm `pow(dot(V, −(L + 0,35N)), 3)` với màu (1; 0,30; 0,17). Tai và mũi đỏ lên khi nguồn nằm sau hoặc bên cạnh.
- *Bóng gương:* hai thùy (88 % thùy chính và 12 % thùy hẹp có độ nhám × 0,65), hệ số 0,75 (bản cũ 0,3, da đọc như đất sét). Độ nhám lấy từ kênh alpha đỉnh sẵn có của glb, dải `mix(0,42; 0,78)` (bản cũ 0,45–0,85), nên vùng chữ T bóng hơn má. Có nhiễu ±15 %. Thử `0,36–0,72` với thùy hẹp 0,22 thì má lấp lánh như mồ hôi, nên đã bỏ.
- *Màu da:* giảm bão hoà albedo còn 0,82. Có loang thủ tục hai tầng (±4 %, lệch đỏ–vàng) và vài đốm tuổi mờ ở trán. Tai, mũi và má hồng hơn (mức 0,55). Quanh hốc mắt tối và lạnh hơn (mức 0,6). Không thêm tài sản ảnh; tất cả đều là thủ tục.
- *Cuộn sáng da mềm:* đồng phục `uKnee/uCap`, chỉ bật ở s03 (0,4/1,0).

**2.2 Tone và phơi sáng theo shot (`design/cong7/thu-mat/v1.js`, bảng `SHOT`):** ở s03, khi L4 bắt lửa (9,2 s), phơi sáng giảm còn 0,5 lần trong 0,4 s, tương tự máy quay thích nghi, cộng với cuộn sáng da. Thử mức 0,62/0,55 thì mặt vẫn cháy 47 %. Mức 0,5/0,4 cho 3,5 %. Tường vôi cũng tối đi; điều này khớp với lời chê "sáng như ban ngày" ở s03, nhưng là tác động phụ cần P và chủ dự án xem.

**2.3 Ánh dội từ nguồn có thật:** ở mỗi khung, xưởng chụp môi trường cảnh bằng CubeCamera 128 px, HDR, đặt tại tâm đầu Ida và ẩn chính Ida, rồi qua PMREM để làm `envMap`. **Không thêm đèn nào.** Ánh dội chỉ là ánh của tường, khăn, lồng đèn và trời có sẵn trong cảnh. Da nhận 30 % phần khuếch tán (facelight của s05 đã lo phần dội chính) và toàn bộ phần gương, nên có ánh ướt ở góc sượt theo Fresnel. Việc chụp lại ở mọi khung giữ hàm thuần theo khung, không sinh trạng thái ẩn. s22 vẫn giữ ánh điện phẳng, không có đèn khí.

**2.4 Vi chuyển động (chỉ dùng kênh facerig có sẵn, cộng lên trọng số của shot):**
- Saccade 2 khung, dừng 0,3–1,15 s, biên độ ±2° ngang và ±0,9° dọc (hạt giống theo shot).
- Mí trên theo mắt khi nhìn xuống (`lidDrop` 0,45 × góc).
- Mày trôi chậm theo nhiễu 0,45–0,7 Hz (±0,05) và nhấn theo độ mở miệng.
- Má và mắt nheo nhẹ theo lời (`cheekRaise` 0,12, `squint` 0,06).
- Thở: môi hé theo nhịp 3,4 s khi im.
- Chớp bổ sung: s03 có 1 chớp đủ và 1 chớp nửa (trước đây không chớp); s05 thêm 1 chớp nửa ở 12,42 s.
- Tần số chớp (đếm theo lịch):

| Shot | Trước | V1 |
|---|---|---|
| s03 | 0/2 s | 2/2 s (1 đủ + 1 nửa) |
| s05 | 3/4 s (45/phút) | 4/4 s (60/phút, trong đó 1 nửa) |
| s22 | 3/3 s | 3/3 s (không thêm) |

Tần số chớp ở s05 và s22 đã cao hơn mức tự nhiên (15–20/phút khi im, cao hơn khi nói). Vì vậy V1 không thêm chớp đủ, chỉ làm cho chớp không đều.

**2.5 Mắt ướt (`eyeMaterial`, khi cờ bật):** clearcoat 1,0 và nhám 0,04 (bản cũ 0,45/0,2), phản chiếu `envMap` thật, nên điểm sáng nằm đúng hướng nguồn. Phần gương của clearcoat bị che bởi bóng mí trên theo cùng hệ số AO với tròng (gián tiếp × AO², trực tiếp × mix(1; AO; 0,6)), tạo dải tối của mí trên trên giác mạc. Gương nền của nhãn cầu giảm × 0,5·AO để khỏi phủ một lớp "sữa". Hình mắt không đổi.

## 3. Tệp mã đã đổi
- `design/cong3/v2/char3d/blender/bl_head.js`: thêm `skinMaterialV1` và `THU_V1`; nhánh V1 của `eyeMaterial`; bật V1 ở `buildBL` chỉ khi `kind === 'ida'` và cờ chứa 'v1'.
- `design/cong5/layout/page.js`: đặt `globalThis.CINE_THU_MAT` từ `dbg.thuMat`; nạp `cong7/thu-mat/<cờ>.js` khi có cờ; `window.__cine` (chỉ để đo mặt nạ, không vẽ).
- Mới: `design/cong7/thu-mat/v1.js` (ánh dội môi trường, phơi sáng theo shot, vi chuyển động), `frames.js` (driver render theo khung dải kèm mặt nạ da mặt), `do_mat.py` (đo và ghép ảnh), `dong_goi.py` (cháy phụ đề như `package.py`, rồi lập dải).
- `PLAN.md`: thêm mục 5 vào hàng chờ (đề xuất cần chủ dự án quyết).
- **Không đổi:** `shots_w1.js`, `facerig.js`, `cast3d.js`, `facelight.js`, glb/json đã khoá, `bible/`, `checks/`. RIGHTS.md không đổi vì không có tài sản mới (mọi kết cấu đều thủ tục).

## 4. Kiểm 0 px (không đặt cờ)
So bản render của nhánh `thu-mat` với cây `design/` của `2ba73f6` (lấy bằng `git archive`), cùng driver, 1 khung mỗi shot:

| Shot | Khung | Số điểm ảnh khác |
|---|---|---|
| s02 | 150 | 0 |
| s21 | 1160 | 0 |
| s22 | 1212 | 0 |
| s05 | 312 | 0 |

## 5. Số đo trước/sau (trong mặt nạ da mặt nhìn thấy, sau toàn bộ đường ống, 960×540)
"Trước" là nhánh không cờ, bằng v22 hiện hành (0 px so với `2ba73f6`). Cùng các khung của dải. s03 chỉ tính 2 khung sau khi đèn bật (1,0 s và 1,5 s); 2 khung đầu mặt là bóng đen (L* ≈ 2–4) ở cả hai bản. Số liệu thô: `reports/m2/cong7/thu-mat/V1/so-do-da.json`.

| Shot | Bản | % cháy (kênh ≥ 250) | % trắng bệch | L* TB | L* p5–p95 (tương phản) | a* / b* | C* TB | C* độ lệch chuẩn |
|---|---|---|---|---|---|---|---|---|
| s03 | trước | **86,9** | 5,5 | 87,6 | 59,9–97,8 (37,9) | 10,9 / 22,9 | 26,3 | 20,5 |
| s03 | V1 | **3,5** | 0,0 | 65,9 | 36,3–84,2 (47,9) | 25,6 / 38,5 | 47,1 | 9,6 |
| s05 | trước | 0 | 0 | 40,6 | 14,0–71,9 (57,9) | 31,0 / 32,3 | 45,4 | 9,7 |
| s05 | V1 | 0 | 0 | **29,9** | 4,4–66,6 (62,2) | 27,1 / 24,6 | 37,3 | 13,5 |
| s22 | trước | 0 | 0 | 39,4 | 18,5–60,0 (41,5) | 10,3 / 12,2 | 16,1 | 3,6 |
| s22 | V1 | 0 | 0 | 38,7 | 22,6–61,6 (38,9) | 8,4 / 9,1 | 12,4 | 3,0 |

Cách đọc bảng:
- s03: mặt từ trắng cháy chuyển sang hổ phách có khối (tương phản tăng 10 L*). C* tăng là do màu ánh đèn khí nay không còn bị cháy mất.
- s05: bớt đỏ cam (C* 45 → 37) và vệt đỏ ở má dịu đi, nhưng **mặt tối đi 10 L*** và bóng dưới hàm gần đen (p5 = 4,4).
- s22: bớt cam, tương phản gần như giữ nguyên. Biến thiên màu (C* SD) không tăng, vì loang da thủ tục quá nhỏ ở cỡ khung này.
- **Chỉ số trong vùng ±5 % quanh ngưỡng:** không có. Không có ngưỡng luật nào được đo ở đây; các số trên chỉ là số mô tả.

## 6. Chi phí render mỗi khung (960×540, 1 mẫu, 4 vCPU swiftshader, chạy trong hàng đợi làn nặng)

| Shot | v22 (P, TB) | V1 TB | V1 trung vị | Hệ số |
|---|---|---|---|---|
| s03 | 2,02 s | 4,64 s | 3,25 s | ×1,6–2,3 |
| s05 | 2,07 s | 2,48 s | 2,33 s | ×1,1–1,2 |
| s22 | 1,00 s | 1,89 s | 1,76 s | ×1,8–1,9 |

Phần chi phí thêm chủ yếu là chụp môi trường mỗi khung (6 mặt × 128 px + PMREM) và morph CPU mỗi khung cho vi chuyển động. Ước tính cho 140 s phim: với khoảng 35 % thời lượng có Ida cận hoặc trung, tổng thời gian render layout tăng khoảng 30–50 %. Có thể giảm nếu chụp môi trường 128 → 64 px, hoặc chỉ chụp khi đèn cảnh đổi trạng thái (cần hàm thuần theo trạng thái đèn).

## 7. V2 (EEVEE có SSS): DỪNG, chưa dựng
- **Lý do:** hạn chung cho V1 và V2 là 300 nghìn token. Đến lúc xong V1 (mã, 3 lượt tinh chỉnh, render, đo, đóng gói) đã dùng khoảng 225 nghìn. Phần còn lại (khoảng 75 nghìn) không đủ để dựng lại cả cảnh.
- **Việc phải làm cho V2** (đường `eevee_4goc.sh` hiện chỉ xuất nhân vật):
  1. Xuất máy quay (vị trí, hướng, fov) và đèn cảnh (vị trí, màu, cường độ, tầm) theo khung, tốt nhất thêm vào `frameMeta`.
  2. Xuất glb Ida theo tư thế từng khung (có sẵn `"export":1`).
  3. Dựng trong EEVEE: Principled có SSS cho da, đèn khớp nguồn thật, grade gần ACES và grade C.
  4. Ghép lên nền three.js của đúng khung đó. Cần mặt nạ che (mũ, tay, cột đèn) lấy từ độ sâu của three.js.
- Ước tính khoảng 100–150 nghìn token cho 15 khung dải, rủi ro chính là khớp máy quay và che khuất.

## 8. Rủi ro và đề xuất cho Cổng 7
**Rủi ro:**
- (a) s05 tối đi 10 L*, nên mặt có thể bị chê "chìm". Cách chỉnh: tăng `S05_EK` hoặc tăng `envDiff`; chưa làm vì hạn.
- (b) Tai đỏ xuyên sáng làm tai nổi hơn. Ở s22, tai đã bị chê "to và nổi rõ".
- (c) s03 hạ phơi sáng làm tường tối theo. Đây là một quyết định ánh sáng cảnh, cần chủ dự án duyệt.
- (d) Vi chuyển động nhỏ (±2°) có thể không thấy ở dải 480 px với khung cách 0,5 s. Kiểm mù bằng dải ảnh tĩnh đo chuyển động rất kém.
- (e) Chi phí render ×1,2–2,3.

**Đề xuất:**
- **V1 khả thi cho 140 s phim** với chi phí render tăng khoảng 30–50 %, không đổi tài sản đã khoá, và bật được theo shot.
- Nếu kiểm mù V1 còn chê "sáp/búp bê" ở s22, nguyên nhân còn lại nằm ở **hình khối và thiết kế**:
  - Không có nếp nhăn tuổi. Có thể thêm bằng bản đồ pháp tuyến ở trán, đuôi mắt, rãnh má; việc này đổi diện mạo tuổi nên cần chủ dự án quyết.
  - Thái dương trơn, đọc là "hói". Sửa phần này cần mở khoá tóc v1.5.1.
  - Hai việc trên đã ghi vào hàng chờ trong PLAN.md (mục 5). Xưởng không tự làm.
- V2 chỉ đáng làm nếu V1 trượt vì lý do vật liệu, chứ không phải vì hình khối.

## 9. Sản phẩm
- mp4 (có phụ đề như layout): `reports/m2/cong7/thu-mat/V1/s03.mp4`, `s05.mp4`, `s22.mp4`
- Dải kiểm mù: `reports/m2/cong7/thu-mat/V1/dai_s03.jpg` (4 khung), `dai_s05.jpg` (8), `dai_s22.jpg` (6). Cùng số khung với `reports/m2/cong6/w1/kiem-mu-v2/dai_*.jpg`.

| Dải | Mốc phim (giây) |
|---|---|
| s03 | 8,5 → 10,0 (hết shot 10,5) |
| s05 | 12,0 → 15,5 (hết 16,0) |
| s22 | 49,5 → 52,0 (hết 52,5) |

- Ảnh trước/sau cùng khung (cả khung và cận mặt): `truoc-sau_s03_f240.jpg`, `truoc-sau_s05_f324.jpg`, `truoc-sau_s22_f1188.jpg`
- Số đo: `so-do-da.json`
- Lệnh tái tạo:
  - `bash scripts/render/queue.sh W-thu-mat V1 -- node design/cong7/thu-mat/frames.js --shot <s> --out <dir> --all --mask --dbg '{"thuMat":"v1"}'`
  - rồi `/opt/cine/bin/python design/cong7/thu-mat/dong_goi.py <dir> reports/m2/cong7/thu-mat/V1`

## 10. Kiểm mù
*(để trống — P điền)*

## Token
Phiên xưởng: khoảng 235 nghìn token (V1 khoảng 235 nghìn, V2 0).
