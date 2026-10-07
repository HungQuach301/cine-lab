# NGUON-TAP4 — Nguồn số liệu Tập 4 "The Typing Pool"

Ngày truy cập tất cả nguồn: **2026-10-05**. Trích dẫn giữ nguyên tiếng Anh (≤ 40 từ).
Không dùng Wikipedia, trang tổng hợp hay Anthropic Economic Index làm nguồn chính. Chỉ số liệu Mỹ.
Bản tải về chỉ lưu trong thư mục tạm của phiên (không nằm trong repo).

Ghi chú phương pháp:
- **HSUS (Census 1975)**: PDF tải bằng curl (62 trang, 6,9 MB). **PDF là ảnh quét, không có lớp chữ**; không có OCR trong môi trường. Tôi đã **đọc bằng mắt trên ảnh dựng lại từ PDF** (pdftoppm, 130–250 dpi) các trang PDF 5, 6, 19, 20, 21. Số liệu hàng 347 đọc ở độ phân giải 250 dpi. Đã **kiểm chéo nội bộ**: nữ + nam của nhóm "Clerical" (D 220 + D 203) cộng đúng bằng tổng hai giới (D 186) ở cả 11 cột (ví dụ 1970: 10.461 + 3.748 = 14.209 so với 14.208, sai số làm tròn). Dù vậy, số hàng 347 chỉ có **một lần đọc**, nên cần một người đối chiếu bằng mắt trên PDF gốc trước khi khoá vào kịch bản cuối.
- Số trang HSUS: **số in** trên trang (số trang PDF = số in − 120). Trong cột bảng dùng "tr. 141 (PDF 21)".
- MLR (FRASER/BLS): `pdftotext` toàn văn bản đã lưu. Trang ghi là trang PDF của bản lưu (bản in từ trang web), không phải số trang tạp chí in.
- Các trang BLS (OOH, Table 1.5, Employment Projections): `curl` trả 403, không tải được. **Không có số BLS nào dưới đây ngoài MLR được coi là đã xác minh.**

---

## 1. Census Bureau — *Historical Statistics of the United States, Colonial Times to 1970*, Part 1, Chapter D "Labor" (Series D 1–682)

- Tác giả: U.S. Department of Commerce, Bureau of the Census (1975). Nguồn gốc bảng D 233–682: U.S. Census of Population (1900–1970); 1900–1950 theo Kaplan & Casey, *Occupational Trends in the United States, 1900–1950*, Working Paper No. 5, 1958 (tr. 125).
- URL: https://www2.census.gov/library/publications/1975/compendia/hist_stats_colonial-1970/hist_stats_colonial-1970p1-chD.pdf (HTTP 200; tệp nội bộ "1-11-d-labor.pdf").
- Trạng thái: **đã đọc các trang bảng cần dùng và trang chú thích định nghĩa (đọc bằng mắt, ảnh quét)**; không đọc toàn bộ 62 trang (không cần).

### 1a. Series D 233–682, hàng 347 "Stenographers, typists, and secretaries" (nghìn người, cả hai giới)

Tiêu đề bảng (tr. 141, PDF 21): "Detailed Occupation of the Economically Active Population: 1900 to 1970". Đơn vị: "In thousands of persons 14 years old and over, except as indicated." Ngày điều tra: 1900 1/6; 1910 15/4; 1920 1/1; 1930–1970 1/4 (tr. 140, PDF 20).

Tách theo **phân loại nghề của từng đợt**. Mỗi đoạn dùng một phân loại; **không nối các đoạn khác phân loại thành một đường liền**.

| Đoạn (phân loại) | Năm: số (nghìn) |
|---|---|
| Phân loại 1950 | 1900: **134**; 1910: **387**; 1920: **786**; 1930: **1.097**; 1940: **1.223**; 1950: **1.661** |
| Phân loại 1960 | 1950: **1.629**; 1960: **2.313** |
| Phân loại 1970 | 1960: **2.316**; 1970: **3.914** (từ 16 tuổi) / **3.920** (từ 14 tuổi) |

