# HỒ SƠ NHÂN VẬT — "Last Round" (v1.2 · chủ dự án đã duyệt ở Cổng 3 vòng 2; B1 đo lại theo hình 3D ở đợt vá A2+; **v1.2: A1 + đo thêm góc (Cổng 4 vòng v2)** · **KHOÁ**; đổi phải qua chủ dự án và ghi AUTHORSHIP.md)

Căn cứ: kịch bản chốt `scripts/last-round.fountain` (nháp 2), luật thế giới v0.3. Dùng cho rubric **C1** (người chấm phải nêu được 4 yếu tố từ phim, không đọc hồ sơ) và cho diễn xuất ở Cổng 6.

## Ida Marrow (74) — người thắp đèn cuối cùng
| Yếu tố | Nội dung | Thấy ở đâu trên phim |
|---|---|---|
| **Mong muốn** | Thắp trọn vòng đèn đêm nay đúng như 40 năm qua, kịp trước làn sóng trắng. | Cảnh 3: chạy đua, *"Not yet… not yet."* |
| **Nhu cầu thật** | Chấp nhận rằng thời của mình đã qua mà không đánh mất phần ấm của nó: trao ngọn lửa cho một người cần. | Cảnh 5: tự tay tắt ngọn cuối, trao đèn lồng cho Cas |
| **Điểm yếu** | Sống theo giờ của riêng mình và không chịu sửa: đồng hồ chậm 7 phút, bà biết mà vẫn để; một mình, không nhờ ai. | Cảnh 1 gõ kính đồng hồ; cảnh 3 lần đầu trễ |
| **Thay đổi** | Từ níu giữ ("chưa phải lúc") sang buông tay có chủ đích, và nhận giờ mới. | Cảnh 6: chỉnh đồng hồ tiến 7 phút |
| **Hành động lặp lại, kết quả ngược** | (1) Gõ kính đồng hồ (cảnh 1, không chịu giờ mới) → gập đồng hồ **không gõ** (cảnh 6, chấp nhận). (2) Hơ tay đếm ba nhịp ở đèn của mình (cảnh 1, 3) → nhìn **Cas** hơ tay đếm ba ở đèn lồng giờ là của cậu (cảnh 5). | Cảnh 1 ↔ 6; cảnh 1 ↔ 5 |
| **Cách thể hiện** | Không nói ra điều gì; chỉ qua nhịp đi, đôi tay, chiếc đồng hồ và 4 câu thoại ngắn. Thẳng lưng dù 74 tuổi: nghề này giữ bà đứng thẳng. | Cả phim |

## Cas (Casimir, 10) — cậu bé làm chim bóng
| Yếu tố | Nội dung | Thấy ở đâu trên phim |
|---|---|---|
| **Mong muốn** | Giữ con chim bóng của mình, trò chơi duy nhất cậu có vào ban đêm. | Cảnh 4: vỗ tay mãi vào bức tường trắng |
| **Nhu cầu thật** | Được một người lớn nhìn thấy và trao cho mình điều gì đó. Áo len quá khổ của người lớn, một mình ngoài phố lúc tối: không ai chăm cậu. | Cảnh 4–5 |
| **Điểm yếu** | Rụt rè, không dám xin; chỉ đứng nhìn chiếc đèn lồng. | Cảnh 4: *"He looks at the lantern. He does not ask."* |
| **Thay đổi** | Từ mất và lặng lẽ nhìn sang nhận lấy, rồi tự làm nghi thức của người trao: người nhận thành người giữ lửa. | Cảnh 5: tự hơ tay đếm ba; cảnh 6: chim lớn bay trong phòng |
| **Hành động lặp lại, kết quả ngược** | Chim bóng tan dưới đèn điện (cảnh 4, mất) → chim bóng lớn bay trên tường phòng mình (cảnh 6, được). | Cảnh 4 ↔ 6 |
| **Cách thể hiện** | Không lời (quyết định Cổng 1). Chỉ tay, hướng nhìn, một tiếng cười khẽ (SFX có giấy phép). | Cả phim |

## Quan hệ
Không có câu thoại nào giữa hai người ngoài *"Go on, then."*. Quan hệ được kể bằng khoảng cách: xa (cảnh 4, Ida đứng nhìn, không gọi) → gần (cảnh 5, hai cái bóng cạnh nhau) → trao (đèn lồng) → tách ra nhưng nối bằng ánh sáng (cảnh 6, ô cửa sáng trên con ngõ nơi Ida đứng).

## Thiết kế và tỷ lệ đã duyệt (Cổng 3 vòng 2, khoá vòng 3)
Nguồn số: `design/cong3/model-sheet/ida.json`, `cas.json` (trường `scale`, `bun_scale`, `scarf`, `skirt`, `hair`, `face`). H = chiều dài đầu.

