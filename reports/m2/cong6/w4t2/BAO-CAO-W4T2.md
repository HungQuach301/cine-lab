# Cổng 6 — W4T lượt 2: sửa thân Cas (quần, eo, áo, gáy, tay MPFB, vật liệu tay); đo C3

Người làm: **phiên P**, không phải phiên xưởng; lý do ở mục 7.
Worktree: `.claude/worktrees/w4t2`, nhánh `w4t2-cas-than`, gốc 1cbd850. Ngày 29/09/2026.

**Mặc định layout không đổi.** Mọi thay đổi đều nằm sau cờ `casStyle:'bl'` + `casBody:'bl'`; da tay nằm sau `handsStyle:'bl'`. Kiểm bằng dò layout mặc định s02, s24c, s37, s42: 12 ảnh nhỏ, **lệch 0 px** so với lần dò sau lượt 1.

## 0. Tóm tắt
- **Điều kiện dừng: QUA.** Kiểm trên ảnh EEVEE 4 góc và khung s42a (3 mẫu):
  - quần ống thẳng, không bó, không lộ háng;
  - áo len phủ qua cạp quần;
  - không còn dải da ở eo khi đứng, khi cầm đèn lồng (s42a) và khi giơ tay cao nhất (s25, chim bóng).
- **Tay Cas theo tỷ lệ MPFB:** tầm với vai → cổ tay ngắn hơn 15,8 %. Điểm nắm lệch 4–7 cm trong 13 shot có Cas (mục 4); danh sách giao W1/W2.
- **C3 Cas 'doc'** đo lại (mục 3). Nháp v1.6 đã có bảng `c3_views` mới (`characters-v1.6-NHAP.md` mục 6).

## 1. Việc đã làm (a–e) và bằng chứng
| Việc | Cách làm | Ảnh |
|---|---|---|
| a. Quần | Mỗi ống có bán kính tối thiểu 4,6 cm quanh trục chân (tiết diện elip, sâu 0,92); dưới đáy đũng vải không bám bắp chân hay đầu gối. Làm mượt riêng vùng đũng. Nếp gối, rủ dọc ống, nếp chùng trên gấu. Gấu thẳng | `W4T2_truoc-sau_quan.jpg` |
| b. Eo | Gấu áo hạ từ 2,25 H xuống **2,10 H**, cách đáy đũng thật 2,1 cm; bỏ bo gấu ôm, cho gấu buông và loe nhẹ. Trọng số hông ở gấu áo dồn 60 % về chậu, để gấu treo theo chậu chứ không kéo theo đùi | `W4T2_truoc-sau_eo.jpg`: s42a 114,5 s và s25 60,5 s |
| c. Áo và gáy | Áo nới 1,1 → 1,6 cm, tay áo 1,2 cm. Ngực: khớp một mặt đa thức trơn, hết in cơ ngực và núm. Lưng: vải bắc cầu qua chỗ lõm, hết rãnh xương cùng. Gáy: cổ lật nới 0,03 H phía sau (thu dần về chân cổ) và dâng 0,085 H | `W4T2_truoc-sau_ao.jpg` |
| d. Tay theo tỷ lệ MPFB | Độ dài xương MPFB × (1,28 / 1,289). Khớp tay trên 0,7643 H, cẳng tay 0,7009 H (sheet: 0,92 và 0,82). Số ghi trong `cas_body_bl.json` (`arm`); cast3d chỉ đổi sheet khi cờ thân 'bl' bật | `W4T2_truoc-sau_tay.jpg` (hàng trên) |
| e. Da tay dưới đèn lồng | Vật liệu da tay 'bl' cuộn sáng mềm (ngưỡng 0,4, trần 0,8), không thêm đèn. Màu da tay Cas #e2bfa2 → #cf9878. **Tay Ida ('bl') cũng nhận cuộn sáng; màu tay Ida giữ nguyên** | `W4T2_truoc-sau_tay.jpg` (hàng dưới). Trung vị pixel tay ở s42a: lượt 1 (244,199,173) → lượt 2 (238,152,108) |
| Thêm: măng sét | Rộng hơn 0,6 cm, dài 0,09 H (trước 0,07 H), trùm hết cuống cổ tay MPFB. Ở lượt 1, chỗ này lộ một tấm da dẹt trông như cổ găng | EEVEE cận (không nộp) |

### Nguyên nhân tìm được khi sửa (đo, không đoán)
- **"Dải da ở eo" ở s42a lượt 1:** đó là **đế đèn lồng sáng** nằm đúng chỗ gấu áo gặp cạp quần. Hạ gấu áo xong thì dưới đèn lồng thấy len, không còn thấy khe.
- **"Gai ở gáy":** da gáy MPFB có bán kính 5,9 cm, **nằm ngoài ống cổ lật** (bán kính ngoài 5,6 cm) nên xuyên qua thành đốm và mép lởm chởm.
- **Rãnh giữa lưng dưới** đọc thành khe mông, sâu 10–15 mm, có hai nguồn:
  - làm mượt Taubin nhiều vòng trên lưới MPFB mật độ không đều làm đỉnh trượt;
  - bước chia lưới Catmull-Clark.

  Đã sửa bằng bắc cầu cục bộ trên lưới đã chia. Lõm còn lại ≤ 1,1 mm.

