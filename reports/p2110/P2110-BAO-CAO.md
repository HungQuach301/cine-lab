Nhánh thật: **`p-2110`** (đúng tên lệnh; đã đẩy `origin/p-2110`). Tạo từ `origin/main` @`bc7e96d1`. Harness của phiên gán nhánh `claude/friendly-franklin-bzbz9j` (cùng gốc `bc7e96d1`), phiên không dùng nhánh đó. `main` cập nhật fast-forward ở §6.

# PHIÊN P-2110: merge ANIMATIC-T3 + NC-N2P, Kinh thánh §14.7 + §15 + §16, sổ. BÁO CÁO. DỪNG chờ chủ dự án

```text
ĐIỀU LỆ PHIÊN P-2110                                           | thực tế
Loại phiên:        P (điều phối)                                | đúng
Nhánh:             p-2110 từ origin/main @bc7e96d1               | đúng
KHÔNG sửa:         checks/, design/, scripts/, loi-khoa.txt      | đúng: 0 tệp trong 41e0c8fd..HEAD (phần của P-2110); loi-khoa.txt 51d1c773… trước = sau
                                                                 | (34 tệp checks/design/scripts trong bc7e96d1..HEAD là của ANIMATIC-T3/V7C, vào bằng ff)
lock.py:           chỉ --verify                                  | đúng; mọi lần KHỚP 1.16.1 a3c39873…
Phiên song song:   ANIMATIC-T3-V2 (k2c-t3-anim-v2), K-1.17       | không đọc, không đụng, không merge
Force:             không                                         | đúng (mọi push không force)
Chi phí:           Claude/OpenAI/ElevenLabs/Gemini/YouTube 0     | $0 · $0 · 0 ký tự (không gọi) · $0 · 0 đơn vị
Giờ máy:           mốc theo dõi 1,5 h                            | ≈ 0,5 h
Preflight:         --staged mỗi commit; --range trước khi đẩy    | --staged ĐẠT 4/4; --range bc7e96d1..HEAD ĐẠT (707 tệp), không trượt ngoại lệ nào
Email:             che; không vào header/URL/payload/UA           | 0 email chủ dự án trong diff; UA mọi GET: "CineLab-research (+https://github.com/HungQuach301/cine-lab)"
Việc dở:           đẩy ≤ 30 phút + CHECKPOINT                    | đẩy origin/p-2110 sau commit Kinh thánh (kèm CHECKPOINT.md) và ở cuối
Dừng hỏi:          không dừng giữa chừng                          | đúng
```

## 0. Tóm tắt
| Mục | Kết quả |
|---|---|
| Merge | (a) `git merge --ff-only origin/ccr-d189108f-6mcz9k` → **`41e0c8fd`** (ANIMATIC-T3, gồm V7C `47a0f55a`: kiểm là tổ tiên). (b) `git merge --no-ff origin/nc-n2p` (`9cb001d1`) → **`c7675665`**, **0 xung đột**; nc-n2p chỉ đổi `reports/` (0 tệp ngoài, kiểm bằng máy). Sau merge: lock KHỚP, selftest 144/105/126, LOI-KHOA 3/3 (§1) |
| Kinh thánh | `docs/BIBLE-KENH2.md` SHA-256 `50554dcc…` → **`14ca13aaed89aade183caf73cc044393c223fb07e7a22bf0b3c56a43e1346429`**; +28 / −1; thêm §14.7, §15 (a)–(i), §16; tiêu đề thêm "§14.7 + §15 + §16 — 21/10/2026" (§2) |
| Sổ | AUTHORSHIP **+12** dòng (21/10) · RIGHTS **+5** (3 nguồn văn bản T4 + 2 dòng đầu ra AI NC-N2P "chỉ nghiên cứu") · COST-LEDGER **+3** (76 dòng × 20 cột) · BAI-HOC **#118–#122** · HANG-DOI cập nhật 21/10 (§3) |
| `T3-loi-moc.json` | **Tái tạo TRÙNG SHA `5f74cf4a…`** bằng chạy lại `reports/p2010b/ghep_lai.py` (không sửa tay). Đã thêm bằng `git add -f`; `SHA256SUMS` giữ nguyên, **14/14 OK** (§4) |
| Kiểm cuối | lock **KHỚP 1.16.1** · selftest k116 **144/144** · k115 **105/105** · k114 **126/126** · LOI-KHOA **3/3** · preflight `--range` **ĐẠT** · 0 email (§5) |
| main | `bc7e96d1` → **commit cuối của nhánh `p-2110`** (commit chứa tệp này), fast-forward, không force (§6) |

