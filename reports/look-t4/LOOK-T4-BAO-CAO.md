Nhánh thật: `k2c-t4-02-look` (gốc `origin/k2c-t4-02-tienky` @888de179). Nhánh mặc định của bộ khung `ccr-32b90b5c-vzo2m7` KHÔNG dùng (lệnh gọi tên nhánh). SHA cuối = đỉnh nhánh (commit "… — DỪNG chờ chủ dự án").

# BÁO CÁO LOOK-T4 — khoá look tập K2C-T4-02 London (mốc M1b) · 23/10/2026

## §0. Nhánh, SHA, phạm vi
- Nhánh `k2c-t4-02-look`, gốc `origin/k2c-t4-02-tienky` @888de179. Commit của phiên: 0e07c0d4, 56984287, 8de0b942, 6ad9918a, e05f5dbe, ac1821cf, 10b25a26, b6f2674a, 67bf3add + commit cuối "LOOK-T4: … — DỪNG chờ chủ dự án" (đỉnh nhánh). Đã đẩy, **không merge**.
- Chỉ sửa trong vùng giao: `design/k2v/ldn/**` (mới: `look.js`), `scripts/k2ldn/**` (mới + sửa đường dẫn `du-lieu/` → `mo-hinh/` trong 4 tệp tiền kỳ), `channel-k2/k2c-t4-02/` (chỉ THÊM `look/`, `mo-hinh/`, `licenses/met-336038|336039|757299.json`, `licenses/SHA256-TU-LIEU-LOOK.txt`, `.gitignore` của thư mục tập; THÊM mục F vào cuối `RIGHTS-NHAP.md` theo lệnh "ghi RIGHTS-NHAP"), `reports/look-t4/**`. Không chạm `checks/`, `docs/`, sổ cái, `tools/`, `design/k2v/tl/**`, `design/cong3/shared/**`, `channel-k2/k2c-t3-01/**` (chỉ đọc LUT), `LOI-NHAP-v1.md`, `BANG-SHOT-v1.*`, `TREATMENT.md`, `main`.
- Mọi commit qua preflight (`set -o pipefail`) "— ĐẠT" + `lock.py --verify` KHỚP; hook pre-commit + pre-push cài trước lần đẩy đầu. Không force-push, không amend.
- Tệp lớn ngoài git ở `/var/tmp/ldn/` (OSM, LiDAR, tư liệu gốc, vân, hình học `ldn2.bin`, lightmap, khung thô, khung theo biến thể) — tái tạo bằng lệnh trong `scripts/k2ldn/`; mọi ĐẦU VÀO đọc tay (điểm khống chế, ranh cháy, toạ độ nhà thờ, máy, tham số look, LUT) nằm trong git.

## §1. Việc 1 — NÂNG HÌNH HỌC + VẬT LIỆU (dùng chung mọi mốc)
Mã: `scripts/k2ldn/hinh_hoc_look.py` (hình học v2 → `ldn2.bin`, SHA trong `ldn2.json`) + `design/k2v/ldn/look.js` (trang dựng look) + `scripts/k2ldn/nuong_look.py` (lightmap Cycles). Tiền kỳ (`hinh_hoc.py`, `page.js`) giữ nguyên để tái lập bản thử.

**Trước / sau (cùng điểm máy xương sống P1, 1666 ngày):** `reports/look-t4/so/truoc-sau-P1-1666.jpg` (trái: tiền kỳ T4, phải: look v2 — **mở SAU khi chọn mù**, vì ảnh phải trùng một ô của tờ mù). Tiền kỳ: nhà đồng dạng màu cam, nền bến bãi màu cát, bờ sông bậc thang, Old St Paul's khối hộp. Look: lô đa dạng + vân + khung gỗ/cửa sổ thủ tục, bờ mịn có kè/cầu thang nước, nước phản chiếu, đồi xa, Old St Paul's theo Hollar.

