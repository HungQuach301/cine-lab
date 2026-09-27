# CHẠY LUẬT KIỂM L1 (v1.4) — hướng dẫn cho phiên xưởng

**Điểm mới v1.4** (3 khiếu nại Cổng 3 được chủ dự án chấp nhận):
1. **File không có luồng âm** (khung phong cách, chưa làm âm): J1 và J1b quyết theo `X.script.txt`.
   - Kịch bản rỗng → "—" (không áp dụng), như M3. Không cần thư mục stem.
   - Kịch bản có lời → THIẾU. Không chèn luồng âm im lặng để lách: khi đó J1 TRƯỢT vì thiếu từ.
2. **Lược đồ model sheet** được ghi ở mục 3.6. Sheet sai định dạng thì C3 báo THIẾU kèm thông báo rõ (không còn "LỖI ĐO KeyError").
3. **C3 theo góc nhìn và tư thế** (mục 3.6):
   - Máy chỉ so tỷ lệ ở mẫu **đo được**: góc nhìn cách một góc trong `c3_views` ≤ 30°, bộ phận không gập, không bị che, không lệch phối cảnh, không bị cắt ở mép khung. So với số của góc gần nhất.
   - Để máy biết góc nhìn và tư thế, xuất thêm **`views`** vào `parts.json` từ chính lần render mặt nạ. Không có `views` thì mọi mẫu được so với góc 0° như v1.3 (chặt nhất).
   - Mẫu không đo được được đếm và liệt kê. Báo cáo nêu tỷ lệ mẫu đo được **theo từng shot**.
   - Shot có nhân vật mà **không mẫu nào đo được** thì C3 = **CẦN NGƯỜI XEM** (mã thoát 5), không bao giờ ĐẠT.
   - Kiểm toán ngẫu nhiên (mục 3.7): render lại phải xuất lại cả `views.json` của khung được chọn.

**Điểm mới v1.3:**
1. **Kiểm toán ngẫu nhiên mặt nạ C3** (mục 3.7):
   - Sau khi nộp, phiên P chọn ngẫu nhiên 1–2 khung.
   - Phiên xưởng render lại mặt nạ đúng các khung đó từ file cảnh đã khoá và nộp kèm log lệnh render.
   - Chưa kiểm toán thì C3 báo THIẾU và shot không thể ĐẠT.
2. **Đầu nhân vật cao dưới 100 px** trong khung ở bất kỳ khung mẫu nào thì mặt nạ **bắt buộc 4×**.
3. **J1 dùng stem thoại** (bắt buộc theo J1b) để quyết chữ nào là chèn:
   - Chữ ASR rơi vào lúc stem thoại im thì bị bỏ và được liệt kê trong báo cáo.
   - Chữ ASR rơi vào lúc stem thoại có lời mà không có trong kịch bản thì tính là chèn.
   - Vì vậy stem thoại phải chứa **mọi** lời thoại, và chỉ lời thoại.

**Điểm mới v1.2:**
1. J1 kiểm theo từng câu thoại (mỗi dòng `X.script.txt` là một câu). Nên giữ mỗi lời thoại một dòng.
2. J1 coi từ ghép và từ tách là một (goodnight = good night…), theo bảng trong RULES.md.
3. J1 bỏ chữ ASR bịa trong đoạn im lặng số tuyệt đối. Báo cáo liệt kê những chữ bị bỏ.
4. Mặt nạ C3 phải render thật ở 2–4×, nhị phân hoặc khử răng cưa **ở chính độ phân giải đó**. Mặt nạ phóng to còn biên xám mờ hoặc biên bậc thang thì TRƯỢT. Dải bảo vệ nhiễu đo rộng gấp đôi v1.1: shot đầu nhỏ cần mặt nạ 4× để chứng minh.

**Điểm mới v1.1** (chi tiết ở mục 3.1, 3.6 và bảng mục 4):
1. Mặt nạ C3 **bắt buộc** ở độ phân giải gấp 2–4 lần khung. Máy đo hệ số từ kích thước PNG.
2. Chữ trong thế giới phim được gắn `"diegetic": true`: miễn G4, vẫn cần matte và vẫn qua P1.
3. Master YouTube có grain phải có bitrate hình ≥ 30 Mbps.
4. Ngưỡng J1b là ngưỡng nội bộ, chưa hiệu chuẩn.

