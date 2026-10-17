# NC-LS — "Lịch sử + Timelapse": chiến tranh, sự kiện và nhân vật lịch sử kể qua nơi chốn mọc/đổi theo thời gian — BÁO CÁO NGHIÊN CỨU

> Phiên nghiên cứu NC-LS, 17/10/2026, theo lệnh chủ dự án 17/10. Nhánh `nc-lich-su` tạo từ `origin/main`. **Chỉ tài liệu. Không merge. DỪNG chờ chủ dự án.**
> Mọi lượt xem, số người đăng ký, số video là **số công khai YouTube Data API, đọc ngày 17/10/2026 (UTC)**. Mọi trung vị, nhịp đăng, tỷ lệ, điểm chấm là **tự tính, không phải chỉ số YouTube**. Chỗ nào là ước tính ghi **(ước)**; chỗ nào chưa kiểm bằng nguồn gốc ghi **(chưa kiểm)**.
> Không tải video, khung hình, thumbnail của kênh nào. Bình luận và mô tả gốc để **ngoài git** (`~/.cache/nc-ls/`); trong repo chỉ có số đo và nhận xét bằng lời của phiên. Tiêu đề video của kênh khác không chép vào repo; trong báo cáo chỉ nêu đề tài.

## Khối điều lệ (lệnh + thực tế)
| Trường | Lệnh | Thực tế |
|---|---|---|
| Loại phiên | Nghiên cứu (chỉ tài liệu) | đúng |
| Nhánh | `nc-lich-su` từ `origin/main` | đúng; đẩy `nc-lich-su`, không merge |
| Tệp được sửa | CHỈ `reports/NC-LICH-SU-BAO-CAO.md` + `reports/nc-lich-su/*.csv\|json` ≤ 1 MB | đúng: báo cáo + 5 tệp (`kenh.csv`, `de-tai-cau.json`, `binh-luan-tom-tat.json`, `cham-diem.json`, `cost.json`), tổng **52 KB**. Không sửa main, nhánh tập, `checks/`, `scripts/`, `design/`, `docs/`. Không ghi RIGHTS/AUTHORSHIP/COST-LEDGER (ngoài vùng; dòng đề xuất ở §10) |
| Trần | Claude API ≤ $1 (ghim) · YouTube ≤ 3 000 đv · ElevenLabs 0 · giờ máy ≤ 1 h | **$0** (không gọi API trả tiền) · **2 124 đv** · **0 ký tự** · **≈ 0,1 h** |
| Preflight | bắt buộc; che email | `verify.sh`: 10 PASS, 3 FAIL không liên quan việc tài liệu (three.js lock, tifffile/pyshp, k2v node_modules). Hook pre-commit/pre-push cài đầu phiên; kết quả `tools/preflight.sh` ở §11. 0 email trong mọi tệp ghi |
| Điều kiện dừng | xong → đẩy → dừng; không dừng hỏi giữa chừng | (1) xong việc. Câu hỏi không chặn đã tự quyết, ghi ở §12 |

---

## 0. Tóm tắt cho chủ dự án (đọc 2 phút)

1. **Cầu của thể loại là thật và rất lớn, nhưng cung cũng dày.** 17 kênh chiến tranh/bản đồ trận đánh mạnh nhất có trung vị 10 video dài gần nhất từ **21 nghìn** (American Battlefield Trust) tới **6,28 triệu** (Yarnhub); 10/17 kênh ≥ 250 nghìn. Ở 15 đề tài ứng viên, **14/15 đã có ít nhất một video dài đúng đề tài ≥ 100 nghìn lượt** (trừ Zürich 1799); Vienna 1683 có **13 video dài ≥ 500 nghìn**. Mình không vào được bằng "đề tài chưa ai làm". Mình vào bằng **cách nhìn chưa ai làm**.
2. **Khoảng trống đo được là "NƠI CHỐN ĐỔI THEO THỜI GIAN, đúng và không AI".**
   - Kênh chiến tranh lớn kể bằng **bản đồ 2D phẳng + tranh**. Chỉ Epic History mới mở loạt "in 3D" (Verdun 3D 336 nghìn, Copenhagen 1801 3D 708 nghìn). Không kênh nào cho thấy **thành phố/thành luỹ mọc, cháy, sập, dựng lại theo năm** quanh trận đánh.
   - Kênh "thành phố theo thời gian" (Latos, Restored Timeline) **hầu như không kể chiến tranh hay nhân vật** (Restored Timeline có 1/10 video dài gần nhất về quân đội, dạng khác). Ba kênh tái dựng nơi chốn bằng **ảnh AI** (Restored Timeline 10/10 video gần nhất nhắc AI trong mô tả; Matt Reconstructs 6/10; Charles Reconstructs 10/10) và bị bắt lỗi thời đại (công trình "đi qua đường", tàu điện trước ga, xe hơi năm 8000 TCN).
   - Bình luận cho thấy khán giả **thưởng cho "không AI"** (một bình luận cảm ơn vì "not being AI" có 296 like ở video Pearl Harbor 782 nghìn lượt) và **thưởng cho then/now** (khán giả video Boston AI xin lặp lại đoạn then/now; khen ảnh hiện đại của toà nhà).
   - **Nhãn "No AI" một mình không độc quyền:** nhóm TimeGhost (The Great War, Real Time History) đã ghi trong 10/10 mô tả rằng họ không dùng AI tạo sinh để tạo tài sản mới. Lợi thế của mình là **"không AI" + nơi chốn 3D đúng năm + nguồn từng mốc**, không phải chỉ "không AI".
3. **Định vị đề xuất (§2):** lời hứa chính *"Why everyone fought over this place — watch it rise, burn and rebuild, every date sourced, no AI imagery."* Hình thức đề xuất: **(A) series trong Moving Parts**, khung "vì sao nơi này được tranh giành", kèm **cổng quyết định sau 3 tập lịch sử** để chuyển sang (C) nếu số liệu ủng hộ. **Không mở kênh 3 (B)** khi chỉ có 1 làn sản xuất.
4. **15 đề tài (§3), chấm /25:** đầu bảng **London 1666** (21, XANH — sự kiện, không phải trận đánh), **Boston 1775–76** (20, XANH), **Vicksburg 1863** (20, XANH), **Vienna 1683** (20, VÀNG), **Gibraltar** (19, VÀNG), **Rotterdam 1940** (19, XANH), **Zürich 1799** (19, XANH). Đã loại 7 đề tài ĐỎ/VÀNG nặng (Crimea, Stalingrad, Constantinople, Derry, Acre/Jerusalem, Dresden, Tenochtitlan).
5. **Tập thử (§4): giữ Gibraltar làm T3, khung lại thành "14 lần bị vây — vì sao Rock luôn bị tranh giành"**, chọn 3 nhịp 1704 → Great Siege 1779–83 → 1941 (đường băng trên eo đất trung lập, đường hầm) → hiệp ước 2026. Lý do: dữ liệu dựng sẵn nhiều nhất (tiền kỳ T3: 44 claim, 28 tài sản, 38 giấy phép; đoạn thử gib20 24,5 s đã dựng trên llvmpipe), neo thời sự có ngày (Nghị viện châu Âu 14/12/2026), cầu đạt (dài lớn nhất 679 nghìn, Short 6,26 triệu). Đổi lại: **VÀNG đầy đủ** và **khoảng trống chỉ 3/5** (3 kênh lớn đã làm Great Siege). Tập kế bắt buộc XANH: **London 1666** hoặc **Boston 1775–76**.
6. **Máy dựng (§5):** k2v + V5b-2a đã có xương sống thời gian, 7 preset máy, nhà thủ tục 6×6 kiểu, tàu theo thời kỳ, xe/người A-lite, chân dung cắt nền Ken Burns. Còn thiếu: **mũi tên/đội hình quân theo giờ, hạm đội theo đội hình, tuyến vây/hào, thành luỹ mọc–sập, đồng hồ ngày/giờ + mặt trời, khói/lửa, nhập footprint nhà thật + mái theo thời kỳ, số hoá footprint lịch sử**. Ước **5,5–7 h máy D / 3,6–4,6 h máy C cho tập 10 phút (ước)**, vẫn dưới trần 12 h. Phần nặng thật là **công người số hoá bản đồ lịch sử: 20–40 h/tập (ước)**.
7. **Luật hình (§6)** từ đánh giá T2 của chủ dự án, đo được bằng mặt nạ đã có (`fabric_pct`, `content_pct`) và `campath.json` (AGL): (a) cảnh gắn nhãn "thành phố" phải có **nhà + đường ≥ 25 % khung (trung vị cảnh)**, không khung nào < 15 % trừ ≤ 3 s cuối của cú reveal; (b) **AGL > 50 km tính là "địa cầu": ≤ 1 lần/tập, ≤ 3 s**; mặc định AGL ≤ 3 km cho thành phố, ≤ 60 km cho vùng.
8. **Kiếm tiền (§7):** theo hướng dẫn quảng cáo YouTube, video giáo dục về chiến tranh **không đồ hoạ** được đủ quảng cáo; xác chết rõ thương tích trong bối cảnh giáo dục chỉ được quảng cáo hạn chế; footage chiến tranh có thương tích/cái chết rõ thì **không quảng cáo trong mọi bối cảnh**. Hình 3D tự dựng không phải AI nên **không bắt buộc nhãn nội dung tổng hợp**, nhưng nên ghi rõ trong mô tả về giọng đọc tổng hợp.
9. **Chi phí thật:** YouTube **2 124/3 000 đơn vị**; Claude API **$0**; ElevenLabs **0**; giờ máy **≈ 0,1 h**; WebSearch/WebFetch 8 lượt.

