Nhánh thật: `claude/eloquent-dijkstra-kemr8j` (harness buộc tên này; lệnh yêu cầu `nc-gpu`). Gốc: `origin/claude/clever-franklin-daez5k` @718dec9e (= nc-cpu). Không merge. Vùng sửa: `reports/nc-gpu/**`, `design/pt/gpu/**`. Không sửa `design/pt/cpu/**`, `design/k2v/**`, `scripts/**`, `checks/`, `docs/`, `channel-*/`. V7B (`origin/ccr-ef2b66f0-9639kq`) và NC-V2V (`origin/nc-v2v`) chỉ ĐỌC (worktree tạm ngoài repo). Không đọc mã `checks/`.

# NC-GPU — BÁO CÁO: đo thật bước nhảy chất lượng + chi phí khi dựng Cycles trên GPU thuê (chưa đổi đường ống)

## §0 Tóm tắt

| Việc | Kết quả |
|---|---|
| Bước 0 (RunPod) | **QUA.** `GET rest.runpod.io/v1/pods` → HTTP 200 `[]`; GraphQL `myself` → số dư **$25,00**. Khoá do proxy gắn; mã không đọc/in/ghi khoá. |
| Bước 0b (truyền tệp) | **QUA.** Tệp cảnh `ncg-canh.tar` **1 259,8 MB** (SHA-256 `655050540e31b966378eefb989222f98775750b9685bd36a35539e699fbaaf9e`) lên pod qua proxy HTTPS RunPod (`https://<pod>-8888.proxy.runpod.net`, máy chủ tệp tối thiểu `design/pt/gpu/pod_srv.py`, PUT theo khúc 64 MB, SHA kiểm trên pod): **61,4 s (20,5 MB/s)**; ảnh về bằng GET theo khúc (14–22 MB EXR, ≈ 1 s/tệp). Lưu ý: 1 trong 4 pod chỉ **2,0 MB/s** (§8). |
| Máy + giá | **RTX 5090 32 GB, SECURE, $1,19/h** (API `api.runpod.io/graphql gpuTypes`, đọc 20/10/2026 00:0x UTC; `reports/nc-gpu/gia-runpod-20261020.jsonl`). RTX PRO 4500 ($0,72/h): **không tạo được** — nguyên văn `{"error":"create pod: There are no instances currently available","status":500}` (00:48 UTC). RTX 4090 và mọi loại COMMUNITY: không có kho. Driver 595.91, OptiX. |
| Benchmark Blender chuẩn | Open Data launcher 3.3.0, **Blender 5.2.0** (bản gần 5.2.2 LTS nhất launcher hỗ trợ), OPTIX, RTX 5090: **monster 7 313,76 · junkshop 5 303,61 · classroom 4 037,31** mẫu/phút (`do/bench-rtx5090-optix.json`). |
| Hệ số GPU/CPU THẬT trên cảnh của ta | Khung B nhanh NC-CPU **nguyên văn** (`nc_blend.py`, 16 spp + OIDN, cùng tệp xuất, Blender 5.2.2 LTS): RTX 5090 **8,6–9,9 s** ↔ CPU 4 vCPU NC-CPU 87–127 s → **×8,9–13,4 (trung vị ×11,2)**; đo lại CPU cục bộ khung "cang" 101,7 s ↔ GPU 8,7 s → **×11,7**. Cảnh mới 64 spp "cang": CPU 397,6 s ↔ GPU 11,7 s → **×34**. |
| Cảnh Cycles "điện ảnh" | `design/pt/gpu/gpu_blend.py`: sửa 5 lỗi NC-CPU §3 + GI 8/6/6, khói/lửa thể tích từ k2v, motion blur, DOF, bụi ×3 quanh bụi có nguồn, nước phản chiếu thật, vân CC0 4k gần máy, albedo 0,5 m quanh điểm máy (§2). **Nguyên nhân "nhạt" tìm ra**: NC-CPU đặt ánh trời Cycles mạnh ≈ 3,6× so three.js (L = hemi·1,15 thay vì hemi/π) → sửa: bão hoà trung vị **0,298 → 0,403**. |
| 6 khung × 2 mức | `reports/nc-gpu/khung/gpu-64/`, `gpu-256/` (+ `b-goc-gpu/` = B NC-CPU dựng trên GPU). 64 spp: **10,9 · 11,7 · 22,2 · 11,1 · 35,9 · 125,3 s**; 256 spp: **13,1 · 12,1 · 24,1 · 13,1 · 41,5 · 265,0 s** (vây hãm · cảng · phố dày · hero · toàn cảnh · bờ + chiến sự). Tờ so: `to-so-khung.jpg`. |
| Cú lặn 20 s, 480/480 khung Cycles GPU (không ghép A↔B) | ⟨D-TOM⟩ |
| Chấm mù 640×360 (3 vai Sonnet 5.5) | **A hạng nhất 12/18, Cycles GPU 6/18, V7B 0/18.** Craft TB: A **6,22** · GPU 5,67 · V7B 5,00. Độ thật: A **5,78** · GPU 5,72 · V7B 4,22. toy_like: GPU **4,17** (tốt nhất) · A 4,44 · V7B 5,83. GPU thắng **vây hãm** và **bờ + chiến sự** (3/3 mỗi cảnh); thua A ở cảng, phố dày, hero, toàn cảnh ("washed out", "empty"). |
| So đích look Omni (chỉ số đo) | Sương (kênh tối) của GPU **0,17–0,22** ≈ Omni 0,15–0,24 (c2/c4); A 0,13–0,18; V7B 0,02–0,22. Phối cảnh khí quyển (bão hoà xa/gần) GPU 0,16–0,64 cùng chiều Omni 0,21–0,64; A/V7B ≥ 0,4–1,4. Bão hoà Omni 0,12–0,40 **thấp hơn ngưỡng 0,40 của BIBLE §11.4** (§6). |
| Ước cả tập 745 s | ⟨G-TOM⟩ |
| Chi phí thật | ⟨CP-TOM⟩ |
| Đề xuất | ⟨DX-TOM⟩ |

