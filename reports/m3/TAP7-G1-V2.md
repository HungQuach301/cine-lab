# TẬP 7 — G1 rút gọn v2 · "When Computers Were People" · 08/10/2026

**Phiên P** · nhánh `claude/eager-babbage-6cc4l6` từ `main` @ `b9acad1` · checks LL v3 1.7.1 (áp từ bước dựng).
**DỪNG ở G1. Chờ chủ dự án duyệt lời.** Chưa thu giọng, chưa sửa đặc tả `episode.yaml` (v1 giữ nguyên để đối chiếu).

## 1. Tóm tắt
- Lời viết lại theo trục kể mới (CHUAN-KENH §12, BAI-HOC #80): Mở → Quá khứ → Chuyển giao → Hiện tại → Tương lai → Kết. 17 đoạn, **1 332 từ, ước 10:39** (tốc độ Bill 2,214 từ/s, gồm khoảng đệm cảnh truyện, tựa và 3 khoảng lặng trước số neo).
  - **Nêu tên theo luật ±5 %:** ước 10:39 nằm dưới trần 11:00 khoảng 3,1 %. BAI-HOC #18 cho thấy `est` thường ước dư khoảng 3 %. Nếu bản thu thật vượt 11:00, P rút đoạn 06 (giai thoại phi hành gia) trước, không đụng số.
- Kiểm mù: **3 subagent Sonnet độc lập**, chỉ nhận tệp lời. **Cả 3 rút ra thông điệp đúng mạch biến đổi** (giọng phim: 3/3 xếp loại (b) "công việc đổi qua thời gian"). P đã sửa **9 điểm ≥ 2/3** (mục 4).
- Nguồn: mọi số trong lời đã đọc toàn văn. Có hai nguồn mới là OOH Software Developers và OOH Computer Programmers 2025–35, P đọc qua WebFetch vì bls.gov chặn curl (BAI-HOC #81). Số khớp với số "đã xác minh (Claude)" 06/10. Chi tiết ở `ep07/NGUON-TAP7.md` §7.

## 2. Ba phương án tiêu đề (cùng trục biến đổi)
| | Tiêu đề | Ưu | Nhược |
|---|---|---|---|
| **A (chủ dự án đề xuất; P khuyến nghị)** | When Computers Were People: How One Word Changed Jobs Three Times | Khớp móc câu §00 và kết §15 ("three kinds of work"); tò mò; không có số dễ sai | Dài (66 ký tự), có thể bị cắt trên di động sau "Three" |
| B | One Word, Three Jobs: From Human Computers to Programmers to AI | Nêu thẳng mạch ba thời; ngắn hơn (61) | Chữ "AI" ở cuối có thể kéo về chủ đề AI hơn chủ đề nghề |
| C | The First Computers Were People. Here's Where Their Work Went | Mạch "việc đi đâu" rõ; giọng kể chuyện | Không có ba mốc; gần giọng tiêu đề câu view |

Q13 (số trong tiêu đề): không có số cần truy nguồn ("three" < 10).

## 3. Lời đầy đủ (v2, sau sửa kiểm mù) — tệp `reports/m3/ep07/loi-v2.txt`
Hồi theo Q30: 1 truyện (ấm) = 00–01 · 2 lịch sử (sepia) = 02–08 · cầu nối truyện 09 · 3 hôm nay (lạnh) = 10–14 · 4 kết (ấm) = 15–16.

**[00]**
What happens to a job when a machine takes its name? The word computer has stood for three kinds of work. First, a person who calculated with a pencil. Second, the people who programmed a new machine. Third, people working beside a machine that can help write the code. Same word. Three different jobs.

**[01]**
At dusk, the lamplighter passes a research laboratory by an airfield. One long window is still lit. The lamplighter raises the flame to the post beside it, and inside, a desk lamp comes on, as if the light had been handed through the glass. Lamplighting is a job machines took over long ago. Tonight, it opens the story of another.

**[02]**
Before electronic computers, the word computer meant a person. It was a job title: someone who performed mathematical equations and calculations by hand. In 1935, five women formed the first computer pool at the Langley aeronautical laboratory in Virginia. They read film of the wind tunnel instruments, ran the calculations, and plotted the results on graph paper, using slide rules, magnifying glasses, and calculating machines that could multiply and take square roots. Their graphs went back to the engineers, to design the next test.

**[03]**
It was skilled work. Most of the women had degrees in mathematics or the sciences, and a good number had been high school teachers. The job was a door: a way into aeronautical research at a time when most women simply were not being hired as engineers, and it paid much better than most jobs open to women. It was a narrow door. The computers were classed as subprofessionals, while men with similar degrees were often hired as junior engineers, for more pay. A 1942 document said the computers did more in a morning than an engineer alone could finish in a day.

**[04]**
Then came the war, and computing spread from one office into the wind tunnels and research divisions. A 1942 report counted seventy-five women computers. By 1946, the head of computing had trained about four hundred and placed them across the laboratory. The door did not open evenly. In the 1940s, Langley also began recruiting Black women with college degrees as computers. Under segregation, they were grouped in a separate section, the West Area Computers, with segregated dining rooms and bathrooms. They did the same work. In the 1950s, the sections began to integrate.

**[05]**
Then came the second kind of work. In 1947, the laboratory's agency acquired a huge electronic computer, and it got its own computing group: people in charge of programming it, feeding it punched tape to solve the equations of high-speed flight. With the first electronic computers, NASA's history says, the human computers took on programming duties as well.

**[06]**
At the Jet Propulsion Laboratory in California, women computers calculated the paths of spacecraft, and went on to become some of the first computer programmers at NASA. In 1958, their calculations helped put Explorer 1, the first American satellite, into orbit. At first, as JPL puts it, the machines were fast but not nearly as reliable as the people. Before the first American orbital flight, the astronaut asked for a mathematician who had started out as a human computer to check the machine's numbers.

**[07]**
Over time, the arithmetic itself went to the machines. Human computing at Langley lasted into the 1970s, but NASA calls those years the dwindling days of human computing, as electronic computers became part of everyday work. The job of calculating by hand faded away. Many of the people found new work. Through the 1950s and 1960s, more and more of them worked their way out of the computer pool and into engineering. Others moved into programming. Not all of them, and not on equal terms.

**[08]**
Programming grew into a large occupation of its own. By 1988, computer programmers held five hundred nineteen thousand jobs in the United States. That count comes from another era, with different job definitions, so we will not set it beside today's numbers. In 1990, the government's job handbook looked ahead. Improved software, it said, would simplify or eliminate some programming tasks. And artificial intelligence would become just additional tools available to programmers.

**[09]**
The lamplighter walks on. The laboratory window goes dark; across the street, in an office tower, a light comes on. A software developer watches lines of code appear on a screen, written by a tool faster than anyone could type, and stops to check one.

**[10]**
Today, the third kind of work. The computer can help write the code. In 2025, BLS economists wrote that programming is one of the activities AI is well suited to augment. Software developers can use generative AI to develop, test, and document code, and to write user stories, short descriptions of what a feature should do for the people who use it. The economists called the effect on the occupation highly uncertain.

**[11]**
Here, two job titles that sound alike are heading in different directions. The first is computer programmers: people who write, modify, and test code. Their jobs are projected to shrink from 2025 to 2035. Programming work continues to be automated, BLS says, companies are expected to use technologies including AI, and some higher-skilled programming tasks will likely shift to other workers, such as software developers.

**[12]**
The second is software developers: the people who design applications and plan how the pieces fit together. Their jobs are projected to grow, from one point seven two million in 2025 to one point eight nine million in 2035. That is ten point two percent, compared with three point five percent for all jobs. BLS expects strong demand, driven in part by the continued expansion of software development for artificial intelligence. Put these sources together, and one reading is that the work is moving: less typing of every line, more deciding what to build, designing how it fits, and checking what the tool wrote. It is a reading, not a forecast. But checking the machine's numbers is an old job here.

**[13]**
What about the people just starting out? Economists at Stanford studied payroll records for millions of workers through June 2026. Overall employment is still robust. What they found is not a wave of layoffs. It is a gap. Employment of workers aged twenty-two to twenty-five in AI-exposed jobs, such as software development and customer service, now stands nineteen percent below where it would be had it kept pace with their less-exposed peers. Experienced workers show no comparable gap. And the gap comes mostly from fewer young people being hired, not from people being let go. The authors are careful: the hardest part, they write, is separating AI from everything else changing in the economy.

**[14]**
They raise one possibility: AI may be taking over the checkable, routine tasks that once justified hiring beginners. The technology is not the same as in 1947, but the pattern is familiar: a repetitive task goes to a machine, and people move to the work around it. One difference matters. Back then, the new machine needed new people to program it, so the change opened doors at the start of a career. This time, it shows up first at the bottom of the ladder. If the tools take on the simple tasks that beginners once learned on, where will the next beginners learn?

**[15]**
What happens to a job when a machine takes its name? Three times, the word computer meant different work: calculating by hand, programming the machine, and now working beside it. The arithmetic went to the machine, and many of the people moved on to the work around it. Now the machine can help write the code. The name stayed; the work moved on. Whether the newest workers can move on with it is the question this time.

**[16]**
Back on the street, the lamplighter reaches the last post. The glass opens, the flame takes, and the light passes on to the next corner, the way the work does. Every era has its last lamplighters. Some of them were called computers.

### Tỷ lệ theo khung kể (ước)
| Phần | Đoạn | Thời lượng | % |
|---|---|---|---|
| Mở | 00–01 | 59,5 s | 9,3 |
| Quá khứ | 02–04 | 130,1 s | 20,3 |
| Chuyển giao | 05–09 | 164,2 s | 25,7 |
| Hiện tại | 10–12 | 120,1 s | 18,8 |
| Tương lai | 13–14 | 100,4 s | 15,7 |
| Kết | 15–16 | 58,9 s | 9,2 |

**Lệch CHUAN-KENH §2** (đích theo trục cũ: STORY 20 / HISTORY 35 / TODAY 45):
- quy đổi STORY (00, 01, 09, 16) ≈ 17 %;
- HISTORY (02–08) ≈ 45 % (**+10 điểm**);
- TODAY (10–15) ≈ 38 % (**−7 điểm**).
Nguyên nhân: trục mới đặt "chuyển giao" (05–08) làm phần chính, mà phần này nằm trong thời lịch sử. CHUAN-KENH §12 đã ghi: đổi đích §2 chờ chủ dự án duyệt.

### Số trên hình và số neo (dự kiến cho đặc tả)
- **Số neo (3):**
  - `c46` about 400 (1946, NASA1);
  - `prog88` 519,000 (1988, OOH90);
  - `sd_chg` +10.2 % (dự báo 2025–35, OOHSD).
- **Số đi kèm trên hình:**
  - 5 → 75 (NASA1, isotype một phòng thí nghiệm);
  - 1.72 → 1.89 million (OOHSD, khung riêng, gốc dự báo);
  - +3.5 % toàn nền (EP);
  - −19 % (CAN, chú thích "gap vs. less-exposed peers, not job losses").
- **Ước Q17:** 9 số / 10,6 phút = 0,85 số/phút.
- **Bỏ khỏi lời:**
  - −7 % của computer programmers (lời chỉ nói "projected to shrink"; bớt số theo kiểm mù);
  - −11 % / +10 % của CAN;
  - +17,9 % (2023–33);
  - 1,69 / 1,96 triệu (2024–34).
- **Kiểm so sánh 6 điểm:**
  - Cặp duy nhất đặt cạnh nhau là +10,2 % ↔ +3,5 %: cùng BLS, cùng kỳ 2025–35, cùng loại dự báo → Đạt.
  - 519 000 (1988) **không** đặt cạnh số hôm nay. Lời §08 nói rõ lý do: khác thời, khác định nghĩa nghề.
  - Số Langley là số của một phòng thí nghiệm.
  - Điểm 5 ("not the same technology… the pattern is familiar" kèm khác biệt): §14.
  - Điểm 6: không so tốc độ.

## 4. Kiểm mù kịch bản (3 subagent Sonnet độc lập, đề bài giống nhau, chỉ đưa tệp lời)
**Câu hỏi mới: "Người xem rút ra thông điệp chính là gì?"**
- R1: "When a machine takes over a job's name and its routine tasks, the work usually shifts rather than vanishes… The ending adds a worry: beginners may lose the tasks they used to learn on."
- R2: "When machines take over a job's name and routine tasks, the people tend to move on to the work around the machine… But this time the change may hit beginners first."
- R3: "When a machine takes over a job's tasks, the job and its name fade, but the people move on to the work around it… The closing worry is whether today's beginners will still have a place to learn."
- **Kết luận:** thông điệp chính **đúng mạch biến đổi** ở cả 3 người; không ai rút ra "máy thay thế người". Giọng phim: 3/3 xếp loại (b). Móc câu được trả lời: Có / Một phần / Có.

**Điểm ≥ 2/3 và cách sửa** (bản trước sửa lưu trong scratchpad của phiên):
| # | Điểm | Số người | Sửa |
|---|---|---|---|
| 1 | "Ba loại việc" ở §00 không được nhắc lại, người nghe mất mạch | 3/3 | §00 đánh số First/Second/Third; §05 "the second kind of work"; §10 "the third kind of work"; §15 nhắc lại đủ ba |
| 2 | Ẩn dụ người thắp đèn khó hiểu khi nghe một lần | 3/3 | §01 thêm "Lamplighting is a job machines took over long ago. Tonight, it opens the story of another."; §16 "the light passes on…, the way the work does" |
| 3 | "programmers" và "software developers" nghe giống nhau, dễ lẫn bên giảm với bên tăng | 3/3 | §11–12 tách thành "two job titles that sound alike… The first… The second…"; bỏ đọc số −7 % |
| 4 | "Not the same technology as in 1947. The same pattern" cụt, khó nghe | 3/3 | viết thành câu đủ: "The technology is not the same as in 1947, but the pattern is familiar: …" |
| 5 | §12 "the work is moving" là suy luận của phim nhưng nghe như kết quả BLS | 3/3 | "Put these sources together, and one reading is… It is a reading, not a forecast." |
| 6 | −19 % dễ nghe thành 19 % người trẻ mất việc | 3/3 | thêm câu đặt **trước** số: "What they found is not a wave of layoffs. It is a gap." |
| 7 | §15 "the people went on" khái quát quá, như truyện thành công | 3/3 | "many of the people"; §07 thêm "Not all of them, and not on equal terms."; §15 kết bằng câu hỏi mở về người mới |
| 8 | Dày số ở §04, §08, §11–12 | 3/3 | bỏ "more than tripled its staff", bỏ đọc số −7 %; giữ 5/75/400, 519 000, 1,72 → 1,89 triệu, +10,2 % vs +3,5 % (số chủ dự án định) |
| 9 | 519 000 (1988) dễ bị so với số hôm nay | 2/3 | §08: "That count comes from another era, with different job definitions, so we will not set it beside today's numbers." |
- **Điểm 2/3 không sửa:** đoạn phân biệt chủng tộc "lạc đề" (R2, R3, mục "chán"). Đây là sự thật lịch sử chủ dự án yêu cầu giữ. P nối vào mạch bằng câu "The door did not open evenly." thay vì cắt.
- **Điểm 1/3 giữ nguyên:** "Checking the machine's numbers is an old job here" (R1 cho là tu từ). Câu này nối giai thoại 1962 với việc kiểm mã hôm nay. P giữ vì nó đặt sau câu "It is a reading, not a forecast."

## 5. Kiểm câu chữ với nguồn (các điểm cần chủ dự án biết)
- **"the first American orbital flight"** (§06): NASA3 ghi "MA-6, John Glenn's first U.S. orbital flight". Lời không nêu tên người, không nêu năm.
- **"The job of calculating by hand faded away"** (§07): diễn giải từ hai nguồn:
  - NASA3 "dwindling days of human computing";
  - NASA1 "into the 1970s".
- **"one reading is that the work is moving…"** (§12): diễn giải từ ba nguồn, đã gắn nhãn "a reading, not a forecast":
  - MLR25: develop/test/document, user stories;
  - OOHSD: nhiệm vụ thiết kế;
  - OOHCP: việc bậc cao chuyển sang developers.
- **Câu BLS nhu cầu AI** (§12): câu gốc nói về cả nhóm developers + QA + testers. Lời gắn với "BLS expects strong demand", không gắn với một con số.
- **Không dùng** kết quả "tự động hoá vs bổ trợ" của nghiên cứu Stanford, vì nó đo bằng Anthropic Economic Index (CHUAN-KENH §4).
- **§10 luật lời dẫn:** lời không nói phim làm bằng AI.

## 6. Hướng hình (tóm tắt, làm sau khi duyệt lời)
- **Cảnh đinh 3D (5):**
  1. phòng thí nghiệm bên sân bay lúc chạng vạng, ngọn lửa trao qua ô cửa (00/01/16);
  2. phòng tính toán 1940s: hàng bàn, máy tính cơ, phim áp kế, giấy kẻ ô (thay bàn làm việc 2D, BAI-HOC #78);
  3. phòng máy điện tử 1947 với băng đục lỗ;
  4. tháp văn phòng đêm, màn hình mã (09–10);
  5. cầu thang/bậc thang "bậc đầu" (14).
- **Tư liệu:** ảnh NASA tổ "computer" Langley/JPL, do NASA tạo, không logo, không hàm ý bảo trợ, ghi RIGHTS; tổng ≤ 20 %.
- **Âm thanh nghề mới:** tiếng máy tính cơ Friden, băng đục lỗ, bàn phím. Nhạc: nhạc hiệu + 3 cue theo hồi.

## 7. Token và giờ máy (đo từ log phiên)
| Bước | Sinh ra | Đầu vào mới (gồm ghi cache) | Đọc cache |
|---|---|---|---|
| P: đọc 8 tệp, tra nguồn, viết lời, sửa, báo cáo (đến lúc viết mục này) | ≈ 35 nghìn | ≈ 148 nghìn | ≈ 4,9 triệu |
| Kiểm mù 3 subagent Sonnet | — | ≈ 3 × 50 nghìn (theo thông báo tác vụ) | — |
- **Tổng đầu vào mới + sinh ra ≈ 0,33 triệu** (trần mềm 1,5 triệu/tập trọn).
- Giờ máy: không render; ElevenLabs: 0 ký tự.

## 8. Đang chờ chủ dự án
1. **Duyệt lời v2** (mục 3), hoặc chỉ đạo sửa.
2. **Chọn tiêu đề:** A, B hoặc C.
3. **Duyệt lệch tỷ lệ §2** theo trục mới, hoặc đặt đích mới cho khung 6 phần.
4. **(Tuỳ chọn)** Nhờ Claude (Cowork) đối chiếu nguyên văn OOH Computer Programmers. Lời hiện không đọc số của nguồn này.
5. G3 tập 6 v2 (đã chờ từ trước).

**Sau khi duyệt**, P sẽ: khoá lời → sửa `episode.yaml` (map, heroes, pause, sfx, frame0) → thu giọng → nháp 960×540 → Q14–Q31 + Q27/Q31 trên nháp → sửa → render 1080p một lần → **DỪNG ở G2**.
