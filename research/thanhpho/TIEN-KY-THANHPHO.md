# TIỀN KỲ THÀNH PHỐ — chọn thành phố cho tập Moving Parts tầng ĐẦY ĐỦ "từng toà mọc đúng năm"

> Phiên Tiền kỳ thành phố, 15–16/10/2026, theo lệnh chủ dự án (duyệt 16/10, Y7). Mẫu trình bày: `channel-k2/k2c-t3-01/TIEN-KY.md`.
> Nhánh tạo từ `origin/main` @ `7255aa4`. **Không merge.**
> Mọi lượt xem là **số công khai YouTube Data API, đọc ngày 15/10/2026 (UTC)**. Mọi điểm chấm, tỷ lệ và nhãn là **tự tính, không phải chỉ số YouTube**.
> Tệp thô (gói dữ liệu, trang giấy phép, ảnh) để **ngoài git** ở `/var/tmp/thanhpho/` và `~/.cache/cine-thanhpho/`. Trong git chỉ có SHA-256.

## 0. Khối điều lệ (chép lệnh, thêm cột thực tế)
| Trường | Lệnh | Thực tế |
|---|---|---|
| Loại phiên | Tiền kỳ (chọn thành phố) | như lệnh |
| Nhánh | `tienky-thanhpho` từ `origin/main` | `7255aa4`. Harness gán nhánh `claude/tienky-thanhpho-selection-91h55s`; cùng commit được đẩy lên **cả hai tên** (`tienky-thanhpho` theo lệnh) |
| Tệp được sửa | `research/thanhpho/**` (TIEN-KY-THANHPHO.md + *.json + licenses/) | chỉ thư mục này. Không sửa mã, `checks/`, `design/`, `scripts/`, `channel-*/`. **Không ghi COST-LEDGER, RIGHTS, AUTHORSHIP** (§9) |
| Trần | YouTube ≤ 300 đv · Claude API ≤ $2 (ghim) · ElevenLabs 0 | **224 đv** · **$0,0081** (1 lượt `claude-haiku-5-5`, served = haiku) · **0 ký tự** |
| Preflight | bắt buộc; che email | hook pre-commit/pre-push cài đầu phiên; `tools/preflight.sh --range origin/main..HEAD` **ĐẠT**, `lock.py --verify` **KHỚP** (§10). 0 email trong mọi tệp ghi |
| Điều kiện dừng | xong → đẩy → dừng | (1) xong việc |

**Lệch so với lệnh (có lý do):**
1. **Không chạy được 1 `search.list` cho mỗi thành phố.** 3 thành phố × 100 đv = 300 đv, không còn đơn vị nào cho `videos.list` (đọc lượt xem, thời lượng) và kiểm uploads tháng 10 của các kênh. Phiên gộp 5 thành phố vào **2 lượt** bằng toán tử `|`:
   - S1: `history 3D timelapse Zurich|Seville|Budapest|Helsinki|Detroit`
   - S2: `why Zurich|Seville|Budapest|Helsinki|Detroit`

   Giới hạn: thành phố có nhiều video lấn chỗ (Budapest ở S1, Detroit ở S2), nên **cầu riêng của Sevilla chưa đo được** (§2).
2. **Thêm 2 thành phố:** Helsinki (đứng đầu R&D về độ đúng dữ liệu) và Detroit (dạng "co lại").

## 1. Tóm tắt và khuyến nghị
**Khuyến nghị: Zürich cho tập đầu tầng đầy đủ.** Đây là thành phố duy nhất đạt tối đa cả ba tiêu chí khó chép (dữ liệu năm, bản đồ có quyền, khoảng trống). Điểm yếu thật nằm ở **cầu theo thành phố** (§2), nên góc kể phải mang cầu thay cho tên thành phố (§3).

| Thành phố | Cầu | Khoảng trống | Dữ liệu năm | Bản đồ có quyền | Công trình biểu tượng | **Tổng /25** | Rủi ro |
|---|---|---|---|---|---|---|---|
| **Zürich** | 2 | **5** | **5** | **5** | 4 | **21** | XANH |
| Helsinki | 1 | 4 | 3 | **5** | 4 | 17 | XANH |
| Detroit | **4** | 3 | 3 | 4 | 3 | 17 | **VÀNG** |
| Sevilla | 2 | **5** | **1** | 4 | 3 | 15 | XANH |
| Budapest | **4** | **0** | **0** | 2 | 2 | 8 | XANH |