Xem nhanh: `reports/nc-gpu/to-so-khung.jpg` (hàng = 6 loại cảnh; cột = V7B · A · B CPU · B nguyên văn/GPU · Cycles GPU 64 · Cycles GPU 256), cú lặn `reports/nc-gpu/lan/ncg-lan-xem.mp4` + tờ `lan/to-lan.jpg`.

## §1 Máy, giá, giờ GPU thật (bật/tắt)

Giá đọc qua API RunPod (GraphQL `gpuTypes` — `securePrice`, `lowestPrice.stockStatus`) lúc 20/10/2026 ≈ 00:05 UTC, lưu nguyên `reports/nc-gpu/gia-runpod-20261020.jsonl`. Trang tham chiếu: https://www.runpod.io/pricing (không đọc được bằng API; số trong báo cáo là số API trả cho tài khoản).

| Loại | VRAM | SECURE $/h | COMMUNITY $/h | Kho (20/10 00:05) | Dùng? |
|---|---|---|---|---|---|
| RTX 5090 | 32 GB | **1,19** | 0,69 | SECURE Low · COMMUNITY không | **Có (4 pod)** |
| RTX PRO 4500 Blackwell | 32 GB | 0,72 | 0,34 | SECURE Low · COMMUNITY không | Tạo pod lỗi 500 "no instances" |
| RTX 4090 | 24 GB | 0,89 | 0,34 | không | — |
| RTX PRO 6000 Blackwell SE | 96 GB | 2,49 | 1,69 | (không hỏi kho) | — |
| L40S | 48 GB | 1,09 | 0,79 | (không hỏi kho) | — |

Ảnh pod: `python:3.13-slim-bookworm` + Blender **5.2.2 LTS** chính thức (download.blender.org, đúng bản NC-CPU dùng qua bpy 5.2.2) — `design/pt/gpu/pod_setup.sh`; máy chủ tệp `pod_srv.py` khởi động từ biến môi trường; mã TOK ngẫu nhiên một lần chặn người lạ — **không khoá GitHub/khoá dịch vụ nào lên pod**. UA mọi lệnh: "CineLab-research (+https://github.com/HungQuach301/cine-lab)"; không email trong header/URL/payload.

Sổ giờ (nguyên văn `reports/nc-gpu/gio-gpu.jsonl`, giờ UTC):

⟨BANG-POD⟩

## §2 Cảnh Cycles "chất lượng điện ảnh" (`design/pt/gpu/gpu_blend.py`, `gpu_export.js`)

Dùng lại cảnh B của NC-CPU: cùng hình học xuất từ k2v (cảnh `ncA`, máy V7B), cùng albedo nền nhìn thẳng xuống (`nc_topo.js` không sửa), cùng chỉnh màu k2v (`nc_exr.py` + `nc_grade.js`, không sửa). `gpu_blend.py` là bản sao + sửa của `nc_blend.py` (tệp gốc không đổi); `gpu_export.js` = `nc_export.js` + 3 phần thêm (bản vá `export6.js` của V7B được chèn **lúc phục vụ trang**, tệp V7B không bị sửa).

