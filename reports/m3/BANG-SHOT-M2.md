# BẢNG SHOT M2 — bảng chốt cho M2.1 (animatic nhịp) · "The Last Lamplighters"

Gói: M2.0 (e) do P giao. Nguồn: `reports/m3/KE-HOACH-TAP-THU.md` §1 (78 shot), được chủ dự án duyệt ngày 01/10/2026 (AUTHORSHIP, mục "Last Lamplighters (Mốc 2)"). Kịch bản: `reports/m3/KICH-BAN-TAP-THU-V2.md`. Trạng thái: **chốt cho M2.1**. Chỉ văn bản: không render, không commit, không gọi API tính phí.

## 1. Thay đổi so với KE-HOACH §1, theo quyết định 01/10/2026

1. **s22 (shot 05-08):** dùng bản B3 v2. Ánh điện đến từ cột mé đối diện, ngoài khung (x = 29, z = +3,9 theo THU-PHONG-CACH-V2), có đổ bóng. **Không có cột điện trong khung.** Luật này áp luôn cho 06-05 (ánh s27).
2. **Tấm chữ 3 cột (T3C):** mẫu rút gọn gồm 1 tiêu đề, 1 số lớn hoặc dòng chính, và tối đa 3 cột. Áp cho:
   - 02-04: 1807 · 1812 · 1813 (thay dòng thời gian);
   - 08-07: 40,000 · ~1,100 · 5 (thay thẻ số).
   Thẻ số, thẻ nguồn và biểu đồ khác giữ nguyên quy cách mục 2 của KE-HOACH.
3. **Thứ tự shot sắp lại để hình khớp câu lời dẫn.** Không đổi thời lượng đoạn, không đổi tổng.
   - **Đoạn 03:** cảnh vòng tắt đèn lúc bình minh lên vị trí 03-04, ngay sau câu "…at dawn". Lau kính thành 03-05, sương mưa thành 03-06.
   - **Đoạn 05:**
     - đồ hoạ Opéra và Broadway lên ngay sau cặp đồng hồ 8:00 / 7:53;
     - cảnh truyện theo sau;
     - 05-10 dùng **s09w (7:53)** thay s06 (7:31) để giờ trên hình chỉ tiến (luật Cổng 5 v2).
   - **Đoạn 14:** thẻ 4 số neo lên 14-01, đi cùng câu "Forty thousand lamps became…". Toàn cảnh thành phố thành 14-02.
4. **Nhạc:** cột ghi chú chỉ ghi "nhạc" ở chỗ cần nhạc. Nhạc là **CC0/CC BY do người làm, không dùng nhạc AI**. Bản animatic M2.1 để trống nhạc hoặc dùng nhạc tạm đã có giấy phép. Không dùng C4-M1 (ACE-Step).
5. **Lời dẫn nháp nhịp:** đọc bằng `flite` (bộ lọc ffmpeg), chỉnh về 150 từ/phút bằng `sox`. Thu ElevenLabs Starter chỉ sau khi nhịp đã duyệt. **Master để ngoài git** (thử GitHub Release).

## 2. Quy ước cột
- **Loại:** R là shot Last Round dùng lại; A là tài sản dùng lại, dàn dựng mới; N là mới. "+ B3" là bật cờ hậu kỳ B3 (cắt giấy / bóng).
- **Mẫu dữ liệu:**
  - D-MAP: bản đồ;
  - D-BAR: cột;
  - D-TL: dòng thời gian;
  - D-NUM: thẻ số;
  - D-SRC: thẻ nguồn;
  - D-GRID: lưới đơn vị;
  - **T3C: tấm chữ 3 cột**.
- **Thời điểm:** giây, cộng dồn từ 0 trên bản có đoạn 07. "Lời đầu shot" là vài từ đầu của câu lời dẫn bắt đầu trong shot; "(tiếp)" nghĩa là câu trước còn chạy sang shot này.
- **Mặt người:** không cận mặt. Insert chỉ quay vật hoặc bàn tay.

## 3. Bảng shot (78 shot · 571 s = 9:31)