Thang 0–5 do phiên tự chấm. Căn cứ từng ô ở `cham-diem.json` và §2–§6.

**Bốn phát hiện đổi quyết định so với R&D:**
1. **Budapest đã hết khoảng trống.** Có ≥ 6 video 3D/timelapse Budapest, trong đó 5 video đăng từ 05/10 đến 15/10/2026 (Urbis Anno, RoZoom Maps, Relax and Understand, CityLapse History, Epic 3D). Thêm TimeLapse Lords (02/09, **209 869** lượt). 2/5 video đầu đã ghi nguồn KSH. Dữ liệu năm cũng không có: OSM chỉ **1,0 %** toà có `start_date`. → **Loại.**
2. **Sevilla không dựng được thời hoàng kim bằng năm toà.** Catastro có 99,7 % toà mang năm, nhưng chỉ **25 toà ≤ 1800** và **12 toà ≤ 1717** trên 58 549 toà; lõi phố cổ dồn 0/5 tới **65,0 %**. Trường `beginning` thực chất là năm xây hoặc cải tạo lớn gần nhất. Câu hỏi hay nhất của Sevilla (cảng giàu nhất thế kỷ 16) rơi đúng vào quãng không có dữ liệu. → Chỉ làm được ở tầng "pha bản đồ" (H1-lite), không phải tầng đầy đủ.
3. **Zürich có thứ không thành phố nào khác có:** mô hình 3D lịch sử **Zürich 4D**, CC0, theo từng toà, ở các mốc 1200 / 1500 / 1800 (1800: 5 688 toà; dựng từ Murerplan 1576, Müllerplan 1788–93). Đây là lời giải có sẵn cho **thiên lệch sống sót** mà R&D đã đo ở Amsterdam (§4). Ngoài ra GWR còn ghi **8 677 toà đã phá dỡ, kèm năm phá (1999–2026)**, đủ để làm toà "biến mất" ở thời hiện đại.
4. **Helsinki đúng đến năm, không đến ngày.** 72,5 % "ngày hoàn công" là 31/12 hoặc 01/01, nên R&D ghi "ngày hoàn công thật" là quá lời. Trước 1900, dữ liệu dồn 39–44 %.

**Dự phòng:**
- **Detroit** cho tập thứ hai, dạng "co lại". Cầu mạnh nhất (Cầu-ngách ĐẠT), có sổ phá dỡ ghi đến ngày, nhưng rủi ro VÀNG, giấy phép cổng dữ liệu chưa rõ, và công số hoá Sanborn lớn nhất.
- **Helsinki** nếu chủ dự án muốn rủi ro thấp nhất về quyền (8 lớp CC BY 4.0).

## 2. Cầu (YouTube Data API) — `cau.json`
**Cách đo:**
- 2 lượt `search.list` (type=video, order=relevance, 50 kết quả, en/US, không giới hạn ngày) + `videos.list` cho 100 video.
- Video được gán cho một thành phố khi tên thành phố có trong tiêu đề. Dài: ≥ 480 s. Short: ≤ 180 s.
- **Kiểm kênh timelapse** (đối chiếu `teardown.json`): `channels.list` + 50 upload mới nhất của Latos và 10 kênh, đọc đến 15/10/2026.
  - Kết quả: **0/11 kênh** đã làm Zürich, Sevilla, Budapest, Helsinki hay Detroit.
  - timewarp cities có 112 video, mới kiểm 50 video mới nhất.
  - Trong tháng 10, các kênh này vẫn đăng dày: Latos 7, Timeline Cities 13, timewarp 14, DataShark 11 video.

