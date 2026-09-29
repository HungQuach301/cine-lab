# NHÁP characters v1.6 — Cas (Cổng 6, gói "Cas MPFB" của W4)

Đây là **bản nháp để P soạn và chủ dự án duyệt**. W4 không sửa `bible/characters.md` hay `design/cong3/model-sheet/cas.json`. Ida giữ nguyên v1.5.
Căn cứ: quyết định chủ dự án ngày 29/09/2026, "Cas đi quy trình MPFB"; `reports/m2/cong5/w4/BAO-CAO-W4.md`, mục "Cas MPFB".

## 1. Thay đổi so với v1.4 (bảng Cas)
| Hạng mục | v1.4 | v1.6 (đề xuất) |
|---|---|---|
| Cách dựng đầu | Đầu SDF thủ tục của cast3d, mặt vẽ tay trên texture (C′), tàn nhang vẽ | **Đầu, cổ, tóc, tai, mắt, mày từ lưới người MPFB2** (tài sản lõi CC0; RIGHTS W4-MPFB-A, phạm vi mở rộng W4-MPFB-A2). Dựng trong Blender bằng `design/cong3/v2/char3d/blender/build_cas_bl.py` → `cas_bl.glb` (SHA-256 bắt đầu `82a349d2cfbac519`). Render trong three.js qua cờ `CAS_STYLE='bl'` |
| Tuổi, giới (MPFB) | — | nam (gender 1,0), 10 tuổi (age 0,169 trên thang MakeHuman), cơ 0,5, cân 0,45 |
| Cách điệu | đầu rộng 0,90 × sâu 0,98 H | **Cùng luật với Ida v1.5.** Đích = sheet × (0,735/0,78) và × (0,88/0,92), hệ số kẹp như Ida. Sọ ×1,163, sâu ×1,003, cổ ×0,70 (sheet cổ 0,26 H). 16 target chi tiết: mắt to, mũi nhỏ hếch, má phính, tai vểnh (ear-wing 0,5), đầu tròn, cằm nhỏ |
| Hệ đầu | cằm → đỉnh sọ = 1 H | Giữ: cằm → đỉnh sọ = 1 H (H_m 0,256 không đổi). Tâm nhãn cầu đặt ở z 0,26 H như Ida (0,259–0,263) → **hai đầu cùng một hệ tỷ lệ MPFB** |
| Mắt | tròng vẽ | Nhãn cầu riêng (R 0,080 H), tròng nâu có điểm sáng (clearcoat), hội tụ; tâm mắt y 0,493 H (Ida 0,508) |
| Tai | elip, vểnh 38° | Tai liền lưới MPFB, vểnh bằng target ear-wing 0,5 |
| Tóc | #5a4034, lộ ở gáy và dưới vành mũ | Giữ màu #5a4034. Vỏ tóc ngắn + 170 chùm ngắn thò dưới gấu mũ + 120 sợi tơ. Tóc nằm trong mũ len, không xuyên len |
| Mũ len có quả bông | chóp elip rộng 0,4995 × sâu 0,5341 H ở y 0,69 | **Giữ nguyên hình, màu, quả bông.** Chỉ đo lại miệng mũ theo đầu + tóc glb: rx 0,454, rz 0,475 H, tâm z −0,075 (`meta.cap`; chỉ khi `CAS_STYLE='bl'`) |
| Da | tô vẽ | Màu đỉnh #e2bfa2: loang, má và mũi ửng lạnh, **tàn nhang** trên sống mũi và gò má. Độ nhám thay đổi theo vùng (0,45–0,85). Không nếp tuổi |
| Rig | nét vẽ theo EXPR | 16 kênh `CHANNELS` + 6 `vis_*` + 4 preset, cùng tên và cùng định nghĩa kênh với Ida v1.5 (kể cả `corr_mouth`, `corr_smile_lip`) |
| Thân, áo, quần, ủng, tay | — | Không đổi |

