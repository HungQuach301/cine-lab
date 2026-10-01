# KHUNG SERIES — kênh "Last Lamplighters"

*Every era has its last lamplighters.*

Gói việc: KHUNG SERIES (P giao theo chỉ thị chủ dự án 01/10/2026) · Người viết: phiên biên tập nội dung · Ngày tra nguồn: **01/10/2026** · Trạng thái: **nháp 1, chờ chủ dự án duyệt**. Chỉ có văn bản: không sửa mã, không đọc `checks/`, không commit.


> **Ghi chú chủ dự án (01/10/2026):** các số BLS — bảng "Fastest declining occupations" 2025–35 (Table 1.5), bài MLR 2025 về AI trong dự báo, và bản tin Employment Projections (ecopro, 27/08/2026) — đã được **Claude (rà độc lập bên ngoài) đọc toàn văn ngày 01/10/2026**. Trạng thái nguồn: **"đã đọc toàn văn (Claude)"**. Không cần tải bản gốc vào repo.

---

## 0. Tóm tắt cho chủ dự án

- **Định vị.** Mỗi tập 8–12 phút đặt một nghề xưa (truyện hoạt hình 2.5D cách điệu quanh Ida và Cas) cạnh một nghề hôm nay dưới AI (số liệu thật). Người thắp đèn là nhận diện xuyên suốt: mỗi tập Ida "thắp" một ngọn đèn cho nghề mới, như một nghi thức mở và đóng tập.
- **Sáu tập**, mỗi tập 2–3 số neo, tất cả có nguồn ghi ở mục 3. Có 13 trên 17 nguồn đã đọc trực tiếp văn bản gốc hoặc toàn văn bài thứ cấp. Bốn nguồn còn lại là nguồn thứ cấp, tài liệu nội bộ, hoặc chỉ kiểm được qua tóm tắt.
- **Hạn chế lớn nhất.** `bls.gov` chặn mọi lối (curl có User-Agent trả 403; WebFetch báo "EGRESS_BLOCKED"). Vì vậy:
  - Số BLS chu kỳ **2025–35** (đã công bố 27/08/2026) chỉ kiểm được qua **bài USA TODAY ngày 01/09/2026** (đọc toàn văn). Bài đó trích BLS nhưng không phải bảng gốc.
  - Số BLS về AI lấy từ bài **MLR 02/2025** (đọc toàn văn bản PDF lưu ở FRASER của Fed St. Louis). Bài này thuộc chu kỳ **2023–33**, cũ hơn chu kỳ hiện hành hai vòng.
  - ~~Trước khi khoá lời dẫn của tập có số BLS, cần một phiên vào được bls.gov để đối chiếu bảng gốc.~~ **Đã xong:** Claude (rà độc lập bên ngoài) đọc toàn văn bảng 2025–35, MLR 2025 và bản tin ecopro ngày 01/10/2026. Riêng BLS OOH "Graphic Designers" [S16] vẫn chỉ qua tóm tắt.
- **Đang chờ chủ dự án:**
  - (a) duyệt 6 tiêu đề và thứ tự tập;
  - (b) duyệt quy ước "Ida thắp một ngọn đèn cho mỗi nghề", ghi vào `AUTHORSHIP.md`;
  - (c) chọn nhịp ra tập (mục 4.1);
  - (d) giao phiên tra nhãn hiệu USPTO cho tên kênh;
  - (e) quyết định có cần phiên mở được bls.gov để kiểm bảng gốc hay không.

---

## 1. Bảng tổng

| # | Tiêu đề (EN) | Nghề xưa → nghề nay | Số neo chính | Độ chắc |
|---|---|---|---|---|
| 1 | **The Last Lamplighters** (tập thử) | Người thắp đèn / người lái thang máy → tự động hoá trọn một nghề | 1 trong 270 nghề · 15 000 người đình công năm 1945 · khoảng 1 500 đèn khí ở London | Cao / cao / trung bình |
| 2 | **Hello, Central** | Cô gái tổng đài → chăm sóc khách hàng bằng AI | 342 000 → 1 460 · hơn một nửa mạng AT&T tự động hoá trong 1920–40 · CSR −5,0% | Cao / cao / cao (chu kỳ cũ) |
| 3 | **The Typing Pool** | Phòng đánh máy → nhập liệu và AI viết | 811 000 (1930) · 40 400 → 26 500 · 57/43 | Trung bình / trung bình / cao |
| 4 | **The Hand That Drew It** | Thợ sắp chữ, hoạ sĩ minh hoạ → thiết kế đồ hoạ thời AI tạo sinh | Ít thợ sắp chữ hơn, nhiều nhà thiết kế hơn · 86 300 → 9 200 · WEF: lần đầu xếp vào nhóm giảm | Cao / cao / cao |
| 5 | **The Apprentice's Lamp** | Thợ học việc → người trẻ 22–25 tuổi trong nghề phơi nhiễm AI | 19% · 39% · 36% và 4% | Cao (chỉ báo sớm) / cao / cao |
| 6 | **The Assessor's Eye** | Giám định viên → AI ước thiệt hại qua ảnh | −4,4% · −9,2% · WEF xếp vào nhóm giảm | Cao (chu kỳ cũ) / cao / cao |

Thứ tự đề xuất: 1 → 2 → 3 → 6 → 4 → 5. Ba tập đầu kể các nghề văn phòng có lịch sử dài và số rõ. Tập 6 là nghề hẹp, ít gây lo âu. Tập 4 (nghề sáng tạo) và tập 5 (người trẻ) nhạy cảm nhất nên để cuối, khi kênh đã có giọng điệu ổn định và có phản hồi khán giả.

---

