#!/bin/bash
# BAN-CUOI-T4-B1 · chờ hình học (hinh_hoc_b1.py, PID trong /var/tmp/bc/pid_hinh) → nướng lightmap look3d theo mốc, thứ tự ưu tiên (mẫu/soi trước, rồi HỒI 1 + HỒI 3).
#   setsid nohup bash scripts/k2ldn/bc/nuong_b1.sh > /var/tmp/bc/log/nuong_b1.log 2>&1 &
set -o pipefail
cd "$(dirname "$0")/../../.."
export LDN_DATA=${LDN_DATA:-/var/tmp/ldn}
while kill -0 "$(cat /var/tmp/bc/pid_hinh)" 2>/dev/null; do sleep 15; done
[ -s $LDN_DATA/look3d/nid.f32 ] || { echo "THIẾU hình học look3d"; exit 2; }
for y in ${NAM:-1666.6 1938.5 2026.7 1711.5 1940.98 1667.3 1700.5 1800.5 1860.5 1900.5}; do echo "== $(date -u +%H:%M:%S) NUONG3D $y"
  [ -s $LDN_DATA/look3d/bake_$y.png ] || LDN_LOOK=look3d /opt/bpy/bin/python scripts/k2ldn/nuong_look.py $y $LDN_DATA/look3d/bake_$y.png --box 530800,179700,534000,182000 | tail -2 || echo "LỖI nướng $y"; done
echo "== $(date -u +%H:%M:%S) NUONG-B1-XONG"
