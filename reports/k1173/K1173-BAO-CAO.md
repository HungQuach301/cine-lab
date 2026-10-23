**Nhánh thật: `checks-1-17-3`** (đúng lệnh; harness gợi ý `ccr-ebaec186-obstp4` nhưng đẩy `checks-1-17-3` được chấp nhận). Gốc `origin/main` @ `9852adf5` (LOCK 1.17.2 `aca05e60…`). Không merge, không đụng `main` hay nhánh khác.

# Phiên K-1.17.3 — xét 6 khiếu nại bộ kiểm của BAN-CUOI-T3 + bảng quyết định K còn treo — BÁO CÁO

> Phiên K, 23/10/2026 ≈ 06:10–07:30 UTC, chạy song song TIEN-KY-T4 và KHEP-T3 (không đụng vùng của họ). Mọi số là số đo thật trong phiên; tệp số đo ở `reports/k1173/do/`.
> Email chủ dự án không có trong tệp, commit, header, URL, payload hay User-Agent nào (tải master bằng UA `CineLab-research (+https://github.com/HungQuach301/cine-lab)`). Không in/ghi khoá.

## 0. Khối điều lệ và tóm tắt
| Trường | Lệnh | Thực tế |
|---|---|---|
| Loại phiên | K-1.17.3 | đúng |
| Nhánh | `checks-1-17-3` từ `origin/main` @9852adf5 | đúng |
| Vùng sửa | `checks/**`, `reports/k1173/**` | đúng + **`checks-appeal.md` (gốc repo)** — chỉ thêm mục "Phán quyết K — checks 1.17.3" theo việc 2 của lệnh. Không sửa `docs/`, sổ, `design/`, `scripts/`, `channel-k2/`, `reports/ban-cuoi-t3/` |
| Chi phí | Claude API mốc $3 (chặn $10), OpenAI $1, giờ máy 4 h; 0 Gemini/ElevenLabs/RunPod/YouTube; không `--o2-api` | **Claude API $0 · OpenAI $0** · giờ máy ≈ 1,2 h (§8) · Gemini/ElevenLabs/RunPod/YouTube **0** · không `--o2-api`, không `--ml2-api`, không `--n2p-vision` |
| Preflight | `set -o pipefail`, commit chỉ khi có "— ĐẠT" | hook pre-commit + pre-push cài trước lần đẩy đầu (06:26); mọi commit/push: `preflight: … — ĐẠT` + `PREFLIGHT ĐẠT` + `lock.py --verify: KHỚP` |
| `lock.py` không `--verify` | chỉ ở bước khoá cuối | **đúng một lần**, 06:58:54 UTC → 1.17.3; mọi lần khác chỉ `--verify` |
| Đẩy ≤ 30 phút + CHECKPOINT | bắt buộc | 06:27, 06:47 (bản vá WIP — `checks/` cất bằng stash vì hook kiểm LOCK), 07:00 (mã khoá), commit cuối; `reports/k1173/CHECKPOINT.md` |
| Force / amend / dừng hỏi | không | không |

**Tóm tắt:**
1. **6 khiếu nại: 4 LỖI LUẬT (A1, A2, A3, A5) + 1 LỖI LUẬT một phần (A6) — đã sửa + selftest; 1 LỖI PHIM/KHAI (A4) — giữ luật.** EO-DAT-R3 (a) N4.5/N5.6 một góc: luật giữ, **không tự cho đạt**; thêm đường "ngoại lệ có khai" chỉ nhận khi AUTHORSHIP có dòng duyệt (đề xuất K1173-D1).
2. **Trên đầu vào thật bản cuối T3 (master SHA `5b9f0bcc…`):** 1.17.2 → 1.17.3 đổi đúng 9 hàng: **Q33-K2, Q33 (1.13), SACH-1 TRƯỢT → ĐẠT; TL-3 CẢNH BÁO (sập) → ĐẠT; EO-DAT-R3 7 → 2 lỗi (chỉ còn (a) N4.5, N5.6); Q37/NHIP-K2 209 → 71, Q37 (1.13) 216 → 78**; 44/53 hàng giống hệt (§5); LOCK 1.17.3 KHỚP trong lượt.
3. **Selftest:** `selftest_k1173.py` **42/42**; cũ k112 75/75 · k1121 48/48 · k1122 37/37 · k113 64/64 · k114 126/126 · k115 105/105 · k116 144/144 · k117 130/130 · k1172 74/74 · k2 129/129 · ll 317/317 — **không kỳ vọng cũ nào đổi**.
4. **Bản sao đường cong thời gian của trình dựng** (`tl7.timeline` + `crossings`) trong `checks/` trùng **chính tl7.js chạy bằng node: lệch 0** trên 147 điểm năm và 12 crossing (7 cảnh T3).
5. **LOCK 1.17.2 `aca05e60…` → 1.17.3 `d99af8f2…`**, `--verify` KHỚP.
6. **Bảng quyết định treo** `reports/k1173/QUYET-DINH-TREO.md`: 14 dòng còn cần (K117-D1, D3, D5, D6, D8; K1171-D2, D3, D4; mới K1173-D1…D6) + 3 dòng hết hiệu lực (K117-D4, K117-D7, K1171-D1, có căn cứ). Trả lời một lần: "Duyệt theo khuyến nghị".

