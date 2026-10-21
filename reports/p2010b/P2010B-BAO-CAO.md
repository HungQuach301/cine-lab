Nhánh thật: **`claude/p-2010b-master-bible-imxw8d`** (harness buộc tên này). Nhánh cục bộ `p-2010b` cùng SHA, đẩy lên `origin/claude/p-2010b-master-bible-imxw8d`. Tạo từ `origin/main` @`7fe4dcdf`. `main` cập nhật fast-forward ở §6.

# PHIÊN P-2010b: áp 8 điểm duyệt P-2010 §9 + lấy lại master giọng T3. BÁO CÁO. DỪNG chờ chủ dự án

```text
ĐIỀU LỆ PHIÊN P-2010b                                          | thực tế
Loại phiên:        P (điều phối)                                | đúng
Nhánh:             p-2010b từ origin/main @7fe4dcdf              | harness buộc claude/p-2010b-master-bible-imxw8d (dòng đầu); gốc đúng
KHÔNG sửa:         checks/, design/, scripts/, loi-khoa.txt      | đúng; loi-khoa.txt 51d1c773… trước = sau (kiểm bằng máy)
lock.py:           chỉ --verify                                  | đúng; mọi lần KHỚP 1.16.1 a3c39873…
Vùng V7C, NC-V2V3: không đụng, không merge                       | đúng (không đọc, không sửa design/k2v/**, scripts/k2*, v7p/**, reports/v7c/**)
Chi phí:           Claude/OpenAI/YouTube 0; ElevenLabs CHỈ GET   | $0 · $0 · 0 đơn vị; ElevenLabs 0 ký tự: bộ đếm 141 009 → 141 009
Giờ máy:           mốc theo dõi 1,5 h                            | ≈ 0,9 h (23:01 → ≈ 23:55 UTC)
Preflight:         --staged mỗi commit; --range trước khi đẩy main | --staged ĐẠT 4/4 commit; --range: §5
Email:             che; không vào header/URL/payload/UA           | 0 email trong diff; UA "CineLab-research (+https://github.com/HungQuach301/cine-lab)" ở mọi yêu cầu mạng
Khoá:              không in, không ghi                           | đúng (khoá do proxy gắn)
Dừng hỏi:          không dừng giữa chừng                          | đúng
```

## 0. Tóm tắt
| Mục | Kết quả |
|---|---|
| Giọng master | **Đủ 8 phần chương + 3 câu `issmus` đã chọn** tìm thấy trong lịch sử, mỗi đích khớp **đúng 1 mục** (không phải đoán), chữ khớp **11/11**. Ghép lại bằng `reports/kl42/ghep.py` → master **TRÙNG BIT** với master KL42: WAV **`ba50fba7…`**, FLAC **`852b9e41…`**, stem **`79ac3589…`**. Thời lượng **733,532 s** (= KL42). WER sau chuẩn hoá số: **M 2,88 %, S 3,36 %**. **0 ký tự**. Đã vào LFS `channel-k2/k2c-t3-01/am-thanh/master/` (§1) |
| Kinh thánh | SHA-256 `9e7492a5…` → **`50554dcce70fab49b20906aeea598dd0c4bc1130b042d3e817b895add56e83dd`**; 7 chỗ, mỗi chỗ kiểm "đúng 1 lần". "14 Times" trong `docs/` + `phat-hanh/`: **5 chỗ → 0** (§2) |
| Nhạc | 8/8 tải lại, **SHA khớp đăng ký 8/8**, vào LFS `assets/k2/music/` + `SHA256SUMS` (111,5 MB) (§3) |
| Dung lượng LFS | nhánh này/`main` mới: **878,8 MB (42 đối tượng)** — **VƯỢT mốc cảnh báo 800 MB (+9,9 %)**; `main` cũ 579,6 MB; toàn repo (137 nhánh, gồm release-*) **11 803,9 MB** (§3) |
| Sổ | RIGHTS **+1** (DG3V2-AI) + 16 sửa (mẫu "(edited)" duyệt, 8 tệp nay ở LFS) · AUTHORSHIP **+4** dòng nguyên văn · COST-LEDGER **+1** (P-2010b, 20 cột) (§4) |
| Kiểm cuối | lock **KHỚP 1.16.1** · selftest k116 **144/144** · k115 **105/105** · k114 **126/126** · `LOI-KHOA.sha256` **3/3 OK** · preflight `--range` **ĐẠT** · 0 email (§5) |
| main | `7fe4dcdf` → **commit cuối của nhánh này** (commit chứa tệp này, "… DỪNG chờ chủ dự án"), fast-forward, không force (§6) |

