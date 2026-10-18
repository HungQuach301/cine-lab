**Nhánh thật: `claude/k2c-t3-loi-khoa-al1itg`** (harness buộc nhánh này thay cho `k2c-t3-loi` của lệnh; tạo từ `origin/ccr-3225b6a6-1yeft3` @ `852f46dc` = gói G1). Đã đẩy, **không merge**.

# K2C-T3-01 "Why Gibraltar Was Besieged 14 Times" — KHOÁ LỜI — DỪNG

> Phiên T3 khoá lời, 18/10/2026 (sau G1: chủ dự án duyệt 09:35). Chỉ sửa `channel-k2/k2c-t3-01/**`. Không sửa `scripts/`, `checks/`, `design/`, `docs/`, `reports/`, nhánh khác. Đã đọc: `G1-BAO-CAO.md`, `script-v1.md`, `g1/**` (công cụ + kiểm chữ), Kinh thánh §3, §10.6, §11, khuôn khoá lời T2 (`loi-khoa.txt`, `LOI-KHOA.sha256`, `script-v3.3-KHOA.md` trên `origin/k2c-t2`), `reports/m3/BAI-HOC-LL.md`.
> Thời lượng lời là **ước** ở 2,5 từ nói/s (cách đếm G1). Chưa thu giọng.

## Khối điều lệ (lệnh + thực tế)
| Trường | Lệnh | Thực tế |
|---|---|---|
| Nhánh | `k2c-t3-loi` từ `origin/ccr-3225b6a6-1yeft3` | harness buộc `claude/k2c-t3-loi-khoa-al1itg` (dòng đầu), cùng gốc `852f46dc` |
| Tệp được sửa | `channel-k2/k2c-t3-01/**` | đúng: tệp mới ở gốc tập (`G1-DUYET.md`, `script-v4-KHOA.md`, `loi-khoa.txt`, `LOI-KHOA.sha256`, báo cáo này) + `khoa-loi/**`; cập nhật `vay-ham/treatment.json`, `vay-ham/tu-kiem.json`, `g1/kiem-chu.{json,md}` |
| Trần | Claude API ≤ $3 · ElevenLabs 0 · YouTube 0 · giờ máy ≤ 1,5 h | **$2,773** · **0** · **0** · **≈ 0,5 h** (§6) |
| Preflight / email | bắt buộc; che email | `tools/preflight.sh` chạy tay trước mỗi commit (hook không cài): **ĐẠT**, `lock.py --verify` **KHỚP**; 0 email trong tệp ghi |
| Dừng | không dừng hỏi giữa chừng | đúng; các câu tự quyết ở §7 |

---

## 0. Tóm tắt (đọc 2 phút)
1. **G1-DUYET.md** ghi nguyên văn: *"Chủ dự án duyệt G1 18/10/2026 09:35: lời L1–L17, bảng shot 74 shot 702 s, mở đầu E, claim G001–G002"*.
2. **L16 điền:** *"As of 18 October 2026, …"* (5i) và chữ trên hình *"Facts as of 18 Oct 2026"* (0b–0e). **Đọc lại mọi nguồn thời sự hôm nay (§3): không nguồn nào đổi** — EP vẫn ghi phiên toàn thể dự kiến 14/12/2026, hiệp ước áp dụng tạm thời từ 15/7, biên giới bộ không kiểm tra thường lệ. Không thêm câu mới vì thời sự; 5 câu thời sự đổi chữ do kiểm mù (5b, 5c, 5g, 5h, 5i — lý do ở §2, §3).
3. **Kiểm mù 2 vòng × 3 vai** (`claude -p` ghim `claude-sonnet-5-5`, không công cụ, thư mục trống, ẩn tác giả) + **REVIEWER 2 vòng** (`claude-opus-5-5`, có bảng claim). **50 sửa** (31 ở v3, 19 ở v4), mỗi sửa là chỗ ≥ 2/3 vai cùng nêu hoặc lỗi dữ kiện đối chiếu claim. **Lỗi dữ kiện thật đã sửa:** 870 → **869** chết (333 + 536); Crillon chỉ huy **cuộc vây**, không phải hạm đội; 10 pin nổi mất hết vào **chiều 14/9**, không phải "sáng"; "almost all left" là nguồn **Anh** (GHT), không phải nguồn TBN; 14 000 quân là **số tình báo Anh "nếu đủ biên chế"**; đạn hai phía: sổ Anh, phía địch chỉ tính từ 4/1781; Tây Ban Nha *"does not"* (không phải *"has never"*) công nhận hàng rào; 1730 là năm **ra lệnh** xây chiến tuyến (câu chốt đổi 1 từ).
4. **REVIEWER vòng 3 KHÔNG chạy** — vòng 2 đã đưa tổng API lên $2,77/$3; phiên tự đối chiếu 19 sửa vòng cuối với claim. Điểm người đọc mù **không tăng** (tổng thể 7/7/7 → 6/6/7; tin cậy 7/7/7 giữ): sửa chủ yếu là độ chính xác và ghi nguồn; chỗ chê còn lại là mật độ số, chương 3 chậm, đoạn hầm 1782 lùi thời gian (§2.3).
5. **Từ điển phát âm** (`khoa-loi/phat-am/`): 47 mục — 28 năm đọc kiểu Anh, ngày khoá lời, 8 địa danh (La Línea, La Línea de la Concepción, San Roque, Algeciras, Tangier, Utrecht, Cádiz dự phòng), 8 tên người, *fait accompli*, *isthmus*. Chỉ dùng luật **alias** vì `eleven_multilingual_v2` bỏ qua phoneme (tài liệu ElevenLabs hiện hành); IPA để tham khảo trong JSON. **Không gọi ElevenLabs.**
6. **Lời khoá:** `script-v4-KHOA.md` + `loi-khoa.txt` (1 557 từ viết, **9 090 ký tự** đọc) + `LOI-KHOA.sha256` (khuôn T2, §4). Thời lượng đặt lại theo lời khoá (luật G1): **74 shot, 718,0 s (11:58)**; `tu_kiem.py` **ĐẠT** mọi luật; `kiem_loi.py` 0 lỗi, 16/16 trích trên hình khớp claim.