## 1. Đầu vào đã đọc
`reports/ban-cuoi-t3/checks-appeal.md` (A1–A6), `BAN-CUOI-BAO-CAO.md` §9, §14, §15, `do/k2check-1.17.2-cap{,-l2,-l3}.txt`; `channel-k2/k2c-t3-01/cuoi/` (episode.yaml, log-shot.json, the-phuong-phap-cuoi.json, mk_ep_cuoi.py); `scripts/k2tl/cuoi_bien_co.py` (thước biến cố của xưởng — đọc để tìm nguyên nhân lệch, K không sửa); `design/k2v/tl/tl7.js`, `sun.js`, `scenes/t3tl.js` (trình dựng); `reports/k117/K117-BAO-CAO.md` §2.3, §3, §4, §10–11; `reports/k1171/K1171-BAO-CAO.md` §10; `reports/k1172/K1172-BAO-CAO.md` §3–§6; Kinh thánh `docs/BIBLE-KENH2.md` §12.1, §13, §14.1, §14.7, §15, §17, §18; AUTHORSHIP 19–23/10; `reports/m3/BAI-HOC-LL.md`.

## 2. Phán quyết A1–A6
Cách tái hiện: thư mục tạm (scratchpad), `git archive origin/main channel-k2/k2c-t3-01 reports/animatic-t3-v2 AUTHORSHIP.md RIGHTS.md`; timeline **tổng hợp từ đặc tả** (`reports/k1172/do/mk_tl.py`, 761,9998 s — timeline prep và log render `sec/` của phiên dựng ở `/var/tmp/cine-out` đã mất); **log chữ tổng hợp** từ đặc tả với đúng vai mà lượt 3 BAN-CUOI báo (thẻ chương vai `chuong`, chữ thẻ PP vai rỗng — `do/mk_log_chu.py`); master thật tải từ LFS `release-k2-t3-g2` (SHA-256 `5b9f0bcc…` khớp). 1.17.2 chạy từ worktree `origin/main` (LOCK KHỚP). Lượt 1.17.2 **tái hiện đủ** các hàng khiếu nại của lượt 3 BAN-CUOI: Q37 209 · Q37 (1.13) 216 · NHIP-K2 209 · Q33-K2/Q33 (1.13) `anim_N1_6` ×3 · SACH-1 3 · TL-3 sập · EO-DAT-R3 7 · PP-1 3,4 từ/s.