## 2. Sáu tập

Quy ước: [Sn] trỏ tới danh mục nguồn ở mục 6. **"Đọc toàn văn"** nghĩa là đã tải và đọc văn bản chứa con số. **"Qua tóm tắt"** nghĩa là chỉ thấy con số trong bản tóm tắt của công cụ tìm kiếm. Luật hình chung: không cận mặt người; nhân vật xuất hiện dưới dạng bóng, hoặc ở cỡ trung đến xa.

### Tập 1 — "The Last Lamplighters" (tập thử)

**Logline.** *On the last night the gas lamps burn, an old lamplighter teaches a boy her round — while history asks how many jobs automation has ever truly erased. The answer is smaller, and stranger, than you think.*

**Nghề xưa → nghề nay.** Người thắp đèn khí (London, Paris, New York) và người lái thang máy, nghề duy nhất trong 270 nghề bị tự động hoá xoá hẳn. Câu hỏi kết hướng sang nghề hôm nay.

**Số neo**
| # | Số | Nguồn | Cách kiểm |
|---|---|---|---|
| 1.1 | Trong khoảng **270** nghề chi tiết của điều tra dân số Mỹ năm 1950, chỉ **1** nghề bị loại bỏ nhờ tự động hoá: người lái thang máy. | Bessen, cột VoxEU đăng lại ở RIETI [S4] | Đọc toàn văn. Bản báo chí ghi 271 (cần kiểm toàn văn bài 2016). Lời dẫn nên nói "about 270". |
| 1.2 | Tháng 9/1945, **15 000** công nhân toà nhà ở New York đình công, trong đó có người lái thang máy. Theo NPR, cuộc đình công khiến **1,5 triệu** nhân viên văn phòng không tới được chỗ làm. | NPR [S13]; Wikipedia "Elevator Strikes" [S15] | Đọc toàn văn cả hai. Lưu ý: 15 000 gồm cả gác cửa và bảo vệ, không chỉ người lái thang. Con số 1,5 triệu là lời của nguồn trong bài NPR. |
| 1.3 | London hiện còn khoảng **1 500** đèn khí đường phố (số "as of 2018"). | Wikipedia "Gas lighting" [S14]; kịch bản v1 [S17] | Đọc toàn văn mục Wikipedia. Kịch bản v1 ghi số năm 2015 qua tóm tắt. Độ chắc: trung bình. Đội "5 người thắp đèn" **cần kiểm**. |

**Cảnh truyện.** Phố Ostler lúc chạng vạng, Ida đi vòng thắp đèn; "làn sóng trắng" của đèn điện; Ida trao đèn lồng cho Cas. Thêm một cảnh nối mới: cửa xếp của một buồng thang máy cổ trong toà nhà cuối phố. Bàn tay đeo găng gạt cần ở cỡ trung, sau đó chính cái cần ấy bị thay bằng một hàng nút bấm.

**Tài sản.**
- *Dùng lại:* phố, Ida, Cas, thang, sào, đèn khí, đèn điện, đồng hồ bỏ túi.
- *Mới:* buồng thang máy có cửa xếp và cần gạt; lưới 270 biểu tượng nghề (đã nêu trong kịch bản v1).

**Shorts.**
1. **"One job in 270"**: lưới 270 ô, chỉ một ô tắt. Đã có trong kịch bản v1, đoạn 11.
2. **"The week New York took the stairs"**: năm 1945, 15 000 người đình công và 1,5 triệu người không tới được chỗ làm. Ý kết: chính cuộc đình công làm thang tự động được đón nhận nhanh hơn. Ý kết này mới có ở mức tóm tắt tìm kiếm, NPR chỉ nói chủ toà nhà đòi thay đổi, nên viết thận trọng.

**Rủi ro.**
- *Nhạy cảm:* thấp. Nghề đã qua lâu, và tập có kết cấu an ủi.
- *YouTube:* ảnh tư liệu về cuộc đình công năm 1945 có bản quyền chưa rõ. Đề xuất vẽ lại thay vì dùng ảnh.
- *Độ chắc của số:* 270 hay 271 nghề; số đèn ở London thay đổi theo năm. Lời dẫn đã dùng cách nói "last time anyone counted publicly".

### Tập 2 — "Hello, Central"

**Logline.** *A switchboard of a hundred blinking jacks, one woman's voice behind each one — then the dial arrived. A century later, the voice that answers is a machine again, and the question is the same: who is left on the line?*

**Nghề xưa → nghề nay.** Nhân viên tổng đài điện thoại (1878–1984) → nhân viên chăm sóc khách hàng (customer service representative) làm việc cùng chatbot và voicebot AI.

**Số neo**
| # | Số | Nguồn | Cách kiểm |
|---|---|---|---|
| 2.1 | Số nhân viên tổng đài: khoảng **178 000** (1920) → khoảng **342 000** (giữa thế kỷ) → dưới **250 000** (1960) → **40 000** (1984) → **1 460** trong ngành viễn thông (số BLS mà bài trích, 2019). | Richmond Fed, *Econ Focus* Q4/2019, "Goodbye, Operator" [S6] | Đọc toàn văn |
| 2.2 | Trong 1920–1940, AT&T thay nhân viên bằng tổng đài cơ khí ở **hơn một nửa** mạng điện thoại Mỹ. Tự động hoá xoá phần lớn các chỗ làm này, nhưng **không làm giảm** việc làm chung của các lớp phụ nữ trẻ đi sau, vì việc văn phòng và dịch vụ tăng lên. Ngược lại, chính những người đang làm tổng đài thì chịu thiệt: mười năm sau, họ dễ rơi vào việc lương thấp hơn hoặc rời lực lượng lao động. | Feigenbaum & Gross, NBER w28061 [S7] | Đọc toàn văn **trang tóm tắt** của bài; bài đầy đủ chưa đọc |
| 2.3 | BLS dự báo việc làm của nhân viên chăm sóc khách hàng giảm **5,0%** trong 2023–33. BLS xếp nghề này vào nhóm chịu tác động chính của AI tạo sinh. | BLS MLR 02/2025 [S2] | Đọc toàn văn (PDF FRASER). Chu kỳ cũ: phải nói "BLS projected in 2025…". |

