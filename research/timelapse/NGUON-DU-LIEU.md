# Nguồn dữ liệu cho định dạng "Watch <CITY> grow — 3D timelapse"

Ngày kiểm tra: 2026-10-15. Dữ liệu máy đọc nằm trong `data-sources.json`, gồm URL bằng chứng cho từng nhận định.
Phạm vi: kiểm giả thuyết H1, tức mỗi toà nhà mọc lên đúng năm xây. Nguồn phải là dữ liệu mở có năm xây theo từng toà, kèm bản đồ lịch sử, chuỗi dân số và thẻ sự kiện có nguồn. Giấy phép phải cho phép thương mại vì phim được bật kiếm tiền trên YouTube và được bán.

## 1. Cách kiểm

- Mọi con số dưới đây lấy từ truy vấn thật trong ngày: WFS `resultType=hits`, Socrata `count(*)`, ArcGIS `returnCountOnly`, CKAN datastore, hoặc tải gói nhỏ hơn 200 MB (Catastro Sevilla 35 MB, GWR Zürich 122 MB). Không số nào lấy từ trí nhớ.
- **Đo dồn năm (heaping):** lấy mẫu ở khung lõi trung tâm và tính tỷ lệ năm tận cùng bằng 0 hoặc 5. Nếu năm phân bố đều, tỷ lệ này khoảng **20%**. Vượt xa 20% nghĩa là năm đã bị làm tròn hoặc gán giá trị mặc định. Chỉ số này phản ánh trực tiếp mức nói thật của câu "mọc đúng năm".
- Giấy phép đọc từ trang điều khoản, siêu dữ liệu CKAN/WFS hoặc file license đi kèm gói tải. Chỗ nào chưa đọc được văn bản gốc thì ghi `unclear`.

## 2. Bảng dữ liệu năm xây theo toà nhà

| Thành phố | Bộ dữ liệu | Giấy phép, thương mại | Số toà | % có năm | Dồn 0/5 (mẫu lõi) | Năm phổ biến nhất (mẫu) | Chiều cao |
|---|---|---|---|---|---|---|---|
| Zürich (toàn CH) | BFS GWR `GBAUJ` | BFS "Freie Nutzung, Quellenangabe Pflicht", **cho phép thương mại** | 54.185 (thành phố) | 100% | **23,8%** (n=3.107) | 1812 ×275 (mốc thay thế "trước 1813") | số tầng; swissBUILDINGS3D |
| Helsinki | `Rakennukset_alue_rekisteritiedot` `c_valmpvm` | CC BY 4.0 | 84.958 | 59,2% (lõi 75,6%) | **21,7%** (n=4.387) | 1928, 1927, 1938 | số tầng |
| Amsterdam (toàn NL) | BAG `bag:pand.bouwjaar` | **CC0** | 11.440.441 | 100% | 45,5% (n=5.000) | **1905 ×394, 1005 ×243** | 3DBAG (CC BY 4.0) |
| Kyoto | PLATEAU `bldg:yearOfConstruction` | PDL 1.0, tương thích CC BY 4.0 | không đếm | 82,6% (mẫu 6.428) | **19,1%** | 2024, 1932, 1995 | có (LOD1/2) |
| New York | Building Footprints `construction_year` | NYC Open Data Law, không ràng buộc | 1.083.059 | 99,1% | 57,0% (n=10.514) | **1900 ×2.349**, 1920, 1910 | `height_roof` |
| Wien | `GEBAEUDEINFOOGD` + `BAUPERIODEDETAILOGD` | CC BY 4.0 | 439.205 phần toà | 19,4% có năm chính xác (11.280) | 23,0% | 1912, 1910, 1911 | số tầng |
| Sevilla (toàn ES*) | Catastro INSPIRE BU | Giấy phép riêng của Catastro: **cho thương mại nếu dữ liệu đã được biến đổi** | 58.723 | 99,7% | 65,2% (n=9.195) | 1900, 1940, 1950 | số tầng (BuildingPart) |
| Montréal | Unités d'évaluation foncière | CC BY 4.0 | 514.600 đơn vị | ~95% (9999 = không rõ) | ~41% | 1910, 1900, 1885 | số tầng |
| Lyon/Bordeaux (toàn FR) | IGN BD TOPO `date_d_apparition` | Etalab 2.0 | 51.450.444 | ~72% | **87–88%** | 1850, 1800, 1880 | có |
| Paris | APUR `EMPRISE_BATIE_PARIS.an_const` | **ODbL (share-alike)** | 128.206 | 63,3% | 84,1% | 1800, 1700, 1750 | có |
| Melbourne (LGA) | CLUE `construction_year` | CC BY | 14.094 | 54,0% | 48,7% | 1900, 1870, 1910 | số tầng |
| Portland | Oregon SBFO `YEAR_BUILT` | **chưa rõ** | 2.170.837 (bang) | 91,8% (mẫu) | 26,5% (n=1.343) | 1912, 1890, 1910 | mái |
| Chicago | Footprints `year_built` | Điều khoản cổng dữ liệu, **chưa rõ** | 820.606 | 54,4% | 18,8% | 2006, 2005, 1891 | số tầng |
| Boston / SF | Sổ thuế tài sản (mức thửa đất) | PDDL | ~185k / 212k | cao | (1900 nổi trội) | 1900, 1920 / 1900 | không |
| Singapore | HDB Property Information | SODL v1.0 | 13.392 block | 100% | 19,1% | 1984, 1985 | số tầng |
| Hồng Kông | BD occupation permit | Điều khoản DATA.GOV.HK cho phép thương mại | 51.354 | 98,5% | 18,8% | 1988, 1989 | không |
| Copenhagen (toàn DK) | BBR `byg026Opførelsesår` | CC BY 4.0 | ~5 triệu (DK) | không đo được | không đo được | không đo được | số tầng |
| Berlin | Umweltatlas Gebäudealter | dl-de/zero-2.0 | **theo khối phố, không theo toà** | không áp dụng | không áp dụng | không áp dụng | Gebäudehöhen 2022 |
| Toronto, Brussels, Prague, Estonia, Finland (quốc gia) | không thấy trường năm mở | | | | | | |
| Tokyo 23 quận | PLATEAU | PDL 1.0 | | **0%: cả 23 tileset không có trường năm** | | | có |

