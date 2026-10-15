# TIỀN KỲ T3 — "Gibraltar ↔ La Línea" (K2C-T3-01)

> Phiên Tiền kỳ T3, 15/10/2026. Lệnh chủ dự án duyệt 15/10 (N2); dự phòng: hiệp ước sông Colorado 1922.
> Nhánh `k2c-t3-tienky` từ `origin/main` @ `7255aa4`. **Không merge.**
> Mọi lượt xem là **số công khai YouTube Data API, đọc ngày 15/10/2026 (UTC)**. Mọi tỷ lệ, xếp hạng và trọng số là **tự tính, không phải chỉ số YouTube**.
> Mọi trích dẫn đều chép **nguyên văn** từ tệp tải bằng curl rồi tách chữ. SHA-256 của tệp ghi trong `tienky/neo.json`. Tệp thô để ngoài git.

## 0. Khối điều lệ (chép lệnh, thêm cột thực tế)
| Trường | Lệnh | Thực tế |
|---|---|---|
| Loại phiên | Tiền kỳ (tập T3, bước Đóng gói) | như lệnh |
| Nhánh | `k2c-t3-tienky` từ `origin/main` | `7255aa4`; đã đẩy |
| Tệp được sửa | `channel-k2/k2c-t3-01/TIEN-KY.md`, `channel-k2/k2c-t3-01/tienky/*.json`, `licenses/` | như lệnh. Giấy phép đặt ở `channel-k2/k2c-t3-01/licenses/` (38 tệp), theo quy ước `k2v4-mau/licenses/`. Không sửa mã, `checks/`, `design/`, `scripts/` hay tệp T2. **Không ghi COST-LEDGER, RIGHTS, AUTHORSHIP** (ngoài vùng lệnh; xem §10). |
| Trần | YouTube ≤ 300 đơn vị · Claude API ≤ $2 (ghim model) · ElevenLabs 0 | **294 đơn vị** · **$0,0217** (`claude-haiku-5-5`, 4 lượt, model thực chạy = haiku cả 4) · **0 ký tự** |
| Preflight | bắt buộc | `verify.sh`: 9 PASS, 4 FAIL không liên quan (three.js, tifffile/pyshp, k2v node_modules, Freesound). `tools/preflight.sh --range origin/main..HEAD`: **ĐẠT**; `lock.py --verify`: **KHỚP** (§11) |
| Điều kiện dừng | xong việc → đẩy → dừng | (1) xong việc |

## 1. Tóm tắt và khuyến nghị
**Khuyến nghị: ĐI TIẾP Gibraltar, không chuyển sang Colorado.** Kèm 4 điều chỉnh bắt buộc so với Teardown §8:
1. **Bỏ tiêu đề làm việc "The Fence Came Down".**
   - Nguồn gốc cho thấy: hàng rào cũ được gỡ từng đoạn, và một hàng rào mới loại "no-climb" đã dựng sẵn cách vài mét, kéo từ biển tới sân bay. Chỉ khoảng 150 m quanh vòng xoay là để trống (thông cáo HMGoG 517/2026).
   - Theo Điều 7 hiệp ước, việc gỡ mọi rào cản đi "theo kế hoạch thực thi".
   - Cái thật sự chấm dứt từ 15/07 là **kiểm soát thường quy ở biên giới đất liền**.
2. **Hiệp ước mới "áp dụng tạm thời" từ 15/07/2026, chưa có hiệu lực chính thức.**
   - Nghị viện châu Âu dự kiến biểu quyết đồng ý ngày **14/12/2026**. Phía Anh còn thủ tục CRaG.
   - Lời, hình và mô tả đều phải ghi "as of".
3. **"15 000 người, hơn một nửa lực lượng lao động" là lời của chính phủ Anh.**
   - Theo Thống kê Gibraltar: **14 112 việc làm do người cư trú ở Tây Ban Nha nắm, trên 32 206 việc làm** (10/2025), tức **43,8 %**.
   - Lời dùng số của Thống kê Gibraltar.
4. **Bỏ "6,8 km²"** vì không có nguồn chính thức. Tài liệu LHQ A/AC.109/2026/8 ghi: **5,8 km² theo Anh, 4,8 km² theo Tây Ban Nha**.

**Lý do đi tiếp:**
- **Neo đúng ở phần cốt lõi.** Hiệp ước ký 14/07, các bên cùng ký, nội dung đã kiểm từ văn bản. Neo còn tạo một **"điều cần theo dõi"** có ngày cụ thể: biểu quyết ở Nghị viện châu Âu 14/12.
- **Nghịch lý mạnh hơn bản Teardown** nhờ một cú lật có số liệu gốc:
  - Gibraltar tính GDP/người trên **dân cư trú**, trong khi khoảng 44 % việc làm do người sống ở La Línea và vùng lân cận nắm.
  - La Línea có thất nghiệp **28,6 %** (INE, năm 2024), **cao nhất trong 113 đô thị** INE đo; toàn quốc là 11,34 %.
- **Cầu đạt điều kiện 1 (Cầu-ngách).**
  - 0/12 kênh lớn và kênh trong Teardown có video về Gibraltar.
  - Khoảng trống đạt: 0/5 video đầu có dấu hiệu dùng số liệu có nguồn.
