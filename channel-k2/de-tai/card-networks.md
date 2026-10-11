# Hồ sơ cầu: "How Visa and Mastercard Make Money Without Lending a Cent" (T3 tài chính–thanh toán, hàng đợi #3)

> Dữ liệu thu ngày 11/10/2026 (`collect.py demand`, `report.py card-networks`; bổ sung `collect.py durable`). Mọi chỉ số là **tự tính, không phải chỉ số YouTube**.
> Bình luận thô nằm ngoài git và tự xoá sau 30 ngày. Hồ sơ chỉ chứa ý tóm tắt do Haiku diễn đạt lại, không có tên người bình luận. **Trọng số** = 1 + số like + số phản hồi.
> **Đề tài tài chính–thanh toán:** chỉ giải thích cơ chế, không lời khuyên (`LUAT-NOI-DUNG.md` §5).

## 1. Cách đo
- **3 câu hỏi khán giả:**
  - "how do visa and mastercard make money"
  - "what happens when you swipe a credit card"
  - "who pays credit card swipe fees"
- **Lấy mẫu:** search.list toàn thời gian, theo độ liên quan, `regionCode=US`, 15 kết quả; giữ 5 video ≥ 8 phút đầu tiên.
  - Câu 2 chỉ có 2 video dài.
  - **Câu 3 không có video dài nào** trong 15 kết quả: toàn Shorts. Đây là dấu hiệu khoảng trống ở dạng dài, nhưng cũng có thể cho thấy khán giả muốn câu trả lời ngắn.
- **Kết quả mẫu:** 7 video duy nhất. **84 bình luận**, gắn nhãn 84/84. Bốn video năm 2026 hầu như không có bình luận.
- **Phân loại:**

| Câu hỏi | Hoàn cảnh cá nhân | Phản bác/chỉnh sai | Yêu cầu | Bỏ |
|---|---|---|---|---|
| 2 | 13 | 23 | 6 | 40 |

- **Cỡ mẫu bình luận nhỏ.** 74/84 bình luận đến từ một video (CNBC). Mọi kết luận ở mục 3–5 vì vậy **yếu hơn** hai hồ sơ kia.

## 2. Đối thủ theo tập
| Lượt xem | Phút | Năm | Kênh | Tiêu đề |
|---|---|---|---|---|
| 1 039 350 | 14,2 | 2021 | CNBC | How Visa Became The Most Popular Card In The U.S. |
| 74 927 | 10,4 | 2021 | Practical Wisdom - Interesting Ideas | How Visa and MasterCard make their money |
| 21 015 | 26,2 | 2014 | The Motley Fool | How Visa and MasterCard Make Money (Where the Money Is) |
| 363 | 9,0 | 2026 | The Fiscal Circuit | What Actually Happens When You Swipe a Credit Card??? |
| 20 | 8,5 | 2026 | ProfitLore | How do Visa and Mastercard makes billions |
| 19 | 9,6 | 2026 | Hidden Millions | How Visa and Mastercard Make Billions Without You Realizing |
| 0 | 10,3 | 2026 | DOT. | What ACTUALLY Happens in the 3 Seconds After You Swipe Your Credit Card? |

**Số đo bổ sung (cùng ngày):**
- **Cửa sổ 90 ngày** (`labels`, câu "how do visa and mastercard make money"): 9 video dài mới, cao nhất **93 lượt**; 0/5 video đầu có dấu hiệu số liệu thật.
- **Đề tài kề "who pays for credit card rewards"** (`durable`): top 5 toàn thời gian có CNBC "Who Actually Pays For Credit Card Rewards?" **1 511 290 lượt** (17,8 phút, 2023). Ba video khác trong top 5 là video tài chính cá nhân (thẻ, điểm thưởng), lệch góc cơ chế.

**Nhãn cầu: Cầu-bền (vừa đủ) + cung mới dày, ít lượt xem.**
- Cầu-bền vừa đủ: chỉ 1 video ≥ 500 nghìn lượt (1,04 triệu), và video đó kể lịch sử một công ty, không giải thích dòng phí.
- Cung mới dày: 4 video năm 2026 có từ 0 đến 363 lượt.
- Cầu toàn thời gian **có thật nhưng mỏng hơn hẳn** container (4,8 triệu) và jet (3,8 triệu).

## 3. Năm câu hỏi hàng đầu
Trọng số thấp, nên thứ tự dưới đây là thứ tự **gợi ý**, không phải xếp hạng chắc.

