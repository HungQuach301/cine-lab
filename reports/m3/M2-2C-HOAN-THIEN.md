# M2.2 — HOÀN THIỆN trên nền animatic v3 · 04/10/2026

Làm theo quyết định chủ dự án ngày 04/10/2026 (duyệt v3 tại `71b68e2`, áp chính sách 3 cổng). **M2.2 không phải cổng duyệt**, nên P làm tiếp sang M2.3 mà không dừng.
- Chỉ render lại các shot và đoạn bị sửa: 00 (mới), 02, 04, 05, 06, 09, 19. Mười đoạn còn lại giữ nguyên trung gian v3.
- Mọi số dưới đây là **số đo thật**: P tự đo lại judder trên trung gian và tự xem khung.
- Ảnh trước/sau (1280×720, chụp cùng thời điểm) ở `reports/m3/m2-2c/truoc-sau/`.

## 0. Kiểm tài sản đầu việc
Master v3 còn nguyên trên đĩa, SHA-256 khớp `3891882d…94ec06`. Còn đủ 16 trung gian `sec/` và clip shot STORY. **Không phải dựng lại**, nên không tốn thêm giờ máy hay token.

## 1. Kết quả từng mục
| Mục | Trước | Sau | Đoạn | Judder (P đo) | Tương phản thấp nhất |
|---|---|---|---|---|---|
| **3.1 Bản đồ** | London: lưới gấp khúc, sông là một dải cong không rõ dáng. Paris: lưới nghiêng, không có sông. New York: một khối dài, không có bờ hay tên | **London:** Thames uốn qua Westminster, chạy qua City, vòng quanh mũi Isle of Dogs; nhãn "Thames", "Westminster". **Paris:** Seine với Île de la Cité và Île Saint-Louis, Louvre, Rivoli, Opéra; máy mở toàn cảnh ≈ 2 s rồi đẩy vào Avenue de l'Opéra. **New York:** Manhattan theo bề rộng từng km (mũi Battery, Lower East Side, hẹp ở Inwood), bờ New Jersey/Brooklyn/Bronx; nhãn "Manhattan", "Hudson River", "Broadway". Giữ phong cách giấy và mực nâu | 02, 05, 06 | 0 / 0 | 4,91:1 ("1807") |
| **3.2 Cuối đoạn 09** | Hai bảng thu còn 60 %, chữ nguồn và trục chỉ còn vài px | Mờ hết chữ nhỏ trước khi thu; chỉ giữ tên ngắn ("Phone operators", "Typists & secretaries") và số lớn **421k**, **3.92M**. Sau khi thu, chữ hoa cao ≈ 22,7 px ở 1080p (ngưỡng 18) | 09 | 0 / 0 | 6,96:1 (lúc đã thu) |
| **3.3 e04b** | 105 mm, máy cách đồng hồ ≈ 0,36 m, trôi 0,12 → mặt đồng hồ bị cắt mép phải | 70 mm, không trôi, giữ vị trí và hướng nhìn gốc. Mặt và khoen nằm trọn trong khung suốt 72 khung (kiểm khung 0/36/71), kim chỉ 7:53 | 04 | 0 / 0 | — (không có chữ) |
| **3.4 e19a** | 28 mm, máy xa: Ida rất nhỏ | 35 mm, đẩy chậm về đầu đèn L11. Cuối shot ở cỡ trung: Ida trên thang cao ≈ 1/3 khung, đọc rõ tay chạm đèn và đèn bừng (≈ 5,08 s). Giữ chạng vạng; trục và hướng nhìn nối với e19b | 19 | 0 / 0 | thẻ kết không đổi (8,78:1) |
| **3.5 Nguồn "1820s · 40,000+ lamps"** | Nguồn: London Remembers, English Heritage, Wikipedia | **Không tìm được nguồn sách hoặc học thuật đọc được toàn văn có trang** (mục 2) → **bỏ số khỏi hình**, sửa câu lời dẫn, thu lại đoạn 02 bằng Bill, ghép lại đoạn 02 | 02 | 0 / 0 | 4,91:1 |
| **3.6 Mở đầu** | Mục 3 | Đoạn móc 00, dài 6 s, không lời | 00 (mới) | 0 / 0 | chữ trong hình cũ đã đo (≥ 5,96:1) |

## 2. Mục 3.5: tìm nguồn, kết quả, câu thay
- **Đã tìm** nguồn cho "by 1823, nearly 40 000 lamps, 215 miles":
  - William Matthews (1827), *An Historical Sketch of the Origin, Progress and Present State of Gas-Lighting*: có trên Google Books và HathiTrust, nhưng truy cập từ máy này bị chặn (Google Books trả trang CAPTCHA; HathiTrust không trả kết quả). Archive.org không có bản.
  - Tomory (2014), "Competition and regulation in the early history of the London gas industry, 1800–1830", *The London Journal* 39(2): sau tường phí (Taylor & Francis). Bản trên Academia và ResearchGate cần đăng nhập.
  - Các trang web khác (historywebsite.co.uk, blog) đều nhắc lại số này nhưng không ghi nguồn gốc có trang.
