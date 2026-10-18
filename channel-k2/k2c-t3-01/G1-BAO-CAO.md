**Nhánh thật: `ccr-3225b6a6-1yeft3`** (harness buộc nhánh này thay cho `k2c-t3-g1` của lệnh; tạo từ `origin/main` @ `82a17aef`, rồi `git merge origin/tuyen-t3` @ `434a90fc` — fast-forward, chỉ `channel-k2/k2c-t3-01/tuyen/**`). Đã đẩy, **không merge**.

# K2C-T3-01 "Why Gibraltar Was Besieged 14 Times" — GÓI DUYỆT LỜI G1 — DỪNG chờ chủ dự án

> Phiên G1 T3, 18/10/2026. Chỉ sửa `channel-k2/k2c-t3-01/**` và `docs/BIBLE-KENH2.md` (chỉ bước 0). Không sửa `scripts/`, `checks/`, `design/`, `reports/`, nhánh khác. Đã đọc: Kinh thánh bản 18/10 (vừa ghi), `TIEN-KY-VAY-HAM.md`, `claims-vay-ham.md` + JSON, `vay-ham/treatment.json` + `tu_kiem.py`, `tuyen/TUYEN-BAO-CAO.md` (+ patch, diff, claims-tuyen), khuôn G1 của T2 (`k2c-t2-01/G1-BAO-CAO.md`, `script-v2.md`), `reports/m3/BAI-HOC-LL.md`; `reports/NC-LICH-SU-BAO-CAO.md` chỉ tra mục cần (luật câu chữ chiến sự đã nằm sẵn ở TIEN-KY-VAY-HAM §6).
> Số đo là số đo **trên bảng shot và lời** (chưa có hình dựng, chưa thu giọng). Thời lượng lời là **ước** ở 2,5 từ nói/s.

## Khối điều lệ (lệnh + thực tế)
| Trường | Lệnh | Thực tế |
|---|---|---|
| Nhánh | `k2c-t3-g1` từ `origin/main` + merge `origin/tuyen-t3` | harness buộc `ccr-3225b6a6-1yeft3` (dòng đầu); merge ff `434a90fc` |
| Bước 0 | ghi KHỐI KINH THÁNH nguyên văn, commit riêng | `bf8ad8ed` "Kinh thánh kênh 2 bản Project 18/10" — thay toàn bộ tệp, không sửa chữ nào |
| Tệp được sửa | `channel-k2/k2c-t3-01/**` + Kinh thánh | đúng; tệp mới chủ yếu ở `g1/` (+ `g1/.gitignore` mở lại `*.json` như gói TUYẾN) |
| Trần | Claude API ≤ $3 · ElevenLabs 0 · YouTube ≤ 300 đv · giờ máy ≤ 2 h | **$1,807** · **0** · **0 đv** · **≈ 0,6 h** (§7) |
| Preflight / email | bắt buộc; che email | hook bị trình phân loại tự động của môi trường chặn (cài hook = "persistence") → chạy `tools/preflight.sh` tay trước mỗi commit: **ĐẠT**, `lock.py --verify` **KHỚP**; 0 email trong tệp ghi |
| Dừng | không dừng hỏi giữa chừng | đúng; các câu tự quyết ghi ở §8 |

---

## 0. Tóm tắt (đọc 2 phút)
1. **Bảng shot:** đã áp `tuyen/treatment-patch.json` (SM1–SM3 + 4 inset) và `tu_kiem_strategic.diff` — kết quả **trùng đúng số TUYẾN báo** (563,5 s; strategic 3,55 %; NC-H2 1 lần 2,5 s; NC-H3 ≤ 3 km 92,3 %; Q26b 7 loại/nửa). Thêm **6 KHUNG NEO** (3 vị trí × 2 mốc, 2 tấm im lặng) và **đặt lại thời lượng theo lời thật** → **74 shot, 702,0 s (11:42)**, tự kiểm **ĐẠT** mọi luật (§1).
2. **Lời v1** (`script-v1.md`): **1 512 từ viết / 1 593 từ nói**, ước **637 s ở 2,5 từ nói/s** (≈ 600 s theo nhịp Eric đo ở T2), móc **44,5 s**, Móc + 5 chương; mọi câu gắn claim; 15 câu trích nguyên văn phía đối phương trên hình kèm bản dịch (O4). Hai sửa đã chốt áp **nguyên văn** (SM1 có Áo; SM3 "run from inside the Rock").
3. **Torch "qua eo":** thêm claim **G001 (XÁC MINH, 3 nguồn)** — Hansard 3/3/1943 ("the safe delivery through the Straits of Gibraltar of the largest expeditionary armada in history…"), Howe 1957 ch. XIII, Hansard 3/12/1942 — và **G002 (XÁC MINH)** "từ Mỹ và từ Anh" (Hansard 3/12/1942 + Howe) = nguồn thứ hai cho T025. Lời: *"The invasion fleets, from Britain and the United States, came through the Strait."* 5/5 câu trích khớp tệp có đúng SHA.
4. **O7 — 3 mở đầu + bảng người xem mô phỏng** (5 vai × 2 thứ tự xáo × 4 lượt, 35 lệnh `claude -p` ghim Sonnet 5.5): thử A "Cổng", B "Con số", C "Chìa khoá", rồi C′ và A′ theo góp ý. **Đề xuất E (A′)**: 10/10 xem tiếp, không vai nào chấm dưới 5 (§4).
5. **Kiểm chữ** (`g1/kiem-chu.md`): 0 lỗi claim, 0 câu tính từ đạo đức, mọi số thương vong nói ai đếm, 14/14 trích trên hình khớp nguyên văn trong claim; từ điển đọc 27 năm.
6. **Chi phí thật:** Claude API **$1,807 / $3** · ElevenLabs **0** · YouTube **0 đv** · giờ máy **≈ 0,6 h**.

