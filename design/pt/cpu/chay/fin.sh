. /tmp/claude-0/-home-user-cine-lab/2dbfdc7c-f7a1-5d76-9f3b-17c2d1dee62e/scratchpad/env.sh
date; bash $S/diveA.sh 300:336 > $S/log/diveA300.log 2>&1; tail -1 $S/log/diveA300.log
# đo chuỗi máy rảnh: cùng shot C5, 48 khung, spp 2 — t3tl (V7B) vs ncA (+ nướng)
for SC in t3tl ../nc/ncA; do OPT=$(/opt/cine/bin/python -c "import json;o=json.load(open('$S/shots/v7b_C5.json'));o['nc']={'bake':'b1782'};print(json.dumps(o))")
node $S/v7b/scripts/k2tl/render.js --scene $SC --pack gib --opt "$OPT" --from 0 --to 48 --override '[{"noText":true}]' --tech '{"spp":2}' --w 1920 --h 1080 --out $O/seq-$(basename $SC) 2>&1 | grep s_per_frame; done
date; $S/gatesBC.sh ceevee2 eevee 32 cang toan-canh > $S/log/ceevee2.log 2>&1; cat $S/log/ceevee2.log
date; $S/gatesBC.sh bdep cycles 128 cang toan-canh > $S/log/bdep.log 2>&1; cat $S/log/bdep.log
date; bash $S/gradeB.sh; date; echo FIN-XONG
