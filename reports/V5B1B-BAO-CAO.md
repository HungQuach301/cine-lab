# V5b-1b — Vòng sửa CHUẨN HÌNH sau cổng chất lượng TRƯỢT lần 1 (Gibraltar 20 s) — BÁO CÁO

> Phiên V5b-1b, 16/10/2026, theo lệnh chủ dự án duyệt 16/10. Nhánh `v5b1b` tạo từ `origin/claude/v5b1-timelapse-gibraltar-6gsf1a` @ `ad3a40d`. **Không merge. DỪNG chờ chủ dự án.**
> Mọi số là số đo thật trong phiên (log ở `channel-k2/k2c-t3-01/v5b1-thu/v5b1b/do/`) hoặc tra nguồn có URL. Số ước ghi **(ước)**. Email người dùng không xuất hiện trong repo/báo cáo.

## 0. Khối điều lệ (lệnh + thực tế)
| Trường | Lệnh | Thực tế |
|---|---|---|
| Loại phiên | V (bộ công cụ hình) — vòng sửa | đúng |
| Nhánh | `v5b1b` từ `origin/claude/v5b1-timelapse-gibraltar-6gsf1a` @ `ad3a40d` | đúng; đẩy `v5b1b`, không merge |
| Tệp được sửa | CHỈ `design/k2v/tl/**`, `scripts/k2tl/**`, `channel-k2/k2c-t3-01/v5b1-thu/**`, `reports/V5B1B-BAO-CAO.md` | chỉ 4 vùng này (`git diff --stat ad3a40d..HEAD` §11). Không đọc mã `checks/` (chỉ chạy `lock.py --verify` qua preflight) |
| Trần | Claude API ≤ $3 (ghim model) · ElevenLabs 0 · YouTube 0 · giờ máy ≤ 5 h · chỉ CPU | **$0** (không gọi API) · **0** · **0** · **≈ 2,4 h** (§9) · chỉ CPU (SwiftShader) |
| Preflight | BẮT BUỘC | hook pre-commit/pre-push cài đầu phiên; mọi lần đẩy ĐẠT (§11) |
| Điều kiện dừng | xong việc → đẩy → dừng | (1) xong việc |

## 1. Tóm tắt (đọc 1 phút)
1. **Số đo chuẩn hình (8 khung 1080p, vùng giữa, không chữ, 640×360) — trung vị TRƯỚC → SAU:** bão hoà **0,200 → 0,429** (mục tiêu ≥ 0,35: **8/8 khung đạt**), colorfulness **24,1 → 45,5** (≥ 35: **8/8**), chi tiết **8,2 → 18,3** (cận dưới đối thủ 16: **6/8**, hai khung 15,8 / 15,9 nằm trong ±5 % — nêu tên §2.3), cháy sáng **0,00 %** mọi khung.
2. **Năm việc hình đã làm:** ánh sáng nắng thấp + trời xanh có mây + sương xanh chỉ ở xa + LUT A chỉ vùng tối & vibrance (chọn bằng số trong 7 phương án); **nền mặt đất 13 lớp vật liệu thủ tục** ở ≤ 2,6 km (vệ tinh chỉ phân lớp); **nhà đầy đủ 6 kiểu mặt đứng × 6 kiểu mái**, chia lô khối lớn, ban công, lớp tái dựng không còn hộp mờ; **Tower of Homage 6 đặc điểm hình học** + tường lâu đài có 8 tháp góc; **tàu theo thời kỳ (74 chiếc)**, **trạm biên giới + hàng xe/người A-lite mốc 1941**.
3. **Máy quay:** tốc độ góc tối đa **226 → 33 °/s**; năm dừng 1,92 s; zoom-in tháp **×8,8**; reveal **×11,8**; bay tuyến Winston Churchill Ave 3,0 s lệch tối đa **4,6 m**; không đứng yên. **Nội dung hình học** (toà/hero/tường/đường/tàu/xe) trên 8 khung: 17–43 %; tính cả nền phố: 22–69 %. **Mục tiêu ≥ 40 % chỉ đạt ở 1/8 khung theo hình học (3/8 khi tính nền phố)** — khung eo đất/mốc đinh còn nhiều đồng cỏ trống (đúng lịch sử, nhưng thưa) — §4.
4. **Bản đồ lịch sử:** tìm được 3 bình đồ sạch quyền (Baedeker 1913, AMS M981 1943 PD-USGov, Admiralty 144 bản 1907); **đã nắn Baedeker 1913** (8 điểm khống chế, RMS 65 m) → mốc 1913; AMS 1943 bị HTTP 429 khi tải — chờ (§5).
5. **Giờ máy:** đoạn thử **6,41 s/khung** trên máy hiện tại (hệ số máy: máy này nhanh hơn máy B của V5b-1 **×1,41**, đo khung 470 SPP2 bằng mã V5b-1). Ngoại suy tập 10 phút kịch bản 3: **18,5 h (máy này) / 26,0 h (máy chậm)** — **KHÔNG ĐẠT ≤ 12 h trên CPU** (§7). Chất lượng mới đắt hơn ≈ 1,85× mỗi khung.