| # | Hàng | Phán | Căn cứ (Kinh thánh / lệnh đã duyệt) | Sửa | Trên T3 (1.17.2 → 1.17.3) | Cách khai đúng cho T4 |
|---|---|---|---|---|---|---|
| **A1** | TL-3 | **LỖI LUẬT** | K117 §2.3 / RULES 1.17: `trong_pct` = "số TB shot **hoặc** `[[t, %], …]`" — chính K định nghĩa; EO-DAT-R2 đọc được, TL-3 ép `float()` | `q_k116.tb_pct`: danh sách → **TB theo thời gian**; kiểu lạ → THIẾU, không sập | CẢNH BÁO (sập) → **ĐẠT** (43 shot 3D, 0 trống) | không cần đổi |
| **A2** | Q37 / NHIP-K2 / Q37 (1.13) (a) | **LỖI LUẬT** (đọc mốc thiếu) + **69 beat LỖI KHAI** | Q37 (a) "biến cố khai khớp mốc thật của đặc tả"; §13.6 TL-1 "trong shot, thời gian chạy (nhà mọc/cháy/sập, công trình có ngày đầu/cuối, tàu, ngày–đêm, khói)" — mốc cảnh tl nằm ở `opt.time` và năm thế giới của lớp vật, bộ đọc 1.11 chỉ biết lớp bản đồ T1/T2 | `q_nhip.tl_moc_canh` (chỉ tập từ T3): `opt.time[].t`, `smoke[].t`, năm thế giới (wY/w/on/off/full/day/hoist/path, `nc.bakes`) → giây cảnh qua **bản sao tl7** (lệch 0 so tl7.js); `p.the_chuong.at` | (a) **207 → 69**; Q37 209 → 71 | beat lấy giờ từ chính đường cong trình dựng (tl7 / `tl_moc_canh`); trạng thái có sẵn từ đầu shot không phải beat (§2.1) |
| **A3** | EO-DAT-R3 (b) | **LỖI LUẬT** | §14.7 R3 "Shot > 15 s chia 2–3 góc, **mỗi góc** có biến cố thấy được ≤ 6 s" — đầu góc là ranh như đầu shot (luật đã tính đầu/cuối shot); cắt góc R3 đã được nhận ở TL-1 (V2-D7, K1172-D2 duyệt) | `goc_may[].t0` (hoặc `t`) > 0 là ranh; mốc quy **lưới khung** round(t·24)/24 | (b) **5 → 0**; N2_11 5,50 · N3_4 5,50 · N4_2 4,83 · **N5_1 6,00 (đúng ngưỡng)** · N5_4 5,87 s | khai `goc_may: [{id, t0, t1}]` mọi shot cắt góc |
| — | EO-DAT-R3 (a) N4.5 27,2 s, N5.6 20 s | **LỖI PHIM** theo chữ R3; luật giữ | R3 "chia 2–3 góc"; 23/10 10:45 "không muốn sửa thêm" là quyết định KHÔNG SỬA PHIM, chưa phải duyệt ngoại lệ R3 | thêm **ngoại lệ có khai** `r3_ngoai_le: {ly_do, authorship}` — chỉ nhận khi AUTHORSHIP.md có dòng cùng ngày giờ nêu id shot + "R3" | (a) **2 → 2** (chưa có dòng duyệt — K không tự cho đạt) | nếu chủ dự án duyệt K1173-D1: P ghi dòng AUTHORSHIP; log shot khai `r3_ngoai_le` |
| **A4** | PP-1 (e) | **LỖI PHIM/KHAI — giữ luật** | K116-D8 (duyệt 19/10 18:48) "'≈ 8 s' = 7–9 s, ≤ 3 từ/s Cảnh báo"; lệnh "7–9 s mỗi thẻ, ≤ 3 từ/s" đo **mỗi thẻ** — tiêu đề là chữ trên thẻ người xem phải đọc (§12.1 (b) gọi thẻ bằng chính tiêu đề) | không | PP1 31 từ / 9 s = **3,44 từ/s → Cảnh báo** (không chặn) — như cũ | ≤ 27 từ (cả tiêu đề) / 9 s; ≤ 24 từ / 8 s |
| **A5** | Q33-K2 / Q33 (1.13) | **LỖI LUẬT** | §13.6 TL-1 "quay lại cùng điểm máy ở **năm khác**" — năm phải là năm HIỆN; log N1_6 `nam` [1704,8; 2026,79] là bao, đường cong `opt.time` NHẢY 1705,3 → 1727,15 → 1735,4 → 2026,78 (mỗi bước 0,05 s): 1782 và 1900–1930 không hiện | `q_k117.nam_hien` / `nam_khoang`: khoảng năm hiện lấy mẫu mỗi khung theo bản sao tl7; hai mốc cách ≤ 3 khung = bước năm, tách khoảng; không `opt.time` → năm log | **TRƯỢT → ĐẠT** cả 2 hàng (N1_6 hiện 1704,8–1705,3 · 1727,15–1727,45 · 1730–1735,4 · 2026,78–2026,79; N2_10 1782,40–1782,58 và N3_4 1900–1930 được miễn) | không cần đổi |
| **A6** | SACH-1 (c)(e) | **LỖI LUẬT một phần** + tên vai **LỖI KHAI** | §13.3 "Thẻ chương (ngoại lệ của §12.1)"; §12.1 (b) đưa "chỗ nào là ước tính" lên thẻ "How this film was made" (chữ "illustrative" ở PP2 đúng chỗ); CHUONG-1, PP-1 cùng lượt nhận thẻ theo đặc tả; SACH-1 chỉ nhận theo tên vai (`the_chuong`, `the_phuong_phap` — K117 §3) | chữ trong khoảng giờ đoạn PP bỏ qua (PP-1 xét); chữ trùng nguyên văn `p.the_chuong` trong [at, at+dur] ± 1 bước mẫu bỏ qua (CHUONG-1 xét); ngoài đó như cũ | **TRƯỢT 3 → ĐẠT** (PP 145 mẫu, chương 30 mẫu nhận theo đặc tả) | log render ghi vai `the_chuong` / `the_phuong_phap` |

