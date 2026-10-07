# TẬP 2 — CỔNG G1: đề tài + kịch bản v1 · 04/10/2026

**P DỪNG ở G1, chờ chủ dự án duyệt đề tài, kịch bản và tiêu đề.**
- Đặc tả nhà máy (lời + shot + số + nguồn): `reports/m3/ep02/episode.yaml` (`ll.py check`: ĐẠT).
- Nguồn đọc toàn văn: `reports/m3/ep02/NGUON-TAP2.md`.

## 1. Đề tài
**"Hello, Central"**: nhân viên tổng đài điện thoại (1910–1940) ↔ nhân viên chăm sóc khách hàng hôm nay, trước AI.
- Lý do chọn: tập 2 trong thứ tự series đã đề xuất (1 → 2 → 3 → 6 → 4 → 5). Đây cũng là cặp mẫu "ĐÚNG" ghi sẵn trong luật so sánh (CHUAN-KENH §3.1).

**Kiểm so sánh tương xứng (6 điểm)**

| Điểm | Cặp trong phim | Kết quả |
|---|---|---|
| 1. Cùng cơ chế | Nối cuộc gọi bằng tay → tổng đài cơ khí; trả lời khách thường lệ → trợ lý AI. Một nhiệm vụ lặp lại của người do hệ thống tự động đảm nhận | Đạt |
| 2. Cùng thước đo | % thay đổi số người làm nghề trong 10 năm (đoạn 11); số người làm nghề (đoạn 08) | Đạt (`ll.py` chặn khác đơn vị) |
| 3. Cùng loại nguồn, địa lý | Mỹ cả hai vế: Census (qua Feigenbaum & Gross) ↔ BLS | Đạt |
| 4. Tách thực tế / dự báo | −16,1 % (đếm, ACTUAL, nét liền) ↔ −5,5 % (PROJECTION, gạch chéo nét đứt). Hai đợt dự báo 2023–33 và 2024–34 nằm ở hai khung riêng, có ghi đợt | Đạt (qc Q7) |
| 5. Phép tương tự kèm khác biệt | "Not the same technology. The same pattern…". Ba khác biệt: quy mô ~15×, AI vượt ra ngoài điện thoại, một bên là dự báo | Đạt |
| 6. Thang thời gian | Cả hai vế đều 10 năm (1930–40; 2024–34), ghi rõ trên hình | Đạt |

## 2. Ba phương án tiêu đề
- **A.** "Hello, Central: What Happened When Machines Took the Operators' Jobs"
- **B.** "The Dial Replaced 180,000 Operators. Customer Service Is Next?"
- **C.** "Automation Hurt the Operators — Not Their Daughters"
- **P đề xuất C**: dựa trên kết quả nghiên cứu, gây tò mò mà không doạ. B có dấu "?" và chạm vùng "your job is next" mà series dặn tránh. Nếu chọn B, cần sửa "180,000" thành "182,000" cho khớp hình (số đỉnh 1930).

## 3. Tóm tắt 5 dòng
1. Ở đầu phố, người thắp đèn thắp ngọn cuối; cuối phố, một tổng đài sáng trăm ngọn đèn nhỏ: "Hello, Central."
2. Lịch sử: tổng đài tự động có từ 1892, nhưng số nhân viên tổng đài vẫn tăng tới đỉnh 182 040 năm 1930, rồi giảm khi AT&T cơ giới hoá hơn nửa mạng lưới (1920–1940).
3. Feigenbaum & Gross: người đang làm chịu thiệt (ít hơn 8 điểm % khả năng còn làm tổng đài, việc mới lương thấp hơn); thế hệ sau thì không giảm việc làm chung.
4. Hôm nay: khoảng 2,8 triệu nhân viên chăm sóc khách hàng; BLS dự báo −5,5 % trong 2024–34 và nêu AI là một lý do. So cùng thang 10 năm: −16,1 % (đã xảy ra) với −5,5 % (dự báo).
5. Câu hỏi thật không chỉ là bao nhiêu việc làm, mà ai gánh chi phí. Kết: "Every era has its last lamplighters. Some of them answer the phone."

