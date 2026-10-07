# MỐC B — ĐÓNG GÓI NHÀ MÁY (B1–B3) · 04/10/2026

Nhánh `claude/modest-volta-7w7y40`, tạo từ `ccr-a27221d7-0iwsne` @f06a2a2 (tập 1 đã qua G2/G3).
- `scripts/env/verify.sh`: 10/11 PASS lúc mở phiên. Mục three.js thiếu `npm ci`; chạy xong thì 11/11.
- B1–B3 **không phải cổng**: P làm liền theo chính sách 3 cổng, rồi sang B4 và dừng ở G1 tập 2 (`reports/m3/TAP2-G1.md`).

## 1. B1 — Chính sách
- `CHUAN-KENH-LL.md` §7: ghi rõ chính sách 3 cổng áp cho mọi tập từ tập 2 và cho Mốc B.
- `CHUAN-KENH-LL.md` §8 mới, "Nguyên tắc tốc độ":
  - không cần quá hoàn hảo;
  - chỉ mở vòng sửa khi qc báo TRƯỢT mục chuẩn kênh hoặc khi lỗi làm sai nội dung;
  - lỗi nhỏ vào hàng chờ;
  - mỗi báo cáo ghi token thực so với trần.
- `PLAN.md` mục 17: trần token, các bước, báo cáo, cổng. AUTHORSHIP: 3 dòng mới ngày 04/10/2026.

## 2. B2 — Thư viện mẫu `scripts/ll/` (hướng dẫn: `scripts/ll/README.md`)
**Nguồn mã.** Mã đồ hoạ tập 1 chỉ còn ở dạng bản vá trong `reports/`. P áp 6 bản vá vào một worktree tạm, đọc rồi tổng quát hoá, không chép nguyên. Ngôn ngữ hình B3 giữ nguyên: giấy, ánh rọi, mực, màu, font DejaVu.

| Thành phần | Mẫu | Tham số chính |
|---|---|---|
| Đồ hoạ số (`lib/charts.js`) | `bars`, `line`, `compare`, `quote`, `bignum`, `text` | số lấy từ `numbers` (giá trị, chữ, ACTUAL/PROJECTION, nguồn); **trục luôn từ 0** (không có tham số tắt); cột âm mọc từ vạch 0; dự báo = gạch chéo + nét đứt + nhãn; dòng nguồn tự sinh |
| Bản đồ (`lib/map.js`) | `map` | `city: london / newyork` hoặc tự khai (sông, đảo, cầu kèm năm), `year`, máy, nhãn, ghim, đèn lan |
| Cảnh truyện 2.5D (`lib/scenes.js`) | `street` (phố đèn + người thắp đèn), `office`, `rows` (tổng đài / phòng đánh máy) | máy lia/đẩy có easing, 3–4 lớp parallax, sương theo độ sâu, quầng rung, hạt; bóng người không mặt, viền tách 2,75 px |
| Thẻ kết | `endcard` | dòng kênh, "Next: …"; Short tự gắn 1,5 s cuối |
| Khuôn Shorts 9:16 | mọi mẫu trên chạy khổ 1080×1920 | tấm giấy dọc, chữ ≥ 42 px, dòng hook trên đầu, vùng an toàn |
| Ghép đoạn (`lib/shot.js`) | chuyển `slide` / `flip` (lật giấy) / `fade` / `cut` | |

**Một tệp đặc tả, một lệnh.** `bash scripts/ll/build.sh <episode.yaml>` chạy:
1. `ll.py`:
   - kiểm đặc tả;
   - thu lời Bill qua ElevenLabs, có cache theo băm văn bản;
   - giải mốc `"@từ"` để hình không đi trước lời;
   - ghi `timeline.json`, phụ đề `.srt` và cue SFX tự sinh.
2. Render song song, chỉ đoạn có đặc tả đổi.
3. `mix.py`: −14 LUFS / ≤ −1 dBTP.
4. Master crf 16 và 3 phần 720p, cắt ở ranh giới đoạn gần 1/3 và 2/3.
5. Shorts.

**Việc tồn tập 1 đã sửa trong mẫu**

