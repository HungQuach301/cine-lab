**Nhánh thật: `claude/k2c-t3-loi-khoa-al1itg`** (harness buộc nhánh này thay cho `k2c-t3-loi41` của lệnh). Gốc là commit `9cca02f0` (lời khoá v4, SHA `a03265c0…`); commit v4.1 nằm ngay sau trên cùng nhánh. Đã đẩy, **không merge**.

# K2C-T3-01 Gibraltar — KHOÁ LỜI v4.1 (LK1–LK4) — DỪNG

> Phiên T3 khoá lời, 18/10/2026, làm tiếp theo lệnh chủ dự án "khoá lời v4.1". Chỉ sửa `channel-k2/k2c-t3-01/**`. Ngoài hai sửa LK2 và LK3, **không câu lời nào khác bị đổi** (kiểm bằng diff `loi-khoa.txt`: đúng 2 đoạn đổi). Trần: Claude API ≤ $1 · ElevenLabs 0 · YouTube 0 · giờ máy ≤ 0,5 h → thật: **$0 · 0 · 0 · ≈ 0,2 h**. Đã chạy preflight: **ĐẠT** (`lock.py --verify` KHỚP); không có email trong các tệp ghi.

## 0. Tóm tắt
1. **G1-DUYET.md**: ghi nguyên văn LK1–LK4 (thêm vào cuối tệp).
2. **LK2 — SM3:** đưa ý sơ tán lên trước, dùng **33 từ nói ≈ 13,2 s**, nằm trong cửa sổ SM3 + 4g = 13,5 s. Câu mẫu trong lệnh có 35 từ ≈ 14,0 s, sẽ tràn 0,5 s sang tấm im lặng KB1943 (§1).
3. **LK3 — 1969:** thêm claim mới **G003** (XÁC MINH, 1 nguồn chính HMGoG + 3 nguồn đối chiếu học thuật Tây Ban Nha; 4/4 trích khớp tệp thô có đúng SHA). Thêm **1 câu 13 từ** vào 5a (§2).
4. **Thời lượng:** **74 shot, 719,7 s** (≤ 720 s). Không cắt lời. Đã rút hai tấm im lặng 9 → 8 s và ba thẻ số về đúng độ dài lời + 0,4 s (§3). `tu_kiem.py` **ĐẠT**; `kiem_loi.py` 0 lỗi; 16/16 trích trên hình khớp claim.
5. **Từ điển phát âm:** không có từ mới cần alias (Madrid, Utrecht, 1940 đã có hoặc đọc chuẩn) → PLS **giữ nguyên** (SHA không đổi).
6. **SHA mới** (§4): `loi-khoa.txt` `a03265c0…` → **`0fdc72ce…`**.

**Chỉ số trong ±5 % quanh ngưỡng (nêu tên):**
| Chỉ số | Đo | Ngưỡng | Lệch |
|---|---|---|---|
| Tổng phim | 719,7 s | 720 s | −0,05 % |
| Tấm im lặng KB1943, KA2026 | 8,0 s | sàn 8 s (§11.2: 8–10 s) | 0 % |
| Thẻ 1f / 2d / 5e | 5,625 / 7,625 / 6,417 s | lời + 0,4 s | 0 % (vừa khít lời) |
| SM3 + 4g (lời SM3) | 13,2 s | 13,5 s | −2,2 % |
| Móc | 44,5 s | 45 s | −1,1 % |
| Hồ sơ thật | 21,4 % | ~21 % | +1,9 % |
| Strategic SM3 · khung neo KC2026 / KB2026 | 8 · 10 / 9,5 s | 8 · 10 s | 0 % · 0 / −5 % |

**⚠ Lỗi có từ bản v4, báo cáo v4 bỏ sót:** lời 5j ("…A runway in 1941.") **tràn 1,4 s sang tấm im lặng KA2026** (nguyên nhân: thẻ 5i bị trần 8 s, lời cần 10 s, nên chảy dồn sang 5j). Hiện KA2026 dài 8 s nhưng chỉ ≈ 6,6 s thật sự im lặng (< sàn 8 s). Muốn sửa phải thêm ≈ 1,5 s vào 5j → tổng ≈ 721,2 s, vượt trần 720 s. Cắt lời thì lệnh cấm. **Chưa sửa — chờ chủ dự án chọn (§6).** Các bản kiểm hiện có không bắt lỗi này: `kiem_loi` chỉ kiểm tấm im lặng không có lời *của chính nó*, ngưỡng cảnh báo tràn là > 1,5 s.

