# K2C-T2-01 · Đóng gói (Mốc A) — chọn đề tài

> Vai **Đóng gói**, chạy thật trong T2 (sổ vai `so-vai.jsonl`, `vai.py sum`). Kinh thánh kênh 2 §2: hồ sơ cầu (Data API) + neo thời sự + nghịch lý một câu + nhân vật người thật có hồ sơ + mức rủi ro (QUAN-TRI-RUI-RO). Mọi chỉ số thị trường là **tự tính, không phải chỉ số YouTube**. Số liệu thô (danh sách video, bình luận) để **ngoài git** (`/var/tmp/cine-out/t2-data/`), không đưa lời/hình/thumbnail của kênh khác vào repo.

## 1. Cách đo (YouTube Data API, trần 300 đơn vị)
| Bước | Lệnh | Đơn vị |
|---|---|---|
| Tìm kênh đối thủ trong Kinh thánh (Fortune of Nations Animated, GoDocs) bằng `channels.list forHandle` | 12 lượt (5 handle GoDocs sai trước khi tìm ra `@GoDocumentaries`) | 12 |
| Toàn bộ video của 2 đối thủ (13 + 42 video) | `playlistItems` + `videos` | 4 |
| **Quét kho 10 kênh giải thích không lộ mặt cùng dạng** (Economics Explained, Wendover, PolyMatter, RealLifeLore, Real Engineering, Business Casual, CaspianReport, Asianometry, Modern MBA, Half as Interesting; 3 788 video) — tìm ai đã làm đề tài, video đó được bao nhiêu lượt | `channels` 10 + `playlistItems` 80 + `videos` 1 | 91 |
| **Hồ sơ cầu đề tài khuyến nghị:** 1 câu hỏi khán giả "why can't america build ships", toàn thời gian, theo độ liên quan, `regionCode=US`; 5 video dài đầu; 150 bình luận (`collect.py demand`, Haiku gắn nhãn 150/150, Sonnet tổng hợp) | `search` 100 + `videos` 1 + `commentThreads` 5 | 106 |
| Lấy mã 2 video để xem thumbnail tham chiếu (ảnh chỉ để ngoài git) | `playlistItems` | 2 |
| **Tổng** | | **≈ 215 / 300** |
- **Vì sao chỉ 1 search.list:** mỗi lượt tốn 100 đơn vị; 3 lượt (một mỗi đề tài) cộng lệnh đọc sẽ vượt 300. Hai đề tài còn lại dùng bằng chứng từ phép quét kho 10 kênh + 2 đối thủ (rẻ, đo được) và ghi rõ là **chưa đo bằng câu hỏi tìm kiếm**.
- AI: Haiku + Sonnet trong `collect.py` **$0,14** (vai Đóng gói).

## 2. Loại trừ: đề tài đối thủ đã làm
- **Fortune of Nations Animated** (13 video, 01–13/10/2026): Mỹ vs Mỹ Latin, Ireland–Anh, Thuỵ Sĩ, Nga–châu Âu, Ai Cập, Alaska, Manhattan–nhục đậu khấu, đồng bạc Tây Ban Nha, cầu Âu–Phi, Oman.
- **GoDocs** (42 video): Palm Jumeirah, **Suez**, Burj Khalifa, Great Green Wall, Kola, **Panama Canal**, Hà Lan, Venice, Taipei 101, Constantinople, sân bay Kansai, Mexico City, Aral, kênh Corinth, Dubai World Islands, thủ đô Indonesia…
- **10 kênh cùng dạng:** Wendover vừa làm **Botswana** (30/09/2026, ≈ 1,02 triệu) → loại Botswana dù đã cân nhắc; Asianometry có "Rapid Rise of Korean Shipbuilding" (05/2023, ≈ 180 nghìn) và "Steel Colossus" (POSCO, 04/2026).
- Loại thêm: Panama (GoDocs), Ireland/Thuỵ Sĩ (FoN), đề tài thành phố (T1 vừa là trụ thành phố — `LUAT-CHON-DE-TAI.md`: không hai tập liền cùng trụ trong 6 tập đầu).

