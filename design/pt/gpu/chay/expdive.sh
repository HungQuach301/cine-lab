#!/usr/bin/env bash
# expdive.sh — hình học cú lặn (đặc tả design/pt/cpu/dive-opt.json, KHÔNG đổi) xuất ở các khung mốc: 6 khung/lần trong timelapse 0–131 (nhà mọc theo năm), 12 khung/lần sau đó.
#  Mỗi bản xuất phục vụ các khung [mốc, mốc kế) — máy, nắng/trăng, trời, khói/lửa vẫn theo TỪNG khung (cam.json, lf/<khung>.json). → $G/dive/exp/d-<khung>
. /home/user/cine-lab/design/pt/gpu/chay/env.sh; mkdir -p $G/dive/exp
OPT=$(/opt/cine/bin/python -c "import json;o=json.load(open('$S/shots/dive.json'));o['nc']={};print(json.dumps(o))")
KEYS=${KEYS:-$( (seq 0 6 131; seq 132 12 479) | tr '\n' ' ')}
for F in $KEYS; do D=$G/dive/exp/d-$(printf %05d $F); [ -f $D/manifest.json ] && continue
  echo -n "$F "; node $GPU/gpu_export.js --scene ../nc/ncA --opt "$OPT" --f $F --far ${FAR:-7000} --nopass --w 1920 --h 1080 --out $D 2>&1 | tail -1; done