| Thành phố | S1 (3D timelapse): số video · dài/Short · lớn nhất | S2 ("why"): số video · lớn nhất (dài) | Nhãn LUAT-CHON-DE-TAI theo thành phố | Lần xin (R&D, 491 bình luận) |
|---|---|---|---|---|
| Zürich | 1 (Short Google Earth 21 101, không phải lịch sử) | 8 · 64 084 ("Why Billionaires Choose Zurich", 01/2026) — cả 8 đều du lịch/lối sống | Không Cầu-ngách (không video dài 10–100 nghìn trong 90 ngày), không Cầu-bền | 0 |
| Sevilla | 0 | 1 · 5 595 (mật độ đô thị, 2025) | **chưa đo riêng** (bị pha loãng) | 1 |
| Budapest | **10 · 6 video thể loại · 5 video từ 01/10** · 209 869 (TimeLapse Lords, cố định + AI) | 3 · 7 065 | cầu thể loại có thật; cung bùng nổ | **4** |
| Helsinki | 3 Short · 1 411 ("Watch Helsinki Grow… in 60 Seconds", 03/2026) | 3 · 18 703 (du lịch); Short "Why Helsinki Wasn't Even Supposed To Be The Capital" 206 (20/09/2026) | không | 0 |
| Detroit | 0 | **34** · 1 982 434 (CNBC, 13 phút, 2022); Versed 203 084; The Why Minutes 135 176 | **Cầu-ngách ĐẠT:** CityWise "Why Detroit Fixed Its Downtown (And Baltimore Didn't)" 36 892 lượt, 16 phút, 21/09/2026. **Cầu-bền KHÔNG ĐẠT:** top 5 video dài không có video ≥ 500 nghìn (CNBC đứng sau) | 2 |

**Đọc bảng:**
- Cầu của **dạng** "thành phố mọc 3D" là Nổ-mẫu (R&D: 6 video ≥ 500 nghìn trong 90 ngày).
- Với thành phố chưa ai làm, cầu riêng chỉ đo được gián tiếp. Zürich và Helsinki gần như không có cầu "lịch sử" trên YouTube, chỉ có cầu du lịch/lối sống.
- Bài học từ Latos: Prague 1,14 triệu lượt (R&D). Người xem thể loại này xem cả thành phố họ chưa từng xin, nhưng phiên này **không có số đo nào chứng minh điều đó cho Zürich**. Đây là rủi ro chính của khuyến nghị.

**Khoảng trống** (`claude-haiku-5-5` đọc tiêu đề + mô tả của tối đa 5 video có tên thành phố):

| | Có nguồn số liệu | Có cơ chế "vì sao" |
|---|---|---|
| Zürich | 0/4 | 2/4 (lối sống, không phải lịch sử) |
| Sevilla | 0/1 | 0/1 |
| Budapest | **2/5** (KSH) | 0/5 |
| Helsinki | 0/2 | 0/2 |
| Detroit | 0/5 | 2/5 |

## 3. Góc Moving Parts — nghịch lý + 3 tiêu đề (≤ 60 ký tự)
Nội dung phim viết bằng tiếng Anh. Mọi số dưới đây đã đọc từ nguồn trong phiên, trừ chỗ đánh dấu **(chờ nguồn)**.

