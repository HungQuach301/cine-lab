**Nhánh thật: `dong-goi-t3`** (đúng lệnh), tạo từ `origin/main` @ `8cedb8af`. Harness gán nhánh `claude/wonderful-lamport-ydmmb4`; mọi commit cũng đẩy sang nhánh đó, cùng SHA. **Không merge.**

# ĐÓNG-GÓI-T3 — tiêu đề, thumbnail, Short, mô tả cho T3 Gibraltar — BÁO CÁO (DỪNG chờ chủ dự án)

> **Phiên:** ĐÓNG-GÓI-T3, 19/10/2026, UTC ≈ 14:20 → 15:25.
>
> **Đã đọc:** `reports/m3/BAI-HOC-LL.md`; Kinh thánh §2, §5, §10 (gồm §10.6), §11.1, §11.2 (khuôn đóng gói series), §12.1, §13; PACKAGING-BRIEF, titles và kiểm tiêu đề của T1 và T2; `TEARDOWN-FON.md` (theo tham chiếu Kinh thánh); `loi-khoa.txt` và `script-v4.2-KHOA.md` (đọc từ `origin/k2c-t3-kl42`, xem §0); `nguon-mo-ta.md`; `reports/v7p/V7P-BAO-CAO.md` §1–§2 (`origin/v7-pilot`).
>
> **Vùng sửa:**
> - `channel-k2/k2c-t3-01/phat-hanh/**`: chỉ thêm tệp mới. `nguon-mo-ta.md` cũ không sửa.
> - `reports/dong-goi-t3/**`: 13 MB, không LFS.
>
> Không sửa `loi-khoa.txt`, `design/`, `scripts/`, `checks/`, `docs/` hay nhánh khác. Máy dựng V7 chạy trong worktree tạm của `origin/v7-pilot` ở scratchpad. Bản vá tô màu cho hướng C cũng chỉ nằm ở đó, **không commit**.
>
> **Preflight:** đã cài hook pre-commit (`tools/preflight.sh`), và chạy `--range` trước mỗi lần đẩy. Kết quả: ĐẠT, LOCK KHỚP.
> - Không đưa email vào tệp, header, URL hay payload. UA là `CineLab-research (+https://github.com/HungQuach301/cine-lab)`.
> - Khoá do proxy gắn (YouTube) hoặc lấy từ biến môi trường của tiến trình con (Claude). Không in, không ghi khoá.

## §0 Tóm tắt

