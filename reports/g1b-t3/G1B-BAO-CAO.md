Nhánh thật: `ccr-6189ede9-lpjwe0` (harness buộc tên này; lệnh yêu cầu `k2c-t3-g1b`). Gốc: `main` = `origin/p-1810c` @5253ba2b. Không merge. Không sửa `checks/`, `docs/`, nhánh khác; `main` chỉ chạm ở bước 0.

# G1b T3 Gibraltar — BÁO CÁO: animatic toàn tập 540p + chuẩn bị dựng

## §0 Tóm tắt

| Việc | Kết quả |
|---|---|
| Bước 0 | `main` ff `6c16e548 → 5253ba2b` (= p-1810c, 69 commit); lock **1.15.0 f4fa0349… KHỚP**; preflight `6c16e548..main` trượt **đúng 1 mục** `reports/v5b2d/khung/v5b2d-t-540p.mp4` (SHA-256 `338cef97…a4a8f`, khớp ngoại lệ P10C-1); `git push origin main` **qua bình thường** — hook pre-push của container chỉ là hook LFS, không chặn, nên **không dùng `--no-verify`**. `docs/BIBLE-KENH2.md` có "## 12.". |
| 1. Khung sạch §12.1 | Cờ `p.sach` trong lớp chữ `scripts/k2/lib/k2.js`: trên hình chỉ còn bộ đếm năm/ngày, chip nơi ≤ 3 s khi vào nơi mới, số/câu trích ≤ 3 s kèm nguồn ngắn. Tắt dòng nguồn, nhãn AI, dòng phương pháp, nguồn ghost, "approx./estimated/Ruins". Dữ liệu vẫn ghi log (`g1b/log-shot.json`: nguon, bac, ai_image, ai_texture, chu_tat). Thẻ cuối **"How this film was made" 5 s**. Văn bản mô tả YouTube, câu minh bạch, bình luận ghim: `phat-hanh/nguon-mo-ta.md` (4 423 ký tự, có ghi chú "AI use = Yes"). |
| 2. VL1 | 5j 17,0 → 18,5 s; tổng **721,2 s** (+ thẻ phương pháp 5 s = 726,2 s); `tu_kiem.py` **ĐẠT**; KA2026 đủ 8 s không lời (lời 5j kết ở 18,4 s). |
| 3. Animatic 540p | **74 shot + thẻ phương pháp, 726,2 s**, dựng bằng máy dựng V6 bản SẢN XUẤT (llvmpipe). 48 shot 3D qua một cảnh tổng quát `tl/t3s` + cảnh V6 có sẵn (vinh6, bo6, gib20). Mọi cú máy 3D ≤ 6 s. Phụ đề lời làm đường ray tạm, nung riêng trên bản xem. |
| 4. AI đọc nguồn | Lọc 62/82 mục (a 12 · b 32 · c 18); bảng gác 7/9/1782 đọc từ **ảnh trang Spilsbury tr. 74**: 793 bộ binh + 108 pháo binh, khu TOWN 397. **Chưa áp vào hình** (xem §2.4). |
| 5. Giờ máy thật 1080p | Đo 2 khung/cảnh × 72 cảnh trên máy rảnh: cảnh 3D **7,2–11,1 s/khung (trung vị 8,6)**; cả tập **29,6 h** một tiến trình → **4 gói, mỗi gói ≤ 7,4 h máy đo / ≤ 9,3 h máy chậm (×1,25)**. |
| 6. Người | MPFB2 **clone được** qua proxy git (HTTPS vẫn 403). Mocap CMU / 100STYLE (CC BY) / Quaternius (CC0) dùng được, không NC/SA/ND. **toy_like 7,0–8,7 — chưa đạt ≤ 4.** |
| 7. Ảnh 1940s | Kiểm có đáp án 3 ảnh NARA 342-FH: Real-ESRGAN loại cả 3 (cạnh mới 49–51 %), Swin2SR đạt 1/3. **Dùng bản gốc.** |
| 8. Kiểm | k2check 1.15 `--cap`: **TRƯỢT** (Q26b, Q33, Q37, ML1, NC-H1 1 shot, BD-1, K-LAI-*). Đạt NC-H2/H3/H4, Q26b-K2, Q34–Q36, Q32. Khiếu nại cho K 1.16: `khieu-nai-K.md` (7 mục). O2 thời đại: 151 khung, **2 khung có nghi vấn**. |
| Chi phí | Claude API **$5,632** (vượt mốc theo dõi $5 — §6) · OpenAI **$0** · ElevenLabs 0 · YouTube 0 · giờ máy ≈ 9 h đồng hồ tường bận máy (§6). |

