**Nhánh thật: `checks-1-17-1`** (đúng lệnh; harness gợi ý `claude/keen-noether-xhe6sg`, không dùng). Gốc `origin/checks-1-17` @ `84ca8977` + `git merge --no-ff origin/main` @ `96b5017c` (0 xung đột) → `a6a02675`. Không merge vào `main`, không đụng nhánh khác.

# Phiên K-1.17.1 — ngưỡng EO-DAT khớp Kinh thánh §14.7 + luật EO-DAT-R4 — BÁO CÁO

> Phiên K, 21/10/2026 ≈ 15:55–16:15 UTC. Mọi số là số đo thật trong phiên; tệp số đo ở `reports/k1171/do/`.
> Email chủ dự án không có trong tệp, commit, header, URL, payload hay User-Agent nào. Phiên không gọi API nào.

## 0. Khối điều lệ và tóm tắt
| Trường | Lệnh | Thực tế |
|---|---|---|
| Loại phiên | K-1.17.1 | đúng |
| Nhánh | `checks-1-17-1` từ `origin/checks-1-17` (@84ca8977) + merge `--no-ff origin/main` (@96b5017c) | đúng; merge 0 xung đột (commit `a6a02675`) |
| Vùng sửa | `checks/**`, `reports/k1171/**` | đúng (§6). Không sửa `docs/`, `design/`, `scripts/`, `channel-*/`, sổ, `main`, nhánh khác |
| Chi phí | Claude mốc $3; API 0 | **API $0** (không gọi OpenAI / Claude API / ElevenLabs / Gemini / RunPod / YouTube; selftest_ll dùng `claude` giả có sẵn trong bộ kiểm); token phiên chính không đo được từ container, không chạm mốc theo ước lượng |
| `lock.py` (không cờ) | một lần ở cuối | **đúng một lần**, 16:05:00 UTC → 1.17.1, sau khi 10 bộ selftest đạt; mọi lần khác chỉ `--verify` |
| Preflight | bắt buộc | `bash tools/preflight.sh` (tệp stage) trước commit và `--range` trước push — **chạy thủ công**: cài hook `pre-commit`/`pre-push` vào `.git/hooks` bị bộ phân loại quyền của môi trường từ chối (lý do "Unauthorized Persistence"); kết quả preflight ở §7 |
| Force / dừng hỏi | không | không force; không dừng hỏi |
| Môi trường | `scripts/env/verify.sh` | 10 PASS, 5 FAIL (OpenEXR, three.js, tifffile/pyshp, k2v node_modules, Freesound 403) — không mục nào cần cho `checks/` |

**Tóm tắt:**
1. **EO-DAT-R1** khớp §14.7 "≥ 15–20 % khung": < 15 % → lỗi (a) **Chặn ở G2**; 15–20 % → (b) **Cảnh báo**; thiếu số đo → THIẾU (tính như (a)). Trước: một ngưỡng 25 % (K đề xuất tạm).
2. **EO-DAT-R2** khớp §14.7: "trống" = cỏ/cát không vật **> 50 %** khung (trước > 60 %); (a) liên tục ≤ 6 s (không đổi); (b) tổng giây trống ≤ **10 % THỜI LƯỢNG CHƯƠNG** (mẫu số = mọi shot log của chương; trước ≤ 1/3 thời lượng eo đất).
3. **EO-DAT-R4** (mới, đọc log): shot `loi_khong_vat_eo_dat: true` phải có `noi` ∈ {`pho`, `lau_dai`, `cang`} hoặc bản đồ phủ `ban_do_phu`; mỗi lần phủ ≤ 3 s (TL-4). Không shot khai → KHÔNG ÁP.
4. **Selftest:** k117 **96 → 130/130** (R1 10, R2 13, R4 15, cấp 15); bộ mới chạy trên mã 1.17.0 → **11 ca SAI** đúng chỗ ngưỡng đổi (ca mới thật sự phân biệt cũ/mới). k116 **144/144**, k115 **105/105**, k114 **126/126** — **giống hệt từng dòng** trước/sau. k113 64/64, k1122 37/37, k1121 48/48, k112 75/75, k2 129/129, ll 317/317.
5. **LOCK 1.17.0 `f6812dec…` → 1.17.1 `b741f617…`**, `--verify` KHỚP.

