# CỔNG 6 — THÂN CAS LƯỢT 2: KIỂM MÙ **TRƯỢT** (1 câu HÌNH ở Cas; đối chứng 1/2) → KHÔNG KHOÁ, DỪNG

Nhánh `claude/cine-lab-m2-cong5-layout-24o5fp` (W4T lượt 2 merge @0c62b9f). Ngày 29/09/2026.
Quyết định gốc: AUTHORSHIP "Cổng 6 — nhân vật": chọn A, cách chấm HÌNH/TƯ THẾ, tay Cas theo tỷ lệ MPFB.

**Làm đúng nhánh TRƯỢT của chỉ thị (mục 4):**
- không khoá v1.5.1 hay v1.6;
- không đổi `CAS_STYLE`, thân hay tay mặc định;
- không render layout-v16, không chạy luật;
- không merge main; không mở W1, W2.

Layout mặc định không đổi: dò s02, s24c, s37, s42 được 12 ảnh nhỏ, **lệch 0 px**.

## 0. Tóm tắt
- **Sửa thân (W4T lượt 2): qua điều kiện dừng.** Đã làm đủ a–e:
  - quần ống thẳng, không bó, không lộ háng;
  - gấu áo 2,10 H phủ qua cạp; không còn dải da, kể cả khi cầm đèn lồng và khi giơ tay cao nhất (s25);
  - áo nới; ngực và lưng trơn;
  - gáy sạch;
  - tay theo tỷ lệ MPFB;
  - da tay ấm hơn.

  Chi tiết: `reports/m2/cong6/w4t2/BAO-CAO-W4T2.md`.
- **Mọi lời chê HÌNH của lượt 1 về quần và eo đã biến mất.** Không subagent nào nhắc quần bó, dải da, háng hay "lệch phong cách".
- **Kiểm mù vẫn TRƯỢT ở hai tiêu chí:**
  1. Khung Cas toàn thân có **1 câu có từ khoá "búp bê"**. Câu này nói cả dáng lẫn hình ("chân … nhỏ so với thân"). Theo luật chấm, câu vừa nói hình vừa nói dáng tính vào **HÌNH**.
  2. **Đối chứng 1/2**: Sprite Fright 332 s bị tả "gần như hình **mặt nạ**" (về miệng méo).
- **Người làm W4T lượt 2 là P, không phải phiên xưởng.** Hai lần giao cine-worker đều dừng ngay: worktree cô lập được tạo từ `main`, thiếu lượt 1, và worker không được phép tự tiến nhánh. P không chạy hộ các lệnh đã bị chặn. P tạo worktree `w4t2` từ nhánh P rồi tự làm.
- **Token phần sửa thân vượt hạn:** khoảng 285 nghìn, so với hạn khoảng 150 nghìn (mục 5).

## 1. Ảnh trước/sau (`reports/m2/cong6/w4t2/`)
| Ảnh | Nội dung |
|---|---|
| `W4T2_truoc-sau_quan.jpg` | Quần: bó sát như quần tất → ống thẳng, rộng, nếp gối, gấu thẳng (EEVEE 0°/90°) |
| `W4T2_truoc-sau_eo.jpg` | Eo ở s42a 114,5 s: lượt 1 lộ háng, dưới đèn lồng là khe → lượt 2 thấy len dưới đèn lồng. Tư thế giơ tay cao nhất (s25 60,5 s), EEVEE trước và sau lưng: không hở |
| `W4T2_truoc-sau_ao.jpg` | Ngực 0°/60°: hết in cơ ngực và núm. Gáy 180°: hết gai và đốm da xuyên cổ áo |
| `W4T2_truoc-sau_tay.jpg` | Độ dài tay: sheet → MPFB. Tay dưới đèn lồng: trung vị pixel (244,199,173) → (238,152,108) |
| `W4T2_cas_eevee_4goc.jpg` | Cas lượt 2, EEVEE 0°/60°/180°/−120° |
| `W4T2_hai-nguoi_s42a.jpg`, `W4T2_hai-nguoi_WS.jpg`, `W4T2_cas_s42a_cat.jpg` | Ba khung nộp kiểm mù: 1920×1080, 3 mẫu, cùng khung với lượt 1 |