Trích định nghĩa (tr. 140–141): nhãn hàng đúng là "Stenographers, typists, and secretaries" (Series 347, nằm trong nhóm "Clerical and kindred workers", Series 337).

Lưu ý định nghĩa và độ tin cậy:
- **Gộp ba nghề** (tốc ký, đánh máy, thư ký) thành một hàng. **Không có tách riêng** từng nghề, và **không có tách nam/nữ cho hàng 347**; bảng chỉ có nam/nữ cho nhóm lớn (xem 1b).
- Hàng này **không phải** "word processors and typists" của BLS (xem mục "Rủi ro so sánh" ở cuối).
- Chú thích của Census (tr. 125, nguồn D 182–232): "the changes made for each of the censuses affect the comparability of data from one census to another." Số nhóm nghề tăng từ 297 (1960) lên 441 (1970). Hai thay đổi 1970: (1) phân bổ ca "not reported" vào nhóm lớn, làm tổng 1970 lớn hơn so với 1950 và 1960; (2) giới hạn tuổi theo định nghĩa lực lượng lao động (16+).
- Cùng chú thích: số liệu 1900 "are approximations only"; "Particularly prior to 1910, there is little information available on the exact definitions used". Nhóm tuổi: "Prior to 1940, this refers to civilian gainful workers 10 years old and over; for 1940 and 1950, … 14 years old and over" (tr. 125), trong khi tiêu đề bảng nói 14+. **Cần xử lý như ngắt chuỗi nhẹ giữa 1930 và 1940.**
- Khi xem **mức tăng 1960–1970**: dùng cặp **cùng phân loại 1970** (2.316 → 3.914), không dùng 2.313 → 3.914.
- Ngoài phạm vi bảng: bảng dừng ở 1970. Không có số sau 1970 từ nguồn này. Muốn nối 1980–2000 phải tìm nguồn toàn văn cùng loại (Census/BLS) và đánh dấu ngắt chuỗi; tôi **chưa** làm trong gói này.

### 1b. Series D 182–232, nhóm lớn "Clerical and kindred workers" theo giới (nghìn người)

Tr. 139 (PDF 19) và tr. 140 (PDF 20). Cột theo thứ tự: 1900 / 1910 / 1920 / 1930 / 1940 / 1950 (phân loại 1950) / 1960 (phân loại 1960) / 1970 (16+).

| Nhóm | 1900 | 1910 | 1920 | 1930 | 1940 | 1950 | 1960 | 1970 |
|---|---|---|---|---|---|---|---|---|
| Cả hai giới (D 186) | 877 | 1.987 | 3.385 | 4.336 | 4.982 | 7.232 | 9.617 | 14.208 |
| Nữ (D 220) | 212 | 688 | 1.614 | 2.246 | 2.700 | 4.502 | 6.497 | 10.461 |
| Nam (D 203) | 665 | 1.300 | 1.771 | 2.090 | 2.282 | 2.730 | 3.120 | 3.748 |

(Tr. 139 in dòng cả hai giới 1930 là "4,386" ở độ phân giải thấp; trang 141 độ phân giải cao ghi 4.336 và khớp với 2.246 + 2.090. Dùng **4.336**.)

Lưu ý: nhóm này **rộng hơn nhiều** hàng 347 (gồm kế toán viên sổ sách, thu ngân, đưa thư, nhân viên điện thoại, nhân viên bán vé, v.v.). Chỉ dùng làm bối cảnh "văn thư hoá thành nghề của phụ nữ", không dùng thay cho hàng 347.

---

## 2. BLS — Monthly Labor Review, tháng 1/2026: "Industry and occupational employment projections overview and highlights, 2024–34"

- URL: https://fraser.stlouisfed.org/files/docs/publications/bls_mlr/bls_mlr_20260108.pdf (bản lưu đọc: 23 trang PDF; bản đọc là bản in từ trang web MLR).
- Trạng thái: **đọc toàn văn** (pdftotext). Đây là **DỰ BÁO, đợt 2024–34** (không phải thực tế, không phải đợt 2025–35).

