# K2C-T2-01 "Shipbuilding" — BÁO CÁO CỔNG G2 (phiên T2, 15/10/2026). DỪNG, chờ chủ dự án duyệt

> Làm theo lệnh duyệt G1b (15/10, M1–M4). Nhánh **`k2c-t2`**, đẩy cả `ccr-bef6f172-fcqat9`. Không sửa `checks/` và không đọc mã trong đó; không sửa `docs/BIBLE-KENH2.md`.

<!-- §0 tóm tắt: điền cuối -->

## 1. AUTHORSHIP, merge `main`
- Ghi dòng "Kênh 2 K2C-T2-01 "Shipbuilding" (G1b — DUYỆT)" vào `AUTHORSHIP.md`: M1–M4 và 7 điểm hình chủ dự án tự rà.
- `origin/main` (nền tảng NT 15/10: preflight, versions, golden, CHUAN-KENH-K2, SESSION-CHARTER) đã merge vào `k2c-t2` hai lần: đầu phiên G2 (24ed1c02) và trước G2 (§10).
  - Xung đột ghi thêm ở `AUTHORSHIP.md`: giải bằng cách giữ cả hai khối theo thời gian (SESSION-CHARTER §4.4). `RIGHTS.md` tự gộp, không xung đột.

## 2. Phí Section 301: tra lại ngay trước khi thu giọng
- **15/10/2026, ~06:10 UTC:**
  - Federal Register API, cơ quan USTR, văn bản từ 01/09/2026: vẫn 8 văn bản. Mới nhất là 08/10 (CBAM EU) và 07/10 (hai văn bản Section 301 về công nghệ/sở hữu trí tuệ); không văn bản nào về hàng hải.
  - Danh mục public inspection hiện hành: 81 văn bản, 0 của USTR.
  - govinfo: tệp FR-2025-11-13 vẫn tải được; API govinfo với DEMO_KEY trả 429 (hết lượt).
- **Kết luận: không đổi** (tạm hoãn tới 9/11/2026). Không sửa lời, SHA lời khoá giữ nguyên. Nhật ký ở `claims.md` §3.

## 3. Giọng và ASR
- **Thu:** Eric `cjVigY5qzO86Huf0OWal`, `eleven_multilingual_v2` (stability 0,5, similarity 0,75).
  - Chuỗi gửi đi trùng `loi-khoa.txt` từng đoạn. `make_spec.py` kiểm SHA của `script.md` và `loi-khoa.txt`, và so từng đoạn; lệch thì dừng.
  - 7 đoạn, 9 728 ký tự; Short S1 413 ký tự. Bộ đếm tài khoản: 105 498 → 114 553.
- **Lỗi chặn đã gỡ:** proxy cắt yêu cầu ElevenLabs sau ~30 s, nên đoạn 05 (2 361 ký tự) trả 502 ba lần. Các lần lỗi không bị tính ký tự.
  - Sửa trong `scripts/k2/prep.py`: đoạn dài hơn 1 900 ký tự thu thành 2–3 phần, tách ở ranh giới câu. Mỗi phần gửi kèm `previous_text`/`next_text` để giữ ngữ điệu liền; ghép mp3 không mã hoá lại; cộng bù mốc căn chữ theo thời lượng thật của phần trước. `scripts/ll/ll.py` không đổi.
- **Thời lượng thật:** 10:45,4 (ước ở G1b: 10:42,5; lệch +0,5 %).
- **ASR hai cách nghe** (`asr2.py`; kết quả ở `kiem-mu/asr/`):
  - A: small.en có gợi ý tên riêng. B: medium.en không gợi ý.
  - Cả 7 đoạn nghe đúng mọi số và tên.
  - Công cụ báo "thiếu" 7 mục, đều là lỗi phân tích của công cụ, không phải lỗi đọc: "zero point oh four", "seven forty seven", "five hundred won" bị nghe thành "501" vì đồng âm, "$5 billion". Không thu lại đoạn nào.

