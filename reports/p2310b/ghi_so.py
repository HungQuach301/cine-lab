"""P-2310b · ghi sổ theo quyết định chủ dự án 23/10/2026 17:42: AUTHORSHIP, RIGHTS, COST-LEDGER, BAI-HOC-K2, HANG-DOI.
Chỉ nối thêm (HANG-DOI: chèn một mục mới ngay trên mục 23/10 PHAT-HANH-T3); không sửa dòng cũ.
Chạy: python3 -I reports/p2310b/ghi_so.py <repo>"""
import csv, io, pathlib, sys

R = pathlib.Path(sys.argv[1])
NGUYEN_VAN = '"S3 KHÔNG cần đổi, còn lại đồng ý theo đề xuất của bạn" (trả lời đề xuất điều phối 17:40; "S3" = mục D3 của phiếu G1)'


def noi(ten, chu):
    p = R / ten
    s = p.open(encoding="utf-8", newline="").read()  # giữ nguyên \r có sẵn (bài học P-2210)
    assert s.endswith("\n")
    p.open("w", encoding="utf-8", newline="").write(s + chu)


# ---------- AUTHORSHIP ----------
au = []
au.append(
    "| 2026-10-23 | Kênh 2 T4 London — G1 tiền kỳ T4 + bước M1b (17:42; P-2310b ghi) | Nguyên văn: " + NGUYEN_VAN + ". "
    "Nội dung theo `reports/tien-ky-t4/PHIEU-G1.md`: D1 treatment + xương sống (a); D2 lời nháp v1 (a), 22 mục [cần kiểm] xử lý ở v2 trước khi ghi giọng; "
    "**D3 GIỮ câu L04 \"London has burned to the ground twice\" và logline như cũ** (không đổi sang \"The heart of London has burned twice\"); "
    "D4 bảng shot v1 (a), khoá cap ở v2; D5 lửa/khói cách A cho cảnh rộng + Cycles GPU chỉ 3–4 cận đêm (≈ 30–40 s), không ghép A↔B trong một cú máy, Cycles ngày không sửa được mép thể tích → chỉ A; "
    "D6 dựng lại Old St Paul's theo bản khắc Hollar trong Dugdale 1658; D7 hoà tranh khắc 4 điểm + thị sai 2,5D thủ công cho 2–3 tranh, góc khung cho phần còn lại; "
    "D8 bản đồ hoạt hoá ranh theo ngày nội suy RBF + thẻ \"ước lượng\"; D9 Kinh thánh §19 (sản xuất giữ ≤ 3°/s); D10 M-d (6) \"nổ nhà Tower Street\" → \"người cứu đồ lên xe ở Cheapside\" (nổ nhà dựng 3D); "
    "**D11 gửi phiên K xét phép (iii) bộ kiểm N2P; kế hoạch sản xuất theo phương án dự phòng tấm nền N2+ ≤ 15 % thời lượng tới khi K kết luận**; "
    "**D12 bỏ Leake 1667, dùng Doornick 1666**; D13 Ogilby & Morgan chỉ dùng kiểm danh sách phố, không lên hình tới khi xác nhận điều khoản BL; "
    "D14 tìm ảnh Crown MOI 1940 ngoài sê-ri HU, mặc định không ảnh; D15 phạm vi bom 29/12/1940 theo văn bản + ranh vẽ tay \"ước lượng\"; D16 ngân sách theo D5 (a); "
    "D17 ghim công cụ `UOC-VA-GHIM.md` §3; D18 ảnh đầu M-d = tấm N2+ đêm dựng từ render rồi mới i2v, dự phòng cắt ≈ 1 s đầu. "
    "Thêm **bước M1b \"khoá look T4\" trước animatic** (phiên LOOK-T4). Văn bản: Kinh thánh §13.6, §15 (d)(f), §19 "
    "| Chủ dự án duyệt G1 T4; tự quyết GIỮ cách nói mạnh của câu mở/logline \"burned to the ground twice\" (bác đề xuất làm mềm D3 (a) của phiên); duyệt thêm bước khoá look trước animatic "
    "| TIEN-KY-T4: treatment, lời nháp v1, bảng shot v1, 6 bản thử, phiếu G1 D1–D18, đề xuất §19; điều phối: đề xuất 17:40 (gồm M1b, D12 (b)) | Chủ dự án |\n")
