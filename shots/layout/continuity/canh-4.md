# Continuity sheet — Cảnh 4 "Bức tường" (0:59,00–1:20,00 · s25 → s32)

Gói W2, Cổng 5, luật O1. Nguồn số: `design/cong5/layout/shots_w2.js` (hằng số `CAS_W`, `IDA_W`, `IDA_K`, `LAN_T`, `CAS_S32`), `sets2.js` (`WALL`), `sets_end.js` (`END`, `wallFromWorld`).

## Hệ toạ độ và địa lý (chốt ở Cổng 5)
- Bộ cảnh 4 là **bộ tường chim** (`sets2.buildWallSet`). Hệ của nó = **hệ tường chim** của `sets_end.js`: tường = **hông nam nhà kho** ở z = 0, nhìn +z (nam).
- Đổi sang toạ độ bộ phố của W1: x = x_w + 10,2; z = z_w − 8,1. Hai bộ cùng **một** địa lý (cùng hàm `buildEndWallFrame`).

| Mốc | Hệ tường chim (x_w; z_w) | Bộ phố (x; z) |
|---|---|---|
| Chỗ Cas làm chim (`casSpot`) | (0,15; 0,95) | (10,35; −7,15) |
| L11 (đèn khí, cao 3,4 m) | (−2,2; 4,2) | (8; −3,9) |
| Hốc cửa bốc hàng (tâm, rộng 3,2 m, sâu 4 m) | (−8,0; 0) | (2,2; −8,1) |
| Góc trong nhà kho (hông gặp mặt cuối phố) | (−15,2; 0) | (−5; −8,1) |
| Đầu hồi căn đầu dãy bắc | x_w = 4,8 | x = 15 |
| Mặt tiền dãy bắc / dãy nam | z_w = 2,5 / 13,7 | z = −5,6 / +5,6 |
| Cột điện phố chính (bật 1:04) | (3,3; 3,9) | (13,5; −4,2) — có ở **cả hai bộ** (W1 đã thêm vào bộ phố: thấy thân tối ở s23, s24; ánh của nó chưa có ở các shot bộ phố cảnh 5 — mâu thuẫn C2, chờ chủ dự án) |
| Cột góc P5 (đoạn cáp cuối) | (0,6; 12,0) | (10,8; 3,9) — ngoài khung mọi shot cảnh 4 |

- Khoảng cách: Cas → tường 0,95 m; Cas → L11 4,0 m; L11 → tường 4,2 m; Cas → hốc cửa 8,15 m (bên TRÁI Cas khi nhìn vào tường).
- **Trục 180° cảnh 4:** đường Ida–Cas (Ida ở `IDA_W`, Cas ở `CAS_W`). Mọi máy ở phía +x của đường này (sau-phải hai người): **Ida TRÁI, Cas PHẢI**; Ida nhìn sang phải khung về Cas; Cas quay lại nhìn sang trái khung về Ida (s29).

## Trạng thái đầu cảnh 4 giả định từ s24c (W1) — để P kiểm chỗ nối
| Mục | Giả định của W2 ở 0:59,00 | Khớp W1 `canh-3.md` |
|---|---|---|
| Giờ | ~8:0x; đồng hồ bỏ túi trong túi Ida | Khớp |
| L11 | vừa thắp (54,5 s), sáng đủ; nguồn ấm duy nhất của góc | Khớp |
| Cột điện | Phố chính đã trắng; cột phố chính cạnh nhà kho **tắt tới 1:04,40**; P5 tắt | Khớp (P5 tắt) |
| Ida | Vừa **xuống thang L11** (s25 ngoài hình), đứng ở phố chính `IDA_W` (−3,8; 7,3) → bộ phố (6,4; −0,8), cách L11 3,5 m | W1 để bà trên thang ở 0:59,00: cần một nhịp xuống thang ngoài hình trong s25 (3 s) — **P kiểm** |
| Đạo cụ Ida | Đèn lồng **cháy**, ở **hông trái** (móc thắt lưng). **Thang tựa L11 phía bắc**: bộ tường chim đặt thang ở (−2,2; 3,35) nghiêng 0,36 rad (= `ladderAt(11)` bộ phố) — có mặt suốt cảnh 4 (sửa C1: s27 bản đầu thiếu thang). Sào mồi ngoài hình. Đồng hồ trong túi | Khớp |
| Trang phục Ida | Mũ #262a33, `hat_back` = 0; khăn một đuôi trước ngực | Khớp |
| Cas | Ở `casSpot`. **s24c: nhìn về Ida / L11 (TRÁI khung)** → s25: đã quay vào tường, giơ tay làm chim | Khớp `canh-3.md` và hình; chuyển hướng qua cắt — hợp lý |
| Trang phục Cas | Mũ len kem có quả bông đỏ, áo len đỏ quá khổ | Khớp |

