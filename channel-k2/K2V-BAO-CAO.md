# Kênh 2 — Bộ công cụ hình k2v (phiên V, 12/10/2026)

Nhánh `k2-visual` (từ `origin/k2g-ep01`, đã merge `origin/channel-k2` và `origin/main` @ `2193dbe`, checks 1.10.1). Phạm vi sửa: `scripts/k2/`, `design/k2v/` (mới), `channel-k2/`, kèm `RIGHTS.md`, `checks-appeal.md` và một ảnh tài sản công `assets/k2/archive/`. Không sửa `checks/`, `scripts/ll/`, `design/ll-hero/`. Phiên V chỉ đọc `checks/ll/RULES-LL.md` và chạy công cụ của K, không đọc mã `checks/`.

## 0. Tóm tắt
- **4 module, mỗi module có API đặc tả và 1 shot mẫu 1080p SPP4** (`design/k2v/README.md`):
  - **A** `map/globe`: địa cầu Blue Marble → bay xuống thành phố (ô 500 m/px), biên giới Natural Earth/Census, cung, cột số liệu nhô, nhãn địa danh bám neo.
  - **B** `chart3d/stack|bars|line`: cột đùn khối và khối xếp chồng tỷ lệ thật trong phòng studio không mờ, đường có chiều sâu, ACTUAL/PROJECTION.
  - **C** `photo/print|doc|headline`: ảnh LoC trong khung với Ken Burns có thị sai; trang Federal Register có highlight quét theo dòng; tiêu đề báo hiện đại dựng lại.
  - **D** chống lặp: `prep.py` đếm (scene_id, camera_id), cộng thêm góc gần nhau theo hình học, chặn > 2 trước khi thu giọng; thư viện góc máy có rà tờ khung.
- **Chấm mù** (3 người chấm, `claude-sonnet-5-5`; tay nghề 1–10, 5 = video faceless thường):

  | Cặp | Steel → mới |
  |---|---|
  | Bản đồ | 4,0 → **8,0** |
  | Số liệu | 5,0 → **7,0**; sau một lượt sửa **7,67** |
  | Tư liệu | 4,0 → **7,0** |
  | Cảnh | 3,33 → **7,0** |

  - Người chấm chọn bản mới ở 3/4 cặp ngay vòng 1 (3/3 người). Cặp số liệu sau lượt sửa: 3/3.
  - Chi phí API **$0,90**/trần $15.
- **Luật K 1.10.1 trên shot mẫu:**
  - Q33 ĐẠT 4/4.
  - Q34: ĐẠT B, D. A, C trượt ý (a)/(b) vì shot mẫu không có lời. A trượt thêm ý (c) → đã ghi khiếu nại.
  - Q32: ĐẠT A, B, D. C là 100 % tư liệu (bản chất của shot mẫu).
- **Pexels/Pixabay:** 4 khoá × 1 lượt gọi đều **HTTP 200**. Hàm tìm + tải qua CDN có cache 24 giờ, SHA và sổ CSV.

## 1. SHA commit
- **Commit cuối của mốc:** xem tin trả lời phiên V (commit sau cùng trên `k2-visual`, cùng commit được đẩy lên `claude/happy-knuth-nm4my8`).
- **Lịch sử:**
  - `65031f3` merge `channel-k2`;
  - `c996f14` WIP module;
  - `7864da1` merge `main` (checks 1.10.1);
  - `544cbb2` khớp luật K.
- **Video mẫu** (ngoài git, `/var/tmp/cine-out/k2v-shots/<id>/shot.mp4`; gửi trực tiếp, mỗi tệp < 30 MB):

