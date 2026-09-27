# CINE LAB — RUBRIC NGƯỜI CHẤM L2 (v1.1, phiên K)

Căn cứ: `docs/cine-lab/CINE-LAB-KHUNG-CHAT-LUONG.md` mục 4 (mọi mã có loại **N**) và mục 6 (neo chung 1/3/5).
Phạm vi: 17 mã A1, A2, A3, B1, B3, C1, D2, D3, E2, G1, H4, K1, K2, L3, O2, P3, Q3. Phần máy (M) và khán giả (K) của các mã lai được đo riêng; rubric này chỉ chấm phần người.

## 1. Cách chấm

- **Thang 1–5.** Mỗi mã có mô tả mức 1, 3, 5. Mức 2 = có dấu hiệu của cả 1 và 3; mức 4 = đạt đủ mức 3 và có ít nhất một dấu hiệu của mức 5 nhưng chưa đủ.
- Neo chung (khung mục 6): **1** lỗi thấy ngay, kéo người xem ra khỏi phim · **3** đúng nghề nhưng không đáng nhớ · **5** ngang phim tham chiếu, chủ động phục vụ cảm xúc và truyện.
- **Bằng chứng bắt buộc:** mọi điểm ≠ 3 phải kèm ít nhất một mốc thời gian (`mm:ss`) hoặc số shot và một câu mô tả điều nhìn/nghe thấy. Điểm không có bằng chứng bị loại.
- **Người chấm:** ≥ 3 người, chấm độc lập, không xem điểm của nhau và không biết phần nào do máy làm. Điểm cuối = trung vị. Hai người lệch nhau ≥ 2 điểm ở cùng mã → thảo luận, ghi lý do, chấm lại một lần.
- **Xem một lần ở tốc độ thường** trước, rồi mới tua lại để lấy bằng chứng. Ấn tượng lần xem đầu ghi riêng.
- **Mức 5 cần đối chiếu phim tham chiếu.** Phim tham chiếu đã chọn (v1.1): *Ice Merchants*, *Hair Love*, *Alike*, *The Flying Sailor*, *Sprite Fright*. Chỉ *Sprite Fright* được tải để phân tích (CC BY 4.0, mục 1.1). Mã có ví dụ mức 5 (dòng **Ví dụ mức 5** dưới mã) được chấm tới 5. Mã chưa có ví dụ vẫn giữ **trần = 4**: D2, D3, E2, G1, H4, L3, P3 mở trần; A1, A2, A3, B1, B3, C1, K1, K2, O2, Q3 giữ trần 4.
- Mã có cấp **Chặn** (O2, Q3): trung vị ≤ 2 là chặn cổng. Mã cấp **Chính**: trung vị ≤ 2 phải sửa trước cổng sau. Mã **Tham khảo** (B3, L3): chỉ ghi nhận.
- Phiếu chấm: mỗi dòng `mã | điểm | mốc thời gian | điều quan sát được | đề xuất sửa (tuỳ chọn)`.

### 1.1 Phim tham chiếu dùng cho ví dụ mức 5

