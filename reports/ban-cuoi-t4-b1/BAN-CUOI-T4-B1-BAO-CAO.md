**Nhánh thật: `claude/k2c-t4-02-final-b1-t9ekhx`** (harness buộc; lệnh ghi `k2c-t4-02-final-b1`). Gốc origin/main @5453a8b2 (khớp lệnh). Đẩy nhánh, KHÔNG merge, KHÔNG tạo PR.

# BAN-CUOI-T4-B1 — bản cuối T4 London (K2C-T4-02), phần B1: sửa 3D chung (D-A4) + dựng 1080p HỒI 1 + HỒI 3 (+ H3-05c) — BÁO CÁO

> Phiên 26/10/2026 03:42 → ≈ 22:10 UTC (10:42 → ≈ 05:10 ngày 27, Asia/Saigon). Mọi số là số đo thật trong phiên.
> **Căn cứ:** chủ dự án 26/10/2026 10:08 "Duyệt PHIẾU-A theo khuyến nghị điều phối" (AUTHORSHIP D-A1…D-A9; Kinh thánh 86daf2d5 §14.7 LOOK-T4-9, §15 (k), §19 (d)). **D-B1** (LFS bản dựng trung gian) = chủ dự án dán lệnh phiên này: **giờ dán 26/10/2026 10:41:56 Asia/Saigon = 03:41:56Z** (giờ tạo phiên, đọc từ `get_session`).
> Email chủ dự án không có trong tệp/commit/header/URL/payload/User-Agent (UA `CineLab-research (+https://github.com/HungQuach301/cine-lab)`). Khoá API do proxy gắn, không in/ghi. Không đọc mã `checks/` (chỉ chạy `k2check.py`, `q_thoi_dai.py`, `lock.py --verify`).

## §0 Nhánh, SHA, khối vận hành

| Mục | Lệnh | Thực tế |
|---|---|---|
| Gốc | origin/main @5453a8b2 | **5453a8b2** khớp (fetch 03:44 UTC) |
| Vùng sửa | `ban-cuoi/**`, `design/k2v/ldn/**`, `scripts/k2ldn/**`, `reports/ban-cuoi-t4-b1/**` + D-B1 | đúng: `ban-cuoi/{dung,may/b1,omni-b1,dac-ta-v5}`, `design/k2v/ldn/bc/look3-b1.js` (tệp mới; `thu-b/look3.js` không sửa), `scripts/k2ldn/bc/*_b1*`, `reports/ban-cuoi-t4-b1/**`; **D-B1**: thêm đúng 1 mẫu (+ dòng chú thích) vào `tools/lfs-allow.txt` và `.gitattributes`. KHÔNG sửa `checks/`, `checks-appeal.md`, `docs/`, sổ, `BANG-SHOT-v1…v4`, `dac-ta-v4/**`, `channel-k2/k2c-t3-01/**`, animatic/âm thanh cũ, main |
| LOCK | `--verify` | KHỚP 1.17.8 `045b7bb7…` ở mọi commit (preflight) |
| Preflight / hook | pipefail, chỉ commit khi "— ĐẠT"; hook trước lần đẩy đầu | `reports/ban-cuoi-t4-b1/cam_commit.sh`; pre-commit + pre-push → `tools/preflight.sh` cài 03:46, lần đẩy đầu 03:50 |
| LFS | đẩy ngay sau mỗi shot; `git lfs ls-files` trước khi báo xong | `git lfs push origin <nhánh>` trước `git push` (K33) trong `xong_b1.sh` sau MỖI shot; **27/27 tệp có trong `git lfs ls-files`**; tải công khai media.githubusercontent.com H1-02h SHA khớp |
| Đẩy ≤ 30 phút + CHECKPOINT | | mỗi shot 1 commit + nhịp CHECKPOINT 25 phút (`nhip_b1.sh`); `reports/ban-cuoi-t4-b1/CHECKPOINT.md` |
| Tiến trình nền | PGID, một vòng nặng, P ≤ 2, RAM ≥ 5 GB | hàng `dung_b1.py` P = 2 (chờ RAM ≥ 5 GB); dừng `du_lieu.sh` bằng `kill -- -PGID`. **Lệch nêu rõ:** 2 lần chạy việc nhẹ (k2check, thử 960×540 1 khung) cạnh 1–2 tiến trình dựng; **1 lần `pgrep -n -x python`** (không `-f`, chỉ in) |
| Force / amend / dừng hỏi | không | không |
| Đầu vào /var/tmp | SHA + cách tái tạo | `reports/ban-cuoi-t4-b1/SHA-du-lieu-ngoai-git.txt` (ldn2.bin, hid/nid, 13 lightmap; 2 bộ hình học) |