| Shot | Thời lượng | SHA-256 |
|---|---|---|
| A `map` Washington ↔ Brussels | 12,0 s | `8450eef5aae09fa5f47dbd97ba7becc1c555a29549824668c849762ac7ca996f` |
| B `chart3d` thép 1950 vs 2025 | 10,0 s | `da5ffbe7b1bc3602f4115bcf710ab7055b5e3ebfae0263ffd55afdebd392dbf5` |
| C `photo` Carnegie + `document` Proclamation 11032 | 9,5 s (6,5 + 3,0) | `cf453980ef6b0883511f9fc57bd6632e4feae1d15898743c79cea7f77bbea032` |
| D `scene3d` một bộ cảnh, 3 preset góc máy | 9,5 s | `40a10b21477d6656ca5a5486369e80dec6f6d705f97b30c312abbb1b9fad1e9c` |

- Ảnh tổng: `channel-k2/k2v-mau/tong-4-shot.jpg` (mỗi hàng là một shot, 3 mốc).
- Đặc tả dạng episode: `channel-k2/k2v-mau/{A,B,C,D}-*.yaml`.

## 2. Bốn module
### A. Bản đồ địa lý thật (`design/k2v/map.js`)
- **Dữ liệu:**
  - npm `world-atlas@2.0.2` (Natural Earth 4.1.0) và `us-atlas@3.0.1` (Census 2017);
  - dựng bằng `d3-geo` + `topojson-client` (bản UMD trong trang);
  - 1:50m/1:110m và bang Mỹ commit ở `design/k2v/data/` (968 KB); 1:10m qua `npm ci`.
- **Texture NASA Blue Marble NG, tháng 7/2004:**
  - Ảnh toàn cầu 21600×10800 dùng cho nền 8192×4096.
  - Ô 500 m/px B1/C1 dùng cho vùng bay xuống (`k2v_assets.py bm-crop --res 500m`).
  - Đổi từ bản 12/2004 sau tờ khung nháp: Canada phủ tuyết, khó nhận ra.
- **Nhận diện ngay:**
  - Đường bờ thật, ranh giới quốc gia và bang.
  - Vịnh Chesapeake, Ngũ Đại Hồ, Tây Âu, dãy Alps hiện rõ ở tầm thành phố.
  - Tường sáng "nhô" theo biên quốc gia được tô.
- **Nhãn địa danh:** lớp 2D vẽ tại điểm neo, ≥ 30 px. Neo nằm sau địa cầu thì tự ẩn.
- **Shot mẫu:**
  - Toàn cầu → Washington (cột 50 %, Proclamation 10947) → cung qua Đại Tây Dương → Brussels (cột 50 %, Reg. (EU) 2026/1384).
  - Hai số đều có trong claims Steel (C74, C41).
  - Câu chú thích lấy từ lời Steel: "from Washington to Brussels".
### B. Số liệu 2.5D/3D (`design/k2v/chart3d.js`)
- **Hình khối:**
  - Thân cột là khối đùn bo góc, vật liệu PBR (cam clearcoat; thép kim loại).
  - Phản xạ từ một phòng hộp đèn PMREM tự dựng, không cần addon.
  - Rãnh khối mỗi 100 Mt để đếm được; bóng tiếp xúc dưới chân cột.
- **Tỷ lệ thật:** 1 đơn vị cảnh = 100 Mt, không cắt trục.
- **Shot mẫu:**
  - 1950: Mỹ 87,8 + phần còn lại 101,2 = 189 Mt.
  - 2025: Mỹ 81,9 + phần còn lại 1 767 = 1 849 Mt.
  - Máy quay bắt đầu thấp sát cột 1950, sau đó cẩu lên theo cột 2025.
- **Chữ và nhãn:**
  - Nhãn ACTUAL đặt cạnh số; dòng nguồn ghi rõ hai chuỗi khác nhau (USGS raw / worldsteel crude).
  - Thước 500/1 000/1 500 Mt ở tường sau.
- **Nền:** phòng studio thật, không làm mờ.
### C. Ảnh thật, văn bản, tiêu đề báo (`design/k2v/photo.js`)
- **`print`:**
  - Bản in đặt trên bìa passe-partout, trên bàn lưu trữ dưới đèn bàn.
  - Ken Burns có thị sai: máy quay di chuyển, ảnh giữ nguyên, giữ màu gốc.
  - Chú thích gồm tên, năm và nguồn.
