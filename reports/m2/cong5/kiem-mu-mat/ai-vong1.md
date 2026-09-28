# Cửa mặt Ida A-i — kiểm mù vòng 1 (28/09/2026, khoảng 11:45 UTC)

Bản thử: gói W3 @8ebf3ef (nhánh `worktree-agent-a83d4075f6a9542ef`). Mặt điêu khắc trong lưới (`facerig.js`), bỏ `facepaint`, rig 16 kênh + 6 khẩu hình, nhãn cầu riêng, da PBR chuyển sắc, 79 lọn tóc.
Khung: s37 layout (facelight 'gas', f2302) cho 3 biểu cảm; s39 khung 2531 (câu thoại cuối, biểu cảm của layout); clip 3 s s37 f2266–2337 (2 lần chớp + khẩu hình "Goodnight"), cắt 6 khung k = 0, 8, 22, 36, 45, 64. Kích thước 1920×1080.
Quy trình: P đổi tên ngẫu nhiên từng ảnh và đặt vào scratchpad. Mỗi ảnh giao cho một subagent MỚI, không có ngữ cảnh, chỉ được mở một file. Câu hỏi y như mọi lần: "Người này bao nhiêu tuổi, giới tính gì, đang cảm thấy gì? Nêu thêm điều gì người xem có thể thấy lạ trong ảnh (nếu có)." Cùng đợt có 2 khung Sprite Fright đối chứng (REF-SF-HC, 104,5 s và 332 s; khung đối chứng không commit), cũng mỗi khung một subagent mới.
Tiêu chí đạt (chủ dự án, quyết định sau Cổng 5 v2): 4/4 ảnh đọc ra phụ nữ lớn tuổi; ≥ 3/4 cảm xúc đúng; số lần bị gọi "búp bê/mặt nạ/con rối" không quá mẫu đối chứng.

## Kết quả

| Ảnh | Đích | Tuổi / giới đọc được | Cảm xúc đọc được | Đúng? | "búp bê / mặt nạ / con rối" (và "ma-nơ-canh") |
|---|---|---|---|---|---|
| anh_neutral | trung tính | nữ 65–75 | "buồn, mệt mỏi… Biểu cảm hơi đơ, giống mặt đang nghỉ" | ✔ (sát biên) | có: "mặt nạ cao su hoặc sáp đang chảy" |
| anh_sad_smile | cười buồn | nữ 70–80 | "buồn, hơi tủi thân hoặc sắp khóc" (không đọc ra nụ cười) | ✘ | có: "giống mặt búp bê" |
| anh_choked | nghẹn | nữ 65–75 | "buồn… như đang cố nén khóc" | ✔ | có: "mặt nạ dán lên đầu", "búp bê hoặc ma-nơ-canh" |
| anh_s39 (câu thoại cuối) | nghẹn | nữ 65–75 | "buồn, chán nản và hơi hờn dỗi" | ✔ (đúng hướng buồn, không đọc ra nén khóc) | có: "búp bê hoặc hình nộm", "như một cái mặt nạ" |
| clip k0 | chớp mắt / thoại | nữ 65–80 | buồn, sắp khóc | — | có: "con rối hoặc ma-nơ-canh" |
| clip k8 | mắt nhắm | nữ 65–75 | buồn, mệt, nén xúc động | — | có: "búp bê hoặc ma-nơ-canh" |
| clip k22 | khẩu hình | nữ 65–75 | buồn, mệt, "hơi trống" | — | không (có: "gương mặt nhựa", miệng "như vết lem") |
| clip k36 | khẩu hình | nữ 65–75 | buồn, đau khổ | — | có: "như mặt nạ, giống búp bê" |
| clip k45 | khẩu hình | nữ 65–75 | buồn, mệt, thất vọng | — | có: "mặt nạ nhựa", "kiểu búp bê" |
| clip k64 | cuối câu | nữ 65–75 | buồn, cam chịu | — | có: "chiếc mặt nạ dán lên đầu" |
| **Đối chứng SF 104,5 s** | — | bé gái 10–13 | bối rối, lo lắng | — | **không** |
| **Đối chứng SF 332 s** | — | nữ 40–50 | giận dữ, chống cự | — | **không** |

**Tổng:**
- Phụ nữ lớn tuổi: **4/4 ✔**, và cả 6/6 khung clip.
- Cảm xúc đúng: **3/4 ✔**, trong đó ảnh trung tính sát biên và "cười buồn" không đọc ra.
- Số lần bị gọi búp bê, mặt nạ hoặc con rối: Ida **4/4 ảnh cộng 5/6 khung clip (9/10)**; đối chứng **0/2** → **TRƯỢT** tiêu chí 3.

**Kết luận vòng 1: TRƯỢT.** Còn 1 vòng, là vòng cuối.

## Lời chê gom nhóm (đếm TAY trên 10 ảnh Ida; số đếm bằng máy chuẩn hơn, xem bảng ở `ai-vong2.md`)
1. **Da nhựa hoặc sáp, không nếp, cam gắt: 10/10.** Tuổi chỉ đọc qua tóc bạc.
2. **Nửa dưới mặt phình, méo, "chảy" (hàm, cằm hình quả lê, miệng như cao su): 9/10.**
3. **Mặt như mặt nạ dán lên, ranh da với tóc cắt sắc ở trán và thái dương: 7/10.**
4. **Cổ dài, mảnh như cột, có mảng bóng răng cưa (lỗi bóng đổ): 8/10.**
5. **Tóc như dải giấy, nhựa hoặc đất nặn; mũ lơ lửng không ôm đầu: 8/10.**
6. **Mũi vẹo, có chấm tròn dưới cánh mũi (đọc thành khuyên mũi hoặc cục u): 7/10.**
7. **Hoa tai lệch độ cao, treo cạnh má, không thấy tai: 7/10.**
8. **Hai mắt không cân, nhìn "lác": 4/10.**
9. Vật cong màu cam ở góc dưới trái (đèn lồng ngoài khung), gây phân tâm: 8/10. Đây là chuyện khung hình, không phải mặt.

