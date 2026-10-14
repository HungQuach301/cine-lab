# V4 — zoom nhiều tầng, tách nền chân dung, footage thật + hai sửa nhỏ sau V3 (phiên V4, 14/10/2026; chủ dự án duyệt 22:11 F1–F5 và 22:55 G1–G4)

- **Nhánh:** `k2-visual4`, tạo từ `main` mới (`650f05b`). **Không merge.** Không sửa `checks/`, không đọc mã trong `checks/` (chỉ chạy công cụ của K), không sửa tệp của tập.
- **Kinh thánh:** `docs/BIBLE-KENH2.md` thay bằng nguyên văn bản bổ sung 14/10 22:11 (commit `e17ae3f`), đã đọc kỹ §4 trước khi làm.

## 0. Tóm tắt
| Hạng mục | Kết quả | Ngưỡng / so sánh |
|---|---|---|
| Bước 0 | AUTHORSHIP V3 ghi; kiểm trước push sạch; `k2-visual3` → `main` **fast-forward** `c226cbf` → `650f05b` | main phải đang @c226cbf — **khớp** |
| Module mới | `relief/map` + `aerial`/`close` (zoom nhiều tầng), `photo/cutout` (tách nền), `footage/clip` chỉnh màu, `cols.layout: row`, bảng điểm gọn một dòng/hàng | — |
| Cuộn mẫu `K2V4-reel.yaml` | 65 s, 7 đoạn: Z 10 · H 15 · J 10 · N 7 · F 8 · P 9 · S 6 | lệnh "~60 s": **dài hơn 5 s** (giữ nguyên H, J của V3 để cặp chấm P1/P2 so được với các vòng trước) |
| Footage | **12,3 %** (8,0 s / 65 s), 2 clip tài sản công, mỗi clip ≤ 4,4 s | ≤ 20 % — ĐẠT |
| Nhịp thị giác (`rhythm-v4.json`) | TB **1,14 s**, khoảng dài nhất 4,15 s, khung tĩnh dài nhất 4,04 s, 0 biến cố không khớp | ≤ 3,5 s / ≤ 6 s — ĐẠT |
| Chữ (1080p) | mép 48 px: **0 vi phạm** (gần nhất 62 px); chữ < 30 px: 0; tương phản < 4,5: 0; chữ bảng điểm nhỏ nhất **34 px** | G3 ≥ 34 px — ĐẠT (**sát ngưỡng**: "Advantages:", tên hai bang ở huy hiệu góc đúng 34,0 px) |
| Giờ render 1080p (một lần, SPP2, 4 tiến trình) | cảnh (3D + footage) **1,79 s/khung**; toàn bộ **2,12 s/khung** (3 313 s / 1 560 khung) | T1: 1,86 / 2,47 s/khung. V3: 2,58 / 2,98 |
| Chấm mù vòng 5 (7 cặp × 3 người) | mới được chọn **21/21**; tay nghề TB 5 cặp cũ **7,13** (V3 7,20); TB 7 cặp **6,95** (T1 5,67) | mục tiêu ≥ 8 — **CHƯA ĐẠT** |
| Chi phí Claude API | **$1,27 / trần $5** (22 lượt, chỉ `claude-sonnet-5-5`) | — |
| `lock.py --verify` · `test_k2v.py` | **KHỚP** (`c598467f…`) · **23/23 ĐẠT** (thêm 5 phép kiểm V4) | — |

**Chỉ số trong ±5 % quanh ngưỡng (luật cứng):** chữ huy hiệu góc 34,0 px (ngưỡng G3 34 px, cách 0 %). Các chỉ số khác cách ngưỡng xa (footage 12,3 % vs 20 %; nhịp 1,14 vs 3,5 s; khung tĩnh 4,04 vs 6 s; mép 62 vs 48 px).

## 1. Bước 0 và 0b
- `AUTHORSHIP.md`: thêm dòng "V3 (DUYỆT 22:11 và 22:55) + giao V4", nêu F2/F3/F4 và G1–G4.
- Kiểm trước push `k2-visual3`: không email (chỉ `noreply@anthropic.com` trong dòng ký), tệp lớn nhất 0,54 MB, `lock.py --verify` KHỚP, `test_k2v.py` 18/18.
- `main` @`c226cbf` đúng như lệnh → đẩy fast-forward lên **`650f05b`**. Tạo `k2-visual4` từ đó.
- Bước 0b: `docs/BIBLE-KENH2.md` = nguyên văn khối giữa hai dòng `===` của lệnh.

