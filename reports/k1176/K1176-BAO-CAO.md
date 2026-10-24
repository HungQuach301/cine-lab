**Nhánh thật: `checks-1-17-6`** (đúng lệnh; gốc `origin/main` @df317915, LOCK 1.17.5 `c7630b4a…`). Harness gợi ý `claude/beautiful-turing-rqkp8c` — không dùng để đẩy công việc. Không merge, không đụng `main` hay nhánh khác (ANIMATIC-T4 `ccr-21ab5d6f-7l1yln` không đụng).

# Phiên K-1.17.6 — bộ kiểm cho bản cuối T4 London: khiếu nại THU-B KN-1…KN-6 + trần tư liệu T4 + B ≥ 4 px/m — BÁO CÁO

> Phiên K, 24/10/2026 08:20 → ≈ 11:20 UTC (15:20 → 18:20 Asia/Saigon). Mọi số là số đo thật trong phiên; tệp số đo ở `reports/k1176/do/`. Đọc (không sửa) nhánh THU-B `origin/ccr-ce664665-996oyl` @353d0f0c bằng `git archive` vào `/var/tmp/k1176/`; mã THU-B chỉ được CHẠY từ bản sao tạm để tái tạo video kiểm.
> Email chủ dự án không có trong tệp, commit, header, URL, payload hay User-Agent nào (UA `CineLab-research (+https://github.com/HungQuach301/cine-lab)`). Không in/ghi khoá (proxy gắn khoá).

## 0. Khối điều lệ và tóm tắt
| Trường | Lệnh | Thực tế |
|---|---|---|
| Nhánh | `checks-1-17-6` từ origin/main @df317915 | đúng |
| Vùng sửa | `checks/**`, `checks-appeal.md`, `reports/k1176/**` | đúng. Không sửa `docs/`, sổ, `scripts/`, `design/`, `channel-k2/`, `main`, nhánh khác |
| Khiếu nại trước phán quyết | chép nguyên văn KN-1…KN-6 vào `checks-appeal.md` TRƯỚC khi phán | commit 08:40 UTC (sha256 nguồn `7a76f249…`), phán quyết thêm sau đo |
| Chi phí | Claude API mốc $3 (chặn $10), OpenAI $1 (chặn $4), Gemini 0, giờ máy 5 h | **Claude API $0,12 · OpenAI $0,08 · Gemini $0** · giờ máy ≈ 3,0 h (§11) |
| Preflight | `set -o pipefail`; commit chỉ khi "— ĐẠT"; hook trước lần đẩy đầu | hook pre-commit + pre-push cài 08:34 (trước lần đẩy đầu 08:41); mọi commit/push "PREFLIGHT ĐẠT" + `lock.py --verify: KHỚP` (mã chưa khoá: cất `checks/` bằng stash khi commit, chỉ khi không có lượt chạy nền đọc `checks/`) |
| `lock.py` không `--verify` | đúng một lần ở bước khoá cuối | **đúng một lần**, 2026-10-24 10:26:29 UTC (§7) |
| Force/amend/dừng hỏi | không | không |
| Đẩy ≤ 30 phút + CHECKPOINT | bắt buộc | `reports/k1176/CHECKPOINT.md` (mục Trạng thái + Lệnh bổ sung đã áp) |

**Tóm tắt:**
1. **KN-1 = LỖI MÃ, sửa.** T9c trả sớm thiếu khoá khi khung không nước (B3 có 213 px nước < 0,2 % khung; M4 không lớp nước) → KeyError, cả 6 hàng N2P "không chạy được". Nay: T9c KHÔNG ÁP, các phép khác chạy; mọi tấm không nước → N2P-3 KHÔNG ÁP.
2. **KN-2 = LỖI LUẬT, sửa.** N2P-1 (i) trừ vùng nhà đo được nở 1 px của tấm `be_mat_nha_ai`: (a) M1 218 → **0**, B3 224 → **0**, M4 183 → **0**/255. Mở rộng cùng nguyên tắc: vật (a) mô hình nhìn báo có tâm trong vùng BMN → (c) người đọc.
3. **KN-3 = chấp nhận, sửa.** Gọi lại Claude một lần khi thiếu ảnh; sổ ghi cả hai lần. Thiếu ảnh 4/14 lần ở THU-B, 0/2 ở phiên này.
4. **KN-4 = thêm (w) CHỈ BÁO; KHÔNG đề xuất Chặn.** Thước tốt nhất bắt **15/20** ống khói thêm (đáp án lập trước), không điểm vận hành nào 100 %; báo nhầm cao (cửa sổ AI lệch render).
5. **KN-5 = LỖI LUẬT, sửa; một phần là LỖI ẢNH.** (d) theo điểm ảnh + sàn Y ≥ 0,01: **tỉ số bóng (ii-b) nay ĐẠT ở cả 3 khung** (B3 7,2 → 0 %, M4 7,1 → 0 %, M1 32,1 → 1,6 %; M1 nhấp nháy 0,0119 sát trần — K1176-D6); ảnh tĩnh vẫn TRƯỢT (64–100 %). **Chiếu 3D trong trình dựng (ii-a) vẫn TRƯỢT** (B3 9,4 %, M4 7,1 % + nhấp nháy 0,0121, M1 26 %) — bản dựng làm tường sáng lên ~20 % hơn render khi nắng đổi (lệch ánh sáng thật).
6. **KN-6 = LỖI LUẬT, sửa.** (e) ở độ phân giải video: chiếu 3D B3 4,63/12,59 → **2,54/7,40**, M4 4,79/14,68 → **3,46/11,54**, M1 4,90/12,94 → **2,98/8,16** (ĐẠT).
7. **Luật mới:** `be_mat_nha_px_m_min` (mặc định 2; T4 khai 4); TU-LIEU-10 `tu_lieu_tran_pct` (mặc định 10; T4 khai 15; > 15 không nhận) + (b) mỗi lần ≤ 10 s; **TU-LIEU-OMNI** (không trùng / không ghép liền clip M-d).
8. Selftest `selftest_k1176.py` **62/62**; cũ k112…k1175, k2, ll đạt trên cây đã khoá, **0 kỳ vọng cũ đổi**. **LOCK 1.17.5 `c7630b4a…` → 1.17.6 `513c9442…`**, `--verify` KHỚP. T3: §9.

