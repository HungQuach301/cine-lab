Nhánh thật: `claude/v7c-layout-density-qg4mng` (harness buộc tên này; lệnh yêu cầu `v7c`). Gốc: `origin/ccr-ef2b66f0-9639kq` @317dcf51 (V7B) → `git merge --no-ff origin/main` @3176ad1b → `git merge --no-ff origin/claude/eloquent-dijkstra-kemr8j` @4fe45ec3 (NC-GPU ⊃ NC-CPU): **0 xung đột** (commit db62b9ed, e9d2abc0). Không merge vào `main`. Không sửa `loi-khoa.txt` (51d1c773…), `checks/`, `docs/`, sổ. Không đọc mã `checks/` (chỉ chạy `k2check.py`).

# V7C T3 Gibraltar — BÁO CÁO: vòng thử 3 — BỐ CỤC + MẬT ĐỘ trên đường dựng A (0 AI trên hình)

## §0 Tóm tắt

| Việc | Kết quả |
|---|---|
| 1. Cách A = `opt.nc` | Đóng gói trong `t3tl.js` (`build` → `buildCore` + bọc `up.js` khi có `opt.nc`); `bake.js` nhận **nhiều lightmap theo năm** (`bakes`). **Tắt → trùng byte V7B 3/3 khung; bật → trùng byte cảnh ncA NC-CPU 3/3**; có lightmap: lệch khung NC-CPU A **0,69–1,70/255** (V7B↔A: 14–39). **Nướng 5 lightmap**: b2026 · b1940 · b1779 (phố nguyên) · b1781r (sau 12/4/1781) · b1782 (+ lửa) = **8 368 s ≈ 2,3 h** CPU. |
| 2. Bố cục + mật độ | 9 shot soạn lại máy bằng **mặt nạ ID** (tái dùng `idmask.js`, thêm phố/trại/công sự/tiêu điểm). Nội dung TB theo thời lượng **25,1 % → 39,1 %**; trống 57,6 → 53,2 %. Đạt ngưỡng nội dung: **H1 78 %, H2 58 %, C4 52 %**; chưa đạt: H3 47, C3 37, C5 38, C1 23, C2 1,4, H2T 6,5 (§2). Mật độ mới: lều **theo hàng lối**, **720 ngựa** (S048), khói bếp, người đi giữa dãy; phố 2026 có **cây, đèn, xe đỗ** theo đường OSM; **shot thumbnail H2T** (đúng N2r của X01/X08) ở câu 0f. |
| 3. XEM CÂM | Bản cuối, P đọc lại (quy ước V7B): **320×180: 18/24 · 640×360: 20/24** (V7B 14/24). Từ khoá 24/24 · 21/24. Q1 6/6, Q2 6/6 (cả hai mức); **Q3 "vì sao đói" 3/6** (chỉ suy ra phong toả); Q4 3/6 (320) · 5/6 (640). **18/24 đúng sàn** (nêu tên §9). |
| 4. Thước cắt | `tl_buoc` khai trong log (H2 15 bước, H3 3). Cắt/phút: đặc tả **4,05** (không tính bước năm) · **13,17** (tính 18 bước năm); video (q_k116 1.16.1 qua k2check) **7,09** = 8 ranh khớp + 6 chỉ-video (3 bước năm, 3 cú cẩu). |
| 5. k2check 1.16.1 | TRƯỢT tập (như V7B: Q37/NHIP-K2, PP-1 chưa có thẻ phương pháp, SACH-1 1 lỗi "không log chữ", NC-H1, **XEM-CAM chờ chủ dự án**). Mới đạt so bản nháp: ML1 9/9, CHUONG-1, **NHIP-NGHIA 16/16**, TL-2, TL-3. TL-1 cảnh báo: góc cao + tl **95,8 %**. |
| Khung cổng + chấm mù | 6 (+1) khung PNG 1920×1080 `reports/v7c/khung/`. Chấm mù 3 người (Sonnet 5.5): craft **V7C 5,17 · V7B 5,39 · A-NC-CPU 6,39** — **V7C THUA** ở vây hãm/cảng/phố dày ("board-game grid", "top-down crop, no sky"); thắng **bờ + chiến sự** (góc thumbnail, 3/3). Thử thêm **V7C-lai** (khung xiên có chân trời, cùng shot/thời điểm): craft **7,00**, hạng nhất 6/9 — nhưng nội dung chỉ 14–25 %. → **Mâu thuẫn giữa luật bố cục đo được và độ "điện ảnh"** (§7, V7C-D1). |
| Giờ máy / chi phí | Giờ máy ≈ **5,8 h** (mốc 12 h). Claude **$4,69** (mốc $8). OpenAI **$0**, ElevenLabs/Gemini/RunPod/YouTube 0. Không thuê GPU. Ước cả tập G0 1080p: A ≈ **54 h ± 25 %** CPU + nướng ≈ **4,2 h** (§10). |

**Xem nhanh:**
- Bản xem 640×360 không phụ đề: `reports/v7c/ban-thu/v7c-xem-khong.mp4` · có phụ đề kiểm: `v7c-xem-phude.mp4`
- Tờ so V7B ↔ V7C 8 cặp: `reports/v7c/so/to-so-8-cap.jpg` · tờ so khung cổng (V7B · A · V7C · V7C-lai): `reports/v7c/khung/to-so-khung.jpg`
- Chuỗi xem câm: `reports/v7c/xem-cam/cuoi/r320/to-*.jpg` (sàn), `r640/to-*.jpg`

