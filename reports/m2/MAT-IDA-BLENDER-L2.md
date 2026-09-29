# CỬA MẶT IDA — LƯỢT 2 (d): LƯỚI NGƯỜI MPFB2 CC0 → three.js · KIỂM MÙ 1 VÒNG

Nhánh: `claude/cine-lab-m2-cong5-layout-24o5fp` (merge W4 @2130fd4). Ngày 28/09/2026.
Quyết định gốc: AUTHORSHIP "Cửa mặt Ida — quyết định", dòng lượt 2.
- **Cổng 6 vẫn khoá.** Layout trên main không đổi.
- `IDA_STYLE` mặc định vẫn `'aa'`. P đo lại sau khi merge: render dò s02, s37, s39, 9 ảnh nhỏ, lệch **0 px**.

## 0. Kết luận
- **Bước 1 (khả thi): ĐẠT.** MPFB2 2.0.17 lấy bằng `git clone` (commit `3edf9df0…`). Lưới gốc và targets có sẵn trong repo, không cần máy chủ makehumancommunity. Addon chạy được với `/opt/bpy` không giao diện.
- **Bước 2–3: xong.** Đầu Ida từ người nữ MPFB 74 tuổi, 70 444 đỉnh (A-i: 86,7 nghìn). Shape key 16 kênh + 6 khẩu hình dựng từ expression unit CC0 của MPFB. Nạp vào three.js bằng cờ `'bl'`. Có đủ 8 khung thử và bảng so sánh.
- **Kiểm mù 1 vòng (khung PA1): TRƯỢT** theo cách chấm nghiêm (xem mục 2):
  - tuổi và giới **4/4 ✔**;
  - cảm xúc rõ đúng **1/4 ✘**, cộng 3 khung "nửa đúng";
  - từ khoá chỉ vào mặt/đầu Ida **1/4 ✘**, là "mép mặt nạ bị rách" ở chỗ da cổ bị khuyết, một lỗi kỹ thuật;
  - đối chứng **0/2 ✔**.
- **Câu đếm riêng "người thật / ảnh chụp lạc phong cách": 0/8.** Không khung nào bị đọc là người thật. Hai khung đối chứng tự nêu "không phải người thật".
- **Điểm quan trọng nhất cho quyết định:**
  - Khung **chính diện** 'bl' vẫn bị gọi "búp bê" **2/2**, giống A-i (9/10).
  - Trong phép so thêm cùng đèn L11 nâng, cùng cỡ cắt (n = 1 mỗi mặt), A-α và A-i **không** bị gọi búp bê, còn 'bl' bị gọi "búp bê hoặc tượng sáp".
  - Tức là mức giảm lời "búp bê" ở khung PA1 (A-α đèn cũ 3/4 → 'bl' đèn mới 1/4) **không thể quy cho lưới**. Góc nghiêng và đèn L11 nâng góp phần lớn; mẫu nhỏ.

## 1. Kết quả khả thi và dựng
| Hạng mục | Kết quả |
|---|---|
| Nguồn, giấy phép | MPFB2 2.0.17, commit `3edf9df0551765be43563d047888cf7877eb89b4`. Tài sản lõi **CC0** (LICENSE.md mục C); mã addon GPLv3, chỉ chạy làm công cụ, không chép vào repo. Đã ghi RIGHTS.md **W4-MPFB-A**, **W4-MPFB-C** trước khi dùng. Không dùng asset pack bên thứ ba |
| Ảnh khả thi | `reports/m2/cong5/w4/L2_kha-thi.jpg` (age 0,94, khoảng 82 tuổi) |
| Ida | age 0,877 (khoảng 74 tuổi) + 33 target chi tiết (mũi dài hơi khoằm, mắt to, dái tai dài, gò má cao, môi mỏng, cằm nhỏ). Chỉ lấy đầu và cổ, sọ ×1,081. Subdivision cấp 2 → **70 444 đỉnh** |
| Mắt | nhãn cầu có tròng và điểm sáng, hai mắt hội tụ (đã sửa "hố đen" của lượt 1) |
| Tóc, mày, búi | tóc và mày bạc; búi liền đầu |
| Tai | **khác lệnh:** W4 dùng tai liền lưới của MPFB thay tai lượt 1, vì không có đường nối. Đổi lại tai lượt 1 được nếu chủ dự án muốn |
| Mũ | mũ phớt D2 #262a33 thật của cast3d; bản lề mới ngả 0,26 rad (A-i 0,36) |
| Shape key | 16 kênh cùng tên `CHANNELS` (bảng ánh xạ expression unit MPFB trong `reports/m2/cong5/w4/BAO-CAO-W4.md`); 6 khẩu hình `vis_*`; 4 preset theo `FACE_PRESETS`. frown, press, chinRaise hạ còn 0,6 / 0,6 / 0,55 vì ở mức 1,0 miệng "gãy như vết rách" |
| Ảnh 4 góc | `reports/m2/cong5/w4/L2_eevee_4goc.jpg` |
| c3_views 'bl' (thân so với sheet) | 0° −16,9 % · ±45° −4,8 / −4,0 % · ±90° −11,2 / −10,2 % · ±135° −21,0 % · 180° −24,5 %. Phần đầu nhìn thấy dài hơn A-α 12–32 %, vì lưới MPFB giữ tỷ lệ mặt người (mắt ở 0,50 H so với 0,575 H). Nếu chọn 'bl' thì phải quyết lại tỷ lệ đầu–thân và đo c3_views mới. **Không sửa ida.json** |

**Đèn L11 nâng: cần chủ dự án xác nhận cách hiểu.**
- W4 đặt L11 cao 17,5° trên tâm mặt, lệch 25° khỏi trục máy, theo đúng chữ của đề xuất.
- Ở máy nghiêng PA1, L11 gốc đã cao 43,2°, nên cách hiểu này thực ra **hạ** đèn so với layout.
- Nếu ý là cộng thêm 15–20° vào góc hiện có thì phải render lại 4 khung PA1 (khoảng 2 phút). Kết quả kiểm mù ở đây là với cách hiểu của W4.

## 2. Kiểm mù (1 vòng)
Quy trình như 2 vòng A-i: đổi tên ngẫu nhiên; mỗi khung một subagent MỚI chỉ mở 1 file; câu hỏi y hệt; 2 khung Sprite Fright đối chứng (104,5 s; 332 s) cùng đợt.
Đích cảm xúc theo layout:
- last và goodnight (s37): **cười buồn**.
- brighter và keep (s39): **nghẹn**.

Cách chấm như A-i:
- **cười buồn** cần cả nụ cười lẫn nỗi buồn. Vòng 1 A-i "buồn, không cười" chấm ✘; vòng 2 "mỉm cười nhẹ, trìu mến pha chút buồn" chấm ✔.
- **nghẹn** chấm ✔ khi đọc ra buồn, nén hoặc tủi thân.
- Khung chỉ đúng một nửa ghi "≈".

