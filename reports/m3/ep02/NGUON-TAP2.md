# NGUON-TAP2 — Nguồn số liệu Tập 2 "Hello, Central"

Ngày truy cập tất cả nguồn: **2026-10-04**. Trích dẫn giữ nguyên tiếng Anh (≤ 40 từ).
Không dùng Wikipedia, trang tổng hợp hay Anthropic Economic Index làm nguồn chính.
Bản tải về chỉ lưu trong thư mục tạm của phiên (không nằm trong repo).

Ghi chú phương pháp:
- Richmond Fed, Feigenbaum & Gross và MLR (FRASER): tải HTML/PDF, đọc bằng `pdftotext` hoặc lọc HTML. Đây là **đọc toàn văn**.
- Các trang BLS (OOH, Table 1.5): `curl` bị 403, `web.archive.org` bị chặn bởi egress policy. Đọc bằng công cụ WebFetch, vốn trả về bản trích do mô hình nhỏ xử lý chứ không phải HTML thô. Tôi coi các trang này là **đọc toàn văn trang, qua WebFetch** và đánh dấu "(WebFetch)". Cần đối chiếu lại bằng trình duyệt trước khi khoá số trong kịch bản cuối.
- Số trong ngoặc "trang" của PDF Feigenbaum: số in trên trang (số trang PDF = số in + 2).

---

## 1. Richmond Fed — "Goodbye, Operator" (Econ Focus, Q4 2019, mục Economic History)

- Tác giả: David A. Price. Ngày đăng trên trang: 2020-01-31.
- URL: https://www.richmondfed.org/publications/research/econ_focus/2019/q4/economic_history
- PDF: https://www.richmondfed.org/-/media/RichmondFedOrg/publications/research/econ_focus/2019/q4/economic_history.pdf (3 trang; các số 178,000 / 342,000 / 250,000 / 40,000 / 1,460 / 1965 nằm ở trang PDF 3; mốc 1892 ở trang PDF 1).
- Trạng thái: **đọc toàn văn**.

| Số | Số liệu đúng | Trích dẫn |
|---|---|---|
| 1a | ~178,000 (1920); ~342,000 ("middle of the century"); <250,000 (1960) | "Growing demand for telephone service led the number of operators to increase for a while, from around 178,000 in 1920 to about 342,000 in the middle of the century — then it declined to less than 250,000 in 1960." |
| 1b | 40,000 (1984); 1,460 (ngành viễn thông, theo BLS, "Today") | "About two decades later, in 1984, the number of operators was down to 40,000. Today, according to the Bureau of Labor Statistics, the telecommunications industry employs a mere 1,460 in its operator ranks" |

Điểm cần lưu ý:
- Bài **không nêu năm cụ thể** cho mốc 342,000, chỉ ghi "in the middle of the century". Không được viết "1950" như thể bài này nói vậy.
- Bài **không ghi nguồn gốc** cho các số 178,000 / 342,000 / 250,000 / 40,000. Đây là số thứ cấp, nên nói "theo Richmond Fed" trong phim.
- 1,460 là số "Today" tại thời điểm viết bài (2019–2020), không có năm. Không dùng làm số hiện tại 2026; số hiện tại dùng mục 3c.
- **Không khớp với nguồn khác:** số 178,000 (1920) của Richmond Fed khác với Feigenbaum & Gross Table II (134,630 người làm tổng đài trong ngành điện thoại năm 1920, cộng 5,740 ở ngành khác; xem mục 4). Hai nguồn định nghĩa khác nhau và bài Richmond Fed không giải thích. Không đặt hai chuỗi số cạnh nhau trên cùng một biểu đồ.

## 5. Mốc kỹ thuật (cùng bài Richmond Fed, đọc toàn văn)

- Tổng đài tự động thương mại đầu tiên: trích: "The first automated telephone switching system … came into use with much fanfare in La Porte, Ind., on Nov. 3, 1892". **Thực tế lịch sử, đã xác minh: 3/11/1892, La Porte, Indiana.**
- Hệ thống Bell (khác với các hãng độc lập) trễ hơn nhiều: "The companies of the Bell System did not install their first fully automated office until Dec. 10, 1921". Đã xác minh. Nên dùng khi nói về lý do Bell chậm tự động hoá.
- 1965: trích: "In 1965, the year after Baker's forecast, the Bell System installed its first permanent fully electronic switching system in Succasunna, N.J." Đã xác minh. **Giữ nguyên chữ "first permanent fully electronic"**; không rút gọn thành "tổng đài điện tử đầu tiên".
- Trạng thái: **đọc toàn văn**. Nguồn thứ hai (Feigenbaum & Gross) có nói chuyển sang chuyển mạch số vào cuối thập niên 1970 ("to 1978") nhưng không nhắc La Porte hay Succasunna, nên hai mốc này chỉ có một nguồn.

