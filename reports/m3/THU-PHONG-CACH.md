# M3 — THỬ PHONG CÁCH cho kênh "Last Lamplighters" (01/10/2026)

**Phiên:** xưởng THỬ PHONG CÁCH, theo P giao (chỉ thị chủ dự án 01/10/2026).
**Nhánh:** `thu-phong-cach`, gốc `ebdacde`. KHÔNG merge, KHÔNG push.
**Tên kênh:** "Last Lamplighters", chủ dự án chọn 01/10/2026, thay tên tạm "Lamplight". Khẩu hiệu gợi ý: "Every era has its last lamplighters".

**Kết luận ngắn:**
- Cả hai biến thể đã làm đủ 3 sản phẩm: dải s03/s05/s22, khung dữ liệu, đoạn 20 s. Mỗi biến thể có thêm dải kiểm mù thứ 4 và khung 1080 cho từng shot.
- Tắt cờ thì 0 px ở s03, s05, s22.
- **B3 (cắt giấy / bóng) đáp ứng đúng hướng "không cận mặt người"**: nhân vật đọc thành bóng, ánh đèn khí thành mảng ấm bậc thang, bóng đổ mạnh.
- B1 (toon + viền nét) cho hình sạch và mắt đọc rõ, nhưng vẫn để lộ mặt ở cỡ cận. Đây đúng là vùng đã trượt kiểm mù 3 vòng.
- Mục "Kiểm mù" để trống cho P.

---

## 1. Cách làm

### 1.1 Cơ chế cờ (chung cho hai biến thể)
- `design/cong5/layout/page.js` (+7/−3 dòng) chỉ nạp `design/m3/thu-phong-cach/style.js` khi `dbg.style` có giá trị (`'b3'` | `'b1'`).
- Khi không có cờ: `STY = null`, `sty = null`, mọi nhánh mới bị bỏ qua, nên lớp vẽ, grade và grain giữ nguyên như v22. Kết quả kiểm ở §5.
- Ba điểm móc:
  - `install()` sau khi dựng shot và đặt grade;
  - `frame()` sau `update` của shot, dùng để đổi máy hoặc phơi sáng;
  - `post()` sau bước lớp vẽ, trước pass cuối (tone map, grade, grain chung không đổi).
- Shot phụ `lp20` (đoạn 20 s) chỉ tìm thấy khi có cờ (`STY.extraShot`), nên không lọt vào bảng shot phim.
- Driver render theo khung: `design/m3/thu-phong-cach/frames.js`. Driver này học từ `cong7/thu-mat/frames.js` và thêm `--page-file` để render bằng page.js gốc ebdacde làm đối chứng 0 px.

### 1.2 B3 "2.5D cắt giấy / vẽ tay / bóng" (ƯU TIÊN)
Hậu kỳ một pass trên ảnh HDR tuyến tính, dùng G-buffer riêng siêu lấy mẫu 2×. G-buffer gồm độ sâu nhìn, mặt nạ nhân vật và mặt nạ tấm số liệu. Bỏ lớp Kuwahara của hướng C vì mảng phẳng đã thay vai trò đó.

1. **Mảng sáng bậc thang:**
   - lượng tử hoá log-độ sáng trên ảnh nhoè nhẹ (σ 1,0 px nửa độ phân giải), bậc 0,85 stop, mép bậc mềm ±0,07;
   - sắc độ lấy từ ảnh nhoè với độ bão hoà 0,82, giữ 32 % chi tiết độ sáng gốc;
   - bậc tối ngả mực lam, bậc sáng ngả hổ phách.
   - Kết quả: ánh đèn khí thành các vành ấm phẳng.
2. **Nhân vật thành bóng cắt giấy:**
   - mặt nạ nhân vật tô mực tối, độc lập phơi sáng;
   - mép nhân vật nơi được đèn chạm giữ viền hổ phách mảnh (≈ 1,7 px), không để lộ chi tiết mặt.
