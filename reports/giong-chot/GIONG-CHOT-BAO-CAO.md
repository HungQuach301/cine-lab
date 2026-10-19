**Nhánh thật: `claude/giong-chot-contested-places-ux4ytb`** (harness buộc nhánh này thay cho `giong-chot` của lệnh). Nhánh tạo từ `origin/main` @ `5253ba2b`, rồi `git merge --no-ff origin/casting-my` @ `3f5dd72b`; merge này chỉ thêm `reports/`. Đã đẩy, **không merge vào main**.

# GIỌNG-CHỐT — chốt G1 cho "Contested Places", sửa từ điển phát âm, đo tốc độ, thử model — DỪNG

> Phiên GIỌNG-CHỐT, 19/10/2026 (UTC 18/10 23:44 → 19/10 00:15). **Chưa thu cả tập.**
> **Phạm vi sửa:** `reports/giong-chot/**`, `channel-k2/k2c-t3-01/khoa-loi/phat-am/**`, và dòng PLS trong `LOI-KHOA.sha256`. Không sửa `loi-khoa.txt`, `scripts/`, `design/`, `checks/`, `docs/`, `treatment.json`.
> **Đã đọc:** `reports/m3/BAI-HOC-LL.md`; `CASTING-MY-BAO-CAO.md` (§0, §1, §4.5); `CASTING-GIONG-BAO-CAO.md` (§1, §6); `casting-giong/giay-phep.md`, `thiet-ke.json`, `phat-am-thu.json`, `alias_thay.py`; `khoa-loi/phat-am/` (47 mục); `loi-khoa.txt`.
> **Môi trường:** `scripts/env/verify.sh` cho 11 ĐẠT, 4 TRƯỢT (OpenEXR, three.js, tifffile/pyshp, k2v node_modules). Phiên này không dùng mục nào trong 4 mục trượt.

## Khối điều lệ
| Trường | Lệnh | Thực tế |
|---|---|---|
| Nhánh | `giong-chot` từ `origin/main` + merge `casting-my` | harness buộc tên khác (dòng đầu); gốc và merge đúng lệnh |
| Vùng sửa | `phat-am/**`, dòng PLS của `LOI-KHOA.sha256`, `reports/giong-chot/**` (≤ 10 MB, không LFS) | đúng: `reports/giong-chot/` ≈ 5,5 MB; không dùng LFS; `loi-khoa.txt` vẫn `0fdc72ce…` (kiểm trước và sau) |
| ElevenLabs | mốc theo dõi 3 000, **chặn 6 000 ký tự gửi** | **4 941 ký tự gửi** (vượt mốc theo dõi; dưới mức chặn 17,7 %). Mức chặn được cài thành mã: `gc_lib.tts` từ chối gửi khi chạm 6 000. Bộ đếm **133 536 → 135 707 (+2 171)** |
| Claude | theo dõi $2; chặn an toàn $10 | Claude API (`claude -p`) **$0**; 0 subagent. Token phiên chính không đo được trong phiên, nên không tự khai |
| OpenAI / YouTube | 0 / 0 | **0 / 0** |
| Preflight / email / khoá | bắt buộc | `tools/preflight.sh` chạy trước mỗi commit (4 commit của phiên): **ĐẠT**, `lock.py --verify` **KHỚP**. Không có email trong tệp, header, URL hay payload. Tải tài liệu bằng UA `CineLab-research (+https://github.com/HungQuach301/cine-lab)`. Khoá do proxy gắn; không đọc, không in |
| Dừng | không dừng hỏi giữa chừng | đúng; đẩy việc dở sau mỗi phần |

**Vượt mốc theo dõi 3 000 ký tự, lợi ích:** kế hoạch đúng lệnh là 3 786 ký tự: bảng 41 mục (1 017), móc 3 mức speed (1 155), pin v2 và v4 (1 614). Phiên thêm **lượt B của móc, 1 155 ký tự**: cả 3 mức dùng chung một seed, vì một lượt mỗi mức cho kết quả ngược. Lượt A ở speed 1,03 lại chậm hơn lượt A ở 1,00 (§3). Không có lượt B thì bảng tốc độ không dùng để quyết định được.

---

