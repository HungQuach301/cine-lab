**Nhánh thật: `claude/optimistic-franklin-ubpkvk`** (harness buộc nhánh này thay cho `nc-viral-2910`; tạo mới từ `origin/main` @ `ed3b79c9373739fcc8541bd98d480058e54c781f`).

# NC-VIRAL — video ≥ 1 triệu lượt xem trong 7 ngày của kênh mới (≤ 30 ngày)

Căn cứ: chủ dự án 29/10/2026 07:26: “tìm khoảng 20 video đạt trên 1 triệu lượt trong 1 tuần sau khi đăng của các kênh mới tạo trong 1 tháng gần đấy”. Phạm vi: mọi chủ đề, cả video dài và Shorts.

## §0. Nhánh, thời điểm đo
- Nhánh `claude/optimistic-franklin-ubpkvk`, gốc `origin/main` @ `ed3b79c9`. Vùng sửa: chỉ `reports/nc-viral/**` và `scripts/nc-viral/**`. Không merge.
- Thời điểm đo (lấy làm mốc tính tuổi video):
  - Lượt 1 (quét chung): **2026-10-29 00:42:48 UTC = 07:42:48 Asia/Saigon**.
  - Lượt 2 (bổ sung video dài): **2026-10-29 00:44:30 UTC = 07:44:30 Asia/Saigon**.
- Hook `pre-commit` và `pre-push` (`tools/preflight.sh`) được cài trước lần đẩy đầu. Mọi commit qua preflight “— ĐẠT”.

## §1. Định nghĩa đo
- **Kênh mới:** `channels.snippet.publishedAt` sớm hơn `videos.snippet.publishedAt` không quá 30 ngày.
- **≥ 1 triệu trong 7 ngày:** API chỉ trả lượt xem hiện tại.
  - **Hạng A (chắc chắn):** video đăng ≤ 7 ngày trước thời điểm đo và hiện có ≥ 1 000 000 lượt.
  - **Hạng B (ước, không chắc chắn):** video đăng 8–21 ngày trước và hiện có ≥ 1 000 000 × (tuổi/7)^0,5 lượt. Đây là ước lượng. Mẫu không đủ 20 video hạng A nên hạng B được dùng để lấp chỗ trống.
- **Dài/Shorts** theo `contentDetails.duration`: ≤ 180 s là Shorts.
- **Cờ** (đánh dấu, không loại):
  - “thương hiệu lớn”: kênh phụ của hãng, nghệ sĩ, mạng phân phối hoặc đài có sẵn khán giả.
  - “nghi mua lượt”: lượt thích/lượt xem < 0,2 %, hoặc bình luận tắt kèm lượt xem tăng bất thường.
  - “bình luận tắt (nhãn trẻ em)”: YouTube tự tắt bình luận khi video gắn `madeForKids`, nên cờ này không tự nó là dấu hiệu mua lượt.
  - “kênh bán hàng”: tiêu đề hoặc mô tả kéo người xem sang link mua hàng.
  - “AI (tự khai)”: chỉ ghi khi mô tả video hoặc kênh nói rõ là dùng AI. Phiên không đoán từ hình. Trường `status.containsSyntheticMedia` không trả giá trị cho video nào nên không dùng được.
- Cột “Video kênh (trước)” gồm số video kênh hiện có và, trong ngoặc, số video kênh đăng trước video bùng nổ. Số trong ngoặc đếm qua `playlistItems.list` của danh sách uploads, chỉ tính video còn công khai.