3. **Tách lớp theo độ sâu:**
   - bóng đổ giấy mềm xuống-phải khi lớp phía trên-trái gần hơn ≥ 20 % (dài 9 px, 5 mẫu);
   - chỉ giấy sáng mảnh ở mép lớp hướng về ánh;
   - mép cắt "tay" nhờ lệch toạ độ lấy mẫu G-buffer theo nhiễu chậm cố định.
4. **Kết cấu giấy THỦ TỤC:**
   - nhiễu nhiều tầng cộng thớ sợi kéo dài, mỗi lớp độ sâu một "tờ" lệch hạt giống;
   - cố định theo không gian, bù trượt máy ngang theo độ sâu. Không phụ thuộc số khung, nên không nhấp nháy (đo ở §4.3).
   - Grade: tắt lớp "canvas" của hướng C (`gCanvas = 0`), giữ vignette và grain chung.
5. **Đổi máy để tránh cận mặt** (bảng `B3_CAM` trong `style.js`; lưới, rig, diễn hoạt giữ nguyên):

| Shot | v22 | B3 | Lý do |
|---|---|---|---|
| s03 | MS thấp, trước mặt, 50 mm | WS 3/4 cạnh, thấp, 40 mm | Ida trên thang thành bóng nhỏ; ngọn L4 nở thành mảng ấm là nhân vật chính của khung |
| s05 | MCU 3/4 trước (mặt), 85 mm | MS nghiêng hẳn (profile) từ phía −x, 35 mm | Bóng nghiêng Ida + hai lòng tay trước lồng kính; giữ phía máy cùng s21/s22 (−x) |
| s22 | MCU 3/4 (mặt), 85 mm | MWS thấp từ lòng phố, phía −x, 35 mm | Bóng đen trên mặt tiền trắng ánh điện, đúng ý "trắng dìm hổ phách" |

   - s05 chạy với `dbg.s05 = 'none'` để tắt facelight (đèn dội mặt cận). Facelight tính theo máy cận cũ, không còn ý nghĩa khi đã thành bóng; phơi sáng 0,42 như nhánh không facelight.
6. **Đoạn 20 s (`lp20`, `lamp_shot.js`):**
   - dùng lại `buildStreetSet` đêm (đoạn x 34–90), Ida + đèn lồng cầm tay (`holdOut`), `walkPose`, `lanternLight`;
   - Ida đi vào từ trái (thấy nghiêng-sau, cỡ trung–xa), quay lưng về máy, giơ đèn soi tấm bản đồ, rồi lia sang tấm biểu đồ;
   - vũng sáng là đèn rọi đặt tại đèn lồng (cách điệu: đèn lồng có chụp), kèm quầng gần yếu;
   - hai tấm giấy dán tường dùng vật liệu Lambert thường, nên chỉ hiện ra trong vũng sáng;
   - cột đèn khí đổ bóng mạnh lên tường;
   - máy trượt ngang chậm và đẩy nhẹ (parallax người, cột đèn, mặt tiền); 1280×720, 24 fps, không tiếng.
7. **Khung dữ liệu (`data_frame.py b3`):**
   - 1920×1080, sinh thủ tục: lớp mái nhà cắt giấy có bóng đổ, vũng sáng bậc thang, cột đèn bóng, hai tờ giấy mép xé dán chéo;
   - tên kênh "LAST LAMPLIGHTERS", khẩu hiệu, dòng trục nội dung "Then: 14 lamplighters became 1. Now: which jobs are next?";
   - nhãn "Illustrative data" ở khung và trên từng tờ.

### 1.3 B1 "toon + viền nét" (3D)
- Giữ máy gốc, lưới, rig, diễn hoạt.
- **Vật liệu:**
  - mọi `MeshLambert`, `Standard` và `Phong` đổi sang `MeshToonMaterial`, cùng màu, map và emissive;
  - `gradientMap` 3 bậc: cảnh [0,16; 0,55; 1,0], nhân vật [0,30; 0,68; 1,0].
  - Vật liệu Basic (lửa, kính, sprite) giữ nguyên.
- **Viền nét:**
  - G-buffer pháp tuyến + độ sâu siêu lấy mẫu 2×;
  - Laplace độ sâu tương đối (ngưỡng 0,06) và độ lệch pháp tuyến (ngưỡng 0,45), mảnh dần sau 25–90 m;
  - nét mực = 8 % màu nền + đen lam.
