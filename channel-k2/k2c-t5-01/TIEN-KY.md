# TIỀN KỲ T5 — "Why Zürich Shrank While Getting Rich" (K2C-T5-01)

> Phiên Tiền kỳ T5, 16/10/2026. Lệnh chủ dự án duyệt 16/10. Tập Moving Parts **tầng đầy đủ** ("từng toà mọc đúng năm"), mức XANH.
> Nhánh `k2c-t5-tienky` từ `origin/main` @ `7255aa4`. **Không merge.**
> Mọi lượt xem là **số công khai YouTube Data API, đọc ngày 16/10/2026 (UTC)**. Mọi tỷ lệ, nhãn và phép cộng trừ là **tự tính**, không phải chỉ số YouTube hay số chính thức.
> Mọi trích dẫn đều chép **nguyên văn** từ tệp tải bằng curl rồi tách chữ. Phần trích được cắt tự động giữa hai mốc trong văn bản, nên chắc chắn đúng nguyên văn. Có một ngoại lệ: bản quét Stadtarchiv và Jahrbuch là OCR do ZB lưu, nên có thể có lỗi OCR nhỏ. SHA-256 ghi trong `tienky/*.json`. Tệp thô, gói 4D, OBJ gộp và ảnh render để **ngoài git** (thư mục scratch của phiên).

## 0. Khối điều lệ (chép lệnh, thêm cột thực tế)
| Trường | Lệnh | Thực tế |
|---|---|---|
| Loại phiên | Tiền kỳ T5 (bước Đóng gói + dữ liệu xương sống) | như lệnh |
| Nhánh | `k2c-t5-tienky` từ `origin/main` | `7255aa4`; đã đẩy. Harness gán thêm nhánh `claude/loving-fermi-igq4yk`; cùng commit được đẩy lên **cả hai tên** |
| Tệp được sửa | `channel-k2/k2c-t5-01/TIEN-KY.md`, `tienky/**`, `licenses/` | đúng như lệnh: 1 tệp md, 14 tệp `tienky/*.json`, 12 tệp `licenses/`. Không sửa mã nhà máy, `checks/`, `design/`, `scripts/` hay tệp của tập khác. **Không ghi COST-LEDGER, RIGHTS, AUTHORSHIP** (xem §14). Không đọc `checks/` |
| Trần | YouTube ≤ 200 đơn vị · Claude API ≤ $2 (ghim model) · ElevenLabs 0 · giờ máy ≤ 2 giờ | **125 đơn vị** · **$0,0045** (1 lượt `claude-haiku-5-5`; model thực chạy = haiku) · **0 ký tự** · **≈ 23 phút** máy (13 phút tính toán + 10 phút tải) |
| Preflight | bắt buộc; che email | hook pre-commit/pre-push cài đầu phiên; `tools/preflight.sh --range origin/main..HEAD` **ĐẠT**, `lock.py --verify` **KHỚP** (§15). 0 email trong các tệp đã ghi |
| Điều kiện dừng | xong → đẩy → dừng; không dừng hỏi giữa chừng | (1) xong việc |

## 1. Tóm tắt và khuyến nghị
**Khuyến nghị: ĐI TIẾP Zürich. Không chuyển sang Helsinki hay Detroit.** Kèm 3 điều chỉnh bắt buộc.

**Lý do đi tiếp:**
1. **Cầu riêng của Zürich nay đã đo được, và tốt hơn phiên chọn thành phố tưởng.**
   - Phiên chọn thành phố gộp 5 thành phố vào một lượt tìm, nên Zürich bị lấn chỗ.
   - Đo riêng ("Zurich history|Zürich history|Zurich timelapse") cho thấy 5 video lịch sử Zürich đăng từ 13/09 đến 12/10/2026.
   - Epoch Timeline "Evolution of ZÜRICH: 1,126 Years of History" đạt **34 505 lượt sau 33 ngày** (9,5 phút) → **Cầu-ngách ĐẠT**.
2. **Khoảng trống vẫn ĐẠT, theo cả hai nhánh của luật:**
   - 0/5 video có nguồn số liệu, 0/5 có cơ chế "vì sao" (Haiku chấm).
   - 12/20 bình luận dưới video lớn nhất là bình luận **chỉnh sai** do người Zürich viết: St. Peter đặt sai bờ sông, "sông chảy ngược", nhà chọc trời năm 1793. Nhóm này nhận 42/48 lượt thích.
   - Không video nào nói tới chuyện Zürich co lại, sáp nhập hay phá dỡ. Cả 5 đều là dạng máy quay cố định dựng hình; 2/5 tự khai là AI.
3. **Mọi nguồn còn thiếu mà §11.4 của TIEN-KY-THANHPHO liệt kê đã có nguồn gốc** (§9): "không sáp nhập sau 1934"; tách phần tăng dân 1880→1893; năm St. Peter, ETH, Prime Tower; cơ chế hồ → Limmat.
4. **Dữ liệu xương sống tốt hơn ước:**
   - Gói 4D 1800 nặng 960 MB, nhưng **98,9 % là texture**. Hình học chỉ có **300 300 tam giác**, không cần giảm lưới.
   - 591 toà của lát 1800 mang **EGID thật**, nối thẳng được vào GWR.
   - Ước công số hoá tay giảm từ 80–130 xuống **53–89 giờ** (chưa kể hero) (§11–§12).
5. **103 claim, 99 XÁC MINH** (§6). Mức XANH giữ được, vì cơ chế nằm ở chuyện nhà ở, ranh giới và đường sắt, không cần tới ngân hàng.

**Ba điều chỉnh bắt buộc so với công thức:**
1. **"Vượt đỉnh năm 2022" chỉ đúng theo số của Thành phố.**
   - Số của Thành phố là dân số "kinh tế", gồm cả người ở theo tuần: 443 037 năm 2022.
   - Theo số của Bang, thành phố **chưa** vượt đỉnh: 439 039 năm 2025, so với 440 784 năm 1962. Đáy theo Bang là năm 1999, không phải 1989.
   - Lời phải nói "by the city's own count", và đưa chỗ lệch này vào đoạn "the honest part" (K04, Z68).
2. **Không đọc thẳng "1893: 117 044" từ CSV.** Con số đó là dân số ngày 1/1/1894. Ngày sáp nhập 1/1/1893 có **107 416** người (Z08).
3. **Toà đã mất trong giai đoạn 1800–1999 không có năm phá trong sổ mở nào**, vì GWR chỉ ghi năm phá từ 1999.
   - Lát 1800 có 4 699 toà như vậy. Để toà "biến mất" phải dùng luật suy luận ("tan khi bị toà mới chồng lên") kèm kẹp năm bằng bản đồ (§11).
   - Trên hình và trong mô tả phải ghi rõ đây là phương pháp suy luận. Lời hứa vẫn giữ nguyên.