## §1 Việc 1 — cách A thành tuỳ chọn cảnh `opt.nc` + nướng theo mốc

**Mã:**
- `design/k2v/tl/scenes/t3tl.js`: `build(ctx)` = `buildCore` khi không có `opt.nc` (hoặc `nc.off`) — `up.js` KHÔNG được nạp (nó thay `fog_fragment` toàn cục); có `opt.nc` → `preBuild → buildCore → postBuild` đúng thứ tự `nc/ncA.js` của NC-CPU. `ncA.js` gọi `buildCore` (không bọc hai lần).
- `design/k2v/tl/nc/bake.js`: `opt.nc.bakes = [{dir, wY: [năm đầu, năm cuối], fire?}]` → đổi lightmap theo năm của khung (ngoài mọi cửa sổ → cửa sổ gần nhất); `opt.nc.bake` một lightmap vẫn chạy như NC-CPU.

**Kiểm bit (960×540, spp 4, `render.js --only`):**

| Khung | Tắt `opt.nc` ↔ V7B @317dcf51 (SHA-256 JPG) | Bật `{}` ↔ `--scene ../nc/ncA` @e9d2abc0 |
|---|---|---|
| C4 f84 (cảng) | `d29652f1c6ba` = `d29652f1c6ba` | `9908c1629669` = `9908c1629669` |
| C3 f276 (phố dày) | `838ca5b00f8b` = `838ca5b00f8b` | `285576b900f9` = `285576b900f9` |
| C5 f62 (toàn cảnh) | `3f4cbd0d7ddb` = `3f4cbd0d7ddb` | `338db2099b63` = `338db2099b63` |

**Khớp khung NC-CPU (1080p spp 4, `bake: b1782` nướng lại trong phiên này) ↔ `reports/nc-cpu/khung/A/cong-*.jpg`** (`reports/v7c/do/khop-nc-cpu.json`): lệch TB **cảng 0,69 · phố dày 1,70 · bờ + chiến sự 1,70 /255** (p99 11–16); đối chứng V7B ↔ A: 22,9 · 39,3 · 14,4. Phần lệch còn lại là JPEG q92 + albedo nền của nướng (hộp 1 m phố + 4 m cả vùng thay vì m1/m4 của NC-CPU).

**Nướng** (`scripts/k2tl/v7c_nuong.sh`: `nc_export.js` máy nhìn thẳng xuống 4,2 km → `nc_topo.js` 4 m + 1 m → `nc_blend.py nuong`; hộp E −3000…1000, N −3000…3500, 3 m/texel, 24 spp; mã NC-CPU không sửa):

| Lightmap | Mốc / trạng thái | Shot dùng | Giây (trời · nảy · nắng · lửa) | Tổng |
|---|---|---|---|---|
| b2026 | 19/10/2026, nhà V7B có vật liệu | H1, H2 (đoạn 2026), H3 (≥ 1960) | 671 · 473 · 423 | 1 583 s |
| b1940 | 1/6/1940, ghost 1943 + đường băng đầu | H3 1938–1960 | 442 · 338 · 369 | 1 162 s |
| b1779 | 15/1/1780 — phố 1779–81 **nguyên**, trại + công sự | H2 (1309–1782,5), C1–C4, C5 trước 10:45 12/4/1781 | 947 · 592 · 808 | 2 362 s |
| b1781r | 1/7/1781 — vùng THE RUINS **đã sập** | C5 sau 12/4/1781 10:45 | 674 · 464 · 513 | 1 664 s |
| b1782 | 13/9/1782 15:30 + 10 đám cháy pin nổi (kênh B) | H2 cuối, H2T | 490 · 296 · 339 · 457 | 1 597 s |

- Phải cài `imageio` vào Python của Blender (`/opt/bpy`) — NC-CPU không ghi bước này.
- Giới hạn: H2 bước năm 1309–1727 dùng b1779 (gần nhất; phố trước 1704 là lớp 1705 đại diện như V7B, bậc 5). Nảy nắng nướng theo một hướng nắng (như NC-CPU §8).

## §2 Việc 2 — bố cục + mật độ (việc chính)

### 2.1 Thước đo (cùng thước cho trước/sau)
- `design/k2v/v7c/idmask_v7c.js` = `design/k2v/v2v/idmask.js` (NC-V2V) + **phố** (nền đô thị theo năm), **đất bằng / sườn / vách** tách riêng, **trại**, **công sự**, **tiêu điểm** (chiếu điểm thế giới của vật hero qua đúng máy: bề ngang hộp bao, tâm ở 1/3 giữa hoặc giao điểm 1/3). Driver `do_bocuc.js` nối mã vào bản sao `page.js` lúc phục vụ (không sửa `page.js`); `--root` đo được cây mã V7B.
- **Nội dung** = phố + nhà + trại + công sự + tàu + cờ + pin nổi + lửa + người + khác (xe, cây phố, đèn). **Trống** = nước + đất bằng tự nhiên + sườn > 30 m. Vách Rock và trời tách riêng. Tiêu điểm: `design/k2v/v7c/tieu-diem.json`.
- Soạn máy: `scripts/k2tl/v7c_thu_may.py` đo mọi ứng viên trên cùng trạng thái khung + khung màu để soi (≈ 60 ứng viên qua 9 shot; `reports/v7c/do/` giữ số đo cuối, khung soi ngoài git).
- V7B đo lại bằng thước cuối trên cây @317dcf51 (`reports/v7c/do/bocuc-v7b/`). 2 khung/s.

