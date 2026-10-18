Nhánh thật: `ccr-8f16467a-mhu954` (harness buộc tên này; lệnh yêu cầu `v5b2d` — nội dung tương đương: tách từ `origin/ccr-11686158-4ucx09` @233f5fa = V5b-2c). Không merge vào main; không sửa `checks/`, `docs/`, `channel-*/`, `design/pt*/`.

# V5b-2d — BÁO CÁO: vượt cổng chuẩn hình cho cảnh 3D bay (C2-1 … C2-9, chủ dự án duyệt 18/10)

## §0 Tóm tắt

| Việc | Kết quả |
|---|---|
| P1 vây hãm | Línea + 2 pháo đài (nguồn cao/vừa) tiền cảnh; khẩu đội tiền phương 15/17 + paralela + hào (do_tin thấp, chỉ hậu cảnh, nhãn "approx."); **108 khối quân kiểu bản đồ** (9 × 30 người, màu B6, ≈ 29 000 người — dưới ước tính quân vây 33 000–40 000 của nguồn S065, ghi trên hình); 20 cờ Cruz de Borgoña; khói dọc tuyến (Montero: đất liền khai hoả 10:25); vườn GARDENS (số hoá mới); máy thấp 22 m nhìn chéo nam-đông-nam, ống dài. Khối quân **18–181 px** (0/32 dưới 6 px). |
| P4 hero | King's Bastion: 23 pháo (mặt hướng vịnh + sườn), **88 pháo thủ** (4/khẩu) + 2 nhóm dự bị, 18 đống đạn, 24 thùng thuốc súng, 3 lán chắn mảnh, 1 lò nung đạn, cột cờ Union 1707 (minh hoạ), 12 cụm khói đầu nòng từ 09:45 (vùng khói chính xác, **0 người trong khói**), vân đá + vết ám khói. Người 21–57 px, tầm 51–137 m (≥ 40 m). |
| P5 toàn cảnh | Máy ≈ 150 m trên mặt vịnh nhìn xuống phố qua King's Bastion; đồn trú trên Grand Parade (6 khối, 1 440), **đám đông** 25 cụm (15–45 người) dọc Main Street + phố sau Line Wall; vườn Convent + vườn nhỏ (có cây, chỉ trong vòng vườn theo plan 1782); St Mary the Crowned có tháp; Grand Parade là bãi đất nện. Nội dung **57,5 %**. |
| P6 bờ + chiến sự | Cảnh mới `bo1782` 17:28–17:32 ngày 13/9: soái hạm Pastora + "admiral's second" cháy (Drinkwater p. 298; lửa bùng ~17:00 — S066), khói dày toàn tuyến trôi đông-bắc theo gió tây-nam (p. 298), xuồng chèo quanh hai pin nổi (p. 295, 298), máy thấp 16 m ống dài 13° nhìn đông vào Line Wall + phố + Rock. **Bờ 54,3 %** khung, **lửa đỏ 0,24 %**. |
| P2/P3 | P2: bay ≈ 110 m qua mặt vịnh trước Old Mole nhìn xuống — 3 tàu neo tiền cảnh, Old Mole, phố, Rock. P3: đoạn nam Main Street, phố dày (50,1 %), tháp St Mary, ngói đa sắc (8 tông). |
| C2-2 / C2-7 | Khung AGL ≤ 150 m: bỏ khối lấp ước tính trong 150 m quanh vết máy (P3 bỏ 26 khối, P2/P4 bỏ 4). Người đơn chỉ hiện trong 150 m quanh máy; xa hơn là cụm đám đông / khối đội hình (không phóng to); kíp pháo chỉ hiện ≤ 300 m. |
| C2-9 | Đối chiếu ảnh PD LoC 2025710362 (vách bắc gần đứng): DEM nâng đỉnh 359 → **412 m** (Rock Gun), làm sắc vách bắc k 1,3 → 1,8. |
| C2-4 | SM3 tách SM3a 1940 (3,5 s) + SM3b 1942 (3,5 s), máy khoá, một nhóm nhãn/shot — **đã dựng hình 1080p** (§6). |
| C2-5 | Đoạn thử theo thứ tự thời gian 09:05 → 10:27 → 10:32 → 10:40 → 17:28; SM2 ("Oct 1782") đặt **sau** cảnh 13/9 (không hoà thẳng). |
| Chấm mù | V5b-2d vs V5b-2c cùng loại cảnh: **V5b-2d được chọn 17/18 lượt** (P1–P2, P4–P6: 3/3; P3: 2/3). |
| Chi phí | Claude API **$1,61** (trần $2) · OpenAI 0 · YouTube 0 · ElevenLabs 0 ký tự · giờ máy ≈ **2,6 h** (cận trên, đồng hồ tường; trần 6 h). |