## 1. Giọng master KL42 (G1 `VDLncRBHDjLHBqLhQ1Qt`, lời v4.2)
### 1.1 Lịch sử ElevenLabs (chỉ GET) — `reports/p2010/giong_lich_su.py` (chạy lại), `tai_lich_su.py`
- `GET /v1/history?voice_id=G1`: **35 mục G1, 21 mục ngày 19/10** (`lich-su-g1-1910.json`). Bộ đếm **141 009 → 141 009** (đọc trước/sau ở cả hai script).
- **Cách chọn mục, không đoán:** mỗi đích phải khớp đúng 1 mục theo (bộ đếm trước của lượt trong `reports/kl42/bo-dem.jsonl`, độ dài chữ gửi, đầu chữ).
  - Chương 02 và 05 gửi 2 phần song song cùng mốc bộ đếm. Phân biệt bằng đầu chữ.
  - **3 câu thay: lịch sử có 4 lượt mỗi câu** (12 mục 06:56–07:13): `iss-muss` seed 19102027; `isthmus`; **`issmus`**; `iss-mus`. Lượt đã chọn theo `thay.json` (`chon: true`) là lượt `issmus` = dòng 4–6 phần "thu lại" của `bo-dem.jsonl` (140 793 → 140 827 → 140 844 → 140 900). Ba mục khớp đúng chữ `gui` của `thay.json`.
  - Câu 1k#0 thu lúc **07:07:46**, ngoài khung "06:26–07:05" trong lệnh 1 phút 46 giây; vẫn xác định duy nhất bằng bộ đếm + chữ. Master trùng bit (§1.3) xác nhận chọn đúng.
- **Tải:** `GET /v1/history/{id}/audio`. Định dạng: **MP3 44,1 kHz mono ≈ 193 kb/s** (mã yêu cầu `mp3_44100_192`; đây là bản tốt nhất có, gói Creator không có PCM).

| Tệp (LFS `am-thanh/master/nguon-lich-su/`) | history_item_id | Thu (UTC 19/10) | Ký tự | Bộ đếm | Định dạng | Giây | SHA-256 |
|---|---|---|---|---|---|---|---|
| 00-HOOK-p0.mp3 | PpjigMZvUFPb03ltLoy5 | 06:26:53 | 589 | 136 226 → 136 485 | mp3 44,1 k mono 195 kb/s | 42,710 | `54a1e44806b678d7c06c8a9f9efaa7e80120a46101681921b2223db0d6355773` |
| 01-ROCK-p0.mp3 | Hba8YbxYvDuv1jOBvOET | 06:28:41 | 1 740 | 136 485 → 137 251 | 193 kb/s | 129,829 | `b0aac10fc9b96d9e9bf63d09467eef298326d3d015f51d66b67dfdb567701964` |
| 02-SIEGE-p0.mp3 | eTJ441slKrzIlIqeKJUe | 06:30:34 | 1 737 | 137 251 → 138 015 | 193 kb/s | 129,802 | `de42319282fecd4fe57561558dd7103a86b5d765b3eadb5286ca4b40dae5a4ed` |
| 02-SIEGE-p1.mp3 | 4uSLFj5LpOboPUfiJF1Y | 06:30:49 | 1 180 | 137 251 → 137 770 | 194 kb/s | 86,596 | `4de8f9ed6a57ef07e3ab3036cac80b266cf1ea4d7b9c8c9112849242566a938f` |
| 03-NEUTRAL-p0.mp3 | NnJRlSIDIlr4yqSYF481 | 06:32:34 | 1 085 | 138 534 → 139 011 | 194 kb/s | 79,778 | `bc31be81cdd9dee92732d0422411b3b927f570a9ec2d0b6f819efc19a5a7ffde` |
| 04-RUNWAY-p0.mp3 | 7Qyes8jiM4m4sN9jjh8x | 06:34:24 | 1 472 | 139 011 → 139 659 | 193 kb/s | 105,143 | `1a78cb68969264c6385e089a5495067432333f7563ebab953902fa260d042f06` |
| 05-GATE-p0.mp3 | DUacg6iMjyWVSVMYhMpk | 06:36:13 | 1 812 | 139 659 → 140 456 | 193 kb/s | 130,664 | `9f9858ca0ab6e74f797d37fa05ffa280959604b01e265c512a4f57a9117e9e6c` |
| 05-GATE-p1.mp3 | Lqr20hhCYYb7h6zQV7ED | 06:36:16 | 269 | 139 659 → 139 777 | 199 kb/s | 19,409 | `7c6dfb7ef9549ccfa5c869dc58e73a10676818e67d4cac76e87486f64825b31a` |
| 01-thay-1i-0.mp3 (`issmus`) | MlqMTZCYnyF3hG973IGV | 07:04:12 | 78 | 140 793 → 140 827 | 218 kb/s | 5,433 | `08f26eba989fd2fb0ed35f1ac744b84f4ca5eaadbec34a256ddb955850037f42` |
| 01-thay-1i-1.mp3 | IvUQUXkpQDAttASePXAZ | 07:05:59 | 38 | 140 827 → 140 844 | 234 kb/s | 3,344 | `8ae448e39b6d169568ad2e4604c4b76739f856a08014ee2f75442f29588a9e16` |
| 01-thay-1k-0.mp3 | QhrejRzxdD3KUbZxw8TG | 07:07:46 | 128 | 140 844 → 140 900 | 209 kb/s | 8,307 | `e903263a58b067830c62de707319eaf08b14c31da8c62d39e461c2a3e2c1c105` |