## 0. Tóm tắt (đọc 2 phút)
1. **G1 đã chốt và đã lưu trong tài khoản.** Thông tin ở `CHON-GIONG.md`: câu chọn ghi nguyên văn, `voice_id` `VDLncRBHDjLHBqLhQ1Qt`, `generated_voice_id` `VDLncRBHDjLHBqLhQ1Qt` (biến thể 3), mô tả thiết kế nguyên văn. `GET /v1/voices/<id>` trả về `CINE-CastingGiong-A2-v3`, `category=generated`, lưu ngày 18/10. Đây không phải bản tạo tạm, nên phiên này không phải lưu lại.
2. **Đã sửa alias Đ3, 7 mục** (chữ thường, không có âm tiết VIẾT HOA). SHA của PLS đổi `3a70a020…0f24` → **`66ed934a…8e29`**; `loi-khoa.txt` giữ `0fdc72ce…`; `sha256sum -c LOI-KHOA.sha256` cho 3/3 OK.
   - **Phát âm G1 sau khi sửa: 47/47 mục đạt ở ít nhất một cách nghe, 41/47 đạt ở cả hai cách nghe, 0 mục sai.** Ở casting, G1 đạt 44/47 và sai Algeciras, Cádiz, La Línea de la Concepción.
   - 6 mục "nghi" (§2) gồm Cádiz và isthmus, cần tai người nghe.
3. **Tham số speed tác dụng yếu hơn số danh định.** So hai lượt cùng seed: speed 1,03 chỉ nhanh hơn 1,00 là **+0,9 %**, speed 1,06 là **+2,5 %** (danh định +3 % và +6 %). Giữa hai lượt cùng mức speed, tốc độ lệch tới 8 % (lượt A ở 1,03 chậm nhất trong cả 6 lượt).
   - Lời T3 ước ở speed 1,03 (theo số đo): **≈ 707 s** (speed 1,00: 713 s).
   - Phim ước sau khi giãn shot (§5): **≈ 744 s**, nằm trong mục tiêu 735–745 s nhưng sát cận trên. Sai số ước khoảng ±5 % vì chỉ đo trên vài đoạn ngắn.
4. **Model** (chỉ đọc sau khi nghe X/Y): **`eleven_v4` không có thanh Speed** (tài liệu hôm nay, `tai-lieu-v4.md`). v4 **tính phí như v2**: hệ số 1,0; bộ đếm đo thật **+355 cho 807 ký tự**, tức 0,440/ký tự, bằng v2. Đo khác nhau ở §4.
5. **Đ2 (c), giãn bảng shot:** với speed 1,03 (theo số đo) cần giãn **10 shot, +24,5 s, từ 719,7 lên 744,1 s**. Phần giãn dồn vào shot 3D có máy chạy. Không giãn tấm im lặng, không cắt lời. Bảng ở §5. Phần giãn này **cũng sửa lỗi lời 5j tràn sang tấm im lặng KA2026**, lỗi có từ KHOA-LOI-41.
6. **Đ5:** thư tiếng Anh `hoi-elevenlabs.md` đã soạn, **chưa gửi**.
7. **Quota sau phiên: bộ đếm 135 707/171 534, còn 35 827** tới 01/11/2026 06:57 UTC.
   - Lượt thu T3 thật ước ≈ 12 900 ký tự gửi, làm bộ đếm tăng ≈ 5 700. Con số này như nhau với v2 và v4, và như nhau ở mọi mức speed.
   - Hiện còn trên mức để dành 15 000 mà lệnh yêu cầu.

**Chỉ số nằm trong ±5 % quanh ngưỡng:**
| Chỉ số | Đo / ước | Ngưỡng | Lệch |
|---|---|---|---|
| Phim T3 ước, speed 1,03 (theo số đo), mô hình shot | 744,1 s | mục tiêu ≤ 745 s | **−0,1 %** |
| Phim T3 ước, speed 1,03 (theo số đo) | 744,1 s | trần 12 phút (720 s) | **+3,35 %** (≤ +5 % theo Đ2) |
| Phim T3 ước, speed 1,00, mô hình shot | 747,9 s | mục tiêu ≤ 745 s | **+0,4 %** |
| Phim T3 ước, speed 1,06 (theo số đo) | 738,6 s | mục tiêu 735–745 s | trong khoảng; cách cận dưới +0,5 % |
| Loudness các tệp nghe | −13,9…−14,1 LUFS | dải đạt −15,0…−13,8 | cách cận trên 0,1 LU |
| Đỉnh thật lớn nhất (bảng 41 mục) | −2,0 dBTP | ≤ −1 dBTP | đạt |

---

## 1. Lựa chọn giọng (bước 1) — `CHON-GIONG.md`
Câu ghi nguyên văn: "Chủ dự án chọn G1 (A2, Voice Design) qua nghe mù 18/10/2026 23:31; chọn lại G1 (M2) qua nghe mù CASTING-MỸ 19/10/2026 06:07".
- Mô tả thiết kế ghi nguyên văn trong tệp. **Lưu ý:** mô tả này ghi *"neutral southern English accent"*, tức G1 là giọng Anh, dù được chọn lại trong vòng "giọng Mỹ". Trong vòng đó G1 là đối chứng và thắng 4 giọng Mỹ mới.
- Giọng nằm trong My Voices với tên `CINE-CastingGiong-A2-v3`. Phiên này không đổi tên giọng, vì không cần cho việc nào trong lệnh.
- **Ghi vào `AUTHORSHIP.md` là việc của phiên P.**