| Thành phố | Nghịch lý một câu | Cơ chế | Ba tiêu đề (ký tự) |
|---|---|---|---|
| **Zürich** | *"One of the richest cities on Earth spent 27 years losing people — 440,180 in 1962, 355,901 in 1989 — and only beat its old record in 2022. It didn't grow outward. It tore itself down and rebuilt: 8,677 buildings demolished since 1999, 9,784 built."* | quy hoạch và luật (biên giới đóng từ sáp nhập 1934 — **chờ nguồn** cho "không sáp nhập thêm"; thay toà cũ bằng toà mới); sáp nhập 1893 (25 102 năm 1880 → 117 044 năm 1893); phá thành luỹ từ 1833; ga 1847 | 1. **Why Zürich Shrank While Getting Rich** (37) · 2. **Zürich Tore Down 8,677 Buildings. Then It Grew.** (47) · 3. **How a Toll Town Became Switzerland's Biggest City** (49) |
| Helsinki | *"Finland's capital was a burnt-out wooden town of a few thousand when a Russian emperor chose it over Turku in 1812 — and every grand square you see was drawn on paper first."* | luật và chính trị (đổi thủ đô 1812), quy hoạch Ehrenström/Engel 1820, cảng và pháo đài Sveaborg 1748 | Why Helsinki Became Finland's Capital (37) · The Russian Plan Behind Helsinki (31) · Why Finland Moved Its Capital to Helsinki (41) |
| Detroit | *"The city that built the machine that let America leave the city: 1,849,568 people in 1950, about 640,000 today — and 31,904 demolitions since 2014 alone."* | công nghiệp ô tô, đường cao tốc, ngoại ô hoá (VÀNG), phá sản 2013 | Why the Car City Lost Two-Thirds of Its People (46) · Watch Detroit Shrink: 1950 to 2026 in 3D (40) · Why Detroit Has 31,904 Fewer Buildings Since 2014 (49) — "fewer" cần đối chiếu số xây mới **(chờ nguồn)** |
| Sevilla | *"Europe's richest port of the 1500s sat far up a river, not on the sea — and the river is why it lost the crown to Cádiz in 1717."* | sông Guadalquivir, độc quyền Casa de Contratación 1503–1717 (luật) | Why Spain's Richest Port Was Nowhere Near the Sea (49) · How Seville Lost the New World to Cádiz (39) · Why Seville Ruled Atlantic Trade, Then Lost It (45) — khoảng cách tới biển **(chờ nguồn)** |
| Budapest | *"Budapest didn't exist until 1873 — a hilly royal town and a flat merchant town on opposite banks, joined by one bridge in 1849."* | sông, địa hình, luật (hợp nhất 1873) | Why Budapest Was Two Cities Until 1873 (38) · Why Pest Grew and Buda Didn't (29) · One Bridge Made Budapest (24) |

**Vì sao góc Zürich mang được cầu:** câu hỏi "giàu mà co lại" là cơ chế Moving Parts thuần ("how places get rich"). Số liệu nằm ngay trong hai bộ dữ liệu sẽ dựng (GWR + chuỗi dân số CC0), nên hình và lời khớp nhau 1:1. Tiêu đề không cần người xem đã từng tìm "Zürich history".

## 4. Dữ liệu năm xây theo toà — kiểm lại R&D bằng API thật (`du-lieu-nam.json`)
| Thành phố | Bộ dữ liệu · giấy phép | Số toà | % có năm | Dồn 0/5 (≈ 20 % là thật) | Đối chiếu R&D | Phát hiện mới |
|---|---|---|---|---|---|---|
| **Zürich** | BFS GWR (zh.zip, SHA `d6babcae…`) · "Freie Nutzung… kommerzielle Zwecke", ghi nguồn bắt buộc | 54 185 | **100 %** | 21,2 % thành phố · **23,8 %** lõi | **khớp** (54 185; 23,8 %; 1812 ×275 ở lõi) | trước 1800 dồn **57–58 %**; 436 toà mã giả 1812 (toàn thành phố); **8 677 toà phá dỡ có năm phá** 1999–2026, so với 9 784 toà xây từ 1999 còn đứng; GWR là **điểm**, khối và mái lấy từ LoD2 CC0 của thành phố |
| Helsinki | Rakennukset WFS · CC BY 4.0 | 84 958 | 59,2 % (lõi 98,6 %) | 21,6 % | **khớp** % toàn thành phố. **Lệch** % lõi: R&D 75,6 % lọc theo polygon, phiên này lọc theo toạ độ điểm | 72,5 % ngày là 31/12 hoặc 01/01; trước 1900 dồn 43,5 %; phần thiếu năm chủ yếu là nhà kho, nhà phụ |
| Sevilla | Catastro INSPIRE BU (SHA `192f915f…`) · thương mại **chỉ khi đã biến đổi**; không gọi là "cartografía catastral" | 58 723 | 99,7 % | 41,5 % thành phố · **65,0 %** lõi | **khớp** (65,2 % → 65,0 %; n 9 195 → 9 211) | **25 toà ≤ 1800; 12 toà ≤ 1717**; 11 % bản ghi có `beginning` ≠ `end` |
| Budapest | OSM (ohsome, 27/07/2026) · ODbL | 352 125 | **1,0 %** (3 529) | 18,4 % (trên 3 442) | R&D chưa kiểm | không có sổ mở theo toà. Overpass/Geofabrik bị proxy cắt; ohsome chỉ cho đếm (lấy hình học trả 403) |
| Detroit | Parcels (Current) + Completed Demolitions (ArcGIS) · **giấy phép chưa rõ** (trường license trống) | 377 940 thửa | 59,9 % | 23,4 % (trước 1950: 20,4 %) | R&D chưa kiểm | **31 904 vụ phá dỡ có ngày**, 02/01/2014 → 09/10/2026; ~151 nghìn thửa không năm (phần lớn đất trống). Mức thửa, không phải toà |

