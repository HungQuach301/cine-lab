# design/k2v/tl — XƯƠNG SỐNG THỜI GIAN (Moving Parts = NƠI CHỐN + CƠ CHẾ + THỜI GIAN)

Phiên V5b-1 (16/10/2026), chủ dự án duyệt Y1–Y7, Z1–Z2. Port từ `lab/timelapse/` (nhánh `timelapse-rd`) thành mô-đun dùng lại được.
**Chỉ CPU** (Chromium headless + SwiftShader). Mô-đun MỚI, độc lập: chỉ *import* `design/cong3/shared/post.js` và three.js 0.180 của `design/cong3/shared`;
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
| `terrain.js` | lớp 3: DTM (20 m gần / 60 m xa, **LOD theo ô 1 km**), vòng chân trời 150 m, phủ Sentinel-2 tự nhiên ↔ đô thị theo năm, đá vôi vách dốc, **AO nướng sẵn theo năm**, đất khai hoang nổi theo năm |
| `water.js` | biển (sóng thủ tục, Fresnel, lấp lánh) + vòm trời; vẽ sau địa hình |
| `city.js` | lớp 2: toà thủ tục gộp theo ô 500 m, **LOD** (gần mái dốc + cửa sổ shader / xa khối / rất xa impostor = nền vệ tinh), mọc theo năm, ghost |
| `geom.js` | hình học thuần (test Node: hướng mặt bằng tích có hướng) |
| `nature.js` | cây instanced (NDVI + OSM, LOD 2 km, bóng theo năm) + đường OSM theo năm từng đỉnh |
| `heroes.js` + `heroes/*.json` | lớp 1: Tower of Homage (tapia, răng cưa, khe bắn), tường lâu đài/thành, đường băng 09/27 (vạch ICAO, chắn đường ngang) — tệp nguồn kích thước ở `heroes/` |
| `campath.js` | ngữ pháp máy quay: Hermite theo thời gian, **bay dọc tuyến thật** (mốc dày trên hình học), nhật ký lệch tuyến/khoảng cách/tốc độ/đứng yên |
| `text.js` | **ngân sách chữ**: năm + chỉ số (2 lớp thường trực), nhãn phương pháp đầu/cuối, ≤ 1 thẻ, thẻ neo, ảnh chú thích neo điểm 3D, nhãn ghost; đo % diện tích, vùng giữa, tương phản WCAG trên điểm ảnh thật |
| `lut.js` | LUT .cube → Data3DTexture, áp trong grade (chỉ cảnh 3D; ảnh sepia/chữ vẽ sau) |
| `scenes/gib20.js` | đoạn thử Gibraltar 20 s |

## Chạy (công cụ ở `scripts/k2tl/`)
```bash
export K2TL_CACHE=/var/tmp/cine-out/k2tl-cache            # dữ liệu thô + gói cảnh, NGOÀI git
python scripts/k2tl/fetch_osm.py --name gib --bbox=-5.385,36.105,-5.320,36.185
# tải tay (lệnh trong reports/V5B1-BAO-CAO.md §7): Copernicus GLO-30, Sentinel-2 S2C_30STF_20260415_0 (TCI+B08), Landsat 5 1987 (Planetary Computer), Catastro BU 11022, ảnh LoC, LUT A (git show origin/v5a)
python scripts/k2tl/build_rasters.py --name gib && python scripts/k2tl/build_vectors.py --name gib && python scripts/k2tl/build_scene.py --name gib --ao --far
node scripts/k2tl/render.js --scene gib20 --pack gib --w 1920 --h 1080 --out <thư mục>      # khung JPG + log.json (s/khung, spp, LOD, chữ, tương phản)
node scripts/k2tl/render.js --campath <tệp>   |   --budget <tệp>                            # nhật ký máy quay / ngân sách chữ cả đoạn (không dựng hình)
bash scripts/k2tl/bench.sh <ra.jsonl> "470,175,300,470,175,300" '{"spp":2,"lod":false}' nhãn   # đo kỹ thuật → s/khung
python scripts/k2tl/mix.py --cues channel-k2/k2c-t3-01/v5b1-thu/cues.json --dur 20 --out mix.wav   # −14 LUFS
python scripts/k2tl/calib.py <điểm-khống-chế.json>                                           # then/now ≥ 6 điểm
bash scripts/k2tl/tests/run.sh                                                               # test
```
Python: `/opt/cine/bin/python` (+ `imagecodecs` cho GeoTIFF nén dự đoán — thêm trong phiên, đề xuất đưa vào `scripts/env/setup.sh`).

## Kỹ thuật CPU (đo trong `reports/V5B1-BAO-CAO.md` §5)
`tech`: `lod` (toà/cây theo khoảng cách), `terrainLod`, `ao` (AO nướng theo năm), `shadowCache` (bóng 1 lần/khung, giữ khi khoá cảnh không đổi), `shadows`,
`spp` (`'adaptive'` theo cảnh: 4 cận hero/mốc đinh, 2 thường, 1 + lọc cạnh khi bay nhanh), `baked` (nhiễu nướng sẵn), `lambert`, `treeDetail`, `city`, `trees`, `shadowRes`.
