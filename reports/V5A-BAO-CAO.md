# Báo cáo phiên V5a — nâng cấp phần KHÔNG chạm T2 (15/10/2026)

> Nhánh `v5a` từ `origin/main` @7255aa4. **Chưa merge** (P merge giữa hai tập, sau T2). **DỪNG chờ chủ dự án.**

## 0. Điều lệ phiên (lệnh + thực tế)
| Trường | Lệnh | Thực tế |
|---|---|---|
| Loại phiên | V (bộ công cụ), lệnh giao thêm `scripts/common`, `scripts/ll/qc.py`, `toolkit/market/brief.py` | đúng; sửa ngoài vùng V mặc định theo lệnh (FILE-ZONES: "lệnh thắng") |
| Nhánh | `v5a` từ `origin/main` | `v5a` @7255aa4, 4 commit, đã đẩy |
| CẤM chạm | `scripts/k2/**`, `design/k2v/**`, `assets/k2/archive/**`, `channel-k2/k2c-t2-01/**`, `docs/BIBLE-KENH2.md`, `checks/**` | **không sửa** (chỉ đọc `design/k2v/common.js`, `relief.js` để lấy mã màu). Không đọc mã `checks/`: k2check chỉ được **chạy** qua dòng lệnh công bố trong `K-1.11-BAO-CAO.md` §2 |
| Tệp đã sửa/thêm | — | `scripts/common/{preflight_scan,versions}.py` (sửa); `scripts/common/{release_check,cc0_fetch,lut}.py` + `scripts/common/tests/` (mới); `scripts/ll/qc.py` (sửa), `scripts/ll/k2hook.py`, `scripts/ll/tests/test_k2hook.py` (mới); `toolkit/market/brief.py` (sửa), `toolkit/tests/test_brief_ab.py` (mới); `tools/lfs-allow.txt` (thêm 2 dòng); `assets/k2/cc0/**`, `assets/k2/lut/*.cube` (mới); `reports/v5a/`, báo cáo này; ghi thêm `RIGHTS.md` (V5a-01..04), `COST-LEDGER.csv` (dòng V5a) |
| Trần chi phí | Claude API ≤ $1 (ghim model) · ElevenLabs 0 · YouTube API 0 | **Claude API $0** (không gọi) · ElevenLabs **0** · YouTube API **0** |
| Preflight | bắt buộc | hook pre-commit/pre-push cài đầu phiên; `tools/preflight.sh --range origin/main..HEAD` **ĐẠT**, `lock.py --verify` **KHỚP** (§9) |
| Merge | không merge | không merge |

## 1. Tóm tắt
| # | Việc | Kết quả | Test |
|---|---|---|---|
| 1 | Preflight P5 không bắt `licenses/…` trong URL | regex `(?<![\w/.:\-])(?:\./)?licenses/…`; trước sửa: `http://creativecommons.org/licenses/publicdomain/` → đòi tệp `licenses/publicdomain` (chặn nhầm); sau sửa: dùng mặc định `licenses/<clip_id>.txt` | 10/10 (6 regex + 4 tích hợp repo git tạm) |
| 2 | `scripts/common/release_check.py` (mới, dùng chung) | R1–R8; **Steel: mô tả 5 502 ký tự → LỖI R2**; Steel TRƯỢT 5 LỖI, T1 TRƯỢT 2 LỖI (§2) | self-test 12/12 + 7 unittest (gồm 2 ca gói thật) |
| 3 | `qc.py --k2check` (hoặc `K2CHECK=1`) | có `checks/ll/k2check.py` → thêm dòng **K2**; chưa có (main hiện tại) → bỏ qua êm, chỉ ghi chú dưới bảng. **Chạy thật** với checks 1.11.1 (nhánh `checks/v1.11`, tách ra thư mục tạm) trên fixture T1: 8,6 phút, mã thoát 1, báo cáo `k2check.md` đúng định dạng K | 6/6 (k2check giả + trạng thái repo thật) |
| 4 | `brief.py ab` — brief thumbnail A/B theo TEARDOWN §9 | `THUMBNAIL-BRIEF-AB.md`: [A] BẢN ĐỒ TƯƠNG PHẢN / [B] CƠ CHẾ LỘ RA; mỗi phương án: chủ thể, chữ ≤ 4 từ, tương phản (thủ pháp + tỉ lệ WCAG), tham chiếu ngách; CLI cũ giữ nguyên | 8/8 mới + 29/29 `test_market.py` cũ |
| 5 | Thư viện CC0 (Mốc D3) | **23 mục, 121 tệp, 105,5 MB** (≤ 300 MB), 15 tệp > 1 MB qua LFS, **0 URL bị chặn**, verify KHỚP (§4) | 6 unittest offline + `cc0_fetch.py verify` |
| 6 | LUT (Mốc D4) | 3 LUT 33³; tờ so sánh 12 khung T1 phát hành; **đề xuất `k2-a-thep-lanh`** (§5). Chưa gắn vào render | self-test 7/7 (ΔE2000 khớp 4 ca chuẩn Sharma 2005) + 4 unittest |
| 7 | `versions.py` + COST-LEDGER | nhóm mới `common`, `market`, `assets_k2`; công cụ máy `git_lfs`, `opencv`; bản ghi cũ (T2) không đổi kết quả (test); dòng `V5a` | 2 unittest |

