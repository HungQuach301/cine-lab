#!/bin/bash
# LOOK-T4 · dựng lại toàn bộ sau khi đổi hình học: chờ nướng (PID trong /var/tmp/ldn/log/nuong.pid) → 24 khung → tờ mù + bảng đo → clip + đo 1080p + T3
set -o pipefail
cd /home/user/cine-lab
while ps -p $(cat /var/tmp/ldn/log/nuong.pid) >/dev/null 2>&1; do sleep 5; done
rm -rf /var/tmp/ldn/look/r /var/tmp/ldn/look/khung-abc /var/tmp/ldn/look/do-abc reports/look-t4/clip reports/look-t4/khung reports/look-t4/do/M*-[XYZ].json reports/look-t4/do/clip-M*.json
SPP=16 bash scripts/k2ldn/look_chay.sh 2 || echo "LỖI chạy"
/opt/cine/bin/python scripts/k2ldn/look_to.py && /opt/cine/bin/python scripts/k2ldn/look_bang.py > /var/tmp/ldn/r/bang.md
bash scripts/k2ldn/look_sau.sh
echo "LAI-HET XONG"
