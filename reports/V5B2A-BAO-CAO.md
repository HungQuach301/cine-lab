# V5b-2a — Mô-đun xương sống thời gian: llvmpipe + ngữ pháp máy + số liệu cho bộ kiểm 1.12 — BÁO CÁO

> Phiên V5b-2a, 16/10/2026, theo lệnh chủ dự án duyệt 16/10 (GG1–GG4, HH2, HH3, JJ1–JJ2, KK1). Nhánh `v5b2a` tạo từ `origin/v5b1b` @ `e8092a1`. **Không merge. DỪNG chờ chủ dự án.**
> Mọi số là số đo thật trong phiên (tệp ở `channel-k2/k2c-t3-01/v5b1-thu/v5b2a/do/`) hoặc ghi rõ **(ước)**. Email người dùng không xuất hiện trong repo/báo cáo.

## 0. Khối điều lệ (lệnh + thực tế)
| Trường | Lệnh | Thực tế |
|---|---|---|
| Loại phiên | V (bộ công cụ hình) | đúng |
| Nhánh | `v5b2a` từ `origin/v5b1b` @ `e8092a1` | đúng; đẩy `v5b2a`, không merge (nhánh harness `claude/magical-galileo-x0whc7` không dùng — lệnh nêu rõ tên nhánh) |
| Tệp được sửa | CHỈ `design/k2v/tl/**`, `scripts/k2tl/**`, `channel-k2/k2c-t3-01/v5b1-thu/**`, `reports/V5B2A-BAO-CAO.md` | chỉ 4 vùng này (§11). Không sửa `scripts/k2/**`, `design/k2v/` ngoài `tl/`, `scripts/env/**`, `checks/**`, nhánh tập. Không ghi RIGHTS/AUTHORSHIP/COST-LEDGER (đề xuất §10) |
| Đọc nhánh khác | `origin/gpu-rd`, `origin/checks/v1.12`, `origin/k2c-t2` | chỉ `git show` / `git archive` / worktree tạm ngoài repo; không sửa. Mã `checks/` **không đọc** — chỉ chạy `q_tl.py`/`q_hinh.py` và đọc bảng định nghĩa trường ở đầu `q_tl.py`/`q_hinh.py` (RULES-LL 1.12.0 chỉ định phiên xưởng đọc bảng này) |
| Trần | Claude API ≤ $2 (ghim model) · ElevenLabs 0 · YouTube 0 · giờ máy ≤ 4 h · chỉ CPU | **$0** (không gọi API; không có `cost.jsonl`) · **0** · **0** · **≈ 2,3 h** (§9) · chỉ CPU |
| Preflight | BẮT BUỘC | hook pre-commit/pre-push cài đầu phiên; mọi commit ĐẠT, `lock.py --verify` KHỚP (§11) |
| Điều kiện dừng | xong việc → đẩy → dừng | (1) xong việc |

## 1. Tóm tắt (đọc 1 phút)
1. **llvmpipe là trình dựng mặc định (GG1)** qua `K2TL_GL` (`llvmpipe` | `swiftshader`); mỗi lượt đọc `UNMASKED_RENDERER` và **DỪNG mã 6** nếu sai trình dựng (có test cờ sai); renderer ghi vào mọi log. `scripts/k2tl/env_check.sh`: Mesa 25.2.8 / LLVM 20 **ĐẠT**. Test chạy được cả hai trình dựng: **TẤT CẢ TEST ĐẠT**.
2. **Ngữ pháp máy (JJ1, KK1):** preset `lien-hoan` + 6 preset (push-in giữ hơi, boundary trace dọc biên giới OSM thật có hai bên tô theo số, follow-object xe A-lite, lateral parallax, top-down rise, vertigo). Mỗi cú khai `vai`, log năm/s, °/s, AGL theo loại tuyến (HH2), thời lượng orbit, SPP theo pha. **7/7 cú đạt mọi giới hạn** (§3).
3. **Gibraltar mới (llvmpipe, 24,5 s):** 7,8–22,8 s là MỘT cú liên hoàn: bay ≈ 100 m trên WCA (lệch ≤ 8,9 m) → speed ramp → orbit 5 s quanh giao lộ + trạm biên giới (năm dừng 1941 **1,79 s**, hero trung vị **27,1 %**) → crane up → reveal ×12,4. Đoạn thử dài hơn 20 s vì **năm ≤ 10 năm/s** trong cú (không chứa nổi 1896 → 2026 trong 12 s) — chờ chủ dự án duyệt (§4).
4. **Bộ kiểm 1.12 CHỈ BÁO:** TL-Q2 **ĐẠT** (V5b-1b TRƯỢT), TL-Q3, TL-Q5 (V5b-1b TRƯỢT), TL-Q6 **ĐẠT**; TL-Q4(b) lệch đường dẫn đo được: **0,195 %** rộng khung. Còn TRƯỢT: TL-Q1(c) sáng công trình 0,59 < 1,5; TL-Q4(a) dòng RIGHTS (P ghi); BC1(a) eo đất trống 1896–1941; MAU1 chi tiết ở khung bay thấp/orbit (§5).
5. **Chuẩn hình 8 khung (không chữ):** trung vị bão hoà **0,429 → 0,445**, colorfulness **45,5 → 45,6**, chi tiết **18,3 → 18,2**, cháy 0 %. Hai khung bay tuyến và khung mốc đinh (góc máy mới, thấp) chi tiết **11,3–14,0 < 16** (§5.2).
6. **Giờ máy:** lượt trọn 1080p **1,594 s/khung** trên máy này — máy này **chậm nhất từng đo** (bench chuẩn V5b-1b: ×1,52 máy C, ×1,08 máy B). Bản đồ nổi llvmpipe **0,460 s** (SwiftShader 0,879), nhà máy **0,54 s** (1,21), hình khớp tiêu chí chặt + cấu trúc 18/18 khung. **Tập 10 phút kịch bản 3 + 2 cú liên hoàn: ≈ 4,3 h máy này / ≈ 2,8 h máy C (ước)**; thêm mặt nạ mọi khung ≈ 0,9 h → **ĐẠT ≤ 12 h** (§7).
7. **Hai lỗi hình có từ V5b-1, đã sửa:** (a) **mảng tam giác đen trên vách bắc Rock** — vòng chân trời 150 m nội suy qua vách 400 m đâm xuyên lưới mịn; (b) vòng mốc thời gian bỏ sót mốc cuối (máy đứng yên 1–2 khung cuối cú). Thêm chi tiết cận cảnh: cụm cỏ, vệt bánh xe đường đất, cốt liệu/mảng vá/đường nối nhựa đường băng (§4.3).

