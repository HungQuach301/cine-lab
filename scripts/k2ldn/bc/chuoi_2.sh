#!/bin/bash
# BAN-CUOI-T4-A · chuỗi nền 2: chờ chuỗi 1 (PGID /var/tmp/bc/pgid_chuoi1) xong → dựng viec-xtra.json (máy M-d sửa toạ độ, M00 góc lửa mới, timelapse B) P = 2.
cd "$(dirname "$0")/../../.."; export LDN_DATA=/var/tmp/ldn
while kill -0 "$(cat /var/tmp/bc/pgid_chuoi1)" 2>/dev/null; do sleep 15; done
echo "== $(date -u +%H:%M:%S) DUNG xtra"; /opt/cine/bin/python scripts/k2ldn/bc/dung_bc.py 2 channel-k2/k2c-t4-02/ban-cuoi/may/viec-xtra.json; echo "== CHUOI-2-XONG"