| Việc | Kết quả |
|---|---|
| **0. Quét ngách** | Quét 6 truy vấn, ra 282 video đăng ≥ 2023. Còn 122 video dài > 180 s; 105 đúng chủ đề; 92 có mốc kênh hợp lệ để tính điểm vượt trội.<br>**Giả thuyết khoảng trống của điều phối: ĐÚNG.** Làn timelapse 3D: 53/54 tiêu đề chỉ hứa "xem nó lớn lên"; **0/54** hứa tranh giành, xung đột hay đổi chủ; 0/54 ảnh có xung đột; 2/54 ảnh có lửa.<br>Đặc trưng duy nhất có KTC 95 % dương rõ là **lửa/khói trên thumbnail**. Cờ nổi bật, bản đồ phẳng và lời hứa "ai sở hữu" trong tiêu đề đi cùng điểm **thấp** (§1). |
| **1. Tiêu đề** | 12 ứng viên, chấm mù 3 người. Đứng đầu là khuôn (c) do việc 0 đề xuất: **"Gibraltar: 14 Sieges in 3D \| Timelapse 1309–2026"** (8,33; cả 3 người chấm xếp số 1). Đề xuất bộ thử: c5 / b3 / a2. "Why Is Gibraltar British?" bị chấm thiên vị 3,33. |
| **2. Thumbnail** | 8 ứng viên (4 hướng × 2), dựng từ máy V7, ở 1280×720, 4K, 360×202 và 168×94. Đã kiểm tương phản và OCR cỡ nhỏ. Chấm mù cỡ nhỏ: **A1 8,67 · A2 8,60 · B1 8,20** (muốn bấm cao nhất) · B2 7,80 · D2 7,20 · D1 6,87 · C2 6,53 · C1 6,20. Đề xuất bộ thử: A2 / B1 / B2. |
| **3. Short** | 2 kịch bản, câu nguyên văn lời khoá v4.2: S1 "Ten floating batteries" 47,8 s; S2 "Walk in across a runway" 44,1 s. Mốc thời gian theo stem KL42. Có khung mẫu dọc. Bản thu G1 **không có trên main**, phải lấy từ `origin/k2c-t3-kl42`; master đã mất (§4). |
| **4. Mô tả v2** | 4 048 ký tự. Gồm: chương (timestamp để trống), khối câu trích và khối số liệu theo TL-4, câu §10.6 đã sửa, "AI use = Yes", C2PA. Bình luận ghim v2: 1 239 ký tự. Thẻ phương pháp: 2 × 8 s × 24 từ. **Sửa một lỗi dữ kiện của bản cũ** (García Sanz, §5). |
| **4b. Xuất cho điều phối** | `thumbnail/xuat-dieu-phoi/T1…T8-{1280x720,168x94,360x202}.png`. Khoá ở `thumbnail/khoa.json`; điều phối **không mở trước khi chấm**. |
| **5. PACKAGING-BRIEF** | `channel-k2/k2c-t3-01/phat-hanh/PACKAGING-BRIEF.md`: bộ thử 3 tiêu đề × 3 thumbnail, điều kiện Test & Compare (đã kiểm trang trợ giúp: điều kiện là "advanced features", **không phải YPP**), và cách thay thế. |
| **Chi phí** | Claude **$0,959** · OpenAI **$0** · YouTube **1 947 đơn vị** (trần 2 000; 1 121 đơn vị mất ở lượt lỗi, §9) · ElevenLabs 0 · giờ máy ≈ 0,7 h. |

**Lời khoá v4.2 không có trên `main`.** `main` có `loi-khoa.txt` `0fdc72ce…` (v4.1). Bản v4.2 `51d1c773…` và `script-v4.2-KHOA.md` chỉ có trên `origin/k2c-t3-kl42`. Phiên này đọc từ nhánh đó; máy kiểm SHA trong `ma/short_kb.py`.

## §1 Quét ngách bằng số (việc 0)

**Cách làm** (`ma/quet.py`, `ma/do_anh.py`, `ma/nhan.py`, `ma/dactrung.py`):
- **6 truy vấn**, ≤ 50 video mỗi truy vấn, lọc ≥ 2023-01-01: "3d time lapse city", "watch city grow timelapse", "history of the city animated", "siege history animated", "contested territory border history", "gibraltar history".
- **Điểm vượt trội** = lượt xem / trung vị lượt xem của 20 video gần nhất trong kênh (danh sách uploads). Chỉ tính kênh có ≥ 5 video gần.
- **Đặc trưng tiêu đề:** đo bằng regex (độ dài, năm, dải năm, mũi tên, 3D, timelapse, grow/evolution) và bằng mô hình (từ mở đầu, vị trí tên nơi, câu hỏi, loại lời hứa, xung đột, tranh chủ, nhãn định dạng, đúng chủ đề).
- **Thumbnail:** tải vào thư mục tạm ngoài git, đo bằng máy (độ sáng L\*, bão hoà, tương phản RMS, độ màu, tỷ lệ ấm/đêm, OCR diện tích/số từ/chiều cao chữ), rồi gắn nhãn bố cục bằng mô hình nhìn (chia đôi, tiêu điểm, đêm, lửa, cờ, dải năm, tên nơi lớn, tỷ lệ trời).
- **Ảnh đối thủ đã xoá.**
- **Repo chỉ lưu** `quet-ngach/dac-trung.json` (video_id + đặc trưng + số, không tiêu đề) và `quet-ngach/thong-ke.json`.

**Cỡ mẫu**

| Tập | Số video |
|---|---|
| Kết quả tìm kiếm | 282 |
| Video dài > 180 s | 122 |
| Đúng chủ đề | 105 |
| Có điểm vượt trội | 92 (làn timelapse 41; làn lịch sử 51) |

