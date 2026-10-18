Nhánh thật: `ccr-11686158-4ucx09` (harness buộc tên này; lệnh yêu cầu `v5b2c` — nội dung tương đương: tách từ origin/v5b2b + merge origin/nc-ban-do, commit `aecd1a78`). Không merge vào main, không sửa checks/, docs/, channel-*/.

# V5b-2c — BÁO CÁO: V0 nâng hình · M14 theo B4 · M13-lite (ranh lịch sử + tuyến + chú giải) · đoạn thử SM2 → vịnh 1782 · chấm mù

## §0 Tóm tắt

| Việc | Kết quả |
|---|---|
| V0 (bắt buộc trước) | Bastion tham số M5 (`tl/fort.js`), lấp phố ước tính 1782 có nhãn (53,9 % diện tích phố là **ước tính**), lớp sống ≥ 3 vật chuyển động (`tl/life.js`), vách bắc Rock làm sắc + vật liệu đá vôi, trời/biển sâu màu hơn. 6 khung 6 loại: **trung vị độ bão hoà 0,419** (khung sạch) / **0,414** (master, trích PNG); colorfulness 74,9 / 72,0; cạnh 22,4 / 25,1; cháy sáng 0,00–0,02 % (khung sạch). |
| M14 → B4 | Inset viết lại: góc trên trái, ≤ 12 %, 2,5–4 s, mờ 0,3 s, hộp dấu chân đỏ theo campath từng khung, vòng định vị 16 px, 1–2 nhãn, không ranh/tuyến, "Map: Natural Earth". Đo trong đoạn thử: 8,89 % khung, 3,0 s. |
| M13-lite | `hist_borders.py` (Cliopatria + đối chiếu OHM, đo lệch, mép mềm/gạch), raster phe trộn A/B theo ngày + đổi chủ từng thực thể (Minorca 1782-02-05), tuyến biển có kiểm đất + mũi tên + "route approx.", chú giải ≤ 3, bộ đếm ngày, nhãn "approx. borders c. YYYY — nguồn", log cho K. ETOPO 2022 (CC0) cho nền nổi. |
| Đoạn thử | `v5b2c-t` 57,5 s 1080p: SM2 6,5 s → hoà 0,5 s → vịnh 1782 (inset B4) · SM2 dự phòng NC-BD §2.4 7 s · phố 8 s · toàn cảnh 6 s · eo 4 s · khung neo PT 8 s. SM3 7 s riêng cho chấm độ rõ. |
| K-1.14 (q_bando, có log) | BD-1, 2, 4, 5, 6, 7, 8 **ĐẠT**; BD-3 **92,3 %** (< 95 %; khung 0 là khung đen fade-in — §3.3). |
| Chấm mù 3 vai | SM2 M13-lite **8,0** craft / **8,0** độ rõ vs dự phòng **7,0 / 5,33**; chọn M13-lite **3/3**; trả lời 4 câu "từ đâu · đường nào · khi nào · ở đâu" đúng 12/12 cả hai (bản dự phòng chỉ cho "1780–82" chung). SM3: craft 6, độ rõ 4, **3/3 đề nghị tách 1940 | 1942**. |
| Chi phí | Claude API **$0,537** (trần $3; chỉ chấm mù) · ElevenLabs 0 ký tự · YouTube 0 · giờ máy **≈ 3,0 h** (cận trên, tính theo đồng hồ tường cả phiên; trần 6 h). |

Video thử 540p (4,07 MB, **ngoài LFS**): `reports/v5b2c/khung/v5b2c-t-540p.mp4`. Tờ khung mỗi 1 s: `reports/v5b2c/khung/to-khung-moi-1s.jpg`. Master 1080p (266 MB, SHA-256 `96135699…1007680`) và SM3 (27 MB, `cc46ca77…be4dc228`) ở `/var/tmp/cine-out/` — không đẩy (> 30 MB, lệnh cấm LFS).

## §1 V0 — nâng hình (sau khi thua 0/6 trước CITYTONS/Barcelona)

