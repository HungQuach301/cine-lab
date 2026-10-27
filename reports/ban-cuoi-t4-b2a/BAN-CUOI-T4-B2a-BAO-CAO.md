**Nhánh thật: `claude/adoring-wright-i76iay`** (harness buộc; lệnh ghi `k2c-t4-02-final-b2a`). Gốc origin/claude/k2c-t4-02-final-b1-t9ekhx @6f6c2636 (khớp lệnh) + merge origin/main @75e94b98 (commit 64a304ee). Đẩy nhánh, KHÔNG merge, KHÔNG tạo PR.

# BAN-CUOI-T4-B2a — bản cuối T4 London (K2C-T4-02), phần B2a: dựng 1080p MÓC + HỒI 2 đầu + dựng lại H1-01h; thử M01 tấm E — BÁO CÁO

> Phiên 27/10/2026 01:19 → ≈ 08:35 UTC (08:19 → ≈ 15:35 Asia/Saigon). Mọi số là số đo thật trong phiên.
> **Căn cứ:** chủ dự án 27/10/2026 "Duyệt B1-Q1…Q5 theo khuyến nghị điều phối" (B1-Q1 nâng máy ≈ 160 m; B1-Q2 chia B2a/B2b/B3; Kinh thánh 22c6889d LOOK-T4 cập nhật 07:24); K1179-D5 (đẩy 2D ≤ 1,5 %/s), K1179-D6 (nước AI, duyệt từng tấm) — 26/10 13:02; D-B1 — 26/10 10:42. **Giờ dán lệnh phiên này: 27/10/2026 00:24:21Z = 07:24:21 Asia/Saigon** (giờ tạo phiên, `get_session`).
> Email chủ dự án không có trong tệp/commit/header/URL/payload/User-Agent (UA `CineLab-research (+https://github.com/HungQuach301/cine-lab)`). Khoá API do proxy gắn, không in/ghi. Không đọc mã `checks/` (chỉ chạy `k2check.py`, `q_thoi_dai.py`, `lock.py --verify`; `ghep_kn8.py` của K1179 nạp các hàm ghép theo K1179 §4).

## §0 Nhánh, SHA, khối vận hành

| Mục | Lệnh | Thực tế |
|---|---|---|
| Gốc B1 | @6f6c2636 (khác → DỪNG) | **6f6c2636** khớp (fetch 01:20 UTC) |
| Merge main | origin/main @75e94b98, không squash, `--no-commit` + preflight | `git merge --no-ff --no-commit 75e94b98` → 0 xung đột, 146 tệp → commit **64a304ee** (preflight "— ĐẠT"). Ghi: origin/main lúc fetch đã tiến tới ed3b79c9 (P-2710) — theo lệnh vẫn merge đúng 75e94b98 |
| LOCK | `lock.py --verify` 1.17.9 `9eddaf24…` | **KHỚP** sau merge và ở mọi commit (hook preflight) |
| Vùng sửa | `ban-cuoi/**` (trừ v4/dac-ta-v4/dung B1), `design/k2v/ldn/**`, `scripts/k2ldn/**`, `reports/ban-cuoi-t4-b2a/**` | đúng: `ban-cuoi/{may/b2a, dac-ta-v5b, e/tam/E-M01, e/kiem/E-M01-*}`, `ban-cuoi/dung/` (thêm 11 shot B2a + `M01-E-1080p.mp4`, **ghi đè H1-01h** + SHA256SUMS), `design/k2v/ldn/bc/look3-b1.js` (sinh lại bằng `tao_look3_b1.py`, xem §1b), `bc/look3-b1d.js` (mới), `scripts/k2ldn/bc/*_b2a*`, `reports/ban-cuoi-t4-b2a/**`. KHÔNG sửa `checks/`, `checks-appeal.md`, `docs/`, sổ, `tools/`, `.gitattributes`, `BANG-SHOT-v4.*`, `dac-ta-v4/**`, `channel-k2/k2c-t3-01/**`, main |
| Preflight / hook | pipefail, chỉ commit khi "— ĐẠT"; hook trước lần đẩy đầu | `reports/ban-cuoi-t4-b2a/cam_commit.sh`; hook pre-commit + pre-push → `tools/preflight.sh` cài 01:21, lần đẩy đầu 01:42 |
| LFS (D-B1) | `git lfs push` trước `git push` sau MỖI shot; `git lfs ls-files` | `scripts/k2ldn/bc/xong_b2a.sh` sau mỗi shot; **13/13 tệp B2a trong `git lfs ls-files`** (11 shot + H1-01h + M01-E); tải công khai media.githubusercontent.com H2-04h: SHA khớp `aeed4a49…` |
| Đẩy ≤ 30 phút + CHECKPOINT | | mỗi shot 1 commit + nhịp 25 phút (`nhip_b2a.sh`); `reports/ban-cuoi-t4-b2a/CHECKPOINT.md` (mục "Trạng thái", "Lệnh bổ sung đã áp": không có) |
| Tiến trình nền | PGID, một vòng nặng, P ≤ 2, RAM ≥ 5 GB | hàng `dung_b2a.py` theo PGID; **lệch nêu rõ:** 02:17–02:34 chạy 4 lượt thử ngắn (khung phế tích, gỡ lỗi, soi lượt 2) làm tiến trình thứ 3 → **OOM giết M00 lần 1** (§6 sự cố 1); sau đó không chạy tiến trình dựng thứ 3 nữa. Không dùng `pgrep -f`/`pkill -f` |
| Force / amend / dừng hỏi | không | không |
| Đầu vào /var/tmp | git hoặc SHA + cách tái tạo | `reports/ban-cuoi-t4-b2a/SHA-du-lieu-ngoai-git.txt` (hình học, 13 lightmap, dan.json, ô OSM, tấm E 2304×1296); **ghim vào git**: `ban-cuoi/may/b2a/osm2026-b2a.json.gz` (2,7 MB) + `thuyen-b2a.json` (§6 sự cố 2) |