**Chỉ số trong ±5 % quanh ngưỡng (nêu tên):**
| Chỉ số | Đo | Ngưỡng | Lệch |
|---|---|---|---|
| Tổng phim (bảng shot) | 718,0 s | 12 phút = 720 s (Kinh thánh §3) | **−0,3 %** (G1: 702 s; +16 s do lời thêm nguồn đếm; theo nhịp Eric đo ở T2 lời ≈ 625 s) |
| Móc | 44,5 s | ≤ 45 s | −1,1 % (không đổi) |
| Hồ sơ thật | 21,4 % | ~21 % (§10.8) | +1,9 % |
| Strategic SM3 | 8,0 s | ≤ 8 s | 0 % (lời chốt chảy sang 4g như G1) |
| Khung neo KC2026 / KB2026 | 10,0 / 9,5 s | ≤ 10 s | 0 % / −5,0 % |
| Lặp vùng + góc | 2 | ≤ 2 | 0 % (khung neo, có chủ đích) |
| 0c (NC-H2) | 3,0 s, lời 4,4 s | ≤ 3 s | 0 % (lời chảy sang 0d, như G1) |
| Shot chạm trần 12 s | 1h, 2k, 2l, 2r | ≤ 12 s | 0 % — lời tràn 1,7–3,2 s sang shot cùng chủ đề; **2r tràn 1,7 s qua ranh chương 3** |
Ngoài ±5 % (đã xét): strategic 3,06 % so 15 %; ai_image 7,3 % so 20 %; NC-H3 ≤ 60 km 99,4 %, ≤ 3 km 92,4 %; footage 1,1 % so 20 %.

**Việc chờ chủ dự án:** §8.

---

## 1. Quy trình kiểm mù + REVIEWER (`khoa-loi/kiem_mu_loi.py`; kết quả thô `khoa-loi/kiem-mu/`, có prompt nguyên văn trong mỗi JSON)
- **3 vai** (mỗi vòng chạy song song, mỗi vai một thư mục tạm trống): R1 người xem YouTube 30+ trên điện thoại (chán/khó hiểu) · R2 giáo viên sử Algeciras đọc tiếng Anh (thiên Anh, từ nặng, số không nói ai đếm) · R3 người kiểm chứng tạp chí sử Anh, chuyên thế kỷ 18 (claim sai/quá tay, thiên TBN, chê Anh). Nhận **chỉ lời đọc + chữ trên hình** (bỏ mã claim, ghi chú tiếng Việt; máy chặn nếu còn chữ Việt). Soi 5 mục của lệnh: claim nghi sai/thiếu nguồn · câu một phía · số thương vong không nói ai đếm · câu khó hiểu · chỗ chán; mỗi mục phải chép nguyên chữ.
- **REVIEWER** (`claude-opus-5-5`): lời có mã claim + bảng claim được gắn (claim_en, nguồn, trích nguyên văn, trạng thái, ghi chú; vòng 2 thêm trích đối chiếu `nguon_doi_chieu`).
- **Lỗi giao thức vòng 1 (đã xử lý):** prompt REVIEWER vòng 1 ghi sai luật "mọi trạng thái khác XÁC MINH không được dùng". Ở bộ claim tập này **MÂU THUẪN = nguồn lệch nhau về một chi tiết, có "lời dẫn an toàn"** (claims-vay-ham.md: 21 claim; G1 đã duyệt L4–L5 trên các claim này). → 12 mục "block" vòng 1 (S014, S016, S020, S021, S053, S066, S069–S071, S034, S112–S113) **không áp máy móc**: phiên xét từng câu có dùng đúng lời dẫn an toàn/ghi nguồn không (áp khi không: F01 1b, F04 1g, F13 3b). Hai mục "trích không khớp" (2c, 2k) là **báo nhầm** vì vòng 1 không đưa `nguon_doi_chieu`; `kiem_loi.py` khớp 16/16. Vòng 2 sửa prompt (luật MÂU THUẪN đúng, tài sản hình không phải claim, câu chủ dự án chốt chỉ được báo lỗi dữ kiện, ≤ 15 mục).
- **Luật sửa (lệnh mục 3):** chỉ sửa chỗ ≥ 2/3 vai cùng nêu (gom theo shot, `ai_neu`) hoặc lỗi dữ kiện đã đối chiếu claim; mỗi sửa ghi trước/sau + claim (`khoa-loi/sua_v3.py`, `sua_v4.py` → `sua-v3.json`, `sua-v4.json`).

| Vòng | Lời | R1 móc/tin/cân/tổng | R2 | R3 | Xem tiếp 30 s | Mục nêu (R1/R2/R3) | REVIEWER |
|---|---|---|---|---|---|---|---|
| 1 | v2 (= v1 + ngày) | 6/7/7/7 | 7/7/6/7 | 7/7/7/7 | 3/3 | 41/53/70 | do_not_lock: 12 block (đều do luật sai ở trên), 6 major, 25 minor |
| 2 | v3 | 7/7/7/6 | 6/7/6/6 | 7/7/7/7 | 3/3 | 53/52/88 | lock_with_fixes: 0 block, 6 major, 9 minor |
| — | v4 KHOÁ | — | — | — | — | — | vòng 3 không chạy (trần $) — phiên tự đối chiếu |

## 2. Sửa sau kiểm mù (bảng đầy đủ; v2 → v3 → v4)
Mã E = vòng 1 (lời v2 → v3), F = vòng 2 (v3 → v4). Một số câu sửa ở E rồi sửa lại ở F khi vòng 2 chê chính chữ sửa (1i "it does", 1j "twice more", 5i "applied provisionally") — bản cuối là cột "Sau" của dòng F.

