**Nhánh thật: `k2c-t3-kl42`**, đúng tên lệnh. Nhánh tạo từ `main` mới @ `8cedb8af`. Harness gợi ý nhánh `ccr-c89b4170-5gj2w0` nhưng không bắt dùng, nên phiên đẩy lên nhánh của lệnh. Đã đẩy, **không merge**.

# KL42-THU T3 — cập nhật main, khoá lời v4.2 (D11 = A), GC-C, thu G1 cả tập T3 — DỪNG chờ chủ dự án

> Phiên KL42, 19/10/2026 (UTC 06:17 → 07:35).
> **Vùng sửa:** `channel-k2/k2c-t3-01/**` (`loi-khoa.txt`, `script-v4.2-KHOA.md`, `LOI-KHOA.sha256`, `khoa-loi/phat-am/**`), `reports/kl42/**`, `AUTHORSHIP.md` (thêm 2 dòng). Không sửa `checks/`, `docs/`, `design/`, `scripts/`, `treatment.json`, hay nhánh khác.
> **Đã đọc:** `reports/m3/BAI-HOC-LL.md`; `reports/P-1910-BAO-CAO.md` §3; `khoa-loi/loi-v4.2-NHAP.txt`; `GIONG-CHOT-BAO-CAO.md` (toàn văn); `CHON-GIONG.md`; `docs/BIBLE-KENH2.md` §4, §10.1, §13.
> **Môi trường:** `verify.sh` cho 11 ĐẠT, 4 TRƯỢT (OpenEXR, three.js, tifffile/pyshp, k2v node_modules), giống GIỌNG-CHỐT. Phiên này không dùng mục nào trong 4 mục trượt.

## Khối điều lệ
| Trường | Lệnh | Thực tế |
|---|---|---|
| Bước 0 | ff-only main ← `p-1910-merge-g1b-giong-chot`, LOCK khớp, preflight chỉ trượt 2 mục đã biết | đúng (§1). Preflight trượt **1 mục**: P4 ở `mpfb2-LICENSE.txt`. Đẩy main bằng `--no-verify` đúng 1 lần |
| Vùng sửa | như trên | đúng |
| ElevenLabs | mốc theo dõi 14 000; **chặn 18 000 ký tự gửi** | **12 052 ký tự gửi**, dưới mốc theo dõi. Mức chặn được cài thành mã trong `kl_lib.tts`. Bộ đếm **135 707 → 141 009 (+5 302; 0,440/ký tự gửi)** |
| Claude | theo dõi $3; chặn $15 hoặc cùng lỗi ≥ 3 lần | Claude API **$0**; 0 subagent. Token phiên chính không đo được, nên không tự khai. Không có lỗi lặp ≥ 3 lần |
| OpenAI / YouTube | 0 / 0 | **0 / 0** |
| Preflight / email / khoá | bắt buộc | hook `pre-commit` + `pre-push` đã cài. Mọi commit của phiên: **ĐẠT**, `lock.py --verify` **KHỚP**. Không có email trong tệp, header, URL hay payload. UA khi gọi ElevenLabs: `CineLab-research (+https://github.com/HungQuach301/cine-lab)`. Khoá do proxy gắn; không đọc, không in |
| Âm thanh trong git | ≤ 5 MB/tệp | 4 MP3, lớn nhất 4,72 MB. Master WAV/FLAC nằm ngoài git, có ghi SHA (§6) |
| Dừng | không dừng hỏi giữa chừng | đúng. Đẩy việc dở 3 lần, kèm `CHECKPOINT.md` |

---

## 0. Tóm tắt (đọc 2 phút)
1. **Main đã cập nhật và đẩy:** `5253ba2b → 8cedb8af` (ff-only). LOCK 1.15.0 `f4fa0349…` **KHỚP**.
2. **Lời v4.2 đã khoá (D11 = A).** Câu nối A thay câu đầu 2o; khối ‹2o›/‹2p› dời lên ngay sau ‹KA1782›, trước ‹2j›. Không câu nào khác đổi.
   - `loi-khoa.txt`: `0fdc72ce…` → **`51d1c773…`**.
   - Số từ: **1 571 → 1 567 từ**.
3. **GC-C đã áp:** mọi alias còn âm tiết VIẾT HOA chuyển thành chữ thường hết.
   - **Thêm GC-C′ (chờ duyệt): isthmus `iss-muss` → `issmus`.** Lý do: với `iss-muss`, G1 đọc thành "Icesmus", "ice muss", có lần thành chữ cái "I.S." (§3.3). Với `issmus`, 3/3 câu đạt ở cả hai cách nghe.
   - PLS cuối: **`714314cf…`**.
