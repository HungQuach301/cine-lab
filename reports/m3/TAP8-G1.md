# TẬP 8 — G1 v2 · "The Translator's Desk" · 09/10/2026

**Phiên P** · nhánh `ccr-a261f349-6rkunc` từ `main` @ `03caa35` · checks LL v3 1.8.1 (LOCK `208121b4…`, không sửa `checks/`).
**DỪNG ở G1. Chờ chủ dự án duyệt lời, tiêu đề và thiết kế hình.** Chưa thu giọng (ElevenLabs: 0 ký tự), chưa sửa `episode.yaml` (v1 giữ nguyên để đối chiếu, như tập 7).

## 1. Tóm tắt
- **Lời viết lại toàn bộ** theo trục biến đổi (CHUAN-KENH §12): `reports/m3/ep08/loi-v2.txt`, 17 đoạn, **1 292 từ, ước 10:23** (Bill 2,214 từ/s, gồm đệm cảnh truyện, tựa, thẻ kết và 3 khoảng lặng trước số neo).
- **Xương sống mới, có thật và nối liền:** người dịch tình nguyện Red Cross 1942 (ảnh LoC) → **Nuremberg 1945**: Leon Dostert dựng phiên dịch song song, thiết bị IBM, nghề phiên dịch đổi từ "chờ người nói dừng" sang "nói cùng lúc" → **cũng Dostert** dẫn thí nghiệm dịch máy Georgetown–IBM 1954 (250 từ, 6 quy tắc, "vài năm nữa") → ALPAC 1966: máy chưa dùng được, phải "postediting", nhưng **máy trợ giúp** (bảng thuật ngữ Mannheim) thì có ích → sau 2010 dịch máy dùng hằng ngày → hôm nay BLS ghi "post-editing" là một phần của nghề → dự báo 2025–35.
- **Mạch biến đổi xuyên suốt:** công nghệ hai lần đổi nghề theo hai cách (giúp người phiên dịch / thay một phần việc dịch), chữ "postediting" của 1966 thành quy trình chuẩn hôm nay. "Máy thay người" chỉ nói đúng nguồn (FLP: ≈ 28 000 việc làm không được tạo ra; BLS: máy "chưa" làm được như người), không làm trọng tâm.
- **Kiểm mù: 2 vòng × 3 subagent Sonnet độc lập (6 lượt).** Cả 6 lượt rút ra **thông điệp đúng mạch biến đổi**, 6/6 xếp giọng phim loại **(b) "công việc đổi qua thời gian, người đi theo"**. Vòng 1: sửa 17 điểm ≥ 2/3; vòng 2: sửa 12 điểm ≥ 2/3 (mục 5).
- **Nguồn:** mọi số và sự kiện trong lời có nguồn đọc toàn văn. Nguồn mới: Bowen (Meta 1985), Hutchins (2006), OOH Interpreters & Translators 2025–35 (WebFetch, BAI-HOC #81). Chi tiết `ep08/NGUON-TAP8.md` §7–10.
- **Thiết kế hình ngay từ G1:** 6 cảnh đinh 3D mới, không còn bàn 2D (`desk`); mô phỏng **Q26b ĐẠT** trên bảng bối cảnh (mục 6).

## 2. Tiêu đề (3 phương án, cùng trục biến đổi)
| | Tiêu đề | Ký tự | Ưu | Nhược |
|---|---|---|---|---|
| **A (P khuyến nghị)** | From Headphones to Machine Drafts: How Translators' Work Changed | 64 | Nêu thẳng mạch biến đổi; hai hình ảnh cụ thể (tai nghe Nuremberg, bản nháp máy) khớp hai cảnh đinh và kết §14 | Ít tò mò hơn C |
| B | The Interpreter Who Tried to Build a Translating Machine | 56 | Truyện người thật, rất tò mò, đúng nguồn (Dostert) | Đặt trọng tâm vào một người và vào "máy dịch", không vào nghề |
| C | In 1954, Machines Were "A Few Years" From Translating. Then What? | 63 | Khớp móc câu §00 và câu trả lời §14–15; có năm (Q13: 1954 có trong lời) | Gần giọng câu view; dấu ngoặc trích có thể bị hiểu là trích một người |

Q13: không có số cần truy nguồn ngoài năm 1954 (có trong lời).

## 3. Lời v2 (khoá ứng viên, sau 2 vòng kiểm mù)
Tệp: `reports/m3/ep08/loi-v2.txt` (SHA-256 `824df1f0…e11d038`). Hồi theo Q30: 1 truyện (ấm) = 00–01 · 2 lịch sử (sepia) = 02–08 · cầu nối truyện 09 · 3 hôm nay (lạnh) = 10–14 · 4 kết (ấm) = 15–16.

**[00]** In 1954, a computer in New York translated more than sixty Russian sentences. The forecasts said that within a few years, machines would translate almost anything. But it took far longer. When the machines finally arrived, what happened to the people who carry words between languages?

**[01]** At dusk, the lamplighter passes a library. Inside, volunteers bend over messages written in Dutch, Polish, German, and French, translating each one. The lamplighter raises the flame to the post by the window, and inside, a reading lamp comes on. Lamplighting is a job machines took over long ago. Tonight, its flame opens the story of a job machines were once expected to take over quickly.

**[02]** Those volunteers were real. A photograph taken in 1942, at the Red Cross in Washington, shows them at work. Translators worked with writing, one sentence at a time. Interpreters worked with speech, and they worked the same way: the speaker stopped, and then the interpreter said it again in another language. A few years later, a trial changed how interpreters worked.

**[03]** In October 1945, Leon Dostert, who had been General Eisenhower's interpreter during the war, was asked to set up the interpretation for the war crimes tribunal at Nuremberg. He chose a method many thought would not work: simultaneous interpretation, speaking while the speaker is still speaking. IBM donated the equipment. Every participant in the courtroom wore headphones and could choose a language. The interpreters sat in booths, each working into their own language only, with a warning light to ask a speaker to slow down.

**[04]** It was the first large-scale use of simultaneous interpretation, and historians count it a success. The new equipment did not replace the interpreters. It changed their job, from waiting for the speaker to stop, to speaking at the same time. Soon the United Nations installed a similar system, and Dostert went on to Georgetown University in Washington, to train linguists for government service.

**[05]** The lamplighter walks on. Machines had long since taken over lamplighting; now they were turned on language. After the war, American officials worried about how little they knew of Soviet work, written in Russian. So Dostert, who had used machines to help interpreters, turned to a machine that would translate by itself. On January 7, 1954, his Georgetown team and IBM showed it in New York. The computer knew only two hundred fifty words and six rules of grammar, enough for those chosen sentences. The next morning it was on front pages, and the forecasts said a machine built just for translation could be ready within a few years.

**[06]** In 1966, twelve years after the demonstration, a committee of the National Academy of Sciences took stock. First, it counted the people. In October 1962, the federal government employed only two hundred sixty-two translators and clerk-translators in the United States, and the committee found more translators available than there was work for them. There was no shortage of people for a machine to fix. Then it counted the money. Over ten years, the government had spent some twenty million dollars on machine translation and related research.

**[07]** The results were thin. Back in 1962, eight years into the work, the Georgetown project had tried to produce useful output, and it had to have people correct the machine's output. The committee called this postediting. The postedited translation took slightly longer, and cost more, than ordinary human translation. Its conclusion was blunt: there was no immediate or predictable prospect of useful machine translation.

**[08]** But the committee also found a machine that did help. At a military translation agency in Germany, a computer produced a list of the technical terms in each text, with their translations. Translators who had the list finished much faster, and made a third fewer errors than translators without it. So the committee recommended research into language, and better human translation, with machine aids. A machine to help the translator, not to replace one.

**[09]** The lamplighter walks on, and the years pass: the sixties, the eighties, a new century. The library's lamps go out. Across the street, a screen is lit in an apartment. Someone pastes a paragraph into a box, and a moment later it comes back in another language.

**[10]** That box is machine translation. After 2010, Google Translate arrived as a phone app and inside web browsers, and it went into everyday use. Today, the government's job handbook describes two kinds of machine on the translator's desk. One keeps a database of sentences already translated, so they can be reused. The other, machine translation software, writes a first draft, which the translator then reviews. The handbook calls this post-editing: the same word the committee used in 1966 for people correcting the machine. Then, it was slower than translating from scratch. Now it is part of the job.

**[11]** The change shows up in the numbers too. Economists at Oxford compared hundreds of local job markets across the United States. Where people used Google Translate more, translator employment grew more slowly. What they found was not layoffs. It was jobs that never appeared: they estimate about twenty-eight thousand translator jobs that the profession's growth would have created, but did not. It is an estimate, not a count. Similar jobs, such as editors and technical writers, showed no such effect. The study also points to a shift toward higher-skilled translation work, the tasks machine translation cannot easily replace.

**[12]** That is translation, the written word. Interpreting, the spoken and signed word, has changed in its own way. Interpreters now work remotely as well as in person. Demand for American Sign Language interpreters is expected to grow, as more people use video relay services: online video calls with a sign language interpreter on the line. And in courtrooms, where this story began, most states now require interpreters to be certified.

**[13]** And the next ten years? The government projects that interpreters and translators will grow from about seventy-four thousand jobs in 2025 to about seventy-five thousand in 2035. That is two percent over the whole decade, about fifteen hundred more jobs, slower than the three and a half percent projected for all jobs. Slower growth, not decline. Even so, about six thousand positions are projected to open each year, mostly to replace people who retire or change careers. Computer tools, including AI, are making the work more efficient, the handbook says. But many of these jobs cannot be entirely automated, because computers cannot yet produce work comparable to what human translators do in most cases. Cannot yet.

**[14]** Here is the comparison we can make, and it is a comparison of patterns, not of technologies. In both eras, a repetitive part of the work went to a machine, and people moved to the work around it. One difference matters. In 1966, the machine was not good enough, and the committee said so. This time, the machine is in everyday use, and the Oxford study finds it has slowed the growth of translator jobs. So what happened to the people who carry words between languages? When machine translation finally reached everyday use, the profession did not disappear. The work moved: from waiting for a speaker to stop, to speaking at the same time; from writing every sentence, to checking a machine's draft; from the courtroom booth, to the video call.

**[15]** In 1954, the forecasts said a few years. It took more than fifty. And the handbook's word, yet, is the open question: which part of the work stays with people, and for how long?

**[16]** Back on the street, the lamplighter reaches the last post. The glass opens, the flame takes, and the light passes on to the next corner. Every era has its last lamplighters. For the people who carry words between languages, the flame keeps changing hands.

*(Thẻ kết sau §16: "More from Last Lamplighters".)*

### Tỷ lệ theo khung kể (ước, cùng cách tính tập 7)
| Phần | Đoạn | Thời lượng | % | Đích |
|---|---|---|---|---|
| Mở | 00–01 | 59,3 s | 9,5 | |
| Quá khứ | 02–04 | 96,8 s | 15,5 | |
| Chuyển giao | 05–09 | 182,3 s | 29,3 | |
| Hiện tại | 10–12 | 123,3 s | 19,8 | |
| Tương lai | 13–14 | 113,9 s | 18,3 | |
| Kết | 15–16 | 47,0 s | 7,6 | |
| **Mở + Kết** | | 106,3 s | **17,1** | 15–20 ✓ |
| **Quá khứ + Chuyển giao** | | 279,1 s | **44,8** | 40–45 ✓ |
| **Hiện tại + Tương lai** | | 237,2 s | **38,1** | 35–40 ✓ |

**Nêu tên theo luật ±5 %:**
- Quá khứ + Chuyển giao 44,8 % sát trần 45 % (cách 0,2 điểm). Bản thu thật lệch ±3 % (BAI-HOC #18) có thể đẩy quá 45 %. Nếu vượt, P rút đoạn 05 (câu "Machines had long since…") trước, không đụng số.
- Hiện tại + Tương lai 38,1 % sát trần 40 % (cách 1,9 điểm).
- Câu trả lời móc câu (≈ 25 s cuối §14) đặt trong đoạn Tương lai, theo góp ý vòng 2 (2/3: "trả lời rõ trước kết"). Nếu tính phần này vào Kết: Mở + Kết ≈ 21 %, Hiện tại + Tương lai ≈ 34 %, cả hai lệch ≤ 1 điểm, trong dung sai ±5 điểm của CHUAN-KENH §2.
- Thời lượng ước 10:23, dưới trần 11:00 khoảng 5,6 %.
- Quy đổi bảng cũ: STORY (00, 01, 09, 16) ≈ 18,5 %; HISTORY (02–08) ≈ 40,9 %; TODAY (10–15) ≈ 40,8 %.

### Số trên hình và số neo (dự kiến cho đặc tả)
| Khoá | Số | Loại | Nguồn | Đoạn |
|---|---|---|---|---|
| `w250` **(neo)** | 250 words · 6 rules | ACTUAL 1954 | HUT06 | 05 |
| `fed62` | 262 | ACTUAL 10/1962 | ALPAC | 06 |
| `mt20` | $20 million (10 năm) | ACTUAL | ALPAC | 06 |
| `frey` **(neo)** | ≈ 28,000 (ước tính, "not a count") | ACTUAL, ước tính phản thực | FLP | 11 |
| `it25` → `it35` | 73,900 → 75,400 | ACTUAL gốc dự báo → PROJECTION 2025–35 | OOH-IT | 13 |
| `it_chg` **(neo)** | +2.0 % (+1,500) | PROJECTION 2025–35 | OOH-IT | 13 |
| `all_chg` | +3.5 % | PROJECTION 2025–35 | EP | 13 |
| `open` | ≈ 6,000/năm | PROJECTION 2025–35 | OOH-IT | 13 |
- Ước Q17: 9 số trên hình / 10,4 phút ≈ 0,87 số/phút (≤ 2).
- Số chỉ đọc, không lên hình: "more than sixty" câu (1954), "a third fewer errors" (ALPAC Mannheim).
- **Bỏ so với v1:** toàn bộ MLR26 (đợt 2024–34) thay bằng đợt 2025–35; 4 000/300 (JPRS), 13/22 triệu USD, 695 thị trường, lương phục hồi 2016 (đọc mù 3/3 khó nghe; giữ trong nguồn).

## 4. Kiểm so sánh tương xứng (6 điểm)
| Điểm | Cặp / nội dung | Kết quả |
|---|---|---|
| 1. Cùng cơ chế | Một phần việc lặp lại của người dịch/phiên dịch chuyển cho máy: 1954–66 (thử, thất bại; máy trợ giúp có ích) ↔ sau 2010 (dịch máy hằng ngày, post-editing). Nuremberg là công nghệ **trợ giúp** người phiên dịch, lời nói rõ "did not replace the interpreters" | Đạt |
| 2. Cùng thước đo | Cặp số duy nhất đặt cạnh nhau: +2.0 % ↔ +3.5 % (cùng BLS, cùng kỳ 2025–35, cùng loại dự báo). 262 (1962) và ≈ 28 000 (ước tính) **không** đặt cạnh số hôm nay | Đạt |
| 3. Cùng loại nguồn, địa lý | Số trên hình đều của Mỹ. Mannheim (Đức) chỉ là sự kiện lịch sử trong lời, không phải số trên hình | Đạt |
| 4. Thực tế / dự báo | 250, 262, $20M, 73 900 (ACTUAL); ≈ 28 000 (ACTUAL, **ước tính**, lời nói "an estimate, not a count"); 75 400, +2.0 %, +1 500, 6 000/năm, +3.5 % (PROJECTION) | Đạt |
| 5. Tương tự kèm khác biệt | §14: "a comparison of patterns, not of technologies" + khác biệt: 1966 máy chưa đủ tốt, uỷ ban nói thẳng; nay dùng hằng ngày và (FLP) đã làm chậm tăng trưởng việc làm | Đạt |
| 6. Thang thời gian | Không so tốc độ giữa hai thời | Đạt (không áp dụng) |
- Q23 dự kiến: câu §13 "seventy-four thousand … 2025 … seventy-five thousand in 2035" là cặp gốc dự báo cùng nguồn (miễn (b)); "two percent … three and a half percent" cùng loại, cùng kỳ, cùng họ nguồn BLS.
- §10 luật lời dẫn (CHUAN-KENH §10): lời không nói phim làm bằng AI; câu duy nhất có "AI" là trích OOH về nghề.

## 5. Kiểm mù kịch bản — khoá lời (2 vòng × 3 subagent Sonnet độc lập)
Đề bài chung (`ep08/blind-g1/DE-BAI.txt`), chỉ đưa tệp lời, không ngữ cảnh. Câu trả lời lưu nguyên văn: vòng 1 `ep08/blind-g1/R1–R3.md` (lời SHA `3e840c71…`), vòng 2 `ep08/blind-g1/vong-02/R1–R3.md` (lời SHA `c437fb68…`).

**Thông điệp chính người xem rút ra (câu hỏi bắt buộc §12):**
- V1-R1: "…has slowly changed translators' work rather than ending it. Machines take the repetitive part and people move to the work around it, though how much stays with people is still open."
- V1-R2: "…when it finally worked, translators' work shifted (post-editing, higher-skill tasks, video relay) rather than vanishing."
- V1-R3: "…it did not erase translators; it moved their work (to checking drafts, remote and video interpreting)."
- V2-R1: "…the translation profession did not vanish; the work shifted…, though machines have slowed job growth."
- V2-R2: "…the profession has not vanished but shifted…, though growth is slowed and the future ('yet') is open."
- V2-R3: "…the profession did not vanish but shifted toward checking machine drafts, as interpreting shifted at Nuremberg."
- **Kết luận:** 6/6 đúng mạch biến đổi; giọng (b) 6/6; không ai rút ra "máy thay người". Móc câu: "Partly" 6/6, vì kết để ngỏ câu hỏi "yet" (chủ ý theo §12: tương lai chỉ bằng nguồn hoặc câu hỏi mở).

**Vòng 1 — điểm ≥ 2/3 đã sửa:**
| # | Điểm | Số người | Sửa |
|---|---|---|---|
| 1 | §00→§01 người thắp đèn không nối với móc câu; ẩn dụ mơ hồ | 3/3 | §01 "opens the story of a job machines were once expected to take over quickly" |
| 2 | §02 "That photograph" không có tiền ngữ khi nghe | 3/3 | "Those volunteers were real. A photograph taken in 1942… shows them at work." |
| 3 | §03 dồn chi tiết thiết bị | 3/3 | bỏ "four language channels", "dictation speed", câu tài liệu |
| 4 | §04 danh sách năm 1946/1949 không có ý | 3/3 | gộp một câu "Soon the United Nations…"; nói rõ Georgetown ở Washington |
| 5 | §04→§05 Georgetown/1954 đột ngột, thiếu lý do | 3/3 | §05 nêu lý do (thiếu hiểu biết về công trình Liên Xô) và nối "Dostert, who had used machines to help interpreters…" |
| 6 | §06 262 / 4 000 / 300 rối | 3/3 | bỏ 4 000/300; thêm "more translators available than there was work for them" |
| 7 | $20 triệu không có thang | 3/3 | (vòng 1 thêm so với hoá đơn dịch một năm; vòng 2 bỏ, xem V2 #3) |
| 8 | §10 "the word from 1966 is back" khó nghe | 3/3 | "The handbook calls this post-editing: the same word the committee used in 1966…" |
| 9 | §10 chồng thuật ngữ (CAT, localizers, MT) | 3/3 | bỏ "localizers"; tả hai loại máy bằng lời thường |
| 10 | §08→§10 nhảy 50 năm không mốc | 3/3 | §09 "the years pass"; §10 mở bằng "That box is machine translation. After 2010…" |
| 11 | ≈ 28 000 dễ nghe thành mất việc; 695 thị trường vô nghĩa | 3/3 | bỏ 695; nói rõ "not layoffs" |
| 12 | §11→§12 đổi dịch viết → phiên dịch không báo | 3/3 | câu chuyển "That is translation, the written word. Interpreting…" |
| 13 | §12 danh sách nhu cầu nhạt | 3/3 | bỏ "diverse population, globalization, military"; thêm tòa án "where this story began" |
| 14 | §13 2 % dễ hiểu thành mỗi năm/giảm; 6 000 dễ hiểu thành việc mới | 3/3 | "two percent over the whole decade… Slower growth, not decline"; 6 000 "mostly to replace…" |
| 15 | §14 "the word yet in that sentence" trỏ vào câu không nghe thấy | 3/3 | §13 kết bằng "Cannot yet." cho nghe rõ |
| 16 | §14–15 nghe như ý kiến người dẫn | 3/3 | gắn nguồn ("the Oxford study finds"; "the handbook's word"); câu so sánh ghi rõ là so sánh mẫu hình (bắt buộc theo §3 điểm 5) |
| 17 | "five years" ↔ "three to five" ↔ "more than fifty" lệch nhau | 3/3 | thống nhất "within a few years" (CSM qua HUT04) ở §00, §05, §15 |
| 18 | §16 "last lamplighters" mâu thuẫn "không biến mất" | 2/3 | "the flame keeps changing hands" |

**Vòng 2 — điểm ≥ 2/3 đã sửa:**
| # | Điểm | Số người | Sửa |
|---|---|---|---|
| 1 | "more than sixty" ↔ "a few dozen" lệch | 3/3 | §05 "enough for those chosen sentences" |
| 2 | Mốc năm lùi (1966 → 1962) | 3/3 | §06 mở "In 1966, twelve years after…"; §07 "Back in 1962, eight years into the work…" |
| 3 | $20 triệu (10 năm) so với hoá đơn 1 năm là so lệch thước | 3/3 | bỏ phép so (đúng luật §3 điểm 2) |
| 4 | 262 không có ý nghĩa | 3/3 | "only 262…"; "There was no shortage of people for a machine to fix." |
| 5 | §09 "half a century later" mơ hồ | 3/3 | "the years pass: the sixties, the eighties, a new century" |
| 6 | 6 000 chỗ trống/năm ↔ tăng ròng ≈ 1 000 | 3/3 | nêu "about fifteen hundred more jobs"; "Even so, about six thousand positions… to replace people…" |
| 7 | 28 000 vẫn dễ nghe thành mất việc | 3/3 | đặt khung trước số: "What they found was not layoffs. It was jobs that never appeared: …" (cách tập 7 #6) |
| 8 | §01→§02 "scene" nào | 3/3 | xem #2 vòng 1 (đã đổi thành "Those volunteers were real") |
| 9 | §05 "The lamplighter walks on" chỉ để trang trí | 3/3 | thêm "Machines had long since taken over lamplighting; now they were turned on language." |
| 10 | §11→§12 vẫn đột ngột | 3/3 | xem #12 vòng 1 |
| 11 | §08 "a third fewer errors" so với ai | 2/3 | "…than translators without it" |
| 12 | Trả lời móc câu chưa rõ; §14 và §15 lặp | 2/3 | §14 kết bằng câu trả lời trực tiếp ("So what happened…? … the profession did not disappear. The work moved: …"); §15 rút còn mốc thời gian + câu hỏi mở |
- **Không sửa (lý do):**
  - §14 "Here is the comparison we can make… One difference matters." (3/3 "ý của người dẫn"): bắt buộc theo CHUAN-KENH §3 điểm 5; câu đã nói rõ đây là phép so sánh mẫu hình của phim, không gán cho nguồn.
  - §13 "Cannot yet." (2/3): nhắc lại nguyên văn từ của OOH, cần cho §15.
  - §08 "A machine to help the translator, not to replace one." (2/3 "lời bình"): tóm tắt khuyến nghị ALPAC ("improved human translation, with an appropriate use of machine aids"). Nếu chủ dự án muốn, đổi thành câu trích.
  - Mật độ chi tiết §03 (2/3): đã rút ở vòng 1. Giữ đèn cảnh báo và buồng dịch vì chúng là hình vật chất của cảnh đinh Nuremberg (Q29).
- Vòng 3 không chạy. Các điểm ≥ 2/3 của vòng 2 là điểm rõ nghĩa, đã sửa đúng như người đọc gợi ý. Nếu chủ dự án muốn khoá bằng một vòng xác nhận nữa, chạy 3 lượt mới trước khi thu giọng (≈ 150 nghìn token subagent).

## 6. Thiết kế hình (theo PLAN "Cải thiện hình", BAI-HOC #96–97, Q26b)
### 6.1 Sáu cảnh đinh 3D mới (`design/ll-hero/ep08.js`, không dùng lại bố cục tập 6–7)
| Khoá | Bối cảnh | Hình vật chất, chất liệu, ánh sáng có nguồn | Đoạn |
|---|---|---|---|
| `library` | Góc phố thư viện lúc chạng vạng; trong: phòng đọc bàn dài, đèn đọc sách xanh | Bậc đá, cửa sổ cao khung gỗ, gạch có vân; trong phòng: kệ sách nhiều gáy màu, giấy viết tay, từ điển mở; đèn bàn + ánh hoàng hôn; người thắp đèn có lửa mồi (BAI-HOC #77) | 00, 01, 02, 05, 09, 15, 16 |
| `booths` | Phòng xử Nuremberg 1945: dãy buồng kính phiên dịch, tai nghe trên mọi băng ghế, cáp trên sàn, đèn cảnh báo vàng/đỏ | Ốp gỗ sẫm có vân, kính phản chiếu, đèn quay phim công suất lớn (sáng, tương phản mạnh, không tối đặc); không cận mặt, người chỉ thấy lưng/bóng | 03, 04, 14 |
| `ibm` | Phòng máy IBM New York 1954 (ban ngày, trắng sáng) | Tủ máy, chồng thẻ đục lỗ, máy in dòng nhả chữ tiếng Anh, sàn ô bóng; ánh cửa sổ + đèn trần ống | 05 |
| `postedit` | Phòng dịch thập niên 1960 ban ngày | Bàn gỗ, máy chữ, tạp chí tiếng Nga, giấy in máy có vết bút đỏ sửa (cận cảnh), bảng thuật ngữ in liên tục; nắng xiên qua rèm | 06, 07, 08, 14 |
| `studio` | Bàn người dịch hôm nay, ban ngày | Hai màn hình (bên trái câu nguồn, bên phải bản nháp máy đang sửa), cây xanh, cốc, sổ tay, thảm có vân; nắng cửa sổ + đèn bàn | 10, 11, 14 |
| `vrs` | Buồng phiên dịch từ xa / video relay, ban ngày | Tai nghe, micro, màn hình gọi video (hình người ra dấu cách điệu, không cận mặt), cửa sổ thành phố; ánh màn hình + cửa sổ | 12, 13, 14 |
- Ảnh tư liệu (trung tính Q26b): LOC-8d21281, LOC-8d21282 (Red Cross 1942, đã có trong NGUON §4), ≈ 32 s ≈ 5 % (≤ 20 %).
- Không còn mẫu `desk` 2D (tập 7 BAI-HOC #78). `sign` 2D chỉ cho hai số ($20M, ≈ 28 000), có thể chuyển thành chú thích số trên cảnh đinh khi viết đặc tả (BAI-HOC #87).
- Âm thanh nghề mới dự kiến: rì rầm phòng xử qua tai nghe, máy in dòng + đọc thẻ đục lỗ, máy chữ + kéo giấy, gõ phím + nhấp chuột, chuông cuộc gọi video. Mọi tệp vào RIGHTS.md.
- Tuỳ chọn sau G1: tìm ảnh Nuremberg buồng phiên dịch của chính phủ Mỹ (.gov, NARA/Truman Library). Chỉ thêm khi đủ hồ sơ quyền Q19.

### 6.2 Bảng bối cảnh – thời lượng dự kiến (theo thời lượng ước từng đoạn)
| Đoạn | Bối cảnh (thời lượng, s) |
|---|---|
| 00 | library 21,9 |
| 01 | library 15 · tư liệu 22,4 |
| 02 | tư liệu 10 · library (phòng đọc) 18,4 |
| 03 | booths 20 · booths (trong buồng) 19,2 |
| 04 | booths 15 · booths 14,3 |
| 05 | library (phố) 10 · ibm 22 · ibm (máy in) 21,2 |
| 06 | postedit 14 · isotype 262 13 · sign $20M 13,4 |
| 07 | postedit (cận bản in sửa đỏ) 20 · trích ALPAC 9,7 |
| 08 | postedit (bảng thuật ngữ) 34,2 |
| 09 | library (thư viện tắt đèn → căn hộ) 25,2 |
| 10 | studio 22 · studio (màn hình post-editing) 23,1 |
| 11 | bản đồ 10 · studio 22 · sign ≈ 28 000 13,8 |
| 12 | vrs 32,4 |
| 13 | isotype 73 900 → 75 400 14 · bars +2.0 % / +3.5 % 12 · vrs 28,8 |
| 14 | diptych postedit 1962 \| studio today (có nhãn) 22 · booths 8 · studio 10 · vrs 10 · studio 10 |
| 15 | library 16,2 |
| 16 | library 24,9 · thẻ kết "More from Last Lamplighters" 6 |

### 6.3 Mô phỏng Q26b trên bảng (theo mô tả RULES-LL 1.8.1; công cụ P, không phải bộ chấm của K)
| Bối cảnh | Tổng | % phim (≤ 25) | Liên tục dài nhất (≤ 90 s) |
|---|---|---|---|
| library | 131,6 s | 21,1 | 55,3 s |
| studio | 98,1 s | 15,7 | 67,1 s |
| postedit | 79,2 s | 12,7 | 54,2 s |
| booths | 76,5 s | 12,3 | 68,5 s |
| vrs | 71,2 s | 11,4 | 61,2 s |
| ibm | 43,2 s | 6,9 | 43,2 s |
| 2d/sign | 27,2 s | 4,4 | 13,8 s |
- **Nửa sau** (từ ≈ 5:12): studio 98,1 s, vrs 71,2 s, library 66,3 s, sign 13,8 s, postedit 12,6 s, booths 8 s → **6 bối cảnh ≥ 3 s (cần ≥ 3)**. Có ban ngày (studio, vrs), cận cảnh (màn hình post-editing).
- **Kết luận: ĐẠT cả (a), (b), (c).** Không chỉ số nào trong ±5 % quanh ngưỡng. Sẽ chạy lại bằng `ll.py check` trên đặc tả thật trước khi dựng nháp.

## 7. Token và giờ máy (đo từ log phiên, khử trùng theo message id)
| Bước | Sinh ra | Đầu vào mới (gồm ghi cache) | Đọc cache |
|---|---|---|---|
| P: đọc tài liệu, tra 5 nguồn, viết lời, 2 lượt sửa, mô phỏng Q26b, NGUON (đến trước khi viết báo cáo này) | ≈ 72 nghìn | ≈ 210 nghìn | ≈ 9,5 triệu |
| Kiểm mù 6 lượt subagent Sonnet | ≈ 6 × 1 nghìn | ≈ 192 nghìn (3 × 49 nghìn vòng 1, 3 × 15 nghìn vòng 2) | ≈ 0,37 triệu |
- **Tổng đầu vào mới + sinh ra ≈ 0,48 triệu** (cộng phần viết báo cáo, commit: ước ≈ 0,5 triệu). Trần mềm 1,5 triệu cho cả tập. G1 dùng ≈ 1/3 trần, cao hơn tập 7 (0,33 triệu): do tra thêm 3 nguồn toàn văn mới và chạy kiểm mù 2 vòng thay vì 1.
- Giờ máy: không render. **ElevenLabs: 0 ký tự** (chưa thu giọng).

## 8. Đang chờ chủ dự án
1. **Duyệt lời v2** (mục 3), hoặc chỉ đạo sửa. Có muốn chạy vòng đọc mù thứ 3 để xác nhận không (mục 5)?
2. **Chọn tiêu đề:** A, B hoặc C (mục 2).
3. **Duyệt thiết kế hình:** 6 cảnh đinh và bảng bối cảnh (mục 6). Riêng cảnh Nuremberg: chủ đề tòa án tội ác chiến tranh. P giữ hình trung tính (buồng dịch, tai nghe), không cận mặt, không nhắc bị cáo.
4. **Ghi AUTHORSHIP** quyết định sáng tạo: trục Dostert (Nuremberg → Georgetown–IBM), câu kết "the flame keeps changing hands".
5. **(Tuỳ chọn)** Nhờ Claude (Cowork) đối chiếu nguyên văn OOH Interpreters & Translators (P đọc qua WebFetch). Các số trong lời khớp số chủ dự án đưa.
6. G3 tập 7 (đã chờ từ trước).

**Sau khi duyệt**, P sẽ:
1. sửa `episode.yaml` (map, heroes, numbers, anchors, pause, sfx, `frame0`) và viết `design/ll-hero/ep08.js`;
2. kiểm trước build: `ll.py check` (gồm Q26b), `tests/run.sh`, `node --check`, xem trước `hero.js --only` vài khung;
3. kiểm bộ đếm ElevenLabs, thu giọng, kiểm bộ đếm lần nữa (#98);
4. dựng nháp 960×540 (không chấm Q27/Q31 mù trên nháp), sửa một lượt;
5. render 1080p một lần (song song cảnh 3D nếu CPU/RAM cho phép, cache theo shot);
6. chạy QC Q1–Q31 + Q26b + LOCK, chấm Q27 chính thức một lần trên 1080p;
7. **DỪNG ở G2.**
