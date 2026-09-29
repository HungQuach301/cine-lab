# Cổng 6 — gói W4T: thân Cas "cách A" (MPFB CC0), cổ tay MPFB, mũ len; đo C3

- Worktree W4 (phiên mới), đã gộp nhánh tích hợp `claude/cine-lab-m2-cong5-layout-24o5fp` @3858cec (có checks v1.5 và `exportSil`).
- Chạy 29/09/2026, 03:20 → 04:15 UTC.
- MPFB2 @3edf9df0, đặt ngoài repo (scratchpad). **RIGHTS W4-MPFB-A4 ghi và commit TRƯỚC khi dùng** (98a3fc5).
- **Không tự chạy kiểm mù.** Không sửa checks/ (không đọc mã checks/), bible/, ida.json, cas.json, facelight.js, file layout W1/W2, PLAN.md, AUTHORSHIP.md.

## 0. Tóm tắt
- **Bước a (khả thi): ĐẠT.** Vai, nách không xẹp; áo không xuyên thân; gập khuỷu mạnh (cầm đèn lồng) không gãy ống tay. Ảnh `W4T_kha-thi.jpg`.
- **Bước b: làm được một phần, DỪNG vì hạn token** (tổng khoảng 350 nghìn; phần đọc tài liệu đầu gói đã ăn khoảng 125 nghìn).
  - Đã làm: thân + áo len + quần + da ống chân MPFB; măng sét len; **sửa mối nối cổ tay MPFB cho cả Ida và Cas**; **sửa khe đen đỉnh mũ len Cas**; đo C3.
  - Chưa làm: gai mảnh ở gáy Cas (nhìn sau lưng); áo len còn hơi ôm sát, ngực còn gợn nhẹ khi nhìn chính diện (mục 5).
- **Ảnh EEVEE 4 góc và khung three.js dùng được** (tự xem, không phải kiểm mù) → nộp đủ khung cho kiểm mù (mục 4).
- **Cờ mới `CAS_BODY` (mặc định `'v14'`).** Dò layout mặc định s02, s24c, s37, s42 trước/sau: **12 thumbs, lệch 0 px**.
- C3: Cas theo **'doc'**, Ida v1.5.1 theo **'pca'** (mục 3). Công cụ đo của tôi tái lập **đúng từng số** của K trên cùng bộ mặt nạ.

## 1. Cách bật cờ
| Cờ | Mặc định | Bật |
|---|---|---|
| **`CAS_BODY`** (mới) | `'v14'` (thân cũ) | `buildCharacter(cas, { casStyle: 'bl', casBody: 'bl' })` hoặc `globalThis.CINE_CAS_BODY='bl'`; phải `await preloadCasBodyBL()` trước. **Chỉ có hiệu lực khi Cas 'bl'.** `page.js` +1 dòng nạp khi cờ bật (không đụng `exportSil`). Trang thử: `"casBody":"bl"` trong `--args` của `page_l2.js` |
| `HANDS_STYLE` | `'v14'` | như cũ (`handsStyle:'bl'`). Cổ tay đã sửa nằm trong `hands_bl.json` và lót măng sét Ida (chỉ khi tay 'bl') |
| Khung dùng trong gói | — | `casStyle:'bl'`, `casBody:'bl'`, `handsStyle:'bl'`, `idaStyle:'bl'` (v1.5.1) |

Thân mới không có lưới đạo cụ gắn vào cây nhân vật, nên không cần `userData.prop` (theo lưu ý của P về `exportSil`).

## 2. Việc đã làm và bằng chứng