## Nguyên văn
### anh_neutral — file mù `6cd8508e.jpg` — nguyên văn

> Tôi chỉ mở đúng một file ảnh: /tmp/claude-0/-home-user-cine-lab/5b95043d-dd86-5cf7-9b06-17de07cfe1f8/scratchpad/matai/v1/6cd8508e.jpg. Không mở hay tìm file nào khác.
>
> Nhận xét dưới góc nhìn người xem bình thường:
>
> **Tuổi:** Khoảng 65–75. Tóc bạc trắng, búi gọn nên nhìn là biết một người lớn tuổi. Tuy vậy, trừ quầng dưới mắt thì da mặt gần như phẳng, không có nếp nhăn, nên nếu chỉ nhìn khuôn mặt thì trông trẻ hơn mái tóc.
>
> **Giới tính:** Nữ, là một bà cụ. Các dấu hiệu là bông tai hạt tròn màu vàng, kiểu tóc búi, mũ rộng vành và khăn len quấn cổ màu đỏ gạch.
>
> **Cảm xúc:** Buồn, mệt mỏi, có phần thất vọng hoặc cam chịu. Mí mắt trên sụp xuống che nửa tròng, ánh mắt nhìn xuống lệch sang một bên. Môi mím thành một đường ngang, khoé miệng hơi trễ xuống. Nhìn cũng có thể hiểu là hoài nghi hoặc không vui, nhưng "buồn, mệt" là cảm nhận đầu tiên. Biểu cảm hơi đơ, giống mặt đang nghỉ hơn là một cảm xúc đang diễn ra.
>
> **Những điểm người xem có thể thấy lạ:**
> 1. **Hai mắt không cân.** Mắt trái (phía người xem) to, tròn và nằm thấp hơn. Mắt phải hẹp và cao hơn. Hai mắt cũng như đang nhìn hai hướng hơi khác nhau, nên mặt trông lệch hoặc lác.
> 2. **Mũi dị dạng.** Sống mũi có vết lõm hoặc gấp khúc như bị méo. Đầu mũi tròn, lệch và trông như dính thêm vào. Lỗ mũi bên phải có một chấm tròn nhỏ trông như cục u, lạ hơn nhiều so với một chiếc khuyên mũi.
> 3. **Miệng và cằm như bị bóp méo.** Môi gần như không có hình dạng rõ, giống một vết cắt ngang. Nửa dưới mặt bị kéo dài và thuôn nhọn, cằm to và phình như quả lê. Cả khuôn mặt trông như mặt nạ cao su hoặc sáp đang chảy.
> 4. **Ranh giới tóc và trán cắt cứng.** Mảng tóc úp lên đầu như một cái mũ hoặc bộ tóc giả, không mọc ra từ da đầu. Tóc có dạng các dải trắng như giấy hoặc đất nặn và hầu như không nhận ánh sáng cam giống da mặt.
> 5. **Cổ có vết loang lạ.** Ngay trên khăn len có những mảng sáng tối viền răng cưa, trông như vết rách hoặc lỗi bóng đổ.
> 6. **Tai và bông tai.** Tai phải gần như không thấy rõ hình dạng, bông tai như cắm thẳng vào da. Hai bông tai cũng nằm ở hai độ cao khác nhau.
> 7. **Ánh sáng.** Da mặt cam rực như dưới đèn sân khấu hoặc ánh lửa, trong khi tóc vẫn trắng lạnh. Nền đen kịt và góc dưới trái có một vệt cam lạ.
>
> **Tổng thể:** Tạo hình vẫn đọc được là một bà cụ đang buồn hoặc mệt. Nhưng khuôn mặt méo, không cân xứng và có chất "sáp chảy", nên người xem dễ thấy hơi rợn (hiệu ứng thung lũng kỳ lạ) hơn là thấy thương cảm. Phần méo mó nặng nhất là mũi, miệng và cằm, tiếp theo là hai mắt không cân.

### anh_sad_smile — file mù `75c7f6b1.jpg` — nguyên văn

> Tôi đã mở đúng một file ảnh: 75c7f6b1.jpg. Dưới đây là cảm nhận của tôi khi xem như một người xem bình thường.
>
> **Tuổi:** Đây là một bà cụ, khoảng 70–80 tuổi. Tóc bà bạc trắng, búi gọn, và mặt có vài nếp nhăn nhẹ ở trán, quanh mắt và khoé miệng.
>
> **Giới tính:** Nữ. Bà đeo hoa tai vàng hình quả tròn thả, đội mũ phớt vành rộng và quàng khăn len đỏ.
>
> **Cảm xúc:** Bà có vẻ buồn, hơi tủi thân hoặc sắp khóc, cũng có thể là đang thất vọng. Lông mày nhướn lên ở phía trong, mắt nhìn chếch xuống. Môi mím lại, khoé miệng trễ xuống, cằm hơi nhăn như đang cố nén cảm xúc. Nếu nói ngắn gọn thì đó là một nỗi buồn lặng lẽ, kìm nén.
>
> **Những điểm người xem có thể thấy lạ:**
> 1. **Miệng và cằm méo:** Cả vùng miệng lệch hẳn sang một bên và phồng như bị bóp. Môi dưới cũng như bị kéo lệch, trông giống lỗi biến dạng hơn là một biểu cảm tự nhiên.
> 2. **Cằm và gò má sưng:** Hai bên cằm phồng tròn, căng bóng như bị sưng, còn gò má lại hơi móp. Phần dưới khuôn mặt vì thế trông to và nặng bất thường.
> 3. **Mũi lệch:** Sống mũi hơi cong và lệch, cánh mũi hai bên không đều nhau.
> 4. **Da quá láng, như nhựa hay sáp:** Làn da trơn bóng, không có kết cấu. Màu cam đỏ rất gắt, nhìn giống mặt búp bê hơn là da người già.
> 5. **Cổ dài và mảnh:** Cổ dài quá mức so với đầu. Chỗ cổ nối vào cằm và vào khăn trông không tự nhiên.
> 6. **Mảng bóng cứng ở cổ:** Chỗ cổ gặp khăn có một mảng tối viền răng cưa, giống lỗi đổ bóng hoặc một mảng bị cắt.
> 7. **Tóc và da đầu tách rời:** Tóc trông như một khối đúc cứng, có vân như tượng. Đường chân tóc chỗ trán bị cắt thẳng, lộ phần da đầu trơn phía dưới, trông như tóc là một cái mũ úp lên đầu.
> 8. **Mắt hơi to và bóng, hai mắt không cân:** Mắt bên phải (theo góc nhìn người xem) mở to hơn mắt bên kia.
> 9. **Hai hoa tai lệch nhau:** Hoa tai bên phải treo cao hơn hẳn bên trái.
> 10. **Vật lạ ở góc trái dưới:** Có một vật cong phát sáng màu cam, không rõ là gì.
>
> **Ấn tượng chung:** Cảm xúc buồn vẫn đọc ra được. Nhưng vùng miệng và cằm méo cùng làn da nhựa bóng khiến khuôn mặt hơi kỳ dị. Người xem dễ thấy bà cụ "lạ", thậm chí hơi đáng sợ, hơn là thấy thương cảm.

