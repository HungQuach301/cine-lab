# CINE LAB — CHUẨN VIỆN HÀN LÂM (OSCAR) CHO PHIM NGẮN HOẠT HÌNH VÀ ĐỐI CHIẾU MỤC TIÊU

Tra cứu ngày 26/09/2026, căn cứ quy chế giải Oscar lần thứ 99 (công bố 05/2026). Nguồn ghi cuối file.

## 0. Điều cần biết trước

**Viện Hàn lâm Khoa học và Nghệ thuật Điện ảnh Hoa Kỳ (AMPAS) không ban hành bộ tiêu chí chấm chất lượng cho từng khía cạnh của phim.** Quy chế chỉ gồm 4 loại quy định:

1. Điều kiện hợp lệ: định nghĩa, thời lượng, con đường đủ điều kiện, cấm phát hành trước.
2. Chuẩn kỹ thuật bản chiếu.
3. Quy định về AI và vai trò tác giả là con người.
4. Quy trình bỏ phiếu: hội viên từng nhánh nghề xem phim rồi xếp hạng theo ưu tiên.

"Chất lượng điện ảnh" vì thế là **đánh giá của đồng nghiệp trong nghề**, không phải một checklist. Mục 5 bên dưới là diễn giải chuyên môn của Cine Lab về những gì các nhánh nghề thường đánh giá. **Mục 5 không phải văn bản của Viện Hàn lâm.**

## 1. Điều kiện hợp lệ — Phim ngắn hoạt hình (Rule Eight, lần thứ 99)

| Hạng mục | Quy định | Áp vào Cine Lab |
|---|---|---|
| Định nghĩa phim ngắn | Phim gốc, dài ≤ 40 phút kể cả credit | Phim 2–3 phút: đạt |
| Tỷ lệ hoạt hình | ≥ 75% thời lượng (không tính credit) là hoạt hình của chủ thể chính | Dựng toàn bộ bằng mã: đạt |
| Định nghĩa hoạt hình | Nhân vật hay vật thể "được tạo ảo giác sự sống bằng chuyển động tạo ra cho chúng, **bằng bất kỳ phương tiện nào của con người**"; hoạt hình là "nghề sáng tạo và thao tác hình ảnh của con người" | Hoạt hình dựng bằng mã do model viết là vùng xám. Cần chứng minh con người giữ vai trò sáng tạo chính (xem mục 3) |
| Con đường đủ điều kiện | (a) Chiếu rạp thương mại 7 ngày liên tiếp, ít nhất 1 suất/ngày, tại các đô thị Mỹ đủ điều kiện; (b) đoạt giải đủ điều kiện tại một liên hoan phim trong danh sách; (c) huy chương Student Academy Awards | Khả thi nhất là (b) |
| Cấm phát hành trước | Phim đi đường (a) không được chiếu công khai hay phát hành ở dạng ngoài rạp (kể cả internet) trước đợt chiếu rạp; chỉ được công bố tối đa 15% thời lượng. **Phim đi đường (b) được miễn quy định này** | Xem mục 6: xung đột với YouTube |
| Thời hạn | Lần 99: phim đủ điều kiện từ 01/10/2025 đến 30/09/2026 (đã hết). Phải đủ điều kiện trong vòng 2 năm kể từ ngày hoàn thành phim | Mục tiêu thực tế là lần 100 trở đi; quy chế lần 100 chưa công bố |
| Phụ đề | Phim không nói tiếng Anh phải có phụ đề tiếng Anh chính xác, dễ đọc | Phim tiếng Anh: không áp dụng |

Một số liên hoan phim đủ điều kiện cho phim hoạt hình: Annecy (Cristal / Best Jury Award), Ottawa (Grand Prize), Hiroshima Animation Season (Grand Prix), Animafest Zagreb (Grand Prix). Tại châu Á: Bucheon BIAF (Grand Prize), ShortShorts Nhật Bản (Best Short – Animation), Singapore IFF (Best Southeast Asian Short Film), Taipei Golden Horse (Best Animated Short Film).

## 2. Chuẩn kỹ thuật bản chiếu (quy chế chung, lần 99)

- **DCP** theo bản sửa đổi mới nhất của SMPTE ST 429-2; container tối thiểu **2048 × 1080**.
- **24 hoặc 48 khung/giây, quét liên tục (progressive).**
- Không chấp nhận định dạng tiêu dùng, phát sóng hay streaming: Blu-ray, DVD, QuickTime, ProRes, MP4 đều không đạt.
- Âm thanh: mono, hoặc đa kênh rời với tối thiểu L-C-R. Cấu hình thông dụng: LCR, 5.1, 7.1. Âm thanh immersive theo SMPTE 429-19.

Hệ quả cho quy trình: bản master phải xuất được **2K DCP 24 fps kèm mix 5.1**, ngoài bản YouTube stereo 1080p. Phòng thí nghiệm cần thêm bước đóng gói DCP (công cụ mã nguồn mở như DCP-o-matic) và mix 5.1 (có thể dựng bằng ffmpeg). **Chưa kiểm chứng trong container.**

