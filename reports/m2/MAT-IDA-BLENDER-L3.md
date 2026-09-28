# CỬA MẶT IDA — A′: LƯỢT SỬA 'bl' (L3) · KIỂM MÙ TRƯỚC CỔNG 6

Nhánh: `claude/cine-lab-m2-cong5-layout-24o5fp` (merge W4 lượt 3 @32a3700). Ngày 29/09/2026 (giờ máy chủ 28/09 22:40 UTC).
Quyết định gốc: AUTHORSHIP "Cửa mặt Ida", dòng A′.
- **Cổng 6 vẫn khoá.** Layout trên main không đổi.
- `IDA_STYLE` mặc định vẫn `'aa'`. P đo lại sau khi merge: dò s02, s37, s39, 9 ảnh nhỏ, lệch **0 px**.

## 0. Kết luận
- W4 **qua điều kiện dừng**: cổ, mũ, búi và da đều sửa rõ rệt (P tự xem bảng so sánh). W4 dùng khoảng 122 nghìn token, trong hạn khoảng 300 nghìn.
- **Kiểm mù (4 khung PA1, L11 gốc): TRƯỢT tiêu chí cảm xúc.**
  - Tuổi và giới **4/4 ✔**.
  - Cảm xúc chấm rõ **2/4 ✘**: cả hai nhịp "cười buồn" đọc ra **cười ấm, không buồn**.
  - Từ khoá búp bê/mặt nạ/con rối/ma-nơ-canh/tượng sáp chỉ vào mặt/đầu Ida: **0/4 ✔** (đếm bằng máy). Đây là **lần đầu** khung PA1 không bị gọi búp bê/mặt nạ. Lưu ý ngữ nghĩa: khung goodnight có "da mịn như đất sét hoặc sáp, hơi giống tượng"; nếu coi câu này là "tượng sáp" thì thành 1/4.
  - Đối chứng **0/2 ✔**.
  - "Người thật / lạc phong cách" **0/6**.
- Khung **chính diện** vẫn bị gọi "búp bê" **2/2** ("mắt búp bê", "nửa người nửa búp bê"), kèm "mặt nạ hay tượng". Hai khung này còn **lưỡng lự về giới** và bị chê "trán hói".
- Theo quyết định: **không thêm lượt.** Mục 5 là các lựa chọn cho chủ dự án.

## 1. Lượt sửa (W4): trước / sau
Ảnh 4 góc: trước `reports/m2/cong5/w4/L2_eevee_4goc.jpg` → sau `reports/m2/cong5/w4/L3_eevee_4goc.jpg`. Bảng so cùng khung PA1_goodnight, L11 gốc: `reports/m2/cong5/w4/L3_SO_goodnight_aa-ai-bl.jpg` (A-α / A-i / 'bl' lượt 2 / 'bl' lượt 3).

| Việc (lệnh) | Đã làm | Kiểm mù nói gì (PA1 L3) |
|---|---|---|
| a. Cổ liền; khăn và cổ áo theo 'bl' | Kẹp bán kính cổ ≤ 0,205 H; glb mang lưới khoảng cách của da 'bl' cho khăn và cổ áo | **Hết** lời "cổ rách / da khuyết" (lượt 2: 3/4 khung). Khung chính diện: "không thấy cổ, đầu cắm vào khăn" |
| a. Mũ ngồi lên sọ | Miệng mũ đo theo khối tóc; tóc bị ép dưới băng | **Vẫn** "mũ lơ lửng / đặt hờ" (3/4 khung PA1, 2/2 chính diện) |
| a. Búi có vân lọn | Lõi + 40 lọn quấn | "búi như cuộn len / sợi bện" (hết "quả bóng trơn") |
| a. Chân tóc | Dày từ mép, hạ ở trán và thái dương | Chính diện choked: "trán lộ rất rộng… như đầu hói"; PA1 keep: "mảng da trơn như cạo trọc sau tai" |
| a. Hoa tai | Treo điểm thấp nhất của dái tai | PA1 keep: "khuyên… như cắm vào má"; chính diện: "treo trên má" (vẫn còn) |
| b. Da già | Loang hai tầng, đốm tuổi, nếp khối sâu hơn, độ nhám theo vùng | Hết "da em bé" ở PA1. Chính diện neutral: "má căng như mặt trẻ con"; goodnight: "da như đất sét hoặc sáp, hơi giống tượng"; brighter: "bóng như sáp hoặc nhựa" |
| c. Mắt góc nghiêng | Mí mở hơn, squint giảm, cheekRaise không kéo khe | PA1 last "mắt nheo lại" đọc được; brighter, keep, goodnight: "mắt gần như nhắm / khe nhỏ" (vẫn còn) |
| d. Biểu cảm | frown, press, chinRaise về 1,0 + `corr_mouth`; sad_smile = cười nén + `corr_smile_lip`, browInnerUp ×2,2 | choked đọc **đúng** (buồn, cam chịu). sad_smile **vẫn đọc thành cười ấm** (last: "không thấy dấu hiệu buồn"; goodnight: "mỉm cười nhẹ… cũng có thể đọc là buồn nhẹ") |
| e. Tỷ lệ | Giữ đầu và tai MPFB; đo c3_views | Mục 3 |
| f. Đèn | L11 gốc ở mọi khung PA1 | — |

