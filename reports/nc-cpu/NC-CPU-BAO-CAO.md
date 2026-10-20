Nhánh thật: `claude/clever-franklin-daez5k` (harness buộc tên này; lệnh yêu cầu `nc-cpu` — mọi commit được đẩy lên CẢ HAI nhánh, nội dung như nhau). Gốc: `origin/main` @3176ad1b. Không merge. Không sửa mã k2v cũ, `scripts/**`, `checks/`, `docs/`, `channel-*/`. V7B (`origin/ccr-ef2b66f0-9639kq`) chỉ ĐỌC (worktree tạm ngoài repo). Không đọc mã `checks/` ngoài `RULES-LL.md` (đúng lệnh).

# NC-CPU — BÁO CÁO: đo thật "bước nhảy chất lượng" chỉ bằng CPU (chưa đổi đường ống sản xuất)

## §0 Tóm tắt

| Việc | Kết quả |
|---|---|
| A. three.js + NƯỚNG Cycles | **Khả thi, thắng rõ nhất.** Nướng 1 lần/mốc: 1782 = **1 481 s** (4 lượt: trời, nảy nắng, nắng chuẩn hoá, lửa pin nổi), 2026 = **1 907 s** (3 lượt, máy có tải song song), hộp 4 × 6,5 km, 3 m/texel. Dựng: khung đơn 1080p spp 4 **25,7–29,3 s** (V7B cùng cách đo 22,7 s, ≈ +20 %); khung chuỗi spp 2 **4,4–5,0 s** (cú lặn, có tải). Vân: 18 tấm CC0 = 119 MB đĩa, 201 MB bộ nhớ đồ hoạ; lightmap 4,6–4,9 MB/mốc. |
| B. Cycles CPU trực tiếp | **Khả thi.** Cảnh Blender đứng riêng (xuất từ k2v + vật liệu riêng). 1080p: nhanh 16 spp + OIDN **87–127 s/khung**; đẹp 128 spp **325–534 s/khung** (2 khung; khác bản 16 spp chỉ 1,8–2,1/255 TB); cú lặn đêm (12 spp, 10 đám cháy + khói thể tích) **≈ 132 s/khung**. |
| C. Eevee trên llvmpipe | **Chạy được** (cảnh báo nguyên văn: `EGL Error (0x3009): EGL_BAD_MATCH: Arguments are inconsistent (for example, a valid context requires buffers not supplied by a valid surface).` — vẫn ra ảnh đúng). 1080p 32 mẫu **106–215 s/khung** (6 khung: 173 · 118 · 215 · 106 · 213 · 115 s; đo lại máy rảnh 2 khung: 110 · 202 s) — **chậm hơn Cycles nhanh** vì OpenGL phần mềm. |
| 6 khung cổng × 3 cách | `reports/nc-cpu/khung/{A,B-nhanh,B-dep,C}/cong-*.jpg` (+ `khung/V7B/` bản sao để so). Tờ so: `reports/nc-cpu/to-so-khung.jpg`. |
| Cú lặn 20 s | `reports/nc-cpu/lan/nc-lan-xem.mp4` (960×540, **4,39 MB**, SHA-256 `b857ef35…f091f`); master 1080p ngoài git `/var/tmp/cine-out/nc/nc-lan-1080p-master.mp4` (158,4 MB, SHA-256 `e76d565e417103783aa2ac320cc2cc90ecde50df7c82972fa9dbfc96691316e6`). A cho đoạn cao (khung 0–215, 313–479), **B (Cycles) cho đoạn lướt mặt nước qua pin nổi cháy đêm 13→14/9/1782** (khung 216–312), hoà chéo 0,5 s ở hai mối. |
| Chấm mù (640×360, 3 vai × 6 loại cảnh, Sonnet 5.5) | **A hạng nhất 11/18**, V7B 3, B 2, C 2. Craft TB: A **6,28** · C 5,61 · B 5,33 · V7B 5,28. Độ thật bề mặt: A **5,67** · C 5,17 · B 4,94 · V7B 4,50. |
| Ước cả tập 745 s | A cho đoạn cao (≈ 80 %) ≈ **54 h** CPU (V7B ≈ 50 h × 1,36 × 0,8) + nướng ≈ **4 h** một lần + B cho cú lặn (20 % = 3 600 khung × 132 s) ≈ **132 h** → **≈ 190 h ≈ 21 phiên × ≤ 10 h** (A 6 · nướng 1 · B 14). Chỉ A cho cả tập: ≈ 72 h (8 phiên). Chi tiết §6. |
| Chi phí | Claude **$1,10** (mốc $8), OpenAI **$0** (không ảnh AI), ElevenLabs 0, YouTube 0. Giờ máy CPU ≈ **7,2 h** (mốc 10 h). |
| Đề xuất | **NC-D1: đưa A vào sản xuất T3** (nâng cấp + nướng theo mốc), **B chỉ cho cú lặn/cận cảnh đêm**, **bỏ C**. Chi tiết §10. |

