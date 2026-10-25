**Nhánh thật: `ccr-21ab5d6f-7l1yln`** (harness buộc tên này; lệnh ghi `k2c-t4-02-animatic`). Gốc `origin/main` @`2414d1d3` + merge (không squash) `origin/claude/k2c-t4-02-giong-a24udn` @`5e5e02ce` (khớp SHA lệnh) → merge commit `b0ff47c9`. Đã đẩy, **không merge vào main**, không tạo PR.

# ANIMATIC-T4 — K2C-T4-02 London, mốc M3: animatic cả tập 640×360 có giọng — BÁO CÁO

Phiên ANIMATIC-T4, 24/10/2026 (đồng hồ container 01:35 → 13:10 UTC). Kiểm bằng checks **1.17.4** (`lock.py --verify` KHỚP `08486eb2…`). Không đọc mã trong `checks/` (chỉ chạy; đọc văn bản luật `RULES-LL.md` và báo cáo K1172/K1174 để biết tên trường khai).

## 0. Tóm tắt

| Hạng mục | Kết quả |
|---|---|
| Animatic đủ (ngoài git) | `/var/tmp/anim/out/k2c-t4-02-animatic-640.mp4` · 730,083 s · 17 522 khung · 640×360 · 24 fps · H.264 crf 20 + AAC 160 k · **SHA-256 `e4a4b09a75458e705dd6866f67076a0b41ce9776fefd3c9b62a6eeba45ebed47`** · 206,2 MB · tái tạo: `du_lieu.sh → dung.sh/dung2.sh (tệp máy animatic/may) → omni/chon + clip → tn_tl.sh → am.py → ghep.py → xuat.py` (`reports/animatic-t4/xuat.json`) |
| Bản xem (git) | `reports/animatic-t4/xem/k2c-t4-02-animatic-xem-{1,2,3}.mp4` = 4,84 / 4,81 / 4,85 MB (≤ 5 MB) · tờ khung `reports/animatic-t4/to-khung.jpg` |
| Âm | −14,0 LUFS · −1,9 dBTP · LRA 9,3 LU (đo trên animatic sau AAC; k2check A1/A2 ĐẠT) |
| k2check 1.17.4 có video | **TRƯỢT tổng** — 37 ĐẠT · 17 CẢNH BÁO · 10 TRƯỢT (mục 9); hàng T4 mới (BAN-DO-12, TU-LIEU-10, AI-TU-LIEU, GEMINI-NGAN-SACH, GOC-CAO-60) ĐẠT; MAY-19 còn 1 (c) cần K giải thích |
| XEM CÂM AI (tham khảo) | P chấm tay 7,5/8 mỗi người (Q4 1/2); từ khoá 8/8 — chủ dự án **chưa** chấm |
| Chi phí | Gemini T4 **$8,54** / $35 (phiên $7,10) · OpenAI **$4,61** / mốc $5 · Claude API **$4,83** / mốc $5 · ElevenLabs 0 · RunPod 0 · giờ máy ≈ 11,6 h / 14 h |
| Phiếu xem | `reports/animatic-t4/PHIEU-XEM.md` (A chỗ xem kỹ + A2 phiên đã thấy · B XEM CÂM 8 câu · C 14 quyết định) |

## 1. Quyết định áp (nguyên văn tinh thần lệnh)

