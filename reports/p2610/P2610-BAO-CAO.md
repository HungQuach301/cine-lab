Nhánh thật: **`claude/p-2610-merge-k1177-animatic-eu7wvv`**. Harness buộc tên này; lệnh ghi `p-2610`. Gốc `origin/main` @`ddc070e9`, đúng gốc lệnh. `main` được cập nhật bằng fast-forward lên đỉnh nhánh này (commit "… DỪNG chờ chủ dự án").

# P-2610 — gộp K-1.17.7 + ANIMATIC-T4-V2 vào main, Kinh thánh theo K1177-D1…D7 và hướng phần hiện đại A+B+E, sổ. BÁO CÁO. DỪNG chờ chủ dự án

## §0 Điều lệ phiên và tóm tắt
| Trường | Lệnh | Thực tế |
|---|---|---|
| Nhánh | `p-2610` từ origin/main @ddc070e9 | harness buộc `claude/p-2610-merge-k1177-animatic-eu7wvv` (ghi ở dòng đầu); gốc đúng ddc070e9 |
| Song song | K-1.17.8: không đụng | nhánh `claude/k1178-t4-london-rules-pdjfmz` có trên origin (thấy qua `ls-remote` khi kiểm). Phiên không fetch, không đọc, không sửa nhánh này |
| Vùng sửa | Kinh thánh, AUTHORSHIP, RIGHTS, COST-LEDGER, BAI-HOC-K2, QUYET-DINH-TREO (chỉ thêm mục cuối), reports/p2610/**, main | đúng. Commit riêng của phiên chỉ đổi 6 tệp sổ/Kinh thánh + `reports/p2610/**` (`git diff --name-only 4d570f34 HEAD`). `checks/` (20 tệp), `checks-appeal.md`, `scripts/k2ldn` (20), `design/k2v` (2), `channel-k2/k2c-t4-02/**` (540) chỉ đổi qua merge. `tools/` 0 tệp |
| Chi phí | API 0; giờ máy mốc 1,5 h | Claude API / OpenAI / Gemini / ElevenLabs / RunPod / YouTube **$0**, không gọi lần nào. 0 tác tử phụ. Không tải LFS. Giờ máy ≈ **0,35 h** (17:14 → ≈ 17:35 UTC), phần lớn là 2 lượt selftest |
| Preflight | `set -o pipefail`; chỉ commit khi có "— ĐẠT" | `reports/p2610/cam_commit.sh` chỉ commit khi có cả "— ĐẠT" và "PREFLIGHT ĐẠT"; hook pre-commit chạy lại. **Lệch một lần, nêu rõ:** commit merge 1 (`8b6a4ca2`) tạo thẳng bằng `git merge --no-ff` (merge commit không chạy hook pre-commit), chưa qua preflight trước. Ngay sau đó `tools/preflight.sh --range ddc070e9..HEAD` cho kết quả "79 tệp — ĐẠT · lock KHỚP · PREFLIGHT ĐẠT", trước lần đẩy đầu. Merge 2 dùng `--no-commit`, chạy preflight trên phần stage rồi mới commit |
| Hook | cài trước lần đẩy đầu | `pre-commit` + `pre-push` → `tools/preflight.sh`, cài 17:14 UTC; lần đẩy đầu 17:27 UTC |
| Force / amend | không | 0 force, 0 amend |
| Email / UA / khoá | che; không đưa email chủ dự án vào tệp | git dùng noreply (86/86 commit trong `ddc070e9..HEAD`). Diff `ddc070e9..HEAD` có **0** chuỗi email chủ dự án. Phiên không gọi HTTP nên không có UA; không đọc, không in khoá |
| `lock.py` | chỉ `--verify` | chỉ `python3 -I checks/lock.py --verify` (gọi trực tiếp và qua preflight). Mọi lần **KHỚP 1.17.7 `3a53574c…`** |
| Tiến trình nền | PGID, một vòng nặng một lúc, P ≤ 2, RAM ≥ 5 GB, kiểm đĩa | selftest chạy bằng `setsid nohup` (PGID 1304, rồi 10323), chờ bằng vòng `grep "== tổng"`, không `pgrep/pkill -f`. Mỗi lúc chỉ 1 lượt nặng. RAM trống 15 GB, đĩa trống 15 GB. Có một lệnh `git grep` qua 2 cây bị harness đẩy nền vì quá 120 s; lệnh tự xong, không trả kết quả, đã bỏ |
| Đẩy ≤ 30 phút + CHECKPOINT | bắt buộc | đẩy 17:27, 17:32, lần cuối; `reports/p2610/CHECKPOINT.md` |
| Đầu vào ở /var/tmp | không chỉ để ở đó | phiên không tạo tệp ở /var/tmp. Bản báo cáo ANIMATIC chép ra scratchpad chỉ để đọc; bản gốc có trong git |
| Lệnh bổ sung | ghi vào CHECKPOINT | không có |
| Đã đọc | — | BAI-HOC-LL (khởi động), K1177-BAO-CAO, ANIMATIC-T4-V2-BAO-CAO, PHIEU-XEM-V2 mục C, `ghi-cong.json`, `sfx.json`, `sha-tu-lieu-t4.txt`, `giay-phep/commons-iwm-d6418.json`, 21 `nc/licenses/*.json` (đọc bằng máy), Kinh thánh §13, §14.7, §15, §17, §19, QUYET-DINH-TREO mục G, P2510B-BAO-CAO §0 (để lấy khuôn). Không đọc mã trong `checks/` |

**Tóm tắt**
1. **Hai merge `--no-ff`, 0 xung đột.** Cả hai đỉnh trùng SHA lệnh (`1277400a`, `1a911a01`). Sau mỗi merge, LOCK **1.17.7 `3a53574c…` KHỚP** và selftest đạt 15/15 bộ, trong đó **k1177 87/87, k1176 62/62, k2 129/129, ll 317/317** (§1).
2. **Kinh thánh `08cc1da9…` → `a4d1c3fd…`** (+13 / −4 dòng). Ghi K1177-D1…D7 và trỏ tới RULES-LL 1.17.7, không chép luật. Thêm **§15 (k): phần hiện đại A+B+E** với hai điều kiện: K-1.17.8 khoá luật E, và thử 2 khung đạt. Kèm ghi chú "AI có thể vẽ sai vị trí nhà thường ở cảnh 2026, chấp nhận theo 25/10 09:08; lớp dữ kiện vẫn chặt" (§2).
3. **Sổ (chỉ thêm, xoá 0 dòng):** AUTHORSHIP +4, RIGHTS +32 (mục ANIMATIC-T4-V2 + dòng trỏ), COST-LEDGER +3 (K-1.17.7, ANIMATIC-T4-V2, P-2610), BAI-HOC-K2 K81–K86, QUYET-DINH-TREO mục H (§3).
4. **Kiểm bằng chứng bằng máy (K84):** 21/21 JSON `nc/licenses/` có trong git, SHA gốc khớp `SHA256-NC.txt` 21/21. Tiền trong sổ AI: Gemini $6,5272 và OpenAI $3,2668 khớp báo cáo. Riêng **q_thoi_dai lớp mốc ≈ $1,55 không kiểm được**, vì `qtd-moc.jsonl` không có usage/giá (K86) (§3).
5. **main `ddc070e9` → đỉnh nhánh** bằng fast-forward. Ngay trước khi đẩy, phiên fetch lại và thấy main vẫn ở ddc070e9; không force (§4).

## §1 Merge
| Nhánh @ SHA lệnh | Commit merge | Tệp | LOCK sau merge | selftest |
|---|---|---|---|---|
| `origin/claude/k1177-animatic-checks-nfbsbr` @`1277400a` (đỉnh khớp) | `8b6a4ca2` | 79 (+8 757 / −72): checks/ 20 (LOCK, cinecheck, ll 16, models 3), checks-appeal.md 1, reports/k1177 57 | **1.17.6 → 1.17.7 `3a53574ce8c2094e4f79bc1fac88cf3e6f7bbe61993ab5a1cf695834a2067b08` KHỚP** | `selftest-1.txt`: 15/15 bộ rc 0 (k112 75 · k1121 48 · k1122 37 · k113 64 · k114 126 · k115 105 · k116 144 · k117 130 · k1172 74 · k1173 42 · k1174 91 · k1175 52 · k1176 62 · **k1177 87/87** · k2 129 · ll 317) |
| `origin/claude/animatic-t4-v2-revision-hwh8jp` @`1a911a01` (đỉnh khớp; gốc = 1277400a) | `4d570f34` | 610: channel-k2/k2c-t4-02 540 (animatic2 499, nc 21, am-thanh 15, …), reports/animatic-t4-v2 66, scripts/k2ldn 20, design/k2v/ldn 2. **0 tệp checks/** | **1.17.7 `3a53574c…` KHỚP** | `selftest-2.txt`: 15/15 bộ rc 0 (cùng số ca như trên) |

## §2 Kinh thánh `docs/BIBLE-KENH2.md`
SHA trước `08cc1da97abfc9c364e1…`, sau `a4d1c3fd61cb5fdf206ea85a30767bbc6edfe14ef8af2ffd1d7dc40bfc759ce1`. Sửa bằng `reports/p2610/sua_bible.py`; diff ở `reports/p2610/bible-diff.txt`. Mọi chỗ trỏ tới luật ghi "`checks/ll/RULES-LL.md` mục 1.17.7 (LOCK 1.17.7 `3a53574c…`; Kinh thánh không chép luật)".
| Chỗ | Đổi | Căn cứ ghi |
|---|---|---|
| Dòng đầu | thêm mốc sửa P-2610 | — |
| 3 chỗ "1.17.7 (đang làm — …)" ở §15 (d) 09:15, §15 (f) nới hẹp, §19 (c) 09:15 | thay bằng chỗ trỏ luật đã khoá | (duyệt 25/10/2026 11:58, D1 = A) |
| §13 "Hàng kiểm mới từ T4" | thêm dòng liệt kê các hàng 1.17.7: GOC-CAO, TU-LIEU-THAT, NHAN-VAT-TEN, KIEM-2-MUC, cùng các hàng đổi K-LAI-1, TL-1, TU-LIEU-10, MAY-19, Q37 (a), BE-MAT-NHA (d) và lớp mốc q_thoi_dai | D1 |
| §14.7 LOOK-T4-8 | thêm dòng cập nhật. Ngoại lệ có điều kiện cho câu "không dùng vân nướng AI ở toàn cảnh": góc rộng 2026 máy cố định theo §15 (k) | (duyệt 26/10/2026 00:07) |
| §15 (d) | thêm dòng 25/10 11:58. 5 chốt góc cao ở mức **Chặn G2** (D2). Kiểm 2 mức đo bằng KIEM-2-MUC. Từ T4, K-LAI-1 không tính M-d (C11 06:56) | D2 |
| §15 (f) | thêm dòng 25/10 11:58. (1) Mặt nhân vật có tên ≤ 1/8 chiều cao khung, đo bằng YuNet, có chân dung tham chiếu và dòng duyệt AUTHORSHIP (D3). (2) Lớp công trình mốc bắt buộc; khai `chan_troi_city` cho **mọi** M-d thấy chân trời City (D4) | D3, D4 |
| §15 (j) | thêm dòng. (1) Sàn Y nhấp nháy theo tập, T4 0,01 (D6). (2) Ảnh nền AI toàn khung cho góc rộng 2026 → §15 (k) | D6; 00:07 |
| **§15 (k) mới** | **Phần hiện đại T4 (≈ 1946–2026) ở bản cuối, hướng A+B+E:**<br>- (A) ≈ 30–40 s 3D trung/cận → Omni. Có lớp mốc, mức ĐỦ, trần Gemini giữ $55/$50.<br>- (B) Ảnh thật CC BY/PD hiện đại. Lớp THAT, không share-alike, có bằng chứng `licenses/`, tính trong ≤ 20 %.<br>- (E) Ảnh nền AI toàn khung cho góc rộng 2026 máy CODINH. Sông, bờ, mái vòm St Paul's và toà tháp có tên ghép lại từ 3D (lớp (a)). BE-MAT-NHA px/m nới riêng cho năm ≥ 2020, luật do K-1.17.8.<br>- **Điều kiện áp E:** K-1.17.8 khoá luật, và 2 khung thử đạt. Thiếu một trong hai thì giữ D 3D. Đêm 2026 trượt thì giữ 3D. Không làm (C).<br>- **Ghi chú:** AI có thể vẽ sai vị trí nhà thường ở cảnh 2026, chấp nhận theo chủ dự án 25/10 09:08 (trích nguyên văn); lớp dữ kiện (a) vẫn chặt | (duyệt 26/10/2026 00:07; hỏi 00:02) |
| §17 | thêm (4): lớp chồng ghi vào `p.lop_chong` của đặc tả; trình ghép đọc từ đó (D5) | D5 |
| §19 | thêm đoạn "(a)/(c) cập nhật 25/10 11:58". TL-1 (c) miễn một cắt ở mỗi ranh M-d/tư liệu (D7, P9). Lớp THAT kiểm bằng TU-LIEU-THAT | D7 |

Phiên tự mở rộng một chỗ ngoài hai mục lệnh nêu (§15 (j), mục phần hiện đại): dòng cập nhật ở **§14.7 LOOK-T4-8**. Lý do: LOOK-T4-8 đang cấm "vân nướng AI ở toàn cảnh", trái với (E). Không ghi dòng này thì Kinh thánh tự mâu thuẫn. Dòng này chỉ trỏ sang §15 (k), không thêm luật.

## §3 Sổ
| Tệp | SHA trước (16 ký tự; sau: `sha-sau.txt`) | Thêm | Nội dung |
|---|---|---|---|
| `AUTHORSHIP.md` | `4262c65d249252bb` | +4 | lệnh bổ sung ANIMATIC #1 (10:05) + #2 (12:05), chủ dự án dán · K1177-D1…D7 (11:58) · câu hỏi 26/10 00:02 (chưa phải quyết định) · A+B+E (00:07). Mỗi dòng có nguyên văn, giờ, nghĩa và đóng góp biểu đạt |
| `RIGHTS.md` | `afdcd3498f09a273` | +32 | mục "T4 London — animatic v2". THAT/góc khung: **T4-TL-IWM-D6418** (Commons, bản thu 500×667, PD-UKGov, SHA `d98e4829…`), T4-TL-RIJKS-200323435 (1892, PDM), T4-TL-LOC-2002696930 (photochrom London Bridge), **T4-TL-LOC-2002696941** (photochrom Embankment, H3-03t: có trong ghi-cong.json nhưng §13 báo cáo xưởng không liệt kê riêng), T4-TL-WELLCOME-UV3MUGCH (bản vẽ 1865, góc khung). SFX T4-SFX-CHUONG-1, T4-SFX-COI-40 (BigSoundBank CC0, có SHA gốc/đoạn/trang). Bằng chứng 21 mục NC-T4: 21/21 trong git. Footage đêm **không dùng** ở T4 v2 → không cần PDF Pexels/Pixabay. Footage trả phí (C) không làm. Thêm 1 dòng trỏ dưới "Lưu ý bằng chứng (P-2510b)" |
| `COST-LEDGER.csv` | `26267bf934c66d46` | +3 | K-1.17.7 (Claude $0,3033 khớp sổ 9 lệnh; ≈ 1,6 h) · ANIMATIC-T4-V2 (Gemini $6,53, T4 tổng $15,07; OpenAI $3,27; Claude ≈ $2,32; ElevenLabs 1 333 ký tự, bộ đếm +586; ≈ 11,8 h; 770,875 s) · P-2610 |
| `channel-k2/BAI-HOC-K2.md` | `08ac6a5d4f60c24f` | +10 | K81 = ANIMATIC-T4-V2 §13 (a)–(e) · K82 = sự cố 11 (clip v1 gõ tay) · K83 = lock gọi 2 lần (preflight chặn email trong giấy phép bên thứ ba) · K84 = bài học điều phối "rà phiên phải kiểm tệp bằng chứng mà báo cáo nhắc tới có thật trong git" (K79) · K85 = `pgrep -f` lặp lần 5 → đề xuất phiên Nền tảng chặn bằng công cụ · K86 = sổ AI q_thoi_dai thiếu usage/giá (phát hiện của P-2610) |
| `reports/k1173/QUYET-DINH-TREO.md` | `2fff7fc1a5251e70` | +34 (chỉ mục H cuối tệp) | Đã quyết: K1177-D1…D7, lệnh #1/#2, A+B+E; mục G "Bằng chứng JSON 21" → xong; "PDF footage" → không cần cho v2. Còn treo: phiếu xem v2 A1/B/C (C1–C7), xung đột K-LAI-3 ↔ KIEM-2-MUC, K-1.17.8, thử 2 khung E, BAN-CUOI-T4, ảnh thật hiện đại (B), IWM D 6418 gốc, sổ AI q_thoi_dai |

SHA đầy đủ trước/sau: `reports/p2610/sha-truoc.txt`, `reports/p2610/sha-sau.txt`. Dòng P-2610 của COST-LEDGER thêm ở commit cuối, nên SHA sau của COST-LEDGER lệch so với `sha-sau.txt`.

**Kiểm bằng máy khi ghi sổ** (đối chiếu số tự khai):
- Sổ AI ANIMATIC-T4-V2 có 97 dòng Gemini: Omni $6,1393 + Flash $0,3879 = **$6,5272**. 31 ảnh OpenAI $2,036, cộng 48 lần kiểm gpt-6.1-sol $1,2308, ra **$3,2668**. XEM CÂM $0,769. Ba số này khớp báo cáo xưởng.
- Sổ AI K-1.17.7 có 9 lệnh, tổng **$0,3033**, khớp báo cáo K.
- **Không kiểm được:** q_thoi_dai lớp mốc ≈ $1,55, vì `qtd-moc.jsonl` 46 dòng không có usage/giá. Đã ghi rõ trong COST-LEDGER và K86.
- `nc/licenses/*.json`: 21 tệp trong git, trường `original.sha256` khớp `SHA256-NC.txt` 21/21. `animatic2/tu-lieu/commons-iwm-d6418.jpg` có SHA `d98e4829…`, khớp `sha-tu-lieu-t4.txt`.

## §4 main
- Trước khi đẩy: `git fetch origin main` → `origin/main` = **`ddc070e9`**, vẫn đúng gốc lệnh.
- Đẩy `HEAD:main` fast-forward `ddc070e9 → <đỉnh nhánh>` (commit "… DỪNG chờ chủ dự án"). Không force; pre-push preflight ĐẠT. SHA đỉnh ghi trong thông điệp phiên.

## §5 Chỉ số trong ±5 % quanh ngưỡng (luật cứng)
Phiên này không đo chỉ số phim mới. Các chỉ số sát ngưỡng đã được hai báo cáo nguồn nêu tên và được chép lại vào sổ, không đổi:
- ANIMATIC-T4-V2 §12: thời lượng 770,875 / 780 s (−1,2 %); M-d dài nhất 8,0 / 8 s; chốt 3 = 2 / 2; MINH-HOA 20,74 / 20 % (+3,7 %); Q37 (1.13) 5,92 / 6 s; thẻ chương 3,0 / 3,0 s; A1 −14,0 LUFS.
- K-1.17.7 §10: TU-LIEU-10 T4 v1 9,66 / 10 % (khi chưa khai); TL-1 (d) H4-07 2,0 / 2 %/s.

## §6 Việc chờ chủ dự án
1. **Phiếu xem v2** (`reports/animatic-t4-v2/PHIEU-XEM-V2.md`, 4 tệp `xem/`):
   - **A1**: duyệt từng clip có nhân vật có tên: H1-05a; H1-15b (mặt Pepys > 1/8 ở 1 khung); H3-05b (không có chân dung). Ngoại lệ H1-06b.
   - **B**: chấm XEM CÂM cho Q2, Q3, Q4, Q6.
   - **C**: chọn C1–C7.
2. **K-1.17.8** (đang chạy song song): khoá luật E và BE-MAT-NHA px/m riêng cho năm ≥ 2020. Sau đó thử 2 khung E. P merge K-1.17.8 khi chủ dự án duyệt.
3. **Xung đột K-LAI-3 ↔ KIEM-2-MUC** (clip mức nền H1-06b, H1-15m): cần ghi `checks-appeal.md`, nhưng lệnh này không cho P-2610 sửa tệp đó. Chủ dự án chọn: giao phiên P sau ghi, hoặc chuyển thẳng cho K-1.17.8.
4. **BAN-CUOI-T4**: mở sau khi có 1–3. Khai đủ K1177 §4, theo A+B+E và phiếu v2.
5. Đề xuất K85: mở phiên Nền tảng chặn `pgrep -f` / `pkill -f` bằng công cụ (lặp lần 5).
6. Giữ từ mục G: Đ5 (quyền giọng G1), đo lại BMN + BIEN-CO-V, ảnh Blitz Crown.

**DỪNG chờ chủ dự án.**