**Kiểm tái tạo:** dựng lại 6 khung B NC-CPU nguyên văn trên GPU → bão hoà trung vị **0,298** (NC-CPU 0,296), colorful 58,2 (57,5), chi tiết 31,4 (31,5) → bản xuất trong container mới khớp NC-CPU.

| Lỗi NC-CPU §3 | Nguyên nhân tìm được | Sửa | Số đo |
|---|---|---|---|
| (1) Nhạt (bão hoà 0,29–0,30) | (a) **ánh trời khuếch tán mạnh ≈ 3,6×**: three.js (V7B) irradiance bán cầu = hemi·I, BRDF/π; NC-CPU đặt nền Cycles L = hemi·I·1,15 → irradiance mặt phẳng π·L ≈ 3,6·hemi → lớp sáng xanh-xám phẳng phủ mọi màu. (b) sương phát xạ áp cho cả tia nảy → mặt xa thành nguồn sáng xám-lam | (a) `--skydif 0,277` (= 1/1,15π, khớp three.js); (b) sương chỉ trên tia máy/tia bóng | 5 khung trời trong: 0,278 → **0,380** (vây hãm 0,278 → 0,447; toàn cảnh 0,314 → 0,427; phố dày 0,251 → 0,341; cảng 0,369 → 0,380; hero 0,098 → 0,184). 6 khung cuối: trung vị **0,403** (§9: trong ±5 %) |
| (2) Nền gần mờ (4 m/px ngoài hộp 1 m) | albedo chỉ 1 m/4 m | albedo **0,5 m/px** hộp 1,8 × 1,8 km quanh điểm nhìn mỗi cổng (`near_box.py`, trạng thái đúng khung) + **vân CC0 4k** theo lớp phủ `cls.png` (cát/khô/garrigue/đá → beach/dry_ground_rocks/grass_rock/rocks, cùng họ vân cách A), tắt dần 150–700 m, pháp tuyến 4k | chi tiết |Laplace| trung vị 31,4 → **34,4** |
| (3) Mái bằng đen | vật không có màu đỉnh trong `export6.js` nhận màu từ VẬT LIỆU three.js (m.color), bản xuất cũ không ghi → Cycles nhận Attribute 'col' rỗng | xuất `rec.mc/me/mo` (màu/phát xạ/độ mờ vật liệu); vật không màu đỉnh dùng m.color; m.color trắng (màu nằm trong shader, vd. công sự) giữ vật liệu đá của NC-CPU | 203–613 vật/khung nhận màu vật liệu; không còn mái đen ở 6 khung |
| (4) Lều xám | như (3): vải lều màu vật liệu (0,84; 0,78; 0,63) | như (3) + vân vải nhẹ | lều màu vải |
| (5) Thiếu khói/lửa ngày | sprite `smokeV6` k2v không xuất | xuất MỌI cụm khói/lửa đang hiện ở khung (vị trí, cỡ, alpha, tuổi, loại) → `fx.json`; mỗi cụm một **cầu thể tích** (khói: mật độ −ln(1−0,9α)/cỡ × nhiễu × tắt mép; muội loại 2 nâu-đen; lửa: phát xạ theo chiều dài, ngọn đứng, chân sáng → đỉnh tắt + đèn điểm) | khói/lửa: vây hãm 0 · cảng 0 · phố dày 58 · hero 0 · toàn cảnh 135 · bờ + chiến sự **362 cụm + 2 lửa** |
| Cờ xám | lá cờ là CanvasTexture k2v (vật mang dữ kiện) | xuất ảnh lá cờ + UV, vải xuyên sáng | 1–30 cờ/khung đúng mẫu |

**Thêm thứ GPU làm được:** GI nảy 8/6/6 + thể tích 2 (CPU NC-CPU: 4/3/2, 0); khói/lửa thể tích mọi khung; **motion blur** (máy khung hoá ±1 khung, màn trập 180°) ở cú lặn; **DOF** f/4 (cổng: nét ở tâm khung; cú lặn: f/5,6 nét ở điểm nhìn đường máy); **bụi ×3** = 2 bản sao nhỏ (0,4–0,8×) lệch ≤ 4 m quanh MỖI bụi k2v đã qua mọi luật ẩn (năm, trại, đô thị) — 0,46–0,59 triệu bản sao thêm/khung, **không rải bụi ở chỗ k2v không có**; nước Principled nhám 0,035, IOR 1,333, phản chiếu path-traced (ánh lửa thành cột trên sóng). Không thêm vật nào không có nguồn.

