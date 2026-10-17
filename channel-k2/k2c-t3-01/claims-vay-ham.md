# CLAIMS VÂY HÃM — T3b Gibraltar "vì sao ai cũng tranh giành Rock" (K2C-T3-01)

> Phiên tiền kỳ T3b, 17/10/2026. Bổ sung cho `tienky/claims.json` (C01–C35, hiệp ước 2026 + kinh tế — giữ nguyên, không sửa).
> Mọi câu trích là **nguyên văn** từ tệp tải bằng curl (ngoài git: `/var/tmp/cine-out/t3b/a1…a3/`), SHA-256 ở cột nguồn. Lỗi OCR giữ nguyên trong trích, chú giải ở "ghi chú".
> **Kiểm độc lập** (phiên P, `vay-ham/verify_quotes.py`, đọc tệp thô ngoài git): so lại mọi câu trích với văn bản tách từ tệp có đúng SHA. "khớp nguyên khối" = toàn câu có trong tệp (bỏ dấu câu/khoảng trắng, ſ/f); "khớp theo mảnh" = mọi mảnh trừ một mảnh do ngắt dòng/OCR → **đối chiếu ảnh trang trước khi đưa lên hình**.
> Máy đọc: `vay-ham/claims-vay-ham.json` (cùng nội dung + bảng số hai phía, lịch sự kiện, số đo đường băng/đường hầm).

**Tổng: 123 claim** — XÁC MINH 99 · MÂU THUẪN 21 · CHƯA XÁC MINH 3 · kiểm độc lập: khớp nguyên khối 116, khớp theo mảnh 7.

## 0. Số lần bị vây (bắt buộc kiểm)

| Số | Nguồn | Cách đếm | Danh sách |
|---|---|---|---|
| 14 | Sayer 1862 (title page "Fourteen Sieges"); [Stephens] 1870 ("the fourteenth of its order"); Gibraltar National Museum (đánh số 8/12/13 + "last siege"); García Sanz 2022 (1704 = "undécimo"); Wikipedia (dẫn Fa & Finlayson 2006) | Tính từ khi Castile chiếm 1309 (cuộc vây đầu tiên được ghi chép); 1333 tính HAI lần (Marinid chiếm Feb–Jun; Alfonso XI phản công Jun–Aug); 1462 tính (cuộc thứ 8, Castile chiếm lại); hai cuộc tranh giành nội bộ Castile 1466–67 và 1506 đều tính; KHÔNG tính cuộc đột kích của cướp biển Algiers 1540; 1704 (Anh–Hà Lan chiếm) và 1704–05 (Pháp–TBN phản công) là HAI cuộc riêng; 1727 và 1779–83 đều tính; dừng ở Great Siege (cuộc vây quân sự cuối). | 1309, 1315 (bảo tàng ghi 1316), 1333 (Feb–Jun), 1333 (Jun–Aug), 1349–1350, 1411, 1436, 1462, 1466–1467, 1506, 1704, 1704–1705, 1727, 1779–1783 |
| 14 | Sayer 1862 — MỤC LỤC (khác thân sách) | Mục lục ghi "Tenth siege, by Mediterranean pirates" (1540) thay vì 1506; nhưng thân sách tr. 85 gọi 1506 là "the 10th siege". Tổng vẫn là 14. Coi là lỗi biên tập nội tại. | 1309, 1315, 1333, 1333, 1349–50, 1411, 1436, 1462, 1466–67, 1540 (theo mục lục) / 1506 (theo thân sách), 1704, 1704–05, 1727, 1779–83 |
| 15 | Wikipedia (dẫn Jackson 1987, tr. 317) — CHƯA XÁC MINH bản gốc | Cộng thêm việc TBN đóng biên giới 1969–1985 như một "fifteenth siege" (ẩn dụ chính trị, không phải vây quân sự). | 14 cuộc trên, 1969–1985 (đóng biên giới) |

**Khuyến nghị cho lời:** Có thể nói "fourteen sieges" — nhất quán giữa sử Anh thế kỷ 19, Bảo tàng Quốc gia Gibraltar và sử học Tây Ban Nha hiện đại. Câu an toàn: "Historians count fourteen sieges of Gibraltar between 1309 and 1783." Tránh: (a) nêu số thứ tự từng cuộc ngoài 1704 = 11th và Great Siege = 14th/last; (b) "fifteenth siege" cho 1969–85 trừ khi gắn "some Gibraltarians called it"; (c) "Gibraltar changed hands only five times" (chưa kiểm sách gốc). Nếu nói về thời đại Anh: "four sieges between 1704 and 1783" (1704, 1704–05, 1727, 1779–83) — khớp mọi nguồn.

## 0b. Số hai phía (Great Siege) — dùng trong lời theo cột "cách nói"

| Chỉ số | Phía Anh | Phía Tây Ban Nha / Pháp | Cách nói |
|---|---|---|---|
| Quân Pháp–TBN trên bộ trước tổng công kích 9/1782 | gần 40.000 (Drinkwater 1905 p.293 (V-A2-21)) | 33.000 (Montero 1860 p.356) | 'khoảng 33.000 đến 40.000 quân' — nêu cả hai nguồn |
| Tàu chiến tuyến Pháp–TBN trong vịnh 12–13/9/1782 | 47 (gồm 3 tàu 2 tầng nhỏ) (Drinkwater p.292) | CHƯA XÁC MINH (Wikipedia: 49; Montero không nêu tổng trong đoạn đã đọc) (—) | 'gần 50 tàu chiến tuyến' |
| Số pháo / người trên 10 khẩu đội nổi | 142 pháo dùng + 70 dự bị (212); 5.260 người (Drinkwater p.306) | 138 pháo; 5.190 người (Montero p.359) | 'khoảng 140 pháo hướng vào thành, hơn 5.000 người' |
| Tổn thất Pháp–TBN ngày 13–14/9/1782 | không dưới 2.000 (gồm tù binh); cứu 357 (Drinkwater p.301, 304) | Montero: 'mas de dos mil'; bản biện hộ Pháp 1785: 185 tử/thương do pháo (không tính cháy/nổ); Gaceta de Madrid (qua Wikipedia): 719 trên tàu — chưa tải được bảng (Montero p.365; Conseil de guerre privé p.201) | 'khoảng hai nghìn người thương vong, bị bắt hoặc mất tích theo cả hai phía; 357 được quân Anh cứu' — không diễn cảnh chết |
| Thương vong đồn Anh ngày 13/9/1782 | 16 chết, 68 bị thương (Drinkwater 1786 p.387 (V-A2-26)) | — (—) | 'khoảng 16 người chết' (Wikipedia/McGuffie: 15) |
| Tổn thất cả cuộc vây — đồn Anh | 333 chết trận/chết vì thương; 536 chết bệnh (không kể scorbut 1779–80); tổng hao hụt 1.231 (Drinkwater p.367) | 'cerca de dos mil' (Montero p.373) | dùng số Drinkwater, nói rõ 'theo sổ của đồn' |
| Tổn thất cả cuộc vây — Pháp–TBN | không có tổng (Drinkwater: 'could never be ascertained') | gần 6.000 'por todas causas'; riêng quân Pháp tự khai 173 tử/thương (Montero p.373; Conseil de guerre privé p.102-103) | 'theo sử gia TBN, gần 6.000 người' |
| Đạn bắn cả cuộc vây | đồn bắn 205.328 (12/9/1779–3/2/1783); địch bắn 258.387 (12/4/1781–2/2/1783); đồn dùng gần 8.000 thùng thuốc (Drinkwater p.368) | nhận 258.387, đáp trả ~200.300; chi phí 12 triệu duro (Montero p.373) | 'gần nửa triệu phát đạn từ hai phía' |
| Giờ khai hoả 13/9/1782 | ~09:45 (Drinkwater); ~09:30 tàu tới (Spilsbury) (Drinkwater p.296; Spilsbury p.77) | 10:25 (Montero p.360) | bộ đếm: 09:30 tàu vào vị trí → 09:45 Anh khai hoả → 10:25 toàn tuyến Pháp–TBN |

## 0c. Lịch sự kiện (cho bộ đếm ngày/giờ M6)

| Ngày | Sự kiện | Claim |
|---|---|---|
| 1779-06-21 | Madrid đóng giao thông Tây Ban Nha–Gibraltar (đồn 5.382 người) | S040 |
| 1779-07-06 | Tin chiến tranh Anh–TBN tới Gibraltar | S041 |
| 1779-07-16 | Hải đội TBN phong toả cảng | S042 |
| 1779-09-12 | Đồn khai hoả lần đầu (CN) từ Green's Lodge, Willis's | S043 |
| 1779-09-23 | Thử nghiệm đạn nung đỏ đầu tiên (tiếp 25/9) | S058 |
| 1780-01 | Nạn đói: cây kế, bồ công anh làm thức ăn | S052 |
| 1780-01-18 | Đoàn cứu viện Rodney tới (tối ~23:00 Apollo vào cảng; suy luận) | S054 |
| 1780-10-11 | Tàu Đan Mạch chở chanh/cam (Drinkwater; Spilsbury ghi 20/10) | S053 |
| 1781-04-12 | Rạng sáng thấy hạm đội Darby; 10:45 thả neo, pháo TBN bắn phá thị trấn (114 khẩu); dân chạy về phía nam | S062 |
| 1781-04-14 | Nhà cháy; bắt đầu lính cướp kho | S063 |
| 1781-05-05 | Xử tử lính 58th cướp kho | S064 |
| 1782-02-15 | Thử bệ pháo hạ nòng Koehler (chiều) | S086 |
| 1782-05-25 | Bắt đầu đào đường hầm trên Farringdon's | S080 |
| 1782-06-15 | Crillon tới nhận chỉ huy (khoảng giữa tháng 6, Montero); Anh biết tin 14/7 | S049 |
| 1782-07-04 | Hầm Ince dài ~82 ft (13 người, ~5 tuần) | S081 |
| 1782-07-15 | Nổ mở lỗ châu mai thông gió; đặt pháo 24 pound | S082 |
| 1782-08-05 | Hầm dài 140 ft | S083 |
| 1782-09-08 | 07:00 đạn nung đỏ đốt khẩu đội Mahon (Boyd) | S059 |
| 1782-09-12 | ~08:00 hạm đội liên hợp xuất hiện; chiều thả neo (47 tàu chiến tuyến) | S065 |
| 1782-09-13 | 06:45 khẩu đội nổi nhổ neo; ~09:30–09:45 vào vị trí, Anh khai hoả 09:45; 10:25 toàn tuyến (Montero); 12:00 đạn nung bắt đầu, 13–14h phổ biến; 17:00 lửa bùng (Montero/Spilsbury); 19–20h pháo địch gần im | S066 |
| 1782-09-14 | 01:00 tàu đầu tiên cháy rực; 03:00 Curtis xuất kích; ~05:00 và 05:15 hai tàu nổ; trước 11:00 thêm 3 tàu nổ; chiều tàu cuối bị đốt; cứu 357 người | S074 |
| 1782-10-11 | Hoàng hôn: Latona báo hạm đội Howe (suy luận ngày) | S056 |
| 1782-10-18 | Trung đoàn 25 & 59 đổ bộ (~trưa) | S056 |
| 1783-01-20 | Ký sơ bộ hoà bình tại Paris/Versailles (Montero: 30/1) | S046 |
| 1783-02-02 | Thư Crillon báo sơ bộ hoà bình; ngừng bắn trên thực tế | S045 |
| 1783-02-05 | Bỏ phong toả biển; ~trưa phát súng cuối cùng | S046 |
| 1783-03-10 | Tàu Thetis mang công văn chính thức | S047 |
| 1783-09-03 | Hiệp ước Versailles chung kết; Gibraltar vẫn thuộc Anh | S038 |

## 0d. Số đo cho hero (đường băng, đường hầm)

| Mốc | Chiều dài | Nguồn |
|---|---|---|
| 1934–1936 | None m  (dải cỏ (grass strip), 03/09/1934→10/03/1936; chiều dài KHÔNG có trong nguồn) | HMGoG 199/2018 |
| 1941 (quyết định cuối 11/1941; xong 07/1943) | 1417.3 m  (1550 yd (mục tiêu)) | Gibraltar Parliament motion 17/05/2018; HMGoG 199/2018 |
| 1955 | 1828.8 m  (6000 ft) | HMGoG 199/2018 ("current length of 6000 feet") |
| 2025–2026 (AIRAC 07/25) | 1798 m × 45 m (1798 x 45 m, Blacktop, 087.5°/267.5° true) | UK Mil AIP AD 2.12 LXGB |
| lấn vịnh | 500 m (quinientos metros) | Marquina Barrio 1981 (học thuật TBN) — MỘT NGUỒN — CHƯA ĐỐI CHỨNG nguồn Anh |
| diện tích lấn | — | CHƯA XÁC MINH — không tìm được nguồn tải được nêu diện tích lấn biển. |
| vật liệu lấp | — | Đá nổ từ mặt bắc Khối Đá + đá thải đào hầm, đổ xuống biển (Parliament motion 2018 / HMGoG 199/2018); mỏ đá của kỹ sư Canada sản xuất vật liệu lấp (CMEA); "most of the pieces of rock dug out… used later to fill the terrain at the North Front" (Gingell). |
| hầm (tổng) | 55 km — toàn bộ hầm, thế kỷ 18 → 1960s | HMGoG 310/2017 (Gibraltar Museum lecture) |
| hầm (tổng) | 55 km — toàn bộ hầm | Gibraltar Nature Reserve "Military Tunnels" |
| hầm (tổng) | 34 dặm (≈54,7 km) — toàn bộ hầm | UK Hansard Commons 08/01/2015 (Bob Stewart MP) |
| hầm (tổng) | 50 km ("over 50") — toàn bộ hầm | Gibraltar National Museum guide, Gibraltar Chronicle 05/08/2026 |
| hầm (tổng) | 30 km — chỉ phần đào trong WWII (1940–1943) | Gibraltar National Museum guide, Gibraltar Chronicle 05/08/2026 |
| hầm (tổng) | 50 km ("more than 50") — toàn bộ, 200 năm | CIM Magazine 2018 |
| hầm: great_north_road | ≈1 dặm (≈1,6 km) — CIM 2018, số tròn | |
| hầm: phong_benh_vien_lon_nhat | 200 ft × 35 ft × 12 ft cao ≈ 61,0 × 10,7 × 3,7 m — CMEA | |
| hầm: tiet_dien_ham_dien_hinh | CHƯA XÁC MINH | |
| hầm: sức chứa | 16.000 (Nature Reserve, CIM, Gingell) / 17.000 (hướng dẫn viên Bảo tàng 2026); thời gian: MÂU THUẪN: 1 năm (Nature Reserve) / 16 tháng (CIM) / gần 2 năm (Gingell) | |

## 1. Claims theo nhóm

### Số lần bị vây

**S001** · XÁC MINH · phía: Anh · nhạy cảm: THẤP — con số 14 là quy ước sử học Anh thế kỷ 19, được giữ đến nay. · as of: xuất bản 1862; đọc 2026-10-17 · (gói: V-A1-01)
- Claim (EN): Gibraltar has been besieged fourteen times, from the Castilian capture of 1309 to the Great Siege of 1779–1783.
- Trích nguyên văn (en): > AND AN ACCOUNT OF THE FOURTEEN SIEGES THE ROCK HAS SUSTAINED SINCE IT BECAME A FORTRESS.
- Nguồn: Capt. Frederick Sayer, The History of Gibraltar (London, 1862), title page [thu-cap] · Trang tên sách (title page) · https://archive.org/download/historyofgibralt00sayeuoft/historyofgibralt00sayeuoft_djvu.txt · SHA-256 `3dd2e42aa4bab8f6…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Sayer (thẩm phán dân sự Gibraltar) đánh số 14 cuộc vây kể từ khi Gibraltar "trở thành pháo đài" (1309). Đây là nguồn sớm nhất tìm được cho con số 14. Cách đếm: 1309, 1315, 1333 (Marinid chiếm), 1333 (Alfonso XI phản công), 1349–50, 1411, 1436, 1462, 1466–67, 1506, 1704, 1704–05, 1727, 1779–83. Lưu ý: mục lục của Sayer ghi "TENTH SIEGE, BY MEDITERRANEAN PIRATES" (cuộc tấn công của cướp biển Algiers 1540) nhưng phần thân sách gọi cuộc vây 1506 của Công tước Medina Sidonia là "10th siege" (dòng: "retired from the 10th siege of Gibraltar") — mâu thuẫn nội tại, xem V-A1-03. [Trích đã chuẩn hoá: gộp khoảng trắng/ngắt dòng OCR, nối từ bị gạch nối cuối dòng, ſ→s; không đổi chữ nào khác.]

**S002** · XÁC MINH · phía: Anh · nhạy cảm: THẤP · as of: xuất bản 1870; đọc 2026-10-17 · (gói: V-A1-02)
- Claim (EN): Victorian historians called the Great Siege of 1779–83 the fourteenth siege of Gibraltar.
- Trích nguyên văn (en): > not a few readers will learn for the first time that this victory was the fourteenth of its order.
- Nguồn: [F. G. Stephens], A History of Gibraltar and Its Sieges (London: Provost, 1870), ảnh J. H. Mann [thu-cap] · Introduction, tr. 2; mục lục "The Fourteenth Siege — The Great Siege, 1779-1783" · https://archive.org/download/historyofgibralt00step/historyofgibralt00step_djvu.txt · SHA-256 `4da9d1c355e46516…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Nguồn thứ hai độc lập một phần (có trích Sayer). Mục lục Stephens: "The Eighth Siege, 1462", "The Ninth Siege, 1466", "...The Tenth Siege" (1506 — "the only bloodless one on record"), "The Attack by the Corsairs, 1540" (KHÔNG đánh số), rồi Capture 1704 (= thứ 11), "The Twelfth Siege", "The Thirteenth Siege", "The Fourteenth Siege — The Great Siege". Tác giả: bản scan ghi ảnh của J. H. Mann; định danh archive.org "step" gợi ý F. G. Stephens — cần kiểm thư mục nếu ghi tên tác giả trên màn hình. [Trích đã chuẩn hoá: gộp khoảng trắng/ngắt dòng OCR, nối từ bị gạch nối cuối dòng, ſ→s; không đổi chữ nào khác.]

**S003** · MÂU THUẪN · phía: Anh · nhạy cảm: THẤP · as of: đọc 2026-10-17 · (gói: V-A1-03)
- Claim (EN): The tenth siege, in 1506, was a four-month blockade by the Duke of Medina Sidonia, remembered as the only bloodless siege of Gibraltar.
- Trích nguyên văn (en): > Thus ended the Tenth Siege of Gibraltar, the only bloodless one on record.
- Nguồn: [F. G. Stephens], A History of Gibraltar and Its Sieges (1870) [thu-cap] · Chương "History of Gibraltar under Ferdinand and Isabella. The Tenth Siege", tr. ~204–212 · https://archive.org/download/historyofgibralt00step/historyofgibralt00step_djvu.txt · SHA-256 `4da9d1c355e46516…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Mâu thuẫn nhỏ về cuộc thứ 10: mục lục Sayer 1862 ghi thứ 10 là "by Mediterranean pirates" (1540), nhưng thân sách Sayer (tr. 85) viết "retired from the 10th siege of Gibraltar" về cuộc vây 1506. Stephens 1870 và Wikipedia (dẫn Fa & Finlayson 2006, Osprey) đều coi 1506 là thứ 10 và không đếm 1540. Kết luận: cách đếm chuẩn KHÔNG tính cuộc đột kích 1540. Không nên nhắc số thứ tự từng cuộc trong lời dẫn. [Trích đã chuẩn hoá: gộp khoảng trắng/ngắt dòng OCR, nối từ bị gạch nối cuối dòng, ſ→s; không đổi chữ nào khác.]

**S004** · XÁC MINH · phía: Anh · nhạy cảm: THẤP · as of: trang web © 2019; đọc 2026-10-17 · (gói: V-A1-04)
- Claim (EN): The Gibraltar National Museum numbers the 1462 Castilian conquest as the eighth siege, the 1704–05 Spanish counter-attack as the twelfth, 1727 as the thirteenth, and calls the Great Siege of 1779–83 the last.
- Trích nguyên văn (en): > A Spanish attempt to re-capture the Rock between 1704 and 1705 (twelfth siege of Gibraltar) failed and the Spanish Crown ceded Gibraltar to the Crown of Great Britain ‘in perpetuity’ under the Treaty of Utrecht in 1713. Despite the truce, they laid siege to Gibraltar again in 1727 (thirteenth siege of Gibraltar). … The last siege, known as the Great Siege (1779-83), saw large-scale destruction of the city by Spanish and French artillery.
- Nguồn: Gibraltar National Museum, "Brief History of Gibraltar" (web) [bao-tang] · Mục 1704–1783 và mục Great Siege (1779-83) · https://www.gibmuseum.gi/our-history/brief-history-of-gibraltar · SHA-256 `8d5ce1f1db2ba73f…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Bảo tàng Quốc gia Gibraltar không nêu tổng "14" trên các trang đã tải, nhưng cách đánh số (8 = 1462, 12 = 1704–05, 13 = 1727, cuộc Great Siege là "last") khớp đúng với hệ đếm 14 của Sayer/Stephens. Cùng trang: "finally ousted by the Catholic Monarchs in 1462 during the eighth siege" (lưu ý: năm 1462 thực tế dưới thời Enrique IV, không phải "Catholic Monarchs" — lỗi của trang; không dùng cụm này).

**S005** · MÂU THUẪN · phía: Anh · nhạy cảm: THẤP · as of: đọc 2026-10-17 · (gói: V-A1-05)
- Claim (EN): The museum dates the second siege to 1316 and says Castile held out.
- Trích nguyên văn (en): > In 1309 Castile besieged and captured Gibraltar after little more than two months, in what would later become known as the First Siege of Gibraltar. … The Second Siege came as soon as 1316 but Castile held out. Acknowledging the the Rock's precarious survival, Ferdinand IV of Castile invested heavily in the city's defences, extending and reinforcing the walls and towers, and building a dry dock (atarazana). Nevertheless, the Marinīds were successful in the Third Siege of Gibraltar of 1333
- Nguồn: Gibraltar National Museum, "Fortifications of Gibraltar" (web) [bao-tang] · Đoạn về thời Trung cổ · https://www.gibmuseum.gi/our-history/military-history/fortifications-of-gibraltar · SHA-256 `1f07ff65b93462b6…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Năm của cuộc vây thứ 2: bảo tàng ghi 1316; Sayer 1862 (tr. 19: "In 1315") và Stephens 1870 ("A.D. 1315") ghi 1315. Không ảnh hưởng tổng số. Nếu cần nêu năm, dùng "around 1315". Bảo tàng cũng ghi cuộc vây 1309 kéo dài "little more than two months", Wikipedia ghi khoảng một tháng — không cần nêu thời lượng.

**S006** · XÁC MINH · phía: TBN · nhạy cảm: THẤP — học giả Tây Ban Nha (ĐH Sevilla) dùng cùng hệ đếm với sử Anh. · as of: đọc 2026-10-17 · (gói: V-A1-06)
- Claim (EN): A modern Spanish academic history also counts the 1704 attack as the eleventh siege of Gibraltar.
- Trích nguyên văn (es): > En el verano de 1704 se llevó a cabo el undécimo asedio sobre Gibraltar, contando desde que el Estrecho se convirtiera en punto neurálgico de la Reconquista castellana durante la Edad Media.
- Nguồn: Carolina García Sanz, Historia de Gibraltar (Madrid: Los Libros de la Catarata, 2022), cap. 2 [hoc-thuat] · Chương 2, đoạn mở đầu về Chiến tranh Kế vị · https://archive.org/download/garcia-sanz-c.-historia-de-gibraltar-madrid-2022./Garc%C3%ADa%20Sanz%2C%20C.-Historia%20de%20Gibraltar%2C%20Madrid%2C%202022.%20180%20pp._djvu.txt · SHA-256 `2357d695b5be8c3f…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Xác nhận hai phía dùng cùng hệ đếm (1704 = thứ 11 ⇒ tổng 14 đến 1783). LƯU Ý QUYỀN: bản trên archive.org do người dùng tải lên, sách còn bản quyền (ISBN 978-84-1352-368-2). Chỉ dùng để kiểm chứng/trích ngắn có ghi nguồn; nên đối chiếu bản in trước khi trích lên phim. [Trích đã chuẩn hoá: gộp khoảng trắng/ngắt dòng OCR, nối từ bị gạch nối cuối dòng, ſ→s; không đổi chữ nào khác.]

**S007** · CHƯA XÁC MINH · phía: trung-lap · nhạy cảm: TRUNG — "fifteenth siege" là cách nói chính trị của phía Gibraltar/Anh; phía TBN không gọi như vậy. · as of: đọc 2026-10-17 · (gói: V-A1-07)
- Claim (EN): Some historians describe Spain’s 1969–1985 closure of the border as a “fifteenth siege”, but it was not a military siege.
- Trích nguyên văn (en): > Some historians discuss the closure of the Gibraltar–Spain border (part of an attempt by Spain to coerce the United Kingdom into ceding Gibraltar) from 1969 to 1985 as a "fifteenth siege";[22] as this differs from the other fourteen sieges in that it was not a conflict between opposing militaries, it is not included in this list.
- Nguồn: Wikipedia, "List of sieges of Gibraltar" (dẫn Jackson 1987, tr. 317) [bach-khoa] · Phần mở đầu, đoạn cuối "Background" · https://en.wikipedia.org/wiki/List_of_sieges_of_Gibraltar · SHA-256 `30c08b13d96c9727…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Chỉ có nguồn bách khoa (thứ cấp cấp 3), dẫn Sir William Jackson, The Rock of the Gibraltarians (1987), tr. 317 — chưa tải được sách gốc. Không dùng trong lời dẫn trừ khi xác minh được nguyên văn Jackson; nếu dùng, phải gắn "some Gibraltarians called it…".

