#!/usr/bin/env bash
# V5b-2d · gom kết quả vào reports/v5b2d/ (khung JPG 1080p q 90, tờ 6 khung, số đo, mặt nạ, video 540p ngoài LFS ≤ 15 MB).
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd); K=${1:-/var/tmp/cine-out/v5b2d/khung}; V=${2:-/var/tmp/cine-out/v5b2d/video}; D=$ROOT/reports/v5b2d
mkdir -p $D/khung $D/do
TEN=(x vay-ham cang-bo pho-day hero toan-canh bo-chien-su)
for k in 1 2 3 4 5 6; do
  /opt/cine/bin/python -c "from PIL import Image;import glob;Image.open(glob.glob('$K/sach-$k/*.jpg')[0]).save('$D/khung/d-$k-${TEN[$k]}.jpg',quality=90)"
  /opt/cine/bin/python -c "from PIL import Image;import glob;Image.open(glob.glob('$K/chu-$k/*.jpg')[0]).save('$D/khung/d-$k-${TEN[$k]}-chu.jpg',quality=90)"
  cp $K/mask-$k.json $D/do/mat-na-$k.json
done
/opt/cine/bin/python - <<EOF
from PIL import Image, ImageDraw
T=['vay-ham','cang-bo','pho-day','hero','toan-canh','bo-chien-su']; W,H=640,360; c=Image.new('RGB',(W*2,H*6),'black'); d=ImageDraw.Draw(c)
for i,t in enumerate(T):
    a=Image.open('$ROOT/reports/v5b2c/khung/v0-%d-%s.jpg'%(i+1, t if t!='bo-chien-su' else 'bien-chien-su')).resize((W,H)); b=Image.open('$D/khung/d-%d-%s.jpg'%(i+1,t)).resize((W,H))
    c.paste(a,(0,i*H)); c.paste(b,(W,i*H)); d.text((8,i*H+6),'V5b-2c · %d %s'%(i+1,t),fill='white'); d.text((W+8,i*H+6),'V5b-2d · %d %s'%(i+1,t),fill='white')
c.save('$D/khung/so-sanh-6-khung.jpg',quality=88)
EOF
[ -f $V/v5b2d-t-540p.mp4 ] && cp $V/v5b2d-t-540p.mp4 $D/khung/ || true
ls -la $D/khung | head -30
