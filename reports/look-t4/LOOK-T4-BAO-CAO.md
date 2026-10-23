Nhánh thật: `k2c-t4-02-look` (gốc `origin/k2c-t4-02-tienky` @888de179). Nhánh mặc định của bộ khung `ccr-32b90b5c-vzo2m7` KHÔNG dùng (lệnh gọi tên nhánh). SHA cuối = đỉnh nhánh (commit "… — DỪNG chờ chủ dự án").

# BÁO CÁO LOOK-T4 — khoá look tập K2C-T4-02 London (mốc M1b) · 23/10/2026

## §0. Nhánh, SHA, phạm vi
- Nhánh `k2c-t4-02-look`, gốc `origin/k2c-t4-02-tienky` @888de179. Commit của phiên: [[COMMITS]]. Đã đẩy, **không merge**.
- Chỉ sửa trong vùng giao: `design/k2v/ldn/**` (mới: `look.js`), `scripts/k2ldn/**` (mới + sửa đường dẫn `du-lieu/` → `mo-hinh/` trong 4 tệp tiền kỳ), `channel-k2/k2c-t4-02/` (chỉ THÊM `look/`, `mo-hinh/`, `licenses/met-336038|336039|757299.json`, `licenses/SHA256-TU-LIEU-LOOK.txt`, `.gitignore` của thư mục tập; THÊM mục F vào cuối `RIGHTS-NHAP.md` theo lệnh "ghi RIGHTS-NHAP"), `reports/look-t4/**`. Không chạm `checks/`, `docs/`, sổ cái, `tools/`, `design/k2v/tl/**`, `design/cong3/shared/**`, `channel-k2/k2c-t3-01/**` (chỉ đọc LUT), `LOI-NHAP-v1.md`, `BANG-SHOT-v1.*`, `TREATMENT.md`, `main`.
- Mọi commit qua preflight (`set -o pipefail`) "— ĐẠT" + `lock.py --verify` KHỚP; hook pre-commit + pre-push cài trước lần đẩy đầu. Không force-push, không amend.
- Tệp lớn ngoài git ở `/var/tmp/ldn/` (OSM, LiDAR, tư liệu gốc, vân, hình học `ldn2.bin`, lightmap, khung thô, khung theo biến thể) — tái tạo bằng lệnh trong `scripts/k2ldn/`; mọi ĐẦU VÀO đọc tay (điểm khống chế, ranh cháy, toạ độ nhà thờ, máy, tham số look, LUT) nằm trong git.

## §1. Việc 1 — NÂNG HÌNH HỌC + VẬT LIỆU (dùng chung mọi mốc)
Mã: `scripts/k2ldn/hinh_hoc_look.py` (hình học v2 → `ldn2.bin`, SHA trong `ldn2.json`) + `design/k2v/ldn/look.js` (trang dựng look) + `scripts/k2ldn/nuong_look.py` (lightmap Cycles). Tiền kỳ (`hinh_hoc.py`, `page.js`) giữ nguyên để tái lập bản thử.

**Trước / sau (cùng điểm máy xương sống P1, 1666 ngày):** `reports/look-t4/so/truoc-sau-P1-1666.jpg` (trái: tiền kỳ T4, phải: look v2 — **mở SAU khi chọn mù**, vì ảnh phải trùng một ô của tờ mù). Tiền kỳ: nhà đồng dạng màu cam, nền bến bãi màu cát, bờ sông bậc thang, Old St Paul's khối hộp. Look: lô đa dạng + vân + khung gỗ/cửa sổ thủ tục, bờ mịn có kè/cầu thang nước, nước phản chiếu, đồi xa, Old St Paul's theo Hollar.