### 1.1 Việc đã làm
- **a) M5 bastion tham số** — `design/k2v/tl/fort.js`: tường dốc (batter) đá ashlar, gờ cordon, lan can có lỗ châu mai loe (mỗi `embr` m, CHỈ ở cạnh hướng địch `face`), pháo trên giá gỗ + sàn ván, chòi gác (garita) ở góc nhọn, đống đạn, sàn lát đá; nhận diện mặt hậu (gorge) bằng địa hình 18 m ra ngoài. King's Bastion dựng từ bao lồi các đoạn OSM `citywalls` trong 85 m; Line Wall theo từng đoạn OSM thẳng (mặt phố có terreplein 26 m; đoạn trên vách > 18 m mỏng 1,6 m, không châu mai); Línea là tường đá thấp hướng bắc.
- **b) Lấp phố ước tính** — `scripts/k2tl/infill_1782.py`: ranh phố = Line Wall + tường nam + mép bắc khối 1782 cực bắc + mép đông lõi phố cổ AMS 1943; khối = toà 1943 (ghost SH) đóng 1,2 m trừ khối 1782 có nguồn (đệm 5 m). **115 khối, 105 484 m² ước tính / 90 149 m² có nguồn → 53,9 % diện tích phố là ước tính.** Trên hình: tông xám-nhạt lệch (`ghostDesat` 0,08, kiểu pd 3) + dòng "Grey-washed blocks: estimated infill". Log: `reports/v5b2c/do/lap-pho-1782.json`.
- **c) Bố cục** — đo mặt nạ (không đổi hình học sau khi đổi trời): phố f96 nội dung **52,7 %**, trống 17,4 %; toàn cảnh f72 55,8 % / 28,7 %; vịnh f132 66 % / 27,9 %; vịnh hero f192 60,6 % / 19,0 %. Ngoại lệ có chủ đích: khung trận trên vịnh (nước ≈ 45 %), khung eo đất (trời 58 %).
- **d) Màu** — vibrance 0,35 → 0,62 (`GRADE` theo cảnh), ngói terracotta bão hoà hơn, ashlar ấm, ghost desat 22 % → 8 % (**đổi thiết kế, cần duyệt**), và (vòng này) **trời chân trời sâu hơn** `skyHor` [0,42 0,62 0,92] → [0,30 0,52 0,90], sương [0,46 0,65 0,91] → [0,40 0,60 0,90] ở 5 cảnh 1782. Trước đổi trời: khung eo 0,294, khung trận 0,278, trung vị 0,392; sau: 0,369 / 0,361 / **0,419**.
- **e) Đo theo cách điều phối** (`scripts/k2tl/measure_dp.py`: sat/colorfulness/FIND_EDGES, 640×360, y 60–300).
- **Rock**: DEM Copernicus đỉnh 359 m (thật ≈ 412–426 m), dốc max ≈ 54°. `terrain.sharpenCliff` (unsharp mặt dốc > 25° hướng bắc, k 1,3): 477 ô sửa, nâng tối đa 19,7 m, hạ 25,1 m; vật liệu vách đá vôi. **Chưa đối chiếu được ảnh PD** của vách bắc: tải Commons bị chặn (429/lỗi); ảnh LoC duy nhất lấy được là cảnh nhìn TỪ Rock. Đối chiếu bằng mắt còn chờ.

### 1.2 Số đo 6 khung 6 loại

| Loại | Khung | sat (sạch) | colorful | cạnh | sat (master PNG) |
|---|---|---|---|---|---|
| 1 vây hãm (eo) | e_eo f48 | 0,369 | 72,3 | 15,8 | 0,369 |
| 2 cảng/bờ | a_vinh f72 | 0,431 | 81,2 | 19,6 | 0,424 |
| 3 phố dày | c_pho f96 | **0,408** | 73,5 | 30,1 | **0,404** |
| 4 hero | a_vinh f192 | 0,443 | 76,2 | 27,7 | 0,443 |
| 5 toàn cảnh đông | d_toan f72 | 0,478 | 90,8 | 25,1 | 0,455 |
| 6 bờ + chiến sự | a_vinh f408 | 0,361 | 63,9 | 17,5 | 0,369 |
| **Trung vị** | | **0,419** | 74,85 | 22,35 | **0,414** |