## 2. Ánh sáng & màu (việc 1)
### 2.1 Thay đổi
| Hạng mục | V5b-1 | V5b-1b |
|---|---|---|
| Nắng | cao 31°, phương 238°, 2,6, trắng ấm | giữ hướng (cao 31° trong khoảng 25–40°), cường độ 3,3, ấm `#ffe3b8`; bóng PCF bán kính 3 → 1,5 (sắc hơn) |
| Trời | gradient xám nhạt, không mây | chân trời xanh `(0.60,0.74,0.90)` → thiên đỉnh `(0.13,0.33,0.70)`; **mây tích thưa** thủ tục (mặt sáng ấm, đáy xám xanh, nhạt về chân trời) — dùng cả cho phản chiếu nước |
| Sương | FogExp2 trắng xám, 2,6e-5 | **ngả xanh** cùng màu chân trời, mật độ 1,75e-5 (gần như không ở < 3 km) |
| Ánh trời | hemisphere 0,85 xám | 0,62, trời `#9cbcf0` / đất `#7a6648` → bóng ngả lạnh, tương phản ấm–lạnh |
| Grade | LUT A toàn dải (k = 1) | **LUT A chỉ vùng tối** (`uLutMode` 1: trọng số 1 − smoothstep(0,10; 0,42; Y)) + **vibrance 0,35** (bù ACES làm nhạt, giữ độ sáng); không làm nhạt trung/sáng |
| Mốc đinh | phần không nhấn giảm bão hoà 55 %, tối 36 % | 25 % / 16 % (×0,45); đường băng nhấn bằng làm SÁNG, không ám nâu |

### 2.2 Chọn LUT bằng số đo (8 khung, 960×540, SPP2, không chữ — `do/lut-*.json`)
| Phương án | Bão hoà trung vị (min) | Colorfulness trung vị (min) |
|---|---|---|
| LUT A toàn dải, không vibrance (= V5b-1) | 0,314 (0,263) | 36,9 (22,5) |
| LUT A chỉ vùng tối | 0,335 (0,298) | 38,1 (23,8) |
| LUT A k = 0,5 + vibrance | 0,402 (0,353) | 46,7 (29,6) |
| **LUT A chỉ vùng tối + vibrance 0,35 (CHỌN)** | **0,412 (0,369)** | **47,7 (30,3)** |
| LUT B (V5a) chỉ vùng tối + vibrance | 0,414 (0,369) | 47,5 (30,3) |
| LUT B toàn dải + vibrance | 0,406 (0,357) | 48,1 (30,2) |
| Không LUT + vibrance | 0,414 (0,365) | 47,2 (30,2) |

Kết luận: hai LUT gần như không đổi số (cả hai đều nhẹ); yếu tố quyết định là bỏ làm nhạt + vibrance. **Giữ LUT A** (chủ dự án đã chọn A ở V5a — bản sắc kênh "thép lạnh") nhưng chỉ ở vùng tối. Không chép bảng màu đối thủ (không dùng tệp đối thủ trong phiên).

### 2.3 Bảng TRƯỚC → SAU (8 khung 1080p; TRƯỚC = mã V5b-1 @ `ad3a40d` dựng lại cùng số khung, cùng gói cảnh; SAU = mã V5b-1b) — `do/compare8.md`, `do/truoc-sau-8-khung.jpg`
Đo: `scripts/k2tl/measure_look.py` (640×360 INTER_AREA, vùng giữa x/y 15–85 %, khung dựng KHÔNG chữ), bảng bởi `compare_look.py`; nội dung bằng `render.js --maskonly`.