- **Tài sản hình đủ cho bản đồ nổi và zoom nhiều tầng** (Copernicus DEM, Sentinel-2, PNOA): giấy phép thương mại rõ, mẫu đã tải thử.

**Điểm yếu cần biết:**
- **Cầu-bền dạng dài không đạt.** Teardown ghi "Cầu-bền CÓ 4,06 triệu", nhưng video đó dài 4 phút, mà luật chỉ tính video ≥ 8 phút. Cầu bền chỉ thấy ở dạng ngắn (6,2 triệu, 4,1 triệu, 2,8 triệu).
- **Góc "giàu dù không tài nguyên" đã có người làm dạng dài trong 2026:** Resource Grab (19,6 nghìn lượt), FIRSTMADE (2 ngày tuổi), Travel Explorer (470 nghìn lượt, dạng du lịch).
  - Khác biệt của mình: **cặp tương phản qua cổng**, **hiệp ước 2026**, **hồ sơ thật**, và **cú lật về mẫu số**. Cả 7 video cùng góc đều không có dấu hiệu dùng nguồn số liệu (Haiku đọc mô tả).
- **Footage lưu trữ Gibraltar gần như trống.**
  - Không dùng được: IWM, British Pathé, Reuters, Gibraltar National Archives.
  - Dùng được: ảnh LoC, tranh CC0 (Rijksmuseum, The Met), ảnh vệ tinh/hàng không. Phần "hồ sơ thật" dựa vào văn bản gốc có tô dòng.
- **Mức rủi ro: VÀNG đầy đủ, không phải "VÀNG nhẹ"** (§7).
  - Lý do: chủ quyền, thời sự còn đang diễn biến (phê chuẩn chưa xong), và một cuộc bầu cử ở Tây Ban Nha có thể rơi vào cùng cửa sổ phát hành. Ngày bầu cử chỉ có nguồn thứ cấp, CHƯA XÁC MINH GỐC.

**Colorado:** không chạy bước 1 đầy đủ vì neo Gibraltar không sai ở cốt lõi. Phiên phụ đã kiểm sẵn 2 neo dự phòng:
- Record of Decision của Interior/USBR ngày **21/08/2026** (khung 2027–2036, các bang không đạt đồng thuận). Câu trích: *"Unfortunately, as of the publication of this Record of Decision (ROD), consensus on long-term operations has not been reached."*
- Hiệp ước 1922 chia **7,5 triệu acre-feet/năm** cho mỗi lưu vực.

## 2. Bước 1 — Xác minh neo bằng nguồn gốc (chi tiết: `tienky/neo.json`)
| # | Neo (Teardown) | Kết luận | Nguồn gốc · as of | Trích nguyên văn |
|---|---|---|---|---|
| N1 | Ký 14/07/2026 | **ĐÚNG** | Thông cáo FCDO (gov.uk) · 14/07/2026 | "following the signing of the historic UK-EU Treaty on Gibraltar in Brussels today (14 July)" |
| N2 | "Có hiệu lực" 15/07 | **ĐÚNG khi gọi là áp dụng tạm thời** | Explanatory Memorandum CP 1645 §5.6 · 14/07/2026 | "the UK and the EU agreed to apply the Treaty provisionally from 15 July 2026" |
| N3 | Trạng thái phê chuẩn | **CHƯA HIỆU LỰC** | European Parliament Legislative Train 2026/0058(NLE) · đọc 15/10/2026 | "Indicative plenary sitting date is set for 14 December 2026." |
| N4 | Gỡ hàng rào 15/07 | **SAI MỘT PHẦN** | HMGoG 517/2026 · 02/07/2026; Hiệp ước Điều 7 | "As the old chain-link and barbed-wire fencing comes down, a new, high-security fence line has already been erected only a few metres away." |
| N5 | Nội dung chính | **ĐÚNG** | EM CP 1645 | "It does not formally integrate Gibraltar into the Schengen Area, the EU Single Market, or the EU Customs Union…" |
| N6 | ~15 000 người/ngày, "hơn một nửa" | **ĐÚNG về cỡ, LỆCH về tỷ lệ** | Employment Survey 2025 (Thống kê HMGoG), Bảng 2.4 · 10/2025 | "Frontier Worker: an employee who is normally resident in Spain and is employed in Gibraltar." Tổng 14 112 / 32 206 |
| N7 | GDP/người "thuộc nhóm cao nhất thế giới" | **SỐ TỰ CÔNG BỐ, PHẢI KÈM 3 CAVEAT** | Thống kê HMGoG (£80 885 năm 2024/25, dự báo); Thủ hiến, ngân sách 07/07/2026 (£85 145, quy ra $126 015, "third") | "[2] Sterling figures are converted to US dollars at £1 = US$1.48, the twenty-year average sterling-to-dollar exchange rate" |
| N8 | Thất nghiệp La Línea (INE/SEPE) | **ĐÚNG — MẠNH** | INE Indicadores Urbanos ed. 2025 (UA121870) · số 2024 | "Línea de la Concepción, La. Tasa de desempleo (Porcentaje). Total." → 28,6; toàn quốc 11,34. Phương pháp: "Fuente: Encuesta de Población Activa (EPA). Registro de parados por municipios del Servicio Público de Empleo Estatal." |

