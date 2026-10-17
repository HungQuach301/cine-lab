# NC-BD — Dữ liệu ranh giới lịch sử và thiết kế "bản đồ chiến lược" + "inset định vị" cho series lịch sử: BÁO CÁO NGHIÊN CỨU

> Phiên nghiên cứu NC-BD, 17/10/2026, theo đề xuất của chủ dự án ngày 17/10. Nhánh `nc-ban-do` tạo từ `origin/main` @ `82a17ae`. **Chỉ tài liệu và mẫu dữ liệu nhỏ. Không merge. DỪNG chờ chủ dự án.**
> Giấy phép đọc **nguyên văn từ trang gốc** bằng `curl` ngày 17/10/2026 (~14:20–14:35 UTC). Văn bản trích kèm SHA-256 của trang ở `reports/nc-ban-do/giay-phep/GIAY-PHEP-NGUYEN-VAN.md`. **Không phải tư vấn pháp lý.**
> Số đo độ chính xác (khoảng cách đỉnh, độ lệch giữa hai nguồn) là **tự đo** trên mẫu đã tải (`reports/nc-ban-do/py/*.py`). Chỗ nào là ước tính ghi **(ước)**; chỗ nào chưa kiểm bằng nguồn gốc ghi **(chưa kiểm)**.

## Khối điều lệ (lệnh + thực tế)
| Trường | Lệnh | Thực tế |
|---|---|---|
| Loại phiên | Nghiên cứu (tài liệu + tải mẫu nhỏ để kiểm) | đúng |
| Nhánh | `nc-ban-do` từ `origin/main` | đúng (@ `82a17ae`); đẩy `nc-ban-do`, không merge |
| Tệp được sửa | CHỈ `reports/NC-BAN-DO-BAO-CAO.md` + `reports/nc-ban-do/**` ≤ 10 MB | đúng: báo cáo + `reports/nc-ban-do/` **≈ 1,2 MB** (bảng nguồn, giấy phép nguyên văn, 8 mẫu GeoJSON đã cắt, 4 ảnh xem trước, 10 script, chi phí). Không sửa main, `checks/`, `scripts/`, `design/`, `docs/`, nhánh khác. Không ghi RIGHTS/AUTHORSHIP/COST-LEDGER (dòng đề xuất ở §7) |
| Trần | Claude API ≤ $1 (ghim) · YouTube 0 · ElevenLabs 0 · giờ máy ≤ 1 h | **$0** (không gọi) · **0 đv** · **0 ký tự** · **≈ 0,15 h** |
| Preflight | bắt buộc; che email | `verify.sh`: 9 PASS, 4 FAIL không liên quan việc tài liệu (three.js lock, tifffile/pyshp, k2v node_modules, Freesound 403 tuỳ chọn). Hook pre-commit/pre-push cài đầu phiên. Kết quả `tools/preflight.sh` ở §8. Email trong trang gốc (David Rumsey, Newberry) **đã che**; 0 email trong tệp ghi |
| Điều kiện dừng | xong → đẩy → dừng; không dừng hỏi giữa chừng | xong việc. Câu hỏi không chặn đã tự quyết, ghi ở §9 |

---

## 0. Tóm tắt cho chủ dự án (đọc 2 phút)

1. **Có dữ liệu ranh giới lịch sử dùng được cho video kiếm tiền, và đủ cho T3 trước 14/12.** Đã kiểm 12 nguồn (§1). Hai nguồn chính đều phủ đủ 1704, 1782, 1941 ở Tây Âu và cho phép thương mại:
   - **Cliopatria v0.2.1** (Seshat, Zenodo, 03/10/2026): **CC BY 4.0**. Phủ toàn cầu 3400 TCN–2024, theo khoảng năm. Khái quát hoá, các đỉnh cách nhau 20–40 km. Đủ cho khung tầm châu lục. **Riêng năm 1941 có vùng Pháp bị Đức chiếm.**
   - **OpenHistoricalMap (OHM)**: dữ liệu **CC0**, nhưng **nhiều đường thành phần mang `license=CC-BY-4.0`**. Kiểm thật: 201/298 đường của quan hệ "Spain 1704" lấy từ đường địa giới hiện hành của IGN Tây Ban Nha. Vì vậy **bắt buộc ghi công**.
     - Ranh theo **ngày**: quan hệ "Spain" bắt đầu đúng 1704‑08‑04, là ngày Gibraltar đổi chủ. Chi tiết: đỉnh cách nhau 75–560 m.
     - Phủ cả Bắc Mỹ 1704/1754/1782/1800/1861: thuộc địa và lãnh thổ bản địa.
2. **Không dùng lên hình:** historical-basemaps (GPL-3.0, chuỗi quyền mờ, sai rõ), CShapes 2.0 (**NC**-SA), ảnh David Rumsey (**NC**-SA 3.0), GeaCron ("All Rights Reserved"), NHGIS (cấm phân phối lại). **Euratlas** là độc quyền; phải mua giấy phép và hỏi điều khoản video (cửa hàng ngắt kết nối từ container). Mỗi thế kỷ chỉ có 1 bản, không có 1704 và 1782.
3. **Bắc Mỹ 1783–1900:** **Newberry Atlas of Historical County Boundaries** cho phép *"reused for any lawful purpose, commercial or non-commercial"*. Ranh bang/lãnh thổ Mỹ chính xác đến ngày, có trích luật. Lưu ý: tệp zip vẫn kèm bản CC BY-NC-SA 2.5 cũ, và trang tải nói bỏ qua bản này → **lưu ảnh trang làm bằng chứng**. Phần ngoài nước Mỹ (Canada, đế quốc Tây Ban Nha, lãnh thổ bản địa) lấy từ OHM.
4. **Số đo độ chính xác:**
   - Biên Tây Ban Nha–Pháp (Pyrenees) giữa OHM và Cliopatria lệch **trung bình 3,4–3,7 km, tối đa 15,6–16,5 km**.
   - Ở khung rộng 2 500 km (1080p, ≈ 1,3 km/px), độ lệch đó là **≈ 2,7 px trung bình, ≈ 12 px tối đa**.
   - Đủ cho tầm châu lục, kèm nhãn "approx.". **Không đủ cho tầm vùng < 300 km.**
5. **Bẫy đã tìm thấy (đều có số đo hoặc hình):**
   - (a) OHM dùng **đường biên giới Gibraltar hiện đại** (mép bắc 36,155°, gồm cả đất lấn biển và sân bay) cho toàn bộ 1713→nay. Năm 1782 chưa có đường đó: lúc ấy chỉ có chiến tuyến Tây Ban Nha và eo đất trung lập.
   - (b) Polygon "disputed: Gibraltar" của Natural Earth chỉ có **7 đỉnh**, mép bắc 36,141°, **không phủ eo đất**. Vì vậy luật K-R3 (NC-LS2) phải có vùng đệm.
   - (c) OHM 1941 tô **cả nước Pháp là "French State"**, không có vùng chiếm đóng.
   - (d) Cliopatria 1704 có "Pro-Habsburg Spain" phủ cả miền đông Tây Ban Nha và Minorca từ 1702. Như vậy là **sớm hơn lịch sử** (chưa kiểm bằng claim).
   - (e) Minorca đổi chủ: OHM ghi **1782‑01‑05**, Cliopatria ghi **1781**. Mốc phổ biến là đầu hàng ngày 5/2/1782 (chưa có claim T3). Vì vậy **một tấm bản đồ "c. 1782" là sai cho các đoàn tiếp tế 1780 và 1781**.
6. **T3 (§2): đề xuất 3 shot bản đồ chiến lược (20 s, 3,5 % thời lượng) và 4 inset.** Tổng thời lượng không đổi:
   - **SM1 1704**: hạm đội Anh–Hà Lan.
   - **SM2 1779–82**: phong toả, 3 đoàn tiếp tế, hạm đội Pháp–Tây Ban Nha.
   - **SM3 1940–42**: sơ tán dân, Torch.

   **Thiếu claim cho tuyến:** claims T3 hiện chỉ có **điểm tới và ngày tới**, không có cảng đi và hải trình. Cần **≈ 10 claim mới** từ chính các sách đã tải (Sayer, Montero, Drinkwater). **Phương án dự phòng không cần code mới:** dùng `relief/map` hiện có với bờ biển, tuyến và nhãn. Tô thêm ≤ 3 phe (`regions ≤ 3`) từ Cliopatria nếu có.
