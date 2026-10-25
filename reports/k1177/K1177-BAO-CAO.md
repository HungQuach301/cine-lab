**Nhánh thật: `claude/k1177-animatic-checks-nfbsbr`** (harness buộc tên này; lệnh ghi `checks-1-17-7`). Gốc `origin/main` @2a49e3ca (LOCK 1.17.6 `513c9442…`). Không merge, không đụng `main` hay nhánh khác (ANIMATIC-T4-V2 và P-2510b không đụng).

# Phiên K-1.17.7 — luật cho animatic v2 + bản cuối T4 London theo gói "50 % tiết kiệm" + khiếu nại ANIMATIC-T4 A1–A5, C11, C13 — BÁO CÁO

> Phiên K, 25/10/2026 ≈ 02:25 → ≈ 04:00 UTC (09:25 → 11:00 Asia/Saigon). Mọi số là số đo thật trong phiên; tệp số đo ở `reports/k1177/do/`.
> Căn cứ (nguyên văn, Asia/Saigon): 25/10 09:08 "Vấn đề tôi concern nhất là chỉ phí bị đội nhiều, còn các vấn đề khác đều có thể nới để tăng chất lượng và độ chân thực của hình ảnh / Người xem cũng không phải là người chuyên về khảo cổ hay gì để có thể nhận ra những dự khác biệt nhỏ trong những frame hình ngắn"; 09:15 "Duyệt gói 50 % tiết kiệm + P1–P10 theo khuyến nghị"; 06:56 C11, C13 theo khuyến nghị.
> Email chủ dự án không có trong tệp, commit, header, URL, payload hay User-Agent nào (UA `CineLab-research (+https://github.com/HungQuach301/cine-lab)`). Không in/ghi khoá (proxy gắn khoá).

## 0. Khối điều lệ và tóm tắt
| Trường | Lệnh | Thực tế |
|---|---|---|
| Nhánh | `checks-1-17-7` từ origin/main @2a49e3ca | harness buộc `claude/k1177-animatic-checks-nfbsbr` (ghi ở dòng đầu); gốc đúng @2a49e3ca |
| Vùng sửa | `checks/**`, `checks-appeal.md`, `reports/k1177/**` | đúng. Không sửa `docs/`, sổ, `scripts/`, `design/`, `channel-k2/`, `main`, nhánh khác |
| Khiếu nại trước phán quyết | chép A1–A5 (§9.3) + C13 vào `checks-appeal.md` TRƯỚC khi phán | commit `839d4b52` 02:34:36 UTC (kèm C11 nguyên văn, ghi chú C14, căn cứ 25/10); phán quyết thêm sau đo |
| Chi phí | Claude API mốc $3 (chặn $10), OpenAI mốc $1 (chặn $4), Gemini 0, giờ máy 5 h | **Claude API $0,3033 · OpenAI $0 · Gemini $0** · giờ máy ≈ 1,6 h (§11) |
| Preflight | `set -o pipefail`; commit chỉ khi "— ĐẠT"; hook trước lần đẩy đầu | hook pre-commit + pre-push cài 02:34 (trước lần đẩy đầu 02:35); mọi commit/push "PREFLIGHT ĐẠT" (mã chưa khoá: cất `checks/` bằng stash khi commit/đẩy — `reports/k1177/day.sh`) |
| `lock.py` không `--verify` | đúng một lần ở bước khoá cuối | **HAI lần — LỆCH LỆNH, nêu rõ (§7, §12 Sự cố):** lần 1 03:37:32 (`6c320eeb…`, KHÔNG commit, KHÔNG đẩy) — preflight chặn email tác giả (bên thứ ba) trong giấy phép MIT của mô hình YuNet; che email (luật cứng) đổi cây → khoá lại lần 2 03:38:17 (`3a53574c…`, cây được commit). Không có lần nào khác |
| Force/amend/dừng hỏi | không | không |
| Đẩy ≤ 30 phút + CHECKPOINT | bắt buộc | `reports/k1177/CHECKPOINT.md` (Trạng thái + Lệnh bổ sung đã áp) |

**Tóm tắt:**
1. **A1 (= C13 (1)) — LUẬT THIẾU CHỮ, sửa:** hệ toạ độ log máy ghi rõ (hệ cảnh y lên, từ `goc_toa_do`); nhận `toa_do: EN`, `cam_en`, `diem_neo_en`; [E, N, h] khai nhầm trường (> 100 km) → đổi + (w).
2. **A2 (= C13 (2)) — LỖI LUẬT 2 lớp, sửa:** neo [E, N, h] đọc như hệ cảnh (điểm cách ≈ 560 km) + (c) chỉ so khung CUỐI shot tham chiếu. H5-07b 62 139 px (trượt giả) → **0,00 px** (khung đầu M03); H2-12 0,08 px (đạt giả) → **0,128 px** thật (khung 202/403 giữa H1-03; đầu/cuối 51,9/51,7 px). MAY-19 (c) T4: **1 → 0**.
3. **A3 (= C11) — LỖI LUẬT, sửa theo C11 (a):** từ T4 K-LAI-1 không tính M-d. T4 v1 **TRƯỢT 20,4 % → ĐẠT** (0 % ngoài M-d).
4. **A4 — KHÔNG phải lỗi thước; chẩn đoán của phiên chưa đúng:** Q37 (a) so beats với mốc ĐẶC TẢ, không với biến cố đo; 12 lớp chồng không có trong đặc tả. Thêm khuôn `p.lop_chong` (mốc `at`, `at + mo_vao_s`).
5. **A5 — KHAI SAI KHUÔN** (RULES 1.17.0 rõ): không đổi luật; thông báo nay chỉ khuôn episode.yaml `n2p.tam`.
6. **Gói tiết kiệm (9 việc):** GOC-CAO (`goc_cao_min_pct` + 5 chốt cấu trúc) · TU-LIEU trần tới 20 % + lớp THAT + TU-LIEU-THAT · K-LAI-1 (Q2) · TL-1 (c) miễn ranh M-d/tư liệu (T4 v1: **6,22 → 2,94 cắt/phút**) · NHAN-VAT-TEN (YuNet, mặt ≤ 1/8) · KIEM-2-MUC · q_thoi_dai lớp công trình mốc (**H2-13 v1 bắt 3/3, khung đúng 0/3**) · BMN sàn Y nhấp nháy (K1176-D6).
7. Selftest `selftest_k1177.py` **87/87**; cũ k112…k1176, k2, ll đạt trên cây đã khoá (§6) — **1 kỳ vọng cũ đổi theo lệnh** (selftest_k1176: ca "khai 20 → (k)" thành "khai 25 → (k)" vì trần duyệt 15 → 20). **LOCK 1.17.6 `513c9442…` → 1.17.7 `3a53574c…`**, `--verify` KHỚP.
8. Animatic T4 v1 (k2check 1.17.6 ↔ 1.17.7, cùng video): đổi K-LAI-1, MAY-19, TL-1, N2P-1…4 (thông báo), GOC-CAO-60 → GOC-CAO + 3 hàng mới; khai thử tham số T4: GOC-CAO 3 lỗi mở/kết + 4 chuỗi liền, NHAN-VAT-TEN THIẾU chân dung/duyệt, KIEM-2-MUC (d) H2-13 (§8). **T3 1.17.6 ↔ 1.17.7: §9.**