| Hạng mục | Làm gì (look v2) | Số đo / nguồn | Bậc (§12.2) |
|---|---|---|---|
| Nhà 1666 theo lô | Lô dọc 7 247 phố OSM còn giữ (bỏ phố sau 1666) trong mặt nạ Doornick; mặt tiền 3,4–11 m (45 % 1 khoang, 43 % 1,5 khoang, 12 % nhà giàu/quán trọ 7–11 m); sâu 7–14 m; 2–5 tầng theo hạng phố; **72 % đầu hồi ra phố** (mái 46–56°), còn lại nóc song song phố; **tầng nhô (jetty)** 0,35–0,6 m ở nhà ≥ 3 tầng mặt phố; ống khói gạch 85 %; vật liệu 78 % trát + khung gỗ, 10 % ván gỗ, 12 % gạch; tầng trệt cửa hàng ở mặt phố; lòng phố không bị lô lấn | **42 898 lô** + 109 kho/bến ven sông; **sân nhà thờ St Paul's để trống** (hộp theo trục nhà thờ u −122…+128 m, v ±62 m — Doornick vẽ khoảng trống quanh "S. Paul Kerck", Hollar sân trống trước mặt đông; bậc 4); lõi khối lấp (≤ 45 m từ phố, ven sông ≤ 110 m) — "estimated infill" | 5 lô · 4 kiểu nhà (Hollar Long View, Prospects) |
| Nhà sau 1667 (Rebuilding Act) | Trên đúng lô cháy, tường gạch, mặt tiền phẳng, nóc song song phố, gác mái; **4 hạng**: by-lane 2 tầng · phố/ngõ đáng kể 3 · phố lớn 4 · dinh thự không ra phố 4 | 12 262 nhà: hạng 1 = 6 408 · 2 = 4 885 · 3 = 756 · 4 = 213 (dữ kiện ≈ 13 200 nhà cháy → −7,1 %) | 4–5 |
| Thành phố 1840–1940 | Khối Victoria–Edward (4–6 tầng, gạch 72 % / Portland 28 %, cửa hàng tầng trệt) thay nhà cũ trên **cùng lô**, sống tới bom 29/12/1940 (vùng ước lượng) hoặc tới năm dựng toà OSM phủ lô | 27 017 khối | 5 |
| Nhà thờ giáo xứ | Doornick **không** đánh dấu nhà thờ trong vùng cháy (số 1–93 là tên PHỐ theo bảng chú giải) → toạ độ 78 nhà thờ từ bài Wikipedia + 30 nhà thờ OSM ngoài vùng; 1666: thân đá + tháp vuông (răng cưa/chóp chì); cháy → phế tích → **49 nhà thờ Wren** (theo danh sách 34 nhà thờ không dựng lại, Reynolds 1922) với tháp/chóp Portland | `mo-hinh/nha-tho-1666.json`; 67 nhà thờ OSM dựng bằng đá (không thành khối văn phòng) | 3 vị trí · 5 hình tháp 1666 |
| Old St Paul's (D6) | Dựng lại theo Hollar/Dugdale 1658 (Met 336039 mặt nam, 395057 mặt đông): dài 179 m, thân 30 m, cánh ngang 88 m; thân tây Romanesque bọc lại (cửa sổ tròn, 12 khoang), hợp xướng Gothic 12 khoang có trụ bay + chóp, mặt đông cửa sổ hoa hồng (đĩa đứng r 4,6 m, tâm 20,2 m) + 7 cửa sổ nhọn, tháp giao điểm 20 m vuông tới ≈ 62 m (Hooke 1664: 204 ft) + 4 chóp góc, portico Inigo Jones 10 cột, nhà thờ St Gregory áp góc tây nam; phế tích sau cháy | kích thước Clifton-Taylor tr. 275 (qua Wikipedia); tháp: Hooke 1664 (Jardine 2001) | 3 kích thước · 4 tỉ lệ |
| St Paul's (Wren) | Thân 2 tầng tường màn 33,5 m, cánh ngang 75 m có portico bán nguyệt, apse; tháp tây 65 m có vòm + chóp mạ vàng; **trống 32 cột**, gác, vòm chì ngoài, đèn lồng, quả cầu + thập giá tới **111 m** | 158 m / 75 m / 37 m / 111 m (Fletcher 1962 qua Wikipedia); bỏ 147 phần OSM chồng lên St Paul's/Tower (trước đó tạo "trụ kính" quanh mái vòm) | 3 + 4 |
| Cầu London 1666 | 19 vòm trên trụ có starling, dãy nhà 4–6 tầng hai bên lòng cầu, phần nhô ra sông trên chân gỗ, **khoảng trống cháy 1633** ở đoạn bắc, Nonsuch House 4 tháp củ hành | Hollar (Met 17.50.100, CC0) | 4 · khoảng trống bậc 5 vị trí |
| Bờ sông | **1666**: mép nước = đường đồng mức của mặt nạ nước làm trơn Gauss σ 6 m + hoà cao độ smoothstep (không răng cưa ô); kè gỗ theo mép + cầu thang nước/cầu tàu ngẫu nhiên; dải kho/bến/nhà dày ≤ 150 m từ bờ bắc (Fleet → Tower) — mặt nạ cháy Doornick bỏ mép sông nên dải này nay **có nhà và cháy** theo trường giờ (Thames Street); **2026**: tường Embankment granite | 1 987 đoạn kè gỗ · 1 793 đoạn Embankment | 4–5 |
| Mặt nước Thames | Sóng gradient fbm dị hướng 2 tầng (không ô vuông lặp), Fresnel, **phản chiếu phẳng** (máy đối xứng + mặt phẳng cắt, nửa độ phân giải), màu nước sông theo biến thể, ánh lửa phản chiếu; không viền xanh nhạt / mảng bọt (LOOK-4 T3) | — | — |
| Toà 2026 | OSM + LiDAR (7 424 toà lấy cao độ từ DSM − DTM); dùng **building:part** (bỏ đường bao khi có phần); Leadenhall **vát** (mái nghiêng theo bắc → nam); 30 St Mary Axe tròn xoay theo hồ sơ; vật liệu theo độ cao/năm: > 60 m kính rèm (80 %) / đá; trước 1914 Portland/gạch; còn lại bê tông-đá / kính / gạch / Portland; cửa sổ thủ tục theo tầng 3,8–3,9 m | 16 786 toà · 6 cầu (một mặt cầu/cầu + trụ) | 1 hình khối · 5 vật liệu |
| Mặt đất | Lớp phủ 2 m theo năm: 1666 phố sỏi, sân đất, vườn trong khối (Doornick vẽ vườn), bến (sỏi + ván), bãi bùn; 2026 nhựa, vỉa hè, cỏ (OSM); tro tối trên vùng đã cháy > 4 h | `cls66.png`, `cls26.png` | 4–5 |
| Cây, thuyền, khói bếp | Cây tán (vườn 1666 trong khối, công viên 2026; mùa đông 1940 trụi lá) 2 193 cây; thuyền theo mốc 153 (1666: đò wherry 70, sà lan 22, tàu buồm neo dưới cầu 14 — buồm cuộn; 1940: sà lan + tàu kéo; 2026: tàu khách + sà lan), không đặt sát điểm máy; khói bếp 2 360 ống khói (mật độ theo biến thể; 2026 không) | — | 4–5 |
| Người / xe | **Chưa dựng** (khung look ở ≥ 19 m, người < 2 px ở khung rộng) → đề xuất L3 | — | — |
| Ánh sáng nướng | Cycles **CPU** 1 m/texel, 32 spp, hộp 3,2 × 2,3 km, 3 mốc (1666 / 1940 / 2026): **86,4 · 87,6 · 107,5 s** (lượt cuối, hình học bản cuối); R = bức xạ trời có che khuất + nảy → AO phố + chân tường (tắt dần theo cao). GPU **không thuê**: CPU đã < 2 phút/mốc (đo), thuê pod chỉ để nướng tốn thời gian khởi động hơn | `bake_*.png.json` | — |
| Khí quyển | Sương có độ cao (tích phân mật độ e^(−y/H) dọc tia máy) + lớp khói than thấp riêng (biến thể B) + đồi xa ngoài hộp (Hampstead/Highgate bắc, Sydenham/Norwood nam — bậc 5) + dãy nhà xa theo năm | — | 5 (đồi xa) |

