# PHIÊN P-1710: hợp nhất 17/10/2026 (chủ dự án duyệt VV1–VV4, RR1–RR3, TT1–TT6). BÁO CÁO. DỪNG chờ chủ dự án

```text
ĐIỀU LỆ PHIÊN P-1710                                        | thực tế
Loại phiên:        P (điều phối)                             | đúng
Nhánh:             p-1710, tạo từ origin/main @ 7255aa4      | đúng; đẩy p-1710. main KHÔNG cập nhật (xem §0.4)
Tệp được sửa:      sổ dùng chung, .gitignore/.gitattributes, | đúng như cột trái; docs/BIBLE-KENH2.md GIỮ bản main (§0.1)
                   tools/lfs-allow.txt, reports/, HANG-DOI,  |
                   BAI-HOC-K2                                |
Tệp KHÔNG sửa:     checks/ · bible/ · docs/BIBLE-KENH2.md    | không sửa; checks/ chỉ chạy selftest/lock, không đọc mã
Trần chi phí:      Claude API $0 · ElevenLabs 0 · YouTube 0  | $0 · 0 ký tự · 0 đơn vị
                   · giờ máy ≤ 1,5 h                         | ≈ 1,2 h thời gian thực; ≈ 2,5 giờ-tiến trình (§0.8)
Preflight:         BẮT BUỘC                                  | ĐẠT (1 455 tệp, lock KHỚP) trước khi đẩy
Merge:             13 nhánh theo thứ tự; main ff nếu mọi kiểm đạt | 13/13 merge; main KHÔNG ff (versions lệch kỳ vọng)
```

## 0. Tóm tắt
### 0.1 Từng merge (mỗi merge một commit `--no-ff`, không squash, không merge nhánh nào khác)
| # | Nhánh @ SHA | Commit merge | Xung đột | Cách giải |
|---|---|---|---|---|
| 1 | `origin/checks/v1.12.2` @0f96a11 (gồm 1.11 → 1.12 → 1.12.1) | `c08ed3d5` | không | — |
| 2 | `origin/am-thanh` @8a8bff4 | **không có commit** | — | nhánh **đã nằm trọn trong** `checks/v1.12.2` (`git merge-base --is-ancestor` đúng); merge = "Already up to date" |
| 3 | `origin/teardown-fon` @0d0bb80 | `9150e41a` | không | — (đã kiểm: chỉ `TEARDOWN-FON.md` + 6 tệp JSON mô tả bằng lời/số; **không có tệp media đối thủ**, thumbnail chỉ mô tả, không lưu ảnh) |
| 4 | `origin/v5a` @3e740e9 | `fda9a1cc` | **RIGHTS.md, COST-LEDGER.csv** | RIGHTS: giữ cả hai khối, khối AM (02:10 15/10) trước khối V5a (13:05 15/10). COST-LEDGER: giữ nguyên vị trí mọi dòng đã có trên main; dòng mới (AM, V5a) hợp lại, bỏ dòng trùng y hệt, sắp theo `ngay` |
| 5 | `origin/timelapse-rd` @23a668d | `fc2ef92f` | không | — |
| 6 | `origin/tienky-thanhpho` @3aeba42 | `600d60b9` | không | — |
| 7 | `origin/k2c-t3-tienky` @d8e83cc | `11317802` | không | — |
| 8 | `origin/k2c-t4-tienky` @3310903 | `468e5b86` | không | — |
| 9 | `origin/k2c-t5-tienky` @dbc4542 | `fe4a73eb` | không | — |
| 10 | `origin/k2c-t6-tienky` @0b52aba | `5d378da1` | không | — |
| 11 | `origin/gpu-rd` @82e6036 | `b84a72a2` | không | — |
| 12 | `origin/v5b2a` @b35995e (gồm v5b1 → v5b1b) | `ce32aaa3` | không | — |
| 13 | `origin/k2c-t2` @86731f5 | `5073067b` | **RIGHTS.md** | giữ cả hai khối theo thời gian: khối T2 tạo 02:01 15/10 (`efb74c2e`) đứng **trước** khối AM 02:10 và V5a 13:05 |

