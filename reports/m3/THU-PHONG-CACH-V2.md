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
| Cờ B1: bản Mốc 1 vs sau v2 | s05 f324; lp20 f240 (720p, hai lần: sau sửa v2 đầu và sau sửa nhắm đèn) | **0 px** |
| Cờ B3 v1: bản Mốc 1 vs sau v2 | s22 f1224 | **0 px** |

## 4. Số đo

### 4.1 Giây render mỗi khung (làn nặng, TB · trung vị)
| Shot | v22 | B3 (Mốc 1) | B3 v2 |
|---|---|---|---|
| s03 960×540 | 2,65 · 2,11 | 2,36 · 1,84 | 2,30 · 1,75 |
| s05 960×540 | 1,81 · 1,65 | 1,36 · 1,19 | 1,32 · 1,17 |
| s22 960×540 | 1,57 · 1,43 | 0,96 · 0,85 | 1,31 · 1,19 (thêm bóng của đèn cột điện) |
| lp20 1280×720 | — | 1,54 · 1,42 | xem `../do/b3v2-lp20.timing.json` (lượt đầu 1,64 · 1,50) |

- Khung 1080 đơn lẻ: 8,6–11,5 s, gồm khởi động khung đầu.
- B3 v2 vẫn nhanh hơn v22 ở cả ba shot.

### 4.2 Tương phản chữ
**Đoạn 20 s:** đo trong vùng sáng, chữ = trung vị 3 % điểm tối nhất, nền = trung vị 40 % điểm sáng nhất của ô. Kết quả đầy đủ ở `tuong-phan-clip.txt`.
- Lượt clip đầu: "46" 5,3:1; số trên cột 8,3:1. Tiêu đề tấm ("OLD TOWN, 1905", "14→1") chỉ 2,9:1 vì nằm ở mép vũng sáng.
- Đã nhắm đèn cao hơn rồi render lại; số đo lượt cuối ở bảng dưới.

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
- **Ánh trắng s22:** hệ số 0,22 và phơi sáng × 1,7 chỉnh cho riêng s22. Shot ánh điện khác trong tập cần chỉnh cùng cách (tham số `dbg.hemiK`, `dbg.s22exp`).

## 6. Token
**Cách đo:** bộ đếm `total_tokens left` của công cụ, từ khi nhận lượt v2 đến khi viết xong báo cáo.

| Phần | Token |
|---|---|
| Mã v2 (style_v2, lp20, tấm v2, khung dữ liệu v2) | ≈ 20 nghìn |
| 3 lượt thử + xem ảnh | ≈ 20 nghìn |
| Render, đóng gói, 0 px, đo, sửa nhắm đèn | ≈ 25 nghìn |
| Báo cáo | ≈ 10 nghìn |
| **Tổng lượt v2** | **≈ 75 nghìn** (hạn 120 nghìn) |

**Quy ra phim:** 9 s Last Round + 20 s clip + 1 khung dữ liệu ≈ 0,5 phút, tức ≈ 0,15 triệu token/phút cho một lượt sửa toàn bộ. Nằm trong mức "≤ 0,3 triệu/phút"; không có chỉ số nào nằm trong ±5 % quanh ngưỡng.

## 7. Việc chờ chủ dự án
Đề nghị P đưa vào hàng chờ PLAN.md:
- chấm 4 cặp ảnh 1080 trước/sau;
- duyệt cách sửa s22 (ánh điện đổ bóng từ cột mé đối diện);
- duyệt tấm chữ đơn giản hoá trong đoạn 20 s (3 cột thay 6).

## 8. Kiểm mù
*(Để trống cho P.)*