**Vì sao không chuyển:**
- **Helsinki** chỉ chính xác đến năm, không đến ngày: 72,5 % "ngày hoàn công" rơi vào 31/12 hoặc 01/01. Thành phố này không có mô hình 3D lịch sử theo từng toà, và cầu thấp hơn.
- **Detroit** ở mức VÀNG, giấy phép cổng dữ liệu chưa rõ, và phải số hoá Sanborn 180–330 giờ.
- Zürich đã vượt cả hai ở đúng điểm yếu cũ (cầu), nhờ số đo của phiên này.

**Rủi ro chính:**
- **Cửa sổ ngắn.** Đã có 5 video Zürich dạng AI trong 33 ngày. Sau Budapest, Zürich có thể là thành phố kế tiếp bị làm dồn dập.
  - Lợi thế của mình là độ đúng và cơ chế, đúng thứ mà 12/20 bình luận đang chê ở các video kia.
  - Đề nghị phát hành sớm.
- **Hero tốn công:** ước 210–305 giờ cho 6 toà nếu dựng mới hoàn toàn (§10). Đề xuất giảm còn 4 toà và dùng mesh 4D có texture 8K làm nền.

## 2. Bước 1 — Neo nguồn gốc (`tienky/neo.json`)
| # | Neo của công thức | Kết luận | Nguồn gốc · as of | Trích nguyên văn (rút gọn) |
|---|---|---|---|---|
| N1 | Đỉnh 440 180 năm 1962 | **ĐÚNG** | Statistik Stadt Zürich, OGD BEV324OD3243, CC0 (SHA `309311a0…`, khớp tienky-thanhpho) · đọc 16/10 | dòng `1962,440180` |
| N2 | Đáy 355 901 năm 1989 | **ĐÚNG theo chuỗi Thành phố**: giảm liên tục mỗi năm 1963–1989 (Z65) | như N1; Zürcher Statistische Nachrichten | `1989,355901` |
| N3 | Vượt đỉnh năm 2022 | **ĐÚNG, KÈM ĐIỀU KIỆN** (§1) | Statistik Stadt (Z66) ↔ Kanton Gemeindeporträt chỉ số 133 (K04) | `2022,443037` ↔ `261,Zürich … 2025,439039` |
| N4 | 8 677 toà phá 1999–2026, 9 784 toà xây | **ĐÚNG** (GWR trích xuất 15/10/2026; năm 2026 chưa trọn, 504 vụ) | BFS GWR zh.zip (SHA `d6babcae…`, khớp) | GSTAT 1007: 8 679, trong đó 8 677 có GABBJ |
| N5 | Năm giả 1812 ×436 | **ĐÚNG** | như N4 | GBAUJ = 1812: 436 |
| N6 | Không sáp nhập sau 1934 | **ĐÚNG** (nguồn năm 1994 và 1963; xem §9) | Stadtarchiv 1994; Statistisches Jahrbuch 1963 | "1934 erreichte die Stadt Zürich ihre heutige Ausdehnung." |
| N7–N9 | 1880→1893; năm của các hero; cơ chế hồ → Limmat | xem §9 | | |

## 3. Bước 2 — Hồ sơ cầu (`tienky/cau.json`, `khoang-trong.json`, `binh-luan.json`)
**Cách đo:**
- **S1:** 1 lượt `search.list`, chuỗi "Zurich history|Zürich history|Zurich timelapse" (type=video, relevance, 50 kết quả, en/US, không giới hạn ngày), cộng `videos.list` cho 50 video.
- **Bình luận:** 1 lượt `commentThreads` cho video lớn nhất.
- **Kênh:** kiểm uploads của 11 kênh timelapse từ 15/10 (`channels` + `playlistItems`), thêm 1 lượt `channels` cho hai kênh Epoch.
- **Quota:** tổng **125/200 đơn vị**. Không còn đủ cho lượt `search.list` thứ hai (100 đơn vị).

| Nhãn (LUAT-CHON-DE-TAI) | Kết quả | Căn cứ |
|---|---|---|
| Cầu-ngách (video dài 10–50 nghìn lượt trong 90 ngày) | **ĐẠT** | Epoch Timeline (kênh tạo 06/2026, 3 510 người đăng ký) "Evolution of ZÜRICH: 1,126 Years of History \| Fixed-Camera Timelapse": 34 505 lượt, 571 s, đăng 13/09/2026 |
| Nổ-mẫu (≥ 500 nghìn trong 90 ngày) | KHÔNG cho Zürich riêng | dạng "thành phố mọc 3D" là Nổ-mẫu (theo R&D) |
| Cầu-bền | KHÔNG | video dài lớn nhất có tên Zürich là 34 505 lượt. Video 4,73 triệu lượt là một Short 60 s về sự hình thành Thuỵ Sĩ |
| Khoảng trống ĐK2 | **ĐẠT** (cả hai nhánh) | 0/5 video có nguồn số liệu; 12/20 bình luận chỉnh sai |

**Cung Zürich đã có** (đều dạng máy quay cố định dựng hình, quanh khung Limmat–Grossmünster):

| Video | Kênh · ngày | Lượt | Dài |
|---|---|---|---|
| Evolution of ZÜRICH: 1,126 Years of History | Epoch Timeline · 13/09 | 34 505 | 9,5 phút |
| Evolution of Zürich: 12,000 Years | Epoch Timelapse · 12/10 (tự khai AI) | 787 | 8,2 phút |
| Zurich, Switzerland: From Early Settlement… | Distant Rain Memories · 04/10 | 19 | 10,8 phút |
| Zurich in 1,000 Years (Short) | History Unsealed · 23/09 (tự khai AI) | 975 | 27 s |
| 1,100 Years of Zurich in 60 Seconds (Short) | EraScapes · 13/09 | 281 | 60 s |

- **11 kênh timelapse:** từ 15/10 đăng New York, Warsaw (Latos), Los Angeles (Cornerstone), Rome (Timeline Cities), Shanghai, Constantinople. Chưa kênh nào làm Zürich, Helsinki, Detroit hay Sevilla.
- **Sửa điểm của phiên chọn thành phố:** Cầu Zürich 2 → **3**, Khoảng trống 5 → **4**. Tổng vẫn 21/25 và vẫn đứng đầu.
- **Điều khán giả soi** (để đưa vào lời): vị trí công trình đúng bờ sông, nhà khung gỗ chỉ có sau khoảng 1150–1200, không có nhà cao tầng trước thời hiện đại, chuông Grossmünster thay năm 1889. Đây là lý do mỗi toà phải có năm và nguồn.

