# NGUỒN KÍCH THƯỚC CÔNG TRÌNH BIỂU TƯỢNG — LOOK-T4-V2 (đọc 23/10/2026)

Mã dựng: `scripts/k2ldn/cong_trinh_v2.py` (gọi qua `scripts/k2ldn/hinh_hoc_v2.py`). Bậc theo Kinh thánh §12.2. Không AI ở lớp này.
Bản sao văn bản (ngoài git, tải lại được bằng URL dưới; SHA-256 ghi để kiểm):
- Gutenberg #48491 *Views of St. Paul's Cathedral, London* (bản .txt, cập nhật 24/10/2024 theo đầu tệp) — `https://www.gutenberg.org/cache/epub/48491/pg48491.txt`, SHA-256 `c2fbc2440a796712bfa9cd43b4f6577e605ad6be15dd6f0ef26a8c10aa78929f`. Phạm vi công cộng (Mỹ); ghi chú Gutenberg.
- Gutenberg #60008 *London and Its Environs Described, vol. 5 (of 6)* (Dodsley 1761) — `https://www.gutenberg.org/cache/epub/60008/pg60008.txt`, SHA-256 `850d5686956f9e2a13719aa2d37edf09ab17658c0b36e65429e88a6cfd870d15`. Phạm vi công cộng.

## St Paul's (Wren) — bậc 3 cho kích thước tổng, bậc 4–5 cho tỉ lệ tầng
Trích nguyên văn (#48491, dòng 56–67, "Rev. Lewis Gilbertson's excellent Official Guide"):
> "The exterior length, exclusive of the projection of the steps, 515 feet; the interior, 479 feet; the width across the Transepts, from door to door, 250 feet; width across Nave and Aisles, 102 feet; and between the stone piers, 41 feet; the Western front, 180 feet; the diameter of the octagonal area at the crossing of Nave and Transept, 107 feet; the diameter of the drum beneath the Dome, 112 feet; of the Dome itself, 102 feet. The height of the Central Aisle, 89 feet. The total height from the pavement of the Churchyard to the top of the Cross, 365 feet; the height of the Western Towers, 221 feet."

Wikipedia "St Paul's Cathedral" (đọc qua WebFetch 23/10/2026, trích ngắn): "The width of the nave is 121 feet (37 m) and across the transepts is 246 feet (75 m)." · "The height from ground level to the top of the parapet is approximately 110 feet." · infobox "Length 518 ft (158 m)", "Height 365 ft (111 m)".

Dùng: dài 157 m (u −90 … +66,5), tường màn tới lan can 33,5 m, thân + gian bên 37 m, cánh ngang tới ±38 m (portico bán nguyệt), mặt tây 54,9 m, tháp tây 67,4 m, Ø trống (hàng cột) 34,1 m, Ø vòm 31,1 m, tới thập giá 111,3 m.
Ước (bậc 4–5, KHÔNG có số trong nguồn đã đọc): số cột hàng cột (32), cao tầng gác 52,4–61 m, dáng mặt cắt vỏ vòm, đèn lồng (86,4–98,4 m, 4 cánh trụ), Golden Gallery 85,6 m, quả cầu Ø ≈ 2 m, tầng tháp tây (tầng chuông mở có cột ghép đôi, mũ chì cong, quả dứa mạ vàng). Ghi: cần bản vẽ mặt đứng đo đạc (bậc 3) nếu chủ dự án muốn đúng tỉ lệ tầng.

## Monument — bậc 3 (kích thước), bậc 1 (vị trí)
Trích nguyên văn (#60008, mục "MONUMENT", dòng 121–143):
> "But the diameter of this column at the base, is 15 feet, and consequently it is 120 feet high; the height of the pedestal is 40, and the cippus or meta with the urn on the top 42, making 202 feet in the whole. On the cap of the pedestal, at the angles, are four dragons (the supporters of the city arms) and between them trophies, with symbols of regality, arts, sciences, commerce, &c."
> "Over the capital is an iron balcony, encompassing a cone 32 feet high, supporting a blazing urn of brass, gilt."

Wikipedia "Monument to the Great Fire of London" (WebFetch 23/10/2026): "202 feet (61.6 m) in height" · "a fluted Doric column" · "built of Portland stone topped with a gilded urn of fire".
Bề ngang bệ 21,5 ft và đế 27 ft vuông: Strype 1720 qua lookup.london (kết quả tìm kiếm, CHƯA đọc bản gốc — bậc 3 thứ cấp; cần kiểm khi chủ dự án duyệt).
Vị trí: OSM relation 3374550 "The Monument to the Great Fire of London" (tâm EPSG:27700 ≈ 532923, 180761). **Sửa lỗi look v1:** mô hình cũ đặt ở (532990, 180750) — lệch ≈ 68 m về đông.
Ước (bậc 5): bốn con rồng góc bệ (khối 1,2 m), hình bầu lửa + 9 lưỡi lửa mạ vàng (≈ 3 m = 42 − 32 ft), lan can ban công sắt 1,15 m.

## White Tower (Tower of London) — bậc 3 + 4, vị trí/hướng bậc 1
Wikipedia "White Tower (Tower of London)" (WebFetch 23/10/2026, trích ngắn): "Excluding its projecting corner towers, the keep measures 36 by 32 metres (118 by 105 ft) at the base" · "is 27 m (90 ft) high at the southern battlements" · "At the western corners are square towers, while to the north-east a round tower houses a spiral staircase." · "At the south-east corner is a larger semi-circular projection which accommodates the apse of the chapel."
Mũ chì cong trên 4 tháp góc + chong chóng: Hollar, *Long View* / *Prospects* (Met 360649, CC0 — đã có trong licenses/) — bậc 4. Tường quét vôi trắng: bậc 4 (tên gọi). Vị trí + hướng trục: OSM way 369135772 "White Tower" (bậc 1).
Ước (bậc 5): răng cưa lan can 1,8 m, trụ áp, 3 tầng cửa sổ, 3 tháp giữa mỗi cạnh tường trong (vị trí ước, như look v1 tường thành).

## London Bridge 1666, Old St Paul's
Giữ như LOOK-T4 (Hollar/Dugdale 1658, Met CC0; báo cáo LOOK-T4 §1) — vòng này không đổi hình học hai công trình này.

## Toà có tên 2026
Hình khối giữ như LOOK-T4 (OSM building:part + LiDAR EA, bậc 1). Vòng này chỉ đổi VẬT LIỆU để dễ nhận: 30 St Mary Axe (dải kính tối xoắn + lưới kim cương, mt 15), The Leadenhall Building (khung giằng chéo lộ, mt 16) — bậc 4 (ảnh công khai), không đổi hình khối.
