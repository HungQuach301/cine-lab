**Nhánh thật: `checks-1-17`** (đúng lệnh; harness gợi ý `claude/focused-hamilton-i3ss8i` nhưng đẩy `checks-1-17` được chấp nhận). Gốc `origin/main` @ `bc7e96d1`. Không merge, không đụng `main` hay nhánh khác.

# Phiên K-1.17 — bộ kiểm N2+ (§15, T4), minh hoạ (§14.1 (c) / M-d), eo đất R1–R3 (§14.7), V7C-D5, 8 hàng Chặn animatic T3 — BÁO CÁO

> Phiên K, 21/10/2026 ≈ 14:20–15:15 UTC. Mọi số là số đo thật trong phiên; tệp số đo ở `reports/k117/do/`.
> Email chủ dự án không có trong tệp, commit, header, URL, payload hay User-Agent nào (UA cố định `CineLab-research (+https://github.com/HungQuach301/cine-lab)`). Không in/ghi khoá (OpenAI do proxy gắn; Claude qua `CONSOLE_API_KEY` trong môi trường tiến trình con của `judge.call`).

## 0. Khối điều lệ và tóm tắt
| Trường | Lệnh | Thực tế |
|---|---|---|
| Loại phiên | K-1.17 | đúng |
| Nhánh | `checks-1-17` từ `origin/main` | đúng (`bc7e96d1`) |
| Vùng sửa | `checks/**`, `reports/k117/**` | đúng (§12). Không sửa `docs/`, `design/`, `scripts/`, `channel-*/`, sổ |
| Chi phí | Claude mốc $5; OpenAI + Claude nhìn chỉ cho selftest ≤ $3; chặn Claude > $15 | nhìn + O2 **$0,369** (OpenAI $0,078 + Claude API $0,291); token phiên chính không đo được từ container (§7) |
| ElevenLabs / Gemini / RunPod / YouTube | 0 | **0 / 0 / 0 / 0** |
| `lock.py` (không cờ) | một lần ở cuối, sau khi selftest đạt | **đúng một lần**, 15:01:40 UTC → 1.17.0; mọi lần khác chỉ `--verify` |
| Preflight | bắt buộc | hook pre-commit + pre-push (bọc LFS) cài đầu phiên; mọi commit + push **PREFLIGHT ĐẠT**; checkpoint việc dở: cất `checks/` bằng `git stash`, đẩy bản vá trong `reports/k117/wip/` (đã gỡ khi commit mã) |
| Việc dở | đẩy ≤ 30 phút + CHECKPOINT | 3 lần đẩy (14:35, 14:47, 15:04) + commit cuối, `reports/k117/CHECKPOINT.md` |
| Force / dừng hỏi | không | không force; không dừng hỏi |

**Tóm tắt:**
1. **N2+ vào `checks/`** (chỉ tập từ T4): `q_n2p.py` (máy + kết luận, 6 hàng N2P-1…6), `q_n2p_vision.py` (2 mô hình nhìn, **mặc định tắt**, cờ `--n2p-vision`), `data/cam_thoi_dai.json` (nguyên văn NC-N2P, SHA `3f5576e4…`). Kiểm có đáp án: **bản lưu NC-N2P và lượt thật 21/10 đều gpt 6/6, claude 6/6, hợp 6/6, q_thoi_dai 3/3; đối chứng 0 báo**.
2. **MINH-HOA** (T3 theo N2, T4 theo M-d) và **EO-DAT-R1…R3** (từ T3) vào `q_k117.py`. Mức: Chặn ở G2, Cảnh báo ở animatic. **R4: lệnh và repo không có định nghĩa → chưa viết luật.**
3. **Kinh thánh §14.7 và §15 không có trên nhánh nào** (đã quét mọi nhánh `origin` lúc 14:30). Luật lấy nội dung theo lệnh; **ngưỡng R1, R2 là K đề xuất tạm** (§2.3), chờ chủ dự án chốt.
4. **8 hàng Chặn animatic T3**: **3 lỗi luật** (Q33 ×3 hàng, ML1, NC-H1 phần lớn) — khiếu nại chấp nhận, đã sửa + selftest; **5 lỗi phim/khai** (Q37 nhịp, Q37 (a) khai beats lời, A11, SACH-1 thiếu log chữ, XEM-CAM chờ chấm) — ghi danh sách cho bản cuối (§4).
5. **V7C-D5**: NC-H1 nay nhận `opt.bfile` / `cityOpt` / `pre1704town` / `pho2026` / `lop_nha`; SACH-1 dùng `log_chu` (đã có từ 1.16, luật đúng) (§3).
6. **Selftest**: k117 **96/96** (+ 8/8 lượt API thật); cũ đều đúng kỳ vọng trên cây đã khoá. `k2check` T1 **31/31**, T2 **49/49** hàng giống hệt 1.16.1 (chỉ đổi tên phiên bản ở hàng LOCK).
7. **LOCK 1.16.1 `a3c39873…` → 1.17.0 `f6812dec…`**, `--verify` KHỚP.