Trung vị điểm vượt trội là 3,1. Con số này lệch lên vì kết quả tìm kiếm thiên về video thắng.

**Đặc trưng ↔ điểm vượt trội** (tập 92; trung vị có / không; KTC 95 % bootstrap của chênh TB log10)

| Đặc trưng | n có | Trung vị có / không | KTC chênh log | Đọc |
|---|---|---|---|---|
| Thumbnail có lửa/khói | 9 | **6,45 / 2,52** | **+0,09 … +0,94** | dương, KTC không chứa 0 |
| Thumbnail đêm/tối | 17 | 4,69 / 2,52 | −0,16 … +0,61 | xu hướng dương |
| Thành phố từ trên cao lấp khung | 13 | 4,68 / 2,89 | −0,33 … +0,40 | xu hướng dương |
| Tiêu đề có năm | 23 | 7,90 / 2,14 | −0,15 … +0,59 | xu hướng dương; làn timelapse 8,8 / 1,49 (−0,10 … +0,95) |
| Tiêu đề có từ xung đột | 25 | 3,53 / 2,36 | −0,09 … +0,44 | xu hướng dương |
| Cờ nổi bật | 8 | **1,48 / 3,38** | −0,75 … 0,00; làn lịch sử **−0,96 … −0,22** | âm |
| Tiêu đề hứa "ai sở hữu / tranh chấp" | 8 | **1,03 / 3,38** | **−0,81 … −0,10** | âm (n nhỏ, phần lớn kênh nhỏ) |
| Tiêu đề dạng câu hỏi | 10 | 2,25 / 3,33 | −0,31 … +0,67 | không rõ |
| Chiều cao chữ lớn nhất (liên tục) | 92 | ρ = **−0,26** | −0,45 … −0,07 | chữ khổng lồ đi cùng điểm thấp hơn; làn timelapse ρ −0,36 |
| Bão hoà (làn timelapse) | 41 | ρ = −0,31 | −0,55 … −0,02 | ảnh ít bão hoà hơn tốt hơn |
| Độ dài tiêu đề | làn timelapse 41 / làn lịch sử 51 | ρ +0,37 / −0,27 | +0,09…+0,62 / −0,51…0,00 | ngược chiều giữa hai làn; trung vị 36 / 58 ký tự |
| Kiểu ảnh | — | ảnh chụp 4,91 · 3D 2,90 · tranh AI **1,85** · bản đồ phẳng **1,62** | — | khớp quan sát "tranh AI lượt thấp" của điều phối |

**Khoảng trống** (`thong-ke.json` → `khoang_trong`)
- **Làn timelapse 3D (n = 54):**
  - Lời hứa: hình 53, cả hai 1, chuyện 0.
  - Tranh chủ 0; xung đột trong tiêu đề 0; ảnh xung đột 0; lửa 2; đêm 9.
  - Dải năm trên ảnh 52; tên nơi lớn 51.
- **Làn lịch sử (n = 51):**
  - Lời hứa chuyện 41; tranh chủ 8; xung đột 25.
  - Ảnh 3D chỉ 10; dải năm trên ảnh 4; chia đôi xưa–nay 0.
- **Giao hai làn** (3D + xung đột): 7 video. Đều là **tái hiện một trận đánh** (Agincourt 53,5×, Rochester 29,2×…), **không có timelapse thành phố**. Vậy chỗ "timelapse thành phố + vì sao bị tranh giành" **chưa ai chiếm**.
- **Phần giả thuyết bị số bác:** lời hứa "đổi chủ / vì sao bị tranh giành" dạng **câu hỏi sở hữu** đi cùng điểm thấp (n = 8). Lời hứa xung đột cụ thể ("siege", số vây) thì xu hướng dương. Một video vây hãm Gibraltar mở bằng cặp số đạt **82×**.
- Vì vậy khuôn (c) đề xuất dùng **"14 Sieges"** (sự kiện cụ thể có số), không dùng "Who owns / Why British".
- **Cảnh báo:** tương quan ≠ nhân quả. Mẫu nhỏ (n có = 8–25). Kết quả tìm kiếm thiên về video thắng. Điểm vượt trội thiên lệch theo tuổi video (video mới chưa đủ thời gian). Nhãn mô hình chưa kiểm tay.