**Ai công bố GDP/người và theo phương pháp nào:**
- Văn phòng Thống kê của chính quyền Gibraltar (HMGoG Statistics Office) công bố bảng "National Income".
- Số liệu là GDP giá yếu tố; năm 2023/24 là ước tính sơ bộ, năm 2024/25 là dự báo. Từ năm 2012/13, chuỗi đã tính lại theo Census 2022.
- Con số "thứ 3 thế giới" là của Thủ hiến:
  - đặt Gibraltar vào bảng IMF WEO (04/2026), trong khi IMF không xếp Gibraltar;
  - quy sang đô-la theo tỷ giá trung bình 20 năm;
  - chính ông nói: "these international comparisons are not an exact science".

**Thất nghiệp La Línea:**
- Đây là **ước tính của INE** (kết hợp vi dữ liệu EPA và sổ đăng ký SEPE theo đô thị), không phải số đếm của SEPE.
- Số SEPE tháng 09/2026 chưa đọc trực tiếp; tuỳ chọn bổ sung ở G1.
- INE không có số gộp cho "Campo de Gibraltar". Dùng La Línea (28,6 %) và Algeciras (22,6 %).

## 3. Bước 2 — Hồ sơ cầu (`tienky/cau.json`, `kho-kenh.json`, `binh-luan.json`, `khoang-trong.json`)
**Cách đo:**
- 2 lượt `search.list` (type=video, order=relevance, 50 kết quả, en/US, không giới hạn ngày):
  - S1 "why is Gibraltar rich";
  - S2 "why is Gibraltar British|Gibraltar Spain border". Câu hỏi thứ ba gộp vào S2 bằng toán tử `|` để giữ trần 300 đơn vị.
- `videos.list` cho 98 video.

| Nhãn (LUAT-CHON-DE-TAI) | S1 "why rich" | S2 "British / border" | Kết luận |
|---|---|---|---|
| Cầu-bền (top 5 video dài ≥ 8 phút có video ≥ 500 nghìn) | lớn nhất 469 932 (Travel Explorer) | lớn nhất 296 597 (DW News) | **KHÔNG ĐẠT** (sửa Teardown) |
| Nổ-mẫu (≥ 500 nghìn trong 90 ngày) | không | không (Why Is Gibraltar British 6,2 triệu, ngắn 1,7 phút, **132 ngày** tuổi) | KHÔNG |
| Cầu-ngách (video dài 10–50 nghìn trong 90 ngày) | Resource Grab 19 586 (10,2 phút, 37 ngày); Impossible Places 31 653 (36,5 phút, 12 ngày) | GB News 18 381 (12,6 phút, 67 ngày) | **ĐẠT** |
| Cầu dạng ngắn bền | — | 6 226 746 · 4 058 323 · 2 842 760 (≤ 4,1 phút) | cầu tò mò lớn ở dạng ngắn → Short |

- **Chỉ số sát ngưỡng:** Travel Explorer 469 932 lượt, thấp hơn ngưỡng Nổ-mẫu/Cầu-bền 500 nghìn khoảng 6 %. Ngay ngoài dải ±5 %, nhưng ghi ra để minh bạch.
- **Bình luận** (100 bình luận hàng đầu × 3 video, Haiku gắn nhãn 294/294):
  - **27, 25 và 22** bình luận thuộc loại hỏi, yêu cầu, sửa sai hoặc tranh luận nguyên nhân.
  - Số câu hỏi/yêu cầu thuần là 14, 8 và 11.
  - Chủ đề nặng ký nhất: chủ quyền (982 ở VisualPolitik), hiệp ước/Brexit (1 005 ở DW), thuế + tài chính (691 ở VisualPolitik).
- **Khoảng trống:** 0/5 video đầu của S1 có dấu hiệu dùng số liệu có nguồn (ngưỡng ≤ 1/5) → **ĐẠT**.
- **Kiểm kho** (toàn bộ uploads, 12 kênh, 3 832 video):
  - Wendover, RealLifeLore, PolyMatter, Economics Explained, Half as Interesting, CaspianReport, Business Casual, Real Engineering, Asianometry, FoN, GoDocs, Geography Effect: **0 video Gibraltar**.
  - Video kề, đã đọc mô tả, không nhắc Gibraltar:
    - Geography Effect "Why Spain's Richest Region Became Its Poorest" (08/2026, 275 nghìn): Andalusia. Tránh lặp khung "đất tập trung, giới tinh hoa".
    - RealLifeLore "The Ceuta Situation is Insane" (02/2026, 470 nghìn).
    - Economics Explained: Monaco, Liechtenstein, Luxembourg, Short "tax haven".
  - **Giới hạn:**
    - Modern MBA không quét, để giữ quota.
    - Uncover History: handle `@UncoverHistory` trả về một kênh khác, nên dựa vào phép loại trừ cùng ngày của Teardown (104 tiêu đề, không có Gibraltar).

## 4. Bước 3 — Nghịch lý, cặp tương phản, nhân vật, chương

### 4.1 Nghịch lý một câu
> **"A rock with no farmland and no river reports one of the highest outputs per person on Earth — and the Spanish town at its gate has the highest unemployment of any city Spain measures. Part of the Rock's number is made by that town's workers."**

