# SH — Số hoá ghost phố Gibraltar cho T3 (1782 · 1704 · 1943)

> Phiên SH, 17/10/2026, theo lệnh chủ dự án (duyệt D5 17/10: 3 mốc 1704, 1782, 1943, lõi ≈ 1 km²). **Không merge. DỪNG chờ chủ dự án.**
> Đã đẩy sớm "1782 SẴN SÀNG" (`16cf81bd`), rồi 1704 (`064170ff`), rồi 1943 + báo cáo này.

## Khối điều lệ (lệnh + thực tế)
| Trường | Lệnh | Thực tế |
|---|---|---|
| Loại phiên | SH (xưởng số hoá) | đúng |
| Nhánh | nhánh mới `sh-ghost` từ `origin/main` @ `82a17ae` | tạo từ `origin/main` @ `82a17ae`; **đẩy lên `claude/sh-ghost-gibraltar-t3-1gkftx`** — nhánh phiên do harness chỉ định, phiên không được đẩy nhánh khác (§9 mục 1) |
| Tệp được sửa | CHỈ `channel-k2/k2c-t3-01/ghost/**` | chỉ thêm tệp trong `ghost/` (3,4 MB ≤ 20 MB). Không sửa main, `checks/`, `scripts/`, `design/`, `docs/`, tệp khác của k2c-t3-01. Chỉ **chạy** `scripts/k2tl/fetch_osm.py` và nhập `scripts/k2tl/geo.py` (UTM), không sửa |
| Trần | Claude API ≤ $1 (ghim) · ElevenLabs 0 · YouTube 0 · giờ máy ≤ 3 h | API **$0** (không gọi) · EL **0** · YouTube **0** · giờ máy **≈ 1,0 h** (phiên 13:31–14:30; tính toán thật < 10 phút) |
| Preflight | bắt buộc; che email | hook pre-commit/pre-push; mọi commit **PREFLIGHT ĐẠT**, `lock.py --verify` **KHỚP** (§8). Không có email trong tệp ghi |
| Điều kiện dừng | xong → đẩy → dừng; không hỏi giữa chừng | (1) xong việc. Câu hỏi không chặn đã tự quyết (§9) |

## 0. Tóm tắt
| Mốc | Trạng thái | Nguồn dựng | Nắn: biến đổi · điểm · **RMS khớp / RMS kiểm chéo (LOO)** | Ngưỡng | Số feature |
|---|---|---|---|---|---|
| **1782** | **XONG** | Drinkwater 1786 "Plan of the Batteries … 13 Sept 1782" | phố: affine · 9 · **21,2 / 33,3 m**; Línea: đồng dạng · 3 · **4,2 / 22,8 m**; dải giữa (công sự tiền phương): TPS · 12 · đối chiếu Faden lệch **99–157 m** | ≤ 50 m | **22 khối phố**, 13 toà, 13 công sự, 2 pháo đài, 11 chiến tuyến (61) |
| **1704** | **XONG PHẦN BẮC** | Exact Plan 1705 (Rijks CC0) | đồng dạng · 4 · **30,0 / 67,4 m** | ≤ 120 m | **26 khối phố**, 1 tháp, 6 công sự (33) |
| 1704 (Visscher) | **KHÔNG ĐẠT** → không dựng | Visscher 1706 (LoC) | affine 9 điểm 99,5 / 162 m; TPS LOO 159 m | ≤ 120 m | — |
| **1943** | **XONG** (lõi phố cổ 1,24 km² + North Front 1,17 km²) | OSM làm nền, lọc + bổ sung theo AMS M981 (Princeton, chỉ nắn) | px→lưới: affine · 24 giao điểm lưới · **1,4 / 1,7 m**; px→UTM: affine · 82 điểm (ô tương quan toà AMS↔OSM) · **6,0 / 6,3 m** | ≤ 15 m | **87 khối phố**, **570 toà** (465 OSM có trên AMS + 105 chỉ có trên AMS) (657) |