## 2. Việc 2 — chạy thử `release_check.py` trên gói Steel và T1
Lệnh: `/opt/cine/bin/python scripts/common/release_check.py channel-k2/<tập>/phat-hanh [--them UPDATE.txt] [--md] [--json]`.

| Mục | Steel `k2g-ep01` | T1 `k2c-t1-06` |
|---|---|---|
| R1 tiêu đề ≤ 60 | chính 55 ✓ · **dự phòng 70 → LỖI** | **chính 63 → LỖI** · dự phòng 53 ✓ |
| R2 mô tả ≤ 5 000 | **5 502 → LỖI (thừa 502)**; nếu dán `UPDATE-14-10.txt` → 5 995 | 4 585 ✓ |
| R3 dòng 1 là câu móc | **LỖI**: dòng 1 là câu miễn trừ | **LỖI**: dòng 1 là câu miễn trừ |
| R4 miễn trừ trong 3 dòng đầu | ✓ (dòng 1) | ✓ (dòng 1) |
| R5 không email | ✓ | ✓ |
| R6 nguồn đầy đủ ở bình luận ghim | **LỖI ×2**: không có tệp bình luận ghim; mục SOURCES của mô tả có 22 URL | ✓ (bình luận ghim 8 261 ký tự, 30 nguồn) |
| R7 chương YouTube | ✓ 14 mốc | ✓ 12 mốc |
| Kết luận | **TRƯỢT, 5 LỖI** | **TRƯỢT, 2 LỖI** |

- R3 trên cả hai tập là do luật mới (QUAN-TRI-RUI-RO §4 mục 5 sửa 15/10 trên nhánh `checks/v1.11`). Hai tập làm trước luật này. Theo lệnh, tôi **không sửa tệp tập cũ**; chỉ ghi nhận ở đây.
- **Ngưỡng ±5 %:** Steel dự phòng 70/60, T1 chính 63/60 (+5 %: nằm sát biên), mô tả Steel 5 502/5 000 (+10 %). Bình luận ghim T1 8 261/10 000: không sát ngưỡng.

## 3. Việc 3, 4 — chi tiết ngắn
- `qc.py`: cờ `--k2check` bị gỡ khỏi `sys.argv` trước khi đọc tham số tập, nên lệnh cũ `qc.sh <episode.yaml>` không đổi. `k2hook.py` chỉ truyền tệp có thật (`--tl/--master/--mix/--logs`), ghi `<out>/k2check.{md,json}`.
- Lần chạy thật (T1, chỉ timeline, không master/log) đúng như báo cáo K §1: Q32, Q35, Q36, Q37 TRƯỢT; A1–A13 CHỈ BÁO; LOCK KHỚP 1.11.1.
- `brief.py ab`: kiểm đọc, không chặn. Các mục kiểm: chữ > 4 từ; A > 2 từ (TEARDOWN gợi ý); B có chữ; số ngoài claims; cụm cấm; chữ lặp từ của tiêu đề; tương phản chữ/nền < 4,5:1 hoặc sát ngưỡng ±5 %; thủ pháp tương phản sai ngữ pháp; tiêu đề > 60 / không mở bằng "Why" / emoji. Hai phương án trùng chủ thể → DỪNG (A/B phải khác ý đồ).
- **Chỗ lệnh và mẫu khác nhau:** lệnh ghi "chữ ≤ 4 từ"; TEARDOWN §9 ghi A tối đa 2 từ, B không chữ. Tôi đặt ≤ 4 là trần cảnh báo cứng. Mức 2 từ / không chữ chỉ là cảnh báo gợi ý (§10, mục 4).