| Khung ('bl') | Tuổi / giới | Cảm xúc đọc được | Chấm | Từ khoá chỉ vào mặt/đầu Ida | Từ khoá chỉ vào vật khác | Lỗi nổi bật |
|---|---|---|---|---|---|---|
| **PA1_last** | nữ 70–80 ✔ | "mỉm cười nhẹ… ấm áp… hoài niệm… cô đơn nhưng **không buồn**" | ≈ (có cười, thiếu buồn) | 0 | 0 | bàn tay to, ngón "như tấm lược"; "mẩu tay" cam sau cột; da "hơi như sáp hay nhựa" |
| **PA1_goodnight** | nữ 65–75 ✔ | "vui, hài lòng và dịu dàng… hoài niệm" | ≈ (có cười, thiếu buồn) | 0 | 0 | mũ "lơ lửng / xuyên vào đầu"; búi "quả bóng trơn"; mắt khe |
| **PA1_brighter** | nữ 65–75 ✔ | "khó đọc… trầm ngâm, hơi buồn hoặc hoài niệm… đơ" | ≈ | **1**: "mảng da nhọn lởm chởm… như **mép mặt nạ** bị rách" (cổ) | "tay ma-nơ-canh" (tay) | da cổ khuyết; búi "cục bông"; hoa tai lơ lửng |
| **PA1_keep** | nữ 70–80 ✔ | "trầm, buồn và cam chịu… hờn dỗi" | ✔ | 0 | 0 | "cổ và hàm bị rách" (da cổ khuyết); mắt "gần như không có" |
| s37 chính diện neutral (chỉ báo số) | "khó đoán", nữ khoảng 70 % | buồn, hờn dỗi, "hơi đơ" | — | 1: "mặt trẻ con hay **búp bê**" | — | "tuổi lệch: tóc già, da em bé"; uncanny |
| s37 chính diện choked (chỉ báo số) | nữ, 65–75 | "buồn… cố nén" ✔ | — | 2: "đầu **búp bê** cắm trên ống", "giống **búp bê** hoặc tượng 3D" | — | tóc "lông vũ"; mũ lơ lửng; không thấy cổ |
| EEVEE PA1_goodnight (chỉ báo số) | nữ 60–70 | "vui, dễ chịu… mỉm cười" | — | 0 | — | mắt khe tối; khăn "vết nứt dọc"; nhiễu hạt |
| EEVEE PA1_keep (chỉ báo số) | nữ, "có thể bị đọc là đàn ông" | "khó đọc… trầm ngâm, hơi buồn" | — | 0 | — | "da cổ và gáy bị rách"; mũ lơ lửng; khuyên sai chỗ |
| Đối chứng SF 104,5 s | bé gái 10–12 | lo lắng, bối rối | — | 0 | — | — |
| Đối chứng SF 332 s | nữ 35–45 | giận dữ, đau đớn | — | 0 | — | — |

**Bảng tiêu chí (khung PA1 'bl'):**

| Tiêu chí (không hạ) | Kết quả | |
|---|---|---|
| Tuổi và giới đúng 4/4 | 4/4 | ✔ |
| Cảm xúc ≥ 3/4 | **1/4** ✔ rõ, 3/4 ≈ (tính ≈ là nửa: 2,5/4) | **✘** |
| 0/4 từ khoá chỉ vào mặt/đầu Ida | **1/4** (cổ khuyết, "mép mặt nạ bị rách") | **✘** |
| Đối chứng 0/2 | 0/2 | ✔ |
| Thêm: "người thật / ảnh chụp lạc phong cách" | 0/8 (EEVEE goodnight có "giống ảnh chụp thiếu sáng", nói về nhiễu hạt, không phải phong cách) | — |

**Kết quả: TRƯỢT** (tiêu chí 2 và 3). Theo quyết định, không làm vòng 2.

### 2.1 Phép so thêm cùng đèn (P tự thêm để tách lưới hay đèn; chỉ báo số, không tính tiêu chí)
Cắt 3 ô hàng trên của `L2_SO_goodnight_aa-ai-bl.jpg`: cùng khung PA1_goodnight, cùng đèn L11 nâng, cùng cỡ 640×314. Mỗi ô một subagent mới.

| Mặt | Tuổi / giới | Cảm xúc | "búp bê/mặt nạ…" | Lỗi nổi bật |
|---|---|---|---|---|
| A-α | nữ 70–80 | bình thản, mỉm cười nhẹ, hoài niệm; "có người sẽ đọc thành buồn nhẹ" | **0** | cổ dài như khối trụ, không thấy hàm; da căng; tóc như giấy |
| A-i | nữ 65–75 | chú ý, hơi ngạc nhiên; "khó đọc" | **0** | tai quá to, sai chỗ; tóc "mây tre đan" |
| 'bl' | nữ 65–75 (da "40–50") | vui, hiền, mỉm cười | **1**: "giống **búp bê** hoặc **tượng sáp**" | không thấy mắt ở góc nghiêng; da quá trẻ; mũ lơ lửng |

## 3. Hình khối hay máy render
- Cùng lưới, cùng góc: EEVEE và three.js cho **cùng lời chê hình khối**: da cổ khuyết hoặc rách, mũ lơ lửng, khuyên tai sai chỗ, mắt khe ở góc nghiêng.
- EEVEE không bị gọi "búp bê" ở 2/2 khung; three.js ở khung cùng góc cũng 0.
- Khác nhau chủ yếu ở cách tô: three.js có lớp vẽ Kuwahara và da cam dưới đèn khí; EEVEE có tán xạ dưới da nhưng lộ nhiễu hạt.
- **Kết luận:** các lỗi còn lại là lỗi **lắp ráp** (cổ–khăn, mũ–đầu, khuyên–dái tai, búi) và **mắt ở góc nghiêng**, không phải lỗi của máy render. Lời "búp bê" ở khung chính diện đến từ tỷ lệ "da trẻ, tóc già" và việc đầu cắm vào ống khăn.

## 4. Nếu chọn 'bl': đưa vào pipeline
- **Shot đổi:** mọi shot có Ida (bật `IDA_STYLE='bl'`, thêm `await preloadIdaBL()` ở trang render).
- **Chi phí:** dựng glb 5 s; khung 1080p 23–28 s (tương đương A-i); glb 11 MB (đã commit).
- **Việc kéo theo:**
  - quyết lại tỷ lệ đầu–thân, c3_views mới, characters v1.5 + khoá SHA;
  - sửa lỗi lắp ráp: da cổ khuyết, mũ lơ lửng, búi "cục bông", khuyên tai, mép cổ áo tính theo đầu A-α;
  - mắt đọc được ở góc nghiêng;
  - rà continuity mũ s36.
- **Rủi ro:** thêm phụ thuộc MPFB mỗi lần dựng lại glb; mọi chỉnh hình phải chạy lại script Blender.
- **Lợi thêm cho Cổng 6:** MPFB có tay đúng giải phẫu (CC0). Lỗi tay xuất hiện ở 2/4 khung PA1 và ở mọi phương án trước.

## 5. Quyết định cần chủ dự án: chọn mặt cho phương án lùi PA1
Cả ba cùng dàn dựng PA1 (nghiêng dưới L11); không dùng cận mặt chính diện ở cao trào, vì cả ba mặt đều bị gọi "búp bê" khi chính diện.