Bản mù đã nộp và bảng tên: `reports/m2/cong6/kiem-mu-than-2/`.

## 2. Kiểm mù (P, 5 subagent mới; câu hỏi y hệt lượt 1; đếm từ khoá bằng máy)
| Khung (tên mù) | Tuổi, giới | Lệch phong cách | Từ khoá chỉ vào Cas: **HÌNH** | Từ khoá: **TƯ THẾ** (giao W1/W2) | Lời chê HÌNH khác, không có từ khoá |
|---|---|---|---|---|---|
| Hai người s42a (`8b8997ea`) | Ida nữ 70–80 ✔; Cas 7–10, "nhiều khả năng bé trai" ✔ | **Không** | 0 | **1** (cả hai nhân vật): "cả hai đứng cứng đơ, chân thẳng, trọng tâm không rõ, trông giống **búp bê** được đặt vào cảnh" | tay "cứng như găng khối", đặt hai bên quai chứ không nắm; Cas cao khoảng 80 % bà cụ, "giống thiếu niên 12–13" |
| Hai người s41 WS (`9c91d38f`) | Ida 60–75, "nghiêng về bà cụ", không chắc; Cas 7–10, "có lẽ bé trai" ✔ | **Không** | 0 | 0 (có "hơi cứng và đơ", không có từ khoá) | mặt quá nhỏ, không đọc được |
| Cas toàn thân (`b9a36d05`) | 9–12, bé trai ("mặt khá trung tính") ✔ | — | **1**: "**Dáng đứng cứng.** Hai chân thẳng, song song, **nhỏ so với thân**, nên trông giống một con **búp bê**" (câu vừa dáng vừa hình → HÌNH) | — | tay "cứng và vuông vức, giống đeo găng"; đèn lồng "dính vào bụng" |
| Đối chứng SF 104,5 s (`261342ee`) | bé gái 10–12 | — | 0 | — | — |
| Đối chứng SF 332 s (`7a570475`) | nữ 40–55 | — | **1**: "Miệng mở rất to … gần như hình **mặt nạ**" | — | — |

**Chấm (chỉ cột HÌNH):**

| Tiêu chí | Kết quả | Đạt? |
|---|---|---|
| Không lệch phong cách | 0/2 khung hai người | ✔ (lần thứ 2 liên tiếp) |
| 0 từ khoá chỉ vào Cas (HÌNH) | **1/3 khung** (lượt 1: 2/3) | **✘** |
| Tuổi và giới đúng | đúng cả 5; rào đón ở WS (mặt nhỏ) | ✔ |
| Đối chứng 0/2 | **1/2** | **✘** |

**Cột TƯ THẾ (giao W1/W2, không tính):** 1 câu ở s42a về dáng đứng cứng đơ của cả hai nhân vật.

**Nhiễu nền của đối chứng:** tính cả vòng này, **2/20 lượt** (trước đó 1/18). Mẫu nhỏ: mỗi vòng chỉ có 1 khung Cas toàn thân, nên một câu đã đổi kết quả.

**P đọc nguyên nhân (tự xem, chưa kiểm):**
- Phần HÌNH của câu trúng là **"chân nhỏ so với thân"**.
- Gấu áo hạ 0,15 H (sửa mục b) làm thân trong hình bóng dài thêm khoảng 13 % (C3 thân 2,41 → 2,72) và chân ngắn lại, nên chân đọc là nhỏ so với thân.
- Đây là hệ quả trực tiếp của sửa mục b. Có thể chỉnh bằng tham số: nâng gấu một phần, và/hoặc cho ống quần rộng hơn.
- "Tay như găng" vẫn còn ở 2/3 khung. Không có từ khoá, nhưng là lời chê HÌNH; một phần do tay chưa nắm quai thật ở s42a (thuộc tư thế).

## 3. C3
- **Cas lượt 2, 'doc'**:

| Góc | 0° | 45° | −45° | 90° | −90° | 135° | −135° | 180° |
|---|---|---|---|---|---|---|---|---|
| thân/đầu | 2,723 | 2,814 | 2,809 | 2,832 | 2,832 | 2,931 | 2,990 | 4,045 |

  - Số bộ phận khác và bảng `c3_views` soạn sẵn: `characters-v1.6-NHAP.md` mục 6 (có JSON).
  - Số thô: `W4T2_c3_cas_doc.json`.
- **Ida v1.5.1, 'pca'**: không đổi so với báo cáo lượt 1. Lượt 2 không sửa gì của Ida ngoài vật liệu da tay 'bl', và vật liệu không đổi hình bóng.
- Luật trên layout-v16: **không chạy**, vì không khoá.

## 4. Việc chuyển W1/W2 (khi mở)
1. **Tư thế đứng:** "cứng đơ, chân thẳng, trọng tâm không rõ" (s42a; cả Ida và Cas).
2. **Các shot cầm nắm theo tay mới** (lệch tâm lòng tay đo thật, cm; bảng đủ ở BAO-CAO-W4T2 mục 4):
   - giữ thang s37w, s38, s40w: 6,7 cm;
   - đèn lồng s41, s42a: khoảng 4 cm;
   - chim bóng s25, s32: 6,4–7,0 cm;
   - vỗ tay s28: 6,4 cm;
   - dựa tường s24c: 7,0 cm;
   - áp tay s42: 6,6 cm;
   - s42b, s48: chưa đo được (trang thử lỗi).
3. **Tay nắm quai đèn lồng thật** ở s41 và s42a (lời chê "đặt hai bên quai chứ không nắm").
4. **Vai khi giơ tay cao (s25):** áo dồn khối. Do biến dạng da, tư thế này chưa kiểm mù.

## 5. Thời gian, token, hàng đợi
| Việc | Giờ UTC | Token | Hàng đợi |
|---|---|---|---|
| Hai lần giao worker (dừng ngay, không sửa gì) | trước 06:15 (lần 1: 2,5 phút; lần 2: 28,5 phút) | 20 249 + 20 279 | 0 |
| P tự làm W4T lượt 2: sửa, điều kiện dừng, C3, dò, lệch điểm nắm, ảnh trước/sau, báo cáo, merge | 06:15–07:20 | **khoảng 285 nghìn** theo bộ đếm phiên P (có ảnh xem kiểm). **Vượt hạn khoảng 150 nghìn**: chẩn đoán rãnh lưng 5 lượt, gáy 2 lượt | 68 việc (6 nặng, 62 nhanh); chờ tổng 300 s; chạy tổng 1 254 s; 0 việc quá 60 s; 4 việc lỗi (trang thử ở s42b, s48) |
| Kiểm mù 5 subagent | 07:18–07:21 (31–49 s mỗi subagent) | 48 091 + 47 488 + 45 213 + 46 158 + 46 231 = **233 181** | 0 |

## 6. Việc treo
- `bl_head.js` trỏ `ida_bl_v151.glb`, bản chưa khoá. Các tệp v1.5 đã khoá không bị đụng.
- s33 P0 (khớp biên 1,61, ngưỡng 1,5): chưa có lần render mới.
- Xuất `silhouettes` đã sẵn cho lần render layout-v16 đầu tiên.

## Phụ lục — nguyên văn 5 subagent (cả đối chứng)
Giữ nguyên văn. Chỉ rút đường dẫn thư mục tạm của phiên P về tên file mù.

### W4T2_hai-nguoi_s42a — file mù `8b8997ea.jpg` — nguyên văn