| Mã | Shot | Trước | Sau | Ai nêu | Claim | Lý do |
|---|---|---|---|---|---|---|
| E01 | 1b | came in the name of "Charles the Third." | came in the name of the rival claimant, "Charles the Third." | R1, R2, R3 | S012 S020 | khó theo ai đứng phía nào (nối với SM1) |
| E02 | 1e | Gibraltar surrendered. English histories say the twenty-fourth of July, on the old calendar. {S013} | Gibraltar surrendered. {S013} [TRÊN HÌNH] "4 August 1704 · English histories: 24 July 1704 (old calendar)" | R1, R2, R3 | S013 | hai ngày + đổi lịch nghe một lần khó hiểu → ngày lịch cũ lên hình |
| E03 | 1g | Almost all of them left. {S017} By Spanish accounts, most settled a league to the north-east, at San Roque. {S019} | By Spanish accounts, almost all left, and the largest group settled a league north-east, at San Roque. {S017} {S019} | R1, R2, R3 + REVIEWER (dữ kiện) | S017 S019 | "almost all" không nói ai kể; S019 nói "nhóm lớn nhất", không phải "most" |
| E04 | 1i | Britain says Gibraltar includes it. {S031} | Britain said in 2015 that it does. {S031} | R2, R3 + REVIEWER (as of) | S031 | lập trường Anh là phát biểu 2015 (Lidington), nói như hiện tại |
| E05 | 1j | Spain tried to take Gibraltar back from 1704 to 1705, with French troops, and again in 1727. | Spain besieged it twice more: from 1704 to 1705, with French troops, and in 1727. | R1, R2, R3 | S021 S004 | "back from 1704" mơ hồ, đoạn dồn ngày |
| E06 | 2a | Madrid closed every link with Gibraltar. {S040} | Madrid cut Gibraltar off from Spain. {S040} | REVIEWER (dữ kiện) | S040 | S040: đóng giao thông với Tây Ban Nha; đường biển còn mở tới phong toả 7/1779 |
| E07 | 2b | By autumn, about fourteen thousand men faced the Rock across the isthmus. {S048} | By October, by the British count, about fourteen thousand Spanish troops faced the Rock. {S048} | R1, R3 + REVIEWER (dữ kiện) | S048 | số của tình báo Anh (Drinkwater) — nói ai đếm |
| E08 | 2c | Its boats at Algeciras had one job: to cut off | Based at Algeciras, its boats were there to cut off | R1, R2 + REVIEWER | T006 T007 | "had one job" nghiêng giọng; giữ "food" theo trích Montero trên hình |
| E09 | 2f | Scurvy spread, until a Danish ship full of lemons was brought in. | Scurvy spread, until a Danish ship of lemons was brought in, garrison diaries record. | R1, R2, R3 | S053 S057 | giai thoại không nói nguồn; S053: chanh và cam |
| E10 | 2i | Between them, the two sides fired nearly half a million rounds. | By British tallies, the two sides fired over four hundred and sixty thousand rounds. | R1, R2, R3 + REVIEWER (dữ kiện) | S051 S077 | 205 328 + 258 387 = 463 715 theo sổ Anh; phía địch chỉ tính từ 4/1781 → "at least" |
| E11 | KA1782 | By September 1782, about seven and a half thousand men held the Rock. | By September 1782, the garrison counted about seven and a half thousand men. | R1, R2, R3 | S079 | số quân không nói ai đếm |
| E12 | 2j | The garrison's answer was heat: | The garrison turned to heat: | R1, R2, R3 | S058 S060 | giọng ca ngợi một phía ("answer"); trình tự |
| E13 | 2k | Four days later, the French and Spanish fleets sailed in, under the Duc de Crillon: forty-seven ships of the line by the British count, fifty by the Spanish. | Four days later, the French and Spanish fleets gathered in the bay: forty-seven ships of the line by the British count, fifty by the Spanish. The Duc de Crillon led the siege. | R2, R3 + REVIEWER (dữ kiện) | S065 T018 S049 | Crillon chỉ huy cuộc vây (S049), không chỉ huy hạm đội; 50 gồm tàu đã ở Algeciras (T018) |
| E14 | 2m | At half past nine, the batteries moved into position. At a quarter to ten, the garrison opened fire. {S066} At ten twenty-five, by the Spanish account, some four hundred guns answered together. {S067} By the next morning, all ten batteries were gone. {S074} | That morning, the batteries moved into position, and the garrison opened fire on them. {S066} At ten twenty-five, by the Spanish account, the attackers' guns, some four hundred, opened fire together. {S067} By the next afternoon, all ten batteries were lost. {S074} | R1, R2, R3 + REVIEWER (dữ kiện) | S066 S067 S074 | bốn mốc giờ liền nhau, "answered" mơ hồ; S074: chiếc cuối bị đốt chiều 14/9 (giờ vẫn trên bộ đếm) |
| E15 | 2n | More than two thousand attackers were lost, by British and Spanish counts; three hundred and fifty-seven were rescued. {S069} | By British and Spanish counts, over two thousand attackers were lost, prisoners included; the British rescued three hundred and fifty-seven. {S069} | R1, R2, R3 | S069 | "lost" chưa rõ; 357 không nói ai đếm |
| E16 | 2o | All that summer, the garrison had also been digging through the north face. | Before the attack, all summer, the garrison had been digging through the north face. | R1, R2 | S080 | nhảy lùi thời gian sau cao trào — báo trước bằng lời |
| E17 | 2q | The Rock was never starved out. | The blockade never forced a surrender. | R1, R2, R3 | S045 S046 | câu khải hoàn một phía |
| E18 | 2r | From all causes, Montero put the losses near two thousand inside and six thousand outside. {S077} The garrison's own records count at least eight hundred and seventy dead. {S076} | From all causes, the Spanish historian Montero put the losses near two thousand defenders and six thousand besiegers. {S077} The garrison's own records count at least eight hundred and sixty-nine dead. {S076} | R1, R2, R3 + REVIEWER (dữ kiện) | S077 S076 | 333 + 536 = 869 (không phải 870); "inside/outside" khó hiểu; loại trừ scorbut 1779–80 giữ trên thẻ ("at least" đã báo thiếu) — lời không đủ chỗ |
| E19 | KC1910 | Remember this street. We'll come back to it. | Remember this street in La Línea. We'll come back to it. | R1, R2 | S033 | nghe riêng không biết phố nào |
| E20 | 3e | This was the gap between them: open sand, between two towns. | This was the gap between them: a strip of neutral ground between two towns. | REVIEWER (dữ kiện) | S035 S088 | "open sand" quá tay (S035 có trại lính từ 1854) |
| E21 | 3f | Spain has never recognised it as a border. | Spain does not recognise it as a border. | R1, R3 + REVIEWER (dữ kiện) | S036 S030 | S030 nói "không công nhận" (hiện tại), không có "never" |
| E22 | 3h | And in 1934, part of the old racecourse became a grass airstrip. | And from 1934, a grass airstrip was built there. | REVIEWER (dữ kiện) | S090 S089 | không claim nào nói dải cỏ chiếm "một phần trường đua"; S090: xây 1934–36 |
| E23 | 4d | Those tunnels became a city inside the Rock: a road about a mile long, a hospital, a power station, dug by British and Canadian tunnellers. | Inside the Rock, those tunnels held a road about a mile long, a hospital and a power station, dug by British and Canadian tunnellers. | R2, R3 | S112 S113 S110 | giọng ngưỡng mộ một phía ("a city") |
| E24 | 4e | Today, the tunnels add up to about fifty-five kilometres, more than the roads above ground. | Gibraltar counts about fifty-five kilometres of tunnels from every era, more than its roads above ground. | R1, R2, R3 + REVIEWER | S106 S108 | không nói ai đếm; 55 km là mọi thời kỳ, không riêng WWII |
| E25 | 4h | Spain protested British ships in its waters, but not the airstrip. | Spain protested what it called breaches of Spanish waters; no complaint over the airstrip is on record. | R1, R2, R3 + REVIEWER (một phía) | S105 | "its waters" là lập trường chủ quyền; S105: "không có hồ sơ phản đối", không phải chắc chắn không phản đối |
| E26 | 4i | at least six hundred and fifty aircraft lined the runway. | by Gibraltar's official record, at least six hundred and fifty aircraft lined the runway. | R1, R2, R3 | S123 | số không nói nguồn (nghị quyết Quốc hội Gibraltar) |
| E27 | 5b | Some four thousand six hundred Spanish day workers were cut off. | Britain counted some four thousand six hundred Spanish day workers cut off. | R1, R2, R3 | C19 | số không nói ai đếm (Ngoại trưởng Anh, Hansard 9/6/1969) |
| E28 | 5f | That divides by the thirty-eight thousand who live there, and leaves out the people in Spain who hold fourteen thousand of its jobs. {C11} {C08} ‹Our read› Our read: the rich-looking number partly rests on the other side. {C08} {C14} | That spreads output over the thirty-eight thousand who live there, and leaves out the people in Spain who hold fourteen thousand of its jobs. {C11} {C08} ‹Our read› Our read: part of the work behind that number is done from the other side. {C08} | R1, R2, R3 + REVIEWER (vượt claim) | C11 C08 | "divides by" khó nghe; câu Our read vượt claim (C14 không đỡ) → nói đúng phạm vi C08, giữ nhãn |
| E29 | 5g | In July 2026, Britain and the EU signed a treaty to take the checks off this border. {C01} {C02} | In July 2026, Britain and the EU signed a treaty; the next day, routine checks here ended. {C01} {C02} | R1, R2, R3 | C01 C02 | "signed" nghe như đã xong; nối với 0b (ký 14/7, bỏ kiểm tra 15/7) |
| E30 | 5h | The old fence is coming down, but a new one stands a few metres behind it, with about a hundred and fifty metres left open. {C03} | In July, Gibraltar's government said the old fence was coming down, with a new one a few metres behind; only about a hundred and fifty metres, where walkers cross, stays open. {C03} | R1, R2, R3 + REVIEWER (as of) | C03 | tin 2/7/2026 nói như hiện tại, không nói ai nói; 150 m là chỗ gì (HMGoG 517/2026: "where pedestrians have always crossed") |
| E31 | 5i | the treaty is provisional, pending | the treaty is applied provisionally, pending | R1, R2, R3 + REVIEWER | C26 | "provisional" nghe như mâu thuẫn 0b "no routine checks" — C26: áp dụng tạm thời |
| F01 | 1b | came in the name of the rival claimant, "Charles the Third." {S012} {S020} | fought for the rival claimant, "Charles the Third." {S012} {S017} | R1, R2 + REVIEWER (dữ kiện) | S012 S017 S020 | S020 MÂU THUẪN: "nhân danh ai" lệch giữa nguồn (García Sanz: Carlos III; Sayer/Montero: Nữ hoàng Anne) → nói điều mọi nguồn cùng nhận |
| F02 | 1d | The fleet answered with some fifteen thousand rounds. {S016} | The fleet answered with some fifteen thousand rounds, by British and Spanish accounts alike. {S016} | R1, R2, R3 | S016 | số đạn không nói ai đếm (Sayer ≥ 15 000 · Montero "sobre quince mil") |
| F03 | 1e | On the fourth of August 1704, Gibraltar surrendered. | On the fourth of August 1704, by the new calendar, Gibraltar surrendered. | R1, R2, R3 | S013 | ngày lịch cũ chỉ trên hình → người chỉ nghe thấy lệch; nói "new calendar" |
| F04 | 1g | By Spanish accounts, almost all left, and the largest group settled a league north-east, at San Roque. | By a British account, almost all left; by a Spanish one, the largest group settled a league north-east, at San Roque. | R1, R2, R3 + REVIEWER (dữ kiện) | S017 S019 | "almost all" là nguồn Anh (GHT, S017), không phải nguồn TBN |
| F05 | 1h | In 1713, the Treaty of Utrecht made it permanent: the town, castle and port went to the British Crown, "for ever." {S022} {S028} {S029} But "without any territorial jurisdiction, and without any open communication by land." {S023} {S027} | In 1713, the Treaty of Utrecht gave it to the British Crown "for ever," {S022} {S028} {S029} but "without any territorial jurisdiction, and without any open communication by land." {S023} {S027} If Britain ever gave it up, Spain would have first refusal. {S025} | R1, R2, R3 (cả hai vòng) | S022 S023 S025 | trích Điều X một chiều — thiếu điều khoản ưu tiên cho Tây Ban Nha (S025 XÁC MINH); "town, castle and port" dời sang 1i (tránh lặp, giữ thời lượng) |
| F06 | 1i | The treaty never mentions the sandy isthmus to the north. {S022} {S035} Spain says the isthmus was never ceded. {S030} Britain said in 2015 that it does. {S031} | The treaty names the town, castle and port, not the sandy isthmus to the north. {S022} {S035} Spain says the isthmus was never ceded. {S030} Britain said in 2015 that Gibraltar includes it. {S031} | R1, R3 + REVIEWER (dữ kiện) | S022 S035 S030 S031 | "it does" mơ hồ (lỗi do sửa vòng 1); "never mentions" nói về cả hiệp ước, claim chỉ trích Điều X |
| F07 | 1j | Spain besieged it twice more: from 1704 to 1705, with French troops, and in 1727. {S021} {S004} Neither siege took it. | Within weeks, Spain and France besieged it, into 1705. {S021} {S004} Spain tried again in 1727. {S004} Neither siege took it. | R1, R2, R3 | S021 S004 | "twice more" (sửa vòng 1) nghe như đếm sai |
| F08 | 2b | By October, by the British count, about fourteen thousand Spanish troops faced the Rock. {S048} | By October, British intelligence put the Spanish army facing the Rock at up to fourteen thousand. {S048} | REVIEWER (dữ kiện) | S048 | S048: quân số giấy "nếu đủ biên chế", tin tình báo Anh |
| F09 | 2i | the two sides fired over four hundred and sixty thousand rounds. {S051} {S077} | the two sides fired over four hundred and sixty thousand rounds. {S051} {S077} [TRÊN HÌNH] Drinkwater (garrison officer), 1785: "garrison 205,328 rounds · besiegers 258,387 (counted from April 1781)" | R1, R2, R3 | S051 | "British tallies" không nói của ai → tên + số tách hai phía lên hình (không thêm lời) |
| F10 | 2m | That morning, the batteries moved into position, and the garrison opened fire on them. {S066} | That morning, the batteries moved into position under the garrison's fire. {S066} | R1, R2, R3 | S066 | trình tự ai bắn trước khó hình dung |
| F11 | 2n | By British and Spanish counts, over two thousand attackers were lost, prisoners included; the British rescued three hundred and fifty-seven. {S069} | Over two thousand attackers were lost, by a British estimate that includes prisoners, and by a Spanish one; the British rescued three hundred and fifty-seven. {S069} | R1, R2, R3 + REVIEWER (dữ kiện) | S069 | chỉ số Anh gồm tù binh; Montero không nói |
| F12 | 2r | From all causes, the Spanish historian Montero put the losses near two thousand defenders and six thousand besiegers. {S077} The garrison's own records count at least eight hundred and sixty-nine dead. {S076} | Spanish historian Montero put losses near two thousand defenders and, from all causes, six thousand besiegers. {S077} The garrison's records count fewer dead: at least eight hundred and sixty-nine. {S076} | R1, R2, R3 + REVIEWER (dữ kiện) | S077 S076 | "por todas causas" chỉ áp cho 6 000; hai số phía giữ thành không cùng cách tính → nói "fewer" |
| F13 | 3b | In 1810, with | Around 1810, with | R1, R2, R3 + REVIEWER | S034 | S034 MÂU THUẪN năm (Montero 1811) — lời nói chắc 1810 |
| F14 | 4b | called the strip a fait accompli, like the Rock itself. {S098} | called the strip a fait accompli, like the Rock itself, while insisting its use breached Spanish territory. {S098} | R1, R2, R3 (4h, cả hai vòng) + REVIEWER ×2 | S098 | cắt nửa claim S098 → nghe như Tây Ban Nha chấp nhận; đoạn 4a–4h bị 3/3 chê nghiêng |
| F15 | 4e | more than its roads above ground. {S106} {S108} | more than its roads above ground. {S106} {S108} [TRÊN HÌNH] "HM Government of Gibraltar, 2017 · UK Hansard, 2015: 34 miles of tunnels, twice the road length" | R1, R2, R3 | S106 S108 | so sánh với đường bộ bị nghi không nguồn → nguồn lên hình |
| F16 | 5c | The UK government puts the daily crossers at about fifteen thousand. | The UK government puts the daily crossers higher, at about fifteen thousand. | R1, R3 (+ R2 vòng 1) | C09b C08 | 14 000 việc làm ↔ 15 000 người qua lại nghe như lệch — báo là số khác, cơ quan khác |
| F17 | 5h | only about a hundred and fifty metres, where walkers cross, stays open. {C03} | only about a hundred and fifty metres would stay open. {C03} | REVIEWER (dữ kiện) | C03 | tin 2/7 là kế hoạch (thì tương lai); "where walkers cross" không có trong trích lưu ở C03 |
| F18 | 5i | the treaty is applied provisionally, pending | the treaty is in force only provisionally, pending | R1, R2, R3 | C26 | "applied provisionally" (sửa vòng 1) nghe như thuật ngữ luật |
| F19 | 5k | In 1730, Spain built a line to cut the Rock off by land. | In 1730, Spain ordered a line to cut the Rock off by land. | REVIEWER (dữ kiện) | S032 | S032: lệnh 1730, xong 1735 — câu chốt L15 chỉ đổi một từ |

