# CỔNG 6 — GÓI THÂN CAS (W4T): KIỂM MÙ **TRƯỢT** → KHÔNG KHOÁ, DỪNG CHỜ CHỦ DỰ ÁN

Nhánh: `claude/cine-lab-m2-cong5-layout-24o5fp` (W4T merge @f8c7455). Ngày 29/09/2026.
Quyết định gốc: AUTHORSHIP "Cổng 6 — nhân vật" và chỉ thị "Quyết định sau gói W4 và checks v1.5".

**Không làm những việc sau** (đúng mục 4 của chỉ thị, nhánh TRƯỢT):
- không khoá v1.5.1 hay v1.6;
- không đổi `CAS_STYLE`, `CAS_BODY` hay tay mặc định;
- không render layout-v16, không chạy luật trên layout-v16;
- không merge main; không mở W1, W2.

Mặc định layout vẫn như cũ: dò s02, s24c, s37, s42 trước/sau gói, 12 ảnh nhỏ, lệch 0 px.

## 0. Tóm tắt
- **Gói thân (W4T):**
  - bước a (khả thi) **ĐẠT**;
  - bước b **làm được một phần**: thân, áo len cổ lật cao, quần, măng sét; sửa cổ tay Ida và Cas; sửa khe mũ len; đo C3;
  - bước b chưa làm, vì hết hạn token: gai mảnh ở gáy Cas; áo len còn hơi ôm.
- **Kiểm mù 5 subagent: TRƯỢT ở một tiêu chí.** 2/3 khung có Cas bị gọi bằng từ khoá, và cả hai lần đều chỉ vào **thân**, không chỉ vào mặt:
  - "chân bé thẳng, mỏng và quần bó sát, trông như **búp bê**";
  - "dáng đứng thẳng đơ như **ma-nơ-canh**".
- **Tiến bộ thật:** lần đầu tiên **0/2 khung hai người bị nói "lệch phong cách"** (W4N: 1/1). Mặt Cas không bị gọi búp bê hay mặt nạ ở cả 3 khung.
- **C3:**
  - Cas theo 'doc': thân/đầu 2,39–2,51 ở các góc trước và nghiêng, 3,12 ở góc 180°;
  - Ida v1.5.1 theo 'pca': thân lệch ≤ 0,14 % so với `ida.json` v1.5.

## 1. Ảnh trước/sau (W4T, `reports/m2/cong6/w4t/`)
| Ảnh | Nội dung |
|---|---|
| `W4T_truoc-sau_than.jpg` | Thân Cas: v1.4 (áo ống, vai vuông) → MPFB (ngực, lưng, eo, vai dốc; tay áo theo cơ) |
| `W4T_truoc-sau_co-tay.jpg` | Cổ tay: mảng đen lởm chởm (Ida, Cas) → cắt phẳng, bịt nắp; Cas có măng sét len, Ida có lót măng sét |
| `W4T_truoc-sau_mu-len.jpg` | Khe đen đỉnh mũ len → vòm liền |
| `W4T_kha-thi.jpg` | Bước a: tư thế sheet và tư thế s42a cầm đèn lồng, 0°/90°/180° |
| `W4T_cas_eevee_4goc.jpg` | Cas EEVEE 4 góc (vẫn thấy gai gáy ở 180°) |
| `W4T_hai-nguoi_s42a.jpg`, `W4T_hai-nguoi_WS.jpg` | Khung hai người: s42a MS 114,5 s và s41 WS 112,8 s |
| `W4T_cas_toan-than_cat.jpg` | Cas toàn thân, do P cắt từ s42a (560,250 → 1920,1015) |

Bản mù (đúng file đã nộp cho subagent) và bảng tên: `reports/m2/cong6/kiem-mu-than/`.

## 2. Kiểm mù (P, 5 subagent mới, mỗi subagent mở đúng 1 ảnh)
**Cách làm:**
- Câu hỏi y như các vòng trước: tuổi, giới, cảm xúc, điều gì lạ.
- Đếm từ khoá bằng máy (regex), không đếm tay.
- Hai khung đối chứng lấy từ Sprite Fright, 104,5 s và 332 s.