## 3. Ba đề tài ứng viên
| | **A. Đóng tàu: Mỹ ↔ Hàn Quốc ↔ Trung Quốc** (khuyến nghị) | B. Ca cao: vì sao nơi trồng sô-cô-la không giàu | C. Houston ↔ Galveston: cảng cách biển 80 km |
|---|---|---|---|
| Lăng kính / trụ | Ngành + quốc gia (trụ T2 ngành) | Quốc gia + ngành (T2) | Thành phố (T1 — **trùng trụ với tập trước**) |
| Nghịch lý một câu | *"In 1942 an American yard built a cargo ship in under five days. Today America builds almost none — and the company buying an American shipyard comes from a country that had never built a ship until the 1970s."* | *"Two West African countries grow most of the world's cocoa; when its price tripled, the farmers' price was set by the state."* | *"America's busiest port by tonnage sits 50 miles from the sea — because a hurricane killed the city that was supposed to win."* |
| Neo thời sự (đã tra, xác minh lại trước khi khoá lời — BAI-HOC-K2 K2) | Phí cảng Section 301 với tàu liên quan Trung Quốc **tạm hoãn đến 09/11/2026** — chưa có quyết định gia hạn (tin cuối 09/2026); Hanwha Philly: cam kết $5 tỷ (08/2025), hợp đồng tàu Missile Defense Agency (07/2026); trung tâm hợp tác đóng tàu Hàn–Mỹ ở Washington (07/2026, gói "MASGA" $150 tỷ) | EUDR áp dụng cho doanh nghiệp vừa/lớn từ **30/12/2026** (Quy định (EU) 2025/2650); giá ca cao biến động sau đỉnh 2024 | Port Houston xong phần mình của Project 11 (lễ 08/10/2026); toàn dự án dời tới 2029 |
| Nhân vật có hồ sơ | Henry J. Kaiser (xưởng Richmond; ảnh LoC/OWI tài sản công); Thượng nghị sĩ Wesley L. Jones (Jones Act 1920; ảnh LoC Harris & Ewing); Chung Ju-yung (Hyundai, Ulsan 1972 — không có chân dung tài sản công → nhân vật A-lite, đạo cụ bản vẽ + tờ tiền); thợ hàn nữ Richmond (ảnh OWI) | Houphouët-Boigny, Nkrumah (ảnh White House/JFK Library tài sản công — cần kiểm từng tệp) | Jesse H. Jones (LoC), Woodrow Wilson bấm nút mở kênh 1914; ảnh bão Galveston 1900 (LoC) |
| Cầu (Data API) | **Đo:** 1 câu hỏi, 5 video dài: **3,21 triệu** (09/2025, góc "chỉ ba nước"), **158 nghìn** (03/2026), 53 nghìn, 39, 7 → **Cầu-bền CÓ**; 2026 có cung mới nhưng video mới nhỏ không bật (39 và 7 lượt) → đúng mẫu "chất lượng thắng". Kho 10 kênh: 2 video Hàn Quốc đóng tàu/thép (180 nghìn, 105 nghìn), "tàu khổng lồ" 554 nghìn | **Gián tiếp:** 0/3 788 video của 10 kênh nói về ca cao → khoảng trống nhưng cầu chưa đo; FoN chứng minh dạng "vì sao nước X giàu/nghèo" (1,36 triệu/1 tuần) | **Gián tiếp:** 0/3 788 video về Houston/Galveston; GoDocs chứng minh cầu "công trình kênh/cảng" (Suez 2,24 triệu, Panama 379 nghìn) |
| Khoảng trống | Bình luận phản bác chiếm 68/90 bình luận có nội dung; ý nặng nhất (trọng số 17 301): "đổ cho lương rẻ là che chiến lược và quản trị yếu"; 2 717: "Hàn Quốc bắt đầu đóng tàu khi còn nghèo hơn nhiều nước châu Phi"; yêu cầu nặng nhất (277): tài chính, biên lợi nhuận, vốn cho chủ tàu; video Mỹ 2026 "như teaser". Không video nào nối **hạn 09/11/2026** + Jones Act + câu chuyện Ulsan | Video phổ thông thường đi theo lao động trẻ em; ít video giải thích cơ chế giá thu mua của nhà nước (CCC, COCOBOD) | Chưa ai trong mẫu |
| Số neo (loại nguồn công khai) | MARAD/NPS (Liberty ships), USTR Section 301 (01/2025), Federal Register (phí, tạm hoãn), CRS (Jones Act, chi phí), UNCTAD/OECD (thị phần), World Bank (GDP/người Hàn Quốc), KOSIS (Ulsan) | ICCO, Quy định EU 2025/2650, World Bank, FAO | USACE, Port Houston, NOAA (bão 1900), Census lịch sử |
| Dựng 3D / hình | Bản đồ nổi Vịnh San Francisco (USGS 3DEP sẵn), Đông Á (cần DEM ngoài Mỹ: SRTM tài sản công — mở rộng `relief_build.py`), hàng xu (thời gian đóng 1 tàu), sticker tàu/cẩu trong cảnh; footage Liberty ship của chính phủ Mỹ (NARA/Internet Archive) + DVIDS (xưởng hải quân, không huy hiệu) | Bản đồ nổi Tây Phi (cần DEM ngoài Mỹ), ít footage tài sản công | Bản đồ nổi bờ Texas (USGS 3DEP sẵn), footage USACE/DVIDS nạo vét (được dùng từ 15/10) |
| Mức rủi ro | **VÀNG** — địa chính trị gần đây (thuế/phí với Trung Quốc, chính sách Mỹ–Hàn). Giữ góc cơ chế; nêu "as of"; không quy động cơ; tên công ty chỉ là ví dụ có nguồn | **VÀNG** — lao động trẻ em, thuộc địa, giá thu mua do nhà nước định | **XANH** — nhưng chạm thảm hoạ có người chết (1900, lịch sử ~126 năm: không vùng phỉ báng) |
| Nhược | Phải mở rộng nền bản đồ ra ngoài Mỹ; hạn 09/11 có thể đổi trước khi thu giọng (rủi ro K2) | Cầu chưa đo; ảnh người thật hiếm | Trùng trụ thành phố với T1; cầu chưa đo |

