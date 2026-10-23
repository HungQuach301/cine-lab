#!/bin/bash
# LOOK-T4 · dựng 4 clip 8 s 640×360 (biến thể A) + đo cú máy + mp4 ≤ 5 MB → reports/look-t4/clip/. P ≤ 2; chờ RAM ≥ 5 GB.
set -o pipefail
cd "$(dirname "$0")/../.."
D=${LDN_DATA:-/var/tmp/ldn}; R=$D/look/r; mkdir -p "$R" reports/look-t4/clip reports/look-t4/do
P=${1:-2}; shift || true; MS=${*:-"M1 M2 M3 M4"}
mot() { local m=$1 j=channel-k2/k2c-t4-02/look/may/clip-$1.json
  [ -s reports/look-t4/clip/clip-$m-A.mp4 ] && return 0
  LDN_DATA=$D node scripts/k2ldn/render_look.js --shot $j --out $R/clip-$m > $R/clip-$m.log 2>&1 || { echo "LỖI clip $m"; return 1; }
  /opt/cine/bin/python scripts/k2ldn/look_clip.py $R/clip-$m reports/look-t4/clip/clip-$m-A.mp4 reports/look-t4/do/clip-$m.json --hero "$(/opt/cine/bin/python -c "import json;print(','.join(map(str,json.load(open('$j'))['hero_EN'])))")" && echo "XONG clip $m"; }
for m in $MS; do while [ "$(jobs -rp | wc -l)" -ge "$P" ]; do sleep 5; done
  while [ "$(free -m | awk '/Mem:/{print $7}')" -lt 5000 ]; do sleep 10; done; mot $m & sleep 20; done
wait; echo "LOOK-CLIP XONG"