## 1. Dữ liệu và tiêu chí (đặt TRƯỚC khi đo)
- **Animatic T4 v1 trong `main`:** `channel-k2/k2c-t4-02/animatic/` (episode.yaml, timeline.json, log-shot.json 74 shot, 58 log máy, 23 clip M-d `omni/clip`, kiểm 2 tầng `omni/kiem*`). Animatic gốc (`e4a4b09a…`, 206 MB) ở ngoài git → video kiểm = **nối 3 bản xem** (`reports/animatic-t4/xem/*`, ffmpeg concat copy) → `anim-xem-noi.mp4` 730,146 s, 640×360, **SHA-256 `4263d29dcb96637e920385556a1ce344bf5894fd70b5b6fef21deeec05d4685c`** (tái tạo: `do/chay_t4.sh` + danh sách concat 3 tệp theo `reports/animatic-t4/xuat.json`). Cùng video cho 1.17.6 và 1.17.7 → so được hàng đổi; số video-phụ thuộc (BIEN-CO-V, Q37 b–d, TL-1 c–d) là của bản xem (bitrate thấp), không thay số của animatic gốc.
- **Khai thử tham số T4** (ngoài `channel-k2`, `/var/tmp/k1177/t4/k2c/animatic/`: symlink mọi tệp gốc + episode.yaml/log-shot.json chép có thêm khai): `goc_cao_min_pct: 50`, `goc_cao_chuong_min_pct: 40`, `tl1_muc_tieu_pct: 60`, `tu_lieu_tran_pct: 20`, `be_mat_nha_px_m_min: 4`, `be_mat_nha_y_san_nhap: 0.01`, `kiem_2_muc: true`; mọi đoạn M-d `muc_kiem: day_du`, `so_luot` (từ tag), `kiem_t1`, `clip`; H1-01b `nhan_vat_ten: Thomas Farriner`, H2-07 `Nicholas Barbon`; H2-13 `cong_trinh_moc: ["St Paul's Cathedral with Wren's dome (completed 1710)"]`, `chan_troi_city: true`.
- **T3 bản cuối:** như K-1.17.6 §9 — `git archive origin/main channel-k2/k2c-t3-01 reports/animatic-t3-v2 reports/k1172/do reports/k1173/do AUTHORSHIP.md RIGHTS.md docs` + git cục bộ, `mk_tl.py` (761,9998 s; SHA `0ff3f0da…`), `mk_log_chu.py` (1 524 khung; `17053dff…`), master LFS `release-k2-t3-g2` **SHA `5b9f0bcc…` khớp**. 1.17.6 chạy lại trên cây gốc: **trùng hệt** `reports/k1176/do/k2check-1.17.6-t3.md` (trừ tiêu đề).
- **Tiêu chí (đặt trước):** A2 — khung KHOP phải khớp ≤ 0,5 px với ÍT NHẤT một khung của shot tham chiếu khi cùng máy thật (đo bằng ma trận máy) và lệch thật vẫn bắt; A4 — tách "thước (a) sai" với "đặc tả thiếu mốc"; lớp mốc q_thoi_dai — H2-13 v1 phải bắt, 3 khung đúng không báo; YuNet — 0 báo nhầm > 1/8 ở ngưỡng chọn trên 23 clip M-d, báo tỉ lệ bắt/sót theo đáp án bằng mắt; mỗi luật ≥ 1 ca đạt + ≥ 1 ca trượt; tập không khai giữ hành vi 1.17.6; T3 giống hệt ngoài hàng mới.

## 2. Phán quyết A1–A5, C11, C13
### A1 (= C13 (1)) — LUẬT THIẾU CHỮ (sửa)
MAY-19 đọc `cam.p`, `tieu_diem`, `diem_neo` theo **hệ cảnh y lên** (x = E − E0, y = h, z = −(N − N0)), nhưng RULES/K1174 §5 chỉ nói "log.json render_ldn.js". Phiên ANIMATIC khai đúng hướng (ghi thêm `cam` hệ cảnh, giữ `cam_en`) nhưng **`diem_neo` vẫn ghi [E, N, h] trong trường hệ cảnh** — lỗi ẩn gây ra A2. 1.17.7 (`q_k1174.chuan_log`, `_diem_neo`): RULES ghi rõ hệ; log khai `toa_do: EN` hoặc chỉ có `cam_en` → đổi theo `goc_toa_do`; trường mới `diem_neo_en`; toạ độ trong trường hệ cảnh có thành phần 1 hoặc 2 > 100 km → đổi + (w). Selftest: log EN = log hệ cảnh (cùng số đo), log chỉ `cam_en` → đạt.

