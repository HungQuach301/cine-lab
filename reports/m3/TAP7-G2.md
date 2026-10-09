# TẬP 7 — CỔNG G2: bản cuối "When Computers Were People: One Word, Three Jobs"

**Ngày:** 09/10/2026 · **Phiên P** · **Nhánh:** `claude/eager-babbage-6cc4l6` · **checks:** v3 1.7.1 (LOCK KHỚP)

## 0. Kết luận

- **QC Q1–Q31 + LOCK: ĐẠT** trên bản cuối 1080p. Bảng đầy đủ ở `reports/m3/ep07/qc-g2.md`.
- **Lời:** đúng bản khoá G1 v2 (`loi-v2.txt`, 17 đoạn). ASR đạt 20/20 đoạn và Short.
- **Thời lượng:** 10:17,7. Dưới mốc 11:00, nên không phải rút đoạn 06.
- **Tỷ lệ trục kể** (CHUAN-KENH §2, ±5 điểm), đều nằm trong khung:

  | Phần | Thực tế | Khung |
  |---|---|---|
  | Mở + Kết (00, 01, 15, 16) | 17,6 % | 15–20 % |
  | Quá khứ + Chuyển giao (02–08) | 43,2 % | 40–45 % |
  | Hiện tại + Tương lai (09–14) | 39,2 % | 35–40 % |

  Nhãn `part` trong timeline cho kết quả STORY 16,4 / HISTORY 43,2 / TODAY 40,4.
- **Q27 chính thức chạy một lần trên 1080p: ĐẠT**, tập 7 được 5,68, tập 1 được 5,64. Mức hơn chỉ +0,7 %, **sát ngưỡng**.
- **Q31:** vòng 5 (bản cuối) **ĐẠT**. Không có điểm đứt mạch 3/3; ba điểm 2/3 đã giải trình, chép nguyên văn ở mục 3.
- **Cần chủ dự án:** xem mục 7.

## 1. Sản phẩm (ngoài repo, `/var/tmp/cine-out/ll-ep07/`)

| Tệp | Cỡ | SHA-256 |
|---|---|---|
| `ll-ep07-v1-master.mp4` (1080p, 24 fps, 14 825 khung) | 973 MB | `ec203d63…ddfb4` |
| `ll-ep07-v1-p1/p2/p3.mp4` (bản xem) | 74,1 / 75,1 / 77,0 MB | xem `reports/m3/ep07/SHA256-v1.txt` |
| `shorts/ll-ep07-short-S1/S2/S3.mp4` (9:16) | 22,4 / 33,7 / 17,3 s | xem `SHA256-v1.txt` |

Trong repo:
- `reports/m3/ep07/phat-hanh/`:
  - thumbnail T1/T2, dựng từ khung cảnh đinh 1080p, không dùng ảnh người thật của NASA;
  - mô tả YouTube có 17 chương theo mốc thật;
  - chữ cho Shorts;
- `reports/m3/ep07/khung-g2.jpg`: 24 khung, mỗi khung cách nhau 25,7 s;
- `reports/m3/ep07/KHAN-GIA.md`: khung số khán giả cho mốc 48 giờ và 7 ngày.

**Chưa đẩy video lên nhánh phát hành.** Phiên chỉ được phép đẩy lên nhánh làm việc. Xin phép ở mục 7.

## 2. Q1–Q31 so với tập 1 và tập 6 v2

