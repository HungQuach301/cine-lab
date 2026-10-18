# PHIÊN P-1810: hợp nhất 18/10/2026 (5 nhánh) + ghi sổ quyết định 17–18/10. BÁO CÁO. DỪNG chờ chủ dự án

Nhánh thật: **`p-1810`** (tạo từ `origin/main` @`82a17aef`). Harness của phiên giao nhánh `ccr-8ceff334-im7fjv` (không phải `claude/...`); P làm và đẩy đúng `p-1810` theo lệnh, không đẩy nhánh harness.

```text
ĐIỀU LỆ PHIÊN P-1810                                        | thực tế
Loại phiên:        P (điều phối)                             | đúng
Nhánh:             p-1810 từ origin/main @82a17ae            | đúng; đẩy p-1810; main KHÔNG cập nhật
Merge --no-ff:     checks/v1.13 → checks-v1-14 → nc-ban-do   | 5/5 merge đúng thứ tự, 0 xung đột
                   → sh-ghost-gibraltar-t3 → tuyen-t3        |
KHÔNG merge:       v5b2b, v5b2c, pt-*, pt2-*, pt3-*, pt4-*,  | không merge; v5b2b/pt2-lai/pt3-van-nuong chỉ ĐỌC báo cáo
                   k2c-t3-g1                                 | qua `git show` để chép dòng sổ
Tệp KHÔNG sửa:     docs/BIBLE-KENH2.md · checks/ ngoài merge | không sửa; checks/ chỉ đổi qua 2 merge K, chạy lock/selftest
                   · scripts/ trừ scripts/env/verify.sh      | chỉ sửa scripts/env/verify.sh
Trần chi phí:      Claude API $0 · YouTube 0 · ElevenLabs 0  | $0 · 0 · 0
                   · giờ máy ≤ 1,5 h                         | ≈ 0,35 h thời gian thực; ≈ 0,5 giờ-tiến trình (§5)
Preflight:         BẮT BUỘC; che email                       | ĐẠT (staged 6 tệp; dải origin/main..HEAD 131 tệp); 0 email mới
```

## 0. Tóm tắt
| Mục | Kết quả |
|---|---|
| Merge | 5/5 `--no-ff`, **0 xung đột** (`git merge-tree` thử tuần tự trước, §1) |
| LOCK | `python3 -I checks/lock.py --verify` **KHỚP 1.14.0 `feb4141d2b8fa589fbfcdbd7a1e2111c582fb635cb30532f1d3c959f9ae4a9ec`** (sau merge, sau ghi sổ, trong preflight) |
| Selftest | k114 **126/126**, k113 **64/64**, k1122 **37/37**, k1121 **48/48**, k112 **75/75**, k2 **129/129**, ll **317/317** — khớp số K-1.14 báo (§0 và bảng selftest) |
| verify.sh | **14 PASS / 0 FAIL** (sau sửa thêm OpenEXR + bpy /opt/bpy, và cài môi trường §3) |
| Golden | steel **KHỚP** · ll08 **KHỚP** · t1 **LỆCH CỤC BỘ 22/144** (đúng bộ ô P-1710, không đổi) |
| Sổ | COST-LEDGER 8 dòng · RIGHTS 15 dòng · AUTHORSHIP 7 dòng · HANG-DOI (K4, F8) · QUAN-TRI-RUI-RO §1.3 · verify.sh (§4) |
| Đẩy | `p-1810` lên origin; **main không cập nhật** (vẫn `82a17aef`) |

## 1. Merge và xung đột
**Trước khi merge:** `git fetch` 5 nhánh (và làm mới `origin/main`: tham chiếu cục bộ cũ là `067c9599`, sau fetch đúng `82a17aef`). SHA đầu nhánh khớp lệnh: `9bf28dc5`, `b92d4da5`, `83dca2d5`, `54185b35`, `434a90fc`. `checks/v1.13` nằm trọn trong `claude/checks-v1-14-1kq3u1` (`merge-base --is-ancestor` đúng).

**`git merge-tree --write-tree` tuần tự** (mỗi bước ghép lên cây của bước trước): cả 5 bước **rc = 0, không xung đột**.