## 2. Feigenbaum & Gross — "Answering the Call of Automation: How the Labor Market Adjusted to Mechanizing Telephone Operation"

- NBER Working Paper 28061, tháng 11/2020, sửa lần cuối tháng 2/2024 (bản đọc). Có bản in trên QJE 2024; **tôi không đọc riêng bản QJE**, chỉ đọc bản NBER sửa 2024 (114 trang).
- URL: https://www.nber.org/system/files/working_papers/w28061/w28061.pdf
- Trạng thái: **đọc toàn văn**.

| Ý | Số liệu đúng | Trích dẫn | Trang |
|---|---|---|---|
| 2a. Tỷ lệ mạng được cơ giới hoá | "over half of the U.S. telephone network" 1920–1940 (tóm tắt). Chi tiết chính xác hơn: 32% điện thoại Bell dùng quay số năm 1930, 60% năm 1940, toàn mạng tới 1978 | "Between 1920 and 1940, AT&T undertook one of the largest automation investments in modern history, replacing operators with mechanical switching technology in over half of the U.S. telephone network." | Tóm tắt (trang PDF 2); 32%/60%: tr. 7 |
| 2b. Nhân viên đang làm | Đã làm tổng đài, ở thành phố bị chuyển sang quay số: **ít hơn 8 điểm phần trăm** khả năng còn làm tổng đài 10 năm sau (khoảng 1/3 mức nền); người trên 25 tuổi: **ít hơn khoảng 7 điểm phần trăm** khả năng còn đi làm | "women who were operators in the base year were 8 p.p. less likely to be operators ten years later if exposed to a cutover" | tr. 19 (7 p.p.: tr. 19–20) |
| 2c. Việc làm thấp lương hơn | Người còn làm việc: khoảng **11 điểm phần trăm** nhiều khả năng đổi nghề hơn; điểm thu nhập nghề **giảm 5%** so với **tăng 8%** ở nhóm đối chứng; khoảng 10% rơi vào nghề lương thấp hơn | "The occupation score of operators exposed to cutovers and still working a decade later on average fell 5%, at the same time as their untreated peers' occupation scores increased 8%" | tr. 20 |
| 2d. Thế hệ trẻ sau | Số nữ 16–25 tuổi làm tổng đài **giảm 50–80%** vĩnh viễn, nhưng **không giảm tỷ lệ có việc làm** nói chung; việc làm chuyển sang văn thư kỹ năng trung bình và dịch vụ kỹ năng thấp | "it did not reduce future cohorts' overall employment: the decline in operators was counteracted by employment growth in middle-skill clerical jobs and lower-skill service jobs" | Tóm tắt (PDF tr. 2); 50–80%: tr. 1; kết luận: tr. 27 |

Lưu ý:
- Tác giả cảnh báo kết luận "không giảm việc làm" chỉ đúng cho **thế hệ trẻ sau**, còn nhân viên đang làm chịu thiệt hại thật. Kịch bản không được rút gọn thành "tự động hoá không làm mất việc".
- "Over half" trong tóm tắt nói về mạng lưới toàn Mỹ (mạng AT&T cộng độc lập); số 32%/60% chỉ nói về điện thoại thuộc hệ thống Bell. Đừng lẫn.
- Các hiệu ứng là ước lượng thống kê theo so sánh thành phố, **không** phải số liệu đếm. Đây là kết quả nghiên cứu, không phải con số chính thức.

## 3. BLS — nhân viên chăm sóc khách hàng (CSR), tổng đài viên

### 3a. Dự báo 2023–33: CSR −5.0% và MLR tháng 2/2025
- Bài: Christine Machovec, Michael J. Rieley, Emily Rolen, "Incorporating AI impacts in BLS employment projections: occupational case studies", Monthly Labor Review, tháng 2/2025 (đăng 2025-02-10).
- URL bản FRASER (đọc toàn văn PDF): https://fraser.stlouisfed.org/files/docs/publications/bls_mlr/bls_mlr_20250210.pdf (trang trang chủ bài: https://fraser.stlouisfed.org/title/monthly-labor-review-6130/incorporating-ai-impacts-bls-employment-projections-682808, không tải được trực tiếp). Bản gốc BLS: https://www.bls.gov/opub/mlr/2025/article/incorporating-ai-impacts-in-bls-employment-projections.htm (403 từ môi trường này).
- Mục: Conclusion (trang PDF 5/8 của bản FRASER; số trang in của MLR không có trong bản này). Chú thích 49 dẫn "Table 1.2. Occupational projections, 2023–33".
- Trích: "These occupations include medical transcriptionists and customer service representatives, whose employment is projected to decline by 4.7 and 5.0 percent, respectively, through 2033."
- Câu liền trước (nêu bối cảnh, vượt 40 từ nên chỉ tóm tắt): AI "is expected to primarily affect occupations whose core tasks can be most easily replicated by GenAI in its current form".
- Trạng thái: **đọc toàn văn**. **Dự báo**, không phải thực tế. Ghi chú: đây là dự báo chu kỳ 2023–33, đã được thay bằng 2024–34 và 2025–35 (3b).

