#!/usr/bin/env bash
# TIEN-KY-T4 · tờ so T1 — màn chia đôi cùng cú máy: TRÁI cách A (atlas, llvmpipe) · PHẢI Cycles GPU (miền thể tích đơn); ngày 5 s + đêm 5 s; 640×360; LUT kênh v030.
#   t1_so.sh <ra.mp4>    (khung: /var/tmp/ldn/t1/a-{ngay,dem}, /var/tmp/ldn/gpu/ra/{ngay,dem})
set -euo pipefail
REPO=$(cd "$(dirname "$0")/../.." && pwd); LUT=$REPO/channel-k2/k2c-t3-01/mau/k2c-t3-kenh-v030.cube; OUT=$1; T=$(mktemp -d)
F=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf
for D in ngay dem; do
  ffmpeg -nostdin -loglevel error -y -framerate 24 -i /var/tmp/ldn/t1/a-$D/%05d.jpg -framerate 24 -i /var/tmp/ldn/gpu/ra/$D/%05d.jpg -filter_complex \
   "[0]scale=640:360,crop=320:360:0:0[a];[1]scale=640:360,crop=320:360:320:0[b];[a][b]hstack,lut3d=$LUT,drawbox=x=319:y=0:w=2:h=360:color=white@0.8:t=fill,\
drawtext=fontfile=$F:text='A atlas':x=8:y=8:fontsize=14:fontcolor=white:box=1:boxcolor=black@0.5,drawtext=fontfile=$F:text='Cycles GPU':x=w-tw-8:y=8:fontsize=14:fontcolor=white:box=1:boxcolor=black@0.5" \
   -frames:v 120 -c:v libx264 -crf 22 -pix_fmt yuv420p $T/$D.mp4
done
printf "file '%s'\nfile '%s'\n" $T/ngay.mp4 $T/dem.mp4 > $T/l.txt; ffmpeg -nostdin -loglevel error -y -f concat -safe 0 -i $T/l.txt -c copy "$OUT"; rm -rf $T; ls -l "$OUT"