- **Mảng màu có kiểm soát:** trộn 50 % × 0,65 ảnh nhoè nhẹ (σ 1,6) giữ tỉ lệ độ sáng, để nén chi tiết vi mô (da, vải).
- Bỏ lớp Kuwahara, `gCanvas = 0`.
- Đoạn 20 s: cùng shot `lp20`, chỉ đổi hậu kỳ.
- Khung dữ liệu (`data_frame.py b1`): mảng phẳng, viền đen 6 px, không hạt giấy, không mép xé, ô chữ toon.

## 2. Tệp mã đổi / thêm
| Tệp | Nội dung |
|---|---|
| `design/cong5/layout/page.js` | +7/−3: 3 điểm móc sau cờ `dbg.style` (không cờ thì 0 px) |
| `design/m3/thu-phong-cach/style.js` | B3 (G-buffer, bậc thang, bóng, viền cắt, giấy, máy thay thế), B1 (toon, viền, mảng) |
| `design/m3/thu-phong-cach/lamp_shot.js` | shot `lp20` 20 s |
| `design/m3/thu-phong-cach/frames.js` | driver render theo khung (+ `--page-file` đối chứng) |
| `design/m3/thu-phong-cach/data_frame.py` | tấm số liệu, khung dữ liệu B3/B1, đo tương phản |
| `design/m3/thu-phong-cach/data/panel_{map,chart}.png` | tấm giấy dùng trong `lp20` (tự tạo) |
| `design/m3/thu-phong-cach/{dai4,so_px,truoc_sau,bang_do,on_dinh}.py` | dải thứ 4, so 0 px, ảnh trước/sau, bảng thời gian, đo nhấp nháy |
| `RIGHTS.md` | + mục M3-TPC-1: tấm số liệu tự tạo, font C4-F1 |

- Không sửa `checks/`, `bible/`, hay tài sản trong `LOCK-THIET-KE.sha256`. Không đọc mã `checks/`.
- Không thêm tài sản ngoài: giấy, mép xé, mái nhà và vũng sáng đều sinh bằng mã; chữ chỉ dùng DejaVu Sans Regular (C4-F1).

## 3. Sản phẩm (`reports/m3/thu-phong-cach/`)
| | B3 | B1 |
|---|---|---|
| Dải s03 / s05 / s22 | `B3/dai-s03-b3.jpg`, `dai-s05-b3.jpg`, `dai-s22-b3.jpg` | `B1/dai-s03-b1.jpg`, `dai-s05-b1.jpg`, `dai-s22-b1.jpg` |
| mp4 trọn shot 960×540 | `B3/s03-b3.mp4`, `s05-b3.mp4`, `s22-b3.mp4` | `B1/s03-b1.mp4`, `s05-b1.mp4`, `s22-b1.mp4` |
| Khung 1920×1080 mỗi shot | `B3/khung1080-s0{3,5}-b3.png`, `khung1080-s22-b3.png` | `B1/khung1080-…-b1.png` |
| Khung dữ liệu 1920×1080 | `B3/khung-du-lieu.png` | `B1/khung-du-lieu.png` |
| Đoạn 20 s (1280×720, 24 fps, crf 18) | `B3/doan20s-b3.mp4` (16,5 MB) | `B1/doan20s-b1.mp4` (15,9 MB) |
| Dải kiểm mù thứ 4 (10 khung bước 2,0 s + khung dữ liệu) | `B3/dai4-du-lieu-b3.jpg` | `B1/dai4-du-lieu-b1.jpg` |
| Ảnh trước (v22) / sau, cùng khung 222 · 324 · 1224 | `B3/truoc-sau-b3.jpg` | `B1/truoc-sau-b1.jpg` |

**Ghi chú dải:**
- mp4 là trọn shot, bắt đầu ở mốc đầu shot. Vì vậy dải lấy mốc tương đối 0 → 1,5 s (s03), 0 → 3,5 s (s05), 0 → 2,5 s (s22), bước 0,5 s.
- Các mốc này trùng mốc phim 8,5 → 10,0, 12,0 → 15,5, 49,5 → 52,0 s như các vòng trước.