| | **A — PA1 + 'bl' (MPFB2)** | **B — PA1 + A-i** | **C — PA1 + A-α (đang khoá v1.4)** |
|---|---|---|---|
| Kiểm mù PA1 | 4 khung, đèn mới: tuổi/giới 4/4; cảm xúc 1/4 rõ (+3 ≈); "mặt nạ" 1/4 (lỗi cổ) | chỉ có 1 khung đèn cũ (goodnight: "mặt búp bê") + 1 ô so cùng đèn mới (0 từ khoá, cảm xúc "khó đọc") | 4 khung, đèn cũ: 4/4; cảm xúc 2/4 rõ (+2 ≈, chấm lại cùng cách); "búp bê/mặt nạ" 3/4 + 1 ô so cùng đèn mới (0 từ khoá) |
| Chính diện | "búp bê" 2/2 | "búp bê/mặt nạ" 9/10 | 4/4 (lần 6) |
| Rig, khẩu hình cho Cổng 6 | shape key 16 kênh + 6 khẩu hình (CC0) | rig 16 kênh + 6 khẩu hình | **không** (mặt vẽ nét) |
| Ưu | Giải phẫu đúng (gốc lỗi của 6 lần tự nặn); không bị đọc là người thật (0/8); có tay MPFB cho Cổng 6 | Tỷ lệ sheet quen; rig đã chạy trong layout | Không phải làm gì thêm; đã khoá |
| Nhược | Trượt tiêu chí 2 và 3 (nghiêm); tỷ lệ đầu lệch sheet 12–32 %; còn lỗi lắp ráp | Nửa dưới mặt phình 10/10, tai lạ; chưa kiểm đủ 4 khung với đèn mới | Không có khẩu hình, nên không lip-sync được câu cao trào |
| Tác động | characters v1.5, c3_views mới, sửa lắp ráp trước Cổng 6 | characters v1.5 (A-i), khoá SHA | Cổng 6 phải giấu miệng ở mọi câu thoại |
| Rủi ro | Sửa lắp ráp xong vẫn có thể bị gọi "búp bê/tượng sáp" (ô so n = 1) | "búp bê" ở góc nghiêng khi động | Cao trào không có khẩu hình |

**Khuyến nghị của P: A (PA1 + 'bl'), kèm điều kiện.**
- 'bl' là mặt duy nhất dựng trên giải phẫu đúng, đúng gốc lỗi mà Claude bên ngoài chỉ ra.
- Lời chê còn lại chủ yếu là **lỗi lắp ráp sửa được**: cổ khuyết (chính là lý do của 1/4 "mặt nạ"), mũ, búi, khuyên, mắt góc nghiêng.
- Cảm xúc ≈ phần lớn do mắt thành khe ở góc nghiêng. Điều này đúng với cả ba mặt (A-α "trầm", A-i "khó đọc").
- Nhưng số liệu **chưa chứng minh** 'bl' hết bị gọi "búp bê": chính diện 2/2; ô so cùng đèn thì A-α và A-i 0, 'bl' 1.
- **Điều kiện:** nhận A nghĩa là chấp nhận trượt tiêu chí ở vòng này. Tôi đề xuất một lần kiểm xác nhận 4 khung PA1 **sau khi sửa lắp ráp**, đặt ở đầu Cổng 6 như một mục kiểm, không phải vòng mặt mới.
- Nếu chủ dự án muốn giữ đúng nguyên tắc "trượt thì lùi" mà không thêm việc, chọn **B**: có rig, không cần đổi tỷ lệ.
- **Không khuyến nghị C** vì không có khẩu hình.

Cần chủ dự án quyết thêm:
- (i) cách hiểu "nâng L11" (mục 1);
- (ii) tai MPFB hay tai lượt 1;
- (iii) nếu chọn A: tỷ lệ đầu–thân mới.

## 6. Thời gian, token, hàng đợi
| Việc | Thời gian | Token (ngữ cảnh tích luỹ do công cụ báo) | Hàng đợi |
|---|---|---|---|
| W4 lượt 1 | khoảng 26 phút | 250 828 | 1 việc, 66 s |
| W4 lượt 2 (15:07–16:30 UTC): khả thi 3 phút, dựng 20, tích hợp 12, khung + c3 + EEVEE + sửa cổ 40, báo cáo 8 | khoảng 1 giờ 23 phút | **486 916** khi kết thúc (công cụ báo; W4 tự ước khoảng 610 nghìn) → lượt 2 khoảng 236 nghìn | gói W4 cả hai lượt: 48 việc, chờ 0 s, chạy 1 623 s (29 việc làn nặng, 1 210 s); EEVEE chạy ngoài hàng đợi 47–50 s mỗi khung |
| Làm lại (W4) | 12 lượt dựng glb (mắt 3, mày 1, chân tóc 3, miệng 1, cổ 4); bộ khung 3 lượt | — | — |
| P kiểm mù: 10 + 3 subagent | 20–37 s mỗi subagent | khoảng 47 000–50 100 mỗi subagent | P dò 'aa' 56 s (làn nhanh) |

Tổng gói Blender (2 lượt) khoảng 487 nghìn token (công cụ báo), dưới hạn khoảng 700 nghìn.

## 7. Nguyên văn subagent (cả đối chứng)
### 7.1 Vòng kiểm mù (8 khung + 2 đối chứng)
#### L2_BL_PA1_last — file mù `df10b579.jpg` — nguyên văn

> Tôi chỉ mở đúng một file ảnh được yêu cầu, là df10b579.jpg. Dưới đây là cảm nhận của một người xem bình thường.
>
> **Tuổi và giới tính:** Đây là một bà cụ, chắc tầm 70–80 tuổi. Tóc bạc trắng búi sau gáy, đeo khuyên tai hạt vàng, mặt có nếp nhăn nhẹ. Bà đội mũ phớt đen, quàng khăn len đỏ, mặc áo khoác dạ xanh rêu.
>
> **Cảm xúc:** Bà đang mỉm cười nhẹ, trông ấm áp và dịu dàng, có chút hoài niệm. Bà áp hai tay vào cột đèn đường đang sáng như để sưởi ấm, hoặc như đang trìu mến một thứ gì thân quen. Cảm giác chung là bình yên, cô đơn nhưng không buồn.
>
> **Những điều người xem có thể thấy lạ:**
> 1. **Bàn tay** là điểm lạ rõ nhất. Hai bàn tay to bất thường so với người. Các ngón dài, thẳng, xếp đều như tấm lược, trông giống găng tay cứng hoặc ngón tay bị kéo dãn. Bàn tay cũng không ôm quanh cột mà như xuyên vào hoặc chồng lên cột, và phần cổ tay nối với tay áo trông gãy khúc.
> 2. **Có một vật nhỏ màu cam** thò ra ở mép trái cột đèn, ngang tầm cằm bà. Nó trông như ngón tay cái hoặc một mẩu tay lạc chỗ, người xem sẽ thắc mắc đó là gì.
> 3. **Ánh sáng trên mặt** hơi gắt. Da mặt và tai đỏ cam rực như đang phát sáng, không giống ánh đèn hắt vào. Mặt trông hơi như sáp hay nhựa.
> 4. **Khoảng cách:** mặt bà sát cột đèn và gần ngọn đèn nóng. Người xem có thể thấy tư thế này hơi lạ và không tự nhiên.
> 5. **Bối cảnh:** tường phía sau có một mảng tróc lộ gạch trông như dán lên. Bên phải có thêm mấy cột mảnh mà không rõ là gì. Bóng lớn bên trái (có vẻ là bóng chiếc mũ) mờ và không khớp lắm với nguồn sáng.
>
> **Tóm lại:** cảm xúc của nhân vật đọc được rõ và dễ chịu. Nhưng bàn tay và vật cam lạ bên cột là thứ sẽ làm người xem chú ý và "vấp" ngay.

#### L2_BL_PA1_goodnight — file mù `c5fde95d.jpg` — nguyên văn

