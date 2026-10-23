# RIGHTS NHÁP — K2C-T4-02 London (TIEN-KY-T4, 23/10/2026) — phiên P chép vào `RIGHTS.md` sau G1

> Bằng chứng từng mục: `licenses/<id>.json` (siêu dữ liệu NGUYÊN VĂN của nơi giữ: API/manifest/linked-art, URL, ngày tải, SHA-256 tệp gốc) + `licenses/<id>-trang.jpg|.html` (chụp trang, khi trang không chặn trình duyệt tự động). Tệp gốc ngoài git (`/var/tmp/ldn/tu-lieu/`, tái tạo bằng `scripts/k2ldn/tai_tu_lieu.py`, SHA trong `licenses/SHA256-TU-LIEU.txt`); bản thu ≤ 2 400 px trong `tu-lieu/`.
> Ngày truy cập mọi mục: 23/10/2026. Email bên thứ ba trong trang lưu đã che (`[email-đã-che]`).

## A. Tư liệu hình (tranh, bản khắc, bản đồ, chân dung)

| ID | Mục | Nơi giữ · số hiệu | Giấy phép (nguyên văn nơi giữ) | Bằng chứng | Rủi ro | Dùng ở (bảng shot v1) | Ghi công đề xuất |
|---|---|---|---|---|---|---|---|
| rijks-doornick | *Platte Grondt der Verbrande Stadt London* (Doornick, Amsterdam 1666; vùng cháy để trắng — theo khảo sát Hollar) | Rijksmuseum RP-P-OB-82.345 | linked-art: `creativecommons.org/publicdomain/mark/1.0/` (+ CC0 siêu dữ liệu) | json + trang chụp | thấp | H1-09 (bản đồ hoạt hoá), H5-03; nguồn ranh cháy cuối (bậc 1) | Rijksmuseum, Amsterdam (Public Domain) |
| met-360649 | Hollar, *Prospects of London Before and After the Great Fire* (2 tấm toàn cảnh) | The Met 17.50.100–.101 | API `isPublicDomain: true` (Met Open Access CC0) | json (trang chặn Vercel) | thấp | H1-03, H2-12 (then–now) | The Metropolitan Museum of Art, CC0 |
| met-361738 | *London before the Great Fire* (1666–77) | The Met 56.581.8 | `isPublicDomain: true` | json | thấp | H1-03 dự phòng | The Met, CC0 |
| met-395057 | Hollar, *Old St Paul's Cathedral seen from the East* (1656–58) | The Met 2010.529 | `isPublicDomain: true` | json | thấp | **T3**; H1-13 góc khung | The Met, CC0 |
| ycba-266 | *The Great Fire of London, with Ludgate and Old St. Paul's* (c. 1670, sơn dầu) | YCBA B1976.7.27 | manifest `rights: creativecommons.org/publicdomain/zero/1.0/`; "Copyright Statement: Public Domain" | json (trang chặn Cloudflare) | thấp | tham chiếu không khí bậc 4 (lửa đêm, Ludgate); tư liệu chồng cảnh H1-13 (tuỳ chọn) | Yale Center for British Art, Paul Mellon Collection |
| ycba-40597 | *General View of London during the Great Fire of 1666* (bản in) | YCBA B1977.14.17854 | như trên (CC0 / Public Domain) | json | thấp | tham chiếu bậc 4 | YCBA |
| rijks-luyken | Jan Luyken, *Grote brand van Londen, 1666* (1698) | Rijksmuseum RP-P-1896-A-19368-1507 | PDM | json + trang | thấp | tham chiếu bậc 4 (không dùng làm dữ kiện vị trí) | Rijksmuseum (PD) |
| rijks-charles2 | *Portret van Karel II* | Rijksmuseum RP-P-OB-32.684 | PDM | json + trang | thấp | thẻ nhân vật (nếu lời nhắc nhà Vua — L37 "hands the King") | Rijksmuseum (PD) |
| rijks-monument | *Gezicht op het Monument* (sau 1676) | Rijksmuseum RP-P-2018-836 | CC0 | json + trang | thấp | H2-08 (góc khung) | Rijksmuseum (CC0) |
| nga-wren | John Smith theo Kneller, *Sir Christopher Wren* | NGA 2001.118.55 | NGA open data `published_images.csv`: `openaccess = 1` (NGA Open Access: CC0) | json (trang chặn) | thấp | thẻ Wren (H2-02) | National Gallery of Art, Washington (CC0) |
| loc-wren-plan | *A Plan for rebuilding the City of London … Wren* (bản khắc 1767) | Library of Congress 2004678686 | `rights_information: "No known restrictions on publication."` | json (trang chặn) | thấp | H2-02 (đặt khớp lên City cháy) | Library of Congress, Prints & Photographs |
| commons-ogilby | Ogilby & Morgan, *A Large and Accurate Map of the City of London* (1676/77) | British Library Crace Port. 2.61, qua Wikimedia Commons | Commons: "Public domain"; "provided by the British Library from its digital collections" | json + trang Commons | **vừa** (bản 2 000 px; cần xác nhận điều khoản BL cho bản phân giải cao) | H2-11 (chờ) | British Library (PD) |

