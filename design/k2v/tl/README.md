# design/k2v/tl — XƯƠNG SỐNG THỜI GIAN (Moving Parts = NƠI CHỐN + CƠ CHẾ + THỜI GIAN)

Phiên V5b-1 (16/10/2026), chủ dự án duyệt Y1–Y7, Z1–Z2. Port từ `lab/timelapse/` (nhánh `timelapse-rd`) thành mô-đun dùng lại được.
**Chỉ CPU** (Chromium headless; V5b-2a: **Mesa llvmpipe mặc định**, SwiftShader giữ được — biến môi trường `K2TL_GL`). Mô-đun MỚI, độc lập: chỉ *import* `design/cong3/shared/post.js` và three.js 0.180 của `design/cong3/shared`;
**không sửa** `design/k2v/*.js`, `scripts/k2/**` (T2 đang dựng). Điểm gắn vào `render.js`/`k2.js` cho V5b-2: `reports/V5B1-BAO-CAO.md` §8.

## Hai tầng thời gian
| Tầng | Khi nào | Cách mọc | Ví dụ Gibraltar |
|---|---|---|---|
| **CHUẨN** (mọi tập) | luôn có | vùng đô thị / mặt đất / mặt nước đổi theo **mốc bằng chứng** (bản đồ, ảnh, vệ tinh) + bộ đếm; **không nội suy năm** giữa mốc | 1704 phố trong tường (bản in LoC 1705) · 1880 sườn tây (ảnh LoC J. Laurent 1860–80) · 1941–43 đường băng lấn vịnh (HMGoG) · 1987 (Landsat 5) · 2026 (Sentinel-2) |
| **ĐẦY ĐỦ** | khi có năm xây từng toà | mỗi toà hoàn thành đúng năm (mọc trong 4 năm trước đó) | La Línea: Catastro INSPIRE `dateOfConstruction` + số tầng |
| **GHOST** | vùng có bằng chứng, không biết toà cụ thể | khối mờ ≤ 12 m (screen-door + tích luỹ SPP), không đổ bóng; nhãn "reconstructed from <nguồn, năm>" | phố cổ 1704; lõi La Línea c.1900 (ảnh LoC + toà còn đứng ≤ 1930) |