### anh_choked — file mù `fbc83dee.jpg` — nguyên văn

> Tôi chỉ mở đúng một file: /tmp/claude-0/-home-user-cine-lab/5b95043d-dd86-5cf7-9b06-17de07cfe1f8/scratchpad/matai/v1/fbc83dee.jpg. Không mở hay tìm file nào khác.
>
> **Nhìn như một người xem bình thường:**
>
> - **Tuổi:** một bà cụ, khoảng 65–75 tuổi. Tôi đoán vậy chủ yếu vì tóc bạc trắng. Da mặt lại căng, gần như không có nếp nhăn, nên nếu che tóc đi thì khó đoán tuổi.
> - **Giới tính:** nữ. Tôi dựa vào hoa tai ngọc tròn màu vàng đồng, kiểu tóc uốn ngắn của người lớn tuổi, mũ vành và khăn len quàng cổ.
> - **Cảm xúc:** buồn, thất vọng, hơi tủi hoặc sắp khóc. Lông mày nhướng lên ở giữa, mí mắt sụp, mắt nhìn xuống và sang một bên. Miệng mím, cong xuống, môi dưới hơi đẩy lên như đang cố nén khóc. Cảm giác chung là buồn lặng lẽ và cam chịu.
>
> **Những điểm người xem có thể thấy lạ:**
>
> 1. **Mặt như cái mặt nạ dán lên đầu.** Mặt có viền cong rõ tách khỏi tóc và tai, ở trán và thái dương trông như một miếng da dán lên. Tai nằm tận sau tóc, lệch khỏi khuôn mặt.
> 2. **Da quá láng, không có nếp nhăn.** Da mịn như nhựa hay sáp, màu cam bóng, không khớp với tóc bạc. Nhìn giống búp bê hoặc ma-nơ-canh hơn là một bà cụ.
> 3. **Cằm và hàm phồng, méo.** Nửa dưới mặt to, phình tròn như túi. Vùng miệng và cằm như bị bơm căng, nên biểu cảm buồn trông hơi kỳ và hơi hài.
> 4. **Cổ dài, gầy như cái que.** Cổ nhỏ hơn hẳn so với cái đầu to, lại có vệt sáng hoặc bóng loang lổ, cạnh răng cưa, trông như lỗi hiển thị.
> 5. **Mũi có chỗ lõm hoặc gãy ở sống mũi,** và cánh mũi hơi lệch.
> 6. **Tóc giống đất nặn hoặc giấy xếp lớp,** màu trắng xám hơi xanh, sáng lạnh, lệch tông với ánh sáng cam ấm trên mặt.
> 7. **Hai hoa tai không cân nhau.** Một bên buông dưới dái tai, bên kia gắn cao ngang má, như mọc ra từ tóc.
> 8. **Góc dưới bên trái có một vệt cong sáng màu cam,** nhìn không rõ là vật gì.
>
> **Tóm lại:** người xem vẫn đọc ra ngay "một bà cụ đang buồn". Nhưng khuôn mặt dễ gây cảm giác "rợn" kiểu thung lũng kỳ lạ (uncanny valley). Lý do là da mặt quá trơn so với tuổi, mặt tách khỏi đầu như mặt nạ, hàm và cằm phồng méo, cổ quá mảnh và có lỗi bóng hoặc sáng.

### anh_s39 — file mù `1d814b45.jpg` — nguyên văn

