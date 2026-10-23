Nhánh thật: `k2c-t4-02-look2` (gốc `origin/k2c-t4-02-look` @5123bebf). Nhánh mặc định của bộ khung (`claude/practical-mendel-u8qqn3`) KHÔNG dùng (lệnh gọi tên nhánh). SHA cuối = đỉnh nhánh (commit "… — DỪNG chờ chủ dự án").

# BÁO CÁO LOOK-T4-V2 — vòng look thứ hai T4 London (K2C-T4-02) · 23/10/2026

Căn cứ: chủ dự án chấm tờ LOOK-T4 (23:14) + nhận xét 23:41 — "1. Thành phố vẫn còn trông như “đồ chơi” 2. Khói và lửa cần rõ hơn 3. Các công trình biểu tượng chưa được rõ nét"; look hợp nhất 23:27 (A chuẩn + cháy ngày 1666/1940 ấm kiểu C + đêm cháy 1666 khói than dày kiểu B); L2–L6 theo khuyến nghị; lệnh 23:45 "1,2,3,4,5, đồng ý theo khuyến nghị".

## Tóm tắt (đọc trước)
- **Công trình (việc 1):** St Paul's, Monument, White Tower dựng lại chi tiết cao theo kích thước có nguồn PD (Gilbertson qua Gutenberg #48491; *London and Its Environs* 1761 qua Gutenberg #60008) + OSM. **Sửa lỗi vị trí Monument của look v1 (lệch ≈ 68 m).** Đo ở P1 1080p: vòm **46 px** (khung P1 fov 50°) — **TRƯỢT ngưỡng ≥ 60 px**; đạt **67 px** nếu P1 dùng fov 36° (cùng vị trí/hướng). **Monument và Tower nằm NGOÀI khung P1** (phương vị 49° và 77°, mép phải khung 46,7°) — đo từ vị trí P1 quay máy về từng công trình: Tower 49 px (đạt ≥ 12), **Monument 7 px (fov 50°) / 10 px (fov 36°) — TRƯỢT ≥ 12 px** vì thân cột bị khối văn phòng 2026 che, chỉ còn nón + bầu lửa ló lên. 3 chi tiết: đèn lồng vòm ĐỌC ĐƯỢC (14 px rộng ở P1), bầu lửa vàng Monument ĐỌC ĐƯỢC (4 px, sáng vàng trên nền xám), tháp góc White Tower MỜ (≈ 6 px/tháp, mũ chì tối khó đọc).
- **Lửa + khói (việc 2):** cách A mới có lõi lửa, quầng sáng, tàn lửa theo gió đông, chân khói hắt đỏ theo độ cao, khói ngày đặc/tối/tách tầng, ánh lửa mặt tiền + mặt sông mạnh hơn. 1 khung Cycles GPU cùng máy/giờ (2 lần chạy, tổng **$0,053** theo số dư RunPod). Tự soi: lửa/khói rõ hơn LOOK-T4 thấy được; khói ngày tầng cao vẫn dạng "rèm"; khung Cycles có khói thể tích phát sáng thật hơn nhưng cảnh Cycles chưa có vân/ánh trăng.
- **Tấm nền AI (việc 3):** 24 tấm (4 khung × 2 công cụ × 3 lượt) + 4 lần ghép lại không gọi AI. **Đạt cổng máy (i)–(v): 1 tấm** — 2026 toàn cảnh, OpenAI lượt 3. Các khung 1666 ngày: sau khi sửa 3 lỗi đường ống/3D của chính phiên này (khói bếp trong ảnh vào; dán khói bếp nguyên nền; khói bếp xa không áp sương) — kết quả §3. Đêm 1940: 0/6 (AI tự thêm cầu, đèn, thuyền). Gemini 0/12: đổi sắc nước (T9b nước→đất 19–69 %).
- **Ước lại (việc 5):** tấm nền khả thi theo số đo ≈ **5–15 % thời lượng** (không phải 35–45 %) cho tới khi K xong phép (iii) và có quyết định V3–V4 ở phiếu. Ngân sách Gemini T4 ≈ $35: tấm nền chỉ ≈ $2–6; phần lớn là Omni M-d ($29–43 + kiểm) → **có thể vượt $35** nếu Omni cần 3 lượt.
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


<!--TAM-NEN-->

<!--TO-SO-->

<!--UOC-->

<!--CUOI-->