> Tôi chỉ mở đúng một file theo yêu cầu: 8b8997ea.jpg. Đây là một khung hình hoạt hình 3D: một phố lát đá lúc chạng vạng, phía sau là cổng vòm tối, cột đèn và một chiếc thang dựa vào tường.
>
> **Những người trong ảnh**
>
> 1. **Người bên trái:** một bà cụ, chừng 70 đến 80 tuổi. Nhận ra là nữ nhờ tóc bạc búi sau gáy, bông tai, áo khoác dài màu xanh lục, váy dài, khăn quàng đỏ và mũ phớt.
>    - Cảm xúc: nghiêm, lạnh, có phần dè chừng hoặc không hài lòng. Môi mím, khoé miệng trễ xuống, mày hơi chau. Dáng đứng thẳng, tay buông xuôi.
> 2. **Người ở giữa:** một đứa trẻ, chừng 7 đến 10 tuổi. Nhiều khả năng là bé trai (tóc ngắn, mũ len có quả bông đỏ, áo len đỏ, quần dài), nhưng gương mặt khá trung tính.
>    - Cảm xúc: rụt rè, hơi lo lắng hoặc thận trọng. Em ôm chiếc đèn lồng sát người, mắt liếc sang phía bà cụ, môi hơi mím như đang chờ bị hỏi hay bị mắng. Có thể đọc là "ngoan nhưng sợ".
>
> **Những điểm người xem có thể thấy lạ**
>
> - **Ánh đèn lồng:** đèn rất sáng và làm áo len đỏ rực lên, nhưng hầu như không chiếu ra mặt đất, tường hay bà cụ ở ngay cạnh. Dưới chân em cũng không có vệt sáng hay bóng đổ. Vì vậy ánh sáng trông như dán lên chứ không có thật trong cảnh.
> - **Tay cầm đèn:** hai tay em đặt hai bên quai chứ không nắm lấy quai. Tay trông cứng như găng khối, nên chiếc đèn có vẻ lơ lửng trước bụng.
> - **Hướng nhìn của bà cụ:** đầu bà gần như nhìn thẳng ngang tầm mắt mình. Ánh mắt có vẻ đi qua trên đầu đứa trẻ chứ không cúi xuống nhìn em, nên hai nhân vật chưa thật sự nhìn nhau.
> - **Tỉ lệ cơ thể:** hai người đứng gần cùng độ sâu, và em cao tới khoảng 80% chiều cao bà cụ. Chiều cao đó giống một thiếu niên 12–13 tuổi, trong khi gương mặt và dáng người lại như trẻ nhỏ.
> - **Dáng đứng:** cả hai đứng cứng đơ, chân thẳng, trọng tâm không rõ, trông giống búp bê được đặt vào cảnh hơn là người đang đứng tự nhiên.
> - **Tiếp đất:** dưới chân cả hai gần như không có bóng tiếp đất, nên nhân vật hơi "trôi" trên nền.
> - **Nền và bối cảnh:**
>   - Đá lát tiền cảnh là các chấm tròn lặp đều, trông như hoa văn in hơn là đá thật.
>   - Cổng vòm đen đặc, không có chút chi tiết nào.
>   - Mấy thanh đen dọc trên tường bên trái không rõ là vật gì.
>   - Cột đèn bị cắt khỏi khung, không thấy đèn.
>   - Tường được chiếu sáng đều và phẳng, không hợp với không khí chạng vạng.
> - **Ánh sáng tổng thể:** ánh sáng lạnh và phẳng, và nguồn sáng ấm duy nhất (đèn lồng) không tương tác với môi trường. Vì vậy cảnh chưa có chiều sâu và không khí.

### W4T2_hai-nguoi_WS — file mù `9c91d38f.jpg` — nguyên văn