Môi trường: container mới, `setup.sh` chạy lại (≈ 4 phút); thêm `pyproj`, `pyyaml`, `OpenEXR` vào /opt/cine (thiếu so với setup). Dữ liệu nền tái tạo bằng `scripts/k2ldn/bc/du_lieu_b2a.sh` 01:25 → 01:43 (18 phút).

## §1 Việc 1 — Máy B1-Q1 (M00, H1-01h ≈ 160 m)

- Tệp máy: `scripts/k2ldn/bc/may_b2a.py` → `ban-cuoi/may/b2a/{M00,H1-01h}.json`; log máy tính `…/b2a/{M00,H1-01h}-log-may.json.gz`; log dựng thật `ban-cuoi/dung/log-may/{M00,H1-01h}.json.gz`. Giữ phương vị, tâm nhìn, cung VONG (M00 ±12,5°, 17 s) và giờ (M00 19,6 → 20,6; H1-01h 0,9 → 1,05).
- Thử 3 cách chỉnh góc cúi (kp = phần nâng điểm nhìn theo máy; 960×540, khung đầu/giữa/cuối; đo bố cục `reports/ban-cuoi-t4-b2a/thu-may-do.json`):

| Máy | Phương án | Cúi (đầu/giữa/cuối) | Chân trời (y/H) | Vòng lửa: trọng tâm y · biên y | Chọn |
|---|---|---|---|---|---|
| M00 cũ (B1) | 125 → 112 m | 11,6 / 11,3 / 10,9° | 0,24 | 0,576 · 0,40–0,80 | — |
| M00 kp 0 | **165 → 155 m** | 15,6 / 15,6 / 15,5° | 0,15 | **0,605 · 0,385–0,874** | **✔** (vòng lửa giữ vị trí; dải trời 24 → 15 %, trong 8–20 % LOOK-2) |
| M00 kp 0,5 | | 13,6 / 13,4 / 13,2° | 0,20 | 0,649 · 0,43–0,92 | |
| M00 kp 1 | | 11,6 / 11,3 / 10,9° | 0,24 | 0,692 · 0,48–**0,95** (sát mép dưới) | |
| H1-01h cũ (B1) | 120 → 118 m | 6,8° | 0,372 | — | — |
| H1-01h kp 1 | **160 m** | 6,8° | **0,376** | khung City/sông như cũ | **✔** |

- **k2check 1.17.9 trên đặc tả `ban-cuoi/dac-ta-v5b/`** (sinh bằng `scripts/k2ldn/bc/dac_ta_v5b.py`: v4 + log dựng thật 36 shot B1/B2a; H2-10/H5-05b log tính; còn lại log animatic): `dac-ta-v5b/k2check-1.17.9-dac-ta-v5b.md` — **GOC-CAO ĐẠT, lỗi Chặn 0, Cảnh báo 0 (hết (a) M00/H1-01h)**: 474,4 / 754,9 s = **62,8 %**; chương MÓC 96, HỒI 1 **51** (B1: 49), HỒI 2 62, HỒI 3 65, HỒI 4 64, HỒI 5 68. Lượt trước dựng (log tính) cùng kết quả: `k2check-1.17.9-dac-ta-v5b-tinh.md`.
- Tờ so trước | sau đầu/giữa/cuối: **`reports/ban-cuoi-t4-b2a/may-B1-Q1-truoc-sau.jpg`** (0,62 MB; H1-01h thêm hàng gamma 2,2 chỉ để soi vì khung rất tối).
- Liền mạch với B1 (hình học tái tạo khác SHA, §6 sự cố 2): H1-01h dựng lại máy cũ bằng dữ liệu B2a so khung B1 (LFS): lệch TB **2,6/255**, p99 11/255, độ sáng 15,8 → 16,5.
- **H1-01h ghi đè**: SHA cũ `d19fbc571d647c68add24ebee7658aea241e59ece5f39e3133f59ff943e21f6b` (B1, 29,61 s/khung) → mới `1565579256b56989…` (ghi trong `reports/ban-cuoi-t4-b2a/SHA-cu-ghi-de.txt`; SHA256SUMS cập nhật).

