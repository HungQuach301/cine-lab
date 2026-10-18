**Nhánh thật: `casting-my`** (đúng như lệnh; tạo từ `origin/main` @ `6c16e548`, rồi `git merge --no-ff origin/claude/casting-giong-contested-places-3zz7fo`: merge này chỉ thêm `reports/`). Đã đẩy, **không merge**.

# CASTING-MỸ — thử giọng Mỹ, trầm, kịch tính hơn cho "Contested Places", so với G1 đã chọn — DỪNG

> Phiên CASTING-MỸ, 18/10/2026 (lệnh chủ dự án 18/10 23:36, phương án A). Chỉ tạo/sửa `reports/casting-my/**` và tệp này. Không sửa `channel-*/`, `scripts/`, `design/`, `checks/`, `docs/`. Đã đọc: `reports/CASTING-GIONG-BAO-CAO.md` (cách làm, §1, §6), `reports/casting-giong/giay-phep.md` (dùng lại, không đọc thêm URL), `doan-thu.json`, `phat-am-thu.json`, `thiet-ke.json`, `khoa-ten.json`, `reports/m3/BAI-HOC-LL.md`. `scripts/env/verify.sh`: 9 ĐẠT, 5 TRƯỢT (OpenEXR, three.js, tifffile/pyshp, k2v node_modules, Freesound). Không mục TRƯỢT nào dùng trong phiên này; ElevenLabs, faster-whisper, librosa, ffmpeg ebur128 đều ĐẠT.

## Khối điều lệ (lệnh + thực tế)
| Trường | Lệnh | Thực tế |
|---|---|---|
| Nhánh | `casting-my` từ `origin/main` + merge `casting-giong` | đúng (dòng đầu) |
| Tệp được sửa | `reports/casting-my/**` + tệp này, ≤ 10 MB, không LFS | đúng; `reports/casting-my/` ≈ 6,0 MB (gói nghe 5 × 1,17–1,27 MB); không LFS |
| ElevenLabs | theo dõi 3 000; **chặn 5 000 ký tự gửi** | **4 970 ký tự gửi** (vượt mốc theo dõi, dưới mức chặn 30 ký tự). Mức chặn được cài thành mã (`my_lib.tts` từ chối gửi khi tổng chạm 5 000). Bộ đếm tài khoản **131 238 → 133 536 (+2 298)** (§5) |
| Claude | theo dõi $2; chặn an toàn $10 | Claude API (`claude -p`) **$0**; không dùng subagent. Token phiên chính không đo được trong phiên, nên không tự khai |
| OpenAI / YouTube | 0 / 0 | **0 / 0** |
| Preflight / email / khoá | bắt buộc; che email; không để email vào header/URL/payload/UA | `tools/preflight.sh` chạy trước mỗi commit: **ĐẠT**, `lock.py --verify` **KHỚP**. Không có email trong tệp ghi hay trong header/URL/payload nào. Tải preview Voice Library dùng UA `CineLab-research (+https://github.com/HungQuach301/cine-lab)`. Khoá do proxy gắn; không đọc, không in |
| Dừng | không dừng hỏi giữa chừng | đúng |

**Vượt mốc theo dõi 3 000 ký tự, lợi ích:** đây là số tối thiểu để làm đúng lệnh: 4 giọng × 2 đoạn khoá (1 192 ký tự sau alias) = 4 768, cộng 2 lần Voice Design × 101 ký tự. G1 dùng lại bản thu cũ (0 ký tự). Vì phần dư dưới mức chặn chỉ còn 30 ký tự, phiên này **không thu lại** chỗ nào và **không thu bảng phát âm 40 mục** (xem §1, "Giới hạn").

---

