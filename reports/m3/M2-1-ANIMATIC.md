# M2.1 — ANIMATIC NHỊP tập thử "The Last Lamplighters" (01/10/2026)

Kênh Last Lamplighters, Mốc 2. Chủ dự án duyệt M2.0 và mở M2.1 (AUTHORSHIP 01/10/2026).
- Xưởng: nhánh `thu-phong-cach` @49df834 (đã push, không merge).
- P: thử giọng, kiểm, tổng hợp.
- Xưởng không ghi được tệp .md, nên P lưu nội dung báo cáo của xưởng vào tệp này.

**Sản phẩm:** `screening/ll-ep01-animatic.mp4`, **9:37,50** (577,5 s), 25,6 MB, 960×540, 24 fps, H.264 + AAC, 75 shot, phụ đề tiếng Anh cháy vào hình. Phụ đề rời: `reports/m3/m2-1/ll-ep01-animatic.en.srt`.

## 1. Giọng và nhịp (a)
**Thử ElevenLabs tốc độ 1,05 (P)** trên cùng đoạn mẫu 375 ký tự, giọng Bill, `eleven_multilingual_v2`:

| Bản | Thời lượng | Từ/phút | Ghi chú |
|---|---|---|---|
| 1,00 (mẫu M2.0) | 29,75 s | 141,2 | `reports/m3/m2-1/bill-1.00.mp3` |
| ElevenLabs speed 1,05 | 29,68 s | 141,5 | **gần như không tác dụng**; `bill-1.05.mp3` |
| ffmpeg atempo 1,05 (giữ cao độ) | 28,37 s | 148,0 | `bill-1.00-atempo1.05.mp3`; chủ dự án nghe để chấm độ tự nhiên |

- **Ký tự ElevenLabs:** trước 84 689 → sau 84 839 (+150 cho 375 ký tự gửi đi). Gói API vẫn báo **Starter**, 105 779 ký tự/kỳ, còn **≈ 20 940**. Việc nâng lên Creator chưa thể hiện trên API lúc kiểm.
- Số dư sau khi chừa cho Crux chưa chắc ≥ 15 000, nên **chưa thu trọn lời dẫn** bằng ElevenLabs; animatic dùng flite theo chỉ thị.

**Nhịp bằng flite** (giọng kal16):
- mỗi câu đọc riêng; hệ số atempo đặt riêng cho từng đoạn để lời dẫn đúng 141,2 từ/phút (hệ số 0,683–1,039);
- nghỉ 0,30 s giữa câu, 0,60 s giữa đoạn văn, 0,80 s cuối đoạn;
- giữ các khoảng lặng của kịch bản: VO vào trễ +2/+3 s; thoại Ida 01-04 và 05-08; lặng 10-04 + 10-05 (11 s); 10-09, 10-10; Ida L1 nghe xa ở 14-03.

| Phương án | Có đoạn 07 | Cắt đoạn 07 |
|---|---|---|
| 1,00 (141,2 từ/phút) | 10:04,63 (quá trần 4,6 s; +0,8 %, trong ±5 %) | **9:37,48 ✔ CHỌN** |
| atempo 1,05 (≈ 148 từ/phút) | 9:40,31 | 9:14,30 |

**Chọn: 1,00 + cắt đoạn 07** (bậc 2 theo thứ tự ưu tiên; việc cắt đoạn 07 đã được duyệt). Còn dư 22,5 s so với trần (3,8 %, trong ±5 %).

## 2. Thời lượng từng đoạn (thực tế)
| Đoạn | Số từ | Hệ số atempo | Kết thúc | Dài (s) | Bảng shot (s) |
|---|---|---|---|---|---|
| 01 | 96 | 0,704 | 0:48,59 | 48,6 | 45 |
| 02 | 129 | 0,785 | 1:47,21 | 58,6 | 56 |
| 03 | 101 | 0,765 | 2:30,93 | 43,7 | 45 |
| 04 | 63 | 0,855 | 2:58,50 | 27,6 | 28 |
| 05 | 145 | 0,842 | 4:07,91 | 69,4 | 63 |
| 06 | 102 | 0,790 | 4:52,05 | 44,1 | 41 |
| 08 | 123 | 0,986 | 5:45,12 | 53,1 | 49 |
| 10 | 100 | 0,683 | 6:46,41 | 61,3 | 52 |
| 11 | 79 | 0,993 | 7:20,78 | 34,4 | 34 |
| 12 | 116 | 1,039 | 8:10,87 | 50,1 | 47 |
| 13 | 128 | 1,001 | 9:06,06 | 55,2 | 51 |
| 14 | 65 | 0,933 | 9:37,48 | 31,4 | 33 |

- Bảng từng shot: `reports/m3/m2-1/thuc-te.json`; nhịp: `nhip.json`.
- Shot ngắn dưới 2,5 s: 03-02 (2,4 s), 05-02 (2,1 s), 12-01 (2,3 s).