### Bảng quyết định đề xuất (chờ chủ dự án duyệt)
| # | Đề xuất | Ưu | Nhược | Tác động | Rủi ro |
|---|---|---|---|---|---|
| Q1 | **Hình thức A:** series "Contested Places" trong Moving Parts, cổng quyết định sau 3 tập lịch sử (đổi sang C nếu tập lịch sử thắng ≥ 2× về lượt xem 7 ngày × thời gian xem trung bình) | giữ 1 kênh, 1 làn; khung "vì sao nơi này quan trọng" vẫn là cơ chế Moving Parts; kênh còn non nên đổi hướng rẻ; có đường lui | lời hứa kênh hiện tại ("How places get rich") lệch một phần với chiến tranh; người đăng ký đến vì kinh tế có thể không xem | nhịp đăng không đổi; mỗi tập lịch sử thay một tập kinh tế | thuật toán lẫn hai nhóm khán giả (§2.3) → giảm bằng tiêu đề/thumbnail thống nhất theo NƠI + playlist riêng |
| Q2 | **Lời hứa series:** "Why everyone fought over this place — watch it rise, burn and rebuild, every date sourced, no AI imagery." | nói đúng thứ không ai làm (nơi đổi theo năm + chiến tranh); khớp bình luận "cảm ơn không AI"; đo được | dài; "no AI" đã có kênh khác dùng | đặt vào mô tả, đầu phim, mô tả playlist | hứa "every date sourced" buộc claims chặt hơn (+ công kiểm chứng) |
| Q3 | **T3 = Gibraltar khung vây hãm** (1704 / 1779–83 / 1941 / 2026), phát hành trước 14/12 | dữ liệu sẵn nhiều nhất; neo có ngày; dùng lại gib20 | VÀNG đầy đủ; Great Siege đã có 3 kênh lớn làm | giữ lịch T3; thêm 2 mô-đun (tuyến vây, hạm đội) | chủ quyền: luật câu chữ tiền kỳ T3 §7 áp nguyên |
| Q4 | **T4 = London 1666 (XANH)**, dự phòng Boston 1775–76 | cầu cao nhất (11 video dài ≥ 100 nghìn, Short 4,29 triệu), 0/5 video đầu có nguồn; bản đồ 1676 thuộc tài sản công | không phải chiến tranh; công số hoá phố trước 1666 lớn | đúng luật "không quá 2 VÀNG liền" | Latos/kênh khác đã làm London (nhiều kênh) → góc "cháy và dựng lại" phải rõ |
| Q5 | **V5b-2b** nhận phần tích hợp + 4 việc nhỏ; **mở phiên V6 "Chiến trường"** cho quân, hạm đội, tuyến vây, thành luỹ, khói/lửa, footprint lịch sử | tách rủi ro; V5b-2b không phình | thêm 1 phiên V | ≈ 2 h máy thử + công V | V6 xong sau T3 → T3 dùng bản rút gọn (§5.3) |
| Q6 | **Kinh thánh + luật K:** hai luật đo được ở §6 (nhà/đường ≥ 25 %, địa cầu ≤ 1 lần ≤ 3 s) | sửa đúng hai lỗi chủ dự án chỉ ra ở T2; đo bằng công cụ có sẵn | ngưỡng 25 % là đề xuất, chưa đo trên gib20/T2 | K thêm 2 mục vào checks kênh 2 | ngưỡng sai làm chặn cảnh vùng hợp lệ → K chạy thử trên T2 + gib20 trước khi khoá |
| Q7 | **Chính sách hình chiến tranh:** không xác chết, không máu, không vũ khí chĩa vào người trên thumbnail; thương vong nói bằng số + biểu tượng trung tính | giữ đủ quảng cáo theo hướng dẫn YouTube | mất một phần "cảm xúc" mà kênh cạnh tranh dùng | ghi vào Kinh thánh §4 + LUAT-NOI-DUNG-G | bị "quảng cáo hạn chế" nếu footage lưu trữ có thi thể → chặn bằng kiểm footage |

**Chỉ số trong ±5 % quanh ngưỡng (nêu tên):**
- Ngưỡng 100 nghìn lượt (video dài): British History — Great Siege Gibraltar **101 524** (+1,5 %); Battle Chronicles — Malta **102 930** (+2,9 %); War Stories — Malta **99 167** (−0,8 %); Little Wars TV — Vicksburg **102 011** (+2,0 %). Số video "≥ 100 nghìn" của Gibraltar (5), Malta (17), Vicksburg (9) vì vậy có thể dao động ±1 tuỳ ngày đo.
- Ngưỡng 500 nghìn: Brian M — London 1666 (đăng lại phim truyền hình) **517 230** (+3,4 %) → London có thể là 3 hoặc 4 video ≥ 500 nghìn.
- Đề xuất luật §6 chưa có số đo nên chưa xét được vùng ±5 %.

**Việc chờ chủ dự án:** §12.

---

## 1. Thị trường

### 1.1 Cách đo
- `channels.list` (forHandle/id) → `playlistItems.list` 50 upload mới nhất → `videos.list`. "Dài" > 180 s ở bảng kênh; ≥ 480 s ở bảng đề tài. **Nhịp** = số video dài trong 50 upload mới nhất chia khoảng ngày giữa video dài cũ nhất và mới nhất (tự tính; kênh đăng thưa thì cửa sổ dài vài năm).
- **Trung vị lượt xem** của 10 video dài gần nhất, đọc 17/10/2026. Video mới vài ngày kéo trung vị xuống, nên chỉ dùng để so cỡ.
- **"Ghi nguồn"** = mô tả có mục Sources/Bibliography/References (regex). **Đây là dấu hiệu, không phải kiểm chứng**: có kênh dẫn nguồn ở bình luận ghim hoặc trang Patreon mà regex không thấy.
- **Hình thức hình** do phiên phân loại từ tiêu đề, mô tả và hiểu biết chung về kênh. Đây **không phải số API**, sai số có thể có ở kênh ít xem.
- 4 lượt `search.list` tìm kênh mới cùng dạng ("siege timelapse 3D map", "battle explained 3D animated map" từ 17/04/2026, "how the city changed over time…", "history documentary biography" từ 17/04/2026).
- Bảng đầy đủ 39 kênh: `reports/nc-lich-su/kenh.csv`.

### 1.2 (a) Lịch sử chiến tranh / bản đồ trận đánh
| Kênh | Sub | Video | Dài/tuần | Trung vị 10 dài | Dài TV (phút) | Mô tả có nguồn /10 | Hình thức |
|---|---|---|---|---|---|---|---|
| Kings and Generals | 4,21 tr | 2 262 | **3,04** | 356 737 | 19,8 | 6 | 2D bản đồ hoạt hình + tranh vẽ tay |
| Yarnhub | 3,36 tr | 368 | 0,51 | **6 276 551** | 17,6 | 7 | hoạt hình 3D CGI (máy bay, tàu, xe tăng) |
| Epic History | 3,19 tr | 380 | 0,38 | 992 712 | 34,5 | 1 | bản đồ 2D + tranh PD; loạt "in 3D" từ 2025–26 |
| The Armchair Historian | 2,54 tr | 335 | 0,57 | 401 807 | 17,8 | 9 | hoạt hình 2D nhân vật + bản đồ |
| Mark Felton Productions | 2,43 tr | 1 009 | 1,78 | 446 806 | 12,3 | 2 | ảnh/footage lưu trữ + tài liệu gốc |
| The Great War | 1,89 tr | 798 | 0,21 | 253 840 | 22,7 | **10** | footage lưu trữ + bản đồ 2D; cam kết không AI tạo sinh |
| Invicta | 1,67 tr | 1 512 | 0,62 | 74 794 | 33,2 | 5 | tranh/bản đồ + người dẫn |
| The Operations Room | 1,45 tr | 213 | 0,47 | 399 704 | 39,8 | 0 | bản đồ vệ tinh/3D chiến thuật, ký hiệu quân sự |
| HistoryMarche | 1,34 tr | 378 | 0,71 | 268 251 | 29,5 | **10** | bản đồ 2D + tranh |
| World War Two (TimeGhost) | 1,19 tr | 1 345 | 1,18 | 127 843 | 20,2 | 4 | footage + bản đồ 2D |
| Historia Civilis | 1,09 tr | 89 | 0,10 | **1 442 237** | 38,3 | **10** | đồ hoạ tối giản + bản đồ |
| Real Time History | 760 nghìn | 80 | 0,34 | 418 562 | 34,7 | **10** | bản đồ 2D + ảnh lưu trữ; cam kết không AI tạo sinh |
| BazBattles | 725 nghìn | 90 | 0,12 | 105 904 | 10,9 | 0 | bản đồ 2D chiến thuật |
| Historigraph | 530 nghìn | 140 | 0,25 | 184 312 | 12,4 | 5 | bản đồ 2D + footage |
| **SandRhoman History** | 527 nghìn | 156 | 0,40 | 139 590 | 28,7 | 9 | bản đồ 2D + tranh PD — **chuyên vây hãm**, có mặt ở 7/15 đề tài của §3 |
| American Battlefield Trust | 511 nghìn | 1 640 | 2,78 | 21 114 | 14,0 | 0 | bản đồ trận đánh hoạt hình + người dẫn tại chiến trường |
| History Mapped Out | 182 nghìn | 145 | 0,86 | 84 862 | 27,3 | 0 | bản đồ 2D hoạt hình |

### 1.3 (b) Nhân vật lịch sử / tiểu sử / sự kiện
| Kênh | Sub | Video | Dài/tuần | Trung vị 10 dài | Dài TV | Nguồn /10 | Hình thức |
|---|---|---|---|---|---|---|---|
| OverSimplified | 9,66 tr | 33 | 0,07 | **35 743 292** | 30,5 | 0 | hoạt hình 2D nhân vật |
| Timeline – World History Doc. | 5,90 tr | 1 491 | 5,04 | 31 390 | 26,2 | 0 | phim tài liệu truyền hình đăng lại |
| Weird History | 4,73 tr | 1 161 | 2,47 | 80 404 | 47,1 | 0 | minh hoạ hoạt hình + ảnh |
| Extra History | 4,62 tr | 1 364 | 1,11 | 355 930 | 21,3 | 0 | hoạt hình 2D |
| Absolute History | 3,70 tr | 1 131 | 2,92 | 19 840 | 51,8 | 0 | phim tài liệu truyền hình đăng lại |
| Biographics | 2,44 tr | 825 | 0,85 | 12 151 | 24,2 | 9 | ảnh/footage + người dẫn (video gần nhất 30/04/2026) |
| History Hit | 2,01 tr | 844 | 2,13 | 211 797 | 42,4 | 0 | người dẫn tại hiện trường + footage |
| History Matters | 1,92 tr | 397 | 0,48 | 623 833 | **8,9** | 0 | hoạt hình 2D đơn giản, câu hỏi "Why did…" |
| Fall of Civilizations | 1,52 tr | 47 | 0,11 | 1 592 997 | 271,8 | 7 | tranh/ảnh + giọng đọc rất dài |
| Fascinating Horror | 1,46 tr | 466 | 1,05 | 616 142 | 11,4 | **10** | đồ hoạ tĩnh + ảnh lưu trữ (thảm hoạ) |
| Voices of the Past | 1,09 tr | 193 | 0,23 | 751 832 | 29,5 | 1 | tranh PD + đọc nguồn sơ cấp (video gần nhất 30/07/2025) |
| toldinstone | 652 nghìn | 253 | 0,51 | 157 288 | 10,2 | 0 | người dẫn + ảnh di tích |

### 1.4 (c) Timelapse thành phố / bản đồ lịch sử
| Kênh | Sub | Video | Dài/tuần | Trung vị 10 dài | Dài TV | Nguồn /10 | Mô tả nhắc AI /10 | Hình thức |
|---|---|---|---|---|---|---|---|---|
| UsefulCharts | 2,09 tr | 303 | 0,70 | 118 203 | 18,3 | 0 | 0 | đồ thị/bản đồ + người dẫn |
| History Scope | 571 nghìn | 89 | 0,14 | 141 571 | 49,3 | 9 | 0 | bản đồ 2D kinh tế–lịch sử |
| EmperorTigerstar | 570 nghìn | 907 | 0,71 | 74 297 | 7,7 | 7 | 1 | bản đồ biên giới theo năm/ngày |
| History on Maps | 417 nghìn | 214 | 0,41 | 138 141 | **3,7** | 1 | 0 | bản đồ 2D "every day" |
| mapsinanutshell | 394 nghìn | 483 | 0,91 | 38 596 | 8,0 | **10** | 0 | Google Earth + đơn vị theo ngày (gồm xung đột đang diễn ra) |
| Ollie Bye | 377 nghìn | 145 | 0,09 | 355 260 | 5,8 | 0 | 0 | bản đồ biên giới theo năm |
| **Matt Reconstructs History** | 112 nghìn | 22 | 0,49 | 125 638 | 30,3 | 1 | **6** | tái dựng thành phố bằng ảnh AI + then/now |
| Latos Charts | 100 nghìn | 15 | 1,51 | 445 289 | 10,2 | 0 | 0 | thành phố mọc 3D, máy cao |
| **Restored Timeline** | 64,5 nghìn | 31 | 0,64 | 77 070 | 14,1 | 0 | **10** | máy cố định, ảnh AI theo thời kỳ |
| Charles Reconstructs | 3,8 nghìn | 23 | 3,35 | 6 013 | 11,0 | 0 | **10** | tái dựng thành phố bằng ảnh AI (đã làm Leiden 1574, Antwerp 1560) |

