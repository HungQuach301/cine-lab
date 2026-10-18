# PHIÊN P-1810c: hợp nhất V6 + NC-AI, Kinh thánh §12, ghi sổ 18/10 tối. BÁO CÁO. DỪNG chờ chủ dự án

Nhánh thật: **`p-1810c`** (tạo từ `origin/main` @`6c16e548`). Harness giao nhánh `ccr-1bdc14ed-kg4yu8`. P làm và đẩy `p-1810c` theo lệnh, không đẩy nhánh harness.

```text
ĐIỀU LỆ PHIÊN P-1810c                                        | thực tế
Loại phiên:        P (điều phối)                              | đúng
Nhánh:             p-1810c từ origin/main @6c16e548            | đúng; đẩy p-1810c; main KHÔNG cập nhật
Merge --no-ff:     ccr-0e3bf8dd-nst2mv (V6) → ccr-fcb0e150-g16lfi (NC-AI)
                                                              | 2/2 đúng thứ tự, 0 xung đột
KHÔNG merge:       nhánh khác (casting-giong đang chạy)        | không merge nhánh nào khác
Sửa ngoài merge:   docs/BIBLE-KENH2.md (§12 + 4 loại chỗ theo lệnh), COST-LEDGER, RIGHTS,
                   AUTHORSHIP, channel-k2/HANG-DOI.md, reports/ | đúng; không sửa checks/, scripts/, design/
Chi phí:           Claude/OpenAI/ElevenLabs/YouTube 0          | $0 · $0 · 0 · 0 (WebFetch + 1 curl đọc trang YouTube Help)
Giờ máy:           mốc theo dõi 1,5 h                          | ≈ 0,3 h thời gian thực (16:22 → 16:40 UTC); chưa vượt
Preflight:         BẮT BUỘC; che email                         | --staged ĐẠT ở cả 3 commit P; --range TRƯỢT 1 mục có sẵn (§2.3); 0 email mới
Email chủ dự án:   không vào header/URL/payload                | đúng; curl dùng UA "CineLab-research (+https://github.com/HungQuach301/cine-lab)"
```

## 0. Tóm tắt
| Mục | Kết quả |
|---|---|
| Merge | 2/2 `--no-ff`, **0 xung đột**: V6 `e7aec271` (1 409 tệp, +268 699 / −114), NC-AI `64b36f3c` (46 tệp, +7 235, chỉ `reports/`) (§1) |
| LOCK | `python3 -I checks/lock.py --verify` **KHỚP 1.15.0 `f4fa0349ca53b05d64e4303554ec168e6445c82d97e662672f70ccf42df80d40`**. Kiểm sau merge, trong preflight mỗi commit, trước khi đẩy. Không gọi `lock.py` khi thiếu `--verify` |
| Selftest | k115 **105/105** · k114 **126/126** · k113 **64/64** · k1122 **37/37** · k1121 **48/48** · k112 **75/75** · k2 **129/129** · ll **317/317** |
| verify.sh | **14 PASS / 1 FAIL**: chỉ còn Freesound 403, mục tuỳ chọn. Đầu phiên được 9/5 vì container mới; P đã cài lại môi trường (§2.2) |
| Golden | steel **KHỚP** · ll08 **KHỚP** · t1 **LỆCH CỤC BỘ 22/144** (như cũ). SSIM cả 3 ca thấp hơn P-1810b, **trùng đúng số V6 tự báo** (§2.1) |
| Kinh thánh | `docs/BIBLE-KENH2.md`: SHA-256 trước `2a8c263a…8816822`, sau **`3307185e3e51a78f57088aa74ae575c828fd9d80fe4f04514451a70d1a24eaaf`**. Khối §12 khớp nguyên văn (máy so `diff`) (§3) |
| YouTube | Cách làm §12.1 **đáp ứng** trang chính sách hiện hành, vì trang không đòi nhãn trên hình. Có 3 điểm cần chủ dự án quyết (§4) |
| Sổ | COST-LEDGER thêm 3 dòng, sửa dòng V1 · RIGHTS thêm 8 dòng và đổi phạm vi 2 dòng · AUTHORSHIP 8 dòng · HANG-DOI T3, T8 (§5) |
| Nhánh tên mới | `v6` → `eb852a30` · `nc-ai` → `4bef9846`. Không xoá nhánh cũ (§6) |