| Khung (số khung) | Bão hoà trước → sau | Colorfulness trước → sau | Chi tiết trước → sau | Cháy sáng sau | Nội dung hình học / + nền phố (sau) |
|---|---|---|---|---|---|
| toàn cảnh 1 · mở đầu 1704 (10) | 0,173 → **0,427** ✓ | 34,6 → **80,2** ✓ | 5,9 → **20,5** ✓ | 0,00 % | 17,1 % / 27,7 % |
| toàn cảnh 2 · kết 2026 (476) | 0,196 → **0,447** ✓ | 39,5 → **90,4** ✓ | 17,5 → **34,0** ✓ | 0,00 % | 31,8 % / 59,8 % |
| cận hero 1 · Tower of Homage (168) | 0,302 → **0,408** ✓ | 21,1 → **46,1** ✓ | 8,6 → **18,6** ✓ | 0,00 % | **42,7 %** / 69,2 % |
| cận hero 2 · đường băng mốc đinh 1941 (312) | 0,090 → **0,388** ✓ | 19,8 → **39,0** ✓ | 11,1 → **15,9** ✗ | 0,00 % | 18,7 % / 21,5 % |
| phố eo đất 1 · bay tuyến c.1900 (214) | 0,208 → **0,435** ✓ | 24,0 → **36,6** ✓ | 7,8 → **15,8** ✗ | 0,00 % | 20,9 % / 26,3 % |
| phố eo đất 2 · La Línea 1916 (240) | 0,204 → **0,435** ✓ | 24,1 → **37,7** ✓ | 11,3 → **17,3** ✓ | 0,00 % | 22,6 % / 29,0 % |
| **mới** · phố dày · phố cổ 1753 (77) | 0,176 → **0,408** ✓ | 31,2 → **52,2** ✓ | 7,8 → **26,3** ✓ | 0,00 % | 33,5 % / **49,3 %** |
| **mới** · cận hero có phố quanh 1883 (172) | 0,286 → **0,431** ✓ | 20,9 → **44,8** ✓ | 5,2 → **18,0** ✓ | 0,00 % | 32,6 % / **59,3 %** |
| **Trung vị** | **0,200 → 0,429** | **24,1 → 45,5** | **8,2 → 18,3** | 0,00 % | 22,6 % / 44,1 % |

- Cách đo của điều phối (khung có chữ, bỏ lớp chữ) cho V5b-1: 0,17 / 25 / 15. Đo lại 6 khung V5b-1 có chữ bằng script này (vùng giữa): 0,194 / 24,9 / 17,8 — chi tiết cao hơn bản không chữ (8,2) vì cạnh chữ/thẻ lọt vùng giữa. Bảng trên dùng bản **không chữ** cho cả trước và sau (khắt khe hơn).
- Khung "trước" cận hero 1 / cận hero 3 là cùng SỐ khung trong mã V5b-1 (góc máy cũ) — so trước/sau theo số khung như lệnh, không phải cùng góc.
- **Chỉ số trong ±5 % quanh ngưỡng (nêu tên):** chi tiết khung 312 = 15,9 (−0,6 % dưới 16), khung 214 = 15,8 (−1,3 %).
- Khung có chữ (bản phát) ở `v5b1b/khung/` (8 tệp, 1080p, đủ lớp chữ).

## 3. Nền mặt đất, nhà, hero (việc 2–4)
### 3.1 Nền mặt đất cách điệu (lớp 3)
- `build_scene.py --cls` → `cls.png` (10 m): lớp TỰ NHIÊN (trạng thái trước đô thị hoá) + lớp ĐÔ THỊ 2026 + khoảng cách bờ 1987/2026. Phân lớp từ NDVI Sentinel-2, độ dốc DTM, độ cao, khoảng cách bờ, polygon OSM (beach, bare_rock/cliff, scrub/heath/wood, farmland, pitch/stadium, parking (mới trích), industrial/port, construction, grass/park/garden, meadow). Ảnh kiểm `do/phan-lop-nen.jpg`.
- 13 vật liệu thủ tục (`terrain.js matC`): cát (gợn + vệt ướt mép nước), cỏ khô/garrigue (cụm bụi), maquis (cụm + khe đá), đá vôi (tầng, hốc, bụi lẻ), ruộng (luống theo hướng từng thửa), nhựa (vá), nền lát (tấm 2 m, ron, ố), sân thể thao (sọc cắt cỏ), bãi đỗ (vạch ô — theo trục lưới, phong cách hoá), bê tông cảng, đất trống, cỏ công viên, đồng cỏ eo đất (cỏ ô liu + mảng cỏ khô + lối mòn sáng — phong cách hoá theo ảnh LoC c.1900).
- **≤ 2,6 km không trải ảnh vệ tinh** (chỉ tông vùng 18 % từ mip mờ ~160 m), mờ dần tới 3,6 km; xa hơn dùng vệ tinh như cũ. Ranh lớp cong hữu cơ (lệch ±15 m). Vách > ~38° → đá vôi, không loang.
- Đường: vỉa hè 2,2 m lát gạch + bó vỉa (sau 1900), lối mòn/lối lát (OSM path/track/footway/steps — mới), đá dăm gần.
- Sửa dữ liệu theo năm: (a) vùng "chưa có đất" trước 1941/1987 phải nối liền biển (bỏ 2 680 ô ao lẻ do nhiễu Landsat — lỗi thấy ở khung 1916); (b) khai hoang 1987→2026 = mảng ≥ 2 ha giáp biển 1987 (sân đỗ nhựa NIR thấp không còn bị coi là "đất mới"); (c) cây OSM trên đất khai hoang không mọc trước khi có đất; (d) khu quân sự trống (Upper Rock) không còn tính là phố; (e) sân bóng hiện đại không lấy năm đường băng 1941; (f) tuyến WCA gồm đoạn mặt đường qua đường băng (OSM ghi `residential`) — trước đây nội suy lệch ~25 m.