- Vế 1: GDP/người tự công bố (C10–C12), có caveat đi kèm trong lời.
- Vế 2: INE Indicadores Urbanos 2025 — La Línea 28,6 %, cao nhất trong 113 đô thị (C14).
- Vế 3 (cú lật): ~14 100 việc làm ở Gibraltar do người sống ở Tây Ban Nha nắm, nhưng họ không nằm trong mẫu số "per head" (C08, C09, C13).

### 4.2 Cặp tương phản (mã màu cố định cả tập — đề xuất, chờ V/chủ dự án)
| Phía | Ai | Số neo | Màu đề xuất |
|---|---|---|---|
| A | Gibraltar (5,8 km² theo Anh, 4,8 theo TBN; 37 936 dân cư trú — Census 2022) | GDP £3,25 tỷ dự báo; £85 145/người (tự công bố) | vàng đất ấm |
| B | La Línea de la Concepción (Cádiz) | thất nghiệp 28,6 % (2024); thu nhập ròng 11 553 €/người (2023) | xanh xám lạnh |
| Dòng nối | Người lao động qua biên giới | 14 112 việc làm (10/2025) | trắng (nét đứt chuyển động) |

### 4.3 Nhân vật người thật có hồ sơ (3–5)
| # | Nhân vật | Vai trong mạch | Hồ sơ | Ảnh/tranh | Ghi chú rủi ro |
|---|---|---|---|---|---|
| 1 | **Admiral Sir George Rooke** (1650–1709) | Ch.1 — muốn một căn cứ ở cửa Địa Trung Hải; chiếm Rock 1704 nhân danh Đại công tước Charles; Anh giữ cho mình | C17 | chân dung Michael Dahl (bản trên Commons/RMG — xem §6, kiểm từng tệp) | người đã mất; trung tính |
| 2 | **Nhóm "the frontier workers"** (A-lite, nhóm người) — 14 112 việc làm, 9 374 là công dân Tây Ban Nha | Ch.4 — muốn lương Gibraltar, sống ở La Línea; bị cản bởi hàng đợi biên giới, rồi Brexit/EES; kết cục: hiệp ước 15/07 | C08, C09 | A-lite (đạo cụ: thẻ đi làm, xe máy, mũ bảo hiểm) | không mặt người thật; không gắn tội phạm/buôn lậu |
| 3 | **Chính quyền Tây Ban Nha 1969** (quyết định đóng cổng) — kể bằng cơ quan + năm, không cá nhân hoá Franco ngoài một câu có nguồn | Ch.2 — muốn ép chủ quyền; đóng biên giới 1969–1985; kết cục: Gibraltar tự tìm nghề mới | C19 (phiên phụ A) | ảnh lưu trữ cổng đóng (chỉ khi có giấy phép rõ; IWM không dùng) | lịch sử, có phán quyết lịch sử rõ; trình bày quan điểm hai phía |
| 4 | **Fabian Picardo** (Thủ hiến Gibraltar 2011–nay, **còn sống**) | Ch.3/Ch.7 — người công bố con số "third in the world"; chính ông nói "not an exact science" | C11, C12 | chỉ ảnh chính thức có điều khoản rõ (chưa tìm được — dùng chữ/lời trích) | LUAT-NOI-DUNG-G §6: chỉ trích nguyên văn có nguồn, không suy động cơ |
| 5 | **Juan Franco** (Thị trưởng La Línea, **còn sống**) — tuỳ chọn | Ch.4 — tiếng nói phía La Línea | **chưa có trích dẫn gốc** (chỉ được nhắc trong thông cáo 517/2026) | không | cần nguồn gốc (Ayuntamiento) trước G1; nếu không có → bỏ |

