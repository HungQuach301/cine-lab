#!/bin/bash
# CINE LAB — setup script cho môi trường cloud "cine-lab-av"
# Dán TOÀN BỘ nội dung file này vào ô "Setup script" của môi trường.
# Chạy với quyền root trên Ubuntu 24.04. Phải xong trong ~5 phút (giới hạn cache môi trường).
# Không tải model lớn ở đây (faster-whisper, ACE-Step): tải trong phiên, lần đầu.
set -uo pipefail
LOG=/var/log/cine-setup.log
exec > >(tee -a "$LOG") 2>&1
echo "== CINE setup start $(date -u +%FT%TZ)"

retry() { local n=0; until "$@"; do n=$((n+1)); [ $n -ge 3 ] && { echo "FAIL: $*"; return 1; }; echo "retry $n: $*"; sleep 5; done; }
export DEBIAN_FRONTEND=noninteractive

# 1) Gói hệ thống: ffmpeg, font, thư viện cho Blender (bpy) + Python 3.13 (bpy không có bản cho 3.12)
(
  { apt-get update -q || echo "WARN: apt-get update báo lỗi một nguồn phụ, vẫn tiếp tục"; } &&
  retry apt-get install -y -q --no-install-recommends software-properties-common ffmpeg sox mediainfo \
      fonts-noto-core fonts-liberation2 libgl1 libegl1 libxi6 libxkbcommon0 libsm6 libxrender1 libxxf86vm1 libxfixes3 &&
  # Ảnh VM trỏ python3 -> 3.11 (không có apt_pkg) nên add-apt-repository lỗi "No module named 'apt_pkg'".
  # Ảnh đã có sẵn nguồn deadsnakes + python3.13; chỉ thêm PPA khi thiếu, và gọi bằng python3.12 của hệ thống.
  if ! command -v python3.13 >/dev/null; then
    if ! ls /etc/apt/sources.list.d/ | grep -q deadsnakes; then
      retry /usr/bin/python3.12 /usr/bin/add-apt-repository -y ppa:deadsnakes/ppa && { apt-get update -q || true; }
    fi
    retry apt-get install -y -q python3.13 python3.13-venv
  fi &&
  python3.13 -m venv --help >/dev/null &&
  echo "OK_APT"
) &
P1=$!

# 2) Python chính (dùng python3 mặc định của VM)
(
  python3 -m venv /opt/cine &&
  retry /opt/cine/bin/pip install -q --upgrade pip &&
  retry /opt/cine/bin/pip install -q faster-whisper pyloudnorm numpy scipy soundfile librosa \
      opencv-python-headless pillow scenedetect elevenlabs requests jsonschema psutil &&
  echo "OK_PY"
) &
P2=$!

# 3) Playwright + Chromium (cần cdn.playwright.dev, playwright.download.prss.microsoft.com)
(
  mkdir -p /opt/pw && cd /opt/pw && npm init -y >/dev/null &&
  retry npm install -s playwright &&
  PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers retry npx -y playwright install chromium &&
  echo "OK_PW"
) &
P3=$!

wait $P1; R1=$?
# 4) Blender as a Python module (bpy) trong venv Python 3.13 riêng — sau khi apt xong
(
  command -v python3.13 >/dev/null && python3.13 -m venv /opt/bpy &&
  retry /opt/bpy/bin/pip install -q bpy &&
  echo "OK_BPY"
) &
P4=$!

wait $P2; R2=$?; wait $P3; R3=$?; wait $P4; R4=$?

# 5) three.js cho trang render (design/cong3/shared/node_modules — KHÔNG nằm trong git).
#    Luôn dùng `npm ci` theo package-lock.json (three 0.180.0, đúng mã integrity), không dùng `npm install`.
#    Setup script có thể chạy trước khi repo được clone: không thấy repo thì bỏ qua; verify.sh báo FAIL kèm lệnh chạy tay.
R5=skip
for REPO in "${CINE_REPO:-}" /home/user/cine-lab; do
  if [ -n "$REPO" ] && [ -f "$REPO/design/cong3/shared/package-lock.json" ]; then
    ( cd "$REPO/design/cong3/shared" && retry npm ci --no-audit --no-fund ) && R5=0 || R5=1
    break
  fi
done

# Biến môi trường cho mọi phiên
cat > /etc/profile.d/cine.sh <<'EOF'
export PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers
export CINE_PY=/opt/cine/bin/python
export CINE_BPY=/opt/bpy/bin/python
export HF_HOME=/opt/hf-cache
EOF
mkdir -p /opt/hf-cache && chmod 777 /opt/hf-cache

echo "== RESULT apt=$R1 py=$R2 playwright=$R3 bpy=$R4 three=$R5 (0 = OK)"
echo "== CINE setup end $(date -u +%FT%TZ)"
# Luôn thoát 0 để cache được lưu; lỗi từng phần do scripts/env/verify.sh phát hiện.
exit 0