### A2 (= C13 (2)) — LỖI LUẬT 2 lớp (sửa)
Tái hiện (log máy thật, `do/` mục A2 trong CHECKPOINT):
| KHOP | Tham chiếu | 1.17.6 | Neo đúng hệ, khung đầu/cuối tham chiếu | 1.17.7 (khung gần nhất) |
|---|---|---|---|---|
| H5-07b | M03 (DAY, máy tiến 80 m) | **62 139,81 px TRƯỢT** (neo ≈ 560 km) | 0,00 / 36,03 px | **0,00 px** (khung 0/264) |
| H2-12 | H1-03 (TRUOT 105 m) | 0,08 px "đạt" (giả) | 51,92 / 51,66 px | **0,128 px** (khung 202/403) |
| H3-06 | H3-01 (CODINH) | 0,0 | 0,0 / 0,0 | 0,0 |
| H4-08 | H2-12 (KHOP) | 0,0 | 0,0 / 0,0 | 0,0 |
Nguyên nhân: (i) neo [532118, 181150, 111] đọc như toạ độ cảnh → điểm ở xa vô cực, phép 7 điểm chỉ còn đo hướng nhìn (trượt giả khi hướng khác, đạt giả khi hướng song song); (ii) (c) so khung CUỐI shot `khop_voi` — sai khi tham chiếu di chuyển (H5-07b về khung ĐẦU M03; H2-12 về khung GIỮA H1-03). Sửa: neo đổi hệ (A1); (c) so khung đầu shot KHOP với **khung gần nhất** của shot tham chiếu (ghim được `khop_khung: dau | cuoi | <giây>`), in `khop_khung_ref`. Ca trượt giữ (selftest): máy dời 5 m so mọi khung → (c); ghim `cuoi` khi chỉ khớp khung đầu → (c).

### A3 (= C11) — LỖI LUẬT (mâu thuẫn Q2) — sửa theo C11 (a) chủ dự án duyệt 06:56
Từ T4 (`q_k1177.klai1_t4`, gọi trong k2check): K-LAI-1 không tính đoạn minh hoạ M-d (tính ở MINH-HOA/N2P-6, tổng AI ≤ 70 %); `ai_image`/`ai_texture` ngoài M-d vẫn ≤ 20 % (log khung trừ cửa sổ M-d, hoặc shot ai_image ngoài M-d). T4 v1: 148,67 s = 20,4 % **TRƯỢT → ĐẠT** (ngoài M-d 0,00 s). T3: q_lai không đổi (selftest: cùng log T3 vẫn trượt).

### A4 (= ghi chú C14) — KHÔNG phải lỗi thước; bổ sung khuôn
Q37 / NHIP-K2 / Q37 (1.13) (a) đối chiếu **beats khai với mốc của ĐẶC TẢ** (`spec_times`: mốc `at` của `p.places/tags/cap/year/title…`), không với biến cố đo trên video — độ trễ mờ vào 0,4–0,5 s không tham gia (a). 12 mốc (thẻ nhân vật, bộ đếm, tư liệu) do `ghep.py` đặt nhưng **không có trong `shots[].p`** của episode.yaml → (a) đúng định nghĩa ("biến cố tự khai không được nhận"). Ví dụ H1-18: bộ đếm 0,242 s "khớp" chỉ vì cách mốc cắt 0 s < 0,3 s; 3,142 s không có mốc nào. 1.17.7 (`q_nhip.spec_times`): đặc tả nhận `p.lop_chong: [{at, k, s, mo_vao_s?}]` — mốc `at` và `at + mo_vao_s`; phía dựng ghi lớp chồng vào đặc tả (ghép đọc từ đó), không dịch mốc. Đặc tả không `lop_chong` → như cũ (T3 giống hệt).

### A5 — KHAI SAI KHUÔN (không đổi luật)
k2check đo N2P-1…4 trên **ảnh** (render đối chứng, ghép, mặt nạ lớp) khai ở **episode.yaml** `n2p: {tam: [{id, shot, render, ghep, mat_na, nam, anh_tinh?, lop_a?}]}` (RULES 1.17.0). `n2p.tam` trong log shot của animatic (`{tag, kiem, ghep, v, khoang_s}`) là KẾT QUẢ kiểm của phiên, không đo lại được. 1.17.7 chỉ sửa thông báo THIẾU: khi thấy khuôn log, nêu khuôn đúng.