## §2 Tiêu đề (việc 1)

**Kiểm cầu** (`cau/cau-thong-ke.json`):
- **"gibraltar", 2 năm, top 50 theo lượt xem:** 134,2 triệu lượt.
  - **Shorts: 31/50 video, 123,5 triệu lượt.** Video dài: 19 video, 10,7 triệu lượt.
  - Short biên giới/đường băng/sân bay: 5 video, 48,4 triệu lượt.
- **Cửa sổ 90 ngày:** 9 video, 11,3 triệu lượt.
- **"gibraltar history" (≥ 2023):**
  - 2 năm: 37 video, tổng 9,7 triệu, trung vị 2 619. Video lớn nhất là một Short dạng câu hỏi sở hữu (6,3 triệu).
  - 90 ngày: 16 video, 382 nghìn lượt.
- **"siege history animated", 2 năm:** 35 video, 79 triệu lượt (25 video về vây hãm, 64 triệu).
- **"contested territory border history", 2 năm:** trung vị 625 lượt, tức cầu dạng tiêu đề "contested" thấp.

**12 ứng viên + chấm mù.** 3 người chấm AI, claude-sonnet-5-5, thứ tự xáo riêng từng người, nhãn trung tính. Vai: (R1) người xem lịch sử/3D ở Mỹ; (R2) người Andalucía có gia đình ở La Línea; (R3) cựu Hải quân Anh.

| Mã | Tiêu đề | Ký tự | Muốn bấm | Rõ | Trung lập | Điềm tĩnh | **TB** | Điểm top 3 |
|---|---|---|---|---|---|---|---|---|
| c5 | Gibraltar: 14 Sieges in 3D \| Timelapse 1309–2026 | 48 | 7,33 | 8,00 | 9,67 | 8,33 | **8,33** | 9 |
| c1 | Gibraltar Under Siege: 1309 → 1783 \| 3D Timelapse | 49 | 6,00 | 7,67 | 9,33 | 8,33 | **7,83** | 2 |
| c0 (đối chứng) | Gibraltar - 3D Timelapse (1704–2026) | 36 | 4,00 | 6,67 | 9,67 | 10,0 | **7,58** | 0 |
| a2 | Why Gibraltar Was Besieged 14 Times | 35 | 6,33 | 6,33 | 9,00 | 8,00 | **7,42** | 0 |
| b3 | Gibraltar \| 700 Years in 3D: 14 Sieges and a Runway | 51 | 6,67 | 6,33 | 9,00 | 7,67 | **7,42** | 3 |
| c3 | Gibraltar: Why Everyone Fought Over It \| 3D Timelapse | 53 | 6,33 | 6,67 | 9,00 | 7,67 | **7,42** | 1 |
| a1 | Why Did Everyone Fight Over Gibraltar? | 38 | 5,67 | 5,33 | 8,67 | 8,00 | **6,92** | 0 |
| b1 | Gibraltar \| 3D Timelapse: Why Everyone Fought Over It | 53 | 6,00 | 5,67 | 9,00 | 7,00 | **6,92** | 1 |
| c4 | Gibraltar, 1704 → 2026: Why Is the Rock Still Contested? | 56 | 6,00 | 6,67 | 6,00 | 7,33 | **6,50** | 2 |
| b2 | Gibraltar \| Watch It Rise, Burn and Rebuild: 14 Sieges | 54 | 6,00 | 5,00 | 8,67 | 5,67 | **6,33** | 0 |
| c2 | Why Is Gibraltar British? \| 3D Timelapse 1704–2026 | 50 | 6,00 | 7,33 | **3,33** | 6,67 | **5,83** | 0 |
| a3 | Why Is the Fight Over Gibraltar Now About Payrolls? | 51 | 3,33 | 3,67 | 5,33 | 6,00 | **4,58** | 0 |