> Tôi đã mở và xem đúng một file c5fde95d.jpg. Không đọc file nào khác.
>
> **Tuổi:** khoảng 65–75. Tóc bạc trắng búi sau gáy, lông mày bạc, có vài nếp nhăn ở đuôi mắt.
>
> **Giới tính:** nữ. Nhìn tóc búi, bông tai vàng và khăn len quấn cổ là nhận ra.
>
> **Cảm xúc:** vui, hài lòng và dịu dàng. Bà nhắm hờ hoặc híp mắt, khóe miệng cười mỉm, trông như đang nhớ lại một điều gì đẹp. Ánh sáng vàng cam ấm chiếu lên mặt càng làm cảm giác ấm áp, hoài niệm rõ hơn.
>
> **Những điểm người xem có thể thấy lạ:**
> 1. **Chiếc mũ không khớp với đầu.** Vành mũ nâu như lơ lửng phía trên. Nó cắt ngang tóc, và chỗ tóc gặp mũ không có bóng đổ hay chỗ tóc bị ép xuống. Trông như mũ xuyên vào đầu.
> 2. **Búi tóc giống quả bóng trơn.** Búi bên trái mờ, màu xám trắng, không có sợi tóc. Nó trông tách rời khỏi phần tóc có sợi rõ ở phía trước.
> 3. **Tóc có răng cưa.** Sợi tóc nhìn như những lớp bậc thang cứng, nhất là ở mép chân tóc trên trán và thái dương.
> 4. **Da mặt quá mịn và phát sáng.** Da trơn láng như sáp hoặc nhựa. Mép má, mũi và cằm có quầng sáng cam như tỏa ra ngoài, không giống da thật được chiếu sáng.
> 5. **Mắt khó đọc.** Mắt quá nhỏ và mờ, gần như chỉ là một khe hở, nên khó biết bà đang nhắm mắt hay đang nhìn.
> 6. **Bông tai đơn giản quá mức.** Hai viên bi nối bằng một que, trông như vật đơn giản kiểu đồ chơi, và hơi lơ lửng dưới dái tai.
> 7. **Cổ và khăn.** Khăn len quấn nhiều vòng dày nhưng chỗ khăn chạm cổ và cằm không có nếp lún. Phần cổ phía sau cũng trông hơi cứng.
> 8. **Có chấm đen nhỏ ở đuôi lông mày.** Chấm này nằm gần đầu lông mày, ở phía trên mắt, trông như một vết lỗi.
>
> Nhìn chung, bà hiện ra là một cụ bà hiền hậu đang mỉm cười. Nhưng người xem sẽ nhận ra đây là hình dựng 3D chưa hoàn thiện, rõ nhất ở chiếc mũ, búi tóc và lớp da phát sáng.

#### L2_BL_PA1_brighter — file mù `58cdf98e.jpg` — nguyên văn

> Tôi chỉ mở đúng một file theo yêu cầu: /tmp/claude-0/-home-user-cine-lab/5b95043d-dd86-5cf7-9b06-17de07cfe1f8/scratchpad/matai/bl2/58cdf98e.jpg. Dưới đây là cảm nhận của một người xem bình thường.
>
> **Tuổi:** một bà cụ, chừng 65–75 tuổi. Tóc bạc trắng búi sau gáy, da mặt có nếp nhăn.
>
> **Giới tính:** nữ. Nhìn ra qua búi tóc, đôi hoa tai vàng, khăn len và áo khoác kiểu nữ.
>
> **Cảm xúc:** khó đọc. Mặt quay nghiêng, mắt gần như nhắm hoặc nheo lại, miệng khép. Tôi đoán bà đang trầm ngâm, lặng lẽ, hơi buồn hoặc hoài niệm, như đang nhớ lại điều gì bên cột đèn. Nhưng biểu cảm khá "đơ" nên không chắc. Cũng có thể hiểu là bà mệt, hoặc chỉ đứng yên không cảm xúc gì.
>
> **Những điểm người xem có thể thấy lạ:**
> 1. **Bàn tay nắm cột đèn** là chỗ dễ thấy nhất:
>    - Tay to bất thường so với đầu.
>    - Các ngón thẳng đơ, xoè đều như tay ma-nơ-canh chứ không ôm quanh cột.
>    - Ngón tay có vẻ như xuyên vào thân cột.
>    - Tay đỏ cam rực như đang phát sáng, trong khi mặt không sáng như vậy.
> 2. **Vùng cổ dưới tai:** có một mảng da nhọn lởm chởm chìa ra phía trên khăn, trông như mép mặt nạ bị rách hoặc da bị cắt.
> 3. **Có vật màu cam lấp ló sau cột đèn,** ngang tầm cổ (khoảng giữa ảnh, bên phải). Không rõ là gì, trông như ngón tay hoặc vật lạ lơ lửng.
> 4. **Búi tóc** trắng, tròn nhẵn như cục bông, khác hẳn phần tóc chải phía trước và có một vệt sọc trắng. Nhìn như được gắn vào.
> 5. **Tỉ lệ:** đầu đèn lồng ngang tầm đầu bà. Cột đèn thì quá thấp, hoặc bà quá to.
> 6. **Khuôn mặt:** mắt gần như không thấy, nên khó đọc cảm xúc. Tai to và hoa tai hai viên bi trông hơi lơ lửng.
> 7. **Nền:** tường mờ bạc, rất ít tương phản. Có một thanh đen dọc ở mép trái khung hình mà không rõ là vật gì.
>
> Tóm lại, người xem dễ nhận ra đây là một bà cụ đứng bên cột đèn đường với tâm trạng lặng lẽ, buồn. Nhưng bàn tay, mảng da ở cổ và vật màu cam sau cột là những chỗ dễ làm họ bị phân tâm hoặc thấy kỳ quặc nhất.

#### L2_BL_PA1_keep — file mù `f4084d16.jpg` — nguyên văn

> Tôi đã xem đúng một file ảnh: /tmp/claude-0/-home-user-cine-lab/5b95043d-dd86-5cf7-9b06-17de07cfe1f8/scratchpad/matai/bl2/f4084d16.jpg. Không mở file nào khác.
>
> **Cảm nhận như người xem bình thường**
> - **Tuổi:** một người già, tôi đoán khoảng 70–80 tuổi. Tóc bạc trắng búi sau gáy, có nếp nhăn ở khóe mắt và quanh miệng, cằm hơi chảy.
> - **Giới tính:** nhiều khả năng là phụ nữ, một bà cụ. Dấu hiệu là búi tóc, bông tai vàng và khăn len quàng cổ. Mũ phớt nâu thì hơi trung tính, nhưng nhìn tổng thể vẫn ra một bà cụ.
> - **Cảm xúc:** trầm, buồn và cam chịu, có chút nghiêm nghị hoặc hờn dỗi. Khóe miệng trễ xuống, môi mím, mắt gần như nhắm hoặc nhìn xuống. Ánh nắng ấm chiếu nghiêng nên cảnh có vẻ hoài niệm, lặng lẽ.
>
> **Điều người xem có thể thấy lạ**
> 1. **Cổ và hàm bị "rách":** chỗ da mặt nối xuống khăn có mép răng cưa như giấy xé. Ở góc dưới bên trái, da kết thúc bằng một mép lởm chởm và lộ bức tường phía sau, như thể thiếu một mảng cổ. Đây là lỗi dễ thấy nhất.
> 2. **Mép trên của khăn len** cũng lởm chởm như bị cắt, không ôm vào cổ.
> 3. **Mắt gần như không có:** nhìn nghiêng chỉ thấy một khe nhỏ, không thấy tròng mắt hay mí rõ ràng. Mặt vì thế trông hơi "trống".
> 4. **Tóc trông như nhựa hoặc thanh gỗ xếp lớp,** không giống sợi tóc. Lông mày là một vệt trắng phẳng.
> 5. **Búi tóc bên trái là một quả cầu xám mờ, phẳng,** trông như tách rời khỏi đầu.
> 6. **Đầu và tai quá to so với mặt.** Tai nằm rất xa về phía sau, phần gáy dưới tóc là một mảng da phẳng lớn.
> 7. **Bông tai giống khuyên kiểu thanh tạ** (hai viên bi nối bằng que). Đồ này hơi lạ với một bà cụ và trông như gắn thẳng vào má dưới tai, không xỏ qua dái tai.
> 8. **Mảng gạch trên tường** trông như miếng dán phẳng, không giống chỗ vữa bong thật.
> 9. **Tổng thể da** nhẵn như sáp hoặc nhựa. Người xem sẽ nhận ra ngay đây là ảnh dựng 3D, chưa hoàn thiện.
>
> Tóm lại: một bà cụ khoảng 70–80 tuổi, buồn và cam chịu. Lỗi nổi bật nhất là phần cổ và hàm bị khuyết hoặc rách mép, rồi đến mắt gần như không thấy.

