#!/bin/bash
# BAN-CUOI-T4-A · chuỗi 3: chờ chuỗi 2 (PGID /var/tmp/bc/pgid_chuoi2) → dựng viec-xtra2.json (máy H5-02b/H5-02s sửa lần 2) P = 2.
cd "$(dirname "$0")/../../.."; export LDN_DATA=/var/tmp/ldn
while kill -0 "$(cat /var/tmp/bc/pgid_chuoi2)" 2>/dev/null; do sleep 15; done
/opt/cine/bin/python scripts/k2ldn/bc/dung_bc.py 2 channel-k2/k2c-t4-02/ban-cuoi/may/viec-xtra2.json; echo "== CHUOI-3-XONG"