\* Không gồm Xứ Basque và Navarra, hai vùng này có cơ quan địa chính riêng.

**Mốc giả và năm mặc định đã phát hiện:**
- BAG: 1005 = "không rõ hoặc rất cũ"; 1905 là giá trị mặc định cho nhà trước 1905.
- GWR: 1812 = "trước 1813".
- NYC, Boston, SF: 1900 (riêng SF là do hồ sơ cháy trong động đất 1906).
- Montréal: 9999. PLATEAU: 0001. Helsinki và Zürich: 1000.

**Hệ quả cho phim:** ở lõi phố cổ, dữ liệu châu Âu và Mỹ phần lớn chỉ đúng đến thập kỷ hoặc nửa thế kỷ. Phải xử lý mốc giả bằng luật riêng, ví dụ cho các toà này đã có sẵn ở khung đầu phim hoặc mọc theo pha bản đồ lịch sử. Thẻ "năm" chỉ nên gắn cho các toà có năm đáng tin.

## 3. Xếp hạng 10 thành phố

Tiêu chí, theo thứ tự ưu tiên:
1. Có năm theo từng toà.
2. Giấy phép thương mại rõ ràng.
3. Mức dồn năm thấp.
4. Có hình khối và chiều cao.
5. Có bản đồ lịch sử và chuỗi dân số chính thức.

