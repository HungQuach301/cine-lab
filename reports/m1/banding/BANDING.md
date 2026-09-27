# M1 bước 3 — Sửa banding (luật G3) cho cảnh mẫu three.js

Phiên P, 27/09/2026. Mọi số dưới đây là đo thật. Không sửa `checks/`, không hạ ngưỡng.

## Kết quả

| | M0 `reports/m0/media/b-3d-mb8.mp4` | **M1 `b-3d-mb8-dither.mp4`** |
|---|---|---|
| G3 diện tích banding, khung tệ nhất (ngưỡng ≤ 0,2%) | 18,45% (trung bình 16,65%) — TRƯỢT | **0,0829%** (trung bình 0,0041%) — **ĐẠT** |
| N1 24 fps CFR | ĐẠT | **ĐẠT** |
| N2 BT.709 + dải limited (luma ngoài dải ≤ 0,5%) | ĐẠT | **ĐẠT** (0,3234%) |
| Bitrate hình | 1,29 Mbps (CRF 16) | **16,15 Mbps** (ABR 16 M, maxrate 24 M) |
| Tốc độ render (8 mẫu motion blur) | 45,31 s/giây phim | **45,64 s/giây phim** |
| RAM đỉnh | 1,45 GB | 1,62 GB |

Báo cáo máy: `reports/checks/b-3d-mb8-dither/`. Báo cáo lỗi gốc: `reports/m1/banding/baseline/`. Chỉ số trong vùng ±5% quanh ngưỡng: **không có** (máy báo "Không có").

Ảnh so sánh khung 216, vùng mặt đường tối: `compare-f216.png` (trên: gốc; dưới: tăng sáng 4× chỉ để minh hoạ; trái M0, phải M1).

## Nguyên nhân banding ở M0 (đọc từ mã, rồi kiểm bằng đo)
1. Tám mẫu motion blur được cộng dồn qua canvas 2D **8 bit** (`globalAlpha = 1/(s+1)`), làm tròn ở mỗi lần cộng.
2. ACES → sRGB xuất thẳng 8 bit, **không dither**.
3. x264 CRF 16 chỉ ra 1,29 Mbps cho cảnh tối, gần như phẳng.

## Cách sửa (`scene3d_dither.js`, `render_chromium.js`)
- Mỗi mẫu render vào render target **Float32** tuyến tính rồi cộng dồn bằng float.
- Khử răng cưa bằng **jitter dưới điểm ảnh** theo dãy R2 cho từng mẫu, thay MSAA.
- Pass cuối: ACES Filmic → sRGB → **grain đơn sắc cố định** (σ 1,5 mã, hạt 1,6 px, toe 1 mã) + **dither TPDF ±1 LSB** → 8 bit.
- Mã hoá: `vflip,scale=out_color_matrix=bt709:out_range=tv:flags=accurate_rnd+full_chroma_int` → x264 High, `preset medium`, `tune grain`, `-b:v 16M -maxrate 24M -bufsize 32M -g 48`, đủ nhãn BT.709/tv.
- Tham số grain nằm trong hằng `GRAIN`; mẫu nhiễu băm theo (x, y, số khung) nên render tất định.

## Các bước thử (số đo thật, theo thứ tự)
| # | Thay đổi | Kết quả | Kết luận |
|---|---|---|---|
| 1 | HalfFloat + MSAA 4, grain σ 1,5 từng điểm ảnh, PNG | 111,8 s/s (thử 1 s) | Quá ngưỡng 60; MSAA trên HalfFloat rất đắt trên SwiftShader |
| 2 | Bỏ MSAA, thay jitter R2 | 61–63 s/s | Còn trên ngưỡng |
| 3 | Rút hash, preset medium, bóng đổ cập nhật 1 lần/khung, RGB24 thô | 57,7 s/s | Trong vùng ±5% quanh 60, chưa đủ biên |
| 4 | Float32 thay HalfFloat | **46,3 s/s** | Đủ biên |
| 5 | Kiểm 1 s | G3 0% nhưng **N2 trượt 0,83%** | Grain cắt ở 0, x264 đẩy luma xuống 15 |
| 6 | Toe 8/255 cho cả grain và dither | N2 ĐẠT, **G3 trượt 0,77%** | Đen sâu không nhiễu → bậc thang 16–19 |
| 7 | Toe 3/255, cả 10 s | N2 0,139%, **G3 trượt 0,81%** (khung 48) | Như trên |
| 8 | Toe tách: grain 6, dither 1 | G3 0,34% (đoạn 36–72) | Chưa đủ |
| 9 | Mã hoá **không mất dữ liệu** cùng nguồn | **G3 0,0032%, N2 0%** | **Nguồn sạch; x264 xoá dither ±1 mã ở vùng tối** |
| 10 | 8 cấu hình x264 (deadzone 0, AQ 2/3, aq-strength 1,2–1,5, tune film, 20–24 Mbps, CRF 12/14) | G3 0,21–0,83%, không đều theo bitrate | Chỉnh bộ mã hoá không giải quyết được |
| 11 | Grain toe 2 (hạt 1 px), cả 10 s | G3 0,29–0,32%, N2 0,156% | Chưa đủ |
| 12 | **Hạt grain 1,6 px + toe 1** | G3 0,0153%, N2 0,322% (mã hoá từ file thô) | Đạt |
| 13 | **Render chính thức qua đường ống thật** | **G3 0,0829%, N2 0,3234%, 45,64 s/s** | **Đạt** |

## Rủi ro và việc còn lại (nêu thẳng)
1. **G3 dao động theo lần mã hoá.** Cùng tham số nguồn, G3 là 0,0153% khi mã hoá từ file thô và 0,0829% qua đường ống chính thức (x264 đa luồng không tất định). Biên còn 59%. Khi làm shot thật, phải chạy G3 trên **từng** file giao nộp.
2. **N2 dùng 65% biên** (0,32/0,5). Grain ở đen sâu đổi lấy việc không bậc thang. Cảnh tối hơn cảnh mẫu có thể cần chỉnh toe; phải đo lại theo shot.
3. **Bóng đổ cập nhật 1 lần/khung** (tư thế giữa màn trập): bóng không có motion blur. Nhân vật dịch ~6 cm trong 1/48 s nên không thấy được ở cảnh này. Với chuyển động nhanh cần xem lại.
4. **Grain là quyết định thẩm mỹ.** σ 1,5 mã, hạt 1,6 px nhìn thấy được ở vùng tối (ảnh so sánh). Chủ dự án duyệt mức grain ở Cổng 3 (style frame). Mức grain nhỏ nhất vẫn giữ G3 đạt đã có trong bảng trên.
5. **Lớp 2D (M0: 1,8%) chưa sửa** trong bước này. Cùng pass cuối (grain + dither) sẽ áp cho lớp 2D khi ghép 2 lớp ở M2.
6. `peak_rss` 1,62 GB, `gl.finish()` không chặn trên SwiftShader: thời gian dựng hình nằm trong cột `png_encode_s` của file `.render.json` (tên cột giữ từ M0).
