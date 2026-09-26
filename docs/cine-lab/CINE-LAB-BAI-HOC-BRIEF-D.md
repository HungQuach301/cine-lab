# CINE LAB — BÀI HỌC TỪ BRIEF-D VÀ ĐỀ XUẤT NÂNG CẤP CHO BỘ LUẬT CINE (26/09/2026)

Đầu vào: đầu bài phiên K và BRIEF-D (bài thử D, Crux); kết quả phiên K chạy luật trên bài C là 27 đạt / 32 trượt / 12 thiếu (theo handoff §3); các quyết định Cine Lab ghi trong handoff §2; chuẩn Oscar tổng hợp trong `claude/CINE-LAB-CHUAN-OSCAR.md`.
Tài liệu này chưa đọc mã checks/ trong repo, nên phần đánh giá luật dựa trên đầu bài.

## 1. Những gì BRIEF-D làm đúng — giữ nguyên

| # | Cơ chế | Vì sao giữ |
|---|---|---|
| 1 | Tách phiên K (viết và khoá luật) khỏi phiên D (dựng); khoá SHA-256; khiếu nại ghi vào file riêng | Chặn việc tự nới luật sau khi trượt, lỗi đã thấy ở bài C |
| 2 | Mỗi luật kèm test tự chứng minh: một mẫu bắt buộc phải trượt, một mẫu bắt buộc phải sạch | Chứng minh luật có tác dụng thật, không phải luật trang trí |
| 3 | Chạy luật lên sản phẩm cũ (bài C) trước khi dùng | Bằng chứng luật bắt được lỗi thật: 32 trượt |
| 4 | Gắn nhãn [MÁY] / [NGƯỜI] cho từng yêu cầu | Tách rõ phần đo được bằng máy và phần cần mắt, tai người |
| 5 | Đo trên file đã render: va chạm chữ tính theo điểm ảnh, ASR theo từ quan trọng, PTS/CFR, banding, pha | Số đo thật thắng số tự khai |
| 6 | Cấm thêm phần tử chỉ để vượt ngưỡng; bắt khai chỉ số nằm trong ±5% quanh ngưỡng | Chống Goodhart |
| 7 | Mốc có điểm dừng; bước 0 có ngưỡng dừng (> 60 s render cho 1 s video thì DỪNG) | Không tốn tiền dựng trước khi biết hạ tầng chịu nổi |
| 8 | Truy vết nguồn và điều khoản sử dụng (URL, SHA, ngày tải, trích nguyên câu); DỪNG nếu điều khoản không cho kênh có quảng cáo | Tương đương khâu thanh lọc quyền (rights clearance) của phim |

## 2. Điểm yếu của chính bộ luật D — bài học

| # | Điểm yếu | Biểu hiện trong BRIEF-D | Hệ quả |
|---|---|---|---|
| W1 | **Máy kiểm lời khai thay vì kiểm hình** | "đếm theo khai báo" (match cut, J/L-cut); tension map do phiên D tự nộp; rack focus chỉ đếm | Goodhart chuyển từ con số sang bản khai |
| W2 | **Chỉ tiêu số lượng cho kỹ thuật nghệ thuật** | ≥ 5 match cut, ≥ 3 rack focus, ≥ 3 khoảng lặng, CV độ dài câu ≥ 0,35, ≥ 70% cú cắt trúng phách | Khuyến khích nhồi kỹ thuật. Điện ảnh đánh giá động cơ của kỹ thuật, không đánh giá số lần dùng |
| W3 | **Không phân cấp mức nghiêm trọng** | 71 luật ngang hàng; 32 trượt không cho biết lỗi nào chặn phát hành | Phiên D sửa lỗi dễ trước, bỏ lỗi quan trọng |
| W4 | **Máy kiểm chưa được hiệu chuẩn với mắt người** | Không có bước so kết quả máy với điểm người | Có thể "đạt 71/71" mà phim vẫn dở; không biết luật nào vô ích |
| W5 | **Người chấm là một người, không mù** | RUBRIC 1–5 nhưng không nói ai chấm, xem mấy lần | Thiên lệch người trong cuộc; không đo được khán giả thật |
| W6 | **Khoá cứng nhưng không có quy trình phán quyết khiếu nại** | Có checks-appeal.md, không có ai quyết, không có lúc quyết | Luật sai ép dựng sai, hoặc khiếu nại dồn ứ |
| W7 | **Phiên K và phiên D cùng một model** | Cùng Opus 5.5 | Điểm mù tương quan: luật không bắt được đúng loại lỗi mà model dựng không thấy |
| W8 | **Chỉ một chuẩn phát hành** | 30 fps, stereo, −14 LUFS | Không đủ cho liên hoan phim (DCP 24/48 fps, tối thiểu LCR, thường 5.1) |
| W9 | **Không có luật cho nhân vật, diễn xuất, cảm xúc** | Hợp với data-explainer | Là trọng tâm của phim hư cấu nên phải viết mới |

