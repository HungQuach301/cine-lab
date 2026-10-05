# TẬP 3 — CỔNG G2: bản cuối · 05/10/2026

**P DỪNG ở G2, chờ chủ dự án duyệt bản cuối, Shorts và thumbnail.**
- Tiêu đề đã chốt ở G1: "The ATM Didn't Kill the Bank Teller. Will AI?". Không đổi.
- Dựng bằng nhà máy: một đặc tả `reports/m3/ep03/episode.yaml` (v2 sau G1 + sửa kiểm mù), một lệnh `scripts/ll/build.sh`, kiểm bằng `scripts/ll/qc.sh`.
- Mọi số dưới đây là số đo thật trên tệp.

## 1. Bàn giao
| Tệp | Thông số | Dung lượng | SHA-256 |
|---|---|---|---|
| Master (Git LFS, nhánh **`release-ll-ep03-v1`**): `ll-ep03-v1-master-1080p.mp4` | 1920×1080, 24 fps, H.264 crf 16, **9:04,50** (13 068 khung) | 477,6 MB | `be24268e3a28f22c54b157bcf8afd4a6bc8f64f2a31cb3ea0460fba49706df4e` |
| `screening/ll-ep03-v1-p1.mp4` | đoạn 00–04 (0:00–2:48,25), 720p | 61,7 MB | 842f2c15…21e9b79fb |
| `screening/ll-ep03-v1-p2.mp4` | đoạn 05–10 (2:48,25–6:09,25) | 73,8 MB | 5612d6bf…5fae52 |
| `screening/ll-ep03-v1-p3.mp4` | đoạn 11–14 (6:09,25–9:04,50) | 64,0 MB | c2422135…2b74b3e6d |
| Shorts S1/S2/S3 (LFS, cùng nhánh) | 1080×1920; 33,42 / 27,54 / 28,96 s | — | trong `SHA256SUMS.txt` của nhánh |
| Thumbnail T1, T2 (+ `.boxes.json`) · mô tả YouTube (15 chương) · text Shorts · phụ đề `.srt` | cùng nhánh và `reports/m3/ep03/phat-hanh/` | | |

- **Kiểm sau khi đẩy:**
  - tải ngược S3 từ link LFS công khai (media.githubusercontent.com): SHA khớp (`c638c740…`);
  - master trả `Content-Length` 477 628 377 byte, khớp tệp gốc.
- Ảnh khung tổng quan (29 shot): `reports/m3/ep03/khung-g2.jpg`.
- Bảng theo dõi khán giả (tự sinh): `reports/m3/ep03/KHAN-GIA.md`.

## 2. Kết quả `qc.sh` lượt cuối (bảng đầy đủ: `reports/m3/ep03/qc-g2.md`): **ĐẠT 26/26**
| Mục | Giá trị |
|---|---|
| Q1 judder · Q2 khung gần trùng · Q3 máy xuyên hình | 0 · 0 · 0 (18 tệp) |
| Q4 loudness / true peak | master **−14,1 LUFS / −1,6 dBTP**; phần −14,5 / −14,0 / −13,9; Shorts −14,1 / −14,1 / −14,0 |
| Q5 tương phản thấp nhất | 5,03:1 |
| Q6 cỡ chữ hoa tối thiểu | 30,7 px (Short S1, "ATM") |
| Q7 nhãn ACTUAL/PROJECTION · Q8 nguồn | 0 thiếu · 0 lỗi |
| Q9 số khung | 13 068 / 13 068 |
| Q10 dung lượng phần · Shorts | 61,7 / 73,8 / 64,0 MB · < 60 s |
| Q11 khung trống (bản dài) / chữ đứng (Shorts) | 0 |
| Q12 thumbnail lề 5 % | T1 ĐẠT, T2 ĐẠT |
| **Q13 (mới)** số trên tiêu đề, thumbnail, mô tả, Shorts truy về `numbers` + nhãn dự báo | 0 lỗi |

**Chỉ số trong ±5 % quanh ngưỡng:**
- cỡ chữ Short 30,7 px (ngưỡng 30, cách 2,3 %);
- HISTORY 30,1 % (sàn 30 %, xem mục 3).