Hình học cuối: **2 270 425 tam giác** (`ldn2.bin` SHA-256 `fef452941430a9163e1a4abe7d94c3cf3d8cee42c53bbb43aa8caff1ee80f518`; mọi khung, clip, tranh khắc dựng trên đúng bản này; siêu dữ liệu: `channel-k2/k2c-t4-02/look/ldn2-meta.json`).

## §2. Việc 2 — BỐN MỐC LOOK × 2 KHUNG
Nguồn thật của máy/giờ/tham số: `channel-k2/k2c-t4-02/look/may/<hàng>-<A|B|C>.json` (sinh bằng `scripts/k2ldn/look_khung.py`). Cao độ máy là cao độ TUYỆT ĐỐI (ODN). Dựng 1920×1080, 16 spp, P = 2 (`scripts/k2ldn/look_chay.sh`).

| Hàng | Điểm máy | Thời điểm | Vai (BANG-SHOT-v1) | Tiêu điểm |
|---|---|---|---|---|
| M1-rong | P1 Bankside cao [532330, 180250, 230], fov 50 | 1/9/1666 (J.) 15:30 LMT | xương sống — chỗ Pepys | Old St Paul's |
| M1-trung | P2 tháp St Saviour [532690, 180290, 70] cúi 14°, fov 50 | 1/9/1666 16:00 | H1-03 góc Hollar Long View | cầu London có nhà (đoạn bắc) |
| M2-ngay | P1 | 3/9/1666 15:00 (giờ cháy 39) | ngày khói: cột khói theo gió đông, phế tích phía đông | Old St Paul's dưới khói |
| M2-dem | P6 giữa sông [533250, 180480, 35], fov 45 | 2/9/1666 23:00 (giờ 23) | H1-02/H1-08: bờ bắc cháy quanh cầu, phản chiếu | cầu + bờ cháy |
| M3-rong | P1 | 29/12/1940 21:30 | H4-02: nhiều đám cháy rời quanh St Paul's (vùng **ước lượng**, D15) | mái vòm |
| M3-trung | P4 Fleet Street [531260, 181158, 52], fov 30 | 29/12/1940 22:30 | H4-04: mái vòm giữa khói lửa — dựng 3D, KHÔNG ảnh Mason | mái vòm |
| M4-rong | P1 | 2/9/2026 15:00 BST | chân trời City: St Paul's + cụm tháp | mái vòm / cụm tháp |
| M4-trung | Fleet Street gần Ludgate Circus [531560, 181176, 19,1] (mặt phố 9,1 m + 10 m), fov 22 | 2/9/2026 16:30 BST | H5-05: tầm nhìn bảo vệ — mái vòm còn nền trời, Leadenhall vát | mái vòm |

Lửa/khói: cách A (atlas thể tích nướng sẵn — tiền kỳ T1, tái tạo bằng `nuong_flipbook.py`) theo trường giờ bén lửa tiền kỳ (RBF 31 tên nơi, bậc 5 nội suy); mặt tiền đang cháy là mảng lửa theo ô cửa/khe mái (không phủ đều), tro tối sau 4 h, phế tích ám khói; 1940: lưới cháy 20 m dạng cụm (≈ 20 % ô trong vùng ước lượng, bén 18:15–21:30). Không Cycles GPU trong khung look (D5: Cycles chỉ cho 3–4 cận đêm ở sản xuất).
Bỏ trong M4-trung bản đầu: máy 52 m nhìn thấy cụm tháp CAO HƠN mái vòm (đúng hình học), nên hạ về gần mặt phố như tầm nhìn bảo vệ được đo (LVMF) — lần đặt 9 m đầu tiên nằm DƯỚI mặt đất (nhầm cao độ tương đối/tuyệt đối), đã sửa (§9).

## §3. Việc 3 — BA BIẾN THỂ + SỐ ĐO
Ba biến thể, **cùng hình học / máy / giờ** trong mỗi hàng, chỉ khác ánh sáng – màu – khí quyển – mật độ chi tiết (tham số `look` trong `look/may/*.json`) + LUT xuất. Không lọc "giả tranh", không AI.

| Biến thể | Khí quyển | Ánh sáng / trời | Nước | Mật độ chi tiết | LUT xuất |
|---|---|---|---|---|---|
| A "T3 kênh" | sương e^(−σd), σ = 1/16 km, màu chân trời [0,60 0,74 0,90]-họ T3 (LOOK-1) | nắng 3,2 · bán cầu 0,62 · trời thiên đỉnh [0,13 0,33 0,70] như `water.js` T3, mây 0,32 | xanh–lục sẫm | vân 100 %, khói bếp 0,30 | `k2c-t3-kenh-v030.cube` (kênh T3, không chép) |
| B "London sương" | sương dày σ = 1/6 km, xám lạnh, H 420 m + **lớp khói than thấp** σ = 1/4,2 km, H 90 m (1666: Evelyn *Fumifugium* 1661 tả khói than London — mức dày bậc 5; 1940: khói than + khói cháy ước lượng; **2026: không khói than** — Clean Air Act 1956) | nắng 2,1 · bán cầu 0,78 · trời phủ mây 0,78 xám | xám lục | vân 90 %, khói bếp 0,85, khói cháy ×1,25 | `look-B-lanh.cube`: bão hoà −18 %, bóng ngả lạnh |
| C "tranh khắc ấm" | sương ấm σ = 1/10,5 km, vàng đất | nắng ấm [1,06 0,97 0,84] · trời [0,40 0,50 0,64]→chân trời [0,88 0,80 0,66], mây 0,5 | nâu lục | vân 85 %, khói bếp 0,45 | `look-C-am.cube`: tương phản mềm (đen nâng 0,035, sáng cuộn), bảng màu ochre/umber — chỉ đường cong màu |

