# CỔNG 2 — KỊCH BẢN · "Last Round" (bản nháp 1)

Phiên P, 27/09/2026. Nhánh `claude/cine-lab-m1-last-round-f1667s`.
Căn cứ: quyết định Cổng 1 của chủ dự án (P3 "Keep a Little Dark", câu tạm biệt số 2, Cas không lời, Ida Marrow 74 / Cas 10, giọng `59pjz3MTZdh9U1AETKfW`), đã ghi vào `AUTHORSHIP.md`.

| Sản phẩm | File |
|---|---|
| Kịch bản Fountain | `scripts/last-round.fountain` |
| Luật thế giới | `bible/world-rules.md` |
| Table read (nghe) | `reports/m1/cong2/tableread/last-round-tableread.mp3` (bản 24 bit: `.wav`) |
| Mốc câu thoại | `reports/m1/cong2/tableread/cue.json` |
| Kiểm J1 | `reports/m1/cong2/tableread/checks/` |

## 1. Beat sheet (6 cảnh, 2:45)

| # | Cảnh | Thời lượng | Giá trị đầu → cuối (A2) | Hành động chính | Cảm xúc người xem |
|---|---|---|---|---|---|
| 1 | The Round (0:00–0:30) | 30 s | Tối → sáng; yên ổn → bị đe doạ | Ida thắp đèn, hơ tay đếm ba, mồi đèn lồng, chào phố; gõ vào đồng hồ chậm. Xa xa có tiếng rơ-le | Êm, trìu mến; gợn lo ở tiếng "tách" cuối cảnh |
| 2 | Switch-on (0:30–0:55) | 25 s | Có bóng → mất bóng | Làn sóng đèn điện trắng lan xuống dốc, nuốt các vùng sáng hổ phách; Ida nhìn xuống: bóng mình biến mất | Hụt hẫng, mất mát lặng lẽ |
| 3 | The Race (0:55–1:25) | 30 s | Còn hy vọng → vô ích | Ida vội thắp tiếp; ngọn nào vừa sáng cũng bị phủ trắng; lần đầu trong 40 năm bà trễ; "Not yet… not yet." Kịp thắp ngọn thứ 11 cạnh tường | Căng, thương; nhịp nhanh dần |
| 4 | The Wall (1:25–1:55) | 30 s | Kỳ diệu → mất → kỳ diệu trở lại | Cas làm chim bóng dưới ngọn 11; cột điện cuối bật, chim nhạt dần rồi mất; Cas nhìn đèn lồng; Ida đưa đèn sát tường: "Go on, then." Chim bay lại, Cas cười khẽ | Đau nhói rồi ấm lên; **bước ngoặt**: Ida có người để trao lại |
| 5 | The Last Lamp (1:55–2:25) | 30 s | Níu giữ → buông tay (lựa chọn, A3) | Hai cái bóng duy nhất của thành phố trên tường trắng; Ida trèo lên ngọn khí cuối, nói lời tạm biệt, **tự tay tắt van**; trao đèn lồng; Cas hơ tay đếm ba | Cao trào lặng: nghẹn, rồi an |
| 6 | The Window (2:25–2:45) | 20 s | Mất → được tiếp nối (kết khép, ấm) | Toàn cảnh thành phố trắng, một ô cửa vàng; chim bóng lớn bay trên tường phòng Cas; Ida chỉnh đồng hồ nhanh thêm 7 phút rồi đi | Ấm, nhẹ, có hy vọng |

Gieo–gặt: hơ tay đếm ba (C1 → C5), chim bóng (C4 → C6), "old street" (C1 chào → C5 tạm biệt), đồng hồ chậm 7 phút (C1 → C6).

## 2. Toàn văn thoại (5 câu, chỉ Ida; Cas không lời)
| Mã | Cảnh · mốc | Câu | Thẻ diễn xuất gửi eleven_v3 |
|---|---|---|---|
| L1 | 1 · 0:10 | *Evening, old street.* | [softly] |
| L2 | 3 · 1:12 | *Not yet... not yet.* | [under her breath, strained] |
| L3 | 4 · 1:44 | *Go on, then.* | [gently] |
| L4 | 5 · 2:02 | *That's the last one, then. Goodnight, old street. You'll be brighter now. Just... keep a little dark for the ones who need it.* | [softly] [sighs] [voice breaking] [whispers] |
| L5 | 5 · 2:19,5 | *Warm your hands first. Three counts.* | [warmly, quietly] |

Âm thanh của Cas: tiếng thở và tiếng cười khẽ (C4), lấy từ SFX có giấy phép. Chưa chọn nguồn; mọi file SFX phải vào `RIGHTS.md` trước khi dùng.