## 4. Số đo

### 4.1 Giây render mỗi khung
Đo trong hàng đợi làn nặng (`scripts/render/queue.sh`, nhật ký `/var/tmp/cine-queue/log.tsv`, gói `W-tpc`), bằng cùng driver, không chạy song song. Tệp gốc nằm ở `do/*.timing.json`.

| Shot (960×540) | v22 (TB · trung vị) | B3 | B3/v22 | B1 | B1/v22 |
|---|---|---|---|---|---|
| s03 (48 khung) | 2,65 · 2,11 | 2,36 · 1,84 | 0,89 | 2,34 · 1,81 | 0,88 |
| s05 (96 khung) | 1,81 · 1,65 | 1,36 · 1,19 | 0,75 | 1,38 · 1,23 | 0,76 |
| s22 (72 khung) | 1,57 · 1,43 | 0,96 · 0,85 | 0,61 | 1,18 · 1,09 | 0,75 |
| lp20 1280×720 (480 khung) | — | 1,54 · 1,42 | — | 1,62 · 1,42 | — |

- Khung 1920×1080 đơn lẻ: 8,6–10,1 s, gồm khởi động khung đầu (khung đầu mọi lượt ≈ 8–10 s).
- **Cả hai biến thể nhanh hơn v22 11–39 %** vì bỏ lớp Kuwahara, dù thêm một G-buffer 2×.
- Chuỗi 1080p chưa đo thành chuỗi; ước ≈ 3,5–5 s/khung, cần đo thật trước khi chốt giờ máy.

### 4.2 Tương phản chữ (khung dữ liệu, đo trên ảnh: màu chữ / nền trung vị)
`B3/tuong-phan.txt`, `B1/tuong-phan.txt`. Ngưỡng 4,5:1.

| Nhóm chữ | B3 | B1 |
|---|---|---|
| Tiêu đề, tên kênh | 11,5:1 | 15,1:1 |
| Dòng Then/Now | 14,3:1 | 16,8:1 |
| "Illustrative data" | 14,3:1 | 16,8:1 |
| Chữ bản đồ / biểu đồ (mực trên giấy) | ≈ 13–15:1 | ≈ 13:1 |

- Cặp thiết kế: mực/giấy 13,0:1, kem/navy 13,7:1.
- Chữ nhỏ nhất trên khung dữ liệu ≈ 16–18 px cao ở 1080p (chú giải bản đồ, nhãn năm).
- Trong đoạn 20 s ở 720p, chỉ số lớn ("46", "14 → 1", số trên cột) đọc được; chữ chú giải trên tờ giấy KHÔNG đọc được. Xem rủi ro R4.

### 4.3 Ổn định theo thời gian (không nhấp nháy)
`do/on-dinh.txt`: chênh lệch luma giữa hai khung liên tiếp, đo trên vùng tĩnh chung, đơn vị mã 8 bit.

| Shot | v22 | B3 | B1 |
|---|---|---|---|
| s05 (93 % khung tĩnh) | 1,32 | 1,22 | 1,35 |
| s22 (65 % khung tĩnh) | 1,25 | 1,09 | 1,37 |
| s03 (3 % khung tĩnh, L4 bắt lửa) | 1,05 | 1,13 | 0,99 |

Mức còn lại chủ yếu là grain chung của đường ống (σ 1,5 mã, đổi theo khung). Kết cấu giấy B3 không thêm nhấp nháy.

### 4.4 Token
**Cách quy đổi:** đọc bộ đếm `total_tokens left` của công cụ trước và sau từng phần. Bộ đếm này gộp mọi lượt đọc mã, viết mã, xem ảnh và chạy lệnh của phiên.