| Số | Số liệu | Trích dẫn | Trang (PDF) |
|---|---|---|---|
| 2a | Nhóm "Office and administrative support occupations" (43-0000): việc làm 2024 **19.325,2** nghìn; dự báo 2034 **18.563,3**; thay đổi **−761,9** nghìn (**−3,9%**); hạng 22/22 nhóm | "Employment of these occupations is projected to decline or show little change over the 2024–34 decade." | Table 2, tr. 7; câu trích tr. 5 |
| 2b | "Secretaries and administrative assistants, except legal, medical, and executive" (43-6014): **1.944,0 → 1.913,2** nghìn; −30,8 nghìn; **−1,6%** | (bảng) | Table 2, tr. 7 |
| 2c | Executive secretaries (43-6011): 502,8 → 494,9; −1,6%. Legal secretaries (43-6012): 156,3 → 147,3; −5,8%. Medical secretaries (43-6013): 850,0 → 885,3; **+4,2%** | (bảng) | Table 2, tr. 7 |
| 2d | Medical transcriptionists: **−4,9%** 2024–34, "because AI technology can recognize speech and transcribe audio" | "Employment of medical transcriptionists, however, is projected to decline 4.9 percent from 2024 to 2034 because AI technology can recognize speech and transcribe audio" | tr. 5 (số %: chỉ trong câu; không có hàng trong Table 2) |
| 2e | Câu chữ về AI và việc văn phòng | "demand is expected to be limited for occupations such as billing and posting clerks; procurement clerks; … customer service representatives; and nonmedical secretaries and administrative assistants." | tr. 5 |

Lưu ý:
- Bảng 2 tựa đề "Select artificial intelligence related occupations, employment, projected 2024–34". Đơn vị nghìn việc làm (gồm làm công ăn lương và tự làm).
- **Bảng này KHÔNG có** "Word processors and typists" (43-9022) và "Data entry keyers" (43-9021). `grep` toàn văn không thấy hai chuỗi đó. Hai nghề này chỉ có trong đợt 2025–35 (xem mục "Danh sách BLS").
- Đây là đợt **2024–34**; không trộn với số đợt 2025–35.

## 3. BLS — MLR tháng 2/2025: "Incorporating AI impacts in BLS employment projections: occupational case studies"

- Tác giả bản MLR: nhóm BLS (Machovec, Rieley, Rolen; theo ghi chú ở phiên Tập 2).
- URL: https://fraser.stlouisfed.org/files/docs/publications/bls_mlr/bls_mlr_20250210.pdf (bản lưu 8 trang PDF).
- Trạng thái: **đọc toàn văn nhưng KHÔNG dùng được cho Tập 4**. Các ca nghiên cứu (đợt 2023–33) thuộc nhóm máy tính, pháp lý, tài chính–kinh doanh, kiến trúc–kỹ thuật. Bản lưu **không** nhắc "word processors", "typists", "data entry" hay "secretaries" (grep). Không lấy số nào.

---

## 4. Noy & Zhang — "Experimental Evidence on the Productivity Effects of Generative Artificial Intelligence"

- Tác giả: Shakked Noy, Whitney Zhang (MIT).
- Phiên bản đọc: **working paper, 2/3/2023, "Working Paper (not peer reviewed)"**, 15 trang PDF. Bản in trên *Science* (2023) là bản khác; **tôi không đọc bản Science**, nên mọi số dưới đây là của bản working paper.
- URL: https://economics.mit.edu/sites/default/files/inline-files/Noy_Zhang_1.pdf
- Trạng thái: **đọc phần tóm tắt, giới thiệu, kết quả năng suất và thảo luận** (trang 1–4, 12); chưa đọc toàn bộ phụ lục.