> Tôi chỉ mở đúng một file ảnh là /tmp/claude-0/-home-user-cine-lab/5b95043d-dd86-5cf7-9b06-17de07cfe1f8/scratchpad/matai/v1/1d814b45.jpg, không mở file nào khác. Dưới đây là cảm nhận của một người xem bình thường.
>
> **Tuổi và giới tính:** Đây là một bà cụ, tức là nữ, chắc khoảng 65 đến 75 tuổi. Tôi đoán vậy vì bà có tóc bạc trắng búi gọn, lông mày bạc, đeo khuyên tai vàng hình hạt tròn, đội mũ rộng vành màu nâu sẫm và quàng khăn len đỏ gạch.
>
> **Cảm xúc:** Bà trông buồn, chán nản và hơi hờn dỗi hay thất vọng. Người xem nhận ra ngay nhờ các dấu hiệu sau:
> - Hai mí mắt trên sụp xuống nửa chừng, mắt nhìn xuống.
> - Đầu trong lông mày hơi nhướng lên, tạo vẻ buồn.
> - Miệng mím và trễ hẳn xuống thành hình chữ "n" úp ngược, môi dưới hơi bĩu ra.
> Nhìn chung là vẻ "buồn thiu, tủi thân" hoặc "ngán ngẩm". Nét mặt không giống giận dữ.
>
> **Những điểm người xem có thể thấy lạ:**
> 1. **Hình dạng đầu:** Mặt rất to, tròn và phình như quả bóng hay quả lê, cằm và má dưới phình ra. Cổ lại dài và mảnh như cái que. Tỉ lệ đầu, mặt và cổ trông thiếu tự nhiên, gần như đầu được cắm trên một cái cột.
> 2. **Da mặt:** Da trơn láng như nhựa hay sáp, gần như không có nếp nhăn. Điều này không khớp với tóc bạc và tuổi già, nên bà trông giống búp bê hoặc hình nộm hơn là người thật.
> 3. **Vùng miệng và cằm:** Chỗ này bị kéo méo như cao su. Khoảng cách từ mũi xuống miệng và từ miệng xuống cằm dài bất thường, tạo cảm giác mặt đang bị "chảy" xuống.
> 4. **Chỗ tiếp giáp giữa mặt và tóc:** Mép mặt cắt thẳng vào khối tóc, như một cái mặt nạ úp lên đầu. Hai bên thái dương và tai trông như tách rời khỏi mặt.
> 5. **Tóc:** Tóc là những dải trắng đặc, giống nhựa hoặc đất nặn, không có cảm giác sợi tóc thật.
> 6. **Bối cảnh:** Phông nền xám phẳng và trống. Bên trái có một cột gỗ và một khối vàng cam bị cắt dở ở mép khung hình. Cảnh trông giống một góc sân khấu hoặc bối cảnh chưa hoàn thiện.
>
> **Tóm lại:** Ai nhìn cũng hiểu ngay đây là một bà cụ đang buồn hoặc thất vọng. Nhưng khuôn mặt phình, cổ que và da nhựa khiến nhân vật gây cảm giác hơi kỳ quái, dễ rơi vào vùng "thung lũng kỳ lạ" (uncanny valley), nhiều hơn là dễ thương.

### clip_k0 — file mù `ea06afcb.jpg` — nguyên văn

> Tôi đã xem đúng một file ảnh: /tmp/claude-0/-home-user-cine-lab/5b95043d-dd86-5cf7-9b06-17de07cfe1f8/scratchpad/matai/v1/ea06afcb.jpg
>
> Ảnh là khung hình 3D của một nhân vật hoạt hình cận mặt, trên nền tối, được chiếu một nguồn sáng ấm màu cam.
>
> **Tuổi:** Là người lớn tuổi, khoảng 65–80 tuổi. Tôi đoán vậy vì tóc bạc trắng và vùng dưới mắt hơi trũng. Nhưng da mặt quá căng và mịn, gần như không có nếp nhăn, nên nếu chỉ nhìn da mặt thì trông trẻ hơn nhiều.
>
> **Giới tính:** Là nữ, một bà cụ. Tôi đoán vậy vì bà đeo khuyên tai dài có hạt tròn màu vàng đồng, tóc ngắn uốn bạc, đội mũ phớt và quàng khăn len đỏ.
>
> **Cảm xúc:** Buồn, thất vọng, có chút chán nản hoặc cam chịu. Hai khoé miệng trễ xuống thành hình chữ U ngược. Mí mắt trên sụp xuống che nửa tròng. Mắt nhìn xuống và hơi lệch sang một bên. Lông mày hơi nhướng ở đầu trong. Tổng thể giống như đang dỗi hoặc sắp khóc. Nét mặt hơi bị cường điệu nên có lúc trông như hờn dỗi hơn là buồn sâu.
>
> **Những điểm người xem có thể thấy lạ:**
> 1. **Tỉ lệ đầu và cổ bất thường:** Mặt dài, hẹp dần xuống cằm như hình quả trứng lộn ngược. Cổ rất dài, thẳng như ống, trông giống con rối hoặc ma-nơ-canh.
> 2. **Sống mũi bị cong lệch:** Mũi xiêu vẹo sang bên trái khung hình. Đầu mũi có một chấm nhỏ sẫm màu như mụn hoặc lỗi bề mặt.
> 3. **Hai mắt không đối xứng:** Mắt trái (bên phải khung hình) nằm cao hơn và mở to hơn một chút. Hai mắt nhìn không cùng hướng, làm ánh nhìn hơi "lác".
> 4. **Miệng bị méo:** Môi dưới phồng, nhô ra, trông như cao su bị kéo. Vùng má và cằm quanh miệng có những vết lõm và gồ khó hiểu.
> 5. **Mũ nằm sai chỗ:** Tóc lòi ra rất nhiều dưới vành mũ, mũ như lơ lửng phía trên chứ không ôm đầu.
> 6. **Tóc không giống tóc:** Tóc trông như những dải giấy hoặc sợi mì trắng xếp chồng lên nhau, không có độ mềm.
> 7. **Tai và khuyên tai:** Tai gần như bị tóc che mất. Khuyên tai như treo lơ lửng cạnh má. Hai chiếc cũng không đối xứng về độ cao.
> 8. **Bóng đổ trên cổ:** Cổ có một mảng bóng răng cưa sắc cạnh, trông giống lỗi đổ bóng hơn là bóng tự nhiên.
> 9. **Da mặt:** Da bóng như nhựa hoặc sáp, đổ màu cam gắt. Da quá căng, không khớp với tóc bạc của người già.
> 10. **Góc dưới bên trái:** Có một vật thể viền cam bị cắt ngang, không rõ là gì, dễ gây phân tâm.
>
> Nhìn chung, nhân vật đọc ra được là một bà cụ đang buồn. Nhưng khuôn mặt có nhiều chỗ méo và bất đối xứng khiến ảnh hơi rơi vào cảm giác "thung lũng kỳ lạ" (uncanny), đáng sợ hơn là đáng thương.

