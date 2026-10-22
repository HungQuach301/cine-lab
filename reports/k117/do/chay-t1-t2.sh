#!/bin/bash
# chạy k2check T1/T2 với hai cây luật trên cùng đầu vào
D=/var/tmp/k117/t1t2; R=/home/user/cine-lab; BT=$R/checks/ll/fixtures/k1121/tl-gib20-v5b2a/bo-tl.json
for V in ${VS:-1161 117}; do
  C=/var/tmp/k117/c$V/checks
  /opt/cine/bin/python $C/ll/k2check.py $D/t1-episode.yaml --tl $D/t1-timeline.json --no-asr --json $D/t1-$V.json > $D/t1-$V.md 2>&1
  /opt/cine/bin/python $C/ll/k2check.py $D/t2l5-episode.yaml --tl $D/t2l5-timeline.json --no-asr --root /var/tmp/k117/t2root --bo-tl $BT --json $D/t2-$V.json > $D/t2-$V.md 2>&1
  echo "xong $V $(date -u +%H:%M:%S)"
done
