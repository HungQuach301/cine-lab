# Lượt thử GPU nhỏ nhất (CHƯA CHẠY — chờ chủ dự án duyệt thuê)

Mục tiêu: 1 phiên máy GPU thuê **≤ $5**, đo s/khung thật của mô-đun xương sống thời gian (`design/k2v/tl`, nhánh `v5b1b`) và **khớp hình với bản CPU**.
Kế hoạch đầy đủ, tiêu chí và chi phí: `reports/GPU-RD-BAO-CAO.md` §5. Không có khoá API nào trong các script này; máy thuê **không** cần khoá Claude/ElevenLabs/YouTube.

| Bước | Ở đâu | Lệnh | Thời gian (ước) |
|---|---|---|---|
| 0 | container CPU hiện tại | `bash research/gpu/thu-gpu/0_chuan_bi_cpu.sh` → gói `gpu-thu.tar.zst` (mã v5b1b + gói cảnh + 24 khung tham chiếu SwiftShader) | ≈ 6 phút máy CPU |
| 1 | máy GPU (Ubuntu 22.04/24.04, driver NVIDIA ≥ 535) | chép gói lên (`scp`/`rsync`, ≈ 30–60 MB), `bash 1_cai_dat_gpu.sh` | 5–10 phút |
| 2 | máy GPU | `bash 2_chay_thu.sh` → `ket-qua/` (probe, hồ sơ 3 khung, 24 khung so, trọn 480 khung, so hình) | 10–20 phút |
| 3 | máy GPU → về | chép `ket-qua/` về (≈ 10–120 MB), **xoá máy** (terminate, không chỉ stop) | 2 phút |

Dừng ngay (không tiếp tục tiêu tiền) khi: `webgl_probe` vẫn ra SwiftShader/llvmpipe sau 2 cách cờ (vulkan, egl) → ghi lỗi, xoá máy.
