**Nhánh thật: `ccr-196e0bda-gcj9iw`** (harness buộc tên này; lệnh ghi `checks-1-17-9`). Gốc origin/main **@41de7ce3** (đỉnh đúng như lệnh; LOCK 1.17.8 `045b7bb7…` KHỚP). Không merge, không đụng `main`, P-2610c, `docs/`, sổ, `channel-k2/**`, `scripts/`, `design/`, `tools/` hay nhánh khác. Đầu vào A @bc1693b5 chỉ ĐỌC (`git archive` → `/var/tmp/k1179/in`).

# Phiên K-1.17.9 — xét khiếu nại BAN-CUOI-T4-A (KN-1, KN-2, KN-4…KN-7; KN-3 rút) + KN-8 (điều phối) — BÁO CÁO

> Phiên K, 26/10/2026 03:12 → ≈ 05:05 UTC (10:12 → ≈ 12:05 Asia/Saigon). Mọi số là số đo thật trong phiên; tệp số đo ở `reports/k1179/do/`.
> Căn cứ (nguyên văn, Asia/Saigon): chủ dự án 26/10 07:39 chọn hướng (a) cho H3-05b (→ KN-7); chủ dự án dán lệnh phiên này = **"Duyệt PHIẾU-A theo khuyến nghị điều phối"** — giờ dán ghi theo giờ mở phiên: **26/10 ≈ 10:12 Asia/Saigon (03:12 UTC)**; 26/10 00:07 "Chọn hướng cho cảnh hiện đại: A+B+E (khuyến nghị)"; 25/10 09:08 "…các vấn đề khác đều có thể nới…".
> Phiên K KHÔNG có văn bản "khuyến nghị điều phối" cho PHIẾU-A (không nằm trong đầu vào được giao) → không suy ra lựa chọn E1/Q-A… nào đã duyệt; mọi ngoại lệ trong phiên là **khai thử**, không phải duyệt thật (§2 KN-1).
> Email chủ dự án không có trong tệp, commit, header, URL, payload hay User-Agent nào (UA `CineLab-research (+https://github.com/HungQuach301/cine-lab)`). Không in/ghi khoá (proxy gắn khoá).

## 0. Khối điều lệ và tóm tắt
| Trường | Lệnh | Thực tế |
|---|---|---|
| Nhánh | `checks-1-17-9` từ origin/main @41de7ce3 | harness buộc `ccr-196e0bda-gcj9iw` (dòng đầu); gốc đúng @41de7ce3 |
| Vùng sửa | `checks/**`, `checks-appeal.md`, `reports/k1179/**` | đúng |
| Khiếu nại trước phán quyết | — | chép nguyên văn KN-1…KN-7 + KN-8 vào `checks-appeal.md` commit `747ab420` 03:17 UTC, trước mọi phán |
| Preflight / hook | `set -o pipefail`; commit chỉ khi "— ĐẠT"; hook trước lần đẩy đầu | hook pre-commit + pre-push cài 03:13 (lần đẩy đầu 03:17); `day.sh` kiểm "— ĐẠT" + "PREFLIGHT ĐẠT" trước commit |
| `lock.py` không `--verify` | đúng một lần, bước khoá | **đúng một lần** 03:54:51 UTC → `9eddaf24…`; preflight quét `checks/` trước khoá (bắt 1 email giả trong selftest — sửa trước khoá) |
| Đẩy ≤ 30 phút + CHECKPOINT | bắt buộc | `reports/k1179/CHECKPOINT.md`; 9 lần đẩy; **một lần trễ 1 phút**: 04:23 → 04:54 = 31 phút (chờ T3/cinecheck — §11) |
| Force/amend/dừng hỏi | không | không |
| Chi phí | Claude mốc $3 (chặn $8), OpenAI mốc $2 (chặn $5), Gemini 0, không sinh ảnh/video | **OpenAI $0,313 · Claude API $0,699 · Gemini 0 · 0 ảnh/video sinh** (§10) |

**Tóm tắt phán quyết:**
| KN | Phán | Một dòng |
|---|---|---|
| KN-1 | **MỘT PHẦN — LỖI LUẬT** | `ngoai_le` + `duyet_chu_du_an` hạ báo MÔ HÌNH "bờ" xuống (w) khi máy sạch; máy không miễn |
| KN-2 | **MỘT PHẦN** | beats `bien_co_tl` tự khai GIỮ LUẬT; LỖI LUẬT nhỏ: cộng biến cố ĐO từ log máy (mặt trời, pha máy) — Q37 vẫn trượt vì **nhịp thật** (39 khoảng > 6 s) |
| KN-4 | **LỖI MÃ** (cat_clip) · GIỮ LUẬT (lọc trời) | H1-15b trong `cat_clip` 0,062 → hết (a) |
| KN-5 | **LỖI LUẬT** | "toà có tên" = tháp ≥ 75 m ODN / lịch sử (`nguon_lich_su`) / St Paul's |
| KN-6 | **MỘT PHẦN** (chấp nhận có điều kiện) | đẩy/trượt 2D ≤ 1,5 %/s = MỘT phép 2D cả khung; (a)-E khác quỹ đạo → (h) |
| KN-7 | **CHẤP NHẬN** (chặt thêm: tính cả hộp 0,60–0,75) | H3-05b: YuNet 0,070, 4 nơi đã tra, AUTHORSHIP 00:12 → miễn (k) |
| KN-8 | **MỘT PHẦN** (sửa cách giữ bờ; T9c không làm thước) | nước AI + bờ PHÍA ĐẤT; dải ±8 px cả hai phía → viền xanh; mô hình bắt 2/2 ca âm, 0 nhầm |