| Hạng mục | Làm gì (look v2) | Số đo / nguồn | Bậc (§12.2) |
|---|---|---|---|
| Nhà 1666 theo lô | Lô dọc 7 247 phố OSM còn giữ (bỏ phố sau 1666) trong mặt nạ Doornick; mặt tiền 3,4–11 m (45 % 1 khoang, 43 % 1,5 khoang, 12 % nhà giàu/quán trọ 7–11 m); sâu 7–14 m; 2–5 tầng theo hạng phố; **72 % đầu hồi ra phố** (mái 46–56°), còn lại nóc song song phố; **tầng nhô (jetty)** 0,35–0,6 m ở nhà ≥ 3 tầng mặt phố; ống khói gạch 85 %; vật liệu 78 % trát + khung gỗ, 10 % ván gỗ, 12 % gạch; tầng trệt cửa hàng ở mặt phố; lòng phố không bị lô lấn | **43 057 lô** + 113 kho/bến ven sông; lõi khối lấp (≤ 45 m từ phố, ven sông ≤ 110 m) — "estimated infill" | 5 lô · 4 kiểu nhà (Hollar Long View, Prospects) |
| Nhà sau 1667 (Rebuilding Act) | Trên đúng lô cháy, tường gạch, mặt tiền phẳng, nóc song song phố, gác mái; **4 hạng**: by-lane 2 tầng · phố/ngõ đáng kể 3 · phố lớn 4 · dinh thự không ra phố 4 | 12 447 nhà: hạng 1 = 6 556 · 2 = 4 923 · 3 = 754 · 4 = 214 (dữ kiện ≈ 13 200 nhà cháy → −5,7 %) | 4–5 |
| Thành phố 1840–1940 | Khối Victoria–Edward (4–6 tầng, gạch 72 % / Portland 28 %, cửa hàng tầng trệt) thay nhà cũ trên **cùng lô**, sống tới bom 29/12/1940 (vùng ước lượng) hoặc tới năm dựng toà OSM phủ lô | 27 197 khối | 5 |
| Nhà thờ giáo xứ | Doornick **không** đánh dấu nhà thờ trong vùng cháy (số 1–93 là tên PHỐ theo bảng chú giải) → toạ độ 78 nhà thờ từ bài Wikipedia + 30 nhà thờ OSM ngoài vùng; 1666: thân đá + tháp vuông (răng cưa/chóp chì); cháy → phế tích → **49 nhà thờ Wren** (theo danh sách 34 nhà thờ không dựng lại, Reynolds 1922) với tháp/chóp Portland | `mo-hinh/nha-tho-1666.json`; 67 nhà thờ OSM dựng bằng đá (không thành khối văn phòng) | 3 vị trí · 5 hình tháp 1666 |
| Old St Paul's (D6) | Dựng lại theo Hollar/Dugdale 1658 (Met 336039 mặt nam, 395057 mặt đông): dài 179 m, thân 30 m, cánh ngang 88 m; thân tây Romanesque bọc lại (cửa sổ tròn, 12 khoang), hợp xướng Gothic 12 khoang có trụ bay + chóp, mặt đông cửa sổ hoa hồng, tháp giao điểm 20 m vuông tới ≈ 62 m (Hooke 1664: 204 ft) + 4 chóp góc, portico Inigo Jones 10 cột, nhà thờ St Gregory áp góc tây nam; phế tích sau cháy | kích thước Clifton-Taylor tr. 275 (qua Wikipedia); tháp: Hooke 1664 (Jardine 2001) | 3 kích thước · 4 tỉ lệ |
| St Paul's (Wren) | Thân 2 tầng tường màn 33,5 m, cánh ngang 75 m có portico bán nguyệt, apse; tháp tây 65 m có vòm + chóp mạ vàng; **trống 32 cột**, gác, vòm chì ngoài, đèn lồng, quả cầu + thập giá tới **111 m** | 158 m / 75 m / 37 m / 111 m (Fletcher 1962 qua Wikipedia); bỏ 147 phần OSM chồng lên St Paul's/Tower (trước đó tạo "trụ kính" quanh mái vòm) | 3 + 4 |
| Cầu London 1666 | 19 vòm trên trụ có starling, dãy nhà 4–6 tầng hai bên lòng cầu, phần nhô ra sông trên chân gỗ, **khoảng trống cháy 1633** ở đoạn bắc, Nonsuch House 4 tháp củ hành | Hollar (Met 17.50.100, CC0) | 4 · khoảng trống bậc 5 vị trí |
| Bờ sông | **1666**: mép nước = đường đồng mức của mặt nạ nước làm trơn Gauss σ 6 m + hoà cao độ smoothstep (không răng cưa ô); kè gỗ theo mép + cầu thang nước/cầu tàu ngẫu nhiên; dải kho/bến/nhà dày ≤ 150 m từ bờ bắc (Fleet → Tower) — mặt nạ cháy Doornick bỏ mép sông nên dải này nay **có nhà và cháy** theo trường giờ (Thames Street); **2026**: tường Embankment granite | 1 987 đoạn kè gỗ · 1 793 đoạn Embankment | 4–5 |
| Mặt nước Thames | Sóng gradient fbm dị hướng 2 tầng (không ô vuông lặp), Fresnel, **phản chiếu phẳng** (máy đối xứng + mặt phẳng cắt, nửa độ phân giải), màu nước sông theo biến thể, ánh lửa phản chiếu; không viền xanh nhạt / mảng bọt (LOOK-4 T3) | — | — |
| Toà 2026 | OSM + LiDAR (7 424 toà lấy cao độ từ DSM − DTM); dùng **building:part** (bỏ đường bao khi có phần); Leadenhall **vát** (mái nghiêng theo bắc → nam); 30 St Mary Axe tròn xoay theo hồ sơ; vật liệu theo độ cao/năm: > 60 m kính rèm (80 %) / đá; trước 1914 Portland/gạch; còn lại bê tông-đá / kính / gạch / Portland; cửa sổ thủ tục theo tầng 3,8–3,9 m | 16 786 toà · 6 cầu (một mặt cầu/cầu + trụ) | 1 hình khối · 5 vật liệu |
| Mặt đất | Lớp phủ 2 m theo năm: 1666 phố sỏi, sân đất, vườn trong khối (Doornick vẽ vườn), bến (sỏi + ván), bãi bùn; 2026 nhựa, vỉa hè, cỏ (OSM); tro tối trên vùng đã cháy > 4 h | `cls66.png`, `cls26.png` | 4–5 |
| Cây, thuyền, khói bếp | Cây tán (vườn 1666 trong khối, công viên 2026; mùa đông 1940 trụi lá) 2 139 cây; thuyền theo mốc 153 (1666: đò wherry 70, sà lan 22, tàu buồm neo dưới cầu 14 — buồm cuộn; 1940: sà lan + tàu kéo; 2026: tàu khách + sà lan), không đặt sát điểm máy; khói bếp 2 338 ống khói (mật độ theo biến thể; 2026 không) | — | 4–5 |
| Người / xe | **Chưa dựng** (khung look ở ≥ 19 m, người < 2 px ở khung rộng) → đề xuất L3 | — | — |
| Ánh sáng nướng | Cycles **CPU** 1 m/texel, 32 spp, hộp 3,2 × 2,3 km, 3 mốc (1666 / 1940 / 2026): **93,8 · 88,3 · 109,1 s**; R = bức xạ trời có che khuất + nảy → AO phố + chân tường (tắt dần theo cao). GPU **không thuê**: CPU đã < 2 phút/mốc (đo), thuê pod chỉ để nướng tốn thời gian khởi động hơn | `bake_*.png.json` | — |
| Khí quyển | Sương có độ cao (tích phân mật độ e^(−y/H) dọc tia máy) + lớp khói than thấp riêng (biến thể B) + đồi xa ngoài hộp (Hampstead/Highgate bắc, Sydenham/Norwood nam — bậc 5) + dãy nhà xa theo năm | — | 5 (đồi xa) |