### a. Khả thi (`W4T_kha-thi.jpg`: EEVEE, trái 3 ảnh đứng thẳng tư thế sheet `turnaround`, phải 3 ảnh tư thế layout s42a 114,5 s cầm đèn lồng; 0°/90°/180°)
- `blender/build_cas_body_bl.py` (Blender không giao diện, khoảng 1,5 s):
  1. Người MPFB như đầu 'bl' và tay (nam 10 tuổi); rig `default` **chỉ để lấy trọng số**.
  2. **Uốn hình về khung cast3d theo sheet Cas** (giữ hệ tỷ lệ v1.6, đầu 'bl'): mỗi đoạn (thân, cánh tay trên, cẳng tay, đùi, cẳng chân) có phép biến đổi riêng: gốc đoạn MPFB → khớp cast3d, dài theo sheet, vòng theo hệ số; trộn theo trọng số MPFB nên mượt qua khớp. Thân: ngang ×0,871, dọc ×0,909, sâu ×0,92.
  3. **Khớp vai:** khớp vai giải phẫu MPFB thấp hơn tâm quay vai cast3d 4,1 cm. Nâng phần vai bên một nửa (LIFT 0,5), nửa còn lại để tâm quay cao hơn khớp 2 cm. Đây là điểm cân bằng giữa "vai vuông" và vai xẹp khi quay.
  4. **Trọng số cast3d** = gộp 163 xương MPFB → 16 khớp cast3d (đòn → thân; vai MPFB 0,35 thân + 0,65 vai; spine05/04 chia chậu/thân). Tay áo: trọng số wrist dồn về khuỷu (vải không xoắn theo cổ tay).
  5. **Tư thế bind** = vai dạng 24°, khuỷu gập 20° (gần tư thế hay dùng, ít biến dạng LBS). three.js ghi bind ở đúng tư thế này bằng một `CpuSkin` riêng (`blender/body_bl.js`), cập nhật cùng `skin.update()`. **Rig, `applyPose`, tư thế layout không đổi.**
  6. Áo len, quần: **vỏ tự dựng** từ lưới thân đã uốn: lệch theo pháp tuyến (áo 1,1 cm, chùng thêm 1,2 cm ở bụng, bo gấu ôm; tay áo 1,0 cm; quần 1,0 cm); làm mượt Taubin 70 lượt (bỏ chi tiết cơ thể); nếp vải thủ tục (khuỷu, cổ tay, gấu, rủ dọc); mép gấu, ống tay, gấu quần cắt phẳng; chia Catmull-Clark 1 cấp; UV quanh trục (nhân đôi đỉnh ở đường nối); AO theo nếp. Da ống chân lấy thẳng từ lưới thân.
  7. Tách lưới theo bộ phận C3 và **theo bên L/R**: `torso`, `upper_arm`, `forearm`, `thigh`, `shin_trouser`, `shin`, `trouser_seat`. Pháp tuyến dùng chung nên không lộ đường nối.
- Giữ nguyên: đầu 'bl', cổ lật cao (ống 0,20 H, lật 0,09 H, Ø ngoài 0,40 H theo nháp v1.6), mũ, ủng cast3d, tay MPFB.

### b. Làm đủ (bằng chứng: `W4T_truoc-sau_than.jpg`, `W4T_cas_eevee_4goc.jpg`, 3 khung nộp)
| Lời chê | Đã làm | Tự xem |
|---|---|---|
| "áo phồng như bóng bay / cái ống" | Áo theo khối thân MPFB: ngực, lưng, eo, gấu ôm hông | Hết khối trụ tròn. Thân đọc thành thân trẻ 10 tuổi mặc áo len |
| "tay áo như ống" | Tay áo theo cơ tay trên, cẳng tay, nếp khuỷu và nếp chùng cổ tay | Hết ống đều; khuỷu gập giữ khối |
| "vai vuông cứng" | Dốc vai theo MPFB (thang, cơ delta), vai liền tay áo | Vai dốc, tròn |
| "hai phong cách không ăn nhập" | Thân Cas cùng nguồn MPFB với đầu và tay | Cần kiểm mù xác nhận |
| Quần, giày | Quần vỏ từ chân MPFB, gấu cách mắt cá 0,25 H (sheet); ủng cast3d giữ | Quần ống đứng, không còn "quần lót" dưới gấu áo |
| **Cổ tay MPFB (Ida + Cas)**: "mảng đen lởm chởm", "tay vụn vỡ" | (1) `build_hands_bl.py`: cắt cổ tay bằng **mặt phẳng** vuông trục cẳng tay (3 cm sau khớp), thay ngưỡng trọng số (mép răng cưa); **bịt miệng ống** bằng nắp da lõm nhẹ. (2) Cas: **măng sét len** ôm miệng tay áo, gắn khuỷu, lót khép vào trong. (3) Ida: lót măng sét khép về cổ tay (chỉ khi tay 'bl') | `W4T_truoc-sau_co-tay.jpg`: Ida hết mảng đen trong măng sét; Cas cổ tay liền |
| **Khe đen trên đỉnh mũ len Cas** | Nguyên nhân: trường khoảng cách nối dài phía trên mép lưới SDF không phải khoảng cách thật, nên bước dò tia vượt vỏ và trúng mặt trong. Sửa: dò tia bước ngắn (×0,35); thêm lưới an toàn (bán kính tia thấp hơn trung vị 5×5 lân cận quá 0,012 H thì kéo về trung vị) | `W4T_truoc-sau_mu-len.jpg`: vòm liền. Làm lại 2 lần: lần hạ YT làm khe to hơn nên đã trả lại |
| Gai mảnh ở gáy Cas (nhìn sau lưng) | **Chưa sửa** (hết hạn) | Vẫn thấy ở 180° (`W4T_cas_eevee_4goc.jpg`) |

