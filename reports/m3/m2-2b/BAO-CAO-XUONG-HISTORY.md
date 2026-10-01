# Animatic v3 · xưởng HISTORY — báo cáo (P lưu từ lời trả về của xưởng, 01/10/2026)

- **Nhánh:** cục bộ `ep01-history`, commit cuối `a8b0ae8`. Bản vá: `reports/m3/m2-2b/ma/ma-history-a8b0ae8.patch`.
- **Token:** harness **328,2 nghìn** so với hạn 200 nghìn (**+64 %**).

## Kết quả (P đo lại judder trên chính clip trung gian H.264 crf 10 yuv444p)
| Đoạn | Khung cần / có | judder loi / giữ ≥ 1 s | Tương phản thấp nhất (xưởng đo) | s/khung TB / max | MB |
|---|---|---|---|---|---|
| 02 | 769 / 769 | 0 / 0 | 4,79:1 ("1820s", nâu, góc tối) | 1,057 / 2,475 | 73 |
| 03 | 637 / 637 | 0 / 0 | 5,59:1 | 0,858 / 2,483 | 82 |
| 05 | 589 / 589 | 0 / 0 | 5,50:1 | 0,847 / 1,837 | 64 |
| 06 | 659 / 659 | 0 / 0 | 4,86:1 ("April 1907") | 0,772 / 2,084 | 84 |
| 07 | 782 / 782 | 0 / 0 | 8,13:1 | 0,566 / 1,592 | 53 |
| 08 | 1 138 / 1 138 | 0 / 0 | 6,22:1 | 1,049 / 2,317 | 137 |
| 09 | 664 / 664 | 0 / 0 | 6,01:1 | 1,063 / 2,546 | 40 |

- Đồ hoạ 5 238 khung: trung bình 0,899 s/khung, cao nhất 2,546 s/khung. Đoạn 03 ghép tấm nền s03 của xưởng STORY.
- **Luật ≤ 3 s trống:** đoạn 07 có quãng 3,4 s; xưởng đã thêm chữ "London:" ở 3,22 s rồi render lại.
- **Đĩa:** mức trống thấp nhất theo khối: 06 là 9,8 GB, 07 là 9,4 GB; lúc kết thúc còn 12 GB. P đã xoá tấm nền s03 (1,1 GB) và gỡ worktree.

## L2 ở đoạn 08 (thống nhất với khối 10–13 và đoạn 14)
Đường thang máy chia 3 mảnh, mỗi mảnh một kiểu điểm:

| Mảnh | Giá trị | Điểm | Nhãn | Hiện lúc |
|---|---|---|---|---|
| A | 1900–1950: 13, 25, 41, 68, 87, 97 (phân loại 1950) | tròn | "13k" ở "thirteen" (14,88 s), "97k" ở ~20,35 s | — |
| B | 94 → 77 (phân loại 1960) | vuông | "94k", "77k" | 21,94 s ("Then") |
| C | 77 → 37 (phân loại 1970) | thoi | "37k" | "thirty-seven" (26,43 s) |

Dòng chú dưới trục: "Line breaks where census job definitions changed". Đoạn 09 dùng cùng bảng §6.1, có vạch phân loại trước cột 1960 và cột 1970.

## Chữ trên hình mới (chờ chủ dự án duyệt)
- **02:** "LONDON"; "1807" / "1820s"; "Pall Mall"; "the first gas-lit street"; "Sources: London Remembers · English Heritage · Wikipedia, “19th-century London”".
- **05:** "PARIS", "1878", "64 / electric arc lamps", "Avenue de l’Opéra", "Source: ETHW, “Jablochkoff Candles in Paris”".
- **06:**
  - "NEW YORK", "April 1907";
  - trang báo vẽ lại, không có tên báo: "NEW YORK · APRIL 1907", "LAMPLIGHTERS / STRIKE", "Men demand union recognition / and better pay";
  - "police lighting the lamps", "about a week", "back at work";
  - dòng nguồn ghi ba báo.
- **07:** "London: Covent Garden · The Mall · palaces & theatres", "clockwork timer", "every two weeks".
- **08:**
  - tựa "Elevator operators, United States", ghi chú phân loại;
  - "James Bessen, economist", "about 270 occupations", "1950 census → 2010", "Elevator operator";
  - "Source: J. Bessen (2016), “How Computer Automation Affects Occupations”".
- **09:** "(counted together)", chú thích phân loại, nhãn ACTUAL.

## P nhận xét khi xem khung
1. Bản đồ London (02) và bản đồ Opéra (05) còn trừu tượng: lưới đường gấp khúc, khó đọc ra là thành phố. Đạt mức animatic; đề xuất làm rõ hơn ở M2.2.
2. Cuối đoạn 09, hai bảng thu còn 60 % để lộ văn phòng phía sau, nên chữ trên bảng rất nhỏ. Tương phản được đo lúc bảng còn đủ cỡ.
3. Đoạn 07 chưa có bản Short 9:16.