### 2.1 A2 — 69 beat còn lệch (LỖI KHAI, không sửa luật)
| Nhóm | Số | Ví dụ | Nguyên nhân |
|---|---|---|---|
| Beat mô tả trạng thái ở 0,5–1,0 s | 21 | N1_4 0,5 s "dòng dân rời phố…"; N5_2 0,5 s "người đi bộ băng qua đường băng…" | không phải biến cố (vật có sẵn từ đầu shot); không ứng mốc nào |
| `bien_co_tu_dac_ta` của thước xưởng | 17 | N2_7 "khói xuất hiện" khai 2,04 / 3,08 / 4,13 / 5,17 s; trình dựng 0,64 / 1,69 / 2,73 / 3,78 s (lệch 1,39 s) | `scripts/k2tl/cuoi_bien_co.py` nội suy tuyến tính giữa mốc + `dy()` (mk_ep_v7p) đổi ngày → năm không theo múi giờ LMT của tl7; trình dựng (`scenes/t3tl.js` → `tl7.timeline`) cho giờ khác |
| Beat tay khác (ngay_dem 7, tau 4, pha 4, xay 4, nguoi 4, lua 3, may 2, dem_nam 1, may_bay 1, den 1) | 31 | N2_8 8,4 s "hoàng hôn 11/9"; N5_4 13,15 s "hàng rào cũ gỡ từng đoạn" | giờ đặt tay theo câu lời/ước lượng, không trùng mốc ±0,3 s (vd. hoàng hôn là giờ mặt trời, không phải mốc đặc tả; rào gỡ `fenceOff` [2026,55; 2026,75] qua đường cong ra giờ khác) |
Selftest kiểm luật không bị nới bừa: beat 9,0 s ở N2_7 (không mốc) vẫn bắt; beat khói khai theo thước xưởng vẫn bắt; beat đúng giờ trình dựng thì nhận. Mật độ mốc cảnh tl trên T3 ≈ 1 mốc / 1,5 s (nêu rủi ro ở K1173-D4).

## 3. Luật đổi (1.17.3 — chỉ tập từ T3; cấp không đổi)
| Hàng | Tệp | Định nghĩa mới (tóm tắt — đầy đủ ở `checks/ll/RULES-LL.md` mục 1.17.3) |
|---|---|---|
| TL-3 | `q_k116.tl3`, `tb_pct` | `trong_pct` số \| `[[t, %], …]` \| `[{t, v\|pct}]` → TB theo thời gian; kiểu lạ → THIẾU (b) |
| Q37 / NHIP-K2 / Q37 (1.13) (a) | `q_nhip.tl_year`, `_crossings`, `_years`, `tl_moc_canh`, `spec_times(tl_moc)`, `q37(tl_moc)`; `q_k2var.nhip_k2(tl_moc)`; `k2check` (`V17`) | mốc cảnh tl từ đặc tả qua bản sao tl7 (JD Gregory, LMT −5,35°/15 hoặc `opt.tz`, Hermite Fritsch–Carlson, `hold`); `p.the_chuong.at`; ±0,3 s |
| EO-DAT-R3 (b) | `q_k117.eo_dat` | ranh `goc_may[].t0` (hoặc `t`) > 0; mốc round(t·24)/24; ≤ 6 s; nêu ±5 % |
| EO-DAT-R3 (a) | `q_k117.r3_ngoai_le`, `_authorship` | `r3_ngoai_le {ly_do, authorship}` + dòng AUTHORSHIP (ngày, giờ, id shot, "R3") → nhận; thiếu → lỗi (a) kèm lý do |
| Q33 / Q33-K2 / Q33 (1.13) miễn năm | `q_k117.nam_hien`, `nam_khoang`, `q33_mien` (nhận cả dạng cũ); `k2check` (`NL17`) | khoảng năm hiện theo `opt.time` (bước năm ≤ 0,125 s tách khoảng, khung giữa bước bỏ); fallback năm log |
| SACH-1 (c)(e) | `q_k116.sach1` | bỏ qua chữ trong đoạn thẻ PP và chữ trùng nguyên văn thẻ chương khai trong khoảng khai ± 1 bước mẫu |
| — | `cinecheck/__init__.py` | VERSION 1.17.3 |
| — | `cap112.py` | chỉ docstring (không đổi cấp) |
Tập trước T3: không đổi hành vi (`tl_moc` chỉ bật khi `ap_117`; các hàng 1.16/1.17 vốn chỉ áp từ T3) — selftest k112…k1172, k2, ll giữ nguyên kỳ vọng.