## 4. Bước 3 — Nghịch lý, cặp tương phản, nhân vật, chương
### 4.1 Nghịch lý một câu
> **"One of the richest cities on Earth spent twenty-seven years losing people — 440,180 in 1962, 355,901 in 1989. It couldn't grow outward: its borders haven't moved since 1934. So it did the only thing left. It tore itself down and built again — 8,677 buildings demolished since 1999 — and only then, by its own count, beat its old record."**
- Các claim của nghịch lý: Z63, Z64, Z65 (dân số); Z01 (ranh giới); G01 (phá và xây); Z66 + K04 (vượt đỉnh, kèm điều kiện).

### 4.2 Cặp tương phản NƠI (đã tự kiểm số)
Đề xuất của lệnh là thành phố ↔ các xã ngoại ô hưởng phần tăng dân 1962–1989. Phép tự kiểm dùng **một nguồn, một định nghĩa cho cả hai phía**: Kanton Zürich Gemeindeporträt, chỉ số 133 (SHA `d6533604…`). Đã bỏ các dòng xã "(bis …)" để không đếm trùng; tổng các xã còn lại khớp mã 0 "ganzer Kanton" ở mọi năm đã kiểm.

| Phía | 1962 | 1989 | Thay đổi | Màu đề xuất |
|---|---|---|---|---|
| **A: Thành phố Zürich** (số của Bang) | 440 784 | 346 678 | **−94 106** (−21,3 %) | xanh hồ lạnh, tối dần |
| **B: phần còn lại của bang** (159 xã) | 561 344 | 798 844 | **+237 500** (+42,3 %) | vàng ngói ấm |
| B1: vành 18 xã giáp ranh | 107 777 | 153 909 | **+46 132** (+42,8 %) | vàng đậm |
| Ví dụ: Greifensee | 440 | 5 306 | **×12,1** | |
| Ví dụ: Volketswil | 2 204 | 12 040 | +9 836 (tăng nhiều nhất về số tuyệt đối) | |

- **Kết luận: cặp tương phản ĐÚNG và mạnh.** Thành phố mất khoảng 94 nghìn người, trong khi phần còn lại của bang được khoảng 237 nghìn.
- Có nguồn gốc độc lập đi kèm (Z73): tỷ trọng dân của thành phố trong vùng đô thị giảm từ 68,1 % (1950) xuống 41,7 % (1990).
- **Lưu ý:**
  - Số Bang của thành phố thấp hơn số Thành phố khoảng 2,5 % (Z68). Trong cặp này dùng số Bang cho cả hai phía; bộ đếm chính vẫn dùng số Thành phố.
  - Danh sách 18 xã giáp ranh do phiên tự lập. Phải kiểm lại bằng lớp ranh giới xã ở G1.

### 4.3 Nhân vật người thật có hồ sơ (`tienky/nhan-vat.json`, HLS)
| # | Nhân vật | Chương | Muốn → bị cản → kết cục (theo nguồn) | Claim | Hình |
|---|---|---|---|---|---|
| 1 | **Unio**, trưởng trạm thuế Statio Turicensis (~200) | 1 | thu thuế 2,5 % ở cửa hồ; ta chỉ biết ông qua tấm bia mộ con trai, tìm thấy trên Lindenhof năm 1747 | Z29–Z32 | bia mộ (tư liệu; quyền ảnh phải kiểm ở G1) + A-lite người thu thuế |
| 2 | **Rudolf Brun** (†1360) | 1 | hiệp sĩ bị gạt khỏi Hội đồng, liên minh với thợ thủ công (1336); muốn mở quyền lực dọc đường nước, xuôi Limmat và hồ; thị trưởng suốt đời, chế độ bị bãi sau khi ông mất | Z49, Z77–Z79, Z92 | A-lite (đạo cụ: chìa khoá thành, cờ phường hội) |
| 3 | **Alfred Escher** (1819–1882) cùng kiến trúc sư **J. F. Wanner** | 3 | lập Nordostbahn 1853, góp phần lập Polytechnikum 1855; đường sắt 1847 bị kẹt ở Baden; bị buộc rời Gotthardbahn năm 1878 và không được mời dự lễ thông hầm 1880 | Z55–Z57, Z83–Z86, Z93 | tượng Escher trước ga (có trong ảnh BAZ 1893, TN1) |
| 4 | **Arnold Bürkli** (kỹ sư thành phố 1860–1882) | 3 | Bahnhofstrasse trên hào Fröschengraben; ven hồ Bürkliplatz 1881–87 | Z58, Z59, Z81, Z82 | A-lite kỹ sư + Kellerplan 1864 |
| 5 | **Emil Klöti** (Stadtpräsident) | 4 | kế hoạch Đại Zürich 1915; đề án lớn (có cả Kilchberg, Zollikon giàu có) bị bác ngày 12/5/1929; sáp nhập 8 xã 1934; mong sáp nhập thêm "erfüllte sich allerdings nie"; hai lần trượt Hội đồng Liên bang | Z02, Z16, Z17, Z88, Z89 | ảnh chân dung: chưa tìm (dùng chữ + A-lite) |
| (nhóm) | **"The families who left"** 1962–1989 | 6 | hộ nhỏ dần (2,7 → 1,8 người/căn), diện tích ở mỗi người tăng 0,5 m²/năm; dời ra Greifensee, Volketswil… | Z69–Z72, K01–K03 | A-lite gia đình + xe chuyển nhà trên bản đồ |

Dự phòng: Zwingli, Semper, Jos Murer (hồ sơ có sẵn). Murer có thể dùng làm "người cầm máy" của lát 1500, vì bản đồ Murer 1576 là một trong các nguồn của 4D.

