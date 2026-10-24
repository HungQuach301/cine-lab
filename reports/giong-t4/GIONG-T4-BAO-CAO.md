**Nhánh thật: `claude/k2c-t4-02-giong-a24udn`** (harness buộc tên này; lệnh ghi `k2c-t4-02-giong`). Gốc `origin/main` @ `c6a4772b`. Đã đẩy, **không merge**.

# GIONG-T4 — K2C-T4-02 London, mốc M2: khoá lời + thu G1 cả tập + mốc câu — DỪNG chờ chủ dự án

> Phiên GIONG-T4, 23/10/2026 23:45 → 24/10/2026 ≈ 01:00 UTC. Chạy song song P-2410 và K-1.17.5; không đụng vùng của họ.
> **Vùng sửa (đúng lệnh):** `channel-k2/k2c-t4-02/{loi-khoa.txt, LOI-KHOA.sha256, khoa-loi/**, am-thanh/**}` (mới), `scripts/k2ldn/giong/**` (mới), `reports/giong-t4/**`. Không sửa `LOI-NHAP-v1.md`, `BANG-SHOT-v1.*`, `TREATMENT.md`, `look/`, `ai/`, `checks/`, `docs/`, sổ, `tools/`, `channel-k2/k2c-t3-01/**` (chỉ đọc làm mẫu), `main`, nhánh khác.
> **Đã đọc:** `reports/m3/BAI-HOC-LL.md` (toàn văn); `reports/kl42/KL42-BAO-CAO.md`; `reports/tien-ky-t4/PHIEU-G1.md`, `DU-KIEN-MOI.md`; `AUTHORSHIP.md` dòng 397 (G1 T4); Kinh thánh §3, §4 dòng âm thanh, §12, §14, §17, §19; `LOI-NHAP-v1.md`, `BANG-SHOT-v1.md`, `TREATMENT.md`; công cụ KL42 + `khoa-loi/` T3.
> **Môi trường:** `verify.sh` 10 ĐẠT, 5 TRƯỢT (OpenEXR, three.js, tifffile/pyshp, k2v node_modules, Freesound — phiên không dùng).

## Khối điều lệ
| Trường | Lệnh | Thực tế |
|---|---|---|
| Preflight | `set -o pipefail`; chỉ commit khi "— ĐẠT" | hook `pre-commit` + `pre-push` cài trước lần đẩy đầu. Mọi commit/đẩy: **PREFLIGHT ĐẠT**, `lock.py --verify` **KHỚP**. Lần commit đầu bị **CHẶN P1** (email trong trang nguồn đã tải) → che email trong công cụ + tệp, rồi mới commit (§7) |
| Force/amend | cấm | không force-push, không amend |
| Email/khoá | che; UA CineLab | không email trong tệp/header/URL/payload (preflight P1 ĐẠT); UA `CineLab-research (+https://github.com/HungQuach301/cine-lab)` cho mọi lệnh curl/ElevenLabs; khoá do proxy gắn, không đọc/in |
| Tiến trình nền | theo PGID, P ≤ 2, RAM ≥ 5 GB | thu (PID/PGID 6053) và ASR (7625) chạy riêng từng vòng; RAM trống 15 GB; đĩa còn 12 GB |
| Đẩy | ≤ 30 phút + CHECKPOINT | 7 lần đẩy, mỗi lần cách nhau ≤ 30 phút; `CHECKPOINT.md` có mục "Trạng thái" + "Lệnh bổ sung đã áp" |
| Tệp tốn tiền | ≤ 5 MB vào git ≤ 10 phút | 13 mp3 gốc ElevenLabs + alignment (mỗi tệp < 5 MB, tổng 20,4 MB) vào `am-thanh/nguon/`. **Lệch:** chương 00 (về 00:16) và 01 p0 (00:19) chỉ vào git lúc 00:28 (≈ 12 và 9 phút) vì phiên chờ cả lượt thu xong (§7) |
| Sổ AI | mọi lệnh gọi | `reports/giong-t4/so-ai.jsonl`: 13 lệnh, mỗi lệnh có model, giọng, thiết lập, seed, **chữ gửi nguyên văn**, ngữ cảnh, SHA vào/ra, ký tự, giá |
| Dừng hỏi | không | đúng |

---