| # | Thành phố | Lý do | Rủi ro chính |
|---|---|---|---|
| 1 | **Zürich** | 100% toà có năm, hầu như không dồn năm (21–24%), BFS ghi rõ cho phép thương mại, swisstopo cho hình khối 3D | Mốc 1812 phủ phố cổ. Giấy phép lớp bản đồ lịch sử Siegfried/Dufour chưa xác nhận |
| 2 | **Helsinki** | Có ngày hoàn công thật, hầu như không dồn năm, CC BY 4.0, có polygon | 41% toà toàn thành phố thiếu năm (chủ yếu nhà phụ); có mốc 1000 |
| 3 | **Amsterdam** | CC0, phủ 100%, polygon + chiều cao 3DBAG, sẵn API | Lõi phố dồn năm 45%; 1005/1905 chiếm khoảng 13% mẫu lõi |
| 4 | **Kyoto** | 82,6% có năm, dồn 19%, có LOD2 và chiều cao, CC BY-compatible | Nhà trước 1869 không có năm; bản đồ lịch sử chưa kiểm |
| 5 | **New York** | Phủ 99%, có chiều cao, không ràng buộc giấy phép, câu chuyện mạnh | Dồn năm 57%; riêng 1900 chiếm 22% mẫu Lower Manhattan |
| 6 | **Wien** | CC BY 4.0, năm chính xác cho 11 nghìn toà, phân kỳ cho phần còn lại, có ảnh hàng không 1938–1992 | Chỉ đạt H1 một phần; nhiều giá trị null |
| 7 | **Sevilla** (hoặc Madrid, Barcelona) | 99,7% có năm, polygon + số tầng | Lõi dồn 65%. Giấy phép đặc thù: chỉ dùng thương mại bản đã biến đổi, không được gọi là "cartografía catastral" |
| 8 | **Montréal** | CC BY 4.0, khoảng 95% có năm | Dữ liệu ở mức đơn vị định giá; dồn khoảng 41% |
| 9 | **Lyon** (đại diện FR, BD TOPO) | Etalab 2.0, phủ toàn quốc, có chiều cao | Năm trước 1900 dồn 87%, gần như chỉ dùng được theo pha |
| 10 | **Melbourne** | CC BY, có năm và số tầng | Chỉ phủ LGA trung tâm (14 nghìn toà); dồn 49% |

Thành phố suýt vào danh sách:
- **Copenhagen:** CC BY 4.0 nhưng chưa đo được dồn năm.
- **Portland:** dữ liệu đẹp nhưng giấy phép chưa rõ.
- **Hồng Kông:** đạt H1 từ 1947.
- **Berlin:** H1-lite rất tốt, có 11 bản đồ pha phát triển 1650–1993 theo dl-de/zero.

Loại vì giấy phép:
- Paris APUR (ODbL): dùng được nhưng có share-alike cho phần cơ sở dữ liệu.
- Chicago: dữ liệu cũ, dừng khoảng 2015.

## 4. Bản đồ lịch sử: giấy phép

| Nguồn | Thương mại | Ghi chú |
|---|---|---|
| David Rumsey | **Không** | "not for commercial use"; muốn dùng phải xin [email liên hệ trên trang Terms of Use của David Rumsey] |
| Gallica (BnF) | **Không, trừ khi mua licence** | Tái sử dụng thương mại là "payante et fait l'objet d'une licence" |
| NAS Singapore | **Không, trừ khi mua licence** | Licence từng ảnh qua e-Request, có phí; bản đồ gốc TNA cần xin TNA |
| Geoportal Berlin (Städtebauliche Entwicklung; Straube 1910) | **Có** | dl-de/zero-2.0. Straube có thêm một bản ghi dl-de/by-2.0 |
| Wien ảnh hàng không 1938–1992 | **Có** | CC BY 4.0 |
| Library of Congress | Thường được, kiểm từng mục | "No known restrictions on publication" |
| Wikimedia Commons PD-old | Có | Bản quét lấy từ Gallica có rủi ro pháp lý tại Pháp |
| swisstopo Zeitreise | Chưa rõ | Điều khoản free geodata cho thương mại nhưng không nêu tên lớp lịch sử |
| IGN État-major / Cassini | Chưa rõ | Etalab 2.0 loại trừ "cartes et SCANs" |
| Kadaster Topotijdreis | Chưa rõ | BRT là CC BY 4.0; lớp lịch sử chưa xác nhận |
| Bản đồ lịch sử Đan Mạch | Chưa rõ | Trang Dataforsyningen chỉ hiển thị bằng JavaScript |
| GSI Nhật | Chưa rõ | Luật Đo đạc điều 29/30; dùng trong video chưa được quy định rõ |
| Lưu trữ Quốc gia VN I/II, Bangkok, Lisboa | Chưa rõ | Không tìm thấy giấy phép mở |
| Allmaps / OldMapsOnline | Không áp dụng | Chỉ là công cụ; quyền nằm ở nơi giữ bản đồ |

## 5. Châu Á