### c. Thân Ida: không sửa. Ghi nhận
Tay Ida dài, áo dạ đọc được. Mặt trong măng sét trước đây tối hẳn; nay đã có lót. Không thấy áo Ida thô ở cỡ khung s42a.

## 3. Đo C3 (không sửa ida.json hay cas.json)
- **Cách đo:** `blender/c3_w4t.py`, cùng cách `c3_cas.py`/`c3_bl.py` (mặt nạ nhìn thấy 4×, turnaround, trực giao). Tính cả hai cách đo đầu theo RUN.md 3.6.1:
  - `'pca'`: trục chính + 1 px;
  - `'doc'`: chiếu lên trục từ tâm mặt nạ thân tới tâm mặt nạ đầu + 1 px.
  - Bộ phận khác luôn theo PCA.
- **Đối chiếu công cụ K:** chạy lại `--masks` trên bộ mặt nạ Cas cũ (gói Cas MPFB). Ra **đúng từng số** của `reports/checks-v1.5/dryrun/k_cas_doc.json`: đầu doc 481,3 / 479,0 / 479,5 / 507,8 / 507,3 / 507,7 / 503,3 / 395,0 px; thân 2,241 / 2,334 / 2,336 / 2,105 / 2,102 / 2,165 / 2,180 / 2,713.
- Ida theo 'pca' khớp số cấp gốc/`c3_views` của K và của ida.json (±0,1 %).
- Số thô: `W4T_c3_cas_doc.json`, `W4T_c3_ida_v151_pca.json` (có cả `pca`, `doc`, px).

**Cas v1.6 thân mới, khai `"c3_head_axis": "doc"`** (trang `page_turn_w4t.js`: Cas 'bl' + thân 'bl' + tay 'bl'; làn nặng 142 s)

| Góc | thân | tay trên | cẳng tay | đùi | cẳng chân | đầu doc (px, 4×) | thân so với K (thân cũ, doc) |
|---|---|---|---|---|---|---|---|
| 0° | **2,406** | 1,725 | 1,242 | 1,804 | 1,544 | 487,0 | +7,4 % |
| 45° | 2,477 | 1,753 | 1,219 | 1,853 | 1,477 | 478,8 | +6,1 % |
| −45° | 2,472 | 1,735 | 1,272 | 1,773 | 1,594 | 479,7 | +5,8 % |
| 90° | 2,508 | null¹ | null¹ | 1,407 | 1,273 | 470,1 | +19,1 % |
| −90° | 2,507 | 1,723 | 1,323 | 1,805 | 1,633 | 470,0 | +19,3 % |
| 135° | 2,385 | 1,655 | 1,126 | 1,704 | 1,494 | 501,3 | +10,2 % |
| −135° | 2,393 | 1,648 | 1,263 | 1,676 | 1,519 | 500,3 | +9,8 % |
| 180° | 3,116 | 2,281 | 1,720 | 2,351 | 2,022 | 370,5 | +14,9 % |

¹ Tay trái khuất sau thân ở 90°: mặt nạ rỗng, ghi null như v1.4.

- **Đọc số:** thân mới dài hơn trong mặt nạ vì áo liền vai (vai, delta thuộc `torso` tới chỗ trọng số vai trội), còn cổ lật cao che phần dưới đầu. Tay trên nay **lộ rõ** ở 0° (1,725; trước 0,787 vì tay áo cũ khuất trong khối thân). Ở 180°, đầu doc chỉ 370,5 px vì cổ lật che gáy.
- **P phải lấy bảng này làm `c3_views` Cas v1.6** (cùng `measured_parts` và độ dài cấp gốc = góc 0°) nếu duyệt thân mới. Số của K (thân cũ) không còn dùng được.
- **Chỉ số trong ±5 % quanh ngưỡng:** không áp dụng được cho Cas, vì bảng này chính là số khai mới (lệch so với chính nó = 0). Không có số nào tôi tự so với ngưỡng 3 %.

**Ida v1.5.1 (mũ y 0,775, `ida_bl_v151.glb`), 'pca'** (trang `page_c3_bl.js`, làn nặng 127 s)