## §2. Phạm vi quét và quota
| Lượt | Truy vấn `search.list` (`type=video`, `order=viewCount`, `maxResults=50`) | Lệnh | Đơn vị |
|---|---|---|---|
| 1a | `publishedAfter` = đo − 21 ngày; 12 `regionCode` (US, GB, IN, BR, ID, MX, PH, VN, DE, JP, KR, FR) × 5 nhóm `videoCategoryId` (tất cả, 22 People & Blogs, 24 Entertainment, 20 Gaming, 23 Comedy) | 60 | 6 000 |
| 1b | `publishedAfter` = đo − 7 ngày; 12 `regionCode`, mọi danh mục (để bắt hạng A, vì danh sách 21 ngày nghiêng về video cũ) | 12 | 1 200 |
| 1c | Truy vấn rỗng theo `relevanceLanguage` es, pt, hi, id, ar, ru; không `regionCode`; 21 ngày | 6 | 600 |
| 2 | Lượt 1 ra 0 video dài, nên quét bổ sung: `videoDuration=medium` (4–20 phút) × {US, IN, BR, ID, MX, PH, toàn cầu} và `videoDuration=long` (> 20 phút) × {US, IN, toàn cầu}; 21 ngày | 10 | 1 000 |
| — | `videos.list` (snippet, statistics, contentDetails, status, topicDetails), gộp 50 id | 24 | 24 |
| — | `channels.list` (snippet, statistics, brandingSettings), gộp 50 id | 16 | 16 |
| — | `playlistItems.list`: đếm video đăng trước video bùng nổ, 29 kênh | 35 | 35 |
| **Tổng** | | **163** | **8 875 / 9 000** |

- Tất cả 88 lệnh `search.list` đều trả đủ 50 kết quả. Không gặp lỗi 403 và không gặp `quotaExceeded`. Sổ từng lệnh: `so-quota.jsonl`.
- Số id duy nhất: 907 video và 632 kênh ở lượt 1; 246 video và 144 kênh ở lượt 2. Các truy vấn trùng nhau nhiều. `regionCode` của `search.list` chỉ lọc yếu, nên các vùng khác nhau trả về nhiều video giống nhau.
- Sau lọc còn **29 video**: 27 Shorts và 2 video dài.
- **Đây là mẫu, không phải danh sách đầy đủ.** `search.list` chỉ trả tối đa 50 video có lượt xem cao nhất cho mỗi truy vấn, và không lọc được theo tuổi kênh. Video của kênh mới chỉ lọt vào mẫu khi đứng trong top 50 của ít nhất một truy vấn.

## §3. Danh sách

### 3.1 Video dài (> 3 phút): 2 video, không đủ 20
Cả hai video đều hạng B (ước), và cả hai đều bị gắn cờ. Không có video dài nào đạt hạng A.