| Phần | Token |
|---|---|
| Khởi động, đọc mã nền (dùng chung) | ≈ 30 nghìn |
| B3 (gồm hạ tầng chung: frames.js, style.js, lp20, data_frame.py; 5 lượt thử; render; dải; đo 0 px) | ≈ 195 nghìn |
| B1 (gia số: thử 1 lượt, render, khung dữ liệu, dải) | ≈ 30 nghìn |
| Báo cáo | ≈ 15 nghìn |
| **Tổng phiên** | **≈ 270 nghìn** (hạn 400 nghìn) |

**Token mỗi phút phim:**
- Phim mỗi biến thể = 9 s Last Round (render lại, không diễn hoạt mới) + 20 s đoạn mới + 1 khung dữ liệu ≈ 0,5 phút.
- B3 tính cả hạ tầng: (30 + 195) nghìn / 0,48 phút ≈ **0,47 triệu/phút**. Đây là chi phí của bài thử, phần lớn trả MỘT LẦN cho hạ tầng.
- B1 gia số khi hạ tầng đã có: 30 nghìn / 0,48 ≈ **0,06 triệu/phút** (chỉ đổi hậu kỳ, không có shot mới).
- Riêng đoạn `lp20` (shot mới hoàn toàn, 4 lượt thử): ≈ 45 nghìn / 0,33 phút ≈ **0,14 triệu/phút**. Đây là số gần nhất với sản xuất thật.

### 4.5 Ước công sức một tập 10 phút theo mẫu B3
Giả định:
- 60 % truyện (6 phút, ≈ 72 shot × 5 s), 40 % số liệu (4 phút, ≈ 12 nhịp × 20 s);
- tối đa 1 lượt sửa mỗi shot;
- xem ảnh thử ở 960 px dạng lưới 2×2.

| Hạng mục | Dùng lại | Mới | Token (ước) | Giờ máy (ước) |
|---|---|---|---|---|
| Hạ tầng phong cách (style.js, driver, lp20) | đã có | tinh chỉnh R1–R3 | 40 nghìn | 1 |
| Shot truyện ×72 | bộ phố/tường/ngõ/phòng, rig Ida và Cas, dáng đi/thang/đèn lồng, hậu kỳ B3 | máy, dàn dựng, nhịp mỗi shot | 72 × ≈ 10 nghìn ≈ 0,72 triệu | 8 640 khung × 3,5–5 s ≈ 8,5–12 h (1080p) |
| Khuôn số liệu (bản đồ, cột, đường, bộ đếm) | data_frame.py | 3–4 khuôn mới, một lần | ≈ 150 nghìn | — |
| Nhịp số liệu ×12 | khuôn | nội dung, số, bố cục | 12 × ≈ 15 nghìn ≈ 0,18 triệu | ≈ 0,5 h |
| Kịch bản, VO (ElevenLabs), nhạc/SFX + RIGHTS, mix, phụ đề, QA | quy trình Cổng 4–6 | — | ≈ 0,15–0,25 triệu | ≈ 1–2 h |
| Luật máy, kiểm mù (P/K) | luật v1.5 | — | ngoài xưởng (≈ 0,5 triệu mỗi lượt kiểm mù, CONG-6 §7) | ≈ 1,7 h |
| **Tổng xưởng** | | | **≈ 1,25–1,35 triệu → ≈ 0,13 triệu/phút** (tập đầu ≈ 0,14) | **≈ 12–17 h** |

**So với tiêu chí:**
- **≤ 0,3 triệu token/phút:** ước 0,13–0,14 triệu/phút; dư gấp ≈ 2 lần cho lượt sửa phát sinh. Nếu cộng một lượt kiểm mù (≈ 0,5 triệu) thì ≈ 0,18 triệu/phút. Chưa có chỉ số nào nằm trong ±5 % quanh ngưỡng.
- **Một chu kỳ hạn mức tuần:**
  - giờ máy ≈ 12–17 h trên một làn nặng: vừa trong một tuần, kể cả khi container khởi động lại;
  - token ≈ 1,3–1,8 triệu: Cổng 6 dùng ≈ 4,3 triệu trong 3 ngày, nên khả thi;
  - P cần đối chiếu với số hạn mức tuần thật.
