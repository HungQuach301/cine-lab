# PHIẾU-A — BAN-CUOI-T4-A (bản cuối T4 London, phần thử + chuẩn bị) · 26/10/2026

**Nhánh:** `claude/k2c-t4-02-final-a-0pb0bh` (harness; lệnh ghi `k2c-t4-02-final-a`). Báo cáo đủ: `BAN-CUOI-T4-A-BAO-CAO.md`. Phiên KHÔNG tự chấm thay chủ dự án — mỗi mục: đánh ✓/✗ hoặc chọn phương án.

Tệp xem: tờ so E `reports/ban-cuoi-t4-a/e/so-*.jpg` · điểm đứng P1 `p1/to-p1.jpg` · mẫu 1080p `mau/to-mau-6.jpg` (+ 6 khung `mau-*-1080.jpg`) · Omni `omni/to-khung-omni.jpg` + clip `channel-k2/k2c-t4-02/ban-cuoi/omni/clip/*.mp4` · B `channel-k2/k2c-t4-02/ban-cuoi/b/tam/<khung>/l*/ghep.png` (so `render.png`) · ảnh thật `channel-k2/k2c-t4-02/ban-cuoi/that/anh/*.jpg` · M00 mới `m00/M00-moi-a.jpg` · bảng shot `channel-k2/k2c-t4-02/ban-cuoi/BANG-SHOT-v4.md`.

## E1 — Khung E (ảnh nền AI toàn khung 2026, máy CODINH; LUẬT E RULES-LL 1.17.8)

| Khung | Lượt | Mặt nạ "đủ" (mọi toà OSM có tên → 3D) | Mặt nạ "tháp" (toà ≥ 75 m ODN + 5 công trình lịch sử → 3D) | Tờ so | Duyệt |
|---|---|---|---|---|---|
| **P9-2026 ngày** (H5-05a) | 1 | **0 Chặn** (N2P-1…5, N2P-E): lớp (a)-E 13,96 % · 0/255 · N2P-5 nhấp nháy 0,071 (trần 3,28) · (w) 5 "tháp bịa" (3 máy = toà KHÔNG tên có thật trong render, báo nhầm; 2 mô hình = cụm tháp nhỏ xa chân trời trái do AI thêm — thật, nhỏ) | **2 Chặn của mô hình "bờ"** (KN-1, kiểu K1178-D2) — máy 0/255, T9b 0 %, T9c 0; AI kéo mép kè/nước ở dải ≈ 10 × 190 px sát mép dưới khung (ngoài dải bờ 8 px) · N2P-E ĐẠT 0 cảnh báo · N2P-5 0,035 | `e/so-E-P9-ngay-l1.jpg` · `e/so-E-P9-ngay-l1-thap.jpg` · `e/soi-P1-nguoi-P9-goc-bo.jpg` (hàng dưới) | ☐ "đủ" ☐ "tháp" + **ngoại lệ "bờ"** ☐ ✗ |
| **P1-2026 ngày** (đuôi H5-04) | 2 (lượt 1: AI vẽ người trên quảng trường → N2P-4 Chặn, đã sửa) | **0 Chặn**; (a)-E 38,16 %; N2P-5 0,164; (w) 6 tháp bịa mô hình (cụm cao tầng xa phía bắc, ≤ 3 % chiều cao) | **0 Chặn**; (a)-E 28,36 %; N2P-5 0,072; (w) 6 như trên | `e/so-E-P1-ngay-l2.jpg` · `e/so-E-P1-ngay-l2-thap.jpg` | ☐ "đủ" ☐ "tháp" ☐ ✗ |
| **P9-2026 đêm** (H5-07a) — render đêm V2 thật | 1 | **TRƯỢT (g)**: mô hình thấy 1 biểu tượng sáng (chữ/logo) ở toà thường; + 9 báo lớp (a) | **TRƯỢT (g)** cùng lỗi | `e/so-E-P9-dem-4o.jpg` | theo §15 (k): **đêm trượt → giữ 3D** (không cần duyệt) |