### §1b Phát sinh: phế tích sau đám cháy (soi năm biên lượt 1 bắt — §4)
- **Nguyên nhân (đo, trang gỡ lỗi tô màu theo lớp):** mọi bề mặt lớp 2 (phế tích) bị nhân 0,38 → vỏ **Old St Paul's** (lớp 5, vật liệu 10, `tl.x` = năm cháy: tường 18–19 m + tháp cụt 20 × 20 × 44 m) và tháp/thân **nhà thờ giáo xứ cháy** (lớp 2, vật liệu 10) thành **khối đen trơn không cửa** — q_thoi_dai đọc H2-04a 1667,9/1668,4 là "toà hiện đại"; B1 đã ghi cùng lỗi ở H2-05s 1670. Lý do khối đen cả trong ảnh: mặt tường hướng máy nằm trong bóng, không có chi tiết nào.
- **Sửa** (một chỗ thay mới trong `scripts/k2ldn/bc/tao_look3_b1.py`, sinh lại `bc/look3-b1.js` + `bc/look3-b1d.js`; **chỉ khi năm 1666,69–1700**): đá giữ màu (vỏ Old St Paul's sáng × 1,55), ám khói dày dần theo độ cao + vệt cháy loang; **ô cửa vòm nhọn theo tầng** (Old St Paul's nhịp 6 m, rộng 2,2 m, cao 8 m, mỗi 12 m; lớp 2 nhịp 4,5 m, rộng 1,6 m, cao 3,4 m, mỗi 7 m); qua ô cửa thấy **lòng phế tích không mái được nắng** (phát sáng cộng `emis`, chỉ ban ngày; 88 % ô sáng); ống khói, tro, đầu tường giữ như cũ.
- **Không đổi khung cũ:** H1-01h khung 0 (1666,67) dựng bằng trang mới so bản sản xuất: **lệch 0/255** (trùng tuyệt đối) → mọi khung HỒI 1 B1, M00, M03, M04, H1-01h không bị ảnh hưởng. Bộ sinh tái tạo đúng từng byte trang B1 trước khi thêm (b7248833…).
- Ghi: phế tích ở các shot B1 trong lúc cháy (≤ 1666,68) vẫn kiểu cũ (tối, đêm/lửa) — chuyển sang kiểu mới từ H2-00 (16/9/1666). Ghi cho chủ dự án soi liền mạch H1-18 → H2-00.

## §2 Việc 2 — Thử M01 bằng tấm E-P1 (K1179-D5, D6)

**(a) Tấm** (0 API sinh ảnh; ảnh AI `ban-cuoi/e/ai/E-P1-ngay-l2.jpg` của phiên A, SHA `ecca9532…`): `scripts/k2ldn/bc/e_m01_b2a.py`.
- Render + mặt nạ 1/2/3e **dựng lại bằng look3-b1** (khoá 0 của M01 ≡ E-P1-ngay.json), **2304 × 1296** (để đẩy 2D tới × 1,179 vẫn cắt từ ≥ 1 954 px, không phóng to), spp 24, LUT kênh (như phiên A). **Thuyền:** hết elip đen (sà lan B1 có boong); thuyen.json tái tạo chỉ còn 1 sà lan trong khung (sự cố 2).
- Mặt nạ "tháp" theo K1179 KN-5: 16 toà có tên khai `loai` — `mai_vom` St Paul's; `lich_su` + `nguon_lich_su` (Historic England NHLE) Mansion House, Royal Exchange, Guildhall, Tower of St Mary Somerset, Bank of England; `thap` + `dinh_odn_m` 10 toà (≥ 75 m). **"Guildhall Art Gallery" hạ về nhà thường** (toà mới).
- **Bóng cầu AI lệch:** mặt nạ vệt = điểm nước AI trong dải 28 px quanh cầu lệch trung vị nước vòng ngoài > 14/255 (tối = bóng lệch; sáng = mặt cầu AI lệch ra ngoài cầu render) → inpaint từ chính nước AI: **17 659 px** (`e/tam/E-M01/l2-thap-bo_dat/vet-bong-cau.png`).
- Ghép = `ghep_kn8.py … thap bo_dat` (hàm nạp nguyên từ `reports/k1179/do/ghep_kn8.py`): **(a)-E 6,52 %** (K1179 ước 6,38 % trên tấm cũ), vùng bảo vệ 7,27 %, nước 22,39 %, lệch (a)-E **0/255**.

**(b) Video E** 17,875 s = tấm + (a)-E 3D CODINH từng khung (`E-M01-tl`, 429 khung 2304 × 1296, 11,82 s/khung; giờ 14,00 → 14,30 vì tấm AI tĩnh) → **đẩy 2D 1,0 %/s một phép cho cả khung** (warp bicubic lên 2× rồi thu INTER_AREA). Tệp: **`ban-cuoi/dung/M01-E-1080p.mp4`** (LFS, `b9c67b09…`, **đã LUT kênh** — B3 không áp LUT lại).