**S008** · XÁC MINH · phía: trung-lap · nhạy cảm: THẤP · as of: đọc 2026-10-17 · (gói: V-A1-08)
- Claim (EN): The most-cited modern list gives fourteen recorded sieges and states that only five resulted in a change of rule.
- Trích nguyên văn (en): > There have been fourteen recorded sieges of Gibraltar. Although the peninsula of Gibraltar is only 6 kilometres (3.7 mi) long and 1 kilometre (0.62 mi) wide, it occupies an extremely strategic location on the southern Iberian coast at the western entrance to the Mediterranean Sea. Its position just across the eponymous Strait from Morocco in North Africa, as well as its natural defensibility, have made it one of the most fought-over places in Europe. Only five of the sieges resulted in a change of rule. Seven were fought between Muslims and Catholics during Muslim rule, four between Spain and Britain from the Anglo-Dutch capture in 1704 to the end of the Great Siege in 1783, two between rival Catholic factions, and one between rival Muslim powers.
- Nguồn: Wikipedia, "List of sieges of Gibraltar" (dẫn Fa & Finlayson 2006; Hills 1974) [bach-khoa] · Đoạn mở đầu · https://en.wikipedia.org/wiki/List_of_sieges_of_Gibraltar · SHA-256 `30c08b13d96c9727…`
- Kiểm độc lập: khớp theo mảnh (1 mảnh lệch do OCR/ngắt dòng) — đối chiếu ảnh trang
- Ghi chú: Nguồn cấp 3, chỉ dùng để đối chiếu danh sách; số 14 đã được xác minh độc lập ở V-A1-01/02/04/06. Ý "chỉ 5 cuộc đổi chủ" (dẫn Hills 1974, tr. 95) CHƯA kiểm được sách gốc — theo danh sách: 1309, 1333 (Feb–Jun), 1411, 1462, 1704 là 5 lần đổi chủ qua vây; 1466–67 là tranh giành giữa phe Castile (đổi người nắm giữ nhưng không đổi "vương quyền") — vì vậy tránh nói "five" trong lời.

### Vì sao Rock có giá

**S009** · XÁC MINH · phía: trung-lap · nhạy cảm: THẤP · as of: đọc 2026-10-17 · (gói: V-A1-34)
- Claim (EN): Gibraltar sits at the western entrance to the Mediterranean, just across the Strait from Morocco — a position that has made it one of the most fought-over places in Europe.
- Trích nguyên văn (en): > it occupies an extremely strategic location on the southern Iberian coast at the western entrance to the Mediterranean Sea. Its position just across the eponymous Strait from Morocco in North Africa, as well as its natural defensibility, have made it one of the most fought-over places in Europe.
- Nguồn: Wikipedia "List of sieges of Gibraltar" (dẫn Fa & Finlayson 2006, tr. 4–5; Rose 2001, tr. 95) [bach-khoa] · Đoạn mở đầu · https://en.wikipedia.org/wiki/List_of_sieges_of_Gibraltar · SHA-256 `30c08b13d96c9727…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Nguồn cấp 3 nhưng nội dung là địa lý không tranh cãi. Phiên bản học thuật TBN tương đương: García Sanz 2022, cap. 1: "una privilegiada posición geopolítica, entre el Atlántico y el Mediterráneo, entre Europa y África".

**S010** · XÁC MINH · phía: ca-hai · nhạy cảm: TRUNG — câu Sayer gắn với giai thoại hạ cờ Habsburg (V-A1-17) đang bị nghi vấn; chỉ dùng cụm "key of the Mediterranean" như cách nhìn của người viết thế kỷ 19, không gán cho Rooke. · as of: đọc 2026-10-17 · (gói: V-A1-35)
- Claim (EN): For British writers Gibraltar was “the key of the Mediterranean”; for Spanish writers, “la preciosa llave del Mediterráneo” — the same image from both sides.
- Trích nguyên văn (en): > But Sir George Rooke was too well aware of the value of Gibraltar to the English nation as the key of the Mediterranean, || Tal fué el primer esfuerzo que hicieron los españoles para recobrar la preciosa llave del Mediterráneo
- Nguồn: Sayer 1862, tr. 114; Montero 1860, tr. 293 [thu-cap] · Sayer tr. 114; Montero tr. 293 · https://archive.org/download/historyofgibralt00sayeuoft/historyofgibralt00sayeuoft_djvu.txt ; https://archive.org/download/historiadegibra00montgoog/historiadegibra00montgoog_djvu.txt · SHA-256 `3dd2e42aa4bab8f6…`
- Kiểm độc lập: khớp theo mảnh (1 mảnh lệch do OCR/ngắt dòng) — đối chiếu ảnh trang
- Ghi chú: Hai nguồn thế kỷ 19 từ hai phía cùng dùng hình ảnh "chìa khoá" — thích hợp làm mô-típ (cũng khớp huy hiệu "Castle and Key" do Isabel I ban năm 1502 theo Bảo tàng Gibraltar). Montero OCR: "españo- les" bị cắt dòng; trích dừng tại "españo" + đoạn sau. [Trích đã chuẩn hoá: gộp khoảng trắng/ngắt dòng OCR, nối từ bị gạch nối cuối dòng, ſ→s; không đổi chữ nào khác.]

**S011** · CHƯA XÁC MINH · phía: Anh · nhạy cảm: THẤP · as of: đọc 2026-10-17 · (gói: V-A1-36)
- Claim (EN): Even at the time, some in Britain doubted Gibraltar was worth its cost — but, as Bishop Burnet observed, Spain spent far more men and money trying to win it back.
- Trích nguyên văn (en): > It has been much questioned by men who understand these matters well, whether our possessing ourselves of Gibraltar, and our maintaining ourselves in it so long, were to our advantage or not. It has certainly put us to a great charge, and we have lost many men in it ; but it seems, the Spaniards, who should know the importance of the place best, think it so valuable that they have been at a much greater charge, and have lost many more men while they have endeavoured to recover it, than the taking and keeping it has cost us.
- Nguồn: Gilbert Burnet, History of His Own Time (1724–34), trích lại trong Sayer 1862, tr. 114–115 [thu-cap] · Sayer tr. 114–115 · https://archive.org/download/historyofgibralt00sayeuoft/historyofgibralt00sayeuoft_djvu.txt · SHA-256 `3dd2e42aa4bab8f6…`
- Kiểm độc lập: khớp theo mảnh (1 mảnh lệch do OCR/ngắt dòng) — đối chiếu ảnh trang
- Ghi chú: Nguyên văn lấy qua trích dẫn của Sayer, chưa đối chiếu bản gốc Burnet (archive.org có "Bishop Burnet's History of his own time", 1753 — chưa tải). Nên đối chiếu trước khi đặt lên màn hình. Lý do chiến lược trực tiếp năm 1704 (hội đồng chiến tranh của Rooke): "Because the possession of such an important fortress would be of infinite value during the war." (Sayer tr. 102, xem V-A1-09). [Trích đã chuẩn hoá: gộp khoảng trắng/ngắt dòng OCR, nối từ bị gạch nối cuối dòng, ſ→s; không đổi chữ nào khác.]

### 1704 — chiếm Rock

**S012** · XÁC MINH · phía: Anh · nhạy cảm: TRUNG — lịch O.S./N.S. dễ gây sai; luôn nói lịch N.S. (1–4 August 1704) hoặc ghi rõ cả hai. · as of: đọc 2026-10-17 · (gói: V-A1-09)
- Claim (EN): The Anglo-Dutch fleet under Admiral Sir George Rooke anchored in the Bay of Gibraltar on 21 July 1704 by the English (Old Style) calendar — 1 August by the Spanish (New Style) calendar.
- Trích nguyên văn (en): > it was resolved to make a sudden attack upon Gibraltar, for the three following reasons : — First. Because the place was so indifferently garrisoned that there was every probability of the attack succeeding. Secondly. Because the possession of such an important fortress would be of infinite value during the war. Thirdly. Because the capture of the place would add a lustre to the queen's arms, and would be likely to dispose the Spaniards in favour of the cause of the Archduke Charles. Pour days were spent in making the necessary preparations, and on the 21st July the fleet, consisting of the following vessels, anchored in the Bay of Gibraltar.
- Nguồn: Sayer 1862, ch. VI (tr. 101–102) [thu-cap] · Ch. VI, tr. 101–102 · https://archive.org/download/historyofgibralt00sayeuoft/historyofgibralt00sayeuoft_djvu.txt · SHA-256 `3dd2e42aa4bab8f6…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Ba lý do của hội đồng chiến tranh 17/7 O.S. (dân phòng yếu; giá trị chiến lược; làm người TBN ngả về Archduke Charles) cũng có thể dùng cho V-A1-29. Đối chiếu N.S.: thư của thành phố Gibraltar gửi Hầu tước Villadarias ngày "agosto 2 de 1704" nói hạm đội đến "ayer que se contó primero de agosto" (Montero 1860, tr. 264, chú thích) ⇒ 21/7 O.S. = 1/8 N.S. (chênh 11 ngày). GHT ghi "31st July" — xem V-A1-14. [Trích đã chuẩn hoá: gộp khoảng trắng/ngắt dòng OCR, nối từ bị gạch nối cuối dòng, ſ→s; không đổi chữ nào khác.]

**S013** · XÁC MINH · phía: ca-hai · nhạy cảm: THẤP · as of: đọc 2026-10-17 · (gói: V-A1-10)
- Claim (EN): Spanish and English histories give different dates for the fall of Gibraltar — 4 August and 24 July 1704 — because England still used the Julian calendar.
- Trích nguyên văn (en): > All the Spanish authors give the 4th August, 1704, as the day on which Gribraltar surrendered to Eooke, and they seem to have been unable to understand why all the English historians agree that the 24th July was the day on which the place fell. … The apparent discrepancy is however very simply accounted for by the fact that the Gregorian calculation was adopted in Spain before the year 1704, while it was not introduced into the English calendar till long afterwards.
- Nguồn: Sayer 1862, tr. 113–114 (chú thích, trích Montero tr. 265) [thu-cap] · Tr. 113, chú thích * · https://archive.org/download/historyofgibralt00sayeuoft/historyofgibralt00sayeuoft_djvu.txt · SHA-256 `3dd2e42aa4bab8f6…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: OCR: "Gribraltar" = Gibraltar, "Eooke" = Rooke (giữ nguyên lỗi OCR trong trích). Mốc chuẩn cho lời dẫn (N.S.): đổ bộ chiều 1/8/1704; pháo kích ngày 3/8 (Chủ nhật — kiểm bằng lịch Gregorius); đầu hàng sáng 4/8. O.S.: 21, 23, 24/7. Văn kiện đầu hàng Sayer chép ký "George, Landgrave of Hesse. July 24th, 1704." Montero (tr. 265) viết "Al amanecer del domingo cuatro" — lệch một ngày so với lịch (3/8/1704 mới là Chủ nhật), nên không dựa vào Montero cho ngày pháo kích. [Trích đã chuẩn hoá: gộp khoảng trắng/ngắt dòng OCR, nối từ bị gạch nối cuối dòng, ſ→s; không đổi chữ nào khác.]

**S014** · MÂU THUẪN · phía: Anh · nhạy cảm: TRUNG — quân số phòng thủ là điểm tự hào/tranh cãi của cả hai phía. · as of: đọc 2026-10-17 · (gói: V-A1-11)
- Claim (EN): Governor Diego de Salinas had barely a hundred regular soldiers; British accounts put the whole defence, armed townsmen included, at no more than about five hundred.
- Trích nguyên văn (en): > There were not more than 150 regulars inside the walls, very few of whom were artillerymen ; and the whole force that could be mustered, including the armed citizens, did not exceed 500 men.
- Nguồn: Sayer 1862, tr. 106–107 (dẫn Montero, Ayala) [thu-cap] · Ch. VI, tr. 106–107 · https://archive.org/download/historyofgibralt00sayeuoft/historyofgibralt00sayeuoft_djvu.txt · SHA-256 `3dd2e42aa4bab8f6…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Các con số khác nhau: Sayer: ≤150 lính chính quy, tổng ≤500 kể cả dân vũ trang. Montero 1860 (phía TBN, V-A1-12): "apenas … cien hombres de guarnición", cộng ~400 dân được vũ trang và 70 lính trong lâu đài. García Sanz 2022 (V-A1-13): "una guarnición escasa", ~4.000 dân, "aproximadamente 1.000 podrían haber tomado las armas". Lời dẫn an toàn: "a garrison of only a few hundred men, most of them armed townspeople". [Trích đã chuẩn hoá: gộp khoảng trắng/ngắt dòng OCR, nối từ bị gạch nối cuối dòng, ſ→s; không đổi chữ nào khác.]

**S015** · XÁC MINH · phía: TBN · nhạy cảm: TRUNG · as of: đọc 2026-10-17 · (gói: V-A1-12)
- Claim (EN): A Spanish historian of 1860 wrote that Gibraltar had barely a hundred garrison soldiers in 1704, and that its hundred guns were mostly dismounted and lacked gunners.
- Trích nguyên văn (es): > llegada la ocasión que Yilladarias creía imposible i penas contaba» empacho da escribirlo» con cien hombres de guarnición la plaaa; y aunque con cien piezas de artillería en su recinto, como estaban en su mayor parte desmontadas y aun sin eso, como no había artilleros que las sirvieran, venían a ser casi del todo inútiles.
- Nguồn: Francisco María Montero, Historia de Gibraltar y de su campo (Cádiz, 1860), tr. 263–264 [thu-cap] · Parte III, tr. 263 · https://archive.org/download/historiadegibra00montgoog/historiadegibra00montgoog_djvu.txt · SHA-256 `a9b8f6b07ee075c9…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: OCR có lỗi ("empacho da escribirlo", "plaaa" = plaza). Trích để đối chiếu, nếu đưa lên hình cần soát bản scan PDF cùng mã archive. Cùng trang Montero kể Salinas đã lên Madrid xin tăng viện nhưng không được. [Trích đã chuẩn hoá: gộp khoảng trắng/ngắt dòng OCR, nối từ bị gạch nối cuối dòng, ſ→s; không đổi chữ nào khác.]

**S016** · MÂU THUẪN · phía: TBN · nhạy cảm: TRUNG · as of: đọc 2026-10-17 · (gói: V-A1-13)
- Claim (EN): On 1 August 1704 Governor Diego de Salinas refused the allied ultimatum, and the town was then hit by more than fifteen thousand cannon shots.
- Trích nguyên văn (es): > El 1 de agosto Diego de Salinas (1649-1720), máxima autoridad militar de la plaza y representante del rey, recibió un ultimátum de la flota enemiga. Ante su negativa a aceptarlo, durante unas pocas horas de la noche, más de 15.000 cañonazos fueron lanzados contra la ciudad
- Nguồn: García Sanz 2022, cap. 2.1 [hoc-thuat] · Chương 2, mục về cuộc chiếm 1704 · https://archive.org/download/garcia-sanz-c.-historia-de-gibraltar-madrid-2022./Garc%C3%ADa%20Sanz%2C%20C.-Historia%20de%20Gibraltar%2C%20Madrid%2C%202022.%20180%20pp._djvu.txt · SHA-256 `2357d695b5be8c3f…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Số đạn: Sayer 1862 "not less than 15,000 shot" trong 6 giờ; Montero "sobre quince mil balas" (ghi Ayala nói 30.000); GHT (V-A1-14) ghi "1,500 cannon shot" — gần như chắc lỗi đánh máy của trang giáo dục. García Sanz nói "durante unas pocas horas de la noche" trong khi các nguồn khác nói pháo kích bắt đầu lúc rạng sáng 3/8 (N.S.) — mâu thuẫn về thời điểm. Lời dẫn an toàn: "some fifteen thousand rounds in about six hours". Cùng nguồn: hạm đội "más de 60 barcos y 3.000 cañones", ~2.000 lính thuỷ đánh bộ Anh–Hà Lan dưới quyền Hoàng tử Georg von Hessen-Darmstadt "en calidad de representante del aspirante austriaco". [Trích đã chuẩn hoá: gộp khoảng trắng/ngắt dòng OCR, nối từ bị gạch nối cuối dòng, ſ→s; không đổi chữ nào khác.]

**S017** · MÂU THUẪN · phía: Anh · nhạy cảm: TRUNG — trang giáo dục có nhiều lỗi; chỉ dùng cho nội dung đã được nguồn khác xác nhận. · as of: đọc 2026-10-17 · (gói: V-A1-14)
- Claim (EN): Prince George of Hesse-Darmstadt took possession of Gibraltar in the name of the Habsburg claimant, “Charles III of Spain”, and almost the entire Spanish population left the town.
- Trích nguyên văn (en): > On the 31st July (see Discussion point ), the combined Anglo- Dutch fleet, under Admiral Sir George Rooke, entered Gibraltar Bay. At 3pm, 1,800 English and Dutch marines were landed on the isthmus with the Dutch Prince Hesse at the head. Gibraltar was cut off but the Spanish Governor of Gibraltar refused to surrender. The days that followed saw a massive bombardment of the town by the English fleet and on the morning of the 3rd August, 1,500 cannon shot were fired in 5-6 hours against the town. Landings took place in the south and in the morning of the 4th, the Spanish Governor finally capitulated. Hesse took possession of Gibraltar in the name of Charles III of Spain after four days of fighting. Almost the entire population of Gibraltar, except around fifty families, left the town and settled in the nearby areas such as Algeciras, Los Barrios and around the small church of San Roque.
- Nguồn: Gibraltar Heritage Trust, The Great Siege — Schools resource, Chapter 1 "Why is Gibraltar British?" [bao-tang] · Chapter 1, đoạn 3 · https://schools.gibraltarheritagetrust.org.gi/siege/chapter-01.html · SHA-256 `db3f6f128a18257b…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Lỗi đã phát hiện trong trang GHT: (1) "31st July" — trang giải thích là ngày theo lịch Tây Ban Nha, nhưng Sayer/Montero cho N.S. = 1/8 (31/7 có thể là ngày hạm đội xuất hiện ngoài khơi); (2) "the Dutch Prince Hesse" — Georg von Hessen-Darmstadt là hoàng tử Đức phục vụ nhà Habsburg, không phải người Hà Lan; (3) "1,500 cannon shot" (các nguồn khác 15.000); (4) mục tiêu học tập ghi "Treaty of Utrecht in 1704". Ý dùng được: chiếm "in the name of Charles III of Spain" và dân bỏ đi trừ "around fifty families" — con số 50 gia đình chưa có nguồn thứ hai (Montero nói chỉ còn "una mujer y algunos ancianos enfermos"; Sayer: "but few inhabitants"). Lời an toàn: "almost the entire Spanish population chose to leave".

**S018** · XÁC MINH · phía: Anh · nhạy cảm: TRUNG · as of: đọc 2026-10-17 · (gói: V-A1-15)
- Claim (EN): The capitulation let the garrison march out with arms and baggage, and promised inhabitants who stayed their old privileges and religion — if they swore allegiance to “Charles III”.
- Trích nguyên văn (en): > The officers and soldiers shall be allowed to march out with their baggage, and the soldiers may take what they can carry with them ; the officers, the magistrates, and gentlemen are allowed to take their horses : and for those without baggage who choose to depart by water vessels shall be provided. … To the inhabitants, soldiers, and officers, who may choose to remain in Gibraltar, shall be conceded the same privileges they had in the time of Charles 11. ; the religion and all the tribunals shall remain intact and without alteration, it being understood that the oath of fidelity to H. M. Charles III., as legitimate lord and king, is to be taken.
- Nguồn: Sayer 1862, tr. 112–113 (bản dịch Anh các Điều khoản đầu hàng) [thu-cap] · Ch. VI, "Articles of Capitulation", Art. I và V · https://archive.org/download/historyofgibralt00sayeuoft/historyofgibralt00sayeuoft_djvu.txt · SHA-256 `3dd2e42aa4bab8f6…`
- Kiểm độc lập: khớp theo mảnh (1 mảnh lệch do OCR/ngắt dòng) — đối chiếu ảnh trang
- Ghi chú: Bản tiếng Tây Ban Nha của cùng các điều khoản có trong Montero 1860, tr. 267–269 (chú thích 3, "Artículo 1°… Artículo 6°", nguồn "Archivo de San Roque"), nội dung khớp: ra đi với vũ khí, hành lý, 3 khẩu pháo đồng, lương thực 6 ngày, ai ở lại giữ đặc quyền thời Carlos II nếu thề trung thành với Carlos III. OCR: "Charles 11." = Charles II. Bản dịch ở Sayer là bản dịch thế kỷ 19, không phải văn bản gốc. [Trích đã chuẩn hoá: gộp khoảng trắng/ngắt dòng OCR, nối từ bị gạch nối cuối dòng, ſ→s; không đổi chữ nào khác.]

**S019** · XÁC MINH · phía: TBN · nhạy cảm: TRUNG — câu chuyện "thành phố Gibraltar lưu vong ở San Roque" là bản sắc của phía TBN. · as of: đọc 2026-10-17 · (gói: V-A1-16)
- Claim (EN): Spanish accounts stress that the townspeople chose exile rather than live under a foreign power, and that the largest group settled by the hermitage of San Roque.
- Trích nguyên văn (es): > el grupo mas numeroso de los fugitivos de la plaza se habia acampado en las haciendas cercanas á la ermita de San Roque distante una legua al N. E. de aquella; antiguo santuario edificado sobre una colina cuyos contornos estaban cubiertos de viñedos y caseríos. Acudian á él los trabajadores en los dias festivos y su Patrono gozaba de mucha veneración entre ellos, particularmente desde la epidemia que afligió á Gibraltar en 1G49. Era, pues, un lugar ameno y de recuerdos gratos, por cuya razón fuéronse reuniendo en él muchos de los dispersos, quienes edificaron junto á la misma ermita chozas, barracas y mas tarde edificios de piedra. Tales fueron los principios de San Roque.
- Nguồn: Montero 1860, Parte IV cap. IV "Fundación de San Roque…", tr. 323–324 [thu-cap] · Tr. 323–324 · https://archive.org/download/historiadegibra00montgoog/historiadegibra00montgoog_djvu.txt · SHA-256 `a9b8f6b07ee075c9…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Montero cũng viết: "Hubo, pues, dos ciudades de Gibraltar; una material ocupada por los ingleses, y otra moral compuesta de españoles" (tr. 323) — câu rất giàu hình ảnh cho phim (nguồn TBN thế kỷ 19, phải gắn "a Spanish historian wrote"). García Sanz 2022 xác nhận: "Los refugiados gibraltareños dieron origen a nuevas poblaciones en el Campo de Gibraltar, como San Roque junto a la ermita del mismo nombre y Los Barrios." [Trích đã chuẩn hoá: gộp khoảng trắng/ngắt dòng OCR, nối từ bị gạch nối cuối dòng, ſ→s; không đổi chữ nào khác.]

**S020** · MÂU THUẪN · phía: TBN · nhạy cảm: CAO — chuyện Rooke "hạ cờ Habsburg, kéo cờ Anh, chiếm nhân danh Nữ hoàng Anne" là huyền thoại gây tranh cãi. · as of: đọc 2026-10-17 · (gói: V-A1-17)
- Claim (EN): Gibraltar was taken in the name of the Habsburg claimant Charles III; the ceremonial sovereignty of the Austrian candidate was kept up until 1709.
- Trích nguyên văn (es): > el 4 de agosto el almirante Rooke conquistó la plaza para Carlos III, aunque izaría sobre la Torre del Hacho —según la costumbre naval— la bandera inglesa … La soberanía del rey austriaco se mantuvo se forma ceremonial hasta 1709
- Nguồn: García Sanz 2022, cap. 2 và chú thích 13 (dẫn Sáez Rodríguez 2015; Hills 1974) [hoc-thuat] · Chương 2 + chú thích 13 · https://archive.org/download/garcia-sanz-c.-historia-de-gibraltar-madrid-2022./Garc%C3%ADa%20Sanz%2C%20C.-Historia%20de%20Gibraltar%2C%20Madrid%2C%202022.%20180%20pp._djvu.txt · SHA-256 `2357d695b5be8c3f…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Sayer 1862 (tr. 114) và Montero 1860 (tr. 268) đều kể Rooke cho hạ cờ Áo, kéo cờ Anh và chiếm thành "in the name of Queen Anne". García Sanz 2022 (dựa trên nghiên cứu mới) nói Rooke chiếm "para Carlos III", chỉ kéo cờ Anh trên Torre del Hacho "según la costumbre naval", và chủ quyền nghi lễ của vua Áo duy trì đến 1709. Lời an toàn: "captured in the name of the Habsburg claimant; within a few years it was effectively a British garrison". Tránh kể chuyện đổi cờ như sự thật. [Trích đã chuẩn hoá: gộp khoảng trắng/ngắt dòng OCR, nối từ bị gạch nối cuối dòng, ſ→s; không đổi chữ nào khác.]

**S021** · MÂU THUẪN · phía: Anh · nhạy cảm: THẤP · as of: đọc 2026-10-17 · (gói: V-A1-18)
- Claim (EN): Within weeks Spain and France counter-attacked: the Marquis of Villadarias besieged the Rock from the isthmus, then Marshal Tessé took command in February 1705, and the siege was given up in spring 1705.
- Trích nguyên văn (en): > The expedition was composed of 12,000 men, 9000 Spaniards and 3000 French, the whole under the command of the Marquis de Villadarias, a brave and able soldier. … On the 8th February, the Marshal arrived before Gibraltar, bringing with him a reinforcement of 4000 men, … On the 18th April, 1705, the siege was raised, a small force of Spaniards only remaining to preserve the blockade.
- Nguồn: Sayer 1862, ch. VIII "Twelfth Siege, by Spain", tr. 128–147 [thu-cap] · Tr. 128, 143, 147 · https://archive.org/download/historyofgibralt00sayeuoft/historyofgibralt00sayeuoft_djvu.txt · SHA-256 `3dd2e42aa4bab8f6…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Ngày kết thúc khác nhau: Sayer và Stephens: 18/4/1705 (gần như chắc là O.S. ⇒ ~29/4 N.S.); Wikipedia: 31/3/1705. Montero (phía TBN) chỉ nói "Duró el sitio cerca de ocho meses", tổn thất "de nueve á diez mil hombres", ném vào thành "ocho mil bombas y mas de setenta mil balas de cañon" và gọi Gibraltar là "la preciosa llave del Mediterráneo". Khởi đầu: Stephens ghi chiến hào mở ngày 9/10 (1704); Wikipedia ghi 3/9/1704 Villadarias đến eo đất. Lời an toàn: "from autumn 1704 to spring 1705". Quân số 12.000 (9.000 TBN + 3.000 Pháp) là số của Sayer, Wikipedia nói ~7.000 vào cuối tháng 10 — không nêu số trong lời. [Trích đã chuẩn hoá: gộp khoảng trắng/ngắt dòng OCR, nối từ bị gạch nối cuối dòng, ſ→s; không đổi chữ nào khác.]

### Utrecht 1713, Điều X

