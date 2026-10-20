#!/usr/bin/env bash
# theo3.sh: theo dõi /w/jobs/xong.jsonl trên pod; job nào xong thì xử lý (xu_ly3.sh) một lần; ghi /var/tmp/cine-out/v2v3/theo3.log
cd /home/user/cine-lab; L=/var/tmp/cine-out/v2v3/theo3.log; D=/var/tmp/cine-out/v2v3/da_xu_ly; touch $D
JOBS="c1-B g-hero-B c2-B c4B-A c2-B2 c1-A g-hero-A c4B-B2 g-vay-ham-B g-vay-ham-A c1-B2 g-bo-chien-su-B g-bo-chien-su-A $*"
while true; do
  X=$(/opt/cine/bin/python design/k2v/v2v3/pod3.py run 'cat /w/jobs/xong.jsonl' --cho 2>/dev/null)
  left=0
  for j in $JOBS; do
    grep -qx "$j" $D && continue; left=1
    if echo "$X" | grep -q "\"job\": \"$j\""; then
      c=${j%-*}; m=${j##*-}; n=81; case $c in g-*) n=17;; esac
      echo "$(date -u +%H:%M) xử lý $j" >> $L
      if design/k2v/v2v3/xu_ly3.sh $c $m $n >> $L 2>&1; then echo $j >> $D; echo "$(date -u +%H:%M) XONG $j" >> $L; else echo "$(date -u +%H:%M) LỖI $j" >> $L; fi
    fi
  done
  [ $left = 0 ] && { echo "$(date -u +%H:%M) HẾT" >> $L; break; }
  sleep 60
done