- **Giờ công:** ước TIEN-KY §3.3 là **37–47 giờ người**; thực tế phiên SH **≈ 1 giờ** (một phiên Claude Code, dò tay + tách màu + tương quan tự động). Không so được 1:1: 1704 chỉ phủ nửa bắc; 1943 dùng lọc tự động thay vì vẽ tay từng nhà (độ tin ghi theo từng toà).
- **Chỉ số trong ±5 % quanh ngưỡng:** không có (§7).
- **Việc chờ chủ dự án:** §9.

## 1. Tải lại nguồn, kiểm SHA-256 (tệp gốc ngoài git `/var/tmp/cine-out/sh/raw/`)
| nguon_id | SHA-256 (tai-san-vay-ham.json) | Kết quả | Dùng |
|---|---|---|---|
| ia-drinkwater1786-plan-batteries | `476cb89b…555117` | **KHỚP** | dựng 1782 |
| ia-drinkwater1786-plan-sortie | `c747dbc8…f167fa` | **KHỚP** | chỉ nhận dạng (nắn thử không đạt) |
| yale-2046612-faden-1783 | `598915ea…91d5c305` | **KHỚP** | đối chiếu độc lập 1782 |
| rijks-rp-p-ob-83400-exact-plan-1705 | `d7a903a6…bdbf73e` | **KHỚP** | dựng 1704 |
| loc-2008621715-visscher-1706 | `42241a7b…afe241` | **KHỚP** | nắn thử, không đạt |
| pu-ams-m981-gibraltar-1943 (Princeton) | `252ca705…a9a5e363` | **KHỚP** | chỉ nắn (D8) |
| Yale 15487373 (AMS M981, bản lên hình D8) | mới: `971cc1ee0708c55a…d113c1` (5517×8495) | tải được | **chưa dùng** — trường quyền Yale không phải "any purpose" (§5, §9) |

OSM hôm nay: API `/map` bbox −5,372…−5,330 / 36,104…36,168, 24 ô, 48 MB thô ngoài git (`/var/tmp/cine-out/sh/osm/sh/`), gộp 112 044 nút / 18 176 way.

## 2. Nắn (sổ điểm: `gcp-*.json`, toạ độ ảnh ↔ UTM 30N + id OSM; công cụ `tools/ghost.py fit`)
### 2.1 1782 — `gcp-1782-drinkwater-batteries.json`
| # | Điểm | Ảnh (px) | OSM | Vùng | Sai khớp (m) | LOO (m) |
|---|---|---|---|---|---|---|
| 1 | King's Bastion — mũi | 895, 1165 | way/952588383 | phố | 15,8 | 31,0 |
| 2 | Orange Bastion — mũi | 1333, 1268 | way/950399540 | phố | 35,0 | 51,2 |
| 3 | Montagu Bastion — tâm | 1540, 1395 | way/951936002 | phố | 35,0 | 63,2 |
| 4 | Spanish Church = St Mary the Crowned | 876, 1432 | way/167262263 | phố | 21,2 | 28,6 |
| 5 | Southport Gates | 315, 1432 | node/243847822 | phố | 3,5 | 6,4 |
| 6–7 | South Bastion — góc TB, góc TN | 365,1281 · 248,1278 | way/963314875 | phố | 17,3 · 9,4 | 23,8 · 14,6 |
| 8–9 | Grand Parade (nay John Mackintosh Sq.) — đầu tây, đầu đông | 1025,1287 · 1025,1425 | quảng trường / way/250867611 | phố | 20,3 · 9,9 | 24,1 · 13,3 |
| 10 | Fuerte de Santa Bárbara — mũi nam | 3438, 2573 | way/462725331 | Línea | 4,3 | 12,5 |
| 11 | Baluarte de San Benito | 3510, 2265 | node/12537395732 | Línea | 5,8 | 9,4 |
| 12 | Baluarte de San Fernando | 3465, 1350 | way/1253399689 | Línea | 1,5 | 36,2 |
| — | Tower of Homage, Landport (không dùng) | | | | lệch 87–153 | nhận dạng không chắc; ghi trong sổ |

