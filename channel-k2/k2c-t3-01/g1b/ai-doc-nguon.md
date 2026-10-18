# G1b T3 — AI đọc nguồn cho cảnh 1782 (Kinh thánh §12.2–§12.3, lệnh AI-T3)

> Phiên con của G1b T3 Gibraltar, 18/10/2026. Máy đọc: `g1b/ai-doc-nguon.json`. Không gọi API nào (chi phí **$0**). Tôi đọc ảnh trang bằng công cụ xem ảnh của phiên, không dùng OCR.

## 1. Lọc và phân loại `reports/nc-ai/aib/danh-sach-9-1782.json`

- Điều kiện lọc: `dung_duoc == true` VÀ `luot2 == "correct"`. Còn **62/82 mục**.
- Phân loại: **(a) hoạt động nhìn thấy 12 · (b) mật độ/thành phần 32 · (c) không dùng cho hình 18**.
- Mọi mục đều ở **bậc 2**. Văn bản không cho vị trí. Tên nơi (Willis', Europa, South Port Ditch…) phải neo bằng bậc 1 (plan 1786) trước khi đặt lên hình.

### (a) Hoạt động nhìn thấy được

| # | Hoạt động (nguồn, trang, ngày) | Gợi ý dùng |
|---|---|---|
| 13 | Dân "wonderfully active in securing themselves and their property" (Drinkwater 1786 tr. 351, ngày không ghi, trước 1/9) | **KA1782 hẻm phố**, 2o-phố, Grand Parade. Ít người, vì phần lớn dân đã rời phố từ 4/1781 (S062) |
| 6 | "Every one … able to fire a musquet, or carry a shot, must take post upon any alarm" (Ancell tr. 254, 6/9) | 2j (khẩu đội). Ở KA1782 chỉ dùng nếu cảnh là lúc báo động (người khiêng đạn) |
| 76, 77 | Khẩu đội bắn đạn nung đỏ hết cỡ 8/9, 7 h → 16 h (Spilsbury tr. 75) | **2j** (khớp S059): kíp pháo nạp đạn nóng |
| 7, 8 | Ống nhòm khắp đồn soi pin nổi, 7/9 (Ancell tr. 254) | Lính/sĩ quan trên tường biển (Line Wall, Grand Parade, King's Bastion). Không dùng trong hẻm kín |
| 22, 23 | Thuỷ thủ khiêng hành lý về Europa, 4/9 (Spilsbury tr. 73) | Chỉ khi bậc 1 cho tuyến đi. Mặc định không đưa vào hẻm |
| 26 | Trung đoàn 39 cắm trại ở South Port Ditch, 6/9 (Spilsbury tr. 73) | 2o/2g góc nam, sau khi neo South Port Ditch trên plan |
| 2 | Rock Gun bắn liên tục, 6/9 (Ancell tr. 254) | Chỉ cảnh công sự có Rock Gun |
| 79, 80 | Thuyền settee từ Algiers chở bò, 30 cừu, rượu, cập 13 h ngày 9/9 (Spilsbury tr. 75) | Chỉ khi bậc 1 cho bến cập. Không đưa vào hẻm |

**Chỉ ba mục dùng được trong khung neo KA1782 (hẻm phố):**
- #13: dân che chắn và mang đồ đạc.
- #6: khiêng đạn, chỉ khi báo động.
- #24 (nhóm c): căn cứ để **không** dựng quầy bày thực phẩm, vì "No sugar, tea, flour, or butter, to be bought here".

### (b) Mật độ và thành phần (32 mục)

- **Bảng gác 7/9/1782:** #42–#63, #66–#68.
- **Biên chế và lao dịch:** #69–#75.
- **Gác cổng và tăng cường:** #4, #35, #36.
- **Thành phần đơn vị:** #5 (đại đội Corsica), #34 (thuỷ thủ, Corsica ở gác nam), #71 (ba trung đoàn Hanover).
- **Toán lao động 1 200 người ở Willis':** #21.
- **Quân số theo Ancell:** #0, "very few more than 5900 men and boys, including sick, wounded and disabled". Số này lệch với biên chế 7 535 (#72) và với S079 "about 7,500" trong lời KA1782. Ancell đếm người còn chống cự được, nên **không** thay số trong lời.

### (c) Không dùng cho hình (18 mục)

- Thuyền đưa thư: #14–#16, #20.
- Thương vong: #78. Kinh thánh §10.6 không cho dựng.
- Tâm trạng: #12, #40. "Pastime" không được dựng, vì §10.6 cấm cổ vũ bạo lực.
- Một cá nhân chỉ huy: #10.
- Bắn đêm, bắn ở Lines: #28–#31, #81.
- Đào ngũ: #32.
- Bỏ gác: #37.
- Trạng thái công sự ở Lines: #33.
- Vật trùng mục khác: #3.
- #24: thêm vào hẻm như một vật "không có".

### Sai sót của danh sách NC-AI phát hiện khi đối chiếu ảnh trang (sửa trong JSON, trường `ghi_chu` / `trang_doi_chieu_anh`)

1. **#57 Mole: 59 lính, không phải 54.** Đọc trên cả hai bản quét. Tổng SOUTH 266 chỉ khớp khi ô này là 59.
2. **#42 Flag Staff: 15 là lính pháo binh** (cột "Ptes." dưới ARTILLERY), không phải bộ binh.
3. Mọi dòng bảng gác (#42–#63) nằm ở **trang 74**. Danh sách NC-AI ghi trang 75 cho phần lớn các dòng này. Trang 75 là bảng Picquets / Establishment / Fatigue (#69–#75).

Ba lỗi này cho thấy luật §12.3 ("câu lên hình đối chiếu ảnh trang") là cần. Lượt 2 chấm cả ba mục là "correct", nhưng đó chỉ là kiểm khớp với OCR.

## 2. Bảng gác 7/9/1782 (Spilsbury, tr. 74–75): đọc từ ẢNH trang

**Nguồn.**
- John Spilsbury, *A Journal of the Siege of Gibraltar 1779–1783*, ed. B. H. T. Frere (Gibraltar Garrison Library, 1908).
- Internet Archive `ajournalsiegegi00spilgoog`, bản University of Michigan do Google quét, `possible-copyright-status: NOT_IN_COPYRIGHT`.
- Chỉ dùng dữ kiện. Ảnh trang không lên hình.
- Tôi tìm vị trí trang bằng `hocr_pageindex` của IA. Leaf 136–138 là tranh minh hoạ chèn giữa tr. 72 và 73. Leaf 139 là tr. 73.

| Trang | Leaf | URL | SHA-256 ảnh (JPEG, BookReader) |
|---|---|---|---|
| 74 | 140 | https://archive.org/download/ajournalsiegegi00spilgoog/page/n140.jpg | `5e47b6e531be1fc11b29ad482b5436a3ea80c8a759fea139cf544f5bb9c3ce88` |
| 74 (bản quét thứ hai) | 142 | https://archive.org/download/ajournalsiegegi00spilgoog/page/n142.jpg | `172aa7d6881126ecf17abad54e3b0bfe1c4d5cce1b1cc974efdfe1b49287a733` |
| 75 | 145 | https://archive.org/download/ajournalsiegegi00spilgoog/page/n145.jpg | `c5d5c32f7c7623ada1822fd58e62148f9a29c1a0c1f79d74f7a31200c6cecb40` |

Ảnh nằm ở scratchpad của phiên con, không vào git (mỗi tệp 0,6–1 MB). Tải lại bằng URL trên rồi so SHA. Lưu ý: BookReader có thể trả JPEG nén lại, nên SHA chỉ đúng với bản tải ngày 18/10/2026.

**Số lính gác theo điểm gác.** Cột: đại uý · sub · trung sĩ · hạ sĩ · tay trống · **lính** | pháo binh: hạ sĩ quan · lính. Đầy đủ trong JSON `bang_gac_7_9_1782`.

**TOWN** (lính bộ binh):

| Điểm gác | Lính bộ binh |
|---|---|
| Governors | 6 |
| Lt-Governors | 9 |
| Land Port | 86 |
| Water Port | 88 |
| Main Guard | 37 |
| Grand Battery | 26 |
| Castle | 12 |
| South Line Wall | 9 |
| North Line Wall | 15 |
| South Port | 29 |
| Middle Hill | 30 |
| Artillery Guard | 15 |
| Signal House | 6 |
| Victualling Office | 9 |
| **Patroles** | **9 trung sĩ + 18 lính** |
| **Orderlies** | **9 trung sĩ + 2 tay trống + 2 lính** |

Điểm gác TOWN chỉ có pháo binh: Willis' 6 hạ sĩ quan + 58 lính; Flag Staff 2 + 15.

| Khu | Lính bộ binh |
|---|---|
| **TOWN PARADE** | **397** (+ 84 lính pháo binh). Cả khu: 5 + 13 + 41 + 42 + 12 + 397 + 12 + 84 = **606 người** |
| **LINES** | Queen's 30, Prince's 50, King's 50 = **130** |
| **SOUTH** | Europa 71, Rosia 30, Mole 59, Ragged Staff 30, South Shed 21, P. W. Lines 6, Magazine 13, Camp 9, Hospital 12, Windmill Hill 6, Buena Vista 6, Gen. La Motte's 3 = **266** |
| **TỔNG IN** | Đại uý 9 · sub 23 · trung sĩ 61 · hạ sĩ 74 · tay trống 23 · **lính 793** · pháo binh hạ sĩ quan 15 · lính 108 |

Tổng toàn đồn: **1 106 người trực gác**.

**Trang 75:**
- Picquets 689 lính.
- Biên chế lính (Establishment, Private) **7 535**.
- King's Works: Engineers 800.
- Fatigue 240.
- "N.B.—One Captain and two Picquets stay at the South."

**Kiểm.** Script kiểm mọi cột của ba khu: cộng lại đúng các dòng tổng in.

**Ô không chắc** (đã giải bằng tổng in):
- Main Guard, cột hạ sĩ: nét in gãy, đọc là 4. Bản n142 rõ hơn.
- TOWN PARADE, cột lính: đọc 397.
- Mole: đọc 59.

### Suy ra mật độ lính cho một hẻm phố cổ trong khung neo KA1782

1. **Người trực gác thật sự đi lại trong phố là Patroles và Orderlies.** Patroles có 27 người, Orderlies 13 người, cộng **40 người** (bậc 2, ảnh trang). Mọi gác khác **đứng cố định tại điểm gác**: cổng, Main Guard, kho… Chỉ đặt lính gác cố định vào khung khi plan 1786 (bậc 1) cho thấy điểm gác nằm trong khung.
2. **Chiều dài phố.** Nửa tổng chu vi 22 khối phố ghost-1782 (Drinkwater 1786, `ghost/ghost-1782.geojson`) là **≈ 2,71 km** mặt phố. Đây là **cận dưới**, vì nửa đông phố cổ không có trên bản đồ (SH để trống). Phép đo dùng toạ độ phẳng tại vĩ độ 36,14°.
3. **Mật độ cận trên.** Giả sử cả 40 người cùng ở ngoài phố một lúc: 40 / 27,1 = **≤ 1,5 lính trực / 100 m phố**. Thực tế thấp hơn, vì mạng phố dài hơn 2,71 km. Bảng không cho biết bao nhiêu người ra đường cùng lúc.
4. **Gợi ý dựng (suy luận, ghi là suy luận).** 9 trung sĩ + 18 lính có thể là 9 toán tuần 1 + 2. Đây là suy luận từ tỷ lệ; văn bản không nói. Như vậy, một hẻm 100–200 m có tối đa **một toán tuần 3 người**, cộng 0–1 lính liên lạc.
   - Thêm toán lao dịch (#74, 240 người) **chỉ khi** có căn cứ vị trí. Ví dụ: tổ sửa tường hoặc dọn đổ nát trong vùng "THE RUINS". Văn bản không cho vị trí.
   - Dân thường: rất ít (#13; S062).
5. **Bậc căn cứ.**
   - Số người: bậc 2 (ảnh trang).
   - Chiều dài phố: dẫn xuất từ bậc 1.
   - Mật độ ≤ 1,5/100 m: phép chia, suy luận.
   - Cách chia toán tuần 1 + 2: suy luận, không có căn cứ trực tiếp.
   - Vị trí: không có. Phải lấy từ plan.
6. **Cần chủ dự án biết.** Khung neo 1782 bản V6 có **47 người** (TB 44,6, tối thiểu 22; `reports/v6/khung-neo/KHUNG-NEO-V6.md`). Bảng gác chỉ đỡ được vài lính trực trong một hẻm. Phần còn lại cần căn cứ khác (lính nghỉ trực ở trong phố? lao dịch? lính đóng trại?), nếu không thì phải giảm. Tôi **không** tìm được nguồn cho lính nghỉ trực đi lại trong phố trong 9 trang đã đọc.

## 3. Trang phục: vai nào có nguồn (theo `reports/v6/RIGHTS-V6.md`, `KHUNG-NEO-V6.md` §2)

| Vai | Nguồn | Mức |
|---|---|---|
| Bộ binh Anh (áo đỏ, gi-lê/quần trắng ngà, ghệt đen, dây đeo trắng) | Royal Warrant 1768. Tranh và phác thảo Copley PD: Met 60.44.17, Cleveland 1950.215, bản khắc Sharp LoC 96510788. Trumbull "Sortie" (Met 12828) | Có nguồn (bậc 3–4). Royal Warrant **chưa trích nguyên văn** → khung neo ghi "approx." Màu nẹp trung đoàn: **illustrative** |
| Pháo binh Hoàng gia (áo lam đậm viền đỏ) | Royal Warrant 1768 | Có nguồn. Cùng lưu ý chưa trích nguyên văn |
| Bộ binh Tây Ban Nha (áo trắng) | Reglamento 1768; Clonard, *Historia orgánica…* (bản khắc PD) | Có nguồn. Màu viền: **illustrative** |
| Bộ binh Pháp (áo trắng) | Règlement 1779 | Có nguồn. Màu viền: **illustrative** |
| Dân thường nam/nữ, thuỷ thủ | Không có nguồn riêng | **illustrative** |
| **Chưa có trong RIGHTS-V6**, nhưng bảng gác cho thấy có mặt: ba trung đoàn Hanover (Rheden, La Motte, Sydow, ~350 lính mỗi trung đoàn, #71); đại đội Corsica (#5, #34); lữ đoàn thuỷ binh (#22, #34); kỹ sư/thợ (800, tr. 75) | — | **Không có nguồn trang phục.** Không dựng riêng các vai này; nếu xuất hiện thì ghi illustrative |

NC-AI §7.1 đã ghi: 9 trang nhật ký không tả quần áo. Vì vậy trang phục chỉ lấy từ bậc 3–4.

## 4. Chi phí
- API: **0** lệnh. Claude/OpenAI $0.
- Tải web: 10 tệp từ archive.org (metadata, page_numbers, hOCR index/searchtext, 7 ảnh trang), User-Agent `CineLab-research (+https://github.com/HungQuach301/cine-lab)`.