### 3.2 Nhà thường & lớp tái dựng (lớp 2)
- **Lớp tái dựng = nhà đầy đủ** (mái ngói, cửa sổ, chớp, ban công), cao 2–4 tầng thời kỳ (băm, xen kẽ), **giảm bão hoà 22 %** (≤ 25 %), KHÔNG trong suốt; nhãn phương pháp giữ nguyên ("reconstructed from LoC print, 1705" / "…LoC photo, 1860–80" mới / thẻ ảnh "muted houses: reconstructed").
- **6 kiểu mặt đứng** (đếm trong cảnh: Genoa phấn màu 5 671 · Andalucía vôi trắng 11 585 · Anh thế kỷ 19 1 705 · chung cư 1960+ 15 345 · kho/xưởng 75 · kính/văn phòng 1 060) × **6 kiểu mái** (tường chắn 8 826 · sân thượng có bồn/lồng thang 8 845 · phẳng 2 555 · mái hông có nóc 5 258 · hai mái 7 829 · chóp 2 128); chìa mái 0,35 m; **22 873 dải ban công** có lan can đục song sắt.
- Cửa sổ căn giữa từng mặt (không vắt góc): khung, kính phản trời, chớp lá sách mở/đóng, bậu, lanh tô, gờ tầng, gờ mái + bóng dưới gờ, chân đế, góc đá; mái ngói có hàng, mái phẳng lát tấm 1,2 m + ố.
- **Chia lô**: 818 khối OSM Gibraltar > 320 m² chia theo trục chính thành lô 7–13 m × ≤ 16 m → 35 441 phần nhà (hết "khối sạch" cả dãy phố một màu).
- Kiểu "doanh trại đá vôi" có trong bảng màu nhưng 0 toà dùng (khối lớn đã chia lô) — vẫn đủ 6 kiểu mặt đứng thực dùng.

### 3.3 Hero (lớp 1)
**Tower of Homage — 6 đặc điểm dựng bằng hình học** (số đo ƯỚC theo ảnh tài sản công; cao 23 m / 320 m² theo Ministry for Heritage — chờ đối chiếu bằng mắt như V5b-1): (1) chân tường choãi 2,5 m; (2) **bậc thềm 6 bậc + cửa vào vòm** mặt tây; (3) **cửa sổ vòm** hai tầng (8,5 m, 15,5 m) trên mỗi mặt dài, viền đá sáng nhô; (4) **răng cưa nhịp 2,2 m có mũ chóp kiểu Moor**; (5) **gờ đá dưới tường chắn + sàn đỉnh có lầu cầu thang** có răng cưa; (6) **tường lâu đài có răng cưa + 8 tháp góc** ở chỗ gãy khúc ≥ 28°. Tapia: lớp đầm tông so le từng mẻ, vệt mưa + rêu chân tường đậm dần theo năm, mảng trát tu bổ nhạt sau 1995. Phố cổ bám quanh lâu đài: khung 168/172 (nội dung 43 % / 33 %).
**Đường băng 09/27 + WCA + cổng biên giới, mốc 1941 (A-lite):** trạm biên giới đặt ở OSM node 5029266974 (`barrier=border_control`; nhà gác mái đỏ, bốt lính, chắn đỏ/trắng); hàng xe kiểu thập niên 1940 (xe con, xe tải, xe buýt — hình khối, không mô phỏng mẫu cụ thể) chờ ở hai phía chắn đường băng, đặt trên tim WCA; 42 người phẳng màu đổ bóng thật; chỉ hiện 1940,5–1946,5. Số lượng là **minh hoạ** (không có nguồn đếm).
**Tàu** (`ships.js`, 74 chiếc): buồm 1704–1860 (11, minh hoạ cảnh 1704 — không theo sổ hạm đội), thuyền nhỏ 1860–1965 (40) + hơi nước (9), tàu hàng/dầu 1965+ (13) + tàu khách 2008+ (1).