## 3. AI và vai trò tác giả là con người (lần 99)

- AI tạo sinh và công cụ số **"không giúp cũng không hại"** cơ hội đề cử.
- Viện Hàn lâm và từng nhánh nghề đánh giá thành tựu có tính đến **mức độ con người giữ vị trí trung tâm của quyền tác giả sáng tạo**. Viện có quyền yêu cầu giải trình cách dùng AI.
- Kịch bản phải do con người viết thì mới hợp lệ (áp cho hạng mục biên kịch).
- Vai diễn chỉ được xét nếu có ghi danh và do con người thực hiện, có sự đồng ý (áp cho hạng mục diễn xuất).

Tác động trực tiếp tới Cine Lab (quy trình Opus viết kịch bản và dựng hình, ElevenLabs lồng tiếng):
- **Chủ dự án phải là tác giả câu chuyện**: ý tưởng, cốt truyện, quyết định sáng tạo then chốt. Opus đóng vai trợ lý biên kịch và đội sản xuất.
- Lập **nhật ký quyền tác giả**: ghi mọi quyết định sáng tạo của con người (duyệt, sửa, chọn phương án) kèm dấu thời gian trong repo. Dùng làm bằng chứng khi bị yêu cầu giải trình.
- Giọng nhân vật bằng TTS không ảnh hưởng hạng mục Phim ngắn hoạt hình, nhưng sẽ bị giám khảo xem như một phần của việc cân nhắc vai trò con người. Với phim nhắm liên hoan phim, nên cân nhắc thuê diễn viên lồng tiếng.

## 4. Quy trình chấm phim ngắn

- Hội viên nhánh nghề bỏ phiếu kín, xếp tối đa 15 phim theo thứ tự ưu tiên; 15 phim nhiều phiếu nhất vào danh sách rút gọn.
- Ở vòng đề cử, hội viên **phải xem hết** các phim trong danh sách rút gọn rồi bầu 5 phim.
- Không có thang điểm công bố. Tiêu chí là đánh giá tổng thể của người trong nghề.

## 5. Tiêu chí theo khía cạnh — diễn giải chuyên môn của Cine Lab

Cột "Thước đo" ánh xạ sang danh mục §4 trong handoff. Thước đo máy chỉ là điều kiện cần. Điều kiện đủ là người chấm và giám khảo liên hoan phim.

| Khía cạnh | Điều hội đồng trong nghề thường đánh giá | Thước đo Cine Lab (máy + người) |
|---|---|---|
| Câu chuyện / kịch bản | Ý tưởng gốc; tiền đề rõ trong 30 s đầu; nhân vật có mong muốn và cái giá; bước ngoặt; kết có dư âm; không nói thay hình | Đọc thử; bản đồ hồi; người chấm ≥ 7/10; nhật ký tác giả |
| Đạo diễn / giọng riêng | Tầm nhìn nhất quán; mỗi lựa chọn hình và âm đều phục vụ ý đồ; phong cách nhận diện được | Tuyên bố ý đồ đạo diễn (1 trang); mỗi cảnh trong shot list có lý do |
| Thiết kế hình / art direction | Ngôn ngữ hình thống nhất; hình dáng, bảng màu, chất liệu kể chuyện; khác biệt với khuôn mẫu AI | Style bible khoá trước khi dựng; color script theo hồi |
| Hoạt hình / diễn xuất nhân vật | Nhân vật "sống": trọng lượng, thời gian, dự báo, quán tính; cảm xúc đọc được qua dáng và nhịp | 12 nguyên lý; kiểm từng cảnh bằng mắt người; không có chuyển động tuyến tính máy móc |
| Quay (máy quay ảo) | Cỡ cảnh và góc có động cơ; bố cục; chuyển động máy có lý do; ngôn ngữ ống kính | Shot list; quy tắc 180°; khoảng trống theo hướng nhìn; motion blur |
| Ánh sáng / màu | Ánh sáng tạo không khí và chiều sâu; một bảng grade nhất quán | Key/fill/rim; không banding; tương phản; an toàn cho người mù màu |
| Dựng | Nhịp căng–chùng; cắt có động cơ; không thừa khung hình | Bản đồ nhịp; độ dài cảnh biến thiên; J/L-cut |
| Âm thanh | Thiết kế âm thanh tạo thế giới; lời rõ; khoảng lặng có chủ ý; mix có không gian | Cue sheet; khoét 1–4 kHz khi có lời; mix 5.1 cho bản chiếu, stereo cho YouTube |
| Nhạc | Nhạc gốc, có chủ đề (leitmotif), khớp dựng | Tempo map; **giấy phép dùng cho phim rõ ràng (xem mục 7)** |
| Diễn xuất giọng | Giọng tự nhiên, có ý đồ diễn xuất; khớp khẩu hình nếu có | Kiểm ASR "mọi từ quan trọng phải có"; người nghe chấm |
| Kỹ thuật | Không lỗi hình (nhấp nháy, rơi khung, chữ đè); đúng chuẩn giao nộp | DCP 2K 24 fps + 5.1 (bản chiếu); YouTube 1080p ≥ 16 Mbps, −14 LUFS, TP ≤ −1 dBTP |
| Kiểm chứng bên ngoài | Được liên hoan phim chọn chiếu hoặc trao giải | Số liên hoan phim nộp / được chọn / đoạt giải |