## 4. Selftest
`checks/ll/selftest_k1173.py` — **42/42** (TL-3 7 · Q37 (a) tl 9 · EO-DAT-R3 12 · cấp 1 · PP-1 2 · Q33 miễn năm 5 · SACH-1 5 · áp dụng 1); mỗi luật đổi có ≥ 1 ca đạt + ≥ 1 ca trượt. Dữ liệu: `fixtures/k1173/t3-cuoi-rut-gon.json` (đặc tả + log shot bản cuối T3 rút gọn, SHA nguồn trong tệp), `fixtures/k1173/tl7-ref.json` (năm + crossing tính bằng tl7.js qua node v22). Không mạng.
Selftest cũ trên cây đã khoá (`do/selftest-sau-khoa.txt`): k112 75/75 · k1121 48/48 · k1122 37/37 · k113 64/64 · k114 126/126 · k115 105/105 · k116 144/144 · k117 130/130 · k1172 74/74 · k2 129/129 · ll 317/317. **Không kỳ vọng cũ nào phải đổi.**

## 5. So k2check 1.17.2 ↔ 1.17.3 trên bản cuối T3
Lệnh (cả hai): `k2check.py <tạm>/channel-k2/k2c-t3-01/cuoi/episode.yaml --tl <tạm>/timeline.json --master k2-t3-v1-master.mp4 --cap --no-asr --json …` (episode.yaml tạm thêm một dòng `log_chu: log-chu-tong-hop.json`). Bảng đủ: `do/k2check-1.17.2-t3.md`, `do/k2check-1.17.3-t3.md`, `do/so-1172-1173.md`.