> Tôi đã mở đúng một file: 9c91d38f.jpg. Không mở hay tìm file nào khác. Dưới đây là cảm nhận của một người xem bình thường.
>
> **Trong ảnh có gì:** Đây là một khung hình hoạt hình 3D. Một con phố lát đá cuội, cạnh một bức tường trắng lớn có cửa vòm tối. Có hai nhân vật đứng cạnh một cột đèn đường kiểu cổ, trên cột có dựa một chiếc thang gỗ.
>
> **Nhân vật 1 (bên trái, cạnh cột đèn):**
> - Tuổi: trông là người già, chừng 60–75 tuổi. Tóc trắng hoặc bạc, dáng hơi khom.
> - Giới tính: không chắc chắn. Người này đội mũ đen, mặc áo khoác dài màu xanh lá gần chạm đất (trông giống váy), quàng khăn đỏ. Có thể là một bà cụ, nhưng cũng có thể là ông cụ thắp đèn đường, vì có thang và đèn lồng. Tôi hơi nghiêng về bà cụ vì tà áo dài.
> - Cảm xúc: mặt quá nhỏ và mờ nên không đọc được nét mặt. Qua dáng người, bà/ông đang chìa chiếc đèn lồng sáng về phía đứa trẻ, trông hiền hậu, ân cần, như đang trao hoặc cho xem.
>
> **Nhân vật 2 (bên phải):**
> - Tuổi: một đứa trẻ, khoảng 7–10 tuổi.
> - Giới tính: có lẽ là bé trai, dựa vào tóc ngắn, áo len đỏ, quần sẫm và mũ len trắng có quả bông đỏ. Chi tiết này cũng không rõ hẳn.
> - Cảm xúc: cũng không thấy rõ mặt. Em giơ hai tay về phía đèn lồng như muốn đón lấy hoặc hơ tay cho ấm. Cảm giác là tò mò, háo hức, hơi rụt rè.
>
> **Không khí chung:** Một khoảnh khắc nhẹ nhàng, ấm áp giữa người già và trẻ nhỏ lúc chiều tối. Đèn lồng là điểm sáng ấm duy nhất.
>
> **Những điều người xem có thể thấy lạ:**
> 1. **Ánh sáng không khớp với giờ trong ngày:** Đèn lồng sáng như lúc chập tối, nhưng bức tường lại sáng đều, bệt và nhạt màu như ban ngày. Đèn lồng gần như không hắt ánh sáng lên tường hay lên người nhân vật.
> 2. **Cột đèn đường không sáng**, trong khi lẽ ra đây là lúc thắp đèn.
> 3. **Nhân vật và đồ vật chồng lên nhau:** Người già đứng sát rạt, gần như dính vào cột đèn. Chiếc thang lại dựa xuyên ra sau lưng người đó, trông không tự nhiên.
> 4. **Các cột hay ống đen mảnh, dựng thẳng đứng mà không rõ để làm gì.** Có một cây đứng trơ trọi trên vỉa hè bên phải. Góc trên bên trái có một mái che hoặc trần nhà trông lơ lửng, kèm cánh cửa chớp và một cái móc treo lủng lẳng.
> 5. **Đá cuội ở tiền cảnh** có hình những chấm tròn lặp lại quá đều, nhìn như hoa văn in hoặc bị nhòe, không giống đá thật. Mặt đường cũng hơi dốc nghiêng lạ.
> 6. **Bố cục trống trải:** Hai nhân vật rất nhỏ, còn nửa bên phải khung hình chỉ là tường trắng trống. Mắt người xem khó tập trung, và không đọc được biểu cảm khuôn mặt, dù đây rõ ràng là khoảnh khắc cảm xúc chính.
> 7. **Nhân vật trông hơi cứng và đơ,** thiếu bóng đổ tiếp đất rõ ràng, nên có cảm giác như được đặt dán vào cảnh.

### W4T2_cas_s42a_cat — file mù `b9a36d05.jpg` — nguyên văn

