# NGUON-TAP3 — Nguồn số liệu Tập 3 "Giao dịch viên ngân hàng & ATM"

Ngày truy cập tất cả nguồn: **2026-10-05**. Trích dẫn giữ nguyên tiếng Anh (≤ 40 từ).
Không dùng Wikipedia, trang tổng hợp hay Anthropic Economic Index làm nguồn chính.
Bản tải về chỉ lưu trong thư mục tạm của phiên (không nằm trong repo). Số lượt tải đã dùng: 10 (trong đó 3 lượt hỏng: IMF F&D bản 2015/09 trả 404; BU/SSRN trả HTML; BIS WP 1244 trả HTML/JS chặn).

Ghi chú phương pháp:
- Mọi nguồn dưới đây tải bằng `curl` rồi `pdftotext`. Đây là **đọc toàn văn**.
- bls.gov trả 403: không thử. Số BLS cần dùng chỉ liệt kê ở cuối (CHỜ XÁC MINH).
- Số trang MLR/FRASER: bản PDF là bản in từ trang web (8 trang, không có số trang in). Ghi **trang PDF**.

---

## 1. Bessen — "Toil and Technology" (IMF Finance & Development, tháng 3/2015)

- Tác giả: James Bessen. Bản đã sửa ("corrected, 1/20/2015" in trên trang 17).
- URL: https://www.imf.org/external/pubs/ft/fandd/2015/03/pdf/bessen.pdf (đường dẫn `2015/09` là sai, 404).
- Trạng thái: **đọc toàn văn** (5 trang PDF, trang in 16–20; ghi theo trang in).

| Số | Số liệu | Trích dẫn | Trang in |
|---|---|---|---|
| 1a | ATM lắp lần đầu ở Mỹ và các nước phát triển trong thập niên 1970; từ giữa thập niên 1990 ngân hàng tăng nhanh việc dùng ATM; "over 400,000" ATM ở Mỹ ("today", bài 2015, không ghi năm) | "Starting in the mid-1990s, banks rapidly increased their use of ATMs; over 400,000 are installed in the United States alone today." | 17 |
| 1b | Số giao dịch viên cần cho một chi nhánh đô thị trung bình: **20 → 13**, giai đoạn **1988–2004** | "the number of tellers required to operate a branch office in the average urban market fell from 20 to 13 between 1988 and 2004." | 17 |
| 1c | Chi nhánh ngân hàng khu đô thị tăng **43%** (bài **không ghi giai đoạn riêng** cho số này; câu liền kề dùng 1988–2004) | "Bank branches in urban areas increased 43 percent." | 17 |
| 1d | Vai trò chuyển sang quan hệ khách hàng / bán sản phẩm | "tellers became an important part of the 'relationship banking team.'" ... "cash handling became less important and human interaction more important." | 17 |
| 1e | Số giao dịch viên **không giảm** khi ATM lắp rộng (Chart 1, chỉ là biểu đồ, không có số trong chữ) | "the number of bank teller jobs did not decrease as the ATMs were rolled out (see Chart 1)." | 17 |

Điểm cần lưu ý:
- **Nguồn dữ liệu của Bessen:** Chart 1 ghi nguồn: IPUMS (Ruggles và cộng sự, Version 5.0), BLS Occupational Employment Survey, và BIS Committee on Payment and Settlement Systems (cho số ATM). Bài **không nêu** nguồn riêng của 20→13 và 43% (nguồn gốc nằm ở sách Bessen 2015 "Learning by Doing", tr. 107–9 theo mục 2; **tôi không đọc sách**). Vì vậy 20→13 và 43% là số thứ cấp do Bessen trích; nói "theo Bessen".
- Bài **không có bảng số giao dịch viên theo năm**. Chart 1 chỉ là đường vẽ; đọc số từ biểu đồ là ước lượng bằng mắt, **không dùng làm số khoá**.
- "Over 400,000" ATM là số "today" của bài 2015, không phải số năm cụ thể. Không viết thành "năm 2015" hay "năm 2010".

## 2. Bessen — "How Computer Automation Affects Occupations: Technology, jobs, and skills" (BU Law WP 15-49; bản NBER Summer Institute 2016)