## 3. Ánh xạ sang Cine Lab (hư cấu phong cách hoá, 2–3 phút, tiếng Anh, YouTube + bán phim)

### 3.1 Giữ nguyên
Cơ chế K/D/SHA/khiếu nại; test tự chứng minh; va chạm chữ theo điểm ảnh (áp cho tiêu đề, phụ đề, credit); kiểm kỹ thuật file (PTS, CFR, BT.709, banding, pha, mono); master; bước 0; báo chỉ số sát ngưỡng.

### 3.2 Bỏ
Mục 1 của BRIEF-D (mô hình tài chính, dữ liệu, đúng số, nhân dạng người phân tích); mật độ con số; callback con số; điểm chèn quảng cáo giữa video (YouTube chỉ cho mid-roll với video từ 8 phút trở lên).

### 3.3 Điều chỉnh

| Luật D | Cine |
|---|---|
| 30 fps CFR | **24 fps CFR** (chuẩn DCP 24/48) |
| Một master YouTube | **Hai master:** (1) YouTube 1080p stereo −14 LUFS, TP ≤ −1 dBTP; (2) bản chiếu DCP 2K 24 fps, 5.1 (kèm bản gộp stereo). Tham chiếu streaming: −27 LKFS đo theo lời, TP −2 dBTP |
| ASR "mọi từ quan trọng" | Thoại hư cấu: **mọi từ trong kịch bản** phải có (WER với danh sách từ bắt buộc = toàn bộ thoại) + người nghe chấm diễn xuất |
| Nhạc sinh bằng mã + sổ giấy phép | Sổ giấy phép mở rộng thành **sổ quyền** cho mọi tài sản (nhạc, SFX, giọng, font, tham chiếu); nhạc phải có quyền dùng cho phim (Eleven Music gói tự phục vụ bị loại trừ) |
| Quy tắc 180°, giữ phía/màu/hình dạng nhân vật | Giữ nguyên, áp cho nhân vật thật trong truyện |

### 3.4 Thêm mới

| Mã | Nhóm | Yêu cầu | Loại |
|---|---|---|---|
| S1 | Kịch bản | Logline 1 câu; nhân vật chính có mong muốn, trở ngại, cái giá; 3 nhịp: thiết lập, đối đầu, giải quyết; kết thay đổi nhân vật hoặc người xem | NGƯỜI |
| S2 | Kịch bản | Không thoại giải thích điều hình đã cho thấy; có ẩn ý (subtext) | NGƯỜI |
| S3 | Kịch bản | Table read bằng giọng ElevenLabs trước khi dựng; nộp audio + danh sách sửa | MÁY (có file) + NGƯỜI |
| A1 | Quyền tác giả | AUTHORSHIP.md: mọi quyết định sáng tạo then chốt (logline, beat sheet, thiết kế nhân vật, chọn take, bản dựng) có dòng duyệt của chủ dự án kèm thời điểm | MÁY (đủ mục) |
| C1 | Nhân vật | Model sheet khoá trước khi dựng: tỷ lệ, bảng màu, hình dạng | MÁY (có file, SHA) |
| C2 | Nhân vật | **Đọc được qua silhouette**: tô đen đặc từng tư thế then chốt, người xem vẫn nhận ra hành động | MÁY (khác biệt hình dạng) + NGƯỜI |
| C3 | Nhân vật | Đúng model qua các cảnh: tỷ lệ các phần so với model sheet sai lệch ≤ ngưỡng | MÁY |
| M1 | Hoạt hình | Không chuyển động tuyến tính ở bộ phận nhân vật; có easing; khớp đi theo cung | MÁY (đường cong transform của rig) |
| M2 | Hoạt hình | Timing chart và tư thế then chốt cho mỗi hành động; lấy đà, theo đà, chồng lớp | NGƯỜI (xem từng cảnh) |
| M3 | Hoạt hình | Khớp khẩu hình (nếu có thoại): hình miệng khớp âm vị ±1 khung theo forced alignment | MÁY |
| V1 | Giọng | Nhiều take cho mỗi câu; người chọn take; chỉ đạo diễn xuất ghi trong kịch bản | MÁY (có file) + NGƯỜI |
| R1 | Quyền | Sổ quyền: mọi tài sản có nguồn, giấy phép, phạm vi (YouTube, liên hoan phim, bán); không giống IP có sẵn | MÁY (đủ trường) + NGƯỜI |
| D1 | Giao nộp | DCP hợp lệ theo SMPTE (kiểm bằng công cụ xác thực DCP); 5.1 gộp stereo không lệch pha; bản không chữ; stem M&E; phụ đề | MÁY |
| Y1 | YouTube | Mỗi phim khác biệt rõ về truyện, hình, nhạc (chính sách "nội dung không nguyên bản/sản xuất hàng loạt") | NGƯỜI |