## 4. Việc 5 — thư viện CC0 `assets/k2/cc0/` (danh mục + giấy phép)
Tải bằng `scripts/common/cc0_fetch.py fetch`; kiểm lại bằng `… verify` (23 mục, 121 tệp KHỚP, 105,5 MB). URL, SHA-256 và kích thước từng tệp ghi trong `catalog.json`. Bảng đọc: `CATALOG.md`. Ảnh xem trước: `reports/v5a/CC0-XEM-TRUOC.jpg`, dựng Blender workbench, ngoài cây tài sản.

| Chủ đề | Mục (nguồn) |
|---|---|
| tàu | `ph-dutch-ship-medium` (Poly Haven, tàu buồm cho cảnh quá khứ) · `q-cruise-ship`, `q-boat` (Quaternius) |
| cần cẩu | `ph-overhead-crane` (Poly Haven) · HDRI `ph-hdri-freight-station` (ga hàng có cẩu) |
| container | `q-container-red`, `q-container-green`, `q-cargo-train-container` (Quaternius) · vật liệu tôn sóng `acg-corrugated-steel` (ambientCG 1K) |
| nhà máy | `ph-factory-facade`, `ph-industrial-pipes` · HDRI `ph-hdri-industrial-sunset` |
| nhà ở | `ph-urban-apartments` · `q-house` (2 kiểu), `q-building-large` |
| biên giới | `ph-concrete-road-barrier`, `ph-chainlink-fence` |
| xe tải | `q-truck` (xe thùng thường; không dùng bản bọc thép) |
| tàu hỏa | `q-cargo-train-front`, `q-railway-track` · HDRI `ph-hdri-freight-station` |
| cảng / hạ tầng | `ph-ocean-buoy`, HDRI `ph-hdri-docklands`, `ph-electricity-poles` |

**Giấy phép** (`assets/k2/cc0/licenses/`, lưu dạng chữ, ngày tải 15/10/2026):
- `cc0-1.0-legalcode.txt`: văn bản pháp lý CC0.
- `polyhaven-license.txt`: "Our assets are all licensed as CC0…".
- `ambientcg-license.txt`.
- `quaternius-license.txt` và `quaternius-<gói>-License.txt`: "CC0 1.0 Universal (CC0 1.0) Public Domain Dedication".
- `quaternius-<gói>-page.txt`: trang gói, kèm liên kết CC0 trên trang.
- Gói Simple Buildings **không có License.txt** trong thư mục tải, nên bằng chứng là trang gói (liên kết `publicdomain/zero/1.0`) cộng trang giấy phép chung.
- Email liên hệ của tác giả trên trang Quaternius đã được thay bằng `[email đã ẩn]`, theo RUNBOOK §3 và preflight P1. Phần chữ giấy phép giữ nguyên.

**URL bị chặn: không có.** Poly Haven (API + `dl.polyhaven.org`), ambientCG (API v2) và Quaternius (thư mục Google Drive công khai, mở từ nút Download trên trang gói) đều tải được qua proxy. Kích thước và md5 khớp API Poly Haven và ambientCG.

**LFS:** đã thêm dòng `assets/k2/cc0/*` vào `tools/lfs-allow.txt`, theo lệnh việc 5. 15 tệp > 1 MB được đánh dấu trong `assets/k2/cc0/.gitattributes`, tổng ≈ 88 MB hạn mức LFS. `assets/k2/lut/*.cube` (0,97 MB mỗi tệp) nằm trong git thường.

**Nhận xét chất lượng (chưa dùng vào cảnh):**
- Hai phong cách lẫn nhau: Poly Haven là PBR tả thực, Quaternius là low-poly màu phẳng.
- Kênh dùng sticker toon 3 nấc (k2v) nên Quaternius hợp sticker hơn; Poly Haven hợp cảnh 3D đặc trưng và HDRI chiếu sáng.
- Chưa có **tàu container hiện đại** CC0 ở ba nguồn này: Poly Haven chỉ có tàu buồm, Quaternius chỉ có tàu khách và tàu nhỏ.

