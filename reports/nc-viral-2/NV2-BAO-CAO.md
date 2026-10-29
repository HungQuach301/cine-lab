**Nhánh thật: `claude/nc-viral-2-moving-parts-9sf5i2`** (harness buộc nhánh này thay cho `nc-viral-2`; tạo từ `origin/main` @ `ed3b79c9373739fcc8541bd98d480058e54c781f`).

# NV-2 (NC-VIRAL-2) — video bùng nổ của kênh mới, ngách gần Moving Parts

Căn cứ: chủ dự án 29/10/2026 08:07 “Tôi muốn test NV2 trc”. Ngách: lịch sử, bản đồ/địa lý, timelapse, 3D/hoạt hình giải thích, “how it was built”, “then and now”, tài liệu. Cả video dài và Shorts.

> **Kết luận trước:** quét `search.list` chỉ chạy được **9/84 truy vấn**. Dự án Google có hạn riêng **100 lệnh `search.list`/ngày** (`defaultSearchListPerDayPerProject`), và NC-VIRAL đã dùng 88 lệnh trong cùng ngày Thái Bình Dương. Theo lệnh “không chờ, không thử lại vòng lặp”, phiên dừng quét và mở rộng mẫu bằng danh sách uploads của kênh mới (không tốn `search.list`). Mẫu vẫn cho tín hiệu rõ, nhưng **mỏng hơn kế hoạch**. Xem §2 và §6.

## §0. Nhánh, gốc, thời điểm đo
- Nhánh `claude/nc-viral-2-moving-parts-9sf5i2`, gốc `origin/main` @ `ed3b79c9`. Vùng sửa chỉ gồm `reports/nc-viral-2/**` và `scripts/nc-viral-2/**`. Không merge.
- Mốc đo (tính tuổi video và cửa sổ 30 ngày): **2026-10-29 01:14:45 UTC = 08:14:45 Asia/Saigon**. `publishedAfter` = 2026-09-29T01:14:45Z.
  - Số liệu video từ `search.list` lấy lúc 01:14–01:17 UTC.
  - Số liệu video từ uploads lấy lúc 01:21 UTC (08:21 Asia/Saigon).
  - Tuổi video tính tới lúc lấy số liệu của chính video đó (trường `fetched` trong `quet.json`).
- Hook `pre-commit` và `pre-push` (`tools/preflight.sh`) được cài trước lần đẩy đầu. Mọi commit đều qua preflight “— ĐẠT”.
- Script là bản sao sửa từ `scripts/nc-viral/*.py` (nhánh `claude/optimistic-franklin-ubpkvk`), nằm trong `scripts/nc-viral-2/`:
  - `quet.py`: quét;
  - `loc.py`: lọc;
  - `truoc.py`: đọc uploads và đếm video trước;
  - `xuat.py`: xuất tệp.

## §1. Định nghĩa đo
- **Kênh mới:** `channels.snippet.publishedAt` sớm hơn `videos.snippet.publishedAt` không quá 90 ngày.
  - Cột “tuổi kênh lúc đăng” tách nhóm ≤ 30 ngày và 31–90 ngày.
- **M1:**
  - Hạng A: video ≤ 7 ngày tuổi và đã ≥ 1 000 000 lượt.
  - Hạng B (**ước**): video 7–30 ngày tuổi và ≥ 1 000 000 × (tuổi/7)^0,5 lượt.
- **M2:** cùng cách tính với ngưỡng 300 000. Bảng M2 không gồm video đã đạt M1.
  - Hạng B ở cả hai mức là ước lượng. API chỉ trả lượt xem hiện tại, không trả lượt xem lúc video tròn 7 ngày.
- **Dài/Shorts** theo `contentDetails.duration`: ≤ 180 s là Shorts. Video dài chia ba nhóm: 3–10 phút, 10–20 phút, > 20 phút.
- **Mức ngách**, phiên gán bằng tay theo kênh, dựa trên tiêu đề và mô tả kênh/video. Không gọi Claude API (bảng `NICHE` trong `xuat.py`).
  - **gần:** lõi ngách Moving Parts.
  - **vừa:** giải thích khoa học/đồ vật, có phần lịch sử.
  - **xa:** ngoài ngách. Video mức xa không vào bảng chính, chỉ được liệt kê dưới mỗi bảng và trong CSV.
- **Cờ** (chỉ đánh dấu, không loại):
  - thương hiệu lớn: không gặp.
  - nghi mua lượt: lượt thích/lượt xem < 0,2 %.
  - bình luận tắt, madeForKids.
  - kênh bán hàng: không gặp.
  - nghi đăng lại phim có bản quyền.
  - **AI tự khai:** chỉ ghi khi mô tả video hoặc kênh tự nói có dùng AI.
  - **AI giả tư liệu thật:** mô tả tự khai dùng hình AI cho cảnh **lịch sử** như thật, ví dụ “Some scenes are AI-generated illustrations of moments no camera recorded”.
  - Ghi thêm “tự khai No AI” khi kênh nói rõ không dùng hình AI.
- **Video kênh (trước):** số video kênh hiện có, kèm trong ngoặc số video đăng trước video bùng nổ. Đếm bằng `playlistItems.list` trên danh sách uploads, nên chỉ tính video còn công khai.
- **Nhịp đăng:** số video ÷ số ngày từ video đầu tới mốc đo.

## §2. Phạm vi quét và quota
**Lệnh thử đầu tiên:** `videos.list` 1 id (1 đơn vị) lúc 01:13:18Z trả **HTTP 200**. Quota đơn vị chưa cạn, nên phiên bắt đầu quét.

**Diễn biến quét:**
- `quet.py` lập kế hoạch **84 lệnh `search.list`**, đều dùng `type=video`, `order=viewCount`, `maxResults=50`, `publishedAfter` = đo − 30 ngày. Kế hoạch có 6 nhóm:
  - 22 từ khoá lõi ngách;
  - 18 lệnh `videoDuration` medium/long;
  - 20 lệnh theo `videoCategoryId` 27/28/19/1/22, kể cả truy vấn rỗng theo 6 `regionCode`;
  - 10 truy vấn tiếng es/pt/hi/id;
  - 6 lệnh `regionCode`;
  - 8 lệnh `videoDuration=short`.
- Lượt đầu gọi cách nhau 0,2 s. Kết quả: 5 lệnh 200, 79 lệnh **429 `rateLimitExceeded`**. Phiên tưởng đây là giới hạn nhịp, nên giãn lên 6 s rồi 20 s và thử lại đúng 1 lần mỗi lượt. Thêm 4 lệnh 200, sau đó 429 lặp lại.
- Phiên đọc thân lỗi 429 bằng 1 lệnh tay. Nội dung: *“Quota exceeded for quota metric 'Search Queries' and limit 'Search Queries per day'”*, kèm `quota_limit=defaultSearchListPerDayPerProject`, `quota_limit_value=100`. Cửa sổ ngày bắt đầu 2026-10-28 07:00Z, tức 0 h giờ Thái Bình Dương, và đặt lại lúc **2026-10-29 07:00Z = 14:00 Asia/Saigon**.
  - NC-VIRAL chạy lúc 00:42Z, tức 28/10 theo giờ Thái Bình Dương, và đã dùng 88 search. NV-2 lấy được 9 lệnh. Tổng 97 lệnh. Phần chênh với 100 có thể là lệnh của phiên khác; phiên không kiểm được.
  - **Hệ quả cấu trúc:** mỗi ngày chỉ chạy được ≤ 100 `search.list` cho **mọi phiên** của dự án, bất kể quota đơn vị còn bao nhiêu.
- **9 truy vấn chạy được:**
  - `history`
  - `how it was built`
  - `3D timelapse`
  - `map` (medium)
  - `then and now`
  - `geography`
  - `documentary`
  - `archaeology` (medium)
  - truy vấn rỗng, danh mục 27, `regionCode=BR`

  Tất cả đều đủ 50 kết quả. Gộp lại được 446 id video, 345 kênh.
- Mở rộng không tốn search (`truoc.py`):
  - Đọc trọn uploads của **39 kênh** ≤ 90 ngày tuổi trong mẫu: 58 lệnh `playlistItems.list`.
  - Lấy số liệu cho 977 video đăng ≤ 30 ngày chưa có trong mẫu: 20 lệnh `videos.list`.
  - Kết quả: 976 video của 39 kênh mới (27 kênh ≤ 30 ngày tuổi), **106 video đạt M2** (53 đạt M1). Trong đó **46 video thuộc ngách gần/vừa**.

| Lệnh | Số lệnh | HTTP | Đơn vị chắc chắn | Đơn vị nếu 429 bị tính |
|---|---|---|---|---|
| `videos.list` thử | 1 | 200 | 1 | 1 |
| `search.list` | 9 | 200 | 900 | 900 |
| `search.list` | 83 | 429 (hạn 100 search/ngày) | 0 | 8 300 |
| `videos.list` (gồm 20 cho uploads) | 29 | 200 | 29 | 29 |
| `channels.list` | 9 | 200 | 9 | 9 |
| `playlistItems.list` | 58 | 200 | 58 | 58 |
| **Tổng** | **189** | | **997 / 9 000** | 9 297 |