**Chỉ số trong ±5 % quanh ngưỡng (nêu tên):**
| Chỉ số | Đo | Ngưỡng | Lệch |
|---|---|---|---|
| Tổng phim (bảng shot) | 702,0 s | 12 phút = 720 s (Kinh thánh §3 "tới 12 phút khi đủ chương thật") | −2,5 % |
| Móc | 44,5 s | ≤ 45 s | −1,1 % |
| Hồ sơ thật (tranh + ảnh + bản đồ lịch sử) | 21,2 % | ~21 % (§10.8, tập lịch sử) | +1,0 % |
| Strategic SM3 | 8,0 s | ≤ 8 s/lần | 0 % (câu SM3 đã chốt 32 từ nói ≈ 13,2 s → chảy sang 4g 5,5 s, khớp mũi tên sơ tán) |
| Khung neo KC2026 | 10,0 s | 6–10 s | 0 % (lời 10,4 s → tràn 0,4 s sang thẻ 5e) |
| Khung neo KB2026 | 9,5 s | ≤ 10 s | −5,0 % |
| Lặp vùng + góc | 2 (mỗi vị trí khung neo) | ≤ 2 | 0 % — khung neo quay lại có chủ đích (§11.2) |
| 0c (lần duy nhất > 50 km) | 3,0 s, lời 4,4 s | ≤ 3 s (NC-H2) | 0 % — lời chảy sang thẻ 0d |
| Shot ảnh/tranh/bản đồ chạm trần 12 s | 1h, 2k, 2l, 2r | ≤ 12 s (có máy trượt/tô dòng, §10.5) | 0 % — 1h tràn 1,6 s sang 1i (cùng chủ đề Utrecht) |
| Người xem mô phỏng | bản E 6,2/10 | không có ngưỡng | — |
Ngoài ±5 % (đã xét): strategic 3,13 % so 15 %; ai_image 7,5 % so 20 %; NC-H3 ≤ 60 km 99,3 % so 70 %, ≤ 3 km 92,4 % so 40 %; footage 1,1 % so 20 %; tấm im lặng 9 s và 9 s so 8–10 s (+12,5 % so sàn).

**Việc chờ chủ dự án:** §9.

---

## 1. Bảng shot: trước / sau

### 1.1 Áp gói TUYẾN (lệnh mục 1)
- `vay-ham/treatment.json` (SHA trước `b7f455d0…`) ← `treatment-patch.json` (3 chèn + 7 cập nhật); `vay-ham/tu_kiem.py` ← `tu_kiem_strategic.diff` (`patch -p0` sạch). Bản sau-TUYẾN lưu ở `g1/treatment-sau-tuyen.json`.
- Thêm khối luật **[G1] khung neo** vào `tu_kiem.py`: 4–6 khung neo, mỗi khung 6–10 s; `ai_image`/`ai_texture` ≤ 20 %; 1–2 tấm im lặng 8–10 s; vào điều kiện ĐẠT chung. (Đề xuất cho K khoá thành luật như E8 của TUYẾN — §9.)