LOCK **1.17.8 `045b7bb7…` → 1.17.9 `9eddaf24e8c5276b6017af172e7c8185ba21831a7b6e842cc17094fd5c66fc34`**, `--verify` KHỚP. Selftest **k1179 50/50**; cũ k112…k1178, k2, ll đạt trên cây đã khoá — 0 SAI, 0 kỳ vọng cũ đổi (§5). T3 1.17.8 ↔ 1.17.9: **giống hệt** (59 hàng; diff chỉ khác tiêu đề và nhãn phiên bản hàng LOCK).

## 1. Đầu vào, cách tái hiện, tiêu chí (đặt TRƯỚC khi đo)
- **Đầu vào A (CHỈ ĐỌC):** `git archive bc1693b5 reports/ban-cuoi-t4-a channel-k2/k2c-t4-02 | tar -x -C /var/tmp/k1179/in` (590 MB; tái tạo được từ git — không giữ riêng ở /var/tmp). SHA nguồn chính: `khieu-nai-K.md` `d5184aea…`, `PHIEU-A.md` `df0ad341…`, `BAN-CUOI-T4-A-BAO-CAO.md` `42666c87…`, bảng k2check đặc tả v4 `795e7585…`. AUTHORSHIP.md của main @41de7ce3 (`d5ced1b2…`) đặt vào gốc đầu vào cho KN-7 (dòng 26/10 00:12 do P-2610b ghi SAU khi nhánh A tách — phiên B merge main sẽ có).
- **Tấm E: bộ đệm mô hình nhìn TÁI TẠO, 0 API** (`do/e_k2.py`): khoá tính bằng chính hàm checks (`q_n2p_vision.khoa_de` + `q_k1178.PROMPT_E` điền danh sách mốc) từ câu trả lời thô `e/kiem/<tấm>/vision/*.raw.txt` trong git. 1.17.8 (worktree @41de7ce3, LOCK KHỚP) trên 8 tấm → **trùng bảng phiên A** ở N2P-1…4, N2P-E. Khác lượt A (nêu rõ, như nhau ở hai phiên bản): video đối chứng `*-tl-render.mp4` ngoài git → bỏ `n2p.video` (N2P-5 "chưa đo"); bộ đệm q_thoi_dai không vào git → N2P-2 (b) không chạy.
- **Đặc tả v4 (chế độ animatic):** k2check 1.17.8 chạy lại trên đầu vào = **0 hàng khác** bảng phiên A (`dac-ta-v4/k2check-1.17.8-dac-ta-v4.md`).
- **Tiêu chí:** luật đo được trên đường dựng thật; không nới ngưỡng chủ dự án đặt; máy (N2P-1 (a), T9b, T9c, YuNet) không bao giờ được miễn bằng khai; mọi miễn cần duyệt chủ dự án có dấu vết; không khai → hành vi 1.17.8; mỗi luật ≥ 1 ca thật + ≥ 1 ca âm.

## 2. Phán từng khiếu nại (số đo)
### KN-1 — ngoại lệ "bờ" của mô hình trên tấm E — **MỘT PHẦN · LỖI LUẬT**
- Tái hiện E-P9-ngay-l1-thap (1.17.8): N2P-1 (b) GPT «projecting dark quay or pier surface…» @[0,0; 0,972; 0,078; 1,0] + N2P-3 (b) @[0,0; 0,975; 0,075; 1,0] → 2 Chặn G2. Claude: 0 báo ở góc đó (chỉ một báo "dải nước xa" do_tin 0,3 < 0,5). **Máy:** N2P-1 (a) 0/255, T9b 0,00 %, T9c 0 đoạn/0,0 px.
- Đo hộp: 4 500 điểm @1080, trong đó lớp nhà thường 3 697, 'bang' 615, **'nha' 235 = 307 (6,3 % hộp nằm trong lõi (a)-E)** — mẩu kè máy đã khoá 0/255. Cùng hộp ở mặt nạ "đủ" và "tháp" giống hệt → GPT không báo ở tấm "đủ" là do mô hình dao động, không phải ảnh khác.
- K1178-D2 phương án A ("người đọc ghi `ngoai_le`") không có đường máy đọc được → **LỖI LUẬT, sửa** (khuôn §3). Khai thử trên đúng tấm này (KHÔNG phải duyệt thật): N2P-1 TRƯỢT → CẢNH BÁO (còn (c) cụm dải 20 px), N2P-3 TRƯỢT → **ĐẠT**, N2P-E 2 dòng (w) "ngoại lệ chủ dự án duyệt (KN-1)". Phương án B tự động không làm (1 ca thật — không đủ đáp án).
### KN-2 — Q37 / NHIP-K2 / Q37 (1.13) trên T4 — **MỘT PHẦN**
- Tái hiện: biến cố khai 143 (gộp 134), TB 5,75 s, dài nhất 20,17 s (H2-03b DAY 1667,05 → 1667,45).
- (B) beats `bien_co_tl` tự khai mỗi 4 s — **GIỮ LUẬT**: biến cố tự khai không được nhận (A4 1.17.7); năm chạy là đồng hồ chạy (I8 1.15 chỉ nhận đồng hồ DỪNG).
- **LỖI LUẬT nhỏ, sửa:** I8 đo biến cố cảnh tl từ campath của T3 nhưng không đọc log máy T4 → 1.17.9 cộng biến cố ĐO từ log máy. Số đo trên log máy thật (`do/kn2-q37-log.json`, 63 shot có log):