- **Chữ:** `kiem_chu.py`. Tách phần như `thu.py` trên `loi-khoa.txt` (`kl_lib.doan_v42` tự kiểm nối lại đúng `loi-khoa.txt`). Alias lấy theo từ điển **tại lúc thu** (commit trước `4cd2d941`, isthmus còn `iss-muss`). Câu thay so với `gui` của `thay.json`. Kết quả: **11/11 KHỚP ký tự**.
- **Thiếu đoạn: không.** Mục lịch sử còn lại của 19/10 (không dùng): 06:23:33 kiểm 47 mục (`kiem47`, 1 180 ký tự) và 9 lượt thu thử isthmus không được chọn.

### 1.2 Ghép lại — `ghep_lai.py` (gọi `ghep.chuong()`/`ghep_cau()` của `reports/kl42/ghep.py`, cùng hằng số)
Lịch sử không trả alignment. Ba nguồn mốc thay cho alignment:
1. **Mốc câu trong chương** (sau ghép) = số KL42 đã ghi trong git: `kiem-tap.json` `cau`, trùng `nhip-that.json` **129/129 câu** (cả hai sinh từ `moc.json` gốc). Mốc tương đối trong phần = mốc chương − dời của phần. Dời đó tính bằng `trim()` của ghep.py trên chính audio tải về, đặt trên lưới 1 ms như `moc()` của `thu.py`.
2. **Hai ẩn số sổ KL42 không giữ.** Suy từ hai bản xem MP3 gốc trong git (`reports/kl42/nghe/…-xem-1/2`, cắt từ master gốc), bằng độ trễ theo mẫu so với phần 1 cùng chương:
   - (a) Vị trí phần 2 của chương 02 và 05 (phụ thuộc alignment ký tự đầu phần). Kết quả: mốc đầu phần = 0,000 s, lệch 0,0 mẫu.
   - (b) Độ dài câu CŨ của 3 câu thay. `ghep_cau()` cắt theo độ dài này. Kết quả: 1i#1 = 3,112 → 2,926 s; 1k#0 = 8,661 s.
3. **Câu cũ 1i#0** nối liền câu thay 1i#1, nên cách (b) không phân biệt được độ dài cũ của nó. Đo riêng bằng `do_khe.py`: 70 ms âm của bản thu chương ở **95,561 s** (khoảng ngừng gốc) nằm ở 94,875 s chương trong bản xem gốc, **r = 1,0**. Vậy câu cũ kết thúc ở 95,306 s, **độ dài cũ 5,573 s**. Ở lần ghép đầu (trước khi đo cách 3), chương 01 lệch đúng ở 80 ms này; sau khi đo thì trùng bit.

