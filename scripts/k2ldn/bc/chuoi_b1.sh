#!/bin/bash
# BAN-CUOI-T4-B1 · chuỗi nền (một vòng nặng một lúc, P = 2): (1) khung "trước" (trang cũ) + P9 ngày/đêm + soi lại H2-09 + ảnh đầu Omni H5-02b/H5-02s (dung_bc.py)
#   → (2) shot nhỏ nhất (thử D-B1 LFS ngay) → (3) toàn bộ HỒI 1 + HỒI 3 + H3-05c (dung_b1.py: mỗi shot → xong_b1.sh → LFS → đẩy).
set -o pipefail
cd "$(dirname "$0")/../../.."; export LDN_DATA=/var/tmp/ldn BC_R=/var/tmp/bc/r; PY=/opt/cine/bin/python
t() { echo "== $(date -u +%H:%M:%S) $*"; }
t PRE; $PY scripts/k2ldn/bc/dung_bc.py 2 channel-k2/k2c-t4-02/ban-cuoi/may/b1/hang-pre.json
t LFS1; $PY scripts/k2ldn/bc/dung_b1.py 2 channel-k2/k2c-t4-02/ban-cuoi/may/b1/hang-lfs1.json; [ -f /var/tmp/bc/DUNG-B1 ] && { t "DỪNG: $(cat /var/tmp/bc/DUNG-B1)"; exit 9; }
t SANXUAT; $PY scripts/k2ldn/bc/dung_b1.py 2 channel-k2/k2c-t4-02/ban-cuoi/may/b1/hang-q2.json
t CHUOI-B1-XONG
