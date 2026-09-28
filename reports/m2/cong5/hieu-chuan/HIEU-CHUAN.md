# Hiệu chuẩn phép kiểm mù mặt (Cổng 5 v2, 28/09/2026 04:50–04:52)

Quyết định chủ dự án sau Cổng 5 (A-α + hiệu chuẩn). Nguồn tham chiếu: **"Sprite Fright"** © Blender Foundation | studio.blender.org — CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/); file 804p từ archive.org (`RIGHTS.md` REF-SF, REF-SF-HC; SHA-256 `85af52d5…a9acfd076`). **Chỉ dùng hiệu chuẩn nội bộ, không đưa vào phim; khung không commit vào repo.**

Cách làm: chọn 4 khung cận/trung cận mặt nhân vật người (cỡ cảnh gần khung Ida MCU/CU), gồm 2 cảnh đêm ánh lạnh để gần điều kiện ánh sáng của Ida. Mỗi khung (PNG 1920×804, tên ngẫu nhiên) gửi một subagent MỚI, không ngữ cảnh, chỉ mở đúng một file, **câu hỏi y như với Ida**: "Người này bao nhiêu tuổi, giới tính gì, đang cảm thấy gì? Nêu thêm điều gì người xem có thể thấy lạ trong ảnh (nếu có)."

| Tên | Mốc (Sprite Fright) | Nhân vật, cỡ cảnh, ánh sáng |
|---|---|---|
| b7 | 1:44,5 | Ellie, trung cận, ban ngày chạng vạng |
| f2 | 4:16,0 | Ellie, cận, ban đêm ánh xanh |
| n4 | 5:32,0 | Victoria, cận, ban đêm ánh xanh |
| u8 | 1:43,5 | Rex, trung cận, ban ngày |

## Quy tắc (chủ dự án) và kết quả
Nếu **≥ 2/3 khung tham chiếu** cũng bị gọi "mặt nạ/búp bê/con rối/ma-nơ-canh" → tiêu chí đổi thành so sánh ("Ida không bị chê là giống búp bê nặng hơn tham chiếu"). Nếu không → **giữ tiêu chí cũ**. Với 4 khung, 2/3 nghĩa là ≥ 3/4.

| Khung | Tuổi/giới đọc ra | Cảm xúc | Có chữ "mặt nạ/búp bê/con rối/ma-nơ-canh"? |
|---|---|---|---|
| b7 | bé gái 10–12 | lo lắng, bối rối, ngạc nhiên | **Không** |
| f2 | bé gái 10–13 | lo lắng, bối rối, ngại ngùng | **Không** (có "da… như đất sét hay tượng") |
| n4 | nữ 40–50 | đau khổ, hoảng sợ, la hét | **Không** |
| u8 | nam 25–35 | tự mãn, tự tin | **Không** |

**Kết quả: 0/4 tham chiếu bị gọi như vậy → GIỮ TIÊU CHÍ CŨ** ("không ảnh nào có mặt nạ/búp bê/con rối/ma-nơ-canh"). Chủ dự án xác nhận khi duyệt.

Ghi nhận thêm: người xem vẫn nêu "điểm lạ" ở phim chuyên nghiệp (khuyên tai "dán vào má", cổ mảnh so với đầu, da "như đất sét hay tượng", tỷ lệ cường điệu) nhưng **không** kết luận là mặt nạ/búp bê. Tức là phép kiểm phân biệt được: lời chê chi tiết là bình thường; từ khoá "mặt nạ/búp bê" là tín hiệu riêng của mặt Ida.

## Nguyên văn

