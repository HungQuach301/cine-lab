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

## 5. Bổ sung từ K 1.11 (O2, O5 — chủ dự án duyệt 15/10)
- **O2, Q34(d) của 1.10.2 đang ghim.** Đặc tả còn 4 shot `document` (8,3–13,3 s), chứ không phải 5 như K đếm trên @8ec1063: shot thư NFTC đã đổi thành bản đồ theo M3.
  - Cả 4 tách thành **8 shot ảnh tư liệu** `photo/print`, mỗi shot ≤ 8 s, tô **một** dòng trích:
    - "five labor union petitioners" / "On March 12, 2024, petitioners";
    - "sectors for dominance is unreasonable" / "burdens or restricts U.S. commerce";
    - "disincentivize the use and purchase of Chinese-built ships" / "create leverage for the elimination of the investigated acts, policies, and practices";
    - "In light of the trade and economic deal…" / "11:59 p.m. … November 9, 2026".
  - Trong mỗi cặp, hai shot dùng hai góc máy khác nhau (detail / push).
  - Bộ dựng: `design/k2v/photo.js` — `photo/print` nhận `page` + `hl` (tách hàm tô dòng dùng chung với `photo/doc`, cảnh `photo/doc` không đổi hành vi).
  - Lệnh tạo lại trang có dòng tô (cache ngoài git):
    `k2v_assets.py doc t2-fr-act --page 2 --find "The five labor union petitioners are" --find "On March 12, 2024, petitioners"`;
    `… --page 5 --find "disincentivize the use and purchase of Chinese-built ships" --find "create leverage for the elimination of the investigated acts, policies, and practices"`;
    `doc t2-fr-det --page 1 --find "burdens or restricts U.S. commerce" --find "sectors for dominance is unreasonable"`;
    `doc t2-fr-susp --page 1 --find "In light of …Xi Jinping" --find "11:59 p.m. Eastern Standard Time on November 9, 2026" --find "is suspending for one year"`.
  - **Chạy lại Q34 (1.10.2, `checks/ll/q_types.py`) lần đầu: (d) ĐẠT nhưng (c) TRƯỢT** — số neo hiện bằng 3D 6/12 = 50 % < 60 %. Lỗi này có từ G1b (cùng danh sách `anchors`), không do O2.
    - Sửa có nội dung: cặp GDP/người Hàn Quốc là phép so sánh nên dựng **cột 3D theo tỉ lệ thật**: 2025 = 12 km, 1962 = 12 × 107/36 227 ≈ 35 m (đĩa mỏng) ở Ulsan, kèm cột nhỏ trên địa cầu cho $107 năm 1962.
    - **Q34 ĐẠT: 42/42 shot có type; map 89,2 %, photo 10,0 %, footage 0,8 %; số neo 3D 8/12 = 67 %.**
- **O5-2 (ACTUAL 1 lần/khung):** 22 thẻ số ở 14 shot (cả 2 shot của Short) thôi khai `kind`; nhãn góc khai rõ `p.kind: actual`.
  - `scripts/k2/lib/k2.js`: `p.kind` (chuỗi) quyết định nhãn góc; `''` = không nhãn góc.
  - Philadelphia có cả số thật lẫn số dự báo: `p.kind: ''`, mỗi thẻ tự mang nhãn, hai thẻ ACTUAL không hiện cùng lúc.
  - Tàu chở dầu chỉ có ESTIMATE: giữ nguyên.
  - Thêm năm vào chữ phụ của số lịch sử còn thiếu: 0,04 % (2026 report), ~5/năm (2023 report), $18 (from Oct 2025), 200+ groups (Sept. 2026).
- **O5-3 (dòng nguồn ≤ 70 ký tự):** 6 dòng 76–87 ký tự đã rút; dài nhất nay 69. Nguồn đầy đủ ở mô tả và bình luận ghim.
- **O5-4 ("Facts as of"):**
  - Khai `loai`/`hieu_luc` ở `ep-src.yaml`:
    - FRACT `quy_dinh`, 2025-10-14 (Phụ lục I "Effective as of October 14, 2025");
    - FRSUSP `quy_dinh`, 2025-11-10 ("as of 12:01 a.m. … November 10, 2025", tới 9/11/2026);
    - FRDET `chinh_sach`, 2025-01-17 ("Decided: January 17, 2025").
  - Shot dẫn văn bản ghi `p.luat`.
  - "Facts as of" **giữ** ở 3 shot dẫn văn bản hiệu lực: phí (FRACT + FRSUSP), tạm hoãn (FRSUSP), What to watch (FRSUSP).
  - **Bỏ** ở 3 shot không dẫn văn bản hiệu lực: trích dẫn Jones Act (dự luật, không phải luật đang hiệu lực), thư các hiệp hội (dòng chú thích "As of 15 Oct 2026: no extension published" vẫn giữ), Philadelphia (tin báo).
  - Câu miễn trừ mở đầu giữ theo J3.
  - Lưu ý cho người rà: phí FRACT đang **tạm hoãn**, không hết hiệu lực; máy không tự tra hiệu lực (K 1.11 §9 mục 6).
- **O5-5 (`scripts/k2/rhythm.py`):** khung đầu của cảnh dùng lại đọc `p.frame0`, không có thì `p.off`; `opt.hl` không phải danh sách thì bỏ qua. Test mới trong `test_k2v.py`; 26/26 đạt.
  - **Nhịp đo lại (đặc tả, căn chữ thật): trung bình 2,31 s, dài nhất 5,46 s → ĐẠT**, không chỉ số nào trong vùng ±5 %.
