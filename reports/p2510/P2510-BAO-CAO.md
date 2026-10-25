Nhánh thật: **`claude/sharp-newton-xqh5yc`**. Harness buộc tên này, lệnh ghi `p-2510`. Gốc `origin/main` @`df317915`, đúng gốc lệnh. `main` được cập nhật bằng fast-forward lên đỉnh nhánh này (commit "… DỪNG chờ chủ dự án").

# P-2510 — gộp bộ kiểm 1.17.6 + ANIMATIC-T4 + THU-B-T4 vào main, Kinh thánh và sổ cho các quyết định 24/10 11:52 → 25/10 07:01. BÁO CÁO. DỪNG chờ chủ dự án

## §0 Điều lệ phiên và tóm tắt
| Trường | Lệnh | Thực tế |
|---|---|---|
| Nhánh | `p-2510` từ origin/main @df317915 | harness buộc `claude/sharp-newton-xqh5yc` (ghi ở dòng đầu); gốc đúng df317915 |
| Song song | NC-T4 (`k2c-t4-02-nc`, chỉ `reports/nc-t4/**`, `channel-k2/k2c-t4-02/nc/**`): không đụng | không fetch, không đọc, không sửa. Diff phiên không có tệp nào trong hai vùng đó |
| Vùng sửa | docs/BIBLE-KENH2.md, AUTHORSHIP.md, RIGHTS.md, COST-LEDGER.csv, channel-k2/BAI-HOC-K2.md, QUYET-DINH-TREO (chỉ mục cuối), reports/p2510/**, main | đúng. Ngoài 3 merge, phiên đổi 14 tệp (`git diff --name-only 139c3a07 HEAD`), tất cả trong vùng. Phiên không sửa `checks/` hay `checks-appeal.md` (chỉ đổi qua merge 1), `scripts/`, `design/`, `channel-k2/k2c-t4-02/**` (chỉ đổi qua merge 2–3), `tools/`, nhánh khác |
| Chi phí | API 0; giờ máy mốc 2 h | Claude API / OpenAI / Gemini / ElevenLabs / RunPod / YouTube **$0**, không gọi lần nào. 0 subagent. Không tải LFS. Giờ máy ≈ **0,5 h** (00:11 → ≈ 00:40 UTC), phần lớn là 3 lượt selftest |
| Preflight | `set -o pipefail`; chỉ commit khi có "— ĐẠT" | `reports/p2510/cam_commit.sh` chỉ commit khi có cả "— ĐẠT" và "PREFLIGHT ĐẠT"; hook pre-commit chạy lại. 4/4 commit thường ĐẠT. `--range df317915..HEAD` (1 223 tệp) ĐẠT |
| Hook | cài trước lần đẩy đầu | `pre-commit` + `pre-push` → `tools/preflight.sh`, cài 00:11 UTC; lần đẩy đầu ≈ 00:27 UTC |
| Force / amend | không | 0 force, 0 amend |
| Email / UA / khoá | che; UA CineLab; không in khoá | git dùng noreply. Diff `df317915..HEAD` có **0** chuỗi email chủ dự án. Phiên không gọi mạng ngoài git, không đọc và không in khoá |
| `lock.py` | chỉ `--verify` | chỉ `python3 -I checks/lock.py --verify`; mọi lần đều **KHỚP 1.17.6 `513c9442…`** |
| Tiến trình nền | PGID, một vòng nặng một lúc, P ≤ 2, RAM ≥ 5 GB, kiểm đĩa | selftest lượt 2 và 3 chạy nền bằng `setsid nohup` (PGID 7335 và PGID ghi ở `st3.pgid` trong scratchpad), chờ bằng vòng `until grep "== tổng"`; không `pgrep/pkill -f`. Mỗi lúc 1 lượt. RAM trống 13–15 GB, đĩa trống 16 GB |
| Đẩy ≤ 30 phút + CHECKPOINT | bắt buộc | đẩy 00:27, 00:30 và lần cuối; `reports/p2510/CHECKPOINT.md` |
| Đầu vào ở /var/tmp | không chỉ để ở đó | phiên không tạo tệp ở /var/tmp |
| Lệnh bổ sung | ghi vào CHECKPOINT | không có lệnh bổ sung nào trong phiên |
| Đã đọc | — | BAI-HOC-LL (khởi động), P2410B-BAO-CAO (khuôn), ANIMATIC-T4-BAO-CAO, PHIEU-XEM mục C, KIEM-TU-LIEU, THU-B-T4-BAO-CAO §7, §10, §11, PHIEU-THU-B, K1176-BAO-CAO §3, §4, §11–§14, RIGHTS-NHAP T4, Kinh thánh §3, §13, §14.1, §14.6, §14.7, §15, §19, QUYET-DINH-TREO, dòng tiêu đề RULES-LL. Không đọc mã trong `checks/` |

**Tóm tắt**
1. **3 merge `--no-ff`, 0 xung đột.** Đỉnh 3 nhánh trùng SHA lệnh. Sau merge 1, LOCK 1.17.5 → **1.17.6 `513c9442…` KHỚP**. Cả 3 lượt selftest đạt 15/15 bộ: **k1176 62/62**, k1175 52/52, k1174 91/91, k117 130/130, k2 129/129, ll 317/317 (§1).
2. **Kinh thánh `0ab7a06b…` → `dbafce00…`** (+13 / −1 dòng): §3 T4 ≤ 13:00; §13.4 XEM CÂM T4 8/8; §14.6 lời mới (N6); §14.7 LOOK-T4-8 (D 3D) và LOOK-T4-9 (C6); §15 (d) mở tấm nền 1666 ban ngày có điều kiện, Gemini $55/$45, góc cao ≥ 60 %, nới Gemini chờ NC-T4; §15 (j) theo THU-B + K1176; §19 (c) ngoại lệ T4 15 %, quy tắc từ T4 cho mọi tập, footage (N5) (§2).
3. **Sổ (chỉ thêm, xoá 0 dòng):** AUTHORSHIP +8, RIGHTS +1 mục (12 dòng + 5 ghi chú), COST-LEDGER +4 (ANIMATIC-T4, THU-B-T4, K-1.17.6, P-2510), BAI-HOC-K2 K59–K75, QUYET-DINH-TREO mục F (§3).
4. **Phát hiện khi ghi RIGHTS:** animatic dùng tiếng **LUAN-2** (OpenGameArt, CC0). Tiếng này chưa có dòng RIGHTS vì T3 đã LOẠI nó (AST "Vehicle" 0,165). Phiên đã thêm dòng `T4-AN-SFX-LUAN2` và ghi chú cho bản cuối: nghe lại hoặc thay bằng LUAN-1 (§3).
5. **main `df317915` → đỉnh nhánh** bằng fast-forward. Ngay trước khi đẩy, phiên fetch lại và kiểm main vẫn ở df317915; không force (§4).

## §1 Merge
| # | Nhánh @SHA (khớp lệnh) | Commit merge | Số tệp | Vùng | LOCK sau merge | selftest |
|---|---|---|---|---|---|---|
| 1 | `origin/checks-1-17-6` @`ee0bfcae` | `9e6921a3` | 50 (+3 475 / −63) | checks/ (11: LOCK, cinecheck, ll/ 9), reports/k1176 (38), checks-appeal.md (1) | **1.17.6 `513c9442fe1cb9950bdf01c3be4dc93b32c4413d9260109c86f0f5d90e5b8ec3` KHỚP** | 15/15 bộ (`selftest-1.txt`) |
| 2 | `origin/ccr-21ab5d6f-7l1yln` @`393c3b55` (ANIMATIC-T4) | `ef3faf97` | 814 (+35 912 / −0) | channel-k2/k2c-t4-02 (753), reports/animatic-t4 (33), scripts/k2ldn (27), design/k2v (1). Không chạm checks/ | KHỚP | 15/15 bộ (`selftest-2.txt`) |
| 3 | `origin/ccr-ce664665-996oyl` @`353d0f0c` (THU-B-T4) | `139c3a07` | 345 (+15 406 / −0) | channel-k2/k2c-t4-02 (259), reports/thu-b-t4 (63), scripts/k2ldn (22), design/k2v (1). Không chạm checks/ | KHỚP | 15/15 bộ (`selftest-3.txt`) |

Kết quả selftest giống nhau ở cả 3 lượt: k112 75/75 · k1121 48/48 · k1122 37/37 · k113 64/64 · k114 126/126 · k115 105/105 · k116 144/144 · k117 130/130 · k1172 74/74 · k1173 42/42 · **k1174 91/91** · **k1175 52/52** · **k1176 62/62** · **k2 129/129** · **ll 317/317**. Mọi bộ đều thoát mã 0.
- Lịch sử merge 2 mang ≈ 244 MB ảnh lát kiểm đã gỡ (ANIMATIC-T4 §11 (3)). Theo lệnh, phiên chấp nhận và không viết lại lịch sử. Mỗi tệp < 5 MB nên preflight ĐẠT; ghi bài học K64.
- THU-B-T4 tự merge `checks-1-17-5` vào nhánh của nó. Phần đó đã có trong main, nên merge 3 không đổi tệp nào trong `checks/`.

## §2 Kinh thánh `docs/BIBLE-KENH2.md`
- **SHA-256 trước:** `0ab7a06bc3c854c21fe13c7706ee0f919e914475f4f832110830c6dbc459677d` (main @df317915).
- **SHA-256 sau:** `dbafce006693054069019ccb6597ca787d15a6c03bedb7a4ffedb55a82b6772a` (commit `1b9b236b`), +13 / −1 dòng. Dòng duy nhất bị đổi là dòng tiêu đề. Diff đủ ở `reports/p2510/bible-diff.txt`; script ở `reports/p2510/sua_bible.py`, kiểm mỗi neo xuất hiện đúng 1 lần trước khi chèn. Mỗi đoạn mới ghi "(duyệt <ngày giờ>, nguyên văn: mã)". Không chép luật K: chỗ nào cần luật thì chỉ trỏ tới `checks/ll/RULES-LL.md` mục 1.17.6 (LOCK `513c9442…`).

| Chỗ | Thay đổi | Căn cứ |
|---|---|---|
| Tiêu đề | thêm "; sửa §3, §13.4, §14.6, §14.7 Look T4, §15 (d)(j), §19 (c) … (P-2510) — 25/10/2026" | — |
| §3 Khuôn lời | +1 dòng: T4 bản cuối **≤ 13:00** (780 s), animatic 730,1 s | 25/10 07:01 N3 |
| §13.4 | +1 đoạn "13.4 bổ sung — T4": chủ dự án XEM CÂM **8/8** ("có thể hiểu được cả 8"), ĐẠT phần chủ dự án; AI tham khảo 7,5/8 | 25/10 06:56 |
| §14.6 Âm thanh | +1 dòng N6: lời mới cho điểm nhấn ≤ 10 câu, ≤ 2 000 ký tự, qua kiểm nguồn; G1 vẫn chờ Đ5 | 25/10 07:01 N6 |
| §14.7 Look T4 | +**LOOK-T4-8**: toàn cảnh bản cuối = D 3D (`look3`, cờ d), không vân nướng AI, nâng vật liệu 3D toà 2026 có tên · +**LOOK-T4-9 (C6)**: P1 xoay ≈ 4° sang trái ở bản cuối (vòm ≈ 30 %), giữ điểm đứng + fov 36°, dựng lại ≈ 9 shot P1; animatic giữ hướng cũ | 24/10 15:25 (D1, D2, T3, T4); 25/10 06:56 (C6 = b) |
| §15 (d) | +1 dòng "(d) cập nhật 24–25/10 (P-2510)": (1) mở tấm nền 1666 ban ngày ở bản cuối, chỉ tấm qua 1.17.6, trượt → 3D; thay câu "chưa có quyết định"; đêm/lửa vẫn không · (2) Gemini T4 **$55**, mốc **$45** (thay $35/$30; khai `ngan_sach_gemini_usd: 55`, `ngan_sach_gemini_moc_usd: 45`) · (3) góc cao ≥ 60 % giữ · (4) nới Gemini + cận/trung (nhận xét mục 3): danh sách và mọi chỗ đụng (f) chờ NC-T4, (f) giữ tới lúc đó | 24/10 12:29; 25/10 07:01 N1, N2; 25/10 06:56 mục 3 |
| §15 (j) | +1 dòng "(j) cập nhật sau THU-B-T4 + K-1.17.6": chọn khung B1 V2 / B2, B3 B chiếu / D1, D2 D 3D; **B chỉ nhà ≥ 4 px/m** (`be_mat_nha_px_m_min: 4`); tỉ số bóng khi máy cố định; chiếu 3D khi máy di chuyển chỉ sau khi sửa và qua (d), tạm chỉ máy cố định; soi hộp (w) bắt buộc; toàn cảnh D 3D + nâng vật liệu toà 2026 có tên; không vân nướng AI ở toàn cảnh; điều kiện (2) giữ (chỉ tấm qua 1.17.6); sàn Y nhấp nháy ở phiên K đo lại; **vẫn chỉ áp ở bản cuối** | 24/10 15:25; 24/10 17:54 (K1176-D2, D3, D6) |
| §19 (c) | +2 đoạn: **(c) ngoại lệ T4 và cách kết hợp tư liệu từ T4**: (1) T4 trần 15 % (`tu_lieu_tran_pct: 15`); (2) từ T4, mọi tập: tư liệu chỉ chồng shot 3D, không chồng/ghép liền clip Omni, ≤ 10 s/lần (TU-LIEU-10, TU-LIEU-OMNI); (3) 5 vị trí + Ogilby D13; (4) Hollar -0 sau / -1 trước cháy, "published 1666" · **(c) ảnh và footage thật**: N5 (miễn phí giấy phép thương mại rõ, không NC/ND, mua khi chủ dự án duyệt giá, RIGHTS + `licenses/` trước khi lên hình); danh sách chờ NC-T4 | 24/10 12:48, 12:52; 24/10 17:54 (K1176-D4); 25/10 06:56 mục 4; 25/10 07:01 N5 |

Ghi chú: dòng "Phạm vi" cũ của §19 vẫn ghi "tư liệu + tranh khắc + thẻ ≤ 10 %". Phiên giữ nguyên dòng đó, vì đoạn ngoại lệ mới ghi rõ là thay 10 % cho riêng T4.

## §3 Sổ đã ghi (chỉ thêm, xoá 0 dòng; commit `24c2d377`, dòng P-2510 ở commit cuối)
| Sổ | Thêm |
|---|---|
| `AUTHORSHIP.md` | **+8 dòng.** (1) Bổ sung giờ **24/10 11:52** cho hai dòng P-2410b (K1175-D1…D7, LFS); hai dòng cũ giữ nguyên. (2) 12:29 mở tấm nền 1666 ngày, A. (3) 12:48 lệnh bổ sung Hollar (ANIMATIC-T4 ghi giờ áp 12:55). (4) 12:52 cách kết hợp tư liệu. (5) 15:25 phiếu THU-B, B1…D2 và T1–T4. (6) 17:54 K1176-D1…D6. (7) 25/10 06:56 XEM CÂM 8/8, C1–C14, F1–F5 và nhận xét nguyên văn 1–4. (8) 25/10 07:01 N1–N6. Mỗi dòng ghi nguyên văn, nghĩa, đóng góp biểu đạt và phần do AI đề xuất |
| `RIGHTS.md` | **+1 mục** "T4 London — animatic + THU-B-T4 + K-1.17.6": 7 dòng tư liệu đã dùng hoặc đã duyệt vị trí, kèm ghi công đã kiểm (Hollar -1 trước cháy / -0 sau cháy → H1-18; YCBA 266 tranh sơn dầu; Rijks Monument nay ở H2-06; Doornick; LoC Wren "engraved 1767"; NGA Wren), mỗi dòng trỏ về dòng giấy phép `T4-TL-*` đã có. Thêm 5 bài nhạc Scott Buckley CC BY 4.0 (= K2-MUS-8, -10…-13); SFX 27 tiếng (26 = K2-SFX-T3-*, cộng **LUAN-2 dòng mới**); ảnh đầu OpenAI + tấm nền; clip Omni (dự án, C2PA theo sổ). Ghi chú: vị trí tư liệu 12:52; giọng G1 chờ Đ5; **THU-B 10 ảnh AI chưa vào phim**; K-1.17.6 không tài sản mới |
| `COST-LEDGER.csv` | **+4 dòng.** ANIMATIC-T4: Gemini $7,10 (T4 tổng $8,54), OpenAI $4,61, Claude API $4,83, ≈ 11,6 h. THU-B-T4: OpenAI $1,33, Claude $0,82, ≈ 3,6 h. K-1.17.6: Claude $0,1199, OpenAI $0,0798, ≈ 3,0 h, LFS 1,79 GB. P-2510: API 0, ≈ 0,5 h. Số lấy từ §12/§14, §7/§10, §11/§13 của từng báo cáo |
| `channel-k2/BAI-HOC-K2.md` | **K59–K75.** ANIMATIC-T4 §14 (1)–(5) = K59–K63; sự cố 244 MB = K64 (đề xuất phiên Nền tảng thêm ngưỡng tổng cỡ mỗi commit). THU-B §10 (1)–(5) = K65–K69. K-1.17.6 §13 (2)–(5) = K70–K73; §13 (1) = **K75 "pgrep -f / pkill -f khớp chính dòng lệnh — LẶP lần 4"**, đề xuất phiên Nền tảng chặn bằng công cụ. Bài học điều phối = **K74**: soi khung mỗi 10 s bắt được lỗi sai sử (H2-13 thiếu mái vòm 1711) mà kiểm 2 tầng bỏ sót, nên kiểm lỗi thời đại phải hỏi "công trình mốc của năm đó có mặt chưa" |
| `reports/k1173/QUYET-DINH-TREO.md` | **mục F** (chỉ thêm ở cuối): bảng đã quyết (10 dòng; V1-1666 và THU-B của mục E chuyển sang đã quyết) và bảng còn treo (NC-T4, K-1.17.7, ANIMATIC-T4-V2, KN THU-B → appeal, LOOK-T9c, Đ5) |

## §4 main
- Trước: `origin/main` @`df3179151439151b43a94c4ebb6ad21267c5022d`.
- Sau: đỉnh `claude/sharp-newton-xqh5yc` (commit cuối "P-2510: báo cáo … — DỪNG chờ chủ dự án"), đẩy bằng `git push origin HEAD:main` (fast-forward, không force). Ngay trước khi đẩy đã `git fetch origin main` và kiểm `origin/main` vẫn là `df317915` và là tổ tiên của HEAD. SHA sau được ghi trong CHECKPOINT và tin nhắn cuối phiên. Báo cáo này nằm trong chính commit đó, nên không tự ghi được SHA của mình.

## §5 Chỉ số trong ±5 % quanh ngưỡng (luật cứng)
Phiên P không đo chỉ số hình hay âm. Các số sát ngưỡng của phiên nguồn đã được nêu tên ở ANIMATIC-T4 §13, THU-B-T4 §9 và K1176 §10, và không đổi khi merge. Ví dụ: M-d 20,36 %, K-LAI-1 20,4 %, TU-LIEU-10 9,66 %, OpenAI $4,61 / mốc $5, Claude $4,83 / mốc $5.

## §6 Việc chờ chủ dự án
1. **NC-T4** (đang chạy song song): duyệt danh sách điểm nhấn (sự kiện, nhân vật, công trình — cận/trung, Gemini ≤ $55) và tư liệu/footage thật. Nếu danh sách cần công trình có tên làm chủ thể hoặc nhân vật có tên trong M-d thì phải quyết nới §15 (f) (Kinh thánh §15 (d) (4) đang giữ (f)).
2. **K-1.17.7:** mở phiên K cho K-LAI-1 theo Q2 (C11), câu A1–A5 của ANIMATIC-T4 §9.3 + C13, sàn Y nhấp nháy (K1176-D6), đo lại tấm BMN ≥ 4 px/m (và chiếu 3D sau khi sửa, D3), hiệu chuẩn lại BIEN-CO-V trên animatic T4.
3. **ANIMATIC-T4-V2:** mở sau NC-T4. Sửa nhận xét 1 (10 s đầu và các khoảnh khắc đứng), F1/F2/F4/F5, điểm nhấn; ≤ 13:00.
4. **LUAN-2 (SFX):** bản cuối nghe lại hoặc thay bằng LUAN-1 (T3 đã loại tiếng này; RIGHTS `T4-AN-SFX-LUAN2`).
5. **Đ5:** quyền giọng G1 cho bản phát hành (chờ thư ElevenLabs).
6. THU-B-T4 §11 mục 2 đề nghị P chuyển `reports/thu-b-t4/khieu-nai-K.md` vào `checks-appeal.md`. Lệnh P-2510 không cho sửa tệp đó, và K-1.17.6 đã xử lý KN-1…KN-6. Nếu vẫn muốn ghi vào hồ sơ appeal thì giao cho phiên K.

**DỪNG chờ chủ dự án.**