- **PHIẾU GIỌNG:** "Duyệt G-1, G-2, G-3 theo khuyến nghị" → **G-1 = (c) K1-C1 730,1 s** (bỏ 7 câu L81, L41b, L45, L38, L77, L15, L54; 0 ký tự ElevenLabs) · **G-2 = (a)** · **G-3:** St Saviour's giữ bản gốc, Wenceslaus giữ, alias Evelyn "Eevlin".
- **Q1** minh hoạ Omni 20–23 % · **Q3** 8 điểm tiết kiệm Omni (đúng độ dài; ảnh đầu hoàn thiện; chế độ ảnh đầu + cuối; thư viện lệnh + danh sách cấm; ≤ 3 lượt/khoảnh khắc + sổ giây; nháp độ phân giải thấp nhất; kiểm 2 tầng, Flash trước; 720p → 1080p ở bản cuối) · **Q4** lượt ĐO ≤ $3 trên 2–3 khoảnh khắc trước; ngân sách Gemini T4 $35 (mốc $30), đã tiêu $1,44 trước phiên.
- **V1** tấm nền chỉ OpenAI `gpt-image-2.5-sunburst-2026-09-08`, chỉ 2026 ban ngày, mục tiêu 5–15 % · **V2** lửa cách A `look2.js` · **V5** P1 fov 36° · **V6** sương σ 1/10 km · **L3** người/xe/thuyền ≤ 60 m · **L4** City 1940 khối ước lượng · **L6** lõi khối 1666 ước lượng chỉ ở thẻ PP · trong phim không nhãn/chữ AI.
- **LỆNH BỔ SUNG 24/10/2026 12:55 (Hollar):** ĐÃ ÁP — xem mục 4.3 và `KIEM-TU-LIEU.md`.

## 2. Việc 1 — Giọng

Master giọng tái tạo bit-trùng bằng `tai_tao.sh` (0 ký tự): WAV `b9cec467…` OK, FLAC `e5d49871…` OK. Lời dựng K1-C1 `scripts/k2ldn/anim/loi_dung.py` → `/var/tmp/anim/am/loi-dung.wav` (SHA `187e059a…`, −14,0 LUFS), mốc `channel-k2/k2c-t4-02/animatic/loi-dung-moc.json` (115 câu dùng, 7 câu bỏ). Độ dài theo nhóm v1 `k1c1.py` (đệm 0,4 s, đuôi 1,0 s, sàn nối 6 s; sàn riêng H5-08 18 / H4-08 12 / H3-06 8): **730,083 s**.

## 3. Việc 2 — BANG-SHOT-v2 + kiểm trần + bảng so v1 ↔ v2

`channel-k2/k2c-t4-02/BANG-SHOT-v2.{md,json}` (`scripts/k2ldn/bang_shot_v2.py`): 74 shot, TB 9,87 s. Bảng so từng nhóm lời: **`reports/animatic-t4/SO-V1-V2.md`** (60 nhóm v1, 720,0 s → 730,083 s; mỗi dòng có căn cứ đổi).

| Lớp | Giây | % | Trần / mục tiêu | Ghi |
|---|---|---|---|---|
| 3D (A) | 556,4 | 76,21 | — | |
| Omni M-d | 148,7 | **20,36** | Q1 20–23 % | 23 clip / 17 khoảnh khắc (8 khoảnh khắc §15f + 9 mới — C3) |
| Tấm nền 2026 (N2P) | 33,5 | **4,59** | V1 5–15 % | **dưới mục tiêu** (P3-2026 trượt 3/3 — C2) |
| Tổng AI | — | 24,95 | N2P-6 ≤ 70 % | |
| Bản đồ (MAP + MAP3D) | 33,5 | 4,58 | ≤ 12 % | H1-09: MAP 5 → 3,5 s, MAP3D 4 → 5,5 s (mục 4.1) |
| Tư liệu + khắc + thẻ | 70,5 | **9,66** | ≤ 10 % | ±5 % |
| THAP | — | 9,21 | ≤ 12 % | |
| Góc cao + timelapse | 482,0 / 714,1 | 67,5 | ≥ 60 % (GOC-CAO-60) | k2check theo log khung |

Thay đổi chính v1 → v2 (đủ trong SO-V1-V2.md): H1-11 ↔ H1-12; H2-04a → M-d rồi trượt 3/3 (mũ lỗi thời đại) → **3D TRUOT P4**; H5-07a ảnh đầu trượt 3/3 → **3D P9 CODINH đêm**; H2-03 tách H2-03b 3D + H2-03c M-d Toà Cháy 1667 (giữ M-d ≥ 20 %); H3-02 3D TRUOT P6 1756 → 1832; H2-07 → M-d (Barbon 1680); H5-06 bỏ tấm nền; M01 / H5-04 / H5-05a tấm nền; KHAC: H1-03 & H2-12 met-360649-1, H1-13 ycba-266-0, H2-06 rijks-monument-0; **trong phiên sửa thêm:** H1-13/H1-15/H1-16 giờ như v1 (lỗi +24 h), H1-13 fov 30°, H1-09/H4-07 XUONG chuyển ≥ 4 s.

