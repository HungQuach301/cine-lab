#!/bin/bash
# k2check trên bản cuối T3 (đầu vào như K-1.17.6 §9); $1 = nhãn phiên bản
set -o pipefail; cd /home/user/cine-lab; R=/var/tmp/k1177/t3/tam; C=$R/channel-k2/k2c-t3-01/cuoi
/opt/cine/bin/python checks/ll/k2check.py $C/episode-k.yaml --tl $R/timeline.json --master /var/tmp/k1177/t3/k2-t3-v1-master.mp4 --cap --no-asr \
  --json /var/tmp/k1177/t3/k2check-$1-t3.json --md /var/tmp/k1177/t3/k2check-$1-t3.md > /dev/null 2> /var/tmp/k1177/t3/k2check-$1-t3.err
echo "XONG $1 rc=$?"