Lỗi ngoài phạm vi, vẫn còn: bàn tay trên cột "như thanh gỗ / xúc xích", "mẩu tay cam" sau cột (2/4 khung PA1). Để Cổng 6; MPFB có tay đúng giải phẫu.

## 2. Kiểm mù (1 vòng, 8 subagent)
Quy trình và cách chấm y hệt lượt 2:
- đích last và goodnight = cười buồn (cần CẢ cười lẫn buồn); brighter và keep = nghẹn (✔ khi đọc ra buồn, nén hoặc tủi thân);
- lượt này không tính "nửa đúng";
- đếm bằng máy trên nguyên văn.

| Khung | Tuổi / giới | Cảm xúc đọc được | Chấm | Từ khoá chỉ vào mặt/đầu Ida | Ghi chú |
|---|---|---|---|---|---|
| **PA1_last** (cười buồn) | nữ ~70 ✔ | "dễ chịu và ấm áp… mỉm cười nhẹ… trìu mến, hoài niệm… **không thấy dấu hiệu buồn**" | ✘ | 0 | tay "thanh gỗ/xúc xích"; "mẩu cam lơ lửng" |
| **PA1_goodnight** (cười buồn) | nữ 65–75 ✔ | "bình thản, hơi hoài niệm, dịu dàng… mỉm cười nhẹ… biểu cảm khá mờ nhạt… **cũng có thể** đọc là mệt mỏi hoặc buồn nhẹ" | ✘ (sát biên: buồn chỉ là cách đọc thay thế) | 0 theo máy; ngữ nghĩa gần: "như đất sét hoặc **sáp**, hơi giống **tượng**" | tóc "len đan"; mũ lơ lửng; mắt khe |
| **PA1_brighter** (nghẹn) | nữ 65–75 ✔ | "trầm ngâm, hơi buồn… cô đơn, có chút tiếc nuối" | ✔ | 0 ("bóng như sáp hoặc nhựa": không phải từ khoá) | tay không nắm cột |
| **PA1_keep** (nghẹn) | nữ 65–75 ✔ | "buồn, mệt mỏi, có phần cam chịu hoặc hơi cau có… không rõ lắm" | ✔ | 0 | khuyên "cắm vào má"; da trơn sau tai |
| s37 chính diện neutral (chỉ báo số) | 65–75, "nhiều khả năng" nữ, "hơi lưỡng lự" | buồn, hơi lo, hờn dỗi | — | 3: "mắt **búp bê**" ×2, "kiểu **mặt nạ** hay tượng" | "má… như mặt trẻ con"; khuyên trên má; tai "yêu tinh" |
| s37 chính diện choked (chỉ báo số) | 70–80, "nhiều khả năng" nữ, "không chắc 100 %" | buồn, lo âu, như sắp khóc ✔ | — | 2: "mắt **búp bê**", "nửa người nửa **búp bê**" | "trán… như đầu hói"; mũ lơ lửng; "không có cổ"; miệng |
| Đối chứng SF 104,5 s | bé gái 10–12 | ngạc nhiên, lo, bối rối | — | 0 | — |
| Đối chứng SF 332 s | nữ 40–50 | ghê sợ, tức giận | — | 0 | — |

| Tiêu chí (không hạ), khung PA1 | Kết quả | |
|---|---|---|
| Tuổi và giới 4/4 | 4/4 | ✔ |
| Cảm xúc ≥ 3/4 (chấm rõ) | **2/4** | **✘** |
| 0/4 từ khoá chỉ vào mặt/đầu Ida | **0/4** theo máy (1/4 nếu tính "sáp… hơi giống tượng") | ✔ (theo máy) |
| Đối chứng 0/2 | 0/2 | ✔ |
| Thêm: "người thật / lạc phong cách" | 0/6 | — |

**Kết quả: TRƯỢT** (tiêu chí cảm xúc).

## 3. c3_views 'bl' mới và nháp characters v1.5
- Bảng 8 góc và các thay đổi so với v1.4: `reports/m2/cong5/characters-v1.5-NHAP.md`. Chưa khoá; không sửa bible hay ida.json.
- Thân ở 0° là **2,272** (v1.4: 2,682; −15,3 %).
- Trong ±5 % so với sheet v1.4: ±45°, ±90°. Lệch hơn 5 %: 0°, ±135°, 180°.
- Tác động tới Cas: ở khung hai người, đầu Ida to hơn tương đối khoảng 13–18 %. Chủ dự án chọn (i) chấp nhận, hoặc (ii) cho Cas đi quy trình MPFB ở Cổng 6.

