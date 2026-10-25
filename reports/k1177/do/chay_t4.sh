#!/bin/bash
# k2check trên animatic T4 v1 (video = nối 3 bản xem, SHA 4263d29d…); $1 = nhãn phiên bản
set -o pipefail; cd /home/user/cine-lab; E=channel-k2/k2c-t4-02/animatic
/opt/cine/bin/python checks/ll/k2check.py $E/episode.yaml --tl $E/timeline.json --master /var/tmp/k1177/t4/anim-xem-noi.mp4 --cap --no-asr \
  --json /var/tmp/k1177/t4/k2check-$1-t4.json --md /var/tmp/k1177/t4/k2check-$1-t4.md > /dev/null 2> /var/tmp/k1177/t4/k2check-$1-t4.err
echo "XONG $1 rc=$?"
