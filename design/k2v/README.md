# design/k2v — module hình kênh 2 (Moving Parts)

Bốn module do chủ dự án yêu cầu sau khi xem Steel (12/10/2026): bản đồ thật, ảnh/văn bản thật, số liệu 2.5D/3D, chống lặp cảnh.
Chạy trong Chromium headless + SwiftShader (three.js 0.180 của `design/cong3/shared`), cùng đường ống hậu kỳ với cảnh Steel
(tích luỹ SPP có jitter, ACES, grade, hạt). Chữ trên hình **không** nằm trong 3D: module xuất **điểm neo** (`anchors.json`),
lớp 2D `scripts/k2/lib/k2.js` vẽ chữ ≥ 30 px và đo tương phản như mọi shot kênh 2.

## Dùng trong đặc tả tập (`channel-k2/<tập>/episode.yaml`)
```yaml
heroes:
  m_pair: {hero: map/globe, cam: pair, opt: {from: washington, to: brussels, places: [washington, brussels], arcs: [...], cols: [...]}}
  c_cmp:  {hero: chart3d/stack, cam: crane-up, opt: {groups: [...], scale: 0.01, block: 100, ruler: [0, 500, 1000, 1500]}}
  p_carn: {hero: photo/print, cam: push, opt: {img: /assets/k2/archive/loc-cph-3c01767.jpg, focus: [0.42, 0.24]}}
segments:
  - id: "05"
    shots:
      - {tpl: plate, at: 0, type: map, scene_id: map/globe, camera_id: pair, p: {hero: m_pair, places: [{a: washington, s: "Washington, D.C."}], tags: [...]}}
places: [Washington, D.C., Brussels]          # luật K Q34(a): mỗi địa danh có shot map ±6 s quanh lần nhắc đầu
people: [{name: Andrew Carnegie, photo: LOC-3c01767}]   # Q34(b): rid RIGHTS.md (bảng tư liệu) hoặc clip_id sổ footage, hoặc ly_do ≥ 20 ký tự
anchors: [us1950, us2025, w2025]             # Q34(c): khoá trong numbers; ≥ 60 % hiện bằng chart3d/scene3d, ≤ 40 % chỉ bằng card
```
- `type` (bắt buộc, luật K Q34): `scene3d | map | chart3d | photo | document | footage | card`. `scripts/k2/prep.py` suy khi thiếu
  (map/* → map, chart3d/* → chart3d, photo/print → photo, photo/doc và photo/headline → document, k2g01/* → scene3d, p.card → card) nhưng **đặc tả nên khai rõ**.
- `camera_id`: tên preset trong `scripts/k2/cams.yaml` (`heroes.<k>.cam`). Cùng (scene_id, camera_id) > 2 lần/tập → `prep.py` dừng trước khi thu giọng (Q33 của K đo thêm pHash trên master).
- `document` ≤ 3 s, có `p.paper` + `p.date` (YYYY-MM-DD).
- Mốc thời gian trong `opt` là **giây trong cảnh**; `prep.py` đổi `"@từ"` thành giây như mọi cảnh kênh 2. Trong `p` (lớp 2D), `at`/`out` là giây trong đoạn.

## A. `map/globe` — bản đồ địa lý thật (`map.js`)
| opt | Ý nghĩa |
|---|---|
| `bm` | nền NASA Blue Marble (mặc định `true`, tệp `/cache/bm-global-8192.jpg` từ `scripts/k2/k2v_assets.py bm-global`); `false` = nền vector mực |
| `patches: [{bbox, img}]` | vùng chi tiết khi bay xuống tầm thành phố: `k2v_assets.py bm-crop --bbox lon0,lat0,lon1,lat1 --res 500m` (ô 500 m/px) |
| `hl: [{country, color, at, lift, fill}]` | tô + tường sáng "nhô" theo biên quốc gia (Natural Earth; tên tiếng Anh hoặc mã ISO số) |
| `states: true \| [{state, color}]` | biên giới bang Mỹ (Census 2017) |
| `places: [id \| {id, ll, name, at}]` | ghim địa danh; gazetteer `data/places.json`; neo cùng tên, mặt sau địa cầu → ẩn |
| `arcs: [{from, to, draw:[t0,t1], color, h}]` | cung đại vòng vẽ dần, đầu sáng; neo `arc<i>` |
| `cols: [{id, at, v, grow, color, r}]` | cột số liệu nhô theo pháp tuyến; neo `col:<id>` (đỉnh) |
| `pinMin` | cỡ tối thiểu của ghim (mặc định 0.6); bay xuống tầm thành phố dùng ~0.07 để hai ghim gần nhau không dính (K2C-T1-06 G1b) |
| `cam` / preset | máy quay địa lý `{u\|t, lon, lat, alt (R = 10), tilt°, head°, mm}`; preset: `orbit, flyto, pullback, tilt-low, top, pan, pair` (cần `focus` hoặc `from`/`to`) |
Dữ liệu: Natural Earth 1:50m/1:110m (`data/`, commit), 1:10m (`npm ci`), Census states (`data/`, commit). Ghi công trên hình: "Map: Natural Earth, U.S. Census · Imagery: NASA Earth Observatory".

## B. `chart3d/stack | bars | line` — số liệu 2.5D/3D (`chart3d.js`)
Biểu đồ đứng trong phòng studio thật (sàn bóng, tường cong, đèn chính/viền, phản xạ PMREM) — **nền không mờ**. Tỷ lệ thật (`scale` đơn vị cảnh/1 đơn vị số, không cắt trục), rãnh khối mỗi `block` đơn vị để đếm được.
- `stack`: `groups: [{id, x, segs: [{id, v, color|'steel'}], grow}]` — khối xếp chồng (vd. Mỹ + phần còn lại của thế giới); neo `<g>:top`, `<g>:<seg>`, `<g>:base`, `<g>:baseL/R`.
- `bars`: `bars: [{id, x, v, kind, grow}]` — `kind: projection` = kính hổ phách + viền nét đứt; neo `<id>:top`, `<id>:base`.
- `line`: `pts: [[x, v, kind]], draw` — dải băng dày có chiều sâu + màn dưới đường; phần PROJECTION tách riêng (hổ phách, kính); neo `pt:<i>`, `end`.
- `ruler: [..]` vạch thước ở tường sau, neo `tick:<v>`. Preset máy quay: `front-dolly, crane-up, low-hero, orbit-l, orbit-r, top-down, side-track`.
- Nhãn ACTUAL/PROJECTION, dòng nguồn: lớp 2D (`p.tags[].kind`, `p.src`).

## C. `photo/print | doc | headline` — ảnh thật, văn bản, tiêu đề báo (`photo.js`)
- `print`: `img` (tư liệu đã kiểm quyền từng tệp), `focus: [u, v]` điểm chính, `push`; bản in trên bìa passe-partout, đặt trên bàn lưu trữ dưới đèn bàn; Ken Burns có thị sai (máy quay di chuyển, ảnh không bị biến đổi). Neo `focus`, `print:bl|br|top`. Chú thích tên + năm + nguồn bằng `p.cap`/`p.src`.
- `doc`: `page` = `/cache/<id>-pN.json` (từ `k2v_assets.py doc <id> --page N --find "cụm nguyên văn"`), `hl: [{i, at:[t0,t1]}]` dải bút dạ quang quét theo dòng; neo `hl<i>`.
- `headline`: báo hiện đại = **VÀNG** (QUAN-TRI-RUI-RO §6.7): chỉ tít nguyên văn + tên báo (chữ thường, không logo) + ngày, ≤ 3 s, thân bài là dòng xám làm mờ, không ảnh trong bài.
- Preset: `push, pull, drift-l, drift-r, tilt-low, detail, top`.
- Không tạo/làm động mặt người thật bằng AI; không tô màu ảnh đen trắng.

## D. Chống lặp (`scripts/k2/prep.py`, `scripts/k2/cams.yaml`)
- Thư viện góc máy: ≥ 6 preset dùng được cho mỗi bộ cảnh (module k2v: tính theo nội dung; cảnh Steel k2g01/*: toạ độ, gồm biến thể quay quanh điểm nhìn đã rà tờ khung `channel-k2/k2v-mau/cams/*.jpg`; preset hỏng đánh `loai: true`).
- `prep.py cams <episode.yaml>`: bảng đếm (scene_id, camera_id); `prep.py prep` dừng nếu > 2. Shot thẻ (`p.card`) không tính (bối cảnh `the` của Q26b).
- Kiểm thử: `/opt/cine/bin/python scripts/k2/test_k2v.py`.

## Công cụ
- `scripts/k2/k2v_assets.py` — tải tài sản (SHA ghim `scripts/k2/k2v-assets.sha.json`), Blue Marble toàn cầu/vùng, ảnh tư liệu, trang PDF + khung highlight, bảng giấy phép.
- `scripts/k2/stock.py` — Pexels/Pixabay: tìm (cache 24 giờ), tải qua CDN, SHA, dòng `SOURCES-FOOTAGE.csv`.
- `scripts/k2/vshot.py` — dựng shot mẫu độc lập từ đặc tả dạng episode (1080p, SPP chọn được), xuất `timeline.json` để chạy `checks/ll/q_types.py`, `q_scene.py`, `q_footage.py`.
- `scripts/k2/cams_sheet.py` — tờ khung rà preset góc máy.
- Cài: `(cd design/k2v && npm ci)`; tài sản: `scripts/k2/k2v_assets.py fetch all && … bm-global && … bm-crop …`.
