# TẬP 2 — CỔNG G2: bản cuối · 05/10/2026

**P DỪNG ở G2, chờ chủ dự án duyệt bản cuối, Shorts và thumbnail.** Tiêu đề do chủ dự án đặt ở G1, không đổi.
- Dựng toàn bộ bằng nhà máy Mốc B: một đặc tả `reports/m3/ep02/episode.yaml` (v2), một lệnh `scripts/ll/build.sh`, kiểm bằng `scripts/ll/qc.sh`.
- Mọi số dưới đây là **số đo thật trên tệp**.

## 1. Bàn giao
| Tệp | Thông số | Dung lượng | SHA-256 |
|---|---|---|---|
| Master (Git LFS, nhánh **`release-ll-ep02-v1`**): `ll-ep02-v1-master-1080p.mp4` | 1920×1080, 24 fps, H.264 crf 16, AAC 256 kb/s, **9:01,38** (12 993 khung) | 493,9 MB | `8b3c0be618dd291eb2692472efea9df8109f9cba66353034e55cc4b1b94383c9` |
| `screening/ll-ep02-v1-p1.mp4` | đoạn 00–05 (0:00–3:11,58), 720p | 70,4 MB | 5e5c5ac3…194bf350 |
| `screening/ll-ep02-v1-p2.mp4` | đoạn 06–10b (3:11,58–6:13,33) | 66,7 MB | 27fcd5e8…65fa4fa7 |
| `screening/ll-ep02-v1-p3.mp4` | đoạn 10c–13 (6:13,33–9:01,38) | 61,4 MB | 78d0a2a6…29cfd50f0 |
| Shorts S1/S2/S3 (LFS, cùng nhánh) | 1080×1920; 40,33 / 30,67 / 27,92 s | — | trong `SHA256SUMS.txt` |
| Thumbnail T1, T2 · mô tả YouTube (16 chương) · text Shorts · phụ đề `.srt` (195 khối, không dòng > 42 ký tự) | cùng nhánh và `reports/m3/ep02/phat-hanh/` | | |

- **Kiểm sau khi đẩy:** tải ngược S3 từ link LFS công khai, SHA khớp (`11d8b328…`); master trả `Content-Length` 493 902 380 byte, khớp tệp gốc.
- Ảnh khung tổng quan (32 shot): `reports/m3/ep02/khung-g2.jpg`.

## 2. Kết quả `qc.sh` (bảng đầy đủ: `/var/tmp/cine-out/ll-ep02/qc.md`)
| Mục | Kết quả | Giá trị |
|---|---|---|
| Q1 judder | ĐẠT | 0 trên 19 tệp (16 đoạn + 3 Short) |
| Q2 khung gần trùng | ĐẠT | 0 |
| Q3 máy xuyên hình học | ĐẠT | 0 |
| Q4 loudness / true peak | ĐẠT | master **−14,0 LUFS / −1,6 dBTP** (LRA 3,8); phần −14,2 / −14,0 / −13,9 (TP ≤ −1,4); Shorts −14,0 / −1,6 |
| Q5 tương phản thấp nhất | ĐẠT | 4,83:1 ("(2025–35)" ở dòng nguồn đoạn 11) |
| Q6 cỡ chữ hoa tối thiểu | ĐẠT | 19 px (16:9) · 30,7 px (Shorts) |
| Q7 nhãn ACTUAL/PROJECTION | ĐẠT | 0 thiếu |
| Q8 nguồn | ĐẠT | toàn văn, không Wikipedia, số trên hình có trong lời |
| Q9 số khung | ĐẠT | master 12 993 / 12 993 |
| Q10 kích thước | ĐẠT | 70,4 / 66,7 / 61,4 MB; Shorts < 60 s |
| Q11 khung trống (bản dài) / chữ đứng (Shorts) | **TRƯỢT 1** | bản dài 0. Short S1: một quãng **3,04 s** ở câu cuối trước thẻ kết, vượt ngưỡng 3 s đúng 1 khung. **Không sửa** theo nguyên tắc tốc độ (CHUAN-KENH §8) |

**Chỉ số trong ±5 % quanh ngưỡng:**
- chữ hoa Short 30,7 px (cách ngưỡng 30 px 2,3 %);
- S1 chữ đứng 3,04 s (1,4 %).

Bốn lỗi qc bắt được trong lúc sản xuất, đều đã sửa trước khi giao:
1. **Nhãn sai loại số:** Short S2 gắn ACTUAL cho −5,3 % (dự báo). Mẫu `bignum` nay lấy loại số từ số khai báo.
2. **Biểu đồ trống > 3 s:** 43 quãng ở lượt đầu, 8 ở lượt hai, 0 ở lượt cuối. Sửa bằng dòng phụ đề đổi theo lời (`beats`), mỗi cụm neo vào đúng từ trong lời.
3. **Nhãn "0", PROJECTION < 4,5:1** ở góc tối: thêm nền giấy, chữ đậm hơn, góc tối của ánh rọi giảm khoảng 17 %.
4. **Một lần render hỏng** (lỗi cú pháp JS) nhưng `build.sh` vẫn ghép tiếp trên trung gian cũ. Nay `build.sh` dừng khi có đoạn render lỗi.