**S022** · XÁC MINH · phía: trung-lap · nhạy cảm: CAO — ngôn từ Điều X là cốt lõi tranh chấp chủ quyền. · as of: văn bản 13/7/1713 (N.S.); bản in 1785; đọc 2026-10-17 · (gói: V-A1-19)
- Claim (EN): Under Article X of the Treaty of Utrecht, signed on 13 July 1713, Spain’s king yielded to the British Crown “the full and entire propriety of the town and castle of Gibraltar, together with the port, fortifications, and forts thereunto belonging”, to be held “for ever”.
- Trích nguyên văn (en): > X. The Catholic King does hereby, for himself, his heirs and successors, yield to the crown of Great Britain the full and entire propriety of the town and castle of Gibraltar, together with the port, fortifications, and forts thereunto belonging; and he gives up the said' propriety to be held and enjoyed absolutely with all manner of right for ever, without any exception or impediment whatsoever
- Nguồn: Treaty of Peace and Friendship between Anne … and Philip V … concluded at Utrecht, 2/13 July 1713, "Reprinted from the Copy published by the Queen's special Command", in [Charles Jenkinson], A Collection of All the Treaties of Peace, Alliance, and Commerce, between Great-Britain and Other Powers, vol. II (London, 1785) [so-cap] · Vol. II, Treaty of Peace with Spain 1713, Art. X (≈ tr. 87–88 bản in) · https://archive.org/download/bim_eighteenth-century_a-collection-of-all-the-_1785_2/bim_eighteenth-century_a-collection-of-all-the-_1785_2_djvu.txt · SHA-256 `121bd2712b4f45db…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Bản dịch Anh chính thức đương thời (in theo lệnh Nữ hoàng 1713). Văn bản gốc có giá trị pháp lý là tiếng Latinh (Elcano, V-A1-24). Đối chiếu độc lập: Chalmers, A Collection of Treaties… vol. II (London, 1790) — cùng từng chữ (OCR: "tov/n", "caftle", nhưng nội dung trùng). "Gib- raltar" đã nối. Ngày: tiêu đề Jenkinson ghi "the 2/13 Day of July 1713" (O.S./N.S.); chính quyền Gibraltar (V-A1-25) và MAEC TBN (V-A1-26) đều ghi 13/7/1713. [Trích đã chuẩn hoá: gộp khoảng trắng/ngắt dòng OCR, nối từ bị gạch nối cuối dòng, ſ→s; không đổi chữ nào khác.]

**S023** · XÁC MINH · phía: trung-lap · nhạy cảm: CAO — TBN dựa vào cụm "without any territorial jurisdiction" để khẳng định eo đất, vùng biển, vùng trời không được nhượng; Anh coi Gibraltar gồm cả eo đất (V-A1-27, V-A1-28). · as of: văn bản 13/7/1713; đọc 2026-10-17 · (gói: V-A1-20)
- Claim (EN): Article X added that the cession was made “without any territorial jurisdiction, and without any open communication by land with the country round about”.
- Trích nguyên văn (en): > But that abuses and frauds may be avoided by importing any kinds of goods, the Catholic King wills, and takes it to be understood, that the abovenamed propriety be yielded to Great Britain, without any territorial jurisdiction, and without any open communication by land with the country round about
- Nguồn: Jenkinson (ed.), Collection of Treaties, vol. II (1785) — Treaty of Utrecht 1713, Art. X [so-cap] · Art. X, câu 2 · https://archive.org/download/bim_eighteenth-century_a-collection-of-all-the-_1785_2/bim_eighteenth-century_a-collection-of-all-the-_1785_2_djvu.txt · SHA-256 `121bd2712b4f45db…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Mục đích nêu trong chính điều khoản: chống buôn lậu ("that abuses and frauds may be avoided by importing any kinds of goods"). Trong lời dẫn nên nói rõ mục đích này để không thiên lệch. Chalmers 1790 có câu giống hệt ("without any territorial jurifdiftion" — lỗi OCR). [Trích đã chuẩn hoá: gộp khoảng trắng/ngắt dòng OCR, nối từ bị gạch nối cuối dòng, ſ→s; không đổi chữ nào khác.]

**S024** · XÁC MINH · phía: trung-lap · nhạy cảm: CAO — điều khoản phân biệt tôn giáo; trình bày như sự kiện lịch sử, không bình luận thay nhân vật. Trên thực tế cộng đồng Do Thái đã sống ở Gibraltar từ thế kỷ 18 (García Sanz nhắc vị thế người Do Thái mạnh lên sau 1727) — cần nguồn riêng nếu nói. · as of: văn bản 13/7/1713; bản in 1790; đọc 2026-10-17 · (gói: V-A1-21)
- Claim (EN): At Spain’s request, Article X barred Jews and Moors from living in Gibraltar, and promised freedom of worship to its Roman Catholic inhabitants.
- Trích nguyên văn (en): > And her Britannic Majefty, at the requeft of the Catholic King, does content and agr<ee, that no leave fhall be given, under any pretence whatfoever, either to Jews or Moors, 10 refide or have their dwellings in the faid town of. Gibraltar ;
- Nguồn: Chalmers (ed.), A Collection of Treaties between Great Britain and Other Powers, vol. II (London, 1790) — Treaty with Spain 1713, Art. X [so-cap] · Vol. II, tr. 83–84 (Art. X) · https://archive.org/download/collectionoftrea02greaiala/collectionoftrea02greaiala_djvu.txt · SHA-256 `1ee7fe1376174aba…`
- Kiểm độc lập: khớp theo mảnh (1 mảnh lệch do OCR/ngắt dòng) — đối chiếu ảnh trang
- Ghi chú: Trích bỏ qua đầu trang/số trang chen giữa ("G 2 … 34 TREATIES [1604"). "content" = consent (OCR). Bản OCR thế kỷ 18 có lỗi chữ s dài ("refide" = reside, "10" = to, "Majefty", "agr<ee"); nguyên văn chuẩn theo bản chép hiện đại của Gibraltar Heritage Trust (V-A1-23): "that no leave shall be given under any pretence whatsoever, either to Jews or Moors, to reside or have their dwellings in the said town of Gibraltar". Hai bản thế kỷ 18 (Jenkinson 1785, Chalmers 1790) và bản GHT khớp nội dung. Câu về tự do tôn giáo: "Her Majesty the Queen of Great Britain does further promise, that the free exercise of their religion shall be indulged to the Roman Catholic inhabitants of the aforesaid town." (Jenkinson, chuẩn hoá ſ, "thei" → OCR cụt chữ "their"). [Trích đã chuẩn hoá: gộp khoảng trắng/ngắt dòng OCR, nối từ bị gạch nối cuối dòng, ſ→s; không đổi chữ nào khác.]

**S025** · XÁC MINH · phía: trung-lap · nhạy cảm: CAO — TBN (Elcano 2013) lập luận quyền "redimir" đã phát sinh; Anh bác bỏ. Không kết luận thay khán giả. · as of: văn bản 13/7/1713; đọc 2026-10-17 · (gói: V-A1-22)
- Claim (EN): And if Britain ever chose to give up Gibraltar, Article X said “the preference of having the same shall always be given to the crown of Spain before any others.”
- Trích nguyên văn (en): > to grant, sell, or by any means to alienate therefrom the propriety of the faid town of Gibraltar, it is hereby agreed, and coneluded, that the preference of having the same, shall always be given to the crown of Spain before any others.
- Nguồn: Jenkinson (ed.), Collection of Treaties, vol. II (1785) — Treaty of Utrecht 1713, Art. X, câu cuối [so-cap] · Art. X, câu cuối · https://archive.org/download/bim_eighteenth-century_a-collection-of-all-the-_1785_2/bim_eighteenth-century_a-collection-of-all-the-_1785_2_djvu.txt · SHA-256 `121bd2712b4f45db…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: OCR trong cùng đoạn có "faid" (= said), "coneluded" (= concluded) ở phần ngay trước; phần trích ở đây sạch. Chalmers 1790 cùng câu: "the preference of having the same shall always be given to the crown of Spain before any others." Bản GHT viết sai thành "the preference of having the sale" — KHÔNG dùng bản GHT cho câu này. Bản TBN: "se dará a la Corona de España la primera acción antes que a otros para redimirla" (V-A1-24). [Trích đã chuẩn hoá: gộp khoảng trắng/ngắt dòng OCR, nối từ bị gạch nối cuối dòng, ſ→s; không đổi chữ nào khác.]

**S026** · XÁC MINH · phía: Anh · nhạy cảm: CAO · as of: đọc 2026-10-17 · (gói: V-A1-23)
- Claim (EN): Full English text of Article X (modern transcription by the Gibraltar Heritage Trust; checked against the 1785 and 1790 printed treaty collections).
- Trích nguyên văn (en): > The Catholic King does hereby, for himself, his heirs and successors, yield to the Crown of Great Britain the full and entire propriety of the town and castle of Gibraltar, together with the port, fortifications, and forts thereunto belonging; and he gives up the said propriety to be held and enjoyed absolutely with all manner of right for ever, without any exception or impediment whatsoever. But that abuses and frauds may be avoided by importing any kind of goods, the Catholic King wills, and takes it to be understood, that the above-named propriety be yielded to Great Britain without any territorial jurisdiction and without any open communication by land with the country round about. Yet whereas the communication by sea with the coast of Spain may not at all times be safe or open, and thereby it may happen that the garrison and other inhabitants of Gibraltar may be brought to great straits; and as it is the intention of the Catholic King, only that fraudulent importations of goods should, as is above said, be hindered by an inland communications. it is therefore provided that in such cases it may be lawful to purchase, for ready money, in the neighbouring territories of Spain, provisions and other things necessary for the use of the garrison, the inhabitants, and the ships which lie in the harbour. But if any goods be found imported by Gibraltar, either by way of barter for purchasing provisions, or under any other pretence, the same shall be confiscated, and complaint being made thereof, those persons who have acted contrary to the faith of this treaty, shall be severely punished. And Her Britannic Majesty, at the request of the Catholic King, does consent and agree, that no leave shall be given under any pretence whatsoever, either to Jews or Moors, to reside or have their dwellings in the said town of Gibraltar; and that no refuge or shelter shall be allowed to any Moorish ships of war in the harbour of the said town, whereby the communication between Spain and Ceuta may be obstructed, or the coasts of Spain be infested by the excursions of the Moors. But whereas treaties of friendship and a liberty and intercourse of commerce are between the British and certain territories situated on the coast of Africa, it is always to be understood, that the British subjects cannot refuse the Moors and their ships entry into the port of Gibraltar purely upon the account of merchandising. Her Majesty the Queen of Great Britain does further promise, that the free exercise of their religion shall be indulged to the Roman Catholic inhabitants of the aforesaid town. And in case it shall hereafter seem meet to the Crown of Great Britain to grant, sell or by any means to alienate there from the propriety of the said town of Gibraltar, it is hereby agreed and concluded that the preference of having the sale shall always be given to the Crown of Spain before any others.
- Nguồn: Gibraltar Heritage Trust, The Great Siege — Schools resource, "Further resources": "Text from Article X of the Treaty of Utrecht, 13th July 1713" [bao-tang] · Further resources → Chapter 1 · https://schools.gibraltarheritagetrust.org.gi/siege/further.html · SHA-256 `ccdd7817266fecab…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: TOÀN VĂN Điều X (bản Anh). Khác biệt so với bản in 1785 (Jenkinson) / 1790 (Chalmers): "any kind of goods" (gốc: "any kinds"); "inland communications." (gốc: "inland communication,"); "situated on the coast of Africa" (gốc: "situate"); "alienate there from" (gốc: "therefrom"); "the preference of having the sale" (gốc: "the same") — LỖI NGHĨA; "grant, sell or by any means" (gốc: "grant, sell, or"). Khi trích lên màn hình, dùng chữ của bản 1785 (V-A1-19..22). Trang GHT là tài liệu giáo dục (có lỗi khác, xem V-A1-14).

**S027** · XÁC MINH · phía: TBN · nhạy cảm: CAO — Elcano là viện nghiên cứu gần chính phủ TBN; phần phân tích của tác giả kết luận TBN "ha recuperado ya sus derechos" — quan điểm một phía. · as of: 31/05/2013; đọc 2026-10-17 · (gói: V-A1-24)
- Claim (EN): The authentic text of Article X is in Latin; Spain uses an accepted Spanish translation stating the property is ceded “sin jurisdicción alguna territorial y sin comunicación alguna abierta con el país circunvecino por parte de tierra”.
- Trích nguyên văn (es): > El texto auténtico del artículo X de dicho tratado, que sigue en vigor para las dos partes, está redactado en latín, por lo que se reproduce la traducción española generalmente aceptada, contenida en la página web del MAEC,1 de los extractos relevantes: “Artículo X. El Rey Católico, por sí y por sus herederos y sucesores, cede por este Tratado a la Corona de la Gran Bretaña la plena y entera propiedad de la ciudad y castillo de Gibraltar, juntamente con su puerto, defensas y fortalezas que le pertenecen, dando la dicha propiedad absolutamente para que la tenga y goce con entero derecho y para siempre, sin excepción ni impedimento alguno. Pero, para evitar cualquiera abusos y fraudes en la introducción de las mercaderías, quiere el Rey Católico, y supone que así se ha de entender, que la dicha propiedad se ceda a la Gran Bretaña sin jurisdicción alguna territorial y sin comunicación alguna abierta con el país circunvecino por parte de tierra. … “Si en algún tiempo a la Corona de la Gran Bretaña le pareciere conveniente dar, vender, enajenar de cualquier modo la propiedad de la dicha Ciudad de Gibraltar, se ha convenido y concordado por este Tratado que se dará a la Corona de España la primera acción antes que a otros para redimirla.”
- Nguồn: Martín Ortega Carcelén, "Gibraltar y el Tratado de Utrecht", Real Instituto Elcano, ARI 19/2013 (31/5/2013) [hoc-thuat] · Tr. 1–2, phần Análisis · https://media.realinstitutoelcano.org/wp-content/uploads/2021/11/ari19-2013-ortega-gibraltar-tratado-de-utrecht.pdf · SHA-256 `528385f5ce88cde1…`
- Kiểm độc lập: khớp theo mảnh (1 mảnh lệch do OCR/ngắt dòng) — đối chiếu ảnh trang
- Ghi chú: Bản TBN "generalmente aceptada, contenida en la página web del MAEC" (trích đoạn, có dấu "…"). Toàn văn TBN thế kỷ 19: Alejandro del Cantillo, Tratados, convenios y declaraciones de paz y de comercio… (Madrid, 1843), Art. 10 — đã tải (sha 957f850035749073881e4eac44a98b02112bc548c6741f307e1b51691bd60d25) và khớp nội dung, nhưng OCR nhiễu ("Gran Bretafia", "juth'os ni moros"), nên ưu tiên bản Elcano cho trích dẫn. Cantillo, phần Do Thái/Moro: "que no se permita por motivo alguno que [judíos] ni moros habiten ni tengan domicilio en la dicha ciudad de Gibraltar" (chữ "judíos" bị OCR thành "juth'os" — cần soát scan trang). Cụm "para redimirla" ⇔ bản Anh "the preference of having the same" — hai bản dịch khác sắc thái (Latinh: "ut prima ante alios ejus redimendae optio Coronae Hispanicae semper deferatur", theo Elcano). [Trích đã chuẩn hoá: gộp khoảng trắng/ngắt dòng OCR, nối từ bị gạch nối cuối dòng, ſ→s; không đổi chữ nào khác.]

**S028** · XÁC MINH · phía: Anh · nhạy cảm: THẤP · as of: 05/07/2013; đọc 2026-10-17 · (gói: V-A1-25)
- Claim (EN): The Government of Gibraltar itself marks 13 July 1713 as the date Article X was signed.
- Trích nguyên văn (es): > El Artículo X del Tratado de Utrecht, que es de suma importancia para Gibraltar y sus habitantes, se firmó el 13 de julio de 1713.
- Nguồn: HM Government of Gibraltar (Ministry of Culture), InfoGibraltar press release 500/2013, 5/7/2013 [chinh-thuc] · Tr. 1 · https://infogibraltar.com/wp-content/uploads/2020/06/130705%20500%20Acto%20conmemorativo%20del%20Tratado%20de%20Utrecht%20-%20s%C3%A1bado%2013%20de%20julio.pdf · SHA-256 `c1aac1c21a5a9587…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Bản TBN của chính quyền Gibraltar ghi "ciudad y castillos" (số nhiều — lỗi chép so với "ciudad y castillo" trong MAEC/Elcano/Cantillo). Dùng nguồn này chỉ để xác nhận ngày 13/7/1713 từ phía Gibraltar.

**S029** · XÁC MINH · phía: TBN · nhạy cảm: CAO · as of: đọc 2026-10-17 · (gói: V-A1-26)
- Claim (EN): Spain’s Foreign Ministry likewise dates the treaty to 13 July 1713 and quotes Article X as ceding “the town and castle of Gibraltar, together with its port, defences and fortresses”.
- Trích nguyên văn (es): > El Tratado de Utrecht. Firmado el 13 de julio de 1713, en su artículo X cede a la Corona Británica “la plena y entera propiedad de la ciudad y el castillo de Gibraltar, conjuntamente con su puerto, defensas y fortalezas que le pertenecen.
- Nguồn: Ministerio de Asuntos Exteriores, UE y Cooperación (España), trang "Gibraltar" [chinh-thuc] · Mục "Los principales documentos…" · https://exteriores.gob.es/es/PoliticaExterior/Paginas/Gibraltar.aspx · SHA-256 `6d9ac371d4f7dd3e…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Hai phía thống nhất ngày ký 13/7/1713.

### Eo đất, chiến tuyến, La Línea, hàng rào

**S030** · XÁC MINH · phía: TBN · nhạy cảm: CAO — luôn đặt cạnh quan điểm Anh (V-A1-28). · as of: đọc 2026-10-17 · (gói: V-A1-27)
- Claim (EN): Spain’s position is that the isthmus was never ceded and that it does not recognise the fence as a border.
- Trích nguyên văn (es): > El istmo, al igual que las aguas adyacentes o el espacio aéreo suprayacente, no fue cedido por España y ha permanecido siempre bajo soberanía española. La ocupación de facto continuada por los británicos no cumple los requisitos del Derecho Internacional para la adquisición de soberanía. Esa es la razón por la que España siempre ha subrayado que la ocupación del istmo es ilegal y contraria al Derecho Internacional y, por tanto, ha reclamado siempre su devolución sin condiciones. España no reconoce la ocupación del istmo ni la verja como frontera.
- Nguồn: MAEC (España), trang "Gibraltar", mục "La historia de Gibraltar" [chinh-thuc] · Mục "La historia de Gibraltar" · https://exteriores.gob.es/es/PoliticaExterior/Paginas/Gibraltar.aspx · SHA-256 `6d9ac371d4f7dd3e…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Đã có trong repo (tiền kỳ T3); trích lại ngắn theo yêu cầu. Lưu ý thời điểm: trang vẫn ghi lập trường này sau thoả thuận chính trị 11/6/2025.

**S031** · XÁC MINH · phía: Anh · nhạy cảm: CAO · as of: 14/10/2015; đọc 2026-10-17 · (gói: V-A1-28)
- Claim (EN): The British government’s position, as stated in Parliament by Europe Minister David Lidington in 2015, is that Gibraltar includes the isthmus as well as the Rock.
- Trích nguyên văn (en): > I want there to be no misunderstanding of our position: Gibraltarians will be British for as long as they wish to remain so. We regard Gibraltar as including the isthmus and British Gibraltar territorial waters, as well as the Rock itself.
- Nguồn: Hansard (HC), Westminster Hall debate "Gibraltar and Spain", 14/10/2015, col. 129WH — Sir David Lidington (Minister for Europe) [chinh-thuc] · Hansard API, ContributionExtId 15101444000092, col. 129WH · https://hansard-api.parliament.uk/search/contributions/Spoken.json?queryParameters.searchTerm=isthmus%20Gibraltar%20sovereignty&queryParameters.take=15 · SHA-256 `b17cacef25fcfe5c…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Lập trường Anh cụ thể về cơ sở pháp lý (chiếm hữu liên tục lâu dài/"prescription") chỉ thấy trong Wikipedia ("The United Kingdom relies on de facto arguments of possession by prescription…", dẫn tài liệu FCO cũ) — CHƯA tải được nguồn chính thức (publications.parliament.uk trả 403, web.archive.org bị chặn). Năm 1966 một nghị sĩ nói tại Hạ viện chủ quyền với eo đất "has remained unchallenged since 1838" (Hansard 10/11/1966) — chỉ là phát biểu nghị sĩ.

**S032** · XÁC MINH · phía: TBN · nhạy cảm: TRUNG · as of: 10/2018; đọc 2026-10-17 · (gói: V-A1-29)
- Claim (EN): In 1730 Philip V ordered a permanent fortified line built across the isthmus, outside cannon range of the Rock, to cut Gibraltar off by land.
- Trích nguyên văn (es): > Felipe V da respuesta el 8 de octubre de 1730 con la gran noticia de que “no es su real intención que se construya la Línea provisional que propuso el ingeniero D. Antonio Montaigú con una simple estacada y barracas para su custodia, pero que ésta se construya toda de mampostería de cal y canto…”. Su majestad manifiesta que el objetivo de esta construcción con carácter permanente es la de bloquear definitivamente la correspondencia y paso a la plaza por tierra. … Por orden del regente, el 2 de noviembre de 1730, se le encarga al ingeniero D. Isidro Próspero Verboom la construcción de una Línea fortificada de mar a mar, en la lengua de tierra delante de Gibraltar y según el proyecto elaborado por el ingeniero general D. Jorge Próspero Verboom, padre de D. Isidro (Patiño, 1730).
- Nguồn: Baltasar Gómez Nadal, "Origen de la línea de contravalación frente a Gibraltar", Almoraima 48 (2018), pp. 259–272 (dựa trên thư Patiño 1730, AGS) [hoc-thuat] · Tr. 268–270 · https://institutoecg.es/almoraima/index.php/revista/article/download/1339/1297/2522 · SHA-256 `471599817786944c…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Thiết kế: Kỹ sư trưởng Jorge Próspero de Verboom (cha), thi công: Isidro Próspero Verboom (con), khởi công cuối 1730; hào "de mar a mar" xong ngày 7/12/1730; công trình hoàn tất 1735 (cùng bài: "La construcción de la obra concluyó en 1735… al fallecer [Isidro] en 1733"). Như vậy "built 1730–31 under the Marquis of Verboom" trong đề bài là chưa chính xác: khởi công 1730, xong 1735; người thi công chính là Isidro. Lệnh vua yêu cầu xây "fuera del tiro del cañón de la Plaza" — đây là gốc của khoảng trống giữa hai tuyến (sau gọi là "neutral ground"). Sau cuộc vây 1727, Montero (1860, tr. 317–318) ghi Conde de Montemar đã cho dựng một tuyến "de uno al otro mar" và lập luận theo Utrecht "la plaza no tenia mas término que sus murallas".

**S033** · XÁC MINH · phía: TBN · nhạy cảm: THẤP · as of: 2007; đọc 2026-10-17 · (gói: V-A1-30)
- Claim (EN): The town of La Línea grew up behind those Spanish lines; its separation from San Roque was approved by Spain’s Council of State on 17 January 1870, and the town was founded that July.
- Trích nguyên văn (es): > el hecho puntual que sitúa en julio de 1870 la fundación de la ciudad de La Línea de la Concepción … el expediente de segregación se tramitó, siendo aprobado finalmente por el Consejo de Estado el 17 de enero de 1870. … La pérdida de Gibraltar determinó la aparición de aquella vieja Línea que, marcada primero por improvisados gaviones y más tarde por los perfiles perfectos de unos baluartes de piedra, había reivindicado la reintegración a España de la perdida plaza de Gibraltar a lo largo del siglo XVIII.
- Nguồn: Alfonso Escuadra Sánchez, "El origen de La Línea en relación con los sucesos de 1704", Almoraima 34 (2007) [hoc-thuat] · Mục 1 (Introducción) và cuối mục 7 – 8 (Conclusión) · https://institutoecg.es/almoraima/index.php/revista/article/download/909/874/1692 · SHA-256 `fba6f8cf68946409…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Tên gọi: "La Línea" bắt nguồn từ Línea de Contravalación/"Línea de Gibraltar" (xác nhận thêm: Moreno Martín, Almoraima 51: "Línea de Fuego —y, más oficialmente, como Línea de Contravalación o de Gibraltar"). Phần "de la Concepción" (Đức Mẹ Vô Nhiễm — thánh bổn mạng) CHƯA tìm được nguồn tải về giải thích nguyên văn → xem "khong_tim_duoc". Ngày cụ thể tháng 7/1870 (thường nêu 20/7) chưa xác minh.

**S034** · MÂU THUẪN · phía: TBN · nhạy cảm: TRUNG — phía TBN thường nhấn mạnh việc phá huỷ "con nuestra autorización" nhưng rồi Anh không cho xây lại. · as of: 12/2022; đọc 2026-10-17 · (gói: V-A1-31)
- Claim (EN): In 1810, as Napoleon’s armies advanced towards the Strait, the British — with Spanish consent — blew up the Spanish forts on the isthmus.
- Trích nguyên văn (es): > invasión de Napoleón provocó la guerra de la Independencia (1808-1814) y la alianza de España con Inglaterra. En 1810, el avance hacia el Estrecho del ejército francés condujo a que, con autorización española, fueran destruidos por los ingleses todas las obras militares que pusieran ser útiles al ejército invasor.
- Nguồn: Carlos Gómez de Avellaneda Sabio, Un par de horas en… "la Línea de Contravalación", Guías del patrimonio del Campo de Gibraltar vol. 6 (IECG, 2022), tr. 60–61 [hoc-thuat] · Mục "h. Vida y muerte del sistema fortificado ante Gibraltar", tr. 60–61 · https://institutoecg.es/wp-content/uploads/2025/08/06_linea-contravalacion.pdf · SHA-256 `cdc8a2e2165d4ece…`
- Kiểm độc lập: khớp theo mảnh (1 mảnh lệch do OCR/ngắt dòng) — đối chiếu ảnh trang
- Ghi chú: Bản PDF dàn 2 cột, câu bị ngắt bởi số trang ("60 … la linea_01.indd 60") — đã ghép hai mảnh, chữ "pusieran" là lỗi in của sách (nghĩa: "pudieran"). Năm: hầu hết nguồn ghi 1810 (García Sanz 2022: "los británicos volaron las fortalezas de Santa Bárbara y San Felipe"; sau chiến tranh Anh tuyên bố mọi việc tái chiếm tuyến sẽ bị coi "como un acto de abierta hostilidad", dẫn Sánchez Mantero 1989). Montero 1860 (tr. 384–385) ghi "Por este tiempo (1811)" và viết "Nosotros consentimos y ayudamos á la destrucción" — lệch năm. Dùng 1810.

