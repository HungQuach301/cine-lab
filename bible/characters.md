# HỒ SƠ NHÂN VẬT — "Last Round" (v1.0 · chủ dự án đã duyệt ở Cổng 3 vòng 2 · **KHOÁ** từ Cổng 3 vòng 3; đổi phải qua chủ dự án và ghi AUTHORSHIP.md)

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
| Mũ | Mũ phớt, **không nơ** trên băng mũ | **Giữ mũ len có quả bông** | 3B, 4A |
| Mặt | Không khắc khe miệng/nếp nhăn vào hình học; khe môi, nếp nhăn, mi, đồi mồi là nét vẽ; chất da mờ (Lambert, không bóng) | như Ida; tàn nhang vẽ | C′, sửa L3 |
| Chim bóng | — | Hai cổ tay **bắt chéo**, ngón cái là đầu chim, các ngón xoè là cánh | 5B |