## Tệp
| Tệp | Vai |
|---|---|
| `page.js` | trang dựng: đường ống post.js (tích luỹ SPP jitter → ACES → grade: lọc cạnh SPP1 + **LUT A** + vignette → grain), lớp chữ 2D vẽ sau; `window.setup/renderFrame/camLog/budgetAll`; kỹ thuật bật/tắt `cfg.tech` |
| `core.js` | tiện ích, mã hoá năm 16 bit, nhiễu GLSL, **kết cấu nhiễu nướng sẵn** |
| `terrain.js` | lớp 3: DTM (20 m gần / 60 m xa, **LOD theo ô 1 km**), vòng chân trời 150 m; **V5b-1b: ≤ 2,6 km vật liệu thủ tục theo 13 lớp nền** (`cls.png` từ build_scene `--cls`: cát, cỏ khô/garrigue, maquis, đá vôi, ruộng, nhựa, nền lát, sân thể thao, bãi đỗ, bê tông cảng, đất trống, cỏ công viên, đồng cỏ eo đất) — vệ tinh chỉ để phân lớp + tông vùng mờ, ảnh vệ tinh chỉ ở xa; vách dốc → đá vôi; **AO nướng sẵn theo năm**, đất khai hoang nổi theo năm (chỉ vùng nối biển) |
| `water.js` | biển (sóng thủ tục, Fresnel, lấp lánh) + vòm trời **gradient xanh + mây tích thưa** (V5b-1b); vẽ sau địa hình |
| `city.js` | lớp 2: toà thủ tục gộp theo ô 500 m, **LOD**; **V5b-1b: 6 kiểu mặt đứng × 6 kiểu mái** (hai mái, mái hông có nóc, chóp, phẳng, tường chắn, sân thượng có bồn nước), cửa sổ căn giữa từng mặt (khung, kính phản trời, chớp lá sách, bậu, lanh tô, gờ), ban công sàn + lan can đục song, chia lô khối Gibraltar lớn, mọc theo năm, lớp tái dựng |
| `geom.js` | hình học thuần (test Node: hướng mặt bằng tích có hướng) |
| `nature.js` | cây instanced (NDVI + OSM, LOD 2 km, bóng theo năm) + đường OSM theo năm từng đỉnh |
| `heroes.js` + `heroes/*.json` | lớp 1: Tower of Homage — **V5b-1b: chân choãi, bậc thềm + cửa vào vòm, cửa sổ vòm 2 tầng, răng cưa mũ chóp kiểu Moor, gờ đá + lầu cầu thang trên sàn đỉnh, tháp góc tường lâu đài**, tapia lớp đầm loang theo năm; tường thành; đường băng 09/27 (vạch ICAO, chắn đường ngang); **mốc 1941: trạm biên giới + xe/người A-lite** — tệp nguồn kích thước ở `heroes/` |
| `ships.js` | V5b-1b: tàu theo thời kỳ (buồm 1704–1860, thuyền/hơi nước 1860–1965, tàu hàng/dầu/khách 1965–2026) — nội dung trung cảnh vịnh |
| `campath.js` | ngữ pháp máy quay: Hermite theo thời gian, **bay dọc tuyến thật** (mốc dày trên hình học), nhật ký lệch tuyến/khoảng cách/tốc độ/đứng yên. **V5b-2a: preset** `lienHoan` (bay thấp dọc tuyến → speed ramp → orbit quanh hero + năm dừng → crane up → rise-and-reveal), `pushIn` (giữ hơi), `boundaryTrace`, `follow`, `lateral`, `topDownRise`, `vertigo`; mỗi cú khai `vai` (co-che / buoc-ngoat / he-qua); `grammar()` ghép cú (+ `cuts`), `sppOf(pha)` (bay nhanh SPP1 · orbit/mốc đinh/cận hero SPP4 · còn lại SPP2), `grammarLog()` ghi mỗi khung preset/vai/pha/AGL/năm/s/°/s và tổng kết mỗi cú so `LIMITS` (≤ 10 năm/s, ≤ 90 °/s, orbit 4–6 s, năm dừng 1,5–2 s) và `ALT_MAX` (HH2: phố ≤ 120 m; eo đất/sông/đại lộ ≤ 300 m) |
| `overlay3d.js` | V5b-2a: dải màu hai bên RANH GIỚI thật theo số (boundary trace) + xe A-lite chạy dọc tuyến (follow-object) |
| `text.js` | **ngân sách chữ**: năm + chỉ số (2 lớp thường trực), nhãn phương pháp đầu/cuối, ≤ 1 thẻ, thẻ neo, ảnh chú thích neo điểm 3D, nhãn ghost; đo % diện tích, vùng giữa, tương phản WCAG trên điểm ảnh thật |
| `lut.js` | LUT .cube → Data3DTexture, áp trong grade (chỉ cảnh 3D; ảnh sepia/chữ vẽ sau); **V5b-1b: `uLutMode` 1 = LUT A chỉ vùng tối + vibrance 0,35** (chọn bằng số đo, `reports/V5B1B-BAO-CAO.md` §2) |
| `scenes/gib20.js` | đoạn thử Gibraltar (V5b-2a: 24,5 s, đoạn giữa là MỘT cú liên hoàn WCA → orbit giao lộ 1941 → crane → reveal) |
| `scenes/presets.js` | V5b-2a: cuộn minh hoạ 6 preset (4,5 s mỗi cú, nối bằng cắt) — không phải phim |