### 4.4 Chương đề xuất (Kinh thánh §3: 9–11 phút, tới 12; ~150 từ/phút)
| # | Tên chương (EN, gợi tò mò) | Nhân vật | Nội dung chính (claim) | Hình (lăng kính) | Thời lượng |
|---|---|---|---|---|---|
| 0 | *Midnight at the Gate* (móc ≤ 45 s) | đám đông qua cổng 15/07 | tin mới (C01–C03) → nghịch lý (C10, C14) → 2 sự thật bất ngờ (không sông/ruộng; 4 trong 10 việc làm do người từ Tây Ban Nha) → một con số (28,6 %) → câu hỏi trùng tiêu đề → hứa cú lật ("the number that makes Gibraltar look rich is partly made in La Línea") | zoom nhiều tầng: bản đồ nổi eo biển → ảnh vệ tinh eo đất → cảnh 3D cổng/đường băng | 0:45 |
| 1 | *A Rock Without a Hinterland* | George Rooke | 1704 (C17), Utrecht 1713 "without any open communication by land" (C18), dưới 6 km² — nêu cả số của Anh và TBN (C20, C20b) | relief sepia, hạm đội sticker, khối Rock 3D | 1:30 |
| 2 | *The Gate Closes* | chính phủ TBN 1969; người lao động bị cắt | đóng "June 1969", ~4 600 lao động ngày bị chặn, mở bộ hành 1982, mở hẳn 1985 (C19, C19b); trưng cầu 1967 (C31); Gibraltar sống nhờ căn cứ | ảnh lưu trữ có giấy phép; cổng 3D đóng | 1:30 |
| 3 | *Selling Rules, Not Things* | Thủ hiến (trích) | thuế doanh nghiệp theo luật (C22), không VAT → "transaction tax" (C06), cờ bạc trực tuyến bằng **giấy phép và số việc làm** (C23, C24), không dùng chữ "tax haven" như khẳng định; nêu trước tranh luận khán giả (thuế, tài chính, cờ bạc) và trả lời bằng số | hàng xu thuế; biểu đồ GDP 2010→2026 (C10) | 1:45 |
| 4 | *The Workers Who Make the Average* | nhóm frontier workers | 14 112 việc làm (C08), 9 374 người TBN (C09), mẫu số "resident" (C11) → cú lật; La Línea 28,6 % (C14), thu nhập 11 553 € vs 14 807 € (C15) | dòng người A-lite chảy qua đường băng mỗi sáng; hai cột so sánh | 1:45 |
| 5 | *The Hard Border That Almost Happened* | cử tri Gibraltar 2016 | 95,91 % ở lại EU (C25); TCA không gồm Gibraltar (C04); EES đe doạ hàng đợi (C05) | relief, vạch đỏ biên giới dày lên | 1:15 |
| 6 | *What Changed on 15 July* | các bên ký (Doughty, Šefčovič, Albares, Picardo — chỉ tên + vai) | không kiểm tra thường quy ở biên giới đất; kiểm tra kép ở sân bay/cảng (C02); liên minh thuế quan (C05b); transaction tax 15→16→~17 % (C06); hàng rào cũ gỡ từng đoạn, hàng rào mới phía sau (C03); Điều 2 chủ quyền (C07) | cảnh 3D đặc trưng: hàng rào cũ tan ra, hàng rào mới đứng; mô hình sân bay hai lớp kiểm tra | 1:45 |
| 7 | *The Honest Part — and What to Watch* | — | 3 caveat GDP/người (C11, C12, C13); hiệp ước mới **áp dụng tạm thời**, EP biểu quyết dự kiến 14/12/2026 (C26); có thể chấm dứt với báo trước 12 tháng (C27); cơ chế phạt thuế gián thu (C28); hai lập trường chủ quyền (C29, C30, C31, C32) | bảng điểm tổng kết (scorecard) | 1:15 |
| — | Kết | quay về cổng lúc nửa đêm | câu chốt nghịch lý; dẫn sang tập kế (chuỗi "border economies" hoặc Colorado) | | (gộp ch.7) |

**Tổng ≈ 11:30** (trong khung "tới 12"). Lời mời đăng ký nhẹ cuối ch.2 (~3:45). 8 chương (0–7).

### 4.5 Nêu trước các nguyên nhân khán giả hay cãi (từ `tienky/binh-luan.json` + Teardown §3)
| Khán giả sẽ nói | Trọng số bình luận (tự tính) | Trả lời trong lời bằng |
|---|---|---|
| "It's just a tax haven" | VisualPolitik: chủ đề thuế+tài chính 691; ý được thích nhất (262) là "thành công nhờ thiên đường thuế" | thuế suất theo luật (C22), tuyên bố chung EU–UK về "harmful tax regimes" 14/07/2026 (C21), thu thuế doanh nghiệp £252 triệu (C24b) — để khán giả tự kết luận; **không** tự gọi là "tax haven" |
| "Spain wants it back / what about Ceuta?" | VisualPolitik: chủ quyền 982 (lớn nhất) | trình bày hai lập trường bằng nguồn chính thức (C29 Anh, C30 TBN), Điều 2 hiệp ước; Ceuta chỉ một câu, không làm trục |
| "Online gambling" | DW: 104 | số việc làm ngành cờ bạc (C23) + cơ chế giấy phép (C24), không nêu tên công ty |
| "It's the military base / UK subsidy" | VisualPolitik: quân sự 74 | MoD 500 việc làm (C08b) — nhỏ so với 32 206 |
| "Is it in Schengen now? Do Brits need EES?" | DW: 168 + 92 + 69 | C05: không gia nhập Schengen/Thị trường chung; cư dân Gibraltar miễn EES/ETIAS (Điều 42) |
| "Gibraltar isn't Europe's southernmost point" | DW: 210 + 166 (sửa sai) | không nói "southernmost" trong lời |

## 5. Bước 4 — Danh mục claims sơ bộ (`tienky/claims.json`: **44 claim**, 14 claim nhạy cảm)
Mỗi claim có nguồn gốc, URL, ngày "as of" và trích nguyên văn. Các nhóm:

| Nhóm | Claim | Nguồn chính |
|---|---|---|
| Hiệp ước 2026 | C01–C07, C03b, C05b, C06b, C26–C28, C34 | gov.uk (FCDO), văn bản hiệp ước MS No.9/2026, EM CP 1645, Hansard 26/02/2026, Nghị viện châu Âu |
| Lao động, GDP | C08–C13, C08b, C09b, C12b, C35 | Thống kê HMGoG (Employment Survey 2025, National Income), ngân sách 536/2026 |
| La Línea, Tây Ban Nha | C14–C16 | INE (UA121870, UA129043, UA121855, UA129028, CRE47377) |
| Lịch sử, chủ quyền | C17–C20b, C29–C33 | Gibraltar National Museum, Hansard 1968/1969, HMGoG, LHQ A/AC.109/2026/8, Hiến pháp 2006, MAEUEC |
| Thuế, cờ bạc, tài chính | C21–C24b | Tuyên bố chung 14/07/2026, Income Tax Office, LHQ §32, Employment Survey |
| Brexit | C25 | Electoral Commission (CSV, SHA `a0592dc3…`) |

