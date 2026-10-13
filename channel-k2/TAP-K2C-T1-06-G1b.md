# K2C-T1-06 "Apartments" — CỔNG G1b: khung mẫu (phiên P, 13/10/2026)

> **Lệnh 13/10 (chủ dự án duyệt mốc V có điều kiện):**
> 1. Squash `k2-visual`.
> 2. Gỡ email khỏi các lệnh gọi mạng.
> 3. Kiểm thử và LOCK.
> 4. Xoá hai nhánh remote.
> 5. Quyền ảnh LoC.
> 6. Lộ trình dùng bản đồ địa cầu, không dùng sa bàn.
> 7. Giữ ảnh lưu trữ ở 12,2 %.
> 8. **G1b dựng khung mẫu bằng bộ k2v, dừng ở G1b.**
>
> Báo cáo kèm: tờ khung tổng (jpg đã commit), SHA của các shot mẫu, số đo Q26b/Q33/Q34/Q32, chi phí.
> Khiếu nại Q34(c) không xử lý ở phiên này (chờ phiên K).

## 0. Tóm tắt

| Hạng mục | Kết quả |
|---|---|
| Squash `k2-visual` @099f055 + gỡ email | **Xong** (a9bcc7f). `git grep -n -i -I 'hungqv301\|gmail'` = 0 dòng. UA: `Mozilla/5.0 (cine-lab research; https://github.com/HungQuach301/cine-lab)` |
| `test_k2v.py` / `checks/lock.py --verify` | **OK** (9 test) / **KHỚP** `1a126d58…`. Không sửa `checks/` |
| Xoá nhánh remote `k2-visual`, `claude/happy-knuth-nm4my8` | **Không được phép**: HTTP 403. **Chủ dự án xoá tay** (cả hai ở 099f055) |
| Quyền ảnh LoC (18 + LOC-3c01767) | **7/19 xác nhận** (LOC-DET-01..07: "No known restrictions on publication."). Dừng ở 429 theo lệnh. 12 mục giữ ở CAN-TAI-HO (06bcfa0). Chưa chặn G1b; **phải xong trước G2** |
| Lộ trình / địa danh | `map/globe` thật (Blue Marble + Natural Earth + Census), không dùng sa bàn. Mẫu: bay xuống Euclid/Cleveland |
| Ảnh lưu trữ | Giữ 12,2 % (shots.yaml không đổi) |
| **G1b** | **3 shot mẫu 1080p SPP4, 78,3 s, 14 shot, đủ 5 loại** (scene3d, map, chart3d, photo, document). Đã dùng đủ **7/7 bộ cảnh 3D** của tập. Tờ khung tổng 42 khung (`g1b/TO-KHUNG-G1b.jpg`). Tờ góc máy 7 cảnh (`g1b/cams/*.jpg`) |
| Chi phí API lượt này | **$0** (không gọi Claude API, ElevenLabs hay YouTube) |

## 1. Bộ cảnh 3D của tập — `design/ll-hero/k2c106.js`

7 bộ cảnh viết theo hợp đồng cảnh ll-hero (`kit.js`, chữ ở lớp 2D qua điểm neo), mô tả theo `shots.yaml` mục `scenes`:

| Cảnh | Nội dung | Tuỳ chọn chính | Điểm neo |
|---|---|---|---|
| `corner` | Toà góc phố 4 tầng (cửa hàng + 3 tầng căn hộ), ngã tư, chạng vạng / giờ xanh / ngày. **Mặt cắt**: hai mặt tiền mờ dần, lộ sàn, vách căn hộ và **một cầu thang cam** ngay sau cửa riêng của căn hộ | `tod`, `section:[t0,t1]`, `shop` | building, shop, apt2–4, stair, roof, street, corner |
| `street` | Dãy phố: duplex, triplex, fourplex, walk-up 5 tầng, walk-up có cửa hàng | `hl`, `hlAt` | duplex…walkup2 (+ `_base`) |
| `tiers` | Sa bàn 4 tầng khu U-1..U-4 tô dần. "Toà thử" (cửa hàng + căn hộ) đặt lần lượt vào từng khu: vòng đỏ ở U-1..U-3, lục lam ở U-4 | `fill`, `probe`, `sun` | u1–u4, probe, apt, small |
| `lot` | Lô góc nhỏ nhìn từ trên: ô đỗ xe rơi xuống lần lượt, toà co chiều sâu | `stalls`, `grow` | lot, building, parking, corner |
| `stairs` | Mặt cắt sàn: 1 cầu thang (lục lam) / 2 cầu thang + hành lang (cam); tầng xếp dần; tầng 4 "NP" đỏ; mũi tên áp suất; 3 đèn điều kiện cháy | `mode`, `floors`, `stackAt`, `np`, `press`, `fire` | one, two, core1/2, np, floor4, fire1–3 |
| `bank` | Khối 1–2–3–4 căn, vạch cam "4", khối thứ 5 trượt sang quầy multifamily; quầy SF/MF; biến thể có cửa hàng | `fifth`, `shop`, `reject` | s1, s4, s5, line, sf, mf |
| `ends` | Sa bàn hai đầu: nhà một hộ tăng, toà nhỏ thưa dần, toà ≥ 50 căn cao dần theo năm 1972 → 2025 | `year`, `year1`, `yearAt` | houses, small, big |

