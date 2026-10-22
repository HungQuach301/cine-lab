Nhánh thật: **`k2c-t3-anim-v2`** (đúng tên lệnh), tạo từ `origin/ccr-d189108f-6mcz9k` @`41e0c8fd` (ANIMATIC-T3). Không merge, không đụng `main`/nhánh khác.

# ANIMATIC-T3-V2 — Gibraltar: vòng sửa animatic theo nhận xét chủ dự án + minh hoạ Omni (N2). BÁO CÁO. DỪNG chờ chủ dự án

## §0 Điều lệ phiên và tóm tắt

```text
ĐIỀU LỆ                                   | thực tế
Vùng sửa                                   | design/k2v/** (tl/nc/up.js, tl/life.js), scripts/k2tl/**, channel-k2/k2c-t3-01/animatic/**, reports/animatic-t3-v2/**
KHÔNG sửa                                  | loi-khoa.txt, LOI-KHOA.sha256, khoa-loi/**, am-thanh/**, assets/, LOOK-KHOA.md, checks/, docs/, sổ, main — đúng (scripts/k2/** không cần sửa)
Lời khoá / thời lượng câu                  | GIỮ NGUYÊN (phương án B 745,0 s; tiếng v2 trùng BIT v1: mix.wav SHA 805432b5…); 5 thẻ chương giữ nguyên chữ
LOCK checks                                | lock.py --verify KHỚP a3c39873… (chỉ chạy, không đọc mã checks/)
GPU / ElevenLabs / RunPod / YouTube         | 0 / 0 ký tự (prep chặn mạng) / 0 / 0
Khoá / email                               | proxy gắn khoá; mã không đọc/in/ghi khoá; 0 email trong diff (preflight ĐẠT mọi commit, trừ 1 sự cố §10); UA "CineLab-research (+https://github.com/HungQuach301/cine-lab)"
Dừng tiến trình                            | theo PID/PGID (1 lần sai — §10)
CHECKPOINT                                 | reports/animatic-t3-v2/CHECKPOINT.md, tự đẩy mỗi 25 phút (anim_ckpt.sh tham số hoá BR/ANIM_CK)
```

| Việc | Kết quả |
|---|---|
| 1. H1 mở đầu | Ban ngày 15:00 → (M5 nắng chiều 17:30–18:20) → hoàng hôn → đêm 23:52, cùng điểm máy D7 trôi rất chậm; Rock nguyên khối trong ánh ngày 0–4,5 s; đèn phố/đường băng bật dần; tổng 12,0 s; H2 nối 23:53. Pin nổi cháy giữ ở 0:28 (trước 0:33) |
| 2. Eo đất R1–R4 | Sửa N1.4, N1.5, N1.6, C1, N2.10, N2.7, N2.11 (+ C2 giữ) và **quét cả phim bằng mặt nạ ID 1 khung/s** → sửa thêm N3.1, N3.2, N3.3, N3.4, N3.5, N4.1, N4.2. Cỏ/cát trống: ch1 **10,8 % → 3,1 %**, ch3 **11,2 % → 0 %**, đoạn liên tục dài nhất **14,0 s → 4,0 s** (§8) |
| 3. C4 + N5.4 | C4: máy thấp chéo từ vịnh (45–52 m) thấy tàu + Old Mole + phố + Rock; M1 trượt → giữa shot là 3D góc thấp gần bến. N5.4: khung lai thấp có chân trời, cây/đèn/xe phố 2026, nhìn bắc từ đường băng qua cổng + góc hàng rào |
| 4. Nước | `nc/up.js`: bờ theo đúng các mốc đất lấn có trong years.png (0 · 1941 · 1987 · 2026) + ô đất lấn chưa nổi ở năm khung = nước sâu. **Hết mảng xanh nhạt** ở N4.3, N4.4, N5.5 (tờ so `to-so/to-so-N4_3.jpg`) |
| 5. Omni M1–M5 | `gemini-omni-1.1-flash` image-to-video (ảnh đầu = render của chính shot). **4/5 đạt kiểm** (M2 l3, M3 l1, M4 l1, M5 l3); **M1 trượt 3 lượt → giữ 3D**. 11 lượt, Gemini **$11,25**. Tổng minh hoạ trong phim **28,4 s = 3,7 %** (≤ 20 %) |
| 6. Dựng lại | Nướng lại 7 lightmap (tệp ngoài git v1 đã mất theo container) + dựng lại **43/43 cảnh** (mọi dấu cảnh đổi do sửa `tl/*.js`) + 5 cảnh dựng lần 2 sau soát; master v2 **761,000 s**, −14,0 LUFS, −1,3 dBTP |
| 7. Xuất | 8 tệp xem 640×360 (4,69–4,85 MB) `xem/`, tờ khung `to-khung.jpg`, tờ so 21 shot + tờ M1–M5 `to-so/`, `PHIEU-XEM-V2.md`; master ngoài git SHA `a9a35a12…` |
| 8. Tự đo | §8. XEM CÂM AI (tham khảo): P đọc lại **37/48** (v1: 31/48); Q8 0 → 5/6, Q3 3 → 6/6. k2check 1.16.1 `--cap`: TRƯỢT (§8.4) |
| Giờ máy / chi phí | ≈ **13,4 h** đồng hồ (14:20 → 03:45 UTC; mốc 14 h) · Gemini $11,25 · Claude ≈ $4,66 · OpenAI $0,83 (§9) |

