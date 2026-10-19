#!/usr/bin/env bash
. /tmp/claude-0/-home-user-cine-lab/2dbfdc7c-f7a1-5d76-9f3b-17c2d1dee62e/scratchpad/env.sh
for g in ${GATES:-vay-ham cang pho-day hero toan-canh bo-chien-su}; do
read SHOT T < <(/opt/cine/bin/python -c "import json;g=[x for x in json.load(open('$S/gates.json')) if x['k']=='$g'][0];print(g['shot'],g['t'])")
F=$(/opt/cine/bin/python -c "print(round($T*24))"); OPT=$(/opt/cine/bin/python -c "import json;o=json.load(open('$S/shots/$SHOT.json'));o['nc']={};print(json.dumps(o))")
node $CPU/nc_export.js --scene ../nc/ncA --opt "$OPT" --f $F --far 7000 --nopass --w 1920 --h 1080 --out $O/exp/g-$g 2>&1 | tail -1
done