## 2. Module và API (chi tiết: `design/k2v/README.md` mục V4)
### 2.1 Zoom nhiều tầng (F4) — `relief/map` + `scripts/k2/aerial.py`
- **Tầng ảnh hàng không** `aerial: [{img, bbox, fade: [dXa, dGần], feather}]`: tấm ảnh phủ đúng toạ độ trên địa hình (theo độ cao), mép mờ dần. Độ hiện **theo khoảng cách máy trên thang log**, không theo giờ → hai tầng luôn chồng nhau ở cùng tỉ lệ, không giật. Ô không có ảnh và mặt nước lớn → trong suốt, để hồ/sông của bản đồ hiện qua (ranh ảnh NAIP trên Hồ Ontario không lộ khối — lỗi này thấy ở nháp đầu và đã sửa).
- **Tầng gần** `close: {img, at, kb, tone}`: ảnh toàn khung hoà lên (1,0 s), tiếp tục "lặn" bằng Ken Burns với độ phóng tăng theo hàm mũ; ảnh đen trắng chuyển tông sepia của kênh (không tô màu).
- `camGround: true`: tâm nhìn trên mặt đất thật khi xuống tầm km (mặc định giữ hành vi V3).
- Khai theo mốc lời như các module khác (mốc `cam[].t`, `close.at`; `rhythm.py` đã tính `close.at`).
- **Cuộn mẫu:** bang New York (640 km, bảng màu TỰ NHIÊN) → Lockport (150 km) → 4 tầng NAIP 130 / 40 / 12 / 3,2 km (43 / 13 / 4 / 0,9 m/px) → khu âu (máy nghiêng 28–38°, cách 1,2–3 km) → hoà sang bưu thiếp "The Locks, Lockport, N.Y." 1905 (sepia) + chip "1905".
- Đề tài trung tính: Lockport, dãy âu trên kênh Erie.

### 2.2 Tách người khỏi nền (F2) — `scripts/k2/cutout.py` + cảnh `photo/cutout`
- Mô hình mã nguồn mở chạy **cục bộ** (rembg 2.0.85 + ONNX Runtime CPU, venv riêng). So 4 mô hình bằng `cutout.py try` (BiRefNet-portrait, BiRefNet-general, IS-Net, U²-Net) rồi chọn theo tờ kiểm mép 2× và số đo. Không dùng `bria-rmbg` (CC BY-NC).
- Chỉ tách nền: lớp người = điểm ảnh gốc × alpha. Bỏ mảnh rời, lấp lỗ nhỏ; không vẽ thêm điểm ảnh.
- Commit: mặt nạ `design/k2v/cutouts/<rid>-mask.png`, nền mờ `<rid>-bg.jpg` (nền gốc lấp chỗ người + mờ), sổ `<rid>.json` (SHA ảnh/mặt nạ/trọng số, mô hình, số đo mép). **Trọng số không vào git.**
- `photo/cutout`: viền trắng + bóng đổ cùng thuật toán `STK.style` (giãn alpha 32 hướng × 2 vòng, bóng mềm lệch xuống phải). Người, bóng, nền đặt ở ba độ sâu → máy tiến + trượt ngang cho **thị sai thật (Ken Burns 2.5D)**. Nền: `blur` hoặc bản đồ sepia + tuyến kênh.

| Ảnh | Mô hình chọn | Lệch đường viền TB / p95 | Dải mềm TB | Kiểm 2× |
|---|---|---|---|---|
| DeWitt Clinton (Morse 1826, MET-11602) | BiRefNet-portrait (giữ sợi tóc tốt nhất) | 0,21 / 0,39 px | 6,78 px | không răng cưa; dải mềm là mép áo tối trên nền tối của chính bức tranh. Vượt ngưỡng tự đặt 6 px của `cutout.py`; ở khung 1080p (thu 0,6×) còn ≈ 4 px. **Giữ, không làm cứng mép.** |
| Stephen Van Rensselaer (Harding ~1828, MET-10991, mới) | BiRefNet-general (bản portrait lấn sang tay ghế) | 0,21 / 0,41 px | 4,22 px | không răng cưa, tóc bạc giữ được |