- Lệnh 429 bị Google từ chối vì chạm hạn đếm lệnh, nên sổ ghi 0 đơn vị. Cột `units_neu_tinh_429` vẫn ghi chi phí danh nghĩa để làm trần trên. Phiên **không kiểm được** con số tiêu hao thật trên Cloud Console.
  - Nếu Google có tính 429, trần trên là 9 297 đơn vị, vượt hạn mức phiên 9 000. Chủ dự án nên đối chiếu trên console.
  - Bài học: gọi 0,2 s/lệnh khi hạn ngày đã gần cạn làm phát sinh 83 lệnh 429. Lần sau phải đọc thân lỗi 429 ngay ở lệnh đầu, thay vì giãn nhịp rồi thử lại.
- Sổ từng lệnh: `so-quota.jsonl`. Mỗi dòng có các trường `units`, `cum`, `http`, `reason`, `usd`, `units_neu_tinh_429`, `cum_tran_tren`.
- **Đây là mẫu, không phải danh sách đầy đủ.** Hai nguồn lệch mẫu:
  - 9 truy vấn tiếng Anh, không chạy được truy vấn theo vùng, danh mục, ngôn ngữ hay Shorts riêng.
  - Bước mở rộng qua uploads kéo thêm video của **cùng các kênh** đã lọt mẫu. Vì vậy The Why Side (16 video M2) và Trial & Eureka (8) chiếm phần lớn bảng Shorts.

## §3. Bốn bảng và danh sách kênh
Cách đọc bảng:
- Ưu tiên hạng A, sau đó sắp theo lượt xem/ngày.
- “Xem/ĐK” là lượt xem chia số người đăng ký hiện tại của kênh.
- “Nguồn”: *search* là video lọt top 50 của một truy vấn; *uploads kênh* là video lấy từ danh sách uploads.

CSV có đủ cột, gồm cả ngưỡng M1/M2 riêng từng video, nhịp đăng, video mức xa (ghi `trong_bang_chinh = ngoài ngách (xa)`) và cột `nguon`.

