# M3 — B3 v2 (sửa nhỏ sau kiểm mù Mốc 1) · kênh "Last Lamplighters" (01/10/2026)

**Phiên:** xưởng THỬ PHONG CÁCH, lượt B3 v2 do P giao. Chủ dự án đã chấm B3 ≥ 8/10, chọn B3 cho phần truyện, và duyệt đổi cỡ cảnh s03/s05/s22 cùng đèn lồng rọi (AUTHORSHIP 01/10/2026).
**Nhánh:** `thu-phong-cach` (push, KHÔNG merge). Cờ mới: `dbg.style = 'b3v2'`.
**Mã:** `design/m3/thu-phong-cach/style_v2.js` (tệp riêng). `style.js` chỉ thêm 1 dòng điều phối và 1 dòng import, nên B3 v1 và B1 giữ nguyên mã. Kết quả 0 px ở §3.

## 1. Việc a–e

### a. Ánh sáng bám nguồn
- **Gốc lỗi Mốc 1:** bước bậc thang hoá áp lên cả VÂN VẬT LIỆU (tường, ô kính), nên sinh vệt "loang/ố" không theo đèn nào.
- **v2 chỉ bậc thang hoá ÁNH SÁNG:**
  - lấy độ sáng nhoè rộng (1/8 độ phân giải, σ ≈ 24 px ảnh đầy), xấp xỉ chiếu sáng vì vân đã bị trung bình hoá;
  - lượng tử hoá log-độ sáng đó;
  - nhân tỉ lệ lên ảnh gốc làm phẳng nhẹ (55 %), nên vân tường giữ nguyên và không còn mảng ố.
- **Hết phân dải:**
  - bậc nhỏ hơn (0,85 → 0,55 stop), mép bậc mềm (±0,07 → ±0,24);
  - thêm dither tam giác TĨNH theo điểm ảnh (0,28 bậc), cộng grain chung của đường ống.
- Vũng sáng giờ giảm dần từ đúng ngọn đèn hoặc đèn lồng trong khung (ảnh trước/sau ở §2).
- **Thời gian lan sáng:**
  - đèn khí giữ nhịp "phụp" nở trong 0,35 s của layout (`gasLevel`, không đổi, nằm trong khoảng 0,3–0,5 s);
  - ở v1, bậc thang thô làm nhịp này đọc thành "bật công tắc"; v2 bậc mịn nên đọc thành lan sáng;
  - đèn lồng `lp20` sáng dần trong 1,2 s.

### b. Bóng nhân vật có khối
- Viền sáng mép bóng lấy màu và độ sáng của ánh quanh mép, từ chính nguồn trong khung. Có hai vành, 2,2 px và 4,5 px; mạnh hơn ở phía có đèn.
- Thân có khối mờ: độ sáng nhoè, tối đa ≈ 1,9 × mực, KHÔNG dùng màu da. Nhờ vậy nếp áo và khối vai có, nhưng không lộ nét mặt.
  - Lượt thử đầu dùng 22 % màu gốc thì lộ mặt ở s03/s05, nên tôi đã bỏ.
- **Chuyển động nhỏ:**
  - s03, s05, s22 giữ diễn hoạt duyệt (đã có thở `breathe`);
  - `lp20` (chỉ khi cờ b3v2) thêm thở (cột sống ±1,4°, chu kỳ 3,4 s), tay cầm đèn chao ±1,5°, đèn lồng đung đưa (±0,10 rad khi đi, ±0,045 rad khi đứng).
  - Áo: không thêm, vì rig không có xương vạt áo (giữ nguyên rig).

### c. s22: ánh điện có hướng (luật thế giới v0.6)
- Giảm ánh trắng tràn phẳng (đèn bán cầu "whiteHemi") còn 22 %.
- Cột điện mé đối diện (x = 29, z = +3,9, đang bật trong s22) thành nguồn chính, có hướng, giảm theo khoảng cách, và ĐỔ BÓNG (bản đồ bóng 1024).
- Phơi sáng bù × 1,7.
- Kết quả: bóng Ida và thang đổ dài lên mặt tiền; tường sáng giảm dần, hết mảng trắng xanh phẳng.
- Không thêm đèn khí; L10 vẫn bắt lửa ở khung cuối như layout.

### d. Đoạn 20 s
- **Tấm chữ trong cảnh làm lại cho 720p** (`data/panel_{map,chart}_v2.png`, chỉ nạp khi cờ b3v2):
  - còn 1 tiêu đề, 1 số lớn ("46 gas lamps", "14→1"), 3 cột (1890 · 1905 · 1920);
  - chữ nhỏ nhất ≈ 15 px cao ở 720p;
  - giữ "Illustrative data" trên cả hai tấm.
