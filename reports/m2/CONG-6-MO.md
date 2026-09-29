# MỞ CỔNG 6: KHOÁ v1.5 · C3 LAYOUT 'bl' · GÓI CAS MPFB · KẾ HOẠCH DIỄN HOẠT

Nhánh: `claude/cine-lab-m2-cong5-layout-24o5fp`. Ngày 29/09/2026.
Quyết định gốc: AUTHORSHIP "Cửa mặt Ida (đóng)".
**DỪNG chờ chủ dự án duyệt TRƯỚC khi bắt đầu diễn hoạt.**

## 0. Tóm tắt
- **Khoá characters v1.5 xong, đã merge vào main: `cce7fb2c5842084e49f54d4c5288e797d81d6993`.**
  - bible v1.5, có ghi chú "Cas: chờ gói MPFB, sẽ lên v1.6";
  - ida.json cập nhật c3_views 8 góc, face, hat;
  - LIBRARY thêm glb và json của đầu Ida;
  - LOCK-THIET-KE khoá lại 28/28;
  - mặc định `IDA_STYLE='bl'`; page.js nạp trước glb.
- **Layout với 'bl'** (`design/cong5/layout/out/layout-v15.mp4`, 44,84 MB, SHA `8a5ebf01…`; layout.mp4 của Cổng 5 giữ nguyên):
  - render lại 52 shot; kiểm toán C3 **đạt** (lệch 0);
  - C3 vẫn **trượt** như Cổng 5; **2 shot đổi kết quả** (s15 KCM → trượt, s33 trượt → KCM);
  - H1b tệ hơn (track tệ nhất 25 % → 0 %).
- **Gói Cas MPFB (W4):** qua điều kiện dừng, dựng xong. **Kiểm mù nhẹ TRƯỢT**:
  - tuổi và giới đúng;
  - khung chỉ có Cas bị gọi "búp bê" **2/2** ("mắt búp bê", "da… như sáp hoặc búp bê");
  - khung hai người bị nói "hai phong cách trông không ăn nhập" **1/2**;
  - đối chứng 0/2.
  - Nháp v1.6 đã nộp, **chưa khoá**; mặc định vẫn Cas v1.4.
- **Kế hoạch Cổng 6** (mục 4): 4 gói.
  - Ước tính **khoảng 3,6–5,2 triệu token** và **khoảng 12–16 subagent kiểm**, cộng 1–2 lượt rà continuity.
  - Ước theo số đo thật của Cổng 5.

## 1. Khoá v1.5 và C3 trên layout
**SHA main sau khoá:** `cce7fb2c5842084e49f54d4c5288e797d81d6993` (merge nhánh @dd95625).

**Kiểm hình sau khi đổi mặc định:** P dò s02, s05, s13, s37, s39, s40w, s44, s45; 'bl' hiện đúng trong cảnh thật. Sau khi merge Cas (mặc định Cas v1.4), dò lại s02, s37, s45: lệch 0 px.

**Luật máy trên `layout-v15.mp4`** (`reports/checks/layout-v15/`):
- ĐẠT: N1, N2, P0, P1, G4, G3, M3, J1, J1b, H1, O3.
- TRƯỢT: G3b, H1b, C3.

| Chỉ số C3 | Cổng 5 (A-α, sheet v1.4) | v1.5 ('bl', sheet v1.5) |
|---|---|---|
| Mẫu đạt / trượt chắc chắn / không chứng minh được (KCM) | 6 / 51 / 47 | 5 / 54 / 45 |
| Biên trên lớn nhất | 36,35 % | 33,58 % |
| Khớp biên thấp nhất (≥ 1,5) | 0,749 | 0,769 |
| Shot CẦN NGƯỜI XEM | 22 theo luật (P gắn được 20 mã shot) | 22 (cùng 20 mã shot) |
| Kiểm toán (hạt giống, khung) | đạt | **đạt** (khung P chọn theo hạt giống; lệch điểm ảnh 0) |

**Shot đổi kết quả C3** (số lần theo mẫu: đạt / trượt / KCM; lệch lớn nhất):

| Shot | Cổng 5 | v1.5 |
|---|---|---|
| **s15** | KCM (0/0/2; 5,3 %) | **TRƯỢT** (0/1/1; 9,9 %) |
| **s33** | TRƯỢT (1/1/6; 7,5 %) | **KCM** (0/0/8; 3,7 %) |

- 14 shot khác giữ nguyên kết quả nhưng số đo đổi: s02, s07, s11, s13, s19, s23, s27, s30, s32, s35, s37w, s40w, s42a, s42.
- Ví dụ s42 từ 4/6/4 thành 4/10/0; s02 lệch lớn nhất từ 15,2 thành 18,8 %.
- Bảng đầy đủ: `reports/checks/layout-v15/so-sanh-C3-theo-shot.json`.

