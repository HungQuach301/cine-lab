# M2.0 — Chuẩn bị tập thử: phần xưởng (a, c, d) · 01/10/2026

**Phiên:** xưởng (gói THỬ PHONG CÁCH), P giao theo chỉ thị chủ dự án mở Mốc 2 (AUTHORSHIP 01/10/2026). P sẽ gộp với (b) giọng mẫu và (e) bảng shot.
**Nhánh:** `thu-phong-cach` (push sau mỗi bước, KHÔNG merge).
**Căn cứ:** `THU-PHONG-CACH-V2.md` §8 trên nhánh P (kiểm mù B3 v2 được 4,50; lời chê lặp "bóng ma, nửa trong suốt" ở s03/s05, s22 bị đọc "đèn pha không rõ từ đâu", còn banding), và `KE-HOACH-TAP-THU.md` §1, §2, §3.2.
**Thư mục sản phẩm:** `reports/m3/thu-phong-cach/M2-0/` và `reports/m3/thu-phong-cach/bo-mau-du-lieu/`.

## (a) Sửa nhỏ B3 → cờ mới `dbg.style = 'b3v3'`
Mã ở `style_v2.js`: chuỗi shader v3 sinh bằng cách thay đoạn trên chuỗi v2, nên chuỗi v2 giữ nguyên byte. `style.js` chỉ thêm `'b3v3'` vào dòng điều phối. `lamp_shot.js` có nhánh `V3`.

| Lỗi kiểm mù | Sửa (chỉ khi cờ b3v3) |
|---|---|
| "Bóng ma, nửa trong suốt" (s03, s05) | Bóng **ĐẶC** bằng mực phẳng; bỏ khối thân mờ. Chỉ còn **một viền mảnh ≈ 1,6 px (ở 960×540) về phía nguồn sáng**; hướng nguồn lấy từ gradient ánh nhoè rộng, độ mạnh theo ánh tại mép. |
| Quầng ≈ 10 px quanh bóng | Nhoè rộng (ước lượng chiếu sáng) **có mặt nạ**: chuẩn hoá theo trọng số, loại điểm ảnh nhân vật, nên bóng tối không còn kéo nền xung quanh. |
| s22 "đèn pha không rõ từ đâu" | Máy mới (28 mm, đặt ở (12; 1,4; −1), nhìn dọc phố): **cột điện mé đối diện (x = 29) và quầng loá của nó nằm ở rìa phải khung**, đúng world-rules v0.6. Ánh điện có hướng, giảm theo khoảng cách. **Bóng người thắp đèn + thang đổ lên tường** từ chính cột đó. Không thêm đèn khí. |
| Banding | Mép bậc mềm hơn (±0,24 → ±0,32), dither tĩnh 0,28 → 0,40 bậc, cộng **hạt tĩnh nhân ±3,5 %** (vân giấy) trước grain chung. Hạt cố định theo điểm ảnh nên không nhấp nháy. |
| Tiêu đề "OLD TOWN, 1905" trong clip dưới 4,5:1 | Tấm v3: tiêu đề bản đồ 100 px, tiêu đề biểu đồ 66 px (để không đè "14→1"); đèn rọi × 1,35. |
| Phát hiện thêm: gốc neo vân giấy phụ thuộc thứ tự render | Ở v1/v2, gốc neo vân giấy là máy ở khung render ĐẦU TIÊN, nên render một khung lẻ khác render nối tiếp khi máy chuyển động (lp20). v3 neo theo **khung đầu shot, tính tường minh lúc dựng**. Đã kiểm: một khung lẻ v3 trùng 0 px với bản nối tiếp. |

**Sản phẩm (a)** trong `M2-0/`:
- Khung 1080 trước (B3 v2) / sau (B3 v3), mỗi cặp 3840×1080: `truoc-sau-1080-s03.jpg`, `-s05.jpg`, `-s22.jpg`, `-lp20.jpg`. Ảnh riêng: `khung1080-*-b3v3.png`, `khung1080-lp20-b3v2.png`.
- Clip 20 s mới: `doan20s-b3v3.mp4` (1280×720, 24 fps, crf 18).
- Dải `kiem_mu.py dai` (cùng mốc như Mốc 1; chỉ để chủ dự án xem, KHÔNG kiểm mù): `dai-s03-b3v3.jpg`, `dai-s05-b3v3.jpg`, `dai-s22-b3v3.jpg`.
- mp4 trọn shot 960×540: `s03-b3v3.mp4`, `s05-b3v3.mp4`, `s22-b3v3.mp4`.