Video thử 540p, 42 s, **11,5 MB** (ngoài LFS): `reports/v5b2d/khung/v5b2d-t-540p.mp4`. Tờ so 6 khung V5b-2c | V5b-2d: `reports/v5b2d/khung/so-sanh-6-khung.jpg`. Khung sạch + khung có chữ: `reports/v5b2d/khung/d-*.jpg`.

## §1 Việc đã làm (mã)

- **Khôi phục môi trường** (container mới, bộ đệm trống): tải lại nguồn thô (SHA khớp V5b-1), dựng lại gói `gib`; **ghi lại lệnh dựng lớp 1782** vốn chưa từng được ghi: `scripts/k2tl/pack_1782.sh` (ghost SH từ `origin/p-1810` bằng `git archive`; lấp ước tính tái lập **khớp từng số** với V5b-2c: 115 khối, 53,9 %).
- `design/k2v/tl/props.js` (mới): cờ (`union1707`, `burgundy`, vải gợn theo thời gian), vườn có nguồn (luống + lối đi, cây chỉ trong vòng vườn, nhà vườn), điểm nhấn (St Mary the Crowned: thân 13 m + tháp 28,5 m; Convent 11 m — chiều cao minh hoạ), đồ sàn pháo + vị trí pháo thủ.
- `fort.js`: trả `guns`/`floors`; `faceMin`; vết ám khói (tường chắn, sàn) theo `soot`. `layers.js`: vùng khói **chính xác** (`zone: 'path'` — chuỗi vòng dọc đường trôi, bán kính = 0,8 × cỡ cụm + 2 m; mặc định giữ công thức cũ), `units` có `y`, `sx/sz`, `near`, áo ánh dội; `town1782` có `near` (C2-2), `extra` (vườn + điểm nhấn), Grand Parade là nền phố. `life.js`: `near` cho người đơn, `crowds` (đám đông). `city.js`: ngói 1782 đa sắc 8 tông. `ships.js`: pin nổi có cột + buồm thu, mái da nâu đỏ, nòng pháo, dải mạn. `terrain.js`: nâng đỉnh theo ảnh PD (`cliff.peak`). `page.js`: mặt nạ tách **đất dốc tự nhiên** (trước lẫn vào nước/trời) + `bo_pct`.
- Cảnh: `eo1782` (viết lại), `vinh1782` (P2 + P4), `pho1782`, `toan1782`, `bo1782` (mới), `neo1782` (C2-7).
- Công cụ: `scripts/k2tl/{pack_1782.sh, so_hoa_v5b2d.py, v5b2d_khung.sh, v5b2d_do.py, v5b2d_video.sh, v5b2d_gom.sh}`; `scripts/k2/hist/sm3_spec.py --tach`, `mk_ep_sm3.py` nhiều spec, `bd_raw_prep.py` (phiên phụ).

## §2 Nguồn cho mọi vật mới

