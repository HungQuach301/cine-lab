. /tmp/claude-0/-home-user-cine-lab/2dbfdc7c-f7a1-5d76-9f3b-17c2d1dee62e/scratchpad/env.sh
rm -f $O/diveB/*.exr; mkdir -p $O/diveB
/opt/bpy/bin/python $CPU/nc_blend.py -- $O/exp/dive-night cycles $O/diveB --topo $O/topo/1782-m1,$O/topo/1782-m4 --spp 12 --res 1920x1080 --threads 4 --night 1 --fires "$(cat $S/fires.json)" --smoke --anim $O/dive-cam.json --frames 216:348 --persist > $S/log/diveB.log 2>&1
$S/gatesBC.sh bdep cycles 128 > $S/log/bdep.log 2>&1
echo XONG >> $S/log/diveB.log
