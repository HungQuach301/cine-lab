# SH — Số hoá ghost phố Gibraltar cho T3 (1782 · 1704 · 1943)

> Phiên SH, 17/10/2026, theo lệnh chủ dự án (duyệt D5 17/10: 3 mốc 1704, 1782, 1943, lõi ≈ 1 km²). **Không merge.**
> Bản này là **lần đẩy sớm: 1782 SẴN SÀNG**. Mốc 1704 và 1943 đang làm — báo cáo sẽ được cập nhật ở commit cuối.

## Khối điều lệ (lệnh + thực tế)
| Trường | Lệnh | Thực tế |
|---|---|---|
| Loại phiên | SH (xưởng số hoá) | đúng |
| Nhánh | nhánh mới `sh-ghost` từ `origin/main` @ `82a17ae` | tạo từ `origin/main` @ `82a17ae`; **đẩy lên `claude/sh-ghost-gibraltar-t3-1gkftx`** — nhánh phiên do harness chỉ định, không được đẩy nhánh khác (xem §9) |
| Tệp được sửa | CHỈ `channel-k2/k2c-t3-01/ghost/**` | chỉ thêm tệp trong `ghost/` |
| Trần | Claude API ≤ $1 (ghim) · ElevenLabs 0 · YouTube 0 · giờ máy ≤ 3 h | API **$0** · EL **0** · YouTube **0** · giờ máy: cập nhật ở bản cuối |
| Preflight | bắt buộc; che email | hook pre-commit/pre-push cài đầu phiên; kết quả ở §8 |

## 0. Tóm tắt (bản sớm — 1782)
- **1782: XONG.** `ghost-1782.geojson` — 61 feature: **22 khối phố** (8 cao · 9 vừa · 5 thấp), **13 toà** tô đậm trên bản đồ, 9 công sự (King's/Orange's/Montague/South Bastion, Old Mole, Line Wall, tường nam), 2 pháo đài (San Felipe, Santa Bárbara), Línea de Contravalación + 10 nét công sự tiền phương TBN (paralela, khẩu đội 5/15/17, hào giao thông).
- **RMS thật (bản Drinkwater 1786 "Plan of the Batteries … 13 Sept 1782")**, nắn theo 3 vùng vì bản khắc ghép hai phần lệch ~4°:

| Vùng | Biến đổi | Điểm | RMS khớp | RMS kiểm chéo (LOO) | Ngưỡng 50 m |
|---|---|---|---|---|---|
| Phố trong tường | affine | 9 | **21,2 m** (max 35,0) | 33,3 m | ĐẠT |
| Línea + 2 pháo đài | đồng dạng | 3 | **4,2 m** (max 5,8) | 22,8 m | ĐẠT |
| Dải giữa eo đất (công sự tiền phương) | TPS | 12 | 1,0 m | 39,3 m; **đối chiếu độc lập Faden 1783: lệch 99–157 m** | **KHÔNG ĐẠT** → mọi nét `do_tin=thấp`, sai số ≥ 160 m |

- Kiểm chồng: `kiem/1782-pho-tren-ban-do.jpg`, `kiem/1782-pho-tren-osm.jpg`, `kiem/1782-eo-dat-tren-ban-do.jpg`, `kiem/1782-eo-dat-tren-osm.jpg`.

## 1. Tải lại nguồn, kiểm SHA-256
| nguon_id | Tệp (ngoài git, `/var/tmp/cine-out/sh/raw/`) | SHA-256 (tai-san-vay-ham.json) | Kết quả |
|---|---|---|---|
| ia-drinkwater1786-plan-batteries | `…leaf373…plan_batteries_13sep1782.jpg` (3995×2837) | `476cb89b…555117` | **KHỚP** |
| ia-drinkwater1786-plan-sortie | `…leaf267…plan_sortie_spanish_lines.jpg` (3562×2665) | `c747dbc8…f167fa` | **KHỚP** |
| yale-2046612-faden-1783 | `yale_2046612_faden_1783_spanish_works.jpg` (10313×6960) | `598915ea…a91d5c305` | **KHỚP** |

OSM hôm nay: API `/map` (bbox −5,372…−5,330; 36,104…36,168), 24 ô, 48 MB thô ngoài git (`/var/tmp/cine-out/sh/osm/sh/`), gộp `osm.json` (112 044 nút, 18 176 way), dùng `scripts/k2tl/fetch_osm.py` (chỉ chạy, không sửa).

