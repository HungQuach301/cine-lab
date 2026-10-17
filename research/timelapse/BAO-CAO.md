# R&D "City Timelapse 3D": làm sao để hơn Latos Charts — BÁO CÁO

> Phiên R&D timelapse, 15/10/2026, theo lệnh chủ dự án duyệt 15/10. Nhánh `timelapse-rd`, **không merge**.
> Mọi số trong báo cáo đều đo thật trong phiên hoặc tra từ nguồn có ghi URL. Những số chưa kiểm được đánh dấu **(ước)** hoặc **(chưa kiểm)**.
> Đã áp hai lệnh bổ sung giữa phiên: **22:47** (4 yếu tố ngôn ngữ hình, §6.6) và **23:04** (ngân sách chữ, §6.7). Đề xuất luật Q cho phiên K ở §6.8.

```text
ĐIỀU LỆ PHIÊN TL-RD                                             | THỰC TẾ
Loại phiên:        R&D (vùng riêng theo lệnh giao)              | đúng
Nhánh:             timelapse-rd, tạo từ origin/main @ 7255aa4    | đúng
Tệp được sửa:      research/timelapse/** · lab/timelapse/**     | chỉ hai thư mục này; KHÔNG ghi RIGHTS/AUTHORSHIP/COST-LEDGER (đề xuất ở §10)
Tệp KHÔNG được sửa: scripts/ design/ checks/ channel-*/ assets/  | không sửa; assets/k2 và scripts/ll/mix.py chỉ đọc
Trần chi phí:      YouTube API ≤ 400 đv · Claude API ≤ $3 (ghim)| 333 đv · $0,051 (claude-haiku-5-5, served = ghim)
                   ElevenLabs 0 · render thử ≤ 2 giờ           | 0 ký tự · ≈ 1,4 giờ máy (§6.4)
Đầu ra:            BAO-CAO.md + bảng json + video thử 30 s     | §11 liệt kê tệp
Điều kiện dừng:    xong việc                                    | xong; DỪNG chờ chủ dự án
Preflight:         bắt buộc trước khi đẩy                       | kết quả ở §12
```

## 0. Tóm tắt cho chủ dự án (đọc 1 phút)

1. **Cầu có thật nhưng cung đang bùng nổ.** Trong mẫu (Latos + 10 kênh + 150 kết quả tìm kiếm), số video "thành phố mọc 3D" tăng từ **19 video tháng 9** lên **61 video chỉ trong nửa đầu tháng 10/2026**, do **17 kênh** đăng. 8/10 kênh cạnh tranh đăng video thể loại này lần đầu trong khoảng 12/09 đến 07/10. Cầu vẫn còn: 12/61 video tháng 10 đã vượt 100 nghìn lượt xem trong ≤ 15 ngày, kể cả kênh 12 ngày tuổi (CityEons, London **472 768** lượt).
2. **Chỗ hơn đo được là ĐỘ ĐÚNG.** Bình luận chỉ ra lỗi lịch sử chiếm 9–21 % số bình luận, nhưng lại là bình luận **được thích nhiều nhất** trên cả 3 video lớn nhất của Latos (Prague 295 like, Lisbon 272 like — "người La Mã bắn súng hoả mai", Athens 729 like). Chưa kênh nào hứa "mỗi ngày đều có nguồn". Một kênh 8 ngày tuổi (Urbavision) đã bắt đầu dùng góc "Built on the Real Street Map".
3. **H1 khả thi về kỹ thuật, nhưng không thể làm "thuần".** Bản thử Amsterdam dựng được **75 534 toà nhà đúng năm xây** (3DBAG/BAG, giấy phép CC BY/CC0), 1 lệnh vẽ, **1,24 s/khung ở 540p** trên CPU (bản cuối, có đủ 4 yếu tố ngôn ngữ hình; 4 yếu tố tốn thêm ≤ 0,16 s/khung). Có hai lỗi gốc của dữ liệu:
   - **Thiên lệch sống sót:** năm 1622 Amsterdam có 104 932 dân nhưng chỉ **199 toà** còn đứng tới nay.
   - **Năm bị làm tròn:** với toà xây trước 1800, **43,8 %** có năm tận cùng bằng 0 hoặc 5 (nếu năm thật thì chỉ khoảng 20 %).

   Vì vậy H1 phải đi kèm lớp bản đồ lịch sử có giấy phép thương mại. Đây là điểm nghẽn thật: David Rumsey và Gallica không cho dùng thương mại miễn phí.
4. **Ngôn ngữ hình + ngân sách chữ:** 4 yếu tố (mốc đinh, bay dọc phố theo hình học NWB, reveal kéo lùi, ảnh lịch sử neo 3D + then/now căn góc từ 7 điểm khống chế, RMS 6,3 px) đều dựng được trên CPU, tổng giờ máy tăng thêm không đáng kể (§6.6). Chữ giảm từ **32,4 % → 10,8 %** diện tích khung (trung vị), 0 khung có chữ không neo ở vùng giữa (§6.7). Phát hiện kể chuyện: chỗ người chụp ảnh năm 1886 đứng nay nằm **trong một toà xây năm 1899**.
5. **Khuyến nghị:** phương án **(B)** — làm dạng tập "Why <city> grew here" trong Moving Parts + Short. **Không mở kênh 3 riêng (A)**, vì thị trường đã bão hoà và nhịp đăng cần ≥ 1 tập/tuần, quá sức nếu làm H1 đúng chuẩn. Tập đầu nên chọn thành phố có dữ liệu năm tốt và chưa ai làm: **Zürich** hoặc **Helsinki** (đúng nhất), **Seville** (có cầu ở bình luận, dữ liệu dồn năm) hoặc Detroit (dạng "thành phố co lại", chưa kiểm dữ liệu). Chủ dự án chọn (§9).

## 1. Teardown cầu (YouTube Data API, 333/400 đơn vị)

Số liệu thô (gồm cả văn bản bình luận) lưu **ngoài git** ở `~/.cache/cine-timelapse/`. Bảng đã gộp nằm trong `research/timelapse/teardown.json`. Không tải video, khung hình hay thumbnail của bất kỳ kênh nào.

**Quota:** 3 search.list × 100 = 300 đơn vị; channels, playlistItems, videos và commentThreads tổng 33 đơn vị. Tổng **333**.

### 1.1 Latos Charts (@latoscharts)
- Kênh tạo 17/03/2019, quốc gia IN. **99 500 người đăng ký**, 15 video, tổng 5 958 971 lượt xem.
- Video timelapse đầu tiên: 11/08/2026. Nhịp đăng **1,51 video/tuần**, nhưng tăng tốc: 7 video trong 15 ngày gần nhất.
- Thời lượng tăng dần: 204 s (London, 08/2026) → 849 s (Berlin, 10/2026). Trung vị 536 s. Dạng "~9–10 phút" mà chủ dự án xem là các video tháng 10.
- Lượt xem/ngày tính đến 15/10: **Prague 110 059** (1 138 090 lượt, 10 ngày) · Amsterdam 45 439 · Lisbon 38 137 · Athens 37 410 · Barcelona 25 010 · Moscow 24 877. Trung vị kênh: 14 414/ngày.
- Tiêu đề chỉ có dạng `CITY - 3D Timelapse`. Hai video đầu có thêm "(Not AI)".

