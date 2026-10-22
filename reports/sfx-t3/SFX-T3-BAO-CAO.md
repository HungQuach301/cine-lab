**Nhánh thật: `claude/laughing-ptolemy-u7xlwe`** — harness của phiên buộc nhánh này (lệnh ghi `sfx-t3`). Nhánh tạo lại từ `origin/main` @ `96b5017c`, đúng gốc lệnh. **Không merge.**

# SFX-T3 — SFX và âm nền theo hình cho bản cuối T3 Gibraltar (Kinh thánh §16) — DỪNG chờ chủ dự án

> Phiên SFX-T3, 22/10/2026, 00:05 → 00:55 UTC. Phiên chỉ nghiên cứu, chọn tiếng và trộn thử. **Chưa trộn bản cuối.**
>
> **Vùng sửa:** chỉ `reports/sfx-t3/**`, tổng ≈ 24 MB, không dùng LFS. Tệp tiếng ứng viên lớn nhất 1,23 MB (≤ 2 MB). Không sửa `assets/`, `channel-*/`, `design/`, `scripts/`, `checks/`, `docs/`, sổ, `main` hay nhánh khác. Không đụng vùng của ANIMATIC-T3-V2.
>
> **Đã đọc:**
> - `reports/m3/BAI-HOC-LL.md`.
> - `docs/BIBLE-KENH2.md` §4 (âm thanh L1–L7), §11.2 (tấm im lặng), §14.6, §16.
> - `channel-k2/k2c-t3-01/animatic/bang-shot.md`, `bang-shot.json`, `anim-loi.json`, và `log-shot.json` (mốc giờ/năm trong từng shot).
> - `reports/nhac-t3/NHAC-T3-BAO-CAO.md` và `cue/cue-B.json`.
> - `reports/kl42/nhip-that.json`.
> - `RIGHTS.md` (AM-01…, K2-MUS-1…13), `assets/audio/sfx/LIBRARY.yaml`.
> - Mã `scripts/audio/master.py`, `lib.py`, `measure.py` và `reports/nhac-t3/cong-cu/tron.py`, `goi_nghe.py`. Các tệp này **chỉ được import**, không sửa.

## Khối điều lệ
| Trường | Lệnh | Thực tế |
|---|---|---|
| Nhánh | `sfx-t3` từ origin/main @96b5017c | `claude/laughing-ptolemy-u7xlwe` (harness buộc), gốc đúng @96b5017c; 5 commit (commit cuối chỉ sửa dòng này); đã đẩy; không merge |
| Vùng sửa | `reports/sfx-t3/**` ≤ 40 MB, không LFS, tệp tiếng ≤ 2 MB OGG/FLAC | ≈ 24 MB; 41 tệp OGG ứng viên, lớn nhất 1,23 MB; gói nghe 4 MP3 (0,74–0,90 MB); 0 tệp LFS |
| Chi phí | Claude mốc $3, chặn $10; dịch vụ khác 0 | Claude API **$0** (không gọi `claude -p`), 0 subagent. Token phiên chính không đo được trong phiên, nên không tự khai. OpenAI / Gemini / ElevenLabs / RunPod / YouTube **0**. Không mua, không đăng ký |
| Preflight | bắt buộc | Hook `pre-commit` + `pre-push` (preflight → `git lfs pre-push`) cài từ commit 2. Mọi lần đẩy sau đều **ĐẠT**, `lock.py --verify` **KHỚP**. **Sự cố:** lần đẩy đầu chạy trước khi cài hook; xem dòng dưới |
| Email / khoá | che email; không đưa email chủ dự án vào header/URL/payload/UA | Không có email chủ dự án ở bất kỳ đâu. UA mọi lệnh tải: `CineLab-research (+https://github.com/HungQuach301/cine-lab)`. Không in, không ghi khoá |
| **Sự cố email** | — | Commit đầu `699403cb` được đẩy **trước** khi cài hook. Commit này có 2 email công khai **của bên thứ ba**: email liên hệ của trang BigSoundBank và email trong thông báo 429 của Wikimedia. Tôi đã che cả hai, sửa commit trên nhánh của phiên (`--amend` + `--force-with-lease`), nên lịch sử nhánh chỉ còn `8d1e9e2c`. Commit cũ `699403cb` có thể còn truy được trên GitHub theo SHA cho tới khi GitHub dọn |
| Trang bị chặn | ghi nguyên văn, không vượt chặn | Freesound 403 rỗng; Pixabay và Sonniss 403 (Cloudflare challenge); Wikimedia API 429. Nguyên văn ở `giay-phep/bi-chan.txt`. Không dùng mirror, cache hay WebFetch để vượt |
| Đẩy việc dở | ≤ 30 phút | đẩy lúc 00:2x, 00:3x, 00:38 và lúc kết thúc; có `CHECKPOINT.md` |
| Dừng hỏi | không dừng giữa chừng | đúng |
| Môi trường | `verify.sh` | 10 ĐẠT, 5 TRƯỢT (OpenEXR, three.js, tifffile/pyshp, k2v node_modules; Freesound 403 là mục tuỳ chọn). Phiên không cần mục nào trong các mục trượt |

---

## 0. Tóm tắt (đọc 2 phút)
1. **Giới hạn phải nói trước:** phiên này **không nghe được bằng tai**. Để bù, việc chọn và loại tiếng dựa trên 4 thứ:
   - Mô tả của người ghi âm.
   - Số đo kỹ thuật: LUFS, đỉnh thật, sàn nhiễu, băng thông.
   - **Soát nội dung bằng mô hình phân loại AudioSet chạy cục bộ** (AST, giấy phép BSD-3; không gửi tiếng ra ngoài). Mô hình tìm động cơ, xe, máy bay, lời nói, nhạc theo cửa sổ 10 s.
   - Số đo trộn thật với lời G1.

   Việc "hợp hình, đúng cảm xúc, không giả" thuộc về tai chủ dự án, chấm qua gói nghe mù (§4.3).