**Số đo mọi khung** (`scripts/k2ldn/look_do.py`, ảnh thu 640×360 như thước V6/NC-CPU; mặt nạ ID dựng riêng mỗi hàng). Bảng theo **nhãn mù** để không lộ khoá; tổng hợp theo biến thể: `reports/look-t4/khoa-do.json` (**mở sau khi chọn**). Định nghĩa: bão hoà = HSV trung vị (cả khung / dải giữa y 60–300); colorfulness Hasler–Süsstrunk; chi tiết = trung vị |Laplace| (NC-CPU: không đo được "độ thật", chỉ theo dõi); nước/trời theo mặt nạ ID; sương = điểm không phải trời có độ lệch chuẩn cục bộ < 2,5/255 và gần màu chân trời (ΔE < 12); tiêu điểm = điểm chiếu vật tiêu điểm (toạ độ trong `look/may/*.json` → `hero_EN`) qua ma trận máy thật của lượt dựng.

| Khung | Cột (mù) | Bão hoà TV (cả khung / giữa) | Colorfulness | Chi tiết | Nước % | Trời % | Sương % | Trời+sương % | Tiêu điểm (x %, y %) · cách giao 1/3 · tương phản | ±5 % ngưỡng |
|---|---|---|---|---|---|---|---|---|---|---|
| M1-rong | X | 0.345 / 0.369 | 27.1 | 7.0 | 28.9 | 20.0 | 0.0 | 20.0 | 28.2, 42.6 · 7.5 · 0.34 | trời+sương |
| M1-rong | Y | 0.051 / 0.047 | 8.6 | 6.0 | 28.9 | 20.0 | 0.8 | 20.8 | 28.2, 42.6 · 7.5 · 0.27 | trời+sương |
| M1-rong | Z | 0.180 / 0.173 | 33.1 | 7.0 | 28.9 | 20.0 | 0.0 | 20.0 | 28.2, 42.6 · 7.5 · 0.41 | trời+sương |
| M1-trung | X | 0.059 / 0.063 | 12.6 | 6.0 | 28.1 | 23.2 | 0.0 | 23.2 | 64.8, 41.0 · 5.6 · 0.35 | — |
| M1-trung | Y | 0.329 / 0.341 | 28.8 | 7.0 | 28.1 | 23.2 | 0.0 | 23.2 | 64.8, 41.0 · 5.6 · 0.45 | — |
| M1-trung | Z | 0.298 / 0.388 | 37.7 | 7.0 | 28.1 | 23.2 | 0.0 | 23.2 | 64.8, 41.0 · 5.6 · 0.53 | — |
| M2-ngay | X | 0.165 / 0.169 | 24.2 | 5.0 | 28.9 | 20.0 | 4.8 | 24.7 | 28.2, 42.6 · 7.5 · 0.27 | — |
| M2-ngay | Y | 0.024 / 0.027 | 10.2 | 5.0 | 28.9 | 20.0 | 5.8 | 25.8 | 28.2, 42.6 · 7.5 · 0.36 | — |
| M2-ngay | Z | 0.369 / 0.376 | 28.0 | 5.0 | 28.9 | 20.0 | 3.0 | 23.0 | 28.2, 42.6 · 7.5 · 0.29 | — |
| M2-dem | X | 0.584 / 0.624 | 31.2 | 4.0 | 30.2 | 49.0 | 0.1 | 49.1 | 28.6, 56.1 · 8.2 · 0.36 | — |
| M2-dem | Y | 0.502 / 0.573 | 31.3 | 2.0 | 30.2 | 49.0 | 0.1 | 49.1 | 28.6, 56.1 · 8.2 · 0.2 | — |
| M2-dem | Z | 0.416 / 0.447 | 23.8 | 4.0 | 30.2 | 49.0 | 1.2 | 50.3 | 28.6, 56.1 · 8.2 · 0.32 | bão hoà |
| M3-rong | X | 0.537 / 0.545 | 18.6 | 5.0 | 27.5 | 20.0 | 0.0 | 20.0 | 26.3, 39.7 · 6.7 · 2.11 | trời+sương |
| M3-rong | Y | 0.584 / 0.502 | 26.4 | 4.0 | 27.5 | 20.0 | 0.0 | 20.0 | 26.3, 39.7 · 6.7 · 2.12 | trời+sương |
| M3-rong | Z | 0.275 / 0.275 | 25.5 | 2.0 | 27.5 | 20.0 | 0.0 | 20.0 | 26.3, 39.7 · 6.7 · 2.61 | trời+sương |
| M3-trung | X | 0.412 / 0.427 | 20.5 | 4.0 | 0.2 | 54.0 | 0.0 | 54.0 | 50.7, 50.5 · 16.1 · 2.74 | bão hoà |
| M3-trung | Y | 0.302 / 0.416 | 27.1 | 2.0 | 0.2 | 54.0 | 0.0 | 54.0 | 50.7, 50.5 · 16.1 · 3.43 | — |
| M3-trung | Z | 0.533 / 0.549 | 27.5 | 4.0 | 0.2 | 54.0 | 0.0 | 54.0 | 50.7, 50.5 · 16.1 · 2.76 | — |
| M4-rong | X | 0.278 / 0.286 | 19.6 | 7.0 | 25.6 | 19.7 | 0.0 | 19.7 | 26.3, 39.7 · 6.7 · 0.65 | trời+sương |
| M4-rong | Y | 0.067 / 0.071 | 6.9 | 6.0 | 25.6 | 19.7 | 0.0 | 19.7 | 26.3, 39.7 · 6.7 · 0.54 | trời+sương |
| M4-rong | Z | 0.141 / 0.110 | 25.6 | 7.0 | 25.6 | 19.7 | 0.0 | 19.7 | 26.3, 39.7 · 6.7 · 0.73 | trời+sương |
| M4-trung | X | 0.047 / 0.047 | 9.6 | 5.0 | 0.0 | 49.7 | 0.4 | 50.1 | 50.0, 57.9 · 13.3 · 0.5 | — |
| M4-trung | Y | 0.196 / 0.184 | 30.8 | 5.0 | 0.0 | 49.7 | 0.0 | 49.7 | 50.0, 57.9 · 13.3 · 0.7 | — |
| M4-trung | Z | 0.161 / 0.161 | 21.0 | 5.0 | 0.0 | 49.7 | 0.7 | 50.4 | 50.0, 57.9 · 13.3 · 0.6 | — |