| Luật | Ngưỡng | TRƯỚC (T3b) | SAU TUYẾN | SAU G1 |
|---|---|---|---|---|
| Tổng · số shot | 9–12 phút | 563,5 s · 65 | 563,5 s · 68 | **702,0 s · 74** |
| Q26b-K2 nửa 1 / nửa 2 | ≥ 3 loại; ≤ 70 % | 6/42,2 % · 6/39,1 % | 7/37,6 % · 7/39,1 % | **8/36,3 % · 6/43,4 %** |
| NC-H2 | > 50 km ≤ 1 lần ≤ 3 s | 1 × 2,5 s | 1 × 2,5 s | **1 × 2,5 s** |
| NC-H3 ≤ 60 km / ≤ 3 km | ≥ 70 % / ≥ 40 % | 99,2 / 87,5 % | 99,2 / 92,3 % | **99,3 / 92,4 %** |
| NC-H1 | 0 lỗi | 0 | 0 | **0** (23 shot phố) |
| Strategic | ≤ 15 %, ≤ 8 s, ≤ 2/chương, không liền | — | 3,55 %, 7 s | **3,13 % (22 s), 8 s, 1/1/1, không liền** |
| Khung neo | 4–6, 6–10 s | — | — | **6; 7–10 s** |
| ai_image | ≤ 20 % | — | — | **7,5 % (52,5 s)** |
| Tấm im lặng | 1–2, 8–10 s | — | — | **2 × 9 s** |
| Lặp vùng + góc | ≤ 2 | 1 | 1 | **2** |
| Footage | ≤ 20 % | 0,9 % | 0,9 % | **1,1 %** |
| Hồ sơ thật | ~21 % | 20,7 % | 20,7 % | **21,2 %** |
| Shot thiếu claim | 0 | 0 | 0 | **0** |
| Mốc đinh | ≥ 1/chương | 6 | 6 | **6** (1e 86,0 · 2g 222,5 · 2m 292,0 · 3b 375,5 · 3f 416,5 · 4b 458,0 s) |
| Cú liên hoàn | 1–2 | 2 | 2 | **2** (4b giữ 15 s — gib20 đã dựng) |

### 1.2 Sáu khung neo (`g1/neo.json`; Kinh thánh §11.2, §11.3 a)
Ba vị trí máy cố định tầm mắt 2–3 m, mỗi vị trí quay lại ở hai mốc; ngày → đêm (đêm làm từ lượt chiếu sáng A); một tấm C ban ngày/khung neo × mốc; nhãn "Surface detail AI-assisted · layout, landmarks & flags from sources".

| Khung | Đặt trước | Nơi | Mốc | Dài | Tấm C | Có sẵn | Vai truyện |
|---|---|---|---|---|---|---|---|
| KA1782 | 2j | hẻm K09/K10 (phố cổ) | 9/1782 | 8 s | có | **PT2** | đứng trong phố bị vây ngay trước cao trào; lời: 7 500 người giữ Rock (S079) |
| KC1910 | 3e | phố hẹp La Línea gần cổng (Catastro BU 11022) | 1910 | 7 s | có | mới | *"Remember this street. We'll come back to it."* — gài cho ch.5 |
| KB1943 | 4h | Commercial Square | 1943 | 9 s | có | **PT2** | **IM LẶNG #1**: quảng trường chỉ có đàn ông (lính, thuỷ thủ, thợ) ngay sau câu "Gibraltar sends its women and children away" |
| KB2026 | 5c | Commercial Square | 2026 | 9,5 s | có | mới | cùng khung, nay đông người; 4 trong 10 việc làm là của người sống bên Tây Ban Nha (C08) |
| KC2026 | 5e | phố La Línea | 2026 | 10 s | có | mới | trả lời KC1910: thất nghiệp 28,6 % (C14), ngay trước cú lật GDP/người |
| KA2026 | 5k | hẻm K09/K10 | 2026 | 9 s | có | mới | **IM LẶNG #2**: cùng hẻm thời vây, nay — rồi câu chốt |

Ghi chú dựng: KA1782 đặt **sáng → chiều tối, không đêm** (tránh trùng khói/lửa 13/9); dân thường trong phố 9/1782 **chưa có claim thành phần** → mặc định chỉ lính/thuỷ binh, không phụ nữ/trẻ em (việc chờ); KC: chọn phố ở G1b sao cho trời ≤ 25 %, đất trống ≤ 1/3, đo trên khung A trước khi gọi AI; 1910 chỉ đặt toà Catastro có năm xây ≤ 1910, lô trống để trống. 5d rút 11 → 4,5 s vì phần "thất nghiệp neo trên phố" chuyển sang KC2026.