**Claim nhạy cảm và cách nói:**
- **Chủ quyền** (C07, C17, C18, C20, C29–C33): luôn đi cặp lập trường Anh ↔ Tây Ban Nha, mỗi phía có nguồn riêng. Không dùng chữ "colony" hay "occupied" như lời của kênh; chỉ được dùng khi trích nguyên văn và nêu rõ ai nói.
- **"Thiên đường thuế"** (C21, C22, C24b): chỉ nói bằng thuế suất theo luật (10 % → 12,5 % → 15 %), văn bản tuyên bố chung về "harmful tax regimes", và số thu. Kênh không tự gán nhãn.
- **Tên gọi thuế mới** (C06, C06b): MÂU THUẪN tên gọi. Anh: "not apply VAT". Tây Ban Nha: "impuesto indirecto equivalente al IVA". Nêu cả hai cách gọi.
- **GDP/người** (C11–C13): luôn nói "Gibraltar's government says" và đặt caveat ngay trong cùng chương.
- **Thời sự** (C26): bắt buộc "as of".

**Không dùng** (lý do trong `claims.json` → `khong_dung`):
- "6,8 km²";
- ngày 4/8/1704 và 8/6/1969 (nguồn mâu thuẫn; nói "1704", "June 1969");
- "the fence came down on 15 July";
- "over half of the workforce" như sự thật;
- "tax haven" như khẳng định của kênh;
- "southernmost point of Europe";
- số nhà cái được cấp phép (trang Gambling Division trả 403).

## 6. Bước 5 — Tài sản hình có giấy phép (`tienky/tai-san.json`: 28 mục; `licenses/`: 38 tệp)

| Tầng hình | Tài sản dùng được | Giấy phép · ghi công | Content ID |
|---|---|---|---|
| Bản đồ nổi | **Copernicus DEM GLO-30** tile N36 W006 (37,95 MB, SHA `3995ee21…`); IGN MDT (chỉ phía Tây Ban Nha); SRTM dự phòng | Copernicus WorldDEM-30: thương mại được. **Phải ghi:** "produced using Copernicus WorldDEM-30 © DLR e.V. 2010-2014 and © Airbus Defence and Space GmbH 2014-2018 provided under COPERNICUS by the European Union and ESA; all rights reserved", kèm câu miễn trách | THẤP |
| Vệ tinh | **Sentinel-2 L2A** 30STF, 24/09/2026, mây 1,27 % (74 cảnh mây < 5 %) | "Contains modified Copernicus Sentinel data 2026" | THẤP |
| Ảnh hàng không | **PNOA 2025 0,15 m** (La Línea, đường băng, phần bắc Gibraltar; phía nam ~36,14° trống) | CC BY 4.0. **Ghi trên hình:** "Obra derivada de PNOA 2025 CC-BY 4.0 scne.es". Ảnh của Tây Ban Nha chụp Gibraltar → nêu ở G1 | THẤP |
| Chân dung Rooke | **Rijksmuseum RP-P-OB-33.529** (mezzotint theo Dahl, CC0) — chọn chính; YCBA B1977.14.10207 (CC0) — dự phòng | CC0 | THẤP |
| Tranh, bản đồ cổ | Rijksmuseum RP-P-OB-83.181 (chiếm Gibraltar 1704, CC0); LoC 2016646782 (Nürnberg 1705); The Met 12828 Trumbull, 18113 Eliott, phác thảo Copley (CC0) | CC0 / "No known restrictions" | THẤP |
| Ảnh lưu trữ | **LoC 2025710366 "Gibraltar. Neutral ground" (1900–1910)** — rất sát chủ đề; LoC 2020680546, 2020680537, 94512284 | "No known restrictions on publication." (94512284: lưu ý quyền ngoài Mỹ) | THẤP |
| Footage | Pexels/Pixabay (điều kiện: xem từng clip, logo); Flickr CC BY-SA (chưa đối chiếu gốc) | Pexels/Pixabay License | TRUNG BÌNH |
| **KHÔNG dùng** | IWM (Non Commercial), British Pathé/Reuters (trả phí), Periscope/RKO, Prelinger Wathen (không có giấy phép), Gibraltar National Archives và ảnh HMGoG (cấm thương mại khi chưa có văn bản), RMG BHC2978 và NPG Dahl (CC-BY-NC-ND / không đọc được), Gallica Boudan | — | CAO hoặc không rõ |

**Bản đồ vector:**
- `design/k2v/data` chỉ có Natural Earth 50m/110m, **không có polygon Gibraltar**.
- Bản 10m có polygon riêng (id 292, 8 đỉnh).
- Biên giới qua eo đất là **vùng tranh chấp** (QUAN-TRI-RUI-RO §6.7). Đề xuất ở G1: dùng mặc định Natural Earth 10m và **không tự vẽ lại** đường biên. Cần V/P cấp dữ liệu 10m.

**Rủi ro Content ID:**
- Thấp cho tầng bản đồ, vệ tinh và tranh CC0.
- Trung bình cho footage stock.
- Footage lưu trữ Gibraltar có quyền rõ gần như **không có**: tỷ trọng footage dự kiến **≤ 8 %**, còn xa trần 20 %.