- Tác giả: James Bessen. Bản đọc: bản hội thảo NBER SI 2016, đề "5/16", 48 trang (số trang in = số trang PDF).
- URL: https://conference.nber.org/confer/2016/SI2016/PRIT/Bessen.pdf
- Trạng thái: **đọc toàn văn** (bản hội thảo; **không** đọc riêng bản WP 15-49 ngày 3/10/2016 vì tải từ BU/SSRN thất bại, nên số trang có thể lệch bản đó).

| Số | Số liệu | Trích dẫn | Trang |
|---|---|---|---|
| 2a | Từ 2000, số giao dịch viên **toàn thời gian quy đổi (FTE)** tăng **2,0%/năm**, nhanh hơn lực lượng lao động chung | "since 2000, the number of fulltime equivalent bank tellers has increased 2.0% per annum, substantially faster than the entire labor force." | 6 |
| 2b | Cơ chế: ATM giảm chi phí chi nhánh, ngân hàng mở thêm chi nhánh | "the ATM allowed banks to operate branch offices at lower cost; this prompted them to open many more branches" | 6 |
| 2c | Định nghĩa / nguồn dữ liệu | "Data from the 1% samples of the Census and ACS survey ... fulltime equivalent workers by dividing total hours worked by 2080." | 6 (chú thích 7) |
| 2d | Hình 1: giao dịch viên FTE và số ATM (BIS), 1970–khoảng 2013 (chỉ có biểu đồ) | "Teller data from Census and ACS 1% samples. Fulltime equivalent workers calculated assuming 2080 hours per work year. Data on number of ATMs installed from the Bank for International Settlements." | 46 |

Điểm cần lưu ý:
- **Chuỗi của Bessen là Census/ACS 1%, FTE (giờ làm / 2080), Mỹ, đến khoảng 2013.** Không phải chuỗi BLS OES/OOH đếm người. Không đặt chuỗi này cạnh số BLS trên cùng một biểu đồ.
- Chú thích 7 nêu: tổng việc làm ngân hàng tăng vọt từ thập niên 1970 đến đầu 1980 (một phần do bỏ quản lý), giảm trong khủng hoảng S&L tới thập niên 1990, rồi tăng lại. Vậy "giao dịch viên không giảm" phụ thuộc mốc đầu/cuối.
- Hình 1 (đọc bằng mắt, chỉ để định hướng): đường FTE đi từ khoảng 190 nghìn (1970), khoảng 400 nghìn (1980), đáy khoảng 340 nghìn quanh 2000, rồi lên khoảng 450 nghìn ở điểm cuối. **Không trích thành số trong phim.**
- Chuỗi **dừng quanh 2013**: không cho biết giảm sau 2010. Không dùng để nói "giao dịch viên vẫn tăng đến nay".
- Bessen 2015 (mục 1) nói "tellers" bằng số lượng việc, bản 2016 dùng FTE: hai định nghĩa khác nhau.

## 3. BLS — Monthly Labor Review, tháng 2/2025

- Bài: Christine Machovec, Michael J. Rieley, Emily Rolen, "Incorporating AI impacts in BLS employment projections: occupational case studies". Đăng 2025-02-10.
- URL: https://fraser.stlouisfed.org/files/docs/publications/bls_mlr/bls_mlr_20250210.pdf
- Trạng thái: **đọc toàn văn** (8 trang PDF; ghi trang PDF).

| Số | Số liệu | Trích dẫn | Trang PDF |
|---|---|---|---|
| 3a | Credit analysts (SOC 13-2041): **−3,9%**, **dự báo 2023–33**; việc làm 73,7 nghìn (2023) → 70,8 nghìn (2033), thay đổi −2,8 nghìn | "credit analysts are likely to see decreasing employment demand, and their employment is projected to decline 3.9 percent from 2023 to 2033." | 4 (văn bản và Table 3) |
| 3b | Lý do BLS nêu | "AI can synthesize large amounts of data and reach big-picture conclusions, and, indeed, these tasks are the essence of a credit rating" | 4 |
| 3c | Claims adjusters, examiners, and investigators (13-1031): −4,4%, 2023–33; 345,2 → 330,0 nghìn (bảo hiểm, ngoài phạm vi nghề ngân hàng) | "employment of claims adjusters, examiners, and investigators is projected to decline 4.4 percent" | 4 |
| 3d | Personal financial advisors (13-2052): +17,1%, 2023–33 (đối chiếu: tác động AI không đồng đều) | "Employment of personal financial advisors is projected to grow 17.1 percent from 2023 to 2033" | 4 |