**Tương phản tiêu đề trong clip 720p** (`M2-0/tuong-phan-clip.txt`; chữ = trung vị 3 % điểm tối nhất, nền = trung vị 40 % điểm sáng nhất của ô):

| Mốc · chữ | B3 v2 | **B3 v3** |
|---|---|---|
| 8,0 s · "OLD TOWN, 1905" | 3,8:1 | **4,7:1** |
| 10,0 s · "OLD TOWN, 1905" | 4,1:1 | **5,1:1** |
| 12,0 s · "OLD TOWN, 1905" | 4,2:1 | **5,8:1** |
| 10,0 s · "46" | 5,1:1 | 6,3:1 |
| 15,0 s · "14→1" / "LAMPLIGHTERS" / số trên cột | 5,4 / 7,0 / 8,3:1 | 6,6 / 8,5 / 8,9:1 |

- **ĐẠT ≥ 4,5:1 ở mọi mốc.**
- Lưu ý ngưỡng: 4,7:1 ở 8,0 s chỉ cao hơn ngưỡng 4,4 %, tức nằm trong ±5 % quanh ngưỡng. Mốc 8,0 s là lúc vũng sáng vừa tới tấm bản đồ.

**Banding đo trên chính dải JPEG** (`M2-0/phan-dai.txt`, công cụ `phan_dai.py`):
- Cách đo: trong vùng mịn, đo độ dài trung bình đoạn luma 8 bit phẳng và tỉ lệ điểm ảnh nằm trong đoạn ≥ 24 px.
- Kết quả v2 → v3:
  - s03: 1,24 → 1,20 px;
  - s05: 1,41 → 1,33 px;
  - s22: 1,22 → 1,20 px;
  - đoạn ≥ 24 px là 0 % ở cả hai bản.
- **Giới hạn của phép đo:** nó chỉ bắt dải PHẲNG 8 bit, nên đã sạch ngay từ v2. Mép của các bậc sáng (bậc thang có chủ ý của phong cách) không được đo bằng số. Phần đó cần mắt chủ dự án trên dải `dai-*-b3v3.jpg`.

### Kiểm 0 px (`M2-0/kiem-0px.txt`)
| Phép so | Khung | Kết quả |
|---|---|---|
| Tắt cờ: page.js gốc ebdacde vs nhánh (sau b3v3) | s03 f222, s05 f324, s22 f1224 | **0 px** |
| Cờ B1: bản Mốc 1 vs sau b3v3 | s05 f324 | **0 px** |
| Cờ b3v2: bản B3v2 đã giao vs sau b3v3 | s22 f1224 | **0 px** |
| Cờ b3v2, lp20 f240 | render 1 khung lẻ | lệch 459 692 px (tối đa 8 mã), do gốc neo vân giấy v2 (xem dòng cuối bảng sửa ở trên) |
| | render **nối tiếp 0→240**, đúng cách bản giao | **0 px**, tức không rò cờ |
| Tất định b3v3: 1 khung lẻ vs bản nối tiếp đã giao | lp20 f240, s05 f324 | **0 px** |

## (c) Bộ mẫu dữ liệu B3: 5 khung 1920×1080 (`bo-mau-du-lieu/`)
Mã: `design/m3/thu-phong-cach/bo_mau.py`. Cùng ngôn ngữ hình B3: nền đêm #141B2D có vân giấy (dither tự nhiên, không dải chuyển màu mịn), tờ giấy ngà mép xé + bóng đổ giấy, hổ phách cho gas, trắng lạnh cho điện. Bảng màu, lề 96/54 px và cỡ chữ ≥ 30 px theo KE-HOACH §2.

| Tệp | Mẫu | Nội dung (số thật, nguồn ngắn trên hình) |
|---|---|---|
| `mau-d-map.png` | D-MAP | London: **40,000+ gas lamps by the 1820s**, some 215 miles; Pall Mall · 1807. "Source: English Heritage". Bản đồ không đúng tỉ lệ nên gắn "Illustrative · Not to scale" |
| `mau-d-bar.png` | D-BAR | Cột là cột đèn cắt giấy, cùng thang từ 0: 40,000+ (1820s) · ~1,500 (2015) · ~1,100 (2023); **5 lamplighters** (British Gas 2023). "Sources: English Heritage; NPR (2015); British Gas (2023)" |
| `mau-d-tl.png` | D-TL | 1807 Pall Mall · 1812 royal charter · 1820s 40,000+ · 1878 đèn hồ quang Paris · 1907 New York strike · 2023 five lamplighters; ghi nhãn trực tiếp "amber = gas · cold white = electric" |
| `mau-d-num.png` | D-NUM (số neo) | **1 in 270**: occupations in the 1950 U.S. Census later eliminated by automation, elevator operator; lưới 270 ô (1 ô rỗng). "Source: J. Bessen (2016), NBER · 271 occupations listed" |
| `mau-d-col.png` | Tấm chữ 3 cột | THEN 40,000+ · TODAY 5 (~1,100 lamps, 2023) · NEXT **−34%** word processors and typists, U.S. projection 2025–35 (dấu trừ U+2212). Nguồn từng cột + dòng nguồn chung |