Phạm vi bão hoà TV trên 24 ô: 0.024 – 0.584 (ngưỡng §14.4: 0,40). Tổng hợp theo biến thể: `khoa-do.json` (mở sau khi chọn).


Đọc số (tự đo, không tự chấm đạt):
- **Bão hoà trung vị ≥ 0,40 (BIBLE §14.4) không đạt ở khung ngày** của cả 3 biến thể (phạm vi 0,024–0,37 ngày); khung đêm lửa 0,40–0,58 (nền tối + cam). Ô ngày cao nhất 0,37 (biến thể nào: xem `khoa-do.json` sau khi chọn — nêu ở đây sẽ lộ khoá). Nguyên nhân đo được: trời London nhạt + đồng xa xám lục + tường trát/đá bão hoà thấp; mặt nước xanh của một biến thể đạt 0,56 nhưng chỉ chiếm 26–30 % khung. Không đẩy màu chỉ để vượt ngưỡng (luật cứng) → đề xuất **L2** ở phiếu.
- **Trời + sương** ở P1 (toàn cảnh): 20,0 % (M1, M3) và 19,7 % (M4) — đúng mép trên dải 8–20 % của LOOK-2 T3 (nêu tên ở §11); M2-ngay 23–26 % do khói che chân trời. Khung trung mặt phố (M3-trung, M4-trung) trời 50–54 %: là khung tầm nhìn mái vòm (vai truyện "mái vòm còn nền trời"), không thuộc khung lai LOOK-2.
- **Nước** ≤ 30,2 % mọi khung (≤ 1/3, §11.4).
- **Tiêu điểm**: P1 ở (28 %, 43 %) — cách giao điểm 1/3 trái-trên 7,5 % đường chéo; M1-trung cầu ở (65 %, 41 %); M2-dem ở (29 %, 56 %); M3-trung / M4-trung mái vòm giữa khung (51 %, 51 %) / (50 %, 58 %) — đặt giữa có chủ ý theo trục phố.


## §4. Việc 4 — TỜ CHỌN MÙ + CLIP
- **Tờ chọn mù:** `reports/look-t4/to-chon-mu.jpg` (2756 × 3836, 1,9 MB) — 8 hàng (4 mốc × 2 khung) × 3 cột; thứ tự cột **xáo theo hàng** (hạt giống 16660902, ghi trong khoá), nhãn trung tính **X / Y / Z**; nhãn hàng chỉ ghi mốc + vai khung. Bản 1080p từng ô: `reports/look-t4/khung/<hàng>-<X|Y|Z>.jpg` (JPG ≤ 2 MB, đã LUT). Bản theo tên biến thể (lộ khoá) để NGOÀI git (`/var/tmp/ldn/look/khung-abc/`), SHA-256 ghi trong khoá.
- **Khoá giải mã:** `reports/look-t4/khoa.json` (+ số đo tổng hợp theo biến thể `reports/look-t4/khoa-do.json`) — **chỉ mở sau khi chọn**. Số đo từng ô theo nhãn mù: `reports/look-t4/do/<hàng>-<X|Y|Z>.json`.
- **Clip 8 s, 640 × 360, biến thể A, ≤ 5 MB** (`scripts/k2ldn/look_clip.sh`; đo cú máy `reports/look-t4/do/clip-M*.json`):

| Clip | Cú máy (§19 đề xuất) | Quay hướng nhìn °/s (TB/max) | Vòng quanh tiêu điểm °/s (TB/max) | Tiêu điểm trôi % khung/s (TB/max) | s/khung dựng (640×360, spp 4, P = 2) | MB |
|---|---|---|---|---|---|---|
| `clip/clip-M1-A.mp4` | VÒNG CUNG 18° / 8 s = 2,25°/s quanh City; thời gian chạy 15:00 → 16:30 | 2.17 / 2.52 | 1.69 / 1.99 | 0.73 / 0.85 | 5.80 | 3.21 |
| `clip/clip-M2-A.mp4` | ĐẨY VÀO 16 % quãng tới tiêu điểm / 8 s; giờ cháy 3/9 12:00 → 18:00 (khói lớn dần) | 0.0 / 0.0 | 0.36 / 0.46 | 0.46 / 0.6 | 6.20 | 1.43 |
| `clip/clip-M3-A.mp4` | ĐẨY VÀO chậm; 29/12/1940 20:00 → 23:00 (đám cháy lan) | 0.0 / 0.0 | 0.34 / 0.43 | 0.47 / 0.6 | 5.88 | 1.03 |
| `clip/clip-M4-A.mp4` | VÒNG CUNG 16° / 8 s = 2°/s; 14:00 → 19:30 (chiều → hoàng hôn, cửa sổ sáng dần) | 1.92 / 2.24 | 1.52 / 1.8 | 0.63 / 0.74 | 6.21 | 2.75 |

Mọi clip trong giới hạn §19 đề xuất (quay ≤ 3°/s; tiêu điểm ≤ 1,5 %/s). Thời gian chạy trong khung ở cả 4 clip (giờ/giờ cháy nội suy theo khoá).

Ghi chú: clip đều là biến thể A theo lệnh, nên xem clip TRƯỚC khi chọn sẽ cho biết A trông thế nào — đề nghị chủ dự án chọn trên tờ mù trước, rồi mới xem clip.