Xem nhanh: `reports/nc-cpu/to-so-khung.jpg` (hàng = 6 loại cảnh; cột = V7B · A · B nhanh · C), cú lặn `reports/nc-cpu/lan/nc-lan-xem.mp4`.

## §1 Chuẩn bị, tái tạo V7B, cách đo

- **Môi trường:** 4 vCPU, 15 GB RAM, không GPU; Blender bpy 5.2.2 LTS; Chromium + Mesa llvmpipe (LLVM 20); three.js 0.180. `verify.sh`: 5 mục thiếu (OpenEXR, tifffile/pyshp, node_modules three.js ×2) → cài trong phiên; Freesound 403 (tuỳ chọn, không dùng).
- **Bộ đệm cảnh k2tl** dựng lại từ nguồn trong container mới (2 phút; SHA nguồn khớp sổ V5b-1). Khung V7B dựng lại khớp PNG cổng: lệch TB **4,7/255** (JPEG + hạt).
- **6 điểm máy cổng** = đúng khung V7B §7: vây hãm (C1-a 21,8 s), cảng (C4 3,5 s), phố dày (C3 11,5 s), hero 2026 (H3 10,4 s), toàn cảnh (C5 2,6 s), bờ + chiến sự (H2 13,3 s). Mốc của lệnh: **13/9/1782** (nướng `b1782`, cũng dùng cho mọi khung vây hãm 1779–1782 — xem giới hạn §8) và **2026 ngày** (nướng `b2026`).
- **Đo màu** theo V6/V5b-1b (`scripts/k2tl/measure_look.py`: 640×360 INTER_AREA, vùng giữa 15–85 %) — `reports/nc-cpu/do/look-*.json`.
- **s/khung**: đồng hồ thật. "Khung đơn" = một khung mỗi lần chạy (gồm biên dịch shader + dựng bóng lần đầu; nạp cảnh tính riêng 15–17 s). "Khung chuỗi" = TB trên chuỗi liên tục. Lượt có tải song song ghi rõ.

## §2 Ba cách — khả thi, s/khung, giờ nướng

### 2.1 Cách A — three.js + NƯỚNG (mã mới `design/k2v/tl/nc/`, `design/pt/cpu/`)
Bọc cảnh `t3tl` của V7B (mọi nội dung, cờ, tàu, người, khói, máy, thời gian giữ nguyên), rồi nâng **độ thật bề mặt** bằng vá vật liệu nối tiếp (không sửa mã cũ):
1. **Nền: vân ảnh chụp CC0** (Poly Haven, 18 tấm 2k → mảng vân 1024² × 18 lớp, có mipmap) theo **13 lớp phủ** (`cls.png`): cát bãi, cỏ khô/garrigue, maquis, đá vôi + vách, ruộng, nhựa, nền đất nện 1782 / lát 2026, sân cỏ, bê tông cảng, đất trống. Hai tỉ lệ không thông ước + một tỉ lệ lớn, chống lặp ô kiểu Quilez (2 mẫu lệch theo nhiễu), pháp tuyến từ vân (vi gồ ghề bắt nắng). Giữ bảng màu thủ tục của k2v; vân mang cấu trúc + 15–35 % sắc độ.
2. **Bụi cây instanced:** 309 620 bụi (2026) / ≈ 140 000 (1782, mật độ × 0,45 — đồn trú chặt củi, bậc 5) rải theo lớp phủ TỰ NHIÊN, ẩn ở nền đô thị theo năm (cùng logic shader địa hình), ở dải trại (bọc `hideWhere` của t3tl), đổ bóng; LOD 20 mặt / 8 mặt / ẩn > 3,6 km.
3. **Nước mới:** sóng 5 hướng (9–70 m) + nhiễu, vệt gió 1 km, màu sâu bớt bão hoà, dải nông + bọt sát bờ theo khoảng cách bờ CỦA NĂM (đất lấn 1941), giữ phản chiếu phẳng V6.
4. **Sương khí quyển** e^(−σd), σ = 1/16 km, màu chân trời sáng ngả xám-lam (thay FogExp2 gần như không có tác dụng).
5. **Nhà / công sự:** vữa CC0 theo toạ độ tường (u, cao), vệt bẩn chân tường, ngói CC0 trên mái dốc, đá CC0 tam phẳng cho công sự.
6. **Ánh sáng NƯỚNG (Cycles CPU, một lần/mốc):** cảnh xuất từ k2v (`nc_export.js`, 7,3–8,6 triệu tam giác gồm bản sao) → Blender (`nc_blend.py nuong`): địa hình UV phẳng, nướng **R = bức xạ trời có che khuất + nảy** (÷ mặt phẳng trống), **G = nảy của nắng**, **B = lửa pin nổi** (10 đèn điểm), **A = cao độ** → `bake.png`. Shader three.js: ánh trời × R, + albedo × màu nắng × G, + albedo × lửa × B (theo thời gian cháy); tường nhà lấy R tại phố trước mặt tiền, tắt dần theo độ cao trên nền (AO hẻm phố).