## 0. Tóm tắt (đọc 2 phút)
1. **22 mục [cần kiểm] đã giải** (`KIEM-LOI.md`, trích dẫn **máy kiểm khớp nguyên văn** 22/22 nguồn đã lưu có SHA): **7 GIỮ · 12 SỬA CHỮ · 2 BỎ VẾ · 1 VIẾT LẠI AN TOÀN**; không mục nào bỏ cả câu, không thêm khẳng định ngoài nguồn. **D3 = GIỮ** "burned to the ground twice" (AUTHORSHIP dòng 397: chủ dự án bác đề xuất làm mềm). Móc Pepys giữ, nay trích **nguyên văn** "a little ale-house on the Bankside"; câu Bludworth giữ bản Pepys (không "piss it out").
2. **Lời khoá v2:** `loi-khoa.txt` **`645c0211…`**, 50 đoạn = 50 shot có lời, **1 553 từ** (nháp 1 593, −40), 8 668 ký tự. `LOI-KHOA.sha256` 3/3 OK (kịch bản `loi-v2-KHOA.md` `b9ad8147…`, PLS `london-g1.pls` `6e11cae0…`).
3. **Phát âm:** thử 48 tên (44 có trong lời + 4 ngoài lời theo lệnh) × 3 lượt (2 061 ký tự), nghe bằng ASR 2 cách + **mô hình âm vị** (IPA). Chỉ **Evelyn** cần alias (`Eevlin`; G1 thô đọc "EV-ə-lin"). Pepys = /piːps/, Bludworth = /blʌdwɜːθ/, Southwark = /sʌðək/ — đúng không cần alias. Từ điển 22 mục (21 năm/thập niên + Evelyn).
4. **Thu G1 cả tập:** 6 chương, 8 lệnh, seed 19102026, speed 1,03 → **ASR toàn tập 210 mục: 209 ĐÚNG, 1 NGHI (St Saviour's — âm vị đúng, ASR M viết "Xavier's"), 0 SAI**. Thu lại **1 câu**: G1 đã rút "I am spent" thành "I'm spent" (trái nguyên văn Pepys) → bản thu lại đúng ở cả 2 cách nghe, khớp mức +3,42 dB.
5. **Master:** **−14,1 LUFS, −1,5 dBTP**, LRA 3,2 LU, 680,760 s; WAV `b9cec467…`, FLAC `e5d49871…`; **tái tạo bit-trùng** từ tệp gốc trong git (`tai_tao.sh`, 0 ký tự, đã chạy: OK/OK). 3 bản nghe MP3 (3,21 / 2,71 / 2,24 MB; −14,2 LUFS; −1,5/−1,5/−1,6 dBTP). Mốc câu: `am-thanh/master/T4-loi-moc.json`.
6. **Thời lượng — điểm phải chủ dự án quyết (PHIẾU G-1):** lời theo shot thật **632,8 s** (G1 2,45 từ/s — đúng ước). Giữ đủ lời thì phim ≥ **782 s (+8,6 %)**; đề xuất **K1-C1 = 730,1 s (+1,4 %)**: bỏ 7 câu nguyên trong dựng (0 ký tự) + rút shot nối/lặng.
7. **Ký tự ElevenLabs:** **11 362 gửi** (mốc 14 000: 81 %; chặn 18 000: 63 %). Bộ đếm **150 839 → 155 837 (+4 998 = 0,440/ký tự gửi)**. Claude API $0; OpenAI/Gemini/RunPod/YouTube 0; giờ máy ≈ 1,2 h.
8. **Chờ chủ dự án:** PHIẾU G-1 (thời lượng), G-2 (vế bỏ), G-3 (tên cần tai người); nghe 3 bản nghe. **Lưu ý quyền:** giọng G1 vẫn "chờ thư Đ5" (RIGHTS P1910-G1) — bản thu dùng cho animatic/nội bộ, chưa phát hành.

**Chỉ số trong ±5 % quanh ngưỡng (nêu tên):**
| Chỉ số | Đo | Ngưỡng | Lệch |
|---|---|---|---|
| Phim K1-C1 (đề xuất) | 730,1 s | mục tiêu 720 s; Đ2 ≤ +5 % | **+1,4 %** |
| Phim K1-C | 752,5 s | ≤ 756 s (720 + 5 %) | **+4,5 %** (cách trần 0,5 %) |
| Loudness master | −14,1 LUFS | dải −15,0…−13,8 | cách cận trên 0,3 LU (2,2 %) |
| Loudness 3 bản nghe | −14,2 LUFS | dải −15,0…−13,8 | cách cận trên 0,4 LU (2,9 %) |
| ASR tên/số | khớp mờ ≥ 0,75 | 0,75 | bộ kiểm KL42 không lưu điểm từng mục đạt; mục NGHI duy nhất: St Saviour's (§4) |

Ngoài dải nhưng nêu để rõ: số từ 1 553 thấp hơn khung nháp 1 650–1 800 **5,9 %** (đã vượt ±5 %; độ dài phim thật lại vượt — xem G-1).

---

## 1. Việc 1 — giải 22 mục [cần kiểm] (`KIEM-LOI.md`)
- **Cách làm:** tải từng trang nguồn bằng `scripts/k2ldn/giong/tai_nguon.py` (UA CineLab) → bản chữ `reports/giong-t4/nguon/<mã>.txt` (dòng đầu: URL, giờ đọc UTC, **SHA-256 tệp gốc**, cỡ; email đã che). Gốc HTML/PDF ngoài git (`/var/tmp/cine-out/giong-t4/nguon/`), tái tạo bằng lệnh trên (trang có thể đổi → so SHA).
- `kiem_loi_md.py` sinh bảng từ `kiem-loi.json` và **dừng nếu bất kỳ trích dẫn nào không khớp nguyên văn** tệp nguồn → 22/22 khớp.
- **Nguồn (22 tệp):** London Museum (2), Library of Congress, Vetusta Monumenta (Univ. Missouri), Oxford (I. Archer), Inner Temple Library, City of London (Protected Views SPD 2012, Great Fire walk, City Cluster 2021, Who we are, Key facts, Guildhall), St Paul's Cathedral (timeline, St Paul's Watch), The Royal Exchange, LMA/AIM25 (Bridge House Estates), M. Cooper (FIG 2000), BBC 2010, Brewers' Company 2020, RMG; cộng Pepys/Evelyn trong repo (bậc 2).
- **Không mở được** (ghi để phiên sau khỏi thử): ICE (403), BBC qua WebFetch (dùng curl được), historyrevealed (503), Londonist (403), bho Old & New London (404 đường dẫn đoán — BAI-HOC #12: không đoán lần 2).
- **D1–D18:** chỉ D3 chạm lời (GIỮ — ghi V01). D10, D12–D15 là việc hình/tư liệu, không đổi lời; D12 (Doornick, bỏ Leake) và D13 (Ogilby không lên hình) được áp vào chữ nháp thẻ phương pháp.

## 2. Việc 2 — lời khoá
- **Công cụ:** `scripts/k2ldn/giong/lam_loi_khoa.py` đọc `LOI-NHAP-v1.md` + `khoa-loi/sua-v2.json` (27 mục V01–V27) + `khoa-loi/doan-shot.json` (gán 86 câu → 50 shot theo nội dung). Kiểm bằng mã: câu không có trong sửa phải **giữ nguyên chữ nháp**; đủ L01–L86, đúng thứ tự, mỗi câu một lần.
- **Sinh:** `loi-khoa.txt` (khuôn T3: `[NN NAME]`, mỗi shot một đoạn), `khoa-loi/loi-v2-KHOA.md` (có mã shot + {Lnn ✎}), `khoa-loi/so-nhap-khoa.json` (86 dòng nháp ↔ khoá), `LOI-KHOA.sha256`.

**Bảng nháp ↔ khoá (câu đổi):**
| Mã | L | Loại | Lý do (rút gọn; đầy đủ ở `sua-v2.json`/`KIEM-LOI.md`) |
|---|---|---|---|
| V01 | L04 | cần kiểm → GIỮ | D3 chủ dự án |
| V02 | L13 | câu chữ | "He hurries…" không có chủ ngữ → "Samuel Pepys hurries…" |
| V03 | L14 | câu chữ | "Samuel Pepys finds him" → "Pepys finds him" (tránh lặp) |
| V04 | L18 | móc Pepys | trích nguyên văn "a little ale-house on the Bankside" |
| V05 | L22 | tách đoạn | 2 câu → 2 shot M-d (chữ giữ) |
| V06 | L25 | tách đoạn | câu chì chảy → shot M-d (5) (chữ giữ) |
| V07 | L39 | SỬA | "an owner, a tenant, a lease" → "its owners"; "cannot afford to wait" |
| V08 | L45 | SỬA | "set out the ground" → "stake out the widened streets, then the old foundations" |
| V09 | L52 | SỬA | 1758 / by 1831 (LMA) thay "by 1761 / seventy years later" |
| V10 | L53 | BỎ VẾ | bỏ "painters…", bỏ "white" |
| V11 | L54 | VIẾT LẠI | "…building by building" |
| V12 | L56 | SỬA | theo SPD §2.4 (Building Act 1930, toà cao che tầm nhìn) |
| V13 | L57 | GIỮ | London Museum + LoC |
| V14 | L58 | SỬA | "from the Thames bridges and the south bank" (SPD §2.8) |
| V15 | L61 | SỬA | "As dusk falls"; "at least a hundred thousand" |
| V16 | L63 | SỬA | "Many offices are locked and unattended." |
| V17 | L64 | GIỮ | BBC + Brewers' Company |
| V18 | L66 | GIỮ | St Paul's + London Museum |
| V19 | L67 | SỬA | "nineteen churches are destroyed" (London Museum + Brewers') |
| V20 | L69 | GIỮ | St Paul's + BBC |
| V21 | L71 | SỬA | "a great stretch of the City lies in ruins" |
| V22 | L76 | BỎ VẾ | "Slowly, the gaps fill again." |
| V23 | L77 | SỬA SỐ | "more than six hundred thousand … the Square Mile" (ONS 2022: 614 500) |
| V24 | L78 | SỬA | "in this century" |
| V25 | L81 | SỬA | "Greenwich Park"; "must also respect protected views" |
| V26 | L21 | GIỮ | Royal Exchange "original trading floor" |
| V27 | L36 | GIỮ | Wren trình Vua 11/9/1666; Evelyn 13/9 |

**Số từ và thời lượng ở speed 1,03:**
| Đo | Giá trị |
|---|---|
| Số từ | 1 593 (nháp) → **1 553** (khoá); 8 668 ký tự lời; 9 061 ký tự gửi sau alias |
| Ước trước khi thu (tốc độ KL42 2,35 từ/s khi nói) | lời theo shot ≈ 660,9 s |
| **Thật** | lời theo shot **632,8 s** (2,45 từ/s); lời liền trong chương 670,8 s; stem 680,8 s |
| So mục tiêu 720 s | lời 632,8 s chiếm 87,9 % — nhưng bảng v1 có 138 s shot không lời → phim ≥ 782 s nếu giữ đủ lời (**lệch > 5 % → PHIẾU G-1**) |

**Thẻ "How this film was made":** chữ NHÁP ở `khoa-loi/the-phuong-phap-NHAP.md` (2 thẻ, 26 và 21 từ, không nhắc AI theo §14.1 c, f), chưa khoá, không đọc thành lời.

## 3. Việc 3 — phát âm (`phat_am_thu.py`, `am_vi.py`, `reports/giong-t4/phat-am/l1–l3.json`)
- **Cách nghe:** mỗi tên trong một câu mang ngắn; cắt đúng khoảng tên theo alignment ký tự của ElevenLabs → (a) ASR M = medium.en beam 5, S = small.en beam 1 (như KL42), (b) **nhận dạng âm vị** `facebook/wav2vec2-lv-60-espeak-cv-ft` (venv riêng `/var/tmp/cine-out/giong-t4/venv-am-vi`, torch 2.5.1 CPU, không đụng `/opt/cine` — ghim D17). Lý do thêm (b): ASR chữ hay tự sửa về chính tả ("Pepys" đọc sai vẫn có thể viết "Pepys").
- **Bản nghe thử (trong git):** `khoa-loi/phat-am/nghe-l1.mp3` (48 tên), `nghe-l2.mp3` (Evelyn, Wenceslaus, Southwark + alias), `nghe-l3.mp3` (Wenceslas/Holler).

| Tên | Âm vị G1 đọc | ASR M / S | Kết luận |
|---|---|---|---|
| Pepys | p iː p s | Peeps / Peeps | ĐÚNG, không alias |
| Bludworth | b l ʌ d w ɜː θ | Bloodworth ×2 | ĐÚNG (Bloodworth = cách viết khác, cùng âm) |
| Farriner | f æ ɹ ə n ɚ | Fariner ×2 | ĐÚNG |
| Southwark | s ʌ ð ɚ k (l2) | Southwark / Sothek | ĐÚNG, không alias ("Suthuk" kém hơn) |
| **Evelyn** | thô: ɛ v ə l ɪ n (3 âm tiết) → alias **`Eevlin`**: iː v l e n | Evelyn ×2 (cả khi alias) | **alias `Eevlin`** (xin duyệt, G-3) |
| Wenceslaus | w ɛ n s ɪ z l aʊ s ("-louse") | Wenceslaus ×2 | giữ (G-3); alias "Wenseslaws"/"Wenceslas" không ra /lɔːs/ |
| Hollar | h ɔ l ə | Holler ×2 | ĐÚNG, không alias |
| St Saviour's, Old St Paul's, St Magnus, St George's | s eɪ n t … | đúng | "St" đọc "Saint" ✓ |
| Leadenhall, Guildhall, Greenwich, Gracechurch, Cripplegate, Bishopsgate, Paternoster, Clifford's Inn, Ludgate, Moorfields, Holden, Holford, Barbon, Barbican, Highgate, Whitehall, Thames, Parmesan, Richmond, King Henry's Mound, Parliament/Primrose Hill | khớp IPA Anh–Anh (điểm 0,78–1,00) | đúng | không alias |
| Ngoài lời: Cheapside, Doornick, Blitz, 30 St Mary Axe | tʃiːpsaɪd · d oː n ɪ k · b l ɪ s · s ə n t m ɛ ɹ i æ k s | đúng (M: "St Mary Acts") | dùng được nếu sau này vào lời |

Từ điển T4 (`khoa-loi/phat-am/tu-dien.json`, `london-g1.pls`): 21 năm/thập niên (kiểu Anh, gạch nối như T3: "sixteen sixty-six", "seventeen oh-eight", "mid-nineteen sixties") + Evelyn. Mã chặn alias VIẾT HOA (Đ3/GC-C).

## 4. Việc 4 — thu G1 cả tập (`gl_thu.py`, `gl_ghep.py`, `gl_kiem_tap.py`, `gl_thu_lai.py`, `gl_xuat.py`)
**Cách thu (như KL42):** G1 `VDLncRBHDjLHBqLhQ1Qt`, `eleven_multilingual_v2`, stability 0,5, similarity 0,75, speed 1,03, seed 19102026, `/with-timestamps`, `mp3_44100_192`; phần ≤ 1 900 ký tự ở ranh giới đoạn; `previous_text`/`next_text` ≤ 900 ký tự; nối bằng trung vị ngừng tự nhiên; không kéo nhịp.

| Chương | Lệnh (ký tự) | Lời liền (s) | Ngừng nối | ASR từ đúng M / S | Mục ĐÚNG/NGHI/SAI |
|---|---|---|---|---|---|
| 00 HOOK | 580 | 43,00 | — | 0,991 / 0,991 | 11 / 0 / 0 |
| 01 FIRE | 1 804 + 1 192 | 221,71 | 0,73 s | 0,983 / 0,970 | 66 / 1 / 0 |
| 02 REBUILD | 1 822 + 285 | 159,17 | 0,86 s | 0,995 / 0,981 | 51 / 0 / 0 |
| 03 DOME | 896 | 62,97 | — | 1,000 / 1,000 | 20 / 0 / 0 |
| 04 BLITZ | 1 021 | 74,86 | — | 0,983 / 0,972 | 22 / 0 / 0 |
| 05 TODAY | 1 461 | 109,04 | — | 0,996 / 0,996 | 39 / 0 / 0 |
| **Tổng** | 8 lệnh, **9 061** | **670,76** | | | **209 / 1 / 0** |

**Rà từng chỗ lệch cấp từ** (không chỉ mục tên/số):
- **Lỗi thật, đã sửa:** "I am spent" → G1 đọc "**I'm** spent" (âm vị aɪ m s p ɛ n t; M và S cùng "I'm"). Trái nguyên văn Pepys. **Thu lại 1 lượt** (seed 19102027, 11 ký tự + ngữ cảnh): âm vị aɪ æ m s p ɛ n t, M+S "I am spent." Bản thu lại nhỏ hơn câu gốc 3,4 dB → `gl_ghep.py` thêm khớp mức theo mức tiếng nói của câu bị thay (**+3,42 dB**, giới hạn ±6 dB). Kiểm lại chương 01: hết "I'm".
- **NGHI giữ nguyên:** St Saviour's (H1-03): âm vị bản gốc s eɪ n t s eɪ v j ɚ z (đúng); M "Xavier's", S đúng. Thu lại 1 lượt (seed 19102027, 229 ký tự): **cả M và S** "Xavier's" → **không dùng**, giữ bản gốc. Còn 1 lượt thu lại theo trần ≤ 2/câu — không dùng vì lỗi do ASR (PHIẾU G-3).
- **Không phải lỗi đọc** (âm vị kiểm): "Thames" → M "James" (âm vị t ɛ m z ✓, S đúng); "Paul's stood" → "Paul stood" (âm /z/ nối vào /st/, âm vị p oʊ l s t ʊ); "Moorfields" → "more fields"; "storeys" → "stories"; "kilometre" → "kilometer"; "ninth" → "nineth".

## 5. Việc 4 (tiếp) — master, mốc câu, bản nghe
| Tệp | I (LUFS) | TP (dBTP) | LRA | Thời lượng | SHA-256 | Nơi |
|---|---|---|---|---|---|---|
| Stem thô | −18,8 | −1,2 | | 680,760 s | `xuat.json` | ngoài git |
| **Master WAV** 48 kHz/24-bit mono | **−14,1** | **−1,5** | 3,2 | 680,760 s | `b9cec46777a02085561f0cdcfc858e5e8890d26382bd24b4bb8a6bcdb810200b` | ngoài git `/var/tmp/cine-out/giong-t4/xuat/` |
| **Master FLAC** | −14,1 | −1,5 | 3,2 | | `e5d49871807109760622d03da7d77884b349fb913cb2aa6c5af48c5f8bacf273` | ngoài git |
| Mốc câu/đoạn/chương | | | | | `7462507710439ad8884515330f29ace85d74f7e29ed8d29a0cdbb76b5e5323fe` | **git** `am-thanh/master/T4-loi-moc.json` |
| Bản nghe 1 (ch 00–01), MP3 96 kb/s | −14,2 | −1,5 | | 0 → 267,7 s | `cdc770d6…` | **git** `am-thanh/nghe/T4-loi-G1-v2-xem-1-ch00-01.mp3` (3,21 MB) |
| Bản nghe 2 (ch 02–03) | −14,2 | −1,5 | | 267,7 → 493,9 s | `17a9def7…` | **git** `…-xem-2-ch02-03.mp3` (2,71 MB) |
| Bản nghe 3 (ch 04–05) | −14,2 | −1,6 | | 493,9 → 680,8 s | `1e9d6af0…` | **git** `…-xem-3-ch04-05.mp3` (2,24 MB) |

- Chuẩn: khuếch đại tuyến tính + `alimiter` trên tín hiệu nâng mẫu ×4, `level=false` (BAI-HOC #121), trần −1,5 dBFS; bản nghe đo trên chính MP3 (BAI-HOC #69). Không nén/EQ.
- **Lưu bền (BAI-HOC #117, Kinh thánh §14.6):** master phải vào LFS, nhưng `tools/lfs-allow.txt` chỉ cho `channel-k2/k2c-t3-01/am-thanh/master/*` và `tools/` ngoài vùng sửa của phiên → **không tự thêm**. Thay vào đó: **13 mp3 gốc + alignment vào git** (`am-thanh/nguon/`, SHA256SUMS) và `scripts/k2ldn/giong/tai_tao.sh` **tái tạo master bit-trùng, 0 ký tự** — đã chạy: `T4-loi-G1-v2-14LUFS.wav: OK`, `.flac: OK`. Đề xuất phiên P thêm mẫu `channel-k2/k2c-t4-02/am-thanh/master/*` vào `tools/lfs-allow.txt` (cần chủ dự án duyệt) và đưa master vào LFS.
- Mốc câu (`T4-loi-moc.json`): mỗi chương → đoạn (shot) → câu: `bd`/`kt` trong chương và trong stem; câu thu lại có `thu_lai` (seed, tệp).

## 6. Việc 5 — bảng giãn shot (`GIAN-SHOT.md`, `gian-shot.json`)
Tóm tắt ở §0 mục 6 và PHIẾU G-1. Ngoài phương án thời lượng, animatic cần áp: đổi chỗ H1-11 ↔ H1-12; cột "Lời" v1 lệch ±1 câu ở Hồi 1 và Hồi 4 (gán lại theo nội dung); 3 M-d > 8 s (H1-01, H1-05, H1-17); thẻ Pepys sang H1-05; H3-02 năm 1758; H5-05 nên tách 2 cú máy.

## 7. Sự cố
| # | Sự cố | Hậu quả | Xử lý |
|---|---|---|---|
| 1 | Preflight CHẶN P1: email có sẵn trong trang nguồn đã tải (City of London, LMA, Oxford — 8 chỗ) | commit đầu không qua | `tai_nguon.py` che email trước khi ghi bản chữ (SHA vẫn của tệp gốc); che trong 5 tệp đã có; commit lại ĐẠT |
| 2 | `pkill -f` trong một lệnh dọn đã giết chính shell gọi (lặp BAI-HOC #24/#41/#112) | không mất dữ liệu (lượt thử 3 đã xong) | từ đó chỉ dừng/chờ theo PID ghi ra tệp (`thu.pid`, `kiem.pid`) |
| 3 | Tokenizer âm vị đòi `phonemizer`/`protobuf` | lượt thử 1 dừng ở bước âm vị (TTS đã về, cache → 0 ký tự thêm) | giải mã CTC bằng `vocab.json` của mô hình |
| 4 | Chương 00 và 01 p0 vào git sau ≈ 12 và 9 phút (lệnh: ≤ 10 phút) | không mất (cache ngoài git còn) | lần sau chạy `luu_nguon.py` sau mỗi chương, không chờ cả lượt |
| 5 | Bản nghe 1 (chương 00–02) 5,15 MB > 5 MB | — | chia 3 tệp theo chương |
| 6 | Bản thu lại "I am spent" nhỏ hơn 3,4 dB | chênh mức ở chỗ ghép | khớp mức theo mức tiếng nói câu bị thay (+3,42 dB) |

Không lỗi nào lặp ≥ 3 lần.

## 8. Ký tự ElevenLabs và chi phí
| Lượt | Ký tự gửi | Bộ đếm trước → sau | Tăng | Tỷ lệ |
|---|---|---|---|---|
| Thử phát âm l1 / l2 / l3 | 1 287 / 617 / 157 | 150 839 → 151 745 | 906 | 0,44 |
| Thu 6 chương (8 lệnh) | 9 061 | 151 745 → 155 731 | 3 986 | 0,44 |
| Thu lại 2 câu | 11 + 229 | 155 731 → 155 837 | 106 | 0,455 / 0,441 |
| **Tổng phiên (13 lệnh)** | **11 362** | **150 839 → 155 837** | **4 998** | **0,440** |

Giới hạn tài khoản 171 534 → **còn 15 697** (đặt lại theo `next_character_count_reset_unix` 1793516261 ≈ 01/11/2026). Không thêm/xoá/đổi giọng. Tái tạo master: 0 ký tự.

| Hạng mục | Mốc | Chặn | Thật |
|---|---|---|---|
| ElevenLabs (ký tự gửi) | 14 000 | 18 000 (cài thành mã trong `gl_lib.tts`) | **11 362** |
| Claude API | $2 | $6 | **$0** (không gọi `claude -p`; 0 subagent). Token phiên chính không đo được trong phiên → không tự khai |
| OpenAI / Gemini / RunPod / YouTube | 0 | | **0 / 0 / 0 / 0** |
| Giờ máy | 3 h | | **≈ 1,2 h** (ASR 2 cách nghe toàn tập + kiểm lại chương 01 ≈ 25 phút; âm vị; cài venv ≈ 3 phút) |
| Tải ngoài | | | PyPI (torch CPU 2.5.1, transformers 4.46.3) + Hugging Face (mô hình âm vị ≈ 1,2 GB, chỉ để đo, không vào phim) |

## 9. Dòng sổ đề xuất (phiên P ghi)
- **COST-LEDGER.csv:** `GIONG-T4,"K2C-T4-02 M2: khoá lời v2 (22 mục [cần kiểm]), phát âm, thu G1 cả tập, ASR, master, giãn shot",xưởng,2026-10-24,,,,,0,2,không gọi API,11362,4998,1.2,,0,680.76,,reports/giong-t4/GIONG-T4-BAO-CAO.md §8,"ElevenLabs 11 362 gửi / bộ đếm +4 998 (0,440); Claude API $0; OpenAI/Gemini/RunPod/YouTube 0"`
- **AUTHORSHIP.md (sau khi chủ dự án duyệt PHIẾU):** "K2C-T4-02 lời khoá v2 — D3 giữ; 22 mục [cần kiểm] theo KIEM-LOI.md; G-1 = <chọn>; G-2 = <chọn>; G-3 alias Evelyn 'Eevlin' = <chọn>" (đóng góp người: quyết định G-1…G-3; máy: kiểm nguồn, đề xuất câu).
- **RIGHTS.md:** không có tài sản mới (giọng G1 = dòng P1910-G1, **vẫn chờ thư Đ5**; mô hình âm vị chỉ dùng để đo).
- **BAI-HOC-K2:** (a) G1 có thể **rút gọn trong lời trích** ("I am" → "I'm") — luôn kiểm cấp từ trong câu trích nguyên văn, không chỉ mục tên/số; (b) nhận dạng âm vị (wav2vec2 espeak) là tai thứ hai tốt cho tên riêng; (c) bảng shot phải tính đủ ngừng giữa đoạn + shot không lời khi đặt độ dài lời.
- **tools/lfs-allow.txt (P, chủ dự án duyệt):** thêm `channel-k2/k2c-t4-02/am-thanh/master/*` để master T4 vào LFS (Kinh thánh §14.6).

## 10. Việc chờ chủ dự án
1. **PHIẾU G-1** — thời lượng: khuyến nghị (c) K1-C1 = 730,1 s (bỏ 7 câu nguyên trong dựng, 0 ký tự).
2. **PHIẾU G-2** — các vế bỏ/làm mềm của mục [cần kiểm]: khuyến nghị (a) duyệt như bản khoá.
3. **PHIẾU G-3** — tên cần tai người: St Saviour's, Wenceslaus; duyệt alias Evelyn "Eevlin".
4. **Nghe** 3 bản nghe (`channel-k2/k2c-t4-02/am-thanh/nghe/`, ≈ 11 phút 21 giây).
5. Việc của phiên P: merge nhánh (phiên này không merge); thêm mẫu LFS + đưa master T4 vào LFS; ghi sổ §9; chuyển `GIAN-SHOT.md` cho animatic.

## 11. Tệp
- **Lời:** `channel-k2/k2c-t4-02/loi-khoa.txt`, `LOI-KHOA.sha256`, `khoa-loi/{loi-v2-KHOA.md, sua-v2.json, doan-shot.json, so-nhap-khoa.json, the-phuong-phap-NHAP.md}`, `khoa-loi/phat-am/{tu-dien.json, ten-chon.json, london-g1.pls, loi-khoa.tts-preview.txt, nghe-l1..l3.mp3}`.
- **Âm thanh:** `am-thanh/nguon/` (13 mp3 gốc + alignment + SHA256SUMS), `am-thanh/master/{SHA256SUMS, T4-loi-moc.json}`, `am-thanh/nghe/` (3 MP3).
- **Báo cáo:** `reports/giong-t4/{GIONG-T4-BAO-CAO.md, KIEM-LOI.md, GIAN-SHOT.md, PHIEU-GIONG.md, CHECKPOINT.md}`; số đo `kiem-loi.json, kiem-tap.json, thay.json, xuat.json, gian-shot.json, phat-am/*.json, so-ai.jsonl, bo-dem.jsonl`; nguồn `nguon/*.txt` (22).
- **Công cụ:** `scripts/k2ldn/giong/{tai_nguon.py, kiem_loi_md.py, lam_loi_khoa.py, lam_tu_dien.py, gl_lib.py, phat_am_thu.py, am_vi.py, gl_thu.py, gl_ghep.py, gl_kiem_tap.py, gl_thu_lai.py, gl_xuat.py, luu_nguon.py, gl_gian_shot.py, tai_tao.sh}`.
