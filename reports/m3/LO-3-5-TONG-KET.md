# LÔ TẬP 3–5 — TỔNG KẾT · 06/10/2026

Ba tập đã qua G2 và có gói G3. Chủ dự án tự đăng.
- **Tập 3** "The Teller's Window": 9:04,5.
- **Tập 4** "The Typing Pool": 8:34,7.
- **Tập 5** "The Claims Desk": 8:32,5, dựng bằng HÌNH v2.
- Nguồn số: log phiên (trường `usage` của từng lượt gọi, đã khử trùng theo mã tin nhắn), log `build.sh`, git. Không dùng số ước.

## 1. Token thực (log phiên; các giai đoạn chồng việc thư viện chung)
| Giai đoạn (giờ UTC) | P: token sinh ra | P: đầu vào mới (input + ghi cache) | P: đọc lại cache | Subagent (đầu vào mới + sinh ra) |
|---|---|---|---|---|
| G1 lô: tra nguồn, 3 đặc tả (05/10 04:03–05:09) | @G1O@ | @G1N@ | @G1C@ | @G1S@ (tra nguồn Sonnet) |
| Tập 3 + nhà máy v1.1 (05:09–12:07) | @T3O@ | @T3N@ | @T3C@ | @T3S@ (kiểm mù tập 3 ×3 + tập 4 ×1) |
| Tập 4 + luật nhịp Q14–Q18 + HÌNH v2 (12:07–23:04) | @T4O@ | @T4N@ | @T4C@ | 0 |
| Tập 5 + Q20–Q22 (23:04 → hết) | @T5O@ | @T5N@ | @T5C@ | @T5S@ (kiểm mù tập 5) |
- **Các báo cáo G2 trước đây ước P ≈ 0,24–0,3 triệu token mỗi tập. Số đó chỉ gần với phần token sinh ra.** Theo đầu vào mới, mỗi tập 1,3–2,6 triệu. Đọc lại cache là 54–58 triệu mỗi tập, phần lớn do vòng lặp công cụ dài trên ngữ cảnh lớn.
- **Cần chủ dự án định nghĩa "trần token"** (sinh ra / đầu vào mới / tổng) cho các lô sau. P đề xuất: trần theo **đầu vào mới + sinh ra**, đo bằng log như bảng này.

## 2. Giờ máy, ElevenLabs, chạm của chủ dự án
| | Tập 3 | Tập 4 | Tập 5 |
|---|---|---|---|
| Lượt build (giây, đo bằng `build.sh`) | 4 625 + 3 875 + 5 161 + 344 + 1 lượt dở ≈ 4,0 giờ | 3 299 + 2 265 + 2 216 + 2 lượt dở ≈ 2,4 giờ | @T5B@ |
| ElevenLabs (ký tự gửi) | 14 004 (≈ 3 000 thừa do ASR báo sai tên) | 8 888 | 5 848, không thu lại |
- **Chủ dự án chạm 9 lần cho cả lô.**
  - 1 lệnh lô;
  - 3 lần quanh G1: trần token, duyệt G1, chấp nhận vượt trần tra bổ sung;
  - 1 lần cho các mục Crux B5–B9;
  - 1 lần "HẤP DẪN & GIỮ CHÂN";
  - 3 lần duyệt G2 (tập 3, 4, 5).
- **P dừng ngoại lệ 3 lần, đều vì vượt trần token:** tra nguồn lô, tra bổ sung, kiểm mù tập 3.

## 3. Số đo Q14–Q22 (cùng `rhythm.py` và qc; tập 3 đo lại trên timeline dựng lại từ giọng đã lưu, không gọi ElevenLabs)
| | Tập 3 (trước luật nhịp) | Tập 4 | Tập 5 |
|---|---|---|---|
| Q14 tựa phim / móc câu < 0:15 | 0:52 / không | 0:18,6 / có | 0:19,8 / có |
| Q15 quãng không đổi hình dài nhất / TB | 21,4 / 4,7 s | 8,0 / 3,0 s | 7,9 / 2,8 s |
| Q16 thẻ giấy | 75,0 % | 32,1 % | 15,5 % |
| Q17 mật độ số | 1,87/phút, chưa khai neo | 1,75/phút | 1,29/phút |
| Q18 thẻ trống > 1,5 s | 8 | 0 | 0 |
| Q19 tư liệu phạm vi công cộng | không dùng | không dùng | 84,5 s (16,5 %), 4 dòng RIGHTS |
| Q20 chữ đè hình | (chưa có luật) | (chưa có luật) | 0 |
| Q21 gán nguồn (mới) | 0 (không có chú thích đè) | không câu nào sai nguồn; 18 câu chưa khai, 7 câu không có dòng nguồn | sửa 1 câu sai + 10 câu chưa khai → 0 |
| Q22 chữ tràn khung (mới) | — | — | 16:9: 0. Shorts: 10 chỗ tràn → @Q22@ |
- Tập 3 trượt cả Q14–Q18 vì làm trước luật nhịp. Tập 4 và tập 5 đạt.
- Tập 4 đã đăng hoặc chờ đăng, P không sửa. Các câu thiếu dòng nguồn của tập 4 ghi ở đây để chủ dự án biết.

## 4. Bài học chính (chi tiết ở `BAI-HOC-LL.md` #42–57)
1. **Luật nhịp đo trên timeline chặn được lỗi trước khi render.** Thẻ giấy giảm từ 75 % xuống 15 % trong 3 tập mà lời phim không đổi.
2. **Qc chỉ bắt được những gì nó đo.**
   - Ba lỗi đến tay chủ dự án hoặc suýt lọt đều là loại chưa có luật: gán nguồn sai, chữ tràn khung, phụ đề đè isotype.
   - Mỗi lỗi giờ có một mục qc riêng (Q20, Q21, Q22) và test tự kiểm.
   - Rà khung tổng quan bằng mắt vẫn cần, nhất là cho Shorts 9:16.
3. **Shorts 9:16 cần thiết kế riêng, không thu nhỏ bản 16:9.** Toạ độ cố định theo 16:9 và nhãn nguồn dài đều tràn khung. Từ tập 6, thư viện tự thu cỡ chữ phủ trên khung; Q22 chặn phần còn tràn.
4. **Một subagent đóng 3 vai thay cho 3 subagent:** kiểm mù tốn ≈ 50 nghìn token thay vì 141 nghìn, chất lượng tương đương (tập 4–5).
5. **Đo token bằng log phiên, không ước** (mục 1).
6. **Sửa `lib/` làm render lại cả tập.** Gom các sửa thư viện vào đầu tập, sửa đặc tả khi có thể.

## 5. Chờ chủ dự án
1. Định nghĩa trần token cho lô sau (mục 1).
2. Lệnh lô tiếp theo (tập 6 trở đi: "The Hand That Drew It"). P dừng phiên này.
