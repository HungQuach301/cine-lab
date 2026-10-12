# K2G-01 "Steel" — Báo cáo G2 (phiên P kênh 2, 12/10/2026)

> Lệnh 11/10 21:05: chạy liền tới G2, trần API $40, không subagent, không YouTube Data API. **Dừng ở G2, chờ duyệt.**
> Nhánh `k2g-ep01`. Video (master 1,35 GB, 2 Short) ở `/var/tmp/cine-out/k2g-ep01/`, chưa đưa lên git: cần chủ dự án cho phép mở nhánh phát hành Git LFS như LL (xem §10).

## 0. Tóm tắt
- **Đã xong cả 7 bước:** giọng, nhạc/SFX, 8 bộ cảnh, nháp → một lượt sửa → 1080p, QC + chấm mù một lần, gói phát hành, báo cáo.
- **Bản cuối:** 17:10 (1 030,1 s), 1080p 24 fps, −14,0 LUFS, true peak −1,6 dBTP; 2 Short 23,3 s và 32,9 s.
- **QC nhà máy:** đạt 23/25 mục. Còn 2 mục trượt:
  - Q5 tương phản 2,68 ở một tựa phụ (lỗi nhỏ, ghi lại);
  - Q23 ở lời đã khoá (so số USGS 1950 với số worldsteel 2025, khác cơ sở; đã ghi rõ cơ sở trên hình).
- **Năm luật máy LUAT-G §7:** đạt cả 5.
- **Chấm mù hình (Q27):** tay nghề trung bình **5,1/10**; cả 3/3 người chấm xếp "tương đương video faceless thông thường". **Chưa đạt "chuẩn điện ảnh cao nhất"** mà dự án đặt ra.
- **Xem liền mạch mù (Q31):**
  - điểm nối **J05 (04→05) bị cả 3/3 coi là gãy** → đây là lỗi nghiêm trọng;
  - lượt sửa duy nhất đã dùng cho một lỗi nghiêm trọng khác (§5.2), nên J05 **chưa sửa**, chờ chủ dự án quyết (§10, D2).
- **Chi phí:**
  - API $1,28 (trần $40);
  - ElevenLabs: phiên gửi 17 009 ký tự;
  - giờ máy ≈ 18 giờ đồng hồ (riêng cảnh 3D 1080p SPP4 là 11 giờ 36 phút).

## 1. Bước 1 — Giọng
Mẫu mù cùng đoạn 277 ký tự (móc + miễn trừ), `eleven_multilingual_v2`, tốc độ 1,00. Tệp: `k2g-ep01/giong/`.

| Giọng | Từ/phút (đo) | Ước cả tập | Clarity / Trust / Fit — L1 | L2 | L3 |
|---|---|---|---|---|---|
| **A · Eric** | **151,2** | ≈ 17,1 phút | 8/8/8 | 8/8/8 | 8/8/8 |
| B · Matilda | 131,2 | ≈ 19,7 phút (vượt 18) | 8/7/4 | 8/7/4 | 8/7/5 |
| C · River | 146,7 | ≈ 17,6 phút | 7/6/6 | 7/6/6 | 7/6/7 |

- **Kết quả:** **Eric thắng 3/3.** Đạt ≥ 144 từ/phút nên **không cắt ~80 từ dự phòng**, không cần REVIEWER.
- **Giới hạn đã nêu:** Claude API không nghe được âm thanh. "Người nghe" chấm trên số đo (tốc độ, cao độ, khoảng lặng, LUFS, ASR) và ảnh phổ/cao độ. Cả 3 người chấm đều ghi rằng không đánh giá được âm sắc. Chủ dự án nên nghe thử 30 s đầu của master.
- **Kiểm ASR toàn bộ lời:** mọi số và tên riêng khớp (`vo/asr-check.json`).

**Bộ đếm ElevenLabs (tài khoản):**
- Các lần đọc: 64 152 (trước mẫu) → 64 518 → 71 284 (sau thu lời) → 71 790 → **77 870** (12/10, 09:30).
- Phiên này gửi **17 009 ký tự**: mẫu 831 + lời 15 378 + Short 800. Bộ đếm tăng 13 718.
- Không có tệp lời nào thu lại sau 15:06 ngày 11/10 (đã kiểm thời điểm tệp), nên không có thu trùng.