## 3. Luật đổi / mới (1.17.7)
| Hàng | Tệp | Trường đọc (tập) | Ngưỡng | Mức |
|---|---|---|---|---|
| **GOC-CAO** (thay GOC-CAO-60, từ T4) | `q_k1177.goc_cao`, `q_k1174.check`, `k2check`, `cap112` | `goc_cao_min_pct` (mặc định 60; nhận 50–100), `goc_cao_cau_truc`, `goc_cao_chuong_min_pct` (40 khi chốt bật), `goc_cao_p1` ("P1"), `goc_cao_hoi`; log shot `goc`, `tl`, `chuong`, `diem_may`, `log_may`, `lop.THAT` | (p) tỉ lệ ≥ ngưỡng (trừ THAT); chốt khi < 60 hoặc khai: (a) chương mở+kết góc cao; (b) P1 mỗi hồi cùng khung (≤ 1 m, ≤ 1°, cùng FOV); (c) ≤ 2 liền {thấp, cận, M-d, THAT}; (d) chương ≥ 40 % | Chặn (p)(a)–(d)(k) G2 · Cảnh báo animatic · (w) luôn Cảnh báo |
| TL-1 (a) (e) | `q_k116.tl1` | `tl1_muc_tieu_pct` (mặc định 75; T4 60) | góc cao + tl ≥ mục tiêu | Cảnh báo (như cũ) |
| TL-1 (c) P9 (từ T4) | `q_k116.tl1`, `q_k1177.ranh_mien/cat_mien` | log shot `minh_hoa` (đoạn), `that`/`lop.THAT`, `tu_lieu_lan` | mỗi ranh miễn 1 cắt ±0,5 s; in trước/sau | Cảnh báo |
| TU-LIEU-10 | `q_k1176.tran_tu_lieu`, `tu_lieu_10` | `tu_lieu_tran_pct` (mặc định 10; **≤ 20**), lớp `THAT` | TL + KHAC + THE + THAT ≤ trần; mỗi lần ≤ 10 s | Chặn G2 · Cảnh báo animatic (như cũ) |
| TU-LIEU-OMNI | `q_k1176.tu_lieu_omni` | `LOP_TU_LIEU` + THAT | không trùng/ghép liền clip M-d | như cũ |
| **TU-LIEU-THAT** (mới) | `q_k1177.tu_lieu_that` | `that: {loai, hien_dai?, giay_phep: {tep, sha256}}`, `lop.THAT` | (a) không AI; (w) goc cao không tính; (g) footage hiện đại có giấy phép + SHA | Chặn (a)(g) G2 · Cảnh báo animatic |
| K-LAI-1 (từ T4) | `q_k1177.klai1_t4`, `k2check` | log shot `minh_hoa`, `ai_image`; `lai.log_khung` | AI ngoài M-d ≤ 20 % | Chặn (P2-2, như cũ) |
| **NHAN-VAT-TEN** (mới) | `q_k1177.nhan_vat_ten/do_mat`, `checks/models/face_detection_yunet_2023mar.onnx` | đoạn M-d `nhan_vat_ten`, `chan_dung_tham_chieu {tep, sha256}`, `duyet_chu_du_an`, `clip` (hoặc `--master`) | mặt lớn nhất (YuNet ≥ 0,75) ≤ 1/8 chiều cao khung; 0,60–0,75 > 1/8 → (w) | Chặn (a)(k)(u)(m) G2 · Cảnh báo animatic · (w) Cảnh báo |
| **KIEM-2-MUC** (mới) | `q_k1177.kiem_2_muc` | `kiem_2_muc`; đoạn `muc_kiem`, `so_luot` (hoặc tag `luot`), `kiem_t1`, `kiem`, `to_khung`, `nhan_vat_ten`, `cong_trinh_moc`, `chan_troi_city` | (a) bắt buộc day_du khi có tên/mốc/City; (b) tầng đủ; (c) nen ≤ 2, day_du ≤ 3 lượt; (d) lớp mốc q_thoi_dai khi có mốc/City | Chặn G2 · Cảnh báo animatic |
| q_thoi_dai lớp mốc | `q_thoi_dai.prompt_for/_khoa/_chuan/soi_khung`, CLI `--lop-moc`, `--moc` | — | mục 9 `cong_trinh_moc`; không qua bước 2 | lưới lọc (O2 không đổi khi không bật) |
| MAY-19 (A1, A2, THAT) | `q_k1174.chuan_log/_diem_neo/la_that/may19` | `goc_toa_do`, `toa_do: EN`, `cam_en`, `diem_neo_en`, `khop_khung`; `that` | (c) khung gần nhất ≤ 0,5 px; (w) khai EN nhầm trường | như cũ |
| Q37 (a) (A4) | `q_nhip.spec_times` | đặc tả `p.lop_chong [{at, mo_vao_s?}]` | ±0,3 s | như cũ |
| N2P-1…4 (A5) | `q_n2p.check` | — | thông báo | như cũ |
| BE-MAT-NHA (d) (K1176-D6) | `q_k1176.y_san_nhap/nhap_nhay_san`, `q_k1175.kiem_bmn/be_mat_nha` | `be_mat_nha_y_san_nhap` (0–0,05; mặc định 0; T4 0,01) | nhấp nháy ≤ 0,012 trên điểm Y ≥ sàn | như cũ |
| SACH-1 (b) (THAT, từ T4) | `q_k116.sach1` | đặc tả `p.that` | ảnh/footage thật toàn khung không là "tư liệu đứng riêng" | như cũ |
| — | `cinecheck/__init__.py` VERSION 1.17.7, `ll/RULES-LL.md` §1.17.7, `ll/cap112.py`, `ll/k2check.py`, `ll/q_k117.py` (chữ), `models/README.md`, `models/LICENSE-yunet.txt` (email đã che), `ll/selftest_k1177.py`, `ll/fixtures/k1177/` | — | — | — |

## 4. Cách khai cho phía dựng (tên trường)
- **T4 episode.yaml (gốc):** `goc_cao_min_pct: 50` · `goc_cao_chuong_min_pct: 40` · `tl1_muc_tieu_pct: 60` · `tu_lieu_tran_pct: 20` · `be_mat_nha_y_san_nhap: 0.01` · `kiem_2_muc: true` (giữ `be_mat_nha_px_m_min: 4`, `goc_toa_do`). Tuỳ chọn: `goc_cao_p1` (mặc định P1), `goc_cao_hoi` (mặc định chương "HỒI…").
- **Log shot — máy:** log máy theo hệ cảnh (như hiện ghi `cam`); nếu chỉ có [E, N, h] → `toa_do: EN` ở gốc log. Điểm neo KHOP khai **`diem_neo_en: [E, N, h]`** (không để [E, N, h] trong `diem_neo`). Muốn ghim khung tham chiếu: `khop_khung: dau | cuoi | <giây>`.
- **Log shot — ảnh/footage thật:** shot riêng `that: {loai: anh | footage | footage_hien_dai, nguon, hien_dai?: true, giay_phep?: {tep, sha256}}`, `lop: {THAT: <giây>}`, `cu_may: THAT` (tuỳ chọn), `goc: phang`; mỗi lần ≤ 10 s; không ghép liền clip M-d (≥ 1 shot 3D hoặc ≥ 1 s 3D xen giữa). Đặc tả shot: `p.that: true` (SACH-1). Lần tư liệu trong shot 3D: `tu_lieu_lan: [{t0, t1, lop}]` (giây tuyệt đối) — cũng để TL-1 (c) miễn ranh.
- **Mục đoạn M-d (`minh_hoa: [{…}]`):** `muc_kiem: day_du | nen`, `so_luot: <số lượt sinh>`, `kiem_t1: <tệp Flash>`, `kiem: <tệp tầng 2>`, `to_khung: <tờ khung soi tay>` (nen), `clip: <mp4 đoạn>`; nhân vật có tên: `nhan_vat_ten`, `chan_dung_tham_chieu: {tep, sha256}`, `duyet_chu_du_an: "<dòng AUTHORSHIP, giờ>"`; công trình mốc / chân trời City: `cong_trinh_moc: ["<tên + dạng ở năm>"]`, `chan_troi_city: true` → tầng 2 chạy `q_thoi_dai.py --anh … --nam N --moc "<tên>; <tên>"`.
- **Đặc tả lớp chồng (Q37 a):** `segments[].shots[].p.lop_chong: [{at: <giây trong đoạn>, k: the_nhan_vat | bo_dem | tu_lieu, s: "<chữ>", mo_vao_s: 0.45}]` — beats giữ như hiện (`t` = `at` hoặc `at + mo_vao_s`).
- **Tấm nền N2+ (A5):** episode.yaml `n2p: {noi, t4: true, tam: [{id, shot, render: <PNG render đối chứng>, ghep: <PNG ghép>, mat_na: <PNG mặt nạ lớp>, nam, anh_tinh: true}], video: [{shot, ghep, render, mat_na, chuyen_tam}]}`.