Điểm cần lưu ý:
- Câu chữ của chủ dự án **được xác minh**: credit analysts −3,9% là **dự báo 2023–33**, không phải số thực tế. Tên bài khớp.
- **Bài này không có loan officers và tellers** (tìm toàn văn, không thấy). Không suy ra số cho hai nghề đó từ bài này.
- BLS ghi đây là dự báo có tính đến tác động AI (đánh giá định tính theo ca nghiên cứu), không phải đo kết quả thực.
- Ghi chú 39 của bài dẫn bài của GICP (2023) làm cơ sở cho nhận định credit analysts; đó là nguồn của BLS, không phải số đo độc lập.

## 4. BLS — Monthly Labor Review, tháng 1/2026

- Bài: "Industry and occupational employment projections overview and highlights, 2024–34". Số tháng 1/2026.
- URL: https://fraser.stlouisfed.org/files/docs/publications/bls_mlr/bls_mlr_20260108.pdf
- Trạng thái: **đọc toàn văn** (8 trang PDF; ghi trang PDF).

| Số | Số liệu | Trích dẫn | Trang PDF |
|---|---|---|---|
| 4a | Customer service representatives (43-4051): **−5,5%**, **dự báo 2024–34**; 2.814,0 → 2.660,3 nghìn (−153,7 nghìn) | (số trong Table 2) | 7 (Table 2); văn bản nêu nghề ở trang 5 |
| 4b | Credit authorizers, checkers, and clerks (43-4041): −6,2%, 2024–34; 12,0 → 11,3 nghìn | (số trong Table 2) | 7 |
| 4c | Claims adjusters, examiners, and investigators (13-1031): **−5,1%**, 2024–34; 356,1 → 337,9 nghìn | "employment of these workers is projected to decline 5.1 percent from 2024–34." | 5 (văn bản); 6 (Table 2) |
| 4d | Lý do chung cho nhóm văn phòng | "demand is expected to be limited for occupations such as billing and posting clerks; procurement clerks; credit authorizers, checkers, and clerks; customer service representatives" | 5 |

Điểm cần lưu ý:
- **Customer service representatives là nghề CSKH nói chung (mọi ngành), không phải CSKH ngân hàng.** Không viết thành "nhân viên CSKH ngân hàng".
- **Bài 2026 không có credit analysts, loan officers, tellers.** Credit analysts −3,9% (2023–33) là của bài 2025, đợt khác: không ghép với số 2024–34.
- Credit authorizers/checkers/clerks (12 nghìn) là nghề nhỏ, không phải loan officers hay credit analysts.

---

## Bảng tổng hợp số dùng được

| # | Số | Loại | Năm / đợt | Nguồn khoá | Trang |
|---|---|---|---|---|---|
| A1 | Giao dịch viên mỗi chi nhánh đô thị trung bình: 20 → 13 | Thực tế (theo Bessen, thứ cấp) | 1988–2004 | Bessen F&D 2015 | 17 |
| A2 | Chi nhánh đô thị +43% | Thực tế (theo Bessen, thứ cấp; giai đoạn không ghi riêng) | không rõ, liền kề 1988–2004 | Bessen F&D 2015 | 17 |
| A3 | Hơn 400.000 ATM ở Mỹ | Thực tế ("today" của bài 2015) | khoảng 2015, không ghi năm | Bessen F&D 2015 | 17 |
| A4 | Giao dịch viên FTE +2,0%/năm | Thực tế (Census/ACS, FTE) | từ 2000 đến cuối chuỗi (khoảng 2013) | Bessen WP 15-49 | 6 |
| A5 | Vai trò chuyển sang "relationship banking team" | Thực tế (định tính) | 1990s–2000s | Bessen F&D 2015 | 17 |
| B1 | Credit analysts −3,9% (73,7 → 70,8 nghìn) | **Dự báo** | 2023–33 | MLR 2/2025 | 4 |
| B2 | Customer service representatives −5,5% (mọi ngành) | **Dự báo** | 2024–34 | MLR 1/2026 | 7 |
| B3 | Claims adjusters −5,1% (bảo hiểm) | **Dự báo** | 2024–34 | MLR 1/2026 | 5–6 |