## 5. Việc 6 — LUT (Mốc D4): tờ so sánh và đề xuất
- Tờ so sánh: `reports/v5a/LUT-SO-SANH.jpg` (12 hàng × GỐC | A | B | C, có dải màu nhận diện qua LUT). Số đo: `reports/v5a/study.json`. Mốc khung: `reports/v5a/lut-frames.json`.
- **12 khung** lấy từ master T1 phát hành qua LFS (`release-k2c-t1-06-v1`, oid 4f2d280bc649), đọc từng khung qua HTTP, không tải cả tệp. Mốc (giây): 8, 44, 95, 178,5, 190, 340, 470, 509, 515, 600, 830, 900. Mẫu gồm biểu đồ 3D, ảnh lưu trữ (2), footage Pexels (3), cảnh phố 3D, bản đồ và thẻ văn bản.
- **Bảng màu đích:**
  - nhận diện `NHAN-DIEN.md` §2: #0F1722, #16212F, #EEF1F4, #9AA7B5, #B9C3CE, #F08A4B, #3CC2B0, #F2C14E;
  - cặp sepia của Kinh thánh §4 (mực #2A1C10 / giấy #F1E4C6, lấy từ `relief.js`).
- **Cách đo** (CIEDE2000, D65):
  - ΔE trung thành = ΔE00(LUT(màu), màu) cho 8 màu nhận diện;
  - ΔE bảng màu = 8 màu chủ đạo k-means Lab của khung → màu bảng gần nhất, có trọng số diện tích;
  - ΔE dịch = độ đổi trung bình từng điểm ảnh.

| LUT | Mô tả | ΔE trung thành max (8 màu) | ΔE sepia (mực/giấy) | Chữ/nền | ΔE bảng màu TB (gốc 7,97) | Khung gần bảng hơn | ΔE dịch TB |
|---|---|---|---|---|---|---|---|
| **A `k2-a-thep-lanh`** | bóng tối ám mực xanh đen, vùng sáng trắng lạnh, −12 % bão hoà màu nền, giữ cam/hổ phách/lục lam, S 18 %, **khoá màu nhận diện** | **0,13** | 0,79 / 1,89 | 15,90:1 | **6,94 (−13 %)** | **12/12** | 2,07 |
| B `k2-b-trung-tinh` | như A nhưng nhẹ (S 10 %, không đổi bão hoà), khoá màu | 0,09 | 2,79 / 0,71 | 15,89:1 | 7,45 (−7 %) | 12/12 | 1,48 |
| C `k2-c-cam-lam` | tách tông lục lam–hổ phách mạnh, **không khoá** (đối chứng) | **19,68** | 23,83 / 12,71 | 14,72:1 | 12,18 (+53 %) | 0/12 | 12,23 |

- **Đề xuất: A `k2-a-thep-lanh`.**
  - Đưa cả 12/12 khung về gần bảng màu kênh nhất.
  - Không đổi màu đồ hoạ đã vẽ đúng nhận diện: ΔE ≤ 0,13, không nhận ra bằng mắt.
  - Giữ tương phản chữ 15,9:1.
  - Đổi ảnh ở mức nhẹ (ΔE dịch ≈ 2, vừa nhận ra).
  - C cho thấy vì sao phải khoá: chữ trắng thành vàng kem, nền biểu đồ thành lam, giấy sepia thành vàng chanh.
- Với cảnh sepia, A kéo giấy 1,89 ΔE (dưới ngưỡng 2 nhưng **sát ngưỡng ±5 %**). Đề xuất V5b áp LUT cho **footage và cảnh TỰ NHIÊN**, còn cảnh/ảnh sepia không áp hoặc áp yếu. V5b quyết sau T2 G2.
- **Hạn chế:** ΔE bảng màu đo khoảng cách tới 10 màu đích, mà cảnh thật (cây, trời, gạch) vốn không nằm trong bảng. Vì vậy số này dùng để **so sánh tương đối giữa các LUT**, không phải mục tiêu tuyệt đối. Chấm bằng mắt trên tờ so sánh vẫn cần chủ dự án.
- **CHƯA gắn vào render.** `lut.py apply` chỉ áp offline lên khung.

## 6. Việc 7 — phiên bản và chi phí
- `versions.py`:
  - nhóm mới `common` (`scripts/common`, `tools`), `market` (`toolkit/market`), `assets_k2` (`assets/k2/cc0/catalog.json` + `assets/k2/lut`). Thư viện CC0 được băm qua catalog chứ không băm từng tệp LFS, vì bản clone có `smudge --skip` chỉ có con trỏ;
  - công cụ máy mới: `git_lfs` 3.4.1, `opencv` 5.0.0.
- **Tác động đến T2 khi merge:** nhóm `ll` có thêm `k2hook.py` và sửa `qc.py`. Một tập đã ghi VERSIONS lúc G1 mà kiểm G2 **sau khi** merge v5a sẽ thấy `toolkit.ll` LỆCH. Theo luật merge giữa hai tập, P merge v5a **sau** T2 G2 thì không ảnh hưởng.
- COST-LEDGER dòng `V5a`: Claude API $0 / trần $1; ElevenLabs 0 ký tự; YouTube API 0 đơn vị. Giờ máy ≈ 0,2 h: k2check thật 8,6 phút, LUT 12 khung 34 s, xem trước CC0. Tải mạng: 105,5 MB tài sản CC0 + khung LFS T1.

## 7. Test (chạy lại cuối phiên, đều OK)
| Bộ | Kết quả |
|---|---|
| `scripts/common/tests/test_preflight_scan.py` | 10/10 |
| `scripts/common/tests/test_release_check.py` | 7/7 (+ self-test 12/12) |
| `scripts/common/tests/test_v5a_tools.py` (lut, cc0_fetch, versions) | 11/11 (+ lut self-test 7/7) |
| `scripts/ll/tests/test_k2hook.py` | 6/6 |
| `toolkit/tests/test_brief_ab.py` | 8/8 |
| `toolkit/tests/test_market.py` (cũ, hồi quy) | 29/29 |

## 8. Ghép thử
| Nhánh | Kết quả `git merge-tree` |
|---|---|
| `origin/main` | sạch |
| `origin/teardown-fon` | sạch |
| `origin/k2c-t2` | xung đột `RIGHTS.md` (cả hai cùng ghi thêm ở cuối) |
| `origin/checks/v1.11` | xung đột `RIGHTS.md`, `COST-LEDGER.csv` (cả hai cùng ghi thêm ở cuối) |

Các xung đột thuộc loại tệp dùng chung. P giải bằng cách giữ cả hai khối theo thứ tự thời gian (SESSION-CHARTER §4.4). Không có xung đột mã.

## 9. Preflight
`bash tools/preflight.sh --range origin/main..HEAD` → **PREFLIGHT ĐẠT**; `lock.py --verify` **KHỚP**.
- Trong phiên, preflight chặn đúng hai lần và tôi đã sửa:
  1. email giả trong self-test của `release_check.py`: đổi sang địa chỉ `.test` dựng bằng ghép chuỗi;
  2. email tác giả trên trang Quaternius: đã ẩn.
- Không dùng `--no-verify`.

## 10. Việc chờ chủ dự án
1. **Duyệt V5a** (nhánh `v5a`). Sau duyệt, P merge **sau T2 G2** (xem §6).
2. **Chọn LUT:** đề xuất A `k2-a-thep-lanh`. Quyết luôn: áp cho cảnh sepia hay chỉ cảnh tự nhiên/footage. Xem `reports/v5a/LUT-SO-SANH.jpg`; việc gắn vào render là của V5b.
3. **Gói Steel/T1 trượt release_check:**
   - Steel: mô tả 5 502 > 5 000; chưa có bình luận ghim; dòng 1 là câu miễn trừ; tiêu đề dự phòng 70 ký tự.
   - T1: tiêu đề chính 63 ký tự; dòng 1 là câu miễn trừ.
   - Cần quyết có sửa gói đã/sắp phát hành không. Việc sửa thuộc phiên tập, tôi không sửa.
4. **Chữ thumbnail:** giữ "≤ 4 từ" (lệnh) làm trần, hay hạ về "A ≤ 2 từ, B không chữ" (TEARDOWN §9) thành mức chặn.
5. **Thư viện CC0:**
   - Duyệt danh mục 23 mục (`assets/k2/cc0/CATALOG.md`, ảnh xem trước `reports/v5a/CC0-XEM-TRUOC.jpg`).
   - Quyết thống nhất phong cách: low-poly Quaternius cho sticker, Poly Haven cho cảnh 3D đặc trưng.
   - Duyệt nguồn bổ sung cho **tàu container hiện đại** (ba nguồn hiện có không có).
   - Duyệt hạn mức LFS ≈ 88 MB đã dùng.
6. Duyệt dòng `assets/k2/cc0/*` trong `tools/lfs-allow.txt` (tôi thêm theo lệnh việc 5; tệp ghi "thêm mẫu mới phải có chủ dự án duyệt").