| Khung (tên mù) | Tuổi/giới | Lệch phong cách | Từ khoá chỉ vào Cas | Lời chê khác đáng chú ý |
|---|---|---|---|---|
| Hai người s42a MS (`2fdcbd31`) | Ida nữ 65–75 ✔; Cas 7–10, "nhiều khả năng là bé trai" ✔ | **Không** | **1** (thân): "Chân bé thẳng, mỏng và quần bó sát, trông như **búp bê**" | đèn lồng không chiếu ra xung quanh; không bóng tiếp đất; hai người đứng "như tượng" |
| Hai người s41 WS (`80f51cba`) | Ida "bà cụ… có thể là ông cụ" (mặt quá nhỏ); Cas "bé trai, không chắc" ✔ | **Không** | 0 | tay đứa trẻ "trắng sáng như đeo găng"; vòng dây treo giống thòng lọng |
| Cas toàn thân (`2431c3a8`) | 8–10, bé trai, "mặt khá trung tính" ✔ | — | **1** (thân): "đầu to, chân rất mảnh và dài, dáng đứng thẳng đơ như **ma-nơ-canh**" | **dải màu da giữa áo và quần**; quần bó như quần tất lộ vùng háng; tay "như găng trắng hoặc cục tròn" |
| Đối chứng SF 104,5 s (`6e49642e`) | bé gái 8–11 | — | 0 (có chữ "đồ chơi", nhưng tả đồng hồ đeo tay) | — |
| Đối chứng SF 332 s (`2a44d73f`) | nữ 35–50 | — | 0 | — |

**Chấm theo tiêu chí của chủ dự án:**

| Tiêu chí | Kết quả | Đạt? |
|---|---|---|
| Không bị nói "lệch phong cách" | 0/2 khung hai người | ✔ (lần đầu) |
| 0 từ khoá búp bê/mặt nạ/con rối/ma-nơ-canh/tượng sáp/đồ chơi chỉ vào Cas (mặt, đầu hoặc thân) | **2/3 khung có Cas** | **✘** |
| Tuổi và giới đúng | đúng cả 5, có rào đón ở WS (mặt nhỏ) | ✔ |
| Đối chứng 0/2 | 0/2 (chữ "đồ chơi" ở SF 104,5 tả đạo cụ, không tả nhân vật) | ✔ |

**Nhiễu nền:**
- Tính cả vòng này, đối chứng bị gọi "búp bê" **1/18 lượt** (trước đó 1/16).
- Hai lần trúng ở Cas không phải nhiễu: cả hai chỉ đích danh chỗ thật trên hình (chân và quần bó, dáng đứng).

**P đọc nguyên nhân (tự xem ảnh, chưa kiểm):**
1. **Quần bó và dải da ở eo là lỗi hình thật**, thuộc gói thân:
   - quần vỏ bám sát chân MPFB;
   - khe giữa gấu áo và cạp quần lộ da.
   - Hai lỗi này dẫn thẳng tới câu "búp bê" và câu "quần tất".
2. **"Đứng thẳng đơ", "như tượng"** là tư thế layout tĩnh, chưa diễn hoạt. Đó là việc của W1/W2. Tuy vậy, tiêu chí không tách được hai loại này, nên **P vẫn chấm TRƯỢT**.
3. **Tay trắng dưới đèn lồng** (2/3 khung) là do vật liệu và ánh sáng, đã nằm trong rủi ro 5 của W4T.

## 3. C3 (W4T đo, P đối chiếu)
- **Công cụ:** công cụ của W4T tái lập **đúng từng số** của K (`k_cas_doc.json`) trên bộ mặt nạ Cas cũ.
- **Cas thân mới, 'doc' (thân/đầu):**

| Góc | 0° | 45° | −45° | 90° | −90° | 135° | −135° | 180° |
|---|---|---|---|---|---|---|---|---|
| thân | 2,406 | 2,477 | 2,472 | 2,508 | 2,507 | 2,385 | 2,393 | 3,116 |
| tay trên | 1,725 | 1,753 | 1,735 | — | 1,723 | 1,655 | 1,648 | 2,281 |
| cẳng tay | 1,242 | 1,219 | 1,272 | — | 1,323 | 1,126 | 1,263 | 1,720 |
| đùi | 1,804 | 1,853 | 1,773 | 1,407 | 1,805 | 1,704 | 1,676 | 2,351 |
| ống chân | 1,544 | 1,477 | 1,594 | 1,273 | 1,633 | 1,494 | 1,519 | 2,022 |

  - Thân cao hơn số K đo trên thân cũ từ +5,8 % đến +19,3 %.
  - Tay trên nay thấy ở 0°.
  - **Nếu dùng thân này, `c3_views` của v1.6 phải soạn lại theo bảng trên.**