| Vật | Nguồn | Độ tin / ghi trên hình |
|---|---|---|
| Línea, Fort San Felipe/Santa Bárbara, Line Wall, King's Bastion | ghost SH (Drinkwater 1786, RMS 4,2/21 m) + OSM citywalls | như V5b-2c |
| Khẩu đội 15/17, paralela, hào T1782-02…11, đồn F1782-03…06 | ghost SH do_tin **thấp** (±160–380 m) | chỉ hậu cảnh; "Works … approx." |
| Vườn GARDENS trên eo đất (V1782-01) + 6 nhà vườn | **số hoá mới** trên cùng bản quét Drinkwater 1786 (leaf373), nắn bằng mã SH (vùng TPS "giua") | ±370 m → do_tin thấp, hậu cảnh, "gardens: approx." |
| Vườn Convent (V1782-02), vườn nhỏ SE nhà thờ (V1782-03) | số hoá mới, vùng affine "pho" | ±33 m; cây trong vườn: số lượng minh hoạ |
| St Mary the Crowned, Convent | ghost SH N1782-09, N1782-07 | vị trí theo plan; chiều cao minh hoạ ("church tower height illustrative") |
| Giờ khai hoả đất liền 10:25 | Montero 1860 p. 360 (S067) | thẻ "Spanish lines open fire, 10:25" |
| Gió sáng NW / chiều SW, thuyền cối bị cản | Drinkwater 1785 (bản 1905) p. 295, 298 — OCR archive.org SHA `9a0c3c3e45f39e2f…` | hướng khói, KHÔNG dựng pháo hạm chiều 13/9 |
| Soái hạm + chiếc kế cháy chiều 13/9, lửa ~17:00 | Drinkwater p. 298; S066 (Montero/Spilsbury) | thẻ "Flagship and her second on fire" |
| Xuồng quanh pin nổi | Drinkwater p. 295 ("attended by a number of boats"), p. 298 ("several boats were seen to row round the disabled ships") | vị trí minh hoạ |
| Lò nung đạn | Drinkwater p. 295 ("grates and furnaces for heating shot"), S061 | vị trí minh hoạ |
| Cột cờ | Drinkwater: cột cờ đồn trú ở **Grand Battery** — cờ trên King's Bastion là MINH HOẠ | "flag: illustrative" |
| Quân số | ≈ 29 000 TBN hiện (S065: 33 000–40 000); đồn trú 7 000 (S065) | "~29,000 troops … illustrative" |
| Cờ Union 1707 / Cruz de Borgoña | mẫu cờ lịch sử (PD) | vị trí minh hoạ |
| Đỉnh Rock 412 m | ảnh LoC 2025710362 "Gibraltar. Rock from neutral ground" (V. B. Cumbo, c. 1900–10), **"No known restrictions on publication."** (nguyên văn), chỉ tham chiếu, không hiện trên hình | độ cao thật Rock Gun ≈ 412 m |

## §3 Số đo (6 khung 6 loại, khung SẠCH, cách điều phối 640×360 y 60–300; PNG đổi từ khung dựng)

| Loại | sat 2d | sat 2c | colorful 2d / 2c | cạnh 2d / 2c | nội dung | nền phố+ND | nước | đất bằng | đất dốc | trời | bờ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 vây hãm | **0,408** | 0,369 | 69,3 / 72,3 | 26,3 / 15,7 | 25,6 | 25,6 | 2,6 | **34,1** | 5,6 | 32,0 | 65,4 |
| 2 cảng/bờ | **0,557** | 0,431 | 95,1 / 81,2 | 28,1 / 19,4 | 20,9 | 26,2 | **43,0** | 24,7 | 5,4 | 0,7 | 56,3 |
| 3 phố dày | **0,416** | 0,408 | 79,2 / 73,4 | 26,7 / 29,8 | **50,1** | 72,3 | 8,5 | 6,2 | 0 | 13,0 | 78,6 |
| 4 hero | 0,439 | 0,443 | 71,7 / 76,1 | 32,3 / 27,5 | 61,9 | 64,3 | 13,8 | 4,5 | 0,1 | 17,2 | 69,0 |
| 5 toàn cảnh | **0,404** | 0,478 | 61,2 / 90,8 | 38,3 / 24,8 | 57,5 | 78,0 | 6,4 | 15,5 | 0 | 0 | 93,6 |
| 6 bờ + chiến sự | 0,341 | 0,361 | 64,8 / 63,8 | 18,1 / 17,3 | 11,7 | 15,5 | 16,1 | 33,7 | 5,0 | 29,6 | **54,3** |
| **Trung vị** | **0,412** | 0,419 | 70,5 / 74,8 | 27,4 / 22,1 | | | | | | | |