- **Lý do biến đổi:** phố — affine (poly2 khớp 12,7 m nhưng LOO 131 m: quá khớp). Línea — 3 di tích gần thẳng hàng nên affine không xác định → đồng dạng (tỷ lệ 0,923 m/px khớp phố 0,917 → nhận dạng 3 bastion đúng). Dải giữa — bản khắc ghép phần phố và phần Línea lệch quay ~4°, không còn vật cố định ở giữa → TPS 12 điểm nội suy; **đối chiếu Faden 1783** (`gcp-1782-faden-doi-chieu.json`, đồng dạng 3 điểm RMS 12,5 m): Mill/Round Tower Battery 130 m, St Carlos Battery 99 / 157 m, Mahon Redoubt 280 m → dải giữa `do_tin=thấp`, sai số ≥ 160 m.
- Plan cuộc xuất kích (`gcp-1782-drinkwater-sortie.json`): affine 5 điểm RMS 70 m / LOO 269 m (phần phố quay ~12°) → **không dùng dựng**.

### 2.2 1704 — `gcp-1704-exact-plan.json` (dùng) · `gcp-1704-visscher.json` (không đạt)
| # | Điểm (chú giải Exact Plan) | Ảnh (px) | OSM | Sai khớp | LOO |
|---|---|---|---|---|---|
| 1 | T — Land Gate = Landport | 3985, 1820 | way/951660527 | 5,8 | 8,2 |
| 2 | A — St Paul's Bastion = North Bastion | 3880, 2215 | way/968308092 | 41,4 | 72,5 |
| 3 | X — The Castle = Tower of Homage | 4174, 1426 | way/950058970 | 21,1 | 73,2 |
| 4 | N — gốc Old Mole (toạ độ từ ghost 1782, ±35 m) | 4283, 2343 | không còn | 37,5 | 86,4 |

- Đồng dạng (4 bậc tự do) vì chỉ 4 điểm (affine 4 điểm: LOO 176 m). **Số điểm 4 < 7 lệnh yêu cầu:** Exact Plan chỉ vẽ phần bắc phố; không còn vật cố định thứ 5 trong khung (Water Gate, tường Barcina|Turba đã mất). Ghi rõ là giới hạn.
- **Visscher 1706** (bản đủ phố, 9 điểm gồm 2 điểm tuyến trên Line Wall): affine 99,5 / 162 m; TPS LOO 159 m; đồng dạng 122 m → **không đạt 120 m**. Bản khắc nén nửa nam ("Ville Neuve"); lần dựng thử 27 khối tách màu rơi ra biển/sườn đồi trên ảnh kiểm → loại, không commit khối.
- → Theo TIEN-KY §3.4: **phần nam phố 1704 (Turba/Ville Neuve) dùng bản đồ lịch sử phẳng**; shot 1d/1e (Old Mole) nằm trong vùng đã nắn.