- **Thư viện góc máy** nằm trong module: `CAM[cảnh]`, gọi qua `opt.preset`; `camera_id` = tên preset, khớp `shots.yaml`.
  - Số preset: 9 / 6 / 6 / 6 / 6 / 6 / 6 (đạt luật ≥ 6 của `test_k2v.py`).
  - Đã đăng ký trong `scripts/k2/cams.yaml` (`module: true`).
- **Rà tờ góc máy** (`g1b/cams/<cảnh>.jpg`, khung đầu và cuối mỗi preset):
  - Lượt 1 có 5 preset hỏng: `street/tall_walkups` (máy sát tường), `street/low_curb` (người và xe che khung), `tiers/close_u3` (mái phủ khung), `tiers/shadow_low` (tường cắt khung), `corner/blue_hour_end` (gần trùng `wide_dusk`, rủi ro pHash Q33).
  - Đã sửa cả 5 và rà lại. Không còn preset phải đánh `loai`.
- **Lỗi đã sửa khi rà khung thử:**
  1. `box()` của kit gắn vào cảnh hiện hành chứ không vào `window.__scene`, khiến bậu cửa sổ và song cửa trôi lơ lửng trên trời. Đã truyền parent tường minh.
  2. Nhà hàng xóm che toà góc phố ở góc rộng: đã dời nhà.
  3. Mặt cắt không thấy cầu thang: đã dời cầu thang ra mặt −z sau cửa căn hộ, làm vách trong mờ, giảm đèn trong.
  4. Vật liệu mặt cắt bị clone mỗi khung (rò bộ nhớ): nay chỉ clone một lần.

### Thay đổi ngoài cảnh (bộ k2v của phiên V, sửa tối thiểu)

| Tệp | Thay đổi | Lý do |
|---|---|---|
| `design/k2v/map.js` (+ README) | `opt.pinMin` (mặc định 0,6, không đổi hành vi cũ) | Bay xuống tầm thành phố, hai ghim Euclid và Cleveland cách 14 km dính thành một vệt sáng |
| `scripts/k2/prep.py` | `CODE` thêm `design/ll-hero/k2c106.js` | **Lỗi bộ đệm:** dấu stamp của vshot không chứa mã cảnh k2c106, nên sửa cảnh mà giữ opt sẽ âm thầm dùng lại khung cũ. Bản dựng G1b đầu không bị ảnh hưởng (thư mục mới). Bản cuối dựng sau khi sửa |
| `scripts/k2/k2v_assets.py` (+ SHA ghim) | 3 tài sản: `loc-hoover-1928`, `loc-det-07`, `usrep-272-365` | Ảnh và trang văn bản cho shot mẫu B. Cache ngoài git |
| `scripts/k2/cams.yaml` | Mục `k2c106/*` | Thư viện góc máy (luật lặp `prep.py`) |

## 2. Tài sản (không commit media; SHA ghim trong `scripts/k2/k2v-assets.sha.json`)

| id | Tệp gốc | SHA-256 (đầu) | Quyền |
|---|---|---|---|
| bm-200407, bm-200407-B1 | Blue Marble NG 07/2004 (toàn cầu 2 km; ô B1 500 m) | khớp ghim V | NASA, ghi "NASA Earth Observatory" trên hình |
| loc-hoover-1928 | `tile.loc.gov …/hec/34800/34871u.tif` | `3ac78a61…` (khớp bản tải G1a) | RIGHTS bảng tư liệu WM-HOOVER-1928 (PD) |
| loc-det-07 | `tile.loc.gov …/det/…/4a17898v.jpg` (1024 px) | `ab67a581…` | RIGHTS LOC-DET-07, Rights Advisory "No known restrictions on publication." |
| usrep-272-365 | U.S. Reports 272 U.S. 365 (PDF LoC) | `3949c701…` | Phán quyết công, 17 U.S.C. §105. **Trang PDF 30 = tr. 394** (trang chẵn có tiêu đề "OCTOBER TERM, 1926"; câu "height and bulk" khớp claims C10) |