## 1. Đầu vào đã đọc
- `reports/NC-N2P-BAO-CAO.md` §2, §6 + `reports/nc-n2p/ma/` (`kiem_n2p.py`, `vision_kiem.py`, `cam_thoi_dai.json`, `cham_dap_an.py`, `n2p_lib.py`) + `reports/nc-n2p/kiem/dap-an/` (nhánh `origin/nc-n2p` @ `9cb001d1`).
- `reports/animatic-t3/ANIMATIC-BAO-CAO.md` §8.3, `do/k2check-1.16.1.txt`, `channel-k2/k2c-t3-01/animatic/{episode.yaml, log-shot.json}`, 8 tệp xem (nhánh `origin/ccr-d189108f-6mcz9k` @ `41e0c8fd`; worktree thưa ngoài repo `/var/tmp/k117-anim`).
- `reports/v7c/V7C-BAO-CAO.md` (V7C-D5, dòng 252); `checks/ll/RULES-LL.md` 1.16.1; `docs/BIBLE-KENH2.md` §13.6, §14.1 (main).
- **Không có:** Kinh thánh §14.7 (R1–R4 eo đất) và §15 (N2+, M-d) — không nhánh nào chứa (có lẽ phiên P-2110 đang viết). §15 dùng nháp NC-N2P §6.3 + số trong lệnh.

## 2. Luật mới (1.17.0) — tên, trường đọc, ngưỡng, mức, nguồn
Bật: N2P chỉ khi episode.yaml khai `kenh2_tu_t4: true` hoặc khối `n2p:`; MINH-HOA/EO-DAT khi tập từ T3 (`khung_sach` | `kenh2_tu_t3`, như 1.16). **Tập trước T3: không thêm hàng nào.** Tập T3: 1 hàng gộp "N2P-1…6 KHÔNG ÁP".
Mức (cap112, áp với `--cap`): mọi hàng mới **Chặn ở cổng G2 · Cảnh báo ở animatic** (`animatic: true`; không khai → G2), cùng cơ chế K116-D5 (tổng quát hoá bằng tập `CONG`; K-LAI-3V giữ nguyên, có selftest).