## 2. Từ điển phát âm (bước 2)
### 2.1 Alias trước → sau (`sua-pls.json`; công cụ `sua_pls.py`)
| Mục | Trước | Sau |
|---|---|---|
| Eliott | `EL-ee-ut` | `Elliot` |
| fait accompli | `fayt a-kom-PLEE` | `fet ah-kom-plee` |
| La Línea | `La LEE-neh-ah` | `la lee-nay-ah` |
| La Línea's | `La LEE-neh-ah's` | `la lee-nay-ah's` |
| La Línea de la Concepción | `La LEE-neh-ah deh la Kon-sep-SYON` | `la lee-nay-ah deh la Kon-sep-SYON` (chỉ đổi phần La Línea, theo Đ3) |
| Montero | `mon-TEH-roh` | `mon-tair-oh` |
| d'Arçon | `dar-SOHN` | `dar-sohn` |
| Cádiz | `KAH-deeth` | **giữ** (dự phòng; để tai người) |

Các tệp trong `phat-am/` được sửa:
- `gibraltar-eric.pls`: SHA `3a70a020da3e084363f2f3e465a73eb9b48d5bc3cc3132d7bd70c5dfb64f0f24` → **`66ed934a5e041e14dee029a89522b7fcba5c83edf3c19741e2dc742179358e29`**. Tên tệp giữ chữ "eric" để không đổi đường dẫn đã khoá; chú thích trong tệp ghi rõ giọng là G1.
- `tu-dien.json`: sửa trường `doc`, thêm ghi chú Đ3 cho từng mục đã đổi, `voice` → G1.
- `loi-khoa.tts-preview.txt`: sinh lại từ lời khoá. Dài 10 060 ký tự (trước là 10 062).

`LOI-KHOA.sha256`: chỉ thay dòng PLS. `sha256sum -c` cho 3/3 OK.