## 4. Việc 3–4 — Máy §19, dựng 3D, bản đồ, tư liệu, lớp §17, thẻ

### 4.1 Cú máy §19 (a)
- Tệp máy 54 (`channel-k2/k2c-t4-02/animatic/may/`, `scripts/k2ldn/anim/may_v2.py`): khoá mỗi 0,25 s, `easeKeys: false`. **P1 fov 36°** (V5). VONG ≤ 3°/s, CAU ≤ 6 m/s (lệnh) — đo thật: mọi shot ĐẠT.
- **Log máy từng shot vào git:** `channel-k2/k2c-t4-02/animatic/log-may/<mã>.json` (50 shot 3D, log.json của `render_look.js`, mỗi khung p/l/fov + ma trận view/proj + năm/giờ).
- Tự đo `kiem_may.py` trên 60 log thật: 0 TRƯỢT (H1-03 TRUOT 2,10 %/s sau hạ hệ số; trước 2,99 %/s sát trần 3). k2check MAY-19: (a) 0 · (b) 0 · (c) 1 · (d)–(f) 0 · (w) 0 sau sửa khai (mục 9.2).
- **Sửa trong phiên:** H1-09 và H4-07 XUONG chuyển 2,71 / 3,71 s < 4 s (k2check) → vận tốc hình thang (dốc 10 %), H1-09 bản đồ 2D 5 → 3,5 s → **chuyển 4,25 s** cả hai; dựng lại.
- **Đo trời + sương P1 fov 36°:** 7,1 % (2026) · 7,0 (1668) · 7,1 (1711) · 6,8 (1940) · 7,5 (1666 đêm) — ≤ 20 % ĐẠT, dưới cận 8 % của LOOK-2 (ghi tên ±: không trong ±5 % ngưỡng 20). Mái vòm St Paul's ở mép trái khung (x ≈ 18 %) — C6.

### 4.2 Dựng 3D toàn tập
640×360 spp 2, P = 2 (chờ RAM ≥ 5 GB), Chromium llvmpipe, 3–5,5 s/khung mỗi tiến trình. Hàng 1 (47 shot, look2) xong 07:55; hàng 2 (7 shot máy thấp, `look2d.js` = look2 + lớp người/xe L3) và hàng 3 (H1-03 Hollar, H5-07a) xong 09:30; dựng lại trong phiên: H1-13/H1-15/H1-16 (11:16–11:56), H1-09/H4-07 (12:37–12:43). Bản đồ Doornick hoạt hoá H1-09 (chiếu cùng máy + lửa `luoi_chay` + 3 nhãn), ranh 1666/1940, vành Heights H3-05, thẻ chương (5), thẻ nhân vật/bộ đếm §17, **bộ đếm năm §11.2** (thêm trong phiên), thẻ PP (2 thẻ 9 s + 7 s; L6 lõi khối 1666 ≈ 42 % — `animatic/the-phuong-phap.json`).

### 4.3 Tư liệu §19 b/c + lệnh bổ sung Hollar (ĐÃ ÁP)
Bảng kiểm 7 tư liệu (chữ đọc trên bản gốc + siêu dữ liệu nơi giữ): **`reports/animatic-t4/KIEM-TU-LIEU.md`**.
- met-360649-0 = SAU cháy, met-360649-1 = TRƯỚC cháy (đọc trên bản khắc) → H1-03, H2-12 đổi sang **-1**; H1-03 dựng lại; kiểm bằng mắt khung 1:15: dải "…BEFORE THE FIRE".
- Ghi công: "Wenceslaus Hollar, prospect of London before the Fire (etching, published 1666) — The Met, CC0"; **không gán 1647**. Bộ đếm năm H1-03/H2-12 đọc 1647 (lời L10 khoá — Long View) → chú thích trên hình thêm **"(pub. 1666)"**.
- Wren plan (LoC, khắc 1767) chú thích "Wren's 1666 plan, engraved 1767"; YCBA accession đoán → sửa thành URL manifest.
- Không thêm tư liệu mới (TU-LIEU 9,66 %); met-360649-0 chỉ đề xuất ở phiếu (C10).

