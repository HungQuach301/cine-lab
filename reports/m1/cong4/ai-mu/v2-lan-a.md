# AI mù — animatic v2, lần chạy A (bản TRUNG GIAN, trước khi sửa trắng tràn ở 0:40–0:42)

Cách chạy: 71 khung JPEG cắt từ `screening/animatic.mp4` (SHA 729dffca…, bản trung gian), mỗi 2 s (lấy ở giây t + 0,5), có phụ đề cháy, không âm thanh.
Một subagent mới, chỉ được mở thư mục khung. Câu hỏi: (a)(b)(c1 0:40)(c2 1:41)(c3 2:00)(d) như `screening/questions.json`, cộng các câu kiểm hiểu (e)–(k).
Sau lần này P phát hiện lỗi ở 0:40–0:42 (xem câu c1: người xem vẫn thấy ánh vàng và bóng dài), sửa hệ số trắng tràn, render lại 21 shot, rồi chạy **lần B** trên bản cuối (`v2-lan-b.md`).

## Nguyên văn
> Tôi đã xem lần lượt cả 71 khung, từ 0:00 đến 2:20, không mở file nào khác.
>
> **(a) Câu chuyện**
> Một bà già thắp đèn đường, đội mũ, mang thang và đèn lồng, đi thắp những ngọn đèn khí cuối cùng trên phố cổ ("Evening, old street."). Cùng lúc ấy, đèn điện trắng mới đang bật sáng khắp thành phố. Bà gặp một cậu bé đang chơi trò bóng tay trên tường. Ánh đèn điện làm bóng của cậu biến mất, nên bà dùng đèn lồng tạo lại bóng cho cậu. Bà nói lời từ biệt ngọn đèn cuối ("That's the last one, then… Goodnight, old street… keep a little dark for the ones who need it"), trao đèn lồng cho cậu rồi rời đi. Cậu tiếp tục làm bóng tay trong một góc tối.
>
> **(b) Các đoạn thấy mất tập trung / khó theo dõi**
> - **0:10–0:20:** cận mặt và cận đồng hồ bỏ túi đứng yên khá lâu. Hai khung liền nhau gần như giống hệt.
> - **0:40–0:50:** ánh sáng đột ngột chuyển xám trắng như ban ngày. Mặt bà đổi hẳn phong cách (chân thực, nhiều nếp nhăn), mũ từ nâu nhạt thành đen, áo từ xanh lá thành xanh két.
> - **0:50–1:00:** cảnh rất tối. Ở 0:54 gần như không có gì trên hình, và tôi không rõ "Not yet… not yet" nghĩa là gì.
> - **1:20–1:30:** cảnh hốc vòm bị lóa trắng. Hai nhân vật trong hốc trông khác thiết kế (cậu bé như không đội mũ len, tóc búi). Khó phân biệt đâu là người thật, đâu là bóng.
> - **1:40–1:50:** câu "Just… keep a little dark…" hiện trên cận mặt cậu bé rồi sang cận mặt bà, nên tôi không chắc ai nói. Ánh sáng lại trắng như ban ngày.
> - **2:00–2:10:** cậu bé ở 2:00 bị nhòe và biến dạng, mũ khác màu. Cảnh toàn thành phố ở 2:02–2:04 lặp lại cảnh đã thấy.
> - **2:10–2:22:** thứ tự cảnh đồng hồ → con hẻm → cậu bé hơi rời rạc, và phim kết thúc khá đột ngột.
>
> **(c1) 0:40**
> Tôi thấy ấm áp, hơi hoài niệm. Bà đứng trên thang, tay ôm cột, vừa thắp xong một ngọn đèn khí. Ánh vàng hắt lên tường, bóng bà in bên cạnh.
>
> **(c2) 1:41**
> Tôi thấy buồn và trầm lắng. Khung 1:40 là cận mặt bà dưới ánh đèn vàng với phụ đề "Goodnight, old street." Bà đang từ biệt ngọn đèn khí cuối cùng; nét mặt buồn nhưng cam chịu.
>
> **(c3) 2:00**
> Tôi thấy dịu lại, có chút hy vọng, nhưng cũng hơi bối rối vì hình nhòe. Cậu bé ngồi thấp trong hốc tường, dưới chân có đèn lồng, hai tay xòe ra như đang làm bóng. Bà đứng ngoài con phố sáng trắng nhìn vào. Tôi hiểu là cậu đã được giữ lại "một chút bóng tối".
>
> **(d) Điểm: 3/5**
> Ý tưởng và cảm xúc hay: ánh sáng cũ đối lập ánh sáng mới, và "giữ lại chút bóng tối". Nhưng nhân vật thiếu nhất quán và có nhiều cảnh lóa trắng nên khó nhập tâm.
>
> **(e) Ngày hay đêm**
> Ban đêm: trời xanh thẫm có sao, cửa sổ sáng đèn. Tuy vậy có vài cảnh (0:48–0:50, 1:06–1:16, 1:44–1:54) ánh sáng xám trắng trông như ban ngày, gây nhầm lẫn. Ánh sáng trắng trên phố là **đèn điện mới** (đèn cao áp lóe sáng, 0:30 và 1:06), đang thay thế đèn khí vàng.
>
> **(f) Nhân vật chính và chỗ không nhất quán**
> Nhân vật chính là một bà già, khoảng 65–75 tuổi, tóc bạc búi, đeo khuyên vàng, quàng khăn đỏ. Cậu bé khoảng 8–10 tuổi. Những chỗ không nhất quán:
> - **Mũ của bà:** xám nâu (0:12), nâu nhạt/cam (0:36, 0:40), đen (0:48–0:50, 1:12–1:14), nâu (1:34–1:50).
> - **Mặt bà:** kiểu khác hẳn giữa 0:12 (hoạt hình), 0:50 (gần chân thực, nhiều nếp nhăn), 1:14 (mịn, trẻ hơn) và 1:36–1:48 (mặt to, méo).
> - **Mắt bà:** tối màu ở 0:50, nâu cam ở 1:46–1:48.
> - **Khăn và áo:** khăn đỏ cam ở một số cảnh, đỏ mận/hồng ở cảnh khác. Áo lúc xanh lá (0:12, 1:34), lúc xanh két (0:48, 1:14).
> - **Cậu bé:** ở 1:22 trông như không có mũ len, tóc búi. Ở 2:00 mặt nhòe, mũ nâu. Ở 2:18–2:20 mắt thành hai vệt đen lạ.
>
> **(g) Đồng hồ**
> - **Đồng hồ bỏ túi của bà:**
>   - khoảng 7:28 (0:16–0:18);
>   - khoảng 7:55 (0:28): mặt đồng hồ này hơi khác mặt ở 0:16;
>   - khoảng 9:55 (2:12);
>   - đúng 10:00 (2:14).
> - **Đồng hồ công cộng trên cột trong quảng trường** (0:24–0:26): khoảng 8:00. Tôi không chắc lắm về kim giờ.
>
> Theo tôi, đồng hồ đếm ngược đến giờ đèn điện bật và điểm kết thúc ca làm, có lẽ cũng là kết thúc nghề thắp đèn của bà. 10:00 như dấu chấm hết.
>
> **(h) 1:49–1:54**
> Ở 1:50 bà đưa tay lên cần/van dưới chụp đèn. Ở 1:52 đèn còn sáng, ở 1:54 ngọn đèn trông đã tắt, và bà đưa đèn lồng cho cậu bé. Tôi hiểu là bà vặn tắt (hoặc chỉnh) ngọn đèn khí cuối cùng, nhưng không chắc chắn.
>
> **(i) 1:20–1:29**
> - **1:20:** chưa thấy bóng rõ.
> - **1:22–1:26:** trên tường hậu của hốc có một bóng lớn của người lớn (bà) và bóng nhỏ của cậu bé có quả len trên mũ. Ngoài ra có hai hình người nhỏ mờ mà tôi không chắc là người thật hay bóng.
> - **1:28:** rõ hai bóng, bóng cao của bà và bóng cậu bé có quả len. Bóng của bà trông như không có vành mũ, dáng thon, trẻ hơn. Tôi không chắc đó là cố ý (bóng thời trẻ?) hay lỗi.
>
> **(j) Cậu bé**
> Cậu xuất hiện rõ lần đầu ở **0:58** (ở 0:56 chỉ có một hình nhỏ mờ trong bóng tối). Cuối phim cậu cầm đèn lồng vào hốc/góc tối và làm bóng tay (hình chim/tay) trên tường (1:58, 2:00, 2:18–2:20). Bà vác thang đi ra khỏi con hẻm.
>
> **(k) Chỗ tôi không hiểu**
> - "Not yet… not yet" (0:50–0:52) ý là gì: chưa đến giờ, hay chưa muốn tắt?
> - Ai nói câu "Just… keep a little dark…": bà hay cậu bé, và nói với ai (với phố hay với đèn điện)?
> - Hốc vòm (1:20–1:26, 1:58) nằm ở đâu so với con phố, và vì sao hình người trong đó khác thiết kế.
> - Vì sao có những cảnh ánh sáng như ban ngày.
> - Bà có phải người thắp đèn cuối cùng không, và việc bà rời đi có nghĩa là nghỉ việc hay chết? Tôi đoán là nghỉ việc, không chắc.
> - Cảnh con hẻm ở 2:06–2:10 bà đang làm gì (vẫy tay? chào ai?).