## 1. Merge (số trước / sau)
SHA đầu nhánh khớp lệnh: `origin/main` = `6c16e548`, `origin/ccr-0e3bf8dd-nst2mv` = `eb852a30`, `origin/ccr-fcb0e150-g16lfi` = `4bef9846`.

| # | Nhánh @ SHA | Commit | Thay đổi (so cha 1) | Xung đột |
|---|---|---|---|---|
| — | `origin/main` (trước) | `6c16e548` | LOCK 1.15.0 `f4fa0349…` | — |
| 1 | `origin/ccr-0e3bf8dd-nst2mv` @eb852a30 (V6; gồm V5b-2c, V5b-2d, PT3, PT4, checks 1.15) | `e7aec271` | 1 409 tệp, +268 699 / −114. Phần lớn ở `reports/` (pt, pt2, pt3, pt4, v5b2b, v5b2d, v6), `design/`, `scripts/k2tl/`. **Không đổi `checks/`**, vì checks 1.15 đã có trên main | không |
| 2 | `origin/ccr-fcb0e150-g16lfi` @4bef9846 (NC-AI) | `64b36f3c` | 46 tệp, +7 235 / −0, gồm `reports/NC-AI-BAO-CAO.md` và `reports/nc-ai/**` | không |
| — | Kinh thánh §12 | `fbc87b76` | 1 tệp, +48 / −14 (§3) | — |
| — | Ghi sổ | `a5b983ea` | 5 tệp (§5) và `reports/p-1810c/golden.json` | — |
| — | Báo cáo | commit chứa tệp này | `reports/P-1810c-BAO-CAO.md` | — |

Sau merge, LOCK vẫn là **1.15.0 `f4fa0349…`**, trước và sau như nhau.

## 2. Kiểm sau merge
| Kiểm | Kết quả | Thời gian |
|---|---|---|
| `python3 -I checks/lock.py --verify` | **KHỚP**: 1.15.0, `f4fa0349…df80d40` | < 1 s |
| `selftest_k115.py` | **105/105**, 15 nhóm | 11 s |
| `selftest_k114.py` | **126/126** | 5 s |
| `selftest_k113.py` | **64/64**, 11 nhóm | 4 s |
| `selftest_k1122.py` | **37/37**, 4 biến thể | 1 s |
| `selftest_k1121.py` | **48/48**, 9 luật | 7 s |
| `selftest_k112.py` | **75/75**, 13 luật | 7 s |
| `selftest_k2.py` | **129/129** (kênh 2, 1.11.1) | 31 s |
| `selftest_ll.py` | **317/317** (LL v3) | 354 s, chạy song song với golden |
| golden steel | **KHỚP**: pHash 0/64, SSIM **0,9449**, MAD 2,08, > 24: 0,04 %, 0/144 ô | 111,1 s |
| golden ll08 | **KHỚP**: pHash 0/64, SSIM **0,9307**, MAD 2,25, > 24: 0,01 %, 0/144 ô | 135,6 s |
| golden t1 | **LỆCH CỤC BỘ**: pHash 0/64, SSIM **0,9082**, MAD 4,51, > 24: 1,28 %, **22/144 ô** | 56,0 s |

Mọi selftest chạy bằng `/opt/cine/bin/python -I checks/ll/selftest_*.py`. P chỉ chạy các tệp này, không đọc mã của chúng.

### 2.1 Golden: số trước / sau
So từng trường với `reports/p-1810b/golden.json`:

| Ca | SSIM P-1810b → P-1810c | MAD | > 24 | Ô lệch | Giây dựng 3D |
|---|---|---|---|---|---|
| steel | 0,978 → **0,9449** | 1,76 → 2,08 | 0,04 → 0,04 % | 0 → 0 | 176,8 → 97,9 |
| ll08 | 0,9686 → **0,9307** | 1,74 → 2,25 | 0,0 → 0,01 % | 0 → 0 | 412,4 → 123,0 |
| t1 | 0,9548 → **0,9082** | 3,86 → 4,51 | 1,24 → 1,28 % | 22 → 22 (danh sách ô trùng) | 129,3 → 47,4 |

- **Nguyên nhân:** V6 sửa trình dựng chung (`k2.js`, `terrain.js`: bóng 8192², SSAO 2 tầng, chỉnh màu V6). V6 §1 tự báo đúng số **"SSIM 0,9449 / 0,9307, pHash 0/64, ô lệch 0/144"** cho steel/ll08 (`reports/v6/do/golden-steel-ll08.json`). Số của P trùng đến chữ số cuối. Danh sách ô lệch của t1 không đổi, nên phần lệch vẫn là dòng nguồn đáy đã biết.
- **Chỉ số trong ±5 % quanh ngưỡng SSIM 0,90:**
  - t1 0,9082 (+0,9 %)
  - ll08 0,9307 (+3,4 %)
  - steel 0,9449 (+4,99 %)

  Cả ba ca đều mất 3–5 điểm SSIM so với P-1810b. Một lượt sửa trình dựng nữa có thể đẩy t1 xuống dưới 0,90. Đề nghị Claude điều phối hoặc chủ dự án xem `sheet.jpg` của t1 (`/var/tmp/golden-p1810c/t1/`, ngoài git). Nếu nhìn ổn thì chụp lại tham chiếu golden theo trình dựng V6, vì §12.5 đã chọn V6 làm mức dựng T3.
- `golden.py` trả mã 1 vì t1 LỆCH CỤC BỘ. Số đo nằm ở `reports/p-1810c/golden.json`.

### 2.2 Môi trường (`scripts/env/verify.sh`)
- Đầu phiên: **9 PASS / 5 FAIL**. Thiếu OpenEXR, three.js, tifffile/pyshp, k2v node_modules; Freesound trả 403.
- P cài `OpenEXR`, `tifffile`, `pyshp` qua pip vào `/opt/cine`, rồi chạy `npm ci` trong `design/cong3/shared` và `design/k2v`. Các bước này không sửa tệp nào trong git.
- Sau khi cài: **14 PASS / 1 FAIL**. Chỉ còn Freesound 403, mục tuỳ chọn. Tổng giờ là 15 mục, P-1810b là 14.

### 2.3 Preflight: một mục chặn có sẵn từ V5b-2d (chưa sửa, cần quyết)
- `bash tools/preflight.sh --staged` **ĐẠT** ở cả 3 commit của P.
- `bash tools/preflight.sh --range origin/main..HEAD` **TRƯỢT 1 mục**: `CHẶN P3 tệp 11.0 MB > 5 MB không qua LFS: reports/v5b2d/khung/v5b2d-t-540p.mp4`. SHA-256 của tệp: `338cef975346541e7b4becc7089beadede6e27a8326c196668e796fc342a4a8f`.
- **Nguồn gốc:** V5b-2d (commit `da53cbd9`) làm đúng luật cũ §11.6 ("540p ≤ 15 MB, không vào LFS"). Preflight chặn ở 5 MB, nên V6 đã phải đẩy `--no-verify` một lần (V6 §4). **§12.5 mới chốt "Video trong git ≤ 5 MB (preflight)".**
- **P không xoá tệp:** lệnh không giao, và tệp đã nằm trong lịch sử nhánh trên origin, nên `git rm` không thu lại dung lượng. Hook không cài trong container này. P đẩy bình thường và ghi lại ở đây.
- **Cần Claude điều phối quyết trước khi ff `main`** (§8 mục 2):
  - (a) Ghi ngoại lệ một lần cho tệp có từ trước §12.5. Ưu: không đổi lịch sử. Nhược: preflight `--range` trên main còn trượt cho tới khi có ngoại lệ trong tools.
  - (b) `git rm` tệp, giữ SHA ở báo cáo V5b-2d. Ưu: cây làm việc đúng §12.5. Nhược: lịch sử vẫn mang 11 MB.
  - (c) Viết lại lịch sử. **Không khuyến nghị**, vì nhánh đã chia sẻ.

