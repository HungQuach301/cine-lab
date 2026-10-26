**Nhánh thật: `claude/k2c-t4-02-final-a-0pb0bh`** (harness buộc; lệnh ghi `k2c-t4-02-final-a`). Đẩy nhánh, KHÔNG merge, KHÔNG tạo PR.

# BAN-CUOI-T4-A — bản cuối T4 London (K2C-T4-02), PHẦN THỬ + CHUẨN BỊ — BÁO CÁO

> Phiên 25/10/2026 23:30 UTC → 26/10 ≈ 02:30 UTC (26/10 06:30 → ≈ 09:30 Asia/Saigon). Mọi số là số đo thật trong phiên; số đo ở `reports/ban-cuoi-t4-a/` và `channel-k2/k2c-t4-02/ban-cuoi/`.
> **Căn cứ (nguyên văn, Asia/Saigon):** 25/10 06:56 nhận xét animatic (1. 10 giây đầu gần như đứng và xấu; 2. thiếu điểm nhấn sự kiện, nhân vật, công trình biểu tượng; 3. nới Gemini, thêm cảnh cận/trung; 4. thêm ảnh, footage thật); 09:08 "Vấn đề tôi concern nhất là chỉ phí bị đội nhiều, còn các vấn đề khác đều có thể nới để tăng chất lượng và độ chân thực của hình ảnh / Người xem cũng không phải là người chuyên về khảo cổ hay gì để có thể nhận ra những dự khác biệt nhỏ trong những frame hình ngắn"; 09:15 gói "50 % tiết kiệm"; 21:35 "Các hình 3D hiện đại đang rất yếu so với hình từ Omni"; 26/10 00:07 "Chọn hướng cho cảnh hiện đại: A+B+E (khuyến nghị)"; 00:12 "Duyệt phiếu xem v2 theo khuyến nghị"; chủ dự án dán lệnh phiên này sau khi trả lời "K1178-D1…D6 theo khuyến nghị".
> Email chủ dự án không có trong tệp/commit/header/URL/payload/User-Agent nào (UA `CineLab-research (+https://github.com/HungQuach301/cine-lab)`). Khoá API do proxy gắn — không in/ghi khoá. Không đọc mã `checks/` (chỉ chạy `k2check.py`, `q_thoi_dai.py`, `lock.py --verify`; dùng tệp mô hình YuNet `checks/models/…onnx`).

## 0. Nhánh, SHA, khối vận hành

| Mục | Lệnh | Thực tế |
|---|---|---|
| Gốc | origin/main @e97fc214 | **e97fc214** (khớp; K-1.17.7 + ANIMATIC-T4-V2 có sẵn) |
| Merge K-1.17.8 | origin/claude/k1178-t4-london-rules-pdjfmz @297eb070, `--no-commit` + preflight, merge-tree sạch | đỉnh **297eb070** khớp; merge-tree sạch; `--no-commit` → preflight "91 tệp — ĐẠT · lock KHỚP · PREFLIGHT ĐẠT" → commit **`00a2f096`** (no-ff, không squash) |
| LOCK | `--verify` KHỚP 1.17.8 `045b7bb7…` | **KHỚP** `045b7bb7414364d4732fe22c4b643ae04d7a0e19ae25f0e839de149379d3185a` ở mọi commit (preflight gọi `lock.py --verify`); không gọi `lock.py` thiếu `--verify` |
| Vùng sửa | `channel-k2/k2c-t4-02/**` (thư mục mới `ban-cuoi/`), `design/k2v/ldn/**`, `scripts/k2ldn/**`, `reports/ban-cuoi-t4-a/**` | chỉ `channel-k2/k2c-t4-02/ban-cuoi/**`, `scripts/k2ldn/bc/**`, `reports/ban-cuoi-t4-a/**` (+ merge K). KHÔNG sửa `checks/`, `checks-appeal.md`, `docs/`, sổ, `tools/`, `channel-k2/k2c-t3-01/**`, bảng/lời/animatic cũ, main, nhánh khác. Không sửa `design/` (dùng nguyên `thu-b/look3.js`) |
| Preflight | `set -o pipefail`; chỉ commit khi "— ĐẠT" | `reports/ban-cuoi-t4-a/cam_commit.sh` (pipefail; commit chỉ khi có "— ĐẠT" và "PREFLIGHT ĐẠT"); 1 lần CHẶN đúng (video 5,4 MB) → bỏ tệp, commit lại |
| Hook | trước lần đẩy đầu | pre-commit + pre-push → `tools/preflight.sh` cài 23:33 UTC; lần đẩy đầu 23:46 |
| Đẩy ≤ 30 phút + CHECKPOINT | bắt buộc | 18 commit trên nhánh sau merge, mỗi commit đẩy ngay (khoảng cách ≤ 30 phút); `reports/ban-cuoi-t4-a/CHECKPOINT.md` |
| Force/amend/dừng hỏi | không | không |
| Tiến trình nền | PGID, một vòng nặng một lúc, P ≤ 2, RAM ≥ 5 GB | hàng dựng `scripts/k2ldn/bc/dung_bc.py` (P = 2, chờ RAM ≥ 5 GB); chuỗi 1/2/3 theo PGID (2328, 4833, 20097, 31528); dừng chuỗi 3 bằng `kill -- -PGID`. **Lệch nêu rõ:** k2check/ghép video/API chạy cạnh 2 tiến trình dựng (việc nhẹ CPU; không có 3 tiến trình dựng cùng lúc); **một lần dùng `pgrep -f`** chỉ để in kiểm (không dừng gì) — trái bài học #112, ghi lại |
| Tệp tốn tiền vào git ≤ 10 phút | bắt buộc | ảnh OpenAI, clip Omni ≤ 5 MB, tệp kiểm vào git trong cùng lượt commit sau khi về (≤ 10 phút); video kiểm > 5 MB ngoài git + SHA (`ban-cuoi/e/video/SHA256-video-kiem.txt`, `ban-cuoi/b/tam/*/video-sha-*.txt`) |
| Sổ AI | mọi lệnh gọi | OpenAI `reports/ban-cuoi-t4-a/so-ai.jsonl` + `cost.jsonl`; Gemini `so-ai-gemini.jsonl`; **Claude `so-ai-claude.jsonl` (64 dòng, có `usd` từng lệnh q_thoi_dai + mô hình nhìn k2check)**; tổng hợp `do/chi-phi.json` (`scripts/k2ldn/bc/chi_phi.py`) |