### 2.1 N2+ — `q_n2p.py`, `q_n2p_vision.py` (nguồn: Kinh thánh §15 nháp NC-N2P §6.3 (a)–(d); số trần theo lệnh K-1.17)
| Hàng | Trường đọc | Đo / ngưỡng | Mức |
|---|---|---|---|
| **N2P-1** (i) lớp (a) | `n2p.tam[]`: `render`, `ghep` (PNG), `mat_na` (bảng màu V7C), `lop_a?`, `bang?` | (a) max \|ghép − render\| trong mặt nạ (a) = **0/255**; (b) **0** vật loại (a) (cờ, công trình, công sự, tàu lớn, chữ, đèn, lửa lớn) THÊM/BỚT/ĐỔI theo ≥ 1 mô hình (tin ≥ 0,5); (c) cụm ΔE76 ≥ 30 ≥ 80 px trong **dải 20 px** quanh (a) (px quy về 1080p) | (a)(b) Chặn G2 / Cảnh báo animatic; **(c) luôn Cảnh báo** (người đọc tờ so) |
| **N2P-2** (ii) thời đại | trả lời 2 mô hình + `cam_thoi_dai.json` + `q_thoi_dai.py` | (a) **0** vật có năm xuất hiện > năm khung (hoặc máy bay/xe máy ở cảnh < 1900) ở ≥ 1 mô hình; "không năm" → ghi, không lỗi; (b) O2 trên khung ghép **trừ nghi vấn trùng nghi vấn của chính render** = 0 | Chặn G2 / Cảnh báo animatic |
| **N2P-3** (iii) đổi vùng | mặt nạ + ảnh | (a) **T9b ≤ 2 %** mỗi chiều; (b) 0 báo đổi đất↔nước | như trên |
| **N2P-4** (iv) đóng băng | `anh_tinh` (mặc định true) | **0** vật chuyển động THÊM (người, động vật, chim, thuyền nhỏ, xe chạy, khói, lửa trại, máy bay, xe máy) | như trên |
| **N2P-5** (v) nhấp nháy + chuyển tấm | `n2p.video[]` {ghep, render đối chứng, mat_na, chuyen_tam [{t, kieu, dur}]} hoặc log `ai_nen.chuyen_tam` | (a) chỉ **hoà ≥ 2 s**; (b) max bước khung của ΔE76 TB trên lớp (c) **≤ 1,0 ΔE/khung**; (c) nhấp nháy \|Δ xám\|/khung trên (c) ngoài cửa sổ hoà **≤ max(1,5 × đối chứng, sàn 0,02)** | như trên |
| **N2P-6** (vi) trần §15(d) | log shot `ai_nen`, `minh_hoa`, `ai_image`, `ai_texture`, `dur` | tấm nền **≤ 50 %** · minh hoạ (M-d) **≤ 20 %** · tổng AI **≤ 70 %** · **0** shot vừa ai_nen vừa minh_hoa | như trên |
- **Tên trường đề xuất (lệnh):** `ai_nen` (bool hoặc `{tam: [id], chuyen_tam: [...]}`) và `minh_hoa` (bool) trong log shot — đã dùng đúng hai tên này.
- **Gọi mô hình nhìn:** chỉ khi `k2check --n2p-vision` (hoặc `q_n2p.py --vision`). Không cờ → đọc bộ đệm `<out>/n2p-vision-cache.json` (khoá = SHA ảnh trước + sau + năm + nơi + t4 + đề bài + hai mô hình); chưa soi → N2P-1 (b) THIẾU = Chặn ở G2. **Chi phí đo 21/10: 2 mô hình $0,097–0,117/khung** (GPT $0,033–0,045 + Claude $0,064–0,072) **+ O2 ghép + render ≈ $0,078/khung**.
- **Giới hạn đã biết (ghi trong mã và RULES-LL):** cờ ~20–25 px @1080 — q_thoi_dai không đọc được mẫu (NC-N2P: báo cờ 1707 của render là 1801). Cờ thuộc lớp (a) nên được bảo vệ bằng (i) 0/255. Đối chứng render ở (ii)(b) loại đúng kiểu báo nhầm này. Số vật mô hình báo thay đổi giữa các lần chạy (lượt thật 21/10: gpt báo thêm 1 "chữ" so với bản lưu). Người đọc tờ so vẫn bắt buộc (§15 (c)).
- **Khác với mã NC-N2P:** chỉ đo, không ghép (ghép là việc phía dựng). Px ngưỡng quy theo chiều cao khung. Claude gọi qua `judge.call` (`--bare --restricted`, chỉ Read, kiểm đọc đủ 10 ảnh, kiểm mô hình ghim). Thêm đối chứng render cho O2. Thêm (v) đo trên video và (vi) trần.

### 2.2 MINH-HOA — `q_k117.minh_hoa` (nguồn: Kinh thánh §14.1 (c) N2; §15 M-d; lệnh K-1.17)
| Mục | Trường đọc | Ngưỡng |
|---|---|---|
| (a) | log shot `minh_hoa: true`, `dur` / `t0`–`t1` | tổng **≤ 20 %** thời lượng |
| (b) | log chữ (`log_chu` / `--logs`) có chữ "Illustration" ở **mọi** khung mẫu của shot; hoặc log shot `nhan_minh_hoa: "Illustration"` + `nhan_t: [t0, t1]` (không có = cả shot) | nhãn suốt đoạn; không có cả hai → THIẾU (chưa có OCR trong môi trường — giới hạn đã biết) |
| (c) | `goc` shot liền trước/sau | kẹp giữa **hai shot 3D** (cao/thap/neo, không minh hoạ) |
| (d) | `agl_m` (nếu có) | **≤ 40 m AGL** |
| (e) | log shot `so_ai` hoặc tệp `so_ai:` (jsonl, `shot` = id đoạn) | ≥ 1 dòng có `model` + lệnh (`lenh`/`prompt`/`lenh_sha`/`prompt_sha`) + SHA ra (`sha_ra`/`sha_out`/`sha256`) |
Kèm SACH-1: chữ "Illustration" trong shot minh hoạ không còn là lỗi (e) (§14.1 (c): ngoại lệ của §12.1); ngoài shot minh hoạ vẫn là lỗi.