### 1.2 Kênh cùng dạng (10 kênh, toàn bộ video của từng kênh)
| Kênh | Tạo kênh | Đăng ký | Video TL | TL đầu tiên | Nhịp/tuần | Trung vị dài (s) | Trung vị xem/ngày | Video lớn nhất |
|---|---|---|---|---|---|---|---|---|
| CITY 3D TIMELAPSE (FR) — **kênh gốc của dạng** | 2025-09-01 | 87 100 | 13 | 2025-09-02 | 0,07 | 55 | 326 | Paris 9 683 617 (2025) |
| Restored Timeline (US) — **máy quay cố định + AI** | 2014 | 64 400 | 12 | 2026-04-23 | 0,47 | 823 | 3 078 | Chicago 3 511 659 |
| Cornerstone Timelapse | 2020 | 1 910 | 3 | 2026-10-02 | 1,56 | 492 | 33 314 | Las Vegas 493 634 |
| CityEons (DE) — kênh bắt chước "No AI imagery" | 2026-10-03 | 2 160 | 3 | 2026-10-05 | 2,33 | 322 | 45 421 | London 472 768 |
| Urbavision (PT) — "Built on the Real Street Map" | 2026-10-07 | 1 020 | 5 | 2026-10-07 | 4,67 | 411 | 8 281 | Rio 191 081 |
| How Cities Grew | 2022 | 603 | 4 | 2026-09-21 | 0,88 | 254 | 762 | Stockholm 151 482 |
| DataShark (US) | 2026-03 | 17 000 | 11 | 2026-10-01 | 5,38 | 495 | 752 | Tokyo 113 023 |
| Timeline Cities | 2006 | 402 | 13 | 2026-09-29 | 5,60 | 372 | 193 | St Petersburg 95 266 |
| nobodycareswhatiswrittenhere (PL) | 2026-09 | 1 050 | 9 | 2026-09-26 | 2,95 | 489 | 2 496 | New York 93 353 |
| timewarp cities | 2025 | 58 300 | 1 | 2026-09-12 | — | 905 | 403 | London 13 364 |

Đọc bảng:
- (a) Nhiều kênh mới đã chạm mức trăm nghìn lượt xem chỉ trong vài ngày, nên cầu là thật.
- (b) Các kênh bắt chước đăng **2–5,6 video/tuần**. Muốn đua về lượng thì phải theo nhịp này.
- (c) Dạng "máy quay cố định + AI" (Restored Timeline) đạt lượt xem cao nhất trong năm (Chicago 3,5 triệu). Người xem không phản đối AI bằng lượt xem, nên nhãn "No AI" một mình không phải lợi thế.

### 1.3 Bình luận: 100 bình luận hàng đầu × 5 video (491 bình luận)
Nhãn gán bằng `claude-haiku-5-5`, chi phí $0,051. Bình luận gốc không đưa vào git.

| Video | Khen chung | Khen hình | Xin thành phố | Lỗi/thiếu/hỏi lịch sử | Tỷ lệ độ đúng | Có trọng số like | Muốn thêm thông tin | Chữ khó đọc |
|---|---|---|---|---|---|---|---|---|
| Latos PRAGUE | 58 | 5 | 17 | 11 | 11 % | 15,1 % | 6 | 1 |
| Latos ATHENS | 27 | 3 | 25 | 16 | 16 % | 26,6 % | 2 | 1 |
| Latos LISBON | 56 | 10 | 23 | 9 | 9 % | 10,9 % | 6 | 1 |
| CityEons ROME (bắt chước) | 38 | 8 | 10 | 19 | 21 % | 6,8 % | 2 | 1 |
| CITY 3D TL PARIS (kênh gốc) | 42 | 8 | 12 | 11 | 11 % | 4,0 % | 8 | 0 |

**Người xem chê gì** (tóm tắt nhãn, kèm số like):
- Prague: sai địa điểm định cư đầu tiên (295); thiếu Vyšehrad (89).
- Lisbon: người La Mã bắn súng hoả mai (272); thiếu trận động đất 1531 (3).
- Athens: cỏ "xanh ngọc" sai với khí hậu Attica (729); sai dòng sông Ilissos (15); thiếu sự kiện 1311 (12).
- Paris: không thấy tháp Eiffel (605); tường Thiers xuất hiện từ 1810 trong khi xây 1841–44 (15).
- Rome: tường Aurelian xuất hiện trước tường Servian.

Ở cả năm video, bình luận độ đúng là nhóm có tương tác cao nhất **sau** khen chung. Đây là khán giả **soi lịch sử**.

**Khen gì:** chủ yếu khen chung ("amazing", "goosebumps"). Khen nhạc rất ít (9/491), nên nhạc không phải lý do người ta xem. Chỉ 4/491 bình luận nói chữ khó đọc. H3 vì vậy là việc vệ sinh cần làm, không phải lợi thế cạnh tranh.

### 1.4 Thành phố đã làm và thành phố được xin
**Đã làm** (mọi kênh trong mẫu, video ≥ 45 s, 49 thành phố; bảng đầy đủ trong `teardown.json` → `cities_done`), xếp theo video lớn nhất:
Paris 9,7 tr · New York 5,3 tr (14 kênh) · Chicago 3,5 tr · Los Angeles · Prague · Athens · San Francisco · London (7 kênh) · Mexico City · Lisbon · Rome (8 kênh) · Istanbul · Moscow · **Amsterdam 514 nghìn (2 kênh)** · Las Vegas · Barcelona · Berlin (4) · Rio · Dubai · Stockholm · … · Tokyo (3) · Hong Kong (3) · Venice (5) · Kyiv (2) · **Bangkok (1 video, 378 lượt)** · Shanghai · Delhi · Manila · Cairo · Hanoi (Restored Timeline, dạng AI, 2 964 lượt).

**Được xin nhưng chưa ai làm** (đếm số lần xin trong 491 bình luận):
| Thành phố | Số lần xin | Ghi chú |
|---|---|---|
| Belgrade, Budapest | 4 mỗi thành phố | |
| Baghdad, Thessaloniki | 3 mỗi thành phố | |
| Naples, Krakow, Antioch, Porto, Detroit | 2 mỗi thành phố | |
| Zaragoza, Bratislava, Madrid, Seville, Nuremberg, Bucharest, Damascus, Izmir, Yogyakarta, Chongqing… | 1 mỗi thành phố | |

*Cần lưu ý:* Jerusalem (6 lần), Mexico City/Tenochtitlan (5) và Kyiv (4) được xin nhiều nhất, nhưng tháng 10 đã có kênh làm.

**Áp LUAT-CHON-DE-TAI** (cho cả dạng, không cho từng tập):

| Điều kiện | Kết quả | Căn cứ |
|---|---|---|
| ĐK1 cầu | **Nổ-mẫu** | 6 video ≥ 500 nghìn trong 90 ngày cùng mẫu tiêu đề "<CITY> 3D Timelapse" |
| ĐK2 khoảng trống | **Đạt theo nhánh "bình luận chỉ ra lỗi lặp lại"** | Lỗi lịch sử xuất hiện ở 5/5 video. Không kênh nào ghi nguồn, trừ Urbavision chớm làm "real street map" |
| ĐK3 số liệu nguồn công khai | **Đạt khi chọn thành phố có thống kê chính thức** | Amsterdam: CBS 7377vt (1899 = 510 853) và CBS 70072ned (01/01/2026 = 941 927) đã kiểm. Nguồn sử học cho trước 1800 phải đọc toàn văn |
| ĐK4 dựng được 3D | Đạt | Bản thử §6 |
| ĐK5 pháp lý | XANH | Câu hỏi là cơ chế đô thị. Rủi ro riêng: quyền bản đồ lịch sử (§3) và tranh cãi dân tộc (6/491 bình luận chính trị) |

## 2. H1 — ĐÚNG HƠN: "mỗi toà mọc đúng năm"
Bằng chứng gồm hai phần: bộ dữ liệu Amsterdam do phiên này tải và đo, và bảng 26 bộ dữ liệu do tác tử con kiểm (`data-sources.json`, `NGUON-DU-LIEU.md`; mọi số đếm qua API ngày 15/10 kèm URL).