### 4.4 Chương (Kinh thánh §3: 9–11 phút; ~150 từ/phút) — xương sống 1357 → 2026 cùng ba nhịp lặn cơ chế
| # | Tên chương (EN) | Nhân vật | Nội dung (claim) | Mốc đinh · nhịp lặn | Thời lượng |
|---|---|---|---|---|---|
| 0 | *504 Buildings This Year* (móc ≤ 45 s) | — | 2026: 504 toà phá tính tới 15/10 (G01) → nghịch lý (Z63–Z65) → 2 sự thật: ranh giới đứng yên từ 1934 (Z01); thành phố mất 1 trong 5 người dân (−19,1 %) → một con số: 84 279 → câu hỏi trùng tiêu đề → hứa cú lật ("it grew by tearing itself down") | — | 0:45 |
| 1 | *A Toll Booth Where the Lake Ends* | Unio, Brun | hồ chảy ra Limmat (Z28), trạm thuế 2,5 % (Z29–Z32), nơi chuyển tải hàng (Z33, Z37); thuyền Limmat bị bán ở Baden (Z38); Fraumünster 853, Grossmünster (Z46, Z47); 1357: 6 600 dân (Z61); Brun và đường nước (Z78) | M1 · M2 · **lặn #1: chuyển tải hồ → sông** (TB-limmat) | 1:30 |
| 2 | *Four Hundred Years, Ten Thousand People* | (Murer) | dân gần như đứng yên: 6 600 (1357) → 10 000 (1799); thành luỹ Barock từ 1642 gấp đôi diện tích trong tường (Z52); 4D 1500 ghost → 1800 đặc; "accurate to the decade" | M3 · TB-schanzengraben | 1:15 |
| 3 | *Tear Down the Walls, Bring In the Trains* | Escher, Wanner, Bürkli | 30/1/1833 quyết định phá luỹ (Z53, Z54); 9/8/1847 tuyến sắt đầu tiên, kẹt ở Baden (Z55, Z56); ga 1865–71 (Z57); Bahnhofstrasse 1863–64 (Z58) | M4 · M5 · TB-bahnhofstrasse · **TN1** | 1:30 |
| 4 | *The Suburbs That Were Bigger Than the City* | Klöti | 1880: các xã gấp đôi thành phố (Z04); Aussersihl 558 → 19 767 (Z42); các xã vỡ ngân sách (Z10); 1893 (Z08, Z09, P01) → thành phố lớn nhất (Z11); 1929 bị bác, 1934 được (Z16, Z17); diện tích gấp đôi (Z13); không sáp nhập thêm (Z01–Z03) | M6 · M7 · **lặn #2: ranh giới khoá lại** | 1:45 |
| 5 | *Peak: 440,180* | — | 1934 → 1962 lên đỉnh (Z63); cùng năm 1962 Altstadt được bảo vệ (Z60) | M8 · TN2 (nếu khớp) | 0:45 |
| 6 | *Richer, and Emptier* | "the families who left" | 1963–1989 năm nào cũng giảm (Z65); 2,7 → 1,8 người/căn (Z69); +0,5 m²/người/năm (Z70); hộ một người (Z71); gia đình ra ngoại ô (Z72); cặp tương phản K01–K03 và Z73; **the honest part**: hai cách đếm (Z68, K04), "Citybildung" không phải nguyên nhân có nguồn cho giai đoạn này | **lặn #3: một căn hộ, ít người hơn** | 1:45 |
| 7 | *Tear Down, Build Up* | — | 8 677 toà phá từ 1999, phần lớn xây trong khoảng 1920–1969 (G01, G02); 9 784 toà mới; vượt đỉnh năm 2022 "by the city's own count" (Z66); 452 421 năm 2025 (Z67); điều cần theo dõi: số phá của năm 2026, số dân cuối 2026 | TB-limmat 2026 · bảng điểm | 1:30 |
| — | Kết | | quay về khung mở đầu; câu chốt: *"Zürich didn't grow out. It grew in — one demolition at a time."*; dẫn sang tập "co lại" kế (Detroit) | | (gộp ch.7) |

**Tổng ≈ 10:45**, 8 chương (0–7). Lời mời đăng ký nhẹ ở cuối ch.2 (~3:30). Nhịp lặn: 3. Mốc đinh: 8.

## 5. (Bước 3 mở rộng) Nêu trước các phản biện
| Khán giả sẽ nói | Trả lời bằng |
|---|---|
| "It's the banks / tax" | **không mở khung này** (giữ mức XANH). Câu hỏi của tập là vì sao dân giảm, và câu trả lời có nguồn nằm ở chuyện nhà ở và ranh giới (Z69–Z73) |
| "Zürich didn't shrink, people just moved to Oerlikon" | Oerlikon nằm trong thành phố từ 1934; dân rời ra các xã **ngoài** ranh giới (K01, K02) |
| "It already passed the record" / "No it didn't" | hai cách đếm, nói cả hai (Z68, K04) |
| "Wrong river bank / houses too early" (bình luận ở video cùng loại) | mỗi toà có năm từ sổ; toà mất dùng mô hình 4D của chính thành phố, ghi "hypothesis" khi độ tin cậy thấp |

## 6. Bước 4 — Danh mục claims (`tienky/claims.json`: **103 claim**; 99 XÁC MINH, 4 MÂU THUẪN, 0 chờ nguồn)
| Nhóm | Claim | Nguồn chính |
|---|---|---|
| Nguồn còn thiếu A1–A4 | Z01–Z41 | Stadtarchiv 1994 và 1993 (bản quét ZB), Statistisches Jahrbuch 1934/1963, HLS (Zürich Gemeinde, Limmat, Zürichsee, Wasserwege, Schiffbau, Zölle), Stadtarchäologie, Grün Stadt Zürich, Swiss Prime Site, ETH |
| Mốc lịch sử | Z44–Z60, Z92, Z94 | HLS, UVEK, Stadtarchiv |
| Dân số | Z42, Z43, Z61–Z68 | OGD BEV324OD3243, Statistik Stadt (bài trực tuyến), Zürcher Statistische Nachrichten |
| Cơ chế co lại | Z69–Z76 | Statistik Stadt ("Wie viel Wohnfläche…", "Home alone"), Quartierspiegel City 2026, HLS |
| Nhân vật | Z77–Z90, Z93 | HLS |
| Tự tính (P) | K01–K04, G01–G03, D01, P01 | Kanton Gemeindeporträt 133, GWR, Zürich 4D |

**Bốn MÂU THUẪN và cách nói:**
- **Z25:** toà chính ETH xây 1859–1864 (HLS Semper) hay 1861–1864 (HLS ETH) → nói "finished in 1864".
- **Z59:** khu ven hồ 1881–1887 hay 1882–87; HLS Enge ghi 1887 → nói "in the 1880s".
- **Z62:** dân số 1880 là 25 102 (CSV) hay 24 453 (Volkszählung) → trong lời dùng số Volkszählung khi tách theo xã, số CSV khi chạy bộ đếm; nhãn ghi rõ nguồn.
- **K04:** vượt đỉnh hay chưa vượt → giải ở §1.

**Không dùng** (`claims.json → khong_dung`, 12 mục):
- "Romans founded Zürich in 15 BC";
- mặt đồng hồ "8,7 m";
- "Prime Tower is Switzerland's tallest" (chỉ nói "when it opened");
- sáp nhập "12 xã" (dùng "eleven");
- "1893 = 117 044";
- khung ngân hàng;
- diện tích "87,9 km² không đổi";
- ngày 7/8/1847;
- Citybildung là nguyên nhân của 1962–1989;
- câu "beat its record" khi không nêu nguồn;
- "8 677 since" một năm trước 1999.