| Đo (A) | Số |
|---|---|
| Nướng 1782 (`b1782`, 1333 × 2167 texel, 3 m, 24 spp, 4 lượt) | trời 481 s · nảy 267 s · nắng chuẩn hoá 327 s · lửa 395 s · **tổng 1 481 s** (có tải: cú lặn A chạy song song) |
| Nướng 2026 (`b2026`, cùng hộp, 3 lượt) | 745 + 569 + 580 s · **tổng 1 907 s** (có tải nặng hơn) |
| Thử đầu (hộp phố 2 × 3 km, 2 m, 32 spp, 3 lượt) | 905 s; lỗi đường lưới 1 km do "váy" ô địa hình chồng mép → đã sửa (cắt váy trước khi nướng) |
| Albedo nền nhìn thẳng xuống cho Blender (`nc_topo.js`, 1 m + 4 m) | 4–5 s / mốc (sau nạp cảnh) |
| Dựng khung đơn 1080p spp 4 (6 khung cổng, máy rảnh) | **25,7 · 27,1 · 27,5 · 26,4 · 27,7 · 29,3 s** (V7B cùng cách đo: 22,7 s) |
| Dựng khung chuỗi 1080p spp 2 (cú lặn, đang có tải nướng) | **4,4 s** (khung 0–227) · **5,0 s** (khung 336–479) |
| Dung lượng | vân 119 MB đĩa / 201 MB bộ nhớ GL; lightmap PNG 4,6 / 4,9 MB; albedo nền 52 MB (cho B/C) |
| So steady-state cùng shot (t3tl ↔ ncA, máy rảnh) | **t3tl (V7B) 3,16 s/khung · ncA 4,28 s/khung → +36 %** (C5, 48 khung chuỗi, 1080p spp 2, máy rảnh; nạp cảnh 9,5 s → 14,2 s; RAM 2,6 → 3,4 GB). Khung đêm cú lặn (khung 300–335, máy rảnh): 2,94 s |

### 2.2 Cách B — Cycles CPU trực tiếp
Cảnh Blender ĐỨNG RIÊNG: hình học xuất từ k2v của đúng khung (`nc_export.js`), vật liệu riêng: nền = albedo nhìn thẳng xuống của chính cảnh A (cùng vân CC0, đường, vườn), nhà = màu đỉnh k2v × vữa + cửa sổ thủ tục + ngói, công sự = đá CC0, bụi/cây = màu bản sao, nước Principled (Fresnel, sóng bump động), trời gradient như k2v (tia máy thấy trời sáng, tia khuếch tán nhận ánh trời k2v), sương e^(−σd) trong MỌI vật liệu; ảnh HDR được **chỉnh màu bằng chính đường ống k2v** (`gradeHDR`: ACES + LUT A + V6 grade + hạt) để cùng tông với A.

| Đo (B, 1080p, 4 luồng) | Số |
|---|---|
| Nhanh: 16 spp + OIDN, adaptive 0,02, nảy 4/3/2 — 6 khung cổng | **88 · 87 · 99 · 109 · 106 · 127 s** (+ nạp 5–10 s, chỉnh màu 4,4 s) |
| Đẹp: 128 spp + OIDN | **325 s** (cảng) · **534 s** (toàn cảnh) — chỉ 2 khung (cắt bớt để giữ mốc giờ máy); số đo màu gần như TRÙNG bản 16 spp (bão hoà 0,369 / 0,306 = bằng hệt) → OIDN ở 16 spp đã đủ cho cảnh trên cao ban ngày; lệch điểm ảnh TB so 16 spp chỉ **1,8 / 2,1 trên 255** |
| Cú lặn đêm: 12 spp + OIDN, dữ liệu bền, 10 đám cháy (đèn + ngọn lửa phát xạ) + 10 cột khói THỂ TÍCH | **132 s/khung TB** (119–147 s, 84 khung sạch 228–312; khung 216–227 có tải chồng 125–220 s) |
| Ước "cú lặn" cả tập: 20 % × 745 s ≈ 150 s × 24 = 3 600 khung | 3 600 × 132 s ≈ **132 h CPU** → **14 phiên × ≤ 10 h** (4 vCPU/phiên); ngày không khói thể tích ≈ 100 s/khung → 100 h, 10 phiên |