## 1. Merge
| Bước | Lệnh | Kết quả |
|---|---|---|
| Kiểm trước | `git merge-base --is-ancestor origin/main origin/ccr-d189108f-6mcz9k`; `… 47a0f55a origin/ccr-d189108f-6mcz9k`; `git merge-tree --write-tree` animatic × nc-n2p | tổ tiên: có; V7C trong animatic: có; merge-tree: 0 xung đột (cây `3df48cad`) |
| (a) | `git merge --ff-only origin/ccr-d189108f-6mcz9k` | `bc7e96d1` → `41e0c8fd` |
| (b) | `git merge --no-ff origin/nc-n2p` | `c7675665` (349 tệp, tất cả trong `reports/`) |
| Sau merge | `checks/lock.py --verify`; selftest; `sha256sum -c LOI-KHOA.sha256` | KHỚP `a3c39873751805a7a0a5e2b544bc2c28630d78e87725b777d3c7ba1c77cc2d2b`; 144/144 · 105/105 · 126/126; 3/3 OK |

## 2. Kinh thánh `docs/BIBLE-KENH2.md` — `reports/p2110/sua_bible.py`, `sua-bible.json`
- SHA trước **`50554dcce70fab49b20906aeea598dd0c4bc1130b042d3e817b895add56e83dd`** (script kiểm đúng bản P-2010b trước khi sửa) → sau **`14ca13aaed89aade183caf73cc044393c223fb07e7a22bf0b3c56a43e1346429`**.
- Mỗi neo/thay kiểm **đúng 1 lần**; sau sửa kiểm `### 14.7`, `## 15.`, `## 16.` mỗi cái đúng 1 lần.
- Nguyên văn được lấy **bằng máy** từ tệp nguồn, không gõ lại: khối LOOK từ `LOOK-KHOA.md` (SHA `72add9b31ba3445348fe0ee20b5b5a3b722d237683971175f5ec99b39a8d38ec`); (a)–(e) từ `reports/NC-N2P-BAO-CAO.md` §6.3 (script kiểm đủ 6 dòng trích, đúng thứ tự a–e).

| Chỗ | Trước → sau |
|---|---|
| Tiêu đề | "…; §14 + sửa 20/10, 20/10 22:34)" → "…; §14 + sửa 20/10, 20/10 22:34; §14.7 + §15 + §16 — 21/10/2026)" |
| §14.7 (mới, sau §14.6) | "### 14.7 Look T3 (chủ dự án chọn mù 21/10/2026 07:05)" + 6 dòng nguyên văn `LOOK-KHOA.md` §1 (LOOK-1…LOOK-5 + "Tham chiếu ngữ pháp máy đã kiểm…") + "Thông số tái lập: channel-k2/k2c-t3-01/LOOK-KHOA.md (SHA 72add9b3…)" (SHA đầy đủ trong tệp) + "R1–R4 (chủ dự án đồng ý 21/10 21:05): R1 … R1–R4 thắng LOOK-2 ở shot có chủ thể trên eo đất." + "Mở đầu tập: … (chủ dự án 21/10 21:09)." — đúng chữ trong lệnh |
| §15 tiêu đề | nháp "§15. Luật AI N2+ (áp từ T4; chủ dự án duyệt …/10/2026)." → "## 15. Luật AI N2+ (áp từ T4; chủ dự án duyệt 21/10/2026 15:59)" |
| §15 dòng ghi chú (**P thêm**) | "(Nháp `reports/NC-N2P-BAO-CAO.md` §6.3 (a)–(e) chép nguyên văn, trừ các chỗ chủ dự án quyết: (b) khớp màu; (d) thay toàn bộ; thêm (f)–(i).)" — để truy nguồn; lệnh không nêu, chủ dự án xem lại |
| §15 (a), (c), (e) | nguyên văn nháp |
| §15 (b) sửa (i) | "rồi ghép lớp (a) + **khớp màu về render trên lớp nền**;" → "rồi ghép lớp (a) + **khớp màu render VÀO tông tấm nền AI (không kéo tấm AI về tông render); vật lớp (a) nằm trên nền đất (vd dãy trại) dựng lại có vân/bóng cùng tông tấm nền**;" — phần còn lại của (b) nguyên văn |
| §15 (d) sửa (ii) | nháp "(d) Trần T4: tấm nền N2+ ≤ 50 % thời lượng, chỉ shot timelapse máy cố định; video AI 0 %; tổng khung có AI (N1 + N2 + N2+) ≤ 50 %; nâng ở tập sau khi bình luận chê AI ≤ 2 % (§11.3)." → thay toàn bộ bằng câu (d) trong lệnh |
| §15 (f), (g), (h), (i) | thêm, đúng chữ trong lệnh (iii)–(vi) |
| §16 (mới) | "## 16. Hậu kỳ chuẩn mỗi tập (chủ dự án duyệt 21/10 20:10)" + câu "Phiên bản cuối gồm: …" đúng chữ trong lệnh |