## 4. Bố cục khung + ngữ pháp máy (việc 5–6)
### 4.1 Nhịp mới (`scenes/gib20.js`; chữ/thời điểm thẻ giữ như V5b-1)
| Giây | Năm | Máy |
|---|---|---|
| 0–3,2 | 1704→1750 | trên vịnh phía tây nhìn **phố trong tường + Line Wall + tàu buồm**, ống 30° |
| 3,2–7,4 | →1850→1882 | lướt từ tây-nam vào tháp, **zoom-in 1 202 → 136 m (×8,8)**, mặt tháp đón nắng; phố sườn tây mốc 1880 mọc quanh lâu đài lúc ~6,9 s |
| 7,8–10,8 | 1895→1932 | **bay dọc WCA** (3,0 s, cao 273–308 m, lệch TB 0,48 m / tối đa **4,6 m**), ống 21° nén **La Línea** đang mọc; ảnh LoC neo 3D |
| 11,5–14,1 | 1941 dừng **1,92 s** | **mốc đinh**: góc chéo qua đường băng + hàng xe ở chắn + La Línea phía sau; năm phóng 1,45× |
| 14,1–20 | 1946→2026 | **reveal kéo lùi 298 → 3 511 m (×11,8)**, vòng từ nam sang tây-bắc, kết nhìn La Línea + sân bay + Gibraltar + vịnh có tàu |

Tốc độ góc tối đa **32,6 °/s** (14,3 s) — ≤ 90 °/s; cú quét 226 °/s cũ đã bỏ. Không khung đứng yên. Ngân sách chữ: ≤ **13,9 %** khung thường, **15,2 %** mốc đinh, vùng giữa không neo 0 %, ≤ 1 thẻ, tương phản min **9,32:1**, chữ ≥ 38 px@1080 (`do/text-budget.json`, `render-log.json`).

### 4.2 Nội dung ≥ 40 % — KHÔNG đạt đủ
Đo bằng mặt nạ dựng cùng máy/năm (`render.js --maskonly`; đỏ = hình học nội dung, xanh = nền phố của năm đó). 8 khung: hình học 17–43 % (trung vị 22,6 %), + nền phố 22–69 %. Đạt ≥ 40 %: khung 168 (hình học); 77, 172, 476 (khi tính nền phố). Khung eo đất (214, 240) và mốc đinh (312) 19–23 %: vùng trung lập/đồng cỏ giữa hai thành phố là trống thật trong 1900–1941 (bình đồ Baedeker 1913 cũng vẽ trống: "Neutral Ground", trường đua, nghĩa trang) — đã dùng ống dài nén La Línea và đặt hàng xe/người ở mốc đinh, nhưng không thêm nhà không có bằng chứng (luật "không thêm phần tử chỉ để vượt ngưỡng"). Hướng gỡ ở §12.

## 5. Bản đồ lịch sử 1880 → 1987 (việc 5, phần dữ liệu)
Tác tử con tra (chỉ đọc, `/tmp`): 15 ứng viên; sạch quyền cho bán phim:
| Bình đồ | Quyền (trích trang chủ) | Dùng |
|---|---|---|
| **Baedeker *Spain and Portugal* 1913, "Gibraltar 1:25 000" (Wagner & Debes)** — archive.org/details/spainportugalhan00karl, trang n643 | IA: `possible-copyright-status: NOT_IN_COPYRIGHT`; in 1913 → PD Hoa Kỳ; ngoài Mỹ CHƯA kiểm (tác giả là hãng) | **ĐÃ NẮN** (affine, 8 điểm khống chế OSM: Europa Point lighthouse, Rosia Bay, Southport Gates, Signal Station, O'Hara's Battery, Catalan Bay, King's Bastion, Windmill Hill) — **RMS 65,3 m, tối đa 102 m** → chỉ dùng mức KHU (đệm 60 m). Khối xây tô cam → **11 toà** (khu Cattle Sheds/Devil's Tower) có mốc tái dựng 1913 (`build_scene.py --plan1913`, `licenses/baedeker-1913-plan-gibraltar.txt`) |
| **U.S. Army Map Service, "Gibraltar" City Plan 1:10 000, AMS M981, 1943** (chép Admiralty Chart 144 sửa đến 1942) — Commons `File:Map_by_the_US_Army_Map_Service_-_Gibraltar_…jpg` (2 912×4 461) | `{{PD-USGov-Military}}`; FAQ UT PCL "public domain, no permissions needed" (đọc qua tìm kiếm) | **CHƯA dùng**: upload.wikimedia.org trả **HTTP 429** liên tục qua proxy; maps.lib.utexas.edu trả trang HTML |
| Admiralty Chart No. 144 "Gibraltar" (in 1907; xuất bản 1886) — Commons, 6 040×8 182 | `{{PD-UKGov}}`; UWM "users need [no] permission… public domain" | chưa xem được (429) |
Loại: David Rumsey (CC BY-NC-SA), Gallica 1940 (thương mại phải trả phí), hải đồ Admiralty 1953/1968 (có thể bị URAA phục hồi ở Mỹ), bản đồ Inundation 1928 TNA (có thể chưa xuất bản → Crown 125 năm). **1950–1987: không tìm được bình đồ sạch quyền** → giữ nguyên, không bịa (Gibraltar ngoài phố cổ/sườn tây vẫn chỉ đặc ở mốc Landsat 1987).
Ghi chú: video 20 s đã dựng TRƯỚC bước `--plan1913` (bước này chạy sau khi lượt dựng nạp gói cảnh) → 11 toà mốc 1913 có trong gói cảnh hiện tại nhưng không có trong `gib20_540p.mp4`; ảnh hưởng hình không đáng kể (một khu nhỏ phía đông eo đất).