### 2.3 Cách C — Eevee trên OpenGL phần mềm
- **Chạy được** trong container (Blender 5.2 Eevee qua EGL → Mesa llvmpipe). Lỗi in ra (không chặn): `EGL Error (0x3009): EGL_BAD_MATCH: Arguments are inconsistent (for example, a valid context requires buffers not supplied by a valid surface).` ×3. Cảnh rỗng 640×360: 34 s (biên dịch shader).
- Cùng cảnh, cùng vật liệu, cùng máy với B; 32 mẫu TAA, bóng, raytracing màn hình.
- 1080p: **106–215 s/khung** (6 khung: 173 · 118 · 215 · 106 · 213 · 115 s; đo lại máy rảnh 2 khung: 110 · 202 s). **Chậm hơn Cycles 16 spp** trên máy này: Eevee là trình dựng GPU, llvmpipe giả lập GPU bằng CPU nên không có lợi thế; ảnh gần như trùng B (cùng ánh sáng/sương) nhưng thiếu GI thật.

## §3 Sáu khung cổng (1920 × 1080)

| Cảnh | V7B | A | B nhanh | B đẹp | C |
|---|---|---|---|---|---|
| vây hãm | `khung/V7B/cong-vay-ham.jpg` | `khung/A/cong-vay-ham.jpg` | `khung/B-nhanh/…` | `khung/B-dep/…` | `khung/C/…` |
| cảng · phố dày · hero · toàn cảnh · bờ + chiến sự | cùng mẫu tên `cong-<loại>.jpg` | | | | |

(JPG q92–95 để giữ repo nhỏ; PNG/EXR gốc ngoài git `/var/tmp/cine-out/nc/gate-*`.)

**Nhìn bằng mắt (P tự soi, trước chấm mù):**
- **A**: đất hết "phẳng đồng màu" (cấu trúc cỏ khô/garrigue/đá, bụi rải bắt nắng), nước lam sẫm có vệt gió và dải bọt bờ, sương làm núi xa lùi về sau; phố 1782 có nền đất nện + vữa; AO hẻm từ nướng. Còn: lặp ô nhẹ trên nước tầm trung (cảng), đá vôi đỉnh Rock bạc màu, cận cảnh vẫn lộ khối (nhà không có chi tiết hình học mới).
- **B/C**: ánh sáng tự nhiên nhất (GI thật, bóng mềm, chiều sâu) — thắng ở **cảng** (giám khảo: "real atmospheric aerial shot"). Thua ở cảnh khác vì (1) **nhạt** — sương dày + LUT, bão hoà 0,29–0,30 < 0,40; (2) nền gần **mờ** (albedo nền 4 m/px ngoài hộp 1 m); (3) **mái bằng đen** rải rác (lỗi vật liệu chưa tìm ra gốc); (4) khung ngày **không có khói/đèn lửa** (sprite k2v không xuất sang Blender); (5) lều trại xám (không có màu đỉnh).

## §4 Cú lặn 20 s

| Mục | Giá trị |
|---|---|
| Nội dung | 0–5,5 s: máy cao (≈ 500 m) trên vịnh, **timelapse 1779 → 13/9/1782** (trại, công sự, phố mọc theo năm, giờ mặt trời cố định); 5,5–9 s: chiều 13/9 → đêm, máy hạ xuống, 10 pin nổi vào vị trí và **bốc cháy**; **9–13 s: lướt 6–17 m trên mặt nước dọc hàng pin nổi cháy** (phản chiếu lửa dài trên sóng, khói thể tích, Line Wall + Rock sau lưng); 13–17 s: ngược lên 380 m, quay về vịnh; 17–20 s: thời gian chạy tiếp 14/9 02:30 → 11:00 (bình minh, khói) |
| Đường máy | `design/pt/cpu/dive-opt.json` (cùng đặc tả cho A và B; B đọc máy MỖI khung từ k2v: `nc_topo.js --campath`) |
| Cách dựng | A: 395 khung (1080p spp 2, có nướng `b1782` + lửa nướng); B: 97 khung 216–312 (1080p, 12 spp + OIDN, dữ liệu bền, 10 đám cháy = đèn điểm + 3 ngọn lửa phát xạ/pin, 10 cột khói thể tích nhiễu 4D), chỉnh màu bằng `gradeHDR` của k2v; hoà chéo smoothstep 216–227 và 300–312 (`reports/nc-cpu/lan/nguon-khung.json`) |
| s/khung | A: 4,4 s (0–227, có tải) · 5,0 s (336–479, có tải) · 2,9 s (300–335, rảnh) · **B: 132 s TB (119–147 s, 84 khung sạch)** |
| Giờ máy cú lặn | A ≈ 0,6 h · B ≈ 3,6 h |
| Tờ khung | `reports/nc-cpu/lan/to-lan.jpg` (khung 0, 96, 168, 210, 222, 240, 264, 290, 306, 330, 400, 470) |

