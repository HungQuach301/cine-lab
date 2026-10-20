#!/usr/bin/env bash
# keo_lan.sh — kéo dần EXR cú lặn đã xong từ pod về $G/dive-exr (bỏ qua tệp đã có), dừng khi pod báo POD-DIVE-XONG
. /home/user/cine-lab/design/pt/gpu/chay/env.sh; P="/opt/cine/bin/python $GPU/pod.py"; mkdir -p $G/dive-exr; PFX=${PFX:-}
while true; do
  L=$($P ls out/dive 2>/dev/null); done_=$($P run 'grep -c POD-DIVE-XONG /w/dive.log' --cho 2>/dev/null | sed -n 2p)
  for f in $(echo "$L" | python3 -c "import json,sys;print(' '.join(x[0] for x in json.load(sys.stdin) if x[0].endswith('.exr') or x[0].endswith('.json')))" 2>/dev/null); do
    [ -f $G/dive-exr/$f ] || [ -f $G/dive-exr/$PFX$f ] || { sleep 1; T=$f; [[ $f == nc-* ]] && T=$PFX$f; $P get out/dive/$f $G/dive-exr/$T > /dev/null 2>&1 || rm -f $G/dive-exr/$T; }; done
  echo "$(date -u +%H:%M) $(ls $G/dive-exr/*.exr 2>/dev/null | wc -l)"
  [ "$done_" = "1" ] && break; sleep 240; done