#### L2_BL_s37_neutral — file mù `c49e634a.jpg` — nguyên văn

> Tôi đã xem đúng một ảnh (c49e634a.jpg) và không mở file nào khác. Đây là ấn tượng của một người xem bình thường.
>
> **Tuổi:** Khó đoán, vì các dấu hiệu mâu thuẫn nhau. Tóc và lông mày bạc trắng, có vài nếp nhăn nhẹ ở khoé mắt, gợi đến một người già khoảng 60–75 tuổi. Nhưng da mặt lại căng, mịn và tròn như mặt trẻ con hay búp bê. Nhìn lướt qua, tôi đoán đây là một bà cụ. Nhìn kỹ thì khuôn mặt giống một người trẻ đội tóc giả bạc.
>
> **Giới tính:** Nghiêng về nữ, khoảng 70%. Lý do là có đôi hoa tai tròn màu vàng và khăn quàng len. Tuy vậy, mũ phớt, tóc ngắn và khuôn mặt khá trung tính khiến người xem có thể nghĩ đây là một ông cụ.
>
> **Cảm xúc:** Buồn, hờn dỗi hoặc thất vọng lặng lẽ. Khoé miệng trễ xuống, môi dưới hơi bĩu ra. Mắt nhìn chếch sang bên, ánh mắt hơi xa xăm. Có thể đọc thành "tủi thân" hoặc "cam chịu". Tuy nhiên biểu cảm khá nhẹ và hơi đơ: vùng trán và lông mày gần như không tham gia, nên nỗi buồn nằm chủ yếu ở cái miệng.
>
> **Những điểm người xem có thể thấy lạ:**
> 1. **Tuổi lệch:** tóc và lông mày của người già đặt trên làn da mịn như em bé. Đây là điểm dễ gây cảm giác "kỳ kỳ" nhất.
> 2. **Tóc không giống tóc:** trông như một chiếc mũ chụp làm bằng lông vũ hoặc sợi nhựa trắng xù cứng, không có sợi tóc tự nhiên.
> 3. **Lông mày** có ánh xanh tím nhạt, trông như vẽ hoặc dán lên hơn là mọc ra.
> 4. **Hoa tai bên trái khung hình** lơ lửng thấp gần đường hàm, dường như không gắn vào dái tai. Hai hoa tai cũng lệch độ cao rõ rệt.
> 5. **Da như nhựa hoặc sáp:** một màu cam đào đồng đều, không có lỗ chân lông hay đốm, và phát sáng cam ở rìa như được chiếu đèn từ bên trong.
> 6. **Đầu như tách khỏi thân:** cổ bị khăn quấn kín, gần như không thấy vai. Khăn len có vân rất đều, giống dây thừng cuộn hơn là len đan.
> 7. **Mắt** bóng và đẹp nhưng hơi vô hồn, không rõ đang nhìn vào điểm nào.
> 8. **Góc dưới bên trái** có một vệt cong màu cam sáng. Không rõ đó là vật gì, nên dễ gây thắc mắc hoặc rối mắt.
>
> **Tổng thể:** Nhân vật đọc được là "một người lớn tuổi, có lẽ là bà cụ, đang buồn". Nhưng sự trộn lẫn giữa mặt trẻ và tóc già, cùng chất da nhựa, dễ khiến người xem thấy hơi rợn, kiểu hiệu ứng "thung lũng kỳ lạ" (uncanny valley), hơn là đồng cảm.

#### L2_BL_s37_choked — file mù `745557f0.jpg` — nguyên văn

> Tôi đã xem đúng một ảnh: /tmp/claude-0/-home-user-cine-lab/5b95043d-dd86-5cf7-9b06-17de07cfe1f8/scratchpad/matai/bl2/745557f0.jpg
>
> **Tuổi:** Người xem sẽ đoán là người già, khoảng 65 đến 75 tuổi. Tóc và lông mày bạc trắng, có vài nếp nhăn ở khóe mắt và giữa hai chân mày. Tuy vậy, da mặt vẫn khá căng và mịn, trông trẻ hơn so với mái tóc.
>
> **Giới tính:** Có lẽ là nữ, một bà cụ. Dấu hiệu chính là đôi hoa tai tròn màu vàng đồng và chiếc khăn len quấn cổ. Nhưng gương mặt khá trung tính, đầu to và tròn, nên nếu che hoa tai đi thì người xem có thể không chắc.
>
> **Cảm xúc:** Buồn, thất vọng, như đang cố nén lại. Khóe miệng trễ xuống rõ, môi dưới hơi đẩy lên, chân mày hơi nhíu ở giữa, mắt nhìn xuống và lảng sang một bên. Nét mặt giống người sắp khóc, hoặc vừa nghe tin không vui mà cố không bật khóc. Cảm xúc đọc được rõ, không mơ hồ.
>
> **Những điểm người xem có thể thấy lạ:**
> 1. **Tóc trông như nhựa hoặc lông vũ.** Tóc thành từng mảng sợi trắng dựng lên, sắc cạnh, giống lông chim hay giấy cắt vụn hơn là tóc người. Lông mày cũng vậy, gồ lên như một dải cứng dán lên mặt.
> 2. **Mũ không đội lên đầu.** Chiếc mũ phớt trông như lơ lửng phía trên. Vành mũ nằm ngang trán, còn phần tóc ngay dưới vành bị cắt phẳng một cách khó hiểu. Mũ không ôm lấy đầu.
> 3. **Không thấy cổ và vai.** Đầu nhô thẳng ra từ một ống khăn len dựng đứng, giống đầu búp bê cắm trên ống, không có đường cổ hay bờ vai.
> 4. **Miệng hơi lạ.** Giữa hai môi có một khe hở, lộ ra một vệt như răng hoặc lợi màu vàng nhạt, trông không tự nhiên. Khóe miệng bên trái có một nếp gấp hơi méo.
> 5. **Da mịn như sáp hoặc đất nặn.** Gần như không có lỗ chân lông hay đốm tuổi già. Điều này hợp với phong cách hoạt hình, nhưng lại lệch với mái tóc bạc và nếp nhăn: da trẻ, tóc già.
> 6. **Tai hơi to và nhọn,** hoa tai nằm khá thấp, gần như treo dưới dái tai.
> 7. **Ánh sáng và bố cục.** Nền đen hoàn toàn, mặt được chiếu sáng cam từ trên xuống, tạo cảm giác sân khấu và cô độc. Đây là điểm cộng. Tuy vậy, góc dưới bên trái có một vệt sáng cam cong bị cắt ở mép khung, không rõ là vật gì, dễ gây chú ý.
>
> **Ấn tượng chung:** Cảm xúc buồn đọc được ngay, nhưng tổng thể trông giống búp bê hoặc tượng 3D hơn là một người thật hay nhân vật hoạt hình hoàn thiện. Các điểm gây lạ nhất là tóc, chỗ mũ và đầu khớp với nhau, và phần cổ.