### 2.3 1943 — `gcp-1943-ams.json` (24 giao điểm lưới + 82 điểm ô)
- **Bước 1 — px → lưới:** dò tự động 10 đường lưới xanh (Iberian Peninsula Zone, Lambert, 1 km), khớp đường thẳng từng đường (sd 0,4–1,7 px), giao → 24 điểm. Affine **RMS 1,43 m** (LOO 1,67) — giấy/quét gần như không méo; poly2 0,97 m (không cần).
- **Bước 2 — lưới → UTM:** thô từ 2 mốc, rồi **tương quan mặt nạ toà nhà** AMS (mực đen) với toà OSM hôm nay theo ô 160 m (bước 80 m, tìm ±25 m, nội suy dưới điểm ảnh, hệ số ≥ 0,3), lặp 3 lượt, loại ngoại lai > max(8 m; 2,5σ) — 9 ô bị loại (nơi toà thay sau 1943). Kết quả: **82 điểm, affine RMS 6,0 m, max 14,6 m, LOO 6,3 m** (poly2 5,7 / 6,6 → giữ affine). Phân bố: dải N 3 999 400–4 002 860 (Europa Flats → Casemates), RMS theo dải 5,0–6,9 m. Không có điểm ở North Front (ít toà còn tồn tại) → ngoại suy affine (bản đồ không méo theo bước 1).
- **Kiểm bằng mắt** (`kiem/1943-tren-ban-do.jpg`): khối phố cổ AMS trùng toà OSM; bờ biển Europa Point OSM trùng bờ AMS. Hai mốc tay tôi chấm thử (ký hiệu "Moorish Castle", toà "112" tưởng là đèn Europa) lệch 21 / 93 m — **là lỗi nhận dạng của tôi** (ký hiệu nhãn, không phải chân tháp; đèn thật ở "Great Europa Pt"), không phải lỗi nắn.

### 2.4 Raster nắn (ngoài git `/var/tmp/cine-out/sh/warp/`, kèm `.jgw` UTM 30N) — SHA-256 + tái tạo
| Tệp | Lưới | SHA-256 |
|---|---|---|
| `1782-batteries-pho-1m.jpg` | E 287950–288750, N 4001250–4002800, 1 m, affine phố | `17d9581d647203f3cc259e62b2486fc67f5b8cb8954a739957f2c79148e989e9` |
| `1782-batteries-tps-2m.jpg` | E 287800–290200, N 4001200–4004600, 2 m, TPS | `32c28de8f0d814a1b561b07a06b743acd76259c68123086dd3772faf0426a1b9` |
| `1704-exactplan-bac-1m.jpg` | E 287900–288800, N 4001800–4002950, 1 m, đồng dạng | `f68e2f8ec18612b4c7ef71cb2ef43ac26cac1af8a6e3a440ccce05c83081dbb2` |
| `1943-ams-princeton-1m.jpg` | E 287700–290000, N 3998400–4004300, 1 m, affine | `cfbc0aad53e5fb3d078d769280dda7645b9276f4ede6b33ff234594d7b366401` |

Tái tạo: `python -I tools/ghost.py warp <gcp.json> <ảnh gốc> <vùng> <E0,N0,E1,N1> <m/px> <out.jpg>` (vùng: `pho`/`giua` cho 1782, `bac` cho 1704, `pho` cho 1943). Ảnh gốc Visscher TIFF→JPEG và AMS TIFF(P)→JPEG chuyển bằng Pillow (cùng lưới điểm ảnh), SHA JPEG: Visscher `cc58a00e14c2cd50eb6af8bad69d2fc6b12a133b856291a578659b4f9878dccb`, AMS `9a43d27430410ae23eb05be653c67d10da1266deff18ffe79f3b99447ad04220`. JPEG mã hoá lại có thể khác byte giữa phiên bản OpenCV/Pillow; hình học tất định.

## 3. Vẽ khối (GeoJSON EPSG:4326)
Mọi feature: `moc`, `nguon_id`, `do_tin` (cao/vua/thap), `so_tang_uoc` + `cach_uoc_tang`, `loai` (khoi_pho/nha/cong_su/chien_tuyen/phao_dai); thêm `vung_nan`, `bien_doi`, `sai_so_vi_tri_uoc_m`, `dien_tich_m2`/`dai_m`, `trong_khoi`. Meta lớp `ghost`: nắn, nguồn, giấy phép, ghi công, thống kê.