## 1. Dữ liệu và tiêu chí (đặt TRƯỚC khi đo)
- **Tấm thật:** `channel-k2/k2c-t4-02/thu-b/tam/{M1-trung, M4-trung, B3-p4-1938}` (render, ghép l1/l2, mặt nạ lớp/nhà/mặt phẳng, pass bóng, nha.json, proj), khai + k2check 1.17.5 + bộ đệm mô hình nhìn `kiem/*`. Bộ đệm mô hình nhìn của THU-B được chép vào `out` của từng khai → phép đo phiên này KHÔNG gọi lại mô hình (trừ KN-3).
- **Video kiểm không mất** (ngoài git ở THU-B): tái tạo bằng đúng mã THU-B (`dung_lai_du_lieu.sh` → `ldn2.bin` `bd776509…` **trùng** THU-B; `hinh_hoc_thub.py b` → look3b SHA trùng; nướng 1938.7 `55da7758…`; `dung.py` + `bmn_thub.py tl/tiso`, `MA_HOA_KIEM=1`), kịch bản `/var/tmp/k1176/tai/tai_video.sh` (chép ở `do/tai_video.sh`):
| Khung | render | ảnh tĩnh | tỉ số bóng | chiếu 3D | Kiểm tương đương |
|---|---|---|---|---|---|
| B3 1938 | **trùng SHA** | **trùng** | **trùng** | khác SHA (PSNR so bản xem 34,73 dB ≈ nền mã hoá 35,23 dB) | 1.17.5 trên bản tái tạo = đúng số THU-B (15,0 % · 4,6/12,6) |
| M4 2026 | khác SHA | khác | khác | khác | PSNR so bản xem 35,2–37,2 dB; 1.17.5 = đúng số THU-B (57,1 · 7,1 · 7,1 % · 0,0138 · 4,8/14,7) |
| M1 1666 | **trùng** | **trùng** | **trùng** | khác | 1.17.5 = đúng số THU-B (100 · 39,3 · 32,1 % · 0,0199 · 0,0143 · 4,9/12,9) |
- **Tiêu chí (theo lệnh, đặt trước):** KN-1 không lỗi chạy, khung không nước KHÔNG ÁP (iii), phép khác vẫn chạy · KN-2 (a) vẫn bắt mọi điểm (a) ngoài vùng nhà đo được · KN-3 gọi lại 1 lần, sổ ghi cả hai · KN-4 đề xuất Chặn CHỈ KHI bắt 100 % ống khói thêm trên đáp án với báo nhầm thấp · KN-5 dựng lại ánh sáng đúng ĐẠT, dán tĩnh và nhiễu mỗi khung TRƯỢT · KN-6 (e) so ở độ phân giải video.

## 2. Phán quyết từng khiếu nại
### KN-1 — LỖI MÃ (sửa)
Tái hiện: `q_n2p.py kiem/M4-l12/episode.yaml` và `kiem/B3-l2` bằng cây 1.17.5 → `KeyError: 'so_doan_lan'` tại `tong_tam` (đúng traceback THU-B). Nguyên nhân: `q_k1175.t9c` trả sớm dict thiếu khoá khi mặt nạ không có lớp nước (M4) hoặc nước < 0,2 % khung (B3: 213 px). Sửa: T9c trả đủ khoá + `ap: False`; `tong_tam` coi tấm đó là "T9c KHÔNG ÁP", vẫn tính T9b đất→nước + mô hình (b); mọi tấm không nước và 0 lỗi → hàng N2P-3 `KHÔNG ÁP`. Sau sửa: N2P-1…6 chạy trên M4/B3 (bảng §5).

### KN-2 — LỖI LUẬT (sửa)
Màu lớp `nha_thuong` (215,215,215) không có trong bảng N2P → rơi vào màu gần nhất `nha` (235) → toàn bộ nhà thường là lớp (a). Khai `lop_a` không đổi được vì ánh xạ màu xảy ra trước (THU-B đã thử — đúng). Sửa: tấm `be_mat_nha_ai: true` → (i)(a) và dải 20 px (i)(c) trừ vùng nhà ĐO ĐƯỢC nở 1 px (3×3), tính bằng `q_k1176.nha_do` — cùng định nghĩa, cùng ngưỡng px/m với BE-MAT-NHA (selftest: tập nhà trùng `hinh_khoi`).
| Tấm (l2) | Nhà đo được | Vùng trừ | (a) max trước | (a) max sau |
|---|---|---|---|---|
| M1-trung | 557 | 28,15 % khung | 218/255 | **0/255** |
| B3 1938 | 153 | 41,42 % | 224/255 | **0/255** |
| M4-trung | 14 | 29,58 % | 183/255 | **0/255** |
Ca trượt (selftest): AI lấn công trình có tên → (a); khai 4 px/m mà AI phủ nhà 3 px/m → (a). **Hệ quả lộ ra sau KN-1:** mô hình nhìn N2+ (lời nhắc n2p-v1) báo "THÊM công trình: khung cửa sổ…" ngay trong vùng BMN (B3: 12 mục) → cùng nguyên tắc, vật (a) có TÂM hộp trong vùng nhà đo được chuyển thành (c) Cảnh báo người đọc; ngoài vùng vẫn (b) Chặn (selftest 3 ca).

