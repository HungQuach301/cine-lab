# BÁO CÁO BẢN CUỐI T3 Gibraltar — BAN-CUOI-T3 (22–23/10/2026) — DỪNG chờ chủ dự án

> Phiên BAN-CUOI-T3. Làm bản phát hành 1080p của tập T3 từ animatic v2 (chủ dự án duyệt V2-D1…D8 kèm 2 điều chỉnh, 22/10 11:09). **Không merge.** Mọi số dưới đây là số đo thật trên tệp; "tự đo" chỉ ghi số, không tự chấm đạt.

## 0. Nhánh, gốc, tệp chính

| Mục | Giá trị |
|---|---|
| Nhánh làm việc | `k2c-t3-cuoi` (đã đẩy; **không** dùng nhánh mặc định của bộ khung `ccr-e46904cd-ltvfbq`) |
| Gốc | `origin/k2c-t3-anim-v2` @72e3f0fe + merge --no-ff `origin/checks-1-17-1` @39d01859 (→ 622a1c27) + `origin/claude/laughing-ptolemy-u7xlwe` @0a10d1fc (→ 170e55ce) + **`origin/checks-1-17-2` @451e3970 (→ 681f0081, lệnh bổ sung 22/10)** — 0 xung đột |
| LOCK | 1.17.2 `aca05e60…6d60` — `lock.py --verify` KHỚP ở mọi lần chạy và mọi commit |
| Nhánh phát hành | `release-k2-t3-g2` — xem §10 (SHA commit ghi ở §10) |
| Master | `k2-t3-v1-master.mp4` SHA-256 `5b9f0bccd88830ab212a6747259ac597328ae87bb964addc953bf1928fd7b682` · 1920×1080 H.264 High 24 fps · 762,000 s · 18 288 khung · hình 18,5 Mb/s (crf 17, trần 19 Mb/s) · AAC LC 48 kHz 310 kb/s · tổng 18,8 Mb/s · 1,79 GB |
| Lệnh bổ sung 22/10 (sau K-1.17.2) | XONG ≈ 07:45 UTC: merge checks-1-17-2; khai M1 không đoạn / C4 `ai_image: false`; M2–M5 `luot` + SHA gốc + tệp kiểm; `so_goc`/`goc_may` mọi shot cắt góc; `giong_tong_hop: true` + `phat_hanh: {cong: phat_hanh, goi: release-k2-t3-g2, youtube_altered_content: true}`; không đổi dấu cảnh nào (prep thử → 0 cảnh đổi) |
| Lệnh bổ sung 22/10 (trạng thái) | XONG 14:57: khối "Trạng thái" trong CHECKPOINT tự cập nhật mỗi lần đẩy (`scripts/k2tl/cuoi_ckpt.py`), số dư RunPod ghi vào `gio-gpu.jsonl` |

## 1. Việc 1 — máy + nội dung (phiếu chi tiết: `PHIEU-XEM-CUOI.md`, 21 shot đổi)
- **1a C4** (V2-D4: giữ 3D): 3 góc — máy thấp theo đoàn cứu viện Rodney (9 tàu chiến + 12 tàu hàng, tàu ≥ 6 px), Rock không cắt mép, giữ tiêu điểm; ngày 17 → 19/1/1780.
- **1b ch3 + N4.1 (+C1)**: vật đời sống chung **bậc 5, `uoc_luong: true`**, không công trình có tên, đúng mốc năm (`design/k2v/tl/doisong.js` mới; móc vào `t3tl.js`): N3.1, N3.3, N3.4, N3.5, N4.1 và (**sau k2check lượt 1**) C1. Trống (bằng + sườn, mặt nạ ID 1 mẫu/s) — xem §9.2.
  - **Sai sót của tôi:** lần đầu tôi **bỏ sót C1** (công cụ soi chỉ cờ "bằng" > 40 %, không cộng sườn, và không chạy cho C1). k2check lượt 1 bắt C1 trống 10,5 s liên tục. Đã sửa máy + vật, dựng lại C1, xuất lại master. Một lượt thử ngửa máy (trời 61 %) đạt số nhưng dải trại chỉ còn vệt chân trời — **bỏ** vì là lách chỉ số.