- Tờ kiểm mép 2× ở cache: `$K2V_CACHE/cutout/<rid>/edge2x.jpg`. `test_v4_cutout_masks` chặn khi lệch p95 > 1,5 px, thiếu mặt nạ, hoặc SHA lệch sổ.

### 2.3 Footage thật (F3) — `footage/clip` + `scripts/k2/footage_share.py`
- Thêm: `grade: 'sepia'|'natural'` (bảng màu kênh), `clean` (khử nhiễu + làm nét nhẹ), `ivtc` (gỡ kéo xuống 3:2). Điểm ảnh không vuông luôn đưa về vuông trước khi cắt khung 16:9.
- Chuyển cảnh hoà giữa hai clip (`in: fade`). Chú thích + dòng nguồn ngắn ≥ 38 px.
- `footage_share.py` kiểm: footage ≤ 20 % thời lượng; mỗi clip có `p.clip` + `p.setting` + SHA; mỗi clip có tệp giấy phép ghi đúng SHA; clip ≤ 8 s.
- Footage đúng nội dung câu:
  - F1 "A barge in a lock on New York's Erie Canal (1957 newsreel)" — cảnh từ trên không, sà lan trong buồng âu.
  - F2 "2025: a replica 19th-century packet boat passes Black Rock Lock in Buffalo" — đúng mô tả của USACE.

### 2.4 Hai sửa nhỏ sau V3
- **G2 xu:** bỏ vạch ×10. Thay bằng `cols[].layout: 'row'`: hàng 10 đồng nằm phẳng rơi lần lượt, cạnh hàng 1 đồng. Mỗi đồng đặt trên điểm cao nhất dưới nó (nháp đầu có đồng lún vào địa hình — đã sửa), giữ bóng thật + viền; nhãn "$90–125", "1/10" như cũ. Nhãn ACTUAL để phiên K.
- **G3 bảng điểm:** khi `w < 1000`, mỗi hàng MỘT dòng (biểu tượng + nhãn 36 px bên trái, giá trị 40/42 px). Bỏ "vs" và dòng phụ `sub`; tên hai phía 36 px; huy hiệu góc 34 px. Rộng 768 px = 40 % khung. Đo trên log 1080p: chữ nhỏ nhất trong bảng 36 px, huy hiệu góc 34 px, dòng nguồn 38 px.
- **G4:** giữ cấu hình V3 (SPP2 + bóng 1024 + viền 12 hướng), không hạ gì.

### 2.5 Sửa chung khác
- `rhythm.py`: mốc lớp 2D (`p.*`) tính là **giây trong đoạn**, đúng cách `k2.js` vẽ. Trước đây cộng thêm mốc shot — chưa lộ vì V2/V3 mỗi đoạn một shot. Cuộn K2V2 vẫn ĐẠT sau sửa.

## 3. Giấy phép từng tài sản (chi tiết `RIGHTS.md` mục V4; văn bản trang giấy phép `channel-k2/k2v4-mau/licenses/`)
| Mã | Tài sản | Giấy phép | Vào git | SHA-256 | Rủi ro Content ID |
|---|---|---|---|---|---|
| K2V4-AER-1 | NAIP 2019 (USDA FSA) qua USGS `USGSNAIPPlus`, 4 tầng | Tài sản công (FSA "public domain information", xin ghi "USDA Farm Service Agency"; USGS "U.S. Public Domain") | không | `aerial-lockport-meta.json` | không áp dụng (ảnh tĩnh) |
| K2V4-PHO-1 | "The Locks, Lockport, N.Y.", Rotograph 1905, LOC 2025670941 | "No known restrictions on publication." | không | TIFF `e5747079…`, bản cắt `4477fc80…` | thấp |
| MET-10991 | Van Rensselaer, C. Harding ~1828 — **đã chỉnh sửa (tách nền)** | Met Open Access, `isPublicDomain: True` | có (1400×1805, 0,54 MB) + mặt nạ | gốc `33b3d812…` | thấp |
| MET-11602 | Clinton, S. F. B. Morse 1826 — **đã chỉnh sửa (tách nền)** | Met Open Access | có (sẵn từ V2) + mặt nạ | `73c2c15f…` | thấp |
| K2V4-FTG-1 | Newsreel 1957 (Warner Pathé), Prelinger, 4,9 s | "Usage: Public Domain" (PD mark) | **không** | `85ec6a67…` | **TRUNG BÌNH**: newsreel PD hay bị bên tổng hợp khai báo; chưa kiểm YouTube |
| K2V4-FTG-2 | USACE Buffalo, DVIDS 978155, 2025, 4,1 s | "PUBLIC DOMAIN" (tác phẩm nhân viên chính phủ Mỹ); không dùng huy hiệu USACE | **không** | `62826fed…` | THẤP–TRUNG BÌNH |
| K2V4-SEG-1..3 | rembg (MIT), onnxruntime (MIT), PyMatting (MIT); trọng số BiRefNet (MIT), U²-Net/IS-Net (Apache-2.0, chỉ để so) | như cột trước | **không** (trọng số) | `RIGHTS.md` | — |