### KN-3 — chấp nhận (sửa)
`q_k1176.goi_claude_du`: Claude không đọc đủ ảnh → gọi lại MỘT lần (BMN (c) và N2+ `q_n2p_vision.soi`); mỗi lần ghi `n2p-cost.jsonl` (dòng của `call_claude` + dòng `ghi: "K-1.17.6 KN-3"`, `lan`, `doc_du`, `goi_lai`); thiếu cả hai → THIẾU; lỗi API/mô hình khác: không gọi lại (fail-closed giữ). Số đo: THU-B 14 lần gọi Claude, 4 lần thiếu ảnh (đọc 2, 2, 2, 6/10) = 29 %; phiên này gọi thật M4 l1 + B3 l1 (hai tấm từng THIẾU): **2/2 đọc đủ 10/10 ở lần 1**, không lỗi thời đại; $0,1997 (sổ AI `so-ai.jsonl`, nguyên văn `do/kn3/`). Đường gọi lại kiểm bằng selftest với mô hình giả lập (2→10: không THIẾU, 2 dòng sổ; 6→3: THIẾU; 10: 1 lần). Ước: tỉ lệ THIẾU giảm từ ≈ 29 % xuống ≈ 8 % nếu các lần độc lập.

### KN-4 — thêm (w) CHỈ BÁO; không đề xuất Chặn
**Đáp án lập trước** (`do/kn4-dap-an.json`, ô soi `do/kn4/soi-dap-an-o3-*.jpg`): B3 l1 **20 ống khói** + **2 đầu hồi** đổi thành mặt mái (trong nhà đo được); l2 **0**. Quan sát then chốt: ống khói AI vẽ ĐÈ lên vùng ảnh của nhiều nhà ở xa (3D phía sau là tường nhà khác) → thước gắn theo nhà/mặt phẳng hụt.
| Thước (lưới) | Ống khói l1 | Đầu hồi l1 | Cụm ngoài đáp án l1 | Cụm ở l2 (sạch) |
|---|---|---|---|---|
| khối màu lạ theo mặt phẳng (96 điểm, `do/kn4-luoi-v2.txt`) | ≤ 4/20 | ≤ 1/2 | 3–4 | 3–9 |
| phần dư affine theo mặt phẳng | ≤ 7/20 | 1/2 | 15 | 10 |
| cạnh mới (không hướng) | ≤ 9/20 | 2/2 | 82–108 | 33–52 |
| **cạnh mới có hướng** (96 điểm, `do/kn4-luoi-v4.txt`) | tối đa **17/20** (khi đó 133–229 cụm nhầm) | 2/2* | — | 68–140 |
| **điểm vận hành chọn** (T_A 8, T_O 5, RAD 2, ≥ 1 m) | **15/20** | 2/2* | 76 (21 nhà) | **23 (14 nhà)** |
\* hai đầu hồi chỉ "trùng hộp" nhờ cửa sổ mới bên trong hộp — thước KHÔNG bắt được đường mái mới; tính là không bắt. Phần lớn cụm nhầm là cửa sổ AI lệch cửa sổ render (`do/kn4/B3-l*-cum-vs-dap-an.jpg`). Mức khung: l1 105 cụm / 587 m cạnh ↔ l2 23 cụm / 77 m (×7,6) — tín hiệu khung rõ, tín hiệu từng vật không đủ. **Không đạt điều kiện đề xuất Chặn.** Hàng (w): một dòng mỗi tấm, số cụm + 8 hộp dài nhất. Bảo vệ thật hiện có: mô hình nhìn `hinh_khoi` (gpt bắt 10 vùng ở B3 l1) + người đọc + lời nhắc bmn-v2b (l2: 0 ống khói thêm trong đáp án).