**Đọc ba bảng:**
1. **Hình 2D phẳng + tranh là chuẩn của ngách chiến tranh.** 3D chỉ xuất hiện ở Yarnhub (vật thể quân sự, không phải nơi chốn), The Operations Room (bản đồ chiến thuật) và loạt "in 3D" mới của Epic History. **Không kênh nào dựng thành phố/thành luỹ thay đổi theo năm quanh một trận.**
2. **Kênh có nguồn thắng ở dạng dài**: Historia Civilis, Real Time History, HistoryMarche, The Great War đều 10/10. Nguồn là **chuẩn vệ sinh** của ngách này, không phải khác biệt.
3. **Thời lượng không có một chuẩn**: từ 3,7 phút (History on Maps) tới 272 phút (Fall of Civilizations). Kênh thắng có trung vị 9–40 phút. Phù hợp với kết luận Teardown: độ dài không phải đòn bẩy.
4. **Nhịp đăng**: kênh lớn nhất trong (a) đăng 3 video dài/tuần (Kings and Generals, có đội ngũ), nhưng nhiều kênh thắng đăng ≤ 0,5/tuần (Yarnhub 0,51, Epic History 0,38, Historia Civilis 0,10). **Ngách này thưởng chất lượng hơn nhịp**, khác ngách kinh tế–địa lý của Teardown (kênh thắng ≥ 2/tuần). Đây là tin tốt cho 1 làn sản xuất.
5. **Kênh mới tìm thấy qua search:** các video ≥ 1 triệu ở dạng **Short bản đồ 2D/Google Earth** (AlternativeGeopoliticsMapped, mapsinanutshell, History on Maps, một số kênh Short) và dạng **Short AI** (itsaihistory lập 11/10/2025: 3,9 triệu một Short; Timeline History lập 06/2025: 3,0 triệu). Ở dạng dài, kênh mới < 12 tháng thắng lớn **rất ít**: chỉ Matt Reconstructs (AI) và British History (một video 101 nghìn, các video khác ~1 nghìn).

### 1.5 Bình luận: khán giả xin gì, chê gì (8 video, 776 bình luận hàng đầu)
Nhãn bằng regex + phiên đọc tay (không gọi API). Trọng số = 1 + like. Chi tiết số: `binh-luan-tom-tat.json`. Ý dưới đây **diễn đạt lại**, không chép nguyên văn.

| Video (kênh, lượt) | Phát hiện |
|---|---|
| Epic History — Verdun 3D (336 nghìn) | **Giọng đọc chiếm 40,6 % trọng số like** (hai bình luận lớn nhất khen người dẫn). Bình luận gắn với nơi chốn/gia đình ("bố tôi quê Verdun", "ông tôi bị bắt ngày đầu") chiếm **11,4 %**. Xin đề tài: Brusilov, Somme. Một bình luận chỉ thiếu vai trò tướng Castelnau |
| Epic History — Copenhagen 1801 3D (708 nghìn) | khen hình 5,9 %; nhiều "fun fact" (thuật ngữ "turn a blind eye"; người Đan Mạch gỡ phao luồng) → khán giả thích **chi tiết gắn với địa hình nơi đó** |
| Matt Reconstructs — Boston 1700s, AI (468 nghìn) | **AI chiếm 28 % trọng số** (cả khen "dùng AI đúng chỗ" lẫn đặt câu hỏi); **gắn với nơi chốn/gia đình 34,2 %** ("gia đình tôi tới Boston năm 1640"); một hướng dẫn viên Boston liệt kê lỗi sự kiện; khán giả **xin lặp lại đoạn then/now**, khen ảnh hiện đại của toà nhà; xin Charleston, Chicago 1893 |
| Restored Timeline — Los Angeles, AI (1,83 triệu) | lỗi AI bị chế giễu: một nhà hát **đổi bên đường** giữa các thời kỳ (183 like), xe hơi ở năm 8000 TCN, tàu điện đặt sai trước ga. Một người hiểu bố cục lịch sử chỉ ra kiến trúc sai |
| SandRhoman — Great Siege Gibraltar (622 nghìn) | bình luận chủ yếu là chi tiết vui về kỹ thuật vây (đạn chùm Shrapnel, lò nung đạn đỏ), **câu hỏi về hậu cần** (thuốc súng, đạn dự trữ bao nhiêu); một người Gibraltar khen chi tiết; vai trò Tây Ban Nha trong độc lập Mỹ |
| Kings and Generals — Great Siege Gibraltar (284 nghìn) | xin thêm vai Pháp–Tây Ban Nha trong chiến tranh độc lập Mỹ (11,2 % trọng số); gợi ý thăm "Great Siege Tunnels"; **một bình luận gây chuyện về Ceuta/Melilla** → bật lọc bình luận như tiền kỳ T3 |
| History Mapped Out — Great Siege Malta (380 nghìn) | **sửa sai 18,5 % trọng số** — cao nhất mẫu: người Malta chỉ ra **Birgu có thành luỹ, khác với video**; chê thiên vị tôn giáo trong cách gọi tù binh; một người khen giữa "thời video lịch sử AI giả" → **thành luỹ vẽ sai là lỗi bị người địa phương bắt ngay** |
| The Operations Room — Pearl Harbor 2/3 (782 nghìn) | "cảm ơn vì không phải AI" **296 like** (lớn thứ 3 video); sửa sai chi tiết tàu/thời điểm 4,7 % |

**Khoảng trống (tổng hợp §1.2–§1.5):**
1. **Thứ khán giả xin mà chưa ai làm tốt:** (i) thấy **nơi đó thật sự trông thế nào** lúc trận đánh, và đổi ra sao tới hôm nay (then/now) — hiện chỉ kênh AI đáp ứng, và bị bắt lỗi; (ii) **hậu cần và kỹ thuật vây** (đạn, lương thực, đường hầm, lò nung) gắn với địa hình; (iii) **người địa phương nhận ra phố nhà mình** — loại bình luận có trọng số lớn ở 4/8 video.
2. **Chỗ đối thủ bị chê sai lịch sử:** thành luỹ/bố cục phố sai (Malta, Boston), sai thời đại do AI (Los Angeles), thiên vị tôn giáo trong cách gọi (Malta), thiếu nhân vật phụ quan trọng (Verdun). Dạng timelapse thành phố (R&D Timelapse §1.3) có 9–21 % bình luận chỉ lỗi lịch sử.
3. **Rủi ro phía mình:** giọng đọc là yếu tố được khen nhiều nhất ở Epic History. Giọng ElevenLabs bị khán giả FoN chê (Teardown §3). → §8 đặt chỉ số đo giọng riêng.

---

## 2. Định vị

### 2.1 Ba lời hứa đề xuất (tiếng Anh, để chọn)
| # | Lời hứa | Dùng cho | Ưu | Nhược |
|---|---|---|---|---|
| L1 (đề xuất) | **"Why everyone fought over this place — watch it rise, burn and rebuild. Every date sourced. No AI imagery."** | series trong Moving Parts (A) | giữ câu hỏi "vì sao nơi này" của kênh; nói rõ hình thức timelapse | dài; cần rút gọn cho banner |
| L2 | "Battles and turning points, seen from the place itself — every date sourced, no AI imagery." | kênh riêng (B) hoặc đổi hướng (C) | đúng ví dụ của chủ dự án; rõ thể loại chiến tranh | không nói "mọc theo thời gian", dễ lẫn với kênh bản đồ 2D |
| L3 | "History you can stand on: the real streets, the real walls, the real dates." | khẩu hiệu ngắn, banner/Short | ngắn, nhớ được; nhấn "thật" đối lập AI | không nói chiến tranh; "real" cần chứng minh từng tập |

Ba lợi thế khó chép (đều đã có một phần trong nhà máy): **(1) nơi chốn đúng năm** (sổ đăng ký toà + bản đồ pha + ghost có ghi nguồn, R&D Timelapse §2); **(2) hồ sơ thật** (claims có trích nguyên văn, tiền kỳ T3); **(3) cú máy liên hoàn** từ phố xuống hero rồi reveal (V5b-2a) — kênh 2D không có, kênh AI không giữ được nhất quán hình học.

### 2.2 So sánh ba hình thức (1 làn sản xuất)
| | (A) Series trong Moving Parts | (B) Kênh 3 riêng | (C) Đổi hướng toàn bộ Moving Parts |
|---|---|---|---|
| Ưu | 1 kênh, 1 bộ nhận diện; khung "vì sao nơi này được tranh giành" = lăng kính hạ tầng/thương mại của Kinh thánh (eo biển, cảng, sông); có đường lui; T3 Gibraltar vốn đã là "nơi bị tranh giành" | lời hứa sạch, khán giả không lẫn; tên kênh có thể chứa "history" (tìm kiếm) | một lời hứa duy nhất; toàn bộ công lực vào thể loại cầu lớn hơn (§1); kênh còn non nên giá đổi thấp |
| Nhược | lời hứa "How places get rich" lệch một phần; khán giả kinh tế có thể không bấm tập chiến tranh | khởi động lạnh từ 0; nhịp mỗi kênh còn ~½; hai bộ nhận diện, hai luồng đóng gói, hai bộ luật K | bỏ phần kinh tế đã đầu tư (Teardown, T1/T2); nếu thể loại lịch sử thất bại thì mất cả hướng cũ |
| Nhịp đăng (1 làn, ~1 tập/1–2 tuần **(ước)**) | không đổi; xen kẽ hoặc chuỗi 3 tập liền | mỗi kênh ~1 tập/2–4 tuần → dưới mức kênh thắng trong mẫu Teardown | không đổi |
| Rủi ro thuật toán | khán giả lẫn: tập chiến tranh được giới thiệu tới người xem kinh tế (CTR thấp lúc đầu) → giảm bằng **mỗi tập vẫn là một NƠI có tên trên tiêu đề + thumbnail cùng ngữ pháp bản đồ**, playlist riêng, chuỗi 3 tập liền để thuật toán học nhóm mới | thấp về lẫn khán giả; cao về khởi động (kênh mới ít tín hiệu) | thấp sau giai đoạn chuyển; người đăng ký cũ ít nên ảnh hưởng nhỏ |
| Tác động | giữ T3 đúng lịch; quyết định cuối sau 3 tập có số liệu thật | trễ T3 (tạo kênh, nhận diện); tốn thêm một phiên đóng gói | cần sửa Kinh thánh §1 ngay; đổi tên/banner |