Nhận xét thẳng: đoạn B là đoạn "điện ảnh" nhất của phiên — ánh lửa phản chiếu thành cột trên sóng, Line Wall và sườn Rock được lửa hắt sáng, khói đen che sao. Điểm yếu: ngọn lửa là khối cầu phát xạ (đọc như "đèn"), khói thể tích 12 spp còn hạt/vệt OIDN, mối nối A↔B lộ do nước A sáng lam hơn nước B (tông chung nhờ LUT k2v nhưng phản chiếu khác). Ban đầu đêm B quá tối so với A (trời đêm 0,01) — đã sửa bằng trời đêm của k2v (`water.js skyCol`, uNight = 1). Cú lặn rút từ 216–348 xuống 216–312 để giữ giờ máy (24 khung cuối đoạn lướt dùng A).

## §5 Đo + so

### 5.1 Màu / chi tiết (thước V6, vùng giữa 640×360)
| Bản | bão hoà TV | colorful TV | chi tiết TV | cháy sáng |
|---|---|---|---|---|
| V7B | 0,580 | 96,5 | 39,2 | 0,20 % |
| **A** | **0,466** | 75,2 | 35,9 | 0,05 % |
| B nhanh | 0,296 | 57,5 | 31,5 | 0,01 % |
| C | 0,286 | 56,3 | 30,4 | 0,01 % |

Đọc: A **giảm** bão hoà/colorful so V7B (nước bớt "lam nhựa", có sương) nhưng vẫn ≥ 0,40 (BIBLE §11.4) ở trung vị; theo khung A: hero 0,247 và bờ + chiến sự 0,361 dưới 0,40 (V7B: 0,329 / 0,388). Thước "chi tiết" (|Laplace|) **không** đo được độ thật: V7B cao vì đốm sóng lam bão hoà, chấm mù xếp ngược lại → không dùng thước này để chọn.

### 5.2 Chấm mù (`reports/nc-cpu/cham-mu/`, `score.json`)
Giao thức như V6: `claude -p` ghim claude-sonnet-5-5, chỉ công cụ Read, thư mục tạm chỉ có 4 ảnh 640×360, 3 vai nguyên văn `blind_v2.py`, nhãn A–D hoán vị (hạt 20261019), mô tả trung tính theo loại cảnh; thêm thang **realism** (độ thật bề mặt). Không khung đối thủ (điều phối tự so trong chat).

| Loại cảnh | V7B craft/realism/hạng 1 | **A** | B nhanh | C |
|---|---|---|---|---|
| vây hãm | 4,33 / 4,33 / 1 | **5,0 / 5,0 / 2** | 4,33 / 4,33 / 0 | 4,33 / 4,33 / 0 |
| cảng | 5,0 / 4,33 / 0 | 6,0 / 5,33 / 0 | **7,33 / 7,33 / 2** | 7,0 / 7,33 / 1 |
| phố dày | 5,0 / 4,0 / 0 | **7,0 / 7,0 / 3** | 6,0 / 5,0 / 0 | 6,0 / 5,0 / 0 |
| hero 2026 | 7,0 / 6,0 / 0 | **7,0 / 6,0 / 3** | 5,0 / 4,0 / 0 | 5,0 / 4,0 / 0 |
| toàn cảnh | 4,0 / 3,0 / 0 | **6,67 / 5,67 / 2** | 4,33 / 5,0 / 0 | 6,33 / 6,33 / 1 |
| bờ + chiến sự | **6,33 / 5,33 / 2** | 6,0 / 5,0 / 1 | 5,0 / 4,0 / 0 | 5,0 / 4,0 / 0 |
| **TB** | 5,28 / 4,50 / **3** | **6,28 / 5,67 / 11** | 5,33 / 4,94 / 2 | 5,61 / 5,17 / 2 |

toy_like TB: V7B 5,56 · **A 4,61** · B 5,22 · C 5,11 (mục tiêu ≤ 4 chưa đạt). Lời giám khảo đáng giữ: phố dày — "A is the only frame where water, land and atmosphere look like a real place"; cảng — "B and C look like real atmospheric aerial shots… A and D have cartoon-saturated water and pink ship halos"; bờ + chiến sự — A thua V7B nhẹ (khói/lửa trận đánh giống nhau, nền A "speckled").