#### L2_EEVEE_PA1_goodnight — file mù `27cfc298.jpg` — nguyên văn

> Tôi đã mở đúng một file ảnh được chỉ định là `/tmp/claude-0/-home-user-cine-lab/5b95043d-dd86-5cf7-9b06-17de07cfe1f8/scratchpad/matai/bl2/27cfc298.jpg`, không mở file nào khác. Dưới đây là cảm nhận của một người xem bình thường.
>
> **Người trong ảnh:**
> - **Tuổi:** trông như một người lớn tuổi, khoảng 60–70. Tóc hoa râm búi sau gáy, má và cằm hơi chảy, có vài nếp nhăn nhẹ ở đuôi mắt.
> - **Giới tính:** nữ. Tôi đoán vậy vì tóc búi, đeo khuyên tai, đội mũ rộng vành và quàng khăn.
> - **Cảm xúc:** có vẻ vui, dễ chịu, như đang mỉm cười hoặc đang nói, cười với ai đó. Miệng hé mở, khoé miệng hơi nhếch lên, mắt híp lại. Nhìn chung là vẻ thân thiện, hơi tinh nghịch, không căng thẳng.
>
> **Những điểm người xem có thể thấy lạ:**
> 1. **Mắt gần như chỉ là một khe tối**, không thấy tròng mắt hay lòng trắng. Người xem khó biết bà đang nhắm mắt, nheo mắt hay nhìn về đâu. Mặt cũng không có lông mày.
> 2. **Trong miệng chỉ là một mảng tối ánh xanh**, không thấy răng hay lưỡi, nên trông hơi trống rỗng.
> 3. **Khuyên tai không treo ở dái tai.** Nó giống một thanh tạ nhỏ hai đầu tròn, lơ lửng dưới tai và gần như dính vào quai hàm.
> 4. **Khăn quàng cổ có một vết nứt dọc sắc cạnh** chạy từ trên xuống dưới, trông như bị rách hoặc hở mép. Khăn cũng như ăn lẹm vào cổ chứ không quấn quanh cổ.
> 5. **Phía sau cổ, dưới búi tóc, có một mảng sáng phẳng và nhạt màu**, trông như một chỗ bị khuyết hoặc cắt.
> 6. **Mũ như đang lơ lửng.** Không thấy chóp mũ ôm lấy đầu, chỉ thấy vành mũ chắn ngang phía trên tóc.
> 7. **Tóc trông như những mảng xước hoặc vảy** hơn là sợi tóc. Mép giữa tóc và trán có chỗ lởm chởm.
> 8. **Da mặt lấm tấm hạt nhiễu li ti**, giống ảnh chụp thiếu sáng hoặc bị sạn, rõ nhất ở má và thái dương.
> 9. **Ánh sáng tương phản mạnh:** mặt sáng rực màu cam vàng, còn búi tóc phía sau lại ánh xanh tím. Trông khá kịch tính nhưng hơi thiếu tự nhiên. Tai cũng khá to so với mặt.
>
> Tóm lại, người xem sẽ thấy đây là một bà cụ vui vẻ, dễ mến, và nhận ra ngay đây là ảnh dựng 3D. Mắt, miệng, khuyên tai, vết nứt ở khăn và hạt nhiễu trên da là những chỗ dễ làm người xem mất tập trung nhất.

#### L2_EEVEE_PA1_keep — file mù `eb7306da.jpg` — nguyên văn

> Tôi đã xem đúng một file: /tmp/claude-0/-home-user-cine-lab/5b95043d-dd86-5cf7-9b06-17de07cfe1f8/scratchpad/matai/bl2/eb7306da.jpg. Đây là ảnh dựng 3D cận cảnh, góc nghiêng, mặt nhân vật quay sang phải khung hình.
>
> **Nếu nhìn như một người xem bình thường:**
> - **Tuổi:** trông như một người già, khoảng 65–75 tuổi. Lý do: tóc bạc trắng búi sau gáy, có nếp nhăn ở khoé miệng và má, phần hàm hơi chảy xệ.
> - **Giới tính:** tôi đoán là nữ, một bà cụ. Lý do: tóc búi, đeo khuyên tai vàng, quàng khăn cổ đỏ cam. Tuy vậy, nếu chỉ nhìn khuôn mặt thì khá trung tính và cũng có thể bị đọc là đàn ông lớn tuổi, vì mũi to, cằm và hàm khá góc cạnh.
> - **Cảm xúc:** khó đọc rõ. Mặt gần như vô cảm, miệng mím, khoé môi hơi trễ xuống, mắt gần như khuất và trông như đang nhắm hoặc nhìn xuống. Tôi thấy nhiều nhất là trầm ngâm, hơi buồn hoặc mệt mỏi, nhưng cũng có thể chỉ là vẻ mặt trống, chưa có biểu cảm.
>
> **Những điểm người xem có thể thấy lạ:**
> 1. **Chiếc mũ nâu lơ lửng:** vành mũ không chạm vào đầu, có khe hở rõ giữa mũ và tóc hoặc trán. Mũ cũng chìa ra rất xa về phía trước.
> 2. **Tóc trông như nhựa:** tóc trắng đục như được đúc hoặc cắt thành mảng, có sọc răng cưa và vết xé lởm chởm. Mép tóc ở gáy cắt ngang cứng.
> 3. **Búi tóc khổng lồ và mờ ảo:** khối tròn bên trái rất to, mờ, trông như một quả bóng sáng hơn là búi tóc.
> 4. **Da cổ và gáy bị rách:** mép da phía sau cổ và dưới cằm lởm chởm như giấy xé, lộ ra như một lớp vỏ mỏng, không có cổ liền khối.
> 5. **Khăn quàng như ống phao:** các vòng khăn đỏ cam trông như ống cao su hoặc áo phao, và có đường nứt hoặc nối dọc lộ rõ ở phía trước.
> 6. **Khuyên tai sai chỗ:** khuyên tai gắn ở má hoặc quai hàm, cách xa dái tai, trông như tạ nhỏ lơ lửng.
> 7. **Ánh sáng và bề mặt da:** vùng trán, má và tóc bị chói, cháy sáng vàng. Da có hạt nhiễu li ti (noise). Mắt gần như không thấy, nên khó đọc cảm xúc.
> 8. **Nền phẳng:** nền xám xanh trơn, không có bối cảnh, nên ảnh giống ảnh thử dựng hình hơn là một khung hình phim hoàn chỉnh.
>
> Tóm lại, người xem sẽ hiểu đây là một bà cụ trầm lặng. Nhưng lỗi hình học (mũ lơ lửng, da cổ rách, khuyên tai sai vị trí) và cảm xúc mơ hồ sẽ phá cảm giác tin vào nhân vật.