## 2. Nắn 1782
### 2.1 Điểm khống chế (sổ: `gcp-1782-drinkwater-batteries.json` — toạ độ ảnh ↔ UTM 30N + id OSM)
| # | Điểm | Ảnh (px) | OSM | Vùng | Sai khớp | LOO |
|---|---|---|---|---|---|---|
| 1 | King's Bastion — mũi | 895, 1165 | way/952588383 đỉnh tây | phố | 15,8 | 31,0 |
| 2 | Orange Bastion — mũi | 1333, 1268 | way/950399540 | phố | 35,0 | 51,2 |
| 3 | Montagu Bastion — tâm | 1540, 1395 | way/951936002 | phố | 35,0 | 63,2 |
| 4 | Spanish Church = St Mary the Crowned | 876, 1432 | way/167262263 | phố | 21,2 | 28,6 |
| 5 | Southport Gates | 315, 1432 | node/243847822 | phố | 3,5 | 6,4 |
| 6 | South Bastion — góc tây bắc | 365, 1281 | way/963314875 | phố | 17,3 | 23,8 |
| 7 | South Bastion — góc tây nam | 248, 1278 | way/963314875 | phố | 9,4 | 14,6 |
| 8 | Grand Parade (nay John Mackintosh Sq.) — đầu tây | 1025, 1287 | khoảng trống giữa City Hall–Line Wall Rd | phố | 20,3 | 24,1 |
| 9 | Grand Parade — đầu đông (Main St.) | 1025, 1425 | way/250867611 | phố | 9,9 | 13,3 |
| 10 | Fuerte de Santa Bárbara — mũi bastion nam | 3438, 2573 | way/462725331 (tàn tích) | Línea | 4,3 | 12,5 |
| 11 | Baluarte de San Benito | 3510, 2265 | node/12537395732 (di tích) | Línea | 5,8 | 9,4 |
| 12 | Baluarte de San Fernando | 3465, 1350 | way/1253399689 (di tích) | Línea | 1,5 | 36,2 |
| — | Tower of Homage (không dùng) | 1310, 1765 | way/950058970 | — | lệch 87–153 m | phần lâu đài trên bản khắc dịch xuống dốc; nhận dạng chưa chắc |
| — | Landport (không dùng) | 1693, 1652 | way/951660527 | — | lệch 99–150 m | nhãn đặt trên công sự ngoài, không chắc vị trí cổng |

Tổng 12 điểm dùng (lệnh: ≥ 9–11). Đơn vị m.