- **Giải xung đột:** cả ba lần làm bằng một công cụ cố định (giữ cả hai phía, xếp theo giờ commit cuối chạm tệp mỗi phía; sổ chi phí hợp dòng). Sau đó kiểm lại giờ tạo khối thật bằng `git log -S`. Không còn dấu xung đột (`git grep '^<<<<<<<'` rỗng).
- **docs/BIBLE-KENH2.md:** `k2c-t2` có commit `72184052` sửa 3 dòng Kinh thánh (duyệt 15/10: footage ≥ 720p/khung trong khung + DVIDS; xu có độ dày; §8 cổng hình G2 ≥ 7,0 và không thua T1). Lệnh nói **không sửa** tệp này, vì Kinh thánh sẽ commit nguyên văn ở bước 0 của T3. Vì vậy commit merge 13 **giữ bản của main** (`git checkout origin/main -- docs/BIBLE-KENH2.md`); `git diff origin/main HEAD -- docs/BIBLE-KENH2.md` rỗng. Ba dòng đó vẫn nằm trong lịch sử nhánh `k2c-t2`, cần đưa vào bản nguyên văn ở bước 0 T3 → **việc chờ 1**.
- **Mã sổ trùng:** `P-K2G` và `P-K2C` có nhiều dòng từ trước (khác cột `cong`), không phải do merge.

### 0.2 Kiểm sau merge: trước/sau
| Kiểm | Trước (main 7255aa4) | Sau (p-1710) | Kết quả |
|---|---|---|---|
| `checks/LOCK` + `lock.py --verify` | 1.10.2 `c598467f…` KHỚP | **1.12.2 `81789fad2e7a986a092cd2c0659a1cb93b3b5f9e87e4cfc79f7a93e316506e93` KHỚP** | **ĐẠT** |
| `selftest_k1122` | không có trên main | **37/37** (1 s) | ĐẠT (= số K báo) |
| `selftest_k1121` | không có trên main | **48/48** (10 s) | ĐẠT |
| `selftest_k112` | không có trên main | **75/75** (9 s) | ĐẠT |
| `selftest_k2` | không có trên main | **129/129** (43 s) | ĐẠT |
| `selftest_ll` | **317/317** (509 s) | **317/317** (132 s) | ĐẠT, không giảm |
| L1 `checks/selftest/run_selftest.py` | **TẤT CẢ KHỚP**: 142 dòng OK, E2E `run.py` 16 luật PASS, bẩn exit 1 (50,3 phút, chạy ở worktree main) | **TẤT CẢ KHỚP**: 142 dòng OK, E2E 16 luật PASS, bẩn exit 1 (49,9 phút) | ĐẠT, không giảm. Hai lượt chạy song song nên mỗi lượt lâu gấp đôi số K báo (25,8 phút). Tệp `reports/checks-selftest/` do L1 tự ghi đã hoàn nguyên, không commit |
| `bash tools/preflight.sh --range origin/main..HEAD` | — | **ĐẠT**: 1 455 tệp, lock KHỚP | ĐẠT |
| `bash scripts/env/verify.sh` | 9 PASS, 4 FAIL (three.js, tifffile/pyshp, k2v node_modules, Freesound 403) → cài theo gợi ý → **13 PASS, 0 FAIL** | **13 PASS, 0 FAIL** | ĐẠT (Freesound sau đó PASS) |
| `versions.py check channel-k2/k2c-t2-01/VERSIONS.yaml` | (T2 §14.1: còn CHẶN `served_models` đã duyệt + BÁO CLI) | **5 CHẶN + 2 BÁO** (bảng dưới) | **KHÔNG khớp kỳ vọng** "chỉ còn served_models/CLI" → main không ff |
| golden steel | KHỚP (NT 15/10) | **KHỚP**: pHash 0/64, SSIM 0,978, MAD 1,76, 0/144 ô lệch | ĐẠT |
| golden ll08 | KHỚP | **KHỚP**: pHash 0/64, SSIM 0,9686, MAD 1,74, 0/144 ô | ĐẠT |
| golden t1 | LỆCH CỤC BỘ, 22 ô | **LỆCH CỤC BỘ**: pHash 0/64, SSIM 0,9548, MAD 3,86, 22/144 ô (hàng 7–8, cột 1–11) | như dự kiến; **không sửa** (§0.6) |