### 2.2 Kết quả 47 mục, chỉ G1, model v2, speed 1,0 (`may-kiem.json`)
Cách kiểm: 41 mục nằm trong `bang` (40 mục của bảng casting, cộng câu 5i nguyên văn có "18 October 2026"); 3 mục trong móc (1309, 1783, 2026); 3 mục trong pin (1782, Duc de Crillon, d'Arçon). Hai cách nghe: **M** = medium.en beam 5, **S** = small.en beam 1, không dùng hotwords (như casting).

**Kết quả: 47/47 đạt ở ít nhất một cách nghe; 41/47 đạt ở cả hai; 0 mục sai ở cả hai.** Mọi năm, ngày và số đều đúng ở cả hai cách nghe.

| Mục "nghi" | M nghe | S nghe | Nhận định |
|---|---|---|---|
| Algeciras | "Alhesiras" ✓ | "Alhesiraz" (0,67) | giới hạn của ASR tiếng Anh, giống casting; âm "al-heh-SEE-rahs" đúng |
| Cádiz (dự phòng) | "Cadiz" ✓ | "Cadith" (0,57) | S nghe ra âm "th" cuối, tức đúng âm KAH-deeth. **Để tai người** (câu đầu của `phat-am/G1-bang-41-muc.mp3`, sau "Algeciras") |
| Diego de Salinas | "Di Aigaudé, Sahlinas" (0,71) | "Di Igoe de Sahlinaaz" ✓ | M tách sai chữ; nên nghe lại |
| d'Arçon | "Darzone" (0,67) | "Darson" ✓ | M nghe ra âm "z". **Tai người**: alias `dar-sohn` có thể bị đọc thành "dar-zone" |
| fait accompli | "fête accompli" ✓ | "fête à complie" (0,72) | đã hết lỗi "fight" của casting |
| isthmus | "**ISS** musse" ✓ (khớp alias) | "ismaz" (0,50) | **M viết "ISS" bằng chữ in hoa**: dấu hiệu alias VIẾT HOA `ISS-muss` bị đọc như ba chữ cái, cùng loại lỗi mà Đ3 đã sửa. **Tai người**; đề xuất Đ-C (§6) |

- **Đã hết lỗi:** cả ba dạng La Línea đều đạt ở cả hai cách nghe. M nghe "La lénaïa", S nghe "la la naya": âm "lee" ngắn đi, nên tai người cần xác nhận. Eliott được nghe thành "Elliott"/"Elliot"; Montero được nghe thành "Montero" ở cả hai.
- **So với casting** (G1 lượt đầu 44/47): các mục từng sai do alias VIẾT HOA nay đều đạt.

## 3. Tốc độ (bước 3) — `toc-do/`, `nhip.json`, `may-kiem.json`
Đoạn móc 0a–0e (60 từ viết, 385 ký tự gửi), model v2, stability 0,5, similarity 0,75. Lượt **A** không có seed; lượt **B** dùng seed 19102026, chung cho cả 3 mức. Từ/giây = từ viết chia cho khoảng lời (từ đầu từ đầu tiên tới cuối từ cuối, theo dấu thời gian ASR M), cùng cách đo với casting.

| speed | Từ/giây A · B · TB | So 1,00, cùng seed (B) | Lời T3 ước, theo số đo | Lời T3 ước, danh định (713,4/speed) | Phim ước, công thức casting* | **Phim ước, mô hình shot (§5)** | Tệp nghe |
|---|---|---|---|---|---|---|---|
| 1,00 | 2,224 · 2,190 · 2,207 | — | 713,4 s | 713,4 s | 765,1 s (+6,1 %) | **747,9 s** (+3,9 %) | `G1-moc-speed-1.00-A/B.mp3` |
| 1,03 | 2,052 · 2,209 · 2,131 | **+0,9 %** | **707,3 s** | 692,6 s | 759,0 s (+5,4 %) | **744,1 s** (+3,35 %) | `G1-moc-speed-1.03-A/B.mp3` |
| 1,06 | 2,252 · 2,244 · 2,248 | **+2,5 %** | 696,2 s | 673,0 s | 747,9 s (+3,7 %) | **738,6 s** (+2,6 %) | `G1-moc-speed-1.06-A/B.mp3` |
| 1,00 kéo nhịp ×1,03 sau thu (rubberband) | — | +3,0 % (chính xác) | 692,6 s | — | 744,3 s | **737,4 s** | `G1-moc-speed-1.00-A-keo-x1.03.mp3` |

\*Công thức casting: 719,667 + max(0, lời − 668). Công thức này giả định mọi giây lời vượt đều làm phim dài thêm. Mô hình shot (§5) tính cả phần dư sẵn có trong từng shot. Phần trăm trong ngoặc là lệch so với 720 s.

**Cách đọc bảng:**
- **Gốc lời T3 ở speed 1,00 = 713,4 s**, đo trên 3 đoạn ở casting (2,202 từ/s). Hôm nay đoạn móc ở speed 1,00 đo 2,207 từ/s (hai lượt), còn casting đo 2,25, lệch 2 %, nên phiên giữ gốc 713,4 s. Lời ở mức speed s = 713,4 × (từ/giây lượt B ở 1,00 ÷ từ/giây lượt B ở s).
- **Biến thiên giữa các lượt thu lớn hơn tác dụng của speed.** Cùng speed 1,03, lượt A ra 2,052 từ/s, lượt B ra 2,209 (lệch 7,6 %). Đoạn pin ở speed 1,0 hôm nay đo 2,200 từ/s, casting đo 2,07 (lệch 6 %).
- Phiên thử tách tốc độ phát âm khỏi chỗ ngừng (`nhip.json`), nhưng số tách ra cũng dao động như vậy (2,6–3,2 từ/s khi có tiếng). Tức là speed không phải nguồn chính của khác biệt; ngừng và nhấn mới là nguồn chính.
- **Kết luận:** speed 1,03 có thể **gần như không rút ngắn được lời**: số đo cùng seed cho +0,9 %, độ bất định cỡ ±4 %. Thời lượng thật chỉ biết sau lượt thu T3 cả tập.
- **Cách nén thời lượng chính xác, không phụ thuộc lượt thu:** kéo nhịp ×1,03 sau khi thu (rubberband, giữ cao độ và formant), tốn 0 ký tự. Tệp tham khảo `…-keo-x1.03.mp3` dài 26,59 s, bằng 27,40/1,03. Rủi ro là tiếng máy, nên chủ dự án cần nghe.
- Loudness 7 tệp: −13,9…−14,1 LUFS, đỉnh thật −2,3…−3,3 dBTP, LRA 1,7–2,4 LU (`xuat.json`).

## 4. So model (bước 4) — **nghe `model/X.mp3`, `model/Y.mp3` trước khi đọc mục này**
**Tài liệu hôm nay (`tai-lieu-v4.md`, truy cập 2026-10-19):**
- https://elevenlabs.io/docs/overview/capabilities/text-to-speech/eleven-v4.md: *"Style and Speed sliders are not available in Eleven v4, and SSML is not supported."* và *"Both variants use two voice settings: Stability and Similarity."* ⇒ v4 được thu **không có speed** (stability 0,5, similarity 0,75). v2 được thu ở speed 1,0 với cùng chữ, cùng stability và similarity.
- https://elevenlabs.io/pricing/api: v4 *"$0.08 Price per 1K characters"*, v4 Turbo $0,04, **v2 Multilingual $0,08**. `GET /v1/models`: `eleven_v4` có `character_cost_multiplier` 1,0, giống v2.
- ⇒ Giá $0,08 của v4 **bằng** giá v2; chỉ v4 Turbo rẻ hơn một nửa.

**Bộ đếm đo thật cho riêng lượt v4:** 134 845 → 135 200 = **+355 cho 807 ký tự gửi, tức 0,440**. Đo sau khi chờ 90 s; đọc lại trước lượt kế tiếp vẫn là 135 200, tức bộ đếm không cập nhật trễ. Lượt v2 cho tỷ lệ 0,439.

| Pin 2k–2n (128 từ viết) | `eleven_multilingual_v2` (speed 1,0) | `eleven_v4` |
|---|---|---|
| Khoảng lời · từ/giây | 58,2 s · 2,200 | **48,6 s · 2,636 (+19,8 %)** |
| Ngừng (RMS < nền + 8 dB, ≥ 0,2 s) | 17,1 s / 29 chỗ | **6,7 s / 17 chỗ** |
| Tốc độ phát âm khi có tiếng | 3,06 từ/s | 3,01 từ/s, nên phần nhanh hơn của v4 gần như hoàn toàn đến từ **ngừng ít hơn** |
| F0 trung vị (p10–p90) | 73,2 Hz (58–106) | 90,6 Hz (50–151): biên độ cao độ rộng hơn, nhiều nhấn hơn |
| Từ đúng M / S | 97,0 % / 96,3 % | 98,5 % / 97,8 % |
| Số, năm | đúng hết ở cả hai cách nghe | đúng hết ở cả hai cách nghe |
| Duc de Crillon | M và S nghe "Duc du Creon" (đạt nhờ khớp alias) | **M nghe "Duc de Crillon", đúng nguyên văn**; S nghe "Duc de Creon" |
| d'Arçon | M nghe "Darzone" (nghi), S nghe "Darson" | M và S nghe "D'Arson" ✓ |
| Lời T3 ước, nếu tỷ lệ giữ như đoạn này | 713 s | **≈ 595 s**: ngắn hơn khung lời của bảng shot (668 s) ≈ 73 s, không cần giãn shot, nhưng sẽ dư hình |
| Tệp nghe | (xem `khoa-model.json`) | (xem `khoa-model.json`) |

**Nhận định của máy** (quyết định là ở tai):
- v4 đọc tên Pháp tốt hơn.
- v4 có ít ngừng hơn rõ rệt và nhấn nhiều hơn. Điều này đi ngược brief "unhurried, grave", và tài liệu cũng nói giọng Voice Design trên v4 *"may be less performative"*.
- v4 **không có cách nào làm chậm lại** ngoài thẻ âm thanh, dấu câu, hoặc kéo nhịp sau thu (×0,85 là mức lớn, rủi ro nghe ra tiếng máy).
- ElevenLabs vẫn *"still experimenting with Eleven v4"*.
- Mỗi model chỉ có 1 lượt thu.

## 5. Đề xuất giãn bảng shot cho Đ2 (c) (bước 5) — CHỈ ĐỀ XUẤT, không sửa `treatment.json`
Công cụ `gian_shot.py` chỉ đọc `vay-ham/treatment.json` (74 shot, 719,667 s) và `g1/kiem-chu.json` (từ nói của từng shot). Kết quả ghi vào `gian-shot-<kịch bản>.json`.
- **Mô hình:** lời của mỗi shot = lời T3 × (từ nói của shot ÷ 1 670). Lời chảy tuần tự từ shot này sang shot kế.
- Mỗi shot phải chứa lời của mình cộng 0,4 s (luật G1). Lời được chảy sang shot kế tối đa 0,5 s, nhưng không được chảy vào tấm im lặng và không được chảy ra ngoài shot cuối.
- **Shot giãn được:** shot 3D có máy chạy, trừ khung neo, mốc đinh, cú liên hoàn và 0c (cố định 3 s theo NC-H2).
- **Thẻ, ảnh, tranh, bản đồ:** chỉ giãn tới trần của loại; phần vượt trần chảy sang shot giãn được kế tiếp.
- Không giãn tấm im lặng, không cắt lời, không rút shot đang dư. Thời lượng làm tròn lên bậc khung hình 24 fps.

| Kịch bản | Lời T3 | Phim sau giãn | Số shot giãn |
|---|---|---|---|
| Bảng hiện tại với lời 668 s (chỉ để đối chiếu) | 668 | 729,3 s (+9,6) | 4 |
| **speed 1,03, theo số đo (đề xuất)** | **707,3** | **744,1 s (+24,5)** | **10** |
| speed 1,00 | 713,4 | 747,9 s (+28,2) | 11 |
| speed 1,06, theo số đo | 696,2 | 738,6 s (+18,9) | 8 |
| speed 1,03 danh định / kéo nhịp ×1,03 sau thu | 692,6 | 737,4 s (+17,7) | 8 |
| v4 (nếu chọn) | ≈ 595 | 719,7 s (+0) | 0 |

**Lưu ý dòng đầu:** ngay ở lời 668 s, mô hình đã đòi **+9,6 s**. Lý do là bảng hiện tại để lời chảy dây chuyền tới 5,2 s qua nhiều shot (1h→1i→1j…, 2k→2l→2m→2n→2o…, SM3→4g, 5i→5j→KA2026). Mô hình này bắt lời được hấp thụ ở shot 3D đầu tiên. Phần này **độc lập với giọng** và có sửa lỗi đã biết: lời 5j tràn 1,4 s sang tấm im lặng KA2026 (KHOA-LOI-41 §6.1).

**Bảng đề xuất, speed 1,03 theo số đo (`gian-shot-v2-s1.03-do.json`):**
| Shot | Loại · máy | Dur hiện tại → đề xuất | + s | Lý do (lời của shot · lời chảy vào từ trước) |
|---|---|---|---|---|
| 0d | thẻ số "14 sieges" | 7,500 → 8,000 | +0,50 | lời 7,2 s + 1,2 s chảy từ 0c (0c cố định 3 s). Đã chạm trần thẻ 8 s |
| 1i | 3D vùng · boundary trace dọc tường bắc | 13,000 → 17,625 | +4,63 | nhận 4,1 s chảy từ 1h (ảnh Điều X, trần 12 s, lời 15 s) |
| 2o | 3D phố · mặt cắt vách bắc, đường hầm đào theo ngày | 12,500 → 18,500 | +6,00 | nhận 5,4 s chảy từ chuỗi 2k–2n (bản đồ, tranh, cú liên hoàn 2m, thẻ 2n đều chạm trần hoặc cố định) |
| 3a | 3D vùng · lateral dọc chiến tuyến | 12,000 → 13,875 | +1,88 | nhận 1,6 s chảy từ 2r (ảnh hiệp ước, trần 12 s) |
| 4c | 3D vùng · top-down rise, đường băng lấn vịnh | 9,000 → 13,042 | +4,04 | nhận 4,2 s chảy từ 4b (cú liên hoàn #1, cố định 15 s, lời 18 s) |
| 4g | 3D vùng · mũi tên sơ tán | 5,500 → 6,417 | +0,92 | giữ phần chảy 6,0 s của SM3, **trước tấm im lặng KB1943** |
| 5e | thẻ số GDP/người | 6,417 → 7,375 | +0,96 | lời 6,4 s + 0,6 s chảy từ khung neo KC2026; vẫn dưới trần 8 s |
| 5h | 3D phố · orbit cổng 2026 | 16,000 → 17,000 | +1,00 | lời 16,1 s + 0,5 s chảy từ 5g |
| 5j | 3D vùng · reveal kéo lùi, các tuyến ghost | 17,000 → 20,375 | +3,38 | nhận 2,6 s chảy từ 5i (thẻ "as of", trần 8 s); **sửa lỗi lời tràn vào KA2026** |
| 5k | 3D phố · quay về hình mở đầu | 20,000 → 21,167 | +1,17 | lời 20,8 s; shot cuối, không cho chảy ra ngoài |
| **Tổng** | | **719,667 → 744,125** | **+24,46** | theo chương: móc +0,5 · 1 +4,6 · 2 +6,0 · 3 +1,9 · 4 +5,0 · 5 +6,5 |

**Ưu:**
- 9/10 shot giãn là shot 3D có máy chạy, hoặc thẻ còn dưới trần.
- Tấm im lặng KB1943 và KA2026 giữ đủ 8 s và không có lời đè.
- Không khung neo, mốc đinh hay cú liên hoàn nào bị đổi.

**Nhược:**
- 2o (+6 s) và 1i (+4,6 s) kéo dài khá nhiều, nên G1b phải thêm nhịp hình cho hai shot này: thêm bước đào hầm ở 2o, đoạn trace chậm ở 1i.
- 0d chạm trần thẻ 8 s.

**Rủi ro:**
- Lời T3 thật có thể lệch ±5 % (≈ ±35 s).
- **Khuyến nghị: G1b đặt số giãn theo dấu thời gian lời thu thật** (ASR từng shot sau lượt thu T3), dùng bảng này làm khung. Nếu lời thật > 715 s, có thể kéo nhịp ≤ ×1,03 sau thu làm dự phòng, sau khi chủ dự án nghe tệp `…keo-x1.03` và thấy chấp nhận được.

## 6. Đề xuất
**Đ-A. Tốc độ:** thu T3 ở **speed 1,03 như Đ2 (c)**, với điều kiện chủ dự án nghe 1,03 B mà không thấy mất cảm giác "unhurried". Thời lượng chốt bằng giãn shot theo lời thu thật (§5). Kéo nhịp ×1,03 sau thu chỉ là dự phòng.
- Ưu: đúng hướng đã duyệt; speed 1,03 hầu như không đổi chất đọc.
- Nhược: speed 1,03 gần như không rút ngắn lời, nên gần hết thời lượng phải đến từ giãn shot (phim ≈ 744 s).
- Tác động: G1b giãn khoảng 10 shot.
- Rủi ro: lời thật dài hơn ước, khi đó phim > 745 s. Biện pháp là kéo nhịp hoặc chấp nhận tới 756 s (+5 %).

**Đ-B. Model: giữ `eleven_multilingual_v2` cho T3**, trừ khi tai chấm v4 hơn rõ (≥ 1,5 điểm ở "đáng tin" và "unhurried").
- Ưu: có speed; ổn định khi đọc dài (*"Most stable on long-form"*); giữ đúng nhịp đã duyệt; giá như v4.
- Nhược: đọc tên Pháp kém hơn v4 một chút (Crillon), và không dùng được phoneme (chỉ alias).
- Nếu chọn v4: lời ≈ 595 s, tức **khoảng 73 s hình không có lời** so với khung lời 668 s. Cần thu lại bảng 47 mục với v4 (≈ 1 000 ký tự) và **rút bảng shot**, ngược với Đ2. Đây là thay đổi lớn, phải duyệt lại.

**Đ-C (ngoài Đ3, cần duyệt): đổi alias isthmus `ISS-muss` → `iss-muss`**, và cân nhắc áp cùng luật chữ thường cho các alias VIẾT HOA còn lại (`dee-AY-go`, `Al-heh-SEE-rahs`, `San ROH-keh`, `tan-JEER`, `YOO-trekt`, `Kree-YOHN`, `Kon-sep-SYON`).
- Ưu: cùng nguyên nhân với các lỗi Đ3 đã sửa (ASR M viết "ISS" in hoa).
- Nhược: đổi trọng âm thì phải để tai kiểm lại; mỗi lượt kiểm tốn ≈ 1 000 ký tự gửi (≈ 450 bộ đếm). Đổi alias là đổi SHA của PLS.
- Rủi ro: thấp, nếu kiểm ngay trong lượt thu T3 bằng ASR toàn tập.

**Đ-D. d'Arçon:** nếu tai nghe ra "dar-zone" (M nghe "Darzone"), thử alias `dar-sawn` hoặc `dar-son` ở phiên sau.

## 7. Thư Đ5 (bước 6) — `hoi-elevenlabs.md`
Thư tiếng Anh, chưa gửi. Thư hỏi 5 điểm, dẫn nguyên văn các đoạn điều khoản trong `giay-phep.md`:
1. Dùng thương mại lâu dài, gồm YouTube có kiếm tiền và bán hoặc cấp phép phim, kể cả sau khi hết gói.
2. Nhãn *"Voice Design is still experimental"* có làm tính năng này rơi vào Beta Services Addendum hay không. Addendum cấm *"any commercial purposes"*.
3. Ai giữ quyền với voice model đã thiết kế; giọng có độc quyền không. Thư dẫn ToS: *"you retain all rights in and to your Output"*, Output *"does not include, ElevenLabs’ foundational … Voice Models"*, và định nghĩa User Voice Model.
4. Giọng có thể bị gỡ hay đổi không, có báo trước không, audio đã tạo còn dùng được không, giọng có giữ nguyên khi đổi model không.
5. Ghi công và công bố dùng AI.

Thư không có email, khoá hay thông tin thanh toán. Chủ dự án điền tên tài khoản, tên người gửi, rồi tự gửi qua kênh hỗ trợ trong tài khoản. **Điểm 2 là then chốt:** nếu ElevenLabs trả lời "Beta", audio của G1 không được dùng cho phim bán.

## 8. Ký tự cho lượt thu T3 thật (bước 7)
Lời gửi sau alias Đ3 là **9 917 ký tự** (71 dòng lời, không tính đầu mục chương). Cộng 30 % dự phòng thu lại, như casting. Tỷ lệ bộ đếm/ký tự gửi đo hôm nay: v2 0,439–0,440, v4 0,440.

| Cách thu | Ký tự gửi | Bộ đếm tăng | Còn lại sau T3 (từ 35 827) |
|---|---|---|---|
| v2, speed 1,03, alias thay vào chữ (cách đã dùng) | 9 917 × 1,3 ≈ **12 900** | **≈ 5 670** | ≈ 30 150 |
| v4 (không có speed), alias thay vào chữ | ≈ 12 900 | ≈ 5 670 | ≈ 30 150 |
| v2 hoặc v4, gắn PLS thay vì thay chữ (tính trên chữ gốc 9 195) | ≈ 11 950 | ≈ 5 260 | ≈ 30 570 (chưa thử cách gắn PLS trong dự án) |
| Cận trên, thu lại 50 % | ≈ 14 900 | ≈ 6 550 | ≈ 29 280 |
| Thêm, nếu chọn v4: kiểm lại 47 mục với v4 | +1 000 | +440 | — |
| Thêm, nếu duyệt Đ-C: kiểm alias chữ thường | +1 000 | +450 | — |

- Speed không đổi giá (casting đã kiểm). Kéo nhịp sau thu tốn 0 ký tự.
- Một lệnh v4 hoặc v2 nhận tối đa 10 000 ký tự, nhưng vẫn nên gửi theo từng chương như T1/T2.
- **Kết luận:** quota hiện tại đủ cho 1 lượt thu T3 và vẫn còn ≈ 29–30 nghìn tới ngày đặt lại 01/11. Lệnh yêu cầu để dành ≥ 15 000: **đạt**.

## 9. Chi phí thật
| Hạng mục | Số |
|---|---|
| ElevenLabs gửi (`nhat-ky-ky-tu.jsonl`, 9 dòng) | **4 941**: bảng 1 017 + móc A 3 × 385 + móc B 3 × 385 + pin v2 807 + pin v4 807. Voice Design 0, lưu giọng 0, đọc API (`/v1/voices`, `/v1/models`, `/v1/user/subscription`) 0 |
| Bộ đếm tài khoản (`bo-dem.jsonl`) | trước **133 536** (23:49 UTC) → sau bảng 133 983 (+447) → sau móc A + pin v2 134 845 (+862; lần đọc sau lượt móc A thấy bộ đếm trễ, nên hai lượt được gộp) → sau pin v4 135 200 (+355) → sau móc B **135 707** (+507). Tổng **+2 171 (0,439/ký tự gửi)**. Giới hạn 171 534, đặt lại 01/11/2026 06:57 UTC |
| Claude API | **$0** (không gọi `claude -p`); 0 subagent. Token phiên chính không đo được |
| OpenAI / YouTube | 0 / 0 |
| Web | 4 trang `elevenlabs.io` (tài liệu v4, API convert, models, giá API) |
| Giờ máy | ≈ 20 phút (ASR 2 cách nghe × 9 bản ≈ 12 phút) |
| Tài khoản ElevenLabs | không thêm, không xoá, không đổi tên giọng |

## 10. Việc chờ chủ dự án
1. **Nghe tốc độ:** `toc-do/G1-moc-speed-1.00|1.03|1.06-A|B.mp3`, 6 tệp. Lệnh giao 3 tệp; phiên xuất thêm lượt B vì lý do ở §3. Nghe thêm tệp kéo nhịp `G1-moc-speed-1.00-A-keo-x1.03.mp3` để tham khảo. Rồi **chọn mức speed cho T3** (Đ-A).
2. **Nghe model:** `model/X.mp3`, `model/Y.mp3`, theo `HUONG-DAN-NGHE.md` §B, **trước khi mở `khoa-model.json` và §4**. Rồi chọn v2 hay v4 (Đ-B).
3. **Tai người cho phát âm:** `phat-am/G1-bang-41-muc.mp3` để nghe Cádiz, La Línea, isthmus, Diego de Salinas; `model/*.mp3` để nghe d'Arçon. Rồi duyệt Đ-C và Đ-D.
4. **Gửi thư Đ5** (`hoi-elevenlabs.md`) sau khi điền tên.
5. Duyệt khung giãn shot ở §5 (làm ở G1b, theo lời thu thật).
6. Việc của phiên P: ghi lựa chọn G1 vào `AUTHORSHIP.md`; cập nhật BIBLE-KENH2 §4 ("giọng Eric" → G1); thêm `RIGHTS.md` dòng giọng G1 (Voice Design, điều khoản chờ thư Đ5).

## 11. Tệp
`reports/giong-chot/`:
- **Hồ sơ:** `CHON-GIONG.md`, `GIONG-CHOT-BAO-CAO.md` (tệp này), `HUONG-DAN-NGHE.md`, `hoi-elevenlabs.md`, `tai-lieu-v4.md`.
- **Tệp nghe:** `toc-do/` (7 MP3), `model/X.mp3`, `model/Y.mp3`, `khoa-model.json` (**mở sau khi nghe**), `phat-am/G1-bang-41-muc.mp3`, `xuat.json`.
- **Số đo:** `may-kiem.json` (ASR 2 cách nghe, 47 mục), `nhip.json`, `sua-pls.json`, `doan.json`, `gian-shot-*.json` (7 kịch bản), `bo-dem.jsonl`, `nhat-ky-ky-tu.jsonl`.
- **Công cụ:** `gc_lib.py` (dùng lại `casting-giong/cg_lib.py`, `kiem_lib.py`; trần 6 000), `sua_pls.py`, `doan.py`, `thu.py`, `kiem.py`, `nhip.py`, `xuat.py`, `gian_shot.py`.

Bản thu thô và ASR đầy đủ nằm ngoài git ở `/var/tmp/cine-out/giong-chot/`, và mất khi container bị thu hồi. Thu lại các bản có seed sẽ cho kết quả gần giống, nhưng tài liệu ghi rõ *"Determinism is not guaranteed"*.