**Xem nhanh:** `reports/animatic-t3-v2/PHIEU-XEM-V2.md` → tệp `reports/animatic-t3-v2/xem/01…08`; tờ so `reports/animatic-t3-v2/to-so/`.

## §1 H1 mở đầu ban ngày → đêm (việc 1)
- Thời gian: 19/10/2026 15:00 (0 s) → 17:30 (4,5 s) → [M5 17:30–18:20] → 18:20 (10,5 s) → 19:45 (11,2 s) → 23:52 (12,0 s). Máy D7 (lùi bắc 650 m, nhìn xuống ≈ 14°) trôi rất chậm; góc giữa (4,5–10,5 s) là máy tầm thấp trên đường Winston Churchill qua đường băng = ảnh đầu M5.
- Ban đầu đặt M5 ở 19:50–21:40 (chạng vạng/đêm); Omni lượt đạt (M5 l3) cho **nắng chiều** → chuyển M5 sang 17:30–18:20 để hình và bộ đếm liền mạch; hoàng hôn → đêm dồn vào 10,5 → 12 s (1,5 s timelapse nhanh).
- H2 mở 23:53 → 00:20 đêm rồi bước năm 14 lần vây như v1. Pin nổi cháy H2T ở 0:28–0:33.
- Lời 0a "Midnight at the Gibraltar frontier" (0–2,15 s) nay nói trên hình ban ngày — theo yêu cầu chủ dự án (timelapse từ ngày tới nửa đêm); ghi để chủ dự án xem lại (đề xuất V2-D3).

## §2 Eo đất R1–R4 — danh sách shot đổi + lý do (giây cắt góc là giây trong shot)
| Shot | Trước (ANIMATIC-T3) | Sau (v2) | Luật |
|---|---|---|---|
| N1.4 (14 s) | 1 góc 160 m, dòng người không thấy | 3 góc: máy 7 m sát dòng 1 400 người (đi cùng chiều về bắc, `life.js dir`) → **M3** 3,5–11,5 s → 30 m dòng người thưa dần (21–26/8) | R1 |
| N1.5 (29,1 s) | eo đất trống 1713 → 2015 (25 s cỏ) | 3 góc: cảng 7/1713 (tàu buôn + thuyền nhỏ, minh hoạ bậc 5) → phố + lâu đài + Line Wall từ vịnh (ống dài) → eo đất từ mép bắc Rock trống ≤ 4 s rồi 2015 đúng chữ "in 2015" | R4 + R3 |
| N1.6 (25,5 s) | 1 góc 480 m, Línea nhỏ | 3 góc: vách bắc + khói vây 1704–05/1727 (khói to hơn, vị trí minh hoạ bậc 5) → Línea mọc tiền cảnh + Rock (60 m, ống dài) → 2026 La Línea (110 m) đúng chữ "still called La Línea" | R1 + R3 |
| C1 (22,5 s) | A3 1 km + U1 | 2 góc: Línea + đồn (đường bộ bị cắt 20–22/6, ngày–đêm) → dải trại mọc dần 13/7 → 28/10 nhìn nam về Rock | R1 + R3 |
| N2.10 (18,4 s) | 326 m | 2 góc 75–95 m trước vách bắc: bụi đào → nổ lỗ thông hơi | R1 + R3 |
| N2.7 (14,4 s) | 320 m | 48 m cách công sự ≈ 500 m; **sửa lỗi cũ**: `fires` ghi [E, 6, N] → quầng lửa lơ lửng cao 190–455 m trên trời | R1 |
| N2.11 (27,6 s) | đỉnh Rock 700 m | 3 góc: công sự + Rock (đông 1782) → cận khẩu đội phát súng cuối 5/2/1783 → dải trại rút (hết ngay trước cuối shot) | R1 + R3 |
| N3.1 (27,3 s) | 700 m từ biển đông | 2 góc thấp: đồn San Felipe + Línea → đồn Santa Bárbara nổ 14/2/1810 | R2 + R3 |
| N3.2 (8,5 s) | eo đất trống | phố + cảng từ vịnh 1810 → 1860 | R4 |
| N3.3 (10 s) | 430 m, 58 % cỏ | hạ 120 m nhìn về La Línea + Rock (47–49 % cỏ — **sát ngưỡng**) | R2 |
| N3.4 (27 s) | 1 góc, 21 s cỏ > 50 % (đo sau sửa lần 1) | 2 góc: mép nam La Línea 1900 + Rock → dọc hàng rào 1909 nhìn về Rock | R2 + R3 |
| N3.5, N4.1, N4.2 | 380–650 m | hạ 40–75 m; N4.1/N4.2 chia 2 góc (đường băng từ vịnh → vách bắc bụi đá) | R2 + R3 |
| C2 | — | giữ (mặt nước + hàng chặn; R1 nói về chủ thể trên eo đất) | — |