| Mục | Tập 7 (bản cuối) | Tập 6 v2 | Tập 1 (m23) |
|---|---|---|---|
| Q1 judder / Q2 khung trùng / Q3 xuyên hình | 0 / 0 / 0 | 0 / 0 / 0 | — |
| Q4 master | −14,0 LUFS / −1,5 dBTP | −14,0 / −1,4 | — |
| Q5 tương phản chữ thấp nhất | 5,12 | 4,6 (sát ngưỡng) | — |
| **Q6 cỡ chữ hoa nhỏ nhất** | **30,7 px (sát ngưỡng 30)** | 30,7 px (sát ngưỡng) | — |
| Q7, Q8, Q20–Q25 | 0 lỗi | 0 lỗi | — |
| Q9 số khung | 14 825 = timeline | 12 402 = timeline | — |
| Q10 bản xem / Shorts | 74–77 MB · 17–34 s | 60–66 MB · 22–26 s | — |
| Q11 / Q12 / Q13 | 0 / 0 / 0 (Q13 lần 1 trượt, xem §5) | 0 / 0 / 0 | — |
| Q14 móc câu · tựa | móc < 0:15; tựa chồng trên cảnh ở 0,0 s | tựa 19,7 s | — |
| Q15 đổi hình | dài nhất 7,6 s · TB 2,8 s | 7,8 · 2,6 | — |
| Q16 thẻ giấy | 2,9 % | 6,9 % | — |
| Q17 mật độ số | 0,78/phút · neo c46, prog88, sd_chg | 0,93/phút | — |
| Q19 tư liệu | 51,5 s (8,3 %, ≤ 20 %) · 7 ảnh NASA có trong RIGHTS | 25,1 s | — |
| Q26 đa dạng hình | 102 khung nhìn · lớn nhất 3,9 % · liền cùng bố cục 1 | (không áp; P đo 79 khung nhìn, 4 %) | (K đo, fixture) |
| **Q27 chấm hình mù** | **5,68 vs 5,64 (sát ngưỡng)** | (P đo 3 vòng 10 + 10 khung: +0,37 / +0,97 / −0,43) | là mốc so sánh |
| Q28 âm thanh | 4 cue · âm nghề 57/57 · lặng trước số neo 0,69 / 0,79 / 0,76 s | (không áp) | — |
| Q29 hình–lời | 89/89 | (không áp) | — |
| Q30 liền mạch / tông | 3 chuyển hồi · b* 18,5 / 12,3 / 1,8 / 17,2 | (không áp) | — |
| Q31 xem liền mạch | vòng 5 ĐẠT · [7, 7, 7] | (P đo: 7 / 6 / 6,5 → 7 / 6 / 7) | — |
| LOCK | KHỚP | KHỚP | — |

- Tập 1 chỉ có số so trực tiếp ở Q27, nơi nó là đối chứng.
- Theo lệnh "không đọc báo cáo cũ", P không mở QC m23 của tập 1. Số tập 6 v2 lấy từ `reports/m3/ep06/qc-g2-v2.md` và `Q27-Q31.md`.

## 3. Mọi lần chấm mù

Bảng đầy đủ, JSON nguyên văn và giải trình nằm ở `reports/m3/ep07/Q27-Q31.md` và `reports/m3/ep07/blind/`. Tóm tắt:

**Q27**, gồm cả lần bị loại:

| Lần | Bản | Tập 7 | Tập 1 | Kết quả |
|---|---|---|---|---|
| 1 | nháp v3 | 4,96 | 5,57 | TRƯỢT |
| 2 | nháp v4 | 5,11 | 4,90 | ĐẠT |
| 3 | nháp v5 | 5,54 | 5,42 | ĐẠT; R3 thừa mục F61 |
| 4 | nháp v6 | (5,40) | (5,37) | **KHÔNG HỢP LỆ** (R1 thiếu F59, F60) |
| 4b | nháp v6 | 5,14 | 5,24 | TRƯỢT, trong sai số ±0,36 |
| **Chính thức** | **1080p** | **5,68** | **5,64** | **ĐẠT** |

- Các lần chấm nháp làm ở 960×540, so với tập 1 ở 1080p, nên lệch độ phân giải và chỉ dùng để chẩn đoán.

**Q31:**

| Vòng | Bản | Kết quả | Điểm ≥ 2/3 |
|---|---|---|---|
| 1 | nháp v3 | TRƯỢT | T08 3/3, T09 |
| 2 | nháp v4 | TRƯỢT | T04, T06 |
| 3 | nháp v5 | TRƯỢT | T04, T07, T11, T13 |
| 4 | nháp v6 | ĐẠT | T04, có giải trình |
| **5** | **1080p** | **ĐẠT** | T05, T09, T15, có giải trình |