### 1.3 Thời lượng theo lời (`g1/fit_dur.py` → `g1/dur-g1.json`; 56 shot đổi, giá trị cũ giữ ở trường `dur_t3b`)
- Luật: cần = từ nói/2,5 + 0,4 s; dur = max(⌈cần⌉, sàn) — sàn = dur cũ cho mốc đinh/cú liên hoàn/khung neo, 3 s cho móc, còn lại min(dur cũ, cần + 0,5 s) ≥ 4 s; trần theo loại (thẻ 8 · ảnh/tranh/bản đồ lịch sử 12 · strategic 8 · khung neo 10); cố định 4b 15 s, 0c 3 s, 4g 5,5 s.
- Theo chương (T3b → G1): Móc 43,5 → 44,5 · Ch.1 101,5 → 117,5 · Ch.2 168,5 → 201,5 · Ch.3 70,5 → 84,0 · Ch.4 79,0 → 107,0 · Ch.5 100,5 → 147,5 s. Lý do tăng: treatment T3b là ước "không lời"; lời thật cần ≈ 637 s nói + 18 s im lặng + chỗ thở.
- Lời tràn > 1,5 s sang shot sau còn 2 chỗ, đều **cùng chủ đề**: 1h → 1i (Utrecht), SM3 → 4g (thiết kế).

## 2. Lời — tóm tắt theo chương (`script-v1.md`; bảng từng shot ở `g1/kiem-chu.md` §2)
| Chương | Dài | Từ nói | Câu hỏi → trở ngại → bước ngoặt → hệ quả | Nhân vật / hai phía |
|---|---|---|---|---|
| **Móc — Midnight at the Gate** | 44,5 s | 103 | (bản E) người đi bộ qua đường băng lúc nửa đêm → cổng không còn kiểm tra từ 7/2026 → "cửa tây Địa Trung Hải" → 14 cuộc vây theo sử gia hai phía → pin nổi 1782, đường băng 1941 → *"So why, today, is the fight over it about paperwork and payrolls?"* | thẻ 14: Sayer 1862 · García Sanz 2022 · Bảo tàng Gibraltar |
| **1 — 1704: A Rock Changes Hands** | 117,5 s | 278 | vì sao một hạm đội muốn một tảng đá → tường + vài trăm người giữ → đầu hàng 4/8/1704 (24/7 lịch cũ) → dân sang San Roque; Utrecht 1713 "without any territorial jurisdiction…"; hai lập trường về eo đất; 1704–05, 1727 thất bại; chiến tuyến 1730 → tên "La Línea" | Rooke + Hesse-Darmstadt "nhân danh Charles III" ↔ Salinas; số người giữ hai phía (Montero ~100 ↔ Anh ≤ 500); "chìa khoá" Montero 1860 + Sayer 1862 |
| **2 — The Great Siege** | 201,5 s | 469 | bỏ đói được một tảng đá không → phong toả bộ + biển, đói, scorbut → phố bị bắn 12/4/1781; đạn đỏ; 13/9/1782 (09:30 → 09:45 → 10:25 theo hai phía) → 10 pin nổi mất, đường hầm 1782, phát súng cuối 5/2/1783; tổn thất hai phía cùng cách tính "mọi nguyên nhân" | Eliott ↔ Crillon, d'Arçon (bản biện hộ Pháp: xin thử đạn đỏ bị từ chối); Ince và 13 thợ mỏ; lính đồn cướp kho — lời người Anh "resentment and intoxication" |
| **3 — The Neutral Ground** | 84,0 s | 186 | Rock kết thúc ở đâu → hiệp ước không nói → 1810 phá pháo đài (TBN đồng ý); Anh lấn dần (lời sử gia TBN); hàng rào 1909 → La Línea mọc; trường đua → dải cỏ 1934 | khung neo La Línea 1910; mời đăng ký ở ranh chương |
| **4 — A Runway on the Isthmus** | 107,0 s | 231 | vì sao xây sân bay trên đất tranh chấp → TBN phản đối 1939 ("porción usurpada", "fait accompli") → 1941 đường băng cắt đường sang TBN, lấn vịnh bằng đá hầm → sơ tán 1940 (tấm im lặng), không có phản đối về dải bay suốt chiến tranh (sử gia TBN), 650 máy bay, hạm đội Torch qua eo | đội đào hầm Anh + Canada; Eisenhower trong lòng Rock (SM3) |
| **5 — The Gate** | 147,5 s | 326 | khi cổng đóng ai mất gì → 1969–85; nay 4/10 việc làm của người sống bên TBN; La Línea 28,6 % thất nghiệp → **cú lật**: £85 145/người chia cho dân cư trú, bỏ ngoài người làm từ TBN ("Our read") → hiệp ước 2026 tạm áp dụng, EP 14/12 → bảng điểm "a wall 1704, a line 1730, a fence 1909, a runway 1941" → tấm im lặng hẻm 2026 → câu chốt nghịch lý + dẫn London 1666 | người lao động qua biên giới (nhóm A-lite) |

Câu chốt (5k): *"In 1730, Spain built a line to cut the Rock off by land. Today, four in ten of the Rock's jobs are held by people who live beyond it. The last siege ended in 1783. The argument didn't. Next in Contested Places: London, 1666."*