- "Sạch" = khung cảnh đinh không lớp chữ (đo cháy sáng đúng: 0,00–0,02 %); "master PNG" = trích từ master có lớp chữ (cháy 0,40–0,54 % là chữ trắng).
- **Ghi chú phương pháp:** trích master ra JPEG (q 2) hạ sat ≈ 0,03 (chroma subsampling): cùng 6 khung đo JPEG = 0,388. Số V5b-2b trước (0,398) là đo JPEG; đo lại bản V5b-2b bằng PNG (6 khung t 2/8/12/16/22/28) = 0,427 (có một khung thẻ 0,847 kéo lên) — so loại-theo-loại mới công bằng; đề nghị điều phối chốt cách trích (PNG).
- Khung: `reports/v5b2c/khung/v0-*.jpg`, tờ 6 khung `v0-6-khung.jpg`; số: `reports/v5b2c/do/v0-6-khung-*.json`.
- **Chưa đạt / yếu:** khung eo và khung trận vẫn dưới 0,40 (trời/biển chiếm phần lớn); người đơn lẻ (lính, người đi bộ) đo vết đỏ ≈ **4 px** trung vị ở 1080p (< 6 px của mục c; khối đội hình và tàu > 6 px) — §6 đề xuất.

### 1.3 Lớp sống + khung neo (F1/F3)
- `life.js`: chim, người đi bộ (instanced, né nhà bằng `freePath`), xuồng có vệt nước, khói bếp. Mỗi cảnh 3D 1782 ≥ 3 loại vật chuyển động (log `song` trong meta).
- `campath.neo` + `NEO_PT` = tư thế máy của phiên PT (`pt_site.py`: E −459,6 N −1139,9, cao 4,6 m, hướng 281°, nghiêng 2°, fovV 41,1°). Cảnh `neo1782`: giữ 8 s, ngày nén 07:30 → **17:40** (bản đầu 18:20 làm nền tối dưới trời còn xanh — đã sửa), đội hình tập trên Grand Parade, người qua quảng trường, khói, hải âu, xuồng.

## §2 Việc 0–5: M14, giấy phép, ranh lịch sử, raster phe, tuyến, chuyển cảnh

### 2.1 M14 → B4 (khác biệt hành vi so với AD3 của V5b-2b)

| | AD3 (V5b-2b) | B4 (V5b-2c, `scripts/k2/lib/k2.js insetLayer`) |
|---|---|---|
| Thời lượng | `true` = 4 s mặc định, 3–5 s; `'giu'` giữ suốt shot | `{t, dur}` mặc định t 0,6 s, dur 3,0 s, **kẹp 2,5–4 s**; `'giu'` **bị bỏ qua + ghi log** (`giu_bo`) |
| Mờ vào/ra | 0,4 s | **0,3 s** |
| Nơi đang xem | chấm đỏ nhấp nháy `inset_dot` | **hộp dấu chân đỏ** = vết chiếu camera từng khung (từ `frames_meta.foot` của cảnh 3D); dấu chân < 16 px → **vòng định vị 16 px** |
| Nội dung | tuyến `inset_route` + ranh `inset_bien` nếu khai | **không ranh, không tuyến**; chỉ bờ NE + 1–2 nhãn `inset_labels` |
| Nguồn | không có dòng nguồn riêng | "Map: Natural Earth" trong inset |
| Log | `LL.inset {box, area_pct, a, map, src, bien, route}` | `LL.inset {box, area_pct, t, inset_goc, ly_do, foot_px, vong_dinh_vi, giu_bo}` |

Bản đồ inset mới `design/k2v/inset/eo-gib.json` (bbox −6,35…−4,4°Đ, 35,6…36,5°B; NE 10 m land + minor islands). Trong đoạn thử: t 7,1–10,1 s, hộp [110, 198, 670, 517] (8,89 %), dấu chân 76,7 px.

### 2.2 Giấy phép ETOPO 2022
`reports/v5b2c/giay-phep/ETOPO-2022.md`: CC0-1.0 nguyên văn, SHA trang, SHA **đủ 9 ô** 15″ đã dùng (N30/N45/N60 × W030/W015/E000).

### 2.3 `scripts/k2/hist/hist_borders.py`
Đặc tả → `idx.png` (chỉ số thực thể), `edge.png` (khoảng cách mép), `entities.json`, `lop-ranh.json` (manifest BD-4), `meta.json`, `ranh.geojson`. Nguồn chính Cliopatria v0.2.1 (CC BY 4.0, zip SHA-256 `d71bde2e…`), đối chiếu OHM; lệch đo **chỉ trên ranh giữa hai chính thể** (bỏ bờ biển/mép khung). Lệch > 4 px → `kieu_mep: mem` (mép mềm 10 px) hoặc `gach`.