- **`doc`:**
  - Dựng trang PDF gốc (`pdftoppm`).
  - Khung highlight lấy từ `pdftotext -bbox-layout` theo cụm nguyên văn; xử lý được từ ngắt gạch nối cuối dòng ("Alu-/minum").
- **`headline`:**
  - Chỉ gồm tít nguyên văn, tên báo bằng chữ thường (không măng-sét) và ngày; ≤ 3 s.
  - Thân bài là dòng xám làm mờ, không có chữ thật; không lấy ảnh trong bài.
  - Mẫu này chưa dùng trong shot chấm. Đã thử khung với tít AP 22/09/2025.
- **Shot mẫu C:** chân dung Andrew Carnegie (Marceau 1913, LoC cph.3c01767) → trang 1 Proclamation 11032 (FR 4/6/2026) highlight số và tên văn bản.
  - Đoạn `document` = 3,0 s, có `p.paper` + `p.date` theo luật K.
### D. Chống lặp (`scripts/k2/prep.py`, `scripts/k2/cams.yaml`)
- **Khai báo:** `heroes.<k>.cam: <preset>` → `camera_id`. Shot khai thêm `type/scene_id/camera_id`; `prep.py` tự suy nếu thiếu và ghi vào `timeline.json` cùng `shots-meta.json`.
- **Chặn lặp:** cùng góc > 2 lần → dừng trước khi gọi ElevenLabs.
  - Shot liền nhau cùng góc tính là một lần, như Q33.
  - **Cộng thêm góc khai khác nhưng gần nhau** (phương vị < 25°, độ cao < 10°, khoảng cách < 1,4×, tiêu cự < 1,3×). Hiệu chuẩn bằng chính pHash Q33 của K trên shot D.
- **Áp thử lên Steel** (`prep.py cams`): 6 góc bị chặn (port 5; chain c_draw/c_own 5 và 4; trade 3; ingots 3).
  - Cùng hướng với Q33 hồi tố của K (p_eu 5, c_own 4, c_draw 3, t_both 3). Phần ingots chặt hơn K.
- **Thư viện:** `cams.yaml` và tờ khung rà ở `channel-k2/k2v-mau/cams/*.jpg`. Preset hỏng đánh `loai: true` kèm lý do.