## §1 Việc 1 — Sửa 3D chung (D-A4)

Trang dựng **`design/k2v/ldn/bc/look3-b1.js`** sinh bằng `scripts/k2ldn/bc/tao_look3_b1.py` = bản sao `thu-b/look3.js` + các chỗ thay có kiểm số lần khớp (look3 cờ d giữ nguyên). Hình học **`scripts/k2ldn/bc/hinh_hoc_b1.py`** = THU-B d + sửa niên đại toà OSM (thay `bc/hinh_hoc_e.py`). Tờ so: `reports/ban-cuoi-t4-b1/sua/`, mẫu trước | sau: **`reports/ban-cuoi-t4-b1/mau-sau-sua.jpg`** ("trước" = cùng khung, cùng hình học, trang look3 của phiên A).

### (i) Niên đại công trình mốc (§19 (d))
- **Nguyên nhân đo được:** look3 cho mọi phần công trình lớp 5 "mọc" 1,5 năm bằng cách bóp dẹt khối từ mặt đất. Vỏ vòm mã 1708,5 → ở 1709,5 mới 74 % → nằm trong trống: **H2-10 1709,5 không có vòm** (K99). Bầu Monument mã 1676,9 → xong 1678,4 (> 1677).
- **Sửa:** lịch xây riêng từng phần theo mã `tl.x` (mã giữ nguyên làm mã mặt nạ 2); phần đang xây mọc bằng **mặt cắt dâng dần** (không bóp dẹt):

| Phần | Mọc | Ghi |
|---|---|---|
| St Paul's thân/hợp xướng/cánh ngang | 1675,5 → 1697 | khởi công 1675 |
| Trống + hàng cột + gác | 1697 → 1705 | |
| Mặt tây + 2 tháp tây | 1702 → 1708 | |
| Vỏ vòm chì | 1707,3 → **1708,0** | lần 1 đặt 1705 → 1708; soi H2-09 1707,86 vẫn đọc "vòm hoàn chỉnh" → dời |
| Đèn lồng + quả cầu + thập giá | 1707,95 → **1708,0** | |
| Monument bệ / thân có rãnh / đầu cột + chóp / bầu lửa | 1671 → 1672,5 / 1672,5 → 1675,5 / 1675,5 → 1676,5 / 1676,5 → **1677,0** | thân: 20 rãnh dọc đọc được (sọc sáng/tối theo góc quanh tâm cột) |

