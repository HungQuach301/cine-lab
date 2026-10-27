#!/bin/bash
# BAN-CUOI-T4-B2a · chuỗi nền (một vòng nặng một lúc, P = 2):
#   giai đoạn "thu": khung thử máy B1-Q1 (960×540, 3 phương án pitch + máy cũ) + tấm E-M01 (tĩnh spp 24 + mặt nạ 1/2/3e, 2304×1296)   (dung_bc.py)
#   giai đoạn "sx":  dựng 1080p theo viec-dung.json (dung_b2a.py: mỗi shot → xong_b2a.sh → LFS → đẩy) — M00, H1-01h, rồi theo bảng; E-M01-tl (lớp (a)-E 3D của thử E, xong: false) xen ngay sau M01
#   bash scripts/k2ldn/bc/chuoi_b2a.sh thu|sx
set -o pipefail
cd "$(dirname "$0")/../../.."; export LDN_DATA=/var/tmp/ldn BC_R=/var/tmp/bc/r; PY=/opt/cine/bin/python; V=channel-k2/k2c-t4-02/ban-cuoi/may/b2a
t() { echo "== $(date -u +%H:%M:%S) $*"; }
case $1 in
thu) t THU-MAY; $PY scripts/k2ldn/bc/dung_bc.py 2 $V/viec-thu-may.json
     t THU-E;   $PY scripts/k2ldn/bc/dung_bc.py 2 $V/viec-e.json E-M01 E-M01-m1 E-M01-m2 E-M01-m3e
     t SOI;     $PY scripts/k2ldn/bc/dung_bc.py 2 $V/viec-soi.json
     t CHUOI-B2a-THU-XONG ;;
sx)  t SX; $PY scripts/k2ldn/bc/dung_b2a.py 2 $V/viec-dung.json; [ -f /var/tmp/bc/DUNG-B2a ] && { t "DỪNG: $(cat /var/tmp/bc/DUNG-B2a)"; exit 9; }
     t CHUOI-B2a-XONG ;;
esac