## 2. Bước 2 — Nhạc, SFX, RIGHTS
- **Nhạc:** 4 bản Kevin MacLeod (incompetech), CC BY 4.0 (K2-MUS-1…4).
  - "Half Mystery": móc và kết (bài chủ đề, mở/đóng vòng);
  - "Beauty Flow": tầng 1;
  - "Tyrant": tầng 2;
  - "Sincerely": tầng 3.
  - Không lặp vòng; nhạc hạ 12 dB khi có lời.
- **SFX:** 15 bản ghi Work With Sounds / Sounds of Changes qua Europeana, CC BY 4.0 (K2-SFX-1…15). Tất cả là ghi âm thật trong nhà máy thép, cảng, đường sắt và tua-bin gió. Bản dài dùng 43 cue.
- **Đã kiểm điều cấm:** không có tài sản NC/ND, không dùng YouTube Audio Library.
- **`RIGHTS.md`:** có đủ giọng Eric (K2-V1) và font Inter OFL 1.1 (K2-F1). Mọi tệp có SHA-256.
- **Ghi công CC BY:** đã đưa nguyên văn vào mô tả phát hành.

## 3. Bước 3 — 8 bộ cảnh (`design/ll-hero/k2g01.js`)
- **Tám bộ cảnh:**
  - valley (thung lũng Braddock; khu lò cốc; sà lan; dùng 4 giờ trong ngày);
  - ingots (sa bàn thỏi thép 10 Mt);
  - chain (bản đồ tuyến theo lời Carnegie);
  - furnace (xưởng Bessemer);
  - trade (sa bàn thương mại);
  - **port** (mới: cảng thép + hải quan, cẩu giàn, xe tải, thanh chắn);
  - **mill** (mới: nhà máy hiện đại ban ngày, lò hồ quang, bãi phế, dây phôi nóng/nguội);
  - north (hydro, công trường Stegra).
- **Các điểm yếu G1 đã xử lý:**
  - Nhãn đọc được trên điện thoại: chữ cỡ tối thiểu **30 px** ở 16:9 (chữ hoa ≈ 22 px; LL Q6 yêu cầu 18 px), 46 px ở 9:16. Mọi chữ vẽ ở lớp 2D bám điểm neo của vật thể, không nướng vào ảnh 3D. Đo Q6 thấp nhất: **33,4 px**.
  - Vân vật liệu (gạch, tôn sóng, bê tông, gỉ) cho mặt nhà và nội thất. Bờ sông có kè đá, đá hộc, bến, sà lan, cây.
  - Dòng "Facts as of" và nhãn nguồn USGS/worldsteel có ở đoạn 00 và 13.
  - Đoạn 07, 08, 10: mỗi số neo có khung riêng. Dòng thời gian thuế là một đồ hoạ riêng. Số phụ đưa lên hình (phần còn lại của thế giới 101 / 1 767 Mt, tỷ lệ EAF 71 / 11 %, mốc 80 %).
- **Luật đa dạng bối cảnh** (`scripts/k2/settings.py`, bối cảnh tính theo cảnh 3D nền, kể cả nền mờ sau thẻ số): **đạt**.
  - Lớn nhất: valley 21,7 %, mill 20,2 % (trần 25 %).
  - Liên tục dài nhất: north 84,0 s (trần 90 s).
  - Nửa sau có 7 bối cảnh (cần ≥ 3).
  - Không chỉ số nào nằm trong ±5 % quanh ngưỡng.
- **Hạ tầng mới của kênh 2** (không sửa LL hay `checks/`): `scripts/k2/` gồm `prep.py`, `render.js`, `lib/k2.js`, `hero.js`, `heroes_par.sh`, `build.sh`, `settings.py`. Đặc tả nguồn là `k2g-ep01/ep-src.yaml`; `make_spec.py` ghép lời khoá v3.7 nguyên văn vào.

## 4. Bước 4 — Nháp → một lượt sửa → 1080p
- **Nháp 960×540:**
  - 37 cảnh 3D trong 88 phút;
  - 14 đoạn và 2 Short;
  - QC nháp (`qc-nhap.md`).
