# TẬP 4 — CỔNG G2: bản cuối · 05/10/2026

**P DỪNG ở G2, chờ chủ dự án duyệt bản cuối, Shorts và thumbnail.**
- Tiêu đề đã chốt ở G1: "The Typewriter Opened a Door for Millions of Women. Who Gets the Next One?".
- Đây là tập đầu tiên áp **luật nhịp Q14–Q18** (quyết định "HẤP DẪN & GIỮ CHÂN", 05/10/2026).
- Dựng bằng nhà máy: `reports/m3/ep04/episode.yaml` (v3), `scripts/ll/build.sh`, kiểm bằng `scripts/ll/qc.sh`.
- Mọi số dưới đây là số đo thật trên tệp.

## 1. Bàn giao
| Tệp | Thông số | Dung lượng | SHA-256 |
|---|---|---|---|
| Master (Git LFS, nhánh **`release-ll-ep04-v1`**, commit `ab9d3bb`): `ll-ep04-v1-master-1080p.mp4` | 1920×1080, 24 fps, crf 16, **8:34,67** (12 352 khung) | 308,7 MB | `856971a3b29ecea9ca5ebb52827bfae36e792f7428a8835249dfd8129d5255be` |
| `screening/ll-ep04-v1-p1.mp4` | đoạn 00–04 (0:00–2:38,5), 720p | 58,2 MB | `2a46691c…f179fc9a` |
| `screening/ll-ep04-v1-p2.mp4` | đoạn 05–09 (2:38,5–5:57,7) | 73,0 MB | `a54e47f2…a5304831` |
| `screening/ll-ep04-v1-p3.mp4` | đoạn 10–13 (5:57,7–8:34,7) | 57,3 MB | `cbbb7d06…0421f190` |
| Shorts S1/S2/S3 (LFS, cùng nhánh) | 1080×1920; 32,6 / 26,6 / 23,7 s | 7,5 / 6,9 / 6,4 MB | `SHA256SUMS.txt` của nhánh |
| Thumbnail T1, T2 · mô tả (14 chương) · text Shorts · phụ đề `.srt` | cùng nhánh và `reports/m3/ep04/phat-hanh/` | | |

- **Kiểm sau khi đẩy:** tải ngược **9/9 tệp** (LFS qua media.githubusercontent.com, tệp thường qua raw.githubusercontent.com), `sha256sum -c`: **cả 9 OK**.
- Khung tổng quan (28 shot): `reports/m3/ep04/khung-g2.jpg`. Bảng khán giả (tự sinh): `reports/m3/ep04/KHAN-GIA.md`.

## 2. Kết quả `qc.sh` lượt cuối: **ĐẠT 31/31** (bảng đầy đủ: `reports/m3/ep04/qc-g2.md`)
| Mục | Giá trị |
|---|---|
| Q1–Q3 judder, khung gần trùng, máy xuyên hình | 0 · 0 · 0 |
| Q4 loudness / true peak | master **−14,1 LUFS / −1,6 dBTP**; phần −14,7 / −14,8 / −14,6 (TP ≤ −1,6); Shorts −14,1 / −14,0 / −14,0 |
| Q5 tương phản thấp nhất | 5,79:1 |
| Q6 cỡ chữ hoa tối thiểu | 30,7 px (Shorts) |
| Q7, Q8, Q9, Q10, Q11, Q12, Q13 | ĐẠT (0 lỗi; 12 352/12 352 khung; phần ≤ 73,0 MB; T1/T2 lề 5 %) |
| **Q14 móc câu** | câu hỏi ở 0:00,6 ("What happened to the typing pool?") + chú thích trên cảnh; **tựa ở 0:18,6**; trả lời ở đoạn 12 ("the next door") |
| **Q15 đổi hình** | quãng dài nhất **8,0 s** (đúng ngưỡng), trung bình **3,0 s** |
| **Q16 thẻ giấy** | **32,1 %** (trần 55 %) |
| **Q17 mật độ số** | **15 số / 8,6 phút = 1,75/phút**. Neo: 3,9 triệu (1970) · 1 416 000 (1988) · −34,4 % (2025–35) |
| **Q18 thẻ trống** | 0 |
| **Q19 hồ sơ quyền tư liệu** | không dùng tư liệu |

**Chỉ số trong ±5 % quanh ngưỡng:**
- Q15: quãng dài nhất 8,0 s = ngưỡng 8 s;
- cỡ chữ Short 30,7 px (ngưỡng 30);
- STORY 17,7 % (đích 20 ±5: −2,3 điểm, trong giới hạn).