**(c) M01 3D** DAY look3-b1 1080p như bảng: `ban-cuoi/dung/M01-1080p.mp4` (§3).

**k2check 1.17.9** (`ban-cuoi/e/kiem/E-M01-a/`, `E-M01-b/`, mô hình nhìn một lần trên (b)):

| Hàng | (a) tấm, máy | (b) tấm + video, có mô hình nhìn | Ghi |
|---|---|---|---|
| N2P-E | Chặn 1: (u) | **Chặn 1: (u)**; (h) đẩy đo **1,00 %/s**, sai sau bù (a)-E **1,87** / ngoài 5,92 → qua; (w) 9 | (u) = tấm nước AI **chưa có duyệt chủ dự án** (đúng trạng thái; không khai hộ). (w) 8 "toà cao bịa" ở chân trời xa (GPT) + T9c chỉ in — người đọc |
| N2P-1 | (a) 0/255; (c) 25 cụm (người đọc) | **Chặn 2 (b)**: GPT "không kiểm được" Tower of St Mary Somerset (vật nhỏ) | máy đo (a)-E lệch 0/255 — tháp là lớp render nguyên điểm → báo nhầm; cần `ngoai_le` + duyệt chủ dự án (K1179 §4) nếu chọn E |
| N2P-2 / 3 / 4 | chưa soi | **ĐẠT / ĐẠT / ĐẠT** | T9c 10 đoạn bờ lấn ≤ 45 px chỉ in (KN-8) |
| N2P-5 | chưa đo | **ĐẠT**: bước 0,744 ΔE/khung; nhấp nháy 0,894 (đối chứng 1,120, trần 1,680) | |
| N2P-6 | Chặn 2 | Chặn 2 | do tập thử 1 shot (100 % tấm nền) — không phải lỗi tập |

Tờ so: **`reports/ban-cuoi-t4-b2a/M01-E-vs-3D.jpg`** (1,55 MB; E | 3D đầu/giữa/cuối + 3 ô phóng × 2: mái vòm, bờ/cầu, cụm tháp; 3D áp LUT kênh **chỉ trên tờ so** để so ngang). Bản xem 640 × 360: **`M01-E-xem-640.mp4`** (4,47 MB), **`M01-3D-xem-640.mp4`** (2,30 MB, có LUT).

### Phiếu ngắn M01 (E | 3D) cho chủ dự án
| | (b) E: tấm AI + đẩy 2D | (c) 3D DAY |
|---|---|---|
| Nhà thường, mái, cây, nền xa | **ảnh thật** (vật liệu, cây, chiều sâu) | khối 3D sạch, nền xa xám dạng hộp |
| Mặt nước | nước sông AI nâu tự nhiên | xanh 3D, phản chiếu phẳng |
| Mái vòm, toà có tên | **giống hệt 3D** (lớp (a)-E = render, lệch 0/255) | |
| Cầu Millennium, dải kè | render CG phẳng, tối hơn ảnh AI (luật: lõi (a)-E phải = render) — thấy ở ô phóng | đồng nhất với cả khung |
| Thời gian | ánh sáng đứng 14:00 (tấm tĩnh; (a)-E chạy 14:00 → 14:30) | **14:00 → 18:00** (chiều trôi, bóng dài) |
| Nối sang M02 (KEO, khoá 0 = 3D 2026 cùng điểm P1) | **nhảy look** ảnh thật → 3D ở điểm cắt; thêm lệch × 1,18 do đẩy | liền look |
| Kiểm | Chặn (u) chờ duyệt tấm + N2P-1 (b) báo nhầm cần ngoại lệ; (w) 9 người đọc | không có hàng N2+ |

Bảng shot **giữ M01 = 3D** tới khi chủ dự án duyệt (Quyết định B2a-Q1).

## §3 Việc 3 — Dựng 1080p (look3-b1 cờ d, spp 4, 24 fps, P = 2, D-B1)
Số khung/cắt theo bảng v4 như B1 §2 (`dac-ta-v4/log-shot.json` t0/t1 → round(t1·24) − round(t0·24), khung 0… của tệp máy). Danh sách: `ban-cuoi/may/b2a/muc-luc-b2a.json`. Mã hoá D-B1 H.264 High CRF 16 yuv420p, không âm, **chưa LUT, chưa lớp chồng**; SHA + số khung `ban-cuoi/dung/SHA256SUMS`, log máy `ban-cuoi/dung/log-may/`.