- **"Sprite Fright"** © Blender Foundation | studio.blender.org — giấy phép Creative Commons Attribution 4.0 (https://creativecommons.org/licenses/by/4.0/). Phim chiếu ở credit cuối (10:19): *"licensed as creative commons attribution 4.0 / © Blender Foundation"*. Bản dùng: archive.org/details/sprite-fright, file 804p (1920×804, 24 fps, 10:29,9). Nguồn, SHA-256 và ngày tải ghi trong `RIGHTS.md` (mã REF-SF). Không sửa đổi phim; chỉ trích khung để phân tích nội bộ; không commit video hay khung vào repo.
- Mốc `mm:ss` tính theo file trên, bắt đầu từ 00:00 (logo Blender 00:00–00:04; tên phim 09:14; credit 09:18–10:30).
- Mỗi ví dụ đã được phiên K tự kiểm bằng cách trích khung thật ở đúng mốc và xem. L3 được kiểm thêm bằng số đo độ ồn. Phần mô tả mức 5 mà ví dụ không chứng minh được ghi ở dòng "Giới hạn".
- Ví dụ minh hoạ **mức 5 trông ra sao**. Đây không phải mẫu để sao chép (luật cứng CLAUDE.md: không sao chép thiết kế, nhân vật hay nhạc của phim tham chiếu).
- Bốn phim còn lại chưa tải và chưa phân tích, nên chưa có mốc thời gian.

## 2. Rubric từng mã

### A1 — Chủ đề (Cổng 1, 2, 4) · Chính
**Câu hỏi:** Sau khi xem, người chấm có viết được chủ đề trong một câu, và mọi sequence có phục vụ câu đó không?
- **1:** Không viết được chủ đề một câu, hoặc câu viết ra khác hẳn bảng ánh xạ chủ đề của đội. Có ≥ 2 sequence không liên quan tới chủ đề (bỏ đi truyện không đổi).
- **3:** Viết được chủ đề khớp bảng ánh xạ. Mọi sequence gắn với chủ đề, nhưng có sequence chỉ gắn qua thoại nói ra thay vì qua hành động hay hình.
- **5:** Chủ đề viết ra khớp bảng ánh xạ mà không cần nghĩ lâu; mỗi sequence thể hiện chủ đề qua lựa chọn của nhân vật hoặc hình ảnh lặp lại có biến đổi; không sequence nào nói thẳng chủ đề bằng lời.

### A2 — Mỗi cảnh xoay một giá trị (Cổng 1, 2, 4) · Chính · phần N (máy kiểm beat sheet đủ trường)
**Câu hỏi:** Ở mỗi cảnh, giá trị ghi trong beat sheet có thật sự đổi trên màn hình không?
- **1:** ≥ 2 cảnh kết thúc ở đúng giá trị lúc bắt đầu (cắt cảnh đi truyện không mất gì), hoặc giá trị chỉ đổi qua lời kể/thoại tóm tắt.
- **3:** Mọi cảnh có giá trị đổi đúng beat sheet, nhìn thấy được; nhưng ≥ 1 cảnh đổi giá trị cùng chiều với cảnh trước (hai cảnh liền cùng "an toàn → nguy hiểm") nên nhịp phẳng.
- **5:** Mọi cảnh đổi giá trị đúng beat sheet bằng một sự kiện trên màn hình; các cảnh liền nhau đổi chiều xen kẽ (lên/xuống); điểm đổi giá trị chỉ ra được bằng một mốc thời gian cụ thể trong mỗi cảnh.

### A3 — Cấu trúc truyện (Cổng 1, 2, 4) · Chính
**Câu hỏi:** Người chấm có chỉ ra được sự kiện khởi đầu, bước ngoặt giữa, cao trào, kết, và lựa chọn của nhân vật chính ở cao trào không?
- **1:** Thiếu ≥ 1 trong 4 mốc, hoặc cao trào được giải quyết bởi tình cờ/nhân vật khác thay vì lựa chọn của nhân vật chính.
- **3:** Chỉ ra đủ 4 mốc bằng mốc thời gian; nhân vật chính có lựa chọn ở cao trào, nhưng lựa chọn đó không có giá phải trả (không mất gì).
- **5:** Đủ 4 mốc; lựa chọn ở cao trào có giá rõ ràng (nhân vật từ bỏ điều đã muốn từ đầu) và được chuẩn bị từ trước (một hình ảnh hay hành động ở nửa đầu báo trước).

### B1 — Không thoại giải thích điều hình đã cho thấy (Cổng 2) · Chính
**Câu hỏi:** Có câu thoại nào nói lại điều khán giả vừa thấy hoặc sẽ thấy ngay không?
- **1:** ≥ 3 câu thoại mô tả điều đang thấy trên hình ("It's getting dark", khi trời đang tối) hoặc giải thích cảm xúc nhân vật đang diễn.
- **3:** 1–2 câu thoại thừa như vậy; bỏ đi không mất thông tin.
- **5:** 0 câu thừa: mọi câu thoại thêm thông tin hình không cho (ý định, quá khứ, điều nhân vật giấu). Người chấm tắt tiếng đoạn bất kỳ vẫn hiểu hành động, bật tiếng thì hiểu thêm điều mới.

### B3 — Ẩn ý (Cổng 2) · Tham khảo
**Câu hỏi:** Ở các cảnh then chốt, điều nhân vật muốn có khác điều nhân vật nói không?
- **1:** Ở mọi cảnh then chốt, nhân vật nói thẳng điều mình muốn và cảm thấy ("I'm sad because…").
- **3:** Có ≥ 1 cảnh then chốt mà lời nói và mong muốn khác nhau, người chấm nhận ra khi xem lại.
- **5:** Ở phần lớn cảnh then chốt, mong muốn thật chỉ lộ qua hành động hoặc im lặng trái với lời nói, và người chấm nhận ra ngay lần xem đầu.

### C1 — Chiều sâu nhân vật (Cổng 3, 6) · Chính
**Câu hỏi:** Từ phim (không đọc hồ sơ), người chấm có nêu được mong muốn, nhu cầu thật, điểm yếu và sự thay đổi của mỗi nhân vật chính không?
- **1:** Nêu được ≤ 1 trong 4 yếu tố, hoặc nêu ra khác hồ sơ nhân vật; nhân vật cuối phim hành xử y như đầu phim.
- **3:** Nêu được mong muốn và điểm yếu khớp hồ sơ; có thay đổi nhưng chỉ thấy qua một câu thoại hoặc một cảnh cuối.
- **5:** Nêu được cả 4 khớp hồ sơ; thay đổi thấy qua một hành động lặp lại ở đầu và cuối phim với kết quả ngược nhau.

### D2 — Ngôn ngữ hình thống nhất (Cổng 3) · Chính
**Câu hỏi:** Đặt khung hình bất kỳ cạnh style frame, hình khối, bảng màu và chất liệu có cùng một thế giới không?
- **1:** ≥ 1 tài sản trông như lấy từ phim khác (độ chi tiết, kiểu viền, chất liệu hay kiểu đổ bóng khác hẳn), thấy ngay ở tốc độ thường.
- **3:** Mọi tài sản cùng kiểu; khác biệt chỉ thấy khi dừng hình so cạnh style frame (ví dụ một đạo cụ bóng hơn, độ bo góc khác).
- **5:** Dừng hình ở 5 mốc ngẫu nhiên, mọi yếu tố khớp style frame; quy luật hình khối (ví dụ nhân vật tròn, thế giới góc cạnh) giữ đúng cả ở tài sản phụ.
- **Ví dụ mức 5 (Sprite Fright):** 00:40, 02:10, 04:54, 05:40, 08:19 (5 mốc rải đều cả phim). Ở cả 5 khung, chất liệu mịn như đất sét hay nhựa dẻo đồng nhất: người có khối kéo dài hoặc phình, sprite tròn. Quy luật hình khối giữ đúng cả ở đạo cụ phụ (loa cassette, bếp nướng, lon rác), qua ngày, đêm và ánh xanh độc. *Giới hạn:* không có style frame gốc của phim để so, nên đây chỉ là bằng chứng thống nhất nội bộ.

### D3 — Thiết kế phục vụ truyện theo color script (Cổng 3) · Chính · phần N
**Câu hỏi:** Màu và hình khối có đổi theo color script ở đúng các điểm truyện không?
- **1:** Màu gần như giống nhau suốt phim, hoặc đổi ngược color script (cảnh ấm áp dùng bảng màu của cảnh nguy hiểm) mà không có lý do ghi lại.
- **3:** Bảng màu từng sequence khớp color script, nhưng chuyển đổi xảy ra đột ngột ở ranh giới sequence thay vì theo điểm truyện.
- **5:** Màu đổi đúng tại điểm đổi giá trị (A2) trong cảnh; người chấm tắt tiếng vẫn đoán đúng tâm trạng từng sequence chỉ từ màu và hình khối.
- **Ví dụ mức 5 (Sprite Fright):** 04:40–04:43. Trong cùng một cảnh, màu chuyển từ cam lửa ấm (04:40,5, sprite quanh lửa) sang xanh lục độc (04:43, mặt Ellie trong bụi cây nhuộm xanh). Màu đổi đúng lúc sprite chuyển sang tấn công, không đợi tới ranh giới sequence. Ở tầm cả phim: vàng chiều (03:49) → xanh đêm (03:57) → hồng bình minh (09:09–09:14).

### E2 — Blocking rõ ràng (Cổng 5) · Chính · phần N
**Câu hỏi:** Ở mỗi cảnh, người chấm có biết ai đứng ở đâu so với ai, và đang nhìn gì không?
- **1:** ≥ 1 cảnh người chấm không vẽ lại được sơ đồ vị trí nhân vật, hoặc hiểu sai ai đang nói với ai.
- **3:** Vẽ lại đúng sơ đồ vị trí mọi cảnh sau khi xem; ≥ 1 lần phải tua lại mới chắc hướng nhìn.
- **5:** Vẽ lại đúng sơ đồ và hướng nhìn mọi cảnh sau một lần xem; thay đổi vị trí giữa các nhân vật tự nó kể quan hệ (lại gần khi thân, xa ra khi rạn).
- **Ví dụ mức 5 (Sprite Fright):** 00:49: Ellie đi một mình trên thân cây đổ giữa khoảng sáng, một bạn trong nhóm tụt lại trong bóng râm bên trái; khoảng cách kể việc cô bị tách khỏi nhóm. 01:14: Ellie nhỏ bé bị kẹp giữa Phil và Jay, mắt nhìn lệch sang bên. *Giới hạn:* mức 5 đòi "mọi cảnh"; phiên K mới kiểm 3 mốc (thêm 02:42).

### G1 — Ánh sáng có nguồn gốc (Cổng 3, 7) · Chính · phần N (máy kiểm có file sơ đồ)
**Câu hỏi:** Ánh sáng trên hình có khớp sơ đồ ánh sáng và có nguồn trong thế giới phim không?
- **1:** ≥ 1 shot có hướng sáng mâu thuẫn nguồn thấy trên hình (bóng đổ về phía đèn), hoặc hướng key đổi giữa hai shot liền nhau của cùng cảnh.
- **3:** Hướng và màu key/fill/rim khớp sơ đồ ở mọi shot; ánh sáng đúng nhưng đều, không dẫn mắt tới chủ thể.
- **5:** Khớp sơ đồ; mỗi shot có điểm sáng nhất hoặc tương phản cao nhất rơi đúng chủ thể kể chuyện; thay đổi ánh sáng trong cảnh có nguồn thấy được (cửa mở, đèn tắt).
- **Ví dụ mức 5 (Sprite Fright):** 05:12–05:16. Nguồn sáng là đèn pin Ellie cầm, thấy rõ trong hình. Ở 05:14 luồng sáng rọi đúng sprite: sprite là vùng sáng nhất, được chiếu từ dưới lên trên nền xanh đêm tối. Thêm 04:41: lửa xanh làm đổi ánh sáng cả cảnh, nguồn thấy được.

### H4 — Lấy đà, theo đà, chồng lớp, co giãn giữ thể tích (Cổng 6) · Chính
**Câu hỏi:** Ở các hành động chính, có lấy đà trước, theo đà sau, chuyển động chồng lớp và co giãn giữ thể tích không?
- **1:** ≥ 1 hành động lớn (nhảy, ném, quay người) bắt đầu hoặc dừng không lấy đà/theo đà; hoặc bộ phận mềm (tóc, áo, sào) dừng cùng khung với thân; hoặc co giãn làm nhân vật phình/xẹp rõ.
- **3:** Mọi hành động lớn có lấy đà và theo đà; chồng lớp có nhưng các bộ phận mềm dừng gần như cùng lúc; khó chỉ ra lỗi nhưng chuyển động không có trọng lượng riêng.
- **5:** Dừng hình từng khung ở hành động lớn: lấy đà ngược hướng rõ, bộ phận mềm trễ và dừng lệch nhau vài khung, co giãn giữ thể tích; hai nhân vật khác khối lượng chuyển động khác nhau thấy rõ.
- **Ví dụ mức 5 (Sprite Fright):** 07:34,4–07:35,1, Ellie vung que đánh sprite, kiểm từng khung. Lấy đà ngược hướng: que đưa ra sau vai, thân xoắn (07:34,5). Cú đánh có khung nhoè (07:34,83). Theo đà: tay vượt qua thân (07:35,0). Tóc và khuyên tai trễ nhịp, còn bay sau khi tay đã dừng (07:35,0–07:35,1). *Giới hạn:* chưa kiểm vế "hai nhân vật khác khối lượng chuyển động khác nhau".

### K1 — Leitmotif (Cổng 8) · Chính
**Câu hỏi:** Mỗi motif trong cue sheet có nhận ra được mỗi lần xuất hiện, và biến tấu theo truyện không?
- **1:** Người chấm không nhận ra lần xuất hiện thứ hai của motif chính, hoặc motif lặp y nguyên bất kể cảnh vui hay buồn.
- **3:** Nhận ra motif ở ≥ 2 lần xuất hiện khớp cue sheet; có biến tấu (đổi nhạc cụ, nhịp) nhưng không khớp với thay đổi của nhân vật/ý mà motif gắn vào.
- **5:** Nhận ra motif ở mọi lần xuất hiện theo cue sheet; mỗi biến tấu khớp trạng thái của nhân vật/ý tại mốc đó (ví dụ motif nhân vật chuyển từ thứ sang trưởng đúng lúc nhân vật đổi).

### K2 — Nhạc phục vụ cảnh (Cổng 8) · Chính
**Câu hỏi:** Nhạc có hỗ trợ cảm xúc cảnh đã tạo ra, thay vì tự báo trước hay nói thay cảm xúc không?
- **1:** ≥ 1 cảnh nhạc báo cảm xúc trước khi hình tạo ra nó, hoặc nhạc đè lên thoại/tiếng động then chốt, hoặc nhạc trái tâm trạng cảnh mà không có chủ ý ghi lại.
- **3:** Nhạc đúng tâm trạng mọi cảnh; nhưng nhạc phủ gần như liên tục, không có chỗ nhạc rút để cảnh tự thở.
- **5:** Nhạc vào và ra tại điểm đổi giá trị của cảnh; có chỗ nhạc rút hẳn và chỗ đó mạnh hơn nhờ im; tắt nhạc thì cảnh vẫn đứng được nhưng yếu rõ.

### L3 — Khoảng lặng có chủ ý (Cổng 8) · Tham khảo
**Câu hỏi:** Ở các beat cảm xúc ghi trong cue sheet, có khoảng lặng (bớt nhạc/tiếng) được dùng có chủ ý không?
- **1:** Không có khoảng lặng nào, hoặc có "lỗ âm" ngoài cue sheet nghe như lỗi (khác L1: đây là cảm nhận, L1 đo sàn nhiễu).
- **3:** Có khoảng lặng đúng vị trí cue sheet, nhưng người chấm không cảm thấy tác dụng khác so với đoạn liền trước.
- **5:** Khoảng lặng đúng cue sheet và người chấm ghi nó là một trong 3 khoảnh khắc mạnh nhất phim.
- **Ví dụ mức 5 (Sprite Fright):** khoảng 02:05–02:33. Khi cắt từ cảnh Phil rắc muối (02:02) sang cận nấm trúng muối, âm thanh rút hẳn: độ ồn momentary tụt từ −12…−17 LUFS xuống −25…−37 LUFS (phiên K đo bằng ffmpeg ebur128). Đoạn lặng giữ suốt lúc nấm lén bước đi và Ellie bò theo, không có thoại, rồi khép lại bằng câu "Wow, incredible". *Giới hạn:* máy chỉ xác nhận vị trí và độ sâu của khoảng lặng. Vế "một trong 3 khoảnh khắc mạnh nhất" là cảm nhận của người chấm.

### O2 — Cảnh kề nhau khớp continuity sheet (Cổng 5–7) · **Chặn** · phần N (máy so đặc trưng)
**Câu hỏi:** Qua mỗi cú cắt trong cùng cảnh, đạo cụ, trang phục, vị trí, thời điểm và thương tích có khớp continuity sheet không?
- **1:** ≥ 1 lỗi liên tục thấy ở tốc độ thường (đạo cụ đổi tay, vết thương biến mất, đèn tắt rồi sáng) không có trong sheet.
- **3:** 0 lỗi thấy ở tốc độ thường; dừng hình so cạnh sheet thấy ≤ 2 lệch nhỏ (vị trí đạo cụ lệch, nếp áo khác).
- **5:** Dừng hình ở mọi cú cắt trong cảnh, mọi mục trong continuity sheet khớp; cả chi tiết không ghi trong sheet (ánh sáng ngoài cửa sổ, bụi trên áo) cũng liên tục.

### P3 — Title sequence và credit (Cổng 9) · Chính · phần N (máy đối chiếu sổ quyền)
**Câu hỏi:** Title và credit có được thiết kế như một phần của phim không?
- **1:** Title/credit dùng font và bố cục mặc định, không liên quan tới ngôn ngữ hình của phim; hoặc chữ khó đọc ở tốc độ thường.
- **3:** Font, màu, nhịp xuất hiện khớp ngôn ngữ hình (D2); đọc được; nhưng tách khỏi truyện (có thể thay bằng thẻ đen mà phim không mất gì).
- **5:** Title/credit dùng hình ảnh hoặc motif của phim và thêm một nhịp cảm xúc (mở không khí, hoặc cho khán giả thở sau cao trào); đọc được trọn vẹn một lần xem.
- **Ví dụ mức 5 (Sprite Fright):** 09:14–09:45. Tên phim hiện trên cảnh bình minh hồng, cho khán giả thở sau đêm kinh hoàng. Mỗi thẻ credit dựng từ rác của nhóm cắm trại nay bị thiên nhiên chiếm lại, là motif của phim: túi của Ellie thành tổ chim (09:18), bếp nướng của Phil thành chậu hoa có bướm (09:26), dao gấp phủ rêu có bọ rùa bò (09:40). Chữ đọc rõ ở tốc độ thường.

### Q3 — Không giống IP có sẵn (xuyên suốt) · **Chặn**
**Câu hỏi:** Có nhân vật, thiết kế, nhạc hay cảnh nào khiến người chấm nghĩ ngay tới một tác phẩm có sẵn cụ thể không?
- **1:** Người chấm nêu được tên một tác phẩm cụ thể mà nhân vật/thiết kế/giai điệu gần như trùng (hình dáng đặc trưng, bảng màu nhận diện, câu nhạc 4 ô nhịp trở lên).
- **3:** Có gợi nhớ thể loại chung (phong cách thời kỳ, motif quen thuộc) nhưng người chấm không nêu được tác phẩm cụ thể nào.
- **5:** Không có gợi nhớ tác phẩm cụ thể; các yếu tố nhận diện chính (hình nhân vật, motif nhạc) được người chấm mô tả là riêng của phim này.

## 3. Việc còn chờ
- 10 mã giữ trần 4 vì chưa có ví dụ tự kiểm được từ *Sprite Fright*:
  - Mã truyện và nhân vật (A1, A2, A3, B1, B3, C1): cần beat sheet hoặc hồ sơ nhân vật của phim tham chiếu, hoặc người xem trọn phim để viết ví dụ.
  - Mã nhạc (K1, K2): máy không tách được nhạc để kiểm biến tấu motif hay điểm nhạc vào/ra.
  - O2: cặp cắt 03:03 → 03:23 có Ellie đổi vị trí nên không dùng làm ví dụ sạch.
  - Q3: phim tham chiếu không làm ví dụ hữu ích cho "không giống IP".
  Có thể mở trần các mã này khi 4 phim còn lại được xem, hoặc khi chủ dự án ghi ví dụ của mình (có mốc thời gian).
- Hiệu chuẩn rubric sau bài thử: mã nào có độ lệch giữa người chấm lớn (khoảng tứ phân vị ≥ 2 điểm) thì viết lại mô tả mức.