## 3. Table read
- Giọng `59pjz3MTZdh9U1AETKfW`, eleven_v3, stability 0,5, seed 101, mỗi câu một take. Mỗi câu đặt đúng mốc trên nền im lặng dài 165 s. Tốn **259 ký tự** (25 754 → 26 013 / 55 779).
- Độ dài đo được: L1 2,16 s · L2 2,88 s · L3 2,30 s · **L4 14,08 s** · L5 3,20 s. Tổng thoại 24,6 s, tức **15% thời lượng phim**; 85% là hình và âm thanh.
- Chỗ đã sửa nhờ table read: L4 dài hơn khoảng trống mà kịch bản cho (mốc 2:04, hành động kế tiếp ở 2:12). Đã dời L4 về 2:02, trao đèn về 2:17, L5 về 2:19,5; Cas hơ tay 2:22–2:25. Mọi câu nằm gọn trong cảnh của nó.
- **J1 (faster-whisper small.en, luật khoá của phiên K): TRƯỢT**, từ bắt buộc 94,87%, WER 10,26%. Ba lỗi, đều do ASR và cách đo:
  1. "Goodnight" bị nghe thành "Good night";
  2. Whisper bịa chữ "you" trong đoạn im lặng tuyệt đối ở 30 s;
  3. "Warm" rơi ở ranh giới đoạn giải mã. Chạy ASR riêng trên câu L5 thì nghe đủ, p 0,84.

  Không sửa thoại hay audio để lách luật. Đã ghi 3 khiếu nại vào `checks-appeal.md` cho phiên K. Tai người vẫn cần xác nhận.
- Bản ghi ASR nguyên văn: *"Evening, Old Street · you · Not yet, not yet. · Go on then. · That's the last one then. Good night, old street. You'll be brighter now. Just keep a little dark for the ones who need it. · your hands first, three counts."*

## 4. Tự rà theo nhóm A, B (thẳng thắn)
| Mã | Đánh giá | Ghi chú |
|---|---|---|
| A1 Chủ đề 1 câu, mọi cảnh phục vụ | **Đạt** | Mỗi cảnh xoay quanh "bóng = dấu vết con người". Riêng mô-típ đồng hồ không phục vụ trực tiếp chủ đề (xem điểm yếu 3) |
| A2 Mỗi cảnh xoay một giá trị | **Đạt trên giấy** | Cảnh 2 và cảnh 3 xoay cùng một hướng (mất); cảnh 3 dễ bị thấy là lặp cảnh 2 |
| A3 Khởi đầu, bước ngoặt, cao trào có lựa chọn, kết | **Đạt nhưng yếu** | Khởi đầu: đèn điện bật (C2). Bước ngoặt: gặp Cas (C4). Cao trào: tự tắt ngọn cuối, trao lửa (C5). **Lựa chọn ít giá phải trả**: đằng nào đèn khí cũng mất, nên tắt van mang tính biểu tượng hơn là hy sinh |
| A4 ≥ 4/5 người xem mù tóm tắt đúng | **Chưa đo** | Đo ở Cổng 4 (animatic) |
| A5 Kết có dư âm | **Chưa đo** | Dự đoán: hình ô cửa vàng và chim bóng đủ mở ý nghĩa |
| B1 Không thoại giải thích điều hình đã cho thấy | **2 câu cần chủ dự án xét** | L5 "Warm your hands first. Three counts." là lời dặn, rồi hình lặp lại đúng hành động đó. L4 "You'll be brighter now" nói điều hình đã cho thấy (phố sáng hơn), nhưng mang nghĩa mỉa ngầm và là câu chủ dự án đã chốt |
| B2 Mỗi nhân vật có cách nói riêng | Không áp dụng | Chỉ một người nói |
| B3 Ẩn ý | **Đạt** | L4 nói với con phố nhưng thật ra là với chính bà và đứa trẻ; L2 "Not yet" là xin thêm thời gian cho cả đời nghề |
| B4 Table read trước khi dựng, ghi mọi chỗ sửa | **Đạt** | Table read + sửa mốc thời gian (mục 3) |

### Điểm yếu (chưa sửa, chờ chủ dự án chọn ở mục 5)
1. **Tiền đề "đèn điện không có bóng" là cường điệu.** Người xem có thể thấy vô lý nếu hình không dựng đúng luật thế giới: tấm sáng rộng, cột dày, sáng chồng nhiều hướng. Phải chứng minh ở style frame (Cổng 3). Đây là rủi ro số 1.
2. **Cao trào ít giá phải trả** (A3). Có thể tăng giá: Ida phải chọn giữa giữ đèn lồng cho mình đi nốt đường về và trao cho Cas.
3. **Đồng hồ chậm 7 phút khó đọc bằng hình.** "Lần đầu trễ" ở cảnh 3 không có chữ, không có lời, nên người xem có thể không hiểu. Chỉnh đồng hồ ở cảnh 6 chỉ có nghĩa nếu cảnh 1 cài đủ rõ.
4. **Cảnh 3 có nguy cơ lặp**: 30 s thắp rồi bị phủ trắng, lặp 3 lần.
5. **2:45 cộng credit ≈ 3:00**, chạm trần bài thử. Render ước 45,6 s/giây phim, khoảng 2,1 giờ mỗi lượt cả phim trên một máy.
6. **Cổng 1 chưa qua tiêu chí L3**: chưa đọc logline cho 3 người.

## 5. Điểm cần chủ dự án chọn
Xem câu trả lời chat (phương án A/B/C kèm khuyến nghị). Lựa chọn sẽ được ghi vào `AUTHORSHIP.md`, rồi P sửa kịch bản thành bản nháp 2.
