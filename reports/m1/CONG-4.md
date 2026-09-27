# CỔNG 4 — CỔNG MẶT IDA + ANIMATIC "Last Round" (M1)

Phiên P · 27/09/2026 · nhánh `claude/cine-lab-m1-cong4-animatic` (tạo từ `main` c21e5df) · **KHÔNG merge**.
Đầu phiên: `bash scripts/env/verify.sh` → 10 PASS, 0 FAIL.
- `checks/lock.py --verify` → KHỚP (`144b3cff…`).
- `sha256sum -c design/cong3/LOCK-THIET-KE.sha256` → 24/24 OK.
- Không sửa `checks/`, không đọc mã trong `checks/` (chỉ đọc RUN.md).

## 0. Kết luận nhanh

| Việc | Kết quả |
|---|---|
| Khoá Cổng 3 | Đã merge vào `main` (c21e5df) và khoá SHA thiết kế (xem phiên trước). |
| **Việc 1 — cổng mặt Ida** | **CHƯA ĐÓNG.** Đạt: tuổi 3/3, cảm xúc 2/3, không ai nói "mặt chết" hay "mắt trống". **Chưa đạt chặt: giới tính** — cả 3 đều nghiêng về "bà cụ" nhưng nói "không chắc", ở cả 2 lần. Đã chỉnh 1 lần (tối đa 2). Nguyên nhân còn lại cần đổi thiết kế đã khoá → quyết định A. **Không sang Cổng 6.** |
| **Việc 2 — animatic** | **Xong.** 48 shot, 2:30,00, 960×540, 24 fps, 1 mẫu, không DOF. Âm tạm đủ. Phụ đề tiếng Anh cháy vào hình. Gói chiếu mù sẵn: `screening/animatic.mp4` (47,85 MB) và `screening/questions.json`. |
| Checks (`--profile shot`) | **TRƯỢT**. ĐẠT 11, TRƯỢT 2 (G3b, H1b), THIẾU 1 (C3), không áp dụng 2 (N3, M1). Nguyên văn ở mục 3.5. |

## 1. Việc 1 — cổng mặt Ida

### 1.1 Đã làm
- **Mặt biến dạng** (`design/cong3/v2/char3d/cast3d.js`): trường dịch chuyển mềm trên đỉnh lưới đầu, áp SAU khi gán UV trung tính. Nhờ vậy lớp vẽ tay C′ bám theo lưới. Các vùng biến dạng:
  - khoé miệng (lên/xuống, ra ngoài khi cười);
  - gò má nâng;
  - môi mím;
  - cằm đẩy lên;
  - đầu trong và đuôi lông mày, kéo mày vào giữa;
  - trán giữa;
  - mí trên sụp và mí dưới nâng — xoay quanh tâm nhãn cầu nên nhãn cầu không xuyên mí.

  Pháp tuyến = gradient SDF + (lưới sau − lưới trước), nên không có vệt nối. Lông mày sợi 3D dịch theo cùng trường này. Nét vẽ (`facepaint.js`, `o.mesh`):
  - nét có vị trí (mày, mi, khoé, rãnh mũi–má) vẽ ở chỗ trung tính;
  - chỉ giữ theo biểu cảm: ngấn nước, nước mắt, nếp cười, nếp cằm, nếp giữa mày.
- **Bỏ vệt tím ở má:** vá shader riêng cho da đầu. Nơi ánh sáng tới da nghiêng lạnh (trời, viền), sắc ánh sáng kéo về xám ấm (70 %). Ánh đèn khí ấm không đổi.
  - Nguyên nhân cũ: đèn viền lạnh `#9aa0e8` rọi vào nửa tối của má.
  - Thay đổi này áp cho mọi lần render sau. Style frame a2p đã khoá giữ nguyên làm tham chiếu, không render lại.
- **Cử chỉ đẩy mũ (C4 có động cơ):**
  - Mũ có bản lề ở mép sau băng mũ (`pose.hat_back`).
  - Ida dùng **tay trái** (phía máy) đẩy vành lên; tay phải để dành cho van. Tư thế trong `IDA_POSES_C4` (`design/cong3/v2/shots.js`).
  - Ảnh: `reports/m1/cong4/kiem-mu-mat/lan2_cu-chi_truoc.jpg` và `lan2_cu-chi_sau.jpg`.