| Lớp | Thực thể | Lệch TB | px ở khung | Kiểu mép |
|---|---|---|---|---|
| sm2-1782 | Spain | 11,66 km | 15,4 | mem |
| | France | 13,4 km | 17,8 | mem |
| | Portugal | 4,13 km | 5,47 | mem |
| sm3-1941 | Spain | 3,61 km | 2,77 | lien |
| | Portugal | 3,04 km | — | lien |

Manifest lớp SM2: `lech_tb_px` 17,77 → `mem` (BD-4 ĐẠT).

### 2.4 Raster phe + đổi chủ (E3–E5, B6)
`relief.js opt.borders`: tô màu phe giữ nền nổi, mép ranh theo px màn hình, mép mềm khi `mem`, gạch 45° ≥ 6 px theo màn hình cho `ve: gach` (E4), bảng màu theo ngày trộn A/B 0,35 s; đổi chủ từng thực thể (Minorca → Spain đúng 1782-02-05; Tangier → Tây Ban Nha 1940-06-14 gạch; Pháp chiếm đóng → xám gạch 1940-07-01). Màu B6: Britain #b03a2e, Spain #c9a227, France #2e5c8a, trung lập #a89f8a (cũng áp vào `layers.FACTION` của cảnh 3D — **đổi màu phe cũ, cần duyệt**).

### 2.5 Tuyến biển
Tuyến lấy từ `routes.geojson` gói TUYẾN @434a90f (git show, không merge), cắt/thưa, mũi tên 2D + viền, `dim` (tuyến trước mờ 30 % — E3), nhãn bám đầu tuyến "route approx.". Chú giải ≤ 3 + nhãn "approx. borders …" trong `k2.js stratLayer`.
- **Ven bờ (lệnh E):** `scripts/k2/hist/route_coast.py`, `reports/v5b2c/do/tuyen-ven-bo-sm{2,3}.json`.
  - SM2: khoảng cách bờ nhỏ nhất Rodney 1,88 km, Darby 1,88 km, Howe 2,91 km → **0 km dưới 1,5 km**. Nửa nét 6,5 px ở 0,755 km/px = 2,45 km → nét **chạm bờ trên hình 4,5 km** (Rodney, Darby, quanh eo biển); cuối cú zoom (0,156 km/px, nửa nét 0,51 km) không chạm.
  - SM3: dưới 1,5 km chỉ ở lối vào cảng: Gibraltar 4,0 km, Casablanca 3,5 km, Funchal 3,0 km, Fedala 5,5 km, Oran 3,5 km, Algiers 2,5 km (đều trong đệm cảng 5 km của BD-6).
- Đường không Torch (Gibraltar → Tafaraoui, nét đứt) + 3 mũi tên biển vào từ mép, Gibraltar "Allied HQ" (E2).

### 2.6 Chuyển strategic → 3D
Cú zoom duy nhất 5,9 → 7,0 s (1 450 → 300 km), hướng kết 71° = hướng khung 0 của `vinh1782`; hoà 0,5 s ở 6,5 s. Khung giữa hoà: `reports/v5b2c/khung/hoa-sm2-vinh.jpg`. Bộ đếm SM2 tắt trước hoà (6,3 s) để không chồng đồng hồ cảnh 3D.

## §3 Đoạn thử và số đo

### 3.1 Cấu trúc (`reports/v5b2c/doan-thu/episode.yaml`, sinh bằng `mk_ep_v5b2c.py` từ `sm2-spec.json`)
a 24,5 s (SM2 0–6,5 s + vịnh 3 plate, inset ở plate đầu) · b 7 s dự phòng · c phố 8 s · d toàn cảnh 6 s · e eo 4 s · f neo 8 s. SM3: `episode-sm3.yaml` (`mk_ep_sm3.py`). Không lời; nhạc `Tyrant.mp3` (dòng RIGHTS K2-MUS có sẵn).

