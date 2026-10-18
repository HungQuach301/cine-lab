# T3 · Kiểm chữ lời KHOÁ v4.1 (khoá lời 18/10/2026, LK2 + LK3; trước là v4, lời v1 G1) — sinh bằng `g1/bang_kiem_chu.py`

Nguồn: `script-v4.1-KHOA.md` × `vay-ham/treatment.json` (bản G1). Ước **2,5 từ NÓI/s** (Kinh thánh §3: ~150 từ/phút; số đọc thành chữ, tách gạch nối — cùng cách đếm gói TUYẾN). Đối chiếu: Eric đo thật ở T2 = 151,2 từ VIẾT/phút.

## 0. Tổng

- Từ viết **1588** · từ nói **1670** · ước lời **668.0 s** (2,5 từ nói/s) · ước theo nhịp Eric T2 **630.2 s** · tổng phim (bảng shot) **719.7 s**.
- Lỗi: không
- Cảnh báo tràn > 1,5 s: 1h: lời tràn 3.2 s sang shot sau; 1i: lời tràn 2.6 s sang shot sau; 2l: lời tràn 2.0 s sang shot sau; 2n: lời tràn 2.4 s sang shot sau; 2o: lời tràn 1.9 s sang shot sau; 2r: lời tràn 1.7 s sang shot sau; 4b: lời tràn 3.0 s sang shot sau; 4c: lời tràn 2.0 s sang shot sau; SM3: lời tràn 5.2 s sang shot sau; 5i: lời tràn 2.0 s sang shot sau

| Chương | Dài (s) | Từ nói | Ước lời (s) | Lời/cửa sổ |
|---|---|---|---|---|
| 00 | 44.5 | 103 | 41.2 | 0.926 |
| 01 | 122.1 | 287 | 114.8 | 0.940 |
| 02 | 203.6 | 488 | 195.2 | 0.959 |
| 03 | 84.5 | 189 | 75.6 | 0.895 |
| 04 | 110.5 | 249 | 99.6 | 0.901 |
| 05 | 154.4 | 354 | 141.6 | 0.917 |

## 1. Từ điển đọc số (áp khi khoá lời, BAI-HOC #19/#59/#104)

| Viết | Đọc |
|---|---|
| 2026 | twenty twenty-six |
| 1309 | thirteen oh-nine |
| 1783 | seventeen eighty-three |
| 1782 | seventeen eighty-two |
| 1941 | nineteen forty-one |
| 1705 | seventeen oh-five |
| 1704 | seventeen oh-four |
| 1713 | seventeen thirteen |
| 2015 | twenty fifteen |
| 1727 | seventeen twenty-seven |
| 1730 | seventeen thirty |
| 1779 | seventeen seventy-nine |
| 1780 | seventeen eighty |
| 1781 | seventeen eighty-one |
| 1810 | eighteen ten |
| 1870 | eighteen seventy |
| 1908 | nineteen oh-eight |
| 1909 | nineteen oh-nine |
| 1934 | nineteen thirty-four |
| 1939 | nineteen thirty-nine |
| 1943 | nineteen forty-three |
| 1940 | nineteen forty |
| 1942 | nineteen forty-two |
| 1969 | nineteen sixty-nine |
| 1985 | nineteen eighty-five |
| 2025 | twenty twenty-five |
| 2024 | twenty twenty-four |
| 18 | eighteen |
| 1666 | sixteen sixty-six |

Số lớn đã viết bằng chữ ngay trong lời (fifteen thousand, three hundred and fifty-seven, twenty-eight point six percent…) để giọng đọc không đoán cách đọc.

## 2. Độ dài từng shot so cửa sổ

`vào trễ` = lời shot trước còn chảy sang (s); `tràn` = lời shot này chảy sang shot sau (s). Thời lượng đã đặt theo lời (`g1/dur-g1.json`); shot bị trần theo loại ghi ở `tran_chan`.