**Đề xuất: (A) + cổng quyết định.** Sau 3 tập lịch sử (Gibraltar, London 1666, Boston/Vicksburg) so với tập kinh tế (T1, T2): nếu **lượt xem 7 ngày × thời gian xem trung bình** của nhóm lịch sử ≥ 2× nhóm kinh tế → đổi sang (C), đổi lời hứa thành L1/L2. Nếu ngược lại → giữ (A) ở tỷ lệ 1 tập lịch sử / 2 tập. **(B) chỉ xét khi có làn sản xuất thứ hai.** Lưu ý: tôi không có số liệu kênh Moving Parts đã phát hành (T2 còn chờ G2), nên mọi so sánh với "khán giả hiện có" là **(ước)**.

### 2.3 Rủi ro khán giả lẫn lộn (cụ thể)
- Teardown đo: khán giả FoN đến để **cãi nguyên nhân kinh tế**; mẫu §1.5 cho thấy khán giả chiến tranh đến vì **giọng kể, chi tiết, gắn bó nơi chốn**. Hai nhóm khác động cơ.
- Cầu nối có thật: Gibraltar (eo biển), Antwerp → Amsterdam (dòng tiền dời đi khi Scheldt bị chặn), Vicksburg (sông Mississippi là đường thương mại), Boston (cảng + đất lấn). → **Chọn đề tài có "vì sao nơi này có giá" trong cùng một câu** để giữ một lời hứa.

---

## 3. Đề tài: 15 ứng viên

### 3.1 Cách đo cầu
Mỗi đề tài **1 lượt `search.list` riêng** (type=video, relevance, 50 kết quả, en/US, không giới hạn ngày) + `videos.list`. Dài ≥ 8 phút. Số đầy đủ: `de-tai-cau.json`; điểm: `cham-diem.json`. Thước /25 theo tiền kỳ thành phố, đổi tiêu chí 3 thành **dữ liệu timelapse** và tiêu chí 4 thành **bản đồ + tranh/ảnh có quyền**.

**Cảnh báo mẫu:** search trả cả video lạc đề. Đã loại tay: Zürich (video lớn nhất 1,08 triệu là trận Zenta 1697, đúng đề tài lớn nhất chỉ 27 686); Copenhagen (2,35 triệu là trận Eylau; đúng đề tài: 1801 708 nghìn, 1807 chỉ 61 338); Boston (15,9 triệu là marathon 3 giờ cả cách mạng Mỹ; đúng đề tài: Bunker Hill + vây Boston 758 nghìn, Boston 1700s AI 468 nghìn).

### 3.2 Bảng cầu (đọc 17/10/2026)
| Đề tài | Video dài | Dài lớn nhất (đúng đề tài) | Dài ≥ 100 k | Dài ≥ 500 k | Short lớn nhất | Dài trong 90 ngày | Top 5 có nguồn | Kênh lớn đã làm |
|---|---|---|---|---|---|---|---|---|
| Gibraltar (các cuộc vây) | 18 | 679 190 | 5 ⚠ | 2 | 6 259 072 | 3 (lớn nhất 101 524 ⚠) | 2/5 | Geographics, SandRhoman, Kings and Generals |
| Malta 1565 | 33 | 1 339 746 | 17 ⚠ | 3 | 157 950 | 4 (380 088) | 1/5 | Kings and Generals, SandRhoman, History Hit, Drachinifel |
| Vicksburg 1863 | 29 | 2 335 925 | 9 ⚠ | 3 | 2 523 819 | 3 (377 983) | 1/5 | HISTORY, Am. Battlefield Trust, Kings and Generals |
| Quebec 1759 | 23 | 698 675 | 6 | 1 | 5 326 | 2 | 2/5 | Extra History, History Hit, SandRhoman |
| Louisbourg 1745/58 | 14 | 230 649 | 1 | 0 | 2 571 | 2 (rất nhỏ) | 2/5 | SandRhoman |
| Leiden 1574 | 15 | 233 690 | 3 | 0 | 332 833 | 3 (rất nhỏ) | 1/5 | SandRhoman; Charles Reconstructs (AI) |
| Antwerp 1584–85 | 12 | 269 101 | 1 | 0 | 30 651 | 1 | 1/5 | SandRhoman; Charles Reconstructs (AI, 1560) |
| Rotterdam 1940 | 18 | 151 204 | 1 | 0 | 204 959 | 0 | 1/5 | TIKhistory (76 nghìn); kênh ảnh tô màu (AI) |
| Boston 1775–76 | 15 | 757 931 (đúng đề tài) | 8 (gồm phim tổng về cách mạng Mỹ) | 4 (như trên) | 107 187 | 2 | 1/5 | Epic History, Kings and Generals, Matt Reconstructs (AI) |
| Paris 1870–71 | 15 | 4 436 944 | 5 | 3 | 4 694 467 | 2 | **4/5** | Armchair Historian, Real Time History, Geographics |
| Halifax 1917 | 27 | 2 689 134 | 14 | 4 | 800 205 | 1 | **0/5** | Fascinating Horror, Scary Interesting, Casual Navigation |
| London 1666 | 23 | 2 454 899 | 11 | 4 ⚠ | 4 287 226 | 1 | **0/5** | Absolute History, Weird History, phim truyền hình đăng lại |
| Copenhagen 1807 | 11 | 61 338 (1807); 708 472 (1801) | 2 (cả hai về 1801) | 1 (1801) | 73 173 | 1 | 0/5 | Epic History (1801, 3D), The History Guy |
| Vienna 1683 | 29 | 2 439 196 | **20** | **13** | 5 118 725 | 0 | 2/5 | Extra History, SandRhoman, Kings and Generals |
| Zürich 1799 | 27 | 27 686 (đúng đề tài) | 0 (1 video lạc đề) | 0 (1 lạc đề) | 5 079 | 1 | 1/5 | Cannons Fire (nhỏ) |
⚠ = có video sát ngưỡng ±5 % (§0).

### 3.3 Mười lăm đề tài (xếp theo điểm)
Ký hiệu cột "Dữ liệu timelapse": nguồn **đã kiểm trong repo** ghi rõ; còn lại là **(chưa kiểm)** — cần phiên tiền kỳ tải và đọc giấy phép từng tệp.

