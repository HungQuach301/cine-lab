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

## E. `relief/map` — bản đồ địa hình nổi + sticker (phiên V2, `relief.js`, 14/10/2026)
Công thức "bản đồ nổi + sticker" học từ thể loại (không dùng hình, thumbnail, câu chữ của kênh nào). Mọi tài sản tự dựng hoặc tài sản công (RIGHTS.md K2V2-*).
- **Nền:** `scripts/k2/relief_build.py build --name <tên> --bbox lon0,lat0,lon1,lat1 [--ppd 600] [--mesh 8] [--routes 'id=Tên NE|Tên NE;…']`
  - DEM USGS 3DEP 1″ (tài sản công) ghép ở 6″ (~140–185 m/px): sắc nét ở tầm vùng 300–500 km.
  - Tô bóng nhiều hướng (315/270/360/225°); mặt nạ nước + sông + ranh bang/tỉnh từ Natural Earth 10m.
  - Ra `$K2V_CACHE/relief/<tên>/{natural.jpg, sepia.jpg, height.f32, routes.json, meta.json}`.
  - Bản `erie`: 82°W–71°W × 39°N–46°N, 6600×4200, lưới 825×525, ≈ 2,5 phút dựng.
- **Hai bảng màu:**
  - TỰ NHIÊN (hiện tại): màu độ cao × bóng, nước có dải nông.
  - SEPIA (quá khứ): giấy, mực nâu, bờ nước kẻ nét.
  - Chuyển dần trong shot: `sepia: [t0, t1]` hoặc `natural: [t0, t1]`; cố định: `palette`.
- **Vùng nổi theo phía** `regions` (≤ 3): khối nhô `lift` km, tô theo phương pháp nhân (giữ vân địa hình), tường tối, viền sáng kiểu sticker, bóng đổ Đông Nam; nổi lên theo `at: [t0, t1]`.
- **Tuyến** `routes`:
  - `style: solid|dashed`; nét đứt "chảy" theo `flow` km/s; vẽ dần theo `draw`; đầu sáng.
  - Độ dày `w` tính theo px khung 1080p, giữ nguyên khi máy zoom.
  - `pts` trộn địa danh, `[lon, lat]` và đoạn của đường Natural Earth `{src, from, to}`.
- **Vòng sáng** `rings` (3 vòng lan, cỡ theo px). **Neo:** địa danh, `st:<id>` (`pins`, `walkers` chạy theo tuyến), `col:<id>` (đỉnh chồng xu/cột), `rt:<id>` (đầu tuyến).
- **Số liệu trên bản đồ** `cols: [{id, at, kind: coins|bar, n|v, unit, t: [t0, t1], r}]`:
  - Mỗi đồng xu là một đơn vị khai rõ, nên chiều cao chồng đúng tỷ lệ thật; xu rơi lần lượt.
  - Nhãn số bám `col:<id>` (`p.tags[].a`) và khai `num`. Như vậy Q34(c) 1.10.2 tính số là hiện bằng 3D.
- **Máy quay** `cam: [{t|u, lon, lat, dist km, tilt°, head°, mm}]`: spline Hermite qua các mốc. Máy không dừng ở mốc giữa và giữ vận tốc ở hai đầu, nên **trượt liên tục**.
- **Tone map riêng** (`export const TONE`): giữ bảng màu bản đồ, vai mềm trên 0,82. ACES vẫn là mặc định cho các module khác (`page.js`).

