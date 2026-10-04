# Gói phát hành nháp · Last Lamplighters · Tập 1 (P, 04/10/2026)

Trạng thái: **nháp chờ cổng G2.** Chủ dự án chọn tiêu đề và thumbnail; cổng G3 là bấm phát hành.
Mốc chapter theo timeline v4 (có đoạn móc 6 s). Sẽ kiểm lại trên master M2.3.

## 1. Tiêu đề (3 phương án, ≤ 70 ký tự)
| # | Tiêu đề | Ký tự | Hợp thumbnail | Ghi chú |
|---|---|---|---|---|
| A | **The Last Lamplighters: Which Jobs Are Next?** | 43 | T1 | Câu hỏi kênh; an toàn, không hứa quá nội dung |
| B | **The Jobs America Expects to Shrink Fastest (and the Lamplighters Who Came First)** | 81 → rút: "Jobs Shrinking Fastest by 2035, and the Last Lamplighters" (56) | T2 | Mạnh về tìm kiếm; số −34 % nằm trên thumbnail, không nằm trong tiêu đề |
| C | **London Still Has 5 Lamplighters. Who Are the Last of Our Time?** | 62 | T3 | Tò mò mạnh nhất. Số 5 = đội British Gas năm 2023 [8], phần mô tả ghi rõ |

**P đề xuất C + T3 cho bản chính.** Lý do: chi tiết lạ, đúng sự thật, dẫn thẳng vào câu hỏi của kênh. A dùng làm phương án dự phòng cho thử A/B.

## 2. Thumbnail (1280×720, `reports/m3/m2-3/thumb/`)
Cùng hệ nhận diện: chàm đêm và giấy ngà, chữ hổ phách DejaVu Serif Bold, dấu kênh (cột đèn và chữ "LAST LAMPLIGHTERS") ở góc dưới trái. Mã: `scripts/p/thumb_ep01.py`.
- **T1 `T1-den-bung.jpg`:** Ida trên thang, đèn số một bừng (đoạn 01). "THE LAST LAMPLIGHTERS · Which jobs are next?"
- **T2 `T2-tru-34.jpg`:** lưới cửa sổ văn phòng trên phố đèn khí (khối 10–13). "−34% · word processors & typists, 2025–35 · U.S. BLS projection"
- **T3 `T3-con-5.jpg`:** Covent Garden hôm nay (đoạn 07). "5 lamplighters · in London, 2023 · Who are the last of our time?"
- Mọi số trên thumbnail đều có trong phim kèm nguồn; không có số mới.

## 3. Mô tả (tiếng Anh, dán vào YouTube)
```
For more than a century, someone walked out at dusk with a ladder and a long pole and gave the street its night. Then the lamps learned to light themselves.

This film follows one job from Pall Mall in 1807 to London's last team of lamplighters today, then asks the same question about the jobs the U.S. Bureau of Labor Statistics expects to shrink fastest by 2035.

Ida and Ostler Street are fictional. Every number on screen comes from the sources listed below.

Chapters
0:00 Cold open
0:06 Ostler Street
0:47 Pall Mall, 1807
1:19 The round
1:45 "Not yet… not yet."
2:01 The white wave: Paris, 1878
2:26 New York, April 1907
2:53 London's last lamplighters
3:26 From lamps to lifts: one job in 270
4:13 The office of 1970
4:41 Today's shortest rounds
6:15 The same clock
7:17 Why these jobs
7:39 Jobs that change
8:27 An early signal
9:00 Not verdicts
9:23 Ida lights a lamp

Sources
- London Remembers, "First gas-lit street in the world"
- English Heritage, "The illuminating history of lighting"
- NPR, "Carrying the Torch for London's Last Gas Lamps" (15 Jan 2015)
- British Gas, The Source, "Celebrating the coronation of King Charles III" (2023)
- ETHW, "Jablochkoff Candles in Paris"
- The Sun (New York), 25 Apr 1907, p. 1; New-York Tribune, 29 Apr 1907, p. 4; The Evening World, 30 Apr 1907, p. 4 (Library of Congress, Chronicling America)
- U.S. Bureau of the Census (1975), Historical Statistics of the United States, Colonial Times to 1970, Part 1, Series D 233–682, pp. 140–145
- J. Bessen (2016), "How Computer Automation Affects Occupations", NBER Summer Institute
- U.S. Bureau of Labor Statistics, Employment Projections 2025–2035, Table 1.5, and news release USDL-26-1422 (27 Aug 2026)
- Machovec, Rieley & Rolen, "Incorporating AI impacts in BLS employment projections", Monthly Labor Review, Feb 2025
- Stanford Digital Economy Lab (12 Aug 2026), "No Widespread Displacement, but the AI Employment Gap for Young Workers Has Widened to 19%"
Projections are forecasts, not verdicts. The Stanford finding is an early signal, not proof that AI caused it.

Music
"Immersed" and "Reawakening" by Kevin MacLeod (incompetech.com)
Licensed under Creative Commons: By Attribution 4.0 License
http://creativecommons.org/licenses/by/4.0/

How this film was made
Written, animated and edited with AI tools (Claude by Anthropic) under the direction of the channel's human author, who approved every creative decision. Narration is a synthetic voice (ElevenLabs library voice, not a real person). Animation is stylised and not intended to depict real footage.
```
- **Ghi công Kevin MacLeod:** câu chuẩn theo RIGHTS M3-MUS-1/2. **Bắt buộc**, không được bỏ.
- **Mục nguồn:** bỏ Wikipedia (CHUAN-KENH §7). Không còn nguồn cho "1820s · 40 000 đèn" vì phim đã bỏ số này (M2.2 mục 3.5).

## 4. Tiết lộ dùng AI
- Chính sách YouTube hiện hành ("Disclosing use of altered or synthetic content", đọc 04/10/2026, support.google.com/youtube/answer/14328491):
  - **bắt buộc** bật "AI use" trong Studio khi nội dung tạo hoặc sửa bằng AI trông **như thật** (người thật nói hay làm điều họ không làm, sửa cảnh thật, cảnh như thật chưa từng xảy ra, nhạc AI là trọng tâm);
  - **không bắt buộc** với nội dung rõ ràng không thật hoặc hoạt hình, và với hỗ trợ sản xuất (kịch bản, thumbnail, tiêu đề, infographic).
- **Đánh giá P:** phim là hoạt hình phong cách hoá, giọng kể là giọng thư viện không nhái người thật, nhạc do người sáng tác. Theo câu chữ chính sách thì **không bắt buộc** bật nhãn.
- **Đề xuất:** vẫn ghi đoạn "How this film was made" trong mô tả (tự nguyện, minh bạch cho khán giả và người mua phim). Chủ dự án quyết ở G3 có bật thêm nhãn "AI use" hay không. Bật nhãn không ảnh hưởng doanh thu theo chính sách.
- **Rủi ro:** chính sách có thể đổi. Kiểm lại trang này ngay trước khi bấm phát hành.

## 5. Việc còn lại trước G3
- Mốc chapter: kiểm trên master M2.3.
- Phụ đề tiếng Anh (`.srt`): sinh từ align, rà tay.
- Đọc lại mô tả trên điện thoại.
