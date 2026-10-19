**Nhánh thật: `claude/casting-giong-contested-places-3zz7fo`** (harness buộc nhánh này thay cho `casting-giong` của lệnh; tạo từ `origin/main` @ `6c16e548`). Đã đẩy, **không merge**.

# CASTING-GIỌNG — giọng đọc mới cho series "Contested Places" (T3 Gibraltar trở đi) — DỪNG

> Phiên CASTING-GIỌNG, 18/10/2026. Chỉ tạo/sửa `reports/casting-giong/**` và tệp này. Không sửa `channel-*/`, `scripts/`, `design/`, `checks/`, `docs/`. Đã đọc: `channel-k2/k2c-t3-01/loi-khoa.txt` (SHA `0fdc72ce…` khớp), `khoa-loi/phat-am/` (47 mục alias), `KHOA-LOI-BAO-CAO.md` §0, `KHOA-LOI-41-BAO-CAO.md` §3 (thời lượng, trần 721,2 s), `docs/BIBLE-KENH2.md` §4 (âm thanh) và §10.1 (đo chê giọng ≤ 2 %), `reports/m3/BAI-HOC-LL.md`.

## Khối điều lệ (lệnh + thực tế)
| Trường | Lệnh | Thực tế |
|---|---|---|
| Nhánh | `casting-giong` từ `origin/main` | harness buộc `claude/casting-giong-contested-places-3zz7fo` (dòng đầu), gốc `6c16e548` = `origin/main` |
| Tệp được sửa | `reports/casting-giong/**` + tệp này, ≤ 15 MB, không LFS | đúng; tổng ≈ 12 MB (gói nghe 6 × 1,7–2,1 MB); không LFS |
| ElevenLabs | mốc 12 000 ký tự; dừng ở 30 000 | **25 627 ký tự gửi**: vượt mốc theo dõi, chưa tới mức dừng. Bộ đếm tài khoản tăng **+12 011** (§5) |
| Claude | mốc $2 | Claude API (`claude -p`) **$0**; 1 subagent đọc tài liệu: 198 209 token (§5) |
| YouTube / OpenAI | 0 / 0 | **0 / 0** |
| Preflight / email / khoá | bắt buộc; che email; không in hay ghi khoá | `tools/preflight.sh` chạy trước mỗi commit: **ĐẠT**, `lock.py --verify` **KHỚP**. Không có email trong tệp ghi hay trong header/URL/payload nào. Khoá do proxy gắn; không đọc, không in |
| Dừng | không dừng hỏi giữa chừng | đúng |

**Vượt mốc ElevenLabs 12 000 ký tự, lợi ích:** đoạn thử đúng các shot lệnh chỉ định dài **2 006 ký tự** sau alias (lệnh ước ≈ 1 200). Ngoài ra phải thêm bảng 40 mục để kiểm đủ 47/47 mục phát âm (847 ký tự/giọng), và một lượt thử alias thay thế (185 ký tự/giọng). Lượt alias thay thế đó chứng minh các lỗi phát âm chung là lỗi alias, không phải lỗi giọng.

---