## 4. Số liệu 3 lượt và bảng so sánh mặt (khung PA1, cùng câu hỏi, cùng cách chấm)
| Mặt / lượt | Đèn | Tuổi + giới | Cảm xúc rõ | Từ khoá chỉ vào mặt/đầu | Chính diện "búp bê/mặt nạ" | Lỗi chính còn lại |
|---|---|---|---|---|---|---|
| A-α (W3, 28/09) | L11 gốc (đèn cũ) | 4/4 | 2/4 | 3/4 | 4/4 (lần 6) | da nhựa, nửa dưới mặt phình; không có khẩu hình |
| A-i (vòng 2 chính diện; PA1 chỉ 1 khung) | cũ | — | — | 1/1 | 9/10 | nửa dưới mặt phình, tai, ranh tóc |
| 'bl' lượt 1 (hàm khoảng cách) | — | không kiểm (dừng) | — | — | — | hình hỏng |
| 'bl' lượt 2 (MPFB) | L11 17,5° | 4/4 | 1/4 | 1/4 (cổ khuyết) | 2/2 | cổ khuyết, mũ, búi, mắt khe |
| **'bl' lượt 3 (MPFB + sửa)** | **L11 gốc** | **4/4** | **2/4** | **0/4** | 2/2 | cười buồn → cười ấm; mũ "lơ lửng"; mắt khe ở góc nghiêng; khuyên; chính diện "mắt búp bê" |
| Đối chứng SF (mỗi lượt) | — | — | — | 0/2 | — | — |

Đọc số: trên PA1, 'bl' L3 là mặt **duy nhất** 0/4 từ khoá, và giữ tuổi, giới 4/4. Thứ còn thiếu cho đạt là **một kênh biểu cảm** (cười buồn). Khung chính diện vẫn trượt với mọi mặt.

## 5. Quyết định cần chủ dự án (không thêm lượt)
| | **A — Nhận 'bl' L3, chấp nhận trượt tiêu chí cảm xúc** | **B — Nhận 'bl' L3 và đổi đích diễn 2 nhịp đầu L4** | **C — Lùi về PA1 + A-i (hoặc A-α)** |
|---|---|---|---|
| Nội dung | Duyệt nháp v1.5, khoá SHA, đổi mặc định 'bl'; mở Cổng 6 với rủi ro ghi rõ: nhịp cười buồn (last, goodnight) chưa đọc đúng ở ảnh tĩnh; cấm cận mặt chính diện ở cao trào | Như A, nhưng chủ dự án đổi đích diễn của "That's the last one" và "Goodnight, old street" từ cười buồn sang một nét khác. Đây là **quyết định sáng tạo, không phải cách để vượt ngưỡng**: chỉ làm nếu nét mới đúng ý đạo diễn | Giữ mặt cũ (A-i có rig; A-α không có khẩu hình), dàn dựng PA1 |
| Ưu | Mặt duy nhất hết "búp bê/mặt nạ" ở PA1; giải phẫu đúng; có shape key và tay MPFB cho Cổng 6 | Như A; nếu nét mới hợp thì các lần đọc hiện có ("trìu mến, hoài niệm") đã khớp | Không phải khoá tài sản mới |
| Nhược | Trượt tiêu chí 2 (2/4). Cười buồn là nhịp quan trọng của L4 | Đổi nghĩa diễn của cảnh cao trào; có rủi ro "đổi đích cho vừa kết quả" | A-α 3/4 và A-i 1/1 bị gọi búp bê ở PA1; A-α không lip-sync được |
| Tác động | characters v1.5, ida.json, LIBRARY, LOCK; luật C3 trên layout với 'bl'; quyết đồng bộ Cas | Như A + ghi AUTHORSHIP đích diễn mới | Như trước lượt Blender |
| Rủi ro | Người xem đọc nhịp chia tay thành vui | Mất sắc thái "cười mà buồn" của câu Goodnight | Quay lại lỗi búp bê ở cao trào |

**Khuyến nghị của P: A.**
- Trên khung PA1, 'bl' L3 là kết quả tốt nhất trong mọi phương án mặt đã kiểm mù từ Cổng 4 tới nay (A1, A3, A-α, A-i ×2, 'bl' L2, L3): 0/4 từ khoá, tuổi và giới 4/4, nghẹn đọc đúng 2/2.
- Tiêu chí còn trượt là một kênh biểu cảm, không phải lỗi hình khối.
- **Không khuyến nghị B** như một cách vượt tiêu chí. B chỉ hợp lệ nếu chủ dự án thực sự muốn nét diễn khác.
- Mọi việc sửa tiếp (cười buồn, mũ, khuyên, mắt góc nghiêng) sẽ là việc của Cổng 6. Việc đưa các sửa này vào Cổng 6 cần chủ dự án duyệt, vì trái với điểm (a) mà Claude bên ngoài đã nêu ("sửa và kiểm lại TRƯỚC Cổng 6").

Cần chủ dự án quyết thêm nếu chọn A hoặc B:
- (i) duyệt nháp v1.5;
- (ii) đồng bộ tỷ lệ Cas: chấp nhận, hay MPFB ở Cổng 6.