## 3. O4 — nguồn phía đối phương trích nguyên văn (chỉ nguồn đã có trong claims)
| Shot | Đoạn hai phía | Trích (nguyên văn trên hình) | Bản dịch trên hình | Claim |
|---|---|---|---|---|
| 1c | "chìa khoá" | Montero 1860: «la preciosa llave del Mediterráneo» | "the precious key of the Mediterranean" (+ Sayer 1862) | S010 |
| 1d | quân giữ 1704 | Montero 1860: «con cien hombres de guarnición … no había artilleros que las sirvieran» | "a garrison of a hundred men … there were no gunners to serve them" | S015 |
| 1g | dân rời đi | Montero 1860: «se habia acampado en las haciendas cercanas á la ermita de San Roque» | "had camped on the farms near the hermitage of San Roque" | S019 |
| 1k | chiến tuyến 1730 | Gómez Nadal (Almoraima): «bloquear definitivamente la correspondencia y paso a la plaza por tierra» | "to block, once and for all, all contact with and passage to the town by land" | S032 |
| 2b | TBN vào chiến tranh | Montero: «Carlos III declaró la guerra á Inglaterra y se unió á Francia» | "Charles III declared war on England and joined France" | S039 |
| 2c | phong toả | Montero: «encaminado principalmente á privar a la plaza de los viveres que le llegaban de las costas de África» | "aimed above all at depriving the town of the food that reached it from the coasts of Africa" | T006 |
| 2k | hạm đội liên hợp | **Fernández Duro 1901**: «alegrando la vista los 50 navios que se juntaron en Algeciras» | "the 50 ships of the line that gathered at Algeciras, a joy to see" | T018 |
| 2l | pin nổi | Conseil de guerre privé 1785: «l'expérience que l'inventeur avoit demandée … à l'épreuve des boulets rouges» | "the test the inventor had asked for … against red-hot shot" | S073 |
| 2m | giờ khai hoả | Montero: «á las diez y veinte y cinco minutos de la mañana … rompieron á un tiempo el fuego» | "at twenty-five past ten in the morning … opened fire all at once" | S067 |
| 2n | thương vong 13/9 | (thẻ số) bản biện hộ Pháp 1785: 185 trúng pháo trước khi cháy | — | S071 |
| 2p | lỗ châu mai | Montero: «se formó un boquete tan grande … que pareció bien colocar en el un cañón» | "an opening was made so large … that it seemed right to place a cannon in it" | S087 |
| 2r | tổn thất cả cuộc vây | Montero: «Los últimos sufrieron una pérdida de cerca de dos mil hombres. La nuestra se aproximó á seis mil por todas causas» | "The latter [the besieged] … nearly two thousand men. Ours came close to six thousand, from all causes" | S077 |
| 3b | phá pháo đài 1810 | Gómez de Avellaneda: «con autorización española, fueran destruidos por los ingleses» (+ "Montero gives 1811") | "with Spanish authorisation, they were destroyed by the British" | S034 |
| 3c | lấn vùng trung lập | García Sanz 2022: «el progresivo avance de la frontera sobre la zona neutral» | "the gradual advance of the frontier over the neutral zone" | S035 |
| 3f | hàng rào 1908–09 | García Sanz: «"como acto de cortesía"» | "as an act of courtesy" | S036 |
| 4a/4b | phản đối 1939 | Chính phủ TBN 4/3/1939 (qua Marquina Barrio 1981): «una porción usurpada del territorio nacional» | "a usurped portion of the national territory" | S096 |
| 4h | không phản đối dải bay | Marquina Barrio: «no queda constancia de reclamaciones por el uso de la pista» | "there is no record of complaints over the use of the strip" | S105 |
- Mọi trích là **chuỗi con của câu trích đã lưu trong claim** (kiểm máy, bỏ dấu/khoảng trắng, 14/14 khớp). Không thêm nguồn mới cho O4. Chính tả giữ theo bản in/OCR (á, «habia», «navios»); **phải đối chiếu ảnh trang trước khi lên hình** (OCR thế kỷ 19 — như T3b).
- Fernández Duro còn có ở SM1/SM2 (Bồ Đào Nha vào "gran liga", ngày Darby) — để ở dữ liệu bản đồ, không thêm chữ lên strategic (chú giải ≤ 3 phe, chữ tối thiểu).

