# Continuity sheet — Cảnh 4 "Bức tường" (0:59,00–1:20,00 · s25 → s32)

Gói W2, Cổng 5, luật O1. Nguồn số: `design/cong5/layout/shots_w2.js` (hằng số `DX`, `CAS_W`, `IDA_W`, `IDA_K`, `LAN_T`, `LAN_K`, `CAS_S32`, `BIRD_CAM`), `sets2.js` (`WALL`), `sets_end.js` (`END`).
Bản v3 (rà continuity v2 — N6, N9): mọi bảng dưới đã mang số sau A2/B1 (không còn phần "cộng 3,95 m"); chỉ ghi những gì có trên hình.

## Quyết định đang áp dụng
- **B1 (chủ dự án sau Cổng 5, AUTHORSHIP @2591e4d):** cột điện phố chính đặt TRONG SÂN trước hông nhà kho, chân (17,0; −5,9) bộ phố; tay vươn về tường; PointLight tầm **8,5 m**, suy giảm 1,2, không bóng. Góc L11 và hốc cửa ngoài tầm → **tối tới khi P5 bật (1:39,2)**. (P đề xuất (15,4; −6,2) — điểm đó nằm trong căn đầu dãy bắc cũ; W2 dời dãy bắc tới x = 18,5 và đặt cột ở (17,0; −5,9).)
- **N6 (P chọn, rà continuity v2):** đèn lồng của Ida **cháy liên tục** từ s23 tới lúc tháo ở s30; **không có nhịp mở/đóng cửa đèn**. Ở thắt lưng (hông trái) kính đèn sáng, nhưng hắt lên tường và nền rất yếu (mức 0,012) vì đèn treo thấp ở hông khuất sau thân và vạt áo bà. s30 chỉ là nhịp **tháo đèn**: hắt sáng tăng liên tục (không bật cóc) khi đèn ra khỏi thân bà và hạ sát tường.

## Hệ toạ độ và địa lý
- Bộ cảnh 4 là **bộ tường chim** (`sets2.buildWallSet`). Hệ của nó = **hệ tường chim** của `sets_end.js`: tường = **hông nam nhà kho** ở z = 0, nhìn +z (nam).
- Đổi sang toạ độ bộ phố của W1: x = x_w + 10,2; z = z_w − 8,1. Hai bộ cùng **một** địa lý (cùng hàm `buildEndWallFrame`).

| Mốc | Hệ tường chim (x_w; z_w) | Bộ phố (x; z) |
|---|---|---|
| Chỗ Cas làm chim (`casSpot` = `CAS_W`) | (4,1; 0,95) | (14,3; −7,15) |
| L11 (đèn khí, cao 3,4 m) | (−2,2; 4,2) | (8; −3,9) |
| Ida đứng xem (`IDA_W`) | (−3,8; 7,3) | (6,4; −0,8) |
| Hốc cửa bốc hàng (tâm, rộng 3,2 m, sâu 4 m) | (−8,0; 0) | (2,2; −8,1) |
| Góc trong nhà kho (hông gặp mặt cuối phố) | (−15,2; 0) | (−5; −8,1) |
| Đầu hồi căn đầu dãy bắc | x_w = 8,3 | x = 18,5 |
| Cột điện phố chính trong sân (bật 1:04,4) | (6,8; 2,2) | (17,0; −5,9) — bản cột cũ (13,5; −4,2) của W1 bị ẩn trong shot W2 |
| Cột góc P5 (đoạn cáp cuối) | (0,6; 12,0) | (10,8; 3,9) — ngoài khung mọi shot cảnh 4 |

- Khoảng cách: Cas → tường 0,95 m; Cas → L11 7,1 m; L11 → tường 4,2 m; Ida → L11 3,5 m; Cas → hốc cửa 12,1 m (bên TRÁI Cas khi nhìn vào tường); đầu đèn cột → tường sau lưng Cas 5,2 m, → lửa L11 9,5 m.
- **Trục 180° cảnh 4:** đường Ida–Cas (Ida ở `IDA_W`, Cas ở `CAS_W`). Mọi máy ở phía +x của đường này (sau-phải hai người): **Ida TRÁI, Cas PHẢI**; Ida nhìn sang phải khung về Cas; Cas quay lại nhìn sang trái khung về Ida (s29).