| Mã | Tệp LFS (`ban-cuoi/dung/`) | Giây | Khung | s/khung/tiến trình | SHA256 | MB | Ghi |
|---|---|---|---|---|---|---|---|
| M00 | M00-1080p.mp4 | 17.000 | 408 (f 0..407) | 10.92 | `7d4468fbcaaa270d…` | 80.4 | máy mới 165 → 155 m; dựng lại sau OOM |
| H1-01h | H1-01h-1080p.mp4 (ghi đè) | 3.000 | 72 (f 0..71) | 17.87 | `1565579256b56989…` | 11.8 | 160 m; SHA cũ `d19fbc57…` |
| M01 | M01-1080p.mp4 | 17.875 | 429 (f 0..428) | 10.71 | `373f74c283f660fc…` | 133.6 | 3D DAY (bảng) |
| M02 | M02-1080p.mp4 | 10.083 | 242 (f 0..241) | 11.49 | `04d3f672b0c9541e…` | 77.0 | KEO 2026 → 1668 |
| M03 | M03-1080p.mp4 | 11.000 | 264 (f 0..263) | 13.43 | `f6a3a7912a96a104…` | 54.5 | |
| M04 | M04-1080p.mp4 | 12.000 | 288 (f 0..287) | 11.44 | `3e557552f8f7e462…` | 65.2 | **+0,5 EV (C9b)**: exposure 1,3435 → 1,9000 |
| H2-00 | H2-00-1080p.mp4 | 3.000 | 72 (f 0..71) | 10.84 | `c2978e1b9a5d387b…` | 13.0 | |
| H2-02 | H2-02-1080p.mp4 | 14.625 | 351 (f 0..350) | 14.58 | `d3f4480ee6aa1c10…` | 73.7 | lớp TL/MAP3D/THE ghép ở B3 |
| H2-03b | H2-03b-1080p.mp4 | 20.167 | 484 (f 0..483) | 10.56 | `814b4738c325a072…` | 96.9 | |
| H2-04h | H2-04h-1080p.mp4 | 2.500 | 60 (f 0..59) | 13.14 | `aeed4a4926c83406…` | 13.9 | |
| H2-04a | H2-04a-1080p.mp4 | 3.500 | 84 (f 0..83) | 14.64 | `7957075968b6bd7f…` | 16.2 | **trang `bc/look3-b1d`** = look3-b1 + lớp người/xe look2d ("look2d tầm phố" như bảng, giữ mọi sửa D-A4) |
| H2-05 | H2-05-1080p.mp4 | 11.000 | 264 (f 0..263) | 11.48 | `b194073a85186098…` | 45.4 | |
| (thử) M01-E | M01-E-1080p.mp4 | 17.875 | 429 | 11.82 (lớp (a)-E 2304×1296) | `b9c67b0962173f64…` | 20.8 | §2; đã LUT |

- **Tổng 11 shot + H1-01h = 12 tệp, 3 018 khung (≈ 0,68 GB LFS)** + thử E 429 khung lớp (a)-E. Đồng hồ hàng dựng 01:55 → 08:09 UTC: **thông lượng 6,5 s/khung tổng (P = 2)** trên 3 447 khung có ích; mỗi tiến trình 10,6–17,9 s/khung (B1: 15,0–33,1; thông lượng 11,6) — máy phiên này nhanh hơn ≈ 1,8×. Mất 178 khung M00 (OOM, ≈ 31 phút máy).
- Thứ tự thật: M00, H1-01h, M01 trước (H1-01h xong 02:18, M01 03:43, M00 03:54), rồi theo bảng (hai hàng P = 1 sau lần dừng tạm 02:03 — §8).
- **Soi cháy trắng 12 khung đầu** (bài học H1-13a/c; `scripts/k2ldn/bc/to_b2a.py trang`): M00, H1-01h, M03, M04 — **0,000 % điểm ≥ 250** ở mọi khung đo; M04 soi thêm khung 200/240/268 (máy hạ 26 m sát lò bánh): 0 %.

## §4 Việc 4 — Soi năm biên công trình mốc (§19 (d))
Danh sách từ bảng v4: shot B2a có St Paul's (cũ/mới) hoặc Monument trong 1666–1711 = M02 (chạy lùi 2026 → 1668 qua 1711 … 1671) + H2-00, H2-02, H2-03b, H2-04h, H2-04a, H2-05 (1666,72–1670,2: chưa có Monument/St Paul's mới — phải có phế tích Old St Paul's). Khung 1080p năm đầu/cuối + năm mốc 1671 / 1675,5 / 1677 / 1708 / 1709,5 / 1711 trong dải (20 khung), **dựng và soi TRƯỚC khi dựng 1080p shot đó**; q_thoi_dai `--lop-moc` + chuỗi `--moc` theo năm (`scripts/k2ldn/bc/qtd_soi_b2a.py`), ô cắt theo mặt nạ 2 (`reports/ban-cuoi-t4-b2a/soi/soi-crop-b2a*.json`, `qtd-*.json`, log `qtd-luot1.log`, `qtd-luot2.log`; sổ `so-ai-claude.jsonl` có usd mọi dòng).