- Tương phản đo trong vùng sáng: §4.2.
- **Bỏ dạng "đèn pha elip viền sắc":**
  - đèn rọi rộng hơn (0,38 → 0,56 rad), bán ảnh 0,5 → 1,0, tức mép tắt dần liên tục;
  - quầng gần của đèn lồng mạnh hơn (2 → 6), nên vũng sáng bắt đầu từ đèn lồng và lan lên tường;
  - nhắm cao hơn để tiêu đề tấm nằm trong vùng sáng.
- **Hết phân dải** (như mục a).
- Khung dữ liệu 1080 v2: vũng sáng liên tục theo khoảng cách từ ngọn đèn vẽ trong khung (1/(1+(4,2 r)²)), có dither, bỏ các vành bậc.

### e. Giữ nguyên
- Lưới, rig, diễn hoạt không đổi.
- Ngoài cờ b3v2, mọi thứ lệch 0 px (§3).
- Không sửa `checks/`, `bible/`, tài sản khoá.
- Không thêm tài sản ngoài: tấm v2 sinh bằng mã, font DejaVu Sans (C4-F1); RIGHTS.md thêm M3-TPC-2.

## 2. Sản phẩm (`reports/m3/thu-phong-cach/B3v2/`)
| Loại | Tệp |
|---|---|
| Dải kiểm mù (cùng mốc, cùng cách làm Mốc 1) | `dai-s03-b3v2.jpg`, `dai-s05-b3v2.jpg`, `dai-s22-b3v2.jpg`, `dai4-du-lieu-b3v2.jpg` |
| Khung 1080 trước (B3) / sau (B3v2), mỗi cặp 3840×1080 | `truoc-sau-1080-s03.jpg`, `-s05.jpg`, `-s22.jpg`, `-du-lieu.jpg` |
| Khung 1080 riêng | `khung1080-s03-b3v2.png`, `khung1080-s05-b3v2.png`, `khung1080-s22-b3v2.png`, `khung-du-lieu-b3v2.png` |
| Clip 20 s mới (1280×720, 24 fps, crf 18) | `doan20s-b3v2.mp4` |
| mp4 trọn shot 960×540 | `s03-b3v2.mp4`, `s05-b3v2.mp4`, `s22-b3v2.mp4` |
| Đo | `kiem-0px-v2.txt`, `tuong-phan-clip.txt`, `tuong-phan-khung.txt`, `../do/b3v2-*.timing.json` |

## 3. Kiểm 0 px (`B3v2/kiem-0px-v2.txt`)
| Phép so | Khung | Kết quả |
|---|---|---|
| Tắt cờ: page.js gốc ebdacde vs nhánh (sau mọi sửa v2) | s03 f222, s05 f324, s22 f1224 | **0 px** |
| Cờ B1: bản Mốc 1 vs sau v2 | s05 f324; lp20 f240 (720p, kiểm 3 lần: sau sửa v2 đầu, sau sửa nhắm đèn, sau bản cuối) | **0 px** |
| Cờ B3 v1: bản Mốc 1 vs sau v2 | s22 f1224 | **0 px** |

## 4. Số đo

### 4.1 Giây render mỗi khung (làn nặng, TB · trung vị)
| Shot | v22 | B3 (Mốc 1) | B3 v2 |
|---|---|---|---|
| s03 960×540 | 2,65 · 2,11 | 2,36 · 1,84 | 2,30 · 1,75 |
| s05 960×540 | 1,81 · 1,65 | 1,36 · 1,19 | 1,32 · 1,17 |
| s22 960×540 | 1,57 · 1,43 | 0,96 · 0,85 | 1,31 · 1,19 (thêm bóng của đèn cột điện) |
| lp20 1280×720 | — | 1,54 · 1,42 | 1,59 · 1,47 |

- Khung 1080 đơn lẻ: 8,6–11,5 s, gồm khởi động khung đầu.
- B3 v2 vẫn nhanh hơn v22 ở cả ba shot.

### 4.2 Tương phản chữ
**Đoạn 20 s:** đo trong vùng sáng, chữ = trung vị 3 % điểm tối nhất, nền = trung vị 40 % điểm sáng nhất của ô. Kết quả đầy đủ ở `tuong-phan-clip.txt`.
- Lượt clip đầu: "46" 5,3:1; số trên cột 8,3:1. Tiêu đề tấm ("OLD TOWN, 1905", "14→1") chỉ 2,9:1 vì nằm ở mép vũng sáng.
- Đã thêm hai lượt sửa: nhắm đèn cao hơn và lệch sang trái, tiêu đề tấm 64 → 84 px. Số đo bản cuối:

| Thời điểm · nhóm chữ | Tương phản | Đánh giá |
|---|---|---|
| 10,0 s · "46" + "gas lamps" | 5,1:1 | ĐẠT |
| 15,0 s · số trên cột + năm | 8,3:1 | ĐẠT |
| 15,0 s · "14→1" | 5,4:1 | ĐẠT |
| 15,0 s · "LAMPLIGHTERS" | 7,0:1 | ĐẠT |
| 8,0 / 10,0 / 12,0 s · "OLD TOWN, 1905" | 3,8 / 4,1 / 4,2:1 | **TRƯỢT** (mép trên-trái vũng sáng) |

- **"OLD TOWN, 1905" vẫn dưới ngưỡng.** Vũng hổ phách chỉ đưa giấy tới độ sáng tương đối ≈ 0,14, và nét chữ mảnh bị khử răng cưa.
- Cách sửa (chưa làm, vì giữ hạn token):
  - hạ tiêu đề vào giữa tấm, hoặc tăng đèn rọi ≈ +40 %;
  - hoặc chuyển tiêu đề sang dạng mực trên nền giấy sáng dán riêng.
- Số "46" (5,1:1) và "14→1" (5,4:1) cao hơn ngưỡng 13–20 %. Tiêu đề 4,1–4,2:1 thấp hơn ngưỡng 7–9 %, ngay ngoài vùng ±5 % nhưng gần; tôi nêu tên ở đây theo luật.

**Khung dữ liệu v2** (`tuong-phan-khung.txt`):
| Nhóm chữ | Tương phản |
|---|---|
| Tiêu đề | 12,4:1 |
| Then/Now | 14,3:1 |
| "Illustrative data" | 14,3:1 |
| Chữ trên giấy | ≈ 13–15:1 |

## 5. Rủi ro còn lại
- **Quầng nhẹ quanh bóng nhân vật:** ánh nhoè rộng bị bóng tối kéo xuống ngay sát mép, tạo vành sáng mờ ≈ 10 px. Trông như mép giấy, nhưng có thể bị đọc là "hào quang". Cách sửa: loại điểm ảnh nhân vật khỏi bước nhoè rộng (≈ 10 nghìn token).
- **s05:** bóng Ida đổ lớn trên tường vẫn là một mảng tối lớn bên trái khung (đúng nguồn L4, nhưng bố cục nặng).
- **Tấm số liệu thấy mờ ngoài vũng sáng ở 0 s** (ánh trời đêm): chủ ý giữ, để người xem biết có "gì đó" trên tường trước khi đèn tới.
- **Tiêu đề tấm bản đồ trong clip 3,8–4,2:1** (§4.2).
- **Ánh trắng s22:** hệ số 0,22 và phơi sáng × 1,7 chỉnh cho riêng s22. Shot ánh điện khác trong tập cần chỉnh cùng cách (tham số `dbg.hemiK`, `dbg.s22exp`).

## 6. Token
**Cách đo:** bộ đếm `total_tokens left` của công cụ, từ khi nhận lượt v2 đến khi viết xong báo cáo.

| Phần | Token |
|---|---|
| Mã v2 (style_v2, lp20, tấm v2, khung dữ liệu v2) | ≈ 20 nghìn |
| 3 lượt thử + xem ảnh | ≈ 20 nghìn |
| Render, đóng gói, 0 px, đo, 3 lượt sửa clip (nhắm đèn, chữ tiêu đề) | ≈ 35 nghìn |
| Báo cáo | ≈ 10 nghìn |
| **Tổng lượt v2** | **≈ 90 nghìn** (hạn 120 nghìn) |

**Quy ra phim:** 9 s Last Round + 20 s clip + 1 khung dữ liệu ≈ 0,5 phút, tức ≈ 0,18 triệu token/phút cho một lượt sửa toàn bộ. Nằm trong mức "≤ 0,3 triệu/phút"; không có chỉ số nào nằm trong ±5 % quanh ngưỡng.

## 7. Việc chờ chủ dự án
Đề nghị P đưa vào hàng chờ PLAN.md:
- chấm 4 cặp ảnh 1080 trước/sau;
- duyệt cách sửa s22 (ánh điện đổ bóng từ cột mé đối diện);
- duyệt tấm chữ đơn giản hoá trong đoạn 20 s (3 cột thay 6).

## 8. Kiểm mù (P điền, 01/10/2026)

**Cách chạy**
- 4 dải B3 v2, mỗi dải một subagent MỚI, câu hỏi như Mốc 1 (kèm câu chấm 1–10; dải dữ liệu thêm câu nhớ số liệu). Nguyên văn: `thu-phong-cach/kiem-mu-v2/NGUYEN-VAN.md`; tên mù: `map.tsv`.
- **Đối chứng dùng lại kết quả Mốc 1** (cùng 2 dải Sprite Fright, cùng câu hỏi, cùng ngày): Ellie 8, Victoria 5 ("mặt nạ").
  - Lý do: 6 subagent tốn ≈ 270 nghìn token, vượt hạn kiểm mù 200 nghìn. Đây là sai lệch so với chỉ thị "4 dải + 2 đối chứng", P ghi rõ.