## §5. Việc 5 — TRANH KHẮC (D7) với Old St Paul's mới
Làm lại bản thử T3 tiền kỳ với Old St Paul's mới: Hollar *Old St Paul's seen from the East* (Met 2010.529 = 395057, CC0) hoà vào 3D cùng góc; **đăng ký điểm** (9 điểm đọc tay giữ nguyên tiền kỳ, toạ độ mô hình theo hình học mới) + **thị sai 2,5D thủ công** (mặt nạ đa giác vẽ tay, lớp nhà 1,000 → 1,012) + uốn tỉ lệ/tịnh tiến về mặt đông + hoà mờ; **không AI**. Mã: `scripts/k2ldn/t3_look.py` (cùng thuật toán `t3_may.py`/`t3_khac.py`, không sửa hai tệp đó). Ngày 1/9/1666 (J.) 9:00 sáng, nắng phía đông như bản khắc.

| Đo | Tiền kỳ (mô hình cũ) | Look (mô hình Hollar/Dugdale) |
|---|---|---|
| Giải máy — RMS 9 điểm (px bản 2000) | 96,1 | **49,8** |
| — trung vị | 50,9 | **33,8** |
| — đỉnh tháp giao điểm | **232,5** | **23,7** |
| Máy giải được | cách mặt đông 72 m, fov dọc 56° | cách mặt đông 247 m, cao 38,7 m, fov dọc 18,9° (khung cao 1002 → cắt 720; tranh gần phối cảnh trực giao — máy xa, ống kính dài hợp hơn) |
| Khớp mặt đông, 7 điểm, trước uốn (px khung 720) — TB / max | — | 23,5 / 37,2 |
| — sau uốn tỉ lệ/tịnh tiến — TB / max | — | 23,7 / 34,2 |
| Điểm kiểm sau uốn: đỉnh tháp · chân cánh ngang nam · tâm cửa sổ hoa hồng | — | 9,9 · 14,0 · **39,9** px (cửa sổ hoa hồng của mô hình nay đứng đúng mặt đông, sân nhà thờ để trống; độ lệch còn lại chưa tách được nguyên nhân — giả thuyết chưa kiểm: tỉ lệ đầu hồi trong bản khắc khác kích thước Dugdale; không bóp hình học để khớp, mặt nạ 2,5D che ở bản hoà) |

Tệp: `reports/look-t4/t3/T3-khac-hoa-look.mp4` (8 s) · tờ so trước/sau cùng thời điểm hoà (4,0 s): `reports/look-t4/t3/T3-so-truoc-sau.jpg` (trái: tiền kỳ `reports/tien-ky-t4/xem/T3-khac-hoa-1080.jpg`, phải: look). Số đo: `reports/look-t4/do/t3-may.json`, `t3-khop.json`.

## §6. Việc 6 — ƯỚC LẠI GIỜ MÁY / CHI PHÍ
**Số đo trong phiên** (llvmpipe, 4 vCPU, P = 2 = hai tiến trình cùng lúc như sản xuất; `look/may/do1080-M*.json`, 24 khung mỗi tiến trình, khung 0 gồm biên dịch shader):

| Lớp / cấu hình | s/khung mỗi tiến trình (trung vị khung 1–23) | Ghi chú |
|---|---|---|
| Cách A look, 1080p, spp 4 — M1 ngày (vòng cung P1) | **7,30 / 7,28** | khung 0: 12,4–13,2 s; nạp cảnh 4,8–5,2 s |
| Cách A look, 1080p, spp 4 — M3 đêm lửa 1940 (đẩy vào P1) | **7,75 / 7,63** | khung 0: 13,7–14,0 s; lửa + khói atlas +5 % |
| Cách A look, 640×360, spp 4 (4 clip) | 5,8–6,2 | nghẽn ở số đỉnh (2,28 tr. tam giác × bóng + gương + 4 mẫu), không ở điểm ảnh |
| Khung look tĩnh 1080p, spp 16 | 37–46 (một khung, gồm nạp + biên dịch) | 24 khung ≈ 16 phút ở P = 2 |
| Nướng lightmap Cycles CPU 1 m, 32 spp, 3,2 × 2,3 km | 86–108 s / mốc | 3 mốc trong phiên |

Tối ưu đã làm (không đổi hình, lệch TB 0,005/255): bản đồ bóng 1 lần/khung (trước: mỗi mẫu); chia hình học thành ô 300 m để loại theo khung nhìn (8,3 → 6,0 s/khung ở 640×360).

**Ước cả tập** (bảng shot v1: lớp A 513 s = 12 312 khung; mặt nạ ID 190 s; 6–8 mốc lightmap):

| Khoản | UOC-VA-GHIM (tiền kỳ) | Ước mới (số đo look) | Lệch | Thay số? |
|---|---|---|---|---|
| Cách A 1080p (P = 2) | 8 s/khung/tiến trình → ≈ 14 h | 7,5 s → 12 312 × 7,5 / 2 ≈ **12,8 h** | −9 % | không (< 20 %) |
| Mặt nạ ID shot N2+ | ≈ 4 h ở P = 2 | ≈ 4 h (mặt nạ 1 lượt, không tích luỹ) | ≈ 0 | không |
| Nướng ánh sáng theo mốc | ≈ 5 h (6–8 mốc × 40 phút) | 6–8 mốc × ≈ 100 s ≈ **0,2 h** | −96 % | **có** — thay bằng ≈ 0,2 h (CPU, không cần GPU) |
| Tổng giờ máy container | ≈ 25–30 h | ≈ **20–25 h** (≈ 2 phiên ≤ 12 h) | −17…−20 % | ghi mới (biên dưới −20 %) |
| GPU Cycles (D5: 3–4 cận đêm 30–40 s) | ≈ $5–8 | không đổi (look không dùng Cycles) — **nướng lightmap: $0 GPU** | — | — |

Rủi ro tốc độ: số đỉnh là nút thắt — thêm người/xe (L3) hay chi tiết hình học mái/cửa sẽ tăng thời gian gần tuyến tính; đề xuất LOD (gộp nhà xa > 1,5 km thành khối mái) nếu cần thêm chi tiết gần.