## 4. Dựng (Mốc B)
### 4.1 Nháp 540p lần 1 và chấm mù bước Dựng
- Nháp 540p (`K2_DRAFT=1`, 960×540, SPP 2): master 10:45,4; Short S1 30,5 s.
  - Mix: −14,0 LUFS, −1,6 dBTP, 14 SFX. Nhạc theo chương bằng `mix.py` hiện hành (không dùng `MIX=audio`).
- `dung_mu.py`: 3 người chấm mù (`claude -p`, ghim claude-sonnet-5-5, chỉ Read, thư mục trống) xem 7 tờ khung + lời theo giây + 66 dòng chú thích có mã. Chi phí $0,55.
  - Điểm: nhịp 4/4/4, đa dạng hình 4/4/4, chung 4/5/5 (thang 10, nháp 540p).
  - 38 dòng chú thích bị ≥ 2/3 đánh dấu thừa; 28 đoạn đề nghị cắt/rút (chi tiết `kiem-mu/dung/gop.json`).
### 4.2 Sửa một lượt
- **Chữ trên hình (M2): 66 → 29 dòng** (mục tiêu ≤ ~45).
  - Bỏ 37/38 dòng bị ≥ 2/3 đánh dấu. Giữ C48 (trích thư NFTC + nguồn) vì là lệnh M3 của chủ dự án.
  - Giữ mọi dòng nguồn, ngày, "as of", "Our read", LORE.
- **Thay chữ bằng biến cố trong hình** (giữ nhịp ≤ 6 s):
  - Thẻ trên vật: định nghĩa Jones Act trên con tàu; "high prices / few orders / no scale" trên đồng xu, phiếu đơn, cần cẩu; "Heavy-industry drive (Jan. 1973)" trên văn bản chính sách; phát hiện USTR trên địa cầu Trung Quốc.
  - Đạo cụ: báo cáo 2023 (văn bản); chuỗi xu → phiếu → tàu → cần cẩu ở phần kết luận; 3 đạo cụ cho "What to watch"; tàu rời Richmond ở câu giới thiệu tập sau.
  - Tô dòng thêm trên Federal Register: "On March 12, 2024, petitioners", "create leverage for the elimination of the investigated acts, policies, and practices", "is suspending for one year". Lệnh tạo lại ở §4.4.
  - Thêm khoá máy ở r02_cut, r02_quotes, r02_subsidy, r03_scale, r04_beach, r04_state, r05_philly; tuyến xuất khẩu vắng (xám, nét đứt) ở r03_loop.
- **Sửa hình theo người chấm và tự rà:**
  - Phim NARA: đổi sang đoạn đám đông + tàu trượt đà (ss 76,72; 128 khung, không lẫn cảnh mặt người ở khung 131). Kéo tương phản sepia (lo 26, hi 226). Shot vào muộn 0,45 s; còi tàu thành J-cut 1,25 s.
  - Ảnh Owens/Jones: dời tiêu điểm để chữ bên phải nằm trên nền tối.
  - Thẻ không chồng nhau: trích dẫn Jones Act hiện từng câu; 15–25 rời trước ~5/năm; $50 rời trước $18; $5B rời khi 1.5→20 hiện.
  - Cận cảnh hơn: thị trấn Richmond to hơn, máy gần hơn; người thợ to hơn và máy gần hơn ở r03_myth/r03_scale; Chung to hơn, máy gần hơn.
  - g04_pacific: bay xuống Hàn Quốc (preset flyto), thẻ $107 cỡ lớn. Seattle hiện ngay đầu shot Alaska.
- **Không áp dụng (lời đã khoá SHA, chờ chủ dự án):** các đề nghị cắt lời (xem §9).
- **Nhịp sau sửa (căn chữ thật):** trung bình 2,36 s, khoảng dài nhất 5,46 s → ĐẠT. Không khoảng nào trong vùng ±5 % quanh 6 s. Footage ≤ 20 %: ĐẠT. Lặp góc máy: 0 góc vượt 2.