- **Ida v1.5.1, 'pca', với mũ hạ 0,025 H:**
  - thân 2,271 / 2,220 / 2,213 / 2,035 / 2,070 / 2,383 / 2,350 / 2,130;
  - lệch so với `ida.json` v1.5: thân ≤ 0,14 %; mọi bộ phận ≤ 0,74 % (ống chân, số nhỏ, do làm tròn);
  - kết luận: mũ hạ không làm đổi C3, và `c3_views` của Ida giữ nguyên được.
- Luật trên layout-v16: **không chạy**, vì không khoá.

## 4. Quyết định cần chủ dự án
| | **A — Một lượt sửa thân, rồi kiểm mù lại** | **B — Nhận kèm điều kiện, khoá ngay** | **C — Không dùng thân mới** |
|---|---|---|---|
| Nội dung | W4T-2, hạn khoảng 150 nghìn token. Sửa: (1) quần rộng, có độ rủ, gấu thẳng; (2) bịt khe da ở eo (áo phủ xuống cạp); (3) nới áo, làm mượt ngực; (4) gai gáy; (5) vật liệu tay dưới đèn lồng. Sau đó kiểm mù lại 5 subagent cùng tiêu chí; đạt thì khoá v1.5.1 + v1.6 một lần | Khoá v1.5.1 + v1.6 với thân hiện tại. Ghi hai lời chê vào sai lệch chấp nhận; giao dáng cứng cho W1/W2, quần và eo cho lượt sau | Giữ thân v1.4 cho Cas; chỉ khoá v1.5.1 (Ida) |
| Ưu | Lỗi quần và eo là lỗi hình rõ, sửa bằng tham số (dựng lại khoảng 1,5 s mỗi lượt), không phải dựng lại cách làm. Giữ được thành quả "hết lệch phong cách" | Nhanh nhất để mở W1/W2 | Không tốn thêm |
| Nhược | Thêm một vòng. Câu "ma-nơ-canh" về dáng đứng có thể vẫn còn, vì khung layout chưa diễn hoạt | Khoá tài sản đang có lỗi hình thật (dải da, quần bó), dễ lộ ở mọi shot toàn thân | Quay lại lỗi "lệch phong cách" (W4N 1/1) và áo ống, vai vuông |
| Tác động | Mở W1/W2 lùi một bước nhỏ | Khoá xong thì lỗi quần và eo phải sửa bằng một lần mở khoá sau | Cổng 6 chạy với Cas kém hơn Ida |
| Rủi ro | Trượt lần nữa chỉ vì dáng tĩnh. Nếu vậy, chủ dự án cần quyết có tách lời chê về tư thế sang W1/W2 hay không (P không tự hạ tiêu chí) | Chất lượng toàn thân dưới chuẩn khi phát hành | Bị chê ở mọi khung hai người |

**Khuyến nghị của P: A.**
- Hai lời chê trúng đích đều có chỗ sửa cụ thể trong gói thân: quần bó và khe da ở eo.
- Thành quả "hết lệch phong cách" đã có. Sửa thêm một lượt rẻ hơn khoá một tài sản đang có lỗi rồi phải mở khoá lại.

## 5. Thời gian, token, hàng đợi
| Việc | Thời gian | Token | Hàng đợi |
|---|---|---|---|
| W4T (worker): đọc 16′, bước a 22′, bước b 9′, C3 và khung 13′ | 03:10–04:15 UTC | **335 066** (công cụ báo); W4T tự khai khoảng 345 nghìn, hạn khoảng 350 nghìn. Bước a khoảng 140 nghìn, vượt mức ~100 nghìn đã đặt | 24 việc, chờ 0 s, mã 0 cả 24, chạy tổng 791,5 s (8 nặng, 16 nhanh). Blender chạy ngoài hàng đợi |
| P kiểm mù: 5 subagent × 2 lượt dùng công cụ | 27–39 s mỗi subagent | 48 785 + 48 902 + 48 584 + 50 690 + 50 423 = **247 384** | 0 việc (cắt ảnh bằng PIL) |

