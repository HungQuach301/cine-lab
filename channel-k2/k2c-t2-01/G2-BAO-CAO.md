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

## 8. CHỜ QUYẾT (chủ dự án) — chưa áp dụng; lời khoá SHA giữ nguyên tới khi có quyết định

### 8.1 Đề nghị cắt lời của người chấm mù (bước Dựng, `kiem-mu/dung/gop.json`)
Giây theo timeline master (lời và giờ không đổi giữa nháp và 1080p). "Tiết kiệm" = từ đầu câu cắt tới đầu câu kế (gồm khoảng nghỉ).

**Chi phí nếu cắt (áp cho mọi mục):**
- **Lời và giọng:** lời khoá SHA phải khoá lại (`loi-khoa.txt`, `LOI-KHOA.sha256`) và chạy ASR lại đoạn bị sửa.
- **ElevenLabs:** chọn một trong hai cách.
  - **(A)** Cắt âm ở ranh câu: 0 ký tự, nhưng có rủi ro nối ngữ điệu (nhất là khi bỏ câu giữa đoạn).
  - **(B)** Thu lại cả đoạn: số ký tự ghi ở từng mục. Đoạn 05 > 1 900 ký tự nên phải thu 2 phần.
- **Dựng lại:** mọi shot sau điểm cắt trong cùng đoạn đổi mốc theo lời, nên cảnh của chúng phải dựng lại ở 1080p.
  - Giờ máy ước theo số đo thật: 3,1 s/khung đồng hồ, 3 tiến trình.
  - Phải ghép lại lớp chữ của đoạn đó. Ước 0,9 s/khung — **chưa đo ở 1080p**, sẽ thay bằng số thật khi lượt 1080p hiện tại ghép xong.
  - Trộn tiếng, ghép master, Short: thêm ≈ 0,5 h.
  - Đo lại nhịp và Q34; giây khung RÀ GU sau điểm cắt sẽ dời.
- Các mục cùng một đoạn gộp chung một lượt dựng, nên chi phí không cộng dồn tuyến tính.