### 3.1 Video dài · M1 (≥ 1 triệu/7 ngày): 4 video ngách, 0 hạng A — không đủ 20
| # | Hạng | Video | Kênh | Kênh tạo | Tuổi kênh lúc đăng (ngày) | Đăng (UTC) | Tuổi video (ngày) | Xem | Xem/ngày | Thích | BL | Dài (s) · nhóm | Video kênh (trước) | Đăng ký | Xem/ĐK | NN/QG | Ngách | Nguồn | Cờ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | B | [Underwater Drone Entered the Titanic — What It Captured W…](https://www.youtube.com/watch?v=v0G9my0lyas) | [Ambrose Discovery](https://www.youtube.com/channel/UCAVxoa11gRHcit9_onvTkMQ) | 2026-07-15 | 86.8 | 2026-10-10 16:00 | 18.38 | 4 182 364 | 227 489 | 21 662 | 760 | 1265 · > 20 phút | 109 (50) | 92 400 | 45.3 | en/US | Tài liệu khám phá (xác tàu, bí ẩn) (gần) | search | — |
| 2 | B | [Geologists Just Found Out What Wyoming’s Devils Tower Act…](https://www.youtube.com/watch?v=id-q1bhqjNU) | [Buried Evidence](https://www.youtube.com/channel/UCdAO08RVzexvMw24cir112g) | 2026-10-09 | 1.2 | 2026-10-10 04:42 | 18.86 | 2 927 374 | 155 216 | 12 346 | 2 316 | 1067 · 10–20 phút | 17 (1) | 2 560 | 1143.5 | en/— | Tài liệu khảo cổ/địa chất (gần) | uploads kênh | — |
| 3 | B | [Watch NEW YORK Grow for 400 Years - 3D Timelapse (No AI i…](https://www.youtube.com/watch?v=Xn1s4JvDKYY) | [CityEons](https://www.youtube.com/channel/UCi216jUuIATe6cfr_pNRdvQ) | 2026-10-03 | 13.8 | 2026-10-17 10:14 | 11.63 | 1 605 745 | 138 104 | 5 284 | 543 | 538 · 3–10 phút | 5 (3) | 6 770 | 237.2 | en/DE | 3D timelapse thành phố (gần) | search | tự khai "No AI" |
| 4 | B | [IRÁN / El País Más Peligroso y Oculto de Oriente Medio / …](https://www.youtube.com/watch?v=LXtJe7-oVhM) | [Sin Coordenadas](https://www.youtube.com/channel/UCnIpkOAIMk5pfhHxIIuwa1g) | 2026-07-19 | 82.4 | 2026-10-09 17:00 | 19.35 | 2 232 524 | 115 388 | 18 131 | 1 422 | 2379 · > 20 phút | 20 (15) | 45 400 | 49.2 | es/ES | Tài liệu địa lý quốc gia (es) (gần) | uploads kênh | — |

*Ngoài ngách (xa), không vào bảng:* Ali Wildlife Hunt 4 727 824 (Tài liệu động vật); CineFlex Entertainment 3 694 303 (Phim truyện đầy đủ); CineFlex Entertainment 1 801 769 (Phim truyện đầy đủ)

### 3.2 Video dài · M2 (≥ 300 nghìn/7 ngày, không gồm M1): 6 video ngách, 0 hạng A — không đủ 20
| # | Hạng | Video | Kênh | Kênh tạo | Tuổi kênh lúc đăng (ngày) | Đăng (UTC) | Tuổi video (ngày) | Xem | Xem/ngày | Thích | BL | Dài (s) · nhóm | Video kênh (trước) | Đăng ký | Xem/ĐK | NN/QG | Ngách | Nguồn | Cờ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | B | [AUSTRALIA: La Tierra Más Aislada y Peligrosa del Mundo / …](https://www.youtube.com/watch?v=el7kS4W0Ulc) | [Sin Coordenadas](https://www.youtube.com/channel/UCnIpkOAIMk5pfhHxIIuwa1g) | 2026-07-19 | 79.0 | 2026-10-06 06:45 | 22.77 | 1 778 460 | 78 104 | 13 087 | 813 | 2665 · > 20 phút | 20 (14) | 45 400 | 39.2 | es/ES | Tài liệu địa lý quốc gia (es) (gần) | search | — |
| 2 | B | [Divers Explored Lake Mead as Water Levels Dropped — What …](https://www.youtube.com/watch?v=dhQBsbBvG2E) | [Ambrose Discovery](https://www.youtube.com/channel/UCAVxoa11gRHcit9_onvTkMQ) | 2026-07-15 | 77.8 | 2026-10-01 16:00 | 27.39 | 1 729 227 | 63 135 | 8 958 | 204 | 1260 · > 20 phút | 109 (36) | 92 400 | 18.7 | en/US | Tài liệu khám phá (xác tàu, bí ẩn) (gần) | uploads kênh | — |
| 3 | B | [RUSIA / El País Más Frío y Peligroso del Mundo / Document…](https://www.youtube.com/watch?v=B5BjPeYBExc) | [Sin Coordenadas](https://www.youtube.com/channel/UCnIpkOAIMk5pfhHxIIuwa1g) | 2026-07-19 | 87.4 | 2026-10-14 17:00 | 14.35 | 832 577 | 58 028 | 9 597 | 570 | 2363 · > 20 phút | 20 (16) | 45 400 | 18.3 | es/ES | Tài liệu địa lý quốc gia (es) (gần) | uploads kênh | — |
| 4 | B | [Archaeologists Just Found Out What the Bullets at Little …](https://www.youtube.com/watch?v=r3IUEQxkpLw) | [Buried Evidence](https://www.youtube.com/channel/UCdAO08RVzexvMw24cir112g) | 2026-10-09 | 2.8 | 2026-10-11 21:00 | 17.18 | 913 243 | 53 168 | 1 501 | 156 | 1096 · 10–20 phút | 17 (3) | 2 560 | 356.7 | en/— | Tài liệu khảo cổ/địa chất (gần) | search | nghi mua lượt (thích/xem 0.164 %) |
| 5 | B | [Watch ROME Grow for 3,000 Years - 3D Timelapse (No AI ima…](https://www.youtube.com/watch?v=50dWQdlHmYI) | [CityEons](https://www.youtube.com/channel/UCi216jUuIATe6cfr_pNRdvQ) | 2026-10-03 | 7.8 | 2026-10-11 09:04 | 17.68 | 897 271 | 50 764 | 3 689 | 305 | 598 · 3–10 phút | 5 (2) | 6 770 | 132.5 | en/DE | 3D timelapse thành phố (gần) | search | tự khai "No AI" |
| 6 | B | [Watch LONDON Grow for 2,000 Years - 3D Timelapse (No AI i…](https://www.youtube.com/watch?v=NfOzqVW33bs) | [CityEons](https://www.youtube.com/channel/UCi216jUuIATe6cfr_pNRdvQ) | 2026-10-03 | 1.7 | 2026-10-05 08:11 | 23.71 | 658 049 | 27 752 | 3 117 | 527 | 322 · 3–10 phút | 5 (0) | 6 770 | 97.2 | en/DE | 3D timelapse thành phố (gần) | search | tự khai "No AI" |

*Ngoài ngách (xa), không vào bảng:* Keyro 375 738 (Gaming Roblox); CineFlex Entertainment 320 879 (Phim truyện đầy đủ); Keyro 835 404 (Gaming Roblox); Keyro 418 848 (Gaming Roblox); CineFlex Entertainment 580 018 (Phim truyện đầy đủ)

### 3.3 Shorts · M1: 18 video ngách (A 2) — không đủ 20
| # | Hạng | Video | Kênh | Kênh tạo | Tuổi kênh lúc đăng (ngày) | Đăng (UTC) | Tuổi video (ngày) | Xem | Xem/ngày | Thích | BL | Dài (s) · nhóm | Video kênh (trước) | Đăng ký | Xem/ĐK | NN/QG | Ngách | Nguồn | Cờ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | A | [The Blind Man Who Dodged Every Obstacle](https://www.youtube.com/watch?v=fhG3L9xbEN8) | [The Why Side](https://www.youtube.com/channel/UCjFTPUCLQucNHkHSTuGxraw) | 2026-09-26 | 25.9 | 2026-10-22 13:45 | 6.48 | 1 710 805 | 263 872 | 47 469 | 493 | 48 · Shorts | 33 (23) | 32 200 | 53.1 | en/US | Giải thích 3D đồ vật/khoa học (có lịch sử) (vừa) | uploads kênh | — |
| 2 | A | [India Controls Bangladesh’s Biggest River #india #banglad…](https://www.youtube.com/watch?v=QQbUPpVQ1ko) | [Whyograph](https://www.youtube.com/channel/UCj8ovMHnMmCUZjditRhiQ0Q) | 2026-10-14 | 7.4 | 2026-10-22 02:30 | 6.95 | 1 010 902 | 145 510 | 8 615 | 570 | 71 · Shorts | 11 (5) | 2 800 | 361.0 | en/— | Bản đồ – địa chính trị (gần) | search | — |
| 3 | B | [He Put His Head in a Particle Accelerator](https://www.youtube.com/watch?v=fM-_0tJG8Eo) | [The Why Side](https://www.youtube.com/channel/UCjFTPUCLQucNHkHSTuGxraw) | 2026-09-26 | 22.9 | 2026-10-19 12:02 | 9.55 | 11 281 197 | 1 181 223 | 413 412 | 2 014 | 73 · Shorts | 33 (19) | 32 200 | 350.3 | en/US | Giải thích 3D đồ vật/khoa học (có lịch sử) (vừa) | search | — |
| 4 | B | [Why Old Soda Bottles Couldn't Stand Up](https://www.youtube.com/watch?v=hRYWcfp6dsg) | [Trial & Eureka](https://www.youtube.com/channel/UCP8wHrwU79SSJUxu1PBmiNQ) | 2026-10-04 | 4.8 | 2026-10-09 10:50 | 19.6 | 14 082 971 | 718 510 | 431 697 | 1 237 | 78 · Shorts | 12 (4) | 23 900 | 589.2 | en/US | Lịch sử phát minh/kỹ thuật – hoạt hình giải thích (gần) | search | — |
| 5 | B | [Why Vending Machines Used to Take Washers](https://www.youtube.com/watch?v=v-K--ioiXms) | [Trial & Eureka](https://www.youtube.com/channel/UCP8wHrwU79SSJUxu1PBmiNQ) | 2026-10-04 | 6.3 | 2026-10-10 23:00 | 18.09 | 11 534 082 | 637 480 | 336 845 | 1 317 | 76 · Shorts | 12 (7) | 23 900 | 482.6 | en/US | Lịch sử phát minh/kỹ thuật – hoạt hình giải thích (gần) | search | — |
| 6 | B | [How an Accident Made Boats Faster #animation](https://www.youtube.com/watch?v=rv6qAgdPsXw) | [The Why Side](https://www.youtube.com/channel/UCjFTPUCLQucNHkHSTuGxraw) | 2026-09-26 | 2.8 | 2026-09-29 10:15 | 29.63 | 14 585 486 | 492 272 | 260 532 | 521 | 49 · Shorts | 33 (0) | 32 200 | 453.0 | en/US | Giải thích 3D đồ vật/khoa học (có lịch sử) (vừa) | uploads kênh | — |
| 7 | B | [The Truck You Don't Want Behind You](https://www.youtube.com/watch?v=vxnnsMcoCMs) | [The Why Side](https://www.youtube.com/channel/UCjFTPUCLQucNHkHSTuGxraw) | 2026-09-26 | 12.2 | 2026-10-08 21:24 | 20.16 | 9 750 827 | 483 565 | 147 328 | 897 | 39 · Shorts | 33 (11) | 32 200 | 302.8 | en/US | Giải thích 3D đồ vật/khoa học (có lịch sử) (vừa) | uploads kênh | — |
| 8 | B | [The Tiny Island That Stopped an Empire - Malta 1565](https://www.youtube.com/watch?v=W1blLBpUeZ8) | [History Maps Lore](https://www.youtube.com/channel/UCFREyVa1PdzGJLugAZmnfcg) | 2026-09-01 | 49.1 | 2026-10-20 05:00 | 8.84 | 2 217 484 | 250 715 | 40 023 | 1 246 | 85 · Shorts | 3 (1) | 3 730 | 594.5 | en/— | Lịch sử – bản đồ trận đánh (gần) | search | — |
| 9 | B | [Why Starting a Car Used to Break Wrists](https://www.youtube.com/watch?v=_VPnRrnsm-w) | [Trial & Eureka](https://www.youtube.com/channel/UCP8wHrwU79SSJUxu1PBmiNQ) | 2026-10-04 | 3.8 | 2026-10-08 11:41 | 20.57 | 4 570 522 | 222 203 | 113 070 | 474 | 74 · Shorts | 12 (3) | 23 900 | 191.2 | en/US | Lịch sử phát minh/kỹ thuật – hoạt hình giải thích (gần) | uploads kênh | — |
| 10 | B | [A Power Line Just Fell on Your Car](https://www.youtube.com/watch?v=1iMQv03XgbQ) | [The Why Side](https://www.youtube.com/channel/UCjFTPUCLQucNHkHSTuGxraw) | 2026-09-26 | 23.0 | 2026-10-19 15:45 | 9.4 | 1 913 940 | 203 615 | 112 699 | 1 035 | 65 · Shorts | 33 (20) | 32 200 | 59.4 | en/US | Giải thích 3D đồ vật/khoa học (có lịch sử) (vừa) | uploads kênh | — |
| 11 | B | [What If Your Pool Were Full of Mercury?](https://www.youtube.com/watch?v=hoOQvyVwphM) | [The Why Side](https://www.youtube.com/channel/UCjFTPUCLQucNHkHSTuGxraw) | 2026-09-26 | 12.9 | 2026-10-09 14:00 | 19.47 | 3 786 593 | 194 454 | 43 069 | 398 | 26 · Shorts | 33 (12) | 32 200 | 117.6 | en/US | Giải thích 3D đồ vật/khoa học (có lịch sử) (vừa) | uploads kênh | — |
| 12 | B | [Why the Navy Ripped This Off Its Ships](https://www.youtube.com/watch?v=Chv-phiUuu0) | [The Why Side](https://www.youtube.com/channel/UCjFTPUCLQucNHkHSTuGxraw) | 2026-09-26 | 5.9 | 2026-10-02 14:00 | 26.47 | 4 404 668 | 166 383 | 82 666 | 394 | 85 · Shorts | 33 (4) | 32 200 | 136.8 | en/US | Giải thích 3D đồ vật/khoa học (có lịch sử) (vừa) | uploads kênh | — |
| 13 | B | [Could You Survive a T. Rex by Standing Still?](https://www.youtube.com/watch?v=tI_UFQ6eOfU) | [The Why Side](https://www.youtube.com/channel/UCjFTPUCLQucNHkHSTuGxraw) | 2026-09-26 | 13.6 | 2026-10-10 05:48 | 18.81 | 2 988 705 | 158 851 | 204 131 | 1 876 | 36 · Shorts | 33 (16) | 32 200 | 92.8 | en/US | Giải thích 3D đồ vật/khoa học (có lịch sử) (vừa) | uploads kênh | — |
| 14 | B | [Why Darwin's Potatoes Wouldn't Cook](https://www.youtube.com/watch?v=pxdzLhsecCc) | [Trial & Eureka](https://www.youtube.com/channel/UCP8wHrwU79SSJUxu1PBmiNQ) | 2026-10-04 | 8.2 | 2026-10-12 19:38 | 16.24 | 1 889 183 | 116 341 | 38 214 | 292 | 76 · Shorts | 12 (9) | 23 900 | 79.0 | en/US | Lịch sử phát minh/kỹ thuật – hoạt hình giải thích (gần) | uploads kênh | — |
| 15 | B | [Why This Yellow Box Eats Guardrails](https://www.youtube.com/watch?v=coqlbmfsiO0) | [The Why Side](https://www.youtube.com/channel/UCjFTPUCLQucNHkHSTuGxraw) | 2026-09-26 | 8.9 | 2026-10-05 14:00 | 23.47 | 2 219 487 | 94 556 | 53 192 | 551 | 72 · Shorts | 33 (7) | 32 200 | 68.9 | en/US | Giải thích 3D đồ vật/khoa học (có lịch sử) (vừa) | uploads kênh | — |
| 16 | B | [How Did They Stop Champagne Bottles From Exploding](https://www.youtube.com/watch?v=isdTFTFn56c) | [The Why Side](https://www.youtube.com/channel/UCjFTPUCLQucNHkHSTuGxraw) | 2026-09-26 | 3.8 | 2026-09-30 10:10 | 28.63 | 2 634 471 | 92 010 | 49 884 | 155 | 49 · Shorts | 33 (1) | 32 200 | 81.8 | en/US | Giải thích 3D đồ vật/khoa học (có lịch sử) (vừa) | uploads kênh | — |
| 17 | B | [Hot Tea in an Upside-Down Plane](https://www.youtube.com/watch?v=ypLZ-ycETCM) | [The Why Side](https://www.youtube.com/channel/UCjFTPUCLQucNHkHSTuGxraw) | 2026-09-26 | 13.1 | 2026-10-09 17:00 | 19.35 | 1 746 537 | 90 270 | 24 804 | 114 | 39 · Shorts | 33 (13) | 32 200 | 54.2 | en/US | Giải thích 3D đồ vật/khoa học (có lịch sử) (vừa) | uploads kênh | — |
| 18 | B | [The Genius Way to Stop a Train](https://www.youtube.com/watch?v=60L_nyl3MsE) | [Trial & Eureka](https://www.youtube.com/channel/UCP8wHrwU79SSJUxu1PBmiNQ) | 2026-10-04 | 1.9 | 2026-10-06 12:21 | 22.54 | 1 885 013 | 83 623 | 37 130 | 247 | 79 · Shorts | 12 (1) | 23 900 | 78.9 | en/US | Lịch sử phát minh/kỹ thuật – hoạt hình giải thích (gần) | uploads kênh | — |

*Ngoài ngách (xa), không vào bảng:* Telugu Learning with Anika 49 158 646 (Trẻ em – học tiếng Telugu); Telugu Learning with Anika 10 032 912 (Trẻ em – học tiếng Telugu); Telugu Learning with Anika 3 923 581 (Trẻ em – học tiếng Telugu); Telugu Learning with Anika 4 812 857 (Trẻ em – học tiếng Telugu); SM Create 4 429 759 (Nhạc Hindi so sánh); Telugu Learning with Anika 4 722 552 (Trẻ em – học tiếng Telugu); Love Nostalgia 1 165 904 (Meme hoài niệm then vs now); Telugu Learning with Anika 69 631 620 (Trẻ em – học tiếng Telugu); Telugu Learning with Anika 43 068 962 (Trẻ em – học tiếng Telugu); Love Nostalgia 18 566 571 (Meme hoài niệm then vs now); Love Nostalgia 16 522 553 (Meme hoài niệm then vs now); Telugu Learning with Anika 7 000 536 (Trẻ em – học tiếng Telugu); Telugu Learning with Anika 9 005 381 (Trẻ em – học tiếng Telugu); Telugu Learning with Anika 3 994 497 (Trẻ em – học tiếng Telugu); Telugu Learning with Anika 7 070 923 (Trẻ em – học tiếng Telugu); AO3DP Motion 6 475 328 (In 3D hoạt hình); Love Nostalgia 3 793 586 (Meme hoài niệm then vs now); Telugu Learning with Anika 10 246 341 (Trẻ em – học tiếng Telugu); Telugu Learning with Anika 5 734 282 (Trẻ em – học tiếng Telugu); Twig by Twig 5 006 423 (Chim làm tổ (macro)); Love Nostalgia 3 761 373 (Meme hoài niệm then vs now); Telugu Learning with Anika 3 692 655 (Trẻ em – học tiếng Telugu); Telugu Learning with Anika 5 524 160 (Trẻ em – học tiếng Telugu); SM Create 3 436 667 (Nhạc Hindi so sánh); Telugu Learning with Anika 2 345 169 (Trẻ em – học tiếng Telugu); SM Create 4 912 667 (Nhạc Hindi so sánh); Love Nostalgia 3 593 040 (Meme hoài niệm then vs now); Telugu Learning with Anika 2 521 120 (Trẻ em – học tiếng Telugu)

### 3.4 Shorts · M2 (không gồm M1): 18 video ngách (A 3) — không đủ 20
| # | Hạng | Video | Kênh | Kênh tạo | Tuổi kênh lúc đăng (ngày) | Đăng (UTC) | Tuổi video (ngày) | Xem | Xem/ngày | Thích | BL | Dài (s) · nhóm | Video kênh (trước) | Đăng ký | Xem/ĐK | NN/QG | Ngách | Nguồn | Cờ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | A | [Why You Couldn't Survive Inside a Whale 🐋](https://www.youtube.com/watch?v=6_H30uAL0jA) | [One Wild Story](https://www.youtube.com/channel/UCm17VXHNs8VhKOzVrnAmPCw) | 2026-10-05 | 19.2 | 2026-10-24 21:08 | 4.18 | 707 122 | 169 354 | 10 913 | 88 | 59 · Shorts | 31 (22) | 2 910 | 243.0 | en/— | Khoa học "what if"/tò mò (vừa) | uploads kênh | — |
| 2 | A | [If You Were Frozen for 100 Years](https://www.youtube.com/watch?v=SOJ_TGbQ194) | [One Wild Story](https://www.youtube.com/channel/UCm17VXHNs8VhKOzVrnAmPCw) | 2026-10-05 | 17.8 | 2026-10-23 10:04 | 5.64 | 841 993 | 149 374 | 29 671 | 333 | 62 · Shorts | 31 (19) | 2 910 | 289.3 | en/— | Khoa học "what if"/tò mò (vừa) | uploads kênh | — |
| 3 | A | [If a Zombie Bit You](https://www.youtube.com/watch?v=fykKB3yLnEQ) | [One Wild Story](https://www.youtube.com/channel/UCm17VXHNs8VhKOzVrnAmPCw) | 2026-10-05 | 17.2 | 2026-10-22 21:01 | 6.18 | 429 227 | 69 448 | 8 352 | 155 | 62 · Shorts | 31 (18) | 2 910 | 147.5 | en/— | Khoa học "what if"/tò mò (vừa) | uploads kênh | — |
| 4 | B | [America Has No Base in Taiwan #usa #taiwan #geography](https://www.youtube.com/watch?v=HgLgA9VGjkk) | [Whyograph](https://www.youtube.com/channel/UCj8ovMHnMmCUZjditRhiQ0Q) | 2026-10-14 | 5.6 | 2026-10-20 05:41 | 8.81 | 807 891 | 91 650 | 11 735 | 798 | 80 · Shorts | 11 (2) | 2 800 | 288.5 | en/— | Bản đồ – địa chính trị (gần) | search | — |
| 5 | B | [A Fleck of Paint Blinded Hubble](https://www.youtube.com/watch?v=dG1ON0TgW6s) | [The Why Side](https://www.youtube.com/channel/UCjFTPUCLQucNHkHSTuGxraw) | 2026-09-26 | 8.0 | 2026-10-04 16:11 | 24.38 | 1 802 479 | 73 927 | 41 738 | 164 | 69 · Shorts | 33 (6) | 32 200 | 56.0 | en/US | Giải thích 3D đồ vật/khoa học (có lịch sử) (vừa) | uploads kênh | — |
| 6 | B | [Why Does This Highway Wall Make Your Car Climb?](https://www.youtube.com/watch?v=bhZ_vUQkhQY) | [The Why Side](https://www.youtube.com/channel/UCjFTPUCLQucNHkHSTuGxraw) | 2026-09-26 | 22.0 | 2026-10-18 15:45 | 10.4 | 765 449 | 73 600 | 14 553 | 108 | 64 · Shorts | 33 (18) | 32 200 | 23.8 | en/US | Giải thích 3D đồ vật/khoa học (có lịch sử) (vừa) | uploads kênh | — |
| 7 | B | [Why Revolving Doors Are Built to Collapse](https://www.youtube.com/watch?v=8rKvHfgsG-U) | [The Why Side](https://www.youtube.com/channel/UCjFTPUCLQucNHkHSTuGxraw) | 2026-09-26 | 4.4 | 2026-10-01 02:09 | 27.97 | 1 688 535 | 60 377 | 33 506 | 488 | 58 · Shorts | 33 (2) | 32 200 | 52.4 | en/US | Giải thích 3D đồ vật/khoa học (có lịch sử) (vừa) | uploads kênh | — |
| 8 | B | [Why Plugging In a Hair Dryer Used to Be Deadly](https://www.youtube.com/watch?v=Ca6for73bI0) | [Trial & Eureka](https://www.youtube.com/channel/UCP8wHrwU79SSJUxu1PBmiNQ) | 2026-10-04 | 5.9 | 2026-10-10 12:44 | 18.53 | 918 625 | 49 586 | 22 873 | 193 | 76 · Shorts | 12 (6) | 23 900 | 38.4 | en/US | Lịch sử phát minh/kỹ thuật – hoạt hình giải thích (gần) | uploads kênh | — |
| 9 | B | [Why This Reflector Wants To Be Run Over](https://www.youtube.com/watch?v=NUc2-5UaPd4) | [The Why Side](https://www.youtube.com/channel/UCjFTPUCLQucNHkHSTuGxraw) | 2026-09-26 | 13.2 | 2026-10-09 21:08 | 19.18 | 928 295 | 48 411 | 10 488 | 77 | 29 · Shorts | 33 (14) | 32 200 | 28.8 | en/US | Giải thích 3D đồ vật/khoa học (có lịch sử) (vừa) | uploads kênh | — |
| 10 | B | [There's Nothing We Can Do... French Empire #geography #hi…](https://www.youtube.com/watch?v=Qd_uWXltjLE) | [Geoevum](https://www.youtube.com/channel/UC6oI5aYgYoaqYQ-yL4w5d-g) | 2026-09-04 | 32.1 | 2026-10-06 11:02 | 22.59 | 1 087 789 | 48 150 | 9 885 | 117 | 25 · Shorts | 25 (18) | 12 300 | 88.4 | en/TR | Bản đồ lịch sử – đế quốc (gần) | search | — |
| 11 | B | [Why Matches Used to Catch Fire in Your Pocket](https://www.youtube.com/watch?v=O4s8lFgipsk) | [Trial & Eureka](https://www.youtube.com/channel/UCP8wHrwU79SSJUxu1PBmiNQ) | 2026-10-04 | 5.4 | 2026-10-10 00:12 | 19.05 | 870 236 | 45 687 | 19 849 | 196 | 80 · Shorts | 12 (5) | 23 900 | 36.4 | en/US | Lịch sử phát minh/kỹ thuật – hoạt hình giải thích (gần) | uploads kênh | — |
| 12 | B | [One World Trade Center - How New York Rebuilt the World T…](https://www.youtube.com/watch?v=cA9kE36NCRk) | [LAYERS](https://www.youtube.com/channel/UCwC00zWVEXFIK-3JbEdIF6w) | 2026-08-13 | 54.0 | 2026-10-06 15:03 | 22.43 | 964 432 | 42 999 | 20 176 | 534 | 103 · Shorts | 256 (107) | 30 800 | 31.3 | en/US | How it was built – công trình (kênh tổng hợp) (gần) | uploads kênh | — |
| 13 | B | [How a Tree Grows](https://www.youtube.com/watch?v=Ky6BJF_tT3s) | [One Wild Story](https://www.youtube.com/channel/UCm17VXHNs8VhKOzVrnAmPCw) | 2026-10-05 | 12.8 | 2026-10-18 12:10 | 10.55 | 446 179 | 42 294 | 6 725 | 17 | 46 · Shorts | 31 (12) | 2 910 | 153.3 | en/— | Khoa học "what if"/tò mò (vừa) | uploads kênh | — |
| 14 | B | [The Engine That Lifted Astronauts Off the Moon Had No Ign…](https://www.youtube.com/watch?v=5leZjiCDe8Y) | [Why It's Built](https://www.youtube.com/channel/UC6REYiUgOmsnKKLrGXxkmUA) | 2026-08-19 | 56.9 | 2026-10-15 00:00 | 14.06 | 588 189 | 41 845 | 9 703 | 925 | 63 · Shorts | 83 (62) | 1 580 | 372.3 | en/US | Kỹ thuật – vì sao xây thế (gần) | uploads kênh | — |
| 15 | B | [There's Nothing We Can Do... Soviet Union #geography #his…](https://www.youtube.com/watch?v=zWAvEO5CF88) | [Geoevum](https://www.youtube.com/channel/UC6oI5aYgYoaqYQ-yL4w5d-g) | 2026-09-04 | 36.9 | 2026-10-11 06:34 | 17.78 | 658 398 | 37 025 | 6 269 | 99 | 25 · Shorts | 25 (19) | 12 300 | 53.5 | en/TR | Bản đồ lịch sử – đế quốc (gần) | uploads kênh | — |
| 16 | B | [Why the First LEGO Bricks Fell Apart](https://www.youtube.com/watch?v=rSjHtiLR-wM) | [Trial & Eureka](https://www.youtube.com/channel/UCP8wHrwU79SSJUxu1PBmiNQ) | 2026-10-04 | 10.4 | 2026-10-15 01:32 | 13.99 | 498 201 | 35 605 | 10 006 | 133 | 76 · Shorts | 12 (11) | 23 900 | 20.8 | en/US | Lịch sử phát minh/kỹ thuật – hoạt hình giải thích (gần) | uploads kênh | — |
| 17 | B | [Your Bike Is Hiding a Giant Wheel](https://www.youtube.com/watch?v=4IrFlbY8DGo) | [The Why Side](https://www.youtube.com/channel/UCjFTPUCLQucNHkHSTuGxraw) | 2026-09-26 | 9.9 | 2026-10-06 14:00 | 22.47 | 734 091 | 32 665 | 14 027 | 83 | 75 · Shorts | 33 (8) | 32 200 | 22.8 | en/US | Giải thích 3D đồ vật/khoa học (có lịch sử) (vừa) | uploads kênh | — |
| 18 | B | [State Farm Stadium - How Arizona Built the First Stadium …](https://www.youtube.com/watch?v=rpXb8ZYiy-M) | [LAYERS](https://www.youtube.com/channel/UCwC00zWVEXFIK-3JbEdIF6w) | 2026-08-13 | 59.3 | 2026-10-11 23:41 | 17.07 | 496 943 | 29 113 | 8 808 | 244 | 106 · Shorts | 256 (137) | 30 800 | 16.1 | en/US | How it was built – công trình (kênh tổng hợp) (gần) | uploads kênh | — |

*Ngoài ngách (xa), không vào bảng:* Telugu Learning with Anika 902 243 (Trẻ em – học tiếng Telugu); SM Create 461 495 (Nhạc Hindi so sánh); Love Nostalgia 630 889 (Meme hoài niệm then vs now); SM Create 536 640 (Nhạc Hindi so sánh); AO3DP Motion 1 089 223 (In 3D hoạt hình); Love Nostalgia 1 183 567 (Meme hoài niệm then vs now); Telugu Learning with Anika 1 399 649 (Trẻ em – học tiếng Telugu); Telugu Learning with Anika 1 779 149 (Trẻ em – học tiếng Telugu); Telugu Learning with Anika 1 488 986 (Trẻ em – học tiếng Telugu); Twig by Twig 943 477 (Chim làm tổ (macro)); Telugu Learning with Anika 1 241 018 (Trẻ em – học tiếng Telugu); Telugu Learning with Anika 1 520 503 (Trẻ em – học tiếng Telugu); Telugu Learning with Anika 1 096 982 (Trẻ em – học tiếng Telugu); SM Create 1 442 787 (Nhạc Hindi so sánh); SM Create 1 270 900 (Nhạc Hindi so sánh); AO3DP Motion 421 895 (In 3D hoạt hình); Twig by Twig 782 924 (Chim làm tổ (macro)); Telugu Learning with Anika 599 964 (Trẻ em – học tiếng Telugu); SM Create 740 894 (Nhạc Hindi so sánh); AO3DP Motion 569 093 (In 3D hoạt hình); Twig by Twig 465 987 (Chim làm tổ (macro)); AO3DP Motion 593 419 (In 3D hoạt hình); Telugu Learning with Anika 632 972 (Trẻ em – học tiếng Telugu); Telugu Learning with Anika 611 667 (Trẻ em – học tiếng Telugu)

### 3.5 Kênh ngách gần/vừa cần theo dõi (≤ 90 ngày tuổi lúc đo, xếp theo đăng ký/ngày tuổi kênh; 15 kênh)
| # | Kênh | Ngách | Tạo | Tuổi (ngày) | Đăng ký | ĐK/ngày | Video (30 ngày: Shorts/dài) | Nhịp (video/ngày) | M2 (M1) | Video cao nhất | Cờ AI |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | [The Why Side](https://www.youtube.com/channel/UCjFTPUCLQucNHkHSTuGxraw) | Giải thích 3D đồ vật/khoa học (có lịch sử) (vừa) | 2026-09-26 | 32.4 | 32 200 | 994 | 33 (33/0) | 1.11 | 16 (11) | [How an Accident Made Boats Faster #animation](https://www.youtube.com/watch?v=rv6qAgdPsXw) — 14 585 486, 49 s | — |
| 2 | [Trial & Eureka](https://www.youtube.com/channel/UCP8wHrwU79SSJUxu1PBmiNQ) | Lịch sử phát minh/kỹ thuật – hoạt hình giải thích (gần) | 2026-10-04 | 24.4 | 23 900 | 979 | 12 (12/0) | 0.51 | 8 (5) | [Why Old Soda Bottles Couldn't Stand Up](https://www.youtube.com/watch?v=hRYWcfp6dsg) — 14 082 971, 78 s | — |
| 3 | [LAYERS](https://www.youtube.com/channel/UCwC00zWVEXFIK-3JbEdIF6w) | How it was built – công trình (kênh tổng hợp) (gần) | 2026-08-13 | 76.4 | 30 800 | 403 | 256 (163/0) | 3.4 | 2 (0) | [One World Trade Center - How New York Rebuilt the Wo…](https://www.youtube.com/watch?v=cA9kE36NCRk) — 964 432, 103 s | — |
| 4 | [CityEons](https://www.youtube.com/channel/UCi216jUuIATe6cfr_pNRdvQ) | 3D timelapse thành phố (gần) | 2026-10-03 | 25.4 | 6 770 | 266 | 5 (0/5) | 0.21 | 3 (1) | [Watch NEW YORK Grow for 400 Years - 3D Timelapse (No…](https://www.youtube.com/watch?v=Xn1s4JvDKYY) — 1 605 745, 538 s | tự khai "No AI" |
| 5 | [Geoevum](https://www.youtube.com/channel/UC6oI5aYgYoaqYQ-yL4w5d-g) | Bản đồ lịch sử – đế quốc (gần) | 2026-09-04 | 54.7 | 12 300 | 225 | 25 (8/0) | 0.46 | 2 (0) | [There's Nothing We Can Do... French Empire #geograph…](https://www.youtube.com/watch?v=Qd_uWXltjLE) — 1 087 789, 25 s | — |
| 6 | [Whyograph](https://www.youtube.com/channel/UCj8ovMHnMmCUZjditRhiQ0Q) | Bản đồ – địa chính trị (gần) | 2026-10-14 | 14.4 | 2 800 | 194 | 11 (10/1) | 0.76 | 2 (1) | [India Controls Bangladesh’s Biggest River #india #ba…](https://www.youtube.com/watch?v=QQbUPpVQ1ko) — 1 010 902, 71 s | — |
| 7 | [Buried Evidence](https://www.youtube.com/channel/UCdAO08RVzexvMw24cir112g) | Tài liệu khảo cổ/địa chất (gần) | 2026-10-09 | 20.0 | 2 560 | 128 | 17 (1/16) | 0.85 | 2 (1) | [Geologists Just Found Out What Wyoming’s Devils Towe…](https://www.youtube.com/watch?v=id-q1bhqjNU) — 2 927 374, 1067 s | — |
| 8 | [One Wild Story](https://www.youtube.com/channel/UCm17VXHNs8VhKOzVrnAmPCw) | Khoa học "what if"/tò mò (vừa) | 2026-10-05 | 23.4 | 2 910 | 124 | 31 (31/0) | 1.37 | 4 (0) | [If You Were Frozen for 100 Years](https://www.youtube.com/watch?v=SOJ_TGbQ194) — 841 993, 62 s | — |
| 9 | [Urbavision](https://www.youtube.com/channel/UC6lDuGFqhHk9huXaKWiztmA) | 3D timelapse thành phố (gần) | 2026-10-07 | 21.5 | 2 420 | 113 | 12 (2/10) | 0.56 | 0 (0) | [São Paulo: 500 Years in 7 Minutes / 3D Timelapse (15…](https://www.youtube.com/watch?v=nzY1lqQZjPU) — 322 647, 411 s | — |
| 10 | [UncoveredHistoryLGC](https://www.youtube.com/channel/UCLBgwl-1RO2RkDpMGkfoFAg) | Lịch sử tổng hợp (gần) | 2026-08-03 | 86.7 | 8 580 | 99 | 141 (32/10) | 1.63 | 0 (0) | [Viral Prompt for Uncovered History / Uncovered History](https://www.youtube.com/watch?v=aQeFj4ZfnXE) — 19 746, 670 s | AI tự khai (giọng/công cụ) |
| 11 | [History Maps Lore](https://www.youtube.com/channel/UCFREyVa1PdzGJLugAZmnfcg) | Lịch sử – bản đồ trận đánh (gần) | 2026-09-01 | 57.9 | 3 730 | 64 | 3 (3/0) | 0.31 | 1 (1) | [The Tiny Island That Stopped an Empire - Malta 1565](https://www.youtube.com/watch?v=W1blLBpUeZ8) — 2 217 484, 85 s | — |
| 12 | [Florida Gilded](https://www.youtube.com/channel/UChXe_TMHI1rIZtT9kAYHnMw) | Lịch sử địa phương – dinh thự (gần) | 2026-08-25 | 64.5 | 3 380 | 52 | 25 (1/15) | 0.54 | 0 (0) | [How St. Petersburg's Old Money Built a Dream Island …](https://www.youtube.com/watch?v=AgIpn1lfDMk) — 288 942, 1901 s | — |
| 13 | [The Real Pennsylvania](https://www.youtube.com/channel/UCOFlPOGq4ENLsO586_grmdw) | Lịch sử/xếp hạng địa phương (vừa) | 2026-09-16 | 42.1 | 1 770 | 42 | 30 (0/28) | 0.96 | 0 (0) | [The Most Famous Athlete From Every Pennsylvania County](https://www.youtube.com/watch?v=UMqVkNArerA) — 67 590, 1218 s | — |
| 14 | [nobodycareswhatiswrittenhere](https://www.youtube.com/channel/UCbPBsWlmBR5UA_WZwHn-IMw) | 3D timelapse thành phố (gần) | 2026-09-10 | 48.2 | 1 940 | 40 | 33 (1/11) | 0.69 | 0 (0) | [3D Timelapse – Buenos Aires (1536–2026)](https://www.youtube.com/watch?v=LehvCwvCfbg) — 248 710, 491 s | — |
| 15 | [The City Clock](https://www.youtube.com/channel/UC4hYqCraGiXHy0pla4jdjLQ) | 3D timelapse thành phố (gần) | 2026-10-13 | 15.5 | 368 | 24 | 12 (9/3) | 0.78 | 0 (0) | [7,400 Years of Belgrade in 8 Minutes, Built from Rea…](https://www.youtube.com/watch?v=VDPGINqfy-Q) — 148 009, 509 s | tự khai "No AI" |

Cột “Video (30 ngày: Shorts/dài)” = tổng video kênh (số Shorts / dài đăng trong 30 ngày). Nhịp = video/ngày từ video đầu.

## §4. Phân tích
Số liệu dưới đây tính trên **46 video M2 thuộc ngách gần/vừa**: 36 Shorts và 10 video dài, của 12 kênh. 35/46 video thuộc kênh ≤ 30 ngày tuổi lúc đăng. Chỉ 5/46 là hạng A, gồm 5 Shorts; còn lại là hạng B (ước). Trung vị lượt xem/người đăng ký là 85.

### (a) Video dài có bùng nổ ở kênh mới trong ngách này không? Độ dài nào?
**Có, nhưng chỉ ở hạng B (ước). 0 video dài hạng A.** 10 video dài đạt M2 (4 trong số đó đạt M1), thuộc 4 kênh:

| Nhóm độ dài | Số video | Kênh · format | Lượt xem |
|---|---|---|---|
| 3–10 phút | 3 | CityEons, kênh 2–14 ngày tuổi · 3D timelapse thành phố, không lời | 0,66–1,61 triệu |
| 10–20 phút | 2 | Buried Evidence, kênh 1–3 ngày tuổi · tài liệu khảo cổ/địa chất có lời dẫn | 0,91–2,93 triệu |
| > 20 phút | 5 | Ambrose Discovery, kênh 78–87 ngày · tài liệu xác tàu/bí ẩn, 21 phút; Sin Coordenadas, kênh 79–87 ngày · tài liệu địa lý quốc gia tiếng Tây Ban Nha, 39–44 phút | 0,83–4,18 triệu |

- Hai đường thắng rõ:
  - 3D timelapse **ngắn, 5–10 phút**, không lời. CityEons đạt 3/5 video.
  - Tài liệu có lời dẫn **dài trên 17 phút** với móc tò mò kiểu “just found out / what it captured”.
- Không có video M2 nào dài 10–17 phút như T3 (12:43). Hai video nhóm 10–20 phút đều dài ≈ 18 phút và là tài liệu có lời dẫn của Buried Evidence. Không có video 3D timelapse không lời nào ở nhóm 10–20 phút đạt M2. Urbis Anno đăng 6 video 10–12 phút; video cao nhất là Budapest với 176 323 lượt, các video còn lại ≤ 2 365.
- Ngoài ngách, video dài đạt M1 gồm Ali Wildlife Hunt (tài liệu động vật, AI tự khai) và CineFlex (phim truyện đầy đủ, nghi đăng lại).

### (b) Mẫu tiêu đề
So sánh video đạt M2 với video không đạt M2 của **cùng các kênh ngách** trong 30 ngày: 383 Shorts và 193 video dài không đạt M2.

| Chỉ số (trung vị / tỷ lệ) | Shorts M2 (36) | Shorts không M2 (383) | Dài M2 (10) | Dài không M2 (193) |
|---|---|---|---|---|
| Ký tự / từ | 40 / 8 | 58 / 10 | 67,5 / 12 | 72 / 12 |
| Có “Why/How” | **50 %** | 38 % | **0 %** | 17 % |
| Câu hỏi “?” | 8 % | 4 % | 0 % | 8 % |
| Có chữ số | **6 %** | 26 % | **60 %** | 34 % |
| Có năm (4 chữ số) | 3 % | 4 % | 0 % | 12 % |
| Có “#” | 14 % | 17 % | 0 % | 5 % |
| Có dấu phân cách “\|”, “ - ”, “:” | **8 %** | 49 % | 60 % | 32 % |

- **Shorts thắng:** một câu ngắn kể một bí ẩn hoặc một nghịch lý. Ví dụ:
  - “Why Old Soda Bottles Couldn't Stand Up”: 14,1 triệu.
  - “He Put His Head in a Particle Accelerator”: 11,3 triệu.
  - “The Tiny Island That Stopped an Empire - Malta 1565”: 2,2 triệu.
  - “India Controls Bangladesh's Biggest River”: 1,0 triệu, hạng A.
  - Hiếm có số, năm hay dấu phân cách. Địa danh, nếu có, nằm trong câu kể: Malta, Bangladesh, Taiwan.
- **Video dài thắng:**
  - Số lớn dạng khoảng thời gian: “400 Years”, “2,000 Years”, “3,000 Years”.
  - Tên địa danh viết HOA: “NEW YORK”, “IRÁN”, “RUSIA”.
  - Mẫu cố định của kênh: “Watch X Grow for N Years - 3D Timelapse (No AI imagery)”; “COUNTRY | El País Más … | Documental 4K”.
  - Hoặc móc khám phá: “Archaeologists Just Found Out What … Actually Reveal”; “… — What It Captured Was Beyond Terrifying”.
  - **Không** video dài nào dùng “Why/How”.
- Đây là tương quan trong một mẫu nhỏ và lệch (§2), không phải quan hệ nhân quả.

### (c) Mô tả kiểu thumbnail suy từ văn bản (không tải ảnh)
API không trả nội dung ảnh. Văn bản chỉ cho biết các điểm sau:
- **CityEons:** tiêu đề viết HOA tên thành phố. Mô tả nói “in 4K”, “3D timelapse … built from real geodata and historical research”. Kênh tự khai “No AI imagery. No narration. Just the city, the years and the music”. Không có dữ kiện nào về chữ hay hình trên thumbnail.
- **Sin Coordenadas:** tiêu đề nhấn “Documental 4K” và tên nước viết HOA. Thẻ là các địa danh và từ “4K”, “naturaleza”.
- **Geoevum:** mô tả kênh “history in 30-second map edits … borders era by era”. Tiêu đề lặp câu meme “There's Nothing We Can Do…”, tức dạng map edit kèm câu thoại meme.
- **Trial & Eureka, The Why Side:**
  - The Why Side tự gọi là “A 3D animated explainer”. Mô tả kênh: “Short animated explanations of everyday objects”.
  - Trial & Eureka kể chuyện phát minh theo khung “From [vật hỏng] to [vật hôm nay]. How engineers learned, one failure at a time…”.
- Không văn bản nào mô tả bố cục hay chữ trên thumbnail. Các điểm trên chỉ suy ra **chủ đề hình** chứ không suy ra thiết kế thumbnail.

### (d) Nhịp đăng và số video trước video bùng nổ
- Số video kênh đã đăng trước video M2 (46 video): trung vị **11**, dải 0–137.
  - 2 video là video đầu tiên của kênh: The Why Side “How an Accident Made Boats Faster” 14,6 triệu; CityEons “Watch LONDON Grow…”.
  - 12/46 video có ≤ 3 video trước đó.
- Nhịp đăng:
  - Kênh Shorts thắng đăng dày: The Why Side 1,11 video/ngày (33 video trong 30 ngày); One Wild Story 1,37; Trial & Eureka 0,51 (12 video trong 24 ngày); Whyograph 0,76.
  - Kênh dài thắng đăng thưa: CityEons 0,21 (5 video trong 25 ngày); Sin Coordenadas 20 video trong 92 ngày; Buried Evidence 0,85.
- **CityEons theo thời gian:** London (video 1) 27 752 lượt/ngày → Berlin 15 734 → Rome 50 764 → New York (video 4) 138 104 → Athens (video 5, 3,7 ngày tuổi) 3 109. Bùng nổ đến ở video thứ 3–4 của một **chuỗi cùng format**, không đến ở video đầu.

### (e) Shorts dẫn sang video dài
- API không có trường “Video liên quan” của Shorts. Phiên chỉ thấy được liên kết khi nó nằm trong mô tả.
- Trong 419 Shorts của kênh ngách, chỉ 3 kênh 3D timelapse dẫn link sang bản dài:
  - The City Clock: 9/9 Shorts, mô tả có “Full 8-minute timelapse: …”.
  - Urbis Anno: 2/2 Shorts, mô tả có “the full 11-minute video: …”.
  - nobodycareswhatiswrittenhere: 1 Short.
- Các Shorts này đạt **151–2 446 lượt**. Bản dài của chúng đạt 761–176 323. Không Shorts nào trong số đó đạt M2.
- **Không Shorts M2 nào trong 36 video ngách dẫn link sang video dài.** Các kênh Shorts thắng (The Why Side, Trial & Eureka, Whyograph, History Maps Lore, Geoevum) **chỉ đăng Shorts**, hoặc chỉ có 1 video dài.

### (f) AI tự khai
- 622 video ngách (gần/vừa) trong 30 ngày: **39 video tự khai AI**, trong đó **0 video đạt M2**.
  - **AI giả tư liệu thật** (tự khai hình AI cho cảnh lịch sử như thật): 19 video của 3 kênh.
    - Why It's Built: 16 video Apollo/NASA (15 Shorts, 1 video dài), “Some scenes are AI-generated illustrations of moments no camera recorded”, 129–63 986 lượt. Video M2 duy nhất của kênh, “The Engine That Lifted Astronauts…” (588 189 lượt), **không** có câu tự khai này.
    - Kwento ng Mundo: 2 video, “AI-assisted archival-style illustrations”.
    - World Discovery Z: 1 video, “AI-generated scanning scenes”.
  - **AI tự khai khác** (giọng AI hoặc hình AI cho cảnh không phải lịch sử):
    - Hownatomy: “3D animation and an AI voice”.
    - How It Was Built: “AI voice”.
    - Slatescope: “Voice: AI (ElevenLabs)”, “Visuals are AI-generated illustrations”.
    - The Manufacturing Lens: “AI-generated documentary reconstruction” ở cảnh nhà máy.
    - UncoveredHistoryLGC: 1 video giới thiệu “viral AI prompt”.
  - **Tự khai “No AI”:** CityEons (cả 5 video, kèm trong tiêu đề) và The City Clock (cả 12 video). CityEons là kênh 3D timelapse duy nhất có video đạt M2.
- Ngoài ngách:
  - Ali Wildlife Hunt: video M1 4,7 triệu tự khai “AI-assisted visual recreations”.
  - Twig by Twig: một phần video tự khai “AI-generated wildlife reconstruction”, và kênh có video M1/M2. Phiên chưa đối chiếu video M2 nào của kênh có câu tự khai.
  - Cả hai đều dựng thiên nhiên như thật, không phải cảnh lịch sử.
- Trường `status.containsSyntheticMedia` không được dùng: NC-VIRAL đã thấy trường này không trả giá trị.

### (g) Đối chiếu T3 Gibraltar của Moving Parts
Số liệu T3 lấy từ đề bài chủ dự án: video dài 12:43, 2 lượt hiển thị sau 7,5 h; Short 0:49, 257 lượt sau 21 h.

| Khía cạnh | T3 Gibraltar | Mẫu NV-2 (kênh mới, ngách gần) |
|---|---|---|
| Tiêu đề dài | “Gibraltar: Why Everyone Fought for This Rock”: 44 ký tự, có “Why”, có “:”, không số | 10 video dài M2: 0 % có “Why/How”, 60 % có số (thường là “N Years”), tên địa danh viết HOA. Mẫu 3D timelapse thắng duy nhất là “Watch X Grow for N Years - 3D Timelapse (No AI imagery)” |
| Độ dài video dài | 12:43 | 3D timelapse thắng dài **4:51–9:58**: CityEons Berlin 291 s, London 322 s, New York 538 s, Rome 598 s. Video 10–20 phút thắng đều là tài liệu có lời dẫn trên 17 phút. 3D timelapse 10–15 phút (Urbis Anno, nobodycares, The City Clock): 0/10 đạt M2 |
| Format Short | “Gibraltar, 1704 → 2026 \| 3D Timelapse”, 0:49 | Cùng dạng “thành phố, năm → năm”: Urbis Anno “Amsterdam, 1262 → 2026 in 1:49” 1 324 lượt sau 20 ngày; The City Clock “… Years of X in 45 Seconds (No AI)” 151–2 446; Urbavision “London: 2,000 Years in 50 Seconds” 2 303 sau 19 ngày. **0/14 Shorts 3D timelapse của kênh mới đạt M2; cao nhất 2 615 lượt** |
| Short thắng cùng chủ đề | — | “The Tiny Island That Stopped an Empire - Malta 1565” (History Maps Lore, 85 s, 2,2 triệu, kênh có 3 video). Cùng loại chuyện vây hãm pháo đài đảo như Gibraltar, nhưng là **một câu chuyện có nhân vật/tình thế**, không phải timelapse năm → năm |
| Shorts → dài | Short quảng bá video dài | Kênh dẫn link (The City Clock, Urbis Anno) không thấy hiệu quả lên bản dài trong 30 ngày (§4e) |

- 257 lượt sau 21 h của T3 nằm trong dải của các Shorts 3D timelapse kênh mới (151–2 615 sau 5–23 ngày).
- Phiên không đo được lượt hiển thị (impression) của kênh khác. API công khai không trả số này, nên chỉ số “2 lượt hiển thị” của T3 không có điểm so sánh.

### (h) Giả thuyết có thể thử cho T4 London
Đây là **giả thuyết từ mẫu nhỏ và lệch**, không phải lựa chọn. Chủ dự án quyết định.

**Bối cảnh cạnh tranh:** trong 30 ngày đã có **3 kênh mới đăng London 3D timelapse**:
- CityEons “Watch LONDON Grow for 2,000 Years”: 322 s, 658 049 lượt.
- Urbavision “London: 2,000 Years in 7 Minutes”: 7 725 lượt, kèm Short 2 303 lượt.
- nobodycareswhatiswrittenhere “3D Timelapse – London (47–2026)”: 876 s, 5 597 lượt.

1. **H1 · Shorts kể chuyện, không timelapse năm → năm.** Mỗi Short kể một chuyện London có tình thế rõ, dài 60–85 s (trung vị Shorts thắng là 67 s). Tiêu đề là một câu kể, khoảng 8 từ, không có khoảng năm hay dấu “|”. 3D timelapse chỉ làm hình nền, không làm tiền đề. Căn cứ:
   - Malta 1565: 2,2 triệu.
   - Trial & Eureka: “From X to Y, one failure at a time”, 0,5–14 triệu.
   - Shorts dạng năm → năm: tối đa 2 615 lượt.
2. **H2 · Video dài 3D timelapse 5–10 phút thay vì 12–13 phút.** Cả 3/3 video 3D timelapse không lời đạt M2 dài 291–598 s; 10/10 video 3D timelapse 10–15 phút của kênh mới không đạt. Nếu giữ trên 10 phút thì cần lời dẫn tài liệu có móc tò mò (mẫu Buried Evidence, Ambrose).
3. **H3 · Tiêu đề dài: thử dạng mệnh lệnh “Watch … Grow / N Years”, hoặc tách hẳn khỏi khung “2,000 năm London” đã có 3 kênh chiếm.** Video dài M2 không dùng “Why/How”, còn 60 % có “N Years”. Rủi ro: tên “Watch LONDON Grow for 2,000 Years” đã là của CityEons. Dùng cùng khung dễ bị xem là sao chép format và cạnh tranh trực diện. Cần cân với luật “không sao chép” của dự án, ví dụ chọn một góc riêng (một sự kiện, một con phố, một thế kỷ).
4. **H4 · Nhịp và chuỗi.**
   - Bùng nổ đến sau trung vị 11 video. Với CityEons, bùng nổ đến ở video 3–4 của chuỗi cùng format, đăng cách nhau 1–8 ngày.
   - Kênh Shorts thắng đăng 0,5–1,4 Short/ngày.
   - Giả thuyết: một chuỗi nhiều thành phố hoặc nhiều Shorts cùng khung, đăng liên tục, có ích hơn việc dồn sức vào một video. Đánh đổi: nhịp này chạm nguyên tắc chất lượng tối cao của dự án, nên chỉ hợp lệ nếu chất lượng giữ nguyên.
5. **H5 · Ghi minh bạch “No AI imagery”.** Kênh 3D timelapse thắng duy nhất ghi điều này trong tiêu đề và mô tả. Không Shorts/video ngách tự khai AI nào đạt M2 (0/39). Bằng chứng yếu: Urbavision không ghi mà vẫn đạt 100–320 nghìn lượt.

## §5. Chỉ số trong ±5 % quanh ngưỡng
**Video ngách (gần/vừa):**
- M1:
  - Whyograph “India Controls Bangladesh's Biggest River”: 1 010 902 / 1 000 000 (+1,1 %, **đạt M1 sát ngưỡng**).
  - Sin Coordenadas “AUSTRALIA…”: 1 778 460 / 1 803 584 (−1,4 %, xếp M2).
  - The Why Side “A Fleck of Paint Blinded Hubble”: 1 802 479 / 1 866 317 (−3,4 %, xếp M2).
- M2: Ambrose Discovery “Marine Biologists Finally Solved the Mystery…”: 440 480 / 443 618 (−0,7 %, **không vào bảng**).
- Tuổi kênh 90 ngày:
  - Ambrose Discovery: video Titanic đăng khi kênh 86,8 ngày (M1 B). Nhiều video khác của kênh đăng ở 85,8–90,0 ngày nhưng không đạt.
  - Sin Coordenadas “RUSIA”: kênh 87,4 ngày (M2 B).
  - UncoveredHistoryLGC: 86,2 ngày, không đạt.
- Cửa sổ 30 ngày: The Why Side “How an Accident Made Boats Faster” 29,63 ngày tuổi; “How Did They Stop Champagne…” 28,63 ngày.
- Ngưỡng Shorts 180 s và tỷ lệ thích/xem 0,2 %: không video ngách nào nằm trong ±5 %.

**Video ngoài ngách:**
- Telugu Learning with Anika: −2,9 % so với M1.
- Twig by Twig: −1,3 % và +3,9 % so với M2.
- CineFlex: +0,9 % so với M2.
- SM Create: −2,1 % so với M2; kênh 87,8–89,7 ngày tuổi lúc đăng.
- Love Nostalgia: một video 173 s, sát ngưỡng Shorts; một video 28,68 ngày tuổi.

## §6. Giới hạn phương pháp
1. **Mẫu mỏng:** 9/84 truy vấn (11 %), vì hạn 100 `search.list`/ngày của dự án đã gần cạn (§2). Phiên không chạy được các truy vấn theo danh mục, vùng (GB, IN, ID, DE), ngôn ngữ (pt/hi/id) và Shorts riêng. Ngách tiếng Hindi/Indonesia gần như vắng mặt trong mẫu.
2. **Lệch do mở rộng uploads:** 33/46 video ngách đến từ uploads của các kênh đã lọt mẫu. Vì vậy The Why Side và Trial & Eureka chiếm 24/36 Shorts. Phép mở rộng đo đúng *trong kênh* nhưng làm phóng đại trọng số của vài kênh.
3. **Hạng B là ước:** 41/46 video ngách là hạng B. Công thức (tuổi/7)^0,5 kế thừa NC-VIRAL, chưa được kiểm định bằng chuỗi lượt xem thật.
4. `search.list` chỉ trả top 50 mỗi truy vấn và không lọc được theo tuổi kênh.
5. Phân loại ngách và cờ AI do phiên làm tay. Cờ AI chỉ dựa vào lời tự khai. Video không khai mà vẫn dùng AI thì không bị đánh dấu.
6. Không tải hay xem ảnh hoặc video, nên §4c chỉ dựa vào văn bản.
7. Số đăng ký của kênh bị API làm tròn 3 chữ số, nên cột Xem/ĐK và ĐK/ngày là xấp xỉ.
8. LAYERS là kênh tổng hợp nhiều chủ đề: 256 video trong 76 ngày, có cả clip WWE dẫn sang Rumble. Hai Shorts công trình của kênh đạt M2, nhưng tín hiệu ngách của kênh này yếu.

## §7. Chi phí

| Hạng mục | Dùng | Trần |
|---|---|---|
| YouTube Data API | **997 đơn vị** chắc chắn (9 297 nếu 83 lệnh 429 bị tính; xem §2) | 9 000 |
| Claude API (phân loại) | **$0**, không gọi (`so-ai.jsonl`) | mốc $1, chặn $3 |
| Gemini, OpenAI, ElevenLabs | 0 | 0 |
| Giờ máy | ≈ 0,3 h (quét + xử lý) | 3 h |

## §8. Tệp
`reports/nc-viral-2/`:
- `NV2-BAO-CAO.md`
- `dai-m1.csv`, `dai-m2.csv`, `shorts-m1.csv`, `shorts-m2.csv`
- `kenh-theo-doi.csv`
- `quet.json`: rút gọn, gồm id, số liệu, `hits`, ngày đăng uploads; không có mô tả, khoá hay ảnh.
- `so-quota.jsonl`, `so-ai.jsonl`
- `CHECKPOINT.md`

Không lưu thumbnail, khung hình hay video của kênh khác. Không có email hay khoá trong tệp.

## §9. Việc đang chờ chủ dự án
1. **Duyệt báo cáo NV-2.** Phiên DỪNG tại đây.
2. **Quyết định có chạy nốt 75 truy vấn còn lại hay không.** Hạn 100 search/ngày đặt lại lúc 14:00 Asia/Saigon (07:00Z) mỗi ngày. Có hai cách:
   - (i) Một phiên NV-2b chạy 75 lệnh, giữ `quet.py --tiep`, và không phiên nào khác dùng `search.list` trong ngày đó.
   - (ii) Xin Google tăng hạn `Search Queries per day` cho dự án.
3. Đối chiếu trên Google Cloud Console xem 83 lệnh 429 có bị tính đơn vị hay không (§2).
4. Chọn hoặc loại các giả thuyết H1–H5 cho T4 London (§4h). Phiên không chọn thay.