### clip_k8 — file mù `18d68efd.jpg` — nguyên văn

> Tôi đã xem ảnh /tmp/claude-0/-home-user-cine-lab/5b95043d-dd86-5cf7-9b06-17de07cfe1f8/scratchpad/matai/v1/18d68efd.jpg. Ngoài ảnh này, tôi không mở file nào khác.
>
> **Tuổi:** Là người xem, tôi đoán đây là một bà cụ khoảng 65–75 tuổi. Chỗ gợi tuổi chủ yếu là mái tóc bạc trắng và cách ăn mặc: mũ phớt, khăn len quàng cổ, hoa tai ngọc.
>
> **Giới tính:** Nữ.
>
> **Cảm xúc:** Buồn và mệt mỏi, như đang cam chịu hoặc nhớ tiếc điều gì. Mắt bà nhắm hoặc gần nhắm, khoé miệng trễ xuống, môi dưới hơi bĩu, đầu hơi cúi. Cũng có thể hiểu là bà đang cố nén xúc động. Nhìn chung cảm xúc đọc được khá rõ, nghiêng về u buồn chứ không phải đang ngủ yên.
>
> **Những điểm người xem có thể thấy lạ:**
> 1. **Da quá láng, trông như nhựa hoặc sáp.** Da bóng và căng, gần như không có nếp nhăn. Điều này không khớp với mái tóc bạc, nên tuổi trông mâu thuẫn: tóc nói "già", còn da mặt nói "trẻ" hoặc "búp bê".
> 2. **Hình dáng mặt kỳ.** Mặt phình rộng ở má và hàm dưới rồi thu thẳng vào một cái cổ to, dài như ống. Nhìn giống một khối nặn hơn là mặt người, hơi giống ma-nơ-canh.
> 3. **Tai và hoa tai.** Hoa tai bên trái khung hình như mọc ra từ má hoặc hàm, không thấy tai đâu. Bên phải thì tai trông nhọn và nhập vào tóc.
> 4. **Tóc như đất sét hoặc gỗ tạc.** Tóc là những dải thô xếp chồng. Ánh sáng làm tóc trắng loá và nó kết thúc khá đột ngột dưới vành mũ. Chiếc mũ trông như đặt lơ lửng phía trên chứ không ôm đầu.
> 5. **Mắt.** Mí mắt to, bóng, không có lông mi. Vùng quanh mắt hơi ánh xanh tím, trông như mắt lồi dưới lớp mí hơn là mắt nhắm tự nhiên.
> 6. **Chấm tối nhỏ ở cánh mũi bên trái khung hình.** Trông như một vết lỗi hoặc cái lỗ trên bề mặt.
> 7. **Ánh sáng.** Đèn cam gắt từ trên chiếu thẳng khiến mặt đỏ cam đều. Vệt bóng trên cổ có mép rất sắc, như bị cắt. Ở góc dưới bên trái có một vật viền cam bị cắt, không rõ là gì.
>
> **Tóm lại:** Cảm xúc buồn, mệt đọc được ngay. Nhưng khuôn mặt tạo cảm giác "búp bê hoặc ma-nơ-canh" hơi rợn, chủ yếu vì da nhựa, hình khối mặt và cổ, tai và hoa tai sai chỗ, và mắt không lông mi.

### clip_k22 — file mù `c6949c2e.jpg` — nguyên văn

> Tôi đã mở và xem đúng một file: /tmp/claude-0/-home-user-cine-lab/5b95043d-dd86-5cf7-9b06-17de07cfe1f8/scratchpad/matai/v1/c6949c2e.jpg. Không mở file nào khác.
>
> **Tuổi, giới tính, cảm xúc (theo cảm nhận của người xem bình thường)**
> - **Giới tính:** nữ. Nhìn là biết ngay nhờ đôi hoa tai ngọc, khăn len quàng cổ và mái tóc ngắn uốn.
> - **Tuổi:** người già, khoảng 65–75. Chủ yếu đoán qua mái tóc bạc trắng và bọng dưới mắt, vì da mặt lại căng và trẻ hơn tuổi đó.
> - **Cảm xúc:** buồn, mệt, có vẻ cam chịu hoặc đang nhớ chuyện gì. Lông mày chùng xuống, mí mắt nặng, mắt nhìn xuống lệch sang một bên. Miệng hé như sắp nói hoặc đang nén khóc. Cảm xúc đọc ra được, nhưng hơi "trống", giống ánh mắt đờ đẫn hơn là nỗi buồn sâu.
>
> **Những điểm người xem có thể thấy lạ**
> 1. **Cái miệng là điểm lạ nhất.** Vùng môi trông như bị nhoè, bị kéo méo, giống vết lem hơn là đôi môi thật. Nó nằm hơi thấp, bè ngang, viền không rõ, bên trong lộ ra một khe tối lởm chởm. Người xem dễ thấy khó chịu hoặc thấy "hỏng".
> 2. **Hình dáng đầu:** mặt thuôn như quả trứng hay quả bóng, cằm nhọn nhỏ, cổ dài và mảnh bất thường so với đầu.
> 3. **Da mặt quá phẳng và bóng so với tuổi:** gần như không có nếp nhăn, trông như sáp hoặc nhựa. Nó không khớp với mái tóc bạc.
> 4. **Chiếc mũ như lơ lửng:** vành mũ rất rộng và có vẻ không đặt lên tóc, như đang trôi phía trên đầu.
> 5. **Tóc** trông như những dải giấy hoặc nét cọ cứng, không giống sợi tóc.
> 6. **Hoa tai:** chiếc bên trái (phía người xem) như treo lơ lửng cạnh má, không thấy dính vào tai. Hai chiếc lại ở hai độ cao khác nhau. Tai bên phải thì nhọn và có hình dạng lạ.
> 7. **Mũi** hơi sần, lồi lõm, vùng lỗ mũi trông không tự nhiên.
> 8. **Bóng đổ trên cổ** có mép cứng và răng cưa, nhìn như lỗi hình chứ không như bóng thật. Trên má phải có một mảng sẫm hình bầu dục như vết ố.
> 9. **Ánh sáng** cam rất gắt từ phía dưới bên trái, làm mặt đỏ cam như đang đứng cạnh lửa. Không khí đẹp, nhưng góc trái dưới có một vệt viền cam của vật gì đó bị cắt dở, khó hiểu.
>
> **Tổng thể:** người xem nhận ra ngay đây là một bà cụ đang buồn. Nhưng cái miệng méo, gương mặt nhựa và các chi tiết lơ lửng (mũ, hoa tai) có thể gây cảm giác "rợn" hoặc "lỗi kỹ thuật" nhiều hơn là xúc động.