**Làm lại (W4T):** dựng thân 6 lượt; mũ 3 lượt; C3 Cas 2 lượt.

## 6. Việc treo và ghi chú
- **Nhánh tích hợp:** `bl_head.js` trỏ `ida_bl_v151.glb`, bản **chưa khoá**. Các file v1.5 đã khoá không bị đụng. Khi khoá v1.5.1 phải ghi SHA mới.
- **s33 P0 (khớp biên 1,61, ngưỡng 1,5):** chưa có lần render lại nào, nên chưa có số mới để theo dõi.
- **Công cụ xuất `silhouettes`** đã sẵn (`export_sil.js`). Sẽ gắn vào lần render layout-v16 đầu tiên.
- **Việc W4T còn treo:**
  - gai gáy;
  - áo ôm;
  - tư thế chim bóng và leo thang chưa thử;
  - tay dài theo sheet (rủi ro 3; là **quyết định sáng tạo** của chủ dự án).

## Phụ lục — nguyên văn 5 subagent (cả đối chứng)
Giữ nguyên văn. Chỉ rút đường dẫn thư mục tạm của phiên P về tên file mù.

### W4T_hai-nguoi_s42a — file mù `2fdcbd31.jpg` — nguyên văn

> Tôi đã mở đúng một file ảnh được chỉ định. Đây là một khung hình hoạt hình 3D phong cách hoá: cảnh phố lát đá lúc chạng vạng, có hai nhân vật.
>
> **Người phụ nữ bên trái**
> - Tuổi: khoảng 65–75. Bà có tóc bạc búi sau gáy, mặt nhiều nếp nhăn và dáng hơi khom.
> - Giới tính: nữ. Bà đội mũ phớt xanh đen, mặc áo khoác dài màu xanh lục, váy tím sẫm và quàng khăn len đỏ hồng.
> - Cảm xúc: bà nhìn xuống đứa trẻ, môi mím, mày hơi chau. Người xem sẽ thấy bà nghiêm nghị, dè chừng, có phần nghi ngờ hoặc không hài lòng. Bà không có vẻ thân thiện.
>
> **Đứa trẻ ở giữa**
> - Tuổi: khoảng 7–10.
> - Giới tính: nhiều khả năng là bé trai, vì tóc ngắn, đội mũ len trắng có quả bông đỏ, mặc áo len cổ lọ đỏ cam và quần xanh đậm. Tuy vậy chi tiết này không hoàn toàn rõ.
> - Cảm xúc: bé ôm chiếc đèn lồng sáng rực trước ngực, mặt hơi ngây, lo lắng hoặc buồn nhẹ. Bé dè dặt, như đang chờ bị hỏi hay bị trách. Mắt bé nhìn lệch sang một bên chứ không nhìn thẳng vào bà.
>
> **Những điểm người xem có thể thấy lạ**
> 1. **Đèn lồng không chiếu sáng xung quanh.** Chiếc đèn trông như một khối vuông phát sáng rất mạnh, nhưng hầu như không hắt ánh sáng lên mặt đường, bức tường hay người phụ nữ. Mặt bé cũng chỉ hơi ửng. Đèn trông như một khối "tự phát sáng" dán vào cảnh, chứ không phải nguồn sáng thật.
> 2. **Nhân vật như đang lơ lửng.** Dưới chân cả hai người gần như không có bóng tiếp đất, nên trông như họ không đứng hẳn trên mặt đường.
> 3. **Cửa vòm đen kịt.** Cửa là một mảng đen phẳng, không có cánh cửa hay chiều sâu bên trong.
> 4. **Ánh sáng không khớp với thời điểm.** Bức tường sáng phẳng, gần như trắng xám, không hợp với không khí chạng vạng. Cột đèn đường (phần bóng đèn bị cắt khỏi khung) cũng không thấy phát sáng.
> 5. **Các thanh dọc đen trên tường bên trái.** Chúng mảnh, không rõ là ống nước hay cột, và trông giống lỗi đồ hoạ.
> 6. **Cái thang dựa tường không có ai dùng.** Thang hơi lạc lõng trong cảnh, dù cũng có thể là đạo cụ dụng ý, ví dụ người thắp đèn đường.
> 7. **Mặt đường lặp lại đều.** Mặt đá lát là các chấm tròn đều tăm tắp như hoa văn lặp, nhìn giống vải chấm bi hơn là đá cuội.
> 8. **Tư thế cứng.** Tay người phụ nữ buông thõng và hơi cứng. Chân bé thẳng, mỏng và quần bó sát, trông như búp bê. Cả hai đứng khá bất động, như tượng.
>
> Nhìn chung, người xem thường vẫn hiểu câu chuyện là một bà cụ nghiêm khắc đang đối diện một cậu bé cầm đèn. Nhưng các điểm 1, 2 và 4 dễ làm cảnh trông "giả", thiếu cảm giác điện ảnh.