- Token: 4 dải = **180,1 nghìn** (hạn 200 nghìn).

**Kết quả**
| Dải | B3 (Mốc 1) | **B3 v2** | Lời chê B3 v2 (rút gọn) |
|---|---|---|---|
| s03 | 5 | **5** | ánh sáng vẫn "bật như công tắc" (0,5 s → 1,0 s); **nhân vật "như bóng ma… nửa trong suốt"** ở 0,0–0,5 s; bóng trên tường to và lệch; tường trái tách cứng với vùng sáng |
| s05 | 5 | **4** | **người thắp đèn "trong suốt như bóng ma"**; bóng tiền cảnh vẫn "phẳng tuyệt đối… như lỗ cắt dán"; quầng đèn **vẫn có vòng đồng tâm (banding)**; nửa dưới đen kịt; gần như bất động |
| s22 | 5 | **4** | "đèn ngay cạnh cô không sáng, vậy mà tường bị rọi trắng gắt như có đèn pha… nguồn sáng tạo ra bóng không thấy ở đâu"; bóng thang không khớp vật thật; người và bóng đen phẳng như nhau |
| Dữ liệu + 20 s | 4 | **5** | biểu đồ in lên tường "giống slide thuyết trình"; quầng sáng ở tường chứ không ở đèn lồng; đèn lồng "viền sáng rỗng" ở 0 s; thẻ kết "khác phong cách"; chữ nhỏ mờ. **Nhớ số liệu: đủ** (46 đèn; 14 → 1; cả 6 năm; câu kết) |
| **Trung bình** | 4,75 | **4,50** | |

**Chấm theo tiêu chí của chủ dự án**
| Tiêu chí | Kết quả | |
|---|---|---|
| 0 lời chê "búp bê / mặt nạ / sáp / rẻ tiền" lặp cùng chỗ | 0/4 dải có các từ này (máy chỉ bắt "khác phong cách", nói về thẻ kết) | **ĐẠT** |
| Điểm TB không thấp hơn 4,75 | **4,50** (−5,3 %, sát ngoài ±5 %) | **CHƯA ĐẠT** |

**Đọc kết quả (P)**
1. **Hai sửa có tác dụng:**
   - dải dữ liệu 4 → 5 điểm; số liệu vẫn được nhớ đủ;
   - lời chê "vết ố / loang lổ" trên tường không còn.
2. **Sửa (b) gây lỗi mới lặp lại: "bóng ma, nửa trong suốt"** ở 2/4 dải (s03, s05). Gốc là "khối thân mờ không dùng màu da" cùng quầng ≈ 10 px quanh bóng mà xưởng đã nêu rủi ro ở §7. Bóng chính ở tiền cảnh s05 vẫn đọc "phẳng như cắt dán", tức viền sáng chưa thấy ở cỡ dải 480 px.
3. **s22 (c) đúng luật thế giới nhưng người xem đọc là vô lý.** Nguồn sáng (cột điện mé đối diện) nằm ngoài khung, còn đèn khí ngay cạnh thì tắt. Người xem không thấy nguồn, nên đọc là "đèn pha không rõ từ đâu". Cần cho thấy nguồn: một mẩu cột điện hoặc quầng lạnh ở mép khung, hoặc một cú máy thiết lập trước đó.
4. **Banding còn ở s05** dù đã dither, có thể do nén JPEG của dải.
5. **Hạn chế đo:**
   - mỗi dải chỉ một người chấm, nên dao động ±1 điểm là nhiễu thường gặp (Mốc 1: cùng biến thể, điểm 4–5);
   - chênh 4,75 → 4,50 tương đương 1 điểm trên 4 dải, khó phân biệt với nhiễu;
   - dải khung tĩnh chấm "bất động" nặng tay.

**Đề xuất (chờ chủ dự án quyết)**
- **(A) Một lượt sửa ngắn ≈ 30–50 nghìn token:**
  - bỏ "khối thân mờ" và quầng 10 px; bóng phải ĐẶC, chỉ viền sáng mảnh 1–2 px phía đèn;
  - s22 cho thấy nguồn điện lạnh ở mép khung, hợp world-rules v0.6 (cột ở mé đối diện);
  - tăng dither hoặc grain ở quầng s05;
  - tiêu đề "OLD TOWN, 1905" đạt 4,5:1.
  - Kiểm mù lại 4 dải ≈ 180 nghìn token.
- **(B) Chấp nhận B3 v1/v2 làm nền**, để chủ dự án chấm bằng mắt trên khung 1080 (tiêu chí 1 là điểm của chủ dự án), và dồn sửa vào lúc làm tập thử.
- P nghiêng về (A), vì lỗi "bóng ma" là lỗi mới do chính lượt v2 tạo ra và có cách sửa rõ.
