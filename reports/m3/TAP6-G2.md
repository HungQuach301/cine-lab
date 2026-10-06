# TẬP 6 — CỔNG G2: bản cuối · 06/10/2026

> **KHÔNG PHÁT HÀNH (chủ dự án, 06/10/2026).** Bản v1 này bị rút theo Nguyên tắc tối cao; tập 6 dựng lại (G2 lần 2). Nhánh `release-ll-ep06-v1` giữ làm đối chiếu, không đăng.

**P DỪNG ở G2, chờ chủ dự án duyệt bản cuối, Shorts và thumbnail.**
- Tiêu đề chốt ở G1 (phương án A): "The Computer Replaced the Typesetter and Made the Designer. Now AI Can Draw".
- Số BLS đợt 2025–35 theo duyệt G1:
  - graphic designers −1,7 % (253 100 → 248 800), kèm câu BLS về AI;
  - toàn nền +3,5 %.
- Đoạn 11 viết lại theo CHUAN-KENH §10: không nói về cách làm phim; giữ câu hỏi "the hand that decides" so với "the hand that drew".
- Dựng bằng HÌNH v2 từ đầu; checks LL v2 (LOCK 0973478b…) áp từ tập này.
- Mọi số dưới đây là số đo thật trên tệp.

## 1. Bàn giao
| Tệp | Thông số | Dung lượng | SHA-256 |
|---|---|---|---|
| Master (Git LFS, nhánh **`release-ll-ep06-v1`**, commit `13a4ace`): `ll-ep06-v1-master-1080p.mp4` | 1920×1080, 24 fps, **8:09,9** (11 758 khung) | 232,7 MB | `a5b231450a4fc652c4760d6b923814a91f0cdc5e864b01b9d665c13afaa2a1ee` |
| `screening/ll-ep06-v1-p1.mp4` | đoạn 00–04 (0:00–2:42,3), 720p | 59,0 MB | `7897a6ac…11e480ac` |
| `screening/ll-ep06-v1-p2.mp4` | đoạn 05–08 (2:42,3–5:23,1) | 58,5 MB | `aa6078dd…ee941b90` |
| `screening/ll-ep06-v1-p3.mp4` | đoạn 09–12 (5:23,1–8:09,9) | 60,9 MB | `a32af143…6be02b08` |
| Shorts S1/S2/S3 (LFS, cùng nhánh) | 1080×1920; 24,9 / 21,8 / 25,2 s | 6,5 / 3,9 / 6,7 MB | `SHA256SUMS.txt` của nhánh |
| Thumbnail T1, T2 · mô tả (13 chương) · text Shorts · phụ đề `.srt` | cùng nhánh và `reports/m3/ep06/phat-hanh/` | | |

- **Kiểm sau khi đẩy:** clone mới nhánh phát hành từ remote, `git lfs pull`, `sha256sum -c`: **11/11 OK**.
- Khung tổng quan (31 shot): `reports/m3/ep06/khung-g2.jpg`.
- Bảng khán giả (tự sinh): `reports/m3/ep06/KHAN-GIA.md`.
- Bảng qc đầy đủ: `reports/m3/ep06/qc-g2.md`.

## 2. Kết quả `qc.sh` lượt cuối: **ĐẠT 38/38**, LOCK KHỚP
| Nhóm | Kết quả |
|---|---|
| Q1 judder, Q2, Q3 | 0 / 0 / 0 (16 tệp trung gian) |
| Q4 loudness | Master −14,0 LUFS / −1,6 dBTP. Shorts −14,0 / −14,1 / −14,0 LUFS, −1,6 dBTP. Bản xem −15,1 / −15,3 / −15,3 LUFS, −2,8 / −2,7 / −2,6 dBTP |
| Q5 tương phản thấp nhất | 4,79:1 (đoạn 08, khung 1200, "Designers") |
| Q6 cỡ chữ hoa nhỏ nhất | **30,7 px** (S1 khung 36, dòng nguồn), ngưỡng 30 px → **sát ngưỡng +2,3 %** |
| Q9 số khung | master 11 758 / timeline 11 758 |
| Q10 | bản xem 59,0 / 58,5 / 60,9 MB; Shorts ≤ 25,2 s |
| Q11, Q12, Q13 | 0 / 0 (T1, T2 trong lề 5 %) / 0 |
| Q14 móc câu | câu hỏi và hình trước 0:15 có; tựa 19,5 s; trả lời ở đoạn 11 có |
| Q15 đổi hình | quãng dài nhất **8,0 s** (đúng ngưỡng 8 s), TB 2,7 s |
| Q16 thẻ giấy | 15,8 % (trần 40 %) |
| Q17 mật độ số | 0,98/phút; neo 86 000 / −1,7 % / −17 % |
| Q18 | 0 |
| Q19 tư liệu LoC | 59,5 s ≈ 12,1 %, 2 ảnh, đủ RIGHTS |
| Q20 chữ–hình (cờ `hit` + `zones` isotype, Q-L20) | 0 |
| Q21 gán nguồn | 0 |
| Q22 chữ tràn khung (16:9 và 9:16) | 0 |
| Q23, Q24, Q25 | 0 / 0 / 0 |
| LOCK | KHỚP (0973478b…) |