au.append(
    "| 2026-10-23 | Kênh 2 T4 London — dữ kiện sáng tạo của treatment đã duyệt (17:42, D1; P-2310b ghi) | Nguồn: `channel-k2/k2c-t4-02/TREATMENT.md`. "
    "**Hook:** Pepys 2/9/1666 xem lửa từ *\"a little ale-house on the Bankside, over against the Three Cranes\"* (bậc 1, Gutenberg #4167) — trùng điểm máy xương sống Bankside CAO (T4-G3). "
    "**8 khoảnh khắc then chốt:** (1) vòng cung lửa từ Bankside (M03; lặp ở H1-08 khi Pepys kể); "
    "(2) bản đồ Doornick 1666 sống dậy: lửa loang theo ngày 2→6/9 trên chính tờ bản đồ, máy đẩy vào rồi bản đồ tan vào 3D cùng toạ độ (H1-09); "
    "(3) Old St Paul's bén lửa qua giàn giáo, chì chảy (H1-13 Cycles + M-d chì chảy H1-14); "
    "(4) phương án Wren đè đúng toạ độ lên City tro tàn rồi mờ đi — \"None of them is built\" (H2-02); "
    "(5) nhà gạch mọc lại trên đúng lô cũ, Monument vươn 202 ft với vạch nối tới lò bánh (H2-05, H2-06); "
    "(6) mái vòm mọc 1675 → 1711, giờ vàng, góc thấp (H2-09, H2-10); "
    "(7) mái vòm giữa khói lửa đêm 29/12/1940 — dựng 3D Cycles (H4-04), thay ảnh Mason (T4-G1); sáng ra 1 ảnh Crown MOI 1940 ở góc khung (H4-05); "
    "(8) khép vòng: cùng khung Bankside — vòng cung lửa 1666 khớp cắt sang đèn City 2026, rồi kéo lùi (H5-07, H5-08). "
    "(Khoảnh khắc M-d (6) trong treatment đổi theo D10 — xem dòng trên.) "
    "| Chủ dự án: xương sống (22/10 07:19), điểm máy Bankside cao (T4-G3), 3 điểm nâng cấp 13:06 (bản đồ lịch sử hoạt hoá, bản vẽ công trình/nhân vật, đa dạng cú máy); duyệt treatment 17:42 "
    "| TIEN-KY-T4: chọn hook Pepys có nguồn, 8 khoảnh khắc, phân bổ shot | Chủ dự án |\n")
au.append(
    "| 2026-10-23 | Kênh 2 — bảng QUYET-DINH-TREO K-1.17.3 (17:42; P-2310b ghi) | Nguyên văn: " + NGUYEN_VAN + ". "
    "Nội dung (`reports/k1173/QUYET-DINH-TREO.md`): theo khuyến nghị phiên K — K117-D1 A (N2P Chặn ở G2, Cảnh báo ở animatic; N2P-1 (c) cụm dải luôn Cảnh báo); "
    "K117-D3 A (3 sửa luật animatic T3 + năm của miễn Q33 theo khoảng năm hiện trên hình); K117-D5 A, đo trên bản KHÔNG nén; K117-D6 A; "
    "K117-D8 A + mở phiên K làm thước biến cố đo trên video trước G2 T4; K1171-D2 A; K1171-D3 A (T4 dùng §17); K1171-D4 A; "
    "K1173-D2 A; K1173-D3 A (T4: ≤ 27 từ cả tiêu đề / 9 s, ≤ 24 từ / 8 s); K1173-D4 A; K1173-D5 A (T4 vẫn ghi vai `the_chuong` / `the_phuong_phap`); K1173-D6 A (phiên K sau viết miễn + selftest). "
    "**RIÊNG K1173-D1 = B:** duyệt cơ chế ngoại lệ có khai (`r3_ngoai_le` + dòng AUTHORSHIP riêng) cho TẬP SAU; T3 GIỮ hàng EO-DAT-R3 (a) hai shot eo đất một góc TRƯỢT trong hồ sơ, "
    "không ghi \"ý đồ bookend\" cho T3 — dòng này KHÔNG phải dòng ngoại lệ cho shot nào. "
    "Hết hiệu lực (theo căn cứ trong bảng): K117-D4, K117-D7, K1171-D1 "
    "| Chủ dự án chọn B cho K1173-D1 (không hồi tố miễn cho T3), trái khuyến nghị A của phiên K; các dòng còn lại theo khuyến nghị "
    "| Phiên K-1.17.3: bảng quyết định treo, phương án, khuyến nghị; điều phối: đề xuất 17:40 | Chủ dự án |\n")