## 6. Thời gian, token, hàng đợi
| Việc | Thời gian | Token (ngữ cảnh tích luỹ do công cụ báo) | Hàng đợi |
|---|---|---|---|
| W4 lượt 3 (21:56–22:45 UTC) | 49 phút | 608 635 khi kết thúc; lượt 3 ≈ **121 700** (hạn khoảng 300 nghìn) | 36 việc, chờ 0 s, chạy 732 s (làn nặng 15 việc 423 s; làn nhanh 21 việc 309 s); EEVEE 4 góc chạy ngoài hàng đợi, 77–99 s mỗi lần |
| Làm lại (W4) | 11 lần dựng glb (cổ 2, mũ và tóc dưới băng 3, búi 3, cười nén 3); ảnh điều kiện dừng 5 lần | — | — |
| P kiểm mù (8 subagent) | 22–38 s mỗi subagent | 48 644–50 251 mỗi subagent | P dò 'aa' 44 s |
| Cả gói Blender, 3 lượt | khoảng 2 giờ 38 phút | W4 khoảng 609 nghìn; P kiểm mù 13 + 8 subagent | — |

## 7. Nguyên văn subagent (cả đối chứng)
#### L3_BL_PA1_last — file mù `11df4201.jpg` — nguyên văn

> Tôi đã mở đúng một file theo yêu cầu (11df4201.jpg) và không đọc file nào khác. Đây là cảm nhận của tôi với tư cách một người xem bình thường.
>
> **Người trong ảnh**
> - **Tuổi:** một bà cụ, trông khoảng 70 tuổi, có thể từ 65 đến 75. Tóc bạc trắng búi sau gáy, mặt có nếp nhăn, má hơi hóp.
> - **Giới tính:** nữ. Có búi tóc, đeo hoa tai tròn nhỏ màu vàng, mặc áo khoác dạ xanh rêu kiểu cổ, quàng khăn len đỏ gạch và đội mũ phớt đen.
> - **Cảm xúc:** dễ chịu và ấm áp. Bà mỉm cười nhẹ, mắt nheo lại, nhìn về phía cột đèn đường. Tôi đọc thấy sự trìu mến, có chút hoài niệm, như gặp lại một thứ quen thuộc. Tay bà nắm cột đèn nhẹ nhàng chứ không gồng. Tôi không thấy dấu hiệu buồn hay lo âu.
>
> **Những điểm người xem có thể thấy lạ**
> 1. **Bàn tay ở cột đèn là điểm lạ nhất.** Các ngón dài, thẳng và cứng như những thanh gỗ hay xúc xích xếp chồng lên nhau. Số ngón khó đếm và trông như nhiều hơn năm. Ngón tay không uốn theo thân cột mà giống như dán lên bề mặt. Cổ tay nối vào ống tay áo cũng không rõ.
> 2. **Một mẩu màu cam lơ lửng ở bên trái thân cột.** Nó nằm ngay dưới chụp đèn, ngang tầm cằm bà cụ, trông như đầu ngón tay hay ngón cái tách rời khỏi cơ thể. Người xem không hiểu đó là tay ai hay vật gì.
> 3. **Da rất cam.** Mặt và tay có màu cam đậm như bị hơ lửa, gắt hơn ánh đèn vàng thông thường.
> 4. **Mũ và tóc hơi cứng.** Mũ trông như đặt hờ trên đầu, không ôm vào tóc. Tóc và búi có vân như cuộn len hay sợi bện, không giống tóc thật.
> 5. **Thanh ngang của cột đèn khá lạ.** Nó to, và đầu mút tròn làm cả cụm trông giống chuôi kiếm hay dao găm hơn là tay treo của đèn đường.
> 6. **Mảng gạch lộ ra trên tường** (bên phải, phía trên) và cột đèn thứ hai phía sau thì hợp lý, có vẻ cố ý. Chỉ là bức tường khá trơn và mờ nên mảng gạch trông như dán thêm vào.
>
> **Tóm lại:** gương mặt và cảm xúc đọc rõ và dễ thương. Chỗ làm người xem khựng lại chủ yếu là bàn tay nắm cột đèn và mẩu màu cam lơ lửng cạnh cột.

#### L3_BL_PA1_goodnight — file mù `5743ab83.jpg` — nguyên văn