- **Đánh giá dữ kiện:**
  - Mọi số đều lấy từ lời khoá. "14 sieges" là số vây 1309–1783, không phải 14 lần đổi chủ. 1309 → 2026 = 717 năm, làm tròn thành "700 Years".
  - Ví dụ "Gibraltar Under Siege: 1704 → 2026" **bị loại vì sai dữ kiện**: cuộc vây cuối kết thúc năm 1783.
- **Khớp móc:**
  - a3 trùng nguyên văn câu hỏi ‹0h›, nhưng điểm thấp nhất.
  - a1, b1, c3 trùng ‹0e›/‹5j› ("why everyone fought over it").
  - c5, c1, b3, a2 trùng **dữ kiện** ‹0d› (và ‹0g›), không trùng câu hỏi.
  - c2 **không khớp** móc.
- **Chọn 3 cho Test & Compare:** **c5 (CHÍNH) · b3 · a2**, mỗi tiêu đề một khuôn; c1 làm dự phòng. Lý do ở `PACKAGING-BRIEF.md` §1.

## §3 Thumbnail (việc 2)

**Dựng nền:**
- Máy dựng V7 (`tl/t3tl`, hero.js, llvmpipe), worktree tạm `origin/v7-pilot`, bộ đệm `v7p_cache.sh`.
- Mỗi khung là một khung đứng yên: opt lấy từ shot H1/H2/H3 của V7P + thời điểm giữ + máy riêng. Dựng 3840×2160 ở SPP 3, ≈ 25 s/khung.
- **Bản vá tạm duy nhất** (không commit): tuỳ chọn `tint` cho hướng C, gồm một lưới 20 m phủ trên địa hình.
- Ghép chữ bằng `ma/thumb_ghep.py`, font Inter Display (RIGHTS K2-F1).

**Đường dẫn:**
- Thumbnail: `thumbnail/xuat-dieu-phoi/T1…T8-1280x720.png` (1,24–1,51 MB; dưới 2 MB), `-360x202.png`, `-168x94.png`.
- 4K ngoài git: `/var/tmp/cine-out/dong-goi-t3/T*-3840x2160.png` (SHA ở `thumbnail/khoa.json`).
- Ảnh nền sạch: `channel-k2/k2c-t3-01/phat-hanh/nen/nen-1…9.jpg`; máy và thời điểm ở PACKAGING-BRIEF §2.5.

**Kiểm cỡ nhỏ** (`thumbnail/do-chu.json`, `khoa.json` → `ocr_co_nho`, `so-do-anh.json`):
- **Tương phản WCAG** (chữ ↔ nền dưới chữ): "GIBRALTAR" 8,65–18,4; dải năm 8,29–9,84; hộp câu hỏi 13,8. Mọi mục ≥ 4,5.
- **OCR cục bộ ở 168×94:** lượt 1 đọc "2026" thành "2028" ở 2 ảnh. Đã tăng dải năm 5,2 % → 7,3 % chiều cao; lượt 2 đọc đúng cả 6 ảnh có năm.
- Huy hiệu "CONTESTED PLACES" (2,9 %) chỉ đọc được từ 360×202.
- **Lửa đỏ–cam** ở B1/B2: 3,8 % / 3,2 % khung, dưới trần 15 % (§10.6).
- **Bão hoà** B1/B2 là 0,73–0,78 (trời đêm xanh), **cao hơn** trung vị đối thủ 0,51. Đây là chỗ lệch khỏi đặc trưng "ít bão hoà" của việc 0.

**Chấm mù ở cỡ nhỏ.** 3 người chấm như §2; tờ lưới 360×202 và 168×94; nhãn T trung tính.