### W4T_hai-nguoi_WS — file mù `80f51cba.jpg` — nguyên văn

> Tôi đã xem đúng một file: 80f51cba.jpg. Tôi không mở file nào khác.
>
> **Ảnh cho thấy gì:** Đây là một khung hình 3D hoạt hình. Cảnh là một con phố lát đá cuội lúc chạng vạng, trước một bức tường trắng rất lớn có cổng vòm tối. Hai nhân vật đứng cạnh một cột đèn đường kiểu cổ, có cái thang dựa vào cột.
>
> **Hai nhân vật:**
> 1. **Nhân vật bên trái:** trông như người già, khoảng 65–75 tuổi. Tóc bạc trắng, đội mũ đen, cổ quấn khăn đỏ. Người này mặc áo khoác dài màu xanh lục, bên dưới lộ gấu váy tím. Tôi đoán đây là **một bà cụ**, nhưng không chắc, vì cũng có thể là ông cụ thắp đèn đường. Bà đưa chiếc đèn lồng đang sáng về phía đứa trẻ.
> 2. **Nhân vật bên phải:** là **một đứa trẻ**, khoảng 7–10 tuổi. Em mặc áo len đỏ, quần sẫm màu, đội mũ len trắng có quả bông đỏ. Tóc ngắn nên tôi đoán là **bé trai**, nhưng không chắc. Hai tay em đưa về phía đèn lồng, như đang hơ tay cho ấm hoặc sắp đón lấy đèn.
>
> **Cảm xúc:** Mặt hai nhân vật rất nhỏ, không đọc được nét mặt. Tôi chỉ đoán được qua dáng người: cả hai bình thản, dịu dàng, thân thiện. Cảnh giống một lúc chia sẻ hơi ấm và ánh sáng: người già cho, đứa trẻ nhận, hơi rụt rè. Không thấy dấu hiệu căng thẳng hay buồn bã.
>
> **Những điều người xem có thể thấy lạ:**
> - **Tỉ lệ:** hai nhân vật quá nhỏ so với toà nhà. Cổng vòm cao gấp mấy lần người, còn bức tường trắng trống trơn chiếm gần hết khung hình. Cảnh trông trống, và mắt không biết nhìn vào đâu trước.
> - **Đèn đường không sáng:** trời đã chạng vạng và cảnh có vẻ nói về việc thắp đèn, nhưng đèn trên cột vẫn tắt. Nguồn sáng ấm duy nhất là chiếc đèn lồng.
> - **Kiến trúc khó hiểu:**
>   - Góc trên bên trái có một mái hoặc trần lơ lửng, với mấy cột hay ống đen dài chống xuống đất.
>   - Bên phải có một cột đen đứng một mình, không nối với vật gì.
>   - Một cánh cửa chớp nâu treo trên tường phía trên cột đèn mà không có cửa sổ.
> - **Vật treo ở mép trên, gần giữa:** một vòng dây treo lủng lẳng. Có người sẽ thấy nó giống thòng lọng, dễ gây cảm giác khó chịu.
> - **Thang và người chồng lên nhau:** thang dựa sát cột đèn, nằm ngay sau lưng bà cụ và gần như dính vào người bà.
> - **Ánh sáng phẳng:** bóng đổ của nhân vật rất mờ. Tường trắng gần như cháy sáng, hầu như không có chi tiết hay vết cũ, nên trông "giả", giống cảnh dựng chưa xong.
> - **Mặt đường:** đá cuội tròn, đều và lặp lại như hoa văn chấm bi. Nhìn lâu dễ thấy rối mắt, không giống đá thật.
> - **Tay đứa trẻ:** màu trắng sáng, như đeo găng hoặc đang phát sáng, nổi bật một cách hơi lạ.