## 7. Bước 5 — Tài sản hình (`tienky/hero.json`, `licenses/` 12 tệp)
| Tầng | Tài sản | Giấy phép · ghi công |
|---|---|---|
| Toà còn đứng | GWR (điểm, năm) + LoD2 Dachmodell (khối, mái) | BFS: ghi nguồn bắt buộc; LoD2: CC0 |
| Toà đã mất | Zürich 4D: lát 200, 1200, 1500, 1800 (OBJ + texture) | CC0 |
| Bản đồ lịch sử | 8 lớp (Murer 1566, Gyger ~1644/1667, Wild 1843–51, Dufour, Altstadtkataster 1859–67, Kellerplan 1864, Siegfried, Übersichtsplan 1932–61) | CC0 / "© swisstopo" |
| Ảnh lịch sử | 7 ảnh BAZ 1890–1902 (OGD "Historische Bilder", CC0); LoC Photochrom ("No known restrictions"); e-rara ETH/ZB (Public Domain Mark) | ghi "Baugeschichtliches Archiv, Amt für Städtebau, Stadt Zürich" theo điều khoản E-Pics |
| Ảnh hiện đại kiểm vật liệu | Wikimedia Commons (CC0, CC BY, CC BY-SA; đã kiểm từng tệp) | **chưa tải** (Commons trả 429); chỉ có SHA-1 của Commons |
| **KHÔNG dùng** | ảnh E-Pics loại CC BY-NC / Restricted; ảnh KGS "© BABS" (chưa đọc được giấy phép); OSM (không cần) | |

**Footage:** đề xuất **≈ 5 %** (~30 s; trần 20 % là tối đa, không phải chỉ tiêu).
- Phần này chỉ gồm ảnh 1890–1902, dùng làm bằng chứng sự việc (ga, cầu, phố đã đổi) và quy mô.
- Không footage phim. Không stock hiện đại: năm 2026 dựng bằng 3D cộng ảnh chỉnh hình CC0.

## 8. Bước 6 — Mức rủi ro (QUAN-TRI-RUI-RO)
**XANH.** Câu hỏi là chuyện quy hoạch, nhà ở và ranh giới. Không có cá nhân còn sống làm trục, không tranh chấp, không thời sự đang mở.

| Tránh | Dùng thay |
|---|---|
| "banking city", "bank secrecy", "tax haven", "Swiss money" | không nhắc; nếu buộc phải nhắc (Kreditanstalt 1856 tài trợ đường sắt) thì một câu trung tính, có nguồn, kèm câu miễn trừ tài chính, **và nâng lên VÀNG** |
| "Zürich beat its record in 2022" (không nêu nguồn) | "by the city's own count…" + đoạn honest part |
| "every building at its exact year" | lời hứa đã duyệt: "Standing buildings from the federal register; lost buildings from the city's own 3D reconstructions (hypothesis where marked)." + "accurate to the decade" trước 1800 |
| "people fled the city" (giọng giật gân) | "families moved to the towns next door" (Z72) |

**Thứ tự mức:** T2 và T3 là VÀNG; T4 đề xuất XANH; T5 XANH → hợp luật.

## 9. Bước 8 — Bốn nguồn còn thiếu (TIEN-KY-THANHPHO §11.4)
| # | Câu hỏi | Kết quả | Trích nguyên văn · nguồn |
|---|---|---|---|
| A1 | Không sáp nhập sau 1934 | **CÓ NGUỒN** (năm 1994, 1963). Chưa có câu tương đương trên trang hiện hành; ranh giới OGD 2026 khớp 34 Quartier | "1934 erreichte die Stadt Zürich ihre heutige Ausdehnung." (Stadtarchiv 1994) · "Seit 1934 heutiges Stadtgebiet" (Jahrbuch 1963) · về mong muốn sáp nhập thêm của Klöti: "erfüllte sich allerdings nie" |
| A2 | Tách phần tăng dân 1880→1893 do sáp nhập | **ĐÃ TÁCH** | Volkszählung 1888: thành phố cũ 27 644, 11 xã 66 485 (đủ số từng xã, Z06, Z07). Năm 1880: 24 453 và 53 886. Ngày 1/1/1893: 107 416. Bỏ phiếu bang 9/8/1891, 37 843 thuận / 24 904 chống |
| | → phép tách | | Trên lãnh thổ 1893, dân tăng **78 339 (1880) → 107 416 (1/1/1893), +37 %**: đây là phần tăng thật. Phần còn lại của bước nhảy 25 102 → 107 416 là do **đổi ranh giới**. Khoảng 7/10 cư dân của Đại Zürich (70,6 % theo số 1888) sống ở ngoài thành phố cũ |
| | 1934 | | 8 xã có 41 117 người (1930). Ngày 1/1/1934 nhập 48 323 người; dân từ 264 971 lên 313 294; diện tích từ 4 480 lên 8 773 ha. Bỏ phiếu 5/7/1931, 69 967 / 33 544 |
| A3 | Năm của St. Peter, ETH, Prime Tower | **CÓ NGUỒN** | St. Peter: nhắc lần đầu năm 857 (HLS), mặt đồng hồ của Luterer năm 1538 rộng 8,64 m, xây lại 1705–06 · ETH: thành lập 1855 (ethz.ch, HLS), toà chính Semper xong 1864, vòm 1919/20 · Prime Tower: 126 m, khánh thành 6/12/2011 (Swiss Prime Site) |
| A4 | Cơ chế hồ → Limmat | **CÓ NGUỒN** | "Die Limmat tritt bei Zürich aus dem Zürichsee" (HLS Limmat); "Umlad- und Etappenort" (Stadtarchäologie); bia mộ ~200 ghi "Statio Turicensis", thuế quadragesima Galliarum 2,5 %; thuyền Limmat bán ở Baden hoặc Basel; năm 1447 được miễn thuế đường thuỷ xuôi Limmat và sông Rhein |

## 10. Bước 9 — HERO (`tienky/hero.json`)
Hình học lấy từ LoD2 Stadt Zürich (WFS theo ô; tệp CityGML toàn thành phố nặng 270 MB). Đã đối chiếu với swissBUILDINGS3D 2.0 ô 1091-41: khớp đến cm ở 4 toà. Chiều cao tính trên địa hình swissALTI3D, vì mặt đất trong LoD2 thấp hơn địa hình thật 3–6 m.

| Hero | EGID | Mặt bằng (m) | Cao trên mặt đất | Tư liệu dùng được | Có sẵn trong 4D 1800 | Ước giờ (ước) |
|---|---|---|---|---|---|---|
| H1 Grossmünster | 302040349 | 55,5 × 28,2; 2 tháp ~12 × 12 | ~57 m (đỉnh LoD2 472,3) | 2/3 (BAZ ~1890 CC0; bản vẽ 1840 PDM — điều kiện) | mesh 5 630 tam giác + texture 8K | 40–60 |
| H2 Fraumünster | 302040792 | 62,3 × 31,1 | ~76 m (mũi nhọn) | 4/5 (BAZ 1901, 1902; LoC; e-rara); **không có bản vẽ** | mesh 3 342 tam giác + 8K | 35–50 |
| H3 St. Peter | 302040601 / 302040793 | tháp 10,7 × 10,5; thân 40 × 29,5 | ~58–63 m | 3/4 (BAZ ~1900; bản khắc 1706 ít giá trị) | mesh 6 886 tam giác + 8K | 25–35 |
| H4 Hauptbahnhof (Wanner) | 140889 | khối chính 139 × 44 | ~25 m | **6/6** (BAZ ~1893, ~1900; LoC Photochrom 7323 px; e-rara 1889–1900; bản vẽ 1898) | không (sau 1800) | 50–70 |
| H5 ETH (Semper) | 3169989 | 151 × 118 | ~46 m (vòm) | 4/4; **cần 2 biến thể** (trước và sau khi xây vòm 1919/20) | không | 45–65 (+8–12) |
| H6 Prime Tower (tuỳ chọn) | 302030099 | 65 × 33 | 125,8 m (chủ toà ghi 126) | 1/1 (CC BY-SA) | không | 15–25 |