### clip_k36 — file mù `facea6c6.jpg` — nguyên văn

> Tôi chỉ mở đúng một ảnh: /tmp/claude-0/-home-user-cine-lab/5b95043d-dd86-5cf7-9b06-17de07cfe1f8/scratchpad/matai/v1/facea6c6.jpg. Dưới đây là cảm nhận của một người xem bình thường.
>
> **Tuổi:** Là người lớn tuổi, khoảng 65–75. Tóc bạc trắng, má và cằm hơi chảy xuống, dưới mắt có nếp.
>
> **Giới tính:** Nữ, trông như một bà cụ. Bà đeo khuyên tai hạt tròn màu vàng, quàng khăn len đỏ gạch, đội mũ phớt vành rộng màu tối.
>
> **Cảm xúc:** Buồn, lo âu, có phần đau khổ hoặc bàng hoàng. Lông mày nhướng lên và chụm vào giữa, mắt sụp và nhìn xuống lệch sang một bên, miệng há như đang than thở hoặc sắp khóc. Tôi chắc chừng 70% là buồn hoặc đau khổ. Cũng có thể đọc thành ngạc nhiên hoặc hụt hẫng, vì miệng há khá to.
>
> **Những điểm có thể thấy lạ:**
> 1. **Khuôn mặt trông như mặt nạ, giống búp bê hoặc đất sét.** Da trơn láng, không có lỗ chân lông hay nếp nhăn nhỏ. Vùng mặt như một tấm dán lên đầu: mép mặt gặp tóc thành một đường ranh rõ ở trán và thái dương, nên trông giống đeo mặt nạ.
> 2. **Mũi hơi lệch và méo.** Sống mũi không thẳng, đầu mũi to lệch sang trái (so với người xem). Dưới mũi có một chấm nhỏ màu vàng hoặc cam, trông như khuyên mũi hoặc một vết lỗi.
> 3. **Miệng méo, cằm dài.** Miệng há kiểu hình bầu dục, môi dưới dày và trễ, khoé miệng lệch. Phần cằm và hàm dưới kéo dài, khiến nửa dưới khuôn mặt bị chảy xuống không tự nhiên.
> 4. **Tai có vẻ sai vị trí.** Khuyên tai bên trái (so với người xem) nằm sát má, gần như không thấy tai. Tai bên phải thì mọc lẫn vào trong tóc.
> 5. **Tóc trông như thạch cao hoặc giấy xếp lớp.** Tóc là những mảng trắng dẹt như vỏ bào, không giống sợi tóc thật. Chiếc mũ như lơ lửng phía trên tóc, không ôm vào đầu.
> 6. **Cổ dài và mảnh so với đầu.** Cái cổ nhô lên từ khăn len như một khối trụ.
> 7. **Ánh sáng.** Toàn bộ mặt bị ánh cam gắt, gần như ánh lửa, chiếu từ phía trước bên trái. Nền đen hoàn toàn. Góc dưới bên trái có một vệt sáng cong màu cam, không rõ là vật gì.
>
> **Ấn tượng chung:** Đây rõ ràng là nhân vật hoạt hình 3D, không phải người thật. Cảm xúc buồn hoặc lo vẫn đọc được. Tuy vậy, khuôn mặt méo và giống mặt nạ gây cảm giác hơi rợn, kiểu "thung lũng kỳ lạ" (uncanny valley). Người xem dễ chú ý vào các lỗi hình dạng hơn là vào cảm xúc của nhân vật.

### clip_k45 — file mù `d3839e55.jpg` — nguyên văn