## 4. O7 — ba mở đầu + bảng người xem mô phỏng (`g1/mo-dau.md`, `g1/mo_dau_panel.py`)
**Giao thức:** `claude -p --model claude-sonnet-5-5`, không công cụ, thư mục tạm trống; 5 vai (lướt điện thoại 23 tuổi · mê sử quân sự 54 · người Cádiz 38 · người Anh có cha từng ở đồn Gibraltar 61 · mê kinh tế–địa lý 31); ẩn tác giả (không nói ai làm/kênh/AI; bản gọi X/Y/Z; thứ tự xáo theo vai, 2 lượt xáo khác nhau mỗi vòng). Hỏi: sau 30 s có xem tiếp không + 0–10 + lý do + chỗ muốn bỏ; xếp hạng; một chỗ sửa. Kết quả thô: vòng 2 `g1/kiem-mu/mo-dau/`, vòng 3 `mo-dau-ACD/`, vòng 4 `mo-dau-ADE/` (mỗi thư mục có `gop.json` + từng vai, kể cả prompt nguyên văn).

| Vòng | Bản | Xem tiếp | Điểm TB | Hạng TB | Ghi chú |
|---|---|---|---|---|---|
| 1 (bỏ) | A/B/C | — | — | — | lỗi giao thức: mô tả hình đưa bằng tiếng Việt → bỏ, lưu `kiem-mu/mo-dau-luot1-hinh-tieng-viet/` |
| 2 | **C** "Chìa khoá" | 9/10 | **6,9** | 1,8 | hai phía ngang nhau được 3 vai khen; vai lướt: "giống bài giảng"; "Same rock…" sáo |
| 2 | A "Cổng" | 9/10 | 6,3 | 1,8 | hình đường băng mạnh; câu hiệp ước làm vai Anh + sử gia khó chịu |
| 2 | B "Con số" | 9/10 | 5,8 | 2,4 | "British and Spanish historians count the same way" bị nghi "quá gọn" (dù có nguồn) |
| 3 | A | 10/10 | **7,2** | **1,5** | |
| 3 | D (C′ theo góp ý) | 10/10 | 6,7 | 2,0 | |
| 3 | C | 10/10 | 5,9 | 2,5 | |
| 4 | **E (A′)** | **10/10** | 6,2 | 1,9 | **không vai nào < 5** (5–8) |
| 4 | A | 6/10 | 5,8 | 1,8 | phân cực: 8/8/8/8 (lướt, mê sử, kinh tế) ↔ 3/3/3/3 (Cádiz, người Anh) |
| 4 | D | 5/10 | 5,1 | 2,3 | phân cực ngược lại |

**Xếp hạng + đề xuất: 1. E (A′) · 2. A · 3. D (C′) · 4. C · 5. B.** Đề xuất **E**, lý do: bản duy nhất giữ 10/10 "xem tiếp" ở vòng cuối mà không mất nhóm nhạy cảm (người Cádiz, người Anh) — đúng rủi ro chính của tập (bình luận chủ quyền, Kinh thánh §9); A và D thắng từng nhóm nhưng thua nhóm kia. Điểm số dao động mạnh giữa các vòng (A: 6,3 → 7,2 → 5,8) → **xếp theo "xem tiếp" và độ phân cực, không theo điểm TB**; đây là chấm mô phỏng, không thay số đo thật sau đăng.

**Bản E (0a–0e, ≈ 26,4 s):** *Midnight at the Gibraltar frontier. To walk in from Spain, you cross an airport runway. · Since July 2026, this gate has had no routine checks. · The Rock sits at the western gate of the Mediterranean. · Historians on both sides count fourteen sieges of it, between 1309 and 1783. · This is why everyone fought over it, told from both sides' records.*
Đã áp từ góp ý ≥ 2 vai: bỏ "UK–EU treaty" và "edge of Spain" ở câu tin mới; thay "look where it sits" bằng câu cụ thể; thêm nguồn Tây Ban Nha (García Sanz 2022) lên thẻ 14; hai câu "chìa khoá" (Montero trước, theo năm) dời vào 1c. Góp ý **chưa áp** (cần chủ dự án): (a) "western gate" vẫn bị vai kinh tế chê là nhãn sách giáo khoa — muốn nói cơ chế (vd. bề rộng eo) cần claim mới; (b) vai mê sử nghi "14" là con số "đã chốt" → có thể đổi "Historians on both sides count…" thành "By the traditional count, …" (mất ý hai phía); (c) "only five changed who ruled it" (S008) bị đòi danh sách năm → đã bỏ khỏi mở đầu vì claim không liệt kê năm. Sau khi chọn E, câu "So why did everyone want this rock?" ở 0h bị bỏ (trùng 0e, giữ móc ≤ 45 s).