- Không cần ghim thêm ô Blue Marble A1: Euclid nằm trong B1. A1 sẽ cần cho các shot Colorado, Seattle, California, Oregon, Texas ở G2.
- Ảnh Woodward Ave chỉ có bản 1024 px. Khi Ken Burns ở 1080p, ảnh mềm thấy được (§5). Ở G2 nên tải bản `u.tif` gốc nếu LoC mở lại.

## 3. Ba shot mẫu — `channel-k2/k2c-t1-06/g1b/`

Đặc tả dạng episode (`*.yaml`), dựng bằng `scripts/k2/vshot.py <yaml> --spp 4`. Video được commit qua **Git LFS** (`.gitattributes`: `channel-k2/k2c-t1-06/g1b/*.mp4`, PLAN.md: video > 30 MB đẩy lên nhánh git). Kèm `*.timeline.json` (chỉ dữ liệu kênh này).

| Shot mẫu | Đoạn lời | Shot (type · scene_id · camera_id) | Thời lượng | Khung | SHA-256 mp4 |
|---|---|---|---|---|---|
| **A** `A-mo-dau.mp4` | 00–01 | scene3d corner·wide_dusk ("about 1 in 13", C01) → chart3d bars·front-dolly (7,5 % / 1,1 %, C01/C02, hai cơ sở) → scene3d corner·push_facade + tựa câu hỏi → scene3d street·dolly_day (duplex…5–19 căn, "Facts as of", dòng không phải lời khuyên tài chính) → scene3d corner·section (Shop · Apartments · One staircase) | 27,0 s | 648 | `6f3776647cbc31a2d6df5228d60200193f2ae49de05134c50ecf5043cd4fad43` |
| **B** `B-euclid.mp4` | 02 | map globe·flyto-euclid (Euclid, Ohio + Cleveland, trích "practically a suburb", C55) → photo print·push-hoover (WM-HOOVER-1928) → **document** doc·push-page394 (2,8 s, `paper: U.S. Reports, vol. 272`, `date: 1926-11-22`, tô "height and bulk…rays of the sun", C10) → scene3d tiers·oblique_tiers (U-1..U-4 + toà thử, C08) → photo print·push-det07 (LOC-DET-07) | 27,3 s | 655 | `dadccebc64a591907cd4722bd87ee010ead194447071a3003b8cbaadbd405a87` |
| **C** `C-ba-khoa.mp4` | 03, 04, 06, 08 | scene3d lot·plan ("2 spaces per home", C14) → scene3d stairs·elev_stack ("One staircase" → "4th story: NP", C15) → scene3d bank·fifth_block ("4", "5+ homes", C26) → scene3d ends·wide_1972 (1972 → 2025) | 24,0 s | 576 | `304711e3ae3f9f8a8311605ae500ae93de64a65c54d9b9e9639765580a5b6a49` |

**Tờ khung tổng:** `channel-k2/k2c-t1-06/g1b/TO-KHUNG-G1b.jpg`, 42 khung (mỗi shot 3 khung ở 15 / 55 / 95 %), có nhãn type · scene_id · camera_id · giây. SHA `0e4d8e44…`.

- Mọi số trên hình khớp claims.md (C01, C02, C08, C10, C14, C15, C26, C55).
- Mọi shot có dòng nguồn. Shot luật / mã xây dựng có "Facts as of 12 Oct 2026". Cảnh minh hoạ ghi "illustration" / "3D illustration, not to scale".

## 4. Số đo luật K (chạy `checks/ll/*.py` trên `g1b/*.yaml`, đọc `<out>/timeline.json`; P chỉ chạy, không đọc mã)

| Luật | A | B | C | Ghi chú |
|---|---|---|---|---|
| **Q33** lặp cảnh | ĐẠT (5 góc, max 1) | ĐẠT (5 góc, max 1) | ĐẠT (4 góc, max 1) | "chưa đo pHash (không có master)" |
| **Q34** loại shot | ĐẠT: scene3d 77,8 % · chart3d 22,2 %; số neo 3D 100 % (2 số) | **TRƯỢT** (a)(b): "không thấy 'Euclid, Ohio' / 'Cleveland' / 'Herbert Hoover' trong lời"; type 5/5, document ≤ 3 s, có paper + date | ĐẠT: scene3d 100 %; số neo 3D 100 % (3 số) | Xem dưới |
| **Q32** footage / nguồn ngoài | ĐẠT (không footage) | **TRƯỢT**: tư liệu / ảnh / báo 13,5 s = **49,5 % > 40 %** | ĐẠT | Xem dưới |
| **Q26b** bối cảnh | corner 57,4 % · chart3d/bars 22,2 % · street 20,4 % · `the` 0 % | tiers 28,6 % · trung tính (map / photo / doc) 19,5 s · `the` 0 % | bank 27,1 % · ends 27,1 % · stairs 25,0 % · lot 20,8 % · `the` 0 % | **Đo tay** (xem dưới) |