2. **Nguồn:**
   - Freesound, kho được ưu tiên, **bị proxy chặn** (403). Pixabay và Sonniss cũng bị chặn (Cloudflare), Wikimedia trả 429. Lỗi ghi nguyên văn.
   - Phiên dùng 3 nguồn đọc được giấy phép nguyên văn, không có NC/ND/SA:
     - **BigSoundBank** (Joseph Sardin, ghi âm thật, CC0 1.0).
     - **NPS Sound Gallery** (tài sản công Mỹ, 17 U.S.C. §105). Có pháo thật ở Fort McHenry, hoả mai, trận tái hiện, biển, máy bay cánh quạt.
     - **OpenGameArt** (chỉ mục CC0).
3. **Ứng viên:** 41 đoạn cắt cho 19 loại âm (§2).
   - Soát AST **bắt được 5 lỗi** mà đọc mô tả không thấy:
     - Tệp "mòng biển" NPS thực ra bị nhận là **cú** (Owl 0,73).
     - "Cảng cá" BSB có **bíp lùi xe tải**.
     - Hoả mai NPS còn **tiếng hô "fire!"** trùng lúc nổ.
     - "Mòng biển ở cảng" BSB bị nhận là **quạ**.
     - Một tệp tải về bị cắt cụt.
   - Các tệp lỗi đã bị loại, hoặc đánh dấu **CHỜ TAI** và rút khỏi trộn thử.
4. **Bản đồ âm 43 shot (§1):**
   - 41 shot có SFX. 2 tấm im lặng **KB1943 và KA2026 không có SFX** (§11.2: chỉ hình + nhạc; KA2026 giữ nhạc A đã duyệt). 2 thẻ phương pháp cũng không có SFX.
   - Có kiểm thời kỳ tự động: không có tiếng động cơ trước năm 1900 trong hình, và không có máy bay trước 1934.
5. **Trộn thử (§4).** Hai đoạn, mỗi đoạn 2 bản (không SFX / có SFX), cùng nhạc B và lời G1 **master FLAC** (lần đầu trộn trên master thật; NHẠC-T3 phải dùng MP3 96 kb/s).

   | Đoạn | Bản | I (LUFS) | TP sau AAC (dBTP) | Lời trên nền p10 / min (dB) |
   |---|---|---|---|---|
   | Móc | không SFX | −13,9 | −1,5 | 20,00 / 19,11 |
   | Móc | có SFX | −13,9 | −1,4 | **18,54 / 17,11** |
   | Pin nổi | không SFX | −13,9 | −1,5 | 19,43 / 19,16 |
   | Pin nổi | có SFX | −13,9 | −1,5 | **16,87 / 16,33** |

   Cả 4 bản **ĐẠT §4** (p10 ≥ 15 / min ≥ 12). Gói nghe mù X/Y: 2 cặp MP3, −14,0 LUFS, −1,8…−1,9 dBTP, đo trên chính tệp. Khoá ở `nghe-mu/khoa.json`.
6. **Gói đề xuất cả phim (§5):** 206 sự kiện, 35 tệp, 41 shot.
   - Mỗi sự kiện **neo** vào đầu shot, vào khe lời (câu thứ k của dòng lời) hoặc vào mốc ngày/năm trong shot (`log-shot.json`). Vì vậy bản cuối áp lại được khi V2 đổi máy.
   - **Đo kiểm cả phim** (chỉ đo, không xuất bản trộn): −14,0 LUFS, −1,3 dBTP sau AAC, **p10 18,65 / min 16,45 dB**. Bản không SFX: 19,58 / 18,25, trùng số NHẠC-T3 (19,58 / 18,23), nên chuỗi đo được xác nhận chéo.
   - 0 lỗi kiểm: tấm im lặng và thời kỳ. Bộ kiểm đã bắt và tôi đã sửa 1 lỗi thật: máy bay ở 4g tràn vào KB1943.
7. **Đề xuất (§7): duyệt gói theo hướng "tối giản dưới lời"**, sau khi nghe mù.
   - Mức SFX trong lúc có lời thấp hơn nhạc ≈ 8–12 dB. Điểm nhấn chỉ đặt vào khe giữa các câu.
   - Rủi ro chính:
     - 4 tệp chưa được tai kiểm (máy bay, còi tàu 1940, hoả mai NPS, mòng biển BSB).
     - Không có tiếng máy bay thập niên 1940 thật nào qua được kiểm giấy phép.
     - Content ID với tư liệu công NPS và các tệp thiết kế trên OpenGameArt (§6).

**Chỉ số trong ±5 % quanh ngưỡng (nêu tên theo luật cứng):**
| Chỉ số | Đo | Ngưỡng | Lệch |
|---|---|---|---|
| Loudness 4 bản trộn thử (WAV từ `master.py`) | −13,9 LUFS | dải −15,0…−13,8 | cách cận trên 0,1 LU (0,7 %) |
| Loudness đo kiểm cả phim, 2 bản | −14,0 LUFS | dải −15,0…−13,8 | cách cận trên 0,2 LU (1,4 %) |
| Loudness 4 tệp nghe mù (MP3) | −14,0 LUFS | đích −14,0 ± 0,1 | 0 % |
| Các chỉ số SMR | p10 thấp nhất 16,87; min thấp nhất 16,33 dB | 15 / 12 | +12,5 % / +36 % — **ngoài** dải ±5 % |
| Đỉnh thật sau AAC | −1,3 … −1,5 dBTP | ≤ −1,0 | dư 0,3–0,5 dB, **ngoài** dải ±5 % |

---

## 1. Bản đồ âm theo shot (`ban-do-am.md` / `ban-do-am.json`)
**Mức so với lời** (Kinh thánh §4; "nền" gồm nhạc + SFX). Thang dưới đây là LUFS trước master, khi lời ở −17 LUFS. Chuỗi `master.py` còn hạ SFX thêm ½ mức duck của nhạc trong lúc có lời.