- **Một lượt sửa — 26 mục** (`SUA-NHAP.md`). Chính:
  - vân vật liệu tối gần đen do màu canvas bị chuyển sRGB→tuyến tính hai lần;
  - 6 máy quay bị khuất hoặc trôi khung;
  - bố cục thẻ (cột, mốc thời gian, danh sách, chữ đè cột);
  - thẻ trống > 3 s;
  - QC nháp: Q1 giữ khung ở Short, Q5 khung tối dần, Q7 nhãn ACTUAL, Q21 nguồn câu có năm, Q22 dòng nguồn tràn.
- **1080p:**
  - SPP4 sau khi đo: SPP2 2,68 s/khung, SPP4 4,15 s/khung trên cảnh nặng nhất. Khác biệt khi đứng yên nhỏ, nhưng SPP4 bớt nhấp nháy ở nét mảnh khi chuyển động;
  - 37 cảnh trong **11 giờ 36 phút** (3 tiến trình trên 4 lõi, setsid nohup);
  - ghép, trộn âm, master và Short trong 1 giờ 48 phút.

## 5. Bước 5 — QC + chấm mù một lần trên 1080p

### 5.1 QC nhà máy (`scripts/ll/qc.py`, luật LL áp dụng được; `k2g-ep01/qc-v1.md`)

| Mục | Kết quả |
|---|---|
| Q1 judder, Q2 khung trùng, Q3 máy xuyên hình | ĐẠT (0) |
| Q4 loudness | ĐẠT: master −14,0 LUFS / −1,6 dBTP; S1 −14,0 / −1,7; S2 −14,0 / −2,2 |
| Q5 tương phản chữ ≥ 4,5:1 | **TRƯỢT: 2,68** ở chữ cam "LAYER 3 · THE NEW ONE" trên nền trời ban ngày (đoạn 10, 2 s). Lỗi nhỏ, ghi lại, không dựng lại (theo lệnh) |
| Q6 cỡ chữ | ĐẠT: 33,4 px (ngưỡng 18) |
| Q7 nhãn ACTUAL/PROJECTION | ĐẠT (sau lượt sửa) |
| Q8 nguồn đọc toàn văn, số khớp lời | ĐẠT (0) |
| Q9 số khung | ĐẠT: 24 723/24 723 |
| Q10 Short ≤ 60 s | ĐẠT |
| Q11 khung trống > 3 s | ĐẠT (0) |
| Q13 số trên tiêu đề, mô tả, Short truy được về claim | ĐẠT (0) |
| Q19, Q20, Q22, Q24, Q25, LOCK | ĐẠT |
| Q21 dòng nguồn khớp câu đang hiện | ĐẠT (sau lượt sửa) |
| Q23 câu/thẻ nhiều số khác cơ sở | **TRƯỢT: 11.** Tất cả nằm ở **lời đã khoá** (06: USGS "raw" 1950 với worldsteel "crude" 2025; 07: các tuyên bố khác nhau). Không đổi lời. Trên hình ghi rõ "(USGS, raw steel)" / "(worldsteel, crude steel)"; mô tả có mục "Notes on the numbers". Đây là cảnh báo C02 của G1 |
| Q14–18, Q26–31 (luật nhịp LL, LL v3) | Bộ qc LL tự đánh "không áp" (tập ≤ 3 / ≤ 6). Q26b thay bằng luật bối cảnh K2 ở §3 |

**Kiểm claim:** mọi số trên hình và trong lời đều khai `num` (giá trị, loại, nguồn) hoặc `src` ở `episode.yaml`. Q8 đạt, Q21 đạt. Số mới chỉ có trên hình (101 Mt và 1 767 Mt) là phép trừ từ hai claim có nguồn (C26), có nhãn "OUR CALCULATION".

**Năm luật máy LUAT-G §7** (kiểm đọc, `luat_g7.py` → `luat-g7.json`):

