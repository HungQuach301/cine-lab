#!/usr/bin/env bash
# NC-N2P · gọi Omni cho một clip: mã hoá khung nguồn → mp4 1280×720 24 fps (crf 17) → 2 biến thể lệnh (vừa, mạnh) qua omni_goi.py (chặn $18, dừng khi 402).
#   chay_omni.sh <khoá c1|c2|c4B|c4A> <f0> [biến thể…]
set -uo pipefail
K=$1; F0=$2; shift 2; VS=${*:-vua manh}; D=${K%[AB]}; [ "$K" = c4A ] || [ "$K" = c4B ] || D=$K
S=/var/tmp/n2p/src/$D; O=/var/tmp/n2p/omni; mkdir -p $O; R=/home/user/cine-lab/reports/nc-n2p
IN=$O/$K-nguon.mp4
[ -s $IN ] || ffmpeg -v error -y -start_number $F0 -framerate 24 -i $S/rgb/%05d.jpg -frames:v 240 -c:v libx264 -preset slow -crf 17 -pix_fmt yuv420p $IN
sha256sum $IN
for v in $VS; do P=$R/omni/lenh/$K-$v.txt; [ -f $P ] || P=$R/omni/lenh/${K%A}B-$v.txt
  /opt/cine/bin/python -I $R/ma/omni_goi.py --video $IN --prompt-file $P --out $O/$K-$v.mp4 --tag $K-$v || echo "LỖI $K-$v"
done
echo OMNI-XONG $K