### Sticker (`scripts/k2/lib/sticker.js`, thư viện `design/k2v/stickers/`, tờ rà `channel-k2/k2v2-mau/stickers-sheet.jpg`)
- **Một phong cách** cho mọi sticker: viền trắng dày ≈ 6 % cạnh, bóng đổ mềm lệch xuống phải (`STK.style`).
  - **Vật 3D:** vật liệu toon 3 nấc, góc 3/4 cố định (`design/k2v/sticker-lab.js`).
  - Tái dùng mô hình của kênh: lò cao và xưởng (K2G-01), nhà (K2C-T1-06). Mô hình nạp qua `?rx=` nên không sửa tệp tập.
  - **Vật mới:** mỏ, tàu buồm, thuyền kênh, xu, chồng xu, văn bản, ngân hàng, cờ trung tính, xe hàng, bao, thùng, núi.
  - Dựng lại: `node scripts/k2/stickers_build.js [tên…]`; SHA trong `stickers.json`.
- **Lớp 2D** `p.stickers: [{a: 'st:<id>'|địa danh|'col:<id>', img: 'stk:<tên>' | {role, hat, hand} | 'role:<vai>', at, out, px, walk, hz, bob, flip|face, dx, dy}]`:
  - Bật nảy khi vào (back-out 0,42 s) và co lại khi ra.
  - `walk`: nhún theo nhịp, tự lật theo hướng đi.
  - Vẽ dưới dải chú thích; hộp sticker ghi vào `LL.occ` để nhãn né.
- **Nhân vật A-lite** (8 vai: worker, merchant, banker, soldier, official, engineer, farmer, sailor):
  - Vẽ vector phẳng. Không mặt chi tiết, không diễn xuất, không khớp miệng.
  - Nhận ra bằng mũ + vật cầm tay, có thể thay: `STK.HATS`, `STK.HANDS`, vd. `{role: farmer, hand: wheat}`.
  - Hoạt ảnh tối thiểu: đi theo tuyến (`walkers` + `walk: true`), nảy nhẹ, xuất hiện/biến mất.
- **Chân dung tài sản công:** dùng lại `photo/print` (Ken Burns có thị sai, chú thích tên · năm · nguồn qua `p.cap`/`p.src`, `p.photo` = rid RIGHTS).
### Nhãn né vật (BAI-HOC-K2 K11)
- `p.tags[].side: 'auto'`: chọn hướng đầu tiên trong `prefer` (mặc định up/right/left/down) không chạm hộp sticker/nhãn đã vẽ ở khung.
- Hướng đã chọn được giữ cho tới khi bị chạm, nên nhãn không nhảy qua lại.
### Bảng điểm (`p.score`, component dùng lại ở `scripts/k2/lib/k2.js`)
- `corner: {at, out, sides: [{s, c, icon, n | [{t, v}]}]}`: huy hiệu góc (biểu tượng + tên + điểm tăng theo mốc).
- `board: {at, out, title, sides: [{s, c, icon}], rows: [{k, icon, v: [trái, phải], win, at, sub}], foot}`: bảng tổng kết hai phía.
  - Mỗi hàng có biểu tượng sticker; ô thắng được khoanh viền màu phía thắng.
  - Các hàng hiện lần lượt.
  - Nền là bản đồ thật làm tối (`p.dim`), không làm mờ (K11: thẻ tóm tắt có biểu tượng cho từng mục).

## Công cụ
- `scripts/k2/k2v_assets.py` — tải tài sản (SHA ghim `scripts/k2/k2v-assets.sha.json`), Blue Marble toàn cầu/vùng, ảnh tư liệu, trang PDF + khung highlight, bảng giấy phép.
- `scripts/k2/stock.py` — Pexels/Pixabay: tìm (cache 24 giờ), tải qua CDN, SHA, dòng `SOURCES-FOOTAGE.csv`.
- `scripts/k2/vshot.py` — dựng shot mẫu độc lập từ đặc tả dạng episode (1080p, SPP chọn được), xuất `timeline.json` để chạy `checks/ll/q_types.py`, `q_scene.py`, `q_footage.py`.
- `scripts/k2/cams_sheet.py` — tờ khung rà preset góc máy.
- Cài: `(cd design/k2v && npm ci)`; tài sản: `scripts/k2/k2v_assets.py fetch all && … bm-global && … bm-crop …`.