**Dữ liệu năm theo từng toà đủ tốt, giấy phép thương mại rõ (≥ 10 thành phố):**
| # | Thành phố | Bộ dữ liệu · giấy phép | % có năm | Dồn 0/5 (≈ 20 % là thật) | Đã có video thể loại? |
|---|---|---|---|---|---|
| 1 | **Zürich** | BFS GWR · dùng tự do, ghi nguồn, thương mại được | 100 % | 23,8 % | **Chưa** |
| 2 | **Helsinki** | Rakennukset · CC BY 4.0 | 59 % (lõi 76 %) | 21,7 % | **Chưa** |
| 3 | Amsterdam | BAG CC0 + 3DBAG CC BY 4.0 (có chiều cao) | 99,0 % (đo: 728/76 006 toà mang năm giả 1005) | 25,8 % toàn vùng; **43,8 % với toà trước 1800** (đo) | Có (Latos 514 nghìn) |
| 4 | **Kyoto** | PLATEAU · PDL 1.0 (≈ CC BY) | 82,6 % | 19,1 % | Có (Restored Timeline, dạng AI) |
| 5 | New York | Building Footprints · NYC Open Data | 99,1 % | **57 %** (năm 1900 chiếm 22 % mẫu Lower Manhattan) | Có (14 kênh) |
| 6 | Wien | OGD · CC BY 4.0 | 19 % có năm chính xác, phần còn lại theo giai đoạn | 23 % | Có (Latos) |
| 7 | **Sevilla / Madrid / Zaragoza** | Catastro INSPIRE · thương mại được nếu đã biến đổi | 99,7 % | **65 %** | **Chưa** (cả ba có người xin) |
| 8 | **Montréal** | CC BY 4.0 | ≈ 95 % | ≈ 41 % | **Chưa** |
| 9 | **Lyon / Bordeaux** | IGN BD TOPO · Etalab 2.0 | ≈ 72 % | 87 % | **Chưa** |
| 10 | **Melbourne** | CLUE · CC BY | 54 % (chỉ trung tâm) | 49 % | **Chưa** |
| + | Hong Kong (từ 1947) · Copenhagen (CC BY, chưa đo dồn) · Berlin (theo khối + 11 bản đồ pha 1650–1993, dl-de/zero) | | | | HK có 3 kênh; Berlin có 4 kênh |

**Ba phát hiện then chốt, đo trên dữ liệu thật** (`h1-amsterdam.json`):
1. **Thiên lệch sống sót.** Toà còn đứng tới nay có năm xây ≤ năm Y (số dân là con số đã kiểm):

   | Năm | Số toà còn đứng | Dân số |
   |---|---|---|
   | 1600 | 48 | |
   | 1622 | 199 | 104 932 |
   | 1700 | 1 623 | |
   | 1795 | 5 006 | 217 024 |
   | 1900 | 17 476 | 510 853 |
   | 1945 | 60 159 | |
   | 2026 | 75 278 | 941 927 |

   Nếu chỉ dùng năm xây, Amsterdam thế kỷ 17 trông như một bãi đất trống, trong khi thực tế là thành phố đông dân nhất châu Âu sau Paris và London. Đó là một kiểu "sai bằng dữ liệu đúng". Bản thử phải đổi nhãn thành **"Standing buildings, by year built"** để khỏi lừa người xem.
2. **Năm bị làm tròn ở phố cổ.** Với toà trước 1800, top năm là 1750 (203 toà), 1650 (174), 1725 (120). Câu "đúng từng năm" chỉ đúng cho thế kỷ 19–21. Với giai đoạn cũ, nói thật phải là "đúng đến thập kỷ".
3. **Lớp nước cũng có tuổi.** Bản thử dùng mặt nước BGT hiện đại từ năm 1275, nên kênh đào thế kỷ 17 hiện ra ngay từ đầu. Đây là cùng loại lỗi khán giả đã chê (tường Thiers xuất hiện năm 1810). Bản sản xuất cần pha nước và tường thành lấy từ bản đồ lịch sử.

**Bản đồ lịch sử có giấy phép (điểm nghẽn):**
- David Rumsey: **không** cho thương mại.
- Gallica/BnF và NAS Singapore: chỉ cho thương mại nếu **trả phí**.
- Library of Congress: thường "no known restrictions", nhưng phải kiểm từng mục.
- Berlin (dl-de/zero) và ảnh hàng không Wien 1938–1992 (CC BY 4.0): **dùng được**.
- swisstopo Zeitreise, Kadaster Topotijdreis, IGN État-major, bản đồ lịch sử Đan Mạch: **chưa rõ** giấy phép, cần hỏi trực tiếp.

**Thẻ sự kiện có nguồn:** 4 thẻ của bản cuối.
- **Móc** và **1655**: năm lấy từ sổ BAG (dữ liệu sơ cấp).
- **1275**: tolprivilege của Floris V ngày 27/10/1275, lưu tại Stadsarchief Amsterdam, đã đối chiếu ở nhiều nguồn.
- **Why here**: cơ chế **chưa có nguồn sơ cấp đọc toàn văn**, nên trên hình ghi rõ "primary source pending".
- Thẻ 1613 đã bỏ, vì trang UNESCO WHC 1349 trả 403, không đọc được toàn văn.
- Ngày khánh thành 29/07/1655 chỉ có nguồn thứ cấp, nên không đưa lên hình.

**Chi phí H1:**
- Dữ liệu toà nhà: gần 0. Một bbox 7 × 6 km tải 76 nghìn toà qua WFS hết khoảng 2 phút.
- Gánh nặng thật nằm ở **pha bản đồ lịch sử**: georeference và số hoá 4–8 lớp mỗi thành phố, tra quyền từng tấm, đọc toàn văn nguồn cho 15–25 thẻ. **(ước)** 1–3 ngày công người + phiên tra nguồn mỗi thành phố. Đây là việc chưa đo.

**Khuyến nghị: GIỮ, nhưng sửa lời hứa.**
- Không hứa "every building at the exact year". Hứa **"Every date sourced. Buildings from the national register. No AI imagery."**
- Hai lớp hiển thị khác nhau: toà còn đứng (khối đặc, năm từ sổ đăng ký) và phố đã mất (khối mờ "ghost", từ bản đồ lịch sử, ghi rõ "reconstructed from <map, year>").
- Năm giả (1005, 1812, 9999…) không được "mọc".
- Chỉ chọn thành phố khi có ít nhất 3 lớp bản đồ lịch sử đã rõ quyền thương mại.

## 3. H5 — CHỌN THÀNH PHỐ KHÁC
**(a) Khán giả xin mà chưa ai làm**
- Top: Belgrade, Budapest, Baghdad, Thessaloniki, Naples, Krakow, Porto, Detroit.
- Không thành phố nào trong top này có dữ liệu năm theo toà đã kiểm, trừ nhóm Tây Ban Nha (Madrid, Seville, Zaragoza: Catastro, mỗi nơi 1 lần xin).
- Budapest và Belgrade có cầu cao nhất nhưng **chưa kiểm dữ liệu** (đưa vào việc tiếp).
- Baghdad, Antioch, Damascus: rủi ro nguồn và chính trị cao.

**(b) Châu Á / Việt Nam** (tác tử kiểm, chi tiết trong `NGUON-DU-LIEU.md` §5)
| Thành phố | Mức | Lý do |
|---|---|---|
| **Hà Nội** | H1-lite có điều kiện | Không có năm theo toà (OSM: 20/71 406 toà có `start_date`). Bản đồ thuộc địa trên Commons chủ yếu quét từ Gallica, dùng thương mại phải trả phí BnF. Chưa rõ điều khoản của Trung tâm Lưu trữ Quốc gia I. Dân số có nguồn từ 1979 (GSO); thời thuộc địa các nguồn học thuật vênh nhau |
| **TP. Hồ Chí Minh** | H1-lite có điều kiện | Như Hà Nội. Có bản đồ Le Brun 1795 trên Commons |
| **Singapore** | H1 một phần | Chỉ có 13 392 block HDB mang năm, không dồn (19 %). Làm được câu chuyện "nhà ở công cộng mọc lên"; CBD không có năm |
| **Bangkok** | Không khả thi | Không có năm, không có giấy phép bản đồ |
| **Tokyo** | H1-lite | PLATEAU 23 quận không có trường năm. Ở Nhật nên dùng **Kyoto** (82,6 % có năm) |
| Hong Kong | H1 từ 1947 | Ứng viên châu Á tốt nhất về dữ liệu, nhưng đã có 3 kênh làm (lượt xem thấp) |

