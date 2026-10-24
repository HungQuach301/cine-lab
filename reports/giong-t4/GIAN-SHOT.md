# BẢNG GIÃN SHOT ĐỀ XUẤT — K2C-T4-02 London (GIONG-T4, 24/10/2026)

> **Không sửa `BANG-SHOT-v1.*`** — bảng này để animatic áp sau khi chủ dự án chọn phương án (PHIEU-GIONG.md G-1). Sinh bằng `scripts/k2ldn/giong/gl_gian_shot.py` (số máy: `gian-shot.json`).
> **Lời từng shot = mốc thật** bản thu G1 cuối (sau thu lại), từ đầu câu đầu tới cuối câu cuối của đoạn gán cho shot (`khoa-loi/doan-shot.json`; mốc: `am-thanh/master/T4-loi-moc.json`).
> **Luật:** shot có lời chứa lời + 0,4 s (luật G1) + phần "lặng N s" đã ghi trong bảng v1; không cắt lời; không kéo nhịp giọng; làm tròn lên 1/24 s.
> **A** = chỉ giãn (shot dư giữ) · **B** = A + rút đuôi hình sau lời xuống ≤ 1,5 s ở shot có lời đang dư (giữ khung P1 tái xuất, KHOP, cú lặn, khoảnh khắc đinh) · **C** = B + shot "nối" không lời → 6 s, H5-08 kéo lùi cuối 28 → 18 s (giữ 6 s lặng) · **C1** = C với đuôi ≤ 1,0 s, H4-08 20 → 12 s, H3-06 12 → 8 s.
> **K0** = đủ lời khoá · **K1** = bỏ 7 câu NGUYÊN trong dựng (không thu lại, 0 ký tự): L81, L41 (nửa sau "Four classes…"), L45, L38, L77, L15, L54.

## Tổng (mục tiêu 720 s; Đ2: ≤ +5 % = 756 s)
| Đo | Giây | Lệch so 720 s |
|---|---|---|
| Lời theo shot (cộng lời từng shot) | **632,8** | — |
| Lời liền trong chương (gồm ngừng tự nhiên giữa đoạn) | 670,8 | — |
| Bảng v1 (giữ nguyên) | 720,0 | 0 % — nhưng **lời không vừa**: 35 shot thiếu chỗ |
| K0-A chỉ giãn | 891,5 | +23,8 % |
| K0-B | 833,3 | +15,7 % |
| K0-C | 803,3 | +11,6 % |
| K0-C1 | 782,2 | +8,6 % |
| K1-B | 782,5 | +8,7 % |
| K1-C | 752,5 | **+4,5 % (trong ±5 % quanh trần — nêu tên)** |
| **K1-C1 (đề xuất)** | **730,1** | **+1,4 % (trong ±5 % — nêu tên)** |

**Nguyên nhân lệch:** tốc độ đọc G1 đúng như ước (1 553 từ / 632,8 s = 2,45 từ/s, nháp ước 145 từ/phút = 2,42). Lệch đến từ cấu trúc bảng v1: 138 s shot không lời (H1-19, H2-11…14, H3-06, H4-08, H5-06, H5-08, H5-09) + ≈ 17 s "lặng" có chủ ý + ngừng giữa 50 đoạn lời, trong khi nháp chỉ tính 45 s lặng + 16 s thẻ.

**Tiết kiệm từng câu K1 (đo trên bản thu, phương án C1):** L81 −11,2 s · L41 nửa sau −9,9 s · L45 −8,5 s · L38 −7,5 s · L15 −6,3 s · L77 −5,8 s · L54 −2,9 s = **−52,1 s**.