Luật khác:
- **H1b:** track tệ nhất 25 % → **0 %** (5 track toàn null như cũ). Đầu 'bl' đổi hình vùng nhân vật; sẽ xử lý cùng diễn hoạt Cổng 6.
- **G3b:** σ nhỏ nhất 0,748, σ lớn/nhỏ 2,889, tương quan khung kề như cũ (layout chưa có khâu grain).

**Chỉ số trong ±5 % quanh ngưỡng:**
- G3b biến thiên σ theo thời gian 0,201 (ngưỡng ≤ 0,2): **mới**.
- C3 hệ số mặt nạ 4 (ngưỡng ≤ 4).
- C3 hệ số khi đầu < 100 px 4 (ngưỡng ≥ 3,98).

## 2. Gói Cas MPFB (W4) và kiểm mù nhẹ
- **Dựng:** nam 10 tuổi (MPFB age 0,169) + 16 target (mắt to, mũi nhỏ hếch, má phính, tai vểnh).
  - Cùng hệ đầu và cùng luật cách điệu với Ida v1.5.
  - Mũ len có quả bông giữ nguyên; tóc #5a4034; tàn nhang.
  - Shape key cùng bộ 16 kênh + 6 khẩu hình + corrective.
  - Lưới 68 770 đỉnh, glb 11,2 MB.
- **Cờ:** `CAS_STYLE='bl'`, mặc định `'v14'`. RIGHTS: W4-MPFB-A2 (mở rộng phạm vi dùng cho Cas), không dùng tài sản mới.
- **Ảnh 4 góc:** `reports/m2/cong5/w4/CAS_eevee_4goc.jpg`.
- **Khung:**
  - `CAS_K1_nghieng.jpg`: s24c MS, 58,2 s;
  - `CAS_K2_chinhdien.jpg`: s38 MS, 106,7 s;
  - `CAS_K3_hai-nguoi.jpg`: s42a MS, 114,5 s;
  - `CAS_K4_hai-nguoi.jpg`: s41 WS, 112,8 s.
- **Kiểm mù:** 6 subagent mới, tên file ngẫu nhiên.
  - Khung chỉ có Cas và đối chứng dùng câu hỏi y hệt mặt Ida.
  - Khung hai người đổi "Người này" thành "Những người trong ảnh", phần còn lại y hệt.

| Khung | Tuổi / giới | Từ khoá chỉ vào mặt/đầu Cas | Lệch phong cách hai người | Lời chê nổi bật |
|---|---|---|---|---|
| K1 nghiêng (s24c) | cậu bé 9–12 ✔ | **2**: "mắt bóng nhưng vô hồn, như mắt **búp bê**"; "hình dựng 3D kiểu **búp bê**" | — | cổ "như cái que"; thân áo phồng; mũ "đậu trên đỉnh như nồi úp"; uncanny |
| K2 gần chính diện (s38) | cậu bé 10–13 ✔ | **1**: "da hơi trắng bệch và trơn như sáp hoặc **búp bê**" | — | tay không nắm thang; cổ dài "cổ cò" |
| K3 hai người (s42a) | bà cụ 70–80 ✔; cậu bé 8–11 ✔ | 0 ("tư thế cứng như ma-nơ-canh" chỉ tư thế cả hai) | **CÓ**: "cạnh bà cụ tạo hình khá thực tế thì **hai phong cách trông không ăn nhập**" | tay cầm đèn không thật; đèn loá |
| K4 hai người (s41) | "nhiều khả năng bà cụ… cũng có thể ông cụ" (≈); cậu bé 7–10 ✔ | 0 | không | mặt quá nhỏ, không đọc cảm xúc |
| Đối chứng SF 104,5 s | bé gái 9–12 | 0 | — | — |
| Đối chứng SF 332 s | nữ 40–55 | 0 | — | — |

**Tiêu chí:**
- Tuổi và giới đúng: ✔ (K4 Ida "nhiều khả năng bà cụ").
- 0 từ khoá chỉ vào mặt/đầu Cas: **✘** (2/2 khung Cas).
- Không bị nói lệch phong cách: **✘** (1/2).
- Đối chứng 0/2 ✔.
- **TRƯỢT.**

**Đọc số:**
- Lời "búp bê" ở Cas trùng đúng lời chê còn lại của Ida ở khung chính diện: **mắt bóng, vô hồn**. Mục sửa b(1) của Cổng 6 ("mắt: bớt bóng kiểu mắt búp bê, mí che bớt tròng, viền nước") áp cho **cả hai** nhân vật.
- Cổ dài, mảnh là **số sheet Cas** (cổ 0,22 × 0,26 H). Sửa cổ phải đổi sheet (v1.6), nằm ngoài quyền của W4.
- "Lệch phong cách" ở K3 nói Ida "khá thực tế" còn Cas thì không. Đây là rủi ro lưới người MPFB mà chủ dự án đã dặn đếm riêng; nay xuất hiện lần đầu.