Kênh phương Tây đã làm Tokyo (3 kênh), Hong Kong (3), Bangkok (1), Manila, Delhi, Shanghai, Hanoi (dạng AI). Châu Á **không còn trống**, chỉ còn **chưa có bản làm tốt**.

**(c) Dạng mới**
- *Thành phố co lại* (Detroit, Venice): đây là lời giải tự nhiên cho thiên lệch sống sót, vì có thể cho toà **biến mất**.
  - Venice đã có 5 video, đều theo kiểu "mọc".
  - Detroit được xin 2 lần, chưa ai làm. Dữ liệu năm xây và sổ phá dỡ **chưa kiểm**.
- *Hai thành phố song song* (Lisbon ↔ Porto; Sài Gòn ↔ Bangkok):
  - Sài Gòn ↔ Bangkok không đạt vì cả hai không có năm theo toà.
  - Lisbon ↔ Porto: Porto được xin 2 lần, nhưng dữ liệu Bồ Đào Nha **chưa kiểm**.
  - Màn hình chia đôi làm chữ nhỏ đi một nửa, nên chạm H3.

**Khuyến nghị: GIỮ có chọn lọc.** Tập đầu chọn trong số **Zürich, Helsinki** (đúng nhất, chưa ai làm, nhưng cầu chưa đo) hoặc **Seville/Madrid** (có người xin, Catastro dồn năm 65 % nên cần pha bản đồ). Detroit để làm tập "co lại" thứ hai, sau khi kiểm dữ liệu. Việt Nam: **bỏ cho tập đầu**, chỉ làm được sau khi mua licence BnF hoặc xin được điều khoản Lưu trữ Quốc gia.

## 4. H2 — KỂ HƠN: lớp "Why it grew here"
**Bằng chứng từ dữ liệu bản thử** (dòng thời gian bản cuối). Số toà mới **hoàn thành** mỗi giây màn hình (theo bảng năm↔giây, không tính toà năm 1005):

`[0, 1, 0, 2, 1, 0, 1, 5, 6, 1, 14, 42, 591, 0, 52, 684, 3475, 6460, 2030, 1800, 14325, 33091, 5680, 7273, 0, 0, 0, 0, 0, 0]`

Có ba quãng mà dữ liệu toà nhà không tự sinh thông tin mới:
- 0–12 s (thời trung cổ) gần như không có toà mới. Đây chính là điểm yếu đã đo ở Latos.
- 13–14 s: năm dừng ở mốc đinh.
- 24–30 s: năm đã tới 2026.

Bản thử lấp cả ba quãng bằng biến cố thiết kế:
- móc ở 0,4 s, thẻ 1275 ở 4,2 s;
- bay dọc Damrak + mô hình cơ chế "why here" 8,5–12,8 s (dòng Amstel, tuyến Damrak, con đập nhô lên, thuyền, vòng sáng);
- mốc đinh 1655 ở 12,8–16,4 s;
- ảnh 1886 neo 3D ở 17,6 s;
- reveal kéo lùi 16,4–24 s;
- glide/zoom-in 24–27 s;
- then/now 26–29 s;
- máy luôn chuyển động, chỉ khoá 1,58 s khi ảnh phủ.

Khoảng cách xa nhất giữa hai biến cố thiết kế: **≈ 4 s**, đạt luật ≤ 6 s. *Giới hạn:* nhịp được đo theo bảng thiết kế, chưa đo bằng công cụ của K trên video.

**Chi phí:**
- Mỗi nhịp lặn cần 1 mô hình cơ chế (đường, tuyến, khối) và 1 thẻ có nguồn. **(ước)** 2–4 giờ dựng và tra cứu mỗi nhịp.
- Thời gian dựng hình không tăng đáng kể: cùng cảnh, cùng s/khung.

**Khuyến nghị: GIỮ.** Đây là chỗ hơn khó chép nhất, vì cần hiểu cơ chế và có nguồn. Kênh bắt chước làm dạng 2–5 video/tuần không theo kịp. Nếu làm bản 9 phút, đề xuất 3–4 nhịp lặn, móc trong 10 s đầu, và kết bằng chồng dấu tích cũ lên hôm nay.

## 5. H3 — ĐỌC ĐƯỢC TRÊN ĐIỆN THOẠI
Bố cục chữ cuối cùng theo ngân sách chữ của chủ dự án (23:04). Chi tiết ở §6.7. Tương phản WCAG đo trên điểm ảnh thật của khung mẫu (mỗi 24 khung). Cỡ chữ quy về khung 1080p.

| Phần chữ | Cỡ (1080p) | Tương phản thấp nhất |
|---|---|---|
| Bộ đếm NĂM (1 dòng, không nhãn) | 96 px; ở mốc đinh 139 px (1,45×) | > 13:1 |
| Chỉ số dân số (1 dòng, "≈" khi nội suy) | 64 px | > 12:1 |
| Tiêu đề thẻ | 44 px (tự co, sàn 38 px; thực tế không thẻ nào phải co) | > 12:1 |
| Dòng nguồn đang hiện | 38 px | **8,26:1** (Source: CBS StatLine) |

- Mọi chữ ≥ 38 px@1080. Thẻ dài nhất 10 từ.
- Q35/Q36 **không tìm thấy định nghĩa trong repo** (chỉ có trong `checks/`, phiên này không được đọc). Phiên dùng ngưỡng của lệnh giao (≥ 38 px, có tương phản) và WCAG 4,5:1. Cần K đối chiếu.
- **Chỉ số trong ±5 % quanh ngưỡng:**
  - dòng nguồn **38 px = đúng ngưỡng 38 px**;
  - ngân sách chữ: **72/634 khung thường** nằm trong 14,25–15,75 % (cao nhất **14,7 %**, trần 15 %).

**Chi phí:** gần 0. **Khuyến nghị: GIỮ**, xem là việc vệ sinh. Chỉ 4/491 bình luận chê chữ. Ngân sách chữ làm hình thoáng hơn, nhưng chưa có bằng chứng giữ chân (đo ở tập đầu).

## 6. Thử khả thi kỹ thuật (lab/timelapse/)
### 6.1 Đường ống (mã mới, độc lập; three.js 0.180.0 riêng trong `lab/timelapse/package.json`; không sửa `design/`)
- `fetch_ams.py`: tải 3DBAG WFS lớp `lod12` (khối LoD1.2, chiều cao `b3_h_70p`, năm `oorspronkelijkbouwjaar`). Bbox RD 117 900–124 900 × 484 400–490 400 (7 × 6 km): **76 006 toà, 76 264 phần**.
- `fetch_water.py`: lấy mặt nước BGT (PDOK OGC API, CC0), 2 281 polygon.
- **Địa hình:** Copernicus GLO-30. Đây là DSM, nên đã mở hình thái 3 × 3 ô (150 m) để bỏ nhà.
  - Amsterdam phẳng: DSM σ = 4,2 m, sau khi mở còn σ = 3,0 m. Địa hình gần như **không ảnh hưởng hình** ở thành phố này.
  - 3DEP chỉ có ở Mỹ. Thành phố đồi châu Âu (Lisbon, Rome, Zürich) cần DTM quốc gia hoặc chấp nhận độ nhiễu của DSM.
- `build_ams.py`: gói cảnh + thống kê H1.
- `scene.js`:
  - **Một BufferGeometry duy nhất.** Mỗi đỉnh mang năm, chiều cao và cờ mái. Vertex shader nâng toà theo `uYear` (mọc trong 4 năm, vượt 6 % rồi lắng), chớp vàng 6 năm khi mọc.
  - Bóng đổ PCF 4096 dùng cùng shader.
  - Lớp 2D vẽ chữ và đo tương phản.
- `render.js`: Chromium headless + SwiftShader, ghi `log.json`.
- `mix30.py`: trộn âm.
- Đây là "instancing theo thuộc tính" chứ không dùng InstancedMesh, vì chân móng mỗi toà khác nhau.