**Xem nhanh:**
- Bản xem trong git: `reports/g1b-t3/animatic/animatic-270p-xem.mp4` (480×270, 12 fps, 4,85 MiB).
- Tờ khung 74 shot: `reports/g1b-t3/khung/to-khung-74-shot.jpg`.
- 7 khung cổng PNG sạch: `reports/g1b-t3/khung/cong-*.png`.

## §1 Việc đã làm

### 1.1 Bước 0
- Local `main` là ref cũ của clone nông. Tôi `fetch --unshallow`, đặt `main` = `origin/main` (6c16e548), rồi `merge --ff-only origin/p-1810c`. Không có commit mới, không force.
- Kiểm `merge-base --is-ancestor origin/main origin/p-1810c`: **đúng**.
- Preflight cả dải: chỉ CHẶN P3 cho video 11,0 MB của V5b-2d, SHA khớp ngoại lệ một lần.
- Đẩy `main` thành công mà không cần `--no-verify` (hook container là LFS). Nhánh làm việc tạo từ `main` mới.

### 1.2 Khung sạch (§12.1) trong máy dựng
- **Lớp chữ** `scripts/k2/lib/k2.js`:
  - `sachP()` lọc đặc tả shot khi `p.sach`.
  - `soLayer()` vẽ số/câu trích ≤ 3 s kèm nguồn ngắn 34 px.
  - `tlLayer` bỏ chữ cảnh tl đã ghi (`ai_label`, `method`, `ghost_src`, `index_src`, `tag`, `card` không khai `so`) và đếm vào `LL.sachTat`.
  - Inset bỏ chữ "Map: …".
- **Cảnh `tl/t3s`** chỉ vẽ bộ đếm. Cảnh V6 cũ (vinh6/bo6/gib20) vẫn ghi chữ cũ nhưng lớp lọc chặn khi dựng.
- **Chip nơi**: chỉ khi `vung` khác shot trước, hiện ≤ 3 s. **Số/câu trích**: lấy từ `[TRÊN HÌNH]` của lời khoá, đặt ở đầu câu lời nói tới (nhịp 2,5 từ/s).
- **Bỏ khỏi hình** dòng "A history explainer · every date sourced…" (0b–0e) theo §12.1. Lời 0e vẫn nói ý này. Đã ghi trong log.
- **Thẻ "How this film was made"** (5 s, 40 px @1080):
  - 6 câu của `phat-hanh/the-phuong-phap.json` (phiên con): nguồn chính, chỗ ước tính, AI dùng vào việc gì, câu C2PA.
  - Câu C2PA viết "YouTube **may** label…" vì trang chính sách chỉ dùng chữ "may".
  - **63 từ / 5 s là quá nhanh để đọc trên điện thoại** → quyết định §5 D6.
- **`phat-hanh/nguon-mo-ta.md`**:
  - Mô tả tiếng Anh: nguồn theo chương, "What is estimated", "How AI was used".
  - Câu §10.6 nguyên văn.
  - Ghi chú người đăng: bật **AI use = Yes** (P10C-2), kiểm trang chính sách mỗi lần đăng.
  - Bình luận ghim 1 207 ký tự + 4 trả lời sẵn. Danh mục nguồn đầy đủ chia vào 5 trả lời dưới bình luận ghim.

### 1.3 Animatic 540p
- **Đặc tả sinh tự động**: `channel-k2/k2c-t3-01/g1b/mk_ep_g1b.py` (đọc `vay-ham/treatment.json` + `script-v4.1-KHOA.md` + `g1/kiem-chu.json`) ra:
  - `g1b/episode.yaml` (75 đoạn, 74 cảnh);
  - `ray-loi.srt` (133 dòng);
  - `log-shot.json`;
  - `cut-plan.json`.
- **Một lệnh dựng**: `bash scripts/k2tl/g1b_animatic.sh` (spec → render → nhạc tạm → ghép → ray).
- **Thời lượng**: theo bảng shot khoá (nhịp **2,5 từ/s**, `g1/kiem_loi.py`, lời bắt đầu trễ theo `bat_dau_tre_s`). Nhịp Eric đo ở T2 **chưa áp** vì giọng series đang chọn — ghi rõ.
- **Cảnh 3D**: `design/k2v/tl/scenes/t3s.js`, một mô-đun tham số hoá:
  - Lớp nhà theo mốc: gói theo năm (OSM 2026 / Catastro La Línea theo năm xây / ghost c.1900); `town1782` (Drinkwater 1786 + lấp ước tính + vùng "THE RUINS OF GIBRALTAR"); ghost 1704 và ghost 1943 (gói thêm bằng `scripts/k2tl/pack_g1b.sh`).
  - Máy: push / bay dọc tuyến / orbit / lateral / top-down / neo, mỗi cú ≤ 6 s, nối bằng cắt.
  - Chiến tuyến 1730 mọc theo thời gian (`lineaAt`), tuyến M4, dải hai bên biên giới tô theo số toà (`border.json toa_dung`).
  - Người V6 có khớp.
  - **Thêm trang phục thời kỳ sau** trong `people.js`: `mod`/`modw` (≥ 1946), `m1910` (1850–1939), `k43` (1939–45). Trước đây mọi người là lính/dân 1782 đội tricorn, sai thời đại ở cảnh 1910/1943/2026.