> Tôi đã xem đúng một file ảnh là b9a36d05.jpg và không mở file nào khác. Dưới đây là cảm nhận của tôi với tư cách một người xem bình thường.
>
> **Tuổi:** Đây là một đứa trẻ, trông khoảng 9–12 tuổi.
>
> **Giới tính:** Trông như một bé trai. Cậu bé tóc ngắn, đội mũ len trắng có quả bông đỏ, mặc áo len cổ lọ và quần dài sẫm màu. Nét mặt khá trung tính nên tôi không chắc lắm, nhưng ấn tượng đầu tiên là con trai.
>
> **Cảm xúc:** Cậu bé bình thản và hơi trầm tư, có chút nghiêm nghị hoặc dè dặt. Mắt nhìn sang một bên chứ không nhìn thẳng. Cậu ôm chặt chiếc đèn lồng trước ngực, vai hơi khép lại, nên trông như đang lạnh (cảnh đêm, đường lát đá). Cũng có thể cậu đang chờ ai đó hoặc hơi lo lắng. Nhìn chung là yên lặng chứ không vui hay buồn rõ rệt. Nét mặt khá "đơ", ít biểu cảm, nên cảm xúc chủ yếu đọc được qua tư thế.
>
> **Những điều người xem có thể thấy lạ:**
> 1. **Ánh đèn lồng không chiếu ra xung quanh.** Đèn sáng rực, loá cả phần áo len thành một mảng cam gần như cháy sáng. Nhưng mặt đường, bức tường và cột đèn bên cạnh gần như không nhận chút ánh sáng ấm nào. Ánh sáng như chỉ dính trên người cậu bé.
> 2. **Không có bóng đổ.** Dưới chân cậu bé và dưới chân cột đèn đều không thấy bóng rõ ràng. Nhân vật trông như được dán vào cảnh chứ không thực sự đứng trên mặt đất.
> 3. **Cách cầm đèn lạ.** Hai bàn tay nắm vào vòng quai ở phía trên, còn thân đèn áp sát, như dính vào bụng. Tay trông cứng và vuông vức, giống đeo găng hơn là ngón tay.
> 4. **Ô cửa phía sau đen kịt, phẳng như một tấm bìa đen**, không có chiều sâu hay chi tiết gì bên trong.
> 5. **Cây cột đèn đường bị cắt mất phần đầu** ở mép trên khung hình, nên không thấy bóng đèn. Chiếc thang gỗ dựng cạnh đó gợi ý có người sắp lên thắp đèn, nhưng không thấy ai.
> 6. **Bố cục hơi lệch.** Chân cậu bé bị cắt sát mép dưới. Bức tường lớn thì khá trống và phẳng, vân gạch rất mờ. Cảnh tổng thể trông giống một cảnh dựng 3D chưa hoàn thiện ánh sáng.
> 7. **Dáng đứng cứng.** Hai chân thẳng, song song, nhỏ so với thân, nên trông giống một con búp bê hơn là một đứa trẻ đang đứng tự nhiên.

### doichung_sf_104.5 — file mù `261342ee.png` — nguyên văn

> Tôi đã mở đúng một file: 261342ee.png. Tôi không mở hay tìm file nào khác.
>
> Đây là khung hình hoạt hình 3D phong cách hoá, không phải ảnh người thật. Nhận xét dưới đây là cảm nhận của một người xem bình thường.
>
> **Tuổi:** Một bé gái khoảng 10–12 tuổi, có lẽ đang học cuối tiểu học hoặc đầu trung học cơ sở. Mặt tròn, mắt to và dáng người nhỏ cho thấy đây là trẻ con. Cuốn sổ có chữ "...ology", chắc là "Biology", hợp với tuổi đi học.
>
> **Giới tính:** Nữ. Cô bé buộc tóc đuôi ngựa bằng dây chun xanh, đeo khuyên tai tròn to màu hồng, mặc áo xanh có cổ cam hình cánh hoa.
>
> **Cảm xúc:** Cô bé đang lo lắng, bối rối và hơi ngạc nhiên pha sợ. Có bốn dấu hiệu:
> - Lông mày nhướng lên và chụm về giữa, một bên cao hơn bên kia, kiểu "ơ… thật à?".
> - Mắt mở to và liếc lên phía trên bên trái khung hình, như đang nhìn vật gì hoặc ai đó ngoài khung.
> - Miệng hé tròn nhỏ, như vừa thốt "oh".
> - Hai tay ôm chặt cuốn sổ vào ngực, một tư thế tự vệ và tìm chỗ dựa.
>
> Tổng thể là cảm giác "lạc lõng, không chắc chuyện gì đang xảy ra" giữa khu rừng lúc chiều tà.
>
> **Điều người xem có thể thấy lạ:**
> 1. **Bím tóc đuôi ngựa** là điểm lạ nhất. Nó rất to so với đầu, dựng ngược lên và cong như ngọn lửa hay đuôi bọ cạp, cứng như không chịu trọng lực. Phần đuôi lại xơ, tua ra thành sợi, có sợi màu xám bạc, nhìn giống chổi hoặc cọ vẽ cũ. Chất tóc ở đây khác hẳn phần tóc mái mượt trên đầu, nên trông như ghép từ hai kiểu tạo hình khác nhau.
> 2. **Khung hình rất dẹt** (1920×804, khoảng 2,39:1, tỉ lệ màn ảnh rộng), không phải 16:9.
> 3. **Chữ trên sổ bị tay che**, chỉ đọc được "...ology" kèm hình chiếc lá.
> 4. Vòng tay đồng hồ vàng–đỏ và khuyên tai hồng rất to, màu rất gắt so với nền rừng tối. Có thể đây là chủ ý thiết kế, nhưng chúng khá nổi bật.
> 5. Nấm đỏ bóng loáng như nhựa rải rác trên cỏ, hợp với không khí cổ tích nhưng hơi giả.
>
> **Lưu ý cho dự án:** Chất lượng dựng hình trông như khung hình cắt từ một phim hoạt hình thương mại đã phát hành, không giống bản render nội bộ. Nếu đây là tham chiếu, cần ghi vào `RIGHTS.md` và không sao chép thiết kế nhân vật, theo luật cứng trong CLAUDE.md. Tôi chưa kiểm nguồn vì chỉ được mở một file này.