### W4T_cas_toan-than_cat — file mù `2431c3a8.jpg` — nguyên văn

> Tôi đã mở đúng một file ảnh được chỉ định. Dưới đây là cảm nhận của một người xem bình thường.
>
> **Tuổi:** trông như một đứa trẻ khoảng 8–10 tuổi.
>
> **Giới tính:** trông giống bé trai (tóc nâu ngắn thò ra dưới mũ len, mặc áo len cổ lọ, quần dài). Tuy vậy, khuôn mặt khá trung tính nên có người xem cũng có thể không chắc.
>
> **Cảm xúc:** trầm lặng, hơi buồn hoặc đang mơ màng. Em nhìn lệch sang phải khỏi khung hình, miệng khép, không cười. Cảm giác như đang chờ ai đó hoặc đang ngẫm nghĩ, có chút rụt rè. Cảm xúc khá nhạt, khó đọc rõ.
>
> **Những điều người xem có thể thấy lạ:**
> 1. **Ánh sáng đèn lồng không khớp.** Đèn sáng rực, làm áo và tay đỏ cam như đang phát sáng hoặc bốc cháy. Nhưng mặt đường, bức tường và cột đèn bên cạnh gần như không nhận chút ánh sáng nào, cũng không có bóng đổ từ đèn. Trời lại còn khá sáng, nên việc thắp đèn trông không hợp lý.
> 2. **Tay trông như găng trắng hoặc cục tròn**, không rõ ngón. Hai tay cùng nắm quai ở tư thế hơi cứng và gượng.
> 3. **Vùng eo và háng trông lạ.** Có một dải màu da hoặc hồng giữa áo và quần. Quần bó sát như quần tất nên lộ hình vùng háng, trông khá kỳ.
> 4. **Tỷ lệ cơ thể:** đầu to, chân rất mảnh và dài, dáng đứng thẳng đơ như ma-nơ-canh.
> 5. **Cột đèn đường không có bóng đèn.** Phần đỉnh bị cắt khỏi khung, nên trông như một cột trụ đen trơ trọi. Cái thang dựa tường gợi ý có người sắp thắp đèn, nhưng không thấy ai.
> 6. **Ô cửa phía sau đen kịt, phẳng lì**, không có chiều sâu hay chi tiết gì, trông như một lỗ đen.
> 7. **Bàn chân bị cắt ở mép dưới khung hình.** Nhân vật đứng rất sát mép, bố cục hơi lệch.
> 8. **Mặt đường:** đá cuội phía trước có hoa văn lặp đều, trông giả. Nhân vật như hơi "dán" vào nền chứ chưa thật sự đứng trên mặt đất.
>
> Tổng thể, ảnh trông như một khung hình hoạt hình 3D phong cách hoá. Chỗ gây chú ý nhất là ánh sáng đèn lồng quá gắt mà không chiếu ra môi trường xung quanh.

### doichung_sf_104.5 — file mù `6e49642e.png` — nguyên văn