#### doichung_sf_104.5 — file mù `32438704.png` — nguyên văn

> Tôi chỉ mở đúng một file: /tmp/claude-0/-home-user-cine-lab/5b95043d-dd86-5cf7-9b06-17de07cfe1f8/scratchpad/matai/bl2/32438704.png. Ảnh là khung hình hoạt hình 3D phong cách hoá, không phải người thật.
>
> **Tuổi:** trông như một bé gái khoảng 10–12 tuổi, tức trẻ tiền dậy thì. Mặt tròn, mắt to, người nhỏ.
>
> **Giới tính:** nữ. Có thể nhận ra qua tóc buộc đuôi ngựa cao với dây buộc tóc màu xanh ngọc, bông tai tròn to màu hồng tím và cách ăn mặc.
>
> **Cảm xúc:** lo lắng, bối rối, hơi e sợ. Chân mày nhướng lên và chụm vào giữa, mắt mở to liếc sang một bên, miệng hé tròn như vừa thốt "ơ…" hay đang ngập ngừng. Em ôm chặt cuốn sổ vào ngực, một tư thế tự che chắn cho thấy em đang bất an hoặc không chắc về điều mình vừa nghe hay thấy. Ngoài ra còn có chút ngạc nhiên.
>
> **Những điểm người xem có thể thấy lạ:**
> 1. **Đuôi tóc bất thường.** Đuôi ngựa rất to và dài, dựng ngược lên cao thay vì rủ xuống. Phần chân tóc lại xù ra thành từng sợi cứng như lông thú hay chổi, trông giống đuôi con vật (kiểu đuôi chồn hôi) hơn là tóc người. Đây là chi tiết dễ gây chú ý nhất.
> 2. **Cuốn sổ.** Chữ trên bìa bị tay che, chỉ đọc được "...ology" (có thể là "Biology"), kèm hình chiếc lá.
> 3. **Đồng hồ đeo tay.** Hình dạng lạ, là những mảnh nhựa vàng và đỏ ghép góc cạnh, giống đồ chơi hơn là đồng hồ thật.
> 4. **Bối cảnh.** Khu rừng tối, ánh chiều ấm, có nhiều nấm đỏ hình trụ mọc rải rác dưới đất, thân cây to và cong vặn. Không khí vừa huyền ảo vừa hơi bí ẩn.
> 5. **Tỉ lệ nhân vật.** Đầu và mắt rất to so với thân. Đây là phong cách hoạt hình bình thường, không phải lỗi.

#### doichung_sf_332 — file mù `66b51fa6.png` — nguyên văn

> Tôi chỉ mở đúng file 66b51fa6.png và không đọc file nào khác.
>
> **Người trong ảnh:** Đây là một nhân vật hoạt hình 3D phong cách hoá, không phải người thật.
>
> - **Tuổi:** Trông như phụ nữ trưởng thành, khoảng 35–45 tuổi. Lý do: lối trang điểm đậm kiểu thập niên 80 và đôi khuyên tai hình học to bản, có nét "nghệ sĩ lớn tuổi". Mặt lại rất tròn và mịn nên khó đoán chính xác.
> - **Giới tính:** Nữ. Nhận ra nhờ lông mi dài, son môi tím, khuyên tai, chuỗi hạt và mái tóc vàng rối.
> - **Cảm xúc:** Giận dữ dữ dội pha đau đớn hoặc hoảng sợ. Chân mày nhíu sâu và mắt nhắm chặt. Miệng méo, há rộng, nhe răng như đang gào hay rít lên. Một tay giơ thẳng về phía máy quay, lòng bàn tay mở. Người xem có thể hiểu động tác này là "đừng lại gần", đang chắn một thứ gì, hoặc đang áp tay vào tấm kính. Nhìn chung là một khoảnh khắc bùng nổ, bị dồn vào đường cùng.
>
> **Những điểm có thể khiến người xem thấy lạ:**
> 1. **Quầng đen quanh mắt:** Vệt đen dày, nhoè thành sọc dưới mi dưới, trông như mascara chảy hoặc mắt thâm. Khó biết đây là trang điểm cố ý hay dấu hiệu nhân vật vừa khóc hoặc bị thương.
> 2. **Mắt nhắm hẳn:** Không thấy mắt, nên cảm xúc chỉ đọc được qua chân mày và miệng.
> 3. **Vết xước trên cằm:** Có vài vệt nâu sẫm. Có thể là vết thương, vết bẩn hoặc nếp nhăn, nhưng nhìn không rõ.
> 4. **Tỉ lệ khuôn mặt và bàn tay:** Mặt rất tròn và phẳng như quả bóng. Miệng lệch hẳn sang một bên. Bàn tay rất to, ngón dài, ngón cái có hình dạng hơi lạ. Tay nằm gần máy quay nên bị phóng to, trông như đang dí sát ống kính.
> 5. **Hàm răng:** Răng không đều. Hàm trên có khe hở và một chiếc răng cửa lệch.
> 6. **Ánh sáng:** Toàn cảnh chìm trong ánh xanh lạnh và có sương mờ. Chỉ phần da quanh mũi và má có chút ấm, nên chiếc mũi hồng trông hơi tách khỏi phần còn lại của mặt.
> 7. **Khung hình:** Ảnh rất rộng ngang, kiểu màn ảnh rộng. Đầu nhân vật nghiêng hẳn, gần như nằm nghiêng hoặc đang ngã, và đỉnh đầu bị cắt khỏi khung.
>
> Cảm giác chung là một cảnh cao trào, căng thẳng. Nhân vật vừa dữ tợn vừa có vẻ tổn thương.

### 7.2 Phép so thêm cùng đèn (3 ô, chỉ báo số)

#### so_aa — file mù `28ffe369.jpg` — nguyên văn

> Tôi đã mở đúng một file ảnh được chỉ định và không mở file nào khác. Dưới đây là cảm nhận của một người xem bình thường.
>
> **Người này bao nhiêu tuổi, giới tính gì**
> - Đây là một bà cụ, khoảng 70–80 tuổi. Tôi đoán dựa trên mái tóc bạc trắng búi gọn, đôi hoa tai tròn nhỏ và chiếc áo len cổ lọ màu đỏ.
> - Nhân vật là hoạt hình 3D, được quay nghiêng từ phía sau, mặt hướng sang phải.
>
> **Đang cảm thấy gì**
> - Bà trông bình thản, hiền và hơi mãn nguyện. Khóe miệng như đang mỉm cười nhẹ, mắt khép hờ nhìn xuống.
> - Cảm giác chung là bà đang hồi tưởng hoặc nghĩ về một điều gì đó êm đềm, có chút hoài niệm.
> - Vì mặt quay nghiêng và mắt gần như không thấy rõ, cảm xúc khá mờ. Có người sẽ đọc thành buồn nhẹ hoặc buồn ngủ.
>
> **Những điều người xem có thể thấy lạ**
> 1. **Cổ quá dài và to.** Cổ trông như một khối trụ nhẵn, gần như nối thẳng từ má xuống. Không thấy đường hàm hay cằm rõ ràng. Đây là điểm dễ gây chú ý nhất.
> 2. **Da mặt căng mịn, không có nếp nhăn**, không hợp với mái tóc bạc của người già. Da còn có màu cam đậm như sáp hay nhựa.
> 3. **Tóc như những tấm giấy hoặc lá mỏng xếp chồng**, cứng và thành lớp. Nhìn không giống sợi tóc.
> 4. **Tai to, phẳng và nằm hơi lệch ra sau**, gần gáy. Hoa tai trông như dính vào dưới dái tai hơn là đeo tự nhiên.
> 5. **Khung hình cắt mất đỉnh đầu.** Mặt lại quay sát mép phải, còn rất ít khoảng trống phía trước mặt, nên hình có cảm giác chật và lệch.
> 6. **Ánh sáng không khớp với cảnh.** Mặt được rọi cam rất gắt trong khi nền tối gần như đen, không thấy nguồn sáng. Phần cổ thì sáng nhạt và phẳng hơn mặt, trông như hai phần không cùng một chất liệu.
> 7. **Mắt gần như chỉ là một khe nhỏ**, nên khó biết bà đang nhìn gì. Điều này làm cảm xúc thiếu rõ ràng.