## 5. Câu cần chủ dự án duyệt (lời, tiêu đề chương, chữ trên hình)
| # | Shot | Câu / quyết định | Vì sao cần duyệt |
|---|---|---|---|
| L1 | 0a–0e | **mở đầu E** (§4) | chọn giữa E / A / D |
| L2 | 0d | "Historians **on both sides** count fourteen sieges…" | D1 đã duyệt câu không có "on both sides"; thêm để giữ lời hứa hai phía (S001 + S006 García Sanz) |
| L3 | SM1 | *Austria, England and the Dutch backed a rival for Spain's crown; France backed Madrid's king.* | câu đã chốt — áp nguyên văn, xác nhận lại (15 từ, 6,4 s/6,5 s) |
| L4 | 1b, 1g | "came in the name of 'Charles the Third'"; "Almost all of them left. By Spanish accounts, most settled … at San Roque." | S017/S020 MÂU THUẪN (chuyện kéo cờ Anh) → không kể; không suy động cơ người dân |
| L5 | 1d/1f | "barely a hundred soldiers, by a Spanish count" ↔ "British accounts … up to five hundred" | số hai phía |
| L6 | 1i | "Spain says the isthmus was never ceded. Britain says Gibraltar includes it." | lập trường chủ quyền hiện hành, hai phía một câu mỗi bên |
| L7 | 2h | "soldiers broke into the merchants' stores. A British officer blamed 'resentment and intoxication.'" | hành vi xấu của phe giữ thành — giữ cho cân bằng, có ghi ai nói |
| L8 | 2n, 2r | ">2 000 attackers lost, by British and Spanish counts; 357 rescued" · "From all causes, Montero put the losses near two thousand inside and six thousand outside. The garrison's own records count at least eight hundred and seventy dead." | §10.6: số nói ai đếm, cùng cách tính; **870 = 333 + 536 do phiên cộng** (Drinkwater, không gồm chết vì scorbut 1779–80) → "at least" |
| L9 | 3c | "A Spanish historian describes Britain advancing into the neutral zone step by step." | lập trường một phía, có ghi nguồn + trích gốc |
| L10 | 4a, 4b | "a usurped portion" · "fait accompli" | chữ của chính phủ TBN 1939, trong ngoặc + nguồn |
| L11 | SM3 | *June 1940: Spain turns "non-belligerent" and occupies Tangier. Gibraltar sends its women and children away. By 1942, the invasion of North Africa is run from inside the Rock.* | câu đã chốt — áp nguyên văn; 32 từ nói (13,2 s) > cửa sổ SM3 8 s → chảy sang 4g |
| L12 | 4i | "The invasion fleets, from Britain and the United States, came through the Strait." | dựa G001 + G002 (mới) — thay "qua eo" của lệnh; không nói "từ Gibraltar" |
| L13 | 5f | "Our read: the rich-looking number partly rests on the other side." | nhận định của kênh, gắn nhãn "Our read" |
| L14 | KC2026 | thất nghiệp La Línea 28,6 % đọc trên một phố thật | tránh dàn cảnh nghèo: người sinh hoạt thường ngày (neo.json) |
| L15 | 5k | câu chốt nghịch lý + "Next in Contested Places: London, 1666." | chốt + dẫn tập kế |
| L16 | 5i | "As of [ngày khoá lời] … indicated for the fourteenth of December" | điền ngày khi khoá lời; đọc lại C02, C26 trước khoá lời và trước đăng |
| L17 | 2k, SM2 | tuỳ chọn Minorca ("Between the second and the third, Spain took back Minorca") **không đưa vào lời** (SM2 + 2f đã đủ chữ); bản đồ vẫn đổi màu Minorca 5/2/1782 | chọn có/không |

Tên chương giữ của T3b: Midnight at the Gate · 1704: A Rock Changes Hands · The Great Siege · The Neutral Ground · A Runway on the Isthmus · The Gate.

## 6. Kiểm chữ (lệnh mục 5) — chi tiết `g1/kiem-chu.md`, máy: `g1/kiem_loi.py`
- **Số đọc thành chữ:** bộ đọc số (năm kiểu Anh: 1704 → "seventeen oh-four", 2026 → "twenty twenty-six"); 27 năm trong từ điển; số lớn viết sẵn bằng chữ trong lời. Đếm từ nói tách gạch nối (giống gói TUYẾN) → ước bảo thủ; theo nhịp Eric đo thật ở T2 (151,2 từ viết/phút) lời ≈ 600 s.
- **Độ dài từng đoạn so cửa sổ shot:** bảng 74 dòng; thời lượng đã đặt theo lời; 8 shot chạm trần theo loại (0c, 1h, 2l, 2r, 4b, SM3, KC2026, 5i) — lời tràn ≤ 1,6 s, trừ SM3 (thiết kế).
- **Câu nhạy cảm §10.6 / CS1–CS10:** 0 tính từ đạo đức cho phe; 0 "impregnable/heroic/crushed…"; 5 câu bộ lọc CS3 bắt ("the French and Spanish fleets", "the Spanish line", "the British blew up…") đều là chủ thể cụ thể → giữ; 2 câu CS1 ("usurped" trong trích; "occupies Tangier" đã chốt) → giữ, nêu ở L10–L11. **Mọi số thương vong nói ai đếm** (bộ lọc 0 lỗi).
- **Claim:** 0 id lạ, 0 claim CHƯA XÁC MINH được gắn (T025 không gắn — dùng G002).