| Ý | Số liệu | Trích dẫn | Trang (PDF) |
|---|---|---|---|
| 4a. Mẫu | **444** người có bằng đại học, có kinh nghiệm; nghề: marketer, grant writer, consultant, data analyst, nhân sự, quản lý; mỗi người làm **hai** bài viết 20–30 phút (thông cáo báo chí, báo cáo ngắn, kế hoạch phân tích, email tế nhị); thử nghiệm trực tuyến, đăng ký trước; **một nửa ngẫu nhiên** dùng ChatGPT ở bài thứ hai | "we recruit 444 experienced, college-educated professionals and assign each to complete two occupation-specific, incentivized writing tasks." | tr. 3 |
| 4b. Thời gian | Nhóm dùng ChatGPT: thời gian bài sau **giảm 10 phút (37%)** so với nhóm đối chứng (trung bình **27 phút**) | "time taken on the post-treatment task drops by 10 minutes (37%) relative to the control group, who take an average of 27 minutes" | tr. 4 |
| 4c. Chất lượng | Điểm người chấm (mù) tăng **0,45 độ lệch chuẩn**; tóm tắt: thời gian giảm 0,8 SD, chất lượng tăng 0,4 SD | "time taken decreases by 0.8 SDs and output quality rises by 0.4 SDs" | tr. 1 (tóm tắt); tr. 4 |
| 4d. Bất bình đẳng | ChatGPT "compresses the productivity distribution" (lợi cho người năng suất thấp nhiều hơn) | "ChatGPT substantially compresses the productivity distribution, reducing inequality." | tr. 12 |

Lưu ý phạm vi:
- Mẫu là **chuyên gia có bằng đại học làm tác vụ viết cấp trung**, trực tuyến, **không phải** thư ký, nhân viên đánh máy hay nhập liệu. Không suy ra tác động lên nghề đánh máy.
- Tác vụ ngắn (20–30 phút), một lần can thiệp; không đo việc làm hay lương dài hạn.
- Có bản 2023 chưa qua bình duyệt; bản in *Science* có thể khác về số.
- Giữ nhãn "thực nghiệm; mẫu 444; viết cấp trung".

---

## Tổng hợp số dùng được

| Số | Loại | Năm / đợt | Nguồn (khoá) | Trang | Ghi chú |
|---|---|---|---|---|---|
| Stenographers, typists, and secretaries: 134 / 387 / 786 / 1.097 / 1.223 / 1.661 nghìn | **Thực tế** (điều tra dân số) | 1900 / 1910 / 1920 / 1930 / 1940 / 1950 | HSUS D 347, phân loại 1950 | tr. 141 (PDF 21) | cả hai giới; 1900 "approximations only"; đọc ảnh quét |
| 1.629 / 2.313 nghìn | Thực tế | 1950 / 1960 (phân loại 1960) | HSUS D 347 | tr. 141 | đoạn riêng |
| 2.316 / 3.914 nghìn (16+) hoặc 3.920 (14+) | Thực tế | 1960 / 1970 (phân loại 1970) | HSUS D 347 | tr. 141 | cặp cùng phân loại để tính mức tăng 1960–70 |
| Clerical nữ 212 → 10.461 nghìn; nam 665 → 3.748 nghìn | Thực tế | 1900 → 1970 | HSUS D 220, D 203 | tr. 139–140 | nhóm lớn, **không** phải đánh máy |
| Office & admin support: 19.325,2 → 18.563,3 nghìn (−3,9%) | **Dự báo** | đợt 2024–34 | MLR 1/2026, Table 2 | tr. 7 (PDF) | nhóm 43-0000 |
| Secretaries & admin assistants (trừ pháp lý, y tế, điều hành): 1.944,0 → 1.913,2 (−1,6%) | Dự báo | đợt 2024–34 | MLR 1/2026, Table 2 | tr. 7 (PDF) | |
| Medical transcriptionists −4,9% | Dự báo | đợt 2024–34 | MLR 1/2026 | tr. 5 (PDF) | câu chữ nêu nguyên nhân AI |
| ChatGPT: thời gian −37% (10 phút, từ 27 phút), chất lượng +0,45 SD; n = 444 | **Thực nghiệm** | 2023 (working paper) | Noy & Zhang | tr. 3–4 (PDF) | tác vụ viết cấp trung, trực tuyến |