## 7. Bước 6 — Mức rủi ro (QUAN-TRI-RUI-RO)
**Đề xuất: VÀNG đầy đủ** (không phải "VÀNG nhẹ"). Phải đủ cả 6 điều kiện VÀNG, và chủ dự án duyệt ở G1.

**Lý do nâng mức:**
1. Tranh chấp chủ quyền hai phía; LHQ vẫn xếp Gibraltar là lãnh thổ chưa tự quản.
2. Thời sự **chưa khép**: hiệp ước mới áp dụng tạm thời, Nghị viện châu Âu biểu quyết ngày 14/12/2026, và có thể rơi vào giai đoạn bầu cử Tây Ban Nha (chưa xác minh gốc).
3. Chạm thuế, tài chính và cờ bạc trực tuyến, nên cần câu miễn trừ tài chính.
4. Bình luận trên video cùng đề tài thiên về chủ quyền, Ceuta, Morocco → bật luật lọc bình luận (§1.2) ngay từ video.

Không có yếu tố ĐỎ: không quy lỗi cho cá nhân, không có vụ kiện làm trục.

**Thứ tự VÀNG:** T2 (đóng tàu) là VÀNG → T3 là VÀNG thứ hai liền nhau, **vẫn hợp luật** (không quá 2 tập VÀNG liền). Tập kế phải là XANH; Colorado là XANH.

**Câu chữ cần tránh (lời, tiêu đề, thumbnail, mô tả):**

| Tránh | Dùng thay |
|---|---|
| "The fence came down" / "the border is gone" | "routine checks ended" / "the old fence began coming down" |
| "Gibraltar joined Schengen" | "not part of Schengen; checks moved to the airport and port" (C05) |
| "the treaty is in force" | "provisionally applied, as of [date]" (C26) |
| "tax haven", "offshore paradise", "Spain's poorest town" | thuế suất theo luật; "the highest unemployment of 113 cities INE tracks" (C14) |
| "Gibraltar is the richest / third richest place on Earth" | "Gibraltar's government says it ranks third — using a twenty-year average exchange rate" (C11, C12) |
| "Spain occupied" / "Britain stole" / "colony" (lời của kênh) | "captured in 1704" (C17); trích hai lập trường (C29, C30) |
| "smugglers", "tobacco smuggling" (gắn với người lao động) | chỉ nói cơ chế truy xuất thuốc lá của hiệp ước, không gắn với nhóm người |
| "southernmost point of Europe" | không dùng |
| cờ làm điểm nhấn trên thumbnail | không cờ (Teardown §9) |

## 8. Bước 7 — Gói sơ bộ
**Tiêu đề** (Why + nơi + tương phản, ≤ 60 ký tự; số trên thumbnail lấy từ claims):

| # | Tiêu đề | Ký tự | Ghi chú |
|---|---|---|---|
| 1 | **Why Gibraltar Got Rich and the Town Next Door Didn't** | 52 | đề xuất chính; lời trả lời được (C10, C14, C15) |
| 2 | Why Is Gibraltar So Rich While La Línea Isn't? | 46 | tên La Línea ít người tìm; dùng cho Test & Compare |
| 3 | Why Gibraltar Is Rich and the Town Across the Gate Isn't | 56 | "gate" khớp cảnh mở đầu; tránh chữ "fence" |

**Thumbnail** (mẫu brief Teardown §9):
```
THUMBNAIL BRIEF — K2C-T3-01
[A] BẢN ĐỒ TƯƠNG PHẢN
- Nền: relief Copernicus GLO-30 eo đất Gibraltar–La Línea (render của mình), tầm thấy rõ hình Rock + vịnh ở 168×94.
- Chủ thể: Gibraltar tô vàng đất bão hoà, La Línea xanh xám lạnh; viền trắng, quầng ≤ 0,2.
- Tương phản: vạch chia dọc đỏ đặt ĐÚNG tuyến cổng/đường băng (không vẽ biên vùng tranh chấp ngoài Natural Earth 10m).
- Chữ (1 hộp, nền tối): A1 "28.6% JOBLESS" đặt phía La Línea (C14) | A2 (chữ khác) "SAME GATE".
- Biểu tượng (≤ 2): sticker người đi làm (A-lite, mũ bảo hiểm xe máy) đi từ phía xám sang phía vàng; chồng xu phía vàng.
[B] CƠ CHẾ LỘ RA (không chữ)
- Cảnh 3D tự dựng: đường băng cắt ngang đường vào; dòng người A-lite đi bộ băng qua đường băng về phía Rock lúc bình minh;
  nửa trái (sepia, 1969) cổng đóng, nửa phải (tự nhiên, 2026) cổng mở — hàng rào mới mờ phía sau (đúng sự thật, C03).
- Không mặt người làm tiêu điểm, không cờ, không logo hãng bay.
Chung: tiêu đề hỏi, thumbnail cho thấy; mọi số có trong video; lề 5 %; tránh góc dưới-phải.
Ghi: nền = relief GLO-30 + Sentinel-2 S2A_30STF_20260924; mã màu A vàng đất / B xanh xám / dòng nối trắng.
Test & Compare: A1, A2, B.
```
**Short đi kèm:** tận dụng cầu dạng ngắn rất lớn (6,2 triệu / 4,1 triệu / 2,8 triệu lượt cho "Why is Gibraltar British"). Short "Why do 14,000 people cross this runway to work?" (C08, C33) dẫn về video dài.

