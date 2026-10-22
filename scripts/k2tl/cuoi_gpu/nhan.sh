#!/usr/bin/env bash
# BAN-CUOI-T3 (việc 2) · NHẬN đoạn Cycles GPU: EXR (half) của pod → chỉnh màu bằng CHÍNH đường ống k2v (design/pt/cpu/nc_exr.py + nc_grade.js: ACES + LUT A + V6 + hạt — như NC-GPU)
#   → PNG → THAY khung cảnh đinh 1080p (jpg q95) của shot (bản A giữ ở <dir>/goc-gpu/). Không ghép A↔B trong một cú máy: mọi khung của đoạn là Cycles.
#   bash nhan.sh <doan n29|h2t> <khóa cảnh anim_N2_9|anim_H2T> <khung đầu> <khung cuối>
set -euo pipefail
REPO=$(cd "$(dirname "$0")/../../.." && pwd); export K2TL_CACHE=${K2TL_CACHE:-/var/tmp/cine-out/k2tl-cache} NC_DESIGN=$REPO/design NC_SCRIPTS=$REPO/scripts/k2tl
D=$1; K=$2; A=$3; B=$4; G=/var/tmp/cine-out/cuoi-gpu; IN=$G/exr/$D; PNG=$G/png/$D; mkdir -p $PNG; CPU=$REPO/design/pt/cpu
HD=$(/opt/cine/bin/python -c "import json;print(json.load(open('/var/tmp/cine-out/k2c-t3-cuoi/heroes.json'))['$K']['dir'])")
for f in $(seq $A $B); do test -s $IN/$(printf %05d $f).exr || { echo "THIẾU EXR $f"; exit 3; }; done
T=$G/f32-$$; ls $IN/*.exr | split -l 24 - $T-l-
for L in $T-l-*; do rm -rf $T; /opt/cine/bin/python $CPU/nc_exr.py $(cat $L) --out $T > /dev/null
  node $CPU/nc_grade.js --scene t3tl --opt "$(cat $G/opt/$D.json)" --in $T --out $PNG --w 1920 --h 1080 2>&1 | tail -1; rm -rf $T $L; done
mkdir -p $HD/goc-gpu
for f in $(seq $A $B); do n=$(printf %05d $f); test -s $PNG/$n.png || { echo "THIẾU PNG $f"; exit 4; }
  [ -f $HD/goc-gpu/$n.jpg ] || cp $HD/$n.jpg $HD/goc-gpu/$n.jpg
  /opt/cine/bin/python -c "from PIL import Image;Image.open('$PNG/$n.png').convert('RGB').save('$HD/$n.jpg',quality=95)"; done
echo "NHAN-XONG $D $A-$B → $HD"