Mọi vật mới đều có nguồn/bậc như ANIMATIC-T3 (dòng người, tàu buôn 1713, khói vây: số/vị trí minh hoạ bậc 5, ghi trong `log-shot.json`); không thêm vật không nguồn để lấp chỗ trống — chỗ thiếu nội dung có nguồn đã đổi góc theo R4 (N1.5, N3.2).

**Soát dựng bắt lỗi và dựng lại (5 cảnh):** N5.4 góc thấp đầu có bãi cỏ công viên chiếm nửa khung → nhìn bắc từ đường băng; N1.4 góc cuối hết người (tắt sớm) → lùi mốc thưa dần; C1 góc cận trại không thấy lều (7–9/1779) → gộp; N1.5 góc lâu đài K-co ở 1713 lỗi hình (tường trong suốt, bụi lơ lửng) → nhìn từ vịnh; N1.6 máy 22 m làm ô đất gần máy biến mất (nước + bụi lơ lửng, thấy ở soát master) → 60 m ống dài.

## §3 C4 và N5.4 (việc 3)
- **C4:** 0–2 s và 9–13,5 s máy thấp chéo 45–52 m từ vịnh (tàu tiền cảnh, Old Mole, phố, Rock); 2–9 s (chỗ M1) giữ 3D góc thấp ≈ 500 m nhìn bến (thuyền cập). Vân CC0 tường/đá đã có trong cách A (`seaworn_sandstone_brick`). **Hạn chế:** phần giữa 3D vẫn thưa (tường + mặt nước, thuyền nhỏ) — chỗ yếu còn lại của chương 2a.
- **N5.4:** khung lai thấp 35–40 m có chân trời; `pho2026` (cây, đèn, xe đỗ dọc đường OSM, bậc 5 vật nền phụ); 2 góc: đường băng → cổng → La Línea · dọc hàng rào (gỡ cũ, dựng mới lệch 6 m).

## §4 Nước (việc 4)
Nguyên nhân đo được: years.png chỉ có các mốc đất 0 · 1941 · 1987 · **2026** (mọi đất lấn hiện đại mã 2026); shader nước v1 dùng bờ năm 2026 cho mọi năm ≥ 1942,5 → đất 1987/2026 chưa nổi bị tính là "bờ" → bọt + màu nông = mảng xanh nhạt phẳng. Sửa: 5 bờ theo mốc (1790/1940/1941/1987/2026, chọn theo năm khung) + kiểm từng điểm ảnh bằng `landKx` (đường băng 1941 đang mọc theo uRecl). Tờ so N4.3/N4.4/N5.5: hết mảng.

## §5 Minh hoạ Omni (việc 5)
**Tài liệu đọc 21/10/2026:** <https://ai.google.dev/gemini-api/docs/omni> (*Last updated 2026-09-23 UTC*): model **`gemini-omni-1.1-flash`** (duy nhất trong trang; `GET /v1beta/models` còn `gemini-omni-flash-preview`), **có image-to-video** (`generation_config.video_config.task = "image_to_video"`, ảnh = khung đầu; hai ảnh = khung đầu/cuối), 360p/720p, 1080p/4K là phóng, không ghi trần độ dài (thực tế mỗi lượt 10,0 s 1280×720 24 fps), *"All generated videos include SynthID watermarking"*; EEA chỉ cấm sửa/nối video **tải lên**. <https://ai.google.dev/gemini-api/docs/pricing> (*Last updated 2026-10-19 UTC*): vào $1,50/1M, ra video $17,50/1M, *"5,792 tokens per second of 720p video"* ≈ $0,10/s.