> Tôi đã xem đúng một ảnh: /tmp/claude-0/-home-user-cine-lab/5b95043d-dd86-5cf7-9b06-17de07cfe1f8/scratchpad/matai/bl3/5743ab83.jpg. Đây là khung hình dựng 3D, chụp nghiêng mặt phải.
>
> **Người xem bình thường sẽ thấy:**
> - **Tuổi:** một bà cụ khoảng 65–75 tuổi. Tóc bạc trắng búi sau gáy, lông mày bạc, có nếp nhăn ở đuôi mắt và khoé miệng.
> - **Giới tính:** nữ. Dấu hiệu là búi tóc, bông tai vàng dạng hai hạt tròn và khăn len quấn cổ.
> - **Cảm xúc:** bình thản, hơi hoài niệm, có chút dịu dàng. Mắt nhắm hờ hoặc nhìn xuống, khoé miệng hơi nhếch như đang mỉm cười nhẹ khi nhớ lại điều gì đó. Ánh sáng ấm màu cam hắt từ phía trước góp phần tạo cảm giác ấm áp, trầm lắng. Tuy vậy biểu cảm khá mờ nhạt, nên người xem cũng có thể đọc là mệt mỏi hoặc buồn nhẹ.
>
> **Những điểm người xem có thể thấy lạ:**
> 1. **Tóc trông như sợi len hoặc dây thừng đan**, không giống tóc người. Có những mảng vân chéo lặp lại, rõ nhất ở búi và vùng trên tai. Ở mép tóc sát trán còn có các mảng răng cưa, vỡ vụn.
> 2. **Mũ nổi lơ lửng:** vành mũ phớt nâu nằm cao phía trên đầu, không thấy phần chóp mũ ôm vào tóc, nên trông như mũ không đội lên đầu.
> 3. **Mắt gần như không thấy rõ:** chỉ là một khe nhỏ, thiếu chi tiết mí và lông mi, nên khó đọc ánh nhìn.
> 4. **Da mịn như đất sét hoặc sáp**, hơi giống tượng. Riêng má và cổ lại mịn, căng so với nếp nhăn ở mắt, nên tuổi trông không nhất quán.
> 5. **Tai hơi to và thô** so với khuôn mặt.
> 6. **Mặt hơi phẳng, dẹt:** mặt nghiêng khá bằng, cằm lùi vào trong khăn, miệng nhỏ và mờ.
> 7. **Ánh sáng cam rất mạnh**, như bị đèn chiếu thẳng vào mặt. Viền sáng quanh mũi và cằm hơi "phát sáng", thiếu tự nhiên.
> 8. **Khăn len đan rất đẹp và chi tiết.** Vì vậy nó lại càng làm nổi bật chỗ tóc và mắt còn thô.
>
> **Tóm lại:** một bà cụ hiền, đang trầm tư hoặc hồi tưởng với nụ cười rất nhẹ. Những lỗi dễ bị chú ý nhất là tóc giống len đan (có mảng vỡ ở mép trán), mũ lơ lửng và mắt thiếu chi tiết.

#### L3_BL_PA1_brighter — file mù `b48b6d7f.jpg` — nguyên văn

> Tôi chỉ mở một file: /tmp/claude-0/-home-user-cine-lab/5b95043d-dd86-5cf7-9b06-17de07cfe1f8/scratchpad/matai/bl3/b48b6d7f.jpg. Dưới đây là cảm nhận của một người xem bình thường.
>
> **Tuổi và giới tính:** Đây là một bà cụ, khoảng 65–75 tuổi. Tóc bà bạc trắng, búi gọn sau gáy. Mặt có nếp nhăn và má hơi xệ. Bà đeo khuyên tai vàng, đội mũ phớt đen, quàng khăn len đỏ và mặc áo khoác dạ xanh rêu cài khuy.
>
> **Cảm xúc:** Bà có vẻ trầm ngâm, hơi buồn, như đang nhớ lại điều gì. Bà nghiêng mặt về phía ngọn đèn đường. Mắt bà gần như nhắm hoặc nheo lại, khoé miệng hơi trễ xuống. Cảm giác chung là tĩnh lặng, cô đơn, có chút tiếc nuối. Tôi không thấy bà vui hay sợ hãi. Ánh đèn vàng ấm giữa nền sương xám lạnh càng làm rõ vẻ hoài niệm.
>
> **Những điểm người xem có thể thấy lạ:**
> 1. **Bàn tay phải không thật sự nắm cột đèn.** Các ngón tay xoè thẳng, duỗi cứng và úp phẳng ra phía trước thân cột, trông như đang lơ lửng hoặc xuyên qua cột. Đây là điểm dễ gây chú ý nhất vì bàn tay lại được chiếu sáng rõ.
> 2. **Một mẩu màu da cam nhỏ ló ra sau cột**, ở ngang tầm vai bà. Có lẽ đó là đầu ngón tay của bàn tay kia, nhưng nó quá nhỏ và rời rạc so với cơ thể nên nhìn khó hiểu, như một vật lạ.
> 3. **Tỉ lệ đèn đường hơi kỳ.** Đầu đèn to và thấp, ngang ngay trước mặt bà, còn thân cột thì ngắn. Trông giống đồ chơi hay đạo cụ sân khấu hơn là đèn đường thật.
> 4. **Chất liệu da mặt hơi bóng như sáp hoặc nhựa.** Mắt gần như không thấy, nên khó đọc biểu cảm.
> 5. **Búi tóc có vân sọc như cuộn len**, không giống tóc thật. Có thể đây là chủ ý của phong cách hoạt hình, nhưng vẫn gây chú ý.
> 6. **Bức tường nền phẳng và mờ như phông vẽ.** Trên tường có một mảng gạch lộ ra do bong vữa, cùng một đường nối ngang ở bên phải. Cột đen dọc ở mép trái khung hình không rõ là vật gì.
> 7. **Không thấy tay trái của bà**, dù tư thế có vẻ đang ôm cột bằng cả hai tay.

