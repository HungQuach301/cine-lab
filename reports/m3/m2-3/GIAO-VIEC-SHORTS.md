# Giao việc SHORTS 9:16 · ep01 (P, 04/10/2026)

Dựng 3 Short dọc từ hình đã duyệt. Áp CHUAN-KENH-LL (gồm §6, §7). Nội dung số giữ nguyên như phim; **không thêm số mới**.

## Thông số chung
- 1080×1920, 24 fps, H.264 crf 10 yuv444p `-g 48`, không tiếng.
- Đầu ra: `/var/tmp/cine-out/ep01/shorts/<S1|S2|S3>.mkv`.
- Thời lượng mỗi Short = 0,6 s đầu + thời lượng lời + 1,5 s cuối, làm tròn lên số khung nguyên. Mọi Short phải **< 60 s**.
- **Vùng an toàn Shorts** (giao diện YouTube che): chữ và số chính phải nằm trong x 60–900 px, y 260–1500 px. Lề phải chừa ~180 px cho nút; dải dưới 1500–1920 dành cho tiêu đề và mô tả của YouTube.
- Cỡ chữ thông tin tối thiểu: chữ hoa ≥ 30 px (ở 1080 px ngang). Tương phản chữ ≥ 4,5:1, đo trên clip.
- Judder 0: chạy `python3 scripts/p/judder.py`, mục tiêu `loi == 0` và `giu_co_y_ge_1s == 0`. Không giữ khung đứng ≥ 2 khung; số lớn "đứng" thì vẫn phải có chuyển động nhẹ (hạt giấy, quầng thở).
- Mờ từ nền tối 6 khung đầu, mờ về nền tối 6 khung cuối, không có khung trùng.
- Hình phải theo **mốc từ** trong `.align.json` (hình không đi trước lời; không đứng trống > 3 s khi có lời).
- 1,5 s cuối: thẻ kết dọc "Last Lamplighters · full film on the channel" (chữ ngà trên chàm, cột đèn nhỏ hổ phách), trong vùng an toàn.
- **Ưu tiên dựng lại bố cục dọc bằng mã đồ hoạ sẵn có** (canvas2D của `design/m3/ep01/history/` và `design/m3/ep01/today/`; kích thước canvas đổi được). Chỉ dùng cảnh 3D đã render dưới dạng nền cắt dọc (crop 9:16 từ trung gian 1080p, scale ≤ 1,0 — không phóng to quá bản gốc) khi đó là cảnh truyện.

## S1 · "London still has lamplighters" (từ đoạn 07)
- Lời: `reports/m3/m2-3/vo/short-s1.mp3` cùng `.align.json` (31,9 s).
- Hình: nền Covent Garden ban đêm, crop dọc từ `/var/tmp/cine-out/ep01/sec/07.mkv` quanh cột đèn (cột đèn giữa khung).
- Đồ hoạ:
  - "London" ở "London";
  - chữ to **5 lamplighters** ở "Five lamplighters";
  - dòng nhỏ "~1,100 gas lamps · British Gas, 2023" ở "eleven hundred";
  - biểu tượng đồng hồ lên dây và chữ "every two weeks" ở "every two weeks".
- Nguồn trên hình: "Source: British Gas (2023)".

## S2 · "Which American jobs are shrinking fastest?" (từ khối 10–13)
- Lời: `reports/m3/m2-3/vo/short-s2.mp3` cùng `.align.json` (37,6 s).
- Hình: dựng dọc bảng cột ngang BLS 2025–35 bằng mã TODAY (`design/m3/ep01/today/s1013.js`, `lib.js`):
  - các cột xếp chồng theo chiều dọc, gạch chéo = dự báo;
  - thẻ "PROJECTION 2025–35 · BLS · jobs";
  - các số: word processors and typists −34 %, telephone operators −28 %, switchboard operators −26 %, data entry keyers −26 % (lời đọc "about a quarter"), telemarketers −21 %;
  - mỗi cột mọc đúng lúc lời đọc tên nghề;
  - số **−34%** đếm lên rồi đứng ≥ 3 s (có chuyển động nhẹ).
- Câu cuối "one task, repeated…": dùng biểu tượng vòng lặp và bánh răng như khối 10–13.
- Nguồn: "Source: U.S. BLS, Employment Projections 2025–35, Table 1.5".

## S3 · "One job in 270" (từ đoạn 08)
- Lời: `reports/m3/m2-2b/vo/bill-08.mp3` cùng `.align.json` (44,7 s) → Short ≈ 46,9 s.
- Hình: dựng dọc từ mã HISTORY (`design/m3/ep01/history/sec/08.js`, `lib.js`):
  - tiêu đề "One job in 270" ở đầu;
  - đường thang máy 1900–1970 **ngắt ở chỗ đổi phân loại** (giống bản 16:9: 97k phân loại 1950; 94k → 77k phân loại 1960; 77k → 37k phân loại 1970), trục từ 0;
  - nhãn "ACTUAL · U.S. Census · persons";
  - lưới khoảng 270 ô nghề, một ô tắt;
  - chữ **1 in ~270**.
- Nguồn: "U.S. Census, Historical Statistics of the U.S., Series D 233–682" và "J. Bessen (2016)".

## Bàn giao
- Từng Short kèm: `.timing.json` (s/khung), `judder.json`, tương phản thấp nhất (ô đo), ảnh 3 khung (đầu/giữa/cuối) 540×960 ở `/var/tmp/cine-out/ep01/shorts/xem/`.
- Âm thanh do P mix (lời, nhạc, SFX, −14 LUFS). Xưởng ghi cue SFX nếu cần vào `/var/tmp/cine-out/ep01/shorts/<S>.sfx.json` (`at_abs` tính từ 0 của Short; chỉ M2-SFX-1/2/3).
- Mã: commit cục bộ trên nhánh của worktree, không push. Cuối gói: `git diff HEAD~N --binary > /var/tmp/cine-out/ep01/shorts/ma-shorts.patch` (chỉ phần mới).
- Báo cáo trong lời trả về: từng Short (thời lượng, khung, judder, tương phản, s/khung), chữ mới trên hình, chỉ số ±5 % quanh ngưỡng, token tự ước.
