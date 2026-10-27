Nhánh thật: **`claude/bold-goodall-xi0iw0`**. Harness buộc tên này; lệnh ghi `p-2710`. Gốc `origin/main` @`75e94b98`, đúng gốc lệnh. `main` được cập nhật bằng fast-forward lên đỉnh nhánh này (commit "… DỪNG chờ chủ dự án").

# P-2710 — gộp BAN-CUOI-T4-B1 vào main, ghi quyết định D-B1 + B1-Q1…Q5. BÁO CÁO. DỪNG chờ chủ dự án

## §0 Điều lệ phiên và tóm tắt
| Trường | Lệnh | Thực tế |
|---|---|---|
| Căn cứ | chủ dự án 27/10/2026 "Duyệt B1-Q1…Q5 theo khuyến nghị điều phối"; giờ dán lệnh = giờ duyệt | **27/10/2026 07:24 Asia/Saigon** = 2026-10-27T00:24:07Z, giờ tạo phiên P-2710 (đọc từ `get_session`). `TZ=Asia/Saigon date` trong container vẫn trả UTC (thiếu tzdata) — giờ Saigon = UTC+7 |
| Nhánh | `p-2710` từ origin/main @75e94b98 | harness buộc `claude/bold-goodall-xi0iw0` (dòng đầu); gốc đúng **75e94b98** (fetch 00:32 UTC) |
| Merge | origin/claude/k2c-t4-02-final-b1-t9ekhx @6f6c2636, không squash, `--no-ff --no-commit` + preflight | đỉnh **6f6c2636** khớp; **0 xung đột**; preflight `--staged` "271 tệp — ĐẠT · lock KHỚP · PREFLIGHT ĐẠT" → commit merge **`58685e04`** (cha 1 `75e94b98`, cha 2 `6f6c2636`) |
| LOCK | sau merge `lock.py --verify` KHỚP 1.17.9 `9eddaf24…` | **KHỚP** `9eddaf24e8c5276b6017af172e7c8185ba21831a7b6e842cc17094fd5c66fc34` (ngay sau merge trước commit; lại ở mọi preflight; lại trước ff main). Merge không đổi tệp nào trong `checks/` hay `checks-appeal.md` (0 tệp) |
| LFS | `git lfs ls-files` có đủ 27 tệp `channel-k2/k2c-t4-02/ban-cuoi/dung/*-1080p.mp4` (con trỏ) | **27/27** — danh sách đầy đủ (OID SHA-256 + đường dẫn) ở `reports/p2710/lfs-1080p.txt`; OID khớp cột SHA256 của bảng B1 §2 (16 ký tự đầu, 27/27). Merge chạy với `GIT_LFS_SKIP_SMUDGE=1` — không tải nội dung |
| Song song BAN-CUOI-T4-B2a | không đụng `ban-cuoi/**`, `scripts/`, `design/` | `git diff --name-only 58685e04 HEAD` trên `checks/`, `checks-appeal.md`, `channel-k2/k2c-t4-02/**`, `scripts/`, `design/`, `tools/`, `.gitattributes`: **0 tệp**. Các đường đó chỉ đổi qua merge (công việc của B1). Không fetch, không đọc nhánh B2a |
| Vùng sửa | Kinh thánh, AUTHORSHIP, RIGHTS, COST-LEDGER, BAI-HOC-K2, QUYET-DINH-TREO, reports/p2710/** (commit riêng ngoài merge) | đúng: `git diff --name-only 58685e04 HEAD` chỉ có 6 tệp sổ/Kinh thánh + `reports/p2710/**` |
| Chi phí | API 0; giờ máy ≤ 2 h | Claude API / OpenAI / Gemini / ElevenLabs / RunPod / YouTube **$0**, không gọi lần nào; 0 tác tử phụ. Giờ máy ≈ **0,2 h** (00:24 → ≈ 00:40 UTC) |
| Preflight | `set -o pipefail`; chỉ commit khi có "— ĐẠT" | `reports/p2710/cam_commit.sh` (`set -o pipefail`) chỉ commit khi có cả "— ĐẠT" và "PREFLIGHT ĐẠT"; hook pre-commit chạy lại |
| Hook | cài trước lần đẩy đầu | `pre-commit` + `pre-push` → `tools/preflight.sh`, cài 00:32 UTC; lần đẩy đầu ≈ 00:34 UTC |
| Force / amend | không | 0 force, 0 amend |
| Email / UA / khoá | che; không đưa email chủ dự án vào tệp | mọi commit `75e94b98..HEAD` (77) dùng noreply; tệp sổ, Kinh thánh và `reports/p2710/**`: **0** chuỗi email chủ dự án. Phiên không gọi HTTP ngoài git (không UA); không đọc, không in khoá |
| `lock.py` | chỉ `--verify` | chỉ `checks/lock.py --verify` (trực tiếp và qua preflight) |
| Tiến trình nền | PGID, một vòng nặng, P ≤ 2, RAM ≥ 5 GB, đĩa | không có tiến trình nền. RAM trống 15 GB, đĩa trống 15 GB. Không dùng `pgrep -f`/`pkill -f` |
| Đẩy ≤ 30 phút + CHECKPOINT | bắt buộc | đẩy ≈ 00:34 (merge), 00:37 (sổ + Kinh thánh), ≈ 00:40 (báo cáo); `reports/p2710/CHECKPOINT.md` |
| Đầu vào /var/tmp | không chỉ để ở đó | phiên không dùng /var/tmp; mọi tệp cần giữ đều trong git (`reports/p2710/`) |
| Đã đọc | — | BAI-HOC-LL (khởi động), P2610D-BAO-CAO + CHECKPOINT (khuôn), BAN-CUOI-T4-B1-BAO-CAO (đủ), sổ AI B1 (đọc bằng máy). Không đọc mã `checks/` |
| `verify.sh` | đầu phiên | 10 PASS, 5 FAIL (OpenEXR, three.js, tifffile/pyshp, k2v node_modules, Freesound 403 tuỳ chọn) — thiếu gói môi trường, phiên này không dựng nên không cần; **phiên B2a/B2b/B3 phải cài trước khi dựng** (lệnh cài in trong `verify.sh`) |

**Tóm tắt**
1. **Merge `--no-ff --no-commit`, 0 xung đột**, 271 tệp (+79 493 dòng): `channel-k2/k2c-t4-02/ban-cuoi/**` 204, `reports/ban-cuoi-t4-b1/**` 50, `scripts/k2ldn/bc/` 14, `design/k2v/ldn/bc/look3-b1.js`, `.gitattributes`, `tools/lfs-allow.txt` (D-B1). LOCK 1.17.9 KHỚP; 27/27 con trỏ LFS (§1).
2. **Kinh thánh `3df8c6e1…` → `22c6889d…`** (+6 / −1): §14.7 Look T4 (trang dựng `bc/look3-b1.js`, LFS D-B1, B1-Q1/Q2/Q4/Q5), §15 (k) (B1-Q3), §19 (d) (lịch xây từng phần + mặt cắt dâng + soi năm biên; niên đại toà hiện đại) (§2).
3. **Sổ** (chỉ thêm): AUTHORSHIP +6, RIGHTS +16 (mục B1), COST-LEDGER +2 (B1, P-2710), BAI-HOC-K2 K106–K112, QUYET-DINH-TREO mục L (§3).
4. **Cộng sổ AI B1 bằng máy:** Gemini, OpenAI khớp báo cáo; **Claude: 9/32 dòng thiếu `usd`** → ghi "≥ $0,806" (§3).
5. **main `75e94b98` → đỉnh nhánh** bằng fast-forward, sau khi fetch lại thấy main vẫn ở 75e94b98; không force (§4).

## §1 Merge
| Nhánh @ SHA lệnh | Commit merge | Tệp | LOCK sau merge | LFS |
|---|---|---|---|---|
| `origin/claude/k2c-t4-02-final-b1-t9ekhx` @`6f6c2636` (đỉnh khớp; cha 2) | `58685e04` (`--no-ff --no-commit` → lock `--verify` → `git lfs ls-files` → preflight `--staged` "271 tệp — ĐẠT · PREFLIGHT ĐẠT" → `cam_commit.sh`) | 271 (+79 493 / −0) | **1.17.9 `9eddaf24…` KHỚP** (không đổi; B1 không sửa `checks/`) | **27/27** `ban-cuoi/dung/*-1080p.mp4` là con trỏ LFS (H1 19 tệp, H3 7 tệp + H3-05c) — `reports/p2710/lfs-1080p.txt` |

Ghi chú: B1 chạy k2check 1.17.8 (LOCK của nhánh gốc 5453a8b2); main nay ở 1.17.9 — phiên B2a/B2b/B3 chạy k2check 1.17.9 từ main.

## §2 Kinh thánh `docs/BIBLE-KENH2.md`
SHA trước `3df8c6e15ea53845b1050c150b55b371c45199019d959344975220e8ff7ed033`, sau `22c6889d7d10cc2963de8d6cc09b4d07dffa60d6fbbb91473914a1ec36d46ba8`. Sửa bằng `reports/p2710/sua_bible.py` (chỉ chèn sau mốc, mỗi mốc kiểm đúng 1 lần); diff `reports/p2710/bible-diff.txt`. Căn cứ ghi một dạng: **"(duyệt 27/10/2026 07:24 — giờ chủ dự án dán lệnh P-2710 sau khi trả lời "Duyệt B1-Q1…Q5 theo khuyến nghị điều phối"; B1 §9 + lệnh P-2710; …)"**; D-B1 ghi "(duyệt 26/10/2026 10:42 — giờ dán lệnh BAN-CUOI-T4-B1 (03:41:56Z) …)".

| Chỗ | Đổi | Căn cứ |
|---|---|---|
| Dòng đầu | thêm mốc sửa P-2710 | — |
| §14.7 Look T4 — dòng mới "trang dựng hiện hành và LFS" | (1) **trang dựng hiện hành `design/k2v/ldn/bc/look3-b1.js`** (cờ d, spp 4, 1080p24; sinh từ `thu-b/look3.js` + sửa D-A4 (i)–(iv)) + hình học `scripts/k2ldn/bc/hinh_hoc_b1.py`; B2a/B2b/B3 dựng bằng trang này. (2) **LFS bản dựng trung gian** đúng một mẫu `ban-cuoi/dung/*-1080p.mp4` (H.264 CRF 16, chưa LUT/lớp chồng; SHA256SUMS; `git lfs push` sau mỗi shot) — ngoại lệ có duyệt cho "chỉ master phát hành vào LFS" (§11.6, §12.5) | D-B1 (26/10 10:42); B1 §1–§2 |
| §14.7 Look T4 — dòng mới "B1-Q1, Q2, Q4, Q5" | (1) M00 (P1b) + H1-01h máy ≈ 160 m, H1-01h dựng lại 72 khung + M00 ở B2a, giữ hướng/VONG/giờ P1b (D-A8). (2) chia B2a / B2b / B3, ≤ 12 h/phiên. (3) H3-03: B2b lấp khối nhà thời kỳ ngoài City (OSM, nhà Victoria, không công trình có tên mới, ghi "ước lượng") + dựng lại 227 khung; không đạt → MAP3D cả shot (tính trần bản đồ §19 (b)). (4) H1-01h/H1-02h (tối) + H1-13a/H1-13c (quầng) chấp nhận ở bản dựng, chỉnh ở màu/ghép B3, chủ dự án chấm lại trên bản xem 1080p (vòng K1179-D3) | B1-Q1, Q2, Q4, Q5 |
| §15 (k) — dòng mới 27/10 07:24 | H5-02b, H5-02s: Omni 2 lượt trượt sau sửa niên đại → **giữ 3D + ảnh thật H5-02t; không thêm lượt Omni**; bảng shot không đổi | B1-Q3 |
| §19 (d) — dòng mới "lịch xây từng phần" | quy tắc **mọc bằng mặt cắt dâng** (không bóp dẹt); lịch: St Paul's thân 1675,5 → 1697, trống 1697 → 1705, mặt tây 1702 → 1708, **vỏ vòm 1707,3 → 1708,0**, **đèn lồng 1707,95 → 1708,0**; Monument bệ 1671 → 1672,5, **thân 1672,5 → 1675,5, 20 rãnh**, đầu cột 1675,5 → 1676,5, **bầu 1676,5 → 1677,0**; **soi năm biên** (năm đầu/cuối + 1675/1708,0/1709,5/1711, mặt nạ 2 + q_thoi_dai `--lop-moc`, sổ có `usd`); kết quả B1 20/24 ĐẠT, 4 ghi | D-A4 (i) (26/10 10:08); B1 §1 (i) |
| §19 (d) — dòng mới "niên đại toà hiện đại" | **năm xuất hiện = năm hoàn thành − 2,5**; bảng năm có nguồn; **Barbican 1973–1976** (Estate thiếu năm 1965–1976); London Wall thiếu năm 1985–2020; vùng bom 1940 → khối tiền nhiệm 1953–1961; bỏ luật ép > 120 m về ≥ 1995; **loại trừ công trình lịch sử có tên khỏi quy tắc vùng**; 323 toà đổi năm | D-A4 (vi), Q-A5 = (a) (26/10 10:08); B1 §1 (vi) |

Cần nêu: các dòng cũ không xoá (Kinh thánh chỉ chèn dòng mới). Dòng LOOK-T4-9 cập nhật 10:08 (2) "M00 dùng P1b" vẫn hiệu lực; dòng mới chỉ đổi độ cao máy (B1-Q1). Ở mục K của QUYET-DINH-TREO và §13.6, "sau phiên B" nay hiểu là **sau B3** (B1-Q2).

## §3 Sổ
| Tệp | SHA trước → sau (16 ký tự) | Thêm | Nội dung |
|---|---|---|---|
| `AUTHORSHIP.md` | `a27a9b39d80536cb` → `cdc7d9ab32919258` | +6 | **D-B1**: nguyên văn "Đã Duyệt D-B1 bằng cách dán lệnh BAN-CUOI-T4-B1 vào một phiên mới.", **26/10/2026 10:42** (10:41:56 = 03:41:56Z), nghĩa: LFS bản dựng trung gian theo một mẫu. **B1-Q1…Q5**: mỗi mục một dòng, nguyên văn "Duyệt B1-Q1…Q5 theo khuyến nghị điều phối", **giờ dán 27/10/2026 07:24 (00:24:07Z)** làm giờ duyệt, nghĩa như lệnh; cột đóng góp của con người + phần AI/điều phối đề xuất |
| `RIGHTS.md` | `52f7a1ffb14f33e7` → `d1e18247d2f43ddc` | +16 | mục "T4 London — bản cuối BAN-CUOI-T4-B1": **T4-BC-B1-DAU** 4 ảnh AI OpenAI (ảnh đầu H5-02b a1/a2, H5-02s a1 (LOẠI)/a2; đầu vào là render của dự án) và **3 clip Omni 360p trượt** (H5-02b l1, l2; H5-02s l2) — tất cả **Không / Không / Không**; SHA gốc theo sổ + bản trong git (P-2710 kiểm: gốc `goc/` khớp `output.sha256` 4/4 ảnh, 3/3 clip). Không tài sản mới dùng trên phim |
| `COST-LEDGER.csv` | `95e83b00d12e1872` → `939c4bb70643242a` (sau dòng B1) → `47e2512992aa584c` (sau dòng P-2710) | +2 | **BAN-CUOI-T4-B1**: dòng nguyên văn lệnh + ghi chú điều phối (dưới); `claude_api_usd` 0.806 (cận dưới), `gio_render` 18.5. **P-2710**: API 0, ≈ 0,2 h |
| `channel-k2/BAI-HOC-K2.md` | `492e2bd40a2854cb` → `afd993fda0432727` | +11 | **K106–K110** = 5 mục B1 §8 (mặt cắt dâng + soi năm biên; RT phản chiếu giữ phát sáng; đo giờ đêm/lửa trước khi chia phiên; `pipefail` + `grep -q`; loại trừ công trình lịch sử khỏi quy tắc vùng). **K111** (điều phối): sổ Claude q_thoi_dai phải có `usd` từng dòng — B1 thiếu 9/32. **K112** (điều phối): ước giờ từ mẫu ngày thấp hơn thực tế ×1,35 (8,58 → 11,6 s/khung) — ước phiên dựng dùng số đo shot đêm/lửa |
| `reports/k1173/QUYET-DINH-TREO.md` | `a6f6b8f428b6c49d` → `b446e75efcf84f98` | +23 (mục L cuối tệp) | Đã quyết: D-B1, B1-Q1…Q5. Còn treo: **hiệu chuẩn BIEN-CO-V T4 trên master 1080p (sau B3)**, **Đ5 quyền giọng G1**, **tra thêm chân dung Godfrey Allen**, **vòng xem nhịp 1080p (K1179-D3)** (cùng vòng chấm độ sáng B1-Q5); giữ từ mục K: phiếu bản cuối D5/D6, chặn `pkill -f` bằng công cụ |

SHA đầy đủ: `reports/p2710/sha-truoc.txt`, `sha-sau.txt` (COST-LEDGER sau thật = `47e25129…`, khác `sha-sau.txt` vì dòng P-2710 thêm ở commit cuối). Script ghi sổ: `reports/p2710/ghi_so.py`.

**Dòng sổ đã ghi (COST-LEDGER, cột `ghi_chu`, nguyên văn lệnh):** `2026-10-26 · BAN-CUOI-T4-B1 · Gemini $0,581 (Omni 360p 3 lệnh $0,529; Flash 7 lệnh $0,052) → T4 tổng $19,16 · OpenAI $0,390 · Claude API ≥ $0,806 · ElevenLabs 0 · RunPod 0 · ≈ 18,5 h máy (vượt mốc 14 h) · LFS ≈ 1,03 GB` + ghi chú điều phối: 9/32 dòng sổ Claude (q_thoi_dai soi năm biên + tầng 2 H5-02s) thiếu `usd` → số Claude thật cao hơn $0,806 (ước ≤ $0,3 thêm — chưa đo). Dòng **P-2710**: API 0; ≈ 0,2 h.

**Kiểm bằng máy khi ghi sổ** (sổ trong `reports/ban-cuoi-t4-b1/`):
| Nhà | Sổ | Lệnh | USD sổ | Báo cáo B1 | Khớp |
|---|---|---|---|---|---|
| Gemini | `so-ai-gemini.jsonl` (10 dòng) | Omni 360p 3 · Flash 7 | 0,5290 · 0,0521 | 0,529 · 0,052 | ✓ |
| OpenAI | `so-ai.jsonl` (4) + `cost.jsonl` (3) | gpt-image-2.5 4 · gpt-6.1-sol 3 | 0,3052 + 0,0847 = 0,3899 | 0,390 | ✓ |
| Anthropic | `so-ai-claude.jsonl` (32) | 23 có `usd` (claude-sonnet-5-5) · **9 thiếu `usd`** (6 soi năm biên H2-05s k0, H2-06 k0, H2-06 k414, H2-09 k239 ×2, H3-01 k71 — `model` rỗng; 3 tầng 2 H5-02s-l2) | 0,8060 (23 dòng) | 0,806 ("có usd từng lệnh") | số khớp, **lời khai sai** → ghi "≥" |

## §4 main
- Trước: `75e94b98f68f3ec6fca5de0b28f35dca63ef5994` (fetch lại ngay trước khi cập nhật: vẫn 75e94b98).
- Sau: đỉnh nhánh `claude/bold-goodall-xi0iw0` = commit "P-2710: báo cáo … DỪNG chờ chủ dự án" (SHA ở `git log origin/main -1`; commit không tự chứa SHA của chính nó). Fast-forward, không force.

## §5 Chỉ số trong ±5 % quanh ngưỡng
Phiên này không đo chỉ số mới. Chép lại từ B1 §7: thời lượng 770,874 / 780 s (−1,2 %), M-d dài nhất 8,0 / 8 s, chốt 3 = 2 / 2, MÓC 4 loại / 4 (không đổi từ v4). Ngoài ±5 % nhưng nêu: giờ máy B1 18,5 / 14 h (+32 %).

## §6 Sự cố
- Không có. Ghi chỗ cần biết: (1) `TZ=Asia/Saigon date` trả UTC — giờ Saigon tính UTC+7 + giờ tạo phiên từ `get_session`. (2) `verify.sh` báo thiếu 4 gói môi trường (§0) — không ảnh hưởng phiên này.

## §7 Việc chờ chủ dự án
1. **Duyệt báo cáo P-2710** (merge B1, Kinh thánh §14.7/§15 (k)/§19 (d), sổ).
2. **Phiên B2a (đang chạy song song)**: lấy main mới (LOCK 1.17.9, Kinh thánh `22c6889d`) trước khi chạy k2check; áp B1-Q1 (M00 + H1-01h ở 160 m). P-2710 không đụng nhánh đó.
3. **Lệnh B2b**: theo B1-Q2 + B1-Q4 (lấp khối ngoài City + dựng lại H3-03; dự phòng MAP3D); tính giờ bằng 11,6 s/khung (K112).
4. **Lệnh B3**: HỒI 5 + E H5-05a + B + Omni 720p + âm + ghép + xuất + G2; chỉnh `nang_toi`/tông lửa (B1-Q5).
5. **Sau B3**: xem bản xem 1080p — chỉ shot chậm, chọn ≤ 3 shot "đứng có chủ ý" (K1179-D3), chấm lại độ sáng H1-01h/H1-02h, H1-13a/H1-13c (B1-Q5); phiếu bản cuối đẩy 2D (D5), nước AI (D6).
6. **Phiên K sau B3:** hiệu chuẩn BIEN-CO-V T4 trên master 1080p.
7. **Đ5 quyền giọng G1** (ElevenLabs) — vẫn chờ.
8. **Tra thêm chân dung Godfrey Allen** (NPG, St Paul's, Commons, Historic England) trước gói phát hành.
9. Đề xuất (giữ): giao phiên Nền tảng chặn `pkill -f`/`pgrep -f` bằng công cụ (K105); thêm: kiểm bằng máy "mọi dòng sổ AI có `usd`" vào preflight hoặc công cụ ghi sổ (K111).

**DỪNG chờ chủ dự án.**