## Lịch ánh sáng cảnh 4 (giây phim)
| Sự kiện | Mốc |
|---|---|
| Cột điện phố chính cạnh nhà kho bật (`WALL_POST_ON` = T0.s27 + 0,4) | 64,40 (1:04,4) — nhấp 2 lần, đứng trắng ở 64,84 |
| Chim bóng L11 tan (luật 3.3: 12 khung) | 64,40 → 64,84 (≈ 11 khung) |
| Ida mở cửa đèn lồng (mức đèn lồng tăng) | 73,0 → 73,9 (s30) |
| L3 "Go on, then." | 74,00 (đầu s31) |

Tỷ lệ tràn điện trên tường (sau 64,84): `whiteHemi` 1,8 + cột 60 cd × 0,65 (fillK = 1, **mọi shot cảnh 4 cùng mức**) → chim L11 biến mất hẳn (s28 kiểm bằng probe).

## s25 · 0:59,00–1:02,00 · MS 45 mm · dolly vào 0,3 m
- **Máy:** (2,2; 1,3; 3,6) → (2,0; 1,3; 3,3), nhìn (0,3; 1,1; 0). Sau-phải Cas.
- **Đèn:** L11 key có bóng; cột điện tắt. **Nguồn sáng:** L11.
- **Cas:** `CAS_W`, yaw π + 0,15 (mặt vào tường), chim 5B vỗ 1,0 Hz. Nhìn: tường (bóng chim).
- **Ida:** ngoài hình, ở `IDA_W` (vừa xuống thang). Đèn lồng hông trái, cháy.
- **Hậu cảnh:** tường vôi hông nhà kho; ống thoát nước ở trái khung.

## s26 · 1:02,00–1:04,00 · MS 50 mm · tĩnh
- **Máy:** (−2,1; 1,5; 6,55), nhìn đầu Ida (lệch 0,05; −0,04). 3/4 trước-phải bà, phía +x đường Ida–Cas.
- **Đèn:** L11 cách mặt bà 3,5 m, **gần chính trước mặt** (lệch ≈ 4°), góc ngẩng ≈ 25° → key trước lên mặt, vành mũ che trán. `facelight` chế độ `gas` (W3): fill 0,20, under 0,12, rim 0,22 × độ rọi L11 tại mặt (probe: key 0,59–0,62, tổng 0,78–0,82). Phơi sáng 3,4. Đèn lồng thắt lưng 0,012 (đóng cửa).
- **Ida:** `IDA_W` (−3,8; 7,3), đứng (turnaround + cổ 4°), mặt về Cas. Mũ `hat_back` 0. Đèn lồng hông trái cháy.
- **Cas:** ngoài hình (chim vẫn vỗ).
- **Nhìn:** Ida nhìn **phải khung** (về Cas).
- **Hậu cảnh:** mặt tiền dãy nam đã trắng (trái khung), mặt cuối phố + phố rẽ tối (phải khung).

## s27 · 1:04,00–1:07,00 · WS 21 mm · tĩnh
- **Máy:** (6,4; 0,85; 12,5), nhìn (0,6; 3,6; 1,0). Thấp, hất lên, từ vỉa hè nam phố chính.
- **Đèn:** cột điện (3,3; 3,9) bật 1:04,4 (nhấp 2 lần, đứng); L11 còn cháy nhưng chìm. Phơi sáng 2,6 → 1,1.
- **Khung:** hông nhà kho (gờ mái, máng nước, cửa sổ cao, cửa kéo hàng + xà tời phía trên **hốc cửa ở trái khung**), L11, Cas nhỏ ở chân tường, cột điện + bóng đèn, đầu dãy bắc (phải). Ida đứng xem ở trái-giữa khung.
- **Cas:** vỗ chim; chim nhạt dần ~11 khung.
- **Ida:** `IDA_W`, đứng xem.