## Trạng thái đầu cảnh 4 giả định từ s24c (W1) — để P kiểm chỗ nối
| Mục | Giả định của W2 ở 0:59,00 | Khớp W1 `canh-3.md` |
|---|---|---|
| Giờ | ~8:0x; đồng hồ bỏ túi trong túi Ida | Khớp |
| L11 | vừa thắp (54,5 s), sáng đủ; nguồn ấm duy nhất của góc | Khớp |
| Cột điện | Phố chính đã trắng; cột trong sân **tắt tới 1:04,40**; P5 tắt | Khớp (P5 tắt) |
| Ida | Đã **xuống thang L11** (ngoài hình), đứng ở `IDA_W` | W1 để bà trên thang ở 0:59,00: nhịp xuống thang ngoài hình — **P kiểm** |
| Đạo cụ Ida | Đèn lồng **cháy liên tục** (N6), ở **hông trái** (móc thắt lưng). **Thang tựa L11 phía bắc**: (−2,2; 3,35) nghiêng 0,36 rad (= `ladderAt(11)` bộ phố) — có mặt suốt cảnh 4. Đồng hồ trong túi | Khớp (W1 s23–s24c: đèn hông trái sáng) |
| Trang phục Ida | Mũ #262a33, `hat_back` = 0; khăn một đuôi trước ngực | Khớp |
| Cas | Ở `casSpot`. **s24c: nhìn về Ida / L11 (TRÁI khung)** → s25: đã quay vào tường, giơ tay làm chim | Khớp; chuyển hướng qua cắt |
| Trang phục Cas | Mũ len kem có quả bông đỏ, áo len đỏ quá khổ | Khớp |

## Lịch ánh sáng cảnh 4 (giây phim)
| Sự kiện | Mốc |
|---|---|
| Cột điện trong sân bật (`WALL_POST_ON` = T0.s27 + 0,4) | 64,40 (1:04,4) — nhấp 2 lần, đứng trắng ở 64,84 |
| Chim bóng L11 tan (luật 3.3: 12 khung) | 64,40 → 64,84 (≈ 11 khung) |
| Ida tháo đèn lồng; hắt sáng đèn lồng tăng liên tục 0,012 → 3,0 (đèn ra khỏi thân bà rồi hạ sát tường) | 72,80 → 73,85 (s30 0,8–1,85 s) |
| L3 "Go on, then." | 74,00 (đầu s31) |

Tràn điện trên tường sau 64,84: vũng sáng cột trong sân (tầm 8,5 m, suy giảm 1,2) + tràn nền 0,054 (= mức góc tối bộ phố); **mọi shot cảnh 4 cùng mức** (fillK = 1) → chim L11 biến mất hẳn (s28, probe).

## s25 · 0:59,00–1:02,00 · MS 45 mm · dolly vào 0,3 m
- **Máy:** (6,15; 1,3; 3,6) → (5,95; 1,3; 3,3), nhìn (4,25; 1,1; 0). Sau-phải Cas. Phơi sáng 3,6.
- **Đèn:** L11 key có bóng; cột điện tắt.
- **Cas:** `CAS_W`, yaw π + 0,15 (mặt vào tường), chim 5B vỗ 1,0 Hz. Nhìn: tường (bóng chim).
- **Ida:** ngoài hình.
- **Hậu cảnh:** tường vôi hông nhà kho, nền đá lát.

## s26 · 1:02,00–1:04,00 · MS 50 mm · tĩnh
- **Máy:** (−2,1; 1,5; 6,55), nhìn đầu Ida (lệch 0,05; −0,04). 3/4 trước-phải bà, phía +x đường Ida–Cas.
- **Đèn:** L11 cách mặt bà 3,5 m, **gần chính trước mặt** (lệch ≈ 4°), góc ngẩng ≈ 25° → key trước lên mặt, vành mũ che trán. `facelight` chế độ `gas` (W3). Phơi sáng 3,4. Đèn lồng ở hông cháy, hắt rất yếu (0,012 — N6).
- **Ida:** `IDA_W`, đứng (turnaround + cổ 4°), mặt về Cas. Mũ `hat_back` 0.
- **Nhìn:** Ida nhìn **phải khung** (về Cas).