| Hạng mục | Ida | Cas | Quyết định |
|---|---|---|---|
| Cách dựng | Thân 3D, tay 3D, **mặt vẽ tay trên texture phủ đầu 3D** | như Ida | C′ |
| Bàn tay | **1,15×** số đo gốc | **1,30×** (trần cho phép) | 2A |
| Búi tóc | **1,3×** (đường kính hiệu dụng 0,546 H) | — | 2A |
| Váy | Váy dài #4a3a44 lộ dưới vạt áo, gấu cách đất 0,42 H; tất tối #3a3235 | — | 3B |
| Khăn | Khăn len #8e5c5a, một đuôi buông trước ngực | — | 3B |
| Tóc | Búi sau gáy dưới vành mũ | Tóc #5a4034 lộ ở gáy và dưới vành mũ (để không đọc thành búi tóc bé gái) | 3B |
| Mũ | Mũ phớt, **không nơ** trên băng mũ; **v1.2:** màu gốc trung tính #2b2a2a (albedo cố định, không chỉnh theo shot) | **Giữ mũ len có quả bông** | 3B, 4A; v1.2 |
| Mặt nữ tính (v1.2) | **A1:** 3 lọn tóc bạc mềm ở mỗi thái dương + 2 lọn ở gáy; hoa tai nhỏ bắt sáng (nụ + giọt, vàng cũ #c9a466). Cổ áo đứng dựng cao tới cằm (khớp hình sheet; bỏ cổ trần dài) | — | A1 (Cổng 4) |
| Mắt (v1.2) | Tròng nâu #5a4636, lòng trắng ngà tối #7a6e66; không tự phát sáng | như cũ | Cổng 4 v2 |
| Mặt | Không khắc khe miệng/nếp nhăn vào hình học; khe môi, nếp nhăn, mi, đồi mồi là nét vẽ; chất da mờ (Lambert, không bóng) | như Ida; tàn nhang vẽ | C′, sửa L3 |
| Chim bóng | — | Hai cổ tay **bắt chéo**, ngón cái là đầu chim, các ngón xoè là cánh | 5B |

## Tỷ lệ đo được trên hình 3D đã duyệt (B1, đợt vá A2+ — dùng cho luật C3)
Cách đo giống checks C3 (RUN.md 3.6): mặt nạ bộ phận **nhìn thấy**, render thật ở 4×, tư thế đứng thẳng (turnaround), máy trực giao; độ dài = bề dài theo trục chính PCA + 1 px; tỷ lệ = độ dài bộ phận / độ dài đầu (đầu = phần đầu nhìn thấy dưới mũ). Số ghi vào sheet = **góc chính diện 0°**. Khung xương dựng hình (`parts{}` trong sheet) không đổi. Số đo nguồn: `model-sheet/*.json` → `c3_views`.

**v1.2 (Q-C3v A):** đo lại sau A1 và cổ áo cao; thêm −45°, ±135°, 180°. Lưới Cas không đổi nên số Cas 0°/45°/±90° giữ nguyên. Ida 0°: cổ áo che cằm nên đầu nhìn thấy ngắn hơn, tỷ lệ 0° cao hơn v1.1 khoảng 3%.

| Bộ phận | Ida 0° (sheet) | 45° | −45° | 90° | −90° | 135° | −135° | 180° |
|---|---|---|---|---|---|---|---|---|
| thân | **2,667** | 2,314 | 2,315 | 2,137 | 2,153 | 2,386 | 2,354 | 2,510 |
| cánh tay trên | **1,600** | 1,483 | 1,466 | — | 1,408 | 1,465 | 1,455 | 1,578 |
| cẳng tay | **0,994** | 0,914 | 1,299¹ | — | 1,009 | 0,825 | 1,087 | 1,193 |
| cẳng chân (bỏ) | 0,293 | 0,282 | 0,282 | — | 0,275 | 0,272 | 0,270 | 0,284 |

| Bộ phận | Cas 0° (sheet) | 45° | −45° | 90° | −90° | 135° | −135° | 180° |
|---|---|---|---|---|---|---|---|---|
| thân | **1,669** | 1,707 | 1,708 | 1,661 | 1,654 | 1,708 | 1,704 | 1,656 |
| cánh tay trên (bỏ) | 0,586 | 0,211 | 0,613 | — | 0,630 | 0,574 | 0,635 | 0,630 |
| cẳng tay | **0,945** | 0,944 | 0,929 | —² | 0,937 | 0,942 | 0,932 | 0,944 |
| đùi | **1,191** | 1,176 | 1,159 | — | 1,076³ | 1,039 | 1,189 | 1,082 |
| cẳng chân | **1,132** | 1,116 | 1,115 | — | 1,134 | 1,126 | 1,122 | 1,105 |

¹ Tay phải cầm đèn đưa ra trước trong tư thế turnaround. ² Đo được 0,05 = mẩu cổ tay ló sau thân; ghi null. ³ **Q-C3w:** đùi Cas 1,19 (−60°), 1,211 (−75°), 1,068 (−80°), 1,076 (−90°). Bậc −13% giữa −75° và −80° là do **cánh tay buông che mép trước đùi**, không phải gấu áo len; số −90° đúng. Ở dáng đi (walk_cas, −71…−80°) tay vung khỏi đùi nên đùi dài hơn 9–11%. Che phụ thuộc tư thế: đã biết, không đổi số.

Bộ phận bị che theo thiết kế nên không đo: Ida — đùi và cẳng chân (váy dài + áo khoác); Cas — cánh tay trên (áo len rộng che, biến thiên 0,21–0,63 theo góc).
**Giới hạn đã biết:** tỷ lệ phụ thuộc góc nhìn (thân Ida 2,15–2,58), nên C3 ở shot nghiêng/sau lưng có thể lệch > 3% dù nhân vật đúng thiết kế (RULES.md giới hạn 4: đo 2D).