### KN-5 — LỖI LUẬT (sửa) · chiếu 3D (ii-a) LỖI ẢNH (giữ)
Thước 1.17.5 lấy tỉ số độ sáng TB mỗi nhà → khi bóng quét qua nhà mà AI phân bố lại độ sáng bề mặt, ảnh đúng vật lý vẫn lệch (THU-B tách đúng). 1.17.6: e_h = max_t |trung vị theo điểm lõi nhà của ln(C(t)/C(0)) − ln(R(t)/R(0))|, đọc video ở cỡ gốc. Trên M1 (nắng tắt dần, khung cuối Y ≈ 0,004–0,006 ≈ mã sRGB 12–17) còn 5,8 % nhà lệch ở tỉ số bóng — không do khói bếp (trừ lớp sống: vẫn 25 nhà; diện tích có khói ở nhà lệch 0 %) mà do lượng tử 8 bit ở vùng gần đen (1 mã ≈ 6–8 %) → thêm **sàn Y ≥ 0,01** (điểm dưới sàn ở khung 0 hoặc khung t bỏ khỏi trung vị khung đó). **Sàn chọn trên chính M1** (`do/kn5-san-do-sang.json`; 0 / 0,003 / 0,005 / 0,01 → 5,8 / 4,6 / 3,3 / 1,6 %) — nêu rõ: không có nửa kiểm độc lập trên ảnh thật; selftest có ca tổng hợp "nắng tắt" (không sàn 100 % → có sàn 0 %).
| Khung · cách | 1.17.5 % nhà lệch · nhấp nháy | 1.17.6 % nhà lệch · nhấp nháy | Kết luận |
|---|---|---|---|
| B3 · ảnh tĩnh | 88,2 · 0,0469 | **85,5 · 0,0407** | TRƯỢT (đúng) |
| B3 · tỉ số bóng | 7,2 · đạt | **0,0 · đạt** | **ĐẠT** |
| B3 · chiếu 3D | 15,0 · đạt | **9,4 · đạt** | TRƯỢT — lỗi ảnh |
| M4 · ảnh tĩnh | 57,1 · 0,0455 | **64,3 · 0,0393** | TRƯỢT |
| M4 · tỉ số bóng | 7,1 (1/14) · đạt | **0,0 · đạt** | **ĐẠT** |
| M4 · chiếu 3D | 7,1 · 0,0138 | **7,1 (1/14) · 0,0121** | TRƯỢT — lỗi ảnh (nhấp nháy sát trần) |
| M1 · ảnh tĩnh | 100 · 0,088 | **99,8 · 0,0773** | TRƯỢT |
| M1 · tỉ số bóng | 32,1 · 0,0143 | **1,6 · 0,0119 (sát)** | **ĐẠT** |
| M1 · chiếu 3D | 39,3 · 0,0199 | **26,0 · 0,0178** | TRƯỢT — lỗi ảnh |
Chiếu 3D (ii-a): soi B3 nhà 35893 (2 396 điểm lõi), khung 71: C(t)/C(0) trung vị 1,53 so render 1,27; 36081: 1,64 so 1,38 — bản đồ lệch đỏ đều trên mặt tường (`do/kn5-d-35893.png`) → bản dựng chiếu 3D không dựng lại đúng ánh sáng của render (không phải nhiễu thước). Phía dựng: máy cố định dùng tỉ số bóng (đã khuyến nghị 15:25); máy di chuyển dùng chiếu 3D thì phải sửa shader chiếu (khử sáng/đổ bóng trùng render) trước khi qua (d).
Selftest (cảnh nhà lớn 1080p, video 640×360): albedo AI phân bố lại + bóng quét, dựng đúng → (d)(e) ĐẠT (thước 1.17.5 trên cùng video: 60 % nhà lệch); dán tĩnh → 100 %; nhiễu 8 %/khung → nhấp nháy 0,0211 (TRƯỢT); chồng sáng → (e).

### KN-6 — LỖI LUẬT (sửa)
1.17.5 phóng video 640×360 lên 960×540 rồi so tấm thu 960×540 → mất vân mịn chiếm ngân sách ΔE. 1.17.6 so ở cỡ gốc video (tấm thu INTER_AREA, mặt nạ NEAREST). (`do/kn6-khung0.txt`)
| Khung · cách | 1.17.5 ΔE TB / p95 | 1.17.6 ΔE TB / p95 (640×360) |
|---|---|---|
| B3 · chiếu 3D | 4,63 / 12,59 TRƯỢT | **2,54 / 7,40** |
| B3 · tỉ số bóng | 3,90 / 10,44 | 0,73 / 1,47 |
| M4 · chiếu 3D | 4,79 / 14,68 TRƯỢT | **3,46 / 11,54** (p95 −3,8 % so trần 12) |
| M4 · tỉ số bóng | 2,85 / 9,19 | 0,72 / 1,47 |
| M1 · chiếu 3D | 4,90 / 12,94 TRƯỢT | **2,98 / 8,16** |
| M1 · tỉ số bóng | 3,96 / 10,68 | 0,83 / 2,24 |
Ca trượt giữ: chồng sáng 2 lần (selftest ΔE 8,05/10,29 → (e)).