*Bổ sung, chưa dùng làm neo:*
- Theo BLS 2025–35 qua USA TODAY [S1]: nhân viên trực tổng đài (switchboard operators) giảm 26,0% (35 400 → 26 200); nhân viên tổng đài điện thoại (telephone operators) giảm 27,6% (3 500 → 2 500); nhân viên chăm sóc khách hàng mất khoảng 141 800 chỗ làm. Cần kiểm bảng gốc.
- Ý "1 trong 13 phụ nữ đi làm năm 1950 là nhân viên tổng đài" có ở [S8] nhưng không thấy trong [S6]. **Cần kiểm.**

**Cảnh truyện.** Một tổng đài trong toà nhà cuối phố Ostler. Hàng bóng người ngồi quay lưng, đội tai nghe, cỡ xa. Các giắc cắm sáng hổ phách như những ngọn đèn. Ida đi ngang cửa sổ và gật đầu với ánh sáng bên trong. Cảnh chuyển: các giắc tắt dần, thay bằng một bảng điện tử (năm 1965, tổng đài điện tử đầu tiên ở Succasunna [S6]), rồi thành một dải sóng âm trên màn hình điện thoại. Cas nhấc ống nghe; giọng trả lời là một giọng tổng hợp, được dán nhãn rõ trên hình.

**Tài sản.**
- *Dùng lại:* phố, Ida, Cas, đồng hồ bỏ túi.
- *Mới:* bàn tổng đài có giắc và dây, tai nghe kiểu cổ, bóng người ngồi, máy quay số, giao diện chat cách điệu.

**Shorts.**
1. **"342,000 to 1,460"**: một cột đèn giắc tắt dần theo năm, dưới chân khung là con số chạy.
2. **"Automation hurt the operators — not their daughters"**: tóm ý bài NBER trong 50 giây: người đang làm nghề thì chịu thiệt, còn thế hệ sau thì không.

**Rủi ro.**
- *Nhạy cảm:* trung bình. Nghề chăm sóc khách hàng đang có nhiều người làm. Tránh câu kiểu "your job is next". Nêu đủ hai mặt theo [S7].
- *Người thật:* không nêu tên người lao động cụ thể. Emma Nutt, nhân viên tổng đài nữ đầu tiên năm 1878, chỉ có nguồn qua tóm tắt, nên **cần kiểm** trước khi nhắc.
- *YouTube:* giọng AI trả lời trong cảnh truyện là nội dung tổng hợp. Nếu nghe giống người thật, cần cân nhắc nhãn công bố.
- *Độ chắc:* số 1 460 là của năm 2019. Đừng nói "today".

### Tập 3 — "The Typing Pool"

**Logline.** *Rows of desks, a thousand keys striking at once — the typewriter built an army of women clerks almost overnight. Now the keyboard itself may be fading, and the pool is draining again.*

**Nghề xưa → nghề nay.** Phòng đánh máy, tốc ký và sao chép văn bản (1880–1980) → người nhập liệu và người viết văn bản thường ngày làm việc cùng AI viết.

**Số neo**
| # | Số | Nguồn | Cách kiểm |
|---|---|---|---|
| 3.1 | Số người làm tốc ký và đánh máy ở Mỹ: **112 000** (1900) → **811 000** (1930). Tỉ lệ nữ tăng từ 77% lên **96%**. | Early Office Museum, bảng dẫn Kwolek-Folland (1994) [S9]; Davies, *Woman's Place Is at the Typewriter*, chương 4 [S10] | Đọc toàn văn cả hai. [S9] là nguồn thứ cấp dẫn sách. [S10] xác nhận ý "trên 95% năm 1930". Độ chắc: trung bình đến cao. |
| 3.2 | BLS 2025–35: nghề xử lý văn bản và đánh máy (word processors and typists) giảm **34,4%** (40 400 → 26 500) và đứng đầu danh sách các nghề giảm nhanh nhất. Nghề nhập liệu (data entry keyers) giảm 25,5% (131 800 → 98 200). | USA TODAY 01/09/2026 trích BLS [S1] | Đọc toàn văn bài báo. **Bảng BLS gốc chưa đọc** (403). Bài báo vừa ghi 34,3% vừa ghi 34,4%. |
| ~~3.3~~ | Trong dữ liệu Claude đầu năm 2025: **57%** tác vụ là tăng cường (AI làm cùng người) và **43%** là tự động hoá (AI làm thay). | Anthropic Economic Index, 10/02/2025 [S12] | Đọc toàn văn. Dữ liệu của chính Anthropic (xem rủi ro). — **BỎ (chủ dự án 01/10/2026: không trích Anthropic Economic Index, tránh xung đột lợi ích); thay bằng số liệu nguồn độc lập khi viết tập** |

**Cảnh truyện.** Một phòng đánh máy nhìn từ ban công: các hàng bàn, bóng lưng người ngồi, ánh đèn bàn ấm. Âm thanh chủ đạo là tiếng gõ và tiếng chuông xuống dòng. Ida mang thư tới cửa, chỉ thấy bóng. Sau đó căn phòng trống dần: từng ngọn đèn bàn tắt, còn lại một màn hình con trỏ nhấp nháy, nơi chữ tự hiện ra. Cas gõ một chữ duy nhất bằng tay.