**S035** · XÁC MINH · phía: TBN · nhạy cảm: CAO — tác giả dùng chữ "usurpaciones" và ghi rõ "si empleamos la terminología de la literatura del contencioso"; trong lời dẫn dùng "advanced", không dùng "usurped". · as of: đọc 2026-10-17 · (gói: V-A1-32)
- Claim (EN): The Treaty of Utrecht gave Britain no sovereignty over the sandy isthmus; through the nineteenth century Britain gradually advanced its line into the neutral zone — for example with epidemic barracks in 1854 that were never fully removed.
- Trích nguyên văn (es): > Uno de los asuntos más polémicos de la consolidación del dominio británico sobre la plaza fue el progresivo avance de la frontera sobre la zona neutral. De hecho, el Tratado de Utrecht no reconocía ningún tipo de soberanía a los británicos sobre el istmo arenoso que tenía tal consideración. … Pero la más reveladora de las usurpaciones, si empleamos la terminología de la literatura del contencioso, se produjo durante la epidemia de cólera de 1854. Aquella fue la más grave en más de 20 años, coincidiendo con los movimientos de tropas por la guerra en Crimea (1854-1856). Los ingleses levantaron en la zona neutral una serie de barracas que servían como lazaretos. Una vez finalizado el brote, las barracas no fueron del todo desmanteladas.
- Nguồn: García Sanz 2022, cap. 3 "La frontera móvil" [hoc-thuat] · Chương 3, mục 2 "La frontera móvil" · https://archive.org/download/garcia-sanz-c.-historia-de-gibraltar-madrid-2022./Garc%C3%ADa%20Sanz%2C%20C.-Historia%20de%20Gibraltar%2C%20Madrid%2C%202022.%20180%20pp._djvu.txt · SHA-256 `2357d695b5be8c3f…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Ý về dịch sốt vàng 1815: Wikipedia (cấp 3) viết "The British informed Spain of its intention to build barracks on the isthmus's neutral ground in 1815, which Spain agreed to for the duration of… a yellow fever epidemic" — CHƯA tìm được nguồn sơ cấp/học thuật tải về cho mốc 1815; García Sanz nêu mốc 1845 (khiếu nại của đại sứ TBN) và 1854 (dịch tả, lán cách ly). Montero 1860 (tr. 405) viết vùng đất trồng vườn sát pháo đài được gọi "campo neutral" và "El Gobierno español toleró esta infracción del tratado". Phía Anh (Hansard 2015) coi eo đất thuộc Gibraltar. [Trích đã chuẩn hoá: gộp khoảng trắng/ngắt dòng OCR, nối từ bị gạch nối cuối dòng, ſ→s; không đổi chữ nào khác.]

**S036** · XÁC MINH · phía: TBN · nhạy cảm: CAO — phía TBN coi hàng rào nằm trên đất không nhượng; phía Anh coi là ranh giới thực tế. · as of: đọc 2026-10-17 · (gói: V-A1-33)
- Claim (EN): In August 1908 Britain informed Spain, “as an act of courtesy”, that it would build a fence on the edge of the neutral ground; the fence went up in 1909.
- Trích nguyên văn (es): > verja levantada por los británicos en 1909. … En agosto de 1908 se produjo el anuncio inglés al Gobierno español —“como acto de cortesía”— de la intención de levantar una verja en el “borde neutral del territorio británico” para reducir el número de efectivos de vigilancia
- Nguồn: García Sanz 2022, tr. ~13 (lời mở) và chú thích 43 (dẫn Ballesta Gómez, La verja de Gibraltar, 2005, tr. 224–225) [hoc-thuat] · Chương 1 + chú thích 43 · https://archive.org/download/garcia-sanz-c.-historia-de-gibraltar-madrid-2022./Garc%C3%ADa%20Sanz%2C%20C.-Historia%20de%20Gibraltar%2C%20Madrid%2C%202022.%20180%20pp._djvu.txt · SHA-256 `2357d695b5be8c3f…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Lý do chính thức nêu với TBN: giảm số lính canh. Lý do "chống buôn lậu" thường được nhắc nhưng CHƯA có nguồn tải về đáng tin (bài Gibraltar Chronicle "Goodbye Frontier" nói "in 1908 the British erected an unclimbable frontier fence… to stop smuggling" nhưng là bài bình luận/hư cấu hài hước, có số liệu sai — KHÔNG dùng). Năm dựng: 1909 (García Sanz, 2 chỗ); có nguồn báo chí nói 1910 — chưa kiểm. Chưa tìm được nguồn phía Anh (Hansard 1908–1910, Colonial Office) cho việc dựng hàng rào. [Trích đã chuẩn hoá: gộp khoảng trắng/ngắt dòng OCR, nối từ bị gạch nối cuối dòng, ſ→s; không đổi chữ nào khác.]

### Great Siege — bối cảnh, hiệp ước

**S037** · XÁC MINH · phía: Anh · nhạy cảm: THẤP · as of: 2026-10-17 · (gói: V-A2-08)
- Claim (EN): The preliminaries (20 Jan 1783) left Gibraltar in British possession.
- Trích nguyên văn (en): > The duke, on the 6th, informed the governor that the preliminaries had been signed the 20th of January at Paris, and that Gibraltar was to remain in the possession of Great Britain.
- Nguồn: John Drinkwater, A History of the Siege of Gibraltar 1779-1783, new ed., London: John Murray, 1905 (text of 1785 original), archive.org OCR djvu.txt [so-cap] · Ch. VIII, p. 354 (ed. 1905) · https://archive.org/download/historysiegegibr00drin/historysiegegibr00drin_djvu.txt · SHA-256 `9a0c3c3e45f39e2f…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Không tải được văn bản Hiệp ước Versailles Anh–TBN (3/9/1783); hiệp ước không cần nhắc Gibraltar vì giữ nguyên trạng. Dùng câu này + V-A2-09 (Montero) thay cho trích hiệp ước.

**S038** · XÁC MINH · phía: TBN · nhạy cảm: THẤP · as of: 2026-10-17 · (gói: V-A2-09)
- Claim (EN): Montero: the definitive treaty signed at Versailles (3 Sept 1783) gave Spain Minorca and the two Floridas, but Spain was left without Gibraltar.
- Trích nguyên văn (es): > Por último se firmó en Versalles (3 de setiembre 1788) el tratado definitivo de paz, por el cual adquiría España la isla de Menorca, las dos Floridas y las costas de Honduras y Campeche.
- Nguồn: Francisco María Montero, Historia de Gibraltar y de su campo, Cádiz 1860, archive.org OCR djvu.txt [hoc-thuat] · p. 372 · https://archive.org/download/bub_gb_4_AqUai2tkIC/bub_gb_4_AqUai2tkIC_djvu.txt · SHA-256 `d99126f25d1c838e…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: '1788' là lỗi OCR/in của 1783 (ngữ cảnh rõ). Câu tiếp theo trong nguồn: '…pero se quedó sin Gibraltar, que valia ella sola mas que estas nuevas adquisiciones'. Hiệp ước Aranjuez (12/4/1779) CHƯA XÁC MINH từ nguồn tải; Montero chỉ nói Carlos III tuyên chiến và liên minh với Pháp.

**S039** · XÁC MINH · phía: TBN · nhạy cảm: TRUNG — động cơ chiến tranh; nói 'theo sử gia TBN Montero (1860)' · as of: 2026-10-17 · (gói: V-A2-10)
- Claim (EN): Montero: Charles III declared war on Britain and joined France; the war was popular in Spain and the exiled 'city of Gibraltar' at San Roque saw a chance to return home.
- Trích nguyên văn (es): > Carlos III declaró la guerra á Inglaterra y se unió á Francia, quejoso de va- rios agravios inferidos por los ingleses en los dominios de América.
- Nguồn: Francisco María Montero, Historia de Gibraltar y de su campo, Cádiz 1860, archive.org OCR djvu.txt [hoc-thuat] · pp. 337-338 · https://archive.org/download/bub_gb_4_AqUai2tkIC/bub_gb_4_AqUai2tkIC_djvu.txt · SHA-256 `d99126f25d1c838e…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Bối cảnh: TBN vào cuộc chiến tranh Mỹ để lấy lại Gibraltar. Drinkwater (p.50) cũng viết 'the siege of that garrison was her first and immediate object'.

### Great Siege — ngày bắt đầu/kết thúc

**S040** · XÁC MINH · phía: Anh · nhạy cảm: THẤP · as of: 2026-10-17 · (gói: V-A2-01)
- Claim (EN): On 21 June 1779 communication between Spain and Gibraltar was closed by order from Madrid; two days earlier Governor Eliott had visited General Mendoza at San Roque.
- Trích nguyên văn (en): > On the 21st of June, 1779, the communication between Spain and Gibraltar was closed, by an order from Madrid. Two days previous to this event General Eliott, the governor, accompanied by many field-officers of the garrison, paid a visit to General Mendoza
- Nguồn: John Drinkwater, A History of the Siege of Gibraltar 1779-1783, new ed., London: John Murray, 1905 (text of 1785 original), archive.org OCR djvu.txt [so-cap] · Ch. III, p. 50 (ed. 1905) · https://archive.org/download/historysiegegibr00drin/historysiegegibr00drin_djvu.txt · SHA-256 `9a0c3c3e45f39e2f…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Mốc 'bắt đầu' an toàn nhất: 21/6/1779 = đóng biên giới (phía Anh). Wikipedia nêu 24/6/1779 hoặc 11/7/1779 làm ngày bắt đầu — không có trong nguồn sơ cấp đã tải; nếu dùng phải ghi 'theo một số tài liệu'. Tuyên chiến của TBN (16/6/1779) CHƯA XÁC MINH trong nguồn đã tải.

**S041** · XÁC MINH · phía: Anh · nhạy cảm: THẤP · as of: 2026-10-17 · (gói: V-A2-02)
- Claim (EN): On 6 July 1779 the garrison learned via Lisbon and Faro that hostilities between Britain and Spain had begun.
- Trích nguyên văn (en): > The following day, the 6th of July, a packet was received from England, by way of Lisbon and Faro, informing the governor that hostilities had commenced between Great Britain and Spain.
- Nguồn: John Drinkwater, A History of the Siege of Gibraltar 1779-1783, new ed., London: John Murray, 1905 (text of 1785 original), archive.org OCR djvu.txt [so-cap] · Ch. III, p. 57 (ed. 1905) · https://archive.org/download/historysiegegibr00drin/historysiegegibr00drin_djvu.txt · SHA-256 `9a0c3c3e45f39e2f…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Tin chiến tranh đến Gibraltar 6/7/1779 (chậm hơn tuyên chiến).

**S042** · XÁC MINH · phía: Anh · nhạy cảm: THẤP · as of: 2026-10-17 · (gói: V-A2-03)
- Claim (EN): On 16 July 1779 a Spanish squadron blockaded the port and the garrison became closely blockaded by sea.
- Trích nguyên văn (en): > The i6th the enemy blocked up the port with a squadron of men-of-war, consisting of 1779] LOGIE'S ESCAPE 59 2 seventy-fours, 2 frigates, 5 xebeques, and a number of galleys, half-galleys, and armed settees : they anchored in the bay, off Algeziras, and being judiciously arranged, and keeping a vigilant lookout, the garrison became closely blockaded.
- Nguồn: John Drinkwater, A History of the Siege of Gibraltar 1779-1783, new ed., London: John Murray, 1905 (text of 1785 original), archive.org OCR djvu.txt [so-cap] · Ch. III, pp. 58-59 (ed. 1905) · https://archive.org/download/historysiegegibr00drin/historysiegegibr00drin_djvu.txt · SHA-256 `9a0c3c3e45f39e2f…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Trích nguyên OCR: 'i6th' = 16th; '1779] LOGIE'S ESCAPE 59' là tiêu đề trang chen vào. Phong toả biển chặt: 16/7/1779 (tháng suy từ ngữ cảnh ngay trước: 6th of July).

**S043** · XÁC MINH · phía: Anh · nhạy cảm: THẤP · as of: 2026-10-17 · (gói: V-A2-04)
- Claim (EN): The garrison first opened fire on the Spanish works on Sunday 12 September 1779 (start of artillery exchanges; ammunition tallies begin that day).
- Trích nguyên văn (en): > for on the succeeding morning, being Sunday the 12th of September, the artillery officers were ordered to the batteries on the heights ; and the Devil's Tower guard being withdrawn, the governor opened on the enemy from Green's Lodge
- Nguồn: John Drinkwater, A History of the Siege of Gibraltar 1779-1783, new ed., London: John Murray, 1905 (text of 1785 original), archive.org OCR djvu.txt [so-cap] · Ch. III, p. 64 (ed. 1905) · https://archive.org/download/historysiegegibr00drin/historysiegegibr00drin_djvu.txt · SHA-256 `9a0c3c3e45f39e2f…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Ba mốc 'bắt đầu' khác nhau, nói rõ: 21/6 đóng biên giới; 16/7 phong toả biển; 12/9/1779 phát pháo đầu tiên của đồn. Ancell & bảng đạn dược Drinkwater đều tính từ 12/9/1779.

**S044** · XÁC MINH · phía: TBN · nhạy cảm: THẤP · as of: 2026-10-17 · (gói: V-A2-05)
- Claim (EN): Spanish historian Montero: the blockade began in June 1779 under commander-in-chief Martín Álvarez de Sotomayor.
- Trích nguyên văn (es): > Pronto (junio 1779) comenzó el bloqueo de esta. Nombróse general en gefe del ejército bloqueador á Don Martin Álvarez de Sotomayor, general experimen- tado en las guerras de Italia.
- Nguồn: Francisco María Montero, Historia de Gibraltar y de su campo, Cádiz 1860, archive.org OCR djvu.txt [hoc-thuat] · Cap. (sitio 1779-83), p. 338 · https://archive.org/download/bub_gb_4_AqUai2tkIC/bub_gb_4_AqUai2tkIC_djvu.txt · SHA-256 `d99126f25d1c838e…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Phía TBN khớp với phía Anh về tháng 6/1779. Đồng thời xác nhận chỉ huy đầu tiên (claim 'chi-huy').

**S045** · XÁC MINH · phía: Anh · nhạy cảm: THẤP · as of: 2026-10-17 · (gói: V-A2-06)
- Claim (EN): On 2 February 1783 letters from the Duc de Crillon told Eliott that preliminaries of a general peace had been signed; the Spaniards called out 'We are all friends!'
- Trích nguyên văn (en): > Thus affairs were pro- ceeding, when, on the 2nd, letters from the Due de Crillon informed the governor that the preliminaries of a general peace had been signed between Great Britain, France, and Spain.
- Nguồn: John Drinkwater, A History of the Siege of Gibraltar 1779-1783, new ed., London: John Murray, 1905 (text of 1785 original), archive.org OCR djvu.txt [so-cap] · Ch. VIII, p. 353-354 (ed. 1905) · https://archive.org/download/historysiegegibr00drin/historysiegegibr00drin_djvu.txt · SHA-256 `9a0c3c3e45f39e2f…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: 'Due' = OCR của 'Duc'. 2/2/1783 = ngừng bắn trên thực tế. Bảng đạn dược của Drinkwater kết thúc 2–3/2/1783.

**S046** · XÁC MINH · phía: Anh · nhạy cảm: THẤP · as of: 2026-10-17 · (gói: V-A2-07)
- Claim (EN): On 5 February 1783 Crillon announced the sea blockade discontinued, the port reopened, and the last shot of the siege was fired; on 6 February he said preliminaries were signed 20 January at Paris and Gibraltar would remain British.
- Trích nguyên văn (en): > The duke, on the 5th, informed the governor that the blockade by sea was discontinued ; in consequence of which, a placard was published in the garrison, signifying that the port of Gibraltar was again open. About noon, an elevated gun was wantonly fired over their works, which w^as the last shot fired in this siege.
- Nguồn: John Drinkwater, A History of the Siege of Gibraltar 1779-1783, new ed., London: John Murray, 1905 (text of 1785 original), archive.org OCR djvu.txt [so-cap] · Ch. VIII, p. 354 (ed. 1905) · https://archive.org/download/historysiegegibr00drin/historysiegegibr00drin_djvu.txt · SHA-256 `9a0c3c3e45f39e2f…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Phát súng cuối: trưa 5/2/1783 (giờ: 'About noon'). Câu tiếp: 'The duke, on the 6th, informed the governor that the preliminaries had been signed the 20th of January at Paris, and that Gibraltar was to remain in the possession of Great Britain.' MÂU THUẪN nhẹ: Montero (p.371) ghi ngày ký sơ bộ '30 de enero 1783' và lệnh ngừng chiến '3 de febrero'; dùng 20/1/1783 (Drinkwater, khớp ngày ký sơ bộ Versailles thường được dẫn).

**S047** · XÁC MINH · phía: Anh · nhạy cảm: THẤP · as of: 2026-10-17 · (gói: V-A2-50)
- Claim (EN): The frigate Thetis arrived 10 March 1783 with official dispatches; Eliott and Crillon later met on the isthmus and embraced.
- Trích nguyên văn (en): > when the long-expected frigate arrived on the loth of March
- Nguồn: John Drinkwater, A History of the Siege of Gibraltar 1779-1783, new ed., London: John Murray, 1905 (text of 1785 original), archive.org OCR djvu.txt [so-cap] · Ch. VIII, p. 355-356 (ed. 1905) · https://archive.org/download/historysiegegibr00drin/historysiegegibr00drin_djvu.txt · SHA-256 `9a0c3c3e45f39e2f…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: 'loth'=10th. Kết thúc chính thức: tin chính thức đến 10/3/1783; lễ phong tước Eliott 23/4/1783 (p.~360). Hiệp ước chung kết 3/9/1783 (Montero).

### Great Siege — chỉ huy

**S048** · XÁC MINH · phía: Anh · nhạy cảm: THẤP · as of: 2026-10-17 · (gói: V-A2-11)
- Claim (EN): In October 1779 the Spanish army (16 battalions, 12 squadrons, ~14,000 men if complete) was commanded by Lt-Gen Don Martín Álvarez de Sotomayor.
- Trích nguyên văn (en): > In the beginning of October the enemy's army, according to our intelligence, consisted of 16 battalions of infantry and 12 squadrons of horse, which, if the regiments were complete, would amount to about 14,000 men. Lieutenant-General Don Martin Alvarez de Sota Mayor was commander-in-chief
- Nguồn: John Drinkwater, A History of the Siege of Gibraltar 1779-1783, new ed., London: John Murray, 1905 (text of 1785 original), archive.org OCR djvu.txt [so-cap] · Ch. III, p. 70-71 (ed. 1905) · https://archive.org/download/historysiegegibr00drin/historysiegegibr00drin_djvu.txt · SHA-256 `9a0c3c3e45f39e2f…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Drinkwater viết 'Sota Mayor'; chuẩn: Martín Álvarez de Sotomayor. Không tải được tiểu sử dbe.rah.es (tìm không ra URL).

**S049** · XÁC MINH · phía: Anh · nhạy cảm: THẤP · as of: 2026-10-17 · (gói: V-A2-12)
- Claim (EN): A deserter on 14 July 1782 reported that the Duc de Crillon had assumed command of the siege and General Álvarez had left the camp.
- Trích nguyên văn (en): > A deserter from the regiment of Bechart came in on the 14th : he acquainted us that the Due de Crillon 1782] EXPLODING A MINE 257 had assumed the command of the siege, and that General Don Alvarez had quitted the camp
- Nguồn: John Drinkwater, A History of the Siege of Gibraltar 1779-1783, new ed., London: John Murray, 1905 (text of 1785 original), archive.org OCR djvu.txt [so-cap] · Ch. VII, pp. 256-257 (ed. 1905) · https://archive.org/download/historysiegegibr00drin/historysiegegibr00drin_djvu.txt · SHA-256 `9a0c3c3e45f39e2f…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Montero (p.356): Crillon đến 'A mediados de junio' 1782 với 4.000 quân, cộng 4.000 Pháp của Falkenstein → quân vây 33.000. Ngày nhận chức: giữa tháng 6/1782 (TBN) / Anh biết tin 14/7/1782.

**S050** · XÁC MINH · phía: Anh · nhạy cảm: THẤP · as of: 2026-10-17 · (gói: V-A2-13)
- Claim (EN): d'Arçon, French engineer, was the designer ('projector') of the floating batteries; he was aboard Tailla Piedra and left about half an hour after midnight (13/14 Sept 1782).
- Trích nguyên văn (en): > M. d'Ar^on, the French engineer, and projector of the floating batteries, embarked on board the Tailla Piedra, and quitted the ship about half an hour after midnight, as he states in the Defence of his plan of attack, which was published at Cadiz the following year.
- Nguồn: John Drinkwater, A History of the Siege of Gibraltar 1779-1783, new ed., London: John Murray, 1905 (text of 1785 original), archive.org OCR djvu.txt [so-cap] · Ch. VII, footnote p. 306 (ed. 1905) · https://archive.org/download/historysiegegibr00drin/historysiegegibr00drin_djvu.txt · SHA-256 `9a0c3c3e45f39e2f…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: 'd'Ar^on' = OCR của d'Arçon. Montero (p.365) dẫn 'Memoire pour servir á l'histoire du siege de Gibraltar par l'auteur des batteries flottantes. Cadix 1783' — bản này KHÔNG tìm thấy trên archive.org; đã dùng 'Conseil de guerre privé' (1785) thay thế (V-A2-24/25).

### Great Siege — hậu cần (lương thực, thuốc súng, tiếp tế)

**S051** · XÁC MINH · phía: Anh · nhạy cảm: THẤP · as of: 2026-10-17 · (gói: V-A2-36)
- Claim (EN): Ammunition expended: garrison (12 Sep 1779 – 3 Feb 1783) 200,600 rounds + 4,728 shot from British gunboats = 205,328; enemy (12 Apr 1781 – 2 Feb 1783) 244,104 + 14,283 from Spanish gunboats = 258,387; garrison used nearly 8,000 barrels of powder.
- Trích nguyên văn (en): > Spanish gun-boats 14,283 shot and shells. 205,328 258,387 The garrison expendud very near 8,000 barrels of pon der
- Nguồn: John Drinkwater, A History of the Siege of Gibraltar 1779-1783, new ed., London: John Murray, 1905 (text of 1785 original), archive.org OCR djvu.txt [so-cap] · Appendix, p. 368 (ed. 1905) · https://archive.org/download/historysiegegibr00drin/historysiegegibr00drin_djvu.txt · SHA-256 `9a0c3c3e45f39e2f…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: OCR: 'expendud'=expended, 'pon der'=powder. Tổng 200.600 và 4.728 đọc từ bảng (OCR '2vl',(i00', '4,72S'); bản 1785 ghi 'Total 200,60[0] Rounds Britiſh Gun-boats 4228[4728]' và 'Total 244,104'. Số đạn địch chỉ tính từ 12/4/1781. Số pháo hư hỏng: bản 1905 '53', bản 1785 OCR '33' — CHƯA chắc.

**S052** · XÁC MINH · phía: Anh · nhạy cảm: TRUNG — nạn đói dân thường; có câu 'One woman actually died through want' · as of: 2026-10-17 · (gói: V-A2-37)
- Claim (EN): January 1780 famine: thistles, dandelion and wild leeks were the daily food of many; extreme prices (eggs 6d each, a small cabbage 1s 6d).
- Trích nguyên văn (en): > Thistles, dandelion, wild leeks, etc., were for some time the daily nourishment of numbers.
- Nguồn: John Drinkwater, A History of the Siege of Gibraltar 1779-1783, new ed., London: John Murray, 1905 (text of 1785 original), archive.org OCR djvu.txt [so-cap] · Ch. III, p. 86 (ed. 1905) · https://archive.org/download/historysiegegibr00drin/historysiegegibr00drin_djvu.txt · SHA-256 `9a0c3c3e45f39e2f…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Cùng đoạn: 'eggs, 6d. each : and candles, 2s. 6d. per pound'. Giá ngay trước cứu viện Rodney (1/1780); khi tin cứu viện tới 'the price of provisions… immedi- ately fell more than two-thirds' (p.89-90).

**S053** · MÂU THUẪN · phía: Anh · nhạy cảm: THẤP · as of: 2026-10-17 · (gói: V-A2-38)
- Claim (EN): Scurvy relief: a Danish dogger from Malaga laden with lemons and oranges was boarded and bought by the governor (Drinkwater: the 11th, autumn 1780); lemons had almost instantaneous effect.
- Trích nguyên văn (en): > She was-a Dane from Malaga, laden with lemons and oranges, i which the governor immediately purchased and distributed to the garrison.
- Nguồn: John Drinkwater, A History of the Siege of Gibraltar 1779-1783, new ed., London: John Murray, 1905 (text of 1785 original), archive.org OCR djvu.txt [so-cap] · Ch. IV, p. 120 (ed. 1905) · https://archive.org/download/historysiegegibr00drin/historysiegegibr00drin_djvu.txt · SHA-256 `9a0c3c3e45f39e2f…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Tàu Đan Mạch (không phải Hà Lan — nó đi trong 'A Dutch convoy'). NGÀY: Drinkwater 'The nth' (=11th), tháng suy từ ngữ cảnh = 10/1780; Spilsbury (p.22): '20th … a Danish dogger was brought in by the boats, lemons' dưới tiêu đề OCTOBER 1780. → 'tháng 10/1780'. Câu sau: 'The salutary effects were almost instantaneous'.

**S054** · XÁC MINH · phía: Anh · nhạy cảm: THẤP · as of: 2026-10-17 · (gói: V-A2-39)
- Claim (EN): Rodney's relief: news on arrival that on 8 Jan 1780 Rodney captured a Caracas Company convoy; convoy reached Gibraltar the night of ~18 Jan 1780 after defeating Langara (Moonlight Battle, 16 Jan); 21 sail of the line.
- Trích nguyên văn (en): > on the 8th of January Admiral Sir George Brydges Rodney had captured off the coast of Portugal, a Spanish 64-gun ship, five of 32 and 28 guns, with fifteen merchantmen, belonging to the Caracca Com- pany, going from Bilbao to Cadiz ; and that, with a fleet of twenty-one sail of the line and a large convoy of merchant-ships and transports, he was proceeding to our relief.
- Nguồn: John Drinkwater, A History of the Siege of Gibraltar 1779-1783, new ed., London: John Murray, 1905 (text of 1785 original), archive.org OCR djvu.txt [so-cap] · Ch. III, pp. 89-91 (ed. 1905) · https://archive.org/download/historysiegegibr00drin/historysiegegibr00drin_djvu.txt · SHA-256 `9a0c3c3e45f39e2f…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Ngày đến: đoạn sau 'The weather on the 17th was very hazy; but clearing up the succeeding day…' → tối 18/1/1780 Apollo vào cảng 'about eleven'; 19/1 Edgar đưa Langara vào. Ngày chính xác của đoàn tàu: suy luận 18–19/1/1780.

**S055** · XÁC MINH · phía: Anh · nhạy cảm: THẤP · as of: 2026-10-17 · (gói: V-A2-40)
- Claim (EN): Darby's relief fleet sighted at daybreak 12 April 1781; stores landed in nine or ten days.
- Trích nguyên văn (en): > At daybreak, on the 12th of April, the much-expected fleet, under the command of Admiral Darby, was in sight from our signal-house, but was not discernible from below, being obscured by a thick mist in the Gut.
- Nguồn: John Drinkwater, A History of the Siege of Gibraltar 1779-1783, new ed., London: John Murray, 1905 (text of 1785 original), archive.org OCR djvu.txt [so-cap] · Ch. V, pp. 147-150 (ed. 1905) · https://archive.org/download/historysiegegibr00drin/historysiegegibr00drin_djvu.txt · SHA-256 `9a0c3c3e45f39e2f…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Hình ảnh: sương mù tan 'like the curtain of a vast theatre'. 'the stores were landed, with the assistance of the navy, in nine or ten days' (p.150).