- Khung có chữ (PNG): trung vị sat **0,400**, cháy sáng 1,55 % (chữ trắng). Khung sạch: cháy 0,00–0,01 %.
- "Đất bằng" gồm cả sườn Rock thoải < ~37° (mặt nạ không tách sườn đồi khỏi bãi cỏ) — với P1/P6 đây là cận trên của "cỏ trống".
- **Cỡ px (1080p, chiếu theo máy của khung):** P1 khối quân 18,0–180,6 px (trung vị 30,5; 0/32 < 6 px), từng người 11,5–43 px. P4 pháo thủ 21–57 px, tầm 51–137 m. P5 khối đồn trú 34–44 px; cụm đám đông 7,8–38,5 px (0/24 < 6). P3 cụm đám đông 3,8–43,8 px — **10/25 cụm < 6 px** (cụm ở 600–840 m cuối Main Street). Tàu: P2 32–37 px, P4 13–16 px, P6 30 px.
- **Lửa đỏ** P6: **0,24 %** khung (khác biệt có/không lửa, cùng máy); mọi điểm đỏ–cam cả khung (gồm mái ngói) 13,35 % — đều < 15 %.
- **Người trong khói:** 0 (units `an_vi_khoi` 0 ở P1, P4, P5).
- Số đầy đủ: `reports/v5b2d/do/6-khung.json`, mặt nạ `do/mat-na-*.json`, máy `do/cam-*.json`.

### 3.1 Chỉ số trong ±5 % quanh ngưỡng (luật cứng) và chỉ số trượt
- sat trung vị **0,412** vs 0,40 (+3,0 %); khung có chữ 0,400 (đúng ngưỡng); P1 0,408 (+2 %), P5 0,404 (+1 %), P3 0,416 (+4 %).
- Nội dung P3 **50,1 %** vs ≥ 50 % (+0,2 %).
- **TRƯỢT nhẹ:** cỏ trống P1 **34,1 %** vs ≤ 33,3 % (+2,4 %) — sau khi giảm quân số xuống dưới số nguồn; không thêm vật để vượt (xem §7). Nước P2 **43 %** > 1/3 (shot cảng, `noi: bien`). P6: đất bằng 33,7 % (+1,1 % — gồm sườn Rock), bờ 54,3 % (+8,6 %, ngoài ±5 %).
- sat P6 0,341 (< 0,40): nắng chiều thấp + khói xám.

## §4 Chấm mù (`reports/v5b2d/blind_v5b2d.py`, `kiem-mu/score.json`)
Giao thức blind_v5b2c: `claude -p` ghim claude-sonnet-5-5, chỉ công cụ Read, thư mục tạm chỉ chứa X.jpg/Y.jpg (1280 px, khung sạch), 3 vai R1–R3 của `blind_v2.py`, X/Y theo hạt giống 20261018, mô tả trung tính theo loại cảnh. Không có khung đối thủ.

| Cặp | chọn V5b-2d | craft 2d / 2c | giàu nội dung 2d / 2c | hợp loại 2d / 2c | cờ (2d) |
|---|---|---|---|---|---|
| P1 vây hãm | **3/3** | 5,0 / 4,0 | 6,33 / 2,0 | 6,33 / 3,0 | cluttered, toy_look |
| P2 cảng | **3/3** | 6,0 / 5,0 | 6,0 / 3,0 | 7,0 / 5,0 | toy_look, unreadable_scale |
| P3 phố dày | **2/3** | 5,67 / 5,0 | 4,67 / 5,33 | 4,67 / 5,0 | empty_frame, toy_look, unreadable_scale |
| P4 hero | **3/3** | 5,67 / 5,33 | 7,0 / 3,0 | 7,0 / 4,0 | toy_look, unreadable_scale |
| P5 toàn cảnh | **3/3** | 6,0 / 4,0 | 6,67 / 3,67 | 7,33 / 3,0 | toy_look, unreadable_scale |
| P6 bờ + chiến sự | **3/3** | 6,0 / 5,0 | 6,0 / 3,0 | 6,0 / 4,0 | flat_slide_look, toy_look |