## 3. Kinh thánh `docs/BIBLE-KENH2.md` (chỉ các chỗ đã sửa)
SHA-256 trước `2a8c263aa71d2297b5bf024c0eb3b16fd7ec4c361526cf9e59dcc8c5e8816822`, sau `3307185e3e51a78f57088aa74ae575c828fd9d80fe4f04514451a70d1a24eaaf`. Mọi thay thế chạy bằng script có kiểm "đúng 1 lần xuất hiện". Ngoài các chỗ dưới đây, không câu nào đổi.

**(a) Dòng tiêu đề**, thêm vào cuối ngoặc:
```diff
-… 16–17/10/2026 — §10 và 17–18/10/2026 — §11)
+… 16–17/10/2026 — §10 và 17–18/10/2026 — §11; bổ sung 18/10/2026 tối — §12)
```

**(b) Khối §12**: thêm vào cuối tệp sau một dòng trống, gồm "## 12. Bổ sung 18/10/2026 tối…" và §12.1–§12.5. `diff` giữa đuôi tệp và bản chép từ lệnh cho **0 khác biệt**.

**(c) §11.3, dòng đầu:**
```diff
-- GIÁ TRỊ KHÔNG ĐÁNH ĐỔI: mọi mốc/dữ kiện có nguồn trên hình; bố cục, …
+- GIÁ TRỊ KHÔNG ĐÁNH ĐỔI: mọi mốc/dữ kiện có nguồn, người xem tra được (mô tả, bình luận ghim, thẻ phương pháp — §12.1); bố cục, …
```

**(d) Thêm " (chữ trên hình: theo §12.1)" vào cuối 12 câu yêu cầu nhãn hoặc chữ trên hình:**

| Mục | Câu (đầu câu) | Chữ trên hình mà câu yêu cầu |
|---|---|---|
| §10.4 | "**Thành phố phải có nhà và đường đúng thời kỳ**…" | GHOST có nhãn nguồn; bản đồ lịch sử phẳng có nhãn |
| §10.4 | "Mọi shot bản đồ có chip nơi dựng hoặc nhãn địa danh…" | chip / nhãn địa danh |
| §10.4 | "Không phần tử nào có năm xây > năm bộ đếm…" | ghost có nhãn nguồn ≥ 38 px |
| §10.5 | "Nhãn chủ chốt hiện đủ…" | nhãn chủ chốt, số so sánh |
| §10.5 | "Dải tối dưới không phủ cả bề ngang…" | tấm chú thích / dòng nguồn |
| §11.1 | "Loại cảnh `strategic`…" | nhãn mốc thời gian, chú giải |
| §11.1 | "Inset: góc TRÊN TRÁI…" | 1–2 nhãn, "Map: Natural Earth" |
| §11.1 | "Ranh lịch sử: nhãn "approx. borders…"" | "approx. borders", "contested" |
| §11.1 | "Tuyến: tuyến biển không cắt đất…" | "route approx." |
| §11.3 | "Được dùng: (a) tấm C khung neo…" | nhãn "illustration" ở mục (d) |
| §11.3 | "Nhãn + công bố:…" | "Surface detail AI-assisted…" suốt shot |
| §11.4 | "Phố có nguồn nhưng bản đồ không vẽ hết…" | "estimated infill" |

