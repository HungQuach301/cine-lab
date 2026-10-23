Nhánh thật: `k2c-t4-02-look2` (gốc `origin/k2c-t4-02-look` @5123bebf). Nhánh mặc định của bộ khung (`claude/practical-mendel-u8qqn3`) KHÔNG dùng (lệnh gọi tên nhánh). SHA cuối = đỉnh nhánh (commit "… — DỪNG chờ chủ dự án").

# BÁO CÁO LOOK-T4-V2 — vòng look thứ hai T4 London (K2C-T4-02) · 23/10/2026

Căn cứ: chủ dự án chấm tờ LOOK-T4 (23:14) + nhận xét 23:41 — "1. Thành phố vẫn còn trông như “đồ chơi” 2. Khói và lửa cần rõ hơn 3. Các công trình biểu tượng chưa được rõ nét"; look hợp nhất 23:27 (A chuẩn + cháy ngày 1666/1940 ấm kiểu C + đêm cháy 1666 khói than dày kiểu B); L2–L6 theo khuyến nghị; lệnh 23:45 "1,2,3,4,5, đồng ý theo khuyến nghị".

## Tóm tắt (đọc trước)
- **Công trình (việc 1):** St Paul's, Monument, White Tower dựng lại chi tiết cao theo kích thước có nguồn PD (Gilbertson qua Gutenberg #48491; *London and Its Environs* 1761 qua Gutenberg #60008) + OSM. **Sửa lỗi vị trí Monument của look v1 (lệch ≈ 68 m).** Đo ở P1 1080p: vòm **46 px** (khung P1 fov 50°) — **TRƯỢT ngưỡng ≥ 60 px**; đạt **67 px** nếu P1 dùng fov 36° (cùng vị trí/hướng). **Monument và Tower nằm NGOÀI khung P1** (phương vị 49° và 77°, mép phải khung 46,7°) — đo từ vị trí P1 quay máy về từng công trình: Tower 49 px (đạt ≥ 12), **Monument 7 px (fov 50°) / 10 px (fov 36°) — TRƯỢT ≥ 12 px** vì thân cột bị khối văn phòng 2026 che, chỉ còn nón + bầu lửa ló lên. 3 chi tiết: đèn lồng vòm ĐỌC ĐƯỢC (14 px rộng ở P1), bầu lửa vàng Monument ĐỌC ĐƯỢC (4 px, sáng vàng trên nền xám), tháp góc White Tower MỜ (≈ 6 px/tháp, mũ chì tối khó đọc).
- **Lửa + khói (việc 2):** cách A mới có lõi lửa, quầng sáng, tàn lửa theo gió đông, chân khói hắt đỏ theo độ cao, khói ngày đặc/tối/tách tầng, ánh lửa mặt tiền + mặt sông mạnh hơn. 1 khung Cycles GPU cùng máy/giờ (2 lần chạy, tổng **$0,053** theo số dư RunPod). Tự soi: lửa/khói rõ hơn LOOK-T4 thấy được; khói ngày tầng cao vẫn dạng "rèm"; khung Cycles có khói thể tích phát sáng thật hơn nhưng cảnh Cycles chưa có vân/ánh trăng.
- **Tấm nền AI (việc 3):** 24 tấm (4 khung × 2 công cụ × 3 lượt) + 4 lần ghép lại không gọi AI. **Đạt cổng máy (i)–(v): 1 tấm** — 2026 toàn cảnh, OpenAI lượt 3. Khung 1666 ngày: sau khi sửa 3 lỗi đường ống/3D của chính phiên này (khói bếp trong ảnh vào; dán khói bếp nguyên nền; khói bếp xa không áp sương), OpenAI lượt 3 ở M1-rong chỉ còn trượt (iv) vì **quầng vùng bảo vệ quanh nhà xa 1–2 px** (luật nở 3 px); biến thể THAM KHẢO xếp nhà xa ngoài hộp vào lớp (c) **đạt (i)–(v)** → quyết định V4. Đêm 1940: 0/6 (AI tự thêm cầu, đèn, thuyền). Gemini 0/12: đổi sắc nước (T9b nước→đất 19–69 %).
- **Ước lại (việc 5):** tấm nền khả thi theo số đo: **≈ 5 %** thời lượng theo luật hiện hành, **≈ 13–16 %** nếu duyệt V4 — chưa có số đo cho 35–45 % (đêm/lửa 0/6). Ngân sách Gemini T4 ≈ $35: tấm nền chỉ ≈ $2–6; phần lớn là Omni M-d ($29–43 + kiểm) → **có thể vượt $35** nếu Omni cần 3 lượt.
- **Phiếu:** `reports/look-t4-v2/PHIEU-LOOK-V2.md` (V1–V7).

## §0. Nhánh, SHA, phạm vi, vận hành
- Nhánh `k2c-t4-02-look2`, gốc `origin/k2c-t4-02-look` @5123bebf. Đã đẩy, **không merge**. Danh sách commit: `git log 5123bebf..k2c-t4-02-look2`.
- Sửa trong vùng giao: `design/k2v/ldn/look2.js` (mới; `look.js` giữ nguyên để tái lập LOOK-T4); `scripts/k2ldn/**` (mới: `cong_trinh_v2.py`, `hinh_hoc_v2.py`, `look_khung_v2.py`, `do_cong_trinh.py`, `tam_nen_v2.py`, `tam_nen_bang.py`, `to_so_v2.py`, `v2_chay.sh`, `cy_xuat2.py`, `cy_ldn2.py`, `ai/gemini_batch.py`, `gpu/chay_cy_v2.sh`; sửa nhỏ có ghi chú: `render_look.js` (tham số --page/--lk/--mask), `nuong_look.py` (biến LDN_LOOK), `ai/n2p_lib.py` (biến N2P_DIR), `ai/oai_edit.py` + `ai/vision_kiem.py` (mốc/chặn qua biến môi trường), `gpu/pod.py` (biến NCG_LEDGER)); `channel-k2/k2c-t4-02/` (chỉ THÊM `look/may-v2/`, `ai/lenh-v2/`, `ai/goc-v2/`); `reports/look-t4-v2/**`. Không chạm `checks/` (chỉ CHẠY `checks/ll/q_thoi_dai.py` và `lock.py --verify`, không đọc mã), `docs/`, sổ, `tools/`, `design/k2v/tl/**`, `design/cong3/shared/**`, `channel-k2/k2c-t3-01/**` (chỉ đọc LUT), `LOI-NHAP-v1.md`, `BANG-SHOT-v1.*`, `TREATMENT.md`, `main`.
- Mọi commit qua preflight (`set -o pipefail`, hook pre-commit + pre-push cài trước lần đẩy đầu) "PREFLIGHT ĐẠT" + `lock.py --verify` KHỚP. Không force-push, không amend. Email che (git dùng noreply). UA "CineLab-research (+https://github.com/HungQuach301/cine-lab)". Khoá do proxy gắn, không in/ghi.
- Tệp lớn ngoài git ở `/var/tmp/ldn/` (OSM, LiDAR, tư liệu, vân, hình học `look2/ldn2.bin` SHA trong log, lightmap, khung thô, timelapse, gốc AI PNG/JSON). Ảnh AI tốn tiền: bản JPG ≤ 5 MB trong `channel-k2/k2c-t4-02/ai/goc-v2/` (đưa vào git trong ≤ 10 phút sau khi về), gốc + SHA trong sổ AI.