## s28 · 1:07,00–1:09,00 · MS 45 mm · tĩnh
- **Máy:** (2,2; 1,3; 3,6), nhìn (0,3; 1,1; 0).
- **Đèn:** trắng phẳng (fillK 1). **Không còn bóng chim** (probe xác nhận).
- **Cas:** vỗ 2,1 Hz, biên độ 1,8×. **Ida:** `IDA_W` (ngoài hình).

## s29 · 1:09,00–1:12,00 · MCU 85 mm · tĩnh
- **Máy:** (1,7; 1,1; 2,8), nhìn (0,1; 1,05; 1,0).
- **Cas:** 0–0,8 s hạ tay; 0,9–1,9 s xoay từ yaw π + 0,15 sang hướng Ida; 2,0 s cúi nhìn đèn lồng (cổ 16°). **Nhìn: trái khung** (về Ida), rồi xuống (đèn lồng ở hông bà — ngoài hình).
- **Ida:** `IDA_W` (ngoài hình), đèn lồng hông trái cháy.

## s30 · 1:12,00–1:14,00 · MS 35 mm · tĩnh
- **Máy:** (2,6; 1,4; 4,0), nhìn (−0,1; 0,8; 0,7).
- **Ida:** 0–0,7 s đi từ (−1,3; 1,85) tới `IDA_K` (−0,75; 0,75) [cắt nén: từ `IDA_W` tới đây ngoài hình]; 0,95 s tay phải tháo đèn lồng (đạo cụ: hông trái → **tay phải**); 1,05–1,85 s quỳ một gối (`crouch_lantern` + tay phải đưa đèn ra trước — tư thế cục bộ `kneelHold`); 1,2–1,85 s đèn tới `LAN_T`.
- **Đèn lồng:** mở cửa, mức 0,012 → 3,0 (0,95–1,9 s). Vỏ đèn không tự che nguồn (sửa lỗi v2).
- **Cas:** `CAS_W`, quay về Ida (cổ 22°).

## s31 · 1:14,00–1:17,00 · MCU 85 mm · tĩnh
- **Máy:** đầu Ida + (1,6; 0,05; 1,25) → ≈ (0,7; 1,1; 1,8), nhìn đầu Ida. 3/4 trước-phải bà, đầu Cas không che.
- **Thoại:** L3 "Go on, then." ở 1:14,0.
- **Ida:** quỳ (`kneelHold`), đầu quay −24° về Cas; biểu cảm sad_smile. Đèn lồng **tay phải**, ở `LAN_T` (−0,22; 0,64; 0,60) — cách tường 0,6 m.
- **Nhìn:** Ida nhìn phải khung (về Cas).

## s32 · 1:17,00–1:20,00 · WS 35 mm · tĩnh
- **Máy:** (1,9; 1,35; 4,1), nhìn (−0,25; 1,45; 0).
- **Cas:** 0–0,7 s quay lại tường; 0,2–0,9 s nhích tới `CAS_S32` (0,15; 0,74); từ 0,8 s chim vươn tay (`birdReach`, vai −92°, khuỷu −12°) — cổ tay ở z ≈ 0,35–0,36.
- **Đèn lồng:** `LAN_T`, cao 0,64 m (dưới tay Cas 0,98 m), cách tường 0,60 m, cạnh hông trái Cas — thân Cas ở SAU đèn nên không đổ bóng thân lên tường; chim phóng đại ≈ 0,60 / 0,25 ≈ 2,4×, to, mềm, ấm.
- **Ida:** quỳ, giữ đèn (tay phải), đầu quay −10°.

## TRẠNG THÁI Ở KHUNG CUỐI s32 (1:20,00) → nối s33 (cảnh 5)
| Mục | Trạng thái |
|---|---|
| Ida | Quỳ cạnh Cas, đèn lồng tay phải (mở cửa) |
| Cas | Đứng sát tường, tay làm chim |
| Đèn | Cột điện phố chính sáng; L11 cháy (chìm); P5 tắt |
| s33 cần | Ida **đặt đèn lồng xuống nền** trong hốc cửa (8 m bên trái) — cắt nén: hai người đã đi tới hốc |
