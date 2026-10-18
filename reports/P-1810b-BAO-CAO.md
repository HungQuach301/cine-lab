# PHIÊN P-1810b: hợp nhất 18/10/2026 (2 nhánh) + ghi sổ 18/10. BÁO CÁO. DỪNG chờ chủ dự án

Nhánh thật: **`p-1810b`** (tạo từ `origin/main` @`209a1a27`). Harness giao nhánh `ccr-f8827be9-fkwpak`. P làm và đẩy `p-1810b` theo lệnh, không đẩy nhánh harness.

```text
ĐIỀU LỆ PHIÊN P-1810b                                       | thực tế
Loại phiên:        P (điều phối)                             | đúng
Nhánh:             p-1810b từ origin/main @209a1a2           | đúng; đẩy p-1810b; main KHÔNG cập nhật
Merge --no-ff:     checks-v1-15 → k2c-t3-loi-khoa            | 2/2 merge đúng thứ tự, 0 xung đột, mỗi merge một commit
KHÔNG merge:       ccr-8f16467a-mhu954, ccr-11686158-4ucx09, | không merge; ccr-8f16467a-mhu954 / pt3-van-nuong /
                   v5b2b, pt-*, pt2-*, pt3-*, pt4-*, v6       | pt4-song / pt2-lai chỉ ĐỌC qua `git show`
Tệp KHÔNG sửa:     scripts/, design/, checks/, docs/          | không sửa; chỉ đổi qua merge
                   (ngoài merge)                             |
Trần chi phí:      Claude API $0 · ElevenLabs 0 · YouTube 0  | $0 · 0 · 0 · 0
                   · OpenAI 0 · giờ máy ≤ 1 h                | ≈ 0,45 h thời gian thực (§5)
Preflight:         BẮT BUỘC; che email                       | ĐẠT (staged 4 tệp, rồi 2 tệp; dải origin/main..HEAD); 0 email mới
```

## 0. Tóm tắt
| Mục | Kết quả |
|---|---|
| Merge | 2/2 `--no-ff`, **0 xung đột** (§1) |
| LOCK | `python3 -I checks/lock.py --verify` **KHỚP 1.15.0 `f4fa0349ca53b05d64e4303554ec168e6445c82d97e662672f70ccf42df80d40`** (DATE_UTC 2026-10-18T02:20:57Z). Kiểm sau merge, sau ghi sổ, trước khi đẩy. Không gọi `lock.py` khi thiếu `--verify` |
| Kinh thánh | `docs/BIBLE-KENH2.md` SHA-256 **`2a8c263aa71d2297b5bf024c0eb3b16fd7ec4c361526cf9e59dcc8c5e8816822`**: đúng tiền tố `2a8c263a` |
| Lời khoá T3 | `channel-k2/k2c-t3-01/loi-khoa.txt` SHA-256 **`0fdc72ce81e33b6f4efc8234a52dafc5410d4448c26c0a0feb3eb01abaa71753`**: đúng tiền tố `0fdc72ce` |
| Selftest | k115 **105/105** · k114 **126/126** · k113 **64/64** · k1122 **37/37** · k1121 **48/48** · k112 **75/75** · k2 **129/129** · ll **317/317** |
| verify.sh | **14 PASS / 0 FAIL**. Đầu phiên là 9/5: thiếu môi trường trong container mới, đã cài lại (§3) |
| Golden | steel **KHỚP** · ll08 **KHỚP** · t1 **LỆCH CỤC BỘ 22/144**. Mọi số đo trùng P-1810, chỉ khác thời gian dựng |
| Sổ | COST-LEDGER 9 dòng · RIGHTS 12 dòng · AUTHORSHIP 7 dòng · HANG-DOI T3 (§4) |
| Nhánh tên mới | `v5b2c` → 233f5fa6 · `v5b2d` → 1eecfec2 · `k2c-t3-loi` → 61946e17. Không xoá nhánh cũ (§6) |