| # | Câu hỏi (EN) | Trọng số | Vì sao đáng trả lời |
|---|---|---|---|
| 1 | How do zero-fee systems like India's UPI survive, and do they threaten the card model? | 330 (gộp nhiều bình luận) | Chủ đề được nhắc nhiều nhất dưới video lớn. So sánh mô hình thu phí với hạ tầng công cho thấy cơ chế rõ nhất |
| 2 | Do the networks earn more than the banks that issue the cards? Who keeps the bigger share? | 29 | Người xem hiểu sai quy mô phần của mạng thẻ. Cần bảng chia phí có nguồn |
| 3 | Why are debit swipe fees so much lower than credit? | 20 | Có thể do quy định (Regulation II) **[cần kiểm trên văn bản 12 CFR 235]**; một khoảng trống rõ |
| 4 | Who actually pays the fee on each swipe, and how is it split between merchant, acquirer, network and issuer? | 5 | Câu hỏi lõi của tựa tập; đối thủ trả lời mơ hồ |
| 5 | Are fees passed to businesses automatically, and how does settlement work? | 2 | Cơ chế clearing/settlement, hợp cảnh 3D đường ống |

## 4. Ba hoàn cảnh điển hình
1. **Người ở nơi có hệ thống thanh toán thay thế** (UPI) tự hỏi vì sao còn cần mạng thẻ; nhiều người từng nhầm thương hiệu thẻ với thị thực. Tổng trọng số 2 143, phần lớn từ một bình luận vui.
2. **Người từng làm thu ngân** nhớ cảnh tiền mặt gây lệch két và mất công đối soát cuối ngày (689). Điểm vào cho câu "vì sao cửa hàng chấp nhận trả phí thẻ".
3. **Người thấy phụ phí khi quẹt thẻ** (trạm xăng, du lịch nước ngoài), hoặc trả tiền mặt ở tiệm nhỏ để tránh phí. Đây đúng là hoàn cảnh dễ trượt sang lời khuyên; kênh chỉ giải thích vì sao có phụ phí, không khuyên trả cách nào.

## 5. Điểm yếu đối thủ
Suy từ bình luận người xem; là ý kiến của người bình luận, chưa kiểm chứng.

| Điểm yếu | Bằng chứng (tóm tắt, trọng số) | Góc của kênh |
|---|---|---|
| **Một chiều:** chỉ nói phí là chi phí của cửa hàng, bỏ qua doanh số tăng thêm và chi phí xử lý tiền mặt | 383 (cao nhất nhóm phản bác) | Trình bày cả chi phí lẫn lợi ích, mỗi bên có nguồn (khảo sát chi phí thanh toán của ngân hàng trung ương) |
| **Không so với hệ thống không thu phí** (UPI, RuPay) | 117; 92; 86 | Một cơ chế so sánh với hệ thống UPI, nguồn RBI/NPCI **[cần kiểm]** |
| **Số liệu bị nghi ngờ:** con số "10 %" chi phí, số GDP sai | 77; 43 | Mọi số có nguồn, ghi năm |
| **Gộp debit và credit** như cùng cơ chế phí | 17 và bình luận nhỏ | Tách rõ hai luồng, có văn bản quy định |
| **Không nói ai giữ phần nào** của phí | 25 và câu hỏi 29 | Mô hình riêng: chia phí trên một giao dịch mẫu, giả định ghi rõ |


**Yêu cầu khán giả** (ít): video về UPI (8 + 4), blockchain/crypto trong thanh toán (7), và **đầu tư thực sự** (17). Kênh **không** đáp yêu cầu đầu tư, vì nằm ngoài phạm vi theo `LUAT-NOI-DUNG.md`.

## 6. Thời lượng thắng
- Video ≥ 500 nghìn lượt duy nhất dài 14,2 phút. Video kề "who pays for rewards" (1,51 triệu) dài 17,8 phút.
- **Đề xuất: 14–16 phút.**

## 7. Mẫu tiêu đề
Mẫu thắng: "How [X] Became The Most Popular [Y]", "Who Actually Pays For [Z]?". Mẫu "How [X] Makes Billions…" xuất hiện nhiều ở video mới ít lượt xem; tránh dùng. Ứng viên:
- "How Visa and Mastercard Make Money Without Lending a Cent" (tên làm việc)
- "Every Card Swipe Splits Four Ways. Here's Who Gets What." *(chỉ dùng khi đã có nguồn cho mô hình 4 bên)*
- "Who Actually Gets Paid When You Tap Your Card"

Không dùng các chữ "secret", "hidden fees they don't want you to know", "save money".