**Hệ quả cho lời hứa của tập Zürich:**
- Dùng **"Standing buildings from the federal register; lost buildings from the city's own 3D reconstructions."**
- Giai đoạn trước 1800 nói "đúng đến thập kỷ".
- 436 toà mã 1812 cho hiện sẵn ở mốc 1800 của Zürich 4D, không cho "mọc" năm 1812.
- Mốc 1200 và 1500 của Zürich 4D phần lớn có độ tin cậy **"tief"** (dựng theo giả thuyết): 15 760/16 999 khối ở mốc 1200. Trên hình phải ghi "reconstruction (hypothesis)", và dùng khối mờ như R&D đề xuất.

## 5. Bản đồ lịch sử có quyền thương mại (`ban-do-cong-trinh-*.json`, `licenses/`)
| Thành phố | Lớp quyền RÕ | Đã có toạ độ | Lớp tiêu biểu (năm · giữ · quyền · độ phân giải) | Chưa rõ quyền → đường liên hệ |
|---|---|---|---|---|
| **Zürich** | **8** | **8/8** | Gyger Schanzen ~1644 (Stadt, CC0) · Gyger 1667 (Kanton, CC0) · Wild-Karte 1843–51 (Kanton, CC0, 2,5 m/px) · Altstadtkataster 1859–67 (Stadt, CC0, 1:200, chu vi từng toà) · Kellerplan 1864 (Stadt, CC0, 1:6 600) · Siegfried 1870–1949 + Dufour 1844–64 (swisstopo, "© swisstopo" — điểm "chưa rõ" của R&D **đã giải**) · Übersichtsplan 1932–61 (Stadt, CC0, 1:5 000) · **+ Zürich 4D** (3D theo toà: 3000 TCN, 200, 1200, 1500, 1800; CC0; OBJ/DXF/GPKG/WFS) | bản quét gốc Murerplan 1576, Müllerplan 1788–93, Breitinger 1814 (e-rara chặn bằng JS): Zentralbibliothek Zürich, trang Kontakt. Không bắt buộc, vì Zürich 4D đã dựng từ các bản đồ này |
| Helsinki | **8** | **8/8** | 1749 · 1780–82 · 1803 · 1820 Ehrenström · 1878 Kjerrström · Senaatinkartta 1870–1907 · 1900/1909 (1:12 000, ~0,76 m/px) · ảnh hàng không chỉnh hình 1932/1943/1950 — tất cả HRI, CC BY 4.0 | Kansallisarkisto (trả 403); Kansalliskirjasto/Doria: trang contact-information |
| Sevilla | **11** | 3/11 | Olavide 1771 + 1788 (RAH qua Europeana, PDM) · 1848–50, 1904 (ICGC, PDM) · 1860 (Banco de España, CC0) · Planimetría 1873, Minuta 1917, MTN50 1918 (IGN/CNIG, CC BY 4.0, WMS) · Ensanche 1929 (CNIG, ~0,20 m/px) · **Vuelo Americano 1956–57** (1 m/px) | quyền RAH chỉ đọc được qua Europeana, phải đối chiếu tại bibliotecadigital.rah.es; BNE yêu cầu ghi nguồn và nộp bản ấn phẩm |
| Budapest | 5 | **0/5** | SLUB Plan von Ofen (PDM, chưa có năm) · Fotothek 1849 (**CC BY-SA 4.0**) · British Library 1868 (PDM) · Kogutowicz 1920 (ICGC, ~2,1 m/px) · NLI 1942 (PDM) | Hungaricana (BFL, MNL): xin phép trước khi công bố — "khong"; MAPIRE chặn |
| Detroit | 6 | 1/6 (USGS) | Farmer 1835 (1:2 400, ~0,2 m/px) · Sanborn 1884/1897/1910/1929/1921–50 · phối cảnh 1889 · atlas 1893 (LoC, PD) · USGS topo 1905–1968 (PD, GeoPDF) | HOLC: bản quét NARA là PD, nhưng lớp georeference của Mapping Inequality là **CC BY-NC → không dùng** |

