Nhánh thật: **`p-2410`** (đúng lệnh). Harness gợi ý `ccr-e75192a3-4tnvpq`, nhưng phiên không dùng nhánh đó; đẩy `p-2410` được chấp nhận. Gốc `origin/main` @`c6a4772b`, đúng gốc lệnh. `main` được cập nhật bằng fast-forward lên đỉnh nhánh này (commit "… DỪNG chờ chủ dự án").

# P-2410 — gộp vòng look T4 + bộ kiểm 1.17.4 vào main, Kinh thánh Look T4, sổ 23/10 21:45 → 24/10. BÁO CÁO. DỪNG chờ chủ dự án

## §0 Điều lệ phiên và tóm tắt
| Trường | Lệnh | Thực tế |
|---|---|---|
| Nhánh | `p-2410` từ origin/main @c6a4772b | đúng |
| Song song | K-1.17.5 (`checks-1-17-5`), GIONG-T4 (`k2c-t4-02-giong`): không đụng | không đọc, không sửa hai nhánh này. Lúc fetch (23:4x UTC) cả hai chưa có trên origin |
| Vùng sửa | docs/BIBLE-KENH2.md, AUTHORSHIP.md, RIGHTS.md, COST-LEDGER.csv, channel-k2/BAI-HOC-K2.md, channel-k2/k2c-t4-02/look/CHON-V2.json (mới), reports/k1173/QUYET-DINH-TREO.md (chỉ nối mục cuối), reports/p2410/**, main | đúng: 16 tệp ngoài 2 merge, đều nằm trong vùng. Phiên không sửa `checks/` (chỉ đổi qua merge), `checks-appeal.md`, `scripts/`, `design/`, `tools/`, `channel-k2/k2c-t3-01/**` hay nhánh khác |
| Chi phí | API/GPU 0; giờ máy mốc 2 h | Claude API / OpenAI / Gemini / ElevenLabs / RunPod / YouTube **$0**, không gọi lần nào; 0 subagent. Giờ máy ≈ **0,6 h** (≈ 23:40 → ≈ 00:15 UTC). COST-LEDGER ghi 0,8 h vì ước trước lúc xong; số đo thật là 0,6 h (§4) |
| Preflight | `set -o pipefail`, chỉ commit khi có "— ĐẠT" | `reports/p2410/cam_commit.sh` chạy `tools/preflight.sh --staged` với `pipefail` và chỉ commit khi có cả "— ĐẠT" lẫn "PREFLIGHT ĐẠT". Hook pre-commit chạy lại. 7/7 commit ĐẠT. `--range c6a4772b..HEAD` (335 tệp) ĐẠT |
| Hook | cài trước lần đẩy đầu | `pre-commit` và `pre-push` → `tools/preflight.sh`, cài 23:46 UTC; lần đẩy đầu ≈ 23:57 UTC |
| Force / amend | không | 0 force, 0 amend |
| Email / UA / khoá | che; không gửi email chủ dự án; không in khoá | git dùng noreply. Diff `c6a4772b..HEAD` có **0** chuỗi email chủ dự án. Phiên không gửi yêu cầu mạng nào ngoài git, không đọc và không in khoá |
| `lock.py` | chỉ `--verify` | chỉ `python3 -I checks/lock.py --verify`, mọi lần đều **KHỚP 1.17.4 `08486eb2…`** |
| Đẩy ≤ 30 phút + CHECKPOINT | bắt buộc | đẩy 23:57, 00:03, 00:07 UTC và lần cuối; `reports/p2410/CHECKPOINT.md` |
| Lệnh bổ sung | ghi vào CHECKPOINT | không có lệnh bổ sung nào trong phiên |
| Tiến trình nền | PGID, P ≤ 2 | không chạy vòng nặng nào; selftest chạy tuần tự ở tiền cảnh |
| Đã đọc | BAI-HOC-LL (khởi động); LOOK-T4-V2-BAO-CAO + PHIEU-LOOK-V2 + NGUON-CONG-TRINH; LOOK-T4-BAO-CAO (§0–§3, §6–§10) + PHIEU-LOOK + khoa.json; K1174-BAO-CAO; QUYET-DINH-TREO; Kinh thánh §11.4, §13–§15, §19; RIGHTS-NHAP mục F | — |

**Tóm tắt**
1. **2 merge `--no-ff`, 0 xung đột.** LOCK 1.17.3 → **1.17.4 `08486eb2…` KHỚP** từ sau merge (1). Cả 3 lượt selftest đều đạt 13/13 bộ, **k1174 91/91** (§1).
2. **`CHON-V2.json` mới:** ghi cột chọn của 8 hàng, ô 1080p, tệp máy V2 kèm SHA, V5 (P1 fov 36°) và V6 (sương σ 1/10 km) (§2).
3. **Kinh thánh `d229fd9d…` → `13dc4641…`:** thêm khối "Look T4" vào §14.7; sửa §11.4 (L6), §13.6 (nhịp đo trên video, hàng kiểm mới, cách khai), §14.2 (T4 không GPU) và §15 (d); thêm §15 (j) "Phủ bề mặt nhà thường bằng AI — ĐANG THỬ, CHƯA ÁP"; cập nhật §19 (ghi chú D5, luật 3) (§3).
4. **Sổ (chỉ thêm, xoá 0 dòng):** AUTHORSHIP +7, RIGHTS +1 mục (23 dòng), COST-LEDGER +4, BAI-HOC-K2 K40–K50, QUYET-DINH-TREO mục D (§4).
5. **main `c6a4772b` → đỉnh `p-2410`** bằng fast-forward. Trước khi đẩy đã kiểm main vẫn ở c6a4772b; không force (§5).

## §1 Merge
| # | Nhánh @SHA (đúng SHA lệnh) | Commit merge | Số tệp | Vùng | LOCK sau merge | selftest |
|---|---|---|---|---|---|---|
| 1 | `origin/checks-1-17-4` @`f4a3d9ca` | `def4ca1c` | 29 (+3 088 / −35) | checks/ (14: LOCK, cinecheck, ll/ 12), reports/k1174 (14), checks-appeal.md (1) | **1.17.4 `08486eb21dc55749115849e9691a4321458ecf8411e0562b141506f77227dd6d` KHỚP** | 13/13 bộ đạt (`selftest-1.txt`) |
| 2 | `origin/k2c-t4-02-look2` @`c4079595` (chứa `k2c-t4-02-look` @`5123bebf` — đã kiểm `merge-base --is-ancestor`) | `23be991e` | 290 (+88 364 / −13) | channel-k2/k2c-t4-02 (116), design/k2v/ldn (2), reports/look-t4 (69), reports/look-t4-v2 (65), scripts/k2ldn (38) — không chạm checks/ | KHỚP | 13/13 bộ đạt (`selftest-2.txt`) |

Kết quả selftest, giống nhau ở cả 3 lượt (sau merge 1, sau merge 2, kiểm cuối `selftest-3.txt`): k112 75/75 · k1121 48/48 · k1122 37/37 · k113 64/64 · k114 126/126 · k115 105/105 · k116 144/144 · k117 130/130 · k1172 74/74 · **k1173 42/42** · **k1174 91/91** · **k2 129/129** · **ll 317/317**. Mã thoát của mọi bộ đều 0.
Diff của 2 nhánh không có tệp LFS nào (`check-attr filter` = 0), nên không cần `git lfs push` (K33).

## §2 `channel-k2/k2c-t4-02/look/CHON-V2.json` (mới; SHA-256 `8560e7621cb07c5d180c01e20515d8819b6d1bf9367caf66d6c708c78f7cf769`)
Tệp sinh bằng `reports/p2410/tao_chon_v2.py` và có trong git: `.gitignore` của tập đã mở `look/**/*.json`, đã kiểm bằng `git check-ignore -v`.
| Hàng | Cột | Ô 1080p | Máy | Kiểu look | P1 → fov 36° |
|---|---|---|---|---|---|
| M1-rong | v2-3d | `reports/look-t4-v2/khung/M1-rong-v2-3d.jpg` | `look/may-v2/M1-rong.json` | A | có — `may-v2/M1-rong-hep.json` |
| M1-trung | v2-3d | `…/M1-trung-v2-3d.jpg` | `may-v2/M1-trung.json` | A | — |
| M2-ngay | v2-3d | `…/M2-ngay-v2-3d.jpg` | `may-v2/M2-ngay.json` | A + ấm C | **có, nhưng chưa có tệp máy fov 36°** (LOOK-T4-V2 chỉ dựng hẹp cho M1/M3/M4-rong) |
| M2-dem | v2-3d | `…/M2-dem-v2-3d.jpg` | `may-v2/M2-dem.json` | A + khói than B | — |
| M3-rong | v2-3d | `…/M3-rong-v2-3d.jpg` | `may-v2/M3-rong.json` | A + ấm C | có — `may-v2/M3-rong-hep.json` |
| M3-trung | v2-3d | `…/M3-trung-v2-3d.jpg` | `may-v2/M3-trung.json` | A + ấm C | — |
| M4-rong | **v2-openai** | `…/M4-rong-v2-openai.jpg` | `may-v2/M4-rong.json` + `tl-M4-rong.json`; tấm `ai/goc-v2/M4-rong-oai-l3-ai.jpg` (SHA trong tệp) | A | có — `may-v2/M4-rong-hep.json` |
| M4-trung | v2-3d | `…/M4-trung-v2-3d.jpg` | `may-v2/M4-trung.json` | A | — |
- **V5:** P1 `[532330, 180250, 230]` nhìn `[532420, 180980, 15]`, fov 50° → **36°**. **V6:** `look.haze[0]` = 1e-4 /m (σ 1/10 km) cho các khung A và C. M2-dem theo kiểu B nên giữ σ 1/6 km và lớp khói than σ 1/4,2 km, đúng như tệp máy.
- **Lưu ý (ghi trong tệp):** tấm nền M4-rong được làm và qua cổng ở fov 50°. Theo V5, bản sản xuất phải làm lại tấm ở fov 36° rồi qua lại cổng (i)–(v).

## §3 Kinh thánh `docs/BIBLE-KENH2.md`
- **SHA-256 trước:** `d229fd9dd8ec61f6c9b3931c8eabc397a76caceb515338b2c1214683e672d35f` (main @c6a4772b).
- **SHA-256 sau:** `13dc4641bbcaabe9ab8e7d5681c91c86d04be11d810a646fadde660bc91cdcab` (commit `150a3f69`); +19 / −2 dòng. Diff đầy đủ ở `reports/p2410/bible-diff.txt`, script ở `reports/p2410/sua_bible.py`. Trước khi thay, script kiểm mỗi chuỗi gốc xuất hiện đúng 1 lần. Mỗi đoạn mới có ghi "(duyệt <ngày giờ>)".

| Chỗ | Thay đổi |
|---|---|
| Tiêu đề | thêm "; Look T4 ở §14.7 + sửa §11.4, §13.6, §14.2, §15 (d), §19, thêm §15 (j) — 24/10/2026" |
| §11.4 | +1 dòng **ngoại lệ T4 (L6)**: lõi khối 1666 lấp ước lượng không tô tông khác; chỉ ghi ở thẻ phương pháp kèm % diện tích lấp (duyệt 23/10 23:27) |
| §13.6 | +3 dòng: (1) **từ T4 nhịp đo trên video** bằng BIEN-CO-V (θ 8/255, k 2), cộng vào Q37 (b)(c); không nhận biến cố tự khai; hiệu chuẩn lại trên animatic T4 trước G2 (K117-D8 17:42, Q7 21:45, K1174-D2 24/10); (2) **hàng kiểm mới** MAY-19, BAN-DO-12, TU-LIEU-10, AI-TU-LIEU, GEMINI-NGAN-SACH, GOC-CAO-60 — chỉ trỏ tới `checks/ll/RULES-LL.md` 1.17.4, không chép luật; K1174-D3…D6 = A; (3) **cách khai T4** theo K1174 §5 với `ngan_sach_gemini_usd: 35`, `ngan_sach_gemini_moc_usd: 30`, giữ `log_may` |
| §14.2 | +1 dòng: **T4 không dùng Cycles GPU**; lửa/khói mọi khung bằng cách A mới `look2.js` (L5 23:27; V2 = a 24/10) |
| §14.7 | + khối **"Look T4"** gồm LOOK-T4-1…7: A (LUT `k2c-t3-kenh-v030.cube`) + ấm kiểu C cho cháy ngày 1666 và toàn cảnh 1940 + khói than dày kiểu B cho đêm cháy 1666; lửa/khói `look2.js`; sương σ 1/10 km; **P1 fov 36°** (đọc lại tham số theo §19 (a) luật 3); `CHON-V2.json`; L2–L4 (bão hoà theo tập, người/xe khung trung, City 1940); "đồ chơi" còn mở → §15 (j) |
| §15 (d) | **viết lại cho T4** thành 2 dòng: bỏ trần cứng 20 % M-d; ngân sách Gemini/tập (T4 $35, mốc $30); tổng AI ≤ 70 %; góc cao ≥ 60 %; trần luật tấm nền 50 % giữ; T3 không hồi tố. Dòng tiếp: phép (iii) giữ 2 % (D11 = LỖI ẢNH, K1174-D1 = A); tấm nền chỉ OpenAI `gpt-image-2.5-sunburst-2026-09-08`, chỉ cảnh 2026 ban ngày; 1666 ngày chờ K-1.17.5 (V3 = a, V4 = b); đêm/lửa không dùng tấm nền; mục tiêu tấm nền animatic 5–15 % (thay mục tiêu 35–45 % lúc 23:45 và dòng "≤ 15 %" của D11 lúc 17:42) |
| §15 (j) (mới) | **"Phủ bề mặt nhà thường bằng AI — ĐANG THỬ, CHƯA ÁP"**: phạm vi B; điều kiện (1) phép kiểm K-1.17.5, (2) một vòng thử đạt, (3) chủ dự án duyệt; animatic không chờ vòng này (A) (duyệt 24/10 06:21) |
| §19 | +1 dòng sau ghi chú D5: "Cập nhật 24/10: T4 không dùng Cycles GPU … dòng D5 trên thay bằng dòng này"; luật (3) cho T4: P1 đọc lại từ `CHON-V2.json` (fov 36°) |

**Chỗ lệch chữ lệnh (đã chọn cách ít rủi ro, cần chủ dự án xác nhận):**
- Lệnh ghi "**§15 (g)**", nhưng §15 (g) đã có nội dung (lối mòn/đường đất, duyệt 21/10). Tôi đặt mục mới ở **§15 (j)**, chữ cái trống kế sau (i). Mục cũ giữ nguyên chữ cái, không bị đẩy số. Đã grep: không tệp nào trỏ tới "§15 (g)".
- §19 không có trong danh sách lệnh, nhưng ghi chú D5 trong §19 ("Cycles GPU chỉ 3–4 cận đêm") trái với L5/V2 đã duyệt. Tôi thêm một dòng cập nhật ngay dưới; dòng D5 cũ vẫn giữ để còn lịch sử.
- Ngân sách Gemini: K1174 §5 lấy ví dụ $30 / mốc $25 (Q1). Kinh thánh ghi **$35 / $30** đúng như lệnh (23:45). Khi khai episode.yaml T4 phải dùng $35/$30.
- Thêm L2–L4 (duyệt 23:27) vào khối Look T4. Lệnh không liệt kê mục này, nhưng nếu thiếu thì §14.4 "bão hoà ≥ 0,40" sẽ mâu thuẫn với look đã duyệt (khung ngày V2 đo được 0,14–0,27).

## §4 Sổ (dòng thêm; 0 dòng cũ bị đổi)
Commit `06fa7a78`, script `reports/p2410/ghi_so.py`. Script chỉ nối cuối tệp, đọc/ghi `newline=""`; dòng `\r` có sẵn trong COST-LEDGER vẫn còn đúng 1. Tổng diff +95 / −0.

| Sổ | Dòng ghi |
|---|---|
| **AUTHORSHIP.md** (+7) | (1) 23/10 21:45 "Duyệt Q1–Q7" (Q1, Q2, Q7 theo RULES-LL 1.17.4; **Q3–Q6 không có văn bản trong repo** nên chưa ghi nội dung); (2) 23/10 23:14 "Tôi chọn 1z 2z 3z 4z 5z 6z 7z 8z", giải mã: M1-rong A · M1-trung A · M2-ngay C · M2-dem B · M3-rong C · M3-trung A · M4-rong A · M4-trung C; (3) 23/10 23:27 look hợp nhất + L2–L6 (L5 = bỏ GPU, khác khuyến nghị (a) của phiếu, chủ dự án quyết sau khi xem clip M2); (4) 23/10 23:41 nhận xét 3 điểm; (5) 23/10 23:45 "1,2,3,4,5, đồng ý theo khuyến nghị / 6 tôi sẽ tự động nạp"; (6) 24/10 06:21 "1. Chọn phương án A+B theo khuyến nghị 2. Lấy cột theo khuyến nghị" (nghĩa A, B và các cột); (7) 24/10 "Duyệt V1–V7 và K1174-D1…D6 theo khuyến nghị" (nghĩa từng mục; **lệnh không cho giờ chính xác**). **XEM CÂM T3 7/8 đã có** (dòng 23/10 10:57, KHEP-T3 ghi) nên không ghi lại |
| **RIGHTS.md** (+1 mục) | "T4 London — look (LOOK-T4, LOOK-T4-V2)": **16 vân Poly Haven CC0** (mỗi lớp 1 dòng: trang, tác giả, SHA diff + nor; nguồn `channel-k2/k2c-t4-02/look/van-cc0.json` — lệnh ghi `design/k2v/ldn`, nhưng tệp thật nằm ở thư mục tập); **3 tư liệu Met CC0** 336039, 336038, 757299 (JSON nguyên văn ở `licenses/`, SHA theo `SHA256-TU-LIEU-LOOK.txt`; chỉ tham chiếu, không lên hình); **dữ kiện** Gutenberg #48491, #60008 (PD; SHA .txt), Wikipedia (chỉ số liệu/toạ độ, CC BY-SA, không chép văn bản), OSM ODbL r3374550, w369135772; tài sản tự tạo (LUT B/C, lightmap); **ảnh AI thử** OpenAI/Gemini chỉ là bản thử, chưa vào phim. Không có tài sản NC/ND |
| **COST-LEDGER.csv** (+4, đủ 20 cột) | LOOK-T4 ($0; ≈ 5,0 h); K-1.17.4 ($0; ≈ 2,5 h; LFS 1,79 GB); LOOK-T4-V2 (Gemini $0,42; OpenAI $2,80; **Claude API $6,02 vượt mốc $3** — lý do theo báo cáo §8: cổng (i)/(ii)/(iv) §15 (c) cần mô hình nhìn thứ hai, 36 lượt kiểm; RunPod $0,053; ≈ 2,4 h; tổng ≈ $9,29); P-2410 ($0; ghi 0,8 h, **đo thật ≈ 0,6 h** — sổ ghi trước khi xong, lệch ước +0,2 h, sửa ở phiên P sau nếu cần). Mọi số lấy từ báo cáo các phiên, không ước lại |
| **BAI-HOC-K2.md** (K40–K50) | K40 màu mặt nạ qua `s2l` (sự cố 3); K41 chú thích chèn giữa dòng, lặp LL #42/#76 (sự cố 4; ≥ 4 lần trong 3 phiên T4); K42 ảnh vào tấm nền còn vật chuyển động (8); K43 vật bán trong suốt dán nguyên điểm ảnh (9); K44 lỗi 3D cũ lộ khi đổi nền (10); K45 quầng vùng bảo vệ 3 px (11); K46–K49 = K-1.17.4 §12 mục 1–4; **K50 "tấm nền AI không chữa được phần thuộc lớp (a) — đo trước xem 'đồ chơi' nằm ở lớp nào rồi mới chọn công cụ"** |
| **QUYET-DINH-TREO.md** (mục D) | **Đã quyết:** K117-D8, K1173-D6 (17:42), D11 (phán quyết K-1.17.4), Q2 (21:45, 23:45), K1174-D1…D6 (24/10), V1–V7 (24/10), các dòng A còn lại (17:42). **Còn treo — K-1.17.5:** (a) khung đáp án D1; (b) (iii) sắc nước; (c) (i)/(iv) lớp sống; (d) vòng bảo vệ; (e) phép kiểm phủ bề mặt nhà; thêm: hiệu chuẩn lại BIEN-CO-V trên animatic T4 |

## §5 main
- **Trước:** `c6a4772bbe58ba33a29dbffa282411cb42f1a1ee`. Đã fetch lại ngay trước khi cập nhật: origin/main vẫn ở c6a4772b.
- **Sau:** đỉnh `p-2410` (commit "P-2410: báo cáo … DỪNG chờ chủ dự án"), đẩy bằng `git push origin p-2410:main`. Đây là fast-forward vì c6a4772b là tổ tiên; không force.
- Commit của phiên: `def4ca1c` merge (1) · `23be991e` merge (2) · `84783200` CHECKPOINT · `b93a44a5` CHON-V2 · `150a3f69` Kinh thánh · `06fa7a78` sổ · commit báo cáo cuối.

## §6 Chỉ số trong ±5 % quanh ngưỡng
Phiên này không đo phim. Các chỉ số dưới đây nằm sát ngưỡng trong các phiên vừa gộp và nay đi vào main:
- TU-LIEU-10 trên bảng shot T4 v1: **9,72 %** (ngưỡng 10 %, −2,8 %) — K1174 §10. Thêm thẻ hoặc tranh khắc là dễ vượt.
- Trời + sương ở P1 (LOOK-T4-V2): 20,0 / 20,0 / 19,7 / 20,3 % so với ≤ 20 % (0 … +1,5 %). **Khi P1 đổi sang fov 36° (V5), tỷ lệ trời sẽ đổi và phải đo lại.**
- (iii) M4-rong-oai-l3 trong hộp: 2,17 % so với ≤ 2 % (+8,5 %, ngoài ±5 %). Tấm này đạt theo số toàn khung (0,89 %). Nêu ở đây vì đây là ô duy nhất được chọn làm cột AI.
- OpenAI LOOK-T4-V2: $2,80 so với mốc $3 (−6,8 %, ngoài ±5 %; ghi để rõ).

## §7 Sự cố
| # | Sự cố | Xử lý |
|---|---|---|
| 1 | Lần đầu `git fetch origin` mọi nhánh mất > 2 phút (repo nhiều nhánh) | chờ fetch xong, rồi kiểm SHA từng nhánh: đúng hết |
| 2 | Lượt đầu `sua_bible.py` có một biến thừa và câu L3 thiếu "≤ 60 m" | khôi phục tệp bằng `git checkout`, sửa script, chạy lại từ bản gốc trước khi commit (SHA ghi ở §3 là của lượt chạy lại) |
| 3 | COST-LEDGER ghi giờ máy P-2410 = 0,8 h (ước trước khi xong); đo thật ≈ 0,6 h | ghi ở §0, §4; không sửa dòng đã commit |
Không force-push, không amend; không có lỗi nào lặp lại.

## §8 Việc chờ chủ dự án
1. **Xác nhận giờ** của tin "Duyệt V1–V7 và K1174-D1…D6 theo khuyến nghị" (24/10). AUTHORSHIP hiện ghi "tin nhắn ngay trước lệnh P-2410; giờ chính xác không có trong lệnh".
2. **Xác nhận đặt mục phủ bề mặt nhà ở §15 (j)** thay vì (g), vì (g) đã là mục lối mòn (§3).
3. **Q3–Q6 (21:45):** văn bản đề xuất không có trong repo nên AUTHORSHIP chỉ ghi Q1, Q2, Q7. Nếu cần hồ sơ đủ, xin gửi lại nội dung Q3–Q6.
4. **Kết quả K-1.17.5** (đang chạy): khung đáp án D1, (iii) sắc nước, (i)/(iv) lớp sống, vòng bảo vệ, phép kiểm phủ bề mặt nhà (QUYET-DINH-TREO mục D). Sau đó phiên P sẽ merge `checks-1-17-5`. Ghi chú: LOOK-T4-V2 §12.3 đề nghị P chuyển khiếu nại (iii)/(i)/(iv) qua `checks-appeal.md`; lệnh này cấm sửa tệp đó, nên các khiếu nại chỉ được giao K-1.17.5 qua QUYET-DINH-TREO mục D.
5. **GIONG-T4** (`k2c-t4-02-giong`): merge khi phiên đó xong và chủ dự án duyệt.
6. **Phương án A — animatic T4 bằng look V2:** cần lệnh mở phiên. Phía dựng lưu ý: (a) P1 fov 36° (V5) — M2-ngay chưa có tệp máy fov 36°, và tấm nền M4-rong phải làm lại ở fov 36° rồi qua lại cổng (≈ $0,30/lượt OpenAI gồm kiểm theo LOOK-T4-V2 §3); (b) tỷ lệ trời + sương ở P1 phải đo lại sau khi đổi fov; (c) khai episode.yaml theo Kinh thánh §13.6 ($35/$30, `log_may` mỗi shot); (d) Monument ở P1 vẫn TRƯỢT ≥ 12 px (7/10 px, bị toà 2026 che) và tháp góc White Tower còn mờ (LOOK-T4-V2 §1). Hai điểm này còn mở, chưa có quyết định.
7. **Phương án B — vòng thử phủ bề mặt nhà:** mở sau khi K-1.17.5 có phép kiểm (§15 (j)).
8. (Đề xuất, chưa làm) Tạo `channel-k2/k2c-t4-02/LOOK-KHOA.md` giống T3, kèm SHA, để khoá thông số look T4 cho phiên dựng. Hiện `CHON-V2.json` và tệp máy `may-v2/` đang làm vai trò này.