## 4. Nâng cấp cơ chế (sửa W1–W7)

| Đề xuất | Ưu | Nhược | Tác động | Rủi ro |
|---|---|---|---|---|
| **N1. Đo từ file, không từ bản khai.** Cú cắt phát hiện bằng scene detection rồi đối chiếu EDL; match cut, rack focus do máy đề cử, người xác nhận | Gỡ W1 | Một số kỹ thuật (match cut theo ý nghĩa) máy không đo được | Luật ít hơn nhưng thật hơn | Scene detection nhầm với chuyển động nhanh; cần test tự chứng minh |
| **N2. Bỏ quota kỹ thuật, thay bằng "có động cơ".** Mỗi kỹ thuật phải có lý do trong shot list; người chấm động cơ; số lượng chỉ là cảnh báo | Gỡ W2, đúng tinh thần điện ảnh | Phụ thuộc người chấm | Giảm nhồi kỹ thuật | Lý do viết cho có; người chấm phải bác được |
| **N3. Phân 3 cấp: Chặn / Chính / Tham khảo.** Chặn = kỹ thuật file, quyền, thoại thiếu từ, chữ đè; mốc không qua khi còn lỗi Chặn | Gỡ W3; ưu tiên rõ | Cần thống nhất phân cấp trước khi khoá | Báo cáo đọc nhanh | Phân cấp sai làm lọt lỗi |
| **N4. Hiệu chuẩn luật với người.** Chạy luật + cho người chấm trên 3–5 mẫu (bài C, bản nháp, 1–2 phim tham chiếu công khai); luật không phân biệt được mẫu tốt và xấu thì hạ cấp | Gỡ W4; biết luật nào có giá trị | Tốn công chấm | Bộ luật gọn lại | Mẫu ít nên kết luận yếu |
| **N5. Người chấm mù, nhiều người.** ≥ 3 người xem nói tiếng Anh, không biết quy trình, xem một lần ở tốc độ thường; câu hỏi: tóm tắt truyện, điểm mất chú ý, cảm xúc, có xem tiếp không | Gỡ W5; gần khán giả thật | Phải tìm người; chậm | Đo được mục tiêu YouTube (giữ chân) | Mẫu nhỏ, ồn |
| **N6. Phán quyết khiếu nại tại mỗi mốc.** Chủ dự án duyệt; phiên K mới phát hành luật v1.x với SHA mới, ghi lý do | Gỡ W6 | Thêm một bước | Luật tiến hoá có kiểm soát | Bị dùng để nới luật; chỉ chấp nhận khi có bằng chứng luật đo sai |
| **N7. Chấm chéo bằng model khác hoặc người** cho các luật về hình và âm | Giảm W7 | Chi phí, hạ tầng | Bắt được điểm mù chung | Model khác cũng có điểm mù riêng |

## 5. Rủi ro chiến lược mới phát hiện

YouTube chỉ cho quảng cáo giữa video (mid-roll) với video từ 8 phút trở lên. Phim 2–3 phút chỉ có quảng cáo đầu/cuối, doanh thu mỗi lượt xem thấp. Điều này mâu thuẫn với "kiếm tiền YouTube là chính". Các hướng cân nhắc:
1. Tuyển tập nhiều phim ngắn thành một video ≥ 8 phút.
2. Phim nhiều tập cùng thế giới.
3. Kèm video hậu trường ("how an AI made this film") dài ≥ 8 phút.
4. Chấp nhận phim ngắn là sản phẩm xây thương hiệu; doanh thu chính đến từ bán phim.

**Đã giải quyết:** chủ dự án xác nhận phim 2–3 phút chỉ là bài thử năng lực; phim đích dài 10–15 phút, đủ điều kiện quảng cáo giữa video.

## Nguồn
- YouTube Help — Manage mid-roll ad breaks: https://support.google.com/youtube/answer/6175006
- AMPAS — 99th Oscars Complete Rules: https://www.oscars.org/sites/oscars/files/2026-05/99th_oscars_complete_rules.pdf
- ElevenLabs — Eleven Music model-specific terms: https://elevenlabs.io/eleven-music-model-specific-terms