B đẹp (128 spp) không vào chấm mù: chỉ 2 khung và ảnh gần như trùng B nhanh (§2.2).

## §6 Ước cả tập 745 s

Phân bổ theo lệnh: timelapse cao bằng A, cú lặn ≈ 20 % (≈ 150 s) bằng B. Một phiên = 4 vCPU, ≤ 10 h.

| Phần | Khung | s/khung (nguồn) | Giờ CPU | Phiên |
|---|---|---|---|---|
| A — 595 s cao | 14 280 | V7B ước cả tập ≈ 50 h (V7B §10) × **1,36** (đo §2.1) × 0,8 | **≈ 54 h** (sàn theo chuỗi C5 đo được: 14 280 × 4,28 s = 17 h) | 6 |
| Nướng (≈ 8 lightmap: 1704 · 1779–81 nguyên · 1781–83 phế tích · 13/9/1782 đêm có lửa · 1943 · 1987 · 2026 ngày · 2026 đêm) | — | 0,4–0,5 h/lightmap (đo) | **≈ 4 h** (một lần, dùng lại cho mọi shot cùng mốc) | 1 |
| B — 150 s cú lặn | 3 600 | 132 s (đêm, lửa + khói thể tích) · ≈ 100 s (ngày, 16 spp) | **≈ 100–132 h** | 10–14 |
| **Tổng** | | | **≈ 160–190 h** | **17–21 phiên song song** |

- So V7B (≈ 50 h, 6 gói × ≤ 8,5 h): **A thay toàn bộ** ≈ 68–72 h (≈ 8 phiên) — **+40 %** giờ máy cho bước nhảy chấm mù 3 → 11/18 hạng nhất.
- **B là phần đắt**: 1 s phim B ≈ 0,9 h CPU (đêm). Nếu cú lặn chỉ 10 % (75 s) → B ≈ 55–64 h.
- Sai số ±25 % (A: chỉ đo 1 shot chuỗi; B: chỉ đo 1 cú lặn đêm + 6 khung ngày đơn).

## §7 Thứ CPU KHÔNG làm được (so GPU) và cách thay

| Hạng mục | GPU làm | Trên CPU đo được | Cách thay đã thử / đề xuất |
|---|---|---|---|
| Ánh sáng toàn cục mọi khung | path tracing thời gian thực/gần thực | Cycles 87–147 s/khung → chỉ cho ≤ 20 % thời lượng | **Nướng** GI tĩnh theo mốc (A, 25–32 phút/mốc); vật động (người, tàu, khói) vẫn đèn k2v |
| Khói thể tích ĐỘNG | volumetrics thời gian thực | Cycles thể tích được (cú lặn) nhưng **+30–40 %** giờ khung; three.js không có | A: khói giả thể tích V6 (bảng instanced) — giữ; B: thể tích chỉ ở cú lặn; đề xuất sprite khói **nướng sẵn** (chuỗi ảnh Cycles RGBA của một cột khói, lặp) cho A |
| Phản chiếu thật (vật trên nước, ánh lửa) | SSR/RT reflections | A: gương phẳng nửa phân giải (V6) đủ cho nước phẳng; không phản chiếu ánh sáng lửa thật | B cho cận cảnh đêm có lửa (phản chiếu cột lửa dài trên sóng — chỉ B làm được); A: quầng lửa sprite + lightmap lửa nướng |
| Bóng mềm theo kích thước nguồn | PCSS/RT | A: PCF + bóng nướng chỉ ở NỀN (tường dùng ánh trời nướng) | nướng thêm bóng nắng vào lightmap khi nắng cố định (timelapse giữ giờ mặt trời) |
| GI trên NHÀ / mặt đứng | probe/RT | lightmap chỉ phủ địa hình (UV phẳng); nhà lấy R của phố trước mặt tiền | nướng UV nhà (atlas) — tốn công, để sau |
| Eevee | nhanh trên GPU | **chậm hơn Cycles** trên llvmpipe | bỏ C |
| Độ phân giải chi tiết cận | vân 8k, tessellation | vân 1–2k, albedo nền 1 m/px | tăng ô albedo 0,5 m chỉ quanh điểm máy cận |

## §8 Giới hạn / rủi ro đã thấy