7. **Luật đề xuất (§3):**
   - Loại cảnh mới `strategic`, **tách khỏi NC-H2 "địa cầu"**: ≤ 15 % thời lượng, mỗi lần ≤ 8 s, luôn có chuyển động (tuyến/mũi tên/hạm đội), luôn có nhãn **"approx. borders c. YYYY — source"**.
   - Inset ≤ 12 % khung, góc trên phải trong vùng an toàn, 2,5–4 s, chỉ bờ biển + điểm + hộp khung máy.
   - Lãnh thổ nhỏ hơn ~8 px vẽ bằng **điểm**, không vẽ polygon (Gibraltar).
   - Không vẽ biên hiện đại đang tranh chấp thành nét liền.
   - Mỗi thực thể giữ một màu suốt tập.
   - Tuyến biển không được cắt qua đất liền. Bản minh hoạ đầu tiên của phiên đã mắc đúng lỗi này, nên K phải đo.
8. **Máy dựng (§5):**
   - **V5b-2c** (ngay sau V5b-2b, trước G1b T3) làm **M13-lite** (bản đồ chiến lược 2D/2.5D trên `relief/map`, DEM ETOPO cho tầm châu lục, raster ranh giới theo phe, tuyến biển có kiểm đất, chú giải, nhãn nguồn) và **M14** (inset). Ước **≈ 1–1,5 h máy thử + 0,4–0,6 h máy/tập (ước)**.
   - **V6**: M13 đầy đủ (chuyển mốc tự động, gạch vùng không chắc, Bắc Mỹ).
9. **Khác đối thủ (§4):** kênh bản đồ trận đánh kể bằng bản đồ 2D phẳng; kênh timelapse thành phố không kể chiến tranh. Mình **nối liền hai tầng**: từ bản đồ chiến lược có ranh đúng năm và nguồn ghi trên hình, **lặn liên tục** xuống thành phố/pháo đài 3D đúng năm, giữ cùng bộ đếm ngày và cùng mặt trời.
10. **Chi phí thật:** Claude API **$0** · YouTube **0** · ElevenLabs **0** · giờ máy **≈ 0,15 h** · mạng ≈ 400 MB (ngoài git) · WebSearch 2.

### Bảng quyết định đề xuất (chờ chủ dự án)
| # | Đề xuất | Ưu | Nhược | Tác động | Rủi ro |
|---|---|---|---|---|---|
| B1 | **Nguồn ranh giới chính:** Cliopatria (CC BY 4.0) cho tầm châu lục + OHM (CC0 + CC BY 4.0) để đối chiếu và lấy ranh theo ngày; Newberry cho Mỹ 1783–1900; Natural Earth (PD) cho bờ biển. **Loại** HB, CShapes, Rumsey, GeaCron, NHGIS; Euratlas chỉ khi mua | cả hai nguồn chính cho thương mại, không share-alike; hai nguồn độc lập để kiểm chéo | ghi công bắt buộc (cả CNIG/IGN cho phần OHM); Cliopatria khái quát 20–40 km | dòng nguồn trên hình + mô tả; 3–4 dòng RIGHTS | sai lịch sử trong nguồn mở (đã thấy 3 lỗi ở §1.3) → luật hai nguồn (B5) |
| B2 | **T3: 3 shot `strategic` (SM1 6 s, SM2 7 s, SM3 7 s) + 4 inset**, thay phần đầu 1a, phần lớn 2f và 4g; tổng thời lượng giữ 9:23,5 | trả lời đúng câu "cuộc chiến đến từ đâu, qua đường nào"; thêm 1 loại cảnh cho Q26b | cần ≈ 10 claim tuyến mới + M13-lite | tiền kỳ thêm 1 gói tra nguồn nhỏ; V5b-2c | nếu claim/M13 trễ → phương án dự phòng (bờ + tuyến + nhãn) trên `relief/map` hiện có |
| B3 | **Loại cảnh mới "bản đồ chiến lược"** vào Kinh thánh §4: ≤ 15 % thời lượng, mỗi lần ≤ 8 s, ≤ 2 lần/chương, bắt buộc chuyển động + nhãn nguồn + mốc thời gian; **không tính vào NC-H2** | lợi thế riêng của series lịch sử; vẫn chặn lỗi T2 "đứng ở địa cầu" | thêm một luật K | K viết luật đo (§3.4) | lạm dụng bản đồ thay cảnh 3D → trần 15 % + ≤ 2/chương |
| B4 | **Inset góc** ≤ 12 % khung, trên phải trong vùng an toàn 5 %, 2,5–4 s, lần đầu mỗi chương máy ≤ 3 km tại nơi có tên hoặc khi nhảy > 300 km | khán giả luôn biết đang ở đâu mà không cần lên địa cầu | thêm lớp chữ/hình ở góc | M14 | che chủ thể/bảng điểm → luật né (LL.occ) |
| B5 | **Luật ranh giới lịch sử** (§3.3): nhãn "approx. borders c. YYYY — source" ≥ 38 px suốt lúc hiện ranh; hai nguồn kiểm chéo, lệch trung bình > 4 px ở khung đầu ra → vẽ mép mềm/gạch; lãnh thổ < 8 px → điểm; không vẽ biên hiện đại tranh chấp thành nét liền (vùng đệm 10 km quanh NE "disputed"); đổi chủ giữa shot thì đổi đúng ngày có claim | chặn cả 5 bẫy đã thấy | công chuẩn hoá dữ liệu mỗi tập (ước 1–2 h) | K-R3 mở rộng + K mới | — |
| B6 | **Màu phe cố định theo thực thể** (không theo ý thức hệ), không dùng cờ làm màu tô, dân thường màu trung tính; bảng màu T3 §3.3 | đúng Kinh thánh §4 "mã màu cố định"; tránh biểu tượng (K-R2) | cần khoá bảng màu cho cả series | AUTHORSHIP (quyết định sáng tạo) | — |
| B7 | **Máy dựng:** V5b-2c = M13-lite + M14 (sau V5b-2b, trước G1b T3); V6 = M13 đầy đủ | không làm chậm P0 của V5b-2b; kịp 14/12 | thêm một phiên V | ≈ 1–1,5 h máy thử (ước) | V5b-2b trễ → V5b-2c dồn; dự phòng B2 |
| B8 | **Bắc Mỹ: lãnh thổ bản địa** vẽ như thực thể có tên khi nguồn có (OHM có), **không** để trắng như "đất trống" | đúng sử liệu; tránh lỗi "terra nullius" mà khán giả hay chỉ trích | thêm nhãn; nguồn ranh bản địa thường rất ước lượng | áp cho tập Bắc Mỹ (Boston, Vicksburg) | chọn tên/ranh nhạy cảm → nhãn "approx." + mô tả |

**Chỉ số trong ±5 % quanh ngưỡng (nêu tên):**
- **Inset minh hoạ 11,9 %** so trần đề xuất 12 %: −0,9 %. Đây là khung minh hoạ, chưa phải luật; M14 nên nhắm ≤ 11 % để có dư.
- **Lệch diện tích Tây Ban Nha OHM ↔ Cliopatria năm 1704 = 5,0 %** (1782: 3,2 %; 1941: 3,1 %). Không có ngưỡng; nêu vì số tròn đúng 5 % dễ bị đọc nhầm là ngưỡng. Phần lệch 1704 do Cliopatria tách "Pro-Habsburg Spain".
- Các ngưỡng đề xuất khác (thời lượng 3,5 % so 15 %; shot 6–7 s so 8 s; lệch trung bình 2,7 px so 4 px) đều ngoài ±5 %.

**Việc chờ chủ dự án:** §10.

---

## 1. Nguồn ranh giới lịch sử (12 nguồn đã kiểm)

### 1.1 Bảng nguồn
Máy đọc: `reports/nc-ban-do/nguon.json`. Giấy phép nguyên văn + SHA: `reports/nc-ban-do/giay-phep/GIAY-PHEP-NGUYEN-VAN.md`.