Phiên xưởng **chỉ đọc file này**. Không đọc, không sửa mã trong `checks/`. Khiếu nại về luật ghi vào `checks-appeal.md` ở gốc repo.

## 1. Lệnh duy nhất

```bash
/opt/cine/bin/python checks/run.py <file-video> [--profile shot|youtube|archive]
```

- `shot` (mặc định): bản render một shot hoặc sequence.
- `youtube`: master YouTube (thêm N3 codec/bitrate và M1 loudness).
- `archive`: master lưu trữ chất lượng cao (thêm N3 bản intermediate).

Ví dụ: `/opt/cine/bin/python checks/run.py shots/sq01_sh010/render/sq01_sh010.mp4`

Lệnh chạy toàn bộ luật áp cho profile, rồi ghi:
- `reports/checks/<tên file>/<tên file>.checks.json` — báo cáo máy đọc;
- `reports/checks/<tên file>/<tên file>.checks.md` — báo cáo người đọc.

Đổi thư mục báo cáo bằng `--out <thư mục>`.

## 2. Kết luận và mã thoát

| Kết luận | Mã thoát | Nghĩa |
|---|---|---|
| ĐẠT | 0 | Mọi luật Chặn áp dụng đều đạt |
| TRƯỢT | 1 | Có luật Chặn trượt, hoặc lỗi khi đo (lỗi đo không được coi là sạch) |
| THIẾU DỮ LIỆU | 2 | Có luật Chặn thiếu file đi kèm (mục 3) nên không đo được |
| LUẬT KHÔNG KHỚP LOCK | 3 | Mã trong `checks/` khác SHA trong `checks/LOCK`: kết quả vô hiệu, báo phiên P |
| CẦN NGƯỜI XEM | 5 | (v1.4) Không luật nào trượt hay thiếu, nhưng C3 có shot có nhân vật mà máy không đo được mẫu nào. Người duyệt so nhân vật với model sheet bằng mắt. Không phải ĐẠT |
| (lỗi dòng lệnh) | 4 | Không thấy file video |

Báo cáo liệt kê mọi chỉ số nằm trong ±5% quanh ngưỡng. **Phải chép danh sách này vào báo cáo gói việc** (luật cứng CLAUDE.md).

## 3. File đi kèm (đặt cạnh file video, cùng tên gốc)

Máy đo từ file đã render. Các file đi kèm dưới đây là **dữ liệu xuất ra từ phần mềm dựng/render**, không phải bản khai tay. Thiếu file thì luật tương ứng báo THIẾU và kết luận không thể là ĐẠT.

Với video `X.mp4`:

| File | Dùng cho | Nội dung |
|---|---|---|
| `X.script.txt` | J1 (và J1b khi không có luồng âm) | Lời thoại tiếng Anh đúng như kịch bản cho đoạn phim này. Mỗi câu một dòng; cho phép nhãn người nói `NAME:` đầu dòng; chỉ dẫn diễn xuất trong `[...]` hoặc `(...)` và dòng bắt đầu `#` bị bỏ qua. File rỗng = đoạn không có lời. v1.4: file video không có luồng âm → kịch bản rỗng thì J1, J1b = "—"; có lời thì THIẾU. |
| `X.text/elements.json` + matte PNG | P0, P1, G4 (P0 dùng thêm `X.script.txt` nếu có) | Mỗi phần tử chữ (tiêu đề, phụ đề, credit, **cả chữ trong thế giới phim như biển hiệu**) xuất một matte RGBA từ render (mục 3.1). Thư mục rỗng phần tử (`{"elements": []}`) = đoạn không có chữ. P0 chạy cả khi thiếu thư mục này: mọi chữ máy dò thấy trong hình mà không có matte đều trượt. |
| `X.motion.json` | H1, H1b | Chuyển động bake theo từng khung ở 24 fps (mục 3.2), **kèm `screen_tracks`** (mục 3.4). |
| `X.stems/` | J1b, J1 | Stem thoại `dialogue.wav` và stem nền (M&E) xuất từ bản mix (mục 3.5). |
| `X.parts/parts.json` + mặt nạ PNG | C3 | Mặt nạ từng bộ phận nhân vật xuất từ render, mỗi 12 khung, **ở 2–4× độ phân giải khung** (4× khi đầu < 100 px), kèm `views` (v1.4) (mục 3.6). |
| `X.audit/` | C3 | Yêu cầu kiểm toán (P phát), mặt nạ render lại và `render.log` (mục 3.7). |
| `X.assets.json` | O3 | Danh sách tài sản mà file cảnh thật sự nạp, xuất từ phần mềm dựng (mục 3.3). |

