Nhánh thật: **`claude/p2610d-merge-k1179-bgul21`**. Harness buộc tên này; lệnh ghi `p-2610d`. Gốc `origin/main` @`5453a8b2`, đúng gốc lệnh. `main` được cập nhật bằng fast-forward lên đỉnh nhánh này (commit "… DỪNG chờ chủ dự án").

# P-2610d — gộp K-1.17.9 vào main, ghi quyết định K1179-D1…D7. BÁO CÁO. DỪNG chờ chủ dự án

## §0 Điều lệ phiên và tóm tắt
| Trường | Lệnh | Thực tế |
|---|---|---|
| Căn cứ | chủ dự án 26/10/2026 "Duyệt K1179-D1…D7 theo khuyến nghị điều phối"; giờ dán lệnh = giờ duyệt | **26/10/2026 13:02 Asia/Saigon** = 2026-10-26T06:02:14Z, giờ tạo phiên P-2610d (đọc từ `get_session`). Ghi chú: `TZ=Asia/Saigon date` trong container trả UTC (thiếu tzdata) — giờ Saigon tính UTC+7 bằng máy |
| Nhánh | `p-2610d` từ origin/main @5453a8b2 | harness buộc `claude/p2610d-merge-k1179-bgul21` (dòng đầu); gốc đúng **5453a8b2** (fetch 06:06 UTC) |
| Merge | origin/ccr-196e0bda-gcj9iw @a7dc969f, không squash, `--no-ff --no-commit` + preflight | đỉnh **a7dc969f** khớp; **0 xung đột**; preflight `--staged` "132 tệp — ĐẠT · lock KHỚP · PREFLIGHT ĐẠT" → commit merge **`6baeef25`** (cha 1 `5453a8b2`, cha 2 `a7dc969f`) |
| LOCK | sau merge `lock.py --verify` KHỚP 1.17.9 `9eddaf24…` | **KHỚP** `9eddaf24e8c5276b6017af172e7c8185ba21831a7b6e842cc17094fd5c66fc34` (trực tiếp sau merge trước commit; lại ở mọi preflight; lại trước ff main) |
| Selftest | selftest_k1179, kỳ vọng 50/50 | **50/50 đúng kỳ vọng**, rc 0, 0 SAI (`/opt/cine/bin/python -I checks/ll/selftest_k1179.py`; log `reports/p2610d/selftest_k1179.log`) |
| Song song BAN-CUOI-T4-B1 | không đụng `channel-k2/k2c-t4-02/ban-cuoi/**`, `design/`, `scripts/`, `tools/lfs-allow.txt`, `.gitattributes` | `git diff --name-only 5453a8b2 HEAD` trên các đường đó: **0 tệp**; không fetch, không đọc nhánh B1 |
| Vùng sửa | Kinh thánh, AUTHORSHIP, RIGHTS, COST-LEDGER, BAI-HOC-K2, QUYET-DINH-TREO, reports/p2610d/** (commit riêng ngoài merge) | đúng: `git diff --name-only 6baeef25 HEAD` chỉ có 5 tệp sổ/Kinh thánh + `reports/p2610d/**`. `checks/` + `checks-appeal.md` chỉ đổi qua merge (30 tệp, công việc của K), **0 tệp** ở commit của P. RIGHTS **không đổi** (K §13: không tài sản mới) |
| Chi phí | API 0; giờ máy ≤ 2 h | Claude API / OpenAI / Gemini / ElevenLabs / RunPod / YouTube **$0**, không gọi lần nào; 0 tác tử phụ; không tải LFS. Giờ máy ≈ **0,2 h** (06:02 → ≈ 06:16 UTC) |
| Preflight | `set -o pipefail`; chỉ commit khi có "— ĐẠT" | `reports/p2610d/cam_commit.sh` (`set -o pipefail`) chỉ commit khi có cả "— ĐẠT" và "PREFLIGHT ĐẠT"; hook pre-commit chạy lại |
| Hook | cài trước lần đẩy đầu | `pre-commit` + `pre-push` → `tools/preflight.sh`, cài 06:06 UTC; lần đẩy đầu ≈ 06:08 UTC |
| Force / amend | không | 0 force, 0 amend |
| Email / UA / khoá | che; không đưa email chủ dự án vào tệp | mọi commit `5453a8b2..HEAD` dùng noreply; tệp sổ và `reports/p2610d/**`: **0** chuỗi email chủ dự án. Phiên không gọi HTTP (không UA); không đọc, không in khoá |
| `lock.py` | chỉ `--verify` | chỉ `python3 -I checks/lock.py --verify` (trực tiếp và qua preflight) |
| Tiến trình nền | PGID, một vòng nặng, P ≤ 2, RAM ≥ 5 GB, đĩa | không có tiến trình nền (selftest chạy tiền cảnh). RAM trống 15 GB, đĩa trống 15 GB. Không dùng `pgrep -f`/`pkill -f` |
| Đẩy ≤ 30 phút + CHECKPOINT | bắt buộc | đẩy ≈ 06:08 (merge), 06:11 (sổ + Kinh thánh), ≈ 06:16 (báo cáo); `reports/p2610d/CHECKPOINT.md` |
| Đầu vào /var/tmp | không chỉ để ở đó | phiên không dùng /var/tmp; mọi tệp cần giữ trong git (`reports/p2610d/`) |
| Đã đọc | — | BAI-HOC-LL (khởi động), P2610C-BAO-CAO + CHECKPOINT (khuôn), K1179-BAO-CAO (đủ). Không đọc mã `checks/` (chỉ chạy selftest và lock) |

**Tóm tắt**
1. **Merge `--no-ff --no-commit`, 0 xung đột**, 132 tệp: `reports/k1179` 102, `checks/ll` 27, `checks/LOCK`, `checks/cinecheck`, `checks-appeal.md`. LOCK 1.17.9 KHỚP, selftest_k1179 **50/50** trước khi commit merge (§1).
2. **Kinh thánh `86daf2d5…` → `3df8c6e1…`** (+6 / −1): §13.6 (nhịp T4 D3; hàng kiểm 1.17.9 + **LOCK hiện hành 1.17.9**; cách khai 1.17.9), §15 (f) (miễn (k) không chân dung, D7), §15 (k) (toà có tên D4, ngoại lệ "bờ" D2 có khuôn khai, đẩy 2D D5, nước AI D6) (§2).
3. **Sổ** (chỉ thêm): AUTHORSHIP +7, COST-LEDGER +2 (K-1.17.9, P-2610d), BAI-HOC-K2 K101–K105, QUYET-DINH-TREO mục K (§3).
4. **Cộng sổ AI K bằng máy** (`reports/k1179/so-ai.jsonl`, 20 dòng): OpenAI 6 lệnh **$0,3132**, Claude 14 lệnh **$0,6991** — khớp báo cáo K và cộng sổ của điều phối.
5. **main `5453a8b2` → đỉnh nhánh** bằng fast-forward, sau khi fetch lại thấy main vẫn ở 5453a8b2; không force (§4).

## §1 Merge
| Nhánh @ SHA lệnh | Commit merge | Tệp | LOCK sau merge | Selftest |
|---|---|---|---|---|
| `origin/ccr-196e0bda-gcj9iw` @`a7dc969f` (đỉnh khớp; cha 2) | `6baeef25` (`--no-ff --no-commit` → lock `--verify` → selftest → preflight `--staged` "132 tệp — ĐẠT · PREFLIGHT ĐẠT" → `cam_commit.sh`) | 132 (+26 045 / −45): reports/k1179 102 · checks/ll 27 · checks/LOCK · checks/cinecheck/__init__.py · checks-appeal.md | **1.17.8 `045b7bb7…` → 1.17.9 `9eddaf24…` KHỚP** | **k1179 50/50** (KN-1 12 · KN-5 8 · KN-8 7 · KN-6 6 · KN-4 4 · KN-7 6 · KN-2 7) |

Ghi chú: các bộ selftest cũ (k112…k1178, k2, ll, cinecheck L1) không chạy lại — lệnh chỉ đòi selftest_k1179; K đã chạy đủ sau khoá (K1179 §5: 0 SAI).

## §2 Kinh thánh `docs/BIBLE-KENH2.md`
SHA trước `86daf2d5c14f8e27d1a7dae3dedb6c1bd3432dd1eb536ff3ecd605ee550320a3`, sau `3df8c6e15ea53845b1050c150b55b371c45199019d959344975220e8ff7ed033`. Sửa bằng `reports/p2610d/sua_bible.py` (chỉ chèn sau mốc, mỗi mốc kiểm đúng 1 lần); diff `reports/p2610d/bible-diff.txt`. Căn cứ ghi một dạng: **"(duyệt 26/10/2026 13:02 — giờ chủ dự án dán lệnh P-2610d sau khi trả lời "Duyệt K1179-D1…D7 theo khuyến nghị điều phối"; `reports/k1179/K1179-BAO-CAO.md` §12; K1179-Dx)"**.

| Chỗ | Đổi | Căn cứ |
|---|---|---|
| Dòng đầu | thêm mốc sửa P-2610d | — |
| §13.6 cập nhật 26/10 13:02 — nhịp T4 | Q37 cộng biến cố đo từ log máy (mặt trời 0°/−6°, pha máy), beats tự khai không nhận; đo v4: TB 5,04 s, **39 khoảng > 6 s = nhịp thật**. (1) **Q37 giữ Chặn ở G2**; (2) sửa nhịp ở khâu dựng **sau khi chủ dự án xem bản xem 1080p**: rút ngắn/cắt xen bằng khung đã dựng (không dựng lại) hoặc thêm biến cố CÓ NGHĨA (§13.2) ở shot chủ dự án chỉ ra; (3) **miễn có duyệt ≤ 3 shot "đứng có chủ ý"** (mỗi shot một dòng AUTHORSHIP); (4) K hiệu chuẩn BIEN-CO-V T4 trên master 1080p sau phiên B (K1178-D4 giữ) | K1179-D3 |
| §13.6 hàng kiểm theo 1.17.9 | **LOCK hiện hành 1.17.9 `9eddaf24…`** (thay 1.17.8); liệt kê hàng đổi (N2P-1/3 `ngoai_le`, N2P-E (k)(h)(u), Q37 log máy, NHAN-VAT-TEN `cat_clip` + miễn (k)); trỏ RULES-LL §1.17.9, không chép luật | K1179-D1 |
| §13.6 cách khai thêm từ 1.17.9 | theo K1179 §4: `ngoai_le`, `toa_co_ten[].loai`, `day_2d`, `nuoc_ai` + ghép bờ phía đất, `cat_clip`, `chan_dung: khong_co` … | K1179-D1 |
| §15 (f) cập nhật 26/10 13:02 | miễn (k) khi không có chân dung: 3 điều kiện 1.17.9 (khai nơi đã tra; YuNet mọi hộp ≥ 0,60 ≤ 1/8; `duyet_chu_du_an` trỏ dòng AUTHORSHIP cùng ngày-giờ-mã); miễn (k) không miễn (a). **H3-05b giữ**; tra thêm NPG, St Paul's, Commons, Historic England trước gói phát hành; H3-05c chỉ dự phòng; H1-15b `cat_clip` [0, 110] | K1179-D7 |
| §15 (k) cập nhật 26/10 13:02 | (1) **toà có tên** = tháp ≥ 75 m ODN + lịch sử có `nguon_lich_su` + St Paul's; Guildhall Art Gallery không tính nếu không có nguồn. (2) **ngoại lệ "bờ" duyệt** cho E-P9-ngay-l1 "tháp" (H5-05a), hộp [0.0, 0.96, 0.09, 1.0], khuôn K1179 §4 → nhánh "K bác → mặt nạ đủ" của cập nhật 10:08 hết hiệu lực. (3) **đẩy/trượt 2D ≤ 1,5 %/s** (một phép 2D cả khung, máy 3D CODINH; theo tờ so, duyệt ở phiếu bản cuối). (4) **nước AI** (`nuoc_ai`, bờ phía đất, duyệt từng tấm; sửa thuyền elip đen + bóng cầu AI lệch trước) → E-P1 có đường dùng | K1179-D1, D2, D4, D5, D6 |

Cần nêu: câu "E-P1 chưa dùng — chờ KN-8, KN-6" và "K bác → mặt nạ đủ" ở dòng (k) cập nhật 10:08 **không xoá** (Kinh thánh chỉ chèn dòng mới); dòng 13:02 ghi rõ phần nào hết hiệu lực.

## §3 Sổ
| Tệp | SHA trước → sau (16 ký tự) | Thêm | Nội dung |
|---|---|---|---|
| `AUTHORSHIP.md` | `2c15f834c7d6d0b0` → `a27a9b39d80536cb` | +7 | mỗi K1179-Dx một dòng: nguyên văn "Duyệt K1179-D1…D7 theo khuyến nghị điều phối", **giờ dán lệnh 13:02 (06:02:14Z) ghi làm giờ duyệt**, nghĩa đúng như lệnh; cột đóng góp của con người và phần AI đề xuất. Dòng D1 kèm **ghi chú giờ**: báo cáo K ghi giờ dán PHIẾU-A "≈ 10:12" theo giờ mở phiên K — giờ duyệt PHIẾU-A chính thức là **10:08** (dòng P-2610c); **không sửa dòng cũ** |
| `RIGHTS.md` | `52f7a1ffb14f33e7` (không đổi) | 0 | K1179 §13: không tài sản mới; fixture `checks/ll/fixtures/k1179/` là ảnh/clip/câu trả lời của dự án thu nhỏ, đã có trong RIGHTS, chỉ dùng kiểm |
| `COST-LEDGER.csv` | `1ed7cf36b76a106d` → `996245ec818a749b` (sau dòng K-1.17.9; dòng P-2610d thêm ở commit cuối) | +2 | **K-1.17.9**: dòng nguyên văn lệnh + ghi chú điều phối (dưới). **P-2610d**: API 0, ≈ 0,2 h |
| `channel-k2/BAI-HOC-K2.md` | `8cd434fdcfdbae43` → `492e2bd40a2854cb` | +9 | K101–K104 = 4 đề xuất K1179 §13 (đổi đề bài khi đổi lớp bảo vệ; `pkill -f <tên script>`; bờ phía đất; T9c không áp vùng AI vẽ lại); **K105** (điều phối): `pkill -f`/`pgrep -f` tự khớp chính lệnh đã lặp ≥ 6 lần (LL #24/#41/#112, K46, K54, K61, K75, K85, BAN-CUOI-T4-A §11 (12), K-1.17.9) dù đã có bài học → **chặn bằng công cụ, giao phiên Nền tảng** |
| `reports/k1173/QUYET-DINH-TREO.md` | `4b089de521904a17` → `a6f6b8f428b6c49d` | +27 (mục K cuối tệp) | Đã quyết K1179-D1…D7 (KN-1, KN-2, KN-4…KN-8 của mục J). Còn treo: **hiệu chuẩn BIEN-CO-V T4 trên master 1080p (sau B)**, **Đ5 quyền giọng G1**, **tra thêm chân dung Godfrey Allen**; kèm chọn shot nhịp D3, phiếu bản cuối D5/D6, chặn `pkill -f` bằng công cụ; giữ mục I/J |

SHA đầy đủ: `reports/p2610d/sha-truoc.txt`, `sha-sau.txt` (COST-LEDGER sau thật khác `sha-sau.txt` vì dòng P-2610d thêm ở commit cuối). Script ghi sổ: `reports/p2610d/ghi_so.py`.

**Dòng sổ đã ghi (COST-LEDGER, cột `ghi_chu`, nguyên văn lệnh):** `2026-10-26 · K-1.17.9 · OpenAI $0,313 · Claude API $0,699 · Gemini 0 · ≈ 1,9 h máy · tải LFS 1,79 GB` + ghi chú điều phối; các cột: `claude_api_usd` 0.699, `tran_api_usd` 8, `gio_render` 1.9, `cham_chu_du_an` 1.

**Kiểm bằng máy khi ghi sổ** (`reports/k1179/so-ai.jsonl`, 20 dòng, mọi dòng có `usd`):
| Nhà | Model | Lệnh | USD sổ | Báo cáo K | Khớp |
|---|---|---|---|---|---|
| OpenAI | gpt-6.1-sol | 6 | 0,3132 | 0,313 | ✓ |
| Anthropic | claude-sonnet-5-5 | 14 | 0,6991 | 0,699 | ✓ |

## §4 main
- Trước: `5453a8b271aa9a32e273884c60bbd2c85d7db610` (fetch lại ngay trước khi cập nhật: vẫn 5453a8b2).
- Sau: đỉnh nhánh `claude/p2610d-merge-k1179-bgul21` = commit "P-2610d: báo cáo … DỪNG chờ chủ dự án" (SHA ở `git log origin/main -1`; commit không tự chứa SHA của chính nó). Fast-forward, không force.

## §5 Chỉ số trong ±5 % quanh ngưỡng
Phiên này không đo chỉ số mới. Chép lại từ K1179 §9: **KN-6 đẩy 2D 1,505 %/s so ngưỡng 1,5 (+0,3 %)** — K thêm sai số đo 2 %.

## §6 Sự cố
- Không có. Ghi một chỗ cần biết: `TZ=Asia/Saigon date` trong container trả giờ UTC (thiếu tzdata) — giờ Saigon tính bằng UTC+7 (Python) và giờ tạo phiên từ `get_session`.

## §7 Việc chờ chủ dự án
1. **Duyệt báo cáo P-2610d** (merge K-1.17.9, Kinh thánh §13.6/§15 (f)(k), sổ).
2. **Sau phiên B:** xem bản xem 1080p T4 → chỉ shot thấy chậm (sửa nhịp theo D3) và chọn **≤ 3 shot "đứng có chủ ý"** được miễn.
3. **Phiếu bản cuối:** duyệt dùng đẩy 2D (D5) và từng tấm nước AI (D6) qua tờ so.
4. **Đ5 quyền giọng G1** (ElevenLabs) — vẫn chờ.
5. **Tra thêm chân dung Godfrey Allen** (NPG, St Paul's, Commons, Historic England) trước gói phát hành — giao phiên nào (B hay phiên phát hành).
6. **Phiên K sau B:** hiệu chuẩn BIEN-CO-V T4 trên master 1080p.
7. Đề xuất: giao **phiên Nền tảng** chặn `pkill -f`/`pgrep -f` bằng công cụ (BAI-HOC-K2 K105).
8. Lưu ý điều phối: phiên BAN-CUOI-T4-B1 (đang chạy song song) nên lấy luật 1.17.9 từ main mới trước khi chạy k2check bản cuối — P-2610d không đụng nhánh đó.

**DỪNG chờ chủ dự án.**
