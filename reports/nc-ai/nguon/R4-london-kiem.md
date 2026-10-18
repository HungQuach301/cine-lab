# R4 — Nguồn London 1666 và lớp kiểm chứng sự kiện/niên đại

Ngày đọc toàn bộ: **2026-10-18**. Người thực hiện: worker nghiên cứu R4. Mọi trích dẫn tiếng Anh giữ nguyên văn như trang trả về. "ĐÃ KIỂM" nghĩa là tôi đã tải thật (curl, HTTP 200) và xem phần đầu file. "CHƯA KIỂM" nghĩa là chưa xác minh bằng tải thật.

---

## PHẦN 1 — Nguồn công cộng (PD/CC0) cho phim tài liệu về Đại hoả London (2–6/9/1666)

### Tầng 1 — Bản đồ, sơ đồ đo vẽ cùng thời

| Nguồn | URL ảnh / trang | Quyền (nguyên văn) | Đánh giá |
|---|---|---|---|
| Hollar, bản đồ vùng cháy 1666 (bản Commons) | Trang: https://commons.wikimedia.org/wiki/File:Map.London.gutted.1666.jpg · Ảnh gốc: https://upload.wikimedia.org/wikipedia/commons/5/59/Map.London.gutted.1666.jpg | "This is a faithful photographic reproduction of a two-dimensional, public domain work of art." + Public Domain Mark 1.0 | Dùng được nhưng **chỉ 2.369 × 1.879 px**, nguồn là trang gia phả rootsweb, không ghi tổ chức giữ bản gốc. Chỉ đủ cho tham chiếu hoặc khung hình nhỏ. |
| Hollar, "Prospects of London Before and After the Great Fire" (1666) — The Met 360649 | Trang: https://www.metmuseum.org/art/collection/search/360649 · Ảnh: https://images.metmuseum.org/CRDImages/dp/original/DP827163.jpg | API Met trả `isPublicDomain: True` (Met Open Access = CC0) | **Nguồn tốt nhất cho cảnh "trước/sau"**: toàn cảnh trước và sau cháy, cùng năm 1666, CC0. |
| Hollar, "London before the Great Fire" (1666–77) — The Met 361738 | https://www.metmuseum.org/art/collection/search/361738 · https://images.metmuseum.org/CRDImages/dp/original/DP823346.jpg | `isPublicDomain: True` | CC0. |
| Leake/Hollar, "An Exact Surveigh…" 1667 | British History Online: https://www.british-history.ac.uk/no-series/london-map-leake/1667 | "This free content was digitised by scanning. All rights reserved." | **LOẠI bản BHO** (bảo lưu quyền). Các bản khác: TAMU Spotlight (bản facsimile LTS 1908–09, theo kết quả tìm kiếm là PD sau rà soát năm 2021, CHƯA KIỂM trang) https://spotlight.library.tamu.edu/spotlight/london-maps-batch-2/catalog/c515c7fba6686f87b94bad30e37daf08 ; National Archives chỉ 900 px. Cần một lượt tìm riêng bản độ phân giải cao CC0. |
| Ogilby & Morgan 1676 | https://www.british-history.ac.uk/no-series/london-map-ogilby-morgan/1676 | "This free content was digitised by scanning. Public Domain." | **Dùng được**: tỷ lệ "100 feet to the inch", toàn bộ City đã xây lại. BHO hiển thị theo ô ảnh; chưa thấy nút tải file gốc, cần tải từng ô hoặc hỏi BHO. Lưu ý: đây là London **sau** khi xây lại (1676), không phải 1666. |
| Bản đồ Rijksmuseum về vùng cháy | RP-P-OB-82.342 "Plattegrond van Londen na de grote brand van 1666" (https://id.rijksmuseum.nl/200503521); RP-P-OB-82.018 "Platte grondt der verbrande stadt London" 1667 (https://id.rijksmuseum.nl/200502631) | Ảnh PD của Rijksmuseum mang nhãn "Public domain" (PDM 1.0), xem tầng 4 | Bản đồ Hà Lan cùng thời, dùng được. |
| Map of Early Modern London (MoEML, nền Agas) | https://mapoflondon.uvic.ca/about.htm | "This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License." | **LOẠI** vì có SA. Trang không tách riêng giấy phép cho dữ liệu địa lý. Bản thân bản đồ Agas (~1561) đã PD, nhưng phải lấy ảnh từ nguồn khác, không lấy lớp số hoá của MoEML. |
| Faithorne & Newcourt 1658; ảnh Agas độc lập | — | — | **CHƯA KIỂM** (hết ngân sách lượt gọi). API Commons trả 429 (giới hạn tốc độ). |

### Tầng 2 — Văn bản (URL tải thẳng bằng curl, ĐÃ KIỂM HTTP 200)

| Tác phẩm | URL tải thẳng | Đã kiểm |
|---|---|---|
| Pepys, Diary — Vol. 45: August/September 1666 (PG #4167; Editor: Braybrooke / Henry B. Wheatley; phát hành 1/12/2004, cập nhật 27/12/2020) | https://www.gutenberg.org/cache/epub/4167/pg4167.txt | 200, 160.645 byte. Dòng 1064 có: "2nd (Lord's day).  Some of our mayds sitting up late last night to get things ready against our feast to-day, Jane called us up about three in the morning, to tell us of a great fire they saw in the City." |
| Pepys — Complete 1666 N.S. (PG #4171) | https://www.gutenberg.org/cache/epub/4171/pg4171.txt | 200, 813.803 byte |
| Pepys — toàn bộ nhật ký (PG #4200) | https://www.gutenberg.org/cache/epub/4200/pg4200.txt | 200, 6.800.848 byte |
| Evelyn, Diary Vol. 2 of 2 (PG #42081, Editor William Bray) — **có các mục 2–7/9/1666** (dòng 946: "2d September, 1666. This fatal night, about ten, began the deplorable…") | https://www.gutenberg.org/cache/epub/42081/pg42081.txt | 200, 864.683 byte |
| Evelyn, Diary Vol. 1 of 2 (PG #41218) — không chứa mục cháy | https://www.gutenberg.org/cache/epub/41218/pg41218.txt | 200, 941.351 byte |
| Thomas Vincent, "God's terrible voice in the city" (1667), EEBO-TCP A64990 (XML TEI) | https://raw.githubusercontent.com/textcreationpartnership/A64990/master/A64990.xml | 200, 442.791 byte. Quyền: "This Phase I text is available for reuse, according to the terms of Creative Commons 0 1.0 Universal . The text can be copied, modified, distributed and performed, even for commercial purposes, all without asking permission." |
| Rege Sincera, "Observations, both historical and moral, upon the burning of London, September 1666…" (1667), EEBO-TCP A53837 | https://raw.githubusercontent.com/textcreationpartnership/A53837/master/A53837.xml | 200, 71.308 byte. Quyền: "…the Text Creation Partnership has waived all copyright … according to the terms of the CC0 1.0 Public Domain Dedication … This waiver does not extend to any page images or other supplementary files…" |
| London Gazette No. 85 (trang hiển thị ngày "03 September 1666") | https://www.thegazette.co.uk/London/issue/85/page/1/data.pdf · https://www.thegazette.co.uk/London/issue/85/page/2/data.pdf | 200, PDF 1 trang mỗi file (104.206 / 89.833 byte). Quyền: "All content is available under the Open Government Licence v3.0, except where otherwise stated." **Chưa đọc được chữ trong PDF** (máy không có pdftotext/pypdf) nên chưa xác nhận trang nào chứa bản tin cháy; cần OCR hoặc mở bằng mắt. OGL v3.0 cho phép thương mại, yêu cầu ghi nguồn. |

Ghi chú: văn bản Gutenberg là PD tại Mỹ; khi dùng nên bỏ phần header/footer "Project Gutenberg" nếu không ghi tên thương hiệu (theo giấy phép PG). Tôi đã tính SHA-256 các file tải về để đối chiếu (bên điều phối sẽ tự tính lại): pg4167.txt `8a7ec38ef2de9aff782077ac6e6127c2b83ecc78e4be22288f68ba43d4a3f918`; pg4171.txt `a0a83c7a98afaddacc381edf252b8ebbfddf948d684daf69899b2e2ba0cc9aa2`; pg4200.txt `1d8c7943d9159e4e40d98e5fc454c4d771951956863048bfdda9e92fb71f58a1`; pg41218.txt `750ab3c0cc5d5d2c5a21d5e63483f2271e74431e2ed30ce376fb66ccc7089911`; pg42081.txt `912a1791a66b5199d34101866d536c701ecf46e8bc4c1fe643e79492dbfd51cb`; A64990.xml `36798f66f98c32482b09209d7acb0ed204bacae744b5eae7c40532ca7a093f29`; A53837.xml `a2f88fdea18ba3365d866703cb350fef780194a32b91199f1793016336ce6b68`; gaz85_p1.pdf `3315c9baf6e50784cc560b9e3e8aa1e4e79dceef96b3d7ef5ada622f05e59877`; gaz85_p2.pdf `f6c8c424f58ef5e7f7cc3d943131fbf8f16bd5f39cc4b2ab550b1b44ba56c718`;  Bản Gutenberg có thể đổi khi PG cập nhật, nên SHA chỉ đúng cho ngày 18/10/2026.

### Tầng 3 — Công trình còn lại, hiện vật, trang phục

- **London Museum** (tên mới của Museum of London), ví dụ tranh 57.54 https://londonmuseum.org.uk/collections/v/object-102171/the-great-fire-of-london : "digital image © London Museum"; ô Creative Commons để trống ("—"); "To license this image for commercial use, please contact the London Museum Picture Library." → **Không phải dữ liệu mở; dùng thương mại phải mua giấy phép.**
- **Monument**: không tìm thấy bộ dữ liệu mở (CHƯA KIỂM). Đề xuất dùng ảnh chụp tự làm hoặc bản khắc thế kỷ 17 (ví dụ Rijksmuseum KOG-AA-1-22-6000 có "gedenkzuil voor de brand").
- **Trang phục, The Met (CC0, API trả `isPublicDomain: True`)**. The Met có rất ít trang phục Anh thật đúng năm 1660; đây là các mục gần nhất:
  1. Doublet, British, ca. 1645, da và lụa — https://www.metmuseum.org/art/collection/search/81557 (ảnh: https://images.metmuseum.org/CRDImages/ci/original/1982.183.2a–c_F1.jpg). Sớm hơn 1666 khoảng 20 năm.
  2. Hollar, "English Lady in Winter Costume" 1644 — https://www.metmuseum.org/art/collection/search/356521
  3. Sir Peter Lely, "A Knight of the Order of the Garter" 1663–71 — https://www.metmuseum.org/art/collection/search/634351
  4. Lely, "Study of the Forearms and Hands of a Woman" ca. 1665 — https://www.metmuseum.org/art/collection/search/459387
  5. Hollar, "Coronation Procession of Charles II Through London" 1662 — https://www.metmuseum.org/art/collection/search/361494 (đám đông, trang phục, phố London ngay trước cháy)
  - Rủi ro: Doublet 81557 có dáng của thập niên 1640, không phải 1666. Dùng làm chuẩn trang phục 1666 dễ sinh lỗi niên đại. Nên đối chiếu thêm Lely và Hollar 1660s, và tìm riêng ở V&A (chưa kiểm điều khoản).
- Ghi chú kỹ thuật: endpoint `/public/collection/v1/search` của Met **đã ngừng ngày 2026-10-01**; phải dùng `/public/collection/v1.1/search` (API trả nguyên văn: "use /public/collection/v1.1/search, which is Elastic-backed and paginated via offset and limit").

### Tầng 4 — Tranh in, tranh vẽ cùng thời

- **Hollar, Long View of London from Bankside (1647)**: https://upload.wikimedia.org/wikipedia/commons/5/5f/1647_Long_view_of_London_From_Bankside_-_Wenceslaus_Hollar.jpg — **28.661 × 5.560 px**, khoảng 73 MB. Trang Commons ghi "Scanned from a facsimile" và gắn Public Domain Mark 1.0 ("This file has been identified as being free of known restrictions under copyright law, including all related and neighboring rights."). Không ghi tổ chức nguồn. Bản British Museum và Royal Collection có giấy phép hạn chế hơn.
- **Hollar, Prospects Before and After the Great Fire 1666**: The Met 360649 (CC0, xem tầng 1).
- **Rijksmuseum (PD, nhãn trang: "Public domain" → PDM 1.0)**:
  - RP-P-OB-76.977 "Gezicht op Londen tijdens de grote brand, 1666", in khắc khuyết danh theo Pieter Hendricksz. Schut, nhà xuất bản Justus Danckerts — https://www.rijksmuseum.nl/en/collection/RP-P-OB-76.977 (id https://id.rijksmuseum.nl/200474126)
  - RP-P-OB-82.020 "Gezicht op Londen tijdens de grote brand, 1666" (https://id.rijksmuseum.nl/200502636)
  - RP-P-OB-82.017 "Pourtraict & description, De l'horrible embrasement de Feu, dans la Ville de Londres" 1666 (https://id.rijksmuseum.nl/200502629)
  - RP-P-OB-82.010: tranh in phúng dụ Hà Lan về vụ đốt Terschelling năm 1666, bối cảnh chiến tranh Anh–Hà Lan (https://id.rijksmuseum.nl/200502499)
- **Tranh sơn dầu của Lieve Verschuier tại Rijksmuseum: KHÔNG TÌM THẤY.** API Rijksmuseum không trả tranh sơn dầu (SK-A) nào về vụ cháy London. Tranh "Dutch School" nổi tiếng thuộc London Museum (57.54), không phải dữ liệu mở. Tranh Loutherbourg (1797) thuộc Yale Center for British Art, quá muộn để làm bằng chứng cùng thời. Không nên ghi "Verschuier, Rijksmuseum" khi chưa có số hiệu.

### Tầng 5 — Tương tự (analogues)

Chưa nghiên cứu sâu (giới hạn lượt gọi). Gợi ý ứng viên: các tranh in Hollar khác về London trước cháy (The Met 360855, 360940, 360615 Royal Exchange, 395057/336038/336039 St Paul's cũ, tất cả CC0); bản đồ phân tích tốc độ cháy theo ngày trên Commons (`Great Fire of London Sunday/Monday/Tuesday.png`, là đồ hoạ hiện đại, phải kiểm giấy phép riêng).

---

## PHẦN 2 — Lớp kiểm chứng sự kiện và niên đại

### (a) Tự động đối chiếu trích dẫn với nguồn; tỷ lệ lỗi đã công bố

1. **Wu et al., "An automated framework for assessing how well LLMs cite relevant medical references", Nature Communications 16:3615 (16/4/2025), DOI 10.1038/s41467-025-58551-6** — https://pmc.ncbi.nlm.nih.gov/articles/PMC12003634/
   - "between 50% and 90% of LLM responses are not fully supported, and sometimes contradicted, by the sources they cite."
   - Với GPT-4o có Web Search: "approximately 30% of individual statements are unsupported, and nearly half of its responses are not fully supported."
   - Bộ kiểm tự động: "88.7% agreement between the Source Verification model and the doctor consensus". Đây là mức tin cậy tham khảo cho một bộ kiểm trích dẫn dùng LLM.
2. **Magesh et al., "Hallucination-Free? Assessing the Reliability of Leading AI Legal Research Tools", arXiv:2405.20362 (30/5/2024)** — https://arxiv.org/abs/2405.20362 : các công cụ của LexisNexis và Thomson Reuters "each hallucinate between 17% and 33% of the time." Đây là các công cụ có RAG.
3. **Verga et al., "Replacing Judges with Juries: Evaluating LLM Generations with a Panel of Diverse Models" (PoLL), arXiv:2404.18796 (29/4/2024)** — https://arxiv.org/abs/2404.18796 : hội đồng nhiều mô hình nhỏ "outperforms a single large judge", "exhibits less intra-model bias due to its composition of disjoint model families", và "over seven times less expensive". Đây là cơ sở cho cách dùng nhiều LLM thuộc các họ khác nhau để kiểm chéo.

Hàm ý cho CINE LAB: ngay cả khi có truy xuất nguồn, LLM vẫn bịa hoặc đưa ra trích dẫn không được nguồn ủng hộ ở mức 17–50%. Vì vậy mọi trích dẫn trong lời dẫn phải được **khớp chuỗi nguyên văn bằng máy** với file nguồn đã băm SHA (Pepys, Evelyn, Vincent, Rege Sincera), không để LLM tự xác nhận.

### (b) Mô hình thị giác phát hiện sai niên đại

- **Ranjan, Jha, Kumari, Shen, "On the Cultural Anachronism and Temporal Reasoning in Vision Language Models", Findings of ACL 2026, tr. 30294–30310** — https://aclanthology.org/2026.findings-acl.1514/ (arXiv 2605.15071). Benchmark TAB-VLM: "a dataset of 600 questions across six categories", 1.600 hiện vật văn hoá Ấn Độ; "even the best model (GPT-5.2) achieves only 58.7% overall accuracy."
- Hàm ý: VLM **không đáng tin** làm cổng duy nhất để bắt lỗi niên đại (độ chính xác khoảng 59% trên miền khác). Nên dùng VLM như bộ lọc gợi ý, kết hợp danh mục kiểm do người soạn (vật liệu, đèn, kính cửa sổ, trang phục) và tham chiếu tầng 1–4 ở trên.

### (c) Công cụ đo nguồn gốc ảnh / phát hiện ảnh AI

- **c2patool** (Content Authenticity Initiative): repo https://github.com/contentauth/c2patool. `Cargo.toml` ghi `version = "0.29.0-dev"`, `license = "MIT OR Apache-2.0"` (có LICENSE-MIT và LICENSE-APACHE, HTTP 200). Thư viện `c2pa-rs` cũng vậy: "distributed under the terms of both the MIT license … and the Apache License (Version 2.0)". Cài đặt: "brew install c2patool" hoặc tải prebuilt binary từ Releases. Lệnh kiểm (từ docs/usage.md): `c2patool sample/C.jpg` (hiển thị manifest; "It will report if the manifest validated or show any errors encountered in validation."), `c2patool sample/C.jpg -d` ("Display detailed C2PA-formatted manifest data."), `--info`, `--certs`, `--tree`; lệnh con `trust` để cấu hình danh sách chứng chỉ tin cậy.
- **SynthID Detector**: blog Google (https://blog.google/technology/ai/ai-image-verification-gemini-app/) mô tả cách kiểm trong ứng dụng Gemini: "upload it to the Gemini app and ask a question such as: 'Was this created with Google AI?'". Theo báo thứ cấp (chưa đối chiếu được trang chính thức synthid.com), cổng detector đã mở công khai và nhận cả dấu của đối tác. Giới hạn: chỉ phát hiện nội dung mang watermark SynthID; kết quả âm tính không chứng minh ảnh không phải do AI tạo.
- Không có thước đo chuẩn công khai cho mức "AI-looking". C2PA và SynthID kiểm nguồn gốc, không đo thẩm mỹ.

### (d) YouTube Data API — phân tích bình luận

- https://developers.google.com/youtube/v3/docs/commentThreads/list : "**Quota impact:** A call to this method has a quota cost of 1 unit." `maxResults`: "Acceptable values are `1` to `100`, inclusive. The default value is `20`."
- https://developers.google.com/youtube/v3/getting-started : "have a default quota allocation of 100 `search.list` calls, 100 `videos.insert` calls, and 10,000 units per day"; "A read operation that retrieves a list of resources -- channels, videos, playlists -- usually costs 1 unit."
- Suy ra: 10.000 đơn vị/ngày tương đương tối đa khoảng 1.000.000 luồng bình luận cấp cao mỗi ngày (100 mỗi lần gọi), dư cho nhu cầu dự án.

---

## Sự cố và hạn chế cần báo

- **Sự cố quyền riêng tư**: trong một lệnh curl tới API Wikimedia Commons, tôi lỡ đặt email chủ dự án trong header User-Agent. Các yêu cầu đó bị Commons trả lỗi 429. Không lặp lại; báo để chủ dự án biết.
- Bị chặn hoặc không đọc được: gutendex.com (timeout); Commons API (429); trang tìm kiếm Rijksmuseum (render JS, rỗng); Commons Category Hollar maps (404); c2pa-rs/cli README (404, công cụ đã chuyển về repo riêng); opensource.contentauthenticity.org docs (trang rỗng); `gh api` (403, repo không gắn vào phiên); Met API v1/search (đã ngừng).
- Chưa kiểm: Faithorne & Newcourt 1658, ảnh Agas độc lập, bản Leake độ phân giải cao CC0, nội dung chữ của Gazette 85, Monument, V&A.
