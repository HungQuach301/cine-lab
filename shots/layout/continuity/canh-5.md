# Continuity sheet — Cảnh 5 "Ngọn cuối" (1:20,00–2:02,50 · s33 → s42)

Gói W2, Cổng 5, luật O1. Nguồn số: `shots_w2.js` (`BAY`, `CAS_LAD`, `CAS_BAY`, `placeBayLantern`), `sets2.js` (`addBayStreet`), `sets_end.js` (`END`).

## Hệ toạ độ
- **Bộ hốc cửa** (s33, s34, s42b, s42 — bộ khoá Cổng 3 `buildS5` + phố bọc ngoài `addBayStreet`): vách trong z_b = 0, miệng vòm z_b = 4, vòm rộng 3,2 m (x_b ±1,6).
  Đổi sang bộ phố: x = x_b + 2,2; z = z_b − 12,1. Ngoài vòm: sân lát 2,5 m, vỉa hè + lòng phố, dãy nam (z_b 17,7), dãy bắc bắt đầu x_b 12,8; L11 + thang ở (5,8; 8,2).
- **Bộ phố** (s35–s41, s42a): toạ độ W1. L11 (8; −3,9), thang tựa phía bắc cột (chân z −4,75), Ida trên thang (8; −4,48; gốc cao 1,55 m).
  `CAS_LAD` = (8,0; −4,98): Cas đứng sau chân thang, mặt +z, hai tay trên hai thanh (x 8 ± 0,17, cao ≈ 0,9 m).
- **Trục 180° cảnh 5:** Ida TRÁI, Cas PHẢI trong mọi shot hai người. s42 máy trong hốc nhìn ra (+z) nên đặt Ida ở +x, Cas ở −x để vẫn Ida trái, Cas phải.

## Lịch (giây phim)
| Sự kiện | Mốc |
|---|---|
| L4 bắt đầu (đầu s37) | 95,00 (1:35,0) |
| P5 (cột góc, đoạn cáp cuối) bật — "…brighter…" | 101,20 (1:41,2), nhấp 2 lần, đứng 101,64 |
| Ida gạt van (`VALVE`) | 109,70 (1:49,7) |
| L11 tắt (`L11_OFF`) | 111,20 (1:51,2) |
| Đèn lồng trao cho Cas | ≈ 114,6 (s41 0,5–0,7 s) |

## s33 · 1:20,00–1:27,00 · WS 32 mm · dolly vào 0,9 m
- **Máy:** bộ khoá: (0,25; 1,35; 10,5) → z 9,6; ống kính dịch (tranh trong tranh).
- **Đèn:** đèn lồng **trên nền đá** ở `BAY.lan` (−0,3; 3,0) — cách vách 3,0 m (nguồn duy nhất trong hốc, có bóng); ngoài vòm điện phẳng. L11 còn cháy (ngoài khung, bên phải).
- **Ida:** 0–1,2 s đứng lên từ tư thế quỳ (vừa đặt đèn) ở (−0,7; 3,5); 1,2–3,2 s đi tới `BAY.ida` (−0,7; 1,6); 3,0–3,8 s quay nhẹ; 4,4 s ngửa nhìn bóng (`look_shadows`). **Không còn đèn lồng trên người** (đang trên nền).
- **Cas:** 1,3–4,7 s đi từ (0,62; 3,9) tới `BAY.cas` (0,62; 0,9); 5,8 s nửa giơ tay (`half_raised`).
- **Bóng (V2, quang học thật):** Ida ×2,14 → cao ≈ 3,5 m, tâm bóng x ≈ −1,16 (lệch trái bà 0,46 m); Cas ×1,43 → ≈ 1,9 m, tâm bóng x ≈ 1,02 (lệch phải cậu 0,40 m). Giữa hai bóng là vách sáng.
- **Trang phục:** mũ Ida `hat_back` 0; mũ len Cas có quả bông.

