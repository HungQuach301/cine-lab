#!/bin/bash
# LOOK-T4-V2 · dựng danh sách máy V2 (look2.js): mỗi tên → khung JPG (spp $SPP) và/hoặc mặt nạ (MASK=1 lớp, 2 mã công trình). P tiến trình, chờ RAM ≥ 5 GB.
#   SPP=24 MASK=0|1|2 bash scripts/k2ldn/v2_chay.sh <P> <ra_thư_mục> <tên máy …>   (máy: channel-k2/k2c-t4-02/look/may-v2/<tên>.json)
set -o pipefail
cd "$(dirname "$0")/../.."
P=$1; R=$2; shift 2; mkdir -p "$R"; D=${LDN_DATA:-/var/tmp/ldn}; SPP=${SPP:-24}; MASK=${MASK:-0}; KHUNG=${KHUNG:-1}
mot() { local k=$1 j=channel-k2/k2c-t4-02/look/may-v2/$1.json
  if [ "$KHUNG" = 1 ] && [ ! -s "$R/$k/00000.jpg" ]; then LDN_DATA=$D node scripts/k2ldn/render_look.js --shot $j --out "$R/$k" --spp $SPP --page look2 > "$R/$k.log" 2>&1 || echo "LỖI $k"; fi
  if [ "$MASK" != 0 ] && [ ! -s "$R/$k-mask$MASK/00000.png" ]; then LDN_DATA=$D node scripts/k2ldn/render_look.js --shot $j --out "$R/$k-mask$MASK" --mask $MASK --page look2 > "$R/$k-mask$MASK.log" 2>&1 || echo "LỖI mặt nạ $k"; fi
  echo "XONG $k $(tail -1 $R/$k.log 2>/dev/null | cut -c1-60)"; }
for k in "$@"; do while [ "$(jobs -rp | wc -l)" -ge "$P" ]; do sleep 3; done
  while [ "$(free -m | awk '/Mem:/{print $7}')" -lt 5000 ]; do sleep 10; done; mot $k & sleep 8; done
wait; echo V2-CHAY-XONG