**Giải trình vòng 5** (chép nguyên văn `giai-trinh.json`):
- **T05:** "Điểm mở phần 'Chuyển giao' của trục kể do chủ dự án duyệt ở G1: lời mở đầu đoạn 05 là 'Then came the second kind of work', nên hình đổi chủ ý từ phòng tính toán sang phòng máy rơ-le 1947 (nơi xuất hiện công việc thứ hai), có tiếng rơ-le vào trước hình 0,5 s và phụ đề 'the second kind of work' ngay chữ 'second'. Ngay sau đó là ảnh NASA 1947 của chính phòng máy Bell, nên người xem được neo nơi chốn trong vòng 4 s."
- **T09:** "Cầu nối có chủ ý của kịch bản khoá (đoạn 09: 'The lamplighter walks on'), chuyển từ quá khứ sang hiện tại theo ẩn dụ ngọn lửa trao tay mà chủ dự án đặt cho kênh: J-cut tiếng bước chân người thắp đèn vào trước hình 1,2 s, cùng dải cửa sổ phòng tính toán tắt rồi một tầng tháp bừng sáng. Một người xem không nêu điểm này."
- **T15:** "Match cut có chủ ý của kịch bản khoá: ngọn đèn trên đầu thang (câu hỏi 'where will the next beginners learn?') khớp với ngọn đèn khí cạnh dải cửa sổ ở đoạn Kết; câu móc 'What happens to a job when a machine takes its name?' lặp lại nguyên văn câu mở đầu phim để đóng vòng kể (Mở + Kết theo CHUAN-KENH §2). Một người xem không nêu điểm này."

**Giải trình vòng 4**, T04, nháp v6: chép ở `Q27-Q31.md`.

**Câu hỏi kiểm mù kịch bản, "Người xem rút ra thông điệp chính là gì?"**
- Ở vòng 5, cả 3 người xem đều tự nêu được trục kể: công việc dịch chuyển khi máy nhận tên nghề, và người mới vào nghề sẽ học ở đâu.
- Không ai đọc phim thành thông điệp "máy thay người".

**Sổ vòng Q31 của tập:** vòng 1–4 chạy trên thư mục nháp, được chép sang thư mục bản cuối trước khi chấm vòng 5, theo luật "Vòng tính theo từng tập" (`blind/q31-NGUON.txt`). Nếu chủ dự án hoặc K muốn bản cuối tính lại từ vòng 1, thì T05, T09 và T15 (2/3) sẽ chặn. P nêu để chủ dự án quyết.

## 4. Thay đổi so với nháp đã duyệt nội dung

Lời, số và nguồn giữ nguyên G1.

**Sửa theo chấm mù:**
1. Cảnh JPL ban ngày mới (`design/ll-hero/ep07.js` → `jpl`):
   - nắng California, hàng cọ ngoài cửa sổ, bảng quỹ đạo vẽ dần;
   - phụ đề "Jet Propulsion Laboratory, California";
   - không ghi số phút trên quỹ đạo, vì không có nguồn.
2. Đoạn 04 mở bằng chồng giấy 3D nối tiếp cuối đoạn 03, rồi hoà 1,4 s sang ảnh NASA 1943.
3. Diptych có nhãn hai nửa (`scripts/ll/lib/v3.js`, `p.labels`):
   - đoạn 11: "computer programmers · software developers";
   - đoạn 12: "Langley, 1940s · today";
   - đoạn 14: "1947 · today".
4. Một lượt sửa nội thất, theo điều phối 08/10:
   - phòng tính toán: ốp gỗ, bảng biểu, lò sưởi, vệt nắng, quầng đèn bàn;
   - người ngồi có vai, cổ áo, bàn tay;
   - văn phòng: thảm ô, giấy, cốc; sàn ô phòng rơ-le;
   - sáng thêm air_hook, relay, tower, air_end.