**P chọn câu như sau, cần Claude điều phối rà:**
- P hiểu "cuối các mục … có câu yêu cầu nhãn/chữ trên hình" là thêm cụm vào cuối từng câu (gạch đầu dòng) có yêu cầu đó, không chỉ cuối mỗi mục.
- Ở §10.5, P đánh dấu 2 câu (nhãn chủ chốt; tấm chú thích / dòng nguồn). Câu "Ảnh có chuyển động máy/chú thích đổi ≤ 12 s" là luật thời lượng, không yêu cầu chữ, nên không đánh dấu.
- Nếu cần thu hẹp về đúng 5 chỗ §12.1 nêu tên, bỏ cụm ở 7 câu còn lại. Cụ thể là bỏ ở chip/nhãn địa danh §10.4, nhãn chủ chốt §10.5, strategic, inset, tuyến §11.1 và "illustration" §11.3.

**Mâu thuẫn còn lại, P không sửa vì lệnh nói "không sửa câu nào khác":**
- §10.6 có câu mô tả mẫu *"…on marked street frames, surface detail is AI-assisted…"*. Theo §12.1, khung không còn được đánh dấu trên hình.
- §11.6 có câu "Video thử: 540p ≤ 15 MB", ngược với §12.5 "≤ 5 MB".
- Cả hai câu cần chủ dự án quyết lời mới (§8 mục 4).

## 4. Chính sách YouTube về nội dung bị thay đổi / tổng hợp (đọc 18/10/2026)
- **Trang:** "Disclosing use of GenAI content", https://support.google.com/youtube/answer/14328491?hl=en
- **Cách đọc:** đọc lúc 18/10/2026 ≈ 16:30 UTC, bằng WebFetch và một `curl`, HTTP 200. SHA-256 bản chữ đã tách: `cdb2e1902aa8d17b7aeef508c1faf9b2cdd8b34f162b5fccf3d00f5e6b6a1d7e`, lưu ở scratchpad, không vào repo vì là nội dung có bản quyền của Google. Trang không ghi ngày cập nhật.

**Trích nguyên văn (ngắn):**
1. "We require creators to disclose AI-generated or altered content that seems realistic. Creators can make this disclosure during the upload process."
2. Phải khai báo nội dung GenAI mà: "Alters footage of a real event or place." / "Generates a realistic scene that didn't actually occur." / "Makes a real person appear to say or do something they didn't do."
3. "Creators don't need to disclose non-realistic content that's made with AI, or edits to realistic content that are minor."
4. Ví dụ không cần khai báo: "Using an AI-generated or altered animation of a missile in a fully animated video"; "Video sharpening, upscaling or repair and voice or audio repair"; "Production assistance, like using generative AI tools to create or improve a video outline, script, thumbnail, title, or infographic".
5. Ví dụ phải khai báo: "AI generated extra footage of a real place, like a video of a surfer in Maui for a promotional travel video".
6. Cách khai báo: "In the Attributes section, under "AI use," tap Yes if your content meets the disclosure requirements or No if not."
7. Nơi hiện nhãn: "Labels may appear in the expanded description for non-music AI-generated audio or AI content that is non-photorealistic or animated."
8. Tự động: "YouTube may automatically apply an AI label … for: … Content that contains C2PA metadata" và "content containing C2PA metadata … can not be adjusted."
9. "Disclosing AI content alone won't limit a video's audience or impact its eligibility to earn money."