**Chẩn đoán `versions.py check` (dừng theo luật mục 2 ở bước cập nhật main):**
| Mục | Giá trị | Nguyên nhân | Có đổi hành vi dựng T2? |
|---|---|---|---|
| CHẶN `checks.version` / `tree_sha256` | 1.10.2 `c598467f…` → 1.12.2 `81789fad…` | T2 ghim 1.10.2; lệnh merge K 1.12.2 | không (luật kiểm, không phải công cụ dựng) |
| CHẶN `toolkit.k2v.tree_sha256` | `72826bdc142a` @40bffdc9 → `00e2540b0e49` @5073067b | (a) `design/k2v/tl/**` **18 tệp mới** của V5b-2a (bộ dựng timelapse riêng, T2 không nạp); (b) `scripts/k2/build.sh` từ nhánh âm thanh: thêm `MIX=audio`, **mặc định giữ `scripts/ll/mix.py`** | không, ở cấu hình mặc định |
| CHẶN `toolkit.ll.tree_sha256` | `e6e2a6fc57e3` @5e2807be → `dc320412017c` @5073067b | `scripts/ll/qc.py` + `k2hook.py` + test (V5a: `--k2check` tuỳ chọn, mặc định tắt); `scripts/ll/mix.py` (âm thanh: `--stems` tuỳ chọn, "không đổi bản mix") | không, ở cấu hình mặc định |
| CHẶN `episode.served_models` | Haiku ngoài model ghim | đã duyệt (G2 §12.3); `versions.py` chưa có miễn trừ → khiếu nại KN-4 | — (như T2 §14.1) |
| BÁO `tools.claude_cli` | 2.1.300 → 2.1.302 | CLI tự cập nhật | — (như T2 §14.1) |
| BÁO `tools.relief_cache` | 6 vùng → None | container mới không có cache relief `/var/tmp` | không (môi trường) |

**Kết luận:** ba mục CHẶN mới (checks, toolkit k2v, toolkit ll) là băm trôi do chính các nhánh đã duyệt merge vào. Không đường dựng mặc định nào của T2 đổi. Golden steel/ll08 KHỚP là bằng chứng chạy thật cho bộ công cụ chung; riêng T2 không chạy golden. Tuy vậy, tiêu chí lệnh ghi đúng chữ là "chỉ còn BÁO served_models/CLI" và kết quả **không khớp chữ đó**. Theo mục 6 ("nếu MỌI kiểm mục 2 đạt"), P **không** cập nhật main. Các việc ghi sổ (mục 3–5) vẫn làm trên `p-1710` vì không chạm main. T2 là bản lưu, không phát hành (VV1) nên `VERSIONS.yaml` của T2 không cập nhật (luật: không tự ghi đè).

### 0.3 LOCK
`checks/LOCK` VERSION **1.12.2**, DATE_UTC 2026-10-17T00:46:57Z, TREE_SHA256 **`81789fad2e7a986a092cd2c0659a1cb93b3b5f9e87e4cfc79f7a93e316506e93`**. `lock.py --verify` KHỚP sau merge, sau ghi sổ và trước khi đẩy.

### 0.4 Đẩy
- `p-1710` đã đẩy lên origin (commit cuối ghi "DỪNG chờ chủ dự án").
- **main không cập nhật**; vẫn ở `7255aa4`.
- `p-1710` là hậu duệ thẳng của `origin/main`, nên chủ dự án duyệt là ff được ngay: `git checkout main && git merge --ff-only origin/p-1710 && git push origin main`.