noi("AUTHORSHIP.md", "".join(au))

# ---------- RIGHTS ----------
BC = "`channel-k2/k2c-t4-02/licenses/`"
BCP = "`reports/p2310b/bang-chung/`"
dong = [
    ("T4-TL-DOORNICK", "*Platte Grondt der Verbrande Stadt London* (Amsterdam 1666; vùng cháy để trắng, theo khảo sát Hollar) — bản đồ hoạt hoá H1-09, H5-03; nguồn ranh cháy cuối (bậc 1)", "Bản đồ khắc", "Rijksmuseum RP-P-OB-82.345 — https://www.rijksmuseum.nl/en/collection/RP-P-OB-82.345 ; ảnh https://iiif.micr.io/cHnSH/full/max/0/default.jpg", "Marcus Willemsz Doornick (xb.)", "Public Domain Mark 1.0 — https://creativecommons.org/publicdomain/mark/1.0/ (trang chụp " + BC + "`rijks-doornick-trang.html, .jpg`)", "Có / Có / Có", "Rijksmuseum, Amsterdam (Public Domain)", "2c51b336901b9745321882d33d98ec5f5de1cb90bca8a9b029946160148203da"),
    ("T4-TL-LUYKEN", "Jan Luyken, *Grote brand van Londen, 1666* (1698) — tham chiếu bậc 4, không dùng làm dữ kiện vị trí", "Bản khắc", "Rijksmuseum RP-P-1896-A-19368-1507 ; ảnh https://iiif.micr.io/ckhwP/full/max/0/default.jpg", "Jan Luyken", "Public Domain Mark 1.0 (trang chụp " + BC + "`rijks-luyken-trang.html, .jpg`)", "Có / Có / Có", "Rijksmuseum (PD)", "cf2ee573633a6f7e5169612d7716c1bfa0082e95e92fb34c45e1ddee92e88f23"),
    ("T4-TL-CHARLES2", "*Portret van Karel II* — thẻ nhân vật nếu lời nhắc nhà Vua (L37)", "Bản khắc chân dung", "Rijksmuseum RP-P-OB-32.684 ; ảnh https://iiif.micr.io/PRhXW/full/max/0/default.jpg", "[không ghi trong nháp]", "Public Domain Mark 1.0 (trang chụp " + BC + "`rijks-charles2-trang.html, .jpg`)", "Có / Có / Có", "Rijksmuseum (PD)", "eed08f8a012f7d6a68268fbd86ad42101a2c3c210968ebb87ea82c42f66b45f1"),
    ("T4-TL-MONUMENT", "*Gezicht op het Monument* (sau 1676) — H2-08 góc khung", "Bản khắc", "Rijksmuseum RP-P-2018-836 ; ảnh https://iiif.micr.io/JJert/full/max/0/default.jpg", "[không ghi trong nháp]", "Trang chụp ghi Public Domain Mark 1.0 (" + BC + "`rijks-monument-trang.html`); nháp ghi CC0 theo JSON không có trong git — cả hai cho dùng tự do", "Có / Có / Có", "Rijksmuseum (PD)", "0f31a9702c4475fe3a4123632dcaf2e52cccdb750066d5e9d9a60178db3ba00e"),
    ("T4-TL-MET-360649", "Hollar, *Prospects of London Before and After the Great Fire* (1666; 2 tấm) — H1-03, H2-12 (then–now)", "Bản khắc", "The Met 17.50.100, .101 — https://www.metmuseum.org/art/collection/search/360649 ; ảnh DP827163.jpg, DP827201.jpg", "Wenceslaus Hollar", "Met API `\"isPublicDomain\": true` (Met Open Access, CC0) — JSON P-2310b tải lại " + BCP + "`met-360649.json`", "Có / Có / Có", "The Metropolitan Museum of Art (CC0)", "d2… xem dưới: 1b34c8c8d0aef76b972ae08a63952f2e1192f594566e8f0cbd662d583de162c2 (tấm 0); b8afc82fbaf191c98825cdfc465c2f7a10742a07e9f0b957ecda73a129030954 (tấm 1)"),
    ("T4-TL-MET-361738", "*London before the Great Fire* (1666–77) — H1-03 dự phòng", "Bản khắc", "The Met 56.581.8 — https://www.metmuseum.org/art/collection/search/361738 ; ảnh DP823346.jpg", "Wenceslaus Hollar", "Met API `\"isPublicDomain\": true` — " + BCP + "`met-361738.json`", "Có / Có / Có", "The Met (CC0)", "d7663fbaf3c462075968580b8a12ce0a150386f183724ab752845c7ad0184c3f"),
    ("T4-TL-MET-395057", "Hollar, *Old St Paul's Cathedral, London, seen from the East* (1656–58) — bản thử T3, H1-13 góc khung; tham chiếu dựng lại Old St Paul's (D6)", "Bản khắc", "The Met 2010.529 — https://www.metmuseum.org/art/collection/search/395057 ; ảnh DP814891.jpg", "Wenceslaus Hollar", "Met API `\"isPublicDomain\": true` — " + BCP + "`met-395057.json`", "Có / Có / Có", "The Met (CC0)", "8d5fe5a6c781397dd3ce4af7b11bf5b22441466cbb31ce3af1a274bd05a7f895"),
    ("T4-TL-YCBA-266", "*The Great Fire of London, with Ludgate and Old St. Paul's* (ca. 1670, sơn dầu) — tham chiếu không khí bậc 4; tư liệu chồng cảnh H1-13 (tuỳ chọn)", "Tranh sơn dầu", "YCBA B1976.7.27 — manifest https://manifests.collections.yale.edu/ycba/obj/266", "unknown artist", "manifest `\"rights\": \"https://creativecommons.org/publicdomain/zero/1.0/\"`; \"Copyright Statement: Public Domain\" — " + BCP + "`ycba-266.json`", "Có / Có / Có", "Yale Center for British Art, Paul Mellon Collection", "abb3b633f24612caa7d591b9906807bba9a38301b278b8a06519bbfad9e9fe97"),
    ("T4-TL-YCBA-40597", "*General View of London during the Great Fire of 1666* (bản in) — tham chiếu bậc 4", "Bản in", "YCBA B1977.14.17854 — manifest https://manifests.collections.yale.edu/ycba/obj/40597", "unknown artist", "như trên (CC0 / Public Domain) — " + BCP + "`ycba-40597.json`", "Có / Có / Có", "Yale Center for British Art, Paul Mellon Collection", "5c8dfe03d80627dbff15742670914bc5b3a72a8004a4424b38cabea21c034a1a"),
    ("T4-TL-NGA-WREN", "John Smith theo Kneller, *Sir Christopher Wren* (NGA 2001.118.55) — thẻ Wren H2-02", "Bản khắc chân dung", "NGA open data `published_images.csv` (depictstmsobjectid 119667) ; ảnh https://api.nga.gov/iiif/e12f2cab-2960-4b05-8658-fac205f5fb37/full/full/0/default.jpg", "John Smith after Godfrey Kneller", "NGA open data: `openaccess = 1` (chính sách NGA Open Access: CC0) — hàng CSV nguyên văn " + BCP + "`nga-wren.json`", "Có / Có / Có", "National Gallery of Art, Washington (CC0)", "abf4493e72b4397d2e97a7d8cb4f8a7808fb34adcadbf7bd7dab624cada1b054"),
    ("T4-TL-LOC-WREN-PLAN", "*A Plan for rebuilding the City of London after the Great Fire in 1666; Designed by that Great Architect Sr. Christopher Wren* (bản khắc TK 18) — H2-02 đặt khớp lên City cháy", "Bản khắc", "Library of Congress 2004678686 — https://www.loc.gov/pictures/item/2004678686/ ; ảnh 3b02873u.tif", "[theo LoC]", "LoC `rights_information`: \"No known restrictions on publication.\" — " + BCP + "`loc-wren-plan.json`", "Có / Có / Có", "Library of Congress, Prints & Photographs Division", "8f9ebde3cc6f33a33d07a04638abf392d46bd7f98f784705b2fcf957cf5ff71a (tif gốc)"),
    ("T4-TL-OGILBY", "Ogilby & Morgan, *A Large and Accurate Map of the City of London* (1676/77) — **D13: chỉ dùng kiểm danh sách phố, KHÔNG lên hình** tới khi xác nhận điều khoản BL cho bản cao", "Bản đồ khắc", "British Library Crace Port. 2.61 qua Wikimedia Commons — https://upload.wikimedia.org/wikipedia/commons/c/ca/Ogilby_and_Morgan_Map_of_London_1677_BL_Maps_Crace_Port_2_61.jpg", "John Ogilby, William Morgan", "Commons: \"CC-PD-Mark\", \"PD-Art (PD-old-100)\"; \"Uploaded by the British Library\" (trang chụp " + BC + "`commons-ogilby-trang.html, .jpg`) — rủi ro vừa", "Chỉ tham khảo nội bộ (không lên hình)", "British Library (PD)", "d2a44427453b35a734fd91dc3fb9b2c33198b63337fc2e5b65589d2157b62a31"),
    ("T4-DL-OSM", "OpenStreetMap: toà, phố, nước, điểm có tên — bbox E −0,130…−0,060, N 51,496…51,526 (21 ô, 156 MB, ngoài git) — toà 2026 (17 815), mạng phố còn giữ (lô nhà 1666), mặt nước 2026, điểm khớp bản đồ", "Dữ liệu không gian", "api.openstreetmap.org /map (tải 23/10/2026)", "OpenStreetMap contributors", "Open Database License (ODbL) 1.0 — https://opendatacommons.org/licenses/odbl/1-0/", "Có / Có / Có (ghi công)", "© OpenStreetMap contributors (ODbL)", "— (dữ liệu tải lại được; xem `scripts/k2ldn/osm_vec.py`)"),
    ("T4-DL-EA-LIDAR", "Environment Agency LiDAR Composite DTM 1 m + First-Return DSM 1 m (2022) — E 529500–535500, N 179500–182500 — địa hình; cao độ 7 824 toà thiếu thẻ", "Dữ liệu không gian", "Environment Agency WCS `environment.data.gov.uk/spatialdata/...` (`scripts/k2ldn/tai_lidar.py`)", "Environment Agency", "Open Government Licence v3.0 — https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/", "Có / Có / Có (ghi công)", "Contains Environment Agency information © Environment Agency and/or database right 2022", "— (tải lại được)"),
    ("T4-DL-OSTN15", "Lưới chuyển đổi OSTN15 (pyproj) — đổi WGS84 → EPSG:27700", "Dữ liệu trắc địa (công cụ)", "cdn.proj.org `uk_os_OSTN15_NTv2_OSGBtoETRS.tif`", "Ordnance Survey", "**[cần kiểm]** câu giấy phép (nháp: \"OSTN15 dùng tự do\")", "Công cụ nội bộ — [cần kiểm] trước G2", "— [cần kiểm]", "—"),
]
# sửa ô SHA dòng MET-360649 cho gọn
dong[4] = dong[4][:8] + ("1b34c8c8d0aef76b972ae08a63952f2e1192f594566e8f0cbd662d583de162c2 (tấm 0); b8afc82fbaf191c98825cdfc465c2f7a10742a07e9f0b957ecda73a129030954 (tấm 1)",)
for d in dong:
    assert len(d) == 9, d[0]
    assert all("|" not in o for o in d), d[0]