## 1. LK2 — SM3 (trước / sau)
| | Câu | Từ nói | Ước |
|---|---|---|---|
| **Trước (v4)** | June 1940: Spain turns "non-belligerent" and occupies Tangier. Gibraltar sends its women and children away. By 1942, the invasion of North Africa is run from inside the Rock. | 32 | 12,8 s |
| Mẫu lệnh | From May 1940, Gibraltar sends its women and children away. In June, Spain turns "non-belligerent" and occupies Tangier. By 1942, the invasion of North Africa is run from inside the Rock. | 35 | 14,0 s — vượt cửa sổ 13,5 s, tràn 0,5 s sang tấm im lặng KB1943 |
| **Sau (v4.1)** | **May 1940: Gibraltar sends its women and children away. June: Spain turns "non-belligerent" and occupies Tangier. By 1942, the invasion of North Africa is run from inside the Rock.** | 33 | 13,2 s (lời vào 4g 5,2 s / 5,5 s) |
- Claim: {S114} {T021} {T022} {T023} {T024} {S122}. Giữ đủ S114, T021, T022, T024 như lệnh; T023 và S122 vốn có trong câu cũ nên giữ lại. S114: "Evacuation began on 22 May 1940 to French Morocco…".
- So với mẫu lệnh chỉ bỏ "From" / "In" và dùng nhãn mốc "May 1940: … June: …", cùng kiểu với câu SM3 cũ ("June 1940: …"). Ý và claim không đổi.
- Ghi chú cho G1b: mũi tên sơ tán trên bản đồ SM3 nay phải chạy ở **đầu** shot (trước là giữa shot); nhãn mốc đổi "May 1940" → "June 1940".

## 2. LK3 — lý do đóng biên giới 1969
### 2.1 Câu (5a, trước / sau)
| | Câu |
|---|---|
| **Trước** | After the war, the argument returned to the gate. In June 1969, Spain closed the land frontier completely. {C19} |
| **Sau** | After the war, the argument returned to the gate. In June 1969, Spain closed the land frontier completely. {C19} **It followed Gibraltar's new constitution; a Spanish historian says Madrid applied Utrecht strictly. {G003}** |
- Câu mới có 13 từ (≤ 20). Câu gồm hai ý. Ý thứ nhất là trình tự thời gian, hai phía khớp: HMGoG và Langa Nuño. Ý thứ hai là cách giải thích của phía Tây Ban Nha, có ghi rõ "a Spanish historian": Sánchez Mantero. Câu không dùng tính từ đạo đức. Câu không nói trưng cầu 1967, vì nguồn Tây Ban Nha nói đến trưng cầu **1964** về đổi hiến pháp, còn HMGoG không nối trưng cầu với việc đóng biên giới.
- Bản nháp đầu dài 16 từ ("It came sixteen days after Gibraltar's new constitution; a Spanish historian calls it applying Utrecht strictly."), đẩy tổng phim lên 724 s. Rút tấm im lặng và thẻ chỉ được ≤ 3,5 s, nên phải rút câu. Ý "sixteen days" còn trong claim (dùng được cho chữ trên hình ở G1b nếu muốn).
- Cụm "Madrid applied Utrecht strictly" dựa đúng nguyên văn: «lo que hizo el Gobierno español fue aplicar estrictamente los terminos del Tratado de Utrecht».

### 2.2 Claim mới G003 (`g1/claims-g1.json`; kiểm độc lập `khoa-loi/verify_g003.py`: 4/4 khớp tệp thô, đúng SHA)
**claim_en:** Gibraltar's new constitution was promulgated on 23 May 1969; sixteen days later (8 June 1969) Spain closed the frontier. A Spanish historian describes the closure as the culmination of an escalation over Gibraltar's constitutional change and self-determination, in which Madrid applied the terms of the Treaty of Utrecht strictly. · **XÁC MINH** · nhạy cảm TRUNG.