## 1. Việc 1 — THỬ E (cổng trước khi dựng, §15 (k) điều kiện 2)

**Cách làm.** Dữ liệu LDN tái tạo bằng `scripts/k2ldn/anim/du_lieu.sh` (23:35 → 23:51 UTC; 2 lỗi tải tư liệu không dùng: Ogilby 429, NGA Wren). Hình học **look3d** (THU-B D, `hinh_hoc_thub.py d` chạy nguyên qua `scripts/k2ldn/bc/hinh_hoc_e.py`): 95 393 nhà thường, 4 599 255 tam giác; **look3e** = cùng hình học + mã 24 bit **3 485 toà OSM có tên** (để mặt nạ `mat_na_ct` có che khuất đúng). Nướng lightmap look3d 9 mốc.
Render 1920×1080 look3 cờ d spp 24 + mặt nạ 1 (`nha_thuong` 215 / `nha` 235 / nước…), mặt nạ 2 (mã công trình mốc → mái vòm St Paul's), mặt nạ 3 look3e (toà có tên). `mat_na_ct` + `toa_co_ten` gồm **mọi** toà có tên ≥ 50 điểm và mái vòm St Paul's (`scripts/k2ldn/bc/ghep_e_bc.py prep`).
Ảnh AI: OpenAI `gpt-image-2.5-sunburst-2026-09-08` edits, không mặt nạ, lệnh theo mẫu `reports/k1178/do/e/lenh-ngay.txt` (+ cấm xe/người/thuyền/chữ, không phản chiếu) — `channel-k2/k2c-t4-02/ban-cuoi/e/lenh-*.txt`. Ghép: lớp (a)-E (nha 235 ∪ nước ∪ bờ ±8 px ∪ tàu) nở 1 px (vật < 60 px nở 3 px) = render đúng từng điểm; chuyển mềm 2 px phía AI.

**Phát hiện lớn — "toà có tên OSM" gồm cả tên cửa hàng:** P9 151 toà (Superdrug, H&M, Wasabi…) → lớp (a)-E 13,96 % khung; P1 247 toà → 38,16 %. Tấm ghép loang lổ 3D ↔ AI. Phiên làm thêm **mặt nạ "tháp"** (toà có tên đỉnh ≥ 75 m ODN + Guildhall, Royal Exchange, Bank of England, Mansion House, Tower of St Mary Somerset → giữ 3D; toà tên thấp → nhà thường): P9 10 toà / 5,74 %; P1 17 toà / 28,36 %. Kiểm cả hai; chọn ở E1 (KN-5).

| Tấm | Lượt | $ | Mặt nạ | N2P-1 | N2P-2 | N2P-3 | N2P-4 | N2P-5 (video 3 s 640, lớp (a)-E ghép lại từng khung) | N2P-E | Kết |
|---|---|---|---|---|---|---|---|---|---|---|
| P9-2026 ngày | 1 | 0,076 | đủ | CB (12 cụm dải 20 px) | ĐẠT | ĐẠT | ĐẠT | ĐẠT 0,071 / trần 3,28 | CB 5 (w) | **0 Chặn** |
| | | | tháp | **2 Chặn mô hình "bờ"** (KN-1) | ĐẠT | **Chặn mô hình "bờ"** | ĐẠT | ĐẠT 0,035 | ĐẠT | Chặn = K1178-D2 → ngoại lệ đề xuất |
| P1-2026 ngày | 1 | 0,076 | đủ / tháp | CB | ĐẠT | ĐẠT | **TRƯỢT: người AI trên quảng trường** (soi: đúng) | — | CB | lượt 2 |
| | 2 | 0,076 | đủ | CB (8) | ĐẠT | ĐẠT | ĐẠT | ĐẠT 0,164 | CB 6 (w) | **0 Chặn** |
| | | | tháp | CB (5) | ĐẠT | ĐẠT | ĐẠT | ĐẠT 0,072 | CB 6 (w) | **0 Chặn** |
| P9-2026 đêm (render đêm V2 thật, không giảm sáng giả) | 1 | 0,076 | đủ | **TRƯỢT 9 (mô hình)** | ĐẠT | ĐẠT | ĐẠT | — | **TRƯỢT (g) chữ/biểu tượng sáng** | **TRƯỢT → H5-07a giữ 3D** |
| | | | tháp | CB | ĐẠT | ĐẠT | ĐẠT | — | **TRƯỢT (g)** | |
(k2check 1.17.8 mức G2 `animatic: false`, `--n2p-vision`; bảng đủ `ban-cuoi/e/kiem/*/k2check.md`; câu trả lời thô mô hình `…/vision/`. N2P-6 TRƯỢT trên các episode thử là do khuôn 1 tấm = 100 % AI — không phải tập.)
- **Soi bằng mắt:** (w) "tháp bịa" máy ở P9 = 3 toà cao KHÔNG tên có thật trong render (AI chỉ đổi vật liệu) → báo nhầm; (w) mô hình = cụm tháp nhỏ xa chân trời trái do AI thêm (thật, nhỏ) (`e/soi-thap-bia-P9.jpg`). Ô phóng đường phố P9: không xe/người. P1 lượt 1: người nhỏ + vật tối trên quảng trường (`e/soi-P1-nguoi-P9-goc-bo.jpg`) → lượt 2 hết. Góc "bờ" P9 tháp: AI vẽ mép kè/nước ở dải ≈ 10 × 190 px sát mép dưới, ngoài dải bờ 8 px; T9b/T9c 0.
- **(c) Đêm:** ngoài (g), mái vòm 3D không có đèn pha (AI có) — tấm đêm lộ khối vòm tối giữa thành phố sáng; theo §15 (k) giữ 3D.
- **(d) Chuyển động:** chỉ lớp (a)-E ghép từ 3D + N2P-5. Đề xuất đẩy 2D chậm trên tấm E → `khieu-nai-K.md` KN-6 + phiếu; KHÔNG dùng.
- **(f) Tờ so** `reports/ban-cuoi-t4-a/e/so-<khung>-<lượt>.jpg` (render | AI | ghép + 3 ô phóng ×2; 1,12–1,36 MB).

## 2. Việc 2 — Điểm đứng P1 (C3 c)
Render look3 d 1080p spp 16 + mặt nạ 2, 3 khung × 3 điểm (dời cả điểm nhìn — giữ hướng, fov 36°): `p1/to-p1.jpg`, `p1/do-p1.json`.

| Khung | Hiện tại | Tây 60 m | Tây 80 m |
|---|---|---|---|
| Mái vòm x % (M01 2026 = H4-05 1940) | 18,2 | 24,2 | 26,2 |
| Lửa M03 1666: x5–x95 % | 76,6–98,1 | 84,3–99,4 | 87,0–99,4 |
| Lửa M03: % điểm lửa sát mép phải (3 %) | 7,85 | 21,94 | 31,74 |
**Khuyến nghị giữ điểm hiện tại (+ C6 4°):** dời 80 m chỉ được 26 % (chưa 30 %) mà lửa dồn ra mép ×4. Nếu dời: dựng lại **16 shot P1 = 157,9 s** (M01–M04, H1-08b, H1-16, H2-05, H2-09, H3-01, H3-06, H4-01a, H4-05, H4-06, H5-04, H5-07b, H5-08). Mọi bước sau dùng điểm hiện tại.

## 3. Việc 3 — Mẫu 1080p bản cuối (D + B)
**D:** 6 khung look3 cờ d 1920×1080 spp 4 (sản xuất), 12 khung liên tiếp giữa shot: `mau/mau-*-1080.jpg`, `mau/to-mau-6.jpg`; giờ `do/gio/mau-*.time.json`:

| Mẫu | s/khung (mỗi tiến trình, P = 2) | Nạp cảnh |
|---|---|---|
| M01 · H1-08b · H2-10 · H3-05 · H4-04a · H5-08 | 16,77 · 19,07 · 17,59 · 14,43 · 18,21 · 16,88 (TB 17,16) | 16,1–17,5 s |
Tự soi: đỡ "đồ chơi" ở 1666/1708/1937; **đêm 2026 (H5-08) yếu** (vòm tối, lưới cửa sổ lặp); H2-10 dùng look3 thay look2d (không có người tầm phố — ghi cho phiên B).

**B (≥ 4 px/m, tỉ số bóng, máy cố định)** — dùng nguyên `scripts/k2ldn/thu-b/bmn_thub.py` qua thư mục ánh xạ (`scripts/k2ldn/bc/b_bc.sh`), kiểm `kiem_b_bc.py`:

| Khung | Nhà ≥ 4 px/m · % khung AI | Lượt | BE-MAT-NHA | N2P-1/2 | Ghi |
|---|---|---|---|---|---|
| H5-06 (P3 2026) | 36 / 1 578 · 15,0 % | 1 | **0 Chặn**, (b) 0/255, video (e) TV 0,0027; (w) 36 cạnh màu mới | N2P-1 CB 4 (lan can/kính AI thêm), N2P-2 ĐẠT | Claude lần đầu không đọc đủ 8 ảnh → (c) THIẾU; chạy lại đủ |
| H2-12b (P2 1711) | 93 / 14 305 · 6,9 % | 1 | **TRƯỢT** (c) lỗi thời đại 1720 | N2P-2 TRƯỢT | **lỗi lệnh của phiên**: ghi "nhà gạch mới" cho cả khung — Southwark (tiền cảnh) không cháy 1666, AI đổi nhà gỗ → gạch Georgian + cửa mái |
| | | 2 | **0 Chặn**, (w) 3 cạnh | ĐẠT / ĐẠT | lệnh sửa: Southwark giữ khung gỗ |

**Ước giờ dựng cả tập 1080p 24 fps:** lớp D + E bảng v4 = **544,2 s = 13 061 khung** (lệnh nêu lớp A ≈ 563 s ở v3; v4 chuyển 19 s sang Omni/THAT). Thông lượng đo 17,16 s/khung/tiến trình ÷ 2 = **8,58 s/khung → ≈ 31,1 h máy** (> 12 h). Theo chương: MÓC 3,9 h · HỒI 1 8,5 h · HỒI 2 7,8 h · HỒI 3 2,6 h · HỒI 4 3,1 h · HỒI 5 5,3 h. **Đề xuất chia:** B1 = HỒI 1 + HỒI 3 (≈ 11,1 h) · B2 = MÓC + HỒI 2 (≈ 11,7 h — sát trần) · B3 = HỒI 4 + HỒI 5 (≈ 8,4 h) + ghép, âm, xuất, Omni 720p, kiểm. Số đo khi có việc nhẹ chạy cạnh → có thể dư 5–15 %. Mỗi phiên đẩy khung/đoạn đã dựng lên LFS trước khi kết thúc (BAI-HOC #109).

## 4. Việc 4 — Omni 360p lượt nháp cuối
Ảnh đầu **dựng từ render 3D CÙNG NĂM** (look3 cờ d, máy tại chỗ sự kiện — `channel-k2/k2c-t4-02/ban-cuoi/may/md-*.json`, tờ máy `scripts/k2ldn/bc/may_md_bc.py`) + OpenAI edits (`oai_bc.py`; nhân vật có tên + chân dung tham chiếu). Lệnh nêu lỗi đo được theo năm (1666: không mái vòm, không tricorn, chỉ cầu London cũ có nhà; 1675: chưa có mái vòm, không tháp kiểu Big Ben; 1708: chỉ một cầu, không tàu lớn thượng lưu cầu) — `ban-cuoi/omni/lenh/`. Trình chạy `scripts/k2ldn/bc/md_bc.sh`: ảnh đầu → Flash ảnh (câu hỏi mốc) → Omni 360p → Flash clip → tầng 2 (gpt-6.1-sol + q_thoi_dai) → q_thoi_dai **lớp công trình mốc** 3 khung. Mức ĐỦ cho mọi clip; ≤ 2 lượt.

| Mã | Lượt | Kết | Lỗi đo được |
|---|---|---|---|
| **H1-06x** sà lan hoàng gia (Charles II, James) | 1 | **CHỌN** | — (YuNet: không mặt nào) |
| **H1-15x** nhà Vua + Công tước ở tuyến chữa cháy | 1 | **CHỌN** | — (YuNet mặt lớn nhất 0,031 khung) |
| H2-02b bàn bản vẽ bên cửa sổ | 2 | TRƯỢT | l1: lớp mốc — cột kiểu Monument trên chân trời 1666; l2: mái vòm St Paul's |
| H2-06b Monument đang xây | 2 | TRƯỢT | l1: lớp mốc — cột trơn, không rãnh; l2 (ảnh đầu): biển tên phố |
| H2-09x nền nhà thờ mới 1675 | 2 | TRƯỢT | lớp mốc 2 lượt: cột Monument 1675 (từ 3D) đọc thành "tháp đồng hồ/cupola" |
| H2-10b đỉnh đèn lồng 1708 | 2 | TRƯỢT | l1: cầu thứ hai + tàu lớn; l2 (ảnh đầu): tàu lớn |
| **H5-04c** cụm toà cao từ Leadenhall St | 1 | **CHỌN** | — |
| **H5-05d** mái vòm từ sông | 2 | **CHỌN** l2 | l1: người đi bộ méo |
| H5-05b Fleet St → mái vòm | 1 (502, $0, không tính) + 2 | TRƯỢT | biển số xe (chữ); người méo; tự soi: toà cao ngay sau mái vòm (trái lời) |
| H5-02b Barbican đang xây · H5-02s London Wall 1976 | 0 | không sinh | nền 3D sai niên đại (không có tháp Barbican 1973; toà kính 2018 trong cảnh 1976) — 3 lần đặt máy |
Ba máy ảnh đầu đầu tiên rơi vào trong nhà/sai phố (H1-15x, H5-05d, H5-05b) → đặt lại theo trục phố OSM, dựng lại (không tốn API).

**Số Omni:** 360p 13 lệnh = **78,2 s sinh, $2,708 → $0,0346/s**; chọn **4 clip = 24,1 s → $0,112/s dùng được (31 % số giây)**; Flash 43 lệnh $0,190. **720p đo thật** (lệnh đã đạt H1-06x): **$0,614 / 6,02 s = $0,102/s** (×2,94 so 360p); clip 720p là lần sinh mới → Flash lại ĐẠT-T1 (`clip/H1-06x-l1-720p.mp4`). H1-06b giữ ngoại lệ animatic (D5), kiểm lại ở B.
**Phần hiện đại A = 12 s** (H5-04c 6 + H5-05d 6) — **dưới mục tiêu 30–40 s**; không thêm clip để bù (luật cứng). Đề xuất Q-A5 (sửa niên đại 3D rồi thử lại H5-02b/s) trong phiếu.

## 5. Việc 5 — Ảnh thật hiện đại (B) + C2
- **Commons:** API 429 từ 23:37 tới 01:19 UTC; mở 01:19–01:45 (tra cứu + trang mô tả); **máy chủ ảnh `upload.wikimedia.org` 429 suốt phiên** (Retry-After 600 s; ≤ 1 yêu cầu/5 s; `scripts/k2ldn/bc/commons_bc.py`, `commons_cho.sh`). Lệnh tải nền đầu tiên bị harness dừng ở 30 phút; chạy lại dạng tiến trình độc lập — vẫn xếp hàng lúc viết báo cáo.
- **Lấy được (bản gốc Flickr cỡ k, cùng tệp Commons):** (1) "City of London" — It's No Game, 2019-11-09, **CC BY 2.0** (FlickreviewR passed + trang Flickr `licenses/by/2.0/`), 2047×1282, SHA `478e3c08…` — cụm 22 Bishopsgate/Leadenhall/Scalpel/Lloyd's; (2) "Barbican Estate, City of London" — Mikey, 2013-04-03, **CC BY 2.0**, 2048×1536, SHA `2e129325…` — tháp Barbican từ London Eye. Bằng chứng `channel-k2/k2c-t4-02/ban-cuoi/that/licenses/*.json` + ảnh **vào git trước khi lên bảng** (`git cat-file -e` OK 4/4). Chú thích ≤ 6 từ, đúng năm: "22 Bishopsgate and Leadenhall, 2019", "Barbican towers, 2013". Không AI chạm.
- **Không tìm được bản CC BY/PD:** St Paul's thập niên 1950 ("St Paul's Cathedral 1951.jpg" = CC BY-SA 4.0 → loại), Barbican/London Wall đang xây 1960s–70s (geograph = CC BY-SA → loại). Ứng viên CC BY 4.0 Tower Block UK l9 (Barbican 1985/1988, Miles Glendinning) đang xếp hàng tải. Europeana/LoC: không có (LoC "rights not evaluated").
- **Mới 2 ảnh / lệnh ≥ 3** — thiếu 1, nêu rõ.
- **IWM D 6418 gốc:** chưa tải được (429); giữ bản 500×667 → **chủ dự án tải tay**. Footage đêm: BỎ (C2).

## 6. Việc 6 — BẢNG SHOT v4
`channel-k2/k2c-t4-02/ban-cuoi/BANG-SHOT-v4.{md,json}` sinh từ đặc tả v4 `ban-cuoi/dac-ta-v4/` (`scripts/k2ldn/bc/dac_ta_v4.py` chép khai animatic v3 rồi áp đổi; `bang_shot_v4.py`). Lời v3 khoá, không đổi, không thu thêm; mỗi chèn M-d/THAT là tách shot 3D trong cùng nhóm lời (tổng nhóm giữ nguyên). Danh sách đổi: `dac-ta-v4/doi-v3-v4.json` (23 mục):
- **M00** mở lạnh: điểm P1b Bankside đông 125 m, VONG — thấy toàn vòng lửa + cầu London có nhà, khác M03 (hết lặp 0:40–0:50; khung thử `m00/M00-moi-a.jpg`). MÓC đủ 4 loại cú máy.
- **M04** +0,5 EV (C9b) · **H1-15b** 7,5 → 4,625 s (khung 0–110) · thẻ Pepys/James chỉ chữ (giữ) · **Hollar** "Hollar: London before the Fire (pub. 1666)" → **"Hollar, pre-Fire view, published 1666"** (5 từ; không gán 1647); "Hollar: Old St Paul's from the east" → **"Old St Paul's, by Hollar"**.
- M-d mới: H1-06x (sau H1-06 13,5 s), H1-15x (H1-15h 3,2 s → clip → H1-15h2 5,3 s; trúng câu "In the last days…"), H5-04c, H5-05d. THAT mới: H5-02t, H5-06t. H5-05a = **E**.
- Khai K1178 §4: `vung` mọi shot (33 vùng; nửa sau 20), `log_chu` khoảng (27 lớp; cửa sổ cách ranh M-d ≥ 1 s — dời 6 cửa sổ), `tu_lieu_lan` cho TL/KHAC/THE/MAP/MAP3D trong shot 3D, `type` minh_hoa/tu_lieu, tấm E (`n2p_toan_khung_hien_dai`, `nam_min`, `toa_co_ten`, `mat_na_ct`, `dem`), M-d mới `muc_kiem/kiem_t1/kiem/kiem_moc/chan_dung_tham_chieu{tep, sha256}`, THAT `that.giay_phep{tep, sha256}`. **Beats:** chỉ từ mốc có neo (ranh shot + `lop_chong`) — beats tự khai bị luật từ chối (KN-2).
- **Tự kiểm (bảng v4):** thời lượng **770,874 s** ≤ 780 · 103 shot · góc cao ước 64,3 % (≥ 50; k2check theo khai: 68,0 %), mỗi chương 58–100 % (≥ 40), mở/kết chương góc cao ĐẠT, P1 tái xuất mọi hồi ĐẠT · **Omni 181 s = 23,98 %** (31 clip; v3 20,74 %) · tư liệu + thật **13,47 %** (≤ 20) · M-d dài nhất 8,0 s (≤ 8) · ≤ 2 shot thấp/M-d/THAT liền: 2 · AI (M-d + E) 24,8 % (≤ 70).

## 7. Việc 7 — Kiểm
- **Tấm E / B:** §1, §3 (k2check 1.17.8 từng tấm, G2).
- **Đặc tả v4 — đính chính 26/10 (lệnh bổ sung #1):** bản trước của `dac-ta-v4/episode.yaml` khai `log_shot: ../../animatic2/log-shot.json` (log **v3**). Đây là lỗi khai của phiên. Hệ quả: lượt k2check đặc tả v4 đầu tiên đọc log v3 cho mọi hàng dựa trên log shot. Đã sửa thành `log_shot: log-shot.json` và chạy lại (máy, chặn mạng, 0 lệnh API). Bảng hiện hành: `dac-ta-v4/k2check-1.17.8-dac-ta-v4.md`, rc 1.
  - **TRƯỢT (không đổi):** Q37 / NHIP-K2 / Q37 (1.13) (TB 5,75 s > 3,5; dài nhất 20,17 s ở H2-03b — KN-2) · K-LAI-2 (chưa khai `phat_hanh.mo_ta`) · **K-LAI-3: 30/31 ĐẠT, 0 thiếu tệp**, chỉ còn H1-06b (mức nen, Flash LOẠI, chờ D5) · XEM-CAM.
  - **Cảnh báo ở animatic, Chặn ở G2 — việc phiên B:**
    - NHAN-VAT-TEN:
      - (a) H1-15b 0,162 khung đo trên **cả clip** — k2check không đọc `cat_clip` [0, 110]; bản dựng cắt khung 0–110 (KN-4).
      - (k) H3-05b → KN-7.
      - (u) H1-05a, H1-15b chưa khai duyệt A1; (u) H1-06x, H1-15x chờ PHIẾU-A.
      - H3-05b: (u) và (m) đã hết, mặt 0,070.
    - KIEM-2-MUC (d): 4 clip mới H1-06x, H1-15x, H5-04c, H5-05d khai `kiem` = tệp o2-v2 (`-kiem.json`). Lớp mốc đã chạy (`kiem_moc` 3 tệp/clip), nhưng chưa có tệp gộp `-kiem-moc.json` → phiên B gộp (không gọi mô hình).
    - MAY-19 (a): H2-10 THAP ngửa 4,35…7,34° và H5-05b THAP ngửa 3,95…6,94° (ngoài 5–15°) → sửa máy trước khi dựng.
    - GOC-CAO (a): HỒI 1 mở bằng H1-01h, chưa nhận là góc cao. Tổng 62,6 % (log khung 63 shot).
  - **ĐẠT:** Q34, SACH-1, TU-LIEU-10 13,19 %, TU-LIEU-THAT, N2P-E, N2P-6 (tổng AI 24,3 %).
  - **TU-LIEU-OMNI:** 6 cảnh báo thật (H2-02 ↔ H2-01b ghép liền). **KN-3 rút lại** vì cùng gốc lỗi `log_shot`.
  - Các số "K-LAI-3 thiếu 27 tệp" và "TU-LIEU-OMNI 11" ở bản báo cáo trước là sai cùng gốc lỗi trên.
- **Tự soi bằng mắt** mọi tấm/clip trước khi đẩy: tờ so E, tờ P1, 6 mẫu, B, tờ khung Omni `omni/to-khung-omni.jpg` (9 clip × 3 khung), M00. Điều phối soi độc lập.

## 8. Việc 8 — Ước phiên B
| Hạng mục | Ước | Căn cứ |
|---|---|---|
| Dựng 1080p (D + E lớp 3D) | **≈ 31 h máy** (P = 2) → B1/B2/B3 (§3) | 13 061 khung × 8,58 s |
| Tấm E thật (H5-05a) + B (nếu duyệt) | ≈ 0,5 h + $0,3 | đã có quy trình + lệnh |
| Omni 720p | 31 clip ≈ 181–186 s × $0,102 = **$18,5–19,0**; + ≤ 30 % làm lại → **≤ $24,7** | đo §4 |
| Gemini T4 tổng | đã tiêu **$18,58** → dự kiến **$37,1–43,3** / mốc $50 / chặn $55 | `do/chi-phi.json` |
| Âm | SFX/nhạc CC0/PD theo cung bậc (thêm: mái chèo/sóng sà lan, dây xô nước, phố 2026); nhạc giữ Scott Buckley CC BY 4.0 (đã RIGHTS); mix −14 LUFS, ≤ −1 dBTP; ElevenLabs 0 (lời khoá) | luật §16 |
| Bản xem | **6 phần ≤ 5 MB** (≈ 128 s/phần; âm AAC 128 k → hình ≈ 180 kb/s, gấp ≈ 2,3 lần v2) | C5 (b) |
| OpenAI / Claude | ≈ $1,5 / ≈ $2 (kiểm tầng 2 + q_thoi_dai 720p) | |

## 9. Việc 9 — Phiếu
`reports/ban-cuoi-t4-a/PHIEU-A.md`: E1 (2 mặt nạ, ngoại lệ "bờ"), E2, P1, D/B mẫu, **A1 duyệt từng clip H1-06x, H1-15x**, clip hiện đại A, ảnh thật, ngân sách/giờ B, Q-A1…Q-A6. Không tự chấm thay chủ dự án.

## 10. Chi phí thật (từ sổ — `reports/ban-cuoi-t4-a/do/chi-phi.json`)
| Nhà | Phiên này | Mốc / chặn | Chi tiết |
|---|---|---|---|
| **Gemini** | **$3,512** | T4 TỔNG **$18,58** / mốc $50 / chặn $55 (phiên dự kiến ≤ $8) | Omni 14 lệnh $3,322 (360p 13 = $2,708; 720p 1 = $0,614) + Flash 43 lệnh $0,190; 0 lỗi 402 |
| **OpenAI** | **$3,345** | mốc $5 / chặn $10 | ảnh gpt-image-2.5 23 lệnh (22 thành công + 1 lỗi 502 $0) $1,706 + gpt-6.1-sol tầng 2 $0,592 + mô hình nhìn k2check $1,047 |
| **Claude API** | **$2,642** | mốc $4 / chặn $10 | q_thoi_dai (claude -p) $1,610 + mô hình nhìn k2check $1,032 — 64 dòng sổ có `usd` |
| ElevenLabs · RunPod | 0 · 0 | 0 | |
| Giờ máy | ≈ 3 h đồng hồ container (23:30 → ≈ 02:30 UTC) | 12 h | dựng ≈ 2 h (P = 2) |

## 11. Sự cố
1. `setsid … & echo $! > tệp` chạy trước `mkdir` (chuỗi `a && b & c`) → ghi PGID hỏng; đọc lại PGID từ `ps` (lặp K1178 sự cố 4).
2. Commons 429 kéo dài (§5); lệnh tải nền bị harness dừng ở 30 phút → tiến trình độc lập.
3. Đặt máy ảnh đầu Omni: 5 máy rơi vào trong nhà/sai trục phố (toạ độ ước bằng tay) → tra trục phố OSM, dựng lại; H5-02b/H5-02s bỏ vì niên đại 3D.
4. **Lỗi lệnh của phiên:** B-H2-12b lượt 1 gán "nhà gạch mới" cho Southwark → TRƯỢT lỗi thời đại 1720; sửa ở lượt 2.
5. OpenAI 502 (H5-05b-a1, $0) — không tính lượt (tiền lệ $0 của ANIMATIC-T4-V2), chạy thêm lượt thật thứ 2 (l3) — nêu để chủ dự án biết.
6. Mặt nạ "mọi toà OSM có tên" làm lớp (a)-E phình (KN-5).
7. Beats tự khai lượt đầu bị Q37 (a) từ chối → bỏ, chỉ giữ mốc có neo (KN-2).
8. Timeline đặc tả v4 bản đầu làm rơi `p.lop_chong` → mốc không neo; sửa.
9. Preflight CHẶN video kiểm 5,4 MB → bỏ khỏi git, giữ SHA + lệnh tái tạo.
10. Mô hình Claude (k2check B-H5-06) không đọc đủ 8 ảnh (kiểu KN-3 THU-B) → chạy lại đủ.
11. Render H5-02b/H5-02s (máy cũ) trong chuỗi 2 và chuỗi 3 bị bỏ (dừng chuỗi 3 theo PGID) — ≈ 6 phút máy phí.
12. Một lần `pgrep -f` để in kiểm (§0).
13. ~~27 tệp kiểm JSON của animatic v3 không có trong git → K-LAI-3 THIẾU~~ — **chẩn đoán sai, đính chính 26/10.** Gốc thật: đặc tả v4 trỏ `log_shot` về log v3 (sự cố 14).
14. **Lỗi khai của phiên** (phát hiện khi làm lệnh bổ sung #1): `dac-ta-v4/episode.yaml` → `log_shot` v3. Lượt k2check đặc tả v4 đầu đọc log v3 → KN-3 và chẩn đoán K-LAI-3 sai. Đã sửa ở `dac_ta_v4.py` và chạy lại (§7).
15. Một lần gọi `checks/ll/k2check.py --help` để xem tham số. Lệnh lỗi và in traceback 5 dòng mã `checks/` ra màn hình. Không mở tệp mã; nêu theo luật "không đọc mã checks/".
Không lỗi nào lặp ≥ 3 lần cùng cách.

## 12. Chỉ số trong ±5 % quanh ngưỡng (luật cứng — nêu tên)
| Chỉ số | Giá trị | Ngưỡng | Lệch |
|---|---|---|---|
| M-d dài nhất (H4-03, v1) | 8,0 s | ≤ 8 s | 0 % |
| Chốt 3: shot thấp/M-d/THAT liền | 2 | ≤ 2 | 0 % |
| MÓC: số loại cú máy | 4 | ≥ 4 | 0 % |
| Thời lượng | 770,874 s | ≤ 780 s | −1,2 % |
| N2P-5, BE-MAT-NHA (d)(e), YuNet, tư liệu, góc cao | — | — | ngoài ±5 % (xa ngưỡng) |
Ngoài ±5 % nhưng đáng nêu: OpenAI $3,345 so mốc $5 (−33 %); Claude $2,642 so mốc $4 (−34 %); P1 dời 80 m mái vòm 26,2 % so đích 30 % (−12,7 %).

## 13. Dòng sổ đề xuất (P ghi — phiên này không sửa sổ)
- **COST-LEDGER:** `2026-10-26 · BAN-CUOI-T4-A · Gemini $3,512 (Omni $3,322 = 360p 13 lệnh $2,708 + 720p 1 lệnh $0,614; Flash $0,190) → T4 tổng $18,58 · OpenAI $3,345 · Claude API $2,642 · ElevenLabs 0 · RunPod 0 · ≈ 3 h máy`.
- **RIGHTS:** (1) `ban-cuoi/that/anh/flickr-49102341647-k.jpg` — It's No Game, CC BY 2.0, Flickr/Commons, ghi công "Photo: It's No Game, CC BY 2.0"; (2) `flickr-8649139240-k.jpg` — Mikey, CC BY 2.0; (3) ảnh AI OpenAI (E: 4; B: 3; ảnh đầu M-d: 15) và clip Omni (4 chọn + 1 720p đo giá) — đầu vào là render của dự án / chân dung PD đã có trong RIGHTS (met-435943, rijks-200221267); SynthID/C2PA có trong sổ.
- **AUTHORSHIP:** khi chủ dự án trả lời PHIẾU-A — A1 H1-06x, H1-15x (nguyên văn + giờ); E1; P1; Q-A1…Q-A6.
- **BAI-HOC-K2 (đề xuất):** (1) ảnh đầu M-d dựng từ render 3D cùng năm giảm lỗi mái vòm sai năm nhưng **kế thừa lỗi niên đại của 3D** (Monument 1675 trơn, toà 2018 trong 1976) — kiểm niên đại 3D trước khi dùng làm ảnh đầu; (2) đặt máy tầm phố phải tra trục phố OSM, không ước tay; (3) "toà có tên OSM" ≠ "toà tháp có tên" (tên cửa hàng); (4) lệnh AI phủ bề mặt phải nói rõ khu không cháy (Southwark 1666) giữ vật liệu cũ; (5) Commons: API và máy chủ ảnh giới hạn riêng — xếp tra cứu trước, tải ảnh sau; Flickr gốc là đường thay hợp lệ khi FlickreviewR đã xác nhận giấy phép.

## 14. Việc chờ chủ dự án
1. Trả lời **PHIẾU-A**: E1 (mặt nạ "đủ"/"tháp" + ngoại lệ "bờ"), E2, P1 (khuyến nghị giữ), mẫu D/B, **A1 từng clip H1-06x, H1-15x**, H5-04c, H5-05d, 2 ảnh thật, Q-A1…Q-A6, chia phiên B (B1/B2/B3 hoặc P = 3).
2. **Tải tay IWM D 6418 bản gốc** (Commons ảnh 429 cả phiên).
3. Phiên P: merge nhánh khi duyệt; ghi sổ §13; chuyển `khieu-nai-K.md` (KN-1, KN-2, KN-4…KN-7; KN-3 rút) vào `checks-appeal.md`.
4. Phiên K (nếu chủ dự án đồng ý): KN-1 (D2 = B), KN-2 (Q37/BIEN-CO-V T4), KN-4, KN-5 (định nghĩa toà có tên cho LUẬT E), **KN-7 (NHAN-VAT-TEN (k) — nhân vật không có chân dung, H3-05b)**. KN-3 đã rút.
5. **H3-05b:** giữ (a) chờ K hay dùng dự phòng (c) H3-05c 3D 6,0 s (PHIẾU-A mục A1-H3-05b).

## 15. Lệnh bổ sung #1 (chủ dự án 26/10/2026 07:39 — H3-05b, hướng (a))
- **(1) Khiếu nại:** `khieu-nai-K.md` **KN-7** — đề xuất luật nguyên văn; số đo YuNet thật; danh sách nơi đã tra chân dung.
  - YuNet chạy 1 lần trên máy, chỉ dùng tệp mô hình. Script `scripts/k2ldn/bc/do_mat_yunet.py`; kết quả `ban-cuoi/omni/kiem/H3-05b-l1-360p-yunet.json`; tờ soi `omni/soi-H3-05b-yunet.jpg`.
  - Số đo: mặt lớn nhất 0,1025 (khung 137, điểm 0,569). Hộp điểm ≥ 0,75: 0,072. k2check: 0,070. Trần 0,125.
  - Đã tra: LoC, Wellcome, Rijksmuseum, The Met. Chưa tra: NPG, St Paul's, Commons, Historic England.
- **(2) BẢNG SHOT v4:** giữ H3-05b. Khai `nhan_vat_ten: Godfrey Allen`, `chan_dung: khong_co`, `chan_dung_nguon_da_tra`, `mat_yunet`, `duyet_chu_du_an` = A1 phiếu xem v2 (AUTHORSHIP 26/10 00:12). Bảng có thêm mục "Nhân vật có tên trong M-d". Các shot khác không đổi; tổng vẫn 770,874 s, 103 shot.
- **(3) PHIẾU-A:** mục A1-H3-05b, dự phòng (c) = H3-05c 3D 6,0 s ở 531,333–537,333 s. Có tệp máy và khung thử 1080p.
- **Phát sinh (nêu thật):** sửa lỗi khai `log_shot` v3 của đặc tả v4 (§7, §11 sự cố 14). Lỗi này làm k2check không thấy khai mới của H3-05b; sửa là cần cho việc (2). Kết quả kiểm đặc tả v4 cập nhật, KN-3 rút. Những việc mới lộ ra (KIEM-2-MUC (d), MAY-19 (a), GOC-CAO (a), (u) H1-05a/H1-15b) **chỉ ghi lại cho phiên B, không sửa** — theo lệnh "không đổi việc khác".
- **Chi phí lệnh bổ sung:** 0 USD API (YuNet + k2check chạy trên máy, chặn mạng). Máy: 1 khung 3D thử (H3-05c) + 2 lượt k2check ≈ 25 phút.
- main đã tiến lên `41de7ce3` (P-2610b) sau khi phiên mở nhánh. Phiên **không** merge main (ngoài phạm vi).

**DỪNG chờ chủ dự án.**