- **1c H1** (V2-D3): "To walk in from Spain…" 0,50 s → "Since July 2026…" 3,76 s → "Midnight at the Gibraltar frontier." **9,75–11,90 s trên đêm 3D**, kết trước 12,0 s; M5 thu còn 4,5–9,5 s (≤ 1 s bớt). Chỉ cắt/đổi chỗ từ master giọng, không tạo giọng mới.
- **1d 1969** (N5.1): rào chắn hạ ngang đường 8/6/1969, đám đông + xe đứng lại hai phía, **≈ 4,8 s** thấy rõ.
- **1e nhịp F1**: thêm góc/biến cố ở N2.8, N5.2, N5.3, N5.4, N5.6, nền thẻ PP chạy tiếp; khói bếp/lửa đồng (bậc 5) ở khoảng > 6 s các shot trước 1950. Còn 1 khoảng > 6 s ngoài khung neo: **N5.5 0,5 → 8,5 s** (giữ nhịp bookend).
- **1f**: bỏ mọi nhãn "Illustration" (V2: không chữ AI trên hình/thẻ; công bố AI chỉ ở YouTube).

## 2. Việc 2 — Cycles GPU (RunPod RTX 5090 SECURE, $1,19/h)
| Pod | Bật → tắt (UTC) | Giờ | Việc |
|---|---|---|---|
| 1 `ban-cuoi` | 22/10 06:30 → 10:59 | 4,48 | đo thử 2 s H2T 0–47 + H2T, N2.9 396–671 |
| 2 `ban-cuoi-2` | 07:05 → 10:05 | 2,99 | N2.9 534–671 |
| 3 `ban-cuoi-3` | 15:29 → 18:19 | 2,83 | N2.9 0–197 (dựng lại trọn) |
| 4 `ban-cuoi-4` | 16:15 → 18:20 | 2,08 | N2.9 198–395 (lần đầu 15:29 lỗi 500 "hết máy", bật lại 16:15) |
- **Đo thử 2 s**: ngày ≈ 27–28 s/khung, đêm 64 spp 100–117 s/khung.
- **Tỉ lệ Cycles** = H2T 5,0 s + N2.9 28,0 s = **33,0 s = 4,33 %** (≤ 20 %). **Không ghép A↔B trong một cú máy**: bản đầu N2.9 ghép A 0–16,5 s với Cycles 16,5–28 s trong cùng cú máy (tôi phát hiện khi soát mối nối 14:20) → dựng lại TRỌN N2.9 bằng Cycles.
- **Chi phí thật (số dư tài khoản)**: $22,95 → $14,07 (pod 1–2: **$8,88**); $28,97 → $23,09 (pod 3–4: **$5,88**; có $15,00 nạp thêm ngoài phiên lúc ≈ 14:5x). **Tổng RunPod $14,76** (mốc $20). Trong đó ≈ **$4,4 lãng phí** (pod 3/4 chạy chờ ≈ 2 h vì lỗi kéo EXR — §12).

## 3. Việc 3 — dựng 1080p cách A
- Lightmap nướng lại 7/7 (b1704 2280 s, b1779 1160 s, b1781r 2104 s, b1782 1548 s, b1900, b1940 2685 s, b2026 2617 s). Cảnh đinh 44/44 = **18 288 khung** (đúng số khung phim) + C1 dựng lại 540 khung; 45/45 đoạn. Giờ máy toàn phiên ≈ **22 h** (04:30 → ≈ 02:30; mốc 30 h) — không cần pod CPU.
- Chống lỗi: Chromium sập khi RAM thấp → P = 2 + render đoạn chờ RAM ≥ 5 GB; hết đĩa 19:23 → kiểm giải mã đủ khung (`cuoi_kiem_khung.py`) và dựng lại 42 khung cụt (§12).