bang = "".join("| " + " | ".join(d) + " | 2026-10-23 |\n" for d in dong)
rights = (
    "\n## Kênh 2 — K2C-T4-02 London: tư liệu hình + dữ liệu không gian — trạng thái \"T4 tiền kỳ — đã kiểm giấy phép\" "
    "(phiên P-2310b ghi theo `channel-k2/k2c-t4-02/RIGHTS-NHAP.md` §A–§B, G1 T4 duyệt 23/10/2026 17:42; 23/10/2026)\n\n"
    "> Ngày truy cập gốc: 23/10/2026 (TIEN-KY-T4). Tệp gốc ngoài git, tái tạo bằng `scripts/k2ldn/tai_tu_lieu.py`; SHA-256 tệp gốc theo `channel-k2/k2c-t4-02/licenses/SHA256-TU-LIEU.txt`; bản thu ≤ 2 400 px ở `channel-k2/k2c-t4-02/tu-lieu/`.\n"
    "> **Bằng chứng:** nháp ghi `licenses/<id>.json` cho mọi mục, nhưng các tệp JSON này **không vào git** (`channel-k2/.gitignore` có `*.json`). "
    "Trong git chỉ có trang chụp của 4 mục Rijksmuseum + Commons Ogilby. Với 7 mục Met/YCBA/NGA/LoC, P-2310b **tải lại siêu dữ liệu nguyên văn** từ API/manifest của nơi giữ (23/10/2026 10:56–10:57 UTC, UA dự án, không ảnh) vào `reports/p2310b/bang-chung/` (SHA trong `SHA256SUMS`); giấy phép khớp nháp ở cả 7 mục.\n\n"
    "| Mã | Tài sản | Loại | Nguồn/URL | Tác giả | Giấy phép (trích nguyên câu + link) | Được dùng: YouTube / bán phim / LHP | Ghi công | SHA-256 | Ngày thêm |\n"
    "|---|---|---|---|---|---|---|---|---|---|\n" + bang +
    "\n- **Không dùng / bị chặn:** Leake 1667 (TAMU, Cloudflare 403) — **bỏ theo D12 (chủ dự án 23/10 17:42), dùng Doornick 1666**; Doornick bản Univ. of Michigan — không cần; "
    "Hollar *Long View* 1647 và phương án Evelyn (RMG qua Commons) — rủi ro vừa, chưa dùng; ảnh Crown MOI 1940 — chưa tìm được bản ngoài sê-ri HU (D14: phiên sau tìm, mặc định không ảnh); "
    "không dùng ảnh Mason \"St Paul's Survives\" (T4-G1). OS Open data: chưa dùng.\n"
    "- **Văn bản nguồn** Pepys #4167, Evelyn #42081, *A True and Exact Relation* 1666: đã có ở mục NC-N2P (`N2P-T4-1…3`, P-2110) — không ghi trùng.\n"
    "- **Đầu ra AI bản thử** (T6 tấm N2+ OpenAI 3 lượt, T5 M-d Gemini Omni 1 lượt; sổ `reports/tien-ky-t4/so-ai*.jsonl`): chỉ bản thử, chưa vào phim — không ghi dòng RIGHTS tới khi đầu ra được dùng.\n"
)
noi("RIGHTS.md", rights)