## 2. c3_views Cas 'bl' (8 góc, cùng cách B1/C3: mặt nạ nhìn thấy 4×, turnaround, trực giao, trục chính PCA + 1 px)
Số thô: `reports/m2/cong5/w4/CAS_c3_bl.json`.

| Bộ phận | 0° | 45° | −45° | 90° | −90° | 135° | −135° | 180° |
|---|---|---|---|---|---|---|---|---|
| thân (v1.6 đề xuất) | **1,379** | 1,711 | 1,715 | 1,724 | 1,732 | 1,811 | 1,821 | 1,370 |
| thân (v1.4) | 1,669 | 1,707 | 1,708 | 1,661 | 1,654 | 1,708 | 1,704 | 1,656 |
| lệch thân | **−17,4 %** | +0,2 % | +0,4 % | +3,8 % | +4,7 % | **+6,0 %** | **+6,9 %** | **−17,3 %** |
| cẳng tay | 0,781 | 0,946 | 0,933 | —¹ | 0,981 | 0,999 | 0,996 | 0,781 |
| đùi | 0,984 | 1,179 | 1,163 | — | 1,126 | 1,102 | 1,271 | 0,895 |
| cẳng chân | 0,935 | 1,119 | 1,119 | — | 1,187 | 1,195 | 1,199 | 0,914 |
| cánh tay trên (bỏ) | 0,484 | 0,298 | 0,612 | — | 0,662 | 0,612 | 0,678 | 0,521 |
| đầu nhìn thấy (px, 4×) | 782 | 654 | 653 | 620 | 616 | 607 | 603 | 782 |

¹ Đo được 0,052, là mẩu cổ tay ló sau thân; ghi null như v1.4.

**Giới hạn phải ghi (quan trọng cho luật C3):**
- Ở 0° và 180°, phần đầu nhìn thấy dưới mũ len **rộng hơn cao**: rộng 782 px, cao 481 px ở 0°, vì tai vểnh nhìn thấy trọn và mũ che phần trên đầu.
- Khi đó trục chính PCA lật sang **ngang**, nên "độ dài đầu" ở hai góc này là bề ngang qua hai tai. Tỷ lệ 1,379 / 1,370 vì vậy **không cùng nghĩa** với 1,669 của v1.4.
- Nếu đo theo bề **dọc** của mặt nạ, tỷ lệ thân/đầu là 2,229 (0°), 2,704 (180°), 2,224 (45°), 2,224 (90°).
- Cần P/K quyết C3 cho Cas 0°/180° dùng cách nào. Đây là giới hạn của phép đo PCA 2D (RULES giới hạn 4), không phải lỗi lưới.
- **Chỉ số trong ±5 % quanh ngưỡng 3 %:** 45°, −45°, 90° (+3,8 %), −90° (+4,7 %). Lệch quá 5 %: 0°, 180°, ±135°.

## 3. Cách đồng bộ tỷ lệ đầu–thân với Ida v1.5
- Cả hai đầu: lưới MPFB, **cằm → đỉnh sọ = 1 H** của từng nhân vật (Ida H_m 0,258; Cas H_m 0,256). Cùng luật cách điệu: hệ số = đích sheet × tỷ lệ đích Ida / số đo MPFB, kẹp 1,0–1,2 ngang, 1,0–1,15 sâu. Cùng mốc tâm mắt z 0,26 H.
- Cao tuyệt đối không đổi. Ở khung hai người (`CAS_K3_hai-nguoi.jpg`, `CAS_K4_hai-nguoi.jpg`), đầu hai nhân vật cùng kiểu dựng và cùng mức cách điệu. Đầu Cas trẻ con nên to so với thân (tổng cao 5,0 H so với Ida 6,27 H, theo sheet).