> Tôi đã mở đúng một file: 6e49642e.png. Không mở hay tìm file nào khác.
>
> Nhận xét như một người xem bình thường:
>
> - **Tuổi:** một bé gái khoảng 8–11 tuổi. Nhân vật hoạt hình 3D phong cách hoá, đầu to, mắt to.
> - **Giới tính:** nữ. Nhận ra qua tóc buộc đuôi ngựa cao, đôi khuyên tai tròn to màu hồng và dây buộc tóc màu xanh ngọc.
> - **Cảm xúc:** bối rối, lo lắng xen chút ngạc nhiên. Lông mày nhướng lên và chụm vào giữa, miệng hé tròn như vừa thốt "ơ?". Mắt nhìn chếch sang bên. Bé ôm chặt cuốn sổ lò xo vào ngực (chữ "…ology" trên bìa, có thể là "Biology"), một tư thế tự che chắn, hơi rụt rè. Nhìn chung là cảm giác không chắc chắn, hơi sợ trước một điều vừa nghe hay vừa thấy.
>
> **Những điểm người xem có thể thấy lạ:**
> 1. **Đuôi tóc** rất lớn, dựng đứng và cong như cái chổi hay đuôi thú, trông cứng và nặng hơn tóc thật. Phần gốc có sợi tóc xơ lởm chởm, trông như tách rời khỏi đầu. Đây là chỗ bắt mắt và "lạ" nhất.
> 2. Đôi khuyên tai tròn hồng rất to so với khuôn mặt. Chiếc đồng hồ đeo tay màu vàng–đỏ có hình dạng khá kỳ quặc, giống đồ chơi.
> 3. Bối cảnh là khu rừng tối, cây cổ thụ uốn cong, dưới đất có những cây nấm đỏ bóng trông như đồ nhựa, tạo cảm giác hơi huyền ảo, như trong truyện cổ tích.
> 4. Chữ trên cuốn sổ bị tay che mất một phần nên không đọc trọn được.
>
> **Hai lưu ý kỹ thuật cho dự án** (ngoài góc nhìn người xem):
> - Ảnh có kích thước 1920×804, tức khung màn ảnh rộng khoảng 2.39:1, không phải 16:9 như chuẩn của dự án.
> - Chất lượng render và vệt nén trông giống một khung hình chụp từ phim hoạt hình thương mại có sẵn. Nếu đúng vậy, ảnh chỉ nên dùng làm tham chiếu. Theo luật cứng trong CLAUDE.md, không được sao chép thiết kế nhân vật, và nếu dùng làm tham chiếu thì phải ghi vào RIGHTS.md.

### doichung_sf_332 — file mù `2a44d73f.png` — nguyên văn

> Tôi đã mở và xem đúng một file ảnh được chỉ định, không mở file nào khác.
>
> Người xem bình thường sẽ thấy như sau:
>
> - **Tuổi:** Đây là nhân vật hoạt hình 3D, không phải người thật. Trông như một người phụ nữ trưởng thành, khoảng 35 đến 50 tuổi. Cách trang điểm (phấn mắt xanh tím đậm, son viền tím, hoa tai hình học to bản) gợi phong cách thập niên 80, nên người xem dễ đoán đây là người trung niên hơn là người trẻ.
> - **Giới tính:** Nữ. Có tóc vàng rối, lông mi dài, hoa tai to, vòng cổ chuỗi hạt và son môi.
> - **Cảm xúc:** Nhân vật đang đau đớn, khó chịu hoặc sợ hãi pha lẫn tức giận. Mắt nhắm chặt, chân mày cau lại, miệng méo và nhe răng như đang rên hoặc hét. Một bàn tay xoè ra phía máy quay như để che chắn, đẩy thứ gì đó ra hoặc ra hiệu "dừng lại". Cả tư thế cho thấy cô đang né tránh hoặc bị tấn công.
>
> **Những điểm người xem có thể thấy lạ:**
> 1. Dưới hai mắt có vệt đen loang rộng, trông như mascara bị nhoè hoặc quầng thâm rất nặng. Chưa rõ đó là chủ ý (đang khóc, bị bẩn) hay là lỗi hiển thị.
> 2. Trên cằm bên trái có vài vết đen mảnh như vết nứt hay vết xước. Trên một khuôn mặt mịn kiểu hoạt hình, chúng trông như lỗi texture hoặc vết thương khó hiểu.
> 3. Mũi hồng rõ trong khi cả mặt bị ánh sáng xanh lạnh phủ lên, nên mũi trông lệch màu, như bị đỏ hoặc được tô riêng.
> 4. Bàn tay ở tiền cảnh to và hơi nhoè. Cổ tay và phần nối với cánh tay gần như biến mất trong sương mờ, nên nhìn giống bàn tay đang trôi lơ lửng.
> 5. Hoa tai hình tam giác bên trái rất to và có màu đậm, gần như tách khỏi ánh sáng của cảnh. Nó trông như một mảng đồ hoạ phẳng dán lên hơn là vật thể 3D.
> 6. Toàn cảnh tối, xanh và có sương, khiến khuôn mặt hơi xám và "chết", tạo cảm giác rợn nhẹ.
>
> Đây là ấn tượng của một người xem thông thường, không phải kết quả đo đạc hay kiểm định kỹ thuật.
