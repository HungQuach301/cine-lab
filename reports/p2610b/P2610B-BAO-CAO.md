Nhánh thật: **`claude/merge-k1178-to-main-ij62my`**. Harness buộc tên này; lệnh ghi `p-2610b`. Gốc `origin/main` @`e97fc214`, đúng gốc lệnh. `main` được cập nhật bằng fast-forward lên đỉnh nhánh này (commit "… DỪNG chờ chủ dự án").

# P-2610b — gộp K-1.17.8 vào main, Kinh thánh theo K1178-D1…D6 và phiếu xem v2, sổ. BÁO CÁO. DỪNG chờ chủ dự án

## §0 Điều lệ phiên và tóm tắt
| Trường | Lệnh | Thực tế |
|---|---|---|
| Nhánh | `p-2610b` từ origin/main @e97fc214 | harness buộc `claude/merge-k1178-to-main-ij62my` (ghi ở dòng đầu); gốc đúng e97fc214 |
| Song song | BAN-CUOI-T4-A: không đụng vùng của nó | không fetch, không đọc, không sửa nhánh của BAN-CUOI-T4-A; không đụng `channel-k2/k2c-t4-02/**`, `scripts/`, `design/`, `tools/` |
| Vùng sửa | Kinh thánh, AUTHORSHIP, RIGHTS, COST-LEDGER, BAI-HOC-K2, QUYET-DINH-TREO (chỉ thêm mục cuối), reports/p2610b/**, main | đúng. Các commit riêng của phiên (sau merge `710bacaf`) chỉ đổi 6 tệp sổ/Kinh thánh + `reports/p2610b/**` (`git diff --name-only 710bacaf HEAD`). `checks/` (19 tệp), `checks-appeal.md` (1), `reports/k1178/` (71) chỉ đổi qua merge. QUYET-DINH-TREO: chỉ thêm mục I ở cuối (+31, −0) |
| Chi phí | API 0; giờ máy mốc 1 h | Claude API / OpenAI / Gemini / ElevenLabs / RunPod / YouTube **$0**, không gọi lần nào. 0 tác tử phụ. Không tải LFS. Giờ máy ≈ **0,4 h** (23:28 → ≈ 23:52 UTC 25/10), phần lớn là 1 lượt selftest |
| Preflight | `set -o pipefail`; chỉ commit khi có "— ĐẠT" | `reports/p2610b/cam_commit.sh` (`set -o pipefail`) chỉ commit khi có cả "— ĐẠT" và "PREFLIGHT ĐẠT"; hook pre-commit chạy lại. **Merge dùng `--no-ff --no-commit`**, preflight `--staged` trên 91 tệp đã stage ("— ĐẠT · lock KHỚP · PREFLIGHT ĐẠT") rồi mới commit (bài học P-2610 → K92) |
| Hook | cài trước lần đẩy đầu | `pre-commit` + `pre-push` → `tools/preflight.sh`, cài 23:31 UTC; lần đẩy đầu 23:38 UTC |
| Force / amend | không | 0 force, 0 amend |
| Email / UA / khoá | che; không đưa email chủ dự án vào tệp | git dùng noreply (mọi commit trong `e97fc214..HEAD`). Diff `e97fc214..HEAD` có **0** chuỗi email chủ dự án. Phiên không gọi HTTP nên không có UA; không đọc, không in khoá |
| `lock.py` | chỉ `--verify` | chỉ `python3 -I checks/lock.py --verify` (trực tiếp, trong selftest và qua preflight). Mọi lần **KHỚP 1.17.8 `045b7bb7…`** |
| Tiến trình nền | PGID, một vòng nặng một lúc, P ≤ 2, RAM ≥ 5 GB, kiểm đĩa | selftest chạy bằng `setsid nohup` (PGID 1493), chờ bằng cách đọc tệp kết quả, không `pgrep/pkill -f`. Một lượt nặng duy nhất. RAM trống 15 GB, đĩa trống 15 GB |
| Đẩy ≤ 30 phút + CHECKPOINT | bắt buộc | đẩy 23:38, lần cuối ≈ 23:52; `reports/p2610b/CHECKPOINT.md` |
| Đầu vào ở /var/tmp | không chỉ để ở đó | phiên không tạo tệp ở /var/tmp. Bản Kinh thánh trước sửa chép ra scratchpad chỉ để chạy lại script; SHA trước ở `sha-truoc.txt` |
| Lệnh bổ sung | ghi vào CHECKPOINT | không có |
| Đã đọc | — | BAI-HOC-LL (khởi động), P2610-BAO-CAO (khuôn), K1178-BAO-CAO (đủ), PHIEU-XEM-V2 mục A1/B/C, `reports/k1178/so-ai.jsonl` (đọc bằng máy), RULES-LL dòng tiêu đề + NHAN-VAT-TEN (văn bản luật, không phải mã), Kinh thánh §6, §13, §14.7, §15, §17, §19, RIGHTS mục NC-T4 footage + ANIMATIC-T4-V2, QUYET-DINH-TREO mục H. Không đọc mã trong `checks/` |

**Tóm tắt**
1. **Merge `--no-ff --no-commit`, 0 xung đột.** Đỉnh trùng SHA lệnh (`297eb070`). Preflight trên phần stage ĐẠT rồi mới commit (`710bacaf`). Sau merge **LOCK 1.17.8 `045b7bb7…` KHỚP**; selftest **17/17 bộ checks/ll rc 0**, trong đó **k1178 69/69**, k1177 87/87, k2 129/129, ll 317/317 (§1).
2. **Kinh thánh `a4d1c3fd…` → `fbac59d9…`** (+14 / −1 dòng: 11 dòng chèn + dòng đầu). Ghi K1178-D1…D6 và phiếu xem v2 A1/B/C1–C9b, trỏ tới RULES-LL 1.17.8, không chép luật. **§15 (k): điều kiện (1) đã có** (LUẬT E khoá ở 1.17.8, hàng N2P-E); **còn điều kiện (2) thử 2 khung** (§2).
3. **Sổ (chỉ thêm; RIGHTS gạch 1 câu chờ + nối 1 đầu bảng theo lệnh "bỏ mục chờ"):** AUTHORSHIP +2, RIGHTS +18/−2, COST-LEDGER +2 (K-1.17.8, P-2610b), BAI-HOC-K2 K87–K93, QUYET-DINH-TREO mục I (§3).
4. **Kiểm tiền bằng máy:** sổ AI K-1.17.8 60/60 dòng có `usd`; OpenAI **$0,8551**, Claude **$1,4187** — khớp báo cáo K và phép cộng của điều phối (0,2268 + 0,6283 + 0,7052 + 0,7135 = $2,2738). SHA 3 ảnh đáp án E trong git khớp `sha_ra` của sổ (§3).
5. **Phát hiện:** H3-05b (Godfrey Allen) được chủ dự án duyệt ở A1 nhưng không có chân dung tham chiếu → hàng NHAN-VAT-TEN (k) vẫn **Chặn ở G2**; duyệt A1 không thay trường này. Đã ghi "còn treo" (§6).
6. **main `e97fc214` → đỉnh nhánh** bằng fast-forward, sau khi fetch lại thấy main vẫn ở e97fc214; không force (§4).

## §1 Merge
| Nhánh @ SHA lệnh | Commit merge | Tệp | LOCK sau merge | selftest |
|---|---|---|---|---|
| `origin/claude/k1178-t4-london-rules-pdjfmz` @`297eb070` (đỉnh khớp; cha 2 của merge) | `710bacaf` (`--no-ff --no-commit` → preflight `--staged` "91 tệp — ĐẠT · lock KHỚP · PREFLIGHT ĐẠT" → `cam_commit.sh`) | 91 (+17 177 / −65): checks/ 19 (LOCK, cinecheck, ll 17), checks-appeal.md 1, reports/k1178 71 | **1.17.7 → 1.17.8 `045b7bb7414364d4732fe22c4b643ae04d7a0e19ae25f0e839de149379d3185a` KHỚP** | `selftest-1.txt`: 17/17 bộ rc 0 (k112 75 · k1121 48 · k1122 37 · k113 64 · k114 126 · k115 105 · k116 144 · k117 130 · k1172 74 · k1173 42 · k1174 91 · k1175 52 · k1176 62 · k1177 87 · **k1178 69/69** · k2 129 · ll 317), `== tổng rc=0` |

Ghi chú: commit `3a3a9a54` (đẩy 23:38) chứa `selftest-1.txt` **chưa xong** (16/17 bộ; `selftest_ll` còn chạy). Bản đủ, có `selftest_ll` và dòng tổng, vào commit báo cáo cuối. Không ảnh hưởng merge (merge đã qua preflight + lock trước đó).

## §2 Kinh thánh `docs/BIBLE-KENH2.md`
SHA trước `a4d1c3fd61cb5fdf206ea85a30767bbc6edfe14ef8af2ffd1d7dc40bfc759ce1`, sau `fbac59d9bac49e13daf56886e8f6eeb3e730287711cb753b129ad895537b3cfe`. Sửa bằng `reports/p2610b/sua_bible.py` (chỉ chèn sau mốc, mỗi mốc kiểm đúng 1 lần); diff ở `reports/p2610b/bible-diff.txt`. Mọi chỗ trỏ luật ghi "`checks/ll/RULES-LL.md` mục 1.17.8 (LOCK 1.17.8 `045b7bb7…`; Kinh thánh không chép luật)". Hai dạng căn cứ: **"(duyệt 26/10/2026 00:12, "Duyệt phiếu xem v2 theo khuyến nghị")"** và **"(duyệt 26/10/2026 06:28 — giờ chủ dự án dán lệnh P-2610b sau khi trả lời điều phối "K1178-D1…D6 theo khuyến nghị"; Dx = A)"**. 06:28 Asia/Saigon = 2026-10-25T23:28:07Z, giờ tạo phiên P-2610b (đọc từ `get_session`), tức giờ dán lệnh.

| Chỗ | Đổi | Căn cứ |
|---|---|---|
| Dòng đầu | thêm mốc sửa P-2610b | — |
| §6 | bản xem gửi chủ dự án từ bản cuối T4: 5–6 phần, ≤ 5 MB/phần, âm ≥ 128 kb/s | C5 = (b), 00:12 |
| §13.4 | bổ sung: XEM CÂM Q2/Q3/Q4/Q6 chấm trên bản cuối (cổng XEM-CAM ở G2) | B, 00:12 |
| §13.6 (dòng BIEN-CO-V) | cập nhật: hiệu chuẩn T4 không đạt → BIEN-CO-V T4 chỉ Cảnh báo, Q37 không cộng biến cố đo, phía dựng khai beats đủ | D4 = A |
| §13.6 hàng kiểm | **hàng 1.17.8**: N2P-E; K-LAI-3 mức nen; Q34 loại T4; Q26b T4 KHÔNG ÁP; SACH-1 khuôn khoảng + vai §17 (5); Q37 (d) miễn thẻ PP; TU-LIEU-OMNI ghép liền < 1 s 3D sạch, đếm clip M-d gần nhất; BIEN-CO-V T4 chỉ Cảnh báo — trả lời C7 | D1 = A; C7 |
| §13.6 cách khai | cách khai 1.17.8: `vung` từng shot (khu nội dung, không dùng `noi`), `log_chu` khoảng, `tu_lieu_lan`, `ngoai_le_duyet` cho mức nen; tấm E theo K1178 §4 | D1, D6 = A |
| §14.7 LOOK-T4-9 | cập nhật: C3 — 4° chỉ đưa vòm lên ≈ 20–21 %; animatic giữ 4°; **bản cuối thử dời điểm đứng P1 sang tây 60–80 m**; C9b — M04 +0,5 EV ở bản cuối; **mở lạnh dùng góc lửa khác shot M03** | C3 = (a)+(c), C9b = (b), ý thêm; 00:12 |
| §15 (d) | cập nhật: (1) C1 — 6 clip điểm nhấn (H1-06x, H1-15x, H2-02b, H2-06b, H2-09x, H2-10b) thử lại ≤ 2 lượt ở bản cuối, lệnh theo lỗi đo, ảnh đầu từ render 3D cùng năm, không nới luật kiểm; (2) H1-06b ngoại lệ ở animatic, bản cuối 720p kiểm lại, còn đọc ra chữ → sinh lại ≤ 2 lượt hoặc 3D | C1 = (b), 00:12; D5 = A |
| §15 (f) | cập nhật — **A1**: H1-05a ✓; H1-15b ✓ (bản cuối cắt khung mặt ≤ 1/8); H3-05b ✓ (Godfrey Allen, khung xa, không chân dung — duyệt theo từng clip, câu "chỉ thẻ chữ" giữ cho mọi trường hợp khác) | A1, 00:12 |
| §15 (k) | cập nhật: **điều kiện (1) đã có** (N2P-E, 1.17.8); **còn điều kiện (2) thử 2 khung** (đáp án K chỉ có P9-2026); báo nhầm bờ sông giữ Chặn, ngoại lệ vào phiếu cùng khung E, B để phiên K sau; (f2) tháp bịa Cảnh báo; tấm nền P1-2026 mới (H5-04) ở bản cuối | D1, D2, D3 = A; C4 = (b) |
| §17 | thêm (5): log chữ theo vai (`year`, `the_chuong`, `the_phuong_phap`, `where`, `the_nhan_vat`, `bo_dem_so`, `chu_thich_tu_lieu`); khuôn khoảng và cách đo SACH-1 trỏ RULES-LL 1.17.8; **thẻ Pepys/James chỉ chữ** | D1 = A; C6 = (a) |
| §19 (c) | thêm "(c) cập nhật 26/10 00:12": bản cuối tự tải lại ảnh gốc IWM D 6418 (bản gốc Commons 600×800; không tải từ trang IWM vì điều khoản phi thương mại); **bỏ footage đêm 2026 ở T4** (câu P7 "1 clip footage đêm H5-07a" không dùng) → không cần PDF Pexels/Pixabay | C2, 00:12 |

Không thêm luật mới: mọi dòng hoặc ghi lựa chọn của chủ dự án, hoặc trỏ tới RULES-LL 1.17.8. Hai chỗ cần nêu rõ:
- **C3 thay một phần LOOK-T4-9.** LOOK-T4-9 ghi "giữ điểm đứng". Phiếu v2 C3 (c) lại cho bản cuối thử dời điểm đứng. Dòng cập nhật ghi rõ phần thay chỉ áp cho lượt thử này.
- **IWM D 6418.** C2 viết "ảnh gốc IWM D 6418". QUYET-DINH-TREO mục H đã ghi chỉ tải bản Commons 600×800, không tải từ trang IWM vì điều khoản phi thương mại. Kinh thánh và RIGHTS ghi theo hướng an toàn này.

## §3 Sổ
| Tệp | SHA trước → sau (16 ký tự) | Thêm | Nội dung |
|---|---|---|---|
| `AUTHORSHIP.md` | `7f12290cc6cfb066` → `d5ced1b24b6b70e5` | +2 | (1) phiếu xem v2, 26/10 00:12, nguyên văn "Duyệt phiếu xem v2 theo khuyến nghị" + nghĩa A1/B/C1–C9b + ý thêm mở lạnh; (2) K1178-D1…D6, nguyên văn "K1178-D1…D6 theo khuyến nghị", **giờ dán lệnh 06:28 ghi làm giờ duyệt**, nghĩa D1–D6. Mỗi dòng có đóng góp biểu đạt của con người và phần AI đề xuất |
| `RIGHTS.md` | `b9ad9a12442ad3d1` → `96ebbe5a32cfa799` | +18 / −2 | Mục mới "K-1.17.8 và phiếu xem v2". **3 ảnh đáp án E** `reports/k1178/do/e/ai/*.jpg`: OpenAI gpt-image-2.5 từ render V2 P9-2026 của dự án; **chỉ dùng kiểm, không vào sản phẩm** (Không/Không/Không). Ảnh "xau" có nhãn hiệu bên thứ ba do mô hình vẽ. SHA khớp `sha_ra` của sổ. **Bỏ mục chờ PDF footage Pexels/Pixabay (C2):** câu "Nếu bản cuối dùng footage… phải lưu PDF" gạch và ghi lý do (2 dòng −: câu đó và đầu bảng footage, nay nối "BỎ ở T4"). D 6418: phiên bản cuối tự tải bản gốc Commons |
| `COST-LEDGER.csv` | `70347fb218f30d60` → `75fb9b856ea301d4` (sau dòng K-1.17.8; dòng P-2610b thêm ở commit cuối) | +2 | **K-1.17.8**: Claude $1,419, OpenAI $0,855, Gemini 0, ≈ 2,5 h, LFS 1,79 GB. **P-2610b**: API 0, ≈ 0,4 h |
| `channel-k2/BAI-HOC-K2.md` | `6446285ce35231e1` → `50cba6e43da420b6` | +11 | K87–K91 = 5 đề xuất K1178 §14 (đối chứng "đọc đủ ảnh"; `(cache or {})`; mô hình ảnh vẫn vẽ xe/người → N2P-4; giữ animatic đủ bitrate cho hiệu chuẩn; preflight `checks/` trước `lock.py`) · **K92** = merge commit không chạy hook pre-commit → `--no-commit` + preflight (P-2610 → áp ở P-2610b) · **K93** = K86 đóng (sổ q_thoi_dai 1.17.8 có usage + usd 26/26) |
| `reports/k1173/QUYET-DINH-TREO.md` | `2e2547b531c56efc` → `c54ce3eb73580d65` | +31 (chỉ mục I cuối tệp) | Đã quyết: phiếu v2 (A1, C1–C7, C9b, mở lạnh), K1178-D1…D6; từ mục H → xong: K-1.17.8, xung đột K-LAI-3 ↔ KIEM-2-MUC, PDF footage, IWM D 6418, sổ q_thoi_dai (phía K). Còn treo: thử 2 khung E, PHIẾU-A của BAN-CUOI-T4-A, XEM CÂM Q2/Q3/Q4/Q6 trên bản cuối, Đ5, **H3-05b ↔ NHAN-VAT-TEN (k)** (phát hiện), các mục giữ từ G/H |

SHA đầy đủ: `reports/p2610b/sha-truoc.txt`, `sha-sau.txt`. Dòng P-2610b của COST-LEDGER thêm ở commit cuối, nên SHA sau thật của COST-LEDGER khác `sha-sau.txt`.

**Kiểm bằng máy khi ghi sổ** (đối chiếu số tự khai), `reports/k1178/so-ai.jsonl` 60 dòng, 0 dòng thiếu `usd`:
| Nhà / model / lệnh | Lệnh gọi | USD |
|---|---|---|
| OpenAI gpt-image-2.5 (`/v1/images/edits`) | 3 | 0,2268 |
| OpenAI gpt-6.1-sol, PROMPT_E v1 / v2 | 6 / 6 | 0,3218 / 0,3065 (= 0,6283) |
| Anthropic claude-sonnet-5-5, PROMPT_E v1 / v2 / đối chứng n2p-v1 | 12 / 6 / 1 | 0,2376 / 0,4024 / 0,0652 (= 0,7052) |
| Anthropic claude-sonnet-5-5, q_thoi_dai O2 | 26 | 0,7135 |
| **Tổng** | 60 | **OpenAI 0,8551 · Claude 1,4187** = 2,2738 |

Khớp K1178 §11 ($0,855 / $1,419) và khớp phép cộng của điều phối. SHA 3 tệp `do/e/ai/*.jpg` (`sha256sum`) khớp `output.sha256` của 3 dòng ảnh trong sổ.

## §4 main
- Trước khi đẩy: `git fetch origin main` → `origin/main` = **`e97fc214`**, vẫn đúng gốc lệnh.
- Đẩy `HEAD:main` fast-forward `e97fc214 → <đỉnh nhánh>` (commit "… DỪNG chờ chủ dự án"). Không force; pre-push preflight ĐẠT. SHA đỉnh ghi trong thông điệp phiên.

## §5 Chỉ số trong ±5 % quanh ngưỡng (luật cứng)
Phiên này không đo chỉ số phim mới. Các chỉ số sát ngưỡng đã được K1178 §10 nêu tên, chép lại, không đổi:
- T4 v2 (bản xem, 1.17.8): TL-1 (d) H1-18a 2,06 / 2 %/s (+3 %); Q37 (1.13) khung tĩnh 5,96 / 6 s @11:22 và @11:28 (−0,7 %); Q26b-K2 nửa đầu đúng 3 loại (= ngưỡng); thẻ chương 5 × 3,0 / 3 s; thẻ PP1 9,0 s / PP2 7,0 s so 10 s; A1 −15,2 LUFS (cận dưới −15).
- Hiệu chuẩn BIEN-CO-V: R cắt nửa sau 97,9 / 95 % (+3 %).

## §6 Việc chờ chủ dự án
1. **Thử 2 khung E** (điều kiện (2) của §15 (k)): giao phiên nào, khung nào. Đáp án K mới có P9-2026; P1-2026 cần render V2 mới theo hướng máy C3/C4. Báo nhầm bờ sông (D2) sẽ vào phiếu cùng khung E để chủ dự án duyệt.
2. **PHIẾU-A của BAN-CUOI-T4-A** (phiên song song). P merge bản cuối khi chủ dự án duyệt.
3. **XEM CÂM Q2/Q3/Q4/Q6**: chủ dự án chấm trên bản cuối (cổng XEM-CAM ở G2).
4. **H3-05b ↔ NHAN-VAT-TEN (k)** (phát hiện của P-2610b): clip đã duyệt ở A1 nhưng không có chân dung tham chiếu, nên hàng NHAN-VAT-TEN vẫn Chặn ở G2. Chủ dự án chọn một trong ba hướng: (a) phía dựng ghi khiếu nại `checks-appeal.md` cho phiên K sau (ví dụ nhân vật không chân dung ở khung xa thì miễn (k) khi có dòng duyệt AUTHORSHIP); (b) bỏ khai nhân vật có tên cho clip này, chỉ dùng thẻ chữ, nếu luật cho phép; (c) thay clip.
5. **Đ5** quyền phát hành giọng G1.
6. Giữ từ mục G/H: ảnh thật hiện đại (B), đo lại BMN, ảnh Blitz Crown, LUAN-2/LOOK-T9c/KN THU-B → appeal, đề xuất K85 (phiên Nền tảng chặn `pgrep -f` bằng công cụ).

**DỪNG chờ chủ dự án.**
