Nhánh thật: **`p-2310b`** (đúng lệnh; harness gợi ý `ccr-7fc2ec53-vzzrgk` nhưng không dùng, đẩy `p-2310b` được chấp nhận). Gốc `origin/main` @`8a437031`, đúng gốc lệnh. `main` được cập nhật bằng fast-forward lên đầu nhánh này.

# P-2310b — gộp bộ kiểm 1.17.3 + tiền kỳ T4 vào main, Kinh thánh §19, sổ quyết định 23/10 17:42. BÁO CÁO. DỪNG chờ chủ dự án

## §0 Điều lệ phiên và tóm tắt
| Trường | Lệnh | Thực tế |
|---|---|---|
| Nhánh | `p-2310b` từ origin/main @8a437031 | đúng |
| Vùng sửa | docs/**, AUTHORSHIP.md, RIGHTS.md, COST-LEDGER.csv, channel-k2/BAI-HOC-K2.md, channel-k2/HANG-DOI.md, reports/p2310b/**, main | đúng. Ngoài 2 merge, phiên không sửa `checks/`, `design/`, `scripts/`, `tools/`, `channel-k2/k2c-t3-01/**`, `channel-k2/k2c-t4-02/**` hay nhánh khác. Không đụng vùng LOOK-T4 |
| Đã đọc | BAI-HOC-LL; K1173-BAO-CAO + QUYET-DINH-TREO; TIEN-KY-T4-BAO-CAO, PHIEU-G1, DE-XUAT-BIBLE-19, UOC-VA-GHIM (tóm tắt §7); RIGHTS-NHAP; TREATMENT; Kinh thánh §13.6, §14, §15, §17, §18 | đúng |
| Chi phí | không gọi API trả phí; giờ máy 2 h | API **$0**, 0 subagent; giờ máy ≈ **0,7 h**. Có tải miễn phí siêu dữ liệu giấy phép (Met/YCBA/LoC API, NGA open data) để vá bằng chứng thiếu (§4) |
| Preflight | `set -o pipefail`, chỉ commit khi có "— ĐẠT" | một script nhỏ chạy `tools/preflight.sh` với `pipefail`, chỉ cho commit khi có cả "— ĐẠT" và "PREFLIGHT ĐẠT". Hook pre-commit cũng chạy lại. Mọi commit đều ĐẠT. `--range origin/main..HEAD` ĐẠT (§5) |
| Hook | cài trước lần đẩy đầu | `pre-commit` và `pre-push` → `tools/preflight.sh`, cài lúc 10:50 UTC, trước lần đẩy đầu (≈ 10:53) |
| Email / UA | che; không đưa email chủ dự án vào header/URL/payload/UA/tệp | 0 email chủ dự án trong diff, commit và tệp. Mọi yêu cầu mạng dùng UA `CineLab-research (+https://github.com/HungQuach301/cine-lab)` |
| `lock.py` | chỉ `--verify` | chỉ `--verify`; mọi lần đều KHỚP |
| Force / amend | không | 0 force, 0 amend |
| Đẩy ≤ 30 phút + CHECKPOINT | bắt buộc | đẩy 10:53 và 11:01 UTC, rồi lần cuối; `reports/p2310b/CHECKPOINT.md` |
| Lệnh bổ sung | ghi vào CHECKPOINT | không có lệnh bổ sung nào trong phiên |
| Môi trường | `verify.sh` | 10 PASS, 5 FAIL (các mục tuỳ chọn, ví dụ Freesound 403). Phiên này không cần mục nào trong số đó |

**Tóm tắt**
1. **2 merge `--no-ff`, 0 xung đột.** LOCK 1.17.2 → **1.17.3 `d99af8f2…` KHỚP** từ sau merge (1). 10/10 bộ `selftest_k11*.py` đạt sau mỗi merge và ở lần kiểm cuối. LOI-KHOA T3 3/3.
2. **Kinh thánh `b607d917…` → `d229fd9d…`.** Thêm §19; §13.6 thêm 1 dòng trỏ §19; sửa §15 (d)(f); ghi chú lửa T4 (D5) đặt trong §19 (§2).
3. **Sổ:** AUTHORSHIP +3 dòng; RIGHTS +1 mục (15 dòng); COST-LEDGER +3 dòng (KHEP-T3 đã có nên không thêm); BAI-HOC-K2 K35–K39; HANG-DOI mục 23/10 17:42 (§3).
4. **Phát hiện:** `channel-k2/.gitignore` có dòng `*.json`, vì vậy nhiều JSON tiền kỳ T4 **không vào git**, dù báo cáo TIEN-KY-T4 ghi là "trong git". Thiếu bằng chứng giấy phép `licenses/<id>.json`, `BANG-SHOT-v1.json` và `du-lieu/khop-doornick.json`, `ranh-chay-1666-cuoi.json`. Phiên này đã tải lại bằng chứng của 7 mục vào vùng của mình; phần còn lại cần chủ dự án quyết (§4, §8).
5. **main `8a437031` → đầu nhánh này** (fast-forward; main cũ là tổ tiên; không force) (§6).

## §1 Merge
| # | Nhánh @SHA | Commit merge | Số tệp | Vùng | LOCK sau merge | selftest k11* | LOI-KHOA |
|---|---|---|---|---|---|---|---|
| 1 | `origin/checks-1-17-3` @`36112c29` | `c9cc5468` | 23 (+1 486 / −46) | checks/ (12: LOCK, cinecheck, ll/ 10), reports/k1173 (10), checks-appeal.md (1) | **1.17.3 `d99af8f22d5e7c0ba3469c4b95bcc01296f72f64d9e72d21ed3fb897549ba10b` KHỚP** | 10/10 đạt | 3/3 |
| 2 | `origin/k2c-t4-02-tienky` @`888de179` | `f0253165` | 134 (+8 430 / −0) | channel-k2/k2c-t4-02 (40), design/k2v/ldn (1), reports/tien-ky-t4 (60), scripts/k2ldn (33) | KHỚP | 10/10 đạt | 3/3 |

Kết quả selftest (giống nhau ở cả 3 lượt): k112 75/75 · k1121 48/48 · k1122 37/37 · k113 64/64 · k114 126/126 · k115 105/105 · k116 144/144 · k117 130/130 · k1172 74/74 · k1173 42/42.

Diff của 2 nhánh không có tệp LFS nào, nên không cần `git lfs push` (K33).

## §2 Kinh thánh `docs/BIBLE-KENH2.md`
- **SHA-256 trước:** `b607d917dd2fd2c1caa1a034307a53d4c69fd95a9411d6bad2aea54b2b94e701` (main @8a437031).
- **SHA-256 sau:** `d229fd9dd8ec61f6c9b3931c8eabc397a76caceb515338b2c1214683e672d35f` (commit `d0e7f7e9`). Thay đổi: +34 dòng, −3 dòng.
- Diff đầy đủ ở `reports/p2310b/bible-diff.txt`; script ở `reports/p2310b/sua_bible.py`. Mỗi chuỗi gốc được kiểm là xuất hiện đúng 1 lần trước khi thay.

| Chỗ | Trước | Sau |
|---|---|---|
| Tiêu đề | "…; sửa §14–§15 + §17 + §18 — 22/10/2026)" | "…; sửa §14–§15 + §17 + §18 — 22/10/2026; **§19 + sửa §13.6, §15 — 23/10/2026**)" |
| §13.6 | — | Thêm 1 dòng sau TL-6: "Từ T4: máy trong shot theo §19 (a) (thay TL-1 "cố định hoặc trôi ≤ 2 %/s"; CODINH vẫn bắt buộc cho shot có tấm nền N2+); bản đồ cổ và tranh khắc theo §19 (b)(c) (thay TL-4) — chủ dự án duyệt 23/10/2026 17:42 (G1 T4, D9)." |
| §15 (d) | "…video AI chỉ cho minh hoạ M-d." | thêm: "T4: tấm nền N2+ lập kế hoạch ≤ 15 % thời lượng tới khi phiên K xét phép (iii) (D11, chủ dự án 23/10/2026 17:42); trần 50 % giữ nguyên làm trần luật." |
| §15 (f) | "(6) nổ nhà bằng thuốc súng Tower Street;" | "(6) người cứu đồ lên xe ở Cheapside sáng 3/9 (thay "nổ nhà bằng thuốc súng Tower Street": nổ nhà là lớp dữ kiện theo LUAT-N2P-T4 b34 → dựng 3D; D10, chủ dự án 23/10/2026 17:42);" |
| §19 (mới) | — | Tiêu đề "## 19. Ngữ pháp máy điện ảnh cho timelapse cùng nơi + chất liệu tư liệu sống (áp từ T4; chủ dự án duyệt 23/10/2026 17:42 (G1 T4, D9))". Thân là (a) bảng 11 cú máy + Luật (1)–(4), (b) bản đồ cổ hoạt hoá, (c) tranh khắc. **Chép nguyên văn khối trích dẫn** của `DE-XUAT-BIBLE-19.md`: chỉ bỏ dấu "> " đầu dòng, đổi dòng in đậm thành tiêu đề "## 19." và điền "…/10/2026" |
| §19 phạm vi (mới) | — | Khối "Phạm vi và quan hệ với luật cũ": áp từ T4; (a) thay TL-1 "cố định (hoặc trôi ≤ 2 %/s)" từ T4, CODINH vẫn bắt buộc khi có N2+, sản xuất giữ ≤ 3°/s (D9); (b)(c) thay TL-4 cho bản đồ cổ/tranh khắc từ T4; trần bản đồ (cổ + 3D kiểu bản đồ) ≤ 12 %, tư liệu + tranh khắc + thẻ ≤ 10 % |
| Ghi chú lửa T4 (D5) | — | Đặt trong khối phạm vi §19: "lửa/khói cách A (atlas nướng sẵn) cho cảnh rộng; Cycles GPU chỉ 3–4 cận đêm (≈ 30–40 s); không ghép A↔B trong một cú máy (§14.2); nếu Cycles ngày không sửa được mép thể tích → chỉ A" |

**Chỗ chữ còn chồng nhau (lệnh không yêu cầu sửa, nên tôi chưa sửa):**
- §17 (1) cho bản đồ bối cảnh "≤ 1 lần/chương, ≤ 8 s", còn §19 (b) cho bản đồ cổ "mỗi lần ≤ 10 s, ≤ 1–2 lần/hồi".
- §17 (2) cho tư liệu "≤ 8 s, ≤ 1 lần/60–90 s", còn §19 (c) không ghi trần thời gian mỗi lần.
- K1171-D3 (17:42) ghi "T4 dùng §17" cho bản đồ.
- Đề xuất cách đọc: §19 (b)(c) là luật riêng cho bản đồ cổ/tranh khắc; §17 áp cho bản đồ 3D kiểu bối cảnh và ảnh tư liệu khác. Xem §8 mục 3.

## §3 Sổ (dòng thêm; 0 dòng cũ bị đổi)
Commit `9ae0f090`, script `reports/p2310b/ghi_so.py`. Script chỉ nối thêm và giữ nguyên byte có sẵn. Lần chạy đầu làm mất 1 ký tự `\r` ở dòng P-2010b của COST-LEDGER (lặp lỗi P-2210). Tôi đã khôi phục trước khi commit và sửa script để đọc/ghi bằng `newline=""`. Diff cuối: +47 / −0.

**AUTHORSHIP.md (+3 dòng, mỗi dòng ghi "P-2310b ghi"):**
- **23/10 17:42 G1 T4 + M1b.** Nguyên văn "S3 KHÔNG cần đổi, còn lại đồng ý theo đề xuất của bạn" ("S3" = D3), kèm nội dung D1–D18:
  - **D3 GIỮ** câu L04 "London has burned to the ground twice" và logline như cũ.
  - **D11** gửi phiên K; kế hoạch N2+ ≤ 15 %.
  - **D12** bỏ Leake, dùng Doornick 1666.
  - D9 là Kinh thánh §19; D10 thay khoảnh khắc Tower Street bằng Cheapside.
  - Bước **M1b "khoá look T4"** trước animatic.
  - Cột đóng góp con người: chủ dự án tự quyết giữ cách nói mạnh của logline, bác đề xuất làm mềm của phiên.
- **23/10 17:42, dữ kiện sáng tạo của treatment (D1).**
  - Hook Pepys *"a little ale-house on the Bankside, over against the Three Cranes"* (bậc 1, Gutenberg #4167).
  - 8 khoảnh khắc then chốt, chép từ `TREATMENT.md` (H1-08/M03, H1-09, H1-13/14, H2-02, H2-05/06, H2-09/10, H4-04/05, H5-07/08).
- **23/10 17:42 bảng QUYET-DINH-TREO K-1.17.3.**
  - Các dòng theo khuyến nghị: K117-D1 A; D3 A; D5 A, đo trên bản không nén; D6 A; D8 A + mở phiên K làm thước biến cố đo trên video trước G2 T4; K1171-D2, D3 (T4 dùng §17), D4 A; K1173-D2…D6 A.
  - **Riêng K1173-D1 = B:** cơ chế ngoại lệ có khai áp cho tập sau; T3 giữ hàng EO-DAT-R3 (a) TRƯỢT trong hồ sơ, không ghi "ý đồ bookend".
  - K117-D4, K117-D7, K1171-D1: hết hiệu lực.
  - Dòng này **không nêu id shot T3** và ghi rõ "KHÔNG phải dòng ngoại lệ cho shot nào". Như vậy cơ chế `r3_ngoai_le` của 1.17.3 không thể vô tình nhận nó làm dòng miễn.

**RIGHTS.md (+1 mục, 15 dòng, trạng thái "T4 tiền kỳ — đã kiểm giấy phép"):**
- 12 tư liệu hình:
  - Rijksmuseum: Doornick, Luyken, Charles II, Monument.
  - The Met: 360649, 361738, 395057.
  - YCBA: 266, 40597.
  - NGA Wren, LoC Wren plan, Ogilby.
- 3 dòng dữ liệu: OSM (ODbL 1.0), EA LiDAR (OGL v3), OSTN15 để **[cần kiểm]** đúng như nguồn.
- **Ogilby:** ghi "chỉ tham khảo nội bộ, không lên hình" (D13).
- **Rijks Monument:** nháp ghi CC0, nhưng trang chụp trong git ghi Public Domain Mark 1.0. Tôi ghi theo bằng chứng có trong repo và nêu cả hai; cả hai đều cho dùng tự do.
- Ghi chú dưới bảng:
  - Leake bỏ (D12); MOI 1940 chưa có (D14); không dùng ảnh Mason (T4-G1).
  - Văn bản Pepys/Evelyn/*True and Exact Relation* đã có ở `N2P-T4-1…3`. Đây là câu "[cần kiểm] RIGHTS.md" của nháp §C, nay đã kiểm: có rồi, nên không ghi trùng.
  - Đầu ra AI bản thử chưa ghi dòng RIGHTS vì chưa vào phim.

**COST-LEDGER.csv (+3 dòng, 20 cột, kiểm bằng `csv`):**
| Phiên | Claude API | Dịch vụ khác | Giờ máy |
|---|---|---|---|
| TIEN-KY-T4 | $0,82 | OpenAI $0,50; Gemini $1,02; RunPod $1,90 (tổng ≈ $4,24) | ≈ 5 h |
| K-1.17.3 | $0 | 0 | ≈ 1,2 h |
| P-2310b | $0 | 0 (chỉ tải miễn phí) | ≈ 0,7 h |

Dòng KHEP-T3 đã có (dòng 85), nên không thêm.

**channel-k2/BAI-HOC-K2.md (+K35–K39):**
- K35: tiền kỳ dựng hình học mới phải có bước khoá look trước animatic (T4 khối thô so với look T3).
- K36: TAMU IIIF và trang bảo tàng chặn trình duyệt tự động → lấy bằng chứng từ JSON API/manifest.
- K37: Commons API 429 → lùi và giảm số lần gọi.
- K38: câu trích nổi tiếng phải tra toàn văn nguồn gốc (Bludworth "piss it out" không có trong Pepys).
- **K39 (P thêm):** `.gitignore` bỏ `*.json` làm mất bằng chứng và dữ liệu tiền kỳ. Luật mới: đối chiếu `git ls-files` với danh sách tệp báo cáo trước commit cuối.

**channel-k2/HANG-DOI.md:** mục "CẬP NHẬT 23/10/2026 17:42 (phiên P-2310b: T4)", đặt trên mục PHAT-HANH-T3.
- T4 K2C-T4-02: "**G1 duyệt 23/10 17:42; M1b khoá look đang chạy**".
- **D3: GIỮ logline** và câu L04.
- Ghi thêm D11, D12, §19. Bước tiếp: M1b → animatic.

## §4 Bằng chứng giấy phép thiếu trong git — đã vá phần thuộc vùng P
- **Nguyên nhân:** `channel-k2/.gitignore:2: *.json` (kiểm bằng `git check-ignore -v`). TIEN-KY-T4 ghi bằng chứng ở `licenses/<id>.json` cho mọi mục, nhưng trong git chỉ có trang chụp `-trang.html/.jpg` của 4 mục Rijks và Ogilby.
- **Đã làm (vùng `reports/p2310b/**`):** tải lại siêu dữ liệu nguyên văn, không tải ảnh, vào `reports/p2310b/bang-chung/` (7 JSON + `SHA256SUMS`, `sha256sum -c` 7/7 OK). Giấy phép **khớp nháp ở cả 7 mục**:
  - Met 360649, 361738, 395057: `"isPublicDomain": true`.
  - YCBA 266, 40597: `"rights": ".../publicdomain/zero/1.0/"` và "Copyright Statement: Public Domain".
  - LoC 2004678686: `"No known restrictions on publication."`.
  - NGA: hàng `published_images.csv` có `openaccess = 1`, uuid `e12f2cab…`, trùng URL ảnh trong `SHA256-TU-LIEU.txt`.
- **Chưa làm được (ngoài vùng, `channel-k2/k2c-t4-02/**` cấm sửa):** `BANG-SHOT-v1.json`, `du-lieu/khop-doornick.json`, `du-lieu/ranh-chay-1666-cuoi.json` (và có thể các JSON khác dưới `channel-k2/`) không có trong git. Đây là đầu vào sản xuất. Theo K22, các tệp này phải có trong git hoặc tái tạo được bằng lệnh + SHA. Xem §8 mục 2.

## §5 Kiểm cuối (đầu nhánh @`89d55a21`, trước commit báo cáo)
| Kiểm | Kết quả |
|---|---|
| `python3 -I checks/lock.py --verify` | **KHỚP** 1.17.3 `d99af8f2…` |
| `checks/ll/selftest_k11*.py` (10 bộ) | **10/10 đạt** (số ca ở §1) |
| LOI-KHOA T3 | **3/3 OK** |
| `bash tools/preflight.sh --range origin/main..HEAD` | "preflight: 175 tệp (range origin/main..HEAD) — ĐẠT" · lock KHỚP · PREFLIGHT ĐẠT |
| Email | email chủ dự án 0 (diff, nội dung commit); tác giả/người commit chỉ là `noreply@anthropic.com` |
| `bang-chung/SHA256SUMS` | 7/7 OK |

Commit báo cáo cũng qua preflight. Tôi chạy lại `--range` trước khi cập nhật main.

## §6 main trước → sau
- **Trước:** `origin/main` = `8a437031`. Tôi fetch lại ngay trước khi cập nhật: main không đổi và là tổ tiên của nhánh.
- **Sau:** `git checkout main && git merge --ff-only p-2310b`, rồi `git push origin main` (không force). main trỏ tới commit báo cáo "DỪNG chờ chủ dự án".
- Chuỗi first-parent sau `8a437031`: `c9cc5468` merge (1) → `f0253165` merge (2) → `2017aa52` CHECKPOINT → `d0e7f7e9` Kinh thánh → `9ae0f090` sổ → `89d55a21` CHECKPOINT → commit báo cáo.

## §7 Chỉ số trong ±5 % quanh ngưỡng (luật cứng)
Phiên này không tự đo chỉ số phim. Các số dưới đây lấy từ báo cáo của nhánh được merge:

| Chỉ số | Đo | Ngưỡng | Lệch | Nguồn |
|---|---|---|---|---|
| Số từ lời nháp v1 T4 | 1 593 | 1 650 (khung 1 650–1 800) | −3,5 % | TIEN-KY-T4 §13; D2 (a) duyệt: sửa ở v2, không độn chữ |
| TL + KHÁC + THẺ (bảng shot v1) | 9,72 % | ≤ 10 % (nay là trần tư liệu + tranh khắc + thẻ §19 (c)) | −2,8 % | TIEN-KY-T4 §13; D4 khoá cap ở v2 |
| Góc cao (bảng shot v1) | 75,56 % | ≥ 75 % (TL-1 / §19 (a) luật 4) | +0,7 % | TIEN-KY-T4 §13 |
| Diện tích vùng cháy số hoá | 399 acre | dữ kiện "over 400 acres" | −0,25 % | TIEN-KY-T4 §13 (đo, không phải ngưỡng kiểm) |
| R3 (b) N5_1 | 6,00 s | ≤ 6 s | 0 % | K1173-D2 (A duyệt 17:42) |

Ngoài ±5 % nhưng cần nhắc:
- Tấm N2+ trong bảng shot v1 là **26,39 %**, so với kế hoạch mới **≤ 15 %** (D11): vượt 76 %. Bảng shot v2 phải hạ N2P tới khi phiên K kết luận phép (iii).
- Vòng cung T4 10,6°/s và cẩu 3,74°/s, so với ≤ 3°/s (§19). Sản xuất giữ ≤ 3°/s.

Giờ máy P-2310b là 0,7 h so với mốc 2 h, ngoài dải.

## §8 Việc chờ chủ dự án
1. **Duyệt kết quả P-2310b:** 2 merge; Kinh thánh §19 + §13.6 + §15 (§2); sổ (§3).
2. **JSON tiền kỳ T4 không có trong git (§4).** Đề xuất giao phiên LOOK-T4 (đang giữ vùng `channel-k2/k2c-t4-02`) hoặc phiên T4 kế tiếp:
   - (a) thêm ngoại lệ `!k2c-t4-02/**/*.json` vào `channel-k2/.gitignore` rồi commit các JSON còn trên máy của phiên đó; nếu đã mất thì tái tạo bằng `scripts/k2ldn/bang_shot.py`, `khop_ban_do.py`, `ranh_chay.py` và ghi SHA.
   - Ưu: đầu vào sản xuất có trong git (K22).
   - Nhược: thêm một lượt việc nhỏ.
   - Tác động: bảng shot v2, bản đồ hoạt hoá, ranh cháy.
   - Rủi ro: nếu không làm, phiên sau dựng trên số không tái lập được.
3. **§17 và §19 chồng nhau ở bản đồ/tư liệu (§2).** Đề xuất ghi một câu vào §19: "bản đồ cổ/tranh khắc theo §19 (b)(c); §17 (1)(2) cho bản đồ 3D bối cảnh và ảnh tư liệu khác".
   - Ưu: hết mơ hồ cho phiên K khi viết luật §19.
   - Nhược: thêm một chỗ sửa Kinh thánh.
   - Rủi ro: thấp.
4. **Phiên K:** (i) xét phép (iii) bộ kiểm N2P (D11); (ii) thước biến cố đo trên video trước G2 T4 (K117-D8); (iii) viết miễn Q37 (c) cho thẻ PP + selftest (K1173-D6); (iv) biến §19 thành chỉ số đo từ log máy `render_ldn.js`.
5. **Còn treo từ tiền kỳ:**
   - D14: tìm ảnh MOI 1940.
   - D13: xác nhận điều khoản BL cho Ogilby nếu muốn đưa lên hình.
   - OSTN15: câu giấy phép [cần kiểm].
   - 22 mục [cần kiểm] của lời nháp: xử lý ở v2.
6. **Phiên song song LOOK-T4:** lấy `main` mới (đã có tiền kỳ T4 + Kinh thánh §19 + LOCK 1.17.3). Phiên này không đụng vùng của LOOK-T4.

**DỪNG — chờ chủ dự án.**
