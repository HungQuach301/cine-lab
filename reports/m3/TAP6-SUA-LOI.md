# Tập 6 v2 — sửa 5 điểm lời sau G2 lần 2 (báo cáo ngắn, chờ Claude kiểm)

07/10/2026 · Phiên P · Nhánh `ccr-5219a838-ftr84s`.
Theo lệnh chủ dự án 07/10: tập 6 v2 phát hành theo luật hiện hành của P (không áp checks v3), không cần G2 lần 3.

## 1. Bản để kiểm
- **Bản xem 8:37:** `screening/ll-ep06-v2-p1.mp4`, `-p2`, `-p3` (60–66 MB mỗi phần).
- **Shorts:** `screening/ll-ep06-v2-short-S1..S3.mp4`.
- **Tờ khung:** `reports/m3/ep06/khung-g2-v2.jpg`.
- **Master 1080p:** `/var/tmp/cine-out/ll-ep06/ll-ep06-v2-master.mp4`, SHA-256 bắt đầu `ddabaec5a6e1f975`. Sẽ đưa lên `release-ll-ep06-v2` sau khi Claude xác nhận.

## 2. Trước / sau từng câu (đã đọc toàn văn các câu cần nguồn mới; ghi chép ở `ep06/NGUON-TAP6.md`)
| # | Đoạn | Trước | Sau | Nguồn |
|---|---|---|---|---|
| 1 | 00 | "…job posts for image work fell seventeen percent." | "…posts for image work fell seventeen percent, compared with manual jobs." | DHZ tr. 6, 19 (Bảng 4) |
| 2 | 05 | "In 1988, visual artists held about two hundred sixteen thousand jobs, and the BLS expected them to grow faster than average, though computers would limit that growth." | "In 1988, visual artists, a broad group from graphic designers and illustrators to painters and sculptors, held about two hundred sixteen thousand jobs. The BLS expected them to grow faster than average, though for graphic artists, computers would limit that growth." | OOH 1990–91 tr. 180–181. Bản cũ gán việc "computers limit growth" cho cả nhóm, nguồn chỉ nói graphic artists. Ý "thợ sắp chữ không chuyển sang thiết kế": Bessen toàn văn **không có**, nên bỏ theo lệnh |
| 3 | 07 | "They fell by nearly nine in ten… But for a brand-new technology like generative AI, the BLS changes its projections only when…" | "…That change was easy to see coming: the digital camera improved on a familiar tool, and its path was clear. The tools now reaching designers are different. For a brand-new technology like generative AI, the BLS changes its projections only when…" | MLR 2/2025 tr. 1 ("Digital cameras improved on an already-existing technology, and the path… was clear"; AI "harder to assess") |
| 4 | 04 | "The BLS expected little or no change in their numbers through the year 2000, despite a growing printing industry, because computers were taking over much of the typing." · "At newspapers, it was blunt: …" | "Across the whole printing industry, the BLS expected their numbers to stay about level through the year 2000: printing was growing, but computers were taking over much of the typing." · "At newspapers, the outlook was blunt: …" | OOH 1990–91 tr. 413 |
| 5 | 10 | "…and the designer took the tool. Today, software drafts the first image, and the designer is the one handed the tool again." | "…and designers began doing that work themselves, on screen. Today, software can draft the first image, and designers use it to reach a first draft much more quickly." | Bessen tr. 6; MLR 1/2026 |
| + | Short S1, mô tả, chữ Shorts | "Designers took the tool." | "…designers began doing it themselves, on computers." | cùng cách nói với điểm 5 (P sửa thêm cho thống nhất) |

- **Thu lại:** 5 đoạn lời phim và lời S1. ASR (faster-whisper small.en) 0/16 đoạn trượt; 100 % từ khoá.
- **Nhịp:**
  - Đoạn 00 đọc ở tốc độ 1,08 và rút đầu/cuối để tựa phim vẫn ≤ 0:20.
  - Đoạn 05 và 07 thêm chú thích gắn đúng lời mới để không quãng hình nào > 8 s.
  - Tập dài 8:37 (trước 8:14).