### 3b. Dự báo mới hơn cho CSR
**(i) 2024–34 — MLR tháng 1/2026**
- Michael J. Rieley và Javier Colato, "Industry and occupational employment projections overview and highlights, 2024–34", MLR, tháng 1/2026, https://doi.org/10.21916/mlr.2026.1
- URL: https://fraser.stlouisfed.org/files/docs/publications/bls_mlr/bls_mlr_20260108.pdf (đọc toàn văn; Table 2 "Select artificial intelligence related occupations", trang PDF 7/8).
- Số liệu: mã 43-4051, việc làm 2024 **2,814.0 nghìn**, dự báo 2034 **2,660.3 nghìn**, thay đổi **−153.7 nghìn (−5.5%)**.
- Trích: "As a result, demand is expected to be limited for occupations such as billing and posting clerks; procurement clerks; credit authorizers, checkers, and clerks; customer service representatives" — câu kế: "Employment of these occupations is projected to decline or show little change over the 2024–34 decade." (Cắt gọn để ≤ 40 từ.)
- Bài này không có số "annual openings" cho CSR.
- Trạng thái: **đọc toàn văn**. **Dự báo.**

**(ii) 2025–35 — OOH (Occupational Outlook Handbook), cập nhật 2026-08-27**
- URL: https://www.bls.gov/ooh/office-and-administrative-support/customer-service-representatives.htm
- Mục: Quick Facts và Job Outlook.
- Số liệu: việc làm 2025 khoảng **2,666,000** (trang ghi ~2.67 triệu); dự báo **−5%** 2025–35; thay đổi **−141,800**; khoảng **289,500** vị trí tuyển mỗi năm.
- Trích 1: "Employment of customer service representatives is projected to decline 5 percent from 2025 to 2035."
- Trích 2: "about 289,500 openings for customer service representatives are projected each year, on average, over the decade."
- Về tự động hoá: trang có câu "There is expected to be less demand for customer service representatives, especially in retail trade, as their tasks continue to be automated." (đọc qua WebFetch, đoạn còn lại bị tóm tắt, không dùng làm trích nguyên văn).
- Trạng thái: **đọc toàn văn trang (WebFetch)**; cần đối chiếu bằng trình duyệt. **Dự báo** (số việc làm 2025 là số ước tính thực tế trong ma trận việc làm).
- Điểm đáng nêu trong phim: số việc làm giảm 5% nhưng vẫn có ~289,500 vị trí tuyển mỗi năm, vì phần lớn đến từ thay thế người nghỉ hoặc chuyển nghề. Đây không phải mâu thuẫn.
- Các bản lưu của bls.gov qua `web.archive.org` bị egress policy chặn (hiển thị "Blocked by egress policy"); host `blsmon1.bls.gov` trả bản cũ (2019–2020, không dùng được).

### 3c. Table 1.5 — nghề giảm nhanh nhất 2025–35
- URL: https://www.bls.gov/emp/tables/fastest-declining-occupations.htm
- Tên bảng: "Table 1.5 Fastest declining occupations, 2025 and projected 2035 (Employment in thousands)". Cập nhật lần cuối 2026-08-27. Nguồn: U.S. Bureau of Labor Statistics.
- Dòng bảng (nguyên văn từ trang): "Switchboard operators, including answering service | 43-2011 | 35.4 | 26.2 | -9.2 | -26.0 | 38,630" và "Telephone operators | 43-2021 | 3.5 | 2.5 | -1.0 | -27.6 | 41,740" (cột cuối là lương trung vị 2025, USD).
- Tức: **tổng đài viên (switchboard operators, gồm cả dịch vụ trả lời): 35,400 → 26,200 (−26.0%)**; **telephone operators: 3,500 → 2,500 (−27.6%)**.
- Trạng thái: **đọc toàn văn trang (WebFetch)**; cần đối chiếu bằng trình duyệt. **Dự báo** (cột 2025 là số ước tính thực tế).
- Lưu ý khi dùng trong phim: đây là nghề **còn tồn tại** ở quy mô nhỏ, khác với số 1,460 của bài Richmond Fed (chỉ tính trong ngành viễn thông, thời điểm 2019–2020). Hai số đo hai phạm vi khác nhau và hai thời điểm khác nhau.