| Hàng | 1.17.2 | 1.17.3 | Lỗi/cảnh báo 1.17.2 → 1.17.3 | Lý do |
|---|---|---|---|---|
| **Q33-K2** | **TRƯỢT** (`anim_N1_6` 3 lần) | **ĐẠT** (0 khoá > 2; pHash thêm 16 lần, miễn 16) | 1 → 0 | A5 năm hiện |
| **Q33 (1.13)** | **TRƯỢT** (`anim_N1_6` 3 lần) | **ĐẠT** (miễn năm khác 16) | 1 → 0 | A5 |
| Q33 | ĐẠT | ĐẠT (chỉ đổi nhãn "1.17.3 … năm hiện theo opt.time") | 0 → 0 | A5 |
| **SACH-1** | **TRƯỢT** ((c) ×1 PP2 "illustrative", (e) ×2 thẻ chương / tiêu đề PP) | **ĐẠT** (chữ thẻ theo đặc tả: PP 145 mẫu, chương 30 mẫu) | 3 → 0 | A6 |
| **TL-3** | **CẢNH BÁO** (sập `float()` danh sách) | **ĐẠT** (43 shot 3D, trống 0) | 1 → 0 | A1 |
| **EO-DAT-R3** | **TRƯỢT** 7: (b) N2_11 8,8 · N3_4 6,5 · N4_2 8,0 · N5_1 6,0 · N5_4 12,7 s; (a) N4_5, N5_6 | **TRƯỢT** 2: (a) N4_5, N5_6 một góc | 7 → 2 | A3 (b); (a) chờ K1173-D1 |
| **Q37** | TRƯỢT 209 ((a) 207 · (c) 9,0 s từ PP1 · (d) khung tĩnh 9,46 s từ 10:09,6) | TRƯỢT 71 ((a) 69 · (c), (d) như cũ) | 209 → 71 | A2; (c) → K1173-D6 |
| **NHIP-K2** | TRƯỢT 209 | TRƯỢT 71 | 209 → 71 | như Q37 |
| **Q37 (1.13)** | TRƯỢT 216 ((a) 207 · (c) 9,0 s PP1 · (d) khung tĩnh neo ×8) | TRƯỢT 78 ((a) 69 · (c) · (d) ×8) | 216 → 78 | như Q37 |
| 44 hàng còn lại (Q26b, Q32, Q34, Q35, Q36, A1–A13, ML1–3, FT1, Q26b-K2, Q32b-K2, NC-H1…H5, Q7/Q8-K2, Q36 (1.13), BD, K-R, K-LAI-1…6, K-LAI-B, K-LAI-3V, O2, CHUONG-1, PP-1, TL-1, TL-2, NHIP-NGHIA, XEM-CAM, PC-1, MINH-HOA, EO-DAT-R1, R2, R4, CONG-BO-1, N2P, LOCK) | — | **giống hệt** (kết quả, giá trị, số lỗi); LOCK 1.17.2 KHỚP → 1.17.3 KHỚP | — | — |
Mã thoát cả hai lượt: 1 (TRƯỢT — còn Q37, EO-DAT-R3 (a), XEM-CAM, K-LAI-2 (d)). Thời gian chạy: 10 m 39 s (1.17.2) · 10 m 59 s (1.17.3).

Hàng **giữ TRƯỢT ở 1.17.3** và vì sao: Q37/NHIP-K2/Q37 (1.13) — 69 beat khai lệch (§2.1) + (c) 9,0 s ở thẻ PP1 (mâu thuẫn hai luật đã duyệt → K1173-D6) + (d) khung tĩnh (phim); EO-DAT-R3 (a) N4.5, N5.6 (K1173-D1); XEM-CAM (chủ dự án chưa chấm); K-LAI-2 (d) không có `phat_hanh.mo_ta` (mô tả do phiên đóng gói — như BAN-CUOI). Không hàng nào chuyển từ ĐẠT sang TRƯỢT.

## 6. LOCK
- **Cũ:** 1.17.2 `aca05e600a51f740c900f5854df47eb730f156c09d62df307d3a31f3b79c6d60` (2026-10-22T04:50:31Z).
- **Mới:** **1.17.3 `d99af8f22d5e7c0ba3469c4b95bcc01296f72f64d9e72d21ed3fb897549ba10b`** (DATE_UTC 2026-10-23T06:58:54Z). `python3 -I checks/lock.py --verify` → **KHỚP** (ngay sau khoá; trong preflight mỗi commit/push; hàng LOCK của k2check 1.17.3 "checks/ khớp LOCK (1.17.3) — KHỚP").
- Tệp đổi trong `checks/`: `LOCK`, `cinecheck/__init__.py`, `ll/RULES-LL.md`, `ll/cap112.py`, `ll/k2check.py`, `ll/q_k116.py`, `ll/q_k117.py`, `ll/q_k2var.py`, `ll/q_nhip.py`; mới `ll/selftest_k1173.py`, `ll/fixtures/k1173/{t3-cuoi-rut-gon.json, tl7-ref.json}`.

## 7. Tệp ngoài `checks/`
`checks-appeal.md` (mục "Phán quyết K — checks 1.17.3"); `reports/k1173/` (báo cáo, `QUYET-DINH-TREO.md`, `CHECKPOINT.md`, `do/`).

## 8. Chi phí thật
| Khoản | Số |
|---|---|
| Claude API (judge, O2, ML2, nhìn) | **$0** — không gọi (không `--o2-api`, `--ml2-api`, `--n2p-vision`, `selftest_k117 --api`) |
| OpenAI | **$0** |
| Gemini / ElevenLabs / RunPod / YouTube | 0 / 0 / 0 / 0 |
| Giờ máy (container) | **≈ 1,2 h đồng hồ**: k2check 3 lượt (10 m 39 s + 10 m 27 s trước khoá + 10 m 59 s) ≈ 32 phút; selftest đủ 2 lượt (≈ 10 + 4 phút) + lẻ ≈ 16 phút; worktree 1.17.2 + tải master ≈ 8 phút; tái hiện/thử mã ≈ 15 phút. CPU (user) mỗi lượt k2check ≈ 23 phút (đa luồng ffmpeg/numpy) |
| Băng thông | tải master 1,79 GB (LFS `release-k2-t3-g2`) một lần |
| Token phiên chính | không đo được từ container (như K-1.17) |

