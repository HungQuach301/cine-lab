#!/bin/bash
# (dung2.sh = dung.sh + biến PAGE: look2d cho máy thấp ≤ 60 m có lớp người/xe L3)
# ANIMATIC-T4 · hàng dựng 3D: mỗi tệp máy → $R/<shot>/%05d.jpg + log.json (render_look.js --page look2). P tiến trình, chờ RAM ≥ 5 GB, bỏ qua shot đã xong.
# log.json (log_may, K1174-D4) chép ngay vào git: channel-k2/k2c-t4-02/animatic/log-may/<shot>.json.gz
#   bash scripts/k2ldn/anim/dung.sh <P> <shot …>
set -o pipefail
cd "$(dirname "$0")/../../.."
P=$1; shift; R=${ANIM_R:-/var/tmp/anim/r}; M=channel-k2/k2c-t4-02/animatic/may; LG=channel-k2/k2c-t4-02/animatic/log-may; mkdir -p "$R" "$LG"
mot() { local k=$1
  [ -s "$R/$k/log.json" ] && { [ -s "$LG/$k.json.gz" ] || gzip -9 -c "$R/$k/log.json" > "$LG/$k.json.gz"; echo "ĐÃ CÓ $k"; return 0; }
  rm -rf "$R/$k"; LDN_DATA=${LDN_DATA:-/var/tmp/ldn} node scripts/k2ldn/render_look.js --shot $M/$k.json --out "$R/$k" --page ${PAGE:-look2} > "$R/$k.log" 2>&1 || { echo "LỖI $k"; return 1; }
  gzip -9 -c "$R/$k/log.json" > "$LG/$k.json.gz"; echo "XONG $k $(date -u +%H:%M) $(tail -1 $R/$k.log | cut -c1-40)"; }
for k in "$@"; do while [ "$(jobs -rp | wc -l)" -ge "$P" ]; do sleep 3; done
  while [ "$(free -m | awk '/Mem:/{print $7}')" -lt 5000 ]; do sleep 10; done; mot $k & sleep 5; done
wait; echo DUNG-XONG