- **Tương phản** (`bo-mau-du-lieu/tuong-phan.txt`, `tuong-phan.json`; đo trên ảnh cuối, từng chữ một):

| Khung | Số chữ | Tương phản nhỏ nhất |
|---|---|---|
| d-map | 8 | 5,33:1 ("Pall Mall · 1807" hổ phách đậm trên giấy) |
| d-bar | 12 | 8,01:1 |
| d-tl | 21 | 8,2:1 |
| d-num | 6 | 8,2:1 |
| d-col | 18 | 5,28:1 ("40,000+" hổ phách đậm trên giấy) |

  - Mọi chữ ≥ 4,5:1. Hai trường hợp 5,28–5,33:1 đúng bằng mức thiết kế của màu #8A4F0E trên giấy (5,3:1), dưới mục tiêu 7:1 nhưng trên sàn.
  - Cỡ chữ nhỏ nhất 30 px.
- **Font:** DejaVu Sans (C4-F1), **DejaVu Sans Bold** và **DejaVu Serif Bold**, nay ghi vào RIGHTS.md (M2-F-DejaVuSans-Bold, M2-F-DejaVuSerif-Bold, kèm SHA-256). DejaVu Serif thường không dùng nên không thêm.
- **RIGHTS:** M3-TPC-3 cho 5 khung mẫu và tấm `panel_*_v3.png`.
- **Chưa làm:**
  - chuyển động của mẫu;
  - mẫu D-GRID và D-SRC riêng (lưới 270 đã lồng trong D-NUM);
  - xuất matte `elements.json` (P0, P1, G4) tự động từ mẫu. Hàm `Frame.text` đã ghi hộp bao từng chữ, là đầu vào sẵn cho matte.

## (d) Đo render thật 1 shot trọn ở 1080p
- **s05, cờ b3v3, 1920×1080, 96 khung, làn nặng** (`do/b3v3-s05-1080.timing.json`): **TB 2,64 s/khung, trung vị 2,46, bỏ khung đầu 2,57.**
- Cùng shot ở 960×540: TB 1,33. **Hệ số 1080/540 đo được = 1,98** (ước cũ 2,5–4).
- 960×540 các shot b3v3: s03 2,39 · s05 1,33 · s22 1,23 · lp20 (720p) 1,64.
- 2D numpy (đo 3 mẫu, mỗi khung sinh lại toàn bộ vân giấy): 0,98–1,58 s/khung. Nếu dựng nền một lần rồi dùng lại thì ước ≈ 0,3–0,5 s.

**Giờ máy tập 9:31** theo 78 shot (KE-HOACH §1, §3.2): 3D B3 6 528 khung (272 s); 2D 7 176 khung (299 s).

| Việc | Cách tính | Giờ máy |
|---|---|---|
| Render 1080p 3D | 6 528 × (2,46–4,8 s; trung tâm 3,3 = TB 960 của 3 shot × 1,98) | **4,5–8,7 (≈ 6,0)** |
| Đồ hoạ 2D 1080p | 7 176 × 0,4–1,6 s | **0,8–3,2 (≈ 1,5)** |
| Thử 960×540 cho animatic (một lượt 3D) | 6 528 × 1,6 s | ≈ 2,9 |
| Render lại cho sửa (≈ 30 % shot) | 30 % của 3D + 2D | 1,6–3,6 |
| Shorts 3D máy dọc (≈ 29 s) | 696 × 3,3 s | ≈ 0,6 |
| Mặt nạ C3, bóng nhân vật, kiểm toán | như KE-HOACH | 1–2 |
| Luật máy × 2 lượt master | như KE-HOACH | 2–3 |
| **Tổng** | | **≈ 13–24 giờ, trung tâm ≈ 17 giờ** trên một làn nặng |

