# CHECKPOINT — BAN-CUOI-T3 (nhánh `k2c-t3-cuoi`)

Gốc: `origin/k2c-t3-anim-v2` @72e3f0fe ("cứu 4 video gốc Omni") + merge --no-ff `origin/checks-1-17-1` @39d01859 (→ 622a1c27) + `origin/claude/laughing-ptolemy-u7xlwe` @0a10d1fc (→ 170e55ce). 0 xung đột.

## Trạng thái (cập nhật 22/10 05:46 UTC)
- Bộ đệm cảnh gib xong; nướng lightmap nền (b1779 1 160 s, b1782 1 548 s xong; còn b2026 b1704 b1781r b1940 b1900).
- Việc 1 (máy + nội dung) XONG ở đặc tả `channel-k2/k2c-t3-01/cuoi/` (mk_ep_cuoi.py → episode.yaml, log-shot.json, bang-shot.json, anim-loi.json, phu-de.srt): 1a C4, 1b ch3–4, 1c H1, 1d cổng 1969, 1e nhịp (283 biến cố, TB 2,65 s), 1f bỏ nhãn (cuoi_minh_hoa.py). Mã `design/k2v/tl/*` CHỐT.
- Prep 1080p xong (762,0 s, 18 288 khung; ElevenLabs 0 ký tự). Vòng dựng cảnh đinh 1080p SPP 4 đang chạy nền: `scripts/k2tl/anim_vong2.sh` (PGID `/var/tmp/cine-out/log/vong.pgid`, P đọc `/var/tmp/cine-out/log/P` = 2 khi nướng). Đo sơ bộ ≈ 3,3–3,8 s/khung/tiến trình.
- Omni 1080p: 4 tệp phóng Lanczos + unsharp ở `/var/tmp/cine-out/omni1080/` (tái tạo bằng lệnh trong `scripts/k2tl/cuoi_minh_hoa.py`).
- Chưa: GPU (việc 2), chèn minh hoạ + lặn sau khi dựng, LUT, âm thanh, k2check, xuất.

## Tệp ngoài git
| Tệp | Tái tạo |
|---|---|
| `/var/tmp/cine-out/k2tl-cache/` | `bash scripts/k2tl/cuoi_cache.sh` |
| lightmap `$K2TL_CACHE/nc/bake/b*/` | `NUONG_META=reports/ban-cuoi-t3/do bash scripts/k2tl/anim_nuong.sh` |
| cảnh đinh 1080p `/var/tmp/cine-out/hero/k2c-t3-cuoi-anim_*` | vòng dựng (dấu cảnh trong heroes.json; `--resume`) |
| `/var/tmp/cine-out/omni1080/M2…M5.mp4` | lệnh ffmpeg trong `scripts/k2tl/cuoi_minh_hoa.py` từ `reports/animatic-t3-v2/omni/goc720/` |

## Sự cố (ghi dần)
- 05:45–06:30: Chromium sập (Target crashed, thiếu RAM) ở N2.9, N2.11, C1 và vài lượt xuất GPU khi nướng b2026 + 3 trình duyệt chạy cùng → P = 1–2 khi nướng, thử lại tự động (giám sát vòng; xuất GPU thử lại 3 lượt).
- 07:22: `nc_topo.js --campath` mặc định 480 khung → `cam.json` của n29 thiếu khung 480–671; bắt được TRƯỚC khi tải lên pod; dựng lại với `--n 684` (chuan_bi.sh đã sửa).
- ≈ 07:24: container khởi động lại (tiến trình mất, đĩa còn); 2 pod vẫn chạy phía RunPod (trạng thái ở đĩa) → khởi động lại nướng/vòng dựng (--resume)/giám sát/CHECKPOINT/điều khiển pod. Pod 2 bật sớm ≈ 25 phút trước khi có dữ liệu (≈ $0,5 chờ).