- **Độ bất định lớn nhất:** số lượt sửa mỗi shot. Bài thử này cần 4–5 lượt cho shot mới đầu tiên (`lp20`), do phải dựng ngôn ngữ hình. Mỗi lượt sửa thêm cho cả 72 shot ≈ +0,07 triệu/phút.

## 5. Kiểm 0 px khi tắt cờ
`kiem-0px.txt`:
- page.js gốc ebdacde (`--page-file`) và page.js nhánh này khi không có cờ;
- render cùng khung s03 f222, s05 f324, s22 f1224 ở 960×540;
- **lệch 0 điểm ảnh, lệch lớn nhất 0, ĐẠT.**
- Ảnh gốc render nối tiếp cả shot; ảnh kiểm render một khung đơn lẻ. Vì vậy phép so đồng thời xác nhận tính tất định của từng khung.
- Không có lệnh kiểm K riêng cho gói này; theo chỉ thị, không chạy kiểm mù.

## 6. Rủi ro
| # | Biến thể | Rủi ro | Mức | Gợi ý |
|---|---|---|---|---|
| R1 | B3 | s05: bóng Ida chìm vào nền tối; ba nhịp tay hơ kính khó đọc; bóng Ida đổ lớn lên tường đọc như "bóng trùm đầu / bóng ma" | cao cho s05 | dàn dựng riêng cho bóng (đèn sau lưng tạo viền, tay ngược sáng trước kính), không dùng lại blocking cận mặt |
| R2 | B3 | ô kính cửa sổ thành mảng "bong bóng" khi bậc thang hoá ở tiêu cự dài (đã giảm khi nhoè 2,6 → 1,0) | vừa | mặt nạ chi tiết riêng cho cửa sổ, hoặc kết cấu mặt tiền phẳng hơn ở phiên bản B3 |
| R3 | B3 | lp20 16–18 s: Ida (bóng) gần như biến mất trên tường tối | vừa | viền ấm mạnh hơn khi nhân vật đứng ngoài vũng sáng; đèn lồng sáng hơn ở tay |
| R4 | cả hai | chữ nhỏ trên tờ giấy trong đoạn 20 s không đọc được ở 720p; "Illustrative data" trong clip chỉ có trên tờ giấy (nhỏ) | vừa | tờ giấy trong cảnh chỉ giữ 1–2 số lớn; chi tiết để ở khung dữ liệu; thêm thẻ "Illustrative data" trên lớp chữ cuối |
| R5 | B3 | kết cấu giấy bù trượt máy NGANG; khi đẩy vào hay xoay máy, giấy trượt nhẹ ("cửa kính tắm") | thấp | neo kết cấu theo UV thế giới (triplanar) nếu tập dùng nhiều máy chuyển động |
| R6 | B1 | mặt vẫn lộ ở MCU (s05 nghiêng, s22 cận); bậc tô trên da tạo mảng loang (đốm tuổi bị bậc hoá) | cao | nếu chọn B1, vẫn phải áp luật "không cận mặt" của hướng mới; chỉnh map da phẳng |
| R7 | cả hai | ánh rọi từ đèn lồng là cách điệu (đèn lồng thật toả đều) | thấp | ghi vào luật thế giới của kênh nếu chủ dự án chấp nhận |
| R8 | đo | giờ máy 1080p của tập mới là ước; mới đo khung đơn lẻ 1080 | vừa | đo một shot trọn ở 1080p trước khi chốt |

## 7. Đề xuất
1. **Chọn B3 làm ngôn ngữ truyện của kênh.**
   - Ưu: tránh hẳn vùng mặt đã trượt kiểm mù; đọc ngay là "minh hoạ cắt giấy"; nhanh hơn v22 11–39 %; dữ liệu và truyện chung một chất liệu (giấy, hổ phách, mực lam).
   - Nhược: mất biểu cảm mặt, nên cảm xúc phải dồn vào dáng, nhịp, ánh sáng và tiếng; s05 cho thấy blocking cũ (thiết kế cho cận mặt) không tự chuyển thành bóng hay.
   - Tác động: kịch bản tập thử phải viết cho bóng và cỡ trung–xa ngay từ đầu.