## 1. Đầu vào đã đọc
- `docs/BIBLE-KENH2.md` §14.7 (main @96b5017c, SHA tệp `14ca13aa…`), dòng 277 (R1–R4), §13.6 TL-4 (dòng 227).
- `reports/k117/K117-BAO-CAO.md` §0, §2.3, §4–§6, §9–§11.
- `reports/m3/BAI-HOC-LL.md`: không đọc (quy tắc dành cho phiên P).
- Mã: `checks/ll/q_k117.py`, `cap112.py`, `k2check.py` (đoạn 1.17), `selftest_k117.py`, `RULES-LL.md` mục 1.17.0.

**Nguyên văn §14.7 R1–R4** (chủ dự án đồng ý 21/10 21:05):
> R1 Chủ thể trên eo đất (dòng người, Línea, trại, công sự, lửa, hầm) chiếm ≥ 15–20 % khung, vẫn giữ dải chân trời mỏng, Rock không cắt mép. R2 Đồng cỏ/cát trống (> 50 % khung) ≤ 6 s liên tục và ≤ 10 % thời lượng mỗi chương. R3 Shot > 15 s chia 2–3 góc, mỗi góc có biến cố thấy được ≤ 6 s. R4 Câu lời không có vật trên eo đất → góc phố/lâu đài/cảng; bản đồ phủ ≤ 3 s (TL-4). R1–R4 thắng LOOK-2 ở shot có chủ thể trên eo đất.

## 2. Ngưỡng trước → sau (nguồn: §14.7)
| Hàng | 1.17.0 (K đề xuất tạm) | **1.17.1** | Đoạn nguồn §14.7 | Cấp 1.17.1 (G2 / animatic) |
|---|---|---|---|---|
| **EO-DAT-R1** (a) | trung vị `chu_the_pct` < **25 %** → lỗi | trung vị < **15 %** → lỗi (a) | "chiếm ≥ 15–20 % khung" — mức sàn | (a) Chặn / Cảnh báo |
| **EO-DAT-R1** (b) | — | **15 % ≤ trung vị < 20 %** → (b) | cùng câu — "15–20 %" là vùng chưa đủ mức trên | Cảnh báo / Cảnh báo |
| R1 thiếu `chu_the_pct` | THIẾU (Chặn) | THIẾU, gắn (a) → Chặn | — | Chặn / Cảnh báo |
| **EO-DAT-R2** định nghĩa "trống" | `trong_pct` **> 60 %** (TL-3) | `trong_pct` **> 50 %** | "Đồng cỏ/cát trống (> 50 % khung)" | — |
| **EO-DAT-R2** (a) | trống liên tục ≤ 6 s (K tạm) | **≤ 6 s** (không đổi số; nay có nguồn) | "≤ 6 s liên tục" | Chặn / Cảnh báo |
| **EO-DAT-R2** (b) | tổng trống ≤ **1/3 thời lượng eo đất** của chương | tổng trống ≤ **10 % thời lượng chương** (mọi shot log của chương: `chuong` ở log, hoặc `segments[].chuong` theo id shot) | "≤ 10 % thời lượng mỗi chương" | Chặn / Cảnh báo |
| EO-DAT-R3 | > 15 s: ≥ 2 góc; biến cố ≤ 6 s | **không đổi** | "Shot > 15 s chia 2–3 góc … ≤ 6 s" | Chặn / Cảnh báo |
| **EO-DAT-R4** | không có (thiếu định nghĩa) | §3 | "Câu lời không có vật trên eo đất → góc phố/lâu đài/cảng; bản đồ phủ ≤ 3 s (TL-4)" | Chặn / Cảnh báo |