## 2. llvmpipe (việc 1, GG1)
| Hạng mục | Làm | Số đo |
|---|---|---|
| Chọn trình dựng | `scripts/k2tl/render.js`: `K2TL_GL=llvmpipe` (mặc định; `--use-gl=angle --use-angle=gl-egl`) \| `swiftshader` (`--use-angle=swiftshader --enable-unsafe-swiftshader`) | — |
| Kiểm mỗi lượt | sau `setup` đọc `UNMASKED_RENDERER`; không khớp `/llvmpipe/` hoặc `/SwiftShader/` → in "DỪNG" + thoát **mã 6**. Test: ép cờ trình dựng kia qua `K2TL_GL_FLAGS` → render.js thoát 6 (cả hai chiều) | ĐẠT |
| Renderer trong log | `log.json` (gốc + `info`), `--campath` (gốc), `--budget` và `--maskonly` (mỗi phần tử, vì bộ kiểm đọc mảng), dòng stderr `[gl]`, dòng kết JSON | llvmpipe: `ANGLE (Mesa, llvmpipe (LLVM 20.1.2 256 bits), OpenGL ES 3.2)` |
| `scripts/k2tl/env_check.sh [--json]` | dpkg `mesa-libgallium`, `libgl1-mesa-dri` = 25.2.8, `libllvm20`; probe WebGL2 cả hai trình dựng | **ĐẠT** (`do/env_check.json`); đề xuất gắn vào `verify.sh` + `VERSIONS.yaml` ở V5b-2b (§8) |
| Test hai trình dựng | `tests/run.sh` chạy `test_browser.js` với `K2TL_GL=llvmpipe` rồi `swiftshader` | ĐẠT cả hai; chữ max 15,69 % (khung mốc đinh, ≤ 25 %), tương phản min 5,26/5,56, hero_pct mốc đinh 31,2 % |

## 3. Ngữ pháp máy (việc 2, JJ1/KK1) — `design/k2v/tl/campath.js`
- Mỗi preset trả một **cú** `{preset, vai, t, keys, phases}`; `vai ∈ {co-che, buoc-ngoat, he-qua}` bắt buộc (sai → lỗi). `grammar()` ghép cú + mốc tự do (`cuts` cho cuộn minh hoạ), `sppOf(pha)`: **fly/ramp/follow/trace → SPP1 · orbit/pin/hero → SPP4 · còn lại SPP2**. `grammarLog()` ghi mỗi khung `preset, vai, phase, spp, agl, yr_s, w, v, route_dev_m` và tổng kết mỗi cú so `LIMITS` (≤ 10 năm/s, ≤ 90 °/s, orbit 4–6 s, năm dừng 1,5–2 s) và `ALT_MAX` (HH2: `pho` ≤ 120 m; `eo_dat`/`song`/`dai_lo` ≤ 300 m; vượt → lỗi ngay khi dựng cú).
- **Liên hoàn** `lienHoan`: bay thấp dọc tuyến thật (đích xa: lệch trục ≤ 10°) → speed ramp (v = 1 + 1,4·sin²: tăng tốc rồi hãm vào orbit, đỉnh ≈ 2,4×) → orbit quanh tâm hero (id mặt nạ) → crane up (nâng thẳng, lùi ×1,35, tâm nhìn trượt) → rise-and-reveal (mốc khoá).
- Cuộn minh hoạ `scenes/presets.js` (6 cú × 4,5 s, nối bằng cắt; `v5b2a/presets_540p.mp4`, `do/presets-to-khung.jpg`, `do/presets-campath.json.gz`):