| # | Nguồn | Phía | Trích nguyên văn | SHA-256 tệp |
|---|---|---|---|---|
| chính | HM Government of Gibraltar, *50 Years — Closure of the Border 1969–2019* (sách kỷ niệm), ch. 6 "Spain closes the frontier" — https://www.gibraltar.gov.gi/uploads/Closure%20Booklet1.pdf | Gibraltar | "Gibraltar's new Constitution was promulgated on 23rd May 1969. Sixteen days later Spain closed the frontier." | `5caf6820…c843` |
| đối chiếu 1 | Rafael Sánchez Mantero (Univ. de Sevilla), "Desde el otro lado de la verja (los gibraltareños y el bloqueo de Gibraltar en 1969)", *Historia Contemporánea* 41 (2010): 373–390, tr. 377 — https://ojs.ehu.eus/index.php/HC/article/download/1336/948/3672 | TBN (học thuật) | «La actitud de Gran Bretaña, convocando un referendum en 1964 para cambiar la constitución gibraltareña y acelerar la autodeterminación de la colonia, marcaron una escalada del conflicto que culminó con la decisión del Gobierno de Madrid de cerrar la comunicación con el Peñón en 1969. En realidad, lo que hizo el Gobierno español fue aplicar estrictamente los terminos del Tratado de Utrecht.» | `80579430…40ab` |
| đối chiếu 2 | Concha Langa Nuño (Univ. de Sevilla), "A través del espejo: la imagen de los gibraltareños a este lado de la frontera", *Historia Contemporánea* 41 (2010): 391–412 — https://ojs.ehu.eus/index.php/HC/article/download/1338/950/3674 | TBN (học thuật) | «El segundo periodo es el inmediatamente posterior al cierre de la verja, el domingo 8 de junio de 1969.» (cùng bài: «se hizo pública en mayo de 1969 la Constitución») | `383f723c…d73d` |
| đối chiếu 3 | Luis María Manglano Tirado (UNED), "Gibraltar al final de la Transición: la agenda británica", *Aportes* nº117 (1/2025): 169–198, chú thích 4 (dịch lời mở đầu Gibraltar Constitution Order 1969) — https://www.revistaaportes.com/index.php/aportes/article/download/885/475/2475 | TBN (học thuật) | «el Gobierno de Su Majestad nunca concederá acuerdo alguno en virtud del cual el pueblo gibraltareño pase a depender de la soberanía de otro Estado contra su voluntad libre y democráticamente expresada» | `89d34a40…dfcfc` |
- Tệp thô nằm ngoài git ở `/var/tmp/cine-out/t3-k41/raw/`. Không tải được: trang Bộ Ngoại giao Tây Ban Nha (exteriores.gob.es, lỗi 503 hai lần); Hansard 9/6/1969 và báo cáo Uỷ ban Đối ngoại 2008 (publications.parliament.uk, lỗi 403). Không dùng Wikipedia.
- Lệch ngày: 8/6 (HMGoG, Langa Nuño) và 9/6 (ngày rút 4 666 lao động, C19 / HMGoG political-development). Lời chỉ nói "June 1969", nên không cần chọn.
- Sách HMGoG là nguồn chính thức của một phía (lời tựa viết "the Spanish dictator"), nên chỉ dùng cho mốc thời gian.

## 3. Thời lượng (`khoa-loi/fit_khoa.py` với `LOI=script-v4.1-KHOA.md`, rồi `khoa-loi/rut_41.py`)
| Bước | Đổi | Tổng |
|---|---|---|
| v4 đã duyệt (LK1) | — | 718,0 s |
| đặt theo lời v4.1 (luật G1) | 5a 9 → 14 s (lời 13,2 s); SM3/4g giữ 8 + 5,5 s | 723,0 s |
| rút tấm im lặng (sàn 8 s) | KB1943 9 → 8 · KA2026 9 → 8 | 721,0 s |
| rút thẻ số về đúng lời + 0,4 s (bậc 1 khung hình, 24 fps) | 1f 6,0 → 5,625 · 2d 8,0 → 7,625 · 5e 7,0 → 6,417 | **719,667 s** |
- Theo chương: Móc 44,5 · 1: 122,1 · 2: 203,6 · 3: 84,5 · 4: 110,5 · 5: 154,4 s. Mốc đinh, cú liên hoàn và khung neo không đổi. Giá trị trước khi rút lưu ở trường `dur_truoc_rut`, giá trị G1 ở `dur_g1` (`vay-ham/treatment.json`); nhật ký ở `khoa-loi/dur-khoa.json` và `khoa-loi/rut-41.json`.
- `tu_kiem.py` **ĐẠT**: Q26b 8 loại/36,5 % · 6 loại/43,6 %; NC-H2 1 × 2,5 s; NC-H3 99,4/92,5 %; strategic 3,06 %; khung neo 6; ai_image 7,0 %; im lặng 2 × 8 s; footage 1,1 %; 0 shot thiếu claim.
- `kiem_loi.py`: 0 lỗi; bộ lọc CS bắt 8 câu như v4 (câu mới không bị bắt); `g1/kiem-chu.{json,md}` sinh lại trên v4.1.
- Theo nhịp Eric đo thật ở T2, lời ≈ 630 s; ước 2,5 từ/s cho 668 s.

