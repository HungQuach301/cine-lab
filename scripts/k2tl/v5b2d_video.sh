#!/usr/bin/env bash
# V5b-2d · VIDEO THỬ 540p (≤ 15 MB, ngoài LFS): các cảnh 3D 13/9/1782 theo THỨ TỰ THỜI GIAN (C2-5): vịnh 09:05→10:27 (cảng → hero King's Bastion → reveal pin nổi)
#  → eo đất 10:32 → toàn cảnh 10:40 → phố (sáng) → bờ + chiến sự 17:13. Dựng thẳng 960×540 (có lớp chữ của trang tl), cắt thẳng giữa cảnh, không tiếng.
#  SM2 (kết "Oct 1782") KHÔNG hoà vào cảnh 13/9: ở phim đặt SAU cảnh bờ 17:13 (đổi thứ tự) — đoạn thử này chỉ gồm cảnh 3D.
#  bash scripts/k2tl/v5b2d_video.sh <thư mục ra> [J=2 tiến trình song song]
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd); O=${1:-/var/tmp/cine-out/v5b2d/video}; J=${J:-2}; mkdir -p $O
export K2TL_CACHE=${K2TL_CACHE:-/var/tmp/cine-out/k2tl-cache} K2TL_GL=${K2TL_GL:-llvmpipe}
SC="vinh1782 eo1782 toan1782 pho1782 bo1782"
for s in $SC; do while [ $(jobs -rp | wc -l) -ge $J ]; do sleep 2; done
  node $ROOT/scripts/k2tl/render.js --scene $s --pack gib --w 960 --h 540 --out $O/$s > $O/$s.log 2>&1 & done; wait
L=$O/list.txt; : > $L
for s in $SC; do ffmpeg -v error -y -framerate 24 -i $O/$s/%05d.jpg -c:v libx264 -preset slow -crf 23 -pix_fmt yuv420p $O/$s.mp4; echo "file '$O/$s.mp4'" >> $L; done
ffmpeg -v error -y -f concat -safe 0 -i $L -c copy $O/v5b2d-t-540p.mp4
ls -la $O/v5b2d-t-540p.mp4; ffprobe -v error -show_entries format=duration -of csv=p=0 $O/v5b2d-t-540p.mp4