## Điểm animatic cần biết (bất kể phương án)
1. **Cột "Lời" của BANG-SHOT-v1 lệch ±1 câu ở Hồi 1 và Hồi 4** (đánh số theo một bản nháp cũ): ví dụ H1-03 (Hollar) ghi L11 nhưng câu Hollar là L10; H1-11 (Royal Exchange) ghi L24 nhưng câu Royal Exchange là L21; H4-05 ghi L68 (Churchill) nhưng vai "sáng ra mái vòm còn đứng" là L69. Bảng này gán theo **nội dung/vai truyện** (`doan-shot.json`).
2. **Đổi chỗ H1-11 ↔ H1-12** (đề xuất): lời "The river fills with boats…" (L22 nửa sau) rơi vào M-d (3) sông H1-12, rồi mới tới Evelyn "like the top of a burning oven" (L23) trên H1-11 — giữ đúng thứ tự lời, khớp hình.
3. **Ba M-d dài hơn 8 s** khi giữ lời trong shot: H1-01 (11,9 s), H1-05 (10,7 s), H1-17 (12,3 s). Cách xử lý: clip M-d dài hơn, hoặc để lời chảy sang shot 3D kế (hình 3D vào sau cùng giờ — §15 f kẹp giữa hai shot 3D cùng giờ vẫn giữ).
4. **Thẻ nhân vật dời theo lời:** thẻ Pepys từ H1-06 sang **H1-05** (lần gọi tên đủ "Samuel Pepys" ở L13, V02); nếu bỏ L45 (K1) → thẻ Hooke từ H2-05 sang **H2-02** (L36 nhắc Hooke).
5. **H3-02 mốc năm:** nhà trên cầu dỡ **1758** (lời V09 theo LMA), không phải 1761 như bảng v1.
6. **H4-03 "triều thấp"** đã có nguồn (BBC 2010, Brewers' Company 2020) — bỏ chú "[cần kiểm]" khi áp.
7. Shot H5-05 mang 4 câu (36,4 s lời ở K0; 25,2 s ở K1) trong khi v1 dài 14 s — nên tách thành 2 cú máy (THAP Fleet Street + một góc LVMF) khi dựng animatic.

## Bảng từng shot (K0; cột A/B/C theo đủ lời — K1 xem `gian-shot.json` → `phuong_an`)
| Shot | Cú máy | Loại | Dài v1 (s) | Lời thật (s) | Cần (lời + 0,4) | A | B | C | Lệch A − v1 | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|
| M01 | CODINH | có lời | 12 | 17.46 | 17.88 | 17.88 | 17.88 | 17.88 | +5.88 | GIÃN |
| M02 | KEO | có lời | 8 | 9.66 | 10.08 | 10.08 | 10.08 | 10.08 | +2.08 | GIÃN |
| M03 | DAY | có lời | 11 | 5.56 | 9.00 | 11.00 | 11.00 | 11.00 | +0.00 |  |
| M04 | LAN | có lời | 12 | 7.48 | 7.92 | 12.00 | 12.00 | 12.00 | +0.00 |  |
| H1-01 | MD | có lời | 8 | 11.47 | 11.88 | 11.88 | 11.88 | 11.88 | +3.88 | M-d > 8 s; GIÃN |
| H1-02 | CODINH | có lời | 12 | 7.91 | 8.33 | 12.00 | 9.42 | 9.42 | +0.00 |  |
| H1-03 | TRUOT | có lời | 10 | 15.45 | 15.88 | 15.88 | 15.88 | 15.88 | +5.88 | GIÃN |
| H1-04 | CODINH | có lời | 12 | 9.57 | 10.00 | 12.00 | 11.08 | 11.08 | +0.00 |  |
| H1-05 | MD | có lời | 8 | 10.24 | 10.67 | 10.67 | 10.67 | 10.67 | +2.67 | M-d > 8 s; GIÃN |
| H1-06 | CAU | có lời | 12 | 19.37 | 19.79 | 19.79 | 19.79 | 19.79 | +7.79 | GIÃN |
| H1-07 | VONG | có lời | 8 | 15.06 | 15.46 | 15.46 | 15.46 | 15.46 | +7.46 | GIÃN |
| H1-08 | CODINH | có lời | 16 | 14.77 | 18.21 | 18.21 | 18.21 | 18.21 | +2.21 | GIÃN |
| H1-09 | XUONG | có lời | 14 | 12.14 | 12.58 | 14.00 | 13.67 | 13.67 | +0.00 |  |
| H1-10 | MD | có lời | 8 | 1.88 | 2.29 | 8.00 | 3.42 | 3.42 | +0.00 |  |
| H1-11 | CODINH | có lời | 12 | 14.00 | 14.42 | 14.42 | 14.42 | 14.42 | +2.42 | GIÃN |
| H1-12 | MD | có lời | 8 | 5.42 | 5.83 | 8.00 | 6.96 | 6.96 | +0.00 |  |
| H1-13 | THAP | có lời | 16 | 11.44 | 11.88 | 16.00 | 12.96 | 12.96 | +0.00 |  |
| H1-14 | MD | có lời | 7 | 4.40 | 4.83 | 7.00 | 5.92 | 5.92 | +0.00 |  |
| H1-15 | CAU | có lời | 12 | 21.09 | 21.50 | 21.50 | 21.50 | 21.50 | +9.50 | GIÃN |
| H1-16 | CODINH | có lời | 10 | 6.21 | 6.62 | 10.00 | 7.75 | 7.75 | +0.00 |  |
| H1-17 | MD | có lời | 7 | 11.85 | 12.29 | 12.29 | 12.29 | 12.29 | +5.29 | M-d > 8 s; GIÃN |
| H1-18 | XUONG | có lời | 9 | 15.87 | 16.29 | 16.29 | 16.29 | 16.29 | +7.29 | GIÃN |
| H1-19 | MD | lặng | 6 | 0.00 | 0.00 | 6.00 | 6.00 | 6.00 | +0.00 |  |
| H2-01 | LAN | có lời | 10 | 12.74 | 13.17 | 13.17 | 13.17 | 13.17 | +3.17 | GIÃN |
| H2-02 | XUONG | có lời | 12 | 21.73 | 22.17 | 22.17 | 22.17 | 22.17 | +10.17 | GIÃN |
| H2-03 | CODINH | có lời | 12 | 25.76 | 26.17 | 26.17 | 26.17 | 26.17 | +14.17 | GIÃN |
| H2-04 | TRUOT | có lời | 12 | 21.22 | 21.62 | 21.62 | 21.62 | 21.62 | +9.62 | GIÃN |
| H2-05 | CODINH | có lời | 14 | 26.93 | 27.38 | 27.38 | 27.38 | 27.38 | +13.38 | GIÃN |
| H2-06 | VONG | có lời | 12 | 11.17 | 11.58 | 12.00 | 12.00 | 12.00 | +0.00 |  |
| H2-07 | CODINH | có lời | 8 | 6.90 | 7.33 | 8.00 | 8.00 | 8.00 | +0.00 |  |
| H2-08 | NGHIENG | có lời | 12 | 4.70 | 5.12 | 12.00 | 6.21 | 6.21 | +0.00 |  |
| H2-09 | CODINH | có lời | 12 | 6.66 | 7.08 | 12.00 | 8.17 | 8.17 | +0.00 |  |
| H2-10 | THAP | có lời | 10 | 13.63 | 18.04 | 18.04 | 18.04 | 18.04 | +8.04 | GIÃN |
| H2-11 | XUONG | nối | 10 | 0.00 | 0.00 | 10.00 | 10.00 | 6.00 | +0.00 |  |
| H2-12 | KHOP | lặng | 12 | 0.00 | 0.00 | 12.00 | 12.00 | 12.00 | +0.00 |  |
| H2-13 | TRUOT | nối | 10 | 0.00 | 0.00 | 10.00 | 10.00 | 6.00 | +0.00 |  |
| H2-14 | CAU | nối | 12 | 0.00 | 0.00 | 12.00 | 12.00 | 6.00 | +0.00 |  |
| H3-01 | CODINH | có lời | 14 | 5.13 | 5.54 | 14.00 | 6.67 | 6.67 | +0.00 |  |
| H3-02 | TRUOT | có lời | 10 | 9.71 | 10.12 | 10.12 | 10.12 | 10.12 | +0.12 | GIÃN |
| H3-03 | XUONG | có lời | 14 | 14.94 | 15.38 | 15.38 | 15.38 | 15.38 | +1.38 | GIÃN |
| H3-04 | CODINH | có lời | 12 | 9.94 | 10.38 | 12.00 | 11.46 | 11.46 | +0.00 |  |
| H3-05 | THAP | có lời | 10 | 19.31 | 19.71 | 19.71 | 19.71 | 19.71 | +9.71 | GIÃN |
| H3-06 | KHOP | nối | 12 | 0.00 | 0.00 | 12.00 | 12.00 | 12.00 | +0.00 |  |
| H4-01 | CODINH | có lời | 12 | 11.20 | 11.62 | 12.00 | 12.00 | 12.00 | +0.00 |  |
| H4-02 | CAU | có lời | 14 | 9.57 | 10.00 | 14.00 | 11.08 | 11.08 | +0.00 |  |
| H4-03 | TRUOT | có lời | 8 | 7.88 | 8.29 | 8.29 | 8.29 | 8.29 | +0.29 | GIÃN |
| H4-04 | THAP | có lời | 16 | 27.83 | 28.25 | 28.25 | 28.25 | 28.25 | +12.25 | GIÃN |
| H4-05 | DAY | có lời | 8 | 3.52 | 3.96 | 8.00 | 5.04 | 5.04 | +0.00 |  |
| H4-06 | CODINH | có lời | 14 | 5.18 | 9.58 | 14.00 | 10.71 | 10.71 | +0.00 |  |
| H4-07 | XUONG | có lời | 16 | 4.45 | 4.88 | 16.00 | 5.96 | 5.96 | +0.00 |  |
| H4-08 | KHOP | lặng | 20 | 0.00 | 0.00 | 20.00 | 20.00 | 20.00 | +0.00 |  |
| H5-01 | CODINH | có lời | 12 | 12.13 | 12.54 | 12.54 | 12.54 | 12.54 | +0.54 | GIÃN |
| H5-02 | CAU | có lời | 16 | 13.84 | 14.25 | 16.00 | 15.38 | 15.38 | +0.00 |  |
| H5-03 | XUONG | có lời | 12 | 5.43 | 5.88 | 12.00 | 6.96 | 6.96 | +0.00 |  |
| H5-04 | CODINH | có lời | 14 | 15.76 | 16.17 | 16.17 | 16.17 | 16.17 | +2.17 | GIÃN |
| H5-05 | THAP | có lời | 14 | 36.35 | 36.79 | 36.79 | 36.79 | 36.79 | +22.79 | GIÃN |
| H5-06 | VONG | nối | 12 | 0.00 | 0.00 | 12.00 | 12.00 | 6.00 | +0.00 |  |
| H5-07 | KHOP | có lời | 20 | 20.92 | 21.33 | 21.33 | 21.33 | 21.33 | +1.33 | GIÃN |
| H5-08 | KEO | lặng | 28 | 0.00 | 0.00 | 28.00 | 28.00 | 18.00 | +0.00 |  |
| H5-09 | PP | PP | 16 | 0.00 | 0.00 | 16.00 | 16.00 | 16.00 | +0.00 |  |