| Luật | Kết quả |
|---|---|
| §1 | 0 cụm âm mưu |
| §2 | 0 câu gán động cơ cho nhóm |
| §4 | miễn trừ trong lời ở 0:18; dòng đầu mô tả có miễn trừ (đã chuyển lên dòng đầu ở bước đóng gói) |
| §5 | 0 câu "will" với thực thể chính trị hay công ty; 5 dòng as-of trên hình |
| §3 | 3 cặp huyền thoại/hồ sơ |

### 5.2 Lỗi nghiêm trọng đã sửa (lượt sửa duy nhất, trước khi chấm mù)
- **Cách phát hiện:** soát thứ tự shot sau QC 1080p.
- **Lỗi:** mốc `@by` (đoạn 08) khớp "by 2028" thay vì "By our calculation"; `@question` (đoạn 12) khớp "security question".
- **Hậu quả:**
  - thẻ số neo **131,2 Mt** không bao giờ hiện;
  - thẻ "our calculation" hiện sớm 8 s, khi lời còn nói số của OECD;
  - shot "a carbon price… it's a toll" bị mất.
- **Sửa:** đổi sang `@by#2` / `@question#2`, chỉ dựng lại 2 đoạn (56 phút). `prep.py` nay **chặn** shot sai thứ tự (BAI-HOC-K2 K4).
- **Kiểm sau sửa:** đã đọc lại khung đoạn 08 và 12.

### 5.3 Chấm mù một lần trên 1080p (`blind_k2.py`, `claude -p` với claude-sonnet-5-5, có ảnh, không subagent)
- **Khác giao thức K của LL:** kênh 2 chưa có tập tham chiếu, nên người chấm cho điểm tuyệt đối (thang 1–10 có mô tả: 5 = video faceless YouTube thông thường) và gắn cờ lỗi.
- **Q27 hình:** 12 khung ngẫu nhiên, `kiem-mu/blind/q27/`, khoá ở `key.json`.

| Người chấm | Tay nghề TB (min) | Đọc chữ TB | Tổng | So với faceless thường |
|---|---|---|---|---|
| R1 người xem phổ thông | 5,17 (4) | 6,36 | 5 | similar |
| R2 đạo diễn motion/3D | 4,92 (3) | 6,45 | 5 | similar |
| R3 biên tập phim tài liệu | 5,17 (4) | 6,36 | 5 | similar |

- **Cờ lặp lại:**
  - thẻ trống một nửa hoặc bị cắt khi chưa hiện đủ (F03, F05, F09, F11: 3/3);
  - tiêu đề cột ở F11 chạm mép thẻ;
  - phụ đề mảnh, chìm vào cảnh 3D (F01, F07, F12);
  - cảnh khối giản lược "phẳng", thiếu điểm nhìn chính (F02 bản đồ, F06/F07 sa bàn).
- **Đề xuất chung của cả 3 người chấm:**
  - thẻ co theo nội dung;
  - nền đậm sau phụ đề;
  - ít thẻ trên nền mờ hơn, nhiều cảnh 3D rõ nét hơn;
  - vật liệu và ánh sáng giàu hơn.

**Q31 liền mạch** (13 điểm nối, mỗi điểm 6 khung + lời quanh điểm nối; 4 tấm tổng quan 1 khung/8 s):

| | Đồng nhất | Đa dạng | Hình khớp lời | Điểm gãy |
|---|---|---|---|---|
| R1 | 7 | 5 | 6 | J05, J08, J09 |
| R2 | 6 | 5 | 6 | J05, J06, J09 |
| R3 | 6 | 5 | 6 | J05, J09 |

- **J05 (04→05) — 3/3 gãy → lỗi nghiêm trọng, chưa sửa:**
  - câu "the marker records what that cost at Homestead" nằm trên shot thùng thép lỏng;
  - sau đó thẻ "March 1901" trống khoảng 3 s khi lời đã nói về Morgan.
  - Lý do chưa sửa: lệnh cho phép **tối đa một lượt sửa** và lượt đó đã dùng ở §5.2.
  - Đề xuất sửa (khoảng 30 phút máy, không dựng lại cảnh 3D): shot cuối đoạn 04 hiện lại thẻ bia di tích thay cho thùng thép; mốc thời gian 1901 hiện mục đầu ngay khi vào thẻ. Xem D2.