**Ước công số hoá** (giờ người, **(ước)**, chi tiết theo lớp trong JSON):
- Zürich **80–130**. Phần lớn là kiểm và ghép, vì Zürich 4D + Altstadtkataster đã có khối nhà.
- Helsinki 90–150 (phải tự dựng toà đã mất từ 1803/1878/1900).
- Sevilla 90–150 (8 lớp phải georeference).
- Budapest 50–80 (ít lớp, độ phân giải thấp).
- Detroit **180–330** (Sanborn từng toà, 5 năm).

## 6. Dân số và mốc đinh, công trình biểu tượng
**Chuỗi dân số (nguồn chính thức, đã tải, có SHA):**

| Thành phố | Nguồn · giấy phép | Từ năm | Mốc chọn | Lưu ý |
|---|---|---|---|---|
| **Zürich** | Statistik Stadt Zürich `BEV324OD3243` · CC0 · SHA `309311a0…` (phiên mẹ tải lại, khớp SHA tác tử con) | **1357** | 1357: 6 600 · 1529: 5 080 · 1637: 8 621 · 1799: 10 000 · 1880: 25 102 · 1893: 117 044 · 1934: 315 864 · **1962: 440 180** · **1989: 355 901** · 2022: 443 037 · 2025: 452 421 | đơn vị "wirtschaftliche Bevölkerung". Ranh giới lịch sử, phiên **suy** ra từ bước nhảy 1893/1934 (metadata không ghi) |
| Helsinki | Kaupunkitieto PxWeb (HRI) · CC BY 4.0 | 1875 | 1875: 23 070 · 1900: 79 126 · 1945: 276 277 · 1950: 370 962 · 1960: 448 315 | dân số "henkikirjoitettu". Sáp nhập lớn 1946. Trước 1875 chỉ có số tròn trong văn bản |
| Sevilla | INE "Alteraciones de los municipios" · SHA `50f0c135…` | 1842 | 1857: 112 529 · 1900: 148 315 · 1950: 376 627 · 1991: 704 857 | không có số chính thức cho thế kỷ 16–17 |
| Budapest | KSH Évkönyv 2010 bảng 4.1 | 1870 | 1870: 302 086 · 1941: 1 712 791 · 1980: 2 059 347 · 2011: 1 733 685 | ranh giới không ghi; số 1870–1890 lệch nguồn thứ cấp |
| Detroit | Census POP-WP027 (Gibson 1998) | 1840 | 1840: 9 102 · **1950: 1 849 568** · 1990: 1 027 974 · 2020: 639 471 | 2000/2020 lấy từ estimates base, **không phải số đếm điều tra** (API cần khoá) |

**Mốc đinh Zürich (7, nguồn HLS 000171 + CKAN):**
1. ~200: Statio Turicensis (trạm thuế).
2. 853: Fraumünster.
3. 1100–1230: Grossmünster.
4. ~1644: thành luỹ Barock (Gyger).
5. **1833: bắt đầu phá thành luỹ.**
6. 1847: ga đầu tiên.
7. **1893 và 1934: sáp nhập.**

Thêm hai mốc dữ liệu: 1962 (đỉnh dân), 2022 (vượt đỉnh). Cơ chế "hồ chảy ra sông Limmat" **chưa có nguồn đọc được**, nên không dùng làm thẻ.

**Công trình biểu tượng Zürich** (hình học: LoD2 CC0 của Stadt Zürich + Zürich 4D; ảnh: BAZ 1870–1900 CC0):
- **Grossmünster** (1100–1230, HLS).
- **Fraumünster** (853; có trong các mốc 4D).
- **Hauptbahnhof** (Wanner 1865–71, Kanton Inventar).
- St. Peter, ETH, Prime Tower: dùng được hình học, nhưng **năm chưa có nguồn** → chưa làm mốc đinh.