**Phát hiện từ phép đo giảm lưới:**
- Hero trong 4D là khối đơn giản, với mặt đứng **vẽ** trên texture 8K: cửa sổ và hoa văn là ảnh, không phải hình học.
- Khối này đủ cho toàn cảnh và trung cảnh, nhưng không đủ cho cận cảnh (ảnh so sánh ở trần 2048 cho thấy hoa văn tháp bị mờ).
- Ghép 4D 1800 với GWR theo EGID cho thấy 4D dùng EGID 302040792 cho Fraumünster và 302040793 cho St. Peter. LoD2 cũng có EGID 302040793 cho St. Peter, nên hai lớp nối liền mạch.

**Đề xuất:** dựng hero chi tiết cho **H1, H2, H4** (ba mốc đinh M2, M5 và TN1). H3 dựng ở mức trung cảnh, dựa trên mesh 4D. H5, H6 dùng LoD2 cộng texture. Tổng ước **≈ 150–215 giờ**, thay vì 210–305 giờ.

**Chỉ số trong ±5 %** (đối chiếu đo đạc, không phải ngưỡng luật):
- diện tích ETH so với GWR: −0,03 %;
- diện tích Prime Tower: −1,9 %;
- chiều cao Prime Tower: −0,2 %.

## 11. Bước 10 — Kế hoạch dữ liệu xương sống (`tienky/xuong-song.json`, `dan-so.json`)
| Lớp | Vai | Số đo / luật chính |
|---|---|---|
| L1 GWR | toà còn đứng mọc đúng năm; toà phá 1999–2026 tan đúng năm | 54 185 toà đang đứng (100 % có năm); 8 677 GABBJ; 1812 ×436 không "mọc"; trước 1800 "accurate to the decade" |
| L2 LoD2 | khối và mái thật | nối GWR theo EGID; toà đã phá không có trong LoD2 hiện hành → khối từ footprint lịch sử hoặc theo GASTW, ghi "approximate massing" |
| L3 4D 1200/1500/1800 (+200) | toà đã mất | lát 1800: 5 613 vật thể, **591 EGID thật** (588 còn đứng), 4 699 EGID âm, 316 không EGID. Lát 1200: 0 EGID thật. Độ tin cậy "tief" → **ghost alpha ~0,35 + nhãn "reconstruction (hypothesis)"**; giữa các lát chỉ hoà chéo, không nội suy từng toà |
| L4 dân số | bộ đếm, mốc 1962/1989/2022 | chuỗi Thành phố; bước nhảy 1893/1934 có nhãn "merger" |
| L5 8 lớp bản đồ | nước, tường, đường theo thời; kẹp năm cho toà mất 1800–1999 | CC0 / © swisstopo |
| L6 ranh giới theo năm | vạch ranh giới sống | gộp 34 Quartier (CC0): trước 1893 ≈ 180 ha (Kreis 1); 1893–1933 ≈ 4 851 ha; từ 1934 ≈ 9 188 ha. So với số chính thức 4 480 và 8 773 ha: **lệch +8 % và +5 %**, chủ yếu do mặt hồ → cắt hồ ở G1 |
| L7 địa hình, nước | nền | nước theo lát 4D, không dùng bờ hồ hiện đại cho năm 1800 (ven hồ Bürkli là đất lấp 1880s) |
| L8 ảnh chỉnh hình | tầng giữa của zoom; NOW | Kanton 2024/25, Stadt 1975–2007 (CC0), SWISSIMAGE |

**Luật nối 1800 ↔ GWR** (mới; đo được nhờ EGID):
- Trong 588 toà còn đứng có trong 4D 1800, GWR ghi:
  - năm ≤ 1800 cho 243 toà → nối liền;
  - mã giả 1812 cho 164 toà → nối liền, không "mọc";
  - năm > 1800 cho **181 toà** → toà 4D tan và toà GWR mọc ("replaced on the same site"). Ca 1801–1850 kiểm tay, ước 2–3 giờ.
- 4 699 toà EGID âm (đã mất, không có năm phá): tan khi một toà GWR mọc chồng lên ≥ 30 % diện tích (tự động). Phần còn lại kẹp năm bằng Altstadtkataster 1859–67, Siegfried 1880/1930 và Übersichtsplan 1932–61.
- Cách hiểu "EGID âm = toà đã mất" là **suy luận từ quy ước đặt tên**. Cần xác nhận với Stadtarchäologie trước khi đọc câu D01 trong lời.

**Số hoá tay (ước): 53–89 giờ**, chưa kể hero:
- kẹp năm toà mất: 40–70 giờ;
- ranh giới xã cũ: 3–4 giờ;
- thành luỹ: 4–6 giờ;
- bờ hồ và Fröschengraben: 4–6 giờ;
- 181 ca EGID lệch năm: 2–3 giờ.

Phiên chọn thành phố ước 80–130 giờ. Số mới thấp hơn vì 4D đã có sẵn texture và EGID.

**Ngôn ngữ hình** (`tienky/hinh-xuong-song.json`, `tuyen-bay.json`):
- **8 mốc đinh:**
  - M1 ~200 (trạm thuế);
  - M2 853 (Fraumünster và Grossmünster);
  - M3 1642 (thành luỹ);
  - M4 1833 (phá luỹ);
  - M5 1847 (đường sắt, ga);
  - M6 1893 (sáp nhập);
  - M7 1934 (sáp nhập);
  - M8 1962 (đỉnh dân);
  - năm 2022 là bảng điểm kết, không phải mốc đinh.
- **4 tuyến bay**, hình học OGD CC0, lấy mẫu mỗi 25 m:

  | Tuyến | Độ dài | Ghi chú |
  |---|---|---|
  | TB-limmat | 1 127 m | đoạn Quaibrücke → Münsterbrücke khoảng 200 m nối thẳng |
  | TB-bahnhofstrasse | 1 229 m | |
  | TB-schanzengraben | 1 660 m | hào Barock còn nước tới nay |
  | TB-limmatquai | 1 044 m | |

