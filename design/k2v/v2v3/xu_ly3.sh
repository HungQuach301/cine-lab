#!/usr/bin/env bash
# xu_ly3.sh <clip> <chế độ A|B|B2> [n=81] — kéo từ pod (kiểm đủ khung), ghép (B/B2: dán lại nguồn trên vùng giữ), đo, tờ so
set -e
c=$1; m=$2; n=${3:-81}; B=/var/tmp/cine-out/v2v3; R=/home/user/cine-lab/design/k2v
/opt/cine/bin/python -I $R/v2v3/keo3.py ra/$c-$m $B/ra/$c-$m $n
/opt/cine/bin/python -I $R/v2v3/ghep3.py ra $B/ctrl/$c $B/ra/$c-$m $B/vid/$c-$m $([ "$m" = A ] || echo --b)
if [ "$n" = 81 ]; then $R/v2v3/do3.sh $c $m; /opt/cine/bin/python -I $R/v2v/to_so.py --src $B/vid/$c-nguon.mp4 --out $B/vid/$c-$m.mp4 --nhan nguon $m --khung 0 40 80 --png $B/to-so/to-so-$c-$m.png; fi
