# TIỀN KỲ T6 — "Why Detroit Shrank While Its Suburbs Grew" (K2C-T6-01)

> Phiên Tiền kỳ T6, 16/10/2026. Lệnh chủ dự án duyệt 16/10. Tập Moving Parts, mức **VÀNG**. Tập này nối tiếp T5 Zürich ("co lại khi giàu") bằng vế còn lại của cặp: "co lại khi nghèo".
> Nhánh `k2c-t6-tienky` từ `origin/main` @ `7255aa4`. **Không merge.**
> Mọi lượt xem là **số công khai YouTube Data API, đọc ngày 16/10/2026 (UTC)**. Mọi tỷ lệ, nhãn và phép cộng trừ là **tự tính**; đó không phải chỉ số của YouTube hay số chính thức.
> Mọi trích dẫn D01–D65 được chép **nguyên văn** từ tệp tải bằng curl. Một script kiểm tự động rằng mỗi đoạn trích là chuỗi con của văn bản tách ra (sau chuẩn hoá NFKC và khoảng trắng): 62/62 trích chính và 16/16 trích phụ đều đạt. Đã thử kiểm âm tính: sửa một chữ số thì script trả False.
> Số P01–P17 do phiên tự tính từ tệp có SHA-256. Có một ngoại lệ phải nói rõ: số dân hạt giai đoạn 1920–1990 đọc tay từ dòng OCR của bản PDF quét Census, nên phải đối chiếu với ảnh trang ở G1. Tệp thô để **ngoài git**, trong thư mục scratch của phiên.

## 0. Khối điều lệ (chép lệnh, thêm cột thực tế)
| Trường | Lệnh | Thực tế |
|---|---|---|
| Loại phiên | Tiền kỳ T6 (Đóng gói + quyết tầng + dữ liệu xương sống) | như lệnh |
| Nhánh | `k2c-t6-tienky` từ `origin/main` | `7255aa4`. Harness gán thêm nhánh `claude/k2c-t6-detroit-tienky-ve47qm`; cùng một commit được đẩy lên **cả hai tên**, như T5 |
| Tệp được sửa | `channel-k2/k2c-t6-01/TIEN-KY.md`, `tienky/**`, `licenses/` | đúng như lệnh: 1 tệp md, 14 tệp `tienky/*.json(l)`, 21 tệp `licenses/`. Không sửa mã nhà máy, `checks/`, `design/`, `scripts/` hay tệp của tập khác. **Không ghi COST-LEDGER, RIGHTS, AUTHORSHIP** (xem §15). Không đọc `checks/` |
| Trần | YouTube ≤ 200 đơn vị · Claude API ≤ $2 (ghim model) · ElevenLabs 0 · giờ máy ≤ 1 giờ | **135 đơn vị** · **$0** (0 lượt; môi trường không có khoá API, xem §15) · **0 ký tự** · **≈ 56 phút** máy (ước, gồm cả hai tác tử con; số này nằm ngoài ±5 % quanh trần, ở mức −6,7 %) |
| Preflight | bắt buộc; che email | hook pre-commit/pre-push cài ngay đầu phiên; `tools/preflight.sh --range origin/main..HEAD` **ĐẠT**, `lock.py --verify` **KHỚP** (§16). Các tệp đã ghi không chứa địa chỉ email nào |
| Điều kiện dừng | xong → đẩy → dừng; không dừng hỏi giữa chừng | (1) xong việc |

## 1. Tóm tắt và khuyến nghị
**Khuyến nghị: ĐI TIẾP Detroit ở TẦNG CHUẨN. Không làm tầng đầy đủ, không chuyển sang Helsinki.**

**Lý do đi tiếp Detroit:**
1. **Câu chuyện mạnh và có số chính thức cho cả hai phía.**
   - Theo Census, thành phố có 1 849 568 người năm 1950 và 639 111 người năm 2020, tức **−65,4 %**.
   - Cùng thời gian, phần còn lại của ba hạt Wayne, Oakland và Macomb tăng **+183,7 %**. Cả ba hạt cộng lại vẫn tăng **+30,9 %**.
   - Tỷ trọng dân của Detroit trong ba hạt giảm từ **61,3 % xuống 16,2 %** (§4.2). Nói theo tầm người: năm 1950 cứ 10 người trong ba hạt thì 6 người sống ở Detroit; nay chỉ còn 1 trong 6.
2. **Cầu-ngách ĐẠT.** CityWise "Why Detroit Fixed Its Downtown…" có **36 914 lượt sau 25 ngày**. IT'S HISTORY "Why Detroit has 100 Miles of Secret Tunnels" có 111 927 lượt sau 99 ngày.
   - Mối quan tâm cũng lâu dài: CNBC đạt 1,98 triệu lượt (2022), Versed đạt 203 nghìn lượt (2024).
3. **Khoảng trống ĐẠT theo cả hai nhánh của luật.**
   - Chỉ 1/5 video đầu có số liệu dẫn nguồn (CNBC).
   - Video dạng gần mình nhất (Epoch Timeline, máy quay cố định đặt trên Woodward) có **7/10 bình luận chê sai hoặc chỉ ra công trình bị thiếu**.
   - Video Versed có bình luận chỉnh lỗi lặp lại: B-24 bị gọi là "fighter jet" ba lần, có người nhớ phá sản là "2008", có người quy redlining cho "insurance companies" (§3).
4. **Ghép rất tốt với T5** (§13). Cả hai thành phố có ranh giới gần như đứng yên: Zürich từ 1934, Detroit từ khoảng 1930. Cả hai đều mất dân vào vành ngoại ô. Cả hai đều phá nhà hàng loạt.
   - Điểm khác làm nên cặp: Zürich phá để xây dày hơn, và theo số của Thành phố đã vượt đỉnh cũ. Detroit phá vì đã co lại: cứ khoảng **14 vụ phá dỡ mới có 1 giấy phép xây mới** (2019–2026, P13).
5. **82 claim**: 61 XÁC MINH, 9 xác minh bằng nguồn phụ, 8 MÂU THUẪN đã ghi cả hai phía, 4 chờ nguồn gốc (§6). Mọi claim cho phần chủng tộc và chính sách đều dựa trên văn bản chính phủ hoặc toà án.

**Vì sao chỉ làm TẦNG CHUẨN, không làm TẦNG ĐẦY ĐỦ** (luật của lệnh; chi tiết ở §11):
- Thành phố có dữ liệu theo toà khá tốt. Lớp footprint có 380 076 toà, 96 % có năm xây. Sổ phá dỡ có 31 904 vụ ghi đến ngày (2014–2026).
- Nhưng **trường giấy phép trống ở mọi lớp**, và trang Terms bị chặn 403. Vậy giấy phép **CHƯA RÕ**, chưa đạt điều kiện của luật.
- Footprint chỉ là ảnh chụp khoảng năm 2010. Toà bị phá giữa 1950 và 2010, tức phần lớn cú co lại, **không có bản ghi** nào.
- Sổ phá dỡ chỉ nối được **39,7 %** số vụ vào footprint theo mã thửa.
- Muốn có lớp 1950 theo từng toà thì phải số hoá Sanborn 1949–51 (PD, 28 tập, **2 647 tờ**). Ước khoảng **1 300–2 700 giờ** làm tay, hoặc 400–800 giờ nếu bán tự động. Ước 180–330 giờ của phiên chọn thành phố là quá thấp.
- **Tầng chuẩn chỉ cần khoảng 45–75 giờ**, và toàn bộ nguồn là PD hoặc CC0.

**Vì sao không chuyển sang Helsinki:**
- Helsinki dữ liệu đẹp nhưng câu hỏi yếu hơn ("vì sao Helsinki lớn lên" không phải một nghịch lý).
- Helsinki cũng không ghép thành cặp với T5.
- Cầu của Helsinki thấp hơn (TIEN-KY-THANHPHO §2).
- Ở tầng chuẩn, rủi ro dữ liệu của Detroit đã được xử lý xong.

