**Nhánh thật: `checks-1-17-2`** (đúng lệnh; harness gợi ý `ccr-c587fe9e-afkkdc`, không dùng làm nhánh làm việc). Gốc `origin/checks-1-17-1` @ `39d01859` (đã chứa main `96b5017c`). Không merge vào `main`, không đụng nhánh khác.

# Phiên K-1.17.2 — vá bộ kiểm theo quyết định chủ dự án 22/10/2026 11:09 (duyệt V2-D1…D8, không nhãn/câu AI trong phim) — BÁO CÁO

> Phiên K, 22/10/2026 ≈ 04:20–05:05 UTC. Mọi số là số đo thật trong phiên; tệp số đo ở `reports/k1172/do/`.
> Email chủ dự án không có trong tệp, commit, header, URL, payload hay User-Agent nào (UA duy nhất dùng: `CineLab-research (+https://github.com/HungQuach301/cine-lab)`, một lần tải trang YouTube Help). Phiên không gọi API trả phí nào.

## 0. Khối điều lệ và tóm tắt
| Trường | Lệnh | Thực tế |
|---|---|---|
| Loại phiên | K-1.17.2 | đúng |
| Nhánh | `checks-1-17-2` từ `origin/checks-1-17-1` @39d01859 | đúng |
| Vùng sửa | `checks/**`, `reports/k1172/**` | đúng (§9). Không sửa `docs/`, sổ, `design/`, `scripts/`, `channel-k2/`, `main`, nhánh khác; không ghi sổ |
| Đầu vào animatic v2 | `git show origin/k2c-t3-anim-v2:<đường dẫn>`, không merge | đúng; đọc @18a5f33d vào thư mục tạm |
| Chi phí | Claude mốc $3 (chặn $10), OpenAI $1, giờ máy 3 h; 0 Gemini/ElevenLabs/RunPod/YouTube | **Claude API $0 · OpenAI $0 · Gemini/ElevenLabs/RunPod/YouTube API 0**; giờ máy ≈ 0,75 h (§7) |
| `lock.py` không `--verify` | chỉ ở bước khoá cuối | **đúng một lần**, 04:50:31 UTC, sau khi 11 bộ selftest đạt; mọi lần khác chỉ `--verify` |
| Preflight | bắt buộc, `set -o pipefail`, commit chỉ khi dòng kết luận có "— ĐẠT" | mọi commit: `preflight: … (staged) — ĐẠT` + `PREFLIGHT ĐẠT` (§8) |
| Force / amend / dừng hỏi | không | không |
| Môi trường | `scripts/env/verify.sh` | 11 PASS, 4 FAIL (OpenEXR, three.js, tifffile/pyshp, k2v node_modules) — không mục nào cần cho `checks/` |

**Tóm tắt:**
1. **MINH-HOA** đo theo **ĐOẠN khai** (danh sách `minh_hoa: [{t0, t1, …}]` hoặc `minh_hoa: true`): (a) ≤ 20 % giữ; **(b) nhãn "Illustration" bỏ**; (c) kẹp theo khung 3D ngay trước/sau đoạn (kể cả cùng shot); (d) AGL theo khoá `cam[i]` ↔ `agl_m[i]`; (e) sổ AI nhận tên trường thật V2. Trên log V2: lỗi Chặn **18 → 4** (chỉ còn (e): log chưa nối sổ AI). SACH-1 không đổi.
2. **V2-D5**: K-LAI-1…6 hết "KHÔNG ÁP: tập không có khối lai / shot AI" trên V2 — nay K-LAI-1 3,7 % ĐẠT, K-LAI-2 bắt **mâu thuẫn khai C4/M1** (log ghi đoạn M1 nhưng shot `ai_image: false`), K-LAI-3/6 báo thiếu tệp kiểm / sổ AI, K-LAI-4/5/B KHÔNG ÁP có lý do (minh hoạ toàn khung).
3. **PP-1 (d)** = nguồn/bản đồ + chỗ ước tính; bỏ câu AI; không thêm luật cấm chữ. **K-LAI-2 (c)** (thẻ PP nói AI) bỏ theo cùng quyết định.
4. **CONG-BO-1** (mới): khung AI hoặc giọng tổng hợp → mô tả YouTube có câu "AI"/"synthetic" + `phat_hanh.youtube_altered_content: true`; **Chặn ở gói phát hành**, chỉ báo trước đó. V2: CẢNH BÁO (chưa có khối `phat_hanh`).
5. **TL-1 (V2-D7)**: cắt góc trong shot khai `so_goc`/`goc_may` không tính trần; vẫn in số thô. V2: không đổi (log chưa khai `so_goc`/`goc_may`); nếu khai cho 10 shot cắt góc → 13 cắt miễn → **4,35/phút** (đo, §5.3).
6. **EO-DAT-R1 (V2-D2)**: chỉ báo ở mọi cổng; in % vùng nở 1,5 % bề ngang cạnh pixel thô (K tự đo từ `chu_the_mat_na`).
7. **Selftest**: `selftest_k1172.py` **74/74**; k117 130/130, k116 144/144 (8 ca đổi kỳ vọng đúng chỗ quyết định 22/10, §3.2), k115 105/105 và k114 126/126 **giống hệt từng dòng** so với 1.17.1; k113 64/64, k1122 37/37, k1121 48/48, k112 75/75, k2 129/129, ll 317/317.
8. **LOCK 1.17.1 `b741f617…` → 1.17.2 `aca05e60…`**, `--verify` KHỚP.