## Số cố ý không dùng

- Số giao dịch viên "theo năm" đọc từ Chart 1 / Figure 1 của Bessen: chỉ là biểu đồ, không có số trong chữ.
- 20 → 13 và 43% **không** ghép với 2,0%/năm thành một "câu chuyện số" duy nhất: khác chuỗi, khác năm, khác định nghĩa (số giao dịch viên mỗi chi nhánh so với FTE toàn quốc).
- Credit analysts −3,9% (2023–33) không ghép với số 2024–34 của bài 2026.
- Số giao dịch viên giảm sau 2007–2010: **không tìm được nguồn toàn văn** trong phạm vi đã tải (Bessen dừng ~2013 và không cho thấy giảm). Không nêu mà không có nguồn.
- Số tổ chức/số chi nhánh FDIC/Fed: không tải (không cần theo phạm vi, không có nguồn toàn văn trong tay).
- Nghiên cứu độc lập về AI trong ngân hàng (BIS WP 1244 "Artificial intelligence and relationship lending", dữ liệu ngân hàng Ý): **tải thất bại (HTML bị chặn), chưa đọc toàn văn**, nên không ghi số. Nếu dùng thì phải nói rõ địa lý Ý, không phải Mỹ.
- Số 47% của Frey & Osborne (xuất hiện trong bài Bessen): không phải số của Bessen và không đọc nguồn gốc.

## Danh sách BLS cần Claude (Cowork) xác minh (CHỜ XÁC MINH)

Không đọc được từ môi trường này (bls.gov 403). Chưa có số nào dưới đây được đọc; không có số giả định.

| Bảng / mục | URL | Số cần đọc |
|---|---|---|
| OOH — Tellers, mục Summary và Job Outlook | https://www.bls.gov/ooh/office-and-administrative-support/tellers.htm | Việc làm hiện tại (năm cơ sở), % thay đổi dự báo **2025–35**, số việc làm giảm; câu chữ BLS về lý do (ATM, ngân hàng trực tuyến) |
| OOH — Loan Officers, Summary và Job Outlook | https://www.bls.gov/ooh/business-and-financial/loan-officers.htm | Việc làm năm cơ sở, % thay đổi **2025–35**, câu chữ về tác động công nghệ/AI |
| OOH — Credit Analysts, Summary và Job Outlook | https://www.bls.gov/ooh/business-and-financial/credit-analysts.htm | Việc làm năm cơ sở, % thay đổi **2025–35** (đối chiếu −3,9% của đợt 2023–33) |
| Employment Projections, Table 1.2 hoặc 1.7 (nghề, 2025–35) | https://www.bls.gov/emp/tables/emp-by-detailed-occupation.htm | Mã SOC 43-3071 (Tellers), 13-2072 (Loan officers), 13-2041 (Credit analysts): việc làm 2025 và 2035 |
| OEWS (nếu cần số thực tế mới nhất) | https://www.bls.gov/oes/current/oes433071.htm | Tellers: việc làm theo năm gần nhất. Dùng để kiểm chứng giảm sau ~2010 (thực tế), cần chuỗi nhiều năm (OEWS các năm cũ) |
| OOH tellers, số "Employment" lịch sử | cùng URL OOH tellers | Số tellers ~2010 và năm gần nhất, nếu có bản lưu hợp lệ, để dựng "giảm sau 2010" |

Việc đang chờ chủ dự án: duyệt danh sách số dùng được ở trên, cho phép Cowork xác minh BLS, và quyết định có cần một nghiên cứu độc lập về AI trong ngân hàng (BIS 1244 hoặc nguồn khác, cần tải lại bản toàn văn).

---

# PHỤ LỤC — Vòng bổ sung (2026-10-05): chuỗi giao dịch viên theo bảng và nghiên cứu ML tín dụng ở Mỹ