**Đã thử và bỏ:** bước thể tích 10 (không nhanh hơn); `vbounce 0` (không nhanh hơn); muội chỉ-hấp-thụ (nhanh nhưng mất cột khói ban đêm). **Chọn:** thể tích chế độ `volume_biased` (ray-marching) cho cú lặn: lệch TB so null-scattering mặc định Blender 5.x **0,38/255**, nhanh **×4** (93 → 23,5 s khung đêm thử).

Lỗi nhìn thấy còn lại (P tự soi): lửa ban ngày trong phố đọc như "quả cầu sáng" (cụm lửa k2v cỡ 58 m); khói súng ngày còn sạn ở 64 spp; khung cảng/hero bị chấm "washed out/empty" (nước phẳng lặng, không thuyền nhỏ — đúng nguồn V7B, không thêm); cận cảnh lộ khối nhà k2v (hình học không đổi).

## §3 Sáu khung cổng (1920 × 1080, cùng điểm máy V7B/NC-CPU)

| Cảnh | B nguyên văn GPU 16 spp | **GPU 64 spp** | **GPU 256 spp** | CPU NC-CPU (B 16 spp) | bão hoà 64 / 256 |
|---|---|---|---|---|---|
| vây hãm (C1-a 21,8 s) | 9,87 s | **10,90 s** | 13,08 s | 88 s | 0,447 / 0,447 |
| cảng (C4 3,5 s) | 8,69 s | **11,67 s** | 12,11 s | 87 s | 0,380 / 0,380 |
| phố dày (C3 11,5 s) | 8,63 s | **22,16 s** | 24,06 s | 99 s | 0,341 / 0,341 |
| hero 2026 (H3 10,4 s) | 9,90 s | **11,08 s** | 13,05 s | 109 s | 0,184 / 0,184 |
| toàn cảnh (C5 2,6 s) | 8,87 s | **35,89 s** | 41,45 s | 106 s | 0,427 / 0,427 |
| bờ + chiến sự (H2 13,3 s) | 9,51 s | **125,28 s** | 265,00 s | 127 s | 0,453 / 0,451 |

Đường dẫn: `reports/nc-gpu/khung/gpu-64/cong-<cảnh>.jpg`, `khung/gpu-256/…`, `khung/b-goc-gpu/…` (JPG q93; EXR gốc ngoài git `/var/tmp/cine-out/ncg/out/`). Thời gian = dựng thuần; mỗi lần chạy thêm ≈ 4–6 s nạp cảnh + ≈ 25–40 s khởi động Blender/BVH/ảnh nền.

**64 ↔ 256 spp:** với lấy mẫu thích ứng (ngưỡng 0,02) + OIDN, 256 spp chỉ tốn ×1,04–2,1 thời gian và ảnh **gần như trùng** (bão hoà/colorful/chi tiết lệch ≤ 0,002 / 0,1 / 0,7) — giống NC-CPU D4 (16 ↔ 128 spp). Khác biệt chỉ đáng kể ở khung nhiều thể tích (bờ + chiến sự: hạt khói mịn hơn).

## §4 Cú lặn 20 s — toàn bộ Cycles GPU

⟨LAN⟩

## §5 Đo

### 5.1 s/khung GPU ↔ CPU

| Việc | CPU (4 vCPU) | RTX 5090 | Hệ số |
|---|---|---|---|
| A (three.js + nướng, NC-CPU) | 4,28 s/khung chuỗi | — (A là llvmpipe/CPU; không chạy trên pod) | — |
| B nhanh NC-CPU 16 spp, 6 khung (cùng tệp) | 87–127 s (NC-CPU) · 101,7 s ("cang", đo lại 20/10) | 8,6–9,9 s | **×8,9–13,4 (trung vị ×11,2)** · "cang" ×11,7 |
| Cảnh mới 64 spp "cang" | 397,6 s | 11,7 s | **×34** |
| B cú lặn đêm NC-CPU (12 spp, 10 lửa + 10 khói) | 132 s | — | — |
| Cú lặn mới đêm (32 spp, 340 khói + 20 lửa thể tích, MB) | (không đo — ước > 30 phút/khung) | ⟨LAN-DEM⟩ | — |