## 7. Chi phí thật
| Mục | Trần | Thật |
|---|---|---|
| Claude API (`claude -p`, bảng người xem mô phỏng) | ≤ $3 | **$1,807** (35 lệnh; vòng 1 bỏ $0,258 · vòng 2 $0,506 · vòng 3 $0,529 · vòng 4 $0,514); vào 1,29 triệu token (gồm cache), ra 33,4 nghìn; `modelUsage` báo `claude-sonnet-5-5` + `claude-haiku-5-5` (Haiku do chính CLI gọi cho việc phụ, đã tính trong $) — sổ `g1/kiem-mu/cost.jsonl` |
| ElevenLabs | 0 | **0** |
| YouTube Data API | ≤ 300 đv | **0** |
| Giờ máy | ≤ 2 h | **≈ 0,6 h** (đồng hồ phiên 01:53 → 02:30 UTC; script < 2 s/lần; còn lại là `claude -p` + tải 6 tệp) |
| Mạng | — | 6 tệp (Howe ch. IV/X/XI/XIII HyperWar, 2 debate Hansard + 1 tìm kiếm) ≈ 0,3 MB, ngoài git `/var/tmp/cine-out/g1/raw/`; Howe ch. IV, XIII **SHA trùng** claims-tuyen |
Dòng đề xuất cho `COST-LEDGER` (P ghi): `T3-G1 | 18/10/2026 | API $1,807 | YT 0 | EL 0 | máy ≈ 0,6 h | nhánh ccr-3225b6a6-1yeft3`.

## 8. Tự quyết của phiên (không dừng hỏi)
1. Thời lượng phim tăng 563,5 → 702 s (lời thật cần ≈ 637 s). Đã cắt lời hai lượt (2 167 → 1 593 từ nói) để nằm trong 12 phút; không cắt chương.
2. Thêm khối luật khung neo vào `vay-ham/tu_kiem.py` (bảng tự kiểm của tập, không phải `checks/`).
3. 2 claim mới G001–G002 (schema của gói TUYẾN) thay vì sửa trạng thái T025 trong `tuyen/`.
4. Bỏ vòng 1 bảng người xem (lỗi mô tả hình tiếng Việt) — vẫn tính chi phí; chạy thêm 2 vòng sửa (C′, A′).
5. Câu tổn thất 2r đổi sang so cùng cách tính ("from all causes") vì bản nháp so 333 "killed" với 6 000 "mọi nguyên nhân" là so lệch.
6. Hook git không cài được (môi trường chặn) → preflight chạy tay mỗi commit.

## 9. Việc đang chờ chủ dự án
1. **Duyệt lời G1:** mở đầu E (L1) và L2–L17 (§5); điền ngày "as of" khi khoá lời.
2. **Duyệt bảng shot G1:** 6 khung neo (§1.2), thời lượng 11:42 (§1.3), hồ sơ thật 21,2 %; ghi AUTHORSHIP (khung neo + chọn mở đầu là quyết định sáng tạo then chốt).
3. **Duyệt G001–G002** (Torch qua eo; "from Britain and the United States"); tuỳ chọn nhãn "from Britain / from the USA" trên mũi tên SM3 (E2 của TUYẾN).
4. **Claim còn thiếu trước G1b:** thành phần dân thường trong phố 9/1782 (KA1782); trang phục La Línea c. 1910 (KC1910); đối chiếu ảnh trang mọi trích OCR lên hình (§3).
5. **Giao K:** khoá luật strategic (E8 TUYẾN) + luật khung neo/ai_image/tấm im lặng (khối [G1] trong `tu_kiem.py`).
6. **RIGHTS (P ghi):** Hansard (Open Parliament Licence) nếu trích chữ lên hình; HyperWar/Howe (US Army CMH — PD).
7. **Sau duyệt:** kiểm mù lời (3 vai) + REVIEWER theo chuẩn hiện hành (Kinh thánh §3) — **chưa chạy** ở phiên này (lệnh chỉ giao bảng người xem cho mở đầu); rồi G1b animatic.

**DỪNG chờ chủ dự án duyệt G1.**