### 2.3 EO-DAT R1–R3 — `q_k117.eo_dat` (nguồn: Kinh thánh §14.7 theo lệnh; shot `noi: eo_dat`)
| Hàng | Trường đọc | Ngưỡng | Ghi chú nguồn ngưỡng |
|---|---|---|---|
| **EO-DAT-R1** | `chu_the_eo_dat: true` + `chu_the_pct` (số TB shot hoặc `[[t, %], …]` từ mặt nạ ID) | trung vị **≥ 25 %** khung | **K đề xuất tạm** (cùng mức NC-H1 fabric ≥ 25 %) |
| **EO-DAT-R2** | `trong_pct` (số TB shot hoặc **trường mới đề xuất** `[[t, %], …]` theo khung mẫu từ mặt nạ ID); "trống" = **> 60 %** | (a) trống liên tục **≤ 6 s** (nối qua ranh shot); (b) mỗi chương: thời lượng eo đất trống **≤ 1/3** thời lượng eo đất | 60 % = TL-3 (đã duyệt K116-D1); **6 s và 1/3 là K đề xuất tạm** (cùng trần biến cố Q37/R3 và BC2) |
| **EO-DAT-R3** | `so_goc` (số) hoặc `goc_may` (danh sách); `su_kien[].t`, `tl_buoc[].t` | shot > **15 s**: (a) **≥ 2 góc**; (b) khoảng giữa biến cố (tính đầu/cuối shot) **≤ 6 s** | theo lệnh. Biến cố là **số tự khai trong log** — sẽ thay bằng biến cố đo khi làm K116-D4 |
| R4 | — | — | **không có định nghĩa** trong lệnh và repo → chưa viết |

## 3. V7C-D5 — tên trường khai
| Hàng | Câu hỏi V7C | Trả lời K |
|---|---|---|
| **NC-H1** "lớp nhà khai 0" ở cảnh `tl/*` | Tên trường? | **Luật sai — đã sửa (chỉ tập từ T3).** `layer_of` 1.16.1 chỉ nhận `aerial/city/buildings/ghost/fabric`. Cảnh `tl/*` nạp nhà qua `opt.bfile` (`design/k2v/tl/page.js` dòng 54: `cfg.opt.bfile`) + `opt.cityOpt`. 1.17 nhận: **`heroes.<k>.opt.bfile`**, `cityOpt`, `pre1704town`, `pho2026`, hoặc trường chung **`lop_nha: "<mô tả>"`** (shot `p` hoặc `opt`). Không có mặt nạ fabric → "khai, không đo fabric" (THIẾU số đo, Cảnh báo như 1.13) |
| **SACH-1** "không log chữ" | Tên trường? | **Luật đúng — không sửa.** Trường đã có từ 1.16: **`log_chu: <tệp>`** ở gốc episode.yaml, dạng `[{f: <khung phim>, items: [{role, s, alpha?, px1080 \| cap, box?}]}]` (hoặc `--logs` log k2.js). Vai hợp lệ: `year`, `clock`, `calendar`, `where`, `the_chuong`, `the_phuong_phap` (+ `minh_hoa` trong shot minh hoạ từ 1.17). Không có log → SACH-1 (c)(d) THIẾU = Chặn: số đo thật thay số khai |

## 4. 8 hàng Chặn animatic T3 — phân loại
Tái hiện: timeline dựng lại từ đặc tả (`do/tl_tu_dac_ta.py`; timeline thật ngoài git); video = 8 tệp xem 640×360 ghép (761,15 s) thay master 960×540. **1.16.1 tái hiện đủ 11 hàng TRƯỢT của báo cáo animatic** (Q33 bộ pHash ra cặp lặp hơi khác vì bản xem nhỏ hơn, cùng bản chất) — `do/k2check-t3-1161-tai-hien.md`, `do/q33-t3-1161.txt`. Chạy 1.17.0 đã khoá: `do/k2check-t3-1170.md`, `do/q33-t3-117.txt`.