## 3. Luật đổi / mới (1.17.6)
| Hàng | Tệp | Trường đọc | Ngưỡng | Mức |
|---|---|---|---|---|
| N2P-3 khung không nước (KN-1) | `q_k1175.t9c`, `q_n2p.tong_tam` | như cũ | T9c KHÔNG ÁP khi không lớp nước / nước < 0,2 % khung | như N2P-3 |
| N2P-1 (i) tấm BMN (KN-2) | `q_n2p.do_tam/kiem_tam/tong_tam`, `q_k1176.vung_bmn/nha_do` | `be_mat_nha_ai`, tệp BMN, `be_mat_nha_px_m_min` | (a) 0/255 ngoài nhà đo được nở 1 px; vật mô hình tâm trong vùng → (c) | (a)(b) Chặn G2 · (c) Cảnh báo |
| Gọi lại mô hình nhìn (KN-3) | `q_k1176.goi_claude_du`, `q_k1175.soi_bmn`, `q_n2p_vision.soi` | — | 1 lần gọi lại khi thiếu ảnh | THIẾU nếu cả hai lần thiếu |
| BE-MAT-NHA (w) cạnh màu mới (KN-4) | `q_k1176.canh_moi`, `q_k1175.kiem_bmn` | như BMN | T_A 8, T_O 5 cùng hướng, RAD 2, ≥ 1 m | Cảnh báo (CHỈ BÁO) |
| BE-MAT-NHA (d) (KN-5) | `q_k1176.quy_dao_px`, `frames_video`; `q_k1175.kiem_bmn` | `be_mat_nha_video` | e_h (trung vị theo điểm lõi) > 0,10 ở > 2 % nhà; Y ≥ 0,01; nhấp nháy ≤ 0,012 (giữ) | Chặn G2 · Cảnh báo animatic |
| BE-MAT-NHA (e) (KN-6) | `q_k1176.khung0_de` | `be_mat_nha_video.tam` | ΔE TB ≤ 4, p95 ≤ 12 ở cỡ video | như cũ |
| BE-MAT-NHA ngưỡng nhà đo được | `q_k1176.ppm_min`, `q_k1175.be_mat_nha` | `be_mat_nha_px_m_min` (gốc hoặc `n2p`) | mặc định 2; < 2 → (w) + dùng 2 | (a)(b) như cũ |
| TU-LIEU-10 | `q_k1176.tu_lieu_10`, `q_k1174.check` | `tu_lieu_tran_pct`; log shot `lop`, `tu_lieu_lan` | (a) ≤ trần (mặc định 10, ≤ 15); (b) ≤ 10 s/lần; (k) khai sai | Chặn G2 · Cảnh báo animatic |
| **TU-LIEU-OMNI** (mới) | `q_k1176.tu_lieu_omni`, `cap112`, `k2check` | log shot `minh_hoa`, `lop`, `tu_lieu_lan`, `t0/t1` | (a) không trùng clip M-d; (b) ≥ 1 shot 3D hoặc ≥ 1 s 3D giữa tư liệu và clip M-d | Chặn G2 · Cảnh báo animatic |
| — | `cinecheck/__init__.py`, `ll/RULES-LL.md` (mục 1.17.6), `ll/k2check.py`, `ll/cap112.py`, `ll/selftest_k1176.py` | — | VERSION 1.17.6 | — |

## 4. Cách khai cho phía dựng (tên trường)
- **T4 episode.yaml:** `be_mat_nha_px_m_min: 4` (B chỉ ở nhà ≥ 4 px/m — nhà 2–4 px/m giữ render 0/255); `tu_lieu_tran_pct: 15`.
- **Log shot tư liệu:** `lop: {TL, KHAC, THE, MAP: giây}` như cũ; nên khai `tu_lieu_lan: [{t0, t1, lop}]` (giây tuyệt đối trong phim) cho mỗi lần tư liệu — bắt buộc nếu muốn hoà qua 3D ≥ 1 s TRONG cùng shot trước/sau clip M-d (không khai → lần tư liệu tính phủ cả shot). Clip Omni/M-d: `minh_hoa: true` (shot riêng, không mang lớp tư liệu).
- **BMN video:** giữ `be_mat_nha_video: {ghep, render, cach, tam}`; video kiểm không mất (crf 0 yuv444p) ở cỡ nào cũng được — (d)(e) đọc ở cỡ gốc. Máy cố định: tỉ số bóng (khai `cach: chieu_3d`, `tam`); chiếu 3D trong trình dựng hiện chưa qua (d) — cần sửa ánh sáng chiếu.
- **Mô hình nhìn:** không cần khai thêm; bộ đệm cũ (`n2p-vision-cache.json`, `bmn-vision-cache.json`) dùng lại được (khoá không đổi).

## 5. Tấm THU-B trước/sau (k2check 1.17.5 ↔ 1.17.6, `--cap`)
Khai tối thiểu của THU-B (`kiem/<tên>/episode.yaml`, timeline 3 s/tấm, log shot tối thiểu) — các hàng ngoài tấm (MAY-19, Q26b…) thuộc khai thử, không phải tấm; chỉ tính hàng tấm. "Trước" = `kiem/*/k2check.md` của THU-B (1.17.5, video gốc). "Sau" = 1.17.6 cây đã khoá trên video tái tạo (§1) với bộ đệm mô hình nhìn của THU-B; thêm lượt khai `be_mat_nha_px_m_min: 4` (tấm hiện có, ghép theo ngưỡng 2). Bảng đủ: `do/k2thub/*.md`, tóm tắt `do/thub-truoc-sau.txt`.
| Tấm (l2) | 1.17.5 (THU-B) | 1.17.6 (không khai px/m — mặc định 2) | 1.17.6 khai 4 px/m |
|---|---|---|---|
| **B3 · tỉ số bóng** | N2P-1…6 "không chạy được"; BMN (d) 7,2 % | **qua đủ Chặn**: N2P-1…6 ĐẠT (N2P-1 (c) 4 người đọc), BMN 0 Chặn, (w) 2 | TRƯỢT (b) 153/255 ở 24 790 điểm + N2P-1 (a): AI ở nhà 2–4 px/m (84 nhà đo được còn lại) |
| B3 · chiếu 3D | không chạy; (d) 15,0 %, (e) 4,6/12,6 | TRƯỢT (d) 9,4 % (lỗi ảnh); (e) ĐẠT | TRƯỢT (b)(d) |
| B3 · ảnh tĩnh | không chạy; (d) | TRƯỢT (d) 85,5 % + nhấp nháy | TRƯỢT |
| **M4 · tỉ số bóng** | không chạy; (d) 7,1 % | **qua đủ Chặn** (N2P ĐẠT; BMN (w) 1) | TRƯỢT (b) 106/255 ở 4 115 điểm (13/34 nhà đo được) |
| M4 · chiếu 3D | không chạy; (d) 7,1 % + 0,0138, (e) 4,8/14,7 | TRƯỢT (d) 7,1 % + nhấp nháy 0,0121; (e) ĐẠT | TRƯỢT |
| M4 · ảnh tĩnh | không chạy; (d) | TRƯỢT (d) 64,3 % | TRƯỢT |
| **M1 · tỉ số bóng** (đối chứng) | N2P-1 (a) 218/255; (d) 32,1 % + 0,0143 | **qua đủ Chặn** (N2P-1 (a) 0; BMN (d) 1,6 %, nhấp nháy 0,0119 — sát trần); (w) 3 | TRƯỢT (b) 183/255 ở 162 166 điểm (72/8 510 nhà đo được) + (d) nhấp nháy 0,0133 (*) |
| M1 · chiếu 3D | (a) + (d) 39,3 % + (e) 4,9/12,9 | TRƯỢT (d) 26,0 % (lỗi ảnh); (e) ĐẠT | TRƯỢT |
| M1 · ảnh tĩnh | (a) + (d) 100 % | TRƯỢT (d) | TRƯỢT |
**Điều kiện (2) §15 (j) — tấm qua đủ cổng (k2check, không tính (w) người đọc):** ở ngưỡng hiện khai (2 px/m): **B3, M4, M1 cách tỉ số bóng** qua đủ hàng Chặn; chiếu 3D trong trình dựng và ảnh tĩnh không qua. Với khai 4 px/m (quyết định 15:25) **chưa tấm nào qua** — vì tấm THU-B ghép AI cả ở nhà 2–4 px/m; phía dựng phải ghép lại chỉ ở nhà ≥ 4 px/m (khi đó (b) = 0 theo định nghĩa; (d) đo lại).
(*) M1 nhấp nháy: không do khói bếp (trừ lớp sống: 0,0133 giữ nguyên) mà do khung nắng tắt gần đen — thước nhấp nháy (giữ nguyên 1.17.5) chưa có sàn Y: với sàn Y 0,01 → 0,0084 (≥ 2 px/m) / 0,0093 (≥ 4 px/m); nửa cuối clip 0,0147 → 0,0103 (`do/m1-nhap-nhay-khoi.txt`). Khiếm khuyết còn lại của thước → **K1176-D6** (mã đã khoá một lần, không sửa trong phiên).