| Việc tồn | Cách sửa | Kiểm |
|---|---|---|
| Cỡ chữ tối thiểu ở mọi trạng thái (đoạn 09 lúc bảng thu nhỏ) | `text()` đọc ma trận biến đổi hiện hành, tự nâng cỡ khi hiệu dụng < 26 px (16:9) / 42 px (9:16) | qc Q6 đo trên khung mẫu. Demo: thấp nhất 19 px chữ hoa (16:9) và 30,7 px (9:16) |
| Phố vắt qua sông (bản đồ 02) | mạng phố không bao giờ đi vào nước; chỉ vẽ cầu có năm xây ≤ năm bản đồ (London 1807: London Bridge, Westminster, Blackfriars, Battersea) | xem khung `reports/m3/moc-b/demo-16x9.jpg` |
| Shorts không SFX, chữ đứng lâu | cue lật/trượt giấy tự sinh ở mỗi chuyển thẻ, đèn khí xì khi đèn bừng; qc Q11 bắt chữ đứng > 3 s khi có lời | demo S1: 1 cue SFX, Q11 đạt |

**SFX:** 3 tệp CC0 đã có trong `RIGHTS.md` (M2-SFX-1/2/3), tải lại vào `assets/ll/sfx/` (0,9 MB). Không có tài sản mới.

**Tốc độ render đo thật:** 0,10–0,26 s/khung (đồ hoạ 0,10; cảnh 2.5D ≈ 0,25 khi chạy 5 tiến trình), nhanh hơn tập 1 (đồ hoạ 0,5–0,9; cảnh 3D 3,5–13,5). Tập 10 phút ≈ 14 400 khung, ước ≈ 0,5–1 giờ máy.
- Lý do: khung chuyển ra bằng JPEG chất lượng 0,96 thay cho RGBA thô qua base64.
- Đánh đổi: thêm một bước nén có mất mát trước trung gian crf 10, không thấy bằng mắt.

**Demo trọn một lệnh** (`scripts/ll/examples/demo.yaml`, dùng mọi mẫu, không lời, 48 s + 1 Short 14 s): 355 s đồng hồ cho render, mix, ghép và Short; qc ĐẠT cả 18 dòng (`reports/m3/moc-b/qc-demo.md`). Ảnh khung: `reports/m3/moc-b/demo-16x9.jpg` (bản trước khi sửa mật độ phố và tay bóng người) và `demo-9x16.jpg`.

**Điểm yếu đã biết (hàng chờ, không chặn):**
1. Cảnh 2.5D đơn giản hơn cảnh three.js tập 1: nhà khối, bóng người hình học. Tập nhà máy sẽ nhìn khác tập 1 ở phần STORY.
2. Mạng phố bản đồ là thủ tục giản lược, chưa giống bố cục phố thật; chỉ có preset London và New York (Paris chưa đóng gói).
3. Tay bóng người ở cảnh `rows` còn cứng.
4. Thẻ `compare` khổ dọc còn nhiều khoảng trống.

## 3. B3 — Bộ kiểm `scripts/ll/qc.sh` (một lệnh, bảng ĐẠT/TRƯỢT ra `<out>/qc.md`)
| Mục | Kiểm | Cách đo |
|---|---|---|
| Q1 | Judder | `scripts/p/judder.py` (framemd5), đoạn giữ 2–12 khung = 0, trên trung gian từng đoạn/Short |
| Q2 | Khung gần trùng | chênh xám TB ≤ 0,1 (192×108) kẹp giữa chuyển động rõ (trung vị 6 khung hai bên > 0,5) |
| Q3 | Máy xuyên hình học | (a) mẫu 2.5D ghi khoảng cách máy–lớp gần mỗi khung, ≤ 0,05 là lỗi; (b) khung > 85 % ô 16×16 phẳng ngoài vùng mờ (heuristic, trừ thẻ kết) |
| Q4 | Loudness / true peak | ebur128: master và Shorts −14 ± 1 LUFS, TP ≤ −1; 3 phần bản xem ±2 LU (đối chiếu) |
| Q5 | Tương phản | **đo trên điểm ảnh thật** mỗi 12 khung: nền = trung vị viền hộp chữ, chữ = phân vị 5 % (95 % với chữ sáng); ≥ 4,5:1 |
| Q6 | Cỡ chữ tối thiểu | cỡ chữ hoa hiệu dụng (qua mọi phép thu phóng) ≥ 18 px (16:9) / 30 px (9:16) |
| Q7 | Nhãn ACTUAL/PROJECTION | shot có số dự báo phải hiện chữ PROJECTION; có số thực tế phải hiện ACTUAL |
| Q8 | Nguồn | đọc toàn văn; URL không phải Wikipedia/Wikimedia; số dự báo có `period`; số trên hình có cụm đọc trong lời |
| Q9 | Số khung | trung gian = timeline, master = tổng khung |
| Q10 | Kích thước | mỗi phần bản xem ≤ 90 MB; Short ≤ 60 s |
| Q11 | Chữ đứng | > 3 s liền không có nội dung mới trong khi lời đang nói (cảnh truyện toàn khung miễn) |