- Ứng viên tra được nhưng **không dùng** (vẫn lưu trang giấy phép để tham khảo): Gouverneur Morris (Met 15082, ảnh nhỏ hơn 1 500 px), "Canal boat colony" (LOC Bain, không rõ địa điểm), stereograph Keystone Lockport 1905.
- **Clip hiện đại:** Pexels/Pixabay không có clip nào đúng kênh Erie (chỉ ra kênh ở Anh, Đức, Welland…). Phiên chọn clip tài sản công của USACE, đúng âu Black Rock nối kênh với hồ Erie, đúng dịp 200 năm.

## 4. Cuộn mẫu và tỉ lệ footage
| Đoạn | Thời lượng | Nội dung | Module |
|---|---|---|---|
| Z (móc) | 0–10 s | Bang NY nổi → vòng Lockport → 4 tầng ảnh hàng không → khu âu → hoà sang bưu thiếp 1905 | relief + aerial + close |
| H | 10–25 s | Hook V3 giữ nguyên (khe Mohawk, sepia, NY/PA nổi, tuyến kênh) | relief |
| J | 25–35 s | Hành trình V3 giữ nguyên | relief + vật trong cảnh + A-lite |
| N | 35–42 s | Hàng 10 xu (cước xe ngựa) cạnh 1 xu (kênh), xe hàng + thuyền 3D | relief cols row |
| F | 42–50 s | Footage 1957 (sepia) → hoà → footage 2025 (tự nhiên) | footage/clip |
| P | 50–59 s | Clinton tách nền trên bản đồ sepia + tuyến kênh → hoà → Van Rensselaer trên nền mờ | photo/cutout |
| S | 59–65 s | Bảng điểm gọn ≥ 34 px | relief + score |

- Footage 8,0 s / 65 s = **12,3 %** (`footage-share-v4.json`). Nguồn ngoài phim gồm cả chân dung (`q_footage`): 26,2 %.
- **Video (ngoài git, chỉ SHA):** `/var/tmp/cine-out/k2v-shots/K2V4-reel/shot.mp4`, 1920×1080, 24 fps, 65,0 s, 168,7 MB, SHA-256 `3f301f793fec5cb7d819e6a392c26fc966247b69e164ee9ff1fd7bb20a6a0576`.
- **Tờ khung:** `channel-k2/k2v4-mau/to-khung-540.jpg` (nháp 2) và `to-khung-1080.jpg`. Sổ footage: `SOURCES-FOOTAGE.csv`. Timeline: `K2V4-reel.timeline.json`.
- **Ghi chú sau dựng:** thêm `p.file` vào hai shot footage (để `q_footage` tìm tệp kiểm SHA). Trường này không ảnh hưởng hình. Hai đường dẫn liên kết trong `/var/tmp/k2-footage/k2v4-reel/`.

## 5. Nhịp
- 63 biến cố khai → 57 sau gộp; **TB 1,14 s**; khoảng dài nhất 4,15 s (S, sau hàng cuối bảng điểm); khung tĩnh dài nhất 4,04 s (60,67 s).
- 9 cắt cứng: 7 đầu đoạn + 2 hoà giữa hai shot trong F và P.
- Theo đoạn: Z 12 biến cố / 10 s · H 14 / 15 · J 10 / 10 · N 8 / 7 · F 4 / 8 · P 8 / 9 · S 7 / 6.