## 5. Hiệu chuẩn
### 5.1 Lớp công trình mốc q_thoi_dai (việc 6) — `do/moc/`, sổ `so-ai.jsonl`
| Khung | Năm | Đáp án (lập trước) | Đề bài 1.15 (bộ đệm ANIMATIC) | Lớp mốc có danh sách | Lớp chung (không danh sách) |
|---|---|---|---|---|---|
| H2-13-l2 k25 | 1711 | thiếu mái vòm St Paul's → phải bắt | — | **bắt** (tin 0,8) | — |
| H2-13-l2 k55 | 1711 | phải bắt | 0 nghi vấn (chỉ ghi chú tin 0,35) | **bắt** (0,8) | **bắt** (0,6) |
| H2-13-l2 k90 | 1711 | phải bắt | — | **bắt** (0,8) | — |
| H3-04b-l1 k55 | 1935 | đúng (vòm có) → không báo | 0 | **không báo** | — |
| H4-01b-l1 k55 | 1940 | đúng → không báo | 0 | **không báo** | **không báo** |
| H2-01a-l1 k55 | 1666 sau cháy | đúng (Old St Paul's đổ nát) → không báo | 0 | **không báo** | **không báo** |
→ có danh sách: **bắt 3/3, báo nhầm 0/3**; lớp chung: bắt 1/1 (tin 0,6 — sát ngưỡng 0,5), nhầm 0/2. Khuyến nghị khai danh sách `cong_trinh_moc`.
### 5.2 Bộ dò mặt YuNet (việc 5) — `do/mat/DAP-AN.md`
Trên 23 clip M-d T4 v1 (347 hộp ≥ 4 % khung, soi bằng mắt): điểm ≥ **0,75** → 160 hộp, **0 sai**, 0 hộp > 1/8; điểm 0,60–0,73 lẫn lửa/khói cao 0,13–0,64 khung → chỉ (w). **Bắt/sót** trên 8 khung đáp án (mặt thấy được ≥ 3,5 % khung): **bắt 8/18 (44 %)**, sót 10 = mặt nhỏ ≤ 6 % khung (điểm 0,51–0,61) và mặt nghiêng đội mũ sắt (H4-04b). Không clip T4 v1 nào có mặt thật > 1/8 → 0 TRƯỢT oan. Mặt cận chính diện (khung H2-03c cắt + phóng): cao 0,236 khung → điểm 0,89 (bắt).

## 6. Selftest
- `checks/ll/selftest_k1177.py` **87/87** (không mạng/API; mô hình nhìn giả lập; fixtures 2 ảnh 640×360 trong `fixtures/k1177/`): GOC-CAO 22 (mặc định + chốt tắt, khai 50, (k), (a)–(d), P1 có log cùng khung / máy dời 40 m / không log animatic–G2, THAT, (e) TL-1, q_k1174.check, áp dụng T3) · TU-LIEU-10 7 (trần 20/25, mặc định 10, THAT (a)(b)) · TU-LIEU-OMNI 2 · TU-LIEU-THAT 5 + cấp 1 · K-LAI-1 3 · TL-1 (c) 3 · NHAN-VAT-TEN 5 + cấp 2 · KIEM-2-MUC 11 + cấp 1 · q_thoi_dai 4 · MAY-19 8 (A1/A2 7, THAT 1) · Q37 (a) 3 · N2P A5 1 · BMN D6 5 · cấp GOC-CAO 3 · áp dụng 1. Mỗi luật đổi/mới ≥ 1 ca đạt + ≥ 1 ca trượt.
- Selftest toàn bộ trên cây ĐÃ KHOÁ (`do/selftest-sau-khoa.txt`, 03:48 UTC, LOCK KHỚP): k112 75/75 · k1121 48/48 · k1122 37/37 · k113 64/64 · k114 126/126 · k115 105/105 · k116 144/144 · k117 130/130 · k1172 74/74 · k1173 42/42 · k1174 91/91 · k1175 52/52 · k1176 62/62 · **k1177 87/87** · k2 129/129 · ll 317/317 — **0 SAI**, rc 0. Lượt trước khoá (`do/selftest-truoc-khoa.txt`) cũng đạt hết.
- **Kỳ vọng cũ đổi: 1** — `selftest_k1176` ca "TU-LIEU-10 (k)": "khai 20 (> 15 %) → (k)" thành "khai 25 (> trần duyệt) → (k)" vì lệnh nâng trần duyệt 15 → 20 (chủ dự án 25/10 09:15). Mọi ca khác giữ nguyên (k1174 GOC-CAO-60, MAY-19 KHOP, k1175/k1176 nhấp nháy: không đổi — tham số mới mặc định = hành vi cũ).

## 7. LOCK
Cũ 1.17.6 `513c9442fe1cb9950bdf01c3be4dc93b32c4413d9260109c86f0f5d90e5b8ec3` → **mới 1.17.7 `3a53574ce8c2094e4f79bc1fac88cf3e6f7bbe61993ab5a1cf695834a2067b08`** (DATE_UTC 2026-10-25T03:38:17Z), `--verify` KHỚP (ngay sau khoá, mọi commit/push, hàng LOCK k2check). **`lock.py` không cờ gọi 2 lần (lệch lệnh):** lần 1 03:37:32 → `6c320eeb…` — commit bị preflight chặn (email tác giả Shiqi Yu trong `checks/models/LICENSE-yunet.txt`, giấy phép MIT của YuNet); luật cứng "che email" ⇒ che email trong bản chép (README ghi SHA bản gốc `c83b8120…`) ⇒ cây đổi ⇒ khoá lần 2 03:38:17. Cây `6c320eeb` chưa từng commit/đẩy; giữa hai lần không đổi tệp nào khác.

## 8. Kết quả trên animatic T4 v1 (k2check `--cap --no-asr`, cùng video `4263d29d…`)
Bảng đủ: `do/k2check-1.17.6-t4.md`, `do/k2check-1.17.7-t4.md`, `do/k2check-1.17.7-t4-khai.md`; so hàng: `do/so-t4.md`, `do/so-t4-khai.md`. Mã thoát cả ba: 1. Hàng TRƯỢT: 1.17.6 **10** (Q26b, Q34, Q37, NHIP-K2, Q26b-K2, Q37 (1.13), **K-LAI-1**, K-LAI-2, SACH-1, XEM-CAM) → 1.17.7 **9** (bỏ K-LAI-1) — các hàng còn lại TRƯỢT vì luật kênh/khai như báo cáo ANIMATIC-T4 §9 (không thuộc phiên này).
| Hàng | 1.17.6 | 1.17.7 (episode.yaml như hiện, không khai mới) | 1.17.7 khai tham số T4 (§1) |
|---|---|---|---|
| **K-LAI-1** | TRƯỢT 148,67 s = 20,4 % | **ĐẠT** — M-d 148,67 s tính ở MINH-HOA/N2P-6; ngoài M-d 0 % | như cột trước |
| **MAY-19** | CẢNH BÁO — (c) H5-07b 62 139,81 px | CẢNH BÁO — (c) **0**; (w) 4: diem_neo [E, N, h] của H2-12, H3-06, H4-08, H5-07b (khai `diem_neo_en`) | như cột trước |
| **TL-1** | CẢNH BÁO — (a) 67,5 % < 75; (c) 75 cắt = 6,22/phút > 5; (d) M03 3,76, H2-11 2,70, H5-03 3,73 %/s; (f) 7 | CẢNH BÁO — (a) như cũ; **(c) sạch: 75 cắt − 39 ranh M-d = 2,94/phút** (in "trước miễn 6,22"); (d)(f) như cũ | CẢNH BÁO — **(a) sạch** (67,5 % ≥ 60); (c) sạch; (d)(f) như cũ |
| GOC-CAO-60 → **GOC-CAO** | ĐẠT 479,5 / 714,1 s = 67,2 % | ĐẠT 67,2 % / 60 (chốt cấu trúc TẮT — không khai) | **CẢNH BÁO** 67,2 % / 50 · **(a) 3**: HỒI 1 mở H1-01a (M-d), kết H1-19 (M-d); HỒI 2 mở H2-01a (M-d) · **(c) 4**: H1-01a–H1-01b–H1-02; H1-19–H2-01a–H2-01b; H2-03c–H2-04a–H2-04b; H4-03–H4-04a–H4-04b · (b) 0 (P1 cùng khung ở mọi hồi) · (d) 0: MÓC 95, HỒI 1 61, HỒI 2 57, HỒI 3 45, HỒI 4 68, HỒI 5 92 % |
| TU-LIEU-10 | CẢNH BÁO 9,66 % / 10 (±5 %) · (b) H2-02 15 s | như cũ (chỉ chữ ngưỡng) | 9,66 % / **20** · (b) H2-02 15 s (lớp TL+THE không khai `tu_lieu_lan` → tính cả shot) |
| **TU-LIEU-THAT** (mới) | — | KHÔNG ÁP (không THAT) | KHÔNG ÁP |
| **NHAN-VAT-TEN** (mới) | — | KHÔNG ÁP (không khai) | **CẢNH BÁO** — H1-01b (Farriner), H2-07 (Barbon): mặt lớn nhất **0,000** khung (≤ 1/8 ĐẠT); THIẾU (k) chân dung tham chiếu, (u) duyệt chủ dự án; (w) H1-01b 9 hộp 0,60–0,75 cao > 1/8 (lửa, lớn nhất 0,156) |
| **KIEM-2-MUC** (mới) | — | KHÔNG ÁP | **CẢNH BÁO** — 23 đoạn day_du: (a)(b)(c) 0; **(d) H2-13**: có mốc/chân trời City nhưng q_thoi_dai tầng 2 chạy đề bài cũ (đúng bài học: H2-13 thiếu mái vòm lọt qua) |
| N2P-1…4 | CẢNH BÁO — "chưa khai tấm kiểm (n2p.tam)" | CẢNH BÁO — cùng lỗi + chỉ khuôn episode.yaml (A5) | như cột trước |
| MINH-HOA | CẢNH BÁO | chỉ đổi chữ giá trị ("xem … GOC-CAO") | như cột trước |
| BE-MAT-NHA | KHÔNG ÁP (chưa tấm BMN) | như cũ | như cũ (khai px/m 4, sàn Y 0,01 — chưa có tấm) |
| 57 hàng khác (Q26b … BIEN-CO-V, O2, SACH-1, PP-1, EO-DAT, N2P-5/6, BAN-DO-12, AI-TU-LIEU, GEMINI, TU-LIEU-OMNI …) | — | **giống hệt** | giống hệt (trừ TL-1, TU-LIEU-10, GOC-CAO, NHAN-VAT-TEN, KIEM-2-MUC) |
| LOCK | KHỚP (1.17.6) | KHỚP (1.17.7) | KHỚP |
Q37 (a) (A4) không đổi trên T4 v1: đặc tả chưa có `p.lop_chong` — phía dựng thêm ở bản sau (§4).

## 9. So k2check 1.17.6 ↔ 1.17.7 trên bản cuối T3
Đầu vào §1; 1.17.6 chạy lại từ cây gốc (stash mã mới, LOCK 513c9442 KHỚP) — **trùng hệt** `reports/k1176/do/k2check-1.17.6-t3.md` (trừ tiêu đề). Bảng đủ: `do/k2check-1.17.6-t3.md`, `do/k2check-1.17.7-t3.md`; so hàng `do/so-t3.md`.
| Hàng | 1.17.6 | 1.17.7 | Lý do |
|---|---|---|---|
| 55 hàng (Q26b … Q37, A1–A13, NHIP-K2, BIEN-CO-V, K-LAI-1…6, O2, SACH-1 … PC-1, MINH-HOA, EO-DAT-R1…R4, CONG-BO-1, N2P-1…6 "KHÔNG ÁP", 1.17.4 (T4), 1.17.5 (T4), LOCK) | — | **giống hệt** (kết quả + giá trị + danh sách lỗi + cấp) | luật 1.17.7 chỉ tập từ T4; Q37 (a) `lop_chong` không có trong đặc tả T3 |
| TL-1 | CẢNH BÁO | CẢNH BÁO — kết quả, giá trị, lỗi, cấp **giống hệt**; chỉ **cột chữ "Ngưỡng"** thêm "(1.17.7: `tl1_muc_tieu_pct` theo tập) … 1.17.7 từ T4: ranh vào/ra M-d…" | chữ mô tả ngưỡng chung của hàng (không đổi phép đo T3) — nêu để đủ |
| LOCK | KHỚP (1.17.6) | KHỚP (1.17.7) | chỉ nhãn phiên bản |
Mã thoát cả hai: 1; TRƯỢT như K-1.17.6 (7 hàng: Q37, NHIP-K2, Q37 (1.13), BIEN-CO-V, K-LAI-2, XEM-CAM, EO-DAT-R3). **Ngoài chữ ngưỡng TL-1 và nhãn LOCK: không hàng nào đổi.**

## 10. Chỉ số trong ±5 % quanh ngưỡng (luật cứng — nêu tên)
- **T4 v1 TU-LIEU-10 9,66 % so trần mặc định 10 % (−3,4 %)** (không khai; với `tu_lieu_tran_pct: 20` xa ngưỡng).
- **T4 v1 TL-1 (d) H4-07 trôi 2,0 %/s so trần 2 (0 %)** (trên bản xem nối; hàng Cảnh báo; như animatic 2,09 %/s).
- T4 v1 (không do phiên này đổi, in lại theo bảng): A1 −14,0 LUFS (cận −13,8/−15); Q37 (1.13) khung tĩnh 5,83 / 5,83 / 5,75 s so 6 s; thẻ chương 3,0 s = trần 3; thẻ PP1 9,0 s (cận trên) / PP2 7,0 s (cận dưới).
- Hiệu chuẩn: lớp mốc chung (không danh sách) bắt H2-13 ở tin **0,6 so ngưỡng 0,5 (+20 %)** — nêu vì là biên mỏng của cách khai không danh sách; có danh sách 0,8.
- Selftest tổng hợp: BMN nắng tắt có sàn 0,0112 so 0,012 (−6,7 %, ngoài ±5 %); YuNet fixture xa 0,093 so 1/8 = 0,125 (−26 %).
- Xa ngưỡng (ghi để rõ): GOC-CAO 67,2 % (60: +12 %; 50: +34 %); chương thấp nhất HỒI 3 45 % so 40 (+12,5 %); TL-1 (a) 67,5 % so mục tiêu 60 (+12,5 %); TL-1 (c) 2,94 cắt/phút so 5 (−41 %); MAY-19 H2-12 0,128 px so 0,5.

## 11. Chi phí thật
| Khoản | Số |
|---|---|
| Claude API | **$0,3033** = claude-sonnet-5-5 (`claude -p`, judge.call) 9 lần q_thoi_dai lớp mốc (hiệu chuẩn việc 6) — sổ `reports/k1177/so-ai.jsonl` (model, lệnh, SHA đề bài/ảnh vào/trả lời ra, usage, giá), bản ghi thô `do/moc/tho/*/run.jsonl.gz` |
| OpenAI / Gemini / ElevenLabs / RunPod / YouTube | **0** |
| Tải | YuNet 232 589 B (HF, MIT); master T3 LFS 1,79 GB (SHA `5b9f0bcc…` khớp) |
| Giờ máy | ≈ 1,6 h đồng hồ container (≈ 02:25 → ≈ 04:00 UTC): k2check 7 lượt (T4 ×4 + khai ×2, T3 ×2; 6–12 phút/lượt, P ≤ 2), selftest toàn bộ 2 lượt (≈ 6 phút/lượt), YuNet 23 clip ≈ 1 phút |
| Token phiên chính | không đo được từ container |

## 12. Sự cố
1. **`lock.py` không `--verify` 2 lần (lệch lệnh "đúng một lần").** Lần 1 (03:37:32, `6c320eeb…`) commit bị preflight chặn: `checks/models/LICENSE-yunet.txt` (giấy phép MIT bắt buộc kèm mô hình YuNet) chứa email tác giả bên thứ ba. Không có cách giữ cây khoá mà vẫn che email (luật cứng) → che email trong bản chép (README ghi SHA bản gốc `c83b8120…`) và khoá lần 2 (03:38:17, `3a53574c…`). Cây lần 1 không commit/đẩy; không tệp nào khác đổi giữa hai lần. Bài học: chạy `tools/preflight.sh --staged` trên `checks/` TRƯỚC lệnh khoá.
2. **Vòng chờ `pgrep -f` tự khớp chính lệnh chờ — 2 lần** (03:15 `until ! pgrep -f "chay.sh …"`, 03:30 `kill -0 $(pgrep -f "k2check.py …")`) — lặp BAI-HOC K-1.17.6 (1) và ANIMATIC-T4 (3). Dừng theo PGID (không giết nhầm tiến trình nào; k2check đã xong). Từ 03:38 chờ theo PID ghi lúc khởi chạy (`setsid … & echo $!`).
3. Hai lỗi trong chính bài selftest_k1177 (truyền trùng tham số `goc`; ca "19 % trong một shot 19 s" vướng (b) ≤ 10 s/lần) và một ca tổng hợp nhấp nháy (nhiễu quá lớn) — sửa bài thử, không sửa luật (85 → 87 ca sau khi thêm ca `so_luot`).
4. Script selftest chép từ P-2510 sai thư mục gốc lượt đầu (`../..` từ `reports/k1177/do`) → sửa `../../..`, chạy lại.
5. KIEM-2-MUC (c): log shot animatic dùng `luot` là TAG lượt chọn ("H1-05a-l3-360p"), không phải số lượt → trường đếm đổi tên `so_luot`; không khai thì lấy cận dưới từ tag (sửa trước khoá, selftest +2 ca).

## 13. Quyết định đề xuất (chủ dự án)
| # | Đề xuất | Phương án | Ưu | Nhược | Tác động | Rủi ro | Khuyến nghị |
|---|---|---|---|---|---|---|---|
| **K1177-D1** | Duyệt luật 1.17.7 (A1/A2 sửa, A3 theo C11, A4 khuôn lop_chong, A5 thông báo, 9 việc gói tiết kiệm) | A: duyệt. B: giữ 1.17.6 | A: T4 qua K-LAI-1, MAY-19 (c) đúng; luật theo gói tiết kiệm. B: không đổi | A: thêm khai cho phía dựng (§4) | T4 animatic v2 + bản cuối | thấp | **A** |
| **K1177-D2** | 5 chốt GOC-CAO ở mức Chặn G2 khi khai 50 % | A: Chặn (a)–(d) như đã khoá. B: (c) "≤ 2 liền" chỉ Cảnh báo | A: hạ 60 → 50 % được "đổi" bằng cấu trúc rõ. B: dựng nhanh hơn | A: animatic v1 vướng (a) 3 + (c) 4 → bản v2 phải chèn 3D mở/kết HỒI 1–2 và tách 4 chuỗi M-d/thấp | T4 v2 dựng | A: thêm 1–2 s 3D mỗi chỗ (rẻ: dựng 3D, không Omni) | **A** (sửa ở v2: chèn 3D góc cao trước H1-01a, sau H1-19, trước H2-01a; xen 3D trong 4 chuỗi) |
| **K1177-D3** | Đo mặt nhân vật có tên bằng YuNet (≥ 0,75, trần 1/8) | A: như đã khoá (TRƯỢT ≥ 0,75; (w) 0,60–0,75). B: thêm soi tay bắt buộc mọi đoạn có tên | A: máy, không API, 0 báo nhầm trên 23 clip. B: chắc hơn với mặt nghiêng | A: sót mặt nghiêng/đội mũ (bắt 44 % mặt nhỏ; mặt cận chính diện bắt). B: thêm chạm người | M-d có nhân vật có tên | A thấp (KIEM-2-MUC buộc day_du + tờ khung cho đoạn có tên) | **A** |
| **K1177-D4** | Lớp công trình mốc q_thoi_dai | A: bắt buộc khi đoạn khai `cong_trinh_moc`/`chan_troi_city` (như khoá), khai danh sách tên. B: bật lớp chung cho mọi khung tầng 2 | A: bắt 3/3, nhầm 0/3, khoá bộ đệm cũ giữ. B: không phụ thuộc khai | A: phụ thuộc phía dựng khai đủ. B: tin 0,6 sát ngưỡng; tốn thêm ≈ 0 (cùng lần gọi) | T4 M-d có chân trời | A: thiếu khai → lọt (như H2-13) | **A + khai `chan_troi_city` cho mọi M-d thấy chân trời City** |
| **K1177-D5** | Q37 (a) lớp chồng | A: phía dựng ghi `p.lop_chong` vào đặc tả (mk_ep/ghep đọc từ đó). B: nhận beats lớp chồng từ log ghép | A: một nguồn sự thật. B: không đổi pipeline | A: sửa mk_ep/ghep. B: tự khai — trái nguyên tắc (a) | T4 v2 | thấp | **A** |
| **K1177-D6** | Sàn Y nhấp nháy BMN mặc định | A: theo tập (mặc định 0 như lệnh; T4 khai 0,01). B: mặc định 0,01 cho mọi tập từ T4 | A: không đổi tập không khai. B: không quên khai | A: T4 phải khai. B: đổi hành vi mặc định | T4 shot nắng tắt có B | thấp | **A** (đã khoá) — T4 khai `be_mat_nha_y_san_nhap: 0.01` |
| **K1177-D7** | TL-1 (c) miễn ranh M-d (P9) | A: như khoá (miễn 1 cắt/ranh ±0,5 s). B: chỉ miễn ranh M-d ↔ 3D cùng khoảnh khắc | A: T4 v1 6,22 → 2,94 cắt/phút. B: chặt hơn | A: gần nửa số cắt được miễn — nhịp cắt thật của phim vẫn 6,2/phút (TL-1 chỉ Cảnh báo) | T4 | thấp | **A**; P/chủ dự án xem nhịp thật ở PHIEU-XEM |

## 14. Dòng sổ đề xuất (P ghi — phiên này không sửa sổ)
- **COST-LEDGER:** `2026-10-25 · K-1.17.7 · Claude API $0,3033 (9 lần q_thoi_dai lớp mốc, hiệu chuẩn) · OpenAI 0 · Gemini 0 · ≈ 1,6 h máy · tải LFS 1,79 GB + YuNet 0,23 MB`.
- **AUTHORSHIP:** ghi khi chủ dự án trả lời K1177-D1…D7 (nguyên văn + giờ). Căn cứ đã có: 25/10 09:08, 09:15 "Duyệt gói 50 % tiết kiệm + P1–P10 theo khuyến nghị", 06:56 "C11, C13 theo khuyến nghị".
- **RIGHTS:** công cụ kiểm (không vào sản phẩm): `checks/models/face_detection_yunet_2023mar.onnx` — YuNet (OpenCV Zoo / ShiqiYu libfacedetection.train), MIT, HF `opencv/face_detection_yunet` rev `3cc26e7f`, SHA-256 `8f2383e4dd3cfbb4553ea8718107fc0423210dc964f9f4280604804ed2552fa4`. Fixture `checks/ll/fixtures/k1177/mat-*.jpg` = khung clip M-d của dự án (Gemini Omni, sổ AI T4) cắt/phóng — tài sản dự án, chỉ dùng kiểm.
- **Kinh thánh (P):** §19 (c) trần tư liệu T4 20 % + lớp THAT (ảnh/footage thật; footage hiện đại có giấy phép + SHA); §15/§13.6 GOC-CAO 50 % + 5 chốt cấu trúc; §15 M-d: nhân vật có tên mặt ≤ 1/8 khung + chân dung + duyệt; kiểm 2 mức day_du/nen.
- **BAI-HOC-K2 (đề xuất):** (1) `pgrep -f` trong vòng chờ — LẶP lần 5 → ghi vào khối vận hành mọi lệnh: "chờ theo PID (`setsid … & echo $!` + `kill -0 <pid>`)"; (2) chạy `tools/preflight.sh --staged` trên `checks/` trước `lock.py` (tệp bên thứ ba có email); (3) toạ độ khai phải ghi hệ trong tên trường (`*_en`) — một trường [E, N, h] lẫn hệ cảnh tạo cả trượt giả lẫn đạt giả; (4) KHOP về shot di chuyển: so khung gần nhất, không khung cuối; (5) lớp chồng do trình ghép đặt phải có trong đặc tả, không chỉ trong beats.

## 15. Việc chờ chủ dự án
1. Trả lời **K1177-D1…D7** (§13) — khuyến nghị: D1 A, D2 A, D3 A, D4 A + khai chân trời City, D5 A, D6 A, D7 A.
2. Phiên P: merge `claude/k1177-animatic-checks-nfbsbr` khi duyệt (nhánh này **không** merge); ghi sổ theo §14.
3. Phía dựng T4 (ANIMATIC-T4-V2 / bản cuối): khai §4 — tham số episode.yaml, `diem_neo_en`, `that`, mục đoạn M-d (`muc_kiem`, `so_luot`, `kiem_t1`, `clip`, nhân vật/công trình có tên), `p.lop_chong`, `n2p.tam` ở episode.yaml; sửa cấu trúc góc cao (D2: mở/kết HỒI 1–2, 4 chuỗi liền); H2-13 chạy lại q_thoi_dai `--moc` (mái vòm St Paul's 1711).

**DỪNG chờ chủ dự án.**