| Mã | Đoạn | Nhãn | t0–t1 (s) | Cỡ | Nguồn hình | Lời đầu shot | Ghi chú dựng | s |
|---|---|---|---|---|---|---|---|---|
| **01** | **Cold open** | **STORY** | | | | | | |
| 01-01 | 01 | STORY | 0–7 | EWS | R · s01 + B3 | "Every evening, for a little…" (VO vào ở +2 s) | giữ khung lâu hơn bản gốc | 7 |
| 01-02 | 01 | STORY | 7–13 | WS | R · s02 + B3 | (tiếp) "…walked out at dusk…" | — | 6 |
| 01-03 | 01 | STORY | 13–18 | WS 3/4 thấp | R · s03 + B3 (B3_CAM) | (tiếp) "…gave the street its night." | bắt lửa 0,3–0,5 s (B3 v2) | 5 |
| 01-04 | 01 | STORY | 18–23 | MS nghiêng, bóng | R · s05 + B3 (B3_CAM profile) | — (IDA L1 "Evening, old street.") | take C4-D1 L1; VO nghỉ | 5 |
| 01-05 | 01 | STORY | 23–27 | WS | R · s04 + B3 | "Ida isn't real." | bóng người + thang trên tường | 4 |
| 01-06 | 01 | STORY | 27–33 | WS | R · s07 + B3 | "But her job was real…" | — | 6 |
| 01-07 | 01 | STORY | 33–39 | WS tele | A · s08 + bóng Cas (s24c) + B3 | "This is a story about that job…" | Cas chỉ là bóng xa | 6 |
| 01-08 | 01 | STORY | 39–45 | EWS đẩy chậm | A · set s01/s43 + B3, giờ chạng vạng | "And at the end, a question…" | chừa chỗ cho thẻ tựa | 6 |
| **02** | **Pall Mall 1807** | **DATA** | | | | | | |
| 02-01 | 02 | DATA | 45–51 | đồ hoạ | N · mới: thẻ tựa (nền data_frame b3) | "Our story starts in London…" (+3 s) | THE LAST LAMPLIGHTERS | 6 |
| 02-02 | 02 | DATA | 51–61 | D-MAP | N · mẫu bản đồ: London | "An inventor named Frederick Winsor…" | "Pall Mall · 1807" (D1) | 10 |
| 02-03 | 02 | DATA | 61–67 | WS minh hoạ | N · mới: bóng đám đông cắt giấy | "People came out just to stare…" | Illustrative | 6 |
| 02-04 | 02 | DATA | 67–76 | T3C | N · mẫu tấm chữ 3 cột | "In 1812 the world's first gas company…" | 3 cột: 1807 · 1812 · 1813 (D1–D3) | 9 |
| 02-05 | 02 | DATA | 76–88 | D-MAP | N · mẫu bản đồ: London (02-02) | "And then the thing spread…" | bộ đếm 40,000; "1820s · 215 miles" (D4) | 12 |
| 02-06 | 02 | DATA | 88–95 | D-NUM | N · mẫu thẻ số | "Forty thousand. Hold on to that number…" | 40,000+; nguồn English Heritage | 7 |
| 02-07 | 02 | DATA | 95–101 | MS | A · đèn khí + bóng Ida đi (lp20) + B3 | "Forty thousand lamps don't light themselves." | — | 6 |
| **03** | **The round** | **STORY+DATA** | | | | | | |
| 03-01 | 03 | STORY+DATA | 101–107 | MS sau-phải | R · s03 + B3, máy mới | "A lamplighter's evening was called a round." | tay, van, sào; không mặt | 6 |
| 03-02 | 03 | STORY+DATA | 107–112 | MS, bóng | R · s24 + B3, máy nghiêng | "You lit dozens of lamps at dusk…" | phải đổi máy: s24 gốc lộ mặt | 5 |
| 03-03 | 03 | STORY+DATA | 112–120 | D-MAP lồng góc | N · mẫu bản đồ: tuyến đèn, nền s07 | (tiếp) "…along a fixed route…" | Illustrative, không ghi số (D5) | 8 |
| 03-04 | 03 | STORY+DATA | 120–126 | WS | A · s40 + B3, màu bình minh | (tiếp) "…at dawn to put them out." | đổi chỗ với KE-HOACH 03-06 để khớp lời | 6 |
| 03-05 | 03 | STORY+DATA | 126–131 | Insert tay | A · đèn khí + rig tay Ida + B3 | "In between, the job was more than fire." | tư thế lau kính (mới) | 5 |
| 03-06 | 03 | STORY+DATA | 131–138 | WS | A · set phố s07 + B3 + lớp sương/mưa | "Rain, fog, frost: it didn't matter." | — | 7 |
| 03-07 | 03 | STORY+DATA | 138–146 | EWS | A · set s01 + bóng vô danh nhân bản (rig Ida) + B3 | "Forty thousand lamps meant a small army…" | Illustrative | 8 |
| **04** | **Across the ocean** | **DATA** | | | | | | |
| 04-01 | 04 | DATA | 146–154 | D-MAP | N · mẫu bản đồ: Đại Tây Dương | "The idea crossed the Atlantic fast." | "1816 · Peale's museum" (D7) | 8 |
| 04-02 | 04 | DATA | 154–160 | WS minh hoạ | N · mới: mặt tiền bảo tàng Peale | (tiếp) "…lit a room of his Baltimore museum…" | — | 6 |
| 04-03 | 04 | DATA | 160–167 | WS | A · đèn khí + mặt phố Market St (mới) + B3 | "Within a year, on the seventh of February 1817…" | "Feb 7, 1817 · first U.S. public gas street lamp" (D6) | 7 |
| 04-04 | 04 | DATA | 167–174 | D-MAP | N · mẫu bản đồ: Đại Tây Dương (04-01) | "Paris took its time…" | "Paris · mid-1800s" ([16]; chưa có D#) | 7 |
| **05** | **The white wave** | **STORY+DATA** | | | | | | |
| 05-01 | 05 | STORY+DATA | 174–179 | MS | R · s09 + B3 | "Then came a different kind of light." (+2 s) | đồng hồ quảng trường 8:00, chuông | 5 |
| 05-02 | 05 | STORY+DATA | 179–183 | Insert | R · s09w + B3 | (tiếp) | đồng hồ bỏ túi 7:53; giờ chỉ tiến | 4 |
| 05-03 | 05 | STORY+DATA | 183–193 | D-MAP | N · mẫu bản đồ: Opéra 1878 | "In 1878, for the World's Fair…" | 64 chấm trắng (D8) | 10 |
| 05-04 | 05 | STORY+DATA | 193–200 | D-MAP | N · mẫu bản đồ: Broadway 1880 | "Two years later, in 1880…" | một hàng chấm trắng (D9) | 7 |
| 05-05 | 05 | STORY+DATA | 200–204 | MS (đèn) | R · s10e + B3 | "At first, gas held on." | bóng điện nháy hai lần | 4 |
| 05-06 | 05 | STORY+DATA | 204–210 | EWS | R · s10 + B3 | (tiếp) "Electricity was new, expensive…" | sóng trắng xuống dốc | 6 |
| 05-07 | 05 | STORY+DATA | 210–216 | WS | R · s19 + B3 | "But each white lamp that went up…" | L8 nở hổ phách rồi bị phủ trắng | 6 |
| 05-08 | 05 | STORY+DATA | 216–221 | MWS thấp | R · s22 + B3 v2 | — (IDA L2 "Not yet… not yet.") | **ánh điện từ cột mé đối diện (ngoài khung), đổ bóng; không có cột điện trong khung**; VO nghỉ | 5 |
| 05-09 | 05 | STORY+DATA | 221–227 | WS qua vai | R · s12 + B3 | "It was a slow tide, not a single night…" | — | 6 |
| 05-10 | 05 | STORY+DATA | 227–232 | Insert | R · s09w + B3, cắt khung khác | "Ida's watch runs seven minutes slow…" | giữ 7:53; không dùng s06 (7:31) để giờ không lùi | 5 |
| 05-11 | 05 | STORY+DATA | 232–237 | WS | R · s15 + B3 | "That's the feeling we wanted…" | — | 5 |
| **06** | **New York 1907** | **DATA** | | | | | | |
| 06-01 | 06 | DATA | 237–247 | D-MAP | N · mẫu bản đồ: Manhattan | "In April 1907, New York's lamplighters…" | mảng tối Illustrative (D10) | 10 |
| 06-02 | 06 | DATA | 247–255 | đồ hoạ | N · mới: trang báo vẽ lại | "The next morning's papers reported…" | tiêu đề diễn đạt lại; nguồn LOC | 8 |
| 06-03 | 06 | DATA | 255–263 | EWS | N · mới: bóng cảnh sát; set phố + đèn khí + B3 | "Police officers were sent out…" | que diêm loé | 8 |
| 06-04 | 06 | DATA | 263–270 | WS | N · mới: bóng đám đông; set phố + B3 | "Within about a week, the men were back…" | — | 7 |
| 06-05 | 06 | DATA | 270–278 | WS | A · set phố + ánh điện s27 + B3 | "But the strike made something plain." | không có cột điện trong khung (luật s27) | 8 |
| **07** | **The great switch-off** | **DATA** | | | | | | |
| **[CẮT-07]** 07-01 | 07 | DATA | 278–292 | D-TL | N · mẫu dòng thời gian | "Over the next half century…" | NY 2 lampposts (D13); Paris 1962 (D12, yếu) | 14 |
| **[CẮT-07]** 07-02 | 07 | DATA | 292–301 | D-BAR | N · mẫu cột | "And London, where it all began…" | 40,000 cạnh ~1,100, cùng thang (D4, D14) | 9 |
| **[CẮT-07]** 07-03 | 07 | DATA | 301–305 | D-MAP | N · mẫu bản đồ: London (02-02) | "London did something unusual. It kept some." | lùi xa, vài đốm hổ phách | 4 |
| **08** | **London's last lamplighters** | **SHORTS** | | | | | | |
| 08-01 | 08 | SHORTS | 305–312 | EWS 2.5D | N · mới: set Covent Garden + đèn khí + B3 | "Here's the part most people don't know." | không logo, không biển thật | 7 |
| 08-02 | 08 | SHORTS | 312–319 | D-NUM | N · mẫu thẻ số | "In 2015, there were about fifteen hundred…" | ~1,500 (2015) → ~1,100 (2023) (D14) | 7 |
| 08-03 | 08 | SHORTS | 319–326 | WS, bóng | N · mới: bóng người thắp đèn hiện đại + B3 | "By British Gas's own count in 2023…" | hư cấu | 7 |
| 08-04 | 08 | SHORTS | 326–332 | D-NUM | N · mẫu thẻ số | "And that team is five people." | **5 lamplighters** (D15) | 6 |
| 08-05 | 08 | SHORTS | 332–339 | Insert vật | N · mới: cơ cấu đồng hồ trong đèn | "They don't carry fire anymore." | "wound every 2 weeks" (D16) | 7 |
| 08-06 | 08 | SHORTS | 339–347 | WS | N · set Covent Garden (08-01) + B3 | "When Westminster proposed swapping…" | 2022 LED; Grade II 2024 (D17, D18) | 8 |
| 08-07 | 08 | SHORTS | 347–354 | T3C | N · mẫu tấm chữ 3 cột | "Forty thousand lamps, once." | 3 cột: 40,000 · ~1,100 · 5 | 7 |
| **10** | **The last lamp** | **STORY** | | | | | | |
| 10-01 | 10 | STORY | 354–360 | WS | R · s35 + B3 | "We gave Ida an ending…" | — | 6 |
| 10-02 | 10 | STORY | 360–366 | WS ngược sáng | R · s37w + B3 | "For the real ones, it was a new contract…" | bỏ thoại L4 | 6 |
| 10-03 | 10 | STORY | 366–370 | MS sau lưng | R · s38 + B3, máy mới | (tiếp) "History doesn't record…" | phải đổi máy: s38 gốc lộ mặt Cas | 4 |
| 10-04 | 10 | STORY | 370–375 | Insert tay | R · s40 + B3 | — (nhịp lặng) | lặng 10–12 s gồm 10-04 và 10-05 | 5 |
| 10-05 | 10 | STORY | 375–381 | WS | R · s40w + B3 | — | — | 6 |
| 10-06 | 10 | STORY | 381–386 | WS | R · s41 + B3 | "What Ida keeps isn't the job." | trao đèn lồng | 5 |
| 10-07 | 10 | STORY | 386–392 | WS → MS | R · s42b + s42 + B3 | "Cas will never light a street." | hơ tay ba nhịp | 6 |
| 10-08 | 10 | STORY | 392–398 | EWS | R · s43 + B3 | "But he knows how to warm his hands…" | một ô cửa vàng | 6 |
| 10-09 | 10 | STORY | 398–403 | Insert | R · s46 + B3 | — | 9:53 → 10:00, không gõ kính | 5 |
| 10-10 | 10 | STORY | 403–406 | WS | R · s48 + B3 | — | chim bóng; nhạc | 3 |
| **11** | **One job in 270** | **DATA** | | | | | | |
| 11-01 | 11 | DATA | 406–410 | đồ hoạ | N · mới: chuyển đèn → ô lưới | "Lamplighting was an extreme case…" | — | 4 |
| 11-02 | 11 | DATA | 410–422 | D-GRID | N · mẫu lưới đơn vị | "The economist James Bessen took…" | "1950 U.S. Census → 2010" (D21) | 12 |
| 11-03 | 11 | DATA | 422–430 | D-GRID | N · mẫu lưới đơn vị (11-02) | "Plenty disappeared…" | một ô tắt: thang máy | 8 |
| 11-04 | 11 | DATA | 430–440 | D-NUM | N · mẫu thẻ số | "One in two hundred and seventy." | **1 in 270**; nguồn ghi 271 nghề | 10 |
| **12** | **Today's shortest rounds** | **SHORTS** | | | | | | |
| 12-01 | 12 | SHORTS | 440–447 | D-NUM | N · mẫu thẻ số | "So who is on that list today?" | **−34%** trong 5 s đầu (D23) | 7 |
| 12-02 | 12 | SHORTS | 447–469 | D-BAR | N · mẫu cột (cột đèn) | "Every year, the U.S. Bureau of Labor Statistics…" | 5 nghề, cùng thang, nhãn 2025–35 (D23–D27) | 22 |
| 12-03 | 12 | SHORTS | 469–477 | D-BAR | N · mẫu cột (12-02) | "Then telephone operators…" | ~3,500 jobs (2025) (D24) | 8 |
| 12-04 | 12 | SHORTS | 477–487 | D-SRC | N · mẫu thẻ nguồn | "What they share…" | "Forecasts, not verdicts"; BLS Table 1.5 | 10 |
| **13** | **AI in the forecast** | **DATA** | | | | | | |
| 13-01 | 13 | DATA | 487–502 | D-BAR | N · mẫu cột | "In an earlier round, for 2023 to 2033…" | nhãn **2023–33** (D32–D35) | 15 |
| 13-02 | 13 | DATA | 502–514 | D-BAR | N · mẫu cột | "And the newest list has fast-growing jobs…" | nhãn **2025–35**, khung riêng (D30) | 12 |
| 13-03 | 13 | DATA | 514–530 | D-BAR | N · mẫu cột (thanh ngang) | "One early warning." | "~19% below expected"; không in 81 (D36) | 16 |
| 13-04 | 13 | DATA | 530–538 | D-SRC | N · mẫu thẻ nguồn | "The researchers call it an early signal…" | Stanford DEL 8/2026; BLS MLR 2/2025 | 8 |
| **14** | **The question** | **STORY+DATA** | | | | | | |
| 14-01 | 14 | STORY+DATA | 538–546 | D-NUM xếp dọc | N · mẫu thẻ số | "Forty thousand lamps became about eleven hundred…" | 4 số neo; đổi chỗ với KE-HOACH 14-02 để khớp lời | 8 |
| 14-02 | 14 | STORY+DATA | 546–555 | EWS | A · set s43/s01 + lớp thành phố hiện đại (mới) + B3 | "Some jobs end. Most change." | một ô hổ phách | 9 |
| 14-03 | 14 | STORY+DATA | 555–561 | WS xa | R · s44 + B3 | (IDA L1 off, distant) rồi "So, the question…" | take C4-D1 L1 xử lý xa | 6 |
| 14-04 | 14 | STORY+DATA | 561–571 | đồ hoạ | N · mới: thẻ kết kênh | "Who are the last lamplighters of our time?" | khẩu hiệu | 10 |

**Cộng theo đoạn (s):**

| Đoạn | 01 | 02 | 03 | 04 | 05 | 06 | 07 | 08 | 10 | 11 | 12 | 13 | 14 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| s | 45 | 56 | 45 | 28 | 63 | 41 | 27 | 49 | 52 | 34 | 47 | 51 | 33 |

**Cộng theo loại:** R 148 s (28 shot) · A 68 s (10 shot) · N 355 s (40 shot). Dùng lại 216 s, tức 38 %.

## 4. Đoạn 07 (cắt nếu animatic > 10:00)

**Các shot của đoạn 07** (đánh dấu **[CẮT-07]** trong bảng):

| Mã | Mẫu | Thời điểm (s) | Dài (s) |
|---|---|---|---|
| 07-01 | D-TL | 278–292 | 14 |
| 07-02 | D-BAR | 292–301 | 9 |
| 07-03 | D-MAP | 301–305 | 4 |

**Tổng thời lượng**

| Bản | Số shot | Thời lượng |
|---|---|---|
| Có đoạn 07 | 78 | 571 s = **9:31** (cách trần 10:00 là 4,8 %, trong vùng ±5 %) |
| Không có đoạn 07 | 75 | 544 s = **9:04** |

**Khi cắt đoạn 07**
- Mọi shot từ 08-01 trở đi lùi 27 s, tức t0 và t1 trừ 27.
- Đoạn 06 kết bằng câu "…a little more without them" rồi vào thẳng 08, "Here's the part most people don't know." Hai câu nối được, không cần sửa lời.
- **Mất hai thứ:** cột so sánh 40,000 với ~1,100 (07-02), và hai số D12, D13.
- Số neo 40,000 vẫn được nhắc đủ 3 lần nhờ 02-05, 02-06, 08-07 và 14-01.

**Ba đoạn không còn giây dư** (đo ở 150 từ/phút, phải đo lại trong M2.1):
- đoạn 05: 58 s lời dẫn, cộng 3 s cho câu L2 của Ida, cộng 2 s đầu đoạn;
- đoạn 08: 49 s;
- đoạn 13: 51 s.

Nếu một đoạn thiếu giờ: kéo dài shot dữ liệu của chính đoạn đó, không cắt lời. Rồi xem tổng; nếu tổng > 10:00 thì cắt đoạn 07.

## 5. Tài sản phải dựng mới cho M2.1, theo thứ tự làm

**Mức animatic:** khung tĩnh hoặc khối thô, đủ để đọc nhịp. Bản hoàn chỉnh làm ở M2.2.

| # | Tài sản | Dùng ở | Vì sao ở thứ tự này |
|---|---|---|---|
| 0 | Nháp lời dẫn `flite` (150 từ/phút) + `X.script.txt` mỗi câu một dòng | mọi shot | cần để đo nhịp trước mọi thứ |
| 1 | Mẫu **D-NUM**, **T3C**, **D-SRC** (khung tĩnh) | 02-04, 02-06, 08-02, 08-04, 08-07, 11-04, 12-01, 12-04, 13-04, 14-01 | rẻ, phủ nhiều shot nhất |
| 2 | **D-MAP London** (Pall Mall, mạng phố, bộ đếm) | 02-02, 02-05, 07-03; nền tuyến đèn cho 03-03 | số neo đầu tiên |
| 3 | **D-BAR** (cột đèn, cùng thang; thanh ngang) | 07-02, 12-02, 12-03, 13-01, 13-02, 13-03 | hai đoạn 12–13 dài nhất phần kết |
| 4 | **D-GRID** 270 ô biểu tượng nghề | 11-02, 11-03 (11-01 chuyển cảnh) | — |
| 5 | **D-MAP Đại Tây Dương**, **Opéra / Broadway**, **Manhattan** | 04-01, 04-04, 05-03, 05-04, 06-01 | dùng chung khung bản đồ của #2 |
| 6 | **D-TL** | 07-01 | đoạn có thể cắt nên làm sau |
| 7 | Thẻ tựa, thẻ kết | 02-01, 14-04 | — |
| 8 | Trang báo vẽ lại (tiêu đề diễn đạt lại) | 06-02 | — |
| 9 | **Bộ bóng người cắt giấy:** đám đông, cảnh sát đội mũ, người thắp đèn hiện đại (áo phản quang, thang nhôm); nhân bản bóng vô danh từ rig Ida | 02-03, 03-07, 06-03, 06-04, 08-03 | cần trước set Covent Garden |
| 10 | **Set Covent Garden** (đèn khí giữa đèn LED, mặt tiền nhà hát) + **cơ cấu đồng hồ trong đèn** | 08-01, 08-05, 08-06 | lõi của Short S1 |
| 11 | Mặt tiền bảo tàng Peale, mặt phố Market St | 04-02, 04-03 | — |
| 12 | Lớp thành phố hiện đại (màn hình, cửa sổ văn phòng) | 14-02 | — |
| 13 | Lớp sương / mưa; màu bình minh; tư thế lau kính | 03-04, 03-05, 03-06 | chỉnh nhỏ trên set có sẵn |
| 14 | Máy mới cho shot lộ mặt (s24, s38, s03 sau-phải) | 03-01, 03-02, 10-03 | đặt máy, không dựng tài sản |

**Phụ thuộc:** các shot R và A chờ lượt B3 v2 được duyệt (ánh sáng bám nguồn, viền sáng, s22). Mục 0–8 không phụ thuộc B3 v2 nên làm trước.

## 6. Khối máy đọc

Mỗi shot một dòng.
- `loai` là nhãn đoạn STORY / DATA / SHORTS.
- `nguon` là R/A/N kèm nguồn hình.
- `cat07` = true cho shot thuộc đoạn 07.

```json
[
{"id": "01-01", "t0": 0, "t1": 7, "loai": "STORY", "nguon": "R · s01 + B3", "cat07": false},
{"id": "01-02", "t0": 7, "t1": 13, "loai": "STORY", "nguon": "R · s02 + B3", "cat07": false},
{"id": "01-03", "t0": 13, "t1": 18, "loai": "STORY", "nguon": "R · s03 + B3 (B3_CAM)", "cat07": false},
{"id": "01-04", "t0": 18, "t1": 23, "loai": "STORY", "nguon": "R · s05 + B3 (B3_CAM profile)", "cat07": false},
{"id": "01-05", "t0": 23, "t1": 27, "loai": "STORY", "nguon": "R · s04 + B3", "cat07": false},
{"id": "01-06", "t0": 27, "t1": 33, "loai": "STORY", "nguon": "R · s07 + B3", "cat07": false},
{"id": "01-07", "t0": 33, "t1": 39, "loai": "STORY", "nguon": "A · s08 + bóng Cas (s24c) + B3", "cat07": false},
{"id": "01-08", "t0": 39, "t1": 45, "loai": "STORY", "nguon": "A · set s01/s43 + B3, giờ chạng vạng", "cat07": false},
{"id": "02-01", "t0": 45, "t1": 51, "loai": "DATA", "nguon": "N · mới: thẻ tựa (nền data_frame b3)", "cat07": false},
{"id": "02-02", "t0": 51, "t1": 61, "loai": "DATA", "nguon": "N · mẫu bản đồ: London", "cat07": false},
{"id": "02-03", "t0": 61, "t1": 67, "loai": "DATA", "nguon": "N · mới: bóng đám đông cắt giấy", "cat07": false},
{"id": "02-04", "t0": 67, "t1": 76, "loai": "DATA", "nguon": "N · mẫu tấm chữ 3 cột", "cat07": false},
{"id": "02-05", "t0": 76, "t1": 88, "loai": "DATA", "nguon": "N · mẫu bản đồ: London (02-02)", "cat07": false},
{"id": "02-06", "t0": 88, "t1": 95, "loai": "DATA", "nguon": "N · mẫu thẻ số", "cat07": false},
{"id": "02-07", "t0": 95, "t1": 101, "loai": "DATA", "nguon": "A · đèn khí + bóng Ida đi (lp20) + B3", "cat07": false},
{"id": "03-01", "t0": 101, "t1": 107, "loai": "STORY+DATA", "nguon": "R · s03 + B3, máy mới", "cat07": false},
{"id": "03-02", "t0": 107, "t1": 112, "loai": "STORY+DATA", "nguon": "R · s24 + B3, máy nghiêng", "cat07": false},
{"id": "03-03", "t0": 112, "t1": 120, "loai": "STORY+DATA", "nguon": "N · mẫu bản đồ: tuyến đèn, nền s07", "cat07": false},
{"id": "03-04", "t0": 120, "t1": 126, "loai": "STORY+DATA", "nguon": "A · s40 + B3, màu bình minh", "cat07": false},
{"id": "03-05", "t0": 126, "t1": 131, "loai": "STORY+DATA", "nguon": "A · đèn khí + rig tay Ida + B3", "cat07": false},
{"id": "03-06", "t0": 131, "t1": 138, "loai": "STORY+DATA", "nguon": "A · set phố s07 + B3 + lớp sương/mưa", "cat07": false},
{"id": "03-07", "t0": 138, "t1": 146, "loai": "STORY+DATA", "nguon": "A · set s01 + bóng vô danh nhân bản (rig Ida) + B3", "cat07": false},
{"id": "04-01", "t0": 146, "t1": 154, "loai": "DATA", "nguon": "N · mẫu bản đồ: Đại Tây Dương", "cat07": false},
{"id": "04-02", "t0": 154, "t1": 160, "loai": "DATA", "nguon": "N · mới: mặt tiền bảo tàng Peale", "cat07": false},
{"id": "04-03", "t0": 160, "t1": 167, "loai": "DATA", "nguon": "A · đèn khí + mặt phố Market St (mới) + B3", "cat07": false},
{"id": "04-04", "t0": 167, "t1": 174, "loai": "DATA", "nguon": "N · mẫu bản đồ: Đại Tây Dương (04-01)", "cat07": false},
{"id": "05-01", "t0": 174, "t1": 179, "loai": "STORY+DATA", "nguon": "R · s09 + B3", "cat07": false},
{"id": "05-02", "t0": 179, "t1": 183, "loai": "STORY+DATA", "nguon": "R · s09w + B3", "cat07": false},
{"id": "05-03", "t0": 183, "t1": 193, "loai": "STORY+DATA", "nguon": "N · mẫu bản đồ: Opéra 1878", "cat07": false},
{"id": "05-04", "t0": 193, "t1": 200, "loai": "STORY+DATA", "nguon": "N · mẫu bản đồ: Broadway 1880", "cat07": false},
{"id": "05-05", "t0": 200, "t1": 204, "loai": "STORY+DATA", "nguon": "R · s10e + B3", "cat07": false},
{"id": "05-06", "t0": 204, "t1": 210, "loai": "STORY+DATA", "nguon": "R · s10 + B3", "cat07": false},
{"id": "05-07", "t0": 210, "t1": 216, "loai": "STORY+DATA", "nguon": "R · s19 + B3", "cat07": false},
{"id": "05-08", "t0": 216, "t1": 221, "loai": "STORY+DATA", "nguon": "R · s22 + B3 v2", "cat07": false},
{"id": "05-09", "t0": 221, "t1": 227, "loai": "STORY+DATA", "nguon": "R · s12 + B3", "cat07": false},
{"id": "05-10", "t0": 227, "t1": 232, "loai": "STORY+DATA", "nguon": "R · s09w + B3, cắt khung khác", "cat07": false},
{"id": "05-11", "t0": 232, "t1": 237, "loai": "STORY+DATA", "nguon": "R · s15 + B3", "cat07": false},
{"id": "06-01", "t0": 237, "t1": 247, "loai": "DATA", "nguon": "N · mẫu bản đồ: Manhattan", "cat07": false},
{"id": "06-02", "t0": 247, "t1": 255, "loai": "DATA", "nguon": "N · mới: trang báo vẽ lại", "cat07": false},
{"id": "06-03", "t0": 255, "t1": 263, "loai": "DATA", "nguon": "N · mới: bóng cảnh sát; set phố + đèn khí + B3", "cat07": false},
{"id": "06-04", "t0": 263, "t1": 270, "loai": "DATA", "nguon": "N · mới: bóng đám đông; set phố + B3", "cat07": false},
{"id": "06-05", "t0": 270, "t1": 278, "loai": "DATA", "nguon": "A · set phố + ánh điện s27 + B3", "cat07": false},
{"id": "07-01", "t0": 278, "t1": 292, "loai": "DATA", "nguon": "N · mẫu dòng thời gian", "cat07": true},
{"id": "07-02", "t0": 292, "t1": 301, "loai": "DATA", "nguon": "N · mẫu cột", "cat07": true},
{"id": "07-03", "t0": 301, "t1": 305, "loai": "DATA", "nguon": "N · mẫu bản đồ: London (02-02)", "cat07": true},
{"id": "08-01", "t0": 305, "t1": 312, "loai": "SHORTS", "nguon": "N · mới: set Covent Garden + đèn khí + B3", "cat07": false},
{"id": "08-02", "t0": 312, "t1": 319, "loai": "SHORTS", "nguon": "N · mẫu thẻ số", "cat07": false},
{"id": "08-03", "t0": 319, "t1": 326, "loai": "SHORTS", "nguon": "N · mới: bóng người thắp đèn hiện đại + B3", "cat07": false},
{"id": "08-04", "t0": 326, "t1": 332, "loai": "SHORTS", "nguon": "N · mẫu thẻ số", "cat07": false},
{"id": "08-05", "t0": 332, "t1": 339, "loai": "SHORTS", "nguon": "N · mới: cơ cấu đồng hồ trong đèn", "cat07": false},
{"id": "08-06", "t0": 339, "t1": 347, "loai": "SHORTS", "nguon": "N · set Covent Garden (08-01) + B3", "cat07": false},
{"id": "08-07", "t0": 347, "t1": 354, "loai": "SHORTS", "nguon": "N · mẫu tấm chữ 3 cột", "cat07": false},
{"id": "10-01", "t0": 354, "t1": 360, "loai": "STORY", "nguon": "R · s35 + B3", "cat07": false},
{"id": "10-02", "t0": 360, "t1": 366, "loai": "STORY", "nguon": "R · s37w + B3", "cat07": false},
{"id": "10-03", "t0": 366, "t1": 370, "loai": "STORY", "nguon": "R · s38 + B3, máy mới", "cat07": false},
{"id": "10-04", "t0": 370, "t1": 375, "loai": "STORY", "nguon": "R · s40 + B3", "cat07": false},
{"id": "10-05", "t0": 375, "t1": 381, "loai": "STORY", "nguon": "R · s40w + B3", "cat07": false},
{"id": "10-06", "t0": 381, "t1": 386, "loai": "STORY", "nguon": "R · s41 + B3", "cat07": false},
{"id": "10-07", "t0": 386, "t1": 392, "loai": "STORY", "nguon": "R · s42b + s42 + B3", "cat07": false},
{"id": "10-08", "t0": 392, "t1": 398, "loai": "STORY", "nguon": "R · s43 + B3", "cat07": false},
{"id": "10-09", "t0": 398, "t1": 403, "loai": "STORY", "nguon": "R · s46 + B3", "cat07": false},
{"id": "10-10", "t0": 403, "t1": 406, "loai": "STORY", "nguon": "R · s48 + B3", "cat07": false},
{"id": "11-01", "t0": 406, "t1": 410, "loai": "DATA", "nguon": "N · mới: chuyển đèn → ô lưới", "cat07": false},
{"id": "11-02", "t0": 410, "t1": 422, "loai": "DATA", "nguon": "N · mẫu lưới đơn vị", "cat07": false},
{"id": "11-03", "t0": 422, "t1": 430, "loai": "DATA", "nguon": "N · mẫu lưới đơn vị (11-02)", "cat07": false},
{"id": "11-04", "t0": 430, "t1": 440, "loai": "DATA", "nguon": "N · mẫu thẻ số", "cat07": false},
{"id": "12-01", "t0": 440, "t1": 447, "loai": "SHORTS", "nguon": "N · mẫu thẻ số", "cat07": false},
{"id": "12-02", "t0": 447, "t1": 469, "loai": "SHORTS", "nguon": "N · mẫu cột (cột đèn)", "cat07": false},
{"id": "12-03", "t0": 469, "t1": 477, "loai": "SHORTS", "nguon": "N · mẫu cột (12-02)", "cat07": false},
{"id": "12-04", "t0": 477, "t1": 487, "loai": "SHORTS", "nguon": "N · mẫu thẻ nguồn", "cat07": false},
{"id": "13-01", "t0": 487, "t1": 502, "loai": "DATA", "nguon": "N · mẫu cột", "cat07": false},
{"id": "13-02", "t0": 502, "t1": 514, "loai": "DATA", "nguon": "N · mẫu cột", "cat07": false},
{"id": "13-03", "t0": 514, "t1": 530, "loai": "DATA", "nguon": "N · mẫu cột (thanh ngang)", "cat07": false},
{"id": "13-04", "t0": 530, "t1": 538, "loai": "DATA", "nguon": "N · mẫu thẻ nguồn", "cat07": false},
{"id": "14-01", "t0": 538, "t1": 546, "loai": "STORY+DATA", "nguon": "N · mẫu thẻ số", "cat07": false},
{"id": "14-02", "t0": 546, "t1": 555, "loai": "STORY+DATA", "nguon": "A · set s43/s01 + lớp thành phố hiện đại (mới) + B3", "cat07": false},
{"id": "14-03", "t0": 555, "t1": 561, "loai": "STORY+DATA", "nguon": "R · s44 + B3", "cat07": false},
{"id": "14-04", "t0": 561, "t1": 571, "loai": "STORY+DATA", "nguon": "N · mới: thẻ kết kênh", "cat07": false}
]```