**Tài sản.**
- *Dùng lại:* phố, Ida, Cas, đèn điện.
- *Mới:* máy đánh máy cách điệu, hàng bàn, đèn bàn, thẻ đục lỗ hoặc phiếu nhập liệu, màn hình con trỏ.

**Shorts.**
1. **"811,000 typists"**: căn phòng lấp đầy bàn theo năm 1870 → 1930, rồi trống dần tới 2035 (dự báo).
2. **"Augment or automate?"**: hai bàn tay, một cái gõ cùng AI và một cái rời bàn phím, với chữ 57/43. Phải ghi rõ đây là số đo trên một sản phẩm (Claude), không phải toàn nền kinh tế.

**Rủi ro.**
- *Nhạy cảm:* trung bình. Nhập liệu là nghề lương thấp, có nhiều người lớn tuổi. Không châm biếm.
- *Xung đột lợi ích:* phim làm bằng Claude và trích số của Anthropic. Lời dẫn phải nói "Anthropic, the company behind the AI model used to make this film" để minh bạch, và nên cân bằng bằng một nguồn độc lập.
- *Độ chắc:* số 811 000 gộp tốc ký với đánh máy, nên không được nói "811,000 typists" trơn. Tiêu đề Short 1 phải đổi thành "811,000 stenographers and typists" hoặc dùng chữ "clerks". Số BLS 2025–35 đã đọc toàn văn (Claude, 01/10/2026); trước đây cần kiểm bảng gốc.

### Tập 4 — "The Hand That Drew It"

**Logline.** *When the printing press went digital, the typesetter vanished — and the graphic designer was born. Now a machine can draw too. What happens to the hand that drew it?*

**Nghề xưa → nghề nay.** Thợ sắp chữ, hoạ sĩ minh hoạ báo in và thợ ảnh buồng tối → nhà thiết kế đồ hoạ thời AI tạo sinh.

**Số neo**
| # | Số / dữ kiện | Nguồn | Cách kiểm |
|---|---|---|---|
| 4.1 | Máy tính làm số thợ sắp chữ giảm nhưng số nhà thiết kế đồ hoạ và người dàn trang tăng. Theo Bessen, máy tính tạo ra gần bằng số việc mà nó thay thế. | Bessen, BU Working Paper 15-49 (2015) [S5]; cột RIETI [S4] | Đọc toàn văn cả hai. Đây là dữ kiện định tính, không phải số. |
| 4.2 | Thợ ảnh và thợ vận hành máy tráng rửa: đỉnh **86 300** người (2004) → 28 800 (2014) → **9 200** (2023). Đây là trường hợp BLS dự báo trúng sự sụp đổ khi máy ảnh số thay phim. | BLS MLR 02/2025 [S2] | Đọc toàn văn |
| 4.3 | WEF *Future of Jobs 2025*: nhà thiết kế đồ hoạ lần đầu nằm sát ngoài top 10 vai trò giảm nhanh nhất (2025–2030), do cả AI lẫn công nghệ thông tin. | WEF [S11] | Đọc trực tiếp bản PDF gốc, phần liên quan. Đây là khảo sát nhà tuyển dụng toàn cầu, không phải số đếm. |

*Bổ sung, chưa dùng làm neo:* BLS OOH 2025–35 dự báo việc làm của nhà thiết kế đồ hoạ giảm 2% (253 100 → 248 800), vẫn có khoảng 16 000 vị trí trống mỗi năm (**qua tóm tắt**) [S16].

**Cảnh truyện.** Xưởng in dưới tầng hầm phố Ostler. Khay chữ chì và bàn tay đeo tao xếp chữ, cận vào tay chứ không vào mặt. Một bảng vẽ có ngọn đèn kẹp. Ida dừng lại xem một tấm áp phích đang khô. Chuyển cảnh: khay chữ thành màn hình dàn trang, rồi thành một ô nhắc lệnh sinh ra hàng trăm áp phích cùng lúc. Cas chọn một tấm và sửa nó bằng bút chì: con người làm biên tập và quyết định.

**Tài sản.**
- *Dùng lại:* phố, Ida, Cas, đèn khí.
- *Mới:* khay chữ chì, tao xếp chữ, bảng vẽ, áp phích. Áp phích phải do dự án tự thiết kế; không mô phỏng tác phẩm hay phong cách của hoạ sĩ đang sống.

**Shorts.**
1. **"From darkroom to zero"**: 86 300 → 9 200; tấm phim ảnh mờ dần.
2. **"The typesetter's grandchild"**: thợ sắp chữ biến mất, nhà thiết kế đồ hoạ xuất hiện. Câu hỏi mở: AI sẽ sinh ra nghề gì mới?

**Rủi ro.**
- *Nhạy cảm:* **cao.** Cộng đồng sáng tạo đang tranh cãi gay gắt về AI tạo sinh và dữ liệu huấn luyện. Bản thân phim cũng làm bằng AI, nên dễ bị xem là đạo đức giả. Cần một đoạn minh bạch: kênh dùng AI ở khâu nào, con người quyết định gì (dẫn tới `AUTHORSHIP.md`).
- *YouTube và bản quyền:* không dùng hình ảnh do AI sinh theo phong cách hoạ sĩ có tên, không đưa áp phích có thật vào hình.
- *Độ chắc:* số OOH −2% chỉ có qua tóm tắt. Các nguồn đo những thứ khác nhau (Bessen đo thực tế quá khứ, WEF là kỳ vọng của nhà tuyển dụng, BLS là dự báo), nên lời dẫn phải gọi đúng loại của từng số.