| T | Hướng | Muốn bấm | Rõ | Trung lập | Điềm tĩnh | Đọc ở 168 | **TB** | Đọc là 3D timelapse | Điểm top 3 |
|---|---|---|---|---|---|---|---|---|---|
| T3 | A1 | 6,67 | 9,00 | 9,67 | 9,67 | 8,33 | **8,67** | 3/3 | 4 |
| T2 | A2 | 7,33 | 9,00 | 9,67 | 9,00 | 8,00 | **8,60** | 3/3 | **8** |
| T5 | B1 | **7,67** | 8,33 | 9,00 | 8,33 | 7,67 | **8,20** | 3/3 | 6 |
| T6 | B2 | 7,33 | 8,00 | 8,67 | 7,33 | 7,67 | **7,80** | 3/3 | 0 |
| T1 | D2 | 5,00 | 4,33 | 9,67 | 9,67 | 7,33 | **7,20** | 3/3 | 0 |
| T8 | D1 | 4,00 | 3,00 | 9,67 | 10,0 | 7,67 | **6,87** | 3/3 | 0 |
| T7 | C2 | 6,00 | 6,00 | 6,00 | 6,67 | 8,00 | **6,53** | 2/3 | 0 |
| T4 | C1 | 6,00 | 6,00 | **4,00** | 7,00 | 8,00 | **6,20** | 3/3 | 0 |

**Đặc trưng áp dụng và chỗ cố ý làm khác:** PACKAGING-BRIEF §2.3.

**Khớp nội dung phim:**
- A, B, D đều có trong kế hoạch V7. D2 dùng năm 1938 thay cho 1782, vì điểm D không quay 1782 (V7P §1).
- B1 ghép hai điểm máy, B cho 1782 và D cho 2026. Lý do: ở điểm B, đèn đêm 2026 quá xa nên không đọc được.
- **C1/C2 hứa một hình không có trong phim** (địa hình tô màu phe) và bị chấm thiên vị → **không đề xuất**.
- Lớp tô ở C để eo đất trung tính, không vẽ ranh (§11.1). Màu vàng TBN trên mái La Línea gần như không thấy.

**Chỗ đã sửa giữa chừng (TT3):**
- A2: chữ "GIBRALTAR" bản đầu đè lên La Línea (đất TBN), nên đã dời sang phần Gibraltar.
- B: chữ che hàng lửa, nên đã hạ chữ.
- C: màu đỏ đậm trông như núi lửa, nên đã giảm độ phủ (0,34 → 0,15) và hạ lớp tô từ 20 m xuống 6 m để bỏ viền đỏ trên đỉnh.

## §4 Short (việc 3) — `phat-hanh/short-kich-ban.md`, `short/short-kich-ban.json`, `short/khung-mau.jpg`
| Short | Khoảnh khắc | Câu / từ | Lời / ước tổng | ≤ 60 s |
|---|---|---|---|---|
| S1 Ten floating batteries | pin nổi cháy 13→14/9/1782 | 11 câu / 97 từ | 41,8 s / 47,8 s | ĐẠT |
| S2 Walk in across a runway | người đi bộ băng qua đường băng | 9 câu / 102 từ | 39,0 s / 44,1 s | ĐẠT |

- **Lời:** máy kiểm mọi câu có nguyên văn trong `loi-khoa.txt` v4.2.
- **Mốc stem:** lấy từ `reports/kl42/nhip-that.json`.
- **Bản thu G1 KL42 không có trên main.** Chỉ có bản MP3 96 kb/s để xem trên `origin/k2c-t3-kl42` (`reports/kl42/nghe/…`). Master WAV/FLAC (SHA `ba50fba7…`) nằm ngoài git và **đã mất theo container**. Khi dựng Short cần thu lại các câu (≈ 1 200 ký tự ElevenLabs) hoặc khôi phục master.
- **Khung mẫu S2:** người đi bộ quá nhỏ ở máy 45 m. Khi dựng cần máy 8–15 m (hạn mức TL-2).
- **Cầu:** Short Gibraltar chiếm 92 % lượt xem top 50, nên đề xuất đăng S2 trước.

## §5 Mô tả v2 (việc 4) — `phat-hanh/nguon-mo-ta-v2.md`, `phat-hanh/the-phuong-phap-v2.json`
- **Mô tả** 4 048 ký tự (< 5 000; không `<` `>`):
  - dòng 1 là móc dữ kiện (có biến thể "Why…" khi chốt a2);
  - "Facts as of" nằm trong 3 dòng đầu;
  - **6 chương, timestamp `‹--:--›` để trống**;
  - **TL-4:** khối "QUOTED IN THE FILM" (5 câu trích nguyên văn + dịch) và "NUMBERS, AND WHO COUNTED" (14 vây, lịch 1704, số đạn, thương vong 1782 hai phía, Montero cả cuộc vây, đường hầm);
  - "What is estimated" thêm trại Faden, ngày sập phố và kiểu đèn đường (phụ thuộc V7);
  - "How AI was used" + C2PA ("may label");
  - câu minh bạch §10.6 **đúng bản đã sửa** ("on two street frames").