### 2.2 Chọn biến đổi (lý do)
- **Phố — affine:** 9 điểm bao quanh phố + 3 điểm trong phố. Poly2 khớp 12,7 m nhưng LOO 131 m (quá khớp); TPS LOO 36 m. Affine (LOO 33 m) bền nhất với nhiễu nhận dạng 10–20 m.
- **Línea — đồng dạng:** 3 di tích gần thẳng hàng → affine không xác định. Đồng dạng 4 bậc tự do: tỷ lệ 0,923 m/px, khớp tỷ lệ phần phố (0,917) → nhận dạng 3 bastion đúng (khoảng cách Santa Bárbara–San Benito–San Fernando 272/788 px ≈ 295/845 m thật).
- **Dải giữa — TPS 12 điểm:** bản khắc ghép phần phố và phần Línea lệch quay ~4° (đồng dạng phố 94,3° so với Línea 90,1°); dải eo đất ở giữa không còn vật cố định nào (Devil's Tower bị phá 1940, Inundation, Bayside/Forbes's Barrier đã mất) → TPS nội suy trơn giữa hai phần.
- **Bản xuất kích (sortie, 11/1781):** thử 5 điểm (`gcp-1782-drinkwater-sortie.json`): affine RMS 70 m / LOO 269 m — cùng kiểu ghép lệch, phần phố quay ~12° so với eo đất → **không dùng để dựng**, chỉ để nhận dạng công trình.
- **Faden 1783 (đối chiếu độc lập):** đồng dạng 3 điểm (King's Bastion, Santa Bárbara, San Benito) RMS 12,5 m. Vị trí công sự tiền phương theo Faden so với ghost: Mill/Round Tower Battery 130 m · St Carlos Battery hai đầu 99 m / 157 m · Mahon Redoubt 280 m (nhận dạng "đồn số 12 = Mahon Redoubt" chưa chắc). → dải giữa **không đạt** 50 m.

### 2.3 Raster nắn (ngoài git) — SHA-256 + cách tái tạo
| Tệp (`/var/tmp/cine-out/sh/warp/`) | Lưới | SHA-256 |
|---|---|---|
| `1782-batteries-pho-1m.jpg` (+ `.jgw`, UTM 30N) | E 287950–288750, N 4001250–4002800, 1 m/px, affine phố | `17d9581d647203f3cc259e62b2486fc67f5b8cb8954a739957f2c79148e989e9` |
| `1782-batteries-tps-2m.jpg` (+ `.jgw`) | E 287800–290200, N 4001200–4004600, 2 m/px, TPS | `32c28de8f0d814a1b561b07a06b743acd76259c68123086dd3772faf0426a1b9` |

Tái tạo: `python -I tools/ghost.py warp gcp-1782-drinkwater-batteries.json <ảnh gốc> pho 287950,4001250,288750,4002800 1.0 <out.jpg>` (đổi `pho`→`giua` và lưới cho bản TPS). JPEG mã hoá lại có thể khác byte giữa bản OpenCV; hình học tất định.

## 3. Vẽ khối 1782 (`so-hoa-1782-px.json` → `ghost-1782.geojson`)
- Dò tay trên ảnh phóng 3,8× có lưới toạ độ ảnh (tách tự động thử và loại: chấm nền khối liền với nét viền chấm). Chỉ vẽ vùng có **đường viền khối** trên bản đồ; vườn (gạch ngang) không vẽ; sườn đồi chấm không viền không vẽ.
- Thuộc tính mỗi feature: `moc`, `nguon_id`, `do_tin`, `so_tang_uoc` + `cach_uoc_tang`, `loai`, `vung_nan`, `bien_doi`, `sai_so_vi_tri_uoc_m`, `dien_tich_m2`/`dai_m`; toà nằm trong khối có `trong_khoi`. Meta lớp (`ghost`): RMS từng vùng, nguồn, giấy phép, ghi công.
- **Tầng:** bản đồ không ghi tầng → khối 2 tầng (khoảng 2–3, tầng chuẩn theo mốc của lớp tái dựng `city.js`); bản đồ ghi "RUINS OF GIBRALTAR" (phố đổ nát sau 4/1781) nên lấy cận dưới. Công sự/chiến tuyến `so_tang_uoc=0` (không áp dụng).
- **`do_tin`:** cao = viền khối liền, không bị chữ đè; vừa = viền rõ nhưng chữ đè/không thấy ngõ cắt; thấp = phố cong sườn đồi, viền đứt.

| Loại | Số | Ghi chú |
|---|---|---|
| khoi_pho | 22 | 84 663 m² (8 cao · 9 vừa · 5 thấp) |
| nha | 13 | toà tô đậm: dinh Thống đốc Eliott, nhà Phó Thống đốc Boyd, Spanish Church, dãy kho Victualling Office, dãy nhà dài sườn đồi |
| cong_su | 9 + 4 tiền phương | bastion, Old Mole, Line Wall, tường nam; đồn khẩu đội 5, cụm Old Windmill, đồn 12, Centre Guard House |
| phao_dai | 2 | San Felipe 12 002 m², Santa Bárbara 11 251 m² |
| chien_tuyen | 11 | Línea (cao) + 10 nét tiền phương (thấp); tổng 4,9 km |

## 4. Kiểm chồng 1782
- `kiem/1782-pho-tren-ban-do.jpg`: ghost 50 % trên raster nắn — khối khớp viền khối bản đồ (cùng nguồn, kiểm nội bộ).
- `kiem/1782-pho-tren-osm.jpg`: ghost trên OSM hôm nay. Line Wall ghost bám Line Wall OSM ≤ ~20 m dọc bờ; King's Bastion, South Bastion, tường nam/Southport khớp; **phía bắc phố (Irish Town → Orange's) ghost lệch tây ~20–35 m** (sai khớp Orange/Montagu 35 m): K1782-14/16/17/18 rơi một phần lên Line Wall Road.
- Khối thừa/thiếu: phố 1782 chỉ phủ nửa tây phố cổ hôm nay (Line Wall → dãy đông Main St.); nửa đông (phố dốc trên Main St.) bản đồ vẽ là sườn đồi chấm không viền → **không vẽ** (đúng luật "không bịa"); khoảng Orange's–Montague bản đồ để trống (nay là Casemates) → không vẽ.
- Thống kê so OSM (khung phố 0,8 × 1,55 km): 823 toà OSM; **83 toà có tâm trong khối ghost**; 4 khối không chứa tâm toà OSM nào (K1782-08/14/17/18 — vì lệch tây phía bắc, nằm trên đường). Phố cổ trong tường hôm nay: 706 toà / 1,07 km² (osm-do.json) ↔ ghost 1782: 22 khối 0,085 km².
- `kiem/1782-eo-dat-*.jpg`: Línea + 2 pháo đài khớp 3 di tích (≤ 6 m); Fort San Felipe rơi vào bờ biển La Línea hôm nay (đúng: pháo đài ở mép vịnh 1782); tuyến tiền phương nằm ngay bắc đường băng hiện nay — sai số ±160 m.