### Tập 5 — "The Apprentice's Lamp"

**Logline.** *Every lamplighter once carried someone else's ladder. Today the youngest workers in AI-exposed jobs are the first to feel the change — not because they were fired, but because the door to the first rung opened less often.*

**Nghề xưa → nghề nay.** Thợ học việc (người học nghề bằng cách theo thầy) → người 22–25 tuổi trong các nghề phơi nhiễm AI (lập trình, chăm sóc khách hàng…).

**Số neo**
| # | Số | Nguồn | Cách kiểm |
|---|---|---|---|
| 5.1 | Việc làm của lao động **22–25 tuổi** trong các nghề phơi nhiễm AI thấp hơn **19%** so với mức lẽ ra đạt được nếu tăng theo nhóm ít phơi nhiễm. Lao động nhiều kinh nghiệm không có khoảng chênh tương tự. Nguyên nhân chủ yếu là tuyển ít người trẻ hơn, không phải sa thải nhiều hơn. Các tác giả nói rõ đây là **chỉ báo sớm, mang tính mô tả, không phải ước lượng nhân quả**, và họ **không thấy bằng chứng về thay thế việc làm trên diện rộng toàn nền kinh tế**. | Brynjolfsson, Chandar, Chen, "Canaries in the Coal Mine?", bản sửa 12/08/2026, dữ liệu ADP tới 06/2026 [S3] | Đọc toàn văn **trang công bố** (tóm tắt của tác giả). PDF chưa đọc. |
| 5.2 | Người lao động được dự kiến thấy khoảng **39%** kỹ năng hiện có thay đổi hoặc lỗi thời trong 2025–2030. | WEF *Future of Jobs 2025* [S11] | Đọc trực tiếp bản PDF gốc, phần liên quan |
| ~~5.3~~ | Khoảng **36%** nghề có dùng AI cho ít nhất 1/4 số tác vụ; chỉ khoảng **4%** dùng AI cho ít nhất 3/4 số tác vụ. | Anthropic Economic Index [S12] | Đọc toàn văn. Số đầu năm 2025, đo trên Claude. — **BỎ (chủ dự án 01/10/2026: không trích Anthropic Economic Index, tránh xung đột lợi ích); thay bằng số liệu nguồn độc lập khi viết tập** |

**Cảnh truyện.** Nối thẳng từ tập thử. Cas vác thang theo Ida, học cách mở nắp đèn, học nghe tiếng khí, học chỉnh đồng hồ. Đây là kiểu học nghề bằng cách làm việc nhỏ trước. Chuyển cảnh: những việc nhỏ ấy, như vác thang hay mở nắp, nay có máy làm, nên Cas phải tìm bậc thang đầu tiên khác. Kết: Ida đưa sào cho Cas thắp ngọn đèn khó nhất. Ý của cảnh: việc học thì vẫn còn, nhưng bậc đầu đã đổi chỗ.

**Tài sản.**
- *Dùng lại:* toàn bộ bộ tài sản Last Round (thang, sào, đèn khí, đồng hồ, Ida, Cas).
- *Mới:* cột thang có các bậc tách rời làm ẩn dụ đồ hoạ cho biểu đồ "bậc đầu tiên".

**Shorts.**
1. **"Canaries"**: một chú chim bóng (đã có trong luật thế giới) bay qua biểu đồ 19%, kèm chữ chân khung "early indicator, not proof of cause".
2. **"The first rung"**: thang có bậc dưới cùng mờ đi; 36% và 4% hiện thành hai cỡ ánh đèn.

**Rủi ro.**
- *Nhạy cảm:* **cao nhất series.** Khán giả trẻ có thể lo âu. Không đưa lời khuyên chọn nghề hay chọn trường. Kết tập phải chỉ về nguồn dữ liệu công khai (AI Economic Indicators [S3]), không chỉ về một lối đi cá nhân.
- *YouTube:* dễ bị cắt khúc thành "AI is killing jobs for young people". Mọi bản Shorts phải giữ dòng "early, descriptive — not causal" trong khung hình. Tiêu đề không được câu view.
- *Độ chắc:* bài này đã sửa nhiều lần (08/2025, 02/2026, 08/2026) và con số thay đổi theo từng bản. Phải ghi rõ "as of the August 2026 revision". Phải kiểm lại nguồn ngay trước khi xuất bản.

### Tập 6 — "The Assessor's Eye"

**Logline.** *For a century, someone walked out into the wreckage with a clipboard to decide what a loss was worth. Now a phone photo and a model can price a dented car in seconds — but who answers when the number is wrong?*

**Nghề xưa → nghề nay.** Giám định viên bảo hiểm đi hiện trường → AI ước thiệt hại qua ảnh và drone, cùng giám định viên làm việc với AI.

**Số neo**
| # | Số | Nguồn | Cách kiểm |
|---|---|---|---|
| 6.1 | Việc làm của nhóm giám định, thẩm tra và điều tra bồi thường được dự báo giảm **4,4%** (345 200 → 330 000) trong 2023–33. | BLS MLR 02/2025 [S2] | Đọc toàn văn (PDF FRASER) |
| 6.2 | Thẩm định viên thiệt hại xe (insurance appraisers, auto damage) được dự báo giảm **9,2%** (10 500 → 9 500). BLS nêu lý do: drone chụp hiện trường mà không cần cử người, và AI có thể tự lập ước tính chi trả ban đầu. | BLS MLR 02/2025 [S2] | Đọc toàn văn |
| 6.3 | Trong khảo sát nhà tuyển dụng toàn cầu, nhóm giám định bồi thường (Claims Adjusters, Examiners, and Investigators) nằm trong nhóm vai trò dự kiến giảm (2025–2030). | WEF [S11] | Đọc trực tiếp bản PDF gốc. Chỉ đọc được tên trong biểu đồ, không thấy thứ hạng. |