## 1. Đầu vào đã đọc
- `reports/k117/K117-BAO-CAO.md`, `reports/k1171/K1171-BAO-CAO.md`; mã `checks/ll/q_k117.py`, `q_k116.py` (SACH-1, PP-1, TL-1, K-LAI-2), `q_lai.py`, `cap112.py`, `k2check.py`; `RULES-LL.md` mục 1.16–1.17.
- Nhánh `origin/k2c-t3-anim-v2` @`18a5f33d` (chỉ `git show`): `channel-k2/k2c-t3-01/animatic/episode.yaml`, `log-shot.json` (SHA `b4431a06…`), `reports/animatic-t3-v2/ANIM-V2-BAO-CAO.md` §8.4, §11 (V2-D2, D5, D7), `do/k2check-1.16.1.txt`; thêm `so-ai-gemini.jsonl` (SHA `f935f48a…`), `omni/kiem/M2-l3/M2-l3-kiem.json`, 8 tệp `xem/` (ghép làm video TL-1).
- Kinh thánh `docs/BIBLE-KENH2.md` §14.1 trên main @96b5017c. **§14.1 (f) bản sửa 22/10 chưa có trên repo** (phiên P-2210 đang ghi song song); bản hiện có: "(f) Công bố: bật khai báo nội dung AI trên YouTube; mô tả §10.6 viết lại theo N1/N2…". CONG-BO-1 viết theo lệnh + (f) hiện có.
- **YouTube Help** <https://support.google.com/youtube/answer/14328491?hl=en>, đọc **22/10/2026 04:28:19 UTC** (HTTP 200; bản chữ `do/youtube-help-genai-2026-10-22.txt`). Trang nay mang tiêu đề **"Disclosing use of GenAI content"** (lệnh gọi tên cũ "Disclosing use of altered or synthetic content"). Điểm dùng: "We require creators to disclose AI-generated or altered content that seems realistic"; khai ở YouTube Studio → Attributes → **"AI use" Yes/No**; "Labels may appear in the expanded description for … AI content that is non-photorealistic or animated"; nội dung có C2PA có thể bị gắn nhãn tự động; "Cloning one's own voice to create voice overs" không phải khai (giọng ElevenLabs của kênh không phải giọng chủ dự án → lệnh vẫn tính là giọng tổng hợp).
- `reports/m3/BAI-HOC-LL.md`: không đọc (quy tắc dành cho phiên P).

## 2. Luật đổi (1.17.2) — tên, trường đọc, ngưỡng, mức, căn cứ
Chỉ tập từ T3 (`khung_sach` | `kenh2_tu_t3`). Tập trước T3: không đổi (selftest k115/k114 giống hệt; `q_k117.check` trả KHÔNG ÁP; `q_lai.ap_dung` không nhận log shot khi tập trước T3).

**Đọc đoạn AI khai trong log shot (`q_k117.doan_ai`, V2-D5)** — dùng chung cho MINH-HOA, K-LAI, CONG-BO-1: shot `minh_hoa: true` (cả shot) | `minh_hoa: [{ma, t0, t1, so_ai?, luot?, kiem?, agl_m?}]` (giây trong shot; `[]` = không đoạn; mục `minh_hoa: false`/`ai_image: false` bị bỏ) | shot `ai_image: true` không có mục đoạn (cả shot) | log khung `lai.log_khung` (ưu tiên khi có). Mục đoạn ở shot `ai_image: false` = **mâu thuẫn khai** → K-LAI-2 (b).