## 1. Merge (số trước / sau)
`git fetch origin` (đủ mọi nhánh, gồm các nhánh `release-*` cho golden). SHA đầu nhánh khớp lệnh: `origin/main` = `209a1a27`, `origin/claude/checks-v1-15-1qzf9z` = `001ee5da`, `origin/claude/k2c-t3-loi-khoa-al1itg` = `61946e17`. P không chạy lại `merge-tree`, vì Claude điều phối đã thử. Cả hai merge thật đều sạch, không xung đột.

| # | Nhánh @ SHA | Commit merge | Thay đổi (so cha 1) | Xung đột |
|---|---|---|---|---|
| — | `origin/main` (trước) | `209a1a27` | LOCK 1.14.0 `feb4141d…` | — |
| 1 | `origin/claude/checks-v1-15-1qzf9z` @001ee5d | `df1d7fc7` | 62 tệp, +9 401 / −35 (`checks/`, `reports/K-1.15-BAO-CAO.md`) | không |
| 2 | `origin/claude/k2c-t3-loi-khoa-al1itg` @61946e17 | `33ad4461` | 138 tệp, +14 062 / −194 (`channel-k2/k2c-t3-01/**`, `docs/BIBLE-KENH2.md`) | không |
| — | commit ghi sổ | `cb7e6868` | 4 tệp, +40 (§4) | — |
| — | commit báo cáo | commit chứa tệp này | `reports/P-1810b-BAO-CAO.md`, `reports/p-1810b/golden.json` | — |

Sau merge, LOCK đổi từ 1.14.0 `feb4141d…` thành **1.15.0 `f4fa0349…`**, đúng như lệnh. `docs/BIBLE-KENH2.md` là bản Project 18/10, gồm §10 và §11 (11.1–11.6).

## 2. Kiểm sau merge
| Kiểm | Kết quả | Thời gian |
|---|---|---|
| `python3 -I checks/lock.py --verify` | **KHỚP**: VERSION 1.15.0, TREE `f4fa0349…df80d40` | < 1 s |
| `sha256sum docs/BIBLE-KENH2.md` | `2a8c263a…8816822` **đúng** | — |
| `sha256sum channel-k2/k2c-t3-01/loi-khoa.txt` | `0fdc72ce…abaa71753` **đúng** | — |
| `selftest_k115.py` | **105/105**, 15 nhóm, đúng số K-1.15 báo | 7 s |
| `selftest_k114.py` | **126/126** | 4 s |
| `selftest_k113.py` | **64/64**, 11 nhóm | 3 s |
| `selftest_k1122.py` | **37/37**, 4 biến thể | 1 s |
| `selftest_k1121.py` | **48/48**, 9 luật | 4 s |
| `selftest_k112.py` | **75/75**, 13 luật | 4 s |
| `selftest_k2.py` | **129/129** (kênh 2, 1.11.1) | 25 s |
| `selftest_ll.py` | **317/317** (LL v3) | 330 s (chạy song song với golden) |
| golden steel | **KHỚP**: pHash 0/64, SSIM 0,978, MAD 1,76, > 24: 0,04 %, 0/144 ô | 186,8 s |
| golden ll08 | **KHỚP**: pHash 0/64, SSIM 0,9686, MAD 1,74, > 24: 0,0 %, 0/144 ô | 420,4 s |
| golden t1 | **LỆCH CỤC BỘ**: pHash 0/64, SSIM 0,9548, MAD 3,86, > 24: 1,24 %, **22/144 ô** | 147,6 s |

- **Selftest:** lượt đầu P gọi bằng `python3` hệ thống, nên thiếu `cv2`/`scipy` và 5/7 lỗi import. Không lỗi nào là lỗi luật. Chạy lại bằng `/opt/cine/bin/python -I` (Python chính theo CLAUDE.md) thì đạt hết. Số trong bảng là của lượt này.
- **Golden t1:** so từng trường với `reports/p-1810/golden.json`, chỉ khác `giay_dung_3d` và `giay_tong`. Danh sách ô lệch và mọi số đo trùng hệt, nên đây là lệch đã biết (dòng nguồn đáy ≥ 38 px theo luật V3, P-1710 §0.6). `golden.py` trả mã 1 vì t1 LỆCH CỤC BỘ. Số đo lưu ở `reports/p-1810b/golden.json`, ảnh ở `/var/tmp/golden-p1810b/` (ngoài git).