## 4. Một số đếm nhân viên tổng đài từ điều tra dân số (Census)

- Không tìm được **bảng Census gốc** (Historical Statistics hay bảng nghề nghiệp 1950) trong toàn văn. Đã thử: tìm kiếm Census/Historical Statistics (3 lần), chỉ ra nguồn thứ cấp (Conversable Economist, danh mục mã IPUMS 1950, "Notable Kentucky African Americans"). Không dùng các trang này làm nguồn chính. **Trạng thái mục này (Census gốc): KHÔNG xác minh được.**
- Thay thế đáng tin: Feigenbaum & Gross, Table II (tính từ dữ liệu Census đếm đủ 1910–1940, IPUMS/complete count), tr. 32 (trang PDF 34).
- Số liệu (nghìn người, ngành điện thoại / ngành khác): 1910: 73.03 / 2.40; 1920: 134.63 / 5.74; 1930: 182.04 / 22.83; 1940: 152.70 / 41.17.
- Trích (tr. 13): "The total number of operators working in the telephone industry was growing rapidly at the beginning of the century and peaked in 1930, at 180,000."
- Trạng thái: **đọc toàn văn**. **Thực tế** (nguồn học thuật dựa trên Census; không phải bảng Census gốc).
- Hệ quả: số **342,000 (giữa thế kỷ)** của Richmond Fed **chưa được xác minh bằng nguồn gốc**. Nếu cần số năm 1950 chính xác thì phiên P cần giao việc riêng tìm Census 1950 (Vol. IV, Occupation by Industry) hoặc IPUMS.

---

## Tổng hợp

| số | nguồn | trang | trạng thái | thực tế hay dự báo |
|---|---|---|---|---|
| 1a: 178,000 (1920), 342,000 (giữa TK), <250,000 (1960) | Richmond Fed, Goodbye, Operator | PDF tr. 3/3 | đọc toàn văn; số 342,000 không có năm cụ thể, không có nguồn gốc | thực tế (thứ cấp) |
| 1b: 40,000 (1984); 1,460 (viễn thông, "Today") | Richmond Fed | PDF tr. 3/3 | đọc toàn văn | thực tế |
| 2a: >½ mạng 1920–40; 32% (1930), 60% (1940) Bell | Feigenbaum & Gross NBER w28061 (bản 2/2024) | tóm tắt; tr. 7 | đọc toàn văn (không đọc riêng bản QJE) | thực tế |
| 2b–2c: −8 p.p. còn làm tổng đài; −7 p.p. còn đi làm (>25 tuổi); lương thấp hơn (−5% vs +8%) | Feigenbaum & Gross | tr. 19–20 | đọc toàn văn | thực tế (ước lượng thống kê) |
| 2d: 50–80% giảm, việc làm thế hệ sau không giảm | Feigenbaum & Gross | tr. 1, 27 | đọc toàn văn | thực tế (ước lượng thống kê) |
| 3a: CSR −5.0% (2023–33) và nhận định AI | MLR 2/2025 (bản FRASER) | PDF tr. 5/8, mục Conclusion | đọc toàn văn | dự báo |
| 3b(i): CSR 2,814.0 → 2,660.3 nghìn (−5.5%), 2024–34 | MLR 1/2026 (bản FRASER), Table 2 | PDF tr. 7/8 | đọc toàn văn | dự báo |
| 3b(ii): CSR ~2.67 triệu (2025), −5% 2025–35, −141,800, ~289,500 vị trí/năm | BLS OOH (cập nhật 2026-08-27) | Quick Facts, Job Outlook | đọc toàn văn trang (WebFetch); cần đối chiếu | dự báo (2025 là ước tính thực tế) |
| 3c: switchboard 35.4 → 26.2 nghìn (−26.0%); telephone operators 3.5 → 2.5 nghìn (−27.6%) | BLS Table 1.5 | bảng (cập nhật 2026-08-27) | đọc toàn văn trang (WebFetch); cần đối chiếu | dự báo (2025 là ước tính thực tế) |
| 3b: openings CSR trong MLR 1/2026 | MLR 1/2026 | n/a | KHÔNG xác minh được (bài không có cột này; số openings lấy từ OOH) | n/a |
| 4: số Census gốc (1950 hoặc Historical Statistics) | Census/Historical Statistics | n/a | KHÔNG xác minh được (đã thử 3 lần; chỉ có nguồn thứ cấp); thay bằng Feigenbaum Table II | thực tế |
| 4 (thay thế): 73.03 / 134.63 / 182.04 / 152.70 nghìn (1910/20/30/40) | Feigenbaum & Gross Table II | tr. 32 | đọc toàn văn | thực tế |
| 5a: La Porte, Indiana, 3/11/1892 | Richmond Fed | PDF tr. 1/3 | đọc toàn văn | thực tế |
| 5b: Succasunna, NJ, 1965 (first permanent fully electronic) | Richmond Fed | PDF tr. 3/3 | đọc toàn văn | thực tế |
| 5c: Bell, văn phòng tự động hoàn toàn đầu tiên 10/12/1921 | Richmond Fed | PDF tr. 1/3 | đọc toàn văn | thực tế |