- **J09 — 2/3:** chữ mờ chồng qua điểm cắt; hình nhà máy chung chung cho câu về Nippon/U.S. Steel. Lỗi nhỏ, ghi lại.
- **J06, J08 — 1/3:** lỗi nhỏ.
- **"Lạm dụng":** cả 3 người chấm nêu thẻ tối trên nền mờ, chiếm khoảng một nửa các tấm tổng quan. Luật bối cảnh đạt vì tính theo cảnh nền; người xem thì thấy "thẻ" là một bối cảnh riêng. Đây là bài học quan trọng nhất của tập (đề xuất D4).

## 6. Bước 6 — Gói phát hành (`k2g-ep01/phat-hanh/`)
- **Video** (ngoài git, `/var/tmp/cine-out/k2g-ep01/`): `k2g-ep01-v1-master.mp4` (1080p, crf 16, 1 347 459 087 byte), `shorts/k2g-ep01-short-S1.mp4`, `-S2.mp4`. SHA-256 ở `SHA256SUMS.txt`.
- **Phụ đề:** `k2g-ep01.en.srt` sinh từ căn chỉnh lời của chính master.
- **Mô tả:** `description.en.txt` gồm:
  - dòng đầu là miễn trừ + "Facts as of 11 October 2026";
  - 14 chương theo timeline thật;
  - 22 nguồn có URL và ngày truy cập;
  - "Notes on the numbers" (khác cơ sở, dự báo, CBAM không nhân với cường độ);
  - ghi công CC BY đầy đủ.
- **3 tiêu đề dạng câu hỏi tìm kiếm** (`titles.txt`; brief kiểm: 0 cảnh báo):
  1. Why Is Steel Guarded Like a Weapon? Who Controls the Path (57 ký tự)
  2. Is American Steel Dying? What 1950 vs 2025 Really Shows (55)
  3. Who Really Controls Steel? Tariffs, a Golden Share, a Carbon Toll (65)
- **PACKAGING-BRIEF.md** (`toolkit/market/brief.py`) và **3 ảnh nền 1280×720 không chữ** lấy từ khung cảnh 3D 1080p chưa phủ chữ: lò cao về đêm, cọc thỏi 1950/2025, cổng hải quan chạng vạng.
  - Chữ thumbnail đề xuất: `GUARDED LIKE A WEAPON?`.
  - Chưa có hồ sơ cầu cho chủ đề này (vòng đo ngách 12/10).
  - **Không làm thumbnail hoàn chỉnh** (theo §13).
- **2 Short:**
  - S1 "1950 vs. 2025: why is steel guarded like a weapon?" — lời móc + câu trả lời của đoạn 13, nguyên văn lời khoá.
  - S2 "Does Washington now own U.S. Steel?" — đoạn golden share nguyên văn. **Sai lệch nhỏ:** bỏ chữ "second" ("A second popular claim" → "A popular claim") vì Short đứng một mình. Không thêm thông tin mới.

## 7. Mục tiêu đo 7 ngày (THI-DIEM §2, số YouTube Studio)

| Chỉ số (ngày 1–7) | Mục tiêu | Sàn | Việc khi dưới sàn |
|---|---|---|---|
| CTR hiển thị | ≥ 4,0 % | 2,5 % | đổi thumbnail trước, tiêu đề sau; đo lại sau 48 giờ |
| Tỷ lệ xem trung bình | ≥ 35 % (≈ 6 phút) | 25 % | xem đường giữ chân; nếu rơi > 30 % trong 0:30 đầu thì sửa móc ở tập sau |
| Giữ chân ở 0:30 | ≥ 70 % | 55 % | như trên |
| Lượt xem/ngày | ≥ 140 (≈ 1 000/7 ngày) | 30 (≈ 210/7 ngày) | không đổi đề tài vì một tập; ghi nguồn lưu lượng |

Với Q27 tay nghề 5/10, tôi đánh giá giữ chân **có rủi ro dưới mục tiêu**. Một tập không đủ để kết luận về kênh.

## 8. Chi phí đo thật