**Lỗi qc bắt được trong lúc sản xuất (đã sửa trước khi giao):**
1. Q5: câu trích dài tràn khung 9:16 ở Short S3 (tương phản 1:1). Đã tách thành hai thẻ trích ngắn nguyên văn.
2. Q5: nhãn "ATM" trên màn hình phát sáng chỉ 4,15:1. Đã cho nền tối hơn, chữ đậm, quầng sáng nhẹ hơn.
3. Q11: lượt 1 có 8 quãng (1 ở bản dài, 7 ở Shorts), lượt 2 còn 2, lượt 3 còn 1. Lỗi cuối do mốc `@fewer` khớp nhầm lần xuất hiện đầu của từ. Đã sửa bằng `beats` gắn đúng lời.

## 3. Nội dung, tỷ lệ, kiểm mù
- **Thời lượng 9:04,5** (chuẩn 8–11 phút).
- **Tỷ lệ STORY / HISTORY / TODAY = 21,3 / 30,1 / 48,6 %.**
  - HISTORY −4,9 điểm, sát giới hạn ±5. TODAY +3,6 điểm.
  - Lời sửa sau kiểm mù làm TODAY dài thêm, nên P kéo dài cảnh mở/chuyển/kết thêm 14 s (đoạn 01, 06, 14). Đây là người thắp đèn đi và thắp đèn có chuyển động thật, không phải khung độn.
- **Kiểm mù (mục B8): 3 subagent Sonnet không có ngữ cảnh, đọc lời trước khi dựng lại.** Điểm có ≥ 2/3 cùng nêu đều đã sửa:

| Điểm (số subagent nêu) | Sửa |
|---|---|
| Đoạn 02 dày số, rối vì đổi phân loại (3/3) | Lời chỉ còn 65 nghìn (1950) → 253 nghìn (1970, "on a newer census basis"); thêm câu "That growth came before cash machines, in the long postwar boom". 135 nghìn chỉ còn trên biểu đồ, có ghi đổi phân loại |
| "Hopeful" ở đoạn 13 quá đà (3/3) | "The more hopeful kind… But that came with a condition. Cheaper branches meant more branches. That condition may not hold now." |
| Credit analysts −3,9 % lẫn với đợt 2025–35 (3/3) | Thêm câu "It belongs to a different projection cycle from the other numbers." |
| Đoạn 12: −13 % đọc như AI gây ra, so dự báo với lịch sử (3/3) | Thêm "For tellers, the BLS points to online banking and machines, not to AI alone." và "We set them side by side for the pattern, not for the arithmetic." |
| Đoạn 10 trừu tượng, "why banks are moving the scoring" như bằng chứng thay người (2/3) | Bỏ "2 % lợi nhuận"; câu kết: "It shows the scoring is getting better. It does not show what happens to the people who did it." |
| Kết "last lamplighters" ngụ ý nghề ngân hàng sắp mất (2/3) | "Some of them stood behind a bank window, **and many still do**." |
| 1950–70 là bùng nổ hậu chiến, không phải thời ATM (2/3) | như dòng đầu |

- **Đoạn 11 ("A banker's view"):** lời của chủ dự án, giữ nguyên văn. Hình là cảnh quầy giao dịch mới (`TPL.teller`): giao dịch viên ô giữa ngẩng lên, khách bồn chồn, bóng 2.5D, không cận mặt.
- **Kiểm so sánh:**
  - thẻ đoạn 12 cùng nguồn, cùng kỳ (BLS 2025–35, PROJECTION): tellers −13 % · loan officers +1 % · toàn nền +3,5 %;
  - chuỗi HSUS chỉ làm bối cảnh, hai đường hai phân loại;
  - credit analysts (2023–33) ở khung riêng có ghi đợt.

## 4. Bổ sung từ Crux (mục B5–B9), chạy tự động từ tập 3
| Mục | Kết quả |
|---|---|
| B5 ASR | `scripts/ll/asr.py` gắn vào `build.sh` trước `prep`: faster-whisper `small.en` nghe lại từng đoạn, so tên riêng và số theo **giá trị**; thiếu thì tự thu lại đúng đoạn đó (≤ 2 lần). Lượt cuối: 17/17 đoạn ĐẠT. **Lượt đầu báo sai** "Bessen" ở 4 đoạn (whisper viết "Besson") nên thu lại 2 lần thừa. Đã sửa: hotwords + so gần đúng ≥ 0,75; năm đọc bằng chữ được chấp nhận. Kiểm lại không tốn ký tự nào |
| B6 Bài học | `reports/m3/BAI-HOC-LL.md` (29 dòng, tập 1 → lô 3–5); CLAUDE.md dặn mọi phiên P đọc tệp này khi khởi động |
| B7 Q13 | thêm vào `qc.py`; thử ĐẠT trên tập 2 và tập 3 |
| B8 Kiểm mù | xem mục 3. **Vượt trần:** 3 × 47 nghìn = **141 nghìn so với trần 25 nghìn**. Nguyên nhân: mỗi subagent tốn ≈ 45 nghìn chi phí nền (lời nhắc hệ thống + công cụ), dù chỉ đọc một tệp 1 000 từ. Phương án ở mục 7 |
| B9 Khán giả | `scripts/ll/khan_gia.py` sinh `KHAN-GIA.md` khi ghép (đã gắn vào `build.sh`) |
| Trần dựng B5–B7, B9 (20 nghìn) | ≈ 15 nghìn (ước) |