## §7. Việc 7 — PHIẾU CHỌN
`reports/look-t4/PHIEU-LOOK.md`: cách chọn (mỗi hàng 1 cột hoặc "không cột nào đạt"), Q1–Q3 (đồ chơi / khói–lửa / nhận ra London), quyết định đề xuất L1–L6. Phiên này **không** chấm mù bằng AI, **không** dùng AI soi có phí (O2: không); tự soi lỗi bằng mắt từng khung (lỗi đã sửa ghi ở §9).

## §8. Nguồn mới + giấy phép
Chi tiết: `channel-k2/k2c-t4-02/RIGHTS-NHAP.md` mục F. Tóm tắt: Met 336039 / 336038 / 757299 (Hollar + Dugdale 1658, CC0, JSON nguyên văn trong `licenses/`); 16 vân Poly Haven CC0 (`look/van-cc0.json`, SHA từng tệp); toạ độ 78 nhà thờ (Wikipedia API, dữ kiện, bậc 3); kích thước Old St Paul's (Clifton-Taylor; Hooke 1664) và St Paul's (Fletcher 1962) qua Wikipedia (bậc 3). Dữ liệu cũ dùng lại: OSM (ODbL), EA LiDAR (OGL v3), Doornick (Rijks PDM). Không AI sinh hình trong khung look.

