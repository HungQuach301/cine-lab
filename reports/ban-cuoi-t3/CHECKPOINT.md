# CHECKPOINT — BAN-CUOI-T3 (nhánh `k2c-t3-cuoi`)

Gốc: `origin/k2c-t3-anim-v2` @72e3f0fe ("cứu 4 video gốc Omni") + merge --no-ff `origin/checks-1-17-1` @39d01859 (→ 622a1c27) + `origin/claude/laughing-ptolemy-u7xlwe` @0a10d1fc (→ 170e55ce). 0 xung đột.

<!-- TRANG-THAI -->
## Trạng thái (22/10/2026 21:42 UTC) — tự động `scripts/k2tl/cuoi_ckpt.py`

- **Khung cảnh đinh 1080p đã dựng:** 18288 / 18288 (100 %) — cảnh xong 44/44; đang dựng: —
- **Đoạn đã render (sec/*.mkv, quy về khung phim):** 45/45 đoạn = 18288 / 18288 khung phim (100 %). Còn: 
- **Cycles GPU:** H2T 0–119 ĐÃ THAY · N2.9 TRỌN Cycles (sửa ghép A↔B trong cú máy, 14:20): khung 396–671 EXR 276/276, khung 0–395 EXR 396/396 — ĐÃ THAY + chờ render lại đoạn. Pod: ban-cuoi hep2qaz5zj5ri9 bật 06:30 UTC (đã tắt); ban-cuoi-2 qwsekut0bu3kkg bật 07:05 UTC (đã tắt); ban-cuoi-3 j8m2halzltpbww bật 15:29 UTC (đã tắt); ban-cuoi-4 0fnofdnz5sl6vn bật 16:15 UTC (đã tắt). Dòng cuối: pod3 `18:19:55 [ban-cuoi-3] TAT-XONG` · pod4 `18:20:20 [ban-cuoi-4] TAT-XONG` · xuất `CHUAN-BI-XONG`
- **Số dư RunPod:** $23.09 (dòng `so_du` cuối gio-gpu.jsonl). Đầu phiên $22,95 → $13,97 sau pod 1/2 (chi thật $8,88); 14:57 đọc $28,97 = có nạp thêm $15,00 ngoài phiên, không phải hoàn tiền
- **Lightmap:** 7/7 (b1704, b1779, b1781r, b1782, b1900, b1940, b2026)
- **Omni đã chèn (không nhãn):** M2→C3, M3→N1.4, M4→C5, M5→H1 · M1 giữ 3D
- **Ước còn:** cảnh đinh 0 khung × 5.1 s/khung ÷ P 2 ≈ **0.0 h**; sau đó render đoạn còn lại + LUT + ghép + k2check + xuất ≈ 2–3 h. Giờ máy đã chạy ≈ 17.2 h (mốc 30 h).
- **Việc còn lại (thứ tự):** (1) dựng nốt cảnh đinh; (2) chèn M3 (N1.4), M4 (C5) — tự động khi cảnh xong; (3) N2.9 trọn Cycles: pod 3/4 → nhận → render lại đoạn; (4) render các đoạn còn lại (tự động, chờ RAM); (5) chốt LUT kênh (bão hoà ≥ 0,40) → ghép master + 3 phần + 8 tệp xem; (6) k2check 1.17.2 `--cap`, selftest, LOI-KHOA 3/3, tự đo, XEM CÂM AI; (7) release-k2-t3-g2 (LFS) + thumbnail; (8) báo cáo, DỪNG.
- Dòng cuối log vòng dựng: `21:29 VONG-XONG` · render đoạn: `DOAN-XONG`
<!-- /TRANG-THAI -->

## LUT kênh — đo thử (19:58, 147 khung mẫu 1/4 s từ 33/45 đoạn, 640×360)
Bão hoà trung vị: v 0 → 0,369 · 0,15 → 0,392 · 0,20 → 0,400 · 0,25 → 0,408 · **0,30 → 0,416** · 0,35 → 0,424; màu cờ/đồng phục đổi ≤ 1/255, mái ngói ≤ 5/255. Tờ so `mau/so-lut-v0-v025-v035.jpg`, số `mau/do-lut-mau147.jsonl`. Tạm chọn v = 0,30 (nằm trong ±5 % ngưỡng 0,40 → nêu tên trong báo cáo); chốt khi đủ 45 đoạn.

## LUT kênh — CHỐT (21:38): v = 0,30
Đo toàn phim (190 khung, 1/4 s, đủ 45 đoạn): bão hoà trung vị v 0 → 0,3725 · 0,20 → 0,400 · 0,25 → 0,408 · **0,30 → 0,416** · 0,35 → 0,424. Tệp `channel-k2/k2c-t3-01/mau/k2c-t3-kenh-v030.cube` SHA-256 `1fc6aa38…b38ba6` (+ `.sha256`, `do-lut-toan-phim-190.jsonl`). 0,416 nằm trong ±5 % ngưỡng 0,40 → nêu tên trong báo cáo. Ghép master + 3 phần + 8 tệp xem đang chạy (`log/xuat.sh`); đo mặt nạ ID 43 shot (trong_pct, chủ thể) đang chạy (`log/do_r2.sh`).

## Tệp ngoài git
| Tệp | Tái tạo |
|---|---|
| `/var/tmp/cine-out/k2tl-cache/` | `bash scripts/k2tl/cuoi_cache.sh` |
| lightmap `$K2TL_CACHE/nc/bake/b*/` | `NUONG_META=reports/ban-cuoi-t3/do bash scripts/k2tl/anim_nuong.sh` |
| cảnh đinh 1080p `/var/tmp/cine-out/hero/k2c-t3-cuoi-anim_*` | vòng dựng (dấu cảnh trong heroes.json; `--resume`) |
| `/var/tmp/cine-out/omni1080/M2…M5.mp4` | lệnh ffmpeg trong `scripts/k2tl/cuoi_minh_hoa.py` từ `reports/animatic-t3-v2/omni/goc720/` |

## Sự cố (ghi dần)
- 19:23 **HẾT ĐĨA** (hạn mức phiên): bước nhận N2.9 (`nhan.sh` giữ ~670 PNG 1080p ≈ 3,4 GB) + khung cảnh đinh + gói tải pod. Hậu quả: (a) `gpu_nhan3` dừng; (b) render đoạn H2 lỗi (vòng sau render lại đủ 384 khung); (c) **42 khung cảnh đinh JPG bị ghi cụt** (N1.3: 21, N2.6: 21) mà `hero.js --resume` vẫn giữ (chỉ xét size > 0). Xử lý: xoá gói tải pod (h2t/n29/n29a/co-so .tar) + thư mục xuất n29a (~3,7 GB, tái tạo bằng `chuan_bi.sh`); `scripts/k2tl/cuoi_kiem_khung.py` giải mã đầy đủ 942 khung ghi sau 18:30 → xoá 42 khung hỏng; dừng riêng 2 `hero.js` (N1.3, N2.6) để vòng sau `--resume` dựng lại đúng các khung đã xoá (cùng N3.1 lỗi từ 15:13); dấu `heroes-par.failed` thay bằng thư mục cùng tên để vòng dựng không tự dừng (sẽ gỡ khi xong vòng); nhận N2.9 bằng `cuoi_gpu/nhan_dan.sh` (PNG → jpg ngay, xoá PNG; cùng chỉnh màu). Kiểm lại mọi đoạn mkv ghi sau 18:50 đủ số khung (H2 384/384, N4_4 406/406). Sẽ quét `cuoi_kiem_khung.py` toàn bộ trước khi ghép master.
- 16:23 (pod 3) / 16:53 (pod 4) → 18:20: pod đã dựng đủ n29a 0–395 nhưng máy không kéo về được 108 khung cuối (147–197, 339–395). Nguyên nhân: `pod.py ls` cắt đầu ra ở 4 000 ký tự → JSON hỏng khi > ~147 tệp → `dk_pod.sh` bỏ qua tất cả (try/except), không báo lỗi, pod vẫn chạy chờ. Bộ chờ của tôi hết hạn 2 h nên tôi phát hiện muộn lúc 18:16. Tốn thêm ≈ 2 h × 2 pod × $1,19 ≈ **$4,4 vô ích**. Sửa: bỏ cắt trong `pod.py ls` (dk_pod đang chạy tự kéo lại ở lượt sau, không khởi động lại). Bài học đề xuất cho BAI-HOC (P ghi): không cắt đầu ra máy đọc; khi pod báo xong mà thiếu khung > 2 lượt thì báo LỖI và dừng chờ.
- 15:29 pod 4 (N2.9 khung 198–395) không bật: RunPod lỗi 500 "no longer any instances available" (RTX 5090 SECURE); bộ chờ của tôi hết hạn nên tới 16:15 mới phát hiện (chậm ≈ 45 phút cho dải này). Xử lý: `log/pod4b.sh` thử lại mỗi 3 phút (sau 3 lần đổi SECURE/COMMUNITY); bật được ngay lần 1 lúc 16:15. Không đổi kết quả (cùng GPU, cùng Blender).
- 05:45–06:30: Chromium sập (Target crashed, thiếu RAM) ở N2.9, N2.11, C1 và vài lượt xuất GPU khi nướng b2026 + 3 trình duyệt chạy cùng → P = 1–2 khi nướng, thử lại tự động (giám sát vòng; xuất GPU thử lại 3 lượt).
- 07:22: `nc_topo.js --campath` mặc định 480 khung → `cam.json` của n29 thiếu khung 480–671; bắt được TRƯỚC khi tải lên pod; dựng lại với `--n 684` (chuan_bi.sh đã sửa).
- ≈ 07:24: container khởi động lại (tiến trình mất, đĩa còn); 2 pod vẫn chạy phía RunPod (trạng thái ở đĩa) → khởi động lại nướng/vòng dựng (--resume)/giám sát/CHECKPOINT/điều khiển pod. Pod 2 bật sớm ≈ 25 phút trước khi có dữ liệu (≈ $0,5 chờ).

## Lệnh bổ sung chủ dự án 22/10 (sau rà K-1.17.2) — XONG (≈ 07:45 UTC)
- `git fetch` + merge --no-ff `origin/checks-1-17-2` @451e3970 (chỉ checks/ + reports/k1172/; 0 xung đột); `lock.py --verify` KHỚP 1.17.2 `aca05e60…`. Mọi k2check từ giờ dùng 1.17.2; bỏ nhánh dự phòng 1.17.1 ở việc 9.
- Khai báo bản cuối (qua `cuoi/mk_ep_cuoi.py`, chỉ log + khoá gốc episode.yaml — prep thử ở thư mục tạm rồi prep thật: **0 cảnh đổi dấu**, vòng dựng 1080p không dừng):
  (a) C4: không mục `minh_hoa` M1, `ai_image: false` (K-LAI-2); (b) M2–M5: `luot` (M2-l3, M3-l1, M4-l1, M5-l3) + `sha_goc` tệp gốc + `kiem` (tệp kiểm lượt) + episode.yaml `so_ai: reports/animatic-t3-v2/so-ai-gemini.jsonl` (MINH-HOA (e), K-LAI-3/6);
  (c) mọi shot có cắt góc: `so_goc` + `goc_may: [{id, t, t0, t1, loai}]` (TL-1 (c)); C3 thêm cắt 8,0 s (minh hoạ M2 → cẩu lên);
  (d) episode.yaml `giong_tong_hop: true`, `phat_hanh: {cong: phat_hanh, goi: release-k2-t3-g2, youtube_altered_content: true}` — mô tả YouTube do phiên đóng gói viết (CONG-BO-1 được phép báo thiếu mô tả ở phiên này).
- 14:20: soát mối nối N2.9 trên đoạn đã render: A (0–16,5 s) và Cycles (16,5–28 s) nằm trong CÙNG một cú máy liên tục → trái "không ghép A↔B trong một cú máy" (tông đổi rõ ở 16,5 s). Đổi cách: dựng TRỌN N2.9 bằng Cycles GPU (thêm khung 0–395, 2 pod), thay toàn bộ khung, render lại đoạn N2_9. Tổng Cycles 33 s = 4,3 %.
- Thiếu RAM khi render đoạn chạy cùng 3 cảnh đinh (Chromium sập 3 lần ở N5.1/N5.3) → đổi cách: P = 2 + render đoạn chờ RAM ≥ 5 GB.