Hệ số ×11 trên cảnh cũ (16 spp) thấp hơn ×34 trên cảnh mới vì 16 spp + OIDN là việc nhỏ (chi phí cố định: đồng bộ cảnh, OIDN 1080p, ghi EXR chiếm phần lớn 9 s trên GPU).

### 5.2 Màu / chi tiết (thước V6, vùng giữa 640×360)

| Bản | bão hoà TV | colorful TV | chi tiết TV | cháy sáng TV |
|---|---|---|---|---|
| V7B | 0,580 | 96,5 | 39,2 | 0,20 % |
| A (NC-CPU) | 0,466 | 75,2 | 35,9 | 0,05 % |
| B CPU (NC-CPU) | 0,296 | 57,5 | 31,5 | 0,01 % |
| B nguyên văn trên GPU | 0,298 | 58,2 | 31,4 | 0,00 % |
| **Cycles GPU 64** | **0,403** | 60,0 | 34,4 | 0,00 % (bờ + chiến sự 3,05 %) |
| Cycles GPU 256 | 0,403 | 60,0 | 34,5 | 0,00 % (3,03 %) |

Theo khung GPU 256: hero 0,184 và phố dày 0,341, cảng 0,380 dưới 0,40 (A: hero 0,247; V7B hero 0,329). JSON: `reports/nc-gpu/do/look-*.json`.

### 5.3 Chấm mù (`reports/nc-gpu/cham-mu/`, `score.json`, `blind_ncg.py`)

Giao thức NC-CPU: `claude -p` ghim claude-sonnet-5-5, chỉ Read, thư mục tạm chỉ 3 ảnh 640×360, 3 vai nguyên văn `blind_v2.py`, nhãn hoán vị (hạt 20261019), mô tả trung tính theo loại cảnh. 3 bản: **Cycles GPU 256** · **A (NC-CPU)** · **V7B**. **KHÔNG** đưa khung Omni (có vật bịa — V2V §0).

| Loại cảnh | GPU craft/realism/toy/hạng 1 | A | V7B |
|---|---|---|---|
| vây hãm | **5,67 / 5,67 / 5,33 / 3** | 4,67 / 4,67 / 5,33 / 0 | 4,00 / 3,67 / 6,33 / 0 |
| cảng | 5,00 / 6,00 / 3,00 / 0 | **6,33 / 6,33 / 4,33 / 3** | 4,33 / 4,00 / 5,33 / 0 |
| phố dày | 6,00 / 6,00 / 3,67 / 0 | **7,00 / 6,67 / 3,00 / 3** | 5,00 / 4,00 / 6,00 / 0 |
| hero 2026 | 5,00 / 5,00 / 5,00 / 0 | **6,67 / 5,67 / 4,67 / 3** | 6,67 / 5,67 / 5,00 / 0 |
| toàn cảnh | 5,67 / 5,67 / 4,33 / 0 | **7,00 / 6,33 / 4,00 / 3** | 4,33 / 3,33 / 6,67 / 0 |
| bờ + chiến sự | **6,67 / 6,00 / 3,67 / 3** | 5,67 / 5,00 / 5,33 / 0 | 5,67 / 4,67 / 5,67 / 0 |
| **TB** | 5,67 / 5,72 / **4,17** / 6 | **6,22 / 5,78** / 4,44 / **12** | 5,00 / 4,22 / 5,83 / 0 |

Lời giám khảo đáng giữ: vây hãm — "A [=GPU] has the most convincing atmosphere and ground texture and the densest, most natural vegetation"; bờ + chiến sự — "B [=GPU] has the most atmospheric depth, the least toy-like feel and the best ground texture, despite its overblown explosion glow"; cảng — "B [=GPU] is realistic but washed out and empty"; hero — GPU "hazy and washed out". So NC-CPU (bảng chấm khác, chỉ để tham khảo): B CPU craft 5,33 / realism 4,94 → GPU 5,67 / 5,72. Chi phí $1,036 (18 lượt).

## §6 So đích look Omni (V2V-D2: chỉ số đo, không chép hình)

Đo bằng `design/pt/gpu/do_look.py` (640×360; sương = trung vị "kênh tối" He 2009; phối cảnh khí quyển = bão hoà dải trên ÷ dải dưới). Omni: phần tư a/b/c của clip so `reports/nc-v2v/clip/so-c*.mp4` (480×270/phần tư, 5–6 khung/clip); ghép cặp theo loại cảnh gần nhất: c2 (hero 2026 ngày) ↔ hero; c3 (lướt thấp đoàn Rodney 1780) ↔ cảng; c4 (trại 1779) ↔ vây hãm. Số: `reports/nc-gpu/do/omni/look-c*.json`, `do/look-<bản>-<cảnh>.json`.

