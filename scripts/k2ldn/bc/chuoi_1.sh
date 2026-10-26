#!/bin/bash
# BAN-CUOI-T4-A · chuỗi nền 1 (một vòng nặng một lúc): chờ du_lieu.sh (PGID trong /var/tmp/bc/pgid_dulieu) → hình học look3d + look3e (hinh_hoc_e.py)
#   → nướng lightmap trên look3d các mốc → dựng việc E, P1, mẫu, B, ảnh đầu M-d (dung_bc.py P=2).   setsid nohup bash scripts/k2ldn/bc/chuoi_1.sh > /var/tmp/bc/log/chuoi_1.log 2>&1 &
set -o pipefail
cd "$(dirname "$0")/../../.."
export LDN_DATA=/var/tmp/ldn; PY=/opt/cine/bin/python; M=channel-k2/k2c-t4-02/ban-cuoi/may
t() { echo "== $(date -u +%H:%M:%S) $*"; }
while kill -0 "$(cat /var/tmp/bc/pgid_dulieu)" 2>/dev/null; do sleep 15; done
t HINH-E; [ -s $LDN_DATA/look3e/ten.json ] || $PY scripts/k2ldn/bc/hinh_hoc_e.py || exit 2
for y in 1666.6 1700.5 1711.5 1938.5 1940.98 1975.5 2026.7 1667.3 1955.5; do t NUONG3D $y
  [ -s $LDN_DATA/look3d/bake_$y.png ] || LDN_LOOK=look3d /opt/bpy/bin/python scripts/k2ldn/nuong_look.py $y $LDN_DATA/look3d/bake_$y.png --box 530800,179700,534000,182000 || echo "LỖI nướng $y"; done
for g in md e p1 b mau etl; do t DUNG $g; $PY scripts/k2ldn/bc/dung_bc.py 2 $M/viec-$g.json; done
t CHUOI-1-XONG