Tham chiếu phân phối streaming (thứ cấp, production-expert.com): Netflix yêu cầu −27 LKFS ±2 LU đo theo lời (dialog-gated), true peak −2 dBTP. Dùng khi bán phim cho nền tảng streaming.

## 6. Xung đột với mục tiêu "kiếm tiền YouTube là chính + bán phim"

| Phương án | Ưu | Nhược | Tác động | Rủi ro |
|---|---|---|---|---|
| A. Đăng YouTube ngay | Có doanh thu và dữ liệu khán giả sớm | Mất đường chiếu rạp; nhiều liên hoan phim yêu cầu phim chưa công chiếu trực tuyến (cần kiểm quy định từng liên hoan phim) | Gần như bỏ con đường Oscar và bán phim cho liên hoan phim | Phim khó bán độc quyền |
| B. Liên hoan phim trước, YouTube sau | Giữ được cơ hội Oscar (đường festival được miễn cấm phát hành trước) và giá trị bán | Trễ doanh thu YouTube nhiều tháng; tốn phí nộp liên hoan phim | Cần bản DCP và mix 5.1 | Không được chọn thì mất thời gian |
| **C. Hai dòng sản phẩm (khuyến nghị)** | YouTube ra đều với phim hoặc tập ngắn; 1 phim "flagship" giữ lại cho liên hoan phim | Tốn công gấp đôi cho flagship | Học được cả hai chuẩn giao nộp | Kênh YouTube phải đủ khác biệt, tránh chính sách "nội dung không nguyên bản / sản xuất hàng loạt" của YouTube (hiệu lực 15/07/2025) |

## 7. Âm thanh: ElevenLabs (đã được chủ dự án chấp nhận)

| Dịch vụ | Giá API | Giấy phép |
|---|---|---|
| TTS Eleven v3 / Multilingual v2 | $0,10 / 1.000 ký tự | Gói trả phí có giấy phép thương mại; gói miễn phí thì không. Không dùng tính năng Beta cho sản phẩm thương mại |
| TTS Flash / Turbo | $0,05 / 1.000 ký tự | Như trên |
| Hiệu ứng âm thanh (SFX) | $0,12 / phút | Như trên |
| Nhạc (Eleven Music) | $0,15 / phút, tối đa 5 phút/bài | **Mọi gói tự phục vụ (Free → Business) đều loại trừ "phim, TV, radio, game studio".** Chỉ gói Enterprise Music (bản đầy đủ) mới cho mọi mục đích |

Ước tính: phim 3 phút tiếng Anh khoảng 3.000 ký tự lời, tức ≈ $0,30 TTS mỗi lượt đọc. Chi phí âm thanh không đáng kể so với trần $250.

**Rủi ro lớn nhất:** dùng Eleven Music cho phim đem bán hoặc nộp liên hoan phim có thể vi phạm điều khoản nếu không có gói Enterprise. Nhạc trên YouTube có thuộc nhóm "online commercial use" được phép hay không còn mơ hồ, vì sản phẩm vẫn là "phim". Phương án thay thế:
1. Liên hệ ElevenLabs xin báo giá Enterprise Music.
2. Dùng thư viện nhạc có giấy phép đồng bộ cho phim.
3. Thuê nhà soạn nhạc là người, việc này cũng củng cố vai trò tác giả con người.
4. Nhạc sinh bằng mã (mắt xích yếu, đã biết).

## Nguồn

- AMPAS — 99th Oscars Complete Rules: https://www.oscars.org/sites/oscars/files/2026-05/99th_oscars_complete_rules.pdf
- AMPAS — 99th Shorts Qualifying Festival List: https://www.oscars.org/sites/oscars/files/2026-05/99AA_Shorts%20Qualifying%20Festivals.pdf
- AMPAS Press — Rules approved for 99th Oscars: https://press.oscars.org/news/awards-rules-and-campaign-promotional-regulations-approved-99th-oscarsr
- ElevenLabs — API pricing: https://elevenlabs.io/pricing/api
- ElevenLabs — Publishing/commercial rights: https://help.elevenlabs.io/hc/en-us/articles/13313564601361-Can-I-publish-the-content-I-generate-on-the-platform
- ElevenLabs — Eleven Music model-specific terms: https://elevenlabs.io/eleven-music-model-specific-terms
- YouTube — Channel monetization policies (inauthentic content): https://support.google.com/youtube/answer/1311392
- Production Expert — Netflix loudness (thứ cấp): https://www.production-expert.com/production-expert-1/understanding-loudness-part-4-creating-loudness-compliant-mixes-for-broadcast-and-netflix