| Luật | Đổi | Trường đọc | Ngưỡng | Mức | Căn cứ |
|---|---|---|---|---|---|
| **MINH-HOA** | theo đoạn; bỏ (b) nhãn | đoạn; `goc`; `agl_m` mục đoạn → `agl_m[i]`↔`cam[i].t`; `so_ai` mục/shot hoặc tệp `so_ai:` (khớp `shot`/`doan`/`ma`, `tag` = `luot`, hoặc `tag` "<mã>-…"); sổ nhận `model`/`model_req`/`model_resp`, `prompt`/`lenh`, `sha_ra`/`sha256`/`output.sha256` | (a) ≤ 20 % · (c) khung trước + sau đoạn là 3D (cao/thap/neo), không trong đoạn khác · (d) ≤ 40 m AGL · (e) sổ đủ model + lệnh + SHA ra | Chặn G2 · Cảnh báo animatic (không đổi) | §14.1 (c); quyết định 22/10 11:09; V2-D5 |
| **SACH-1** | không đổi | — | — | — | lệnh |
| **K-LAI-1** | không log khung → đoạn khai + shot `ai_image` | log shot | ≤ 20 % | Chặn (P2-2) | §14.1 (d); V2-D5 |
| **K-LAI-2** | (a) cờ `ai_image` mọi shot log khi không log khung; (b) + mâu thuẫn khai; **(c) bỏ** | log shot, log khung, mô tả | 0 | Chặn | quyết định 22/10; V2-D5 |
| **K-LAI-3** | + kiểm từng đoạn minh hoạ | `kiem` của mục đoạn hoặc `lai.kiem_minh_hoa.{mã}`; `ket_luan_may.ket_qua`, `loi_mo_hinh` | ĐẠT, 0 lỗi mô hình, không chấm mù | Chặn | §14.1 (e) |
| **K-LAI-4/5/B** | chỉ minh hoạ → KHÔNG ÁP có lý do; shot `ai_image` không đoạn, không `lai:` → THIẾU | — | — | như cũ | minh hoạ toàn khung không có khung A/tấm C để so |
| **K-LAI-6** | sổ minh hoạ (`so_ai:` / `lai.goi_api`), chuẩn hoá sổ Gemini V2 | model_req/resp, prompt ≥ 40 ký tự, usage, usd, c2pa (`{co_manifest}` → bool), date_utc, file/sha256 (`output`), mặt nạ = "toàn khung" | đủ trường | Chặn | §14.1 (e) "sổ AI ghi mọi lệnh gọi" |
| **PP-1 (d)** | nguồn/bản đồ + chỗ ước tính; bỏ AI | chữ thẻ PP | có cả hai | Chặn (a)–(d) | quyết định 22/10; không thêm luật cấm chữ |
| **CONG-BO-1** | mới | khung AI (đoạn, `ai_image` log shot/log khung/đặc tả) hoặc giọng (`giong_tong_hop`, `vo`/`voice`.`tong_hop`/`synthetic`/`engine`/`nguon`/`model` ~ elevenlabs/tts/synthetic); `phat_hanh.mo_ta`; `phat_hanh.youtube_altered_content`; cổng `cong: phat_hanh` \| `phat_hanh.goi: true` | (a) câu mô tả có "AI"/"synthetic" · (b) cờ = true | **Chặn ở gói phát hành**; Cảnh báo ở animatic/G2 | §14.1 (f); YouTube Help (§1) |
| **TL-1 (c)** | cắt góc R3 không tính trần; in số thô | `so_goc` \| `goc_may` (có `t` → khớp ±0,5 s) | mỗi shot miễn ≤ (số góc − 1) cắt trong shot (cách ranh > 0,5 s); trần ≤ 5/phút trên số tính trần | Cảnh báo | V2-D7 |
| **EO-DAT-R1** | chỉ báo mọi cổng; + vùng nở | `chu_the_mat_na` (K đo) \| `chu_the_pct_no`; `chu_the_pct` | nở đĩa bán kính 1,5 % bề ngang; (a) < 15 %, (b) 15–20 % vẫn xét pixel thô | Chỉ báo (Cảnh báo) | V2-D2 |