## 6. Selftest
- `checks/ll/selftest_k1176.py` **62/62** (không mạng/API, không fixtures ngoài; ≈ 45 s): KN-1 7 (khung không nước, nước < 0,2 %, AI vẽ nước lên đất vẫn bắt, trộn tấm có bờ lấn vẫn trượt) · KN-2 9 (gồm 3 ca mô hình qua `kiem_tam`) · px/m 5 (gồm ca nhà 3 px/m khi khai 4) · KN-4 3 · KN-3 7 (mô hình giả lập) · KN-5/KN-6 9 (albedo phân bố lại + bóng quét; video 640×360 + tấm 1080p; sàn Y nắng tắt) · TU-LIEU-10/OMNI 17 (gồm tư liệu chồng M-d, ghép liền, hoà 1,5 s / 0,5 s, khai 20 %) · cấp 4 · áp dụng 1. Mỗi luật đổi/mới ≥ 1 ca đạt + ≥ 1 ca trượt.
- Selftest cũ trên cây ĐÃ KHOÁ (`do/selftest-sau-khoa.txt`): k112 75/75 · k1121 48/48 · k1122 37/37 · k113 64/64 · k114 126/126 · k115 105/105 · k116 144/144 · k117 130/130 · k1172 74/74 · k1173 42/42 · k1174 91/91 · k1175 52/52 · **k1176 62/62** · k2 129/129 · ll 317/317 — 0 SAI. **0 kỳ vọng cũ đổi** (k1175 52/52 giữ với (d) theo điểm ảnh, (e) độ phân giải video).
- Lượt trước khoá (`do/selftest-truoc-khoa.txt`) cũng đạt hết; sau lượt đó chỉ sửa `q_n2p` (vật mô hình trong vùng BMN) → chạy lại k117 130/130, k1175 52/52, k1176 62/62 trước khoá.

## 7. LOCK
Cũ 1.17.5 `c7630b4a6b8f4f8e7a2bcfc593b59e35df76e21ab404b0d532c595c2d06ea10a` → **mới 1.17.6 `513c9442fe1cb9950bdf01c3be4dc93b32c4413d9260109c86f0f5d90e5b8ec3`** (DATE_UTC 2026-10-24T10:26:29Z); `python3 -I checks/lock.py` không cờ: đúng một lần; `--verify` KHỚP (ngay sau khoá, mọi commit/push, hàng LOCK k2check). Tệp đổi: `LOCK`, `cinecheck/__init__.py`, `ll/RULES-LL.md`, `ll/cap112.py`, `ll/k2check.py`, `ll/q_k1174.py`, `ll/q_k1175.py`, `ll/q_n2p.py`, `ll/q_n2p_vision.py`; mới `ll/q_k1176.py`, `ll/selftest_k1176.py`.