### 2.1 Câu chủ dự án đã duyệt nguyên văn bị chạm (cần xác nhận)
| Câu | Duyệt ở | Đổi | Lý do |
|---|---|---|---|
| 1b "came in the name of 'Charles the Third'" | L4 | → "fought for the rival claimant, 'Charles the Third.'" | S020 MÂU THUẪN (nhân danh ai); 2/3 vai khó theo |
| 5f "Our read: the rich-looking number partly rests on the other side." | L13 | → "Our read: part of the work behind that number is done from the other side." | 3/3 vai + REVIEWER: câu cũ vượt claim (C14 không đỡ); câu mới trong phạm vi C08, giữ nhãn "Our read" |
| 5k "In 1730, Spain built a line…" | L15 | "built" → "ordered" | S032: lệnh 1730, hoàn tất 1735 |
| 2r (L8) | L8 | 869 thay 870; "from all causes" chỉ gắn 6 000; "count fewer dead" | dữ kiện |
| 2n (L8) | L8 | tách hai ước tính (chỉ số Anh gồm tù binh) | dữ kiện |
| 1h (Utrecht) | — | thêm câu 12 từ về điều khoản ưu tiên cho TBN (S025) | 3/3 vai cả hai vòng: trích Điều X một chiều |
**Không đổi:** SM1, SM3 (câu chủ dự án chốt), mở đầu E (0a–0e), 2h (L7), L5 (1d/1f), L9–L12.