# ---------- COST-LEDGER ----------
p = R / "COST-LEDGER.csv"
dau = next(csv.reader(io.StringIO(p.read_text(encoding="utf-8").split("\n")[0])))
assert len(dau) == 20


def hang(**k):
    h = [""] * 20
    for kk, v in k.items():
        h[dau.index(kk)] = v
    return h


moi = [
    hang(phien="TIEN-KY-T4", tap_hoac_moc="K2C-T4-02 London tiền kỳ M1: treatment, lời nháp v1 (1 593 từ), bảng shot v1 (60 shot), 6 bản thử, RIGHTS nháp, phiếu G1 D1–D18, đề xuất §19",
         cong="G1", ngay="2026-10-23", claude_api_usd="0.82", tran_api_usd="8", model_ghim="claude-sonnet-5-5 (bộ kiểm); gpt-image-2.5-sunburst-2026-09-08; gemini-omni-1.1-flash",
         el_ky_tu_gui="0", el_ky_tu_bo_dem="0", gio_render="5", cham_chu_du_an="1",
         nguon="reports/tien-ky-t4/TIEN-KY-T4-BAO-CAO.md §11 (nhánh k2c-t4-02-tienky @888de179)",
         ghi_chu="Claude API $0,82; OpenAI $0,50 (ảnh N2+ 3 × $0,077 + kiểm $0,27); Gemini $1,02 (Omni 1 lượt 10 s 720p); RunPod $1,90 (RTX 5090 SECURE, số dư 23,08 → 21,18; pod đã xoá); ElevenLabs 0; YouTube 0; tổng API/GPU ≈ $4,24; giờ máy ≈ 5 h (mốc 12 h); chủ dự án duyệt G1 23/10 17:42; ghi sổ bởi P-2310b"),
    hang(phien="K-1.17.3", tap_hoac_moc="Luật 1.17.3: xét 6 khiếu nại BAN-CUOI-T3 (A1–A6), bảng QUYET-DINH-TREO; LOCK 1.17.2 aca05e60 → 1.17.3 d99af8f2",
         cong="K", ngay="2026-10-23", claude_api_usd="0", tran_api_usd="3", model_ghim="không gọi API", el_ky_tu_gui="0", el_ky_tu_bo_dem="0", gio_render="1.2", cham_chu_du_an="1",
         nguon="reports/k1173/K1173-BAO-CAO.md §8 (nhánh checks-1-17-3 @36112c29)",
         ghi_chu="Claude API $0; OpenAI $0; Gemini/ElevenLabs/RunPod/YouTube 0; selftest k1173 42/42; giờ máy ≈ 1,2 h (mốc 4 h); chủ dự án duyệt bảng quyết định 23/10 17:42 (K1173-D1 = B); ghi sổ bởi P-2310b"),
    hang(phien="P-2310b", tap_hoac_moc="Merge checks-1-17-3 + k2c-t4-02-tienky vào main, Kinh thánh §19 + sửa §13.6, §15, sổ (AUTHORSHIP, RIGHTS, BAI-HOC-K2, HANG-DOI), cập nhật main",
         cong="P", ngay="2026-10-23", claude_api_usd="0", tran_api_usd="0", model_ghim="không gọi API", el_ky_tu_gui="0", el_ky_tu_bo_dem="0", gio_render="0.7", cham_chu_du_an="0",
         nguon="reports/p2310b/P2310B-BAO-CAO.md",
         ghi_chu="Claude API 0; OpenAI 0; Gemini 0; ElevenLabs 0; RunPod 0; YouTube 0; tải lại siêu dữ liệu giấy phép miễn phí (Met/YCBA/LoC API, NGA open data CSV 89 MB ngoài git); selftest k11* 3 lượt; giờ máy ≈ 0,7 h (mốc 2 h); ghi sổ bởi P-2310b"),
]
buf = io.StringIO()
w = csv.writer(buf, lineterminator="\n")
for h in moi:
    w.writerow(h)