4. **Kiểm 47 mục (speed 1,03):** 46/47 đạt ở ít nhất một cách nghe, 41/47 đạt ở cả hai.
   - Mục sai duy nhất là **Cádiz**, mục dự phòng không có trong lời.
   - d'Arçon được nghe là "D'Arson"/"Darson", nên **không áp GC-D**.
5. **Thu cả tập xong:** 6 chương, 8 lệnh (mỗi lệnh ≤ 1 812 ký tự), cùng seed 19102026, speed 1,03, alias thay vào chữ.
   - **ASR toàn tập, 2 cách nghe: 259 mục số/năm/tên → 258 ĐÚNG, 1 NGHI, 0 SAI.** Mọi số và năm đều đúng ở cả hai cách nghe.
   - Mục NGHI là **Algeciras**: ASR tiếng Anh viết âm seseo thành "Alhaciras", giống ở GIỌNG-CHỐT.
   - Thu lại 3 câu có isthmus, và lấy bản thu lại vào stem.
6. **Loudness:** master **−14,1 LUFS, −1,5 dBTP**, LRA 3,8 LU. Hai tệp xem: −14,2 LUFS, −1,2 và −1,3 dBTP.
7. **Nhịp thật:** lời theo shot (từ đầu tới cuối lời của mỗi shot, cộng lại) là **666,3 s**. Lời liền trong chương, gồm khoảng ngừng tự nhiên, là **723,5 s** (ước GIỌNG-CHỐT: 707,3 s, tức thật dài hơn +2,3 %).
   - **Bảng giãn shot mới:** phương án **B (đề xuất) = 745,0 s**: giãn 12 shot và giới hạn đuôi hình sau lời ≤ 1,37 s ở 13 shot.
   - Phương án **A (chỉ giãn) = 751,5 s**.
   - Bảng ở `bang-gian-shot.md`; mốc từng câu và shot ở `nhip-that.json`.
8. **Chờ chủ dự án:** nghe bản thu đủ; duyệt GC-C′; chọn A hay B; cho giờ chọn D11 để ghi AUTHORSHIP (§10).

**Chỉ số nằm trong ±5 % quanh ngưỡng:**
| Chỉ số | Đo | Ngưỡng | Lệch |
|---|---|---|---|
| Phim T3, phương án B | 745,000 s | mục tiêu ≤ 745 s | **0,0 %** (chạm ngưỡng) |
| Phim T3, phương án B | 745,000 s | trần 12 phút (720 s), cho phép ≤ +5 % (Đ2) | **+3,47 %** |
| Phim T3, phương án A | 751,500 s | mục tiêu ≤ 745 s | **+0,87 %** |
| Phim T3, phương án A | 751,500 s | trần 720 s, ≤ +5 % | **+4,38 %** |
| Phim T3, kéo nhịp ×1,02 (C102, để so) | 745,583 s | ≤ 745 s | +0,08 % |
| Loudness master | −14,1 LUFS | dải đạt −15,0…−13,8 | cách cận trên 0,3 LU (2,2 %) |
| Loudness 2 tệp xem | −14,2 LUFS | dải đạt −15,0…−13,8 | cách cận trên 0,4 LU (2,9 %) |
| Khớp tên ASR, ngưỡng 0,75 | Diego de Salinas (S, câu tách) 0,759 · Algeciras (M) 0,778 · Montero (S) 0,750 · fait accompli (S) 0,750 | ≥ 0,75 | +1,2 % · +3,7 % · 0 % · 0 % — đều cần tai người (§5) |
| Đỉnh thật tệp xem | −1,2 / −1,3 dBTP | ≤ −1 dBTP | đạt (dư 0,2–0,3 dB) |

---

