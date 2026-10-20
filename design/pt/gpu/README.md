# design/pt/gpu — NC-GPU (20/10/2026): Cycles trên GPU thuê (RunPod), dùng lại cảnh B của NC-CPU

| Tệp | Vai |
|---|---|
| `pod.py`, `pod_srv.py`, `pod_setup.sh` | điều khiển pod RunPod (bật/tắt/sổ giờ `reports/nc-gpu/gio-gpu.jsonl`), máy chủ tệp trên pod (PUT/GET theo khúc, SHA), cài Blender 5.2.2 LTS — khoá RunPod do proxy gắn, mã không đọc khoá |
| `pod_bench.sh` | Blender Open Data benchmark (launcher 3.3.0, Blender 5.2.0, OPTIX) |
| `nc_gpu_compat.py` | chạy NGUYÊN VĂN `../cpu/nc_blend.py` trên GPU (hệ số GPU/CPU cùng tệp) |
| `gpu_export.js` | xuất cảnh k2v + màu vật liệu, ảnh lá cờ, khói/lửa (`fx.json`); `--lightfx a:b` trạng thái ánh sáng/khói từng khung |
| `gpu_blend.py` | cảnh Cycles "điện ảnh" (sửa lỗi NC-CPU §3, ánh trời khớp three.js, thể tích, MB, DOF, bụi ×3, vân 4k, `--needgpu`) |
| `pod_gates.sh`, `pod_dive.sh`, `pod_thu.sh` | trên pod: 6 khung cổng (B nguyên văn / 64 / 256 spp), cú lặn theo đoạn mốc, lượt thử chỉnh |
| `near_box.py`, `topo_full.py`, `dive_pack.py`, `do_look.py` | hộp albedo 0,5 m quanh máy, ghép ô albedo, gói cú lặn khử trùng lặp SHA, số đo màu/sương so đích look |
| `chay/` | lệnh đã chạy: `env.sh`, `expg.sh`, `topo.sh`, `expdive.sh`, `grade.sh`, `ghep_lan.sh`, `theo_pod.sh` (kéo ảnh, kiểm đủ dải, tắt pod) |

Chạy lại: như `../cpu/README.md` (worktree V7B + bộ đệm k2tl + vân CC0, 4k thêm bằng `fetch_tex` trong báo cáo) → `chay/expg.sh`, `chay/topo.sh nam|gan` → tar `exp topo pack tex` → `pod.py len/put/run` → `pod_gates.sh` / `pod_dive.sh` → `chay/grade.sh`, `chay/ghep_lan.sh`. Báo cáo: `reports/nc-gpu/NC-GPU-BAO-CAO.md`.