## 4. Khuyến nghị: **A — đóng tàu**
- **Lý do:**
  1. Đề tài duy nhất có **cầu đo được** bằng câu hỏi tìm kiếm (Cầu-bền 3,21 triệu) và **khoảng trống đọc từ bình luận** (phản bác "lương rẻ", hỏi vai trò nhà nước, đòi bàn tài chính).
  2. **Neo thời sự có hạn chót** trong 4 tuần (09/11/2026) → lý do xem ngay; tập vẫn sống lâu nhờ phần lịch sử (Liberty ships, Ulsan).
  3. Đúng lời hứa kênh "How places get rich": Richmond (CA) và Ulsan là **nơi** giàu lên nhờ xưởng tàu; nước Mỹ "tụt lại" ở cùng ngành.
  4. Nhân vật có hồ sơ cho từng chương (Kaiser, Jones, Chung) và kho hình tài sản công lớn, độ phân giải cao (OWI, NARA, DVIDS).
  5. Không trùng 55 video của 2 đối thủ; khác góc với video 3,21 triệu ("chỉ ba nước"): tập này kể **vì sao một nước mất ngành và một nước nghèo có được nó**, bằng cơ chế (đơn hàng ổn định, vốn, bảo hộ không cạnh tranh).
- **Rủi ro chính và cách giảm:** VÀNG (6 điều kiện, REVIEWER Opus rà lời + tiêu đề/thumbnail); "as of" cho mọi trạng thái mở, tra lại trước khoá lời và trước thu giọng; tên Hanwha/HD Hyundai/CSSC chỉ là chủ thể của hành động có nguồn, không đánh giá công ty; không đi vào hải quân/quân sự quá mức cần.