**Nháp v1.6 (Cas)**, chưa khoá: `reports/m2/cong5/w4/characters-v1.6-NHAP.md`.
- c3_views thân 0° 1,379 / 180° 1,370 (v1.4: 1,669 / 1,656); ±45° +0,2 / +0,4 %; ±90° +3,8 / +4,7 %; ±135° +6,0 / +6,9 %.
- **Cần P/K quyết:** ở 0° và 180°, đầu nhìn thấy dưới mũ len rộng hơn cao (tai vểnh), nên trục PCA lật ngang. Theo bề dọc thì thân/đầu = 2,229 (0°), 2,704 (180°). Đây là giới hạn phép đo 2D, P không sửa checks/.

## 3. Shot có Ida quay chính diện hoặc gần chính diện (≤ 30°): PLAN Cổng 6 mục c
**Cách lập:**
- Góc **thân** Ida so với trục máy đo từ C3 (mỗi 12 khung; `view_deg`).
- Cộng **ước lượng bằng mắt** hướng **mặt** trên khung giữa shot của layout v1.5 (P xem 35 shot có Ida). Đầu có thể quay khác thân, ví dụ s37: thân −42° nhưng mặt nhìn máy.
- Cỡ cảnh theo bảng shot.

| Shot | Thời gian | Cỡ, ống kính | Góc thân (C3) | Mặt (ước bằng mắt) | Chưa sửa mắt thì |
|---|---|---|---|---|---|
| **s22** | 0:49,5–0:52,5 | MCU 85 mm | 18° | gần chính diện, hai mắt rõ | **Đổi cỡ:** MS hoặc xoay 3/4 > 30° |
| s26 | 1:02–1:04 | MS 50 mm | 15° | chính diện | Giữ MS (mặt vừa); không đẩy vào cận |
| **s36** | 1:31–1:33 | MCU 85 mm | 25° | gần chính diện | **Đổi:** theo PA1 (3/4 nghiêng, đã chọn) |
| **s37** | 1:33–1:38,8 | CU 85 mm | 42° (mặt quay về máy) | chính diện | **Đổi:** theo PA1 (s37a/b/c nghiêng) |
| **s39** | 1:41,6–1:46 | CU 85 mm | 24° | chính diện | **Đổi:** theo PA1 (s39′ CU nghiêng 96°) |
| **s40** | 1:47,4–1:50 | CU (insert) 50 mm | 5° | chính diện, sau lồng đèn, mặt cỡ MCU | **Đổi:** cho mặt khuất (vành mũ hoặc lồng đèn) hoặc lùi WS |
| s30 | 1:12–1:14 | MS 35 mm | > 30° (C3) | gần chính diện, rất nhỏ | Giữ |
| s42a | 1:53,5–1:55,5 | MS 45 mm | > 30° (C3) | gần chính diện, nhỏ (Ida WS) | Giữ |
| s42 | 1:57,5–2:00,5 | MS 40 mm | 23° | chính diện, nhỏ ở hậu cảnh | Giữ |
| s02, s08, s24, s35 | — | WS / EWS | 28° / 11° / 27° / 13° | mặt < 15 px | Giữ |
| s31 (theo dõi) | 1:14–1:17 | MCU 85 mm | — | 3/4 khoảng 35–45° | Giữ 3/4, không xoay thêm về máy |

**Phải đổi cỡ nếu chưa sửa mắt: s22, s36, s37, s39, s40** (s36–s39 đã nằm trong dàn dựng lại PA1).

## 4. Kế hoạch Cổng 6 (chưa làm), ước tính token theo gói
Căn cứ đo thật ở Cổng 5: W1 566–690 nghìn mỗi vòng; W2 226–770 nghìn mỗi vòng; W3 407–737 nghìn mỗi vòng; W4 3 lượt mặt Ida + Cas khoảng 709 nghìn; 1 lượt continuity khoảng 220 nghìn; mỗi subagent kiểm khoảng 49–50 nghìn. Số dưới đây là **ước tính**, không phải số đo.

| Gói | Phạm vi | Ước token | Kiểm dự kiến |
|---|---|---|---|
| **W4 — nhân vật (trước diễn hoạt)** | (b1) mắt Ida và Cas: bớt bóng, mí che tròng, viền nước; (b2) mũ ôm đầu; (b3) mắt góc nghiêng; (b4) tay MPFB Ida (và Cas nếu duyệt), cầm cột và van; cổ Cas theo sheet v1.6 nếu duyệt | 0,4–0,6 triệu | 6 subagent (2 Ida chính diện, 2 Cas, 2 đối chứng) |
| **W1 — diễn hoạt cảnh 1–3** (23 shot) | diễn hoạt, tay cầm, lip-sync L1–L2, s22 đổi cỡ | 1,0–1,4 triệu (2 vòng) | continuity cảnh 1–3 |
| **W2 — diễn hoạt cảnh 4–6** (29 shot) | **dàn dựng lại PA1 s36–s39**, lip-sync L3–L4, s40 đổi, B1 cảnh 6 (hướng mặt, đồng hồ), các mục G2/G5/G6/G10/G11/G13 | 1,2–1,6 triệu (2 vòng) | — |
| **P** | tích hợp, render, luật, báo cáo | 0,3–0,5 triệu | — |
| **Kiểm** | (a) nhịp cười buồn: clip có tiếng + bảng khung mỗi 0,5 s kèm phụ đề, 2 nhịp × 1 subagent + 2 đối chứng; kiểm mù shot sau sửa mắt; rà continuity 1–2 lượt | 0,6–1,1 triệu | khoảng 12–16 subagent + 1–2 agent rà |
| **Tổng** | | **khoảng 3,6–5,2 triệu** | |

