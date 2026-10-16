#!/bin/bash
# GPU-RD · bước 1 (máy GPU thuê, Ubuntu 22.04/24.04 có driver NVIDIA): cài Node 22, Playwright 1.64.0 + Chromium cùng bản container CPU (Chrome for Testing 156.0.8078.4),
# Vulkan/EGL, three.js. Không cài gì cần khoá. Dùng: bash 1_cai_dat_gpu.sh <gpu-thu.tar.zst>
set -euo pipefail
PK=$1; H=$HOME/gpu-thu; mkdir -p "$H"; zstd -dc "$PK" | tar -x -C "$H"
nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv | tee "$H/nvidia.txt"
sudo apt-get update -qq && sudo apt-get install -y -qq vulkan-tools libvulkan1 libegl1 libgl1 mesa-utils curl zstd python3-venv >/dev/null
# Container (RunPod/Vast): cần NVIDIA_DRIVER_CAPABILITIES chứa 'graphics' (hoặc 'all'), nếu không Vulkan/EGL của NVIDIA không có (tài liệu NVIDIA container toolkit)
echo "NVIDIA_DRIVER_CAPABILITIES=${NVIDIA_DRIVER_CAPABILITIES:-<không đặt>}" | tee -a "$H/nvidia.txt"
vulkaninfo --summary 2>&1 | grep -E "deviceName|driverName|apiVersion" | tee -a "$H/nvidia.txt" || echo "vulkaninfo LỖI" | tee -a "$H/nvidia.txt"
command -v node >/dev/null || { curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash - >/dev/null; sudo apt-get install -y -qq nodejs >/dev/null; }
mkdir -p "$H/pw" && cd "$H/pw" && npm init -y >/dev/null && npm i -s playwright@1.64.0 >/dev/null && npx playwright install --with-deps chromium chromium-headless-shell >/dev/null
cd "$H/repo/design/cong3/shared" && npm ci --silent
python3 -m venv "$H/py" && "$H/py/bin/pip" -q install numpy pillow opencv-python-headless
echo "CÀI XONG — tiếp: bash $H/repo/research-gpu/thu-gpu/2_chay_thu.sh"
