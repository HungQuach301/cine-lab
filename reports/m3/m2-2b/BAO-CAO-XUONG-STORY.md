# Animatic v3 · xưởng STORY và STORY-2 — báo cáo (P lưu từ lời trả về, 01/10/2026)

## STORY (gói 1)
- Token harness 170,6 nghìn so với hạn 180 nghìn. Gói hết hạn trước khi render đoạn 01/04/19.
- **Tấm nền br10** (180 khung, 0 khung trùng): khối văn phòng mới, ba khối ở ba độ sâu.
  - Mật độ sáng theo tầng 0,08–0,9; khoảng 7 % ô ấm; khoảng 4,5 % ô bật/tắt chậm, chu kỳ 5–11 s.
  - Sương FogExp2(0,008): mặt tiền ≈ 4 %, khối A ≈ 26 %, khối B ≈ 53 %, khối C ≈ 81 %.
  - Xưởng sửa luôn mã `design/m3/lat-cat/story_shot.js`. Lát cắt đã duyệt không render lại nên tệp lát cắt không đổi.
- **Tấm nền s03** (288 khung): người thắp đèn vô danh (mũ chóp, áo dài) dựng trên rig Ida.
  - **Sửa bóng s03/s05:** viền sáng 2,75 px quanh toàn bộ bóng, sáng gấp đôi nền (1 stop); tham số `b3.rimAll`, `b3.rimPx`.

## STORY-2
- Nhánh `ep01-story`; commit xưởng `683527d`; bản sửa của P `bada6bc`.
- Token harness 196,8 nghìn so với hạn 180 nghìn (+9 %).

| Đoạn | Khung | Judder (P đo lại) | Giờ máy |
|---|---|---|---|
| 01 | 992 | 0 / 0 | ≈ 1,41 h |
| 04 | 378 | 0 / 0 | ≈ 0,65 h |
| 19 | 950 | 0 / 0 | ≈ 1,90 h |

- **Giây render/khung:**
  - có nhân vật: 1 062 khung, trung bình 9,34 s (5,6–16,4 s);
  - không nhân vật: 1 258 khung, trung bình 3,46 s.
- **Thẻ kết:**
  - DejaVu Serif Bold 80 px;
  - dòng dài nhất bằng 69,9 % chiều rộng khung, nằm trong vùng an toàn 90 %;
  - tương phản 14,0:1 (dòng lớn) và 8,78:1 (dòng nhỏ).
- **Ba rủi ro:**
  - (a) Ở e19d có hai đốm hổ phách: hai ngọn đèn đặt trên mặt phố giữa khung; ô cửa nhà Cas đổi màu lạnh; quầng đèn tắt depthTest để không bị mái nhà che.
  - (b) Đoạn 19 và e01n4 đổi sang chạng vạng muộn bằng `duskify`.
  - (c) Cas đứng giữ chân thang, IK hai tay lệch 4,4 cm và 0 cm.
- **Đĩa:** ghi clip shot thẳng ra H.264, không qua PNG. Đĩa trống thấp nhất theo khối: 04 là 9,7 GB, 19 là 12 GB, 01 là 14 GB.

### Shot đã thay (theo giới hạn của chủ dự án; giữ đủ e01b, e01c, e19a)
| Shot gốc → shot thay | Khung | Lý do | Giờ máy tiết kiệm |
|---|---|---|---|
| e01e (bọc s05) → e01n2 (cận trung ngọn đèn vừa thắp) | 168 | Khung gốc tối, tường đen chiếm tiền cảnh; đèn vừa thắp hợp câu "But her job was real…" | −206 s (tốn hơn) |
| e01f (bọc s24, Cas ở xa) → e01n3 (hàng đèn khí cạnh cột điện chưa bật) | 120 | Nguồn s24 là đêm có sao, lệch với chạng vạng của đoạn 01; trùng với e19b | +939 s |
| e01g (bọc s43, thành phố trắng điện) → e01n4 (phố chưa thắp) | 128 | Trái với chạng vạng đầu tập; trùng ảnh kết e19d | −256 s (e01g vốn không có nhân vật) |

- Ròng cả ba shot tiết kiệm ≈ +477 s (≈ 8 phút máy). Lý do chính của các lần thay là liền mạch hình. Khung có nhân vật đo thật chỉ 6–7 s/khung, thấp hơn mức ≈ 14 s đã ước.
- Thời lượng STORY không đổi.

### Lỗi P phát hiện khi xem khung và đã sửa
- **Hiện tượng:** với shot dùng máy gốc (`cam: null`), độ "trôi máy" cộng dồn qua từng khung. Máy tĩnh của các shot nguồn s02, s09w, s09, s19 vì thế trôi xa dần:
  - e01b (đoạn 01, khoảng 7,7–9,9 s): máy xuyên vào khối nhà, khung có mảng đen và nền trắng;
  - e04c (đoạn 04, khoảng 8,5–12 s): đồng hồ quảng trường trôi ra khỏi khung, chỉ còn trời trống;
  - e04d (khoảng 14 s): máy xuyên tường;
  - e04b: đồng hồ bỏ túi lệch dần.
- Judder vẫn bằng 0 vì khung vẫn thay đổi liên tục, nên công cụ đo không bắt được lỗi này.
- **Sửa:** trôi máy tính từ vị trí gốc của từng khung (commit `bada6bc`); render lại e01b, e04b, e04c, e04d; ghép lại đoạn 01 và 04.
- Đoạn 19 không dính lỗi (shot nguồn s23/s24 tự đặt lại máy mỗi khung), nên giữ nguyên.

### Chờ chủ dự án duyệt
1. Ba shot thay ở đoạn 01.
2. Cách làm chạng vạng muộn.
3. Cách đặt hai đốm hổ phách ở e19d.
4. Tư thế Cas giữ thang.
5. Thẻ kết.
6. Ghi clip shot thẳng ra H.264, không qua PNG (lệch quy trình CHUAN-KENH §6.2 theo hướng tiết kiệm đĩa hơn).
7. Ở e19a (shot bắt buộc (c)), Ida thắp ngọn thứ hai ở cỡ xa, hình người nhỏ trên khung.