noi("COST-LEDGER.csv", buf.getvalue())

# ---------- BAI-HOC-K2 ----------
bh = (
    "\n## K35–K39 · Tiền kỳ T4 và gộp nhánh (P-2310b ghi 23/10/2026)\n"
    "| # | Bài học | Số đo | Nguyên nhân | Luật hiện hành |\n|---|---|---|---|---|\n"
    "| K35 | Tiền kỳ dựng hình học mới ở mức thử thì phải có bước khoá look riêng trước animatic | T4 London 1666: khung 1080 bản thử là khối thô (nhà/mái đồng dạng, bến bãi màu cát, bờ sông bậc thang, Old St Paul's thô) so với look T3 đã khoá (`reports/tien-ky-t4/TIEN-KY-T4-BAO-CAO.md` §6) | Tiền kỳ ưu tiên dữ liệu, luật và bản thử kỹ thuật; look T3 gắn với địa hình Gibraltar, không mang sang thành phố mới | **Thêm bước M1b \"khoá look\" (vật liệu, mái, bờ, ánh sáng nướng, mô hình mốc) trước animatic** khi tập dựng hình học mới (chủ dự án 23/10/2026 17:42; phiên LOOK-T4) |\n"
    "| K36 | TAMU IIIF và trang bảo tàng chặn trình duyệt tự động | Leake 1667 (TAMU): Cloudflare 403 cả curl lẫn Playwright; trang Met (Vercel), YCBA (Cloudflare), LoC, NGA chặn chụp trang (TIEN-KY-T4 §12 mục 1, 3) | Chính sách chống bot của nơi giữ | **Bằng chứng giấy phép lấy từ JSON API/manifest/open data của nơi giữ** (nguyên văn, kèm URL, ngày, SHA); không cố vượt chặn; nguồn chỉ có qua trang bị chặn → chọn bản khác (D12: Doornick thay Leake) |\n"
    "| K37 | Commons API trả 429 lặp | TIEN-KY-T4 §12 mục 2: ảnh Crown MOI 1940 chưa tìm được (D14) | Gọi API dày | **Lùi (≥ 6 s, tăng dần) + giảm số lần gọi** (gộp truy vấn, lưu đệm kết quả); hết lượt thì ghi \"chưa tìm được\", không đoán tệp |\n"
    "| K38 | Câu trích nổi tiếng không có trong nguồn gốc | Bludworth \"a woman might piss it out\" không có trong nhật ký Pepys (Gutenberg #4200, tìm toàn văn; DU-KIEN-MOI N2) → bỏ, thay câu Pepys thật \"Lord! what can I do?\" | Câu trích lưu truyền qua sách phổ thông, gán sai nguồn | **Câu trích nổi tiếng phải tra toàn văn nguồn gốc** (tìm chuỗi trong bản toàn văn) trước khi vào lời; không thấy thì bỏ hoặc nói rõ là lời truyền lại |\n"
    "| K39 | `.gitignore` bỏ `*.json` làm mất bằng chứng giấy phép và dữ liệu của tiền kỳ | TIEN-KY-T4: `channel-k2/k2c-t4-02/licenses/<id>.json` (12 mục) và các JSON khác dưới `channel-k2/` không vào git dù báo cáo ghi \"trong git\"; P-2310b tải lại 7 mục Met/YCBA/NGA/LoC vào `reports/p2310b/bang-chung/` | `channel-k2/.gitignore` dòng `*.json`; phiên không đối chiếu `git ls-files` với danh sách tệp báo cáo | **Trước commit cuối: đối chiếu mọi tệp báo cáo nói \"trong git\" với `git ls-files`** (`git check-ignore -v` cho tệp thiếu); bằng chứng giấy phép để ở đuôi không bị bỏ qua hoặc thêm ngoại lệ `!licenses/*.json` (đề xuất cho phiên được giao vùng `channel-k2/`) |\n"
)
noi("channel-k2/BAI-HOC-K2.md", bh)