**Cách làm:** ảnh đầu = khung render 1280×720 (cách A, spp 8; **không lightmap** vì lúc đó chưa nướng xong — khác nhẹ về bóng so với khung 3D cuối) của chính shot ở máy tầm người/≤ 40 m; lệnh = mô tả riêng + luật chung (`omni/lenh/CHUNG.txt`, `CHUNG-2026.txt`); kiểm mỗi lượt bằng `ma/kiem_minh_hoa.py`: 3 khung (25/55/90 %) × 2 mô hình nhìn (gpt-6.1-sol, claude-sonnet-5-5, đề bài + 5 ảnh phóng của NC-N2P) + `checks/ll/q_thoi_dai.py` (K). Máy kết luận LOẠI khi: lỗi thời đại có năm > năm khung; cờ/công trình nhận ra được/tàu lớn/chữ MỚI so với ảnh đầu; thi thể/máu/người trong lửa. Chèn bằng `scripts/k2tl/anim_minh_hoa.py`: cắt vào theo góc/nhịp lời, khớp màu Lab k = 0,7 về khung 3D quanh đoạn, hoà 0,5 s về 3D ở cuối, nhãn **"Illustration"** góc dưới phải suốt đoạn, bộ đếm chạy tiếp.

| Lượt | Lệnh thêm | Kiểm máy | Lỗi chính | $ | Giữ/loại |
|---|---|---|---|---|---|
| M3-l1 | — | ĐẠT (0 lỗi, q_thoi_dai 0) | nghi vấn: "khung lưới mờ ở chân trời phải" (claude 0,35) | 1,02 | **GIỮ** (0 → 8 s) |
| M2-l1 | — | LOẠI (17) | tàu buồm, tháp chuông, đê/cầu cảng, khu nhà trắng bịa ở vịnh | 1,03 | loại → đổi ảnh đầu nhìn LÊN sườn đá |
| M2-l2 | `M2-them-l2.txt` | LOẠI (1) | gpt: nét giống chữ/watermark trên bụi cọ (0,76) | 1,02 | loại |
| M2-l3 | `M2-them-l3.txt` | ĐẠT | nghi vấn: khói xa (đúng lệnh) | 1,02 | **GIỮ** (bỏ 1 s đầu) |
| M4-l1 | — | ĐẠT | nghi vấn: lâu đài trên đồi, đèn lồng tường (≤ 0,6) | 1,02 | **GIỮ** (bỏ 2 s đầu: Omni giữ khung render rồi tự cắt cảnh) |
| M1-l1 | — | LOẠI (2) | tàu có cột buồm mép trái | 1,02 | loại |
| M1-l2 | `M1-them-l2.txt` | LOẠI (6) | cờ trên cột (bastion), chòi gác | 1,03 | loại |
| M1-l3 | `M1-them-l3.txt` | LOẠI (1) | cọc buộc tàu sắt "≈ 1800" (gpt 0,73) | 1,02 | loại → **giữ 3D** (hết 3 lượt) |
| M5-l1 | — | LOẠI (15) | logo giày, biển vàng sân bay, logo đuôi máy bay | 1,02 | loại |
| M5-l2 | `M5-them-l2.txt` | LOẠI (1) | chữ/logo trên thân máy bay (claude 0,6) | 1,02 | loại |
| M5-l3 | `M5-them-l3.txt` | ĐẠT | nghi vấn: máy bay xa (đúng lệnh) | 1,02 | **GIỮ** (0 → 6 s) |

- Mọi đầu ra có C2PA `trainedAlgorithmicMedia` + SynthID trong manifest (mã hoá lại khi chèn làm mất C2PA; SynthID trong điểm ảnh theo tài liệu). Sổ AI K-LAI: `so-ai-gemini.jsonl` (model, ngày, lệnh nguyên văn, SHA vào/ra, usage, giá, C2PA/SynthID); chi phí soi: `cost.jsonl`; kết quả: `omni/kiem/<lượt>/<lượt>-kiem.json`; bản xem 640×360 mọi lượt: `omni/xem/`; video gốc 1280×720 (> 5 MB) ngoài git `/var/tmp/cine-out/omni-goc/` (SHA trong sổ).
- **Người đọc tờ so (P):** `to-so/to-so-minh-hoa.jpg`. M2/M3/M4 đúng thời kỳ, không cờ/chữ; M4 có nhiều mái cháy hơn "4–5 nhà" (S063) — là minh hoạ, dữ kiện do lời; M5 nắng chiều, máy bay xa không dấu. **Tỷ lệ làm lại đo được:** 11 lượt cho 5 đoạn; 4/5 đạt ≤ 3 lượt (M3, M4 lượt 1; M2, M5 lượt 3); M1 0/3.
- **Vị trí trong phim:** M5 0:04,5–0:10,5 · M3 1:48,0–1:56,0 · M2 3:27,6–3:35,6 · M4 4:01,3–4:07,7 (+ M1 giữ 3D 3:43,7–3:50,7). Tổng chèn 28,4 s = **3,7 %** thời lượng (≤ 20 %; dưới mức ≈ 7–8 % dự kiến vì M1 trượt).