Ba thành phố còn lại (chi tiết trong JSON):
- Sevilla: Giralda, Torre del Oro, Alcázar, Plaza de España 1929, Puente de Triana 1852; ảnh LoC "No known restrictions"; PNOA LiDAR.
- Detroit: HABS/HAER (Guardian MI-273, Olympia MI-252, Tuller MI-335, Piquette MI-347). Có ảnh và trang dữ liệu, **không có bản vẽ đo đạc**.
- Budapest: chỉ OSM; năm của Parliament, Basilica và Hoàng cung chưa có nguồn đọc được.

## 7. Mức rủi ro (QUAN-TRI-RUI-RO)
| Thành phố | Mức | Lý do |
|---|---|---|
| **Zürich** | **XANH** | Câu hỏi là quy hoạch và dân số. **Tránh** khung "ngân hàng / bí mật ngân hàng / thiên đường thuế": tập không cần đến. Nếu chạm tới thì thêm câu miễn trừ tài chính và nâng lên VÀNG |
| Helsinki | XANH | lịch sử Nga–Thuỵ Điển, trình bày theo hồ sơ |
| Sevilla | XANH | buôn bán châu Mỹ và nô lệ: phải nói có nguồn, không né |
| Budapest | XANH | lọc bình luận dân tộc chủ nghĩa (Trianon) |
| Detroit | **VÀNG** | chủng tộc, đường cao tốc, khu dân cư (`LUAT-NOI-DUNG.md` §8), 1967, phá sản 2013. Cần đủ 6 điều kiện VÀNG |

**Thứ tự VÀNG:** T2 và T3 đều VÀNG, nên tập kế phải là XANH. Zürich XANH đáp ứng luật này.

## 8. Chi phí tập đầu Zürich (ước) và chi phí phiên
**Tập 9–11 phút, tầng đầy đủ (ước):**
- **Số hoá bản đồ + ghép 4D:** 80–130 giờ người, hoặc phiên tra nguồn/dựng tương đương.
- **Thẻ có nguồn:** 15–25 thẻ, mỗi thẻ 1–2 giờ (theo R&D) → 20–40 giờ.
- **Giờ máy CPU:** cảnh ≈ 54 nghìn toà + ≤ 17 nghìn khối 4D, dưới giới hạn 300 nghìn toà/cảnh đo ở R&D. Theo ngoại suy R&D: **≈ 8–10 giờ máy** ở 1080p, ×2 nếu chống răng cưa 2 lượt.
  - Gói OBJ của 4D nặng (mốc 1200: 529 MB), phải giảm lưới. Việc này **chưa đo**.
- **API:** tra nguồn Sonnet/Haiku ≈ $1–3 (ước). Giọng ElevenLabs ≈ 8–10 nghìn ký tự cho bản dài + Short. Tính ở G1.
- **Không có chi phí giấy phép:** cả 8 lớp + 4D + GWR + LoD2 đều CC0/miễn phí. Ghi công "© swisstopo" và "Bundesamt für Statistik; Eidg. Gebäude- und Wohnungsregister".

**Chi phí phiên này (`cost.json`, `cost.jsonl`):**

| Mục | Trần | Thực tế |
|---|---|---|
| YouTube Data API | 300 | **224**: search 200 · channels 11 · playlistItems 11 · videos 2 (sổ `quota.jsonl` ngoài git) |
| Claude API | $2 (ghim `claude-haiku-5-5`) | **$0,0081**, 1 lượt, served = `claude-haiku-5-5` |
| ElevenLabs | 0 | 0 |
| Token | trần mềm | 2 tác tử con tra bản đồ/giấy phép: 242 nghìn + 317 nghìn token (bộ đếm harness) |

**Chỉ số trong ±5 % quanh ngưỡng:** không có.
- Ngưỡng Cầu-ngách 10–100 nghìn: CityWise 36 892 nằm xa biên.
- Dồn 0/5 GWR thành phố 21,2 % so với mức "thật" 20 % chỉ là mốc tham chiếu, không phải ngưỡng luật.

