#!/usr/bin/env bash
# expg.sh — xuất 6 khung cổng (cảnh ncA, máy V7B) bằng gpu_export.js → $G/exp/g-<cổng>
. /home/user/cine-lab/design/pt/gpu/chay/env.sh; mkdir -p $G/exp
for g in ${GATES:-vay-ham cang pho-day hero toan-canh bo-chien-su}; do
read SHOT T < <(/opt/cine/bin/python -c "import json;g=[x for x in json.load(open('$CPU/gates.json')) if x['k']=='$g'][0];print(g['shot'],g['t'])")
F=$(/opt/cine/bin/python -c "print(round($T*24))"); OPT=$(/opt/cine/bin/python -c "import json;o=json.load(open('$S/shots/$SHOT.json'));o['nc']={};print(json.dumps(o))")
echo -n "$g "; node $GPU/gpu_export.js --scene ../nc/ncA --opt "$OPT" --f $F --far ${FAR:-7000} --nopass --w 1920 --h 1080 --out $G/exp/g-$g 2>&1 | tail -1
done
