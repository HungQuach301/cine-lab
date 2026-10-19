Nhánh thật: `claude/clever-franklin-daez5k` (harness buộc tên này; lệnh yêu cầu `nc-cpu` — mọi commit được đẩy lên CẢ HAI nhánh, nội dung như nhau). Gốc: `origin/main` @3176ad1b. Không merge. Không sửa mã k2v cũ, `scripts/**`, `checks/`, `docs/`, `channel-*/`. V7B (`origin/ccr-ef2b66f0-9639kq`) chỉ ĐỌC (worktree tạm ngoài repo). Không đọc mã `checks/` ngoài `RULES-LL.md` (đúng lệnh).

# NC-CPU — BÁO CÁO: đo thật "bước nhảy chất lượng" chỉ bằng CPU (chưa đổi đường ống sản xuất)

## §0 Tóm tắt

| Việc | Kết quả |
|---|---|
| A. three.js + NƯỚNG Cycles | **Khả thi, thắng rõ nhất.** Nướng 1 lần/mốc: 1782 = **1 481 s** (4 lượt: trời, nảy nắng, nắng chuẩn hoá, lửa pin nổi), 2026 = **1 907 s** (3 lượt, máy có tải song song), hộp 4 × 6,5 km, 3 m/texel. Dựng: khung đơn 1080p spp 4 **25,7–29,3 s** (V7B cùng cách đo 22,7 s, ≈ +20 %); khung chuỗi spp 2 **4,4–5,0 s** (cú lặn, có tải). Vân: 18 tấm CC0 = 119 MB đĩa, 201 MB bộ nhớ đồ hoạ; lightmap 4,6–4,9 MB/mốc. |
| B. Cycles CPU trực tiếp | **Khả thi.** Cảnh Blender đứng riêng (xuất từ k2v + vật liệu riêng). 1080p: nhanh 16 spp + OIDN **87–127 s/khung**; đẹp 128 spp [B_DEP]; cú lặn đêm (12 spp, 10 đám cháy + khói thể tích) **≈ 128 s/khung**. |
| C. Eevee trên llvmpipe | **Chạy được** (cảnh báo nguyên văn: `EGL Error (0x3009): EGL_BAD_MATCH: Arguments are inconsistent (for example, a valid context requires buffers not supplied by a valid surface).` — vẫn ra ảnh đúng). 1080p 32 mẫu [C_SFK] — **chậm hơn Cycles nhanh** vì OpenGL phần mềm. |
| 6 khung cổng × 3 cách | `reports/nc-cpu/khung/{A,B-nhanh,B-dep,C}/cong-*.jpg` (+ `khung/V7B/` bản sao để so). Tờ so: `reports/nc-cpu/to-so-khung.jpg`. |
| Cú lặn 20 s | [LAN] |
| Chấm mù (640×360, 3 vai × 6 loại cảnh, Sonnet 5.5) | **A hạng nhất 11/18**, V7B 3, B 2, C 2. Craft TB: A **6,28** · C 5,61 · B 5,33 · V7B 5,28. Độ thật bề mặt: A **5,67** · C 5,17 · B 4,94 · V7B 4,50. |
| Ước cả tập 745 s | [TAP] |
| Chi phí | Claude **[USD]** (mốc $8), OpenAI **$0** (không ảnh AI), ElevenLabs 0, YouTube 0. Giờ máy CPU ≈ **[GIO] h** (mốc 10 h). |
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
| So steady-state cùng shot (t3tl ↔ ncA, máy rảnh) | [SEQ] |

### 2.2 Cách B — Cycles CPU trực tiếp
Cảnh Blender ĐỨNG RIÊNG: hình học xuất từ k2v của đúng khung (`nc_export.js`), vật liệu riêng: nền = albedo nhìn thẳng xuống của chính cảnh A (cùng vân CC0, đường, vườn), nhà = màu đỉnh k2v × vữa + cửa sổ thủ tục + ngói, công sự = đá CC0, bụi/cây = màu bản sao, nước Principled (Fresnel, sóng bump động), trời gradient như k2v (tia máy thấy trời sáng, tia khuếch tán nhận ánh trời k2v), sương e^(−σd) trong MỌI vật liệu; ảnh HDR được **chỉnh màu bằng chính đường ống k2v** (`gradeHDR`: ACES + LUT A + V6 grade + hạt) để cùng tông với A.

| Đo (B, 1080p, 4 luồng) | Số |
|---|---|
| Nhanh: 16 spp + OIDN, adaptive 0,02, nảy 4/3/2 — 6 khung cổng | **88 · 87 · 99 · 109 · 106 · 127 s** (+ nạp 5–10 s, chỉnh màu 4,4 s) |
| Đẹp: 128 spp + OIDN | [B_DEP] |
| Cú lặn đêm: 12 spp + OIDN, dữ liệu bền, 10 đám cháy (đèn + ngọn lửa phát xạ) + 10 cột khói THỂ TÍCH | **≈ 128 s/khung** (đo sạch khung 228–230; khung 216–227 có tải chồng 125–220 s) |
| Ước "cú lặn" cả tập: 20 % × 745 s ≈ 150 s × 24 = 3 600 khung | 3 600 × 128 s ≈ **128 h CPU** → **13 phiên × ≤ 10 h** (4 vCPU/phiên); ngày không khói thể tích ≈ 100 s/khung → 100 h, 10 phiên |

### 2.3 Cách C — Eevee trên OpenGL phần mềm
- **Chạy được** trong container (Blender 5.2 Eevee qua EGL → Mesa llvmpipe). Lỗi in ra (không chặn): `EGL Error (0x3009): EGL_BAD_MATCH: Arguments are inconsistent (for example, a valid context requires buffers not supplied by a valid surface).` ×3. Cảnh rỗng 640×360: 34 s (biên dịch shader).
- Cùng cảnh, cùng vật liệu, cùng máy với B; 32 mẫu TAA, bóng, raytracing màn hình.
- 1080p: [C_SFK]. **Chậm hơn Cycles 16 spp** trên máy này: Eevee là trình dựng GPU, llvmpipe giả lập GPU bằng CPU nên không có lợi thế; ảnh gần như trùng B (cùng ánh sáng/sương) nhưng thiếu GI thật.

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

[LAN_CT]

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
[CHAM2]

## §6 Ước cả tập 745 s

[TAP_CT]

## §7 Thứ CPU KHÔNG làm được (so GPU) và cách thay

| Hạng mục | GPU làm | Trên CPU đo được | Cách thay đã thử / đề xuất |
|---|---|---|---|
| Ánh sáng toàn cục mọi khung | path tracing thời gian thực/gần thực | Cycles 87–128 s/khung → chỉ cho ≤ 20 % thời lượng | **Nướng** GI tĩnh theo mốc (A, 25–32 phút/mốc); vật động (người, tàu, khói) vẫn đèn k2v |
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
- Số A khung đơn gồm khởi động; số A khung chuỗi đo khi có tải → cần đo lại khi đưa vào sản xuất ([SEQ]).

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

Rủi ro: (1) A chậm hơn V7B ≈ 20 % khung đơn ([SEQ] cho chuỗi) → +giờ máy; (2) lightmap sai khi phố đổi trong shot (mọc/sập) — chỉ nướng phần tĩnh, AO động vẫn SSAO; (3) cú lặn B nặng: 13 phiên song song cho 150 s.

[CUOI]