| # | Hàng (k2check) | Lỗi animatic (1.16.1) | Phân loại | Lý do | 1.17.0 trên cùng đầu vào |
|---|---|---|---|---|---|
| 1 | **Q33, Q33-K2, Q33 (1.13)** | 3 góc "> 2 lần" (N4_1, C1, C2 …; cùng điểm máy D ở năm khác) | **LỖI LUẬT — chấp nhận** | Kinh thánh §13.6 TL-1 (duyệt 19/10): *"mỗi phần phim quay lại cùng điểm máy ở năm khác"*, 6–8 điểm máy cả tập ⇒ "≤ 2 lần" mâu thuẫn. Miễn của Q33-K2 cần năm trong đặc tả, cảnh `tl/*` chỉ có năm ở log shot. **Sửa:** lần ở đoạn khác, khoảng năm log `nam` không chồng MỌI lần trước → miễn; cùng năm/cùng đoạn/không log năm vẫn đếm | **ĐẠT cả 3** (miễn 16 / 10 / 10) |
| 2 | **Q37, NHIP-K2, Q37 (1.13)** (b)(c) | TB 5,21 s > 3,5; dài nhất 12,71 s > 6 | **LỖI PHIM** | Nhịp thưa thật. Kể cả cộng biến cố log (`su_kien`, `tl_buoc`) và bỏ beats lời: 160 biến cố, TB 4,76 s, dài nhất 25,5 s, **52 khoảng > 6 s**. R3 (§14.7) xác nhận lại trần 6 s | không đổi (TRƯỢT) |
| 3 | **Q37 (a)** (cùng 3 hàng) | 101 beats `k: loi` "không khớp mốc" | **LỖI KHAI PHIM** | `beats` là biến cố HÌNH; mốc câu lời không phải biến cố hình (và làm phồng số biến cố: 146 = 45 cắt + 101 lời). Luật đúng | không đổi |
| 4 | **A1–A13** (A11) | `mix.json` không có `nhac[]` | **LỖI PHIM/KHAI** | Trộn bằng `anim_mix.py` không ghi nhật ký giao nhạc. Animatic phải khai **`animatic: true`** (K116-D9 mục 6) → A* chỉ báo; bản cuối trộn qua chuỗi có `nhac[]`. Không tái hiện được (mix.json ngoài git) — theo số của báo cáo animatic | — |
| 5 | **ML1** | KB1943, KA2026 `cau ''` "không khớp" | **LỖI LUẬT — chấp nhận** | `cau: ""` nghĩa là không gắn câu (tấm im lặng — §14.6 KA2026, §11.2); chuỗi rỗng không thể khớp câu nào. **Sửa:** rỗng = không khai; shot vẫn tính (b) trôi (4,2 % < 15 %) | **ĐẠT** |
| 6 | **NC-H1** | 16 shot "không lớp nhà" | **LỖI LUẬT (14) + LỖI KHAI (2)** | §3: `opt.bfile`/`cityOpt` không được nhận. Sau sửa còn **C3, C5** (`noi: thanh_pho`, không `bfile`/`lop_nha`) | **2 Chặn** (C3, C5) |
| 7 | **SACH-1** | "không log chữ" | **LỖI PHIM** | Luật đúng (§3); phiên dựng chưa xuất `log_chu` | không đổi |
| 8 | **XEM-CAM** | thiếu điểm chủ dự án | **PHIM/QUY TRÌNH — chờ dữ liệu** | Cổng §13.4 cần chủ dự án chấm tắt tiếng; không phải lỗi luật | không đổi |

**Danh sách cho phiên bản cuối (không sửa phim trong phiên này):**
- **F1** Q37/R3: thêm biến cố thấy được (≤ 6 s) hoặc góc thứ hai trong 13 shot eo đất > 15 s (N1_5 25,5 s · N4_2 25,4 s · N4_1 21,2 s · N5_1 16,8 s · N5_4 16,3 s · N3_4 15,0 s · N1_6 14,5 s · N3_1 13,8 s · C1 13,5 s · N2_11 13,5 s · N4_5 10,8 s · N2_10 10,2 s · N5_6 6,7 s khoảng dài nhất); khung tĩnh neo 17,46 s từ 5:05,5 (bản xem).
- **F2** chuyển 101 beats `k: loi` ra khỏi `beats` (vd. `moc_loi`).
- **F3** đặc tả animatic: `animatic: true`; bản cuối trộn có `nhac[]`.
- **F4** đặc tả: `khung_neo: true` cho KA/KB/KC (hiện chỉ có trong log shot → Q37 miễn 0 khoảng), `im_lang: true` cho KB1943, KA2026.
- **F5** C3, C5: khai `lop_nha` (hoặc `opt.bfile`) nếu khung có phố.
- **F6** xuất `log_chu`.
- **F7** chủ dự án chấm XEM CÂM.
- **F8** log shot cho 1.17: `trong_pct` theo khung (R2; hiện thiếu cả 43 shot), `so_goc`/`goc_may` (R3), `chu_the_eo_dat` + `chu_the_pct` (R1); với 5 đoạn Omni của ANIMATIC-T3-V2: `minh_hoa`, `nhan_minh_hoa` hoặc `log_chu`, `agl_m`, `so_ai` (model, lệnh, SHA).

## 5. Selftest
| Bộ | Trước khoá | **Sau khoá (cây 1.17.0)** |
|---|---|---|
| `selftest_k117.py` (mới) | 96/96 | **96/96** — N2P đáp án 3, N2P-1 7, N2P-2 5, N2P-3 4, N2P-4 3, vision 2, N2P-5 6, N2P-6 6, áp dụng 2, MINH-HOA 16, SACH-1 3, EO-DAT-R1 4, R2 6, R3 6, Q33 6, Q33-K2 2, ML1 2, NC-H1 4, cấp 9. Mọi luật ≥ 1 ca đạt + ≥ 1 ca trượt |
| `selftest_k117.py --api` (lượt thật, 1 lần) | **104/104** (thêm 8: gpt 6/6, claude 6/6, hợp 6/6, q_thoi_dai 3/3, đối chứng N2P-1…4 0 báo) | — (không chạy lại để giữ chi phí) |
| `selftest_k116.py` | 144/144 | **144/144** |
| `selftest_k115.py` | 105/105 | **105/105** |
| `selftest_k114.py` | 126/126 | **126/126** |
| `selftest_k113.py` | 64/64 | **64/64** |
| `selftest_k1122.py` | 37/37 | **37/37** |
| `selftest_k1121.py` | 48/48 | **48/48** |
| `selftest_k112.py` | 75/75 | **75/75** |
| `selftest_k2.py` | 129/129 | **129/129** |
| `selftest_ll.py` | 317/317 | **317/317** |