## s34 · 1:27,00–1:29,00 · MS nghiêng 30 mm · tĩnh
- **Máy:** (1,3; 1,15; 3,6), nhìn (−0,3; 1,5; 0,6) — từ phía phải, sau đèn lồng.
- **Khung trái → phải:** Ida, bóng Ida (cao), Cas, bóng Cas (to hơn cậu, lệch phải).
- **Ida / Cas:** giữ tư thế cuối s33. **Nhìn:** cả hai nhìn lên vách.

## s35 · 1:29,00–1:33,00 · WS 28 mm · tĩnh
- **Máy:** (16,5; 1,7; 2,6), nhìn (5,5; 2,3; −3,8) — xuôi dốc. Khung: hông nhà kho + hốc cửa (trái), L11 + thang (giữa-phải), mặt cuối phố + phố rẽ (nền), dãy bắc (phải).
- **Đèn:** góc TỐI: chỉ L11 (có bóng) + tràn 0,06; P5 tắt.
- **Ida:** 0–2,3 s đi từ (5,7; −6,2) [phía hốc cửa, cắt nén] tới chân thang (8; −5,05); 2,3–3,4 s trèo; từ 3,4 s đứng trên thang (`restLadder`). Đèn lồng: bà **nhặt lại khi rời hốc (ngoài hình, giữa s34 và s35)** và móc ở **hông trái**, cháy — giữ tới s40; s41 tháo ra tay phải để trao.
- **Cas:** 0–3,0 s chạy (1,43 m/s) từ (3,6; −4,6) tới `CAS_LAD`; 3,0–3,6 s chuyển sang giữ thang.

## s36 · 1:33,00–1:35,00 · MCU 85 mm · tĩnh
- **Máy:** `faceCam` (lệch −10°, cách 1,9 m, ngang mắt −0,05).
- **Đèn:** L11 ngay trước mặt (key); `facelight` `gas`; phơi sáng = fl.exposure × 2,0 (probe: fl.exposure 0,082–0,086 → 0,16–0,17).
- **Ida:** trên thang; 0–0,35 s tay trái lên vành (hat_push_a); 1,05 s mũ ngả (hat_push_b, `hat_back` 0,35); 1,6 s tay hạ (`faceRest`, `hat_back` 0,35, cổ quay 35° — nhìn lên phố, **phải khung**).
- **Cas:** giữ thang (ngoài hình).

## s37 · 1:35,00–1:40,80 · CU 85 mm · đẩy vào 1,10 → 0,97 m
- **Đèn:** như s36 (phơi sáng ≈ 0,16). **Thoại:** L4 vế đầu.
- **Ida:** `faceRest` (`hat_back` 0,35), sad_smile, nhìn lên phố (phải khung). Tay phải gần van.

## s37w · 1:40,80–1:43,60 · WS 28 mm · tĩnh
- **Máy:** (17; 1,6; 1,2), nhìn (8,8; 3,6; 0,6). Khung: mặt cuối phố + phố rẽ (giữa-trái), hông + hốc cửa (phải), L11 + thang + hai người (phải), P5 (trái, bóng đèn trong khung).
- **Đèn:** P5 bật 1:41,2 (nhấp 2, đứng) → trắng tràn góc (0,06 → 1,10); bóng dài tan; L11 nhạt về 0,35.
- **Ida:** `faceRest` trên thang. **Cas:** giữ thang, ngửa (cổ −30°).

## s38 · 1:43,60–1:45,00 · MS 50 mm · tĩnh
- **Máy:** (8,75; 2,45; −3,55), nhìn (8,0; 0,95; −5,0) — cao, gần mắt Ida.
- **Cas:** `CAS_LAD`, `hold_ladder` + cổ −36°; **hai tay trên hai thanh thang** (sửa v2: tay lơ lửng). Nhìn lên (Ida).
- **Đèn:** trắng phẳng; L11 0,35.