## 0. Tóm tắt (đọc 2 phút; không nêu tên giọng)
1. **Gói nghe mù sẵn sàng:** `reports/casting-giong/nghe-mu/G1.mp3 … G6.mp3`, mỗi tệp khoảng 2:05–2:28. Mỗi tệp gồm 3 đoạn nguyên văn của lời khoá: móc mở đầu 0a–0e, pin nổi 13/9/1782 2k–2n, kết số liệu 5e–5i. Mọi tệp ở **−14,0 … −14,3 LUFS** và đỉnh thật **≤ −4,2 dBTP**. Thứ tự G sinh ngẫu nhiên bằng `secrets` (Fisher–Yates). Tên giọng chỉ có trong `khoa-ten.json`. Hướng dẫn nghe và phiếu chấm 1–10 ở `reports/casting-giong/HUONG-DAN-NGHE.md`. **Trong 6 tệp có 1 tệp đối chứng là giọng hiện tại của kênh.**
2. **8 ứng viên đã thu, lọc còn 6:** 3 giọng tạo bằng Voice Design (3 mô tả × 3 biến thể; máy chọn biến thể tốt nhất), 3 giọng Voice Library (nam lớn tuổi giọng Anh, nhãn narration/documentary, thời hạn báo trước 730 ngày, không tính phụ phí), 1 giọng sẵn có của ElevenLabs, và giọng đối chứng. Có 2 giọng bị loại vì làm **phim T3 vượt trần nhiều nhất** (+8,2 % và +10,1 %, §2). **Không giọng nào bị loại vì phát âm.**
3. **Máy kiểm (cả 6 giọng trong gói):** ASR nghe đúng **mọi năm và số** ít nhất ở một cách nghe. Tỷ lệ từ đúng **97,0–98,2 %**, so với lời khoá; phần lệch còn lại chủ yếu do ASR viết tên Pháp/Tây Ban Nha và "metres". Tên riêng trong đoạn thử: không có tên nào sai ở cả hai cách nghe.
4. **Phát âm 47 mục:** đạt **42–46/47** ở lượt đầu. Các mục sai **xuất hiện ở hầu hết hoặc mọi giọng**, nên là **lỗi của alias**: "EL-ee-ut" bị đọc thành chữ cái "E.L.", "fayt" bị đọc thành "fight", âm tiết viết hoa "LEE-neh-ah" ra "neha". Thử alias thay (chữ thường, chính tả tiếng Anh quen) cho kết quả: **Eliott → "Elliot" đúng 8/8 giọng; fait accompli → "fête accompli" 8/8; La Línea → "la lee-nay-ah" đúng 8/8.** Riêng *Cádiz* (chỉ là mục dự phòng, không có trong lời) bị ASR nghe thành "Cardiff" ở 4/8 giọng; mục này cần tai người. → Đề xuất sửa từ điển ở phiên khoá lời/âm thanh (§6, Đ3).
5. **Thời lượng là ràng buộc máy quan trọng nhất.** Bảng shot T3 (719,7 s) được dựng cho lời ≈ 668 s. Có 3 giọng trong gói đọc chậm hơn mức đó: hai giọng làm phim ước **≈ 763–765 s (+5,7 % / +6,1 % so trần 721,2 s)** nếu giữ tốc độ 1,0; giọng thứ ba **≈ 730 s (+1,2 %)**. Cách xử lý: tham số `speed` ≈ 1,015–1,07 của ElevenLabs, hoặc giãn bảng shot (§2). Ba giọng còn lại vừa bảng shot hiện tại.
6. **Phát hiện điều khoản (nguyên văn ở `reports/casting-giong/giay-phep.md`):**
   - **Mọi giọng Default của ElevenLabs, gồm giọng hiện tại của kênh, hết hạn 31/12/2026** (*"All our Default voices will expire on December 31, 2026, and they will no longer be accessible after this date"*). Vậy dù chọn giọng nào, giọng kênh phải đổi trước cuối năm; T4–T5 sẽ được thu sau mốc đó.
   - Giọng Voice Library có thời hạn báo trước **30 ngày–2 năm**. Audio đã tạo thì *"will continue to exist and remain available for use thereafter"*.
   - Quyền sở hữu giọng tạo bằng Voice Design **không được ghi rõ** (CHƯA XÁC MINH).
   - Tài liệu hôm nay khuyến nghị **`eleven_v4`** cho đọc dài. Model kênh `eleven_multilingual_v2` *"doesn't support phoneme tags"*, tức chỉ nhận alias.