- **Góc gần chính diện:**
  - Ở cột đèn, lồng kính che mặt nếu máy đặt thẳng trước mặt.
  - Cách giải: Ida quay đầu 35° nhìn lên phố (hợp kịch bản 1:50: bà chào con phố). Máy lệch 10° khỏi hướng mặt.

### 1.2 Kiểm mù: nguyên văn trong `reports/m1/cong4/kiem-mu-mat/lan1.md` và `lan2.md`
Cách hỏi:
- Mỗi ảnh gửi cho một subagent MỚI, không có bối cảnh. Tên file trung tính.
- Câu hỏi đúng nguyên văn: "Người này bao nhiêu tuổi, giới tính gì, đang cảm thấy gì?"
- Ảnh: 1920×1080, 3 mẫu.

**Lần 1** (mũ đẩy hết, `hat_back = 1`):
- *Trung tính (x7):* "Một người già, khoảng 70 đến 80 tuổi… Tôi nghiêng về một bà cụ, khoảng 60–70% chắc chắn… tóc ngắn chải ngược nên nhìn cũng có thể là một ông cụ… đang trầm ngâm, có chút buồn hoặc lo lắng… khuôn mặt hơi cứng, giống búp bê. Vì vậy cảm xúc đọc được nhưng chưa thật "sống"."
- *Cười buồn (k2):* "một bà cụ, chừng 70 đến 80 tuổi… Tôi đoán là nữ chủ yếu nhờ gương mặt hiền và cách ăn mặc, chứ không có dấu hiệu nào thật rõ, nên cũng có thể là một ông cụ. Bà đang buồn mà vẫn cố mỉm cười… Mặt và cổ trông hơi dài, như một con rối."
- *Nghẹn (m4):* "một người già, chắc khoảng 70 đến 80 tuổi… Giới tính thì tôi không chắc lắm… nghiêng về bà cụ, khoảng 60%. Về cảm xúc thì rõ là buồn, đau lòng, như đang cố nén để không khóc… nhân vật trông hơi giống con rối hoặc búp bê. Cổ rất mảnh so với cái đầu to, mặt nhẵn như sáp."

**Chỉnh lần 1** (chỉ dàn dựng và biểu cảm, không đổi thiết kế khoá):
- mũ đẩy 35 % để vành vẫn ôm mặt;
- biểu cảm lệch hai bên (cười buồn 0,3; nghẹn 0,2);
- mắt có điểm nhìn.

**Lần 2:**
- *Trung tính (p3):* "Người này đã lớn tuổi, tôi đoán khoảng 60 đến 70… Tôi nghiêng về một bà cụ, nhưng không chắc lắm… kiểu tóc cắt ngắn bên dưới mũ cũng hợp với một ông cụ. Tôi chỉ chắc khoảng 60 đến 65% là nữ… có vẻ đang trầm ngâm, hơi buồn hoặc bâng khuâng, pha chút lo lắng… Phần má, cằm và miệng gần như đứng yên, trông hơi giống mặt nạ."
- *Cười buồn (r8):* "một người già, chắc khoảng 70 tuổi hoặc hơn… Tôi đoán nghiêng về một bà cụ… nói là ông cụ cũng không sai… Tôi đọc ra một nỗi buồn nhẹ, kiểu bồi hồi nhớ lại chuyện cũ: vừa thương vừa tiếc, cười mà vẫn buồn."
- *Nghẹn (t5):* "Một người già, tôi đoán khoảng 70 tuổi, có thể hơn… Giới tính: Tôi không chắc chắn. Nhìn thoáng qua thì tôi nghiêng về một bà cụ… Người này đang buồn, đau lòng, như đang cố nén khóc… Trên má trái của nhân vật có một vệt nước mắt mờ."

| Tiêu chí | Lần 1 | Lần 2 |
|---|---|---|
| 3/3 đọc ra bà lão | Tuổi 3/3. Giới tính: 3/3 "bà cụ" nhưng **không chắc** | Như lần 1 |
| Cảm xúc đúng ≥ 2/3 | **2/3** (cười buồn, nghẹn; trung tính → "trầm ngâm, hơi buồn") | **2/3** (như lần 1) |
| Không có "mặt chết" hay "mắt trống" | Không có hai chữ đó; có "búp bê/con rối" ở cả 3 ảnh | Không có hai chữ đó; "búp bê/con rối" không còn ở r8 và t5; p3 (trung tính): "hơi giống mặt nạ" |