### 2.2 Góp ý ≥ 2 vai KHÔNG sửa (lý do)
| Chỗ | Ai nêu | Vì sao giữ |
|---|---|---|
| 0d "Historians on both sides count fourteen sieges" | 3/3 cả hai vòng ("số đếm khác nhau") | claim S001–S008 XÁC MINH: 4 nguồn hai phía cùng hệ đếm 14; "15" chỉ có ở bách khoa (ẩn dụ 1969–85); thẻ trên hình nêu Sayer · García Sanz · Bảo tàng; L2 + mở đầu E đã duyệt. **Đề xuất xem lại ở G1b** (§8) |
| 0b ↔ 5i "no routine checks" ↔ "provisional" | 3/3 | đúng dữ kiện (C02, C26); đã nối bằng 5g ("the next day, routine checks here ended") + 5i "in force only provisionally" |
| SM1 dồn Chiến tranh Kế vị vào một câu; SM3 "run from inside the Rock", sơ tán từ 22/5 | 3/3; REVIEWER | câu chủ dự án chốt; SM3: REVIEWER vòng 2 xếp minor (sơ tán bắt đầu 22/5, "sends" thì hiện tại vẫn đúng tháng 6) — **nêu để chủ dự án quyết** |
| 3b "With Spain's consent" | 3/3 ("chọn bản có lợi cho Anh") | sự đồng ý là **nguồn TBN** (Gómez de Avellaneda, trích gốc trên hình) và đoạn kế (3c) là quan điểm sử gia TBN về lấn dần; chỉ hạ năm thành "Around 1810" (F13) |
| 2h cướp kho + lời sĩ quan Anh | 3/3 vòng 2 | L7 duyệt để cân bằng (chuyện xấu của phe giữ thành, có ghi ai nói) |
| 4h Tây Ban Nha không phản đối dải bay | 3/3 ("ngầm nói TBN chấp nhận") | đã đổi chữ (E25) + 4b nói đủ hai nửa S098 (F14); bối cảnh "Franco phụ thuộc Đồng minh" **không có claim** |
| 5a đóng biên giới 1969 không nêu lý do (Hiến pháp Gibraltar 1969) | R2, R3 | **không có claim** — cần tra nguồn trước khi thêm (§8) |
| 5f/5e "Here's the twist" + "Our read" vẫn bị chê là ý kiến | 3/3 | là nhận định có nhãn (L13); đã thu hẹp vào phạm vi claim |
| 2o đoạn hầm 1782 lùi thời gian sau cao trào; ch.3 chậm | 3/3 | thứ tự shot thuộc bảng shot đã duyệt; đã thêm "Before the attack" — đổi cấu trúc cần chủ dự án |
| KC1910 "Remember this street" phụ thuộc hình | 3/3 | là khung neo (§11.2); đã thêm "in La Línea" |
| 3h lời mời đăng ký giữa phim | R2, R3 vòng 1 | đúng ranh chương (Kinh thánh §3 FF2) và G1 đã duyệt |
| 1d số đạn 1704 | 3/3 vòng 2 | đã sửa (F02: "by British and Spanish accounts alike") |
| 2k "ships of the line" khó hiểu | R1, R2 | thuật ngữ đúng; hình hạm đội giải thích |