**So với trước luật nhịp** (đặc tả v2 của cùng tập, đo bằng `rhythm.py`):
| | Trước | Sau |
|---|---|---|
| Tựa phim | 0:46 | **0:18,6** |
| Móc câu < 0:15 | không | có |
| Quãng không đổi hình dài nhất | 18,1 s | **8,0 s** |
| Thẻ giấy | 80,1 % | **32,1 %** |
| Số trên hình | 27 (3,1/phút) | **15 (1,75/phút)** |
| Thẻ trống > 1,5 s | 7 | **0** |

**Lỗi bắt được trong lúc sản xuất (đã sửa trước khi giao):**
1. Shorts: chữ đứng > 3 s (9 quãng) và "million" tương phản 1,19:1. Đã dựng lại 3 Shorts bằng cảnh + chú thích đổi theo lời.
2. True peak phần 1 bản xem −0,8 dBTP. Bản xem hạ 0,6 dB (`build.sh`).
3. Q13: số "444" trong text Shorts chưa có trong `numbers`. Đã thêm.
4. **P tự phát hiện khi rà khung tổng quan:** màn hình phòng đánh máy hiện nhãn "AUTOMATED VOICE" (mặc định của tập 2) ở 4 đoạn. Đã đổi thành "WORD PROCESSOR" và render lại 4 đoạn.
5. **Lỗi nhà máy:** băm đoạn rỗng (thư mục `lib/preview` lọt vào danh sách) làm `build.sh` suýt giữ 6 đoạn trung gian cũ của đặc tả trước luật nhịp. Đã sửa: băm chỉ `lib/*.js`, băm rỗng = lỗi. Đã render lại toàn bộ.

## 3. Nội dung, tỷ lệ, kiểm mù
- **Thời lượng 8:34,7. Tỷ lệ 17,7 / 33,8 / 48,4 %**, cả ba trong ±5 điểm.
- **Theo quyết định "HẤP DẪN & GIỮ CHÂN"** (không đổi nội dung đã duyệt):
  - 15 s mở đầu mới dùng 2 số neo, kết bằng câu hỏi "Who gets the next door?". Câu hỏi được trả lời ở đoạn 12.
  - Người thắp đèn làm cầu nối ngắn (đoạn 01: 40 s → 24 s), tựa phim đặt ở đầu đoạn 01.
  - 7 thẻ chữ/cột thành **cảnh có chú thích đè** (`cap`).
  - Gộp số phụ: số đếm 2025/2035 chỉ đọc trong lời, trên hình giữ % thay đổi.
  - Mọi cảnh còn lại có mốc máy quay ≤ 6 s.
- **Kiểm mù** (1 subagent Sonnet, 3 vai, 47,3 nghìn token, trước khi thu giọng). Điểm có ≥ 2/3 vai cùng nêu đã sửa:
  - thẻ +69 % ↔ −2 % thay bằng thẻ BLS 2025–35 cùng nguồn, cùng kỳ (3/3);
  - giọng kết "nghề đã chết": thêm "and millions still keep an office running" (2/3);
  - đoạn 05 dày số (2/3);
  - đợt dự báo khác nhau của phiên mã y khoa (2/3).
- **ASR:** 18/18 đoạn ĐẠT. Báo sai tên "Shakked/Noy" làm đoạn 10 thu lại 2 lần thừa (≈ 1 300 ký tự). Đã nới so tên trong `asr.py`.