### 2.2 Bảng bố cục từng shot — trước (V7B) ↔ sau (V7C) — `reports/v7c/do/bang-bo-cuc.md`

| Shot | Loại (ngưỡng) | V7B: nội dung % (min) · khung đạt · trống · tiêu điểm đạt (rộng) · AGL · nhìn xuống · tiêu cự 35 mm | **V7C** |
|---|---|---|---|
| H1 | phố (≥ 50) | 52,9 (52) · 100 % · 24 · 0 % (41) · 245 m · 12,5° · 30 mm | **78,1 (78) · 100 % · 22 · 100 % (51) · 355 m · 29,3° · 37 mm** |
| H2 | tàu–vịnh (≥ 40) | 49,1 (39) · 55 % · 51 · 0 % (44) · 85 m · 26,9° · 27 mm | **58,3 (33) · 78 % · 42 · 81 % (34) · 267 m · 41,5° · 32 mm** |
| H2T (mới) | tàu–vịnh (≥ 40) | — | 6,5 (5) · 0 % · 39 · 0 % (96) · 25 m · −6,3° · 28 mm |
| H3 | phố (≥ 50) | 28,5 (6) · 41 % · 47 · 100 % (9) · 245 m · 12,5° · 30 mm | 46,9 (19) · 41 % · 50 · 0 % (12) · 374 m · 26,4° · 33 mm |
| C1 | trại (≥ 40) | 12,8 (0) · 0 % · 78 · 100 % (66) · 189 m · 18,2° · 30 mm | 23,0 (0) · 33 % · 67 · 60 % (62) · 228 m · 27,8° · 51 mm |
| C2 | tàu–vịnh (≥ 40) | 0,9 (1) · 0 % · 51 · 100 % (17) · 169 m · 0,2° · 45 mm | 1,4 (1) · 0 % · 86 · 0 % (82) · 250 m · 11,5° · 45 mm |
| C3 | phố (≥ 50) | 21,2 (5) · 0 % · 61 · 59 % (33) · 127 m · 13,9° · 33 mm | 37,0 (12) · 10 % · 49 · 86 % (54) · 135 m · 19,2° · 33 mm |
| C4 | tàu–vịnh (≥ 40) | 9,1 (9) · 0 % · 64 · 0 % (13) · 171 m · 12,0° · 25 mm | **51,7 (0) · 41 % · 47 · 52 % (41) · 120 m · 32,5° · 35 mm** |
| C5 | tàu–vịnh (≥ 40) | 21,9 (22) · 0 % · 71 · 68 % (27) · 228 m · 23,4° · 25 mm | 37,5 (36) · 0 % · 63 · 52 % (39) · 237 m · 27,5° · 30 mm |
| **TB theo thời lượng** | | nội dung **25,1** · trống 57,6 · tiêu điểm 52 % · góc cao (khung) 95,5 % · thấp 4,1 % | nội dung **39,1** · trống 53,2 · tiêu điểm 54 % · góc cao 91,2 % · thấp **9,5 %** |

Đọc thẳng:
- **Đạt cả (a) và (c):** H1, H2, C4 (theo TB shot). Trống ≤ 1/3 chỉ H1 đạt.
- **H3** dưới 50 % vì 1938–1985 eo đất còn trống (đúng dữ liệu; bước 2026 đạt 80 %). Tiêu điểm "chỗ đường cắt đường băng" lệch phải (✗).
- **C1:** dải trại theo nguồn (35 % lều của đợt 1782 ở 10/1779) chỉ phủ đủ khung khi nhìn gần từ trên (43 % ở U1); 0–8 s trước ngày dựng trại là đồng trống (đúng nguồn) → mở bằng khung có Rock rồi bay qua trại.
- **C2:** cảnh biển, hàng chặn + thuyền nhỏ — nội dung ≈ 1 % ở mọi máy đã thử; không đạt được mà không thêm vật không nguồn. Đổi để kể đúng: thuyền châu Phi (V7B: điểm đến nằm phía đông hàng chặn → trông như lọt qua) **dời tới sát đầu nam hàng chặn rồi quay về** (S042), máy ≈ 1,2 km sau hàng chặn nhìn về Rock.
- **H2T (thumbnail)** cố ý thấp và nhiều trời theo đúng X01/X08 — không đạt luật nội dung (vai: khoảnh khắc biến cố).
- **(c) máy gần hơn:** AGL TB các shot cao 120–374 m; nhìn xuống 19–42° (C2 11,5°); tiêu cự hẹp hơn ở C1 (51 mm), C4 cận (35–50 mm), H1 (37 mm). Góc cao theo khung 91,2 % (≥ 75 %).

