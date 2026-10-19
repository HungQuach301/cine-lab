. /tmp/claude-0/-home-user-cine-lab/2dbfdc7c-f7a1-5d76-9f3b-17c2d1dee62e/scratchpad/env.sh
/opt/bpy/bin/python $CPU/nc_blend.py -- $O/exp/1782-bake nuong $O/bake/b1782 --topo $O/topo/1782-m1,$O/topo/1782-m4 --box -3000,-3000,1000,3500 --bres 3 --spp 24 --fires "$(cat $S/fires.json)" --pack $K2TL_CACHE/scene/gib/pack 2>&1 | grep -E "NC-BAKE|Error|Traceback"
/opt/bpy/bin/python $CPU/nc_blend.py -- $O/exp/2026-bake nuong $O/bake/b2026 --topo $O/topo/2026-m1,$O/topo/2026-m4 --box -3000,-3000,1000,3500 --bres 3 --spp 24 --pack $K2TL_CACHE/scene/gib/pack 2>&1 | grep -E "NC-BAKE|Error|Traceback"