**Rủi ro chính:**
- **VÀNG** (chủng tộc, đường cao tốc, nhà ở, 1967, phá sản) → phải đủ 6 điều kiện (§8). T5 là XANH nên T6 VÀNG hợp luật thứ tự mức.
- Ba nguồn phải tìm nốt trước G1:
  - năm 1911, 1983, 1998 của Hudson's hiện chỉ có báo chí;
  - năm khánh thành RenCen 1977 hiện chỉ có ảnh Korab;
  - câu "first growth since 1957" là của Thành phố, nhưng `detroitmi.gov` chặn 403 nên chưa trích được.
- **Lần tìm YouTube chính bị hỏng** (§3). Cầu-bền của câu hỏi "Detroit history" chưa đo riêng được.

## 2. Bước 1 — Neo nguồn gốc (`tienky/neo.json`)
| # | Neo | Kết luận | Nguồn · as of | Trích nguyên văn (rút gọn) |
|---|---|---|---|---|
| N1 | Đỉnh 1 849 568 năm 1950 | **ĐÚNG** | Census Gibson 1998 POP-WP027 tab18 (SHA `6562bfe0…`) · đọc 16/10 | "5 Detroit city, MI……… 1,849,568 139.6 13,249" |
| N2 | "≈ 640 000 nay" / 639 471 | **SỬA**: 639 471 là estimates base cũ. **Số đếm 2020 = 639 111** (PL 94-171, SHA `971bd53a…`). Ước tính Vintage 2025 = **649 095** | Census | dòng P1_001N = 639111 |
| N3 | 31 904 vụ phá từ 2014 | **ĐÚNG** theo sổ Completed Demolitions (02/01/2014 → 09/10/2026). Lớp cũ đã ngưng ghi 31 646 vụ tới 09/2024 (D52). Giấy phép sổ: chưa rõ | City of Detroit ArcGIS (SHA `b4d4e457…`) | — |
| N4 | Sanborn 180–330 giờ | **SỬA** thành ≈ 1 300–2 700 giờ cho tầng đầy đủ (§11) | LoC (28 tập / 2 647 tờ) | "…is in the public domain and is free to use and reuse." |
| N5 | "0 timelapse 3D Detroit" | **SỬA**: đã có 1 video máy quay cố định (Epoch Timeline, 19/07/2026) | YouTube API | — |
| N6 | Tiêu đề "…31,904 Fewer Buildings…" | **KHÔNG DÙNG "fewer"** (P13) | — | — |
| N7 | Phá sản 2013 | **ĐÚNG**, kèm cách nói chính xác: "an estimated $18 billion" | Bankr. E.D. Mich. 13-53846, Doc 1945 | "The City estimates its debt to be $18,000,000,000." |

## 3. Bước 2 — Hồ sơ cầu (`tienky/cau.json`, `khoang-trong.json`, `binh-luan.json`)
**Cách đo, và chỗ hỏng:**
- **S1** gồm 1 lượt `search.list` cho chuỗi đúng như lệnh, "Detroit history|Detroit timelapse|why Detroit shrank" (type=video, relevance, 50 kết quả, en/US). Lượt này **chỉ trả 3 kết quả không liên quan**: một video "Detroit art" năm 2013, một video về Ground Zero, một video vẽ số.
  - Toán tử `|` không chạy như ở T5. Lý do có lẽ là các cụm nhiều từ ở hai đầu chuỗi.
  - **Không chạy lại**, vì lượt search thứ hai sẽ đưa tổng lên 235 đơn vị, vượt trần 200.