**Diễn giải, không che số:**
- **Q34(a)(b) ở B trượt vì shot mẫu không có lời** (vshot không thu giọng). Luật tìm lần nhắc tên trong lời ±6 s.
  - Trong tập thật, map Euclid nằm ở câu "In 1926, a case from Euclid, Ohio…" và ảnh Hoover ở câu "In 1921… Herbert Hoover" (shots.yaml s02g, s02b).
  - Lần chạy chính thức là trên `episode.yaml` có lời, ở G2.
- **Q32 ở B 49,5 %** vì tôi cố ý dồn đoạn 02, đoạn nhiều tư liệu nhất (ảnh Hoover, trang bản án, ảnh Detroit), vào một mẫu 27 s.
  - Trần 40 % là trần của **cả phim**. Tự đo trên shot list cả tập: photo + document + footage = **15,6 %**, ảnh lưu trữ 12,2 % (SHOTLIST.md).
  - **Không cân lại mẫu để vượt chỉ số** (luật cứng).
- **Q26b:** `checks/ll/q_setting.py` dừng với `json.decoder.JSONDecodeError: Expecting value` trên cả 3 timeline của vshot. P không đọc mã `checks/`, nên đo tay theo câu chữ RULES-LL (plate → `heroes.<k>.hero`; map / ảnh / văn bản trung tính; `p.card` → `the`). Script đo tay ở scratchpad, kết quả như bảng.
  - Q26b là luật **cả phim** (trần 25 %, liên tục 90 s). Mẫu 24–27 s một bộ cảnh chiếm > 25 % là đương nhiên.
  - Tự đo cả tập (SHOTLIST.md): `the` 13,8 % (liên tục ≤ 60 s), corner 11,6 %, stairs 6,0 %, các cảnh khác ≤ 3,9 %; nửa sau có 5 bộ cảnh 3D.
  - **Đề nghị phiên K** xem lỗi `q_setting.py` trên timeline của vshot (P không ghi vào checks-appeal vì chưa chắc là lỗi luật hay thiếu tệp đầu vào mà vshot không sinh).
- **Lớp chữ** (log render.js): chữ nhỏ dưới 30 px = **0**, tương phản < 4,5 = **0** ở cả 3 shot.

### Chỉ số trong ±5 % quanh ngưỡng (luật cứng)
- **Document B2 = 2,8 s / trần 3 s**: cách 6,7 %, sát nhưng ngoài dải ±5 %. Nêu để G2 không kéo dài shot này.
- Không có chỉ số nào khác trong dải ±5 %. Số neo 3D 100 % so với ngưỡng 60 %; cả tập 72 %.

## 5. Rà hình (bằng mắt, tờ khung tổng)

**Đạt:**
- Toà góc phố chạng vạng: ánh cửa hàng, hiên lục lam, người đi bộ.
- Mặt cắt một cầu thang đọc rõ.
- Sa bàn tầng khu đọc được thứ tự U-1 → U-4 và toà thử đỏ → lục lam.
- Vạch "4" và khối thứ 5 trượt sang quầy multifamily.
- Sa bàn hai đầu thay đổi theo năm.
- Mặt cắt cầu thang tầng 4 NP đỏ.
- Bản đồ bay từ địa cầu xuống bờ hồ Erie có ranh bang Ohio.
- Ảnh in trên bàn lưu trữ có thị sai.
- Trang bản án có dải tô theo dòng.

**Đã sửa sau lượt dựng đầu** (dựng lại toàn bộ bản 1080p, sau đó dựng lại riêng lớp chữ shot A):
- Nhãn đè nhau ở mặt cắt và tầng khu U-3/U-4.
- Chú thích lô xe hai dòng đè nhãn.
- Khối 5 căn bị cắt đỉnh.
- Khung cầu thang quá cao.
- Nhãn "Small apartment building" đè dòng "Facts as of".