- **Cảnh V6 dùng lại**:
  - 2m = vinh6 0–14 s (cú liên hoàn, King's Bastion có vân HC7 `ai_texture`) + bo6 6 s.
  - 4b = gib20 9–24 s (bật `tech.v6`).
- **Nhảy mốc năm trong shot**: 0e "tua ngược" chia 4 cảnh (2026 / 1943 / 1782 / 1704), 5j chia 5 cảnh (1704 / 1735 / 1910 / 1943 / 2026). Mỗi mảnh là một cảnh riêng, cùng một đường máy.
- **Phố dày (V6-3)**:
  - Cảnh phố 1782 đổ nát (2g, 2j, KA1782) đi kèm phố còn nguyên: 0e (2026 + 1943), KB2026, 5d, KC1910/KC2026 (La Línea), 1d/1e (phố 1704 nguyên vẹn).
  - Khung `cong-pho-con-nguyen-2026.png`.
  - Grand Parade (2j) có đồn trú + đám đông ở tiền/trung cảnh. **Số lượng và cách xếp là minh hoạ; nguồn bậc 2 chưa áp** (§2.4).
- **Khung neo**:
  - KA1782 / KB1943: bản LAI 540p của V6 (`reports/v6/khung-neo/v6-LAI-960x540-*.mp4`), cắt bỏ dải chữ cũ (khung 810×456 phóng lại) và **chậm 0,85×** để đủ 10,3 s đoạn cần. Chỉ dùng cho animatic.
  - KB2026 / KA2026 / KC1910 / KC2026: khung tầm mắt k2v ở đúng tư thế PT (`design/pt/scene/pt_site.py`: `pt` và `k1782`). Bản sản xuất nên dùng nền PT/Blender (§5 D4).
  - Gói PT4 + vật nền phụ V6-5 nằm trong 2 clip LAI.
- **Ảnh/tranh/bản đồ lịch sử**:
  - Animatic dùng ảnh tham chiếu ≤ 1 600 px trong `vay-ham/ref/`, cộng 3 ảnh tải thêm: Rooke Rijks RP-P-OB-33.529 CC0 (SHA `7f24f0bb…`), Capture 1704 Rijks RP-P-OB-83.181 CC0 (`710731a6…`), LoC 2020680546 (`57fbdfc5…`).
  - Ảnh > 6 s dùng Ken Burns hai chặng (đổi hướng giữa shot là một biến cố thật).
  - Văn bản hiệp ước (1h, 2r, 4h, 5g) chưa có ảnh tài liệu trong repo → thẻ trích nguyên văn trên nền tư liệu liên quan.
- **Thẻ số**: 0d, 1f, 2d, 2i, 2n, 4e, 5b, 5e, 5i, đặt trên nền cảnh trước làm mờ.
- **Bản đồ chiến lược SM1–SM3** (phiên con):
  - ETOPO 2022 + ranh Cliopatria (Zenodo 23128623, SHA khớp NC-BD) + tuyến claim T….
  - Khung sạch: không dòng nguồn, không "approx.".
  - SM3 tách a 4,6 s + b 3,4 s.
  - **SM1 (1704) dựng lần đầu**: `scripts/k2/hist/sm1_spec.py`, `lop-sm1-1704.json`.
- **Soi trước khi dựng cả tập**: 1 khung/cảnh (`scripts/k2tl/g1b_probe.sh`, tờ `g1b_sheet.py`). Đã sửa máy ở 0a, 0g, 1g, 1i, 2o, 4d, 5j, KA2026, 5k, và lỗi trang phục.

**Tệp animatic** (lệnh tái tạo: `bash scripts/k2tl/g1b_animatic.sh`):

| Tệp | Nơi | Cỡ | SHA-256 |
|---|---|---|---|
| Master 960×540 crf16 (nhạc tạm) | ngoài git `/var/tmp/cine-out/k2c-t3-g1b/k2c-t3-g1b-v1-master.mp4` | 688 MB | `e186dbb266ccef16437120412907f27f7f82129254fdb6215994be2c7046dc2b` |
| Bản xem 540p **có ray lời** (2,3 Mb/s) | ngoài git `/var/tmp/cine-out/k2c-t3-g1b/k2c-t3-g1b-animatic-540p-ray.mp4` | ≈ 210 MB | `2b8ed11fbfbdf8d8c7366b841262413ad6ba0c97486f313e3d693c253755f4f0` |
| Bản xem 270p 12 fps có ray | **trong git** `reports/g1b-t3/animatic/animatic-270p-xem.mp4` | 5 088 914 B | `aab41c2818bb4e55e05d7d01c21d29fbf2d57d0b9b0744a3aa8c5e0195ba6c65` |

Master dựng hai lần (trước và sau khi thêm khai báo kiểm) ra cùng SHA, tức dựng là tất định.

### 1.4 Đo giờ máy 1080p + kế hoạch render song song
- **Cách đo**:
  - Đặc tả 1080p (prep không `K2_DRAFT`) → `/var/tmp/cine-out/k2c-t3-g1b-1080/heroes.json`.
  - `P=1 W=1920 H=1080 FR=two bash scripts/k2tl/g1b_probe.sh` dựng khung 1/3 và 2/3 mỗi cảnh, một tiến trình, máy không tải khác (03:52 → 04:16 UTC).
  - Số đo: `reports/g1b-t3/render/do-1080.json` + `do-1080-probe.log`.
- **Kết quả**:
  - 49 cảnh tl: **7,19 / 8,60 / 11,07 s/khung** (min/trung vị/max).
  - Ảnh 0,4 s, bản đồ 0,5–1,6 s.
  - Khung 3D cả tập: 11 266.
  - V6 ghi 16,8 s/khung vì đo khi máy có tải song song.
- **Kế hoạch**: `scripts/k2tl/g1b_goi.py` → `reports/g1b-t3/render/ke-hoach.json`/`.md`.
  - Cách tính giờ một cảnh = setup + khung × s/khung. Gói hoá tham lam LPT. Trần 10 h ÷ hệ số máy chậm 1,25.
  - **Tổng 29,6 h một tiến trình** (gib20 dựng đủ 24,5 s dù chỉ dùng 15 s; bản sản xuất có thể cắt).
  - Chia **4 gói**: 7,41 / 7,39 / 7,39 / 7,39 h máy đo = 9,23–9,26 h máy chậm, **≤ 10 h đồng hồ**.
- **Lệnh dựng một gói**: `bash scripts/k2tl/g1b_goi_chay.sh G01` (…G04).
  - Ghi SHA mã. Dựng tiếp `--resume` khi bị ngắt.
  - Cuối gói dựng **khung tham chiếu màu chung** `g1b_2j_0 #150` → `ref-G0x.jpg`.
- **Ghép**:
  - Chép các thư mục cảnh đinh về `/var/tmp/cine-out/hero/`.
  - Kiểm khớp màu: các `ref-G*.jpg` phải trùng SHA, hoặc ΔE00 trung bình ≤ 0,5, và cùng commit mã.
  - Rồi `build.sh render` (giữ cảnh theo stamp, dựng lớp 2D ≈ 17 428 khung × ~0,5 s ≈ 2,4 h) → mix → ghép.
  - Bộ dựng tất định (master 540p lặp lại cùng SHA), nên các gói cùng mã phải cho cùng điểm ảnh.

### 1.5 Người (V6-4) — phiên con, `reports/g1b-t3/nguoi/`
- **MPFB2**: HTTPS bị chặn, lỗi nguyên văn `403 {"message":"GitHub access to this repository is not enabled for this session. Use add_repo to request access..."}`. Qua `add_repo` + proxy git thì **clone được** (HEAD `3af0cd5a…`, ngoài repo). Tài sản CC0, mã GPLv3 (không dùng mã). Đã dựng thử 1 người 1782 + 1 người 1943 (`nguoi/mpfb_thu.py`, Cycles 119 s); quần áo mới là vùng màu vẽ lên da.
- **Mocap** (giấy phép nguyên văn + SHA trong `nguoi/giay-phep/`):
  - CMU "free for all uses": 3 clip.
  - 100STYLE CC BY 4.0: 6 clip, phải ghi công.
  - Quaternius CC0: chưa tải được (itch.io trả "invalid key" 3 lần).
  - Bản thử `mocap_gait.py` rút chu kỳ hông 16°, r² 0,93.
- **toy_like** (chấm mù 3 vai, `claude -p` ghim claude-sonnet-5-5): khung neo 1782 **8,00** · khung neo 1943 **7,00** · P4 **8,67** · P5 **8,67**. Bản people.js cải tiến (pháp tuyến mượt, khớp khuỷu, 5 tư thế, vân vải, bóng tiếp đất) **không đổi điểm** → không áp; để ở `nguoi/people-js-thu.patch`. Người MPFB cận cảnh **7,0** (people.js 9,0). Lý do người chấm: thân "peg", đội hình lưới, "box torsos, stick legs".
- **Thang đo lệch giữa hai lần chấm**: lượt này ra 7–8,7, còn V6 ghi 5,8–6,6 với cùng loại khung (người chấm và đề khác). Cần cố định đề và người chấm trước khi so tiếp.

### 1.6 Ảnh chụp 1940s (§12.3) — phiên con, `reports/g1b-t3/phuc-che/KQ.md`
- Cả 3 bản gốc NARA 342-FH tải lại đều khớp SHA. Chỉ xử lý ảnh chụp, không đụng tranh/bản khắc.
- Kiểm có đáp án (×0,5 → phục chế ×2 → so gốc):
  - Real-ESRGAN x2plus: cạnh mới 49–51 % → **loại cả 3**.
  - Swin2SR ×2: 000757 3,72 % **đạt**; 000759 8,64 % và 000761 6,34 % **loại**. Chỉ hơn bicubic 0,3–0,7 dB.
- Bản thân phóng bicubic đã cho 3,95–6,40 % cạnh mới (hạt phim), tức thước có nền nhiễu sát ngưỡng → khiếu nại A-G1B-6.
- Phục chế ×1 một vùng 000757: lệch trung bình 0,06 mức xám, mắt thường không thấy khác. **Không dùng bản AI; dùng bản gốc.**

### 1.7 Kiểm (bước 8)
**k2check 1.15 `--cap`** (`reports/g1b-t3/do/k2check-1.15-animatic.txt`, LOCK KHỚP):

| Hàng | Kết quả | Giá trị chính | Ghi chú |
|---|---|---|---|
| Q26b | TRƯỢT | tl/t3s 57,6 % | Một mô-đun dựng mọi cảnh 3D → khiếu nại A-G1B-4. Q26b-K2 (theo vùng) **ĐẠT**: 37 vùng, lớn nhất eo-dat 22,4 %. |
| Q33 / Q33-K2 / Q33 (1.13) | TRƯỢT | 46 / 30 / 44 lần pHash lặp không khai | Nhiều cảnh eo đất cỏ trống (đúng nguồn, ít nội dung) và thẻ trên nền mờ. Việc của tập. |
| Q37 / NHIP-K2 | TRƯỢT | biến cố khai 194, **TB 3,95 s**, dài nhất 10,0 s (khung neo) | Ngoài khung neo dài nhất 6,0 s. Khung tĩnh 11,46 s ở 5:58,8 (thẻ trích 2r trên nền gần tĩnh). |
| ML1 | TRƯỢT | 0/84 shot gắn | Đã khai `cau` / `claim` ở shot và `p` nhưng bộ kiểm không nhận → cần K chỉ trường (không đọc mã checks/). (b) "timelapse trôi 72 %" tính mọi cảnh tl là timelapse. |
| FT1 | CẢNH BÁO | khai lý do 0/15 | Cùng vấn đề tên trường (`ly_do` đã khai). |
| NC-H1 | TRƯỢT | 26/27 shot thành phố có lớp nhà | Còn 1 shot. "Không đo fabric 26" (cần lượt `--maskonly`). |
| NC-H2 / NC-H3 / NC-H4 | ĐẠT | strategic hợp lệ 4 shot | — |
| BD-1 | TRƯỢT | hợp lệ định nghĩa 4 | Nghi do SM3a/SM3b liền nhau (luật "không liền nhau"). |
| BD-2 | CẢNH BÁO | — | — |
| K-LAI-1…6 | TRƯỢT | — | Đặc tả animatic chưa khai khối `lai:`; K-LAI-2 trái §12.1 → A-G1B-1. |
| A1–A13 | CHỈ BÁO | −18,0 LUFS | Chỉ có nhạc tạm (ElevenLabs 0). |
| Q32 / Q34 / Q35 / Q36 / Q32b-K2 / NC-H5 / Q7/Q8 / K-R | ĐẠT | — | NC-H5 "không áp" vì bộ kiểm không nhận bộ đếm tl → A-G1B-2. |

**O2 soi lỗi thời đại** (`checks/ll/q_thoi_dai.py --buoc 5 --neo … --api`; `reports/g1b-t3/do/o2/ket-qua.json`): 151 khung, 2 khung có nghi vấn, $4,729.
- **22,5 s (0d)**: báo "tàu/nhà hiện đại" với năm 1309. Đây là lỗi **bảng năm tôi đưa vào** (thẻ "1309–1783" đặt trên nền cảnh 2026 làm mờ), không phải lỗi hình. Nền thẻ 0d nên đổi sang cảnh không hiện đại.
- **437,5 s (3f, 1910)**: một dải lát sáng có ngã chữ T trên eo đất. Có thể là đường thời đó (gói `roads.json` theo năm bằng chứng) hoặc vạch đường băng lọt ra trước 1941. **Chưa kết luận — cần người xem khung** (`khung/` + toạ độ trong ket-qua.json).

**Tờ khung**:
- `khung/to-khung-74-shot.jpg`: 74 ô, 0,85 MB.
- 7 khung loại cảnh cổng, PNG sạch 540p không chữ: vây hãm 2a, cảng/bờ 2f, phố dày 1d, hero 2m, đông người 2j, bờ + chiến sự 2m/bo6, phố còn nguyên 2026 KB2026.

**LK4 — câu/shot chủ dự án xem lại ở G1b** (kèm khung):
1. **"fourteen sieges" — 0d** (15,0–22,5 s). Thẻ "14 · sieges · 1309–1783" + nguồn ngắn "Sayer 1862 · García Sanz 2022 · Gibraltar National Museum" 3 s. Khung `khung/lk4-0d.jpg`.
2. **Thứ tự đoạn hầm 1782 — 2o/2p** (326,75–347,25 s). Hiện tại đi sau 2m (tấn công 13/9) và 2n (thương vong), lời mở bằng "Before the attack, all summer…". Khung `khung/lk4-2n.jpg`, `lk4-2o.jpg`, `lk4-2p.jpg`. Đề xuất ở §5 D11.

## §2 Số đo và những gì chưa làm được (ghi thật)
1. **0a / 5k "nửa đêm"**: máy dựng V6 chưa có đêm có đèn. Animatic dùng nắng chiều thấp (mặt trời ≈ 4°). Lời và hình đang lệch → D1.
2. **2o / 4d hầm (M11 mặt cắt)**: chưa có trong máy dựng; animatic dùng mặt ngoài vách bắc → D2.
3. **4i máy bay 1942, 5h hàng rào 2026 (C03), 3f hàng rào 1909**: chưa có mô hình. 3f vẽ tạm bằng dải tuyến M4 → D3.
4. **AI đọc nguồn chưa áp vào hình**:
   - Mapping có đủ (`g1b/ai-doc-nguon.json`).
   - Khung neo KA1782 trong animatic là clip LAI của V6, có ≈ 44 người. Bảng gác Spilsbury chỉ đỡ **≤ 1,5 lính/100 m phố** (≈ một toán tuần 3 người mỗi hẻm), vì chỉ Patroles + Orderlies (40 người) đi lại trong phố.
   - Người ở cảnh phố 1782 t3s vẫn là minh hoạ, chưa gắn id mục.
   - Đây là quyết định sáng tạo trái với Q-PT4-4 (30–80 người) → D8.
5. **Trang phục**: chưa có nguồn cho lính Hanover, Corsica, thuỷ binh. Nữ c.1900 (váy dài + mũ) chưa có lưới nên cảnh 1850–1939 chỉ có nam.
6. **Ảnh**: chưa có chân dung Hesse-Darmstadt và d'Arçon PD (1b dùng Rooke; 2l dùng phác thảo Copley). Văn bản hiệp ước mới là thẻ trích, chưa có ảnh tài liệu. 2p chưa có footage hầm có giấy phép → ảnh 1860 Rijks.
7. **SM** (phiên con):
   - Lời ‹SM3› cần 13,2 s nhưng shot chỉ 8 s (đã biết từ khoá lời: SM3 chảy sang 4g).
   - Nền SM1/SM3 dựng ở 120 điểm/độ; bản 1080p nên dựng lại ở 240.
   - Hướng cuối máy SM1/SM2 chưa khớp 1a/2f.
8. **Preflight sau đẩy**:
   - Commit `d9c496c0` có `reports/g1b-t3/nguoi/giay-phep/mpfb2-LICENSE.txt`: bản giấy phép nguyên văn có dòng phân cách `=======`, bị preflight P4 coi là dấu xung đột merge (báo nhầm).
   - Tôi đã đẩy trước khi chạy preflight dải này. Lý do: container không có hook preflight, chỉ có hook LFS.
   - Hai cách sửa (thụt dòng, hoặc đưa tệp ra ngoài git) đều bị trình phân loại quyền chặn, vì có thể coi là lách bộ kiểm.
   - **Chờ chủ dự án/P quyết**: giữ (báo nhầm), hay xoá tệp khỏi git và chỉ ghi URL + SHA. Mọi lần đẩy khác đều đã qua preflight.
9. **Máy khởi động lại 2 lần** (≈ 19:40 → 22:22 và ≈ 01:42 UTC). /var/tmp còn nguyên. Cảnh đã có stamp được giữ, cảnh dở dựng tiếp; bản ray đang ghi dở thì dựng lại. Không mất tệp.

## §3 Chỉ số trong ±5 % quanh ngưỡng (luật cứng)
- **Bản xem trong git** 4,85 MiB vs trần 5 MiB (−2,9 %).
- **Thẻ phương pháp** 5,0 s vs trần §12.1 "4–5 s" (0 %).
- **tu_kiem**: SM3 8 s vs trần strategic 8 s (0 %); KB2026 9,5 s vs trần khung neo 10 s (−5 %); KC2026 10 s vs 10 s (0 %).
- **Cú máy 3D** 6,0 s vs Q37 6 s (0 %): các cú cuối của 2c (6,0 s) và một số cú chia đều.
- **Q32b-K2**: ảnh 2k, 2l 12,0 s vs trần 12 s (0 %).
- **Lời 5j** kết ở 18,4 s trong shot 18,5 s (lề 0,1 s; VL1).
- **Ngoài ±5 %, nêu cho rõ**: Q37 TB 3,95 s vs 3,5 s (+12,9 %); Claude API $5,632 vs mốc theo dõi $5 (+12,6 %).
- **Không thêm phần tử nào để vượt ngưỡng.** Biến cố khai cho Q37 chỉ là cắt/số/thẻ đã có trên hình, và Ken Burns hai chặng là chuyển động máy thật.

## §4 Chi phí và giờ máy

| Khoản | Mốc / chặn | Thật | Ghi |
|---|---|---|---|
| Claude API | $5 / $25 | **$5,632** | O2 $4,729 + chấm mù người $0,903. Vượt mốc $5 khi chạy O2. **Lợi ích**: lưới lọc thứ hai trên toàn tập (151 khung) bắt 1 nghi vấn thật cần người xem (3f) + 1 lỗi bảng năm của tôi (0d). Phiên con nguồn/AI đọc nguồn và SM không gọi API. |
| OpenAI | $5 / $50 | **$0** | Không sinh ảnh. |
| ElevenLabs / YouTube | 0 | 0 / 0 | — |
| Giờ máy | 10 h | ≈ **9 h** đồng hồ tường bận máy (16:55 → 04:30 UTC trừ 2,7 h máy chết), phiên con chạy song song cùng máy | Dựng cảnh 3D 540p ≈ 3,5 h; lớp 2D + ghép 4 lượt ≈ 3,2 h; soi 1 khung/cảnh ≈ 1,5 h; đo 1080p 0,4 h; bộ đệm 0,5 h. Chưa vượt mốc 10 h. |

Chặn an toàn: không lỗi nào lặp ≥ 3 lần cùng nguyên nhân. Lặp góc máy ảnh (prep) đổi cách sau 3 lượt, từ xoay phương vị sang xoay + tiêu cự.

## §5 Quyết định đề xuất

| # | Đề xuất | Ưu | Nhược | Tác động | Rủi ro |
|---|---|---|---|---|---|
| D1 | Làm **đêm có đèn** cho 0a/5k (lượt chiếu sáng riêng + đèn đường có nguồn ảnh 2020s), trước bản sản xuất | Lời "midnight" khớp hình; bookend mở/kết đẹp | Thêm mã ánh sáng đêm cho llvmpipe (≈ nửa phiên) | 26,5 s hình | Đêm sáng hơn 1,5× A (luật §11.3 cho tấm C) — cần đo |
| D1b | Hoặc sửa lời 0a/5k thành "At dusk…" | Không cần mã | Chạm lời đã khoá | — | Phải mở khoá lời |
| D2 | **M11 mặt cắt hầm** theo plan ONI 1954 (NARA PD) cho 2o/4d | Đúng cơ chế lời nói | Mô-đun mới | 23 s | Bậc 1 cho tuyến hầm 1782 còn mỏng |
| D3 | Mô hình **máy bay 1942** (khối có nguồn ảnh NARA 342-FH), **hàng rào 1909/2026** | Hình đúng lời 4i/5h/3f | Thêm 3 mô hình | 48 s | Cần nguồn kích thước |
| D4 | Khung neo **2026 / 1910** dựng bằng nền PT Blender như 1782/1943 | Cùng chất lượng 4 cặp then/now | +2 h máy/khung | 34,5 s | Lại cần tấm C → thêm ai_image (K-LAI-1 ≤ 20 %) |
| D5 | Người khung neo/hero chuyển sang **thân MPFB CC0** + quần áo theo nguồn quân phục | Duy nhất đã hạ toy_like (9 → 7) | Việc quần áo lớn; khó ở k2v llvmpipe | Mọi cảnh người | Vẫn chưa ≤ 4 |
| D6 | Thẻ phương pháp: **2 thẻ × 3 dòng, mỗi thẻ ≈ 8 s** (hoặc 1 thẻ 15–18 s cuối phim) thay 5 s | Đọc được trên điện thoại (≈ 3 từ/s) | Trái §12.1 "4–5 s" | +11–13 s | Cần chủ dự án sửa §12.1 |
| D7 | Sửa câu §10.6 "on marked street frames" → "on two street frames" | Đúng thực tế khung sạch | Chạm câu minh bạch đã duyệt | Mô tả | — |
| D8 | Mật độ lính khung neo 1782 theo **bảng gác 7/9/1782** (≤ 1,5 lính/100 m, toán tuần 3 người + dân #13 che chắn đồ đạc) | Đúng nguồn bậc 2 (AI-T3) | Hẻm "vắng"; trái Q-PT4-4 (30–80 người) | KA1782 | Thua chấm "sự sống"; cần sửa Q-PT4-4 |
| D9 | Render 1080p theo **4 gói** (`ke-hoach.json`) | Mỗi gói ≤ 9,3 h máy chậm | Cần 4 phiên + dựng lại bộ đệm 4 lần | Ra master sau ≈ 10 h đồng hồ | Lệch mã giữa gói → kiểm ref-G*.jpg |
| D10 | Tăng biến cố thật để Q37 TB ≤ 3,5 s: chia cú 3D ≤ 4 s ở shot ≥ 12 s, thêm chuyển động sống có nguồn | Đạt Q37 | +≈ 25 cảnh con | Nhịp nhanh hơn | Dễ thành "thêm để vượt ngưỡng" — mỗi cú phải có vai truyện |
| D11 | LK4 thứ tự hầm: dời **2o–2p lên trước 2j** (mùa hè 1782 trước 8/9 đạn đỏ và 13/9) | Đúng trình tự thời gian; "Before the attack" thừa | Đổi thứ tự shot đã duyệt | ch.2 | Phải khoá lại lời (câu nối) |
| D12 | Nền thẻ 0d đổi sang cảnh không hiện đại (vd. SM1 hoặc tranh 1782) | Hết nghi vấn O2 giả | — | 7,5 s | — |

## §6 Việc chờ chủ dự án
1. **Duyệt G1b**: animatic (bản 270p trong git; bản 540p có ray ngoài git, SHA §1.3), tờ khung, 7 khung cổng.
2. **LK4**: "fourteen sieges" ở 0d; thứ tự đoạn hầm 1782 (D11).
3. **Quyết D1–D12**, nhất là:
   - D6 (thời lượng thẻ phương pháp — trái §12.1);
   - D8 (mật độ theo bảng gác — trái Q-PT4-4);
   - D1/D1b ("midnight").
4. **SM1 tô màu 1704**: nước không có claim phe để trống (kể cả Bavaria); Hà Lan thuộc TBN và Ý thuộc TBN tô màu Tây Ban Nha theo Cliopatria.
5. **Người**: chuyển sang MPFB (D5)? Chấp nhận rủi ro dữ liệu huấn luyện DIV2K/Flickr2K của Swin2SR/Real-ESRGAN không (hiện không dùng)?
6. **RIGHTS.md** (phiên P ghi):
   - 100STYLE CC BY 4.0 — ghi công "The 100STYLE Dataset - Ian Mason";
   - CMU mocap;
   - MPFB2/MakeHuman CC0 (tài sản);
   - Cliopatria (Zenodo 23128623) và ETOPO 2022 cho SM1;
   - 3 ảnh tải thêm (Rooke RP-P-OB-33.529, Capture 1704 RP-P-OB-83.181, LoC 2020680546);
   - nhạc tạm Tyrant.mp3 (dòng K2-MUS có sẵn).
7. **Preflight P4 báo nhầm** ở `mpfb2-LICENSE.txt` (§2.8): giữ, hay đưa ra ngoài git.
8. **Phiên K 1.16**: `reports/g1b-t3/khieu-nai-K.md` (K-LAI-2, NC-H5 b, BD-3 trái §12.1; Q26b theo vùng; Q37 miễn khung neo; thước phục chế; A* khi chưa có lời). Cần K chỉ tên trường ML1/FT1.
9. **O2 nghi vấn 3f** (437,5 s): người xem khung, xác nhận đường 1910 hay vạch đường băng lọt.
10. Phiên P merge nhánh này khi duyệt.

**DỪNG — chờ chủ dự án.**