## Số cố ý không dùng

- **Mọi so sánh một chuỗi liền 1900–1970 trên "stenographers, typists, secretaries" mà không ghi ngắt phân loại.** Ba phân loại khác nhau (1950, 1960, 1970).
- **Giá trị 2.313 (1960 theo phân loại 1960) nối với 3.914 (1970).** Dùng 2.316 cho cặp 1960–70.
- **Số nam/nữ của riêng đánh máy hay tốc ký.** Bảng HSUS không có; chỉ có nhóm Clerical. Không suy ra tỉ lệ nữ của nghề đánh máy từ nhóm Clerical (nữ 10.461 / 14.208 = 74% năm 1970 là của cả nhóm).
- **BLS 2025–35 (−34,4%, 40.400 → 26.500; −25,5%, 131.800 → 98.200):** chưa xác minh bằng nguồn đọc được (xem danh sách bên dưới). Không dùng cho tới khi có xác nhận.
- **Số đợt 2024–34 ghép với đợt 2025–35.** Hai đợt khác năm gốc và khác phương pháp.
- **Số MLR 2/2025:** bản đọc không có nghề đánh máy/nhập liệu.
- **Số sau 1970:** chưa có nguồn toàn văn cùng loại trong gói này.
- **Mốc IBM MT/ST (1964)** và mốc máy đánh máy/xử lý văn bản: **không tìm** trong gói này (hết lượt tra); không dùng.
- **Số "AI thay thế X% nhân viên văn phòng" từ báo chí hay trang tổng hợp**: loại theo luật nguồn.

## Danh sách BLS cần Claude (Cowork) xác minh

`bls.gov` trả 403 với curl. Các số dưới đây **CHỜ XÁC MINH** (chưa đọc được văn bản gốc).

| Bảng / trang | Mục | URL | Số cần xác nhận |
|---|---|---|---|
| Employment Projections, Table 1.5 "Fastest declining occupations, 2025–35" | Word processors and typists (SOC 43-9022) | https://www.bls.gov/emp/tables/fastest-declining-occupations.htm | −34,4%; 40.400 → 26.500 (nghìn việc làm: kiểm lại đơn vị; số này có vẻ là số người, không phải nghìn: xác nhận cột "Employment, 2025" và "Employment, 2035") |
| Cùng Table 1.5 | Data entry keyers (SOC 43-9021) | https://www.bls.gov/emp/tables/fastest-declining-occupations.htm | −25,5%; 131.800 → 98.200; cũng xác nhận có nằm trong top giảm nhanh nhất không |
| OOH trang nghề | Word processors and typists | https://www.bls.gov/ooh/office-and-administrative-support/word-processors-and-typists.htm | số việc làm 2025, dự báo 2025–35, mô tả "Job Outlook", câu chữ về AI (nếu có) |
| OOH trang nghề | Data entry keyers | https://www.bls.gov/ooh/office-and-administrative-support/data-entry-keyers.htm | như trên |
| OOH trang nghề | Secretaries and administrative assistants | https://www.bls.gov/ooh/office-and-administrative-support/secretaries-and-administrative-assistants.htm | số 2025, % thay đổi 2025–35, chữ về AI |
| Employment Projections, Table 1.2 (nghề, 2025–35) | Word processors and typists; Data entry keyers; Secretaries and administrative assistants | https://www.bls.gov/emp/tables/emp-by-detailed-occupation.htm | hàng SOC tương ứng; đối chiếu với hai bảng trên |
| Occupational Employment and Wage Statistics (nếu cần "thực tế" gần nhất) | SOC 43-9022, 43-9021 | https://www.bls.gov/oes/ | số việc làm điều tra gần nhất (**thực tế**, khác dự báo); cần để làm cột "hôm nay" |