Có thể chỉ đường dẫn khác bằng `--script`, `--text`, `--motion`, `--stems`, `--parts`, `--assets`, `--library`.

### 3.1 Matte chữ (`X.text/`)

```json
{"elements": [
  {"id": "title", "first_frame": 0,  "last_frame": 47,  "matte": "title.png"},
  {"id": "sub01", "first_frame": 48, "last_frame": 191, "matte": "sub01/%05d.png"},
  {"id": "sign_inn", "first_frame": 60, "last_frame": 140, "matte": "sign_inn/%05d.png", "diegetic": true}
]}
```

- Chỉ số khung tính từ 0 theo file video.
- Matte: PNG RGBA **đúng kích thước khung**, alpha thẳng, màu = màu **phần ruột nét chữ** (không gồm viền/bóng; viền và bóng được tính là nền khi đo tương phản).
- Chữ tĩnh dùng một PNG; chữ chuyển động dùng chuỗi PNG theo số khung (`%05d`).
- Máy đối chiếu matte với khung render: matte không khớp hình (lệch vị trí, sai màu) thì P1 và G4 trượt.
- **`"diegetic": true`** (v1.1, boolean, không phải chuỗi) chỉ dành cho chữ **nằm trong thế giới phim**: biển hiệu, tên phố, nhãn chai, trang sách mà nhân vật nhìn thấy.
  - Được miễn luật tương phản G4.
  - **Vẫn bắt buộc có matte** (P0), **vẫn tính va chạm P1**, và vẫn kiểm matte khớp render.
  - Tiêu đề, phụ đề, credit **không bao giờ** là diegetic. Máy đọc chữ trong matte diegetic và so với từng câu thoại của `X.script.txt` và với chữ của các phần tử không diegetic. Trùng thì **P0 TRƯỢT**.
  - Có thể thêm `"text": "…"` cho phần tử không diegetic (nội dung chữ) để máy so chính xác hơn.

### 3.2 Dữ liệu chuyển động (`X.motion.json`)

```json
{"fps": 24, "channels": [
  {"id": "hero/forearm_L.rot", "class": "character_part", "first_frame": 0, "values": [[0,0,0], [0.1,0,0], ...]},
  {"id": "hero/root.loc",      "class": "character_root", "first_frame": 0, "values": [...]},
  {"id": "clock/hand.rot",     "class": "mechanical", "reason": "kim đồng hồ quay đều có chủ ý", "values": [...]}
]}
```

- `values`: một giá trị mỗi khung (số hoặc vectơ), **bake** từ rig sau mọi ràng buộc, không phải khoá gốc.
- Lớp: `character_part` (bộ phận nhân vật — bị kiểm), `character_root`, `mechanical` (bắt buộc có `reason`), `camera`, `prop`. Kênh miễn kiểm được liệt kê trong báo cáo cho người duyệt.

### 3.3 Danh sách tài sản (`X.assets.json`) và thư viện

```json
{"workdir": "shots/sq01_sh010",
 "scene_files": ["shots/sq01_sh010/sq01_sh010.blend"],
 "assets": ["assets/characters/hero_v1.blend", "assets/sets/room_v1.blend"]}
```