## 0. Tóm tắt (đọc 2 phút; không nêu tên giọng)
1. **Gói nghe mù sẵn sàng:** `reports/casting-my/nghe-mu/M1.mp3 … M5.mp3`, mỗi tệp dài 1:23–1:30. Mỗi tệp gồm 2 đoạn nguyên văn của lời khoá: móc mở đầu 0a–0e và pin nổi 13/9/1782 2k–2n. Mọi tệp ở **−13,9 … −14,1 LUFS**, đỉnh thật **≤ −1,7 dBTP**, MP3 112 kb/s, cùng một chuỗi xử lý giọng. Thứ tự M sinh ngẫu nhiên bằng `secrets` (Fisher–Yates). Tên giọng chỉ có trong `reports/casting-my/khoa-ten.json`. Hướng dẫn, đường dẫn mở trên điện thoại và phiếu chấm 1–10 có năm tiêu chí (thêm **"kịch tính vừa đủ (không phóng đại)"**) ở `reports/casting-my/HUONG-DAN-NGHE.md`. **Trong 5 tệp có 1 tệp là G1, giọng đã chọn, làm đối chứng.**
2. **4 ứng viên mới, cả 4 đạt máy kiểm và vào gói:** 2 giọng tạo bằng Voice Design (2 mô tả nam Mỹ lớn tuổi, trầm, phim tài liệu điện ảnh; máy chọn 1 trong biến thể 1–2 của mỗi mô tả) và 2 giọng Voice Library (nam Mỹ lớn tuổi, nhãn narrative, thời hạn báo trước 730 ngày, hệ số phí 1,0, đăng 2024–2025). **Không giọng nào bị loại vì phát âm.**
3. **Máy kiểm (cả 5 tệp):** cả hai cách nghe ASR đều đúng **mọi năm và số** (fourteen, 1309, 1783, July 2026; four, forty-seven, fifty, ten, 1782, 10:25, 400, 2 000, 357). Tỷ lệ từ đúng **95,5–98,0 %** so với lời khoá; phần lệch giống nhau ở mọi giọng là cách ASR viết "Duc de Crillon" và "d'Arçon". Không tên nào sai ở cả hai cách nghe. Hai tệp có tên "nghi" (chỉ một cách nghe nhận ra), §1.
4. **Thời lượng:** sau hiệu chỉnh (§1), 3 giọng mới vừa bảng shot T3 hiện tại ở speed 1,0. Một giọng mới cần speed ≈ 1,035 (phim ước +3,1 % so trần 721,2 s nếu giữ speed 1,0). Đối chứng G1 giữ nguyên như casting: speed ≈ 1,068 (+6,1 %).
5. **Trầm hơn G1 là số đo thật:** ba trong bốn giọng mới có F0 trung vị **65,6–73,6 Hz**; G1 trên cùng hai đoạn là 94,9 Hz. Giọng mới còn lại ở 92,8 Hz. Còn "kịch tính vừa đủ" và "đáng tin" thì máy không đo được, phải dựa vào tai.
6. **Quota:** bộ đếm hiện là **133 536 / 171 534**, đặt lại 01/11/2026. **Giới hạn kỳ hôm nay đọc được là 171 534, khác số 144 034 trong báo cáo casting**; phiên này chưa xác minh được lý do. Nếu tính theo giới hạn cũ thì còn 10 498, theo giới hạn mới thì còn 37 998. Cả hai đều trên mức phải giữ ≈ 7 000 cho lượt thu T3 (lượt đó cần ≈ 6 000 bộ đếm, như nhau với mọi giọng).

**Chỉ số nằm trong ±5 % quanh ngưỡng:**
| Chỉ số | Đo | Ngưỡng | Lệch |
|---|---|---|---|
| ElevenLabs gửi | 4 970 | chặn 5 000 | **−0,6 %** |
| Phim T3 ước, M1 | 720,6 s | trần 721,2 s | −0,1 % (lời 668,9 s so khung 668 s: +0,1 %, speed cần 1,001) |
| Phim T3 ước, M4 / M5 | 719,7 s | 721,2 s | −0,2 % (vừa bảng shot hiện tại) |
| Lời T3 ước, M4 | 664,8 s | khung lời 668 s | −0,5 % (dư 3 s) |
| Phim T3 ước, M3 | 743,3 s | 721,2 s | **+3,1 %** (cần speed ≈ 1,035) |
| Loudness M4, M5 | −13,9 LUFS | dải đạt −15,0…−13,8 | cách cận trên 0,1 LU |

