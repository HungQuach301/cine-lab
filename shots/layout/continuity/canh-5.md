# Continuity sheet — Cảnh 5 "Ngọn cuối" (1:20,00–2:00,50 · s33 → s42)

Gói W2, Cổng 5, luật O1. Nguồn số: `shots_w2.js` (`BAY`, `CAS_LAD`, `CAS_BAY`, `casHug`, `placeBayLantern`), `sets2.js` (`addBayStreet`), `sets_end.js` (`END`).
Bản v3 (rà continuity v2 — C5, N2, N3, N7, N9): mốc thời gian theo bảng thời gian hiện hành (s33 5,0 s; tổng phim 140,5 s); chỉ ghi những gì có trên hình. Ảnh 4 kiểm mù: khung toàn cục **2510** (khung 72 của s39, 104,58 s — chữ "dark").
**Bản Cổng 6 W2 v1 (29/09/2026 — AUTHORSHIP "Cổng 6 — diễn hoạt"):** PA1 "nghiêng dưới ngọn lửa" cho s36–s39 (tách s37 → **s37 + s37b**, giữ id s37 cho phần đầu); s40 mặt Ida chìm vào bóng tối đúng 109,20; Cas giữ thang **cạnh chân thang phía đông** (G10); bà xuống thang trong s40w; trao đèn s41 ở khoảng cách 0,57 m; tay MPFB nắm van, cần van, thanh thang, vòng quai bằng IK. Chi tiết: mục "Cổng 6" cuối tệp.
Bản v4 (Cổng 5 v2 — quyết định chủ dự án @e850c0f): **B-i** mọi shot là hàm thuần theo t (xem LAYOUT-W2 §0); **(c)** s39 (Ida) đứng TRƯỚC s38 (Cas) — câu "Just… keep a little dark for the ones who need it." bắt đầu trên mặt Ida; **(e)** người/bóng hốc vòm không sửa ở layout (Cổng 7).