**Đổi luật qc trong mốc (gửi K, `checks-appeal.md` mục 8b):**
- Q11 bản dài đo đúng luật kênh "khung đồ hoạ **đứng trống**" (chưa có dữ liệu, chỉ tựa/trục/nguồn), theo lỗi L1 tập 1.
- Bản đo cũ "không có nội dung mới" chặt hơn luật và báo cả lúc biểu đồ đã đủ số. Nay chỉ còn áp cho Shorts, theo yêu cầu Mốc B.

## 3. Nội dung và tỷ lệ
- **Thời lượng 9:01** (đích ≈ 8 phút; chuẩn 8–11). Lời Bill đọc chậm hơn ước (G1 ước 7:35 với 2,55 từ/s).
- **Tỷ lệ STORY / HISTORY / TODAY = 18,8 / 31,5 / 49,6 %.** TODAY lệch +4,6 điểm, sát giới hạn ±5. Để cân tỷ lệ, cảnh truyện mở/kết dài thêm 16 s (người thắp đèn đi và thắp đèn, có chuyển động thật). Đây không phải khung đồ hoạ độn.
- **Vòng tra nguồn bổ sung** (`reports/m3/ep02/NGUON-TAP2.md` §6): ≈ 20 nghìn token / trần 80. Hai đoạn TODAY mới:
  - **10b "AI at the help desk"** (Brynjolfsson, Li & Raymond, NBER w31161): +14 % số vấn đề giải quyết mỗi giờ; +34 % với người mới và ít kỹ năng; người giàu kinh nghiệm thay đổi tối thiểu; trích câu tác giả nói nghiên cứu không đo được việc làm chung. Nhân viên phần lớn ở **Philippines** → khung riêng, không ghép với số BLS (luật so sánh, điểm 3).
  - **10c "An early signal"** (Canaries, bản 8/2026): −19 % việc làm tuổi 22–25 ở nghề phơi nhiễm AI cao; chủ yếu qua tuyển ít đi; không có dấu hiệu mất việc diện rộng; CSR thứ 2 về số việc làm trong nhóm phơi nhiễm cao nhất (Table A.6); "early, descriptive — not proof of cause".
  - Đoạn 12 nối hai thời: thời tổng đài, người đang làm gánh chi phí; nay tín hiệu sớm cho thấy người mới vào nghề, dù AI giúp họ nhiều nhất trong công việc. Có câu "too soon to know".
- **Số BLS theo G1:**
  - 2 666 000 (2025) → 2 524 100 (2035, PROJECTION), −5,3 % ("about five percent").
  - Đợt 2023–33 ở khung riêng, ghi rõ đợt.
  - Thẻ so sánh 10 năm: −16,1 % ACTUAL ↔ −5,3 % PROJECTION.
  - Không còn số 2024–34.
- **Kiểm so sánh 6 điểm** vẫn đạt như hồ sơ G1. Các số mới không đặt cạnh số khác loại.

## 4. Thử Sonnet ↔ Opus (cùng đoạn đồ hoạ 10b, cùng đề bài, cùng thư viện)
| | Opus | Sonnet |
|---|---|---|
| Token (harness) | 64,5 nghìn | **60,0 nghìn** (−7 %) |
| Thời gian | 66 s | 44 s |
| Kết quả | 9 shot, mọi mốc giải được | 9 shot, mọi mốc giải được |
| qc Q1–Q3, Q6–Q8 | ĐẠT | ĐẠT |
| qc Q5 | trượt (lỗi mẫu nhãn "0", chung cho cả hai, đã sửa ở thư viện) | như Opus |
| qc Q11 (đo bản chặt lúc thử) | **ĐẠT** | **TRƯỢT**: 2 quãng đứng 4,1 s và 5,6 s |
| Khung hình | mạch rõ: câu hỏi → tác giả → quy mô → +14 % → cột +14/+34 → trích dẫn | gần tương đương; có một thẻ chữ đứng lâu ("Most experienced… minimal") |

**Kết luận:**
- **Không chuyển phần dựng shot đồ hoạ sang Sonnet** (điều kiện "chỉ chuyển nếu đạt chuẩn kênh": Sonnet trượt Q11 ở lần đầu).
- Chênh token chỉ 7 %. Thêm một vòng sửa sẽ ăn hết phần tiết kiệm.
- Sonnet làm tốt việc tra nguồn (gói nguồn G1). Đề xuất giữ Sonnet cho tra nguồn, Opus cho dựng shot.
- Bản dùng trong phim là bản P viết; không dùng bản của gói thử.