| Biến cố cộng thêm | số | TB (s) | dài nhất (s) | khoảng > 6 s |
|---|---|---|---|---|
| không (1.17.8) | — | 5,75 | 20,17 | 46 (đếm từ beats khai) |
| (n1) mặt trời qua 0°/−6° | 25 | 5,32 | 20,17 | — |
| (n2) pha máy đứng↔chạy | 17 | 5,43 | 20,17 | — |
| **(n1)+(n2) = luật 1.17.9** | 42 | **5,04** | **20,17** | — |
| + (n3) `fire` ±10 % (chưa hiệu chuẩn — KHÔNG nhận) | +188 | 3,03 | 20,17 | **39** |
| cận trên: + mỗi lần năm nhảy (KHÔNG nhận) | +560 | 1,78 | 20,17 | — |

- Kết luận: kể cả cộng mọi thứ đo được, (c) vẫn trượt ở **39 khoảng > 6 s** — M00 17,0 s, M01 17,9 s, H2-03b 20,2 s, H5-07b 15,3 s, H1-06 14,9 s, H5-08 14,0 s, H3-05 12,7 s… → **LỖI PHIM (nhịp thật)**, khớp nhận xét chủ dự án 25/10 06:56 "10 giây đầu gần như đứng". Không ép thêm cắt (luật cứng); quyết định ở K1179-D3. (A) hiệu chuẩn BIEN-CO-V: chưa có master 1080p — giữ K1178-D4.
### KN-4 — YuNet mặt giả trên trời/tán cây; `cat_clip` — **LỖI MÃ (sửa) · GIỮ LUẬT phần lọc trời**
- Máy K (`q_k1177.do_mat`, mỗi 2 khung, gốc 640×360) trên `H1-15b-l1-360p` (SHA trong `do/yunet-H1-15b-l1-360p.json`): cả clip điểm ≥ 0,75 **0,162** (khung 124, điểm 0,77, hộp chạm mép trên — trời); 7 hộp > 1/8, **mọi hộp ở khung ≥ 118**. Trong `cat_clip` [0, 110]: **0,062** (≥ 0,75) / 0,067 (≥ 0,60) → hết (a) và (w).
- Không thêm luật lọc trời/tán cây: 1 ca; mức 0,60–0,75 đã là (w) người soi; ngưỡng 0,75 hiệu chuẩn 23 clip (1.17.7).
### KN-5 — "toà có tên" cho LUẬT E — **LỖI LUẬT, sửa**
- Căn cứ 00:07 "toà THÁP có tên ghép lại từ 3D"; chữ 1.17.8 "toà có tên OSM" rộng hơn. Đo (`toa.json`/`toa-thap.json` phía A, k2check): P9 151 toà có tên → 7 đỉnh ≥ 75 m + 2 lịch sử + St Paul's = 10; (a)-E **13,88 → 5,74 %**; P1 247 → 10 + 6 + St Paul's = 17; **38,11 → 28,36 %** (sông 22,03 % vẫn trong (a)-E — KN-8).
- Ghi kèm: danh sách lịch sử của phía A khớp theo tiền tố → nhận cả "Guildhall Art Gallery" (toà mới, không phải công trình lịch sử) → theo 1.17.9 phải khai `nguon_lich_su` hoặc hạ nhà thường. Trường `nguon` trong toa.json phía A là nguồn MẶT NẠ ("OSM name (look3e)") — không thay `nguon_lich_su`.
### KN-6 — đẩy/trượt 2D ≤ 1,5 %/s trên tấm E — **MỘT PHẦN (chấp nhận có điều kiện)**
- Căn cứ: §19 (c) ảnh thật ≤ 1,5 %/s (đề xuất của A dựa vào). Rủi ro chính: lớp (a)-E 3D có thị sai so nền AI phẳng → lớp trượt trên nền. Điều kiện K: chuyển động = MỘT phép 2D cho CẢ tấm ghép (máy 3D giữ CODINH — MAY-19 (b) đo log như cũ); đo trên video ghép (§3).
- Số đo (video tổng hợp từ tấm P9 thật 640×360, `do/kn6-day2d.json`): đẩy 1,0 / 1,5 / 3,0 %/s → đo **1,014 / 1,505 / 2,972**; (a)-E lệch quỹ đạo 1,0 vs 0 %/s → sai sau bù 13,26 > 5,42 (h); 1,0 vs 0,8 → 4,07 > 3,0 (h); 1,0 vs 0,9 → 1,71 (≈ 0,6 px mép — không thấy được) → qua. **1,505 sát ngưỡng 1,5 (+0,3 %)** → thêm sai số đo 2 %. Chưa có video E thật có đẩy để kiểm — luật có sẵn, chưa dùng ở bảng v4.
### KN-7 — NHAN-VAT-TEN (k), không có chân dung — **CHẤP NHẬN (chặt thêm một điều)**
- Máy K trên `H3-05b-l1-360p` (SHA `0a87b9e1…` theo phiên A; tệp đo `do/yunet-H3-05b-l1-360p.json`): điểm ≥ 0,75 **0,0699**, ≥ 0,60 **0,0704**, 0 hộp > 1/8 (144 khung, 85 hộp/72 khung đo). Số của phiên A (0,1025 @ điểm 0,569, có phóng ×2) dưới ngưỡng mô hình của K — không dùng.
- Luật theo nguyên văn lệnh chủ dự án 07:39; K chặt thêm: tính cả hộp 0,60–0,75 (không có chân dung thì không nhận cả hộp nghi), và `duyet_chu_du_an` phải trỏ dòng AUTHORSHIP có cùng ngày, giờ, mã shot.
- Đặc tả v4 (1.17.9): **H3-05b (k) miễn** — "không có chân dung (4 nơi đã tra), YuNet ≤ 0,070 ≤ 1/8, AUTHORSHIP 2026-10-26 00:12". Ca âm thật: H1-15b không cắt + `chan_dung: khong_co` → (k) giữ + (a) giữ. Ghi: danh sách "chưa tra" (NPG, St Paul's, Commons, Historic England) — luật chỉ đòi ≥ 1 nơi đã tra; nên tra thêm trước bản phát hành (K1179-D7).
### KN-8 — mặt nước AI — **MỘT PHẦN (sửa cách giữ bờ; T9c không làm thước)**
- Ghép thử máy (0 API sinh ảnh; ảnh AI + render trong git; `do/ghep_kn8.py`; tái tạo ghép cũ phiên A **trùng từng điểm**): P1 sông 22,03 % khung (KN-8 nói ≈ 1/3 — đo 22 %), P9 0,42 %.

| Tấm | (a)-E cũ | (a)-E đề xuất (bờ ±8 px cả hai phía) | (a)-E K (bờ phía đất) |
|---|---|---|---|
| E-P1-ngay l2 "tháp" | 28,41 % | 8,20 % | **6,38 %** |
| E-P1-ngay l2 "đủ" | 38,16 % | 17,95 % | 16,13 % |
| E-P9-ngay l1 "tháp" | 5,82 % (k2check: 5,74 %) | 5,73 % | 5,40 % |

- **Đúng đề xuất → lỗi hình rõ:** dải ±8 px phía NƯỚC giữ màu nước render (xanh) → viền xanh quanh bờ, cầu, mọi thuyền trên nước AI nâu (tờ so `do/kn8/so-KN8-E-P1-ngay-l2-thap.jpg`, giữa). Bờ phía đất → liền mạch (phải). Còn thấy: cầu render phẳng CG cạnh nước AI; vệt tối mảnh bên phải cầu = bóng cầu AI lệch vị trí; **2 "thuyền" render là elip đen** (lớp tàu) — lỗi 3D lộ rõ trên nước AI.
- **T9c trên nước AI** (`do/kn8-t9c.json`): tấm sạch báo **7 đoạn bờ lấn tới 70 px** (1 thật: bóng cầu AI; còn lại bóng tường kè), không tách được 4 ca âm tổng hợp (dán thuyền, dán cầu, bờ lấn 20 px, 6 đốm nổi: số đo ngang hoặc thấp hơn tấm sạch) → **không dùng làm thước Chặn**, chỉ in.
- **Mô hình nhìn** (đề bài mới `n2p-e-v2-nuoc`; lượt đầu dùng đề bài E cũ: GPT báo "sông được bảo vệ đổi" @[0; 0,686; 1; 1] → báo nhầm do đề bài): 2 tấm sạch (P1, P9 "tháp" bo_dat) **0 Chặn**; ca âm "cầu thứ hai" — GPT và Claude đều báo nhiều mục "thêm trên mặt nước" (+ N2P-3 (b) Claude); "thuyền thêm" — GPT + Claude bắt (N2P-4 + KN-8). **2/2 bắt, 0/2 nhầm** (đáp án nhỏ — nêu rõ).

## 3. Luật 1.17.9 (RULES-LL §1.17.9; `checks/ll/q_k1179.py`)
| Hàng | Trường khai | Đo / điều kiện | Mức |
|---|---|---|---|
| N2P-1 (b), N2P-3 (b) tấm E (KN-1) | `ngoai_le: [{hang, hop, ly_do, duyet_chu_du_an: {nguoi_ky, vai: chu_du_an, ngay, ket_luan: chap_nhan}}]` | máy tấm sạch; tâm hộp trong `hop`; ≤ 25 % hộp trong lõi (a)-E | báo mô hình → (w) N2P-E |
| N2P-E (k) KN-5 | `toa_co_ten[].loai`: thap (`dinh_odn_m`/`y1_m` ≥ 75) · lich_su (`nguon_lich_su`) · mai_vom | sai định nghĩa | Chặn G2 · CB animatic |
| N2P-E (h) KN-6 | `n2p.video[].day_2d: {kieu: day|truot, toc_do_pct_s}` | hệ số góc max(|tỉ lệ−1|, dịch tâm/rộng) ≤ 1,5 %/s (+2 % sai số đo); sai sau bù (a)-E ≤ max(3/255, 2× ngoài) | Chặn G2 · CB animatic |
| N2P-E (u) + N2P-1 (b) KN-8 | tấm `nuoc_ai: true` + `duyet_chu_du_an` | (a)-E bỏ mọi điểm nước; đề bài `n2p-e-v2-nuoc`; vật thêm trên nước → (b); T9c chỉ in | Chặn G2 |
| Q37 / NHIP-K2 / Q37 (1.13) KN-2 | `log_may` trong log shot (đã có) | + biến cố đo (n1) mặt trời 0°/−6°, (n2) pha máy | như cũ |
| NHAN-VAT-TEN KN-4 | `cat_clip: [k0, k1]` \| `{t0, t1}` | đo mặt trong cửa sổ; dài ≠ đoạn > 1 khung → (k) | như cũ |
| NHAN-VAT-TEN (k) KN-7 | `chan_dung: khong_co`, `chan_dung_nguon_da_tra.noi`, `duyet_chu_du_an` "YYYY-MM-DD HH:MM" | YuNet mọi hộp ≥ 0,60 ≤ 1/8; dòng AUTHORSHIP khớp ngày-giờ-mã | miễn (k); (a) giữ |
Tệp đổi: `q_k1179.py` (mới), `q_n2p.py` (`bo_nuoc`, ngoại lệ, video `day_2d`), `q_k1178.py` (nước AI, đề bài, KN-5, hàng N2P-E h/u), `q_k1177.py` (cat_clip, KN-7), `q_nhip.py` + `q_k2var.py` + `k2check.py` (`blog`), `cap112.py` (mức h/u), `cinecheck/__init__.py` VERSION 1.17.9, `RULES-LL.md` §1.17.9, `selftest_k1179.py`, `fixtures/k1179/` (2,2 MB).

## 4. Cách khai cho phía dựng (phiên B)
- **Tấm E ngoại lệ "bờ"** (chỉ sau khi chủ dự án duyệt K1179-D2): `ngoai_le: [{hang: ["N2P-1 (b)", "N2P-3 (b)"], hop: [0.0, 0.96, 0.09, 1.0], ly_do: "K1178-D2 — mép kè/nước AI ngoài dải bờ 8 px; máy 0/255, T9c 0", duyet_chu_du_an: {nguoi_ky: "Chủ dự án (tác giả – đạo diễn)", vai: chu_du_an, ngay: "2026-10-26", ket_luan: chap_nhan}}]` + dòng AUTHORSHIP (P ghi). Mẫu: `do/k2/e/KN1-khai-thu-episode.yaml`.
- **Toà có tên:** mỗi mục `toa_co_ten` thêm `loai` và `dinh_odn_m` (= `y1_m` của toa.json) hoặc `nguon_lich_su` (NHLE/Historic England…); bỏ "Guildhall Art Gallery" khỏi lịch sử hoặc ghi nguồn.
- **Nước AI (nếu chủ dự án chọn K1179-D6 A):** ghép = `do/ghep_kn8.py <khung> <lượt> thap bo_dat` (bờ phía đất); tấm khai `nuoc_ai: true` + `duyet_chu_du_an` sau khi soi tờ so; sửa trước: thuyền render elip đen (lớp tàu P1), bóng cầu AI lệch (che hoặc ghép lại vệt tối cạnh cầu).
- **Đẩy 2D:** `n2p.video[{…, day_2d: {kieu: day, toc_do_pct_s: 1.0}}]`; dựng đẩy SAU ghép (một phép 2D cho cả khung); máy 3D CODINH.
- **NHAN-VAT-TEN:** `cat_clip` đúng khung bản dựng dùng (H1-15b [0, 110] đã đúng); H3-05b giữ khai hiện có (đủ điều kiện).

## 5. Selftest
- `checks/ll/selftest_k1179.py` **50/50** (không mạng/API; mô hình giả lập; **ca thật** từ đầu vào A thu nhỏ 640×360 + câu trả lời GPT thật + toa-thap thật + 2 clip Omni thật + 3 log máy thật — nguồn/SHA `fixtures/k1179/NGUON.json`): KN-1 12 · KN-5 8 · KN-8 7 · KN-6 6 · KN-4 4 · KN-7 6 · KN-2 7. Mỗi luật ≥ 1 ca đạt + ≥ 1 ca trượt + ca "không khai → 1.17.8".
- Trước khoá (`do/selftest-truoc-khoa.txt`) và **sau khoá** (`do/selftest-sau-khoa.txt`, LOCK KHỚP): k112 75/75 · k1121 48/48 · k1122 37/37 · k113 64/64 · k114 126/126 · k115 105/105 · k116 144/144 · k117 130/130 · k1172 74/74 · k1173 42/42 · k1174 91/91 · k1175 52/52 · k1176 62/62 · **k1177 87/87 · k1178 69/69** · **k1179 50/50** · k2 129/129 · ll 317/317 — **0 SAI, 0 kỳ vọng cũ đổi**. Bộ L1 cinecheck: `checks/selftest/run_selftest.py` (không đổi trừ VERSION) **rc 0, TẤT CẢ KHỚP (142 ca OK)** ở lượt 2 (lượt 1 TRƯỢT do phiên chặn mạng — §11); bản chạy ở `do/cinecheck-selftest/`.

## 6. Bảng hàng đổi k2check 1.17.8 → 1.17.9 (đầy đủ: `do/k2/hang-doi.md`; bảng gốc `do/k2/`)
| Đầu vào | Hàng đổi | Chi tiết |
|---|---|---|
| 8 tấm E thật (P9 ngày/đêm, P1 l1/l2; "đủ"/"tháp"), không khai mới | **0 / 77** | không khai → hành vi 1.17.8 (số toà chưa khai `loai` chỉ in ở giá trị) |
| E-P9-ngay-l1-thap + `ngoai_le` khai thử (KN-1) | 3 | N2P-1 TRƯỢT → **CẢNH BÁO** · N2P-3 TRƯỢT → **ĐẠT** · N2P-E ĐẠT → CẢNH BÁO (2 (w) ngoại lệ) |
| Đặc tả v4 (animatic) | 5 (+ LOCK nhãn) | Q37/NHIP-K2/Q37 (1.13): TB 5,75 → **5,04 s** (+42 biến cố log máy), dài nhất 20,17 s — vẫn TRƯỢT · NHAN-VAT-TEN CB 7 → **4** (hết (a)+(w) H1-15b nhờ `cat_clip`; hết (k) H3-05b nhờ KN-7; còn (u) H1-05a, H1-06x, H1-15b, H1-15x chờ duyệt A1) · N2P-E giá trị in "toà chưa khai loai 10" |
| Ghép thử KN-8 bo_dat (không mô hình) ×4, bo8 ×4 | 2–3 mỗi tấm | N2P-1 (a) 1.17.8 TRƯỢT (nước ≠ render) → 1.17.9 0/255; N2P-3 T9c 6–8 lỗi → chỉ in; N2P-E + (u) THIẾU duyệt; còn THIẾU mô hình (không bộ đệm) |
| Ghép thử KN-8 có mô hình (đề bài nuoc) | — (chỉ 1.17.9) | P1, P9 "tháp" bo_dat: N2P-1 CẢNH BÁO (cụm dải 20 px), N2P-2…4 ĐẠT, N2P-E chỉ (u) duyệt · am_cau: N2P-1/N2P-3 TRƯỢT (mô hình 9 mục trên nước) · am_thuyen: N2P-1 (b) + N2P-4 TRƯỢT |

## 7. LOCK
1.17.8 `045b7bb7414364d4732fe22c4b643ae04d7a0e19ae25f0e839de149379d3185a` → **1.17.9 `9eddaf24e8c5276b6017af172e7c8185ba21831a7b6e842cc17094fd5c66fc34`** (DATE_UTC 2026-10-26T03:54:51Z), `--verify` KHỚP. `lock.py` không cờ gọi **đúng một lần**.

## 8. T3 bản cuối 1.17.8 ↔ 1.17.9
Đầu vào như K-1.17.8 §9 (`git archive 41de7ce3 channel-k2/k2c-t3-01 reports/animatic-t3-v2 reports/k1172/do reports/k1173/do AUTHORSHIP.md RIGHTS.md docs` + git cục bộ; `mk_tl.py` → timeline `0ff3f0da…` 761,9998 s; `mk_log_chu.py` → `17053dff…` 1 524 khung; master LFS `release-k2-t3-g2` **SHA `5b9f0bcc…` khớp**). 1.17.8 (worktree): **trùng hệt** `reports/k1178/do/k2/k2check-1.17.8-t3.md` trừ tiêu đề. 1.17.9 (cây đã khoá): `diff` hai bảng **chỉ khác dòng tiêu đề và nhãn phiên bản hàng LOCK** (`do/k2/k2check-1.17.{8,9}-t3.md`, JSON `.json.gz`). Mã thoát cả hai: 1 (TRƯỢT như K-1.17.8). Luật 1.17.9 chỉ áp tập từ T4.

## 9. Chỉ số trong ±5 % quanh ngưỡng (luật cứng — nêu tên)
- **KN-6: đẩy 2D tổng hợp 1,5 %/s đo 1,505 %/s (+0,3 %)** — lý do thêm sai số đo 2 %.
- **KN-1: 6,3 % hộp trong lõi so trần 25 %** — xa ngưỡng (ghi để rõ).
- Đặc tả v4 (không đổi so phiên A): Q26b-K2/Q37… như bảng A; YuNet H3-05b 0,070 so 0,125 (−44 %, ngoài ±5 %); H1-15b cat_clip 0,062 (−50 %).
- KN-8: T9c giữa nước P1 bo_dat 0,77 % so 2 % (chỉ in).

## 10. Chi phí thật (sổ `reports/k1179/so-ai.jsonl`, 20 dòng, có `usd`)
| Nhà | Số | Chi tiết |
|---|---|---|
| OpenAI | **$0,313** | gpt-6.1-sol, 6 lần mô hình nhìn k2check KN-8 (lượt 1: 2 tấm đề bài E cũ; lượt 2: 4 tấm đề bài nuoc) — mốc $2 |
| Claude API | **$0,699** | claude-sonnet-5-5: 6 lần mô hình nhìn ($0,421) + 8 lần q_thoi_dai O2 ($0,278) — mốc $3 |
| Gemini / ElevenLabs / RunPod | 0 | 0 ảnh/video sinh |
| Tải | master T3 LFS 1,79 GB (SHA khớp) | |
| Giờ máy | ≈ 1,9 h (03:12 → ≈ 05:05 UTC; P ≤ 2) | |

## 11. Sự cố
1. **Lượt chuẩn 1.17.8 đầu tiên chạy trên cây đang sửa** → dừng (PGID) và chuyển sang worktree @41de7ce3 để mã sửa dở không lẫn (không có số nào lấy từ lượt đó).
2. **Đề bài E coi sông là phần bảo vệ** → GPT báo nhầm "sông đổi" trên tấm nước AI (lượt 1, $0,24) → đề bài `n2p-e-v2-nuoc`; raw lượt 1 của P1 bị lượt 2 ghi đè cùng tên tệp (sổ AI giữ đủ dòng chi phí; `sha_ra` lượt 1 trỏ tệp lượt 2 — nêu rõ).
3. **Email giả trong selftest** (ca "ngoai_le có email") bị preflight chặn trước khoá → dựng lúc chạy (bài học K-1.17.8 lặp lại — đã áp quét trước khoá nên không lọt vào khoá).
4. **`pkill -f e_sau_khoa.sh` tự giết lệnh shell của phiên** (khớp chuỗi trong chính lệnh) — trái bài học #112; không mất dữ liệu; sau đó chỉ dừng theo PGID.
5. **Một lần cất `checks/` (day.sh stash) lúc selftest trước khoá đang chạy** (03:42) — bộ k114 chạy trùng lúc vẫn 126/126; toàn bộ selftest chạy lại sau khoá (0 SAI).
6. Bộ L1 cinecheck chạy lâu (> 15 phút) → chuỗi E/đặc tả sau khoá được tách chạy song song (P = 2).
8. **Bộ L1 cinecheck lượt 1 TRƯỢT do phiên** chặn mạng (proxy 127.0.0.1:9) → ca E2E không tải được mô hình faster-whisper từ Hugging Face; chạy lại không chặn (không gọi API trả tiền) — kết quả §5; log lượt 1 `do/cinecheck-selftest-luot1-chan-mang.txt`. `run_selftest.py` ghi đè `reports/checks-selftest/` (ngoài vùng) → chép sang `do/cinecheck-selftest/`, khôi phục bằng `git checkout`.
9. **Đẩy trễ 1 phút** (04:23 → 04:54) so mốc 30 phút.
7. KN-6/KN-2 thước được chỉnh sau đo đầu (tốc độ: max-góc → hệ số góc; sai số đo 2 %) — trước khoá, nêu ở §2.

## 12. Bảng quyết định cho chủ dự án
| # | Việc | Phương án | Ưu | Nhược | Tác động | Rủi ro | Khuyến nghị |
|---|---|---|---|---|---|---|---|
| **K1179-D1** | Duyệt luật 1.17.9 | A: duyệt · B: giữ 1.17.8 | A: hết Chặn oan (H3-05b, H1-15b, "bờ"), mở đường E nước AI/đẩy 2D | A: phía dựng khai thêm (§4) | T4 bản cuối | thấp | **A** |
| **K1179-D2** | Ngoại lệ "bờ" H5-05a (E-P9 "tháp") | A: duyệt `ngoai_le` (soi ô dưới trái `reports/ban-cuoi-t4-a/e/so-E-P9-ngay-l1-thap.jpg`) · B: mặt nạ "đủ" · C: sinh lại ảnh AI | A: giữ ảnh đẹp hơn, máy sạch, thay đổi 0,09 % khung ở mép | A: một chạm người | 1 tấm | thấp | **A** |
| **K1179-D3** | Q37 nhịp T4 (39 khoảng > 6 s) | A: giữ Q37 Chặn G2; chủ dự án chỉ các shot thấy chậm khi xem, phía dựng thêm biến cố CÓ NGHĨA (vật mang nghĩa §13.2) chỉ ở đó; K hiệu chuẩn BIEN-CO-V trên master 1080p sau phiên B · B: nới (c) cho timelapse có biến cố đo · C: miễn từng shot dài có duyệt (như khung neo §11.2 ≤ 10 s) | A: đúng luật cứng, đúng nhận xét 06:56 | A: thêm vòng sửa nhịp | MÓC, HỒI 1–5 | B: đạt giả; C: nhiều ngoại lệ | **A** (+ C cho ≤ 3 shot "đứng có chủ ý" nếu chủ dự án muốn) |
| **K1179-D4** | Định nghĩa toà có tên (Q-A1) | A: tháp ≥ 75 m + lịch sử có nguồn + St Paul's (mặt nạ "tháp") · B: mọi toà OSM có tên | A: đúng chữ 00:07, ít loang lổ ((a)-E P9 5,74 %) | A: AI vẽ lại toà tên thấp (sai nhỏ — chủ dự án chấp nhận 09:08) | P1/P9 | thấp | **A** |
| **K1179-D5** | Đẩy/trượt 2D trên tấm E | A: cho phép theo luật (một phép 2D, ≤ 1,5 %/s) — dùng ở M01/H5-05a khi chủ dự án muốn · B: không dùng | A: bớt cảm giác "đứng" (liên quan D3) | A: nền AI phóng → mềm hơn | ≤ 2 shot | thấp | **A**, dùng theo xem |
| **K1179-D6** | Nước AI (KN-8) cho P1 | A: `nuoc_ai` bờ phía đất + duyệt từng tấm; sửa thuyền elip đen + bóng cầu AI trước · B: giữ nước render | A: sông 22 % khung hết "phẳng CG" | A: cầu/thuyền render lộ CG hơn trên nước thật; duyệt mỗi tấm | P1 (H5-04 đuôi, M01 nếu E) | thấp–vừa (thước máy cho nước AI chưa có — dựa mô hình + người) | **A** |
| **K1179-D7** | H3-05b (Godfrey Allen) | A: giữ H3-05b (miễn (k) đạt) · B: dự phòng H3-05c 3D | A: giữ nhân vật đúng lời, khung xa | A: 4 nguồn chưa tra (NPG, St Paul's, Commons, HE) | 6 s | thấp | **A**; tra thêm 4 nguồn trước gói phát hành |

**Dòng QUYET-DINH-TREO đề xuất (P ghi):** `K1179-D1…D7 — chờ chủ dự án (K-1.17.9, 26/10/2026): D1 duyệt luật 1.17.9 (khuyến nghị A) · D2 ngoại lệ "bờ" E-P9 (A) · D3 Q37 nhịp T4: giữ Chặn, sửa nhịp thật ở shot chủ dự án thấy chậm, hiệu chuẩn BIEN-CO-V trên master 1080p (A) · D4 toà có tên = tháp ≥ 75 m/lịch sử/St Paul's (A) · D5 đẩy 2D tấm E (A, dùng theo xem) · D6 nước AI P1 (A, sửa thuyền/bóng cầu trước) · D7 giữ H3-05b (A)`.

## 13. Dòng sổ đề xuất (P ghi — phiên này không sửa sổ)
- **COST-LEDGER:** `2026-10-26 · K-1.17.9 · OpenAI $0,313 (mô hình nhìn KN-8) · Claude API $0,699 (mô hình nhìn $0,421 + q_thoi_dai $0,278) · Gemini 0 · ≈ 1,9 h (03:12 → ≈ 05:05 UTC; P ≤ 2) máy · tải LFS 1,79 GB`.
- **AUTHORSHIP:** căn cứ 26/10 07:39 (H3-05b hướng (a)); lệnh K-1.17.9 "Duyệt PHIẾU-A theo khuyến nghị điều phối" (giờ dán ≈ 10:12); ghi khi chủ dự án trả lời K1179-D1…D7.
- **RIGHTS:** không tài sản mới (fixture `checks/ll/fixtures/k1179/` là ảnh/clip của dự án thu nhỏ — chỉ dùng kiểm).
- **BAI-HOC-K2 (đề xuất):** (1) đề bài mô hình phải đổi khi đổi lớp được bảo vệ (nước AI) — chạy đối chứng tấm sạch trước; (2) không `pkill -f <tên script>` trong lệnh có chứa chính tên đó; (3) giữ dải bảo vệ phía ĐẤT khi nền đổi màu (viền màu cũ lộ ngay); (4) thước đối chứng render (T9c) không áp cho vùng AI vẽ lại toàn phần.

## 14. Việc chờ chủ dự án
1. Trả lời **K1179-D1…D7** (§12).
2. Phiên P: merge nhánh `ccr-196e0bda-gcj9iw` khi duyệt (nhánh này **không** merge); ghi sổ theo §13.
3. Phiên B (dựng): khai theo §4; sửa thuyền elip đen + bóng cầu AI nếu dùng nước AI; nhịp theo D3.
4. Phiên K sau phiên B: hiệu chuẩn BIEN-CO-V T4 trên master 1080p (K1178-D4).

**DỪNG chờ chủ dự án.**