Ghi chú: các URL BLS ở trên là **địa chỉ tôi suy ra theo cấu trúc trang BLS**, **chưa mở được**; cần kiểm đúng đường dẫn khi xác minh.
Số trong ngoặc ở hàng đầu (−34,4%; 40.400 → 26.500) là số do chủ dự án giao, **chưa được đối chiếu**.

## Rủi ro so sánh (cho kịch bản)

1. **Định nghĩa khác nhau.** HSUS "Stenographers, typists, and secretaries" gộp ba nghề (kể cả thư ký, tức quản trị văn phòng) trong phân loại điều tra dân số của từng đợt. BLS "word processors and typists" là **một mã SOC hẹp** (chỉ gõ văn bản/xử lý văn bản), tách riêng khỏi "secretaries and administrative assistants" và "data entry keyers". Nên **không đặt 3.914 nghìn (1970) cạnh 26.500 hay 40.400 (BLS)** như cùng một nghề.
2. **Khác loại số.** HSUS là điều tra dân số mười năm một lần (số người "economically active", 14+/16+); BLS là ước tính việc làm theo nghề (dự báo, gồm làm công ăn lương và tự làm).
3. **Khác phân loại giữa đợt.** Đoạn 1900–1950, 1950–60 và 1960–70 dùng ba phân loại; mức tăng 1960–70 chỉ so cùng phân loại 1970 (2.316 → 3.914).
4. **Thang 10 năm.** HSUS cho điểm mỗi 10 năm (1900…1970), so sánh được theo thang 10 năm nhưng **chỉ trong từng đoạn phân loại**, và 1900–1930 có chú thích tuổi 10+ và "approximations only". Số BLS là một đợt dự báo 10 năm (2024–34 hoặc 2025–35) và **không nối được** với HSUS (khoảng trống 1970–2024, đổi phân loại). Nên kể hai đoạn **riêng**, không vẽ một đường liền; nếu cần minh hoạ sau 1970 phải có nguồn Census/BLS toàn văn cùng loại.
5. **Dự báo không phải thực tế.** Mọi số BLS là dự báo; chỉ số "hôm nay" thực tế cần OEWS (CHỜ XÁC MINH).
6. **Noy & Zhang** không đo việc làm; không dùng để nói "AI làm mất việc đánh máy".

## Việc đang chờ chủ dự án / phiên P

- Duyệt gói nguồn Tập 4; quyết định có chấp nhận chuỗi HSUS theo từng đoạn phân loại (không một đường liền).
- Giao Claude (Cowork) xác minh bảng BLS ở trên; cho đến lúc đó không đưa số 2025–35 vào kịch bản.
- Một người đối chiếu bằng mắt hàng 347 trên PDF HSUS (tr. 141) trước khi khoá.
- Quyết định có tra tiếp mốc IBM MT/ST 1964 và nguồn Census/BLS sau 1970 hay không.

## PHỤ LỤC 1970–2000

**Kết quả: KHÔNG TÌM ĐƯỢC** số toàn văn cho typists/secretaries/stenographers/word processors/data entry keyers ở Mỹ giai đoạn 1970–2000. Không có số nào được ghi vào đây.

Đã thử (5/5 lượt tải, đã hết hạn mức của gói):
1. FRASER API tìm kiếm (`/api/search`): HTTP 401, cần khoá API.
2. `.../bls_mlr/bls_mlr_19830101.pdf`: 404.
3. Trang tiêu đề MLR `fraser.stlouisfed.org/title/monthly-labor-review-82`: HTTP 200 (3,4 MB) nhưng danh sách số báo nạp động, không có liên kết PDF theo năm trong HTML tĩnh.
4. `.../mlr/mlr_198307.pdf`: 404.
5. `.../bls_mlr/bls_mlr_19830701.pdf`: 404.

Kết luận: quy ước tên tệp các số MLR thập niên 1980–90 trên FRASER chưa xác định được; các số gần đây dùng `bls_mlr_YYYYMMDD.pdf` nhưng các ngày đoán cho 1983 không tồn tại. Không có câu trích về máy xử lý văn bản thay đánh máy.