## Chạy (công cụ ở `scripts/k2tl/`)
```bash
export K2TL_CACHE=/var/tmp/cine-out/k2tl-cache            # dữ liệu thô + gói cảnh, NGOÀI git
python scripts/k2tl/fetch_sources.py && python scripts/k2tl/fetch_osm.py --name gib --bbox=-5.385,36.105,-5.320,36.185   # V5b-1b: tải lại + kiểm SHA
# tải tay (lệnh trong reports/V5B1-BAO-CAO.md §7): Copernicus GLO-30, Sentinel-2 S2C_30STF_20260415_0 (TCI+B08), Landsat 5 1987 (Planetary Computer), Catastro BU 11022, ảnh LoC, LUT A (git show origin/v5a)
python scripts/k2tl/build_rasters.py --name gib && python scripts/k2tl/build_vectors.py --name gib && python scripts/k2tl/build_scene.py --name gib --ao --far --cls
bash scripts/k2tl/env_check.sh                                                               # V5b-2a: Mesa 25.2.8 / LLVM 20 + renderer WebGL thật của hai trình dựng
python scripts/k2tl/build_border.py --name gib                                               # V5b-2a: biên giới OSM admin_level=2 → lines.json "border" + số toà theo năm
K2TL_GL=llvmpipe node scripts/k2tl/render.js --scene gib20 --pack gib --w 1920 --h 1080 --out <thư mục>   # khung JPG + log.json (renderer, s/khung, spp, pha, LOD, chữ, đường dẫn neo); K2TL_GL=swiftshader cho khung vàng cũ
node scripts/k2tl/render.js --campath <tệp>   |   --budget <tệp>                            # nhật ký máy quay + ngữ pháp (grammarLog) / ngân sách chữ + vai chữ + đường dẫn mọi khung (không dựng hình)
python scripts/k2tl/anchor_dev.py <campath.json> <log.json|text-budget.json>                  # V5b-2a: lệch đầu đường dẫn ↔ điểm chiếu 3D (TL-Q4b, ≤ 1 % rộng khung)
node scripts/k2tl/render.js --maskonly <ra.json>                                               # % nội dung (hình học + nền phố) + hero_pct (id hero) MỌI khung — lượt RIÊNG
python scripts/k2tl/measure_look.py <ảnh…>                                                   # bão hoà / colorfulness / chi tiết / cháy sáng (640×360, vùng giữa)
bash scripts/k2tl/bench.sh <ra.jsonl> "470,175,300,470,175,300" '{"spp":2,"lod":false}' nhãn   # đo kỹ thuật → s/khung
python scripts/k2tl/mix.py --cues channel-k2/k2c-t3-01/v5b1-thu/cues.json --dur 20 --out mix.wav   # −14 LUFS
python scripts/k2tl/calib.py <điểm-khống-chế.json>                                           # then/now ≥ 6 điểm
bash scripts/k2tl/tests/run.sh                                                               # test
```
Python: `/opt/cine/bin/python` (+ `imagecodecs` cho GeoTIFF nén dự đoán — thêm trong phiên, đề xuất đưa vào `scripts/env/setup.sh`).

## Kỹ thuật CPU (đo trong `reports/V5B1-BAO-CAO.md` §5)
`tech`: `lod` (toà/cây theo khoảng cách), `terrainLod`, `ao` (AO nướng theo năm), `shadowCache` (bóng 1 lần/khung, giữ khi khoá cảnh không đổi), `shadows`,
`spp` (`'adaptive'` theo cảnh: 4 cận hero/mốc đinh, 2 thường, 1 + lọc cạnh khi bay nhanh), `baked` (nhiễu nướng sẵn), `lambert`, `treeDetail`, `city`, `trees`, `shadowRes`.

## V5b-1b (16/10/2026) — vòng sửa CHUẨN HÌNH sau cổng TRƯỢT lần 1
Ánh sáng/màu, nền phân lớp thủ tục, nhà đầy đủ + lớp tái dựng, hero 6 đặc điểm, tàu, xe/người 1941, bố cục máy ≥ nội dung, tốc độ góc ≤ 90 °/s. Số đo trước → sau: `reports/V5B1B-BAO-CAO.md`.

## V5b-2a (16/10/2026) — llvmpipe + ngữ pháp máy + số liệu cho bộ kiểm 1.12
- **Trình dựng (GG1):** `K2TL_GL=llvmpipe` (mặc định, `--use-gl=angle --use-angle=gl-egl`) | `swiftshader`. Mỗi lượt đọc `UNMASKED_RENDERER` và **DỪNG mã 6** nếu không đúng trình dựng yêu cầu; chuỗi renderer ghi vào `log.json`, `--campath`, `--budget`, `--maskonly`. `scripts/k2tl/env_check.sh` kiểm Mesa 25.2.8 / LLVM 20. Test trình duyệt chạy cả hai trình dựng.
- **Ngữ pháp máy (JJ1, KK1):** preset ở `campath.js` (bảng trên); log `grammarLog` trong `--campath`.
- **Số liệu cho checks 1.12 (K §7.1):** mặt nạ MỌI khung + `hero_pct` theo id hero (`heroes.heroIds`: tower = 1, crossing = 2; kênh B của mặt nạ); log chữ mọi khung có thẻ/ảnh/nhãn neo; vai `index_src` cho dòng nguồn của số đếm; log đường dẫn neo (`leaders[]`: đầu đường dẫn + điểm 3D) đo bằng `anchor_dev.py`.
- **Sửa theo K/HH:** thẻ ảnh LoC hiện ≈ 3,4 s (≥ 3,0); dòng phương pháp "≈ = interpolated between counts" (HH3); bay WCA ≈ 100 m so mặt đất (≤ 120 m, TL-Q2). Báo cáo: `reports/V5B2A-BAO-CAO.md`.