Ghi chú định nghĩa (K chọn, nêu ra để duyệt — §6): `cat_trong_shot` của log V2 **không** được coi là khai R3 (lệnh nêu `so_goc`/`goc_may`; `cat_trong_shot` lẫn cả ranh đoạn minh hoạ H1, N1.4, C5). CONG-BO-1 không tính `ai_texture` (lệnh nêu "đoạn minh hoạ/ai_image"). N2P-6 (T4) vẫn đếm `minh_hoa` theo shot — ngoài phạm vi lệnh.

## 3. Selftest
### 3.1 Kết quả (cây 1.17.2 đã khoá; tệp `do/selftest-*-1.17.2.txt`)
| Bộ | 1.17.1 | **1.17.2** | Ghi chú |
|---|---|---|---|
| `selftest_k1172.py` (mới) | — | **74/74** | MINH-HOA 17, cấp 7, V2-D5 7, K-LAI 16 (1 / 1-2 / 2-4 / 3-3 / 4/5/B-1 / 6-3 / áp 3), PP-1 4, CONG-BO-1 9, TL-1 7, EO-DAT-R1 4, SACH-1 1, áp dụng 2. Mọi luật đổi có ≥ 1 ca đạt + ≥ 1 ca trượt |
| `selftest_k117.py` | 130/130 | **130/130** | 6 ca đổi kỳ vọng (§3.2); còn lại giống hệt |
| `selftest_k116.py` | 144/144 | **144/144** | 2 ca đổi kỳ vọng + chữ giá trị TL-1 thêm "(thô)" |
| `selftest_k115.py` / `k114` | 105/105 · 126/126 | **105/105 · 126/126** | `diff` đầu ra: **0 dòng khác** |
| `k113` / `k1122` / `k1121` / `k112` / `k2` / `ll` | — | 64/64 · 37/37 · 48/48 · 75/75 · 129/129 · 317/317 | `ll` dùng `claude` giả của bộ kiểm, không mạng |

Ca dữ liệu thật (`fixtures/k1172/`: log shot V2 rút gọn + sổ Gemini nguyên văn): `doan_ai` ra đúng **H1/M5, N1_4/M3, C3/M2, C5/M4 = 28,4 s** (khớp báo cáo V2 §5) và **C4/M1 mâu thuẫn**; MINH-HOA (a)(c)(d) sạch; (e) ×4 khi chưa nối sổ, **sạch khi nối `so-ai-gemini.jsonl`**; K-LAI-6 sạch với sổ Gemini thật.

### 3.2 Kỳ vọng cũ đã đổi (đúng chỗ quyết định 22/10 — không phải luật hỏng)
- k117 MINH-HOA (b) ×4: "nhãn sai chữ", "nhãn 2–10 s", "không log chữ/không trường nhãn → THIẾU", "nhãn tắt từ 45,8 s" — trước **bắt lỗi**, nay **sạch** (bỏ nhãn bắt buộc).
- k117 cấp EO-DAT-R1 ×2: "12 % ở G2 → Chặn", "thiếu ở G2 → Chặn" — nay **chỉ báo, không Chặn** (V2-D2).
- k116 PP-1 "không nói AI → (d)" và K-LAI-2 "thẻ PP không nói AI → (c)" — nay **sạch**. Ca trượt mới của PP-1 (d) (thiếu nguồn; thiếu ước tính) ở k1172.

## 4. Chạy k2check trên animatic v2 — 1.17.1 ↔ 1.17.2
**Cách chạy (thư mục tạm, không ghi vào repo đầu vào):** đặc tả + log shot + nhịp + lời khoá + claims từ `git show origin/k2c-t3-anim-v2:…`; **timeline tổng hợp từ đặc tả** (`do/mk_tl.py`: đoạn nối theo `dur`, shot theo `at`; 760,9998 s — timeline prep của k2v ở container phiên dựng đã mất); video TL-1 = ghép 8 tệp `xem/` 640×360 (761,125 s; master 960×540 ngoài git đã mất); `--no-asr --cap`. 1.17.1 chạy từ `git archive 39d01859 checks` (+ RIGHTS.md) — LOCK KHỚP. Bảng đầy đủ: `do/k2check-v2-1.17.1.md`, `do/k2check-v2-1.17.2.md`.