### 2.3 Còn lại sau khoá (không sửa được trong luật lệnh)
Mật độ số chương 2 và 5 (3/3 cả hai vòng), chương 3 "chậm" (3/3), hình dung ngày 13/9 (3/3) — là việc dựng (hình, nhịp, bộ đếm giờ) ở G1b, không phải lời.

## 3. Câu thời sự — đọc lại 18/10/2026 (tệp thô ngoài git `/var/tmp/cine-out/t3-khoa/raw/`)
| Câu (shot) | Claim | Nguồn đọc lại | SHA-256 tệp | Kết quả | Lời |
|---|---|---|---|---|---|
| "Since July 2026, this gate has had no routine checks." (0b) | C02 | FCDO Explanatory Memorandum CP 1645 (.odt): mục tiêu "operate without routine checks"; §5.6 áp dụng tạm thời từ 15/7/2026; trích lưu trong C02 vẫn có nguyên văn | `c363a24a…f8d5c` | không đổi | giữ |
| "In July 2026, Britain and the EU signed a treaty…" (5g) | C01, C02 | FCDO press release 14/7/2026 ("Published: 14 July 2026") | `fb5dbddc…2717e` | không đổi | chữ đổi do kiểm mù (E29): "signed a treaty; the next day, routine checks here ended" (ký 14/7 · áp dụng 15/7) |
| "…puts the daily crossers higher, at about fifteen thousand." (5c) | C09b | cùng trang FCDO: "the 15,000 people – over half of Gibraltar's workforce – who cross…" | `fb5dbddc…` | không đổi | thêm "higher" (F16) |
| "It says it changes neither side's position on sovereignty." (5h) | C07 | Hiệp ước Điều 2 (trích lưu) — văn bản ký không đổi | — | không đọc lại (văn bản hiệp ước) | giữ |
| hàng rào cũ/mới, 150 m (5h) | C03 | HMGoG 517/2026: "As the old chain-link… comes down, a new… fence line has already been erected only a few metres away"; "The only section without a border fence **will be** the area of approximately 150 metres by the loop, where pedestrians have always crossed" | `d7e72413…b30` | không đổi | chữ đổi (E30 + F17): ghi "In July, Gibraltar's government said…", 150 m "would stay open" (tin 2/7 là kế hoạch) |
| "As of 18 October 2026, the treaty is in force only provisionally, pending a European Parliament vote indicated for the fourteenth of December." (5i) | C26 | EP Legislative Train 2026/0058(NLE), "Information updated as of 20/09/2026": "entered into provisional application on 15 July 2026 … The European Parliament will need to give its consent … Indicative plenary sitting date is set for 14 December 2026"; tìm kiếm tin 10/2026: không có thay đổi (Lords Grand Committee bàn hiệp ước 20/10/2026) | `60eecfb1…c38f` | không đổi | "provisional" → "in force only provisionally" (E31 + F18) |
| "In October 2025, people living in Spain held more than four in ten of Gibraltar's jobs." (KB2026) | C08 | Employment Survey 2025 vẫn là bản mới nhất (khảo sát tháng 10; bản 2026 chưa có) | — | không đổi | giữ |
| "In 2024, La Línea's unemployment was twenty-eight point six percent…" (KC2026) | C14 | INE API UA121870: năm mới nhất vẫn 2024 = 28.6 | `d3c65edb…44da` | không đổi | giữ |
| "Gibraltar's government puts output per resident at about eighty-five thousand pounds." (5e) | C11 | Budget Address 7/7/2026 — số của năm ngân sách | — | không đổi | giữ |
| "…cut off" 1969 (5b) | C19 | Hansard 1969 (lịch sử) | — | — | thêm ai đếm (E27) |
Ghi chú: trang FCDO nay mang dòng "This was published under the 2024 to 2026 Starmer Labour government" — tức đã có chính phủ Anh mới; **không claim nào trong lời phụ thuộc chuyện này** (lời nói "Britain", "the UK government"). Cần đọc lại C02, C26 **trước khi đăng** (TIEN-KY-VAY-HAM §7.3).