## s39 · 1:45,00–1:49,40 · CU 85 mm · tĩnh (khung ảnh 4 kiểm mù)
- **Máy:** `faceCam` cách 0,95 m, gần chính diện.
- **Đèn:** trắng phẳng (whiteHemi 0,99) + L11 nhạt; `facelight` `elec` (keyE = whiteHemi); phơi sáng = fl.exposure × 1,0 (probe: 0,358). Vành mũ đổ bóng lên trán; tường vôi sau lưng sáng xám — mặt không là vùng sáng duy nhất.
- **Ida:** choked, nhìn lên phố (phải khung).

## s40 · 1:49,40–1:52,00 · CU insert 50 mm
- **Ida:** tay phải gạt van 0,3–0,9 s; lửa co, xanh, tắt ở 1,8 s; giữ im 0,8 s.

## s40w · 1:52,00–1:54,00 · WS 28 mm — cùng máy s37w
- L11 tối; không gì đổi. Ida `restLadder`, Cas giữ thang.

## s41 · 1:54,00–1:55,50 · WS 28 mm
- **Máy:** (12,8; 1,5; 0,6), nhìn (8,2; 1,2; −4,6).
- **Ida:** dưới chân thang (8,9; −4,6), đèn lồng **tay phải** (0 s) → chìa ra (0,5 s). **Cas:** (7,9; −4,4) đón bằng hai tay (0,7 s). Đạo cụ đổi chủ: đèn lồng → Cas (hai tay).

## s42a · 1:55,50–1:57,50 · MS 45 mm
- **Cas:** (7,6; −3,3), ôm đèn lồng giữa hai cổ tay; đầu quay trái 38° (0,8 s), phải −30° (1,6 s), −45° (2,0 s: nhìn hốc cửa — **trái khung**).
- **Ida:** (8,9; −4,6), không đèn lồng, nhìn Cas.

## s42b · 1:57,50–1:59,50 · WS 32 mm (ngoài vòm)
- **Máy:** (0,9; 1,25; 8,2), nhìn (0,3; 1,1; 2,0).
- **Cas:** đi từ (1,9; 5,3) vào `CAS_BAY` (−0,35; 2,55) trong 1,5 s, đèn lồng treo giữa hai cổ tay (nguồn sáng đi theo); 1,3–2,0 s quay người ra vòm. **Mũ len + quả bông còn nguyên** (V1).

## s42 · 1:59,50–2:02,50 · MS 40 mm (trong hốc nhìn ra vòm)
- **Máy:** (0,55; 0,66; 0,45), nhìn (−0,15; 0,75; 4,5) — sau lưng Cas lệch phải, thấp ngang vai.
- **Đèn:** đèn lồng trên nền đá trước mặt Cas (−0,38; 3,10); ngoài vòm điện phẳng.
- **Cas:** `CAS_BAY`, ngồi xổm (`warm_hands_copy`), **quay ra vòm** (yaw 0); nhịp đếm 0,6 / 1,2 / 1,8 s. Mũ len + quả bông in trên nền phố trắng (V1). **Phải khung.**
- **Ida:** miệng vòm (1,25; 5,25), đứng nhìn vào, không đèn lồng. **Trái khung.**

## TRẠNG THÁI Ở KHUNG CUỐI s42 (2:02,50) → cảnh 6
| Mục | Trạng thái |
|---|---|
| L11 | Tắt (lồng kính tối) |
| Cột điện | Toàn phố trắng, P5 sáng |
| Đèn lồng | Của Cas (đặt trên nền hốc cửa) |
| Ida | Không đèn lồng; thang còn tựa L11 (cảnh 6: bà vác thang — s47) |
| Mũ Ida | `hat_back` 0,35 từ s36 tới hết cảnh 5 (s37, s37w, s38, s39, s40, s40w, s41, s42a, s42 đều 0,35). Cảnh 6 (2 giờ sau) về 0 — **chờ chủ dự án** (LAYOUT-W2.md, hàng chờ Q-W2-2) |