## 5. Ghi công + quyền
- Bản đồ: Drinkwater 1786 — phạm vi công cộng (`licenses/ia-drinkwater1786-plan-batteries.txt`); Faden 1783 (Yale, "any purpose", `licenses/yale-2046612-faden-1783.txt`) chỉ dùng đối chiếu; sortie plan (`licenses/ia-drinkwater1786-plan-sortie.txt`) chỉ nhận dạng.
- OSM (ODbL 1.0): chỉ dùng **toạ độ điểm khống chế** và nền ảnh kiểm; ghi công theo `licenses/osm-odbl-attribution.txt` — trên hình: "Map data from OpenStreetMap (ODbL)" + `https://www.openstreetmap.org/copyright`. GeoJSON là dữ liệu dẫn xuất, **không phát hành** (phim = Produced Work). Mỗi GeoJSON ghi `ghost.giay_phep`, `ghost.ghi_cong`.
- Nhãn phương pháp trên hình (đề xuất): "Reconstructed from J. Drinkwater, Plan of the Batteries, 1782 (pub. 1786)".

## 6. Shot T3 dùng được ghost 1782
| Shot | Cần | Dùng được | Ghi chú |
|---|---|---|---|
| 0e (pha 1782) | phố 1782 | **CÓ** | khối phố ±21–35 m; nhãn nguồn |
| 2a | chiến tuyến 6/1779 | **CÓ (Línea + 2 pháo đài)** | công sự tiền phương xây 1781–82 → tắt trong 2a |
| 2g | phố cháy 4/1781 | **CÓ** | khối là phố sau bắn phá (bản đồ 9/1782) — đúng tinh thần "ghost tro" |
| 2j | King's Bastion + phố | **CÓ** | bastion ghost ±16 m; dùng OSM footprint bastion làm hình chính |
| 2m | vịnh 13/9/1782, reveal | **CÓ** | phố + Línea đạt; tuyến tiền phương ±160 m chỉ ở hậu cảnh xa (≥ 1 km) |
| 2q | kết vây 2/1783 | **CÓ (Línea)**; tuyến tiền phương do_tin thấp | góc rộng cao 2,5 km chấp nhận được |

## 7. Chỉ số trong ±5 % quanh ngưỡng
- Không có. (Phố 21,2 m và Línea 4,2 m xa ngưỡng 50 m; dải giữa 99–157 m vượt rõ.)

## 8. Chi phí, tệp, preflight
- Claude API $0 (không gọi) · ElevenLabs 0 · YouTube 0 · mạng ≈ 63 MB (3 bản đồ 14 MB + OSM 48 MB), ngoài git.
- Tệp thêm: `ghost/` — `ghost-1782.geojson`, `so-hoa-1782-px.json`, `gcp-1782-*.json` (3), `tools/ghost.py`, `kiem/1782-*.jpg` (4, mỗi ảnh ≤ 0,41 MB), báo cáo này.
- `channel-k2/.gitignore` chặn `*.json` → các tệp JSON/GeoJSON trong `ghost/` thêm bằng `git add -f` (như v5b1-thu). Đề xuất ngoài vùng: thêm `!k2c-t3-01/ghost/**/*.json`.
- Preflight: ghi ở bản cuối.

## 9. Việc chờ chủ dự án (bản sớm)
1. Nhánh: lệnh ghi `sh-ghost`; harness của phiên chỉ cho đẩy `claude/sh-ghost-gibraltar-t3-1gkftx` → đã đẩy nhánh này. Nếu cần tên `sh-ghost`, P đổi tên/tạo nhánh từ commit này.
2. Dải giữa 1782 (công sự tiền phương TBN) chỉ đạt ±160 m → duyệt dùng ở hậu cảnh xa (2m, 2q) hoặc tắt.