| Shot | Ch | Dài (s) | Từ nói | Ước (s) | Vào trễ | Tràn | Ghi chú |
|---|---|---|---|---|---|---|---|
| 0a | 00 | 6.5 | 15 | 6.0 | 0.0 | 0.0 |  |
| 0b | 00 | 5.5 | 12 | 4.8 | 0.0 | 0.0 |  |
| 0c | 00 | 3.0 | 10 | 4.0 | 0.0 | 1.0 |  |
| 0d | 00 | 7.5 | 17 | 6.8 | 1.0 | 0.3 |  |
| 0e | 00 | 5.5 | 12 | 4.8 | 0.3 | 0.0 |  |
| 0f | 00 | 5.0 | 11 | 4.4 | 0.0 | 0.0 |  |
| 0g | 00 | 6.0 | 14 | 5.6 | 0.0 | 0.0 |  |
| 0h | 00 | 5.5 | 12 | 4.8 | 0.0 | 0.0 |  |
| SM1 | 01 | 6.5 | 15 | 6.0 | 0.0 | 0.0 |  |
| 1a | 01 | 5.0 | 10 | 4.0 | 0.0 | 0.0 |  |
| 1b | 01 | 8.0 | 19 | 7.6 | 0.0 | 0.0 |  |
| 1c | 01 | 10.5 | 25 | 10.0 | 0.0 | 0.0 |  |
| 1d | 01 | 13.5 | 32 | 12.8 | 0.0 | 0.0 |  |
| 1e | 01 | 9.5 | 14 | 5.6 | 0.0 | 0.0 |  |
| 1f | 01 | 5.625 | 13 | 5.2 | 0.0 | 0.0 |  |
| 1g | 01 | 14.0 | 33 | 13.2 | 0.0 | 0.0 |  |
| 1h | 01 | 12 | 38 | 15.2 | 0.0 | 3.2 |  |
| 1i | 01 | 13.0 | 31 | 12.4 | 3.2 | 2.6 |  |
| 1j | 01 | 10.0 | 22 | 8.8 | 2.6 | 1.4 |  |
| 1k | 01 | 14.5 | 35 | 14.0 | 1.4 | 0.9 |  |
| 2a | 02 | 12.0 | 28 | 11.2 | 0.9 | 0.1 |  |
| 2b | 02 | 10.5 | 25 | 10.0 | 0.1 | 0.0 |  |
| 2c | 02 | 12.0 | 28 | 11.2 | 0.0 | 0.0 |  |
| 2d | 02 | 7.625 | 18 | 7.2 | 0.0 | 0.0 |  |
| 2e | 02 | 6.5 | 15 | 6.0 | 0.0 | 0.0 |  |
| SM2 | 02 | 7.5 | 17 | 6.8 | 0.0 | 0.0 |  |
| 2f | 02 | 6.0 | 14 | 5.6 | 0.0 | 0.0 |  |
| 2g | 02 | 12.5 | 26 | 10.4 | 0.0 | 0.0 |  |
| 2h | 02 | 7.0 | 16 | 6.4 | 0.0 | 0.0 |  |
| 2i | 02 | 6.0 | 14 | 5.6 | 0.0 | 0.0 |  |
| KA1782 | 02 | 8.0 | 15 | 6.0 | 0.0 | 0.0 |  |
| 2j | 02 | 12.5 | 30 | 12.0 | 0.0 | 0.0 |  |
| 2k | 02 | 12.0 | 33 | 13.2 | 0.0 | 1.2 |  |
| 2l | 02 | 12 | 32 | 12.8 | 1.2 | 2.0 |  |
| 2m | 02 | 20.0 | 44 | 17.6 | 2.0 | 0.0 |  |
| 2n | 02 | 8.0 | 26 | 10.4 | 0.0 | 2.4 |  |
| 2o | 02 | 12.5 | 30 | 12.0 | 2.4 | 1.9 |  |
| 2p | 02 | 8.0 | 19 | 7.6 | 1.9 | 1.5 |  |
| 2q | 02 | 11.0 | 26 | 10.4 | 1.5 | 0.9 |  |
| 2r | 02 | 12 | 32 | 12.8 | 0.9 | 1.7 |  |
| 3a | 03 | 12.0 | 28 | 11.2 | 1.7 | 0.9 |  |
| 3b | 03 | 10.5 | 25 | 10.0 | 0.9 | 0.4 |  |
| 3c | 03 | 8.5 | 19 | 7.6 | 0.4 | 0.0 |  |
| 3d | 03 | 10.0 | 22 | 8.8 | 0.0 | 0.0 |  |
| KC1910 | 03 | 7.0 | 11 | 4.4 | 0.0 | 0.0 |  |
| 3e | 03 | 6.0 | 14 | 5.6 | 0.0 | 0.0 |  |
| 3f | 03 | 16.0 | 38 | 15.2 | 0.0 | 0.0 |  |
| 3g | 03 | 5.0 | 11 | 4.4 | 0.0 | 0.0 |  |
| 3h | 03 | 9.5 | 21 | 8.4 | 0.0 | 0.0 |  |
| 4a | 04 | 10.5 | 25 | 10.0 | 0.0 | 0.0 |  |
| 4b | 04 | 15.0 | 45 | 18.0 | 0.0 | 3.0 |  |
| 4c | 04 | 9.0 | 20 | 8.0 | 3.0 | 2.0 |  |
| 4d | 04 | 10.5 | 24 | 9.6 | 2.0 | 1.1 |  |
| 4e | 04 | 7.5 | 17 | 6.8 | 1.1 | 0.4 |  |
| 4f | 04 | 9.0 | 20 | 8.0 | 0.4 | 0.0 |  |
| SM3 | 04 | 8 | 33 | 13.2 | 0.0 | 5.2 |  |
| 4g | 04 | 5.5 | 0 | 0.0 | 5.2 | 0.0 |  |
| KB1943 | 04 | 8.0 | 0 | 0.0 | 0.0 | 0.0 | IM LẶNG |
| 4h | 04 | 11.5 | 27 | 10.8 | 0.0 | 0.0 |  |
| 4i | 04 | 16.0 | 38 | 15.2 | 0.0 | 0.0 |  |
| 5a | 05 | 14.0 | 33 | 13.2 | 0.0 | 0.0 |  |
| 5b | 05 | 8.0 | 20 | 8.0 | 0.0 | 0.0 |  |
| KB2026 | 05 | 9.5 | 22 | 8.8 | 0.0 | 0.0 |  |
| 5c | 05 | 8.5 | 19 | 7.6 | 0.0 | 0.0 |  |
| 5d | 05 | 4.5 | 8 | 3.2 | 0.0 | 0.0 |  |
| KC2026 | 05 | 10.0 | 25 | 10.0 | 0.0 | 0.0 |  |
| 5e | 05 | 6.4167 | 15 | 6.0 | 0.0 | 0.0 |  |
| 5f | 05 | 16.5 | 40 | 16.0 | 0.0 | 0.0 |  |
| 5g | 05 | 8.0 | 19 | 7.6 | 0.0 | 0.0 |  |
| 5h | 05 | 16.0 | 38 | 15.2 | 0.0 | 0.0 |  |
| 5i | 05 | 8 | 25 | 10.0 | 0.0 | 2.0 |  |
| 5j | 05 | 17.0 | 41 | 16.4 | 2.0 | 1.4 |  |
| KA2026 | 05 | 8.0 | 0 | 0.0 | 1.4 | 0.0 | IM LẶNG |
| 5k | 05 | 20.0 | 49 | 19.6 | 0.0 | 0.0 |  |