| Bộ cảnh | Preset dùng được | Họ góc khác nhau thật* |
|---|---|---|
| map/globe, chart3d/* | 7 | 7 (rà tờ khung) |
| photo/print, photo/doc | 7 | **4–5** (drift-l/drift-r/top gần giống nhau về hình, chỉ khác chuyển động) |
| k2g01 valley / ingots / furnace / trade / port / mill / north | 9 / 14 / 12 / 14 / 13 / 11 / 13 | 9 / 11 / 7 / 12 / 12 / 10 / 9 |
| **k2g01/chain** (sa bàn bản đồ) | 7 | **4 (< 6)** — mọi góc xoay > 60° làm mất nhận diện bản đồ; đề xuất dùng `map/globe` thay cảnh này |

\* "Họ góc" gộp các preset gần nhau theo luật hình học ở trên.

- **Shot mẫu D, vòng đầu:** dùng `mid-push` / `orbit-l45` / `orbit-r12-low`. Q33 pHash của K gộp `mid-push` ↔ `orbit-r12-low` (lệch 21°), và lần thử tiếp `orbit-l45` ↔ `orbit-r60` (15°).
- **Shot mẫu D, bản cuối:** `mid-push` / `orbit-l45` / `orbit-r25` (lệch 33–70°). Q33: 3 góc, **0 lần lặp không khai**.

## 3. Bảng giấy phép (chi tiết: `RIGHTS.md` mục "Kênh 2 — module hình k2v")

| Mã | Tài sản | Giấy phép | Commit | SHA-256 |
|---|---|---|---|---|
| K2V-MAP-1 | Natural Earth 1:50m/1:110m (world-atlas) | Tài sản công ("No permission is needed") | có | `04342cdc…` / `2516c915…` |
| K2V-MAP-2 | Census states 2017 (us-atlas) | Tác phẩm chính phủ Mỹ | có | `d76b391c…` |
| K2V-LIB-1 | d3-geo, d3-array, topojson-client | ISC | qua `npm ci` | `23e574f1…` … |
| K2V-IMG-1 | NASA Blue Marble NG 7/2004 (toàn cầu + ô B1, C1) | NASA: không có bản quyền ở Mỹ; ghi "NASA Earth Observatory"; không logo, không hàm ý bảo trợ | **không** (27–88 MB) | `d225f1f3…`, `15d8ceb5…`, `ee8490ab…` |
| K2V-IMG-2 / LOC-3c01767 | Andrew Carnegie, T. C. Marceau 1913, LoC cph.3c01767 | Tài sản công (xuất bản 1913) | TIFF gốc không; bản 1281×1600 **có** (324 KB, `assets/k2/archive/`) | TIFF `f1fc56a6…` |
| K2V-DOC-1 | Federal Register 2026-11314 (Proclamation 11032) | Tác phẩm chính phủ Mỹ (17 U.S.C. §105) | không | `382464d1…` |
| K2V-F2 | DejaVu Serif Bold (tít báo) | Bitstream Vera License | hệ thống | `847b33e1…` |

- SHA ghim ở `scripts/k2/k2v-assets.sha.json`; `k2v_assets.py fetch` dừng nếu nguồn đổi.
- **Pexels/Pixabay** (`scripts/k2/stock.py`):
  - Điều khoản API đọc 12/10:
    - Pexels: 200 yêu cầu/giờ, liên kết Pexels.
    - Pixabay: 100/60 s, cache 24 giờ, không hotlink.
  - Thử tải 4 tệp (2 video, 2 ảnh) qua CDN, có SHA, rồi **xoá**: không dùng trong shot mẫu, không commit.

## 4. Số đo render (1080p, 24 khung mẫu/cảnh, máy 4 vCPU rảnh, SwiftShader)

| Module (cảnh) | SPP1 s/khung | SPP4 s/khung | Ghi chú |
|---|---|---|---|
| A `map/globe` | 2,09 | 2,50 | + ~25–30 s dựng texture 8192² và 2 vùng 6144 px mỗi lần mở cảnh |
| B `chart3d/stack` | 2,55 | 3,60 | bóng PCF 2048 + vật liệu physical |
| C `photo/print` | 1,50 | 2,04 | |
| C `photo/doc` | 1,04 | 2,11 | |
| D `k2g01/furnace` (3 preset) | 1,10–1,25 | 2,68–2,97 | Steel G2 đo 4,2 s/khung SPP4 khi 3 tiến trình chạy song song |
| Lớp chữ 2D (`render.js`) | — | 0,15–0,38 | |

- **SPP1 không nhanh gấp 4 SPP4:** mỗi khung tốn khoảng 1 s cố định để đọc điểm ảnh, base64, mã JPEG và gọi trang.
- **Bản cuối chạy song song 2–3 tiến trình nên chậm hơn:** A 2,9; B 6,0 s/khung.
- **Ước tính cho tập 15 phút** (≈ 21 600 khung, nếu 50 % thời lượng là module k2v SPP4): ≈ 8–10 giờ máy nếu chạy tuần tự. Mức này tương đương Steel (11,6 giờ cảnh 1080p).

## 5. Chấm mù trước/sau (`channel-k2/k2v-mau/blind_v.py`, `kiem-mu/blind-score.json`)
- **Cách chấm:**
  - Mỗi cặp gồm 1 khung Steel 1080p (bộ Q27 G2: F02, F04, F09, F12) và 1 khung shot mẫu ở mốc khai trước (A 11,2 s; B 8,6 s; C 3,6 s; D 4,6 s).
  - Tên X/Y trộn bằng hạt giống cố định.
  - 3 vai chấm (người xem; đạo diễn motion/3D; biên tập tài liệu), thư mục tạm trống, chỉ được dùng công cụ Read.
  - Mô hình thực chạy: `claude-sonnet-5-5` (15/15 lượt).

| Cặp | Tay nghề Steel → mới | Đọc chữ | Rõ ý | Người chấm chọn | Cờ mới |
|---|---|---|---|---|---|
| P1 bản đồ (F02 sa bàn Ngũ Đại Hồ ↔ A) | 4,0 → **8,0** | 0 → 8,0 | 2,67 → **8,0** | mới 3/3 | — |
| P2 số liệu (F04 thẻ cột ↔ B) vòng 1 | 5,0 → **7,0** | 8,33 → 6,0 | 8,0 → 6,33 | **Steel 2/3** | cluttered, text_cut_off |
| P2 vòng 2 (sau một lượt sửa) | 4,67 → **7,67** | 7,67 → 7,0 | 7,33 → **7,67** | **mới 3/3** | cluttered (1 người) |
| P3 tư liệu (F09 thẻ mốc thời gian ↔ C chân dung) | 4,0 → **7,0** | 6,67 → 6,0 | 5,0 → **8,67** | mới 3/3 | — |
| P4 cảnh (F12 port ↔ D furnace) | 3,33 → **7,0** | 5,33 → 0 (khung không chữ) | 3,0 → **7,0** | mới 3/3 | — |

- **Lượt sửa P2 (một lượt), nguyên nhân đo được:**
  - Dải tối của dòng nguồn (`caps`) vẽ **sau** nhãn nên phủ mờ mọi nhãn ở 1/3 dưới khung. Tương phản đo được 2,8–3,9; người chấm ghi "faint US callout".
  - Sửa: nhãn k2v vẽ sau dải nguồn, nền nhãn đặc hơn, chữ phụ sáng hơn và 32 px.
  - Máy quay lùi để không cắt đỉnh cột.
  - Nhãn "World 189 Mt · 1950" hiện lại ở cuối, sau khi tắt nhãn năm để không chồng chữ.
  - Sau sửa: **0 mẫu chữ tương phản < 4,5** (trước sửa 17).
- **Thứ tự chấm:** P1 chấm trên A trước lượt sửa thứ tự vẽ. Khung chấm của P1 có nhãn ở nửa trên, không bị dải nguồn phủ. Bản A cuối đã dựng lại với thứ tự vẽ mới.
- **Giới hạn của phép so:** 1 khung/cặp. Khung Steel lấy ngẫu nhiên từ Q27, khung mẫu là shot đã thiết kế cho nội dung đó. Đây là so sánh **loại hình** (thẻ phẳng ↔ module mới), chưa phải Q27 của một tập. Tiêu chí tiến bộ ở BAI-HOC-K2 K7 (≥ 7/10, "above") phải đo lại bằng Q27 chính thức trên K2 tập 2.

## 6. Luật K 1.10.1 trên 4 shot mẫu (`checks/ll/q_types.py`, `q_scene.py`, `q_footage.py`)

| Shot | Q33 | Q34 | Q32 |
|---|---|---|---|
| A | ĐẠT (1 góc) | TRƯỢT (a) ×2: không có lời; **(c) 0/2 số bằng chart3d/scene3d** | ĐẠT |
| B | ĐẠT | **ĐẠT** (3 số neo, 100 % 3D) | ĐẠT |
| C | ĐẠT (2 góc) | TRƯỢT (b): không có lời (ảnh LOC-3c01767 hợp lệ) | TRƯỢT (b): 100 % tư liệu (shot mẫu 9,5 s) |
| D | ĐẠT (3 góc, 0 lặp không khai) | **ĐẠT** | ĐẠT |

- **Q34(c) ở A:** số đặt trên **cột 3D của bản đồ** không được tính là 3D. Đã ghi khiếu nại ở `checks-appeal.md` (đề nghị tính `map` có neo `col:*`). Phiên V không thêm phần tử chart3d chỉ để qua thước.
- **Định dạng khai báo đọc được nhờ chạy thử:**
  - `people: [{name, photo: <rid bảng tư liệu RIGHTS>}]` và shot photo có `p.photo` = rid. Dòng RIGHTS dạng 10 cột không được nhận, nên đã thêm dòng `LOC-3c01767` theo bảng tư liệu kiểu LL.
  - `p.date` theo dạng YYYY-MM-DD.
  - `anchors` là danh sách khoá `numbers`; nhãn số khai `num`.

## 7. Thay đổi khác
- **`QUAN-TRI-RUI-RO.md` §6.7 (mới):**
  - Bảng nguồn bản đồ, ảnh, văn bản, tiêu đề báo kèm mức (báo hiện đại = **VÀNG**: tít + tên báo + ngày, ≤ 3 s, làm mờ thân bài, không ảnh trong bài).
  - 6 quy tắc ảnh người thật: đúng ngữ cảnh; không đặt vào thế xấu; chú thích tên + năm + nguồn; không tạo hay làm động mặt bằng AI; người còn sống; người không phải nhân vật công chúng.
  - Cập nhật hiện trạng khoá Pexels/Pixabay và LoC 403.
- **`BAI-HOC-K2.md` K10 (đổi số từ K8 khi squash vào k2c-t1-06):**
  - `ctx.filter` trên canvas lớn trả rỗng.
  - Tiến trình dựng chết khi tiến trình cha bị dừng.
  - Biến thể rẻ phải khác góc thật.
  - Bản đồ giữ hướng Bắc.
  - Bài học chữ P2.
- **`scripts/k2/hero.js`:** tự chọn trang `design/k2v/page.js`; thêm đường `/cache/` (tài sản ngoài git) và `/assets/`; meta ghi SPP.
- **`scripts/k2/lib/k2.js`:** thêm lớp nhãn `p.places` / `p.tags` (≥ 30 px, nền đặc, vẽ sau dải nguồn). Không đổi `labels`, `caps`, `card` của Steel.
- **`scripts/k2/test_k2v.py`:** 9/9 ĐẠT.

## 8. Sai lệch, hạn chế, rủi ro
- **Trang LoC item bị 403/Cloudflare với máy.** "Rights Advisory" của cph.3c01767 mới đối chiếu qua Commons; tệp tải thẳng từ `tile.loc.gov`.
- **Tít báo:** module có, đã thử khung, nhưng không nằm trong 4 shot chấm (lệnh chỉ định Carnegie + Federal Register).
- **Đo SPP1** chạy trùng một lần dựng lớp chữ D (vài phút). Sai số nhỏ, số SPP4 không bị ảnh hưởng.
- **Rủi ro:**
  - Mỗi lần mở cảnh map tốn ~25–30 s dựng texture.
  - Ô 500 m chỉ ghim B1, C1. Vùng khác cần thêm ô (A1, D1, A2–D2: 50–90 MB mỗi ô).
  - Chain chỉ có 4 họ góc khác nhau.

## 9. Việc đang chờ chủ dự án
1. **Duyệt mốc** (4 module, 4 shot mẫu, luật chống lặp, §6.7 QUAN-TRI-RUI-RO). Sau khi duyệt, P ghi `AUTHORSHIP.md`.
2. **Mở trang LoC** https://www.loc.gov/pictures/item/2002712252/, đối chiếu "Rights Advisory" của ảnh Carnegie (máy bị chặn).
3. **Khiếu nại Q34(c)** (số trên cột bản đồ) — chuyển phiên K.
4. **Cảnh `k2g01/chain`** chỉ có 4 họ góc: chấp nhận, hoặc thay bằng `map/globe` cho mọi bản đồ tuyến (đề xuất).
5. **Merge:** nhánh `k2-visual` chờ phiên P merge (phiên V không merge `main`).