## 9. Tệp đã ghi và đề xuất ngoài vùng
**Đã ghi (`research/thanhpho/`):**
- `TIEN-KY-THANHPHO.md`.
- JSON: `cau.json`, `du-lieu-nam.json`, `cham-diem.json`, `cost.json`, `cost.jsonl`, `ban-do-cong-trinh-zh-hel.json`, `ban-do-cong-trinh-sev-bud-det.json`.
- `licenses/`: 25 tệp.
  - GWR, Catastro (phiên mẹ).
  - Stadt/Kanton Zürich CC0, swisstopo, Zürich 4D, HRI CC BY 4.0, Finna.
  - CNIG, ICGC, Europeana RAH/BdE, BNE, PNOA lịch sử, LoC (ảnh, GMD, Sanborn, HABS), USGS, Mapping Inequality, Detroit open data, Hungaricana, Fortepan, OSM ODbL.
  - Mọi email đã thay bằng mô tả đường liên hệ.

**Sự cố đã khắc phục:** tác tử con lỡ ghi nối vào `sevilla-catastro-inspire.txt` (tệp đã commit). Nó đã khôi phục bằng `git checkout`, và tệp hiện tại khớp bản commit.

**Đề xuất cho P (chưa ghi, ngoài vùng lệnh):**
1. `COST-LEDGER.csv`: `TP-01,Tiền kỳ thành phố,Tiền kỳ,2026-10-16,,,,,0.0081,2,claude-haiku-5-5,0,0,,,,,,research/thanhpho/TIEN-KY-THANHPHO.md,YT 224/300 đv; 2 tác tử con; không merge`
2. `RIGHTS.md`: thêm GWR, Zürich 4D, LoD2 Stadt Zürich, các lớp bản đồ CC0 và swisstopo **khi tập dùng thật** (G1).
3. `AUTHORSHIP.md`: ghi quyết định chọn thành phố và góc kể sau khi chủ dự án duyệt.

## 10. Preflight
- `bash scripts/env/verify.sh`: 10 PASS, 3 FAIL (three.js, tifffile/pyshp, k2v node_modules). Cả 3 không liên quan việc tiền kỳ.
- Hook pre-commit/pre-push cài đầu phiên. Mỗi commit: `preflight ĐẠT`, `lock.py --verify KHỚP`. Không dùng `--no-verify`.
- Lần cuối: `tools/preflight.sh --range origin/main..HEAD`, kết quả ghi trong commit cuối.
- Ghép thử: nhánh chỉ thêm tệp mới trong `research/thanhpho/` (thư mục mới), nên không xung đột với `main`, `timelapse-rd` hay `k2c-t3-tienky`.

## 11. Việc đang chờ chủ dự án
1. **Duyệt Zürich** cho tập đầu tầng đầy đủ, với góc "Why Zürich Shrank While Getting Rich", hoặc chọn dự phòng: Detroit (VÀNG, cầu mạnh) hay Helsinki (XANH, quyền đơn giản). Ghi vào AUTHORSHIP.
2. **Chấp nhận rủi ro cầu theo thành phố của Zürich** (không đo được cầu lịch sử riêng), hoặc giao thêm 100 đv để đo riêng "Zurich history" và "Seville history".
3. **Duyệt lời hứa mới:** "Standing buildings from the federal register; lost buildings from the city's own 3D reconstructions (hypothesis where marked)."
4. **Nguồn còn thiếu trước G1:**
   - Zürich: nguồn cho "không sáp nhập sau 1934"; tách phần tăng dân 1880→1893 do sáp nhập; năm St. Peter, ETH, Prime Tower; cơ chế hồ → Limmat.
   - Sevilla: khoảng cách cảng tới biển.
   - Detroit: số xây mới đối chiếu với số phá dỡ; giấy phép cổng dữ liệu (liên hệ qua trang Department of Innovation & Technology, City of Detroit).
5. **Có cho đo giảm lưới gói OBJ Zürich 4D** (trước G1, 1–2 giờ máy) hay không.
6. **P chép các đề xuất §9.**