Thứ tự đề xuất: **W4 (nhân vật) trước**, vì mắt, mũ và tay ảnh hưởng mọi shot; sau đó W1 và W2 song song; cuối cùng kiểm (a) trên clip có tiếng.

## 5. Quyết định cần chủ dự án
**Cas:**
- **A. Duyệt Cas 'bl' làm nền, sửa trong gói W4 nhân vật trước diễn hoạt.** Gói gồm mắt chung với Ida, cổ theo sheet v1.6 (P soạn số cổ mới), mũ ôm đầu. Kiểm lại nhẹ Cas sau gói W4 (đã tính trong 6 subagent ở trên), rồi mới khoá v1.6.
  - Ưu: cùng một hệ với Ida; lời chê trùng mục sửa mắt đã lên kế hoạch.
  - Nhược: chưa đạt kiểm mù; lệch phong cách 1/2.
  - Rủi ro: lưới MPFB đọc "thực tế" cạnh nhau.
- **B. Giữ Cas v1.4 (mặt vẽ tay).**
  - Ưu: không thêm việc.
  - Nhược: đầu Ida và Cas khác kiểu dựng; nguy cơ lệch phong cách cao hơn.
- **C. Làm thêm một lượt riêng cho Cas trước gói W4 nhân vật.**
  - Nhược: trùng việc sửa mắt, tốn thêm khoảng 150 nghìn token và 6 subagent.
- **Khuyến nghị: A.** Lời chê Cas (mắt, cổ, mũ) nằm đúng trong gói W4 nhân vật đã lên kế hoạch cho cả hai.

**Các điểm khác:**
- Cách đo C3 Cas ở 0°/180° (PCA lật ngang): cần phiên K quyết. P đề xuất ghi số theo bề dọc vào sheet v1.6 và nêu giới hạn.
- Duyệt kế hoạch Cổng 6 (mục 4) và thứ tự gói.

## 6. Thời gian, token, hàng đợi (từ 28/09 22:50 tới 29/09 01:00 UTC)
| Việc | Thời gian | Token | Hàng đợi |
|---|---|---|---|
| P khoá v1.5, dò, render lại layout 52 shot, ghép, đóng gói, mặt nạ C3, kiểm toán, luật | render 4 324 s, ghép 476 s, đóng gói 193 s, mặt nạ C3 556 s, kiểm toán 7 s, luật 399 s | — | P: 8 việc, chờ 98 s, chạy 6 095 s |
| W4 gói Cas MPFB | 23:03 → 00:55 (1 giờ 52 phút, trong đó khoảng 81 phút chờ làn nặng vì P render) | khoảng 100 nghìn (công cụ báo 708 757 khi kết thúc, trước đó 608 635) | W4: 20 việc, chờ 4 599 s, chạy 602 s |
| P kiểm mù Cas: 6 subagent | 27–38 s mỗi subagent | 49 209–50 578 mỗi subagent | — |

## 7. Nguyên văn subagent kiểm mù Cas (cả đối chứng)
#### CAS_K1_nghieng — file mù `6832730f.jpg` — nguyên văn

