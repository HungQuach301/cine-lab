# MỞ ĐẦU MỚI + SHOT "ĐỨNG" — K2C-T4-02 animatic v2 (NC-T4, 25/10/2026)

> Căn cứ nhận xét 1 của chủ dự án (25/10/2026 06:56): "Hình ở 10 giầy đầu gần như đứng và khá xấu và bị đứng ở 1 số khoảnh khắc nữa".
> Số đo dùng ở đây là số **của k2check 1.17.4 trên animatic** (`reports/animatic-t4/k2check-1.17.4-animatic.md`, nhánh ANIMATIC-T4 @393c3b55: Q37 (1.13) (d), Q37 (c)/(d), BIEN-CO-V (c), TL-1 (d)) và `animatic/log-shot.json` + `kiem-may-log.json` (td = 0 với mọi shot CODINH). Phiên không đo lại video. Ước tỷ lệ: `bo-tri/uoc-A|B|C.json` (script `scripts/k2ldn/nc/bo_tri.py`).

## 1. Chẩn đoán 30 s đầu hiện tại

| t | Shot | Cú máy | Lớp | Đo | Vấn đề |
|---|---|---|---|---|---|
| 0:00–0:17.9 | M01 | CODINH (td 0) | A + **tấm nền N2P 0–11 s** | Q37: "trôi chậm … 9,83 s từ 0:00.0"; ngày→đêm diễn ra trên tấm tĩnh | 10 s đầu là một tấm ảnh AI tĩnh (cổng N2P cấm vật chuyển động trên tấm tĩnh — §15 (c)(iv)), nên gần như không có gì động; tấm nền là nơi lộ "xấu" nhất (AI, sương/trời phẳng) |
| 0:17.9–0:28.0 | M02 | KEO | A | — | tua ngược tốt nhưng tới muộn (giây 18) |
| 0:28.0–0:39.0 | M03 | DAY | A | TL-1 (d) trôi 3,67 %/s | khoảnh khắc mạnh nhất (vòng cung lửa) nằm ở giây 28 |

## 2. Ba phương án cho 30 s đầu

Lời L01–L03 giữ nguyên ở cả ba phương án; chỉ A thêm hai câu mở lạnh (N0a, N0b — tính trong hạn N6). Bảng khung theo giây.

### A — "Lửa trước" (khuyến nghị)

| Giây | Khung | Cú máy | Lời |
|---|---|---|---|
| 0–10 | P1 Bankside đêm 2/9/1666, vòng cung lửa (render M03 có sẵn, giờ 21→21,5) | DAY ≤ 1,5 %/s | N0a "September 1666. From an alehouse on this bank, a man watches the City burn." · N0b "“A most horrid malicious bloody flame,” he writes, “not like the fine flame of an ordinary fire.”" |
| 10–11 | KHOP hoà 1 s cùng khung P1: lửa 1666 → City 2026 chiều | KHOP | — |
| 11–23 | M01 rút còn 12 s, **bỏ tấm nền**, CODINH → DAY chậm; lớp sống 3D (thuyền, xe trên cầu, mây) | DAY | L01–L03 |
| 23–33 | M02 tua ngược (giữ) | KEO | L04–L05 |
| 33–44 | M03 vòng cung lửa (giữ — nay là "trả lời" mở lạnh) | DAY | L06 |

Nhịp: biến cố mạnh ở giây 0 (lửa), giây 10 (khớp năm), giây 23 (tua ngược). Ưu: móc mạnh nhất ngay giây 0, không cần Gemini, dùng render đã có, KHOP 1666 ↔ 2026 ở đầu phim báo trước KHÉP VÒNG H5-07b (cùng khung). Nhược: +10 s; tấm nền N2P giảm 11 s (N2P 2,37 % — vốn đã dưới mục tiêu V7 5–15 %); mở bằng câu trích nên phải đọc rõ (giọng G1). Tác động (ước `uoc-A.json`): 760,0 s · M-d 27,98 % · góc cao 60,57 %. Rủi ro: M03 và M00 cùng khung lửa — phải khác giờ (21 vs 22,5) và khác cú máy để không thành lặp (Q33-K2 lặp cảnh "≤ 2 lần" theo pHash: M00, M03, H1-08b, H5-07b sẽ cùng khung P1 lửa — animatic chưa đo pHash (k2check: "chưa đo pHash (không có master)") nên **chưa biết** có vượt không; cần K xác nhận cách tính với KHOP/xương sống, hoặc M00 lấy giờ 20 khi lửa còn hẹp).

### B — "2026 có máy + chớp lửa"

| Giây | Khung | Cú máy | Lời |
|---|---|---|---|
| 0–14 | M01 rút còn 14 s, **bỏ tấm nền**, VONG ≤ 3°/s quanh mái vòm; lớp sống 3D | VONG | L01–L03 |
| ~9,5 | 3 chớp KHOP 0,5–0,75 s: cùng khung P1 năm 1666 đang cháy (ở chữ "burned to the ground twice" của L04) | KHOP | — |
| 14–24 | M02 tua ngược | KEO | L04–L05 |
| 24–35 | M03 | DAY | L06 |

Ưu: không thêm lời; giữ thứ tự đã khoá; 0 Gemini. Nhược: 2026 ban ngày vẫn là hình mở (kém kịch tính hơn A); chớp lửa < 1 s dễ bị TL-1 (c) tính thêm cắt và có thể gây cảm giác "giật". Tác động (`uoc-B.json`): 754,0 s · M-d 28,20 % · góc cao 60,25 %. Rủi ro: chớp sáng mạnh — phải kiểm nhấp nháy (WCAG ≤ 3 lần/s).