### 3.2 Tốc độ dựng (llvmpipe, 4 lõi)
Cảnh đinh (3 tiến trình song song): vinh 2,87 s/khung, phố 3,77, toàn cảnh 3,70, eo 3,91, neo 2,57, SM2 3,22, SM3 ≈ 3,8 (1 tiến trình). Lớp 2D: 0,23–0,76 s/khung. Lần dựng đủ cuối (đổi trời): 29 min 54 s tường.
Đồng bộ dấu (stamp) cảnh đinh: 6 cảnh dựng xong trước khi đặc tả 2D đổi được gán dấu mới thay vì dựng lại (mã dựng không đổi — log `reports/v5b2c/do/stamp-sync.json`); sau đó toàn bộ cảnh tl đã dựng lại thật vì đổi trời.

### 3.3 K-1.14 (`checks` @b92d4da, LOCK 1.14.0 KHỚP; chạy từ bản `git archive`, không đọc mã)
Đầu vào xuất theo §9: `reports/v5b2c/doan-thu/bd/{lop-ranh.json, routes-ve.geojson, claims.json, inset.log.json}` (`scripts/k2/hist/export_bd.py`, từ dữ liệu thật).

`q_bando.py … --logs` (`reports/v5b2c/do/q_bando.txt`):

| Mã | Kết quả | Số |
|---|---|---|
| BD-1 | ĐẠT | 1 shot, 6,5 s = 11,3 % phim, hợp lệ định nghĩa (nghiêng 28°, 1 500→300 km) |
| BD-2 | ĐẠT | phong toả từ 0,0 s, tuyến 0,6–6,4 s |
| BD-3 | **TRƯỢT (sát ngưỡng)** | **12/13 khung = 92,3 %** < 95 %. Khung thiếu là **khung 0** — khung đen của fade-in 6 khung đầu tập (nhãn đã vẽ nhưng khung đen, log chữ không ghi). Mọi khung có hình đều có nhãn (cap 27,6 px ≈ cỡ 38 px). Không sửa bằng cách bỏ fade-in; đề xuất K loại khung mờ-từ-đen (§6). |
| BD-4 | ĐẠT | lech 17,77 px, mem, CC-BY-4.0 / đối chiếu CC0 |
| BD-5 | ĐẠT | không lớp biên hiện đại |
| BD-6 | ĐẠT | 3 tuyến biển, 0 cắt đất ngoài đệm cảng; claim đủ (12/12) |
| BD-7 | ĐẠT | 3 phe, 0 đổi màu |
| BD-8 | ĐẠT | 8,89 %, 3,0 s, góc trên trái. Lưu ý: hộp bắt đầu y 198 (dưới 2 dòng nguồn của cảnh 3D) — q_bando chấp nhận; chủ dự án xác nhận ý "góc trên trái" có tính chồng dưới dòng nguồn. |

`k2check.py` toàn tập (`reports/v5b2c/do/k2check-1.14.txt`, không truyền log → BD-3/BD-8 THIẾU ở bảng này): NC-H1 ĐẠT, NC-H3 ĐẠT (≤ 60 km 76,8 %), NC-H4 ĐẠT, NC-H2 **TRƯỢT do đoạn b** (bản dự phòng là `type: map` → 7,25 s tầm cao > 3 s; strategic hợp lệ được loại đúng) — đây là thêm một lý do bản dự phòng không dùng được nguyên trạng. Q37, Q26b, Q26b-K2, ML1 trượt — đặc thù đoạn thử ghép (không lời, nhịp dài, vịnh chiếm 31 %). A1 −14,1 LUFS (sát ngưỡng −13,8, công cụ tự nêu); A2 −0,0 dBTP BÁO.

### 3.4 Chỉ số trong ±5 % quanh ngưỡng (luật cứng)
- sat trung vị 6 khung **0,419** (sạch) và **0,414** (master PNG) vs 0,40: +4,8 % / +3,5 %; khung phố 0,408 (+2 %); master đo JPEG 0,388 (−3 %).
- Nội dung khung phố **52,7 %** vs ≥ 50 % (+5,4 %, ngay ngoài biên — nêu vì sát).
- BD-3 **92,3 %** vs 95 % (−2,8 %).
- A1 −14,1 LUFS vs trần −13,8.

