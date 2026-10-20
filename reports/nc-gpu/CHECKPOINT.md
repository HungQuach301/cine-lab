# NC-GPU — CHECKPOINT (nhánh thật: `claude/eloquent-dijkstra-kemr8j` — harness buộc; lệnh yêu cầu `nc-gpu`; gốc origin/claude/clever-franklin-daez5k @718dec9e = nc-cpu)

## Lượt 1 (≈ 00:30 UTC 20/10)
- Bước 0 QUA: `GET rest.runpod.io/v1/pods` → HTTP 200 `[]`; GraphQL `myself` → số dư $25,00. Giá đọc qua API `api.runpod.io/graphql gpuTypes` 20/10/2026 (`reports/nc-gpu/gia-runpod-20261020.jsonl`): RTX 5090 32 GB SECURE $1,19/h (kho Low), RTX PRO 4500 32 GB SECURE $0,72/h (Low), RTX 4090: không có kho; COMMUNITY: không có kho.
- Pod 1: RTX 5090 SECURE (driver 595.91, OptiX OK), python:3.13-slim + máy chủ tệp `design/pt/gpu/pod_srv.py` qua proxy HTTPS RunPod; mã TOK một lần, không khoá nào lên pod.
- Benchmark Blender Open Data (launcher 3.3.0, Blender 5.2.0, OPTIX): monster 7 313,76 · junkshop 5 303,61 · classroom 4 037,31 mẫu/phút.
- Bước 0b QUA: tệp cảnh `ncg-canh.tar` 1 259,8 MB (SHA-256 655050540e31…) lên pod 61,4 s (20,5 MB/s), SHA khớp trên pod; ảnh về qua GET theo khúc.
- Đang dựng: 6 khung B NC-CPU nguyên văn trên GPU (nc_gpu_compat.py) + 6 khung cảnh mới 64 spp; cục bộ: ánh sáng/khói từng khung cú lặn (480) + hình học cú lặn theo mốc.

## Lượt 2 (≈ 02:45 UTC 20/10)
- 6 khung cổng × 2 mức (64/256 spp) + 6 khung B NC-CPU nguyên văn trên GPU (8,6–9,9 s/khung; CPU NC-CPU 87–127 s; đo lại CPU cục bộ "cang" 101,7 s) → `reports/nc-gpu/khung/`, tờ so `to-so-khung.jpg`.
- Sửa nguyên nhân "nhạt": ánh trời khuếch tán ×1/π (khớp three.js) → bão hoà trung vị 0,298 → 0,403.
- Chấm mù 640×360 (3 vai Sonnet 5.5, $1,04): A 12/18 hạng nhất, Cycles GPU 6, V7B 0.
- Cú lặn 480 khung đang dựng trên 2 pod RTX 5090 (khung 93–335, 336–479); khung 0–92 đã về. Lỗi vận hành: bộ canh chia việc khớp nhầm câu lỗi `ls` → tắt pod 2 ở khung 92 (không mất khung nào; đã sửa phép kiểm).
- PRO 4500: "There are no instances currently available" (00:48 UTC). Pod 3 nhận tệp chỉ 2,0 MB/s (pod 1, 2, 4: 20–22 MB/s).

## Lượt 3 (≈ 03:25 UTC 20/10)
- Container của phiên khởi động lại ≈ 03:15 (không do phiên): dữ liệu `/var/tmp/cine-out/ncg` còn nguyên; pod 3/4 tiếp tục dựng phía RunPod; pod 5 (vừa bật, chưa có dữ liệu) được nạp lại. Bộ theo dõi mới `design/pt/gpu/chay/theo_pod.sh` (kéo ảnh, dừng theo khung, tắt pod).
- Chia cú lặn: pod 3 336–479, pod 4 93–255, pod 5 256–335; khung 0–92 đã về.

## Lượt 4 (≈ 06:00 UTC 20/10)
- Pod 4 tắt sớm trước khi kéo khung 242–255 (dựng lại trên pod 6, xong); `theo_pod.sh` nay kiểm đủ dải khung trước khi tắt.
- Pod 3: hết VRAM 32 GB ở khung 442 (rò dữ liệu cụm khói khi dựng lại từng khung với `--persist`), sau đó Blender rơi về CPU của pod (GPU 0 %) → khung 444–467 dựng bằng CPU ≈ 220 s/khung. Sửa: xoá dữ liệu cụm khói cũ; `--needgpu` dừng thay vì rơi âm thầm về CPU. `pod_dive.sh`: lỗi số học đoạn cuối (468–479 chưa dựng) đã sửa.
- Pod 7: dựng 442–443, 468–479 (+ 444–445 để đối chứng GPU ↔ CPU-pod).

## CUỐI (≈ 07:30 UTC 20/10) — DỪNG chờ chủ dự án
- Cú lặn 480/480 khung Cycles GPU; bản xem `reports/nc-gpu/lan/ncg-lan-xem.mp4` (4,25 MB) + master ngoài git (SHA trong báo cáo). Dựng lại 36 khung để lửa sáng dần theo uNight (pod 8).
- Không còn pod nào chạy; RunPod thật $10,98 (số dư $14,02). Báo cáo hoàn chỉnh `reports/nc-gpu/NC-GPU-BAO-CAO.md`.