- **Bình luận ghim v2:** 1 239 ký tự. **Trả lời 6/6 mới:** 1 425 ký tự, chứa 8 câu trích còn lại. Trả lời 1–5 về nguồn giữ nguyên, vì nguồn không đổi giữa v4.1 và v4.2.
- **Lỗi dữ kiện trong bản cũ đã sửa:** trả lời ghim (1) viết García Sanz "counts differently". Claim S006 (trích nguyên văn: «el undécimo asedio») cho thấy bà **dùng cùng hệ đếm**.
- **Thẻ "How this film was made":** 2 thẻ × 8 s × 24 từ. Thay bản 6 dòng/63 từ/4–5 s cũ (quá nhanh).

## §6 Chỗ hai khuôn Kinh thánh trái nhau (chờ chủ dự án quyết)
1. **Từ mở đầu tiêu đề:** §2 đòi "Why…"; §11.2 đòi tên nơi đứng đầu.
2. **Nội dung tiêu đề:** §2 đòi nghịch lý hoặc cặp đối lập; §11.2 đòi lời hứa định dạng + chủ đề.
3. **Câu hỏi trùng móc:** §3 bắt buộc; §11.2 không nói. Ứng viên trùng nguyên văn câu hỏi ‹0h› bị chấm thấp nhất.
4. **Thumbnail:**
   - §2 brief A: bản đồ nổi + vùng tô bão hoà + hộp 1–2 từ. Brief B: không chữ.
   - §11.2: tên nơi lớn + dải năm + huy hiệu.
   - Brief A gần hướng C (thiên vị, hứa hình không có). Brief B (D1/D2) bị chấm "rõ chủ đề" thấp (3,0–4,3).
5. **Đề xuất Q1:** khuôn lai (c) cho series (PACKAGING-BRIEF §1.3). Cần sửa Kinh thánh §2, §3 và §11.2.

## §7 Chỉ số trong ±5 % quanh ngưỡng (luật cứng)
| Chỉ số | Đo | Ngưỡng | Lệch |
|---|---|---|---|
| YouTube Data API | 1 947 đơn vị | trần 2 000 | −2,65 % (dưới trần) |
| Thẻ phương pháp (mỗi thẻ) | 3,00 từ/s (24 từ / 8 s) | ≤ 3 từ/s | 0 % (chạm trần) |

Ngoài vùng ±5 %:
- Tiêu đề dài nhất 56/60 ký tự (−6,7 %).
- PNG lớn nhất 1,51/2 MB.
- Short dài nhất 47,8/60 s.
- Tương phản chữ thấp nhất 8,29 (ngưỡng 4,5).
- Lửa 3,8 % (trần 15 %).