## 4. Việc 4 — Omni 1080p
M2→C3, M3→N1.4, M4→C5, M5→H1 từ `goc720` (Lanczos + unsharp 5:5:0,45), khớp màu Lab k 0,7; **M1 giữ 3D** (V2-D4). Không nhãn. Không dùng dự phòng Omni. Gemini **$0**. Minh hoạ AI **27,4 s = 3,6 %**. Nhật ký `do/minh-hoa-ghep.json`.

## 5. Việc 5 — LUT kênh
Một LUT cho cả phim: vibrance bảo vệ màu đậm, giữ luma/tông. **v = 0,30**: `channel-k2/k2c-t3-01/mau/k2c-t3-kenh-v030.cube` SHA-256 `1fc6aa3822708ca146fce932807029f9d811c0ffe2ee2f52d084104618b38ba6`. Đo toàn phim (190 khung, 45 đoạn): bão hoà trung vị v 0 → 0,3725 · 0,20 → 0,400 · 0,25 → 0,408 · **0,30 → 0,416** · 0,35 → 0,424. Màu cờ/đồng phục đổi ≤ 1/255, mái ngói ≤ 5/255 (`mau/do-lut-toan-phim-190.jsonl`, tờ so `reports/ban-cuoi-t3/mau/`). **Trên master: bão hoà trung vị 0,416 — trong ±5 % ngưỡng 0,40 (nêu tên).** ΔE76 shot kề: TB 22,4, trung vị 19,3, lớn nhất N2.7 → N2.8 61,2 (chiều → biển trưa, đổi cảnh có chủ ý).

## 6. Việc 6 — âm thanh
Giọng master `T3-loi-G1-v42-14LUFS` (chỉ cắt/đổi chỗ 3 câu H1), nhạc §14.6, SFX gói "tối giản dưới lời" + HOAMAI-1 (sau 2,85 s), CHIM-1 (5–33 s), giữ MAYBAY-1, COI-1; 2 thẻ im lặng không SFX (216 sự kiện, 38 tệp, `channel-k2/k2c-t3-01/cuoi/RIGHTS-SFX-T3.md`). Chuỗi trộn có `nhac[]`. **Master: −14,0 LUFS · LRA 3,1 LU · đỉnh thật −1,4 dBTP** (≤ −1). Stem giọng/nhạc/SFX căn lệch 48 mẫu (dư −28 dB) — ngoài git, SHA ở §10.

## 7. Việc 7 — thẻ + phụ đề
PP1 9,0 s (thân 26 từ = 2,89 từ/s; **k2check đếm cả tiêu đề "How this film was made" → 31 từ = 3,4 từ/s**, xem §9 khiếu nại A4), dòng 3 đúng chữ chủ dự án. PP2 8,0 s, 2 dòng mới (18 từ). Phụ đề CC `k2-t3-v1-en.srt` + `.vtt` (129 câu, thứ tự mới, không ghép cứng).

## 8. Việc 8 — khai cho K (F2–F8)
episode.yaml bản cuối (không animatic); beats = biến cố hình, mốc lời → `moc_loi` (F2); `khung_neo`/`im_lang` (F4); `lop_nha` C3/C5 (F5); `log_chu` = log render đoạn (`--logs sec/`, F6); `trong_pct` + `chu_the_pct` dạng `[[t, %]]` từ mặt nạ ID 43 shot + `chu_the_eo_dat` (F8); `so_goc`/`goc_may`; `minh_hoa` + `luot`/`sha_goc`/`kiem` + `so_ai` cấp episode; `agl_m`; `bac`/`uoc_luong`; N2.9 `lan` trọn shot; `xem_cam: xem-cam-cuoi.json`. **Sự cố khai:** 6 tệp khai `.json` bị `channel-k2/.gitignore` (`*.json`) chặn — đã thêm `-f` như animatic/v7p.

## 9. Việc 9 — kiểm cuối
### 9.1 k2check 1.17.2 `--cap` (LOCK KHỚP) — 3 lượt
<!-- K2CHECK -->