## 6. Giờ render (1080p MỘT lần sau tờ khung 540p; SPP2 + bóng 1024 + viền 12 hướng; 4 tiến trình trên 4 vCPU)
| Đoạn | Khung | s/khung mỗi tiến trình (chạy song song, `measure-1080-spp2-v4.json`) | 1 tiến trình, đo riêng (`measure-1tien-trinh-v4.json`)* |
|---|---|---|---|
| **Z zoom** | 252 | **7,12** | bản đồ 3,76 · **chuyển tầng ảnh hàng không 3,68** · tầng gần (ảnh + Ken Burns) 4,33 |
| H relief | 372 | 7,13 | 4,15 |
| J | 252 | 11,08 | — |
| N | 180 | 9,20 | — |
| **F footage** | 118 + 99 | **0,14 / 0,26** | trích khung ffmpeg |
| **P tách nền** | 120 + 120 | **2,98 / 3,18** | 1,17 |
| S | 156 | 7,18 | — |
| **Toàn cuộn** | 1 560 | cảnh (3D + footage) **1,79 s/khung** đồng hồ thật (2 797,8 s); toàn bộ gồm lớp chữ + ghép **2,12 s/khung** (3 313 s) | T1 1,86 / 2,47 · V3 2,58 / 2,98 |

\* Đo 4–5 khung mỗi pha, chạy cùng lúc với chấm mù (tải CPU nhẹ). Chỉ dùng để so tương đối.

- **Zoom có nặng ở đoạn chuyển không (Kinh thánh §9):** không. Pha chuyển tầng ảnh (3,68) ngang pha bản đồ (3,76) và nhẹ hơn hook relief H (4,15). Pha tầng gần chậm hơn ~15 % vì vẫn dựng địa hình phía dưới khi ảnh hoà lên. Có thể tắt địa hình khi `close` đã đủ 100 % — chưa làm, vì lệnh G4 là không đổi cấu hình.
- **Vì sao toàn cuộn nhanh hơn T1:** 17 s footage + chân dung rất nhẹ (0,14–3,2 s/khung mỗi tiến trình). Riêng relief vẫn chậm như V3 (H 7,13 vs V3 7,12; J 11,08 vs 10,81) — G4 giữ nguyên cấu hình.

## 7. Chấm mù vòng 5 (`channel-k2/k2v4-mau/blind_v4.py`, cùng giao thức `blind_v2.py`)
- **Giao thức:** cùng đề bài và 3 vai (nạp nguyên từ `blind_v2.py`). Model ghim `claude-sonnet-5-5` — `modelUsage` chỉ có sonnet; vòng này không còn lượt phụ haiku như V2–V3.
- **Khung T1:** trích từ master `release-k2c-t1-06-v1` (SHA `4f2d280b…`, đã kiểm).
- **Mốc giây:** khai và commit trong `f607015`, **trước** lượt dựng 1080p.
- **Thứ tự X/Y:** 5 cặp cũ giữ như vòng 1–4; 2 cặp mới theo hạt giống 20261014.
- **Không sửa sau chấm.**

| Cặp | Khung mới | V3 (vòng 4) T1 → mới | **Vòng 5: T1 → mới** (từng người) | Đọc / Rõ ý mới | Chọn | Cờ mới |
|---|---|---|---|---|---|---|
| P1 bản đồ (H 13 s) | 23,0 s | 6,0 → 7,67 | 5,67 → **7,67** (8/8/7) | 8,0 / 9,0 | mới 3/3 | — |
| P2 hành trình (J 6 s) | 31,0 s | 7,0 → 7,0 | 7,0 → **6,67** (7/6/7) | 7,67 / 8,0 | mới 3/3 | — |
| P3 số liệu (G2) | 39,6 s | 4,0 → 7,0 | 5,0 → **6,0** (6/6/6) | 8,0 / 8,0 | mới 3/3 | flat_slide_look |
| P4 chân dung tách nền (F2) | 53,0 s | 5,33 → 7,0 | 6,33 → **7,67** (8/7/8) | 8,33 / 8,0 | mới 3/3 | — |
| P5 bảng điểm (G3) | 62,5 s | 3,33 → 7,33 | 3,67 → **7,67** (8/7/8) | 7,33 / 8,67 | mới 3/3 | — |
| P6 footage (F3) — mới | 44,0 s | — | 6,67 → **6,0** (6/6/6) | 8,0 / 7,67 | mới 3/3 | — |
| P7 tầng gần của zoom (F4) — mới | 8,6 s | — | 5,33 → **7,0** (7/7/7) | 8,0 / 8,0 | mới 3/3 | — |
| **TB 5 cặp cũ** | | 5,13 → 7,20 | 5,53 → **7,13** | | 15/15 | |
| **TB 7 cặp** | | | 5,67 → **6,95** | | **21/21** | 1 cờ |

