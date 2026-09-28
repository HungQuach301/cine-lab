# Continuity sheet — Cảnh 5 "Ngọn cuối" (1:20,00–2:00,50 · s33 → s42)

Gói W2, Cổng 5, luật O1. Nguồn số: `shots_w2.js` (`BAY`, `CAS_LAD`, `CAS_BAY`, `casHug`, `placeBayLantern`), `sets2.js` (`addBayStreet`), `sets_end.js` (`END`).
Bản v3 (rà continuity v2 — C5, N2, N3, N7, N9): mốc thời gian theo bảng thời gian hiện hành (s33 5,0 s; tổng phim 140,5 s); chỉ ghi những gì có trên hình. Ảnh 4 kiểm mù: khung toàn cục **2510** (khung 72 của s39, 104,58 s — chữ "dark").
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
| s37, s37w, s39, s38, s40, s40w | 0,35 | 0,35 | |
| s41, s42a | 0,35 | 0,35 | |
| s42b | — | — | Ida không có trong khung |
| s42 | 0,35 | **0** | 1,9–2,2 s tay trái lên vành; **2,2–2,8 s kéo vành xuống (0,35 → 0)**; 2,8–3,0 s hạ tay, quay người +0,5 rad (rời khỏi vòm) |
| s43 → s48 | 0 | 0 | cảnh 6 |

## Đèn lồng — ai giữ, cầm thế nào (N2, N7)
| Shot | Chủ | Cách cầm / vị trí |
|---|---|---|
| s33, s34 | — | trên nền đá hốc cửa, `BAY.lan` (0,2; 3,0) |
| s35 → s40w | Ida | móc **hông trái**, cháy (nhặt lại khi rời hốc — ngoài hình, giữa s34 và s35) |
| s41 | Ida → Cas | Ida tay phải (0 s) → chìa ra (0,5 s); Cas đón bằng hai tay, **ôm sát ngực** (`casHug`, 0,7 s) |
| s42a | Cas | `casHug`: hai khuỷu gập sát, hai cổ tay trước ngực, đèn áp bụng |
| s42b | Cas | `casHug` khi đi (0–1,45 s); 1,6–2,0 s hạ đèn xuống nền trước mặt (−0,38; 3,10) |
| s42 | Cas | trên nền đá trước mặt Cas (−0,38; 3,10) |

## Lịch (giây phim)
| Sự kiện | Mốc |
|---|---|
| L4 bắt đầu (đầu s37) | 93,00 (1:33,0) |
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
- **Ida:** `faceRest` (`hat_back` 0,35), sad_smile, nhìn lên phố (phải khung).

## s37w · 1:38,80–1:41,60 · WS 28 mm · tĩnh
- **Máy:** (17; 1,6; 1,2), nhìn (8,8; 3,6; 0,6). Khung: mặt cuối phố + phố rẽ (giữa-trái), hông + hốc cửa (phải), L11 + thang + hai người (phải), P5 (trái, bóng đèn trong khung).
- **Đèn:** P5 bật 1:39,2 (nhấp 2, đứng 1:39,64) → trắng tràn góc (0,06 → 1,10); bóng dài tan; L11 nhạt về 0,35.
- **Ida:** `faceRest` trên thang. **Cas:** giữ thang, ngửa.

## s39 · 1:41,60–1:46,00 · CU 85 mm · tĩnh (khung ảnh 4 kiểm mù: khung 72 = toàn cục 2510)
- **(c) Thứ tự mới:** s39 đứng trước s38 để câu cuối L4 BẮT ĐẦU trên mặt Ida ("Just…" 1:42,33 là 0,73 s sau đầu shot) và kéo qua "…keep a little dark for the ones".
- **Máy:** `faceCam` cách 0,95 m, gần chính diện.
- **Đèn:** trắng phẳng + L11 nhạt; `facelight` `elec`; phơi sáng × 0,8. Vành mũ đổ bóng lên trán; tường vôi sau lưng sáng xám.
- **Ida:** choked, nhìn lên phố (phải khung).

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
