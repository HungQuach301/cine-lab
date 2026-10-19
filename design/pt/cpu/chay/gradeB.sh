. /tmp/claude-0/-home-user-cine-lab/2dbfdc7c-f7a1-5d76-9f3b-17c2d1dee62e/scratchpad/env.sh
mkdir -p $O/diveB-png; ls $O/diveB/*.exr | split -l 20 - /tmp/claude-0/-home-user-cine-lab/2dbfdc7c-f7a1-5d76-9f3b-17c2d1dee62e/scratchpad/gB_
for L in /tmp/claude-0/-home-user-cine-lab/2dbfdc7c-f7a1-5d76-9f3b-17c2d1dee62e/scratchpad/gB_*; do rm -rf $O/f32; /opt/cine/bin/python $CPU/nc_exr.py $(cat $L) --out $O/f32 >/dev/null
node $CPU/nc_grade.js --scene ../nc/ncA --opt "$(cat $S/shots/dive.json)" --in $O/f32 --out $O/diveB-png --w 1920 --h 1080 2>&1 | tail -1; rm -rf $O/f32 $L; done
