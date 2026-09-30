# BÁO CÁO W1-v3 — Cổng 6, sửa nhỏ sau kiểm mù vòng 2 (layout v21)

Phiên xưởng W1 · nhánh `cong6-w1-v3` (từ `f2ec9f3`) · 30/09/2026 · căn cứ: lệnh W1-v3 của P (chủ dự án duyệt, AUTHORSHIP "Cổng 6 — diễn hoạt"); `kiem-mu-v2/CHAM-W1-V2.md`, `continuity/RA-W1-V2.md`.
Chỉ sửa `design/cong5/layout/shots_w1.js` (s05, s22, s24, s24c) và thư mục `reports/m2/cong6/w1/sua-v3/`. Không đổi mặt, ánh sáng, thân Cas, mã dùng chung, tài sản khoá. Không chạy kiểm mù / luật.

## 1. Bảng việc a–e
| Mục | Trạng thái | Làm gì · số đo |
|---|---|---|
| **a** s05 bàn tay phải "vuốt", "trôi" 3,0–3,5 s | **Đã sửa** | Tay riêng của s05 (không đụng `S05.hands` dùng chung với s24): xoè 0 / gập **0,62** (v2 xoè 0,3 / gập 0,3). Thử gập 0,42: ngón vẫn gần thẳng (bộ tay MPFB khoá ngón khi va chạm lồng/cột) — không đổi so v2 → loại. Với 0,62 bàn tay khum, ngón khép (`can_s05_tay.jpg`, 12,5 / 13,5 s). "Trôi" 3,0–3,5 s: v2 tay hạ xuống nắm thanh móc ngay mép dưới khung → mẩu bàn tay rời ở mép. Nay tay nghỉ nắm **thân cột thấp** (phải y 2,20 m, trái 2,30 m, nắm hẳn gập 0,85) → ra khỏi khung từ ≈ 2,8 s (`can_s05_tay.jpg`, 15,0 / 15,4 s: không còn tay). |
| **b** s22 mũ xê dịch, chân tóc lùi | **Đã sửa bằng đặt mũ + tư thế đầu trong shot** | Gốc: mũ là con của khối đầu (`hatPivot` trong `headG`, cast3d) — không trễ, không dịch so với đầu. Cảm giác "mũ lơ lửng, lộ tóc, hói" do đầu NGẨNG 14° ở 1,6–2,4 s trước máy tĩnh thấp ngang mắt: thấy mặt dưới vành và vùng trán/chân tóc dưới vành. Sửa trong shot: `hat_back` **−0,35** (vành chúc trước ≈ 5°, che chân tóc) và ngẩng **−8°** thay −14°. Không sửa mô hình tóc/mũ. `can_s22_mu-toc.jpg` (51,5 / 51,75 / 52,0 s): vành phủ trán tới chân tóc cả lúc ngẩng. |
| **c** s24c quả bông lún tường (K2); khe cổ | **Đã sửa (chỉ s24c)** | Đầu CÚI nhẹ (cổ **+10°**, nghiêng 3°) thay ngả tựa −9°/5° — quả bông cách xa tường, thấy **suốt 36 khung** (v2 mất từ khung 1391); cằm khép lên cổ áo lật (hết khe). Chỗ đứng, thân, tay, máy giữ nguyên v2 (s23, s24 dùng chung tư thế thân Cas: không đổi — s23 lệch 0 px). Thân phồng: giữ nguyên theo lệnh. `can_s24c_qua-bong-co.jpg`. |
| **d** s24 đếm ba (L4) | **Đã sửa** | Ba nhịp tách bạch có dừng: mỗi nhịp khép 0,12 s → **giữ áp kính 0,12 s** → mở 0,18 s; giữa hai nhịp tay dang yên ≈ 0,18 s (v2: gauss 0,16 s liền). Lòng tay nâng lên ngang lồng kính L11 (gập vai −118° khi dang / −130° khi áp; v2 −86/−100). **Đo (chiếu tâm lòng tay trái lên khung 960×540, cùng máy s24):** ở mỗi nhịp 55,70 / 56,30 / 56,90 s so với lúc nghỉ +0,3 s: **v3 Δngang 29,6 / 29,7 / 29,7 px, Δdọc 8,1 / 8,1 / 8,7 px** (v2: 29,9 / 29,4 / 29,9 và 6,1 / 6,3 / 6,9 px). Độ cao lòng tay lúc áp: **cao hơn đáy lồng ≈ 20–21 px** (v2: thấp hơn đáy lồng 6–7 px theo phép chiếu của tôi; continuity đo 40–47 px — khác mốc đáy lồng, cùng chiều). `can_s24_ba-nhip.jpg`. |
| **e** Lệch 0 px mọi shot khác, kể cả W2 | **Đạt** | §2. |