| Lượt | Kết | Khung lỗi / ghi |
|---|---|---|
| 1 (trang B1) | 16/20 ĐẠT | **H2-04a k0 (1667,9), k83 (1668,4): "khối tối phẳng không cửa như toà hiện đại"** → lỗi phế tích → sửa §1b; M02 k213 (1709,8), k214 (1708,3): "không thấy Monument" (ô cắt chỉ chứa St Paul's) |
| 2 (trang sửa; 16 khung 1666,69–1700 + M02 k213/214 toàn khung) | **17/18 ĐẠT** | H2-04a k0/k83 **ĐẠT**; M02 k213 ĐẠT; **M02 k214 ghi:** "không thấy Monument" — Monument lệch ≈ 46° khỏi trục nhìn P1 (nửa góc ngang ≈ 30°) và **không có mã Monument trong mặt nạ 2 ở mọi khung M02** → ngoài khung, chuỗi `--moc` nêu thừa (cùng loại H3-01 ở B1). M02 k235 (1677,06): thân St Paul's mới đang xây (mã 20) ĐẠT; k236 (1675,57), k239 (1671,1), k241 (1668,1) ĐẠT |

## §5 Việc 5 — Kiểm
- **k2check 1.17.9 trên v5b** (log dựng thật): **MAY-19 CẢNH BÁO, lỗi (a)…(f) = 0** (3 (g) `cu_may 'TL'` có từ v4); **GOC-CAO ĐẠT 0**; **N2P-E ĐẠT** (tập chỉ khai tấm E-P9 có sẵn; M01 vẫn 3D); N2P-E tấm thử ở §2. Các hàng TRƯỢT còn lại **giống hệt v5 B1** (Q37, NHIP-K2, Q37 (1.13), K-LAI-2, K-LAI-3, XEM-CAM — chờ B3/âm thanh); chỉ GOC-CAO đổi CẢNH BÁO → ĐẠT.
- **Tờ khung** đầu/giữa/cuối: **`reports/ban-cuoi-t4-b2a/to-khung-moc.jpg`** (0,82 MB), **`to-khung-hoi2-dau.jpg`** (1,19 MB).
- **Tự soi bằng mắt:**
  - Niên đại: M02 lùi đúng (2026 kính → Victoria/Wren → nhà gạch 1668 + vỏ Old St Paul's); H2-00/H2-03b nền tro + gốc tường; H2-04a/H2-05 nhà gạch Rebuilding Act mọc dần, vỏ Old St Paul's có ô cửa (sau sửa).
  - Lửa: M00 vòng lửa **liền** suốt cung VONG; M03 mặt lửa liền, khói thành cột liền (không cụm bông); M04 lửa lò bánh nhỏ đúng ≈ 01:00.
  - Nước đêm: M00/M03 mặt sông tối có vệt ánh lửa, không mảng cát; M04 sông xanh đêm.
  - **Độ sáng TB khung giữa (0–255, luma):** M00 **49,0** · M03 **34,0** · M04 **15,6** · H1-01h **15,4** (B1-Q5: chỉnh ở B3, `nang_toi`).
  - Ghi cho điều phối soi độc lập: (1) M00 ở 165 m thấy rìa mặt đất mô hình thành dải tối phẳng tới chân trời (đêm — đọc như đồng quê tối; có ở máy B1); (2) H2-02 đoạn đầu gần nhìn thẳng xuống (XUONG từ 2 199 m, theo bảng; lớp MAP3D phủ 4 s ở B3); (3) M04 khung cuối: mặt tường nhà thờ ánh lửa theo mảng (kiểu lửa B1); (4) liền mạch phế tích H1-18 (kiểu cũ) → H2-00 (kiểu mới).

## §6 Việc 6 — Ước lại B2b, B3 (s/khung đo thật)
Thông lượng đo B2a **6,5 s/khung (P = 2)**; nếu máy phiên sau chậm như B1 (11,6) dùng cột phải.

| Phần | Khung | Giờ dựng @6,5 | @11,6 |
|---|---|---|---|
| **B2b**: H2-05s, H2-06, H2-08, H2-09, H2-10 (v5), H2-11, H2-12 (KHOP 2 máy), H2-14 | 1 977 | 3,6 h | 6,4 h |
| + HỒI 4 | 1 322 | 2,4 h | 4,3 h |
| + lấp khối Victoria ngoài City (B1-Q4: viết + thử ≈ 1,5 h) + dựng lại H3-03 | 227 | 0,4 h (+1,5) | 0,7 h (+1,5) |
| + dữ liệu (GHIM=1) + soi năm biên + kiểm | — | ≈ 0,8 h | ≈ 0,8 h |
| **B2b tổng** | **3 526** | **≈ 8,7 h** | **≈ 13,7 h** |
| **B3**: HỒI 5 (+ tấm E H5-05a) | 2 238 | 4,0 h | 7,2 h |
| + Omni 720p 31 clip + âm + ghép + xuất + G2 | — | 3–4 h | 3–4 h |
| **B3 tổng** | | **≈ 7,5–8,5 h** | **≈ 10–11 h** |

- **Gemini T4 tổng dự kiến:** đã tiêu **$19,16** (B2a: $0) + Omni 720p 31 clip ≈ $18,5–19,0 (+ ≤ 30 % làm lại → ≤ $24,7) → **$37,7–43,9** / mốc $50 / chặn $55 (không đổi so B1).

## §7 Chi phí thật (sổ trong `reports/ban-cuoi-t4-b2a/`, mọi dòng có `usd`)
| Nhà | Phiên này | Mốc / chặn | Chi tiết |
|---|---|---|---|
| Gemini | **$0** | T4 tổng $19,16 / $50 / $55 | không Omni |
| OpenAI | **$0,069** | $1 / $3 (chỉ để sinh lại tấm) | **lệch nêu rõ:** 1 lệnh gpt-6.1-sol là mô hình nhìn N2P của k2check (`--n2p-vision`, `so-ai.jsonl`); không sinh lại tấm (0 lệnh ảnh) |
| Claude API | **$1,199** | $2 / $5 | q_thoi_dai lớp mốc 38 lệnh $1,130 (`so-ai-claude.jsonl`) + mô hình nhìn N2P 1 lệnh $0,069 (`so-ai.jsonl`) |
| ElevenLabs · RunPod | 0 · 0 | | |
| **Giờ máy** | **≈ 7,3 h** (01:19 → ≈ 08:35 UTC) | 12 h | dựng 6,2 h (gồm 0,5 h mất do OOM) |

## §8 Sự cố
1. **OOM giết M00 lần 1** (02:26, khung 178/408, ≈ 31 phút máy): tôi chạy lượt thử phế tích (tiến trình dựng thứ 3) cạnh M00 + M01 vừa khởi động; cgroup giết Chromium. Dựng lại M00 từ đầu 02:38 (đầu hàng C, dừng M02 vừa chạy 10 s). Sau đó không chạy tiến trình dựng thứ 3. Bài học: "chờ RAM ≥ 5 GB" chỉ kiểm lúc khởi động, không chặn tiến trình đang lớn dần → giữ cứng P ≤ 2 kể cả lượt thử 1–2 khung.
2. **Hình học tái tạo khác SHA B1** (`ldn2.bin` `d4d4e6a7…` ≠ B1 `77579f6c…`): `tai_osm.py` tải OSM API **sống** → sửa OSM sau 26/10 làm lệch. Đo: 394/394 toà đổi năm trùng id, 2 toà lệch > 3 m, lệch tâm TB 2 m; khung H1-01h máy cũ lệch TB 2,6/255 so B1. **Thuyền** lấy mẫu loại bỏ trên mặt nạ nước (hạt giống cố định) nên dãy lệch: M01 2026 còn 1 sà lan trong khung (B1/phiên A: 4). Ghim `osm2026-b2a.json.gz` + `thuyen-b2a.json` vào git; `du_lieu_b2a.sh GHIM=1` khôi phục cho B2b/B3.
3. Lần sửa phế tích đầu không có tác dụng (Old St Paul's là lớp 5, không phải lớp 2) → trang gỡ lỗi tô màu theo lớp/vật liệu + albedo (mặt nạ 6) → tìm đúng nguyên nhân (bóng + không chi tiết); 4 lượt thử 1–2 khung.
4. Dòng chú thích SHA256SUMS ghi chữ `trang=$trang` (biến trong chuỗi định dạng nháy đơn) ở H1-01h, M01 → sửa script + 2 dòng (commit d1bbcd99).
5. Hàng chờ sai PID (PID 1 luôn sống) khi chia hàng C — phát hiện ngay, khởi lại (≈ 20 s).
6. Wikimedia trả 429 ở bước tư liệu (không dùng cho hình học) — bỏ qua.
Không lỗi nào lặp ≥ 3 lần cùng cách.

## §9 Chỉ số trong ±5 % quanh ngưỡng
| Chỉ số | Giá trị | Ngưỡng | Lệch |
|---|---|---|---|
| Thời lượng / M-d dài nhất / chốt 3 / MÓC 4 loại (từ v4, không đổi) | 770,874 s / 8,0 s / 2 / 4 | 780 / 8 / 2 / 4 | −1,2 % / 0 / 0 / 0 |
Ngoài ±5 % nhưng nêu: đẩy 2D 1,00 %/s (trần 1,5; −33 %); GOC-CAO HỒI 1 51 % (≥ 40); dải trời M00 15 % (LOOK-2 8–20 %); N2P-5 nhấp nháy 0,894 / trần 1,680.

## §10 Dòng sổ đề xuất (P ghi — phiên không sửa sổ)
- **COST-LEDGER:** `2026-10-27 · BAN-CUOI-T4-B2a · Gemini $0 → T4 tổng $19,16 · OpenAI $0,069 (mô hình nhìn N2P, không sinh ảnh) · Claude API $1,199 (q_thoi_dai 38 lệnh $1,130 + mô hình nhìn $0,069) · ElevenLabs 0 · RunPod 0 · ≈ 7,3 h máy`.
- **RIGHTS:** không tài sản mới; tấm E dùng lại ảnh AI E-P1-ngay-l2 của phiên A (đã có sổ); vector OSM ghim trong git `ban-cuoi/may/b2a/osm2026-b2a.json.gz` — © OpenStreetMap contributors, ODbL 1.0 (như dữ liệu OSM hiện có).
- **AUTHORSHIP:** khi chủ dự án trả lời §11 (đặc biệt B2a-Q1 M01).
- **BAI-HOC-K2 (đề xuất):** (1) không chạy tiến trình dựng thứ 3 kể cả lượt thử ngắn — OOM giết tiến trình dài (B2a 178 khung); (2) dữ liệu OSM API là dữ liệu sống → ghim vector đã dùng vào git để các phiên dựng cùng một tập phim trùng hình học/thuyền; (3) phế tích không mái phải có ô cửa + lòng được nắng, không chỉ nhân tối — soi lớp mốc bắt "toà hiện đại"; (4) soi năm biên: khi ô cắt mặt nạ 2 không chứa mốc thì soi toàn khung và đối chiếu mã mặt nạ để tách "vắng" khỏi "ngoài khung"; (5) biến shell trong chuỗi định dạng `printf` nháy đơn không được thay.

## §11 Quyết định cần chủ dự án
| # | Việc | Phương án | Ưu | Nhược | Tác động | Rủi ro | Khuyến nghị |
|---|---|---|---|---|---|---|---|
| **B2a-Q1** | M01: E hay 3D (§2, phiếu) | (a) giữ 3D (bảng hiện tại); (b) dùng E — cần duyệt tấm nước AI (K1179-D6) + ngoại lệ N2P-1 (b) (GPT không kiểm được St Mary Somerset; máy 0/255) + chấp nhận ánh sáng đứng 14 h; (c) E nhưng hoà ≥ 2 s về 3D cuối M01 để nối M02 | (a) liền look với M02 (cùng điểm P1), giữ chiều 14 → 18 h, 0 thủ tục; (b) ảnh thật hơn hẳn ở nhà thường/nước/nền xa; (c) vừa ảnh thật vừa nối M02 | (a) look 3D ở shot "nhận ra nơi chốn"; (b) nhảy look ở cắt M01 → M02, cầu/kè CG trên nước AI, 9 (w) người đọc; (c) thêm một hoà, hai look trong một shot | MÓC | (b)(c) G2 cần duyệt tấm + ngoại lệ | **(a)** cho M01 (liền mạch M01 → M02 KEO là ưu tiên); dành E cho shot 2026 không nối thẳng 3D cùng điểm (H5) |
| **B2a-Q2** | Sửa phế tích sau cháy trong trang dựng hiện hành (§1b) | (a) giữ (đã dùng ở H2-00…H2-05; áp tiếp B2b 1666,69–1700, gồm H2-05s); (b) bỏ, về khối tối | (a) hết "toà hiện đại", vỏ Old St Paul's đọc được; khung ≤ 1666,68 trùng tuyệt đối | (a) phế tích lúc cháy (HỒI 1, đã duyệt) vẫn kiểu cũ | HỒI 2 | (b) q_thoi_dai báo lỗi thời đại | **(a)**; ghi Kinh thánh §19 (d) |
| **B2a-Q3** | Ghim dữ liệu OSM cho B2b/B3 (sự cố 2) | (a) B2b/B3 chạy `du_lieu_b2a.sh GHIM=1` (vector B2a trong git); (b) tải lại OSM sống | (a) trùng hình học + thuyền B2a | (a) không cập nhật OSM mới (không cần cho phim) | B2b, B3 | (b) lệch toà/thuyền giữa các phiên | **(a)** |
| **B2a-Q4** | Chi phí mô hình nhìn N2P gọi OpenAI ($0,069) ngoài mục đích mốc OpenAI phiên này | (a) chấp nhận + từ nay khai mô hình nhìn N2P vào mốc OpenAI; (b) chỉ chạy mô hình nhìn khi lệnh cho phép OpenAI | (a) kiểm đủ N2P | | chi phí | thấp | **(a)** |

## §12 Việc chờ chủ dự án
1. Trả lời §11 (B2a-Q1…Q4); xem `M01-E-vs-3D.jpg` + 2 bản xem, `may-B1-Q1-truoc-sau.jpg`, `to-khung-moc.jpg`, `to-khung-hoi2-dau.jpg`.
2. Nếu chọn E cho M01 (B2a-Q1 (b)/(c)): duyệt tấm `E-M01-l2-thap-bo_dat` (dòng AUTHORSHIP có ngày-giờ) + ngoại lệ N2P-1 (b).
3. Phiên P: merge nhánh khi duyệt; ghi sổ §10; Kinh thánh: B1-Q1 kết quả (M00 165 → 155 m kp 0, H1-01h 160 m), sửa phế tích §1b, ghim OSM.
4. Phiên B2b: dùng `GHIM=1`, trang `bc/look3-b1` (đã sửa phế tích) và `bc/look3-b1d` cho H2-05s (look2d tầm phố); ước §6.

**DỪNG chờ chủ dự án.**