#### so_ai — file mù `fa9df549.jpg` — nguyên văn

> Tôi chỉ mở đúng một file theo yêu cầu: /tmp/claude-0/-home-user-cine-lab/5b95043d-dd86-5cf7-9b06-17de07cfe1f8/scratchpad/matai/bl2so/fa9df549.jpg. Không mở hay tìm file nào khác.
>
> Ảnh là một nhân vật hoạt hình 3D phong cách hoá, nhìn nghiêng sang phải, khung cận cảnh từ vai trở lên. Nền tường tối, ánh sáng ấm.
>
> **Tuổi và giới tính**
> - Tuổi: một bà cụ, khoảng 65–75 tuổi. Tôi đoán vậy vì tóc bạc trắng, má và cằm hơi chảy, có nếp ở khoé miệng.
> - Giới tính: nữ. Bà đeo hoa tai vàng hai hạt, mặc áo len cổ lọ màu đỏ gạch, lông mày mảnh.
>
> **Cảm xúc**
> - Bà có vẻ đang chú ý, hơi ngạc nhiên hoặc tò mò, hoặc đang sắp nói gì đó. Miệng hé mở, mắt nhìn thẳng về phía trước, hơi hướng lên.
> - Nét mặt khá trung tính, không rõ vui hay buồn. Nếu chỉ xem một khung hình này, người xem khó đọc được cảm xúc cụ thể.
>
> **Những điểm người xem có thể thấy lạ**
> 1. **Tai quá to và đặt sai chỗ.** Tai rất lớn, nằm quá cao và quá lên trước, gần như ở giữa má. Chỗ này lộ nhất, khiến gương mặt trông méo.
> 2. **Tóc trông như mây tre đan.** Tóc là những sợi dẹt đan chéo nhau, giống giỏ mây hay vải bố hơn là tóc người. Ở gần tai, phần tóc này nối vào da khá đột ngột.
> 3. **Hoa tai như lơ lửng.** Hai hạt vàng nối bằng một que thẳng cứng, gắn ở phía dưới tai. Nhìn giống cái đinh ghim hơn là hoa tai thật.
> 4. **Khung hình bị cắt vụng.** Đỉnh đầu bị cắt mất. Góc trên bên phải có một mảng tối không rõ là gì, có thể là vành mũ hoặc một vật khác. Nó gây rối mắt.
> 5. **Da trơn như nhựa hoặc sáp.** Da gần như không có chi tiết bề mặt. Lông mày chỉ là một vệt cam mảnh vẽ lên. Mắt nhỏ và nông so với khuôn mặt.
> 6. **Cổ và cổ áo không khớp.** Cổ khá mảnh, nằm lọt trong cổ áo len rất dày. Nhìn như đầu được cắm vào thân.
>
> Nhận xét chung: chất liệu áo len và ánh sáng trông khá ổn. Riêng vị trí tai và kết cấu tóc có thể khiến người xem thấy nhân vật "kỳ kỳ" ngay từ cái nhìn đầu tiên.

#### so_bl — file mù `a382ac19.jpg` — nguyên văn

> Tôi chỉ mở đúng một file theo yêu cầu: /tmp/claude-0/-home-user-cine-lab/5b95043d-dd86-5cf7-9b06-17de07cfe1f8/scratchpad/matai/bl2so/a382ac19.jpg. Tôi không mở hay tìm file nào khác.
>
> **Người trong ảnh là ai**
> - **Tuổi:** Nhìn là thấy một bà cụ, khoảng 65–75 tuổi. Tóc bạc trắng, búi gọn ra sau, lông mày cũng bạc. Tuy vậy, da mặt lại căng, mịn và hầu như không có nếp nhăn, nên nếu chỉ nhìn da thì trông trẻ hơn tóc nhiều, chừng 40–50 tuổi.
> - **Giới tính:** Nữ. Người xem nhận ra qua bông tai vàng hai hạt tròn, kiểu tóc búi và áo len cổ lọ màu đỏ gạch. Sống mũi thẳng và dài, cằm và cổ khá đầy, nhưng không đến mức gây nhầm.
> - **Cảm xúc:** Bà đang mỉm cười hé miệng và nhìn về phía trước bên phải. Cảm giác là vui, hiền, có chút thích thú, như đang nói chuyện hoặc nhìn ai đó mình quý. Ánh sáng vàng cam từ bên trái làm khung hình ấm và dễ chịu.
>
> **Những điều người xem có thể thấy lạ**
> 1. **Không thấy rõ con mắt.** Ở góc nghiêng này lẽ ra phải thấy mí và mắt, nhưng chỗ đó chỉ là một mảng da trơn dưới lông mày. Đây là điểm dễ gây cảm giác "không ổn" nhất.
> 2. **Tuổi không khớp với làn da.** Tóc bạc trắng mà da căng bóng, mịn như nhựa, nên bà trông giống búp bê hoặc tượng sáp hơn là người già thật.
> 3. **Vành mũ tối màu ở góc trên bên phải trông như lơ lửng.** Người xem không hiểu vành mũ đó có đội trên đầu không, vì phía dưới vẫn thấy tóc trắng và không thấy phần chóp mũ nối vào.
> 4. **Bố cục lệch.** Tâm điểm của khung hình là cái tai và bông tai, còn khuôn mặt (nơi có cảm xúc) bị đẩy sát mép phải. Đỉnh đầu bị cắt, cổ và cổ áo chiếm gần nửa dưới khung hình. Người xem có thể không biết mình nên nhìn vào đâu.
> 5. **Tỉ lệ đầu và cổ hơi lạ.** Cổ trông rất to và dày so với đầu. Tai to và đặt khá thấp.
> 6. **Mảng trắng mờ ở góc trên bên trái** (có lẽ là búi tóc hoặc một vật khác) bị cháy sáng và không rõ hình, gây phân tán.
> 7. **Chất liệu:** Tóc trông như những rãnh khắc đều nhau chứ không như sợi tóc thật. Ngược lại, áo len đan lại rất chi tiết và chân thực, nên hai phần chênh nhau về độ kỹ.
>
> **Tóm lại:** Người xem sẽ thấy đây là một bà cụ hiền, đang vui vẻ mỉm cười. Nhưng việc không thấy mắt, làn da quá trẻ so với tóc và vành mũ lơ lửng nhiều khả năng khiến ảnh trông "hơi rợn", giống tượng hoặc búp bê hơn là một nhân vật sống.
