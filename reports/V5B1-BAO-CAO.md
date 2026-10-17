# V5b-1 — Mô-đun "xương sống thời gian" + CHUẨN HÌNH 4 lớp + đoạn thử Gibraltar 20 s — BÁO CÁO

> Phiên V5b-1, 15–16/10/2026, theo lệnh chủ dự án duyệt 16/10 (Y1–Y7, Z1–Z2; chỉ CPU). Nhánh `claude/v5b1-timelapse-gibraltar-6gsf1a` (nhánh phiên do harness chỉ định, tương ứng "v5b1" trong lệnh), tạo từ `origin/main` @ `7255aa4`. **Không merge. DỪNG chờ chủ dự án.**
> Mọi số trong báo cáo là số đo thật trong phiên (log ghi ở `channel-k2/k2c-t3-01/v5b1-thu/do/`) hoặc tra nguồn có ghi URL. Số ước ghi **(ước)**.

## 0. Khối điều lệ (lệnh + thực tế)
| Trường | Lệnh | Thực tế |
|---|---|---|
| Loại phiên | V (bộ công cụ hình), vùng tệp riêng | đúng |
| Nhánh | v5b1 từ `origin/main` | `claude/v5b1-timelapse-gibraltar-6gsf1a` @ `7255aa4` (tên nhánh theo harness); không merge nhánh khác — đọc `timelapse-rd`, `k2c-t3-tienky`, `v5a` bằng `git show` |
| Tệp được sửa | CHỈ tạo mới: `design/k2v/tl/**`, `scripts/k2tl/**`, `channel-k2/k2c-t3-01/v5b1-thu/**`, `reports/V5B1-BAO-CAO.md` | chỉ 4 vùng này. **Không sửa tệp có sẵn nào** (kể cả RIGHTS/AUTHORSHIP/COST-LEDGER — đề xuất ở §10). Không đọc mã `checks/` (chỉ chạy `lock.py --verify` qua preflight) |
| Trần | Claude API ≤ $3 · ElevenLabs 0 · YouTube 0 · giờ máy ≤ 4 h | **$0** (không gọi API) · **0** · **0** · **≈ 2,5 giờ máy** (§9) |
| Preflight | BẮT BUỘC | hook pre-commit/pre-push cài đầu phiên; kết quả §11 |
| Điều kiện dừng | xong việc → đẩy → dừng | (1) xong việc. Giữa phiên worker bị khởi động lại một lần (mất một lượt đo tải); đã commit bảo toàn và chạy lại |

## 1. Tóm tắt (đọc 1 phút)
1. **Mô-đun `design/k2v/tl/`** (12 tệp JS + 2 tệp nguồn hero) + **công cụ `scripts/k2tl/`** (tải OSM, dựng raster/vector/gói cảnh, driver dựng, đo kỹ thuật, trộn âm, căn góc then/now) — port từ `lab/timelapse`, sửa 4 lỗi R&D (§2.2). Test: **6 bộ, đều ĐẠT** (§3).
2. **Hai tầng thời gian chạy thật trên Gibraltar:** La Línea = TẦNG ĐẦY ĐỦ (26 087 phần toà Catastro mọc đúng năm xây); Gibraltar = TẦNG CHUẨN theo 5 mốc bằng chứng (bản in LoC 1705, ảnh LoC 1860–80, HMGoG 1941/1943, Landsat 1987, Sentinel-2 2026) + lớp GHOST có nhãn "reconstructed from …". Mặt nước theo năm: phần đường băng lấn vịnh chỉ nổi 1941→1943, đất khai hoang sau 1987 không có ở năm cũ.
3. **Đoạn thử 20 s 1080p** đủ yêu cầu: 2 hero (Tower of Homage, đường băng 09/27), 1 mốc đinh 1941 (năm dừng **1,92 s**, phóng 1,45×), bay dọc Winston Churchill Ave **3,0 s, lệch tim tuyến tối đa 5,7 m**, zoom-in ×22,5, reveal kéo lùi ×14,0, ảnh LoC "Neutral ground" neo điểm 3D; âm **−14,0 LUFS / −1,6 dBTP**. Chữ: ≤ **13,9 %** khung thường, **15,2 %** mốc đinh, vùng giữa 0 %, tương phản tối thiểu **9,11:1**.
4. **Giờ máy:** đoạn thử **4,88 s/khung** (39,0 phút cho 480 khung, máy sau khởi động lại; lượt trước trên máy nhanh hơn: 3,42 s/khung). Ngoại suy tập 10 phút: **≤ 12 h chỉ ĐẠT trên máy nhanh** (10,6 h với 30 % cảnh relief/2.5D; 8,9 h khi thêm SPP1 bay nhanh + bỏ bóng cảnh xa) — **trên máy chậm KHÔNG ĐẠT** (thấp nhất 13,2 h). Chi tiết §5.3.
5. **Tự chấm 4 lớp** (§6): hero 6/10, nhà thường 6/10, nền sống 4,5/10, ánh sáng/hoàn thiện 5,5/10. Đã hơn bản R&D (hộp trơn, nền phẳng) nhưng **chưa đạt mức "công trình biểu tượng dựng chi tiết" của đối thủ**; điểm yếu lớn nhất: nền vệ tinh 10 m ở cận cảnh và bãi eo đất phẳng.