**Việc chờ chủ dự án:** §7.

---

## 1. Bảng máy kiểm theo mã mù (chi tiết: `reports/casting-my/may-kiem.json`)
> **Hãy nghe và chấm gói mù trước khi đọc mục này.** Số đo ở đây (nhất là cột thời lượng, có thể so với báo cáo casting) đủ để đoán tệp nào là đối chứng.

Hai cách nghe theo BAI-HOC #86: **M** = faster-whisper `medium.en` beam 5, **S** = `small.en` beam 1; cả hai không dùng hotwords. Lời gốc so sánh là lời khoá (số được chuẩn hoá thành chữ). "Sai" = cả hai cách nghe đều không nhận ra; "nghi" = chỉ một cách nghe nhận ra.

| Mã | Từ đúng M / S | Số, năm sai (nghi) | Tên trong đoạn sai (nghi) | Từ/giây (móc · pin) | Lời T3 ước (thô → hiệu chỉnh) | Phim T3 ước · lệch trần | speed cần | F0 trung vị (p10–p90) | LUFS / dBTP / LRA | Thời lượng tệp |
|---|---|---|---|---|---|---|---|---|---|---|
| M1 | 98,0 % / 98,0 % | 0 | 0 | 2,257 (2,23 · 2,27) | 696,1 → 668,9 s | 720,6 s · −0,1 % | 1,001 | 73,6 Hz (62–98) | −14,0 / −2,2 / 3,0 | 85,4 s |
| M2 | 98,0 % / 97,5 % | 0 | 0 (d'Arçon) | 2,116 (2,25 · 2,06) | 742,4 → 713,4 s | 765,1 s · **+6,1 %** | 1,068 | 94,9 Hz (51–145) | −14,1 / −2,4 / 4,0 | 90,5 s |
| M3 | 96,5 % / 95,5 % | 0 | 0 (Duc de Crillon, d'Arçon) | 2,183 (2,24 · 2,16) | 719,7 → 691,6 s | 743,3 s · **+3,1 %** | 1,035 | 65,6 Hz (50–78) | −14,0 / −2,1 / 2,8 | 88,4 s |
| M4 | 98,0 % / 96,0 % | 0 | 0 | 2,271 (2,30 · 2,26) | 691,8 → 664,8 s | 719,7 s · −0,2 % | 1,0 | 92,8 Hz (70–129) | −13,9 / −1,7 / 2,9 | 85,1 s |
| M5 | 98,0 % / 97,5 % | 0 | 0 | 2,313 (2,34 · 2,30) | 679,2 → 652,7 s | 719,7 s · −0,2 % | 1,0 | 70,3 Hz (55–105) | −13,9 / −2,2 / 2,9 | 83,4 s |

**Cách đọc các cột:**
- **Từ đúng** = 1 − (thay + bỏ + chèn)/số từ của lời khoá (2 đoạn, 65 + 135 = 200 từ sau chuẩn hoá). Đoạn móc đúng 100 % ở mọi giọng và cả hai cách nghe. Phần lệch chung ở đoạn pin: "de Crillon" bị ASR viết "du Creon", "d'Arçon" thành "d'Arson"/"Darcon" (cả hai đều là cách viết của đúng âm *dar-sohn*), "attackers'" thành "attacker's". Phần lệch riêng: S nghe "the thirteenth of September" thành "thirteen September" ở M3 và M4 (M nghe đúng). Ở M3, M nghe "Their answer to" thành "there answered a" trên bản thô; trên tệp gói thì nghe đúng. Chỗ này ở khoảng 0:41 của M3, nên nghe kỹ.
- **Tên "nghi"**: ở M2, M nghe "d'Arçon" thành "Darcon"; khớp mờ với "dar-sohn" chỉ đạt < 0,75 do cách tách chữ của bộ so, chứ không phải đọc sai. Ở M3, S nghe "Duke du Creon" (Duc ≈ "Duke" là đúng âm) và "d'Arson". **Không có lỗi phát âm nào phải loại giọng.** Alias Đ3 `dar-sohn` (chữ thường) được đọc ra đúng âm ở cả 4 giọng mới.
- **Lời T3 ước**: lấy 1 571 từ viết của lời khoá chia cho tốc độ đo trên 2 đoạn ("thô"). Hai đoạn này **đọc chậm hơn trung bình cả lời**, vì đoạn pin nổi có nhiều chỗ ngừng. Bằng chứng: G1 đo trên 3 đoạn ở casting ra 2,202 từ/s (lời 713,4 s), nhưng trên 2 đoạn này chỉ ra 2,116 từ/s (742,4 s). Vì vậy phiên này nhân mọi giọng với cùng một hệ số **0,961** (= 713,4 / 742,4), giả định tỷ lệ nhịp giữa các đoạn như nhau ở mọi giọng. Sai số ước khoảng ±5 %, vì 2 đoạn chỉ dài khoảng 1,5 phút.
- **Phim T3 ước** = 719,667 + max(0, lời − 668), và **speed cần** = lời/668, như casting (KHOA-LOI-41 §3).
- **F0** đo bằng pyin trên bản nối 2 đoạn chưa xử lý; F0 thấp hơn nghĩa là giọng trầm hơn. Cột này chỉ để tham khảo, quyết định là ở tai.
- **LRA** (dải độ to) 2,8–4,0 LU. Tệp có LRA cao hơn có nhịp to/nhỏ thay đổi nhiều hơn; đây là một dấu hiệu của cách đọc kịch tính, nhưng không thay được tai.

**Giới hạn của phiên (vì giữ trần ký tự):**
- Không thu bảng phát âm 40 mục. Bốn alias Đ3 không có trong 2 đoạn (Elliot, fet ah-kom-plee, la lee-nay-ah, mon-tair-oh) **chưa được thử trên 4 giọng mới**. Ở casting, cả 4 alias này đúng 8/8 giọng, nên rủi ro thấp; nhưng phải kiểm lại khi thu T3 (ASR toàn tập của BIBLE §10).
- Chỉ có 1 lượt thu mỗi giọng, nên chỗ vấp có thể là ngẫu nhiên.

**Đối chứng G1:** không thu lại (0 ký tự). Phiên này cắt 0–90,40 s của `reports/casting-giong/nghe-mu/G1.mp3` (đoạn 1 + đoạn 2), với ranh giới tìm bằng dấu thời gian ASR và `silencedetect`. Có hai khác biệt đã biết so với 4 ứng viên: (a) chữ gửi đoạn 2 của G1 dùng alias cũ `dar-SOHN`, ứng viên dùng `dar-sohn`, còn lại trùng từng ký tự; (b) nguồn G1 đã qua xử lý loudness của gói casting một lần.

**Chuỗi xử lý gói nghe (giống nhau cho cả 5 tệp, `nghe_mu.py`):** nguồn ứng viên được mã hoá MP3 112 kb/s một lần để cùng thế hệ với G1 (G1 vốn là MP3 112 kb/s). Sau đó: gain tuyến tính về −20 LUFS → chuỗi giọng của kênh (`scripts/audio/master.py` `vo_chain`: highpass 70 Hz, deesser, nén −24 dB 2,5:1) → gain tới −14 LUFS → lên stereo không suy hao → giới hạn đỉnh trên tín hiệu nâng mẫu 192 kHz (trần −2 dBFS) → MP3 112 kb/s. Cuối cùng đo `ebur128` trên chính tệp phát hành.
- **Đã bỏ lượt đầu**, dùng chuỗi cũ của casting (gain + alimiter), vì hai lỗi: (1) một giọng ra rất nhỏ (−30 LUFS mono, đỉnh/độ to ≈ 25 dB), nên alimiter phải nén khoảng 10 dB; (2) tệp đối chứng ở 192 kb/s, dung lượng gấp đôi, làm lộ đối chứng. Lượt đầu chưa commit và chưa ai nghe; thứ tự M được sinh lại.
- Ở chuỗi mới, giọng đó vẫn cần giới hạn đỉnh nhiều nhất trong 5 tệp: đỉnh trước limiter +5,4 dBFS, 3 ‰ số mẫu vượt trần; các tệp khác ≤ 0,6 ‰. Tức là limiter chỉ cắt tức thời ở các đỉnh, không nén cả câu. Tệp đó vẫn nên được nghe kỹ xem có bị bẹt không.
- Vì có thêm chuỗi giọng của kênh, G1 trong gói này nghe hơi khác (dày hơn) so với G1 trong gói casting. Cả 5 tệp được xử lý như nhau, nên so sánh vẫn công bằng.

## 2. Ứng viên và cách chọn (tên thật chỉ có trong `khoa-ten.json`, `thiet-ke.json`, `thu-vien.json`)
| Nhóm | Ứng viên | Cách chọn |
|---|---|---|
| A. Voice Design | 2 mô tả (`thiet-ke.json`): A1 *"A deep, older American male narrator in his sixties for a cinematic historical documentary. Dramatic yet measured, rich low voice with a slight gravel. Credible and grounded, never a movie-trailer announcer…"*; A2 *"An older American man with a deep, resonant voice. Serious war-documentary narrator with controlled intensity, unhurried and grave, General American accent. Not exaggerated, not an advertisement…"* | Model `eleven_multilingual_ttv_v2` (như casting), seed 18102026, guidance 5. Chữ thử 101 ký tự: 2 câu nguyên văn của 2m/2n. API trả 3 biến thể cho một lần tính phí; **theo lệnh chỉ xét biến thể 1–2** (biến thể 3 lưu ngoài git, không xét). Máy chọn theo: (1) tỷ lệ từ đúng cao nhất, lấy giá trị thấp hơn của 2 cách nghe; (2) nếu bằng nhau thì lấy F0 thấp nhất. Ở cả hai mô tả, cả hai biến thể đều đạt 100 %, nên F0 quyết định: A1 chọn v2 (69,5 Hz, so với v1 91,7 Hz), A2 chọn v2 (80,3 Hz, so với v1 82,2 Hz). Lưu vào tài khoản: `CINE-CastingMy-A1-v2`, `CINE-CastingMy-A2-v2` (0 ký tự) |
| B. Voice Library | 2 giọng nam Mỹ lớn tuổi | `/v1/shared-voices` (male, old, american, en; từ khoá documentary, narrator, history, deep) cho ra 57 giọng. Lọc thời hạn báo trước **730 ngày** (tối đa), hệ số phí **1,0**, use case narrative/informative: còn 35 giọng. Phiên chọn tay 10 giọng để tải preview công khai (0 ký tự): đăng trước 01/12/2025, mô tả không phải vai nhân vật. Từ 10 giọng này, máy lấy 2 giọng có F0 preview thấp nhất, bỏ giọng có mô tả "Motivational" vì rủi ro thành giọng quảng cáo. Hai giọng được chọn đăng **02/2024** và **07/2025**. Dùng trực tiếp, không lưu vào tài khoản. Bảng sàng đầy đủ ở `thu-vien.json` |
| Đ. Đối chứng | G1 = A2 của casting, giọng đã chọn | dùng lại bản thu (§1) |

Cấu hình đọc giống nhau cho mọi giọng mới: `eleven_multilingual_v2`, stability 0,5, similarity 0,75, speed 1,0, giống cấu hình G1 ở casting. Alias được áp vào chữ trước khi gửi; mỗi đoạn là một lệnh gửi riêng.

## 3. Điều khoản (dùng lại `reports/casting-giong/giay-phep.md`, đọc ngày 18/10/2026; phiên này không đọc thêm URL)
- **Voice Design:** *"The only charge for using voice design is the number of credits to generate your preview text"*. Phiên này đo được bộ đếm tăng đúng 202 cho 202 ký tự, tức hệ số 1,0 (khác TTS ≈ 0,44). Giọng thiết kế chỉ nằm trong tài khoản, không đưa lên Library được. **Chưa có câu nào ghi rõ ai sở hữu voice model đã thiết kế** (CHƯA XÁC MINH). Tính năng được gọi là *"still experimental"* và **chưa rõ** có thuộc Beta Services Addendum hay không; addendum này cấm dùng thương mại. Vấn đề này giống hệt G1, vì G1 cũng là giọng Voice Design.
- **Voice Library:** thời hạn báo trước tối đa 2 năm: *"any Outputs generated … prior to the end of the Notice Period will continue to exist and remain available for use thereafter"*. Muốn giữ quyền 730 ngày thì phải thêm giọng vào tài khoản trước khi chủ giọng gỡ. Giọng Library không độc quyền: *"others may be able to generate Output"*.
- **Dùng thương mại:** gói hiện tại (Creator) có giấy phép thương mại và không bắt ghi công.
- **Ngày hết hạn:** giọng Default hết hạn 31/12/2026. **Không giọng nào trong 5 tệp là giọng Default**, nên mốc này không áp dụng cho các giọng ở đây.

## 4. Rủi ro riêng
**4.1. Kịch tính làm giảm "đáng tin".** Mục tiêu "kịch tính" đi ngược một phần với nguyên tắc "ghi nguồn từ cả hai phía" của series: giọng nghe như tuyên bố có thể làm khán giả nghi rằng phim thiên lệch. Có ba dấu hiệu cần để ý khi nghe: nhấn mạnh ở câu trung tính ("by the British count, fifty by the Spanish"), hạ giọng thì thầm ở số liệu, hoặc kéo dài ở "It was refused."
- Phiếu chấm tách riêng "đáng tin" và "kịch tính vừa đủ" để thấy được đánh đổi này.
- Sau khi đăng T3, chỉ số §10.1 của BIBLE (bình luận chê giọng hoặc chê AI ≤ 2 %) là thước đo thật.
- Trong phim, nhạc nền sẽ cộng thêm kịch tính. Một giọng nghe "vừa" khi đọc khô có thể thành "quá" khi có nhạc.

**4.2. Theo nguồn giọng** (không gắn với mã M):
| Nguồn | Bị gỡ / hết hạn | Điều khoản | Trùng kênh khác |
|---|---|---|---|
| A. Voice Design (2 giọng mới, và cả G1) | chỉ mình xoá được; phụ thuộc tài khoản ElevenLabs; không có ngày hết hạn đã công bố | quyền với voice model **chưa ghi rõ**; nhãn "experimental" (CHƯA XÁC MINH có tính là Beta không) → **nên hỏi ElevenLabs bằng văn bản trước khi bán phim** (Đ5 của casting, vẫn còn chờ) | thấp: chỉ có trong tài khoản này |
| B. Voice Library (2 giọng mới) | chủ giọng gỡ được; ta còn 730 ngày nếu đã thêm giọng vào tài khoản; ElevenLabs có thể gỡ *"with or without notice"*; audio đã tạo vẫn dùng được | VLA; cả hai giọng cho phép cả người dùng free | **một giọng cực cao: 466 825 lượt thêm**, rất phổ biến trên YouTube, nên khán giả dễ đã nghe ở kênh khác. Giọng còn lại: 7 736 lượt thêm |

**4.3. Thời lượng:** một giọng mới cần speed ≈ 1,035; G1 cần ≈ 1,068. Với speed > 1,05, nhịp "unhurried" có thể mất. Giọng chọn mà cần speed thì phải nghe lại 1 đoạn ở speed mới trước khi thu cả tập (≈ 1 200 ký tự).

**4.4. Âm thanh:** một giọng Library ra mức rất nhỏ và có đỉnh nhọn (đỉnh/độ to ≈ 25 dB), nên phải giới hạn đỉnh nhiều hơn các giọng khác. Trong sản xuất, chuỗi `master.py` xử lý được việc này, nhưng nên nghe kỹ chỗ có âm bật (p, t, k).

**4.5. Ước ký tự lượt thu T3 với từng giọng:** **như nhau ở cả 5 giọng.** Lý do: cả 5 cùng hệ số phí 1,0 (Voice Design khi đọc TTS và Library hệ số 1,0), cùng model `eleven_multilingual_v2`, và tham số speed không đổi giá.
- Ước: ≈ 9 919 ký tự lời sau alias × 1,3 (thu lại) ≈ **12 900 ký tự gửi**, làm bộ đếm tăng **≈ 5 700** (tỷ lệ TTS đo phiên này 0,440; casting 0,44–0,47).
- Nếu chọn giọng cần speed: cộng ≈ 1 200 ký tự gửi (≈ 530 bộ đếm) cho lượt nghe thử ở speed mới.
- Nếu đổi giọng: cộng thêm 1 lượt kiểm 4 alias Đ3 chưa thử (≈ 185 ký tự).

**4.6. Quota còn lại sau phiên này:** bộ đếm **133 536**, đặt lại 01/11/2026 06:57 UTC.
- Theo giới hạn đọc hôm nay (171 534): còn **37 998**.
- Theo giới hạn 144 034 của báo cáo casting: còn **10 498**.
- Cả hai trường hợp đều đủ 1 lượt thu T3 (≈ 5 700–6 300 bộ đếm) và vẫn giữ trên mức 7 000 mà lệnh yêu cầu, **với điều kiện giới hạn đúng là 171 534**. Nếu giới hạn đúng là 144 034, sau lượt thu T3 còn ≈ 4 500, nên không đủ cho lượt thứ hai trước 01/11. Chủ dự án nên xem trang Subscription để biết vì sao giới hạn đổi (nạp thêm hay đổi gói).

## 5. Chi phí thật
| Hạng mục | Số |
|---|---|
| ElevenLabs gửi (`reports/casting-my/nhat-ky-ky-tu.jsonl`, 10 dòng) | **4 970 ký tự**: Voice Design 2 × 101 = 202; TTS 4 giọng × (385 + 807) = 4 768. G1: 0. Tải preview Library: 0. Lưu 2 giọng thiết kế: 0 |
| Bộ đếm tài khoản | trước **131 238** → sau Voice Design 131 440 (+202, tỷ lệ 1,00) → sau TTS **133 536** (+2 096, tỷ lệ 0,440). Tổng **+2 298** (0,462 ký tự/ký tự gửi). Bộ đếm không tăng nhiều hơn log (BAI-HOC #98) |
| Claude API (`claude -p`) | **$0** (không gọi). Không dùng subagent. Token phiên chính không đo được |
| OpenAI / YouTube | 0 / 0 |
| Giờ máy | ≈ 30 phút (ASR 2 cách nghe × 5 giọng × 2 đoạn ≈ 12 phút; sàng preview; dựng gói 2 lượt) |
| Tài khoản ElevenLabs | thêm 2 giọng thiết kế vào My Voices (`CINE-CastingMy-A1-v2`, `CINE-CastingMy-A2-v2`). Giọng không được chọn có thể xoá sau khi chủ dự án chấm |

## 6. Đề xuất
**Đ1. Quyết định bằng nghe mù M1–M5, trong đó G1 có mặt như một ứng viên (khuyến nghị).**
- Ưu: so trực tiếp với giọng đã chọn trong cùng điều kiện, nên giữ hay đổi đều có căn cứ. Cả 5 giọng đều đạt chữ và số.
- Nhược: chỉ có 2 đoạn, khoảng 1,5 phút mỗi giọng, và 1 lượt thu mỗi giọng.
- Tác động: nếu giữ G1 thì không đổi gì. Nếu đổi thì phiên P sửa BIBLE-KENH2 §4 và AUTHORSHIP.
- Rủi ro: tai bị cuốn theo giọng kịch tính nhất trong lần nghe đầu. Phiếu chấm tách "đáng tin" và "kịch tính vừa đủ" để giảm rủi ro này.

**Đ2. Luật chọn khi điểm sát nhau:** nếu một giọng mới chỉ hơn G1 dưới 1 điểm trung bình, **giữ G1**.
- Ưu: không đổi giọng vì khác biệt nhỏ. G1 đã qua đủ kiểm 47 mục phát âm ở casting.
- Nhược: có thể bỏ lỡ một giọng hợp series hơn.
- Rủi ro: thấp.

**Đ3. Nếu chọn giọng mới:**
- (a) Thu 1 lượt kiểm 4 alias Đ3 còn lại (≈ 185 ký tự).
- (b) Nếu giọng cần speed: nghe lại 1 đoạn ở speed mới (≈ 1 200 ký tự).
- (c) Nếu là giọng Library: thêm giọng vào tài khoản ngay, để khoá quyền dùng 730 ngày.
- (d) Nếu là giọng Voice Design: cùng câu hỏi điều khoản với G1 (Đ5 casting).
- Ưu: chặn rủi ro trước khi thu T3. Nhược: thêm ≈ 1 400 ký tự gửi.

**Đ4. Không xét giọng có lượt thêm rất cao cho phim bán**, trừ khi tai chấm nó hơn rõ (≥ 1,5 điểm "không AI" và "hợp thể loại").
- Ưu: giữ nhận diện riêng của series.
- Nhược: loại một giọng nghe quen tai.
- Rủi ro: thấp.

## 7. Việc chờ chủ dự án
1. **Nghe mù 5 tệp** `reports/casting-my/nghe-mu/M1.mp3 … M5.mp3` theo `reports/casting-my/HUONG-DAN-NGHE.md` (trang đó có đường dẫn GitHub mở trên điện thoại; nghe bằng tai nghe; chấm 1–10 năm tiêu chí, gồm **"kịch tính vừa đủ (không phóng đại)"**). Rồi **chọn: giữ G1 hay đổi sang giọng mới**. Chưa mở `khoa-ten.json`.
2. Duyệt Đ2 (luật giữ G1 khi điểm sát nhau) và Đ4 (giọng phổ biến).
3. Xem vì sao giới hạn ký tự ElevenLabs là 171 534 (báo cáo casting ghi 144 034), để biết quota thật cho lượt thu T3.
4. Vẫn còn chờ từ casting: Đ3 (sửa alias trong từ điển khoá) và Đ5 (hỏi ElevenLabs bằng văn bản về quyền với giọng Voice Design). Đ5 áp dụng cho cả G1.

## 8. Tệp
`reports/casting-my/`:
- `HUONG-DAN-NGHE.md`, `nghe-mu/M1–M5.mp3`: gói nghe mù.
- `khoa-ten.json`: **chỉ mở sau khi chấm**.
- `may-kiem.json`: theo mã M, không có tên; đọc sau khi nghe.
- `doan-thu.json`: 2 đoạn, chữ khoá và chữ gửi, alias Đ3.
- `thiet-ke.json`, `thu-vien.json`: có tên và nguồn giọng; không mở trước khi chấm.
- `nhat-ky-ky-tu.jsonl`: có mã nội bộ; không mở trước khi chấm.
- Công cụ: `my_lib.py` (dùng lại `casting-giong/cg_lib.py`, `kiem_lib.py`; cài trần 5 000), `thiet_ke.py`, `chon_bien_the.py`, `luu_thiet_ke.py`, `doan_thu.py`, `thu.py`, `doi_chung.py`, `kiem.py`, `nghe_mu.py`, `tong_hop.py`.

Bản thu thô, preview và kết quả ASR đầy đủ nằm ngoài git ở `/var/tmp/cine-out/casting-my/` và mất khi container bị thu hồi. Thu lại đúng như vậy tốn ≈ 4 970 ký tự (các biến thể Voice Design có thể ra khác dù cùng seed).