## 9. Chỉ số trong ±5 % quanh ngưỡng (luật cứng — nêu tên)
Trên lượt k2check 1.17.3 (bản cuối T3) và trong luật đổi:
- **EO-DAT-R3 N5_1: khoảng biến cố 6,00 s = ngưỡng 6 s** (9,599 → 15,6 s = 6,001 s, quy lưới khung 144 khung). Đạt nhờ định nghĩa lưới khung của 1.17.3 — nêu riêng ở K1173-D2; theo cách so tới 1 µs của 1.17.2 sẽ trượt 0,001 s.
- EO-DAT-R3 N5_4: 5,87 s (ngưỡng 6 s, −2,2 %).
- Q37 (1.13): khung tĩnh 5,92 s từ 12:19,0 (ngưỡng 6 s) — không đổi so 1.17.2.
- CHUONG-1: 5 thẻ chương đúng 3,00 s (ngưỡng ≤ 3 s) — không đổi.
- PP-1: thẻ PP1 9,0 s (cận trên 9 s) — không đổi; tốc độ đọc PP1 3,44 từ/s vượt 3 từ/s 15 % (ngoài ±5 %, Cảnh báo).
- EO-DAT-R1: N4_2 chủ thể 14,3 % (ngưỡng 15 %) — chỉ báo (V2-D2), không đổi.
- A1 loudness −14,0 LUFS (cửa sổ −15 … −13,8) — không đổi.
Không có phần tử nào được thêm để vượt ngưỡng; phiên này không sửa phim.

## 10. Dòng sổ đề xuất (phiên P sau ghi — phiên này không sửa sổ)
- **COST-LEDGER:** 23/10 K-1.17.3 — Claude API $0, OpenAI $0, giờ máy ≈ 1,2 h (container), tải LFS 1,79 GB.
- **RIGHTS / AUTHORSHIP:** không tài sản mới. Khi chủ dự án trả lời `QUYET-DINH-TREO.md`, ghi nguyên văn + giờ; nếu duyệt K1173-D1 phương án A thì ghi thêm một dòng AUTHORSHIP nêu "N4.5, N5.6 — R3 một góc (bookend)" với ngày giờ duyệt (đường ngoại lệ 1.17.3 đọc dòng này).
- **BAI-HOC-K2 (đề xuất):** "beat cảnh timelapse phải lấy giờ từ chính đường cong trình dựng; thước tự nội suy lệch tới 1,4 s (T3 N2_7)"; "log render dùng đúng tên vai K công bố (`the_chuong`, `the_phuong_phap`)".

## 11. Việc chờ chủ dự án
1. **Trả lời bảng `reports/k1173/QUYET-DINH-TREO.md`** (một lần): 14 dòng còn cần — K117-D1, D3, D5, D6, D8; K1171-D2, D3, D4; K1173-D1 (ngoại lệ R3 có khai + N4.5/N5.6 của T3), D2 (R3 lưới khung + ranh góc), D3 (PP-1 tính tiêu đề), D4 (mốc cảnh tl cho Q37 (a)), D5 (SACH-1 chữ thẻ theo đặc tả), D6 (Q37 (c) miễn thẻ PP — chưa sửa luật). Khuyến nghị: duyệt theo cột cuối.
2. Phiên P: merge `checks-1-17-3` khi duyệt (nhánh này **không** merge); ghi sổ theo §10.
3. Nếu duyệt K1173-D6: một phiên K ngắn viết miễn Q37 (c) cho đoạn thẻ PP + selftest trước G2 T4. Nếu duyệt K117-D8 (A): phiên K làm thước biến cố đo trên video (K116-D4) trước G2 T4.
4. (Nhắc, không phải quyết định K) Cổng XEM CÂM §13.4 của T3 vẫn ghi "chủ dự án chưa chấm".