#### L3_BL_PA1_keep — file mù `eb1f7668.jpg` — nguyên văn

> Đã mở đúng một file: /tmp/claude-0/-home-user-cine-lab/5b95043d-dd86-5cf7-9b06-17de07cfe1f8/scratchpad/matai/bl3/eb1f7668.jpg. Ảnh là cận cảnh góng nghiêng, nhân vật quay mặt sang phải, dựng bằng 3D.
>
> **Tuổi và giới tính (theo cảm nhận của người xem):** Một bà cụ, chừng 65–75 tuổi. Tôi đoán vậy vì tóc bạc búi sau gáy, có đeo khuyên tai, quấn khăn len và đội mũ phớt. Mặt có nếp nhăn ở đuôi mắt và khoé miệng.
>
> **Cảm xúc:** Mắt nheo gần như nhắm, khoé miệng trễ xuống, môi mím. Tôi thấy bà buồn, mệt mỏi, có phần cam chịu hoặc hơi cau có, như đang nhìn vào điều gì làm mình phiền lòng. Tuy vậy, vì mắt gần như bị che khuất nên cảm xúc không rõ lắm. Người xem có thể hiểu là "buồn", "khó chịu" hoặc "đang nheo mắt vì nắng".
>
> **Những điểm người xem có thể thấy lạ:**
> 1. **Khuyên tai lơ lửng:** Khuyên hình quả tạ nằm hẳn dưới dái tai, như cắm vào má hay quai hàm chứ không treo từ dái tai. Đây là điểm dễ thấy nhất.
> 2. **Tóc trông giả:** Tóc như những dải nhựa hay nét cọ xếp chồng, có răng cưa và các vệt đan chéo lộn xộn ở mép, nhất là quanh thái dương và phía trên tai. Búi tóc giống cuộn len. Đường chân tóc sau tai cắt ngang cứng như mép mũ bảo hiểm hay tóc giả, để lộ một mảng da trơn như cạo trọc phía trên và sau tai.
> 3. **Mũ không khớp với đầu:** Mũ như đặt hờ trên lớp tóc, không ôm đầu. Đầu mũ lại chạm đúng cây cột dọc phía sau, nhìn như dính vào cột.
> 4. **Tỉ lệ đầu và cổ:** Đầu to, cổ và gáy rất dày. Vùng má và hàm liền một khối mềm như đất nặn. Cằm và môi dưới hơi "chảy", khó nhận ra đường viền.
> 5. **Mắt và lông mày:** Mắt gần như không thấy, lông mày chỉ là một vệt trắng mờ.
> 6. **Hậu cảnh:** Mảng gạch lộ ra trên bức tường sơn trắng có hình ngôi sao sắc cạnh, trông như miếng dán phẳng hơn là vữa bong thật.
> 7. **Ánh sáng:** Mặt được chiếu nắng cam ấm, trong khi nền lại lạnh và mờ. Chuyện này tự nó không sai, nhưng làm nhân vật trông hơi "tách" khỏi cảnh.
>
> **Điểm tốt:** Khăn len đan có chất liệu thuyết phục. Tai được dựng khá chi tiết.

#### L3_BL_s37_neutral — file mù `64049037.jpg` — nguyên văn

> Tôi đã xem đúng một file 64049037.jpg và không mở file nào khác. Đây là cận mặt một nhân vật hoạt hình 3D, trên nền tối, ánh sáng ấm cam chiếu từ phía trước.
>
> **Tuổi:** khoảng 65–75. Tóc và lông mày bạc trắng, có nếp nhăn quanh mắt và dưới mắt. Tuy vậy, má và cằm căng tròn như mặt trẻ con, nên nhìn thoáng qua cũng có thể đoán nhân vật trẻ hơn.
>
> **Giới tính:** nhiều khả năng là nữ, một bà cụ, vì có đeo khuyên tai hạt tròn màu vàng. Mặt khá trung tính: tóc bị mũ che gần hết và nét mặt không rõ nữ tính, nên người xem có thể hơi lưỡng lự.
>
> **Cảm xúc:** buồn, hơi lo, có chút hờn dỗi hoặc ngậm ngùi. Khoé miệng trễ xuống, môi mím, mắt mở to nhìn thẳng. Lông mày hơi nhíu, nhưng không đủ rõ để đọc thành giận. Cảm giác chung là buồn lặng lẽ, hơi ngơ ngác.
>
> **Những điểm người xem có thể thấy lạ:**
> 1. **Tóc trông như một cái vòng hay mũ len trắng:** tóc bạc tạo thành một khối trắng xếp sọc như vải bông, ôm quanh đầu dưới vành mũ, không giống sợi tóc thật.
> 2. **Khuyên tai mọc ra từ má hoặc hàm:** khuyên bên trái khung hình (tai phải nhân vật) treo trên má, sát góc hàm, không gắn vào dái tai. Bên kia gắn gần dái tai hơn nhưng vẫn hơi lệch.
> 3. **Tai to và nhọn, đặt hơi cao,** trông giống tai yêu tinh.
> 4. **Mắt quá tròn và to, hơi trố,** tròng nâu đồng nhất, trông như mắt búp bê. Ánh nhìn hơi vô hồn và không khớp hẳn với nét buồn ở miệng.
> 5. **Da sần như vỏ cam, mờ đục như sáp hoặc đất nặn,** kiểu mặt nạ hay tượng.
> 6. **Không thấy cổ:** đầu như cắm thẳng vào khăn len đỏ quấn cao. Cằm và khối mặt trông như đặt rời trên khăn.
> 7. **Mũ phớt đen quá lớn so với đầu,** vành rộng. Vành mũ và khối tóc tách nhau thành từng lớp rời.
> 8. **Vật thể lạ ở góc dưới bên trái:** có một đường cong viền cam hoặc vàng lọt vào mép khung, không rõ là gì.
> 9. **Sống mũi hơi vẹo sang một bên,** mặt hơi lệch, không cân.
>
> **Tóm lại:** người xem sẽ thấy đây là một bà cụ buồn bã, trầm lặng. Nhưng tổng thể gây cảm giác hơi rợn kiểu thung lũng kỳ lạ (uncanny valley), chủ yếu do mắt búp bê, khuyên tai đặt sai chỗ, tóc giống vải và da mặt như sáp.

