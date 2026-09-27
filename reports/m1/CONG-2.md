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

---

# NHÁP 2 (27/09/2026, sau quyết định Cổng 2 của chủ dự án)

Quyết định (đã ghi vào `AUTHORSHIP.md`): 1C, 2B, 3B, 5A, 6B theo khuyến nghị; **4A khác khuyến nghị** (giữ cả 3 nhịp đồng hồ); sửa quang học cảnh 5 và 6; luật thế giới lên v0.2; 3 khiếu nại J1 được chấp nhận.

## Beat sheet nháp 2 (6 cảnh, **2:30**)
| # | Cảnh | Thời lượng | Giá trị (A2) | Hành động chính |
|---|---|---|---|---|
| 1 | The Round (0:00–0:26) | 26 s | Tối → sáng; yên ổn → bị đe doạ | Toàn cảnh cao lúc chạng vạng, đèn khí thành những tâm hổ phách; Ida thắp đèn, hơ tay đếm ba, mồi đèn lồng, "Evening, old street."; gõ vào kính đồng hồ bỏ túi; tiếng rơ-le |
| 2 | Switch-on (0:26–0:44) | 18 s | Có bóng → mất bóng | Đồng hồ điện quảng trường sáng đầu tiên, chuông "ding"; làn sóng trắng lan xuống dốc; bóng Ida biến mất |
| 3 | The Race (0:44–1:08) | 24 s | Tin mình kịp → biết mình trễ → vô ích | So đồng hồ bỏ túi với đồng hồ điện: hai kim nằm hai bên số 12, lệch 7 phút; Ida vội thắp 8, 9, 10 ("Not yet… not yet."); kịp thắp ngọn 11 và hơ tay đếm ba, Cas nhìn thấy |
| 4 | The Wall (1:08–1:34) | 26 s | Kỳ diệu → mất → trở lại | Chim bóng tan khi cột điện cuối bật; Cas nhìn đèn lồng; Ida cầm đèn thấp sau tay cậu: "Go on, then."; chim to hơn, ấm hơn bay lại |
| 5 | The Last Lamp (1:34–2:10) | 36 s | Níu giữ → buông tay (lựa chọn) | Trong hốc cửa khuất điện, hai bóng người trên vách vôi; Ida trèo lên ngọn khí cuối, nói lời tạm biệt, tắt van; trao đèn lồng; **Cas tự hơ tay đếm ba** |
| 6 | The Window (2:10–2:30) | 20 s | Mất → tiếp nối; chống cự → chấp nhận | Toàn cảnh trắng, một ô vàng; trong ngõ khuất, bóng mờ của Ida trở lại; bà chỉnh đồng hồ tiến 7 phút cho khớp giờ quảng trường rồi đi; kết: chim bóng lớn bay trên tường phòng Cas |

## Thoại nháp 2 (4 câu, chỉ Ida)
| Mã | Mốc | Câu |
|---|---|---|
| L1 | 0:12 | *Evening, old street.* |
| L2 | 1:00 | *Not yet... not yet.* |
| L3 | 1:28 | *Go on, then.* |
| L4 | 1:50 | *That's the last one, then. Goodnight, old street. You'll be brighter now. Just... keep a little dark for the ones who need it.* |

## Table read nháp 2
- `reports/m1/cong2/tableread-d2/last-round-tableread-d2.mp3`, 2:30. Câu thoại ở 0:12 · 1:00 · 1:28 · 1:50. Tổng thoại 21,4 s = 14% phim.
- Take L1–L4 dùng lại từ nháp 1 (câu chữ không đổi, cùng giọng `59pjz3MTZdh9U1AETKfW`), nên **0 ký tự** mới. Mọi câu nằm gọn trong cảnh; L4 kết thúc ở 2:04,08, trùng lúc vặn van (2:04).
- **J1: TRƯỢT** (từ bắt buộc 96,97%, WER 15,15%; 33 từ: 1 thay, 0 mất, 4 chèn). Nguyên nhân đúng như 2 khiếu nại đã được chấp nhận: "Goodnight" → "Good night"; Whisper bịa "Thank you" (14,1 s) và "You" (134,1 s) trong im lặng tuyệt đối. **Không có từ thoại nào bị mất.** Chờ phiên K sửa luật rồi chạy lại. Báo cáo: `tableread-d2/checks/`.

## Tự rà nhóm A, B (nháp 2)
| Mã | Đánh giá | Ghi chú |
|---|---|---|
| A1 | Đạt | Mô-típ đồng hồ giờ gắn với chủ đề: "giờ mới" = tiến bộ; chỉnh giờ = chấp nhận |
| A2 | Đạt | Cảnh 3 giờ xoay thêm một giá trị riêng (tin mình kịp → biết mình trễ), bớt lặp với cảnh 2 |
| A3 | Đạt | Lựa chọn ở cảnh 5 (tắt van, trao lửa); giá phải trả giữ nguyên theo 5A |
| A4, A5 | Chưa đo | Cổng 4 |
| B1 | Đạt; 1 câu cần lưu ý | Đã bỏ L5. L4 "You'll be brighter now" vẫn nói điều hình đã cho thấy, nhưng là câu chủ dự án chốt và mang nghĩa mỉa ngầm |
| B3 | Đạt | L2 và L4 có ẩn ý |
| B4 | Đạt | Table read nháp 1 và 2; mọi chỗ sửa đều ghi lại |

## Rà quang học theo luật thế giới v0.2: mọi chỗ còn mâu thuẫn
Đã sửa ngay trong nháp 2 (lỗi P tự phát hiện):
1. Cảnh 4: chim bóng dưới đèn lồng ghi "small" → sửa thành **to hơn, mềm hơn** (tay ở giữa, đèn rất gần). Luật v0.1 cũng sai chỗ này, đã sửa ở v0.2 mục 3.2–3.3.
2. Luật v0.1 điều kiện 3 ("tay gần tường hơn nguồn") chặn luôn chim bóng lớn ở cảnh kết (2B) → bỏ điều kiện này, thay bằng hình học phóng đại (mục 3.2).
3. Cảnh 3: đồng hồ quảng trường "đứng đúng giờ" lúc đã trôi qua vài phút truyện → sửa thành hai kim nằm hai bên số 12.

**Còn mở, cần chủ dự án chọn:**
4. **Cảnh 5, sửa (a):** đèn lồng cách tường ~3 m không thể đạt 4 : 1 trên một bức tường đang bị đèn điện rọi (mục 3.4). Nháp 2 tạm đặt cảnh vào **hốc cửa bốc hàng khuất điện** → điểm chọn 7.
5. **Cảnh 1, bóng lúc chạng vạng:** trời còn sáng thì ánh trời tràn làm bóng từ đèn khí yếu, chưa đạt 4 : 1. Kịch bản ghi "shadow falls long and soft" ngay từ 0:04 → điểm chọn 10.
6. **Cảnh 6, phơi sáng trong ngõ:** muốn đạt 4 : 1 từ ánh cửa sổ tầng một, ngõ phải gần như tối đen, nên Ida cũng gần như không nhìn thấy. Đây là việc của ánh sáng ở Cổng 3/7 (rim nhẹ từ miệng ngõ, giữ tỷ lệ tại nền). Ghi lại, chưa cần chọn.
7. **Bố cục cảnh 6:** cửa sổ nhà Cas trông ra ngõ, nhưng toàn cảnh cao phải thấy được ô cửa đó. Việc của layout ở Cổng 5; ghi lại.

Không còn chỗ nào trong nháp 2 có bóng hiện dưới ánh điện tràn.