## §4 Chấm mù (`reports/v5b2c/blind_v5b2c.py`, `kiem-mu/score.json`)
Giao thức blind_g2: `claude -p` ghim claude-sonnet-5-5 (máy chủ có gọi kèm claude-haiku-5-5 $0,0002/lượt — ghi trong sổ), chỉ công cụ Read, thư mục tạm chỉ chứa ảnh, 3 vai R1–R3 của `blind_v2.py`. Bản đồ là chuyển động → mỗi bản = **4 khung theo thời gian** (1,6/3,6/5,3/6,3 s). Mô tả cho người chấm trung tính ("an animated historical strategic map") để không lộ đáp án; nhãn phiên bản ẩn (X/Y theo hạt giống 20261018: dự phòng = X, M13-lite = Y). Độ rõ chấm bằng đáp án khai trước (từ khoá).

| SM2 | craft | đọc | độ rõ | đúng 4 câu | cờ |
|---|---|---|---|---|---|
| M13-lite | **8, 8, 8** (8,0) | 7,33 | **8,0** | 12/12 | — |
| Dự phòng §2.4 | 7, 7, 7 (7,0) | 7,0 | 5,33 | 12/12 | confusing |

- Chọn M13-lite **3/3**; lý do chung: ngày riêng từng đoàn, chú giải màu, mũi tên hướng, dấu Gibraltar rõ. Cả hai đều trả lời đúng "từ đâu/đường nào/ở đâu"; khác biệt ở "khi nào" (dự phòng chỉ "1780–82").
- Góp ý cho bản yếu (dự phòng) đều là thứ M13-lite đã có; một góp ý chung đáng làm cho M13-lite: tách nhãn Howe khỏi nhãn Gibraltar ở khung cuối (đã đổi `side: auto` cho điểm Gibraltar — khung cuối hiện không chồng, xem `sm2-m13-4khung.jpg`).

| SM3 (đơn) | craft 6, 6, 6 · độ rõ 4, 4, 4 · đọc 6,33 · đúng 12/12 · cờ: cluttered, confusing, text_overlap, too_many_things_at_once · **tách: 3/3** |
|---|---|

Lý do tách (cả 3): sơ tán dân 1940 và đổ bộ 1942 là hai câu chuyện khác hướng, khác tác nhân, cách 2,5 năm; một shot buộc người xem học lại bản đồ. Theo E-SM3 → đề xuất tách (§6). Trước chấm đã sửa 3 lỗi hiển nhiên (nhãn chồng "German-occupied"/"to London", nhãn tuyến ra mép đè nhãn ranh, bờ Bắc Phi rơi khỏi khung 1942 → lia nam cùng tầm); không sửa sau chấm.

Chi phí: 6 lượt, **$0,537** (`kiem-mu/cost.jsonl`).

## §5 Giờ máy và chi phí thật
- Giờ máy ≈ **3,0 h** = đồng hồ tường cả phiên 23:27 → ≈ 02:30 (cận trên; phần dựng/đo thật ≈ 2,0 h: thử V0 ≈ 0,5 h, nền nổi + ranh ≈ 0,2 h, 4 lần dựng đoạn thử ≈ 1,2 h, SM3 chạy song song). Trần 6 h.
- Claude API $0,537 (trần $3). ElevenLabs 0 (prep ghi `el` gửi 0). YouTube 0.

## §6 Đề xuất (ưu · nhược · tác động · rủi ro)