**Kết luận:** chưa đạt chặt ở tiêu chí giới tính.
- Nguyên nhân: ở góc gần chính diện, **búi tóc** (dấu hiệu nữ trong model sheet) bị đầu che. Phần tóc lộ dưới vành mũ đọc thành "tóc cắt ngắn".
- Không dùng lần chỉnh thứ 2, vì dàn dựng không sửa được nguyên nhân này. Muốn sửa phải đổi thiết kế đã khoá → **quyết định A**.
- Cổng mặt để mở; không sang Cổng 6.

## 2. Việc 2 — animatic 2:30

### 2.1 Shot list: `shots/animatic/SHOTLIST.md` (sinh từ `design/cong4/animatic/film.js`) + `shots/animatic/shots.json`
- **48 shot, 150,0 s.** Tiêu cự 21–200 mm (tương đương 35 mm). Mỗi shot có:
  - cỡ, góc, tiêu cự, chuyển máy, thời lượng;
  - thoại/âm, nguồn sáng trong truyện, hành động, lý do chọn.

| Cảnh | Thời gian | Số shot |
|---|---|---|
| 1 Vòng đèn | 0:00–0:26 | 8 |
| 2 Bật điện | 0:26–0:44 | 6 |
| 3 Chạy đua | 0:44–1:08 | 10 |
| 4 Bức tường | 1:08–1:34 | 8 |
| 5 Ngọn cuối | 1:34–2:10 | 10 |
| 6 Ô cửa | 2:10–2:30 | 6 |

- **Luật 180° và hướng nhìn:**
  - Quảng trường và đồng hồ ở phải khung, nhà kho ở trái. Ida đi phải → trái suốt cảnh 1–3; sóng trắng tới từ phải.
  - Cảnh 4–5: máy luôn ở sau-phải; Ida trái, Cas phải. Cận L3 chụp qua vai phải Cas, vẫn cùng phía đường nối.
  - Cận L4: Ida nhìn lên phố (phải khung). Cas (s38) nhìn lên.
  - Match cut 8B: hai mặt đồng hồ cùng vị trí, cùng cỡ.
- **Tư thế then chốt:**

  | Tư thế | Shot | Thời điểm |
  |---|---|---|
  | Hơ tay đếm ba | s05, s24 | 0:12, 1:06 |
  | Chim bóng | s25, s32, s48 | 1:08, 1:31, 2:25 |
  | Cảnh 5: hai cái bóng | s33 (style frame c_s5_wide), s34 | 1:34, 1:42 |
  | Đẩy mũ | s36 | 1:48 |
  | Tắt ngọn cuối | s40 | 2:04 |
  | Cas hơ tay | s42 | 2:07 |

  Bảng 48 khung: `reports/m1/cong4/animatic_48-shot.jpg`.
- **Sai khác previs so với thiết kế khoá** (ghi trong SHOTLIST):
  - phố thẳng, phẳng (bản khoá cong, dốc);
  - cảnh 3 là montage nén thời gian;
  - đồng hồ bỏ túi, cột đồng hồ và phòng Cas là đạo cụ/bối cảnh previs, chưa có trang thiết kế;
  - **không có khẩu hình**;
  - một số tư thế ngoài sheet.

### 2.2 Previs — dựng bằng tài sản 3D đã khoá
`design/cong4/animatic/`. Tài sản dùng lại:
- nhân vật C′ (cast3d);
- cột đèn khí (props.js);
- cột điện, mặt tiền, cửa sổ, đá lát, trời vẽ (street.js);
- thang, đèn lồng (cast.js);
- cảnh s1 (toàn cảnh thành phố: chạng vạng / sóng trắng / đêm), s5 (hốc cửa), s6 (ngõ);
- bố cục b_cas_bird (tường chim bóng).

Thông số render: 960×540, 1 mẫu, không DOF, lớp vẽ C giữ nguyên, grain chung. Mỗi shot dựng trong một trang Chromium riêng, để s1 (sửa ShaderChunk sương) và s5/s6 (uniform dùng chung) không nhiễm chéo.