> Tôi đã mở đúng một file ảnh: `/tmp/claude-0/-home-user-cine-lab/5b95043d-dd86-5cf7-9b06-17de07cfe1f8/scratchpad/matai/v1/d3839e55.jpg`. Tôi không mở hay tìm file nào khác. Dưới đây là nhận xét của một người xem bình thường.
>
> **Tuổi:** Trông là một bà cụ, khoảng 65–75 tuổi. Người xem đoán như vậy vì tóc bạc trắng, mí mắt sụp, có túi mắt và má hơi chảy xệ.
>
> **Giới tính:** Nữ. Người xem nhận ra qua bông tai vàng dạng hai hạt tròn, tóc uốn ngắn kiểu bà cụ, mũ vành và khăn len quàng cổ màu đỏ gạch.
>
> **Cảm xúc:** Buồn, mệt mỏi và thất vọng, như đang cam chịu hoặc sắp khóc.
> - Đuôi lông mày cụp xuống.
> - Mí mắt nặng, ánh mắt nhìn chếch xuống.
> - Miệng hé, khoé môi trễ xuống.
>
> Cũng có thể đọc thành vẻ ngán ngẩm hoặc hờn dỗi nhẹ, nhưng cảm giác chung là buồn.
>
> **Những điều người xem có thể thấy lạ:**
> 1. **Mặt như chiếc mặt nạ nhựa hay sáp.** Da láng bóng, không có nếp nhăn thật, trông giống khuôn nhựa hơn là da người già. Tuổi chỉ đọc được qua tóc bạc và túi mắt; bản thân da mặt lại trông trẻ và căng.
> 2. **Hình khối đầu kỳ lạ.** Khuôn mặt hình quả lê ngược, cằm và hàm rất dài và thon nhọn. Trán hẹp, bị mũ và tóc đè thấp. Khuôn mặt trông như dán lên phía trước khối tóc, và ở hai bên thái dương mép da tiếp giáp tóc hơi lộ.
> 3. **Mũi lệch và có "vết" lạ.** Sống mũi hơi vẹo. Dưới lỗ mũi bên phải (phía trái khung hình) có một chấm nhỏ màu vàng, trông như khuyên mũi hoặc lỗi hình, không rõ là cố ý hay không.
> 4. **Mắt hai bên không cân.** Mắt trái (phía phải khung hình) mở to và nằm cao hơn mắt còn lại. Mắt lệch nhau nên nét mặt có phần khó chịu, không chỉ buồn thuần tuý.
> 5. **Tóc như sợi nhựa hay giấy xé.** Lọn tóc to, bẹt, trắng đục như đất sét hoặc giấy, trông giả so với độ bóng của da mặt. Chất liệu tóc và da không hợp nhau.
> 6. **Cổ dài và thẳng như cột.** Cổ dài bất thường, đổ thẳng xuống khăn len, và có một vệt bóng đổ sắc cạnh ngang cổ.
> 7. **Mũ lơ lửng.** Vành mũ rất rộng và nằm cao trên khối tóc. Trông như mũ không thật sự đội lên đầu mà trôi phía trên.
> 8. **Ánh sáng.** Nền đen kịt; mặt được chiếu bằng ánh cam gắt từ phía trước bên trái, nên da gần như cam đỏ. Bầu không khí ấm, nhưng khiến da trông càng giống sáp hoặc nhựa.
> 9. **Góc dưới bên trái có một vệt sáng vàng nhỏ ở mép khung.** Đó là một vật lạ, không rõ là gì.
>
> **Ấn tượng tổng thể:** Một nhân vật hoạt hình 3D kiểu búp bê hay đất sét, đọc ra được cảm xúc buồn và mệt. Tuy vậy, khuôn mặt rơi vào "vùng kỳ dị" (uncanny valley), hơi đáng sợ hoặc gây cảm giác khó chịu. Nguyên nhân là mặt quá láng, tỉ lệ đầu và cằm méo, mắt lệch, và tóc với da không cùng một chất liệu.

### clip_k64 — file mù `c270a36e.jpg` — nguyên văn

> Tôi đã mở đúng một file ảnh: /tmp/claude-0/-home-user-cine-lab/5b95043d-dd86-5cf7-9b06-17de07cfe1f8/scratchpad/matai/v1/c270a36e.jpg. Không mở file nào khác.
>
> **Nhìn như một người xem bình thường:**
>
> - **Tuổi:** Tôi đoán là một bà cụ, khoảng 65–75 tuổi. Tôi đoán vậy chủ yếu vì tóc trắng bạc, bọng mắt nặng và mí mắt sụp.
> - **Giới tính:** Nữ. Nhân vật đeo khuyên tai hạt tròn màu vàng đồng, đội mũ vành, mặc áo len cổ lọ.
> - **Cảm xúc:** Buồn, mệt mỏi, như cam chịu. Có thể bà đang nhớ ai đó hoặc vừa nghe tin không vui. Mắt nhắm hoặc nhìn xuống, lông mày hơi xếch lên ở giữa, khoé miệng trễ xuống. Tôi đọc được nỗi buồn khá rõ, không bị nhầm sang giận hay ngủ gật.
>
> **Những điểm người xem có thể thấy lạ:**
>
> 1. **Mặt trông như chiếc mặt nạ dán lên đầu.** Da mặt là một mảng trơn và bóng, ranh giới với tóc ở trán và thái dương sắc như viền mặt nạ. Tóc giống những dải ruy băng hay nhựa xếp lớp, không giống tóc thật.
> 2. **Hầu như không có cằm và đường hàm.** Mặt thuôn xuống như quả trứng hay cái bình rồi nối thẳng vào một chiếc cổ dài, gầy và trơn láng. Dáng đầu trông kỳ và hơi đáng sợ.
> 3. **Tuổi không khớp nhau.** Tóc bạc và bọng mắt là của người già, nhưng má, trán và cổ lại căng mịn, gần như không có nếp nhăn.
> 4. **Khuyên tai như lơ lửng.** Chiếc bên trái khung hình treo cạnh má mà gần như không thấy tai. Tai bên phải thì chìa ra khỏi mảng tóc khá gượng.
> 5. **Có vệt lạ trên mặt.** Gần khoé mắt phía phải khung hình (cạnh sống mũi) có một vệt ánh xanh tím. Dưới cánh mũi bên đó có một chấm tối, nhìn như lỗ hổng hoặc khuyên mũi.
> 6. **Miệng méo và các nếp quanh miệng như bị bóp.** Chúng trông giống lỗi biến dạng bề mặt hơn là nếp nhăn tự nhiên.
> 7. **Bóng đổ trên cổ cắt rất gắt và có răng cưa.** Ánh cam rất đậm làm cả khuôn mặt giống tượng sáp hay đất nặn hơn là da người.
>
> **Tóm lại:** Cảm xúc buồn đọc được rõ. Nhưng tạo hình khuôn mặt, nhất là việc mặt tách khỏi đầu như mặt nạ, cằm biến mất vào cổ và tuổi không khớp, dễ làm người xem thấy rợn (thung lũng kỳ lạ) và bị kéo ra khỏi câu chuyện.

### doichung_sf_104.5 — file mù `9bfaffe1.png` — nguyên văn

