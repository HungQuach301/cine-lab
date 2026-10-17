# V5b-2b — Gắn mô-đun timelapse vào dây chuyền kênh 2 + P0 cho T3 "vây hãm" + đoạn thử phố Gibraltar 1782 — BÁO CÁO

> Phiên V5b-2b, 17/10/2026, theo lệnh chủ dự án (duyệt WW5, D6, VV2, K-1.13 17/10) + **lệnh bổ sung AE** (17/10, nhận giữa phiên: ghost SH ở nhánh `claude/sh-ghost-gibraltar-t3-1gkftx`, cảnh (b) dùng ghost 1782 thật).
> Nhánh `v5b2b` từ `origin/main` @ `82a17ae`. **Không merge. DỪNG chờ chủ dự án.** Mọi số là số đo thật trong phiên (tệp ở `reports/v5b2b/`) hoặc ghi rõ **(ước)**. Email người dùng không xuất hiện trong repo/báo cáo.

## 0. Khối điều lệ (lệnh + thực tế)
| Trường | Lệnh | Thực tế |
|---|---|---|
| Loại phiên | V (bộ công cụ hình) | đúng |
| Nhánh | `v5b2b` từ `origin/main` @ `82a17ae` | đúng; đẩy `v5b2b`, không merge (nhánh harness `ccr-…` không dùng — lệnh nêu tên nhánh) |
| Tệp được sửa | `scripts/k2/**`, `scripts/k2tl/**`, `scripts/ll/hero.js`, `scripts/ll/ll.py` + `qc.py` (chỉ K-1.13 §8.3), `design/k2v/**`, `scripts/env/verify.sh`, `scripts/common/versions.py` (GROUPS + khối môi trường), `reports/V5B2B-BAO-CAO.md`, `reports/v5b2b/**` | chỉ các vùng này (§9). `checks/**` chỉ merge 1.13, không sửa, **không đọc mã** (chỉ chạy công cụ + đọc `RULES-LL.md`/báo cáo K). Không ghi `channel-k2/k2c-t3-01/**` (ghost SH chỉ đọc bằng `git show`, chép GeoJSON ra `/var/tmp/cine-out/ghost/`), không sửa `docs/BIBLE-KENH2.md`, `main` |
| Trần | Claude API ≤ $2 (ghim, chỉ chấm mù) · ElevenLabs 0 · YouTube 0 · giờ máy ≤ 8 h · llvmpipe | **$1,61** (27 lượt, ghim `claude-sonnet-5-5`) · **0** · **0** · **≈ 3,3 h** (§7) · dựng trọn trên llvmpipe (`--use-gl=angle --use-angle=gl-egl`) |
| Preflight | bắt buộc; che email | hook pre-commit/pre-push cài đầu phiên; **mọi commit + push PREFLIGHT ĐẠT, `lock.py --verify` KHỚP** (1.13.0 `d1161ebe…`) |
| Điều kiện dừng | xong → đẩy → dừng; không dừng hỏi | (1) xong việc. Câu hỏi không chặn đã tự quyết (§10) |

## 1. Tóm tắt (đọc 2 phút)
1. **Checks 1.13 đã merge** (`--no-ff`, không sửa): `lock.py --verify` **KHỚP**, selftest_k113 **64/64**. K-1.13 §8.3 đã áp: `ll.check` nhận `estimate` cho kênh 2, qc gọi `K.q7(…, est=is_k2)`.
2. **9 điểm gắn V5B2A §8 xong.** `scripts/k2tl/gl.js` dùng chung cho `scripts/k2/hero.js`, `scripts/ll/hero.js`, `scripts/k2tl/render.js`: `K2TL_GL` = llvmpipe (mặc định) | swiftshader | vulkan | egl-gpu; đọc `UNMASKED_RENDERER`, sai thì **DỪNG mã 6**; renderer vào `meta.json` và `.log.json`. Các phần gắn: trang `tl/<cảnh>`, SPP theo pha, lớp chữ tl trong `k2.js`, prep nhận tl, LUT A (opt-in), `verify.sh` + `versions.py`.
3. **Golden sau tích hợp (llvmpipe): steel KHỚP, ll08 KHỚP, t1 LỆCH CỤC BỘ 22 ô** (đúng như đã biết). Đối chứng `K2TL_GL=swiftshader` **trùng từng số với P-1710** (steel 0,978, ll08 0,9686, t1 22 ô), nên tích hợp không đổi hình. Mọi chênh lệch chỉ do đổi trình dựng (§2.3).
4. **P0 cho T3: làm đủ 6/6.**
   - AGL mỗi khung vào `meta.json` → `p.agl` trong timeline.
   - M9: bộ nạp footprint chung + mái theo 3 thời kỳ + công sự đá.
   - M12: bản đồ pha phủ địa hình, crossfade theo mốc.
   - M6: bộ đếm ngày/giờ, hai lịch O.S./N.S., mặt trời theo thiên văn.
   - M3: hạm đội theo đội hình + đường đi theo giờ.
   - M4: chiến tuyến mọc theo thời gian, có gờ đất và dải màu phe.

   **P1:** làm **M1** (mũi tên) và **M7** (khói/lửa sprite); **chưa làm M8, M11** (§3).
5. **Đầu ra cho checks 1.13 (§8.1) đủ:** `p.agl`, `fabric_pct`, `ghost_pct`, `nam_khung`, `noi` theo cửa sổ, role `where`/`ghost_src`, `*.log.json` cùng master. Luật hình VV2 cảnh báo ngay khi prep (thành phố không lớp nhà, địa cầu > 1 lần/> 3 s, shot chưa khai `noi`).
6. **Đoạn thử V5b-2b-T, 1080p, 26,0 s, 2 cảnh, phố 1782 = ghost SH thật (lệnh AE).** Dựng qua đúng dây chuyền `scripts/k2/build.sh`. Master LFS `reports/v5b2b/v5b2b-t-1080p-master.mp4`, SHA `43da3d93…`.
   - **k2check 1.13: NC-H1…H5 [bộ] đều ĐẠT.** NC-H1…H4 cấp tập ĐẠT (NC-H5 tập: không áp). TL-Q2/Q7/Q8/Q9, Q33/Q36 (1.13), Q34, Q35, Q7/Q8-K2 ĐẠT.
   - Còn TRƯỢT: Q37, ML1, Q26b, TL-Q1. Đây là đặc thù đoạn thử 2 cảnh hoặc luật chưa nhận biến cố bên trong cảnh tl (§4.4).