## 4. Việc cần duyệt
1. Chủ dự án duyệt hình Cas MPFB (ảnh `CAS_eevee_4goc.jpg`, 4 khung `CAS_K*.jpg`), sau kiểm mù của P.
2. P/K quyết cách đo C3 0°/180° cho Cas (mục 2).
3. Nếu duyệt: đặt `CAS_STYLE='bl'` làm mặc định, khoá cas.json v1.6 (c3_views + `face`/`cap`), ghi AUTHORSHIP.

## 5. Cổ áo len lật cao (P soạn theo quyết định chủ dự án "Cas A+", 29/09/2026). CHƯA DUYỆT
| Hạng mục | v1.4 | v1.6 (đề xuất) |
|---|---|---|
| Cổ áo len | cổ tròn rộng, hở, lộ cổ 0,22 H | **cổ lật cao (turtleneck):** ống cổ cao **0,20 H** tính từ chân cổ, che gần hết phần cổ lộ (0,22 H); mép trên cách cằm khoảng 0,02–0,04 H ở tư thế đứng thẳng. Phần **lật gập xuống 0,09 H**. Đường kính ngoài khoảng **0,40 H** (cổ 0,26 H + len dày khoảng 0,07 H mỗi bên); ôm vừa, không bó. Cùng màu, cùng vân len với thân áo; nếp gấp mềm ở mép lật |
| Số đo cổ (sheet) | length 0,22, width_front 0,26 H | Giữ khung xương; phần cổ nhìn thấy còn khoảng 0,02–0,04 H. Mặt nạ C3 "đầu" không đổi cách đo (đầu = phần nhìn thấy dưới mũ, trên cổ áo) |
| Lý do | lời chê kiểm mù "cổ như cái que", "cổ cò" (2/2 khung Cas) | Chủ dự án đổi thiết kế; đề xuất của Claude (rà độc lập bên ngoài) |

## 6. Thân MPFB, tay theo tỷ lệ MPFB (W4T lượt 1 + 2 + 3, 29/09/2026). CHƯA DUYỆT — P soạn
Quyết định chủ dự án (AUTHORSHIP "Cổng 6 — nhân vật", 29/09/2026): **tay Cas rút về tỷ lệ MPFB**; sửa thân một lượt sau kiểm mù lượt 1.

| Hạng mục | v1.4 (sheet) | v1.6 (đề xuất) |
|---|---|---|
| Tay trên (độ dài KHỚP cast3d) | 0,92 H | **0,7643 H** (19,6 cm): phần nhìn thấy 0,6849 H (17,5 cm) + (1 − LIFT)·khe vai (khớp vai cast3d cao hơn khớp giải phẫu) |
| Cẳng tay | 0,82 H | **0,7009 H** (17,9 cm) |
| Nguồn số | sheet | xương MPFB nam 10 tuổi (upperarm01→lowerarm01, lowerarm01→wrist) × (chiều cao sheet 5,0 H = 1,28 m / chiều cao MPFB 1,289 m = 0,9931) |
| Tầm với khi duỗi thẳng (vai → cổ tay) | 1,74 H | 1,465 H (ngắn hơn 15,8 %) |
| Gấu áo len | 2,25 H từ đất, bo ôm hông | **2,17 H** (lượt 3; lượt 2 là 2,10 H), buông, loe nhẹ; phủ qua cạp quần (đáy đũng 0,517 m, gấu 0,556 m); không hở ở s42a và s25 (giơ tay cao nhất) |
| Áo len | lệch 1,1 cm (bụng +1,2) | lệch 1,6 cm (bụng +1,2), tay áo 1,2 cm; ngực và lưng phủ trơn (không in cơ ngực, núm, rãnh sống lưng, khe mông) |
| Quần | vỏ bám chân (lệch 1,0 cm) | **ống thẳng, rộng**: bán kính tối thiểu 5,1 cm quanh trục chân (lượt 3; lượt 2 là 4,6 cm) (sâu 0,92), nếp gối, rủ dọc, nếp chùng trên gấu; đũng làm mượt (không lộ háng); gấu thẳng cách mắt cá 0,25 H |
| Măng sét | 0,07 H, bán kính miệng tay áo + 0,3 cm | 0,09 H, + 0,9 cm (trùm hết cuống cổ tay MPFB) |
| Cổ lật cao, sau gáy | dâng 0,055 H | dâng 0,085 H, nới sau gáy 0,03 H (thu dần về chân cổ): da gáy không xuyên cổ áo |
| Tay nắm quai đèn lồng (s41, s42a; layout, chỉ khi tay 'bl') | treo đèn giữa hai cổ tay | hai tay nắm hai điểm chéo trên vòng quai (IK `reachGrip`, ngón gập quanh ống quai) |
| Da tay MPFB ('bl', Ida và Cas) | — | cuộn sáng mềm (ngưỡng 0,4, trần 0,8); màu da tay Cas #cf9878 (lượt 1 #e2bfa2). Da tay Ida chỉ đổi cuộn sáng, màu giữ #d8b49a |