| Góc | thân | tay trên | cẳng tay | cẳng chân | đầu PCA (px) | ida.json thân | lệch |
|---|---|---|---|---|---|---|---|
| 0° | 2,271 | 1,337 | 0,831 | 0,245 | 529,2 | 2,272 | −0,0 % |
| 45° | 2,220 | 1,429 | 0,883 | 0,274 | 497,4 | 2,219 | +0,0 % |
| −45° | 2,213 | 1,424 | 1,255 | 0,274 | 497,4 | 2,216 | −0,1 % |
| 90° | 2,035 | — | — | — | 509,4 | 2,033 | +0,1 % |
| −90° | 2,070 | 1,404 | 1,005 | 0,273 | 509,5 | 2,069 | +0,0 % |
| 135° | 2,383 | 1,483 | 0,836 | 0,276 | 484,6 | 2,381 | +0,1 % |
| −135° | 2,350 | 1,472 | 1,100 | 0,274 | 484,7 | 2,353 | −0,1 % |
| 180° | 2,130 | 1,357 | 1,026 | 0,244 | 529,0 | 2,130 | +0,0 % |

- Mũ hạ 0,025 H **không đổi** độ dài đầu nhìn thấy ở turnaround trong phạm vi ±0,1 %. Ida có thể khoá v1.5.1 với `c3_views` hiện có ('pca').
- Không số nào nằm gần biên ±3 %.

## 4. Khung nộp cho kiểm mù (`reports/m2/cong6/w4t/`, 1920×1080, 3 mẫu, làn nặng, layout thật, Ida 'bl' v1.5.1 + Cas thân mới + tay MPFB)
| Tệp | Shot | Giây | Ghi chú |
|---|---|---|---|
| `W4T_hai-nguoi_s42a.jpg` | s42a (MS) | 114,5 | Quai đèn lồng dời vào giữa hai nắm tay (`grips` lantern của trang thử, như W4N); layout W2 chưa đổi |
| `W4T_hai-nguoi_WS.jpg` | s41 (WS) | 112,8 | Cả hai toàn thân, nhỏ trong khung |
| `W4T_cas_toan-than.jpg` | s42a | 114,5 | Cas thấy từ mũ tới ủng. **Cùng khung với tệp hai người**, vì s24c và s38 chỉ là MS. Hai khung phụ: `W4T_cas_s24c_phu.jpg` (s24c 58,2 s, MS), `W4T_cas_s38_phu.jpg` (s38 106,7 s) |
| `W4T_truoc-sau_than.jpg`, `W4T_truoc-sau_co-tay.jpg` | s42a 114,5 s | | Trái W4N, phải W4T; cùng khung |
| `W4T_truoc-sau_mu-len.jpg` | EEVEE | | Trái: trước sửa; phải: sau sửa |
| `W4T_cas_eevee_4goc.jpg` | EEVEE, tư thế `turnaround` | | 0°, 60°, 180°, −120°; đèn studio (`blender/eevee_4goc_than.py`) |
| `W4T_kha-thi.jpg` | EEVEE | | Bước a |

## 5. Rủi ro và việc chưa làm
1. **Gai mảnh ở gáy Cas** (180°) chưa sửa.
2. **Áo len hơi ôm sát:** nhìn chính diện còn gợn nhẹ ở ngực. Có thể bị đọc là "áo thun" hoặc "bó". Nếu kiểm mù chê, tăng lệch và làm mượt: chỉ cần chỉnh tham số `SW`, `SW_BELLY`, `SMOOTH` rồi dựng lại (1,5 s).
3. **Tay dài theo sheet** (tay trên 0,92 H + cẳng tay 0,82 H = 23 % dài hơn người thật MPFB). Thân mới làm tay lộ rõ hơn, nên lời "tay dài thõng" có thể tăng. Đổi sheet là **quyết định sáng tạo** của chủ dự án.
4. **Tâm quay vai cao hơn khớp giải phẫu 2 cm.** Khi giơ tay cao (ngoài các tư thế đã thử) có thể lộ nếp ở nách. Chưa thử tư thế chim bóng (`shadow_bird`) và tư thế leo thang.
5. **Tay MPFB dưới ánh đèn lồng** đọc rất sáng (trắng) ở s42a: do vật liệu và đèn, không phải hình. Chưa xử lý.
6. **Hiệu năng:** da CPU thêm khoảng 23 nghìn đỉnh cho Cas (khung 1920 3 mẫu: 15–17 s, như trước).
7. C3 Cas đổi hẳn so với số của K: xem mục 3. P cần soạn lại `c3_views` khi khoá v1.6.

