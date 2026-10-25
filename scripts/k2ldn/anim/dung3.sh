#!/bin/bash
# ANIMATIC-T4-V2 · hàng dựng 3D v3 (theo dung.sh/dung2.sh của ANIMATIC-T4): mỗi tệp máy animatic2/may/<shot>.json → $R/<shot>/%05d.jpg + log.json; trang theo trường "page" (look2 | look2d).
# P tiến trình, chờ RAM ≥ 5 GB; bỏ qua shot đã xong; log máy (K1174-D4) chép ngay vào git: animatic2/log-may/<shot>.json.gz
#   bash scripts/k2ldn/anim/dung3.sh <P> <shot …>
set -o pipefail
cd "$(dirname "$0")/../../.."
P=$1; shift; R=${ANIM_R:-/var/tmp/anim/r3}; M=channel-k2/k2c-t4-02/animatic2/may; LG=channel-k2/k2c-t4-02/animatic2/log-may; mkdir -p "$R" "$LG"
mot() { local k=$1; local pg; pg=$(/opt/cine/bin/python -c "import json;print(json.load(open('$M/$k.json')).get('page','look2'))")
  [ -s "$R/$k/log.json" ] && [ "$R/$k/log.json" -nt "$M/$k.json" ] && { [ -s "$LG/$k.json.gz" ] || gzip -9 -c "$R/$k/log.json" > "$LG/$k.json.gz"; echo "ĐÃ CÓ $k"; return 0; }
  rm -rf "$R/$k"; LDN_DATA=${LDN_DATA:-/var/tmp/ldn} node scripts/k2ldn/render_look.js --shot $M/$k.json --out "$R/$k" --page $pg > "$R/$k.log" 2>&1 || { echo "LỖI $k"; return 1; }
  gzip -9 -c "$R/$k/log.json" > "$LG/$k.json.gz"; echo "XONG $k $pg $(date -u +%H:%M) $(tail -1 $R/$k.log | cut -c1-40)"; }
for k in "$@"; do while [ "$(jobs -rp | wc -l)" -ge "$P" ]; do sleep 3; done
  while [ "$(free -m | awk '/Mem:/{print $7}')" -lt 5000 ]; do sleep 10; done; mot $k & sleep 5; done
wait; echo DUNG-XONG