## §1. Việc 1 — CÔNG TRÌNH BIỂU TƯỢNG (lớp dữ kiện, 3D, không AI)
Mã: `scripts/k2ldn/cong_trinh_v2.py` (St Paul's, Monument, White Tower) gọi qua `scripts/k2ldn/hinh_hoc_v2.py` (thay 3 hàm của `hinh_hoc_look.py`; hàm cũ vẫn được gọi trên lưới bỏ đi để chuỗi ngẫu nhiên của phần thành phố còn lại KHÔNG lệch). Nguồn + trích nguyên văn + bậc: `reports/look-t4-v2/NGUON-CONG-TRINH.md`.

| Công trình | Làm gì (V2) | Kích thước dùng · nguồn | Bậc §12.2 |
|---|---|---|---|
| St Paul's (Wren) | Bố cục lại theo kích thước nguồn: dài 157 m (look v1 ≈ 178 m — dài quá ≈ 20 m), tường màn 2 tầng có cửa sổ theo khoang + trụ áp + lan can sáng, cánh ngang + portico bán nguyệt có cột, mặt tây 54,9 m: portico 2 tầng cột ghép đôi (12 + 8) + trán tam giác, **hai tháp tây 67,4 m** (tầng chuông mở có cột ghép đôi, mũ chì cong, quả dứa mạ vàng); trống Ø 34,1 m: hàng 32 cột + 8 khối đặc + Stone Gallery + tầng gác có 24 cửa sổ; **vỏ vòm chì Ø 31,1 m có 24 gân** (shader theo góc); Golden Gallery + lan can sắt; **đèn lồng có 4 cánh trụ + 8 ô cửa**; mũ chì; quả cầu vàng Ø ≈ 2 m; thập giá tới 111,3 m | 515 / 250 / 180 / 112 / 102 / 221 / 365 ft (Gilbertson, Gutenberg #48491); 110 ft lan can, 121 ft thân (Wikipedia) | 3 (kích thước) · 4–5 (tỉ lệ tầng, số cột, đèn lồng) |
| Monument | **Đặt lại theo OSM r3374550 (532923, 180761)** — look v1 lệch ≈ 68 m; đế 27 ft, bệ 21,5 ft × 40 ft + gờ + 4 khối rồng góc, thân Doric 20 rãnh Ø 15 ft cao 120 ft, đầu cột + abacus + lan can sắt, nón 32 ft, bầu lửa mạ vàng + 9 lưỡi lửa | 15 / 120 / 40 / 42 / 32 ft (*London and Its Environs* 1761, Gutenberg #60008); 21,5 / 27 ft (Strype 1720 qua lookup.london — thứ cấp, chưa đọc gốc) | 1 vị trí · 3 · 5 (rồng, lưỡi lửa) |
| White Tower | Theo tâm + trục OSM w369135772; 36 × 32 m, 27 m; răng cưa lan can, trụ áp, 3 tầng cửa sổ; tháp vuông TB + TN, tháp tròn ĐB, apse bán nguyệt ĐN; mũ chì cong + chong chóng mạ vàng; màu quét vôi trắng; tường thành giữ như v1 + 3 tháp giữa mỗi cạnh tường (bậc 5) | Wikipedia "White Tower" (36 × 32 m, 27 m, vị trí tháp góc) | 1 · 3 · 4 (mũ chì, Hollar) · 5 |
| Old St Paul's, London Bridge 1666 | Giữ như LOOK-T4 (Hollar/Dugdale 1658) | — | — |
| 30 St Mary Axe, Leadenhall | Hình khối giữ (OSM + LiDAR); **vật liệu** riêng: dải kính tối xoắn + lưới kim cương (mt 15); khung giằng chéo lộ (mt 16) | ảnh công khai | 1 hình khối · 4 vật liệu |

Hình học: 2 276 564 tam giác (`look2/ldn2.bin`, SHA-256 `73e68223b0bb7b7224340c61465f1aefcec440e129440f656c024262ec6766f3`), = look v2 dựng lại hôm nay (`40f8f1aa…`, 2 271 093 tam giác) + 5 471 tam giác công trình. **Lưu ý:** look v2 dựng lại KHÁC SHA bản LOOK-T4 (`fef45294…`) vì OSM sống đã đổi (lô 42 898 → 42 951, toà 2026 16 786 → 16 787) — cột "LOOK-T4 đã chọn" của tờ so dùng đúng ảnh trong git của LOOK-T4.

**Số đo 1080p từ điểm máy P1 [532330, 180250, 230]** (mặt nạ mã công trình có che khuất thật, `scripts/k2ldn/do_cong_trinh.py`; thước bỏ cụm lẻ < 5 px; ô cắt phóng ×3 lân cận gần nhất: `reports/look-t4-v2/cong-trinh/`; số: `reports/look-t4-v2/do/cong-trinh.json`). Năm 2026 ngày (khung M4-rong).

| Đo | P1 khung thật (fov 50°) | P1 fov 36° (cùng vị trí/hướng) | P1 quay nhìn thẳng công trình, fov 50° / 36° | Ngưỡng lệnh | Kết quả |
|---|---|---|---|---|---|
| Bề ngang VỎ VÒM St Paul's | **46 px** | **67 px** | 39 / 55 | ≥ 60 | TRƯỢT ở fov 50°; đạt ở fov 36° |
| — trống (hàng cột) | 51 | 73 | 43 / 61 | — | — |
| — đèn lồng (gồm Golden Gallery, cầu, thập giá) | 14 × 32 | 20 × 51 | 11 / 16 | chi tiết nhận ra | ĐỌC ĐƯỢC (ô cắt) |
| — tháp tây (mỗi tháp) | 34 × 81 | 49 × 144 | 27 / 38 | — | — |
| Monument (phần thấy được) | ngoài khung (phương vị 49°) | ngoài khung | **7 / 10** (thân cột chỉ thấy 1 px — khối văn phòng 2026 che; bệ khuất hẳn) | ≥ 12 | **TRƯỢT** |
| — bầu lửa mạ vàng | — | — | 4 × 4 / 4 × 6 | chi tiết nhận ra | ĐỌC ĐƯỢC (chấm vàng sáng) |
| White Tower (khối + tháp góc) | ngoài khung (phương vị 77°) | ngoài khung | **49 / 70** (khối chính 38 / 54) | ≥ 12 | đạt |
| — mỗi tháp góc | — | — | ≈ 6 px (6,6 m ở 1,32 km) | chi tiết nhận ra | MỜ — mũ chì tối khó đọc |

Đọc số: ngưỡng ≥ 60 px cho vòm ở P1 **không đạt được với kích thước đúng nguồn ở fov 50°** (vòm 31,1 m ở ≈ 0,94 km). Không phóng to mô hình để "đạt số" (luật cứng). Đường đạt: P1 fov 36° (đề xuất V5) hoặc máy gần hơn. Monument: kể cả fov 36° cũng không đủ 12 px vì bị che ở 2026; ở 1700–1840 (trước khối Victoria) Monument sẽ lộ cả thân — chưa đo (không có khung đó trong tờ so).


## §2. Việc 2 — LỬA + KHÓI (lớp dữ kiện, 3D)
Mã: `design/k2v/ldn/look2.js` (bản sao `look.js` + nâng; LOOK-T4 tái lập được bằng `look.js`). Look hợp nhất theo mốc ở `scripts/k2ldn/look_khung_v2.py` → `channel-k2/k2c-t4-02/look/may-v2/*.json` (cùng máy/giờ 8 hàng LOOK-T4).

| Hạng mục | LOOK-T4 (A) | V2 |
|---|---|---|
| Ngọn lửa | sprite atlas cam đều | **lõi vàng trắng** (t² + nhánh lõi), cỡ 5–14 m (trước 4–11), + **quầng sáng** mềm 26–48 m trên mỗi ô cháy (cộng sáng, đêm ×4) |
| Tàn lửa | không có | **tàn lửa bay theo gió** (5/ô 1666, 3/ô 1940): bốc 60–220 m, trôi theo gió 160–460 m, chập chờn; cỡ ≥ 1,5 px ở mọi khoảng cách |
| Khói ngày | xám nhạt, mỏng như sương | **đặc khối, mép rõ, nâu đen ở chân → xám nâu lên cao**, được nắng chiếu theo kênh G atlas; **tách tầng**: cột bốc tới trần 0,36–0,70 km rồi loang ngang theo gió đông; chân cột hắt lửa cả ban ngày |
| Khói đêm | toàn cụm phát sáng cam | **chỉ chân cột/mặt dưới tầng khói (< ≈ 150 m) hắt đỏ** theo độ cao thật của cụm khói; tầng trên tối |
| Ánh lửa | mặt tiền ×(2,2 · 0,5 · 0,06), mặt sông ×(0,14 · 0,05) | mặt tiền ×(2,4 · 0,85 · 0,14) (lan xa hơn), mặt sông ×(0,30 · 0,12) |
| Look | A | A + C ấm (M2-ngay, M3-*), A + B khói than (M2-dem); sương phối cảnh 1/16 → **1/10 km**; mái/tường phong hoá theo nhà (chống "đồ chơi", `uToy`) |

Ba khung so (cách A mới): `khung/M2-ngay-v2-3d.jpg` (ngày khói 3/9/1666 15:00, P1), `khung/M2-dem-v2-3d.jpg` (đêm 2/9 23:00 từ giữa sông, P6), `khung/M3-trung-v2-3d.jpg` (đêm 29/12/1940 22:30 quanh mái vòm, Fleet St) — cột "LOOK-T4 đã chọn" cạnh từng ô trên tờ so.

**Cycles GPU (một khung cùng máy/giờ M2-dem):** cảnh xuất bằng `scripts/k2ldn/cy_xuat2.py` (hình học V2, 772 246 tam giác, 169 ô cháy) → RunPod.
| Lần | Cảnh | GPU | Bật → tắt | Dựng 1 khung 1080p | $ ước theo giờ | Ghi chú |
|---|---|---|---|---|---|---|
| 1 | `cy_ldn.py` (tiền kỳ, giữ nguyên) spp 48 | RTX 5090 SECURE $1,19/h | 74 s (sẵn sàng 22 s; cài + tải 24 s) | **10,85 s** (23 s gồm nạp cảnh) | $0,024 | mặt tiền cháy trắng cả mảng; khói lốm đốm — không công bằng để so → `khung/M2-dem-cycles-ban1.jpg` |
| 2 | `cy_ldn2.py` (chỉnh: cháy theo mảng, lửa thể tích sáng hơn, khói cụm lớn, trăng) spp 64 | RTX 4090 SECURE $0,89/h (5090 hết máy, HTTP 500) | 117 s | **23,83 s** (33 s gồm nạp) | $0,029 | khói thể tích phát sáng mềm, phản chiếu sông; thiếu vân, ánh trăng yếu → cột "Cycles" tờ so |
Số dư RunPod: $21,138 → **$21,085 (thật $0,053)**; pod xoá HTTP 204 cả hai lần; không pod nào còn chạy.

Tốc độ sản xuất cách A V2 (1080p, spp 4, P = 2, 24 khung, trung vị khung 1–23): ngày 1666 **7,04 / 7,11 s**; đêm lửa 1940 **7,16 / 7,11 s** (LOOK-T4: 7,28–7,75 s) — thêm tàn lửa/quầng không làm chậm đo được. Khung tĩnh spp 24: 38–47 s.

Tự soi (thẳng): khói ngày V2 đọc thành cột/khối rõ hơn, nhưng **tầng cao vẫn là "rèm" sprite lặp**; đêm 1940: các đám cháy rời + tàn lửa + cột khói hắt đỏ đọc tốt; **St Paul's bị ánh lửa hắt trắng đều** (đọc như đèn pha) — nên giảm ánh lửa trên Portland ở vòng sau; mặt sông đêm 1940 gần đen (không thấy phản chiếu lửa vì lửa cách sông > 500 m).


## §3. Việc 3 — TẤM NỀN AI N2+ (§15 b–c)
**Cách làm** (`scripts/k2ldn/tam_nen_v2.py`): ảnh vào = khung V2 đã áp LUT kênh, **không gửi mặt nạ**; 1940 ảnh vào KHÔNG lửa/khói (lửa 3D ghép lại theo mặt nạ sai khác có/không lửa > 8/255 → nhãn 'lua' = lớp (a)); 1666 ảnh vào KHÔNG khói bếp (khói bếp = vật chuyển động, ghép lại bằng CỘNG HIỆU render có/không khói — xem V3). Ghép lớp (a) (mặt nạ ID: nhà/công trình/cầu/tường 'nha', thuyền 'tau', nhà xa ngoài hộp 'khac', lửa 'lua'; nở 1 px, vật < 60 px nở 3 px, viền ≤ 3 px) + khớp màu render VÀO tông tấm (Lab toàn cục, k = 0,7 — như T6). Phóng ảnh AI về 1920×1080 bằng Lanczos (không dùng bộ phóng AI). Lệnh: `channel-k2/k2c-t4-02/ai/lenh-v2/*-l{1,2,3}.txt` (chỉ nêu bề mặt/ánh sáng; lượt 1 cho phép thùng/thùng gỗ/bao/đống gỗ ở bến 1666 theo bảng vật; lượt 3 "add nothing"). Ảnh AI: `channel-k2/k2c-t4-02/ai/goc-v2/`. Sổ AI: `reports/look-t4-v2/so-ai.jsonl` (model, lệnh nguyên văn, SHA vào/ra, usage, $, C2PA, thời gian chờ Batch); chi phí kiểm: `cost.jsonl`.
**Cổng** (§15 c): (i) `kiem_n2p.py` max |ghép − render khớp màu| trong lớp (a) + 2 mô hình nhìn liệt kê vật (a) thêm/bớt/đổi; (ii) 2 mô hình (gpt-6.1-sol, claude-sonnet-5-5) + `checks/ll/q_thoi_dai.py` (K, chỉ chạy); (iii) T9b toàn khung + **trong hộp địa hình đã dựng** (bỏ đất xa ngoài hộp + nhà xa) — phép (iii) đang được K-1.17.4 xét, KHÔNG tự nới; (iv) 2 mô hình; (v) timelapse máy CODINH (8 s M1-rong, 3 s còn lại; 640×360): nhấp nháy vùng lớp (c) tĩnh của ghép so đối chứng = cùng đường ghép với tấm = khung render đầu; ngưỡng ≤ 1,5 ×.

**Kết quả mọi tấm** (`reports/look-t4-v2/do/tam-nen.json`; JSON từng tấm ngoài git ở `/var/tmp/ldn/v2/tn/`, nguyên văn mô hình nhìn `*.raw.txt`). l3g = ghép lại lượt 3 với khói bếp cộng hiệu; l3h = sau khi sửa khói bếp xa trong 3D (cùng ảnh AI lượt 3); `-thamkhao` = biến thể THAM KHẢO nhà xa ngoài hộp xếp lớp (c) — KHÔNG phải luật hiện hành, không tính vào tỷ lệ đạt.

| Tấm | (i) max/255 · vật (a) | (ii) lỗi thời đại · q_thoi_dai | (iii) T9b đất→nước / nước→đất % — toàn khung | — trong hộp địa hình | mô hình báo đổi vùng | (iv) | (v) nhấp nháy ghép/đối chứng | ĐẠT (i–iv) |
|---|---|---|---|---|---|---|---|---|
| M1-rong-gem-l1 | 0 · 0 () | 0 · 1 khung soi · nghi vấn 0 ở 0 khung · ghi | 0.02 / 29.77 | 0.05 / 29.77 | 0 | 0  | — | TRƯỢT |
| M1-rong-gem-l2 | 0 · 2 (gpt:cong_trinh:Added pale branching tracks or lanes through the f; gpt:cong_trinh:Added pa) | 0 · 1 khung soi · nghi vấn 0 ở 0 khung · ghi | 0.12 / 34.37 | 0.27 / 34.37 | 2 | 1 claude:khoi | — | TRƯỢT |
| M1-rong-gem-l3 | 0 · 0 () | 0 · 1 khung soi · nghi vấn 0 ở 0 khung · ghi | 1.06 / 19.35 | 2.6 / 19.35 | 0 | 0  | 0.0227 / 0.0066 | TRƯỢT |
| M1-rong-gem-l3g | 0 · 0 () | 0 · 1 khung soi · nghi vấn 0 ở 0 khung · ghi | 1.11 / 19.77 | 2.61 / 19.77 | 0 | 1 claude:khoi | 0.0666 / 0.0662 | TRƯỢT |
| M1-rong-gem-l3h | 0 · 0 () | 0 · 1 khung soi · nghi vấn 0 ở 0 khung · ghi | 1.11 / 19.77 | 2.61 / 19.77 | 0 | 1 claude:khoi | 0.0624 / 0.0619 | TRƯỢT |
| M1-rong-oai-l1 | 0 · 1 (gpt:cong_trinh:Added branching pale tracks between the background) | 0 · 1 khung soi · nghi vấn 0 ở 0 khung · ghi | 2.16 / 25.27 | 0.64 / 25.27 | 0 | 0  | — | TRƯỢT |
| M1-rong-oai-l2 | 0 · 0 () | 0 · 1 khung soi · nghi vấn 0 ở 0 khung · ghi | 0.19 / 0.7 | 0.45 / 0.7 | 0 | 1 claude:khoi | — | TRƯỢT |
| M1-rong-oai-l3-thamkhao | 0 · 0 () | 0 · 1 khung soi · nghi vấn 0 ở 0 khung · ghi | 0.12 / 0.03 | 0.3 / 0.03 | 0 | 1 claude:khoi | — | TRƯỢT |
| M1-rong-oai-l3 | 0 · 0 () | 0 · 1 khung soi · nghi vấn 0 ở 0 khung · ghi | 0.12 / 0.03 | 0.3 / 0.03 | 0 | 2 gpt:khoi; claude:khoi | 0.0246 / 0.0054 | TRƯỢT |
| M1-rong-oai-l3g | 0 · 0 () | 0 · 1 khung soi · nghi vấn 0 ở 0 khung · ghi | 0.15 / 0.03 | 0.35 / 0.03 | 0 | 1 claude:khoi | 0.0663 / 0.066 | TRƯỢT |
| M1-rong-oai-l3h-thamkhao | 0 · 0 () | 0 · 1 khung soi · nghi vấn 0 ở 0 khung · ghi | 0.15 / 0.03 | 0.36 / 0.03 | 0 | 0  | 0.0621 / 0.0617 | ĐẠT |
| M1-rong-oai-l3h | 0 · 0 () | 0 · 1 khung soi · nghi vấn 0 ở 0 khung · ghi | 0.15 / 0.03 | 0.35 / 0.03 | 0 | 2 gpt:khoi; claude:khoi | 0.0621 / 0.0618 | TRƯỢT |
| M1-trung-gem-l1 | 0 · 4 (gpt:cong_trinh:Short low timber railing with upright posts along ; gpt:cong_trinh:Circular) | 0 · 1 khung soi · nghi vấn 0 ở 0 khung · ghi | 0.0 / 68.88 | 0.0 / 68.88 | 2 | 2 gpt:khoi; claude:khoi | — | TRƯỢT |
| M1-trung-gem-l2 | 0 · 1 (gpt:cong_trinh:Broad goods wharf added behind the foreground hous) | 0 · 1 khung soi · nghi vấn 0 ở 0 khung · ghi | 0.0 / 43.47 | 0.0 / 43.47 | 2 | 2 gpt:khoi; claude:khoi | — | TRƯỢT |
| M1-trung-gem-l3 | 0 · 0 () | 0 · 1 khung soi · nghi vấn 0 ở 0 khung · ghi | 0.15 / 25.84 | 0.25 / 25.84 | 0 | 1 claude:khoi | 0.0186 / 0.0035 | TRƯỢT |
| M1-trung-gem-l3g | 0 · 0 () | 0 · 1 khung soi · nghi vấn 0 ở 0 khung · ghi | 0.14 / 26.28 | 0.25 / 26.28 | 0 | 1 claude:khoi | 0.043 / 0.0428 | TRƯỢT |
| M1-trung-gem-l3h | 0 · 0 () | 0 · 1 khung soi · nghi vấn 0 ở 0 khung · ghi | 0.14 / 26.28 | 0.25 / 26.28 | 0 | 1 claude:khoi | 0.041 / 0.0407 | TRƯỢT |
| M1-trung-oai-l1 | 0 · 1 (gpt:cong_trinh:Apparent added closely spaced vertical timber-like) | 0 · 1 khung soi · nghi vấn 0 ở 0 khung · ghi | 11.42 / 18.14 | 1.57 / 18.14 | 0 | 7 gpt:khoi; gpt:khoi; gpt:khoi; gpt:khoi;  | — | TRƯỢT |
| M1-trung-oai-l2 | 0 · 1 (gpt:cong_trinh:Added repeated thin vertical piles and connecting ) | 0 · 1 khung soi · nghi vấn 0 ở 0 khung · ghi | 0.04 / 3.35 | 0.07 / 3.35 | 0 | 7 gpt:khoi; gpt:khoi; gpt:khoi; gpt:khoi;  | — | TRƯỢT |
| M1-trung-oai-l3-thamkhao | 0 · 0 () | 0 · 1 khung soi · nghi vấn 0 ở 0 khung · ghi | 0.15 / 4.83 | 0.27 / 4.83 | 0 | 2 gpt:khoi; claude:khoi | — | TRƯỢT |
| M1-trung-oai-l3 | 0 · 0 () | 0 · 1 khung soi · nghi vấn 0 ở 0 khung · ghi | 0.16 / 4.84 | 0.27 / 4.84 | 0 | 2 gpt:khoi; claude:khoi | 0.0427 / 0.0036 | TRƯỢT |
| M1-trung-oai-l3g | 0 · 0 () | 0 · 1 khung soi · nghi vấn 0 ở 0 khung · ghi | 0.14 / 4.88 | 0.26 / 4.88 | 0 | 2 gpt:khoi; claude:khoi | 0.0429 / 0.0429 | TRƯỢT |
| M1-trung-oai-l3h-thamkhao | 0 · 0 () | 0 · 1 khung soi · nghi vấn 0 ở 0 khung · ghi | 0.14 / 4.86 | 0.26 / 4.86 | 0 | 0  | 0.0408 / 0.0409 | TRƯỢT |
| M1-trung-oai-l3h | 0 · 0 () | 0 · 1 khung soi · nghi vấn 0 ở 0 khung · ghi | 0.14 / 4.88 | 0.26 / 4.88 | 0 | 2 gpt:khoi; claude:khoi | 0.0408 / 0.0409 | TRƯỢT |
| M3-rong-gem-l1 | 0 · 7 (gpt:cong_trinh:Added clusters of dark, block-like buildings acros; gpt:cong_trinh:Added cl) | 0 · 1 khung soi · nghi vấn 0 ở 0 khung · ghi | 1.26 / 0.0 | 2.52 / 0.0 | 2 | 11 gpt:thuyen_nho; gpt:thuyen_nho; gpt:thuy | — | TRƯỢT |
| M3-rong-gem-l2 | 0 · 2 (gpt:cong_trinh:A broad, straight bridge now crosses the river dia; claude:cong_trinh:A lon) | 0 · 1 khung soi · nghi vấn 0 ở 0 khung · ghi | 3.49 / 0.0 | 7.01 / 0.0 | 0 | 10 gpt:thuyen_nho; gpt:thuyen_nho; gpt:thuy | — | TRƯỢT |
| M3-rong-gem-l3 | 0 · 2 (gpt:cong_trinh:Broad, straight bridge crossing the foreground riv; claude:cong_trinh:A lon) | 0 · 1 khung soi · nghi vấn 0 ở 0 khung · ghi | 26.15 / 0.0 | 12.48 / 0.0 | 1 | 1 claude:khoi | 0.02 / 0.0061 | TRƯỢT |
| M3-rong-oai-l1 | 0 · 5 (gpt:cong_trinh:New bridge crossing the foreground river diagonall; gpt:den:Repeated small ) | 0 · 1 khung soi · nghi vấn 0 ở 0 khung · ghi | 0.28 / 0.0 | 0.22 / 0.0 | 1 | 5 gpt:thuyen_nho; gpt:thuyen_nho; gpt:thuy | — | TRƯỢT |
| M3-rong-oai-l2 | 0 · 9 (gpt:cong_trinh:New bridge crossing the foreground river diagonall; gpt:cong_trinh:Added di) | 0 · 1 khung soi · nghi vấn 0 ở 0 khung · ghi | 0.03 / 0.0 | 0.05 / 0.0 | 0 | 14 gpt:may_bay; gpt:may_bay; gpt:may_bay; g | — | TRƯỢT |
| M3-rong-oai-l3 | 0 · 2 (gpt:cong_trinh:Added straight bridge crossing the foreground rive; claude:cong_trinh:Dark ) | 0 · 1 khung soi · nghi vấn 0 ở 0 khung · ghi | 0.29 / 0.0 | 0.51 / 0.0 | 0 | 12 gpt:thuyen_nho; gpt:thuyen_nho; gpt:thuy | 0.0293 / 0.0061 | TRƯỢT |
| M4-rong-gem-l1 | 0 · 8 (gpt:cong_trinh:New slender tower or chimney on the distant skylin; gpt:cong_trinh:Added cl) | 0 · 1 khung soi · nghi vấn 0 ở 0 khung · ghi | 8.73 / 23.92 | 21.29 / 23.92 | 0 | 4 gpt:xe_may; gpt:xe_may; gpt:xe_may; gpt: | — | TRƯỢT |
| M4-rong-gem-l2 | 0 · 11 (gpt:cong_trinh:New paths, edging and curved paved circulation aro; gpt:cong_trinh:Added cu) | 0 · 1 khung soi · nghi vấn 0 ở 0 khung · ghi | 8.03 / 7.2 | 19.57 / 7.2 | 0 | 3 gpt:xe_may; gpt:nguoi; gpt:nguoi | — | TRƯỢT |
| M4-rong-gem-l3 | 0 · 0 () | 0 · 1 khung soi · nghi vấn 0 ở 0 khung · ghi | 4.89 / 8.82 | 11.92 / 8.82 | 0 | 0  | 0.0001 / 0.0 | TRƯỢT |
| M4-rong-oai-l1 | 0 · 3 (gpt:chu:Added painted lane lines, junction markings and cr; gpt:chu:Added road and junctio) | 0 · 1 khung soi · nghi vấn 0 ở 0 khung · ghi | 9.0 / 9.17 | 3.4 / 9.17 | 0 | 0  | — | TRƯỢT |
| M4-rong-oai-l2 | 0 · 3 (gpt:cong_trinh:A ground-floor arcade or row of recessed entrances; gpt:cong_trinh:New indi) | 0 · 1 khung soi · nghi vấn 0 ở 0 khung · ghi | 2.1 / 0.88 | 5.1 / 0.88 | 0 | 0  | — | TRƯỢT |
| M4-rong-oai-l3 | 0 · 0 () | 0 · 1 khung soi · nghi vấn 0 ở 0 khung · ghi | 0.89 / 0.0 | 2.17 / 0.0 | 0 | 0  | 0.0001 / 0.0 | ĐẠT |

**Tỷ lệ đạt theo luật hiện hành:** 1/24 lượt AI (M4-rong OpenAI lượt 3: (i) 0/255, 0 vật; (ii) 0; (iii) 0,89 / 0,00 % toàn khung — 2,17 / 0,00 % trong hộp; (iv) 0; (v) 0,0001 ≈ đối chứng). Theo khung × công cụ (≤ 3 lượt): OpenAI 1/4 khung, Gemini 0/4.
- **Gemini (Nano Banana 2.1, Batch):** giữ ánh sáng/tông ảnh vào tốt nhất bằng mắt, nhưng **đổi sắc nước sang xám–ô liu** (chẩn đoán M1-rong lượt 1: H trung vị 70°, S 26 → ngoài định nghĩa "màu nước" T9b) — nước→đất 19,8–68,9 %; lượt 1–2 thêm lối/cầu tàu/nhà/thuyền; đêm 1940 thêm cầu sáng + thuyền.
- **OpenAI (gpt-image-2.5-sunburst-2026-09-08, edits, không mặt nạ, high):** lượt 1–2 thêm lối, vạch kẻ đường (2026), khói; lượt 3 sạch hơn: 2026 đạt; 1666 M1-rong chỉ còn (iv) do **quầng ghép nhà xa** (biến thể tham khảo đạt cả (i)–(v)); M1-trung (iii) nước→đất 4,9 %.
- **Đêm 1940: 0/6** — cả hai công cụ đều thêm cầu/đèn/thuyền/máy bay (OpenAI lượt 2: "máy bay") — cảnh đêm không nên dùng tấm nền với lệnh hiện tại.
- **Ba lỗi của chính phiên này đã tìm và sửa** (làm hỏng kết quả lượt 1–3 ban đầu): ảnh vào 1666 có khói bếp (AI vẽ khói lên tấm tĩnh); khói bếp dán nguyên điểm ảnh render cả nền sương ("đốm trắng"); khói bếp 3D ở xa không áp sương (lỗi có từ look v1). Sau khi sửa, (iv) 1666 còn trượt chỉ vì quầng vùng bảo vệ của nhà xa 1–2 px (đã chứng minh bằng biến thể tham khảo).
- **(v) nhấp nháy:** mọi tấm sau khi sửa khói bếp: tỷ lệ 0,998–1,008 × đối chứng (đạt); trước khi sửa 3,3–11,9 × (khói bếp dán nguyên nền). Tuyệt đối ≤ 0,07 mức xám/khung so với render thô 2,24–2,48.

**Giá + thời gian (thật, theo sổ):**
| Công cụ | Ảnh | $ ảnh | $/ảnh | Kiểm/lượt (gpt + claude + q_thoi_dai) | $/lượt gồm kiểm | Thời gian |
|---|---|---|---|---|---|---|
| Gemini `gemini-nano-banana-2.1` Batch 2K (ra 2752×1536) | 12 | $0,420 | **$0,035** | ≈ $0,052 + $0,133 + $0,034 | **≈ $0,25** | chờ Batch 134–209 s (5 job; tài liệu: mục tiêu ≤ 24 h) |
| OpenAI `gpt-image-2.5-sunburst-2026-09-08` edits 2560×1440 high | 12 (+ 2 lỗi 400 `input_fidelity`, $0) | $0,914 | **$0,076** | như trên | **≈ $0,30** | 33,6–38,5 s/ảnh |
C2PA: 24/24 ảnh có manifest `trainedAlgorithmicMedia`; Gemini thêm chuỗi SynthID trong tệp (12/12) + tài liệu "All generated images include a SynthID watermark".
Lưu ý: ảnh Gemini 2752×1536 (1,792:1) ≠ 16:9 — ghép co dọc 0,7 % (Lanczos); ghi để K xét khi đo (i)/(iii).

**Tài liệu Gemini đã đọc (23/10/2026; bản sao + SHA ngoài git `/var/tmp/ldn/gdoc/`):**
- Trang giá `https://ai.google.dev/gemini-api/docs/pricing` — "Last updated 2026-10-22 UTC" (SHA html `5faff50c…`). Nano Banana 2.1 (`gemini-nano-banana-2.1`), trích: Batch input "$0.75 (text/image/video)"; Batch output "$15.00 (images)", "Equivalent to $0.0168 per 1K image\*," "$0.0252 per 2K image\*," "and $0.0567 per 4K image\*." Standard: "$30.00 (images)", "$0.0504 per 2K image\*". (Thật đo: $0,033–0,042/ảnh 2K vì có token vào + ra lớn hơn bảng.)
- Trang model `https://ai.google.dev/gemini-api/docs/models/gemini-nano-banana-2.1.md.txt` (SHA `1d2906d8…`): "**Gemini Nano Banana 2.1** (`gemini-nano-banana-2.1`) is the latest high-efficiency image generation and conversational editing model."; "Improved visual quality and realism across `1K`, `2K`, and `4K` output resolutions (default `1K`)"; bảng: "**[Batch API](…)** Supported"; "Latest update | October 2026".
- Trang ảnh `https://ai.google.dev/gemini-api/docs/image-generation` — "Last updated 2026-10-09 UTC": "Recommended for all new projects to use Nano Banana 2.1."; "All generated images include a SynthID watermark."
- Trang Batch `https://ai.google.dev/gemini-api/docs/batch-api` — "Last updated 2026-09-17 UTC" (SHA md `d94b57f9…`): "asynchronously at 50% of the standard cost"; "The target turnaround time is 24 hours, but in majority of cases, it is much quicker."; "inline requests … for small batches of requests (under 20MB)".
- Gọi: `POST v1beta/models/gemini-nano-banana-2.1:batchGenerateContent`, `generation_config: {responseModalities: ["IMAGE"], imageConfig: {aspectRatio: "16:9", imageSize: "2K"}}`; không có HTTP 402.


## §4. Việc 4 — TỜ SO
- Tờ so: `reports/look-t4-v2/to-so-v2.jpg` (3500 × 2926, 1,5 MB) — 8 hàng (cùng máy/giờ LOOK-T4) × cột **LOOK-T4 đã chọn (A)** · **V2 3D** · **V2 + tấm nền Gemini** · **V2 + tấm nền OpenAI** (4 khung rộng; ô AI = lượt cuối, nhãn kết quả cổng) · **Cycles** (M2-dem). Nhãn rõ, KHÔNG mù.
- Ô 1080p (JPG ≤ 2 MB): `reports/look-t4-v2/khung/<hàng>-<look-t4|v2-3d|v2-gemini|v2-openai|cycles>.jpg`; thêm: `M1-rong|M3-rong|M4-rong-p1-hep36.jpg` (đề xuất V5), `M2-dem-cycles-ban1.jpg` (Cycles lần 1), `M1-rong-v2-openai-THAMKHAO-nhaxa-lop-c.jpg` (biến thể tham khảo V4).
- Clip 8 s 640×360, máy CODINH, thời gian chạy 15:15 → 15:45 (1/9/1666): `clip/clip-M1-rong-so-8s.mp4` (0–4 s V2 3D, 4–8 s V2 + tấm nền OpenAI lượt 3; 1,2 MB) + bản đủ 8 s từng loại `clip-M1-rong-V2-3D.mp4` (1,5 MB), `clip-M1-rong-V2-tamnen-OpenAI-l3h.mp4` (0,9 MB).
- Số đo khung V2 (thước LOOK-T4 `look_do.py`): `reports/look-t4-v2/do/khung/*.json`. Bão hoà trung vị V2: ngày 0,141–0,271 (vẫn < 0,40 — L2 đã duyệt ngưỡng theo tập), đêm 0,333–0,667.

**Tự soi chất lượng chung (thẳng):**
- **Còn "đồ chơi" ở 3D V2:** nhà 1666 vẫn là khối đồng cỡ lặp lại dày đặc khi nhìn toàn cảnh (mái đã phong hoá/ám khói, tường bẩn, sương sâu hơn, nhưng nhịp khối đều + mép sắc vẫn đọc như mô hình thu nhỏ); 2026 toàn cảnh: toà văn phòng trắng/lam phẳng, không chi tiết mái/thiết bị — rõ "đồ chơi" nhất; mặt sông 1666 xanh đậm đều. M4-trung (mặt phố): khối hộp trắng.
- **Tấm nền:** chỉ thay trời/nước/đất — phần "đồ chơi" lớn nhất (mái + tường nhà) lại là lớp (a) nên được dán lại từ render; tấm nền làm khung "thật" hơn rõ ở trời/sông/đồng (xem ô OpenAI 2026) nhưng **không chữa được nhà**. Theo §14.1 (a) "vân tường/mái" thuộc lớp nền — nếu chủ dự án muốn AI sửa BỀ MẶT mái/tường nhà thường (giữ hình học), cần một quyết định luật mới + phép kiểm hình học riêng (chưa có trong phiếu vì vượt phạm vi §15 hiện hành; nêu ở §11).
- **Lửa/khói:** xem §2 — tốt hơn rõ ở đêm; khói ngày tầng cao còn dạng rèm; St Paul's bị hắt trắng đều ở 1940.
- **Công trình:** vòm St Paul's đọc rõ ở M3-trung/M4-trung (gân vòm, đèn lồng, tháp tây); ở P1 46 px — nhận ra nhưng nhỏ; Monument/Tower ngoài khung P1.


## §5. Việc 5 — ƯỚC LẠI CẢ TẬP (theo số đo; mọi số dưới là ƯỚC)
Cơ cấu bảng shot v1: 720 s; N2P 190 s (26 %, 15 shot: 6 shot đêm/lửa — H1-02, H1-08, H1-11, H1-16, H4-01, H4-06 ≈ 78 s; 9 shot ngày/qua năm ≈ 112 s); M-d 52 s (7 %). Mục tiêu chủ dự án: tấm nền 35–45 % nếu đạt + K xong (iii).

| Khoản | Số đo phiên này | Ước cả tập |
|---|---|---|
| % tấm nền khả thi | đạt cổng: 2026 ngày (1/2 công cụ, lượt 3); 1666 ngày: chỉ đạt nếu quyết V4 (tham khảo đạt); đêm/lửa: 0/6 | **luật hiện hành: ≈ 5 %** (chỉ shot hiện đại ban ngày: M01 phần ngày, H5-04 ≈ 20–30 s) · **nếu V4 duyệt: ≈ 13–16 %** (+ shot ngày 1666–1940: H1-04, H2-*, H3-*, H5-01 ≈ 70–80 s) · **35–45 % chưa có số đo ủng hộ** (cần đêm/lửa đạt + thêm shot) |
| Số tấm × lượt × $/tấm | OpenAI ≈ $0,30/lượt, Gemini ≈ $0,25/lượt (gồm kiểm); lượt tới tấm đạt: 3 (2026) | 15 shot × ≈ 2,5 trạng thái sáng ≈ 38 tấm × 3 lượt × $0,30 ≈ **$34** (OpenAI, gồm kiểm) — ảnh chỉ ≈ $9; Gemini ảnh ≈ $4 + kiểm ≈ $25 |
| Omni M-d 20 % (Q1) | (không chạy vòng này) | 144 s × $0,10/s = $14,4/lượt → 2 lượt **$28,8**, 3 lượt **$43,2** + kiểm ≈ $3–5 |
| GPU lửa (nếu chọn Cycles, V2 = b) | 10,85 s/khung (5090, spp 48) – 23,8 s (4090, spp 64) 1080p, cảnh chưa đủ chất liệu | 3–4 cận đêm ≈ 30–40 s = 720–960 khung × 11–24 s ≈ 2,2–6,4 h GPU × $0,89–1,19 ≈ **$3–8** + một vòng dựng cảnh Cycles (vân, trăng) |
| Ngân sách Gemini T4 đã duyệt ≈ $35 | Gemini vòng này $0,42 | tấm nền Gemini (nếu chọn) ≈ $4 ảnh + Omni $29–43 → **$33–47: có thể VƯỢT $35** nếu Omni cần 3 lượt; kiểm (OpenAI/Claude) tính riêng |
| Giờ máy | V2 1080p spp 4 P = 2: 7,04–7,16 s/khung | lớp A 12 312 khung × 7,1 / 2 ≈ **12,1 h** (LOOK-T4 ước 12,8 h, lệch −5 %); timelapse tấm nền thêm ≈ 0,5 h (khung đôi có/không khói) |


## §6. Việc 6 — PHIẾU
`reports/look-t4-v2/PHIEU-LOOK-V2.md`: chọn mỗi khung 1 cột + Q1–Q3; quyết V1 (công cụ tấm nền), V2 (lửa cách A mới / Cycles), V3 (khói bếp trên tấm nền), V4 (vật nhỏ lớp (a) / nhà xa ngoài hộp), V5 (P1 fov 36°), V6 (sương), V7 (mục tiêu %). Phiên này không chấm mù bằng AI, không chọn hộ.

## §7. Nguồn mới + giấy phép
- Gutenberg #48491 *Views of St. Paul's Cathedral, London* (Gilbertson) và #60008 *London and Its Environs Described* vol. 5 (Dodsley 1761) — phạm vi công cộng (Mỹ; tác phẩm trước 1929/1761); trích nguyên văn + SHA: `NGUON-CONG-TRINH.md`. Phiên P chép vào `RIGHTS.md` (dữ kiện kích thước, không dùng hình).
- Wikipedia (St Paul's, Monument, White Tower) — dữ kiện số, bậc 3 thứ cấp (CC BY-SA: chỉ dùng số, không chép văn bản vào phim).
- OSM (ODbL) relation 3374550 (Monument), way 369135772 (White Tower) — đã có trong bộ OSM của tập.
- Ảnh AI (OpenAI, Gemini) — sổ AI; chưa dùng trong phim (bản thử look).
- Không tư liệu hình mới; không nhạc/SFX/giọng.

## §8. Chi phí thật
| Khoản | Mốc theo dõi | Chặn | Thật | Ghi |
|---|---|---|---|---|
| Gemini | $5 | > $8 | **$0,42** (12 ảnh Batch) | không 402 |
| OpenAI | $3 | > $8 | **$2,80** = ảnh $0,914 + kiểm gpt-6.1-sol $1,881 (36 lần) | sát mốc (−6,8 %) |
| Claude API | $3 | > $15 | **$6,02** = kiểm claude-sonnet-5-5 $4,80 (36 lần) + `q_thoi_dai.py` $1,22 (36 khung) | **vượt mốc theo dõi** — lợi ích: cổng (i)/(ii)/(iv) bắt buộc §15 c cần mô hình nhìn thứ hai; 36 lượt kiểm (24 tấm + 4 ghép lại + 4 l3h + 4 tham khảo) |
| RunPod | $4 | > $10 | **$0,053** (số dư $21,138 → $21,085; 2 pod, 74 s + 117 s) | |
| ElevenLabs / YouTube | 0 | — | 0 / 0 | |
| Giờ máy container | 12 h | — | **≈ 2,4 h** (16:50 → ≈ 19:10 UTC) | |
| **Tổng tiền API/GPU** | | | **≈ $9,29** | |
Chi phí mô hình của chính phiên Claude Code không có trong bảng.

## §9. Sự cố
| # | Sự cố | Xử lý | Kết quả |
|---|---|---|---|
| 1 | Container mới: `/var/tmp` trống (OSM, LiDAR, tư liệu, vân, atlas lửa) | tải lại bằng lệnh có sẵn; atlas 138 s | đủ; `tai_tu_lieu.py` ghi đè `licenses/SHA256-TU-LIEU.txt` → khôi phục bằng git (không sửa tệp ngoài vùng) |
| 2 | OSM sống đổi → hình học look v2 dựng lại khác SHA LOOK-T4 (`40f8f1aa…` ≠ `fef45294…`; lô +53, toà +1) | tờ so dùng ảnh LOOK-T4 trong git cho cột "đã chọn"; V2 dựng trên bản mới | ghi |
| 3 | Mặt nạ mã công trình đọc sai (mã năm qua ánh xạ tông) và **mọi màu mặt nạ ghi qua `s2l` bị lệch** (đầu ra sau colorspace_fragment không mã hoá lại — lỗi có từ `look.js`: đất 'bang' bị đọc thành 'suon' ở LOOK-T4, không đổi kết luận vì cùng nhóm đất) | bảng màu cách 20 mức + ghi màu thẳng trong `look2.js` | mặt nạ đúng bảng |
| 4 | Chú thích `#` chèn giữa dòng nuốt lệnh `M = …` trong `tam_nen_v2.py` (**lặp BAI-HOC #42/#76**) | thấy khi đọc lại, sửa trước lần chạy thật | 0 lượt hỏng |
| 5 | RTX 5090 hết máy (HTTP 500) | đổi RTX 4090 SECURE | ổn |
| 6 | OpenAI `input_fidelity` không hỗ trợ với model ghim (HTTP 400 ×2, $0) | bỏ tham số | — |
| 7 | **Chạy chồng > P = 2** vài giây (chuỗi 4 khởi động khi chuỗi 3 đang dựng) | dừng theo PGID ngay, xếp lại sau chuỗi 3 | không mất dữ liệu |
| 8 | **Lỗi đường ống của phiên:** ảnh vào 1666 còn khói bếp (vật chuyển động) → AI vẽ khói lên tấm tĩnh → (iv) trượt | ảnh vào không khói bếp (`chim=false`) | sửa từ lượt 3 |
| 9 | Khói bếp dán nguyên điểm ảnh render (gồm nền sương) → "đốm trắng" trên tấm; (v) 3,3–11,9 × đối chứng | cộng HIỆU có/không khói (V3) | (v) 1,00 × |
| 10 | **Lỗi 3D có từ look v1:** khói bếp không áp sương → đốm sáng ở chân trời xa | mờ dần 1,5–3 km trong `look2.js`; dựng lại 4 khung 1666 + 2 timelapse | — |
| 11 | Sau 8–10, (iv) 1666 vẫn trượt: quầng vùng bảo vệ quanh nhà xa 1–2 px (luật nở 3 px) | chẩn đoán bằng ảnh tách lớp; biến thể tham khảo (V4) | tham khảo đạt (i)–(v) |
| 12 | Thước đo bề ngang gộp điểm lẻ cách xa (Monument 12 px → thật 7 px) | bỏ cụm < 5 px | số đã sửa ở §1 |
| 13 | Lệnh lượt 2 có từ "tracks, paths" trong câu CẤM (gần tên vật lớp (a) — §15 b) | bỏ ở lượt 3 | ghi |
| 14 | Ảnh Gemini 2752×1536 ≠ 16:9 | co 0,7 % khi ghép | ghi cho K |
| 15 | Sổ chi phí đổi liên tục khi kiểm chạy nền → nhắc commit liên tục | tự commit 2 phút/lần qua preflight; sau đó sổ kiểm ghi tạm `/var/tmp`, gộp (bỏ trùng) vào `cost.jsonl` ở mốc cuối | đủ dòng |
Không force-push, không amend. Không lỗi nào lặp ≥ 3 lần trong cùng một cách.

## §10. Chỉ số trong ±5 % quanh ngưỡng
| Chỉ số | Giá trị | Ngưỡng | Lệch |
|---|---|---|---|
| Trời + sương P1 (M1-rong, M3-rong, M4-rong, M2-ngay) | 20,0 / 20,0 / 19,7 / 20,3 % | ≤ 20 % (LOOK-2) | 0 … +1,5 % |
| (iii) T9b đất→nước M4-rong-oai-l3 trong hộp | 2,17 % (toàn khung 0,89 %) | ≤ 2 % | +8,5 % (ngoài ±5 %, nêu vì là tấm duy nhất đạt — đạt theo số toàn khung) |
| (iii) M1-rong-gem-l3 đất→nước trong hộp | 2,61 % | ≤ 2 % | +30 % (ngoài) |
| (v) tỷ lệ nhấp nháy sau sửa | 0,998–1,008 × | ≤ 1,5 × | xa ngưỡng |
| Tốc độ 1080p V2 so LOOK-T4 | 7,04–7,16 s | 7,28–7,75 s | −3…−9 % |
| OpenAI chi | $2,80 | mốc $3 | −6,8 % |
| Bề ngang vòm P1 fov 36° | 67 px | ≥ 60 | +12 % (ngoài) |

## §11. Quyết định đề xuất
Xem `PHIEU-LOOK-V2.md` V1–V7. Ngoài phiếu (cần chủ dự án + K, vượt phạm vi vòng này): (1) "đồ chơi" nằm chủ yếu ở NHÀ (lớp (a)); hai đường: nâng 3D (đa dạng khối/mái, LOD xa, chi tiết mái, vật liệu 2026 thật hơn) hoặc luật mới cho AI sửa BỀ MẶT nhà thường giữ hình học (§14.1 a xếp "vân tường/mái" vào lớp nền) với phép kiểm cạnh/hình học riêng; (2) K: phép (iii) T9b dùng định nghĩa "màu nước" HSV — Gemini/OpenAI đổi nước sang xám/ô-liu/nhạt bị tính là "nước→đất" dù vẫn là nước (chẩn đoán §3); (3) K: phép (i)/(iv) cho lớp sống (khói bếp cộng hiệu) và khớp màu cục bộ vòng bảo vệ vật nhỏ.

## §12. Việc chờ chủ dự án
1. Chọn cột mỗi hàng trên `to-so-v2.jpg` + Q1–Q3 (`PHIEU-LOOK-V2.md`).
2. Quyết V1–V7.
3. Phiên P: chép nguồn §7 vào `RIGHTS.md`; ghi BAI-HOC (sự cố 3, 8–11); chuyển khiếu nại (iii)/(i)/(iv) cho K qua `checks-appeal.md`; merge nhánh (phiên này không merge).