### 9.2 Tự đo master (`do/tu-do-master.json`, `do/r2-tom-tat.json`)
| Chỉ số | Giá trị |
|---|---|
| Thời lượng | 762,000 s (18 288 khung) |
| LUFS / LRA / đỉnh thật | −14,0 / 3,1 LU / −1,4 dBTP |
| Bão hoà / colorfulness / chi tiết (trung vị, 381 khung) | **0,416** / 77,0 / 27,7 |
| Trống (bằng > 50 %) theo chương | ch0 0 % · ch1 3,1 % · ch2 3,4 % · ch3 0 % · ch4 0 % · ch5 0 %; liên tục dài nhất **4,0 s (N1.5)** |
| Trống (bằng + sườn > 40 %) > 4 s liên tục (ngưỡng mắt 1b) | trong phạm vi 1b: **N3.3 7 s (40–45 %)**; ngoài phạm vi: N1.3 16 s, N2.7 14 s, N2.11 12 s, N5.1 10 s, N1.6 5 s, N1.4/N1.5 4 s |
| % minh hoạ AI / % Cycles | 3,6 % / 4,33 % |
| Cắt/phút | 3,39 (shot) · 5,59 (cả cắt góc) · 8,19 (cả bước năm) |
| XEM CÂM 3 AI (tham khảo, 1 khung/4 s, 320×180, không tiếng) | từ khoá **45/48** (R1 16/16, R2 13/16, R3 16/16; Q4 5/6, Q7 4/6); thang 8 câu: 8,0 · 6,5 · 8,0; $0,39. **P chưa đọc lại nguyên văn; chủ dự án chưa chấm** |

## 10. Việc 10 — xuất
<!-- XUAT -->

## 11. Chi phí thật
| Dịch vụ | Chi | Mốc |
|---|---|---|
| RunPod | **$14,76** (4 pod, 12,4 giờ GPU; ≈ $4,4 lãng phí do lỗi kéo EXR) | $20 |
| Claude API (XEM CÂM 3 AI, `claude -p`) | **$0,39** | $10 |
| OpenAI | $0 | $5 |
| Gemini | $0 (không dùng dự phòng Omni) | $0 (+$8 dự phòng) |
| ElevenLabs / YouTube | 0 ký tự / 0 | 0 |
| Giờ máy | ≈ 22 h | 30 h |

## 12. Sự cố (chi tiết + giờ trong `CHECKPOINT.md`)
1. **N2.9 ghép A↔B trong một cú máy** (14:20) → dựng lại trọn bằng Cycles (pod 3/4).
2. **Pod 4 không bật** 15:29 (RunPod hết RTX 5090 SECURE); bộ chờ của tôi hết hạn nên 16:15 mới bật lại.
3. **Lỗi kéo EXR** 16:23–18:20: `pod.py ls` cắt đầu ra 4 000 ký tự → JSON hỏng khi > ~147 tệp → không kéo được 108 khung, pod chạy chờ ≈ 2 h (≈ $4,4). Sửa: bỏ cắt.
4. **Hết đĩa 19:23** (giữ ~670 PNG 1080p khi nhận N2.9): 42 khung cảnh đinh JPG bị ghi cụt mà `--resume` vẫn giữ → kiểm giải mã, xoá, dựng lại; nhận GPU đổi sang `nhan_dan.sh` (PNG → jpg rồi xoá ngay).
5. **Master lượt 1 = 41,3 Mb/s, 3,94 GB** (> 2 GB/tệp LFS gói thường) + ranh 3 phần sai (173 s thay vì ranh chương 262,208 s) → crf 17 + trần 19 Mb/s, khung khoá đúng ranh; 3 phần cắt sao chép luồng theo chỉ số khung (lượt `-ss/-t` lệch 1 khung, đã kiểm MD5 khung ranh KHỚP).
6. **Vòng tệp xem chỉ ra 1/8** (ffmpeg đọc stdin heredoc) → `-nostdin`.
7. **C1 bỏ sót ở 1b** (§1) — sửa sau k2check lượt 1.
8. Container khởi động lại ≈ 07:24 — khởi động lại tiến trình nền (`--resume`), pod giữ trạng thái ở đĩa.