## 5. Việc 5 — Tấm nền 2026 fov 36°, cổng (i)–(v), ≤ 3 lượt

| Điểm máy | Lượt | (i) | (ii) | (iii) T9b ≤ 2 % | (iv) | (v) | Dùng |
|---|---|---|---|---|---|---|---|
| P1-2026 | l1 | ĐẠT | ĐẠT | ĐẠT | ĐẠT | ĐẠT (M01, H5-04) | M01 [0, 11] s, H5-04 [4,417, 10,417] s |
| P9-2026 | l2 | ĐẠT | ĐẠT | **1,98 %** (±5 %) | ĐẠT | ĐẠT | H5-05a |
| P3-2026 | l1–l3 | — | — | TRƯỢT (nước → đất 3,5 / 28 / 39 %) | — | — | H5-06 dùng 3D V2 |

**Tỷ lệ đạt:** 2/3 điểm máy; 2/6 lượt OpenAI edits ($0,455). Tấm nền 4,59 % < 5 % (C2). k2check N2P-1…5 = CẢNH BÁO ở animatic ("chưa khai tấm kiểm `n2p.tam`" dù log shot có `n2p.tam` — xin K chỉ khuôn khai đúng; mục 9.3).

## 6. Việc 6 — Omni M-d

| Chỉ số | Số |
|---|---|
| Model | `gemini-omni-1.1-flash` (interactions API, ảnh đầu → video), 360p, khung giờ [0–N s] trong lệnh |
| Lệnh video | **30** · **$6,754** · ≈ 194 s sinh · **$0,0348/s** |
| Kiểm tầng 1 (Flash `gemini-3.8-flash`) | 62 lệnh · $0,35 |
| Kiểm tầng 2 | `gpt-6.1-sol` 3 khung + `q_thoi_dai` (Claude) mỗi clip |
| Khoảnh khắc / clip dùng | 17 khoảnh khắc · **23 clip · 148,7 s** (tỷ lệ dùng 148,7 / 194 ≈ **77 %**) |
| Lượt / khoảnh khắc | ≤ 3 (sổ giây `reports/animatic-t4/md-so-giay.jsonl`; H4-04b 3 lượt — sổ có một dòng lượt 1 ghi trùng do lượt ĐO) |
| Trượt 3/3 → 3D | H2-04a (mũ bowler/chóp tròn — lỗi thời đại), H5-07a (ảnh đầu 2026 có chữ/biển) |
| Ảnh đầu | ảnh tĩnh OpenAI generations 2560×1440 (34 lệnh, 32 OK, $2,039; 2 lỗi 502 tính lượt, $0) — render 3D tầm người không dùng được (máy nằm trong khối) |
| Lượt ĐO (Q4) | 3 khoảnh khắc khó (H1-02, H1-12, H4-04b) $0,72 ≤ $3 |

Bản cuối (Q3 điểm 8): sinh lại 720p các lệnh đã chọn ≈ 149 s × $0,10 ≈ **$15–16** (C1).

## 7. Việc 7 — Âm thanh nháp

`scripts/k2ldn/anim/am.py` → `/var/tmp/anim/out/am-nhap.wav`; cue `animatic/am-cue.json`. Nhạc Scott Buckley CC BY 4.0 (Katabasis I, Hiraeth, Echoes, Undertow, Never Dying — RIGHTS K2-MUS-6…13 / T3-MUS-DUNG); SFX CC0 BigSoundBank/OpenGameArt + NPS (tài sản công Mỹ) từ `reports/sfx-t3/ung-vien`. Trên animatic: **−14,0 LUFS · −1,9 dBTP**; k2check A1, A2, A5, A7, A8, A9 ĐẠT (A4 chỉ báo: không có stem).