## s27 · 1:04,00–1:07,00 · WS 21 mm · tĩnh
- **Máy:** (−1,0; 0,85; 13,0), nhìn (1,2; 3,0; 1,0). Thấp, hất lên, từ vỉa hè nam.
- **Đèn:** cột trong sân bật 1:04,4 (nhấp 2 lần, đứng); L11 còn cháy nhưng chìm. Phơi sáng 3,6 → 1,1 theo công tắc.
- **Khung (trái → phải):** hốc cửa, Ida đứng xem, L11 + thang, tường chim với Cas nhỏ ở chân tường, cột điện + bóng đèn, đầu dãy bắc.
- **Cas:** vỗ chim; chim nhạt dần ~11 khung.

## s28 · 1:07,00–1:09,00 · MS 45 mm · tĩnh
- **Máy:** `BIRD_CAM` (6,15; 1,3; 3,6), nhìn (4,25; 1,1; 0).
- **Đèn:** trắng phẳng (fillK 1). **Không còn bóng chim** (probe xác nhận).
- **Cas:** vỗ 2,1 Hz, biên độ 1,8×. **Ida:** ngoài hình.

## s29 · 1:09,00–1:12,00 · MCU 85 mm · tĩnh
- **Máy:** (5,65; 1,1; 2,8), nhìn (4,05; 1,05; 1,0).
- **Cas:** 0–0,8 s hạ tay; 0,9–1,9 s xoay từ yaw π + 0,15 sang hướng Ida; 2,0 s cúi nhìn (cổ 16°). **Nhìn: trái khung** (về Ida), rồi xuống (đèn lồng ở hông bà — ngoài hình).

## s30 · 1:12,00–1:14,00 · MS 35 mm · tĩnh
- **Máy:** (6,55; 1,4; 4,0), nhìn (3,85; 0,8; 0,7).
- **Ida:** 0–0,7 s đi từ (2,65; 1,85) tới `IDA_K` (3,2; 0,75) [cắt nén]; 0,95 s tay phải tháo đèn lồng (đạo cụ: hông trái → **tay phải**); 1,05–1,85 s quỳ một gối (`kneelHold`); 1,2–1,85 s đèn tới `LAN_T`.
- **Đèn lồng (N6):** cháy suốt shot; hắt sáng tăng liên tục 0,012 → 3,0 trong 0,8–1,85 s (đèn ra khỏi thân bà, hạ sát tường) — không có nhịp mở cửa. Vỏ đèn không tự che nguồn.
- **Cas:** `CAS_W`, quay về Ida (cổ 22°).

## s31 · 1:14,00–1:17,00 · MCU 85 mm · tĩnh
- **Máy:** đầu Ida + (1,6; 0,05; 1,25), nhìn đầu Ida. 3/4 trước-phải bà, đầu Cas ở mép phải khung. Phơi sáng 0,45 (bảng phơi sáng cận mặt W3).
- **Thoại:** L3 "Go on, then." ở 1:14,0.
- **Ida:** quỳ (`kneelHold`), đầu quay −24° về Cas; sad_smile. Đèn lồng **tay phải**, ở `LAN_T` (3,73; 0,75; 0,6) — cách tường 0,6 m.
- **Nhìn:** Ida nhìn phải khung (về Cas).

## s32 · 1:17,00–1:20,00 · WS 35 mm · tĩnh
- **Máy:** (5,85; 1,35; 4,1), nhìn (3,7; 1,45; 0).
- **Cas:** 0–0,7 s quay lại tường; 0,2–0,9 s nhích tới `CAS_S32` (4,1; 0,74); từ 0,8 s chim vươn tay (`birdReach`).
- **Đèn lồng:** `LAN_T`, dưới tay Cas, cách tường 0,6 m, cạnh hông trái Cas — thân Cas ở SAU đèn nên không đổ bóng thân lên tường; chim phóng đại lớn, mềm, ấm.
- **Ida:** quỳ, giữ đèn (tay phải), đầu quay −10°.

## TRẠNG THÁI Ở KHUNG CUỐI s32 (1:20,00) → nối s33 (cảnh 5)
| Mục | Trạng thái |
|---|---|
| Ida | Quỳ cạnh Cas, đèn lồng tay phải (cháy) |
| Cas | Đứng sát tường, tay làm chim |
| Đèn | Cột điện trong sân sáng; L11 cháy (chìm); P5 tắt |
| s33 cần | Ida **đặt đèn lồng xuống nền** trong hốc cửa (12 m bên trái) — cắt nén: hai người đã đi tới hốc; góc hốc cửa **tối** (ngoài vũng cột sân) |