| Chương | Giây ghép lại | KL42 (lời liền, §4) | Lệch | Ngừng nối (KL42) | Đầu chương trong stem |
|---|---|---|---|---|---|
| 00 HOOK | 42,678 | 42,68 | ≤ 0,002 | — | 0,000 |
| 01 ROCK | 128,090 | 128,09 | 0,000 | — | 44,678 |
| 02 SIEGE | 217,143 | 217,14 (vị trí stem cho 217,144) | ≤ 0,001 (làm tròn) | 0,859 (0,86) | 174,768 |
| 03 NEUTRAL | 79,737 | 79,74 | ≤ 0,003 | — | 393,912 |
| 04 RUNWAY | 105,094 | 105,09 | ≤ 0,004 | — | 475,649 |
| 05 GATE | 150,789 | 150,79 | ≤ 0,001 | 0,789 (0,79) | 582,743 |
| **Stem** | **733,532** | **733,532** | **0,000** | | |

- Mọi chương **trong ±0,05 s**. KL42 không ghi giây từng phần (chỉ ghi giây chương). Vì vậy mức phần được kiểm bằng tương quan với bản xem: mọi phần r ≥ 0,99, độ trễ hằng (limiter + giải mã MP3).

### 1.3 Master và trùng bit — `xuat_lai.py` (cùng cách chuẩn `xuat.py`), `so_xem.py`
| Tệp | I / TP / LRA | Giây | SHA-256 ghép lại | SHA-256 KL42 (§6) |
|---|---|---|---|---|
| Stem thô 48 kHz/24-bit | −19,0 / −1,7 / 3,8 | 733,532 | `79ac35890190d62d6d87f0d31310ef1850ff2bd4efd264e8d9388a2d4f94ef21` | **=** |
| **Master WAV** 48 kHz/24-bit mono (+5,3 dB, 2 vòng như KL42) | **−14,1 / −1,5 / 3,8** | 733,532 | `ba50fba75aa956731226f7269adbffb6728853d6d2a7fc95b4eefba8e13b586d` | **=** |
| **Master FLAC** (mức 8) | như trên | 733,532 | `852b9e419b40d16657f3280dfb03ef7c422c50434fa63db57c2ace8e5b29b7de` | **=** |

- **Thử triệt** (`so-xem.json`): mã hoá lại bản xem từ master mới bằng đúng lệnh và tham số vòng cuối của `xuat.py`, rồi so mẫu giải mã với bản xem gốc. Cả 6 chương đạt **SNR 248–257 dB**, tức trùng mẫu.
- Tệp trong LFS: `channel-k2/k2c-t3-01/am-thanh/master/` có `T3-loi-G1-v42-14LUFS.wav` (105,6 MB), `.flac` (64,0 MB), `T3-loi-moc.json` (mốc câu/đoạn trong stem), `nguon-lich-su/` (11 MP3) và `SHA256SUMS` (kiểm `sha256sum -c`: 14/14 OK).

### 1.4 ASR — `asr_wer.py`, `wer_chuan.py`, `asr-wer.json`
- faster-whisper, cùng hai cách nghe của KL42: M = medium.en beam 5, S = small.en beam 1, không hotwords. Chạy trên master, từng chương. So với chữ `loi-khoa.txt` của chương; tổng 1 584 từ.
- **WER thô:** M **8,14 %** (129 sửa), S **8,96 %** (142). Phần lớn là cách viết số: lời viết chữ "fourteen thousand", ASR viết "14000".
- **WER sau chuẩn hoá số hai phía** (num2words; năm đọc kiểu năm): **M 2,88 %**, **S 3,36 %**.

| Chương | M | S |
|---|---|---|
| 00 HOOK | 0,00 % | 0,00 % |
| 01 ROCK | 4,18 % | 7,32 % |
| 02 SIEGE | 3,10 % | 3,31 % |
| 03 NEUTRAL | 2,12 % | 2,65 % |
| 04 RUNWAY | 2,41 % | 2,81 % |
| 05 GATE | 3,11 % | 1,98 % |

- **Chỗ lệch còn lại** đúng loại KL42 §4 đã ghi:
  - cách viết của ASR: "Rook", "Elliott", "northeast", "forever", "race course", "III/V";
  - tên theo alias: "Alhaciras", "Darson", "Montair O", "Linaire", "fete a com pli", "duke du crijon";
  - "crossers" → "crosses", "and a half thousand".