**Đánh giá cách làm §12.1** (nút khai báo + mô tả + thẻ phương pháp, không nhãn trên hình):
- **Đáp ứng chính sách.** Trang chỉ yêu cầu bật trường "AI use" trong YouTube Studio. Nhãn do YouTube gắn, trong mô tả mở rộng hoặc trên trình phát. Trang **không** yêu cầu người làm phim tự đặt nhãn trên hình. Mô tả, bình luận ghim và thẻ "How this film was made" đi xa hơn mức trang đòi hỏi.
- **Các điểm cần chủ dự án quyết.** P không sửa Kinh thánh.
  1. **T3 nên bật "AI use = Yes".** §12.1(c) viết "khi chính sách hiện hành yêu cầu". T3 có tấm C khung neo và vân HC7 do AI sửa, đặt trên một nơi có thật (Gibraltar), ở cảnh dựng 3D tầm mắt. Mức chân thực cao nên dễ rơi vào "Alters footage of a real event or place" / "realistic scene". Trang cũng ghi khai báo không giảm khán giả hay kiếm tiền. Vì vậy P đề xuất coi T3 là "chính sách yêu cầu" và bật **Yes**. Phục chế ảnh 1940s (§12.3) thuộc nhóm "sharpening, upscaling or repair", không cần khai báo riêng.
  2. **C2PA.** Ảnh OpenAI của PT2/PT3/PT4/V6 mang C2PA. Nếu tệp tải lên còn siêu dữ liệu C2PA, YouTube tự gắn nhãn và **không cho gỡ**. Nếu đã bật Yes theo điểm 1 thì việc này không gây hại. Dù vậy cần biết trước, và nên ghi trong thẻ phương pháp.
  3. **Từ T4, lời nhân chứng đọc bằng giọng tổng hợp (§12.3).** Trang buộc khai báo nội dung "Makes a real person appear to say or do something they didn't do". Đọc lời có thật bằng giọng tổng hợp có thể bị hiểu là người thật đang nói, nếu không ghi rõ. Đề xuất: ghi "voiced by a synthetic narrator, words from <nguồn>" trong thẻ phương pháp và bật Yes. Điểm này nên quyết trước G1 T4.

## 5. Sổ đã ghi (commit `a5b983ea`)
| Sổ | Nội dung |
|---|---|
| `COST-LEDGER.csv` | **Sửa dòng V1** (12/10): bọc nháy `ghi_chu`, từ 21 cột về 20. **Thêm 3 dòng:**<br>• **V6-01**: Claude **$5,202** (claude-sonnet-5-5, vượt mốc theo dõi $5), OpenAI **$0,0632**, giờ máy ≈ **7,5 h** đồng hồ + phiên con ≈ 8 h tiến trình, nguồn V6 §3<br>• **NC-AI-01**: OpenAI **$0,1608**; Claude để trống cột $ vì không có đồng hồ, `ghi_chu` ghi "ước > $3"; ≈ 0,3 h tính toán / 1,5 h đồng hồ; nguồn NC-AI §8<br>• **P-1810b**: đúng dòng đề xuất §5 của P-1810b<br>Kiểm bằng `csv`: **mọi dòng đúng 20 cột** |
| `RIGHTS.md` | **Đổi phạm vi 2 dòng cũ:**<br>• **P1810B-AI** (60 vân PT3 + tấm C PT2 + tấm C PT4): đổi sang "**dùng trên hình T3 theo Kinh thánh §11.3, §12**", gồm cả cách công bố §12.1<br>• **P1810-AI**: phần PT2 đổi; phần PT (vân nhánh B ×9, tấm C PT) **giữ chỉ nghiên cứu**, vì lệnh chỉ nêu PT2/PT3/PT4/V6<br>**Khối mới 8 dòng:**<br>• **P1810C-DRINK373**: Drinkwater 1786 tờ 373, PD, chỉ dữ kiện<br>• **P1810C-RIJKS**: RP-P-OB-19.249, CC0, chỉ tham chiếu<br>• **P1810C-PH-NOR**: pháp tuyến Poly Haven, CC0<br>• **P1810C-UNIF**: quân phục 1782 (Royal Warrant 1768, Reglamento 1768, Règlement 1779, Copley PD, Clonard PD); viền từng khối là minh hoạ<br>• **P1810C-HC7**: vân King's Bastion<br>• **P1810C-AI-V6**: tấm C 1943 lần 3; OpenAI Services Agreement §4.1; có C2PA<br>• **P1810C-SAM**: Apache-2.0, chỉ công cụ<br>• **P1810C-TESS**: Apache-2.0, chỉ công cụ |
| `AUTHORSHIP.md` | 8 dòng có giờ:<br>• **AI-A + AI-B** (20:14)<br>• **AI-T3 + AI-5 bỏ** (20:30)<br>• **NCAI-1…4** (20:57–20:59; NCAI-3 = B cổng mềm; NCAI-4 = AI-3 chỉ ảnh chụp, bỏ 2,5D ở T3)<br>• **V6-1…V6-7 + CHU-1 = A** (23:15)<br>• **V6-5 vật nền phụ**: bỏ 102 chậu cây 1943; giữ 13/40 mái che 1943; bỏ 1 mái che 1782; thêm bao cát, hòm, phuy 1943; thêm thùng vỡ và giỏ 1782<br>• **Q1–Q2 nguyên văn** (09:23): Q1 = ff main ← p-1810; Q2 = T8 Antwerp 1585 → Amsterdam (XANH, tạm)<br>• **C2-1…C2-9** (§8 mục 3)<br>• **VL1 = (a)**: KA2026, 5j +1,5 s, tổng 721,2 s |
| `channel-k2/HANG-DOI.md` | Mục mới "CẬP NHẬT 18/10/2026 tối (P-1810c)":<br>• **T3**: cổng chuẩn hình **ĐẠT** (V6; Claude điều phối chấm 23:10: thua 2, hoà 4) → **G1b**; chọn giọng series đang chạy (casting-giong)<br>• **T8**: Antwerp 1585 → Amsterdam, XANH tạm (Q2) |
| `reports/p-1810c/golden.json` | Số đo golden của phiên (§2.1) |

