#!/bin/bash
# GPU-RD · bước 2 (máy GPU): probe → hồ sơ 3 khung (470/175/300 SPP2) → 24 khung so với SwiftShader → trọn 480 khung (đo tốc độ) → so hình. Ra: ~/gpu-thu/ket-qua/
set -uo pipefail
H=$HOME/gpu-thu; R=$H/repo; G=$R/research-gpu; K=$H/ket-qua; mkdir -p "$K"
export K2TL_CACHE=$H/cache CINE_PW=$H/pw/node_modules/playwright PLAYWRIGHT_BROWSERS_PATH=${PLAYWRIGHT_BROWSERS_PATH:-$HOME/.cache/ms-playwright}
# render.js/profile.js nạp Playwright từ /opt/pw → liên kết về bản vừa cài (không sửa mã v5b1b)
sudo mkdir -p /opt/pw && sudo ln -sfn "$H/pw/node_modules" /opt/pw/node_modules
T0=$(date +%s); log() { echo "[$(( $(date +%s)-T0 ))s] $*" | tee -a "$K/nhat-ky.txt"; }
# 1) chọn đường GL: vulkan → egl (headless-shell), rồi Chromium đầy đủ (CINE_CHANNEL=chromium)
PICK=""
for ch in "" chromium; do for gl in vulkan egl; do
  if CINE_CHANNEL=$ch CINE_GL=$gl node -r "$G/gl_flags.js" "$G/webgl_probe.js" > "$K/probe-$gl-${ch:-shell}.json" 2>&1; then PICK="$gl ${ch}"; break 2; fi
done; done
cat "$K"/probe-*.json | tee -a "$K/nhat-ky.txt"
[ -z "$PICK" ] && { log "DỪNG: không có WebGL GPU thật (SwiftShader/llvmpipe) — xoá máy"; exit 5; }
export CINE_GL=${PICK% *} CINE_CHANNEL=${PICK#* }; [ "$CINE_CHANNEL" = "$CINE_GL" ] && CINE_CHANNEL=""; log "chọn CINE_GL=$CINE_GL kênh=${CINE_CHANNEL:-headless-shell}"
# 2) hồ sơ 3 khung (cùng phép đo container CPU)
node -r "$G/gl_flags.js" "$G/profile.js" --root "$R" --only 470,175,300 --rep 2 --tech '{"spp":2}' --out "$K/profile-gpu.json" 2>>"$K/err.txt" | tee -a "$K/nhat-ky.txt"
# 3) 24 khung rải, so với tham chiếu SwiftShader (dựng lẻ --only như bản tham chiếu)
node -r "$G/gl_flags.js" "$R/scripts/k2tl/render.js" --scene gib20 --pack gib --w 1920 --h 1080 --only "$(cat $H/frames.txt)" --out "$K/khung-gpu" 2>>"$K/err.txt" | tee -a "$K/nhat-ky.txt"
"$H/py/bin/python" "$G/compare.py" "$H/ref-swiftshader" "$K/khung-gpu" --out "$K/so-hinh.json" | tail -1 | tee -a "$K/nhat-ky.txt"
# 4) trọn 480 khung tuần tự (tốc độ thật, SPP thích ứng) — giữ log, khung chỉ giữ 540p để chép về nhẹ
node -r "$G/gl_flags.js" "$R/scripts/k2tl/render.js" --scene gib20 --pack gib --w 1920 --h 1080 --out "$H/tron" 2>>"$K/err.txt" | tee "$K/tron.json" | tee -a "$K/nhat-ky.txt"
cp "$H/tron/log.json" "$K/tron-log.json"
ffmpeg -loglevel error -framerate 24 -i "$H/tron/%05d.jpg" -vf scale=960:540 -c:v libx264 -crf 18 -pix_fmt yuv420p "$K/gib20_gpu_540p.mp4" 2>/dev/null || log "không có ffmpeg — bỏ bản xem"
nvidia-smi --query-gpu=name,utilization.gpu,memory.used --format=csv >> "$K/nvidia.txt"; cp "$H/nvidia.txt" "$K/" 2>/dev/null
log "XONG — chép $K về rồi XOÁ MÁY (terminate)"
