# Cổng mặt Ida — kiểm mù lần 2 (sau lần chỉnh 1)

Lần chỉnh 1 chỉ đổi dàn dựng và biểu cảm, không đổi thiết kế đã khoá:
- mũ đẩy 35% (hat_back = 0,35), không đẩy hết. Vành vẫn ôm mặt; tóc lộ ra không còn đọc thành "tóc cắt ngắn".
- biểu cảm lệch hai bên: cười buồn 0,3; nghẹn 0,2. Mặt thật không đối xứng.
- mắt có điểm nhìn: gaze ngang 0,05 rad, dọc −0,04 rad.

Cách hỏi và độ phân giải giống lần 1. Tên file mới: p3, r8, t5. Mỗi ảnh gửi cho một subagent mới.

| File | Biểu cảm đích | Ảnh |
|---|---|---|
| p3 | trung tính | `lan2_neutral.jpg` |
| r8 | cười buồn | `lan2_sad_smile.jpg` |
| t5 | nghẹn lời | `lan2_choked.jpg` |

## p3 (trung tính) — nguyên văn
> Tôi đã mở đúng một file p3.png. Dưới đây là cảm nhận của tôi khi xem như một người xem bình thường.
>
> **Tuổi:** Người này đã lớn tuổi, tôi đoán khoảng 60 đến 70. Tôi đoán vậy vì tóc hai bên thái dương đã bạc, trán có nếp nhăn ngang, khoé mắt có vết chân chim, và có rãnh sâu từ cánh mũi xuống khoé miệng.
>
> **Giới tính:** Tôi nghiêng về một bà cụ, nhưng không chắc lắm. Gương mặt không có râu, đường nét khá thanh, cổ quấn khăn len đỏ, nên tôi nghĩ là nữ. Tuy vậy, chiếc mũ phớt rộng vành, áo khoác xanh sẫm và kiểu tóc cắt ngắn bên dưới mũ cũng hợp với một ông cụ. Tôi chỉ chắc khoảng 60 đến 65% là nữ.
>
> **Cảm xúc:** Người này có vẻ đang trầm ngâm, hơi buồn hoặc bâng khuâng, pha chút lo lắng. Mắt nhìn chếch xuống và sang một bên như đang nhớ lại điều gì. Lông mày hơi nhướng ở phía trong. Miệng mím nhẹ, không cười.
>
> Cảm xúc này khá mờ nhạt, phải nhìn kỹ mới đoán ra. Tôi dựa chủ yếu vào đôi mắt và ánh sáng cam ấm trong khung cảnh buổi tối. Phần má, cằm và miệng gần như đứng yên, trông hơi giống mặt nạ. Vì vậy nếu chỉ nhìn nửa dưới khuôn mặt thì tôi sẽ đọc là vô cảm.

## r8 (cười buồn) — nguyên văn
> Nhìn qua thì đây là một người già, chắc khoảng 70 tuổi hoặc hơn. Trán có nhiều nếp nhăn, khóe mắt có vết chân chim, má hơi chảy xệ, và tóc bạc lòi ra dưới vành mũ.
>
> Giới tính thì tôi không chắc lắm. Tôi đoán nghiêng về một bà cụ, vì khuôn mặt tròn, đường nét mềm và không có râu. Nhưng chiếc mũ phớt với khăn len quàng cổ thì nam hay nữ đều đội, đều quàng được, nên nói là ông cụ cũng không sai.
>
> Về cảm xúc, nét mặt khá rõ. Hai đầu lông mày phía trong nhướn lên, mắt nhìn xuống, còn miệng thì hơi mỉm cười. Tôi đọc ra một nỗi buồn nhẹ, kiểu bồi hồi nhớ lại chuyện cũ: vừa thương vừa tiếc, cười mà vẫn buồn. Không phải đau khổ hay khóc lóc, mà là một nỗi buồn lặng lẽ và dịu dàng. Ánh đèn vàng ấm chiếu từ một phía, xung quanh là phố tối, nên cảnh càng có vẻ cô đơn và hoài niệm.

## t5 (nghẹn lời) — nguyên văn
> Mô tả như một người xem bình thường:
>
> - **Tuổi:** Một người già, tôi đoán khoảng 70 tuổi, có thể hơn. Tóc bạc lộ ra dưới vành mũ, trán nhăn nhiều, quanh mắt và hai bên miệng có nếp nhăn sâu, má hơi chảy xệ.
> - **Giới tính:** Tôi không chắc chắn. Nhìn thoáng qua thì tôi nghiêng về một **bà cụ**, vì gương mặt thon mềm và chiếc khăn len quàng cổ. Tuy vậy, mũ phớt và tóc ngắn bạc cũng hợp với một ông cụ, nên ảnh không cho thấy rõ.
> - **Cảm xúc:** Người này đang **buồn, đau lòng, như đang cố nén khóc**. Hai đầu lông mày nhướng lên và chụm lại ở giữa, mắt nhìn xuống, khoé miệng trễ xuống, môi mím lại. Trên má trái của nhân vật có một vệt nước mắt mờ. Tôi đọc được cảm giác mất mát hoặc thương nhớ hơn là tức giận hay sợ hãi. Ánh đèn ấm hắt lên mặt giữa khung cảnh tối cũng làm khoảnh khắc này thêm cô đơn.

## Chấm theo tiêu chí
| Tiêu chí | Kết quả |
|---|---|
| Đọc là bà lão | Tuổi: 3/3 người già (60–70+). Giới tính: 3/3 "nghiêng về bà cụ", nhưng cả 3 nói **không chắc** (60–65%). Lý do: tóc lộ ra đọc thành tóc ngắn; mũ phớt, áo khoác, khăn hợp cả nam lẫn nữ. |
| Cảm xúc đúng ≥ 2/3 | **2/3 đúng**: r8 "cười mà vẫn buồn"; t5 "cố nén khóc". p3 (trung tính) đọc thành "trầm ngâm, hơi buồn". |
| Không có "mặt chết" hay "mắt trống" | Không ai dùng hai chữ đó. Nhận xét "búp bê/con rối" của lần 1 không còn ở r8 và t5. Còn một nhận xét: "phần má, cằm và miệng gần như đứng yên, trông hơi giống mặt nạ" (p3, ảnh trung tính). |

## Kết luận
- **Đạt:** tuổi (3/3); cảm xúc (2/3); không có chữ "mặt chết" hay "mắt trống".
- **Chưa đạt chặt:** giới tính. Cả 3 đều nghiêng về nữ nhưng không chắc, ở cả hai lần.
- **Nguyên nhân:** ở góc gần chính diện, búi tóc (dấu hiệu nữ chính trong model sheet) bị đầu che mất. Phần tóc lộ ra dưới vành mũ đọc thành tóc cắt ngắn.
- **Không dùng lần chỉnh 2:** dàn dựng không sửa được nguyên nhân này. Muốn sửa phải đổi thiết kế tóc hoặc phụ kiện đã khoá bằng SHA, nên chủ dự án phải quyết (quyết định C trong CONG-4.md).
- **Cổng mặt: CHƯA ĐÓNG. Không đi tiếp Cổng 6.**