- Đường dẫn tính từ gốc repo.
- Thư viện mặc định `assets/LIBRARY.json` (phiên P giữ và khoá):
  `{"assets": [{"id": "CHR-hero-v1", "path": "assets/characters/hero_v1.blend", "sha256": "<64 hex>", "rights": "R-001"}]}`
- Máy tính lại SHA-256 từ đĩa. Mọi file media trong `workdir` (trừ `render/`, `out/`, `cache/`, `frames/` và `scene_files`) không có trong thư viện đều bị tính là tài sản ngoài thư viện.

### 3.4 Track màn hình (`screen_tracks` trong `X.motion.json`)

```json
{"fps": 24, "channels": [...],
 "screen_tracks": [
   {"id": "hero/head",   "first_frame": 0, "values": [[812.4, 330.1], [815.0, 331.2], null, ...]},
   {"id": "hero/hand_R", "first_frame": 0, "values": [[...], ...]}]}
```

- Toạ độ **điểm ảnh của file video** (gốc trên–trái, x sang phải, y xuống), một điểm mỗi khung, là vị trí khớp nhân vật **sau mọi ràng buộc, chiếu qua máy quay render** (không phải khoá gốc). Chọn khớp nằm trên vùng có chi tiết (mép áo, bàn tay, mũ); tâm mảng màu phẳng cho luồng quang học yếu.
- `null` khi điểm bị che hoặc ra khỏi khung. Tiền tố trước `/` là tên nhân vật: mỗi nhân vật có kênh `character_part` phải có ≥ 1 track. Nên xuất 2–4 track mỗi nhân vật.
- Máy so dịch chuyển khai báo với luồng quang học trên hình render: khai một đằng, render một nẻo thì H1b trượt.

### 3.5 Stem âm (`X.stems/`)

- `dialogue.wav` (hoặc `.flac`): **chỉ thoại** (không nhạc, không tiếng động), 48 kHz, cùng điểm bắt đầu với luồng âm của video.
- Mọi file âm khác trong thư mục (`me.wav`, hoặc `music.wav` + `sfx.wav` + `amb.wav`...) được cộng thành nền.
- **Tổng các stem phải bằng mix trong file video** (sai lệch bao năng lượng P95 ≤ 3 dB; thoại và nền cùng hệ số ±1 dB). Xuất stem qua cùng bus master; limiter master nhẹ được chấp nhận. Stem thiếu âm hay khai to/nhỏ khác mix thì J1b trượt.
- Đoạn không có lời: `dialogue.wav` im lặng.

### 3.6 Mặt nạ bộ phận nhân vật (`X.parts/`)

```json
{"model_sheet": "bible/characters/hero.model.json",
 "scale": 4,
 "frames": {"0":  {"head": "00000/head.png", "torso": "00000/torso.png", "upper_arm": "00000/upper_arm.png", ...},
            "12": {...}, "24": {...}}}
```

- Mặt nạ cho **mọi khung chia hết cho 12** (0, 12, 24…). Mỗi bộ phận một PNG, bộ phận = điểm ảnh ≥ 128 (xám hoặc alpha), cùng phép biến đổi với khung hình. Khung nhân vật không hiện: mặt nạ đầu rỗng.
- **Bắt buộc (v1.1): render mặt nạ ở độ phân giải gấp 2–4 lần khung video** (ví dụ khung 1920×1080 → mặt nạ 3840×2160 hoặc 7680×4320). Cả chiều ngang và chiều dọc cùng hệ số; mọi mặt nạ cùng kích thước.
- Máy **đo hệ số từ kích thước PNG**. Trường `scale` là tuỳ chọn; nếu ghi thì phải đúng hệ số đo, sai thì C3 trượt.
- Mặt nạ phải **render thật** ở độ phân giải đó, trong cùng lần render với khung hình, bằng cách tăng độ phân giải cho pass mặt nạ. **Không** phóng to mặt nạ 1× lên. Máy kiểm vị trí biên mặt nạ trên lưới điểm ảnh: mặt nạ phóng to có biên nằm thẳng hàng theo lưới thô và C3 trượt.
- Lý do: ở đầu cao dưới ~100 px video, mặt nạ 1× có nhiễu đo ăn gần hết biên 3% (C3 báo "không chứng minh được"). Mặt nạ 4× giảm nhiễu khoảng 4 lần.
- `model_sheet`: đường dẫn tính từ thư mục `parts/` rồi từ gốc repo; bộ phận đo lấy từ `measured_parts` của sheet; độ dài đo từ đầu mút đến đầu mút dọc trục chính.
- Nhiều nhân vật: một thư mục `parts` cho mỗi lần chạy (v1 kiểm một nhân vật mỗi file; báo P nếu shot có nhiều nhân vật chính). Shot không có nhân vật: `{"no_character": true}` (người duyệt xác nhận).
- Máy đối chiếu biên mặt nạ với cạnh ảnh render: mặt nạ không khớp hình thì C3 trượt.
- **v1.3:** đầu nhân vật cao dưới 100 px video ở bất kỳ khung mẫu nào thì mặt nạ **bắt buộc 4×** (2× hoặc 3× thì C3 trượt).

