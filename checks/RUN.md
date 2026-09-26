# CHẠY LUẬT KIỂM L1 — hướng dẫn cho phiên xưởng

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
| (lỗi dòng lệnh) | 4 | Không thấy file video |

Báo cáo liệt kê mọi chỉ số nằm trong ±5% quanh ngưỡng. **Phải chép danh sách này vào báo cáo gói việc** (luật cứng CLAUDE.md).

## 3. File đi kèm (đặt cạnh file video, cùng tên gốc)

Máy đo từ file đã render. Các file đi kèm dưới đây là **dữ liệu xuất ra từ phần mềm dựng/render**, không phải bản khai tay. Thiếu file thì luật tương ứng báo THIẾU và kết luận không thể là ĐẠT.

Với video `X.mp4`:

| File | Dùng cho | Nội dung |
|---|---|---|
| `X.script.txt` | J1 | Lời thoại tiếng Anh đúng như kịch bản cho đoạn phim này. Mỗi câu một dòng; cho phép nhãn người nói `NAME:` đầu dòng; chỉ dẫn diễn xuất trong `[...]` hoặc `(...)` và dòng bắt đầu `#` bị bỏ qua. File rỗng = đoạn không có lời. |
| `X.text/elements.json` + matte PNG | P1, G4 | Mỗi phần tử chữ (tiêu đề, phụ đề, credit) xuất một matte RGBA từ render (mục 3.1). Thư mục rỗng phần tử (`{"elements": []}`) = đoạn không có chữ. |
| `X.motion.json` | H1 | Chuyển động bake theo từng khung ở 24 fps (mục 3.2). |
| `X.assets.json` | O3 | Danh sách tài sản mà file cảnh thật sự nạp, xuất từ phần mềm dựng (mục 3.3). |

Có thể chỉ đường dẫn khác bằng `--script`, `--text`, `--motion`, `--assets`, `--library`.

### 3.1 Matte chữ (`X.text/`)

```json
{"elements": [
  {"id": "title", "first_frame": 0,  "last_frame": 47,  "matte": "title.png"},
  {"id": "sub01", "first_frame": 48, "last_frame": 191, "matte": "sub01/%05d.png"}
]}
```

- Chỉ số khung tính từ 0 theo file video.
- Matte: PNG RGBA **đúng kích thước khung**, alpha thẳng, màu = màu **phần ruột nét chữ** (không gồm viền/bóng; viền và bóng được tính là nền khi đo tương phản).
- Chữ tĩnh dùng một PNG; chữ chuyển động dùng chuỗi PNG theo số khung (`%05d`).
- Máy đối chiếu matte với khung render: matte không khớp hình (lệch vị trí, sai màu) thì P1 và G4 trượt.

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

## 4. Luật trong bộ v0 (đều cấp Chặn)

| Mã | Luật | Profile |
|---|---|---|
| N1 | 24 fps CFR; không rơi/lặp khung theo PTS | mọi |
| N2 | BT.709 đủ nhãn, dải limited (đo cả giá trị điểm ảnh) | mọi |
| N3 | Codec, bitrate, 16:9, SAR 1:1 theo loại master | youtube, archive |
| P1 | Không chữ đè chữ theo điểm ảnh nét | mọi |
| G4 | Tương phản chữ ≥ 4,5:1 | mọi |
| G3 | Không banding trên gradient | mọi |
| M1 | −14 LUFS ±1; true peak ≤ −1 dBTP | youtube |
| M3 | Tương quan pha, tương thích mono | mọi |
| J1 | ASR trên mix cuối: 100% từ kịch bản, WER ≤ 5% | mọi |
| H1 | Không chuyển động tuyến tính ở bộ phận nhân vật | mọi |
| O3 | Tài sản lấy từ thư viện có SHA | mọi |

Định nghĩa đo và ngưỡng đầy đủ có trong từng báo cáo (mục "Chi tiết từng luật").

## 5. Ghi chú vận hành

- Thời gian đo thật: mẫu 1080p24 dài 8 giây, profile youtube, chạy hết 11 luật trong 16 giây trên máy 4 vCPU (J1 chạy ASR lâu nhất, ~4,5 giây). Bản dài hơn tăng gần tuyến tính theo thời lượng ở J1 và P1; G3 và N2 lấy tối đa 240 khung. Lần chạy đầu tải mô hình ASR (~480 MB) từ Hugging Face.
- Kiểm tính toàn vẹn luật: `/opt/cine/bin/python checks/lock.py --verify` (in KHỚP/KHÔNG KHỚP).
- Không thêm phần tử chỉ để vượt ngưỡng. Luật đo sai thì khiếu nại, không lách.