## 6. Đoạn thử 20 s + âm
- `channel-k2/k2c-t3-01/v5b1-thu/v5b1b/gib20_540p.mp4` (960×540, **4,67 MB**, commit thường; SHA-256 `9c0ba518…`) · **1080p ngoài git** `/var/tmp/cine-out/gib20_1080p.mp4` (**102,1 MB**, SHA-256 `c2448d03cdb6846c846119095e2d977358002bae2684d6c5140accb2b872dc04`) — chờ duyệt dòng LFS (đề xuất V5b-1 §10.1, cùng mẫu đường dẫn thêm `v5b1b/`).
- Âm: `mix.py` + `cues.json` V5b-1 (biến cố giữ thời điểm), master **−14,3 LUFS / −1,7 dBTP** (1080p), −14,3 / −1,5 (540p) — giảm 0,3 dB để true peak sau AAC ≤ −1,5 dBTP. Không lời; ElevenLabs 0.
- 8 khung 1080p có chữ: `v5b1b/khung/` (6 loại như V5b-1 cùng số khung + `pho-day-pho-co-1753` + `can-hero-3-thap-pho-quanh-1883`); tờ khung `do/to-khung-20s.jpg`; trước/sau `do/truoc-sau-8-khung.jpg`.
- Dữ liệu thô tải lại (container mới không giữ bộ đệm): `scripts/k2tl/fetch_sources.py` — **12/12 tệp KHỚP SHA-256 của V5b-1** (`do/fetch_sources.json`); gói cảnh dựng lại trùng thống kê V5b-1 (28 538 toà, 82 615 cây) trước khi sửa. Ảnh cắt LoC `ng_crop.jpg` (V5b-1 không ghi cách cắt) cắt lại từ TIF gốc, SHA trong `do/sha256.txt`.

## 7. Giờ máy (việc 7)
### 7.1 Hệ số máy (bench chuẩn V5b-1 §5.2: khung 470 SPP2, dựng 2 lần lấy lần 2, mã V5b-1 @ `ad3a40d`)
| Máy | khung 470 SPP2 | Nguồn |
|---|---|---|
| máy B (V5b-1, lượt cuối) | 4,35 / 4,45 s | `v5b1-thu/do/bench-final.jsonl` (A, A2) |
| **máy hiện tại (C)** | **3,09 / 3,14 s** (đầu / cuối phiên) | `do/bench-may-dau-phien.jsonl`, `do/bench-v5b1b.jsonl` |
| **Hệ số B / C** | **×1,41** (C ≈ máy A của V5b-1, ×1,48) | — |

### 7.2 Đo trên máy C
| Đo | s/khung |
|---|---|
| Đoạn thử 1080p, 480 khung (SPP thích ứng: 329×SPP2, 79×SPP4, 72×SPP1) | **6,41** (51,3 phút) |
| theo nhịp: S1 mở 6,26 · S2 glide→tháp 7,65 · S3 bay tuyến (SPP1) 3,46 · S4 mốc đinh 9,26 · S5 reveal 5,19 | — |
| theo SPP (trung bình trong đoạn, bỏ khung đo tương phản): SPP1 3,34 · SPP2 5,83 · SPP4 11,57 | — |
| Bench 3 khung (470, 175, 300) SPP2 mã mới / mã V5b-1 cùng máy | 5,81 / 3,51 (+66 %; khung cùng số nhưng góc máy mới dày nội dung hơn) |
| Kỹ thuật (SPP2, 3 khung): nền vệ tinh thay vật liệu thủ tục | 5,67 (thủ tục chỉ +2,5 %) |
| · nhiễu nướng sẵn cho nền | 6,41 (+10 % — CHẬM hơn → giữ tắt) |
| · tắt bóng | 5,00 (−14 %) |
| · không nhà | 5,13 (nhà −12 %) · không tàu 5,87 (≈ 0) · tán cây 20 mặt 5,77 (≈ 0) · phản chiếu nước không mây 5,76 (≈ 0) |
| · chỉ nền (không nhà/tàu/cây) | 5,00 |
| SPP1 / SPP4 | 3,23 / 10,91 |

Phần tăng lớn nhất nằm ở "nền" (địa hình + nước + trời + hero + đường) trong khung có nhiều nội dung hơn, không ở một kỹ thuật riêng; tắt từng phần đều chỉ ≤ 14 %.