7. **Chi phí ký tự không phụ thuộc giọng:** cả 8 giọng đều tính hệ số 1,0 và cùng model. Một tập 12 phút cần ≈ 9 919 ký tự gửi, cộng thu lại ≈ 30 %, tức ≈ 12 900 ký tự, làm bộ đếm tăng **≈ 6 000** (tỷ lệ đo được 0,469). **Bộ đếm tài khoản hiện ở 131 238/144 034, còn ≈ 12 800 tới lúc đặt lại ngày 01/11/2026**: đủ cho 1 lượt thu T3, không đủ cho 2.

**Chỉ số nằm trong ±5 % quanh ngưỡng:**
| Chỉ số | Đo | Ngưỡng | Lệch |
|---|---|---|---|
| Ước phim T3, G2 | 730,0 s | trần 721,2 s | **+1,2 %** (cần speed ≈ 1,015 hoặc giãn 10 s) |
| Ước phim T3, G4 / G5 / G6 | 719,7 s | 721,2 s | −0,2 % (vừa bảng shot hiện tại) |
| Lời T3 của G5 so khung lời của bảng shot | 662,6 s | 668 s | −0,8 % (chỉ còn 5 s dư) |
| Loudness G4 | −14,3 LUFS | −14,0 (đạt −15,0…−13,8) | trong dải |
| ElevenLabs gửi | 25 627 | mức dừng 30 000 | −14,6 % (không trong ±5 %; nêu để theo dõi) |

**Việc chờ chủ dự án:** §7.

---

## 1. Bảng máy kiểm theo mã mù (chi tiết: `reports/casting-giong/may-kiem.json`)
> Nên nghe gói mù **trước** khi đọc bảng này, vì số đo có thể làm lệch cảm nhận.

Hai cách nghe theo BAI-HOC #86: **M** = faster-whisper `medium.en` beam 5, **S** = `small.en` beam 1; cả hai không dùng hotwords. Lời gốc so sánh là lời khoá (số được chuẩn hoá thành chữ). "Sai" = cả hai cách nghe đều không nhận ra; "nghi" = chỉ một cách nghe nhận ra.