| Mốc | Tệp | Cách vẽ | Tầng |
|---|---|---|---|
| 1782 | `ghost-1782.geojson` ← `so-hoa-1782-px.json` | dò tay trên ảnh phóng 3,8× có lưới; chỉ vùng có viền khối; vườn/sườn chấm không vẽ | 2 (tầng chuẩn mốc; bản đồ ghi "RUINS" → cận dưới) |
| 1704 | `ghost-1704.geojson` ← `so-hoa-1704-px.json` | tách màu vùng hồng + dò tay; 8 khối Turba ngoài vùng điểm khống chế → `do_tin=thấp` | 2 (tầng chuẩn mốc); tháp 3 |
| 1943 | `ghost-1943.geojson` ← `tools/ghost1943.py` | toà OSM có tâm phủ mực khối xây AMS ≥ 0,45 (cao) / 0,25–0,45 (vừa) → giữ hình OSM; toà OSM < 0,25 → bỏ (xây sau 1943); khối xây AMS không trùng toà OSM giữ → vẽ từ mặt nạ (đặc, dạng toà, không trên tim đường/nghĩa trang, gần phố) → `do_tin=vừa`; khối phố = hợp toà nở/co 3 m | OSM `building:levels` nếu có (12 toà), còn lại 3 (tầng chuẩn mốc 1943, khoảng 2–5) |