| # | Nơi · sự kiện · nhân vật | "Why" một câu (EN) | Nơi đổi ra sao theo thời gian | Dữ liệu timelapse · tư liệu PD | Hero cần dựng | Mức | Kênh lớn đã làm? | /25 |
|---|---|---|---|---|---|---|---|---|
| 1 | **London · Great Fire 2–6/9/1666 · Samuel Pepys, Christopher Wren, Charles II** | *Why did a city that burned to the ground rebuild on almost exactly the same streets?* | thành phố gỗ trong tường La Mã → cháy 4 ngày → dựng lại bằng gạch (Rebuilding Act 1667) trên lưới phố cũ → St Paul's mới 1675–1710 → Blitz 1940 lại cháy vùng gần như trùng | bản đồ Ogilby & Morgan 1676 và "Agas" (PD theo tuổi; kiểm từng bản quét), khắc Hollar (CC0 qua Rijksmuseum/The Met **(chưa kiểm từng mục)**); Historic England listing (OGL, năm theo toà cho toà còn đứng **(chưa kiểm)**); footprint trước 1666 phải **ghost** | Old St Paul's → St Paul's của Wren; The Monument; Pudding Lane; tường thành; London Bridge có nhà | XANH | Có, nhưng dạng phim truyền hình/minh hoạ, 0/5 có nguồn; không ai dựng phố cháy–dựng lại theo năm | **21** |
| 2 | **Boston · Siege 1775–76 · George Washington, Henry Knox, William Howe** | *Why could the British hold Boston for eleven months, then lose it in one night?* | bán đảo nhỏ nối đất liền bằng eo Boston Neck → cao điểm Dorchester bị chiếm đêm 4–5/3/1776 → **Boston lấn biển gấp nhiều lần** (Back Bay, South End thế kỷ 19) | sổ thuế Boston có `YR_BUILT` (Analyze Boston, **PDDL** — đã kiểm giấy phép bộ dữ liệu, chưa đo độ dồn năm); bản đồ Leventhal Map Center (nhiều mục "no known restrictions", bản trước 1923 được nói là PD — **kiểm từng mục**); bản đồ LoC 1775–76 (PD) | Boston Neck + chiến luỹ; Dorchester Heights; Old State House; cảng/Long Wharf | XANH | Có (Epic History, K&G trong phim tổng; Matt Reconstructs bằng AI). Không ai cho thấy đất lấn + vây cùng một trục thời gian | **20** |
| 3 | **Vicksburg · Siege 18/5–4/7/1863 · Ulysses S. Grant, John C. Pemberton** | *Why was a bluff town on a river bend worth more than Gettysburg — and why did the river leave it thirteen years later?* | thành phố trên vách sông → hào vây 47 ngày, dân ở hang → **sông Mississippi tự cắt khúc uốn năm 1876** để Vicksburg xa sông → kênh Yazoo đưa nước về lại (đầu thế kỷ 20) **(ngày cắt/khánh thành chưa kiểm nguồn gốc USACE)** | bản đồ Civil War của LoC/NARA (tác phẩm chính phủ Mỹ, PD); bản đồ địa hình lịch sử USGS (PD); Sanborn LoC (PD; **năm sớm nhất cho Vicksburg chưa tra được**); GIS chiến tuyến của NPS **(chưa kiểm)** | khúc sông De Soto; dinh toà án 1858; chiến tuyến + hầm mìn 3rd Louisiana Redan; hang dân | XANH (lưu ý tượng đài miền Nam: không bình luận, chỉ địa danh) | Có (HISTORY, ABT bản đồ hoạt hình 1,53 triệu); không ai làm "con sông bỏ đi" | **20** |
| 4 | **Vienna · Siege 14/7–12/9/1683 · Kara Mustafa, Jan III Sobieski, Ernst Rüdiger von Starhemberg** | *Why did the walls that saved Vienna in 1683 have to be torn down for the city to grow?* | thành cổ trong pháo đài + vành đất trống (glacis) → vây 1683 → glacis giữ đến 1857 → Ringstraße thay tường | Wien OGD (CC BY 4.0) giai đoạn xây theo toà (R&D: 19 % năm chính xác, còn lại theo giai đoạn); bản đồ lịch sử Wien Kulturgut **(giấy phép CC BY — cần kiểm lại)**; Huber 1769–74 (PD theo tuổi) | bastion + glacis; St. Stephen; Ringstraße | **VÀNG** (khung "Kitô giáo vs Hồi giáo", ngày 11/9 bị cực hữu dùng làm biểu tượng) | **Rất dày** (13 video ≥ 500 nghìn); Latos đã làm Vienna timelapse 13/10 | 20 |
| 5 | **Gibraltar · 1704 / Great Siege 1779–83 / 1940s · George Rooke, George Augustus Eliott, (1941) kỹ sư Hoàng gia** | *Why has everyone fought over this rock — fourteen sieges, and a runway built on no-man's-land?* | phố trong tường 1704 → phố bị bắn cháy 1781, Great Siege Tunnels 1782 → eo đất trung lập → đường băng 1941 lấn vịnh → 2026 | **đã có:** tiền kỳ T3 (44 claim, 28 tài sản, 38 giấy phép: Rijksmuseum CC0 chiếm 1704, LoC 1705, The Met CC0 Trumbull/Copley Great Siege, LoC "Neutral ground" 1900–10, Copernicus, Sentinel-2, PNOA CC BY), gib20 (V5b-2a); thiếu: năm theo toà phía Gibraltar (chỉ mốc + ghost), footprint OSM (ODbL) | Rock + vách bắc; King's Bastion; Great Siege Tunnels; đường băng 1941; cổng biên giới | **VÀNG** đầy đủ | Có (Geographics 14 sieges 679 nghìn; SandRhoman 622 nghìn; K&G 284 nghìn) | 19 |
| 6 | **Rotterdam · bombing 14/5/1940 · (thị trưởng P. J. Oud; kiến trúc sư W. G. Witteveen — kế hoạch tái thiết)** | *Why does the centre of a 700-year-old city look brand new?* | phố cổ dày đặc → một buổi chiều lõi trung tâm cháy → đất trống → tái thiết hiện đại; Laurenskerk + Witte Huis còn đứng | **BAG CC0 + 3DBAG CC BY** (cùng đường ống Amsterdam đã đo ở R&D): năm xây sẽ cho thấy **lỗ trống 1940** ngay trong dữ liệu; ảnh Stadsarchief Rotterdam **(giấy phép chưa kiểm)**; bản đồ Kadaster lịch sử **(chưa rõ, R&D §2)** | Laurenskerk; Witte Huis; Coolsingel; cầu Erasmus | XANH | Không có video dài tiếng Anh lớn (lớn nhất 151 nghìn, ảnh tô màu AI) | 19 |
| 7 | **Zürich · Hai trận Zürich 6/1799 và 9/1799 · André Masséna, Alexander Korsakov, Alexander Suvorov** | *Why did three empires' armies fight over a Swiss toll town in one summer?* | thành phố trong thành luỹ thế kỷ 17 → chiến trường 1799 → phá luỹ từ 1833 → mở rộng 1893 | **đã kiểm (tiền kỳ thành phố):** GWR 100 % có năm; **Zürich 4D CC0 mốc 1800 (5 688 toà)**; 8 lớp bản đồ có quyền thương mại | thành luỹ 1642–1830; Limmat; Grossmünster | XANH | Không (lớn nhất 27 nghìn) | 19 |
| 8 | **Halifax · Explosion 6/12/1917 · Vince Coleman (điều độ đường sắt), thuyền trưởng Mont-Blanc** | *Why did the worst man-made blast before the atomic age happen in a harbour town in Canada?* | cảng thời chiến đông tàu → vụ nổ xoá khu Richmond → khu Hydrostone dựng lại | bản đồ bảo hiểm/thành phố 1917 **(quyền Canada chưa kiểm)**; ảnh lưu trữ Nova Scotia **(điều khoản chưa kiểm)**; dữ liệu mở Halifax **(chưa rõ có năm xây)** | eo Narrows; khu Richmond; Hydrostone | XANH (thảm hoạ: không ảnh thi thể) | Có (Fascinating Horror 2,69 triệu…), **0/5 có nguồn**, dạng "kinh dị" | 18 |
| 9 | **Malta · Great Siege 18/5–11/9/1565 → Valletta 1566 → vây 1940–42 · Jean de Valette, Dragut** | *Why did a siege build a city — and why did the same harbour get besieged again 377 years later?* | Birgu/Senglea có luỹ → Fort St Elmo thất thủ → **Valletta xây từ 1566 trên bán đảo trống** → bom 1942 | tranh/khắc PD (Rijksmuseum/LoC **(chưa kiểm)**); sơ đồ luỹ của Hiệp sĩ (PD theo tuổi); dữ liệu nhà Malta **(chưa kiểm)** | Fort St Elmo, Fort St Angelo, lưới phố Valletta, Grand Harbour | **VÀNG** (khung tôn giáo; bình luận đã thấy tranh cãi) | **Dày** (17 video ≥ 100 nghìn) | 18 |
| 10 | **Paris · Siege 9/1870–1/1871 · Bismarck, Moltke, Léon Gambetta (thoát bằng khinh khí cầu)** | *Why did the world's grandest new city need balloons to talk to France?* | Paris Haussmann + tường Thiers 1841–44 + vòng pháo đài → vây, khinh khí cầu, ăn thú vườn bách thú → Công xã | APUR năm xây theo toà **(giấy phép chưa kiểm)**; bản đồ Gallica phải trả phí (R&D) → dùng bản in khác PD | tường Thiers + pháo đài; Montmartre; ga xuất phát khinh khí cầu | XANH (Công xã: hai phía) | Có, dạng toàn chiến tranh; **4/5 có nguồn** | 18 |
| 11 | **Louisbourg · Sieges 1745 và 1758 · James Wolfe, Jeffery Amherst** | *Why did France spend a fortune on a fortress it lost twice — and why did Canada rebuild it 200 years later?* | pháo đài sao xây 1720s → thất thủ 1745 → trả lại 1748 → thất thủ 1758 → phá 1760 → tái dựng một phần từ thập niên 1960 | sơ đồ pháo đài Pháp thế kỷ 18 (PD theo tuổi; lưu trữ LAC/ANOM **(chưa kiểm)**); Parks Canada | pháo đài + cảng + "mọc–sập–dựng lại" | XANH | Ít (lớn nhất 231 nghìn, SandRhoman) | 18 |
| 12 | **Quebec · Plains of Abraham 13/9/1759 · Wolfe, Montcalm** | *Why did a cliff decide who would own Canada?* | thành phố trên vách + tường → vây và bắn phá mùa hè 1759 → leo vách Anse-au-Foulon → Citadelle 1820–50 | bản đồ LoC/LAC (PD theo tuổi **(chưa kiểm từng mục)**); dữ liệu mở Ville de Québec **(chưa rõ năm xây)** | vách đá; tường; Citadelle | XANH | Có (Extra History 699 nghìn, History Hit) | 17 |
| 13 | **Leiden · Siege 1573–74 · William of Orange, Louis de Boisot** | *Why did the Dutch drown their own land to save a city?* | thành phố trong kênh/tường → phá đê, nước tràn polder → giải vây 3/10/1574 → đại học 1575 | **BAG CC0 + AHN độ cao + đường ống R&D Amsterdam**; khắc Rijksmuseum CC0 **(chưa kiểm từng mục)** | đê + polder ngập; Burcht; tường | XANH | SandRhoman 234 nghìn; Charles Reconstructs (AI) | 17 |
| 14 | **Antwerp · Siege 1584–85 · Alessandro Farnese (Parma), Federico Giambelli (tàu lửa)** | *Why did one bridge across the Scheldt make Amsterdam rich?* | Antwerp cảng giàu nhất → Parma xây cầu chặn sông → thất thủ 17/8/1585 → thương nhân dời đi → Amsterdam mọc | khắc cầu Parma (Rijksmuseum CC0 **(chưa kiểm)**); phía Amsterdam: dữ liệu đã đo ở R&D (BAG/3DBAG); phía Antwerp: năm xây Flanders **(chưa kiểm)** | cầu phao chặn Scheldt; thành luỹ; cảng | XANH | SandRhoman 269 nghìn | 17 |
| 15 | **Copenhagen · Bombardment 2–5/9/1807 · Arthur Wellesley, Lord Cathcart** | *Why did Britain shell a neutral capital to steal its fleet?* | thành phố trong tường + Holmen → bắn phá 3 đêm, tháp Vor Frue sập → giao hạm đội | dữ liệu năm xây Đan Mạch (BBR) + Copenhagen CC BY (R&D: chưa đo dồn); bản đồ lịch sử Đan Mạch **(giấy phép chưa rõ, R&D)** | tháp Vor Frue; Holmen; pháo đài Trekroner | XANH | Epic History làm 1801 (3D, 708 nghìn); 1807 chỉ 61 nghìn | 17 |

**Dự phòng ngoài 15:** Cádiz 1810–12 (Cortes 1812), Yorktown 1781, Syracuse 213–212 TCN (Archimedes), Cartagena de Indias 1741 (Blas de Lezo — VÀNG nhẹ vì tranh cãi dân tộc chủ nghĩa), Dunkirk 1940 (ảnh hàng không lịch sử IGN — giấy phép Etalab **(chưa kiểm)**), Sveaborg/Helsinki 1808 (8 lớp CC BY 4.0 đã kiểm).

**Loại (`cham-diem.json` → `loai_khoi_danh_sach`):** Sevastopol/Crimea (ĐỎ — chủ quyền đang tranh chấp, xung đột đang diễn ra); Stalingrad/Leningrad (VÀNG/ĐỎ, đã bị làm dày); Constantinople 1453 (điểm nóng Hy Lạp–Thổ, tôn giáo); Derry 1689 (giáo phái Bắc Ireland); Acre 1799/Masada/Jerusalem (ĐỎ); Dresden 1945 (số người chết bị chính trị hoá); Tenochtitlan 1521 (VÀNG, đã có kênh AI làm Mexico City).

---

## 4. Tập thử: Gibraltar khung vây hãm so với hai ứng viên tốt nhất

### 4.1 So sánh
| Tiêu chí | **Gibraltar (vây hãm 1704 → 1779–83 → 1941 → 2026)** | London 1666 | Boston 1775–76 |
|---|---|---|---|
| Độ hợp với lời hứa L1 | **rất hợp**: "14 lần bị vây" chính là "vì sao ai cũng tranh giành"; đường băng 1941 trên eo đất trung lập nối thẳng với hiệp ước 2026 | hợp ở vế "burn and rebuild"; không có "fought over" | hợp: vây + đất lấn |
| Cầu | dài lớn nhất 679 nghìn; 5 video ≥ 100 nghìn ⚠; **Short 6,26 triệu** | 2,45 triệu; 11 ≥ 100 nghìn; Short 4,29 triệu | 758 nghìn (đúng đề tài); 4 ≥ 500 nghìn |
| Khoảng trống | 3/5: Great Siege đã có 3 kênh lớn; **chưa ai nối 1704 → 1941 → 2026 trên cùng một nơi 3D** | 3/5: 0/5 có nguồn; chưa ai dựng phố | 3/5: có bản AI |
| Dữ liệu sẵn | **cao nhất:** tiền kỳ T3 đủ (44 claim, 14 nhạy cảm, 28 tài sản, 38 giấy phép); gib20 24,5 s đã dựng llvmpipe (cú liên hoàn WCA → giao lộ 1941 → reveal, năm dừng 1941 1,79 s, hero trung vị 27,1 %); đường băng/trạm biên giới/xe 1941 đã là hero | thấp: chưa tải gì; phải số hoá phố trước 1666 từ bản đồ 1676 (ghost) | trung bình: giấy phép sổ thuế đã kiểm; bản đồ chưa tải |
| Thiếu để thành tập chiến tranh | tuyến vây 1779–83 (chiến tuyến Tây Ban Nha trên eo đất), hạm đội + pin nổi 13/9/1782, phố cháy 1781, đường hầm 1782 (mặt cắt), lớp nhà thật phía Gibraltar (footprint OSM + ghost) | toàn bộ mô-đun lửa/khói + ghost phố | hào/luỹ, đất lấn theo năm |
| Rủi ro | **VÀNG** (chủ quyền; luật câu chữ tiền kỳ T3 §7 áp nguyên; không "colony/occupied/stole" bằng lời kênh; bật lọc bình luận — mẫu §1.5 đã có bình luận Ceuta) | XANH | XANH |
| Hạn | **neo 14/12/2026** (biểu quyết Nghị viện châu Âu) → còn **58 ngày** từ 17/10 | không neo cứng (dịp 360 năm: 9/2026 đã qua) | không neo cứng (250 năm: 3/2026 đã qua) |