- **Có tiến bộ:**
  - Chân dung tách nền **7,0 → 7,67**: "cut-out portrait with a white outline… clean hierarchy".
  - Bảng điểm **7,33 → 7,67**, rõ ý 8,67; còn nêu "table text smallish for a phone" (1/3) và "table covers part of the map".
  - Tầng gần của zoom 7,0 vs ảnh lưu trữ T1 5,33: "strong central subject… consistent sepia grade".
- **Kém đi / chưa tới 8 (ghi nhận trung thực):**
  1. **P3 hàng xu 7,0 → 6,0**, cờ `flat_slide_look`. Tỷ lệ 10 : 1 được cả 3 người khen "easy to see at a glance" (rõ ý 7,0 → 8,0, đọc 8,0). Nhưng đồng xu nằm phẳng nhìn từ trên xuống thành "flat ovals / sticker-like discs", còn xe và thuyền "look pasted on". Chồng xu V3 có chiều cao (3D) nên tay nghề cao hơn. **Đánh đổi G2: rõ ý tăng, tay nghề giảm.**
  2. **P6 footage 6,0 < T1 6,67** (Pexels 4K): newsreel 1957 gốc 368×480 phóng lên 1080p nên "soft and grainy, subject small". Nội dung, chú thích và nguồn được khen.
  3. P2 hành trình 6,67: vẫn nêu nhân vật/thuyền nhỏ, kiểu sticker.
  4. Dòng nguồn 38 px vẫn bị nêu "small" ở P1, P4, P7 (đã là quy định chủ dự án duyệt).
- **Nhiễu phép đo:** khung T1 giống hệt mà điểm dao động ±0,67 so với vòng 4 (F01 5,33 → 6,33; F03 4,0 → 5,0). Chênh ≤ 0,7 nằm trong nhiễu.
- Chi tiết: `kiem-mu/blind-score.json`, `kiem-mu/blind/P*/R*.json`, `key.json`.

## 8. Chi phí
| Hạng mục | Chi phí |
|---|---|
| Claude API (chấm mù vòng 5, 22 lượt gồm 1 lượt thử lại do JSON hỏng) | **$1,27 / trần $5** (`k2v4-mau/kiem-mu/cost.jsonl`) |
| ElevenLabs · YouTube Data API | 0 · 0 |
| Tác tử tra nguồn (trong phiên, WebSearch/WebFetch) | thuộc phiên, không qua API trả phí của dự án |
| Giờ máy | Dựng lại nền relief (tải DEM 3,2 GB, ≈ 10 phút; SHA nền khớp V2); tải trọng số 2,3 GB; thử tách nền 4 mô hình (≈ 5 phút/ảnh); nháp 540p 2 lượt (22,5 + 3,7 phút); **1080p một lần 55,2 phút**; đo 1 tiến trình ≈ 2 phút |

## 9. Kiểm trước khi đẩy
- **Không có email** trong tệp commit (chỉ `noreply@anthropic.com` ở dòng ký). User-Agent tải tư liệu: `cine-lab/1.0`.
- **Không có media lớn:** clip, ảnh hàng không, TIFF gốc, trọng số, cuộn 1080p **không** vào git hay LFS, chỉ ghi SHA. Tệp commit lớn nhất: `to-khung-1080.jpg` 0,65 MB, `to-khung-540.jpg` 0,64 MB, chân dung Van Rensselaer 0,54 MB; mặt nạ 50–60 KB.
- `checks/lock.py --verify`: **KHỚP** (`c598467f…`); không sửa `checks/`.
- `scripts/k2/test_k2v.py`: **23/23 ĐẠT**. Thêm:
  - `test_v4_footage_share`: footage ≤ 20 %, giấy phép mỗi clip có tệp và đúng SHA;
  - `test_v4_cutout_masks`: mặt nạ tách nền tồn tại, SHA khớp, mép p95 ≤ 1,5 px;
  - `test_v4_rhythm`;
  - `test_v4_zoom_api`;
  - `test_v4_coin_row_and_board`.