| Cặp | Chỉ số | Omni a / b / c | **GPU 256** | A | V7B | B CPU |
|---|---|---|---|---|---|---|
| hero ↔ c2 | bão hoà | 0,122 / 0,149 / 0,173 | **0,184** | 0,247 | 0,329 | 0,094 |
| | sương (kênh tối) | 0,200 / 0,208 / 0,224 | **0,224** | 0,184 | 0,071 | 0,341 |
| | xa/gần bão hoà | 0,21 / 0,36 / 0,63 | **0,50** | 1,42 | 1,40 | 2,08 |
| cảng ↔ c3 | bão hoà | 0,067 / 0,075 / 0,082 | 0,380 | 0,484 | 0,604 | 0,369 |
| | sương | 0,365 / 0,408 / 0,318 | 0,216 | 0,133 | 0,016 | 0,278 |
| | xa/gần | 0,50 / 0,28 / 0,31 | 0,16 | 0,40 | 0,40 | 0,15 |
| vây hãm ↔ c4 | bão hoà | 0,396 / 0,267 / 0,351 | **0,447** | 0,502 | 0,600 | 0,286 |
| | sương | 0,145 / 0,237 / 0,122 | **0,173** | 0,161 | 0,220 | 0,384 |
| | xa/gần | 0,57 / 0,64 / 0,48 | **0,64** | 0,71 | 0,96 | 0,70 |

Đọc: (1) GPU **gần đích Omni nhất** về sương và phối cảnh khí quyển ở hero và vây hãm (xa nhạt hơn gần, như ảnh chụp thật); A/V7B ở hero có bão hoà xa ≥ gần (ngược tự nhiên). (2) Omni **bão hoà thấp hơn ngưỡng 0,40** của BIBLE §11.4 ở 8/9 phần tư (0,07–0,40): đích look "thật" và luật bão hoà kênh đang kéo hai hướng — cần chủ dự án quyết (§11 NG-D4). (3) Cảng: Omni (c3, lướt thấp 1780) mù sương nặng (0,32–0,41) — khác góc máy, chỉ tham khảo.

## §7 Ước cả tập 745 s — 3 đường

Một tập = 745 s × 24 = **17 880 khung**. Đơn vị: RTX 5090 SECURE $1,19/h (giá đọc 20/10). Số s/khung đều là **số đo phiên này** (§3, §4); chỗ là ước có ghi (ước).

**Số đo dùng để ước (RTX 5090, 1080p, OIDN):**

| Loại khung | s/khung đo | Nguồn |
|---|---|---|
| Ngày trời trong, ít thể tích | **12,8** (64 spp + MB; 9,6–19,1) · 10,9–11,7 (khung cổng) | cú lặn 0–131; vây hãm, cảng, hero |
| Ngày có khói/lửa thể tích | **17,3** (13–28, thể tích biased) · 22–36 (khung cổng, thể tích không chệch) · 125 (bờ + chiến sự, 362 cụm, không chệch) | cú lặn 408–479; phố dày, toàn cảnh, chiến sự |
| Đêm có lửa + khói (pin nổi cháy) | **59,1** (32 spp; 26–89) · 108–126 (64 spp, 2 khung thử) | cú lặn 168–407 |
| Nạp cảnh mỗi đoạn (khởi động Blender + dựng cảnh + BVH + ảnh nền) | ≈ 40–60 s / đoạn 6–12 khung → **≈ 5 s/khung** | cú lặn 51 đoạn |
| 256 ↔ 64 spp | ×1,04–1,17 (trời trong) · ×2,1 (nhiều thể tích) | §3 |
| Chuẩn bị trên CPU cho đường Cycles | xuất hình học ≈ 35–50 s / mốc 6–12 khung + trạng thái ánh sáng/khói ≈ 3–6 s/khung → **≈ 9 s/khung CPU** | §4 |

**Phân bổ cảnh giả định (trung tâm):** 60 % ngày trời trong · 25 % ngày có khói/lửa · 15 % đêm có lửa (V7B: pin nổi cháy 27 s / 118 s = 23 % của bản thử). Sai số ±30 % theo phân bổ.