#### 3.6.1 Lược đồ model sheet (v1.4)

Máy đọc model sheet (JSON) như sau. Tỷ lệ luôn là **độ dài bộ phận / độ dài đầu**, đo như C3: bề dài trục chính (PCA) của mặt nạ **nhìn thấy**.

```json
{"measured_parts": ["head", "torso", "upper_arm", "forearm"],
 "head":  {"length": 1.0},   "torso": {"length": 2.584},
 "upper_arm": {"length": 1.55}, "forearm": {"length": 0.963},
 "parts": {"head": {"length": 1.0}, "torso": {"length": 2.0}, "...": "..."},
 "c3_views": {"0°":   {"head": 1.0, "torso": 2.584, "upper_arm": 1.55,  "forearm": 0.963},
              "45°":  {"head": 1.0, "torso": 2.332, "upper_arm": 1.495, "forearm": 0.921},
              "90°":  {"head": 1.0, "torso": 2.138, "upper_arm": null,  "forearm": null},
              "-90°": {"head": 1.0, "torso": 2.153, "upper_arm": 1.406, "forearm": 1.008}}}
```

| Trường | Bắt buộc | Nghĩa |
|---|---|---|
| `measured_parts` | nên có | Bộ phận C3 đo (có hoặc không có `head`). Thiếu thì máy lấy các khoá cấp gốc có `length`, rồi tới `parts{}`, rồi tới `c3_views` |
| `<bộ phận>.length` ở **cấp gốc** | một trong ba nguồn | Độ dài góc 0°. Máy ưu tiên nguồn này |
| `parts.<bộ phận>.length` | | Dùng khi cấp gốc không đủ `head` và mọi bộ phận đo. Máy lấy **một nguồn cho mọi bộ phận**, không trộn cấp gốc với `parts{}` |
| `c3_views` | nên có (bắt buộc để có góc khác 0°) | `{góc: {bộ phận: tỷ lệ hoặc null}}`. Khoá góc: `"0°"`, `"45°"`, `"-90°"` (dấu trừ thường hoặc `−`), `"90"`. Mỗi góc phải có **mọi** bộ phận đo; `null` = bộ phận khuất ở góc đó (không đo). `head` bỏ trống thì hiểu là 1,0. Góc 0° trong `c3_views` phải khớp độ dài cấp gốc (±0,1%) |

Góc nhìn theo quy ước lúc đo sheet: 0° = nhân vật nhìn thẳng vào máy; **+90° = máy ở bên PHẢI nhân vật**; −90° = máy ở bên trái; ±180° = sau lưng. (Cách đo B1: gốc nhân vật quay `rotation.y = góc` trước máy đặt trên trục +z.)

Sheet thiếu độ dài, sai kiểu số, khoá góc không đọc được, hay `c3_views` mâu thuẫn cấp gốc thì C3 báo **THIẾU** với dòng "Sai định dạng (RUN.md mục 3.6): …" nêu đúng trường sai.

#### 3.6.2 Góc nhìn và tư thế: `views` (v1.4)

Xuất từ **chính lần render mặt nạ** (cùng cảnh, máy quay, tư thế), một mục cho **mọi** khung trong `frames`:

```json
{"model_sheet": "...", "scale": 4, "frames": {"0": {...}, "12": {...}},
 "views": {"0":  {"view_deg": -74.1, "elev_deg": 5.7,
                  "parts": {"head":    {"foreshorten": 1.000, "hidden": 0.00, "depth": 1.000},
                            "torso":   {"foreshorten": 1.000, "hidden": 0.00, "depth": 0.997},
                            "forearm": {"foreshorten": 0.998, "hidden": 0.00, "depth": 0.975}}},
           "12": {...}}}
```

| Trường | Cách tính (trên cảnh render, không khai tay) |
|---|---|
| `view_deg` | Hướng từ tâm thân (giữa hai đầu xương thân) tới máy quay, đổi sang hệ gốc nhân vật (x = trái nhân vật, y = lên, z = hướng mặt): `view = −atan2(x, z)` theo độ. Cùng quy ước với khoá `c3_views` |
| `elev_deg` | Góc ngẩng của cùng vectơ: `atan2(y, √(x² + z²))`. Dương = máy ở trên |
| `foreshorten` | Độ dài hình chiếu lên mặt phẳng ảnh của xương bộ phận (tâm khớp → tâm khớp; đầu: gốc đầu → đỉnh đầu) **bây giờ**, chia cho của cùng xương khi đặt góc khớp về tư thế `turnaround` (giữ gốc nhân vật và máy quay). 1 = không co ngắn do tư thế |
| `hidden` | 1 − (điểm ảnh bộ phận nhìn thấy trong cảnh) / (điểm ảnh bộ phận khi chỉ vẽ **thân nhân vật**: mọi lưới bộ phận và trang phục, bỏ cảnh, đạo cụ, nhân vật khác). Trang phục tự che theo thiết kế không tính |
| `depth` | Độ sâu theo trục máy quay của điểm giữa xương bộ phận / của tâm đầu. Máy trực giao: 1 |

Phải có mục cho `head` và mọi bộ phận đo có mặt nạ ở khung đó. Công cụ tham chiếu (cách tính trên trang three.js của phim): `reports/checks-v1.4/dryrun/k_views.js`.

**Máy quyết một mẫu (khung × bộ phận) là "không đo được" khi:**

| Điều kiện | Ngưỡng | Nguồn |
|---|---|---|
| Đầu hoặc bộ phận chạm mép khung (bị cắt) | chạm | máy đo từ mặt nạ, không cần `views` |
| Không có mặt nạ đầu | — | máy |
| Góc 3D giữa hướng nhìn (view, elev) và góc `c3_views` gần nhất | > 30° | `views` (quyết định chủ dự án) |
| Đầu: \|foreshorten − 1\| hoặc hidden | > 0,02 / > 0,10 | `views`; cả khung không đo được |
| `c3_views` ghi `null` cho bộ phận ở góc gần nhất | — | sheet |
| Bộ phận: hidden | > 0,10 | `views` |
| Bộ phận: \|foreshorten − 1\| (gập) | > 0,02 | `views` |
| Bộ phận: \|depth − 1\| (phối cảnh) | > 0,02 | `views` |

- Mẫu đo được so với **số của góc gần nhất** trong `c3_views` (không nội suy), theo quy tắc dải bảo vệ như cũ.
- Mặt nạ bộ phận rỗng mà `views` khai không bị che (hidden ≤ 0,10) thì tính **thiếu mặt nạ** (lỗi, như v1.3).
- Báo cáo C3 nêu: số mẫu đo được / tổng mẫu, **theo từng shot** (tách shot như G3b), và danh sách mẫu không đo được kèm lý do.
- **Shot có nhân vật mà không mẫu nào đo được → C3 = CẦN NGƯỜI XEM.** Không khai `views` sai để lách: kiểm toán ngẫu nhiên render lại cả `views` (mục 3.7).
- Không có `views`: mọi mẫu so với góc 0° như v1.3 (chỉ loại mẫu bị cắt khung). Đây là cách chặt nhất, không phải cách lách.