| Preset | Vai | Cảnh | năm/s max | °/s max | AGL (m) | Riêng |
|---|---|---|---|---|---|---|
| lien-hoan (gib20) | buoc-ngoat | WCA → giao lộ 1941 → La Línea/vịnh | **10,0** | 50,8 | bay 97,9–103,5 (≤ 120; eo đất ≤ 300) | bay 3,0 s lệch max 8,92 m; orbit 5,0 s; năm dừng 1,79 s; SPP 1/4/2 |
| push-in giữ hơi | co-che | Tower of Homage 1883→1900 | 3,8 | 5,7 | 58–222 | hold 1,3 s trôi 1 % quãng (không đứng yên); SPP 2→4 |
| boundary trace | he-qua | biên giới OSM admin_level=2 (760 m, 2 quan hệ) 1960→2004 | **9,87** | 76,2 | 94–95 (eo đất) | lệch tuyến max 1,24 m; hai dải màu theo **số toà đang đứng** mỗi bên (La Línea Catastro / Gibraltar mốc; `build_border.py`) |
| follow-object | co-che | xe A-lite 1941 chạy 11 m/s trên WCA | 0,3 | 40,0 | 13 | giữ khoảng cách máy–xe (test ±0,5 m) |
| lateral parallax | he-qua | trước La Línea 1990→2026 | 8,1 | 4,8 | 110 | chuyển động ⟂ trục nhìn (test < 2 %) |
| top-down rise | buoc-ngoat | giao lộ 1937→1945 (đường băng xuất hiện) | 1,8 | 0,05 | 260→1 300 | nhìn xuống 89,5° |
| vertigo | buoc-ngoat | tháp 1980→2020 | 9,0 | 0 | 127–234 | fov 20,9° → 8,7°, bề rộng chủ thể lệch **0,09 %** |

- Ngoài cú liên hoàn, đoạn 0–7,8 s của gib20 giữ nhịp V5b-1b (không phải preset): năm chạy tới **40 năm/s** (6,2–7,0 s) — không thuộc giới hạn preset; nêu để chủ dự án biết.

## 4. Gibraltar mới (việc 4–5)
### 4.1 Nhịp (`scenes/gib20.js`, 588 khung, 24,5 s)
| Giây | Năm | Pha (preset) | Máy / chữ |
|---|---|---|---|
| 0–7,4 | 1704→1886 | tự do (như V5b-1b) | thẻ 1704 0,1–3,25 s (hiện 3,12 s); dòng phương pháp 2 dòng 0–4,45 s; **"≈ = interpolated between counts" 3,3–6,0 s (HH3)**; thẻ Tower 4,5–7,65 s (3,12 s) |
| 7,8–10,8 | 1896→1925 | **fly** SPP1 | bay ≈ 100 m dọc WCA, nhìn La Línea (lệch trục 4,4°), ống 26°; ảnh LoC 7,9–11,3 s (**hiện 3,42 s**, ≥ 3,0) |
| 10,8–11,6 | →1933 | **ramp** SPP1 | 80 → 260 m/s → vào orbit |
| 11,6–16,6 | →1941 · **dừng 12,4–14,2** · →1964 | **orbit** SPP4 (5,0 s, 156°: nam → tây → bắc-tây bắc) | r 95 m, cao 38 m; thẻ 1941 12,2–15,6 s; năm phóng 1,45×; nhìn bắc thấy hàng xe + trạm biên giới + La Línea, rồi vòng sang nhìn Rock + phố |
| 16,6–17,8 | →1976 | **crane** SPP2 | nâng 38 → 240 m |
| 17,8–22,8 | →2026 | **reveal** SPP2 | 268 → 3 325 m (×12,4) |
| 22,8–24,5 | 2026 | màn kết | dòng nguồn bản đồ; số đếm "37,936 residents (2022)" + dòng nguồn **role `index_src`** "Count: Census of Gibraltar 2022, Table 1" |

- **Quyết định không dừng hỏi:** cú liên hoàn phải giữ ≤ 10 năm/s ở mọi pha → 1896 → 2026 cần ≥ 12,6 s chuyển động + 1,8 s năm dừng → đoạn thử 24,5 s (V5b-1b: 20 s, reveal 13,5 năm/s). Phương án khác (chờ chủ dự án): chỉ áp ≤ 10 năm/s cho pha bay tuyến → giữ được 20 s. Năm/s = **10,0 đúng ngưỡng** (nêu §6).
- Chỉ số dân **không loé số đếm** khi năm chạy qua năm điều tra (V5b-1b hiện số đếm 1–2 khung); số đếm chỉ hiện từ năm điều tra cuối, kèm dòng nguồn riêng.
- Âm: `v5b2a/cues.json` (cùng 4 SFX + nhạc của V5b-1, dòng RIGHTS có sẵn), master **−14,5 LUFS / −1,9 dBTP** (1080p), −1,8 dBTP (540p) sau AAC (hạ 0,5 dB để true peak ≤ −1,5).
- Ra: `v5b2a/gib20_540p.mp4` (**4,59 MB**, commit thường) · **1080p ngoài git** `/var/tmp/cine-out/v5b2a/gib20_1080p.mp4` (150,8 MB, SHA-256 `89738ce9ea38bdc7caa2d4015e7da78e14e593e4ccdda854430aac6a73110368`) · 8 khung 1080p có chữ `v5b2a/khung/` + không chữ `v5b2a/khung-khong-chu/` · tờ khung `do/to-khung-24s.jpg` · trước/sau `do/truoc-sau-8-khung.jpg`.
- Dựng lại khung 0–199 sau khi sửa cửa sổ thẻ (TL-Q5c): phần hình **trùng byte** với lượt trọn (kiểm khung 60/150/199) — ghép an toàn.