**S056** · XÁC MINH · phía: Anh · nhạy cảm: THẤP · as of: 2026-10-17 · (gói: V-A2-41)
- Claim (EN): Howe's relief: on the evening of (implied) 11 Oct 1782 the Latona reported Howe's fleet of 34 sail of the line, 6 frigates, 31 ordnance transports and over 1,600 troops; most transports were swept into the Mediterranean; 25th and 59th Regiments landed on 18 Oct 1782.
- Trích nguyên văn (en): > com- manded by Lord Howe, consisting of 34 sail-of-the- line, including 11 three-deckers, with 6 frigates and 31 ordnance transports, and a reinforcement of upward of 1,600 men for the garrison.
- Nguồn: John Drinkwater, A History of the Siege of Gibraltar 1779-1783, new ed., London: John Murray, 1905 (text of 1785 original), archive.org OCR djvu.txt [so-cap] · Ch. VIII, pp. 324, 331 (ed. 1905) · https://archive.org/download/historysiegegibr00drin/historysiegegibr00drin_djvu.txt · SHA-256 `9a0c3c3e45f39e2f…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Ngày 11/10 SUY LUẬN (bão đêm 10→11, Latona đến 'About sunset'; câu sau nhắc 'early on the 12th'). Quân đổ bộ 'The i8th' (18/10). Howe rời đi 19/10.

**S057** · XÁC MINH · phía: Anh · nhạy cảm: THẤP · as of: 2026-10-17 · (gói: V-A2-51)
- Claim (EN): Ancell's journal also records small boats bringing lemons and oranges from Tangier as 'very salutary in the cure of the scurvy'.
- Trích nguyên văn (en): > This morning arrived from Tangier, a fmall boat with lemons and oranges ;--a ve- ry ufeful article, as they are very falutary in the cure of the fcurvy
- Nguồn: Samuel Ancell (58th Regt), A Circumstantial Journal of the Long and Tedious Blockade and Siege of Gibraltar, 1784, archive.org OCR djvu.txt [so-cap] · Journal entry (1780), pp. ~25-30 · https://archive.org/download/acircumstantial00ancegoog/acircumstantial00ancegoog_djvu.txt · SHA-256 `67d61d0aced58597…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Nguồn sơ cấp thứ hai (lính 58th). OCR ſ→f. Ngày cụ thể chưa xác định từ OCR.

### Great Siege — đạn nung đỏ, lò

**S058** · XÁC MINH · phía: Anh · nhạy cảm: THẤP · as of: 2026-10-17 · (gói: V-A2-14)
- Claim (EN): First recorded experiments with red-hot shot by the garrison: 23 and 25 September 1779 (carcasses also thrown).
- Trích nguyên văn (en): > The same day some experi- ments were made with red-hot shot : this practice was continued on the 25th, when some carcasses were also thrown, and much approved.
- Nguồn: John Drinkwater, A History of the Siege of Gibraltar 1779-1783, new ed., London: John Murray, 1905 (text of 1785 original), archive.org OCR djvu.txt [so-cap] · Ch. III, p. 66 (ed. 1905) · https://archive.org/download/historysiegegibr00drin/historysiegegibr00drin_djvu.txt · SHA-256 `9a0c3c3e45f39e2f…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: 'The same day' = 23 [Sept 1779] (câu trước: 'The 23rd, the corps of engineers were formed…'). Đây là thử nghiệm, chưa phải dùng đại trà.

**S059** · XÁC MINH · phía: Anh · nhạy cảm: THẤP · as of: 2026-10-17 · (gói: V-A2-15)
- Claim (EN): On 8 Sept 1782, on Lt-Gen Boyd's recommendation, the northern batteries opened at 7 a.m. with red-hot shot and carcasses, burning the Mahon battery and much of the parallel.
- Trích nguyên văn (en): > At seven o'clock, the town-guards being relieved, the firing commenced from all the northern batteries which bore upon the western part of the parallel, and was sup- ported through the day with admirable precision and vivacity. The effect of the red-hot shot and carcasses exceeded our most sanguine expectations.
- Nguồn: John Drinkwater, A History of the Siege of Gibraltar 1779-1783, new ed., London: John Murray, 1905 (text of 1785 original), archive.org OCR djvu.txt [so-cap] · Ch. VII, pp. 281-284 (ed. 1905) · https://archive.org/download/historysiegegibr00drin/historysiegegibr00drin_djvu.txt · SHA-256 `9a0c3c3e45f39e2f…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Ngày: 'By the morning of the 8th' [Sept 1782]; giờ 07:00. Boyd đề xuất ngày 6/9 (p.280-281).

**S060** · XÁC MINH · phía: Anh · nhạy cảm: THẤP · as of: 2026-10-17 · (gói: V-A2-16)
- Claim (EN): On 13 Sept 1782 the portable furnaces were insufficient, so shot were heated in wood fires in corners of buildings — the men called them 'roasted potatoes'.
- Trích nguyên văn (en): > As the ordnance portable furnaces for heating shot were not sufficient in number to supply the demands of the artillery when the attack was at its height, large fires were kindled of wood in the corners of the nearest buildings, and shot, being thrown into these piles, were soon heated red-hot. These supplies were jocularly termed by the men " roasted potatoes."
- Nguồn: John Drinkwater, A History of the Siege of Gibraltar 1779-1783, new ed., London: John Murray, 1905 (text of 1785 original), archive.org OCR djvu.txt [so-cap] · Ch. VII, footnote p. 297 (ed. 1905) · https://archive.org/download/historysiegegibr00drin/historysiegegibr00drin_djvu.txt · SHA-256 `9a0c3c3e45f39e2f…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Hình ảnh mạnh cho hoạt hình (lò nung + đống lửa góc nhà). Cùng trang: lò 'grates and furnaces for heating shot ordered to be lighted' sáng 13/9.

**S061** · XÁC MINH · phía: Anh · nhạy cảm: THẤP · as of: 2026-10-17 · (gói: V-A2-17)
- Claim (EN): After 13 Sept 1782 the engineers built lime-kiln-like furnaces able to heat over 100 balls in an hour and a quarter.
- Trích nguyên văn (en): > the engineers erected kilns (similar to those used in burn- ing lime, but smaller) in various parts of the garrison. They were large enough to heat upward of 100 balls in an hour and a quarter
- Nguồn: John Drinkwater, A History of the Siege of Gibraltar 1779-1783, new ed., London: John Murray, 1905 (text of 1785 original), archive.org OCR djvu.txt [so-cap] · Ch. VII, p. 307 (ed. 1905) · https://archive.org/download/historysiegegibr00drin/historysiegegibr00drin_djvu.txt · SHA-256 `9a0c3c3e45f39e2f…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Số liệu kỹ thuật cho cảnh lò nung đạn.

### Great Siege — phố bị bắn cháy 1781

**S062** · XÁC MINH · phía: Anh · nhạy cảm: TRUNG — dân thường bị pháo kích; nói bằng sự kiện, không cảnh thương vong · as of: 2026-10-17 · (gói: V-A2-18)
- Claim (EN): 12 April 1781: Darby's relief convoy anchored about 10:45 a.m.; the Spanish batteries (114 pieces incl. ~50 mortars) immediately opened fire; terrified inhabitants fled south leaving property to the soldiers.
- Trích nguyên văn (en): > The miserable and terrified inhabitants, who just before were congratulating each other on the arrival of the fleet, now changed their exultation to sorrow, and flocked, old and young, men, women, and children, in the greatest confusion, to the southward, leaving their property, unsecured, to the mercy of the soldiers.
- Nguồn: John Drinkwater, A History of the Siege of Gibraltar 1779-1783, new ed., London: John Murray, 1905 (text of 1785 original), archive.org OCR djvu.txt [so-cap] · Ch. V, pp. 148-149 (ed. 1905) · https://archive.org/download/historysiegegibr00drin/historysiegegibr00drin_djvu.txt · SHA-256 `9a0c3c3e45f39e2f…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Giờ: 'About three-quarters past lo o'clock' (=10:45) đoàn tàu thả neo, pháo TBN bắn ngay; 'Be- tween I and 2 o'clock their firing abated'; 'About 5 o'clock … again opened'. Số pháo TBN: 'amount to 114 pieces of artillery'.

**S063** · XÁC MINH · phía: Anh · nhạy cảm: TRUNG — cướp phá của chính quân đồn trú; Drinkwater biện hộ (do con buôn găm hàng) · as of: 2026-10-17 · (gói: V-A2-19)
- Claim (EN): 14 April 1781: shells with incendiary matter set fire to a wine-house; 4-5 houses burned; from then soldiers, through 'resentment and intoxication', broke into merchants' hoarded stores.
- Trích nguyên văn (en): > these combustibles set fire to a wine-house in the green-market, near the Spanish church, and before the fire could be extinguished, four or five houses were burnt to the ground.
- Nguồn: John Drinkwater, A History of the Siege of Gibraltar 1779-1783, new ed., London: John Murray, 1905 (text of 1785 original), archive.org OCR djvu.txt [so-cap] · Ch. V, p. 152 (ed. 1905) · https://archive.org/download/historysiegegibr00drin/historysiegegibr00drin_djvu.txt · SHA-256 `9a0c3c3e45f39e2f…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Câu sau: 'From this moment we may date the commencement of the irregularities into which, through resentment and intoxication, the soldiers were betrayed.' Nêu cả hai: hành vi cướp & lời giải thích của tác giả người Anh. Tránh cảnh say xỉn gây cười.

**S064** · XÁC MINH · phía: Anh · nhạy cảm: TRUNG · as of: 2026-10-17 · (gói: V-A2-20)
- Claim (EN): During the 1781 looting soldiers destroyed liquor and goods with extravagance (Drinkwater saw a pig roasted over a fire of cinnamon); a plundering soldier of the 58th was later hanged as an example.
- Trích nguyên văn (en): > Among other instances of caprice and extravagance, I recollect seeing a party of soldiers roast a pig by a fire made of cinnamon.
- Nguồn: John Drinkwater, A History of the Siege of Gibraltar 1779-1783, new ed., London: John Murray, 1905 (text of 1785 original), archive.org OCR djvu.txt [so-cap] · Ch. V, p. 153 (ed. 1905) · https://archive.org/download/historysiegegibr00drin/historysiegegibr00drin_djvu.txt · SHA-256 `9a0c3c3e45f39e2f…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Chi tiết hình ảnh mạnh (quế làm củi). Xử tử kẻ cướp: p.~160 'a soldier of the 58th regiment was executed on the grand parade, at the door of the store where he was detected plundering' (ngày 5, tháng 5/1781) — nói, không diễn cảnh treo cổ.

### Great Siege — tổng công kích, pin nổi 13/9/1782

**S065** · XÁC MINH · phía: Anh · nhạy cảm: THẤP · as of: 2026-10-17 · (gói: V-A2-21)
- Claim (EN): 12 Sept 1782: combined fleets of France and Spain arrived (7 three-deckers, 31 two-deckers etc.); in total 47 sail of the line, 10 battering-ships with 212 guns, ~200 land guns and an army of near 40,000 (British estimate).
- Trích nguyên văn (en): > 47 sail of the line, including 3 inferior 2- deckers, 10 battering-ships, deemed perfect in design, and esteemed invincible, carrying 212 guns ; innumer- able frigates, xebeques, bomb-ketches, cutters, gun and mortar-boats, and smaller craft for disembarking men ; these were assembled in the bay. On the land 1782] THE RIVAL CHANCES 293 side were most stupendous and strong batteries and works, mounting 200 pieces of iieav}'- ordnance, and protected by an army of near 40,000 men
- Nguồn: John Drinkwater, A History of the Siege of Gibraltar 1779-1783, new ed., London: John Murray, 1905 (text of 1785 original), archive.org OCR djvu.txt [so-cap] · Ch. VII, pp. 292-293 (ed. 1905) · https://archive.org/download/historysiegegibr00drin/historysiegegibr00drin_djvu.txt · SHA-256 `9a0c3c3e45f39e2f…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Số phía Anh. Phía TBN (Montero p.356): quân vây 33.000 sau khi Crillon và Falkenstein đến. Đồn Anh: 'scarcely consisted of more than 7,000 effective men, including the marine brigade'. Dùng 'khoảng 33.000–40.000' và nêu nguồn.

**S066** · MÂU THUẪN · phía: Anh · nhạy cảm: THẤP · as of: 2026-10-17 · (gói: V-A2-22)
- Claim (EN): 13 Sept 1782: battering-ships got under way ~6:45 a.m., bore down a little past 9; flagship moored ~900 yards off King's Bastion; garrison opened fire at ~9:45 when the first ship anchored.
- Trích nguyên văn (en): > but as soon as the first ship dropped her anchors, which was about a quarter before ten o'clock, that instant our firing commenced.
- Nguồn: John Drinkwater, A History of the Siege of Gibraltar 1779-1783, new ed., London: John Murray, 1905 (text of 1785 original), archive.org OCR djvu.txt [so-cap] · Ch. VII, pp. 295-296 (ed. 1905) · https://archive.org/download/historysiegegibr00drin/historysiegegibr00drin_djvu.txt · SHA-256 `9a0c3c3e45f39e2f…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: GIỜ (cho bộ đếm & mặt trời): Drinkwater: 'About a quarter before seven' rời neo; 'a little past nine o'clock' tiến vào; khai hoả ~09:45. Spilsbury (p.77): 'At about $ past 9 a.m. ten junk ships came' (=½ past 9, 09:30). Montero (p.360): 'á las diez y veinte y cinco minu- tos de la mañana' (10:25) toàn bộ phía Pháp–TBN đồng loạt khai hoả. Đề xuất: tàu vào vị trí 09:30–09:45, đấu pháo toàn diện ~10:00–10:25.

**S067** · XÁC MINH · phía: TBN · nhạy cảm: THẤP · as of: 2026-10-17 · (gói: V-A2-23)
- Claim (EN): Montero: at 10:25 a.m. on 13 Sept the floating batteries, land batteries, fleet and gunboats (about 400 pieces) opened fire together; red-hot shot used from 12, general by 2 p.m.
- Trích nguyên văn (es): > á las diez y veinte y cinco mi- nutos de la mañana (1 3 de setiembre) las flotantes, las baterías y esplanadas de tierra, buques de la escua- dra y cañoneras, que en todo componían sobre cuatro- cientas piezas, rompieron á un tiempo el fuego
- Nguồn: Francisco María Montero, Historia de Gibraltar y de su campo, Cádiz 1860, archive.org OCR djvu.txt [hoc-thuat] · pp. 360-361 · https://archive.org/download/bub_gb_4_AqUai2tkIC/bub_gb_4_AqUai2tkIC_djvu.txt · SHA-256 `d99126f25d1c838e…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Khớp Drinkwater về 'upward of four hundred pieces' (p.296: 424 = 328 của địch + 96 của đồn). Đạn nung: Drinkwater 'began to be used about twelve, but were not general till between one and two o'clock'.

**S068** · MÂU THUẪN · phía: Anh · nhạy cảm: THẤP · as of: 2026-10-17 · (gói: V-A2-24)
- Claim (EN): Drinkwater's 'authentic list' of the 10 battering-ships: 142 guns in use, 70 in reserve, 5,260 men (about 36 men per gun).
- Trích nguyên văn (en): > 142 70 5,260 N.B. — About 36 men to each gun in use, besides sailors, etc., to work the ships.
- Nguồn: John Drinkwater, A History of the Siege of Gibraltar 1779-1783, new ed., London: John Murray, 1905 (text of 1785 original), archive.org OCR djvu.txt [so-cap] · Ch. VII, p. 306 (ed. 1905) · https://archive.org/download/historysiegegibr00drin/historysiegegibr00drin_djvu.txt · SHA-256 `9a0c3c3e45f39e2f…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: HAI PHÍA: Anh (Drinkwater) 142 pháo dùng + 70 dự bị (=212), 5.260 người. TBN (Montero p.359): '138 5190' (138 pháo, 5.190 người). Spilsbury (danh sách từ thuỷ thủ trưởng tàu Sta. Paula): tổng OCR '4560' người. Todo a Babor (Gaceta de Madrid): bảng tổng ~5.196 người, 172 pháo (tính từ bảng). Cách nói: '10 khẩu đội nổi, khoảng 140 pháo hướng về thành, hơn 5.000 người'.

**S069** · MÂU THUẪN · phía: Anh · nhạy cảm: CAO — tử vong hàng loạt, chết cháy/đuối; nói bằng số, không diễn cảnh chết · as of: 2026-10-17 · (gói: V-A2-25)
- Claim (EN): British estimate: enemy loss on 13-14 Sept 'not less than 2,000 men including the prisoners'; 357 were rescued (9 officers, 2 priests, 334 Spanish men + 1 officer and 11 Frenchmen).
- Trích nguyên văn (en): > The loss sustained by the enemy could never be ascertained ; but from the information of the prisoners, and the numbers seen dead on board the ships, we estimated it could not be less than 2,000 men including the prisoners.
- Nguồn: John Drinkwater, A History of the Siege of Gibraltar 1779-1783, new ed., London: John Murray, 1905 (text of 1785 original), archive.org OCR djvu.txt [so-cap] · Ch. VII, pp. 301, 304 (ed. 1905) · https://archive.org/download/historysiegegibr00drin/historysiegegibr00drin_djvu.txt · SHA-256 `9a0c3c3e45f39e2f…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: HAI PHÍA: Anh ước ≥2.000 (gồm tù binh). Montero (TBN, p.365 chú thích): 'Gradúase en mas de dos mil hom- bres la pérdida'. Phía Pháp ('Conseil de guerre privé', p.201): chỉ 185 thương vong do pháo trước khi đốt tàu (V-A2-27) — con số này KHÔNG gồm người chết khi tàu cháy/nổ. Wikipedia (dẫn Gaceta de Madrid qua todoababor): 719 thương vong trên tàu; Chartrand: tổng 1.473 — chưa tải được bảng số Gaceta (ảnh). Cứu sống: 357 (p.301).

**S070** · MÂU THUẪN · phía: Anh · nhạy cảm: CAO — nói bằng số · as of: 2026-10-17 · (gói: V-A2-26)
- Claim (EN): Garrison casualties on 13 Sept 1782: killed 1 officer, 2 sergeants, 13 rank and file (16); wounded 5 officers and 63 rank and file (68).
- Trích nguyên văn (en): > Total i 2 o 13 5 o o 63 Officers killed and wounded f Artillery, Captain Reeves killed
- Nguồn: John Drinkwater, A History of the Late Siege of Gibraltar, 3rd ed., Dublin 1786, archive.org OCR djvu.txt [so-cap] · Ch. 13 Sept 1782 return, p. 387 (Dublin 1786) · https://archive.org/download/historyoflatesie00driniala/historyoflatesie00driniala_djvu.txt · SHA-256 `7576bb8fb645db34…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Dòng tổng OCR 'i 2 o 13 | 5 o o 63' = chết: 1 sĩ quan, 2 hạ sĩ quan, 0 tay trống, 13 lính (=16); bị thương: 5 sĩ quan, 63 lính (=68). Wikipedia (dẫn McGuffie) ghi 15 chết, 68 bị thương. Spilsbury (p.77) ghi một con số riêng cho đợt pháo 9/9: 'Our loss in this attack 8 killed and 17 wounded' (không phải 13/9). Đề xuất: 'khoảng 16 chết, 68 bị thương' (Drinkwater).

**S071** · MÂU THUẪN · phía: Phap · nhạy cảm: CAO — văn bản biện hộ của người thiết kế; số chỉ tính thương vong do pháo, không tính người chết khi đốt/nổ tàu · as of: 2026-10-17 · (gói: V-A2-27)
- Claim (EN): French-side account (Conseil de guerre privé, 1785): 80 men hors de combat on Tailla Piedra, 75 on Pastora, 25 on San Paolo, 1-2 or none on the other seven — 185 killed or wounded in 34 hours of presence.
- Trích nguyên văn (fr): > Il y eut 80 hommes hors de combat fur la Tailla-piedra , 75 fur la Pafîora ,25 fur la San-Paolo ; 1 , 2, ou rien, fur les fept autres batteries ; rien à l’attaque de terre ; en tout 185 hommes tués ou bielles pendant 34 heures de prélénce
- Nguồn: [Anon., traditionally attributed to J.-C.-É. Le Michaud d'Arçon] Conseil de guerre privé sur l'événement de Gibraltar en 1782, 1785, archive.org OCR djvu.txt [so-cap] · p. 201 · https://archive.org/download/bub_gb_Lx5oLGPGvfgC/bub_gb_Lx5oLGPGvfgC_djvu.txt · SHA-256 `8e958846266e06bd…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: OCR giữ nguyên (ſ→f, 'bielles'=blessés, 'prélénce'=présence). Tác giả tác phẩm khuyết danh, truyền thống gán cho d'Arçon — ghi 'một bản biện hộ phía Pháp năm 1785'. p.296: tác giả phản bác một 'mémoire' ghi 300 người, nói 'nos appels les plus authentiques n'ont jamais donné qu'environ 180 hommes tués ou blessés'.

**S072** · XÁC MINH · phía: Phap · nhạy cảm: TRUNG — số tự khai của một bên · as of: 2026-10-17 · (gói: V-A2-28)
- Claim (EN): The same French account says the French army lost in total only 173 killed or wounded during the entire siege including 13 September.
- Trích nguyên văn (fr): > l’armée françoife n’a eu en tout que 173 hommes tués ou blefiés.
- Nguồn: [Anon., traditionally attributed to J.-C.-É. Le Michaud d'Arçon] Conseil de guerre privé sur l'événement de Gibraltar en 1782, 1785, archive.org OCR djvu.txt [so-cap] · pp. 102-103 · https://archive.org/download/bub_gb_Lx5oLGPGvfgC/bub_gb_Lx5oLGPGvfgC_djvu.txt · SHA-256 `8e958846266e06bd…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Chỉ là quân Pháp trên bộ/khẩu đội; tổng thương vong Pháp–TBN theo Montero ~6.000 (V-A2-33).

**S073** · XÁC MINH · phía: Phap · nhạy cảm: TRUNG — tranh cãi trách nhiệm · as of: 2026-10-17 · (gói: V-A2-29)
- Claim (EN): French account: the inventor had asked that all floating batteries be tested against red-hot shot before facing the enemy; the test was refused.
- Trích nguyên văn (fr): > l’expérience que l’in- venteur avoit demandée de paire pajfer toutes les batteries flottantes à l'épreuve des boulets rouges avant de les préfenter à l’ennemi , cette confiance naturelle de la part de l’artifie , infpira une fécurité qui fervit même de prétexte au refus de l’experience demandée.
- Nguồn: [Anon., traditionally attributed to J.-C.-É. Le Michaud d'Arçon] Conseil de guerre privé sur l'événement de Gibraltar en 1782, 1785, archive.org OCR djvu.txt [so-cap] · pp. 49-50 · https://archive.org/download/bub_gb_Lx5oLGPGvfgC/bub_gb_Lx5oLGPGvfgC_djvu.txt · SHA-256 `8e958846266e06bd…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: OCR: 'paire pajfer'=faire passer. Montero (p.365) xác nhận d'Arçon than rằng 'tampoco se habían probado previamente con la bala roja, según él habia pedido'. Đối lập: Drinkwater kể tù binh nói 'they had been taught to believe the garrison would not be able to discharge many rounds of hot balls'.

**S074** · XÁC MINH · phía: Anh · nhạy cảm: CAO — cảnh cháy nổ có người; diễn tàu cháy từ xa, không diễn người · as of: 2026-10-17 · (gói: V-A2-30)
- Claim (EN): By the morning of 14 Sept all ten battering-ships were destroyed: several blew up (~5 a.m. onwards), three burned to the water's edge, the last was burned by the British in the afternoon.
- Trích nguyên văn (en): > Of the 6 ships which were still in flames, 3 blew up before 11 o'clock; the other 3 burnt to the water's edge, the magazines being wetted by the enemy before the principal officers quitted the ships.
- Nguồn: John Drinkwater, A History of the Siege of Gibraltar 1779-1783, new ed., London: John Murray, 1905 (text of 1785 original), archive.org OCR djvu.txt [so-cap] · Ch. VII, pp. 299-302 (ed. 1905) · https://archive.org/download/historysiegegibr00drin/historysiegegibr00drin_djvu.txt · SHA-256 `9a0c3c3e45f39e2f…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Mốc giờ 14/9: ~01:00 tàu đầu tiên bốc cháy hoàn toàn; 02:00 'one continued blaze'; 03-04h thêm 6 tàu cháy; ~05:00 một tàu nổ, 05:15 tàu thứ hai nổ; trước 11:00 thêm 3 tàu nổ; chiều: tàu cuối bị đốt (Capt. Gibson). Montero: TBN tự đốt 7 tàu theo lệnh Moreno 'con tal azoramiento y precipita- ción, que muchas empezaron á arder con la gente toda- vía dentro' (p.362) — điểm nhạy cảm.

**S075** · XÁC MINH · phía: Anh · nhạy cảm: THẤP · as of: 2026-10-17 · (gói: V-A2-31)
- Claim (EN): On 13 Sept the garrison fired upwards of 8,300 rounds (more than half hot shot) and 716 barrels of powder, with 80 cannon, 7 mortars and 9 howitzers against 328 enemy pieces.
- Trích nguyên văn (en): > The enemy, in this action, had 328 pieces ot heavy ordnance in play; whilst the garrison had only 80 cannon, 7 mortars, and 9 howitzers in opposition. Upwards of 8,300 rounds (more than half of which were hot shot), and 716 barrels of powder, were expended by our artillery.
- Nguồn: John Drinkwater, A History of the Siege of Gibraltar 1779-1783, new ed., London: John Murray, 1905 (text of 1785 original), archive.org OCR djvu.txt [so-cap] · Ch. VII, p. 305 (ed. 1905) · https://archive.org/download/historysiegegibr00drin/historysiegegibr00drin_djvu.txt · SHA-256 `9a0c3c3e45f39e2f…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: 'ot'=of (OCR). Hậu cần ngày 13/9.

### Great Siege — quân số, thương vong cả cuộc vây

**S076** · XÁC MINH · phía: Anh · nhạy cảm: CAO — nói bằng số, không diễn cảnh chết · as of: 2026-10-17 · (gói: V-A2-32)
- Claim (EN): Drinkwater's abstract of total garrison loss: killed and died of wounds 333; disabled by wounds 138; died of sickness 536 (excluding scurvy deaths 1779-80); discharged 181; deserted 43; total 1,231.
- Trích nguyên văn (en): > Killed, and dead of wounds 333 Disabled by wounds (discharged) 138 Dead of sickness, exclusive of those who died of the scurvy in 1779 and 1780 .536 Discharged from incurable complaints 181 Deserted 43 Total 1231
- Nguồn: John Drinkwater, A History of the Siege of Gibraltar 1779-1783, new ed., London: John Murray, 1905 (text of 1785 original), archive.org OCR djvu.txt [so-cap] · Appendix, p. 367 (ed. 1905) · https://archive.org/download/historysiegegibr00drin/historysiegegibr00drin_djvu.txt · SHA-256 `9a0c3c3e45f39e2f…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Phía Anh, số chính thức của đồn. Lưu ý '536' KHÔNG gồm người chết vì scorbut 1779–80. Bản 1785 xác nhận 333 và 138. Montero (TBN) ghi đồn Anh mất 'cerca de dos mil hombres' (V-A2-33) — khác vì cách tính.

**S077** · XÁC MINH · phía: TBN · nhạy cảm: CAO — nói bằng số · as of: 2026-10-17 · (gói: V-A2-33)
- Claim (EN): Montero: the besieged lost nearly 2,000 men, the besiegers nearly 6,000 from all causes; the place received about 258,387 rounds and returned about 200,300; the enterprise cost Spain twelve million duros.
- Trích nguyên văn (es): > Los últimos sufrieron una pérdida de cerca de dos mil hombres. La nuestra se aproximó á seis mil por todas causas. Recibió la plaza de las baterías de tierra y cañoneras en los tres años y siete meses que duró el sitio unos 258.387 disparos de mortero y cañón. Devolvió aque- lla y sus cañoneras unos 200.300. Costó la empresa á España doce millones de duros.
- Nguồn: Francisco María Montero, Historia de Gibraltar y de su campo, Cádiz 1860, archive.org OCR djvu.txt [hoc-thuat] · p. 373 · https://archive.org/download/bub_gb_4_AqUai2tkIC/bub_gb_4_AqUai2tkIC_djvu.txt · SHA-256 `d99126f25d1c838e…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Đây là số TBN cho tổn thất Pháp–TBN cả cuộc vây (~6.000 'por todas causas'). Số đạn Montero lấy lại từ Drinkwater (258.387) nhưng ghi 200.300 thay vì 205.328/200.600 — khác biệt nhỏ.

**S078** · XÁC MINH · phía: Anh · nhạy cảm: THẤP · as of: 2026-10-17 · (gói: V-A2-34)
- Claim (EN): Garrison strength when communication closed (June 1779): 5,382 men.
- Trích nguyên văn (en): > Total . . 209 59 313 169 4,632 — making an army of 5,382 men.
- Nguồn: John Drinkwater, A History of the Siege of Gibraltar 1779-1783, new ed., London: John Murray, 1905 (text of 1785 original), archive.org OCR djvu.txt [so-cap] · Ch. III, p. 51 (ed. 1905) · https://archive.org/download/historysiegegibr00drin/historysiegegibr00drin_djvu.txt · SHA-256 `9a0c3c3e45f39e2f…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Tăng lên: tháng 9/1782 'about 7,500 men; upwards of 400 of whom were in the hospital' (p.283); Howe đưa thêm 'upward of 1,600 men' (p.324).

**S079** · XÁC MINH · phía: Anh · nhạy cảm: THẤP · as of: 2026-10-17 · (gói: V-A2-35)
- Claim (EN): In September 1782, with the marine brigade, the garrison numbered about 7,500 men, over 400 in hospital.
- Trích nguyên văn (en): > The strength of the garrison, with the marine brigade (including the officers), in September, was about 7,500 men; upwards 1782] DETAIL OF GUARDS 283 of 400 of whom were in the hospital.
- Nguồn: John Drinkwater, A History of the Siege of Gibraltar 1779-1783, new ed., London: John Murray, 1905 (text of 1785 original), archive.org OCR djvu.txt [so-cap] · Ch. VII, pp. 282-283 (ed. 1905) · https://archive.org/download/historysiegegibr00drin/historysiegegibr00drin_djvu.txt · SHA-256 `9a0c3c3e45f39e2f…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Drinkwater p.293 cũng viết 'scarcely consisted of more than 7,000 effective men'.

### Great Siege — đường hầm 1782, bệ pháo Koehler

**S080** · XÁC MINH · phía: Anh · nhạy cảm: THẤP · as of: 2026-10-17 · (gói: V-A2-42)
- Claim (EN): On 25 May 1782 the engineers began mining a gallery from above Farringdon's battery (Willis's) through the rock to a notch below Green's Lodge where the governor proposed a battery.
- Trích nguyên văn (en): > The 25th the engineers began to mine a gallery from a place above Farring- don's battery (Willis's), to communicate through the rock to a notch or projection of the rock, below Green's Lodge, in which the governor proposed to make a battery.
- Nguồn: John Drinkwater, A History of the Siege of Gibraltar 1779-1783, new ed., London: John Murray, 1905 (text of 1785 original), archive.org OCR djvu.txt [so-cap] · Ch. VI, p. 244 (ed. 1905) · https://archive.org/download/historysiegegibr00drin/historysiegegibr00drin_djvu.txt · SHA-256 `9a0c3c3e45f39e2f…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Tháng 5/1782 (bản 1786 có tiêu đề lề 'May.]'). Drinkwater KHÔNG nêu tên Ince; tên Ince có trong Spilsbury (V-A2-43). Wikipedia (Henry Ince, dẫn Connolly) trích lệnh Col. Green ngày 22/5/1782 '12 miners, under the executive direction of Sergeant-major Ince' — CHƯA tải được Connolly.