## §9. Sự cố
| # | Sự cố | Xử lý | Kết quả |
|---|---|---|---|
| 1 | Dữ liệu tiền kỳ ngoài git mất theo container (`/var/tmp/ldn`: OSM, LiDAR, tư liệu, atlas lửa) | tải lại bằng lệnh tiền kỳ (`tai_lidar.py`, `tai_tu_lieu.py`, OSM bằng `tai_osm.py` mới — UA đúng luật), nướng lại atlas (`nuong_flipbook.py` 96×192, 148 s) | đủ; SHA tư liệu khớp (bản thu trong git không đổi) |
| 2 | **`khop-doornick.json` + `ranh-chay-1666-cuoi.json` của tiền kỳ KHÔNG có trong git** — `channel-k2/.gitignore` chặn `*.json` (lặp kiểu BAI-HOC #117) | đọc lại 11 điểm khống chế + 3 điểm kiểm trên Doornick gốc 5324×4650; thêm `channel-k2/k2c-t4-02/.gitignore` mở `mo-hinh/*.json`, `look/**/*.json`; dữ liệu nay ở `mo-hinh/` (trong git) | affine RMS 49,9 m (tiền kỳ 44,2), LOO 70,3 m; nhãn St Paul's lệch 85,9 m (tiền kỳ ≈ 85 m); ranh cháy 148,3 ha = **366 acre** (tiền kỳ 399) — §11 |
| 3 | Thiếu `pyproj` + lưới OSTN15 | cài `pyproj==3.8.0` (ghim D17) + `uk_os_OSTN15_NTv2_OSGBtoETRS.tif` (SHA 5d6ed64d…) | — |
| 4 | `kill $(pgrep -f …)` giết chính shell (exit 144) — **lặp BAI-HOC #112** | từ đó chỉ dừng theo PID | không mất dữ liệu |
| 5 | Hai chuỗi nền (dựng hình học + nướng) chạy chồng 3 lần vì PID ghi nhầm (`setsid` tách tiến trình; `ps | head -1` lấy tiến trình cũ) → nướng trên hình học cũ | dừng theo PID thật, chạy lại | mất ≈ 15 phút máy |
| 6 | Nướng Cycles ra "không che khuất" (trung vị 1,0) | mặt đất tạo bằng `foreach_set` có pháp tuyến ÚP (trục Y Blender = −z đảo chiều vòng) → bake nhìn nửa cầu dưới; đảo thứ tự đỉnh | 0,59–0,65 trung bình, AO phố đúng |
| 7 | UV mặt đất tràn ngoài [0,1] (đệm 300 m) bị ghi chồng khi nướng | mặt đất đúng hộp, nhà giữ đệm để che | — |
| 8 | Hai lần sửa mã chèn chú thích `#`/`//` giữa dòng nuốt phần còn lại (Python: mất `VICT`; JS: trang lỗi cú pháp) — **lặp sự cố #16 tiền kỳ** | sửa; từ đó `node --check` sau mỗi lần sửa `look.js` | 2 lượt thử hỏng |
| 9 | Doornick: số 1–93 là **tên phố** (bảng chú giải "Direction to the names of the Streetes"), không phải nhà thờ → không lấy được vị trí nhà thờ trong vùng cháy từ Doornick như lệnh | vị trí từ toạ độ Wikipedia (78) + OSM (30); ghi bậc 3 | lệch lệnh có lý do (Doornick để trắng vùng cháy) |
| 10 | Wikipedia API trả 429 | lùi 15–30 s, gom 50 tiêu đề/lượt | đủ 85/100 toạ độ |
| 11 | Mặt nạ cháy Doornick bỏ mép sông → dải Thames Street không có nhà và không cháy; trước đó dải cỏ xanh ven sông | dải ≤ 150 m bờ bắc = có nhà (lõi khối ≤ 110 m), cháy theo trường giờ RBF | nhà trong vùng cháy 12 262 (dữ kiện 13 200 → −7,1 %) |
| 12 | Lô của phố này lấn lòng phố khác (khối nhà giữa Fleet Street che máy P4) | vẽ lòng phố vào lưới chiếm chỗ trước khi đặt lô | lô 60 569 → 43 057 (bỏ nhà nằm trên phố) |
| 12b | Soát tranh khắc T3 (14:33): sân nhà thờ St Paul's bị lô nhà lấp kín (trái Doornick/Hollar) và cửa sổ hoa hồng mặt đông là trụ dẹt NẰM NGANG (không thấy) | sân nhà thờ để trống (hộp theo trục nhà thờ), đĩa hoa hồng đứng; **dựng lại toàn bộ** 24 khung + 4 clip + T3 trên hình học mới | lô 43 057 → 42 898; ≈ 75 phút máy thêm |
| 13 | Phần OSM `building:part` của St Paul's dựng thành khối kính văn phòng quanh mái vòm ("trụ kính") | bỏ mọi toà/phần nằm trong đường bao St Paul's (−6 m) và quanh Tower; nhà thờ OSM dựng bằng đá | mái vòm đọc đúng (trống 32 cột, vòm chì, đèn lồng) |
| 14 | M4-trung đặt máy 9 m tưởng là trên mặt phố → nằm DƯỚI mặt đất (cao độ máy là tuyệt đối ODN, mặt phố 15,1 m) | ghi rõ "TUYỆT ĐỐI" trong `look_khung.py`; đặt 19,1 m (mặt phố 9,1 m + 10 m) gần Ludgate Circus | khung đúng tầm nhìn |
| 15 | Bản đồ bóng 6144² dựng lại ở MỖI mẫu tích luỹ | dựng một lần mỗi khung | tích luỹ 1080p 16 spp còn ≈ 5 s |
| 16 | Sửa `look_chay.sh` khi nó đang chạy → bash báo EOF cuối lượt | đủ 24/24 khung trước lỗi; từ đó không sửa tệp đang chạy | — |
| 17 | Một lượt nướng 2026 (205 s) chạy chồng lúc đã bắt đầu dựng 2 khung → **3 tiến trình nặng ≈ 3 phút** (luật P ≤ 2 khi nướng) | khung lượt đó bị dựng lại toàn bộ ở lượt cuối (nướng xong trước) | lượt cuối tuân P = 2 |
| 18 | Thử nghiệm bằng mắt phát hiện và sửa trước lượt cuối: thuyền neo che máy P6; nhà đang cháy "phát sáng trắng" (phát xạ bão hoà) → mảng lửa theo ô cửa; trời đêm ám cam toàn bầu; lớp khói than sáng ở đêm (B); kính cửa sổ văn phòng ánh lam như nhiễu; hộp nhà xa trôi nổi; trụ cầu/đường OSM vẽ chồng thành tấm cầu 40 m | sửa trong `look.js` / `hinh_hoc_look.py` | — |

Không force-push, không amend, không pod GPU nào được bật. Không lỗi nào lặp ≥ 3 lần trong cùng một cách làm.

## §10. Chi phí thật
| Khoản | Mốc theo dõi | Chặn | Thật | Nguồn số |
|---|---|---|---|---|
| Claude API | $5 | > $20 | **$0** (không gọi; không chấm/soi AI) | — |
| OpenAI (chỉ soi/chấm) | $3 | > $10 | **$0** | — |
| RunPod | $10 (số dư ≈ $21) | > $20 | **$0** — không bật pod: nướng Cycles CPU đo 86–108 s/mốc (1 m, 32 spp) nên GPU không "nhanh hơn rõ" khi tính cả khởi động pod | `bake_*.png.json` |
| Gemini / ElevenLabs / YouTube | 0 | — | 0 / 0 / 0 | — |
| Giờ máy container | 12 h | — | **≈ 5,0 h** (10:53 → ≈ 15:50 UTC, gồm 2 lượt dựng toàn bộ do sửa hình học sau soát) | CHECKPOINT |
| **Tổng tiền API/GPU** | | | **$0** | |

Chi phí mô hình của chính phiên Claude Code không nằm trong bảng (không có số đo trong phiên).

## §11. Chỉ số trong ±5 % quanh ngưỡng
| Chỉ số | Giá trị | Ngưỡng | Lệch | Ghi chú |
|---|---|---|---|---|
| Trời + sương, toàn cảnh P1 (M1-rong, M3-rong, M4-rong) | 20,0 % / 20,0 % / 19,7 % (M1-rong một ô 20,8 %) | ≤ 20 % (LOOK-2 T3: 8–20 %) | 0 … +4 % | sát mép trên — máy P1 giữ như BANG-SHOT-v1, không chỉnh để "đạt số" |
| Bão hoà trung vị, ô M2-dem / M3-trung | 0,416 / 0,412 | ≥ 0,40 (§14.4) | +4 % / +3 % | khung đêm; khung ngày đều dưới ngưỡng xa (0,024–0,37) — quyết định L2 |
| Nhà cháy (hình học) | 12 262 | dữ kiện ≈ 13 200 | −7,1 % (ngoài ±5 %) | bậc 5, không lên lời |
| Diện tích vùng cháy (Doornick, đọc lại điểm khống chế) | 148,3 ha = 366 acre | dữ kiện "over 400 acres" | −8,5 % (ngoài ±5 %) | tiền kỳ 399 acre với bộ điểm cũ (đã mất); hình học không lên lời; đề xuất: thêm điểm khống chế trong vùng cháy (Guildhall, Royal Exchange) khi làm bản đồ hoạt hoá |
| Khớp Doornick affine RMS | 49,9 m | tiền kỳ 44,2 m | +13 % | bộ điểm mới (11 + 3 kiểm) |
| Nước trong khung | ≤ 30,2 % | ≤ 33,3 % (§11.4) | −9 % | ngoài ±5 % — ghi để rõ |

## §12. Quyết định đề xuất
Xem `PHIEU-LOOK.md` §3 (L1–L6). Ba điểm chính: **L2** ngưỡng bão hoà ≥ 0,40 (§14.4) không hợp London ở biến thể A/B → đề xuất ngưỡng theo tập; **L3** người/xe cho khung trung/cận ở sản xuất; **L6** "estimated infill" ghi trong thẻ phương pháp thay vì tông khác.

## §13. Việc chờ chủ dự án
1. **Chọn mù** 8 hàng ở `reports/look-t4/to-chon-mu.jpg` (ô 1080p: `reports/look-t4/khung/<hàng>-<X|Y|Z>.jpg`) + trả lời Q1–Q3 trong `PHIEU-LOOK.md`. Không mở `khoa.json` trước khi chọn.
2. Quyết định L2–L6.
3. Phiên P: chép RIGHTS mục F vào `RIGHTS.md`; sau khi chọn, ghi look T4 vào `LOOK-KHOA` + Kinh thánh §14.7; merge nhánh (phiên này không merge).