## 1. Bước 0: cập nhật main
| Bước | Kết quả |
|---|---|
| `git fetch` | `origin/main` = `5253ba2b`. `main` cục bộ của bản clone cũ (`067c9599`) **không phải** tổ tiên của `origin/main`, vì bản clone có ref cũ. Phiên đặt lại `main` cục bộ = `origin/main` (`git checkout -B main origin/main`) trước khi merge. Không force lên remote |
| `merge-base --is-ancestor origin/main origin/claude/p-1910-merge-g1b-giong-chot-49iath` | **ĐÚNG** (30 commit phía trước) |
| `git merge --ff-only` | `main` = **`8cedb8af`** |
| `python3 -I checks/lock.py --verify` | LOCK `f4fa0349ca53…0d40` = tính lại → **KHỚP** (VERSION 1.15.0) |
| `tools/preflight.sh --range 5253ba2b..main` | 228 tệp; **1 mục CHẶN: P4** "dấu xung đột merge" ở `reports/g1b-t3/nguoi/giay-phep/mpfb2-LICENSE.txt` (dòng 2 là `=======` của giấy phép nguyên văn), đúng mục báo nhầm đã biết. Mục video V5b-2d `338cef97…` **không bị báo** trong khoảng này. Không có mục lạ |
| `git push origin main` | hook `pre-push` chặn vì đúng mục P4 trên, nên phiên đẩy bằng **`--no-verify` cho riêng lần này** (theo lệnh): `5253ba2b..8cedb8af main -> main`. Không commit mới lên main |
| Nhánh làm việc | `k2c-t3-kl42` tạo từ `main` mới |

## 2. Lời v4.2 (bước 1)
- **Công cụ:** `reports/kl42/lam_v42.py` sinh `script-v4.2-KHOA.md` từ `script-v4.1-KHOA.md`. Công cụ kiểm SHA nguồn v4.1 và SHA nháp, kiểm chỉ đổi vị trí khối và đúng 1 câu. Sau đó `lam_loi_khoa.py` chạy với `LOI=script-v4.2-KHOA.md`.
- **Kiểm độc lập:** `loi-khoa.txt` mới so với nháp `loi-v4.2-NHAP.txt` (`d48c2333…`) chỉ khác đúng dòng 69:

```diff
- All summer, the garrison had been digging through the north face. By early July, Sergeant Ince's thirteen men had cut about eighty-two feet of solid rock.
+ That summer, they had been digging through the north face. By early July, Sergeant Ince's thirteen men had cut about eighty-two feet of solid rock.
```

- **Kịch bản:** ‹2o› (câu A + claim {S080} {S081}) và ‹2p› (kèm dòng [TRÊN HÌNH] Montero) nằm giữa ‹KA1782› và ‹2j›. Dòng tựa đổi thành "lời v4.2 KHOÁ 19/10/2026 … v4.2 = D11". Không dòng nào khác đổi (kiểm bằng so tập dòng đã sắp).
- **Lưu ý:** `lam_loi_khoa.py` sinh lại PLS từ bảng gốc thời Eric (alias VIẾT HOA, chưa có Đ3). PLS lúc đó tạm thành `3a70a020…`. `sua_pls_gcc.py` lấy lại `tu-dien.json` bản Đ3, kiểm danh mục 47 mục trùng, rồi áp GC-C.

**SHA cũ → mới** (`LOI-KHOA.sha256`; các dòng `# cũ` v4 và v4.1 được giữ; `sha256sum -c` cho 3/3 OK):
| Tệp | v4.1 (@8cedb8af) | v4.2 |
|---|---|---|
| kịch bản | `script-v4.1-KHOA.md` `7e0cdc0b218cdcd3fee6d091f1bff9fbef261de5c812d5653b9ce8ed0dbe5a34` | `script-v4.2-KHOA.md` **`d19211148db3e16a597d6b16e3bdd31178e39605fb88d88bd96511800ac1236f`** |
| `loi-khoa.txt` | `0fdc72ce81e33b6f4efc8234a52dafc5410d4448c26c0a0feb3eb01abaa71753` | **`51d1c7735a106efdefc3f466ad77ea03cabdade4d38e7d513cc0e5227d6e431c`** |
| `khoa-loi/phat-am/gibraltar-eric.pls` | `66ed934a…8e29` (Đ3) | GC-C `8242b87b12a4…397e` → GC-C′ **`714314cfc6cfff5e2abde6abec660e5137bddb34d20d08eeefff53053338305b`** |

**Số từ:** 1 571 → **1 567 từ** viết (−4); 9 169 ký tự lời. Sau alias, chữ gửi là 9 884 ký tự (6 chương).