- **Kết luận:** không xác minh được bằng nguồn đọc toàn văn có trang → áp phương án dự phòng của chủ dự án.
- **Lời cũ:** "The idea spread fast. By the 1820s, London had more than forty thousand gas lamps, along some two hundred and fifteen miles of street."
- **Lời mới:** "The idea spread fast. **Within a few years, gas lamps ran along street after street across London.**"
  - Không còn số.
  - "Within a few years" khớp mốc 1807 → khoảng 1812–1820. Mốc khởi đầu 1807 vẫn dựa trên London Remembers và English Heritage.
- **Thu lại** cả đoạn 02 bằng Bill (`pqHfZKP75CvOlQylNhV4`, `eleven_multilingual_v2`, stability 0,5, similarity 0,75, tốc độ 1,00) cho giọng liền mạch.
  - 314 ký tự, 25,99 s (bản cũ 27,48 s). Thời lượng đoạn giữ 32,04 s.
  - Whisper (small) khớp văn bản; chỉ đọc "Pall Mall" thành "Palmel", là cách đọc đã duyệt.
  - Tệp: `reports/m3/m2-2b/vo/bill-02-m22.mp3` cùng `.align.json`.
- **Hình:** bỏ dải "1820s · 40,000+ lamps · 215 miles" và chữ "1820s" trong ô tựa. Mạng phố sáng lan từ "spread" (16,56 s) tới "London." (22,8 s). Dòng nguồn còn "Sources: London Remembers · English Heritage".
- **SFX đoạn 02:** giữ 2 cue cũ (dời +6 s); thêm 2 cue khí xì: khi hàng đèn Pall Mall bật và khi mạng phố bắt đầu lan (M2-SFX-2, CC0).
- **AUTHORSHIP:** "Claude (rà độc lập bên ngoài) phát hiện; chủ dự án duyệt và giao sửa" (dòng 04/10/2026).

## 3. Mục 3.6: mở đầu, trước và sau
**Đánh giá 30 s đầu v3:**

| Mốc | v3 |
|---|---|
| 0–6 s | toàn cảnh thành phố chạng vạng, không lời |
| 5,5 s | Ida: "Evening, old street." |
| 9,0 s | lời dẫn bắt đầu |
| 11–18 s | đèn số một bừng |
| 41,3 s | sang đoạn 02 |
| ≈ 4:41 | số liệu "hôm nay" đầu tiên (BLS) |

- Trong 9 s đầu không có lời và không có tín hiệu nào cho biết phim nói về nghề nghiệp hôm nay. Người xem YouTube thường quyết định ở lại trong khoảng này.

**Sau (v4): đoạn móc 00, 6 s = 144 khung, không lời, chèn trước đoạn 01. Lời dẫn đã duyệt không đổi.**

| Mốc | v4 |
|---|---|
| 0–3,3 s | lưới cửa sổ văn phòng hiện đại sau ngọn đèn khí trên phố cổ (lấy từ khối 10–13, 1,0–4,3 s, máy đang chuyển động) |
| 3,0–3,3 s | hoà sang biểu đồ "CHANGE IN 10 YEARS" (lấy từ đoạn 14, 17–20 s): cột thang máy −18 % / −52 % đã có, cột word processors & typists đang mọc |
| 5,5 s | cột chạm **−34 %** |
| 5,75–6,0 s | mờ về nền tối, vào đoạn 01 |

- Câu hỏi hình ảnh ngay từ đầu: đèn khí cạnh văn phòng, nghề cũ cạnh nghề đang co. Sau đó phim kể từ đầu.
- **Chỉ dùng hình và số đã duyệt.** Số −34 % có dòng nguồn BLS trên khung. Không có chữ mới.
- **Âm thanh:** chỉ có nhạc nền "Immersed" (vào từ 0 s, có fade 1,5 s). Không SFX, không lời.
- **Tác động:** tổng thời lượng **9:56,6 → 10:02,6** (vẫn dưới trần 11:00). Mọi mốc tuyệt đối dời +6 s (timeline v4, cue SFX dời theo).
- Tỷ lệ phần, khi tính 6 s móc vào TODAY:

| Phần | Tỷ lệ |
|---|---|
| STORY | 17,2 % |
| HISTORY | 36,2 % |
| TODAY | 46,6 % |