> Tôi đã mở đúng một file ảnh: /tmp/claude-0/-home-user-cine-lab/5b95043d-dd86-5cf7-9b06-17de07cfe1f8/scratchpad/matai/cas/6832730f.jpg. Tôi không mở hay tìm file nào khác.
>
> **Ấn tượng của một người xem bình thường**
> - **Tuổi:** trông là một cậu bé khoảng 9–12 tuổi.
> - **Giới tính:** nam, vì tóc ngắn, mặt con trai, đội mũ len có quả bông đỏ, mặc áo len đỏ sẫm và quần tối màu.
> - **Cảm xúc:** buồn, trầm ngâm, có chút lạc lõng hoặc lo lắng. Mắt liếc sang trái khung hình, mí mắt hơi sụp. Môi mím và hơi trề, lông mày hơi chau. Cảm giác như cậu đang đứng một mình chờ ai đó, hoặc vừa bị bỏ lại. Tuy vậy, biểu cảm khá "đơ", đọc được là buồn nhưng thiếu sức sống.
>
> **Những điều người xem có thể thấy lạ**
> 1. **Cổ quá dài và mảnh, như một cái que.** Đầu trông như cắm lên trên áo chứ không nối liền với thân. Cổ áo len rộng và hở, nên cổ lộ ra rất rõ. Màu da ở cổ cũng sáng và cam hơn mặt.
> 2. **Thân áo phồng như bóng bay.** Vai vuông cứng, không thấy hình dạng tay hay khuỷu tay bên trong. Tay áo rủ thẳng như cái ống.
> 3. **Bàn tay ở góc dưới bên trái mờ và cụt,** trông như một khúc gỗ, không rõ ngón tay.
> 4. **Mũ len không ôm đầu mà đậu trên đỉnh đầu** như một cái nồi úp. Mép tóc bị cắt ngang cứng dưới vành mũ. Có một lọn tóc lẻ lòi ra sau tai.
> 5. **Tai to và nằm hơi lùi ra sau,** mặt thì hơi dẹt. Đôi mắt bóng nhưng "vô hồn", như mắt búp bê.
> 6. **Bóng đổ mờ trên tường bên phải không khớp với cậu bé.** Nó là một mảng loang, không có hình mũ hay quả bông, và nằm quá xa. Trông như bóng của một thứ gì khác ngoài khung hình.
> 7. **Bức tường gạch trông phẳng như giấy dán tường,** không có độ sâu ở mạch gạch. Nửa bên phải tường nhạt dần như bị sương hoặc bị cháy sáng. Đường giao giữa tường và sàn nghiêng lệch và hơi gợn.
> 8. **Góc dưới bên phải có một tấm lưới hoặc nắp cống lỗ tròn** xuất hiện đột ngột, khó hiểu là vật gì.
> 9. **Nhìn tổng thể là hình dựng 3D kiểu "búp bê",** chưa có cảm giác một nhân vật hoạt hình hoàn thiện. Đây là hiệu ứng "thung lũng kỳ lạ" (uncanny valley): nhân vật gần giống người thật nhưng không hẳn, nên người xem thấy hơi rờn rợn. Chỗ gây cảm giác này mạnh nhất là phần cổ và vai.

#### CAS_K2_chinhdien — file mù `8048ff61.jpg` — nguyên văn

> Tôi đã mở đúng một file 8048ff61.jpg và không mở file nào khác. Dưới đây là cảm nhận của một người xem bình thường.
>
> **Tuổi và giới tính:** Trông như một cậu bé khoảng 10–13 tuổi. Cậu tóc nâu sẫm, đội mũ len màu kem có quả bông đỏ, mặc áo len đỏ và quần xanh đậm.
>
> **Cảm xúc:** Cậu có vẻ buồn, lo lắng hoặc ngập ngừng, như đang cam chịu. Lông mày hơi nhíu và xếch lên ở giữa, môi mím lại. Mắt cậu nhìn chếch lên về phía bên trái khung hình, về phía một nhân vật người lớn mặc áo choàng xanh ngọc và tím. Cảm giác như cậu đang nghe người đó nói hoặc chờ bị la. Nét mặt khá kín đáo, không bộc lộ mạnh.
>
> **Những điểm người xem có thể thấy lạ:**
> 1. **Hai bàn tay:** Tay phải của cậu (bên trái ảnh) như đang lơ lửng cạnh thang, không thật sự nắm vào thanh gỗ nào. Tay trái (bên phải ảnh) lại xoè ra giữa không trung, không cầm gì, trông như bị cắt rời khỏi động tác. Hai bàn tay cũng trông to, bè và hơi thô so với cơ thể.
> 2. **Cổ quá dài và mảnh:** Cổ lộ ra khỏi cổ áo len rộng. Trông hơi mất cân đối, gần như "cổ cò".
> 3. **Cánh tay:** Hai cánh tay dài và duỗi thẳng ra trước một cách cứng đờ, dáng đứng thiếu tự nhiên.
> 4. **Nhân vật bên trái bị cắt:** Chỉ thấy vạt áo choàng xanh ngọc và phần váy tím, không thấy chân hay thân trên. Trông như một khối vải lơ lửng, người xem khó hiểu đó là ai và đang đứng đâu.
> 5. **Nền đá cuội:** Các viên đá hình bầu dục rất đều, lặp lại như hoa văn, trông giống tấm vải chấm bi hơn là mặt đường thật. Chỗ giáp với nền đá lát lớn cũng hơi đột ngột.
> 6. **Chiếc thang:** Thang dựng nghiêng nhưng không rõ tựa vào đâu. Chân thang trông như chạm thẳng vào vạt áo của nhân vật kia.
> 7. **Da mặt:** Da hơi trắng bệch và trơn như sáp hoặc búp bê. Đôi mắt có chút "vô hồn", nhìn hơi mơ hồ, không thật sự khoá vào một điểm.
>
> **Tóm lại:** Người xem sẽ hiểu ngay đây là một cậu bé buồn hoặc bất an đang ngước nhìn người lớn. Tuy vậy, tư thế tay không cầm gì và phần cổ dài là hai chỗ dễ gây cảm giác "có gì đó sai sai" nhất.