**Kiểm có đáp án N2+** (khung thử NC-N2P: render cổng "cang" + 6 lỗi chèn; khung ghép dựng tại chỗ bằng dán lại lớp (a)):
| | L1 máy bay | L2 ô tô | L3 cột điện | L4 tàu chiến | L5 cột cờ (dải a) | L6 người | Bắt | Đối chứng |
|---|---|---|---|---|---|---|---|---|
| Bản lưu NC-N2P (gpt / claude) | ✓/✓ | ✓/✓ | ✓/✓ | ✓/✓ | ✓/✓ | ✓/✓ | **6/6 · 6/6** | 0 |
| Lượt thật 21/10 (gpt / claude) | ✓/✓ | ✓/✓ | ✓/✓ | ✓/✓ | ✓/✓ | ✓/✓ | **6/6 · 6/6** | **0** |
| q_thoi_dai (lượt thật, trừ nghi vấn render) | ✓ | ✓ | ✓ | — | — | — | **3/3** | 0 |
Máy: ghép (a) **0/255**; dải 20 px **2 cụm** (L5 [483,337], L6 [342,627] — khớp số NC-N2P); T9b 0,39 / 0,80 %; khung chưa ghép (a) lệch 40/255 → bắt; tô nước 6 % đất → T9b > 2 % → bắt.
Video (v) tổng hợp 320×180: hoà 2 s → bước **0,68** ΔE/khung (sạch); cắt cứng → **4,26** (bắt); nhấp nháy ±2 → **0,73** mức xám/khung so đối chứng 0 (bắt).

**`k2check` tập cũ** (cùng đầu vào, hai cây luật trong thư mục tạm có liên kết tới repo; `do/chay-t1-t2.sh`, `do/selftest-va-t1-t2-sau-khoa.txt`):
- Trước khoá: T1 **30/31**, T2 **48/49** giống hệt — chỉ khác LOCK (chưa khoá).
- **Sau khoá: T1 31/31, T2 49/49 giống hệt** (kq, val, lỗi, sát ngưỡng, cấp, số Chặn/Cảnh báo); hàng LOCK ĐẠT ở cả hai, chỉ tên đổi "(1.16.1)" → "(1.17.0)". Không thêm hàng nào cho tập trước T3.

## 6. LOCK
- **Trước:** 1.16.1 `a3c39873751805a7a0a5e2b544bc2c28630d78e87725b777d3c7ba1c77cc2d2b` (2026-10-19T14:33:40Z).
- **Sau:** **1.17.0 `f6812decc87a1950617e8226b73fe737c1f3438c58b88de7eb9a7e4d202bce1c`** (DATE_UTC 2026-10-21T15:01:40Z). `--verify` → **KHỚP** (sau khoá, sau selftest, trước mỗi commit).
- `lock.py` không cờ gọi **đúng một lần**, sau khi 10 bộ selftest đạt.

## 7. Chi phí thật
| Khoản | Mốc / chặn | Thật | Ghi chú |
|---|---|---|---|
| OpenAI (gpt-6.1-sol, nhìn) | ≤ $3 (cùng Claude nhìn) | **$0,0784** | 2 lượt: khung thử $0,0454, đối chứng $0,0330 (`do/api/n2p-cost.jsonl`) |
| Claude API nhìn (claude-sonnet-5-5, `judge.call`) | (trong $3) | **$0,1351** | khung thử $0,0715 (đọc 10 ảnh), đối chứng $0,0636 |
| Claude API O2 (`q_thoi_dai`, 4 khung + bước phóng) | (trong $3) | **$0,1556** | `do/api/selftest-api.json` |
| **Tổng nhìn + O2** | **$3** | **$0,369** | |
| Claude phiên chính (token) | mốc $5, chặn $15 | không đo được từ container | không chạm chặn; không lỗi lặp ≥ 3 |
| ElevenLabs / Gemini / RunPod / YouTube | 0 | 0 / 0 / 0 / 0 | không gọi |
| Giờ máy | — | ≈ 0,9 h đồng hồ | k2check animatic 1.16.1 lần đầu 7 m 41 s (đọc đĩa lạnh); các lần sau ≈ 1–3 phút |

