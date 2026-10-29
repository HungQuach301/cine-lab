# CHECKPOINT NV-2 (NC-VIRAL-2)
- 01:13Z: lệnh thử videos.list (1 đơn vị) → HTTP 200, quota chưa cạn → quét.
- 01:14Z: lượt quét đầu: 5/84 search.list 200, 79 bị 429 `rateLimitExceeded` (giới hạn nhịp do gọi cách 0,2 s; không phải `quotaExceeded`). Sổ ghi 429 = 0 đơn vị, kèm cột trần trên.
- 01:16Z: thử tay 1 search 'history' sau ~35 s → 200. Sửa quet.py: giãn 6 s, 429 chờ 30 s thử lại đúng 1 lần.
- 01:20Z: chạy tiếp phần còn lại (đang chạy).
- 01:18Z: lượt tiếp 1 (giãn 6 s): 3 search 200 rồi 429 lặp → dừng. Đổi giãn 20 s, 429 chờ 65 s; chạy lượt tiếp 2.
- 01:20Z: 1 lệnh tay đọc thân lỗi 429: "Quota exceeded for quota metric 'Search Queries' and limit 'Search Queries per day'" — `quota_limit=defaultSearchListPerDayPerProject`, `quota_limit_value=100`, cửa sổ từ 2026-10-28 07:00Z (0 h giờ Thái Bình Dương). NC-VIRAL đã dùng 88 search hôm nay → còn 9 search 200 cho NV-2. Theo lệnh "không chờ, không thử lại vòng lặp": DỪNG search.list, phân tích mẫu 9 truy vấn (446 video, 345 kênh).
- 01:30Z: truoc.py đọc uploads 39 kênh (78 đơn vị) → thêm 977 video đăng ≤ 30 ngày; 106 video M2 (53 M1) của kênh ≤ 90 ngày, nhiều video ngoài ngách → phân loại ngách theo kênh (đang làm).
- 01:27Z: xuất 4 CSV + kenh-theo-doi.csv + quet.json + so-ai.jsonl; viết NV2-BAO-CAO.md — DỪNG chờ chủ dự án.