#### CAS_K3_hai-nguoi — file mù `186d27ae.jpg` — nguyên văn

> Tôi chỉ mở đúng một file: /tmp/claude-0/-home-user-cine-lab/5b95043d-dd86-5cf7-9b06-17de07cfe1f8/scratchpad/matai/cas/186d27ae.jpg. Dưới đây là cảm nhận của một người xem bình thường.
>
> **Tổng quan:** Đây là một khung hình hoạt hình 3D. Hai nhân vật đứng trên con phố lát đá, trước một bức tường trắng có cửa vòm tối. Bên phải có cột đèn và một chiếc thang gỗ dựng vào tường.
>
> **Người thứ nhất (bên trái): một bà cụ**
> - Tuổi: khoảng 70–80. Tóc bạc búi sau gáy, mặt nhiều nếp nhăn, lưng hơi còng.
> - Giới tính: nữ. Bà đội mũ phớt đen, quàng khăn len hồng đỏ, mặc áo khoác dài xanh rêu, váy tím sẫm và đeo hoa tai.
> - Cảm xúc: nghiêm, dè dặt, có thể hơi nghi ngờ hoặc đang cân nhắc. Bà nhìn nghiêng về phía cậu bé, khoé miệng trễ xuống, không cười. Bàn tay trái hơi ngửa ra như sắp nói gì hoặc sắp đưa tay ra.
>
> **Người thứ hai (ở giữa): một cậu bé**
> - Tuổi: khoảng 8–11.
> - Giới tính: nam, theo cảm nhận. Cậu đội mũ len trắng có quả bông đỏ, mặc áo len đỏ cam, quần sẫm màu, đi giày đen và đeo găng tay trắng.
> - Cảm xúc: rụt rè, căng thẳng hoặc hơi hờn dỗi. Cậu mím môi, mắt nhìn ngang sang phải chứ không nhìn bà cụ. Hai tay cậu giữ chiếc đèn lồng sát ngực như đang che chở nó. Cả dáng đứng cứng đơ, hai chân khép sát như đang chịu trận hoặc đang chờ bị hỏi chuyện.
>
> **Những điều người xem có thể thấy lạ**
> 1. **Tay cầm đèn lồng không thật.** Hai bàn tay đeo găng chụm lại ở ngang ngực, phía trên đèn, trông như đang chắp tay. Đèn lại treo lơ lửng bên dưới, không thấy tay nắm vào quai. Nhìn như đèn tự bay.
> 2. **Ánh đèn quá gắt và vô lý.** Đèn sáng loá, làm áo và tay cậu bé đỏ rực như phát sáng. Trong khi đó mặt đất, mặt cậu bé và bà cụ gần như không nhận chút ánh sáng nào. Cảnh xung quanh lại khá sáng, giống ban ngày, nên người xem khó hiểu vì sao cần đèn lồng.
> 3. **Nhân vật trông như lơ lửng.** Dưới chân hai người gần như không có bóng đổ, nên cả hai như được dán lên nền chứ không đứng hẳn trên đường.
> 4. **Tư thế cứng như ma-nơ-canh.** Cả hai đứng thẳng đơ, tay buông, không có chuyển động cơ thể tự nhiên. Tay trái bà cụ ngửa ra trông gượng.
> 5. **Hướng nhìn không khớp.** Bà cụ nhìn về phía cậu bé, còn cậu bé nhìn lệch sang phải. Vì vậy khó biết hai người có đang nói chuyện với nhau hay không.
> 6. **Bối cảnh hơi trống và giả.** Cửa vòm là một mảng đen phẳng, không có chiều sâu. Mấy thanh cột đen bên trái không rõ là gì. Đá lát bên trái là các chấm tròn đều tăm tắp, giống hoa văn lặp. Chiếc thang dựng cạnh cột đèn trông ngẫu nhiên. Cột đèn bị cắt khỏi khung nên không thấy bóng đèn.
> 7. **Tỉ lệ cậu bé hơi lạ.** Đầu to, cổ và chân rất mảnh, thân ngắn. Đây có thể là phong cách cố ý, nhưng cạnh bà cụ tạo hình khá thực tế thì hai phong cách trông không ăn nhập.

#### CAS_K4_hai-nguoi — file mù `88b32b21.jpg` — nguyên văn