## 3. Từ điển phát âm và 47 mục (bước 2)
### 3.1 GC-C (`sua_pls_gcc.py`, `sua-pls-gcc.json`)
| Mục | Trước | Sau |
|---|---|---|
| isthmus | `ISS-muss` (đã là `iss-muss` theo lệnh) | `iss-muss` → **GC-C′ `issmus`** (§3.3) |
| Diego de Salinas | `dee-AY-go deh sah-LEE-nahs` | `dee-ay-go deh sah-lee-nahs` |
| Algeciras | `Al-heh-SEE-rahs` | `al-heh-see-rahs` |
| San Roque | `San ROH-keh` | `san roh-keh` |
| Tangier | `tan-JEER` | `tan-jeer` |
| Utrecht | `YOO-trekt` | `yoo-trekt` |
| Duc de Crillon | `Dook duh Kree-YOHN` | `dook duh kree-yohn` |
| La Línea de la Concepción | `la lee-nay-ah deh la Kon-sep-SYON` | `la lee-nay-ah deh la kon-sep-syon` |
| Cádiz (dự phòng, không có trong lời) | `KAH-deeth` | `kah-deeth` |

Sau khi sửa, không alias nào còn ≥ 2 chữ hoa liền nhau (có kiểm bằng mã). Các mục Đ3 đã duyệt (`Elliot`, `Rook`, `Hessa Darm-shtat`, `Inss's`) giữ chữ hoa đầu, không đổi.