**Chỗ vênh P thấy, chưa sửa (chủ dự án quyết):**
1. §15 (b) giữ nguyên văn nháp câu "**Video AI (video→video) không dùng** cho tới khi một mô hình qua cổng (c) với tỷ lệ làm lại ≤ 3 lượt/đoạn." Câu (d) mới cho phép "video AI chỉ cho minh hoạ M-d". Hai câu đọc chung được (video→video cấm; video AI đứng riêng M-d được), nhưng câu (b) có thể hiểu là cấm mọi video AI. Đề xuất: thêm vào (b) "(trừ minh hoạ M-d, xem (d), (f))".
2. Câu (g) ghi "không nguồn thuộc lớp (c)", nhưng (a) gọi các lớp bằng tên, không bằng chữ cái. Theo thứ tự trong (a), "lớp (c)" là LỚP NỀN. Nếu ý chủ dự án là LỚP CHI TIẾT MINH HOẠ (lớp thứ hai) thì cần sửa chữ.
3. §14.1 (d) "Tổng khung có AI (N1 + N2) ≤ 20 % ở T3" vẫn đúng với §15 (i) (minh hoạ ≤ 20 %), nếu vòng sửa T3 không dùng thêm khung N1.

## 3. Sổ
### 3.1 AUTHORSHIP (+12 dòng, ngày 2026-10-21)
Ghi theo đúng chữ trong lệnh P-2110. Câu chủ dự án có ngoặc kép trong lệnh được ghi là "Nguyên văn: "…"". Câu lệnh tóm tắt được ghi "Nguyên văn (theo lệnh P-2110): …". Các mốc: 07:05 · 10:03 · 10:11 · 11:13 · 15:56 · 15:59 · 17:50 · 20:10 · 20:38 · 21:05–21:09 · 21:15 · 21:22. Mỗi dòng có cột đóng góp biểu đạt của con người và chỉ đến chỗ trong Kinh thánh (§14.7, §15, §16).

### 3.2 COST-LEDGER (+3; `reports/p2110/ghi_cost.py`; kiểm 76 dòng × 20 cột)
| Phiên | Claude API | Khác | Giờ máy | Nguồn |
|---|---|---|---|---|
| ANIMATIC-T3 | **$0,752** (§0 làm tròn $0,75; `xem-cam/cost.jsonl`) | OpenAI/RunPod/EL/Gemini/YouTube 0 | 13,5 h | `reports/animatic-t3/ANIMATIC-BAO-CAO.md` dòng 32, 66, 162–165 |
| NC-N2P | **$6,946** theo sổ `cost.jsonl` (49 lượt; P cộng lại khớp) | **ghi chú:** báo cáo §8 ghi thêm **$1,422 q_thoi_dai.py không có dòng sổ** (Claude tổng theo báo cáo $8,37). OpenAI $5,77 (ảnh $2,065 + chữ/nhìn $3,708). Gemini $9,92 | 3,5 h | `reports/NC-N2P-BAO-CAO.md` §0, §8 |
| P-2110 | 0 | mọi API 0 | ≈ 0,5 h | tệp này |