| Mã | Người chấm | Đoạn lời nguyên văn (giây) | Lý do người chấm | Claim | Tiết kiệm | EL (B) | Dựng lại 1080p (ước) | Xung đột cần lưu ý |
|---|---|---|---|---|---|---|---|---|
| D5 | **3/3** | 198,6–202,3: "If you're finding this useful, subscribing is how you'll catch the next one." | Lời mời đăng ký giữa phim cắt mạch ngay trước luận điểm "lương" | không | 4,7 s | 1 496 ký tự (đoạn 02) | 1 cảnh (r02_subsidy, 37 s) ≈ 0,8 h + chữ ≈ 0,6 h | Kinh thánh kênh 2: "Lời mời đăng ký nhẹ quanh phút 3" — cắt là lệch Kinh thánh; phương án khác: dời xuống cuối phim |
| D7 | **3/3** | 287,8–298,5: "So the record says something narrower than "wages": wages are one factor it lists; the lack of exports, and the scale that comes with them, is another." | Vòng lặp nói 3 lần (273–282, 287–305, 600s) | opinion (không mã; dựa C25) | 11,3 s | 1 258 (03) | 1 cảnh (r03_loop, 33 s) ≈ 0,7 h + chữ ≈ 0,6 h | — |
| D7b | (R1, R3 gồm cả câu sau) | D7 + 299,1–303,5: "Our emphasis on scale is a position the evidence only partly supports." | như trên | opinion | 16,7 s | 1 187 (03) | như D7 | Câu "only partly supports" do **người đọc mù vòng 4 (J4) yêu cầu 3/3** khi khoá lời v3.3 — bỏ là đi ngược vòng J4 |
| D13 | **3/3** | 620,1–630,8: "Supporters, like the American Maritime Partnership, make their case on jobs and security. Critics, like Senator Lee and Representative McClintock, make theirs on higher prices for Americans." | Phần kết lặp gần nguyên văn ủng hộ/phản đối ở 148–168 | C47, C48 (giữ ở chương 02) | 11,4 s | 886 (06) | 2 cảnh (r06_score2, r06_home, 45 s) ≈ 0,9 h + chữ ≈ 0,4 h | Chọn **một trong D4/D13** để còn đủ hai phía một lần (Kinh thánh: nêu cả hai phía) |
| D4 | 2/3 (R1, R3; R2 rộng hơn 113–170) | 148,3–167,9: "The American Maritime Partnership, a coalition of supporters, puts its case in its headline: "American Jobs. American Security." Critics, like Senator Mike Lee and Representative Tom McClintock, who introduced a bill on June twelfth, 2025, to repeal it, say its costs mean "higher prices for Americans."" | 35 s tên, ngày, trích dẫn trên bản đồ tĩnh; lặp ở phần kết | C47, C48 | 20,3 s | 1 269 (02) | 2 cảnh (r02_quotes, r02_subsidy, 66 s) ≈ 1,4 h + chữ ≈ 0,6 h | Như D13. Nếu cắt ở đây thì mất ngày dự luật 12/6/2025 và trích dẫn gốc; giữ D13 làm chỗ duy nhất nêu hai phía |
| D10 | **3/3** (giữ một câu báo giới hạn) | 399,8–403,1: "The sources we used don't say how much of that went to Hyundai's yard." | Hai câu "nguồn không nói" liền nhau | giới hạn nguồn (C49) | 3,7 s | 1 721 (04) | 2 cảnh (r04_state, r04_abroad, 51 s) ≈ 1,1 h + chữ ≈ 0,7 h | Câu còn lại 416,4–420,0 vẫn giữ tính trung thực về nguồn |
| D6 | 2/3 (R1; R2 224–252 rộng hơn) | 218,5–223,6: "By the 1950s, double. By the 1990s, three times." | Danh sách giá liệt kê trên hình ít đổi; giữ hai mốc | C23 | 5,8 s | 1 361 (03) | 4 cảnh (r03_ladder, r03_tanker, r03_scale, r03_loop, 103 s) ≈ 2,1 h + chữ ≈ 0,6 h | Mất 2 cột 3D số liệu 1950s/1990s (không thuộc `anchors`, Q34(c) không đổi) |
| D11 | 2/3 (R2, R3; R1 gộp 423–528) | 477,2–485,8: "The stated aim: to discourage the use and purchase of Chinese-built ships, and to press China to drop the practices the Trade Representative had found." | Cơ chế phí quá chi tiết so với luận điểm | C57 | 9,5 s | 2 210 (05, thu 2 phần) | 7 cảnh (113 s) ≈ 2,3 h + chữ ≈ 0,9 h | Câu mục đích của phí do **J4 yêu cầu 3/3** (nguồn FR-ACT) — bỏ là đi ngược vòng J4. Không thể chỉ rút "up to five times a year" mà không thu lại câu |
| D12 | 2/3 (R2, R3) | 510,5–523,4: "In September, a letter from more than two hundred trade groups, by our count of its signatories, asked for the suspension to be extended. Resuming the fees, they wrote, "would add another cost layer to an already strained transportation system."" | Bốn nhịp thủ tục liền nhau; thư là chi tiết phụ | C39 | 13,7 s | 2 116 (05) | 2 cảnh (r05_cost, r05_philly, 68 s) ≈ 1,4 h + chữ ≈ 0,9 h | **M3** (chủ dự án): giữ một câu trích + nguồn của thư — cắt là đổi quyết định M3 |
| D1 | 1/3 (R2) | 17,0–21,6: "And the company that has announced plans to expand a Philadelphia shipyard is South Korean." · 28,6–32,4: "And there's a deadline in this story: November ninth, 2026." | Mở đầu 34 s, rút còn ~15 s | C40, C01 | 9,8 s | 307 (00) | 1 cảnh (r00_philly, 19 s) ≈ 0,4 h + chữ ≈ 0,2 h | **J2/J3** (móc "nghịch lý trước", miễn trừ 0:03–0:12) — chỉ rút câu, không đổi cấu trúc móc |
| D9 | 1/3 (R1) | 339,3–356,5: "A 2010 Korea Times column adds a story. Chung went abroad carrying a photo of the empty beach and a 500-won banknote showing a turtle ship, a warship from Korea's history. We found no documents for it, so treat it as lore: one columnist's account, not a record." | Chuyện bên lề 18 s trên bản đồ tĩnh | C30, C31 (lore) | 17,6 s | 1 530 (04) | 3 cảnh (r04_beach, r04_state, r04_abroad, 102 s) ≈ 2,1 h + chữ ≈ 0,7 h | Thẻ LORE và tờ 500 won (sửa điểm hình 04-2-36 của chủ dự án) sẽ bỏ theo |
| D2 | 1/3 (R2) | 59,7–65,7: "As a publicity stunt, one Richmond yard built the Robert E. Peary in four days and fifteen and a half hours." | Chi tiết đố vui sau mốc 122 → 39 ngày | C04 | 6,4 s | 946 (01) | 4 cảnh (62 s) ≈ 1,3 h + chữ ≈ 0,4 h | — |
| D3 | 1/3 (R2) | 94,1–97,0: "The British government, and America's own Maritime Commission." | "Our read" nói một ý ba lần | C08, C15 | 3,5 s | 992 (01) | 1 cảnh (r01_dive, 16 s) ≈ 0,3 h + chữ ≈ 0,4 h | — |