### 3.2 Kiểm 47 mục, G1, v2, speed 1,03, seed 19102026 (`kiem47.py`, `kiem47.json`, nghe `nghe/G1-47-muc-s1.03.mp3`)
- **Chữ thu:** bảng 41 mục của GIỌNG-CHỐT, cộng 1 câu bổ sung chứa 6 mục trước đây kiểm trong móc/pin (1309, 1782, 1783, 2026, Duc de Crillon, d'Arçon). Tổng 1 180 ký tự.
- **Hai cách nghe như GIỌNG-CHỐT:** M = medium.en beam 5; S = small.en beam 1; không hotwords.
- **Kết quả: 46/47 đạt ở ít nhất một cách nghe, 41/47 đạt ở cả hai, 1 SAI.**

| Mục | M nghe | S nghe | Nhận định |
|---|---|---|---|
| **Cádiz (SAI)** | "Cardiff" | "Cardiath" | Không có trong lời, nên không chặn việc thu. Âm /ˈkɑː.diθ/ hợp với "kah-deeth" theo giọng Anh không cuốn r. ASR viết "Car-" là giới hạn của ASR. Chỉ cần nếu sau này lời có Cádiz; khi đó phải để tai người kiểm |
| Algeciras (NGHI) | "Alhesiras" ✓ | "Al-hesiraz" | giống GIỌNG-CHỐT; âm seseo đúng |
| Duc de Crillon (NGHI) | "Duke du Creon" | "Duc de Crillon" ✓ | |
| La Línea, La Línea's (NGHI) | "la linea", "la lineas" ✓ | "la linaia" | |
| fait accompli (NGHI) | "fête accompli" ✓ | "Fête-Arcomple" | |
| d'Arçon | "D'Arson" ✓ | "Darson" ✓ | **không nghe ra "dar-zone", nên không áp GC-D** |
| isthmus | "isthmus" ✓ | "Ismous" ✓ | đạt ở bảng; nhưng trong lời cả tập lại lỗi (§3.3) |

- Mọi năm, ngày và số đều đúng ở cả hai cách nghe.
- Không có mục nào sai mà phải sửa bằng alias trước khi thu, nên **không DỪNG**.

### 3.3 GC-C′, isthmus (phát hiện trong lượt thu cả tập; `sua_pls_isthmus.py`, `thay.json`, nghe `nghe/isthmus-so-sanh.mp3`)
Ba câu có isthmus (1i#0, 1i#1, 1k#0):

| Bản | Alias · seed | M | S | Kết quả |
|---|---|---|---|---|
| 1. Bản thu cả tập | `iss-muss` · 19102026 | "Isesmus" ×3 | "Icesmus" ×3 | NGHI ×3 (S nghe nguyên âm "ice") |
| 2. Thu lại | `iss-muss` · 19102027 | "ice muss", "ice moss", "IS Mus" | "ice must" ×2, "**I.S.** Musse" | tệ hơn: 2 câu SAI, có lần đọc thành chữ cái |
| 3. Thử | **`issmus`** · 19102026 | "isthmus" ×3 | "isthmus" ×3 | **ĐÚNG 3/3**. **Đã dùng trong stem** |
| 4. Thử | không alias (`isthmus`) · 19102026 | "isthmus" ×3 | "isthmus" ×3 | ĐÚNG 3/3, nhưng không chắc có đọc âm "th" hay không (ASR viết "isthmus" cho cả hai cách đọc) |
| 5. Thử | `iss-mus` · 19102026 | "isthmus", "isthmus", "ESS moose" | …"Ismás", "ESS moose" | 1/3 |

- **Chọn `issmus`:** giữ ý gốc của từ điển ("không đọc âm th"), chữ thường, không gạch nối.
- Đây là **lệch khỏi chữ "iss-muss" của GC-C**, nên ghi là **GC-C′ — chờ chủ dự án duyệt**.
- Nếu chủ dự án không duyệt: bản 1 vẫn còn ngoài git, và `ghep.py` ghép lại được ngay (0 ký tự).
- **Sự cố, 0 ký tự:** lần chạy đầu của `thu_lai.py` vô tình nhập `reports/casting-giong/thu.py`, vì `kiem_tap` chèn thư mục đó vào đầu `sys.path`. Tệp đó gọi TTS với voice_id là "1i", nên bị **404 và không tính phí**. Bộ đếm và nhật ký của casting-giong không đổi. Đã sửa thứ tự nhập.

## 4. Thu cả tập (bước 3) — `thu.py`, `ghep.py`
**Cách thu:**
- G1 `VDLncRBHDjLHBqLhQ1Qt`, `eleven_multilingual_v2`, stability 0,5, similarity 0,75, speed 1,03 (bản 1.03-B), **seed 19102026** (seed của lượt B GIỌNG-CHỐT) cho mọi lệnh.
- Endpoint `/with-timestamps`, định dạng `mp3_44100_192` (gói Creator không có PCM).
- Mỗi chương tách thành phần ≤ 1 900 ký tự ở ranh giới đoạn, vì proxy cắt lệnh dài ~30 s (BAI-HOC, prep.py T2). Mỗi phần gửi kèm `previous_text`/`next_text` trong chương, ≤ 900 ký tự mỗi bên.
- **Nối:** cắt lặng đầu/cuối mỗi phần theo năng lượng (giữ 80 ms đầu, 150 ms cuối). Đặt phần sau sao cho khoảng ngừng ở chỗ nối bằng trung vị khoảng ngừng tự nhiên giữa các đoạn của chính chương đó. Không kéo nhịp.
- Câu thu lại được ghép đè vào đúng khoảng của câu cũ (½ khoảng ngừng tới câu kề, ≤ 0,25 s), rồi dời mốc phía sau.

| Chương | Lệnh (ký tự) | Ký tự gửi | Ngữ cảnh (không tính phí*) | Lời liền (s) | Lời theo shot (s) | Ngừng nối | Thu lại | ASR từ đúng M / S | Mục ĐÚNG/NGHI/SAI |
|---|---|---|---|---|---|---|---|---|---|
| 00 HOOK | 589 | 589 | 0 | 42,68 | 36,41 | — | 0 | 1,000 / 1,000 | 13 / 0 / 0 |
| 01 ROCK | 1 740 | 1 740 | 0 | 128,09 | 118,68 | — | **3 câu isthmus** (12 lệnh thử, 988 ký tự; chọn `issmus`) | 0,958 / 0,944 | 53 / 0 / 0 |
| 02 SIEGE | 1 737 + 1 180 | 2 917 | 1 800 | 217,14 | 200,26 | 0,86 s | 0 | 0,979 / 0,977 | 76 / 1 / 0 |
| 03 NEUTRAL | 1 085 | 1 085 | 0 | 79,74 | 71,94 | — | 0 | 0,969 / 0,943 | 24 / 0 / 0 |
| 04 RUNWAY | 1 472 | 1 472 | 0 | 105,09 | 97,48 | — | 0 | 0,976 / 0,964 | 37 / 0 / 0 |
| 05 GATE | 1 812 + 269 | 2 081 | 1 169 | 150,79 | 141,55 | 0,79 s | 0 | 0,983 / 0,977 | 55 / 0 / 0 |
| **Tổng** | 8 lệnh | **9 884** | | **723,53** | **666,31** | | 988 | | **258 / 1 / 0** |

\*Bộ đếm tăng 0,44 × ký tự `text` ở mọi chương, kể cả chương có ngữ cảnh. Vậy `previous_text`/`next_text` không bị tính phí.

**ASR toàn tập** (`kiem_tap.py`, `kiem-tap.json`):
- Theo **từng câu**, cửa sổ ±0,6 s quanh mốc câu.
  - Số/năm: mọi giá trị trong câu khoá phải nghe ra.
  - Tên: các mục từ điển, cộng mọi từ viết hoa giữa câu, khớp mờ ≥ 0,75. Có thêm cách so bỏ dấu và bỏ khoảng trắng.
- Câu chưa ĐÚNG được nghe lại **tách riêng** (±0,3 s), vì ASR cả chương đổi theo ngữ cảnh dù âm thanh không đổi. Ví dụ: Diego de Salinas ở lượt kiểm thứ hai nghe "D. A. Gaudet" ở cả chương, nhưng câu tách thì M nghe đúng nguyên văn. Hai kết quả đều được ghi.
- **Lần sửa bộ kiểm** (không phải lỗi đọc; BAI-HOC #104):
  - faster-whisper viết "15 ,000", có khoảng trắng trước dấu phẩy, làm hỏng bộ đọc số (8 mục "SAI" giả).
  - "Charles III", "Philip V" bị coi là tên "Third", "Fifth".
  - "fête-à-com-pli" bị tách bằng gạch nối.
  - Sau khi sửa, kiểm lại toàn tập trên cùng bản thu.
- **Kết quả: 259 mục → 258 ĐÚNG, 1 NGHI, 0 SAI; mọi số và năm ĐÚNG ở cả hai cách nghe.**
  - NGHI: **Algeciras** ở 2c (M "Alhaciras/Alhaysiras", S "Alhay-Sih-Raz"). Đây là cách ASR tiếng Anh viết âm seseo "al-heh-see-rahs" đúng; thu lại không đổi được, nên **không thu lại**, để tai người.
- **Chỗ lệch còn lại ở mức từ:** cách viết của ASR ("Rook", "Elliott", "northeast", "forever", "race course", "28.6%" làm mất chữ "point"), sở hữu cách ("merchant's"), "crossers" → "crosses", và tên đọc theo alias ("Montair O" = `mon-tair-oh`, "Darson", "Duc de Creon"). Không chỗ nào là thiếu hay thừa câu.

**Stem ngoài git** (`/var/tmp/cine-out/kl42/stem/`):
- `00.wav` … `05.wav`: thô, 48 kHz, 24-bit.
- `T3-loi-tho.wav`: 733,53 s; các chương cách nhau 2,0 s, chỉ để nghe. SHA `79ac3589…ef21`.
- `moc.json`: mốc câu và đoạn.

## 5. Phát âm cần tai người (khi nghe bản đủ)
| Chỗ | Ở đâu | Lý do |
|---|---|---|
| isthmus `issmus` (GC-C′) | 1i, 1k (chương 01) + `nghe/isthmus-so-sanh.mp3` (khối 1 = bản cũ, 2 = thu lại `iss-muss`, 3 = `issmus` đang dùng, 4 = không alias) | cần duyệt |
| Algeciras | 2c (chương 02) | ASR chỉ NGHI |
| Diego de Salinas | 1d | S nghe "D. A. Gaudet": alias `dee-ay-go` có nghe như đọc chữ cái không? |
| Montero | 2r | S "Montayo" (0,75) |
| fait accompli | 4b | S "Fête-Arcomple" (0,75) |
| La Línea / La Línea de la Concepción | 3d, KC1910, 5… | M "La Linaire" |
| d'Arçon | 2l | M "Darcon", S "Darson"; không nghe ra "dar-zone" (GC-D không áp) |

## 6. Loudness và tệp xuất — `xuat.py`, `xuat.json`
- **Cách chuẩn:** khuếch đại tuyến tính, cộng `alimiter` trên tín hiệu nâng mẫu ×4 (trần −1,5 dBFS). Đo bằng `ffmpeg ebur128`, bù tuyến tính tới khi lệch ≤ 0,1 LU.
- Không nén, không EQ, để `master.py` xử lý lời khi trộn. Với tệp MP3 xem: đo trên chính tệp MP3 và hạ trần nếu đỉnh vọt (BAI-HOC #69).

| Tệp | I (LUFS) | TP (dBTP) | LRA | Thời lượng | SHA-256 | Nơi |
|---|---|---|---|---|---|---|
| Stem thô | −19,0 | −1,7 | 3,8 | 733,532 s | `79ac35890190d62d6d87f0d31310ef1850ff2bd4efd264e8d9388a2d4f94ef21` | ngoài git |
| **Master WAV** 48 kHz/24-bit mono (+5,3 dB) | **−14,1** | **−1,5** | 3,8 | 733,532 s | `ba50fba75aa956731226f7269adbffb6728853d6d2a7fc95b4eefba8e13b586d` | ngoài git `/var/tmp/cine-out/kl42/xuat/T3-loi-G1-v42-14LUFS.wav` |
| **Master FLAC** | −14,1 | −1,5 | 3,8 | | `852b9e419b40d16657f3280dfb03ef7c422c50434fa63db57c2ace8e5b29b7de` | ngoài git `…/T3-loi-G1-v42-14LUFS.flac` |
| Bản xem 1 (chương 00–02), MP3 96 kb/s | −14,2 | −1,2 | | 0 → 392,9 s | xem `xuat.json` | **git** `nghe/T3-loi-G1-v42-xem-1-ch00-02.mp3` (4,72 MB) |
| Bản xem 2 (chương 03–05) | −14,2 | −1,3 | | 392,9 → 733,5 s | xem `xuat.json` | **git** `nghe/T3-loi-G1-v42-xem-2-ch03-05.mp3` (4,09 MB) |

- **Bản thu đủ ngoài git mất khi container bị thu hồi.** Cache theo băm nằm ở `/var/tmp/cine-out/kl42/raw/`.
- Thu lại có seed sẽ cho kết quả gần giống, nhưng không bảo đảm y hệt. **Phiên P/V7 nên chép master FLAC sang nơi lưu bền** theo quy ước `out/` của PLAN.md (FLAC ≈ 30 MB: không gửi qua giao diện).

## 7. Nhịp thật và bảng giãn shot (bước 4) — `nhip.py`, `lam_bang.py`, **`bang-gian-shot.md`**, **`nhip-that.json`** (B), `nhip-that-A.json`
- **Lời theo shot = 666,3 s**, lời liền trong chương = 723,5 s, stem = 733,5 s.
- Tốc độ: 1 567 từ / 666,3 s = 2,35 từ/s khi đang nói; 2,17 từ/s nếu tính cả ngừng giữa đoạn (GIỌNG-CHỐT đo móc 1,03-B: 2,21).
- Mốc bắt đầu/kết thúc từng câu và từng shot lấy theo alignment ký tự của ElevenLabs. Có ở hai hệ toạ độ: trong chương và trong stem. Kèm vị trí đề xuất trên trục phim.
- Thứ tự shot theo v4.2: 2o, 2p đứng trước 2j. `treatment.json` không bị sửa.

| Phương án | Phim | Thay đổi | Ưu | Nhược / rủi ro |
|---|---|---|---|---|
| **B (đề xuất)** | **745,000 s** | 12 shot giãn (+30,3 s); 13 shot rút đuôi hình sau lời xuống ≤ 1,37 s (−6,5 s; lớn nhất 2o −2,04 s, 4f −0,79 s, 1a −0,71 s, 4d −0,67 s) | đạt mục tiêu 735–745 s; không đụng giọng; đuôi ≥ 1,37 s sau lời vẫn thoáng; không đổi khung neo, mốc đinh, cú liên hoàn hay tấm im lặng | rút một chút nhịp hình ở 13 shot. Lệnh GIỌNG-CHỐT từng có luật "không rút shot đang dư", nên **cần chủ dự án chấp thuận rút** |
| A | 751,500 s | chỉ giãn 12 shot | không rút gì | vượt 745 s 6,5 s (+0,87 %); +4,38 % so với trần 720 s (vẫn ≤ +5 %) |
| C (để so) | 745,6 s (×1,02) · 743,4 s (×1,03) | kéo nhịp lời sau thu | 0 ký tự | rủi ro tiếng máy, phải nghe; cần thêm một lượt ASR |

So với bảng GIỌNG-CHỐT §5 (ước):
- 2o không còn cần +6 s, vì ở v4.2 nó không hứng lời chảy từ 2k–2n. Phần đó nay rơi vào **2q** (+4,6 s).
- **1d** (+2,75 s), **2j** (+1,9 s), **5a** (+1,75 s) và **2h** (+1,46 s) phải giãn theo lời thật, dù bảng ước không có.
- 0d không cần giãn nữa.
- Lời SM3 chảy sang 4g (+3,4 s) trước KB1943; lời 5j kết thúc trước KA2026 ≥ 0,4 s.
- **Kiểm cả hai phương án:** không lời nào cách lời kế < 0,4 s, không lời nào vào tấm im lặng, không lời nào tràn ra cuối phim.

## 8. AUTHORSHIP (bước 5)
Thêm 2 dòng ở cuối bảng:
1. **P10C-3…P10C-5 nguyên văn** (duyệt 18/10 23:49), chép đúng lời trong lệnh. Dòng này thay phần "nguyên văn chưa có trong repo" của dòng P-1910.
2. **D11 câu nối = A.** Lệnh KL42 **không ghi giờ chọn**, nên dòng ghi "giờ chọn: chờ chủ dự án bổ sung". Phiên không tự điền giờ.

## 9. Ký tự ElevenLabs và chi phí
| Hạng mục | Ký tự gửi |
|---|---|
| Kiểm 47 mục (speed 1,03) | 1 180 |
| Thu cả tập, 6 chương, 8 lệnh | 9 884 |
| Thu lại và thử alias isthmus: 4 bộ × 3 câu, gồm 1 bộ thu lại seed 19102027 và 3 bộ thử `isthmus`/`issmus`/`iss-mus` | 988 |
| **Tổng phiên** (`nhat-ky-ky-tu.jsonl`, 21 lệnh) | **12 052** (mốc theo dõi 14 000: 86 %; mức chặn 18 000: 67 %) |

**Bộ đếm tài khoản** (`bo-dem.jsonl`; đọc trước/sau mỗi lượt, chờ 90 s):
- **135 707** (06:22 UTC) → 136 226 (kiểm 47) → 136 485 → 137 251 → 138 534 → 139 011 → 139 659 → 140 574 (sau 6 chương) → 140 684 (bộ thu lại đầu; dòng bộ đếm không được ghi vì script dừng sau khi thu, bộ đếm đọc ở lần chạy sau) → … → **141 009**.
- **Tổng tăng +5 302 = 0,440/ký tự gửi**, đúng tỷ lệ 0,44 của BAI-HOC #103. Không có phần tăng nào chưa giải thích được.
- Giới hạn 171 534, **còn 30 525** tới 01/11/2026 06:57 UTC.

| Hạng mục khác | Số |
|---|---|
| Claude API | **$0** (không gọi `claude -p`); 0 subagent. Token phiên chính không đo được trong phiên |
| OpenAI / YouTube | 0 / 0 |
| Giờ máy | ≈ 75 phút (ASR 2 cách nghe toàn tập × 3 lượt kiểm ≈ 35 phút) |
| Tài khoản ElevenLabs | không thêm, không xoá, không đổi giọng |

## 10. Việc chờ chủ dự án
1. **Nghe bản thu đủ:** `reports/kl42/nghe/T3-loi-G1-v42-xem-1-ch00-02.mp3` rồi `…-xem-2-ch03-05.mp3` (≈ 12 phút 14 giây). Các chỗ nên chú ý ở §5. Nếu có câu cần thu lại, ghi mã shot và số câu; mỗi câu tốn ≈ 40–130 ký tự.
2. **Duyệt GC-C′:** isthmus `issmus` thay `iss-muss`. Nghe `nghe/isthmus-so-sanh.mp3`.
3. **Chọn bảng shot:** B (745,0 s, có rút đuôi ở 13 shot) hay A (751,5 s, chỉ giãn). Chỉ xét C nếu muốn kéo nhịp lời (phải nghe trước). Bảng ở `bang-gian-shot.md`.
4. **Cho giờ chọn D11 = A** để ghi vào dòng AUTHORSHIP.
5. **Lưu master FLAC** (`/var/tmp/cine-out/kl42/xuat/`, SHA ở §6) sang nơi lưu bền trước khi container bị thu hồi. Việc này thuộc phiên P/V7.
6. Việc của phiên P: merge nhánh `k2c-t3-kl42` (phiên này không merge). G1b/V7 dời 2o, 2p trong treatment theo v4.2 và đặt lời theo `nhip-that.json`.

## 11. Tệp (`reports/kl42/`)
- **Hồ sơ:** `KL42-BAO-CAO.md`, `bang-gian-shot.md`, `CHECKPOINT.md`.
- **Số đo:** `kiem47.json`, `kiem-tap.json`, `thay.json`, `nhip-that.json`, `nhip-that-A.json`, `xuat.json`, `sua-pls-gcc.json`, `sua-pls-isthmus.json`, `nhat-ky-ky-tu.jsonl`, `bo-dem.jsonl`.
- **Tệp nghe:** `nghe/T3-loi-G1-v42-xem-1-ch00-02.mp3`, `nghe/T3-loi-G1-v42-xem-2-ch03-05.mp3`, `nghe/isthmus-so-sanh.mp3`, `nghe/G1-47-muc-s1.03.mp3`.
- **Công cụ:** `lam_v42.py`, `sua_pls_gcc.py`, `sua_pls_isthmus.py`, `kl_lib.py` (trần 18 000), `kiem47.py`, `thu.py`, `thu_lai.py`, `ghep.py`, `kiem_tap.py`, `xuat.py`, `nhip.py`, `lam_bang.py`, `nghe_isthmus.py`.
