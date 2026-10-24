Nhánh thật: **`claude/p-2410b-merge-lfs-3bti59`**. Harness buộc tên này; lệnh ghi `p-2410b`. Gốc `origin/main` @`2414d1d3`, đúng gốc lệnh. `main` được cập nhật bằng fast-forward lên đỉnh nhánh này (commit "… DỪNG chờ chủ dự án").

# P-2410b — gộp bộ kiểm 1.17.5 + nhánh giọng T4 vào main, master giọng T4 vào LFS, Kinh thánh theo K1175-D1…D7, sổ 24/10. BÁO CÁO. DỪNG chờ chủ dự án

## §0 Điều lệ phiên và tóm tắt
| Trường | Lệnh | Thực tế |
|---|---|---|
| Nhánh | `p-2410b` từ origin/main @2414d1d3 | harness buộc `claude/p-2410b-merge-lfs-3bti59` (dòng đầu); gốc đúng 2414d1d3 |
| Song song | ANIMATIC-T4 (`ccr-21ab5d6f-7l1yln`), THU-B-T4: không đụng | không fetch, không đọc, không sửa hai nhánh này |
| Vùng sửa | docs/BIBLE-KENH2.md, AUTHORSHIP.md, RIGHTS.md, COST-LEDGER.csv, channel-k2/BAI-HOC-K2.md, PLAN.md (chỉ D6), tools/lfs-allow.txt + .gitattributes (chỉ mẫu master T4), am-thanh/master/ (chỉ thêm 2 tệp), QUYET-DINH-TREO (chỉ mục cuối), reports/p2410b/**, main | đúng. Ngoài 2 merge, phiên đổi 13 tệp, tất cả trong vùng. Riêng `am-thanh/master/SHA256SUMS` có thêm 1 dòng chú thích ghi cỡ tệp, theo việc 2 của lệnh. Phiên không sửa `checks/` (chỉ đổi qua merge), `checks-appeal.md` (chỉ qua merge), `scripts/`, `design/`, các tệp khác của `channel-k2/k2c-t4-02`, `channel-k2/k2c-t3-01/**` hay nhánh khác |
| Chi phí | API 0; LFS ≈ cỡ 2 master; giờ máy mốc 2 h | Claude API / OpenAI / Gemini / ElevenLabs / RunPod / YouTube **$0**, không gọi lần nào. Tái tạo master gửi **0 ký tự** (cache trúng cả 8 lệnh). 0 subagent. LFS tải lên **157 MB** (98 029 582 + 59 258 364 byte). Giờ máy ≈ **0,6 h** (04:33 → ≈ 05:05 UTC) |
| Preflight | `set -o pipefail`; chỉ commit khi có "— ĐẠT" | `reports/p2410b/cam_commit.sh` chỉ commit khi có cả "— ĐẠT" và "PREFLIGHT ĐẠT"; hook pre-commit chạy lại. 4/4 commit thường ĐẠT. `--range 2414d1d3..HEAD` (286 tệp) ĐẠT |
| Hook | cài trước lần đẩy đầu | `pre-commit` + `pre-push` → `tools/preflight.sh`, cài 04:33 UTC; lần đẩy đầu 04:50 UTC |
| Force / amend | không | 0 force, 0 amend |
| Email / UA / khoá | che; UA CineLab; không in khoá | git dùng noreply. Diff `2414d1d3..HEAD` có **0** chuỗi email chủ dự án. Yêu cầu mạng ngoài git chỉ có 2 lần tải kiểm LFS qua media.githubusercontent.com, UA `CineLab-research (+https://github.com/HungQuach301/cine-lab)`. Phiên không đọc và không in khoá |
| `lock.py` | chỉ `--verify` | chỉ `python3 -I checks/lock.py --verify`; mọi lần đều **KHỚP 1.17.5 `c7630b4a…`** |
| Tiến trình nền | PGID, một vòng nặng một lúc, P ≤ 2, RAM ≥ 5 GB, kiểm đĩa | chỉ 1 tiến trình nền là `tai_tao.sh` (PGID 12981, ghi `tai_tao.pgid`), chạy sau khi selftest lượt 2 xong. RAM trống 13–15 GB; đĩa trống 16 GB. Selftest chạy tuần tự |
| Đẩy ≤ 30 phút + CHECKPOINT | bắt buộc | đẩy 04:50, 04:54 và lần cuối; `reports/p2410b/CHECKPOINT.md` |
| Đầu vào ở /var/tmp | không chỉ để ở đó | master tái tạo nằm ở `/var/tmp/cine-out/p2410b-tai-tao/`. Bản cần giữ đã vào LFS kèm SHA; gốc tái tạo được (13 mp3 + alignment) đã có trong git |
| Lệnh bổ sung | ghi vào CHECKPOINT | không có lệnh bổ sung nào trong phiên |
| Đã đọc | — | BAI-HOC-LL (khởi động), P2410-BAO-CAO (khuôn), K1175-BAO-CAO, GIONG-T4-BAO-CAO, PHIEU-GIONG, Kinh thánh §13, §15, QUYET-DINH-TREO, đầu RULES-LL mục 1.17.5. Không đọc mã trong `checks/` |

**Tóm tắt**
1. **2 merge `--no-ff`, 0 xung đột.** Đỉnh 2 nhánh trùng SHA lệnh. Sau merge (1), LOCK 1.17.4 → **1.17.5 `c7630b4a…` KHỚP**. Cả 3 lượt selftest đạt 14/14 bộ, **k1175 52/52** (§1).
2. **Master giọng T4 đã vào LFS.** Tái tạo bit-trùng bằng `tai_tao.sh` (0 ký tự): WAV `b9cec467…` OK, FLAC `e5d49871…` OK. `git lfs push` 2/2 (157 MB) trước khi đẩy nhánh. Tải lại từ máy chủ, SHA vẫn khớp (§2).
3. **Kinh thánh `13dc4641…` → `0ab7a06b…`:** §13.6 thêm cách khai 1.17.5; §15 (a) thêm D3; (b) thêm D1 và D4; (c)(iii) đổi chiều nước→đất sang T9c; (d) thêm ghi chú cập nhật; (j) cập nhật theo D5 + D7, vẫn ĐANG THỬ (§3).
4. **PLAN.md:** thêm quy ước D6 (§4).
5. **Sổ (chỉ thêm, xoá 0 dòng):** AUTHORSHIP +5, RIGHTS +1 mục (22 nguồn + 4 ghi chú), COST-LEDGER +3 (GIONG-T4, K-1.17.5, P-2410b), BAI-HOC-K2 K51–K58, QUYET-DINH-TREO mục E (§5).
6. **main `2414d1d3` → đỉnh nhánh** bằng fast-forward. Ngay trước khi đẩy đã fetch lại và kiểm main vẫn ở 2414d1d3; không force (§6).

## §1 Merge
| # | Nhánh @SHA (khớp lệnh) | Commit merge | Số tệp | Vùng | LOCK sau merge | selftest |
|---|---|---|---|---|---|---|
| 1 | `origin/checks-1-17-5` @`1dc8be60` | `96086e1e` | 168 (+5 208 / −22) | checks/ (16: LOCK, cinecheck, ll/ 14), reports/k1175 (151), checks-appeal.md (1) | **1.17.5 `c7630b4a6b8f4f8e7a2bcfc593b59e35df76e21ab404b0d532c595c2d06ea10a` KHỚP** | 14/14 bộ (`selftest-1.txt`) |
| 2 | `origin/claude/k2c-t4-02-giong-a24udn` @`5e5e02ce` | `455fd0de` | 99 (+19 019 / −0) | channel-k2/k2c-t4-02 (48: lời khoá, khoa-loi, am-thanh/nguon + nghe + master/SHA256SUMS + mốc câu), reports/giong-t4 (36), scripts/k2ldn/giong (15). Không chạm checks/ | KHỚP | 14/14 bộ (`selftest-2.txt`) |

Kết quả selftest, giống nhau ở cả 3 lượt (sau merge 1, sau merge 2, kiểm cuối `selftest-3.txt` @ae5f5d4d): k112 75/75 · k1121 48/48 · k1122 37/37 · k113 64/64 · k114 126/126 · k115 105/105 · k116 144/144 · k117 130/130 · k1172 74/74 · k1173 42/42 · **k1174 91/91** · **k1175 52/52** · **k2 129/129** · **ll 317/317**. Mọi bộ đều thoát mã 0.
Diff của 2 nhánh không có tệp LFS nào (`check-attr filter` = 0). LFS chỉ phát sinh ở việc 2.

## §2 LFS master giọng T4
| Bước | Kết quả |
|---|---|
| Mẫu | `tools/lfs-allow.txt` +4 dòng: 2 dòng chú thích "P-2410b (24/10/2026, chủ dự án duyệt 24/10 …)" + `channel-k2/k2c-t4-02/am-thanh/master/*.wav`, `…/*.flac`. `.gitattributes` gốc +3 dòng (chú thích + 2 mẫu `filter=lfs diff=lfs merge=lfs -text`). Mẫu đặt ở `.gitattributes` gốc, không tạo `.gitattributes` con, vì lệnh chỉ cho thêm đúng 2 tệp vào `am-thanh/master/`. `check-attr`: wav/flac = lfs; `T4-loi-moc.json`, `SHA256SUMS` = không |
| Tái tạo | `bash scripts/k2ldn/giong/tai_tao.sh /var/tmp/cine-out/p2410b-tai-tao` (PGID 12981, ≈ 1,5 phút). 8 lệnh thu đều "gửi 0" (cache theo băm từ `am-thanh/nguon/`), stem 680,76 s. Kiểm `sha256sum -c`: **`T4-loi-G1-v2-14LUFS.wav: OK`, `.flac: OK`**. Không ghi thêm dòng nào vào `reports/giong-t4/so-ai.jsonl` hay `bo-dem.jsonl` (`git status` sạch) |
| Tệp | `T4-loi-G1-v2-14LUFS.wav` SHA-256 `b9cec46777a02085561f0cdcfc858e5e8890d26382bd24b4bb8a6bcdb810200b`, **98 029 582 byte** · `T4-loi-G1-v2-14LUFS.flac` `e5d49871807109760622d03da7d77884b349fb913cb2aa6c5af48c5f8bacf273`, **59 258 364 byte** (cả hai < 2 GB/tệp, K30) |
| SHA256SUMS | Hai dòng SHA đã có sẵn (do GIONG-T4 ghi), nên phiên không thêm dòng SHA. Định dạng `sha256sum` không có cột cỡ, nên cỡ được thêm thành 1 dòng chú thích `#` (lệnh kiểm `grep -v "^#" SHA256SUMS \| sha256sum -c` vẫn OK 3/3) |
| Commit | `b398e921` (preflight ĐẠT; tệp > 5 MB nằm trong mẫu LFS cho phép) |
| `git lfs push` | `git lfs push origin claude/p-2410b-merge-lfs-3bti59` lúc 04:50:07 UTC: **"Uploading LFS objects: 100% (2/2), 157 MB"**, mã 0. Chạy **trước** `git push` nhánh (K33: hook preflight thay hook pre-push của LFS) |
| Kiểm máy chủ | tải lại cả 2 tệp qua `media.githubusercontent.com/media/HungQuach301/cine-lab/<nhánh>/…` (UA CineLab): SHA và cỡ **trùng** từng byte |

## §3 Kinh thánh `docs/BIBLE-KENH2.md`
- **SHA-256 trước:** `13dc4641bbcaabe9ab8e7d5681c91c86d04be11d810a646fadde660bc91cdcab` (main @2414d1d3).
- **SHA-256 sau:** `0ab7a06bc3c854c21fe13c7706ee0f919e914475f4f832110830c6dbc459677d` (commit `c905fe99`); +8 / −2 dòng. Diff đủ ở `reports/p2410b/bible-diff.txt`, script ở `reports/p2410b/sua_bible.py`. Trước khi thay, script kiểm mỗi chuỗi gốc xuất hiện đúng 1 lần. Mỗi đoạn mới ghi "(duyệt 24/10/2026, tin nhắn ngay trước lệnh P-2410b, "Duyệt K1175-D1…D7 theo khuyến nghị": K1175-Dx)". Lệnh không cho giờ chính xác của tin này, nên đoạn chỉ ghi ngày.

| Chỗ | Thay đổi |
|---|---|
| Tiêu đề | thêm "; sửa §13.6, §15 (a)(b)(c)(d)(j) theo K-1.17.5 (K1175-D1…D7) — 24/10/2026" |
| §13.6 | +1 dòng **"Cách khai thêm từ 1.17.5"** theo K1175 §7, chỉ trỏ tới RULES-LL mục 1.17.5 (LOCK `c7630b4a…`), không chép luật. Gồm: `n2p.tam[]` {id, shot, render, ghep, mat_na đúng độ phân giải, nam}; mặt nạ + tấm ghép + JSON vào git (D6); `song: {render_co, render_khong, nen}`; `khop_mau_cuc_bo: true`; BE-MAT-NHA `be_mat_nha_ai`, `mat_na_nha`, `mat_na_mat`, `bong`, `nha` [{id, lo, px_m}], lớp `nha_thuong` (215,215,215), `nen_ai`, `be_mat_nha_video {ghep, render, cach, tam}` |
| §15 (a) | +1 dòng **ngoại lệ D3**: khi khai `khop_mau_cuc_bo: true`, vòng bảo vệ = render-khớp + MỘT độ lệch màu/vật; lõi (a) vẫn 0/255; K kiểm N2P-1 (d). Ghi "thay V4 = b" |
| §15 (b) | +2 dòng: **D1** — phản chiếu chỉ từ render 3D; lệnh AI ghi rõ không vẽ phản chiếu; phản chiếu AI tự vẽ không được miễn. **D4** — lớp sống ghép bằng cộng hiệu clip(nền + (render có − không)); khai `song`; K kiểm N2P-1 (e) + (iv) soi `nen` |
| §15 (c) (iii) | sửa trong dòng: "đổi loại vùng T9b ≤ 2 % mỗi chiều" → "chiều đất→nước T9b ≤ 2 %, chiều nước→đất đo bằng **T9c** (… định nghĩa và ngưỡng ở RULES-LL 1.17.5 …)" |
| §15 (d) | +1 dòng ghi chú (lệnh không liệt kê, xem dưới) |
| §15 (j) | +1 dòng cập nhật: điều kiện (1) đã có (BE-MAT-NHA). AI chỉ phủ nhà ĐO ĐƯỢC (≥ 2 px/m và ≥ 40 điểm cạnh, chủ yếu khung trung/cận); nhà xa giữ render; toàn cảnh xa giữ render và nâng bằng 3D (D5 = A + D). Lời nhắc v2 có năm bắt buộc + q_thoi_dai (D7). **Vẫn ĐANG THỬ, CHƯA ÁP** tới khi THU-B-T4 đạt và chủ dự án duyệt. Chữ (j) cũ giữ nguyên |

**Chỗ lệch chữ lệnh (đã chọn cách ít rủi ro, cần chủ dự án xác nhận):**
- **§15 (d)** không có trong danh sách lệnh. Tuy vậy, dòng "(d) tiếp" (P-2410) vẫn ghi "phép (iii) giữ T9b ≤ 2 % mỗi chiều", "phản chiếu chờ khung đáp án", "1666 ngày chờ K-1.17.5". Các câu này nay trái với (a)(b)(c) mới. Tôi thêm 1 dòng ghi chú để trỏ sang (a)(b)(c) mới; chữ cũ giữ để còn lịch sử. Riêng việc **mở tấm nền cho cảnh 1666 ban ngày**, tôi chỉ ghi "chưa có quyết định — chờ chủ dự án (V1 giữ tới lúc đó)", không tự mở (§8 mục 3).

## §4 PLAN.md
+1 dòng ở "Luật làm việc", commit `c905fe99`: **Quy ước D6** (K1175-D6 = A). Mọi tấm N2+ và tấm BMN phải có mặt nạ ID + tấm ghép + JSON kiểm trong git, mỗi tệp nén ≤ 5 MB, commit ≤ 10 phút sau khi tấm về, không chỉ để ở `/var/tmp`. Gốc lớn hơn để ngoài git kèm SHA-256 + lệnh tái tạo. Có ghi lý do (K1175 §1, §12) và trỏ tới Kinh thánh §13.6. Các phần khác của PLAN.md không đổi.

## §5 Sổ (dòng thêm; 0 dòng cũ bị đổi)
Commit `ae5f5d4d`, script `reports/p2410b/ghi_so.py`. Script chỉ nối cuối tệp, đọc/ghi `newline=""`; dòng `\r` có sẵn trong COST-LEDGER vẫn còn đúng 1. Số cột mỗi dòng mới đã kiểm: AUTHORSHIP 6, RIGHTS 10, COST-LEDGER 20, BAI-HOC 5, QUYET-DINH-TREO 4. Diff sổ +82 / −0. Dòng COST-LEDGER P-2410b ghi ở commit cuối, sau khi đo giờ máy.

| Sổ | Dòng ghi |
|---|---|
| **AUTHORSHIP.md** (+5) | (1) **bổ sung giờ**: tin "Duyệt V1–V7 và K1174-D1…D6 theo khuyến nghị" lúc **24/10 06:42** (Asia/Saigon); dòng P-2410 giữ nguyên. (2) **Q1–Q7 đủ nội dung** (23/10 21:45): Q1 20–23 % ($25/$30 → nay $35/$30), Q2, **Q3 8 điểm tiết kiệm Omni**, **Q4** lượt đo $2–3, **Q5** GPU sau tờ look, **Q6** chủ dự án nạp Gemini, Q7. (3) **G-1…G-3** (24/10 08:31), nguyên văn "Duyệt G-1, G-2, G-3 theo khuyến nghị": G-1 = (c) K1-C1 730,1 s (7 câu bỏ, kể tên), G-2 = (a), G-3 = St Saviour's giữ bản gốc / Wenceslaus giữ / alias Evelyn "Eevlin"; kèm lời khoá v2 `645c0211…`. (4) **K1175-D1…D7**, nguyên văn "Duyệt K1175-D1…D7 theo khuyến nghị và lưu master giọng T4 vào LFS", nghĩa từng mục; **giờ không có trong lệnh** (ghi rõ). (5) **LFS** master giọng T4 (mẫu, SHA, cỡ, lfs push 2/2) |
| **RIGHTS.md** (+1 mục "T4 London — giọng (GIONG-T4) + bộ kiểm K-1.17.5") | **22 nguồn dữ kiện KIEM-LOI**: 20 trang tải về, mỗi trang 1 dòng `T4-GL-<mã>` (URL, bản chữ trong git, giờ đọc, SHA tệp gốc; "chỉ dùng dữ kiện, không chép câu chữ/hình"), cộng Pepys (#4167) và Evelyn (#42081) trỏ về N2P-T4-1/-2. **Giọng G1** theo P1910-G1, **vẫn chờ thư Đ5**: chỉ dùng cho animatic/nội bộ. Mô hình âm vị/ASR chỉ để đo. **K-1.17.5: 2 ảnh AI** `reports/k1175/ai/` (SHA), chỉ là khung đáp án kiểm, không vào phim. Không có NC/ND, nhạc, SFX hay font mới |
| **COST-LEDGER.csv** (+3, đủ 20 cột) | **GIONG-T4**: đúng dòng đề xuất §9; thêm vào cột nguồn tên nhánh @5e5e02ce + sổ AI, và vào ghi chú "giờ máy ≈ 1,2 h; duyệt G-1…G-3 08:31; ghi sổ bởi P-2410b". **K-1.17.5**: Claude API $0,497 (mốc $3), OpenAI $0,343, giờ máy 2,9 h, LFS 1,79 GB, tổng ≈ $0,84. **P-2410b**: $0, 0,6 h, ghi chú "**P-2410 giờ máy đo thật ≈ 0,6 h (sổ ghi 0,8 h)**" |
| **BAI-HOC-K2.md** (K51–K58) | K51–K53 = GIONG-T4 §9 (a)(b)(c): rút gọn câu trích, âm vị làm tai thứ hai, độ dài lời tính đủ ngừng + shot không lời. K54–K58 = K-1.17.5 §13 (1)–(5). **K54 ghi rõ "pkill -f khớp chính shell" — lặp lần 3**, kèm đề xuất chặn bằng công cụ. K55 stash checks/; K56 /var/tmp → D6; K57 mặt nạ đúng độ phân giải; K58 `view_layer.update()` |
| **QUYET-DINH-TREO.md** (mục E) | **Đã quyết:** G-1, G-2, G-3; K1175-D1…D7 (ánh xạ về K1175-a…e của mục D); LFS; giờ 06:42. **Còn treo:** THU-B-T4; phiên LOOK đo lại 24 tấm look2 bằng T9c + M1-rong-oai-l3h với khớp màu cục bộ; hiệu chuẩn lại BIEN-CO-V trên animatic T4; mở tấm nền 1666 ngày (V1); quyền giọng Đ5 |

## §6 main
- **Trước:** `2414d1d31a766973ab70cc50ffb463581a28e100`. Đã fetch lại ngay trước khi cập nhật: origin/main vẫn ở 2414d1d3.
- **Sau:** đỉnh nhánh (commit "P-2410b: báo cáo … DỪNG chờ chủ dự án"), đẩy bằng `git push origin HEAD:main`. Đây là fast-forward vì 2414d1d3 là tổ tiên; không force.
- Commit của phiên: `96086e1e` merge (1) · `455fd0de` merge (2) · `b398e921` LFS + CHECKPOINT · `c905fe99` Kinh thánh + PLAN · `ae5f5d4d` sổ · commit báo cáo cuối (+ dòng COST-LEDGER P-2410b, selftest-3, CHECKPOINT xong).

## §7 Chỉ số trong ±5 % quanh ngưỡng
Phiên này không đo phim. Các chỉ số sát ngưỡng trong hai phiên vừa gộp, nay đi vào main:
- Phim T4 theo **G-1 = K1-C1: 730,1 s** so mục tiêu 720 s (+1,4 %; Đ2 ≤ +5 %). Giữ lại câu nào trong 7 câu bỏ thì chỉ còn ≈ 26 s dư trước khi chạm trần 756 s.
- Loudness master giọng T4 **−14,1 LUFS**, dải −15,0…−13,8 (cách cận trên 0,3 LU); 3 bản nghe −14,2 LUFS (cách 0,4 LU).
- K-1.17.5: selftest BE-MAT-NHA nhà 20 dời 2,5 m — đỡ cạnh **0,44 so ngưỡng Cảnh báo 0,45 (−2,2 %)**, trên dữ liệu tổng hợp; τ0 = 6 cách điểm hỏng (5) một nấc lưới.

## §8 Việc chờ chủ dự án
1. **Giờ của tin "Duyệt K1175-D1…D7 … lưu master giọng T4 vào LFS"** (24/10): lệnh không cho giờ, nên AUTHORSHIP và Kinh thánh mới ghi ngày. Nếu cần, gửi giờ để phiên P sau thêm dòng bổ sung (như dòng 06:42).
2. **Xác nhận ghi chú §15 (d)** do P thêm để hết mâu thuẫn với (a)(b)(c) mới (§3).
3. **Mở tấm nền cho cảnh 1666 ban ngày?** V1 (24/10 06:42) cho "1666 ngày chờ K-1.17.5". Nay K-1.17.5 đã xong và D1–D4 đã duyệt, nhưng chưa có lệnh mở. Kinh thánh hiện giữ V1 (QUYET-DINH-TREO E, V1-1666).
4. **THU-B-T4** (đang chạy): kết quả vòng thử phủ bề mặt nhà và duyệt (§15 (j) điều kiện 2, 3). Phiên P sau sẽ merge khi xong.
5. **ANIMATIC-T4** (đang chạy, `ccr-21ab5d6f-7l1yln`): merge khi xong; hiệu chuẩn lại BIEN-CO-V trên animatic đó trước G2. Phía dựng lưu ý: độ dài theo G-1 (730,1 s, `GIAN-SHOT.md`); các thay đổi bảng shot ở GIONG-T4 §6 (đổi chỗ H1-11 ↔ H1-12, gán lại cột "Lời" ở Hồi 1 và Hồi 4, 3 M-d > 8 s, thẻ Pepys sang H1-05, H3-02 năm 1758, tách H5-05).
6. **Phiên LOOK:** đo lại 24 tấm look2 bằng T9c và đo lại M1-rong-oai-l3h với khớp màu cục bộ. Cần mặt nạ của họ, lưu theo D6.
7. **Quyền giọng G1 (Đ5):** vẫn chờ ElevenLabs; master T4 chỉ dùng cho animatic/nội bộ.
8. **Đề xuất (chưa làm, ngoài vùng):** `pkill -f` theo chuỗi đã giết shell ≥ 3 lần dù đã có luật chữ (K54). Đề nghị phiên Nền tảng chặn bằng công cụ, ví dụ một hàm `dung_pgid` trong `scripts/common/` và preflight cảnh báo `pkill -f` / `pgrep -f` trong tệp `.sh` mới. Cũng đề nghị preflight gọi thêm `git lfs pre-push` (K33) để đẩy nhánh LFS không cần nhớ bước tay.