## 8. Dòng sổ đề xuất (phiên P sau ghi — phiên này không sửa sổ)
- **COST-LEDGER.csv** (20 cột):
  `K-1.17,"Luật 1.17.0: N2P-1…6 (N2+ T4), MINH-HOA, EO-DAT-R1…R3, khiếu nại animatic T3 (Q33, ML1, NC-H1), V7C-D5",K,2026-10-21,,,,,0.291,3,claude-sonnet-5-5 (judge.MODEL) + gpt-6.1-sol,0,0,0.9,,0,,,reports/k117/K117-BAO-CAO.md,"OpenAI $0,078 (2 lượt nhìn); Claude API $0,291 (nhìn $0,135 + O2 $0,156); ElevenLabs 0; Gemini 0; RunPod 0; YouTube 0; LOCK 1.16.1 a3c39873 → 1.17.0 f6812dec; token phiên chính không đo được"`
- **RIGHTS.md**: `checks/ll/fixtures/k117/n2p/khung-thu.jpg` — khung thử nội bộ: render của dự án (cổng "cang", NC-CPU cách A) + 6 vật chèn bằng OpenAI gpt-image (NC-N2P, sổ `reports/nc-n2p/so-ai.jsonl`); **chỉ dùng kiểm luật, không phát hành**. `render.jpg`, `id-cang.png`: sản phẩm dự án. `data/cam_thoi_dai.json`: văn bản dự án (NC-N2P).
- **AUTHORSHIP.md**: chưa có quyết định của chủ dự án trong phiên này. Khi chủ dự án duyệt K117-D* (§10), ghi nguyên văn + giờ.
- **BAI-HOC** (phiên P cân nhắc): (a) đặc tả để mốc câu lời trong `beats` làm phồng nhịp Q37 và sinh 101 lỗi (a); (b) `khung_neo` khai ở log shot nhưng không ở đặc tả → Q37 không miễn; (c) k2check lần đầu trên container mới chậm (≈ 7 phút) vì đọc đĩa lạnh.

## 9. Chỉ số trong ±5 % quanh ngưỡng (luật cứng)
**Dữ liệu thật:**
- Animatic T3 (1.17): **Q33 "đúng 2 lần"** ở anim_H3 (Q33), anim_N1_5 (Q33-K2, Q33 (1.13)) và các góc khác = trần 2 (0 %).
- Animatic T3: shot eo đất **N2_7 14,42 s** so ngưỡng R3 "> 15 s" (−3,9 %) — không vào R3.
- Kiểm có đáp án N2+: không giá trị nào trong ±5 % (T9b 0,39 / 0,80 % so 2 %; lệch (a) 0).

**Ca selftest cố ý đặt đúng ngưỡng:** N2P-6 tấm nền 50 % · minh hoạ 20 % · tổng 70 %; MINH-HOA 20 %; N2P-5 hoà 2,0 s; EO-DAT-R3 shot đúng 15 s (không xét).
**Không thêm phần tử nào để vượt ngưỡng.**