### 7.3 Ngoại suy tập 10 phút (14 400 khung), kịch bản V5b-1 §5.3 với số đo mới
| # | Kịch bản | s/khung máy C | giờ máy C | giờ máy chậm B (×1,41) |
|---|---|---|---|---|
| 2 | 100 % 3D, SPP4 5 % · SPP1 15 % · SPP2 80 % | 5,74 | 23,0 h | 32,4 h |
| **3** | **như 2 + 30 % relief/2.5D (1,98 s, NT 15/10)** | **4,61** | **18,5 h** | **26,0 h** |
| 4 | như 3 + SPP1 cho 50 % khung bay nhanh + tắt bóng cảnh xa | 3,58 **(ước)** | 14,3 h | 20,2 h |

**Trần 12 h: KHÔNG ĐẠT** ở mọi kịch bản, cả máy nhanh. Mức chuẩn hình mới đắt ≈ 1,85× mỗi khung so với V5b-1 (6,41 s ↔ 4,88/1,41 = 3,46 s cùng máy). Đường ra (cần chủ dự án quyết): (a) GPU (NT K6 đang hoãn) — giải pháp duy nhất giữ nguyên chất lượng; (b) dựng song song nhiều container (giờ máy không đổi, thời gian tường giảm); (c) ≥ 50 % relief/2.5D + SPP1 bay nhanh ≈ 12–13 h máy C **(ước)**, thấp hơn mức chất lượng của đoạn thử.

## 8. Tự chấm 4 lớp (0–10; điều phối chấm mù với đối thủ ngoài repo)
| Lớp | V5b-1 | V5b-1b | Đạt | Chưa đạt |
|---|---|---|---|---|
| 1 Hero | 6 | **7,5** | tháp 6 đặc điểm nhận diện, tapia lớp/loang theo năm, lâu đài có tháp góc; đường băng + chắn + hàng xe/người + trạm biên giới 1941 | số đo chi tiết tháp là ước (không bản vẽ); người/xe ở mốc đinh nhỏ (≈ 15–20 px@1080 mỗi xe); nhà ga/đường hầm 2023 chưa dựng |
| 2 Nhà thường | 6 | **7,5** | 6 × 6 kiểu, chia lô, ban công, cửa sổ chi tiết, tái dựng là nhà đầy đủ; phố cổ/La Línea đọc được như thành phố thật | mái chóp còn hình học đơn; cửa sổ là shader (không lõm); nhà La Línea xa nhìn trắng đều |
| 3 Nền sống | 4,5 | **6,5** | 13 vật liệu, không trải vệ tinh gần, vỉa hè, lối mòn, tàu, dữ liệu năm sạch ao lẻ | sườn Rock garrigue hơi "loang rằn ri" ở trung cảnh; mảng cỏ công viên/nền lát bờ cứng; đồng cỏ eo đất phẳng; Rock ở khung kết xa > 3,6 km còn là vệ tinh tối |
| 4 Ánh sáng/hoàn thiện | 5,5 | **7,5** | nắng có hướng, bóng sắc, trời xanh có mây, sương xanh chỉ ở xa, LUT vùng tối + vibrance, 0 % cháy sáng | không AO trong (SSAO); mây chỉ là lớp vòm (không bóng mây trên đất) |

## 9. Chi phí
| Khoản | Trần | Thực tế |
|---|---|---|
| Claude API | $3 | **$0** (không gọi; không có `cost.jsonl`) |
| ElevenLabs / YouTube | 0 / 0 | 0 / 0 |
| Giờ máy | ≤ 5 h | **≈ 2,4 h**: lượt dựng trọn 51,3 phút; khung kiểm/thăm dò ≈ 35 phút **(ước theo log)**; chọn LUT 7×8 khung ≈ 12 phút; khung đo trước/sau + mặt nạ ≈ 8 phút; bench 10 lượt ≈ 12 phút; dựng gói cảnh 4 lần ≈ 15 phút; tải dữ liệu ≈ 5 phút; test ≈ 6 phút |
| Mạng | — | ≈ 1,6 GB (tải lại bộ đệm V5b-1) + 0,8 MB bình đồ |
| Token | trần mềm | chưa đọc được (chủ dự án xem Usage); 1 tác tử con tra bản đồ (chỉ đọc) |

Đề xuất dòng `COST-LEDGER.csv` (P ghi — ngoài vùng lệnh): `V5b1b,Vòng sửa chuẩn hình Gibraltar 20 s,V,2026-10-16,,,,,0,3,—,0,0,≈ 2,4,,0,20,,reports/V5B1B-BAO-CAO.md,YouTube 0; không merge`