### C — "Footage thật trước"

| Giây | Khung | Cú máy | Lời |
|---|---|---|---|
| 0–6 | Footage thật 2026 tầm người: Bankside/Millennium Bridge, người qua lại, mái vòm phía xa (ứng viên ở `FOOTAGE-2026.md`) | máy tay/trượt | L01 bắt đầu |
| 6–18 | M01 rút 12 s, DAY, bỏ tấm nền | DAY | L01–L03 |
| 18–28 | M02 | KEO | L04–L05 |
| 28–39 | M03 | DAY | L06 |

Ưu: "thật" ngay giây 0, đáp nhận xét 4 (ảnh/footage thật). Nhược: hình đầu là footage người khác quay (khó làm thumbnail/nhận diện kênh); phụ thuộc giấy phép clip. Tác động (`uoc-C.json`): 756,0 s · M-d 28,13 % · **góc cao 59,55 % < 60 % — TRƯỢT GOC-CAO-60**, phải rút thêm ≈ 4 s M-d hoặc thấp. Rủi ro: CC BY-SA → điều kiện chia sẻ tương tự (xem FOOTAGE-2026 §2).

**Khuyến nghị: A**, kèm điều kiện M00 lấy giờ khác M03 và K xác nhận Q33 với KHOP.

## 3. Mọi shot "đứng" và cách sửa

Tiêu chí: (i) CODINH > 8 s (td = 0, `kiem-may-log.json`) hoặc (ii) khoảng **khung tĩnh / không biến cố đo** > 6 s trong k2check 1.17.4 animatic (Q37 (1.13) (d), Q37 (c)/(d), BIEN-CO-V (c)). Shot timelapse CODINH có thời gian chạy nên không phải shot nào cũng "đứng" trên video — cột "Đo" cho biết shot nào bị máy đo bắt.

| Shot | t | Dài | Cú máy | Đo k2check | Cách sửa đề xuất | Trong bố trí A |
|---|---|---|---|---|---|---|
| M01 | 0:00 | 17,9 | CODINH + tấm nền | trôi chậm 9,83 s từ 0:00 | rút 12 s, bỏ tấm nền, DAY; mở lạnh trước | có |
| H1-04 | 1:27.6 | 10,6 | CODINH | — | tách M-d 6 s (Pepys trên Tower, DN02) | có |
| H1-08b | 2:23.9 | 12,2 | CODINH | — (lửa lan = biến cố) | giữ (P1 tái xuất bắt buộc §19 (3)); lớp sống: đèn thuyền trên sông | lớp sống |
| H1-11 | 2:58.6 | 14,4 | CODINH | — | tách M-d 6 s Royal Exchange (DN06) | có |
| H2-03b | 5:10.0 | 12,2 | CODINH | — | rút 2 s hoặc lớp sống (người đo đạc nhỏ L3) | lớp sống |
| H2-05 | 5:39.9 | 18,8 | CODINH | — (timelapse xây) | giữ — timelapse nhà mọc là biến cố liên tục; cân nhắc rút 3 s | không đổi |
| H3-05 | 7:59.8 | 19,7 | THAP | **khung tĩnh 8,83 s từ 8:04.0** | tách M-d 6 s (người khảo sát 1937) + rút 3,7 s | có |
| H4-04c | 9:13.4 | 13,25 | CODINH | **khung tĩnh 9,21 s từ 9:14.0** | bỏ câu Churchill → rút 5,5 s (DN13) | có |
| H4-06 | 9:31.2 | 10,2 | CODINH | — | tách ảnh thật 1940 5 s (DN13) | có |
| H5-01 | 9:58.8 | 12,5 | CODINH | — | lớp sống (cần cẩu, xe 1950) hoặc cú máy chậm DAY | cú máy chậm |
| H5-04 | 10:32.7 | 10,4 | CODINH + tấm nền | — | giữ (tấm nền chỉ cho CODINH) | không đổi |
| H5-05a | 10:43.1 | 16,5 | CODINH + tấm nền | **khung tĩnh 14,04 s từ 10:44.5**; Q37 (c) và BIEN-CO-V (c) khoảng dài nhất 16,5 s | rút 12 s + lớp sống cộng hiệu (thuyền, người trên cầu Millennium — §15 (b) lớp sống) | có (rút) |
| H5-05b | 10:59.6 | 9,1 | THAP | **khung tĩnh 8,75 s từ 11:00.0** | cú máy THAP có trôi (ngửa chậm ≤ 1°/s) hoặc rút 3 s | cú máy chậm |
| H5-07a | 11:14.8 | 6,0 | CODINH | (trong khoảng 11:14–11:20) | footage thật 2026 đêm (DN15) | có |
| H5-07b | 11:20.8 | 15,3 | KHOP | **khung tĩnh 7,12 s từ 11:29.0** (nửa 2026) | lớp sống: đèn xe/thuyền, cửa sổ sáng tắt | lớp sống |
| H5-09 (PP) | 11:54.1 | 16,0 | thẻ | khung tĩnh 8,58 s + 6,58 s | Q37 (c) đã miễn thẻ PP (1.17.4); giữ | không đổi |

Lớp sống (thuyền, xe, người L3, đèn) là 3D — không tính AI, không tốn Gemini; với shot có tấm nền phải ghép bằng cộng hiệu (§15 (b) lớp sống).