## 6. Cập nhật nháp v1.6 cho thân (đề xuất, chưa duyệt)
| Hạng mục | Nháp v1.6 (W4N) | W4T |
|---|---|---|
| Thân, áo len | SDF cast3d (khối ống), tay áo ống + chỏm cầu | **Lưới thân MPFB2 CC0** (nam 10 tuổi), uốn theo khung sheet v1.4 (không đổi khớp), áo len vỏ tự dựng: lệch 1,1 cm (bụng +1,2 cm), bo gấu ôm; tay áo 1,0 cm có nếp khuỷu/cổ tay; màu `C.sweater`, vân len |
| Măng sét | tay áo trùm 0,18 H qua cổ tay, loe | Măng sét len ôm miệng tay áo, dài 0,07 H qua cổ tay, lót khép vào trong |
| Quần | ống SDF | Vỏ từ chân MPFB (lệch 1,0 cm, nếp dưới gối), gấu cách mắt cá 0,25 H (sheet), màu `C.trousers` |
| Ống chân | ống da | Da MPFB (hệ số vòng chân 0,82) |
| Ủng, cổ lật cao, mũ, đầu, tay | — | Giữ. Mũ len: sửa khe đỉnh (không đổi hình) |
| c3_views | bảng W4N ('pca') | **Bảng mục 3 ('doc')**, khai `"c3_head_axis": "doc"` |
| Tài sản | W4-MPFB-A3 | **W4-MPFB-A4** |

## 7. Tệp
- Mới:
  - `design/cong3/v2/char3d/blender/build_cas_body_bl.py`, `body_bl.js`, `cas_body_bl.json` (1,9 MB);
  - `page_turn_w4t.js`, `c3_w4t.py`, `eevee_4goc_than.py`.
- Sửa:
  - `cast3d.js`: cờ `CAS_BODY`, nhánh thân, măng sét, lót măng sét Ida khi tay 'bl', mũ len;
  - `build_hands_bl.py` + `hands_bl.json` (cổ tay; 4,1 MB, không khoá);
  - `page_l2.js`: `casBody`, `pose`;
  - `design/cong5/layout/page.js`: +1 dòng;
  - `RIGHTS.md`: W4-MPFB-A4.
- `node --check` đạt ở mọi tệp .js đã sửa.

## 8. Thời gian thật, làm lại, hàng đợi, token
| Bước | Giờ UTC | Thời gian |
|---|---|---|
| Gộp nhánh, đọc báo cáo, tài liệu, mã | 03:10 → 03:26 | khoảng 16 phút |
| RIGHTS, script thân, dò "trước", bước a | 03:26 → 03:48 | khoảng 22 phút |
| Bước b: cổ tay, mũ, áo | 03:48 → 03:57 | khoảng 9 phút |
| C3 (3 lượt làn nặng), khung nộp, dò "sau" | 03:57 → 04:10 | khoảng 13 phút |
| Báo cáo, commit | 04:10 → 04:15 | — |

- **Làm lại:**
  - dựng thân 6 lượt (UV; mép co do làm mượt → giữ mép; gấu răng cưa → bỏ điều kiện chân; tay áo dồn trọng số wrist; mượt 40 → 70; tách lưới theo bên L/R vì mặt nạ C3 chọn bên theo tâm hộp bao);
  - mũ 3 lượt (hạ YT làm khe to hơn → trả lại; trung vị; bước dò ngắn);
  - C3 Cas 2 lượt (lượt 1 sai vì lưới hai bên chung một mesh).
- **Hàng đợi** (`/var/tmp/cine-queue/log.tsv`, gói W4, từ 03:35): **24 việc, chờ 0 s, mã 0 cả 24, chạy tổng 791,5 s.**
  - Làn nặng 8 việc: 3 lượt C3 (127–156 s), 5 khung 1920×1080 3 mẫu (15–17 s).
  - Làn nhanh 16 việc: 2 lượt dò 51–53 s; xuất lưới và thử khung 7–18 s.
  - Blender (dựng thân, tay; EEVEE 4 góc khoảng 40–70 s mỗi lượt) chạy ngoài hàng đợi.
- **Token:** khoảng 345 nghìn (hạn khoảng 350 nghìn). Riêng phần đọc đầu gói khoảng 125 nghìn. Bước a khoảng 140 nghìn, vượt hạn khoảng 100 nghìn.

## 9. Việc đang chờ
- **P:** kiểm mù bộ khung mục 4. Nếu đạt: soạn characters v1.6 với bảng C3 'doc' ở mục 3 và phần thân ở mục 6. Khoá v1.5.1 (Ida, `c3_views` giữ nguyên) và v1.6 (Cas) một lần.
- **Chủ dự án:**
  - duyệt thân Cas MPFB và mặc định `CAS_BODY='bl'`;
  - quyết độ dài tay theo sheet (rủi ro 3).
- **Lượt sau (nếu duyệt):** gai gáy Cas; độ rộng áo nếu kiểm mù chê; thử tư thế chim bóng và leo thang; vật liệu tay dưới đèn lồng.