## 9. So k2check 1.17.5 ↔ 1.17.6 trên bản cuối T3
Đầu vào như K-1.17.5 §9: `git archive origin/main channel-k2/k2c-t3-01 reports/animatic-t3-v2 reports/k1172/do reports/k1173/do AUTHORSHIP.md RIGHTS.md docs` vào thư mục tạm (khởi tạo git cục bộ — Q32 đọc cây git; lượt đầu thiếu git làm Q32 khác, đã chạy lại), timeline tổng hợp `mk_tl.py` (761,9998 s), log chữ `mk_log_chu.py` (1 524 khung mẫu), master LFS `release-k2-t3-g2` (UA CineLab-research, SHA-256 `5b9f0bcc…` khớp). Lệnh: `k2check.py …/cuoi/episode-k.yaml --tl timeline.json --master k2-t3-v1-master.mp4 --cap --no-asr`. 1.17.5 chạy từ cây origin/main (LOCK 1.17.5 KHỚP) — **trùng hệt bảng K-1.17.5** (`reports/k1175/do/k2check-1.17.5-t3.md`) trừ tiêu đề. Bảng đủ: `do/k2check-1.17.5-t3.md`, `do/k2check-1.17.6-t3.md`.
| Hàng | 1.17.5 | 1.17.6 | Lý do |
|---|---|---|---|
| 56 hàng (Q26b … Q37, A1–A13, NHIP-K2, BIEN-CO-V, N2P-1…6 "KHÔNG ÁP", MINH-HOA, EO-DAT-R1…R4, 1.17.4 (T4), 1.17.5 (T4)) | — | **giống hệt** (kết quả + giá trị + danh sách lỗi) | luật 1.17.6 chỉ tập từ T4; TU-LIEU-OMNI gộp trong hàng "1.17.4 (T4) KHÔNG ÁP" |
| LOCK | KHỚP (1.17.5) | KHỚP (1.17.6) | chỉ nhãn phiên bản |
Mã thoát cả hai: 1 (TRƯỢT như K-1.17.5 — Q37 (a)(c)(d), EO-DAT-R3 (a), XEM-CAM, K-LAI-2 (d), BIEN-CO-V). **Ngoài hàng LOCK: không hàng nào đổi** (không có hàng đổi theo phán quyết vì T3 không áp luật T4).

## 10. Chỉ số trong ±5 % quanh ngưỡng (luật cứng — nêu tên)
- **M1 tỉ số bóng nhấp nháy 0,0119 so trần 0,012 (−0,8 %)** (ĐẠT sát; khai 4 px/m: 0,0133, +10,8 % — K1176-D6).
- **M4 chiếu 3D nhấp nháy 0,0121 so trần 0,012 (+0,8 %)** (giữ thước 1.17.5; TRƯỢT sát).
- **M4 chiếu 3D (e) p95 11,54 so trần 12 (−3,8 %)** (ĐẠT sát).
- Selftest tổng hợp: ca dựng đúng nhấp nháy 0,0118 so 0,012 (−1,7 %) — dữ liệu tổng hợp.
- Xa ngưỡng (ghi để rõ): M1 tỉ số bóng 1,6 % so trần 2 % (−19 %; phụ thuộc sàn Y chọn trên chính M1 — xem KN-5).

## 11. Chi phí thật
| Khoản | Số |
|---|---|
| Claude API | **$0,1199** = claude-sonnet-5-5 (claude -p) 2 lần nhìn BMN (KN-3) |
| OpenAI | **$0,0798** = gpt-6.1-sol 2 lần nhìn BMN (KN-3) |
| Gemini / ElevenLabs / RunPod / YouTube | 0 |
| Giờ máy | ≈ 3,0 h đồng hồ container (08:20 → ≈ 11:20 UTC): dựng lại dữ liệu nền 9 phút; 9 lượt dựng timelapse three.js (≈ 6,5–9 phút/lượt) ≈ 65 phút; selftest 2 lượt toàn bộ ≈ 18 phút; k2check T3 3 lượt ≈ 36 phút; k2check THU-B 6 lượt; lưới KN-4 ≈ 25 phút |
| Băng thông | master T3 1,79 GB (LFS `release-k2-t3-g2`, SHA `5b9f0bcc…` khớp); OSM/LiDAR/vân CC0 ≈ 0,2 GB (dựng lại dữ liệu nền) |
| Token phiên chính | không đo được từ container |
| Sổ AI | `reports/k1176/so-ai.jsonl` (4 dòng: model, lời nhắc mẫu + tham số, SHA vào/ra, usage, giá) |