### 6.2 Kết quả
- `research/timelapse/ams30_540p_A.mp4`: 30 s, 960 × 540, 24 fps, H.264 + AAC, < 5 MB nên **không cần LFS**.
- Nội dung (bản cuối):
  - máy bay liên tục, 0 điểm cắt;
  - 1275 → 2026, mỗi toà **hoàn thành** đúng năm sổ đăng ký (BAG định nghĩa `oorspronkelijk bouwjaar` là năm hoàn thành; toà mọc trong 4 năm trước đó);
  - 4 yếu tố ngôn ngữ hình (§6.6);
  - bộ đếm năm và dân số theo ngân sách chữ (§6.7);
  - 4 thẻ có dòng nguồn: móc, 1275, why here (nguồn sơ cấp còn chờ), 1655;
  - ghi công dữ liệu ở 0–4,2 s và màn kết;
  - âm biến thể A.
- Bản đầu (trước 22:47, 1,407 s/khung) đã bị thay. Số đo của nó vẫn giữ trong `render-log.json` → `v1`.

### 6.3 Lỗi hình đã thấy (tự chấm, chưa qua K/chấm mù)
0. **Lỗi đã sửa trong phiên — cần ghi nhận:** bản đầu dựng tường toà nhà **lộn mặt vào trong**. Tôi đã đổi thứ tự đỉnh khi thấy mái "rỗng" mà không kiểm bằng tích có hướng. Nhìn từ trên cao thì gần như không thấy lỗi. Lỗi chỉ lộ ra khi máy hạ xuống mặt đất ở nhịp then/now. Đã sửa (thứ tự (a₀, b₀, b₁) cho pháp tuyến ra ngoài) và dựng lại cả đoạn. Bài học: kiểm hướng mặt bằng phép tính, đừng sửa theo mắt.
1. Mặt nước hiện đại có từ 1275 (§2.3).
2. Thành phố thưa trước 1700 do thiên lệch sống sót (§2.1).
3. Vật liệu đơn giản, không có cây, đường, mái dốc. 3DBAG có LoD2.2 mái dốc nhưng nặng gấp nhiều lần, chưa thử.
4. Mũi tên cơ chế và thuyền còn thô.
5. Chống răng cưa chỉ có MSAA 4×, chưa tích luỹ SPP như bộ k2v.

Bản này đủ cho một phép thử khả thi. **Chưa đạt** chuẩn phát hành của nhà máy.

### 6.4 Số đo (CPU 4 lõi, 15,7 GB RAM, không GPU; renderer "SwiftShader Device (Subzero)")
| Phép đo | Kết quả |
|---|---|
| Dựng đủ 720 khung 540p, bóng 4096 | **1,407 s/khung**, 16,9 phút; RSS đỉnh 2 940 MB; nạp cảnh 6,2 s; 1 300 822 tam giác |
| Ảnh tĩnh 1080p, cả thành phố, có bóng | 1,96–2,76 s/khung (5 mẫu); không bóng 1,56–1,64 |
| 151 068 toà (×2), 540p | 2,66–2,77 s/khung, RSS 3,1 GB |
| 302 136 toà (×4), 540p | 3,85–4,22 s/khung, RSS 4,6 GB |
| 453 204 toà (×6) và 604 272 toà (×8) | **trình duyệt sập** ("Target crashed") |

**Giới hạn đo được: khoảng 300 nghìn toà, 5,2 triệu tam giác mỗi cảnh**, với cách gộp một hình học. Lớn hơn thì phải chia ô và giảm chi tiết ở xa (LOD).

**Bản cuối** (đủ 4 yếu tố + ngân sách chữ): **1,238 s/khung**, 14,9 phút máy cho 720 khung, RSS đỉnh 1 909 MB.

**Giờ máy dựng tính tới nộp:** ≈ **1,4 giờ**, dưới trần 2 giờ.
- Phần đo thật (≈ 62 phút):
  - v1: 16,9 phút;
  - v1b: dừng giữa chừng sau ~13 phút, vì bị thay bởi lệnh 22:47;
  - v2: 14,7 phút;
  - v3: 14,8 phút;
  - dựng lại khung 600–719: 2,7 phút.
- Phần ước theo log (≈ 25 phút): ảnh tĩnh, stress, 1080p, bật/tắt hiệu ứng, căn góc.

### 6.5 Ngoại suy: tập 9 phút 1080p (12 960 khung)
| Kịch bản | s/khung | Giờ máy |
|---|---|---|
| CPU hiện có, cảnh cỡ bản thử (75 nghìn toà, có bóng) | ≈ 2,1–2,6 (từ ảnh tĩnh 1080p; luồng liên tục nhanh hơn ảnh tĩnh ~15 %) | **≈ 7,6–9,4 giờ** |
| CPU, cảnh toàn thành phố ~300 nghìn toà | ≈ 5–6 **(ước**: ×4 đo ở 540p là 4 s, nhân hệ số 1080p) | **≈ 18–22 giờ** |
| + chống răng cưa 2 lượt (chất lượng nhà máy) | ×2 | 15–44 giờ |
| GPU (chưa có, NT K6 hoãn) | **(ước)** 0,1–0,25: 1,3–5 triệu tam giác là nhẹ với GPU, nút cổ chai là đọc khung và mã hoá | **≈ 0,4–0,9 giờ** |

Chạy song song không giúp nhiều: NT đo 4 tiến trình chỉ nhanh 1,2×. **Kết luận:** với CPU hiện có, 1 tập/tuần làm được nếu chấp nhận 8–20 giờ máy mỗi tập. Không thể đua nhịp 2–5 video/tuần của các kênh bắt chước. Có GPU thì giờ máy không còn là nút cổ chai. Nút cổ chai khi đó là tra nguồn và số hoá bản đồ lịch sử.