### 2.3 Âm tạm: `design/cong4/animatic/audio/mix.py`
- **Thoại:** take L1–L4 của **table read nháp 2**. Đây là bản chủ dự án đã nghe và duyệt ở Cổng 2 ("4 câu thoại rõ và tự nhiên"), nên **không cần A/B**. Đặt đúng mốc 12,0 / 60,0 / 88,0 / 110,0 s.
- **Room tone, rè điện, SFX:** **tổng hợp bằng mã** (không dùng mẫu ngoài):
  - "phụp" mồi đèn: 9,2 / 52,4 / 55,4 / 62,95 / 65,0 s;
  - tách rơ-le;
  - chuông điện 27,0 s;
  - gõ kính 16,9 và 17,3 s;
  - núm đồng hồ và tiếng gập;
  - van 124,2 s;
  - bước chân;
  - rè điện nhấp theo lịch bật cột điện.
- **Nhạc:** ACE-Step M0 `theme-dit-1.flac`, **ghi rõ NHẠC TẠM**, 3 đoạn: 0:00–0:24, 1:31–1:50, 2:07–2:30.
- **Mix:**
  - thoại −14 LUFS; cả phim −22,2 LUFS integrated; true peak −2,8 dBFS (4×);
  - nền hạ 8 dB khi có thoại;
  - stem FLAC 24-bit, tổng stem = mix.
- **RIGHTS.md:** thêm C4-D1, C4-M1, C4-S1, C4-F1 (font phụ đề DejaVu Sans, giấy phép Bitstream Vera).
- **`assets/LIBRARY.json`:** thêm 7 mục có SHA.

### 2.4 Gói chiếu mù
- **`screening/animatic.mp4`:**
  - 47,85 MB; bản sao y từng byte của `design/cong4/animatic/out/animatic.mp4` (SHA `e9d7b271…`);
  - H.264 2 pass 2 350 kb/s + AAC 192 kb/s;
  - 7 thẻ phụ đề tiếng Anh cháy vào hình, có hộp nền tối; mốc theo lời đo trên stem thoại.
- **`screening/questions.json`:**
  - (a) "Tell us the story in 2–3 sentences."
  - (b) 15 ô mốc 10 s để đánh dấu lúc mất tập trung, cộng ô ghi mốc tự do.
  - (c) "What did you feel at 0:40?", "…at 1:50?", "…at 2:07?"
  - (d) "Would you watch another film by this maker? (1–5)"

  Không câu nào nêu nhân vật, sự kiện hay cảm xúc. Có hướng dẫn cho người xem và cho chủ nhà.
- **Lưu ý về mốc c1:** đề bài ghi 0:48 cho "phố trắng", nhưng trong kịch bản nháp 2 và animatic:
  - sóng trắng tới Ida lúc **0:40** (s13), và 0:42–0:44 là cảnh bà giơ tay trên nền không bóng;
  - 0:48 là nhịp so hai mặt đồng hồ.

  Tôi đặt câu hỏi ở 0:40 và ghi chú trong file → **quyết định B**.

## 3. Checks — `/opt/cine/bin/python checks/run.py design/cong4/animatic/out/animatic.mp4 --profile shot`

### 3.1 Kết quả lần cuối (nguyên văn)
```
[   PASS] N1 24 fps CFR; không rơi hay lặp khung theo PTS
[   PASS] N2 BT.709 đủ 3 trường; dải limited — đo cả nhãn lẫn giá trị điểm ảnh
[    N/A] N3 Codec và bitrate đúng loại master; khung 16:9, SAR 1:1
[   PASS] P0 Máy dò chữ độc lập: mọi chữ trong hình phải có matte
[   PASS] P1 Không chữ đè chữ, tính theo điểm ảnh nét chữ
[   PASS] G4 Chữ tương phản ≥ 4,5:1 (WCAG AA), đo điểm ảnh
[   PASS] G3 Không banding trên gradient
[   FAIL] G3b Grain cố định: có grain, ổn định theo thời gian và giữa các shot, chuyển động theo khung
[    N/A] M1 Master YouTube: −14 LUFS ±1; true peak ≤ −1 dBTP
[   PASS] M3 Tương quan pha và tương thích mono
[   PASS] J1 Mọi từ trong kịch bản nghe rõ trên bản mix cuối
[   PASS] J1b Lời rõ trên nhạc theo từng câu, đo từ stem thoại và stem nền
[   PASS] H1 Không chuyển động tuyến tính ở bộ phận nhân vật
[   FAIL] H1b Chuyển động khai báo khớp hình render (luồng quang học ở vùng nhân vật)
[MISSING] C3 Đúng model: tỷ lệ bộ phận so với model sheet, có tính nhiễu đo
[   PASS] O3 Mọi tài sản lấy từ thư viện có SHA
VERDICT: TRƯỢT
```
Báo cáo đầy đủ: `reports/checks/animatic/animatic.checks.{md,json}` (LOCK khớp `144b3cff…`).