2. **Dùng nét của B1 cho đồ hoạ số liệu nếu cần độ đọc cao hơn**, ví dụ khung dữ liệu toàn màn hình. Không dùng B1 cho nhân vật cận.
3. **Bước nhỏ tiếp theo** (trước tập thử, ≈ 40–60 nghìn token):
   - sửa R1, R3 bằng một mẫu viền ngược sáng;
   - sửa R2;
   - đo một shot 1080p trọn;
   - P chạy kiểm mù 4 dải mỗi biến thể;
   - chủ dự án chấm khung 1080.
4. Tách luật "đèn lồng rọi" thành mục luật thế giới của kênh nếu được duyệt.

## 8. Việc chờ chủ dự án
Xưởng không sửa PLAN.md. Đề nghị P đưa các mục sau vào hàng chờ:
- **Chấm hình** 6 khung 1080 (3 × B3, 3 × B1) và 2 khung dữ liệu; tiêu chí ≥ 8/10.
- **Chọn biến thể** (đề xuất B3) và duyệt các quyết định sáng tạo:
  - đổi cỡ cảnh s03, s05, s22 (§1.2.5);
  - đèn lồng "rọi" cách điệu (R7);
  - tên kênh và khẩu hiệu trên khung dữ liệu;
  - số liệu minh hoạ (46 đèn, 14 → 1 người thắp đèn).
- Ghi các quyết định đã duyệt vào AUTHORSHIP.md.

## 9. Kiểm mù (P điền, 01/10/2026)

**Cách chạy**
- 8 dải biến thể (mỗi biến thể 3 dải Last Round + 1 dải dữ liệu / đoạn 20 s) và 2 đối chứng Sprite Fright dùng chung.
- Mỗi dải do một subagent MỚI (general-purpose) chấm.
- Câu hỏi nguyên văn như các vòng trước, **thêm** "Chấm chất lượng hình ảnh 1–10 so với phim hoạt hình chuyên nghiệp, nêu một lý do." (hỏi cả đối chứng). Hai dải dữ liệu hỏi thêm "Bạn nhớ được những số liệu nào?".
- Nguyên văn: `thu-phong-cach/kiem-mu/NGUYEN-VAN.md`. Tên mù: `kiem-mu/map.tsv`.
- Token: 44,0–46,6 nghìn mỗi dải; 10 dải = **449,7 nghìn** (hạn 450 nghìn; sát ngưỡng, −0,06 %, trong ±5 %).

**Kết quả**
| Dải | Từ khoá chê (máy đếm) | Điểm 1–10 | Lời chê chính (rút gọn) |
|---|---|---|---|
| B3 s03 | 0 | 5 | đèn bật như "bật công tắc"; quầng sáng loang lổ "như vết bẩn hay vân giấy"; nhân vật chìm vào nền tối; bóng thang to, đặc. Khen: "phong cách cắt giấy nhất quán" |
| B3 s05 | 0 | 5 | bóng tiền cảnh "khối đen phẳng… như hình cắt dán", không được đèn hắt sáng; gần như đứng yên 3 s; người thắp đèn lẫn vào tường. Khen: bảng màu tím/vàng |
| B3 s22 | 0 | 5 | đèn cạnh nhân vật tối mà tường có mảng sáng hình nón "không rõ từ đâu"; gần như không chuyển động; khung hơi xê dịch |
| B3 dữ liệu + 20 s | 0 | 4 | vùng sáng quá to, xa đèn lồng; nhân vật tan vào tối ở 14–18 s; viền sáng phân tầng (banding); thẻ kết đổi phong cách |
| B1 s03 | 0 | 5 | ánh sáng nhảy gắt, cả tường sáng đều "như ban ngày"; mặt cháy; bóng lạ |
| B1 s05 | 0 | 5 | tay áo dài bất thường, tay nhảy vị trí; mặt "đơ", chỉ có môi cử động; ánh sáng chưa "chạm" nhân vật |
| B1 s22 | 0 | **4** | **mặt: đổ bóng "vỡ thành các mảng loang lổ"** như vết bẩn hay vết bầm; răng "nhọn lởm chởm… như răng nanh"; "tư thế cứng, giống tượng" |
| B1 dữ liệu + 20 s | 0 | 5 | vệt sáng elip viền sắc "như đèn sân khấu"; nhân vật quá nhỏ; cột cuối biểu đồ đổi màu |
| Đối chứng Ellie (104) | 0 | 8 | ánh sáng ấm, chất liệu "gần phim chiếu rạp" |
| Đối chứng Victoria (332) | **"mặt nạ"** | 5 | mi mắt dính khối "giống mặt nạ"; da "như nhựa" |

