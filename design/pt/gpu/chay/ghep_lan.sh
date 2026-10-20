#!/usr/bin/env bash
# ghep_lan.sh [grade|ghep] — cú lặn Cycles GPU: chỉnh màu (đường ống k2v, như NC-CPU) các EXR chưa có PNG → $G/dive-png; ghép master 1080p24 (x264 CRF 14, ngoài git)
#  + bản xem 960×540 ≤ 5 MB trong git (reports/nc-gpu/lan/). Không ghép A↔B: 480/480 khung là Cycles GPU.
. /home/user/cine-lab/design/pt/gpu/chay/env.sh; mkdir -p $G/dive-png; R=/home/user/cine-lab/reports/nc-gpu/lan; mkdir -p $R
if [ "${1:-grade}" = grade ]; then T=$G/dive-moi; rm -rf $T; mkdir -p $T
  for e in $G/dive-exr/[0-9]*.exr; do b=$(basename $e .exr); [ -f $G/dive-png/$b.png ] || ln -s $e $T/; done
  n=$(ls $T | wc -l); [ $n -gt 0 ] && DIVE=1 $GPU/chay/grade.sh $T $G/dive-png > /dev/null 2>&1; echo "chinh mau $n"; rm -rf $T; fi
if [ "$1" = ghep ]; then
  ffmpeg -v error -y -framerate 24 -i $G/dive-png/%05d.png -c:v libx264 -preset slow -crf 14 -pix_fmt yuv420p /var/tmp/cine-out/ncg/ncg-lan-1080p-master.mp4
  ffmpeg -v error -y -i /var/tmp/cine-out/ncg/ncg-lan-1080p-master.mp4 -vf scale=960:540:flags=lanczos -c:v libx264 -preset slow -b:v 1700k -maxrate 2200k -bufsize 4000k -pix_fmt yuv420p -movflags +faststart $R/ncg-lan-xem.mp4
  ls -la /var/tmp/cine-out/ncg/ncg-lan-1080p-master.mp4 $R/ncg-lan-xem.mp4; sha256sum /var/tmp/cine-out/ncg/ncg-lan-1080p-master.mp4 $R/ncg-lan-xem.mp4; fi
