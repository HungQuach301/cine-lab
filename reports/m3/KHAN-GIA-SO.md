# KHÁN GIẢ THEO SỐ — Last Lamplighters (dự đoán G1 so với lượt xem thật)

Máy sinh: `toolkit/market/market.py own --pack ll` (Việc 0 mỗi tập tự chạy). Nguồn: viewCount công khai qua YouTube Data API videos.list (1 đơn vị/50 video) — số của **kênh mình**, commit dạng tổng hợp theo video. Lượt xem/ngày, dải dự đoán, ρ: **tự tính, không phải chỉ số YouTube**. Ảnh chụp thô: `reports/m3/khan-gia/snapshots.jsonl`.
> Dữ liệu chọn và định hướng; không quyết định nội dung hay hình. Sau 3 tập, phần nào của quy trình dữ liệu không có số đo chứng minh hiệu quả thì bỏ (CHUAN-KENH §14).

Lần đọc gần nhất: 2026-10-11T13:32+00:00 · kênh có 9 video công khai (cả Shorts) · tìm thấy 4/8 tập trong gói · dò uploads: không (quota-policy chặn playlistItems).

| Tập | Video | Phút | Dự đoán G1 (nhãn · 7 ngày · 28 ngày) | 48 giờ | 7 ngày | 28 ngày | Lượt xem/ngày (gần nhất) | Trong dải 7 ngày? |
|---|---|---|---|---|---|---|---|---|
| ep01 London Still Has 5 Lamplighters. Who Are the Last of Our Time?<br>YouTube: “History Has a Clue! Which Jobs Will AI Replace?” | [PqS6vL7yaUk](https://youtu.be/PqS6vL7yaUk) | 10.1 | chưa có (tập trước luật dự đoán) | lỡ mốc (5 ở 5 ngày) | chờ | chờ | 1.0 (5 ngày) | — |
| ep02 Automation Hurt the Phone Operators. Not the Next Generation. What About Us? | chưa thấy trên kênh | — | chưa có (tập trước luật dự đoán) | chưa có ảnh chụp | chưa có ảnh chụp | chưa có ảnh chụp | — | — |
| ep03 The ATM Didn't Kill the Bank Teller. Will AI? | chưa thấy trên kênh | — | chưa có (tập trước luật dự đoán) | chưa có ảnh chụp | chưa có ảnh chụp | chưa có ảnh chụp | — | — |
| ep04 The Typewriter Opened a Door for Millions of Women. Who Gets the Next One? | chưa thấy trên kênh | — | chưa có (tập trước luật dự đoán) | chưa có ảnh chụp | chưa có ảnh chụp | chưa có ảnh chụp | — | — |
| ep05 In 1966, Computers Couldn't Judge an Insurance Claim. Now Software Prices the Wreck | chưa thấy trên kênh | — | chưa có (tập trước luật dự đoán) | chưa có ảnh chụp | chưa có ảnh chụp | chưa có ảnh chụp | — | — |
| ep06 The Computer Replaced the Typesetter and Made the Designer. Now AI Can Draw<br>YouTube: “Will AI Replace Graphic Designers? History Has a Clue” | [nBY2-E9lUt8](https://youtu.be/nBY2-E9lUt8) | 8.6 | chưa có (tập trước luật dự đoán) | lỡ mốc (129 ở 4 ngày) | chờ | chờ | 36.4 (4 ngày) | — |
| ep07 When Computers Were People: One Word, Three Jobs<br>YouTube: “From Human Computers to AI: Three Eras of Work” | [Xg1nIQOQMOY](https://youtu.be/Xg1nIQOQMOY) | 10.3 | chưa có (tập trước luật dự đoán) | 10 (đúng mốc) | chờ | chờ | 4.9 (2 ngày) | — |
| ep08 From Headphones to Machine Drafts: How Translators' Work Changed<br>YouTube: “How Translators' Work Changed: From Paper to AI” | [hm-pBARZYag](https://youtu.be/hm-pBARZYag) | 10.1 | chưa có (tập trước luật dự đoán) | chờ | chờ | chờ | 4.0 (1 ngày) | — |

## Hiệu chỉnh nhãn cầu (sau mỗi 3 tập có nhãn)
- Kết luận hiện tại: **chưa đủ mẫu (0/3 tập có nhãn cầu + số 7 ngày đúng mốc)**.
- Luật: Spearman(nhãn cầu hiện hành Mạnh 2 · Yếu 1 · Không 0, lượt xem 7 ngày đúng mốc/nội suy) trên bội số 3 tập; ρ > 0 và trung vị nhóm Mạnh > nhóm còn lại → giữ; ngược lại → sửa công thức `demand.py` hoặc giảm trọng nhãn cầu trong chọn đề tài, ghi lý do bên dưới. Trọng số hiện TẠM, chốt sau `channel-k2/CALIBRATION.md` (12/10).
- Nhãn hồi tố 8 tập đầu: chờ `channel-k2/calib.py` (phiên k2, cần search.list) — khi có, ghi vào `reports/m3/khan-gia/predictions.json` với `"retro": true` (dùng để hiệu chỉnh, không tính là dự đoán G1).

### Lần sửa công thức
- (chưa có)

## Phương án tuỳ chọn: YouTube Analytics API (CHƯA LÀM)
- Cho CTR lượt hiển thị, thời lượng xem trung bình, giữ chân theo giây, nguồn lưu lượng (tìm kiếm/đề xuất/Shorts).
- Cần OAuth 2.0 của chủ kênh (scope `yt-analytics.readonly`), refresh token lưu ngoài repo (bí mật môi trường), proxy hiện chỉ gắn khoá Data API → phải thêm luồng OAuth. Quota riêng, không trừ vào 10 000 đơn vị Data API.
- Ưu: số giữ chân/CTR thật thay ảnh chụp Studio thủ công. Nhược: thiết lập OAuth một lần, rủi ro lộ token. Tác động: hiệu chỉnh theo giữ chân thay vì chỉ lượt xem. Chỉ làm khi chủ dự án yêu cầu (không phải việc chờ của quy trình tập).