### 4.2 Sửa theo K/HH (việc 4)
| Mục | V5b-1b | V5b-2a |
|---|---|---|
| Thẻ ảnh LoC (TL-Q5c) | 2,96 s | **3,42 s**; mọi thẻ 3,12–3,42 s, có khoảng trống giữa hai thẻ liền nhau (q_tl ban đầu tính thẻ Tower + ảnh là một thẻ 6,5 s → đã tách) |
| Dòng phương pháp HH3 | — | "≈ = interpolated between counts" 3,3–6,0 s; tấm nền gọn (cao 64) để giữ ≤ 15 % |
| Bay WCA (TL-Q2/HH2) | 273–308 m → TRƯỢT | **97,9–105,6 m**, lệch TB 0,41 / max 8,92 m, 3,0 s → **ĐẠT** |
| Ảnh LoC cắt | V5b-1 không ghi cách cắt | `fetch_sources.py` ghi hộp cắt `(70, 66, 3315, 1611)` (tìm lại bằng đối khớp với 540p V5b-1b, tương quan 0,987); SHA mới trong `do/sha256.txt` |

### 4.3 Chất lượng hình đã sửa trong phiên
- **Tam giác đen trên vách bắc Rock** (cũng có ở V5b-1b): mặt nạ cho thấy là địa hình; nguyên nhân: ô 150 m của vòng chân trời (ảnh vệ tinh — vách trong bóng = đen) và ô 60 m lưới ngoài nội suy qua vách ≈ 400 m nên đâm xuyên lưới 20 m dù đã hạ 40–60 m. Sửa: bỏ ô lưới thô nằm trọn trong vùng lưới mịn (`terrain.js`). Phụ: −9 % thời gian khung (1,752 → 1,594 s).
- Cận cảnh bay thấp/orbit: cụm cỏ 0,7–1,5 m + hạt cỏ + bụi thấp lẻ (mờ theo kích thước điểm ảnh, không răng cưa) cho cỏ khô/đồng cỏ eo đất; đường đất trước 1935–50: hai vệt bánh xe, loang ổ gà, lề cỏ; nhựa đường băng: cốt liệu, mảng vá, vết dầu, đường nối thi công 7,5 m; viền mốc đinh mảnh hơn (3 m → 1,4 m).
- Bố cục orbit chọn bằng số (3 phương án đo): r 120/h 48 hero 20 %; r 80/h 32 bão hoà 0,17 ở một khung; **r 95/h 38: hero 27,1 %, mốc đinh bão hoà 0,40 / colorfulness 35,3** (chọn).

## 5. Số đo + bộ kiểm 1.12 CHỈ BÁO (việc 3, 5)
### 5.1 Số liệu xuất cho bộ kiểm (K §7.1) — `v5b2a/do/` (216 KB, `scripts/k2tl/tl_bundle.py`)
| Tệp | Nội dung |
|---|---|
| `noi-dung-mask.json.gz` | mặt nạ **MỌI** khung (588): `content_pct`, `fabric_pct`, **`hero_pct`** + `hero_id` (crossing/tower), `hero_pct_by_id`, pha, renderer. Id hero = kênh B mặt nạ (`heroes.heroIds`) |
| `log-chu.json` | log chữ **mọi khung có thẻ/ảnh/nhãn neo** + mỗi 24 khung (s, role, px1080, words, ratio); role riêng **`index_src`** cho dòng nguồn số đếm |
| `anchor-dev.json` | 267 đường dẫn neo / 258 khung: đầu đường dẫn ↔ điểm 3D chiếu lại ĐỘC LẬP từ campath (`anchor_dev.py`): **max 0,195 %** rộng khung (nhãn tag), thẻ 0,048 %, ảnh 0,005 % — ≤ 1 % |
| `campath.json.gz`, `text-budget.json.gz`, `render-log.json.gz`, `nhan-sang.json`, `goi-canh-meta.json`, `bo-tl.json` | campath = grammarLog; ngân sách chữ + vai + đường dẫn mọi khung; log dựng; sáng công trình mốc đinh (TL-Q1c); bộ timelapse cho `q_tl.py` (`neo_px_loi`, `nhan_sang`) |

