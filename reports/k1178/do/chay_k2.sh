#!/bin/bash
# k2check trên animatic T4 v2 (video = nối 4 bản xem, SHA d4b5d486…) và bản cuối T3 (đầu vào như K-1.17.7 §1); $1 = nhãn phiên bản, $2 = t4 | t3 | t4e
set -o pipefail; cd /home/user/cine-lab; O=/var/tmp/k1178/k2; mkdir -p $O
if [ "$2" = t4 ]; then E=/var/tmp/k1178/v2/channel-k2/k2c-t4-02/animatic2
  /opt/cine/bin/python checks/ll/k2check.py $E/episode.yaml --tl $E/timeline.json --master /var/tmp/k1178/anim-v2-xem-noi.mp4 --cap --no-asr \
    --json $O/k2check-$1-t4.json --md $O/k2check-$1-t4.md > /dev/null 2> $O/k2check-$1-t4.err
elif [ "$2" = t4e ]; then E=/var/tmp/k1178/v2e/channel-k2/k2c-t4-02/animatic2
  /opt/cine/bin/python checks/ll/k2check.py $E/episode.yaml --tl $E/timeline.json --master /var/tmp/k1178/anim-v2-xem-noi.mp4 --cap --no-asr \
    --json $O/k2check-$1-t4e.json --md $O/k2check-$1-t4e.md > /dev/null 2> $O/k2check-$1-t4e.err
else R=/var/tmp/k1178/t3/tam; C=$R/channel-k2/k2c-t3-01/cuoi
  /opt/cine/bin/python checks/ll/k2check.py $C/episode-k.yaml --tl $R/timeline.json --master /var/tmp/k1178/t3/k2-t3-v1-master.mp4 --cap --no-asr \
    --json $O/k2check-$1-t3.json --md $O/k2check-$1-t3.md > /dev/null 2> $O/k2check-$1-t3.err
fi
echo "XONG $1 $2 rc=$?" >> $O/xong.txt