| Hàng | 1.17.1 | 1.17.2 | Lý do đổi |
|---|---|---|---|
| **MINH-HOA** | **TRƯỢT** (Chặn 18): 5 "đoạn" = cả shot H1, N1_4, C3, C4, C5 = 66,1 s (8,7 %); (b) THIẾU ×5; (c) ×4 (kẹp theo shot; H1 đầu phim); (d) ×4 (AGL cả shot 52–427 m); (e) ×5 | **TRƯỢT** (Chặn 4): 4 đoạn M5, M3, M2, M4 = **28,4 s = 3,7 %**; (c) 0; (d) 0 (7 · 2 · 4 · 22 m); **(e) ×4**: episode.yaml chưa khai `so_ai:` / đoạn chưa có `luot` | đo theo đoạn; bỏ nhãn; C4/M1 tách ra (mâu thuẫn) |
| **K-LAI-1…6** | 1 hàng **ĐẠT/KHÔNG ÁP** "tập không có khối lai / shot AI" (lỗi luật V2-D5) | K-LAI-1 **ĐẠT** 3,7 % · K-LAI-2 **TRƯỢT** (b) C4/M1 + (d) không mô tả · K-LAI-3 **TRƯỢT** thiếu tệp kiểm ×4 · K-LAI-4/5/B **KHÔNG ÁP** (minh hoạ toàn khung, có lý do) · K-LAI-6 **TRƯỢT** thiếu sổ · K-LAI-3V KHÔNG ÁP | V2-D5 |
| **PP-1** | CẢNH BÁO (e) 3,6 từ/s ×2; (d) đạt | CẢNH BÁO (e) ×2; (d) đạt (không còn đòi AI) | thẻ PP2 V2 vẫn có câu AI — hợp lệ, không cấm chữ |
| **TL-1** | CẢNH BÁO: video 67 cắt = 5,40/phút; (d) trôi máy (như nhau) | CẢNH BÁO: **5,40/phút (thô) − 0 cắt góc R3 = 5,40 tính trần** | log V2 chưa khai `so_goc`/`goc_may` |
| **EO-DAT-R1** | ĐẠT/KHÔNG ÁP (không shot `chu_the_eo_dat`) | như cũ | log V2 chưa khai `chu_the_eo_dat` |
| EO-DAT-R2 / R3 / R4 | TRƯỢT (thiếu `trong_pct` ×18) / TRƯỢT (thiếu `so_goc` + khoảng biến cố) / KHÔNG ÁP | giống hệt | không đổi luật |
| **CONG-BO-1** | — | **CẢNH BÁO** (cổng G2): (a) không `phat_hanh.mo_ta`, (b) không `youtube_altered_content` | luật mới; chưa phải gói phát hành |
| LOCK | ĐẠT 1.17.1 | ĐẠT 1.17.2 | |
Hàng khác ngoài danh sách: chỉ **Q32** khác (1.17.1 báo "(e) không đọc được cây git" vì cây 1.17.1 nằm trong thư mục tạm không phải repo git — sản phẩm của cách chạy, không phải đổi luật). Mọi hàng khác giống hệt.

### 4.1 Việc log V2 cần thêm để các hàng đo được (cho phiên dựng/đóng gói — K không sửa)
1. Bỏ mục đoạn M1 ở C4 (giữ 3D) **hoặc** đặt `ai_image: true` nếu có dùng — hiện là mâu thuẫn khai.
2. Mỗi mục đoạn: `luot` (`M5-l3`, `M3-l1`, `M2-l3`, `M4-l1`) + `kiem: reports/animatic-t3-v2/omni/kiem/<lượt>/<lượt>-kiem.json`; episode.yaml `so_ai: …/so-ai-gemini.jsonl`.
3. `giong_tong_hop: true` (giọng G1 ElevenLabs) và ở gói phát hành: `phat_hanh: {mo_ta, youtube_altered_content: true, goi: true}`.
4. `so_goc`/`goc_may: [{id, t}]` cho shot cắt góc R3; `trong_pct`, `chu_the_eo_dat` + `chu_the_mat_na` cho shot eo đất.

### 4.2 TL-1 nếu log khai R3 (đo trên video ghép, `do/tl1-cat-v2.json`)
20 mốc `cat_trong_shot`: 13 cắt góc (N1.5 ×2, N1.6 ×2, C1, N2.10, N2.11 ×2, N3.1, N3.4, N4.1, N4.2, N5.4) **đều khớp cắt video ±0,5 s**; 5 khớp là ranh đoạn minh hoạ (H1 4,5 s, N1.4 3,5 s, C5 6,1 s, C4 2,0 / 9,0 s). Nếu 10 shot cắt góc khai `so_goc` → miễn 13 → **(67 − 13) / 12,42 phút = 4,35 cắt/phút ≤ 5**.