**Nhận xét thẳng của phiên (không thay chủ dự án chấm):** E đẹp hơn render rõ ở nhà thường, cây, mái, trời. Điểm yếu: các phần buộc giữ 3D (mái vòm St Paul's thân trắng phẳng + vòm xám; toà tháp kính phẳng) lộ "chất CG" cạnh nền ảnh chụp, nhất là với mặt nạ "đủ" (loang lổ). Đêm: mái vòm 3D không được chiếu đèn pha (AI thì có) — đây là lý do lớn nhất giữ 3D đêm, ngoài lỗi (g). Đề xuất kèm (B-x1 dưới): nâng vật liệu 3D mái vòm + toà tháp có tên trước khi dựng E thật.

## E2 — Shot nào dùng E (trong BẢNG SHOT v4)
| Shot | Đề xuất | Ghi |
|---|---|---|
| **H5-05a** (P9 CODINH 6 s) | **E ngày** (mặt nạ theo E1) | thay tấm nền N2P cũ; bảng v4 khai tạm mặt nạ "tháp" |
| H5-04 (P1 timelapse 1985 → 2026) | **không** (giữ D 3D) | v4 tách H5-04 → P1 4,417 s + M-d H5-04c; tấm P1-2026 chỉ dùng được nếu chủ dự án muốn giữ đuôi CODINH 2026 ≥ 2 s + hoà ≥ 2 s (sẽ bỏ clip H5-04c) — ☐ chọn |
| H5-07a (P9 đêm) | **không** — giữ D 3D (đêm trượt) | |
| M01 (P1 2026 DAY) | không (máy di chuyển; E chỉ CODINH) | đẩy 2D trên tấm E = đề xuất KN-6, chưa dùng |

## P1 — Điểm đứng (C3 c)
| Khung | Hiện tại | Tây 60 m | Tây 80 m |
|---|---|---|---|
| M01 2026 — mái vòm x % | 18,2 | 24,2 | 26,2 |
| H4-05 1940 — mái vòm x % | 18,2 | 24,2 | 26,2 |
| M03 1666 — lửa (x5–x95 %) · % điểm lửa sát mép phải 3 % | 76,6–98,1 · **7,9 %** | 84,3–99,4 · **21,9 %** | 87,0–99,4 · **31,7 %** |
- Dời tây (giữ hướng nhìn, fov 36°) **không** đạt 30 % mà đẩy vòng cung lửa ra mép phải ×2,8–4. Nếu dời: phải dựng lại **16 shot P1 = 157,9 s** (M01–M04, H1-08b, H1-16, H2-05, H2-09, H3-01, H3-06, H4-01a, H4-05, H4-06, H5-04, H5-07b, H5-08).
- Phương án: (a) **giữ điểm hiện tại + C6 4°** (khuyến nghị) · (b) dời 60 m · (c) dời 80 m. ☐ a ☐ b ☐ c
- Ghi: ở khung khởi đầu M03 vòng lửa đã sát mép phải (7,9 % điểm lửa) — M03 có cú DAY nên giữa shot cân lại; nếu chủ dự án thấy chật, xoay ngược về 2° chỉ cho M03/H5-07b là một lựa chọn rẻ (không dựng lại P1 khác) — ☐ muốn thử.

## D/B — Mẫu 1080p bản cuối
| Mẫu | Lớp | Kết quả | Duyệt |
|---|---|---|---|
| M01, H1-08b, H2-10, H3-05, H4-04a, H5-08 | **D 3D** look3 cờ d, spp 4 | `mau/mau-*-1080.jpg`; 14,4–19,1 s/khung/tiến trình (P = 2) | ☐ ✓ ☐ ✗ |
| B-H5-06 (P3 2026 CODINH) | D + **B** ≥ 4 px/m, tỉ số bóng | 36/1 578 nhà (15,0 % khung); BE-MAT-NHA **0 Chặn**, (b) 0/255; (w) 36 cạnh màu mới (lan can/kính AI thêm trên mái — người đọc) | ☐ ✓ ☐ ✗ |
| B-H2-12b (P2 1711) | D + **B** | lượt 2: 93/14 305 nhà (6,9 %); **0 Chặn**, (w) 3 cạnh. Lượt 1 TRƯỢT do **lệnh của phiên** (gán gạch cho Southwark — nơi không cháy năm 1666) | ☐ ✓ ☐ ✗ |
Tự soi: look3 d đỡ "đồ chơi" ở 1666–1940; **đêm 2026 (H5-08) còn yếu**: mái vòm tối, lưới cửa sổ lặp đều. B chỉ chạm ≤ 15 % khung, cải thiện nhà gần, không đổi cảm giác toàn khung.

## A1 — Clip Omni có NHÂN VẬT CÓ TÊN (duyệt TỪNG clip; khung trung/xa; trang phục/dáng theo chân dung tham chiếu)
| Mã | Clip | Nhân vật | Chân dung tham chiếu (SHA trong `dac-ta-v4/log-shot.json`) | YuNet mặt lớn nhất | Kiểm | Duyệt |
|---|---|---|---|---|---|---|
| **H1-06x** (DN03, 6 s, chèn sau H1-06 13,5 s — đúng câu "That afternoon, the King and his brother James… royal barge") | `H1-06x-l1-360p` | Charles II, James Duke of York | met-435943-charles2-cooper · rijks-200221267-james2-loggan | 0 (không phát hiện mặt; người ≈ 3–5 % khung) | Flash ĐẠT · tầng 2 ĐẠT · lớp mốc 3/3 ĐẠT | ☐ ✓ ☐ ✗ |
| **H1-15x** (DN04, 6 s, đặt đúng câu "In the last days… the King and the Duke work the fire-lines") | `H1-15x-l1-360p` | Charles II, James Duke of York | như trên | 0,031 khung (≤ 1/8) | Flash ĐẠT · tầng 2 ĐẠT · lớp mốc ĐẠT | ☐ ✓ ☐ ✗ |
Ghi: hình nhà Vua/Công tước nhỏ, khó nhận ra là ai — đúng P2 (b) "không cận mặt"; nhận diện dựa vào lời + thẻ chữ.

## A — Clip Omni hiện đại (A, mức ĐỦ, lớp công trình mốc)
| Mã | Kết quả | Giây | Duyệt |
|---|---|---|---|
| **H5-04c** cụm toà cao Leadenhall/Bishopsgate từ phố | CHỌN lượt 1 | 6 | ☐ ✓ ☐ ✗ |
| **H5-05d** mái vòm từ sông (2026 chiều) | CHỌN lượt 2 (lượt 1: người đi bộ méo) | 6 | ☐ ✓ ☐ ✗ |
| H5-05b Fleet Street → mái vòm | TRƯỢT 2 lượt thật (+1 lỗi 502 $0): chữ biển số; người méo; **toà cao đứng sau mái vòm — trái câu lời** | — | giữ 3D |
| H5-02b Barbican đang xây · H5-02s London Wall 1976 | **không sinh**: nền 3D sai niên đại (thiếu tháp Barbican 1973; toà kính 2018 trong cảnh 1976) | — | giữ 3D; sửa niên đại 3D ở phiên B (đề xuất) |
**Tổng A = 12 s** (< mục tiêu 30–40 s). Không thêm clip chỉ để đạt con số.

## Điểm nhấn C1 (b) — 6 clip, ≤ 2 lượt: **2/6 đạt** (H1-06x, H1-15x). Trượt (lỗi thật, giữ 3D): H2-02b (cột Monument/mái vòm xuất hiện năm 1666), H2-06b (Monument không có rãnh dọc; biển chữ), H2-09x (cột Monument 1675 dựng trong 3D bị đọc thành "tháp đồng hồ"), H2-10b (cầu thứ hai + tàu lớn năm 1708).

## Ảnh thật hiện đại (B) + C2
| Ảnh | Giấy phép | Dùng | Chú thích | Duyệt |
|---|---|---|---|---|
| Cụm tháp City (22 Bishopsgate, Leadenhall, Scalpel, Lloyd's) — It's No Game, 2019 | **CC BY 2.0** (FlickreviewR passed) | H5-06t (3 s) | "22 Bishopsgate and Leadenhall, 2019" | ☐ ✓ ☐ ✗ |
| Tháp Barbican nhìn từ London Eye — Mikey, 2013 | **CC BY 2.0** | H5-02t (4 s) | "Barbican towers, 2013" | ☐ ✓ ☐ ✗ |
| St Paul's thập niên 1950 · Barbican/London Wall đang xây | **không tìm được** bản CC BY/PD (chỉ có CC BY-SA / geograph — loại) | — | — | — |
| IWM D 6418 gốc 600×800 | Commons API mở lúc 01:19–01:45 UTC nhưng máy chủ ảnh `upload.wikimedia.org` 429 suốt phiên | giữ bản 500×667 | — | ☐ chủ dự án tải tay |
| Tower Block UK l9 (Barbican 1985/1988, CC BY 4.0, Miles Glendinning) | xếp hàng tải (429) | dự phòng | — | — |
Footage đêm: **BỎ** (C2 đã quyết).

## Ngân sách + giờ phiên B (chi tiết báo cáo §8)
- Dựng 1080p look3 d lớp D + E: **13 061 khung ≈ 31 h máy ở P = 2** (đo 8,58 s/khung thông lượng) → > 12 h → **chia B1/B2/B3**: B1 = HỒI 1 + HỒI 3 (≈ 11,1 h) · B2 = MÓC + HỒI 2 (≈ 11,7 h) · B3 = HỒI 4 + HỒI 5 (≈ 8,4 h) + ghép, âm, xuất, Omni 720p.
- Omni 720p: 31 clip, ≈ 181–186 s × $0,102/s = **$18,5–19,0** (+ ≤ 30 % làm lại → ≤ $24,7); Gemini T4 tổng dự kiến **$37,1–43,3** / mốc $50 / chặn $55.
- ☐ đồng ý chia 3 phiên · ☐ cho P = 3 (BAI-HOC #110: ≤ 3 trên 4 nhân; ước ≈ 22–24 h, chưa đo) · ☐ khác

## Quyết định khác
| # | Việc | Phương án | Ưu | Nhược | Tác động | Rủi ro | Khuyến nghị |
|---|---|---|---|---|---|---|---|
| **Q-A1** | Mặt nạ E | (a) "đủ" (mọi toà OSM có tên); (b) "tháp" + ngoại lệ "bờ" | (a) 0 Chặn, chặt nhất; (b) đẹp hơn rõ, đúng chữ §15 (k) "toà tháp" | (a) loang lổ 3D↔AI; (b) cần ngoại lệ + K định nghĩa (KN-5) | H5-05a 6 s | (b) AI vẽ lại toà thấp có tên (sai nhỏ — chủ dự án đã chấp nhận 09:08) | **(b)** nếu chủ dự án thấy tờ so (b) rõ hơn; nếu không, (a) |
| **Q-A2** | Q37 nhịp (TB 5,75 s / 3,5; dài nhất 20,17 s ở H2-03b) | (a) chờ K hiệu chuẩn BIEN-CO-V trên 1080p (KN-2 A); (b) K nhận beats `bien_co_tl` neo log máy (KN-2 B); (c) thêm cắt góc R3 cho shot > 15 s (M00, M01, H1-08b, H2-03b, H2-06, H2-10, H5-07b) | (a)(b) không thêm phần tử chỉ để vượt chỉ số; (c) nhịp nhanh hơn thật | (a) phụ thuộc K; (c) đổi bố cục, thêm giờ dựng | G2 | (c) phạm luật cứng nếu chỉ để vượt ngưỡng | **(a) + (b)**; (c) chỉ nơi chủ dự án thấy chậm khi xem |
| **Q-A3** | M00 mở lạnh | (a) điểm P1b mới (Bankside đông, 125 m, VONG — `m00/M00-moi-a.jpg`); (b) `M00-moi-b` | khác hẳn M03, thấy cầu London có nhà + toàn vòng lửa | phải dựng mới 17 s | MÓC | thấp | **(a)** |
| **Q-A4** | Nâng 3D mái vòm + toà tháp có tên (B-x1) | (a) làm ở B1 trước khi dựng (vật liệu đá Portland, chì, đèn pha đêm); (b) giữ | E, đêm 2026, H5-08 bớt CG | thêm ≈ 1–2 h | phần hiện đại | thấp | **(a)** |
| **Q-A5** | Niên đại 3D 1960s–70s (London Wall/Barbican) | (a) sửa lọc năm toà OSM theo năm xây (B1) rồi thử lại H5-02b/H5-02s Omni (≤ 2 lượt, ≈ $0,9); (b) giữ 3D như v3 | (a) đạt mục tiêu A gần 30 s | thêm 1 vòng | H5 | thấp | **(a)** |
| **Q-A6** | H1-06b (ngoại lệ animatic D5) | kiểm lại ở 720p (phiên B) | — | — | 4,3 s | — | giữ D5 |

## Việc chờ chủ dự án
1. E1 (mặt nạ + ngoại lệ "bờ"), E2 (H5-04 đuôi E?), P1 (a/b/c), D/B mẫu, **A1 từng clip H1-06x, H1-15x**, clip hiện đại H5-04c, H5-05d, 2 ảnh thật, Q-A1…Q-A6, chia phiên B.
2. Tải tay IWM D 6418 bản gốc (Commons ảnh 429 suốt phiên).
3. Dòng AUTHORSHIP cho A1 (P ghi) → khai `duyet_chu_du_an` ở phiên B.