- **Một lightmap cho 1779–1782:** `b1782` chụp phố ở trạng thái 13/9/1782 (đã sập theo "THE RUINS"); khung 1779–1781 (vây hãm, cảng, phố dày, toàn cảnh) dùng chung → AO dưới khối nhà đã sập hơi sai. Sản xuất: nướng theo **mốc + trạng thái phố** (trước/sau 12/4/1781).
- **Nảy nắng nướng theo MỘT hướng nắng**; khung khác giờ nhân cos(lệch hướng) — gần đúng. Timelapse giữ giờ mặt trời cố định (V7B-D2) nên đúng cho phần lớn khung.
- **Mật độ bụi 1782 × 0,45 là bậc 5** (chưa có nguồn mật độ thảm thực vật 1782); cần chủ dự án duyệt hoặc tra Drinkwater/tranh thời đó.
- **Lọc dị hướng trên sampler2DArray ở llvmpipe làm hỏng điểm ảnh** (khối đen NaN dọc mép lớp phủ) → phải tắt (aniso 1). Bài học mới.
- B/C: mái bằng đen, lều xám, khung ngày thiếu khói (§3) — lỗi xuất/vật liệu, sửa được, không phải giới hạn CPU.
- Số A khung đơn gồm khởi động; số A khung chuỗi đo khi có tải → cần đo lại khi đưa vào sản xuất (**t3tl (V7B) 3,16 s/khung · ncA 4,28 s/khung → +36 %** (C5, 48 khung chuỗi, 1080p spp 2, máy rảnh; nạp cảnh 9,5 s → 14,2 s; RAM 2,6 → 3,4 GB). Khung đêm cú lặn (khung 300–335, máy rảnh): 2,94 s).

## §9 Đường ống: đưa A (+ B cho cú lặn) vào T3 và các tập sau

| Bước | Công sức ước (phiên) | Tái dùng |
|---|---|---|
| 1. Đóng gói A: `nc/up.js` thành tuỳ chọn cảnh (`opt.nc`), test bit-giống khi tắt, golden mới khi bật | 1 phiên | mọi cảnh tl |
| 2. Thư viện vật liệu: 18 vân CC0 + bảng lớp phủ → vân (đã có), thêm 0,5 m quanh máy cận | 0,5 phiên | **mọi tập** (nền Địa Trung Hải; tập vùng khác đổi 4–6 vân) |
| 3. Bụi/cây theo lớp phủ + mật độ theo thời kỳ (cần nguồn) | 0,5 phiên + tra nguồn | mọi tập có `cls.png` |
| 4. Nướng theo mốc: script `nc_blend.py nuong` (đã có) chạy cho mỗi (mốc × trạng thái × giờ nắng) — T3 ≈ 8–10 lightmap × 0,5 h | 0,5 phiên + 5 h máy | lightmap giữ trong ổ cache theo SHA cảnh |
| 5. B cho cú lặn: cảnh Blender đứng riêng + chỉnh màu k2v (đã có); sửa mái đen, màu lều, xuất sprite khói/lửa | 1 phiên | mọi tập |
| 6. Ghép A↔B ở mối nối (hoà chéo ≤ 0,5 s, cùng LUT) | đã có (`nc_ghep_lan.py`) | — |
| **Tổng** | **≈ 3,5 phiên** + giờ máy §6 | |

Rủi ro: (1) A chậm hơn V7B ≈ 20 % khung đơn (**t3tl (V7B) 3,16 s/khung · ncA 4,28 s/khung → +36 %** (C5, 48 khung chuỗi, 1080p spp 2, máy rảnh; nạp cảnh 9,5 s → 14,2 s; RAM 2,6 → 3,4 GB). Khung đêm cú lặn (khung 300–335, máy rảnh): 2,94 s cho chuỗi) → +giờ máy; (2) lightmap sai khi phố đổi trong shot (mọc/sập) — chỉ nướng phần tĩnh, AO động vẫn SSAO; (3) cú lặn B nặng: 14 phiên song song cho 150 s.

## §10 Quyết định đề xuất