## 4. Lời khoá + SHA (`LOI-KHOA.sha256`, khuôn T2: `sha256sum`)
```
1d3a2454a7ea100d525a85da7b4a6abb3cd3b35926ccdd1e280d29c12ef80ec1  script-v4-KHOA.md
a03265c036111b275c1efa8167c2438179a335fcd63748c4918a72e928be550f  loi-khoa.txt
3a70a020da3e084363f2f3e465a73eb9b48d5bc3cc3132d7bd70c5dfb64f0f24  khoa-loi/phat-am/gibraltar-eric.pls
```
- `script-v4-KHOA.md`: lời khoá có mã shot/claim + chữ trên hình (nguồn thật cho dựng). `loi-khoa.txt`: văn bản đọc cuối như T2 (đầu chương `[NN PART]`, mỗi shot một đoạn, bỏ mã/chữ trên hình/tấm im lặng/shot không lời). Sinh bằng `khoa-loi/lam_loi_khoa.py` (chạy lại cho ra cùng SHA). Kiểm: `sha256sum -c LOI-KHOA.sha256` trong thư mục tập.
- **Từ điển** `khoa-loi/phat-am/gibraltar-eric.pls` (PLS 1.0, `xml:lang="en-GB"`, chỉ `<alias>`, cụm dài xếp trước) + `tu-dien.json` (chữ viết · alias · IPA tham khảo · ghi chú) + `loi-khoa.tts-preview.txt` (lời sau khi áp alias, chỉ để soi; 9 955 ký tự). Cách đọc chọn: La Línea "LEE-neh-ah", Concepción / Algeciras theo **giọng Andalucía (seseo)** — cách người địa phương đọc; San Roque "ROH-keh"; Rooke "rook"; Crillon "kree-YOHN"; d'Arçon "dar-SOHN"; năm kiểu Anh (1704 "seventeen oh-four", 2026 "twenty twenty-six"); "18 October 2026" → "the eighteenth of October, twenty twenty-six". **Chưa nghe thử** (ElevenLabs = 0) — lần thu đầu phải ASR soi các mục này (BAI-HOC #19).
- **Thời lượng theo lời khoá** (`khoa-loi/fit_khoa.py` → `khoa-loi/dur-khoa.json`; giá trị G1 giữ ở trường `dur_g1` trong `vay-ham/treatment.json`): 15 shot đổi — tăng 1d 11,5→13,5 · 1g 12,5→14 · 1i 10→13 · 2b 9→10,5 · 2f 5,5→6 · 2i 5,5→6 · 3e 5→6 · 4e 7→7,5 · 4h 9→11,5 · 4i 14→16 · 5f 15→16,5 · 5h 14→16; giảm 1j 11,5→10 · 3h 10→9,5 · 4d 11→10,5. Theo chương: Móc 44,5 · 1: 122,5 · 2: 204,0 · 3: 84,5 · 4: 111,5 · 5: 151,0 s. Mốc đinh, cú liên hoàn, khung neo, tấm im lặng **không đổi**.
- `tu_kiem.py`: **ĐẠT** (Q26b 8/36,6 % · 6/42,9 %; NC-H1 0 lỗi; NC-H2 1 × 2,5 s; NC-H3 99,4/92,4 %; strategic 3,06 %; khung neo 6, 7–10 s; ai_image 7,3 %; im lặng 2 × 9 s; lặp ≤ 2; footage 1,1 %; 0 shot thiếu claim; 6 mốc đinh; 2 cú liên hoàn). `kiem_loi.py`: 0 lỗi (claim lạ / CHƯA XÁC MINH / số thương vong không nói ai đếm / tấm im lặng có lời); bộ lọc CS bắt 8 câu, đều đã xét (`g1/kiem-chu.md` §3). `g1/kiem-chu.{json,md}` sinh lại trên lời khoá.