### 4.2 Đề xuất
- **T3 = Gibraltar, khung lại quanh vây hãm, giữ cú lật kinh tế của tiền kỳ T3 làm chương kết.** Gợi ý mạch (lời tiếng Anh viết ở G1, không chốt ở đây):
  0. Móc: hàng xe ở cổng 2026 → máy kéo lùi → năm chạy ngược về 1704.
  1. 1704 — Rooke chiếm Rock (tranh Rijksmuseum CC0; phố trong tường, ghost).
  2. 1779–83 — Great Siege: chiến tuyến Tây Ban Nha mọc trên eo đất; phố bị bắn cháy 1781; Eliott và lò nung đạn đỏ; pin nổi 13/9/1782; đường hầm 1782 (mặt cắt). Trả lời câu hỏi hậu cần khán giả hỏi (§1.5).
  3. Thế kỷ 19 — eo đất trung lập, rào, La Línea mọc (Catastro, đã có ở gib20).
  4. 1941 — đường băng lấn vịnh trên eo đất (cú liên hoàn gib20), đường hầm WWII.
  5. 1969–85 cổng đóng → 2026 hiệp ước; "điều cần theo dõi" 14/12; chương kinh tế (GDP/người theo dân cư trú vs thất nghiệp La Línea 28,6 %) giữ từ tiền kỳ T3.
- **Tiêu đề làm việc** (chờ Đóng gói, ≤ 60 ký tự): "Why Everyone Keeps Besieging Gibraltar" (38) · "14 Sieges: Why Everyone Wants Gibraltar" (39) · "Why a Runway Sits on Gibraltar's No-Man's-Land" (46). Số "14" lấy từ cách đếm phổ biến; **chưa kiểm nguồn gốc** (Gibraltar National Museum) → claim mới ở G1.
- **Phạm vi máy dựng cho T3 (để kịp 14/12):** dùng bản rút gọn của V6 — tuyến vây (đường + dải tô theo năm, mở rộng `boundaryTrace`), hạm đội = `ships.js` + đường đi theo khung giờ, phố cháy = đổi vật liệu/ghost + sprite khói 2D, đường hầm = mặt cắt tĩnh. Không làm đội hình bộ binh chi tiết.
- **T4 bắt buộc XANH: London 1666** (đề xuất) hoặc Boston. London cần phiên tiền kỳ riêng (số hoá Ogilby & Morgan, giấy phép từng bản quét) — bắt đầu song song với G1 T3.

---

## 5. Khoảng trống máy dựng

### 5.1 Đã có (đọc từ `design/k2v/tl/README.md` và `reports/V5B2A-BAO-CAO.md` trên `origin/v5b2a`)
Xương sống thời gian 3 tầng (CHUẨN theo mốc bằng chứng / ĐẦY ĐỦ theo năm toà / GHOST có nhãn nguồn); địa hình DTM LOD + 13 lớp nền thủ tục; nước + trời; **nhà thủ tục 6 kiểu mặt đứng × 6 kiểu mái, gộp theo ô, LOD**; cây, đường OSM theo năm; hero (tháp, tường, đường băng, trạm biên giới 1941); **tàu theo thời kỳ** (buồm → hơi nước → hiện đại); xe/người A-lite đi theo tuyến; **7 preset máy** (liên hoàn, push-in, boundary trace, follow, lateral, top-down rise, vertigo) có giới hạn ≤ 10 năm/s, ≤ 90 °/s, AGL theo loại tuyến; ngân sách chữ + thẻ neo + log; mặt nạ mọi khung (`content_pct`, `fabric_pct`, `hero_pct`); then/now căn từ điểm khống chế (R&D). Bộ k2v: bản đồ nổi, sticker vật trong cảnh, chân dung cắt nền Ken Burns 2.5D (Kinh thánh §4 F2), footage, zoom nhiều tầng.

### 5.2 Thiếu cho thể loại chiến tranh/sự kiện
| # | Thiếu | Cách làm đề xuất | Dữ liệu vào | Giờ máy thêm/tập 10 phút (ước) | Phiên |
|---|---|---|---|---|---|
| M1 | **Mũi tên tiến quân 3D bám địa hình** (dải ruy băng có đầu mũi tên, mọc theo giờ, màu phe cố định) | mở rộng `overlay3d.js` (đã có dải bám ranh giới) | tệp tuyến GeoJSON + mốc giờ, mỗi tuyến 1 claim | +0,05 h | **V5b-2b** |
| M2 | **Đội hình quân theo thời gian** (khối đơn vị A-lite instanced, xoay/dịch theo bảng lệnh tác chiến) | mô-đun mới `troops.js` (instancing theo thuộc tính như `city.js`) | bảng đơn vị × thời điểm × vị trí (từ sơ đồ trận PD) | +0,2 h | **V6** |
| M3 | **Hạm đội** (tàu theo thời kỳ đi theo đội hình, khói pháo 2D) | `ships.js` + đường đi + đội hình | vị trí theo giờ (sơ đồ trận) | +0,1 h | **V6** (bản rút gọn cho T3 ở V5b-2b) |
| M4 | **Tuyến vây/hào/chiến luỹ mọc theo ngày** | khắc vào DTM (dải hạ thấp + gờ đất) + vật liệu đất mới, mọc theo `uYear`/`uDay` | sơ đồ vây PD được georeference | +0,1 h | **V6** |
| M5 | **Thành luỹ mọc/sập** (bastion sao tham số hoá, trạng thái nguyên/vỡ/phá) | bộ sinh hero tham số (`heroes.js`), trạng thái theo năm | kích thước từ sơ đồ luỹ | +0,1 h | **V6** |
| M6 | **Ngày/giờ trong trận** (bộ đếm "13 Sep 1782 · 10:00", vị trí mặt trời theo giờ thật, đêm/ngày) | biến thể bộ đếm trong `text.js` + mặt trời theo thiên văn | lịch sự kiện có nguồn | ≈ 0 | **V5b-2b** |
| M7 | **Khói/lửa** (phố cháy London 1666, Rotterdam 1940, phố Gibraltar 1781) | sprite 2D billboard có tích luỹ SPP + đổi vật liệu toà "cháy" → "ghost tro"; **không** mô phỏng thể tích (CPU không kham) | vùng cháy theo giờ (bản đồ PD) | +0,2–0,4 h (trên ~10 % khung) | **V6** |
| M8 | **Chân dung tranh PD Ken Burns trong trang tl** (không AI) | tích hợp cắt nền + Ken Burns k2v vào `tl/page.js` (thẻ neo đã có) | tranh CC0/PD | ≈ 0 (khung 2D thay khung 3D) | **V5b-2b** |
| M9 | **Nhà thật ở thành phố**: nhập footprint OSM/sổ đăng ký (BAG, GWR, Catastro, Boston, Wien) → khối + **mái theo thời kỳ** (thư viện mái theo vùng × thế kỷ) | tổng quát bộ nạp Catastro hiện có → nạp chung; thư viện mái: V6 | sổ đăng ký (đã có cho NL, CH, ES; Boston PDDL) | +0,9 h (nặng hơn ở cảnh phố dày) | nạp chung **V5b-2b**; thư viện mái **V6** |
| M10 | **Số hoá footprint lịch sử** (công cụ georeference + vẽ khối ghost từ bản đồ PD) | công cụ bán thủ công + kiểm chồng | bản đồ PD | 0 máy; **20–40 h người/tập (ước)** — tiền kỳ thành phố ước 80–130 h cho cả thành phố, tập chiến tranh chỉ cần lõi ~1–2 km² | **V6** (công cụ) + phiên tiền kỳ (số hoá) |
| M11 | **Mặt cắt đường hầm** (Great Siege Tunnels, đường hầm WWII) | mặt cắt khối đá + hầm theo năm | sơ đồ hầm (nguồn chưa kiểm) | ≈ 0,05 h | **V6** |
| M12 | **Lớp bản đồ pha làm vân mặt đất theo năm** (crossfade bản đồ lịch sử đã georeference) | tầng CHUẨN đã có khái niệm mốc → thêm raster theo mốc | bản đồ PD | ≈ 0 | **V5b-2b** |

### 5.3 Ước giờ máy tập 10 phút (CPU llvmpipe)
- **Nền đã đo (V5b-2a §7.3, máy D):** 4,33 h dựng + 0,91 h mặt nạ = **5,24 h**; máy C ≈ 3,45 h.
- **Thêm (ước):** M9 phố dày (giả sử 50 % khung 3D là phố dày; R&D đo 75 nghìn toà 1080p SwiftShader 2,1–2,6 s/khung, quy llvmpipe ×0,45–0,5 theo hệ số V5b-2a đo trên relief/nhà máy → ~1,0–1,3 s, cộng SPP như gib20 → ~2,0 s so 1,33 s) ≈ +0,9 h; M1–M5 + M11 ≈ +0,5 h; M7 ≈ +0,3 h; M8 thay khung 3D bằng 2D → −0,2 h.
- **Tổng ≈ 6,7 h máy D (dải 5,5–7 h) / ≈ 4,4 h máy C (dải 3,6–4,6 h) — (ước)**, dưới trần 12 h. Rủi ro: thành phố > 300 nghìn toà làm trình duyệt sập (R&D §6.4) → bắt buộc chia ô/LOD (đã có ở `city.js`).
- **Đề xuất đo thật trước khi khoá:** V5b-2b dựng 1 đoạn 20 s phố dày Rotterdam hoặc Amsterdam trên llvmpipe để thay số ước của M9.

### 5.4 Chia việc
- **V5b-2b** (đã có danh sách tích hợp 9 điểm ở V5b-2a §8): thêm **M1, M6, M8, M9 (nạp chung), M12** + bản rút gọn M3/M4 cho T3 Gibraltar. Ước thêm ≈ 1,5 h máy thử **(ước)**.
- **V6 "Chiến trường" (phiên V riêng, sau V5b-2b):** **M2, M3 đầy đủ, M4, M5, M7, M9 thư viện mái, M10 công cụ, M11**, kèm đoạn thử 30 s (đề xuất London 1666 hoặc Vicksburg) và luật đo cho K (lệch tuyến quân so tuyến nguồn, mũi tên không đè thẻ, khói ≤ x % khung).

---

## 6. Luật hình rút từ đánh giá T2 của chủ dự án