| # | Hạng | Video | Kênh | Kênh tạo | Đăng (UTC) | Tuổi (ngày) | Xem | Xem/ngày | Thích | BL | Dài (s) | Video kênh (trước) | Đăng ký | NN/QG | Ngách | Cờ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | B | [Finger Family Where Are You? - Balloon Finger Song / Kids…](https://www.youtube.com/watch?v=kzUe5s-Q1jo) | [PawPawVEVO](https://www.youtube.com/channel/UCCznEFpmb_BxszSrUH4cWnQ) | 2026-10-01 | 2026-10-08 10:00 | 20.61 | 12 223 115 | 592 951 | 5 763 | 0 | 317 | 6 (1) | 2 990 | en/— | Nhạc thiếu nhi | thương hiệu lớn: kênh VEVO (mạng phân phối nhạc), mô tả dẫn về kênh gốc; nghi mua lượt (thích/xem 0.047 %); bình luận tắt (nhãn trẻ em) |
| 2 | B | [Kakek Diusir dari Hotel, Besoknya Duduk di Kursi Pemilik](https://www.youtube.com/watch?v=QmHzxSgIXlk) | [Storyverse Studio](https://www.youtube.com/channel/UCHaK1oHbOOwatw2kouEVJvw) | 2026-09-29 | 2026-10-10 20:42 | 18.17 | 2 842 878 | 156 474 | 5 421 | 413 | 569 | 11 (5) | 8 210 | id/US | Drama xã hội | nghi mua lượt (thích/xem 0.191 %); AI (tự khai trong mô tả) |

Ngoài định nghĩa, lượt 2 còn có các video dài của kênh 31–90 ngày tuổi, ví dụ:
- Kiddies Fun Rhymes: kênh 56 ngày tuổi, 4,3 triệu lượt.
- Dino World: kênh 71 ngày tuổi, 1,4 triệu lượt.
- Upin & Ipin Indonesia: kênh 80 ngày tuổi, 6,7 triệu lượt. Đây là kênh của thương hiệu có sẵn.
- DenLion: kênh 81 ngày tuổi, 3,7 triệu lượt.

Các kênh này đều làm nhạc hoặc hoạt hình thiếu nhi. Chúng không vào bảng.

### 3.2 Shorts (≤ 180 s): 20 video
Bảng gồm 10 video hạng A và 10 video hạng B, sắp hạng A trước, trong mỗi hạng theo lượt xem/ngày. Có 7 video hạng B nữa, đưa vào phụ lục.

| # | Hạng | Video | Kênh | Kênh tạo | Đăng (UTC) | Tuổi (ngày) | Xem | Xem/ngày | Thích | BL | Dài (s) | Video kênh (trước) | Đăng ký | NN/QG | Ngách | Cờ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | A | [JACK CLOGGED THE TOILET at Daycare! 🚽💩😱 Iggy FREAKS OUT! …](https://www.youtube.com/watch?v=ajjH9jQGDJU) | [Kelli’s Korner Adventures](https://www.youtube.com/channel/UCCVoELSXWKVFGb71y1giTMQ) | 2026-09-25 | 2026-10-23 18:06 | 5.28 | 33 127 236 | 6 279 769 | 230 513 | 0 | 31 | 103 (75) | 27 200 | en/— | Trẻ em – truyện nhân vật | bình luận tắt (nhãn trẻ em) |
| 2 | A | [🔥It was a hot summer night... Until the power cut 🌛💡#ghib…](https://www.youtube.com/watch?v=UTQle6WAvSA) | [GHIBL01](https://www.youtube.com/channel/UCFROpk6lf3ljDYVGWhhMw2w) | 2026-10-07 | 2026-10-24 08:19 | 4.68 | 16 851 209 | 3 598 541 | ẩn | 78 | 29 | 34 (29) | 31 300 | en/IN | Hoạt hình hoài niệm kiểu Ghibli | ẩn lượt thích |
| 3 | A | [Big Crayon Box Saves the Day After Red Crayon Breaks! 🖍️😭…](https://www.youtube.com/watch?v=E-Aio5HyWhM) | [le viet](https://www.youtube.com/channel/UCmOVT5zXeUIQyBoU0jra1ng) | 2026-09-27 | 2026-10-22 02:26 | 6.93 | 24 149 091 | 3 485 847 | 154 188 | 134 | 29 | 28 (21) | 13 600 | en/— | Gia đình – em bé | — |
| 4 | A | [Phillies land All-Star closer Jhoan Duran ahead of MLB tr…](https://www.youtube.com/watch?v=PsP3tUGZv7w) | [Opera Ind GG](https://www.youtube.com/channel/UCA8QCad9S2fMGA_BVCYEEKQ) | 2026-09-27 | 2026-10-26 11:40 | 2.54 | 8 298 616 | 3 263 291 | 41 349 | 27 | 31 | 20 (17) | 7 890 | bn/IN | Gaming (tiêu đề thể thao lệch mô tả kênh) | — |
| 5 | A | [They leaped from giant swaying poles and caught each othe…](https://www.youtube.com/watch?v=-VgwyMQU5U8) | [Gravity rebels](https://www.youtube.com/channel/UCPYvheiAq3HIN0FjhF8-sRQ) | 2026-10-16 | 2026-10-22 16:45 | 6.33 | 14 677 603 | 2 318 139 | 50 145 | 204 | 16 | 12 (5) | 12 700 | en/LK | Nhào lộn/xiếc | AI (tự khai trong mô tả) |
| 6 | A | [His Soldier Dad Arrived When He Least Expected It 🥹🏒❤️ #S…](https://www.youtube.com/watch?v=nxPOSOYQFhw) | [Heart in Seconds](https://www.youtube.com/channel/UCmnu7qIXMcn1z9tIGnkmRgQ) | 2026-09-24 | 2026-10-22 23:15 | 6.06 | 13 760 280 | 2 270 417 | 75 581 | 654 | 16 | 66 (57) | 20 900 | en/PH | Đoàn tụ cảm xúc | — |
| 7 | A | [This Mega Ramp Stunt Looks Impossible #shorts](https://www.youtube.com/watch?v=rfdCkPDhYtk) | [Ramp Stunts](https://www.youtube.com/channel/UCIeAkGBwy-_JjHvorN9D2Vg) | 2026-10-21 | 2026-10-22 13:04 | 6.48 | 13 180 049 | 2 032 499 | 317 913 | 2830 | 31 | 8 (1) | 21 700 | en/— | Mạo hiểm/stunt | — |
| 8 | A | [Toddler Calling The Shots](https://www.youtube.com/watch?v=9OeWy6q-X-A) | [Daisy Family Life](https://www.youtube.com/channel/UCxsiB7XvOtSrSW-BhCPnqIg) | 2026-10-08 | 2026-10-22 22:09 | 6.11 | 10 311 716 | 1 688 744 | 79 718 | 298 | 31 | 32 (22) | 23 000 | en/AE | Gia đình – em bé | — |
| 9 | A | [Baby's Crayon Broke & The Reaction Will Melt Your Heart! …](https://www.youtube.com/watch?v=zJXUkQKqpOg) | [Jeffrey Ebadi](https://www.youtube.com/channel/UCMUx4Nc1yZ-xK1IIh3v0AOA) | 2026-10-14 | 2026-10-23 03:58 | 5.86 | 8 662 541 | 1 477 196 | 55 014 | 22 | 31 | 14 (8) | 5 750 | en/— | Gia đình – em bé | — |
| 10 | A | [How A Hole in your yard can become a nuclear bunker #engi…](https://www.youtube.com/watch?v=TLF9znXtSFc) | [Doodles Fact](https://www.youtube.com/channel/UCMtaW-zKVdo0p6n6HDXyQrA) | 2026-10-24 | 2026-10-24 01:06 | 4.98 | 5 387 760 | 1 081 173 | 208 838 | 1838 | 99 | 5 (0) | 11 300 | en/— | Giải thích kỹ thuật (3D) | — |
| 11 | B | [Comment “STRAW” if you NEED this!😱💕](https://www.youtube.com/watch?v=97v-ISQesJo) | [Merry Latte](https://www.youtube.com/channel/UC56CcJJePEXJrjefWibz6Uw) | 2026-09-30 | 2026-10-19 23:24 | 9.05 | 45 230 533 | 4 995 294 | 299 799 | 833 | 15 | 38 (23) | 41 300 | en/— | Bán hàng – phụ kiện xe | kênh bán hàng |
| 12 | B | [Get Yours At Link in Bi0! 🌊😍 #ocean #vinyl #vinylaestheti…](https://www.youtube.com/watch?v=YU3KhmHUfTg) | [WavesVinyl™](https://www.youtube.com/channel/UCF_sghDxchcUOxsq9BVUKlA) | 2026-10-15 | 2026-10-19 22:37 | 9.09 | 30 846 853 | 3 394 617 | 178 393 | 246 | 21 | 23 (8) | 41 600 | en/— | Bán hàng – đồ trang trí | kênh bán hàng |
| 13 | B | [Comment “GRINCH” if you want it 😈🎄 #audi #m3 #christmas #…](https://www.youtube.com/watch?v=CTFJ-OdSP9U) | [TrunkMisChief🎄](https://www.youtube.com/channel/UC-Tzq8hD8T6T_UneOdCoPow) | 2026-09-22 | 2026-10-21 13:45 | 7.46 | 20 987 178 | 2 814 605 | 74 685 | 127 | 11 | 68 (51) | 19 900 | en/— | Bán hàng – phụ kiện xe | kênh bán hàng |
| 14 | B | [اشش! لا تخبروا أحمد 🤫🍪 مغامرة البسكوتة الهاربة #shorts #ك…](https://www.youtube.com/watch?v=UkBpKBU2-2Y) | [kidz بالعربى](https://www.youtube.com/channel/UCCxZ9UfO4po7LlZN1SQdVPg) | 2026-10-03 | 2026-10-20 18:15 | 8.27 | 21 885 193 | 2 646 602 | 232 164 | 0 | 61 | 35 (23) | 16 800 | ar/EG | Trẻ em – hoạt hình tiếng Ả Rập | bình luận tắt (nhãn trẻ em) |
| 15 | B | [Watch how an old, discarded dumpster is completely transf…](https://www.youtube.com/watch?v=N4jB87mZGX8) | [@SherryKerr](https://www.youtube.com/channel/UCjNuJb2dlOdx28n2Y2m2Vbw) | 2026-10-19 | 2026-10-21 19:45 | 7.21 | 16 873 420 | 2 341 430 | 263 991 | 839 | 61 | 22 (7) | 43 400 | en/SG | Cải tạo/biến đổi đồ vật | — |
| 16 | B | [Nuevo Shampoo Alma de Romero](https://www.youtube.com/watch?v=DSnY8_a6mJw) | [Alma de Romero](https://www.youtube.com/channel/UC5MoY_Q3tlsZqEz18HQx6xQ) | 2026-10-19 | 2026-10-20 22:57 | 8.07 | 16 511 198 | 2 045 126 | 20 | 3 | 41 | 1 (0) | 84 | es/— | Quảng cáo sản phẩm | nghi mua lượt (thích/xem 0.000 %); kênh bán hàng |
| 17 | B | [अमीरजादे का घमंड तोड़ा 😱 / Wrecked BMW M8 Restoration 🧑‍🔧/…](https://www.youtube.com/watch?v=MLL8QiDZFi0) | [Varsile Diaries](https://www.youtube.com/channel/UCLYJFPgx5nB_7njfpA3wckA) | 2026-09-20 | 2026-10-17 08:45 | 11.66 | 21 914 363 | 1 878 668 | 453 378 | 9620 | 139 | 40 (27) | 196 000 | hi/IN | Truyện kể – phục chế xe | AI (tự khai trong mô tả) |
| 18 | B | [They Pulled a REAL TANK Out of the Water 😱🪖 #Shorts](https://www.youtube.com/watch?v=VT0IWbHL4I0) | [River Recovery](https://www.youtube.com/channel/UCdLnVg_oErN7eVwssMdufDA) | 2026-10-09 | 2026-10-17 13:25 | 11.47 | 17 514 876 | 1 526 950 | 52 657 | 202 | 31 | 40 (20) | 27 500 | en-US/US | Trục vớt/khám phá | — |
| 19 | B | [My Brother Took the Whole Room… BIG MISTAK](https://www.youtube.com/watch?v=4c8nW0eASug) | [sssss](https://www.youtube.com/channel/UCkPIEUmhH0g5gSilExNKiJw) | 2026-09-21 | 2026-10-16 07:24 | 12.72 | 16 891 348 | 1 327 861 | 109 247 | 239 | 61 | 33 (18) | 22 500 | en/GB | Truyện ngắn anh chị em | — |
| 20 | B | [karodon ki deal chhoti Bahu ki samajhdari Se hua final](https://www.youtube.com/watch?v=4J51OQEDReo) | [Indu kanchan Singh](https://www.youtube.com/channel/UCtN9XdDk9kUBnxfmU8bGgeg) | 2026-10-08 | 2026-10-21 08:33 | 7.67 | 10 117 141 | 1 318 473 | 485 941 | 678 | 180 | 5 (3) | 130 000 | en/— | Drama gia đình | — |

**Phụ lục: 7 Shorts hạng B ngoài bảng chính**

| # | Hạng | Video | Kênh | Kênh tạo | Đăng (UTC) | Tuổi (ngày) | Xem | Xem/ngày | Thích | BL | Dài (s) | Video kênh (trước) | Đăng ký | NN/QG | Ngách | Cờ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | B | [பஸ்ல எழுப்பி விட்ட பணக்காரம்மா😡கடைசியில அவங்க வாசல்ல வந்த…](https://www.youtube.com/watch?v=vjlmPlVI-Ws) | [TAMIL AI STORY ](https://www.youtube.com/channel/UCwtupt5veE2prgxjMcEawvQ) | 2026-10-02 | 2026-10-19 13:21 | 9.47 | 10 382 617 | 1 096 000 | 340 657 | 824 | 179 | 54 (35) | 200 000 | ta/— | Drama xã hội | AI (tự khai trong mô tả) |
| 2 | B | [🎃🍿 Halloween Movie Night 🎬👻 #halloween #kidactivities #sp…](https://www.youtube.com/watch?v=MECqPd3deRo) | [The Craig Crew](https://www.youtube.com/channel/UCSV69VBsOLCMc8q4niYPPcQ) | 2026-09-25 | 2026-10-12 03:35 | 16.88 | 15 340 138 | 908 760 | 209 630 | 1122 | 36 | 5 (1) | 22 800 | en/— | Gia đình – hoạt động | — |
| 3 | B | [From Tiny Peanut Seeds to Huge Harvest! 🌱🥜/ Rainy Season …](https://www.youtube.com/watch?v=DUZfv1I6X5U) | [Dreamy Farm Life](https://www.youtube.com/channel/UCTm9n33pquyIPCLEBnwbpgA) | 2026-10-03 | 2026-10-13 11:54 | 15.53 | 12 835 131 | 826 267 | ẩn | 393 | 151 | 17 (10) | 37 800 | en/— | Nông trại/đời sống quê | ẩn lượt thích; AI (tự khai trong mô tả) |
| 4 | B | [Why Old Soda Bottles Couldn't Stand Up](https://www.youtube.com/watch?v=hRYWcfp6dsg) | [Trial & Eureka](https://www.youtube.com/channel/UCP8wHrwU79SSJUxu1PBmiNQ) | 2026-10-04 | 2026-10-09 10:50 | 19.58 | 14 078 938 | 719 118 | 431 531 | 1237 | 78 | 12 (4) | 23 900 | en/US | Lịch sử phát minh (giải thích) | — |
| 5 | B | [Toddler Tries to Shush Newborns and Instantly Regrets It …](https://www.youtube.com/watch?v=VTtaYwY956U) | [Gala Awesome](https://www.youtube.com/channel/UCS8eC9hjtB7wOYfWJvdh0Ww) | 2026-09-19 | 2026-10-14 17:15 | 14.31 | 9 058 728 | 633 000 | 63 349 | 451 | 16 | 40 (39) | 154 000 | en-US/US | Gia đình – em bé | AI (tự khai trong mô tả) |
| 6 | B | [3 Tahun Tanam Pisang di Pot, Akhirnya Berbuah! 🍌😱](https://www.youtube.com/watch?v=CmyNfvNOeic) | [Tanam Cepat](https://www.youtube.com/channel/UClQ03GKsIuCtgyYkLtRhebw) | 2026-09-22 | 2026-10-10 08:00 | 18.7 | 11 587 224 | 619 760 | 136 737 | 374 | 152 | 26 (10) | 14 700 | id/ID | Trồng cây (timelapse) | — |
| 7 | B | [Big Sister Meets Quadruplets and Her Hilarious Reaction t…](https://www.youtube.com/watch?v=Re5eIR7KJy0) | [Katil Heart & Family](https://www.youtube.com/channel/UCS5PvDJCS1F2Bx74fYAOcUw) | 2026-09-19 | 2026-10-10 17:11 | 18.31 | 6 734 014 | 367 704 | 55 797 | 133 | 16 | 59 (24) | 16 600 | en-US/US | Gia đình – em bé | AI (tự khai trong mô tả) |

Dữ liệu đầy đủ, gồm cả cột ngày giờ tạo kênh, nằm trong `shorts.csv` và `video-dai.csv`. Cột `trong_bang_chinh` ghi “có” hoặc “phụ lục”.

## §4. Phân tích ngắn (29 video)
1. **Ngách nổi:**
   - Gia đình và em bé: 5 video, cộng 1 video hoạt động gia đình (The Craig Crew). 2 trong số này tự khai làm bằng AI “realistic” (Gala Awesome, Katil Heart & Family).
   - Trẻ em/hoạt hình: 4 video.
   - Kênh bán hàng “Comment X / Link in bio”: 4 video. Lượt xem/ngày rất cao (2–5 triệu).
   - Drama xã hội/gia đình: 4 video, bằng tiếng Hindi, Tamil, Indonesia. 2 video tự khai AI.
   - Biến đổi theo thời gian: 3 video (cải tạo thùng rác, trồng chuối 3 năm, hạt lạc → thu hoạch).
   - Stunt/nhào lộn: 2 video. Trục vớt: 1 video.
   - Giải thích kỹ thuật/lịch sử phát minh: 2 video (Doodles Fact, Trial & Eureka).
   - Có hai kênh khác nhau (le viet, Jeffrey Ebadi) cùng làm một ý tưởng “bút sáp màu đỏ gãy”, đăng cách nhau một ngày. Đây là dấu hiệu chạy theo trend hoặc sao ý tưởng.
2. **Độ dài:** trung vị 31 s. 17 trên 29 video ≤ 41 s. Trong khoảng 1 150 id đã quét (hai lượt, có thể trùng), chỉ có 2 video > 3 phút của kênh ≤ 30 ngày tuổi đạt ngưỡng. Trong mẫu này, kênh mới bùng nổ gần như chỉ qua Shorts.
3. **Kiểu tiêu đề:**
   - Trung vị 81 ký tự. 18/29 tiêu đề có emoji, 20/29 có hashtag.
   - Chỉ 1/29 tiêu đề là câu hỏi. 3/29 có con số (ví dụ “3 Tahun…”).
   - 5 tiêu đề có từ viết hoa toàn bộ.
   - Khoảng 8 tiêu đề dùng mẫu “tình huống → phản ứng/bước ngoặt” (“…and Instantly Regrets It”, “Until the power cut”, “BIG MISTAKE”, “Saves the Day”).
   - 2 tiêu đề là lệnh kêu gọi bình luận để nhận link (“Comment ‘STRAW’…”).
   - Ẩn số/tò mò xuất hiện ở “Why…”/“How…” (2 video giải thích).
4. **Số video trước video bùng nổ:**
   - Trung vị 17 video (khoảng 0–75). Trung vị tốc độ đăng xấp xỉ 1 video/ngày từ khi lập kênh.
   - 4 kênh bùng nổ ngay ở video đầu hoặc thứ hai: Doodles Fact (0), Alma de Romero (0, nghi mua lượt), Ramp Stunts (1), PawPawVEVO (1, kênh VEVO).
   - Kênh mới bùng nổ thường là kênh đăng dày (đăng nhiều, thử nhanh), ít khi là video đầu tay.
5. **AI rõ ràng (tự khai):** 7/29 video (24 %): Gravity rebels, Varsile Diaries, TAMIL AI STORY, Dreamy Farm Life, Gala Awesome, Katil Heart & Family, Storyverse Studio. Các video còn lại không tự khai. Phiên không đoán thêm. Con số này là cận dưới.
6. **Cờ:**
   - 1 video “thương hiệu lớn”: PawPawVEVO.
   - 3 video nghi mua lượt:
     - Alma de Romero: 20 lượt thích / 16,5 triệu lượt xem. Kênh có 1 video và 84 người đăng ký. Rất có thể đây là lượt xem từ quảng cáo trả tiền.
     - PawPawVEVO: 0,047 %.
     - Storyverse Studio: 0,191 %.
   - 4 kênh bán hàng.
   - 2 video ẩn lượt thích.

### Có thể áp cho Moving Parts (series lịch sử timelapse 3D)
- **Trial & Eureka** gần nhất về ngách. Video là lịch sử phát minh qua các thất bại kỹ thuật (“Why Old Soda Bottles Couldn't Stand Up”), dài 78 s. Kênh 5 ngày tuổi, có 4 video trước đó. Video đạt 14,1 triệu lượt, tỉ lệ thích 3,1 %. Mẫu tiêu đề là câu “Why…” về một vật quen thuộc, kèm mô tả “every great invention started as a failure”.
- **Doodles Fact** (3D, “How A Hole in your yard can become a nuclear bunker”, 99 s) đạt 5,4 triệu lượt trong 5 ngày ngay ở video đầu tiên. Hình 3D giải thích một quá trình xây dựng có thể kéo người xem mà không cần kênh có sẵn khán giả.
- **Biến đổi theo thời gian** khớp với lõi timelapse: Tanam Cepat (3 năm → 152 s), Dreamy Farm Life (hạt → thu hoạch), SherryKerr (cũ → mới), River Recovery (đáy sông → vật lộ ra). Cấu trúc chung là trạng thái đầu → các bước → kết quả, với kết quả hé lộ ở cuối.
- Shorts 60–100 s đóng vai trò cửa vào kênh. Trong mẫu, video dài không bùng nổ ở kênh mới, nên video dài của series có lẽ cần Shorts dẫn đường.
- Nhịp đăng: trung vị 17 video trước video bùng nổ. Điều này gợi ý cần một lô Shorts cùng format trước khi đánh giá.

### KHÔNG áp được
- AI giả làm cảnh thật (em bé/gia đình “realistic”, drama xã hội): người xem dễ bị đánh lừa. Kiểu này trái nguyên tắc chất lượng và trung thực của dự án, và cũng khác ngách.
- Kênh bán hàng “Comment X”, quảng cáo trả tiền, video nghi mua lượt: chỉ số không phản ánh khán giả tự nhiên.
- Nhạc và hoạt hình thiếu nhi gắn `madeForKids`: khác khán giả, bình luận bị tắt, quảng cáo bị hạn chế.
- Tiêu đề lệch nội dung (Opera Ind GG: tiêu đề tin bóng chày MLB, kênh tự mô tả là game mô phỏng): đây là clickbait và có rủi ro chính sách.
- Sao ý tưởng của kênh khác (cặp video “bút sáp màu đỏ gãy”): trái luật cứng không sao chép.

Phần này chỉ mô tả các mẫu quan sát được. Phiên không chấm điểm hay chọn hướng thay chủ dự án.

## §5. Chỉ số nằm trong ±5 % quanh ngưỡng
- **Tuổi kênh 30 ngày (28,5–31,5):** Kelli’s Korner 28,6; TrunkMisChief 28,6; Heart in Seconds 28,6; Opera Ind GG 29,3. Tuổi kênh tính chính xác tới giây.
- **Shorts 180 s (171–189):** Indu kanchan Singh đúng 180 s, được tính là Shorts. TAMIL AI STORY 179 s.
- **Nghi mua lượt 0,2 % (0,19–0,21 %):** Storyverse Studio 0,191 %, có gắn cờ.
- **Ngưỡng hạng A/B:** không video nào nằm trong ±5 %. Video hạng A thấp nhất đạt 5,39 triệu lượt. Các video hạng B đều vượt ngưỡng ước ít nhất 1,7 lần.

## §6. Giới hạn phương pháp
- Danh sách là mẫu lấy từ `search.list`, không phải danh sách đầy đủ. Kết quả lệch về video có lượt xem cao nhất trong từng truy vấn, và về các vùng/danh mục đã chọn. Danh mục Music, Sports, Education, Howto chỉ được quét qua truy vấn “mọi danh mục”.
- Không có lượt xem lịch sử. Hạng B dựa trên giả định tăng theo √tuổi. Một video hạng B có thể chưa đạt 1 triệu ở ngày thứ 7, hoặc đã vượt từ lâu.
- Ngày tạo kênh có thể là ngày tạo tài khoản Google/thương hiệu, không phải ngày mở kênh. Ngược lại, kênh cũ đổi tên sẽ không lọt vào mẫu. Kênh có thể là kênh phụ của người có sẵn khán giả mà API không cho thấy. Cờ “thương hiệu lớn” chỉ dựa vào tên và mô tả.
- “Nghi mua lượt” là heuristic theo tỉ lệ thích/xem. Video được quảng cáo trả tiền hợp lệ cũng có tỉ lệ thấp.
- Số video trước video bùng nổ chỉ tính video còn công khai lúc đo.
- Ngách do phiên tự gán bằng tay từ tiêu đề và mô tả, không xem nội dung video.

## §7. Chi phí
| Mục | Hạn | Dùng |
|---|---|---|
| YouTube Data API v3 | ≤ 9 000 đơn vị | **8 875** (sổ `so-quota.jsonl`) |
| Claude API | mốc $1, chặn $3 | **$0**. Phân loại ngách do phiên tự gán bằng tay, không gọi API (`so-ai.jsonl`). |
| Gemini, OpenAI, ElevenLabs | 0 | 0 |
| Giờ máy | ≤ 3 h | khoảng 0,2 h |

## §8. Tệp
`reports/nc-viral/`:
- `NC-VIRAL-BAO-CAO.md`
- `video-dai.csv`
- `shorts.csv`
- `quet.json`: id, số liệu thô, truy vấn trúng. Không có mô tả, không có khoá.
- `so-quota.jsonl`
- `so-ai.jsonl`
- `CHECKPOINT.md`

`scripts/nc-viral/`:
- `quet.py`
- `loc.py`
- `truoc.py`
- `xuat.py`

Khoá API do proxy gắn. Script không đọc và không ghi khoá. Repo không lưu ảnh, thumbnail hay video của kênh khác, chỉ lưu URL và số liệu văn bản.

## Việc đang chờ chủ dự án
- Duyệt báo cáo.
- Quyết định có cần quét lượt sau không. Lượt sau sẽ cần quota ngày mới, sau khi hạn mức đặt lại, và có thể nhắm vào video dài hoặc ngách lịch sử/giáo dục.
- Quyết định có rút bài học nào cho kênh Moving Parts không.

**DỪNG chờ chủ dự án.**