#### L3_BL_s37_choked — file mù `a877bf12.jpg` — nguyên văn

> Tôi đã mở đúng một file ảnh được chỉ định và không mở file nào khác.
>
> **Tuổi:** một người già, trông khoảng 70–80 tuổi. Tóc bạc trắng, lông mày bạc, trán và khóe mắt có nếp nhăn, má hơi xệ.
>
> **Giới tính:** nhiều khả năng là nữ, tức một bà cụ. Dấu hiệu chính là đôi hoa tai tròn màu vàng. Tuy vậy, khuôn mặt khá trung tính. Nếu bỏ hoa tai đi, người xem cũng có thể đoán đây là một ông cụ, vì mũ trông giống mũ phớt, tóc ngắn và mặt tròn to. Tôi không chắc 100% về giới tính.
>
> **Cảm xúc:** buồn, lo âu, như sắp khóc. Hai đầu lông mày trong nhướng lên, khóe miệng trễ xuống, môi hơi hé và méo. Ánh mắt ngước lên như đang van nài hoặc bất lực. Có thể hiểu là đau lòng, tủi thân hoặc sợ hãi nhẹ.
>
> **Những điểm người xem có thể thấy lạ:**
> 1. **Tóc trông giả.** Tóc chỉ là một dải trắng xù quanh vành mũ, giống vòng bông hay mũ tắm. Phần trán lộ ra rất rộng và nhẵn như đầu hói.
> 2. **Mũ như đang lơ lửng.** Vành mũ không có vẻ đè lên đầu hay lên tóc, nhìn như đặt hờ phía trên.
> 3. **Miệng méo và bất thường.** Bên trong miệng là một mảng phẳng màu cam nhạt, không thấy răng hay lưỡi rõ ràng. Khóe miệng bên trái (phía người xem) có nếp gấp trắng trông như bị rách hoặc lỗi hình. Môi trên và môi dưới lệch nhau.
> 4. **Không có cổ.** Đầu cắm thẳng vào khăn len, cằm và hàm to phình ra. Đầu có vẻ quá to so với cơ thể.
> 5. **Tai và hoa tai kỳ lạ.** Tai bên trái (phía người xem) gần như không thấy, còn hoa tai treo khá thấp và xa. Tai bên phải to, dẹt, và hoa tai dính ở vị trí hơi lạ.
> 6. **Da sần như đất sét hay vỏ cam.** Lông mày trông như vài nét sơn xám vẽ đè lên, không giống lông thật.
> 7. **Mắt bóng như mắt búp bê,** hơi vô hồn dù nét mặt đang buồn.
> 8. **Ánh sáng.** Mặt bị chiếu cam rất gắt trên nền đen tuyền. Ở góc dưới bên trái có một đường viền cam sáng của một vật gì đó không rõ.
>
> **Ấn tượng chung:** đây là nhân vật hoạt hình 3D phong cách hoá đang diễn cảm xúc buồn, và cảm xúc đọc được khá rõ. Tuy vậy, cái miệng, mái tóc, phần không có cổ và chiếc mũ lơ lửng dễ tạo cảm giác "hơi rợn", nửa người nửa búp bê (uncanny). Chi tiết dễ khiến người xem bị phân tâm nhất là cái miệng.

#### doichung_sf_104.5 — file mù `a18ee199.png` — nguyên văn