**Chỉ số nằm trong ±5% quanh ngưỡng** (chép từ báo cáo):
- G3b — σ grain nhỏ nhất theo shot: 0.799 (ngưỡng 0.8).

### 3.2 Lần 1 và các sửa giữa hai lần chạy
Lần 1 (lưu ở `reports/m1/cong4/checks-lan1/`) có 5 TRƯỢT: G4, G3b, M3, J1b, H1b. Tôi sửa **lỗi thật** của bản dựng, không thêm phần tử nào chỉ để vượt ngưỡng:

| Luật | Lần 1 | Nguyên nhân (của tôi) | Sửa | Lần cuối |
|---|---|---|---|---|
| G4 | 1,19:1 | Phụ đề trắng viền mảnh đặt trên phố trắng (cảnh 3–5), không đọc được | Hộp nền tối gần đục sau chữ (kiểu phụ đề có hộp tiêu chuẩn) | 14,13:1 ĐẠT |
| M3 | 2,77 % cửa sổ < −0,3 | Nhạc tạm ACE-Step có đoạn ngược pha (tới −0,74 ở 15,6 s). Đo từng stem: thoại, room tone, SFX sạch | Thu hẹp độ rộng stereo của nhạc còn 35 % (M/S); room tone gom về giữa | 0 % ĐẠT |
| J1b | cửa sổ 0,155 (61,0 s) | Tôi đặt tiếng "phụp" của L10 GIỮA câu "Not yet… not yet.", sai kịch bản ("The lamp catches" đứng sau câu) | Dời L10 bắt lửa sang 62,95 s (render lại s22–s23); hạ nền 8 dB dưới thoại | 0,81 ĐẠT |
| H1b | 67 track toàn null; track tệ nhất 0 % | Track tay lấy ở khớp cổ tay (mép tay áo); kiểm che khuất cho phép thân nhân vật che tới 0,2 m | Lấy điểm giữa lòng bàn tay; kiểm che khuất chặt (0,06 m); bỏ track toàn null. Xuất lại bằng lượt chỉ-cập-nhật: góc khớp, gốc, máy trùng 100 % với lúc render (3600/3600 khung) | Vẫn TRƯỢT (mục 3.3) |

### 3.3 Ba luật chưa đạt
- **H1b:**
  - 86 track đo được: **70 đạt ≥ 90 %; 16 trượt, đều là track BÀN TAY**. Mọi track đầu đều đạt.
  - Các chỗ lệch lớn nhất là cử động rất nhanh, vượt khả năng của luồng quang học: tay Cas hạ xuống 118 px/khung ở s29; tay Ida ở s03, s18.
  - Các chỗ còn lại là tay nhỏ vài pixel ở 540p, hoặc vung qua thân khi đi (s02, s07, s35).
  - 1 track không có cặp khung kề nào đo được.
  - Tôi dừng sau một lần sửa độ chính xác dữ liệu. Tinh chỉnh tiếp để ép qua ngưỡng sẽ là lách luật. Luật sẽ đo lại ở bản render thật (1080p).
- **G3b:**
  - Bản nộp (47,85 MB): σ nhỏ nhất 0,799 (**±5 %**), CV 0,211 ✗, tỷ lệ σ giữa shot 2,69 ✗, tương quan khung kề 0,868 ✗.
  - **Đối chứng** CRF 14 (198 MB, không nộp, không commit; báo cáo ở `reports/checks/animatic_hq_doi-chung/`): σ 1,15 và CV 0,168 đạt, nhưng tỷ lệ σ 2,15 ✗ và tương quan 0,73 ✗.
  - Kết luận: trần 50 MB làm grain yếu thêm, nhưng nguyên nhân chính nằm ở previs:
    - vân canvas và nét cọ tĩnh của lớp vẽ đọc thành "grain đứng yên";
    - tham số lớp vẽ khác nhau theo bộ cảnh ở 540p.

    Việc này xử lý ở render hoàn thiện, không chỉnh previs để qua luật.
- **C3: THIẾU.**
  - Animatic không xuất mặt nạ bộ phận 4× (48 shot, 3600 khung, 2 nhân vật).
  - Luật C3 đang có khiếu nại phụ thuộc tư thế/góc (B-i) → **chờ K v1.4**. P chưa đầu tư xuất mặt nạ cho previs trước khi K sửa luật.