### c3_views Cas v1.6 — `"c3_head_axis": "doc"` (đo W4T lượt 3: `c3_w4t.py`, trang `page_turn_w4t.js`, mặt nạ nhìn thấy 4×, turnaround, trực giao)
| Góc | thân | tay trên | cẳng tay | đùi | cẳng chân | đầu doc (px, 4×) |
|---|---|---|---|---|---|---|
| 0° | 2,618 | 1,564 | 1,051 | 1,604 | 1,464 | 487,0 |
| 45° | 2,706 | 1,608 | 1,047 | 1,697 | 1,443 | 478,7 |
| -45° | 2,700 | 1,548 | 1,087 | 1,620 | 1,604 | 479,6 |
| 90° | 2,723 | — | — | 1,633 | 1,384 | 474,2 |
| -90° | 2,725 | 1,540 | 1,114 | 1,688 | 1,620 | 474,1 |
| 135° | 2,803 | 1,554 | 1,132 | 1,672 | 1,599 | 467,8 |
| -135° | 2,871 | 1,636 | 1,162 | 1,651 | 1,654 | 457,1 |
| 180° | 3,886 | 2,280 | 1,634 | 2,376 | 2,278 | 328,3 |

Số thô: `reports/m2/cong6/w4t3/W4T3_c3_cas_doc.json`. Khi khoá: `c3_views` = bảng trên (head 1,0), `measured_parts` = thân, tay trên, cẳng tay, đùi, cẳng chân; độ dài cấp gốc = góc 0°.
```json
{"0\u00b0": {"head": 1.0, "torso": 2.618, "upper_arm": 1.564, "forearm": 1.051, "thigh": 1.604, "shin": 1.464}, "45\u00b0": {"head": 1.0, "torso": 2.706, "upper_arm": 1.608, "forearm": 1.047, "thigh": 1.697, "shin": 1.443}, "-45\u00b0": {"head": 1.0, "torso": 2.7, "upper_arm": 1.548, "forearm": 1.087, "thigh": 1.62, "shin": 1.604}, "90\u00b0": {"head": 1.0, "torso": 2.723, "upper_arm": null, "forearm": null, "thigh": 1.633, "shin": 1.384}, "-90\u00b0": {"head": 1.0, "torso": 2.725, "upper_arm": 1.54, "forearm": 1.114, "thigh": 1.688, "shin": 1.62}, "135\u00b0": {"head": 1.0, "torso": 2.803, "upper_arm": 1.554, "forearm": 1.132, "thigh": 1.672, "shin": 1.599}, "-135\u00b0": {"head": 1.0, "torso": 2.871, "upper_arm": 1.636, "forearm": 1.162, "thigh": 1.651, "shin": 1.654}, "180\u00b0": {"head": 1.0, "torso": 3.886, "upper_arm": 2.28, "forearm": 1.634, "thigh": 2.376, "shin": 2.278}}
```