**Còn tồn (đề nghị xử lý ở G2, không chặn duyệt mẫu):**
1. Bản đồ ở tầm ~400 km: ảnh Blue Marble 500 m/px mềm thấy rõ. Đây là giới hạn dữ liệu, không phải lỗi dựng. Ở G2 dừng máy cao hơn hoặc dùng nền vector.
2. Ảnh Woodward 1024 px hơi mềm khi đẩy (§2).
3. Dãy phố dolly mỗi lúc chỉ thấy 1–2 toà; "họ hàng" toà nhỏ đọc qua nhãn nối tiếp, chưa có khung tổng thấy cả dãy. G2 có thể ghép 1 khung `high_block` trước dolly.
4. Biểu đồ hook: cột 1,1 % thấp, nhãn nằm sát đáy. Đúng tỷ lệ thật (trục từ 0), giữ nguyên.
5. Hình khối nhân vật và xe còn đơn giản (low-poly); mức chi tiết ngang cảnh Steel. Mục tiêu nâng hình K7 (Q27) cần đo bằng chấm mù chính thức ở G2, chưa đo ở G1b.

## 6. Đo giờ máy (thật)

| Hạng mục | Số đo |
|---|---|
| 3D 1080p SPP4, **mỗi tiến trình** (3 tiến trình song song trên 4 vCPU) | corner 3,5–5,9 · street 4,0 · tiers 4,8 · lot 4,9 · stairs 2,9 · bank 2,6 · ends 4,7 · map 2,9 · photo 3,4–4,2 · doc 3,0 · chart3d 5,9 s/khung |
| Lớp chữ 2D | 0,17–0,29 s/khung |
| Đồng hồ thật | 1 879 khung trong **61 phút** (01:09 → 02:10 UTC) ≈ **1,95 s/khung đồng hồ** |
| Suy ra cho cả tập 15,6 phút (≈ 22 450 khung) | ≈ **12,2 giờ đồng hồ** cho 3D + 2D. G1a ước 10 h (lạc quan) / 13 h (nếu vật liệu giàu hơn); số đo nằm trong khoảng đó |

## 7. Chi phí

| Mục | Lượt này | Luỹ kế tập |
|---|---|---|
| Claude API (`claude -p`, trần $40) | $0 | $7,74 ghi sổ (`kiem-mu/cost.jsonl`) + ≤ $0,75 không ghi sổ (G1a) |
| ElevenLabs / YouTube Data API | $0 / không gọi | $0 |
| Tài sản | $0 (NASA, LoC, Natural Earth, Census) | $0 |

## 8. Sai lệch và rủi ro

- **Sửa bộ k2v của phiên V** (`map.js` `pinMin`, `prep.py` `CODE`): ngoài gói việc thuần cảnh. Lý do ở §1. Thay đổi tối thiểu, `test_k2v.py` OK, không đổi hành vi mặc định.
- **Video trong LFS trên nhánh làm việc `k2c-t1-06`**: 152 MB. Nếu chủ dự án muốn tách sang nhánh riêng thì báo, P chuyển.
- **Sau bản dựng cuối, `k2c106.js` có sửa 5 preset góc máy không dùng trong mẫu** (§1, rà tờ góc máy). Hình của 3 mp4 không đổi. Nhưng vì `CODE` nay chứa `k2c106.js`, chạy lại `vshot.py` sẽ dựng lại cảnh (đúng thiết kế).
- `shots.yaml` s02d (SSZEA) đang `date: "1926"`, chưa đúng dạng YYYY-MM-DD của Q34(d). Chưa có ngày phát hành chính xác của bản rev. ed., sẽ tra trước G2. Đã đổi `d_euclid` thành `1926-11-22` (ngày quyết, claims EUCLID). CFR ("current") và IBC ("2021") sẽ chuẩn hoá cùng lượt với SSZEA.

## 9. Việc đang chờ chủ dự án

1. **Duyệt G1b**: 3 shot mẫu + tờ khung tổng + 7 bộ cảnh và thư viện góc máy (§3, §5). Có chấp nhận các tồn đọng §5 để xử lý ở G2 không?
2. **Xoá tay** hai nhánh remote `k2-visual` và `claude/happy-knuth-nm4my8` (cùng ở 099f055). Phiên P bị 403.
3. Nơi chứa video mẫu: giữ LFS trên `k2c-t1-06` hay tách nhánh riêng (§8).
4. **Quyền 12 ảnh LoC** còn ở CAN-TAI-HO: P thử lại (cách ≥ 10 s, dừng ở 429) trước G2, hay chủ dự án kiểm tay trên trình duyệt?
5. Lỗi `q_setting.py` (Q26b) trên timeline của vshot: chuyển phiên K (§4).
6. Khiếu nại Q34(c): chờ phiên K (theo lệnh, không xử lý ở đây).
7. D6: sau 16/10 chỉ kiểm lại "as of".
