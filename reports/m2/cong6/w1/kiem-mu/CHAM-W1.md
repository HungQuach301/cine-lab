# Kiểm mù W1 — 10 dải khung + 2 đối chứng (30/09/2026)

Nguồn: `design/cong5/layout/out/layout-v20.mp4` (W1 v1 + W2 + B3–B4, có phụ đề). Công cụ `kiem_mu.py dai` (khung cách 0,5 s của một shot, lưới 4 cột, nhãn giây tương đối). Đối chứng: cùng 2 dải Sprite Fright như W2 (không commit).
**10 dải:** 6 cố định theo việc trọng tâm W1 — s02 (đi vác thang), s03 (trèo, thắp L4), s05 (L1 "Evening, old street."), s22 (L2, xoay 3/4), s23 (B2, WS cuối phố, Ida + Cas), s24c (Cas dựa tường) — và 4 theo **hạt giống `d425369e852f43fa`** trong 13 shot W1 còn lại có Ida (`kiem_mu.py chon`): s06, s07, s13, s15.
Mỗi dải một subagent MỚI (general-purpose), câu hỏi nguyên văn như W2 (+ "Nhân vật cảm thấy gì trong đoạn này?"). Nguyên văn: `NGUYEN-VAN.md`; tên mù: `map.tsv`; dải: `dai_*.jpg`. Token 43 707–46 250 mỗi dải (12 dải ≈ 536 nghìn).
Cách chấm (chủ dự án 30/09/2026): đạt khi ≤ 1 dải có từ khoá và không có chỗ chê cùng vị trí lặp ở ≥ 2 dải; cột HÌNH và TƯ THẾ tính riêng; tính nhiễu nền 4/24.

## 1. Đếm máy (`kiem_mu.py dem`)
| Dải | Từ khoá | Chỉ vào | Cột |
|---|---|---|---|
| **s05** (MCU, L1) | "con rối" | mặt Ida: "gương mặt hơi cứng, giống con rối" (kèm cổ/khăn "như lò xo") | **HÌNH** |
| **s22** (MCU 3/4, L2) | "búp bê" ×2 | mắt Ida: "mắt đen tròn, nhỏ như hạt cườm… giống mắt búp bê" (0,0; 0,5 s); tỉ lệ mặt: "búp bê sáp… uncanny valley"; da "mịn như nhựa hoặc sáp" | **HÌNH** |
| **s24c** (Cas dựa tường) | "ma-nơ-canh" | Cas: "gần như đứng im… giống tượng hay ma-nơ-canh… không thấy thở, không chớp mắt"; tay "buông thẳng… như tư thế mặc định" | **TƯ THẾ** |
| doichung-332 (Victoria) | "búp bê" | miệng nhân vật đối chứng | (đối chứng) |
| s02, s03, s06, s07, s13, s15, s23; doichung-104 | 0 | — | — |

## 2. Chấm
| Tiêu chí | Kết quả | |
|---|---|---|
| Cột HÌNH ≤ 1/10 dải | **2/10** (s05, s22) | **TRƯỢT** |
| Cột TƯ THẾ ≤ 1/10 dải | 1/10 (s24c) | đạt |
| Tổng (nếu gộp) ≤ 1/10 | 3/10 | TRƯỢT |
| Không lặp cùng vị trí ≥ 2 dải | **Mặt Ida ở cỡ MCU (s05, s22) đọc "con rối / búp bê"** — cùng vị trí (mặt Ida cận) ở 2 dải | **TRƯỢT** |
| **Kết luận** | | **TRƯỢT** → theo chỉ thị: **DỪNG**, báo cáo phần đã làm |

**Nhiễu nền:** dải Victoria trúng từ khoá lần thứ 3 liên tiếp (lần này "búp bê" về miệng). Cộng dồn **5/26 = 19,2 %** (trước 4/24 = 16,7 %). Để tham khảo (P không đổi ngưỡng): nếu nhân vật "tốt thật" và chỉ có nhiễu 16,7 %, xác suất một lần 10 dải đạt ≤ 1 là **0,48** (với 19,2 %: 0,40). Nhưng lần này lời chê chỉ đúng chỗ thật (mắt "hạt cườm" s22, mặt cứng s05) và lặp cùng vị trí, nên không thể quy cho nhiễu.

## 3. Lời chê không có từ khoá nhưng chỉ đúng chỗ thật
| Nhóm | Dải | Nguyên văn (rút gọn) |
|---|---|---|
| **Bàn tay vỡ hình** | **s05** | "bàn tay bị biến dạng nặng (0,0–2,5 s)… như cái vuốt hay cái sừng: ngón nhọn, có mảng đỏ loang, hình khối vỡ… lỗi dễ thấy nhất"; "tay đổi đột ngột (2,5 → 3,0 s)… nhảy hình"; "một cánh tay khác ở mép phải khung… mờ, màu da" |
| Xuyên hình | s06, s13 | s06 "mảng hình lưỡi liềm… như đầu hoặc tai nhân vật đâm xuyên qua mặt đồng hồ" (2,5 s); s13 "tay và thân có vẻ xuyên qua cột đèn" |
| Mặt | s22, s13, s05 | s22 "miệng hầu như không đổi hình dù đang nói"; s13 "mặt… chỉ còn một khối màu nâu" (1,0; 1,5 s); s05 "miệng méo khi nói (1,0–1,5 s)" |
| Nhịp động tác | s15, s03, s24c | s15 xuống thang "trong khoảng 1 giây… giống trượt hoặc rơi hơn là trèo từng bậc", "lơ lửng chứ không bám vào thang"; s03 "leo nhanh bất thường"; s24c đứng im, tay cứng, "vết tối lạ ở bắp tay/khuỷu tay trái" |
| Ánh sáng (Cổng 7) | s03, s07, s13, s23, s02 | tường bừng sáng quá mạnh khi đèn bật; nhân vật đen kịt cạnh đèn; s13 ánh cam → xám lạnh trong 0,5 s; s23 bóng tròn lớn trên tường |
| Đọc được | s22, s05 | s22 "Not yet… not yet" → "đang níu kéo, chưa sẵn sàng… do dự pha chút buồn và cam chịu"; s05 "yên bình, hơi buồn và hoài niệm… nụ cười thoáng" |
| Tuổi/giới | — | Ida: bà cụ ở s22 (70–80), s05 "phân vân một chút"; cỡ rộng/bóng đen (s02, s03, s07, s13, s15, s23) không đoán được hoặc đọc "đàn ông / ông già" (s03, s13) |