| # | Đề xuất | Ưu | Nhược | Tác động | Rủi ro |
|---|---|---|---|---|---|
| NC-D1 | **Đưa cách A vào sản xuất T3**: vân CC0 theo lớp phủ + bụi cây + nước mới + sương e^(−σd) + nướng Cycles theo mốc | Chấm mù: hạng nhất **11/18** (V7B 3), craft +1,0, độ thật +1,2; chỉ CPU; dùng lại mọi tập | +36 % s/khung chuỗi, +5 h máy/tập để nướng; bão hoà giảm (0,58 → 0,47, vẫn ≥ 0,40) | mọi shot tl T3 | lặp vân nước tầm trung; lightmap sai khi phố đổi trong shot → nướng theo trạng thái |
| NC-D2 | **B (Cycles CPU) CHỈ cho cú lặn/cận cảnh đêm có lửa** (≤ 10–20 % thời lượng), cảnh Blender đứng riêng + chỉnh màu k2v, ghép hoà chéo 0,5 s | ánh lửa phản chiếu, khói thể tích, GI thật — thứ A không làm được | 1 s phim ≈ 0,9 h CPU; 14 phiên cho 150 s | cú lặn T3 | mối nối lộ (nước A sáng hơn) → cần khớp nước A↔B; khung ngày B bị nhạt/mờ nếu dùng ngoài cú lặn |
| NC-D3 | **Bỏ C (Eevee/llvmpipe)** | — | chậm hơn Cycles 16 spp (106–215 s so 87–127 s), thiếu GI | — | — |
| NC-D4 | B nhanh **16 spp + OIDN** là đủ cho cảnh cao ban ngày (128 spp không khác về số đo) | rẻ 3–5× so 128 spp | — | giờ máy B | cảnh đêm nhiều thể tích cần đo riêng |
| NC-D5 | Mật độ bụi trước 1900 = 0,45 × hiện nay (**bậc 5**) — chủ dự án duyệt hoặc giao tra nguồn thảm thực vật 1782 | khớp bản khắc (sườn thưa) | chưa có nguồn số | vây hãm, toàn cảnh | sai thời đại nếu thực tế trọc hơn/rậm hơn |
| NC-D6 | Bài học kỹ thuật: tắt lọc dị hướng cho sampler2DArray trên llvmpipe; cắt "váy" ô địa hình trước khi nướng; dừng tiến trình theo PID (một `nohup` cũ chạy chồng lượt) | tránh 3 lỗi đã gặp | — | BAI-HOC | — |

## §11 Chi phí thật

| Khoản | Mốc / chặn | Thật |
|---|---|---|
| Claude API (chấm mù 18 lượt `claude -p`, Sonnet 5.5) | $8 / $25 | **$1,10** (`reports/nc-cpu/cham-mu/cost.jsonl`) |
| OpenAI | $3 | **$0** (không ảnh AI; vân đất là ảnh chụp CC0 → K-LAI không áp) |
| ElevenLabs / YouTube | 0 | 0 / 0 |
| GPU thuê | không | không |
| Giờ máy CPU (4 vCPU, đồng hồ máy bận) | mốc 10 h | **≈ 7,2 h**: bộ đệm 0,05 · thử/soi 0,7 · nướng 0,25 + 0,41 + 0,53 · xuất/albedo 0,2 · A cổng 0,1 · cú lặn A 0,6 · B nhanh 0,2 · C 0,4 (có chồng) · cú lặn B 3,6 · B đẹp 0,25 · đo lại 0,2 (có chồng lặp nên tổng < tổng mục) |
| Lưu trữ ngoài git | — | `/var/tmp/cine-out/nc/` ≈ 2 GB (vân, xuất cảnh, EXR, master cú lặn) |

## §12 Chỉ số trong ±5 % quanh ngưỡng (luật cứng)

- Không chỉ số nào của A/B/C nằm trong ±5 % quanh ngưỡng đã định. Gần nhất: bão hoà khung "bờ + chiến sự" A 0,361 (−9,8 % so 0,40), toy_like TB A 4,61 (+15 % so ≤ 4), bản xem cú lặn 4,39 MB (−12 % so 5 MB).
- Của V7B (để biết): bão hoà khung "bờ + chiến sự" 0,388 (**−3 %** so 0,40).
- Không thêm phần tử nào để vượt ngưỡng (bụi cây rải theo lớp phủ có nguồn, mật độ 1782 bậc 5 — §10 NC-D5).

## §13 Việc chờ chủ dự án

1. **Xem** `reports/nc-cpu/to-so-khung.jpg` (V7B · A · B · C) và cú lặn `reports/nc-cpu/lan/nc-lan-xem.mp4` (+ tờ `lan/to-lan.jpg`). Điều phối so đối thủ trong chat theo cổng §11.4 (6 khung A ở `khung/A/`).
2. **Quyết NC-D1…D6**, nhất là D1 (A vào sản xuất T3, +36 % giờ máy, +≈ 4 h nướng) và D2 (B cho cú lặn: ≈ 0,9 h CPU/giây phim; tỉ lệ cú lặn 10 % hay 20 %).
3. **Duyệt bậc 5**: mật độ bụi trước 1900 × 0,45 (D5).
4. **Ghi RIGHTS/AUTHORSHIP (phiên P)**: 18 vân Poly Haven CC0 (`reports/nc-cpu/RIGHTS-NC.md`, tác giả + SHA); quyết định sáng tạo trong lệnh NC-CPU 19/10 22:51 (3 cách, 2 mốc, cú lặn 1779 → 1782 lướt qua pin nổi cháy).
5. Phiên P merge khi duyệt. Nhánh **không** merge.

**DỪNG — chờ chủ dự án.**

