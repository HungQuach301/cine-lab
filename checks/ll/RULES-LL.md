# Last Lamplighters — luật kênh khoá, bản LL v2 (phiên K, 06/10/2026)

Chủ dự án duyệt lệnh khoá ngày 06/10/2026. Áp cho mọi tập dựng bằng `scripts/ll/`, chạy qua `bash scripts/ll/qc.sh <episode.yaml>`.
Mã luật nằm trong `checks/ll/` và được khoá SHA-256 trong `checks/LOCK`. qc.py chỉ gọi luật và có thêm dòng **LOCK** (TRƯỢT nếu `checks/` đã bị sửa).
Phiên xưởng không đọc mã trong `checks/`; chỉ cần đọc tệp này. Khiếu nại về luật ghi vào `checks-appeal.md`.

| Mã | Luật (TRƯỢT khi…) | Dữ liệu đọc |
|---|---|---|
| Q7 | Shot có số mà thiếu nhãn của loại số đó (ACTUAL/PROJECTION). **Mới ở v2:** shot hiện nhãn của một loại mà shot không có số loại đó; tham số `kind` khai trên mẫu khác `kind` của `num` đi kèm | đặc tả + log render (`text`) |
| Q12 | Thumbnail khác 1280×720; thiếu `.boxes.json`; hộp chữ (gồm nền chữ) chạm hoặc vượt lề an toàn 5 % | ảnh + `.boxes.json` |
| Q13 | Số trên tiêu đề, chữ thumbnail, câu mô tả YouTube, hook và chữ Shorts không truy được về `numbers` (năm 1800–2100 phải có trong lời hoặc số; số đếm < 10 bỏ qua; "k" = nghìn, "million" sai lệch ≤ 5,1 %). **Mới ở v2:** sai dấu (+9 % khi số là −9 %). Số dự báo phải có dấu hiệu dự báo trong cùng câu: projected, projection, forecast, expects, "by 20xx", "(proj". **Ở v2, dấu "?" không còn được tính là dấu hiệu dự báo** | đặc tả + `phat-hanh/` |
| Q14 | Trước 0:15 không có câu hỏi hay mâu thuẫn bằng lời (có "?", but, yet, never…) kèm hình; tựa phim (`text` + `lamp`) muộn hơn 0:20; đoạn `hook.answer` không chứa đủ `hook.keys` | timeline + giọng `.align.json` |
| Q15 | Có quãng > 8 s không có sự kiện hình, hoặc trung bình > 6 s | timeline |
| Q16 | Thẻ giấy (mẫu đồ hoạ, không tính cảnh toàn khung) vượt `rhythm.paper_max` (mặc định 55 %) | timeline |
| Q17 | Số mới trên hình > 2/phút, hoặc `anchors` không đúng 3 số có hiện trên hình | timeline |
| Q18 | Shot số liệu (bars/line/compare/bignum) có số đầu tiên muộn hơn 1,5 s sau đầu shot | timeline |
| Q19 | Shot `archive` không có `rid` khớp một dòng RIGHTS.md; URL ngoài danh sách trắng (loc.gov, *.gov; **v2: tên miền phải kết thúc ở .gov**); thiếu tình trạng quyền, ngày tải, tệp ảnh hoặc `credit`; tư liệu > 20 % thời lượng | đặc tả, RIGHTS.md, timeline |
| Q20 | Cờ `hit` của render ≠ 0. **Mới ở v2:** khi log có `zones` (vùng hình như isotype), mọi hộp chữ không được giao vùng hình. **Từ tập 6**, đoạn có isotype bắt buộc ghi `zones` vào log | log render |
| Q21 | Dòng nguồn đang hiện thiếu nguồn của câu hay số đang hiện; câu có số, năm hoặc cơ quan mà không khai `num` hay `src`. **Mới ở v2:** nguồn cần có lấy cả từ đặc tả (nguồn của `num`, danh sách `src` của câu), không chỉ từ `capsrc` do ll.py ghi | đặc tả + timeline |
| Q22 | Hộp chữ ở khung mẫu ra ngoài khung hoặc cách mép trái/phải < 8 px (16:9 và Shorts 9:16). **Mới ở v2:** không có log render thì TRƯỢT, vì không đo được | log render |
| **Q23** (mới) | Một câu lời, một thẻ, một chú thích hay một dòng phát hành có ≥ 2 số mà (a) số thuộc hai họ nguồn khác nhau (cơ quan phát hành, chữ đầu của `short`); (b) trộn ACTUAL với PROJECTION, trừ khi số ACTUAL là **điểm gốc dự báo** (số mức cùng nguồn, năm = năm đầu kỳ dự báo); (c) các tỷ lệ thay đổi (đơn vị `%`, chữ có dấu +/−) khác loại hoặc khác kỳ; (d) số mức thuộc hai cơ sở phân loại mà khung không ghi riêng từng cơ sở ("YYYY classification"), hoặc số cùng nguồn có số khai cơ sở, có số không khai, mà khung không nhắc cơ sở. **Khung riêng:** thẻ mà mọi số mức (trừ tối đa một) có nhãn riêng ghi năm của nó (label/years/name/title) thì không xét (a), (b), (d). Tỷ lệ thay đổi không bao giờ được miễn | lời (`say`), thẻ (`num`), chú thích (`num`), bề mặt phát hành (Q13) |
| **Q24** (mới) | Nhãn "(YYYY classification)" trên đường số (tên chuỗi hoặc `ltext`) khác cơ sở phân loại của số mà nhãn gắn vào; hoặc số đó không khai cơ sở | timeline |
| **Q25** (mới) | Thẻ `bignum` khoảng số (`range`, `value` là mảng, hoặc chữ dạng "50–80…") hiện bất kỳ chuỗi có chữ số nào không nằm trong tham số của thẻ (tức là số trung gian khi đếm) | timeline + log render |
| LOCK | `checks/` không khớp `checks/LOCK` | `checks/lock.py --verify` |

## Khai báo trong đặc tả để luật đọc đúng
- `numbers.<k>.kind`: actual | projection. Nếu là dự báo thì có `period: YYYY–YY`. Số thật có `year`; tỷ lệ thay đổi thật thì ghi kỳ trong `period` hoặc `note` (ví dụ `1930–40`).
- `numbers.<k>.basis: "1970"` (hoặc `note` có "1970 classification") cho số Census/HSUS theo phân loại nghề.
- `numbers.<k>.say`: cụm đọc **đúng như trong lời**. Q23 nhận số trong lời bằng cụm này.
- Từ tập 6, render ghi `zones` (toạ độ khung) vào từng mục `text` của log cho đoạn có isotype.

## Không đổi so với luật làm việc của P
Ngưỡng của Q12–Q22 giữ nguyên như P đề xuất ở lô 3–5. Q1–Q6 và Q8–Q11 vẫn là luật làm việc của P (xem checks-appeal mục 8; chưa khoá ở bản này).

## Tự kiểm
`/opt/cine/bin/python checks/ll/selftest_ll.py` cho 52/52 ca đúng kỳ vọng. Dữ liệu tự kiểm là bản đóng băng tập 2–5 trong `checks/ll/fixtures/`.