## 9. Chi phí (`tienky/cost.json`)
| Mục | Trần | Thực tế |
|---|---|---|
| YouTube Data API | 300 | **294**: search 200 · playlistItems 82 · videos 5 · channels 4 · commentThreads 3 (cache, sổ `quota.jsonl` ngoài git) |
| Claude API | $2 (ghim `claude-haiku-5-5`) | **$0,0217** · 4 lượt (khoảng trống 1, bình luận 3) · model thực chạy = `claude-haiku-5-5` cả 4 |
| ElevenLabs | 0 | **0** |
| WebSearch | — | ~10 lượt (không thuộc quota YouTube) |
| Token | trần mềm | 2 phiên phụ Claude Code (nguồn lịch sử, giấy phép tài sản); không qua API trả tiền |

## 10. Tệp đã ghi và đề xuất ngoài vùng
- **Đã ghi:**
  - `channel-k2/k2c-t3-01/TIEN-KY.md`;
  - `tienky/`: `neo.json`, `cau.json`, `kho-kenh.json`, `binh-luan.json`, `khoang-trong.json`, `claims.json`, `tai-san.json`, `cost.json`. Thêm bằng `git add -f` vì `channel-k2/.gitignore` chặn `*.json`. Tôi không sửa `.gitignore`, giống cách phiên Teardown làm.
  - `licenses/`: 38 tệp. Preflight chặn email (P1), nên mọi email trong văn bản giấy phép đã thay bằng "[email đã che — xem URL gốc]".
- **Đề xuất cho P** (ngoài vùng lệnh, chưa ghi):
  1. `COST-LEDGER.csv` dòng `T3-01`: tiền kỳ, YouTube 294, Claude $0,0217 (haiku), ElevenLabs 0.
  2. `RIGHTS.md`: các dòng cho Copernicus DEM, Sentinel-2, PNOA, Rijksmuseum, Met, LoC khi tài sản được dùng thật (G1).
  3. `channel-k2/.gitignore`: thêm `!k2c-t3-01/tienky/*.json`.
  4. `HANG-DOI.md`: thêm K2C-T3-01 mức VÀNG.
- **Ghép thử:** nhánh chỉ thêm tệp mới trong `channel-k2/k2c-t3-01/`, nên không đụng `main` hay `k2c-t2`. Preflight trên `origin/main..HEAD` ĐẠT.

## 11. Preflight
- `bash scripts/env/verify.sh`: 9 PASS, 4 FAIL (three.js, tifffile/pyshp, k2v node_modules, Freesound). Cả 4 không liên quan việc tiền kỳ; giống kết quả của phiên Teardown.
- `bash tools/preflight.sh --range origin/main..HEAD`:
  - Lần 1 **TRƯỢT** vì 3 email trong tệp giấy phép. Đã che rồi chạy lại: **ĐẠT**.
  - `checks/lock.py --verify`: **KHỚP**.
  - Lần cuối chạy ngay trước lần đẩy cuối (ghi trong commit).
- Không dùng `--no-verify`.

## 12. Việc đang chờ chủ dự án
1. **Duyệt khuyến nghị:** đi tiếp Gibraltar (VÀNG đầy đủ) với 4 điều chỉnh ở §1. Hoặc chuyển Colorado (XANH).
2. **Chọn cửa sổ phát hành.**
   - (a) Trước 14/12: neo "điều cần theo dõi" là biểu quyết ở Nghị viện châu Âu; sau biểu quyết thì cập nhật bình luận ghim.
   - (b) Sau 14/12: có kết quả, ít rủi ro sai thời sự hơn nhưng mất độ nóng.
   - Đề xuất: **(a)**, kèm "as of" và kế hoạch cập nhật.
3. **Chốt cách gọi tên thuế mới:** "transaction tax" (tên trong hiệp ước), kèm hai cách gọi của Anh và Tây Ban Nha (C06, C06b).
4. **Duyệt tài sản mức "điều kiện":** Copley của Tate, Wright of Derby, LoC Keystone 1934, Pexels/Pixabay. Chủ dự án đối chiếu các trang giấy phép bị 403 (Pexels, Pixabay, IWM, NPG, Gallica). Xin API key NARA nếu cần ảnh Thế chiến II.
5. **Bản đồ biên giới:** duyệt việc dùng Natural Earth 10m mặc định (cần V/P cấp dữ liệu), và việc dùng ảnh PNOA (Tây Ban Nha) chụp Gibraltar.
6. **Có xin phép Gibraltar National Archives** cho ảnh đóng biên giới năm 1969 hay không (cần văn bản cho phép).
7. **P chép các đề xuất §10** vào COST-LEDGER, RIGHTS, `.gitignore`, HANG-DOI.
8. **Nguồn còn thiếu trước G1:**
   - trích dẫn gốc của Thị trưởng La Línea (Ayuntamiento), nếu giữ nhân vật này;
   - số SEPE 09/2026;
   - ngày bầu cử Tây Ban Nha (BOE);
   - nguyên văn trang MAEUEC về thuế "equivalente al IVA".