- **Soi năm biên** (danh sách từ bảng v4: shot 3D có St Paul's mới/Monument năm 1666–1711): H2-05s, H2-06, H2-08, H2-09, H2-10 (máy v5), H2-11, H2-12-b, H2-14, H3-01, H3-06-b — 24 khung 1080p ở năm đầu/cuối shot + 1675 / 1708,0 / 1709,5 / 1711; đo mặt nạ 2 (`sua/soi/soi-do-mat-na2.json`) + **q_thoi_dai lớp công trình mốc** (`sua/soi/qtd-*.json`, sổ `so-ai-claude.jsonl` có usd). Tờ: **`sua/i-nien-dai-soi.jpg`** (ô cắt theo mặt nạ 2 + trước/sau H2-10 1709,5 và H2-09 1707,86).

| Kết quả | Khung |
|---|---|
| **ĐẠT 20/24 khung** (lượt cuối) | H2-05s k187; H2-06 k277 (1675: bệ + thân Monument, chưa St Paul's); H2-08 ×3; H2-09 k0; **H2-09 k239 (1707,86) lần 3 ĐẠT** (vòm dở, chưa đèn lồng); **H2-10 1708,0 / 1709,5 / 1711 ĐẠT** (vòm + đèn lồng); H2-11 ×2 (1676: Monument chưa bầu, St Paul's nền móng); H2-12-b ×2; H2-14 ×3; H3-01 k0; H3-06-b ×2 (1666: chỉ Old St Paul's) |
| Ghi 4 (không sửa ở B1, lý do) | **H2-05s k0 (1670):** khối tối không cửa giữa mái nhà — phế tích tháp nhà thờ cháy (lớp 2), đúng niên đại nhưng hình khối trơn → đề xuất B2 thêm chi tiết · **H2-06 k0 (1671,0):** "Monument vắng" — năm biên đầu (tháng 1/1671, móng); chấp nhận · **H2-06 k414 (1676,99):** "không thấy St Paul's" — thân mới cao ≈ 2,9 m theo lịch tuyến tính (công trường thật cao hơn) → đề xuất B2 cân nhắc lịch thân nhanh hơn ở đầu · **H3-01 k71 (1798):** "không thấy Monument" — Monument ngoài khung, chuỗi `--moc` của phiên nêu thừa · (H2-09 k239 lần 1–2 bị ghi trước khi dời lịch vỏ vòm; lần 3 ĐẠT). Đính chính: thông điệp commit b53ddce9 ghi "18 ĐẠT, 6 ghi" là đếm sai — đúng là 19 ĐẠT, 5 ghi ở lượt đầu |

### (ii) Đốm đen hình elip trên mặt nước 2026
- **Nguyên nhân (đo):** `thuyen.json` có **6 sà lan (barge) 1990–9999** (+ 26 sà lan 1900–1950); hình thuyền "barge" = chỉ thân, màu sRGB (0,16; 0,14; 0,12) → tuyến tính 0,018, **không boong** → nhìn từ trên là elip gần đen (M01, và cả cảnh 1900–1950). Không phải bóng.
- **Sửa:** thuyền nhóm theo kiểu + thời kỳ; sà lan: thân sơn (2026 xanh xám / 1900–50 nâu), boong 24 × 5,6 m, 2026 thêm 3 công-te-nơ màu, 1900–50 bạt phủ hầm. Tờ: **`sua/ii-nuoc-2026-M01.jpg`** (hết elip đen).

### (iii) M00 mở lạnh (P1b, VONG) — nước đêm + lửa
- **Nguyên nhân:** (1) ánh lửa trên mặt sông cộng thẳng bản đồ lửa mờ rộng (12 ô × 8) → mặt sông thành mảng phẳng màu cát; (2) phản chiếu phẳng **bỏ phần phát sáng** (lửa/tàn/quầng cộng với alpha 0 trong RT) → không có vệt lửa phản chiếu; (3) khói đêm mép cứng, hắt sáng đều từng cụm → "cụm bông rời".
- **Sửa:** ánh lửa nước giảm ≈ 4 lần, điều theo sóng + Fresnel; giữ phần phát sáng của RT phản chiếu; hệ số phản xạ đêm cháy (1666/1940) tăng tới ≤ 0,6; quầng lửa to hơn (44–84 m) → vòng lửa liền; khói đêm mép mềm, mỏng hơn, 4 hạt/ô (3 → 4). **Máy M00** VONG 17 s ±12,5° quanh tâm nhìn P1b (≈ 1,5°/s), 125 → 112 m, giờ 19,6 → 20,6 (`ban-cuoi/may/b1/M00.json`; dựng ở B2).
- Tờ: **`sua/iii-M00-dau-giua-cuoi.jpg`** (đầu/giữa/cuối trước | sau + `M00-moi-a.jpg`).
- **Phát sinh khi tự soi tờ khung HỒI 1:** máy tầm phố cạnh đám cháy (H1-13a/H1-13c) bị quầng to làm cháy trắng → quầng giảm khi cách máy < 320 m (≥ 320 m không đổi); thử trước/sau **`sua/iii-b-quang-lua-gan-H1-13.jpg`**; **dựng lại H1-13a + H1-13c** (317 khung).

### (iv) Vật liệu St Paul's + toà tháp + đêm 2026 (Q-A4 (a))
- Đá Portland lớp 5: vỉa 0,62 m × khối 1,1–1,6 m sáng/tối lệch, vệt chảy, ám khói than theo thời kỳ (1720 → 1860 tăng, sạch dần 1995 → 2011). Mái chì: xám sáng (không đen), mạch tấm, vệt ô-xít, ánh trời nhẹ, gân 24.
- Toà kính rèm: mỗi toà một loại (màu kính 4 nhóm, khung, nhịp 1,2/1,5/3 m, tầng 3,6–4,3 m, dải spandrel); **kính rèm trước 1985 đọc thành văn phòng bê tông** (niên đại).
- Đêm (từ 1951): **đèn pha St Paul's + Monument**; cửa sổ đêm theo toà + tầng (tỉ lệ sáng 12–78 %/toà, tầng sáng thành dải, ấm/lạnh, độ sáng khác nhau, xa giảm nhấp nháy) thay lưới ô ngẫu nhiên đều.
- Tờ: **`sua/iv-vat-lieu-ngay-dem.jpg`** (P1 ngày M01, P1 đêm H5-08, P9 ngày, P9 đêm; trước | sau).

### (v) MAY-19 (a)
- H2-10 THAP: ngửa v4 **4,35 → 7,34°** → v5 **6,00 → 8,96°**; H5-05b THAP: **3,95 → 6,94°** → **6,00 → 8,98°** (giữ điểm máy, hướng ngang, nhịp ngửa dần; trong 5–15°).
- Tệp máy `ban-cuoi/may/b1/H2-10-v5.json`, `H5-05b-v5.json`; **log máy (tính từ tệp máy, bản sao `at()` của render_thub.js) vào git**: `…/H2-10-v5-log-may.json.gz`, `H5-05b-v5-log-may.json.gz` (+ `M00-log-may.json.gz`). k2check v5: **MAY-19 lỗi (a) 0**. Tờ: `sua/v-may19-H2-10.jpg`.

### (vi) Niên đại toà 1960s–70s (Q-A5 (a)) + thử lại Omni
- **Nguyên nhân (đo):** `toa_start` ép mọi toà > 120 m về năm ≥ 1995 → **ba tháp Barbican (123 m) vắng ở 1973–1976**; toà thiếu `start_date` nhận năm ngẫu nhiên 1950–2020.
- **Sửa** (`hinh_hoc_b1.py`, không đổi chuỗi ngẫu nhiên chung): bảng năm hoàn thành có nguồn (Cromwell 1973, Lauderdale 1974, Shakespeare 1976, City Point/Britannic House 1967, London Wall Place 2017, 5 Aldermanbury Sq 2007, 20 Ropemaker 2021, 6 hội quán phường hội) — năm xuất hiện = hoàn thành − 2,5 (lớp 4 mọc 2,5 năm); Barbican Estate thiếu năm 1965–1976; hành lang London Wall thiếu năm (trừ nhà thờ/hội quán/tên riêng lịch sử) dựng lại 1985–2020; vùng bom 1940 thiếu năm có năm dựng > 1962 → **178 khối tiền nhiệm hậu chiến** 1953–1961 → năm dựng. **323 toà đổi năm** (`sua/nam-toa-b1.json`). Tờ: **`sua/vi-ban-do-nam-toa.jpg`** (bản đồ toà có mặt 1973/1976: luật cũ ↔ B1).
- Hai lần sửa trong phiên (nêu thật): (1) bảng ghi năm hoàn thành nhưng dùng làm năm xuất hiện → trừ 2,5; (2) quy tắc hành lang gán nhầm năm cho nhà thờ St Giles/St Alban/St Botolph và hội quán → loại trừ + bảng hội quán. HỒI 1/HỒI 3 (≤ 1938) không bị ảnh hưởng (Armourers' Hall nay 1838 — trước đó lô có khối Victoria).
- **Omni 360p** (ảnh đầu từ render 3D cùng năm `md-H5-02b` 1973 / `md-H5-02s` 1976 + OpenAI edits; kiểm 2 mức + lớp mốc như phiên A; `scripts/k2ldn/bc/md_b1.sh`, lệnh `ban-cuoi/omni-b1/lenh/`; H5-02b đổi năm cảnh 1968 → 1973 = năm máy ảnh đầu và năm 3D có tháp — không đổi lời):

| Mã | Lượt | Kết | Lỗi |
|---|---|---|---|
| H5-02b | 1 | TRƯỢT Flash clip | tháp cao "hiện đại" ở chân trời phải |
| | 2 | TRƯỢT Flash clip | xe hơi trắng kiểu khí động học hiện đại; khối tháp tối mép phải |
| H5-02s | 1 | ảnh đầu LOẠI | tháp Barbican bị AI vẽ sai |
| | 2 | Flash ĐẠT, lớp mốc 3/3 ĐẠT, **tầng 2 LOẠI** (1 lỗi mô hình) | |

  → **cả hai giữ 3D**, bảng shot không đổi (không có BANG-SHOT-v5). Clip/ảnh gốc (< 5 MB) trong `ban-cuoi/omni-b1/goc/`, kiểm `kiem/`, `kiem2/`.

## §2 Việc 2 — Dựng 1080p HỒI 1 + HỒI 3 (+ H3-05c)
Trang `bc/look3-b1`, cờ d, spp 4, 1920 × 1080, 24 fps, P = 2 (`scripts/k2ldn/bc/dung_b1.py` → `xong_b1.sh`). Máy/khung/cắt theo bảng v4 (`dac-ta-v4/log-shot.json` t0/t1 → số khung = round(t1·24) − round(t0·24), khung 0… của tệp máy animatic — như `ghep_v3.py`). Danh sách + máy: `ban-cuoi/may/b1/muc-luc-b1.json`. Mã hoá D-B1: H.264 High, CRF 16, veryfast, yuv420p, không âm thanh — **chưa LUT, chưa lớp chồng** (MAP/THE/KHAC… ghép ở B3 từ log máy). SHA256 + số khung: `ban-cuoi/dung/SHA256SUMS`; log máy từng shot: `ban-cuoi/dung/log-may/*.json.gz`.

| Mã | Tệp LFS (`ban-cuoi/dung/`) | Giây | Khung | s/khung/tiến trình | SHA256 | MB |
|---|---|---|---|---|---|---|
| H1-01h | H1-01h-1080p.mp4 | 3.0 | 72 (f 0..71) | 29.61 | `d19fbc571d647c68…` | 11.7 |
| H1-02h | H1-02h-1080p.mp4 | 2.0 | 48 (f 0..47) | 23.04 | `8a705c9ff61842f8…` | 8.5 |
| H1-03 | H1-03-1080p.mp4 | 15.875 | 381 (f 0..380) | 19.97 | `aedd457e707b3702…` | 83.5 |
| H1-04 | H1-04-1080p.mp4 | 10.583 | 254 (f 0..253) | 23.66 | `2bc3ac580acfc4df…` | 56.7 |
| H1-05h | H1-05h-1080p.mp4 | 2.0 | 48 (f 0..47) | 27.26 | `111018185915fc08…` | 11.0 |
| H1-06 | H1-06-1080p.mp4 | 13.5 | 324 (f 0..323) | 21.90 | `399ea8bd4bafdb14…` | 69.7 |
| H1-07 | H1-07-1080p.mp4 | 9.458 | 227 (f 0..226) | 20.74 | `3c419fcf12e8019c…` | 46.2 |
| H1-08b | H1-08b-1080p.mp4 | 18.208 | 437 (f 0..436) | 20.23 | `c8e65802f993680e…` | 77.1 |
| H1-09 | H1-09-1080p.mp4 | 9.0 | 216 (f 0..215) | 26.94 | `ec55c10067c4c852…` | 48.4 |
| H1-11 | H1-11-1080p.mp4 | 8.417 | 202 (f 0..201) | 31.65 | `161c062b94594cc6…` | 33.6 |
| H1-13a | H1-13a-1080p.mp4 (dựng lại) | 7.0 | 168 (f 0..167) | 21.71 | `b240417590b8a6bc…` | 31.2 |
| H1-12x | H1-12x-1080p.mp4 | 7.5 | 180 (f 0..179) | 14.75 | `333f22b262d3b43c…` | 42.9 |
| H1-13c | H1-13c-1080p.mp4 (dựng lại) | 6.208 | 149 (f 0..148) | 22.06 | `732620e79d639b4d…` | 27.3 |
| H1-15 | H1-15-1080p.mp4 | 8.0 | 192 (f 0..191) | 33.10 | `6e312821ed7e983d…` | 41.2 |
| H1-15h | H1-15h-1080p.mp4 | 3.208 | 77 (f 0..76) | 27.34 | `74a675fa8213bf46…` | 13.6 |
| H1-15h2 | H1-15h2-1080p.mp4 | 5.292 | 127 (**f 152..278** của máy H1-15h) | 27.54 | `d5b81bc80d15a011…` | 22.5 |
| H1-16 | H1-16-1080p.mp4 | 7.25 | 174 (f 0..173) | 19.96 | `d23702d2d3dc226a…` | 30.1 |
| H1-18a | H1-18a-1080p.mp4 | 6.0 | 144 (f 0..143) | 28.27 | `5ae0de3c8420a380…` | 33.2 |
| H1-18b | H1-18b-1080p.mp4 | 5.292 | 127 (f 0..126) | 27.17 | `d63b4bfc0eb7321f…` | 20.6 |
| H3-01 | H3-01-1080p.mp4 | 3.0 | 72 (f 0..71) | 18.30 | `c5a6c49e9a232170…` | 16.9 |
| H3-02 | H3-02-1080p.mp4 | 6.792 | 163 (f 0..162) | 23.79 | `1fa4c43fe8ccd680…` | 35.7 |
| H3-03 | H3-03-1080p.mp4 | 9.458 | 227 (f 0..226) | 23.53 | `34b519ad7534ebcf…` | 59.4 |
| H3-04a | H3-04a-1080p.mp4 | 5.0 | 120 (f 0..119) | 18.71 | `cd217a6645b63a7c…` | 26.6 |
| H3-05 | H3-05-1080p.mp4 | 13.708 | 329 (f 0..328) | 14.99 | `8ae1266cd4543faa…` | 83.2 |
| H3-06 (KHOP) | H3-06-a-1080p.mp4 + H3-06-b-1080p.mp4 | 4,5 + 4,5 (bảng 8,0; hoà ở B3) | 108 + 108 | 18.12 / 16.94 | `677be1da2a3c3750…` / `824b990106474f71…` | 13.7 / 15.3 |
| **H3-05c** (dự phòng) | H3-05c-1080p.mp4 | 6.0 | 144 (f 0..143) | 15.48 | `0a285b5d8068d1c6…` | 22.5 |

- **Tổng 27 tệp, 4 818 khung (+ 317 khung dựng lại H1-13a/c), ≈ 1,03 GB LFS.** Đồng hồ 05:14 → 20:28 UTC (+ dựng lại 20:28 → 21:30): **thông lượng 11,6 s/khung (P = 2)**; mỗi tiến trình 15,0–33,1 s/khung (TB ≈ 22; đêm/lửa nặng nhất). CPU bão hoà (load 8/4 nhân) — P = 3 không có lợi.
- **Cắt có ghi:** H1-15h2 = 127 khung **cuối** máy H1-15h (phần 3D sau clip H1-15x; máy chạy tiếp, kết đúng khung cuối máy, không đóng băng — `dac_ta_v4.py` ghi "cùng máy, thời gian chạy tiếp" nhưng máy v3 chỉ 11,625 s). H1-03: 381/403 khung máy (bảng 15,875 s). H1-06: 324/468 khung (13,5 s; phần sau là clip H1-06x).
- **H3-05c:** soi 3 phương án (`ban-cuoi/may/b1/H3-05c-s20*.json`; tờ `sua/h3-05c-phuong-an.jpg`: A | s20 | s20-l | s20-ll): dịch 20 m về nam đưa tháp tiền cảnh sang phải mái vòm, lộ chân trống + thân; hạ máy làm tháp che thêm → chọn **s20 giữ cao 48 m, hạ điểm nhìn 95 → 85 m**.

## §3 Việc 3 — Kiểm
- **k2check 1.17.8 trên đặc tả v5** (`ban-cuoi/dac-ta-v5/`, sinh bằng `scripts/k2ldn/bc/dac_ta_v5.py`: = v4 + log khung 1080p thật của 25 shot đã dựng, log tính cho H2-10/H5-05b/M00; còn lại giữ log animatic): `dac-ta-v5/k2check-1.17.8-dac-ta-v5.md` (rc 1 — các TRƯỢT cũ Q37/NHIP-K2/K-LAI-2/XEM-CAM không đổi).
  - **MAY-19: CẢNH BÁO, lỗi (a)…(f) = 0** (H2-10, H5-05b hết (a)); còn 3 (g): `cu_may 'TL'` của H1-18t, H5-02t, H5-06t (loại TL/THAT không thuộc §19 (a) — có từ v4).
  - **GOC-CAO: CẢNH BÁO** — 460,9 / 754,9 s = **61,1 %** (≥ 50); chương MÓC 81, HỒI 1 **49**, HỒI 2 62, HỒI 3 65, HỒI 4 64, HỒI 5 68 (≥ 40); **(a) 2: M00 và H1-01h mở chương nhưng chưa được nhận là góc cao** (log máy: H1-01h 120 m, M00 125 → 112 m). Thử bằng bản sao tạm (không giữ): đặt cao 160 m → **GOC-CAO ĐẠT, 0 cảnh báo** → xem Quyết định B1-Q1.
- **Tờ khung mỗi chương** (đầu/giữa/cuối): **`reports/ban-cuoi-t4-b1/to-khung-hoi1.jpg`**, **`to-khung-hoi3.jpg`**.
- **Tự soi bằng mắt:** niên đại (H2-09/H2-10 sửa xong; H3-01/H3-05/H3-06 vòm đủ, 1666 chỉ Old St Paul's), lửa (vòng lửa liền; H1-13a/c cháy trắng → sửa + dựng lại), nước (hết mảng cát/elip đen), công trình có tên (vòm chì xám, đá Portland ám khói 1711–1938). **Ghi cho điều phối soi độc lập:** (1) H1-01h, H1-02h rất tối (đêm 01:00–02:00, lửa nhỏ) — như animatic; bước ghép có `nang_toi`; (2) **H3-03 (1860–1871, nhìn xuống)**: các vùng ngoài lõi City là nền xám sáng gần như không nhà (Westminster/Southwark 1860s chưa có khối) — có từ hình học look2, B1 không đổi; lớp MAP3D phủ 4 s; (3) H1-11 giữa shot có lóa mặt trời trên sông, cuối shot vào đêm (theo máy animatic).

## §4 Việc 4 — Ước lại B2/B3 (thông lượng đo 11,6 s/khung, P = 2)

| Phần | Khung | Giờ dựng |
|---|---|---|
| MÓC (M00–M04; lửa đêm, có thể nặng hơn TB) | 1 631 | ≈ 5,3 h |
| HỒI 2 (14 shot; H2-12 KHOP 2 máy) | 3 292 | ≈ 10,6 h |
| HỒI 4 | 1 322 | ≈ 4,3 h |
| HỒI 5 (+ tấm E H5-05a) | 2 238 | ≈ 7,2 h |
| Omni 720p 31 clip + âm + ghép + xuất + G2 | — | ≈ 3–4 h |

- B2 nguyên (MÓC + HỒI 2) ≈ **15,9 h** > 12 h → **đề xuất chia lại:** **B2a** = MÓC + H2-00…H2-05 (2 946 khung ≈ 9,5 h + nạp dữ liệu ≈ 0,5 h); **B2b** = H2-05s…H2-14 + HỒI 4 (3 299 khung ≈ 10,6 h); **B3** = HỒI 5 + E H5-05a + B + Omni 720p + âm + ghép + xuất + G2 (≈ 7,2 + 3–4 ≈ 10–11 h).
- **Gemini T4 tổng dự kiến:** đã tiêu **$19,16** (sau B1) + Omni 720p 31 clip ≈ $18,5–19,0 (+ ≤ 30 % làm lại → ≤ $24,7) → **$37,7–43,9** / mốc $50 / chặn $55.

## §5 Chi phí thật (từ sổ trong `reports/ban-cuoi-t4-b1/`)
| Nhà | Phiên này | Mốc / chặn | Chi tiết |
|---|---|---|---|
| **Gemini** | **$0,581** | **T4 TỔNG $19,16** / mốc $50 / chặn $55 | Omni 360p 3 lệnh ($0,529) + Flash 7 lệnh ($0,052) — `so-ai-gemini.jsonl`; 0 lỗi 402 |
| **OpenAI** | **$0,390** | mốc $2 / chặn $5 | ảnh gpt-image 4 lệnh $0,305 (`so-ai.jsonl`) + gpt-6.1-sol tầng 2 3 lệnh $0,085 (`cost.jsonl`) |
| **Claude API** | **$0,806** | mốc $3 / chặn $8 | q_thoi_dai lớp mốc 32 dòng (`so-ai-claude.jsonl`, có usd từng lệnh) |
| ElevenLabs · RunPod | 0 · 0 | | |
| **Giờ máy** | **≈ 18,5 h** (03:42 → ≈ 22:10 UTC) | **14 h** | **VƯỢT ≈ 4,5 h (+32 %)**: dựng 1080p đo 11,6 s/khung (phiên A ước 8,58 từ mẫu ngày) + dựng lại H1-13a/c 1 h — chọn dựng đủ thay vì cắt chất lượng (nguyên tắc tối cao) |

## §6 Sự cố
1. Bước kiểm `git lfs ls-files | grep -q` trong `xong_b1.sh` trả lỗi giả do `pipefail` + SIGPIPE ở shot đầu (H1-02h) → hàng dừng đúng thiết kế dù LFS + đẩy đã THÀNH CÔNG (tải công khai SHA khớp) → sửa (lưu đầu ra trước khi grep), chạy tiếp; mất ≈ 1 phút.
2. Lịch vỏ vòm lần 1 (1705 → 1708) vẫn để H2-09 1707,86 đọc "vòm hoàn chỉnh" → dời 2 lần (q_thoi_dai 3 lượt khung này).
3. `hinh_hoc_b1.py`: 2 lỗi quy tắc của phiên (năm hoàn thành ≠ năm xuất hiện; quy tắc hành lang chạm công trình lịch sử) → sửa; hình học dựng 3 lần (≈ 7–10 phút/lần).
4. Quầng lửa B1 làm cháy trắng máy tầm phố (H1-13a/c) — bắt khi tự soi tờ khung → sửa + dựng lại 317 khung (≈ 1 h máy).
5. Lỡ xoá 1 dòng sổ Claude (`sed '$d'`) khi dọn lần chạy hỏng → khôi phục từ commit trước, kiểm lại 25/25 dòng.
6. k2check lượt đầu "không chạy được" MAY-19/GOC-CAO vì log máy tính có trường `shot` dạng chuỗi → sửa `dac_ta_v5.py`.
7. Hàng thử 1 khung bị kẹt chờ RAM ≥ 5 GB khi 2 tiến trình dựng chạy → dừng bằng PID, thử lại khi rảnh.
8. Một lần `pgrep -n -x python` (không `-f`, chỉ in kiểm).
Không lỗi nào lặp ≥ 3 lần cùng cách.

## §7 Chỉ số trong ±5 % quanh ngưỡng
| Chỉ số | Giá trị | Ngưỡng | Lệch |
|---|---|---|---|
| GOC-CAO chương HỒI 1 | 49 % | ≥ 40 % | +22 % (ngoài ±5 %, nêu vì giảm từ 50 ở v4) |
| MAY-19 H2-10 ngửa nhỏ nhất | 6,00° | ≥ 5° | +20 % |
| Thời lượng / M-d dài nhất / chốt 3 / MÓC 4 loại | 770,874 s / 8,0 s / 2 / 4 | 780 / 8 / 2 / 4 | −1,2 % / 0 / 0 / 0 (không đổi từ v4) |
Ngoài ±5 % nhưng nêu: giờ máy 18,5 / 14 h (+32 %).

## §8 Dòng sổ đề xuất (P ghi — phiên không sửa sổ)
- **COST-LEDGER:** `2026-10-26 · BAN-CUOI-T4-B1 · Gemini $0,581 (Omni 360p 3 lệnh $0,529; Flash 7 lệnh $0,052) → T4 tổng $19,16 · OpenAI $0,390 · Claude API $0,806 · ElevenLabs 0 · RunPod 0 · ≈ 18,5 h máy (vượt 14 h)`.
- **RIGHTS:** ảnh AI OpenAI 4 (ảnh đầu H5-02b a1/a2, H5-02s a1/a2 — đầu vào render dự án) + 3 clip Omni 360p trượt (không dùng) — SHA trong sổ; không tài sản mới dùng trên phim.
- **AUTHORSHIP:** khi chủ dự án trả lời §9.
- **BAI-HOC-K2 (đề xuất):** (1) công trình mốc đang xây phải "mọc" bằng mặt cắt dâng theo lịch từng phần, không bóp dẹt cả khối; soi lớp mốc ở năm biên bắt được cả lỗi "gần xong đọc thành xong"; (2) RT phản chiếu phải giữ phần phát sáng cộng (alpha 0); (3) đo giờ dựng trên shot đêm/lửa trước khi chia phiên (đêm/lửa 20–33 s/khung so mẫu ngày 14–19); (4) `pipefail` + `grep -q` sau ống dẫn cho lỗi giả — lưu đầu ra trước; (5) quy tắc gán năm toà theo vùng phải loại trừ công trình lịch sử có tên.

## §9 Quyết định cần chủ dự án
| # | Việc | Phương án | Ưu | Nhược | Tác động | Rủi ro | Khuyến nghị |
|---|---|---|---|---|---|---|---|
| **B1-Q1** | GOC-CAO (a): M00 (P1b 125 → 112 m) và H1-01h (120 m) chưa được nhận là góc cao → Chặn ở G2 | (a) nâng máy lên ≈ 160 m (đã thử: ĐẠT); H1-01h dựng lại 72 khung (≈ 0,5 h, ở B2a), M00 dựng ở B2a với máy nâng; (b) giữ độ cao, khiếu nại K (ngưỡng góc cao cho máy mở chương) | (a) qua G2 chắc chắn, không phụ thuộc K; (b) giữ khung P1b đã duyệt (D-A8) | (a) đổi nhẹ khung P1b đã duyệt; (b) chờ K, có thể Chặn | MÓC, HỒI 1 | (a) thấp; (b) trễ G2 | **(a)** |
| **B1-Q2** | Chia phiên B2/B3 (§4) | (a) B2a / B2b / B3 như §4 (4 phiên tổng); (b) giữ B2, B3 và nhận ≈ 16 h/phiên | (a) ≤ 12 h/phiên | (a) thêm 1 phiên (nạp dữ liệu ≈ 0,5 h) | lịch | (b) quá giờ máy, mất tiến trình nếu container dừng | **(a)** |
| **B1-Q3** | H5-02b/H5-02s: Omni trượt 2 lượt sau sửa niên đại | (a) giữ 3D (đã sửa niên đại, tháp Barbican đúng năm) + ảnh thật H5-02t; (b) thêm lượt 3 | (a) không thêm chi phí | phần hiện đại A vẫn 12 s | H5 | thấp | **(a)** |

## §10 Việc chờ chủ dự án
1. Trả lời §9 (B1-Q1…Q3) và duyệt mẫu sau sửa (`mau-sau-sua.jpg`, `sua/*.jpg`) + tờ khung HỒI 1/HỒI 3.
2. Phiên P: merge nhánh khi duyệt; ghi sổ §8; nếu (b) ở B1-Q1 thì chuyển khiếu nại cho K.
3. Phiên K-1.17.9 (đang chạy): KN-7 quyết H3-05b ↔ H3-05c (H3-05c đã dựng sẵn, LFS).
4. Điều phối soi độc lập tờ khung (đặc biệt H3-03 nền trống ngoài City, H1-01h/H1-02h tối).

**DỪNG chờ chủ dự án.**