## 4. Số liệu chính và nguồn (đọc toàn văn)
| Số trên hình / lời | Loại | Nguồn | Trang |
|---|---|---|---|
| 73 030 (1910) · 134 630 (1920) · **182 040 (1930, đỉnh)** · 152 700 (1940) nhân viên tổng đài ngành điện thoại | thực tế | Feigenbaum & Gross, NBER w28061 (bản sửa 2/2024), Table II (dựng từ Census đếm đủ) | tr. 32; "peaked in 1930" tr. 13 |
| −16,1 % (1930–40) | thực tế, tính từ Table II | như trên | (152,70 − 182,04) / 182,04 |
| >½ mạng Mỹ cơ giới hoá 1920–40; Bell quay số 32 % (1930) → 60 % (1940) | thực tế | Feigenbaum & Gross | tóm tắt; tr. 7 |
| −8 điểm % còn làm tổng đài; −7 điểm % còn đi làm (>25 tuổi); đổi nghề +11 điểm %; điểm thu nhập nghề −5 % so với +8 % | ước lượng thống kê | Feigenbaum & Gross | tr. 19–20 |
| Thế hệ sau: tổng đài viên nữ 16–25 tuổi giảm 50–80 %, việc làm chung không giảm (trích nguyên văn) | ước lượng thống kê | Feigenbaum & Gross | tr. 1, 27; tóm tắt |
| 1892 La Porte; 1921 văn phòng Bell tự động hoàn toàn đầu tiên; 1965 Succasunna | mốc | Richmond Fed, *Econ Focus* Q4/2019, "Goodbye, Operator" | PDF tr. 1, 3 |
| 2 814 000 nhân viên CSKH (2024) → 2 660 300 (2034), **−5,5 %** | 2024: thực tế ước tính; 2034: dự báo | BLS, *Monthly Labor Review* 1/2026, Table 2 (bản FRASER) | tr. 7 |
| CSKH −5,0 %, phiên mã y khoa −4,7 % (2023–33); trích câu về GenAI | dự báo | BLS, *MLR* 2/2025 (bản FRASER) | mục Conclusion |

**Số cố ý KHÔNG dùng** (theo luật nguồn và ngoại lệ "nguồn không xác minh được"):
- 342 000 "giữa thế kỷ" (Richmond Fed không ghi năm, không ghi nguồn gốc).
- 178 000 năm 1920 của Richmond Fed: lệch với Table II, nên không ghép chung.
- Số BLS 2025–35 (OOH, Table 1.5): chỉ đọc qua WebFetch, chưa đối chiếu bảng gốc.
- Wikipedia: không dùng.

## 5. Kịch bản v1 (lời Bill; hình xem `episode.yaml`)
| Đoạn | Phần | Lời (tóm) | Hình chính |
|---|---|---|---|
| 00 | STORY | 6 s, không lời | phòng tổng đài, đèn giắc tắt dần → màn hình "AUTOMATED VOICE" |
| 01 | STORY | "At dusk, the last lamp on the street still waits for a hand… Hello, Central. Number, please." | phố đèn 2.5D, người thắp đèn vô danh → phòng tổng đài |
| 02 | HISTORY | người ở giữa cuộc gọi; 1892 La Porte; 1921 Bell; phần lớn cuộc gọi vẫn qua người | thẻ tựa "HELLO, CENTRAL" → thẻ mốc |
| 03 | HISTORY | đếm Census: 73 nghìn → 182 nghìn (đỉnh 1930) → 153 nghìn | đường vẽ dần, nhãn ACTUAL |
| 04 | HISTORY | AT&T cơ giới hoá >½ mạng; quay số 32 % → 60 %; đêm "cutover"; 1965 điện tử | cột · tổng đài tắt · thẻ 1965 |
| 05 | HISTORY | người đang làm: −8, −7 điểm %, đổi nghề, thu nhập nghề −5 % / +8 % | 2 thẻ số lớn · cột ± từ vạch 0 |
| 06 | HISTORY | thế hệ sau: 50–80 % ít tổng đài viên hơn, nhưng việc làm chung không giảm | thẻ số · trích dẫn |
| 07 | STORY | "The switchboards went dark long ago… someone, or something, still answers." | tổng đài tắt → giọng tự động |
| 08 | TODAY | ~2,8 triệu nhân viên CSKH (2024), khoảng 15 lần tổng đài viên năm 1930 | thẻ số · cột so quy mô |
| 09 | TODAY | dự báo 2024–34: −5,5 %, còn ~2,66 triệu; "a projection, not a count" | cột ACTUAL / PROJECTION |
| 10 | TODAY | BLS về GenAI (trích); đợt dự báo trước: CSKH −5,0 %, phiên mã y khoa −4,7 % | trích dẫn · cột dự báo đợt 2023–33 |
| 11 | TODAY | so cùng thang 10 năm: −16,1 % ↔ −5,5 %; "not the same technology — the same pattern"; 3 khác biệt | thẻ so sánh |
| 12 | TODAY | ai gánh chi phí; điều chưa biết: tốc độ, việc mới | thẻ chữ → văn phòng sáng đèn |
| 13 | STORY | "Every era has its last lamplighters. Some of them answer the phone." | người thắp đèn thắp ngọn cuối → thẻ kết "Next: The Typing Pool" |