## 2. Lệch 0 px toàn phim (53 shot, 159 ảnh)
- Gốc: ảnh dò v2 (`/var/tmp/cine-out/W1/lech0v2/sau`, mã v2 `56b834a`; chỉ s24c khác mã hiện hành vì lượt lia 9° → dò lại riêng s24c từ `f2ec9f3`), gộp ở `…/lech0v3/goc`.
- Sau: mã `1c903b1`, `…/lech0v3/sau` (lượt dò bị dừng khi container khởi động lại sau s40w → dò nốt s41–s48 vào `…/lech0v3/sau-b`, gộp, so bằng cùng phép so của `do_lech_0px.sh`).
- **Kết quả: 159 ảnh; lệch 12 — đúng 12 ảnh của 4 shot cố ý đổi (s05, s22, s24, s24c).** s23 (dùng chung tư thế thân Cas) và **30 shot W2: 0 px.**

## 3. Render, mp4 hiện hành
- `v3-render` (hàng đợi W1, chờ 182 s sau luật v21 của P, chạy 1 214 s): s05 96 · s22 72 · s24 48 · s24c 36 khung. Lượt render đầu bị dừng khi container khởi động lại (mp4 dở, không có timing) — đã render lại.
- **MP4 hiện hành theo shot** (`/var/tmp/cine-out/W1/`, 960×540, có `timing_*.json`):

| Shot | MP4 |
|---|---|
| s05, s22, s24, s24c | `video_s05-s22-s24-s24c.mp4` (v3) |
| s03, s06, s13, s15, s23 | `video_s03-s05-s06-s13-s15-s22-s23-s24-s24c.mp4` (v2; s05, s22, s24, s24c trong tệp này là bản cũ) |
| s02, s04, s07, s08 | `video_s02-s03-s04-s05-s06-s07-s08.mp4` (v1) |
| s09w, s11, s12 | `video_s09w-s11-s12-s13-s14.mp4` (v1) |
| s14 | `video_s14.mp4` (v1) |
| s19, s21 | `video_s15-s19-s21-s22-s23-s24-s24c.mp4` (v1) |
| s01, s09, s10e, s10 | bản Cổng 5 (P giữ) |
| W2 | không đổi |

- Bảng khung 0,5 s: `sua-v3/<shot>_truoc.jpg` (từ mp4 v2 hiện hành) và `_sau.jpg` cho s05, s22, s24, s24c; ảnh cận `can_s05_tay.jpg`, `can_s22_mu-toc.jpg`, `can_s24_ba-nhip.jpg`, `can_s24c_qua-bong-co.jpg` (hàng trên v2, hàng dưới v3).

## 4. Rủi ro
- s05: tay khum khi hơ gần lồng có thể đọc thành "nắm hờ" hơn là "áp lòng tay"; tay không còn thấy sau khi hạ (chủ ý).
- s22: vành mũ thấp hơn → bóng vành phủ mắt nhiều hơn ở đầu shot.
- s24c: đầu cúi nhẹ — cậu nhìn về Ida hơi từ dưới lên; "dựa tường" đọc nhờ lưng + bóng, không còn đầu tựa tường.

## 5. Token, thời gian
- Thời gian thật: 16:41 → ≈ 17:50 UTC 30/09/2026 (gồm một lần container khởi động lại).
- Token lượt W1-v3: bộ đếm công cụ ≈ 50 nghìn (hạn 150 nghìn).