## 5. Token thực (trần tập 2: 1,2 triệu)
| Phần | Token | Nguồn số |
|---|---|---|
| G1: tra nguồn (gói Sonnet) | 101,2 nghìn | harness |
| G1: P (đề tài, kịch bản v1, đặc tả, hồ sơ) | ≈ 40 nghìn | ước |
| Sau G1: tra nguồn bổ sung | ≈ 20 nghìn (trần 80) | bộ đếm phiên P |
| Sau G1: P sản xuất (đặc tả v2, sửa thư viện/qc, render, đóng gói, báo cáo) | ≈ 115 nghìn | bộ đếm phiên P |
| Thử Sonnet ↔ Opus | 124,5 nghìn (60,0 + 64,5) | harness |
| **Tổng tập 2** | **≈ 0,40 triệu** | **33 % trần**; tập 1: 2,16 triệu (giảm ≈ 81 %) |

- Theo phút phim: ≈ 0,045 triệu/phút (tập 1: 0,215).
- Bỏ phần thử A/B (việc một lần) thì sản xuất tập ≈ 0,28 triệu.
- **ElevenLabs:** phiên gửi 7 533 ký tự (16 đoạn + 3 Short), một lần thu, không thu lại.
- Bộ đếm tài khoản tăng 8 503 → 15 729 (+7 226) trong phiên, lệch số đã gửi khoảng 300 ký tự (bộ đếm cập nhật trễ hoặc có lượt dùng ngoài phiên); nhờ chủ dự án xem trên tài khoản.

## 6. Giờ máy và đĩa
| Việc | Đo |
|---|---|
| Render đồ hoạ / cảnh 2.5D | 0,20–0,36 s/khung (3 tiến trình song song) |
| Lượt build trọn cuối (render 6 đoạn đổi + mix + master + 3 phần + Shorts) | 3 367 s |
| Lượt sửa đoạn 10 + Shorts | 2 888 s; lượt Shorts riêng ≈ 6 phút |
| **Tổng đồng hồ** các lượt build tập 2 | **≈ 2,5 giờ**, gồm 2 lượt bị dừng giữa chừng |
| **Giờ máy ước** (4 vCPU) | **≈ 5 giờ**. Phần lớn là mã hoá 2 lượt "slow" cho 3 phần bản xem, lặp 3 lần |

- **Đĩa:** trống ≥ 17,9 GB suốt mốc, trên ngưỡng 3 GB.
- **Giữ ngoài git:** `/var/tmp/cine-out/ll-ep02` gồm trung gian 16 đoạn và master. Xoá khi G2 duyệt.

## 7. Số lần chủ dự án chạm (tập 2)
| # | Lần | Nội dung |
|---|---|---|
| 1 | G1 (05/10) | duyệt đề tài và kịch bản, sửa số BLS, đặt tiêu đề, chọn B, người dẫn vô danh |
| 2 | **G2 (bây giờ)** | duyệt bản cuối, Shorts, thumbnail |
| 3 | G3 | bấm phát hành |

**Chỉ 3 lần**, đúng chính sách 3 cổng. Không có ngoại lệ phải hỏi: không vượt trần token, không đổi kịch bản đã duyệt ngoài sửa của G1, không có số chưa xác minh, không có tài sản mới.

## 8. Hàng chờ nhỏ (không chặn G2)
1. Đoạn 08: cột 2025 chỉ hiện đủ số ≈ 0,8 s trước khi chuyển đoạn.
2. Nhãn "73,030" sát trục và "152,700" chạm đường (đoạn 03).
3. Short S1: chữ đứng 3,04 s ở câu cuối.
4. Tay bóng người ở cảnh tổng đài còn cứng (đã biết từ Mốc B).
5. Mã hoá bản xem 2 lượt "slow" chiếm phần lớn giờ máy; có thể đổi sang "medium" cho bản duyệt.

## 9. Chờ chủ dự án — CỔNG G2
1. **Duyệt bản cuối:** xem `screening/ll-ep02-v1-p1/p2/p3.mp4`. Master trên nhánh `release-ll-ep02-v1`, SHA `8b3c0be6…94383c9`.
2. **Duyệt 3 Shorts:**
   - S1 "Automation hurt the operators — not the next generation";
   - S2 "How many U.S. customer service jobs could disappear?";
   - S3 "The night the switchboard went quiet".
3. **Chọn thumbnail:**
   - T1: phòng tổng đài + "Automation hurt the operators. Not the next generation. What about us?";
   - T2: thẻ so sánh + "Then −16% · Next −5%?".
   - P đề xuất T1, thử A/B với T2.
4. **Sau G2:** xoá trung gian, rồi tới G3 (bấm phát hành theo cách của tập 1).