- **Dấu cảnh:** sửa `photo.js` đổi dấu của mọi cảnh, vì dấu băm cả mã mọi module.
  - Thay vì dựng lại 44 cảnh, đã tính dấu cũ bằng `photo.js` trước khi sửa (`git show HEAD`) và chỉ chuyển dấu cho cảnh **không phải photo/*** có dấu cũ khớp đúng tham số (29 cảnh; không module nào import `photo.js`).
  - Dựng lại 16 cảnh: 8 trang văn bản, 2 ảnh, phim NARA, g04_pacific, r04_abroad, r02_cut, r03_myth, r06_home.

## 6. Rà tờ khung toàn tập trên nháp 540p sau O2/O5 (tự rà, mỗi 3 s) — lỗi tìm thấy và cách sửa
- **Địa cầu (cả 5 cảnh, có cảnh móc 0:05–0:16):** ba lỗi khai báo, đều có từ G1b, nên người chấm mù ở bước Dựng đã xem bản có lỗi.
  - `lift: 1` tính theo bán kính Trái Đất → tường cao gấp đôi địa cầu, thành quạt tia vàng/xanh. Sửa: `lift: true`.
  - Cột `r: 1.2` to hơn địa cầu → đĩa tím/kem khổng lồ. Sửa: 0,035.
  - Cung `h: 0.5` → dải tím nhô ra. Sửa: dùng mặc định.
  - Cột 0,04 % : 54,6 % cũ phóng đại phần Mỹ ~11×; nay theo tỉ lệ thật.
  - Tô quốc gia đậm hơn: `fill` 0,26 → 0,45.
- **Alaska 2 thiếu ghim `ship`:** con tàu và thẻ định nghĩa Jones Act chưa từng hiện. Đã thêm ghim + tàu đi theo tuyến Seattle → Juneau. Đã kiểm toàn tập: chỉ shot này thiếu.
- **Trang Federal Register dạng ảnh tư liệu cháy sáng**, chữ không đọc được. Sửa trong `photo.js` cho chế độ có trang: giấy bớt chói, phơi sáng 0,9. Máy tiến gần hơn (push 0,6), trang lớn hơn (h 3,4).
- **Ảnh Owens/Jones:** cột chữ bên phải đè mép bìa ảnh.
  - Preset `drift-r` của Jones bỏ qua tiêu điểm → đổi sang `push`.
  - Tiêu điểm x 1,1 và cột chữ dời sang `x0: 0,68`. Đo thử: mép ảnh dừng ở 0,61–0,64 khung.
- **Đạo cụ nhỏ ở r03_myth:** cỡ đạo cụ tính theo khoảng cách tới tâm nhìn, mà người thợ nằm cách tâm nhìn ~9 km. Sửa: máy nhìn thẳng vào người thợ.
- **Nhịp và đạo cụ:**
  - r03_scale trống ~5 s đầu shot → thêm đạo cụ "báo cáo 2023" từ đầu shot, người thợ vào ở "lists".
  - Tàu chở dầu: đồng xu "world price" không nhãn 7 s → nhãn từ đầu shot.
  - Chung sát mép trên → máy đi theo.
  - 4 đạo cụ kết luận chồng thành một cụm → dàn hàng.
  - Tàu gợi ý tập sau ra khỏi mép trái → dời vào vùng nước.
- **Phim NARA:** khung trong khung đè dải chú thích → `maxScale` 1,1 (cao ≈ 49 % khung ở 1080p). Đã kiểm khung cắt: shot 127 khung, cận mặt người chỉ bắt đầu ở khung 131, không lên hình.
- **Dấu cảnh:** mỗi lần sửa `photo.js` đổi dấu mọi cảnh. Dùng cách chuyển dấu có kiểm (dấu cũ tính bằng `photo.js` của HEAD, chỉ cho cảnh có tham số giống hệt) — 29 rồi 30 cảnh giữ nguyên, chỉ dựng lại cảnh thật sự đổi.
- **Đĩa:** worktree v5a (4,9 GB, cả repo) làm đĩa còn 1,5 GB → bản dựng tự dừng ở ngưỡng 3 GB. Đã gỡ worktree; sẽ thêm lại lúc kiểm gói rồi gỡ ngay.

## 7. Bờ biển Ulsan (mục 6 lệnh K 1.11) — ghi nhận, không chặn
- Kiểm ở khung 1080p của r04_beach (máy cách ~13–14 km, xem 100 %): đường bờ còn **bậc răng cưa của điểm ảnh nền**, thấy rõ ở khung cuối.
- Gốc lỗi là độ phân giải mặt nạ bờ của nền `korea` (ppd 1800, bờ suy từ DEM). Sửa phải **dựng lại nền lớn** (ppd cao hơn hoặc vector bờ biển cho vùng Ulsan), không chỉ dựng lại shot Ulsan.
- Theo lệnh: không sửa ở lượt này, ghi ở đây. Đề xuất cho T3/V: nền cục bộ ppd ≥ 3 600 quanh Ulsan (bbox ~129,3–129,5°E, 35,4–35,6°N), hoặc vẽ đường bờ từ Natural Earth 10 m / OSM coastline.