> Tôi đã mở đúng một file theo yêu cầu: /tmp/claude-0/-home-user-cine-lab/5b95043d-dd86-5cf7-9b06-17de07cfe1f8/scratchpad/matai/bl3/a18ee199.png
>
> Người xem bình thường sẽ thấy như sau:
>
> **Tuổi, giới tính:** Đây là một bé gái hoạt hình 3D, trông khoảng 10–12 tuổi. Em có tóc đen buộc đuôi ngựa cao bằng dây buộc tóc xanh ngọc, mái lưa thưa, đeo khuyên tròn to màu hồng tím và mặc áo xanh có cổ đỏ.
>
> **Cảm xúc:** Em đang ngạc nhiên, hơi lo và bối rối, kiểu "Ơ… cái gì thế?". Mắt em mở to và nhìn lên chếch sang một bên, lông mày nhướng và chau vào giữa, miệng hé tròn. Hai tay ôm chặt cuốn sổ vào ngực như để tự trấn an. Có vẻ em vừa nghe hoặc thấy điều gì bất ngờ, không hẳn là sợ hãi mà là căng thẳng, dè dặt.
>
> **Những điểm có thể thấy lạ:**
> 1. **Đuôi tóc** là chỗ dễ gây chú ý nhất. Nó to, dựng đứng và cong như một cái đuôi thú, không giống tóc người. Chỗ gốc có một búi sợi trắng xám lởm chởm, trông như lông cứng hay chổi. Khối tóc này cũng hơi quá khổ so với đầu.
> 2. **Chiếc vòng tay hay đồng hồ** vàng viền đỏ có hình dạng khó đoán, trông giống đồ chơi nhựa hơn là đồng hồ thật.
> 3. **Ánh mắt** hơi lệch nhau một chút. Hai con ngươi không hẳn cùng nhìn vào một điểm, nên nhìn kỹ thấy hơi lác nhẹ. Có thể đó là chủ ý để diễn tả sự bối rối.
> 4. **Cuốn sổ** bị tay che mất chữ, chỉ còn đọc được "…ology" (có lẽ là "Biology") kèm hình chiếc lá. Người xem có thể tò mò không biết chữ đầy đủ là gì.
> 5. **Nấm đỏ** dưới đất bóng loáng như nhựa hoặc kẹo. Có một cây nấm nằm lẻ loi, trông như bị ngắt rời, ở góc phải phía dưới.
> 6. **Khung hình** là màn ảnh rộng kiểu điện ảnh (khoảng 2.39:1), rộng hơn chuẩn 16:9 của dự án. Tông màu rừng chiều tối ấm, gốc cây nâu đỏ và tán lá dày tạo cảm giác hơi kỳ bí.
>
> Nhìn chung, đây là khung hình hoạt hình chất lượng cao, cảm xúc nhân vật rõ ràng. Điểm "lạ" nổi bật nhất là mái tóc đuôi ngựa trông như đuôi thú.

#### doichung_sf_332 — file mù `a9742853.png` — nguyên văn

> Tôi đã xem đúng một ảnh (a9742853.png) và không mở file nào khác. Ảnh là một khung hình hoạt hình 3D, cảnh tối, ánh sáng xanh lam lạnh như ban đêm hoặc có sương.
>
> **Tuổi:** Một phụ nữ trưởng thành, trông khoảng 40 đến 50 tuổi. Người xem đoán tuổi chủ yếu nhờ lối trang điểm đậm và phong cách "thập niên 80" (tóc vàng xù, bông tai hình học to màu tím và xanh, vòng cổ chuỗi hạt), chứ khuôn mặt không có nếp nhăn rõ.
>
> **Giới tính:** Nữ. Nhận ra nhờ mi dài cong, son tím, phấn má và trang sức.
>
> **Cảm xúc:** Rất mạnh và tiêu cực: vừa ghê sợ vừa tức giận, kiểu "tránh xa tôi ra!".
> - Mắt nhắm nghiền, chân mày nhíu sâu hình chữ V.
> - Miệng méo sang một bên, nhe răng như đang hét hoặc gầm gừ.
> - Bàn tay giơ thẳng về phía người xem như đang đẩy ra hay che chắn.
> - Đầu ngả ra sau, né đi.
>
> Nhìn chung là giây phút giật lùi, bị tấn công hoặc cực kỳ ghê tởm thứ gì đó.
>
> **Những điểm người xem có thể thấy lạ:**
> 1. Có những vệt sẫm dài dưới hai mắt, như mascara bị lem, chảy xuống hoặc quầng thâm rất đậm. Nhìn thoáng qua khó biết là cố ý hay lỗi hình.
> 2. Có vài vệt đen như vết xước hoặc vết bẩn ở cằm và má trái.
> 3. Khuôn mặt tròn, căng và nhẵn bất thường, gần như "cao su". Mũi nhỏ mà đầu mũi lại hồng, lệch khỏi tông da.
> 4. Răng lởm chởm, lệch, có khe hở. Viền môi tím dày như một vòng cao su bao quanh miệng.
> 5. Bàn tay ở rất gần máy quay nên trông to và mờ nhẹ. Các ngón tay dài, và mặt nhìn không có chỗ nào gợi rõ cổ hay vai nối liền, vì vậy tư thế hơi khó đọc.
> 6. Ánh sáng xanh phủ toàn cảnh làm màu da tái, gần như không còn sắc. Người xem có thể thấy nhân vật hơi "ma quái" hơn mức chủ ý.
>
> Không có việc gì đang chờ chủ dự án từ yêu cầu này.