## 3. Câu nhạy cảm (§10.6, TIEN-KY-VAY-HAM §6.1 CS1–CS10) — bộ lọc bắt và cách xử lý

| Shot | Luật | Câu | Xử lý |
|---|---|---|---|
| 2k | CS3 dân tộc như một khối (xem ngữ cảnh) | Four days later, the French and Spanish fleets gathered in the bay: | giữ — chủ thể cụ thể (hạm đội, chiến tuyến, pháo đài, kỹ sư, cách đếm), không phải dân tộc như một khối đạo đức |
| 2k | CS3 dân tộc như một khối (xem ngữ cảnh) | forty-seven ships of the line by the British count, fifty by the Spanish. | giữ — chủ thể cụ thể (hạm đội, chiến tuyến, pháo đài, kỹ sư, cách đếm), không phải dân tộc như một khối đạo đức |
| 2l | CS3 dân tộc như một khối (xem ngữ cảnh) | ten floating batteries, designed by the French engineer d'Arçon. | giữ — chủ thể cụ thể (hạm đội, chiến tuyến, pháo đài, kỹ sư, cách đếm), không phải dân tộc như một khối đạo đức |
| 2n | CS3 dân tộc như một khối (xem ngữ cảnh) | Over two thousand attackers were lost, by a British estimate that includes prisoners, and by a Spanish one; the British rescued three hundred and fifty-seven. | giữ — chủ thể cụ thể (hạm đội, chiến tuyến, pháo đài, kỹ sư, cách đếm), không phải dân tộc như một khối đạo đức |
| 3a | CS3 dân tộc như một khối (xem ngữ cảnh) | Between the walls and the Spanish line lay a strip of sand: | giữ — chủ thể cụ thể (hạm đội, chiến tuyến, pháo đài, kỹ sư, cách đếm), không phải dân tộc như một khối đạo đức |
| 3b | CS3 dân tộc như một khối (xem ngữ cảnh) | With Spain's consent, the British blew up the Spanish forts. | giữ — chủ thể cụ thể (hạm đội, chiến tuyến, pháo đài, kỹ sư, cách đếm), không phải dân tộc như một khối đạo đức |
| 4a | CS1 (chỉ trong trích có ghi nguồn) | In March 1939, Spain protested that the works stood on "a usurped portion" of its territory. | giữ — trích nguyên văn chính phủ TBN 4/3/1939 (S096), có ghi ai nói + chữ gốc trên hình |
| SM3 | CS1 occupied/occupation (chỉ được trong câu trích có ghi ai nói, hoặc sự kiện không về chủ quyền Gibraltar) | Spain turns "non-belligerent" and occupies Tangier. | giữ — câu SM3 chủ dự án đã chốt; "occupies Tangier" là sự kiện 14/6/1940 (T022), không nói về chủ quyền Gibraltar |