### b7 (Ellie, 1:44,5)
> Tôi chỉ mở đúng một file: …/scratchpad/hc/b7.png. Ảnh là một khung hình hoạt hình 3D, khổ rộng, cảnh rừng lúc chạng vạng.
>
> **Tuổi:** Một bé gái khoảng 10–12 tuổi, tức cuối tiểu học hoặc đầu trung học cơ sở.
>
> **Giới tính:** Nữ. Cô bé buộc tóc đuôi ngựa, đeo khuyên tai tròn màu hồng, dây buộc tóc màu xanh ngọc.
>
> **Cảm xúc:** Lo lắng, bối rối và hơi e dè, xen chút ngạc nhiên. Người xem nhận ra điều này qua:
> - Hai chân mày nhướng lên ở giữa, vẻ mặt lo âu.
> - Mắt mở to, liếc lên và sang một bên, như đang nghe hoặc nhìn một điều khó xử.
> - Miệng hé tròn, như vừa thốt "ồ?" hay định hỏi lại.
> - Tay ôm chặt cuốn sổ lò xo trước ngực, một tư thế tự vệ. Cô bé trông như đang cảm thấy mình lạc lõng hoặc không chắc chắn.
>
> **Những điểm người xem có thể thấy lạ:**
> 1. **Bím tóc đuôi ngựa quá khổ.** Nó to gần bằng cả đầu, dựng cao vượt khỏi đỉnh đầu rồi rủ xuống quá vai, cứng như một cây chổi hay đuôi ngựa thật. Mép tóc có nhiều sợi lởm chởm, bạc màu, trông như tua xơ. Đây là điểm dễ gây chú ý hoặc khó hiểu nhất: không rõ đó là cách điệu có chủ ý hay lỗi dựng tóc.
> 2. **Tỷ lệ cơ thể.** Đầu và mắt rất to so với thân. Kiểu này quen thuộc với hoạt hình nên không hẳn là lạ, nhưng cổ khá nhỏ.
> 3. **Phụ kiện lớn và sặc sỡ.** Khuyên tai hồng rất to, và cổ tay đeo một chiếc vòng hoặc đồng hồ vàng–đỏ khá cồng kềnh. Chúng nổi bật hẳn so với nền rừng tối.
> 4. **Chữ trên cuốn sổ.** Đọc được phần đuôi "...ology" (có lẽ là "Biology") kèm hình chiếc lá. Chi tiết này gợi ý cô bé đang đi quan sát thiên nhiên.
> 5. **Nấm đỏ bóng loáng rải trên cỏ.** Trông giống đồ chơi nhựa hơn nấm thật. Cái lạ này có thể là cố ý, để tạo không khí cổ tích.
>
> Nhìn chung, hình ảnh rõ, cảm xúc đọc được dễ dàng. Điểm lạ đáng kể duy nhất là bím tóc: quá to, cứng và xơ ở mép.

### f2 (Ellie, 4:16,0)
> Tôi đã mở và xem đúng một file ảnh: …/scratchpad/hc/f2.png. Không mở file nào khác.
>
> Nhận xét của tôi như một người xem bình thường:
>
> **Tuổi:** Là một bé gái hoạt hình 3D, trông khoảng 10–13 tuổi, tức đang ở tuổi học trò.
>
> **Giới tính:** Nữ.
>
> **Cảm xúc:** Cô bé đang lo lắng, bối rối và ngại ngùng, giống như vừa làm hỏng việc gì đó hoặc sợ điều sắp xảy ra.
> - Hai lông mày nhíu lại và xếch lên ở giữa.
> - Miệng méo, nghiến răng kiểu nhăn mặt "ôi chết rồi".
> - Mắt liếc sang một bên thay vì nhìn thẳng.
> Cảm xúc đọc ra rất rõ, không bị lẫn.
>
> **Những điểm người xem có thể thấy lạ:**
> 1. **Bím tóc đuôi ngựa to bất thường.** Nó to gần bằng cả cái đầu, vắt ngược lên rồi đổ sang trái và bị nhoè mờ. Nhìn thoáng qua dễ tưởng đó là một mảng tối hay một vật khác lơ lửng sau lưng, chứ không phải tóc của cô bé.
> 2. **Đôi khuyên tai tím quá sáng so với cảnh.** Cả cảnh tối xanh, vậy mà đôi khuyên rực màu gần như tự phát sáng, cùng với dây buộc tóc xanh chói. Chúng hút mắt hơn cả khuôn mặt. Chiếc khuyên bên phải ảnh không thấy tai, trông như dán vào má hoặc hàm và hơi lơ lửng.
> 3. **Da mặt xám và phẳng.** Da trông như đất sét hay tượng, thiếu sắc hồng. Mặt cũng không sáng hơn nền bao nhiêu nên hơi "chết".
> 4. **Cổ rất mảnh so với đầu to.** Đây có thể là do phong cách vẽ, nhưng vẫn gây cảm giác mất cân đối.
> 5. **Nền tối và đục đến mức không đọc được.** Người xem không biết cô bé đang ở đâu. Chỉ lờ mờ thấy vài vật phía dưới, chẳng hạn một vật tròn trắng ở gần cổ áo.
> 6. **Răng trong miệng hơi nhoè và bẩn màu.** Chi tiết răng không sắc nét như phần còn lại của khuôn mặt.
>
> **Ấn tượng chung:** Người xem đọc được ngay cảm xúc lo lắng và bối rối của cô bé. Chỗ bị phân tâm nhiều nhất là bím tóc khổng lồ mờ nhoè và đôi khuyên tai quá rực.