- **Cách thay thế** (34 đơn vị):
  - đo lại 34 video Detroit từ lượt S2 của phiên chọn thành phố (15/10);
  - đọc 50 upload mới nhất của 17 kênh cùng loại (11 kênh timelapse, Epoch Timeline, Epoch Timelapse, CityWise, IT'S HISTORY, Versed, Boundless Building), tổng cộng 481 video;
  - đọc bình luận của 2 video.
- **Tổng quota: 135/200 đơn vị.**

| Nhãn (LUAT-CHON-DE-TAI) | Kết quả | Căn cứ |
|---|---|---|
| Cầu-ngách | **ĐẠT** | CityWise "Why Detroit Fixed Its Downtown (And Baltimore Didn't)" 36 914 lượt, 966 s, đăng 21/09/2026. Bổ sung theo luật (tới 100 nghìn ghi rõ số): IT'S HISTORY "Why Detroit has 100 Miles of Secret Tunnels Below the City" 111 927 lượt sau 99 ngày |
| Nổ-mẫu | KHÔNG | — |
| Cầu-bền | **KHÔNG ĐO ĐƯỢC** (S1 hỏng). Phiên chọn thành phố ghi KHÔNG cho chuỗi "why …" | CNBC "Why Detroit Is Tearing Down A Highway" 1 982 440 lượt (2022) đứng hạng 17 trong S2 cũ, nên không lọt top 5 |
| Khoảng trống ĐK2 | **ĐẠT** (cả hai nhánh) | 1/5 video có số liệu dẫn nguồn (CNBC, dẫn SEMCOG). Bình luận chỉnh sai lặp lại ở cả 2 video đã đọc |

**Cung đã có, theo câu hỏi "vì sao Detroit co lại":**

| Video | Kênh · ngày | Lượt (16/10) | Dài | Ghi chú |
|---|---|---|---|---|
| Why Detroit Is Tearing Down A Highway | CNBC · 10/08/2022 | 1 982 440 | 13,1 phút | có nguồn (SEMCOG); trọng tâm I-375 và downtown |
| Why Basically Everyone Left Detroit | Versed · 15/05/2024 | 203 092 | 16,5 phút | không nguồn; 4/20 bình luận chỉnh sai sự kiện |
| Why Detroit Became America's Biggest Ghost Town | The Why Minutes · 2022 | 135 203 | 3 phút | — |
| Why Detroit Fixed Its Downtown… | CityWise · 21/09/2026 | 36 914 | 16 phút | Cầu-ngách |
| Why Detroit's Comeback Is Already Falling Apart | Boundless Building · 21/09/2026 | 8 553 | 13,3 phút | kênh này làm 4 video Detroit trong 3 tháng, đều không nguồn |
| **Evolution of Detroit (1000 AD–2026)** | **Epoch Timeline · 19/07/2026** | **3 595** | 8,1 phút | **dạng máy quay cố định Woodward/Sproat, gần mình nhất**; 7/10 bình luận chê sai (thiếu RenCen và tháp Hudson's, "off by a decade", "AI slop") |

- **11 kênh timelapse 3D và Epoch Timelapse: 0 video Detroit** trong 481 upload đọc được.
- **Sửa TIEN-KY-THANHPHO:** câu "0 timelapse 3D" nay sai, vì đã có 1 video máy quay cố định. Khoảng trống dạng "bay dọc phố + từng toà + có nguồn" vẫn còn nguyên.
- **Điều khán giả soi**, cần đưa vào lời hoặc hình:
  - RenCen và tháp Hudson's mới phải có mặt trong cảnh NOW;
  - xe và biển hiệu phải đúng thập kỷ;
  - phá sản là năm **2013**, không phải 2008;
  - redlining phải gắn đúng chủ thể là cơ quan liên bang HOLC/FHA (D21–D24);
  - "first growth since 1957" phải nói kèm vintage (D58);
  - một bình luận người Detroit nói "chỉ downtown hồi phục" → đưa vào đoạn the honest part.
- **Cách chấm khoảng trống:** môi trường **không có khoá Claude API**, nên không chạy Haiku như T5. Phiên tự chấm bằng quy tắc máy (mô tả có nguồn hay không, có cơ chế hay không); nhãn ghi trong `khoang-trong.json`.

## 4. Bước 3 — Nghịch lý, cặp tương phản, nhân vật, chương
### 4.1 Nghịch lý một câu
> **"The city that built the machine that let America leave the city. In 1950, 1.85 million people lived in Detroit. By 2020, 639,111 — two out of every three gone — on almost exactly the same land. And yet the three counties around it grew. Since 2014, Detroit has demolished 31,904 buildings. Zürich tore down buildings to make room. Detroit wasn't making room."**
- Claim dùng: P01, P08, P03, P11, P13; vế Zürich lấy từ T5 G01.
- Cụm "built the machine…" là cách nói hình ảnh. Phần sự kiện đứng sau nó là D01–D06 (dây chuyền 1913, $5 một ngày).

### 4.2 Cặp tương phản NƠI (đã tự kiểm số; `tienky/dan-so.json`)
**Cặp chính: thành phố ↔ phần còn lại của ba hạt.**
- Hai phía dùng **cùng một nguồn và cùng một định nghĩa**: số đếm Census thập niên.
- Số hạt: bản Census "Population of States and Counties 1790–1990" (PDF, SHA `cf394566…`) và PL 94-171 năm 2020.
- Số thành phố: Gibson 1998 và PL 2020.

| Phía | 1950 | 1980 | 2020 | 1950→2020 | Màu đề xuất |
|---|---|---|---|---|---|
| **A: Detroit** | 1 849 568 | 1 203 339 | 639 111 | **−1 210 457 (−65,4 %)** | đỏ gạch tối dần |
| **B: phần còn lại của Wayne + Oakland + Macomb** | 1 166 629 | 2 840 945 | 3 310 062 | **+2 143 433 (+183,7 %)** | xanh lá ngoại ô sáng lên |
| Tổng ba hạt | 3 016 197 | 4 044 284 | 3 949 173 | +932 976 (+30,9 %) | — |
| Tỷ trọng của Detroit | 61,3 % | 29,8 % | **16,2 %** | — | — |

- **Kết luận:** cặp tương phản **ĐÚNG và mạnh hơn T5**. Trong 30 năm đầu sau đỉnh (1950→1980), thành phố mất 34,9 %, còn phần còn lại tăng 143,5 % (P05). Ở Zürich, con số tương ứng là −21,3 % và +42,3 %.
- **Dòng ranh trên hình là 8 Mile Road** (TB-8mile). Bay dọc đường này thì hai bên đổi màu theo số Census.
- **Lưu ý:**
  - (1) Số hạt 1920–1990 đọc tay từ dòng OCR, ví dụ "2.111,6872,337,891…". Tổng đã kiểm hợp lý, nhưng phải đối chiếu ảnh trang ở G1.
  - (2) Hamtramck và Highland Park nằm trong Wayne County nên được tính vào phía B. Hai thành phố này nhỏ (28 433 và 8 977 người năm 2020), nhưng nằm lọt trong lòng Detroit. Trên hình phải khoét lỗ đúng chỗ.
  - (3) Không dùng thuật ngữ "suburbs" cho toàn bộ phía B trong lời. Nói "the rest of the three counties" và cho hình chỉ ra vành ngoại ô.

**Cặp chéo với T5: Detroit ↔ Zürich** (chỉ so %, vì hai cơ quan thống kê khác nhau; P16):

| | Đỉnh | Sau ~30 năm | Ranh giới đứng yên từ | Vành bên ngoài |
|---|---|---|---|---|
| Zürich (số Bang) | 440 784 (1962) | −21,3 % (1989) | 1934 | +42,3 % |
| Detroit (Census) | 1 849 568 (1950) | −34,9 % (1980); **−65,4 % (2020)** | ~1930 (137,9 dặm² năm 1930; 138,7 dặm² năm 2020) | +143,5 % (1980); +183,7 % (2020) |

### 4.3 Nhân vật người thật có hồ sơ (`tienky/nhan-vat.json`)
| # | Nhân vật | Chương | Muốn → bị cản → kết cục (theo nguồn) | Claim | Hình |
|---|---|---|---|---|---|
| 1 | **Henry Ford** | 1 | muốn làm xe hàng loạt, nhanh và rẻ: dây chuyền 1913 rút thời gian lắp từ 728 xuống 93 phút; ngày công $5 công bố 05/01/1914 → bị cản vì hết mặt bằng → dời lắp ráp sang Rouge năm 1927. Kết cục: các nhà máy then chốt **nằm ngoài ranh Detroit** (Highland Park, Dearborn) | D01–D06 | LoC 94506959 (~1919, "No known restrictions") |
| 2 | **Albert Kahn** (kiến trúc sư) | 2 | muốn sàn nhà máy rộng và sáng (Packard No. 10); các nhà máy sau của ông cần đất rộng → Packard đóng năm 1958 | D04, D05, D07 | chỉ dùng ảnh công trình (chưa có chân dung PD) |
| 3 | **Coleman A. Young** | 5 | thị trưởng da đen đầu tiên (bầu năm 1973, tái cử 4 lần); điều hành một thành phố đang co (1 203 339 → 1 027 974 người). **Không quy kết** sự suy giảm cho cá nhân | D63, D55 | ảnh LoC ghi "May be restricted" → **KHÔNG dùng**; A-lite |
| 4 | **Kevyn Orr & Judge Steven Rhodes** | 5 | Orr được bổ nhiệm 15/03/2013 để tái cơ cấu khoản nợ ước tính $18 tỷ → hơn 100 000 chủ nợ, lương hưu được hiến pháp bảo vệ → "Grand Bargain" $816 triệu; xoá khoảng $7 tỷ nợ; thoát phá sản 10/12/2014 | D35–D43, D62 | A-lite (đạo cụ: cặp hồ sơ, búa toà); trang đầu đơn toà làm hồ sơ thật |
| 5 | **Mike Duggan** | 6 | nhận lại toàn quyền điều hành từ 09/2014 (D65); chương trình phá dỡ, Proposal N | D64, D65, D48, P11 | A-lite |
| (nhóm) | **"The families who moved past 8 Mile"** | 4 | nhân vật tổng hợp, theo số Census P02–P05. **Phải có dòng "composite characters"** trên màn hình | P02–P05 | A-lite gia đình + xe chuyển nhà |

### 4.4 Chương (Kinh thánh §3: 9–11 phút) — xương sống năm từ đỉnh 1950 tới nay, 5 nhịp lặn cơ chế
Luật mạch truyện áp vào từng chương:
- mỗi chương đi theo trình tự **câu hỏi → trở ngại → bước ngoặt (mốc đinh) → hệ quả**;
- mỗi shot gắn với một câu lời hoặc một claim;
- timelapse trôi tự do ≤ 15 % thời lượng, chỉ dùng ở ch.4 và ch.6.

| # | Tên chương (EN) | Nhân vật | Câu hỏi → trở ngại → bước ngoặt → hệ quả (claim) | Mốc · lặn · tuyến | Dài |
|---|---|---|---|---|---|
| 0 | *31,904* (móc ≤ 45 s) | — | Tin: năm 2026 thành phố vẫn còn phá nhà (P11) → nghịch lý (P01, P03) → lật: "it wasn't making room" (P13) → 2 sự thật: ranh giới đứng yên từ khoảng 1930 (P08); cứ 10 người trong ba hạt thì 6 người sống ở Detroit năm 1950, nay còn 1 trong 6 (P04) → một con số: 1,2 triệu → câu hỏi trùng tiêu đề → hứa một cú lật | TB-river reveal | 0:45 |
| 1 | *The Biggest Factory Town on Earth* | Ford | Hỏi: vì sao Detroit lớn nhanh đến vậy? Dây chuyền 1913 và $5 một ngày (D02, D03) → trở ngại: hết đất, nên nhà máy dời ra **ngoài ranh** (D05, D06) → **M1 1950: đỉnh 1 849 568** (D53) → hệ quả: mật độ 13 249 người/dặm² (P06) | **M1** · TB-woodward (đi qua Highland Park) · Sanborn 1950 sepia | 1:30 |
| 2 | *The Factories Leave* | Kahn | Hỏi: việc làm ở đâu? Arsenal nằm ở Warren (D09); Rouge ở Dearborn (D05) → **M2 1958: Packard đóng** → hệ quả: từ 1972 đến 2007 thành phố mất khoảng 80 % cơ sở sản xuất; số việc làm giảm từ 735 104 (1970) xuống 346 545 (2012) (D10) | **M2** · **lặn #1: công nghiệp ô tô** | 1:20 |
| 3 | *Concrete Rivers* | — | Hỏi: người đi bằng đường nào? Davison 1942 (D13); Luật 1956 (D16) → **M3 1964: I-375**; Black Bottom và Paradise Valley bị phá (D17, D30); FHWA và MDOT "fully acknowledge…" (D18) → hệ quả: as of 2026 vẫn chưa thành đại lộ (D19) | **M3** · **lặn #2: đường cao tốc** · TB-i375 | 1:20 |
| — | *(lời mời đăng ký nhẹ, ranh ch.3/4, ~3:35)* | | | | |
| 4 | *Eight Mile* | "the families" | Hỏi: ai được vay để mua nhà, và mua ở đâu? HOLC 1939 công bố sau khoản vay cuối (D21); Birwood wall 1941; NPS không tìm thấy hồ sơ liên lạc với FHA (D23, D24); Sojourner Truth 1942 (D25) → cặp tương phản P02–P05 → **M4 1967**: 43 người chết (D27), nhưng Census cho thấy thành phố **đã giảm từ trước** (D29, P05) → hệ quả: ngoại ô +143,5 % tới 1980 | **M4** · **lặn #3: nhà ở / ngoại ô** · TB-8mile · timelapse vùng loang (≤ 20 s) | 1:30 |
| 5 | *The Bill Comes Due* | Young; Orr & Rhodes | Hỏi: ai trả tiền khi người đi? **M5 1977 RenCen** là nỗ lực giữ downtown → thuế thu nhập thành phố giảm từ $276,5 triệu (2008) xuống $233 triệu (2012) (D34) → **M6 18/07/2013: phá sản**, nợ ước tính $18 tỷ, dân còn 684 799 (D35, D40, D44) → hệ quả: Grand Bargain; thoát phá sản 10/12/2014 (D37–D43) | **M5 · M6** · **lặn #4: thuế / ngân sách** · TB-river | 1:35 |
| 6 | *Tear It Down* | Duggan | Hỏi: làm gì với 40 077 công trình bị đề nghị phá (D47)? Hardest Hit Fund $235 triệu (D46); Proposal N $250 triệu (D48) → **M7 2015: năm phá nhiều nhất, 4 012 vụ** (P11) → hệ quả: 150 730/377 940 thửa trống; DLBA đứng tên 57 737 thửa (P14); cứ khoảng 14 vụ phá có 1 giấy phép xây mới (P13). **Gương T5:** Zürich phá để xây lại, Detroit phá vì trống | **M7** · **lặn #5: chương trình phá dỡ** · heat map 2014→2026 (≤ 20 s) | 1:30 |
| 7 | *The Station* | — | Hỏi: đã chạm đáy chưa? **M8 06/06/2024: MCS mở lại** sau chuyến tàu cuối năm 1988 (D59); Hudson's (D60); Vintage 2025: 649 095 người (D57). **The honest part:** ước tính đổi theo vintage (D58); ước tính 2020 cao hơn số đếm 26 258 người (P09); một người Detroit nói "chỉ downtown hồi phục" → quay về khung mở đầu, bảng điểm, câu chốt | **M8** · TB-michigan · TN1 | 1:15 |

- **Tổng ≈ 10:45**, gồm 8 chương (0–7), **8 mốc đinh**, **5 nhịp lặn**.
- **Câu chốt (nháp):** *"Zürich tore itself down to grow. Detroit tore itself down because it had already shrunk — and only now is it counting up again."*
- **Câu dẫn sang tập kế:** đề xuất một thành phố "co rồi hồi" thật, hoặc dạng ngược lại (thành phố bị chặn không cho mọc). Việc chọn để cho P quyết.

## 5. (Bước 3 mở rộng) Nêu trước các phản biện
| Khán giả sẽ nói | Trả lời bằng |
|---|---|
| "It was the riots" | Census cho thấy thành phố đã giảm từ 1950 tới 1960 và 1967 (D55, D29). **Không nói "caused"** cho bất kỳ yếu tố đơn lẻ nào (khong_dung) |
| "It was white flight" / "It was the city government" | Chỉ dùng số và lời trích của cơ quan. Nêu nhiều cơ chế song song: nhà máy ngoài ranh, đường cao tốc, nhà ở liên bang, thuế. Không quy kết cho một nhóm người nào (§8) |
| "Detroit went bankrupt in 2008" | 18/07/2013, 16:06 (D40) |
| "Insurance companies redlined Detroit" | Bản đồ 1939 là của HOLC, cơ quan liên bang, và được công bố sau khoản vay cuối (D21). Hồ sơ NPS về bức tường Birwood (D24) |
| "Detroit is booming now" / "Only downtown" | Hai mặt: Vintage 2025 tăng ba năm liền (D57), nhưng 39,9 % số thửa trống (P14) và ước tính vẫn bị sửa qua từng vintage (D58) |
| "The Rouge plant is in Detroit" | Rouge nằm ở Dearborn (D05). Đây chính là điểm mấu chốt của ch.1–2 |

## 6. Bước 4 — Danh mục claims (`tienky/claims.json`: **82 claim**)
**Tình trạng:** 61 XÁC MINH · 9 XÁC MINH (nguồn phụ) · 8 MÂU THUẪN · 4 CHỜ XÁC MINH GỐC.

| Nhóm | Claim | Nguồn chính |
|---|---|---|
| A. Công nghiệp ô tô | D01–D12 | hồ sơ NRHP/NHL của NPS (Highland Park 73000961, Rouge 78001516), UCSB Presidency Project, Archives of Michigan, toà phá sản (Doc 1945) |
| B. Đường cao tốc | D13–D20 | NARA (Luật 1956), Văn phòng Thống đốc, MDOT (FAQ, thông cáo 14/11/2025), Detroit Historical Society (nguồn phụ) |
| C. Nhà ở, 1967 | D21–D32 | hồ sơ NRHP Birwood Wall (NPS), LoC FSA/OWI, báo cáo Kerner 1968 (ấn bản GPO), Federal Register |
| D, E. Thuế, phá sản | D33–D45 | Bankr. E.D. Mich. 13-53846 (Doc 1945, 8272, 8993, 10079), Citizens Research Council |
| F. Phá dỡ | D46–D52 | SIGTARP 03/2020, Data Driven Detroit, Financial Review Commission (Michigan Treasury), DLBA, dữ liệu mở của Thành phố |
| G. Ranh giới | D53–D56 | Census Gibson 1998, Vintage 2025 |
| H. Hiện nay | D57–D61 | Census V2023–V2025, Michigan Central (Ford), Bedrock, Michigan Public |
| I. Nhân vật | D62–D65 | toà án, Văn phòng Thống đốc, DHS |
| P (tự tính) | P01–P17 | Census, TIGER, các lớp dữ liệu của City of Detroit, LoC |

**Tám MÂU THUẪN và cách nói:**
- **D20 (lịch I-375):** không nêu ngày; nói "as of October 2026, still a freeway".
- **D28 (Kerner 82 hay 80 người):** nói "more than 80 people".
- **D41 (ngày phán quyết tư cách):** văn bản đề ngày 05/12/2013 → nói "In December 2013".
- **D45 (toà ghi "1952 … 1,850,000"):** dùng số Census 1950.
- **D49 (mục tiêu Proposal N):** chỉ nói "$250 million, November 3, 2020".
- **D51 (hai tổng phá dỡ của DLBA):** dùng sổ của Thành phố.
- **D58 (số dân 2023 theo các vintage):** luôn ghi vintage.
- **P12 (số vụ HHF):** sổ Thành phố ghi 15 082, SIGTARP ghi 12 679 → trong lời dùng số SIGTARP cho HHF, số Thành phố cho tổng.

**Bốn claim CHỜ** (không dùng cho tới khi có nguồn gốc): D11 (bảng việc làm sản xuất 1947–1977), D12 (25 nhà máy mới ở ngoại ô 1945–57), D15 (Edsel Ford Freeway), D33 (thuế thu nhập năm 1962, câu trích không nêu tên Detroit).

**Không dùng** (`claims.json → khong_dung`, 23 mục), tiêu biểu:
- "largest US city ever to go bankrupt" (chưa có nguồn chính phủ);
- "the riots caused the decline";
- "peaked in 1952";
- "built half the world's cars" (chưa kiểm);
- "the FHA built the Birwood Wall";
- "Davison was the first freeway in America" (DHS chỉ viết "arguably");
- "Detroit owed $18 billion" (phải nói "an estimated");
- "Mary Sheffield is the first woman mayor" (đúng là "first woman elected");
- "31,904 fewer buildings";
- tổng "$711 million" chi phí phá dỡ (chưa rõ nghĩa của trường dữ liệu);
- "Rouge is in Detroit";
- mọi câu quy nguyên nhân cho một nhóm người.

## 7. Bước 5 — Tài sản hình (`tienky/hero.json`, `licenses/` 21 tệp)
| Tầng | Tài sản | Giấy phép · ghi công |
|---|---|---|
| Dân số, ranh giới, đường, sông | Census (Gibson, PL 2020, PEP), TIGERweb, USGS NHD, USGS topo 1940–1968 | PD (17 U.S.C. §105, trích ở `census-usgs-tiger-pd.txt`) |
| Bản đồ lịch sử | Sanborn 1949–51 (28 tập, 2 647 tờ), Farmer 1835, phối cảnh 1889 (LoC) | PD / "No known restrictions" |
| Bản đồ HOLC 1939 | **bản quét NARA (PD)**, tự georeference. **KHÔNG dùng lớp Mapping Inequality (CC BY-NC)** | `detroit-mapping-inequality-KHONG-DUNG.txt` |
| Ảnh lịch sử | 15 ảnh LoC (Detroit Publishing Co. trước 1931, FSA/OWI Siegel 1939/1942, Leffler 1958, Korab 1977, Highsmith 2020, Keystone 1925); Henry Ford ~1919; Sojourner Truth Homes 1942 | từng tệp có rights nguyên văn và SHA-256 |
| Hình học hero | OSM qua Nominatim / API v0.6 (Overpass bị chặn) | ODbL: "© OpenStreetMap contributors" |
| **KHÔNG dùng** | ảnh Camilo Vergara ("Publication may be restricted"); ảnh Coleman Young LoC ("May be restricted"); lớp footprint và sổ phá dỡ của Thành phố để **phát hành hình theo toà** (giấy phép chưa rõ) | `loc-vergara-LOAI.txt`, `detroit-opendata-t6.txt` |

**Footage: đề xuất ≈ 6 %** (~40 s); trần 20 % là mức tối đa, không phải chỉ tiêu.
- Gồm khoảng 7 ảnh lưu trữ (Ken Burns 2.5D) dùng làm bằng chứng sự việc hoặc cho thấy quy mô, cộng tối đa 8 s phim PD về nhà máy, và chỉ khi đã kiểm rủi ro Content ID.
- Không dùng stock hiện đại; giai đoạn 2014–2026 dựng bằng 3D và NAIP.
- Hồ sơ thật chiếm 10–15 % thời lượng: bản đồ HOLC, trang báo cáo Kerner, đơn toà 2013, câu trong FAQ của MDOT, hồ sơ NPS Birwood.

## 8. Bước 6 — Mức rủi ro (QUAN-TRI-RUI-RO): **VÀNG**
**Lý do:** đề tài chạm chủng tộc, đường cao tốc và khu dân cư (LUAT-NOI-DUNG §8), sự kiện 1967, phá sản 2013, và nhân vật chính trị còn sống (Duggan, Orr).

**Sáu điều kiện VÀNG và kế hoạch đáp ứng:**
1. Mọi khẳng định đều có nguồn (82 claim).
2. Mốc **"as of 16 October 2026"** xuất hiện trong lời, trên hình và trong mô tả.
3. REVIEWER Opus rà độc lập bản lời, tiêu đề và thumbnail.
4. Câu miễn trừ tài chính chỉ cần nếu chạm trái phiếu hay đầu tư; đề xuất **không cần**, vì Proposal N chỉ được nhắc như một sự kiện ngân sách.
5. Trình bày các phía, mỗi phía có nguồn riêng: Grand Bargain có toà và Thành phố, cùng chỉ trích của SIGTARP 2020; Proposal N có kết quả bỏ phiếu và các mục tiêu khác nhau (D49).
6. Không đứng về phe đảng phái nào.

| Tránh | Dùng thay |
|---|---|
| "white flight", "Black residents left", "blight" (khi nói về người) | "families moved to the rest of the three counties" kèm số P02–P05; chữ "blight" chỉ dùng khi trích tên chương trình chính thức |
| "the riots destroyed Detroit" | "the July 1967 uprising — the Kerner Commission called it a disorder; 43 people died" (D26, D27), đặt **sau** số Census cho thấy thành phố đã giảm từ trước |
| "the government destroyed Black Bottom" (lời của kênh) | trích nguyên văn lời thừa nhận chính thức của FHWA/MDOT (D18), ghi tên cơ quan |
| "redlining" mà không nêu chủ thể | "a federal agency, HOLC, graded neighborhoods on a 1939 map" (D21, D22) + giới hạn của hồ sơ (D24) |
| tên thị trưởng gắn với chữ "decline" | dân số theo Census trong nhiệm kỳ, không bình luận |
| ảnh nhà riêng bị phá có số nhà đọc được | heat map tổng hợp, khối 3D không địa chỉ |
| từ ngữ trong trích Kerner năm 1968 | chỉ xuất hiện trong ngoặc trích; không đọc thành lời bình |

**Thứ tự mức:** T4 đề xuất XANH, T5 XANH, T6 VÀNG → hợp luật (không quá 2 tập VÀNG liền nhau).

## 9. Bước 7 — Gói sơ bộ
| # | Tiêu đề | Ký tự | Ghi chú |
|---|---|---|---|
| 1 | **Why Detroit Shrank While Its Suburbs Grew** | 41 | đề xuất chính; song song với tiêu đề T5 "Why Zürich Shrank While Getting Rich"; số liệu là P02 |
| 2 | Detroit Tore Down 31,904 Buildings. It Wasn't Making Room. | 58 | P11, P13; tránh chữ "fewer" |
| 3 | The Car City That Lost Two-Thirds of Its People | 47 | P01 (−65,4 %) |

```
THUMBNAIL BRIEF — K2C-T6-01
[A] BẢN ĐỒ TƯƠNG PHẢN (cặp với T5 [A])
- Nền: render 3D của mình, ranh Detroit (TIGER 2020, nét trắng dày) + đường 8 Mile; nhìn chếch từ sông Detroit lên phía bắc.
- Trong ranh: khối nhà đỏ gạch, nhiều ô trống. Ngoài ranh (Oakland, Macomb): khối nhà xanh lá sáng.
- Chữ (1 hộp, nền tối): A1 "−65%" (P01) | A2 "2 OF 3 GONE" (chữ khác).
- Biểu tượng (≤ 2): xe chuyển nhà A-lite băng qua 8 Mile; một máy xúc nhỏ trong ranh.
[B] THEN/NOW (không chữ)
- Woodward ở Campus Martius: nửa trái là DPC 1917 tô màu sepia (Hudson's), nửa phải là render 2026 cùng góc (tháp mới). Đúng khung TN1.
- Không logo GM/Ford/Bedrock, không cờ, không người nhận ra được, không cảnh bạo lực.
Chung: tiêu đề hỏi, thumbnail cho thấy; mọi số có trong video; lề 5 %; tránh góc dưới-phải.
Test & Compare: A1, A2, B.
```

**Short đi kèm (chính):** *"Detroit vs. the rest of its three counties, 1950 → 2020, in 40 seconds."*
- Hai cột dân số bằng 3D chạy theo Census (PD, rủi ro quyền bằng 0), kết bằng tỷ trọng "6 in 10 → 1 in 6".
- Short dẫn về video dài; chữ trên Short theo BAI-HOC-LL #6–7.

**Short dự phòng (điều kiện):** "Every Detroit demolition since 2014 — in 45 s". **Chỉ làm** khi Thành phố xác nhận giấy phép (§11). Trong lúc chờ, chỉ dùng heat map tổng hợp theo năm.

## 10. Bước 9 — HERO (`tienky/hero.json`; tác tử con, 2 vòng)
| Hero | Mốc (nguồn) | Mặt bằng / cao | Tư liệu | Mức · giờ (ước) |
|---|---|---|---|---|
| **H1 Michigan Central Station** | đưa vào dùng 12/1913; chuyến tàu cuối 05/01/1988 (City Planning Commission 02/2024); Ford mua 2018; mở lại 06/06/2024 (Ford/MC) | 128,2 × 103,6 m; 10 065 m² (OSM). Số tầng **lệch**: tháp 18 tầng + ga 3 tầng (City) so với 15 + 3 (State). Chiều cao bằng m: **không có** | Highsmith 2020 trên không (LoC, "No known restrictions"); **không có ảnh PD mặt đứng trước 1988** | **chi tiết · 60–80** |
| **H4 Hudson's → Hudson's Detroit** | toà đầu khởi công 1891 (GM 2024); đóng 17/01/1983 và nổ phá 24/10/1998: **chỉ có báo chí**; tháp mới (GM: 45 tầng; OSM: 49 tầng, 208,9 m → **lệch**) | khối phố cũ 129,6 × 68,6 m (lớp ArcGIS, chỉ dùng đối chiếu); toà cũ cao "410 ft" (CBS dẫn DHS, độ tin thấp) | DPC 1917 Campus Martius, biển HUDSONS (TN1); Keystone 1925 | **chi tiết · 50–70** |
| **H2 Packard** | 1903–1958; Thành phố bắt đầu phá năm 2017, đợt khẩn cấp từ 09/2022, dự kiến xong "by the end of 2024", **chưa có thông báo hoàn tất**; giữ cánh trước 1539 E. Grand Blvd; Packard Park dự kiến 2029 (City of Detroit qua Wayback) | khu 1 231,9 × 176,4 m (OSM) | Leffler 1958, ống khói chữ PACKARD (M2) | trung cảnh · 25–35 |
| **H3 Renaissance Center** | 1977 (chỉ có ảnh Korab "Phase 1" và OSM); GM mua 1996; GM dời trụ sở về Woodward (GM 15/04/2024; 12/01/2026) | 324,1 × 218,7 m; cao 221,5 m (OSM) | Korab 1977 nhìn từ sông | trung cảnh, **không logo** · 15–20 |
| H6 Guardian (nền đỉnh giàu 1929) | xong năm 1929; 40 tầng, 485 ft = 147,8 m (NHL 89001165). OSM ghi 36 tầng / 151 m → **lệch**, dùng NHL | 82,8 × 24,8 m | Siegel FSA 1939/1942 | trung cảnh · 20–25 |
| H5 Ford Highland Park | 1910–1927; dây chuyền 1913 (NRHP 73000961). Factory H 75 × 760 ft, 4 tầng; các xưởng W–Z mỗi xưởng 60 × 840 ft, 6 tầng | — | ảnh dây chuyền 1913, toàn cảnh DPC | ảnh 2.5D · 0–10 |

- **Tổng (tác tử con đề xuất): 170–240 giờ.**
- **Đề xuất của P:** giữ H1, H4 ở mức chi tiết (mốc M8 và TN1); H2, H3 ở trung cảnh; **hạ H6 xuống nền** (khối LoD từ footprint OSM cộng texture), vì 1929 nằm ngoài xương sống năm. Như vậy tổng ≈ **150–205 giờ**.
- **Bản vẽ đo đạc HABS/HAER: không có cho hero nào** (đã kiểm LoC). Fisher NHL 80001922: 28 tầng, 442 ft, hai cánh 11 tầng; dùng cho TN2.
- **Thương hiệu và kiến trúc:**
  - không dựng logo GM, Ford, Bedrock;
  - chữ PACKARD chỉ xuất hiện như trạng thái lịch sử năm 1958;
  - tháp Hudson's mới (sau 1990): theo 17 U.S.C. §120(a), được phép tả hình ảnh toà nhìn từ nơi công cộng. Cần tư vấn pháp lý xác nhận trước khi bán phim (chưa kiểm).

**Chỉ số trong ±5 %:** không có ngưỡng định lượng nào áp lên phần hero. Phần đối chiếu đo đạc có một chỗ lệch: Guardian, 147,8 m (NHL) so với 151 m (OSM), +2,2 %.

## 11. Bước 8 — Quyết tầng: **TẦNG CHUẨN** (`tienky/du-lieu-toa.json`, `xuong-song.json`)
**Kiểm nguồn theo toà (đúng như lệnh yêu cầu):**

| Nguồn | Có gì | Giấy phép (nguyên văn) | Kết luận |
|---|---|---|---|
| City of Detroit — *Detroit Building Footprints (Public Safety)* | 380 076 footprint (244 938 toà chính); YEAR_BUILT có ở 96,0 %; YEAR_DEMO bằng 0 ở 380 075/380 076; năm lớn nhất là 2010 → **ảnh chụp khoảng 2010** (có trường semcogID) | `licenseInfo` trống; `accessInformation` trống | CHƯA RÕ |
| *Completed Demolitions* | 31 904 vụ có ngày (02/01/2014 → 09/10/2026), toạ độ, cờ HHF/bond | `licenseInfo: None`; nơi cung cấp: "Construction and Demolition Department (CDD)" | CHƯA RÕ |
| *Parcels (Current)* | 377 940 thửa; year_built 59,9 %; is_improved | `licenseInfo: ''` | CHƯA RÕ |
| Cổng `data.detroitmi.gov` | trang Hub, `licenseInfo: 'null'`; link "Terms of Service & Privacy Policy" dẫn tới detroitmi.gov/Privacy | **403 (Cloudflare)**; Wayback 429/offline | CHƯA RÕ |
| Toàn tổ chức ArcGIS | 1 386/1 518 mục có licenseInfo trống | — | — |
| Detroit Land Bank | nằm trong cùng tổ chức ArcGIS (DLBA Buildings 1 804 mục, licenseInfo trống) | — | CHƯA RÕ |
| Wayne County | không tìm thấy lớp năm xây/phá theo toà có giấy phép mở | — | không có |

**Đo nhanh** (13,6 phút máy, trong trần 30 phút; chỉ thuộc tính, không tải hình học):
- **Dồn năm 0/5** của footprint: 22,7 %; riêng các toà trước 1950: 19,8 %. Mức "thật" là 20 %, nên năm xây khá thật. Các năm đỉnh 1950, 1941, 1948 cho thấy làn sóng xây dựng thời chiến và hậu chiến.
- **78,2 % toà chính xây trước 1950.** Những toà bị phá mà nối được có năm xây trung vị là **1925**.
- **Nối phá dỡ ↔ footprint theo mã thửa đạt 39,7 %.** Lấy mẫu không gian 150 vụ không nối được: 69 % có một toà trong bán kính 15 m, nhưng mẫu cho thấy đó thường là **nhà bên cạnh**, không phải chính toà bị phá. Muốn nối chính xác phải tải hình học và nối không gian ở G1 (2–4 giờ máy).
- **Giấy phép xây mới** (permit_type = New): 1 112 giấy phép, cho 7 516 căn (2019–2026). Số vụ phá cùng cửa sổ: 15 416 → khoảng 13,9 vụ phá cho mỗi giấy phép.

**Ba phương án (giờ số hoá tay, ước):**

| Phương án | Giờ | Quyền | Kết luận |
|---|---|---|---|
| A. Tầng đầy đủ: Sanborn 1950 toàn thành phố + footprint 2010 + phá dỡ 2014–2026 | **1 300–2 700** (tay, 100–200 toà/giờ cho khoảng 250–400 nghìn toà); 400–800 nếu bán tự động | Sanborn PD; lớp Thành phố CHƯA RÕ | **LOẠI** |
| **B. Tầng chuẩn**: vùng đô thị theo năm (HISDAC-US CC0, rồi NLCD PD) + ranh giới theo năm (USGS topo PD) + 3 khu hero lấy từ Sanborn 1950 (~20 tờ) + đường cao tốc theo năm mở + HOLC bản quét NARA | **45–75** | PD/CC0 toàn bộ | **CHỌN** |
| C. Đổi sang Helsinki | theo TIEN-KY-THANHPHO | CC BY 4.0 | không cần (§1) |

- **Sanborn:** chỉ dùng phần PD, và chỉ ở chỗ có lợi rõ. Cụ thể là ba khu: Black Bottom (ch.3), Campus Martius–Hudson's (ch.1, TN1) và Packard–E. Grand Blvd (ch.2). Các tờ còn lại chỉ làm texture sepia nền.
- **Nâng cấp có điều kiện:** nếu DoIT (City of Detroit) xác nhận giấy phép bằng văn bản trước G1, thì ở ch.6 chuyển heat map thành **từng nhà tắt đúng ngày** (31 904 điểm). Phần 1950–2013 vẫn ở tầng chuẩn.

## 12. Bước 10 — Kế hoạch dữ liệu xương sống (`tienky/xuong-song.json`, `dan-so.json`, `tuyen-bay.json`)
| Lớp | Vai | Nguồn · luật |
|---|---|---|
| L1 Dân số | bộ đếm, cặp tương phản, bảng điểm | Census 1840–2020 theo thập niên và Vintage 2025. Giữa các mốc: nội suy, có nhãn "interpolated"; 2021–2025 có nhãn "estimate (Vintage 2025)" |
| L2 Ranh giới theo năm | vạch ranh sống | Gibson: 40,8 dặm² (1910) → 77,9 (1920) → 137,9 (1930) → 139,6 (1950) → 135,6 (1980) → 138,7 (1990). TIGER 2020: 359,32 km² = 138,7 dặm². Vạch từng năm số hoá từ USGS topo 1940/1947/1952/1968. Highland Park và Hamtramck luôn là lỗ khoét. **Năm sáp nhập cuối (1926) hiện chỉ có nguồn phụ** → lời nói "by 1930" |
| L3 Vùng đô thị | vùng loang ra ba hạt (ch.4) | HISDAC-US FBUY v2 (CC0, 250 m) tới 1985, sau đó Annual NLCD (PD, 30 m), chuyển mềm như T4 |
| L4 Sanborn 1949–51 | nền 1950 sepia cho 3 khu hero | LoC PD, 28 tập / 2 647 tờ (`loc-sanborn-detroit-1950.txt`) |
| L5 Phá dỡ 2014–2026 | ch.6 | **heat map tổng hợp theo năm × ô 250 m** (mặc định); từng điểm chỉ khi có giấy phép |
| L6 Đường cao tốc theo năm mở | ch.3 | hình học TIGER (PD); năm lấy từ claim; đoạn nào không có năm nguồn thì không hiện (Edsel Ford: D15 đang CHỜ) |
| L7 Thửa hiện nay | chỉ đọc số trong lời | P14; không vẽ theo thửa |
| L8 Nền | địa hình, nước, NOW | USGS 3DEP, NHD, NAIP (PD) |

**Ghép lớp:** lặn theo thứ tự L3 → L2 → topo/NAIP → L4 → hero 3D. Hệ toạ độ UTM 17N (EPSG:26917); dời gốc về Campus Martius trước khi đưa vào float32 (bài học T5 §12).

**Tuyến bay** (TIGER/NHD, PD; lấy mẫu mỗi 25 m; `tuyen-bay.json`) — **3 tuyến bắt buộc dọc phố và sông thật, cộng 2 tuyến phụ:**

| Tuyến | Độ dài | Ghi chú |
|---|---|---|
| **TB-woodward** | 14,7 km | từ Hart Plaza bên sông lên 8 Mile; **21 % chiều dài nằm trong Highland Park** (thành phố lọt trong thành phố, có nhà máy Ford); đoạn đầu nối thẳng 460 m |
| **TB-river** | 10,5 km | sông Detroit, từ gần cầu Ambassador tới đầu đảo Belle Isle; hình học là đường dòng chảy giữa sông → ở G1 dịch về phía bờ Mỹ 150–250 m |
| **TB-8mile** | 29,1 km (thô) | đường ranh của cặp tương phản; phải cắt theo ranh TIGER ở G1 |
| TB-michigan | 2,6 km | từ Campus Martius tới MCS |
| TB-i375 | 1,7 km | qua khu Black Bottom cũ |

- **Mở chương:** reveal và glide → zoom-in xen kẽ ở cả 8 chương (`hinh-xuong-song.json`).
- **Then/now:**
  - **TN1 GIỮ:** Hudson's/Campus Martius 1917 ↔ 2026.
  - TN2 ĐIỀU KIỆN: Fisher, Siegel 1939.
- **Chuẩn 4 lớp:**
  - hero: H1–H5;
  - nhà thường: khối thủ tục theo mật độ, cộng khối Sanborn ở 3 khu;
  - nền sống: sông, tàu, xe A-lite, khói nhà máy năm 1950;
  - ánh sáng: sepia trước 1958, rồi tự nhiên, xám mùa đông cho năm 2013.
- **Ngân sách chữ** ≤ 15 % diện tích khung.
- **Dựng bằng llvmpipe** (không GPU), như lệnh.

## 13. Bước 11 — So với T5: thành cặp, không lặp khung
**Câu nối cuối T5 → mở đầu T6:**
- T5 kết: *"Zürich didn't grow out. It grew in — one demolition at a time."*
- Câu dẫn đề xuất thêm vào cuối T5: *"Four thousand miles away, another city was tearing itself down too. It wasn't making room."*
- T6 mở bằng một reveal trên sông Detroit, với bộ đếm 31 904.

**Điểm làm hai tập thành cặp:**
- ranh giới đứng yên (Zürich 1934, Detroit khoảng 1930);
- mất dân vào vành ngoài, đo bằng cùng phương pháp tương phản "thành phố ↔ phần còn lại của vùng hành chính";
- phá nhà hàng loạt;
- tiêu đề song song "Why X Shrank While …";
- thumbnail [A] dùng cùng ngữ pháp bản đồ tương phản.

**Tránh lặp khung kể:**

| T5 Zürich | T6 Detroit |
|---|---|
| Xương sống ~1357 → 2026, từng toà mọc đúng năm | Xương sống 1950 → 2026, **không có "từng toà mọc"** (tầng chuẩn); thành phố hiện lên bằng **vùng loang và vạch ranh**, chuyện kể đi qua **5 cơ chế** |
| Máy quay chủ yếu đi dọc sông Limmat | Chuyến bay xương sống dọc **Woodward**, từ sông lên 8 Mile, xuyên qua một thành phố khác (Highland Park) |
| Cao trào ở chương 7: phá để mọc cao hơn | Cao trào ở chương 6: phá để lại đất trống (heat map và 150 730 thửa trống) |
| Bảng màu xanh hồ lạnh / vàng ngói | Bảng màu đỏ gạch / xanh lá ngoại ô |
| Mức XANH, không có nhân vật chính trị còn sống | Mức VÀNG, có nhân vật trong toà án và chính quyền; giọng trung tính, nhiều hồ sơ văn bản |
| Kết: vượt đỉnh "by the city's own count" | Kết: tăng trở lại "by the Census estimate, Vintage 2025", kèm đoạn honest part về các vintage và số đếm 2020 |

## 14. Chi phí; tệp đã ghi
| Mục | Trần | Thực tế |
|---|---|---|
| YouTube Data API | 200 | **135**: thử kết nối 1 · search 100 (hỏng, §3) · videos 3 · channels 12 · playlistItems 17 · commentThreads 2 |
| Claude API | $2 (ghim `claude-haiku-5-5`) | **$0**, 0 lượt: api.anthropic.com trả "x-api-key header is required" (môi trường không có khoá). Ghi một dòng `usd: 0` trong `tienky/cost.jsonl` |
| ElevenLabs | 0 | **0** |
| Giờ máy | ≤ 1 giờ | **≈ 56 phút (ước)**: tải và đo dữ liệu toà 13,6 · Census/PL 3 · tuyến bay 1 · tác tử hero ≈ 23 · tác tử nguồn ≈ 15 (gồm tải bản PDF Kerner 34 MB) |
| Token | trần mềm | 2 tác tử con: nguồn ≈ 270 nghìn, hero ≈ 199 nghìn token (2 vòng); phiên chính ngoài các số này |

**Đã ghi:**
- `channel-k2/k2c-t6-01/TIEN-KY.md`.
- `tienky/` gồm `neo`, `cau`, `khoang-trong`, `binh-luan`, `dan-so`, `claims`, `nhan-vat`, `hero`, `du-lieu-toa`, `xuong-song`, `hinh-xuong-song`, `tuyen-bay`, `cost` (.json) và `cost.jsonl`. Các tệp này được thêm bằng `git add -f`, vì `channel-k2/.gitignore` chặn `*.json`; phiên không sửa `.gitignore`.
- `licenses/` gồm 21 tệp:
  - 3 tệp mới của phiên chính: `census-usgs-tiger-pd`, `loc-sanborn-detroit-1950`, `detroit-opendata-t6`;
  - 3 tệp chép từ `tienky-thanhpho`: `detroit-usgs-topo`, `detroit-loc-gmd`, `detroit-mapping-inequality-KHONG-DUNG` (đổi tên để ghi rõ là KHÔNG dùng);
  - 12 tệp hero: LoC DPC, FSA/OWI, Korab, Highsmith, USN&WR, Keystone, các nguồn khác, Vergara-LOẠI, NPS NRHP, OSM ODbL, footprint ArcGIS, thông cáo chủ sở hữu/Thành phố;
  - 3 tệp chân dung: Ford, Coleman Young (KHÔNG dùng), Sojourner Truth Homes.
  - Mọi email đã thay bằng mô tả đường liên hệ.

**Đề xuất cho P** (chưa ghi, vì nằm ngoài vùng của phiên):
1. `COST-LEDGER.csv`: `T6-01,Tiền kỳ T6 Detroit,Tiền kỳ,2026-10-16,,,,,0,0,claude-haiku-5-5 (không gọi),0,0,,,,,,channel-k2/k2c-t6-01/TIEN-KY.md,YT 135/200 đv (search hỏng); 2 tác tử con; giờ máy ≈ 56 phút; không merge`
2. `RIGHTS.md`: thêm Census/TIGER/USGS (PD), Sanborn 1949–51, ảnh LoC, OSM **khi tập dùng thật** (G1).
3. `AUTHORSHIP.md`: ghi việc chọn Detroit tầng chuẩn, góc kể, cặp tương phản, nhân vật và bảng cách nói trung tính, sau khi chủ dự án duyệt.
4. `channel-k2/.gitignore`: thêm `!k2c-t6-01/tienky/*.json` và `!k2c-t6-01/tienky/*.jsonl`.
5. `HANG-DOI.md`: thêm K2C-T6-01, mức VÀNG.
6. `TIEN-KY-THANHPHO.md`: sửa câu "0 timelapse 3D" của Detroit; sửa ước Sanborn 180–330 giờ thành giá trị ở §11.
7. Cuối lời T5: thêm câu dẫn sang T6 (§13); việc này cần P sửa vùng của T5.
8. `scripts/env/verify.sh` hoặc RUNBOOK: ghi rằng **môi trường cine-lab-av không có khoá Claude API**. Các phiên sau cần biết điều này trước khi lập ngân sách Haiku.

**Ghép thử:** nhánh chỉ thêm tệp mới trong `channel-k2/k2c-t6-01/` (thư mục mới), nên không xung đột với `main`, `tienky-thanhpho`, `k2c-t4-tienky` hay `k2c-t5-tienky`.

## 15. Những điều phiên đã làm khác lệnh hoặc chưa làm được
- **Không gọi Claude API.** Không có khoá; khoảng trống được chấm bằng quy tắc máy thay cho Haiku (§3).
- **Lượt search chính hỏng.** Đã dùng cách đo thay thế; chưa có Cầu-bền riêng cho "Detroit history" (§3).
- **`detroitmi.gov` bị chặn 403 với curl.** Vì vậy mất: thông cáo "first since 1957", trang Proposal N, Terms của cổng dữ liệu, bảng việc làm 1947–1977. Đã thay bằng nguồn Census, FRC/Michigan Treasury, toà án và ArcGIS.
- **Nguồn mốc hero còn yếu:**
  - Hudson's năm 1911, 1983, 1998 chỉ có báo chí;
  - RenCen năm 1977 chỉ có ảnh Korab và OSM;
  - chiều cao MCS bằng m chưa có;
  - số tầng MCS lệch giữa City (18 + 3) và State (15 + 3).

## 16. Preflight
- `bash scripts/env/verify.sh`: 9 PASS, 4 FAIL. Freesound trả 403 (tuỳ chọn); các mục còn lại giống phiên trước. Không mục nào liên quan đến việc tiền kỳ.
- Hook pre-commit/pre-push đã cài đầu phiên. `tools/preflight.sh --range origin/main..HEAD`: **ĐẠT**; `checks/lock.py --verify`: **KHỚP**. Không dùng `--no-verify`.

## 17. Việc đang chờ chủ dự án
1. **Duyệt khuyến nghị:** đi tiếp Detroit ở **TẦNG CHUẨN**, không làm tầng đầy đủ, không chuyển sang Helsinki (§1, §11).
2. **Duyệt cặp tương phản** thành phố ↔ phần còn lại của ba hạt (§4.2), cặp chéo với Zürich (chỉ so %), và **tiêu đề 1 song song với T5**.
3. **Duyệt 5 nhân vật cùng nhóm tổng hợp**, và **bảng cách nói trung tính ở §8**. Mức VÀNG nên phải ghi vào AUTHORSHIP ở G1.
4. **Duyệt hero:** H1, H4 chi tiết; H2, H3 trung cảnh; H6 hạ xuống nền; H5 ảnh 2.5D (≈ 150–205 giờ).
5. **Liên hệ DoIT, City of Detroit** (qua trang Department of Innovation & Technology) để xin xác nhận giấy phép của: Completed Demolitions, Building Footprints, Parcels. Nếu có xác nhận trước G1 thì ch.6 nâng lên "từng nhà tắt đúng ngày", và Short dự phòng được bật.
6. **Cho phép tải tay** (bằng trình duyệt) các trang `detroitmi.gov` bị chặn: thông cáo "first since 1957", Proposal N, Terms. Hoặc chấp nhận nguồn thay thế đã có.
7. **Việc kỹ thuật trước G1:**
   - đối chiếu số hạt 1920–1990 với ảnh trang PDF;
   - cắt TB-8mile theo ranh TIGER;
   - dịch TB-river về phía bờ Mỹ;
   - nối không gian phá dỡ ↔ footprint (nếu được cấp giấy phép);
   - tìm nguồn gốc cho Hudson's (1911, 1983, 1998), RenCen 1977, chiều cao MCS, và các claim D11, D12, D15, D33;
   - tư vấn pháp lý về §120(a) cho tháp Hudson's mới.
8. **Chi phí:** cấp thêm 100 đơn vị YouTube để đo riêng Cầu-bền cho "Detroit history" (chuỗi một cụm, không dùng `|`) nếu muốn. Đề xuất: **không cần**, vì Cầu-ngách đã đạt.
9. **P chép các đề xuất ở §14**, kể cả việc thêm câu dẫn vào cuối lời T5.