Vòng này dùng thêm 5 lượt tải (tổng cộng tệp này: 15). Mục cũ ở trên không đổi.

## 5. Census — Historical Statistics of the United States, Colonial Times to 1970, Part 1, Chapter D (Labor), Series D 233–682

- Tiêu đề bảng: "Detailed Occupation of the Economically Active Population: 1900 to 1970". Đơn vị: nghìn người, 14 tuổi trở lên (riêng cột 1970 có thêm bản 16 tuổi trở lên).
- URL (kiểm, tải được): https://www2.census.gov/library/publications/1975/compendia/hist_stats_colonial-1970/hist_stats_colonial-1970p1-chD.pdf (62 trang PDF).
- Trạng thái: **đọc bảng (không phải toàn văn chương)**. PDF là bản quét hình, không có lớp chữ, và môi trường không có OCR. Tôi dựng lại trang chứa hàng "Bank tellers" (series 355) và **đọc bằng mắt** ở độ phân giải 300 dpi. Tôi **không đọc** chú thích cuối bảng và phần giải thích số liệu. Số vì thế cần đối chiếu lại bản gốc trước khi khoá.
- Vị trí: trang in 141, trang PDF 21 của tệp chương. Nhóm "Clerical and kindred workers" (series 337), hàng 355 "Bank tellers".

| Cột (cách phân loại) | Nghìn người | Ghi chú |
|---|---|---|
| 1970, 16 tuổi trở lên | **253** | phân loại 1970 |
| 1970, 14 tuổi trở lên | **254** | phân loại 1970 |
| 1960, theo phân loại 1970 | **135** | cùng phân loại với số 1970, so sánh được |
| 1960, theo phân loại 1960 | **131** | |
| 1950, theo phân loại 1960 | **65** | |
| 1950, theo phân loại 1950 | **32** | trong bảng, ô này nằm cạnh dấu ngoặc nhóm (3.178 là tổng nhóm), nên định nghĩa 1950 rộng hơn hoặc gộp; **không dùng một mình** |
| 1900–1940 | không có số riêng | hàng gộp trong nhóm, không tách được |

Điểm cần lưu ý:
- Trong bản quét, số bị xếp lệch nửa dòng so với nhãn hàng. Tôi ghép số vào nhãn bằng cách đối chiếu các nghề lân cận có số đã biết (ví dụ Telephone operators 1970 khoảng 420 nghìn). Mức chắc chắn: cao, nhưng chưa phải bằng OCR hay chữ số.
- **Ngắt chuỗi:** số 1950, 1960, 1970 dùng các phân loại khác nhau (1950, 1960, 1970). Chuỗi sạch duy nhất theo bảng: **1960 (135) → 1970 (253), cùng phân loại 1970**, tức khoảng gấp 1,9 lần. Không nối 32 (1950, phân loại 1950) với 253.
- Tuổi: 14+ (1970: 254) khác 16+ (1970: 253), chênh 1 nghìn.
- Đơn vị là **người** (economically active population), khác chuỗi FTE của Bessen (mục 2). Bessen vẽ khoảng 190 nghìn FTE cho 1970 trên biểu đồ; HSUS cho 253 nghìn người. Hai số khác loại, **không đặt chung**.
- Không có nguồn cùng loại cho 1980–2010: Bessen (Census/ACS FTE) chỉ có biểu đồ; MLR/FRASER cho tellers theo năm: **không tìm được**. Câu "giao dịch viên đi ngang 1980–2010" xuất hiện trong kết quả tìm kiếm nhưng từ trang BLS (bị 403, chưa đọc). **Không dùng.** Đưa vào danh sách CHỜ XÁC MINH (OEWS/OOH tellers chuỗi năm).

## 6. Meursault, Moulton, Santucci & Schor — "One Threshold Doesn't Fit All: Tailoring Machine Learning Predictions of Consumer Default for Lower-Income Areas" (Philadelphia Fed WP 22-39)

