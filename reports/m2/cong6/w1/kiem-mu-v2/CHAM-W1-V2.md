# Kiểm mù W1 vòng 2 — 10 dải khung + 2 đối chứng (30/09/2026)

Nguồn: `design/cong5/layout/out/layout-v21.mp4` (W1-v2 + W2 + B3–B4, có phụ đề). Công cụ `kiem_mu.py dai` (khung cách 0,5 s của một shot, lưới 4 cột, nhãn giây tương đối). Đối chứng: cùng 2 dải Sprite Fright như vòng 1 (không commit, RIGHTS REF-SF-HC).
**10 dải:** 6 dải cố định như vòng 1 (s02, s03, s05, s22, s23 hỏi hai người, s24c) và 4 dải theo **hạt giống mới `6dadcf1e2242975a`** (`kiem_mu.py chon`): s04, s08, s12, s19.
Mỗi dải do một subagent MỚI (general-purpose) chấm, câu hỏi nguyên văn như vòng 1. Nguyên văn: `NGUYEN-VAN.md`; tên mù: `map.tsv`; dải: `dai_*.jpg`. Token ≈ 535 nghìn cho 12 dải, trong hạn 600k.
Cách chấm giữ như vòng 1 (chủ dự án 30/09/2026): đạt khi ≤ 1 dải có từ khoá và không có chỗ chê cùng vị trí lặp ở ≥ 2 dải; cột HÌNH và TƯ THẾ tính riêng; nhiễu nền cộng dồn.

## 1. Đếm máy (`kiem_mu.py dem`)
| Dải | Từ khoá | Chỉ vào | Cột |
|---|---|---|---|
| **s03** (trèo, thắp L4) | "mặt nạ" | mặt Ida: "Mặt sáng trắng hồng như đeo mặt nạ hoặc kính" | **HÌNH** |
| **s05** (MCU, L1) | "con rối" | mặt Ida: "Mặt gần như không cử động… giống con rối" | **HÌNH** |
| **s22** (MCU 3/4, L2) | "búp bê" | mặt Ida: "Da mặt như sáp hay búp bê… Mắt hơi đờ, thiếu độ ẩm và ánh sống" | **HÌNH** |
| **s24c** (Cas dựa tường) | "con rối", "ma-nơ-canh" | Cas: "Thân giống một khối ống phồng, vai tròn u lên như hai cục bướu. Tay ngắn, buông thẳng và cứng… giống con rối hoặc ma-nơ-canh" | **HÌNH** (câu chê cả khối thân/vai; kèm tư thế) |
| s02, s04, s08, s12, s19, s23; doichung-104, doichung-332 | 0 | — | — |

## 2. Chấm
| Tiêu chí | Kết quả | |
|---|---|---|
| Cột HÌNH ≤ 1/10 dải | **4/10** (s03, s05, s22, s24c) | **TRƯỢT** |
| Cột TƯ THẾ ≤ 1/10 dải | 0–1/10 (s24c nếu tách phần "tay buông cứng") | đạt |
| Tổng (nếu gộp) ≤ 1/10 | 4/10 | TRƯỢT |
| Không lặp cùng vị trí ≥ 2 dải | **Mặt Ida đọc "mặt nạ / con rối / búp bê" ở 3 dải (s03, s05, s22)** — cùng vị trí như vòng 1, nay thêm s03 | **TRƯỢT** |
| **Kết luận** | | **TRƯỢT lần 2** → theo chỉ thị: **DỪNG, không tự mở vòng 3** |

So với vòng 1: HÌNH 2/10 → 4/10. Lỗi mặt Ida cận không đỡ (W1-v2 không nhận việc sửa mặt; phạm vi a–k chủ yếu là tay, thang, nhịp). s24c chuyển từ "đứng im" sang chê khối thân/vai Cas.
**Nhiễu nền:** hai dải đối chứng lần này 0 từ khoá. Cộng dồn **5/28 = 17,9 %** (vòng 1: 5/26 = 19,2 %). Để tham khảo (P không đổi ngưỡng): với nhiễu 17,9 %, xác suất một lượt 10 dải đạt ≤ 1 là **0,44**. Nhưng 4/10 vượt xa mức nhiễu (kỳ vọng ≈ 1,8), và 3 lời chê cùng chỉ vào mặt Ida, nên không thể quy cho nhiễu.

## 3. Lời chê không có từ khoá nhưng chỉ đúng chỗ thật
| Nhóm | Dải | Nguyên văn (rút gọn) |
|---|---|---|
| **Bàn tay** | **s05** | bàn tay phía trước bên phải "rất to… ngón xoè cứng như móng vuốt… như một bàn tay rời… trôi đi" (3,0–3,5 s): lỗi tay vòng 1 chưa hết ở cỡ MCU |
| Mặt | s22, s05 | s22 miệng hầu như không đổi khi nói; đường chân tóc lùi, trông như hói; s05 mặt gần như không cử động |
| Mũ / phụ kiện | s22, s24c | s22 mũ "không ổn định, lơ lửng" (2,0–2,5 s), tóc lộ trên vành; s24c **quả bông mũ Cas biến mất** sau 0,0 s (lỗi liên tục); khe hở ở cổ Cas, "đầu như đặt rời lên cổ áo" |
| Nhịp / tư thế | s24c | "gần như đứng im… không thấy thở, không chớp mắt… chết cứng" |
| Bóng lạ | s04, s03, s23 | s04 bóng hình bàn tay có vuốt (0,5 s); s03, s23 bóng tròn lớn trên tường "như cái bướu" |
| Ánh sáng (Cổng 7) | s12, s19, s23 | s12 bừng trắng ở 2,0 s; s19 cam → trắng; s23 viền vỉa hè trắng bất thường |
| Hai người (s23) | s23 | chỉ thấy **một** bóng người nhỏ; Cas không được nhận ra ở cỡ WS |
| Cỡ hình | s02, s04, s08, s12, s19, s23 | nhân vật quá nhỏ hoặc ngược sáng, không đọc được tuổi, giới, cảm xúc |
| Đọc được | s05, s22, s24c | s05 bà cụ 65–75, "hoài niệm, thân thuộc"; s22 "do dự, trầm buồn… cam chịu"; s24c cậu bé 8–11 "buồn lặng, trầm tư, như bị bỏ lại" |
