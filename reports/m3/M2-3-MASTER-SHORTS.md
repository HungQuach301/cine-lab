# M2.3 — MASTER + SHORTS + GÓI PHÁT HÀNH + GỬI K · 04/10/2026

**Cổng G2: P DỪNG, chờ chủ dự án duyệt bản cuối và chọn tiêu đề/thumbnail.**
- Master dựng trên v3 đã duyệt, cộng các sửa M2.2 (`reports/m3/M2-2C-HOAN-THIEN.md`).
- Mọi số là **số đo thật trên tệp**.

## 1. Bản cuối (master)
| Tệp | Thông số | Dung lượng | SHA-256 |
|---|---|---|---|
| Master (ngoài git): `/var/tmp/cine-out/ep01/out4/ll-ep01-animatic-m23-master.mp4` | 1920×1080, 24 fps, H.264 crf 16, AAC 256 kb/s | 852,9 MB | `9c3825387345ec0af6c035ec3f94809644ca7767d1ecbafcaed4710480113942` |
| `screening/ll-ep01-m23-p1.mp4` | đoạn 00–07 (0:00–3:26,25); 720p, 24 fps, hình 2,8 Mb/s | 75,0 MB | 4c8b71e9…f9338a5 |
| `screening/ll-ep01-m23-p2.mp4` | đoạn 08–14 (3:26,25–7:17,92) | **84,8 MB** | 9a258f6b…e70e5d5 |
| `screening/ll-ep01-m23-p3.mp4` | đoạn 15–19 (7:17,92–10:02,58) | 60,8 MB | aac50b57…5af4f |

| Chỉ số | Chuẩn | Master | 3 phần (đối chiếu) |
|---|---|---|---|
| Thời lượng | ≤ 11:00 | **10:02,58** (14 462 khung) | 206,25 + 231,67 + 164,67 s |
| Judder | 0 | **0** trên trung gian cả 17 đoạn (số chuẩn) và trên master | 0 / 0 / 0 |
| Giữ ≥ 1 s / giữ 13–23 / giây < 12 khung mới | 0 | 0 / 0 / 0 | 0 |
| Loudness | −14 LUFS | **−14,0** | −14,2 / −14,0 / −14,0 |
| True peak | ≤ −1 dBTP | **−1,6** | −1,4 / −1,3 / −1,3 |
| LRA | — | 3,8 LU | 5,1 / 2,7 / 3,5 |
| Nhạc hạ khi có lời | 10–14 dB | 12,0 dB | |
| SFX | — | 36 cue (M2-SFX-1/2/3, CC0) | |
| Tỷ lệ STORY / HISTORY / TODAY | 20 / 35 / 45 % | 17,2 / 36,2 / 46,6 % (6 s móc tính vào TODAY) | |
| Tương phản chữ thấp nhất | ≥ 4,5:1 | **4,91:1** ("1807", đoạn 02). Hai mức thấp của v3 đã hết: 4,79 ("1820s", đã bỏ) và 4,86 (06, nay 5,30) | |
| Mù màu | đạt | đạt (8 khung số, v3; các đoạn đồ hoạ số không đổi màu ở M2.2) | |

- Mốc chapter đã kiểm trên master: 0:47 vào đoạn 02 (tờ giấy bản đồ); 4:41 vào khối 10–13 (lưới văn phòng).

### Chỉ số trong ±5 % quanh ngưỡng
- **Phần p2:** 84,8 MB so với trần 90 MB, cách 5,8 %.
- **True peak hai phần p2, p3:** −1,3 dBTP, cách ngưỡng −1 dBTP 0,3 dB, do mã hoá lại AAC. Master đạt −1,6.
- **Dòng nguồn 26 px:** chữ hoa ≈ 18,95 px, cao hơn ngưỡng 18 px 5,3 % (M2-2C §4).
- **Cỡ chữ Shorts:** chữ hoa ≈ 30,6 px, cao hơn ngưỡng 30 px 2 %.
- **Dòng nguồn S3 (Census, Bessen):** chân chữ ở y ≈ 1471–1476, cách mép dưới vùng an toàn (1500) ≈ 2 %.

## 2. Shorts 9:16 (`screening/ll-ep01-short-S1/S2/S3.mp4`)
**Chọn 3 trong 4** (S1–S4 theo kịch bản v3.1):

| Short | Nguồn | Lý do chọn |
|---|---|---|
| **S1 "London still has lamplighters. Five of them."** | đoạn 07 | Chi tiết lạ, đúng sự thật, dễ chia sẻ. Một số neo (5 người, ~1 100 đèn, British Gas 2023); không phải so sánh |
| **S2 "Which American jobs are shrinking fastest?"** | khối 10–13 | Câu hỏi tìm kiếm có nhu cầu cao. Số −34 % rõ, có nguồn BLS; dẫn về câu hỏi chính của phim |
| **S3 "One job in 270"** | đoạn 08 | Câu chuyện trọn vẹn (thang máy, Bessen), mạnh về "điều bạn chưa biết". Số thực tế, có ngắt phân loại đúng như bản 16:9 |
| ~~S4 Stanford~~ | đoạn 17 | **Bỏ.** Lời dẫn cần câu rào "early signal, not proof"; đứng riêng 30–40 s dễ bị cắt ý và hiểu thành "AI đang lấy việc người trẻ". Rủi ro hiểu sai cao nhất trong 4 |