## Quyết định đang áp dụng
- **A2 (a):** s33 5,0 s. **A2 (b):** sau `L11_OFF`, kính L11 tối đục (#16181f, độ đục 0,85) ở s40w, s41, s42a — kính trống, không lửa, không quầng.
- **B1:** cột điện phố chính trong sân SÁNG suốt các shot bộ phố cảnh 5 (vũng sáng tầm 8,5 m quanh (17,0; −5,9)); góc L11 và hốc cửa ngoài vũng → **tối tới khi P5 bật (1:39,2)**; bản cột cũ (13,5; −4,2) của W1 bị ẩn trong shot W2.
- **C5 (v3):** s33, s34 (trước P5) ngoài vòm là **góc tối lạnh**: chỉ hổ phách L11 từ bên phải (ngoài khung) + tràn điện xa × 0,05 (cùng mức tràn góc tối của s35). s42b, s42 (sau P5) ngoài vòm trắng.

## Hệ toạ độ
- **Bộ hốc cửa** (s33, s34, s42b, s42 — bộ khoá Cổng 3 `buildS5` + phố bọc ngoài `addBayStreet`): vách trong z_b = 0, miệng vòm z_b = 4, vòm rộng 3,2 m (x_b ±1,6).
  Đổi sang bộ phố: x = x_b + 2,2; z = z_b − 12,1. Ngoài vòm: sân lát, vỉa hè + lòng phố, dãy nam (z_b 17,7), dãy bắc bắt đầu x_b 12,8; L11 + thang ở (5,8; 8,2).
- **Bộ phố** (s35–s41, s42a): toạ độ W1. L11 (8; −3,9), thang tựa phía bắc cột (chân z −4,75), Ida trên thang (8; −4,48; gốc cao 1,55 m).
  `CAS_LAD` = (8,0; −4,98): Cas đứng sau chân thang, mặt +z, hai tay trên hai thanh (x 8 ± 0,17, cao ≈ 0,9 m).
- **Trục 180° cảnh 5:** Ida TRÁI, Cas PHẢI trong mọi shot hai người (s33, s34, s35, s37w, s40w, s41, s42a, s42). s42 máy trong hốc nhìn ra (+z) nên đặt Ida ở +x, Cas ở −x để vẫn Ida trái, Cas phải.

## Mũ Ida — `hat_back` đầu / cuối mỗi shot (quyết định chủ dự án, AUTHORSHIP; world-rules v0.5)
Bà tự đẩy vành mũ ra sau trước lời từ biệt (s36) và **kéo mũ lại khi rời đi** (cuối s42) — cử chỉ khép "hết ca".
Chọn s42 thay vì s41: ở s41 bà đang trao đèn (hai tay bận, trao là nhịp chính); ở cuối s42 bà vừa thấy Cas tự đếm ba — khoảnh khắc buông tay,
bà đứng ở miệng vòm trên nền phố trắng nên dáng tay–vành mũ in rõ, và ngay sau đó bà quay người rời khỏi vòm (nối sang cảnh 6).

| Shot | Đầu | Cuối | Ghi chú |
|---|---|---|---|
| s33, s34, s35 | 0 | 0 | |
| s36 | 0 | 0,35 | tay trái đẩy vành: 0–0,35 s đưa tay, 0,35–1,05 s đẩy, 1,6 s hạ tay |
| s37, s37b, s37w, s39, s38, s40, s40w | 0,35 | 0,35 | Cổng 6 G2: s40 giữ 0,35 như s39 (không còn "mũ thẳng") |
| s41, s42a | 0,35 | 0,35 | |
| s42b | — | — | Ida không có trong khung |
| s42 | 0,35 | **0** | 1,9–2,2 s tay trái lên vành; **2,2–2,8 s kéo vành xuống (0,35 → 0)**; 2,8–3,0 s hạ tay, quay người +0,5 rad (rời khỏi vòm) |
| s43 → s48 | 0 | 0 | cảnh 6 |

## Đèn lồng — ai giữ, cầm thế nào (N2, N7)
| Shot | Chủ | Cách cầm / vị trí |
|---|---|---|
| s33, s34 | — | trên nền đá hốc cửa, `BAY.lan` (0,2; 3,0) |
| s35 → s40w (1,8 s) | Ida | móc **hông trái**, cháy (nhặt lại khi rời hốc — ngoài hình, giữa s34 và s35) |
| s40w 1,8–2,0 s | Ida | tháo khỏi móc, sang **tay phải** (Cổng 6 — nối s41) |
| s41 | Ida → Cas | Cổng 6: Ida tay phải (0 s) → chìa ngắn (0,45 s, khuỷu gập); Cas nắm hai bên vòng quai (IK, 0,35–0,75 s); Ida buông 0,85 s; Cas kéo về ôm sát ngực (1,35 s) |
| s42a | Cas | `casHug`: hai khuỷu gập sát, hai cổ tay trước ngực, đèn áp bụng |
| s42b | Cas | `casHug` khi đi (0–1,45 s); 1,6–2,0 s hạ đèn xuống nền trước mặt (−0,38; 3,10) |
| s42 | Cas | trên nền đá trước mặt Cas (−0,38; 3,10) |

## Lịch (giây phim)
| Sự kiện | Mốc |
|---|---|
| L4 bắt đầu (đầu s37) | 93,00 (1:33,0) |
| Cổng 6 — "That's the last one, then." (đo trên tệp take: bao năng lượng −38 dB + onset) | 93,09–95,01 — s37 (MCU nghiêng) |
| Cổng 6 — nhịp cười buồn 1 (cười, mắt chùng, dừng) | 95,0–96,4 — s37 |
| Cắt s37 → s37b | 96,40 |
| Cổng 6 — "Goodnight, old street." | 96,55–98,06 — s37b (CU nghiêng, đẩy chậm) |
| Cổng 6 — nhịp cười buồn 2 | 98,1–98,8 — s37b |
| "You'll be brighter now." | 99,54–100,97 — s37w (ngoài hình mặt) |
| "Just…" (vế cuối L4) — lời thật từ L4 + 9,33 s (P); whisper: "Just" 9,68 | 102,33 (1:42,33) — trên **s39 (Ida)** |
| "keep a little dark" (whisper 10,36–12,08) | 103,36–105,08 — s39 |
| "for the ones" (whisper 12,08–13,00) | 105,08–106,00 — s39 |
| **Cắt s39 → s38 (Cas phản ứng)** | **106,00 (1:46,0)** — giữa "…ones / who need it" |
| "who need it." (whisper 13,00–14,00) | 106,00–107,00 — s38 |
| P5 (cột góc, đoạn cáp cuối) bật — "…brighter…" | 99,20 (1:39,2), nhấp 2 lần, đứng 99,64 |
| Ida gạt van (`VALVE`) | 107,70 (1:47,7) |
| L11 tắt (`L11_OFF`) | 109,20 (1:49,2) |
| Đèn lồng trao cho Cas | ≈ 112,5–112,7 (s41 0,5–0,7 s) |
| Cas đặt đèn xuống nền | 117,1–117,5 (s42b 1,6–2,0 s) |
| Ida kéo mũ lại | 119,70 → 120,30 (s42 2,2–2,8 s) |

## s33 · 1:20,00–1:25,00 · WS 32 mm · dolly vào 0,9 m + dịch ngang trái 0,4 m
- **Máy:** bộ khoá (0,25; 1,35; 10,5) → dịch (−0,4; 0; −0,9); ống kính dịch (tranh trong tranh). Phơi sáng 1,5.
- **Đèn (C5):** trong hốc: đèn lồng **trên nền đá** ở `BAY.lan` (0,2; 3,0) — nguồn duy nhất trong hốc, có bóng, key hổ phách. Ngoài vòm: **góc tối lạnh** — mặt tường quanh vòm đo (48, 46, 52) bên trái, (91, 69, 61) bên phải (hổ phách L11 từ ngoài khung phải); v2 là (217, 217, 221) trắng phẳng.
- **Ida:** 0–0,6 s đứng dậy từ tư thế quỳ (vừa đặt đèn) ở (−0,62; 3,5); 0,6–2,7 s đi tới `BAY.ida` (−0,62; 1,45); 2,5–3,3 s quay nhẹ; 3,6 s ngửa nhìn bóng (`look_shadows`). Không đèn lồng trên người.
- **Cas:** 0,6–4,1 s đi từ (0,9; 3,9) tới `BAY.cas` (0,9; 0,8); 3,9–4,6 s quay nhẹ; 4,6 s nửa giơ tay (`half_raised`).
- **Bóng (V2, quang học thật — N3 v3):** phóng đại = đèn→vách ÷ đèn→người. Ida ×1,94 → cao ≈ 3,2 m, tâm bóng x ≈ −1,39 (lệch **trái** bà 0,77 m: vành mũ của bóng ra khỏi người); Cas ×1,36 → ≈ 1,8 m, tâm bóng x ≈ 1,15 (lệch phải cậu 0,25 m). Máy dịch trái làm Ida (gần máy hơn vách) trượt sang phải, xa bóng của bà. Nửa tối: PCF radius 4.
- **Trang phục:** mũ Ida `hat_back` 0; mũ len Cas có quả bông.

## s34 · 1:25,00–1:27,00 · MS nghiêng 26 mm · tĩnh
- **Máy:** (1,35; 1,15; 4,0), nhìn (−0,2; 1,35; 0,4) — từ phía phải, sau đèn lồng; thấy nền đá: vệt bóng trên nền nối chân mỗi người với bóng của họ trên vách. Không thấy ngoài vòm.
- **Khung trái → phải:** Ida, bóng Ida (cao), Cas, bóng Cas (to hơn cậu, lệch phải).
- **Ida / Cas:** giữ vị trí cuối s33 (`BAY`). **Nhìn:** cả hai nhìn lên vách.

## s35 · 1:27,00–1:31,00 · WS 28 mm · tĩnh
- **Máy:** (16,5; 1,7; 2,6), nhìn (5,5; 2,3; −3,8) — xuôi dốc. Khung: hông nhà kho + hốc cửa (trái), L11 + thang (giữa-phải), mặt cuối phố + phố rẽ (nền).
- **Đèn:** góc TỐI: chỉ L11 (có bóng) + tràn 0,06; P5 tắt.
- **Ida:** 0–2,3 s đi từ (5,7; −6,2) [phía hốc cửa, cắt nén] tới chân thang (8; −5,05); 2,3–3,4 s trèo; từ 3,4 s đứng trên thang (`restLadder`). Đèn lồng ở **hông trái**, cháy.
- **Cas:** 0–3,0 s chạy từ (3,6; −4,6) tới `CAS_LAD`; 3,0–3,6 s chuyển sang giữ thang.

## s36 · 1:31,00–1:33,00 · MCU 85 mm · tĩnh
- **Máy:** `faceCam` (lệch −10°, cách 1,9 m, ngang mắt −0,05).
- **Đèn:** L11 ngay trước mặt (key); `facelight` `gas`, EK 1,3.
- **Ida:** trên thang; 0–0,35 s tay trái lên vành; 1,05 s mũ ngả (`hat_back` 0,35); 1,6 s tay hạ, cổ quay 35° — nhìn lên phố, **phải khung**.
- **Cas:** giữ thang (ngoài hình).

## s37 · 1:33,00–1:38,80 · CU 85 mm · đẩy vào 1,10 → 0,97 m
- **Đèn:** như s36 (EK 1,3; máy lệch +10°). **Thoại:** L4 vế đầu.
- **Ida:** `faceRest` (`hat_back` 0,35), sad_smile. Trên hình (N11): mặt 3/4 sang phải khung, **mắt nhìn xuống** (về phía Cas dưới chân thang), không nhìn lên phố.

## s37w · 1:38,80–1:41,60 · WS 28 mm · tĩnh
- **Máy:** (17; 1,6; 1,2), nhìn (8,8; 3,6; 0,6). Khung: mặt cuối phố + phố rẽ (giữa-trái), hông + hốc cửa (phải), L11 + thang + hai người (phải), P5 (trái, bóng đèn trong khung).
- **Đèn:** P5 bật 1:39,2 (nhấp 2, đứng 1:39,64) → trắng tràn góc (0,06 → 1,10); bóng dài tan; L11 nhạt về 0,35.
- **Ida:** `faceRest` trên thang. **Cas:** giữ thang, ngửa.

## s39 · 1:41,60–1:46,00 · CU 85 mm · tĩnh (khung ảnh 4 kiểm mù: khung 72 = toàn cục 2510)
- **(c) Thứ tự mới:** s39 đứng trước s38 để câu cuối L4 BẮT ĐẦU trên mặt Ida ("Just…" 1:42,33 là 0,73 s sau đầu shot) và kéo qua "…keep a little dark for the ones".
- **Máy:** `faceCam` cách 0,95 m, gần chính diện.
- **Đèn:** trắng phẳng + L11 nhạt; `facelight` `elec`; phơi sáng × 0,8. Vành mũ đổ bóng lên trán; tường vôi sau lưng sáng xám.
- **Ida:** choked. Trên hình (N11): mặt gần chính diện, **mắt nhìn xuống** (về Cas) — khớp s38 ngay sau: Cas ngước lên về phía bà (bà nhìn xuống, cậu nhìn lên).

## s38 · 1:46,00–1:47,40 · MS 50 mm · tĩnh
- **(c)** Cas phản ứng từ giữa câu ("…who need it." 1:46,0–1:47,0), rồi 0,4 s im trước insert van (s40).
- **Máy:** (8,75; 2,45; −3,55), nhìn (8,0; 0,95; −5,0) — cao, gần mắt Ida.
- **Cas:** `CAS_LAD`, `hold_ladder` + cổ −36°; hai tay trên hai thanh thang. Nhìn lên (Ida).
- **Đèn:** trắng phẳng; L11 0,35.

## s40 · 1:47,40–1:50,00 · CU insert 50 mm
- **Ida:** tay phải gạt van 0,3–0,9 s (1:47,7); lửa co, xanh, tắt ở 1,8 s (1:49,2); giữ im 0,8 s.

## s40w · 1:50,00–1:52,00 · WS 28 mm — cùng máy s37w
- L11 tối (kính đục, không lửa). Ida `restLadder`, Cas giữ thang.

## s41 · 1:52,00–1:53,50 · WS 28 mm
- **Máy:** (12,8; 1,5; 0,6), nhìn (8,2; 1,2; −4,6).
- **Ida:** chân thang phía tây (7,9; −4,4), đèn lồng **tay phải** (0 s) → chìa ra (0,5 s). **Cas:** (8,9; −4,6) đón bằng hai tay, ôm sát ngực (`casHug`, 0,7 s). **Ida TRÁI, Cas PHẢI**.

## s42a · 1:53,50–1:55,50 · MS 45 mm
- **Cas:** (7,6; −3,3), ôm đèn sát ngực (`casHug`); đầu quay trái 38° (0,8 s), phải −30° (1,6 s), −45° (2,0 s: nhìn hốc cửa — **trái khung**).
- **Ida:** (6,8; −2,5) — lòng phố, **TRÁI khung**, không đèn lồng, nhìn Cas.

## s42b · 1:55,50–1:57,50 · WS 32 mm (ngoài vòm) — N2 + N7
- **Máy:** (0,9; 1,25; 8,2), nhìn (0,3; 1,1; 2,0). Ngoài vòm: phố trắng (sau P5).
- **Cas:** 0–1,3 s đi từ (1,9; 5,3) vào `CAS_BAY` (−0,35; 2,55), đèn lồng **ôm sát ngực** (`casHug`, cùng cách cầm s41/s42a); 1,1–1,5 s quay ra vòm (yaw 0); 1,45–2,0 s **ngồi xổm** (tư thế cuối = `warm_hands_copy`, đúng tư thế mở s42); 1,6–2,0 s **đặt đèn xuống nền** trước mặt (−0,38; 3,10) — đúng chỗ đèn ở s42. Bóng lớn của Cas đổ lên vách trong khi đèn hạ thấp. Mũ len + quả bông còn nguyên (V1).

## s42 · 1:57,50–2:00,50 · MS 40 mm (trong hốc nhìn ra vòm)
- **Máy:** (0,55; 0,66; 0,45), nhìn (−0,15; 0,75; 4,5) — sau lưng Cas lệch phải, thấp ngang vai.
- **Đèn:** đèn lồng trên nền đá trước mặt Cas (−0,38; 3,10); ngoài vòm điện phẳng (sau P5).
- **Cas:** `CAS_BAY`, ngồi xổm (`warm_hands_copy`), **quay ra vòm**; nhịp đếm 0,6 / 1,2 / 1,8 s. Mũ len + quả bông in trên nền phố trắng (V1). **Phải khung.**
- **Ida:** miệng vòm (1,25; 5,25), đứng nhìn vào, không đèn lồng. **Trái khung.** Cuối shot kéo mũ lại (bảng mũ) rồi quay người đi.

## TRẠNG THÁI Ở KHUNG CUỐI s42 (2:00,50) → cảnh 6
| Mục | Trạng thái |
|---|---|
| L11 | Tắt (lồng kính tối) |
| Cột điện | Toàn phố trắng, P5 sáng |
| Đèn lồng | Của Cas (đặt trên nền hốc cửa) |
| Ida | Không đèn lồng; thang còn tựa L11 (cảnh 6: bà vác thang — s47) |
| Mũ Ida | Kéo lại về `hat_back` 0 ở cuối s42 (1:59,70 → 2:00,30) — cảnh 6 giữ 0 |


## Cổng 6 · W2 v1 — diễn hoạt (29/09/2026)
**Trục 180°:** mọi máy PA1 (s36, s37, s37b, s39) và s40 ở phía **+x (phía phố)**, cùng phía máy s37w/s38/s40w/s41 → Ida nhìn sang **TRÁI khung** ở cả CU lẫn WS (Cổng 5: CU chính diện, bà nhìn phải khung — ngược hướng màn hình với s37w).

| Shot | Thời gian | Cỡ · mm | Máy (so với hướng MẶT bà) | Diễn / tay |
|---|---|---|---|---|
| s36 | 91,0–93,0 | MCU · 85 | 3/4 nghiêng **60°**, 1,9 m, tĩnh | đẩy vành mũ (0–1,05 s); 1,55–2,0 s tay trái hạ xuống **nắm thân van** (IK trộn); hít vào trước lời |
| s37 | 93,0–96,4 | MCU · 50 | nghiêng **90°**, 1,35 m, tĩnh; ngọn L11 trong khung | tay trái nắm van; "That's the last one, then." (khẩu hình); **95,0–96,4 cười buồn + mắt chùng + dừng** (chớp chậm 95,75) |
| s37b | 96,4–98,8 | CU · 85 | nghiêng **90°**, đẩy 1,10 → 0,95 m | ngẩng mắt lên phố; "Goodnight, old street."; **98,1–98,8 cười buồn + mắt chùng + dừng** |
| s37w | 98,8–101,6 | WS · 28 | như Cổng 5 | Ida tay trái nắm van; Cas cạnh chân thang, hai tay nắm thanh |
| s39 | 101,6–106,0 | CU · 85 | nghiêng **96°**, 0,95 m, tĩnh | nghẹn, cúi 12° nhìn xuống Cas; "Just…" 102,32; nuốt 103,2–103,6; "keep a little dark for the ones" 103,86–106,0 |
| s38 | 106,0–107,4 | MS · 50 | (8,75; 2,45; −3,55) → (8,36; 0,95; −4,60) | Cas nắm thanh (IK), ngửa, chớp 106,62, mày trong nâng dần |
| s40 | 107,4–110,0 | CU insert · 50 | phía phố, ngang lồng đèn | tay trái nắm **cần van** (IK điểm) gạt 107,7–108,3; (v2, N1/N14 — số thật) 109,08 → 109,32 bà cúi 16° + quay mặt 80° khỏi máy (thân 16°); mặt còn thấy ở khung 2620 (109,17, quay 26°), **khuất ở khung 2621 (109,21) = khung lửa tắt**; kính tối đục (v1: 108,75 → 109,20, cúi 30°, quay 72°, khuất từ 108,94) |
| s40w | 110,0–112,0 | WS · 28 | như s37w | **G10:** 0–0,35 s tay rời van; 0,35–1,55 s xuống thang; 1,55–2,0 s chạm đất, quay về Cas, đèn sang tay phải. Cas buông thang 1,55–1,9 s |
| s41 | 112,0–113,5 | WS · 28 | nhìn (8,2; 1,15; −4,9) | Ida (7,95; −5,00), Cas (8,50; −4,85) — **cách 0,57 m** (Cổng 5: 1,02 m); trao như bảng đèn lồng |
| s42a | 113,5–115,5 | MS · 45 | như Cổng 5 | Ida **nhìn xuống Cas**: cổ 24° + thân 4° + nhãn cầu 0,12 rad |
| s42b | 115,5–117,5 | WS · 32 | như Cổng 5 | hai tay nắm vòng quai (IK) tới 1,75 s, buông tới 2,0 s |
| s42 | 117,5–120,5 | MS · 40 | như Cổng 5 | mỗi nhịp đếm lòng tay Cas về hai mặt kính (4 cm, trộn 0,8) |

**Vị trí Cas giữ thang (G10):** `CAS_LAD` (8,40; −4,62), hướng −0,6 rad, cạnh chân thang phía **đông**; tay phải nắm thanh đông ở 1,00 m, tay trái ở 0,74 m. Lối trèo (mặt dưới thang, −z) trống → bà xuống thang không xuyên qua cậu. Áp dụng s35 (từ 3,05 s), s36–s40w.
**Ida trên thang:** gốc (8,0; 1,55; −4,38) (Cổng 5: z −4,48) — nhích sát cột 0,1 m để tay trái tới van (vai → thân van ≈ 0,5 m).
**Mũ (G2):** hat_back 0,35 liên tục s36 (sau 1,05 s) → s42 (2,2 s).


## Cổng 6 · W2 v2 (rà continuity + kiểm mù layout-v17)
| Mục | Sửa v2 |
|---|---|
| N1 s40 | xem bảng trên: mặt khuất ở khung 2621 (lửa tắt); cúi giảm 30° → 16° (mũ không còn "lơ lửng") |
| N2 s40w → s41 | cuối s40w: Cas buông thang, bước tới `CAS_41` (8,50; −4,85), quay về bà; bà ở `IDA_41` (7,95; −5,00) cầm đèn tay phải nhấc về phía cậu (`IDA_LIFT`) = đúng tư thế mở s41 |
| N3 s40w | xuống TỪNG BẬC: 4 bậc × 0,3 s (75 % đi, 25 % dừng), thân thẳng nghiêng vào thang 5°, chân so le; tay nắm hai thanh (IK) khi gốc < 0,9 m |
| N5 s42b | Ida đứng ở miệng vòm (1,25; 5,25) trong khung, dõi theo cậu (quay 0,35 rad trong 1,4 s) — nối s42 |
| N6 s33 | quỳ có hạ gốc (`kneelOf`) → đứng dậy thấy được 0–0,7 s; đi từ 0,7 s |
| N8 s37b/s39 | tay trái nắm ống khí thấp hơn 0,12 m dưới tâm van → ra khỏi khung CU; s39 máy hạ 0,12 → 0,03 m |
| N4 | không sửa (gắn Đ6, chờ chủ dự án) |