## Việc đang chờ chủ dự án / phiên P
1. Quyết định có chấp nhận số 178,000 (1920) và 342,000 (giữa TK) như số thứ cấp "theo Richmond Fed", hay giao thêm việc tìm Census gốc.
2. Duyệt cách xử lý lệch số giữa Richmond Fed (178,000, 1920) và Feigenbaum & Gross (134,630 + 5,740, 1920).
3. Đối chiếu bằng trình duyệt các số BLS 2025–35 (OOH, Table 1.5) vì đọc qua WebFetch, trước khi khoá vào kịch bản.
4. Ghi các nguồn vào `RIGHTS.md` nếu có dùng trích dẫn hoặc biểu đồ lấy từ các nguồn này.

---

## 6. Bổ sung sau G1 (P, 05/10/2026; vòng tra trần 80 nghìn token)

### 6a. BLS 2025–35, CSR (chủ dự án giao)
- https://www.bls.gov/ooh/office-and-administrative-support/customer-service-representatives.htm — 2 666 000 (2025) → 2 524 100 (2035), −5,3 % (BLS làm tròn −5 %). **Đã xác minh (Claude, 05/10/2026)**: chủ dự án ghi ở G1; P không vào được bls.gov (403). **Dự báo.**

### 6b. Brynjolfsson, Li & Raymond, "Generative AI at Work", NBER w31161 (tháng 4/2023, sửa 11/2023)
- PDF: https://www.nber.org/system/files/working_papers/w31161/w31161.pdf — **đọc toàn văn** (pdftotext).
- Tóm tắt (tr. bìa): "data from 5,179 customer support agents. Access to the tool increases productivity, as measured by issues resolved per hour, by 14% on average, including a 34% improvement for novice and low-skilled workers but with minimal impact on experienced and highly skilled workers."
- Tr. 2: "treated agents with two months of tenure perform just as well as untreated agents with more than six months of tenure."
- Tr. 3: "a substantial decrease in worker attrition, which is driven by the retention of newer workers." · "our paper is not designed to shed light on the aggregate employment or wage effects of generative AI tools. Firms may respond to increasing productivity among novice workers by hiring more of them, de-skilling positions, or seeking to develop more powerful AI systems that can replace lower-skill workers entirely."
- Tr. 9: một công ty phần mềm Fortune 500; nhân viên phần lớn làm ở **Philippines** (một nhóm nhỏ ở Mỹ) → **khác địa lý với BLS: không đặt chung khung với số BLS** (luật so sánh, điểm 3). Số là ước lượng thống kê trong một công ty (thực tế, không phải dự báo).
- Bản QJE 2025 không đọc; dùng bản NBER.

### 6c. Brynjolfsson, Chandar & Chen, "Canaries in the Coal Mine? Six Facts…", bản tháng 8/2026
- PDF: https://digitaleconomy.stanford.edu/app/uploads/2026/08/Canaries_August2026.pdf — **đọc toàn văn** (dữ liệu ADP tới 6/2026).
- Tóm tắt: "(1) We find no evidence of widespread, economy-wide job displacement. (2) However, employment of young workers (ages 22–25) in AI-exposed occupations now stands 19% below where it would be had it kept pace with that of their less-exposed peers; experienced workers show no comparable gap. … (4) It operates primarily through reduced hiring of young workers rather than increased separations." · "early, descriptive indicators … rather than causal estimates".
- Table A.6 (PDF tr. 56): **Customer Service Representatives** xếp **thứ 2** theo số việc làm ADP trong nhóm phơi nhiễm AI cao nhất (Quintile 5, tháng 10/2022).
- Không dùng số riêng cho CSR trẻ (chỉ có hình B.3/H.2, cỡ mẫu nhỏ 30–63 người).
