# Lượt sửa sau nháp 960×540 (một lượt, theo lệnh 11/10)

| # | Lỗi (soi khung nháp) | Sửa | Trạng thái |
|---|---|---|---|
| 1 | Máy quay `i_hist` trôi phải, mất cọc 1900; nửa trên khung trống | đổi máy quay (giữ 3 cọc, khung chặt) | đã sửa đặc tả |
| 2 | Thẻ cột: chữ giá trị đè đầu cột cam (tương phản Q5); nửa dưới thẻ trống | chữ vào trong cột (màu mực) khi không đủ chỗ; căn giữa dọc; cột 90 px, chữ 52 px | đã sửa `k2.js` |
| 3 | Thẻ mốc thời gian: chữ các mốc chồng nhau | chia cột đều, căn trái trong cột | đã sửa |
| 4 | Thẻ danh sách: ô vuông trống ở mục không đánh dấu; nội dung dồn lên | vạch thay ô; khối căn giữa dọc | đã sửa |
| 5 | Thẻ số chờ số neo theo lời (vd €82.32) trống ~7 s (Q11) | dòng đơn vị hiện khi vào thẻ | đã sửa |
| 6 | Thẻ luồng CBAM: ô 4 tràn mép dưới; dòng "as of" đè mép trên thẻ | ô cao hơn, bắt đầu sớm hơn; "as of" lên mép khung khi có thẻ | đã sửa |
| 7 | Vân vật liệu tối gần đen (tôn, gạch, xe tải, chốt hải quan): màu canvas bị chuyển sRGB→tuyến tính hai lần | dùng `getHexString()` (sRGB) khi vẽ canvas | đã sửa `k2g01.js` — cảnh nháp dựng sau 15:40 đã mang bản sửa, 1080p dựng lại toàn bộ |
| 8 | Chú thích dài bị cắt sau 2 dòng | cho tối đa 3 dòng | đã sửa |
| 9 | Thẻ kết: khoảng dòng sai | cộng dồn theo cỡ chữ | đã sửa |
| 10 | `v_end`: cây đen lớn chắn tiền cảnh | máy quay cao hơn | đã sửa đặc tả |
| 11 | Tựa "The toll" trên mặt tường tôn trống (`m_stack` máy quay đứng khuất) | máy quay ngoài nhà xưởng, nhìn ống khói | đã sửa đặc tả |
| 12 | Nền thẻ phát cảnh 3D chậm (speed 0,35) → giữ khung 2–3 lần (judder Q1) | hoà 2 khung kề theo phần lẻ thời gian (render.js nạp cả i, i+1) | đã sửa |
| 13 | Short 9:16: `s_ingots` hai cọc ở mép khung; `s_port` xe tải chắn sát ống kính | xếp cọc theo chiều sâu (dọc khung); lùi máy quay cổng | đã sửa đặc tả |
| 14 | 01: thẻ "ba tầng" chỉ kịp hiện tầng 1 rồi cắt | hiện đủ 3 tầng ngay đầu thẻ, nổi tầng 1 (đang kể) | đã sửa |
| 15 | 01 thẻ "con đường", 03 thẻ trích: trống 4–6 s trước nội dung (Q11) | nút đường hiện từ đầu câu "Under all three"; câu trích hiện từ "Writing about…" | đã sửa |
| 16 | 02 `v_works`: máy quay sát tường nhà xưởng, tường che gần hết khung (kính mái nhìn nghiêng thành tam giác cam) | máy quay trên mặt sông nhìn lò cao | đã sửa đặc tả |
| 17 | 04 lò cốc: khói trắng mờ to sát ống kính; `v_coke2` và Homestead (`v_night`) tối gần đen | máy quay lùi/cao; khói lò cốc nhẹ hơn; `v_coke2` chạng vạng; Homestead giờ xanh (đổ bộ lúc rạng sáng) | đã sửa |
| 18 | 07: thẻ Section 232 trống ~12 s; thẻ công suất chỉ có tựa ~6 s | mục đầu hiện từ "Section 232"; nhãn cột hiện cùng thẻ | đã sửa |
| 19 | 07: dòng nguồn 5 tuyên bố tràn mép phải (Q22) | nguồn dài tự xuống dòng | đã sửa |
| 20 | 09: danh sách golden share đè dòng nguồn; thẻ trích AP trống ~6 s · 11: thẻ Stegra trống ~12 s, thẻ hai khẳng định ~3 s | chữ danh sách 35 px, giãn 40; câu trích hiện từ 'According'; mục đầu từ 'most recent'; cột 1 từ 'You'll hear' | đã sửa |
| 21 | 13: thẻ 'Our answer' chỉ có tựa ~4,6 s | mục đầu hiện từ 'Our answer' | đã sửa |
| 22 | QC nháp Q1/Q3 (Short): thẻ kết đứng yên, nền phẳng | nền lưới trôi chậm + chữ phóng nhẹ | đã sửa |
| 23 | QC nháp Q5: khung cuối đoạn đang tối dần bị tính tương phản | không ghi chữ khi lớp tối > 20 % | đã sửa |
| 24 | QC nháp Q7: shot có số thiếu nhãn ACTUAL | nhãn loại số tự động cạnh dòng nguồn/góc thẻ | đã sửa |
| 25 | QC nháp Q21: 4 chú thích có năm/số chưa khai nguồn | thêm nguồn; câu "our read" khai src: [] | đã sửa |
| 26 | QC nháp Q23 (lời khoá so USGS 1950 với worldsteel 2025) | không đổi lời khoá; thẻ ghi rõ "USGS, raw steel" / "worldsteel, crude steel"; nêu trong báo cáo | ghi nhận |