| # | Nguồn | Giấy phép (đọc nguyên văn) | Thương mại / phái sinh / ghi công / share-alike cho video | Phủ (ưu tiên: Tây Âu–ĐTH 1300–1950, Bắc Mỹ 1700–1900) | Độ chính xác (tự đo hoặc nguồn tự nêu) | Định dạng | Dùng được? |
|---|---|---|---|---|---|---|---|
| 1 | **OpenHistoricalMap** | "dedicated to the public domain under a Creative Commons CC0 dedication"; một số phần tử "Creative Commons Attribution (CC BY) or … (CC BY-SA), as noted in license=* tags" | Có / có / **bắt buộc cho phần CC BY** (đã thấy CNIG/IGN, LSIB) / chỉ khi dùng "significant portion" phần BY-SA (0 đường BY-SA trong 3 quan hệ kiểm) | Toàn cầu, **theo ngày**. Tây Âu 1704/1782/1941 đủ; Bắc Mỹ có thuộc địa + lãnh thổ bản địa từ 1704 | Đỉnh cách 75–560 m; ranh ghép từ **đường hiện đại** (CNIG LILIM, LSIB) + bản đồ cũ (Cassini, bản đồ Flanders); polygon **gồm vùng biển 3 hải lý**; Gibraltar dùng ranh hiện đại cho 1713→nay; 1941 thiếu vùng chiếm đóng | OSM JSON/XML (API, Overpass), vector tiles | **CÓ** (đối chiếu + ranh theo ngày; ghi công CC BY) |
| 2 | **Cliopatria v0.2.1** (Seshat) | Zenodo: `"license": {"id": "cc-by-4.0"}`; README: "these maps reflect only one version of the territory held by past polities" | Có / có / **bắt buộc** / không | Toàn cầu 3400 TCN–2024, khoảng năm; 13 797 bản ghi; Tây Âu 1704/1782/1941 đủ; 1941 có vùng Đức chiếm | Đỉnh cách 20–40 km (khái quát); 3 điểm nghi sai thời điểm/tên (§1.3) | GeoJSON (zip 46 MB) | **CÓ** (chính cho tầm châu lục) |
| 3 | historical-basemaps (aourednik) | **GPL-3.0**; "work in progress: verify the maps …"; nguồn "collected … sometimes only available through the wayback machine … ThinkQuest" | Có về chữ / có, nhưng copyleft; video chỉ bị phủ nếu "constitutes a covered work" (mơ hồ) / giữ thông báo GPL / copyleft | Ảnh chụp năm cố định: 1700, 1715, 1783, 1800, 1815…1938, 1945 (không có 1704/1782/1941) | Đỉnh cách 15–25 km; **Spain giống hệt nhau ở 1700 và 1715** (cùng polygon); Minorca, Gibraltar không thuộc polygon nào; `BORDERPRECISION=3` ("international law") cho gần như mọi vùng 1700; "Lombardy" 1783 có `SUBJECTO=3` (lỗi trường); Sardinia 1700 ghi thuộc "Austrian Empire" | GeoJSON, SVG | **KHÔNG** lên hình (chuỗi quyền + lỗi); chỉ tham khảo |
| 4 | CShapes 2.0 / CShapes-Europe (ETH ICR) | "licensed under a Creative Commons Attribution-**NonCommercial**-ShareAlike 4.0" | **Không** (NC) | Thế giới 1886–2019; châu Âu từ 1816 | Học thuật, mã hoá theo Territorial Change Dataset (theo trang) | Shapefile, GeoJSON, gói R | **KHÔNG** (kênh kiếm tiền); chỉ để kiểm chéo nội bộ |
| 5 | Euratlas (Nüssli) | "Toute autre utilisation d'éléments des sites Euratlas, est interdite" | Chỉ khi mua giấy phép riêng; điều khoản GIS **chưa đọc được** (cửa hàng ngắt kết nối) | Châu Âu, **1 bản/thế kỷ** (1 → 2000); không có 1704/1782 | Có lớp "uncertain borders" (thư viện Duke, qua WebSearch, chưa đọc trang gốc) | Shapefile (bán) | **CHƯA** — cần chủ dự án hỏi giá + điều khoản video |
| 6 | GeaCron | "Copyright © 2011 - geacron.com - All Rights Reserved"; trang rao "Exclusive Sale Offer €450,000 … proprietary database" | Chỉ qua thoả thuận | Thế giới theo năm, có tuyến | Không công bố nguồn từng ranh | Web app; vector chỉ khi mua | **KHÔNG** |
| 7 | **Newberry AHCB** | "reused for any lawful purpose, commercial or non-commercial, without licensing or permission fees … some files may contain the original, out-of-date copyright license; these can be ignored" | Có / có / nên ghi / không | Mỹ: bang + lãnh thổ **1783–2000 theo ngày**; hạt từ 1629 | Học thuật, có trích luật mỗi thay đổi; bản Gen01 khái quát 0,01° | Shapefile, KMZ | **CÓ** (Mỹ); lưu ảnh trang Download làm bằng chứng vì zip còn kèm CC BY-NC-SA 2.5 |
| 8 | IPUMS NHGIS | "You will not redistribute the data without permission" | Phải xin phép | Mỹ 1790–nay | Cao | Shapefile | **KHÔNG cần** (Newberry thay được) |
| 9 | **Natural Earth** | "in the public domain. You may use the maps in any manner" | Có / có / không bắt buộc / không | Hiện đại; bờ biển, đất, sông; lớp "disputed areas" | 1:10m–1:110m; **Gibraltar "disputed" 7 đỉnh, mép bắc 36,141°** (không phủ eo đất) | Shapefile, GeoJSON | **CÓ** (bờ biển nền; kiểm tranh chấp có đệm) |
| 10 | Bản đồ PD để tự số hoá: **LoC, Rijksmuseum** | LoC: "Rights Advisory" từng item (luật repo §6.7); Rijks: "Public Domain or … CC0 … In some cases … CC BY 4.0" | Có (theo từng item) | Bản đồ châu Âu/thế giới đương thời | Hình chiếu cổ, sai số có thể tới hàng chục–trăm km ở tầm châu lục (ước); ranh theo quan điểm người vẽ | Ảnh TIFF/JPG | **CÓ** làm "hồ sơ thật" hoặc kiểm chéo; **không** tự số hoá ranh châu lục cho T3 (công lớn, kém chính xác hơn nguồn 1–2) |
| 11 | David Rumsey Map Collection | "may be reproduced or transmitted, but not for commercial use … licensed under a Creative Commons License" → liên kết `by-nc-sa/3.0` | **Không** (NC-SA; thương mại phải xin) | Rất rộng | như #10 | Ảnh | **KHÔNG** dùng ảnh Rumsey; tìm cùng bản in ở LoC/Rijks/Commons PD |
| 12 | Atlas Pi | "Apache-2.0 licensed" (chỉ **mã**) | Giấy phép **dữ liệu** không nêu | 1 038 thực thể 4500 TCN–2024 | "per-record confidence scores" (theo README HB) | REST, GeoJSON | **CHƯA** |

Ngoài bảng:
- Thư viện Harvard Dataverse: tìm theo API (3 truy vấn) không ra bộ ranh giới nhà nước châu Âu 1500–1800 có giấy phép mở.
- Bộ Abramson (nhà nước châu Âu 1100–1790) không tìm thấy bản phân phối công khai.
- Các bản Euratlas trên Stanford/Duke chỉ cấp cho thành viên trường.

### 1.2 Share-alike có áp cho "produced work" (video) không — kết luận vận hành
- **CC BY-SA 4.0** định nghĩa "Adapted Material" là tài liệu "translated, altered, arranged, transformed, or otherwise modified". Riêng nhạc thì luôn là phái sinh khi đồng bộ với hình động.
  - Bản đồ được tô màu, cắt, chiếu lại rồi dựng vào video **rất có thể là "altered/transformed"**. Khi đó share-alike buộc phát hành phần phái sinh theo BY-SA, và mâu thuẫn với việc bán phim.
  - **Luật đề xuất:** không dùng dữ liệu/ảnh BY-SA cho bản đồ đã biến đổi. OHM: lọc bỏ phần tử `license=CC-BY-SA*` khi chuẩn hoá (3 quan hệ đã kiểm có 0 phần tử như vậy).