Hình học cuối: **2 283 957 tam giác** (`ldn2.bin` SHA-256 [[SHA_BIN]]).

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
[[VIEC3]]

## §4. Việc 4 — TỜ CHỌN MÙ + CLIP
[[VIEC4]]

## §5. Việc 5 — TRANH KHẮC (D7) với Old St Paul's mới
[[VIEC5]]

## §6. Việc 6 — ƯỚC LẠI GIỜ MÁY / CHI PHÍ
[[VIEC6]]

## §7. Việc 7 — PHIẾU CHỌN
`reports/look-t4/PHIEU-LOOK.md`: cách chọn (mỗi hàng 1 cột hoặc "không cột nào đạt"), Q1–Q3 (đồ chơi / khói–lửa / nhận ra London), quyết định đề xuất L1–L6. Phiên này **không** chấm mù bằng AI, **không** dùng AI soi có phí (O2: không); tự soi lỗi bằng mắt từng khung (lỗi đã sửa ghi ở §9).

## §8. Nguồn mới + giấy phép
Chi tiết: `channel-k2/k2c-t4-02/RIGHTS-NHAP.md` mục F. Tóm tắt: Met 336039 / 336038 / 757299 (Hollar + Dugdale 1658, CC0, JSON nguyên văn trong `licenses/`); 16 vân Poly Haven CC0 (`look/van-cc0.json`, SHA từng tệp); toạ độ 78 nhà thờ (Wikipedia API, dữ kiện, bậc 3); kích thước Old St Paul's (Clifton-Taylor; Hooke 1664) và St Paul's (Fletcher 1962) qua Wikipedia (bậc 3). Dữ liệu cũ dùng lại: OSM (ODbL), EA LiDAR (OGL v3), Doornick (Rijks PDM). Không AI sinh hình trong khung look.

## §9. Sự cố
[[SUCO]]

## §10. Chi phí thật
[[CHIPHI]]

## §11. Chỉ số trong ±5 % quanh ngưỡng
[[NGUONG]]

## §12. Quyết định đề xuất
Xem `PHIEU-LOOK.md` §3 (L1–L6). Ba điểm chính: **L2** ngưỡng bão hoà ≥ 0,40 (§14.4) không hợp London ở biến thể A/B → đề xuất ngưỡng theo tập; **L3** người/xe cho khung trung/cận ở sản xuất; **L6** "estimated infill" ghi trong thẻ phương pháp thay vì tông khác.

## §13. Việc chờ chủ dự án
1. **Chọn mù** 8 hàng ở `reports/look-t4/to-chon-mu.jpg` (ô 1080p: `reports/look-t4/khung/<hàng>-<X|Y|Z>.jpg`) + trả lời Q1–Q3 trong `PHIEU-LOOK.md`. Không mở `khoa.json` trước khi chọn.
2. Quyết định L2–L6.
3. Phiên P: chép RIGHTS mục F vào `RIGHTS.md`; sau khi chọn, ghi look T4 vào `LOOK-KHOA` + Kinh thánh §14.7; merge nhánh (phiên này không merge).