> Tôi đã xem đúng một file: /tmp/claude-0/-home-user-cine-lab/5b95043d-dd86-5cf7-9b06-17de07cfe1f8/scratchpad/matai/v1/9bfaffe1.png. Tôi không mở hay tìm file nào khác.
>
> **Nhận xét của một người xem bình thường**
>
> - **Tuổi:** Một bé gái khoảng 10–13 tuổi, tức độ tuổi cuối tiểu học hoặc đầu trung học cơ sở. Mặt bé tròn, người nhỏ, tay ôm cuốn sổ ghi chép mà trên bìa đọc được chữ "…ology", nhiều khả năng là "Biology".
> - **Giới tính:** Nữ. Có thể nhận ra qua tóc buộc đuôi ngựa với dây buộc màu xanh ngọc, bông tai tròn to màu hồng và nét mặt.
> - **Cảm xúc:** Bé đang bối rối, lo lắng xen lẫn ngạc nhiên. Lông mày nhướng lên và chụm vào giữa, mắt mở to liếc lên phía trên bên phải, miệng hé chữ "o". Hai tay ôm chặt cuốn sổ trước ngực như để tự trấn an. Cảm giác chung là bé đang hơi sợ hoặc không chắc chắn trước điều gì đó vừa nghe hay vừa thấy, kiểu "Hả? Thật sao?".
>
> **Những điểm người xem có thể thấy lạ**
>
> 1. **Búi đuôi ngựa to và cứng một cách bất thường.** Nó dựng ngược lên cao hơn cả đầu rồi cong xuống như một cái đuôi động vật, trông nặng và đứng yên như tượng. Đây là điểm gây chú ý nhất.
> 2. **Chất liệu tóc ở đuôi ngựa khác hẳn phần tóc trên đầu.** Tóc trên đầu mịn, liền khối kiểu hoạt hình. Còn đuôi ngựa lại có sợi lởm chởm và ngọn ngả màu xám bạc, nhìn như lông thú hoặc cọ vẽ. Hai kiểu này đặt cạnh nhau trông không ăn khớp, như thể đuôi tóc được ghép từ nguồn khác vào.
> 3. **Đuôi ngựa có vẻ không gắn vào đầu.** Nó như lơ lửng tách ra phía sau, gốc tóc chỗ dây buộc không nối mượt với phần tóc trên đầu.
> 4. **Ánh mắt hơi lệch.** Hai con ngươi nhìn lên cùng hướng nhưng trông hơi lác nhẹ, đúng chất hoạt hình nhưng có thể khiến người xem thấy "ngơ".
> 5. **Chi tiết nhỏ.** Chiếc đồng hồ nhựa vàng đỏ trên cổ tay khá to và nổi. Bối cảnh là rừng tối có nấm đỏ, cho cảm giác hơi huyền ảo, bí ẩn.
>
> **Lưu ý thêm cho phiên điều phối:** Khung hình có chất lượng dựng hình, ánh sáng và phong cách giống ảnh cắt từ một phim hoạt hình 3D thương mại của studio lớn. Tôi không xác định được nguồn và không tra thêm. Nếu đây là ảnh tham chiếu bên ngoài thì nên đối chiếu với luật không sao chép nhân vật hay thiết kế của phim tham chiếu, và ghi vào RIGHTS.md.

### doichung_sf_332 — file mù `2258669e.png` — nguyên văn

> Tôi đã xem đúng một file: /tmp/claude-0/-home-user-cine-lab/5b95043d-dd86-5cf7-9b06-17de07cfe1f8/scratchpad/matai/v1/2258669e.png. Không mở file nào khác.
>
> Nhận xét như một người xem bình thường:
>
> **Tuổi và giới tính:** Đây là một nhân vật hoạt hình 3D, trông là phụ nữ trung niên, khoảng 40 đến 50 tuổi. Tôi đoán vậy vì cô trang điểm đậm kiểu thập niên 80 (phấn mắt xanh tím, son tím), đeo khuyên tai hình học to, vòng cổ chuỗi hạt, tóc vàng rối, và khuôn mặt có nét từng trải.
>
> **Cảm xúc:** Cô đang rất giận dữ, hoặc đang gắng sức chống cự. Mắt nhắm chặt, lông mày nhíu sâu xuống sống mũi, miệng há rộng nhe răng như đang gầm hay hét. Bàn tay giơ lên, lòng bàn tay hướng ra ngoài, như đang đẩy hoặc chặn một thứ gì đó. Người xem sẽ đọc cảnh này là cô vừa tức giận vừa hoảng, như đang kháng cự một lực hay một mối đe doạ.
>
> **Những điểm người xem có thể thấy lạ:**
> - Dưới mắt có mảng đen loang như mascara bị nhoè hoặc vệt bóng tối. Ta không rõ đó là trang điểm chảy, là bóng của lông mi hay là lỗi đổ bóng. Mảng này làm mặt trông bẩn, không có chủ ý rõ ràng.
> - Lông mi vẽ nằm phía trên mí mắt đang nhắm, trông hơi giống hình dán hơn là lông mi thật.
> - Mặt rất tròn, gần như hình quả trứng, và bị nghiêng mạnh. Gần như không thấy cổ, nên đầu như tách khỏi thân.
> - Ở má dưới và cằm có vài vết xước hoặc sợi tóc mảnh. Khó biết đó là vết thương hay là tóc lạc.
> - Răng lệch, có chỗ hở. Có lẽ đây là chủ ý tạo tính cách, nhưng dễ gây chú ý.
> - Bàn tay to và nhoè so với mặt, vì mờ chuyển động hoặc lấy nét nông. Tay trông hơi phồng, như cao su.
> - Toàn cảnh tối, ánh sáng xanh lạnh có sương mờ, và mép khung bị mờ. Ta không rõ nhân vật đang ở đâu và đang đối mặt với cái gì.