**Chỉ số trong ±5 % quanh ngưỡng:**
- Q6: 30,7 px so với 30 px.
- Q15: 8,0 s so với 8 s.
- Thời lượng: 8:09,9, cao hơn sàn 8:00 khoảng +2,1 %.

## 3. Nội dung, tỷ lệ, kiểm mù
- **Thời lượng và tỷ lệ:**
  - Thời lượng 8:09,9 so với ước 8:19,5: lời thật ngắn hơn 1,9 %.
  - Tỷ lệ STORY / HISTORY / TODAY = 19,7 / 33,7 / 46,6 %.
  - Phương án A (G1): không cần kéo cảnh truyện.
- **Kiểm so sánh 6 điểm chạy lại với số 2025–35:** đạt cả 6 (`NGUON-TAP6.md` §3).
  - Thẻ duy nhất đặt cạnh nhau: −1,7 % ↔ +3,5 %, cùng BLS, cùng loại, cùng kỳ.
  - Đoạn 10 sửa theo chiều giảm: "then… more designers; this time… the BLS projects fewer designers".
- **Kiểm mù:** đã làm ở G1 cho cả lô (1 subagent, 3 vai), 4 điểm của tập 6 đã sửa.
  - Phần viết lại sau G1 (đoạn 08, 10, 11, S3) **không qua kiểm mù lần hai**, để tiết kiệm khoảng 50 nghìn token.
  - Các câu mới đều trích hoặc diễn giải sát nguồn (OOH 2025–35, MLR 1/2026).
- **ASR:** 13 đoạn và 3 Shorts ĐẠT ngay lần thu đầu; không thu lại đoạn nào.