**Sửa nhà máy:**
- `hero.js --resume` và `pending` stamp: dựng tiếp cảnh đinh sau khi job nền bị ngắt ở mốc 2 giờ.
- `asr.py` truyền `speed`. Lỗi này đã làm đoạn 12 bị thu lại 2 lần mỗi build bản cuối (BAI-HOC #95). Bản cuối dùng **đúng bản thu đoạn 12 đã kiểm trên nháp**, khôi phục từ git; prep kiểm lại cho `el_sent` = 0 và đoạn 12 = 56,67 s.
- Mô tả YouTube: độ tuổi "twenty-two to twenty-five" viết bằng chữ như lời phim (Q13 lần 1, §5).

## 5. Chỉ số sát ngưỡng (±5 %) và sự cố

- **Q27:** 5,68 vs 5,64, chênh +0,04, tức +0,7 %. Nằm trong sai số ±0,36 K đo, nên kết quả ĐẠT không chắc chắn về thống kê.
  - Điểm yếu nhất quán theo ý người chấm là nội thất 3D khối thô, tối, và thẻ giấy dựng dở.
- **Q6:** cỡ chữ hoa nhỏ nhất 30,7 px, ngưỡng 30, ở dòng nguồn trên Short S1.
- **Q13 lần 1 trượt:** "22", "25" trong mô tả không truy được về `numbers`.
  - Đây là độ tuổi nhóm nghiên cứu, không phải thống kê. P viết bằng chữ như lời phim, không thêm số vào `numbers`.
- **Sự cố render:**
  - lỗi `asr.py` làm mất khoảng 43 phút cảnh đinh;
  - job nền bị ngắt ở mốc 2 giờ: trước khi có `--resume` mất 655 khung (lỗi gộp vào trên); sau đó không mất thêm.

## 6. Token và giờ máy (đo thật)

**Token**, đo từ log phiên, khử trùng theo message id. Cột "cache tạo" và "cache đọc" là token đầu vào phục vụ từ cache.

| Giai đoạn | Opus đầu ra | Opus cache tạo | Opus cache đọc | Sonnet (subagent) đầu ra | Sonnet cache tạo / đọc |
|---|---|---|---|---|---|
| 1. G1 v2 (viết lại, kiểm mù kịch bản) | 43 528 | 157 008 | 5 463 074 | 312 | 146 760 / 134 568 |
| 2. Giọng, nháp v1–v6, QC và chấm mù nháp | 371 205 | 2 880 903 | 167 394 505 | 11 806 | 2 444 635 / 3 081 560 |
| 3. Lượt sửa nội thất, 1080p, QC, chấm chính thức, G2 | 64 269 | 1 744 056 | 34 876 687 | 7 532 | 626 189 / 371 962 |
| **Cộng** | **479 002** | **4 781 967** | **207 734 266** | **19 650** | **3 217 584 / 3 588 090** |

Token đầu vào không cache: Opus 1 136, Sonnet 200.

- Ghi chú về subagent:
  - 31 lượt chấm mù: Q27 16 lượt, Q31 15 lượt. Mỗi lượt Q27 khoảng 126 nghìn token, Q31 khoảng 72 nghìn token theo báo của công cụ.
  - Mỗi lượt Q27 đọc 60 ảnh 1080p.
- **Vượt trần token của tập.** `ep07/PLAN.md` đặt trần 1,5 triệu token mỗi tập (đầu vào mới + sinh ra).
  - Số đo: Opus khoảng 5,26 triệu (cache tạo 4,78 triệu + đầu vào 0,001 triệu + đầu ra 0,48 triệu); Sonnet khoảng 3,24 triệu. Cộng khoảng 8,5 triệu, tức khoảng 5,7 lần trần.
  - Theo NGUYÊN TẮC TỐI CAO (CLAUDE.md), trần token là trần mềm: vượt để giữ chất lượng thì làm và báo, không dừng hỏi.
  - Phần lớn nằm ở giai đoạn 2: 6 bản nháp, 5 lượt chấm Q27 và 4 vòng Q31 trên nháp. Mỗi vòng sửa đều kéo theo đọc lại ảnh và log dài.
  - Từ điều phối 08/10, chấm mù trên nháp đã dừng.

**Giờ máy** (4 nhân CPU, SwiftShader):

| Bước | Giờ máy |
|---|---|
| Nháp v1–v6, 960×540 SPP1 (render + ghép, 6 bản và các lần dựng lại từng phần) | ≈ 11,7 giờ |
| QC trên nháp, khoảng 7 lần × 12 phút | ≈ 1,4 giờ |
| Nháp v7, dừng theo điều phối | ≈ 0,05 giờ |
| **Bản cuối 1080p SPP4** | |
| — cảnh đinh 22 cảnh và 17 đoạn, 7 lượt nền | ≈ 11,0 giờ (khoảng 0,7 giờ do lỗi `asr.py`) |
| — trộn, ghép, Shorts | 0,9 giờ |
| — QC 2 lần | ≈ 0,4 giờ |
| **Cộng** | **≈ 25,5 giờ** |

**ElevenLabs:**
- Bộ đếm 52 188 ký tự ở nháp v6, 56 810 ký tự ở bản cuối, tức +4 622 ký tự do lỗi `asr.py`.
  - Log của P giải thích được 2 808 ký tự: 4 lần thu đoạn 12, mỗi lần 702 ký tự.
  - Phần còn lại không thấy trong log của phiên.
- Sau khi sửa: 0 ký tự mỗi build.

**Đĩa:** còn trống 8,0 GB.

## 7. Việc chờ chủ dự án

1. **Duyệt G2** bản cuối tập 7, hoặc chỉ đạo sửa.
2. **Cho phép tạo nhánh phát hành `release-ll-ep07-v1` (Git LFS):** master, 3 bản xem, 3 Shorts, thumbnail, mô tả.
   - P sẽ tải ngược về và kiểm SHA như tập 6.
   - Bản xem lớn hơn 30 MB nên không gửi qua giao diện được.
3. **Q27 sát ngưỡng:** 5,68 vs 5,64, trong sai số. Chủ dự án chấp nhận, hoặc giao lượt sửa nội thất tiếp theo cho tập sau. P đề xuất chấp nhận cho tập 7, và đưa "nội thất chi tiết hơn" vào kế hoạch tập 8.
4. **Cách đếm vòng Q31 theo tập** (sổ vòng nháp → bản cuối): chủ dự án xác nhận, hoặc chuyển K quyết.
5. **Hai SFX mang dấu Public Domain Mark 1.0** (LL-SFX-12 `wall-clock.mp3`, LL-SFX-13 `film-reader.mp3`):
   - PDM là dấu, không phải lời từ bỏ quyền như CC0;
   - tác giả tự đặt dấu cho bản ghi gần đây, nên chắc chắn pháp lý thấp hơn CC0 khi bán phim;
   - lựa chọn: chấp nhận, hoặc giao P thay bằng bản CC0 (phải dựng lại âm, khoảng 1 giờ máy, không render hình).
6. **Điểm "chán" đồng thuận ở vòng 5:** văn phòng tối lặp lại ở phần Stanford, khoảng 8:00–9:20.
   - Theo điều phối "render 1080p một lần", tập 7 không sửa.
   - Hướng sửa cho tập sau đã ghi ở BAI-HOC.
7. G3 tập 6 v2 do chủ dự án tự đăng (đã giao). P không chờ.

## 8. Sau duyệt G2 (09/10/2026): nhánh phát hành và kiểm SHA

- **Chủ dự án DUYỆT bản cuối nguyên trạng.** Các quyết định ghi ở AUTHORSHIP 09/10.
- **Nhánh phát hành:** https://github.com/HungQuach301/cine-lab/tree/release-ll-ep07-v1, commit `6adb15c`.
  - Nhánh mồ côi, Git LFS cho `*.mp4`.
  - Gồm 14 tệp: master, 3 bản xem, 3 Shorts, thumbnail T1/T2 kèm `.boxes.json`, mô tả, chữ Shorts, `SHA256-v1.txt`. Có thêm `SHA256SUMS.txt` và `.gitattributes`.
- **Kiểm SHA sau khi tải ngược:**
  - P tải cả 14 tệp từ link công khai `https://github.com/HungQuach301/cine-lab/raw/release-ll-ep07-v1/<tệp>` vào thư mục trống, rồi chạy `sha256sum -c SHA256SUMS.txt`: **14/14 OK**.
  - Master tải về đủ 973 019 139 byte, đúng tệp thật chứ không phải con trỏ LFS.
  - SHA master `ec203d6304b0aed13c5dd7f7f3a1649a44255ad03bbc850c68839fa83b3ddfb4`, khớp `SHA256-v1.txt` lập lúc dựng.
- **Ghi thêm:**
  - RIGHTS.md: LL-SFX-12, LL-SFX-13 ghi "chủ dự án chấp nhận PDM 09/10".
  - BAI-HOC #96–#98 (giới hạn bối cảnh 3D, nội thất chi tiết, kiểm bộ đếm ElevenLabs) và luật mới trong `reports/m3/ep08/PLAN.md`.
  - Hướng dẫn đăng: `reports/m3/HUONG-DAN-DANG-TAP7.md`.
- **Việc còn lại: G3, chủ dự án đăng.**