- Không có câu thiếu hay thừa. Audio trùng bit với master KL42, nên kết quả 258 ĐÚNG / 1 NGHI / 0 SAI của KL42 áp nguyên.

### 1.5 Ghi chú
- Lượt thu thử `iss-muss` seed 19102027 (06:56:53–06:57:03) có trong lịch sử với bộ đếm 140 574 → 140 684 (+110). `thay.json` ghi `ky_tu: 0` cho lượt này, và `bo-dem.jsonl` không có dòng cho nó. Đây là chỗ hở sổ của KL42 (không phải tiêu dùng mới). Ghi để đối chiếu BAI-HOC #98.
- Tệp làm việc ngoài git (`/var/tmp/cine-out/p2010b/`) không cần nữa: mọi thứ cần giữ đã vào LFS (BAI-HOC #117 không lặp).

## 2. Kinh thánh `docs/BIBLE-KENH2.md` — `sua_bible.py`, `sua-bible.json`
- SHA-256 trước `9e7492a5a6742a0578dc9c06518e92a8ecc077dd345bfdefb426c1438c5631ad`: script kiểm đúng bản P-2010 trước khi sửa.
- SHA-256 sau **`50554dcce70fab49b20906aeea598dd0c4bc1130b042d3e817b895add56e83dd`**.
- Mỗi thay thế kiểm **đúng 1 lần xuất hiện**. Bản nháp §10.6 được kiểm **nguyên văn** với P-2010 §9 mục 3; ba câu trích thực vật được kiểm nguyên văn với `THUC-VAT-1782.md`. `git diff`: +7 / −6.

| Điểm | Chỗ | Trước → sau (rút gọn; nguyên văn trong diff) |
|---|---|---|
| (a) | §10.6 | *"… registers; on two street frames, surface detail is AI-assisted — layout, landmarks and flags come from the sources. Historical images: public domain / CC0, credited."* → *"Narration: synthetic voice. Visuals: 3D reconstructions built from the cited sources and registers. In some shots AI repaints background surfaces only (terrain, water, sky, vegetation, textures); buildings, street layout, flags, ships, people, lights, text, dates and numbers come from the sources and are never AI-generated. Segments labelled "Illustration" are fully AI-generated and carry no location facts. Historical images: public domain / CC0 / CC BY, credited."* (ghi "viết lại theo N1/N2 §14.1; chủ dự án duyệt 20/10 22:34") |
| (a) kéo theo | §14.1 (f) | "(câu hiện hành ở §10.6 giữ tới khi chủ dự án duyệt bản viết lại)" → "(đã viết lại, chủ dự án duyệt 20/10 22:34)". **P thêm** chỗ này để câu (f) không lỗi thời; lệnh không nêu, chủ dự án xem lại |
| (b) | §11.3 Trần | "khung lai bão hoà trung vị ≤ 0,40 và chỉnh màu riêng" → "khung lai theo chuẩn chung §14.4 (bão hoà trung vị ≥ 0,40; sửa 20/10 22:34)" |
| (c) | §11.3 | "- Được dùng: (a) …" → "- Được dùng — VÍ DỤ của N1 (§14.1), không còn là danh sách đóng (sửa 20/10 22:34): (a) …" |
| (e) | §12.5 | "… dựng trọn bằng Cycles GPU — §14.2)" → "… — §14.2; chủ dự án xác nhận 20/10 22:34)" |
| (f) | §14.4 | thêm dòng "Thực vật mốc 9/1782 — hai ràng buộc có nguồn". (a) Sườn gần trơ, cây/bụi chủ yếu cọ lùn: Drinkwater 1786 tr. 49 *"The appearance of the rock is barren and forbidding ; as few trees or (hrubs, excepting palmettos, are to be feen on the face of the hill"*; Ancell 1784 tr. 40 *"Our barren rock yields but little"*. (b) Tông khô cuối mùa khô: Drinkwater 1786 tr. 50 *"nothing offers to the eye but fharp uncouth rocks, and dried palmetto bufhes."* Hướng bậc 2; hệ số 0,45 giữ TẠM bậc 5 |
| — | tiêu đề | "§14 + sửa 20/10)" → "§14 + sửa 20/10, 20/10 22:34)" |

**(d) "14 Times"** (KHÔNG sửa `loi-khoa.txt`; SHA `51d1c773…` trước = sau). Khuôn §14.5 = `<Nơi>: <lời hứa> | 3D Timelapse`, ≤ 60 ký tự; P **không tự đặt lời hứa**.

| Tệp | SHA trước → sau | Sửa |
|---|---|---|
| `phat-hanh/titles.txt` | `c708c1f9…` → `216e3dbb…` | THỬ 3 → `Gibraltar: <lời hứa> \| 3D Timelapse` (lời hứa chờ chốt) |
| `phat-hanh/PACKAGING-BRIEF.md` | `462e482d…` → `bfdeda02…` | bảng 1.1 dòng THỬ 3; §1.4 câu "dùng … làm CHÍNH" → câu khuôn §14.5 |
| `phat-hanh/nguon-mo-ta.md` | `cb3b1c2f…` → `1d21ae1f…` | tiêu đề tệp |
| `phat-hanh/nguon-mo-ta-v2.md` | `3851b9b1…` → `8ac50373…` | mục 3 "Nếu chốt THỬ 3"; câu dòng 1 cũ giữ "để tham khảo" |

Còn lại 0 chỗ "14 Times" trong `docs/` và `phat-hanh/`. **Ngoài phạm vi lệnh, chưa sửa:**
- `channel-k2/HANG-DOI.md`;
- `script-v4.1/v4.2-KHOA.md` (khoá);
- `g1b/episode.yaml`, `g1b/mk_ep_g1b.py`, `KHOA-LOI-BAO-CAO.md`;
- `v7p/*` (vùng V7C), `design/k2v/tl/scenes/t3s.js` (design/);
- các tệp chấm mù `g1/kiem-mu/**`.

## 3. Nhạc vào LFS — `reports/p2010b/nhac-tai.json`
Tải lại đúng URL của `reports/nhac-t3/nguon-moi.json`, UA trung tính. **SHA khớp đăng ký 8/8 → không phải DỪNG.** `assets/k2/music/`: `.gitattributes` (8 tên tệp, LFS), `SHA256SUMS` (`sha256sum -c` 8/8 OK). `tools/lfs-allow.txt` thêm 8 tên tệp và vùng `channel-k2/k2c-t3-01/am-thanh/master/*`; chủ dự án duyệt trong lệnh này, Kinh thánh §14.6.

| RIGHTS | Tệp | Byte | SHA-256 |
|---|---|---|---|
| K2-MUS-6 | sb_intervention_nomelody.mp3 | 10 340 546 | `decafaf069940c9e0038c54d707a7dd27903ec91e661c1b46dbbb705c44e934c` |
| K2-MUS-7 | sb_signaltonoise_nomelody.mp3 | 14 178 456 | `8e20b496b0614053565d4f43c80f469c84abd2aefb3ba01e29dfa813f49b9594` |
| K2-MUS-8 | Katabasis_I.mp3 | 23 591 705 | `bdce0cfde5f900a60b5c7f769261d0f8438a77e6e6bce351071de0c6d25d0f58` |
| K2-MUS-9 | Juggernaut.mp3 | 8 885 000 | `50be286d170f5a08791f1540b110fbbb4c0aa26e841084fceff0c908379e76f6` |
| K2-MUS-10 | sb_neverdying.mp3 | 16 076 978 | `4058afd709b398a4eaa38252dc47397ee00a67eb6a80553795deb211a1c9f4c2` |
| K2-MUS-11 | sb_undertow.mp3 | 10 000 906 | `4652007dad67295f1f5c87c8cbc8e2df1a530e7671266a29f693a084375d3910` |
| K2-MUS-12 | Echoes.mp3 | 14 557 747 | `d82b855a4a606f597820c8d7ff9719173189b8862f440480cb4cbd85b41a91d2` |
| K2-MUS-13 | sb_hiraeth.mp3 | 13 851 302 | `f790c7d53b8d802981ff7cdd8c59e22cdfe103ea66aba296c6cf1a65fe7fcf01` |

**Dung lượng LFS** (đo trên bản clone `--bare --filter=blob:limit=1k` của origin, cộng `size` của mọi con trỏ LFS duy nhất). Đã đẩy đủ: `git lfs push --all` báo 37/37 đối tượng có trên máy chủ.

| Phạm vi | Đối tượng | Dung lượng |
|---|---|---|
| `main` cũ `7fe4dcdf` (cả lịch sử) | 21 | 579,6 MB |
| Nhánh này = `main` mới | 42 | **878,8 MB** (+299,2 MB: master WAV 105,6 + FLAC 64,0 + 11 nguồn 18,0 + nhạc 111,5) |
| Toàn repo, 137 nhánh (gồm release-* có video master) | 94 | **11 803,9 MB** |

**CẢNH BÁO:** `main` vượt mốc 800 MB (+9,9 %); toàn repo ≈ 11,8 GB. Hạn mức lưu trữ/băng thông LFS của tài khoản GitHub cần chủ dự án kiểm (§8).

## 4. Sổ — `ghi_so.py`, COST-LEDGER bằng csv (kiểm 20 cột)
- **RIGHTS +1 dòng `DG3V2-AI`**, đọc thẳng từ `reports/dong-goi-t3-v2/ai/goi-api.jsonl` (chỉ 3 lệnh HTTP 200 của F1–F3).
  - Model `gpt-image-2.5-sunburst-2026-09-08` (model trả về đúng bản ghim), `POST /v1/images/edits`.
  - Ngày: F1 15:39:09Z, F2 15:40:02Z, F3 15:40:39Z (19/10). Ghi 2 lệnh nguyên văn: `pin1782` cho F1, F2; `pho2026` cho F3.
  - SHA vào → ra: F1 `0711a396…` → `1469cdc2…`; F2 `edf0262e…` → `c51bb6be…`; F3 `3fa32921…` → `429310c9…`.
  - C2PA có 3/3 (`APP11+jumb+c2pa`); chi phí $0,0761 / $0,0761 / $0,0756.
  - F2: 3 cờ Union được ghép lại điểm ảnh gốc. F4 LOẠI, không thuộc dòng này.
  - Giấy phép: câu §4.1 OpenAI Services Agreement, nguyên văn như dòng P1810B-AI. Phạm vi: thumbnail T3 theo §14.5 + cổng §14.1 (e).
- **RIGHTS sửa 16 chỗ:**
  - 8 dòng K2-MUS-6…13: "chờ chủ dự án duyệt mẫu" → "**chủ dự án duyệt mẫu 20/10 22:34**". Mẫu ghi công: `"<tên>" by Scott Buckley – released under CC-BY 4.0. www.scottbuckley.com.au (edited)`.
  - 8 dòng: "ngoài git, chưa vào `assets/`" → "`assets/k2/music/<tệp>` (LFS từ P-2010b 20/10; SHA khớp)".
- **AUTHORSHIP +4 dòng nguyên văn.** Các dòng P-2010 cùng sự kiện giữ nguyên; dòng mới ghi "bổ sung".
  1. 19/10 (trước 22:24): "Tôi chọn 1x,2x,3x,4x".
  2. 19/10 22:24: "Đồng ý Xác nhận 3 điểm của K-1.16.1 … Vẫn thiên về phương án nhạc free tránh rủi ro không đáng có". Dấu "…" có sẵn trong lệnh; phần lược không có trong repo.
  3. 19/10 23:21: "duyệt phiên thử NC-V2V".
  4. 20/10 22:34: "duyệt 8 điểm của phiên P-2010; Đã bật quyền History", kèm cách áp từng điểm.
- **COST-LEDGER +1** dòng `P-2010b`: Claude/OpenAI/YouTube 0; ElevenLabs 0 / 0; giờ máy 0,9 h; thời lượng 733,532 s. Cả tệp: 72 dòng × 20 cột.

## 5. Kiểm cuối
| Kiểm | Kết quả |
|---|---|
| `python3 -I checks/lock.py --verify` | **KHỚP** 1.16.1 `a3c39873751805a7a0a5e2b544bc2c28630d78e87725b777d3c7ba1c77cc2d2b` (mỗi commit qua preflight; trước và sau cập nhật main) |
| selftest (P chỉ chạy, không đọc mã) | `checks/ll/selftest_k116.py` **144/144** (23 nhóm) · `selftest_k115.py` **105/105** (15 nhóm) · `selftest_k114.py` **126/126** |
| `LOI-KHOA.sha256` | **3/3 OK** (`script-v4.2-KHOA.md`, `loi-khoa.txt`, `khoa-loi/phat-am/gibraltar-eric.pls`) |
| preflight `--range 7fe4dcdf..HEAD` | **ĐẠT** — 55 tệp, không cần trượt ngoại lệ nào |
| Email | 0 địa chỉ email trong diff `7fe4dcdf..HEAD`; không email trong header/URL/payload/UA |

## 6. main
- Trước: `main` = `origin/main` = **`7fe4dcdf`**. Kiểm lại ngay trước khi merge: `git fetch origin main` vẫn là `7fe4dcdf`, và `7fe4dcdf` là tổ tiên của nhánh.
- `git checkout main && git merge --ff-only p-2010b` → `main` = **commit cuối của nhánh** (commit chứa tệp này), fast-forward. `lock.py --verify` trên main: KHỚP. `git push origin main`, không force.

## 7. Chỉ số trong ±5 % quanh ngưỡng (và vượt mốc)
| Chỉ số | Số đo | Ngưỡng/mốc | Lệch |
|---|---|---|---|
| Bộ đếm ElevenLabs trước/sau | 141 009 / 141 009 | phải bằng 141 009 | 0 (đạt) |
| Thời lượng master | 733,532 s | = 733,532 s; ±0,05 s mỗi chương | 0,000 s; chương ≤ 0,004 s (làm tròn sổ KL42) |
| Loudness master (giữ nguyên KL42, trùng bit) | −14,1 LUFS | dải −15,0…−13,8 | cách cận trên 0,3 LU (**2,2 %**) |
| Dung lượng LFS `main` | 878,8 MB | mốc cảnh báo 800 MB | **+9,9 % (VƯỢT)** |
| Giờ máy | ≈ 0,9 h | mốc 1,5 h | −40 % (ngoài ±5 %) |

Không thêm phần tử nào để vượt ngưỡng.

## 8. Việc chờ chủ dự án
1. **LFS:** `main` 878,8 MB (> 800 MB), toàn repo ≈ 11,8 GB. Cần kiểm hạn mức LFS GitHub; quyết có dọn LFS ở các nhánh release-* cũ / giữ cả WAV lẫn FLAC master hay chỉ FLAC.
2. **Master giọng T3** đã khôi phục trùng bit KL42 và nằm ở LFS. Giọng G1 vẫn **chưa được dùng cho bản phát hành** tới khi ElevenLabs trả lời thư Đ5 (RIGHTS P1910-G1).
3. **Lời hứa tiêu đề THỬ 3** theo khuôn §14.5. Các tiêu đề CHÍNH/THỬ 2 "14 Sieges in 3D" trong `titles.txt` đúng kiểu §14.5 cấm (khi chỉ dựng 2 cuộc vây): giữ hay thay. Những chỗ "14 Times" ngoài phạm vi (§2 cuối) có sửa không, và giao ai (`HANG-DOI.md`: P; `v7p/`, `t3s.js`: phiên dựng).
4. **Câu minh bạch mới §10.6** chưa vào bản nháp mô tả. `phat-hanh/nguon-mo-ta.md`, `nguon-mo-ta-v2.md`, `the-phuong-phap*.json` còn câu cũ "two street frames" (ngoài phạm vi lệnh). Duyệt giao P/ĐÓNG-GÓI cập nhật.
5. Xác nhận sửa kéo theo **§14.1 (f)** (P thêm, §2).
6. Chọn ứng viên thumbnail (RIGHTS DG3V2-AI đã ghi phạm vi theo §14.5).
7. Còn từ P-2010 §9: giao phiên K V2V-D4 (bộ đo bịa vào `checks/`) trước M2; NC-V2V3 và V7C chờ xong để merge.

## 9. Tệp (`reports/p2010b/`)
- `P2010B-BAO-CAO.md` (tệp này), `CHECKPOINT.md`.
- Giọng: `lich-su-g1-1910.json` (đầu ra `reports/p2010/giong_lich_su.py`, dời sang đây), `tai_lich_su.py` + `lich-su-tai.json`, `kiem_chu.py` + `kiem-chu.json`, `ghep_lai.py` + `ghep-lai.json`, `do_khe.py`, `xuat_lai.py` + `xuat-lai.json`, `so_xem.py` + `so-xem.json`, `asr_wer.py` + `wer_chuan.py` + `asr-wer.json`.
- Kinh thánh: `sua_bible.py` + `sua-bible.json`.
- Nhạc: `nhac-tai.json`.
- Sổ: `ghi_so.py`.

**DỪNG — chờ chủ dự án.**