## 4. SHA (`LOI-KHOA.sha256`; dòng "# cũ" = bản v4 @9cca02f0; kiểm bằng `sha256sum -c LOI-KHOA.sha256`, 3/3 OK)
| Tệp | Cũ (v4) | Mới (v4.1) |
|---|---|---|
| lời khoá có mã | `script-v4-KHOA.md` `1d3a2454a7ea100d525a85da7b4a6abb3cd3b35926ccdd1e280d29c12ef80ec1` | `script-v4.1-KHOA.md` `7e0cdc0b218cdcd3fee6d091f1bff9fbef261de5c812d5653b9ce8ed0dbe5a34` |
| `loi-khoa.txt` | `a03265c036111b275c1efa8167c2438179a335fcd63748c4918a72e928be550f` | **`0fdc72ce81e33b6f4efc8234a52dafc5410d4448c26c0a0feb3eb01abaa71753`** |
| `khoa-loi/phat-am/gibraltar-eric.pls` | `3a70a020…0f24` | không đổi |
`loi-khoa.txt`: 1 571 từ viết, **9 195 ký tự** (+105). `script-v4-KHOA.md` vẫn giữ trong repo để đối chiếu.

## 5. Chi phí thật
| Mục | Trần | Thật |
|---|---|---|
| Claude API | ≤ $1 | **$0** (không gọi `claude -p`; không kiểm mù lại vì lệnh chỉ giao hai sửa cụ thể) |
| ElevenLabs · YouTube | 0 · 0 | **0 · 0** |
| Giờ máy | ≤ 0,5 h | **≈ 0,2 h** (tải 8 tệp ≈ 12,5 MB, gồm sách HMGoG 12 MB; script < 2 s/lần) |
Dòng đề xuất `COST-LEDGER`: `T3-KHOA-LOI-41 | 18/10/2026 | API $0 | YT 0 | EL 0 | máy ≈ 0,2 h | nhánh claude/k2c-t3-loi-khoa-al1itg`.

## 6. Việc chờ chủ dự án
1. **Tấm im lặng KA2026 có 1,4 s lời 5j đè lên** (lỗi có từ v4). Chọn một trong ba: (a) cho 5j dài thêm 1,5 s, tổng ≈ 721,2 s (vượt trần 12 phút 0,17 %); (b) nới trần thẻ 5i 8 → 10,5 s (tổng ≈ 722,2 s); (c) xử lý ở G1b bằng cách đặt lời/hình chồng (lời kết câu trên 0,5 s đầu của tấm) và chấp nhận phần im lặng thật còn ≈ 6,6 s.
2. Xác nhận SM3 dạng nhãn mốc "May 1940: … June: …" (§1) và câu LK3 13 từ (§2.1). Tuỳ chọn: thêm chữ trên hình "Constitution 23 May 1969 → frontier closed 8 June 1969" ở 5a (đã có claim G003).
3. G1b (animatic) chờ cổng hình V5b-2d + V6. LK4: "fourteen sieges" và thứ tự đoạn hầm 1782 sẽ xem lại ở G1b.
4. Trước khi thu giọng: nghe thử từ điển + ASR. Trước khi đăng: đọc lại C02, C26.
5. RIGHTS (P ghi): ba bài học thuật chỉ dùng làm nguồn kiểm chứng, không trích lên hình; sách HMGoG không lên hình.

**DỪNG — lời T3 v4.1 đã khoá.**