| Mã | Từ đúng M / S | Số, năm sai (nghi) | Tên trong đoạn sai (nghi) | Phát âm 47 lượt đầu: đúng · sai | Alias thay (ASR, M) | Từ/giây (3 đoạn) | Lời T3 ước | Phim T3 ước · lệch trần | speed cần | F0 trung vị (p10–p90) | LUFS / dBTP | Thời lượng tệp |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| G1 | 97,9 % / 97,3 % | 0 (2000: M nghe "two zero") | 0 (d'Arçon) | 44 · Algeciras, Cádiz, La Línea de la Concepción | Elliot · fait accompli · Cardiff · Montiro · La Linaire · d'Arson · Alhaciras | 2,202 (2,25 · 2,07 · 2,32) | 713,4 s | 765,1 s · **+6,1 %** | 1,068 | 88,6 Hz (54–134) | −14,1 / −5,1 | 147,9 s |
| G2 | 97,9 % / 98,2 % | 0 | 0 | 42 · Algeciras, Cádiz, Eliott, La Línea de la Concepción, fait accompli | Elliot · fête accompli · Cadith · Montyreaux · La Linaire · d'Arson · Al-Hacie-Raz | 2,316 (2,27 · 2,12 · 2,57) | 678,3 s | 730,0 s · **+1,2 %** | 1,015 | 128,2 Hz (88–168) | −14,1 / −4,2 | 141,6 s |
| G3 | 97,9 % / 97,9 % | 0 | 0 | 44 · Cádiz, Eliott, fait accompli | Elliot · fête accompli · Cardiff · Montero · La Linaia · Darson · Alhacie Raz | 2,210 (2,25 · 2,16 · 2,24) | 710,9 s | 762,6 s · **+5,7 %** | 1,064 | 76,7 Hz (53–105) | −14,0 / −5,4 | 147,4 s |
| G4 | 97,3 % / 97,6 % | 0 | 0 | 46 · Cádiz | Elliot · fête à compli · Cadith · Montero · La Linnea · Darzón · Alhesiraz | 2,578 (2,15 · 2,70 · 2,70) | 609,4 s | 719,7 s · −0,2 % | 1,0 | 104,1 Hz (79–133) | −14,3 / −4,5 | 126,9 s |
| G5 | 97,0 % / 97,6 % | 0 | 0 (d'Arçon) | 44 · Cádiz, Eliott, fait accompli | Elliot · fête à complais · Cardiff · Montayer O · La Ly-Naya · Darcon · Alhaciras | 2,371 (2,20 · 2,43 · 2,40) | 662,6 s | 719,7 s · −0,2 % | 1,0 | 124,5 Hz (94–167) | −14,1 / −5,2 | 138,0 s |
| G6 | 97,6 % / 98,2 % | 0 | 0 | 45 · Cádiz, fait accompli | Elliot · fête accompli · Cadith · Monter-aux · Lalini-a · D'Arson · Al-Haciras | 2,653 (2,54 · 2,54 · 2,84) | 592,2 s | 719,7 s · −0,2 % | 1,0 | 153,3 Hz (115–207) | −14,1 / −5,3 | 123,5 s |

**Cách đọc các cột:**
- **Từ đúng** = 1 − (thay + bỏ + chèn)/số từ, so với lời khoá. Phần lệch giống nhau ở mọi giọng: "Duc de Crillon" bị ASR viết "du Creon", "d'Arçon" thành "d'Arson", "the fourteenth of December" thành "fourteen December", "metres" thành "meters". Các lệch riêng từng giọng: G1 bị M nghe "Here's the twist" thành "How's the twist" ở cả hai cách nghe (nên nghe lại chỗ này); G5 và G6 có "Our read" bị S nghe thành "I'll read".
- **Phát âm 47** = 40 mục ở bảng thử (`phat-am-thu.json`) + 7 mục trong đoạn thử. Mọi mục sai đều nằm trong nhóm lỗi alias chung ở §0 mục 4, hoặc là giới hạn của ASR tiếng Anh: *Algeciras* đọc đúng "al-heh-SEE-rahs" nhưng ASR viết "Alhesiras", nên không đạt ngưỡng khớp mờ 0,75. Kết quả lượt alias thay xem ở cột "Alias thay". Năm và mốc ngày được đọc đúng ở mọi giọng.
- **Lời T3 ước** = 1 571 từ viết của lời khoá (đếm bằng `split()` trên các dòng lời; KHOA-LOI ghi 1 557 theo cách đếm G1) chia cho tốc độ đo trên 3 đoạn. Đây là số ước, sai số khoảng ±5 %, vì 3 đoạn chỉ dài khoảng 2 phút.
- **Phim T3 ước** = 719,667 + max(0, lời − 668). Bảng shot được dựng cho lời ≈ 668 s (KHOA-LOI-41 §3), nên lời dài hơn thì shot phải giãn.
- **speed cần** = lời/668: tham số `speed` của ElevenLabs (0,7–1,2) để lời vừa bảng shot hiện tại. Giọng sẽ nhanh hơn bản bạn nghe trong gói.
- **F0** đo bằng pyin. F0 thấp hơn nghĩa là giọng trầm hơn; chỉ để tham khảo, quyết định là ở tai.

**Hai giọng bị loại trước khi vào gói** (luật lọc đặt trước khi chấm: không giọng nào sai phát âm không sửa được, nên lọc theo độ vượt trần thời lượng; bỏ 2 giọng vượt nhiều nhất):
| Mã | Nguồn | Từ đúng M / S | Lời T3 · phim T3 ước | Lý do loại |
|---|---|---|---|---|
| L-a | Voice Design, mô tả A3 | 98,5 % / 98,2 % | 742,4 s · 794,1 s (**+10,1 %**) | chậm nhất: cần speed 1,11 hoặc giãn phim 74 s |
| L-b | Voice Library | 97,6 % / 87,8 % (S bỏ sót một đoạn) | 728,7 s · 780,4 s (**+8,2 %**) | cần speed 1,09. Đây cũng là giọng duy nhất bị cả hai cách nghe báo sai d'Arçon và Montero trong đoạn thử (lượt alias thay thì đúng 7/7) |

Loudness (BIBLE §4): mọi tệp phát hành đều ở dạng stereo dual-mono và nằm trong dải đạt −15,0…−13,8 LUFS, đỉnh thật ≤ −1 dBTP. Cách làm: tăng gain, dùng `alimiter` với trần mẫu ≈ −2,5 dBFS, rồi lặp đo `ebur128` trên chính tệp MP3. **Bài học:** đo bản mono cho LUFS thấp hơn bản phát ≈ 3 LU; lượt đầu của `kiem.py` đo trên mono nên số loudness trong `kiem-*.json` không phải số phát hành. Số phát hành nằm ở `khoa-ten.json` và `may-kiem.json`.

## 2. Ứng viên và cách chọn (tên thật chỉ có trong `khoa-ten.json`)
| Nhóm | Ứng viên | Cách chọn |
|---|---|---|
| A. Voice Design | 3 mô tả, mỗi mô tả 3 biến thể (`thiet-ke.json`): A1 *"deep, older British male in his sixties… warm gravel… unhurried… received pronunciation"*, A2 *"older male narrator, low register, BBC historical documentary, calm authority…"*, A3 *"mature… deep, resonant mid-Atlantic… slight rasp, slow and deliberate"* | Model `eleven_multilingual_ttv_v2`, cùng họ với model đọc của kênh. Chữ thử là 2m–2n. Máy chọn biến thể theo thứ tự: (1) tỷ lệ từ đúng cao nhất, lấy giá trị thấp hơn của 2 cách nghe; (2) nếu bằng nhau thì lấy F0 thấp nhất. Kết quả: A1 biến thể 3, A2 biến thể 3, A3 biến thể 1. Lưu vào tài khoản với tên `CINE-CastingGiong-A*` |
| B. Voice Library | 3 giọng nam lớn tuổi giọng Anh, nhãn narration hoặc "history/documentary", thời hạn báo trước **730 ngày** (mức tối đa), hệ số tính phí **1,0**, có trong thư viện từ 10/2024–11/2025 (ưu tiên giọng đăng lâu, ổn định). Đã loại các giọng có hệ số 3,0 (tính gấp 3) | Lọc bằng API `/v1/shared-voices` (giới tính, tuổi, ngôn ngữ, từ khoá, sắp theo lượng dùng 1 năm). Dùng trực tiếp không cần lưu: tài liệu ghi *"the notice period will be saved for your account"* |
| C. Giọng sẵn có | Giọng **thay thế vĩnh viễn** mà ElevenLabs công bố cho giọng Default nam giọng Anh kể chuyện (thời hạn báo trước 4 015 ngày) | Không dùng giọng Default vì hết hạn 31/12/2026 |
| Đ. Đối chứng | giọng hiện tại của kênh, giữ đúng cấu hình T1/T2 | — |

Cấu hình chung cho mọi giọng: `eleven_multilingual_v2`, stability 0,5, similarity 0,75, speed 1,0 (cấu hình của kênh). Alias được áp vào chữ trước khi gửi; với luật alias, kết quả tương đương gắn PLS. Mỗi đoạn là một lệnh gửi riêng. Chỉ thu 1 lượt mỗi giọng, nên **chỗ vấp có thể là ngẫu nhiên**: hãy ghi mốc thời gian vào phiếu.

## 3. Điều khoản nguyên văn (toàn văn và URL: `reports/casting-giong/giay-phep.md`; đọc ngày 18/10/2026)
- **Giọng Default hết hạn** — https://elevenlabs.io/docs/help-center/product/voices/my-voices/what-are-default-voices.md
  > Our Default voices are being replaced with new voices that you will be able to use forever. All our Default voices will expire on December 31, 2026, and they will no longer be accessible after this date. As part of this process, Default voices are only available for accounts that were created before March 2026.
- **Voice Library: thời hạn báo trước** — https://elevenlabs.io/vla (Voice Library Addendum, "Last Updated 6 March 2026")
  > (a) any Outputs generated using your User Voice Model prior to the end of the Notice Period will continue to exist and remain available for use thereafter, and (b) the User Voice Model will remain accessible for the duration of the Notice Period to users that added that User Voice Model to their account prior to removal of the User Voice Model from the Voice Library Service.
  
  — https://elevenlabs.io/docs/help-center/product/voices/voice-library/what-is-a-notice-period.md
  > If no notice period is set, their voice will be removed immediately if they decide to stop sharing it, and anyone who has saved the voice will immediately lose access.
  > The minimum notice period is 30 days, and the maximum is 2 years.
- **Voice Library không độc quyền:** VLA ghi *"others may be able to generate Output"* (xem `giay-phep.md` §7).
- **Voice Design:** trang tài liệu gọi tính năng này là *"still experimental"*. Giọng tạo ra chỉ tài khoản hoặc workspace của mình truy cập được, không đưa lên Library được. ToS (Last Updated 09/10/2026) cho người dùng giữ quyền với *Output* (audio). **Không có câu nào nói rõ ai sở hữu voice model đã thiết kế (CHƯA XÁC MINH).** Cũng **chưa rõ** nhãn "experimental" có rơi vào Beta Services Addendum hay không (addendum này cấm dùng thương mại dịch vụ alpha/beta/preview *"or similar designation"*).
- **Dùng thương mại:** mọi gói trả phí (gói hiện tại: Creator) có giấy phép thương mại, không bắt ghi công. Audio tạo ra khi không có gói trả phí thì không được dùng thương mại (`giay-phep.md` §4).
- **Model và từ điển:** `eleven_v4` được khuyến nghị cho đọc dài và audiobook. `eleven_multilingual_v2`: *"Most stable on long-form generations"*, nhưng *"doesn't support phoneme tags"* (chỉ alias). Phoneme IPA/CMU chạy trên `eleven_v4`, `eleven_v3`, `eleven_flash_v2`. Mỗi lệnh gắn tối đa 3 từ điển. **Mâu thuẫn:** các trang help/Studio cũ vẫn ghi phoneme *"only compatible with Eleven Flash v2"*, nên phải thử thật trước khi dựa vào.
- API `/v1/models` hôm nay (số đo thật): `eleven_v4`, `eleven_v3`, `eleven_multilingual_v2` có hệ số ký tự 1,0; `eleven_v4_turbo`, Flash/Turbo có hệ số 0,5. Không model nào yêu cầu alpha.

## 4. Rủi ro theo nguồn giọng (không gắn với mã G)
| Nguồn | Bị gỡ | Điều khoản | Trùng kênh khác |
|---|---|---|---|
| A. Voice Design | chỉ mình xoá được; phụ thuộc tài khoản ElevenLabs | quyền với voice model **chưa được ghi rõ**; tính năng "experimental" (CHƯA XÁC MINH có tính là Beta không) → **nên hỏi ElevenLabs bằng văn bản** trước khi dùng cho phim bán | thấp: giọng riêng của tài khoản, không có trên Library |
| B. Voice Library | chủ giọng gỡ được; ta còn 730 ngày (đã chọn mức tối đa); ElevenLabs có thể gỡ *"with or without notice"*; audio đã tạo vẫn dùng được | VLA; cần gói trả phí; hai trong ba giọng cho phép cả người dùng free | **cao**: hai giọng B có 60 339 và 113 578 lượt thêm (một giọng 12 746), nhiều kênh YouTube lịch sử đang dùng |
| C. Giọng thay thế của ElevenLabs | thời hạn báo trước 4 015 ngày; được nói là *"use forever / in perpetuity"* | ToS chung | **tăng dần**: hiện 4 257 lượt thêm, nhưng là giọng thay thế mặc định cho mọi tài khoản đang dùng giọng Default cũ |
| Đ. Giọng hiện tại (Default) | **hết hạn 31/12/2026** | ToS chung | rất cao (giọng Default phổ biến) |
- Rủi ro chung: kênh Last Lamplighters dùng một giọng Default khác, cũng hết hạn 31/12/2026. Việc này nằm ngoài phạm vi phiên, nhưng chủ dự án cần biết.
- §10.1 (bình luận chê giọng hoặc chê AI ≤ 2 %) chỉ đo được sau khi đăng T3. Gói nghe mù là cách sàng lọc trước.

## 5. Chi phí thật
| Hạng mục | Số |
|---|---|
| ElevenLabs gửi (`nhat-ky-ky-tu.jsonl`, 43 dòng) | **25 627 ký tự**: 8 giọng × (2 006 đoạn thử + 847 bảng phát âm) = 22 824; Voice Design 3 lệnh × 441 = 1 323; alias thay 8 × 185 = 1 480. Lưu 3 giọng thiết kế: 0 ký tự |
| Bộ đếm tài khoản | 119 227 → **131 238 (+12 011)**, tỷ lệ 0,469 ký tự/ký tự gửi (BAI-HOC #103 ghi 0,44; riêng các lượt thu TTS đo được 0,44 ở lượt đầu). Giới hạn kỳ 144 034, đặt lại 01/11/2026 |
| Ước mỗi tập 12 phút, mọi giọng | ≈ 9 919 ký tự lời sau alias × 1,3 (thu lại) ≈ **12 900 ký tự gửi, bộ đếm ≈ 6 000**. Giọng không làm đổi giá; tham số speed không làm đổi giá; `eleven_v4` cùng hệ số 1,0; nếu dùng PLS thay vì thay chữ thì tính trên chữ gốc (9 195) |
| Claude API (`claude -p`) | **$0** (không gọi) |
| Claude subagent (đọc tài liệu, 44 lượt công cụ) | 198 209 token. Token của phiên chính không đo được trong phiên, nên không tự khai |
| YouTube / OpenAI | 0 / 0 |
| Giờ máy | ≈ 1,5 h (ASR 2 cách nghe × 8 giọng ≈ 40 phút) |
| Tài khoản ElevenLabs | thêm 3 giọng thiết kế vào My Voices (slot 6/30). 4 giọng Library/thay thế ở trạng thái "copied" (đã lưu thời hạn báo trước cho tài khoản) |

## 6. Đề xuất
**Đ1. Chọn giọng bằng nghe mù (khuyến nghị), dùng máy kiểm làm điều kiện cần.**
- Ưu: 6 giọng trong gói đều đạt chữ và số; quyết định sáng tạo thuộc về chủ dự án (ghi vào AUTHORSHIP).
- Nhược: chỉ có 1 lượt thu mỗi giọng; khoảng 2 phút chưa nói hết cảm giác nghe 12 phút.
- Tác động: chọn xong thì phải sửa BIBLE-KENH2 §4 ("giọng Eric eleven_multilingual_v2"); việc này do phiên P làm.
- Rủi ro: nếu chọn một trong 3 giọng đọc chậm thì phải xử lý thời lượng (Đ2).

**Đ2. Nếu chọn giọng đọc chậm (phim ước vượt trần):** (a) thu với `speed` = giá trị ở cột "speed cần" (1,015–1,07); hoặc (b) giãn bảng shot và chấp nhận phim ≈ 12:10–12:45.
- Ưu (a): giữ bảng shot G1 đã duyệt.
- Nhược (a): giọng nhanh hơn bản đã nghe; với speed > 1,05 nhịp "unhurried" có thể mất.
- Tác động (b): phim vượt trần 12 phút của BIBLE §3, cần chủ dự án duyệt.
- Rủi ro: phải nghe lại 1 đoạn ở speed mới trước khi thu cả tập (≈ 2 000 ký tự).

**Đ3. Sửa từ điển alias trước khi thu T3** (do phiên khoá lời/âm thanh làm; phiên này không sửa `channel-k2/`).
- Thay: Eliott → `Elliot`; fait accompli → `fet ah-kom-plee`; La Línea (và các dạng ghép) → `la lee-nay-ah`; Montero → `mon-tair-oh`; d'Arçon → `dar-sohn`. **Luật: alias viết thường, không có âm tiết VIẾT HOA**, vì một số giọng đọc thành chữ cái. Cádiz giữ dự phòng và để tai người kiểm.
- Ưu: lượt thử cho thấy đúng ở 8/8 giọng.
- Nhược: PLS đổi thì SHA trong `LOI-KHOA.sha256` cũng đổi (lời khoá không đổi).
- Rủi ro: đổi trọng âm phải để tai người kiểm lại 1 lượt.

**Đ4. Thử `eleven_v4` với giọng được chọn** (≈ 2 000 ký tự) trước khi khoá model cho series. Tài liệu hôm nay khuyến nghị v4 cho đọc dài và hỗ trợ phoneme.
- Ưu: chất lượng và phoneme.
- Nhược: v4 không có `<break>`/SSML và không có thanh Style/Speed (theo `giay-phep.md`), nên cách xử lý thời lượng ở Đ2(a) có thể không dùng được.
- Rủi ro: khác chất giọng so với bản nghe mù, phải nghe lại.

**Đ5. Nếu chọn giọng Voice Design:** gửi câu hỏi bằng văn bản cho ElevenLabs về quyền đối với voice model đã thiết kế và nhãn "experimental" trước khi bán phim. Lưu `voice_id`, `generated_voice_id` và mô tả (đã có trong `thiet-ke.json`).

## 7. Việc chờ chủ dự án
1. **Nghe mù 6 tệp** `reports/casting-giong/nghe-mu/G1–G6.mp3` theo `reports/casting-giong/HUONG-DAN-NGHE.md` (điện thoại + tai nghe; chấm 1–10 bốn tiêu chí) và **chọn 1 giọng** (kèm 1 giọng dự phòng nếu muốn). Chưa mở `khoa-ten.json`.
2. Nếu giọng được chọn đọc chậm: chọn Đ2 (a) speed hoặc (b) giãn phim.
3. Duyệt Đ3 (sửa alias) và giao cho phiên nào.
4. Duyệt Đ4 (thử `eleven_v4`) và Đ5 (hỏi ElevenLabs, nếu chọn giọng Voice Design).
5. Biết trước: **giọng Default hiện tại của kênh (và giọng của Last Lamplighters) hết hạn 31/12/2026**. Quota ElevenLabs còn ≈ 12 800 tới ngày 01/11.

## 8. Tệp
`reports/casting-giong/`:
- `giay-phep.md`: điều khoản nguyên văn + 60 URL.
- `doan-thu.json`: 3 đoạn, chữ khoá và chữ gửi.
- `phat-am-thu.json`: 40 mục.
- `thiet-ke.json`: Voice Design (mô tả, biến thể, điểm, voice_id).
- `may-kiem.json`: theo mã G và L.
- `khoa-ten.json`: **chỉ mở sau khi chấm**.
- `nhat-ky-ky-tu.jsonl`: có mã nội bộ; không mở trước khi chấm.
- `HUONG-DAN-NGHE.md`, `nghe-mu/`.
- Công cụ: `doan_thu.py`, `phat_am_thu.py`, `thiet_ke.py`, `chon_bien_the.py`, `luu_thiet_ke.py`, `thu.py`, `kiem.py`, `kiem_lib.py`, `alias_thay.py`, `nghe_mu.py`, `tong_hop.py`, `cg_lib.py`.

Bản thu thô và kết quả ASR đầy đủ nằm ngoài git ở `/var/tmp/cine-out/casting-giong/` và mất khi container bị thu hồi. Thu lại đúng như vậy bằng cache theo băm tốn ≈ 25 600 ký tự.