### n4 (Victoria, 5:32,0)
> Tôi đã mở và xem đúng một file ảnh: …/scratchpad/hc/n4.png. Tôi không mở hay tìm file nào khác.
>
> **Ấn tượng của một người xem bình thường**
>
> - **Đây là ai:** một nhân vật hoạt hình 3D phong cách hoá, không phải người thật. Ánh sáng xanh tím, tối, như cảnh ban đêm hoặc sương mù. Khung hình rất rộng, kiểu điện ảnh.
> - **Tuổi:** khoảng 40–50. Cảm giác này đến từ khuôn mặt hơi đầy, nếp ở cằm và má, cách trang điểm đậm kiểu thập niên 80 (phấn mắt xanh, son tím, bông tai hình học to, vòng cổ chuỗi hạt), và tóc vàng hơi rối, chân tóc sẫm màu.
> - **Giới tính:** nữ.
> - **Cảm xúc:** rất đau khổ, hoảng sợ hoặc tuyệt vọng, như đang gào khóc hay la hét.
>   - Mắt nhắm chặt, lông mày nhíu mạnh.
>   - Miệng mở méo, nhe răng.
>   - Vệt đen dưới mắt trông như mascara bị nhoè vì khóc.
>   - Một bàn tay giơ về phía trước như muốn che chắn, đẩy ra hay xua đuổi điều gì đó.
>   - Cả cảnh vừa đau đớn vừa kháng cự, có chút cường điệu kiểu hài bi.
>
> **Những điểm có thể thấy lạ**
>
> 1. **Mũi khác màu:** mũi hồng và ấm hơn hẳn phần còn lại của khuôn mặt, vốn đang ám xanh lạnh. Trông như mũi được chiếu một nguồn sáng riêng, hoặc bị đỏ vì khóc.
> 2. **Bông tai bên phải nằm sai chỗ:** nó rủ xuống ngang cằm hoặc cổ, gần bàn tay, chứ không nằm cạnh tai. Tai bên đó bị che nên nhìn khá khó hiểu.
> 3. **Vệt tối ở cằm:** có vài vệt nhỏ bên trái cằm, trông như vết nứt, vết xước hoặc sợi tóc vương. Không rõ là cố ý hay lỗi.
> 4. **Vệt đen dưới mắt đặc và rộng:** trông giống bóng đổ của lông mi hay một mảng đen hơn là nước mắt lem mascara, nên hơi khó đọc.
> 5. **Bàn tay:** rất to và mờ vì ở gần máy quay, ngón tay dài, mềm như cao su. Đây là kiểu phóng đại của hoạt hình nhưng có thể gây cảm giác hơi kỳ.
> 6. **Miệng:** rất méo, viền son tím dày như một vành ống. Răng trên thưa, trông hơi dị, tuy khớp với phong cách cường điệu.
>
> Nhìn chung, cảm xúc "đau khổ, hoảng loạn, muốn đẩy ra" đọc được rất rõ. Chỗ dễ làm người xem khựng lại nhất là mũi khác màu và vị trí bông tai bên phải.

### u8 (Rex, 1:43,5)
> Tôi đã xem đúng một file `…/scratchpad/hc/u8.png` và không mở file nào khác.
>
> **Nhìn như một người xem bình thường:**
>
> - **Tuổi:** Một người đàn ông trẻ, khoảng 25–35 tuổi.
> - **Giới tính:** Nam. Nhân vật có vai rộng, tay to, tóc vàng vuốt kiểu "soái ca".
> - **Cảm xúc:** Tự mãn, tự tin, hơi kiêu. Mí mắt khép hờ, lông mày hơi nhướng, miệng cười nhếch nhẹ. Đó là vẻ "ta đây biết mình ngầu", có chút coi thường hoặc trêu chọc người đối diện. Nhân vật không tỏ ra sợ, buồn hay giận mà thoải mái, dửng dưng.
>
> **Những điểm người xem có thể thấy lạ:**
>
> 1. **Tỷ lệ cơ thể rất cường điệu.** Cằm và hàm dài quá mức, cổ gần như liền với cằm. Mũi to, dài và thẳng. Đầu nhỏ so với thân và tay đồ sộ. Đây rõ ràng là phong cách biếm hoạ có chủ ý, nhưng thoạt nhìn khá kỳ.
> 2. **Nhân vật phụ ở nền bên phải trông bí ẩn.** Đầu bị che hoàn toàn bởi một cái mũ nâu hình chuông, không thấy mặt. Nhân vật mặc áo trắng, quần đùi đỏ, giày thể thao trắng, đứng im như quay lưng lại, không thấy tay. Người xem dễ hỏi đó là ai, đang làm gì hay đang trốn.
> 3. **Trang phục lệch với bối cảnh.** Nhân vật chính mặc áo polo xanh với áo gile len trắng viền xanh kiểu cricket hoặc quần vợt, thắt lưng hồng, nhưng lại đứng giữa rừng tối có gốc cây khổng lồ và nấm đỏ. Trông như người đi chơi thể thao lạc vào khu rừng cổ tích.
> 4. **Chi tiết nhỏ.** Có một dải xám (giống băng đô) lấp ló trên tóc. Bàn tay góc trái dưới bị khung hình cắt ngang, trông hơi cứng. Khung hình có tỷ lệ rất rộng (1920×804, khoảng 2.39:1, kiểu màn ảnh rộng điện ảnh) chứ không phải 16:9.
>
> Tổng thể đây là một khung hình hoạt hình 3D phong cách hoá, không phải người thật. Ánh sáng ấm, phần nền chìm mờ nên nhân vật chính nổi bật rõ.
