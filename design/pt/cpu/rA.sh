#!/usr/bin/env bash
# rA.sh <gate-key> <outdir> <W> <H> [nc-json]  — dựng 1 khung cổng bằng cảnh ncA (hoặc t3tl nếu NC=t3)
S=/tmp/claude-0/-home-user-cine-lab/2dbfdc7c-f7a1-5d76-9f3b-17c2d1dee62e/scratchpad; export K2TL_CACHE=/var/tmp/cine-out/k2tl-cache
K=$1; O=$2; W=${3:-960}; H=${4:-540}; NCJ=${5:-'{}'}; SCN=${SCN:-../nc/ncA}
read SHOT T < <(/opt/cine/bin/python -c "import json;g=[x for x in json.load(open('$S/gates.json')) if x['k']=='$K'][0];print(g['shot'],g['t'])")
F=$(/opt/cine/bin/python -c "print(round($T*24))")
OPT=$(/opt/cine/bin/python -c "import json,sys;o=json.load(open('$S/shots/$SHOT.json'));o['nc']=json.loads(sys.argv[1]);print(json.dumps(o))" "$NCJ")
node $S/v7b/scripts/k2tl/render.js --scene $SCN --pack gib --opt "$OPT" --only $F --override '[{"noText":true}]' --tech '{"spp":4}' --w $W --h $H --out $O 2>&1 | grep -v "^\[page\] \[\.WebGL\|GPU stall" | cut -c1-600 | tail -${TAILN:-6}