## §6 Dựng lại + giờ máy (việc 6)
- Tệp ngoài git của ANIMATIC-T3 (master v1, lightmap, cảnh đinh, bộ đệm) **không còn** trong container mới (BAI-HOC #117) → dựng lại bộ đệm (`v7p_cache.sh` + 3 bước), nướng 7 lightmap **19 467 s ≈ 5,4 h** (b2026 2 353 · b1704 2 138 · b1779 1 856 · b1782 4 087 · b1781r 2 242 · b1940 2 885 · b1900 2 506 s; meta `do/nuong-*.json`).
- **Cảnh dựng lại: 43/43** (lý do: sửa `tl/nc/up.js` + `tl/life.js` → dấu cảnh băm cả `design/k2v/tl` đổi cho mọi cảnh, như AT-D6) + **5 cảnh lần 2** sau soát (§2). 48 lượt cảnh, 21 432 khung, **19,5 h tiến trình**; P = 2 khi nướng (OOM khi P = 3 + Blender), P = 3 sau đó. Render đoạn + ghép 2 lượt ≈ 1,7 h.
- **Giờ máy thật ≈ 13,4 h đồng hồ** (14:20 → 03:45 UTC), gồm nướng chồng dựng.
- Master v2: `/var/tmp/cine-out/k2c-t3-anim/k2c-t3-anim-v2-master.mp4` 960×540 24 fps **761,000 s**, 757,0 MB, SHA-256 `a9a35a128225bbf0ab8cce3de3a361e16dc95002170235ef6fd574465ff59b74`. Tiếng = mix.wav v1 trùng bit (`805432b5…`): giọng G1 LFS `ba50fba7…` + nhạc B (8/8 SHA khớp sau `git lfs pull`), −14,0 LUFS, −1,3 dBTP sau AAC, SMR p10 19,7 dB.
- **Tái tạo:** `v7p_cache.sh` → `v7b_mau_nha.py` → `v7b_faden.py` → `anim_tex.py` → `NUONG_META=reports/animatic-t3-v2/do anim_nuong.sh` → `mk_ep_anim.py` → `K2_DRAFT=1 MW=960 build.sh …/animatic/episode.yaml prep` (chặn mạng) → `anim_vong2.sh` → `anim_lan.py` → `anim_minh_hoa.py` (cần `omni/chon/*.mp4` ngoài git) → `anim_mix.py` → `build.sh … render ghep`.

## §7 Tệp cho chủ dự án (việc 7) — SHA đầy đủ `do/sha-xem.txt`
| Tệp | Cỡ | SHA-256 (16 ký tự đầu) |
|---|---|---|
| `xem/01-mo-dau.mp4` (0:00–0:43,8) | 4,69 MB | `19f88f7f359c502f` |
| `xem/02-ch1-rock-1704.mp4` (0:43,8–2:53,1) | 4,81 MB | `1d2c9ae5f2e1600e` |
| `xem/03-ch2a-vay-ham.mp4` (2:53,1–4:22,2) | 4,78 MB | `fb9ff1c2e0eb3ba8` |
| `xem/04-ch2b-tan-cong-1782.mp4` (4:22,2–6:22,6) | 4,85 MB | `28ae3def3f27bddc` |
| `xem/05-ch3-dat-trung-lap.mp4` (6:22,6–7:51,6) | 4,78 MB | `891946c6dfb9662d` |
| `xem/06-ch4-duong-bang.mp4` (7:51,6–9:45,8) | 4,77 MB | `4136b7099ca327f0` |
| `xem/07-ch5a-cong.mp4` (9:45,8–11:06,1) | 4,79 MB | `e95691276ab926b8` |
| `xem/08-ch5b-ket.mp4` (11:06,1–12:41,0) | 4,78 MB | `4eefbbf1061235db` |
| `to-khung.jpg` (1 khung/shot) | 0,87 MB | `78700eb207305081` |
| `to-so/to-so-<shot>.jpg` × 21 + `to-so-minh-hoa.jpg` | 4,3 MB | TRƯỚC = tệp xem v1 640×360 (master v1 đã mất) |
| Master v2 960×540 (ngoài git) | 757,0 MB | `a9a35a128225bbf0` |

Cả 8 chương đều có shot đổi (nước đổi ở mọi năm < 2026, N5.x đổi máy) nên xuất đủ 8 tệp, cùng tên/thứ tự ANIMATIC-T3.

## §8 Tự đo (ghi số, KHÔNG tự chấm đạt)
### 8.1 R2 — cỏ/cát trống (mặt nạ ID `idmask_v7c`, lớp `bang` > 50 % khung, 1 khung/s; `scripts/k2tl/v2_do_r2.py`; số thô `do/r2-truoc.json`, `do/r2-sau.json`)
| Chương | Trước (s · %) | Sau (s · %) |
|---|---|---|
| 0 móc | 0 · 0 % | 0 · 0 % |
| 1 Rock 1704 | 14,0 · **10,8 %** | 4,0 · 3,1 % |
| 2 vây hãm | 7,0 · 3,3 % | 7,1 · 3,4 % |
| 3 đất trung lập | 10,0 · **11,2 %** | 0 · 0 % |
| 4 đường băng | 0 | 0 |
| 5 cổng | 0 | 0 |
| **Liên tục dài nhất** | **14,0 s** (N1.4) | **4,0 s** (N1.5, eo đất 1729 trước 2015) |

**Giới hạn của thước:** khung "eo đất trống" mà chủ dự án thấy (v1 N1.5, N1.6) có cỏ 25–45 % + trời 40 % nên KHÔNG vượt 50 % → thước R2 bắt thiếu. Bổ sung `bang` TB theo shot (trước → sau): N1.4 62 → 22 %, N1.6 26 → 19 %, C1 51 → 44 %, N2.7 46 → 41 %, N3.3 58 → 48 %, N3.4 38 → 39 %, N5.4 18 → 2 %. **Nhìn bằng mắt chương 3 vẫn nhiều cỏ** (N3.1, N3.3, N3.4 góc 2 dưới ngưỡng nhưng 40–49 %).

### 8.2 R3 / R1
- Shot > 15 s: **22 → 22** (thời lượng câu giữ nguyên); **đoạn liền một góc > 15 s: 22 → 17** (sau cắt góc + đoạn minh hoạ). Bắt buộc R3: N1.5 (3 góc), N1.6 (3), C1 (2), N2.11 (3) — đã chia; N2.10 chia 2.
- R1 % chủ thể (pixel mặt nạ: người, trại, công sự, nhà, phố, lửa, tàu, cờ; TB shot, trước → sau): N1.4 0,8 → 10,4 · N1.5 3,6 → 17,4 · N1.6 1,2 → 15,7 · C1 6,3 → 3,7 · N2.10 3,0 → 3,7 (+ vách đá 7,5 → 16,0) · N2.7 3,9 → 11,6 · N2.11 1,4 → 9,2. **Chỉ N1.5, N1.6 đạt 15–20 % theo pixel**; người/lều/tuyến tường mảnh nên pixel thấp dù chủ thể chiếm vùng lớn — chưa đo vùng nở (đề xuất V2-D2). C1 giảm vì gộp góc cận trại (lều không đọc được ở cận).
- % thời lượng minh hoạ AI: **3,7 %** (28,4 s; ≤ 20 %).
- Kết quả bộ kiểm từng lượt Omni: §5.

### 8.3 Tự đo master (`do/so-do.json`)
| Chỉ số | v1 | v2 |
|---|---|---|
| Thời lượng | 761,000 | 761,000 |
| LUFS · LRA · đỉnh thật | −14,0 · 3,1 · −1,3 | −14,0 · 3,1 · −1,3 |
| Cắt/phút: shot · tính bước năm | 3,46 · 5,96 | 3,46 · 6,20 (k2check video: **5,40** cắt/phút, 68 cắt) |
| % góc cao có tl · lướt thấp | 82,5 · 8,1 | 80,6 · 8,5 (k2check TL-2: 4,8 %) |
| Bão hoà trung vị | 0,400 | **0,388** (< 0,40 — §10) |
| Colorfulness · chi tiết | 67,6 · 13,63 | 71,8 · 16,81 |

### 8.4 k2check 1.16.1 `--cap` (LOCK KHỚP) — `do/k2check-1.16.1.txt` — tập TRƯỢT
ĐẠT: Q26b, Q32, Q34, Q35, Q36, ML2, ML3, FT1, NC-H2…H5, BD, K-R, **K-LAI-1…6 ("tập không có khối lai / shot AI" — K chưa đọc `minh_hoa` trong log-shot; xem V2-D5)**, CHUONG-1, TL-2 (4,8 %), NHIP-NGHIA (71/71), PC-1, LOCK. CẢNH BÁO: Q26b-K2, O2, PP-1, **TL-1 (95,2 % góc cao; video 5,40 cắt/phút > 5 — do R3)**, TL-3 (thiếu `trong_pct`). TRƯỢT: Q33/Q33-K2 (anim_N2_8/anim_C3 lặp > 2 theo pHash), Q37/NHIP-K2 (TB 5,21 s/biến cố, dài nhất 12,7 s), ML1 (41/45 shot gắn câu — như v1), NC-H1 (khai lớp nhà — như v1), SACH-1 (không log chữ — như v1), XEM-CAM (chờ chủ dự án). A1–A13: CHỈ BÁO.

### 8.5 XEM CÂM 3 AI — CHỈ THAM KHẢO (`xem-cam/ket-qua.json`, claude-sonnet-5-5, 190 khung không tiếng không phụ đề, $0,40)
| Câu | v1 P đọc | v2 từ khoá | **v2 P đọc** |
|---|---|---|---|
| Q1 ai giữ Rock sau 1704 | 6 | 6 | 6 |
| Q2 1779 bắt đầu gì | 6 | 6 | 6 |
| Q3 vì sao đói | 3 | 6 | **6** (cả 3 nêu phong toả + cận người hái rau) |
| Q4 cái gì đến cứu | 4 | 4 | 2 (rào "not sure": không rõ tàu ta/địch) |
| Q5 biển 9/1782 | 5 | 6 | 6 |
| Q6 xây gì trên eo cát | 6 | 6 | 6 |
| Q7 cổng 1969 và sau đó | 1 | 0 | 0 |
| Q8 cái gì nối hai phố hôm nay | 0 | 6 | **5** (người kéo vali băng qua đường băng — M5) |
| **Tổng** | **31/48** | 40/48 | **37/48** · độ rõ 2,67/5 |
Lạc chung: mở đầu nhảy năm 2026 → 1411 → 1782; 1729 → 2015 chưa rõ ý; 1969 không thấy cổng/người dừng; người hái rau "không nói rõ là đói"; M4 phố cháy "không rõ ai bắn".

## §9 Chi phí thật
| Khoản | Mốc / chặn | Thật |
|---|---|---|
| Gemini (Omni, 11 lượt × ≈ $1,02) | $15 / dừng $20 | **$11,25** (sổ `so-ai-gemini.jsonl`; không 402) |
| Claude (bộ soi 2 mô hình $3,35 + q_thoi_dai K $0,92 + xem câm $0,40) | $10 / $30 | **≈ $4,66** (`cost.jsonl`, qtd json, `xem-cam/cost.jsonl`). Token của chính phiên không đo được trong container |
| OpenAI (gpt-6.1-sol soi) | $5 / $15 | **$0,83** |
| ElevenLabs / RunPod / YouTube | 0 | 0 ký tự / 0 / 0 |
| Giờ máy | 14 h | **≈ 13,4 h** |
Không lỗi nào lặp ≥ 3 lần. Không chặn an toàn nào kích hoạt.

## §10 Sự cố + chỉ số trong ±5 % quanh ngưỡng
- **Commit lọt 9 video > 5 MB** (`omni/ra|chon/*.mp4`): preflight báo TRƯỢT nhưng `… | tail -1 &&` không chặn → sửa commit trên nhánh của phiên (amend + force-with-lease), video gốc ra ngoài git + `.gitignore`; từ đó kiểm chữ "— ĐẠT" trước commit.
- **3 vòng dựng chạy chồng** (PID ghi từ `$!` của `setsid` là tiến trình đã thoát → tác vụ chờ khởi động thêm vòng) → dừng theo PGID, thống nhất 1 vòng `anim_vong2.sh` (P đọc từ tệp).
- **OOM** khi 3 trình duyệt dựng + Blender nướng (cgroup giết chrome) → P = 2 khi nướng.
- Chú thích chèn giữa dòng nuốt mã (BAI-HOC #42) **2 lần** trong `mk_ep_anim.py` (đều lỗi cú pháp, bắt ngay). Thiếu `imageio` cho /opt/bpy, thiếu `origin/v5a` (LUT), LFS giọng/nhạc chưa kéo → đã xử lý.
- Đĩa còn < 3 GB ở bước cuối build (bước tách phần dừng sau khi master đã ghép xong) → xoá tệp trung gian nướng.
- **Chỉ số sát ngưỡng (±5 %):** bão hoà trung vị **0,388** (ngưỡng ≥ 0,40: −3 %, **dưới ngưỡng**); N3.3 cỏ 47–49 % (ngưỡng 50 %); N1.6 góc 2 cỏ 33–41 %; C1 cỏ 43–58 % theo khung (2 đoạn 3 s > 50 %); thẻ chương 3,00 s = trần; loudness −14,0 LUFS (dải −15…−13,8). Ngoài ±5 %: TL-1 video 5,40 cắt/phút (> 5, +8 %).

## §11 Quyết định đề xuất
| # | Đề xuất | Ưu | Nhược | Tác động | Rủi ro |
|---|---|---|---|---|---|
| V2-D1 | **Bão hoà 0,388 → ≥ 0,40**: tăng vibrance cảnh tl 0,78 → 0,82 hoặc khớp màu minh hoạ k 0,7 → 0,85 | về lại LOOK-1 | sửa `t3tl.js` GRADE → dựng lại cả tập (dấu băm) — gộp vào lượt dựng bản cuối 1080p | toàn phim | màu cỏ chói hơn |
| V2-D2 | **Thước R1**: đo "vùng chủ thể" bằng mặt nạ nở (≈ 1,5 % bề ngang) bên cạnh pixel thô; chốt định nghĩa 15–20 % theo thước nào | số khớp cảm nhận | phải chốt với K | R1 eo đất | — |
| V2-D3 | **Lời 0a "Midnight…" trên hình ban ngày**: giữ (theo yêu cầu) hoặc dời ban ngày → 0–2 s đêm trước | nhận ra Rock trong nắng | lệch chữ "Midnight" ↔ hình | 12 s mở đầu | — |
| V2-D4 | **M1**: chấp nhận bản 3D góc thấp gần bến, hoặc thử lượt 4–6 với ảnh đầu không tường/không mặt nước sát (cần chủ dự án nới trần 3 lượt) | M1 là đoạn "dỡ hàng" chủ dự án muốn | thêm ≈ $3 + kiểm | C4 2–9 s | Omni hay bịa cờ/cọc sắt ở bến |
| V2-D5 | **K-LAI chưa thấy đoạn minh hoạ**: phiên K đọc `log-shot.json` `minh_hoa`/`ai_image` (hoặc khai `khoi_lai` trong episode.yaml) | cổng AI tự động áp đúng | việc của K | k2check | — |
| V2-D6 | **Thẻ PP2 "AI retouched two street frames…" sai** với v2 (có 4 đoạn minh hoạ toàn khung) → sửa dòng thành ví dụ "Four short scenes marked Illustration are AI-generated; they add no facts." | không khẳng định sai (§10.6) | đổi chữ đã duyệt | PP2 | — |
| V2-D7 | **TL-1 5,40 cắt/phút** (do R3): chấp nhận như hệ quả R3, hoặc giảm 1–2 lần cắt góc ngắn nhất | đúng R3 | vượt TL-1 | TL-1 | — |
| V2-D8 | Chương 3 còn nhiều cỏ bằng mắt (dưới ngưỡng thước): thêm nội dung có nguồn (trại lính/vườn/trường đua 1909–30 — chờ nguồn vị trí bậc 1) | hết "bãi đất trống" thật sự | cần tra nguồn | ch3 | — |

## §12 Việc chờ chủ dự án
1. **Xem lại MỘT lần** theo `reports/animatic-t3-v2/PHIEU-XEM-V2.md` (8 tệp `xem/`), ghi `<mã shot>: …`; tờ so `to-so/`.
2. Duyệt **4 đoạn minh hoạ** M2, M3, M4, M5 (nhãn "Illustration") và việc **M1 giữ 3D** (V2-D4).
3. Chấm XEM CÂM tắt tiếng (§13.4, ≥ 6/8); số AI tham khảo §8.5.
4. Quyết V2-D1…V2-D8; duyệt sáng tạo (ghi AUTHORSHIP qua phiên P): H1 ngày → đêm với M5 nắng chiều; các góc mới §2; lệnh Omni `omni/lenh/`.
5. Phiên P: RIGHTS cho 4 đầu ra Omni (Gemini API, điều khoản đã đọc ở NC-N2P: không độc quyền, được dùng thương mại) + DejaVuSans cho nhãn "Illustration" (đã có C4-F1); ghi Kinh thánh §14.7 luật R1–R4; BAI-HOC (§10). Sau duyệt → dựng bản cuối 1080p (Cycles GPU cho cú lặn). Nhánh này **không** merge.

**DỪNG — chờ chủ dự án.**