### 5.2 Bảng TRƯỚC (V5b-1b) → SAU (V5b-2a), 8 khung 1080p không chữ (`measure_look.py`, vùng giữa, 640×360)
| Khung (số, năm) | Bão hoà | Colorfulness | Chi tiết | Cháy | Nội dung hình học | hero_pct |
|---|---|---|---|---|---|---|
| toàn cảnh 1 · mở đầu (10, 1710) | 0,427 → **0,447** | 80,2 → **80,2** | 20,5 → **21,2** | 0 % | 17,1 → 17,1 % | — |
| toàn cảnh 2 · kết (580, 2026) | 0,447 → **0,443** | 90,4 → **89,7** | 34,0 → **34,1** | 0 % | 31,8 → 31,7 % | — |
| cận hero 1 · Tower (168, 1882) | 0,408 → **0,420** | 46,1 → **46,0** | 18,6 → **19,8** | 0 % | 42,7 → 42,7 % | tower 3,0 % |
| **cận hero 2 · mốc đinh 1941 (320, orbit — góc mới)** | 0,388 → **0,404** | 39,0 → **35,3** | 15,9 → **11,3** ✗ | 0 % | 18,7 → **32,9 %** | **crossing 31,2 %** |
| **eo đất 1 · bay WCA (214, 1907 — góc mới)** | 0,435 → **0,455** | 36,6 → **45,1** | 15,8 → **13,6** ✗ | 0 % | 20,9 → **6,8 %** | — |
| **eo đất 2 · nhìn La Línea (250, 1921 — góc mới)** | 0,435 → **0,451** | 37,7 → **44,9** | 17,3 → **14,0** ✗ | 0 % | 22,6 → **7,7 %** | — |
| phố cổ 1753 (77) | 0,408 → **0,424** | 52,2 → **52,7** | 26,3 → **27,1** | 0 % | 33,5 → 33,5 % | — |
| cận hero 3 · tháp + phố (172, 1885) | 0,431 → **0,455** | 44,8 → **45,0** | 18,0 → **16,6** | 0 % | 32,6 → 30,2 % | tower 6,3 % |
| **Trung vị** | **0,429 → 0,445** | **45,5 → 45,6** | **18,3 → 18,2** | 0 % | | |
- Mục tiêu bão hoà ≥ 0,35: **8/8**; colorfulness ≥ 35: **8/8**; cháy ≤ 1 %: **8/8**; chi tiết ≥ 16: **5/8**.
- Vì sao chi tiết thấp ở 3 khung góc mới: máy ở 38–100 m nhìn đồng trung lập c.1900–1941 — đất trống thật (Baedeker 1913 vẽ trống) và mặt nhựa lớn; đã thêm vi chi tiết vật liệu (§4.3: +0,4 đến +1,5 điểm) nhưng **không thêm vật thể chỉ để vượt ngưỡng**. 24 khung mẫu (mỗi giây, `do/mau24.json`): nhóm Chặn MAU1 (bão hoà/colorfulness/cháy) **18/24**; trượt: 180 (chuyển cảnh, colorfulness 33,4), 276 (ramp, 32,3), 348/372 (orbit nhìn vách bắc Rock trong bóng, bão hoà 0,24/0,28), 468/492 (reveal 1993–2003, phố bê tông xám, 0,19/0,34); chi tiết ≥ 16: 13/24.

### 5.3 Bộ kiểm checks 1.12 (worktree tạm `origin/checks/v1.12`, chỉ chạy) — `do/q_tl-chi-bao.*`, `do/q_hinh-*`
| Luật | V5b-1b (K-1.12 §3.2) | V5b-2a | Ghi chú |
|---|---|---|---|
| TL-Q1 mốc đinh | THIẾU (c) | **TRƯỢT (c)**: 1 mốc 1941 **1,79 s** ✓ · (c) sáng trong/ngoài công trình **0,59 < 1,5** | đường băng nhựa tối đứng giữa cỏ + trời sáng: không thể sáng hơn 1,5× mà không giả hiệu ứng phát sáng → chờ chủ dự án/K (§12) |
| TL-Q2 bay dọc phố | **TRƯỢT** (273–308 m) | **ĐẠT**: 3,0 s ≤ 15 m/≤ 120 m, max 8,92 m, cao 97,9–105,6, đích 4,4° | |
| TL-Q3 reveal | ĐẠT | **ĐẠT**: zoom-in ×10,4 / 4,2 s; kéo lùi ×12,4 / 5,0 s | |
| TL-Q4 ảnh lịch sử | TRƯỢT (a), THIẾU (b) | **TRƯỢT (a)** RIGHTS.md chưa có dòng LoC 2025710366 · (b) đo được (`neo_px_loi`), không lỗi | (a) là việc của P (ngoài vùng) |
| TL-Q5 ngân sách chữ | TRƯỢT (c) 2,96 s | **ĐẠT**: thường max 14,8 %, mốc đinh 15,2 %, vùng giữa 0, chữ ≥ 38 px, tương phản min 8,11 | |
| TL-Q6 năm giả | THIẾU (La Línea) | **ĐẠT** (2 lớp tầng chuẩn) | lớp La Línea vẫn chỉ có tổng (như V5b-1b) — bộ do tôi lập không khai lớp đó |
| BC1 bố cục | THIẾU (10 khung) | **TRƯỢT (a)**: 588/588 khung; quãng < 30 % liên tục: 0–2,83 s (toàn cảnh mở 1704, thấp nhất 15,6 %) và **7,2–12,2 s (5,0 s; bay eo đất 1890–1941, thấp nhất 2 %)** · (b) hero orbit 279–398: **không lỗi** (trung vị 27,1 %) | eo đất trống thật 1896–1941 — cùng câu hỏi V5B1B §12.2 |
| MAU1 | THIẾU (khung có chữ) | **TRƯỢT** chi tiết 3/8 khung (trên) | nhóm Chặn đạt 8/8 |