## 3. Hình (b), phụ đề (d), thẻ Bessen (e)
- **Hình:**
  - 29 khung tĩnh render với cờ b3v3 (28 shot nguồn + lp20), có pan/zoom nhẹ;
  - 25 thẻ dữ liệu theo bộ mẫu B3;
  - 11 thẻ PLACEHOLDER.
  - Tương phản chữ trên thẻ thấp nhất 5,28:1.
  - Cắt thẳng trong đoạn; nhúng đen 8 khung ở ranh giới đoạn.
- **Thoại Ida:** dùng lại take C4-D1 (L1, L2; RIGHTS M1-V3). L1 dùng lần hai ở 14-03, xử lý nghe xa.
- **Phụ đề:** 165 câu, chữ trắng trên hộp đen 75 %. Tương phản đo trên chính mp4: thấp nhất 6,71:1, trung vị 20,5:1.
- **Thẻ Bessen:** đã đổi đúng câu "Only 1 of ~270 occupations was eliminated mainly by automation" ở thẻ 11-04, tấm mẫu `mau-d-num.png` và thẻ 14-01.

**Placeholder**
- Thẻ PLACEHOLDER (tài sản mới chưa làm): 02-03, 04-02, 04-03, 06-02, 06-03, 06-04, 08-01, 08-03, 08-05, 08-06, 11-01.
- Bản đồ dùng khung chung: 03-03, 04-01, 04-04, 05-03, 05-04, 06-01.
- Khung b3v3 có nhãn TEMP (dàn dựng mới chưa làm): 01-07, 01-08, 02-07, 03-01, 03-02, 03-04, 03-05, 03-06, 03-07, 05-10, 06-05, 10-03, 14-02.
- 13-02 ghi "+30% or more", vì kịch bản không có số riêng cho từng nghề.

## 4. Nhạc tạm (c)
- Freesound #496757 "Ambient Wave 48 (Tribute)", tác giả Erokia, **CC0**.
  - Do người làm: tải lên 2019, mô tả cách làm bằng VST/EQ/sampling, không gắn nhãn AI.
  - P đã kiểm trên trang gốc: "Creative Commons 0".
- Mức: −20 dB so với lời, hạ thêm −10 dB khi có lời.
- RIGHTS: M2-MUS-1 (nhạc), M2-VO-0 (lời dẫn flite).

## 5. Shorts (f)
| Short | Đoạn | Thời điểm | Dài | Khung 9:16 dự kiến |
|---|---|---|---|---|
| S1 "London's last lamplighters" | 08 | 4:52,05–5:45,12 | 53,1 s | shot 3D cắt dọc giữa khung; các thẻ dàn lại dọc |
| S2 "Today's shortest rounds" | 12 | 7:20,78–8:10,87 | 50,1 s | toàn thẻ, dựng bản dọc riêng |
| S3 "One job in 270" (đề xuất thêm) | 11 | 6:46,41–7:20,78 | 34,4 s | lưới 270 ô xếp lại 15 × 18 |

## 6. Điểm cần chủ dự án chốt
1. **s22 (shot 05-08):** hai chỉ thị mâu thuẫn. M2.0 đã duyệt B3 v3 (thấy cột điện ở rìa khung), trong khi BANG-SHOT §1 ghi "không có cột điện trong khung" theo B3 v2. Animatic dùng b3v3.
   - **P đề xuất giữ b3v3**: chủ dự án đã duyệt "s22 đạt" ở M2.0, và world-rules v0.6 cho phép cột điện ở mé đối diện. P sẽ sửa BANG-SHOT khi được duyệt.
2. **Thẻ −34 % ở 12-01 chỉ đứng 2,3 s.** Đề xuất giữ thẻ này làm lớp trên 12-02 thêm 3 s ở bản dựng sau, để con số neo đứng ≥ 5 s.
3. Duyệt nhạc tạm M2-MUS-1 và 3 Shorts (S3 là đề xuất mới).
4. Duyệt nhịp (≤ 10:00) và giọng (Bill 1,00; atempo 1,05 chỉ là phương án dự phòng) → mở M2.2.
5. ElevenLabs: khi API báo Creator, P thu trọn lời dẫn bằng Bill, khoảng 7 400 ký tự (đoạn 07 đã cắt nên ít hơn), ghi số dư trước và sau mỗi lượt.

## 7. Token (bộ đếm harness)
| Phần | Token | Hạn |
|---|---|---|
| Xưởng (nhịp, hình, nhạc, phụ đề, dựng) | ≈ 94 nghìn | 160 nghìn |
| P (thử giọng, kiểm, tổng hợp) | nhỏ (không đo chính xác) | |
| **M2.1** | **≈ 100 nghìn** | 220 nghìn |

**Dựng lại:** chạy `design/m3/animatic/nhip.py`, `frames.js --mid` với cờ b3v3 cho từng shot nguồn, `the.py`, rồi `dung.py … screening/ll-ep01-animatic.mp4 1.00 1` (trên nhánh `thu-phong-cach`; mã lưu trong `reports/m3/thu-phong-cach/ma-thu-phong-cach.patch`).