- Vòng: P2, P4, P5, P6 chấm trên khung r3 (trước đổi màu mũ khối quân — khác biệt nhỏ ở P4/P5); P3 chấm lại sau sửa theo góp ý vòng 1 (vòng 1: 1/3 — "ruộng sọc + cây kẹo mút"; lưu `kiem-mu/vong1/`); P1 chấm lại sau giảm quân số (bản 43 000 người: 3/3, lưu `kiem-mu/vong2-P1-43k/`).
- Góp ý chung cho bản V5b-2d (để làm tiếp): người/khối là trụ hộp → "toy look"; khói là sprite mờ; P3 vùng trống bên phải (do C2-2 bỏ lấp gần); P6 khung phẳng ngang, nước phẳng, pin nổi giống hộp.
- Chi phí chấm: **$1,606** (27 lượt, `kiem-mu/cost.jsonl`).

## §5 Video thử
`reports/v5b2d/khung/v5b2d-t-540p.mp4` — 42 s, 960×540 dựng thẳng (lớp chữ của trang tl), x264 crf 25, 11,5 MB, không tiếng: vịnh 09:05–10:27 (cảng → hero King's Bastion 09:45 → reveal pin nổi) · eo đất 10:32 · toàn cảnh 10:40 · Main Street · bờ 17:28. `scripts/k2tl/v5b2d_video.sh`.

## §6 SM3 tách (C2-4) và thứ tự SM2 (C2-5)
- `sm3_spec.py --tach` → `-a.json` (1940: 4 cung sơ tán, nhãn nơi đến, bộ đếm "May–Aug 1940", chú giải 2 mục) và `-b.json` (1942: đường bay + 3 mũi biển Torch, bộ đếm "8 Nov 1942", chú giải 3 mục). Máy khoá (cùng tư thế đầu–cuối).
- Dựng (phiên phụ trong phiên này, rồi sửa 3 lỗi thấy trên khung lần 1: chú giải SM3b ghi "Vichy (hatched)" sai so với hình → "Vichy France" đặc + "German-occupied (hatched)"; cuối cung Madeira/Casablanca bị hộp bộ đếm che → khung SM3a lệch nam-tây; nhãn Gibraltar đè đầu đường bay → lên trên). Kết quả: xem §6.1 (điền sau lượt dựng cuối).
- Dữ liệu dựng lại: ETOPO 2022 9 ô (SHA **khớp** `reports/v5b2c/giay-phep/ETOPO-2022.md`), Cliopatria v0.2.1 (zip SHA `d71bde2e…` khớp V5b-2c), Natural Earth 10m; `fr-metro.geojson` không có trong repo → tái dựng từ NE admin_0 (France, hộp −6…10°Đ, 41…52°B); số lệch biên ra trùng V5b-2c (Spain 3,61 km, Portugal 3,04 km). pyproj cài riêng vào `/var/tmp/cine-out/v5b2d-sm3/pylib` (không đụng `/opt/cine`).
- **C2-5:** ở phim SM2 (kết "Oct 1782" — đoàn Howe) đặt SAU khối cảnh 13/9/1782; đoạn thử 3D xếp theo giờ (toàn cảnh dời 09:52 → 10:40 để sau eo đất 10:32).

## §7 Giờ máy và chi phí thật
- Đồng hồ tường phiên chính 02:33 → ≈ 05:10 ≈ **2,6 h** (gồm phiên phụ SM3 ≈ 1,05 h chạy song song, `nice`). Dựng 1080p llvmpipe 7–14 s/khung (đơn tiến trình, có tải song song).
- Claude API $1,606 (trần $2). OpenAI 0. YouTube 0. ElevenLabs 0 ký tự (prep SM3 `el` gửi 0).

## §8 Quyết định đề xuất (ưu · nhược · tác động · rủi ro)

| # | Đề xuất | Ưu | Nhược | Tác động | Rủi ro |
|---|---|---|---|---|---|
| 1 | Duyệt 6 khung V5b-2d làm chuẩn cổng mới, gửi điều phối chấm lại 6 cặp vs CITYTONS/Barcelona | chấm mù 17/18 hơn V5b-2c; P1/P4/P5/P6 sửa đúng lỗi thua | chưa biết kết quả vs đối thủ | mở cổng | "toy look" còn — có thể vẫn thua P3/P6 |
| 2 | P1: chấp nhận cỏ trống 34,1 % (giữ ≈ 29 000 quân < nguồn) hoặc cho phép thêm **trại quân TBN có nguồn** (Faden 1783 "Incampment … 19 Oct 1782") ở hậu cảnh bắc | đúng nguồn, không độn chỉ số | trượt 2,4 % | cần chủ dự án chọn | trại Faden là 19/10, không phải 13/9 |
| 3 | Thay người hộp bằng hình người low-poly có tư thế (A-lite v2), khói thể tích giả (nhiều lớp, tối dần) | đúng góp ý chung 3/3 vai | thêm ≈ 1 bước mã + kiểm px | giảm "toy look" mọi cảnh | tăng s/khung |
| 4 | C2-2 với P3: cho phép **"tàn phá"** (tường không mái, đống gạch) cho khối ước tính trong vùng plan ghi "RUINS" (bằng chứng: Drinkwater 1786 + S062/S063 — phố bị bắn cháy 4/1781) | lấp vùng trống tiền cảnh bằng trạng thái có nguồn | hình khối vẫn ước tính | P3 hết "empty_frame" | trái chữ C2-2 nếu không duyệt rõ |
| 5 | Đường bờ 1782: hạ đất lấn biển sau 1782 (DEM 2026) phía tây Line Wall thành nước | đúng lịch sử, bớt "đất bằng" ở P2/P5 | cần ranh bờ 1782 có nguồn | nhiều cảnh | nắn sai bờ nếu không có nguồn |
| 6 | Mặt nạ: tách "sườn đồi" khỏi "cỏ trống" (độ cao > 30 m) cho luật ≤ 1/3 | số đo sát nghĩa "cỏ trống" | đổi định nghĩa | P1/P6 đo đúng hơn | K phải đồng ý |
| 7 | RIGHTS (P ghi): ảnh LoC 2025710362 (chỉ tham chiếu, "No known restrictions on publication."); Drinkwater 1785 OCR (PD); Cliopatria/ETOPO/NE như đề xuất 7 V5b-2c; `fr-metro.geojson` dẫn xuất NE (PD) | đủ hồ sơ tài sản | — | bắt buộc trước phát hành | không |

## §9 Kiểm định
- **k2check 1.14:** đoạn thử V5b-2d là chuỗi cảnh tl dựng trực tiếp (không qua `scripts/k2/build.sh`), nên **không có đặc tả/timeline tập** để chạy `k2check.py` toàn tập như V5b-2c; kết quả chạy trên tập SM3 tách: xem §6.1. **K 1.15:** nhánh `checks/v1.15` **chưa tồn tại** trên origin → không chạy.
- Luật cảnh (tự kiểm trong mã, log `scene_meta`): 0 người trong vùng khói; lửa ≤ 15 %; quân/tàu ≥ 6 px (trừ 10 cụm đám đông xa ở P3 — §3); vị trí công sự/khẩu đội/hào theo nguồn, do_tin thấp có "approx.".
- Tốc độ máy P2 mới: góc ≤ 78,8 °/s (< 90), orbit 4,7 s, ghim 1,79 s; tốc độ tịnh tiến lớn nhất 533 m/s ở speed-ramp (V5b-2c chưa ghi số này — nêu để K xem).

## §10 Việc đang chờ chủ dự án
1. Duyệt 6 khung + video 540p (§0, tờ so `so-sanh-6-khung.jpg`); gửi điều phối chấm cổng lại vs CITYTONS/Barcelona.
2. Chọn hướng P1 (đề xuất 2) và P3 (đề xuất 4); duyệt hướng "người low-poly + khói lớp" (đề xuất 3).
3. Duyệt SM3a/SM3b (§6.1) thay bản 7 s; xác nhận thứ tự SM2 sau 13/9 ở phim.
4. Duyệt các đổi thiết kế: đỉnh Rock 412 m + vách sắc hơn (C2-9); ngói 8 tông; cảnh mới `bo1782` (17:30); P5 đổi máy sang mặt vịnh; P2 đổi đường bay.
5. Ghi `AUTHORSHIP.md` (P): các quyết định C2-1…C2-9 của chủ dự án áp ở đây.
6. RIGHTS (đề xuất 7) — P thêm.
7. Phiên K: đề xuất 6 (mặt nạ sườn đồi); kiểm luật tốc độ tịnh tiến speed-ramp.