**S081** · XÁC MINH · phía: Anh · nhạy cảm: THẤP · as of: 2026-10-17 · (gói: V-A2-43)
- Claim (EN): Spilsbury, 4 July 1782: Sergeant Ince's gallery — 13 men in about 5 weeks cut about 82 feet long by 8 feet high and broad in the solid rock of the North Face.
- Trích nguyên văn (en): > Serjt. Tnce’s gallery going on well; 13 men, in abont 5 weeks, have cut about 82 fect long by 8 feet high and broad, in the solid rock, North Face.
- Nguồn: Captain John Spilsbury (12th Regt), A Journal of the Siege of Gibraltar 1779-1783, ed. B.H.T. Frere, Gibraltar Garrison Library 1908, archive.org OCR djvu.txt [so-cap] · p. 67, entry July 4th 1782 · https://archive.org/download/ajournalsiegegi00spilgoog/ajournalsiegegi00spilgoog_djvu.txt · SHA-256 `f6c2f3a940cde7ac…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: OCR: 'Tnce'=Ince, 'abont'=about, 'fect'=feet. 82 ft ≈ 25 m. Visitgibraltar (theo kết quả tìm kiếm, không tải được – 403) ghi 18 người — MÂU THUẪN số người (13 vs 18); dùng 13 (sơ cấp).

**S082** · XÁC MINH · phía: Anh · nhạy cảm: THẤP · as of: 2026-10-17 · (gói: V-A2-44)
- Claim (EN): 15 July 1782: an embrasure was blasted through the face of the rock for ventilation; the blast startled the Spanish camp; a 24-pounder was then mounted.
- Trích nguyên văn (en): > The same day an embrasure was opened in the face of the Rock, communicating with the gallery above Farringdon's : the mine was loaded with an unusual quantity of powder, and the explosion was so amazingly loud, that almost the whole of the enemy's camp turned out at the report
- Nguồn: John Drinkwater, A History of the Siege of Gibraltar 1779-1783, new ed., London: John Murray, 1905 (text of 1785 original), archive.org OCR djvu.txt [so-cap] · Ch. VII, pp. 257-258 (ed. 1905) · https://archive.org/download/historysiegegibr00drin/historysiegegibr00drin_djvu.txt · SHA-256 `9a0c3c3e45f39e2f…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: 'The same day' = the 15th [July 1782]. Mục đích ban đầu: 'to communicate air to the work- men, who before were almost suffocated with the smoke'. Kỹ thuật: thuốc nổ ('blowing the different mines'). Chú thích p.258: 4–5 khẩu trước tháng 9, hơn 12 tháng sau tới mỏm đá → 'St. George's Hall'.

**S083** · XÁC MINH · phía: Anh · nhạy cảm: THẤP · as of: 2026-10-17 · (gói: V-A2-45)
- Claim (EN): By 5 August 1782 the gallery above Farringdon's extended 140 feet in the solid rock; all regimental miners were ordered to the works.
- Trích nguyên văn (en): > the governor, on the 5th, ordered all the miners in the different regiments into the King's works, to prosecute it with greater diligence, and assist in the gallery above Farringdon's, which now extended 140 feet in the solid rock.
- Nguồn: John Drinkwater, A History of the Siege of Gibraltar 1779-1783, new ed., London: John Murray, 1905 (text of 1785 original), archive.org OCR djvu.txt [so-cap] · Ch. VII, p. 261 (ed. 1905) · https://archive.org/download/historysiegegibr00drin/historysiegegibr00drin_djvu.txt · SHA-256 `9a0c3c3e45f39e2f…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Tháng 8/1782 (bản 1786 có tiêu đề 'Aug.]'). Tiến độ khác theo Spilsbury: 18/8 '165 feet', 28/8 '200 fect long, and has two 2[4] pounders'. Cuối vây (5/1783) Spilsbury: 'about 600 and odd feet long' (V-A2-46).

**S084** · MÂU THUẪN · phía: Anh · nhạy cảm: THẤP · as of: 2026-10-17 · (gói: V-A2-46)
- Claim (EN): Spilsbury, May 1783: Ince's gallery has 10 embrasures and an air hole and is about 600-odd feet long.
- Trích nguyên văn (en): > Ince’s gallery has 10 embrasures and an air hole cut, and is about 600 and odd feet long; the 9th chamber or cave is large enough for a guard room, has 2 doors, and is tolerably dry.
- Nguồn: Captain John Spilsbury (12th Regt), A Journal of the Siege of Gibraltar 1779-1783, ed. B.H.T. Frere, Gibraltar Garrison Library 1908, archive.org OCR djvu.txt [so-cap] · p. 107, entry ~10/11 May 1783 · https://archive.org/download/ajournalsiegegi00spilgoog/ajournalsiegegi00spilgoog_djvu.txt · SHA-256 `f6c2f3a940cde7ac…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Ngày OCR 'Wth' (10 hoặc 11/5/1783). MÂU THUẪN chiều dài cuối vây: 370 ft (113 m, visitgibraltar theo kết quả tìm kiếm – không tải được) vs ~600 ft (Spilsbury, 5/1783, sau khi hết vây) vs 908 ft cuối 1783 (Wikipedia/Fa & Finlayson). Con số 370 ft CHƯA XÁC MINH từ nguồn tải. Chiều dài đường hầm hiện mở cho khách: CHƯA XÁC MINH (trang chính thức 403).

**S085** · CHƯA XÁC MINH · phía: trung-lap · nhạy cảm: THẤP · as of: 2026-10-17 · (gói: V-A2-47)
- Claim (EN): Tertiary: Sergeant-Major Henry Ince (Soldier Artificers) proposed the tunnel; Col. Green's order of 22 May 1782 assigned 12 miners under him; by 1799 the tunnels reached nearly 4,000 ft.
- Trích nguyên văn (en): > Henry Ince – who had been promoted to the rank of Sergeant-Major in September 1781 – proposed to tunnel a gallery through the Rock.
- Nguồn: Wikipedia (EN), "Henry Ince", raw wikitext [bach-khoa] · Wikipedia 'Henry Ince' (citing Connolly p.14; Hughes & Migos p.248) · https://en.wikipedia.org/w/index.php?title=Henry_Ince&action=raw · SHA-256 `c14a47cff2c4d8d2…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Chỉ là bách khoa, chưa đối chiếu nguồn gốc (Connolly 1855 'History of the Royal Sappers and Miners'). Câu trích có trong file tải nhưng chưa có nguồn cấp 1. Sơ cấp xác nhận Ince phụ trách: Spilsbury 'Serjt. Ince's gallery'.

**S086** · XÁC MINH · phía: Anh · nhạy cảm: THẤP · as of: 2026-10-17 · (gói: V-A2-48)
- Claim (EN): 15 Feb 1782: trial of Lt Koehler's newly invented depressing gun carriage, approved by the governor.
- Trích nguyên văn (en): > The afternoon of the 15th, some practice was made from a gun mounted upon a new-constructed depress- ing carriage, the invention of Lieutenant Koehler, of the Royal Artillery, which was highly approved of by the governor and other officers present.
- Nguồn: John Drinkwater, A History of the Siege of Gibraltar 1779-1783, new ed., London: John Murray, 1905 (text of 1785 original), archive.org OCR djvu.txt [so-cap] · Ch. VI, p. 226 (ed. 1905) · https://archive.org/download/historysiegegibr00drin/historysiegegibr00drin_djvu.txt · SHA-256 `9a0c3c3e45f39e2f…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Tháng 2/1782 suy từ ngữ cảnh ('In the beginning of February' ngay trước; tháng 3 bắt đầu sau). Koehler cũng là sĩ quan tuỳ tùng của Eliott khi gặp Crillon (p.356).