## 8. Số neo cần nguồn (chưa khẳng định số nào)
| # | Số cần | Loại nguồn dự kiến |
|---|---|---|
| 1 | Trần phí interchange thẻ ghi nợ cho ngân hàng lớn ở Mỹ | Federal Reserve, Regulation II (12 CFR 235), bản hiện hành và năm hiệu lực |
| 2 | Phí interchange trung bình thẻ tín dụng và ghi nợ ở Mỹ | Báo cáo dữ liệu Regulation II của Federal Reserve; nếu không có số cho thẻ tín dụng, ghi rõ là không có số chính thức |
| 3 | Trần interchange ở EU | Regulation (EU) 2015/751 |
| 4 | Doanh thu và cơ cấu doanh thu của hai mạng thẻ | Form 10-K của Visa và Mastercard (SEC EDGAR) |
| 5 | Số giao dịch và giá trị thanh toán thẻ ở Mỹ | Federal Reserve Payments Study |
| 6 | Chi phí chấp nhận thanh toán của cửa hàng (thẻ và tiền mặt) | Khảo sát/nghiên cứu của ngân hàng trung ương (Fed, ECB) |
| 7 | Khối lượng giao dịch UPI và chính sách phí | NPCI (thống kê công bố), RBI |
| 8 | Ai trả cho điểm thưởng (trợ cấp chéo giữa người dùng tiền mặt/thẻ thường và thẻ thưởng) | Nghiên cứu của Federal Reserve Bank (cần tìm và đọc toàn văn) |

## 9. Góc tập (chờ duyệt)
- **Câu miễn trừ:** "This video explains how the system works. It isn't financial advice." (30 s đầu + đầu mô tả).
- **Móc:** nghịch lý "công ty thẻ không cho ai vay tiền, vậy tiền của họ từ đâu" (đúng mô hình bốn bên, cần nguồn 10-K).
- **Cơ chế 1, mô hình bốn bên:** cửa hàng → ngân hàng thanh toán → mạng → ngân hàng phát hành. Cảnh 3D: đường ống tiền trong suốt, gói tin chạy theo ống.
- **Cơ chế 2, interchange và quy định:** phí debit và credit theo quy định Mỹ và EU **[cần kiểm trên văn bản 12 CFR 235 và Regulation (EU) 2015/751 trước khi viết lời]**. Cảnh 3D: van điều tiết trên ống.
- **Cơ chế 3, điểm thưởng do ai trả:** trợ cấp chéo (chỉ khi có nguồn nghiên cứu). Cảnh 3D: quầy thanh toán, các dòng tiền nhỏ tách nhánh.
- **Chỗ hay hiểu sai:** "Visa giữ phần lớn phí", "phí chỉ trả cho máy POS".
- **So sánh:** UPI, theo mô tả của NPCI/RBI **[cần kiểm: cơ cấu sở hữu, chính sách phí]**. Chỉ dùng số NPCI/RBI, không đánh giá chính sách nào tốt hơn.
- **Mô hình riêng (our calculation):** chia phí trên một giao dịch 50 USD theo loại thẻ, dựa trên quy định và 10-K, giả định ghi rõ.

## 10. Rủi ro pháp lý / nội dung
- **Trung bình–cao, do YMYL.** Phải giữ đúng luật §5: không khuyên dùng thẻ hay tiền mặt, không bàn cổ phiếu V/MA, không persona chuyên gia.
- Ngành thẻ có thể có tranh chấp pháp lý đang diễn ra **[cần kiểm: tình trạng hiện hành, theo hồ sơ toà án hoặc thông cáo cơ quan]**. Kênh **không** đặt tranh chấp làm trục. Nếu nhắc, chỉ nêu đúng tình trạng từ văn bản chính thức, không nêu cáo buộc như sự thật.
- Câu hỏi về UPI dễ thành so sánh chính trị quốc gia. Giữ ở cơ chế phí và nguồn chính thức.

## Ưu, nhược, tác động, rủi ro của đề tài
- **Ưu:** thử nhánh tài chính–thanh toán sớm, đúng quyết định chủ dự án. CPM nhóm tài chính cao nhất (OutlierKit, mức công khai). Có khoảng trống rõ ở dạng dài cho câu "ai trả phí". Cảnh 3D đường ống tiền là hình riêng.
- **Nhược:** cầu toàn thời gian mỏng (1 video ≥ 500 nghìn); bình luận ít (84), nên hồ sơ yếu. Cung mới dày.
- **Tác động:** cần bộ cảnh đường ống thanh toán. Bộ này dùng lại cho "Who Actually Pays for Credit Card Rewards" (hàng đợi #10).
- **Rủi ro:** YMYL và khả năng có tranh chấp pháp lý đang diễn ra (cần kiểm). **Không đề xuất làm thí điểm.** Đề xuất đặt sau 2 tập T1/T2 để kênh có đà và quy trình soát đã chạy.

## Phép thử F1
- **Dùng chung lõi LL:** `ll.py` (nguồn, số), `charts.js` (`compare` cùng đơn vị), `kit.js` + `canvasTex` (màn hình, bảng số), `mix.py`, `qc.sh`.
- **Riêng gói kênh:** bộ cảnh đường ống tiền, câu miễn trừ và kiểm câu miễn trừ, mô hình chia phí tự tính.
