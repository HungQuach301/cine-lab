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

⟨UOC⟩

## §8 Đường ống: công sức đưa G0/G1/G2 vào T3 và các tập sau

⟨ONG⟩

## §9 Chỉ số trong ±5 % quanh ngưỡng (luật cứng)

⟨NGUONG⟩

## §10 Chi phí thật

⟨CHIPHI⟩

## §11 Quyết định đề xuất

⟨QD⟩

## §12 Việc chờ chủ dự án

⟨CHO⟩