- **Mở chương:** reveal và glide → zoom-in xen kẽ ở cả 8 chương.
- **Then/now:**
  - TN1 GIỮ: BAZ "Bahnhofplatz Hauptbahnhof" ~1893. Tượng Escher và mặt Wanner gần như không đổi, nên có điểm khống chế tốt.
  - TN2 ĐIỀU KIỆN: BAZ "Rathausbrücke" ~1900, với tháp St. Peter.
- **Ngân sách chữ:** ≤ 15 % diện tích khung.
- **Chuẩn 4 lớp:**
  - hero: H1–H6;
  - nhà thường: texture Fachwerk/Steinwand có cửa sổ của 4D, và LoD2 + shader cửa sổ theo số tầng GWR;
  - nền sống: nước theo lát, cây, thuyền và tàu A-lite;
  - ánh sáng: sepia trước 1847, sau đó chuyển dần sang tự nhiên.

## 12. Bước 11 — Đo giảm lưới gói OBJ Zürich 4D (`tienky/giam-luoi.json`)
Máy 4 vCPU, 15 GB RAM, không GPU; Blender 5.2.2 LTS, Workbench. Gói và ảnh render để ngoài git. Trong git chỉ có số đo và lệnh.

| Gói | Tải | Nội dung | Tam giác (đọc tệp / sau import) |
|---|---|---|---|
| **1800** (960 MB, SHA `48cd6c4d…`) | 386 s | 5 613 OBJ (33,7 MB) + **146 PNG = 950 MB**; 6 texture 8K (Fraumünster, St. Peter, Rathaus, Grossmünster, Helmhaus, Waisenhaus), 13 texture 4K | 300 606 / **300 300** |
| **1200** (529 MB, SHA `602632b5…`) | 187 s | 68 571 OBJ (291 MB) + 91 texture (430 MB) | 3 066 175 / 2 311 189. Trong đó **rào (64 450 vật) và hàng cọc (88 vật) chiếm khoảng 90 %**; toà nhà ~286 nghìn |

**Giảm lưới** (sai số = khoảng cách gần nhất hai chiều, tính bằng mét; Δ điểm ảnh = render 960×540 so với bản gốc ở cùng camera):

| Phép | Tam giác sau | Thời gian | Sai số p99 / max | % điểm ảnh lệch > 10/255 (toàn cảnh / gần) | Kết luận |
|---|---|---|---|---|---|
| 1800 planar 1° | 292 046 (97,3 %) | 1,5 s | 0,000 / 0,10 | 1,5 / 0,8 | gần như không mất, nhưng gần như không lợi |
| 1800 collapse 0,5 | 150 150 (50 %) | 0,7 s | 2,39 / 106 | **35,2 / 37,3** | **loại**: UV mặt đứng méo, cửa sổ bị kéo xiên (đã xem ảnh) |
| 1800 collapse 0,25 / 0,10 | 75 k / 30 k | < 1 s | 4,6 / 23,3 | 42 | loại |
| 1200 rào + cọc planar 1° | 1 966 274 (97,1 %) | 10,8 s | 0 / 0 | 0,2 / 0,1 | không lợi |
| 1200 rào + cọc collapse 0,5 | 1 012 394 (50 %) | 8,1 s | 0,04 / 0,23 | 0,3 / 0,3 | đạt |
| **1200 rào + cọc collapse 0,25** | **506 197 (25 %)** | 9,1 s | **0,07 / 0,97** | **0,4 / 0,3** | **ĐỀ XUẤT** |
| 1200 rào + cọc collapse 0,10 | 202 478 | 9,6 s | đỉnh bay tới km | 9,5 / 8,3 | cấm |

**Texture 1800** (render 1920×1080, ba khung: Limmat, Grossmünster ~95 m, St. Peter ~95 m):

| Chính sách | Dung lượng | Thời gian tạo | PSNR (gần / Grossmünster / St. Peter) | % > 10/255 ở hero | Kết luận |
|---|---|---|---|---|---|
| PNG gốc | 950 MB | — | — | — | |
| JPEG q90, cùng độ phân giải (bỏ alpha, vì alpha = 255) | 388 MB | 86 s | 54,9 / 52,6 / 52,7 dB | 0,0 | **mặc định** |
| trần 4096 | 365 MB | 87 s | 53,0 / 47,2 / 48,7 dB | ≤ 0,1 | toàn cảnh, trung cảnh |
| trần 2048 | 339 MB | 88 s | 47,4 / 39,4 / 42,9 dB | 1,0–2,9 | chỉ nền xa (mắt thấy hoa văn và ngói bị mờ) |

**Kết luận đo:**
1. Gói 1800 **không cần giảm lưới**: 300 nghìn tam giác là quá nhẹ. Việc cần làm là quản lý texture: JPEG q90; texture 8K cho cận cảnh và trung cảnh, 4K cho toàn cảnh. RAM giải nén 1,6 GB → 0,4 GB.
2. Gói 1200: giảm riêng rào và hàng cọc bằng collapse 0,25. Cảnh còn khoảng 0,79 triệu tam giác. Tốt hơn nữa là instancing (G1).
3. **Bắt buộc dời gốc toạ độ LV95 trước khi đưa vào float32.** Toạ độ ~2,68 triệu m sẽ rung khoảng 0,25 m.
4. **Giờ máy:** 13,2 phút tính toán, 22,8 phút nếu tính cả tải về. Còn xa trần 2 giờ.

**Lệnh đã chạy** (script nằm ở scratch phiên, không commit): `merge_obj.py`, `decimate_4d.py` (bpy), `tex_policy.py`, `tex_render.py`. Chi tiết ở `giam-luoi.json → lenh`.

## 13. Bước 7 — Gói sơ bộ
| # | Tiêu đề | Ký tự | Ghi chú |
|---|---|---|---|
| 1 | **Why Zürich Shrank While Getting Rich** | 36 | đề xuất chính (chủ dự án đã duyệt) |
| 2 | Zürich Tore Down 8,677 Buildings. Then It Grew. | 47 | số khớp G01; "then it grew" đúng theo số của Thành phố |
| 3 | The Rich City That Lost 84,000 People | 37 | 440 180 − 355 901 = 84 279 |