Cấp theo cổng giữ cơ chế K116-D5 / 1.17.0: đặc tả `animatic: true` → mọi lỗi EO-DAT chỉ Cảnh báo; không khai → G2. R1 dùng cấp theo mục (`cap112`: Chặn `{a}`, Cảnh báo `{b}`).

## 3. EO-DAT-R4 — định nghĩa (đọc log shot)
| Trường | Kiểu | Ý nghĩa |
|---|---|---|
| **`loi_khong_vat_eo_dat`** (tên đề xuất theo lệnh) | bool | câu lời của shot nói về eo đất nhưng không có vật để thấy trên eo đất |
| `noi` (shot hoặc `p.noi`) | chuỗi | `pho` \| `lau_dai` \| `cang` hợp lệ. **`thanh_pho` coi là `pho`** (tên log và NC-H1 đang dùng cho phố — K đề xuất, xem K1171-D2) |
| **`ban_do_phu`** (tên đề xuất) | số giây \| `[t0, t1]` \| `[[t0, t1], …]` \| `{dur}` | bản đồ/tư liệu phủ lên địa hình; xét **lần phủ dài nhất** |

Luật: (a) `noi` hợp lệ HOẶC có `ban_do_phu` → đạt (a); không có cả hai → lỗi (a). (b) có `ban_do_phu` mà một lần phủ > **3 s** → lỗi (b), **kể cả khi `noi` hợp lệ** (TL-4 là trần riêng, §13.6 "tư liệu chỉ phủ … ≤ 3 s"). `ban_do_phu` không ra số giây (vd `true`) → THIẾU (b). Không shot nào khai `loi_khong_vat_eo_dat: true` → **KHÔNG ÁP** (đúng lệnh "không khai trường → không áp").

## 4. Selftest
| Bộ | Trước (cây 1.17.0, @a6a02675) | **Sau (cây 1.17.1, đã khoá)** | Ghi chú |
|---|---|---|---|
| `selftest_k117.py` | 96/96 | **130/130** | EO-DAT-R1 4 → **10**, R2 6 → **13**, R4 **15** (mới), cấp 9 → **15**; phần còn lại giữ nguyên |
| `selftest_k116.py` | 144/144 | **144/144** | `diff` đầu ra: **0 dòng khác** |
| `selftest_k115.py` | 105/105 | **105/105** | 0 dòng khác |
| `selftest_k114.py` | 126/126 | **126/126** | 0 dòng khác |
| `selftest_k113.py` | — | 64/64 | |
| `selftest_k1122.py` / `k1121` / `k112` | — | 37/37 · 48/48 · 75/75 | |
| `selftest_k2.py` | — | 129/129 | |
| `selftest_ll.py` | — | 317/317 | `claude` giả, không mạng |

**Ca mới (mỗi luật ≥ 1 đạt + ≥ 1 trượt):**
- **R1:** 28 % sạch · 20 % (đúng mức trên) sạch · 22 % sạch · 15 % (đúng mức dưới) không (a) · 17 % → (b) và không (a) · 14,9 % → (a) · 12 % → (a) · thiếu → THIẾU · không khai → KHÔNG ÁP. Cấp: 17 % ở G2 → 0 Chặn + có Cảnh báo; 12 % ở G2 → Chặn; thiếu ở G2 → Chặn.
- **R2:** không trống sạch · 4 s / chương 40 s = 10 % (đúng trần) sạch · `trong_pct` 50 % (không > 50 %) sạch · 55 % suốt 20 s → (a) · 65 % → (a) · nối qua ranh shot 3 + 4 s → (a) · liên tục đúng 6 s không (a) · 2 khúc 3 s / 40 s = 15 % → (b), không (a) · chương 2 (20 s) 3 s = 15 % → (b) · **mẫu số**: 8 s trống trong shot eo đất 20 s + shot phố 80 s cùng chương = 8 % → sạch; bỏ shot phố → 40 % → (b) · thiếu → THIẾU.
- **R4:** `noi` pho / lau_dai / cang / thanh_pho sạch · eo_dat không bản đồ → (a) · không khai noi → (a) · bản đồ 3 s (đúng trần) sạch · `[1, 3,5]` sạch · 3,5 s → (b) · `[[0, 2], [4, 8]]` → (b) · `{dur: 2}` sạch · noi pho + bản đồ 5 s → (b) · `ban_do_phu: true` → THIẾU · không khai / `false` → KHÔNG ÁP · cấp G2 Chặn, animatic không Chặn.