| # | Đề xuất | Ưu | Nhược | Tác động | Rủi ro |
|---|---|---|---|---|---|
| 1 | Dùng **M13-lite** cho SM1–SM3 của T3, bỏ dự phòng §2.4 | Chấm mù 8,0 vs 7,0, độ rõ 8,0 vs 5,3; BD-1…8 đạt (trừ BD-3 khung fade) | Mỗi shot thêm cảnh đinh ≈ 12 min máy; cần ranh từng mốc năm | Bản đồ T3 có ngày/màu phe/chú giải đúng luật | Ranh Cliopatria lệch 12–13 km ở Pháp/TBN (đã mép mềm + nhãn approx.) |
| 2 | **Tách SM3** thành 1940 (3,5 s) và 1942 (3,5 s), máy khoá, 1 nhóm nhãn mỗi shot | 3/3 người chấm đề nghị; độ rõ hiện 4/10 | Thêm 1 shot strategic (BD-1 c: ≤ 2/chương — cần xếp chương) | Rõ hơn đúng chỗ yếu nhất | Tổng strategic T3 tăng (vẫn ≪ 15 %) |
| 3 | K: BD-3 **loại khung mờ-từ-đen** khỏi mẫu số (hoặc chỉ tính khung có độ sáng > ngưỡng) | Bỏ trượt giả ở đầu tập | K phải sửa luật (phiên K) | BD-3 phản ánh đúng ý "nhãn có mặt khi ranh hiện" | Không |
| 4 | Ở phim: SM2 (kết "Oct 1782") **không hoà thẳng** vào cảnh vịnh 13/9/1782 như đoạn thử | Tránh lùi ngày (Oct → 13 Sep) mà đoạn thử đang có | Đoạn thử theo lệnh vẫn ghép thế | Liền mạch thời gian | Không |
| 5 | Chuẩn **LOOK trời sâu** (skyHor 0,30/0,52/0,90) cho mọi cảnh 3D ngoài trời Địa Trung Hải | +0,07–0,08 sat ở khung trời/biển, nhìn "nắng" hơn | Dựng lại cảnh cũ nếu dùng lại | Đẩy trung vị qua 0,40 không thêm vật | Trời gắt quá ở cảnh chiều (cần LOOK riêng) |
| 6 | **Tăng cỡ người** ở tầm ≥ 150 m (lính/người đi bộ ≥ 6 px) hoặc chỉ hiện người ở tầm gần, tầm xa dùng khối | Đạt mục c (≥ 6 px) | Phóng to quá → sai tỷ lệ | Đám đông đọc được ở 1080p | Nhìn "đồ chơi" nếu > 1,5× |
| 7 | Gửi P các dòng RIGHTS: ETOPO 2022 (CC0-1.0), Cliopatria v0.2.1 (CC BY 4.0, ghi công Seshat), OpenHistoricalMap (CC0, chỉ đối chiếu, không vẽ), Natural Earth (PD) | Đủ điều kiện tài sản | — | Bắt buộc trước phát hành | Không |

## §7 Việc đang chờ chủ dự án
1. **Duyệt V0** (ảnh `reports/v5b2c/khung/v0-*.jpg`, video 540p) và 3 đổi thiết kế: ghost desat 22 % → 8 %; trời sâu hơn ở cảnh 1782; màu phe B6 thay màu `layers.FACTION` cũ.
2. **Lấp phố ước tính 53,9 %** diện tích phố (có nhãn "estimated infill") — chấp nhận tỷ lệ này hay giới hạn lấp ở khung xa.
3. Quyết **tách SM3** (đề xuất 2) và **chuỗi SM2 → cảnh kế** ở phim (đề xuất 4).
4. Ghi `AUTHORSHIP.md` (P ghi): các lựa chọn của chủ dự án đã duyệt B1–B8/E1–E9/F1–F8/I1–I8 được áp ở đây; chọn khung neo PT; chọn ranh mép mềm cho Pháp/TBN 1782.
5. Dòng RIGHTS (đề xuất 7) — P thêm (phiên xưởng không sửa `RIGHTS.md`).
6. Phiên K: BD-3 khung fade (đề xuất 3); xác nhận nghĩa "góc trên trái" của BD-8 khi có dòng nguồn ở góc.
7. Đối chiếu vách bắc Rock với ảnh PD (chưa tải được ảnh; cần nguồn ảnh cho phép).
8. Nhánh: đổi tên `ccr-11686158-4ucx09` → `v5b2c` nếu cần (P).

## Phụ lục — tệp chính
- Mã: `design/k2v/tl/{fort,life}.js` (mới), `layers.js`, `terrain.js`, `page.js`, `water.js`, `city.js`, `campath.js`, `scenes/{vinh,pho,eo,toan,neo}1782.js`; `design/k2v/relief.js`; `design/k2v/hist/sm{2-1782,3-1941}.json`; `design/k2v/inset/eo-gib.json`; `scripts/k2/hist/{hist_borders,sm2_spec,sm3_spec,mk_ep_v5b2c,mk_ep_sm3,export_bd,route_coast}.py`; `scripts/k2/lib/k2.js` (stratLayer, insetLayer B4, điểm `side: auto`); `scripts/k2/render.js`; `scripts/k2/relief_build.py` (ETOPO); `scripts/k2/inset_build.js`; `scripts/k2/build.sh` (ghép tập 1 đoạn); `scripts/k2tl/{infill_1782,measure_dp}.py`.
- Số đo: `reports/v5b2c/do/`. Khung: `reports/v5b2c/khung/`. Chấm mù: `reports/v5b2c/kiem-mu/`.