**S087** · XÁC MINH · phía: TBN · nhạy cảm: THẤP · as of: 2026-10-17 · (gói: V-A2-49)
- Claim (EN): Spanish view: the ventilation blast in the Farringdon gallery made an opening so large that a gun was mounted; later four; origin of the battery known as San Jorge (St George's).
- Trích nguyên văn (es): > se formó un bo- quete tan grande por la escesiva -cantidad de pólvora cjue en la misma pusieron, que pareció bien colocar en el un cañón; y como dominaba nuestro campo surtió tan buen efecto, que meses adelante se colocaron hasta cuatro en la misma forma.
- Nguồn: Francisco María Montero, Historia de Gibraltar y de su campo, Cádiz 1860, archive.org OCR djvu.txt [hoc-thuat] · p. 358 · https://archive.org/download/bub_gb_4_AqUai2tkIC/bub_gb_4_AqUai2tkIC_djvu.txt · SHA-256 `d99126f25d1c838e…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Phía TBN thừa nhận hiệu quả các pháo trong hầm.

### Eo đất trước sân bay

**S088** · XÁC MINH · phía: trung-lap · nhạy cảm: Thấp. · as of: 2026-10-17 (ngày đọc) · (gói: V-A3-31)
- Claim (EN): Before the airfield, the neutral ground held a garrison camp, gardens and rifle-range butts, and was used for the townspeople's recreation; lengthening the strip meant relocating military installations.
- Trích nguyên văn (es): > Esta pista resultó ser más pequeña de lo deseable, pero no se ha tomado ninguna iniciativa para alargarla hasta hace muy poco, principalmente porque el efecto de tal alargamiento habría de implicar la reducción de la ya inadecuada zona utilizable para el esparcimiento de la población.
- Nguồn: Antonio Marquina Barrio, "La pista de aterrizaje de Gibraltar", Revista de Estudios Internacionales vol. 2 núm. 2 (abr–jun 1981), CEPC [hoc-thuat] · tr.307 (Mapa 1, chú thích) và tr.311 (memorandum Anh 11/1939) · https://www.cepc.gob.es/sites/default/files/2021-12/34994rei02002051.pdf · SHA-256 `c5e24d09cb641074…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Câu trích là bản dịch tiếng TBN memorandum của Foreign Office (11/1939) do Marquina dẫn. Chú thích Mapa 1 (tr.307) ghi 'la situación del campamento, jardines y los espaldones de tiro de la zona apropiada por los ingleses' (OCR lỗi 'zohá'). Trường đua: xem V-A3-01 và V-A3-14. Sân bóng đá, chuồng gia súc, nghĩa trang North Front, Devil's Tower: CHƯA XÁC MINH bằng nguồn tải được.

### Đường băng 1934–1955–nay; lập trường hai phía

**S089** · XÁC MINH · phía: Anh · nhạy cảm:  · as of: 2026-10-17 (ngày đọc) · (gói: V-A3-01)
- Claim (EN): Before the war, flying in Gibraltar used the racecourse on the isthmus: a 1931 air service to Tangier operated from it, and RAF North Front was later built on the site of the old racecourse.
- Trích nguyên văn (en): > Permission was granted to operate an air passenger service from Gibraltar to Tangier in 1931. The service operated from the racecourse but was terminated after only three months due to maintenance difficulties.
- Nguồn: HM Government of Gibraltar, Press Release 199/2018 (2 Apr 2018), Notes to Editors: History of RAF Gibraltar (based on an article by Air Cdre H. Probert) [chinh-thuc] · tr.1, Notes to Editors §1 · https://www.gibraltar.gov.gi/new/sites/default/files/press/2018/Press%20Releases/199-2018.pdf · SHA-256 `eb7a48f36a6bed8d…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Nguồn chính thức HMGoG nhưng tự ghi 'based on an article by Air Cdr H Probert' (sử gia RAF) → bán-thứ-cấp. Câu 'RAF North Front on the site of the old racecourse' cũng có trong cùng văn bản và trong motion Quốc hội 2018.

**S090** · XÁC MINH · phía: Anh · nhạy cảm:  · as of: 2026-10-17 (ngày đọc) · (gói: V-A3-02)
- Claim (EN): A grass airstrip was built between 3 September 1934 and 10 March 1936, for £573.
- Trích nguyên văn (en): > Work began on a grass strip on 3rd September 1934 and was completed 18 months later on 10th March 1936, all for the princely sum of £573.
- Nguồn: HM Government of Gibraltar, Press Release 199/2018 (2 Apr 2018), Notes to Editors: History of RAF Gibraltar (based on an article by Air Cdre H. Probert) [chinh-thuc] · tr.1, Notes to Editors §1 · https://www.gibraltar.gov.gi/new/sites/default/files/press/2018/Press%20Releases/199-2018.pdf · SHA-256 `eb7a48f36a6bed8d…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Khớp với motion Quốc hội Gibraltar 17/05/2018 (không có con số £573). Phía TBN (Marquina 1981) nói đường hạ cánh khẩn cấp 'usándose desde 1935' — lệch 1 năm, không mâu thuẫn bản chất.

**S091** · XÁC MINH · phía: Anh · nhạy cảm:  · as of: 2026-10-17 (ngày đọc) · (gói: V-A3-03)
- Claim (EN): A hard-surface runway was begun in late 1939; land reclamation began towards the end of 1941.
- Trích nguyên văn (en): > Construction of a solid surface runway began in late 1939 and land reclamation commenced towards the end of 1941 along with the construction of the RAF camp at North Front.
- Nguồn: Gibraltar Parliament — Notice of Motion (Chief Minister), Freedom of the City for RAF Gibraltar, 17 May 2018 [chinh-thuc] · tr.1, đoạn NOTES · https://www.parliament.gi/uploads/contents/motions/2018/motion_freedom_of_the_city_raf.pdf · SHA-256 `ad162db22ad76cbd…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Văn bản Quốc hội Gibraltar (nghị quyết do Chief Minister đệ trình). Không trùng C33 (đường băng cắt qua đường bộ 1941) vì đây là mốc khởi công mặt cứng + lấn biển. V5b-1 đã dùng 199/2018 cho 11/1941→07/1943; claim này dùng nguồn khác (motion Parliament) để có 2 nguồn độc lập về hình thức.

**S092** · XÁC MINH · phía: Anh · nhạy cảm:  · as of: 2026-10-17 (ngày đọc) · (gói: V-A3-04)
- Claim (EN): At the end of November 1941 it was decided to extend the runway seaward to a total length of 1,550 yards (about 1,417 m); it was built with stone blasted from the Rock's north face plus spoil from tunnelling, and was ready for use in July 1943.
- Trích nguyên văn (en): > TAKES NOTE that at the end of November 1941 it was decided that the runway should be extended seaward to give a total length of 1550 yards. Construction teams were brought from the UK and they used stone blasted from the north face of the Rock and dumped into the sea along with stone taken from tunnel construction. The extended runway was ready for use in July 1943
- Nguồn: Gibraltar Parliament — Notice of Motion (Chief Minister), Freedom of the City for RAF Gibraltar, 17 May 2018 [chinh-thuc] · tr.1–2, đoạn TAKES NOTE · https://www.parliament.gi/uploads/contents/motions/2018/motion_freedom_of_the_city_raf.pdf · SHA-256 `ad162db22ad76cbd…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: 1550 yd = 1417,3 m (quy đổi của tác giả, 1 yd = 0,9144 m). Đây là chiều dài MỤC TIÊU quyết định 11/1941, không phải số đo nghiệm thu. Con số '1.800 yd vào 07/1943' chỉ thấy trên Wikipedia → không dùng. Vật liệu: đá nổ từ mặt bắc + đá đào hầm (cả hai, không chỉ đá hầm).

**S093** · MÂU THUẪN · phía: Anh · nhạy cảm:  · as of: 2026-10-17 (ngày đọc) · (gói: V-A3-05)
- Claim (EN): In 1955 the runway was extended to 6,000 feet, the length the Gibraltar government calls current.
- Trích nguyên văn (en): > In 1955 the runway was extended to its current length of 6000 feet, a length which supports all current day RAF aircraft apart from Voyager aircraft.
- Nguồn: HM Government of Gibraltar, Press Release 199/2018 (2 Apr 2018), Notes to Editors: History of RAF Gibraltar (based on an article by Air Cdre H. Probert) [chinh-thuc] · tr.2 · https://www.gibraltar.gov.gi/new/sites/default/files/press/2018/Press%20Releases/199-2018.pdf · SHA-256 `eb7a48f36a6bed8d…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: 6000 ft = 1828,8 m. MÂU THUẪN với AIP quân sự hiện hành (1798 m × 45 m, xem claim kế). Nhiều CSDL thương mại ghi 1829 m × 46 m — có lẽ lấy từ con số 6000 ft này. Cho dựng 3D dùng số AIP.

**S094** · XÁC MINH · phía: Anh · nhạy cảm:  · as of: 2026-10-17 (ngày đọc) · (gói: V-A3-06)
- Claim (EN): Today the runway (09/27) measures 1,798 m by 45 m, blacktop, on true bearings 087.5°/267.5°; declared take-off run is 1,666 m (09) / 1,662 m (27) and landing distance 1,528 m.
- Trích nguyên văn (en): > 09 087.50° 1798 x 45
- Nguồn: UK Military AIP (MoD AIDU), AD 2 LXGB Gibraltar (combined; AD 2.12/2.13 page AIRAC 07/25, 10 JUL 25; file created 8 May 2026) [chinh-thuc] · AD 2-LXGB-1-4, mục AD 2.12 và AD 2.13 (AIRAC 07/25, 10 JUL 25) · https://www.aidu.mod.uk/aip/pdf/ad/LXGB-Gibraltar-Combined.pdf · SHA-256 `e5cce511fe147311…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Nguồn chính thức MoD (UK Mil AIP). Bảng AD 2.12: 09 và 27 đều '1798 x 45', 'Blacktop', PCN 65/F/A/W/T; ngưỡng 09 N36 09 03·17 W005 21 29·16; ngưỡng 27 N36 09 05·29 W005 20 28·21; strip 1650 x 150; RESA 92 m; clearway 833 x 150 (09) / 831 x 150 (27). AD 2.13: TORA 1666/1662, TODA 2499/2493, ASDA 1666/1662, LDA 1528 (cả hai). AD 2.14: đèn tiếp cận đơn giản 'extending 300m into the sea' ở cả hai đầu. Trích dẫn rút từ bản -layout (bảng). Lưu ý: AIP (trang AIRAC 06/26) vẫn ghi 'Pedestrian, cycle lane and road crosses Rwy 09 / 27 at mid point' — khác C33 (xe hơi đi hầm từ 2023); cần K kiểm khi dùng.

**S095** · XÁC MINH · phía: TBN · nhạy cảm: Cao — quan điểm chủ quyền TBN (eo đất không nhượng). Trình bày như lập trường, không như sự thật trung lập. · as of: 2026-10-17 (ngày đọc) · (gói: V-A3-07)
- Claim (EN): Spain's position (Spanish academic, 1981): the emergency strip had been used since 1935 with Spain's knowledge; in 1938 Britain lengthened it, and it was later pushed some 500 m out into the bay waters.
- Trích nguyên văn (es): > Existía en esta zona neutral una pista de aterrizaje que había venido usándose desde 1935, con el conocimiento del Gobierno español, para el embarque y entrenamiento de aviones de la fuerza aérea naval basados en portaaviones. En el año 1938, estando España en plena guerra civil, Inglaterra procedió al alargamiento de la pista de aterrizaje, que incluso llegaría a extenderse posteriormente quinientos metros—gracias a la postura española que expondremos—, adentrándose en las aguas donde tradicionalmente habían fondeado los buques británicos.
- Nguồn: Antonio Marquina Barrio, "La pista de aterrizaje de Gibraltar", Revista de Estudios Internacionales vol. 2 núm. 2 (abr–jun 1981), CEPC [hoc-thuat] · tr.308 (PDF tr.4), mục "La pista de aterrizaje" · https://www.cepc.gob.es/sites/default/files/2021-12/34994rei02002051.pdf · SHA-256 `c5e24d09cb641074…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Bài học thuật TBN (Revista de Estudios Internacionales, CEPC 1981) dựa trên hồ sơ Bộ Ngoại giao TBN và Foreign Office. '500 m vào vịnh' là số ước của tác giả TBN — số lấn biển duy nhất tìm được; chưa có nguồn Anh đối chứng. Năm '1938' cũng được Algarbani (Almoraima 2009) nhắc: 'el aeródromo de Gibraltar que comenzó a construirse en 1938'.

**S096** · XÁC MINH · phía: TBN · nhạy cảm: Cao — ngôn từ chủ quyền ("usurpada"). · as of: 2026-10-17 (ngày đọc) · (gói: V-A3-08)
- Claim (EN): On 4 March 1939 Franco's government told its ambassador in London to protest that the works were on 'usurped' national territory.
- Trích nguyên văn (es): > El día 4 de marzo de 1939 el Gobierno español ordenó a su embajador en Londres, el duque de Alba, que señalase que las obras que se realizaban para la ampliación tenían lugar en una porción usurpada del territorio nacional
- Nguồn: Antonio Marquina Barrio, "La pista de aterrizaje de Gibraltar", Revista de Estudios Internacionales vol. 2 núm. 2 (abr–jun 1981), CEPC [hoc-thuat] · tr.308 (PDF tr.4) · https://www.cepc.gob.es/sites/default/files/2021-12/34994rei02002051.pdf · SHA-256 `c5e24d09cb641074…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Tác giả dẫn 'Negociaciones sobre Gibraltar' (Libro Rojo 1967) doc. 26, p.483 — tài liệu chính thức TBN.

**S097** · XÁC MINH · phía: TBN · nhạy cảm: Cao — trích lời người Anh do phía TBN dịch lại sang tiếng TBN; bản gốc tiếng Anh (Daily Telegraph 28/04/1955) CHƯA XÁC MINH. · as of: 2026-10-17 (ngày đọc) · (gói: V-A3-09)
- Claim (EN): A British naval attaché in wartime Madrid, Alan Hillgarth, later admitted the airport sat on 'so-called neutral territory' and that its extension into the bay violated Spanish waters (as quoted by a Spanish scholar).
- Trích nguyên văn (es): > «el aeropuerto está situado en el llamado territorio neutral, que en estricta aplicación d,el espíritu de los Tratados debería haberse respetado. Su prolongación en aguas de la bahía de Algeciras se hizo de tal modo que viola aguas que ni siquiera son neutrales, sino definitivamente españolas»
- Nguồn: Antonio Marquina Barrio, "La pista de aterrizaje de Gibraltar", Revista de Estudios Internacionales vol. 2 núm. 2 (abr–jun 1981), CEPC [hoc-thuat] · tr.308 (PDF tr.4), chú thích 3 (Daily Telegraph, 28/04/1955) · https://www.cepc.gob.es/sites/default/files/2021-12/34994rei02002051.pdf · SHA-256 `c5e24d09cb641074…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Trích nguyên văn đúng như bản OCR (có lỗi 'd,el' và tên in 'Alian Hillgarth' = Alan Hillgarth). Chỉ xác minh rằng Marquina trích như vậy; không xác minh lời gốc. Không dùng làm câu thoại nếu chưa có bản tiếng Anh.

**S098** · XÁC MINH · phía: TBN · nhạy cảm: Trung bình — cho thấy TBN chấp nhận thực tế nhưng giữ lập trường pháp lý. · as of: 2026-10-17 (ngày đọc) · (gói: V-A3-10)
- Claim (EN): In November 1939 Spain's foreign minister Beigbeder told Britain the strip on the neutral zone was a 'fait accompli' like the Rock itself, while Spain maintained it could not be used without violating Spanish territory and waters.
- Trích nguyên văn (es): > El ministro español aseguró que la pista de aterrizaje en la zona neutral era un hecho consumado (fait accompli) como lo había sido la posesión de la Roca, y que el gobierno español no tenía intención de poner en cuestión el derecho británico de utilización; sin embargo, las autoridades españolas, tal como había quedado de manifiesto en anteriores reclamaciones y observaciones, consideraban que la pista no podía ser utilizada sin violar el territorio y las aguas españolas, en base a informes de expertos.
- Nguồn: Antonio Marquina Barrio, "La pista de aterrizaje de Gibraltar", Revista de Estudios Internacionales vol. 2 núm. 2 (abr–jun 1981), CEPC [hoc-thuat] · tr.313 (PDF tr.9), mục "La entrevista Beigbeder-Peterson" · https://www.cepc.gob.es/sites/default/files/2021-12/34994rei02002051.pdf · SHA-256 `c5e24d09cb641074…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Dựa trên biên bản phía Anh (FO 425/416 C19704). Hai mặt: 'fait accompli' + phản đối pháp lý — tốt cho cảnh 'cả hai phía'.

**S099** · XÁC MINH · phía: TBN · nhạy cảm: Trung bình. · as of: 2026-10-17 (ngày đọc) · (gói: V-A3-11)
- Claim (EN): Britain's Foreign Secretary Halifax instructed his ambassador never to call it an 'aerodrome', only a landing strip (per Spanish scholar citing FO papers).
- Trích nguyên văn (es): > En las conversaciones con el ministro no debía nunca utilizar la palabra «aeródromo», sino pista de aterrizaje, evitando con ello dar la impresión de que se estuviese organizando una base aérea.
- Nguồn: Antonio Marquina Barrio, "La pista de aterrizaje de Gibraltar", Revista de Estudios Internacionales vol. 2 núm. 2 (abr–jun 1981), CEPC [hoc-thuat] · tr.312 (PDF tr.8), điểm 5 · https://www.cepc.gob.es/sites/default/files/2021-12/34994rei02002051.pdf · SHA-256 `c5e24d09cb641074…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Tóm lược (tiếng TBN) chỉ thị của Halifax 12/11/1939 (FO 425/416 C18192). Đây là diễn giải của tác giả, không phải văn bản gốc tiếng Anh.

**S100** · XÁC MINH · phía: TBN · nhạy cảm: Cao — lập trường chính thức TBN. · as of: 2026-10-17 (ngày đọc) · (gói: V-A3-12)
- Claim (EN): Spain's foreign ministry today: the isthmus was never ceded, and Spain calls its occupation illegal and does not recognise the fence as a border.
- Trích nguyên văn (es): > Esa es la razón por la que España siempre ha subrayado que la ocupación del istmo es ilegal y contraria al Derecho Internacional y, por tanto, ha reclamado siempre su devolución sin condiciones. España no reconoce la ocupación del istmo ni la verja como frontera.
- Nguồn: Ministerio de Asuntos Exteriores (España), página "Gibraltar" [chinh-thuc] · mục "La historia de Gibraltar" · https://www.exteriores.gob.es/es/PoliticaExterior/Paginas/Gibraltar.aspx · SHA-256 `9054592acb8887ac…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: C30 đã dùng trang này cho phạm vi nhượng của Utrecht; claim này chỉ thêm câu 'ilegal… ni la verja como frontera' (gắn với sân bay trên eo đất). Có thể gộp với C30 nếu K thấy trùng.

**S101** · XÁC MINH · phía: Anh · nhạy cảm: Trung bình — phát ngôn chính phủ Anh. · as of: 2026-10-17 (ngày đọc) · (gói: V-A3-13)
- Claim (EN): The UK government (1991) summarised Spain's claim: Spain accepts Utrecht's cession of town and castle but not British sovereignty over the isthmus.
- Trích nguyên văn (en): > She does not accept our sovereignty over the isthmus which Spain regards as having been usurped over the years. I make no comment on the Spanish claim other than to say that it does not change our right to administer Gibraltar
- Nguồn: UK Hansard, Commons, "Gibraltar", 15 Jul 1991 — Tristan Garel-Jones (Minister of State, FCO) [so-cap] · Commons 15/07/1991, phát biểu Tristan Garel-Jones · https://hansard-api.parliament.uk/debates/debate/1a8e7e14-30c1-4960-9da1-540b2c9d04df.json · SHA-256 `0123d55a7d721041…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Nguồn Hansard qua API chính thức hansard-api.parliament.uk (trang web hansard.parliament.uk trả 403 qua proxy). Đối trọng phía Anh cho các claim TBN.

**S102** · XÁC MINH · phía: Anh · nhạy cảm:  · as of: 2026-10-17 (ngày đọc) · (gói: V-A3-14)
- Claim (EN): The Chief Minister of Gibraltar (2013) said the airfield grew from an old hippodrome using debris from the tunnels.
- Trích nguyên văn (en): > The airfield at Gibraltar was developed at the old time from an old hippodrome, and using much of the debris from creating tunnels inside the rock
- Nguồn: HM Government of Gibraltar, Press Release 713/2013 (9 Oct 2013) — Chief Minister speech, National Press Club [chinh-thuc] · tr.2 · https://www.gibraltar.gov.gi/new/sites/default/files/Press%20archives/Press%20Releases/2013/713-2013.pdf · SHA-256 `0486de8a85025ffc…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Bản ghi lời nói (transcript) — văn phong nói. Dùng làm nguồn thứ hai cho 'trường đua' và 'đá hầm'.

### Tây Ban Nha trong Thế chiến II (Felix)

**S103** · XÁC MINH · phía: TBN · nhạy cảm: Cao — hợp tác quân sự Franco–Đức là chủ đề nhạy cảm ở TBN; tác giả dựa trên Bundesarchiv-Militärarchiv Freiburg. · as of: 2026-10-17 (ngày đọc) · (gói: V-A3-34)
- Claim (EN): Germany's plan to seize Gibraltar, first called 'G', was named 'Felix' by the OKW in the second week of November 1940 and set in motion by Directive 18.
- Trích nguyên văn (es): > Desde el principio la operación de Gibraltar había venido llamándose “G”, pero en la segunda semana de noviembre, una vez desarrollada por el Estado mayor del Ejército, el OKW decidió bautizarla con el nombre clave de “Félix”.
- Nguồn: Alfonso Escuadra, "Del Plan “G” a la Operación “Félix”. La cooperación militar hispano germana en relación con Gibraltar (junio 1940 – enero 1941)", Almoraima 51 (dic. 2019), IECG, pp. 21–34 [hoc-thuat] · tr.31 (PDF tr.11) · https://institutoecg.es/almoraima/index.php/revista/article/download/1418/1370/2664 · SHA-256 `2340fbb91e315303…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Bài học thuật IECG (Almoraima 51, 2019). Cùng trang: 'Este plan entraría en fase de ejecución mediante la Directriz XVIII'. Ngày Directive 18 (12/11/1940) chỉ thấy ở nguồn phổ thông → không ghi ngày cụ thể.

**S104** · XÁC MINH · phía: TBN · nhạy cảm: Cao — tác giả lập luận TBN và Đức hợp tác chặt chẽ ("alianza virtual"); đây là diễn giải học thuật, không phải đồng thuận. · as of: 2026-10-17 (ngày đọc) · (gói: V-A3-35)
- Claim (EN): Felix was suspended immediately after Admiral Canaris failed in mid-December 1940 to get Spain to enter the war quickly.
- Trích nguyên văn (es): > la negativa española a entrar en la guerra a corto plazo se desplace hasta el fracaso de las gestiones protagonizadas por Canaris a mediados de diciembre; un fracaso que determinaría la inmediata suspensión de “Félix”.
- Nguồn: Alfonso Escuadra, "Del Plan “G” a la Operación “Félix”. La cooperación militar hispano germana en relación con Gibraltar (junio 1940 – enero 1941)", Almoraima 51 (dic. 2019), IECG, pp. 21–34 [hoc-thuat] · tr.33 (PDF tr.13), Conclusiones · https://institutoecg.es/almoraima/index.php/revista/article/download/1418/1370/2664 · SHA-256 `2340fbb91e315303…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Đủ cho một dòng thoại: 'Hitler planned to storm the Rock through Spain in 1940 — Operation Felix. Franco would not commit; the plan was shelved.' Tránh khẳng định 'Franco cứu Gibraltar'.

**S105** · XÁC MINH · phía: TBN · nhạy cảm: Trung bình. · as of: 2026-10-17 (ngày đọc) · (gói: V-A3-36)
- Claim (EN): After the fall of France, Spanish authorities kept protesting British violations of Spanish waters, but there is no record of protests over use of the airstrip during the rest of the war (Spanish scholar).
- Trích nguyên văn (es): > Las autoridades españolas siguieron protestando por las continuadas violaciones de las aguas de jurisdicción española, pero no queda constancia de reclamaciones por el uso de la pista
- Nguồn: Antonio Marquina Barrio, "La pista de aterrizaje de Gibraltar", Revista de Estudios Internacionales vol. 2 núm. 2 (abr–jun 1981), CEPC [hoc-thuat] · tr.314 (PDF tr.10) · https://www.cepc.gob.es/sites/default/files/2021-12/34994rei02002051.pdf · SHA-256 `c5e24d09cb641074…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Giải thích vì sao việc lấn biển 1941–43 diễn ra không bị TBN phản đối chính thức (theo Marquina). Cùng trang: 'Más de las tres cuartas partes de la población fue trasladada a Jamaica, las Azores, Madeira o Gran Bretaña' (ghi 'Azores' — có lẽ nhầm, nguồn khác không nhắc Azores).

### Đường hầm Thế chiến II

**S106** · XÁC MINH · phía: Anh · nhạy cảm:  · as of: 2026-10-17 (ngày đọc) · (gói: V-A3-15)
- Claim (EN): Gibraltar's tunnels total around 55 km, more than the length of its surface roads (Gibraltar Museum lecture notice).
- Trích nguyên văn (en): > Despite Gibraltar’s relatively small area of less than 7km2, it has around 55km of tunnels, much more than the total length of its surface road network.
- Nguồn: HM Government of Gibraltar, Press Release 310/2017 (16 May 2017), Gibraltar Museum lecture "The Five Stages of Tunnelling in Gibraltar" [chinh-thuc] · tr.1 · https://www.gibraltar.gov.gi/new/sites/default/files/press/2017/Press%20Releases/310-2017.pdf · SHA-256 `5ec9ec0185baf60e…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Cách đếm: TOÀN BỘ hầm qua 2 thế kỷ (từ thế kỷ 18 đến 1960s), không riêng WWII.

**S107** · MÂU THUẪN · phía: Anh · nhạy cảm:  · as of: 2026-10-17 (ngày đọc) · (gói: V-A3-16)
- Claim (EN): The Gibraltar Nature Reserve also gives some 55 km of tunnels and calls the WWII complex an 'underground city' for a 16,000-strong garrison able to withstand a year-long siege.
- Trích nguyên văn (en): > some 55 kilometres of tunnels honeycombed throughout the Rock. During WWII the epitome of this concept came to fruition when the Royal Engineers and the Canadian Army ventured to create the WWII Tunnels an ‘underground city’ capable of housing a 16,000 strong garrison with all the necessary amenities and provisions capable of withstanding a year long siege.
- Nguồn: Gibraltar Nature Reserve, "Military Tunnels" [chinh-thuc] · đoạn giữa trang "Military Tunnels" · https://naturereserve.gi/?p=1034 · SHA-256 `bfec36b355e74298…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: 55 km khớp 310/2017 (nhưng cùng hệ HMGoG → không hoàn toàn độc lập). Thời gian chịu vây MÂU THUẪN giữa các nguồn: 'a year long siege' (Nature Reserve) / '16 months' (CIM 2018) / 'nearly two years' (Gingell). Sức chứa: 16.000 (3 nguồn) vs 17.000 (hướng dẫn viên Bảo tàng 2026).

**S108** · XÁC MINH · phía: Anh · nhạy cảm:  · as of: 2026-10-17 (ngày đọc) · (gói: V-A3-17)
- Claim (EN): A UK MP told the Commons in 2015 there are 34 miles of tunnels in the Rock, twice its road length.
- Trích nguyên văn (en): > Within the Rock are 34 miles of tunnels—twice the length of the entire road system around the Rock—which were dug with picks by British sappers.
- Nguồn: UK Hansard, Commons, "Gibraltar", 8 Jan 2015 — Bob Stewart MP [so-cap] · Commons 08/01/2015, Bob Stewart · https://hansard-api.parliament.uk/debates/debate/15010857000002.json · SHA-256 `1b8bacbff302b822…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: 34 dặm = 54,7 km → khớp ~55 km. Nguồn độc lập với HMGoG (Hansard Anh), nhưng là lời một nghị sĩ, không phải số đo. 'dug with picks by British sappers' bỏ qua vai trò Canada → không dùng nửa sau.

**S109** · XÁC MINH · phía: Anh · nhạy cảm:  · as of: 2026-10-17 (ngày đọc) · (gói: V-A3-18)
- Claim (EN): A Gibraltar National Museum guide (2026): the system is over 50 km long, of which about 30 km were dug during WWII (1940–43) by British and Canadian engineers.
- Trích nguyên văn (en): > "Now, the tunnel system in Gibraltar is over 50 kilometres long," he said. "The very first tunnel was built in Gibraltar during the Great Siege back in the 1780s, and the last tunnels in Gibraltar were built in the 1960s just to improve road traffic." "But most of those tunnels, 30 kilometres of them, were built during the Second World War."
- Nguồn: Gibraltar Chronicle, M. J. Corrales, 5 Aug 2026 — quoting Gibraltar National Museum guide Phil Smith [bao-tang] · đoạn trích lời Phil Smith · https://www.chronicle.gi/?p=179342 · SHA-256 `64578af911f2d09d…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Lời hướng dẫn viên bảo tàng qua báo — số WWII 30 km là con số duy nhất tìm được cho riêng WWII. Wikipedia nói 'từ 7 dặm lên 25 dặm (40 km)' — không có nguồn gốc tải được → không dùng. Cùng bài: 'excavated around 30 kilometres of tunnels between 1940 and 1943'.

**S110** · XÁC MINH · phía: trung-lap · nhạy cảm:  · as of: 2026-10-17 (ngày đọc) · (gói: V-A3-19)
- Claim (EN): Two Royal Engineer tunnelling companies went to Gibraltar in 1940; a detachment of No. 1 Canadian Tunnelling Company began work on 26 November 1940, and No. 2 Company followed in 1941.
- Trích nguyên văn (en): > Two Royal Engineer Tunnelling Companies were dispatched to Gibraltar in 1940.
- Nguồn: Canadian Military Engineers Association, "Canadian Tunnellers Tackle Gibraltar" [thu-cap] · đoạn 2–3 · https://cmea-agmc.ca/en/node/4345 · SHA-256 `24af7eb0e5b791ed…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Cùng trang: 'This detachment commenced work on 26 November 1940' và 'No. 2 Tunneling Company joined them early in 1941'. Trang tự mâu thuẫn nhẹ (có câu 'arrived in Gibraltar on 12 November 1940'). Số hiệu đại đội RE (170, 178, 180) chỉ có trên Wikipedia → CHƯA XÁC MINH.

**S111** · MÂU THUẪN · phía: trung-lap · nhạy cảm:  · as of: 2026-10-17 (ngày đọc) · (gói: V-A3-20)
- Claim (EN): Canadian tunnellers dug a hospital inside the Rock — largest chamber 200 × 35 ft, 12 ft high — and in two years 234 Canadians removed about 140,000 tons of rock; a quarry also produced fill for the runway.
- Trích nguyên văn (en): > The Canadians worked on excavating a series of wards and tunnels to make a hospital area inside the Rock. The largest chamber was 200' x 35' and 12' high. They also constructed ammunition magazines, oil storage tanks, pillbox fortifications and installed heavy timbering where rock conditions required it. A quarrying operation produced fill to extend the airfield runways. During their two years on The Rock, 234 Canadian men and officers mined and removed about 140,000 tons of solid rock
- Nguồn: Canadian Military Engineers Association, "Canadian Tunnellers Tackle Gibraltar" [thu-cap] · đoạn 4 · https://cmea-agmc.ca/en/node/4345 · SHA-256 `24af7eb0e5b791ed…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Kích thước cho 3D: 200 ft × 35 ft × 12 ft = 61,0 m × 10,7 m × 3,7 m. Số người MÂU THUẪN: CMEA 234 vs CIM 2018 '324 tunnellers' (Gibraltar Key). 140.000 tấn khớp CIM ('140,000 Imperial tons (142,246 metric tonnes)').

**S112** · MÂU THUẪN · phía: trung-lap · nhạy cảm:  · as of: 2026-10-17 (ngày đọc) · (gói: V-A3-21)
- Claim (EN): The central bomb-proof tunnel, the Great North Road, ran for about a mile; the finished network could hold a 16,000-strong garrison with food for 16 months, plus a 200-bed hospital.
- Trích nguyên văn (en): > The central bomb-proof tunnel ran for a mile and was named the Great North Road after a historic highway in the U.K. connecting London to Scotland. Smaller tunnels led off the main thoroughfare. When the tunnel network was finished, it could fit an entire 16,000-strong garrison with food to last 16 months.
- Nguồn: CIM Magazine (Canadian Institute of Mining), Cecilia Keating, "Hard rock mining on the Rock", 5 Nov 2018 [thu-cap] · đoạn 6–7 · https://magazine.cim.org/en/in-search/hard-rock-mining-on-the-rock/ · SHA-256 `f99e7a28ee341c8c…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Tạp chí ngành (thứ cấp). 'a mile' ≈ 1,6 km — số tròn, không phải số đo. '16 months' mâu thuẫn với 'year long siege' và 'nearly two years'. Cùng bài: bệnh viện 'would later house 200 beds'.

**S113** · MÂU THUẪN · phía: Anh · nhạy cảm:  · as of: 2026-10-17 (ngày đọc) · (gói: V-A3-22)
- Claim (EN): The underground city could house 16,000 troops, with hospital, workshops, stores for nearly two years, a power station, a desalination plant and a telephone exchange; most of the excavated rock went to fill North Front for the aerodrome.
- Trích nguyên văn (en): > accommodating 16,000 troops, contain a hospital, workshops, ammunitions, victuals stores with capacity to maintain an entire garrison for nearly two years, a power station, a desalination plant and a telephone exchange. Most of the pieces of rock dug out from the drilling of the tunnels were used later to fill the terrain at the North Front for the construction of a military aerodrome.
- Nguồn: Joe Gingell, "Between the Devil and the Deep Blue Sea" (2nd ed., ISBN 978-1-919663-62-3), hosted by Gibraltar National Archives [thu-cap] · tr. sách 296 (PDF tr.317), Chương 7 · https://nationalarchives.gi/Images/Evacuation/Book/EvacBook2.pdf · SHA-256 `724499bb9cffa69e…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Sách tư nhân (Joe Gingell 2018) do Gibraltar National Archives lưu trữ → thứ cấp. Phần đầu câu ('This underground city was capable of') bị lỗi mã font trong PDF nên trích từ 'accommodating'. Liệt kê nhà máy điện + chưng cất nước — dùng cho cảnh 3D. 'nearly two years' mâu thuẫn nguồn khác.

### Sơ tán dân thường 1940

**S114** · XÁC MINH · phía: Anh · nhạy cảm:  · as of: 2026-10-17 (ngày đọc) · (gói: V-A3-23)
- Claim (EN): Evacuation began on 22 May 1940 to French Morocco; after France fell the evacuees were brought back and sent on to London, Jamaica, Madeira and later Northern Ireland.
- Trích nguyên văn (en): > On 22 May 1940, women, children, the elderly and the infirm were evacuated to French Morocco. After the fall of France they were brought to Gibraltar and then evacuated onwards to London, Jamaica, Madeira and later Northern Ireland.
- Nguồn: HM Government of Gibraltar, Press Release 85/2015 (16 Feb 2015) [chinh-thuc] · tr.1, đoạn 2 · https://www.gibraltar.gov.gi/new/sites/default/files/press/2015/Press%20Releases/85-2015.pdf · SHA-256 `40fb7d78d414bd03…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Nguồn chính thức HMGoG.

**S115** · XÁC MINH · phía: Anh · nhạy cảm:  · as of: 2026-10-17 (ngày đọc) · (gói: V-A3-24)
- Claim (EN): Between 22 May and 24 June 1940 one ship, the Mohamed-Ali-el-Kebir, carried 12,044 evacuees to Casablanca in twelve trips.
- Trích nguyên văn (en): > As from the 22nd May to the 24th June 1940, the Mohamed-Ali-el- Kebir made twelve trips to Casablanca carrying a total of 12,044 evacuees.
- Nguồn: Joe Gingell, "Between the Devil and the Deep Blue Sea" (2nd ed., ISBN 978-1-919663-62-3), hosted by Gibraltar National Archives [thu-cap] · tr. sách 3 (PDF tr.24), Chương 1 · https://nationalarchives.gi/Images/Evacuation/Book/EvacBook2.pdf · SHA-256 `724499bb9cffa69e…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Thứ cấp (sách lưu tại GNA). Chỉ là số của một tàu; còn 1.038 người tự đi sang Casablanca (cùng sách) → tổng ~13.000, khớp câu sách trích FO 'the 13,000 Gibraltarians who had been evacuated from Gibraltar to French Morocco'.

**S116** · XÁC MINH · phía: Anh · nhạy cảm:  · as of: 2026-10-17 (ngày đọc) · (gói: V-A3-25)
- Claim (EN): In August 1940 the UK government said it had housed about 11,000 refugees from Gibraltar in London at very short notice.
- Trích nguyên văn (en): > My Lords, it was necessary at very short notice to find accommodation for about 11,000 refugees from Gibraltar, of whom the majority were women and children, unable in many cases to speak English.
- Nguồn: UK Hansard, Lords, "Accommodation for Refugees from Gibraltar", 13 Aug 1940 — Lord Tryon (First Commissioner of Works) [so-cap] · Lords 13/08/1940, Lord Tryon · https://hansard-api.parliament.uk/debates/debate/75be6cfb-7424-4392-a9ea-400cfaa04de4.json · SHA-256 `1f99cd905a722a7a…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Nguồn sơ cấp (Hansard, qua API chính thức). Mốc giữa đợt: sau đó còn 1.786 người tới UK ngày 20/08/1940 (Gingell) → tổng London 10.816.

**S117** · XÁC MINH · phía: Anh · nhạy cảm:  · as of: 2026-10-17 (ngày đọc) · (gói: V-A3-26)
- Claim (EN): By 20 August 1940, 10,816 civilians had been evacuated to London and nearly 2,000 to Madeira.
- Trích nguyên văn (en): > With this last group of evacuees a total of 10,816 civilians had been evacuated to London and nearly 2,000 to Madeira.
- Nguồn: Joe Gingell, "Between the Devil and the Deep Blue Sea" (2nd ed., ISBN 978-1-919663-62-3), hosted by Gibraltar National Archives [thu-cap] · tr. sách 12 (PDF tr.33) · https://nationalarchives.gi/Images/Evacuation/Book/EvacBook2.pdf · SHA-256 `724499bb9cffa69e…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Thứ cấp, nhưng khớp Hansard (~11.000 ở London) và HMGoG 315/2019 ('Some 2000… went to… Madeira').

**S118** · XÁC MINH · phía: Anh · nhạy cảm:  · as of: 2026-10-17 (ngày đọc) · (gói: V-A3-27)
- Claim (EN): Jamaica received 1,093 evacuees on the Neuralia (9 Oct 1940) and 393 on the Thysville (31 Oct 1940).
- Trích nguyên văn (en): > the Neuralia left Gibraltar for Jamaica with 1,093
- Nguồn: Joe Gingell, "Between the Devil and the Deep Blue Sea" (2nd ed., ISBN 978-1-919663-62-3), hosted by Gibraltar National Archives [thu-cap] · tr. sách 13 (PDF tr.34) · https://nationalarchives.gi/Images/Evacuation/Book/EvacBook2.pdf · SHA-256 `724499bb9cffa69e…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Văn bản PDF bị chen cột: '…for Jamaica with 1,093 A further 393 evacuees on 9th October 1940. evacuees left also on the Thysville for Jamaica on the 31st October 1940.' → đọc là 1.093 (Neuralia, 9/10) + 393 (Thysville, 31/10) = 1.486 ≈ '1,500' mà sách nêu ở chương Jamaica. Chỉ trích phần không bị chen.

**S119** · MÂU THUẪN · phía: Anh · nhạy cảm:  · as of: 2026-10-17 (ngày đọc) · (gói: V-A3-28)
- Claim (EN): A 2 May 1941 Colonial Office memorandum put the total at some 14,000: 10,500 to the UK, 2,000 to Madeira, the balance to Jamaica.
- Trích nguyên văn (en): > On the 2nd May 1941 a memorandum was submitted by the Secretary of State for the Colonies to the War Office which said that some 14,000 civilians had been evacuated from Gibraltar, 10,500 to the UK, 2,000 to Madeira and the balance to Jamaica.
- Nguồn: Joe Gingell, "Between the Devil and the Deep Blue Sea" (2nd ed., ISBN 978-1-919663-62-3), hosted by Gibraltar National Archives [thu-cap] · tr. sách 17 (PDF tr.38) · https://nationalarchives.gi/Images/Evacuation/Book/EvacBook2.pdf · SHA-256 `724499bb9cffa69e…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Tổng MÂU THUẪN theo cách đếm: ~13.000 (sang Ma-rốc, 05–06/1940) / ~14.000 (bản ghi nhớ 05/1941, tính đến lúc đó) / ~16.000 (HMGoG 315/2019 và Gingell — tổng cả chiến tranh, gồm đợt 1941). Đề xuất lời thoại: 'some 16,000 over the war, most within weeks in 1940' hoặc nêu rõ mốc.

**S120** · XÁC MINH · phía: Anh · nhạy cảm:  · as of: 2026-10-17 (ngày đọc) · (gói: V-A3-29)
- Claim (EN): The Gibraltar government puts the total at 16,000 evacuees, some 2,000 of whom went to Madeira.
- Trích nguyên văn (en): > Some 2000 of the 16,000 evacuees went to the Portuguese Atlantic island of Madeira.
- Nguồn: HM Government of Gibraltar, Press Release 315/2019 (26 Apr 2019) [chinh-thuc] · đoạn 2 · https://www.gibraltar.gov.gi/press-releases/government-pays-tribute-to-evacuation-generation-3152019-4885 · SHA-256 `3122a67d7cb01b74…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Chính thức HMGoG.

**S121** · XÁC MINH · phía: Anh · nhạy cảm:  · as of: 2026-10-17 (ngày đọc) · (gói: V-A3-30)
- Claim (EN): By December 1944 only about half of those evacuated in 1940 had returned, the Colonial Secretary told the Commons.
- Trích nguyên văn (en): > About half of those who left the Colony in 1940, when the evacuation was originally ordered, have now gone back.
- Nguồn: UK Hansard, Commons, "Gibraltar Evacuees (Northern Ireland)", 13 Dec 1944 — Colonel Oliver Stanley (Colonial Secretary) [so-cap] · Commons 13/12/1944, Col. Oliver Stanley · https://hansard-api.parliament.uk/debates/debate/c09ebbe8-5db0-4f12-84b4-4c215eea0e4e.json · SHA-256 `54d11187c2463412…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Sơ cấp (Hansard). Hữu ích cho phần kết của đoạn sơ tán.

### Căn cứ Thế chiến II (Torch)

**S122** · XÁC MINH · phía: Anh · nhạy cảm:  · as of: 2026-10-17 (ngày đọc) · (gói: V-A3-32)
- Claim (EN): Eisenhower, overall commander of Operation Torch, based his headquarters in tunnels deep inside the Rock; the invasion of North Africa was planned from Gibraltar in November 1942.
- Trích nguyên văn (en): > General Eisenhower, who was the overall commander of Operation Torch, based his headquarters in tunnels deep inside the actual Rock itself.
- Nguồn: HM Government of Gibraltar, Press Release 838/2022 (9 Nov 2022) [chinh-thuc] · đoạn 1–3 · https://www.gibraltar.gov.gi/press-releases/exhibition-opened-to-mark-80-years-since-operation-torch-8382022-8438 · SHA-256 `29f37ef291504b9c…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Chính thức HMGoG. Cùng thông cáo: 'Operation Torch… which was planned from Gibraltar in November 1942'. Câu Eisenhower gốc từ 'Crusade in Europe' CHƯA XÁC MINH (không tải được văn bản).

**S123** · XÁC MINH · phía: Anh · nhạy cảm:  · as of: 2026-10-17 (ngày đọc) · (gói: V-A3-33)
- Claim (EN): On the night of 7/8 November 1942 no fewer than 650 aircraft were parked along both sides of the North Front runway for Operation Torch.
- Trích nguyên văn (en): > the night of 7/8 November 1942 when no fewer than 650 aircraft of many types were parked along both sides of the runway in readiness for operation TORCH, the Anglo-American invasion of North Africa.
- Nguồn: Gibraltar Parliament — Notice of Motion (Chief Minister), Freedom of the City for RAF Gibraltar, 17 May 2018 [chinh-thuc] · tr.2 · https://www.parliament.gi/uploads/contents/motions/2018/motion_freedom_of_the_city_raf.pdf · SHA-256 `ad162db22ad76cbd…`
- Kiểm độc lập: khớp nguyên khối
- Ghi chú: Dùng cho cảnh 3D 'đường băng chật máy bay'. HMGoG 199/2018 có cùng câu + 'Churchill called it, ‘Gibraltar’s greatest contribution to the War.’' (lời Churchill chưa đối chiếu hồi ký gốc).

## 2. Chưa tìm được / nguồn bị chặn

- (a1) Nguyên văn sách gốc Fa & Finlayson, The Fortifications of Gibraltar 1068–1945 (Osprey 2006), tr. 9 — nguồn hiện đại của danh sách 14 cuộc vây; chỉ thấy qua Wikipedia.
- (a1) Jackson, The Rock of the Gibraltarians (1987), tr. 317 — cụm "fifteenth siege" (1969–85).
- (a1) Hills, Rock of Contention (1974), tr. 95 — "only five sieges resulted in a change of rule".
- (a1) Nguồn chính thức phía Anh nêu cơ sở pháp lý "prescription"/chiếm hữu lâu dài với eo đất (FCO OT13.pdf, FAC 1998–99 HC 366) — publications.parliament.uk 403, web.archive.org bị chặn qua proxy.
- (a1) Nguồn sơ cấp/học thuật cho lán dịch sốt vàng trên vùng trung lập năm 1815 và yêu cầu năm 1854 của TBN (chỉ có Wikipedia; García Sanz nêu 1845, 1854).
- (a1) Nguồn phía Anh (Hansard 1908–1910, Colonial Office) về việc dựng hàng rào 1908–1909 và lý do; năm 1909 vs 1910 chưa đối chiếu nguồn Anh.
- (a1) Nguồn giải thích nguyên văn phần "de la Concepción" trong tên La Línea de la Concepción, và ngày cụ thể tháng 7/1870.
- (a1) Bản gốc Burnet, History of His Own Time — chỉ có trích lại qua Sayer.
- (a1) Văn bản Latinh gốc của Điều X (chỉ thấy cụm Latinh trích trong Elcano).
- (a1) commons.wikimedia.org (429), visitgibraltar.gi (403) — không truy cập được.
- (a2) Hiệp ước Aranjuez (12/4/1779) – không có nguồn sơ cấp/ học thuật tải được; CHƯA XÁC MINH
- (a2) Văn bản Hiệp ước Versailles Anh–TBN 3/9/1783 (Wellcome Collection có bản số hoá, chưa tải) – dùng Drinkwater/Montero thay
- (a2) Mémoire của d'Arçon (Cadix 1783) – không có trên archive.org; dùng 'Conseil de guerre privé' 1785 thay
- (a2) dbe.rah.es tiểu sử Álvarez de Sotomayor / Crillon – không tìm được URL
- (a2) publicaciones.defensa.gob.es (Revista General de Marina rgm_151.pdf) – connection reset ×2
- (a2) visitgibraltar.gi & ministryforheritage.gi – 403 Forbidden; web.archive.org – kết nối bị đóng → chiều dài Great Siege Tunnels hiện nay và con số 370 ft/18 người CHƯA XÁC MINH
- (a2) Bảng thương vong Gaceta de Madrid (719 người trên khẩu đội nổi) – chỉ là ảnh trên todoababor; CHƯA XÁC MINH
- (a2) Ngày tuyên chiến TBN (16/6/1779) – CHƯA XÁC MINH
- (a2) Số tàu chiến tuyến theo nguồn TBN; tổng 1.473 thương vong Grand Assault (Chartrand) – CHƯA XÁC MINH
- (a2) Số pháo hư hỏng trong vây: '53' (bản 1905) vs '33' (OCR bản 1785) – chưa chắc
- (a3) Chiều dài 1.150 yd (04/1942) và 1.800 yd (07/1943): chỉ có trên Wikipedia — không có nguồn tải được.
- (a3) Diện tích lấn biển (ha) cho đường băng: không tìm được.
- (a3) RAF Air Historical Branch "Flying from the Rock: the story of aviation at Gibraltar 1901–1945" (raf.mod.uk) — trả 403 qua proxy (curl và WebFetch). Nguồn ưu tiên để thử lại.
- (a3) Trang di sản ministryforheritage.gi (WWII tunnel complex, Great North Road, Calpe Hole, Hays Level) và visitgibraltar.gi — 403 qua proxy.
- (a3) Số hiệu đại đội Royal Engineers (170/178/180 Tunnelling Coy) và ngày khởi công Great North Road — chỉ Wikipedia.
- (a3) Tiết diện hầm điển hình (rộng × cao) cho mô hình 3D — không có nguồn.
- (a3) Force H (thành lập ở Gibraltar 06/1940, Somerville) — không có nguồn chính thức tải được (chỉ Wikipedia/blog); Hansard 1940–46 không có kết quả.
- (a3) Câu gốc của Eisenhower (Crusade in Europe) về sở chỉ huy trong hầm — chưa có văn bản tải được.
- (a3) Operation Tracer (Stay Behind Cave) — không tìm.
- (a3) Water catchments mặt đông (1903→1961, 10→34 mẫu Anh): chỉ thấy ở nguồn du lịch/Wikipedia; trang visitgibraltar.gi 403.
- (a3) Sân bóng đá, chuồng gia súc, nghĩa trang North Front, Devil's Tower trên eo đất trước sân bay — chưa có nguồn tải được (chỉ có: trường đua, trại lính, vườn, trường bắn, khu giải trí).
- (a3) Lời gốc tiếng Anh của Alan Hillgarth (Daily Telegraph 28/04/1955).
- (a3) Văn bản Directive 18 (12/11/1940) từ nguồn lưu trữ/học thuật — chỉ thấy bản dịch trên trang phổ thông; Revista General de Marina 2015 (armada.defensa.gob.es) trả 403.

## 3. Nguồn đã tải (SHA-256; tệp ngoài git)

| URL | SHA-256 | Ghi chú |
|---|---|---|
| https://en.wikipedia.org/wiki/List_of_sieges_of_Gibraltar | `30c08b13d96c97272f156f7f0243745800f9201bc9b165cf8def34c852dba8e6` | Tertiary; dùng để tìm nguồn (Fa & Finlayson, Hills, Jackson) |
| https://visitgibraltar.gi/history-1704-1911 | `889403e5cfbb7981f7a26aced0d7492524e5397d6996f7fccd67562d2a4a71a3` | HTTP 403 — không dùng |
| https://www.gibmuseum.gi/ | `3f62e0d9e7bbc51d8721099f5822c38a94fcbe8f9fa79d0d28bedfd0b935fe5b` | Trang chủ bảo tàng — chỉ để tìm link |
| https://archive.org/download/historyofgibralt00sayeuoft/historyofgibralt00sayeuoft_djvu.txt | `3dd2e42aa4bab8f62f2b83c9d9ae7c8761915cce89e74b10f4ac8781a31c127d` | Sayer 1862 full text (OCR) |
| https://archive.org/download/historyofgibralt00step/historyofgibralt00step_djvu.txt | `4da9d1c355e465161a409aaa56183c800c26c37cb189726e221532cf4ea7c7b8` | [Stephens] 1870 full text (OCR) |
| https://archive.org/download/gibraltaritssieg00londuoft/gibraltaritssieg00londuoft_djvu.txt | `293791a72423b0e3756f40518a2b6f585d1b66e9eaa06c3b2c78b13785d8aa95` | Gibraltar and its sieges (1900) — không dùng trích |
| https://archive.org/download/historiadegibra00montgoog/historiadegibra00montgoog_djvu.txt | `a9b8f6b07ee075c9f5a7c79b47925ddb3c539e6feb31ebb0ca621459e31abfe5` | Montero 1860 full text (OCR nhiễu) |
| https://archive.org/download/historyoflatesie00driniala/historyoflatesie00driniala_djvu.txt | `9e93ecf12d78a8c4c278708706bd249fe086983fb28f82eb880f5c7795043962` | HTTP 500 (Drinkwater) — không dùng |
| https://archive.org/download/collectionoftrea02greaiala/collectionoftrea02greaiala_djvu.txt | `1ee7fe1376174aba388f55a7f3dc925688cda7f97f4de12664ba412ce5566e46` | Chalmers 1790 vol. II — Art. X |
| https://archive.org/download/collectionoftrea01greaiala/collectionoftrea01greaiala_djvu.txt | `724f6390f31e008470e0bf94ed2f9da59e601f707ccbfb7ab009c0337c8f10c9` | Chalmers 1790 vol. I — không chứa Art. X |
| https://archive.org/download/bim_eighteenth-century_a-collection-of-all-the-_1785_2/bim_eighteenth-century_a-collection-of-all-the-_1785_2_djvu.txt | `121bd2712b4f45db112f3a7d0ab50dfb5a830a6b9d9b04f13a148dd6ecc1ffef` | Jenkinson 1785 vol. II — Art. X (bản "Queen's special Command") |
| https://archive.org/download/collectionofallt01grea/collectionofallt01grea_djvu.txt | `89c7a088d994275d28769bc3ae7f6a386c806e71b6ca0833c4ad377f43b567d4` | 1772 Collection vol. I — có câu "without any territorial jurisdiction" (đối chiếu) |
| https://archive.org/download/tratadosconveni00cantgoog/tratadosconveni00cantgoog_djvu.txt | `957f850035749073881e4eac44a98b02112bc548c6741f307e1b51691bd60d25` | Cantillo 1843 — Art. 10 tiếng TBN (OCR nhiễu) |
| https://archive.org/download/garcia-sanz-c.-historia-de-gibraltar-madrid-2022./Garc%C3%ADa%20Sanz%2C%20C.-Historia%20de%20Gibraltar%2C%20Madrid%2C%202022.%20180%20pp._djvu.txt | `2357d695b5be8c3fa4450b2d866dc6fb4fc9376ca3522dd4fe4d6964d63386f8` | García Sanz 2022 (Catarata) — bản người dùng tải lên archive.org; sách còn bản quyền |
| https://archive.org/download/bub_gb_Dc0NAAAAQAAJ/bub_gb_Dc0NAAAAQAAJ_djvu.txt | `2d6ee3ff7926a6999534dd1c1446efb80faf856d4bf0476d3b9eb89494f5ac61` | López de Ayala 1782 Historia de Gibraltar — tải nhưng chưa trích |
| https://media.realinstitutoelcano.org/wp-content/uploads/2021/11/ari19-2013-ortega-gibraltar-tratado-de-utrecht.pdf | `528385f5ce88cde1bd7ce754edf4e9edd8e16b0c6a1ea13b9b721bc5da635609` | Real Instituto Elcano ARI 19/2013 |
| https://schools.gibraltarheritagetrust.org.gi/siege/further.html | `ccdd7817266fecabd3c816f695467d1516ca085633e24fe6e15f9565d07ae295` | GHT schools — toàn văn Art. X (có lỗi chép) |
| https://schools.gibraltarheritagetrust.org.gi/siege/ | `ab9440a2dd591278176e78841fecfb42238f73c00a95437d112ec402f72f26c4` | GHT schools index |
| https://infogibraltar.com/wp-content/uploads/2020/06/130705%20500%20Acto%20conmemorativo%20del%20Tratado%20de%20Utrecht%20-%20s%C3%A1bado%2013%20de%20julio.pdf | `c1aac1c21a5a958790339167c4f033bac5c210374ca2d0bebf6e58d0e061bda8` | HMGoG press release 2013 |
| https://schools.gibraltarheritagetrust.org.gi/siege/chapter-01.html | `db3f6f128a18257b5aa2c734ebc1deb128723e0ec2242486b80feec022524471` | GHT schools ch. 1 (có lỗi) |
| https://exteriores.gob.es/es/PoliticaExterior/Paginas/Gibraltar.aspx | `6d9ac371d4f7dd3eedd5a3a2aef530378e1f5ad12b1b7b26ae16c362937fa5b9` | MAEC España |
| https://en.wikipedia.org/wiki/Disputed_status_of_the_isthmus_between_Gibraltar_and_Spain | `e36eb22855a61109ac95835ca366eb21d68bbe97edd121b69e86c0b459ff2f17` | Tertiary — chỉ tìm nguồn |
| https://publications.parliament.uk/pa/cm199899/cmselect/cmfaff/366/36616.htm | `e4db3003f476d5d910b60f5b1d423bc2fc755bab7fa385ae8d70777bb1a146f1` | publications.parliament.uk 403 (Cloudflare) — không dùng |
| https://hansard-api.parliament.uk/search/contributions/Spoken.json?queryParameters.searchTerm=isthmus%20Gibraltar%20sovereignty&queryParameters.take=15 | `b17cacef25fcfe5ccf4d0bb5e9c2ed76b075186b7b0a1d2e1faaf73ded359202` | Hansard API search JSON (chứa phát biểu Lidington 14/10/2015) |
| https://www.gibmuseum.gi/our-history/brief-history-of-gibraltar | `8d5ce1f1db2ba73fa5859cb217ce8e51dce45bcdcc4a261616a574e483d3d26f` | Gibraltar National Museum |
| https://www.gibmuseum.gi/our-history/military-history/fortifications-of-gibraltar | `1f07ff65b93462b6b51d840b0f35125ac0b155007111df261d27e93a31cba262` | Gibraltar National Museum |
| https://institutoecg.es/wp-content/uploads/2025/08/06_linea-contravalacion.pdf | `cdc8a2e2165d4ecec131a377697b3cf1442c22655717a3068a2178c48d83ea31` | IECG guía vol. 6 (2022) |
| https://institutoecg.es/almoraima/index.php/revista/article/download/1446/1397/2718 | `a22508eab727663f1302fcf2f5a88a79f089a911164b329d128955f90e0c89ed` | Gómez Nadal, asedio 1727, Almoraima 52 — đọc, chưa trích |
| https://institutoecg.es/almoraima/index.php/revista/article/download/1339/1297/2522 | `471599817786944c8b057db6f5cee7cd9f37cc42972258b3acce15d9da1a16d3` | Gómez Nadal 2018, Almoraima 48 |
| https://institutoecg.es/almoraima/index.php/revista/article/download/1429/1380/2684 | `fe55929644c1d07e0cc204ed84f3fd8d303fee4bd91dbf03a26b0255faec2917` | Moreno Martín, Almoraima 51 (La Línea 1870) |
| https://institutoecg.es/almoraima/index.php/revista/article/download/909/874/1692 | `fba6f8cf689464092a7832677f9ab944a228a2b5fcfbb450e7ef19b1212199e8` | Escuadra Sánchez 2007, Almoraima 34 |
| https://www.chronicle.gi/goodbye-frontier/ | `eeda2bf333367f2403fc5f252923be522019f3d3ab8baf84b922378ebc5b1d4e` | Gibraltar Chronicle — bài bình luận/hư cấu, KHÔNG dùng |
| https://archive.org/download/historysiegegibr00drin/historysiegegibr00drin_djvu.txt | `9a0c3c3e45f39e2fdbb46de1b92aef6d61d1d8b5100e170d4dcf60c86eb42709` | Drinkwater 1905 |
| https://archive.org/download/historyoflatesie00driniala/historyoflatesie00driniala_djvu.txt | `7576bb8fb645db341cbf981383d7d41efae91fce1c9991737e21be4d04565212` | Drinkwater Dublin 1786 |
| https://archive.org/download/bim_eighteenth-century_a-history-of-the-late-si_drinkwater-john_1785/bim_eighteenth-century_a-history-of-the-late-si_drinkwater-john_1785_djvu.txt | `d55e8ebfdb7ba5c6138eb45946f550a5e510230d20850e35524ccee66058027b` | Drinkwater London 1785 (đối chiếu) |
| https://archive.org/download/ahistorysiegegi00dringoog/ahistorysiegegi00dringoog_djvu.txt | `3c23dd075ee1934f14d7a05a92f7e73952c17d1693dbf0caabf19ffd38539e5c` | Drinkwater 1839 (đối chiếu) |
| https://archive.org/download/in.ernet.dli.2015.109526/2015.109526.A-History-Of-The-Siege-Of-Gibraltar1779-1783_djvu.txt | `863e727fbd2ac7e2fb7a7e0f64341987aefc18fa109dd67f185fed90dbd8cea0` | Drinkwater (DLI, OCR kém) |
| https://archive.org/download/ajournalsiegegi00spilgoog/ajournalsiegegi00spilgoog_djvu.txt | `f6c2f3a940cde7ac88eb6745421b458f1f8c764c4a8affef42a784c54699dc1f` | Spilsbury journal (1908 ed.) |
| https://archive.org/download/acircumstantial00ancegoog/acircumstantial00ancegoog_djvu.txt | `67d61d0aced585978cd08b34717ca985699b3dc7e32d01014f974d1fe488b526` | Ancell journal 1784 |
| https://archive.org/download/bub_gb_4_AqUai2tkIC/bub_gb_4_AqUai2tkIC_djvu.txt | `d99126f25d1c838e4866e7824bb1a485478bac471347093476df2161cb7d6187` | Montero 1860 |
| https://archive.org/download/bub_gb_Lx5oLGPGvfgC/bub_gb_Lx5oLGPGvfgC_djvu.txt | `8e958846266e06bde890335e43188d229b8460c3b7e1fc78b0406a65ac2b18b2` | Conseil de guerre privé 1785 |
| http://www.todoababor.es/datos_docum/bajas-flotantes.html | `de928d198e9d0318069990d849f4bc0f652eb12544e75aadb2da2965db3db8b0` | Todo a Babor – bảng khẩu đội nổi (bảng thương vong là ảnh) |
| https://en.wikipedia.org/w/index.php?title=Great_Siege_of_Gibraltar&action=raw | `0d2a19b8166ae84650658222626e0bf4649043aabb8c63cf1902b81a8048d036` | Wikipedia (định vị nguồn) |
| https://en.wikipedia.org/w/index.php?title=Great_Siege_Tunnels&action=raw | `6b8fee6d7c803949c0595e03f6ae58b6bb080391b4e8d5a797da357aa93e5eda` | Wikipedia (định vị nguồn) |
| https://en.wikipedia.org/w/index.php?title=Henry_Ince&action=raw | `c14a47cff2c4d8d2579f5361823f629b3a48d865391f67c8113f76dcd9a1e40a` | Wikipedia (định vị nguồn) |
| https://cmea-agmc.ca/en/node/4345 | `24af7eb0e5b791edf6edefe7b971de8c0a338a5b42e2db699f10846960013b89` |  |
| https://hansard-api.parliament.uk/debates/debate/15010857000002.json | `1b8bacbff302b822c924e5bb5632a80e486ede28b1151da6e81a7226d54f8c57` |  |
| https://hansard-api.parliament.uk/debates/debate/1a8e7e14-30c1-4960-9da1-540b2c9d04df.json | `0123d55a7d72104188d2c2236edad09d026c491bd7a63f658c26c95c8aa1168b` |  |
| https://hansard-api.parliament.uk/debates/debate/75be6cfb-7424-4392-a9ea-400cfaa04de4.json | `1f99cd905a722a7a2d1aae168767978cf60446707a579901729df55910ed3303` |  |
| https://hansard-api.parliament.uk/debates/debate/c09ebbe8-5db0-4f12-84b4-4c215eea0e4e.json | `54d11187c2463412ce880b420d7d61fc56aeb68ad112131a2b35e927a5694049` |  |
| https://institutoecg.es/almoraima/index.php/revista/article/download/1418/1370/2664 | `2340fbb91e315303b731b225fa7df2ad371e46f08bae04cd659ddd03d8368ff0` |  |
| https://magazine.cim.org/en/in-search/hard-rock-mining-on-the-rock/ | `f99e7a28ee341c8c795c020ce52bbfad2c690794c49e6ee5f6d3d85e9b21b953` |  |
| https://nationalarchives.gi/Images/Evacuation/Book/EvacBook2.pdf | `724499bb9cffa69efdf76e171d0360d4d618cf9c4a760ad45e477aeca841cfff` |  |
| https://naturereserve.gi/?p=1034 | `bfec36b355e742986a7da26da3b97d6d5a2d56685ad7bcc29e5a3bc8eb011f7c` |  |
| https://www.aidu.mod.uk/aip/pdf/ad/LXGB-Gibraltar-Combined.pdf | `e5cce511fe147311f1e55d5b3bb2b6c259cdddcccc98596160525babd10d2f6f` |  |
| https://www.cepc.gob.es/sites/default/files/2021-12/34994rei02002051.pdf | `c5e24d09cb641074063ab36a878130d91191262524430a7eae8e70a04c4a65d7` |  |
| https://www.chronicle.gi/?p=179342 | `64578af911f2d09d47473f618f19ecbfa084fcab75c3e8b1496b07b37b439fcb` |  |
| https://www.exteriores.gob.es/es/PoliticaExterior/Paginas/Gibraltar.aspx | `9054592acb8887acafbd18c5c482ac753a018f12781ffac650f8aea66e7b652c` |  |
| https://www.gibraltar.gov.gi/new/sites/default/files/Press%20archives/Press%20Releases/2013/713-2013.pdf | `0486de8a85025ffcc3c97c0d4e34e09974221514d7ad032596b29231a705fae0` |  |
| https://www.gibraltar.gov.gi/new/sites/default/files/press/2015/Press%20Releases/85-2015.pdf | `40fb7d78d414bd03f22a7cb8939912bf1d1f04832cb54b385218c3410e4ad381` |  |
| https://www.gibraltar.gov.gi/new/sites/default/files/press/2017/Press%20Releases/310-2017.pdf | `5ec9ec0185baf60e926b29c0b385d3260921f382449efef01ba74cdf50de454a` |  |
| https://www.gibraltar.gov.gi/new/sites/default/files/press/2018/Press%20Releases/199-2018.pdf | `eb7a48f36a6bed8d442e04d3e1cb1b9ef7b76e6a2d3659f4f023dd1461c81cb0` |  |
| https://www.gibraltar.gov.gi/press-releases/exhibition-opened-to-mark-80-years-since-operation-torch-8382022-8438 | `29f37ef291504b9c3826f83e8ddb9ba1ba02e8ddc2b90f1679006f586a344079` |  |
| https://www.gibraltar.gov.gi/press-releases/government-pays-tribute-to-evacuation-generation-3152019-4885 | `3122a67d7cb01b74b74cc0ce8a2b1d874922156df58cd3b5fb82c9b1b56a8194` |  |
| https://www.parliament.gi/uploads/contents/motions/2018/motion_freedom_of_the_city_raf.pdf | `ad162db22ad76cbd98e4083cef83c0d043e8de1b09285e581e1c19397900cc31` |  |