- **Rủi ro:** móc dùng lại hình xuất hiện lần nữa ở 4:41–6:15. Đây là kiểu "flash-forward" quen thuộc; cảnh lặp lại chính là phần thưởng cho người xem đã chờ.
- Ảnh: `truoc-sau/3.6-moc-t2-*.jpg`, `3.6-moc-t5.5-*.jpg`.

## 4. Lỗi và giới hạn còn lại (đưa vào hàng chờ, không chặn G2)
1. **Đoạn 09, lúc bảng còn đủ cỡ:** nhãn trục 19 px, năm 18 px, chú thích 17 px, nguồn 16 px, ACTUAL 18 px (đo ở 1080p; ngưỡng chữ hoa ≈ 18 px). Đã như vậy từ v3. Mục 3.2 chỉ giao xử lý trạng thái thu nhỏ. Sửa phải làm lại bố cục bảng.
2. **Dòng nguồn** tăng 20 → 26 px (`lib.js`), chữ hoa ≈ 18,95 px: **cao hơn ngưỡng 18 px 5,3 %, sát vùng ±5 %**. Áp cho 02, 05, 06; đoạn 03, 07, 08 còn cỡ cũ vì không render lại.
3. **Đoạn 02:** vài đường phố cách điệu vắt qua sông phía đông Tower; năm 1820 chưa có cầu ở đó.
4. **e19a:** 1,5 s đầu shot là phố trống, Ida bước vào từ bên phải; than hồng đầu sào khó thấy ở cỡ trung.
5. **Đoạn 05:** nhãn "Opéra" lúc toàn cảnh nằm sát mép trên tấm giấy (đọc được, 8,38:1).
6. **Màu nâu năm/ngày:** đổi sang #4f2a0c vì trên trung gian mới chỉ đo được 4,24:1 và 4,38:1, dưới ngưỡng.

## 5. Chữ trên hình mới (theo chính sách 3 cổng; chủ dự án xem ở G2)
- **02:** "Thames", "Westminster". Dòng nguồn bỏ Wikipedia.
- **05:** "Seine", "Louvre", "Opéra"; "Avenue de l'Opéra" đặt lại nằm ngang.
- **06:** "Manhattan", "Hudson River", "Broadway".
- **09:** "Phone operators", "Typists & secretaries" (tên ngắn), "421k", "3.92M" cỡ lớn.
- Dữ liệu bản đồ: tự vẽ giản lược từ toạ độ công khai của cầu và địa danh. Không tải dữ liệu, không dùng tile bản đồ hay ảnh, nên không có tài sản mới cho RIGHTS.

## 6. Giờ máy, đĩa, token
**Render:**

| Mục | s/khung |
|---|---|
| Đồ hoạ 02 / 05 / 06 / 09 | 0,46–0,53 (TB) |
| e04b | 4,83 |
| e19a | 13,5 (tối đa 21,6) |

- Giờ máy M2.2 ≈ 1,5 h (render và ghép), chưa tính master.
- **Đĩa:** trống thấp nhất 7,8 GB, trên ngưỡng 6 GB. P đã dọn tấm nền, bản xem v3 và clip cũ: còn 14 GB lúc ghép master.
- **Trung gian:** `sec/` (v3) và `sec-m22/` giữ tới khi G2 duyệt; `sec-v4/` là symlink trộn hai thư mục.

**Token (harness):**

| Gói | Token | Hạn |
|---|---|---|
| HISTORY-M22 | 203,9 nghìn | 160 nghìn (**+27 %** so với hạn gói) |
| STORY-M22 | 64,6 nghìn | 100 nghìn |
| P cho M2.2 | ≈ 0,1 triệu (ước) | |
| **Cộng M2.2** | **≈ 0,37 triệu** | |

- Cộng dồn của tập ghi ở báo cáo M2.3 và đối chiếu với trần 2,85 triệu.

**ElevenLabs:**
- Đầu M2.2, bộ đếm đọc được 7 983/144 034, nhưng cuối M2.2b ghi 5 707. Phần chênh ≈ 2 276 ký tự **không do phiên này gửi**; phiên này chỉ gửi 314 ký tự cho đoạn 02 (M2.2) và 868 ký tự cho 2 Short (M2.3).
- Sau cả hai mốc: 8 121.
- Bộ đếm có thể cập nhật trễ, hoặc có lượt dùng ngoài phiên.

## 7. Mã
Nhánh cục bộ; bản vá lưu trong repo:
- `ep01-history` → `3083243`, bản vá `reports/m3/m2-2b/ma/ma-history-3083243.patch`
- `ep01-story` → `3cc1654`, bản vá `reports/m3/m2-2b/ma/ma-story-3cc1654.patch`

Thay đổi phía P:
- timeline v4 (`reports/m3/m2-2b/timeline-v4.json`);
- `mix_ep01.py` bỏ qua đoạn không lời;
- `ghep_ep01.sh` nhận tham số S, SFX, V.
