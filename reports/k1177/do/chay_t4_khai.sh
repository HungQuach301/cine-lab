#!/bin/bash
# k2check trên animatic T4 v1 với episode.yaml KHAI THỬ tham số gói tiết kiệm (bản sao ngoài channel-k2, symlink tệp gốc); $1 = nhãn
set -o pipefail; cd /home/user/cine-lab; K=/var/tmp/k1177/t4/k2c/animatic
/opt/cine/bin/python checks/ll/k2check.py $K/episode.yaml --tl $K/timeline.json --master /var/tmp/k1177/t4/anim-xem-noi.mp4 --cap --no-asr \
  --json /var/tmp/k1177/t4/k2check-$1-t4-khai.json --md /var/tmp/k1177/t4/k2check-$1-t4-khai.md > /dev/null 2> /var/tmp/k1177/t4/k2check-$1-t4-khai.err
echo "XONG $1 rc=$?"