### 0.5 RR2: thử GitHub Releases → **TRƯỢT** (không có quyền tạo release ở loại phiên này)
- Tệp thử: 1 048 576 byte ngẫu nhiên, SHA256 `d6b37e938ee6d43c1c20a9e7d62540e3b9a63f66ed8d6f130bcdd65743bed8c1`, ở scratchpad, không vào repo.
- `gh api -X POST repos/HungQuach301/cine-lab/releases -f tag_name=rr2-thu -F prerelease=true …` → nguyên văn: `gh: Creating, editing, or deleting releases is not permitted for this session type. (HTTP 403)`.
- `curl -X POST https://api.github.com/repos/HungQuach301/cine-lab/releases` (kèm `Content-Type: application/json`) → nguyên văn: `HTTP/1.1 403 Forbidden` · `{"message":"Creating, editing, or deleting releases is not permitted for this session type.","documentation_url":"https://docs.anthropic.com/en/docs/claude-code/github-actions"}`.
- Bộ công cụ GitHub MCP của phiên chỉ có `list_releases`/`get_release_by_tag`/`get_latest_release`, không có công cụ tạo release.
- **Không có gì được tạo:** `GET …/releases` → `[]`; `GET …/git/refs/tags/rr2-thu` → 404. Không cần xoá.
- **Hệ quả theo lệnh:** giữ LFS như hiện tại, **không viết** `scripts/common/publish_release.py`, không sửa RUNBOOK.
- Chặn nằm ở chính sách proxy cho phiên cloud, không ở quyền repo. Nếu muốn dùng Releases, chủ dự án tự tạo release (web hoặc `gh` trên máy mình), hoặc chạy bằng GitHub Actions → **việc chờ 5**.

### 0.6 Golden: ghi rõ, không sửa
- **steel, ll08: KHỚP** (bảng §0.2). Bộ công cụ sau merge dựng lại khung đã phát hành, không trôi.
- **t1: LỆCH CỤC BỘ**, 22/144 ô ở **hàng 7–8 (dải đáy), cột 1–11**: đúng bộ ô của lần chạy NT 15/10 (`reports/nen-tang/golden/golden.json`).
  - Xem tờ so khung `reports/p-1710/golden-t1-sheet.jpg` (tham chiếu | mới | diff): khác biệt là **dòng nguồn đáy** cỡ ≥ 38 px (luật V3 duyệt 14/10) xuống 2 dòng. Cảnh 3D, thẻ "about 1 in 13", nhãn ACTUAL góc và người đi bộ trùng.
  - Khung ca t1 (đoạn 00, khung 48, phố đêm) **không có** chip nơi dựng hay tấm chữ trên ảnh/footage. Q5 (`kindTag` nền tối) không tạo ô lệch nào thấy được ở đây.
  - Vậy trong ba đổi kiểu đã duyệt mà lệnh nêu (Q5, chip, hai tấm chữ), khung này chỉ lộ kiểu dòng nguồn. Ca này **ghi lại, không sửa** theo lệnh.
- Số đo: `reports/p-1710/golden.json`. Ảnh đầy đủ ở `/var/tmp/golden-p1710/` (ngoài git). Thời gian 34,1 phút (steel 7,5; ll08 20,4; t1 6,3).

