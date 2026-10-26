Nhánh thật: **`claude/p2610c-merge-ban-cuoi-t4a-vcrr3c`**. Harness buộc tên này; lệnh ghi `p-2610c`. Gốc `origin/main` @`41de7ce3`, đúng gốc lệnh. `main` được cập nhật bằng fast-forward lên đỉnh nhánh này (commit "… DỪNG chờ chủ dự án").

# P-2610c — gộp BAN-CUOI-T4-A vào main, ghi quyết định PHIẾU-A (D-A1…D-A9). BÁO CÁO. DỪNG chờ chủ dự án

## §0 Điều lệ phiên và tóm tắt
| Trường | Lệnh | Thực tế |
|---|---|---|
| Căn cứ | chủ dự án 26/10/2026 "Duyệt PHIẾU-A theo khuyến nghị điều phối"; giờ dán lệnh = giờ duyệt | **26/10/2026 10:08 Asia/Saigon** = 2026-10-26T03:08:34Z, giờ tạo phiên P-2610c (đọc từ `get_session`) |
| Nhánh | `p-2610c` từ origin/main @41de7ce3 | harness buộc `claude/p2610c-merge-ban-cuoi-t4a-vcrr3c` (ghi ở dòng đầu); gốc đúng **41de7ce3** (fetch 03:10 UTC) |
| Merge | origin/claude/k2c-t4-02-final-a-0pb0bh @bc1693b5, không squash, `--no-ff --no-commit` + preflight | đỉnh **bc1693b5** khớp; 0 xung đột; preflight `--staged` "531 tệp — ĐẠT · lock KHỚP · PREFLIGHT ĐẠT" → commit `9db46b08` (cha 1 `41de7ce3`, cha 2 `bc1693b5`) |
| LOCK | sau merge `lock.py --verify` KHỚP 1.17.8 `045b7bb7…` | **KHỚP** `045b7bb7414364d4732fe22c4b643ae04d7a0e19ae25f0e839de149379d3185a` (trực tiếp sau merge, qua mọi preflight, trước khi ff main). Merge đổi **0** tệp trong `checks/` và `checks-appeal.md` |
| Song song K-1.17.9 | không đụng `checks/**`, `checks-appeal.md`, `reports/k1179/**` | không đọc, không sửa; không fetch nhánh K |
| Vùng sửa | Kinh thánh, AUTHORSHIP, RIGHTS, COST-LEDGER, BAI-HOC-K2, QUYET-DINH-TREO, reports/p2610c/** (commit riêng ngoài merge) | đúng: `git diff --name-only 9db46b08 HEAD` chỉ có 6 tệp sổ/Kinh thánh + `reports/p2610c/**`. Không sửa `checks/`, `checks-appeal.md`, `channel-k2/k2c-t4-02/**`, `scripts/`, `design/`, `tools/`, nhánh khác |
| Chi phí | API 0; giờ máy ≤ 2 h | Claude API / OpenAI / Gemini / ElevenLabs / RunPod / YouTube **$0**, không gọi lần nào; 0 tác tử phụ; không tải LFS. Giờ máy ≈ **0,3 h** (03:10 → ≈ 03:27 UTC) |
| Preflight | `set -o pipefail`; chỉ commit khi có "— ĐẠT" | `reports/p2610c/cam_commit.sh` (`set -o pipefail`) chỉ commit khi có cả "— ĐẠT" và "PREFLIGHT ĐẠT"; hook pre-commit chạy lại |
| Hook | cài trước lần đẩy đầu | `pre-commit` + `pre-push` → `tools/preflight.sh`, cài 03:12 UTC; lần đẩy đầu 03:23 UTC |
| Force / amend | không | 0 force, 0 amend |
| Email / UA / khoá | che; không đưa email chủ dự án vào tệp | mọi commit `41de7ce3..HEAD` dùng noreply (22/22). Diff sổ của phiên: **0** chuỗi email chủ dự án. Phiên không gọi HTTP (không UA); không đọc, không in khoá |
| `lock.py` | chỉ `--verify` | chỉ `python3 -I checks/lock.py --verify` (trực tiếp và qua preflight) |
| Tiến trình nền | PGID, một vòng nặng, P ≤ 2, RAM ≥ 5 GB, đĩa | không có tiến trình nền (việc nhẹ: merge, sổ). RAM trống 15 GB, đĩa trống 15 GB |
| Đẩy ≤ 30 phút + CHECKPOINT | bắt buộc | đẩy 03:23 (sổ + Kinh thánh), lần cuối ≈ 03:27 (báo cáo); `reports/p2610c/CHECKPOINT.md` |
| Đầu vào /var/tmp | không chỉ để ở đó | phiên không tạo tệp ở /var/tmp; bản Kinh thánh trước sửa chép ra scratchpad chỉ để chạy lại script, SHA ở `sha-truoc.txt` |
| Đã đọc | — | BAI-HOC-LL (khởi động), P2610B-BAO-CAO (khuôn), BAN-CUOI-T4-A-BAO-CAO (đủ), PHIEU-A (đủ), khieu-nai-K (mục lục), sổ AI BAN-CUOI-T4-A (đọc bằng máy), `that/licenses/*.json`, 1 khung mẫu `mau-H2-10-1080.jpg`. Không đọc mã `checks/` |

**Tóm tắt**
1. **Merge `--no-ff --no-commit`, 0 xung đột**, 531 tệp (+57 952): `channel-k2/k2c-t4-02` 402, `reports/ban-cuoi-t4-a` 107, `scripts/k2ldn` 22. Preflight trên phần stage ĐẠT rồi mới commit (`9db46b08`). LOCK 1.17.8 KHỚP; `checks/` không đổi nên không chạy lại selftest (§1).
2. **Kinh thánh `fbac59d9…` → `86daf2d5…`** (+9 / −1): §15 (k) cập nhật (D-A1, D-A2), §14.7 LOOK-T4-9 cập nhật (D-A3, D-A8), **§19 (d) mới "Niên đại công trình mốc T4 — luật dựng"** (D-A4 (i)) (§2).
3. **Sổ** (chỉ thêm): AUTHORSHIP +9 (D-A1…D-A9), RIGHTS +28, COST-LEDGER +2 (BAN-CUOI-T4-A, P-2610c), BAI-HOC-K2 K94–K100, QUYET-DINH-TREO mục J (§3).
4. **Cộng sổ bằng máy** xác nhận hai ghi chú điều phối: sổ k2check gpt trong git **$0,9663** (13 lệnh, 10 tệp `n2p-cost.jsonl`) so báo cáo $1,047 — chênh $0,081; Flash **29** lệnh ($0,1898) so báo cáo ghi 43 (43 là tổng dòng Gemini) (§3).
5. **Soi khung H2-10** (`mau-H2-10-1080.jpg`): chỉ có tang trống + hai tháp phía tây, **không có vỏ vòm, không đèn lồng** — xác nhận lỗi niên đại D-A4 (i).
6. **Phát hiện:** 4 clip Omni 360p được duyệt trong git là **bản nén lại** (SHA khác `output.sha256` của sổ); gốc ở `/var/tmp/bc/omni/` của container BAN-CUOI-T4-A không còn. Chỉ clip 720p đo giá là bản gốc (SHA khớp). Ảnh hưởng thấp vì bản cuối sinh lại 720p (§6).
7. **main `41de7ce3` → đỉnh nhánh** bằng fast-forward, sau khi fetch lại thấy main vẫn ở 41de7ce3; không force (§4).

## §1 Merge
| Nhánh @ SHA lệnh | Commit merge | Tệp | LOCK sau merge |
|---|---|---|---|
| `origin/claude/k2c-t4-02-final-a-0pb0bh` @`bc1693b5` (đỉnh khớp; cha 2) | `9db46b08` (`--no-ff --no-commit` → preflight `--staged` "531 tệp — ĐẠT · lock KHỚP · PREFLIGHT ĐẠT" → `cam_commit.sh`) | 531 (+57 952 / −0): channel-k2/k2c-t4-02 402 · reports/ban-cuoi-t4-a 107 · scripts/k2ldn 22 · checks/ 0 · checks-appeal.md 0 | **1.17.8 `045b7bb7…` KHỚP** (không đổi) |

Ghi chú: `git merge-base` báo nhiều gốc chung (nhánh BAN-CUOI-T4-A đã tự merge K-1.17.8 @297eb070, main cũng có K-1.17.8 qua P-2610b) — git tự giải, 0 xung đột. Sổ chung (AUTHORSHIP, RIGHTS, COST-LEDGER, Kinh thánh…) không bị merge đổi: nhánh A không sửa sổ.

## §2 Kinh thánh `docs/BIBLE-KENH2.md`
SHA trước `fbac59d9bac49e13daf56886e8f6eeb3e730287711cb753b129ad895537b3cfe`, sau `86daf2d5c14f8e27d1a7dae3dedb6c1bd3432dd1eb536ff3ecd605ee550320a3`. Sửa bằng `reports/p2610c/sua_bible.py` (chỉ chèn sau mốc, mỗi mốc kiểm đúng 1 lần); diff `reports/p2610c/bible-diff.txt`. Căn cứ ghi một dạng: **"(duyệt 26/10/2026 10:08 — giờ chủ dự án dán lệnh P-2610c sau khi trả lời "Duyệt PHIẾU-A theo khuyến nghị điều phối"; `reports/ban-cuoi-t4-a/PHIEU-A.md`; D-Ax)"**.

| Chỗ | Đổi | Căn cứ |
|---|---|---|
| Dòng đầu | thêm mốc sửa P-2610c | — |
| §14.7 LOOK-T4-9 cập nhật 26/10 10:08 | (1) **giữ điểm đứng P1 hiện tại + C6 4°; không dời, không xoay riêng M03**; lượt thử (c) đã làm (mái vòm 18,2 / 24,2 / 26,2 %; lửa M03 sát mép 7,85 → 31,74 %) → câu "giữ điểm đứng" của LOOK-T4-9 có hiệu lực lại. (2) **M00 mở lạnh = điểm P1b** (Bankside đông 125 m, VONG) **kèm sửa**: mặt sông đêm không phẳng màu cát, lửa không thành cụm bông | D-A3; D-A8 (Q-A3 (a)); D-A4 (iii) |
| §15 (k) cập nhật 26/10 10:08 | điều kiện (2) đã thử; (1) **E ở H5-05a**: tấm P9-2026 ngày, mặt nạ "tháp" + ngoại lệ "bờ" (KN-1) — **chờ K-1.17.9**; K bác → mặt nạ "đủ"; (2) **E-P1 chưa dùng** (chờ KN-8 nước, KN-6 đẩy 2D); (3) **H5-04 giữ D 3D + H5-04c**; (4) **đêm H5-07a giữ 3D**; (5) nâng vật liệu mái vòm + toà tháp có tên + đèn pha đêm trước khi dựng | D-A1, D-A2; D-A4 (iv) |
| **§19 (d) mới** — Niên đại công trình mốc T4, luật dựng | St Paul's mới: khởi công **1675**, vỏ vòm + đèn lồng xong **1708**, hoàn tất **1711**; Monument **1671–1677**, thân **có rãnh dọc**; **mọi shot có năm biên (năm đầu/cuối, kể cả ảnh đầu M-d dựng từ 3D) chạm giai đoạn xây của công trình mốc phải soi khung 3D ở chính năm biên trước khi dựng 1080p**, ghi kết quả soi vào báo cáo. Căn cứ: H2-10 ≈ 1709,5 thiếu mái vòm; ảnh đầu M-d kế thừa Monument trơn. Kèm việc phiên B: D-A4 (i), (v) MAY-19, (vi) Q-A5 | D-A4 (i), (v), (vi) |

Hai chỗ cần nêu:
- **§19 (d) là luật dựng, không phải luật kiểm.** Không có hàng kiểm trong `checks/`; phiên dựng tự soi và ghi. Nếu chủ dự án muốn kiểm bằng máy (lớp mốc q_thoi_dai cho khung 3D) thì phải giao phiên K.
- **KN-8** không có trong repo khi P-2610c ghi (không có trong `khieu-nai-K.md` của A, KN-1…KN-7). Ghi theo lệnh điều phối, coi là việc của K-1.17.9.

## §3 Sổ
| Tệp | SHA trước → sau (16 ký tự) | Thêm | Nội dung |
|---|---|---|---|
| `AUTHORSHIP.md` | `d5ced1b24b6b70e5` → `2c15f834c7d6d0b0` | +9 | mỗi D-A một dòng: nguyên văn "Duyệt PHIẾU-A theo khuyến nghị điều phối", **giờ dán lệnh 10:08 (03:08:34Z) ghi làm giờ duyệt**, nghĩa đúng như lệnh; cột đóng góp biểu đạt của con người và phần AI đề xuất. D-A6 là dòng phiên B dùng để khai `duyet_chu_du_an` cho H1-06x, H1-15x |
| `RIGHTS.md` | `96ebbe5a32cfa799` → `52f7a1ffb14f33e7` | +28 | Mục mới "T4 London — bản cuối phần thử (BAN-CUOI-T4-A)": **2 ảnh thật CC BY 2.0** (T4-THAT-H5-06t, T4-THAT-H5-02t) — ghi công nguyên văn trường `ghi_cong`: **"Photo: It's No Game, CC BY 2.0"**, **"Photo: Mikey, CC BY 2.0"**; SHA trong git khớp `sha256` của JSON giấy phép · **ảnh AI OpenAI**: 4 tấm E (P9 ngày l1 dùng ở H5-05a khi K xác nhận; 3 tấm chỉ kiểm), 3 tấm B (2 duyệt D-A5, 1 trượt), 15 ảnh đầu M-d (+1 lỗi 502 $0) — SHA E/B trong git khớp `output.sha256` của sổ 7/7 · **clip Omni**: H1-06x, H1-15x, H5-04c, H5-05d l2 (duyệt) + H1-06x 720p (đo giá), SHA gốc theo sổ · SHA bản git; 9 clip trượt ghi "Không/Không/Không" · IWM D 6418 theo D-A9 |
| `COST-LEDGER.csv` | `564458faf9c371b3` → `b17e97ffa79dd284` (sau dòng BAN-CUOI-T4-A; dòng P-2610c thêm ở commit cuối) | +2 | **BAN-CUOI-T4-A**: dòng nguyên văn lệnh + ghi chú điều phối (bảng dưới). **P-2610c**: API 0, ≈ 0,3 h |
| `channel-k2/BAI-HOC-K2.md` | `50cba6e43da420b6` → `8cd434fdcfdbae43` | +11 | K94–K98 = 5 đề xuất báo cáo A §13 (ảnh đầu kế thừa niên đại 3D; tra trục phố OSM; "toà có tên OSM" ≠ "toà tháp có tên"; lệnh phủ bề mặt nêu khu không cháy; Commons API ≠ máy chủ ảnh, Flickr gốc) · **K99** soi niên đại công trình mốc trên khung 3D ở năm biên (H2-10) · **K100** đánh giá tấm E trên cả khung ghép, không chỉ ô phóng (lớp (a)-E gồm toàn mặt nước, sông render ≈ 1/3 khung P1) |
| `reports/k1173/QUYET-DINH-TREO.md` | `c54ce3eb73580d65` → `4b089de521904a17` | +30 (chỉ mục J cuối tệp) | Đã quyết D-A1…D-A9 (mục I "PHIẾU-A" và "Thử 2 khung E" → đã quyết). Còn treo: **KN-1, KN-2, KN-4, KN-5, KN-6, KN-7, KN-8 (K-1.17.9), Đ5 quyền giọng G1**; giữ các mục khác của I |

SHA đầy đủ: `reports/p2610c/sha-truoc.txt`, `sha-sau.txt`. Dòng P-2610c của COST-LEDGER thêm ở commit cuối nên SHA sau thật của COST-LEDGER khác `sha-sau.txt`.

**Dòng sổ đã ghi (COST-LEDGER, cột `ghi_chu`, nguyên văn lệnh):** `2026-10-26 · BAN-CUOI-T4-A · Gemini $3,512 (Omni 14 lệnh $3,322; Flash 29 lệnh $0,190) → T4 tổng $18,58 · OpenAI $3,345 · Claude API $2,642 · ElevenLabs 0 · RunPod 0 · ≈ 3 h máy` + ghi chú điều phối.

**Kiểm bằng máy khi ghi sổ** (P-2610c cộng lại từ sổ trong git):
| Nhà / nhóm | Sổ | Lệnh | USD sổ | Báo cáo A | Khớp |
|---|---|---|---|---|---|
| Gemini Omni 360p / 720p | `so-ai-gemini.jsonl` | 13 / 1 | 2,7085 / 0,6136 (= 3,3220) | 3,322 | ✓ |
| Gemini Flash | như trên | **29** | 0,1898 | 0,190 ("43 lệnh") | tiền ✓, **số lệnh lệch** (43 = tổng dòng Gemini) |
| Gemini T4 gộp | `so-ai-gemini-t4-gop.jsonl` | 245 dòng | 18,5823 | 18,58 | ✓ |
| OpenAI ảnh | `so-ai.jsonl` | 23 (22 + 1 lỗi 502 $0) | 1,7058 | 1,706 | ✓ |
| OpenAI gpt-6.1-sol tầng 2 | `cost.jsonl` | 24 | 0,5924 | 0,592 | ✓ |
| OpenAI mô hình nhìn k2check | 10 × `ban-cuoi/**/vision/n2p-cost.jsonl` | 13 | **0,9663** | 1,047 | **chênh $0,081 — thiếu tệp n2p-cost** |
| Claude API | `so-ai-claude.jsonl` | 64 | 2,6422 | 2,642 | ✓ |

OpenAI theo sổ có trong git = 1,7058 + 0,5924 + 0,9663 = **$3,2645** (báo cáo $3,345). Sổ ghi số báo cáo theo lệnh, kèm số trong git ở ghi chú.

## §4 main
- Trước khi đẩy: `git fetch origin main` → `origin/main` = **`41de7ce3`**, vẫn đúng gốc lệnh.
- Đẩy `HEAD:main` fast-forward `41de7ce3 → <đỉnh nhánh>` (commit "… DỪNG chờ chủ dự án"). Không force; pre-push preflight ĐẠT. SHA đỉnh ghi trong thông điệp phiên.

## §5 Chỉ số trong ±5 % quanh ngưỡng (luật cứng)
Phiên này không đo chỉ số phim mới. Chép lại các chỉ số sát ngưỡng báo cáo A §12 đã nêu, không đổi: M-d dài nhất 8,0 / 8 s (0 %); chốt 3 shot thấp/M-d/THAT liền 2 / 2 (0 %); MÓC 4 / 4 loại cú máy (0 %); thời lượng 770,874 / 780 s (−1,2 %).

## §6 Phát hiện
1. **Clip Omni 360p trong git là bản nén lại; gốc mất theo container.** SHA bản git khác `output.sha256` của sổ ở 13/13 clip 360p (gốc 0,9–1,7 MB, bản git 0,2–0,45 MB). Gốc ở `/var/tmp/bc/omni/` không còn. Chỉ `H1-06x-l1-720p.mp4` là gốc (SHA khớp). Theo luật "tệp tốn tiền nén ≤ 5 MB vào git", gốc < 5 MB đáng lẽ vào git nguyên bản. **Ảnh hưởng:** thấp — bản cuối sinh lại 720p (Omni lần mới); nhưng nếu phải dùng 360p làm dự phòng thì chất lượng thấp hơn gốc. RIGHTS ghi cả hai SHA.
2. **Ảnh đầu M-d trong git là bản chuẩn hoá cỡ cho Omni**: SHA khác `output.sha256` của sổ OpenAI, nhưng khớp `input.sha256` của sổ Omni 14/14 — chuỗi truy vết còn đủ.
3. **KN-8** chưa có tệp trong repo (xem §2).

## §7 Việc chờ chủ dự án
1. **K-1.17.9** (đang chạy): KN-1 (ngoại lệ "bờ" → mặt nạ "tháp" ở H5-05a), KN-2 (Q37/BIEN-CO-V), KN-4, KN-5 (định nghĩa toà có tên), KN-6 (đẩy 2D trên tấm E), KN-7 (H3-05b; bác → H3-05c), KN-8 (nước, E-P1). P merge K-1.17.9 khi chủ dự án duyệt.
2. **Phiên B1/B2/B3 (P = 2)**: giao lệnh. Trước khi dựng, phiên B làm D-A4 (i)–(vi) và soi niên đại theo Kinh thánh §19 (d); khai `duyet_chu_du_an` H1-06x, H1-15x bằng dòng AUTHORSHIP D-A6; thử lại Commons cho IWM D 6418 gốc (D-A9).
3. **IWM D 6418**: chủ dự án chỉ tải tay nếu phiên B vẫn gặp 429.
4. **XEM CÂM Q2/Q3/Q4/Q6**: chấm trên bản cuối (cổng XEM-CAM ở G2).
5. **Đ5** quyền phát hành giọng G1.
6. (Tuỳ chủ dự án) Có muốn §19 (d) thành hàng kiểm máy của phiên K (lớp mốc trên khung 3D) hay giữ là luật tự soi của phiên dựng.

**DỪNG chờ chủ dự án.**