## 2. Điều kiện dừng
`W4T2_cas_eevee_4goc.jpg` (0°, 60°, 180°, −120°) và `W4T2_hai-nguoi_s42a.jpg` (1920×1080, 3 mẫu): không còn quần bó, không lộ háng, không khe da. **Qua.**

## 3. C3 Cas theo 'doc' (tay mới; `c3_w4t.py` + `page_turn_w4t.js`; làn nặng 174 s)
| Góc | thân | tay trên | cẳng tay | đùi | cẳng chân | đầu doc (px, 4×) | thân so với lượt 1 |
|---|---|---|---|---|---|---|---|
| 0° | 2,723 | 1,564 | 1,053 | 1,494 | 1,461 | 487,0 | +13,2 % |
| 45° | 2,814 | 1,607 | 1,047 | 1,587 | 1,457 | 478,8 | +13,6 % |
| −45° | 2,809 | 1,548 | 1,087 | 1,527 | 1,608 | 479,7 | +13,6 % |
| 90° | 2,832 | —¹ | —¹ | 0,986 | 1,395 | 475,1 | +12,9 % |
| −90° | 2,832 | 1,537 | 1,112 | 1,581 | 1,618 | 475,1 | +13,0 % |
| 135° | 2,931 | 1,563 | 1,138 | 1,592 | 1,613 | 465,1 | +22,9 % |
| −135° | 2,990 | 1,639 | 1,164 | 1,546 | 1,657 | 456,4 | +24,9 % |
| 180° | 4,045 | 2,261 | 1,635 | 2,209 | 2,272 | 328,1 | +29,8 % |

¹ Tay khuất sau thân, ghi null như v1.4.

Đọc số:
- Thân dài hơn trong mặt nạ vì gấu áo hạ 0,15 H.
- Ở góc sau, cổ lật dâng cao che thêm gáy, nên đầu doc nhỏ lại (180°: 370,5 → 328,1 px) và tỷ lệ thân/đầu tăng.
- Đùi ngắn lại vì áo phủ phần trên đùi.
- Tay ngắn lại theo MPFB.
- Đây là số khai mới của v1.6, không phải số so với ngưỡng.

Số thô: `W4T2_c3_cas_doc.json`.

## 4. Shot có tư thế cầm nắm hoặc với tay của Cas: giao W1/W2 (không sửa layout)
**Cách đo:**
- Chạy trang thử `page_l2.js` tại giữa shot, hai cấu hình:
  - A: Cas 'bl', thân cũ, tay theo sheet;
  - B: thân mới, tay MPFB.
- Đo độ dời tâm lòng bàn tay (thế giới, cm).
- "Nắm" là cờ nắm của bộ giải tay MPFB.

| Shot | Giây | Việc của tay | Độ dời tâm lòng tay L / R | Cần W1/W2 |
|---|---|---|---|---|
| s24c | 58,2 | dựa tường | 7,0 / 7,0 cm | tay không còn chạm tường |
| s25 | 60,5 | chim bóng (tay giơ cao) | 6,4 / 6,4 cm | hình chim bóng thấp hơn, gần đầu hơn; kiểm bóng trên tường |
| s28 | 68,0 | vỗ tay | 6,4 / 6,4 cm | điểm chạm hai tay |
| s29 | 70,5 | hạ tay, xoay người | 7,0 / 7,0 cm | — (không cầm) |
| s32 | 78,5 | giơ tay vào quầng hổ phách | 7,0 / 6,9 cm | chim bóng |
| s33 | 82,5 | bước vào | 7,0 / 7,0 cm | — |
| s34 | 86,0 | (tay tự do) | 6,5 / 6,0 cm | — |
| **s37w** | 100,2 | **giữ thang** | 6,7 / 6,7 cm (đang nắm) | **dời tay lên thanh thang (IK `reachGrip`)** |
| **s38** | 106,7 | **giữ hai thanh thang** | 6,7 / 6,7 cm (đang nắm) | **như trên** |
| **s40w** | 111,0 | **giữ thang** | 6,7 / 6,7 cm (đang nắm) | **như trên** |
| **s41** | 112,8 | **đón đèn lồng hai tay** | 3,9 / 4,0 cm (đang nắm) | **quai đèn lồng về nắm tay** |
| **s42a** | 114,5 | **cầm đèn lồng** | 4,0 / 4,0 cm (đang nắm) | **như trên** (khung nộp dùng `grips` của trang thử) |
| s42 | 119,0 | ngồi xổm, áp tay | 6,6 / 6,6 cm | điểm áp tay lên vòm |
| s42b, s48 | 116,5; 138,0 | ôm đèn đi; chim trên cao | **không đo được**: trang thử lỗi ngay (mã 1, 3–4 s) ở hai shot này | W1/W2 đo lại trên clip |