## 2. Mô-đun và công cụ (việc 1, 2)
### 2.1 Tệp
| Tệp | Vai | Lớp chuẩn hình |
|---|---|---|
| `design/k2v/tl/page.js` | trang dựng: đường ống `post.js` dùng chung (tích luỹ SPP jitter → ACES → grade: lọc cạnh khung SPP1 + **LUT A** + vignette → grain); lớp chữ 2D vẽ sau; kỹ thuật bật/tắt qua `cfg.tech` | 4 |
| `core.js` | tiện ích, mã hoá năm 16 bit, nhiễu GLSL, kết cấu nhiễu nướng sẵn (chống lặp ô) | — |
| `terrain.js` | DTM 20 m (ô 1 km, LOD 20/60 m) + vòng chân trời 150 m; phủ Sentinel-2: nền tự nhiên ↔ nền đô thị theo năm; đá vôi vách dốc; chi tiết gần; **AO nướng sẵn theo năm**; đất khai hoang nổi theo năm | 3 |
| `water.js` | biển thủ tục (Fresnel, sóng, lấp lánh) + vòm trời + sương xa cùng màu chân trời; vẽ sau địa hình | 3, 4 |
| `city.js` + `geom.js` | nhà thủ tục gộp theo ô 500 m, LOD (gần: mái hông ngói + cửa sổ shader; xa: khối; rất xa: ẩn, nền vệ tinh làm impostor); vật liệu theo vùng + thời kỳ; mọc theo năm; ghost | 2 |
| `nature.js` | cây instanced từ NDVI Sentinel-2 + cây OSM (LOD 2 km, bóng theo năm); đường OSM theo năm từng đỉnh (đất trước 1940, nhựa sau) | 3 |
| `heroes.js` + `heroes/*.json` | Tower of Homage (tapia, răng cưa, khe bắn, viền Fresnel), tường lâu đài + tường thành, đường băng 09/27 (vạch ICAO, chắn đường ngang, khung sáng mốc đinh) | 1 |
| `campath.js` | spline Hermite theo thời gian; bay dọc tuyến thật (mốc dày trên hình học OSM); nhật ký lệch tuyến, khoảng cách, tốc độ, đứng yên | ngữ pháp máy |
| `text.js` | ngân sách chữ (port `textBudget` + tương phản WCAG trên điểm ảnh thật); năm + chỉ số, nhãn phương pháp, thẻ, thẻ neo, ảnh chú thích neo 3D, nhãn ghost | chữ |
| `lut.js` | `.cube` 33³ → Data3DTexture; chỉ áp lên cảnh 3D (ảnh sepia, chữ vẽ sau → không qua LUT) | 4 |
| `scenes/gib20.js` | đoạn thử Gibraltar 20 s | — |
| `scripts/k2tl/fetch_osm.py`, `geo.py`, `build_rasters.py`, `build_vectors.py`, `build_scene.py` | tải OSM (API /map chia ô — Overpass 504/ngắt qua proxy); UTM/raster không cần GDAL; gói cảnh: DTM, mặt nạ đất 1987/2026, năm đô thị, năm đất, toà (2 tầng + ghost), đường, cây, hero, AO, vòng xa | — |
| `scripts/k2tl/render.js`, `bench.sh`, `mix.py`, `calib.py` | driver (khung JPG + `log.json`), đo kỹ thuật, trộn âm −14 LUFS, căn góc then/now ≥ 6 điểm | — |

### 2.2 Sửa lỗi R&D đã nêu (`research/timelapse/BAO-CAO.md` §6.3)
| Lỗi R&D | Sửa | Kiểm |
|---|---|---|
| Mặt nước hiện đại có từ năm đầu | `years.png` kênh B/A = năm có đất; terrain hạ đất chưa có xuống −10 m (dưới mặt biển); đường băng `discard` khi đất chưa có | khung kiểm từ trên xuống 1940/1941/1942/1944/1990 (`do/kiem-dat-theo-nam.jpg`): 1940 không đường băng, 1941 chỉ phần trên đất, 1944 đủ phần lấn vịnh, 1990 có Westside 1987 |
| Khung trống đầu phim | không mờ từ đen, không thẻ trễ: khung 0 có địa hình + năm + nhãn phương pháp; thẻ móc từ 0,1 s | khung 0 trong tờ khung (`do/to-khung-20s.jpg`) |
| Cảnh NOW trơn (hộp, nền phẳng) | 4 lớp chuẩn hình (§2.1), nền Sentinel-2 + vòng chân trời, cây, đường | tự chấm §6 |
| Chống răng cưa chỉ MSAA 4× | tích luỹ SPP có jitter (post.js) 2/4 mẫu; khung SPP1 có lọc cạnh; cửa sổ mờ theo `fwidth` | xem cận khung 1080p |
| (thêm) Tường lộn mặt (R&D §6.3 lỗi 0) | hình học thuần `geom.js`, **test bằng tích có hướng** | `test_geom.mjs` 42 tam giác |