- So với KE-HOACH (14–34 giờ, trung tâm 20 giờ): biên trên giảm khoảng 10 giờ, nhờ hệ số 1080p đo thật (1,98) thay cho ước (2,5–4).
- Phần 3D vẫn là ngoại suy từ một shot 1080p (s05). s03 có bộ cảnh lớn nên chậm nhất ở 960; nên đo thêm một shot loại s03 nếu cần biên chặt hơn.
- Chưa có chỉ số giờ máy nào nằm trong ±5 % quanh một ngưỡng.

## Tệp mã đổi / thêm
| Tệp | Thay đổi |
|---|---|
| `design/m3/thu-phong-cach/style_v2.js` | nhánh `V3`: thay đoạn shader (bóng đặc + viền một phía, nhoè rộng có mặt nạ, hạt tĩnh), máy s22, mặt nạ nhoè (`downM`/`downA`), gốc neo giấy theo khung đầu shot |
| `design/m3/thu-phong-cach/style.js` | `'b3v3'` vào dòng điều phối |
| `design/m3/thu-phong-cach/lamp_shot.js` | `V3`: tấm `_v3`, rọi × 1,35 (nhánh V2/B1 giữ nguyên) |
| `design/m3/thu-phong-cach/data_frame.py` | `panels_v3`; tham số cỡ tiêu đề (mặc định giữ v2, tấm v2 tái tạo trùng byte) |
| `design/m3/thu-phong-cach/bo_mau.py` | MỚI: 5 mẫu dữ liệu + đo tương phản từng chữ |
| `design/m3/thu-phong-cach/phan_dai.py` | MỚI: đo banding trên dải JPEG |
| `design/m3/thu-phong-cach/tuong_phan_clip.py` | thêm mốc 8 / 12 s và chữ "LAMPLIGHTERS" |
| `RIGHTS.md` | M2-F-DejaVuSans-Bold, M2-F-DejaVuSerif-Bold, M3-TPC-3 |

Không sửa `checks/`, `bible/`, tài sản khoá; không đổi lưới, rig, diễn hoạt; page.js không đổi trong lượt này.

## Token (phần xưởng M2.0)
**Cách đo:** bộ đếm `total_tokens left` của công cụ, từ khi nhận việc M2.0 đến khi viết xong báo cáo.

| Phần | Token |
|---|---|
| (a) mã, 1 lượt thử, render, đóng gói, 0 px, sửa tất định | ≈ 40 nghìn |
| (c) bộ mẫu, 1 lượt sửa bố cục, RIGHTS | ≈ 18 nghìn |
| (d) đo và tính giờ máy | ≈ 4 nghìn |
| Báo cáo | ≈ 8 nghìn |
| **Tổng** | **≈ 70 nghìn** (hạn 90 nghìn) |

## Việc chờ chủ dự án (đề nghị P đưa vào hàng chờ PLAN.md)
- Xem 4 cặp ảnh 1080 trước/sau và 3 dải b3v3.
- Duyệt máy s22 mới (thấy cột điện ở rìa phải khung).
- Duyệt 5 khung mẫu dữ liệu và 2 mặt chữ DejaVu bổ sung.
- Quyết có cần đo thêm một shot 1080p loại s03 hay không.

## Kiểm mù
*(Không chạy, theo chỉ thị: chủ dự án gộp sửa B3 vào M2.0, không kiểm mù riêng.)*

---

## Phần P (01/10/2026)

### (b) Giọng kể: 3 mẫu → chủ dự án chọn **Bill**
- Đoạn đọc: mở đầu đoạn 02 kịch bản V2, 375 ký tự, 70 từ (`reports/m3/m2-0/giong-mau/doan-doc.txt`). Mô hình `eleven_multilingual_v2`; stability 0,5, similarity 0,75. Giọng premade của thư viện ElevenLabs, không nhái người thật. RIGHTS M3-N1..N3.

| Giọng | voice_id | Thời lượng | Từ/phút | Ước cả tập (lời dẫn 1 309 từ + ≈ 47 s) |
|---|---|---|---|---|
| George (Anh, nam, kể chuyện) | JBFqnCBsd6RMkjVDRZzb | 25,68 s | 163,6 | ≈ 8:47 |
| Alice (Anh, nữ, giảng giải) | Xb7hH8MSUJpSbSDYk0k2 | 27,53 s | 152,5 | ≈ 9:22 |
| **Bill (Mỹ, nam, điềm đạm) — CHỌN** | pqHfZKP75CvOlQylNhV4 | 29,75 s | **141,2** | **≈ 10:03–10:05** (vượt trần 10:00 ≈ 0,5–0,8 %, trong ±5 %) |