# ---------- HANG-DOI ----------
p = R / "channel-k2/HANG-DOI.md"
s = p.open(encoding="utf-8", newline="").read()
moc = "## CẬP NHẬT 23/10/2026 (phiên PHAT-HANH-T3: T3, T4) — bổ sung, không thay\n"
assert s.count(moc) == 1
hd = (
    "## CẬP NHẬT 23/10/2026 17:42 (phiên P-2310b: T4) — bổ sung, không thay\n"
    "| Thứ tự | Tập | Đề tài (tên làm việc) | Mức | Trạng thái 23/10 (P-2310b) |\n|---|---|---|---|---|\n"
    "| T4 | K2C-T4-02 | **London — cháy hai lần, làm lại hai lần** | XANH | **G1 duyệt 23/10 17:42; M1b khoá look đang chạy** (phiên LOOK-T4). Tiền kỳ (`k2c-t4-02-tienky` @888de179) đã merge vào `main`: `channel-k2/k2c-t4-02/` (TREATMENT, LOI-NHAP-v1, BANG-SHOT-v1, RIGHTS-NHAP), `reports/tien-ky-t4/`. **D3: GIỮ logline** \"London burned to the ground twice…\" và câu L04 \"London has burned to the ground twice\" như cũ. D11: tấm nền N2+ lập kế hoạch ≤ 15 % tới khi phiên K xét phép (iii); D12: bỏ Leake, dùng Doornick 1666. Luật máy/bản đồ/tranh khắc: Kinh thánh §19. Tiếp theo: M1b → animatic |\n\n"
)
s = s.replace(moc, hd + moc)
p.open("w", encoding="utf-8", newline="").write(s)
print("xong")