**Chưa dùng / bị chặn (ghi để phiên sau):**
- Leake 1667 / Hollar "An Exact Surveigh" — bản TAMU (NoC-US, "copyright review … public domain") **không tải được: Cloudflare 403** cả với trình duyệt tự động; bản Yale Beinecke (15831925) có câu quyền chung "may be subject to the copyright law…" → không dùng khi chưa rõ. Đề xuất: chủ dự án tải tay bản TAMU (trình duyệt thật) hoặc thay bằng Doornick (đã dùng).
- Doornick 1666 bản Univ. of Michigan — không cần (đã có bản Rijksmuseum PDM, cùng bản khắc).
- Hollar *Long View* 1647 (Commons, nhiều bản cắt) — rủi ro vừa, chưa xác minh nguồn scan → chưa dùng.
- Phương án Evelyn (RMG F0422 qua Commons "Public domain") — rủi ro vừa (RMG có điều khoản riêng) → chưa tải.
- Ảnh Crown MOI 1940 (PD vì chụp trước 1957): **chưa tìm được bản Commons ngoài sê-ri HU** trong phiên (API Commons trả 429 nhiều lần); ứng viên để kiểm: "File:St Paul destroyed.jpg" (danh mục London Blitz — chưa đọc được trang). KHÔNG dùng ảnh Mason "St Paul's Survives" (T4-G1).

## B. Dữ liệu không gian

| Mục | Nguồn | Giấy phép | Dùng | Ghi công |
|---|---|---|---|---|
| OpenStreetMap (toà, phố, nước, điểm có tên) — bbox E −0,130…−0,060, N 51,496…51,526 | api.openstreetmap.org /map (tải 23/10/2026, 21 ô, 156 MB) | ODbL 1.0 | toà 2026 (17 815), mạng phố còn giữ (lô nhà 1666), mặt nước 2026, điểm khớp bản đồ | © OpenStreetMap contributors (ODbL) |
| LiDAR Composite DTM 1 m + First-Return DSM 1 m (2022) — E 529500–535500, N 179500–182500 | Environment Agency, WCS `environment.data.gov.uk/spatialdata/...` | Open Government Licence v3 | địa hình; cao độ toà thiếu thẻ (7 824 toà) | Contains Environment Agency information © Environment Agency and/or database right 2022 |
| Lưới OSTN15 (pyproj) | cdn.proj.org `uk_os_OSTN15_NTv2_OSGBtoETRS.tif` | (OS — OSTN15 dùng tự do; **[cần kiểm]** câu giấy phép) | đổi WGS84 → EPSG:27700 | — |
| OS Open data | — | OGL | **chưa dùng** trong phiên | — |

## C. Văn bản nguồn (đã có trong repo, NC-N2P)
- Pepys (Braybrooke), Gutenberg #4167 — PD Mỹ; Evelyn (Bray), Gutenberg #42081 — PD Mỹ; *A True and Exact Relation…* 1666, EEBO-TCP A63370 (EarlyPrint) — CC0. (Phiên P đã có dòng RIGHTS từ NC-N2P? — **[cần kiểm]** RIGHTS.md.)

## D. Đầu ra AI của phiên (sổ AI `reports/tien-ky-t4/so-ai.jsonl`, `so-ai-gemini.jsonl`)
| Mục | Công cụ | Điều khoản | C2PA | Dùng |
|---|---|---|---|---|
| T6 tấm nền N2+ (3 lượt) | OpenAI `gpt-image-2.5-sunburst-2026-09-08`, `POST /v1/images/edits` | điều khoản OpenAI (đầu ra thuộc người dùng) — như NC-N2P | `trainedAlgorithmicMedia` 3/3 | chỉ bản thử |
| T5 minh hoạ M-d (1 lượt) | Gemini `gemini-omni-1.1-flash` image-to-video | Gemini API terms (đọc 21/10, NC-N2P §4): dùng thương mại, không độc quyền | C2PA + SynthID trong manifest | chỉ bản thử |

## E. Phần mềm/tài sản khác
- Lửa/khói cách A: atlas thể tích sinh thủ tục (`scripts/k2ldn/nuong_flipbook.py`, numpy) — không tài sản ngoài.
- LUT kênh xem thử: `channel-k2/k2c-t3-01/mau/k2c-t3-kenh-v030.cube` (của dự án).
- Blender 5.2.2 (GPL, công cụ), three.js 0.180 (MIT), Chromium/Playwright (công cụ).