Độ dời pixel chưa đo, vì nó tuỳ máy quay từng shot. W1/W2 đo trên clip.

## 5. Rủi ro còn lại
1. **Vai khi giơ tay cao (s25):** áo len dồn thành khối ở vai bên giơ tay. Đây là biến dạng da tuyến tính (bind ở tư thế vai dạng 24°). Tư thế này không nằm trong khung kiểm mù. Việc cho W1/W2 hoặc lượt sau.
2. **Ngực:** ở góc 0° vẫn còn bóng rất nhẹ ở mép dưới cơ ngực.
3. **Đế đèn lồng sáng** vẫn nằm ngang eo ở s42a. Nay phía dưới là len chứ không phải khe, nhưng người xem vẫn có thể thấy một dải sáng.
4. **Tay dưới đèn lồng:** mặt trên các ngón vẫn nhạt, vì hướng về phía ánh trời lạnh. Tay đã ấm hơn rõ, nhưng chưa chắc qua kiểm mù.
5. **Tay ngắn:** mọi tư thế cầm nắm lệch 4–7 cm (mục 4).

## 6. Tệp
- Sửa:
  - `blender/build_cas_body_bl.py`: tay MPFB, gấu áo, quần thẳng, đũng, ngực/lưng trơn, bắc cầu;
  - `blender/cas_body_bl.json`: `version` w4t-2, có `arm`, `meta.hemY`, `meta.crotchY`;
  - `blender/body_bl.js`: `casBodyArm()`;
  - `cast3d.js`: đổi độ dài tay trước khi dựng khung (chỉ khi cờ bật); cổ lật nới sau gáy; măng sét; `HAND_SKIN`;
  - `blender/bl_head.js`: tuỳ chọn `skinKnee`/`skinCap`, mặc định 0 nên đầu không đổi.
- Nháp: `reports/m2/cong5/w4/characters-v1.6-NHAP.md` mục 6.
- Không có tài sản mới. Số đo tay lấy từ khung xương MPFB lõi, nằm trong phạm vi RIGHTS W4-MPFB-A3/A4.

## 7. Thời gian, hàng đợi, token, và việc phiên xưởng không chạy được
- **Hai lần giao phiên xưởng (cine-worker) đều dừng ngay.**
  - Worktree cô lập của phiên xưởng được tạo từ `main` @08c07dd, không có W4T lượt 1.
  - Worker không được phép tự đưa nhánh lên đầu nhánh P (bộ phân loại quyền chặn), nên đã dừng đúng luật.
  - Chi phí: khoảng 20 nghìn + 20 nghìn token, lần hai chạy 28,5 phút.
  - **P tự làm** trong worktree `w4t2` do P tạo từ nhánh P. P không chạy hộ các lệnh đã bị chặn với worker.
- **Giờ UTC** (P làm):

  | Việc | Giờ |
  |---|---|
  | Chẩn đoán | 06:15–06:20 |
  | Tay, gấu áo, quần | 06:20–06:25 |
  | Vật liệu tay | 06:26–06:28 |
  | Gáy | 06:28–06:36 |
  | Eo khi giơ tay, rãnh lưng | 06:36–06:53 |
  | Ngực | 06:53–06:56 |
  | Măng sét | 06:56–06:58 |
  | Điều kiện dừng | 06:58–07:00 |
  | C3, dò, lệch điểm nắm, ảnh trước/sau | 07:00–07:20 |

- **Làm lại:**
  - rãnh lưng 5 lượt (làm mượt → giảm nếp → bắc cầu trước làm mượt → sau nếp → sau chia lưới + lấp cục bộ);
  - ngực 2 lượt (khớp theo lát gây nhiễu, đổi sang mặt đa thức);
  - da tay 3 lượt;
  - gáy 2 lượt;
  - đáy đũng 1 lượt (lần đầu nhận nhầm đùi trong làm đáy đũng).
- **Hàng đợi** (gói W4, từ 06:15):
  - 68 việc: 6 nặng, 62 nhanh;
  - chờ tổng 300 s, chạy tổng 1 254 s, 0 việc quá 60 s ở làn nhanh;
  - 4 việc mã ≠ 0: trang thử ở s42b và s48, mục 4.
  - Blender (dựng thân 2 s mỗi lượt; EEVEE) chạy ngoài hàng đợi.
- **Token:** phần P tự làm tốn **khoảng 285 nghìn** theo bộ đếm phiên P (có cả ảnh xem kiểm), **vượt hạn khoảng 150 nghìn**. Nguyên nhân chính là chẩn đoán rãnh lưng và gáy.