## 4. Kiểm chồng + thống kê (`kiem/*.jpg`, mỗi ảnh ≤ 0,63 MB)
| Mốc | Ảnh | Số khối | Diện tích khối | So OSM hôm nay | Lệch / thừa / thiếu đã rà |
|---|---|---|---|---|---|
| 1782 | `1782-pho-tren-{ban-do,osm}.jpg`, `1782-eo-dat-*.jpg` | 22 (+13 toà) | 84 663 m² | khung phố 823 toà OSM; 83 có tâm trong khối ghost; 4 khối không chứa toà OSM (K1782-08/14/17/18) | bắc phố (Irish Town→Orange's) lệch tây ~20–35 m (một phần khối lên Line Wall Road); nửa đông phố cổ hôm nay bản đồ vẽ sườn đồi không viền → không vẽ (không bịa); Línea khớp 3 di tích ≤ 6 m |
| 1704 | `1704-tren-{ban-do,osm}.jpg` | 26 (+1 tháp) | 66 083 m² | khung 649 toà OSM; 33 có tâm trong khối; 9 khối không chứa toà OSM (chủ yếu trong thành lâu đài — nay sườn trống) | khối Barcina (giữa Landport–Old Mole–lâu đài) rơi đúng phố cổ phía bắc hôm nay; Turba lệch tới ~70–90 m (ngoài vùng điểm) |
| 1943 | `1943-tren-{ban-do,osm}.jpg` | 87 | 304 355 m² | vùng 2,4 km²: 1 062 toà OSM → 465 có trên AMS, 597 xây sau 1943; **+105 toà chỉ có trên AMS**. Phố cổ trong tường: 397 OSM giữ + 52 AMS-only (OSM hôm nay 706) | **sót:** dãy nhà Devil's Tower Road, Boat House, vài toà khu Coaling Island; **thừa có thể:** vài vệt mép nghĩa trang North Front (đường viền đậm) — đều `do_tin=vừa`; toà AMS tô gạch chéo (không đặc) không được bổ sung (bảo thủ) |

## 5. Ghi công + quyền
- Mỗi GeoJSON ghi `ghost.giay_phep` và `ghost.ghi_cong`. Bản đồ: Drinkwater 1786 (PD), Exact Plan 1705 (Rijksmuseum CC0), AMS M981 (tác phẩm chính phủ Mỹ, PD; bản quét Princeton chỉ dùng nắn/bằng chứng theo D8). OSM ODbL 1.0 theo `licenses/osm-odbl-attribution.txt`: hình toà N1943-w* lấy từ OSM; toạ độ điểm khống chế các mốc lấy từ OSM. Dữ liệu dẫn xuất **không phát hành** (phim = Produced Work); trên hình ghi "Map data from OpenStreetMap (ODbL)" + `openstreetmap.org/copyright` khi lớp 1943 xuất hiện.
- **Bản Yale 15487373 (D8):** trường quyền là câu cảnh báo chung ("may be subject to the copyright law… The person using the image is liable…"), **không** phải "any purpose" như TIEN-KY giả định. Chép nguyên văn ở `quyen-yale-15487373.txt`. Tác phẩm vẫn PD (chính phủ Mỹ; nền Admiralty 1942 hết hạn Crown 50 năm) → cần chủ dự án xác nhận trước khi lên hình (§9). Ghost 1943 **không phụ thuộc** bản quét nào lên hình (chỉ hình học).
- Nhãn phương pháp đề xuất trên hình: "Reconstructed from J. Drinkwater, Plan of the Batteries, 1782" · "Reconstructed from An Exact Plan of … Gibraltar, 1705" · "Buildings: OpenStreetMap, checked against U.S. Army Map Service plan, 1943".

## 6. Bảng shot T3 dùng ghost nào
| Shot | Mốc | Ghost dùng được | Ghi chú |
|---|---|---|---|
| 0e (pha 1943) | 1943 | **ghost-1943** | phố cổ đủ |
| 0e (pha 1782) | 1782 | **ghost-1782** | |
| 0e (pha 1704) | 1704 | **ghost-1704 (bắc)** | khung push-in vào phố bắc/Old Mole; nếu khung thấy cả phố nam → nửa nam trống — chọn góc hoặc thay bằng Exact Plan phẳng |
| 1d | 1704 | **ghost-1704** | push-in từ vịnh vào Old Mole: trong vùng nắn (LOO 67 m) |
| 1e | 1704 | **ghost-1704** | orbit Old Mole: trong vùng nắn |
| 1g, 1i | 1704 | ghost-1704 + Línea-less eo đất | top-down rộng: phố nam trống → giữ cao độ thấp hoặc mờ dần mép nam |
| 2a | 1779 | **ghost-1782: Línea + 2 pháo đài** | tắt công sự tiền phương (xây 1781–82) |
| 2g | 1781 | **ghost-1782** | khối = phố sau bắn phá (bản đồ 9/1782) |
| 2j | 1782 | **ghost-1782** + OSM bastion | |
| 2m | 13/9/1782 | **ghost-1782** | tuyến tiền phương ±160 m chỉ ở hậu cảnh ≥ 1 km |
| 2q, 3a | 1783 | ghost-1782 (Línea cao; tiền phương thấp) | góc rộng cao |
| 4c, 4i | 1941–43 | ghost-1943 (toà North Front, hangar) | đường băng 1943 chưa số hoá (ngoài D5) — lấy từ raster nắn `1943-ams-princeton-1m.jpg` khi V5b-2b cần |
| 4g | 1940 | ghost-1943 | |
| 5j | 1704→2026 | 1704 tường, 1782 Línea, 1943 | |

## 7. Chỉ số trong ±5 % quanh ngưỡng
- **Không có.** 1782 phố 21,2 m (LOO 33,3) vs 50; Línea 4,2 vs 50; 1704 30,0 (LOO 67,4) vs 120; 1943 6,0 (LOO 6,3) vs 15; các giá trị không đạt (dải giữa 1782 99–157 m; Visscher LOO 159 m) vượt xa ngưỡng.

## 8. Chi phí, tệp, preflight
- Claude API **$0** · ElevenLabs **0** · YouTube **0** · mạng ≈ 0,45 GB (bản đồ 330 MB + OSM 48 MB + Yale 7 MB), ngoài git · giờ máy ≈ 1,0 h (trần 3 h). Không có `cost.jsonl` (không gọi API). Đề xuất dòng COST-LEDGER (P ghi): `SH-01,số hoá ghost 1704/1782/1943,xưởng,2026-10-17,,,,,0,1,—,0,0,≈ 1,0,,0,,,channel-k2/k2c-t3-01/ghost/SH-BAO-CAO.md,YouTube 0; không merge`.
- Tệp (tất cả trong `ghost/`, 3,4 MB): `ghost-{1704,1782,1943}.geojson`, `so-hoa-{1704,1782}-px.json`, `gcp-1782-{drinkwater-batteries,drinkwater-sortie,faden-doi-chieu}.json`, `gcp-1704-{exact-plan,visscher}.json`, `gcp-1943-ams.json`, `tools/ghost.py`, `tools/ghost1943.py`, `kiem/*.jpg` (8), `quyen-yale-15487373.txt`, báo cáo này. JSON thêm bằng `git add -f` (`channel-k2/.gitignore` chặn `*.json`) — đề xuất ngoài vùng: thêm `!k2c-t3-01/ghost/**/*.json`.
- Script dùng tạm ngoài git (`/var/tmp/cine-out/sh/tools/`: crop, overlay, tách màu, tương quan AMS) — phần cần tái tạo đã đưa vào `tools/ghost.py`/`ghost1943.py` + sổ điểm; tương quan ô 1943 tái tạo từ sổ `gcp-1943-ams.json` (đã lưu toạ độ từng ô).
- Preflight: mọi commit **PREFLIGHT ĐẠT**, `lock.py --verify` **KHỚP**; `--range origin/main..HEAD` ĐẠT trước mỗi lần đẩy. Không dùng `--no-verify`.
- Ghép thử: chỉ thêm tệp mới trong `ghost/` (thư mục mới) → không xung đột với `main`.
- Đề xuất ngoài vùng (chưa ghi): `RIGHTS.md` dòng dữ liệu ghost (OSM ODbL + 3 bản đồ); `AUTHORSHIP.md` — quyết định dùng Exact Plan thay Visscher, phạm vi 1704 nửa bắc; V5b-2b: bộ đọc GeoJSON → bản ghi `[năm, năm_ghost, cao, cốt, mái, vùng, vòng]` của `city.js` (cao = `so_tang_uoc` × 3 m; năm_ghost = `moc`; vùng 1).

## 9. Việc chờ chủ dự án
1. **Nhánh:** lệnh ghi `sh-ghost`; harness phiên chỉ cho đẩy `claude/sh-ghost-gibraltar-t3-1gkftx` → đã đẩy nhánh này. Cần tên `sh-ghost` thì P tạo từ commit cuối.
2. **1704 chỉ nửa bắc** (Exact Plan, RMS 30 / LOO 67 m, 4 điểm < 7 yêu cầu); Visscher không đạt → duyệt: (a) dùng như vậy cho 1d/1e/0e, nửa nam = bản đồ phẳng; hoặc (b) giao thêm việc tìm bình đồ 1704–1727 khác (vd Homann 1733 phố, RMS ước 90 m) để dựng nửa nam.
3. **1782 dải công sự tiền phương** ±160 m (do_tin thấp) → duyệt dùng ở hậu cảnh xa (2m, 2q) hoặc tắt.
4. **D8 — bản Yale AMS 1943:** trường quyền Yale không phải "any purpose" (`quyen-yale-15487373.txt`) → xác nhận dùng (tác phẩm chính phủ Mỹ, PD) hay tìm bản khác cho shot 4f.
5. **Ghost 1943 tự động:** đã rà mắt; còn sót vài toà (Devil's Tower Road…) và có thể thừa vài vệt mép nghĩa trang. Nếu shot 4c/4i quay cận North Front, cần 1–2 h rà tay. Đường băng 1943 chưa số hoá (ngoài D5) — giao V5b-2b hoặc phiên SH tiếp.
6. Ghi các đề xuất ngoài vùng ở §8 (RIGHTS, AUTHORSHIP, COST-LEDGER, `.gitignore`).