**Shorts (3 bản, cùng nguồn):**
- S1 "Automation hurt the operators — not the next generation".
- S2 "How many U.S. customer service jobs could disappear?" (−5,5 %, có dòng "a projection, not a count").
- S3 "The night the switchboard went quiet" (cutover, 32 % → 60 %).

## 6. Thời lượng và tỷ lệ (ước, đọc 2,55 từ/s; đo thật sau khi thu lời)
- **≈ 5:50** (796 từ lời). **Dưới chuẩn kênh 8–11 phút.**
- Tỷ lệ STORY / HISTORY / TODAY ≈ **16 / 43 / 41 %**. Lệch quá ±5 điểm: **HISTORY +8 điểm**. TODAY −4,5 điểm, sát ngưỡng.
- Lý do ngắn: P chỉ dùng số đã đọc toàn văn. Phần TODAY thiếu số độc lập đã xác minh (ví dụ mức dùng chatbot trong CSKH, số BLS 2025–35 bảng gốc). P **không thêm phần tử chỉ để kéo dài** (luật cứng).

## 7. Ước token tập 2 (trần 1,2 triệu)
| Phần | Token |
|---|---|
| Tra nguồn (gói phụ Sonnet, harness) | 101 nghìn (thực) |
| P: chọn đề tài, kịch bản v1, `episode.yaml`, báo cáo G1 | ≈ 40 nghìn (ước) |
| Sau G1: thu lời (≈ 7 200 ký tự ElevenLabs), prep, render, sửa theo qc | ≈ 150 nghìn |
| Thử Sonnet ↔ Opus một đoạn đồ hoạ (2 gói) | ≈ 100 nghìn |
| G2: bản xem, thumbnail, gói phát hành, báo cáo | ≈ 80 nghìn |
| **Cộng ước** | **≈ 0,47 triệu**, tức 39 % trần, 22 % tập 1 |
| (+ phương án B ở mục 8, nếu chọn) | + 60–80 nghìn |

## 8. Chờ chủ dự án — CỔNG G1
1. **Duyệt đề tài** "Hello, Central" và kịch bản v1 (mục 5; lời đầy đủ trong `episode.yaml`).
2. **Chọn tiêu đề:** A / B / C. P đề xuất C.
3. **Quyết thời lượng** (lệch chuẩn 8–11 phút):
   - **(A) P đề xuất:** giữ ≈ 6 phút cho tập 2. Ưu: nhanh, ít token, mọi số đã xác minh. Nhược: dưới chuẩn kênh; HISTORY dư 8 điểm.
   - **(B)** Giao thêm một vòng tra nguồn (≈ 60–80 nghìn token) để bổ sung TODAY ≈ 2 phút: số dùng AI trong CSKH từ nguồn độc lập, và đối chiếu số BLS 2025–35 bằng trình duyệt. Ưu: đúng chuẩn và tỷ lệ. Nhược: chậm hơn một vòng; còn rủi ro không tìm được nguồn toàn văn.
4. **Người dẫn truyện:** cảnh truyện dùng người thắp đèn **vô danh** (bóng 2.5D của thư viện), không dùng Ida/Cas (tài sản `bible/` 3D, tốn 9–13 s/khung). Đây là khác biệt hình so với tập 1. Nếu cần quy ước "Ida thắp đèn mỗi tập", cần chủ dự án duyệt riêng.
5. Sau G1, P sản xuất theo chính sách 3 cổng và dừng ở G2.