### 0.7 Sổ đã ghi (commit `81e977bf`)
| Sổ | Nội dung |
|---|---|
| `COST-LEDGER.csv` | +14 dòng: T3-01, T4-01, TL-RD, TP-01, T5-01, T6-01, V5b1, V5b1b, V5b2a, GPU-RD-01, K-1.12, K-1.12.1, K-1.12.2, K2C-T2-01 (+ P-1710 ở commit báo cáo). **V5a** đã có từ nhánh v5a, không ghi trùng. Số lấy từ báo cáo từng nhánh, có `tệp:dòng`. "chưa rõ": giờ máy T3-01, T4-01, TP-01, K2C-T2-01 (báo cáo không có tổng); `cham_chu_du_an`/`thoi_luong_s` K2C-T2-01 |
| ↳ K2C-T2-01 | API **$15,16** = tổng `kiem-mu/cost.jsonl` (208 dòng), **đã gồm** $3,79 tới G1 (Đóng gói + Biên kịch v1–v3) và $0,24 G1b. P không thấy "phần trước" nào nằm ngoài sổ này nên **cộng thêm 0**, chờ chủ dự án xác nhận (**việc chờ 3**). ElevenLabs: gửi 10 141 ký tự (9 728 lời + 413 Short); bộ đếm tài khoản 105 498 → 114 553 (+9 055); hai số lệch nhau ghi nguyên |
| `RIGHTS.md` | khối mới: **P1710-01** LoC 2025710366 "Gibraltar. Neutral ground" (No known restrictions; TIF `e12f08e7…54f0`; tệp quyền có sẵn ở T3/V5b1) và **P1710-02** Rijksmuseum RP-F-00-568 (1886). Ảnh số gắn **Public Domain Mark 1.0**, siêu dữ liệu **CC0**; đọc lại bản ghi Linked Art 17/10 và lưu tại `research/timelapse/licenses/rijksmuseum-RP-F-00-568.txt`. Báo cáo TL-RD ghi "CC0" cho ảnh; bản ghi nói ảnh là PDM, cũng tự do cho mọi mục đích. Trước đây chưa có dòng nào |
| `AUTHORSHIP.md` | NN2 (Q32b-K2), **QQ5** (nguyên văn không có trong repo, xem dưới), SS1–SS5, TT1–TT6, VV1 (T2 KHÔNG phát hành; `release-k2c-t2-01-v1` @784a58f1 giữ làm bản lưu, master `f63b0b4b…`). Dòng VV1 nhắc VV2–VV4 và RR1–RR3 |
| `channel-k2/HANG-DOI.md` | mục "CẬP NHẬT 17/10" đặt trên bảng 12/10: T2 không phát hành (VV1); **T3 Gibraltar chờ phiên NC-LS** (khung lại quanh các cuộc vây hãm); T4 Las Vegas → T5 Zürich → T6 Detroit giữ thứ tự; VV2 áp T3–T6 khi K hiện thực |
| `channel-k2/BAI-HOC-K2.md` (đã có, ghi thêm) | **K13** bản đồ 88,7 % phim · **K14** nơi thành phố chỉ có địa hình · **K15** địa cầu/độ cao lớn thừa · **K16** vòng sửa chấm mù tạo lỗi mới (L4) → **TT3: luôn so khung trước khi chấm** · **K17** 5 vòng chấm mù không vượt giới hạn thiết kế |
| `.gitignore` | `**/sec/*.mkv`, `k2v-cache/`, `/out/` (chỉ gốc; **không** chặn `*/out/` vì `design/cong3–5` đang theo dõi hàng nghìn tệp trong `out/`) |
| `.gitattributes` (mới ở gốc) | LFS cho `*-master.mp4`, `*-short-*.mp4`, `*-v[0-9]-p[0-9].mp4` (khớp `tools/lfs-allow.txt`) và `channel-k2/*/v5b1-thu/**/*-1080p.mp4`. Các nhánh `release-*` giữ `.gitattributes` riêng (`*.mp4` LFS), không động tới |
| `tools/lfs-allow.txt` | thêm `channel-k2/*/v5b1-thu/**/*-1080p.mp4` + dạng fnmatch `channel-k2/*/v5b1-thu/*-1080p.mp4` (`preflight_scan.py` dùng fnmatch nên mẫu `**/` không khớp tệp nằm thẳng trong `v5b1-thu/`) |
| `reports/K-HANG-DOI-KHIEU-NAI.md` (mới) | KN-1 Q7/Q8 `estimate`; KN-2 Q36(b) một lần trong 0:00–0:15; KN-3 Q33 bỏ lớp chữ cố định; KN-4 `versions.py` miễn trừ `served_models` (tệp thuộc vùng NT); KN-5 Q37/`rhythm.py` đo trên điểm ảnh; KN-6 luật mới **VV2** kèm cách đo (khai lớp + gazetteer + năm tài sản; log máy quay, ≤ 1 đoạn, ≤ 3,0 s) |