| Đường | Nội dung | GPU h/tập | Tiền GPU/tập | CPU h/tập | Phiên Claude* | Giờ đồng hồ** |
|---|---|---|---|---|---|---|
| **G0** | A (three.js + nướng) trên CPU cho ≈ 80 % (14 300 khung) + **cú lặn/cận đêm ≈ 20 % (3 580 khung) Cycles GPU** như cú lặn này | **≈ 44 h** (3 580 × (39,1 + 5) s; 39,1 = TB dựng GPU đo được của 429 khung cú lặn) | **≈ $52** | A ≈ 54 h + nướng ≈ 4 h (NC-CPU §6) + chuẩn bị ≈ 9 h | **≈ 9** (A 6 + nướng 1 + GPU 1–2, chạy song song) | **≈ 11–12 h** (4 pod) |
| **G1** | toàn tập Cycles GPU 64 spp (đêm 64 spp), thể tích biased, không MB | **≈ 177 h** (35,7 s/khung) — đêm 32 spp: ≈ 136 h | **≈ $211** (đêm 32 spp: ≈ $162) | ≈ 45 h chuẩn bị | **≈ 9** (GPU 4 × 4 pod + CPU 5) | ≈ 11 h nếu 16 pod cùng lúc; ≈ 44 h với 4 pod |
| **G2** | toàn tập 256 spp + motion blur + thể tích | **≈ 313 h** (63 s/khung; đêm 256 spp là (ước) ×2,1 của 64 spp) | **≈ $373** | ≈ 45 h | **≈ 12** (GPU 7 × 4 pod + CPU 5) | ≈ 20 h với 16 pod; ≈ 78 h với 4 pod |

\* Một phiên Claude điều phối được ≥ 3 pod song song (phiên này: 3 pod cùng lúc, 7 pod tổng) trong ≤ 12 h đồng hồ; một phiên CPU ≤ 10 h máy (như NC-CPU). Chưa tính phiên chuẩn bị đường ống (§8).
\** Giới hạn bởi kho GPU: RTX 5090 SECURE "Low", PRO 4500 không có máy lúc thử, COMMUNITY không có kho (§1). 16 pod cùng lúc **chưa được kiểm**.

So NC-CPU (cùng tập): G0 thay phần B CPU (≈ 100–132 h CPU, 10–14 phiên) bằng ≈ 44 h GPU ($52, 1–2 phiên); A giữ nguyên. Chi phí thật của cú lặn 20 s trong phiên này cao hơn số ước vì sự cố (§10): 10,2 h pod cho 480 khung, trong đó ≈ 2,6 h là lãng phí do lỗi.

## §8 Đường ống: công sức đưa G0/G1/G2 vào T3 và các tập sau

| Hạng mục | Hiện có (phiên này) | Việc còn | Công sức (phiên) | Dùng cho |
|---|---|---|---|---|
| Cầu nối đặc tả shot → máy/timeline Blender | `nc_topo.js --campath` (máy + năm + đêm + nắng mỗi khung từ chính k2v) → `gpu_blend.py --anim` khung hoá máy (motion blur); `gpu_export.js --lightfx` (nắng/trăng/trời/khói/lửa mỗi khung) | gói thành một lệnh theo `episode.yaml` (shot → đoạn → mốc xuất), kiểm khớp khung k2v ↔ Blender (chồng cạnh) | 1 | G0, G1, G2 |
| Vật có ngày (tl7: nhà mọc/sập, công sự theo năm, đất lấn biển) | xuất lại hình học theo **mốc 6–12 khung** (51 mốc cho 20 s; khử trùng lặp SHA: 2 569 MB → 116 MB) | G1/G2: ghi thuộc tính năm/thời lượng theo đỉnh (như `cityY` của export6) và tính trong Geometry Nodes theo khung → không cần xuất lại, không giật bậc | 2–3 | G1, G2 (G0 chỉ cú lặn: giữ cách mốc) |
| Đám đông / cờ / tàu động | tàu, người, cờ đứng yên trong mỗi mốc → **chuyển động theo bậc 0,25–0,5 s** (G0 cú lặn: tàu trôi chậm, P không thấy giật ở bản xem; chưa đo bằng máy) | xuất ma trận bản sao theo khung (tàu, người), cờ bay bằng Geometry Nodes, khói/lửa đã theo khung | 2 | G1, G2 (G0 nếu cú lặn có quân/tàu chạy nhanh) |
| Lưu cảnh / bộ nhớ đệm | tar cảnh 1,26 GB + tar cú lặn CAS 126 MB, tải mỗi pod 1–2 phút (pod chậm: 10 phút) | Network Volume RunPod (một lần tải, mọi pod gắn vào) hoặc ảnh pod có sẵn Blender + vân | 0,5 | mọi đường |
| Nướng (lightmap A) | NC-CPU `nc_blend.py nuong` trên CPU 25–32 phút/mốc | chạy trên GPU (×11–34) → ≈ 1–3 phút/mốc | 0,5 | G0 |
| Vận hành pod | `pod.py` (bật/tắt/sổ), `pod_srv.py`, `theo_pod.sh` (kéo dần, kiểm đủ dải trước khi tắt), `--needgpu`, xoá dữ liệu cụm khói (rò VRAM) | dựng lại khung thiếu tự động; giới hạn tiền theo phiên trong `pod.py` | 0,5 | mọi đường |
| Chỉnh màu | `nc_grade.js` của NC-CPU (k2v gradeHDR) | lô 24/6 khung làm Node thoát ngẫu nhiên → đang chạy 1 khung/lần (4–5 s); sửa cho lô | 0,3 | mọi đường |
| **Tổng** | | | **G0 ≈ 2–2,5 · G1/G2 ≈ 7–8** | |