### 3.7 Kiểm toán ngẫu nhiên mặt nạ C3 (`X.audit/`, v1.3)

Mục đích: xác nhận mặt nạ đã nộp thật sự được render từ file cảnh đã khoá, ở đúng độ phân giải khai, chứ không phải phóng to hay vẽ tay. Xưởng **không biết trước** khung nào sẽ bị kiểm.

**Bước 1: phiên xưởng nộp**
- Nộp video, `X.parts/` và `X.assets.json` như thường lệ.
- Từ lúc này **không sửa** video hay mặt nạ nữa. Máy so SHA-256; sửa sau khi phát yêu cầu thì TRƯỢT.

**Bước 2: phiên P phát yêu cầu** (xưởng không tự chạy lệnh này):
```bash
/opt/cine/bin/python checks/audit.py issue <X.mp4>
```
- Máy lấy hạt giống ngẫu nhiên từ hệ điều hành và chọn 1–2 khung trong các khung có mặt nạ đầu.
- Kết quả ghi vào `X.audit/request.json` (hạt giống, khung, giờ phát, SHA video, SHA bộ mặt nạ). Hạt giống được chép vào báo cáo C3.
- Lệnh từ chối phát lại khi đã có yêu cầu, để không ai chọn lại khung cho có lợi.
- P commit `request.json` rồi giao khung cho xưởng.

**Bước 3: phiên xưởng xem khung phải render lại**
```bash
/opt/cine/bin/python checks/audit.py show <X.mp4>
```

**Bước 4: phiên xưởng render lại và nộp**
- Render lại mặt nạ bộ phận **đúng các khung đó**, từ **file cảnh đã khoá** (file trong `scene_files` của `X.assets.json`), bằng **đúng cách** đã dùng cho mặt nạ nộp: cùng độ phân giải, cùng pass.
- Đặt mặt nạ render lại vào:
```
X.audit/rerender/<khung 5 chữ số>/<bộ phận>.png     # ví dụ X.audit/rerender/00036/head.png
```
  Phải đủ mọi bộ phận có trong `parts.json` ở khung đó, cùng kích thước PNG.
- **v1.4:** `parts.json` có `views` thì xuất lại `views` của đúng khung đó vào `X.audit/rerender/<khung 5 chữ số>/views.json` (cùng lược đồ một mục của `views`). Lệch bản nộp quá 1° (góc nhìn, góc ngẩng) hoặc quá 0,005 (foreshorten, hidden, depth) thì C3 TRƯỢT.
- Ghi `X.audit/render.log`. Dòng tự do được phép, nhưng bắt buộc có:
```
SCENE shots/sq01_sh010/sq01_sh010.blend SHA256 <sha256 của file cảnh, 64 hex>
FRAME 36 CMD blender -b shots/sq01_sh010/sq01_sh010.blend -P tools/render_masks.py -- --frame 36 --scale 4
```
  - Có một dòng `FRAME … CMD …` cho **mỗi** khung được chọn, chép đúng lệnh đã chạy.
  - Đường dẫn file cảnh tính từ gốc repo.

**Bước 5: chạy lại `checks/run.py`.** C3 đối chiếu và **TRƯỢT** khi có một trong các lỗi sau:

| Lỗi | Điều kiện trượt |
|---|---|
| Sửa sau khi phát yêu cầu | video hoặc bộ mặt nạ khác SHA lúc phát |
| Log | thiếu `render.log`, thiếu dòng `SCENE`, hoặc thiếu dòng `FRAME … CMD` cho khung được chọn |
| File cảnh | SHA trong log khác file cảnh trên đĩa, hoặc file cảnh không thuộc `scene_files` |
| Không render lại được | thiếu mặt nạ render lại, hoặc khác kích thước với mặt nạ nộp |
| Lệch tỷ lệ | tỷ lệ bộ phận/đầu của mặt nạ nộp lệch mặt nạ render lại quá 1 dải nhiễu U |
| Lệch điểm ảnh | điểm ảnh khác nhau vượt 2% số điểm ảnh biên. Render lại cùng cách thì mặt nạ gần như trùng khít |
| `views` (v1.4) | thiếu `views.json` render lại, sai định dạng, hoặc lệch bản nộp quá 1° / 0,005 |