### 2.3 Điểm máy mới (đặc tả `channel-k2/k2c-t3-01/v7p/mk_ep_v7c.py`)
| Shot | Điểm | Máy (E, cao, N → nhìn, fov) | Ghi |
|---|---|---|---|
| H1 | D7 | [420, 360, 700] → [40, 0, 180], 36° | mép nam La Línea nhìn nam: cổng, chỗ cắt đường băng, phố hai phía |
| H2 | K2 | [60, 420, −1000] → [−330, 0, −900], 40° → (10,5–13,5 s lia) → [−760, 0, −1045], 44° | trên sườn Rock: phố + lâu đài phủ khung; lia sang hàng pin nổi ở dải trên |
| H2T | **N2r** | [−1950, 25, −1150] → [−600, 180, −1600], 46° | **đúng điểm X01/X08** (`reports/dong-goi-t3-v2` §1), câu 0f, 5,0 s |
| H3 | D7h | [−150, 380, 560] → [−200, 0, −200], 40° | biên giới nhìn nam qua đường băng vào phố Gibraltar |
| C1 | A3 → U1 | mở [−1250, 330, 3500] → Rock; 7,5–10,4 s bay qua trại; U1 [−1150, 170, 2780] → [−1220, 0, 2990], 22° | nhìn bắc để mặt lều được nắng (nhìn nam/tây lều ngược sáng — đã thử) |
| C2 | E2 | [−4440, 250, −3180] → [−3300, 0, −2700], 30° | sau hàng chặn, nhìn về Rock |
| C3 | Ca2 | cận AGL 4 m [−118, 93, −985] → lâu đài, 38° (0–4,5 s) → cẩu → [−200, 300, −1400] → [−600, 0, −1100], 42° | |
| C4 | Bm | cao [−700, 260, −450] (0–1,8 s) → cận Old Mole [−603, 53, −678], 28° (3–7 s) → [−560, 120, −470], 48° | |
| C5 | Cc2 | [−250, 300, −1700] → [−700, 0, −1250], 44° (0–4,5 s) → lia [−110, 378, −1652] → [−605, 0, −1202] | |