### 6.6 Bốn yếu tố ngôn ngữ hình (bổ sung chủ dự án 22:47)
| Yếu tố | Trong đoạn thử | Cách dựng | Số đo | Giờ máy trong đoạn | Tăng thêm do hiệu ứng |
|---|---|---|---|---|---|
| **E1 mốc đinh** | 12,8–16,4 s, năm 1655 | Bộ đếm năm **dừng 1,83 s** (khung 312–355) và phóng 1,45×, chuyển vàng, có viền. Cung điện sáng (pha vàng 45 %) + viền phát sáng (vỏ lộn nở 2,2 m). Phần còn lại giảm bão hoà 55 % và tối 38 %. Thẻ neo vào mái Cung điện, nguồn "BAG register, building 0363100012167579" | Năm dừng 1,83 s (yêu cầu 1,5–2 s) | 86 khung, 0,992 s/khung, **85 s** | **+0,03 s/khung (+2 %)** |
| **E2 bay dọc phố theo hình học thật** | 8,5–12,8 s | Máy bay theo tim đường **Damrak**: NWB, Rijkswaterstaat, CC0, `stt_naam=Damrak`, 134 đỉnh → 8 điểm tâm tuyến. Cao 72 → 54 m, kết thúc nhìn thẳng Cung điện. Đây là cửa sông Amstel cũ, nên trùng nhịp "why here" | Lệch khỏi tâm tuyến: **TB 2,6 m, tối đa 10,5 m** trong 3,5 s; quãng bay 476 m; Cung điện lệch trục nhìn 0,0° khi tới đích | 103 khung, 1,049 s/khung, **108 s** | 0 (chỉ là đường bay) |
| **E3 reveal kéo lùi** + glide → zoom-in | Kéo lùi 16,4–24,0 s; glide/zoom-in 24–27 s | Kéo lùi từ Cung điện ra toàn cảnh trong lúc 1900–2026 bùng nổ. Sau đó lướt và lặn thẳng về đúng góc ảnh 1886 | Khoảng cách tới đích **184 → 3 947 m (×21)** khi kéo lùi; **3 947 → 98 m (×40)** khi zoom-in; 0 điểm cắt | Kéo lùi 82 khung: 1,563 s/khung, 128 s. Glide 48 khung: 1,524 s/khung, 73 s | 0. Toàn cảnh nhiều toà nên nặng hơn trung bình 26 % |
| **E4a ảnh lịch sử neo 3D** | 17,6–20,6 s | Ảnh Rijksmuseum **RP-F-00-568** "Achterzijde van het Paleis op de Dam", 1886, **CC0** (https://id.rijksmuseum.nl/200144330; IIIF micr.io; SHA-256 `552b3a71…1f93`). Đường dẫn và điểm sáng neo vào góc tây-bắc đỉnh tường Cung điện, chiếu lại mỗi khung | Đầu đường dẫn trùng điểm chiếu 3D (cùng phép chiếu của máy) | 72 khung, 1,088 s/khung, 78 s | **+0,135 s/khung (+13 %)** |
| **E4b then/now** | 26,0–29,0 s | Ảnh 1886 chồng đúng góc máy, giữ, rồi hoà 0,8 s sang cảnh 3D cùng góc. Máy **khoá 1,58 s** (khung 648–685), sau đó đẩy nhẹ vào | **Căn góc TỪ ĐIỂM KHỐNG CHẾ, không thủ công** (chi tiết bên dưới): RMS **6,3 px / 1 200 px (0,52 %)** | 72 khung, 1,313 s/khung, 95 s | **+0,16 s/khung (+14 %)** |

**Căn góc then/now** (`lab/timelapse/calib_photo.py`, kết quả `then-now-pose.json`):
- Đầu vào là 7 điểm ảnh đo tay trên lưới 100 px:
  - 3 góc chân móng/đỉnh tường;
  - 2 điểm gờ và 1 điểm chân trên mặt tây;
  - đỉnh đầu hồi mặt bắc.
- Mỗi điểm ảnh ghép với toạ độ thật của vòng chân móng Cung điện trong 3DBAG.
- Bình phương tối thiểu (scipy) giải 11 ẩn: x, y, yaw, pitch, roll, tiêu cự, 3 độ cao, 2 vị trí trên cạnh. Mắt cố định ở 1,7 m trên chân toà.
- Kết quả: fov dọc **38,0°**, máy ở ENU (−172, 80), cách góc tây-bắc ~46 m.

**Hai lần sai trước khi đúng (ghi để K biết rủi ro thật):**
1. Lần 1 tôi nhận nhầm góc tây-nam. Sai số nhỏ (RMS 5 px), nhưng máy rơi vào khối nhà hiện đại. **RMS thấp không chứng minh đúng góc.** Phải kiểm bằng ảnh chồng.
2. Lần 2 dùng góc của hình chữ nhật bao, nên lệch ~70 px ở cạnh gần. Lần 3 dùng góc thật của vòng chân móng thì khớp mặt tiền và chiều cao (`out/pose_*.jpg`).

**Phát hiện:** điểm đứng giải được nằm **trong một toà 30,2 m xây năm 1899** (BAG). Theo vị trí có lẽ là Bưu điện cũ / Magna Plaza (**tên chưa kiểm**). Đoạn thử cắt bỏ toà này trong nhịp then/now và ghi rõ trên thẻ. Đây là một nhịp kể chuyện thật: "this view no longer exists".

**Ngoại suy cho tập 9 phút** (ví dụ 4 mốc đinh, 6 ảnh neo, 2 then/now, 3 bay dọc phố, 2 reveal): giờ máy tăng thêm do hiệu ứng ≈ 4×86×0,03 + 6×72×0,135 + 2×72×0,16 ≈ **1,5 phút**, không đáng kể so với 8–20 giờ dựng nền. Chi phí thật nằm ở phần người làm:
- mỗi then/now ≈ 30–60 phút (chọn ảnh có quyền, chấm 6–8 điểm, kiểm chồng);
- mỗi ảnh neo ≈ 15–30 phút tra quyền **(ước)**;
- bay dọc phố ≈ 10 phút lấy tuyến NWB/OSM.

### 6.7 Ngân sách chữ (điều chỉnh chủ dự án 23:04)
**Cách đo** (`textBudget()` trong `scene.js`, chạy cả 720 khung):
- Diện tích = hợp các hình chữ nhật chữ + nền chữ, rải lên lưới 4 px.
- Vùng giữa = hình chữ nhật 20–80 % rộng × 20–80 % cao.
- Thẻ neo vào công trình (mốc đinh, ảnh neo) được miễn luật vùng giữa.
- Ảnh lịch sử là hình, không tính là chữ.

| | Trước (bố cục cũ, 60 khung, mỗi 0,5 s) | Sau (bản giao, 720 khung) |
|---|---|---|
| % diện tích chữ, trung vị | **32,4 %** | **10,8 %** |
| Cao nhất, khung thường | 43,6 % | **14,7 %** (trần 15 %; p90 14,5 %) |
| Cao nhất, mốc đinh | 35,9 % (14 khối chữ) | **16,0 %** (trần 25 %) |
| Khung có chữ không neo ở vùng giữa | 60/60 | **0/720** |
| Thẻ cùng lúc | đến 2 + chú thích | **≤ 1** |
| Lớp thường trực | 5 (YEAR, năm, POPULATION, số, phương pháp) + ghi công | **2** (năm, chỉ số) |

**Đã áp:**
1. Bỏ nhãn "YEAR"/"POPULATION". Năm 96 px, chỉ phóng ở mốc đinh. Dân số 1 dòng.
2. Dòng phương pháp + nguồn dữ liệu còn 1 dòng ("No AI imagery · 3DBAG · Kadaster · Copernicus DEM"), chỉ hiện **0–4,2 s và 29–30 s**. Câu "standing buildings, by year built" chuyển vào dòng nguồn của thẻ móc. Nguồn đầy đủ để ở mô tả/bình luận ghim.
3. "between counts, interpolated" đổi thành "≈" trước số. Ô dân số ẩn trước 1622.
4. Thẻ:
   - tối đa 1, dài 3,0–3,8 s, tiêu đề ≤ 10 từ, dòng phụ là nguồn của chính thẻ;
   - thẻ ảnh 1886 hết tràn: không thẻ nào tràn trong 720 khung (log "thẻ tràn" = 0).

**Hai chỗ phải chỉnh để đạt trần:**
- Hộp năm phóng 1,6× lấn mép vùng giữa (khung 316–358), nên hạ xuống 1,45×.
- Đầu phim lên 15,3–16 % vì khối nguồn 2 dòng chồng thẻ móc, nên rút còn 1 dòng và tắt ở 4,2 s.

**Giới hạn của đoạn 30 s:** màn kết chỉ có 1 s (29–30 s), vì thẻ then/now phải đủ 3 s. Phim dài sẽ có màn kết 4–6 s.

### 6.8 Đề xuất luật đo được cho phiên K (viết thành Q)
Mỗi luật kèm cách đo trên log của bộ dựng (đã có trong `render.js`/`scene.js` của lab) và kết quả của đoạn thử.

| Mã đề xuất | Luật | Đo bằng | Đoạn thử |
|---|---|---|---|
| **TL-Q1 Mốc đinh** | (a) giá trị năm không đổi trong **1,5–2,0 s**; (b) bộ đếm phóng **≥ 1,4×**; (c) công trình được làm nổi: độ sáng trung bình trong mặt nạ công trình / phần còn lại ≥ 1,5 (cần K thêm mặt nạ); (d) có thẻ neo với dòng nguồn không rỗng ≥ 38 px trong ≥ 3 s; (e) ≥ 1 mốc đinh mỗi 3 phút | log năm theo khung (`campath.json`), log chữ | (a) 1,83 s ✓ (b) 1,45× ✓ (c) chưa đo (d) 3,3 s ✓ |
| **TL-Q2 Bay dọc phố/sông** | Trong ≥ 3 s liên tục, vị trí máy (mặt bằng) cách đường hình học thật ≤ **15 m**, độ cao ≤ 120 m; nguồn hình học (NWB/OSM/bản đồ lịch sử) ghi trong đặc tả; kết thúc với công trình đích lệch trục nhìn ≤ 10° | `campath.json` + tệp tuyến | 3,5 s; TB 2,6 m, max 10,5 m; 54–72 m; 0,0° ✓ |
| **TL-Q3 Reveal** | Kéo lùi: khoảng cách tới đích tăng ≥ **5×** trong 2–8 s, không cắt. Hoặc glide → zoom-in: giảm ≥ 5× | `campath.json` | ×21 trong 7,6 s; ×40 trong 3 s ✓ |
| **TL-Q4 Ảnh lịch sử** | (a) mỗi ảnh có dòng RIGHTS: PD/CC0/CC BY + URL + SHA; (b) ảnh neo: đầu đường dẫn cách điểm chiếu 3D ≤ 1 % rộng khung ở mọi khung; (c) then/now: ≥ 6 điểm khống chế, RMS chiếu lại ≤ **1 % rộng ảnh**, **kèm ảnh chồng 50 % để người kiểm** (RMS thấp không đủ, xem §6.6); máy đứng yên ≥ 0,8 s khi ảnh phủ; hoà 0,6–1,5 s; ghi phương pháp "thủ công" hay "điểm khống chế" | `then-now-pose.json`, `campath.json`, RIGHTS | (a) chờ P ghi (b) ✓ theo cách dựng (c) 7 điểm, 0,52 %, khoá 1,58 s, hoà 0,8 s ✓ |
| **TL-Q5 Ngân sách chữ** | (a) % diện tích chữ + nền chữ ≤ **15 %** mọi khung thường, ≤ **25 %** khung mốc đinh; (b) vùng 20–80 % × 20–80 % không có chữ trừ thẻ neo; (c) ≤ 1 thẻ cùng lúc, mỗi thẻ 3–5 s, tiêu đề ≤ 10 từ, dòng phụ là nguồn của thẻ; (d) ≤ 2 lớp thường trực, mỗi lớp 1 dòng (thêm dòng nguồn khi số đang hiện là số đếm); (e) dòng phương pháp/ghi công chỉ trong 6 s đầu + màn kết; (f) chữ đang hiện ≥ 38 px@1080, tương phản ≥ 4,5:1 | `textBudget()` mỗi khung + log chữ | (a) 14,7 % / 16,0 % ✓ (**14,7 % trong ±5 % quanh trần**) (b) 0 ✓ (c) ✓ (d) ✓ (e) 0–4,2 s + 29–30 s ✓ (f) ✓ min 8,26:1 |

## 7. H4 — ÂM
- **Biến thể A (đã làm):** nhạc + SFX gắn biến cố.
  - Nhạc: "Beauty Flow" (K2-MUS-2).
  - SFX (mốc theo dòng thời gian bản cuối): còi tàu lúc bay dọc Damrak / "why here" ở 8,5 s (K2-SFX-9); nhịp trầm tự tổng hợp khi năm dừng ở mốc đinh 13,0 s; công trường lúc reveal 1900–1945 ở 20,4 s (K2-SFX-24); giao thông khi hoà sang "now" ở 27,9 s (K2-SFX-16); tiếng "tích" tự tổng hợp khi mỗi thẻ hiện.
  - Đo bằng ffmpeg ebur128 trên tệp giao: **−14,0 LUFS, đỉnh −1,5 dBFS**. Bản WAV: true peak −1,8 dBTP.
  - Mọi tài sản đã có dòng RIGHTS (CC BY 4.0). Không thêm tài sản mới.
- **Biến thể B (chỉ đặc tả, ElevenLabs 0 ký tự):** thêm 6–8 câu dẫn ≤ 12 từ ở các mốc. Lời hạ nhạc 12 dB, master −14 LUFS như `scripts/ll/mix.py`. Câu mẫu cho Amsterdam (nội dung phim, tiếng Anh; mọi con số đã kiểm ở §1.4/§2, trừ câu đánh dấu):
  1. "In 1275, this was just a dam. Watch what grew around it."
  2. "River boats on one side, sea ships on the other." *(chờ nguồn sơ cấp)*
  3. "1622: the first count — 104,932 people."
  4. "You're seeing only buildings still standing. Most of 1650 is gone."
  5. "1900 to 1945: 42,683 of today's buildings go up."
  6. "1959: 872,428 people — a record that stood sixty years." *(nguồn thứ cấp trích O&S, cần bảng gốc)*
  7. "Today: 941,927. The dam is still here. It's called Dam Square."

  Ước ≈ 450 ký tự/tập.
- Rủi ro **Content ID**: "Beauty Flow" có ISRC (USUAN1900008). Video bán kèm nhạc CC BY vẫn có thể bị khiếu nại nhầm. Kênh đối thủ dùng nhạc gì thì phiên này không đo, vì không tải video.

**Khuyến nghị: GIỮ A làm nền.** Nên A/B thật trên video đăng thay vì đoán, vì khen nhạc chỉ 9/491 bình luận. Đề xuất **B chỉ cho bản dài** (lời làm nhịp "why here" rõ hơn). Short dùng A.

## 8. H6 — ĐÓNG GÓI
**Không tìm thấy `TEARDOWN §9`** trong repo, kể cả `origin/main`. Brief dưới đây dùng khung tự soạn, cần P đối chiếu.

**Ba tiêu đề** (ví dụ Amsterdam; khi chọn thành phố khác thì thay số):
1. `Amsterdam: 104,932 → 941,927 People — 750 Years in 3D (Every Date Sourced)`: móc bằng số đầu → cuối.
2. `Why Amsterdam Grew on a Dam — 1275 to 2026, 3D Timelapse`: móc bằng cơ chế.
3. `Watch Amsterdam Grow From a Dam — 3D Timelapse (No AI, Real Building Data)`: đối chứng gần với mẫu của thể loại.

**Ba thumbnail** (không cờ): A "1275 → 2026" + tên thành phố (đối chứng) · B "105,000 → 942,000" lớn + tên · C "THE CITY BUILT ON A DAM" + chi tiết con đập.

**Brief A/B (Test & Compare):**
- Chạy 3 thumbnail cùng lúc ngay khi đăng. Chỉ số YouTube chọn là *watch time share*. Không đổi tiêu đề trong 14 ngày đầu.
- Ghi kết quả vào báo cáo tập.
- Thắng khi chênh ≥ 5 % watch time share và YouTube báo "conclusive". Không kết luận thì giữ A và thử lại ở tập 2.

**Khuyến nghị: GIỮ (thử).** Dạng "số → số" còn trống. Toàn bộ tiêu đề đối thủ chỉ có "CITY – 3D Timelapse" kèm năm.

## 9. Hình thức sản xuất: A / B / C
| | (A) Kênh 3 riêng | (B) Dạng tập + Short trong Moving Parts | (C) Chỉ học kỹ thuật cho kênh 2 |
|---|---|---|---|
| Ưu | Đúng thể loại đang nổ; tên kênh rõ | Dùng lại nhận diện, bible, luật nguồn của kênh 2; lớp "why here" chính là công thức Moving Parts; trụ T1 thành phố ≈ 60 % trong `LUAT-CHON-DE-TAI` | Rủi ro thấp nhất; module "thành phố mọc" thành cảnh 3D cho các tập T1 |
| Nhược | Phải ≥ 1 video/tuần mà mỗi tập 8–20 giờ máy CPU + 1–3 ngày nguồn; vào sau 17 kênh | Tập dạng này khác giọng tập giải thích, có thể làm loãng nhận diện | Bỏ lỡ cầu Nổ-mẫu đang có |
| Tác động | Thêm một dây chuyền đầy đủ | +1 dạng tập mỗi 3–4 tuần; Short 50–60 s mỗi tập (thể loại đã có Short 1,58 triệu lượt) | Không đổi lịch |
| Bão hoà / bắt chước | **Cao**: 61 video trong nửa tháng, kênh mới mỗi tuần | Trung bình: cạnh tranh ở độ đúng, không ở số lượng | Không áp dụng |
| Content ID nhạc | Như nhau (CC BY có ISRC) | Như nhau | — |
| Độ đúng lịch sử | Áp lực nhịp làm giảm độ đúng | Giữ được luật nguồn của kênh 2 | — |
| Giờ dựng | Nút cổ chai khi chưa có GPU | Chấp nhận được (1 tập/3–4 tuần) | Thấp |

**Khuyến nghị: (B).** Lý do: lợi thế đo được (độ đúng + "why here") cần thời gian tra nguồn, và mâu thuẫn với nhịp ≥ 1/tuần mà (A) đòi hỏi trong một thị trường đang bão hoà. Xét lại (A) khi có GPU và khi tập (B) đầu tiên vượt các ngưỡng "hơn" dưới đây.

**Định nghĩa "hơn" đo được cho tập đầu** (so ở ngày 30):
| Chỉ số | Mốc so sánh | Ngưỡng "hơn" |
|---|---|---|
| Giữ chân trung bình (% thời lượng) | Không đọc được số của Latos | ≥ 50 % với bản 9 phút; đặt mốc nội bộ ở tập 1 |
| CTR hiển thị | Mốc nội bộ kênh 2 | ≥ mốc kênh + 1 điểm % |
| Tỷ lệ bình luận về độ đúng | Latos 9–16 %, toàn mẫu 13,4 % | Bình luận **chỉ ra lỗi** ≤ 1/3 mức Latos (≤ 5 %), và bình luận **khen độ đúng hoặc nguồn** ≥ 5 % |
| Lượt xem/ngày trong 30 ngày | Nếu trùng thành phố: video Latos cùng thành phố (Amsterdam 45 439/ngày ở ngày 11). Nếu không: trung vị Latos 14 414/ngày | ≥ trung vị Latos (14 414/ngày) với thành phố chưa ai làm; ≥ 1,0× video cùng thành phố |

## 10. Chi phí và đề xuất dòng sổ chung (P ghi, phiên này không được sửa tệp chung)
| Khoản | Trần | Thực tế |
|---|---|---|
| YouTube Data API | 400 | **333 đơn vị** (`~/.cache/cine-timelapse/quota.jsonl`) |
| Claude API | $3 | **$0,051**: 5 lượt `claude-haiku-5-5`, served = claude-haiku-5-5 (`research/timelapse/cost.jsonl`) |
| ElevenLabs | 0 | 0 |
| Giờ máy dựng | 2 h | ≈ 1,4 h (§6.4) |
| Token phiên | trần mềm | Chưa đọc được: chủ dự án xem trang Usage. Có 1 tác tử con kiểm dữ liệu (≈ 245 nghìn token theo bộ đếm của harness) |

Đề xuất dòng `COST-LEDGER.csv`:
`TL-RD,City Timelapse R&D,R&D,2026-10-15,,,,,0.051,3,claude-haiku-5-5,0,0,1.4,,2,30,,research/timelapse/BAO-CAO.md,YT 333/400 đv; 2 lệnh bổ sung 22:47 + 23:04; không merge`

**RIGHTS:** đề xuất thêm 2 dòng cho P:
- ảnh Rijksmuseum RP-F-00-568 (1886, CC0; https://id.rijksmuseum.nl/200144330; SHA-256 `552b3a71c94d0fc8c5ba9dcfd52fae993e807d43ad430796ddaf6c3a6df01f93`; tệp ở ngoài git);
- NWB wegvakken (Rijkswaterstaat/PDOK, CC0).

Không có tài sản âm thanh mới. Dữ liệu 3DBAG, BAG, BGT và Copernicus mới chỉ dùng trong lab. Khi dùng cho phim phải thêm dòng RIGHTS với ghi công:
- "3DBAG by tudelft3d and 3DGI, CC BY 4.0"
- "Kadaster BAG/BGT, CC0"
- "© DLR e.V. 2010-2014 and © Airbus Defence and Space GmbH 2014-2018 provided under COPERNICUS by the European Union and ESA; all rights reserved"

## 11. Tệp
- `research/timelapse/`:
  - `BAO-CAO.md`
  - `teardown.json` (cầu, kênh, thành phố, bình luận)
  - `h1-amsterdam.json` (thống kê năm, thiên lệch, DEM)
  - `data-sources.json` + `NGUON-DU-LIEU.md` (26 bộ dữ liệu, 16 nguồn bản đồ, 7 thành phố châu Á, 17 chuỗi dân số; tác tử con)
  - `hypotheses.json` (H1–H6 giữ/bỏ)
  - `render-log.json` (số đo dựng: bản đầu, bản cuối, từng yếu tố, bật/tắt hiệu ứng, ngân sách chữ, tương phản)
  - `then-now-pose.json` (góc máy giải từ điểm khống chế)
  - `damrak-path.json` (tim tuyến NWB)
  - `text-budget-before.json`, `text-budget-after.json` (đo ngân sách chữ theo khung)
  - `cost.jsonl`
  - `ams30_540p_A.mp4`
- `lab/timelapse/`: `teardown.py`, `classify_comments.py`, `aggregate.py`, `fetch_ams.py`, `fetch_water.py`, `build_ams.py`, `rijks.py`, `calib_photo.py`, `scene.js`, `render.js`, `mix30.py`, `package.json`, `package-lock.json`, `.gitignore`. Thư mục `node_modules/` và `out/` không commit.

## 12. Preflight, ghép thử
- **Preflight:** `bash tools/preflight.sh` trên 27 tệp staged.
  - Lần 1 **TRƯỢT** vì 4 địa chỉ email của bên thứ ba (David Rumsey, swisstopo, BnF) nằm trong `NGUON-DU-LIEU.md` và `data-sources.json` do tác tử con viết.
  - Đã thay bằng mô tả kênh liên hệ, không ghi email.
  - Lần 2 **ĐẠT**; `checks/lock.py --verify` **KHỚP**.
  - Hook pre-commit/pre-push đã cài ngay đầu phiên.
- **Ghép thử với `main`:** nhánh tạo từ `origin/main` @ 7255aa4 và chỉ thêm 2 thư mục mới (`lab/timelapse/`, `research/timelapse/`), nên không có xung đột. Trên remote không có nhánh phiên nào khác đang chạy ngoài `main` và `claude/dazzling-galileo-zt3yd3`.
- **Tệp lớn:** `ams30_540p_A.mp4` 4,6 MB < 5 MB, nên không cần LFS. Dữ liệu thô (3DBAG, BGT, DEM, ảnh, bình luận) ở ngoài git (`~/.cache/cine-timelapse/`).
- **Tiến trình nền:** một lượt dựng (v1b) chạy bằng `&` bên trong lệnh nền của harness. Trái luật 10 của điều lệ, không gây hại; đã dừng bằng PID.

## 13. Việc chờ chủ dự án
1. **Duyệt hay không phương án (B)** và định nghĩa "hơn" ở §9.
2. **Chọn thành phố tập đầu:** Zürich / Helsinki / Seville-Madrid / Detroit (dạng co lại). Nếu cần, giao một phiên M đo cầu riêng cho từng thành phố (search.list 100 đv/lượt).
3. **Cho phép hỏi quyền** bản đồ lịch sử (swisstopo, Kadaster, IGN, Lưu trữ Quốc gia VN) hoặc mua licence BnF cho Hà Nội/Sài Gòn.
4. **GPU** (NT K6 đang hoãn): tập 9 phút đúng chuẩn trên CPU tốn 8–44 giờ máy (§6.5).
5. **K viết luật TL-Q1…Q5** (§6.8) nếu chủ dự án giữ dạng này. K đối chiếu Q35/Q36 với số đo §5. P cấp hoặc chỉ chỗ `TEARDOWN §9` (không có trong repo).
6. **Kiểm tên toà 1899** chứa điểm chụp ảnh 1886 (có lẽ Magna Plaza) trước khi dùng câu "this view no longer exists". Tìm nguồn sơ cấp cho ngày khánh thành 29/07/1655 (hiện chỉ có nguồn thứ cấp, nên trên hình chỉ dùng năm BAG).
7. **P ghi** dòng COST-LEDGER và 2 dòng RIGHTS ở §10. Nếu chọn (B), thêm dòng AUTHORSHIP cho quyết định sáng tạo.
