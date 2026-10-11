# QC k2g-ep01 (nhap) — TRƯỢT

| Mục | Kiểm | Kết quả | Giá trị | Ngưỡng | Sát ngưỡng (±5 %) | Ghi chú |
|---|---|---|---|---|---|---|
| Q1 | Judder (giữ 2–12 khung, framemd5) | **TRƯỢT** | 7 | 0 |  | {'S1': 5, 'S2': 2} |
| Q2 | Khung gần trùng giữa chuyển động (tol 0,1) | **ĐẠT** | 0 | 0 |  |  |
| Q3 | Máy xuyên hình học (log máy + khung phẳng) | **TRƯỢT** | 4 | 0 |  | log {} · phẳng {'S1': 2, 'S2': 2} |
| Q4 | Loudness/TP k2g-ep01-nhap-master.mp4 | **ĐẠT** | -14.0 LUFS / -1.6 dBTP | −14±1 / ≤ −1 |  |  |
| Q4 | Loudness/TP k2g-ep01-short-S1.mp4 | **ĐẠT** | -14.0 LUFS / -1.7 dBTP | −14±1 / ≤ −1 |  |  |
| Q4 | Loudness/TP k2g-ep01-short-S2.mp4 | **ĐẠT** | -14.0 LUFS / -2.2 dBTP | −14±1 / ≤ −1 |  |  |
| Q5 | Tương phản chữ thấp nhất | **TRƯỢT** | 1.02 | 4.5 |  | 07 f2508 “WHAT STUDIES FOUND (CRS SUMMARY)” |
| Q6 | Cỡ chữ hoa tối thiểu (mọi khung mẫu) | **ĐẠT** | 33.4 px (S1 f12 “Sources: USGS, Iron and Steel Statistics”) | 18 / 30 px |  | mẫu tự nâng cỡ: {'02': 120, '04': 184, '06': 710, '07': 102, '08': 932, '10': 560, '11': 274, 'S1': 389, 'S2': 525} |
| Q7 | Nhãn ACTUAL/PROJECTION khớp loại số | **TRƯỢT** | 15 | 0 |  | 00/plate@0.0: thiếu nhãn ACTUAL; 05/plate@25.1: thiếu nhãn ACTUAL; 06/plate@0.0: thiếu nhãn ACTUAL; 06/plate@27.6: thiếu nhãn ACTUAL; 06/plate@63.9: thiếu nhãn ACTUAL; 06/plate@87.0: thiếu nhãn ACTUAL |
| Q8 | Nguồn (toàn văn, không Wikipedia) + số khớp lời | **ĐẠT** | 0 | 0 |  |  |
| Q9 | Số khung khớp timeline | **ĐẠT** | master 24723/24723 | = timeline |  |  |
| Q10 | Thời lượng Short S1 | **ĐẠT** | 23.25 s | ≤ 60 s |  |  |
| Q10 | Thời lượng Short S2 | **ĐẠT** | 32.92 s | ≤ 60 s |  |  |
| Q11 | Khung trống > 3 s khi có lời (bản dài) · chữ đứng > 3 s (Shorts) | **ĐẠT** | 0 | 0 |  |  |
| Q13 | Số trên tiêu đề/thumbnail/mô tả/Shorts truy được về numbers, đúng dấu, nhãn dự báo | **ĐẠT** | 0 | 0 |  |  |
| Q14–18 | Luật nhịp | **ĐẠT** | không áp (tập ≤ 3) |  |  |  |
| Q20 | Chữ không đè hình (cờ hit + vùng isotype) | **ĐẠT** | 0 | 0 |  |  |
| Q19 | Hồ sơ quyền tư liệu (danh sách trắng, RIGHTS, ≤ 20 %) | **ĐẠT** | 0 | 0 |  | không dùng tư liệu |
| Q21 | Dòng nguồn khớp số/câu đang hiện | **TRƯỢT** | 6 | 0 |  | 04 “1892: a strike at the Homestead works”: câu có số/năm/cơ quan chưa khai num hoặc src; 05 “1 bar = 10 million tonnes · orange = Uni”: câu có số/năm/cơ quan chưa khai num hoặc src; 05 “1950: much of the world was still rebuil”: câu có số/năm/cơ quan chưa khai num hoặc src; 12 “1880s: power meant controlling the cheap”: câu có số/năm/cơ quan chưa khai num hoặc src |
| Q22 | Chữ nằm trong khung (lề ≥ 8 px, gồm Shorts 9:16) | **TRƯỢT** | 1 | 0 |  | 07 f1080 “Sources: Proclamation 10896 (Feb 2025) ·” hộp 200…2647 (khung 1920) |
| Q23 | Câu/thẻ nhiều số: cùng đối tượng, loại, kỳ, cơ sở | **TRƯỢT** | 11 | 0 |  | lời 06: khác đối tượng (nguồn USGS/worldsteel); lời 06: khác đối tượng (nguồn USGS/worldsteel); lời 06: khác đối tượng (nguồn USGS/worldsteel); lời 07: khác đối tượng (nguồn Proclamation/Regulation) |
| Q24 | Nhãn phân loại khớp số | **ĐẠT** | 0 | 0 |  |  |
| Q25 | Thẻ khoảng số không hiện số trung gian | **ĐẠT** | 0 | 0 |  |  |
| Q26–31 | Luật chất lượng v3 | **ĐẠT** | không áp (tập ≤ 6; Q-L6v2 = B) |  |  |  |
| LOCK | checks/ khớp LOCK (luật khoá không bị sửa) | **ĐẠT** | KHỚP | TREE_SHA256 |  |  |
