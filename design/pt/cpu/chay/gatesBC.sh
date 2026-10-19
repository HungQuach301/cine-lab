#!/usr/bin/env bash
# gatesBC.sh <nhãn> <việc cycles|eevee> <spp> [gates…]  → $O/gate-<nhãn>/<g>.exr + .json ; chỉnh màu k2v → $O/gate-<nhãn>/png/<g>.png
. /tmp/claude-0/-home-user-cine-lab/2dbfdc7c-f7a1-5d76-9f3b-17c2d1dee62e/scratchpad/env.sh
LAB=$1; JOB=$2; SPP=$3; shift 3; D=$O/gate-$LAB; mkdir -p $D/png
for g in ${@:-vay-ham cang pho-day hero toan-canh bo-chien-su}; do
  T=1782; [ $g = hero ] && T=2026
  /opt/bpy/bin/python $CPU/nc_blend.py -- $O/exp/g-$g $JOB $D/$g.exr --topo $O/topo/$T-m1,$O/topo/$T-m4 --spp $SPP --res 1920x1080 --threads 4 2>&1 | grep "NC-RENDER\|Traceback\|Error:" | tail -2
  read SHOT TT < <(/opt/cine/bin/python -c "import json;g=[x for x in json.load(open('$S/gates.json')) if x['k']=='$g'][0];print(g['shot'],g['t'])")
  F=$(/opt/cine/bin/python -c "print(round($TT*24))"); rm -rf $D/f32; /opt/cine/bin/python $CPU/nc_exr.py $D/$g.exr --out $D/f32 > /dev/null; mv $D/f32/$g.f32 $D/f32/$(printf %05d $F).f32
  OPT=$(/opt/cine/bin/python -c "import json;o=json.load(open('$S/shots/$SHOT.json'));o['nc']={};print(json.dumps(o))")
  node $CPU/nc_grade.js --scene ../nc/ncA --opt "$OPT" --in $D/f32 --out $D/f32 --w 1920 --h 1080 2>&1 | tail -1
  mv $D/f32/$(printf %05d $F).png $D/png/$g.png; rm -rf $D/f32
done