## 10. Quyết định đề xuất
| # | Đề xuất | Ưu | Nhược | Tác động | Rủi ro |
|---|---|---|---|---|---|
| **K117-D1** | Duyệt mức N2P-1…6: **Chặn ở G2, Cảnh báo ở animatic**; N2P-1 (c) cụm dải luôn Cảnh báo | Khớp §15 (c) "cổng bắt buộc"; cùng sơ đồ K116-D5 | Tấm chưa soi bằng mô hình = Chặn ở G2 (cần chi ≈ $0,2/tấm) | T4 G2 | Mô hình báo dư → người đọc phải phân xử |
| **K117-D2** | **Chốt ngưỡng R1/R2** (đề xuất: chủ thể ≥ 25 %; trống > 60 % liên tục ≤ 6 s; ≤ 1/3 mỗi chương) **hoặc gửi nguyên văn §14.7**; định nghĩa **R4** | Gỡ "K đề xuất tạm" | — | `q_k117.py` hằng số | Ngưỡng tạm lệch ý chủ dự án |
| **K117-D3** | Xác nhận 3 khiếu nại luật đã sửa: Q33 miễn "cùng điểm máy, năm khác"; ML1 `cau: ""`; NC-H1 nhận `opt.bfile`/`lop_nha` | Hết 5/8 nhóm Chặn sai ở animatic | Q33 miễn dựa trên năm log (tự khai) | Mọi tập từ T3 | Lặp thật khác năm không bị bắt — vẫn còn Q26b, XEM CÂM |
| **K117-D4** | MINH-HOA (c) "kẹp giữa hai shot 3D" làm **minh hoạ mở đầu phim** (§14.1 (c) nêu "móc mở đầu") luôn trượt. Đề xuất: cho phép shot đầu phim nếu shot sau là 3D | Không trái §14.1 (c) | Lệnh K-1.17 nói "kẹp giữa" | MINH-HOA (c) | Hiện giữ đúng lệnh (chặt) |
| **K117-D5** | Duyệt định nghĩa N2P-5: bước = max ΔE76 TB lớp (c)/khung ≤ 1,0; nhấp nháy ≤ max(1,5 × đối chứng, **sàn 0,02**) | Đo được khi đối chứng = 0 (render tĩnh) | Sàn 0,02 do K đặt (NC đo 0,006) | T4 tấm nền | Sàn quá thấp với nén H.264 → đo trên bản không nén mất |
| **K117-D6** | N2P-2 (b): O2 chỉ tính nghi vấn **mới so với render** | Loại báo nhầm cờ nhỏ đã có ở render (NC-N2P) | Lỗi thời đại sẵn có ở render không vào N2P (vẫn ở O2 riêng) | — | — |
| **K117-D7** | Nhãn "Illustration": dùng `log_chu` (khuyến nghị) thay OCR | Số đo thật từ trình dựng | Phiên dựng phải xuất log | ANIMATIC-T3-V2, T4 | Không log → THIẾU |
| K117-D8 | Giữ Q37 không nhận biến cố log; làm biến cố ĐO theo K116-D4 khi có V7B/T3 bản cuối | Không nhận số tự khai | Q37 vẫn TRƯỢT animatic tới khi phim thêm biến cố | — | — |

## 11. Việc chờ chủ dự án
1. Quyết **K117-D1…D8** (chính: D1, D2, D3, D4).
2. **Gửi/ghi Kinh thánh §14.7 (R1–R4) và §15 nguyên văn** lên repo (phiên P-2110?) để K đối chiếu ngưỡng; nêu định nghĩa **R4**.
3. Chấm **XEM CÂM T3** (§13.4).
4. Phiên P: ghi sổ theo §8 (COST-LEDGER, RIGHTS, BAI-HOC); merge `checks-1-17` khi duyệt (nhánh này **không** merge).
5. Phiên ANIMATIC-T3-V2 / bản cuối T3: danh sách F1–F8 (§4).
6. Việc treo từ K-1.16.1: K116-D4 (biến cố đo cho Q37, thước cắt trên V7B).

## 12. Tệp đã sửa
| Tệp | Việc |
|---|---|
| `checks/ll/q_n2p.py` (mới) | N2P-1…6: mặt nạ ID, (i) lớp (a) + dải 20 px, (iii) T9/T9b, kết luận theo mô hình, O2 đối chứng render, (v) video, (vi) trần |
| `checks/ll/q_n2p_vision.py` (mới) | 2 mô hình nhìn (OpenAI + Claude ghim), bộ đệm, sổ chi phí; mặc định tắt |
| `checks/ll/data/cam_thoi_dai.json` (mới) | danh sách CẤM NC-N2P (nguyên văn, SHA `3f5576e4…`) |
| `checks/ll/q_k117.py` (mới) | MINH-HOA, EO-DAT-R1…R3, miễn Q33 theo năm, lớp nhà tl/* |
| `checks/ll/q_scene.py`, `q_k2var.py` | Q33 / Q33 (1.13) / Q33-K2: tham số `nam_log` (chỉ tập từ T3) |
| `checks/ll/q_mach.py` | ML1 `v117`: `cau: ""` = không gắn câu |
| `checks/ll/q_noi.py` | NC-H1 `layer_of(z, v117)` |
| `checks/ll/q_k116.py` | SACH-1 nhận nhãn Illustration trong shot minh hoạ |
| `checks/ll/cap112.py` | cấp 11 hàng mới; tập `CONG` (cấp theo cổng, gồm K-LAI-3V) |
| `checks/ll/k2check.py` | nối hàng 1.17, `--n2p-vision`, `nam_log`, `v117` |
| `checks/ll/selftest_k117.py` (mới) + `fixtures/k117/n2p/` | 96 ca (+ `--api`); bản sao đáp án NC-N2P (1,6 MB) |
| `checks/ll/RULES-LL.md` | mục 1.17.0 + tự kiểm |
| `checks/cinecheck/__init__.py`, `checks/LOCK` | 1.17.0 |
| `reports/k117/` | báo cáo, CHECKPOINT, `do/` (tái hiện animatic, Q33, T1/T2, selftest, lượt API) |

**DỪNG — chờ chủ dự án.**