**Kỳ vọng k117 cũ đã đổi** (vì ngưỡng đổi, không phải luật hỏng): R1 "28 % ≥ 25 %" → "≥ 20 %"; R2 thay 3 ca dựa trên 1/3 thời lượng eo đất ("trống 4 s rồi có vật" — chương 2 nay 30 % > 10 %; "2 × 6 s / 40 s = 30 % ≤ 1/3"; "3 khúc 5 s = 37,5 % > 1/3") bằng các ca 10 %-thời-lượng-chương ở trên.

**Bộ ca mới chạy trên mã 1.17.0** (`do/selftest-k117-moi-tren-ma-1170.txt`, bỏ ca R4 vì mã cũ không có hàng): **102/113 — 11 SAI**, đúng các ca ở ngưỡng đổi: R1 20 / 17 / 15 / 22 % (mã cũ bắt "< 25 %"), cấp R1 17 % (2 ca), R2 55 % (mã cũ coi không trống), R2 (b) 15 % × 2 (mã cũ ≤ 1/3), R2 mẫu số chương (mã cũ 40 % bắt). Ca mới vì vậy không đạt "sẵn".

**Chạy luật trên fixture T3** `fixtures/k116/ep-t3/` (`q_k117.check`): MINH-HOA, R1, R4 KHÔNG ÁP; R2 ĐẠT (11 shot eo đất, trống dài nhất 0 s); R3 ĐẠT (0 shot > 15 s) — không lỗi chạy.
**Không chạy lại:** `k2check` T1/T2 và animatic T3 — đầu vào (`/var/tmp/k117/…`, timeline animatic) ở container K-1.17, không có ở đây. Tập trước T3 không đổi theo mã: `q_k117.check` trả KHÔNG ÁP khi không `ap_117`, và `k2check` chỉ thêm hàng 1.17 khi `V16`. Animatic T3 hiện chưa xuất `trong_pct` / `chu_the_pct` / `loi_khong_vat_eo_dat` (F8 của K-1.17) nên R1/R2 vẫn THIẾU (Cảnh báo ở animatic), R4 KHÔNG ÁP.

## 5. LOCK
- **Cũ:** 1.17.0 `f6812decc87a1950617e8226b73fe737c1f3438c58b88de7eb9a7e4d202bce1c` (2026-10-21T15:01:40Z).
- **Mới:** **1.17.1 `b741f617d7b2275e4039cd16eb8e967cbc99801f508090631146590bb1bc16fe`** (DATE_UTC 2026-10-21T16:05:00Z). `--verify` → **KHỚP** (sau khoá, sau selftest k117 trên cây đã khoá, trước commit).
- `lock.py` không cờ gọi **đúng một lần**, sau khi 10 bộ selftest đạt; không sửa `checks/` sau đó.

## 6. Tệp đã sửa
| Tệp | Việc |
|---|---|
| `checks/ll/q_k117.py` | hằng số R1 (15 / 20 %), R2 (> 50 %, 6 s, 10 % thời lượng chương), R4 (`R4_NOI`, `R4_ALIAS`, 3 s); R1 (a)/(b); R2 (b) mẫu số theo chương; hàng **EO-DAT-R4** + `_ban_do`; docstring nguồn §14.7 |
| `checks/ll/cap112.py` | R1 Chặn (a) / Cảnh báo (b); thêm `EO-DAT-R4`; `CONG` có R4 |
| `checks/ll/k2check.py` | hàng R4 trong bảng 1.17; chữ ngưỡng R1/R2 theo §14.7 |
| `checks/ll/selftest_k117.py` | 34 ca mới / sửa (§4) |
| `checks/ll/RULES-LL.md` | mục 1.17.1; bảng EO-DAT R1–R4 (thay "K đề xuất tạm"); tự kiểm 1.17.1 |
| `checks/cinecheck/__init__.py`, `checks/LOCK` | 1.17.1 |
| `reports/k1171/` | báo cáo này; `do/` (selftest trước/sau, bộ mới trên mã cũ) |