**Cảnh truyện.** Sau một đêm bão ở phố Ostler, một cột đèn khí bị đổ. Bóng một giám định viên thời 1920, cỡ xa, đi đo bằng thước, ghi sổ và nhìn đồng hồ bỏ túi. Chuyển cảnh: một drone cách điệu lượn trên mái nhà, và các ô khung nhận dạng tự gắn giá. Ida chỉ vào chỗ máy bỏ sót: một vết nứt nằm trong bóng. Ý kết: con người vẫn giữ phần xét lại.

**Tài sản.**
- *Dùng lại:* phố, đèn khí, đồng hồ bỏ túi, Ida.
- *Mới:* cột đèn đổ, sổ và thước của giám định viên, drone cách điệu, lớp giao diện khung nhận dạng.

**Shorts.**
1. **"Priced by a photo"**: chiếc xe móp, khung nhận dạng và con số −9,2%.
2. **"The drone didn't climb the roof"**: dẫn đúng lập luận của BLS về drone và AI.

**Rủi ro.**
- *Nhạy cảm:* thấp đến trung bình. Có thể chạm tới người từng bị từ chối bồi thường. Không bàn về tranh chấp bồi thường cụ thể và không nêu tên hãng bảo hiểm.
- *Pháp lý:* không đưa lời khuyên về khiếu nại bảo hiểm.
- *Độ chắc:* số thuộc chu kỳ 2023–33 (MLR 2025, đã đọc toàn văn — Claude, 01/10/2026). Bản 2025–35 cho riêng nghề này chưa tra.

---

## 3. Tình trạng kiểm nguồn

- Tổng cộng 17 nguồn ở mục 6. **13 nguồn đã đọc trực tiếp** văn bản chứa con số. Trong đó S3 và S7 là trang tóm tắt do chính tác giả viết.
  - Cụ thể: S2, S3, S4, S5, S6, S7, S9, S10, S11, S12, S13, S14, S15.
- **4 nguồn chưa đọc toàn văn**:
  - S1: đọc toàn văn bài báo, nhưng bài báo là nguồn thứ cấp của BLS;
  - S8: blog, chỉ dùng để dẫn ý phụ;
  - S16: chỉ qua tóm tắt;
  - S17: số bên trong là số qua tóm tắt.
- **Số đã loại khỏi số neo vì chưa kiểm:**
  - "1 in 13 working women" (1950);
  - đội 5 người thắp đèn ở London;
  - Emma Nutt năm 1878;
  - mọi số BLS 2025–35 lấy trực tiếp từ bảng gốc;
  - số OOH của nhà thiết kế đồ hoạ;
  - WEF "graphic designers hạng 11" (bản PDF chỉ ghi "just outside the top 10").
- **Chỉ số trong vùng ±5% quanh ngưỡng:** không có. Báo cáo này không đo chỉ số nào có ngưỡng.

---

## 4. Phần chung

### 4.1 Nhịp ra tập và công sức

**Đề xuất A (mặc định):** cứ 2 tuần một chu kỳ, gồm 1 tập dài và 2–3 Shorts. Shorts ra rải: một bản trước tập để mồi, một bản ngày ra tập, một bản sau tập.
- Ưu: đều đặn, hợp thuật toán YouTube; Shorts dẫn người xem về tập dài.
- Nhược: đòi xưởng chạy song song.
- Rủi ro: nếu một tập trượt hạn thì cả chuỗi trượt theo.

**Đề xuất B:** sản xuất xong trước 3 tập rồi mới mở kênh, sau đó giữ nhịp A.
- Ưu: có đệm, an toàn.
- Nhược: kênh mở muộn hơn.
- Tác động: giảm áp lực cho bước kiểm nguồn, nhất là các số BLS.

Khuyến nghị **B**. Lý do: rủi ro lớn nhất hiện nay là độ chắc của số, và phần đệm cho phép kiểm bảng gốc trước khi xuất bản.

**Công sức mỗi tập** (mức khung; theo luật repo, đo bằng bước và phiên, không đo bằng ngày):

| Bước | Phiên | Ghi chú |
|---|---|---|
| Nghiên cứu và kiểm nguồn | 1 phiên | Cần mạng mở tới bls.gov |
| Kịch bản (lời dẫn khoảng 1 300–1 600 từ) cùng bảng shot | 1 phiên, sau đó P duyệt | |
| Tài sản mới | 1–2 phiên xưởng | 3–6 đạo cụ mỗi tập; tái dùng khoảng 60–70% |
| Biểu đồ và bản đồ | 1 phiên | Dùng bộ khuôn chung ở mục 4.2 |
| Giọng, nhạc, mix | 1 phiên | |
| Dựng, render 16:9 và 3 bản 9:16 | 1 phiên | |
| Kiểm định (K) | 1 phiên | |

Tổng khoảng **7–8 phiên mỗi tập**. Tập 1 gần như đã có kịch bản. Các tập 2, 3 và 6 có nhiều tài sản mới nhất (tổng đài, phòng đánh máy, drone).

### 4.2 Tài sản dùng chung