Lỗi mới phát hiện và đã sửa trong phiên (ghi để K biết): đáy biển −1,5 m xuyên mặt nước ở xa (depth) → −12 m, near 5 m; tàu lớn bị nhận là đất (NIR) → lọc mảng đất rời có DSM < 0,5 m; bóng cây chưa mọc (vật liệu độ sâu thiếu phép co) → `customDepthMaterial`; nền đô thị hiện sớm 3 năm → không hiện trước năm bằng chứng; đường dài lấy năm sớm nhất cả tuyến → năm theo từng đỉnh; chú thích `//` chèn giữa dòng nuốt mã (lặp **BAI-HOC-LL #42**, 2 lần) → đổi `/* */`, test trình duyệt bắt được.

## 3. Test
| Bộ | Kết quả |
|---|---|
| `scripts/k2tl/tests/test_geo.py` (UTM khứ hồi < 1 mm, điểm chuẩn kinh tuyến trục) | 2/2 ĐẠT |
| `test_calib.py` (máy tổng hợp, 8 điểm, nhiễu 1 px → khôi phục vị trí < 2 m, RMS < 1 % rộng; < 6 điểm phải dừng) | 2/2 ĐẠT |
| `test_geom.mjs` (hướng mặt tường/mái phẳng/mái hông bằng tích có hướng; lồi/lõm; đơn giản hoá vòng) | ĐẠT, 42 tam giác |
| `test_campath.mjs` (spline qua mốc; bay tuyến ≥ 3 s lệch ≤ 15 m; phát hiện đứng yên > 6 s) | ĐẠT |
| `test_browser.js` (SwiftShader: 3 khung gib20, ngân sách chữ, tương phản ≥ 4,5, cỡ ≥ 38 px, năm mốc đinh = 1941, tất định) | ĐẠT (960×540; chữ ≤ 15,7 % ở mốc đinh; tương phản min 9,26; gần tất định: khung 300 dựng lại lệch > 8 mức ở 0,26 % điểm ảnh) |
| Chạy tất cả: `bash scripts/k2tl/tests/run.sh` | **TẤT CẢ TEST ĐẠT** (lần chạy cuối) |

## 4. Đoạn thử Gibraltar 20 s (việc 3)
**Tệp:** `channel-k2/k2c-t3-01/v5b1-thu/gib20_540p.mp4` (bản xem 960×540, 4,5 MB, commit thường) · bản 1080p đầy đủ **ngoài git** (`gib20_1080p.mp4`, 84,9 MB, SHA-256 `fa33873b2b816db35af0bf77934640b06fa121cc73f544b68bb417513f22e9a9`) — chờ duyệt dòng LFS (§10) · 6 khung 1080p ở `khung/` · log ở `do/`.

### 4.1 Nhịp hình (thời gian thật trong `scenes/gib20.js`)
| Giây | Năm | Máy | Chữ |
|---|---|---|---|
| 0–3,2 | 1704→1750 | mở toàn cảnh từ đông-bắc (glide) | nhãn phương pháp 0–4,6 s · thẻ móc "1704 · British and Dutch forces capture Gibraltar" (Gibraltar National Museum, claim C17) 0,1–3,1 s · nhãn ghost "reconstructed from LoC print, 1705" 3,3–4,7 s |
| 3,2–7,4 | →1850 | **glide → zoom-in** Tower of Homage: 2 785 → 124 m (**×22,5**) | thẻ neo "Tower of Homage · stands 23 metres tall" (Ministry for Heritage) 4,8–7,9 s, hero viền Fresnel |
| 7,8–10,8 | 1875→1932 | **bay dọc Winston Churchill Ave** (tim OSM, 3,0 s, cao 54–72 m, lệch TB 0,57 m / tối đa **5,72 m**) | **ảnh LoC 2025710366 "Gibraltar. Neutral ground"** (V.B. Cumbo, c.1900–10) neo điểm 3D trên vùng trung lập 8,0–11,0 s |
| 10,8–12,1 | →1941 | ngẩng lên nhìn La Línea đang mọc, quét về giao lộ | — |
| 12,1–14,0 | **1941 dừng 1,92 s** | **MỐC ĐINH**: quỹ đạo quanh giao lộ; năm phóng 1,45×, vàng; đường băng sáng + khung viền (chỉ phần có đất năm 1941), phần còn lại mờ (giảm bão hoà 55 %, tối 36 %) | thẻ neo "1941 · A runway is built across the only road" (HMGoG 177/2023, C33) 12,1–15,2 s |
| 14,4–20 | 1946→2026 | **reveal kéo lùi** 411 → 5 748 m (**×14,0** trong 7,4 s): đường băng lấn vịnh (1943), La Línea bùng nổ 1950–2000, Westside (1987→2026) | màn kết 18,6–20 s: "© OpenStreetMap contributors · Copernicus Sentinel data 2026" |

Máy không đứng yên khung nào (đứng yên dài nhất 0 s). **Tốc độ góc lớn nhất 226 °/s** ở cú quét 11,2–11,6 s (≈ 0,4 s) — nhanh; ghi để chấm mù xét.

### 4.2 Dữ liệu và bằng chứng theo năm
| Lớp | Nguồn | Cách dùng |
|---|---|---|
| Địa hình | Copernicus GLO-30 DSM N36 W006 (SHA `3995ee21…` khớp tiền kỳ T3) | DTM = mở hình thái DSM trong vùng có toà; vòng xa 150 m |
| Mặt đất 2026 | Sentinel-2 L2A **S2C_30STF_20260415_0** (TCI + B08). Cảnh 24/09 trong tai-san.json có **mây đúng trên Rock**; cảnh 22/04 cụt mép dải quét → chọn bằng lớp SCL: 0,12 % mây, 0 % trống trong vùng cắt | màu đô thị thật; vùng nhân tạo vá thành nền tự nhiên cho năm cũ; NDVI → cây |
| Đất 1987 | **Landsat 5 TM C2 L2 LT05_L2SP_201035_19870726** (USGS, công cộng; tải qua Planetary Computer vì `landsatlook` đòi đăng nhập) | mặt nạ đất 1987 (NIR, Otsu); khác biệt 1987→2026 = khai hoang (Westside, cảng La Línea, bờ đông) |
| Toà La Línea | **Catastro INSPIRE BU 11022** (D.G. del Catastro; 11 141 toà, 26 087 phần toà có số tầng; năm 1849–2025; 14 toà không năm → không mọc) | TẦNG ĐẦY ĐỦ, cao = số tầng × 3,0 m |
| Toà Gibraltar | OSM (2 451 toà; 110 có số tầng/cao; còn lại ước từ phần nhô DSM) | TẦNG CHUẨN: ghost 1704 (phố trong tường, 356 toà) · ghost 1880 (sườn tây, 1 198 toà — ảnh LoC 94512284 J. Laurent 1860–80) · khối đặc 1987 (Landsat) / 2026 |
| Lõi La Línea c.1900 | ảnh LoC 2025710366 + vị trí toà Catastro còn đứng xây ≤ 1930 | ghost từ 1900 cho 12 465 phần toà xây sau 1900 trong lõi |
| Đường băng | HMGoG 177/2023 (1941) · HMGoG 199/2018 (lấn vịnh 11/1941 → 07/1943) | đất lấn vịnh nổi 1941→1943; đường băng từ 1941 |
| Dân số | **Census of Gibraltar 2022 Report, Bảng 1** (24 kỳ đếm 1753–2022; PDF SHA `a1527efe…`) | chỉ số trên-phải; "≈" giữa hai kỳ (nội suy log); ẩn trước 1753 |
| Ảnh | LoC 2025710366 (TIF gốc SHA `e12f08e7…`) | ảnh chú thích neo 3D (sepia nhẹ, không LUT) |

**Năm giả không mọc:** Gibraltar không có năm xây mở → không toà nào mọc giữa hai mốc; thời điểm ghost/khối đặc là mốc bằng chứng sớm nhất. Hệ quả cần biết: Gibraltar ngoài phố cổ hiện ghost từ 1880 và chỉ thành khối đặc ở mốc 1987 — đúng nguyên tắc nhưng thưa so với thực tế 1900–1980. Cần bản đồ lịch sử có quyền cho các mốc giữa (§12).

### 4.3 Âm
`scripts/k2tl/mix.py` + `v5b1-thu/cues.json`: nhạc K2-MUS-1 "Half Mystery" (−17 LUFS nền); còi tàu lúc mở vịnh (K2-SFX-9), màn trập khi ảnh LoC hiện (K2-SFX-26), nhịp trầm tự tổng hợp khi năm dừng 12,1 s, công trường lúc bùng nổ (K2-SFX-24), giao thông ở hiện tại (K2-SFX-16), "tích" tự tổng hợp khi thẻ hiện. **Master −14,0 LUFS, đỉnh −1,6 dBTP** (ebur128 trên mp4 1080p); bản xem 540p −14,5 LUFS / −2,9 dBTP. Không lời, ElevenLabs 0.

## 5. Giờ máy (việc 5)
### 5.1 Đoạn thử (1080p, 480 khung, lượt cuối)
| Nhịp | SPP | s/khung |
|---|---|---|
| S1 mở 0–3,2 s | 2 | 4.05 |
| S2 glide→tháp 3,2–7,8 s | 2/4 | 5.68 |
| S3 bay tuyến 7,8–10,8 s | 1/2 | 2.56 |
| S4 quay + mốc đinh 10,8–14,4 s | 1/2/4 | 7.26 |
| S5 reveal 14,4–20 s | 2 | 4.41 |
| **Cả đoạn** | thích ứng | **4,88** (39,0 phút) |

### 5.2 Kỹ thuật → s/khung (1080p, SPP2 trừ khi ghi; 3 khung đại diện — toàn cảnh 470, cận tháp 168, eo đất 360 — mỗi khung dựng 2 lần, lấy lần 2; **11 lượt liền nhau trên cùng máy** `bench-final.jsonl`)
| # | Kỹ thuật | s/khung | so với nền 4,84 s* |
|---|---|---|---|
| A | Nền: LOD toà/cây + LOD địa hình + bóng 1 lần/khung + AO nướng theo năm + Lambert | 4,90 / 4,79 / 4,45 (lặp lại 3 lượt → nhiễu đo ±5 %) | — |
| K | Tắt bóng (dùng cho cảnh xa, bóng không thấy ở > 3 km) | 3,96 (cặp với A 4,45 chạy liền) | **−11 %** |
| B | **Tắt LOD toà + cây** | **8,26** | **+71 %** → LOD là kỹ thuật lớn nhất |
| C | Tắt LOD địa hình (một lưới 20 m) | 5,14 | +6 % |
| D | Tắt "bóng 1 lần/khung" (bóng dựng lại mỗi mẫu SPP) | 4,97 | +3 % (khung đứng; khi năm đổi bóng cập nhật mọi khung — lượt dựng: 480/480 khung cập nhật) |
| E | Tắt AO nướng theo năm | 4,67 | −4 % (AO tốn 0,2 s; giữ vì chất lượng chân toà) |
| F | Nhiễu nướng sẵn → nhiễu thủ tục | 4,65 | −4 % → nướng sẵn KHÔNG lợi sau chống lặp ô; **tắt mặc định** |
| G | Tắt cây | 4,68 | −4 % |
| H | Lambert → PBR (Standard) | 4,92 | +1 % |
| I | **SPP1** + lọc cạnh | **2,69** | −45 % |
| J | **SPP4** | **9,09** | +88 % |
| — | SPP3 (lượt riêng) | 6,16 | — |
| — | Bóng 2048 thay 4096 (lượt máy trước) | +4 % | không lợi |
| — | **Chia ô ≤ 300 nghìn toà:** ×5 (142 690 toà, 3,5 triệu tam giác gần) | 4,50 (+5 % so lượt cùng máy 4,28) · RSS nạp 4,5 GB | chạy được |
| — | ×10 (285 380 toà) | **trình duyệt sập** (không ra log) | trần thực tế của mô-đun (2 mức LOD giữ trong bộ nhớ) ≈ **150 nghìn toà/cảnh** — thấp hơn R&D (300 nghìn, 1 hình học) |
| — | Dùng lại lớp nền cho cảnh lặp góc | không áp được trong đoạn thử (máy không bao giờ đứng yên) — chi phí nền (địa hình + nước + trời) đo gián tiếp: tắt toà chỉ −4 % ⇒ nền ≈ 85–90 % giờ khung; lợi chỉ khi có cảnh khoá góc |
| — | Xen cảnh relief/2.5D có sẵn | 1,98 s/khung (đo NT 15/10, `RUNBOOK` §7) |

\* Máy bị khởi động lại giữa phiên; máy sau chậm hơn máy trước ≈ 45 % ở cùng cấu hình (SPP2: 3,27 → 4,8 s). Bảng trên chỉ dùng số **cùng máy, liền nhau**. Lượt dựng cuối của đoạn thử chạy trên máy sau.

Ba lượt tối ưu đã áp trước bảng (đo trên máy trước): LOD địa hình + cây 20 mặt + vẽ nước/trời sau địa hình: 3,66 → 3,28 s (−10 %); phát hiện thời gian thật nằm ở bước đồng bộ GPU→canvas (lệnh GL xếp hàng), nên đo bằng thời gian tường mỗi khung.

### 5.3 Ngoại suy tập 10 phút (14 400 khung)
Số đo dùng (máy B = máy của lượt dựng cuối; máy A = máy trước khởi động lại, chậm hơn ×1,48 ở cùng cấu hình): SPP1 2,50 s · SPP2 4,40 s · SPP4 8,65 s (máy B, lượt dựng cuối) · relief/2.5D 1,98 s (NT 15/10, máy kiểu A; quy đổi máy B ≈ 2,93 s **(ước)**) · tắt bóng ở cảnh xa −11 % (lượt K).

| # | Kịch bản (14 400 khung) | s/khung máy B | giờ máy B | giờ máy A **(ước ÷1,48)** |
|---|---|---|---|---|
| 1 | 100 % cảnh 3D, tỉ lệ SPP như đoạn thử (SPP4 18 %, SPP1 15 %) | 4,88 (đo) | **19,5 h** | 13,2 h |
| 2 | 100 % 3D, nhịp tập thật: SPP4 5 % (4 mốc đinh + 6 cận hero), SPP1 15 %, SPP2 80 % | 4,33 | 17,3 h | 11,7 h |
| 3 | như 2 + 30 % cảnh relief/2.5D/ảnh lưu trữ có sẵn | 3,91 | 15,6 h | **10,6 h** |
| 4 | như 3 + SPP1 cho mọi khung bay nhanh (50 %) + tắt bóng ở cảnh xa (40 %) | 3,30 **(ước)** | 13,2 h | **8,9 h** |

**Trần 12 h: ĐẠT trên máy A ở kịch bản 3–4; KHÔNG ĐẠT trên máy B ở mọi kịch bản (thấp nhất 13,2 h).** Biến thiên giữa hai container cùng loại CPU (×1,48) lớn hơn lợi ích của mọi kỹ thuật trừ LOD và SPP. Số "trong ±5 % quanh ngưỡng": không có (gần nhất 11,7 h máy A kịch bản 2 = −2,5 % dưới 12 h → **nêu tên**: nằm trong ±5 %).

**Kết luận:** với CPU hiện có, tập 10 phút toàn cảnh 3D theo nhịp hiệu ứng dày như đoạn thử **vượt 12 h**. Đạt ≤ 12 h khi: (a) SPP4 chỉ ở mốc đinh/cận hero (≈ 5 % thời lượng), SPP1 khi bay nhanh, và (b) ≥ 25–30 % thời lượng là cảnh relief/2.5D/ảnh lưu trữ có sẵn — đúng ngữ pháp kênh (Kinh thánh §4: bản đồ nổi, hồ sơ thật 10–15 %). Nếu tập cần > 75 % cảnh 3D, cần GPU (NT K6 đang hoãn) hoặc chấp nhận 14–16 h.

### 5.4 Chỉ số trong ±5 % quanh ngưỡng (luật cứng CLAUDE.md)
| Chỉ số | Đo | Ngưỡng | Lệch |
|---|---|---|---|
| Năm dừng ở mốc đinh | 1,92 s | 1,5–2,0 s | −4 % dưới trần trên |
| Giờ máy tập 10 phút, máy A kịch bản 2 | 11,7 h | ≤ 12 h | −2,5 % |
| Diện tích vòng chân tháp OSM so với nguồn | 334,1 m² | 320 m² | +4,4 % |
| Phóng hộp năm ở mốc đinh | 1,45× | ≥ 1,4× | +3,6 % |
| Nhãn phương pháp đầu phim | 0–4,6 s | 4–6 s | trong khoảng (mép dưới +15 %) — không sát |

## 6. Khung tĩnh 1080p và tự chấm 4 lớp (việc 4)
Tệp `channel-k2/k2c-t3-01/v5b1-thu/khung/` (lấy từ lượt dựng cuối, đủ lớp chữ như bản phát):
| Tệp | Khung | Loại |
|---|---|---|
| `toan-canh-1-mo-dau-1704.jpg` | 10 | toàn cảnh |
| `toan-canh-2-ket-2026.jpg` | 476 | toàn cảnh |
| `can-hero-1-thap-homage.jpg` | 168 | cận hero |
| `can-hero-2-duong-bang-moc-dinh-1941.jpg` | 312 | cận hero (mốc đinh) |
| `pho-eo-dat-1-bay-tuyen-c1900.jpg` | 214 | eo đất (bay tuyến + ảnh neo) |
| `pho-eo-dat-2-la-linea-1916.jpg` | 240 | eo đất / phố La Línea xa |

**Thước 4 lớp (tự chấm, 0–10; điều phối chấm mù với đối thủ ngoài repo):**
| Lớp | Điểm | Đạt | Chưa đạt |
|---|---|---|---|
| 1 Hero | 6 | tháp đúng vòng chân + cao có nguồn, tapia có lớp đầm, răng cưa, khe bắn, viền Fresnel; đường băng đủ vạch ICAO, chắn đường ngang, năm 1941/1943 đúng nguồn | chi tiết tháp còn "khối + kết cấu" (không cửa vòm, không mặt bằng tầng, răng cưa ước); tường lâu đài như dải; không có CC0 phù hợp; nhà ga/đường hầm 2023 chưa dựng |
| 2 Nhà thường | 6 | 28 538 toà, mái hông ngói cho nhà thấp cũ, phẳng cho nhà mới, màu theo vùng/thời kỳ, cửa sổ + chớp + cửa hiệu bằng shader, cao từ số tầng thật (La Línea) | Gibraltar cao ước từ DSM; mái hông dạng chóp đơn giản; không ban công/lan can; nhìn gần vẫn "khối sạch" |
| 3 Nền sống | 4,5 | địa hình thật + vòng chân trời, ảnh vệ tinh 2026 tự nhiên/đô thị theo năm, cây instanced, đường theo năm (đất → nhựa), mặt nước theo năm | ở cận cảnh ảnh 10 m mờ; bãi eo đất năm cũ là màu vá phẳng; cây là khối tròn đơn giản; không quảng trường/vỉa hè riêng; sườn Rock loang |
| 4 Ánh sáng/hoàn thiện | 5,5 | nắng tây-nam + trời, bóng mềm PCF, AO tiếp đất nướng theo năm, sương xa, 1080p, SPP2–4, LUT A chỉ trên cảnh 3D, grain chung | sương hơi xám/đục ở toàn cảnh; không AO trong (SSAO); bầu trời phẳng, không mây |

## 7. Giấy phép và nguồn (hero, tài sản, dữ liệu)
Tệp giấy phép ở `channel-k2/k2c-t3-01/v5b1-thu/licenses/` (mới: `osm-odbl.txt`, `catastro-inspire-bu.txt`, `usgs-landsat.txt`; chép từ tiền kỳ T3 bằng `git show`: Copernicus DEM, Sentinel, LoC 2025710366, 2016646782, 94512284). Tệp thô ngoài git ở `$K2TL_CACHE` (`/var/tmp/cine-out/k2tl-cache`).
| Tài sản | Giấy phép | Ghi công | SHA-256 |
|---|---|---|---|
| Copernicus GLO-30 N36 W006 | Copernicus WorldDEM-30 (thương mại được) | câu ghi công đầy đủ ở mô tả | `3995ee2187c0…` |
| Sentinel-2 S2C_30STF_20260415_0 TCI / B08 | Copernicus Sentinel legal notice | "Contains modified Copernicus Sentinel data 2026" (mô tả; trên hình rút gọn ở màn kết) | `316119e38d4c…` / `37a312ebae91…` |
| Landsat 5 LT05 19870726 (B1–B5) | USGS — U.S. Public Domain | "Landsat imagery courtesy of USGS" (khuyến nghị) | nir `c4b7f4185977…` (đủ 5 tệp trong `do/sha256.txt`) |
| Catastro INSPIRE BU 11022 | dùng miễn phí mọi trường hợp, ghi D.G. del Catastro (câu `<rights>` dịch vụ tải; trang giấy phép riêng 404) | "Source: Dirección General del Catastro" | `3ff87a71b80c…` |
| OpenStreetMap (19 ô API /map) | ODbL 1.0 | "© OpenStreetMap contributors" (trên hình màn kết) | ô thô ngoài git |
| LoC 2025710366 "Neutral ground" | No known restrictions on publication | "Library of Congress, V.B. Cumbo" | TIF `e12f08e7a393…` |
| LoC 2016646782 (1705), 94512284 (1860–80) | No known restrictions (94512284: ngoài Mỹ có thể hạn chế; tác giả J. Laurent mất 1886) | chỉ dùng làm bằng chứng mốc, **không lên hình** | `fae6c37ef43e…` / `a8a3b85ff46c…` |
| Census of Gibraltar 2022 Report | văn bản chính phủ — chỉ trích số | "Census of Gibraltar" | `a1527efede9e…` |
| HMGoG 199/2018 | trích số | — | (PDF ngoài git) |
| LUT A `k2-a-thep-lanh.cube` | tự tạo (V5a) | — | `4e3ba0a0e8c5…` (đọc từ `origin/v5a`) |
| Nhạc/SFX | đã có dòng RIGHTS (K2-MUS-1, K2-SFX-9/16/24/26) | CC BY 4.0 | — |
| Hero | dựng thủ tục, không tài sản CC0 (V5a không có mô hình phù hợp) | — | nguồn số đo: `design/k2v/tl/heroes/*.json` |

## 8. Điểm gắn vào `scripts/k2/render.js` / `lib/k2.js` cho V5b-2 (sau T2 G2)
1. **`scripts/k2/hero.js`** (trang theo tên cảnh): thêm nhánh `--hero tl/<cảnh>` → trang `design/k2v/tl/page.js`. Cần thêm ở `page.js` hợp đồng của trang k2v: `window.finalize(f)` (RGB base64, không vẽ chữ) và `window.anchorsAt()` (neo: tháp, giao lộ, điểm ảnh LoC, ghost) — hiện `renderFrame` trả JPEG đã có chữ.
2. **`scripts/k2/lib/k2.js`**: thêm mẫu lớp 2D `tl` (năm dưới-trái + chỉ số trên-phải 1 dòng, "≈" nội suy, phóng 1,45× ở mốc đinh; thẻ neo; ảnh chú thích neo; nhãn ghost) — chuyển logic từ `design/k2v/tl/text.js` để mọi cảnh kênh 2 đo ngân sách chữ cùng một chỗ.
3. **`scripts/k2/render.js`**: SPP theo trạng thái cảnh (`state(t).spp` — 4 mốc đinh/cận hero, 2 thường, 1 + lọc cạnh khi bay nhanh) thay `--spp` cố định; ghi `log.json` s/khung từng khung.
4. **LUT A vào grade của `design/k2v/page.js`** (cảnh tự nhiên/footage, không sepia) — dùng `lut.js` + `GRADE_GLSL`.
5. **`scripts/k2/prep.py`**: `type: scene3d`, `scene_id: tl/<cảnh>`, preset máy trong `cams.yaml` (glide-zoom, line-flight, pin-orbit, reveal-pull) — tính trùng (scene_id, camera_id) như hiện hành.
6. **`scripts/common/versions.py`**: nhóm mới `k2tl` (`design/k2v/tl`, `scripts/k2tl`).
7. **`scripts/env/setup.sh` + `verify.sh`**: `imagecodecs` (đọc GeoTIFF nén dự đoán số thực — Copernicus) — đã cài tay trong phiên.
8. **Phiên K**: viết luật TL-Q1…Q5 (đề xuất R&D §6.8) đo trên `log.json` + `campath.json` của driver này; thêm (đề xuất) TL-Q6 "năm giả không mọc": toà tầng chuẩn chỉ đổi trạng thái tại năm mốc có nguồn.

## 9. Chi phí
| Khoản | Trần | Thực tế |
|---|---|---|
| Claude API | $3 | **$0** (không gọi; không có `cost.jsonl` vì không có lượt nào) |
| ElevenLabs | 0 | 0 |
| YouTube Data API | 0 | 0 |
| Giờ máy dựng/đo | ≤ 4 h | **≈ 2,5 h** (đo: hai lượt dựng trọn đoạn 27,4 + 39,0 phút; ước theo log: 40 lượt đo kỹ thuật/khung kiểm ≈ 60 phút, dựng gói cảnh + tải ≈ 15 phút, test ≈ 10 phút) |
| Tải mạng | — | ≈ 1,6 GB (Sentinel-2 2 cảnh ≈ 1,14 GB, Landsat 0,25 GB, DEM 38 MB, Catastro 6 MB, OSM 70 MB, LoC 26 MB, PDF 18 MB) |
| Token phiên | trần mềm | chưa đọc được (chủ dự án xem Usage); không dùng tác tử con |

Đề xuất dòng `COST-LEDGER.csv` (P ghi — ngoài vùng lệnh): `V5b1,Xương sống thời gian + đoạn thử Gibraltar,V,2026-10-16,,,,,0,3,—,0,0,≈ 2,5,,0,20,,reports/V5B1-BAO-CAO.md,YouTube 0; không merge`

## 10. Đề xuất ngoài vùng (chưa ghi)
1. **`tools/lfs-allow.txt`**: thêm `channel-k2/*/v5b1-thu/*-1080p.mp4` để đẩy bản 1080p đầy đủ (84,9 MB) qua LFS — chủ dự án duyệt.
2. **`RIGHTS.md`** (V5b1-01…06): Copernicus GLO-30; Sentinel-2 S2C_30STF_20260415_0; Landsat 5 LT05 19870726 (USGS PD); Catastro INSPIRE BU 11022; OpenStreetMap ODbL (dữ liệu toà, đường, đường băng); ảnh LoC 2025710366 (dùng trên hình). LoC 2016646782 / 94512284 chỉ là bằng chứng mốc — ghi "không hiển thị".
3. **`channel-k2/.gitignore`**: thêm `!k2c-t3-01/v5b1-thu/**/*.json` (phiên này `git add -f` như phiên tiền kỳ).
4. **`AUTHORSHIP.md`**: ghi quyết định sáng tạo cần chủ dự án duyệt — cách kể 5 nhịp; ghost "pale blocks"; chọn mốc đinh 1941 thay 1704.
5. **`scripts/env/setup.sh`**: `imagecodecs`.

## 11. Preflight, ghép thử
- Hook pre-commit/pre-push cài đầu phiên (`ln -sf ../../tools/preflight.sh .git/hooks/…`); `bash scripts/env/verify.sh` đầu phiên: 10 PASS, 3 FAIL (three.js, tifffile/pyshp, k2v node_modules) → đã cài theo hướng dẫn của verify → **13 PASS**. Thêm `imagecodecs` (cần cho GeoTIFF Copernicus).
- `bash tools/preflight.sh --range origin/main..HEAD`: **ĐẠT** (58 tệp), `checks/lock.py --verify`: **KHỚP**. Không dùng `--no-verify`. Mọi tệp commit ≤ 5 MB (lớn nhất `gib20_540p.mp4` 4,5 MB); bản 1080p (84,9 MB) ngoài git.
- **Ghép thử** (`git merge-tree`) với `origin/main`, `k2c-t2`, `k2c-t3-tienky`, `v5a`, `timelapse-rd`, `nen-tang`, `am-thanh`: **sạch** (chỉ thêm tệp mới trong 4 vùng).
- Tiến trình nền: chạy bằng công cụ nền của harness. Một lượt dựng bị harness dừng ở giới hạn 30 phút (khung 356/480) → dựng tiếp 336–479; tiến trình trình duyệt còn sót dừng bằng PID (không `pkill -f`).

## 12. Việc chờ chủ dự án
1. **Duyệt mô-đun + đoạn thử** (`v5b1-thu/gib20_540p.mp4`, 6 khung) và **chấm mù với đối thủ** (điều phối, ngoài repo).
2. **Giờ máy:** chấp nhận ngoại suy §5.3 (≤ 12 h chỉ khi ≥ 25–30 % cảnh relief/2.5D và SPP4 ≤ 5 %) — hoặc mở lại GPU (NT K6).
3. **Bản đồ lịch sử có quyền cho Gibraltar 1900–1980** (vd. bản đồ quân sự/Admiralty PD) để tầng chuẩn không nhảy từ ghost 1880 sang khối 1987.
4. **Đối chiếu bằng mắt** trang Ministry for Heritage (403 cho máy) cho số 23 m / 320 m² của Tower of Homage.
5. **Duyệt dòng LFS** (§10.1), dòng RIGHTS/COST-LEDGER/AUTHORSHIP/.gitignore (§10) — P ghi.
6. **Trần toà/cảnh ≈ 150 nghìn** với mô-đun hiện tại (×10 = 285 nghìn làm sập trình duyệt) — chấp nhận, hay giao V5b-2 thêm chế độ 1 mức LOD/giải phóng bộ nhớ cho thành phố lớn.
7. Cú quét 226 °/s (11,2–11,6 s): giữ hay kéo dài nhịp ở bản tập.