Chưa có `request.json` thì C3 báo **THIẾU**, và kết luận không thể là ĐẠT.

## 4. Luật trong bộ v1.4 (đều cấp Chặn)

| Mã | Luật | Profile |
|---|---|---|
| N1 | 24 fps CFR; không rơi/lặp khung theo PTS | mọi |
| N2 | BT.709 đủ nhãn, dải limited (đo cả giá trị điểm ảnh) | mọi |
| N3 | Codec, bitrate, 16:9, SAR 1:1 theo loại master. **v1.1: master YouTube có grain (σ ≥ 0,8 theo G3b) phải ≥ 30 Mbps** (1080p) | youtube, archive |
| P0 | Máy dò chữ độc lập: mọi chữ trong hình phải có matte; chữ gắn diegetic không được trùng phụ đề/tiêu đề | mọi |
| P1 | Không chữ đè chữ theo điểm ảnh nét | mọi |
| G4 | Tương phản chữ ≥ 4,5:1 (miễn phần tử `diegetic`) | mọi |
| G3 | Không banding trên gradient | mọi |
| G3b | Grain có, ổn định theo thời gian và giữa shot, chuyển động theo khung | mọi |
| M1 | −14 LUFS ±1; true peak ≤ −1 dBTP | youtube |
| M3 | Tương quan pha, tương thích mono | mọi |
| J1 | ASR trên mix cuối, theo từng câu: 100% từ kịch bản, WER ≤ 5%; chèn chỉ tính khi stem thoại có lời. v1.4: không có luồng âm → kịch bản rỗng "—", có lời THIẾU | mọi |
| J1b | Lời rõ trên nhạc theo từng câu (stem), tổng stem khớp mix. Ngưỡng SII **nội bộ, chưa hiệu chuẩn** (hiệu chuẩn sau bài thử với 3–5 người nghe mù) nhưng vẫn cấp Chặn. v1.4: không có luồng âm → như J1 | mọi |
| H1 | Không chuyển động tuyến tính ở bộ phận nhân vật | mọi |
| H1b | Chuyển động khai báo khớp hình render (luồng quang học) | mọi |
| C3 | Tỷ lệ bộ phận nhân vật đúng model sheet (có tính nhiễu đo); mặt nạ 2–4× (4× khi đầu < 100 px); kiểm toán ngẫu nhiên. v1.4: chỉ so ở mẫu đo được theo góc nhìn/tư thế (`views`, `c3_views`); shot không có mẫu đo được = CẦN NGƯỜI XEM | mọi |
| O3 | Tài sản lấy từ thư viện có SHA | mọi |

Định nghĩa đo và ngưỡng đầy đủ có trong từng báo cáo (mục "Chi tiết từng luật").

## 5. Ghi chú vận hành

- Thời gian đo thật (v1): mẫu 1080p24 dài 8 giây, profile youtube, chạy hết 16 luật trong ~60 giây trên máy 4 vCPU (H1b 12,6 s, C3 11,4 s, P0 7,0 s, J1 7,0 s). Bản dài hơn tăng gần tuyến tính theo thời lượng ở J1, J1b, P1, H1b (tối đa 480 cặp khung) và C3 (mỗi 12 khung); G3, G3b, N2, P0 lấy tối đa 240 khung/cặp. Lần chạy đầu tải mô hình ASR (~480 MB) từ Hugging Face; mô hình dò chữ của P0 đã nằm sẵn trong `checks/models/`.
- v1.1: ở profile youtube, N3 dùng chung số đo grain với G3b (không giải mã hai lần). C3 với mặt nạ 4× đọc chậm hơn 1× khoảng 10–16 lần mỗi khung mẫu.
- Kiểm tính toàn vẹn luật: `/opt/cine/bin/python checks/lock.py --verify` (in KHỚP/KHÔNG KHỚP).
- Không thêm phần tử chỉ để vượt ngưỡng. Luật đo sai thì khiếu nại, không lách.