**Điểm P tự quyết hoặc chưa kiểm được:**
1. **C2-1…C2-9 nguyên văn:** lệnh ghi "= mục 'Việc' 1–9 lệnh V5b-2d (V5B2D-BAO-CAO.md §0 dẫn lệnh)". Nhưng §0 của báo cáo V5b-2d là bảng kết quả (P1–P6, C2-2/C2-7, C2-9, C2-4, C2-5), **không chép lệnh**. Commit V5b-2d cũng không chép. **P không tự viết lại.** AUTHORSHIP ghi rõ còn thiếu nguyên văn.
2. **NCAI-1…4:** P ánh xạ vào mục 1–4 của NC-AI §15. Ánh xạ này khớp với nội dung Kinh thánh §12.2–12.3 và được ghi rõ là "ánh xạ của P". Văn bản có hiệu lực là §12.
3. **V6-01, cột `tran_api_usd` = 5:** đây là mốc theo dõi, không phải trần cứng (§12.5). Điều này có ghi trong `ghi_chu`.
4. **VL1 = (a)** làm tổng 721,2 s, vượt trần 12 phút **0,17 %**. Chỉ số này nằm trong ±5 % (KHOA-LOI-41 §6 mục 1).
5. **RIGHTS:** SAM và Tesseract chỉ ghi giấy phép theo NC-AI §1. P không đọc lại tệp LICENSE vì phiên không cần mạng cho việc này. Nếu T3 thật sự dùng hai công cụ, phiên dùng nên chép nguyên văn LICENSE.

## 6. Nhánh đã đặt tên (chỉ tạo tên mới, không xoá nhánh cũ)
`git ls-remote` xác nhận hai tên chưa có trên origin, rồi chạy:
```text
git push origin eb852a30837343664ea6ad08cf0afb619c862e48:refs/heads/v6 \
                4bef98465a826c09bc0702302cdc4431a573629d:refs/heads/nc-ai
```
| Tên mới | Commit | Nhánh harness cũ (giữ nguyên) |
|---|---|---|
| `v6` | `eb852a30` (V6) | `ccr-0e3bf8dd-nst2mv` |
| `nc-ai` | `4bef9846` (NC-AI) | `ccr-fcb0e150-g16lfi` |

## 7. Chi phí
| Mục | Lệnh | Thực tế |
|---|---|---|
| Claude API (gọi từ script) | 0 | **$0** |
| OpenAI / ElevenLabs / YouTube Data API | 0 | **$0 / 0 ký tự / 0 đơn vị** |
| Web | WebFetch nếu cần | 1 WebFetch và 1 `curl` tới support.google.com, UA dự án, không email |
| Giờ máy | mốc 1,5 h | **≈ 0,3 h thời gian thực** (16:22 → 16:40 UTC). Tiến trình: golden 5,0 phút và selftest_ll 5,9 phút (song song), 7 selftest khác 1,1 phút, verify.sh ×2, pip/npm |
| Token | trần mềm | không đo được trong phiên |