Hai lỗi chủ dự án nêu khi xem T2 "Shipbuilding": **(1)** nơi thành phố chỉ là địa hình, không có nhà cửa thật; **(2)** địa cầu/độ cao lớn không cần thiết. Số liệu từ G2 T2 xác nhận: 29 shot bản đồ, map 88,7 % thời lượng (Q34); người chấm mù chê "nơi không được gọi tên" ở cả 3 lần (§12.7 G2); cảnh g05_china máy đẩy từ 30 → 18 rồi lùi 22 **bán kính Trái Đất**; khung T1 thắng cặp E2 là một **quả địa cầu tô Texas**.

### 6.1 Đề xuất cho Kinh thánh §4 (P ghi; phiên này không sửa `docs/`)
- **(a) Thành phố phải có nhà và đường đúng thời kỳ.** Mọi shot mà lời nhắc một thành phố/thị trấn, hoặc máy ở AGL ≤ 3 km trên vùng đô thị, phải hiện nhà cửa + đường phố của đúng năm đang kể: toà từ sổ đăng ký (tầng ĐẦY ĐỦ), khối ghost có nhãn nguồn (tầng GHOST), hoặc ảnh/bản đồ lịch sử neo. **Không dùng địa hình trống đại diện thành phố.** Không có dữ liệu → đổi đề tài hoặc dùng bản đồ lịch sử phẳng có nhãn, không giả nhà.
- **(b) Địa cầu/độ cao lớn chỉ khi khán giả cần định vị.** Tối đa **1 lần/tập, ≤ 3 s**, ở móc câu hoặc lần đầu đổi châu lục; mặc định **tầm vùng hoặc thành phố**. Chuyển tầng bằng zoom nhiều tầng (đã duyệt F4) thay vì đứng ở địa cầu.

### 6.2 Ngưỡng đo được (đề xuất cho K; đo bằng công cụ đã có)
| Mã đề xuất | Luật | Đo bằng | Ghi chú |
|---|---|---|---|
| **NC-H1 Thành phố có nhà** | Shot khai `noi: thanh_pho` (hoặc AGL ≤ 3 km và tâm khung trong polygon đô thị OSM `landuse=residential/commercial`): **trung vị `fabric_pct` (nhà + đường) ≥ 25 %** trong shot; **không khung < 15 %**, trừ ≤ 3 s cuối cú reveal | mặt nạ mọi khung (`render.js --maskonly`, V5b-2a đã xuất `fabric_pct`) | 25 %/15 % là **đề xuất chưa đo**: K chạy thử trên gib20 + T2 trước khi khoá; số tham chiếu duy nhất có sẵn là hero trung vị 27,1 % ở orbit gib20 (hero ≠ fabric) |
| **NC-H2 Địa cầu** | Khung có **AGL > 50 km** tính là "địa cầu"; tổng thời gian ≤ **3 s/lần**, ≤ **1 lần/tập** | `campath.json` (AGL mỗi khung); với `scripts/k2` cần ghi AGL vào `meta.json` (V5b-2b) | T2 có cảnh 18–30 bán kính Trái Đất → sẽ TRƯỢT |
| **NC-H3 Tầm mặc định** | ≥ 70 % thời lượng 3D ở AGL ≤ 60 km; ≥ 40 % ở AGL ≤ 3 km (tập có thành phố) | `campath.json` | đề xuất chưa đo |
| **NC-H4 Nơi có tên** | mọi shot bản đồ có chip nơi dựng hoặc nhãn địa danh (đã là đề xuất SS5/TT6 của T2) | log chữ | nhập chung |
| **NC-H5 Đúng thời kỳ** | toà/đường hiện trong khung có năm xây ≤ năm bộ đếm (không "mọc trước"); ghost có nhãn nguồn ≥ 38 px trong ≥ 3 s lần đầu hiện | log năm + log chữ | chặn đúng lỗi khán giả bắt ở đối thủ (tường Thiers 1810; Malta Birgu) |

---

## 7. Kiếm tiền và chính sách (nguồn: support.google.com, đọc 17/10/2026; trang không ghi ngày cập nhật)

### 7.1 Hướng dẫn nội dung thân thiện với quảng cáo — `support.google.com/youtube/answer/6162278`
| Mục | Đủ quảng cáo | Quảng cáo hạn chế | Không quảng cáo |
|---|---|---|---|
| Bạo lực / chiến tranh | thảo luận/đưa tin giáo dục **không đồ hoạ** về chiến tranh; thi thể **che kín, làm mờ, đã khâm liệm, hoặc trong sự kiện lịch sử như chiến tranh trong video giáo dục** | thi thể có thương tích rõ trong bối cảnh giáo dục/tài liệu; footage chiến tranh thô, không đồ hoạ, **không có bối cảnh giáo dục** | **footage chiến tranh có mô tả đồ hoạ thương tích, cái chết, đau đớn — trong mọi bối cảnh**; thi thể đồ hoạ trong video không giáo dục |
| Sự kiện nhạy cảm (gồm xung đột, bạo lực hàng loạt) | thảo luận mất mát không khai thác, không xem nhẹ | — | khai thác/trục lợi sự kiện (vd nhồi từ khoá) |
| Gây sốc | gây sốc nhẹ/vừa, được che hoặc có bối cảnh | hình bộ phận cơ thể không che | mục đích chính là gây sốc |

Định nghĩa trên trang: *educational* = dạy về một chủ đề mà không cố ý gây hiểu sai; *documentary* = ghi nhớ, lưu giữ sự kiện lịch sử bằng cách trích tài liệu gốc hoặc mô tả sự thật. Quy trình claims có trích nguyên văn của nhà máy khớp đúng định nghĩa này.

### 7.2 Nguyên tắc cộng đồng — bạo lực đồ hoạ (`answer/2802008`) và tổ chức cực đoan (`answer/9229472`)
- Ngoại lệ giáo dục/tài liệu (EDSA): **bối cảnh phải nằm trong hình hoặc tiếng của chính video**; ghi ở tiêu đề hay mô tả là không đủ. Luật áp cho cả **thumbnail**.
- Nội dung đủ bối cảnh vẫn có thể bị **giới hạn độ tuổi** (ẩn với người < 18 và người chưa đăng nhập) — mất phần lớn phân phối.
- Biểu tượng tổ chức cực đoan bị cấm khi nhằm ca ngợi/quảng bá; có ngoại lệ EDSA, nhưng trang không nói riêng về biểu tượng Quốc xã hay tuyên truyền Thế chiến II → **suy luận của phiên:** thumbnail không có ngữ cảnh, nên không đặt biểu tượng cực đoan lên thumbnail.

### 7.3 Nội dung tổng hợp / AI — `answer/14328491`
- Phải khai khi nội dung **trông thật** và: làm người thật nói/làm điều họ không làm; **sửa footage sự kiện/nơi có thật**; tạo cảnh thật như chưa từng xảy ra; tạo nhạc làm trọng tâm.
- Không phải khai: nội dung không thật (hoạt hình), chỉnh màu/ánh sáng, dùng AI cho kịch bản/tiêu đề/ý tưởng.
- Khai báo **không tự giảm phân phối hay quyền kiếm tiền**; nhiều lần không khai → có thể bị gắn nhãn thủ công, gỡ, hoặc dừng YPP.

### 7.4 Kiếm tiền YPP — nội dung không chân thực / dùng lại — `answer/1311392`
- Từ **15/07/2025**, "repetitious content" đổi tên thành **"inauthentic content"**: nội dung lặp lại hoặc sản xuất hàng loạt, trông như làm từ khuôn; nêu rõ nội dung AI làm theo khuôn chung không có góc nhìn riêng. Cùng cấu trúc mở/kết vẫn được nếu nội dung chính khác nhau.
- "Reused content": dùng lại nội dung nguồn khác không thêm bình luận/biến đổi đáng kể → **có thể mất kiếm tiền cả kênh**, kể cả khi được phép.

### 7.5 Cách giữ đủ quảng cáo cho series (đề xuất ghi vào LUAT-NOI-DUNG-G)
1. **Không thi thể, không máu, không vết thương** trong hình tự dựng lẫn ảnh/footage lưu trữ. Ảnh lưu trữ có thi thể (kể cả nhỏ, xa) → không dùng; thay bằng ảnh nơi chốn.
2. **Thương vong nói bằng số có nguồn + biểu tượng trung tính** (cột, chấm, sticker không người), đặt trên bản đồ; không diễn cảnh chết.
3. **Không cổ vũ bạo lực:** lời kể theo cơ chế (vì sao nơi này quan trọng, hậu cần, quyết định), không tôn vinh thảm sát; nhân vật được kể bằng mong muốn–trở ngại–kết cục (Kinh thánh §3), không phán xét đạo đức bằng lời kênh.
4. **Bối cảnh giáo dục trong hình và tiếng:** câu mở nói rõ đây là giải thích lịch sử; dòng nguồn ngắn trên hình (đã có).
5. **Thumbnail:** nơi chốn + thành luỹ/đường băng/hạm đội; không vũ khí chĩa vào người, không lửa có người, không biểu tượng cực đoan, không cờ làm điểm nhấn (tiền kỳ T3 §8).
6. **Footage chiến tranh** (nếu dùng, ≤ 20 % theo F3): chỉ cảnh không có người bị thương/chết; kiểm từng clip trước khi khoá.
7. **Không nhồi từ khoá sự kiện** trong mô tả/tag (mục "sensitive events").
8. **Mỗi tập phải khác nhau thật về nội dung chính** (tránh "inauthentic content" khi làm series theo khuôn): đề tài, nhân vật, cơ chế, dữ liệu riêng; khung mở/kết giống nhau được.

### 7.6 Ghi nhãn và giữ "no AI imagery"
- Hình 3D tự dựng từ dữ liệu là CGI, **không phải AI tạo sinh** → không thuộc diện bắt buộc khai. Phim tái dựng phong cách hoá, không trông như footage thật.
- **Giọng ElevenLabs** là giọng tổng hợp nhưng không mạo danh người thật → không thuộc mục bắt buộc trên trang. Đề xuất vẫn ghi minh bạch trong mô tả: *"Narration: synthetic voice. Visuals: 3D reconstructions built from the cited sources and registers; no AI-generated imagery. Historical images: public domain / CC0, credited."*
- **Phải khai** nếu sau này: đọc lời trích của nhân vật thật bằng giọng tổng hợp mô phỏng người đó; hoặc sửa ảnh/footage lưu trữ cho trông như cảnh thật khác đi.
- **Giữ "no AI imagery":** công cụ tách nền (F2) chỉ tách, không sinh hình — giữ đúng như Kinh thánh; không phóng to/tô màu ảnh bằng mô hình tạo sinh; ghi "đã chỉnh sửa" khi giấy phép yêu cầu.

---

## 8. Đề xuất cuối