## 6. Chỉ số trong ±5 % quanh ngưỡng (luật cứng)
| Chỉ số | Đo | Ngưỡng | Lệch |
|---|---|---|---|
| Năm/s cú liên hoàn | 10,0 | ≤ 10 | 0 % (đúng ngưỡng, theo thiết kế) |
| Năm/s boundary trace | 9,87 | ≤ 10 | −1,3 % |
| Ngân sách chữ khung thường max | 14,85 % (35 khung trong 14,25–15,75 %) | ≤ 15 % | −1,0 % |
| Colorfulness khung mốc đinh 320 | 35,3 | ≥ 35 | +0,9 % |
| Colorfulness khung mẫu 300 / 324 | 36,0 / 35,6 | ≥ 35 | +2,9 / +1,7 % |
| Bão hoà khung mẫu 492 | 0,341 | ≥ 0,35 | −2,6 % (TRƯỢT) |
| Chi tiết khung 172 | 16,6 | ≥ 16 | +3,8 % |
| Thẻ 1704 / Tower hiện | 3,12 s | ≥ 3,0 s | +4,0 % |
| hero_pct orbit trung vị (sau 1941) | 27,36 % (min 24,71 %) | ≥ 25 % | +9 % (min −1,2 %) |
| BC1 khung 63–69 | 28,6–30,3 % | ≥ 30 % | −4,7…+1 % |
| Dòng nguồn | 38 px | ≥ 38 px | 0 % |
| Âm true peak 540p | −1,8 dBTP | ≤ −1,5 | biên 0,3 dB |

## 7. Giờ máy (việc 7)
### 7.1 Hệ số máy — bench chuẩn V5b-1b §7.1 (khung 470, SPP2, SwiftShader, mã V5b-1 @ `ad3a40d`, lấy lần 2; `do/bench-chuan-470.jsonl`)
| Máy | Khung 470 | Hệ số so C |
|---|---|---|
| C (V5b-1b) | 3,09 / 3,14 s | 1 |
| B (V5b-1, "máy chậm") | 4,35 / 4,45 s | ×1,41 |
| **D (máy phiên này)** | **4,70 / 4,76 s** (lượt sạch; lượt đầu bị lẫn tải 7,6–8,0 s — bỏ) | **×1,52** (chậm hơn B ×1,08) |
### 7.2 Đo trên máy D (llvmpipe, 1080p)
| Đo | s/khung |
|---|---|
| gib20 trọn 588 khung (lượt cuối) | **1,594** (lượt trước khi sửa lưới thô: 1,752) |
| theo SPP: SPP1 / SPP2 / SPP4 | 1,042 / 1,329 / 2,209 |
| cú liên hoàn (khung 200–547) | 1,58 (fly 1,07 · orbit/pin 2,21 · crane 1,32 · reveal 1,37) |
| mặt nạ mọi khung (lượt riêng, 960×540) | 0,325 |
| bản đồ nổi `relief/map` (k2c-t2, `scripts/k2/hero.js`) SwiftShader → llvmpipe | 0,879 → **0,460** (×1,91) |
| nhà máy `k2g01/mill` qua `scripts/k2/hero.js` / `scripts/ll/hero.js` | 1,214 → **0,543** / 1,178 → **0,557** (×2,2) |
| cuộn preset 540p (648 khung) | 0,933 |
### 7.3 Ngoại suy tập 10 phút (14 400 khung) — kịch bản 3 (70 % 3D + 30 % relief) + 2 cú liên hoàn × 15 s
| Thành phần | Khung | s/khung (D) | Giờ D |
|---|---|---|---|
| 2 cú liên hoàn | 720 | 1,58 | 0,32 |
| 3D còn lại (SPP4 5 % · SPP1 15 % · SPP2 80 % như V5b-1b kịch bản 2) | 9 360 | 1,330 | 3,46 |
| relief/2.5D llvmpipe | 4 320 | 0,460 | 0,55 |
| **Tổng dựng** | 14 400 | | **4,33 h** |
| + mặt nạ mọi khung 3D (cho BC1) | 10 080 | 0,325 | +0,91 → **5,24 h** |
| Nếu cả tập 3D có nhịp SPP như gib20 (1,594) | | | 5,01 h (+0,91 mặt nạ) |
- Máy C (÷1,52, **ước** — hệ số đo bằng SwiftShader, áp cho llvmpipe): **2,85 h** dựng / 3,45 h kèm mặt nạ. Máy B (÷1,08): 4,0 / 4,9 h. Máy chậm nhất đã đo là chính máy D: **4,3 h / 5,2 h**. Trần 12 h: **ĐẠT** mọi máy, không cần GPU. (GPU-RD ước 5,4/7,7 h với relief SwiftShader 1,98 s; số mới thấp hơn vì relief cũng chạy llvmpipe.)

