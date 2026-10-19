Nhánh thật: `ccr-ef2b66f0-9639kq` (harness buộc tên này; lệnh yêu cầu `v7b`). Gốc: `origin/v7-pilot` @71932a3f + `git merge --no-ff origin/k2c-t3-kl42` (không xung đột; commit 2e23dbaf). Không merge vào `main`. Không sửa `loi-khoa.txt` (v4.2, SHA 51d1c773… kiểm lại khớp), `checks/`, `docs/`.

# V7B T3 Gibraltar — BÁO CÁO: vòng thử 2 của ngữ pháp timelapse

## §0 Tóm tắt

| Việc | Kết quả |
|---|---|
| Merge KL42 | Không xung đột. Ngoài `channel-k2/`, `reports/`, `AUTHORSHIP.md`, merge còn mang theo `docs/BIBLE-KENH2.md` (§13), `RIGHTS.md` và `COST-LEDGER.csv`. Đây là lịch sử P-1910/KL42 đã có trên nhánh KL42, tôi không sửa gì. |
| 1. Giọng thật | Stem G1 v4.2 đặt theo `nhip-that.json` (phương án B): 8 shot, **118,458 s**, 22 câu. Mix **−13,9 LUFS**, đỉnh thật −3,2 dBTP, lời trên nhạc ≈ 16,7 dB. Có hai bản xem: có phụ đề kiểm và không phụ đề. |
| 2. Ai giữ Rock | Cờ đúng mẫu theo nguồn (§2). Năm 1704 thấy cờ Borgoña **hạ** rồi Union **kéo** lên Tower of Homage. Cờ Union ở lâu đài, King's Bastion và Orange's Bastion. Mọi tàu mang cờ đuôi theo phe, soái hạm thêm cờ đỉnh cột. Có viền màu phe §11.1. |
| 3. Khung dày | Định nghĩa góc cao đề xuất: **máy ≥ 120 m trên đất hoặc nhìn xuống ≥ 15°**. Có 4 điểm máy mới/sửa: K, A2, Cc, D thấp hơn. Tỉ lệ khối xây dựng/trại/quân (cùng thước) **tăng nhưng chưa đạt 40 %**: H2 2,7 → 30,9 %, C1 3,4 → 12,9 %, C5 11,0 → 14,5 % (§7). |
| 4. Nhà 2026 | 14 440 toà có màu và kiểu theo nguồn. Mái lấy từ Sentinel-2 2026, có 45 thẻ OSM roof:colour và 16 thẻ building:colour. Tường lấy bảng màu từ 4 ảnh CC của Gibraltar. LOD có cửa sổ kéo tới 2,6 km. |
| 5. Đói + 9/1782 | C3 mở bằng cận ≈ 68 người hái rau dại (đa số cúi), nền là lâu đài có cờ Union và toán lính áo đỏ, rồi cần cẩu lên cao thấy hải đội phong toả. Danh sách 9/1782 (King's Lines 50, Main Guard 37) áp ở H2, đoạn ngày 13/9/1782. |
| 6. Mở đầu | Pin nổi hiện ở **23,8 s**, khai hoả 25,5 s, **cháy 27,0 s** (≤ 30 s). Tua ngược chạy theo **bước năm đều**: 15 bước, mỗi bước giữ 11 khung = 0,458 s, giờ mặt trời cố định. Đoạn chạy liên tục tối đa **0,014 năm/s** ở H2 và **1,9 năm/s** ở H3 (§10.3: ≤ 20). |
| 7. Tự đo | 4,05 cắt/phút; shot TB 14,8 s; góc cao 95,4 % theo định nghĩa (96,7 % theo vai); lướt thấp 3,3 %; khung trống 4/60 (C1, trước ngày dựng trại); tấm chữ 3,0 s (thẻ chương). Có 6 khung cổng PNG 1920×1080. |
| 8. XEM CÂM | Bản cuối (C1-a, lượt 5): từ khoá **22/24**; **P đọc lại 14/24 (58 %)**. Q1 "ai giữ Rock" từ 0 lên **3/6**. **TRƯỢT mục tiêu 18/24.** Cách sửa: §8. |
| Chi phí | Claude API **$0,657**, OpenAI **$0**, ElevenLabs 0, YouTube 0. Giờ máy ≈ **5,5 h** (§10). |

**Xem nhanh:**
- Bản cuối không phụ đề: `reports/v7b/ban-thu/v7b-a-xem-khong.mp4`
- Có phụ đề kiểm: `v7b-a-xem-phude.mp4`
- Tờ so: `reports/v7b/so/to-so-8-cap-a.jpg`
- Khung cổng: `reports/v7b/khung/cong-*.png`
- Chuỗi xem câm: `reports/v7b/xem-cam/a/to-1.jpg`, `to-2.jpg`

## §1 Giọng thật (việc 1)

- **Nguồn tiếng:** dùng bản xem MP3 96 kbps của stem trong git, `reports/kl42/nghe/T3-loi-G1-v42-xem-1-ch00-02.mp3` (SHA e35ca483…). Lý do: master WAV/FLAC của KL42 nằm ngoài git và không còn trong container này. ElevenLabs không tốn ký tự nào. **Bản phát hành phải lấy lại WAV từ phiên KL42/ổ lưu** (xem §12).
- **Cách đặt:** mỗi dòng lời lấy đoạn `[bd_stem, kt_stem]` của nó trong stem, đặt ở `loi_bd_phim` theo `nhip-that.json` B. Đoạn 2 dời về sau mở đầu: 2a nằm ở 43,833 s. Khoảng ngừng giữa các câu trong cùng một shot giữ nguyên như bản thu. Bản đặt âm: `channel-k2/k2c-t3-01/v7p/v7b-loi.json`.
- **Thời lượng shot = `dur_moi` (B):** H1 12,0 · H2 21,0 · H3 10,833 · C1 22,5 · C2 12,0 · C3 14,125 · C4 13,5 · C5 12,5 s.
- **Nhạc tạm** Tyrant.mp3 (K2-MUS) ở −31 LUFS dưới lời. Sau hai lượt loudnorm, mix đạt −13,9 LUFS, LRA 4,1, đỉnh −3,2 dBTP. Lời −14,3 LUFS so với nhạc −31,0 LUFS → lời trên nhạc ≈ 16,7 dB (tích phân; p10 chưa đo).
- **Phụ đề kiểm** `v7b-phu-de.srt` lấy từ mốc câu thật. Chỉ nung vào bản "phude", không đưa vào chuỗi xem câm.

## §2 Ai giữ Rock (việc 2, V7P-D4) — nguồn mẫu cờ

| Cờ | Mẫu | Nguồn mẫu | Dùng ở | Bậc |
|---|---|---|---|---|
| Union 1707–1800 (Great Union, **không** chéo St Patrick) | chữ thập St George viền trắng trên chéo St Andrew, nền lam | Act of Union 1707 / [Red Ensign (Wikipedia)](https://en.wikipedia.org/wiki/Red_Ensign) (chéo St Patrick thêm năm 1801) | Tower of Homage (từ 4/8/1704), King's Bastion, Orange's Bastion | mẫu 3 |
| Red Ensign 1707–1800 | nền đỏ, góc cờ Great Union 1707 | Order in Council 21/7/1707 — [Red Ensign](https://en.wikipedia.org/wiki/Red_Ensign); hệ phân đội cờ [Coloured squadrons](https://en.wikipedia.org/wiki/Coloured_squadrons_of_the_Royal_Navy) | mọi tàu Anh (đoàn Rooke 1704, Rodney 1780, Darby 1781) | mẫu 3; **màu phân đội của từng đô đốc chưa xác minh → dùng đỏ cho mọi đoàn (bậc 4)** |
| Cờ hải quân TBN 1701–1785 | nền **trắng** + huy hiệu hoàng gia Bourbon (giản lược) | [FOTW es1701](https://www.crwflags.com/fotw/flags/es1701.html), [FOTW es1785](https://crwflags.com/FOTW/flags/es1785~c.html): cờ trắng có huy hiệu, đổi sang đỏ–vàng ngày 28/5/1785 vì dễ lẫn với cờ các nước Bourbon; chưa đọc được nguyên văn sắc lệnh 1785 | hải đội Barceló (C2–C4), hạm đội liên quân và pin nổi 1782 (H2) | mẫu 3; huy hiệu giản lược bậc 4 |
| Cruz de Borgoña | chéo đỏ răng cưa trên nền trắng | cờ trung đoàn TBN theo quy định 1734 ([FOTW es^1701](https://cdn.fotw.info/flags/es^1701.html)); [Cross of Burgundy](https://en.wikipedia.org/wiki/Cross_of_Burgundy) | Tower of Homage và King's Bastion trước 4/8/1704; cờ trung đoàn dọc mỗi dãy trại TBN 1779 | mẫu 3; số cờ/vị trí trên trại bậc 5 |
| Cờ trắng Pháp | trắng trơn | hải quân Bourbon Pháp | trại Pháp 1782 (không có trong đoạn thử) | 3 |

- **Cỡ:**
  - cờ đất liền 6 × 3 m × **1,5** = 9 × 4,5 m;
  - cờ trại 4 × 2 m × 1,5;
  - cờ tàu 8 × 4 m × 1,5 = 12 × 6 m;
  - cỡ gốc là ước tính (bậc 4), hệ số phóng **đúng trần 1,5×** (luật D4) và có ghi trong log từng shot (`co_v7b`, `co_tau`).
- **1704 hạ–kéo** (H2, 7,9–10,4 s cảnh = 19,9–22,4 s phim; máy K cách cờ ≈ 150 m):
  - Borgoña hạ 10:00 → 11:30 ngày 4/8/1704;
  - Union kéo 13:00 → 15:00;
  - giờ trong ngày là minh hoạ;
  - đã kiểm trên khung phóng to: cờ trắng có chéo đỏ, rồi đến Union.
- **Viền phe** (`design/k2v/tl/phe.js`):
  - vòng elip sát mặt nước/đất, màu §11.1: Anh #b03a2e, TBN #c9a227;
  - mờ dần khi máy cách 800 → 1 200 m;
  - không vào mặt nạ nội dung.
  - Lượt 1 viền quá mờ, C2 không thấy. Lượt 2 tăng dày 0,32 và độ đục 0,8.
  - Thuyền tiếp tế từ châu Phi (C2) và tàu chanh Đan Mạch (C4) **không cờ, không viền**, vì phiên chưa có nguồn mẫu cờ của chúng.
- **Rủi ro (§8):** 2/3 người chấm đọc đoàn tiếp viện có viền đỏ thành "tàu đỏ bắn vào phố" ở C5. Ở C5, lời 2g nói đoàn thả neo đúng lúc pháo TBN bắn vào phố.

## §3 Khung dày (việc 3) — định nghĩa góc cao + điểm máy

**Định nghĩa đề xuất:** shot/khung là "góc cao" khi máy ≥ 120 m trên mặt đất **hoặc** trục nhìn chúc xuống ≥ 15°. Đo mỗi 6 khung từ nhật ký máy (`render.js --campath`).

| Shot | Điểm (lượt cuối) | AGL (m) | Nhìn xuống | Thay đổi so V7P |
|---|---|---|---|---|
| H1, H3 | D (thấp/gần hơn) | 242–247 | 12,4–12,6° | 320 → 250 m, lùi 230 m |
| H2 | **K** mới, trên sườn Rock sau lâu đài | 85 | 26,9° | V7P: B trên vịnh, cách 2,2 km |
| C1-a | **A2** mới, giữa dãy trại E5 và E6/E7 | 188–189 | 17,9–18,5° | V7P: A, cách dãy trại 1–2 km |
| C1-b | A (V7P) + Faden 1783 phủ 3 s | — | — | D3-b |
| C2 | E (giữ) | 168–170 | 0,2° | — |
| C3 | cận 30–70 m (AGL ≈ 22) → cần cẩu → Ca | 6–211 | 8–61° | thêm cận người (lướt thấp 3,9 s) |
| C4 | **Bb** mới, cách Old Mole ≈ 450 m | 175 | ≈ 11° | lượt 5 |
| C5 | **Cc** mới, trên South Bastion nhìn dọc phố | 227–229 | 23,2–23,5° | V7P: C-b |

- **Tỉ lệ góc cao (C1-a, lượt cuối):**
  - theo định nghĩa: **95,4 %** (riêng điều kiện AGL ≥ 120 m: 77,5 %; riêng nhìn xuống ≥ 15°: 54,5 %);
  - theo vai, không tính 3,9 s lướt thấp: 96,7 %.
- **C1 (D3), đã thử cả hai cách:** (a) máy A2 gần dãy trại; (b) máy A + Faden 1783 (Yale 2046612, PD) nắn bằng 3 GCP (RMS 12,5 m), phủ khớp địa hình 3 s đúng lúc lời nói "facing the Rock" rồi tan vào trại.
- **Kết quả xem câm lượt 4 (cùng phần khác, chỉ khác C1):**
  - từ khoá: a 18, b 17;
  - P đọc lại: a 10, b 11;
  - Q2 "1779 bắt đầu gì" 6/6 ở cả hai.
- **Chọn (a) làm bản cuối:** khối trại trong khung 12,9 % so với 5,8 % của (b), không có khung trống ở C1 lượt 5. Ở 320×180, bản đồ Faden phủ chỉ hiện như "vùng cát" (R2 lượt 4: "the sandy close-up has no context").
- **(b) vẫn giữ trong repo:** `episode-v7b-b.yaml`, bản xem `v7b-b-xem-*.mp4` (lượt 4).
- **Vì sao C1 vẫn thưa:** theo nguồn, tới 10/1779 mới có ≈ 14 000 quân (35 % số lều của đợt 1782). Lều 3 × 2,4 m, dãy trại sâu ≈ 100 m. Cây bụi hiện nay trong dải trại ±110 m đã được ẩn (bậc 5).

## §4 Nhà 2026 có vật liệu (việc 4) — `scripts/k2tl/v7b_mau_nha.py` → `pack/buildings-v7b.json`

| Lớp | Nguồn | Số toà |
|---|---|---|
| Mái | **Sentinel-2 L2A TCI 15/4/2026** (Copernicus, 10 m): trung vị điểm ảnh trong dấu chân. Đỏ hơn lam ≥ 40 % → ngói; còn lại → mái bằng xám/trắng | 14 440 (ngói 9 501, bằng 4 939; trung bình 1,7 điểm ảnh/toà) |
| Mái / tường theo thẻ OSM | `roof:colour` 45 · `building:colour` 16 (đọc thẳng từ tệp .osm, khớp tâm ≤ 15 m) | 61 |
| Tường | bảng màu theo nhóm dùng × số tầng (`design/k2v/tl/data/mau-nha-v7b.json`). Rút bằng k-means từ vùng mặt tiền được nắng của 4 ảnh Commons: *Europort Avenue* (CC BY-SA 2.0, 2009), *Gibraltar Harbour 03* (CC BY 3.0, Oltau, 2008), *Moorish Castle from the housing estate below* (CC BY 3.0, HJ Mitchell, 2011), *Rock of Gibraltar Europort Avenue* (CC BY-SA 3.0) | Gibraltar 862 · La Línea 13 578 (dùng bảng vôi trắng Andalucía có sẵn, bậc 5) |
| Kiểu mặt đứng | OSM `building=*` (Gibraltar) / Catastro `u` (La Línea) + chiều cao → tháp chung cư, ở, công nghiệp, văn phòng kính | toàn bộ |

- **Giới hạn:**
  - **chưa có ảnh 2020s** (Commons trả 429 cho proxy, đúng BAI-HOC #82); ảnh dùng được là 2008–2011;
  - La Línea không có ảnh nào;
  - màu tường là bảng màu vùng (bậc 4), không phải màu từng toà.
- `city.js`: thêm hai tham số `near` (ô LOD có cửa sổ, 1 400 → 2 600 m) và `winFar` (chi tiết cửa sổ tắt dần tới 2 400 m).
- **Khung hero** (`cong-hero.png`) có tường trắng/kem/vàng cát, mái ngói theo S2, cửa sổ ở tầm 1–2,5 km. Mảng xám lớn còn lại là đường băng, sân đỗ và đường phố, đúng như thật.

## §5 Đói có hình + danh sách 9/1782 (việc 5, V7P-D5/D6)

- **C3, 0–3,9 s (lướt thấp, vai "khoảnh khắc người"):**
  - ≈ 68 người (34 cặp, nửa nữ) hái rau dại trên sườn dưới lâu đài; 80 % đang cúi 0–37° (`people.js` thêm tham số `lean`);
  - toán 16 lính áo đỏ gác dưới lâu đài;
  - nền là Tower of Homage có cờ Union cách ≈ 290 m;
  - lượt 4 người cúi tới 60° trông như ngã, đã giảm.
- **C3, 3,9–7,6 s:** cần cẩu lên điểm C, thấy phố, Line Wall có cờ Union, hải đội TBN phong toả (cờ trắng, viền vàng).
- **Nguồn:** S052 (hái rau dại, bậc 2). Vị trí và số người minh hoạ (bậc 5).
- **C4:**
  - 5 thuyền chở hàng đi từ đoàn Rodney vào Old Mole;
  - 360 thùng hàng chất trên Mole (S054; số và vị trí minh hoạ);
  - người bốc hàng và lính áo đỏ ở bến.
  - Ở cỡ khung chấm, thùng và người chưa đọc được (§8).
- **Danh sách 9/1782 (D6):** mọi mục trong danh sách chỉ hợp ngày 1–9/9/1782, nên chỉ áp vào H2 đoạn 13/9/1782: King's Lines 50 người trên King's Bastion và Main Guard 37 trên Line Wall (Spilsbury 7/9/1782; vị trí minh hoạ). Không áp lệch ngày sang 1779–1781 (§12.3).

## §6 Mở đầu (việc 6; D2 không miễn §10.3)

- **H2, tua ngược bằng bước năm đều:**
  - 2026 (giữ 3,3 s) → 1309 → 1316 → 1333 → 1333 → 1350 → 1411 → 1436 → 1462 → 1467 → 1506, mỗi bước giữ 11 khung;
  - **4/8/1704 chạy chậm 2,5 s** (cờ hạ–kéo);
  - → 1705 → 1727 → 1779 → 13/9/1782 06:45 chạy liên tục tới 14/9 02:30.
- **Chống nhấp nháy:**
  - mốc thời gian đặt đúng lưới khung, nên không có khung nào mang năm trung gian;
  - giờ mặt trời cố định 15:30 trong mọi bước.
- **Phố trước 1704:** dùng lớp tái dựng 1705 làm đại diện (bậc 5). Phố trong tường thời Trung cổ có thật nhưng chưa có bản đồ trước 1704; V7P để trống, sai hơn.
- **H3:** V7P chạy 1943,6 → 2026 trong 3 s (≈ 28 năm/s, **trái §10.3**). Nay là 1938,6 → 1943,6 liên tục (≤ 1,9 năm/s), rồi bước năm 1969 → 1985 → 2026.
- **Mốc pin nổi** (giây phim, đo từ đường cong): hiện 23,83 · vào vị trí 25,33 · khai hoả 25,46 · cháy 26,96.

## §7 Số đo (việc 7; ghi số, không tự chấm đạt) — `reports/v7b/do/do-v7b-a.json` (bản cuối), `do-v7b-b.json`

| Chỉ số | V7P | **V7B (C1-a, lượt 5)** | Mục tiêu |
|---|---|---|---|
| Thời lượng / số shot | 119,1 s / 8 | 118,458 s / 8 | — |
| Cắt/phút · shot TB | 4,03 · 14,9 s | **4,05 · 14,8 s** | ≤ 5 · ≥ 12 s |
| Góc cao (định nghĩa §3) | 100 % (theo vai) | **95,4 %** (theo vai 96,7 %) | ≥ 75 % |
| Lướt thấp | 0 % | **3,3 %** (C3 cận người 3,9 s) | ≤ 10 % |
| Khung "trống" (đất phẳng tự nhiên > 60 %) | 0/60 | **4/60** (C1, 44–50 s, 20/6–13/7/1779, trước khi dựng trại) | — |
| Tấm chữ | 3,0 s | **3,0 s** (thẻ chương) | — |
| Trôi máy | 0,06–0,38 %/s | 0,03–0,25 %/s; C3 là cần cẩu (207 %/s, cú có chủ đích) | ≤ 2 %/s |
| Năm/s, đoạn liên tục | H2 538 · H3 41 | **H2 0,014 · H3 1,88 · còn lại ≤ 0,38** | ≤ 20 |
| Bước năm | — | H2 15 · H3 3 (giữ ≥ 0,458 s) | — |
| Pin nổi cháy | 29,3 s | **26,96 s** | ≤ 30 s |

**Khối xây dựng/trại/quân** (`page.js classMask`: chỉ đếm điểm ảnh toà, lâu đài, tường, pháo đài, công sự, phế tích, lều + dải đất trại, khối quân; có địa hình che khuất; cây và tàu không che khuất; 1 khung/2 s). Đo cùng thước cho V7P (`khoi-v7p-cung-thuoc.json`):

| Shot (nhóm) | V7P khối | **V7B khối TB (min–max)** | V7B vùng phố/trại* | ≥ 40 %? |
|---|---|---|---|---|
| H2 (toàn cảnh) | 2,7 | **30,9** (20,3–61,0) | 49,5 | không (2/11 khung ≥ 40) |
| C1 vây hãm (a) | 3,4 | **12,9** (0,2–20,5) | 13,0 | không |
| C1 vây hãm (b) | — | 5,8 | 5,9 | không |
| C3 toàn cảnh (sau cần cẩu) | 16,1 | **15,1** | 25,9 | không |
| C5 toàn cảnh | 11,0 | **14,5** | 22,7 | không |
| H3 hero | 8,5 | 13,3 | — | (không thuộc nhóm) |

\* Vùng phố/trại = `fabric_pct` của mặt nạ nội dung: khối + nền phố của năm đó (sân, phố, quảng trường), có cả cây/tàu. Đây chỉ là số tham khảo.

- **Đánh giá thẳng:** việc 3 **chưa đạt ≥ 40 %** ở mọi shot vây hãm/toàn cảnh. H2 gần nhất (30,9 %; vùng phố 49,5 %).
- **Phố 1781–82 (C5):** dải phố trong tường chỉ rộng ≈ 300–400 m, phần còn lại là vịnh. Muốn khối ≥ 40 % phải nhìn xuống ≥ 35° từ sát phố, nhưng khi đó mất đoàn tàu khỏi khung, trong khi lời 2g cần cả hai.
- **Trại 1779 (C1):** mật độ theo nguồn thấp (§3).
- Đề xuất: D3′ (§11).

**6 khung cổng PNG sạch 1920×1080** (`reports/v7b/khung/`; hero.js SPP 4, JPG q2 → PNG; không chữ ngoài bộ đếm):

| Khung | Shot / thời điểm |
|---|---|
| `cong-vay-ham` | C1-a 21,8 s (28/10/1779) |
| `cong-cang` | C4 3,5 s (đoàn Rodney 1/1780, máy Bb lượt 5) |
| `cong-pho-day` | C3 11,5 s |
| `cong-hero` | H3 10,4 s (2026) |
| `cong-toan-canh` | C5 2,6 s (12/4/1781 10:50, đoàn Darby) |
| `cong-bo-chien-su` | H2 13,3 s (pin nổi khai hoả, cờ Union trên lâu đài) |
| `cong-pho-day-can-nguoi` (thêm) | C3 3,5 s (cận người hái rau + cờ Union) |

Cùng loại cảnh với 6 khung của V7P. Chờ điều phối chấm so đối thủ.

## §8 XEM CÂM (việc 8) — `reports/v7b/xem-cam/`

**Giao thức như V7P:**
- 3 vai (người xem YouTube tắt tiếng, giáo viên sử, dựng phim), cùng 4 câu;
- `claude -p` ghim claude-sonnet-5-5, chỉ được dùng Read;
- mỗi người xem 59 khung (1 khung/2 s, mỗi khung 320×180), không phụ đề, không lời;
- máy chạy thật: sonnet-5-5 + haiku-5-5.

| Lượt | Q1 Ai giữ Rock | Q2 1779 bắt đầu gì | Q3 Vì sao đói | Q4 Cái gì đến cứu | Tổng P đọc lại | Từ khoá |
|---|---|---|---|---|---|---|
| V7P | 0 | 6 | 3 | 2 | **11/24** | 17 |
| V7B lượt 4, C1-a | 0 | 6 | 3 | 1 | 10/24 | 18 |
| V7B lượt 4, C1-b | 0 | 6 | 3 | 2 | 11/24 | 17 |
| **V7B lượt 5, C1-a (bản cuối)** | **3** (R1 0 · R2 2 · R3 1) | **6** | **3** (1 · 1 · 1) | **2** (0 · 1 · 1) | **14/24 (58 %)** | 22 |

Quy ước P đọc lại giữ như V7P: "not sure" kèm suy đoán yếu = 1 điểm; đọc tàu tiếp viện thành tàu tấn công = 0. Bảng điểm: `reports/v7b/xem-cam/p-doc.json` và phần dưới. Độ rõ 2,0/5.

**Lý do người chấm nêu (lượt 5):**
1. **Q1:** 2/3 người thấy cờ Union trên tháp ở khung #40–41 ("looks like a British Union Jack, but it is tiny"). Chỉ có 2 khung mẫu nằm trong 3,9 s cận người. Ở mọi khung khác, cờ chỉ còn vài điểm ảnh.
2. **Q4:** cả 3 người đọc đoàn Darby có viền đỏ ở C5 thành "red ships firing on the town". Đoàn Rodney (C4) bị đọc là "ships arrive, can't tell friend from foe". Thuyền chở hàng và thùng ở Old Mole chưa thấy được ở 320×180.
3. **Q3:** chỉ suy ra được "bị phong toả nên bị cắt nguồn". Không thấy được người đói hay kho rỗng; người hái rau dại bị đọc là "tiny figures on a field".
4. **Thứ tự thời gian:** cả 3 người lạc ở đoạn móc (2026 đêm → bước năm → 1782 đêm → 1939–2026) trước khi vào 1779. Đúng thiết kế lời móc (TL-5), nhưng là chi phí khi xem tắt tiếng.

**Cần sửa để đạt ≥ 18/24 (không thêm chữ ngoài thẻ chương):**
- **Q1 (cần +3):** đặt một khoảnh khắc cờ lớn ≥ 4 % bề ngang khung, giữ ≥ 4 s (≥ 2 khung mẫu), ở **mỗi chương vây hãm**:
  - C3: kéo dài cận lâu đài lên 4–5 s, máy cách cờ ≤ 150 m;
  - C5: thêm cận Line Wall/King's Bastion có cờ Union và lính áo đỏ (từ hạn mức lướt thấp, đang dùng 3,3/10 %).
- **Q4 (cần +2):** tách "tàu đến cứu" khỏi "pháo bắn":
  - (a) bỏ viền đỏ ở tàu Anh, chỉ giữ cờ, vì viền đỏ đọc thành lửa/tấn công;
  - (b) cận Old Mole ≤ 150 m lúc đoàn Rodney dỡ hàng (thuyền cập bến, người khiêng thùng, đống thùng lớn dần);
  - (c) ở C5, cho đoàn Darby thả neo **trước**, pháo bắn vào phố **sau** ≥ 2 s, không chung khung mở đầu.
- **Q3 (cần +2):** chuỗi nhân quả thấy được:
  - C2: máy gần hơn (≤ 1,5 km) khi thuyền châu Phi gặp hàng chặn và quay đầu;
  - C3: cận ≤ 30 m người cúi hái cây (giỏ, bó rau), giữ ≥ 4 s;
  - có thể thêm cận chợ vắng/hàng người nhận khẩu phần, nhưng **cần nguồn** (S052 chỉ nói hái rau dại).
- **Quy ước chấm:** chuỗi 320×180 làm vật nhỏ biến mất nhanh hơn trên điện thoại thật. Đề xuất (D9) bổ sung một lượt chấm ở 640×360 và giữ 320×180 làm sàn.

## §9 Tờ so V7P ↔ V7B 8 cặp — `reports/v7b/so/to-so-8-cap-a.jpg`

| Câu | V7P | V7B |
|---|---|---|
| 0a | đêm 2026 ở biên giới | như V7P (nhà có vật liệu) |
| 0d | Rock xa 2 km, khói nhỏ | phố + lâu đài cận, khói vây hãm, bộ đếm 1462 |
| 0f | pin nổi cháy đêm (thấy từ 29,3 s) | pin nổi cháy (từ 27,0 s) + cờ Union trên lâu đài |
| 0g | 1941 đường băng | 1940 đường băng (D thấp hơn) |
| 2a | đồng cỏ, Rock xa | đồng + dải trại (A2), thẻ chương |
| 2d | phố 1/1780 từ C | **cận người hái rau + lâu đài cờ Union** |
| SM2 | đoàn Rodney cách 2 km | đoàn Rodney cờ Red Ensign + Old Mole (Bb) |
| 2g | **đêm 21:31** (lệch câu lời) | **ban ngày 11:19**: đoàn Darby thả neo, phố bị bắn (đã khớp câu) |

Hai bên lấy cùng câu lời. V7P dùng nhịp ước 2,5 từ/s, V7B dùng nhịp thật G1.

## §10 Bản thử, giờ máy, chi phí

| Tệp | Nơi | Cỡ | SHA-256 |
|---|---|---|---|
| Master 960×540 C1-a lượt 5 (G1 + nhạc tạm) | ngoài git `/var/tmp/cine-out/k2c-t3-v7b-a/k2c-t3-v7b-v1-master.mp4` | 128 374 651 B | `d4b6dec9e97fb451d1ccd7566d36ad1241606eb7fe7ab733eb08d7018b524c74` |
| 540p KHÔNG phụ đề (C1-a) | ngoài git `…/k2c-t3-v7b-a-540p-khong.mp4` | 35 985 470 B | `ded7a863af49aa2e5322a0f8a7291e458ce47743069a01248c7a5e1c1d46b481` |
| 540p CÓ phụ đề kiểm (C1-a) | ngoài git `…/k2c-t3-v7b-a-540p-phude.mp4` | 35 842 702 B | `f4946de6592136fb41f4ff01b934ada590cc5630db99f61aefa9d8cd9db9f799` |
| **Bản xem 640×360 không phụ đề (C1-a)** | trong git `reports/v7b/ban-thu/v7b-a-xem-khong.mp4` | 4 828 334 B | `5849f0832909cda2fee0fd763e2b87539e6cc76fc0c2d96ce031eaca3aff8ee5` |
| **Bản xem 640×360 có phụ đề (C1-a)** | trong git `reports/v7b/ban-thu/v7b-a-xem-phude.mp4` | 4 861 538 B | `c0f3b50749c90b052c6d3c01afdcb3e58f74914819d58e1021e24f5b8a5c4a0d` |
| Master C1-b (lượt 4) | ngoài git `/var/tmp/cine-out/k2c-t3-v7b-b/k2c-t3-v7b-v1-master.mp4` | 127 799 406 B | `93587ecfad75d9dac2109bd5d0e433b85c42fdc38bb244ca3eae685ad920ea55` |
| Bản xem C1-b không / có phụ đề | trong git `reports/v7b/ban-thu/v7b-b-xem-{khong,phude}.mp4` | 4 788 536 / 4 827 667 B | `596f606f…a4134` / `406b522a…45` |

**Tái tạo:**
1. `bash scripts/k2tl/v7p_cache.sh`
2. `K2TL_CACHE=… /opt/cine/bin/python -I scripts/k2tl/v7b_mau_nha.py`
3. `… v7b_faden.py`
4. `bash scripts/k2tl/v7b_dung.sh a` (hoặc `b`)
5. Đo: `v7b_do.py a --mask` · chuỗi câm + tờ so: `v7b_so.py a` · chấm: `v7b_cam.py a run score`

**Giờ máy thật** (đồng hồ bận máy) ≈ **5,5 h**:
- bộ đệm 0,05;
- soi khung 0,8;
- 5 lượt dựng (lượt 1 0,9 · lượt 2 0,85 · bỏ dở 0,2 · lượt 3 C1-a/b 0,95 · lượt 4 H3 0,55 · lượt 5 C3/C4 0,3) ≈ 3,75;
- đo + mặt nạ 0,6;
- khung 1080p 0,3.

Dưới mốc theo dõi 10 h.

**Giờ máy 1080p ước cả tập:**
- Lấy ước V7P **≈ 48 h** làm gốc.
- Cộng nhà 2026 LOD gần 2,6 km (ước +15 % ở các điểm D/G/H ≈ +2 h) và lượt cận người/cần cẩu (≈ +0,5 h).
- → **≈ 50 h một tiến trình** (≈ 6 gói × ≤ 8,5 h).
- Số s/khung 1080p đo lượt này (6,7–16 s/khung, một khung mỗi lần chạy, máy đang bận dựng) có cả thời gian nạp cảnh, **không so được** với số đo cả shot của V7P, nên tôi không dùng để ước. Sai số ±20 %.

**Chi phí:**

| Khoản | Mốc / chặn | Thật |
|---|---|---|
| Claude API | $8 / $25 | **$0,657** (9 lượt `claude -p`: 3 lượt chấm × 3 vai + 1 lệnh thử) — `reports/v7b/xem-cam/cost.jsonl` |
| OpenAI | $5 / $50 | **$0** (không sinh ảnh) |
| ElevenLabs / YouTube | 0 | 0 / 0 |
| Giờ máy | 10 h | ≈ 5,5 h |

Chặn an toàn:
- Lỗi chú thích `//` nuốt mã (BAI-HOC #42/#76) xảy ra 3 lần trong phiên (props.js, t3tl.js, people.js). Cả 3 lần bắt được trước khi dựng: lần đầu nhờ `node --input-type=module --check`, lần sau nhờ khung soi. Đã đổi sang `/* */`.
- `pkill -f` giết luôn shell của P một lần (BAI-HOC #24). Từ đó dừng tiến trình theo PID.

## §11 Chỉ số trong ±5 % quanh ngưỡng (luật cứng)

- **Hệ số phóng cờ = 1,5×**, đúng trần D4 (0 %).
- **Bước năm giữ 0,458 s** so sàn tự đặt 0,45 s (+1,8 %).
- **Loudness −13,9 LUFS**: mục tiêu −14,0, dải −15,0…−13,8; cách mép trên 0,1 LU.
- Ngoài vùng ±5 %, ghi để rõ:
  - cắt/phút 4,05 (trần 5);
  - shot TB 14,8 s (sàn 12);
  - pin nổi cháy 26,96 s (trần 30);
  - lời trên nhạc ≈ 16,7 dB (sàn 15);
  - năm/s liên tục ≤ 1,9 (trần 20);
  - lướt thấp 3,3 % (trần 10);
  - góc cao 95,4 % (sàn 75).
- **Trượt (không phải sát ngưỡng):** khối ≥ 40 % (cao nhất 30,9 %); XEM CÂM 14/24 (cần 18).

## §12 Quyết định đề xuất

| # | Đề xuất | Ưu | Nhược | Tác động | Rủi ro |
|---|---|---|---|---|---|
| V7B-D1 | Duyệt **định nghĩa góc cao**: AGL ≥ 120 m HOẶC nhìn xuống ≥ 15° | đo được bằng máy; cho phép máy gần khối mà vẫn "cao" (K: AGL 85 m, nhìn xuống 27°) | điều kiện "hoặc" cho cả cú cận 30 m nhìn xuống 28° là góc cao → phải giữ thêm cột "theo vai" | TL-1, checks | lạm dụng góc chúc để né TL-2 → đề xuất K chặn AGL < 50 m |
| V7B-D2 | Chốt **bước năm đều** (giữ ≥ 0,45 s, giờ mặt trời cố định, mốc đúng lưới khung) cho mọi đoạn tua nhanh hơn 20 năm/s | giữ "14 lần vây" và 1943 → 2026 mà không trái §10.3; không nhấp nháy | người xem câm vẫn lạc ở móc (3/3) | H2, H3, N5.5, bookend | bước nhiều quá thành trình chiếu năm → giới hạn ≤ 15 bước/shot |
| V7B-D3′ | Hạ mục tiêu khối cho cảnh **có lời nhắc tới tàu/vịnh**: "khối + vùng phố ≥ 40 %" thay cho "khối ≥ 40 %"; giữ ≥ 40 % khối cho cảnh chỉ có phố/trại | H2 đạt ngay (49,5 %); phản ánh đúng phố 1781 hẹp giữa núi và vịnh | nới mục tiêu chủ dự án đặt | C1, C5, H2 | nếu không nới thì phải tách tàu và phố thành hai shot (+1 cắt/chương) |
| V7B-D4 | Viền phe: **bỏ ở tàu Anh**, giữ ở khối quân TBN và tàu TBN; cờ tàu giữ nguyên | gỡ lỗi "tàu đỏ = tấn công" (3/3 ở C5) | lệch đối xứng giữa hai phe | C2–C5, H2 | người xem không phân được hai đoàn khi xa → bù bằng cận cờ (D5) |
| V7B-D5 | **Khoảnh khắc cờ lớn ≥ 4 % bề ngang khung, ≥ 4 s, mỗi chương vây hãm** (lâu đài / Line Wall / soái hạm), dùng hạn mức lướt thấp | Q1 từ 0 lên 3/6 chỉ với 3,9 s cận; ước lên ≥ 5/6 | +1–2 cú cận mỗi chương (lướt thấp ≈ 6–8 %) | ch.1–2 | gần trần TL-2 10 % |
| V7B-D6 | Bản cuối dùng **C1-a** (máy gần dãy trại); bỏ Faden phủ (C1-b) cho C1 | khối trại 12,9 % so với 5,8 %; xem câm ngang nhau (10 so với 11) | mất tư liệu phủ khớp địa hình | C1, N1.4, N2.11, N3.1 | Faden vẫn dùng được ở cảnh bản đồ (TL-4) khi máy cao hơn để đọc ra nét bản đồ |
| V7B-D7 | Thêm lượt chấm xem câm ở **640×360** bên cạnh 320×180 | sát cỡ điện thoại thật | +$0,22/lượt | cổng HC-2 | điểm 640 cao hơn có thể che lỗi trên màn nhỏ → giữ 320 làm sàn |
| V7B-D8 | Lấy lại WAV/FLAC G1 v4.2 của KL42 (SHA ba50fba7… / 852b9e41…) vào ổ lưu chung cho bản phát hành | bản thử dùng MP3 96 kbps | — | G4 / phát hành | ElevenLabs thu lại nếu mất ≈ 12 000 ký tự |

## §13 Việc chờ chủ dự án

1. **Xem bản thử** `reports/v7b/ban-thu/v7b-a-xem-khong.mp4` (xem tắt tiếng) và `v7b-a-xem-phude.mp4` (có giọng G1 + phụ đề kiểm). Bản C1-b để so: `v7b-b-xem-*.mp4`. Chủ dự án xem tắt tiếng ≈ 2 phút theo §13.4.
2. **Quyết V7B-D1…D8**, nhất là D1 (định nghĩa góc cao), D3′ (mục tiêu khối), D4 (viền phe), D5 (cận cờ). Đây là các việc cho vòng sau, vì XEM CÂM đang **TRƯỢT 14/24**.
3. **Điều phối chấm 6 khung cổng** `reports/v7b/khung/cong-*.png` so đối thủ và so V7P.
4. **Ghi RIGHTS/AUTHORSHIP (phiên P; vùng này tôi không được sửa):**
   - Sentinel-2 L2A 15/4/2026 (Copernicus) dùng cho màu mái;
   - 4 ảnh Wikimedia Commons (CC BY-SA 2.0 / CC BY 3.0 ×2 / CC BY-SA 3.0, tác giả theo `design/k2v/tl/data/mau-nha-v7b.json`), chỉ dùng rút bảng màu, không đưa ảnh lên hình;
   - OSM (ODbL) thẻ màu;
   - Faden 1783 (Yale 2046612, PD) phủ ở C1-b;
   - mẫu cờ (§2, tư liệu PD);
   - nhạc tạm Tyrant.mp3 (K2-MUS);
   - quyết định sáng tạo của chủ dự án duyệt khi dán lệnh V7B (ngữ pháp TL giữ; D2 không miễn; C1 thử cả a và b).
5. Phiên P merge nhánh này khi duyệt. Nhánh **không** merge.

**DỪNG — chờ chủ dự án.**