## 5. Tệp
| Tệp | Nội dung |
|---|---|
| `G1-DUYET.md` | quyết định G1 nguyên văn |
| `script-v4-KHOA.md`, `loi-khoa.txt`, `LOI-KHOA.sha256` | lời khoá |
| `khoa-loi/script-v2.md`, `script-v3.md` | v1 + ngày; v3 sau vòng 1 |
| `khoa-loi/sua_v3.py`, `sua_v4.py` (+ `sua-v3.json`, `sua-v4.json`) | mọi sửa: trước/sau/ai nêu/claim/lý do |
| `khoa-loi/kiem_mu_loi.py`, `kiem-mu/` | kiểm mù + REVIEWER, kết quả thô + sổ chi phí `cost.jsonl` |
| `khoa-loi/fit_khoa.py`, `dur-khoa.json` | thời lượng theo lời khoá |
| `khoa-loi/lam_loi_khoa.py`, `phat-am/` | loi-khoa.txt, từ điển, SHA |

## 6. Chi phí thật
| Mục | Trần | Thật |
|---|---|---|
| Claude API (`claude -p`) | ≤ $3 | **$2,773** — kiểm mù vòng 1 $0,366 · vòng 2 $0,417 (Sonnet 5.5; ~40,7 nghìn token vào/lệnh) · REVIEWER vòng 1 $1,045 · vòng 2 $0,946 (Opus 5.5; 93–97 nghìn vào gồm cache, 18,5–24,5 nghìn ra). `modelUsage` báo thêm `claude-haiku-5-5` (CLI tự gọi việc phụ, đã tính trong $). Sổ `khoa-loi/kiem-mu/cost.jsonl` |
| ElevenLabs | 0 | **0** |
| YouTube Data API | 0 | **0** |
| Giờ máy | ≤ 1,5 h | **≈ 0,5 h** (02:35 → ~03:05 UTC; script < 2 s/lần; còn lại là `claude -p` và tải 5 tệp ≈ 0,3 MB) |
Dòng đề xuất cho `COST-LEDGER` (P ghi): `T3-KHOA-LOI | 18/10/2026 | API $2,773 | YT 0 | EL 0 | máy ≈ 0,5 h | nhánh claude/k2c-t3-loi-khoa-al1itg`.
Nhận xét chi phí: REVIEWER Opus chiếm 72 % ($1,99) chủ yếu do bảng claim (~55 nghìn token) và đầu ra dài; lần sau nên chỉ đưa claim của shot đổi ở vòng 2+, để đủ ngân sách cho vòng 3.

## 7. Tự quyết của phiên (không dừng hỏi)
1. Không áp máy móc các mục "block" của REVIEWER vòng 1 (luật MÂU THUẪN trong prompt sai — lỗi của phiên, đã sửa ở vòng 2).
2. Không chạy REVIEWER vòng 3 (trần $3); 19 sửa vòng cuối tự đối chiếu claim từng câu.
3. Đặt lại thời lượng theo lời khoá bằng đúng luật G1 (cho phép rút shot có lời ngắn hơn) → 718,0 s, sát trần 12 phút; không cắt câu nào chỉ để lọt trần.
4. Đặt `script-v4-KHOA.md`, `loi-khoa.txt`, `LOI-KHOA.sha256` ở gốc thư mục tập như T2; SHA thêm dòng PLS.
5. Năm trong `loi-khoa.txt` giữ chữ số như T2; cách đọc nằm ở từ điển alias (không đổi chữ lời).
6. 1e: ngày lịch cũ (24/7) chuyển lên chữ trên hình, lời nói "by the new calendar" (3/3 vai hai vòng).

## 8. Việc đang chờ chủ dự án
1. **Xác nhận các câu đã duyệt bị chạm** (§2.1: 1b/L4, 5f/L13, 5k/L15 một từ, 2n–2r/L8, câu Utrecht mới ở 1h) và **thời lượng mới 718,0 s** (từ 702 s, sát trần 12 phút).
2. **Quyết các góp ý 3/3 không sửa** (§2.2): "fourteen sieges" ở 0d (giữ L2 hay "By the traditional count…"), SM3 (sơ tán từ 22/5; "run from inside the Rock"), lý do đóng biên giới 1969 (cần claim mới), đoạn hầm 1782 đặt sau cao trào.
3. **G1b (animatic) chờ cổng hình V5b-2d + V6.**
4. Trước thu giọng: nghe thử từ điển (47 mục) + ASR; trước đăng: đọc lại C02, C26 (và EP sau phiên 14/12).
5. **AUTHORSHIP (P ghi):** mở đầu E, khung neo (từ G1) + các câu §2.1 nếu duyệt. **Giao K:** luật khung neo/ai_image/tấm im lặng (khối [G1] `tu_kiem.py`) như G1 §9.5.
6. **RIGHTS (P ghi):** như G1 §9.6 (Hansard OPL nếu trích chữ lên hình; HyperWar/Howe PD). Chữ trên hình mới ở 2i (Drinkwater 1785, PD) và 4e (HMGoG 2017 · Hansard 2015).

**DỪNG — lời T3 đã khoá.**