## 8. Việc cho V5b-2b (sau T2 G2) — điểm gắn chính xác (mã `origin/k2c-t2` @ `382eeef`)
1. **`scripts/k2/hero.js:52`** `chromium.launch` (SwiftShader cứng) → chọn cờ theo `K2TL_GL` + kiểm `UNMASKED_RENDERER` + DỪNG mã 6 (chép `scripts/k2tl/render.js:13–16, 41–43`); ghi `renderer` vào `meta.json` (dòng 84) — KHOP1(a)(b). Tương tự **`scripts/ll/hero.js:13`**.
2. **`scripts/k2/hero.js:10`** chọn trang `PAGE`: thêm nhánh `tl/<cảnh>` → `design/k2v/tl/page.js`, route `/cache/` → `K2TL_CACHE`. Trang tl cần thêm (vùng V, làm ở V5b-2b) `window.finalize(f)` (RGB không chữ) và `window.anchorsAt()` (tháp, giao lộ, điểm ảnh LoC) vì vòng dựng hero.js dòng 74–76 gọi hai hàm này.
3. **`scripts/k2/hero.js:67`** `spp: +arg('spp', 1)` cố định → với cảnh tl lấy `state(t).spp` (`sppOf` theo pha) mỗi khung.
4. **`scripts/k2/render.js:77`** `.log.json`: gom `renderer` từ `meta.json` của mọi plate (dòng 28–30) để KHOP1(b) bắt trộn trình dựng trong một tập; dòng 18 (`--disable-gpu`, canvas 2D) không đổi.
5. **`scripts/k2/lib/k2.js`**: `TPL.plate` (293–303) thêm lớp 2D `tl` — năm dưới-trái + chỉ số "≈" + phóng 1,45× mốc đinh, dòng phương pháp HH3, `index_src`, thẻ neo qua `anc()` (67) + log đường dẫn; `srcLine` (51) cho dòng nguồn số đếm. Chuyển logic từ `design/k2v/tl/text.js`.
6. **`scripts/k2/prep.py`**: `shot_type` (96–101) nhận `tl/…` (scene3d hoặc `timelapse` — đề xuất K §7.4); `resolve_cams` (60–77) nhận preset `lien-hoan`/… làm `camera_id`; `CODE` (22) thêm `design/k2v/tl/*.js`, `scripts/k2tl/render.js` vào dấu cảnh; khai `tl: true` + `cau` (ML1).
7. **LUT A** vào `design/k2v/page.js` (`GRADE` 10–41, `createPipeline` 57): `lut.js` + `uLutMode` 1 (chỉ vùng tối + vibrance 0,35).
8. **Công tắc GPU**: cùng biến `K2TL_GL` thêm giá trị `vulkan`/`egl-gpu` (cờ trong `research/gpu/gl_flags.js`), kiểm renderer phải KHÔNG chứa llvmpipe/SwiftShader.
9. **`scripts/env/verify.sh`** (sau dòng 23, mẫu `ok/ko`): gọi `bash scripts/k2tl/env_check.sh`. **`scripts/common/versions.py`**: `GROUPS` (19–20) thêm `'k2tl': ['design/k2v/tl', 'scripts/k2tl']`; khối thông tin môi trường (dòng 78–89: playwright, chromium) thêm `mesa_libgallium`, `libllvm20` → `VERSIONS.yaml`.

## 9. Chi phí
| Khoản | Trần | Thực tế |
|---|---|---|
| Claude API | $2 | **$0** (không gọi; không có `cost.jsonl`) |
| ElevenLabs / YouTube | 0 / 0 | 0 / 0 |
| Giờ máy | ≤ 4 h | **≈ 2,3 h** (ước theo log): 4 lượt dựng trọn 1080p (1 bị dừng sớm khi sửa mã) ≈ 75 phút gồm mặt nạ/ngân sách/khung mẫu; dựng lại 200 khung 7 phút; khung thử bố cục/vật liệu ≈ 15 phút; cuộn preset 10 phút; test ≈ 8 phút; mã hoá ≈ 8 phút; tải + dựng gói cảnh 3,5 phút; việc 6 ≈ 3 phút; bench 1 phút |
| Mạng | — | ≈ 1,3 GB (dữ liệu thô V5b-1 — **10/10 + Baedeker KHỚP SHA**, OSM 70 MB, DEM 3DEP 1 ô) |
| Đĩa tạm | — | worktree `checks/v1.12` 3,7 GB + bản trích k2c-t2 0,8 GB (scratchpad, xoá cuối phiên) |
Đề xuất dòng `COST-LEDGER.csv` (P ghi): `V5b2a,llvmpipe + ngữ pháp máy + số liệu checks 1.12,V,2026-10-16,,,,,0,2,—,0,0,≈ 2,3,,0,24.5,,reports/V5B2A-BAO-CAO.md,YouTube 0; không merge`