| Thành phố | Mức | Năm theo toà | Bản đồ lịch sử | Dân số | Kết luận |
|---|---|---|---|---|---|
| Hà Nội | **H1-lite có điều kiện** | Không có. OSM có 20/71.406 toà ghi `start_date` | Commons có 90 file, phần lớn từ Gallica (thương mại phải trả phí); TT Lưu trữ QG I chưa rõ điều khoản | Tổng cục Thống kê (GSO): điều tra 1979–2019. Thời thuộc địa chỉ có bảng học thuật, số liệu vênh nhau (IER Hitotsubashi, INRS) | Chỉ làm được theo pha, sau khi giải quyết quyền 3–5 bản đồ |
| TP. Hồ Chí Minh | **H1-lite có điều kiện** | Không có (OSM 18/23.253) | Commons có 50 file (có bản Le Brun 1795) | GSO từ 1979 | Như Hà Nội |
| Singapore | **H1 một phần + H1-lite** | Chỉ có block HDB: 13.392 block, đủ năm, không dồn | NAS phải trả phí | SingStat: điều tra 1871–1931, 1947, 1957, 1970 về sau | Làm được câu chuyện "nhà ở công cộng mọc lên"; khu tư nhân và CBD không có năm |
| Bangkok | **Không khả thi** | Không có (OSM 43/80.548) | Không có giấy phép rõ | NSO Thái Lan | Loại |
| Tokyo | **H1-lite** | PLATEAU 23 quận không có trường năm | GSI và Thư viện Tokyo đều phải xin phép | Cục Thống kê (Statistics Bureau): điều tra 1920–2020 | Ở Nhật nên chọn **Kyoto (H1)**; Sapporo, Kanazawa khoảng 58% |
| Hồng Kông | H1 từ 1947 | 50.575 toà có ngày occupation permit | Chưa kiểm | C&SD | Ứng viên châu Á tốt nhất về dữ liệu |

## 6. Chuỗi dân số

Các nguồn chấp nhận được (cơ quan thống kê quốc gia hoặc thành phố, hoặc nguồn học thuật có thể trích dẫn):

| Thành phố | Nguồn |
|---|---|
| Mỹ (NYC, Chicago, Boston, SF, Portland) | U.S. Census Bureau WP-27 (1790–1990) và điều tra 2000–2020 |
| Amsterdam | CBS và OIS; trước 1900 dùng TSEG/NIDI |
| Zürich | Statistik Stadt Zürich |
| Wien | Stadt Wien / Statistik Austria |
| Berlin | AfS Berlin-Brandenburg |
| Helsinki | Statistics Finland |
| Copenhagen | Statistikbanken |
| Tây Ban Nha | INE, chuỗi liên điều tra từ 1842/1900 |
| Pháp | INSEE và EHESS "Cassini" (máy chủ từ chối kết nối khi kiểm) |
| Montréal | Statistics Canada |
| Melbourne | ABS |
| Kyoto, Tokyo | Statistics Bureau of Japan |
| Singapore | SingStat và Saw Swee-Hock (ISEAS) |
| Việt Nam | GSO và IER |
| Bangkok | NSO |

**Wikipedia không được chấp nhận làm nguồn**, chỉ dùng để tìm ra nguồn gốc.

## 7. Điều chưa biết (cần kiểm trước khi chọn thành phố)

1. Giấy phép thương mại của các lớp bản đồ lịch sử: swisstopo (Siegfried, Dufour), Kadaster Topotijdreis, IGN État-major, SDFI Đan Mạch, GSI Nhật, và nguồn bản đồ lịch sử của Kyoto.
2. Copenhagen BBR: tỷ lệ dồn năm ở lõi. Cần tài khoản Datafordeler miễn phí hoặc tải GeoPackage.
3. Giấy phép Oregon SBFO (Portland) và điều khoản Chicago.
4. Năm bắt đầu cụ thể của chuỗi dân số Zürich, Wien, Berlin, Helsinki, Copenhagen, Melbourne, Bangkok.
5. Ngữ nghĩa trường `beginning`/`end` của Catastro: 11% bản ghi Sevilla có hai giá trị khác nhau, có thể do cải tạo. Cần đọc đặc tả.
6. BDNB (CSTB, Pháp): giấy phép và độ phủ `annee_construction`. Chưa kiểm.
7. Prague (IPR), Estonia (EHR), Finland quốc gia (DVV), Brussels (UrbIS): chưa tìm thấy trường năm. Chưa kết luận là không có.
8. PLATEAU: có bị ràng buộc bởi Luật Đo đạc (測量法) khi dùng trong video thương mại hay không. Cần hỏi MLIT hoặc từng thành phố.
9. Điều khoản của GSO Việt Nam và Lưu trữ Quốc gia I/II về tái sử dụng thương mại. Trang GSO trả 502 qua proxy khi kiểm.
10. Điều khoản OneMap khi geocode địa chỉ HDB.