## 3. Môi trường (`scripts/env/verify.sh`)
- Đầu phiên được **9 PASS / 5 FAIL**: thiếu OpenEXR, three.js, tifffile/pyshp, k2v node_modules; Freesound 403 (tuỳ chọn). Container mới không giữ phần P-1810 đã cài.
- P cài `OpenEXR`, `tifffile`, `pyshp` (pip, `/opt/cine`) và chạy `npm ci` trong `design/cong3/shared` và `design/k2v`. Các bước này không sửa tệp nào trong git; `node_modules/` không vào git.
- Sau cài: **13/1** (chỉ Freesound 403). Lần chạy cuối, Freesound cũng PASS, nên **14 PASS / 0 FAIL**.

## 4. Sổ đã ghi (commit `cb7e6868`)
| Sổ | Nội dung |
|---|---|
| `COST-LEDGER.csv` | 9 dòng, cả 9 đúng 20 cột (kiểm bằng `csv`): **K-1.15** ($0,39 / 0,6 h, nguyên văn §9) · **T3-G1** ($1,807 / 0,6 h) · **T3-LOI-KHOA-v4** ($2,773 / 0,5 h) · **T3-LOI-KHOA-v4.1** ($0 / 0,2 h) · **V5b2c** ($0,537 / ≈ 3,0 h, chỉ ghi sổ) · **V5b2d** ($1,918 / ≈ 2,4 h, chỉ ghi sổ) · **PT3-01** (Claude $1,17; OpenAI **$8,906** `gpt-image-2.5-sunburst` ×133; 3,4 h) · **PT4-01** (Claude $2,458; OpenAI **$0,0629** ×1; 4,0 h) · **P-1810** (dòng tự đề xuất của P-1810 §5, "ghi ở lần P kế") |
| `RIGHTS.md` | Khối mới gồm 12 dòng: **P1810B-ETOPO** (CC0-1.0, trích nguyên câu NOAA) · **P1810B-NE-FR** `fr-metro.geojson` dẫn xuất Natural Earth (PD) · **P1810B-LOC** ảnh LoC 2025710362, chỉ tham chiếu dựng DEM, "No known restrictions on publication." (P đọc lại JSON loc.gov 18/10, HTTP 200) · **P1810B-DRINK** Drinkwater 1785, bản 1905, OCR archive.org (PD) · **P1810B-HOWE** Howe/CMH (PD) · **P1810B-HANSARD** UK Hansard (Open Parliament Licence) · **P1810B-HMGOG**, **P1810B-HC-SM**, **P1810B-HC-LN**, **P1810B-AP-MT** (chỉ nguồn kiểm chứng, không trích lên hình) · **W4-MPFB-A5b** (MPFB2 commit `3edf9df0`, CC0, mở rộng A5 sang PT4) · **P1810B-AI** 60 vân AI PT3 + tấm C PT2/PT4 (Services Agreement §4.1 nguyên văn, có C2PA, "chỉ nghiên cứu cho tới khi V6 dùng trên hình") |
| `AUTHORSHIP.md` | 7 dòng kèm giờ: **C2-1…C2-9** (09:29) · **K15-1…K15-8 + G1 T3** (09:35) · **Q1–Q2** (09:23) · **LK1–LK4** (10:44) · **Q-PT3-1…5** (11:08) + phương án A (11:11) · **V2D-1…V2D-6 + VL1 = (a)** (12:05) · **Q-PT4-1…4** ("duyệt theo khuyến nghị điều phối 13:05", vì lệnh không kèm Bảng trạng thái) |
| `channel-k2/HANG-DOI.md` | Mục "CẬP NHẬT 18/10/2026 chiều (P-1810b: T3)": T3 Gibraltar có **lời khoá v4.1 (SHA `0fdc72ce…`)**, **chờ cổng hình (V6) → G1b** |