| Nhóm | Nội dung | Ghi chú quyền |
|---|---|---|
| Nhận diện | Ida thắp một ngọn đèn ở đầu mỗi tập; ngọn đèn cuối phố là "đèn của nghề hôm nay". Cas là người thừa kế. | Nhân vật của dự án, đã khoá trong `bible/`. Việc dùng lại trong khung kênh cần chủ dự án duyệt và ghi `AUTHORSHIP.md`. |
| Phố | Phố Ostler lúc chạng vạng, mỗi tập một toà nhà cuối phố: thang máy, tổng đài, phòng đánh máy, xưởng in, văn phòng bảo hiểm | Tài sản Last Round; thêm mặt tiền mới |
| Biểu đồ và bản đồ | Một bộ khuôn gồm đường theo thời gian, cột so sánh, lưới biểu tượng, bản đồ Mỹ và bản đồ thế giới; màu lấy từ hai loại ánh sáng của luật thế giới (hổ phách cho xưa, trắng cho nay); có chú thích nguồn cố định ở chân khung. Đi kèm thẻ phân loại số: **ACTUAL / PROJECTION / SURVEY**. | Dữ liệu từ nguồn công khai; tự vẽ, không chụp biểu đồ của nguồn |
| Thẻ tựa | Thẻ tựa tập, thẻ chương "STORY / DATA", thẻ nguồn cuối tập, thẻ minh bạch "How this film was made" | Font phải có giấy phép thương mại và ghi vào `RIGHTS.md` |
| Nhạc và SFX | Một chủ đề nhạc có biến tấu theo từng nghề; SFX tiếng gõ, giắc cắm, cửa thang, tiếng khí | Mỗi tệp phải có trong `RIGHTS.md` (nguồn, giấy phép, phạm vi dùng). Chỉ chấp nhận giấy phép cho phép **dùng thương mại và bán phim**. **Không dùng NC/ND, không dùng YouTube Audio Library.** Ưu tiên tự sáng tác, CC0, hoặc giấy phép mua có điều khoản phát hành phim. |

### 4.3 Nguyên tắc biên tập

1. **Cân bằng ba chiều trong mỗi tập:** nghề **mất**, nghề **đổi**, nghề **mới**. Mỗi tập có ít nhất một dữ kiện cho từng chiều (ví dụ tập 2 có [S7], tập 4 có [S5]).
2. **Không gây hoảng sợ.** Không dùng các từ "replace you", "doomed", "dying jobs" trong tiêu đề và thumbnail. Câu kết là câu hỏi mở, không phải lời phán.
3. **Không đưa lời khuyên** tài chính, pháp lý, y tế hay nghề nghiệp cho từng cá nhân. Cuối tập chỉ trỏ tới nguồn dữ liệu.
4. **Nói rõ phạm vi của mỗi số:** quốc gia (phần lớn là Mỹ; WEF là toàn cầu), loại số (thực tế, dự báo hay khảo sát), chu kỳ (ví dụ 2023–33 hay 2025–35), và năm của số. Nghiên cứu tương quan phải nói "not causal".
5. **Tách bạch hư cấu và thật.** Ida, Cas và phố Ostler là hư cấu, và lời dẫn nói rõ điều đó trong mỗi tập. Không vẽ người thật.
6. **Minh bạch về AI.** Nêu rõ phim dùng AI ở khâu nào. **Không trích Anthropic Economic Index** (chủ dự án quyết 01/10/2026, tránh xung đột lợi ích).
7. **Không trích nguyên văn dài.** Lời dẫn diễn đạt lại; tên nguồn hiện trên khung.

### 4.4 Rủi ro chung

| Rủi ro | Mức | Xử lý |
|---|---|---|
| **Tên kênh chưa tra nhãn hiệu USPTO** (cũng chưa tra sách, phim cùng tên) | Cao | Giao một phiên tra USPTO trước khi lập kênh và in thẻ tựa |
| **Chính sách YouTube về nội dung AI**: nhãn "altered or synthetic content" bắt buộc khi nội dung trông như thật. Theo hiểu biết của phiên, hoạt hình cách điệu rõ ràng không thuộc diện bắt buộc, nhưng giọng tổng hợp giống người thật thì có thể thuộc diện. Ngoài ra YPP có chính sách với nội dung sản xuất hàng loạt hoặc lặp lại ("inauthentic content"). | Trung bình | **Chưa đọc trang chính sách hiện hành ngày 01/10/2026; cần kiểm.** Đề xuất mặc định bật nhãn khi có giọng AI, và giữ mỗi tập có đóng góp biên tập rõ của con người. |
| **Thông tin sai hoặc gây hiểu lầm** | Trung bình | Thẻ ACTUAL / PROJECTION / SURVEY, chú thích nguồn ở chân khung, mô tả video có danh mục nguồn kèm URL và ngày tra |
| **Quyền dùng ảnh tư liệu** (ảnh tổng đài Bell, phòng đánh máy, đình công 1945) | Trung bình | Mặc định vẽ lại theo phong cách riêng. Nếu dùng ảnh gốc thì kiểm từng tấm (public domain hay có bản quyền) và ghi `RIGHTS.md`. |
| **Số liệu cũ đi** (BLS cập nhật mỗi năm, bài Stanford sửa nhiều lần) | Trung bình | Ghi "as of" trên khung; kiểm lại nguồn ngay trước khi xuất bản mỗi tập |
| **Không vào được bls.gov** từ môi trường này | Cao, cho các tập 2, 3 và 6 | Cần phiên có mạng mở tới bls.gov, hoặc chủ dự án tự tải bảng |
| **Phản ứng của cộng đồng sáng tạo** (tập 4) | Trung bình đến cao | Phần minh bạch AI, không bắt chước phong cách hoạ sĩ có tên |

---

## 5. Việc đang chờ chủ dự án