- **GPL-3.0** (historical-basemaps): *"The output from running a covered work is covered by this License only if the output, given its content, constitutes a covered work."* Video dựng từ dữ liệu GPL nằm ở vùng mơ hồ. Kèm chuỗi quyền (ThinkQuest, wayback) không rõ, nên **không dùng**.
- **NC** (CShapes, Rumsey): kênh có kiếm tiền + bán phim = thương mại → **không dùng**.
- **CC BY 4.0** (Cliopatria, phần OHM): dùng được. **Ghi công ở dòng nguồn ngắn trên hình + mô tả.**

### 1.3 Kiểm mẫu thật (Iberia–Pháp–Anh, bbox −10,5…4,5 / 35,5…52)
Mẫu đã cắt ở `reports/nc-ban-do/mau/`; ghi công ở `mau/ATTRIBUTION.md`. Ảnh so: `reports/nc-ban-do/so-3-nguon-1704-1782-1941.png`.

| Đo | OHM | Cliopatria | historical-basemaps |
|---|---|---|---|
| Thực thể cắt được 1704 / 1782 / 1941 | 9 / 10 / 9 (quan hệ hiệu lực đúng năm) | 10 / 10 / 9 | 8 (tệp 1700) / 9 (1783) / 10 (1938) |
| Khoảng cách đỉnh (Tây Ban Nha) | 87–146 m | 27–36 km | 15–25 km |
| Gibraltar thuộc polygon nào (điểm −5,35; 36,14) | 1704: không (đúng: không có quan hệ Anh 1704–13) · 1782, 1941: "Gibraltar" | không (quá nhỏ) | không |
| Minorca | Anh tới 1781, Tây Ban Nha từ **1782‑01‑05** | Anh tới 1780, Tây Ban Nha từ **1781** | 1783: **không thuộc ai** |
| 1941 Pháp | **cả nước = "French State"**; chỉ có "Military Administration in Belgium and Northern France" | có "Nazi Germany" phủ vùng chiếm đóng + "Vichy France" | không có (tệp 1938) |
| Lỗi/nghi sai thấy được | Gibraltar 1713→nay dùng ranh hiện đại (gồm sân bay, cảng); polygon gồm vùng biển 3 hải lý | "Pro-Habsburg Spain" 1702–1705 gồm miền đông + Minorca (chưa kiểm); 1941 tên "Kingdom of Great Britain"; Tangier "International Zone" 1912–1955 liền (năm 1940–45 Tây Ban Nha chiếm đóng — **chưa có claim**) | Spain 1700 = 1715 (cùng hình); Sardinia 1700 "Austrian Empire"; trường lỗi "Lombardy" |

**Độ khớp hai nguồn chính (OHM ↔ Cliopatria; chiếu EPSG:3035; cắt theo đất Natural Earth 1:50m):**

| Năm | Lệch diện tích TBN | Biên Pyrenees: Hausdorff / trung bình | Lệch diện tích BĐN |
|---|---|---|---|
| 1704 | 5,0 % | 15,6 km / 3,5 km | 4,1 % |
| 1782 | 3,2 % | 15,6 km / 3,4 km | 4,1 % |
| 1941 | 3,1 % | 16,5 km / 3,7 km | 3,8 % |

Đổi ra điểm ảnh 1080p:

| Bề ngang khung | km/px | Lệch trung bình | Lệch tối đa |
|---|---|---|---|
| 2 500 km (bán đảo + Pháp) | 1,3 | ≈ 2,7 px | ≈ 12 px |
| 1 000 km (tầm vùng) | 0,52 | ≈ 6,7 px | ≈ 30 px |

→ Hai nguồn **đủ cho khung ≥ ~1 500 km**. Hẹp hơn thì phải vẽ mép mềm hoặc dùng bản đồ thời kỳ phẳng (`bản đồ lịch sử` hiện có).

**Eo đất Gibraltar** (`reports/nc-ban-do/gibraltar-eo-dat-ohm-vs-ne.png`):
- Polygon OHM "Gibraltar" (1713→nay) có mép bắc **36,155°**, tức đường rào hiện đại, gồm đất lấn biển và sân bay.
- Polygon "Spain" của OHM có một **cạnh thẳng kẻ ngang vịnh** ở 36,155° (mép vùng đệm biển).
- Natural Earth "disputed: Gibraltar" có 7 đỉnh, mép bắc 36,141°.

→ Không nguồn nào vẽ đúng tình trạng 1704–1909 (chiến tuyến 1730–35, eo đất trung lập; S032, S035). **Ở tầm châu lục, Gibraltar chỉ rộng ≈ 4 px, vẽ bằng điểm là đúng và đủ.**