## §8 Quyết định đề xuất
| # | Đề xuất | Ưu | Nhược | Tác động | Rủi ro |
|---|---|---|---|---|---|
| Q1 | Khuôn tiêu đề series = (c) lai "Nơi: <dữ kiện móc> \| <định dạng> <dải năm>"; "Why…" chuyển xuống dòng 1 mô tả và móc | Điểm chấm cao nhất (8,33); khớp quy ước làn timelapse (tên nơi + dải năm) và mang xung đột của làn lịch sử | Lệch §2 và §3 | Sửa Kinh thánh §2, §3, §11.2; áp từ T3 | Chấm AI ≠ CTR thật. Kiểm bằng lưới của điều phối và Test & Compare |
| Q2 | Bộ thử tiêu đề c5 / b3 / a2 | Mỗi khuôn một đại diện; kết quả trả lời luôn Q1 | b3 và a2 điểm thấp hơn | Cần thử tiêu đề trong Studio | Nếu không thử được tiêu đề thì đổi tay (PACKAGING-BRIEF §3) |
| Q3 | Bộ thử thumbnail A2 / B1 / B2 | Thử đúng giả thuyết "mã thể loại + điểm lệch" ở hai mức | Bỏ brief B của Kinh thánh (D2 làm thay thế) | — | Hai ảnh đêm nổi giữa lưới ban ngày nhưng có thể bị đọc là "trận đánh" chứ không phải timelapse. Lưới thật của điều phối sẽ trả lời |
| Q4 | Loại hướng C (tô màu phe trên địa hình) | Tránh thiên vị (4,0–6,0) và tránh hứa hình phim không có | Mất làn câu hỏi | — | — |
| Q5 | Đăng Short S2 (đường băng) trước S1 | Cầu Short Gibraltar rất lớn (48,4 triệu lượt cho chủ đề đường băng/biên giới) | Phải thu lại lời (master KL42 đã mất) | ≈ 1 200 ký tự ElevenLabs | Giọng thu lại lệch nhẹ so với bản phim nếu seed không tái tạo đúng |
| Q6 | P sửa trả lời ghim (1) (García Sanz) theo v2 | Đúng claim S006 | — | `nguon-mo-ta-v2.md` thay bản cũ ở G2 | — |
| Q7 | Mọi tiêu đề/thumbnail "3D timelapse" chỉ dùng khi duyệt V7 | Không hứa sai định dạng | — | Nếu không duyệt V7, CHÍNH = a2 | — |

## §9 Chi phí thật
| Khoản | Mốc / chặn | Thật | Ghi |
|---|---|---|---|
| Claude API | $5 / $15 | **$0,959** | 10 lệnh claude-sonnet-5-5 (phục vụ đúng model): gắn nhãn ảnh 4 + tiêu đề 1, chấm tiêu đề 3, chấm thumbnail 3 → `cost.jsonl` |
| OpenAI | $3 / $10 | **$0** | Không dùng; người chấm mù chạy bằng Claude như các tập trước |
| YouTube Data API | ≤ 2 000 đơn vị | **1 947** | Lượt 1 (8 truy vấn) tiêu 1 121 đơn vị rồi lỗi `KeyError 'duration'` (video không có thời lượng) **trước khi ghi dữ liệu** → mất. Lượt 2 gọn 6 truy vấn, chỉ tính mốc kênh cho kênh có video dài, thêm bộ đệm phản hồi: 724. Kiểm cầu 101. Thử 1. Lỗi xảy ra 1 lần, không lặp |
| ElevenLabs | 0 | **0** | — |
| Giờ máy | 6 h | **≈ 0,7 h** (ước từ log dựng) | ≈ 40 lần dựng khung (540p + 4K + dọc), mỗi lần ≈ 15–28 s/khung + dựng cảnh; bộ đệm V7 ≈ 2 phút |

## §10 Việc chờ chủ dự án
1. **Chọn 3 tiêu đề** cho Test & Compare. Đề xuất: c5 / b3 / a2 (§2).
2. **Chọn 3 thumbnail.** Đề xuất: A2 (T2) / B1 (T5) / B2 (T6). Nên chọn sau khi điều phối chấm T1…T8 trên lưới tìm kiếm thật. Khoá ở `thumbnail/khoa.json`; không mở trước khi chấm.
3. **Quyết Q1:** sửa Kinh thánh §2, §3, §11.2 cho khuôn series.
4. **Duyệt V7.** Tiêu đề/thumbnail "3D timelapse" phụ thuộc vào V7.
5. **Duyệt mô tả v2, bình luận ghim v2, trả lời (1) đã sửa và thẻ phương pháp v2.** Timestamp chương điền sau khi dựng.
6. **Quyết nguồn âm thanh cho Short:** thu lại các câu, hoặc khôi phục master KL42.
7. **Ghi AUTHORSHIP (phiên P):** lựa chọn tiêu đề và thumbnail của chủ dự án.
8. **Ghi RIGHTS (phiên P):** ảnh nền và thumbnail tự dựng (máy V7, font K2-F1).
9. Phiên P merge nhánh này khi duyệt.

**DỪNG — chờ chủ dự án.**
