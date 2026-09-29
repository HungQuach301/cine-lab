# Kiểm mù W2 vòng 1 — 10 dải khung + 2 đối chứng (29/09/2026)

Nguồn: `design/cong5/layout/out/layout-v17.mp4` (có phụ đề). Mỗi dải = các khung cách nhau 0,5 s của **một shot**, lưới 4 cột, nhãn giây tương đối (`scripts/p/kiem_mu.py dai`).
Đối chứng: Sprite Fright, mỗi dải trọn một shot (Ellie 104,0–106,3 s; Victoria 330,9–332,08 s). Dải đối chứng KHÔNG commit (RIGHTS REF-SF-HC).
3 dải chọn theo hạt giống **`a443c83796f0d4e6`** trong 20 shot W2 có nhân vật (trừ các dải chỉ định) → s32, s34, s42b.
Mỗi dải một subagent MỚI (general-purpose), prompt nguyên văn: câu hỏi cũ + " Nhân vật cảm thấy gì trong đoạn này?". Nguyên văn: `NGUYEN-VAN.md`; bảng tên mù: `map.tsv`; dải: `dai_*.jpg`.
Token subagent: 44 681–46 441 mỗi dải (12 dải ≈ 548 nghìn).

## 1. Đếm máy (`kiem_mu.py dem`, danh sách từ khoá cố định)
| Dải | Từ khoá trúng | Chỉ vào | Cột |
|---|---|---|---|
| s32 (hai người, WS tường chim) | "mặt nạ" ×2 | mặt Ida ("mặt rất nhỏ, xám… như đeo kính hoặc mặt nạ", "xám và cứng như mặt nạ") | **HÌNH** |
| s34 (hai người, hốc vòm) | "mặt nạ" ×2 | mặt Ida ("mảng trắng không có chi tiết, dễ bị đọc thành mặt nạ") | **HÌNH** |
| doichung-332 (Victoria) | "ma-nơ-canh" | bàn tay nhân vật đối chứng | HÌNH |
| 8 dải còn lại + doichung-104 | 0 | — | — |

## 2. Chấm theo AUTHORSHIP "Cổng 6 — diễn hoạt"
| Tiêu chí | Kết quả | |
|---|---|---|
| ≤ 1/10 dải có từ khoá (HÌNH + TƯ THẾ) | **2/10** (s32, s34) | **TRƯỢT** |
| Không có lời chê cùng một chỗ lặp ≥ 2 dải | **"Mặt Ida ở cỡ cảnh rộng đọc thành mặt nạ / mảng trắng xám"**: s32 và s34 | **TRƯỢT** |
| Dải s37 kể ra cả "cười" lẫn "buồn/tiếc" | Nhịp 1 (s37, "That's the last one, then."): "buồn lặng lẽ, cam chịu… luyến tiếc", nhưng "**không khóc cũng không cười**", "mặt quá tĩnh" → **thiếu "cười"**. Nhịp 2 (s37b, "Goodnight, old street."): "khép lại thành một **nụ cười mỉm** kín", "luyến tiếc", "buồn chia tay" → **đủ cả hai** | **TRƯỢT nhịp 1**, đạt nhịp 2 |
| **Kết luận** | | **TRƯỢT** |

**Nhiễu nền đối chứng cập nhật:** lần này 1/2 lượt đối chứng có từ khoá chỉ vào nhân vật; cộng dồn **3/22 = 13,6 %** (trước 2/20 = 10 %). Theo cách chấm 10 dải, ngưỡng vẫn là ≤ 1/10 (chủ dự án chốt); P không tự đổi.

## 3. Lời chê không có từ khoá trong danh sách nhưng chỉ đúng chỗ thật (phải sửa, theo AUTHORSHIP)
| Nhóm | Dải | Nguyên văn (rút gọn) |
|---|---|---|
| Mặt tĩnh, không diễn | s37, s39, s41, s42a, s34 | s37 "mặt quá tĩnh… giống tượng hay **rối stop-motion**"; s39 "miệng hầu như không động, khó tin là bà đang nói"; s41 "gần như bất động, giống **hình nộm**"; s42a "gần như đứng im… giống ảnh tĩnh hay **tượng**" |
| Bàn tay | s45, s37, s37b, s39, s40 | s45 "to, cứng, ngón xoắn và xuyên vào nhau… giống móng vuốt"; s39 "như **nhựa hoặc sáp**"; s37/s37b "hình dạng bàn tay rối, khó nhận ra / nhoè như một khối lạ"; s40 "tay và chốt như dính vào nhau" |
| Da / vật liệu | s37b | "da mặt sần, lấm tấm như hạt nhiễu hoặc như **đất sét thô**" |
| Tóc | s39, s40 | "tóc trông như một chiếc mũ hay miếng bọc dán lên đầu"; "búi tóc như cuộn len trắng" (tài sản khoá; ghi) |
| Chuyển động giật / nhảy | s45, s42b, s37b | s45 quay đầu ~90° trong 0,5 s; s42b Cas "dịch chuyển tức thời" 0,5 → 1,0 s và "gần như trong suốt" ở 1,5 s; s37b máy/nhân vật "giật" ở 2,0 s |
| Ánh sáng (phần lớn Cổng 7) | s40, s41, s42a, s42b, s32, s34 | s40 "đèn tắt mà cảnh không tối đi"; s41 đèn lồng "gần như biến mất" ở 1,0 s; s42a đèn lồng không hắt sáng ra quanh; s42b vòng tròn tối đồng tâm trên tường; s32/s34 bóng không khớp người |
| Đọc được đúng ý | s39, s37b, s40, s42a, s45 | s39 "buồn dịu… buông bỏ"; s37b "hoài niệm, lưu luyến… dịu dàng"; s40 "mệt mỏi, trầm buồn, cam chịu"; s42a "trìu mến pha buồn" (bà cúi nhìn đứa trẻ — nhưng "không chắc nhìn vào bé") |

Tuổi/giới: Ida đọc là phụ nữ lớn tuổi 50–80 tuổi ở 6/6 dải thấy mặt (s37, s37b, s39, s40, s42a, s45); ở WS/hốc vòm (s32, s34, s41) mặt quá nhỏ → đọc thành "ông / đàn ông lớn tuổi" 3/3. Cas: đứa trẻ 6–10 tuổi, giới không rõ (nghiêng bé trai).