**Bắc Mỹ (kiểm nhanh):**
- OHM có các thực thể cấp 2 năm 1704 (vd. Nouvelle-France, Nueva España, Province of Carolina, Rupert's Land), 1754, 1782 (United States, Province of Quebec, East/West Florida, Nʉmʉnʉʉ Sookobitʉ), 1800 và 1861 (Confederate States).
- Newberry: mẫu 1783‑09‑03 (15 thực thể) và 1803‑05‑01 (22 thực thể, gồm Louisiana Purchase) ở `mau/`.

### 1.4 Định dạng và cách lấy (cho phiên máy dựng)
- **Cliopatria:** một tệp GeoJSON (`FromYear`/`ToYear`/`Name`/`Wikidata`). Lọc theo năm → cắt bbox → cắt theo đất Natural Earth → đơn giản hoá theo km/px của khung.
- **OHM:**
  - Overpass `overpass-api.openhistoricalmap.org`, `rel[boundary=administrative][admin_level=2](bbox)` → lọc `start_date ≤ ngày < end_date` → `rel(id…); out geom;` → ghép polygon (`py/ohm_build.py`).
  - Ghi lại `license`/`source` của từng đường (`way(r); out tags;`) để lập dòng ghi công.
  - 3 truy vấn tải ≈ 47 MB.
- **Newberry:** shapefile, lọc `START_DATE ≤ ngày ≤ END_DATE`.
- **SHA của tệp đã tải** (ngoài git, `~/.cache/nc-bd/`):

| Tệp | SHA-256 |
|---|---|
| `cliopatria.geojson.zip` | `e10a4e42…eed4` |
| `US_AtlasHCB_StateTerr_Gen01.zip` | `db6f124d…c457` |
| `ohm-1704.json` | `1b5f59ec…f9826b` |
| `ohm-1782.json` | `e2a8f57c…c484` |
| `ohm-1941.json` | `1da63045…e9` |
| `hb_world_1700/1783/1938` | `eb73d6b0…`, `7cfa9241…`, `f2565926…` |

---

## 2. Phương án cho T3 (kịp 14/12)

### 2.1 Ranh giới từng mốc
| Mốc | Nguồn chính | Kiểm chéo | Cần chỉnh/số hoá thêm | Công (ước) |
|---|---|---|---|---|
| **~1704** (8/1704) | **OHM** (Spain bắt đầu 1704‑08‑04, France 1697–1714, England 1660–1707, Portugal, Dutch Republic, HRE) | Cliopatria 1702–1705 | Bỏ tách "Pro-Habsburg Spain" của Cliopatria (sai thời điểm). Không tô phe trong lòng Tây Ban Nha: Tây Ban Nha là một thực thể "Spain (Philip V)". Gibraltar = điểm + nhãn "taken in the name of 'Charles III'" (S012; S017 là MÂU THUẪN, chỉ dùng phần đã xác minh). Liên minh (Anh, Hà Lan, Bồ Đào Nha từ 1703, Áo ↔ Pháp, Tây Ban Nha) cần **claim mới** | 0,5 h máy+phiên |
| **~1782** | **Cliopatria** (khái quát vừa tầm châu lục) | OHM theo ngày | **Minorca đổi màu đúng ngày có claim** (OHM 1782‑01‑05 ↔ mốc phổ biến 5/2/1782; cần claim). Đoàn 1780, 1781 phải dùng trạng thái Minorca = Anh. Gibraltar = điểm | 0,5 h |
| **~1941** | **Cliopatria** (có vùng chiếm đóng) | OHM (thiếu vùng chiếm đóng → chỉ kiểm phần Tây Ban Nha/Bồ Đào Nha) | Gọi đúng tên: "German-occupied France" (không tô theo biểu tượng chế độ); "Vichy France"; "Spain (non-belligerent)" cần claim. **Tangier 1940–45** do Tây Ban Nha chiếm, khác với Cliopatria "International Zone" → cần claim, rồi sửa tay | 0,5–1 h |
| Bờ biển nền mọi mốc | Natural Earth 1:10m/1:50m (PD) | — | Đất lấn biển (đường băng 1941–43) không hiện ở tầm châu lục → không cần | 0 |

Tổng ≈ 1,5–2 h phiên chuẩn hoá (ước). Đây là việc dữ liệu cho V5b-2c hoặc tiền kỳ, **không phải công số hoá tay**.

### 2.2 Tuyến cần vẽ — toạ độ lấy từ claim nào
Claims T3 hiện có **ngày đến và điểm đến**, chưa có **cảng đi/hải trình**:

| Tuyến | Shot | Claim đã có (điểm/ngày) | Thiếu (claim mới, nguồn gợi ý đã tải ở tiền kỳ T3) | Cách vẽ khi chỉ có điểm mốc |
|---|---|---|---|---|
| Hạm đội Anh–Hà Lan 1704 | SM1, 1a | S012 (thả neo vịnh 21/7 O.S. = 1/8 N.S.), S013 | điểm xuất phát, hành trình 5–7/1704 (Sayer 1862, Montero 1860) | qua đúng các điểm có claim; đoạn giữa là spline trên biển, nhãn "route approx." |
| Phong toả biển 1779 | SM2, 2c | S042 (16/7/1779), S048 | căn cứ hải đội Tây Ban Nha (Algeciras), vị trí tuần tra (Drinkwater) | vòng phong toả quanh vịnh, không cần hải trình |
| Đoàn tiếp tế 1 (Rodney, 1/1780) | SM2, 2f | S054: bắt đoàn Caracas ngày 8/1/1780 "off the coast of Portugal"; trận ánh trăng 16/1; tới Gibraltar ~18/1; 21 tàu chiến tuyến | cảng đi + ngày đi; vị trí trận 16/1 (mũi St Vincent, cần claim) | Anh → ngoài khơi Bồ Đào Nha → St Vincent → eo biển |
| Đoàn 2 (Darby, 4/1781) | SM2, 2f, 2g | S055 (thấy 12/4/1781), S062 (thả neo 10:45) | cảng đi + ngày đi | Anh → eo biển (đường biển, không cắt Iberia) |
| Đoàn 3 (Howe, 10/1782) | SM2, 2f | S056 (11/10/1782: 34 tàu chiến tuyến, 31 tàu vận tải; phần lớn bị cuốn vào Địa Trung Hải; đổ bộ 18/10) | cảng đi + ngày đi; trận Cape Spartel 20/10/1782 (cần claim) | Anh → eo → **trôi vào Địa Trung Hải** → quay lại (đúng S056) |
| Hạm đội Pháp–Tây Ban Nha 1782 | SM2, 2k, 2m | S065–S068 (pin nổi, 47 tàu chiến tuyến — 2k) | nơi tập kết (Cádiz → Algeciras), ngày (cần claim) | mũi tên ngắn Cádiz → vịnh |
| Sơ tán dân 1940 | SM3, 4g | S114 (Ma-rốc thuộc Pháp từ 22/5/1940 → trở về → London, Jamaica, Madeira), S117, S118, S120 | không cần hải trình: vẽ **điểm đến + cung trung tính**; Jamaica ngoài khung → mũi tên ra mép khung + nhãn "to Jamaica" | cung, màu trung tính (dân thường, NC-LS M1) |
| Torch 11/1942 | SM3, 4i | S122, S123 (650 máy bay đêm 7–8/11/1942) | điểm đổ bộ Bắc Phi (cần claim) | mũi tên từ Gibraltar → bờ Bắc Phi |
| Đường bay/tàu 1940s khác | — | không có claim | — | **không vẽ** cho tới khi có claim |

→ **Một gói tra nguồn nhỏ ≈ 10 claim** (đề xuất 1 subagent Sonnet, trần ~50–80 nghìn token, theo BAI-HOC-LL #14, #31: P lọc trước, chỉ giao đoạn trích). Hầu hết nguồn đã có tệp và SHA ở tiền kỳ T3.

### 2.3 Chỗ đặt trong bảng shot T3 (đề xuất; P sửa `treatment.json`, phiên này không sửa)
| Mới | Thay | Thời lượng | Nội dung |
|---|---|---|---|
| **SM1** (đầu Ch.1) | 6 s đầu của 1a (1a 11 → 5 s) | 6 s | Tây Âu c. 1704: Pháp, Tây Ban Nha (Philip V) ↔ Anh, Hà Lan, Bồ Đào Nha (màu phe); tuyến hạm đội vào eo biển; bộ đếm "1 Aug 1704 (N.S.)" → hoà vào 1a (3D vịnh) |
| **SM2** (giữa Ch.2) | 2f (11 → 4 s, giữ 3D eo biển cho chanh Malaga) | 7 s | c. 1780–82: vòng phong toả; 3 đoàn tiếp tế vẽ lần lượt (≈ 2 s mỗi đoàn) theo bộ đếm ngày; Minorca đổi màu đúng ngày; Cádiz → vịnh |
| **SM3** (Ch.4) | 4g (9 → 2 s) | 7 s | c. 1941: Vichy, vùng chiếm đóng, Tây Ban Nha, Ma-rốc; cung sơ tán (trung tính) + mũi tên Torch 1942 |
| **Inset ×4** (đè lên 3D, không thêm thời lượng) | — | 3 s mỗi lần | 1d (phố 1704), 2a (chiến tuyến 1779), 3d (La Línea), 5d (La Línea 2026) |

- **Tổng `strategic` = 20 s = 3,5 % của 563,5 s.**
- Hai cảnh 3D (2f, 4g) ở AGL 5–45 km rút ngắn → NC-H3 (≥ 70 % 3D ở ≤ 60 km) càng dễ đạt. Phần 3D giảm 20 s → P chạy lại `tu_kiem.py`.
- 0c (địa cầu 3 s) giữ nguyên.

### 2.4 Phương án dự phòng (nếu M13-lite hoặc claim tuyến không kịp)
1. **Bờ biển + tuyến + nhãn, không ranh giới:** dùng `relief/map` hiện có.
   - `routes` có `draw`/`flow`/`trail`, `walkers` dùng sticker tàu buồm, `rings`, bảng màu SEPIA, nhãn neo.
   - Dữ liệu: bờ biển Natural Earth (`--coast`).
   - DEM: SRTM 1″ `--dem skadi` (đã có, ≤ 60°N) hoặc dựng phẳng.
   - Không cần code mới; chỉ cần đặc tả.
2. **Tô ≤ 3 phe** bằng `regions` (đã có, giới hạn 3: Anh, Tây Ban Nha, Pháp năm 1782) từ polygon Cliopatria → gần đúng bản đồ chiến lược mà không cần M13.
3. Nếu thiếu claim cảng đi: chỉ vẽ **đoạn cuối có claim** (ngoài khơi Bồ Đào Nha → eo biển), mũi tên vào từ mép khung, nhãn "from England".

---

## 3. Luật thiết kế đề xuất (cho Kinh thánh §4 + K; phiên này không sửa `docs/`, `checks/`)

### 3.1 (a) Loại cảnh mới "bản đồ chiến lược" (`type: strategic`)
- **Là gì:** bản đồ 2D hoặc 2.5D nhìn gần thẳng xuống (nghiêng ≤ 30°), bề ngang khung **≈ 300–5 000 km**, nền bờ biển + địa hình nhẹ, bảng màu SEPIA (quá khứ) hoặc TỰ NHIÊN (hiện tại), **ranh giới đúng thời kỳ** + **thông tin chuyển động** (tuyến, mũi tên, hạm đội, mặt trận, vòng phong toả).
- **Tách khỏi NC-H2 "địa cầu".**
  - NC-H2 nhắm lỗi T2: máy đứng ở 18–30 bán kính Trái Đất mà không kể gì.
  - `strategic` là phẳng/2.5D, có nội dung chuyển động, nên không tính vào NC-H2.
  - NC-H2 vẫn áp cho `map/globe` và mọi cảnh 3D (AGL > 50 km).
- **Trần đề xuất:**
  - ≤ **15 %** thời lượng tập; inset không tính.
  - Mỗi lần ≤ **8 s**.
  - ≤ **2 lần/chương**.
  - Không hai shot `strategic` liền nhau.
- **Bắt buộc:**
  - (1) Có ít nhất một phần tử chuyển động bắt đầu trong ≤ 1,5 s đầu và chạy ≥ 60 % thời lượng shot.
  - (2) Có nhãn mốc thời gian (năm hoặc bộ đếm ngày M6).
  - (3) Có dòng nguồn ranh giới (3.3).
  - (4) Chú giải ≤ 3 phe.
  - (5) Shot trước hoặc sau trong cùng chương là cảnh 3D tại nơi được chỉ tới. Ưu tiên chuyển bằng hoà/zoom nhiều tầng F4: "từ đâu → tới đâu → nơi ấy trông thế nào".
- **Không dùng** cho: thay thế cảnh thành phố (NC-H1 vẫn áp); minh hoạ không có chuyển động; diễn biến chiến thuật chi tiết (đội hình, M2 thuộc V6).

### 3.2 (b) Inset định vị ở góc
- **Cỡ và vị trí:**
  - ≤ **12 %** diện tích khung (khuyến nghị ≤ 11 %).
  - Góc **trên phải**, nằm trong vùng an toàn 5 %.
  - Nếu góc đó đang có huy hiệu bảng điểm thì chuyển sang trên trái.
  - Không trùng dải chú thích/dòng nguồn ở đáy và hộp nhãn (`LL.occ`).
  - Khung minh hoạ: `reports/nc-ban-do/minh-hoa-inset-goc.png` (11,9 %).
- **Khi nào hiện:**
  - Lần đầu mỗi chương máy ở AGL ≤ 3 km tại nơi có tên.
  - Hoặc khi nơi của shot cách nơi của shot trước > 300 km.
  - **Không** hiện trong cú liên hoàn, thẻ số, ảnh/văn bản lưu trữ, hoặc 2 s đầu sau cắt cứng.
- **Bao lâu:** 2,5–4 s, hiện/ẩn bằng mờ dần 0,3 s.
- **Nội dung:**
  - Bờ biển cùng bảng màu với shot, 1–2 nhãn (nơi + vùng/nước).
  - **Hộp đỏ = dấu chân khung máy trên mặt đất** (tính từ campath), có thể chạy theo máy.
  - Không vẽ ranh giới; ranh và nguồn để ở shot `strategic`. Chỉ ghi nguồn ngắn "Map: Natural Earth".
- **Đo:** bbox inset ≤ 12 %, nằm trong vùng an toàn, thời lượng 2,5–4 s, không giao hộp chữ khác.

### 3.3 (c) Ranh giới lịch sử
1. **Nhãn bắt buộc** trong suốt thời gian ranh giới hiện: `approx. borders c. YYYY — <nguồn ngắn>`.
   - Ví dụ: "approx. borders c. 1782 — Cliopatria (Seshat)"; "… — OpenHistoricalMap, IGN".
   - Cỡ ≥ 38 px (SRCPX 16:9), góc dưới trái, không xuống dòng.
   - Nguồn đầy đủ + giấy phép ở mô tả.
2. **Hai nguồn kiểm chéo:** mỗi ảnh chụp ranh giới có một nguồn chính và một nguồn đối chiếu.
   - Đo **lệch trung bình** của đường biên ở thang khung đầu ra.
   - **> 4 px** → vẽ mép mềm (gradient 8–12 px) hoặc gạch chéo, kèm nhãn "border uncertain".
   - Số đo §1.3: Pyrenees 2,7 px ở khung 2 500 km → nét liền được.
3. **Lãnh thổ nhỏ hơn ~8 px** ở khung đầu ra vẽ bằng **điểm** (vòng tròn viền trắng) + tên, **không vẽ polygon**. Ví dụ Gibraltar ≈ 4 px ở khung 2 500 km.
4. **Biên hiện đại đang tranh chấp:**
   - Không vẽ thành nét liền.
   - Kiểm hình học bằng lớp Natural Earth "breakaway & disputed areas" **+ vùng đệm 10 km**, vì polygon Gibraltar của Natural Earth không phủ eo đất. Đây là bản mở rộng K-R3 của NC-LS2.
   - Với eo đất Gibraltar ở tầm vùng: giữ cách làm T3 (1i, 5f): **không vẽ biên giới trên eo đất**, tô theo số liệu, nhãn hai lập trường.
5. **Vùng tranh chấp hoặc không rõ trong quá khứ** (vd. kế vị Tây Ban Nha 1704):
   - Gạch chéo hai màu phe, kèm nhãn "contested".
   - Không chia lãnh thổ theo nguồn khi nguồn tự mâu thuẫn (Cliopatria "Pro-Habsburg Spain" 1702–1705).
6. **Đổi chủ giữa shot:** đổi màu đúng ngày có claim (Minorca), bộ đếm ngày hiện cùng lúc.
   - Ranh của **một** tấm "c. YYYY" chỉ dùng trong ±1 năm quanh sự kiện **và** khi không có thay đổi ở vùng đang nói.
7. **Màu phe:**
   - **Cố định theo thực thể trong cả tập.** Đề xuất cho cả series để khán giả học dần: Anh `#b03a2e` (đỏ gạch), Tây Ban Nha `#c9a227` (vàng đất), Pháp `#2e5c8a` (xanh lam), bên không tham chiến `#a89f8a` (xám nâu), dân thường trắng/kem trung tính.
   - Không dùng cờ làm màu tô.
   - Không dùng bảng màu gắn với biểu tượng chế độ (1941: vùng chiếm đóng tô xám nâu gạch chéo, nhãn chữ).
   - Kiểm mù màu: ΔE giữa hai phe ≥ 20 dưới mô phỏng deuteranopia (đề xuất, chưa đo).
8. **Lãnh thổ bản địa (Bắc Mỹ):** vẽ như thực thể có tên khi nguồn có. Không để trắng như "đất trống" (B8).
9. **Tuyến biển không cắt đất liền.** Spline qua các điểm có claim. Đoạn giữa hai điểm có claim ghi "route approx.".
   - Bài học của chính phiên: khung minh hoạ đầu tiên vẽ cung từ eo Manche tới Gibraltar **cắt ngang Tây Ban Nha**. Đã sửa ở `minh-hoa-ban-do-chien-luoc-1782.png`.

### 3.4 (d) Cách đo cho K (đề xuất; K viết, khoá SHA)
| Mã đề xuất | Luật | Đo bằng | Ngưỡng |
|---|---|---|---|
| **BD-1** Tỷ trọng | tổng `type: strategic` / thời lượng tập; mỗi shot; số/chương | manifest shot (`episode.yaml` / `treatment.json`) | ≤ 15 %; ≤ 8 s; ≤ 2/chương; không liền nhau |
| **BD-2** Chuyển động | mỗi shot `strategic` có ≥ 1 phần tử `route/arrow/fleet/front` với `draw`/`walk` bắt đầu ≤ 1,5 s, phủ ≥ 60 % thời lượng | đặc tả + `rhythm.py` (mốc biến cố) | đủ |
| **BD-3** Nhãn ranh giới | có lớp ranh → có chữ khớp regex `^approx\. borders c\. \d{3,4} — .+` ≥ 38 px, hiện ≥ 95 % số khung có ranh | log chữ (`k2.js`) | 100 % shot |
| **BD-4** Manifest lớp ranh | mỗi lớp `loai: bien_gioi_lich_su` có `nam`, `nguon`, `nguon_doi_chieu`, `lech_tb_px`, `giay_phep` ∈ {CC0, PD, CC-BY-4.0}; `lech_tb_px > 4` → `kieu_mep ∈ {mem, gach}` | manifest + script đo lệch (`py/cmp.py` tổng quát hoá) | 0 vi phạm |
| **BD-5** Tranh chấp hiện đại (K-R3 mở rộng) | lớp `bien_gioi_hien_dai` ∩ (NE disputed ⊕ 10 km) = ∅; lãnh thổ < 8 px phải là điểm | phép giao hình học + log | 0 giao |
| **BD-6** Tuyến biển | tuyến `mode: sea` ∩ đất (NE 1:10m, trừ đệm 5 km quanh cảng) = ∅; mỗi tuyến có ≥ 1 claim id | đặc tả + hình học | 0 |
| **BD-7** Màu phe | cùng `faction_id` → cùng mã màu trong cả tập; không thẻ `co`/`bieu_tuong` làm fill (K-R2) | manifest | đúng |
| **BD-8** Inset | bbox ≤ 12 % khung, trong vùng an toàn 5 %, 2,5–4 s, không giao `LL.occ`, không trong shot liên hoàn | log 2D | 0 vi phạm |

---

## 4. So đối thủ (mô tả bằng lời, không chép hình)
Mô tả dựa trên hiểu biết chung về các kênh và bảng hình thức NC-LS §1.2/§1.4. **Phiên này không xem video** (YouTube 0 đơn vị); không chép khung, thumbnail, câu chữ.

| Kênh | Cách làm bản đồ chiến lược (tóm tắt) | Mạnh | Không có |
|---|---|---|---|
| Kings and Generals | Bản đồ 2D có vân giấy/địa hình vẽ; quân là khối/biểu tượng di chuyển, mũi tên tiến quân; máy trượt và zoom trên bản đồ; xen tranh minh hoạ | Nhịp đều, rõ phe, nhiều tập | Nơi chốn 3D đúng năm; ranh có nguồn trên hình |
| Epic History | Bản đồ chiến dịch sạch, mũi tên kèm ngày; gần đây có loạt "in 3D" dựng địa hình chiến trường | Rõ ràng, có chuẩn chiến dịch dài | Thành phố/pháo đài đổi theo năm; nguồn từng mốc (1/10 mô tả có nguồn, NC-LS) |
| EmperorTigerstar, Ollie Bye, History on Maps | Bản đồ phẳng cả châu lục/thế giới; tô màu quốc gia đổi theo năm hoặc ngày, bộ đếm thời gian; ít hoặc không lời | Cảm giác "toàn cảnh thời gian" | Câu chuyện nhân vật; tầng gần mặt đất |
| The Operations Room | Nền ảnh vệ tinh/3D, ký hiệu quân sự chiến thuật | Chính xác chiến thuật hiện đại | Thời kỳ trước 1900; nơi chốn đúng năm |
| Timelapse thành phố (Latos, Restored Timeline, Matt Reconstructs) | Thành phố mọc theo thời gian; nhiều kênh dùng ảnh AI | Cảm xúc "nơi chốn đổi" | Chiến lược/ranh giới; lỗi thời đại (NC-LS §1) |

**Mình khác ở đâu (ba điểm):**
1. **Một đường máy liền hai tầng.** Bản đồ chiến lược có ranh đúng năm, tuyến chạy theo ngày, rồi zoom nhiều tầng (F4) xuống thành phố/pháo đài 3D đúng năm đó, giữ cùng bộ đếm ngày và mặt trời (M6). Đối thủ hoặc chỉ có tầng trên (kênh bản đồ) hoặc chỉ có tầng dưới (kênh thành phố).
2. **Ranh giới có nguồn ngay trên hình** ("approx. borders c. 1782 — Cliopatria"), hai nguồn kiểm chéo, vùng tranh chấp vẽ có kiểm soát. Khớp lời hứa "every date sourced, no AI imagery".
3. **Inset thay địa cầu:** khán giả luôn biết đang ở đâu mà không cần những cú bay địa cầu (lỗi T2).

**Rủi ro:** kênh bản đồ 2D đã đặt chuẩn rất cao về độ rõ (chú giải, mũi tên, nhịp). Shot `strategic` của mình phải **đạt độ rõ ngang họ**, không chỉ "đẹp hơn". Vì vậy cần luật BD-2/BD-3 và chấm mù riêng cho shot `strategic` ở G1b.

---

## 5. Máy dựng: M13 "bản đồ chiến lược" và M14 "inset"

### 5.1 Dùng lại từ k2v
- **`relief/map`** (`design/k2v/README.md` §E):
  - Nền tô bóng nhiều hướng, hai bảng màu (SEPIA cho quá khứ).
  - `routes` (nét đứt chảy, `draw`, `trail`, độ dày theo px không đổi khi zoom).
  - `walkers` + sticker tàu buồm (vật trong cảnh D2b).
  - `rings`, `regions` ≤ 3 (tô nhân giữ vân địa hình, viền sáng).
  - Máy spline liền, neo nhãn, LOD.
- **`relief_build.py`:** `--dem skadi` (SRTM 1″ ngoài Mỹ, ≤ 60°N), `--coast dem`, ranh và sông Natural Earth 10m.
- **Zoom nhiều tầng F4** (`aerial`, `close`) cho cú lặn từ bản đồ xuống ảnh/cảnh gần.
- **Lớp 2D `scripts/k2/lib/k2.js`:** SRCPX 38 px, `LL.occ` né nhãn, bảng điểm, log chữ cho K.
- **V5b-2b:** M1 (mũi tên ruy băng), M6 (bộ đếm ngày + mặt trời), campath có AGL (cho hộp dấu chân của inset).
- **Dữ liệu:** Natural Earth 1:50m/1:110m đã commit ở `design/k2v/data/`.

### 5.2 Cần thêm
| # | Việc | Ghi chú | Phiên |
|---|---|---|---|
| 1 | **DEM tầm châu lục `--dem etopo`** (NOAA ETOPO 2022, 15″/30″, có đáy biển) | SRTM 1″ cho khung 25° × 25° là ≈ 600 ô và không có đáy biển → quá nặng cho tầm châu lục. Giấy phép ETOPO **chưa kiểm** (dữ liệu NOAA thường là tài sản công) | V5b-2c |
| 2 | **Raster ranh giới theo phe** (Python lúc build): polygon → ảnh chỉ số thực thể + trường khoảng cách (mép mềm) → shader tô theo bảng `faction → màu`; viền px cố định | `regions` hiện giới hạn 3 khối nổi; ranh giới cần N thực thể, phẳng | V5b-2c (lite) |
| 3 | **Đổi mốc trong shot**: hai raster A/B hoà theo `uDay`; đổi chủ từng thực thể theo ngày (Minorca) | | V5b-2c (từng thực thể); V6 (tổng quát) |
| 4 | **Chuẩn hoá dữ liệu** `hist_borders.py`: lọc năm/ngày (Cliopatria, OHM, Newberry) → cắt đất NE → đơn giản theo km/px → lãnh thổ < 8 px thành điểm → đo lệch hai nguồn → manifest BD-4 + dòng ghi công | chủ yếu là `py/*.py` của phiên này, tổng quát hoá | V5b-2c |
| 5 | **Tuyến biển có kiểm đất** (BD-6) + mũi tên đầu nhọn 2D trên `strategic`, nhãn bám đầu tuyến | mở rộng `routes` | V5b-2c |
| 6 | **Chú giải ≤ 3 phe + dòng "approx. borders…"** trong `k2.js` | component mới nhỏ | V5b-2c |
| 7 | **M14 inset:** ảnh tĩnh bờ biển (từ relief/strategic, render một lần mỗi nơi) + hộp dấu chân khung máy tính từ campath, ghép ở lớp 2D (`k2.js` hoặc `tl/page.js`) | chi phí render ≈ 0 | V5b-2c |
| 8 | **Chuyển `strategic` → 3D `tl`** (hai bộ dựng khác nhau): khung cuối shot `strategic` khớp toạ độ/hướng với khung đầu shot 3D, hoà 0,5 s | | V5b-2c (khớp tay); V6 (tự động) |
| 9 | Log cho K: manifest lớp, nhãn, bbox inset, tuyến + claim id | | V5b-2c |
| 10 | M13 đầy đủ: nghiêng 2.5D, gạch vùng không chắc tự động, thư viện bảng màu series, Bắc Mỹ (Newberry + OHM bản địa), tuyến bộ/mặt trận | | V6 |

### 5.3 Ước giờ máy (ước — chưa đo)
| Hạng mục | Cách ước | Giờ máy |
|---|---|---|
| Render `strategic` cho T3 | 20 s × 24 = 480 khung; `relief/map` tầm 660 km đo được 10,65 s/khung mỗi tiến trình (K2V2, có lưới dời đỉnh); bản đồ chiến lược dùng địa hình nướng vào texture, lưới thưa, nên ước ≈ 2–4 s/khung; 3 tiến trình | ≈ 0,1–0,2 h; × 2 lượt sửa ≈ **0,2–0,4 h** |
| Inset | 4 ảnh tĩnh + ghép 2D | ≈ 0,02 h |
| Dựng nền ETOPO + raster ranh 3 mốc | ước theo `erie` 2,5 phút/bản | ≈ 0,1 h |
| **Tổng/tập** | | **≈ 0,4–0,6 h** |
| Phát triển + thử V5b-2c | đo thật 1 đoạn 8 s trước khi khoá | ≈ 1–1,5 h |

### 5.4 Phiên nào làm
| Phương án | Ưu | Nhược | Tác động | Rủi ro |
|---|---|---|---|---|
| **V5b-2c ngay sau V5b-2b (đề xuất)** — M13-lite + M14 | không đè P0 của V5b-2b; kịp G1b T3 | thêm một phiên V; chuỗi phụ thuộc dài hơn | lộ trình T3 §8: V5b-2b → **V5b-2c** ∥ gói claim tuyến → G1b | V5b-2b trễ → dùng dự phòng §2.4 |
| Gộp vào V5b-2b | ít phiên | V5b-2b đã nặng (P0 = 9 điểm + M9/M12/M6/M3/M4) | — | trễ P0 → chặn G1b T3 |
| Để cả cho V6 | gọn | T3 không có bản đồ chiến lược (chỉ dự phòng §2.4) | mất lợi thế ở tập thử | — |

---

## 6. Hạn chế
- Mẫu chỉ ở vùng Iberia–Pháp–Anh và 3 mốc. Chưa kiểm Địa Trung Hải phía đông, Trung Âu 1300–1600 hay Bắc Mỹ chi tiết; Bắc Mỹ mới đếm thực thể.
- Độ chính xác lịch sử của từng ranh **chưa kiểm bằng sử liệu**. Phiên chỉ đo độ khớp giữa hai nguồn (khớp chưa chắc đã đúng) và nêu 3 điểm nghi sai.
- Chưa đọc được: điều khoản GIS của Euratlas; trang Terms của GeaCron; trang quyền của LoC (403); giấy phép dữ liệu Atlas Pi; giấy phép ETOPO.
- §4 dựa trên hiểu biết chung, không xem lại video trong phiên này.
- Giờ render §5.3 là ước tính, chưa đo.
- Ảnh xem trước dựng bằng matplotlib để kiểm, **không phải** hình thật của kênh.

## 7. Chi phí thật và dòng đề xuất cho tệp dùng chung
| Hạng mục | Thực tế | Trần |
|---|---|---|
| Claude API | **$0** (không gọi; không có `cost.jsonl`) | $1 |
| YouTube Data API | **0 đv** | 0 |
| ElevenLabs | **0** ký tự | 0 |
| Giờ máy | **≈ 0,15 h** (Python/shapely/matplotlib + curl; venv tạm ngoài repo) | 1 h |
| Mạng (ngoài git) | ≈ 400 MB | — |
| WebSearch / WebFetch | 2 / 0 | — |

- **Dòng đề xuất cho `COST-LEDGER.csv`** (P chép): `NC-BD-01, 2026-10-17, nc-ban-do, nghiên cứu, claude_api_usd=0, youtube_units=0, elevenlabs_chars=0, render_h=0.15`.
- **RIGHTS (khi một tập dùng thật, P ghi):** Cliopatria v0.2.1 (CC BY 4.0, Zenodo 23128623); OpenHistoricalMap (CC0) + phần CC BY 4.0 (CNIG/IGN, LSIB…) theo danh sách đường của từng quan hệ đã dùng; Newberry AHCB (kèm ảnh trang Download); Natural Earth (PD).
- **AUTHORSHIP:** B3, B6, B8 là quyết định sáng tạo, ghi khi chủ dự án duyệt.

## 8. Tệp và preflight
- `reports/NC-BAN-DO-BAO-CAO.md` (tệp này).
- `reports/nc-ban-do/`:

| Tệp | Nội dung |
|---|---|
| `nguon.json` | bảng nguồn máy đọc |
| `cost.json` | chi phí thật |
| `giay-phep/GIAY-PHEP-NGUYEN-VAN.md` | trích nguyên văn + SHA trang |
| `mau/` | 8 GeoJSON: OHM ×3, Cliopatria ×3, Newberry ×2; tổng ≈ 660 KB, kèm `ATTRIBUTION.md` |
| `so-3-nguon-1704-1782-1941.png` | ảnh so 3 nguồn × 3 mốc |
| `gibraltar-eo-dat-ohm-vs-ne.png` | ảnh phóng eo đất Gibraltar |
| `minh-hoa-ban-do-chien-luoc-1782.png` | khung minh hoạ bản đồ chiến lược |
| `minh-hoa-inset-goc.png` | khung minh hoạ inset |
| `py/` | 10 script tái lập |

- Không commit dữ liệu GPL (historical-basemaps) hay tệp lớn.
- **Preflight:** `bash tools/preflight.sh --staged` (27 tệp) → **PREFLIGHT ĐẠT**; `lock.py --verify` → **KHỚP**; `origin/main` đã fetch trước khi chạy. Hook pre-commit/pre-push chạy lại khi commit/đẩy.

## 9. Tự quyết của phiên (không dừng hỏi), cần chủ dự án biết
1. Đếm 12 nguồn, trong đó Natural Earth, NHGIS, Atlas Pi là nguồn so sánh/nền. Có 8 nguồn ranh giới lịch sử thật: OHM, Cliopatria, HB, CShapes, Euratlas, GeaCron, Newberry, PD/Rumsey.
2. Thêm Cliopatria (không có trong danh sách ứng viên của lệnh): kết quả cho thấy đây là nguồn mở tốt nhất cho tầm châu lục.
3. Không chép dữ liệu GPL vào repo; chỉ ghi SHA + số đo.
4. Mẫu OHM đơn giản hoá 0,005° (~0,5 km) để vừa trần dung lượng; số đo độ chính xác dùng bản đầy đủ ngoài git.
5. Tạo venv tạm (shapely, pyproj, matplotlib, scipy, pyshp) trong thư mục scratch, không cài vào `/opt/cine`.
6. Hai khung minh hoạ có tuyến **SƠ ĐỒ** (ghi rõ trên hình "claims pending"). Không dùng làm tài sản phim.
7. Đề xuất bảng màu phe (B6) là đề xuất sáng tạo, chờ chủ dự án.

## 10. Việc chờ chủ dự án
1. **Duyệt B1:** nguồn chính Cliopatria + OHM (+ Newberry cho Mỹ; Natural Earth nền); loại HB, CShapes, Rumsey, GeaCron, NHGIS.
2. **Quyết Euratlas:** có muốn hỏi giá + điều khoản dùng trong video bán không? Phiên không đọc được trang cửa hàng. Không cần cho T3.
3. **Duyệt B2:** 3 shot `strategic` (SM1/SM2/SM3, 20 s) + 4 inset cho T3; giao P sửa `treatment.json` và mở **gói claim tuyến ≈ 10 claim** (cảng đi, ngày đi, Cape St Vincent 16/1/1780, Cape Spartel 20/10/1782, Cádiz → Algeciras 1782, Minorca 5/2/1782, Tangier 1940, liên minh 1703–04, điểm đổ bộ Torch).
4. **Duyệt B3–B5:** loại cảnh mới (trần 15 % / 8 s / 2 mỗi chương, tách NC-H2), inset (12 %, góc trên phải, 2,5–4 s), luật ranh giới (nhãn, hai nguồn, điểm thay polygon nhỏ, đệm 10 km quanh vùng tranh chấp) → P ghi Kinh thánh §4; **giao K viết BD-1…BD-8**.
5. **Duyệt B6 (màu phe series)** và **B8 (lãnh thổ bản địa)** → AUTHORSHIP.
6. **Duyệt B7:** mở **V5b-2c** (M13-lite + M14) ngay sau V5b-2b; M13 đầy đủ vào V6.
7. **Newberry:** có muốn gửi thư xin xác nhận bằng văn bản cho dùng thương mại không? Trang đã ghi rõ, nhưng tệp zip còn kèm giấy phép NC cũ. Không bắt buộc.