## 8. Việc 8 — Ghép, xuất, episode.yaml

`ghep.py` (LUT kênh, KHOP hoà 1 s, tấm nền hoà 2 s, M-d khớp màu Lab 0,7, lớp chồng) → `xuat.py` (animatic đủ + 3 phần ≤ 5 MB + tờ khung) → `mk_ep.py` → `channel-k2/k2c-t4-02/animatic/{episode.yaml, log-shot.json, timeline.json, nhip-vat.json, so-ai-gemini-t4.jsonl, so-ai-openai-t4.jsonl, sha-tu-lieu-t4.txt, xem-cam.json, log-may/}`.

## 9. Việc 9 — k2check 1.17.4 (animatic, có video, có ASR)

Lệnh: `/opt/cine/bin/python checks/ll/k2check.py channel-k2/k2c-t4-02/animatic/episode.yaml --tl …/timeline.json --master <animatic e4a4b09a…> --cap`. Bản đầy đủ: **`reports/animatic-t4/k2check-1.17.4-animatic.md`**.

### 9.1 Bảng hàng

| Hàng | Kết quả | Số / lý do |
|---|---|---|
| **BAN-DO-12** | ĐẠT | 33,5 / 730,1 s = 4,58 % |
| **TU-LIEU-10** | ĐẠT (±5 %) | 70,5 s = **9,66 %** (TL 8 · KHAC 16 · THE 46,5) |
| **AI-TU-LIEU** | ĐẠT | 7 shot tư liệu · 17 SHA · 219 dòng sổ AI đối chiếu |
| **GEMINI-NGAN-SACH** | ĐẠT | 105 lệnh · $8,54 / $35 (mốc $30) |
| **GOC-CAO-60** | ĐẠT | 482,0 / 714,1 s = 67,5 % |
| **MAY-19** | CẢNH BÁO | 50 shot · log khung 50 · THAP 9,2 % · lỗi (c) 1: H5-07b KHOP "lệch 62 139 px" (mục 9.3) |
| K-LAI-3 | ĐẠT | 23/23 đoạn có tệp kiểm, kết luận máy ĐẠT |
| K-LAI-4/5/6/B, K-LAI-3V | ĐẠT | K-LAI-6: 57 lệnh, C2PA 53/53 |
| CHUONG-1 | ĐẠT (±5 %) | 5 thẻ, mỗi thẻ 3,0 s = trần 3 s |
| NHIP-NGHIA | ĐẠT | 64/64 nhịp chính có vật mang nghĩa |
| N2P-6 | ĐẠT | tấm nền 6,1 % (theo shot) · minh hoạ 20,4 % · tổng 26,5 % |
| A1–A9 (âm) | ĐẠT | −14,0 LUFS · −1,9 dBTP · 0 lặng · 0 chạm trần · ASR 0 lỗi |
| LOCK | ĐẠT | KHỚP |
| **K-LAI-1** | **TRƯỢT** | 148,67 s = **20,4 % > 20 %** — mâu thuẫn với Q1/Q2 (C11) |
| **K-LAI-2** | TRƯỢT | (d) chưa khai `phat_hanh.mo_ta` — thuộc gói phát hành |
| **XEM-CAM** | TRƯỢT | chủ dự án chưa chấm (AI TB 7,5/8) — chờ PHIEU-XEM mục B |
| **Q37 / NHIP-K2 / Q37 (1.13)** | TRƯỢT | (a) 12 mốc lớp chồng khai không khớp biến cố đo ±0,3 s (mờ vào 0,4–0,5 s); (c) khoảng 16,5 s, (d) khung tĩnh 10,4 s từ 10:43 (H5-05a tấm nền) — C14 |
| **SACH-1** | TRƯỢT | (c) không có log chữ `--logs k2.js` (ghép bằng `ghep.py`, không qua k2.js) |
| Q26b, Q26b-K2, Q34 | TRƯỢT | luật kênh 1 / cũ: "bối cảnh" theo cảnh tl/*, type `minh_hoa` ngoài danh sách Q34 — như animatic T3 |
| PP-1 | CẢNH BÁO | (e) PP2 24 từ / 7 s = 3,4 từ/s (the-phuong-phap.json đếm 19 từ — hai cách đếm khác nhau, chưa rõ; bản cuối rút câu PP2 hoặc kéo 8 s) |
| TL-1 | CẢNH BÁO | 67,5 % < 75 %; 6,39 cắt/phút > 5; H1-07 trôi 2,09 %/s (±5 %); M03/M04 trôi |
| TL-2 | CẢNH BÁO | lướt thấp 11,7 % > 10 % |
| MINH-HOA | CẢNH BÁO | (c) 12 đoạn M-d liền nhau không kẹp 3D (C8) |
| BIEN-CO-V, TL-3, ML1, O2, CONG-BO-1, N2P-1…5, NC-H2/H3 | CẢNH BÁO | ở animatic; BIEN-CO-V chỉ ghi: 1 718 biến cố đo, TB 0,55 s, dài nhất 16,5 s, ranh shot bắt 73/74 (98,6 %) |

### 9.2 Sửa KHAI trong phiên (không đổi hình/tiếng)
1. **Log máy hệ cảnh:** MAY-19 đọc `cam.p` theo hệ cảnh y-lên (như log T3); log `render_look.js`/`render_ldn.js` ghi [E, N, h] → `mk_ep.py` ghi thêm `cam` hệ cảnh (x = E − 532000, y = h, z = −(N − 180800) — đúng hệ `look2.js` và ma trận view trong log), giữ `cam_en` gốc. **MAY-19 42 → 3 → 1 cảnh báo** (2 lỗi XUONG còn lại là thật, đã sửa hình).
2. **Minh hoạ theo mục đoạn** `minh_hoa: [{ma, t0, t1, luot, kiem, so_ai}]` (K1172): K-LAI-3 0 → 23/23 ĐẠT.
3. **Chữ thẻ PP** khuôn T3 `p.card.items`: PP-1 (d) TRƯỢT → ĐẠT.
4. `xem-cam.json` (khuôn T3) + điểm P đọc tay.

### 9.3 Câu hỏi cho K (đề xuất ghi `checks-appeal.md` — phiên này không được sửa tệp đó)
- **A1.** K1174 §5 nói `log_may` = log.json `render_ldn.js` (ghi [E, N, h]) nhưng MAY-19 đọc hệ cảnh → xin ghi rõ hệ toạ độ trong RULES-LL (hoặc MAY-19 dùng `goc_toa_do` để đổi).
- **A2.** MAY-19 (c) H5-07b KHOP "lệch 62 139 px": tự chiếu điểm neo [532118, 181150, 111] qua ma trận máy → **0 px** giữa hai nửa a/b và với khung đầu M03; xin xem cách (c) chọn khung so khi `khop_voi` là shot DAY.
- **A3.** K-LAI-1 (≤ 20 % `ai_image`) mâu thuẫn Q2/1.17.4 (bỏ trần 20 % M-d từ T4) ở đúng dải Q1 20–23 %.
- **A4.** Q37 (a): lớp chồng mờ vào 0,4–0,5 s → biến cố đo trễ > 0,3 s so với mốc khai; phiên không dịch mốc để khớp thước.
- **A5.** N2P-1…5 báo "chưa khai `n2p.tam`" dù log shot có `n2p: {tam: [{tag, kiem, ghep, v, khoang_s}]}` — xin khuôn đúng.

### 9.4 XEM CÂM AI (tham khảo — không thay chủ dự án)
3 vai `claude-sonnet-5-5` (chỉ Read; 1 khung/4 s 320×180; không tiếng, không phụ đề). Lượt 1 (bản trước sửa H1-13): từ khoá 48/48 nhưng đọc tay **Q4 0/3 người** → truy gốc ra **lỗi +24 h** (mục 11). Lượt 2 (sau sửa, animatic `ae7dadbb…`; bản cuối `e4a4b09a…` chỉ khác máy H1-09/H4-07): cả 3 thấy "toà giống nhà thờ có tháp giữa đám cháy" nhưng "Not sure" kết cục → P chấm tay **Q4 = 1/2, 7,5/8 mỗi người**. Chi phí 2 lượt $0,762. Kết quả: `reports/animatic-t4/xem-cam/ket-qua.json`, khai `animatic/xem-cam.json`.

## 10. Việc 10 — PHIẾU XEM

**`reports/animatic-t4/PHIEU-XEM.md`**: A (69 chỗ xem kỹ theo mã + vị trí trong 3 tệp xem) + A2 (10 điều phiên đã thấy) · B XEM CÂM 8 câu, ngưỡng ≥ 6/8 (chủ dự án chấm — phiên không chấm mù) · C 14 quyết định, mỗi mục phương án / ưu / nhược / tác động / rủi ro / khuyến nghị.

## 11. Sự cố

1. **Lỗi +24 h ở BANG-SHOT-v2** (H1-13, H1-15, H1-16: h66 90/92/94 thay vì 66/68/70 như v1) → H1-13 (Old St Paul's cháy) dựng ở 5/9 khi vùng đã cháy xong: không thấy nhà thờ, bộ đếm ngày lùi 5 → 4 SEPT. Phát hiện nhờ XEM CÂM Q4. Sửa giờ + H1-13 fov 42° → 30° (thử 1 khung trước), dựng lại 3 shot. Các shot h66 khác khớp v1.
2. **Hai lỗi đệm:** `mk_ep.py` không chép đè log máy khi shot dựng lại; `ghep.py` giữ đệm LUT cũ → một bản ghép mang khung cũ của 3 shot (phát hiện khi xem khung, chưa commit bản xem sai). Sửa so mtime; rà: chỉ 3 shot dính.
3. **Commit ≈ 244 MB ảnh lát kiểm** (`animatic/omni/kiem2/qtd-*/`, PNG; mỗi tệp < 5 MB, preflight ĐẠT) đã đẩy ở commit "M-d 22/24…" → không force-push/amend; `git rm --cached` + `.gitignore`; lịch sử nhánh vẫn mang ≈ 244 MB.
4. **Trình chờ `pgrep -f` tự khớp chính dòng lệnh** → máy rỗi ≈ 56 phút (09:30–10:26); một lần `pkill -f` dừng nhầm shell của chính nó (k2check bị huỷ — đã định huỷ). Bài học: lọc PID tiến trình, không lọc theo chuỗi lệnh.
5. Tiến trình ghép tách nền bằng `( … &)` bị ngắt khi shell thoát → chạy lại bằng tác vụ nền.
6. OpenAI 502 ×2 ở H1-14 (tính 2 lượt, $0). verify.sh 5 TRƯỢT lúc khởi động → cài OpenEXR/tifffile/pyshp, `npm ci`, pyproj 3.8.0 + OSTN15 (`5d6ed64d…`).

## 12. Chi phí (mốc / chặn / thật)

| Nguồn | Mốc | Chặn | Thật | Ghi |
|---|---|---|---|---|
| Gemini (T4 tổng) | $30 | $35 | **$8,54** (phiên $7,10) | Omni 30 video $6,754 · Flash 62 $0,35 · khác |
| OpenAI | $5 | $10 | **$4,61** (±5 % mốc → nêu tên) | ảnh đầu generations 34 $2,039 · edits tấm nền 6 $0,455 · kiểm gpt-6.1-sol 87 $2,111 |
| Claude API | $5 | $15 | **$4,83** | kiểm tấm nền $0,757 · q_thoi_dai ≈ $3,31 (tệp kiểm giữ $3,115) · XEM CÂM 2 lượt $0,762 |
| ElevenLabs | 0 | 1000 ký tự | **0** | master tái tạo |
| RunPod | 0 | — | **0** | |
| Giờ máy | 14 h | — | ≈ **11,6 h** | |

Sổ: `reports/animatic-t4/so-ai-gemini.jsonl`, `so-ai.jsonl`, `cost.jsonl`, `xem-cam/cost.jsonl` (model, lệnh nguyên văn, SHA vào/ra, usage, giá).

## 13. Chỉ số trong ±5 % quanh ngưỡng (nêu tên)

M-d 20,36 % (Q1 cận dưới 20) · K-LAI-1 20,4 % (trần 20) · TU-LIEU-10 9,66 % (trần 10) · tấm nền P9 (iii) 1,98 % (trần 2) · tấm nền 4,59 % (mục tiêu 5; −8 %, nêu thêm) · TL-1 H1-07 trôi 2,09 %/s (trần 2) · thẻ chương 3,0 s (trần 3) · thẻ PP1 9,0 s (cận trên) / PP2 7,0 s (cận dưới) · PP1 3,0 từ/s (trần 3) · M-d dài nhất 8,0 s (trần 8) · MÓC 4 loại cú máy (sàn 4) · HỒI 5 chuỗi cùng loại 2 (trần 2) · A1 −14,0 LUFS · OpenAI $4,61 (mốc $5) · Claude $4,83 (mốc $5) · XUONG chuyển 4,25 s (sàn 4; +6 %, nêu thêm).

## 14. Dòng sổ đề xuất (P ghi — phiên này không sửa sổ)

- **COST-LEDGER:** `2026-10-24 · ANIMATIC-T4 · Gemini $7,10 (T4 tổng $8,54/$35) · OpenAI $4,61 · Claude API $4,83 · ElevenLabs 0 · RunPod 0 · ≈ 11,6 h máy`.
- **AUTHORSHIP:** chủ dự án duyệt PHIẾU GIỌNG G-1 (c) K1-C1, G-2 (a), G-3 (St Saviour's/Wenceslaus/"Eevlin"); Q1 M-d 20–23 %; Q3 8 điểm Omni; Q4; V1/V2/V5/V6; L3/L4/L6; lệnh bổ sung Hollar (đọc tấm trước/sau cháy, ghi công không 1647) — đóng góp biểu đạt: chọn nhịp lời K1-C1, tỷ lệ minh hoạ, cách ghi công tư liệu. (Quyết định C1–C14 chờ.)
- **RIGHTS:** Hollar met-360649-1 "prospect of London before the Fire (etching, published 1666) — The Met, CC0"; YCBA 266 (PD, manifest URL); Rijksmuseum monument + Doornick RP-P-OB-82.345 (PDM); LoC Wren plan 1767 (PD); NGA Wren (CC0); nhạc Scott Buckley CC BY 4.0 (5 bài); SFX CC0 BigSoundBank/OpenGameArt + NPS; ảnh đầu OpenAI `gpt-image-2.5-sunburst-2026-09-08` + clip `gemini-omni-1.1-flash` (tạo bởi dự án, C2PA theo sổ).
- **BAI-HOC-K2:** (1) XEM CÂM AI đọc tay, không tin bộ chấm từ khoá — nó che lỗi Q4; (2) mọi bộ đệm (log máy, LUT) phải so mtime với nguồn; (3) không chờ/giết tiến trình theo chuỗi lệnh (`pgrep -f` tự khớp); (4) giờ `h66` phải đối chiếu ngày trong v1 bằng bảng tự động trước khi dựng; (5) XUONG đo chuyển −85° → −35°: shot ≤ 5,5 s cần vận tốc hình thang.
- **lfs-allow:** không cần (mọi tệp git ≤ 5 MB; bản xem 4,81–4,85 MB).

## 15. Việc chờ chủ dự án

1. **Xem 3 tệp `reports/animatic-t4/xem/` một lần**, nhận xét theo mã shot (PHIEU-XEM mục A, A2).
2. **XEM CÂM 8 câu** (mục B) — cổng XEM-CAM cần chủ dự án ≥ 6/8.
3. **Quyết định C1–C14** (mục C): đặc biệt C1 (M-d 720p ≈ $16), C2 (tấm nền 4,59 %), C11 (K-LAI-1 — chờ K), C12 (Q4 nhà thờ), C14 (H5-05a nhịp).
4. Chuyển câu hỏi A1–A5 (mục 9.3) cho phiên K.

**DỪNG chờ chủ dự án.**