| Short | Thời lượng | Khung | Judder | Loudness / TP | Tương phản thấp nhất | Dung lượng | SHA-256 |
|---|---|---|---|---|---|---|---|
| S1 | 33,96 s | 815 | 0 / 0 | −14,1 LUFS / −1,3 dBTP | 7,58:1 | 7,3 MB | b13b66c7…c2c0e3 |
| S2 | 39,71 s | 953 | 0 / 0 | −14,0 / −1,4 | 6,24:1 | 21,9 MB | 253bda06…0a0eb6 |
| S3 | 46,83 s | 1 124 | 0 / 0 | −14,0 / −1,3 | 6,39:1 | 29,4 MB | 233eef54…3f606 |

- **Định dạng:** 1080×1920, 24 fps, H.264 crf 18, AAC 192 kb/s. Judder đo trên trung gian và trên tệp cuối, đều 0.
- **Vùng an toàn:** chữ và số chính nằm trong x 60–900, y 260–1500. Thẻ kết dọc "Last Lamplighters · full film on the channel".
- **Lời:**
  - S1, S2: Bill thu mới (868 ký tự), whisper khớp văn bản.
  - S3: dùng nguyên lời đoạn 08.
  - S1 thay câu mở đúng theo dòng *Bản Short* của kịch bản.
  - S2 đổi câu mở và bỏ câu thang máy theo kịch bản; **P bỏ thêm "Today," và "of its own"** vì hai cụm này chỉ có nghĩa khi nối với câu đã bỏ. Câu thành "The U.S. Bureau of Labor Statistics has a list: …". Đây là chỉnh ngữ pháp, không đổi nội dung.
- **Âm thanh:** lời vào ở 0,6 s; nhạc "Immersed" hạ theo lời (sidechain); chuẩn −14 LUFS hai lượt. Chưa có SFX trong Short.
- **Chữ mới trên hình** (chi tiết trong báo cáo xưởng, lưu ở mục 7):
  - S2: tiêu đề 2 dòng; bìa BLS; "same pattern"; rút tên "Switchboard operators" (bỏ "incl. answering service").
  - S3: chú giải 3 dòng phân loại 1950/1960/1970 thay cho ghi chú nhỏ.
  - S1: "Covent Garden · The Mall / palaces & theatres", "clockwork timer", dải 14 ô "every two weeks".
- **Điểm yếu:**
  1. S1 0,6–6,9 s chỉ có chữ "London" và cảnh lia; câu "Five of them" ở 2,9 s chưa có hình riêng.
  2. Nền S1 là một khung tĩnh lia ngang, vì trung gian 07 về sau đã in sẵn chữ lên hình.
  3. Biểu tượng góc S3 nằm trong lề nút của YouTube (chỉ trang trí).

## 3. Gói phát hành nháp (`reports/m3/m2-3/GOI-PHAT-HANH-NHAP.md`)
- **3 tiêu đề:**
  - A "The Last Lamplighters: Which Jobs Are Next?"
  - B "Jobs Shrinking Fastest by 2035, and the Last Lamplighters"
  - C "London Still Has 5 Lamplighters. Who Are the Last of Our Time?"
- **3 thumbnail** cùng hệ nhận diện (`reports/m3/m2-3/thumb/T1-den-bung.jpg`, `T2-tru-34.jpg`, `T3-con-5.jpg`). **P đề xuất C + T3**, dùng A + T1 để thử A/B.
- **Mô tả:**
  - 17 chapter, mốc kiểm trên master;
  - danh sách nguồn, đã bỏ Wikipedia;
  - **câu ghi công Kevin MacLeod "Immersed" và "Reawakening", CC BY 4.0 (bắt buộc)**;
  - đoạn "How this film was made".
- **Tiết lộ AI:** theo trang chính sách YouTube đọc 04/10/2026, nhãn "AI use" là bắt buộc với nội dung **như thật**. Phim là hoạt hình phong cách hoá, giọng thư viện không nhái người thật, nhạc do người sáng tác, nên **không bắt buộc**. P đề xuất ghi tiết lộ tự nguyện trong mô tả; chủ dự án quyết ở G3 có bật thêm nhãn hay không. Kiểm lại chính sách ngay trước khi phát hành.
- **Phụ đề tiếng Anh:** `reports/m3/m2-3/ll-ep01.en.srt`, 151 khối, có thoại Ida, mốc theo timeline v4. Có 1 dòng dài 44 ký tự (chuẩn 42).