- **Luật K 1.10.2** (`luat-k-v4.txt`):
  - Q33 ĐẠT.
  - Q34: 9/9 shot có type, số neo 3D 100 %; (a)(b) trượt vì cuộn mẫu không có lời, như V2–V3.
  - **Q32 TRƯỢT đúng một mục:** "nguồn www.dvidshub.net ngoài danh sách cho phép (cần chủ dự án duyệt)". Sổ footage, SHA, timecode đều khớp.
- Tệp tập không bị sửa (`design/ll-hero/`, `channel-k2/k2c-t1-06/`, `channel-k2/k2g-ep01/`).

## 10. Rủi ro
- **Content ID:** newsreel 1957 (TRUNG BÌNH) — giữ trang giấy phép Prelinger làm bằng chứng; mỗi đoạn ngắn (4,9 s). Clip USACE (THẤP–TRUNG BÌNH). Phiên chưa kiểm YouTube.
- **Chất lượng footage lưu trữ:** bản gốc độ phân giải thấp làm điểm tay nghề giảm (P6). Tập thật nên ưu tiên bản quét HD (LoC/NARA) hoặc trình bày khung 4:3 trong khung hình thay vì phóng to cắt cúp.
- **Tách nền ảnh tranh tối:** mép áo tối trên nền tối mềm hơn mép tóc. Đã kiểm từng ảnh ở 2×; mỗi tập phải kiểm lại (`cutout.py try`).
- **NAIP:** dịch vụ USGS trộn NAIP với ảnh HRO của bang; vùng Lockport đã xác nhận chỉ NAIP 2019. Vùng khác phải kiểm từng tầng (`identify`). Dịch vụ từng trả 502 với ảnh 4 000 px; 3 600 px chạy được.
- **Số lệch nguồn đã né:** độ dâng ở Lockport (60 ft vs 49 ft) và vai "chủ tịch" của Van Rensselaer không đưa lên hình (`k2v4-mau/claims.md`).

## 11. Việc đang chờ chủ dự án
1. **Duyệt V4** (zoom nhiều tầng, tách nền chân dung, footage, hàng xu, bảng điểm gọn). Sau đó P ghi `AUTHORSHIP.md` và merge `k2-visual4`; phiên V4 không merge.
2. **Duyệt nguồn DVIDS** (tư liệu tài sản công của quân đội/USACE) vào danh sách nguồn footage cho phép. Q32 của K đang chặn đúng mục này; nếu không duyệt thì thay clip hiện đại (Pexels/Pixabay không có clip kênh Erie).
3. **Hàng xu (G2) làm tay nghề P3 giảm 7,0 → 6,0**, dù rõ ý tăng. Chọn hướng cho T2:
   - (a) giữ hàng xu phẳng;
   - (b) hàng 10 **chồng thấp** — mỗi ô 1 chồng nhiều đồng có độ dày, vừa đếm được vừa có khối 3D;
   - (c) quay về chồng V3 + số "10" lớn.
4. **Footage lưu trữ độ phân giải thấp** (P6 6,0): duyệt quy tắc cho tập thật — chỉ dùng tư liệu ≥ 720p, hoặc khung 4:3 có viền thay vì phóng 3×.
5. **Cuộn 65 s thay vì ~60 s:** giữ nguyên H/J của V3 để so được với các vòng chấm trước. Chấp nhận hay cắt ở T2.
6. **Còn treo:** nhãn ACTUAL (phiên K); đối chiếu trang The Met bằng mắt (máy bị 429 ở cả 11602 và 10991); Content ID trên YouTube chưa kiểm.
7. Mục tiêu tay nghề ≥ 8 **chưa đạt** (TB 5 cặp cũ 7,13). Điểm cao nhất vòng này là 7,67 (P1, P4, P5).