**Không đề xuất cắt lời** (đã xử lý bằng hình hoặc không nêu câu cụ thể):
- R1 305–340 (GDP Hàn Quốc + câu "no experience"): đã thêm cột GDP 3D, Chung to hơn và máy đi theo.
- R3 635,5–645 (phần kết và câu dẫn tập sau "hiện hai lần"): đã bỏ dòng chữ "Next…" (C66); lời giữ.
- R1 423–528 ("giảm một nửa phần USTR"): đã quy về D11 và D12.

**Đề xuất của P:**
- Nếu chỉ cắt **3/3 mà không đụng quyết định đã duyệt**: D7 (11,3 s) + D13 (11,4 s) + D10 (3,7 s) = **26,4 s**; ba đoạn 03, 04, 06; giờ máy ≈ 2,7 h cảnh + ≈ 1,7 h chữ + 0,5 h.
- D5 cần chủ dự án quyết vì lệch Kinh thánh: hoặc giữ, hoặc dời xuống cuối phim.
- D4, D7b, D11, D12, D1 đụng các quyết định J2/J3/J4/M3 đã duyệt; P không đề xuất trừ khi chủ dự án đổi các quyết định đó.

### 8.2 Tiêu đề (Q3: mọi tiêu đề ≤ 60 ký tự; J5: tiêu đề chính)
| Vai | Tiêu đề | Ký tự | Claim đỡ |
|---|---|---|---|
| **Chính (J5, đã duyệt)** | Why America Builds So Few Ships (It's Not Just Wages) | 53 | C05 (0,04 % tấn đóng tàu thế giới, CRS 2026), C21 (~5 tàu/năm, CRS 2023), C25 (lương là một yếu tố; thiếu xuất khẩu → không đạt quy mô, CRS 2023), C22 (huyền thoại "lương") |
| **Dự phòng 1 — MỚI, chờ duyệt** | In 1943, America Launched 3 Ships a Day. What Happened? | 55 | C03 (1943, đỉnh: 3 tàu Liberty/ngày, NPS), C05 + C21 (mức hiện nay) |
| (Dự phòng 1 cũ, bỏ vì 70 > 60 ký tự) | In 1943, America Launched 3 Ships a Day. Why Does It Build So Few Now? | 70 | như trên |
| Dự phòng 2 (không đổi) | From Richmond to Ulsan: Why America Builds So Few Ships | 55 | C07, C13 (xưởng Kaiser ở Richmond, 747 tàu), C31, C06 (Ulsan: động thổ 3/1972, xong 1974 — tự thuật công ty), C05 + C21 |

- Ba tiêu đề đều qua `release_check.py` của v5a (R1 ≤ 60 ký tự) trong lần chạy thử trên bản nháp: 0 LỖI.
- Dự phòng 1 mới giữ con số mạnh nhất của móc (3/ngày năm 1943) và để câu hỏi mở. Không có số nào ngoài claims.

## 9. Áp quyết định §8 (16/10) — lời v3.4
- **Cách làm (A, 0 ký tự ElevenLabs):** `sua_loi.py apply` cắt/chèn âm ở ranh câu trên bản thu sẵn có.
  - Điểm nối đặt giữa khoảng nghỉ trước và sau câu; hoà 25 ms trong vùng lặng.
  - Căn chữ bỏ đúng ký tự của câu và dời mốc theo độ dài âm; chữ ký cache tính lại.
  - Bản gốc giữ ở `vo/v3.3/` và `script-v3.3-KHOA.md`; nhật ký ở `vo/sua-v3.4.json`.
  - Lời khoá v3.4: `script.md` + `loi-khoa.txt` sửa cùng chữ, `LOI-KHOA.sha256` tính lại.
  - Chương 06 không còn gắn C47/C48 (vẫn nêu ở chương 02).
- **Độ dài âm:**
  - D7 −11,26 s (03).
  - D10 −3,71 s (04).
  - D13 −5,34 −5,88 s (06).
  - D5: chương 02 −3,79 s; chèn vào chương 06 +4,09 s, sau "No source we found measures how much each factor counts.", trước "Back in Richmond…".
  - **Phim 645,4 s → 618,9 s.**
- **Nghe thử + ASR từng điểm nối** (`noi_check.py`, hai cách nghe A small.en / B medium.en, cửa sổ ±6 s; `kiem-mu/asr/noi-v3.4.json`).
  - 6 điểm nối: khoảng lặng 0,41–0,75 s và chênh mức −/+ dB đều **trong dải ranh câu tự nhiên của chính đoạn đó**. WER A/B: 03 0,04/0,04; 06 (sau bỏ D13) 0,09/0,03; 06 (chèn D5, hai đầu) 0,03/0,13 và 0,00/0,00; 02 (cuối) 0,00/0,00.
  - Điểm 04 bị công cụ gắn cờ (WER 0,13/0,21) vì "Our read" nghe thành "Our red" + lệch mép cửa sổ. **Bản thu gốc v3.3 cùng chỗ cũng nghe "Our red" (small.en)** → đồng âm, không phải lộ nối.
  - **Không đoạn nào phải thu lại → ký tự ElevenLabs thật: 0.** `prep` chạy với proxy chặn để bảo đảm không gọi API: bộ đếm "gửi 0".
- **Mốc shot:** `moc_check.py` so mọi mốc "@từ" của 4 đoạn bị sửa giữa căn chữ v3.3 và v3.4 (mốc trước điểm nối phải giữ giây, mốc sau phải dời đúng phần cắt/chèn).
  - 12 mốc lệch → sửa: bỏ khoá máy theo câu đã cắt (02: `@subscribing`, `@next+2`; 03: `@factor`; 06: `@Supporters`, `@Critics`, `@theirs`); bỏ tuyến "xuất khẩu vắng" của 03 (lời không còn nói "lack of exports"); bảng "The record" của 03 hiện ở `@emphasis`; khoá cuối r04_state theo "government." thứ 2; thêm khoá máy 06 ở `@measures` và `@subscribing`.
  - **Mốc `@sources#1` của 04 không gãy mà tự trỏ sang câu "nguồn" còn lại (lệch 16,5 s)** — đã bắt và bỏ.
  - Còn 2 mốc báo lệch, cả hai đúng ý: `@government#2+1` mới đặt; `@Back-0.5` nằm ngay sau câu chèn.
- **Nhịp (đặc tả v3.4, căn chữ thật): trung bình 2,27 s, dài nhất 5,46 s → ĐẠT**; footage ≤ 20 % ĐẠT.
- **Cảnh đổi dấu vì v3.4: 4** (r02_subsidy, r03_loop, r04_state, r06_score2; 107,9 s cảnh) → dựng lại 1080p, gộp trong lượt dựng đang chạy. Các cảnh khác tính giờ theo cảnh nên không đổi.
- **Đề xuất sửa Kinh thánh (chủ dự án, D5):** "lời mời đăng ký đặt ở cuối hoặc ở ranh chương, không chen trước luận điểm chính" — P ghi vào `docs/BIBLE-KENH2.md` (phiên này không sửa Kinh thánh).
- **Tiêu đề dự phòng 1 DUYỆT** (16/10): "In 1943, America Launched 3 Ships a Day. What Happened?" (55 ký tự) — đã có trong `make_release.py`; chạy lại `release_check` ở bước gói.

## 10. RÀ GU 1080p lần 1 — TRƯỢT → sửa đúng chỗ, dựng lại, chấm lại
- **Bản chấm:** master 1080p v3.4 (SHA `86fc2866…`, 618,917 s), 3 người chấm mù (`claude -p`, chỉ công cụ Read), seed 20261015.
  - Giây khung khai **trước khi ghép** (`g2/rague-cap.json`, `g2/sua-cap.json`); không đổi giây sau khi đã thấy bản dựng.
- **RÀ GU (P1–P7, T2 vs T1): TB T2 6,62 / T1 5,86 → TRƯỢT** (dưới 7,0; thua 2 cặp).

  | Cặp | Loại | T1 | T2 | Ghi chú người chấm (T2) |
  |---|---|---|---|---|
  | P1 | bản đồ địa hình mở chuyện | 6,33 | 6,33 (hoà) | icon chồng nhau thành cụm; không tên nơi; "LORE…" khó hiểu |
  | **P2** | **bản đồ tuyến** | **7,33** | **6,67 (thua)** | "$107 1962" không đơn vị/chủ thể; tuyến chạy ra biển trống; không tên nơi |
  | P3 | số liệu thành vật 3D | 5,00 | 6,67 | khung rơi trước khi thẻ "≈ 4×" hiện (chỉ có đồng xu) — giữ giây đã khai |
  | P4 | chân dung tư liệu + chú thích | 6,00 | 7,00 | — |
  | P5 | màn tóm tắt/so sánh | 4,00 | 7,33 | — |
  | **P6** | **footage thật** | **7,00** | **5,67 (thua)** | newsreel là ô nhỏ ~1/3 khung trên nền mờ ("flat slide look") |
  | P7 | ảnh tư liệu toàn khung | 5,33 | 6,67 | — |

- **Phần bị sửa v3.4 (E1–E5, T2 vs T1): TB T2 6,47 / T1 5,27 → TRƯỢT**, thua E2 (6,00 so với 8,00). E2 là cùng cảnh với P2 (r04_abroad), cùng lý do.
- **Chẩn đoán (xem khung thật, không chỉ đọc điểm):** đây là lỗi hình thật, không phải khẩu vị.
  - **r04_beach (P1):** chú thích "LORE" **ở lại tới hết cảnh**, phủ lên cả phần lời về lịch sử công ty (động thổ 1972, hoàn thành 1974). Như vậy sự kiện có nguồn bị dán nhãn "lore": **lỗi nội dung**, sửa bất kể điểm.
  - **r04_abroad (P2/E2):** số 1962 thiếu đơn vị và chủ thể; không có tên Ulsan / South Korea.
  - **f_liberty (P6):** khung trong khung chỉ phóng 1,1× (Kinh thánh cho phép ≤ 1,5×) và nằm giữa khung dọc, nên không phóng thêm được mà không đè dải chú thích.
- **Sửa (đúng chỗ, không thêm phần tử để vượt ngưỡng):**
  - **r04_beach:**
    - Chú thích LORE kết thúc tại "Hyundai's own history…" và thay bằng "By Hyundai's own history: ground broken 1972, yard done 1974".
    - Phiếu đơn hàng và hai tờ tài liệu (ảnh bãi trống, tờ 500 won) rút khỏi khung cùng lúc.
    - Nhãn "Ulsan · South Korea" giữ tới hết cảnh.
    - Hai tàu Atlantic Baron/Baroness dời ghim ra biển, đứng cạnh nhau, không chồng lên cẩu.
    - **Dựng lại cảnh 3D** (1217 khung; prop 3D nằm trong cảnh): chia 3 phần khung song song (`--only`), gộp khung + điểm neo, rồi ghi dấu.
  - **r04_abroad:**
    - Thẻ "$107 · output per person, 1962 (current $)", cùng cách ghi với thẻ 2025.
    - Thêm nhãn "Ulsan · South Korea" (lớp 2D, không dựng lại 3D).
    - Thử thêm thẻ "Customers abroad" ở đầu tuyến nhưng điểm neo nằm ngoài khung nên bỏ: chú thích "Our read…" đã nói điều đó.
  - **f_liberty:**
    - `maxScale` 1,1 → 1,45 (≤ 1,5 theo Kinh thánh §4).
    - `crop 624:456:6:4` bỏ viền overscan đen của bản phát hình (không cắt nội dung).
    - Khung dời lên 110 px bằng tuỳ chọn mới `opt.oy` trong `scripts/k2/hero.js`. Khung nay 904×662 thay 704×528 (diện tích ×1,61) và không chạm dải chú thích.
  - **Dấu cảnh:** `hero.js` đổi nên mọi dấu đổi. Chuyển dấu cho 42 cảnh có tham số không đổi (so tham số cũ/mới, cùng cách đã dùng khi sửa photo.js); chỉ 2 cảnh dựng lại.
- **Lưu bản chấm lần 1:** `kiem-mu/ragu-l1/`, `kiem-mu/ragu-sua-l1/`, điểm `kiem-mu/ragu-score-l1.json`, `kiem-mu/ragu-sua-score-l1.json` (chi phí API sau lần 1: $6,70 / trần $11).
- **Kết quả chấm lại:** ghi ở §11 sau khi ghép lại và chấm lại cùng giây khung đã khai.

## 11. RÀ GU 1080p lần 2 — VẪN TRƯỢT → DỪNG CHỜ CHỦ DỰ ÁN (luật chủ dự án 16/10: không tự sửa vòng 3)
- **Bản chấm lần 2:** master 1080p sau sửa §10, **SHA256 `fd395b6976ef815a042c776194abd3661182be9a296622a819fbd09fe8bb933c`**.
  - Thời lượng 618,917 s; 1920×1080, 24 fps; −14,0 LUFS, −1,6 dBTP, LRA 2,2.
  - Short không đổi: `9d4f3e45…`.
- **Giao thức giữ nguyên:**
  - Đúng các giây khung đã khai trong `g2/rague-cap.json` và `g2/sua-cap.json`; hai tệp này và `blind_g2.py` không đổi so với HEAD, đã kiểm bằng `git diff` trước khi chạy.
  - Seed 20261015 (RÀ GU) và 20261016 (phần sửa); 3 người chấm; chỉ công cụ Read.
  - Bản chấm lần 2 lưu ở `kiem-mu/ragu/`, `kiem-mu/ragu-sua/`, `kiem-mu/ragu-score.json`, `kiem-mu/ragu-sua-score.json`. Lần 1 lưu ở `*-l1`.

### 11.1 Điểm từng cặp, lần 1 → lần 2
**RÀ GU (P1–P7): TB T2 6,62 → 6,81 (T1 5,86 → 5,81). TRƯỢT: dưới 7,0. Không còn thua cặp nào.**

| Cặp | Cảnh (giây) | T1 L1 → L2 | T2 L1 → L2 | 3 người (L2) | Chọn T2 (L2) | Kết luận |
|---|---|---|---|---|---|---|
| P1 | r04_beach (355,49) | 6,33 → 6,00 | 6,33 → **7,00** | 7/7/7 | 3/3 | hết hoà, thắng |
| P2 | r04_abroad (389,37) | 7,33 → 7,00 | 6,67 → **7,33** | 8/7/7 | 1/3 | hết thua, thắng điểm |
| P3 | r03_tanker (228,58) | 5,00 → 5,33 | 6,67 → 6,67 | 7/6/7 | 2/3 | không sửa ở §10 |
| P4 | p01_owens (75,50) | 6,00 → 6,33 | 7,00 → 6,67 | 7/6/7 | 3/3 | không sửa |
| P5 | r06 so sánh (577,30) | 4,00 → 3,67 | 7,33 → 7,00 | 7/7/7 | 3/3 | không sửa |
| P6 | f_liberty (50,68) | 7,00 → 6,33 | 5,67 → 6,33 | 6/6/7 | 3/3 | hết thua (hoà điểm, thắng 3/3 lựa chọn) |
| P7 | p02_jones (124,96) | 5,33 → 6,00 | 6,67 → 6,67 | 6/7/7 | 3/3 | không sửa |

**Phần bị sửa v3.4 (E1–E5): TB T2 6,47 → 6,87 (T1 5,27 → 5,33). TRƯỢT: dưới 7,0 và thua E2.**

| Cặp | Cảnh (giây) | T1 L1 → L2 | T2 L1 → L2 | 3 người (L2) | Chọn T2 (L2) |
|---|---|---|---|---|---|
| E1 | r03_loop (285,12) | 5,00 → 5,33 | 6,33 → 7,00 | 7/7/7 | 3/3 |
| **E2** | **r04_abroad (385,93)** | **8,00 → 8,00** | **6,00 → 6,33** | 7/6/6 | **0/3 — THUA** |
| E3 | r06 kết (602,53) | 4,00 → 4,00 | 7,00 → 7,00 | 7/7/7 | 3/3 |
| E4 | r06 kết (606,56) | 4,00 → 4,00 | 7,00 → 7,67 | 8/8/7 | 3/3 |
| E5 | r02_subsidy (197,42) | 5,33 → 5,33 | 6,00 → 6,33 | 6/6/7 | 3/3 |

- **Vùng ±5 % quanh ngưỡng 7,0 (luật cứng, phải nêu tên):**
  - RÀ GU 6,81 (−2,7 %).
  - Phần sửa 6,87 (−1,9 %).
  - Các cặp nằm trong vùng ±5 %: P1 7,00; P2 7,33; P5 7,00; E1 7,00; E3 7,00.
- **Độ nhiễu của người chấm:** khung T1 giữ nguyên giữa hai lần mà điểm vẫn đổi tới 0,67 mỗi cặp (P6 7,00 → 6,33; P7 5,33 → 6,00). Mức chênh 0,19–0,13 so với ngưỡng nằm trong độ nhiễu này. Mình không dùng điều này để coi là đạt; chỉ nêu để chủ dự án cân nhắc cách quyết.

### 11.2 Ghi chú nguyên văn của người chấm (lần 2; các cặp dưới 7,0 hoặc thua)
- **E2 (THUA, T2 = X):**
  - R1: "The $107 callout is tied to a tiny yellow box by a thin line. The Ulsan marker is a faint dot, and the callout sits well away from it. Half the frame is empty ocean. … No route or movement is visible, so the frame reads as two disconnected labels."
  - R2: "The $107 callout leader points to an unexplained small yellow rectangle that is not Ulsan. The Ulsan label floats away from its pin, and no country or region context is shown."
  - R3: "A viewer can't tell if $107 belongs to Ulsan, to the box, or to the country. … The map is zoomed too far in to show where Ulsan sits in Korea."
- **P3 (6,67):**
  - R1: "there are no numbers or labels and no place name. The only text is a small source line. It's unclear what the coins count, what region this is, or why one coin is separated from the other four."
  - R3: "Five coins sit on an unnamed landscape and nothing says what they count or where."
- **E5 (6,33):**
  - R1: "One small cube, a tiny document icon and a cut-off cube at the left edge give no clear place or comparison. The caption says 'Construction Differential Subsidy' but nothing in the frame connects to it."
  - R3: "A big teal shape is cut off at the left edge. … The document icon isn't tied to the 'Construction Differential Subsidy' caption."
- **P6 (6,33):**
  - R1: "The photo is small in the frame and low-res, and the large empty dark area at the bottom looks unfinished."
  - R2: "The footage is small and sits in a big, dark, empty blurred border."
- **P4 (6,67), P7 (6,67):** khen bố cục; chê dải tối dưới làm mờ mép ảnh và dòng nguồn nhỏ. Ví dụ R2 P7: "The bottom gradient washes out the lower part of the mat, and the print is slightly off-center and tilted."
- **E1 (7,00):** R1: "The map shows no place name and no numbers, so the viewer can't tell where this is or what the 4 coins, the document or the loop mean." R2: "The 'Wages 1 / Scale 1' pills are cryptic."

### 11.3 Chẩn đoán từ khung thật (đã xem từng khung T2)
- **E2, r04_abroad giây 2,1 của cảnh — LỖI HÌNH THẬT.**
  - Thẻ "$107" bám vào cột GDP 1962 vẽ đúng tỉ lệ thật, nhỏ tới mức trông như "hộp vàng bí ẩn". Đúng tỉ lệ là chủ ý, để cột 2025 cao gấp ≈ 338 lần.
  - Lúc này tuyến chưa vẽ và chú thích chưa hiện (cả hai đặt ở "@abroad#2"); máy quay quá gần nên không thấy vị trí Ulsan trên bán đảo Triều Tiên.
  - Sửa §10 (đơn vị, nhãn Ulsan) đúng hướng nhưng chưa đủ: điểm T2 tăng 6,00 → 6,33; T1 ở cặp này là khung mạnh (8,00).
- **P3, r03_tanker giây 8,81 — LỖI HÌNH THẬT (lỗi hiển thị).** Thẻ "world price" khai hiện từ giây 0,6 nhưng **không thấy trên khung**; thẻ "≈ 4×" mới hiện ở "@four", sau giây khung. Khả năng cao là điểm neo `col:world` không hiện (v = false) ở đoạn này. Cần kiểm điểm neo của prop dạng đồng xu; chưa kiểm vì đang dừng.
- **E5, r02_subsidy giây 29,15 — LỖI HÌNH THẬT.**
  - Có một khối xanh bị cắt ở mép trái khung (lỗi khuôn hình máy quay).
  - Icon tài liệu không có nhãn nên không nối với chú thích "Construction Differential Subsidy".
- **E1, r03_loop — NỬA HÌNH, NỬA KHẨU VỊ.** Bảng "The record: Wages 1 · Scale 1" khó hiểu nếu đứng riêng một khung, và các icon không có nhãn ở giây khung (các thẻ "high prices / few orders / no scale" đã tắt ở "@pieces"). Đây là cách kể theo thời gian; khung tĩnh làm lộ điểm yếu.
- **P6, f_liberty — RÀNG BUỘC KINH THÁNH, không phải lỗi dựng.** Nguồn 640×480; khung đã ở 1,45×, gần trần 1,5× (Kinh thánh §4). Muốn lớn hơn phải đổi luật hoặc tìm bản nguồn độ phân giải cao hơn.
- **P4, P7 — KHẨU VỊ / CHI TIẾT.** Dải tối dưới phủ mép ảnh in; không sai nội dung.

### 11.4 Đề xuất sửa (chờ chủ dự án chọn; chưa làm gì)
| # | Việc | Cảnh | Dựng lại 3D? | Giờ máy ước | API ước |
|---|---|---|---|---|---|
| S1 | P3: sửa điểm neo hoặc thẻ "world price" cho hiện từ đầu cảnh; thêm chú thích "Price to build one tanker: U.S. vs world (one firm's estimate)" | r03_tanker | không (nếu chỉ là neo 2D) / 0,8 giờ-tiến trình nếu prop cần xuất neo | 0–0,3 giờ thật | 0 |
| S2 | E2: chú thích từ đầu cảnh "South Korea, 1962: about $107 output per person"; thẻ $107 bám nhãn Ulsan thay cho cột nhỏ (cột giữ đúng tỉ lệ) | r04_abroad | không | — | 0 |
| S3 | E2: máy quay mở đầu rộng hơn, thấy bán đảo Triều Tiên rồi mới vào Ulsan | r04_abroad | **có**, 482 khung | ≈ 1,2 giờ-tiến trình (≈ 25 phút thật, chia 3) | 0 |
| S4 | E5: khuôn hình máy quay bỏ khối bị cắt mép; nhãn cho icon tài liệu ("CRS report") | r02_subsidy | **có**, 792 khung | ≈ 2,0 giờ-tiến trình (≈ 45 phút thật, chia 3) | 0 |
| S5 | E1: nhãn chữ cho icon và bảng "The record" giữ tới hết cảnh | r03_loop | không | — | 0 |
| S6 | P6: (a) cho phép riêng clip này phóng tới 1,8×, **cần chủ dự án sửa Kinh thánh §4**; hoặc (b) tìm bản nguồn ≥ 720p; hoặc (c) giữ nguyên | f_liberty | footage (1 phút) | ≈ 0 | 0 |

- **Sau sửa:**
  - Dựng lớp chữ các đoạn bị đổi: 02, 03, 04, khoảng 25 phút; 01 thêm 6 phút nếu chọn S6.
  - Ghép master khoảng 40 phút; Short không đổi.
- **Tổng giờ máy ước:** S1 + S2 + S5 (chỉ 2D) ≈ 1,1 giờ thật; thêm S3 + S4 ≈ 2,3 giờ thật (≈ 4,5 giờ-tiến trình).
- **Chấm mù lần 3 (cùng giao thức):**
  - RÀ GU ≈ $1,28; phần sửa ≈ $0,84; cả hai ≈ $2,12.
  - **Vượt mốc dừng $10** (lũy kế sẽ ≈ $10,94, sát trần $11) → **cần chủ dự án cho phép.**
  - Phương án rẻ hơn: chỉ chấm lại phần sửa (≈ $0,84, lũy kế ≈ $9,66), nhưng như vậy là đổi giao thức nên cũng cần chủ dự án duyệt.

### 11.5 Chi phí và giờ máy thật của vòng sửa §10
- **API `claude -p` (lũy kế tập, `kiem-mu/cost.jsonl`): $8,82 / trần $11 (mốc dừng $10).**
  - Chấm lần 1: $5,86 → $6,70.
  - Chấm lần 2: RÀ GU $1,28, phần sửa $0,84.
- **Ký tự ElevenLabs của vòng này: 0** (prep chạy với proxy chặn).
- **Giờ máy thật:**
  - r04_beach: 1217 khung, 3 tiến trình × 78 phút ≈ 3,9 giờ-tiến trình (≈ 15 giây/khung mỗi tiến trình khi chạy song song).
  - f_liberty: < 1 phút.
  - Build `render mix ghep shorts`: 5644 s (1,57 giờ). Cả 7 đoạn dựng lại lớp chữ, vì dấu cảnh nằm trong băm đoạn.

### 11.6 Trạng thái các việc trước G2 (đã làm tới lúc dừng)
- **Gói phát hành:** đã sinh lại với master mới (SHA256SUMS cập nhật). `release_check` v5a: **ĐẠT, 0 LỖI, 0 BÁO**.
  - Tiêu đề CHÍNH 53, DỰ PHÒNG 1 55, DỰ PHÒNG 2 55 ký tự; mô tả 3607 ký tự; bình luận ghim 3960 ký tự.
  - Có PACKAGING-BRIEF và 3 ảnh nền.
- **Mã thời gian footage** đã điền vào `SOURCES-FOOTAGE.csv`. **Bản đồ nhịp** sinh lại (`g2/BAN-DO-NHIP.md`).
- **Merge `main`:** origin/main không có commit mới.
- **`versions.py check`: LỆCH, 2 mục chặn** (không tự cập nhật VERSIONS.yaml):
  - `toolkit.k2v.tree_sha256` đổi (photo.js, hero.js `opt.oy`, rhythm.py, k2.js);
  - `served_models` có `claude-haiku-5-5` ngoài model ghim. CLI `claude` tự dùng Haiku cho tác vụ phụ khi chạy `claude -p`; việc chấm ghim Sonnet.
  - Báo thêm (không chặn): `claude_cli` 2.1.300 → 2.1.301.
- **RÀ LUẬT (checks 1.10.2) — CHƯA XONG, chỉ có kết quả chạy thử, chưa phân tích.**
  - Đạt: Q34 (`q_types`), Q33 (`q_scene`), `q_rights`.
  - Trượt: `q_footage` Q32, `q_rhythm` Q14/Q15/Q17, `q_setting` Q26b.
  - Lỗi cách gọi (cần đường dẫn mp4 hoặc chạy theo mô-đun): `q_diversity`, `q_av`, `q_chu`, `q_nhip`, `q_amthanh`.
  - Chưa xác định mục nào áp cho kênh 2. Sẽ phân tích và ghi khi được tiếp tục; không kết luận ở đây.
- **golden.py run:** đang chạy lúc dừng; kết quả ghi khi xong.
- **k2check v1.11 (chỉ báo):** chưa chạy, vì dừng.

**DỪNG chờ chủ dự án.**
- **Cần quyết:**
  1. Chọn sửa S1–S6, hoặc chấp nhận bản hiện tại.
  2. Cho phép vượt mốc dừng $10 để chấm lần 3; hoặc chọn chỉ chấm lại phần sửa.
  3. S6 có đổi Kinh thánh §4 (trần phóng 1,5×) hay không.