7. **Số đo chính:**
   - hero King's Bastion trong orbit: trung vị **29,6 %**;
   - fabric shot thành phố: trung vị **40,1 %**, thấp nhất 24,6 %;
   - AGL ≤ **0,30 km**; lửa đỏ ≤ **0,63 %** khung; neo 624/624 khung;
   - nhãn nguồn ghost hiện liền **17,5 s** từ 0,5 s.
   - **Ngoại suy tập 10 phút: ≈ 6,5 h ≤ 12 h** (§7).
8. **Chấm mù** (3 người, giao thức blind_g2):
   - vòng 1: V5b-2b-T **6,22** so gib20 **6,11**; thua P1, P4.
   - Sau khi sửa 3 lỗi chấm mù chỉ ra, vòng 2 chấm lại P1/P2/P4. Gộp: **6,39 so 6,06**.
   - **Vẫn thua P1** (bay trên vịnh: nửa dưới khung là nước) **và P4** (reveal: pin nổi nhỏ, thân đơn giản) — §4.6.

## 2. Việc 0–1: checks 1.13 + 9 điểm gắn
### 2.1 Merge checks 1.13 + K-1.13 §8.3
| Việc | Kết quả |
|---|---|
| `git merge --no-ff origin/checks/v1.13` (@ `9bf28dc`) | commit `d08aa10c`, không sửa tệp nào của checks |
| `lock.py --verify` | **KHỚP** `d1161ebee509d4d5…ecce` |
| `selftest_k113` | **64/64** |
| `scripts/ll/ll.py` (dòng 81 cũ) | `is_k2(E)` (vo_dir dưới `channel-k2/`, `channel: k2` hoặc brand MOVING PARTS) → kind ∈ actual/projection/**estimate**; LL giữ 2 loại. T2 `ll.check` 0 lỗi; 4 fixture LL vẫn 0 lỗi |
| `scripts/ll/qc.py` (dòng 125 cũ) | `K.q7(E, TL, logs, est=ll.is_k2(E))` (chữ ký `q7(E, TL, logs, est=False)` đọc bằng `inspect`, không đọc mã) |

### 2.2 Chín điểm gắn (V5B2A §8)
| # | Điểm gắn | Làm |
|---|---|---|
| 1 | `scripts/k2/hero.js`, `scripts/ll/hero.js` llvmpipe + kiểm renderer + mã 6 + renderer vào meta | `scripts/k2tl/gl.js` (`pick`, `rendererOf`, `assertRenderer`) dùng cho cả 3 driver; `meta.json` có `renderer`, `gl` (k2 cả cảnh LL/k2v/tl; ll: cảnh LL). Thử: đọc renderer thật mỗi lượt (`[gl …] llvmpipe · ANGLE (Mesa, llvmpipe (LLVM 20.1.2 256 bits), OpenGL ES 3.2)`); test cờ sai → mã 6 vẫn ĐẠT trong `tests/run.sh` |
| 2 | Nhánh trang `tl/<cảnh>` | `hero.js`: `--hero tl/<cảnh>` → `design/k2v/tl/page.js`, `/cache/` → `$K2TL_CACHE`. Trang tl thêm chế độ HERO: `window.finalize` (RGB không chữ), `window.anchorsAt()` (điểm neo đặt tên + **lớp chữ ghi lại `_tl`** qua `record.js`), `window.frameMeta()`. Cảnh tl không dựng khung sau hết cảnh |
| 3 | SPP theo pha | trang tl dùng `state(t).spp` (`sppOf`) mỗi khung, bỏ qua `--spp 4` của heroes_par; SPP từng khung ghi `frames_meta` |
| 4 | `render.js` gom renderer | `.log.json` thêm `renderers {plate: renderer}` + `renderer_set` (bắt trộn trình dựng, KHOP1 b); mục chữ có `role` |
| 5 | Lớp 2D `tl` trong `k2.js` | `tlLayer()`: năm hoặc **ngày/giờ** dưới-trái (phóng 1,45× + viền hổ phách ở mốc đinh), lịch thứ hai, chỉ số "≈" + `index_src`, dòng phương pháp (HH3), thẻ neo/dải dưới, nhãn neo, **nhãn nguồn ghost ≥ 38 px (role `ghost_src`)**, chip nơi (role `where`). Chữ Inter + bảng màu kênh; cảnh tl ghi một lần, hai driver dùng chung |
| 6 | `prep.py` | `shot_type` tl → `scene3d` + `tl: true`, `cau` (ML1), `noi`; preset ngữ pháp làm `camera_id`; dấu cảnh tl = mã chung + mã tl (cảnh k2v/LL cũ **không đổi dấu**); cảnh báo VV2 (§3.2) |
| 7 | LUT A vào `design/k2v/page.js` | opt-in `opt.lut` (+ `lutMode`, `vib`, `lutK`); không khai → nhánh shader tắt, ô LUT trống 2³ → khung cũ không đổi (golden giữ số) |
| 8 | Công tắc GPU | `K2TL_GL=vulkan` \| `egl-gpu` (cờ theo `research/gpu/gl_flags.js`); renderer chứa llvmpipe/SwiftShader → DỪNG mã 6 (không âm thầm rơi về CPU). Máy này không có GPU → chưa chạy thật |
| 9 | `verify.sh` + `versions.py` | `verify.sh` gọi `scripts/k2tl/env_check.sh` (**PASS** "llvmpipe: mesa-libgallium 25.2.8… · llvmpipe (LLVM 20.1.2 256 bits)"); `versions.py` GROUPS thêm `k2tl: [design/k2v/tl, scripts/k2tl]`, khối máy thêm `mesa_libgallium` 25.2.8-0ubuntu0.24.04.4, `libllvm20` 1:20.1.2-0ubuntu1~24.04.3, `k2tl_gl` |
| + | `build.sh` | gọi `scripts/k2/tl_post.py` sau cảnh đinh (ghi `p.agl` + cảnh báo địa cầu); bước ghép chịu được tập < 3 đoạn |

### 2.3 Golden (`scripts/common/golden.py run --only steel,ll08,t1`) — `reports/v5b2b/golden/`
| Ca | P-1710 (SwiftShader) | Sau tích hợp, `K2TL_GL=swiftshader` | **Sau tích hợp, llvmpipe (mặc định mới)** | Kết luận |
|---|---|---|---|---|
| steel | KHỚP · SSIM 0,978 · 0 ô | KHỚP · **0,978** · 0 ô (trùng) | **KHỚP** · pHash 0 · SSIM **0,9449** · 0 ô | KHỚP |
| ll08 | KHỚP · 0,9686 · 0 ô | KHỚP · **0,9686** · 0 ô (trùng) | **KHỚP** · pHash 0 · SSIM **0,9307** · 0 ô | KHỚP |
| t1 | LỆCH CỤC BỘ · 0,9548 · 22 ô | LỆCH CỤC BỘ · **0,9548** · 22 ô (trùng) | LỆCH CỤC BỘ · SSIM **0,9082** · **22 ô** | lệch như đã biết |

- **Lượt cuối** chạy trên mã cuối phiên (sau mọi sửa `k2.js`/`prep.py`): số ở §8.
- SSIM giảm 0,03–0,05 chỉ do đổi trình dựng (khung tham chiếu là master dựng bằng SwiftShader). Dùng llvmpipe làm chuẩn thì khung vàng cũng phải dựng lại trên llvmpipe (KHOP1, RULES-LL 1.12.1) — chờ chủ dự án (§11).

## 3. Việc 2–3: P0/P1 cho T3 + đầu ra checks 1.13
### 3.1 P0 / P1 (TIEN-KY-VAY-HAM §5)
| Ưu tiên | Việc | Trạng thái | Mã + cách kiểm |
|---|---|---|---|
| P0 | 9 điểm gắn | **XONG** | §2 |
| P0 | AGL mỗi khung → `meta.json` | **XONG** | `frames_meta[f].agl_m/agl_km/spp/phase/preset/vai/year/clock/noi/sun`; `tl_post.py` → `p.agl` [[giây trong shot, km]] mỗi 0,5 s + `p.agl_max` |
| P0 | **M9** footprint chung + mái 3 thời kỳ | **XONG** | `scripts/k2tl/load_footprints.py`: GeoJSON bất kỳ (OSM, Catastro, ghost SH: `so_tang_uoc`, `loai`, `do_tin`, `--skip`), hoặc way/bbox OSM từ ô thô; `--kind ghost` → khối tái dựng; `--lines` → tuyến. `city.js styleOf(…, pd)`: **pd 0** 1704–1782 (mái ngói thấp + sân thượng, 2–3 tầng, không ban công sắt) · **pd 1** 1900–1943 (ngói + mái bằng có tường chắn, ban công) · **pd 2** 2026 (như cũ). `layers.footprints` (cửa sổ năm, `hid` cho hero_pct, `namMax` → `nam_khung`), `fort: true` = công sự đá (tường ốp đá, sàn pháo, tường chắn có lỗ châu mai — **không** dựng bastion như nhà ở). `opt.cut` bỏ toà gói nằm trong lớp riêng |
| P0 | **M12** bản đồ pha theo mốc | **XONG (cơ chế)** | `layers.phaseMaps`: raster đã nắn (hộp ENU) phủ lưới bám DTM, crossfade theo mốc; kiểm trên llvmpipe bằng `scenes/t3lab.js` (raster thay thế — raster nắn của SH ở `/var/tmp/cine-out/sh/warp/` máy khác, chưa có ở máy này). Kèm: **nền phố của địa hình theo vùng ghost** (`terrain.js` `tGhostU`) — mốc có ghost thì ngoài khối ghost là vườn/sườn, không phải nền lát 2026 |
| P0 | **M6** ngày/giờ + mặt trời | **XONG** | `sun.js`: NOAA/Meeus (cao độ/phương vị), lịch Gregory/Julius, giờ địa phương thế kỷ 18 (LMT). Bộ đếm `"13 Sep 1782 · 09:45"`, hai lịch `"O.S. 24 Jul · N.S. 4 Aug 1704"`; `page.js applySun` đổi hướng nắng + khoá bóng mỗi khung. 13/9/1782 09:45 Gibraltar: cao **45,8°**, phương vị **129,4°**. `tests/test_t3.mjs` ĐẠT |
| P0 | **M3** hạm đội + đường đi theo giờ | **XONG** | `ships.js lineFormation` + `makeFleet` (pin nổi 1782 **minh hoạ** theo bản khắc: thân thấp, mái nghiêng, 2 hàng lỗ pháo, 2 cột ngắn, mép boong sáng, đường mớn nước; tàu chiến tuyến; nội suy vị trí theo giờ, hướng mũi theo chuyển động). Không người trên boong |
| P0 | **M4** chiến tuyến mọc theo ngày | **XONG** | `layers.frontLines`: dải phe bám DTM + gờ đất hình thang, mọc theo quãng (`uGrow`), mờ theo cửa sổ; `stone` = tường đá (Line Wall). Màu phe: cam Pháp–TBN, lục lam đồn trú (bảng màu kênh, **không đỏ máu**) |
| P1 | **M1** mũi tên | **XONG** | `layers.arrows`: ruy băng bám địa hình + đầu mũi, mọc theo thời gian; dân thường màu trung tính |
| P1 | **M7** khói/lửa sprite 2D | **XONG** | `layers.smoke`: cụm khói thủ tục tất định (billboard, tích luỹ SPP), lửa nhỏ tuỳ chọn; ẩn khỏi mặt nạ (nền); `zones()` trả vùng khói để kiểm "không người trong khói". Đoạn thử: lửa đỏ ≤ **0,63 %** khung (≤ 15 %) |
| P1 | M8 Ken Burns tranh trong tl | **CHƯA** | ưu tiên đoạn thử + 3 vòng sửa theo tự rà/chấm mù; dự phòng của TIEN-KY: plate k2v ngoài tl (cắt cảnh) |
| P1 | M11 mặt cắt hầm | **CHƯA** | như trên; dự phòng: bản đồ hầm phẳng có nhãn |
| — | M2 | không làm (lệnh) | |

### 3.2 Đầu ra cho checks 1.13 (K-1.13 §8.1) + luật hình VV2
| Yêu cầu | Làm |
|---|---|
| `agl` (km) mỗi mốc → `p.agl` | `tl_post.py` (build.sh gọi) |
| `fabric_pct` shot bản đồ nổi có lớp nhà | mặt nạ tl có `fabric_pct` mọi khung; bộ đo `k2_measure.py` ghi theo khung toàn đoạn. Bản đồ nổi k2v (relief) chưa có lớp nhà → không có gì để xuất; đặc tả khai `p.city/p.ghost` cho shot thành phố (NC-H1 tập đọc khai) |
| `ghost_pct` | `city.js` mặt nạ G = 0,2 cho toà lớp tái dựng → `contentMask().ghost_pct` |
| `nam_khung` [{f, nam_max: {lớp: năm}}], `noi` [{t, noi}] | `SC.namKhung(st)` + `st.noi`; `bo-tl.json` (đoạn thử) và `tl_bundle.py nam_noi()` (bộ kiểu gib20) |
| log chữ role `where`, `ghost_src` | `k2.js` (`whereChip`, `tlLayer`), `text.js` (`where`, `ghostSrc`); `render.js` ghi `role` |
| `*.log.json` cùng master | `reports/v5b2b/do/log-chu.json` (gom từ `sec/*.log.json`); log gốc ngoài git `/var/tmp/cine-out/v5b2b-t/sec/` |
| Đặc tả bắt buộc khai `noi` từ T3 | `prep.vv2_warn`: shot cảnh địa lý chưa khai → CẢNH BÁO VV2; giá trị ngoài {thanh_pho, eo_dat, vung, bien, song, trong_nha} → cảnh báo |
| VV2 trong máy dựng | cảnh báo khi prep: (1) `noi: thanh_pho` mà cảnh không có lớp nhà; (2) địa cầu/relief > 50 km > 1 lần hoặc > 3 s; `tl_post.py` lặp lại (2) trên AGL thật mỗi khung. Chip nơi + hai tấm chữ (T2 TT6) giữ nguyên |

## 4. Việc 4: đoạn thử V5b-2b-T
### 4.1 Nội dung + dây chuyền
- **Đặc tả** `reports/v5b2b/doan-thu/episode.yaml`:
  - 2 đoạn, 4 shot plate, không lời (ElevenLabs 0);
  - nhạc `Tyrant.mp3` (dòng RIGHTS K2-MUS có sẵn);
  - `noi` khai từng shot: bien → thanh_pho → vung → thanh_pho.
- **Chạy:** `P=2 PARTS=0 bash scripts/k2/build.sh … prep render mix ghep` (prep → hero.js tl → tl_post → render.js + k2.js → mix → ghép).
- **(a) `scenes/vinh1782.js`, 18 s — cú liên hoàn #2, vai "bước ngoặt":**
  - bay ≈ 100 m trên mặt vịnh (lệch tuyến ≤ 0,01 m, AGL 96–100 m);
  - speed ramp;
  - orbit King's Bastion 5 s (footprint OSM 952588383 + 256821558, dựng như công sự đá);
  - **đồng hồ dừng 13 Sep 1782 · 09:45** từ 7,4 đến 9,2 s (1,8 s, phóng 1,45×);
  - crane;
  - lùi ra vịnh tây-nam: **đủ 10 pin nổi** chạy chéo khung, phố + Rock + Línea ở hậu cảnh;
  - khói M7: King's Bastion từ 09:45; pin nổi lần lượt 09:50 → 10:25 (toàn tuyến);
  - mặt trời đúng giờ (M6).

  Chữ trên hình:
  - thẻ "09:45 · The garrison's guns open fire / Times: Drinkwater 1786 and two other accounts";
  - thẻ "10 floating batteries · positions illustrative / Line: Drinkwater 1786 plan · hulls drawn from engravings";
  - chip nơi đổi theo cửa sổ (Bay of Gibraltar ↔ King's Bastion, Gibraltar);
  - dòng "Map data: OpenStreetMap (ODbL)" 0–4,6 s.
- **(b) `scenes/pho1782.js`, 8 s — phố 1782 có nhà (ghost SH, lệnh AE), vai "hệ quả":**
  - bay ≈ 70 m dọc tim Main Street (HH2 phố ≤ 120 m; lệch ≤ 0,37 m);
  - nhìn lệch tây về phần phố bản đồ có vẽ;
  - dòng phương pháp "Houses: 2-storey standard for 1782 (estimated)";
  - thẻ "Main Street, 1782 · blocks from the siege plan / Positions within ~21 m · east side not drawn on the plan".
- **Ghost 1782** (SH @ `54185b3`, đọc `SH-BAO-CAO.md` trước):
  - dùng 22 khối phố + 13 toà (`do_tin` cao/vừa), 4 bastion + Old Mole + 2 pháo đài TBN, Line Wall + tường nam (gờ đá), Línea (chiến tuyến);
  - **không dùng** feature `do_tin = thấp` (dải công sự tiền phương ±160 m);
  - King's Bastion lấy OSM (chính xác hơn RMS 21 m của plan);
  - lớp tái dựng 1705 của gói cảnh **ẩn** ở cả hai cảnh (một mốc, một nguồn);
  - nhãn nguồn đúng SH §5: **"Reconstructed from J. Drinkwater, Plan of the Batteries, 1782"**, role `ghost_src`, 38 px, hiện suốt cảnh;
  - không commit lại tệp ghost vào v5b2b.
- **Ra:**
  - master `reports/v5b2b/v5b2b-t-1080p-master.mp4` (LFS, 120,2 MB, 1920×1080, 24 fps, 624 khung, −14,1 LUFS / −1,6 dBTP, SHA-256 `43da3d93d3734b2013ce4a3d0be3c0eb14b2acd4ec783f484f859a598c1afeb1`);
  - tờ khung mỗi 1 s `reports/v5b2b/do/to-khung-moi-1s.jpg` (0,8 MB);
  - số đo `reports/v5b2b/do/`.

### 4.2 Tự rà trước khi báo (bài học T2 TT3) — 6 lượt dựng, mỗi lượt xem tờ khung mỗi 1 s
| Lượt | Phát hiện | Sửa |
|---|---|---|
| thử khung | nhà tái dựng mọc trên mặt sàn pháo King's Bastion; cỏ công viên 2026 ở 1782; reveal chỉ thấy nước | `opt.cut`; lớp nền đô thị trước 1900 đổi nhựa/sân/cỏ công viên → nền lát/đất trống; đổi góc reveal |
| 1 | thẻ pin nổi cắt mép trái (neo ngoài khung, nhãn ghost rộng đẩy thẻ ra x âm); thẻ 09:45 đè mặt bastion; hero orbit 23 % < 25 %; "every building drawn" nói quá | thẻ neo lên dải trên + luật thẻ ngoài khung; orbit r 118 → 100 m; câu đúng |
| 2 (lệnh AE) | phố 2026 thay bằng ghost 1782; phần phố bản đồ không vẽ hiện thành nền lát + đường 2026 | `layers.town1782` + nền phố theo vùng ghost + ẩn đường OSM |
| 3 | (k2check) nhãn ghost bị thu 30 px < 38; chưa khai lớp nhà/beats/type | giữ ≥ 38 px; khai `p.ghost/city`, `beats` (chỉ mốc cắt thật), `type` |
| 4 (chấm mù v1) | **nhãn ghost đè hộp ngày giờ phóng to (09:45 bị che)**; **mảng be giả giữa vịnh** = tàu neo trong DSM Copernicus lọt mặt nạ đất; reveal 5/10 pin nổi | nhãn ghost lên hàng trên khi có bộ đếm giờ (cố định cả shot); `build_scene.py` bỏ đốm đất rời < 2 000 ô 10 m + < 500 ô 20 m (417 + 158 + 92 ô); reveal tây-nam thấy đủ 10 pin nổi; thân pin nổi thêm chi tiết |
| 5 | thẻ pin nổi (neo ngoài khung) chồng nhãn ghost ở 14,75 s | thẻ lên trên cả hai hàng (chỉ dựng lại lớp 2D) |

Kết quả lượt cuối:
- **Độ đục nhãn:** mọi nhãn đủ độ đục, trừ quãng hoà vào/ra 0,35 s.
- **Viền/dải lạ:** không có. Không nhãn đè vật chính.
- **Nhà:** có ở mọi khung phố (fabric shot thành phố thấp nhất 24,6 %).
- **Điểm neo:** mỗi khung có neo và có lớp chữ `_tl`, **432/432 + 192/192** (kiem_neo).
- **Nhãn nguồn ghost:** hiện liền **17,5 s** ngay lần đầu (ghost hiện từ khung 0).
- **Chip nơi:** có ở mọi shot.
- **`noi` khai đúng:** đoạn thử không có eo đất trống, nên không có `eo_dat`.
- **Luật hình chiến tranh §6.2:**
  - không người A-lite ở 1782 (xe/người của gói chỉ có ở mốc 1941);
  - không người trên tàu; khói chỉ ở công trình và tàu;
  - lửa đỏ ≤ 0,63 %.
- **Tồn đọng đã biết:** một chấm be ≈ 12 px (1080p) trên mặt nước ở vài khung reveal. Không phải đất (đã lọc), không phải cây. Chưa tìm được nguồn, ghi ở §11.

### 4.3 Số đo (`reports/v5b2b/do/so-do.json`; mặt nạ MỌI khung `noi-dung-mask.json.gz`)
| Chỉ số | Trước (gib20 V5b-2a, khung tương ứng) | **V5b-2b-T** |
|---|---|---|
| fabric_pct shot thành phố (NC-H1) | gib20 khung thành phố trung vị 42,4 %, thấp nhất 15,3 % (K-1.13 §3.1) | trung vị **40,1 %**, thấp nhất **24,6 %**, p10 27,3 % (346 khung) |
| fabric_pct cả đoạn / content_pct | — | 28,6 % / **17,0 %** trung vị (vịnh + vườn 1782 chiếm nhiều diện tích) |
| hero_pct orbit (≥ 25 %) | 27,1 % (giao lộ 1941) | **29,6 %** (King's Bastion), thấp nhất 27,9 % |
| ghost_pct | (không có) | trung vị 6,3 %, cao nhất 30,8 %; lần đầu khung 0 |
| AGL (NC-H2/H3) | ≤ 2,17 km | **0,037–0,30 km**; > 50 km: 0; > 3 km: 0 |
| MAU1 (26 khung, mỗi 1 s, không chữ) | bão hoà 0,445 · colorfulness 45,6 · chi tiết 18,2 (8 khung) | bão hoà **0,378** · colorfulness **61,5** · chi tiết **17,4** · cháy 0 %; đạt bão hoà ≥ 0,35: **16/26**, colorfulness ≥ 35: **26/26**, chi tiết ≥ 16: **20/26** |
| BC1 (content < 30 %) | eo đất 5 s | **442/624 khung** (bay trên vịnh, vườn 1782, nhìn xuống nước khi crane) |
| lửa đỏ % khung | — | ≤ **0,63 %** |
| giờ máy / khung (hero, 2 cảnh song song) | gib20 1,594 s (1 tiến trình) | lượt sạch (3): **1,34 / 1,47 s**; lượt 5 (lẫn selftest): 1,52 / 1,71 s; lớp 2D 0,31–0,44 s |

- **MAU1 trượt bão hoà** ở 10/26 khung:
  - orbit/crane trên mặt sàn bastion màu be: 0,25–0,34;
  - phố 1782 (vữa nhạt): 0,28–0,35.
- **Chi tiết < 16** ở 6 khung: mặt sàn bastion không vân, 5,9–15,2.
- **Người chấm cùng nêu:** "flat beige slab". Cách sửa đúng là M5 (thành luỹ tham số: ụ pháo, gờ, đá) — P2, chưa làm. Không thêm vật để vượt ngưỡng.

### 4.4 k2check 1.13 (CHỈ BÁO) — `reports/v5b2b/do/k2check-1.13.md`, `--bo-tl reports/v5b2b/do/bo-tl.json`
| Hàng | Kết quả | Ghi chú |
|---|---|---|
| **NC-H1 / NC-H1 [bộ]** | **ĐẠT / ĐẠT** | tập: 2 shot thành phố khai lớp nhà; bộ: 345/624 khung thành phố, fabric trung vị 40,1 %, thấp nhất 24,6 % |
| **NC-H2 / [bộ]** (ngưỡng 50 km mọi khung) | **ĐẠT / ĐẠT** | 0 lần; AGL cao nhất 0,28 km (timeline) / 0,30 km (khung) |
| **NC-H3 / [bộ]** | **ĐẠT / ĐẠT** | AGL ≤ 3 km 100 % |
| **NC-H4 / [bộ]** | **ĐẠT / ĐẠT** | log chữ 55 mục nơi/địa danh, role where |
| **NC-H5 [bộ]** | **ĐẠT** | nhãn ghost **38,0 px** (đúng ngưỡng), liền 0:00,5–0:18,0 (17,5 s) và 0:18,5–0:26,0; (a) `nam_khung` ≤ năm bộ đếm. NC-H5 tập: không áp |
| **Q37(d) / Q37 (1.13)** | (d) **ĐẠT**: khung tĩnh dài nhất 0,25 s · hàng **TRƯỢT** (b) TB 6,5 s, (c) 8,0 s | beats chỉ được khai ở mốc thật của đặc tả (4 mốc cắt). Biến cố trong cảnh tl (ramp 4,0 · đồng hồ dừng 7,4–9,2 · crane 10,6 · pin nổi vào khung 15,2) không phải mốc đặc tả → K không nhận. **Không thêm phần tử giả để tạo mốc**; đề xuất K §10 |
| Q7/Q8-K2, Q33 (1.13), Q36 (1.13), Q33-K2, Q32b-K2, Q34, Q35, Q35-TL, Q36, TL-Q2, TL-Q7, TL-Q8, TL-Q9, NHIP-K2, FT1, ML2, ML3, LOCK | ĐẠT | TL-Q2: vịnh 4,04 s lệch ≤ 0,01 m / AGL 96–100 m (khai `song` ≤ 300 m); phố 8,0 s lệch ≤ 0,37 m / AGL 65,9–70 m ≤ 120 m |
| ML1 | TRƯỢT | timelapse 100 % > 15 % — đoạn thử toàn cảnh tl theo thiết kế |
| Q26b / Q26b-K2 | TRƯỢT | 2 cảnh trong 26 s — luật đa dạng cấp tập, không đo được trên đoạn thử |
| TL-Q1 | TRƯỢT (e) 0 mốc đinh; (c),(d) THIẾU | mốc đinh của đoạn thử là **dừng GIỜ** (năm đứng yên 1782) — luật đếm năm dừng; không xuất `hero_anh`/số thẻ mỗi khung |
| TL-Q3…Q6 | THIẾU | bộ đoạn thử không khai reveal/ảnh/ngân sách chữ kiểu gib20 (không có ảnh lịch sử, không có chỉ số) |

### 4.5 Ngoại suy tập 10 phút (14 400 khung, ≤ 12 h)
| Thành phần | Đo (lượt sạch 3, 624 khung) | ×(600 / 26) | Giờ |
|---|---|---|---|
| Trọn dây chuyền prep → cảnh tl (2 tiến trình) → 2D → mix → ghép | 856 s | ×23,1 | **5,5 h** |
| Mặt nạ mọi khung + campath + đo (`k2_measure.py`) | 154 s | ×23,1 | **1,0 h** |
| **Tổng** | | | **≈ 6,5 h ≤ 12 h** (máy 4 vCPU này; V5b-2a máy D 4,3 h + 0,9 h với nhịp SPP khác) |

- Giả định chặt: cả tập là cảnh tl 1080p. Bảng shot T3 chỉ có 68,3 % là 3D, phần còn lại (thẻ, ảnh, Ken Burns) rẻ hơn nhiều, nên số thật thấp hơn. Ghép (120 s cố định) đã tính tuyến tính.

### 4.6 Chấm mù (giao thức blind_g2: `claude -p` ghim `claude-sonnet-5-5`, chỉ Read, 3 vai, thang tuyệt đối) — `reports/v5b2b/kiem-mu/`
Cặp và giây V5b-2b-T khai **trước** khi có master (commit `blind_v5b2b.py`). P5/P6 khai lúc cảnh (b) còn là phố 2026; sau lệnh AE vẫn giữ nguyên giây, loại cảnh không đổi.
| Cặp | Loại cảnh | gib20 | Vòng 1 (lượt 3) | Vòng 2 (lượt 6, chỉ cặp đã sửa) | Thắng/thua (vòng mới nhất) |
|---|---|---|---|---|---|
| P1 | bay thấp tới nơi | 6,67 / 7,0 | 6,0 (0/3 chọn) | **6,0** (0/3) | **thua** — "nửa dưới là mặt nước trống" |
| P2 | orbit, ngày dừng | 5,0 / 4,33 | 5,67 (2/3; lỗi chữ đè ngày) | **6,0** (3/3; hết `text_overlap`) | thắng |
| P3 | cận công trình lịch sử | 5,67 | **6,67** (3/3) | — | thắng |
| P4 | reveal toàn cảnh | 7,0 / 7,0 | 5,0 (0/3) | **5,67** (0/3) | **thua** — "pin nổi nhỏ, thân như tấm ván, khói nhạt" |
| P5 | phố cổ dày nhà | 7,0 | **7,0** (3/3) | — | hoà điểm, 3/3 chọn |
| P6 | toàn cảnh phố + công trình | 5,33 | **7,0** (3/3) | — | thắng |
| **TB** | | 6,11 (v1) | **6,22** | gộp (P1, P2, P4 vòng 2): **6,39** so 6,06 | thua 2/6 |

- **Chi phí chấm mù:** $1,61 / trần $2 (27 lượt). Sổ ghi cả model nền CLI tự gọi: `served` có claude-haiku-5-5, ≈ $0,0002/lượt.
- Dừng sau vòng 2 để giữ trần.
- **Phần so đối thủ:** khung đối thủ không có trong repo — Claude điều phối chấm ở chat.

## 5. Kiểm (việc 5)
| Kiểm | Kết quả |
|---|---|
| selftest checks: k113 / k1122 / k1121 / k112 / k2 / ll | **64/64 · 37/37 · 48/48 · 75/75 · 129/129 · 317/317** — không giảm |
| `scripts/k2/test_k2v.py` | OK |
| `scripts/k2tl/tests/run.sh` | **TẤT CẢ TEST ĐẠT** (geo, calib, look, geom, campath, grammar, **t3 mới**, env_check, test_browser llvmpipe + swiftshader, cờ sai → mã 6) |
| golden | §2.3 + §8 |
| preflight | mọi commit/push ĐẠT; `lock.py --verify` KHỚP |
| `verify.sh` | đầu phiên 10 PASS / 3 FAIL (three.js, tifffile/pyshp, k2v node_modules — container mới) → cài theo hướng dẫn; + hạng mục mới **llvmpipe PASS** |
| `versions.py check` (so `channel-k2/k2c-t2-01/VERSIONS.yaml`) | **CHẶN 5**: `checks.version` 1.10.2 → 1.13.0, `checks.tree_sha256` (merge 1.13 theo lệnh); `toolkit.k2v`, `toolkit.ll` (chính phiên này sửa — dự kiến); `episode.served_models` (có từ trước, model nền CLI). **BÁO 2**: `claude_cli` 2.1.300 → 2.1.302; `relief_cache` không có ở container này. Không tự ghi đè VERSIONS.yaml của T2 |

## 6. Chỉ số trong ±5 % quanh ngưỡng (luật cứng)
| Chỉ số | Đo | Ngưỡng | Lệch |
|---|---|---|---|
| Cỡ nhãn nguồn ghost (NC-H5b) | 38,0 px | ≥ 38 px | 0 % (đúng ngưỡng, theo thiết kế SRCPX) |
| Golden SSIM t1 (llvmpipe) | 0,9082 | ≥ 0,90 | +0,9 % |
| Golden SSIM ll08 (llvmpipe) | 0,9307 | ≥ 0,90 | +3,4 % |
| Golden SSIM steel (llvmpipe) | 0,9449 | ≥ 0,90 | +5,0 % |
| MAU1 bão hoà khung 7 s / 17 s / 25 s | 0,341 / 0,353 / 0,345 | ≥ 0,35 | −2,6 % (TRƯỢT) / +0,9 % / −1,4 % (TRƯỢT) |
| MAU1 chi tiết khung 17 s / 15 s / 25 s / 16 s / 8 s | 16,0 / 16,3 / 16,4 / 16,7 / 15,2 | ≥ 16 | 0 % / +1,9 % / +2,5 % / +4,4 % / −5,0 % (TRƯỢT) |
| True peak master | −1,6 dBTP | ≤ −1,5 dBTP (kênh) | biên 0,1 dB |
| Loudness master | −14,1 LUFS | −14 | −0,7 % |
| Đồng hồ dừng mốc đinh | 1,8 s | 1,5–2,0 s | trong khoảng |

## 7. Giờ máy + chi phí
| Khoản | Trần | Thực tế |
|---|---|---|
| Claude API | $2 (ghim) | **$1,61** (chỉ chấm mù; `reports/v5b2b/kiem-mu/cost.jsonl`) |
| ElevenLabs / YouTube | 0 / 0 | 0 / 0 |
| Giờ máy | ≤ 8 h | **≈ 3,3 h** (ước theo log, 4 vCPU): dựng gói cảnh 3 lần ≈ 0,15 h · test k2tl ≈ 0,25 h · golden 3 lượt ≈ 0,6 h · 6 lượt dây chuyền đoạn thử ≈ 1,2 h · khung thử ≈ 0,3 h · đo + k2check ×7 ≈ 0,45 h · selftest ≈ 0,2 h · chấm mù (mạng) ≈ 0,15 h |
| Mạng | — | ≈ 1,4 GB dữ liệu thô (10/10 tệp nguồn KHỚP SHA), OSM 70 MB, LFS 119 MB × 2 |

Đề xuất dòng `COST-LEDGER.csv` (P ghi): `V5b2b,gắn tl vào kênh 2 + P0 T3 + đoạn thử 1782,V,2026-10-17,,,,,1.61,2,claude-sonnet-5-5,0,0,≈ 3,3,,0,26,,reports/V5B2B-BAO-CAO.md,YouTube 0; không merge`

## 8. Golden lượt cuối (mã cuối phiên)
`reports/v5b2b/golden/golden-llvmpipe-cuoi.json` (247,7 s): **steel KHỚP** (pHash 0, SSIM 0,9449, 0 ô) · **ll08 KHỚP** (0, 0,9307, 0 ô) · **t1 LỆCH CỤC BỘ** (0, 0,9082, 22 ô) — trùng từng số với lượt ngay sau tích hợp; các sửa sau đó (`k2.js` lớp tl, `prep.py`, `build_scene.py`) không đổi hình tập cũ.

## 9. Tệp đã sửa (`git diff --name-only origin/main..HEAD`, trừ `checks/` + `reports/K-1.13-BAO-CAO.md` đến từ merge 1.13)
- **`scripts/k2/`:**
  - sửa: `hero.js`, `render.js`, `prep.py`, `build.sh`, `lib/k2.js`;
  - mới: `tl_post.py`.
- **`scripts/k2tl/`:**
  - sửa: `render.js`, `tl_bundle.py`, `build_scene.py`, `tests/run.sh`;
  - mới: `gl.js`, `load_footprints.py`, `k2_measure.py`, `tests/test_t3.mjs`.
- **`scripts/ll/`:** `hero.js`, `ll.py`, `qc.py` (chỉ K-1.13 §8.3).
- **`design/k2v/`:**
  - sửa: `page.js` (LUT A opt-in), `tl/page.js`, `tl/city.js`, `tl/terrain.js`, `tl/text.js`, `tl/ships.js`, `tl/campath.js` (ALT_MAX `vinh`);
  - mới: `tl/record.js`, `tl/sun.js`, `tl/layers.js`, `tl/scenes/vinh1782.js`, `tl/scenes/pho1782.js`, `tl/scenes/pho2026.js` (dự phòng), `tl/scenes/t3lab.js` (cảnh kiểm máy).
- **`scripts/env/verify.sh`, `scripts/common/versions.py`.**
- **`reports/V5B2B-BAO-CAO.md` + `reports/v5b2b/**`:**
  - 4,3 MB thường ≤ 20 MB;
  - master qua LFS (mẫu `*-master.mp4` đã được phép trong `tools/lfs-allow.txt`, §10.4).
- **Gói cảnh ngoài git** `$K2TL_CACHE/scene/gib/pack` dựng lại sau khi lọc đốm đất giả. Lần dựng khung vàng llvmpipe tới phải khai `goi_canh.sha256` mới (KHOP1 d).

## 10. Tự quyết của phiên (không dừng hỏi)
1. **Lệnh AE nhận giữa phiên:**
   - dùng ghost 1782 cho **cả hai** cảnh (cùng mốc), không chỉ cảnh (b), để không trộn lớp 1705 với 1782 trong một đoạn;
   - lượt dựng đang chạy (phố 2026) để xong, rồi dựng lại.
2. **Bỏ ghost `do_tin = thấp`** khỏi đoạn thử: lệnh cho phép dùng ở hậu cảnh xa kèm "approx.", nhưng khung (a) không cần đến nó.
3. **Loại tuyến "vinh"** (mặt vịnh) chưa có trong HH2 → thêm `ALT_MAX.vinh = 300` (như sông); khai `song` cho K. Chờ chủ dự án.
4. **LFS:**
   - mẫu `*-1080p.mp4` (ZZ4) chỉ được phép trong `channel-k2/*/v5b1-thu/`, thuộc vùng `k2c-t3-01` mà phiên này không được ghi;
   - nên đặt tên `reports/v5b2b/v5b2b-t-1080p-master.mp4`: khớp mẫu đã phép `*-master.mp4`, có "1080p" trong tên.
   - Đề xuất P: thêm mẫu `reports/v5b2b/*-1080p*.mp4` hoặc chuyển tệp nếu muốn đúng ZZ4.
5. **Q37:** không bịa mốc đặc tả để khai beats. **Đề xuất cho K:** nhận `campath.shots[].phases` (fly/ramp/orbit/pin/crane/reveal) và đồng hồ dừng (`frames_meta.clock`) của cảnh tl làm biến cố thị giác. Ghi ở đây vì `checks-appeal.md` ngoài vùng lệnh.
6. **TL-Q1:** mốc đinh T3 là **dừng giờ** (13/9/1782 09:45), không phải dừng năm. Đề xuất K đọc `frames_meta.clock`/pha `pin` thay vì năm.
7. **Sửa dữ liệu gói cảnh** (`build_scene.py`): bỏ đốm đất giả do tàu neo trong DSM. Việc này đổi hình gib20 cũ ở các khung có vịnh (chỉ bỏ vật sai).

## 11. Việc chờ chủ dự án
1. **Xem duyệt đoạn thử** `reports/v5b2b/v5b2b-t-1080p-master.mp4` (LFS) + `reports/v5b2b/do/to-khung-moi-1s.jpg`: cú liên hoàn #2 (đồng hồ dừng 09:45, 10 pin nổi), phố 1782 ghost.
2. **Hai cặp chấm mù còn thua gib20 (P1, P4).** Hướng sửa (chưa làm, cần một vòng dựng + chấm, ước $0,6):
   - P1: hạ/ngẩng máy cho bờ thành phố chiếm giữa khung, thêm tàu tiền cảnh;
   - P4: máy thấp + gần hàng pin nổi, khói/lửa đậm hơn có kiểm ≤ 15 %, thân pin nổi chi tiết hơn (cần nguồn kích thước — TIEN-KY ghi "chưa có nguồn");
   - mặt sàn bastion phẳng → M5 thành luỹ tham số (P2).
3. **Duyệt llvmpipe là chuẩn cho dây chuyền kênh 2:** golden giảm SSIM 0,03–0,05 so khung tham chiếu SwiftShader. Nếu duyệt, giao V/K dựng lại khung vàng trên llvmpipe với `goi_canh.sha256` (RULES-LL 1.12.1 hướng dẫn V5b-2b mục 1–5; phiên này chưa làm bước 2–4).
4. **K xem đề xuất §10.5–10.6** (Q37 nhận biến cố cảnh tl; TL-Q1 nhận dừng giờ) và ML1/Q26b khi chấm đoạn thử.
5. **Duyệt** `ALT_MAX.vinh` (≤ 300 m) cho bay mặt vịnh (HH2).
6. **P ghi:**
   - `COST-LEDGER` (§7);
   - LFS mẫu (§10.4);
   - `AUTHORSHIP` (quyết định sáng tạo chờ duyệt: đường máy cú #2, góc reveal tây-nam, chọn ghost cao/vừa, câu chữ trên hình §4.1);
   - `RIGHTS` (không có tài sản mới; OSM/Drinkwater đã có dòng qua T3b/SH).
7. **P1 còn lại** M8 (Ken Burns trong tl), M11 (mặt cắt hầm) và **tồn đọng** chấm be ≈ 12 px trên nước ở vài khung reveal — giao phiên V sau.