| Hạng mục | Số |
|---|---|
| API G2 (`kiem-mu/cost-g2.jsonl`) | **$1,28**, 12 lượt (vòng mù v3.7, 3 người nghe giọng, Q27 ×3, Q31 ×3); trần $40 |
| Token phiên P (log phiên G1 + G2, khử trùng theo mã tin nhắn) | sinh 0,56 triệu; ghi cache 4,95 triệu; đọc cache 158,3 triệu |
| ElevenLabs | phiên gửi 17 009 ký tự; bộ đếm tài khoản 64 152 → 77 870 (+13 718) |
| Giờ máy | cảnh nháp 1,5 giờ; ghép nháp + Short 1,5 giờ; **cảnh 1080p 11,6 giờ**; ghép 1080p 1,8 giờ; dựng lại 08/12 0,9 giờ; QC, thử khung ≈ 0,7 giờ → **≈ 18 giờ đồng hồ** (3 tiến trình trên 4 lõi) |
| Đĩa | `/var/tmp/cine-out`: master 1,35 GB; khung cảnh 1080p ≈ 6 GB (xoá được sau khi duyệt) |

## 9. Sai lệch và bài học
- **Sai lệch:**
  - chấm mù dùng thang tuyệt đối (không có tập tham chiếu kênh 2);
  - S2 bỏ chữ "second";
  - bỏ 3 phần xem 720p (gói phát hành kênh 2 không yêu cầu);
  - J05 3/3 chưa sửa (đã dùng hết lượt sửa);
  - hai lần dùng lõi thứ tư cho tiến trình thử khung vài phút trong lúc 3 tiến trình dựng đang chạy.
- **BAI-HOC-K2 thêm:**
  - K4: mốc "@từ" khớp lần đầu → máy chặn shot sai thứ tự;
  - K5: màu canvas trong three.js mới.
- **Đề xuất ghi BAI-HOC (chờ duyệt):** luật đa dạng bối cảnh tính theo cảnh nền chưa đủ. Q31 cho thấy người xem coi "thẻ trên nền mờ" là một bối cảnh riêng.

## 10. Việc đang chờ chủ dự án
- **D1. Cho phép mở nhánh phát hành `release-k2g-ep01-v1` (Git LFS):** master, 2 Short, `.srt`, mô tả, SHA256SUMS. Như LL tập 8: P tải ngược và kiểm SHA.
- **D2. Lỗi J05 (3/3 gãy liền mạch)** — chọn một:
  - (a) cho thêm một lượt sửa đoạn 04–05 (≈ 30 phút máy, không dựng lại cảnh 3D);
  - (b) chấp nhận và ghi lại.
  - Tôi đề xuất (a): rẻ, sửa đúng chỗ cả 3 người chấm cùng nêu.
- **D3. Đánh giá chất lượng:** Q27 = 5/10 ("tương đương faceless thường") chưa đạt chuẩn điện ảnh cao nhất. Đề xuất cho tập sau, không làm lại tập này:
  - giảm thẻ trên nền mờ xuống ≤ 25 %; số đặt trong cảnh 3D rõ (nhãn bám vật thể như đoạn 00, 05);
  - thẻ co theo nội dung;
  - nền đậm sau phụ đề;
  - vật liệu PBR và ánh sáng giàu hơn cho port/mill;
  - bản đồ có nhãn địa danh.
  - Ưu: tăng điểm hình. Nhược: thêm giờ dựng cảnh. Rủi ro: SwiftShader chậm hơn (đã đo 4,2 s/khung SPP4).
- **D4. Ghi bài học** "bối cảnh tính cả thẻ" vào BAI-HOC kênh 2 và đề nghị K bổ sung vào luật Q26b cho kênh 2.
- **D5. Duyệt gói phát hành** (tiêu đề, mô tả, brief, 2 Short); chủ dự án tạo 2–3 thumbnail theo PACKAGING-BRIEF.
- **D6. Ghi `AUTHORSHIP.md`** cho quyết định G2 sau khi chủ dự án duyệt.
- **Đã kiểm, không có việc chờ:** trạng thái as-of được tra lại lúc 11/10 21:30, không đổi. Nên tra lại một lần nữa ngay trước khi đăng (LUAT-G §5).