## 12. Quyết định đề xuất (chủ dự án)
| # | Đề xuất | Phương án | Ưu | Nhược | Tác động | Rủi ro | Khuyến nghị |
|---|---|---|---|---|---|---|---|
| **K1176-D1** | Duyệt luật 1.17.6 (KN-1, KN-2, KN-5, KN-6 sửa; KN-3 gọi lại) | A: duyệt. B: giữ 1.17.5 | A: tấm BMN đúng (tỉ số bóng) qua (d)(e); N2P chạy được trên khung không nước. B: không đổi | A: sàn Y chọn trên M1 (chưa có nửa kiểm thật). B: mọi tấm BMN trượt oan | T4 G2 | A thấp: ảnh tĩnh vẫn trượt 64–100 %, chiếu 3D sai vẫn trượt | **A** |
| **K1176-D2** | KN-4 (w) cạnh màu mới | A: CHỈ BÁO (w) như đã khoá. B: Chặn | A: không chặn oan cửa sổ AI lệch. B: chặn ống khói thêm | A: ống khói thêm chỉ người đọc + mô hình nhìn bắt (bắt 15/20). B: 23 cụm báo nhầm trên tấm sạch, 5/20 vẫn lọt | B3/T4 tấm BMN | A: ống khói thêm lọt nếu người đọc bỏ sót | **A** + bắt buộc soi các hộp (w) trên tờ so + lời nhắc bmn-v2b |
| **K1176-D3** | Cách chiếu B khi máy di chuyển (chiếu 3D trong trình dựng chưa qua (d): tường sáng lên ~20 % hơn render) | A: phía dựng sửa shader chiếu (khử sáng + đổ bóng trùng render) rồi đo lại. B: hạn chế B ở shot máy cố định (tỉ số bóng). C: nới (d) cho chiếu 3D | A: giữ phương án 15:25. B: chắc chắn qua. C: nhanh | A: thêm một vòng dựng. B: mất B ở shot máy di chuyển. C: trái nguyên tắc chất lượng | T4 shot máy di chuyển có B | C: bề mặt "dán" lộ khi nắng đổi | **A, tạm B** đến khi A qua (d) |
| **K1176-D4** | TU-LIEU-OMNI + (b) ≤ 10 s áp cho mọi tập từ T4 (không chỉ khi khai 15 %) | A: mọi tập từ T4 (như đã khoá). B: chỉ tập khai `tu_lieu_tran_pct` > 10 | A: một quy tắc kết hợp tư liệu thống nhất. B: hẹp đúng chữ ngoại lệ T4 | A: ràng buộc thêm cho tập sau T4. B: tập sau có thể ghép liền | T4+ | thấp | **A** (đúng ý "cách kết hợp tư liệu" 12:52); Kinh thánh §19 (c) ghi kèm |
| **K1176-D6** | Thước nhấp nháy (d) chưa có sàn Y (M1 tỉ số bóng 0,0119 ở 2 px/m, 0,0133 ở 4 px/m; có sàn 0,0084 / 0,0093) | A: mở phiên K-1.17.7 ngắn thêm sàn Y 0,01 cho nhấp nháy (cùng sàn (d)) + selftest. B: giữ, phía dựng tránh khung gần đen. C: phía dựng ghép lại B ≥ 4 px/m trước, K đo lại rồi quyết | A: shot cuối ngày dựng đúng không trượt oan. B: không đổi luật | A: thêm một lần khoá. B: shot hoàng hôn khó qua | T4 shot nắng tắt có B | A thấp (ảnh tĩnh nhấp nháy 0,04–0,08, xa trần) | **A**, làm cùng lượt đo lại tấm ghép ≥ 4 px/m |
| **K1176-D5** | Sàn Y ≥ 0,01 cho (d) | A: duyệt (đã khoá). B: bỏ sàn, phía dựng tránh khung gần đen | A: M1 nắng tắt qua. B: thước thuần hơn | A: điểm dưới sàn không được kiểm (vùng gần đen, mắt khó thấy). B: shot hoàng hôn khó qua | shot cuối ngày | A thấp | **A** + K đo lại trên shot hoàng hôn thật đầu tiên của T4 |

## 13. Dòng sổ đề xuất (P ghi — phiên này không sửa sổ)
- **COST-LEDGER:** 24/10 K-1.17.6 — Claude API $0,1199 (2 lần nhìn BMN), OpenAI $0,0798 (2 lần nhìn BMN), Gemini $0, giờ máy ≈ 3,0 h, tải LFS 1,79 GB.
- **AUTHORSHIP:** ghi khi chủ dự án trả lời K1176-D1…D5 (nguyên văn + giờ). Căn cứ đã có: 24/10 12:52 "Duyệt cách kết hợp tư liệu theo khuyến nghị"; 24/10 15:25 phiếu THU-B "theo khuyến nghị".
- **RIGHTS:** không tài sản mới (không ảnh AI mới; 4 lần mô hình nhìn chỉ đọc ảnh của ta).
- **Kinh thánh (P):** §19 (c) ngoại lệ T4 15 % + "tư liệu chỉ chồng shot 3D, không chồng/ghép liền clip Omni, mỗi lần ≤ 10 s" (khoá ở TU-LIEU-10/OMNI); §15 (j) B ≥ 4 px/m (`be_mat_nha_px_m_min: 4`).
- **BAI-HOC-K2 (đề xuất):** (1) `pgrep -f "<chuỗi>"` trong vòng chờ khớp chính dòng lệnh chờ — LẶP lần 4: chờ theo PID cụ thể (`kill -0`); (2) `git worktree add` cả repo tốn ≈ 6 GB — tái tạo bằng `git archive` thư mục cần; (3) video kiểm ngoài git tái tạo được trùng SHA khi dữ liệu nền trùng (`ldn2.bin`) — giữ `video-sha.json` + lệnh tái tạo là đủ; (4) cảnh tổng hợp cho thước ánh sáng phải dựng trong không gian tuyến tính rồi mã sRGB, tránh bão hoà; (5) thước quỹ đạo sáng cần sàn độ sáng — khung gần đen chỉ còn lượng tử 8 bit.

## 14. Việc chờ chủ dự án
1. Trả lời **K1176-D1…D5** (§12) — khuyến nghị: D1 A, D2 A, D3 A (tạm B), D4 A, D5 A, D6 A.
2. Phiên P: merge `checks-1-17-6` khi duyệt (nhánh này **không** merge); ghi sổ theo §13; ghi Kinh thánh §19 (c) ngoại lệ T4 và §15 (j) B ≥ 4 px/m.
3. (Nếu D6 = A) một phiên K-1.17.7 ngắn: sàn Y cho nhấp nháy, đo lại tấm ghép ≥ 4 px/m.
4. Phía dựng T4: khai `be_mat_nha_px_m_min: 4`, `tu_lieu_tran_pct: 15`, `tu_lieu_lan`; tấm BMN ghép lại chỉ ở nhà ≥ 4 px/m (B1/B3 hiện phủ cả nhà 2–4 px/m → trượt (b) khi khai 4, §5); sửa chiếu 3D (D3).