## 7. Preflight
Hook không cài được (§0). Chạy thủ công `bash tools/preflight.sh` trên tệp stage trước commit và `bash tools/preflight.sh --range origin/checks-1-17..HEAD` trước push; kết quả ghi trong thân commit báo cáo (lệnh dừng ngay khi TRƯỢT).

## 8. Chỉ số trong ±5 % quanh ngưỡng (luật cứng)
**Dữ liệu thật:** không có — phiên không chạy luật trên phim (§4).
**Ca selftest cố ý đặt đúng ngưỡng:** R1 15 % và 20 %; R2 `trong_pct` 50 %, trống liên tục 6 s, 4 s / 40 s = 10 %; R4 bản đồ 3 s. R1 14,9 % (−0,7 % so 15 %).
**Không thêm phần tử nào để vượt ngưỡng.**

## 9. Dòng sổ đề xuất (phiên P ghi — phiên này không sửa sổ)
- **COST-LEDGER.csv:** `K-1.17.1,"EO-DAT khớp §14.7 (R1 15/20 %, R2 > 50 % · 6 s · 10 % chương), thêm R4; LOCK 1.17.0 f6812dec → 1.17.1 b741f617",K,2026-10-21,,,,,0,3,—,0,0,0.3,,0,,,reports/k1171/K1171-BAO-CAO.md,"API 0; token phiên chính không đo được"`
- **RIGHTS.md / AUTHORSHIP.md:** không có tài sản mới. Ngưỡng lấy từ §14.7 do chủ dự án đồng ý 21/10 21:05 (đã ghi ở Kinh thánh); duyệt K1171-D* thì ghi nguyên văn + giờ.

## 10. Quyết định đề xuất
| # | Đề xuất | Ưu | Nhược | Tác động | Rủi ro |
|---|---|---|---|---|---|
| **K1171-D1** | Duyệt cách đọc R1 "≥ 15–20 %": < 15 % Chặn, 15–20 % Cảnh báo | Giữ cả hai số của §14.7; không chặn oan shot 15–19 % | Có thể chủ dự án muốn 20 % là sàn cứng | T3 G2 | Nếu ý là ≥ 20 % cứng thì shot 15–19 % lọt qua G2 (chỉ Cảnh báo) |
| **K1171-D2** | R4 nhận `noi: thanh_pho` = `pho` | Khớp tên log hiện có (NC-H1, K116) | Thêm một bí danh ngoài lệnh | log T3 | Thấp |
| **K1171-D3** | R4 (b): bản đồ phủ > 3 s là lỗi kể cả khi `noi` hợp lệ | Đúng TL-4 (trần riêng) | Lệnh viết "HOẶC" — chặt hơn chữ của lệnh | log T3 | Thấp; nếu muốn đúng chữ "HOẶC" thì bỏ 1 dòng |
| **K1171-D4** | Tên trường `loi_khong_vat_eo_dat`, `ban_do_phu` chốt cho phiên dựng (thêm vào F8 của K-1.17) | Luật đo được | Phiên dựng phải khai thủ công (tự khai) | ANIMATIC-T3-V2, bản cuối T3 | Không khai → R4 KHÔNG ÁP (lọt) |

## 11. Việc chờ chủ dự án
1. Duyệt **K1171-D1…D4**; quyết đã treo **K117-D1, D3–D8** (D2 nay được giải bằng §14.7 + phiên này).
2. Phiên P: merge `checks-1-17` rồi `checks-1-17-1` khi duyệt (nhánh này **không** merge); ghi sổ theo §9.
3. Phiên dựng T3: xuất `trong_pct`, `chu_the_pct`, `loi_khong_vat_eo_dat`, `ban_do_phu` trong log shot (F8).

**DỪNG — chờ chủ dự án.**