```
THUMBNAIL BRIEF — K2C-T5-01
[A] BẢN ĐỒ TƯƠNG PHẢN
- Nền: render 3D của mình, ranh giới thành phố 1934 (nét trắng dày) trên chỉnh hình CC0 + hồ Zürich, nhìn chếch từ nam.
- Trong ranh giới: toà nhà xanh lạnh, tối dần. Vành xã ngoài: vàng ngói sáng lên (Greifensee, Volketswil nổi rõ).
- Chữ (1 hộp, nền tối): A1 "−84,000" (Z63/Z64) | A2 "SHRANK" (chữ khác).
- Biểu tượng (≤ 2): mũi tên xe chuyển nhà A-lite từ trong ra ngoài ranh giới; cần cẩu nhỏ trong thành phố.
[B] PHÁ VÀ XÂY (không chữ)
- Một dãy phố Zürich 3D: nửa trái toà 1940s đang tan (hạt bụi, viền đỏ, đúng năm GABBJ), nửa phải toà mới mọc cao hơn, cùng khung.
- Không cờ, không logo ngân hàng, không ký hiệu tiền.
Chung: tiêu đề hỏi, thumbnail cho thấy; mọi số có trong video; lề 5 %; tránh góc dưới-phải.
Test & Compare: A1, A2, B.
```

**Short đi kèm:** *"Every building Zürich tore down since 1999 — in 45 seconds."* 8 677 toà tan đúng năm trên nền 3D, bộ đếm 1999 → 2026, kết bằng "and the city finally grew back" (theo số của Thành phố). Dẫn về video dài. Cầu: các Short Zürich dạng AI đạt 281–975 lượt; phần chữ trên Short phải tuân BAI-HOC-LL #6–7.

## 14. Chi phí; tệp đã ghi; đề xuất ngoài vùng
| Mục | Trần | Thực tế |
|---|---|---|
| YouTube Data API | 200 | **125**: search 100 · videos 1 · commentThreads 1 · channels 12 · playlistItems 11 |
| Claude API | $2 (ghim `claude-haiku-5-5`) | **$0,00453** · 1 lượt (khoảng trống + nhãn bình luận) · served = `claude-haiku-5-5` (`tienky/cost.jsonl`) |
| ElevenLabs | 0 | **0** |
| Giờ máy | ≤ 2 giờ | **≈ 23 phút** (gồm tải 1,6 GB gói 4D và GWR) |
| Token | trần mềm | 2 tác tử con: tra nguồn ≈ 299 nghìn, hero ≈ 293 nghìn token (bộ đếm harness); phiên chính ngoài các số này |

**Đã ghi:**
- `channel-k2/k2c-t5-01/TIEN-KY.md`.
- `tienky/`: `neo`, `cau`, `khoang-trong`, `binh-luan`, `dan-so`, `claims`, `nhan-vat`, `hero`, `xuong-song`, `hinh-xuong-song`, `tuyen-bay`, `giam-luoi`, `cost` (.json) và `cost.jsonl`. Thêm bằng `git add -f`, vì `channel-k2/.gitignore` chặn `*.json`; phiên không sửa `.gitignore`.
- `licenses/` (12 tệp): 5 tệp Zürich chép từ `tienky-thanhpho` (4D, GWR, Kanton OGD, Stadt OGD, swisstopo) và 7 tệp mới (LoD2, BAZ, e-rara, LoC Photochrom, swissBUILDINGS3D, GWR qua geo.admin, Commons). Mọi email đã thay bằng mô tả đường liên hệ.

**Đề xuất cho P** (chưa ghi, vì ngoài vùng):
1. `COST-LEDGER.csv`: `T5-01,Tiền kỳ T5 Zürich,Tiền kỳ,2026-10-16,,,,,0.0045,2,claude-haiku-5-5,0,0,,,,,,channel-k2/k2c-t5-01/TIEN-KY.md,YT 125/200 đv; 2 tác tử con; giờ máy ≈ 23 phút; không merge`
2. `RIGHTS.md`: thêm các dòng GWR, LoD2, Zürich 4D, 8 lớp bản đồ, ảnh BAZ, LoC, e-rara **khi tập dùng thật** (G1).
3. `AUTHORSHIP.md`: ghi việc chọn Zürich, góc kể, lời hứa và cặp tương phản sau khi chủ dự án duyệt.
4. `channel-k2/.gitignore`: thêm `!k2c-t5-01/tienky/*.json` và `!k2c-t5-01/tienky/*.jsonl`.
5. `HANG-DOI.md`: thêm K2C-T5-01, mức XANH.
6. `TIEN-KY-THANHPHO.md`: sửa điểm Cầu Zürich 2 → 3 và Khoảng trống 5 → 4 (§3).

**Ghép thử:** nhánh chỉ thêm tệp mới trong `channel-k2/k2c-t5-01/` (thư mục mới), nên không xung đột với `main`, `tienky-thanhpho`, `timelapse-rd`, `k2c-t3-tienky` hay `k2c-t4-tienky`.

## 15. Preflight
- `bash scripts/env/verify.sh`: 10 PASS, 3 FAIL (three.js, tifffile/pyshp, k2v node_modules). Cả 3 không liên quan việc tiền kỳ; giống phiên chọn thành phố.
- Hook pre-commit/pre-push cài đầu phiên. `tools/preflight.sh --range origin/main..HEAD`: **ĐẠT**; `checks/lock.py --verify`: **KHỚP**. Kết quả lần cuối ghi trong commit. Không dùng `--no-verify`.

## 16. Việc đang chờ chủ dự án
1. **Duyệt khuyến nghị đi tiếp Zürich** (không chuyển Helsinki hay Detroit), kèm 3 điều chỉnh ở §1. Điều chỉnh quan trọng nhất là nói "by the city's own count" khi nêu năm 2022.
2. **Duyệt cặp tương phản** thành phố ↔ phần còn lại của bang và vành 18 xã giáp ranh (§4.2), và **5 nhân vật** (§4.3).
3. **Duyệt danh sách hero** và mức dựng: H1, H2, H4 chi tiết; H3 trung cảnh; H5, H6 dùng LoD2 (≈ 150–215 giờ, thay vì 210–305 giờ). Rathaus đã đo sẵn làm dự phòng.
4. **Duyệt luật dựng mới:**
   - nối 1800 ↔ GWR theo EGID;
   - toà mất 1800–1999 "tan khi bị toà mới chồng lên ≥ 30 %", kèm nhãn phương pháp;
   - ghost alpha ~0,35 cho độ tin cậy "tief".
5. **Liên hệ Stadtarchäologie Zürich** (qua trang liên hệ Amt für Städtebau) để xác nhận ý nghĩa EGID âm trong 4D, trước khi đọc câu D01 trong lời. Nếu không có xác nhận, D01 chỉ dùng làm luật dựng.
6. **Việc kỹ thuật trước G1:**
   - tải lại 7 ảnh Commons (bị 429) và ghi SHA-256;
   - kiểm danh sách 18 xã giáp ranh bằng lớp ranh giới xã;
   - cắt mặt hồ khỏi lớp ranh giới L6;
   - kiểm quyền ảnh bia mộ Statio Turicensis.
7. **Chọn cửa sổ phát hành:** đề xuất **sớm nhất có thể**, vì đã có 5 video Zürich dạng AI trong 33 ngày.
8. **P chép các đề xuất ở §14.**