## 4. Gửi K
Đã ghi 7 mục vào `checks-appeal.md` (mục "Yêu cầu mới, 2026-10"; nguồn `reports/m3/YEU-CAU-K-NHAP.md`):
1. C3 cho bóng người.
2. Profile Shorts 9:16.
3. Luật judder.
4. Luật máy xuyên hình học.
5. Kiểm chéo 24 số HSUS từ bản quét.
6. Kiểm lại số BLS 2025–35.
7. Luật "nguồn số không dùng Wikipedia làm nguồn chính".

K là phiên riêng: **chờ K phán quyết và khoá bản checks mới.** Kết quả mục 5–6 có thể dẫn tới sửa hình trước G3.

## 5. Token
**Từng phần của M2.3** (harness cho gói xưởng; P ước):

| Phần | Token |
|---|---|
| Xưởng SHORTS | 157,8 nghìn (hạn 180 nghìn) |
| P: Shorts (lời, mix), master, gói phát hành, thumbnail, phụ đề, gửi K, báo cáo | ≈ 0,12 triệu (ước) |
| **Cộng M2.3** | **≈ 0,28 triệu** |

**Cộng dồn tập 1:**

| Mốc | Token |
|---|---|
| Kịch bản v3 | ≈ 0,18 triệu |
| Lát cắt M2.2a | ≈ 0,23 triệu |
| Animatic v3 (M2.2b) | ≈ 1,10 triệu |
| Hoàn thiện M2.2 | ≈ 0,37 triệu (HISTORY-M22 203,9 nghìn + STORY-M22 64,6 nghìn + P ≈ 0,1 triệu) |
| M2.3 | ≈ 0,28 triệu |
| **Tổng tập 1** | **≈ 2,16 triệu** |

- **So với trần 2,85 triệu:** dùng ≈ 76 %, còn ≈ 0,69 triệu cho sửa sau G2 và G3.
- **Theo phút phim:** 2,16 triệu / 10,04 phút ≈ **0,215 triệu/phút**, dưới trần 0,3 triệu/phút.
- **Độ tin cậy:** số P là ước, vì harness không cho bộ đếm riêng của phiên P. Số các gói xưởng là số harness.

**ElevenLabs:** bộ đếm 8 121/144 034. Có khoảng 2 276 ký tự không do phiên này gửi (M2-2C §6); nhờ chủ dự án kiểm trên tài khoản.

## 6. Đĩa và bàn giao (CHUAN-KENH §6)
- **Mức trống:** thấp nhất ở M2.2–M2.3 là 7,8 GB (sau xưởng HISTORY-M22), trên ngưỡng 6 GB. Lúc ghép master còn 12–14 GB.
- **Đang giữ ngoài git:**

| Thứ giữ | Dung lượng | Ghi chú |
|---|---|---|
| Trung gian `sec/` + `sec-m22/` | ≈ 3,0 GB | `sec-v4/` là symlink |
| Clip shot STORY | ≈ 1,4 GB | |
| Master v3 | 840,7 MB | đã duyệt |
| Master M2.3 | 852,9 MB | |

  Xoá trung gian sau khi G2 duyệt master.
- **Không dùng GitHub Release.** Bản xem 720p 3 phần và 3 Short nằm trong git ở `screening/`; master ở ngoài git, có SHA ở mục 1.
- **Worktree:** đã gỡ hết sau khi lưu bản vá. Bản vá mã:
  - `reports/m3/m2-2b/ma/ma-history-3083243.patch`
  - `reports/m3/m2-2b/ma/ma-story-3cc1654.patch`
  - `reports/m3/m2-2b/ma/ma-today-82cdc61.patch`
  - `reports/m3/m2-3/ma-shorts-*.patch`

## 7. Chờ chủ dự án — CỔNG G2
1. **Duyệt bản cuối:** xem `screening/ll-ep01-m23-p1/p2/p3.mp4`. Master SHA `9c382538…0113942`.
2. **Chọn tiêu đề và thumbnail:** A/B/C × T1/T2/T3. P đề xuất C + T3.
3. **Duyệt 3 Shorts** (`screening/ll-ep01-short-S1/S2/S3.mp4`) và việc bỏ S4.
4. **Xem các sửa M2.2:** đoạn móc 6 s mở đầu, lời mới đoạn 02, bản đồ, cuối 09, e04b, e19a (`reports/m3/M2-2C-HOAN-THIEN.md`, ảnh `reports/m3/m2-2c/truoc-sau/`).
5. **Hàng chờ không chặn G2:**
   - chữ nhỏ ở đoạn 09 lúc bảng còn đủ cỡ;
   - cầu vắt sông ở bản đồ 02;
   - 1,5 s phố trống đầu e19a;
   - khoảng đầu S1;
   - chưa có SFX trong Shorts.
6. **K:** kết quả kiểm HSUS và BLS (mục 4) có thể cần sửa trước G3.
7. **Sau G2:** sửa theo góp ý (nếu có), xoá trung gian, rồi tới G3 (bấm phát hành).