**Điểm P tự quyết hoặc chưa kiểm được, cần chủ dự án biết:**
1. **Q1–Q2 (09:23) và VL1:** hai mã này không có trong repo hay trong các báo cáo P đã đọc. AUTHORSHIP chỉ ghi mã, giờ và nguyên văn "VL1 = (a)". **P không tự viết nội dung.** Có thể VL1 = (a) là quyết định cho tấm im lặng KA2026 (`KHOA-LOI-41-BAO-CAO.md` §6 mục 1, phương án (a): 5j dài thêm 1,5 s, tổng ≈ 721,2 s). P chưa kiểm được nên ghi vào HANG-DOI là "cần xác nhận".
2. **Ánh xạ của P** (ghi rõ trong AUTHORSHIP là "chủ dự án xác nhận"):
   - K15-1…K15-8 ứng với bảng K1–K8 của `reports/K-1.15-BAO-CAO.md`.
   - V2D-1…V2D-6 ứng với đề xuất 1–6 của `reports/v5b2d/V5B2D-BAO-CAO.md` §8.
   - C2-1…C2-9: chỉ ghi các mục thấy được trong V5b-2d (C2-2/4/5/7/9).
3. **Q-PT4-4:** PT4 §9 chỉ có Q-PT4-1…3. Dòng AUTHORSHIP ghi đúng câu dự phòng của lệnh và nêu điều này.
4. **Open Parliament Licence:** P chưa đọc được nguyên văn, vì parliament.uk trả **403** cho cả curl và WebFetch. RIGHTS ghi "OPL v3.0 (theo lệnh)" kèm việc phải làm: đọc nguyên văn và câu ghi công **trước G2**. Howe/CMH ghi PD theo lệnh, lý do là tác phẩm của chính phủ Mỹ.
5. **Số chi phí theo lệnh, khác chữ số so với dòng đề xuất:**
   - PT3: lệnh ghi OpenAI $8,906, đề xuất ghi $8,91.
   - PT4: lệnh ghi Claude $2,458 và OpenAI $0,0629, đề xuất ghi $2,46 và $0,063.
   - Sổ dùng số của lệnh. Nguyên văn đề xuất nằm trong `ghi_chu`.
   - Đề xuất PT3/PT4 dùng "≈ 3,4" / "≈ 4,0" và đặt chữ "OpenAI …" ở cột `ty_le_relief_pct`. P chuyển sang khuôn 20 cột, giống cách P-1810 đã làm.
   - Đề xuất T3 ở dạng "a | b | c" được đổi sang khuôn; nguyên văn để trong `ghi_chu`.
6. **Lỗi cũ trong sổ, không sửa:** dòng `V1` (12/10, dòng 8) của COST-LEDGER có 21 cột, vì dấu phẩy trong `ghi_chu` không được bọc nháy. P-1810b không sửa dòng cũ; cần một lượt P sửa riêng.
7. **RIGHTS đã có `W4-MPFB-A5`** (P-1810, cho PT2). Lệnh ghi "theo PT2/PT4", nên P thêm dòng **A5b** cho PT4 thay vì sửa dòng cũ.

## 5. Chi phí
| Mục | Trần | Thực tế |
|---|---|---|
| Claude API (gọi từ script) | $0 | **$0** |
| ElevenLabs | 0 | **0** ký tự |
| YouTube Data API | 0 | **0** đơn vị |
| OpenAI | 0 | **$0** (không gọi) |
| Giờ máy | ≤ 1 h | **≈ 0,45 h thời gian thực** (≈ 06:00 → 06:30 UTC). Các tiến trình chính: fetch đủ nhánh ≈ 10 phút, golden 12,6 phút, selftest_ll 5,5 phút (song song), 7 selftest khác 0,8 phút, verify.sh ×3, pip/npm |
| Token | trần mềm | không đo được trong phiên |