## 5. LOCK
- **Cũ:** 1.17.1 `b741f617d7b2275e4039cd16eb8e967cbc99801f508090631146590bb1bc16fe` (2026-10-21T16:05:00Z).
- **Mới:** **1.17.2 `aca05e600a51f740c900f5854df47eb730f156c09d62df307d3a31f3b79c6d60`** (DATE_UTC 2026-10-22T04:50:31Z). `python3 -I checks/lock.py --verify` → **KHỚP** (ngay sau khoá; trong k2check hàng LOCK; trong preflight mỗi commit).

## 6. Quyết định đề xuất
| # | Đề xuất | Ưu | Nhược | Tác động | Rủi ro |
|---|---|---|---|---|---|
| **K1172-D1** | Đoạn khai ở shot `ai_image: false` = mâu thuẫn, báo **K-LAI-2 (b) Chặn**, không đếm vào MINH-HOA | Bắt đúng lỗi log C4/M1; số minh hoạ khớp thực tế (28,4 s) | Phiên dựng phải sửa log | log V2 → bản cuối | Nếu chủ dự án muốn đếm "an toàn" (đếm cả M1) thì (a) tăng 7 s — vẫn ≪ 20 % |
| **K1172-D2** | TL-1 chỉ miễn khi khai `so_goc`/`goc_may`; **không** nhận `cat_trong_shot` | Đúng chữ lệnh; tách cắt góc R3 khỏi ranh minh hoạ | V2 phải khai thêm trường | TL-1 V2: 5,40 → 4,35 khi khai | Thấp |
| **K1172-D3** | EO-DAT-R1 (a)/(b) vẫn xét **pixel thô**, vùng nở chỉ in kèm (chưa đổi định nghĩa 15–20 %) | Không đoán thước khi chủ dự án đang chấm bằng mắt | Hai số có thể kể chuyện khác nhau | R1 chỉ báo | Không — R1 không vào mã thoát |
| **K1172-D4** | CONG-BO-1: cổng gói phát hành nhận diện bằng `cong: phat_hanh` hoặc `phat_hanh.goi: true`; giọng tổng hợp bằng `giong_tong_hop` / `vo.engine`…; không tính `ai_texture` | Đo được, không đoán | Thêm trường khai | gói phát hành T3 | Quên khai cổng → chỉ Cảnh báo (lọt Chặn); nếu muốn tính cả vân AI thì thêm 1 điều kiện |
| **K1172-D5** | MINH-HOA (e) khớp sổ theo `tag` "<mã>-…" khi đoạn không khai `luot` | Đọc được sổ Gemini thật ngay | Có thể khớp nhầm lượt bị loại (đều có model/prompt/SHA) | (e) | Thấp; khai `luot` thì khớp đúng lượt |
| **K1172-D6** | N2P-6 (T4) đếm minh hoạ theo đoạn như MINH-HOA (làm ở phiên K sau) | Nhất quán T3/T4 | Ngoài lệnh này | T4 | Hiện N2P-6 đếm cả shot nếu log T4 dùng danh sách đoạn |

## 7. Chi phí thật
| Khoản | Mốc / chặn | Thật |
|---|---|---|
| Claude API | $3 / $10 | **$0** (không gọi; token của chính phiên không đo được trong container — ước lượng dưới mốc) |
| OpenAI | $1 | **$0** |
| Gemini / ElevenLabs / RunPod / YouTube API | 0 | 0 / 0 / 0 / 0 (trang YouTube Help tải bằng HTTP thường, không phải API) |
| Giờ máy | 3 h | **≈ 0,75 h** (11 bộ selftest × 2 lượt, 2 lượt k2check ≈ 45 s mỗi lượt + nháp, đo cắt video) |

## 8. Preflight
`set -o pipefail; bash tools/preflight.sh` trên tệp stage trước mỗi commit; chỉ commit khi có cả `preflight: … — ĐẠT` và `PREFLIGHT ĐẠT`. Commit mã `0af47b37`: "preflight: 13 tệp (staged) — ĐẠT", lock KHỚP. Commit báo cáo: ghi trong thân commit. Hook git không cài (như K-1.17.1).

