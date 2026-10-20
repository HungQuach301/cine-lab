# NC-GPU — CHECKPOINT (nhánh thật: `claude/eloquent-dijkstra-kemr8j` — harness buộc; lệnh yêu cầu `nc-gpu`; gốc origin/claude/clever-franklin-daez5k @718dec9e = nc-cpu)

## Lượt 1 (≈ 00:30 UTC 20/10)
- Bước 0 QUA: `GET rest.runpod.io/v1/pods` → HTTP 200 `[]`; GraphQL `myself` → số dư $25,00. Giá đọc qua API `api.runpod.io/graphql gpuTypes` 20/10/2026 (`reports/nc-gpu/gia-runpod-20261020.jsonl`): RTX 5090 32 GB SECURE $1,19/h (kho Low), RTX PRO 4500 32 GB SECURE $0,72/h (Low), RTX 4090: không có kho; COMMUNITY: không có kho.
- Pod 1: RTX 5090 SECURE (driver 595.91, OptiX OK), python:3.13-slim + máy chủ tệp `design/pt/gpu/pod_srv.py` qua proxy HTTPS RunPod; mã TOK một lần, không khoá nào lên pod.
- Benchmark Blender Open Data (launcher 3.3.0, Blender 5.2.0, OPTIX): monster 7 313,76 · junkshop 5 303,61 · classroom 4 037,31 mẫu/phút.
- Bước 0b QUA: tệp cảnh `ncg-canh.tar` 1 259,8 MB (SHA-256 655050540e31…) lên pod 61,4 s (20,5 MB/s), SHA khớp trên pod; ảnh về qua GET theo khúc.
- Đang dựng: 6 khung B NC-CPU nguyên văn trên GPU (nc_gpu_compat.py) + 6 khung cảnh mới 64 spp; cục bộ: ánh sáng/khói từng khung cú lặn (480) + hình học cú lặn theo mốc.