**Chỉ số trong ±5 % quanh ngưỡng:**
- Golden SSIM so ngưỡng 0,90: t1 **0,9082** (+0,9 %), ll08 **0,9307** (+3,4 %), steel **0,9449** (+4,99 %).
- VL1 = (a): 721,2 s so trần 720 s (+0,17 %).
- Trong các sổ đã ghi:
  - V6 Claude **$5,202** so mốc $5 (+4,0 %), V6 tự nêu.
  - V6 `ai_texture` 19,5 % so trần 20 % (−2,5 %), V6 checks-appeal tự nêu.
  - NC-AI: các số trong §12 của báo cáo đó, ví dụ khớp nguyên khối 97,6 % so 95 %, SAM 0,690–0,725 so 0,7.

**Dòng đề xuất cho `COST-LEDGER.csv`** (ghi ở lần P kế): `P-1810c,Hợp nhất 18/10 tối (V6 + NC-AI) + Kinh thánh §12 + ghi sổ 18/10 tối,P,2026-10-18,,,,,0,0,không gọi API,0,0,0.3,,,,,reports/P-1810c-BAO-CAO.md §7,YouTube 0; OpenAI 0; giờ máy = thời gian thực; 1 WebFetch + 1 curl trang YouTube Help`.

## 8. Việc chờ chủ dự án
1. **Claude điều phối rà `p-1810c` rồi ff `main`.** `p-1810c` là hậu duệ thẳng của `origin/main` `6c16e548`: `git checkout main && git merge --ff-only origin/p-1810c && git push origin main`.
2. **Video 11 MB của V5b-2d trong git** (§2.3): chọn (a) ngoại lệ một lần, hoặc (b) `git rm` và giữ SHA. Nên quyết **trước khi ff main**, vì hook pre-push sẽ chặn dải commit này.
3. **Nguyên văn C2-1…C2-9** (9 mục "Việc" của lệnh V5b-2d): cần dán để P ghi đủ vào AUTHORSHIP.
4. **Kinh thánh:**
   - Rà cách P đánh dấu 12 câu (§3 d). Nếu chỉ muốn 5 chỗ §12.1 nêu tên thì bỏ cụm ở 7 câu.
   - Quyết lời mới cho câu mô tả mẫu §10.6 ("on marked street frames") và §11.6 "540p ≤ 15 MB", vì cả hai ngược §12.
5. **YouTube** (§4):
   - T3 bật "AI use = Yes" (P đề xuất Yes).
   - Ghi việc nhãn C2PA tự động không gỡ được.
   - Cách ghi lời nhân chứng bằng giọng tổng hợp từ T4.
6. **Golden:** SSIM đã sát ngưỡng sau V6. Xem sheet t1 và cân nhắc chụp lại tham chiếu golden theo trình dựng V6 (§2.1).
7. **T3 → G1b:** mức dựng SẢN XUẤT V6 + khung sạch §12.1. Chọn giọng series đang chạy (casting-giong, chưa merge, P không merge).
8. **Khiếu nại luật của V6** (`reports/v6/checks-appeal.md`, K-LAI-3…6 cho `ai_texture`; A4 khi không lời): giao phiên K. Khiếu nại cũng cần cập nhật theo §12.1, vì nhãn AI không còn trên hình nên luật K-LAI-2 "nhãn suốt shot" phải đổi.
9. **Còn treo từ P-1810b:** Open Parliament Licence nguyên văn trước G2; xác nhận ánh xạ K15-n, V2D-n và nội dung Q-PT4-4.
10. Ghi dòng `P-1810c` (§7) vào COST-LEDGER ở lần P kế.