> Tôi đã mở đúng một file: /tmp/claude-0/-home-user-cine-lab/5b95043d-dd86-5cf7-9b06-17de07cfe1f8/scratchpad/matai/cas/88b32b21.jpg. Đây là khung hình hoạt hình 3D phong cách hoá: một phố lát đá vắng người, hai nhân vật đứng dưới một cột đèn đường cổ.
>
> **Hai nhân vật**
> - **Người lớn tuổi (bên trái, sát cột đèn):** trông khoảng 65–75 tuổi. Tóc bạc trắng, đội mũ đen, quàng khăn đỏ, mặc áo choàng dài màu xanh lục và thắt dây lưng. Nhiều khả năng là **bà cụ** vì dáng người và áo dài như váy, nhưng không chắc hẳn; cũng có thể là một ông cụ. Cạnh người này có chiếc thang dựa vào cột đèn, nên người xem dễ đoán đây là người thắp đèn đường. Bà đang đưa chiếc đèn lồng đang cháy về phía đứa trẻ.
> - **Đứa trẻ (bên phải):** trông khoảng 7–10 tuổi, nhiều khả năng là **bé trai**. Cậu đội mũ len trắng có quả bông đỏ, mặc áo len đỏ và quần sẫm màu. Cậu giơ hai tay về phía đèn lồng, như đang hơ tay cho ấm hoặc định đón lấy đèn.
> - **Cảm xúc:** mặt quá nhỏ và đơn giản nên gần như không đọc được nét mặt. Người xem chỉ đoán được qua dáng người. Người lớn tuổi có vẻ hiền hậu, ân cần. Đứa trẻ tò mò, háo hức, có lẽ hơi lạnh. Cả cảnh gợi sự ấm áp và gần gũi giữa hai thế hệ, trong một buổi chiều muộn se lạnh.
>
> **Những điều người xem có thể thấy lạ**
> 1. **Tỉ lệ bị lệch:** hai nhân vật quá nhỏ so với cửa vòm và bức tường. Cửa vòm cao gấp khoảng 2–3 lần người lớn, nên nhân vật trông như đồ chơi đặt trong một phông nền khổng lồ.
> 2. **Tường trống và phẳng:** mặt tường trắng rất lớn, gần như không có chi tiết, vết bẩn hay dấu thời gian. Chỉ có vài ô cửa sổ nhỏ đặt rất cao, nên trông giống phông trường quay hơn là nhà thật.
> 3. **Các thanh cột đen khó hiểu:** bên trái có mấy thanh đen dài rủ từ mái đua xuống tới đất. Bên phải có một cột đen đứng trơ trọi, không nối với vật gì rõ ràng. Người xem khó hiểu chúng là gì.
> 4. **Mái đua và cánh cửa chớp:** phần mái nhô ra ở góc trên bên trái trông như lơ lửng. Các cánh cửa chớp màu nâu treo ở vị trí hơi kỳ, trong đó có một cánh nằm sát mép khung hình.
> 5. **Đá lát đường giống chấm bi:** đá trên mặt đường là những viên tròn đều tăm tắp, lặp lại như họa tiết chấm bi. Ở tiền cảnh, chúng tạo cảm giác nhiễu mắt và giả.
> 6. **Ánh sáng chưa khớp:** trời trông như ban ngày hoặc chạng vạng khá sáng, nên ánh đèn lồng không nổi bật lắm. Đèn đường chưa sáng, mà cũng không có ai trên thang.
> 7. **Cảnh quá vắng:** cả khung hình chỉ có hai nhân vật, chiếm một góc nhỏ ở giữa. Phần lớn khung hình là tường trống và mặt đường, nên bố cục trông trống trải.
> 8. **Chi tiết nhỏ:** có một sợi dây màu vàng buộc trên cột đèn và một cái vòng hay móc treo gần ô cửa sổ trên cao, không rõ để làm gì.

#### doichung_sf_104.5 — file mù `e3180977.png` — nguyên văn