- **QQ5:** P tìm trong mọi báo cáo, commit và nhánh nhưng không thấy mã "QQ5". Dòng AUTHORSHIP ghi "chủ dự án duyệt, nguyên văn chờ chủ dự án"; khả năng liên quan đổi kiểu Q5 (SS4) ghi rõ là CHƯA XÁC MINH → **việc chờ 2**.
- **Tên tệp 1080p:** bản 1080p của V5b1 tên `gib20_1080p.mp4` (gạch dưới), **không khớp** mẫu `*-1080p.mp4` đã duyệt. Khi đẩy tệp này phải đổi tên thành `gib20-1080p.mp4`, hoặc chủ dự án duyệt thêm mẫu `*_1080p.mp4` → **việc chờ 4**.

### 0.8 Chi phí
| Mục | Trần | Thực tế |
|---|---|---|
| Claude API (gọi từ script) | $0 | **$0** |
| ElevenLabs | 0 | **0** ký tự |
| YouTube Data API | 0 | **0** |
| Mạng khác | — | 1 lần đọc `id.rijksmuseum.nl` (26,7 KB); 2 lần POST release bị 403 |
| Giờ máy | ≤ 1,5 h | **≈ 1,2 h thời gian thực** (11:25 → 12:35 UTC). Cộng các tiến trình: **≈ 2,5 giờ-tiến trình**, gồm L1 trước 50,3 + L1 sau 49,9 phút (chạy song song), golden 34,1, selftest_ll trước 8,5, các selftest sau 3,3, verify/npm ≈ 4, preflight 0,25. Không có số nào trong ±5 % quanh trần |
| Token | trần mềm | không đo được trong phiên (bộ đếm harness) |

**Chỉ số trong ±5 % quanh ngưỡng:** không có chỉ số nào của phiên này nằm trong dải. Gần nhất là golden t1 SSIM 0,9548, cách ngưỡng tạm 0,90 là 6,1 %. Nhắc lại từ báo cáo T2 đã merge: RÀ GU 6,90 (+3,8 %) và phần sửa 6,87 (+3,3 %) so với 6,65.

## 1. Việc chờ chủ dự án
1. **Cập nhật main:** duyệt ff `main` ← `p-1710`. Mọi kiểm đã ĐẠT, trừ `versions.py` lệch chữ kỳ vọng do băm trôi từ các nhánh đã duyệt (§0.2). Lệnh ff ở §0.4. Kèm theo: đưa 3 dòng Kinh thánh duyệt 15/10 (commit `72184052` trên `k2c-t2`) và đề xuất TT6 (a)–(e) vào bản nguyên văn ở **bước 0 T3**.
2. **QQ5:** cho nguyên văn quyết định để P sửa dòng AUTHORSHIP.
3. **COST-LEDGER K2C-T2-01:** xác nhận $15,16 là tổng API cả tập. Nếu "phần trước" là khoản khác (ví dụ token phiên hay tác tử con), cho số và nguồn.
4. **Tệp 1080p V5b1:** đổi tên `gib20_1080p.mp4` → `gib20-1080p.mp4` khi đẩy LFS, hay duyệt thêm mẫu `*_1080p.mp4`.
5. **RR2 trượt:** chọn giữ LFS (hiện tại) hay tạo release ngoài phiên cloud (chủ dự án tự làm hoặc qua GitHub Actions). Nếu chọn Releases, cần một lệnh mới cho `publish_release.py`.
6. **Phiên K kế:** mở theo `reports/K-HANG-DOI-KHIEU-NAI.md` (KN-1…KN-6; KN-4 có thể chuyển phiên NT).
7. **Phiên NC-LS** cho T3 Gibraltar (khung lại quanh các cuộc vây hãm) trước G1 T3.
8. **VERSIONS T2:** giữ nguyên (bản lưu, không phát hành), hay ghi lại một bản chụp "sau hợp nhất" để đối chiếu.