## 9. Tệp đã sửa
| Tệp | Việc |
|---|---|
| `checks/ll/q_k117.py` | `doan_ai`, MINH-HOA theo đoạn (bỏ (b)), `_agl_doan`, `_so_ai_rows`, `_dong_ok` tên trường thật; EO-DAT-R1 vùng nở (`vung_no`); CONG-BO-1 (`co_ai`, `giong_tong_hop`, `cong_bo1`, `cong_cb`) |
| `checks/ll/q_lai.py` | `ap_dung(E, LS)`, `log_ai`, `klai1_log`, `klai3_mh`, `so_ai_tap`, `_norm_mh`; `check116` nhận LS |
| `checks/ll/q_k116.py` | PP-1 (d); K-LAI-2 (a)(b), bỏ (c); TL-1 `cat_r3`, `_n_goc`, số thô + số tính trần |
| `checks/ll/cap112.py` | EO-DAT-R1 chỉ báo; CONG-BO-1 Chặn chỉ ở `phat_hanh` |
| `checks/ll/k2check.py` | truyền log shot cho K-LAI; hàng CONG-BO-1; chữ ngưỡng |
| `checks/ll/selftest_k1172.py`, `fixtures/k1172/` | bộ mới + SAO dữ liệu thật V2 |
| `checks/ll/selftest_k117.py`, `selftest_k116.py` | 8 kỳ vọng đổi (§3.2) |
| `checks/ll/RULES-LL.md` | mục 1.17.2 + ghi chú tại chỗ ở 1.17.0/1.16 + tự kiểm |
| `checks/cinecheck/__init__.py`, `checks/LOCK` | 1.17.2 |
| `reports/k1172/` | báo cáo này + `do/` |

## 10. Chỉ số trong ±5 % quanh ngưỡng (luật cứng)
**Dữ liệu thật (animatic v2, 1.17.2):** chỉ **CHUONG-1** 5 thẻ chương đúng **3,0 s** = trần 3 s (đã có từ V2, không do phiên này). Không có chỉ số MINH-HOA/K-LAI/TL-1/CONG-BO-1 nào trong ±5 %: minh hoạ 3,7 % (trần 20 %), AGL lớn nhất 22 m (trần 40 m), TL-1 5,40/phút (**+8 %** trên trần 5 — ngoài ±5 %, Cảnh báo).
**Ca selftest đặt đúng ngưỡng:** MINH-HOA đúng 20 %; TL-1 sau miễn 3,33/phút; PP-1 thẻ 8 s.
**Không thêm phần tử nào để vượt ngưỡng.**

## 11. Dòng sổ đề xuất (phiên P ghi — phiên này không sửa sổ)
- **COST-LEDGER.csv:** `K-1.17.2,"MINH-HOA theo đoạn + bỏ nhãn, K-LAI đọc log shot (V2-D5), PP-1 (d), CONG-BO-1, TL-1 R3 (V2-D7), EO-DAT-R1 chỉ báo (V2-D2); LOCK 1.17.1 b741f617 → 1.17.2 aca05e60",K,2026-10-22,,,,,0,3,—,0,0,0.75,,0,,,reports/k1172/K1172-BAO-CAO.md,"API 0; token phiên chính không đo được"`
- **RIGHTS.md / AUTHORSHIP.md:** không tài sản mới. Fixture `checks/ll/fixtures/k1172/` là SAO log + sổ AI nội bộ của dự án (không phải tài sản phim).

## 12. Việc chờ chủ dự án
1. Duyệt **K1172-D1…D6**; quyết đang treo từ trước: K117-D1, D3–D8, K1171-D1…D4.
2. Phiên P: ghi Kinh thánh §14.1 (f) bản sửa 22/10 (K đã viết CONG-BO-1 theo lệnh + bản (f) hiện có); merge `checks-1-17`, `checks-1-17-1`, rồi `checks-1-17-2` khi duyệt (nhánh này **không** merge); ghi sổ theo §11.
3. Phiên dựng/đóng gói T3: khai thêm các trường §4.1 (đặc biệt sửa C4/M1, nối sổ AI + tệp kiểm, `so_goc`/`goc_may`, khối `phat_hanh` với `youtube_altered_content: true`, `giong_tong_hop: true`).

**DỪNG — chờ chủ dự án.**