## 3. Sửa thêm trong lúc làm (lỗi thật, tìm bằng qc, xem mù, hoặc xem khung)
| Lỗi | Phát hiện | Sửa |
|---|---|---|
| Khoá YAML `off:` bị đọc thành boolean, nên mọi khung bắt đầu cảnh đinh bị bỏ qua lặng lẽ qua 4 lần dựng v2 | Xem khung điểm cắt 06→07 | Đặc tả dùng `frame0`; `ll.py` chặn khoá boolean (BAI-HOC #79). Kết quả: Q26 đạt hẳn |
| Người thắp đèn chìm vào mặt tiền tối, không thấy | Q31 vòng 2 (2/3) | Ngọn lửa mồi ở đầu sào; vào khung sớm ở đoạn 12 |
| Đoạn 07 nhảy khuôn so với 06; đầu đoạn 08 tối khoảng 2 s | Q31 vòng 2 (2/3) | 07 nối tiếp chuyển động máy; 08 mở bằng tường bản nháp sáng |
| Hai dòng nguồn chồng nhau thành bóng mờ | Q27 vòng 3 (3/3 chấm thấp F18) | Dải đặc che dòng nguồn cũ |
| Thẻ kết lặp tên kênh | Q31 vòng 3 (2/3) | "Episode 6 · The Hand That Drew It" |
| Dải đặc của chính P che mất ghi công ảnh tư liệu | Q5 (tương phản 1) | Vẽ dải trước ghi công |
| Chú thích chèn giữa dòng nuốt mã (lần 2 và 3 của #70) | Lỗi cú pháp; người thắp đèn đứng ở gốc toạ độ | `tests/comment_guard.py` + `node --check` trong `tests/run.sh` (BAI-HOC #76) |
| Công cụ Q28 bỏ sót 86 000 ("eighty-six" có gạch nối) | P soát lại | Sửa `cont.py`. **Đính chính G2 lần 2:** "86 000: 0,83 s" sai; số thật 0,77 s |

## 4. qc bản cuối (luật hiện hành của P; `checks/` = v3 1.7.1, LOCK KHỚP)
| Mục | Kết quả |
|---|---|
| qc.sh Q1–Q25 + LOCK | **ĐẠT toàn bộ** (38 dòng). Q16 nay đạt 6,9 %: bản khoá v3 nhận 5 mẫu toàn khung mới |
| Q26 (P) | **ĐẠT**: 78 khung nhìn (tập 1: 50); lớn nhất 4,7 % (tập 1: 21,1 %); cảnh liền cùng bố cục **2** (tập 1: 4) |
| Q28 (P) | **ĐẠT**: 4 cue không lặp; lặng trước số neo 0,77 / 0,78 / 0,58 / 0,76 s; −14,0 LUFS / −1,6 dBTP master; ASR 100 % |
| Q29 (P) | **ĐẠT** 55/55 |
| Q30 (P) | **ĐẠT** (cảnh đinh đúng tông: hồi 1 92 %, hồi 2 88 %, hồi 3 70 %, hồi 4 100 %) |
| Q27 (P, 3 vòng × 10 + 10 khung) | Vòng 1 +0,37 ĐẠT · vòng 2 +0,97 ĐẠT · vòng 3 **−0,43 TRƯỢT**. Gộp: v2 ≈ 5,35 vs tập 1 ≈ 5,05. Lỗi thật vòng 3 đã sửa (bóng chữ) |
| Q31 (P, 3 vòng) | 7/6/6,5 → 7/6/7 → 6,5/6,5/7. Mọi lỗi thật ≥ 2/3 đã sửa. Điểm ≥ 2/3 thuộc thiết kế (thẻ tựa giấy, bàn làm việc 2D, khung đôi, ảnh sepia) để lại cho tập 7 |

**Chỉ số trong ±5 % quanh ngưỡng (nêu tên):**
- Q5: tương phản chữ thấp nhất 4,6 (ngưỡng 4,5; dòng nguồn đoạn 09 f672).
- Q6: cỡ chữ 30,7 px (ngưỡng 30).
- Q14: tựa ở 19,7 s (ngưỡng 20).
- Q15: quãng không đổi hình dài nhất 7,8 s (ngưỡng 8).
- Q26: chuỗi cảnh cùng bố cục bằng 2, đúng ngưỡng ≤ 2.

Sổ chấm mù đủ 3 vòng ở `ep06/Q27-Q31.md`.

## 5. Checks v3
- `checks/ll-v3` (1.7.1, LOCK `e3fcd2e6…`) đã merge vào nhánh lô (`5e048cc`) và `main` (`f16b725`).
- `checks/lock.py --verify` **KHỚP** trên cả hai.
- `checks/` trùng hệt bản của K; P không sửa.
- `q31-lich-su/` nằm trong `<out>/blind/` của từng tập, tạo từ tập 7; P không xoá.

## 6. Token thật (đầu vào mới + sinh ra, log phiên)
- **Từ G2 lần 2 (07/10 05:22) tới nay:** phiên chính khoảng 4,17 triệu, subagent khoảng 0,85 triệu, tổng **khoảng 5,0 triệu**.
- **Cộng dồn từ lệnh dựng lại (06/10 09:28):** khoảng **9,0 triệu**.
- **Nguyên nhân chính:**
  - ngữ cảnh phiên rất dài, nên mỗi lượt ghi cache lớn;
  - 6 vòng dựng lại;
  - 12 subagent chấm mù;
  - các lỗi của P (#76, #79 và dải che ghi công) buộc dựng thêm.
- **Đề xuất cho tập 7:** mở phiên P mới (ngữ cảnh ngắn); kiểm giá trị tham số trong `timeline.json` trước mỗi lần dựng.

## 7. Đang chờ
- **Claude kiểm bản sửa này.** Sau khi Claude xác nhận, P tạo `release-ll-ep06-v2` (master, Shorts, bộ phát hành, SHA256, kiểm sau đẩy), rồi sang tập 7 theo checks v3.
