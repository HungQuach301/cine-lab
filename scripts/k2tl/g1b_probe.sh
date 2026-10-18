#!/usr/bin/env bash
# G1b T3 · dựng thử 1 khung giữa (hoặc khung chỉ định) cho mọi cảnh trong heroes.json của tập → soi bố cục trước khi dựng cả tập. Ra <out>/<khoá>/NNNNN.jpg + probe.log
#   bash scripts/k2tl/g1b_probe.sh <heroes.json> <out> [P=2] [W=960 H=540] [FR=mid|0|end] [ONLY="khoá1 khoá2"]
set -u
REPO=$(cd "$(dirname "$0")/../.." && pwd); HJ=$1; OUT=$2; P=${P:-2}; W=${W:-960}; H=${H:-540}; FR=${FR:-mid}
export K2TL_CACHE=${K2TL_CACHE:-/var/tmp/cine-out/k2tl-cache}; mkdir -p $OUT
/opt/cine/bin/python -c "
import json,sys; H=json.load(open('$HJ')); only='${ONLY:-}'.split()
for k,v in H.items():
  if only and k not in only: continue
  if v['hero'].startswith('footage/'): continue
  n=int(v['opt'].get('dur', v['dur'])*24); f={'mid':n//2,'0':0,'end':max(0,n-2)}['$FR']
  print(k, v['hero'], v['dur'], f, json.dumps(v['opt'],separators=(',',':')))" > $OUT/list.txt
while read -r k h d f opt; do
  while [ $(jobs -rp | wc -l) -ge $P ]; do wait -n; done
  ( t0=$(date +%s); nice -n 5 node $REPO/scripts/k2/hero.js --hero $h --variant a --dur $d --w $W --h $H --spp 2 --opt "$opt" --out $OUT/$k --only $f 2>$OUT/$k.err; rc=$?
    echo "$k rc=$rc $(( $(date +%s) - t0 ))s $(grep -m1 -E 'pageerror|LỖI|Error' $OUT/$k.err | cut -c1-200)" >> $OUT/probe.log ) &
done < $OUT/list.txt
wait; echo XONG >> $OUT/probe.log