Số thương vong: mọi câu có số chết/mất/cứu đều nói ai đếm (bộ lọc: 0 lỗi). Không tính từ đạo đức cho phe nào (bộ lọc: 0 câu).

## 4. Trích trên hình (O4) — đối chiếu nguyên văn trong claim

| Shot | Trích | Claim khớp |
|---|---|---|
| 1c | «la preciosa llave del Mediterráneo» | S010 |
| 1d | «con cien hombres de guarnición … no había artilleros que las sirvieran» | S015 |
| 1g | «se habia acampado en las haciendas cercanas á la ermita de San Roque» | S019 |
| 1k | «bloquear definitivamente la correspondencia y paso a la plaza por tierra» | S032 |
| 2b | «Carlos III declaró la guerra á Inglaterra y se unió á Francia» | S039 |
| 2c | «encaminado principalmente á privar a la plaza de los viveres que le llegaban de las costas de África» | T006 |
| 2k | «alegrando la vista los 50 navios que se juntaron en Algeciras» | T018 |
| 2l | «l'expérience que l'inventeur avoit demandée … à l'épreuve des boulets rouges» | S073 |
| 2m | «á las diez y veinte y cinco minutos de la mañana … rompieron á un tiempo el fuego» | S067 |
| 2p | «se formó un boquete tan grande … que pareció bien colocar en el un cañón» | S087 |
| 2r | «Los últimos sufrieron una pérdida de cerca de dos mil hombres. La nuestra se aproximó á seis mil por todas causas» | S077 |
| 3b | «con autorización española, fueran destruidos por los ingleses» | S034 |
| 3c | «el progresivo avance de la frontera sobre la zona neutral» | S035 |
| 3f | «"como acto de cortesía"» | S036 |
| 4b | «una porción usurpada del territorio nacional» | S096 |
| 4h | «no queda constancia de reclamaciones por el uso de la pista» | S105 |