Lỗi đã gặp và sửa: (1) spline Hermite (tiếp tuyến Catmull-Rom) **vọt xuống dưới đất** ở cú cận C3/C4 khi khoá kề là cú cẩu cao (AGL 22 → −1 m) → thêm khoá giữ 0,02 s hai đầu mỗi cú cẩu; (2) chú thích chèn giữa dòng nuốt khoá máy C4 (đúng BAI-HOC #42, lần này trong Python — bắt được ở lỗi cú pháp).

### 2.4 Mật độ — vật mới và nguồn (5 bậc; không thêm vật không nguồn)
| Vật | Shot | Nguồn / bậc | Mã |
|---|---|---|---|
| Lều **theo hàng lối**, lấp kín từ đầu dãy theo cửa sổ năm (thay rải ngẫu nhiên 35 % khắp dãy); dải đất giẫm dài theo phần đã dựng | C1 | vị trí dãy: Faden 1783 (bậc 1); số lều: S048/S065 (bậc 2) — **không đổi số**; hàng lối: bậc 4 (bản khắc) | `tl7.js camps(…, {hangLoi})`, `opt.campRows` |
| **720 ngựa** ở 3 hàng cọc giữa dãy E5–E7 | C1 | S048 Drinkwater 1786 (dòng 4177 bản OCR `historyoflatesie00drin`, SHA `d17a7894…`): 10/1779 "12 squadrons of horse"; số đặt 720 < 12 × 120; vị trí bậc 5 | `tl/ngua.js` (mới) |
| Khói bếp 21 cột nhỏ dọc dãy | C1 | bậc 5 (vật nền phụ) | `opt.smoke` |
| 100 người đi giữa dãy lều | C1 | có mặt: S048 ≈ 14 000 quân (bậc 2); vị trí bậc 5 | `opt.lives` |
| Người khiêng thùng (26) từ thuyền vào đống thùng Old Mole | C4 | S054 (bậc 2); số/vị trí bậc 5 | `opt.lives` |
| Cây đường phố, cột đèn, xe đỗ dọc đường OSM (không đặt vào trong dấu chân nhà) | H1, H3 | tuyến: OSM 2026 (ODbL, bậc 1); mật độ/kiểu: bậc 5 (vật nền phụ) | `tl/duong2026.js` (mới), `opt.pho2026` |
| Bỏ viền phe quanh tàu/quân Anh (V7B-D4) | mọi shot | — | `opt.rimPhe: ['es']` |

**Không làm (ghi để rõ):** xe ngựa/la của trại — Drinkwater có "covered waggons" (1781) và "multitudes of mules" (1782), **lệch ngày** so với 1779 (nguyên tắc V7B-D6) → không đặt. Mặt tiền 2026: `city.js` đã có cửa sổ/khung/ban công theo kiểu toà và màu tường theo bảng V7B; phiên này chỉ đưa máy gần hơn (≤ 1,2 km) để chi tiết đó hiện lên, cộng cây/đèn/xe — **chưa** làm thư viện mặt tiền mới (cửa chớp, mái đa dạng theo toà). Khung hero vẫn có mảng xám trơn của sân đỗ/đường băng (đúng thật) và khối công nghiệp trơn ở tiền cảnh.

## §3 Việc 3 — XEM CÂM (sửa theo V7B §8)

Giao thức V7B (`scripts/k2tl/v7c_cam.py` dùng nguyên vai/câu/đáp án `v7b_cam.py`): 3 vai, `claude -p` ghim claude-sonnet-5-5, chỉ Read; 59 khung (1/2 s), không phụ đề, không lời; thêm mức 640×360 (V7B-D7).

| Lượt | Bản (SHA master) | 320×180 từ khoá · **P** | 640×360 từ khoá · **P** | Thay đổi trước lượt |
|---|---|---|---|---|
| V7B (để so) | `d4b6dec9…` | 22 · **14** | — | — |
| nháp (không cách A) | — | 23 · **18** | 23 · **20** | 9 shot, máy mới, H2T |
| cuối lượt 1 | `b4f554ff…` | 24 · **18** | 24 · **19** | C1 mở thấy Rock; C2 nhìn về Rock; người hái rau gần; cận Old Mole 50 m |
| cuối lượt 2 | `8e68eca6…` | 23 · **18** | 23 · **19** | bay qua trại → U1 nắng trưa; người 12–25 m cúi 40°; cận Old Mole 28 mm — **2/3 người chấm 640 đọc người cúi 40° thành "ngã lăn"** |
| **cuối (bản giao)** | **`c8bb1c02…`** | 24 · **18/24** | 21 · **20/24** | cúi 29° |

Theo câu (P, bản giao): **Q1 ai giữ Rock 6/6 · 6/6** (cờ Union ≥ 5 % bề ngang, 4,5 s ở C3 — 2 khung mẫu) · **Q2 1779 bắt đầu gì 6/6 · 6/6** · **Q3 vì sao đói 3/6 · 3/6** · **Q4 cái gì đến cứu 3/6 · 5/6**. Bảng điểm `reports/v7c/xem-cam/p-doc.json`; nguyên văn `reports/v7c/xem-cam/cuoi/r*/phieu-R*.json`. Độ rõ 2,0 (320) · 2,33 (640).

Đã làm theo V7B §8:
- **Cận cờ mỗi chương:** chương vây hãm (C3 0–4,5 s), máy cách cờ ≈ 152 m, cờ ≈ 5,4 % bề ngang. Không làm cận Line Wall thứ hai ở C5 (hết hạn mức lướt thấp — §9).
- **Tách "đến cứu" khỏi "pháo bắn":** bỏ viền đỏ tàu Anh; Rodney dỡ hàng Old Mole cận **≈ 50 m ngang (AGL 53 m), 3–7 s, 19/1 → 1/2/1780**: thuyền, người khiêng, đống thùng lớn dần; Darby **thả neo xong 3,6 s, pháo bắn từ 5,8 s (cách 2,2 s)**.
- **Chuỗi nhân quả:** thuyền châu Phi tới sát hàng chặn rồi quay về, máy ≈ 1,2 km; cận người cúi hái rau (S052; Drinkwater dòng 4723 "thistles, dandelion, wild leeks…") **12–25 m, 4,5 s**.
- **Bản đồ phủ ≤ 3 s:** không dùng — Q1/Q2 đã 6/6 ở cả hai mức.

Chưa giải được: **Q3** — cả 3 vai đều nói "không có hình nào cho thấy đói, kho rỗng" dù thấy người trên sườn; người hái rau ở 320×180 không đọc thành "kiếm ăn". **Q4 ở 320**: đống thùng đỏ được nêu ở 640 ("people unload barrels"), ở 320 chỉ "red objects". Lạc chung 3/3: mở đầu đêm 2026, bước năm 1316–1704, 1782 trước 1779, 1939–2026 (đúng thiết kế lời móc TL-5, như V7B).

**XEM-CAM (k2check):** TB AI **6,00/8** (= ngưỡng) — **chưa có chủ dự án chấm** → TRƯỢT cho tới khi chủ dự án xem tắt tiếng.

## §4 Việc 4 — thước cắt

- `log-shot-v7c.json` có `tl_buoc` (mỗi bước: giây trong shot, năm từ → tới) và `tl_buoc_n`: **H2 15 · H3 3 · còn lại 0**.
- Đặc tả: 9 shot, 8 ranh → **4,05 cắt/phút** (shot TB 13,2 s). Tính cả 18 bước năm: (8 + 18) / 1,974 phút = **13,17 cắt/phút**.
- Video (TL-1 (c) của `q_k116.py` 1.16.1, qua `k2check.py`): **14 cắt = 7,09/phút**; khớp ±0,5 s 8/8 ranh đặc tả; 6 cắt chỉ-video: 0:15.4, 0:23.4, 0:23.8 (**bước năm** 2026→1309 và 1704–1727 có khói đổi cấu trúc), 1:22.9, 1:23.2 (**cẩu** C3), 1:35.4 (**hạ máy** C4). Không tính 3 bước năm: 11 = 5,57/phút; không tính bước năm và cú cẩu: 8 = 4,05/phút.

## §5 Việc 5 — k2check 1.16.1 (`reports/v7c/do/k2check-ban-cuoi.txt`; bản nháp: `k2check-ban-nhap.txt`)

Lệnh: `k2check.py v7p/episode-v7c.yaml --tl …/timeline.json --master …/k2c-t3-v7c-v1-master.mp4 --no-asr --cap`. LOCK KHỚP.

| Hàng | Kết quả | Ghi |
|---|---|---|
| TL-1 | CẢNH BÁO | góc cao + tl 113,5 s = **95,8 %**; 8 điểm máy; trôi góc cao trung vị 0,14 %/s; video 7,09 cắt/phút (§4) |
| TL-2 | ĐẠT | khai `goc: thap` 1 shot (H2T) 5,0 s = 4,2 %. **Theo khung** (cả cận C3 0–4,5 s, AGL 4 m): 9,5 s = **8,0 %**; theo mẫu 2 khung/s AGL < 50 m: 9,5 % |
| TL-3 | ĐẠT | `trong_pct` đủ 9 shot; C1 62,2 % (trên 60 %, có `tl`) |
| NHIP-NGHIA | **ĐẠT 16/16** | `nhip-vat-v7c.json` |
| CHUONG-1 | ĐẠT | 1 thẻ "1779 — The Great Siege" 3,00 s (= trần 3 s) |
| ML1 | ĐẠT 9/9 | khai `loi_khoa`, `claims_md` |
| XEM-CAM | TRƯỢT | thiếu chủ dự án; TB AI 6,00/8 |
| PP-1 | TRƯỢT | bản thử không có thẻ phương pháp (như V7B) |
| SACH-1 | TRƯỢT (1) | "không log chữ" — bản thử không xuất log chữ k2.js; không có chữ ngoài bộ đếm + thẻ chương |
| NC-H1 | TRƯỢT (4) | "có lớp nhà khai 0" — trường khai lớp nhà chưa có trong đặc tả timelapse (tên trường chưa rõ trong RULES; hỏi K) |
| Q37 / NHIP-K2 / Q37 (1.13) | TRƯỢT | TB 5,15 s/biến cố, dài nhất 9,8 s (ngữ pháp timelapse; như V7B) |
| O2, Q26b-K2 | CẢNH BÁO | |

Trường K116-D9 đã xuất: `goc`, `tl`, `vai`, `noi`, `nguoi`, `trong_pct`, `su_kien` [{t, k, s}], `diem_may`, `moc`, `bac`, `nguon`, `ai_image`/`ai_texture` = false, `tl_buoc`; `nhip-vat-v7c.json`; `xem-cam-v7c.json` (8 mục = 4 câu × 2 tiêu chí, `dung` = P đọc lại, `video_sha256`).

## §6 Khung cổng 1920×1080 (`reports/v7c/khung/`, PNG sạch, không chữ, spp 4, cách A)

| Khung | Shot @ giây | Bão hoà trung vị (V7B) |
|---|---|---|
| `cong-vay-ham` | C1 @ 21,8 (28/10/1779, U1) | 0,557 (0,600) |
| `cong-cang` | C4 @ 5,0 (cận Old Mole dỡ hàng) | 0,475 (0,608) |
| `cong-pho-day` | C3 @ 11,5 | 0,549 (0,584) |
| `cong-hero` | H3 @ 10,4 (2026) | **0,239** (0,329) |
| `cong-toan-canh` | C5 @ 2,6 (Darby) | 0,573 (0,580) |
| `cong-bo-chien-su` | **H2T @ 1,0 (góc thumbnail, pin nổi cháy)** | 0,890 (0,388) |
| `cong-bo-chien-su-cao` (thêm) | H2 @ 13,8 (từ trên sườn) | 0,576 |
| **trung vị** | | **0,557** (V7B 0,584 · A-NC-CPU 0,466) — NG-D4 ≥ 0,40 đạt; khung hero dưới ngưỡng |

Thử: `reports/v7c/khung/lai/cong-{vay-ham,cang,pho-day}.png` (V7C-lai, §7). Tờ so: `reports/v7c/khung/to-so-khung.jpg`. Tờ so V7B ↔ V7C 8 cặp cùng câu lời: `reports/v7c/so/to-so-8-cap.jpg`.

## §7 Chấm mù (3 người AI, 640×360, giao thức NC-CPU `blind_nc.py`) — `reports/v7c/cham-mu/`, `cham-mu-lai/`

**Lượt 1: V7B ↔ A-NC-CPU ↔ V7C, 6 loại cảnh** (craft / realism / số hạng nhất):

| Loại | V7B | A-NC-CPU | V7C |
|---|---|---|---|
| vây hãm | 4,33 / 4,0 / 0 | **5,33** / 5,0 / 3 | 3,0 / 2,67 / 0 |
| cảng | 5,0 / 4,67 / 0 | **6,67** / 6,0 / 3 | 3,67 / 3,67 / 0 |
| phố dày | 6,0 / 5,33 / 0 | **7,0** / 7,0 / 3 | 5,0 / 4,0 / 0 |
| hero | 6,67 / 5,33 / 1 | 6,67 / 5,33 / 1 | 6,33 / 4,67 / 1 |
| toàn cảnh | 5,0 / 4,0 / 0 | **6,67** / 6,0 / 3 | 6,0 / 5,0 / 0 |
| bờ + chiến sự | 5,33 / 4,33 / 0 | 6,0 / 5,0 / 0 | **7,0** / 5,67 / 3 |
| **TB** | 5,39 / 4,61 / 1 | **6,39 / 5,72 / 13** | 5,17 / 4,28 / 4 |

Lý do (nguyên văn rút gọn): vây hãm V7C — "top-down view with no rock, sea or context… like a board game" (3/3); cảng V7C — "a top-down view of fortress walls, not a harbour with a convoy" (3/3; mô tả loại cảnh là "đoàn tàu tới cảng", khung V7C là cận dỡ hàng); phố dày V7C — "tight top-down crop with no sky or horizon… noisy ground" (3/3). A-NC-CPU thắng nhờ "haze, horizon, sense of place" ở cùng điểm máy V7B.

**Lượt 2 (thêm V7C-lai: cùng shot/thời điểm, máy xiên có chân trời — nhìn xuống 12–17°), 3 loại:**

| Loại | V7B | A-NC-CPU | V7C | **V7C-lai** | nội dung % V7C-lai |
|---|---|---|---|---|---|
| vây hãm | 4,33 | 5,0 | 3,0 | **6,33 (3/3 hạng nhất)** | 15 |
| cảng | 5,67 | 6,33 | 3,67 | **7,67 (3/3)** | 14 |
| phố dày | 6,0 | **7,67 (3/3)** | 5,0 | 7,0 | 25 |
| **TB craft / realism / toy_like** | 5,33 / 4,67 / 5,22 | 6,33 / 6,0 / 3,89 | 3,89 / 3,44 / 6,67 | **7,00 / 6,44 / 3,55** | |

**Kết luận thẳng:** với người chấm AI, luật bố cục việc 2 (nội dung ≥ 50 %, trống ≤ 1/3, nhìn xuống 25–45°) **làm khung trông như đồ chơi** khi thế giới 1779–81 thưa theo nguồn (trại 35 %, phố hẹp giữa núi và vịnh): muốn ≥ 40–50 % phải cắt chặt từ trên, mất chân trời và sương — thứ làm A-NC-CPU thắng. Khung lai (nội dung 14–25 %) đạt craft cao nhất từ trước tới nay (7,0). Chấm mù không so đối thủ — **điều phối cần đặt V7C và V7C-lai cạnh đối thủ** để quyết (V7C-D1). Không lấy khung đối thủ vào repo.

## §8 Bản thử, tệp, tái tạo

| Tệp | Nơi | Cỡ | SHA-256 |
|---|---|---|---|
| Master 960×540 (G1 + nhạc tạm, −13,9 LUFS, đỉnh −3,2 dBFS) | ngoài git `/var/tmp/cine-out/k2c-t3-v7c/k2c-t3-v7c-v1-master.mp4` | ≈ 128 MB | `c8bb1c02ec262cbae4f89db2882305a832ad951e6700ad6eb2b326ea7df70f7c` |
| 540p không phụ đề / có phụ đề kiểm | ngoài git `…/k2c-t3-v7c-540p-{khong,phude}.mp4` | ≈ 36 MB | `05b2329dd5decc621cdb70263f72883ff9e0bf9a44532263862e5010deb6a612` / `448100460f775f7857107b9fafdc1dd6618bbba11c724693f3ce667fe4035521` |
| **Bản xem 640×360 không / có phụ đề** | trong git `reports/v7c/ban-thu/v7c-xem-{khong,phude}.mp4` | 4,6 MB | `bb2e999fdc1a63cf1d2bc58422753d48c4984b1d0eddc3b913d4bf718ff1e3aa` / `17e2c86a2442a218e21f8e02bb99f970a95abeb93e37a1a8562d696b1a700de8` |
| Lightmap 5 mốc | ngoài git `$K2TL_CACHE/nc/bake/b*/` | 4,6–4,9 MB | meta: `reports/v7c/do/nuong-*.json` |

Tái tạo: `bash scripts/k2tl/v7p_cache.sh` (cần `git fetch origin v5a` cho LUT) → `v7b_mau_nha.py` → `v7b_faden.py` → vân CC0 (54 tệp, SHA khớp `reports/nc-cpu/RIGHTS-NC.md`) → `bash scripts/k2tl/v7c_nuong.sh` → `NC=1 bash scripts/k2tl/v7c_dung.sh` → đo `v7c_bocuc.py run …` / `bang v7b v7c` → `v7c_cam.py to|run` → `v7c_khung.sh` → `v7c_cham_mu.py set|run|score` → `v7c_log.py`.

## §9 Chỉ số trong ±5 % quanh ngưỡng (luật cứng)
- **XEM CÂM 320×180 = 18/24** — đúng sàn (0 %). 640×360 = 20/24 (+11 %).
- **XEM-CAM TB AI = 6,00/8** — đúng ngưỡng K116-D2 (0 %).
- **Lướt thấp theo mẫu khung 9,5 %** (trần 10 %, −5 %); theo khoảng khai (H2T + cận C3) 8,0 %.
- **Thẻ chương 3,00 s** = trần 3 s (0 %, như V7B).
- **Loudness −13,9 LUFS** (mục tiêu −14,0; dải −15,0…−13,8) — cách mép trên 0,1 LU (như V7B).
- Gần nhưng ngoài ±5 %: nội dung C4 51,7 % (+3,4 % trên 50 nhưng ngưỡng của C4 là 40), H3 46,9 % (−6 % dưới 50), C1 `trong_pct` 62,2 % (+3,7 % trên 60 — **trong ±5 %**, TL-3 cảnh báo).
- Không thêm phần tử nào để vượt chỉ số; số lều, số tàu, số người theo nguồn giữ nguyên V7B.

## §10 Giờ máy và chi phí

**Giờ máy phiên này** (đồng hồ, máy bận gần như liên tục) ≈ **5,8 h** (mốc 12 h): bộ đệm + phụ thuộc 0,1 · kiểm bit + khớp 0,4 · nướng 2,3 (chạy chồng) · đo + thử máy 1,2 · nháp 540p 1,2 · bản cuối 3 lượt 1,6 · khung 1080p 0,2 · k2check 0,4 (tổng mục > đồng hồ vì chạy song song).

**Ước cả tập 745 s ở 1080p theo G0** (A cho phần cao ≈ 80 %, cú lặn ≈ 20 % để Cycles GPU phiên sau):
- A (595 s = 14 280 khung): theo NC-CPU §6: V7B ≈ 50 h × 1,36 × 0,8 ≈ **54 h CPU ± 25 %**. Phiên này: khung đơn 1080p spp 4 cách A **15–24 s** (NC-CPU 25,7–29,3 s cùng cách đo, máy bận hơn); vật mới (ngựa, phố 2026) chưa đo riêng — ước ≤ +5 %.
- Nướng: đo **1 162–2 362 s/lightmap (TB 1 674 s)**; T3 ≈ 9 trạng thái → **≈ 4,2 h** một lần.
- Cú lặn/cận đêm (≈ 150 s): Cycles GPU (NC-GPU G0: ≈ 44 h GPU ≈ $52) — phiên sau, không thuê GPU ở phiên này.
- → **≈ 58–60 h CPU** (+ GPU phiên sau) ≈ 6–7 gói × ≤ 10 h song song.

**Chi phí thật:**

| Khoản | Mốc / chặn | Thật |
|---|---|---|
| Claude API (`claude -p` Sonnet 5.5) | $8 / $25 | **$4,69**: xem câm 4 lượt × 2 mức $2,54 · chấm mù $1,05 + $0,55 · (thử 0) — `reports/v7c/*/cost.jsonl` |
| OpenAI | $5 / $20 | **$0** (chấm mù/xem câm dùng Claude như V7B/NC-CPU) |
| ElevenLabs / Gemini / RunPod / YouTube | 0 | 0 / 0 / 0 / 0 |
| Giờ máy | 12 h | ≈ 5,8 h |

Chặn an toàn / lỗi vận hành: `pkill -f` (1 lần) và `kill` theo `grep` (1 lần) khớp chính shell của tôi — đúng BAI-HOC #41 (lần 2 không gây mất việc); từ sau dừng theo PID nhóm. Chú thích giữa dòng nuốt mã (BAI-HOC #42) 1 lần trong `mk_ep_v7c.py` (bắt được bằng lỗi cú pháp).

## §11 Quyết định đề xuất

| # | Đề xuất | Ưu | Nhược | Tác động | Rủi ro |
|---|---|---|---|---|---|
| **V7C-D1** | **Sửa luật bố cục §11.4 cho cảnh có trời**: đo nội dung **trên phần dưới chân trời**, cho phép dải trời/sương **8–20 %**, nhìn xuống **12–25°** cho shot toàn cảnh; giữ ≥ 50 % chỉ cho cảnh phố cận/thẳng xuống. Điều phối so V7C ↔ **V7C-lai** ↔ đối thủ trước khi chốt | chấm mù: lai 7,0 craft, 6/9 hạng nhất; V7C chặt 3,9; tránh "board game" | nới luật vừa đặt; nội dung khung lai 14–25 % | §11.4, mọi shot timelapse | nếu đối thủ thắng nhờ khung kín mái thì lai lại thua — cần so thật |
| V7C-D2 | Duyệt **`opt.nc` + `bakes` theo năm** làm mặc định T3 (tắt = V7B bit-giống) | kiểm bit 6/6; nướng một lần/mốc | +2,3 h/5 lightmap | đường ống T3 | lightmap theo một hướng nắng |
| V7C-D3 | Giữ **H2T góc thumbnail** trong phim (câu 0f) | hứa thumbnail có trong phim; chấm mù bờ + chiến sự 3/3 hạng nhất | 5 s lướt thấp | TL-2, đóng gói | — |
| V7C-D4 | **Q3 "đói" cần vật có nguồn mới** (ví dụ hàng người nhận khẩu phần, chợ vắng, giá trứng 6 pence trên bảng giá) — giao tra nguồn trước (S052 chỉ có hái rau dại) | Q3 kẹt 3/6 qua 5 lượt dù cận người 12–25 m | cần nguồn bậc 1–3 | C3 | thêm vật không nguồn là phạm luật |
| V7C-D5 | Hỏi K: **NC-H1 "lớp nhà khai"** và **SACH-1 "không log chữ"** cho cảnh `tl/*` — tên trường để khai | gỡ 5 lỗi Chặn có thể là thiếu khai | — | checks | — |
| V7C-D6 | Bài học (phiên P ghi BAI-HOC): (a) spline Hermite vọt dưới đất khi khoá cận kề khoá cẩu cao → khoá giữ 0,02 s; (b) Blender `/opt/bpy` thiếu `imageio` cho `nc_blend.py nuong`; (c) cúi > 35° ở cận ≤ 25 m đọc thành "ngã"; (d) nhìn nam/tây ở trưa → lều ngược sáng; (e) thẻ chương phải khai `p.the_chuong` (k2check), `p.chuong` chỉ để dựng | tránh lặp | — | BAI-HOC | — |

## §12 Việc chờ chủ dự án
1. **Xem tắt tiếng ≈ 2 phút** `reports/v7c/ban-thu/v7c-xem-khong.mp4` và chấm 8 câu XEM CÂM (K116-D2: cần chủ dự án ≥ 6/8) — ghi vào `channel-k2/k2c-t3-01/v7p/xem-cam-v7c.json` (phiên P).
2. **Điều phối đặt khung cổng V7C và V7C-lai cạnh đối thủ** (`reports/v7c/khung/`, `khung/lai/`, tờ `to-so-khung.jpg`) rồi **quyết V7C-D1** (luật bố cục).
3. Quyết V7C-D2…D5; duyệt bậc 5 các vật nền phụ mới (§2.4: hàng ngựa, khói bếp, người đi, cây/đèn/xe phố 2026).
4. **Ghi RIGHTS/AUTHORSHIP (phiên P):** Drinkwater 1786 (archive.org `historyoflatesie00drin`, PD; OCR SHA `d17a7894…`) — dùng làm nguồn số ngựa (dòng 4177) và hái rau (dòng 4723); OSM 2026 (ODbL) cho tuyến cây/đèn/xe; 18 vân Poly Haven CC0 (như NC-CPU); nhạc tạm Tyrant.mp3 (K2-MUS); quyết định sáng tạo trong lệnh V7C (20/10 21:22: góc thumbnail vào đoạn pin nổi; trại dày theo Faden; máy gần hơn).
5. Phiên P merge nhánh này khi duyệt. Nhánh **không** merge.

**DỪNG — chờ chủ dự án.**
