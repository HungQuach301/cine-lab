# BÀI HỌC — Kênh 2 (cơ chế kinh tế, ngách B/G)

> Mọi phiên P kênh 2 đọc tệp này khi khởi động, cùng `reports/m3/BAI-HOC-LL.md` (phần dùng chung của nhà máy).
> Mỗi dòng: bài học · số đo · nguyên nhân · luật hiện hành (nằm ở đâu). Chủ dự án duyệt ghi 11/10/2026 (G1 K2G-01, D6).

| # | Bài học | Số đo | Nguyên cớ | Luật hiện hành |
|---|---|---|---|---|
| K1 | Nhân giá CBAM (€/t CO₂) với cường độ CO₂ theo tuyến của worldsteel là **trộn cơ sở**: CBAM với thép chỉ tính phát thải **trực tiếp** (quy định (EU) 2023/956, Phụ lục II), còn số worldsteel tính theo phương pháp riêng (có phần gián tiếp) | K2G-01: phép tính "≈ 190 €/t vs ≈ 57 €/t" sống qua v1–v3.3, REVIEWER Opus phát hiện ở lượt 7 | ghép hai số đúng từ hai nguồn mà không đọc định nghĩa phạm vi | Phép tính riêng của kênh phải kiểm **định nghĩa và phạm vi** của từng đầu vào (BAI-HOC LL #62 mở rộng sang luật/giá); khác phạm vi thì bỏ phép tính, chỉ nêu cơ chế (claims C51 → C73) |
| K2 | Sự kiện "đang diễn ra" có thể đổi trong 3 tuần giữa lúc viết lời | Stegra: thông cáo 24/06/2026 "timeline under review" → tin 30/09/2026 cần thêm vốn, đổi CEO; lời v2 ghi "latest public update" đã lỗi thời, phát hiện ở vòng kiểm 2 | tra trạng thái một lần lúc lấy nguồn | Tra lại mọi trạng thái "as of" **ngay trước khi khoá lời** và **ngay trước khi thu giọng** (LUAT-NOI-DUNG-G §5); ghi ngày tra vào `claims.md` |
| K3 | REVIEWER Opus không hội tụ trong một lượt: mỗi lượt sửa câu làm lộ lỗi câu mới | K2G-01: major 13 → 6 → 4 → 3 → 3 → 4 → 1 → 2 → 0 qua 9 lượt; minor không về 0; Opus = $5,37 / $6,12 chi phí AI | sửa từng câu theo danh sách, câu mới lại có quy chủ thể/nhân quả/mốc thời gian chưa chặt | **Tiêu chí dừng: 0 major** (minor áp nếu rẻ, không chạy thêm lượt vì minor). Viết lời từ đầu theo danh sách lỗi hay gặp: nhân quả chỉ khi nguồn nêu; "as of" cho mọi sự kiện mở; quy lời cho đúng chủ thể (văn bản, cơ quan, báo); không tự chấm đạt/trượt chính sách; số khác cơ sở nói rõ |

## K4 · Mốc "@từ" khớp lần xuất hiện ĐẦU TIÊN — kiểm thứ tự shot bằng máy (G2 K2G-01, 12/10/2026)
- **Chuyện xảy ra:** đoạn 08 `@by` khớp "by 2028" thay vì "By our calculation"; đoạn 12 `@question` khớp "security question" thay vì "One question". Shot sau bắt đầu TRƯỚC shot trước → thẻ số neo 131,2 Mt và shot "a toll" không bao giờ hiện; QC nhà máy (Q1–Q25) không bắt được, chỉ lộ khi soát timeline sau QC 1080p. Tốn một lượt dựng lại 2 đoạn.
- **Luật:** `scripts/k2/prep.py` nay dừng hẳn khi có shot `t1 ≤ t0 + 0,3 s`. Khi viết đặc tả, từ phổ biến (by, in, the, question, one, our…) luôn kèm `#n` hoặc chọn từ hiếm.
- **Lưu ý cho LL:** README LL đã ghi bẫy "@many"; nên thêm cùng chặn vào `scripts/ll/ll.py` (đề xuất cho phiên P LL/K, không sửa ở phiên này).

## K5 · Màu canvas trong three.js mới: `THREE.Color` ở hệ tuyến tính (G2 K2G-01)
- Vẽ vân bằng `new THREE.Color(hex).multiplyScalar(k)` rồi lấy `c.r*255` cho ra màu tuyến tính → vân tối gần đen sau khi texture được coi là sRGB. Dùng `'#' + c.getHexString()`. Phát hiện ở nháp 960×540 nhờ soát khung, trước khi dựng 1080p.

## K6 · Bối cảnh tính cả thẻ (chủ dự án duyệt D4, 12/10/2026)
- **Chuyện xảy ra:** luật đa dạng bối cảnh (Q26b kênh 2) tính bối cảnh theo cảnh 3D nền, kể cả nền mờ sau thẻ số → K2G-01 đạt (lớn nhất 21,7 %). Nhưng cả 3/3 người xem mù (Q31) nêu "thẻ tối trên nền mờ" là bối cảnh bị lạm dụng (~ một nửa tấm tổng quan); Q27 tay nghề 5/10.
- **Luật từ tập sau:** "thẻ trên nền mờ" là MỘT bối cảnh riêng, chịu cùng trần (≤ 25 % thời lượng, ≤ 90 s liên tục). Nền mờ không tính cho bối cảnh của cảnh 3D. `scripts/k2/settings.py` sẽ tính thêm hạng mục `card` (phiên P làm ở tập sau); luật khoá do phiên K cập nhật (không sửa `checks/` ở phiên P).

## K7 · Đề xuất nâng hình cho tập sau (chủ dự án ghi nhận D3, 12/10/2026; không làm lại K2G-01)
- **Số đặt trong cảnh 3D rõ nét** bằng nhãn bám vật thể (như đoạn 00, 05 của K2G-01); thẻ trên nền mờ chỉ cho số cần so sánh trên trục (cột, đường).
- **Thay một phần thẻ-trên-nền-mờ bằng footage lưu trữ** theo `QUAN-TRI-RUI-RO.md` §6: nguồn cho phép (LoC, NARA, NASA, Prelinger, Commons kiểm từng file, Pexels/Pixabay), trần ≤ 40 % thời lượng và ≤ 8 s mỗi clip, nhãn năm trên hình, sổ `SOURCES-FOOTAGE.csv`, không commit media, giữ màu gốc cảnh lưu trữ.
- **Thẻ co theo nội dung** (không nửa thẻ trống); mục đầu luôn hiện khi vào thẻ.
- **Phụ đề có nền đậm** (dải đặc, không chỉ gradient) và chữ trắng đủ đậm; kiểm Q5 trên khung trời sáng.
- **Vật liệu PBR và ánh sáng giàu hơn** cho port/mill (Q27 nêu "khối xám phẳng"); bản đồ có nhãn địa danh trên hình.
- **Đo:** Q27 tay nghề ≥ 7/10 và "above" so với faceless thường mới coi là tiến bộ; giữ chấm mù một lần trên 1080p.
- Ưu: tăng điểm hình, giảm cảm giác "slide". Nhược: thêm giờ dựng cảnh và giờ tìm footage. Rủi ro: SwiftShader chậm (4,2 s/khung SPP4); footage sai quyền → luật §6 và sổ CSV.