1. Duyệt 6 tiêu đề, logline và thứ tự tập (đề xuất: 1, 2, 3, 6, 4, 5).
2. Duyệt quy ước nhận diện "Ida thắp một ngọn đèn cho mỗi nghề", ghi vào `AUTHORSHIP.md`.
3. Chọn nhịp ra tập: A hay B (khuyến nghị B).
4. Giao phiên tra nhãn hiệu USPTO cho "Last Lamplighters".
5. Giao phiên có mạng mở tới bls.gov để đối chiếu bảng 2025–35 và bản OOH.

---

## 6. Danh mục nguồn (ngày tra: 01/10/2026)

| ID | Nguồn | URL | Cách kiểm |
|---|---|---|---|
| S1 | M. Walrath-Holdridge, "US jobs most likely to grow or shrink in the next decade. See list", USA TODAY (đăng lại trên Yahoo Finance), 01/09/2026. Trích BLS Employment Projections 2025–35. | https://finance.yahoo.com/economy/articles/us-jobs-most-likely-grow-233238983.html | Đọc toàn văn bài báo; bảng BLS gốc (https://www.bls.gov/emp/tables/fastest-declining-occupations.htm) trả **403**, chưa đọc |
| S2 | C. Machovec, M. J. Rieley et al., "Incorporating AI impacts in BLS employment projections: occupational case studies", *Monthly Labor Review*, 02/2025 | https://www.bls.gov/opub/mlr/2025/article/incorporating-ai-impacts-in-bls-employment-projections.htm (403); đã đọc bản PDF lưu ở FRASER: https://fraser.stlouisfed.org/files/docs/publications/bls_mlr/bls_mlr_20250210.pdf | Đọc toàn văn |
| S3 | E. Brynjolfsson, B. Chandar, R. Chen, "Canaries in the Coal Mine? Six Facts about the Recent Employment Effects of Artificial Intelligence", Stanford Digital Economy Lab, bản sửa 12/08/2026 | https://digitaleconomy.stanford.edu/publications/canaries-in-the-coal-mine/ | Đọc toàn văn trang công bố (tóm tắt của tác giả); PDF chưa đọc |
| S4 | J. Bessen, "How computer automation affects occupations: Technology, jobs, and skills" (cột VoxEU, đăng lại ở RIETI) | https://www.rieti.go.jp/en/special/p_a_w/076.html | Đọc toàn văn |
| S5 | J. Bessen, "How Computer Automation Affects Occupations: Technology, Jobs, and Skills", BU School of Law Working Paper 15-49, 13/11/2015 | https://www.bu.edu/law/files/2015/11/NewTech-2.pdf | Đọc toàn văn (bản 2015 không có câu về thang máy; câu đó có trong [S4]) |
| S6 | D. A. Price, "Goodbye, Operator", *Econ Focus* Q4/2019, Federal Reserve Bank of Richmond | https://www.richmondfed.org/publications/research/econ_focus/2019/q4/economic_history | Đọc toàn văn |
| S7 | J. Feigenbaum, D. P. Gross, "Answering the Call of Automation: How the Labor Market Adjusted to Mechanizing Telephone Operation", NBER w28061 (11/2020, sửa 02/2024) | https://www.nber.org/papers/w28061 | Đọc toàn văn trang tóm tắt; bài đầy đủ chưa đọc |
| S8 | T. Taylor, "Telephone Switchboard Operators: Rise and Fall", *Conversable Economist*, 14/02/2020 | https://conversableeconomist.com/2020/02/14/telephone-switchboard-operators-rise-and-fall/ | Đọc toàn văn; nguồn thứ cấp, không dùng làm neo |
| S9 | Early Office Museum, "Gender & the Office" (bảng dẫn Kwolek-Folland 1994, tr. 30) | https://www.officemuseum.com/office_gender.htm | Đọc toàn văn |
| S10 | M. W. Davies, *Woman's Place Is at the Typewriter: Office Work and Office Workers 1870–1930*, Temple University Press, chương 4 | https://temple.manifoldapp.org/read/untitled-a3dba793-4797-49f5-bcd7-2d03fccbc425/section/a69a8a8b-1b3c-4ed4-a2eb-6a9f80eed4f7 | Đọc toàn văn chương |
| S11 | World Economic Forum, *Future of Jobs Report 2025*, 01/2025 | https://reports.weforum.org/docs/WEF_Future_of_Jobs_Report_2025.pdf | Đọc trực tiếp bản PDF gốc, các phần liên quan (290 trang, không đọc hết) |
| S12 | Anthropic, "The Anthropic Economic Index", 10/02/2025 | https://www.anthropic.com/news/the-anthropic-economic-index | Đọc toàn văn. Trang chỉ số (https://www.anthropic.com/economic-index, cập nhật 26/06/2026) tải dữ liệu bằng JS nên chưa đọc được. — **không dùng (chủ dự án 01/10/2026)** |
| S13 | NPR, "Remembering When Driverless Elevators Drew Skepticism", 31/07/2015 | https://www.npr.org/2015/07/31/427990392/remembering-when-driverless-elevators-drew-skepticism | Đọc toàn văn |
| S14 | Wikipedia, "Gas lighting" | https://en.wikipedia.org/wiki/Gas_lighting | Đọc toàn văn mục liên quan |
| S15 | Wikipedia, "Elevator Strikes" | https://en.wikipedia.org/wiki/Elevator_Strikes | Đọc toàn văn |
| S16 | BLS, Occupational Outlook Handbook, "Graphic Designers" | https://www.bls.gov/ooh/arts-and-design/graphic-designers.htm | **Qua tóm tắt** (403) |
| S17 | Kịch bản tập thử v1 (nội bộ) | `/home/user/cine-lab/reports/m3/KICH-BAN-TAP-THU.md` | Đọc. Các số bên trong được kiểm qua tóm tắt. |
