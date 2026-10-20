#!/usr/bin/env bash
# do3.sh <clip c2|c4B|c1> <biến thể A|B|dc>  — đo bằng bộ đo NC-V2V (do_v2v.py, không sửa) + do_them3.py; f0 = khung tuyệt đối đầu cửa sổ (id/ đánh số tuyệt đối)
set -e
B=/var/tmp/cine-out/v2v3; R=/home/user/cine-lab/design/k2v; declare -A F0=([c2]=80 [c4B]=320 [c1]=344)
c=$1; v=$2; f0=${F0[$c]}; src=$B/vid/$c-nguon.mp4; out=$([ "$v" = dc ] && echo $B/vid/$c-nguon-dc.mp4 || echo $B/vid/$c-$v.mp4)
/opt/cine/bin/python -I $R/v2v/do_v2v.py --src $src --out $out --id $B/src/$c/id --f0 $f0 --json $B/do/$c-$v.json --label $c-$v > /dev/null
/opt/cine/bin/python -I $R/v2v3/do_them3.py --src $src --out $out --id $B/src/$c/id --f0 $f0 --json $B/do/$c-$v-them.json --label $c-$v