**Rủi ro:**
1. **Lệch previs three.js ↔ final Cycles:** cùng hình học/máy, nhưng ánh sáng khác hẳn (GI, sương, ánh trời) → chấm mù khác nhau theo cảnh (GPU thắng vây hãm, chiến sự; thua cảng, phố, hero, toàn cảnh). Duyệt cổng phải xem bản Cycles, không duyệt previs.
2. **VRAM với 14 440 toà 2026:** khung hero 2026 (8,6 triệu tam giác + 0,46 triệu bụi) dùng ≈ 3,3 GB; cú lặn đêm (360 cụm thể tích) ≈ 8,8 GB → còn dư trên 32 GB. Hết VRAM duy nhất gặp là do **rò dữ liệu của tôi** (đã sửa), không do cảnh.
3. **Truyền tệp:** 18–22 MB/s ở 6/7 pod, **2,0 MB/s** ở 1 pod (1,26 GB mất 10,5 phút). Proxy HTTPS RunPod đôi khi trả rỗng (1 lần) → `pod.py` cần thử lại kiểm SHA.
4. **Hàng chờ GPU:** kho "Low"; 1/2 loại muốn dùng không có máy; chưa thử >3 pod cùng lúc.
5. **Rơi về CPU âm thầm:** sau lỗi CUDA, Blender trên pod 3 tiếp tục dựng bằng CPU (×13 chậm) mà không báo → nay `--needgpu` dừng ngay.
6. **Container phiên khởi động lại** (≈ 03:15): pod vẫn chạy phía RunPod → phải có sổ trạng thái ngoài bộ nhớ phiên (đã có: `/var/tmp/cine-out/ncg/pod*.json` + sổ git).

## §9 Chỉ số trong ±5 % quanh ngưỡng (luật cứng)

- **Bão hoà trung vị 6 khung Cycles GPU: 0,403** so ngưỡng ≥ 0,40 (BIBLE §11.4) → **+0,75 %, trong ±5 %**. Có được nhờ sửa ánh trời (khớp three.js), **không thêm phần tử nào**; nhưng đạt "sát nút" — chỉ 3/6 khung ≥ 0,40.
- **Bão hoà khung cảng (GPU): 0,380** → **−5,0 %**, ở mép ±5 %.
- Khác (ngoài ±5 %): vây hãm 0,447 (+11,8 %), toàn cảnh 0,427 (+6,8 %), phố dày 0,341 (−14,8 %), hero 0,184 (−54 %); toy_like TB GPU 4,17 (+4,25 % so mục tiêu ≤ 4 — **trong ±5 %**, chưa đạt); bản xem cú lặn ⟨MB⟩ so 5 MB; tiền GPU thật $10,28 so mốc theo dõi $12 (−14 %).
- Của Omni (để biết): bão hoà c4-a 0,396 (−1 % so 0,40).
- Không thêm phần tử nào để vượt ngưỡng: bụi ×3 là bản sao quanh bụi đã có nguồn lớp phủ (không rải chỗ mới); khói/lửa đúng cụm k2v.

## §10 Chi phí thật

⟨CHIPHI⟩

## §11 Quyết định đề xuất

⟨QD⟩

## §12 Việc chờ chủ dự án

⟨CHO⟩