| Mức | Nghĩa | LUFS trước master |
|---|---|---|
| N0 | im, không SFX | — |
| N1 | nền xa | ≈ −41 … −46 |
| N2 | nền rõ | ≈ −35 … −40 |
| N3 | điểm nhấn trong khe lời, không trùng từ | ≈ −27 … −31 |
| N4 | ngang nhạc | chỉ khi không có lời (4g) |

**Thời kỳ:**
- **P**: trước 1900. Không động cơ, không đường phố hiện đại, không tiếng nói nghe rõ chữ.
- **M1**: 1900–1945. Cho phép máy bay cánh quạt từ 1934 và còi tàu.
- **M2**: từ 1946.

Bộ kiểm trong `cong-cu/goi.py` đọc năm trong hình ở từng giây (`log-shot.json`) và báo mọi tiếng sai thời kỳ.

| # | Mã | Phim (s) | Thời kỳ | Lớp âm (mức) | Ghi |
|---|---|---|---|---|---|
| 1 | H1 | 0,0–12,0 | M2 | đêm (dế) N1; phố/xe xa N1; bước chân N2; gió N1 | vào ở 0,0 s cùng lời, dốc 1,5 s |
| 2 | H2 | 12,0–28,0 | 2026→P | gió N2; pháo rất xa N2 dưới bộ đếm 14 lần vây (15,4–19,9 s); cờ 1704 N2 (20,0–22,4 s); pháo N3 trong khe 22,1–22,5 s và 26,7–28,0 s; lửa pin nổi N1 | 12,0–15,3 s (2026 chiều): chỉ gió |
| 3 | H2T | 28,0–33,0 | P | lửa lớn N2; sóng vỗ N1; nổ xa N3 trong khe 31,9–33,0 s | |
| 4 | H3 | 33,0–43,8 | M1→M2 | cánh quạt xa N1 (1939–43); phố 2026 N1 từ 39,0 s; gió N1; **J-cut biển 1704 vào 42,8 s** | không có động cơ trước 1939 (BAI-HOC #105: âm vào trước hình) |
| 5 | N1.1 | 43,8–62,6 | P | biển N2; gió; dây/gỗ tàu; sóng + mòng biển | hạm đội 1704 |
| 6 | N1.2 | 62,6–89,4 | P | pháo xa dày dần ở 1d; phố trong tường rất xa (lọc 1,2 kHz) | |
| 7 | N1.3 | 89,4–104,5 | P | cờ N2; gió; bước chân lính N1 | không trống/kèn (không có nguồn sạch) |
| 8 | N1.4 | 104,5–118,5 | P | dòng dân rời phố N1 (lọc 0,9 kHz, không rõ chữ); bước chân; gió | |
| 9 | N1.5 | 118,5–147,6 | P→M2 | gió, biển; phố chỉ từ mốc 2015 | đổi nền đúng cú bước năm |
| 10 | N1.6 | 147,6–173,1 | P | pháo vây 1704–05 và 1727; đá + xẻng từ mốc 1730 (Línea) | |
| 11 | C1 | 173,1–195,6 | P | trại TBN rất xa; ngựa; bếp trại; gió; vải lều | |
| 12 | C2 | 195,6–207,6 | P | biển; mái chèo thuyền châu Phi; gió; mòng biển | |
| 13 | C3 | 207,6–221,7 | P | gió (cận người hái rau); cờ; sóng khi cần cẩu lên | |
| 14 | C4 | 221,7–235,2 | P | sóng Old Mole; mái chèo, dây; người khiêng thùng rất xa | |
| 15 | C5 | 235,2–247,7 | P | pháo TBN N3 sau khi neo (238,8 s); phố cháy từ mốc 15:00; dân chạy (02:30) | |
| 16 | N2.6 | 247,7–262,2 | P | pháo xa; lửa nhỏ; đá rơi (phố sập); pháo N3 sau câu 2h#1 | |
| 17 | KA1782 | 262,2–270,2 | P | gió; một phát pháo rất xa; sóng | khung neo có lời |
| 18 | N2.10 | 270,2–288,5 | P | đào (xẻng, đá); nổ lỗ thông hơi N3 sau câu 2p#1 | |
| 19 | N2.7 | 288,5–303,0 | P | pháo đạn nung; công sự cháy N2 | |
| 20 | N2.8 | 303,0–327,0 | P | biển; dây/gỗ tàu neo; gió; sóng + mòng biển | |
| 21 | N2.9 | 327,0–355,0 | P | **đoạn trộn thử 2** — §4.2 | |
| 22 | N2.11 | 355,0–382,6 | P | gió mùa đông; **một phát pháo cuối** ngay sau "the last shot was fired" (370,2 s) | sau phát đó không còn tiếng pháo |
| 23 | N3.1 | 382,6–409,8 | P | gió, biển; 1810: San Felipe nổ (mốc 08:00), Santa Bárbara nổ trong khe 405,9 s | |
| 24 | N3.2 | 409,8–418,3 | P | gió, sóng, mòng biển | |
| 25 | N3.3 | 418,3–428,3 | P | phố La Línea thế kỷ 19 rất xa; xe ngựa | |
| 26 | KC1910 | 428,3–435,3 | M1 | phố tiếng Tây Ban Nha N2 (lọc 3,5 kHz); ngựa; bước chân | không ô tô |
| 27 | N3.4 | 435,3–462,3 | M1 | gió N2; hai phố rất xa | không thêm tiếng dựng rào (không có nguồn sạch) |
| 28 | N3.5 | 462,3–471,6 | M1 | gió; một lượt cánh quạt xa từ mốc 1934 | |
| 29 | N4.1 | 471,6–497,1 | M1 | đá, xẻng (làm đường băng); cánh quạt từ mốc 1941 | không máy xúc có bíp lùi |
| 30 | N4.2 | 497,1–525,5 | M1 | nổ mìn vách bắc N3; đá đổ; sóng; máy bay | |
| 31 | N4.3 | 525,5–533,7 | M1 | máy bay xa; gió; sóng + mòng biển | |
| 32 | N4.4 | 533,7–550,6 | M1 | còi tàu sơ tán; biển; máy bay dày dần trong 4g (không lời) | **tắt hết trước 550,4 s** |
| 33 | **KB1943** | 550,6–558,6 | M1 | **N0 — im** | tấm im lặng §11.2: chỉ hình + nhạc (B8 Echoes) |
| 34 | N4.5 | 558,6–585,8 | M1 | động cơ dọc đường băng N1–N2; biển; gió | vào lại bằng dốc 1 s; không còi (đoàn tàu tắt đèn) |
| 35 | N5.1 | 585,8–609,6 | M2 | dòng người + bước chân → **tắt khi cổng đóng 6/1969**; trở lại ở mốc 1985 | khoảng im 1969–85 kể bằng âm |
| 36 | KB2026 | 609,6–619,1 | M2 | quảng trường hôm nay; phố; sóng + mòng biển | |
| 37 | N5.2 | 619,1–631,6 | M2 | bước chân giờ cao điểm; người; phố | |
| 38 | KC2026 | 631,6–641,6 | M2 | phố La Línea; tiếng Tây Ban Nha lọc 4 kHz | |
| 39 | N5.3 | 641,6–666,1 | M2 | bước chân, người, phố, gió (N1) | |
| 40 | N5.4 | 666,1–697,5 | M2 | người qua cổng; phố; gió | không thêm tiếng gỡ rào kim loại (không có nguồn sạch) |
| 41 | N5.5 | 697,5–717,0 | P→M2 | biển, gió, mòng biển | không chèn tiếng theo từng năm; Hiraeth dâng |
| 42 | **KA2026** | 717,0–725,0 | M2 | **N0 — im** | tấm im lặng, **giữ phương án đã duyệt** (nhạc A), không SFX |
| 43 | N5.6 | 725,0–745,0 | P→M2 | gió; phố 2026 (mốc 13:00); đêm + phố xa từ mốc 19:30 | đoạn 1730/1783: chỉ gió |
| — | PP1, PP2 | 745,0–761,0 | — | N0 | thẻ phương pháp |

**Về "khói":** khói không có tiếng riêng. Gió và lửa xa gánh phần này; phiên không thêm tiếng "giả khói".

---

## 2. Ứng viên và giấy phép (`ung-vien.md`, `ung-vien/ung-vien.json`, `giay-phep/`)
### 2.1 Giấy phép nguyên văn (đọc 22/10/2026)
- **BigSoundBank**, https://bigsoundbank.com/licenses.html (`giay-phep/bigsoundbank-licenses.txt`):
  - Trang giấy phép: *"You are allowed to: Share, copy, distribute and communicate the material by all means and in all formats. Adapt, remix, transform and create from material. Use, including for commercial purposes. Without any restrictions. Without asking permission. This is: Creative Commons CC0 1.0 Universal …"*
  - Chân trang: *"All files whose download page mentions "Free and Royalty Free" are made available free of charge and freely for all your projects, whether commercial or not, and worldwide."*
  - **Trang của cả 30 tệp BSB được chọn đều ghi** *"CC0 (public domain): Free and royalty-free"*. Dòng của từng trang lưu ở `ung-vien.json → dong_giay_phep_trang`.
  - Mã s#### khớp với trang đã quét. Một URL tôi gõ đoán đã được sửa theo trang thật (s0262 "horn-of-a-ship-2").
- **NPS**, https://www.nps.gov/aboutus/disclaimer.htm, mục Ownership (`giay-phep/nps-disclaimer.txt`):
  - *"Copyright law does not protect "any work of the U.S. Government" … material created by the National Park Service and presented on this website, unless otherwise indicated, is generally considered in the public domain."*
  - Kèm điều kiện cho dùng thương mại: *"when such information is published or republished commercially … the copyright notice must include a reference to the original U.S. Government work … such as: "No claim to original U.S. Government works.""* → **bản bán phim phải có dòng này trong credit.**
  - Mỗi trang tiếng ghi "Credit / Author: NPS".
- **OpenGameArt:** từng trang ghi "License(s): CC0 → http://creativecommons.org/publicdomain/zero/1.0/". Văn bản CC0 1.0 lưu ở `giay-phep/cc0-legalcode.txt`.
- **Không dùng:** Freesound (403), Pixabay và Sonniss (Cloudflare 403; giấy phép gói GDC không đọc được), Wikimedia (429). Nguyên văn ở `giay-phep/bi-chan.txt`. Không có tệp nào có NC/ND/SA.

### 2.2 Số đo và soát
Đầy đủ ở `ung-vien.md`. Gồm: I/TP/sàn nhiễu/băng thông của tệp gốc (`so-do/do-ung-vien.json`), top-1 AudioSet, điểm "hiện đại" lớn nhất, điểm "lời" lớn nhất, số lần dùng trong gói và trạng thái.

Công cụ soát `cong-cu/phan_loai.py`:
- Mô hình AST AudioSet (MIT, BSD-3), bản ONNX lượng tử hoá, chạy bằng onnxruntime cục bộ.
- Đặc trưng fbank Kaldi dựng lại bằng numpy, vì môi trường không có torch. Lần đầu tôi để sai thang ×32768 và sai cửa sổ; đã sửa sau khi kiểm trên 4 tệp đã biết nội dung (pháo → Explosion 0,70; biển → Waves 0,85).
- Đây chỉ là **công cụ soát**: số có thể lệch nhẹ so với bản gốc, và nó không thay tai.

| Loại | Ứng viên (★ = dùng chính trong gói) | Ghi |
|---|---|---|
| Pháo xa/gần | ★PXA-1 NPS Fort McHenry (pháo nạp đầu nòng thật, 2,7 s, 16 kHz); ★PXA-2 OGA thimras "Cannon fire"; PXA-3 BSB s1023 (súng hơi doạ chim, lọc xa) | Loạt pháo = chùm PXA-1/2/3 lệch nhau 80–170 ms, pan khác nhau. PGAN-1 (NPS trận Cedar Creek) để **dự phòng** vì có tiếng người la |
| Hoả mai | ★HOAMAI-2 BSB s2853 (súng săn, vọng đồng); HOAMAI-1 NPS Minute Man — **CHỜ TAI** | HOAMAI-1: cắt ở mọi điểm 2,65–2,85 s vẫn còn Speech 0,44–0,62 (tiếng hô trùng lúc nổ); phần đuôi riêng thì sạch |
| Nổ lớn | ★NO-1 OGA thimras "ship_destroyed" (nổ + cháy + biển, 18,5 s); NO-2 BSB s1806; NUOC-1 OGA "cannon_miss" (đạn rơi xuống biển) | |
| Lửa lớn / nhỏ | ★LUAL-1/2/3 BSB s0988/s0989/s0987 "Big branching fire"; ★LUAN-1 BSB s2855 "Fireplace #3"; LUAN-2 OGA — **LOẠI** (Vehicle 0,165) | Lửa BSB có độ động lớn (bị hạ 12–21 dB vì trần đỉnh), nên mức trong gói đặt theo LUFS thật |
| Sóng/biển | ★SONG-1 BSB s0698 Đại Tây Dương (120–160 s); ★SONG-2 BSB s1448 sóng nhỏ cách 10 m (110–150 s); ★SONG-3 NPS Olympic (sóng + mòng biển, 6,6 s) | **Loại s2564 Dellec:** "Boat" 0,2–0,6 suốt tệp, nghi có thuyền máy. **Loại s2570:** tải về bị cắt cụt (31/333 s) |
| Gió | ★GIO-2 BSB s0625 (gió mạnh trong làng, 15–55 s); ★GIO-1 BSB s0146 (gió thông); GIO-3 OGA "wind1" (tổng hợp PureData, sạch nhất) | |
| Chim biển | ★SONG-3 (mòng biển trong tiếng sóng NPS); CHIM-1 BSB s2573 "Gulls on the Harbor" 5–33 s — **CHỜ TAI** | CHIM-1: AST nhận là **quạ** (Crow 0,72). Các đoạn khác của s2573 có động cơ/lời. **Loại NPS "Western Gull"**: tệp trên trang bị nhận là **cú** (Owl 0,73), nghi tệp không khớp trang. **Loại** OGA "Solo Seagull" vì lấy từ một video YouTube, quyền không kiểm được |
| Đám đông | ★DONG-3 BSB s0684 walla 25 người; ★DONG-1 BSB s0825 đám đông tiếng Tây Ban Nha; ★DONG-2 BSB s3515 50–60 người | Tiếng Pháp/Tây Ban Nha **luôn lọc thấp 0,9–4 kHz**, mức −39…−47 LUFS, nên không nghe ra chữ. Cảnh trước 1900 dùng lọc 0,9–1,5 kHz |
| Bước chân | ★BUOC-1 BSB s1318 (bê tông, 2026); ★BUOC-2 BSB s0839 (sỏi, trước 1946) | |
| Ngựa | ★NGUA-1 BSB s1854; NGUA-2 BSB s1852 | |
| Thuyền / dây | ★THUYEN-1 BSB s1514 (mái chèo, foley ván gỗ); ★THUYEN-2 BSB s3426 (dây thừng lớn kẽo kẹt) | |
| Cờ | ★CO-1/CO-2 BSB s1632/s1633 (vải cầm tay, không cột kim loại) | |
| Đào / đá | ★DAO-1 BSB s1305 (xẻng); ★DAO-2 BSB s1022 (đá rơi) | **Loại** OGA "breaking-rock" và "catching-fire" (làm lại từ tệp Freesound, không kiểm được giấy phép gốc). **Loại** s0631–s1638 "Roadworks" (máy xúc, bíp lùi) |
| Máy bay 1930–40s | MAYBAY-1 NPS "Propeller Plane" GGNRA — **CHỜ TAI** | Đây là máy bay nhỏ hiện đại, không rõ đời máy; AST không nhận ra máy bay (Gong/Hum, băng thông 99 % chỉ 201 Hz). **Không tìm được tiếng máy bay thập niên 1940 thật qua được kiểm giấy phép.** **Loại** OGA "war-on-water": tác giả ghi lấy từ Freesound mà không ghi công được |
| Phố/xe 2026 | ★PHO-1 BSB s3188 (trung tâm phố, 8/2024); ★PHO-2 BSB s0602 (quảng trường đi bộ); ★PHO-3 BSB s0621 (đêm sau mưa, đường xa) | **Loại** s2571 "Small fishing port": bíp lùi xe tải (Reversing beeps 0,62) |
| Đêm yên | ★DEM-1 BSB s1880 (dế, ếch); DEM-2 OGA "crickets" | |
| Còi tàu 1940 | COI-1 BSB s0262 — **CHỜ TAI** | Còi tàu khách hiện đại, dùng cho tàu sơ tán 1940. Chỉ dùng 1 lần, lọc 4 kHz |

---

## 3. Đoạn cắt (`ung-vien/*.ogg`)
- 48 kHz Vorbis q6, giữ số kênh gốc, chuẩn tuyến tính về −23 LUFS. Nếu đỉnh vượt −1 dBFS thì hạ chung (lượng hạ ghi ở `ha_vi_dinh_db`). Dốc 10 ms ở hai đầu. Không nén, không EQ; lọc và đặt mức làm khi trộn.
- SHA của tệp tải về nguyên vẹn ở `so-do/sha-goc.txt`; SHA của đoạn cắt ở `ung-vien.json`.

---

## 4. Trộn thử (`cong-cu/tron_thu.py`, `su-kien/moc.json`, `su-kien/pin.json`, `so-do/tron-*.json`)
**Chuỗi** (giống hệt cho bản không SFX và bản có SFX):
- Nhạc B theo `cue-B.json`, dựng bằng nguyên hàm `nen()` của NHẠC-T3; tệp nhạc lấy từ `assets/k2/music` (LFS, `sha256sum -c` khớp 8/8 dòng của `SHA256SUMS`).
- Lời G1 **master FLAC** (`852b9e41…`) đặt theo `anim-loi.json`.
- Hoàn thiện bằng nguyên hàm `master.finish()`: lời −17 LUFS → duck thích ứng (nhạc −12 dB cơ bản; SFX hạ ½ mức đó) → 2 lượt loudness −14 LUFS, trần −1 dBTP, kiểm sau AAC.
- SMR đo trên stem lời so với **nền = nhạc + SFX đã duck**.

### 4.1 Móc mở đầu 0,0–45,0 s (19 sự kiện)
- **H1:** đêm 2026 (dế, đường xa, bước chân qua đường băng) → bình minh (sóng + mòng biển).
- **H2:** gió → 6 tiếng pháo rất xa (lọc 1,5 kHz) dưới bộ đếm 14 lần vây → cờ 1704 → pháo trong khe 22,1 s → pin nổi khai hoả (3 tiếng dưới lời, 2 tiếng trong khe 26,7–28,0 s) → lửa.
- **H2T:** lửa + sóng vỗ + nổ xa trong khe 31,9 s.
- **H3:** cánh quạt xa (1941) → phố 2026 → **J-cut** biển 1704 vào 1 s trước cú cắt sang N1.1.

### 4.2 Pin nổi 321,0–358,0 s (28 sự kiện)
- Hạm đội (biển, dây tàu).
- Garrison bắn khi pin vào vị trí, trong khe 330,6 s.
- **Từ 333,9 s (10:25 trong hình)**: pháo dày dần dưới lời, lọc xa, pan ngẫu nhiên có hạt giống 1782.
- **Loạt lớn ngay sau "…opened fire together." trong khe 342,9–344,2 s**, rồi đạn rơi xuống biển.
- Cú lặn: lửa đêm + sóng → pin nổ trong khe 348,06 s (đuôi kéo dưới lời 2n) → nổ xa 352,4 s.

### 4.3 Số đo
| Đoạn | Bản | I / LRA / TP (dBTP) / TP sau AAC | SMR p10 / min / trung vị (dB), số cửa sổ | Duck trung vị / sâu nhất (dB) | Cửa sổ thấp nhất (giây phim: dB) |
|---|---|---|---|---|---|
| Móc | không SFX | −13,9 / 2,8 / −1,5 / −1,5 | 20,00 / 19,11 / 24,81 (21) | −12,0 / −13,3 | 23: 19,11 · 22: 19,93 |
| Móc | **có SFX** | −13,9 / 2,8 / −1,5 / −1,4 | **18,54 / 17,11** / 21,68 (21) | −12,0 / −14,0 | 33: 17,11 (đầu H3) · 22: 17,83 |
| Pin | không SFX | −13,9 / 2,3 / −1,5 / −1,5 | 19,43 / 19,16 / 20,29 (23) | −15,9 / −16,4 | 350,2: 19,16 |
| Pin | **có SFX** | −13,9 / 2,1 / −1,5 / −1,5 | **16,87 / 16,33** / 19,19 (23) | −16,5 / −17,3 | 349,2: 16,33 · 348,2: 16,43 (đuôi nổ pin dưới 2n) |
| Cả phim (đo kiểm gói, 206 sự kiện) | không SFX | −14,0 / 3,1 / −1,5 / −1,4 | 19,58 / 18,25 / 21,95 (439) | −13,95 / −16,5 | 239,7: 18,25 |
| Cả phim | **có SFX** | −14,0 / 3,1 / −1,5 / −1,3 | **18,65 / 16,45** / 20,99 (439) | −14,2 / −17,4 | 349,2: 16,45 · 406,7: 16,46 (nổ 1810) · 292,5: 16,56 |

- Cả 6 bản: 0 quãng lặng bất thường, 0 lần chạm trần, loudnorm tuyến tính.
- Cân bằng trước master (cả phim): SFX trong lúc có lời **−35,96 LUFS**, nhạc **−24,1** → SFX thấp hơn nhạc ≈ 12 dB. Ngoài lời, SFX ở −32,6.
- Đoạn pin, ngoài lời: SFX −22,9 so với nhạc ≈ −22. Điểm nhấn được lên ngang nhạc trong khe, có chủ ý.

**Đọc số:**
- SFX lấy của lời 1,5–2,5 dB SMR, nhưng chỗ thấp nhất vẫn dư ≥ 4,3 dB so với ngưỡng min 12 dB.
- Chuỗi duck chỉ phải hạ nhạc sâu thêm 0,7–0,9 dB.
- Chỗ "tốn" nhất là đuôi tiếng nổ kéo dưới lời (348–350 s, 406,7 s). Nếu tai thấy lấn lời, sửa bằng cách rút đuôi NO-1 từ 6 s xuống 3 s, không cần hạ cả gói.

### 4.4 Gói nghe mù (`nghe-mu/`, 3,3 MB)
- 2 cặp X/Y: `1-moc-*.mp3` (45 s, 0,90 MB) và `2-pin-noi-*.mp3` (37 s, 0,74 MB).
- MP3 160 kb/s; I = −14,0 LUFS; TP = −1,8 / −1,9 dBTP, đo trên chính MP3 (BAI-HOC #69, #121: `alimiter level=disabled`).
- Hai bản trong cùng cặp có cùng kích thước tệp, nên không lộ bản.
- X/Y gán bằng `secrets.randbelow(2)`. Khoá và SHA ở `khoa.json` — **chỉ mở sau khi chấm.** Hướng dẫn và phiếu ghi ở `HUONG-DAN-NGHE.md`.

---

## 5. Gói SFX đề xuất cho bản cuối (`goi-de-xuat.md` / `goi-de-xuat.json`; dòng RIGHTS: `de-xuat-RIGHTS.md`)
- **35 tệp, 206 sự kiện, 41 shot.** Mỗi dòng gồm: shot, giây phim (theo bảng shot v1), tệp, **neo**, mức (LUFS trước master), độ dài, dốc vào/ra, lọc/pan, ghi chú.
- **Lời và mức chung:** nền phủ shot, dốc vào 1,5 s / ra 2,0 s tại ranh shot. Điểm nhấn trong khe lời bắt đầu sau từ cuối 20–50 ms. Không tiếng nào chạm tấm im lặng: tiếng cuối trước KB1943 tắt ở 550,4 s; nền sau KB1943 vào từ 558,6 s bằng dốc 1 s; nền trước KA2026 tắt ở 716,6 s.
- **35 dòng RIGHTS đề xuất** (`K2-SFX-T3-01…35`) theo đúng cột của `RIGHTS.md`: tài sản, nguồn/URL tệp, tác giả, trích giấy phép nguyên câu + link, phạm vi, ghi công, SHA gốc và SHA đoạn. **Phiên P ghi vào sổ** khi chủ dự án duyệt; tệp chép vào `assets/k2/sfx/t3/` (đề xuất). Phiên này không sửa sổ.
- **Ghi công:**
  - CC0 không bắt buộc ghi công. Đề xuất credit "Additional sounds: Joseph SARDIN – BigSoundBank.com" và tên tác giả OGA trong mô tả.
  - **Bản bán phim bắt buộc** dòng "No claim to original U.S. Government works" (NPS).

### 5.1 Cách bản cuối áp gói khi bảng shot V2 đổi máy (các shot eo đất)
1. **Thời gian không phải đặt lại bằng tay.** Nhịp lời B cố định, nên neo `khe:<dòng>#k` giữ nguyên. Neo `moc:<ngày/năm>` tự tính lại từ `log-shot.json` của V2 khi chạy `cong-cu/goi.py`. Neo `shot` nền đi theo `t0/dur` mới của shot.
2. **Shot nào V2 đổi máy** (điểm nhìn, hướng, AGL, kiểu khung), chỉnh 3 tham số cho từng nguồn có vị trí (pháo, đám đông, ngựa, cờ, nổ):
   - pan = sin(góc phương vị của nguồn − hướng máy), kẹp ±0,8;
   - mức += −20·log10(d_V2 / d_V1) dB, kẹp ±6 dB;
   - với tiếng xung (pháo, nổ): lọc thấp ≈ 8000·√(100 / d) Hz, kẹp 1–8 kHz.

   Nền (gió, biển) giữ nguyên, trừ khi kiểu khung đổi:
   - lai → chặt có vai: +3 dB cho lớp tiền cảnh (cờ, bước chân, ngựa);
   - chặt → lai: −3 dB.
3. **Thứ tự chạy:** sửa `goi.py` → chạy lại → bộ kiểm phải báo 0 lỗi (tấm im lặng, thời kỳ) → `tron_thu.py su-kien/ca-phim.json` đo SMR cả phim (p10 ≥ 15, min ≥ 12) → mới trộn bản cuối bằng chuỗi `master.py` (MIX=audio, xuất stem SFX riêng) → master vào LFS kèm SHA (§14.6).
4. **4 tệp CHỜ TAI** (MAYBAY-1, COI-1, và HOAMAI-1, CHIM-1 không có trong gói): nếu chủ dự án loại MAYBAY-1 hay COI-1, xoá các dòng của chúng trong `goi.py`. Các shot N3.5, N4.1–N4.5 khi đó chỉ còn gió/biển/đá; luật §4 không bị ảnh hưởng.

---

## 6. Rủi ro Content ID và giấy phép
| Nguồn | Giấy phép | Rủi ro Content ID | Ghi |
|---|---|---|---|
| BigSoundBank (30 tệp) | CC0 1.0, ghi âm của chính tác giả | **Thấp – trung bình.** CC0 bị bên thứ ba gom vào thư viện rồi đăng ký Content ID là rủi ro có thật. Phiên không kiểm được tác giả có đăng ký Content ID hay không (trang giấy phép không nói). SFX nằm dưới lời và nhạc thì khó khớp vân | Giữ bằng chứng: URL, dòng giấy phép của trang, ngày đọc, SHA gốc. Khiếu nại thì dùng bộ này |
| NPS (3 tệp trong gói: PXA-1, SONG-3, MAYBAY-1) | Tài sản công Mỹ | **Trung bình – thấp.** Tư liệu công hay bị bên thứ ba đăng ký trong tuyển tập | Ngoài Mỹ, tác phẩm chính phủ Mỹ về lý thuyết có thể được bảo hộ ở nước khác; rủi ro thấp. Bản bán phim cần dòng "No claim…" |
| OpenGameArt thimras (PXA-2, NO-1, NUOC-1) | CC0 do người đăng khai | **Trung bình.** Tiếng thiết kế (Winter Jam 2022), **không ghi vật liệu gốc**. Nếu tác giả dựng từ thư viện thương mại thì có thể bị claim | Giảm rủi ro: PXA-2 luôn đi trong chùm với PXA-1 (NPS); NO-1 chỉ dùng 4 lần. Có thể thay toàn bộ bằng PXA-1 / NO-2 nếu chủ dự án muốn rủi ro thấp nhất |
| OpenGameArt khác (GIO-3 tổng hợp, DEM-2) | CC0 | GIO-3 thấp (tổng hợp PureData). DEM-2 không dùng trong gói | |
| Đã loại vì giấy phép | — | — | Freesound / Pixabay / Sonniss (không đọc được); OGA "war-on-water", "breaking-rock", "catching-fire" (làm lại từ Freesound); OGA "Solo Seagull" (lấy từ video YouTube) |
| Nhạc B (đã có, K2-MUS-6…13) | CC BY 4.0 | Smart Content ID (đã nêu ở NHẠC-T3) | SFX không làm đổi rủi ro này |

---

## 7. Quyết định đề xuất
**SFX-1. Duyệt gói "tối giản dưới lời" làm nền cho bản cuối T3, sau khi chủ dự án nghe mù 2 cặp.**
- *Ưu:*
  - Đúng §16: CC0 hoặc tài sản công, ghi RIGHTS từng tiếng, trộn dưới lời theo §4.
  - Số thật đạt luật trên cả phim với master FLAC (p10 18,65 / min 16,45).
  - Điểm nhấn kể chuyện bằng âm: phát pháo cuối 1783, cổng đóng 1969 thành im, pháo đài nổ 1810, J-cut vào chương 1.
  - Tôn trọng hai tấm im lặng.
  - Có neo để áp sau V2.
- *Nhược:* mức SFX thấp (thấp hơn nhạc ≈ 12 dB trong lúc có lời), nên trên loa điện thoại có thể khó nghe ra. Lớp máy bay 1940s yếu.
- *Tác động:* bản cuối thêm 1 stem SFX. Trộn bằng chuỗi `master.py` sẵn có, không đổi mã.
- *Rủi ro:* tai chủ dự án có thể thấy một tiếng giả, sai chỗ hoặc lặp lộ (phiên không nghe được); Content ID (§6).

**SFX-2 (chọn trong nghe mù):** mức tổng của SFX.
- Nếu "quá nhỏ": nâng nền +3 dB. SMR còn dư (min 16,45 → ước ≈ 15,5).
- Nếu "quá to": hạ −3 dB.

**SFX-3 (rủi ro Content ID thấp nhất):** thay 3 tệp thiết kế OGA (PXA-2, NO-1, NUOC-1) bằng PXA-1 / NO-2.
- *Ưu:* chỉ còn ghi âm thật có nguồn rõ.
- *Nhược:* mất tiếng "cháy + nổ + biển" liền mạch của NO-1 ở đêm pin nổi.

**SFX-4 (máy bay 1940s):**
- (a) giữ MAYBAY-1 lọc xa và thấp (hiện tại); hoặc
- (b) bỏ tiếng máy bay, chỉ để gió/biển;
- (c) phiên sau tìm tiếng máy bay thật thời 1940s có giấy phép rõ, ví dụ phim tài sản công NARA, phải tách được tiếng khỏi lời bình và nhạc. Tốn thêm 1 phiên, rủi ro không tìm được bản sạch.

---

## 8. Chi phí thật
- Claude API **$0**, 0 subagent; token phiên chính không đo được.
- OpenAI / Gemini / ElevenLabs / RunPod / YouTube: **0**.
- Tải miễn phí: mô hình AST ONNX 90 MB từ Hugging Face (BSD-3, không tài khoản), ≈ 0,8 GB tiếng gốc (để ngoài git, chỉ ghi SHA).
- Không mua, không đăng ký dịch vụ trả phí.
- **Dòng COST-LEDGER** (phiên P ghi): `SFX-T3, 2026-10-22, Claude $0, khác $0`.

## 9. Việc chờ chủ dự án
1. **Nghe mù 2 cặp X/Y** (`nghe-mu/HUONG-DAN-NGHE.md`). Chọn bản hay hơn; ghi chỗ SFX lấn lời, tiếng sai thời kỳ hoặc giả; mức (nhỏ / vừa / to). Sau đó mới mở `khoa.json`.
2. **Tai kiểm 4 tệp CHỜ TAI:** MAYBAY-1, COI-1 (đang trong gói), HOAMAI-1, CHIM-1 (đang ngoài gói). Giữ hay loại từng tệp.
3. Quyết **SFX-1** (gói), **SFX-2** (mức), **SFX-3** (thay tiếng thiết kế OGA), **SFX-4** (máy bay 1940s).
4. Sau khi duyệt, phiên P:
   - ghi 35 dòng RIGHTS (`de-xuat-RIGHTS.md`);
   - chép tệp vào `assets/k2/sfx/t3/`;
   - thêm dòng "No claim to original U.S. Government works" và credit BigSoundBank vào mẫu mô tả/credit;
   - ghi AUTHORSHIP cho các lựa chọn sáng tạo đã duyệt (vị trí phát pháo cuối, im lặng khi cổng đóng 1969, J-cut chương 1);
   - cân nhắc ghi vào sổ AI việc dùng mô hình phân loại AST để soát (cục bộ, không sinh nội dung).
5. Không có xung đột với `main` (main vẫn @96b5017c) hay với ANIMATIC-T3-V2 (khác vùng). Bản cuối chạy `goi.py` trên bảng shot V2 khi V2 xong (§5.1).

## 10. Tệp (`reports/sfx-t3/`)
| Tệp | Nội dung |
|---|---|
| `SFX-T3-BAO-CAO.md` | báo cáo này |
| `ban-do-am.md/.json` | bản đồ âm 45 dòng (43 shot + 2 thẻ) |
| `ung-vien.md`, `ung-vien/*.ogg`, `ung-vien/ung-vien.json` | 41 ứng viên + số đo + soát + metadata nguồn/giấy phép/SHA |
| `giay-phep/` | giấy phép nguyên văn (BigSoundBank, NPS, CC0), `bi-chan.txt` |
| `su-kien/moc.json`, `pin.json`, `ca-phim.json` | sự kiện trộn thử / đo kiểm cả phim |
| `goi-de-xuat.md/.json`, `de-xuat-RIGHTS.md` | gói đề xuất + dòng RIGHTS |
| `nghe-mu/` | 4 MP3 X/Y, `khoa.json`, hướng dẫn |
| `so-do/` | số đo trộn (`tron-moc/pin/ca-phim.json`), đo tệp, soát AST (gốc và đoạn cắt), `sha-goc.txt` |
| `cong-cu/` | `phan_loai.py`, `do_tep.py`, `cat_ung_vien.py`, `dat_loi_flac.py`, `tron_thu.py`, `goi_nghe.py`, `goi.py`, `ban_do.py`, `bang.py` |
| `CHECKPOINT.md` | nhật ký việc dở |

Tệp lớn ngoài git (không phát hành, có thể dựng lại bằng `cong-cu/`): WAV trộn thử và WAV đo kiểm cả phim ở `/tmp/claude-0/sfx/tron/`; tệp tiếng gốc ở `/tmp/claude-0/sfx/dl/` (SHA ở `so-do/sha-goc.txt`).
