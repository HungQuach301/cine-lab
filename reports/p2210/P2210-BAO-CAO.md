Nhánh thật: **`claude/p-2210-merge-bible-update-9kpvi8`** (harness buộc; lệnh ghi `p-2210`). Tạo từ `origin/main` @`96b5017c`, đúng gốc lệnh. `main` được cập nhật bằng fast-forward lên đầu nhánh này.

# P-2210 — merge 3 nhánh đã rà vào main + ghi quyết định 21–22/10 vào Kinh thánh và sổ. BÁO CÁO. DỪNG chờ chủ dự án

## §0 Điều lệ phiên và tóm tắt
| Trường | Lệnh | Thực tế |
|---|---|---|
| Nhánh | `p-2210` từ origin/main @96b5017c | `claude/p-2210-merge-bible-update-9kpvi8` (harness buộc), gốc @96b5017c |
| Vùng sửa | docs/**, AUTHORSHIP.md, RIGHTS.md, COST-LEDGER.csv, channel-k2/BAI-HOC-K2.md, channel-k2/HANG-DOI.md, reports/p2210/**, main | đúng. Ngoài các merge, phiên không sửa `checks/`, `design/`, `scripts/`, `tools/`, `channel-k2/k2c-t3-01/**` hay nhánh khác |
| Đã đọc | BAI-HOC-LL; ANIM-V2 §5, §10–§12; SFX-T3 + de-xuat-RIGHTS; K1171; Kinh thánh §12.1, §14–§16; AUTHORSHIP 21/10 | đúng |
| Chi phí | không gọi API trả phí; giờ máy 2 h | API **$0** (0 lời gọi, 0 subagent); giờ máy ≈ **0,5 h** |
| Preflight | bắt buộc, `set -o pipefail`, chỉ commit khi dòng kết luận có "— ĐẠT" | chạy tay trước **mọi** commit qua một script nhỏ: `set -o pipefail` + chỉ commit khi có "— ĐẠT" và "PREFLIGHT ĐẠT". Mọi commit ĐẠT. `--range origin/main..HEAD` ĐẠT (§5) |
| Email | che; không đưa vào header/URL/payload/UA | 0 email chủ dự án trong diff và commit; 0 email khác trong dòng thêm; phiên không gửi yêu cầu mạng nào ngoài git |
| `lock.py` | chỉ `--verify` | chỉ `--verify` (mọi lần, kể cả trong preflight, đều KHỚP) |
| Force / amend | không force; không amend commit đã đẩy | 0 force. **1 lần amend commit CHƯA đẩy** (`774e2fcc` → `59b0972b`) để trả lại ký tự `\r` có sẵn ở cuối dòng P-2010b của COST-LEDGER, ký tự này bị bước ghi CSV bỏ mất. Commit này chưa từng lên remote |
| Dừng hỏi | không dừng giữa chừng | đúng |
| Môi trường | `verify.sh` | 11 PASS, 4 FAIL (OpenEXR, three.js, tifffile/pyshp, k2v node_modules). Phiên này không cần mục nào trong số đó |

**Tóm tắt**
1. **3 merge `--no-ff`, 0 xung đột.** LOCK 1.16.1 → **1.17.1 `b741f617…` KHỚP** từ sau merge (1). 8/8 bộ `selftest_k11*.py` đạt sau mỗi merge và ở lần kiểm cuối.
2. **Nhánh ANIMATIC-T3-V2 có thêm commit "cứu 4 video gốc Omni"**: SHA thật **`72e3f0fe`** (con của `18a5f33d`). 4 tệp 3,0–4,8 MB, `sha256sum -c` OK.
3. **Kinh thánh `14ca13aa…` → `ca1801e7…`**: §14.1 (c)(f), §14.7 (+4 dòng), §15 (e)(f)(i), thêm §17 và §18 (§2).
4. **Sổ:** AUTHORSHIP +6 dòng, RIGHTS +41 dòng (4 Omni + 37 SFX), BAI-HOC-K2 K18–K24, HANG-DOI mục 22/10, COST-LEDGER +5 dòng (§3).
5. **main `96b5017c` → đầu nhánh này** (fast-forward, main cũ là tổ tiên, không force) (§6).

## §1 Merge
| # | Nhánh @SHA | Commit merge | Số tệp | Vùng | LOCK sau merge | selftest k11* |
|---|---|---|---|---|---|---|
| 1 | `origin/checks-1-17-1` @`39d01859` | `36205cf8` | 53 (+5 720 / −39) | checks/ (22), reports/k117 (19), reports/k1171 (12) | **1.17.1 `b741f617d7b2275e4039cd16eb8e967cbc99801f508090631146590bb1bc16fe` KHỚP** | 8/8 đạt |
| 2 | `origin/claude/laughing-ptolemy-u7xlwe` @`0a10d1fc` | `e7c88d70` | 80 (+45 086) | chỉ `reports/sfx-t3/**` (0 tệp ngoài vùng) | KHỚP | 8/8 đạt |
| 3 | `origin/k2c-t3-anim-v2` @**`72e3f0fe`** (sau `18a5f33d` có 1 commit "ANIMATIC-T3-V2: cứu 4 video gốc Omni 720p") | `132ea033` | 288 (+19 614 / −1 551) | reports/animatic-t3-v2 (269), scripts/k2tl (11), channel-k2/k2c-t3-01/animatic (6), design/k2v/tl (2) | KHỚP | 8/8 đạt |

- Trước khi merge (3), tôi đã chạy lại merge-tree với `72e3f0fe`: 0 xung đột. `18a5f33d` là tổ tiên của `72e3f0fe`.
- Kết quả selftest (dòng kết luận, giống nhau ở cả 4 lượt): k112 75/75 · k1121 48/48 · k1122 37/37 · k113 64/64 · k114 126/126 · k115 105/105 · k116 144/144 · k117 130/130.
- Merge (3) đưa `design/k2v/tl/*.js`, `scripts/k2tl/*` và `channel-k2/k2c-t3-01/animatic/*` của V2 vào `main` theo lệnh. Phiên BAN-CUOI-T3 làm ở vùng này nên cần lấy `main` mới. Phiên này không sửa thêm gì ở các vùng đó.
- LOI-KHOA 3/3 OK sau merge (3).

## §2 Kinh thánh `docs/BIBLE-KENH2.md`
- **SHA-256 trước:** `14ca13aaed89aade183caf73cc044393c223fb07e7a22bf0b3c56a43e1346429` (main @96b5017c).
- **SHA-256 sau:** `ca1801e78b0e47e3cbff2c754bc8cfc381d00810ed2482ffec3d3cdd72a6a6b8` (commit `318bbc9e`). Thay đổi: +21 dòng, −6 dòng. Diff đầy đủ ở `reports/p2210/bible-diff.txt`.
- Mỗi chuỗi gốc được kiểm là xuất hiện đúng 1 lần trước khi thay.

| Chỗ | Trước | Sau |
|---|---|---|
| Tiêu đề | "… §14.7 + §15 + §16 — 21/10/2026)" | "… §14.7 + §15 + §16 — 21/10/2026; sửa §14–§15 + §17 + §18 — 22/10/2026)" |
| §14.1 (c) | "…nhãn "Illustration" trên hình suốt đoạn (ngoại lệ của §12.1)." | "…không nhãn AI hay "Illustration" trên hình (chủ dự án 22/10/2026 11:09)." |
| §14.1 (f) | "Công bố: bật khai báo nội dung AI trên YouTube; mô tả §10.6 viết lại theo N1/N2 (đã viết lại, chủ dự án duyệt 20/10 22:34); giữ đo bình luận chê AI ≤ 2 % (§11.3)." | Chép nguyên văn lệnh: "Công bố: bật khai báo nội dung bị thay đổi/tổng hợp (altered or synthetic content) trên YouTube khi tập có khung AI giống thật hoặc giọng tổng hợp; mô tả YouTube ghi việc dùng AI theo §10.6; TRONG PHIM không có thẻ, nhãn hay câu nhắc AI (chủ dự án 22/10 11:09); giữ đo bình luận chê AI ≤ 2 %." |
| §14.7 | — | Thêm 4 dòng sau "Mở đầu tập…": R1 chấm bằng mắt (V2-D2); TL-1 được vượt khi cắt góc theo R3 (V2-D7); T3 eo đất 1809–1939 được thêm vật đời sống chung / hạ máy, cắt khung không cần nguồn mới, thẻ PP1 nêu "isthmus buildings" (V2-D8); màu ≥ 0,40 ở bước chỉnh màu bản cuối, khớp tông minh hoạ AI vào 3D (V2-D1). Mỗi dòng ghi "chủ dự án 22/10/2026 11:09" |
| §15 (e) | "…thẻ phương pháp + mô tả ghi "illustrative detail … from sources";…" | "…thẻ phương pháp KHÔNG nhắc AI (chủ dự án 22/10/2026 11:09); câu "illustrative detail … from sources" CHỈ ở mô tả YouTube;…" |
| §15 (f) | "…bộ đếm chạy tiếp, nhãn 'Illustration' suốt đoạn; khớp lớp (a)…" | "…bộ đếm chạy tiếp; khớp lớp (a)…" |
| §15 (i) | "…được dùng minh hoạ AI có nhãn theo đúng nguyên tắc (f)…" | "…được dùng minh hoạ AI theo đúng nguyên tắc (f)…" |
| §17 (mới) | — | "Lớp thông tin chồng cảnh (áp từ T4; chủ dự án duyệt 22/10/2026 07:24, nguyên văn …; T3 không áp)". Là ngoại lệ có giới hạn của §12.1; cùng lúc ≤ 2 lớp. Gồm (1) bản đồ bối cảnh, (2) tư liệu thật chồng cảnh, (3) thẻ nhân vật + bộ đếm số liệu, giới hạn đúng như lệnh |
| §18 (mới) | — | "Định vị kênh (chủ dự án 22/10/2026)": 07:04 hướng T3, series "Contested Places", bỏ Steel; 07:07 Steel không công khai; §1–§9 chỉ còn giá trị lịch sử, chỗ trái thì §18 thắng |

**Mâu thuẫn còn lại (lệnh không yêu cầu sửa, nên tôi chưa sửa):**
- §12.1 (b) vẫn mô tả thẻ "How this film was made" có nêu "AI dùng vào việc gì".
- Điều này trái với §14.1 (f) và §15 (e) mới ("trong phim không có thẻ, nhãn hay câu nhắc AI"; "thẻ phương pháp không nhắc AI").
- §12.1 là luật cũ hơn nên §14.1 thắng, nhưng chữ vẫn còn trong Kinh thánh. Đề xuất ở §8.

## §3 Sổ (dòng thêm)
**AUTHORSHIP.md (+6 dòng, cùng dạng bảng các dòng 21/10, mỗi dòng ghi "P-2210 ghi"):**
- 22/10 07:04: định vị kênh.
- 22/10 07:07: video Steel không công khai.
- 22/10 07:19: xương sống T4 London, kèm yêu cầu bản đồ tổng thể và tư liệu thật.
- 22/10 07:24: luật lớp thông tin chồng cảnh, phương án A (chỉ từ T4).
- 22/10 08:23: nghe mù SFX. Điều phối chọn bản có SFX "tối giản dưới lời" và giữ 4 tiếng.
- 22/10 11:09: V2-D1…D8 kèm 2 điều chỉnh. Lời chủ dự án chép nguyên văn, giữ cả lỗi gõ và chú giải.

Dòng 21/10 21:15 (Omni chọn A) đã có nên không ghi trùng.

**RIGHTS.md (+1 mục, 41 dòng tài sản):** mục "Kênh 2 — K2C-T3-01: minh hoạ Omni M2–M5 (ANIMATIC-T3-V2) + ứng viên SFX T3 (SFX-T3)".
- (a) `T3-AI-M2…M5`: model `gemini-omni-1.1-flash`.
  - Trích nguyên văn điều khoản Gemini API "Use of Generated Content", đã đọc ở NC-N2P/P-2110.
  - Ghi SHA vào/ra theo `reports/animatic-t3-v2/so-ai-gemini.jsonl`, kèm SHA bản nén 720p ở `omni/goc720/`.
  - Gốc có C2PA `trainedAlgorithmicMedia` + SynthID; bản nén/ghép mất C2PA.
  - Công bố theo §14.1 (f) mới: không nhãn trong phim.
- (b) "Ứng viên SFX T3", trạng thái **"ứng viên — bản cuối chốt danh sách dùng"**:
  - 35 dòng `K2-SFX-T3-01…35` chép nguyên từ `reports/sfx-t3/de-xuat-RIGHTS.md`. Chỉ đổi "(ngày P ghi)" thành 2026-10-22.
  - **+2 dòng P-2210 thêm**: `-36` HOAMAI-1 và `-37` CHIM-1. Đây là 2 tiếng ngoài gói mà chủ dự án giữ lúc 08:23, nên không có trong tệp đề xuất. Nguồn và SHA lấy từ `ung-vien.json` và `so-do/sha-goc.txt`. Giấy phép trích như dòng cùng nguồn (`-01` NPS, `-03` BigSoundBank).
  - **Lưu ý HOAMAI-1:** ứng viên cắt từ 2,65 s, còn chủ dự án giữ "phần sau 2,85 s". Dòng RIGHTS ghi rõ: bản cuối cắt lại từ 2,85 s và ghi SHA đoạn mới.
- (c) Nhãn "Illustration" dùng font DejaVu Sans của C4-F1, không có dòng RIGHTS riêng. Đã ghi chú "không dùng từ 22/10/2026" trong mục mới và không sửa dòng C4-F1.

**channel-k2/BAI-HOC-K2.md (+K18–K24, 7 dòng):**
- K18: không force, kể cả nhánh phiên; cài hook trước lần đẩy đầu.
- K19: `pipefail` + kiểm chữ "— ĐẠT".
- K20: dừng theo PGID, một vòng dựng một lúc.
- K21: P = 2 khi nướng.
- K22: đầu vào bước sau phải có bản nén ≤ 5 MB trong git, hoặc lệnh + SHA để tạo lại.
- K23: thước R2 bắt thiếu → mắt chủ dự án là chuẩn.
- K24: đổi góc phải giữ vật mà lời nhắc tới (C4, XEM CÂM Q4 4 → 2).

**channel-k2/HANG-DOI.md:** thêm mục "CẬP NHẬT 22/10/2026 (P-2210)" ở trên mục 21/10.
- T3 Gibraltar → bản cuối.
- T4 London: xương sống chủ dự án duyệt 07:19, logline nguyên văn, cấu trúc ≈ 12 phút gồm móc + 5 hồi (6/27/22/10/15/20 %), điểm máy Bankside.
- **Giữ nguyên 4 nhãn [cần kiểm].** Áp §15 và §17.

**COST-LEDGER.csv (+5 dòng, 20 cột, kiểm bằng `csv`):**

| Phiên | Claude API | Ghi chú | Giờ máy |
|---|---|---|---|
| K-1.17 (theo đề xuất K117 §8; chưa có trên main) | $0,291 | OpenAI $0,078 | 0,9 h |
| K-1.17.1 | $0 | — | 0,3 h |
| ANIMATIC-T3-V2 | ≈ $4,66 | Gemini $11,25; OpenAI $0,83. Đối chiếu sổ: Gemini $11,2461 · OpenAI $0,8319 · Claude $3,3485 + $0,92 + $0,3956 | ≈ 13,4 h |
| SFX-T3 | $0 | dịch vụ khác 0 | ≈ 0,8 h |
| P-2210 | $0 | — | ≈ 0,5 h |

## §4 Kiểm cuối (trên đầu nhánh trước commit báo cáo, @`59b0972b`)
| Kiểm | Kết quả |
|---|---|
| `python3 -I checks/lock.py --verify` | **KHỚP** 1.17.1 `b741f617…` |
| `checks/ll/selftest_k11*.py` (8 bộ) | **8/8 đạt** (số ca ở §1) |
| LOI-KHOA (`cd channel-k2/k2c-t3-01 && sha256sum -c LOI-KHOA.sha256`) | **3/3 OK** (script-v4.2-KHOA.md, loi-khoa.txt, khoa-loi/phat-am/gibraltar-eric.pls) |
| `bash tools/preflight.sh --range origin/main..HEAD` | "preflight: 428 tệp (range origin/main..HEAD) — ĐẠT" · lock KHỚP · PREFLIGHT ĐẠT |
| Email | email chủ dự án 0; email khác trong dòng thêm 0; tác giả/người commit chỉ là `noreply@anthropic.com` |
| `omni/goc720/SHA256SUMS` | 4/4 OK |

Commit báo cáo này cũng qua preflight như các commit khác. Sau đó tôi chạy lại `--range` trước khi đẩy.

## §5 main trước → sau
- **Trước:** `origin/main` = `96b5017c`. Tôi fetch lại ngay trước khi cập nhật: main không đổi và là tổ tiên của nhánh.
- **Sau:** `git checkout main && git merge --ff-only <nhánh>`, rồi `git push origin main` (không force). main trỏ tới commit báo cáo "DỪNG chờ chủ dự án" (con của `59b0972b`). Chuỗi first-parent sau `96b5017c`:
  `36205cf8` merge (1) → `e7c88d70` merge (2) → `132ea033` merge (3) → `318bbc9e` Kinh thánh → `59b0972b` sổ → commit báo cáo.

## §6 Chỉ số trong ±5 % quanh ngưỡng (luật cứng)
Phiên này không tự đo chỉ số phim. Các số trong ±5 % lấy từ báo cáo phiên được merge, nêu lại ở đây:

| Chỉ số | Đo | Ngưỡng | Lệch | Nguồn |
|---|---|---|---|---|
| Bão hoà trung vị V2 | 0,388 | ≥ 0,40 | −3 % (dưới ngưỡng) | ANIM-V2 §10. Đã có quyết định V2-D1: đặt lại ở bước chỉnh màu bản cuối (§14.7) |
| N3.3 cỏ | 47–49 % | 50 % | −2…−6 % | ANIM-V2 §10 |
| Thẻ chương | 3,00 s | trần 3,00 s | 0 % | ANIM-V2 §10 |
| Loudness master V2 | −14,0 LUFS | dải −15…−13,8 | cách cận trên 0,2 LU | ANIM-V2 §10 |
| Loudness trộn thử SFX | −13,9 / −14,0 LUFS | dải −15…−13,8 | 0,1–0,2 LU | SFX-T3 §0 |
| Shot N2_7 | 14,42 s | R3 "> 15 s" | −3,9 % | K117 §9 |
| **Giờ máy ANIMATIC-T3-V2** | ≈ 13,4 h | mốc 14 h | −4,3 % | COST-LEDGER (P-2210 nêu) |

Ngoài ±5 % nhưng cần nhắc: TL-1 5,40 cắt/phút (> 5, +8 %). Chủ dự án đã chấp nhận ở V2-D7, nay ghi ở §14.7.

Giờ máy của P-2210 là 0,5 h so với mốc 2 h, ngoài dải.

## §7 Sự cố
- Bước ghi CSV làm mất ký tự `\r` có sẵn cuối dòng P-2010b. Tôi phát hiện khi đọc diff (−1 dòng không mong muốn), khôi phục từng byte và amend commit **chưa đẩy**. Diff cuối của COST-LEDGER chỉ có +5 dòng, 0 dòng cũ đổi.
- Hook preflight không cài vào `.git/hooks`. Thay vào đó, script tạm chạy preflight trước mọi commit với `pipefail` + kiểm "— ĐẠT".

## §8 Việc chờ chủ dự án
1. **Duyệt kết quả P-2210:** 3 merge; các sửa Kinh thánh (§2); sổ (§3); RIGHTS SFX ở trạng thái "ứng viên" cho tới khi bản cuối chốt danh sách.
2. **§12.1 (b) Kinh thánh**, mâu thuẫn với §14.1 (f)/§15 (e) mới (thẻ "How this film was made" có nêu "AI dùng vào việc gì"). Đề xuất: sửa §12.1 (b) thành "…chỗ nào là ước tính (không nhắc AI — §14.1 (f))".
   - Ưu: hết mâu thuẫn chữ.
   - Nhược: thêm một chỗ sửa Kinh thánh.
   - Tác động: chỉ đổi chữ; thẻ PP T3 đã theo V2-D6.
   - Rủi ro: không có.
3. **HOAMAI-1:** xác nhận mốc giữ là "sau 2,85 s" (ứng viên hiện cắt ở 2,65 s; báo cáo SFX ghi AST còn nghe tiếng "fire" ở mọi điểm cắt 2,65–2,85 s). Bản cuối cắt lại và ghi SHA mới.
4. **T4 London:** 4 mục [cần kiểm] trong HANG-DOI cần tra nguồn ở tiền kỳ T4 (Wren bị gác; Barbican; toà chọc trời vát theo tầm nhìn; mốc Holden–Holford).
5. Phiên song song: BAN-CUOI-T3 lấy `main` mới (đã có V2 + SFX-T3 + Kinh thánh 22/10); K-1.17.2 làm trên LOCK 1.17.1 hiện ở main. Hai việc K có thể gộp: V2-D5 (K-LAI đọc `minh_hoa`) và rà lại SACH-1 (K-1.17 đã xử khiếu nại nhãn "Illustration") theo §14.1 (c) mới: nay không còn nhãn trên hình.

**DỪNG — chờ chủ dự án.**