**Chỉ số trong ±5 % quanh ngưỡng:**
- Phiên này không có chỉ số nào trong ±5 %. Gần nhất là golden t1 SSIM 0,9548 so ngưỡng 0,90 (+6,1 %).
- Từ sổ đã ghi:
  - **V5b-2d Claude $1,918 so trần $2 (−4,1 %)**, trong ±5 %; V5b-2d tự nêu.
  - PT3: ảnh 39,47/40 MB (−1,3 %) và hệ số nắn c6 1,143/1,2 (−4,75 %), PT3 §10 tự nêu.
  - PT4: toy_like 4,0, nhãn 38 px, chu kỳ đi 8 khung, đều = ngưỡng; PT4 §10 tự nêu.

**Dòng đề xuất cho `COST-LEDGER.csv`** (ghi ở lần P kế): `P-1810b,Hợp nhất 18/10 chiều (2 nhánh) + ghi sổ 18/10,P,2026-10-18,,,,,0,0,không gọi API,0,0,0.45,,,,,reports/P-1810b-BAO-CAO.md §5,YouTube 0; OpenAI 0; giờ máy = thời gian thực`.

## 6. Nhánh đã đặt tên (chỉ tạo tên mới, không xoá nhánh cũ)
Lệnh đã chạy (sau `git ls-remote` xác nhận 3 tên chưa có trên origin):
```text
git push origin 233f5fa6f1e72ac4759964a69b71e98d48dac3ea:refs/heads/v5b2c \
                1eecfec21f92f0aeb6c7df14f82871d9a620391d:refs/heads/v5b2d \
                61946e1787acc99e3f73deed264e405b0984bb26:refs/heads/k2c-t3-loi
```
| Tên mới | Commit | Nhánh harness cũ (giữ nguyên) |
|---|---|---|
| `v5b2c` | `233f5fa6` (V5b-2c) | `ccr-11686158-4ucx09` (cùng commit); `ccr-8f16467a-mhu954` chứa commit này |
| `v5b2d` | `1eecfec2` (V5b-2d) | `ccr-8f16467a-mhu954` (cùng commit) |
| `k2c-t3-loi` | `61946e17` (lời v4.1 khoá) | `claude/k2c-t3-loi-khoa-al1itg` (cùng commit; đã merge vào p-1810b) |

## 7. Việc chờ chủ dự án
1. **Claude điều phối rà `p-1810b` → ff `main`.** `p-1810b` là hậu duệ thẳng của `origin/main` `209a1a27`: `git checkout main && git merge --ff-only origin/p-1810b && git push origin main`.
2. **Nguyên văn Q1–Q2 (09:23) và nghĩa của VL1 = (a)** (§4 điểm 1). Nếu VL1 không phải quyết định cho KA2026 thì vẫn cần chọn a/b/c cho tấm im lặng KA2026 (`KHOA-LOI-41-BAO-CAO.md` §6 mục 1).
3. **Xác nhận các ánh xạ K15-n = K1–K8 (K-1.15) và V2D-n = đề xuất 1–6 (V5b-2d §8)**, và nội dung Q-PT4-4 (§4 điểm 2–3).
4. **Open Parliament Licence:** cần một phiên đọc được parliament.uk (hoặc Claude Cowork) chép nguyên văn và câu ghi công vào RIGHTS `P1810B-HANSARD` trước G2.
5. **T3 Gibraltar:** chờ cổng hình V6 → G1b (LK4 xem lại ở G1b).
6. **Nhánh chưa merge:** `v5b2c`/`v5b2d` (= `ccr-8f16467a-mhu954`, `ccr-11686158-4ucx09`), `v5b2b`, `pt2-lai`, `pt3-van-nuong`, `pt4-song`, và V6 đang chạy. Khi các nhánh này merge, đường dẫn trong RIGHTS `P1810B-*` thành tệp có trên main.
7. **Ảnh AI (PT2/PT3/PT4):** giữ "chỉ nghiên cứu" cho tới khi V6 dùng trên hình. Lúc đó P ghi lại phạm vi trong RIGHTS.
8. Sửa dòng `V1` 21 cột trong COST-LEDGER (§4 điểm 6) và ghi dòng `P-1810b` (§5) ở lần P kế.