| # | Nhánh @ SHA | Commit merge | Tệp (so cha 1) | Xung đột |
|---|---|---|---|---|
| 1 | `origin/checks/v1.13` @9bf28dc | `573ced14` | 6 A, 9 M (`checks/`, `reports/K-1.13-BAO-CAO.md`) | không |
| 2 | `origin/claude/checks-v1-14-1kq3u1` @b92d4da | `8a82105b` | 35 A, 7 M (`checks/`, `reports/K-1.14-BAO-CAO.md`) | không |
| 3 | `origin/nc-ban-do` @83dca2d | `ddffb695` | 27 A (`reports/NC-BAN-DO-BAO-CAO.md`, `reports/nc-ban-do/**`) | không |
| 4 | `origin/claude/sh-ghost-gibraltar-t3-1gkftx` @54185b3 | `a1626818` | 23 A (`channel-k2/k2c-t3-01/ghost/**`) | không |
| 5 | `origin/tuyen-t3` @434a90f | `9057e9cf` | 24 A (`channel-k2/k2c-t3-01/tuyen/**`) | không |
| — | commit ghi sổ | `492996e0` | 6 M (§4) | — |
| — | commit báo cáo | commit chứa tệp này | `reports/P-1810-BAO-CAO.md`, `reports/p-1810/golden.json` | — |

- Hai nhánh K chỉ sửa trong `checks/` + thêm báo cáo K; ba nhánh xưởng/nghiên cứu chỉ **thêm** tệp trong vùng của mình.
- Không merge: `v5b2b`, `v5b2c`, `pt-*`, `pt2-*` (`pt2-lai`), `pt3-*` (`pt3-van-nuong`), `pt4-*`, `k2c-t3-g1`.

## 2. LOCK, selftest, golden
| Kiểm | Kết quả | Thời gian |
|---|---|---|
| `python3 -I checks/lock.py --verify` | **KHỚP** VERSION 1.14.0, DATE_UTC 2026-10-17T16:00:47Z, TREE_SHA256 `feb4141d…9ae4a9ec` | < 1 s |
| `checks/ll/selftest_k114.py` | **126/126** đúng kỳ vọng | 6 s |
| `selftest_k113.py` | **64/64** · 11 nhóm | 7 s |
| `selftest_k1122.py` | **37/37** · 4 biến thể | < 1 s |
| `selftest_k1121.py` | **48/48** · 9 luật | 5 s |
| `selftest_k112.py` | **75/75** · 13 luật | 6 s |
| `selftest_k2.py` | **129/129** (kênh 2, 1.11.1) | 24 s |
| `selftest_ll.py` | **317/317** (LL v3) | 420 s (chạy song song với golden) |
| golden steel | **KHỚP**: pHash 0/64, SSIM 0,978, MAD 1,76, > 24: 0,04 %, 0/144 ô | 184,7 s |
| golden ll08 | **KHỚP**: pHash 0/64, SSIM 0,9686, MAD 1,74, > 24: 0,0 %, 0/144 ô | 417,2 s |
| golden t1 | **LỆCH CỤC BỘ**: pHash 0/64, SSIM 0,9548, MAD 3,86, > 24: 1,24 %, **22/144 ô** | 118,4 s |