### doichung_sf_332 — file mù `7a570475.png` — nguyên văn

> Tôi đã mở đúng một file: 7a570475.png. Tôi không mở hay tìm file nào khác.
>
> **Người xem thấy gì:**
> - **Tuổi:** trông như một người phụ nữ trung niên, khoảng 40–55 tuổi. Mái tóc vàng rối và cách trang điểm đậm kiểu thập niên 80 gợi cảm giác bà ấy đang cố giữ vẻ trẻ trung.
> - **Giới tính:** nữ. Có thể nhận ra qua lông mi dài, phấn mắt xanh, son tím, bông tai to hình tam giác và chuỗi hạt.
> - **Cảm xúc:** giận dữ và bực bội, xen chút ghê sợ hoặc muốn né tránh. Bà nhắm chặt mắt, nhíu mày gắt, miệng mở méo như đang gào hay gầm gừ, nghiến răng. Tay giơ thẳng về phía ống kính như muốn nói "Dừng lại!" hoặc đẩy thứ gì đó ra xa. Đầu nghiêng và ngả ra sau, trông như đang lùi lại.
>
> **Những điểm người xem có thể thấy lạ:**
> 1. Dưới mắt có những vệt tối như lông mi giả hoặc mascara bị nhoè. Khi mắt nhắm, chúng trông như bóng đen kỳ quặc.
> 2. Toàn cảnh chìm trong ánh xanh lạnh, nhưng mũi lại hồng rõ, trông như được tô riêng và lệch tông với phần còn lại của mặt.
> 3. Miệng mở rất to và méo thành hình bầu dục lệch, răng lởm chởm và thưa. Hiệu ứng khá mạnh, gần như hình mặt nạ.
> 4. Ở cằm hoặc má trái có một vết xước hay vệt sẫm nhỏ, không rõ là vết thương hay lỗi bề mặt.
> 5. Khó thấy cổ, nên đầu và chuỗi hạt trông hơi "trôi", không rõ nối với thân thế nào.
> 6. Bàn tay rất to vì ở sát ống kính. Ngón cái hơi mờ và ngắn so với các ngón còn lại, trông hơi gượng.
> 7. Nền mờ, sương mù và tối, nên người xem không biết nhân vật đang ở đâu hay đang chống lại cái gì.
>
> **Nhận xét thêm:** Khung hình nhìn rất giống ảnh cắt từ một phim hoạt hình 3D thương mại chuyên nghiệp, có dấu nén video. Nếu ảnh này là tham chiếu từ phim có sẵn thì cần ghi vào RIGHTS.md và không sao chép thiết kế nhân vật, theo luật cứng của dự án.
