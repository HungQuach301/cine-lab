. /tmp/claude-0/-home-user-cine-lab/2dbfdc7c-f7a1-5d76-9f3b-17c2d1dee62e/scratchpad/env.sh
OPT=$(/opt/cine/bin/python -c "import json;o=json.load(open('$S/shots/dive.json'));o['nc']={'bake':'b1782','fire':{'wY':[1782.70046,1782.703082],'k':1.5}};print(json.dumps(o))")
RS=${*:-"0:228 336:480"}; for R in $RS; do a=${R%:*}; b=${R#*:}
node $S/v7b/scripts/k2tl/render.js --scene ../nc/ncA --pack gib --opt "$OPT" --from $a --to $b --override '[{"noText":true}]' --tech '{"spp":2}' --w 1920 --h 1080 --out $O/diveA-$a 2>&1 | grep -v "^\[page\]" | tail -2
done