- J1 **ĐẠT**: 100 % từ, WER 0 %. Không cần ghi "chờ K".

## 4. Thời gian render thật và số lần làm lại

| Việc | Đo thật | Làm lại |
|---|---|---|
| Cổng mặt: 5 ảnh/lần (1920×1080, 3 mẫu) | Lần 1: 8,8–9,2 s/ảnh; lần 2: 8,3–9,1 s/ảnh | Test nhanh 1 mẫu (960 và 640 px) — tổng ~24 khung. **Lỗi của tôi:** quên tham số `char:"3d"` nên 3 ảnh đầu dựng nhầm module nhân vật cũ. Lồng đèn che mặt 2 lần; tư thế đẩy mũ 3 vòng. **Kiểm mù 2 lần, chỉnh 1 lần.** |
| Animatic toàn phim (3600 khung) | **2 701 s (45 phút)**; TB 0,72 s/khung; dựng cảnh ≤ 2,9 s/shot. Chậm nhất là cảnh tường 1,0–1,2 s/khung (2 đèn điểm có bóng) | — |
| Soát bằng probe (3 khung/shot) | Vòng 1: 48 shot 338 s; vòng 2: 16 shot 107 s; vòng 3: 10 shot 66 s; vòng 4: 4 shot 25 s | 4 vòng. Lỗi đã sửa: máy nằm sau dãy nhà; phơi sáng; insert đồng hồ bị tay che; máy s31 sau gáy; s24 lệch khung; chim đèn lồng nhạt; đèn sát máy cháy sáng; mắt phát sáng. **Chú thích `//` nuốt `scene.add(L)` ở phòng Cas** (s48 đen; lỗi lặp lại từ Cổng 3) — đã quét toàn bộ, không còn chỗ nào khác |
| Render lại có chọn lọc | s42: 72 khung, 50 s (Cas đè chân cột đèn → đặt lại, thêm đèn lồng). s22–s23: 144 khung, 104 s (L10 bắt lửa sau câu thoại) | 2 lần, chỉ phần đổi, rồi ghép vào video |
| Xuất lại chuyển động (không render) | 3600 khung, 177 s | 1 |
| Âm | ~40 s/lần trộn | 7 lần (độ to; FLAC; ưu tiên lời; nhạc M/S; dời "phụp") |
| Đóng gói (2 pass + phụ đề) | ~180 s/lần | 5 lần. Lần đầu CRF 16 ra 148 MB, vượt trần → chuyển sang 2 pass |
| Checks | 175 s/lần | 3 lần trên bản nộp + 1 lần đối chứng |

## 5. Quyết định cho chủ dự án

### A — Cổng mặt: giới tính đọc do dự (nguyên nhân: tóc nhìn từ trước như tóc ngắn, búi bị khuất)
| | A1: thêm dấu hiệu nữ nhìn được từ trước (vài lọn tóc mềm thoát khỏi búi ở thái dương/gáy, và đôi khuyên tai nhỏ bắt sáng); sửa `bible/characters.md` → v1.2, khoá SHA lại | A2: giữ thiết kế; dựa vào dàn dựng (có búi trong các shot 3/4 và nghiêng) và giọng nói để đọc giới tính; chấp nhận ảnh chính diện đọc do dự | A3: đổi kiểu tóc lớn hơn (mái/tóc buông trước trán) |
|---|---|---|---|
| Ưu | Sửa đúng nguyên nhân; thay đổi nhỏ, ít rủi ro cho silhouette đã duyệt | Không đụng thiết kế khoá; không tốn thêm | Đọc nữ chắc nhất |
| Nhược | Mở lại khoá thiết kế (SHA characters.md) | Tiêu chí "3/3 bà lão" không đạt chặt; cổng mặt vẫn mở | Đổi hình ảnh nhân vật đã duyệt; silhouette mũ + tóc thay đổi |
| Tác động | Thêm 1 vòng kiểm mù (3 ảnh). Có thể đóng cổng mặt trước Cổng 6 | Chủ dự án phải hạ tiêu chí hoặc đóng cổng bằng quyết định | Làm lại model sheet, C3/B1, style frame |
| Rủi ro | Thấp: vẫn có thể đọc do dự nếu lọn tóc quá nhỏ ở cận | Khán giả nhầm giới tính ở cận mặt đầu tiên (0:12) | Cao: trễ tiến độ, lệch model sheet |
| **Khuyến nghị** | **A1** | | |