- **Bộ đếm ký tự** (tài khoản dùng chung):
  - trước 3 mẫu: 76 383;
  - ngay sau: 76 683 (tăng **300**, trong khi đã gửi ≈ 1 125 ký tự);
  - lúc kiểm lại: **80 471 / 105 779 → còn 25 308**;
  - kỳ làm mới 23/10/2026.
  - Phần tăng thêm 3 788 xảy ra khi phiên P không gọi API. Khoá của proxy thiếu quyền `speech_history_read` nên không đọc được lịch sử để quy nguồn. Tài khoản có giọng của dự án khác ("AI-Era Money Defense Narrator", "crux-analyst").
  - **Quy tắc từ nay:** ghi số dư trước và sau mỗi lượt; không đọc trọn lời dẫn cho tới khi animatic nhịp (nháp flite) được duyệt.
- **M2.1:** thử tốc độ ElevenLabs 1,05 trên một đoạn; nếu vẫn > 10:00 hoặc mất tự nhiên thì cắt đoạn 07 (−27 s → ≈ 9:36–9:38).

### (e) Bảng shot chốt cho M2.1
`reports/m3/BANG-SHOT-M2.md`:
- 78 shot, 571 s; dùng lại 38 %;
- đoạn 07 (07-01..03, 278–305 s) đánh dấu [CẮT-07]; khi cắt còn 75 shot, 9:04 (tính theo 150 từ/phút);
- có khối JSON máy đọc (P kiểm: 78 dòng, kết thúc 571 s).
- Lưu ý: bảng tính theo 150 từ/phút; với Bill (141,2) các khung thời gian sẽ giãn ≈ 6 %, cần đo lại trong M2.1 bằng nháp flite.

### Yêu cầu gửi K (soạn sẵn, chưa gửi)
`reports/m3/YEU-CAU-K-NHAP.md`: C3 cho nhân vật dạng bóng; profile luật Shorts 9:16.

### P xem khung 1080 (rà độc lập)
- **s22 (b3v3): đạt.** Thấy cột điện mé đối diện và quầng sáng ở rìa phải khung; ánh có hướng; bóng người thắp đèn đặc, đổ lên tường cùng thang. Máy mới rộng hơn, thấy cả phố.
- **s03, s05 (b3v3):** hết "nửa trong suốt". Nhưng ở s05, **bóng người thắp đèn nay quá tối, gần như chìm vào mảng tường tối**; viền sáng 1,6 px khó thấy ở 1080. Rủi ro đổi chiều từ "bóng ma" sang "không thấy người". Đề xuất: nâng viền sáng lên ≈ 2,5–3 px phía đèn, hoặc tách nền sau lưng bóng sáng hơn một bậc. Chủ dự án xem `M2-0/truoc-sau-1080-s05.jpg`.
- Mốc 8 s của tiêu đề "OLD TOWN, 1905": 4,7:1, cao hơn ngưỡng 4,4 % (trong ±5 %).

### Token M2.0 (bộ đếm harness)
| Phần | Token |
|---|---|
| Xưởng (a, c, d) | ≈ 75 nghìn |
| Bảng shot (e) | ≈ 22 nghìn |
| P: giọng mẫu, nháp K, tổng hợp | (không đo chính xác; nhỏ) |
| **Tổng xưởng + bảng shot** | **≈ 97 nghìn** (hạn M2.0 150 nghìn) |

### Việc đang chờ chủ dự án (DỪNG sau M2.0)
1. Duyệt các khung sửa B3 (`reports/m3/thu-phong-cach/M2-0/truoc-sau-1080-*.jpg`, dải `dai-*-b3v3.jpg`, clip `doan20s-b3v3.mp4`). Lưu ý độ chìm của bóng ở s05.
2. Duyệt bộ mẫu dữ liệu: 5 khung `reports/m3/thu-phong-cach/bo-mau-du-lieu/`, và hai mặt chữ DejaVu Bold bổ sung (RIGHTS).
3. Quyết có đo thêm 1 shot loại s03 ở 1080p để chặt biên giờ máy (hiện ≈ 13–24 h, trung tâm ≈ 17 h cho tập 9:31) hay không.
4. Sau khi duyệt → mở **M2.1** (animatic nhịp: nháp flite, thử Bill 1,05, quyết đoạn 07).
