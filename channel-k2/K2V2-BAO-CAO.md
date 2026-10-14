# Kênh 2 — Bộ hình k2v nâng cấp V2: bản đồ nổi + sticker (phiên V2, 14/10/2026)

Nhánh `k2-visual2` (từ `origin/main` @ `d3beb5f`; checks 1.10.2, LOCK `c598467f…`).

**Phạm vi sửa:** `design/k2v/`, `scripts/k2/`, `channel-k2/k2v2-mau/` (mới), `channel-k2/K2V2-BAO-CAO.md`, `RIGHTS.md`, `assets/k2/archive/` (thêm 1 ảnh tài sản công).

**Không đụng tới:**
- Không sửa `checks/`, không đọc mã trong `checks/`; chỉ chạy công cụ của K.
- Không sửa tệp của tập: `design/ll-hero/k2g01.js` và `k2c106.js` chỉ được nạp qua `?rx=`.
- Không gọi công cụ tạo ảnh/video AI ngoài.

**Kinh thánh kênh 2:** tệp `claude/CINE-LAB-BIBLE-KENH2.md` nằm trong Project, phiên này không đọc được (không có trong repo, không có trên Drive). Phiên làm theo đặc tả chi tiết trong lệnh giao việc. Mục cần đối chiếu nằm ở §9.

@@TOM-TAT@@

## 1. Đề tài mẫu và nguyên tắc nguồn
- **Đề tài:** kênh Erie (New York, 1825) và Main Line of Public Works (Pennsylvania, 1834).
- **Vì sao chọn:**
  - Lịch sử hạ tầng, không có phe, không có người còn sống.
  - Không nằm trong hàng đợi kênh 2. `market-k2/REPORT.md` không có video đối thủ nào về "canal"/"Erie".
  - Bản đồ nổi **tự nó cho thấy cơ chế**: khe Mohawk thấp xuyên vùng đồi, so với các dãy núi gấp nếp của Pennsylvania. Đây là câu chuyện mà hình phải kể được, không phải trang trí.
- **Nguồn số:**
  - Mọi số và câu trên hình có nguyên văn nguồn công khai trong `channel-k2/k2v2-mau/claims.md`: LOC, NPS, NPS ALPO, ECNHC (đối tác NPS), NYS Archives Partnership Trust, The Met.
  - Tác tử tra cứu đã đọc trang gốc. Số chỉ thấy qua kết quả tìm kiếm thì **không dùng**; ví dụ câu "$100 → $10" của NYSM và Britannica.
- **Học công thức, không học hình:**
  - Công thức lấy từ thể loại: bản đồ nổi, sticker viền trắng, máy trượt, vùng theo phe, bảng điểm.
  - Không mở, không tải, không dùng hình, thumbnail hay câu chữ của kênh nào.
  - Mọi tài sản đều tự dựng (three.js, vector), hoặc là tài sản công: USGS 3DEP, Natural Earth, The Met Open Access.

## 2. Module và API (chi tiết: `design/k2v/README.md` mục E)
### 2.1 `relief/map` — bản đồ địa hình nổi (`design/k2v/relief.js`, nền `scripts/k2/relief_build.py`)
@@RELIEF@@

### 2.2 Sticker vật — `design/k2v/stickers/` (16 vật + 8 vai), `scripts/k2/lib/sticker.js`, `design/k2v/sticker-lab.js`
@@STICKER@@

### 2.3 Nhân vật A-lite (phần nhân vật ≈ 6–8 % công sức phiên)
@@CHAR@@

### 2.4 Số liệu trên bản đồ (Q34(c))
@@NUM@@

### 2.5 Bảng điểm (component dùng lại)
@@SCORE@@

### 2.6 Sửa chung (dùng cho mọi tập kênh 2, chỉ thêm, không đổi hành vi cũ)
@@CHUNG@@

## 3. Cuộn shot mẫu (`channel-k2/k2v2-mau/K2V2-reel.yaml`, 44 s, 1080p24 SPP4)
@@REEL@@

## 4. Số đo
@@DO@@

## 5. Chấm mù (3 người chấm, model ghim)
@@MU@@

## 6. Giấy phép (chi tiết `RIGHTS.md` mục K2V2-* và dòng MET-11602)
@@GP@@

## 7. Chi phí
@@CP@@

## 8. Kiểm trước khi đẩy
@@KIEM@@

## 9. Việc đang chờ chủ dự án
@@CHO@@