## 13. Chỉ số trong ±5 % ngưỡng (nêu tên)
Bão hoà trung vị master **0,416** (ngưỡng ≥ 0,40) · trống liên tục dài nhất **4,0 s N1.5** (≤ 4 s, 1b) · N3.3 trống **40–45 %** (ngưỡng mắt 40 %) · N5.1 khoảng biến cố **6,0 s** khi tính cắt góc (≤ 6 s) · LUFS −14,0 (−15…−13,8) — trong khoảng, không sát biên.

## 14. Đề xuất (chờ chủ dự án)
| # | Đề xuất | Ưu | Nhược | Tác động | Rủi ro |
|---|---|---|---|---|---|
| D1 | N4.5 (27,2 s) và N5.6 (20 s) **thêm góc thứ 2** (EO-DAT-R3 (a)) | Đạt R3 (a) | N5.6 là bookend ngược của H1 — một góc là ý đồ | dựng lại 2 cảnh ≈ 2 h máy + xuất lại | đổi nhịp bookend |
| D2 | PP1: rút 2 dòng đầu còn ≤ 9 từ (nếu K xác nhận tính cả tiêu đề) | đạt ≤ 3 từ/s theo cách K đếm | sửa chữ đã duyệt (dòng 1–2) | dựng lại đoạn PP1 + xuất | thấp |
| D3 | Master giữ crf 16 không trần (41 Mb/s, 3,9 GB) nếu tài khoản GitHub cho LFS > 2 GB/tệp | chất lượng nguồn cao hơn cho YouTube | tốn LFS (lưu trữ/băng thông) | thay 1 tệp ở nhánh release | thấp; mắt thường khó thấy khác ở 1080p |
| D4 | Stem âm thanh vào LFS (thêm mẫu `release-*/*-stem-*.wav` vào `tools/lfs-allow.txt`) | đủ gói bán phim | ≈ 0,8 GB LFS | chỉ nhánh release | thấp |
| D5 | N3.3 / N2.7 / N2.11 / N1.3: thêm vật thật (người/trại) hoặc máy khác để trống (bằng + sườn) < 40 % | mắt bớt "cỏ" | ngoài phạm vi 1b lệnh này | dựng lại 1–4 cảnh | thấp |
| D6 | N2.8 viền vàng lửa/khói ở góc 2 (thấy khi soát) | — | cần chủ dự án xem | — | — |
| D7 | BAI-HOC (P ghi): không cắt đầu ra máy đọc; pod báo xong mà thiếu khung > 2 lượt → LỖI + dừng; đo "trống" cùng định nghĩa với K (bằng + sườn) | tránh lặp sự cố 3, 7 | — | — | — |

## 15. Việc chờ chủ dự án
1. **Duyệt G2** bản cuối: xem master hoặc 3 phần / 8 tệp xem (`reports/ban-cuoi-t3/xem/`), phiếu `PHIEU-XEM-CUOI.md`, tờ khung `to/to-khung.jpg`, tờ so `to/to-so-*.jpg`, tờ soi `to/soi/`.
2. **XEM CÂM chủ dự án** (cổng §13.4 — K báo XEM-CAM (b) chờ người) + P đọc lại nguyên văn 3 phiếu AI.
3. Chọn 1/6 thumbnail (`k2-t3-v1-thumb-1…6.jpg`, tờ `to/to-thumbnail-6.jpg`).
4. Quyết D1–D6; mô tả YouTube (câu công bố AI/synthetic — CONG-BO-1/K-LAI-2 (d) chờ phiên đóng gói).
5. K xét `checks-appeal.md` (5 điểm: TL-3, Q37 (a), R3 (b), PP-1, Q33; + SACH-1 thẻ chương/thẻ PP).
6. Merge (phiên P) — phiên này **không merge**.