### B — Mốc câu hỏi (c) cho "phố trắng"
| | B1: giữ **0:40** (lúc sóng trắng tới Ida, s13) | B2: đổi về **0:48** như đề bài | B3: hỏi cả 0:40 và 0:48 |
|---|---|---|---|
| Ưu | Hỏi đúng khoảnh khắc chủ dự án muốn đo | Đúng chữ đề bài | Có cả hai số đo |
| Nhược | Khác chữ đề bài | 0:48 là nhịp so đồng hồ, không phải phố trắng → đo nhầm khoảnh khắc | Thêm câu hỏi; người xem mỏi, dễ trả lời qua loa |
| Tác động | Không | Sửa 1 dòng `questions.json` | Sửa 1 mục |
| Rủi ro | Thấp | Kết quả c1 không dùng được cho mục đích ban đầu | Thấp |
| **Khuyến nghị** | **B1** | | |

### C — Bước tiếp theo của animatic
| | C1: chiếu mù NGAY bản này cho 3–5 người xem thật (chủ dự án tổ chức, dùng `questions.json`) | C2: trước khi chiếu, sửa previs: phố cong/dốc đúng s1, rig miệng nói cho 4 câu thoại, tư thế ngoài sheet đưa vào sheet | C3: bỏ qua chiếu mù, sang Cổng 5 (layout) |
|---|---|---|---|
| Ưu | Đo sớm câu chuyện và nhịp khi sửa còn rẻ; đúng mục đích animatic | Người xem ít bị phân tâm bởi môi không mấp máy | Nhanh nhất |
| Nhược | Previs thô (không khẩu hình, grain yếu) có thể kéo điểm (d) xuống | Tốn thêm một vòng dựng; khẩu hình là việc của Cổng 6+ | Không có số đo người xem thật cho cấu trúc truyện |
| Tác động | Dữ liệu (a)–(d) quyết định có cắt, đổi nhịp cảnh 3 (montage) và cảnh 6 hay không | Lùi chiếu mù 1 vòng | Rủi ro sửa cấu trúc muộn |
| Rủi ro | Thấp | Trung bình (tiến độ) | Cao |
| **Khuyến nghị** | **C1** | | |

## 6. Việc đang chờ chủ dự án
1. Xem `screening/animatic.mp4`, chọn **A / B / C**.
2. **Cổng mặt Ida: CHƯA ĐÓNG** (quyết định A). Không sang Cổng 6.
3. Nếu chọn C1: tổ chức chiếu mù 3–5 người, gửi lại câu trả lời nguyên văn.
4. **Chờ K v1.4:**
   - khiếu nại C3 (tư thế/góc);
   - gộp hai khiếu nại vòng 3 đã chấp nhận.
5. **Tồn đọng đã biết:**

   | Hạng mục | Chi tiết |
   |---|---|
   | Ánh mắt s26 | Mắt Ida còn sáng nhẹ (đèn lồng ở thắt lưng rọi từ dưới) |
   | Mặt Ida (Cổng 6) | "Mặt nhẵn như sáp", "cổ mảnh" — hai nhận xét của người xem mù; thuộc chất lượng mặt, xử lý ở Cổng 6 |
   | Âm | Tiếng cười khẽ của Cas và hơi thở cười của Ida chưa có SFX có giấy phép — để trống |

## 7. File
- **Mã:**
  - `design/cong4/animatic/{page.js, film.js, sets.js, sets2.js, util.js, render_film.js, package.py, make_shotlist.py, audio/mix.py}`;
  - `design/cong4/mat/run_mat.sh`;
  - sửa `design/cong3/v2/char3d/{cast3d.js, facepaint.js}`, `design/cong3/v2/shots.js`.
- **Sản phẩm:**
  - `screening/animatic.mp4`, `screening/questions.json`;
  - `design/cong4/animatic/out/animatic.mp4`, kèm file đi kèm cho checks: `.script.txt`, `.text/`, `.stems/`, `.motion.json`, `.assets.json`;
  - `shots/animatic/SHOTLIST.md`, `shots/animatic/shots.json`;
  - `reports/m1/cong4/`: kiểm mù, bảng 48 shot, checks lần 1.
- **Không commit** (tái tạo được):
  - `design/cong4/animatic/out/video.mp4` (hình trung gian, 187 MB);
  - `design/cong4/animatic/out/hq/` (đối chứng 198 MB).