- **t1:** danh sách ô lệch (`o_lech_ds`) và mọi số đo **trùng hệt** `reports/p-1710/golden.json` (P-1710, 17/10; chỉ khác thời gian dựng 3D). Đây là dòng nguồn đáy ≥ 38 px theo luật V3 (14/10), đã giải thích ở P-1710 §0.6. Không sửa.
- Số đo: `reports/p-1810/golden.json`. Ảnh đầy đủ ở `/var/tmp/golden-p1810/` (ngoài git).
- **Sự cố đã xử lý:** lượt golden đầu báo `steel LỖI 'oid'` vì bản clone chưa có tham chiếu `origin/release-*` (con trỏ LFS của khung tham chiếu). P fetch `release-k2g-ep01-v1`, `release-k2c-t1-06-v1`, `release-ll-ep08-v1`, dừng lượt cũ bằng PID (BAI-HOC #24/#41), chạy lại sạch. Số trên là của lượt sạch.

## 3. Môi trường (`scripts/env/verify.sh`)
- Đầu phiên (bản verify.sh của tham chiếu main cũ): 10 PASS / 1 FAIL (three.js). P chạy `npm ci` trong `design/cong3/shared`.
- Sau merge + sửa verify.sh: 11 PASS / 3 FAIL (OpenEXR, tifffile/pyshp, k2v node_modules) → cài `OpenEXR` 3.5.2, `tifffile`, `pyshp` vào `/opt/cine` (pip), `npm ci` trong `design/k2v` → **14 PASS / 0 FAIL**. `node_modules/` không vào git; `git status` sạch ngoài tệp sổ.

## 4. Sổ đã ghi (commit `492996e0`)
| Sổ | Nội dung |
|---|---|
| `COST-LEDGER.csv` | 8 dòng, chép đề xuất nguyên văn của từng báo cáo: **K-1.13** (K, 1,4 h), **K-1.14** (K, 1,2 h), **NC-BD-01** (0,15 h), **SH-01** (1,0 h), **TUYEN-T3-01** (0,05 h), **V5b2b** ($1,61, 4,1 h; **chỉ ghi sổ, mã chưa merge**), **PT-01** (Claude $2,641; OpenAI **$0,48 + $0,38**; 1,9 h), **PT2-01** (Claude $1,42; OpenAI **$0,19**; 3,6 giờ-tiến trình). Kiểm bằng `csv`: cả 8 dòng đúng 20 cột |
| `RIGHTS.md` | Khối mới "bản đồ lịch sử, toạ độ tuyến, người đám đông, vân phim trường": **P1810-NE** Natural Earth 1:10m/1:50m (PD) · **P1810-CLIO** Cliopatria v0.2.1 (CC BY 4.0, Seshat) · **P1810-OHM** OpenHistoricalMap (CC0 + phần CC BY 4.0 CNIG/IGN) · **P1810-AHCB** Newberry AHCB · **P1810-OSMN** OSM Nominatim 38 toạ độ (ODbL, "© OpenStreetMap contributors") · **W4-MPFB-A5** (CC0, mở rộng sang đám đông khung neo) · **P1810-PH01…PH09** 9 vân Poly Haven CC0 · **P1810-AI** ảnh AI PT/PT2 = **CHỈ NGHIÊN CỨU, không vào gói phát hành**. Giấy phép trích nguyên câu từ `reports/nc-ban-do/giay-phep/GIAY-PHEP-NGUYEN-VAN.md` và `reports/pt/giay-phep/` (nhánh `pt2-lai`) |
| `AUTHORSHIP.md` | 7 dòng kèm giờ: **B1–B8** (22:15) · **E1–E9** (23:02) · **F1–F8** (23:29), **G1–G5 + H1–H4** (23:50) · **I1–I8 + K1–K6** (18/10 00:05) · **J1, J3–J6 + HC1–HC6** (06:26) · **M1–M6 HỦY** (06:48, kèm nguyên văn đính chính "No AI imagery") · **N1–N4** (06:51), **O-AI** nhóm 1 = O2/O3/O4/O5/O7/O8/O9/O10, O1 có điều kiện, O6 đo trước (07:04), **HC7–HC9** (07:10), **P2-1…P2-6** (08:43) |
| `channel-k2/HANG-DOI.md` | Mục "CẬP NHẬT 18/10" trên lịch 17/10: **K4 — T8 = Antwerp 1585 → Amsterdam (XANH), đề xuất của P, CHỜ CHỦ DỰ ÁN DUYỆT**, kèm 5 lý do, nhược, phương án thay (Vicksburg 1863); **ghi chú Berlin chấm lại ở G0 vì đối thủ đã thử nghiệm (F8)** |
| `channel-k2/QUAN-TRI-RUI-RO.md` | **§1.3 "AI trên hình"** theo Kinh thánh §11.3: rào chắn (nền mã trước, mặt nạ, lớp dữ kiện được bảo vệ, kiểm dữ kiện, nhãn + công bố GenAI), **trần 20 %**, **đo bình luận chê AI ≤ 2 %** (7 và 28 ngày) |
| `scripts/env/verify.sh` | Thêm kiểm **`OpenEXR`** trong Python chính; kiểm **bpy** dùng `${CINE_BPY:-/opt/bpy/bin/python}` và in đường dẫn |

**Điểm P tự đọc, cần chủ dự án biết:**
1. **Văn bản Kinh thánh §11 (bản Project 18/10) không có trong repo** (`docs/BIBLE-KENH2.md` chỉ có §1–9, và P không được sửa tệp này). Với F/G/H/I/K/J/HC6/HC9/N/O/P2, AUTHORSHIP ghi mã, giờ, phần thấy được trong báo cáo đã merge hoặc đã đọc, rồi trỏ "chi tiết: Kinh thánh §11". **P không tự viết nội dung nào không có nguồn.**
2. **I1–I8 và K1–K6:** P ánh xạ theo số mục "Việc chờ chủ dự án" của K-1.13 §12 (8 mục) và K-1.14 §13 (6 mục; mục 4 đúng là "K4: chốt T8"). Nếu cách đánh số của chủ dự án khác thì cần sửa dòng AUTHORSHIP này.
3. **PT-01:** đề xuất ở PT §12 (Claude 1,47; OpenAI $0,48; ≈ 1,8 h) viết **trước** phần C ngày 18/10. P ghi số cả phiên theo PT §15: Claude $1,467 + $1,174 = **$2,641**; OpenAI **$0,48 + $0,38** (theo lệnh); ≈ **1,9 h**. Ghi chú trong dòng sổ nêu rõ.
4. **Dấu thập phân:** đề xuất SH-01 ("≈ 1,0"), V5b2b ("≈ 4,1"), PT-01 ("≈ 1,8") dùng dấu phẩy, làm lệch cột CSV. P ghi `1.0`, `4.1`, `1.9`; dấu "≈" và nguyên văn ghi trong cột `ghi_chu`. Chữ "OpenAI $…" của PT/PT2 chuyển từ cột `ty_le_relief_pct` sang `ghi_chu`. NC-BD-01 và TUYEN-T3-01 đề xuất không theo khuôn 20 cột: P đổi sang khuôn, nguyên văn để trong `ghi_chu`.
5. **Ảnh AI và vân Poly Haven:** tài sản nằm trên nhánh chưa merge (`pt2-lai`, `pt3-van-nuong`). RIGHTS ghi theo lệnh, đường dẫn kèm tên nhánh. SHA vân Poly Haven chép đúng 16 ký tự đầu như bảng nguồn; SHA đủ ở `reports/pt/giay-phep/README.md`.
6. **Trần 20 % (§1.3):** lệnh không nêu đơn vị (thời lượng hay số khung). P ghi "theo §11.3" và đặt dòng nhắc đối chiếu khi §11 vào Kinh thánh.

## 5. Chi phí
| Mục | Trần | Thực tế |
|---|---|---|
| Claude API (gọi từ script) | $0 | **$0** |
| ElevenLabs | 0 | **0** ký tự |
| YouTube Data API | 0 | **0** đơn vị |
| OpenAI | — | **$0** (không gọi) |
| Giờ máy | ≤ 1,5 h | **≈ 0,35 h thời gian thực** (01:55 → 02:16 UTC). Cộng các tiến trình **≈ 0,5 giờ-tiến trình**: golden lượt sạch 12,0 phút + lượt hỏng ≈ 5 phút, selftest_ll 7,0 phút, 6 selftest khác 0,8 phút, verify.sh ×4, npm/pip, preflight |
| Token | trần mềm | không đo được trong phiên |

**Chỉ số trong ±5 % quanh ngưỡng:** không có chỉ số nào của phiên này. Gần nhất: golden t1 SSIM 0,9548 so với ngưỡng 0,90 (+6,1 %); ll08 SSIM 0,9686 (+7,6 %). Nhắc lại từ báo cáo nhánh đã merge: NC-BD inset minh hoạ 11,9 % so với trần 12 % (−0,9 %).

**Dòng đề xuất cho `COST-LEDGER.csv`** (ghi ở lần P kế; commit báo cáo không sửa sổ sau khi đã kiểm): `P-1810,Hợp nhất 18/10 (5 nhánh) + ghi sổ 17–18/10,P,2026-10-18,,,,,0,0,không gọi API,0,0,0.35,,,,,reports/P-1810-BAO-CAO.md §5,YouTube 0; giờ máy = thời gian thực; ≈ 0.5 giờ-tiến trình (golden 3 ca + selftest)`.

## 6. Việc chờ chủ dự án
1. **Duyệt `p-1810` → `main`.** `p-1810` là hậu duệ thẳng của `origin/main` `82a17aef`, nên ff được ngay: `git checkout main && git merge --ff-only origin/p-1810 && git push origin main`.
2. **K4 / T8:** duyệt đề xuất **Antwerp 1585 → Amsterdam (XANH)** hoặc chọn đề tài khác (`HANG-DOI.md` "CẬP NHẬT 18/10"). Sau khi duyệt, K-R7 Dresden mới có tập kề sau.
3. **Văn bản Kinh thánh §11 (bản Project 18/10):** chỉ định phiên được ghi `docs/BIBLE-KENH2.md` (lệnh này cấm P sửa; phiên G1 T3 đang ghi). Khi §11 vào repo, P đối chiếu lại 7 dòng AUTHORSHIP và QUAN-TRI-RUI-RO §1.3, nhất là đơn vị của trần 20 %.
4. **Xác nhận cách ánh xạ I1–I8 / K1–K6** (§4 điểm 2) và số PT-01 dùng số cả phiên §15 (§4 điểm 3).
5. **Nhánh chưa merge (đang chạy hoặc chưa duyệt):** `v5b2b` (đã ghi sổ chi phí, mã chưa merge), `v5b2c`, `pt-*`/`pt2-lai`/`pt3-van-nuong`/`pt4-*`, `k2c-t3-g1`. Khi merge `pt2-lai`, đường dẫn trong RIGHTS `P1810-PH*`/`P1810-AI` trở thành tệp trên main.
6. **Ảnh AI PT/PT2:** giữ "CHỈ NGHIÊN CỨU" cho tới khi chủ dự án duyệt riêng việc đưa vào gói phát hành (theo O-AI và §11.3).
7. Ghi dòng COST-LEDGER `P-1810` (§5) ở lần P kế.