- Tác giả: Vitaly Meursault, Daniel Moulton, Larry Santucci, Nathan Schor (Federal Reserve Bank of Philadelphia). Đăng 11/2022, sửa 10/2024 (bản đọc).
- URL: https://www.philadelphiafed.org/-/media/frbp/assets/working-papers/2022/wp22-39.pdf
- Trạng thái: **đọc các phần liên quan (tóm tắt, mở đầu, phương pháp, kết quả chính)**, đã tải toàn bộ 76 trang; không đọc hết phụ lục. Địa lý: **Mỹ**, dữ liệu hồ sơ tín dụng (credit bureau) người tiêu dùng, 2000–2021 (tr. in 17: kết quả theo năm 2004–2019).

| Số | Số liệu | Trích dẫn | Trang PDF |
|---|---|---|---|
| 6a | Mô hình ML (XGBoost) dự báo vỡ nợ tốt hơn mô hình logistic ở mọi năm 2004–2019 (đo bằng ROC AUC; chỉ có hình, không có số AUC trong chữ) | "in all periods, XGBoost performs better than a logistic model." | 18 |
| 6b | Chênh lệch lợi nhuận: ML hơn logistic **khoảng 2%** "under a set of assumptions" (Section 4.6) | "it corresponds to a 2 percent profit difference under a set of assumptions" | 18 |
| 6c | Với ngưỡng duy nhất, người vay đáng tin ở khu vực thu nhập thấp–trung bình có khả năng được xếp "đáng tin" thấp hơn khoảng **9 điểm phần trăm** | "a creditworthy LMI tract consumer is about 9 percentage points less likely to be classified as creditworthy than a creditworthy non-LMI tract consumer." | 6 |

Điểm cần lưu ý:
- **Đây là nghiên cứu về độ chính xác và công bằng của mô hình chấm điểm tín dụng bằng ML, không phải nghiên cứu việc làm.** Không có số về loan officers hay credit analysts mất việc. Chỉ dùng để nói: ML chấm điểm tín dụng chính xác hơn mô hình truyền thống (đo thật, Mỹ), nhưng "2%" là kết quả mô phỏng theo giả định của tác giả, không phải lợi nhuận ngân hàng thực.
- 6c là về công bằng, không nên đưa vào phim về nghề.
- Đây là working paper Fed, chưa phản biện (bản đọc). Ý kiến tác giả không phải quan điểm của Fed Philadelphia hay Fed (ghi trong miễn trừ).

## Số cố ý không dùng (bổ sung)

- Fuster, Goldsmith-Pinkham, Ramadorai & Walther (J. Finance 2022): **không đọc được toàn văn**. Bản Semantic Scholar tải về thực chất là bộ slide của người bình luận (Tobias Berg, 9/2020), **không phải bài gốc**; Wiley và SSRN trả HTML. Tôi không dùng bất kỳ số nào từ slide đó (ví dụ "PD 1,6% → 1,9%").
- Số 253 nghìn (1970) ghép với số FTE của Bessen: không ghép (khác loại).
- Số 32 nghìn (1950, phân loại 1950): không dùng, định nghĩa không rõ (xem mục 5).

## Cập nhật số dùng được (thêm vào bảng tổng hợp)

| # | Số | Loại | Năm | Nguồn khoá | Trang |
|---|---|---|---|---|---|
| C1 | Bank tellers: **135 nghìn (1960) → 253 nghìn (1970)**, cùng phân loại 1970, 16+ (14+: 254) | Thực tế (Census, người) | 1960, 1970 | HSUS Series D 355 | in 141 (PDF 21); đọc bằng mắt từ bản quét, cần đối chiếu |
| C2 | ML (XGBoost) dự báo vỡ nợ tốt hơn logistic; chênh lợi nhuận khoảng 2% (mô phỏng, theo giả định) | Thực tế/mô phỏng (Mỹ, dữ liệu tín dụng) | 2004–2019 | Philadelphia Fed WP 22-39 | 18 |

Việc đang chờ chủ dự án: (1) cho phép Cowork đối chiếu bản gốc HSUS (hàng 355, trang in 141) và BLS tellers; (2) quyết định có chấp nhận C2 như bằng chứng "ML hiệu quả trong tín dụng" (không phải bằng chứng về việc làm), hay tìm tiếp một nghiên cứu về việc làm hoặc chatbot/gian lận ngân hàng.
