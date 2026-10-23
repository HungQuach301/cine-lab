# PHIẾU LOOK V2 — K2C-T4-02 London (LOOK-T4-V2, 23/10/2026)

> Không mù: chủ dự án so trước/sau. Phiên này KHÔNG chấm mù bằng AI và không chọn hộ. Tờ so: `reports/look-t4-v2/to-so-v2.jpg`; ô 1080p: `reports/look-t4-v2/khung/<hàng>-<cột>.jpg`; clip 8 s: `reports/look-t4-v2/clip/`. Số đo: báo cáo `LOOK-T4-V2-BAO-CAO.md`.

## 1. Chọn mỗi khung một cột
Cột: **look-t4** (LOOK-T4 đã chọn, A) · **v2-3d** · **v2-gemini** / **v2-openai** (chỉ 4 khung rộng; ô ghi kết quả cổng máy) · **cycles** (chỉ M2-dem).

| Hàng | Khung | Chọn cột | Ghi chú |
|---|---|---|---|
| 1 | M1-rong — 1666 toàn cảnh P1 | | |
| 2 | M1-trung — 1666 tháp St Saviour | | |
| 3 | M2-ngay — 3/9/1666 ngày khói | | |
| 4 | M2-dem — 2/9/1666 đêm lửa từ sông | | |
| 5 | M3-rong — 29/12/1940 toàn cảnh P1 | | |
| 6 | M3-trung — 1940 mái vòm từ Fleet St | | |
| 7 | M4-rong — 2026 chân trời City | | |
| 8 | M4-trung — 2026 mái vòm từ Fleet St | | |

Câu hỏi kèm (ngắn): Q1 còn "đồ chơi" ở đâu? · Q2 lửa/khói đã rõ chưa (lõi lửa, tàn lửa, chân khói hắt đỏ, khói ngày đặc)? · Q3 công trình biểu tượng đọc được chưa (đèn lồng vòm, bầu lửa Monument, tháp góc Tower — ô cắt `reports/look-t4-v2/cong-trinh/`)?

## 2. Quyết định
| # | Quyết định | Phương án | Ưu | Nhược | Tác động | Rủi ro | Khuyến nghị |
|---|---|---|---|---|---|---|---|
| V1 | Công cụ tấm nền | (a) Gemini Nano Banana 2.1 Batch · (b) OpenAI gpt-image-2.5 · (c) không dùng tấm nền ở T4 (chỉ 3D V2) · (d) chỉ dùng cho cảnh ngày hiện đại (2026), còn lại 3D | (a) rẻ (≈ $0,034/ảnh), giữ ánh sáng ảnh vào sát hơn · (b) qua cổng 1 tấm (2026 lượt 3), giữ sắc nước tốt hơn · (c) không rủi ro dữ kiện · (d) dùng đúng chỗ đã đo đạt | (a) 0/12 đạt; đổi sắc nước sang ô-liu (T9b), thêm nhà/cầu/thuyền ở đêm · (b) 1/12 đạt; đêm 1940 0/3 · (c) "đồ chơi" chỉ giảm bằng 3D · (d) phần "đồ chơi" lớn nhất (1666) chưa giải | tỷ lệ tấm nền thật ≈ 5–15 % thời lượng (không phải 35–45 %) | (a)(b) đêm/lửa: AI tự thêm cầu, đèn, thuyền — vi phạm lớp (a)/(iv) | **(d) + (b)** cho 2026 ngày; giữ thử 1666 ngày ở vòng sau khi K xong (iii) và quyết V3–V4 |
| V2 | Lửa đêm cận | (a) cách A mới (V2) · (b) Cycles GPU cho 3–4 cận đêm | (a) lõi lửa, tàn lửa, chân khói hắt đỏ, không ghép A↔B; 7,1 s/khung 1080p · (b) khói thể tích phát sáng thật hơn | (a) khói vẫn là sprite (tầng trên dạng "rèm") · (b) cảnh Cycles hiện chưa có vân/ánh trăng, mặt tiền cháy dạng khối; cần một vòng dựng cảnh Cycles | GPU ≈ $4–8 (ước) | (b) lệch chất liệu với A trong cùng cảnh (cấm ghép A↔B trong một cú máy) | **(a)** cho mọi khung; (b) chỉ khi chủ dự án thấy khói Cycles đáng một vòng dựng cảnh riêng |
| V3 | Khói bếp/vật chuyển động trên tấm nền | (a) cộng HIỆU render có/không khói lên tấm (đã làm, `-l3g`) · (b) dán nguyên điểm ảnh render (cách T6) | (a) không có "đốm trắng" (nền sương render không bị dán) | (a) khói không thuộc lớp (a) nên KHÔNG qua phép (i) 0/255 — cần K xác nhận cách đo | mọi tấm 1666 | (b) tạo "đốm" mà mô hình nhìn báo là khói bịa → (iv) trượt | **(a)**, đưa K định nghĩa phép (i)/(iv) cho lớp sống |
| V4 | Vật nhỏ lớp (a) (< 60 px nở 3 px) | (a) giữ luật · (b) K thêm khớp màu cục bộ vòng bảo vệ · (c) nhà xa ngoài hộp (bậc 5) xếp lớp (c) | (a) an toàn | (a) quầng sáng quanh thuyền/nhà xa khi tông tấm lệch render | toàn cảnh | (c) nới luật | **(b)** — đề nghị K (khiếu nại `checks-appeal.md` do P/K ghi; phiên xưởng không sửa checks/) |
| V5 | Điểm máy P1 | (a) giữ fov 50° · (b) fov 36° cùng vị trí/hướng | (b) vòm St Paul's 67 px (đạt ≥ 60), City đọc như ảnh tele, bớt "đồ chơi" | (b) mất hai mép City (Tower, Monument vốn đã ngoài khung P1) | xương sống P1 (§19 a luật 3) | đổi khung xương sống đã khoá | **(b)** — xem `khung/` hàng P1-hẹp trong báo cáo §1 |
| V6 | Sương phối cảnh khí quyển | (a) A gốc σ 1/16 km · (b) V2 σ 1/10 km | (b) chiều sâu không khí giữa máy và City | (b) giảm tương phản xa | mọi khung ngày | thấp | **(b)** |
| V7 | Mục tiêu tấm nền 35–45 % | (a) giữ mục tiêu, chờ K (iii) + V3–V4 rồi đo lại · (b) hạ mục tiêu theo số đo (≈ 5–15 %) | (a) giữ tham vọng | (a) chưa có số đo ủng hộ | ngân sách + lịch | (a) trễ animatic | **(b) cho animatic**, (a) ở vòng sau nếu K xong |

## 3. Việc chờ chủ dự án
- Chọn cột mỗi hàng (§1) + Q1–Q3; quyết V1–V7.