## 4. Sự cố trong lúc dựng và cách xử lý (đã ghi BAI-HOC #66–69)
| # | Sự cố | Xử lý |
|---|---|---|
| 66 | ASR dừng build: faster-whisper 1.2.1 truyền `metadata_errors` mà PyAV 19 không nhận. `verify.sh` không bắt vì chỉ kiểm import | `asr.py` tự giải mã bằng ffmpeg rồi đưa mảng cho faster-whisper. 0 ký tự thừa (cache theo băm) |
| 67 | **Cổng luật nhịp không chặn**: `rhythm.py \| tee` trả mã của `tee` khi pipefail tắt. Lỗi có từ tập 4, đến nay không lộ vì nhịp luôn đạt. P tưởng build đã dừng ở Q15 nên chạy lượt thứ hai, khiến **2 build ghi chồng một thư mục** | `build.sh` đọc mã qua `PIPESTATUS`. Ca test "dừng mã 3" chạy với `RHYTHM=0`. Xoá trung gian, dựng lại sạch. Luật mới: kiểm `ps` trước mỗi build |
| 68 | **Chữ đè chữ, qc không đo:** dòng nguồn (trái) đè dòng ghi ảnh (phải) ở `archive`; `caption` của mẫu `sign` chồng dải `cap` (BAI-HOC #51 bị quên khi viết đặc tả) | Nhãn `short` gọn, ghi ảnh gọn. `caption` của `sign` đưa vào `cap`, khai nguồn. P thấy khi rà khung tổng quan |
| 69 | Bản xem p1 có true peak −0,0 dBTP dù có `alimiter` | Bộ mã AAC mặc định (twoloop) vọt ≈ 2,5 dB trên phần dài 162 s. Đổi sang `-aac_coder fast`: −2,8 dBTP. Master không đổi |
| — | Q22 Short S3: dòng nguồn ghép 2 nhãn tràn khung 9:16 | `ll.py` bỏ nhãn trùng. OOHGD và EP dùng chung nhãn gọn "BLS projections 2025–35" |
| — | Q15 đoạn 10: 8,4 s trên lời thật (ước 8,0 s) | Thêm mốc máy ở "automated" |

## 5. HÌNH v2 và thư viện (một lượt cho cả lô)
- Đạo cụ mới: `typecase` (khay chữ chì + tay cầm sắp chữ), `drawboard` (bàn vẽ nghiêng + đèn kẹp), `calculator` (cho tập 7), `dictionary` (cho tập 8). Khoá ERA: 1942, 1960, 1944, 1962.
- `render.js` ghi `zones` (Q-L20).
- `ll.py est` đo Q14–Q19 và Q21 trên timeline ước (duyệt G1 mục 6.8).
- Test thư viện: ĐẠT 23 mẫu, sau mỗi lần chạm thư viện.
- Mẫu dùng trong tập: `desk` (1942 → 1960 → 1988 → 2025, nhân vật vô danh khăn xanh), `archive` (2 ảnh LoC), `quote`, `sign`, `isotype`, `bars`, `street`, `text`, `endcard`.
- Thẻ giấy chiếm 15,8 %.

## 6. Token, ElevenLabs, giờ máy, đĩa
| Phần | Đầu vào mới + sinh ra | Nguồn số |
|---|---|---|
| P, tập 6 sản xuất (09:28 → viết báo cáo): ghi duyệt G1, đặc tả v2, `ll.py est`, thư viện, ảnh/RIGHTS, 7 lượt build, 3 lượt qc, phát hành, báo cáo | **≈ 0,23 triệu** (sinh ra 79 nghìn; đầu vào mới 148 nghìn; đọc lại cache 67,5 triệu) | log phiên (khử trùng theo mã tin nhắn) |
| **So với trần tập 1,5 triệu** | **≈ 15 %** | |

- **ElevenLabs:** bộ đếm 36 970 → **39 915** (+2 945 ký tự: lời phim và 3 Shorts; không thu lại).
- **Giờ máy:** khoảng 3,6 giờ build.
  - Gồm 1 lượt ASR dừng sớm, 2 lượt chồng nhau (bỏ), 1 lượt sạch (2 514 s), 3 lượt dựng lại đoạn đổi (2 194 / 1 722 / 1 742 s).
  - Thêm 3 lượt qc.
- **Đĩa:**
  - Trống 17 GB / hạn mức. Đỉnh trong tập khoảng 1,6 GB dùng cho trung gian và bản xem.
  - Trung gian `/var/tmp/cine-out/ll-ep06` (1,2 GB) giữ đến khi G2 duyệt.

## 7. Hàng chờ nhỏ (không chặn G2)
1. Luật làm việc của P: đo **hộp chữ giao hộp chữ** trong log render (lỗi #68). Hiện chỉ bắt được bằng cách rà khung tổng quan.
2. `verify.sh`: thêm một lần nhận dạng ASR thử (lỗi #66).
3. Q6 sát ngưỡng ở dòng nguồn Shorts (30,7 px): có thể rút nhãn `short9` của OOH 1990–91 thêm nếu cần.
4. Tập 7–8: viết `cap` cho mẫu `sign` ngay từ đầu (#68); nhãn `short` ≤ 30 ký tự cho nguồn đi cùng ảnh tư liệu.

## 8. Chờ chủ dự án — CỔNG G2 tập 6
1. **Duyệt bản cuối:** 3 phần bản xem trong `screening/` và master trên `release-ll-ep06-v1`.
2. **Thumbnail:**
   - T1 (chính): ảnh phòng sắp chữ New York Times 1942, chữ tiêu đề.
   - T2 (A/B): cảnh bàn làm việc 2025, chữ "GRAPHIC DESIGNERS: −1.7% PROJECTED, 2025–35 · BLS: AI 'REDUCE THE NEED'".
   - P đề xuất **T1 chính, A/B T2**.
3. **Shorts S1–S3** và text Shorts (`phat-hanh/ll-ep06-shorts-text.txt`).
4. Sau G2, P làm G3 không dừng: hướng dẫn đăng, Altered content = No, xoá trung gian. Sau đó P chuyển sang **tập 7**.