1. **Hình thức:** **(A)** series "Contested Places" trong Moving Parts, lời hứa L1; cổng quyết định sau 3 tập (§2.2).
2. **Tập thử:** **T3 Gibraltar khung vây hãm**, phát hành trước 14/12/2026. **T4 London 1666** (XANH).
3. **Hàng đợi 6–8 đề tài** (sau T3–T4, đã cân XANH/VÀNG):
   | Thứ tự | Đề tài | Điểm | Mức | Lý do |
   |---|---|---|---|---|
   | 1 | Boston 1775–76 + đất lấn | 20 | XANH | sổ PDDL có năm; đối đầu trực tiếp bản AI |
   | 2 | Vicksburg 1863 + "con sông bỏ đi" 1876 | 20 | XANH | góc riêng duy nhất; bản đồ chính phủ Mỹ PD |
   | 3 | Rotterdam 1940 | 19 | XANH | dữ liệu tốt nhất (BAG/3DBAG), khoảng trống lớn |
   | 4 | Antwerp 1585 → Amsterdam | 17 | XANH | cầu nối với Moving Parts (dòng tiền dời đi), dùng lại dữ liệu R&D Amsterdam |
   | 5 | Malta 1565 → Valletta | 18 | VÀNG | cầu lớn; góc "vây hãm xây nên thành phố" |
   | 6 | Halifax 1917 | 18 | XANH | cầu lớn, 0/5 có nguồn; cần kiểm quyền tư liệu |
   | 7 | Zürich 1799 | 19 | XANH | dữ liệu sẵn tốt nhất (tiền kỳ thành phố); cầu thấp → làm khi kênh đã có đà |
   | 8 | Leiden 1574 | 17 | XANH | dữ liệu NL tốt; ngập polder là cảnh timelapse hay |
   Vienna 1683 để cuối (khoảng trống 1/5, VÀNG).
4. **Việc máy dựng:** V5b-2b nhận M1, M6, M8, M9 (nạp chung), M12 + bản rút gọn M3/M4 cho T3; mở **phiên V6 "Chiến trường"** cho M2, M3, M4, M5, M7, M9 (mái), M10, M11 (§5.4).
5. **Thay đổi Kinh thánh** (P ghi): §1 thêm lời hứa series L1 + lăng kính "nơi bị tranh giành"; §2 thêm điều kiện chọn đề tài "câu Why có cả chiến sự lẫn giá trị của nơi"; §4 thêm luật (a)(b) ở §6.1 và luật hình chiến tranh ở §7.5; §6 thêm phiên tiền kỳ số hoá footprint lịch sử cho tập thành phố.
6. **Chỉ số đo thành công** (7 ngày và 28 ngày sau đăng):
   | Chỉ số | Mục tiêu đề xuất | Nguồn số |
   |---|---|---|
   | CTR hiển thị | ≥ T1/T2 trung bình; ≥ 5 % ở 7 ngày **(ước — chuẩn ngành, chưa có số kênh)** | YouTube Studio |
   | Thời gian xem trung bình | ≥ 40 % thời lượng **(ước)** | Studio |
   | Giữ chân phút 1 | ≥ 60 % **(ước)** | Studio |
   | Đường giữ chân tại các nhịp timelapse/cú liên hoàn | không tụt > 5 điểm % trong 10 s quanh nhịp | Studio (đánh dấu theo timecode bảng shot) |
   | **Chấm mù vs đối thủ cùng loại cảnh** | ≥ 7/10 và thắng ≥ 2/3 người chấm ở mỗi cặp; cặp so **cùng loại cảnh**: (i) bản đồ trận 2D của kênh (a) vs cảnh trận của mình; (ii) tái dựng AI của kênh (c) vs then/now của mình; (iii) thành phố mọc của Latos vs cảnh phố của mình. Khung đối thủ chỉ xem tạm ngoài git, không commit | giao thức `blind_g2.py` (mở rộng) |
   | Giọng đọc | tỷ lệ bình luận chê giọng/AI ≤ 2 % (mẫu 100 bình luận) | commentThreads |
   | Độ đúng | ≤ 1 bình luận sửa sai có trọng số ≥ 20 like không phản bác được bằng claims | commentThreads + claims |
   | Luật hình mới | NC-H1, NC-H2 ĐẠT | K |
   | Chi phí | giờ máy ≤ 12 h/tập; công số hoá ≤ 40 h | log |
7. **Rủi ro chính và cách giảm**
   | Rủi ro | Mức | Giảm |
   |---|---|---|
   | Khán giả lẫn lộn (kinh tế vs chiến tranh) | trung bình | khung "vì sao nơi này có giá"; playlist riêng; chuỗi 3 tập liền; cổng quyết định (§2.2) |
   | Đề tài đã bị kênh lớn làm (14/15 có video dài đúng đề tài ≥ 100 nghìn) | cao | thắng bằng hình nơi chốn + then/now + đúng năm; đo chấm mù cùng loại cảnh |
   | Giọng tổng hợp thua giọng người (Epic History: giọng 40,6 % trọng số like) | cao | đo riêng giọng ở T3; nếu chê > 2 % → chủ dự án cân nhắc giọng người thật (chi phí, quyền) |
   | Sai lịch sử ở thành luỹ/bố cục phố (lỗi người địa phương bắt) | trung bình | NC-H5; mỗi hero có claim nguồn; ghost có nhãn |
   | Chủ quyền/tôn giáo (Gibraltar, Malta, Vienna) | VÀNG | luật câu chữ tiền kỳ T3 §7; ≤ 2 VÀNG liền; lọc bình luận từ video đầu |
   | Quảng cáo hạn chế/giới hạn tuổi do hình chiến tranh | trung bình | §7.5; kiểm thumbnail và footage trước khi khoá |
   | Công số hoá bản đồ lịch sử vượt ước | cao | chọn đề tài có sổ đăng ký (NL, CH, Boston); giới hạn lõi 1–2 km²; công cụ M10 |
   | Giấy phép bản đồ lịch sử (Gallica, Rumsey không thương mại) | trung bình | chỉ dùng LoC/NARA/USGS (PD), Rijksmuseum/The Met CC0, Wien/Zürich/Helsinki OGD; lưu trang giấy phép từng tệp |
   | Máy dựng trễ cho T3 | trung bình | bản rút gọn ở V5b-2b (§4.2); V6 cho T4+ |

---

## 9. Hạn chế của nghiên cứu này
- Mẫu kênh có chủ đích (39 kênh do phiên chọn + 4 lượt tìm); không đại diện toàn ngách. Search `order=relevance` thiên về kênh lớn; kênh mới nhỏ có thể bị sót.
- "Hình thức hình" và "nhóm" là phân loại của phiên, không phải số đo.
- Nhãn bình luận bằng regex + đọc tay, 8 video; tỷ lệ chỉ để so hướng, không dùng làm xác suất.
- Dữ liệu timelapse/giấy phép của 15 đề tài phần lớn **chưa tải, chưa đọc từng trang giấy phép**; chỉ Gibraltar (tiền kỳ T3), Zürich (tiền kỳ thành phố), Amsterdam/NL (R&D) và Boston (giấy phép bộ dữ liệu PDDL) có kiểm. Mọi ô ghi "(chưa kiểm)" phải qua phiên tiền kỳ trước G1.
- Các mốc lịch sử nêu trong §3 là kiến thức chung của phiên, **chưa qua quy trình claims**; không dùng trong lời trước khi kiểm.
- Giờ máy §5.3 là ngoại suy từ số đo cũ, chưa đo cảnh phố dày trên llvmpipe.
- Không có số liệu kênh Moving Parts đã phát hành, nên so sánh hình thức A/B/C dựa vào suy luận.

## 10. Chi phí thật và dòng đề xuất cho tệp dùng chung
| Hạng mục | Thực tế | Trần |
|---|---|---|
| YouTube Data API | **2 124 đơn vị** (search.list 19 × 100 = 1 900; channels 79; playlistItems 59; videos 78; commentThreads 8) | 3 000 |
| Claude API | **$0** — không gọi; không có `cost.jsonl` | $1 |
| ElevenLabs | **0** ký tự | 0 |
| Giờ máy | **≈ 0,1 h** (script Python, không dựng hình) | 1 h |
| WebSearch / WebFetch | 3 / 5 lượt | — |

**Dòng đề xuất cho `COST-LEDGER.csv`** (P chép; phiên này không ghi vì ngoài vùng): `NC-LS-01, 2026-10-17, nc-lich-su, nghiên cứu, claude_api_usd=0, youtube_units=2124, elevenlabs_chars=0, render_h=0.1`.
**RIGHTS.md / AUTHORSHIP.md:** không có tài sản mới vào repo; không cần dòng. Quyết định sáng tạo (hình thức, lời hứa, đề tài) chờ chủ dự án → ghi AUTHORSHIP khi duyệt.

## 11. Tệp và preflight
- `reports/NC-LICH-SU-BAO-CAO.md` (tệp này)
- `reports/nc-lich-su/kenh.csv` — 39 kênh, số đo + phân loại hình thức
- `reports/nc-lich-su/de-tai-cau.json` — cầu 15 đề tài (không có tiêu đề/mô tả của kênh khác)
- `reports/nc-lich-su/binh-luan-tom-tat.json` — số đếm nhãn bình luận 8 video (không có văn bản bình luận)
- `reports/nc-lich-su/cham-diem.json` — điểm /25 + danh sách loại
- `reports/nc-lich-su/cost.json` — chi phí
- **Preflight:** `bash tools/preflight.sh --range origin/main..HEAD` → **PREFLIGHT ĐẠT**; `lock.py --verify` → **KHỚP** (chạy trước commit; hook pre-commit/pre-push chạy lại khi commit/đẩy).

## 12. Việc chờ chủ dự án
1. **Chọn hình thức** A / B / C (đề xuất A + cổng quyết định sau 3 tập).
2. **Chọn lời hứa** L1 / L2 / L3 (đề xuất L1).
3. **Duyệt T3 = Gibraltar khung vây hãm** và mạch 6 chương (§4.2); xác nhận vẫn nhắm trước 14/12.
4. **Duyệt T4 = London 1666** (hoặc Boston) và cho mở phiên tiền kỳ số hoá song song.
5. **Duyệt hàng đợi 8 đề tài** (§8.3).
6. **Duyệt chia việc máy dựng:** thêm M1/M6/M8/M9/M12 + bản rút gọn M3/M4 vào V5b-2b; mở phiên **V6 "Chiến trường"**.
7. **Duyệt đề xuất Kinh thánh** (§8.5) và giao K chạy thử NC-H1…H5 trên gib20 + T2 trước khi khoá ngưỡng (25 %/15 %, 50 km/3 s).
8. **Duyệt luật hình chiến tranh** (§7.5) cho LUAT-NOI-DUNG-G.
9. **Giọng đọc:** đồng ý đo riêng chỉ số chê giọng ở T3; nếu > 2 % thì cân nhắc giọng người thật (quyết định chi phí).
10. **Tự quyết của phiên (không dừng hỏi), cần chủ dự án biết:** (i) không gọi Claude API — nhãn bình luận làm bằng regex + đọc tay để giữ $0; (ii) đổi tiêu chí 3–4 của thước /25 cho hợp thể loại (§3.1); (iii) London 1666 được tính là "sự kiện" dù không phải trận đánh, vì lệnh cho phép "sự kiện lịch sử"; (iv) không chép tiêu đề video đối thủ vào repo (chặt hơn Teardown) để đúng lệnh "không đưa lời của kênh khác".