## 10. Đề xuất ngoài vùng (chưa ghi)
1. `tools/lfs-allow.txt`: thêm `channel-k2/*/v5b1-thu/**/*-1080p.mp4` (bản 1080p 102,1 MB).
2. `RIGHTS.md`: dòng V5b1b-01 Baedeker 1913 "Plan of Gibraltar" (bằng chứng mốc, không hiển thị; quyền ngoài Mỹ chưa kiểm); khi dùng AMS M981 1943 → dòng riêng (PD-USGov-Military).
3. `AUTHORSHIP.md`: quyết định sáng tạo chờ chủ dự án duyệt — lớp tái dựng là "nhà đầy đủ giảm bão hoà 22 %" thay "khối mờ"; xe/người/tàu minh hoạ; nhịp máy mới (mở từ vịnh, bay tuyến nhìn La Línea, mốc đinh góc chéo); LUT A chỉ vùng tối + vibrance.
4. `channel-k2/.gitignore`: `!k2c-t3-01/v5b1-thu/**/*.json` (phiên này `git add -f`).
5. `scripts/env/setup.sh`: `imagecodecs` (vẫn cần cho GeoTIFF Copernicus).

## 11. Preflight, tệp, ghép thử
- `bash scripts/env/verify.sh` đầu phiên: 10 PASS / 3 FAIL (three.js, tifffile/pyshp, k2v node_modules — container mới) → cài theo hướng dẫn của verify.
- Hook pre-commit/pre-push cài đầu phiên. `bash tools/preflight.sh --range origin/main..HEAD`: **ĐẠT**, `lock.py --verify`: **KHỚP** (lần đẩy đầu bị chặn vì ref `origin/main` cục bộ cũ → 1 042 tệp lạ; `git fetch origin main` rồi đẩy lại ĐẠT, không dùng `--no-verify`).
- Tệp đổi so với `ad3a40d`: chỉ `design/k2v/tl/**` (11 tệp sửa + `ships.js`), `scripts/k2tl/**` (5 sửa + `fetch_sources.py`, `measure_look.py`, `compare_look.py`, `tests/test_look.py`), `channel-k2/k2c-t3-01/v5b1-thu/**` (`v5b1b/` + 1 tệp giấy phép), báo cáo này. Mọi tệp commit ≤ 5 MB (lớn nhất `gib20_540p.mp4` 4,67 MB).
- **Test** `bash scripts/k2tl/tests/run.sh`: **TẤT CẢ TEST ĐẠT** — test_geo 2/2, test_calib 2/2, **test_look (mới)**, test_geom **88 tam giác** (thêm mái hai mái/mái hông/hộp/chia lô/cắt nửa mặt phẳng), test_campath (lệch 6,31 m), test_browser (4 khung; chữ ≤ 15,63 % ở mốc đinh; tương phản min 9,63; dựng lại khung 300 khác byte — như V5b-1, do thứ tự bóng/cache).
- Lỗi tìm thấy và sửa trong phiên (ghi cho K): three.js dùng chung shader giữa vật liệu có cùng mã `onBeforeCompile` (đá vôi 'lime' ↔ tapia; đường băng mượn shader khác → hiện từ 1704) → khoá `customProgramCacheKey`; đo mặt nạ xen dựng hình làm hỏng trạng thái → tách lượt riêng; xem §3.1 (a)–(f).
- Ghép thử: nhánh chỉ thêm/sửa tệp trong 4 vùng của chuỗi V5b-1 (không phiên nào khác sửa các vùng này) — ghép với `origin/main` sạch theo `git merge-tree` (chạy trước lần đẩy cuối).

## 12. Việc chờ chủ dự án
1. **Duyệt vòng sửa + chấm mù lại với đối thủ** (`v5b1b/gib20_540p.mp4`, 8 khung `v5b1b/khung/`) — điều phối đo lại bằng cách của cổng.
2. **Nội dung ≥ 40 %** chưa đạt ở khung eo đất/mốc đinh (19–23 % hình học): chọn (a) chấp nhận vì trống là sự thật lịch sử, (b) đổi kịch bản đoạn eo đất sang nhìn phố Gibraltar/cảng, hoặc (c) dùng AMS 1943 + Baedeker 1913 để dựng các công trình có bằng chứng ở North Front (trại, trường đua, nghĩa trang, chuồng gia súc) thành nội dung trung cảnh.
3. **Giờ máy: KHÔNG ĐẠT 12 h trên CPU** (18,5 h máy nhanh / 26 h máy chậm, kịch bản 3) — quyết GPU (NT K6) / dựng song song / hạ tỉ lệ cảnh 3D.
4. **Bình đồ AMS M981 1943** (PD-USGov) — tải thủ công (Commons đang 429 qua proxy) hoặc cho phép thử lại ở phiên sau; quyền ngoài Mỹ của Baedeker 1913.
5. Đối chiếu bằng mắt số đo Tower of Homage (23 m / 320 m²) — vẫn treo từ V5b-1.
6. Duyệt dòng LFS/RIGHTS/AUTHORSHIP/COST-LEDGER/.gitignore (§10) — P ghi.