### 3.3 RIGHTS (+5, mục mới "Kênh 2 — nguồn văn bản T4 London 1666 + đầu ra AI NC-N2P")
| Mã | Nội dung | Giấy phép (cách lấy) | SHA |
|---|---|---|---|
| N2P-T4-1 | Pepys, Gutenberg #4167 | PD Mỹ. Câu đầu tệp Gutenberg ghi nguyên văn; tải lại 21/10, SHA khớp | `8a7ec38e…` |
| N2P-T4-2 | Evelyn, Gutenberg #42081 | như trên | `912a1791…` |
| N2P-T4-3 | EEBO-TCP A63370 (EarlyPrint) | Tệp chữ distantreader không kèm câu giấy phép. P đọc khối `<availability>` của bản TEI gốc (TCP GitHub) và ghi nguyên văn: "… This Phase I text is available for reuse, according to the terms of Creative Commons 0 1.0 Universal …" → **CC0 1.0** (khớp NC-N2P §6.4) | `1bf5c146…` |
| N2P-AI-1 | OpenAI `gpt-image-2.5-sunburst-2026-09-08`: 27 ảnh (28 lệnh, 1 lỗi 400), C2PA 27/27 | OpenAI Services Agreement §4.1 (nguyên văn như dòng P1810B-AI; trang 403 trong NC-N2P) | theo sổ `so-ai.jsonl` |
| N2P-AI-2 | Gemini `gemini-omni-1.1-flash`: 9 clip ra (11 lệnh), C2PA + SynthID 9/9 | Gemini API Additional Terms (Last updated 2026-04-28), mục "Use of Generated Content", P đọc 21/10 và ghi nguyên văn ("Google won't claim ownership over that content…") | theo sổ `so-ai-gemini.jsonl` |

Hai dòng AI có phạm vi **"Chỉ nghiên cứu, không lên hình T3"**. Năm đoạn minh hoạ Omni của vòng sửa T3 thuộc phiên ANIMATIC-T3-V2. Chúng sẽ có dòng RIGHTS riêng khi merge.

### 3.4 BAI-HOC (`reports/m3/BAI-HOC-LL.md`, mục mới)
- #118: V7C-D6 (a)–(e).
- #119: N2P-D7 (a)–(e).
- #120: stamp cảnh băm cả `design/k2v/tl/*.js` → gom mọi sửa mã thành một lượt, chốt mã trước đợt dựng.
- #121: `alimiter` tự bù mức khi xuất bản xem → `level=disabled` + đo LUFS.
- #122: container khởi động lại giữa phiên (đĩa `/var/tmp` còn, tiến trình mất) → checkpoint + `--resume`.

### 3.5 HANG-DOI (`channel-k2/HANG-DOI.md`, mục "CẬP NHẬT 21/10/2026")
- T3: vòng sửa animatic V2 (đang chạy, 5 minh hoạ Omni) → bản cuối (màu + SFX + cú lặn Cycles GPU) → G2 → đăng.
- T4 London 1666: áp §15 (+ §16). Bộ kiểm N2+ vào `checks/`: chờ giao phiên K.

## 4. `channel-k2/k2c-t3-01/am-thanh/master/T3-loi-moc.json`
- Tệp vắng trên `main` vì `channel-k2/.gitignore` dòng 2 `*.json`. `SHA256SUMS` (P-2010b) ghi `5f74cf4af91a2e2b678dc8ed576ca97eca91715e8460e3e69b223637c04b596e`.
- **Tái tạo:**
  1. `git lfs pull` 11 MP3 `nguon-lich-su/` (SHA khớp 11/11) và chép vào `$P_OUT/lich-su/`.
  2. Chạy `reports/p2010b/ghep_lai.py` (không sửa mã) → `$P_OUT/stem/moc.json` = nội dung `T3-loi-moc.json`.