## 5. Token, ElevenLabs, giờ máy, đĩa
| Phần | Token | Nguồn số |
|---|---|---|
| P: sửa G1, thư viện `teller`, 5 lượt build/qc, sửa qc, phát hành, báo cáo | ≈ 140 nghìn | ước |
| P: dựng B5–B7, B9 | ≈ 15 nghìn | ước |
| Kiểm mù (3 subagent Sonnet) | 141,2 nghìn | harness |
| **Tổng tập 3 (sản xuất)** | **≈ 0,30 triệu / trần 0,5 triệu (60 %)** | |

- **ElevenLabs:** gửi 7 088 ký tự (lượt đầu) + 6 916 (ASR: đoạn sửa theo kiểm mù + 8 lần thu thừa do báo sai "Bessen") = **14 004 ký tự**.
  - Bộ đếm tài khoản: 17 369 → 23 527 (+6 158), thấp hơn số đã gửi. Có thể bộ đếm cập nhật trễ; nhờ chủ dự án xem trên tài khoản.
  - Phần thừa do ASR báo sai khoảng 3 000 ký tự.
- **Giờ máy:**
  - 5 lượt build: 4 625 + 3 875 + (1 lượt dừng giữa chừng) + 5 161 + 344 s ≈ **4 giờ đồng hồ**, ≈ 8 giờ máy (4 vCPU).
  - Bài học: một lần sửa `lib/` làm render lại cả 16 đoạn (BAI-HOC #23).
- **Đĩa:** trống ≥ 16 GB suốt mốc. Trung gian giữ ở `/var/tmp/cine-out/ll-ep03` (2,5 GB) cho tới khi G2 duyệt.

## 6. Hàng chờ nhỏ (không chặn G2)
1. Đoạn 04: từ beat "cheaper to run" tới lúc cột 20/13 hiện là ≈ 8 s chỉ có tựa và dòng phụ. qc vẫn ĐẠT vì dòng phụ đổi theo lời.
2. Khách ở cảnh quầy (đoạn 11) hơi trong suốt do quầng viền. Bóng người vẫn đọc được.
3. Cảnh truyện dùng lại phố đèn của tập 2. Quầy giao dịch là cảnh mới duy nhất.

## 7. Chờ chủ dự án — CỔNG G2
1. **Duyệt bản cuối:** xem `screening/ll-ep03-v1-p1/p2/p3.mp4`. Master trên nhánh `release-ll-ep03-v1`, SHA `be24268e…49706df4e`.
2. **Duyệt 3 Shorts:**
   - S1 "The ATM didn't kill the bank teller";
   - S2 "Bank tellers: 13% fewer by 2035?";
   - S3 "AI and the essence of a credit rating".
3. **Chọn thumbnail:**
   - T1: cảnh quầy giao dịch + "THE ATM DIDN'T KILL THE BANK TELLER. WILL AI?";
   - T2: thẻ so sánh + "TELLERS −13% BY 2035 · BLS PROJECTION".
   - P đề xuất T1, thử A/B với T2.
4. **Kiểm mù vượt trần (141 / 25 nghìn), quyết cách chạy cho tập 4–5:**
   - **(A, P đề xuất)** 1 subagent đọc với 3 vai độc lập trong cùng một lượt: ≈ 48 nghìn/tập. Ưu: gần đúng trần, giữ được 3 góc nhìn. Nhược: 3 vai do cùng một mô hình trong cùng ngữ cảnh, kém độc lập.
   - (B) Giữ 3 subagent, nâng trần lên ≈ 145 nghìn/tập. Ưu: độc lập thật. Nhược: tốn gấp 3 lần.
   - (C) P tự đọc theo 3 câu hỏi, không dùng subagent: ≈ 5 nghìn/tập. Nhược: không "mù".
5. **Sau G2:**
   - P xoá trung gian, chuẩn bị G3 (hướng dẫn đăng theo khung tập 2);
   - P sang tập 4 theo chính sách 3 cổng, dừng ở G2.
