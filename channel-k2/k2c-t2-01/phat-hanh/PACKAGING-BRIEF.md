# PACKAGING-BRIEF — K2C-T2-01 · Why America Builds So Few Ships (It's Not Just Wages)

Bản gói phát hành (G2, 16/10/2026), rút từ `../PACKAGING-BRIEF.md` (Mốc A, vai Đóng gói) và cập nhật theo quyết định của chủ dự án. Nhà máy **không** làm thumbnail hoàn chỉnh: chủ dự án tự tạo thumbnail theo brief này, bật **YouTube Test & Compare**, rồi ghi CTR của bản thắng vào `channel-k2/k2c-t2-01/SO-LIEU-7-NGAY.md`. Các mục kiểm dưới đây chỉ **đọc, không chặn**.

## 1. Tiêu đề (chủ dự án duyệt: J5 ngày 15/10; dự phòng 1 duyệt ở §8 ngày 16/10)
| Vai | Tiêu đề | Ký tự | Claim đỡ tiêu đề |
|---|---|---|---|
| CHÍNH | **Why America Builds So Few Ships (It's Not Just Wages)** | 53 | "around five a year" (CRS 2023); lương là một yếu tố, hồ sơ nêu thêm xuất khẩu và quy mô (chương 03) |
| DỰ PHÒNG 1 | **In 1943, America Launched 3 Ships a Day. What Happened?** | 55 | "three cargo ships a day" ở đỉnh năm 1943 (lời đoạn 00) |
| DỰ PHÒNG 2 | From Richmond to Ulsan: Why America Builds So Few Ships | 55 | Richmond 1940 (chương 01); Ulsan 1972 (chương 04) |

`release_check.py` (nhánh v5a): mọi tiêu đề ≤ 60 ký tự, **0 LỖI** (xem G2-BAO-CAO.md).

## 2. Thumbnail (chủ dự án tạo; ý đã chốt ở G1 §3)
- **T-B (mặc định Test & Compare):** không chữ. Nửa trái là ảnh OWI 1943 (LoC 2017854462, "No known restrictions"), cắt theo thân tàu Liberty, đèn hàn và đôi tay; mặt người **không** làm tiêu điểm. Nửa phải là ụ tàu 3D tự dựng với hai cẩu và hai thân tàu (`nen-3.jpg`), không gán là một xưởng Mỹ có thật. Hai nửa nối bằng đường cắt chéo; nửa trái sepia, nửa phải màu tự nhiên.
- **T-A (biến thể số):** bờ vịnh Richmond có ba tàu (`nen-1.jpg`). Hai hộp số **cùng đặt ở bờ Mỹ**: "1943: 3 SHIPS/DAY" và "NOW: ~5/YEAR". Không đặt số cạnh Ulsan.
- **T-A′ (biến thể motif):** phiếu đơn hàng 3D (dấu đỏ) trên bãi biển trống ở Ulsan (`nen-2.jpg`), kèm chữ 2 từ "ORDER FIRST?".
- **Bố cục chung:**
  - một vật hoặc vùng trung tâm;
  - mọi chữ nằm trong vùng an toàn 5 % mỗi cạnh, tránh góc dưới phải khoảng 18 % × 12 % (chỗ YouTube hiện thời lượng);
  - không mặt người thật làm tiêu điểm, không logo Hanwha/HD Hyundai, không cờ quốc gia làm điểm nhấn, không mũi tên, không "secret/hidden".
- **Bảng màu** (đo trên ảnh nền bằng k-means 5 cụm, không ước lượng):
  - `nen-1.jpg`: #a3a799 #c0ac88 #ac9978 #908670 #756651
  - `nen-2.jpg`: #a5ab9d #bdaa86 #979b8d #a18f70 #7b6a52
  - `nen-3.jpg`: #a6ab9d #bba884 #979a8c #99896c #71624c
  - Nền sepia sáng, nên chữ dùng khối tối #23262c với chữ vàng #F2C14E (màu nhấn của phim) để đủ tương phản ≥ 4,5:1.
- **Ảnh nền** (1280×720, không chữ): lấy thẳng từ khung cảnh đinh 1080p, trước lớp chữ (không chú thích, nhãn hay dòng nguồn).
  - `nen-1` = r00_launch, khung 170: vịnh Richmond, ba tàu hàng, sepia.
  - `nen-2` = r04_beach, khung 300: phiếu đơn hàng trên bãi biển Ulsan trống, sepia.
  - `nen-3` = r04_beach, khung 1210: hai cẩu và hai tàu Atlantic Baron/Baroness, bản dựng lại sau chấm mù G2.

### Prompt mẫu (T-A; dán vào công cụ tạo ảnh, đính kèm `nen-1.jpg`)
```
YouTube thumbnail, 1280x720. Use the attached frame as the background and keep its stylized sepia relief-map look, lighting and colours. Keep the three cargo ships on the bay as the single clear focal point. Add two dark boxes with yellow bold sans-serif text on the left (American) shore only: "1943: 3 SHIPS/DAY" and "NOW: ~5/YEAR", high contrast (at least 4.5:1), inside a 5% safe margin, not in the bottom-right corner. No faces, no logos, no flags, no real photos, no arrows, no extra text or numbers.
```

## 3. Kiểm (đọc, không chặn)
- Tiêu đề CHÍNH / DỰ PHÒNG 1 / DỰ PHÒNG 2: ĐẠT (≤ 60 ký tự, không cụm cấm; release_check v5a: 0 LỖI, 0 BÁO).
- Chữ thumbnail T-A: "1943: 3 SHIPS/DAY" (lời đoạn 00) và "NOW: ~5/YEAR" (lời đoạn 00, CRS 2023). Hai số khác cơ sở và khác thời kỳ; mô tả đã ghi rõ ở NOTES ON THE NUMBERS.
- Chữ trên thumbnail chủ dự án tạo: phiên P đọc ảnh, kiểm chữ trong vùng an toàn 5 %, không ở góc thời lượng, không có số ngoài claim.
- Claim được phép trên thumbnail: 1943, 3 a day, ~5 a year, 0.04%, 1962, 1972, 1974 (truy về lời khoá v3.4 và `claims`).

## 4. Test & Compare (chủ dự án chạy trong YouTube Studio)
1. Lúc đăng: dùng tiêu đề CHÍNH, chạy Test & Compare với 3 thumbnail **T-B, T-A, T-A′**.
2. Để YouTube chạy tới khi có kết quả; không đổi tiêu đề trong lúc test.
3. Thước đo: chỉ số YouTube chọn, cộng CTR 7 ngày so với T1 cùng mốc (Kinh thánh §8).
4. Vòng 2: giữ thumbnail thắng, thử tiêu đề CHÍNH với DỰ PHÒNG 1 (nếu kênh có test tiêu đề). Nếu không có, đổi tay sau 14 ngày khi CTR < T1 và ghi ngày đổi.