| Tổng hợp | B3 | B1 | Đối chứng |
|---|---|---|---|
| Dải có từ khoá chê (búp bê / mặt nạ / sáp / con rối / rẻ tiền…) | **0/4** | **0/4** | 1/2 |
| Lặp lời chê cùng chỗ | **ánh sáng đèn: quầng/vùng sáng không khớp nguồn, bật đột ngột** (4/4 dải); **nhân vật chìm vào nền tối / bóng phẳng không được chiếu** (4/4) | ánh sáng nhảy hoặc không khớp nguồn (3/4); mặt và miệng ở cỡ cận (s22; s05 "đơ") | — |
| Điểm trung bình | **4,75** | **4,75** | 6,5 (8 và 5) |
| Nhớ số liệu (dải dữ liệu) | **đủ**: 46 đèn, 14 → 1, cả 6 phố và 6 năm; nhận ra "Illustrative data" | **đủ** (như B3) | — |

**Đọc kết quả (P)**
1. **Hết lời chê "búp bê / mặt nạ / sáp"** ở cả hai biến thể. Đây là lần đầu từ Cổng 6. Với B3 là do bỏ mặt (nhân vật thành bóng). Với B1, s22 vẫn lộ mặt và bị chê "loang lổ", "răng nanh", "tượng", tức là không có từ khoá nhưng vẫn là lỗi mặt cận.
2. **Điểm chất lượng còn thấp: 4,75/10 cho cả hai**, so với đối chứng 6,5 (Ellie 8). Tiêu chí tập thử của chủ dự án là chủ dự án chấm ≥ 8/10; người xem mù hiện chấm thấp hơn nhiều.
   - Gốc lặp lại nhất là **ánh sáng**: vùng sáng không khớp nguồn đèn, bật như công tắc, banding.
   - Kế đến là **nhân vật quá tối hoặc bất động** (B3: bóng phẳng không được hắt sáng, không viền ngược sáng; xưởng đã tự nêu rủi ro này ở §6 và đề xuất thêm viền ngược sáng).
3. **Số liệu được nhớ rất tốt:** cả hai người xem dải dữ liệu chép lại đủ 46 đèn, 14 → 1 và câu kết. Tiêu chí (4) "nhớ ≥ 2 số liệu" đạt rõ trên hai dải này.
4. **Hạn chế của phép thử:** dải khung tĩnh cách 0,5–2 s chấm "đứng yên" nặng tay. Các shot Last Round vốn ít chuyển động, và chuyển động mượt không thấy được trên tờ ghép.

**Đề xuất (chờ chủ dự án quyết)**
- **Chọn B3 làm hướng phần truyện** (không còn mặt nên không còn rủi ro "búp bê"), kèm một lượt sửa nhỏ nhắm đúng hai lời chê lặp:
  - (a) ánh sáng có lý: vùng sáng bám nguồn đèn, có thời gian "bắt lửa" khoảng 0,3–0,5 s, bỏ banding ở viền;
  - (b) bóng nhân vật có viền ngược sáng hoặc ánh hắt ấm từ đèn, cùng một chuyển động thở hoặc tay nhỏ;
  - ước ≈ 40–80 nghìn token, rồi kiểm mù lại 4 dải B3 + 2 đối chứng (≈ 270 nghìn).
- Đồ hoạ số liệu: giữ ngôn ngữ B3 nhưng bỏ "đèn pha" elip, cho chữ và số ổn định một phong cách với thẻ kết.
- **B1 không đề xuất cho phần truyện** vì mặt cận vẫn lộ lỗi.