## 4. Thư viện HÌNH v2 (mục C; dùng từ tập 6) — làm song song, không dừng
| Hạng mục | Kết quả |
|---|---|
| C1 số trong thế giới cắt giấy | mẫu `isotype` (hàng hình người), `stack` (cột dựng bằng đồ vật: hồ sơ, máy đánh chữ, ATM…), `sign` (số sơn trên biển hiệu, đèn rọi) |
| C2 đạo cụ + nhân vật | `props.js`: 10 đạo cụ cắt giấy theo thời kỳ; `worker()` (nhân vật vô danh, khăn quàng màu nhấn cố định); mẫu `desk` (đổi thời kỳ 1900 → 2025 trên cùng một bàn) |
| C3 tư liệu phạm vi công cộng | mẫu `archive` (Ken Burns + phủ tông B3 + vignette + dòng nguồn); `rights_check.py` + **qc Q19** (danh sách trắng loc.gov/*.gov, tình trạng quyền nguyên văn, ngày tải, ≤ 20 %). Tư liệu đầu tiên: LoC FSA/OWI 8d03493 ("No known restrictions"), RIGHTS `LOC-8d03493` |
| C4 test + xem trước | `scripts/ll/tests`: **19 mẫu** (13 cũ + 6 mới) ĐẠT, chạy đầu mỗi build; ảnh xem trước + tham số trong `scripts/ll/lib/README.md` |
| C5 lát cắt 90 s v1 ↔ v2 | xem mục 4.1 |
| AUTHORSHIP/RIGHTS | đã ghi việc đổi quyết định "chỉ dựng hình bằng mã" |

### 4.1 Lát cắt tự kiểm (ba đoạn đầu tập 4; `reports/m3/v2-lat-cat/`)
| Đo (`rhythm.py`) | v1 (đặc tả cũ, thư viện v1) | v2 (luật nhịp + thư viện v2) |
|---|---|---|
| Q14 | TRƯỢT (tựa 0:46, không móc câu) | ĐẠT (tựa 0:18,6) |
| Q15 quãng dài nhất / TB | 17,6 s / 5,4 s | **7,1 s / 2,6 s** |
| Q16 thẻ giấy | 50,0 % | **3,4 %** (tư liệu LoC + isotype thay cảnh hàng ghế + đường) |
| Q17 | 1,96/phút | 3,39/phút. Lát cắt 90 s dồn cả móc câu lẫn 3 số lịch sử; luật tính trung bình trên cả tập |
| Q18 | 0 | 0 |
- Video lát cắt: xem mục 7 (đang/đã render, ngoài git, `/var/tmp/cine-out/ll-cut-v*/`). Chủ dự án xem ở G2 tập 6 theo chỉ đạo.

## 5. Token, ElevenLabs, giờ máy, đĩa
| Phần | Token | Nguồn số |
|---|---|---|
| Kiểm mù (1 subagent, 3 vai) | 47,3 nghìn | harness |
| P: sửa theo kiểm mù, thu giọng, luật nhịp B (viết lại đặc tả 2 lượt), 5 lượt build/qc, phát hành, báo cáo | ≈ 190 nghìn | ước |
| **Tổng tập 4** | **≈ 0,24 triệu / trần 0,5 triệu (48 %)** | |
| Mục B cho tập 4 (trần 30 nghìn) | ≈ 35 nghìn (ước), **vượt khoảng 17 %**: hai lượt sửa Q15 | ước |
| Dựng luật nhịp (rhythm.py, qc, build.sh, cap) | ≈ 25 nghìn | ước |
| Thư viện HÌNH v2 (trần 150 nghìn) | ≈ 60 nghìn | ước |

- **ElevenLabs:** gửi 8 384 + 504 = **8 888 ký tự**. Gồm 2 lần thu thừa đoạn 10 do ASR báo sai, và 2 đoạn mở đầu mới. Bộ đếm tài khoản 23 527 → 27 538.
- **Giờ máy:** 5 lượt build (3 299 + 2 265 + 2 216 s + 2 lượt dở). Một lượt mất do máy khởi động lại; một lượt P dừng khi phát hiện lỗi băm.
- **Đĩa:** trống ≥ 15,6 GB. Trung gian `/var/tmp/cine-out/ll-ep04` giữ đến khi G2 duyệt.

## 6. Hàng chờ nhỏ (không chặn G2)
1. Hình người ở mẫu `rows` phòng đánh máy giơ tay cao như đang vẫy (tư thế tổng đài cũ). Sửa ở thư viện lần chạm tới; nếu làm bây giờ, mọi đoạn phải render lại.
2. Thumbnail T1 dùng cảnh `desk` của thư viện v2 (người đánh máy bên máy chữ). Đây là xem trước phong cách v2.
3. Q15 đúng ngưỡng 8,0 s ở một quãng.

## 7. Chờ chủ dự án — CỔNG G2 tập 4
1. **Duyệt bản cuối:** xem `screening/ll-ep04-v1-p1/p2/p3.mp4`. Master trên nhánh `release-ll-ep04-v1`, SHA `856971a3…d5255be`.
2. **Duyệt 3 Shorts:**
   - S1 "Stenographers, typists & secretaries: 134,000 to 3.9 million";
   - S2 "The job AI names directly: medical transcription";
   - S3 "37% faster with AI — but not typists".
3. **Chọn thumbnail:**
   - T1: người đánh máy + "THE TYPEWRITER OPENED A DOOR FOR MILLIONS OF WOMEN. WHO GETS THE NEXT ONE?";
   - T2: thẻ so sánh + "TYPISTS −34.4% BY 2035 · BLS PROJECTION".
   - P đề xuất T1, thử A/B với T2.
4. **Sau G2:** P chuẩn bị G3 (hướng dẫn đăng, xoá trung gian), rồi sang tập 5: thu giọng, đo Q14–Q18 trên timeline thật, dừng ở G2.