## 10. Đề xuất ngoài vùng (chưa ghi)
1. `RIGHTS.md`: dòng LoC 2025710366 (TL-Q4a — vẫn TRƯỢT); Baedeker 1913 (V5B1B §10); **dữ liệu ranh giới OSM admin_level=2** (ODbL, cùng dòng OSM hiện có).
2. `tools/lfs-allow.txt`: `channel-k2/*/v5b1-thu/**/*_1080p.mp4` (150,8 MB).
3. `AUTHORSHIP.md`: quyết định sáng tạo chờ duyệt — cú liên hoàn (đường bay, orbit 156°, crane, reveal), đoạn thử 24,5 s, số đếm chỉ hiện ở năm điều tra cuối, cuộn 6 preset.
4. `channel-k2/.gitignore`: `!k2c-t3-01/v5b1-thu/**/*.json` (phiên này `git add -f`).
5. `scripts/env/setup.sh`: `imagecodecs` (thiếu lại trong container mới — `build_rasters.py` dừng).
6. Bài học (đề xuất `BAI-HOC-LL.md`, P ghi): (a) vòng `for (t = t0; t <= t1; t += dt)` bỏ sót t1 khi (t1−t0) không chia hết dt → máy đứng yên cuối cú; (b) chú thích `//` nuốt mã lần 4 (`node --check` không bắt được khi phần bị nuốt là câu lệnh hợp lệ) — dùng `/* */`; (c) lưới LOD thô "hạ X m" không đủ ở vách đứng — phải bỏ ô; (d) `git worktree add` repo này tốn 3,7 GB — dùng `git archive` các thư mục cần.

## 11. Preflight, tệp, ghép thử
- `verify.sh` đầu phiên: 10 PASS / 3 FAIL (three.js, tifffile/pyshp, k2v node_modules — container mới) → cài theo hướng dẫn; thêm `imagecodecs`.
- Hook pre-commit/pre-push cài đầu phiên; mọi commit **PREFLIGHT ĐẠT, `lock.py --verify` KHỚP**; không dùng `--no-verify`.
- Tệp sửa so với `e8092a1`: `design/k2v/tl/` (campath, page, text, core, heroes, terrain, nature, scenes/gib20, README; mới `overlay3d.js`, `scenes/presets.js`), `scripts/k2tl/` (render.js, fetch_sources.py, tests/run.sh, tests/test_browser.js; mới `env_check.sh`, `anchor_dev.py`, `build_border.py`, `tl_bundle.py`, `tests/test_grammar.mjs`), `channel-k2/k2c-t3-01/v5b1-thu/v5b2a/**` (21 MB; tệp lớn nhất `gib20_540p.mp4` 4,59 MB), báo cáo này.
- **Test** `bash scripts/k2tl/tests/run.sh`: **TẤT CẢ TEST ĐẠT** — geo, calib, look, geom 88 tam giác, campath, **grammar (mới)**, env_check, **test_browser llvmpipe + swiftshader** (khung 320 dựng lại trong lượt khác thứ tự: khác byte, như V5b-1b; dựng tuần tự cùng thứ tự: trùng byte — §4.1).
- Ghép thử: nhánh chỉ sửa 4 vùng của chuỗi V5b-1 (không phiên khác sửa) — không xung đột với `main`, `k2c-t2`.

## 12. Việc chờ chủ dự án
1. **Xem duyệt** `v5b2a/gib20_540p.mp4` (llvmpipe) + `do/truoc-sau-8-khung.jpg`, `do/to-khung-24s.jpg`, cuộn `v5b2a/presets_540p.mp4` — cú liên hoàn và 6 preset (JJ1/KK1).
2. **Độ dài đoạn thử 24,5 s** (do ≤ 10 năm/s cho mọi pha của cú) hay chỉ giới hạn năm/s ở pha bay tuyến (giữ 20 s).
3. **TL-Q1(c) "sáng công trình ≥ 1,5"** không hợp với hero tối màu (nhựa đường băng: 0,59) — giữ luật, đổi phép đo (so với chính công trình ngoài mốc đinh), hay cho phép nhấn bằng viền/độ tương phản (K quyết).
4. **Eo đất trống 1896–1941** (BC1 5 s < 30 %; chi tiết < 16 ở bay thấp) — như V5B1B §12.2: chấp nhận vì là sự thật lịch sử, hay dựng công trình có bằng chứng (AMS 1943 / Baedeker 1913) cho North Front.
5. Duyệt **llvmpipe làm trình dựng chuẩn** (GG2 khớp cấu trúc: relief/nhà máy 18/18 khung đạt cả tiêu chí chặt) và giao K dựng lại khung vàng trên llvmpipe.
6. P ghi RIGHTS / LFS / AUTHORSHIP / COST-LEDGER / .gitignore / bài học (§9, §10).
7. Duyệt danh sách điểm gắn V5b-2b (§8) — làm sau T2 G2.