> Tôi đã xem đúng một file: /tmp/claude-0/-home-user-cine-lab/5b95043d-dd86-5cf7-9b06-17de07cfe1f8/scratchpad/matai/cas/e3180977.png. Không mở file nào khác.
>
> Nhận xét dưới góc nhìn người xem bình thường:
>
> - **Tuổi:** trông như một bé gái khoảng 9 đến 12 tuổi, tức là tuổi tiểu học hoặc đầu cấp hai. Mặt tròn, mắt to, người nhỏ.
> - **Giới tính:** nữ.
> - **Cảm xúc:** bé đang bối rối, lo lắng, hơi ngỡ ngàng hoặc nghi ngại. Lông mày nhướng lên và chau vào giữa, mắt mở to liếc lên phía trên bên trái, miệng hé tròn như vừa thốt "hả?" hoặc "ơ…". Bé ôm chặt cuốn sổ trước ngực, một tư thế tự che chắn. Tôi đọc đây là cảm giác bất an, không chắc chắn trước điều gì đó bé vừa thấy hoặc nghe, chứ không phải hoảng sợ tột độ.
>
> Bối cảnh: một khu rừng sẫm màu lúc chạng vạng. Có thân cây lớn màu nâu đỏ, bụi lá xanh rậm và những cây nấm đỏ bóng rải rác trên nền cỏ. Nhân vật là hoạt hình 3D phong cách hoá.
>
> Những điểm người xem có thể thấy lạ:
> 1. **Bím tóc đuôi ngựa** rất to, dựng ngược lên cao, gần như bất chấp trọng lực. Các sợi tóc xơ cứng và có ánh xám bạc, trông giống chổi lông hoặc đuôi thú hơn là tóc người. Đây là chi tiết nổi bật nhất.
> 2. **Phụ kiện quá cỡ:** đôi khuyên tai tròn màu hồng tím rất to và dày, cùng chiếc vòng tay (hoặc đồng hồ) nhựa vàng đỏ to bản, trông như đồ chơi.
> 3. **Cổ áo** màu đỏ cam có hình răng cưa, nhọn như cánh hoa hoặc vây, khá lạ mắt so với chiếc áo xanh.
> 4. **Cuốn sổ** có nhãn bị tay che mất một phần, chỉ đọc được "…ology" (có thể là "Biology" hoặc "Zoology"), kèm hình vẽ chiếc lá. Có lẽ bé là một nhà khám phá hoặc mê sinh học nhỏ tuổi.
> 5. **Nấm đỏ** bóng như nhựa, có vài cây mọc lơ lửng ở vị trí khó hiểu, ví dụ góc phải phía dưới.
> 6. **Khung hình kỹ thuật:** ảnh rất dẹt, khoảng 1920x804 (tỷ lệ gần 2.39:1, kiểu màn ảnh rộng điện ảnh), không phải 16:9.
>
> Lưu ý cho dự án: chất lượng render và thiết kế nhân vật trông như một khung hình cắt từ một phim hoạt hình thương mại có sẵn, không giống sản phẩm nội bộ. Nếu ảnh này là tham chiếu, cần ghi vào RIGHTS.md và không sao chép thiết kế nhân vật, theo luật cứng trong CLAUDE.md. Đây chỉ là nhận định bằng mắt, tôi chưa kiểm chứng nguồn gốc.

#### doichung_sf_332 — file mù `a8af9757.png` — nguyên văn

> Tôi đã mở đúng một file ảnh (a8af9757.png) và không mở file nào khác.
>
> Đây là một nhân vật hoạt hình 3D phong cách hoá, không phải người thật. Cảnh tối, ánh sáng xanh lam lạnh, có sương mờ.
>
> **Tuổi:** trông như một người phụ nữ trung niên, khoảng 40 đến 55 tuổi. Tôi đoán vậy vì kiểu trang điểm và trang sức "retro" thập niên 80, cùng vài nếp nhăn ở cằm và má.
>
> **Giới tính:** nữ. Các dấu hiệu là mi dài, trang điểm mắt đậm, son môi tím, khuyên tai lớn và vòng cổ chuỗi hạt.
>
> **Cảm xúc:** một cơn bộc phát tiêu cực mạnh, pha giữa giận dữ, ghê tởm và hoảng sợ hay đau khổ. Mắt nhắm nghiền, lông mày nhíu sâu, miệng méo, nhe răng như đang gào hoặc rên lên. Bàn tay xoè thẳng về phía máy quay như muốn nói "Dừng lại!", "Tránh ra!" hay "Đừng nhìn tôi!". Nhìn chung là đang chối bỏ và đẩy thứ gì đó ra xa.
>
> **Điều người xem có thể thấy lạ:**
> - **Vệt đen dưới mắt:** mảng đen nhòe dưới cả hai mắt trông như lớp mascara bị chảy hoặc bóng mắt quá đậm. Người xem có thể hiểu là cô vừa khóc, hoặc thấy mặt hơi "bẩn" hay đáng sợ.
> - **Khuôn mặt:** mặt tròn và nhẵn như quả trứng, nghiêng hẳn sang một bên. Mũi ửng hồng, trông tách màu khỏi phần còn lại của mặt.
> - **Bàn tay:** rất to vì ở sát ống kính, ngón dài và nhợt, hơi mờ nhòe. Tay áp sát đến mức trông như đang úp vào mặt kính hay màn hình.
> - **Đôi khuyên tai:** kiểu hình học (tam giác, thanh dài) màu xanh tím, hai bên trông không giống nhau. Có thể do góc nhìn, nhưng dễ gây chú ý.
> - **Cằm:** có vài vạch nhỏ, trông như vết xước, nếp nhăn hoặc râu lún phún, hơi khó hiểu.
> - **Tóc:** màu vàng ngả xanh rêu dưới ánh sáng lạnh, rối tung.
> - **Trông như khung hình cắt từ video:** hơi nhoè, có dấu nén ảnh. Nếu đây là ảnh lấy từ phim của người khác để làm tham chiếu, cần nhớ luật của dự án: không sao chép thiết kế hay nhân vật, và phải ghi tham chiếu vào `RIGHTS.md`.