- Mục nào sát ngưỡng ±5 % được ghi tên tự động ở cột "Sát ngưỡng".
- **Hiệu chỉnh trên demo, đều có số đo:**
  - Q2 tol 0,5 báo nhầm, vì giấy lay rất nhẹ (chênh nhỏ nhất đo được 0,15) → hạ tol về 0,1 và thêm điều kiện "kẹp giữa chuyển động".
  - Q5 ban đầu tính màu chữ theo màu khai báo, sai dưới ánh rọi → đo màu chữ trên điểm ảnh. Bốn nhãn ở góc tối dưới 4,5:1 → INK2 đậm hơn (#382d25), nhãn trục và năm bản đồ đổi sang mực đậm.
  - Âm phần p3 bị đỉnh +3,1 dBTP do cắt đột ngột rồi mã hoá AAC → thêm fade 30/60 ms ở mép phần (đo lại −2,5 dBTP).
  - Q3 khung phẳng báo nhầm ở thẻ kết và cảnh tổng đài khổ dọc → trừ thẻ kết, nâng ngưỡng 70 → 85 %.
- **Sát ngưỡng trên demo:**
  - tương phản thấp nhất 4,57:1 (nhãn "0", cách ngưỡng 1,6 %);
  - chữ hoa Short 30,7 px (cách ngưỡng 30 px 2,3 %).
- **Gửi K:** `checks-appeal.md` mục 8, đề nghị K xét khoá Q1–Q11, xác nhận cách đo Q5, chọn ngưỡng hoặc bỏ heuristic Q3b. P không sửa và không đọc `checks/`.

## 4. Token (trần: B2 400 nghìn, B3 150 nghìn)
| Phần | Token | So trần |
|---|---|---|
| B1 | ≈ 10 nghìn | — |
| B2 thư viện + build + demo | ≈ 190 nghìn | 48 % |
| B3 qc + hiệu chỉnh + gửi K | ≈ 55 nghìn | 37 % |
| **Cộng B1–B3** | **≈ 0,25 triệu** | 46 % của 550 nghìn |

- Nguồn số: bộ đếm ngữ cảnh của phiên P (tổng dùng tới lúc dừng G1 ≈ 0,30 triệu, gồm cả phần G1 tập 2 ≈ 40 nghìn). Chia theo bước là ước.
- Gói phụ tra nguồn tập 2 (Sonnet): 101 nghìn, số harness, tính vào tập 2.
- ElevenLabs: bộ đếm 8 503/144 034 lúc mở phiên. Phiên này **chưa gửi ký tự nào**; lời tập 2 thu sau G1.
- Chênh 382 ký tự so với cuối M2.3 (8 121) không do phiên này gửi.

## 5. Đĩa
- Trống 17,5 GB sau demo. Demo chiếm 284 MB ở `/var/tmp/cine-out/ll-demo` (ngoài git).
- Worktree tạm đọc mã tập 1 nằm ở scratchpad và đã gỡ.

## 6. Chờ chủ dự án
- **Không có cổng ở B1–B3.** Việc đang chờ là **G1 tập 2** (`reports/m3/TAP2-G1.md` §8).
- K: phán quyết mục 8 (và mục 1–7 còn treo) trong `checks-appeal.md`.