- Lần 1 với `P_OUT=/var/tmp/cine-out/p2110` cho SHA `a8bb4658…`. Lý do: trường `tep` của 3 câu thay ghi đường dẫn tuyệt đối `$P_OUT/lich-su/…`. Thay tiền tố bằng `/var/tmp/cine-out/p2010b/` thì khớp `5f74cf4a…`.
- Lần 2 chạy thật với `P_OUT=/var/tmp/cine-out/p2010b` (đúng đường P-2010b) → **`5f74cf4a…` TRÙNG**. Stem cả hai lần `79ac3589…` = KL42.
- `reports/p2010b/ghep-lai.json` do script ghi lại **trùng byte** bản trong git, nên không đổi.
- Thêm bằng `git add -f`. `SHA256SUMS` **giữ nguyên dòng**. `grep -v '^#' SHA256SUMS | sha256sum -c` → **14/14 OK** (WAV/FLAC kéo LFS để kiểm).
- Ghi chú: tệp chứa đường dẫn máy cục bộ `/var/tmp/cine-out/p2010b/lich-su/…` (3 chỗ). Không phải bí mật, nhưng không di chuyển được giữa máy.

## 5. Kiểm cuối
| Kiểm | Kết quả |
|---|---|
| `checks/lock.py --verify` | **KHỚP** 1.16.1 `a3c39873…` (sau merge, mỗi commit, trước và sau cập nhật main) |
| selftest (P chỉ chạy, không đọc mã) | `selftest_k116.py` **144/144** (23 nhóm) · `selftest_k115.py` **105/105** (15 nhóm) · `selftest_k114.py` **126/126** |
| `LOI-KHOA.sha256` | **3/3 OK**; `loi-khoa.txt` `51d1c773…` trước = sau |
| preflight `--range bc7e96d1..HEAD` | **ĐẠT** — 707 tệp, không trượt ngoại lệ nào |
| Email | 0 email chủ dự án trong diff. Địa chỉ duy nhất là `noreply@anthropic.com` (dòng ghi công trong một tệp của ANIMATIC-T3), không phải email chủ dự án |
| Vùng cấm | `git diff --name-only 41e0c8fd..HEAD -- checks/ design/ scripts/` = 0 tệp |

## 6. main
- Trước: `main` = `origin/main` = **`bc7e96d1`**. Kiểm lại ngay trước khi cập nhật: `git fetch origin main` vẫn là `bc7e96d1`, và nó là tổ tiên của `p-2110`.
- `git checkout main && git merge --ff-only p-2110` → `main` = **commit cuối của `p-2110`** (commit chứa tệp này, "… DỪNG chờ chủ dự án"). `lock.py --verify` trên main: KHỚP. `git push origin main`, không force.

## 7. Chỉ số trong ±5 % quanh ngưỡng
| Chỉ số | Số đo | Ngưỡng/mốc | Ghi chú |
|---|---|---|---|
| — | — | — | Phiên không đo chỉ số hình/âm. Giờ máy ≈ 0,5 h so với mốc 1,5 h, xa ngưỡng |

## 8. Việc chờ chủ dự án
1. **Duyệt P-2110**: §14.7, §15, §16 như đã ghi. Xem dòng ghi chú P thêm ở đầu §15, và ba chỗ vênh ở §2: câu "Video AI không dùng" trong (b); "lớp (c)" trong (g); trần §14.1 (d) cho vòng sửa T3.
2. **Phiên ANIMATIC-T3-V2** (đang chạy): khi xong, P merge và ghi RIGHTS cho 5 đoạn minh hoạ Omni.
3. **Phiên K-1.17** (đang chạy): giao/nhận bộ kiểm N2+ (§15 (h), N2P-D4) nếu chưa nằm trong phạm vi K-1.17.
4. **Gemini**: đối chiếu số Google thực tính với sổ NC-N2P ($9,92). Nạp thêm ₫350.000 cho vòng sửa T3 (AUTHORSHIP 21:15).
5. **ElevenLabs**: thư hỏi Beta Services (giọng G1 Voice Design) đang chờ trả lời.
6. **LFS**: `main` đã vượt mốc cảnh báo 800 MB từ P-2010b. P-2110 không thêm LFS (T3-loi-moc.json là JSON 1 357 dòng, ngoài LFS).
7. Lời hứa tiêu đề T3 theo khuôn §14.5 vẫn chờ chốt (P-2010b).

## Tệp
- `reports/p2110/sua_bible.py`, `sua-bible.json`: sửa Kinh thánh + SHA trước/sau.
- `reports/p2110/ghi_cost.py`: COST-LEDGER.
- `reports/p2110/CHECKPOINT.md`: mốc việc dở.