Việc còn lại (chờ chủ dự án duyệt hạn mức mới): cấp thêm lượt tải, hoặc cung cấp URL cụ thể một số MLR/Census 1980–2000 (ví dụ bài về clerical employment và office automation), hoặc khoá API FRASER. Chuỗi HSUS đến 1970 (mục 1) vẫn là nguồn Census duy nhất đã có.

## PHỤ LỤC G1-B (bổ sung thời lượng)

Nguồn: FRASER, BLS. Tải 4 URL (4/6 lượt). Số đều ghi theo bản in và trang PDF.

**Tình trạng URL.** (1) bls_1276_1960: tải được, có lớp chữ. (2) bls_1241_1958: tải được (tiêu đề thật là "Automation and Employment Opportunities for Office Workers", 24 trang), lớp chữ OCR rất kém, chưa trích được số đáng tin. (3) bls_1875_1976 (OOH 1976–77): **404**, không thử URL khác. (4) bls_2350_1990: tải được (506 trang), có lớp chữ.

**G1-B-1. Bulletin 1276 (1960), thực tế (khảo sát 20 văn phòng đã lắp máy tính điện tử cỡ lớn; không có năm khảo sát rõ trong đoạn trích).**
- Khoảng 2.800 nhân viên trong các đơn vị bị ảnh hưởng trực tiếp; sau 1 năm, việc làm ở đơn vị đó giảm khoảng 25%; chỉ 9 người bị sa thải.
- Chỉ hơn 4% làm việc thư tín, tốc ký, thư ký.
- Trang in 3, trang PDF 13. Trích: "Only a little over 4 percent were engaged in the less routine clerical jobs such as correspondence, stenographic, and secretarial work." (OCR: số "4" bị nhiễu thành "h", đã đối chiếu với ngữ cảnh "a little over 80 percent" của đoạn trước; cần kiểm bằng mắt trên ảnh trang trước khi dùng cuối.)
- Thiếu hụt thị trường lao động lúc lắp máy: chủ yếu thợ đánh máy có kinh nghiệm, tốc ký, thợ máy tính bảng (lập bảng). Nằm quanh dòng 620 của văn bản trích; chưa xác định trang PDF/in.

**G1-B-2. OOH 1990–91 (Bulletin 2350), việc làm năm gốc 1988 (thực tế); dự báo đến 2000 (đợt dự báo 1988–2000).**
- Typists, word processors, and data entry keyers: 1.416.000 việc làm năm 1988. Trang in 283, trang PDF 294. Trích: "Typists, word processors, and data entry keyers held 1,416,000 jobs in 1988 and were employed in every sector of the economy."
- Dự báo: giảm đến 2000. Trang in 283, PDF 294. Trích: "Employment ... is expected to decline through the year 2000 despite the 'information explosion' ... significant productivity improvements ... due to the widespread use of automated office equipment."
- Máy tính cá nhân làm thay việc đánh máy. Trang in 284, PDF 295. Trích: "With the proliferation of personal computers throughout the economy, more and more workers are performing work formerly done by typists, word processors, and data entry keyers."
- Secretaries: 3.373.000 việc làm năm 1988. Trang in 277, PDF 288. Trích: "Secretaries held 3,373,000 jobs in 1988, making this one of the largest occupations in the U.S. economy." Dự báo cùng trang: tăng "about as fast as the average" đến 2000.
- Số in trang suy ra từ đầu trang 295 (in "284"); chưa kiểm số in của PDF 288 trực tiếp (suy từ độ lệch 11).
- Định nghĩa nghề: chưa trích mục "Nature of the work"; chỉ dùng được số như tổng nhóm OOH.

**Còn thiếu cho G1-B:** mốc 1976 (404) và số liệu 1950–75; số 1958 (Bulletin 1241) cần OCR lại hoặc đọc ảnh. Chờ chủ dự án duyệt thêm lượt hoặc URL.
