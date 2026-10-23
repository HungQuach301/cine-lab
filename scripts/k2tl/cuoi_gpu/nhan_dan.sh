#!/usr/bin/env bash
# BAN-CUOI-T3 (việc 2) · NHẬN DẦN (thay nhan.sh khi đĩa chật — sự cố 22/10 19:23 hết đĩa vì giữ ~670 PNG 1080p): cùng đường ống chỉnh màu (nc_exr.py + nc_grade.js, lô 6, thử lại ≤ 3 lượt)
#   nhưng mỗi PNG → jpg q95 vào thư mục cảnh đinh NGAY rồi xoá PNG; khung đã nhận ghi ở <PNG>/xong.txt. Bản A không giữ (đã xoá sau render đoạn, xem nhan.sh).
#   bash nhan_dan.sh <doan> <khóa cảnh> <khung đầu> <khung cuối>
set -uo pipefail
REPO=$(cd "$(dirname "$0")/../../.." && pwd); export K2TL_CACHE=${K2TL_CACHE:-/var/tmp/cine-out/k2tl-cache} NC_DESIGN=$REPO/design NC_SCRIPTS=$REPO/scripts/k2tl
D=$1; K=$2; A=$3; B=$4; G=/var/tmp/cine-out/cuoi-gpu; IN=$G/exr/$D; PNG=$G/png/$D; mkdir -p $PNG; touch $PNG/xong.txt; CPU=$REPO/design/pt/cpu
HD=$(/opt/cine/bin/python -c "import json;print(json.load(open('/var/tmp/cine-out/k2c-t3-cuoi/heroes.json'))['$K']['dir'])")
for f in $(seq $A $B); do test -s $IN/$(printf %05d $f).exr || { echo "THIẾU EXR $f"; exit 3; }; done
doi() { for p in $PNG/*.png; do [ -s "$p" ] || continue; n=$(basename $p .png)
  /opt/cine/bin/python -c "from PIL import Image;Image.open('$p').convert('RGB').save('$HD/$n.jpg',quality=95)" && echo $n >> $PNG/xong.txt && rm -f $p; done; }
doi; T=$G/f32-$$
for k in 1 2 3; do for f in $(seq $A $B); do n=$(printf %05d $f); grep -qx $n $PNG/xong.txt || echo $IN/$n.exr; done | split -l 6 - $T-l-
  for L in $T-l-*; do [ -f $L ] || continue; rm -rf $T; /opt/cine/bin/python $CPU/nc_exr.py $(cat $L) --out $T > /dev/null
    node $CPU/nc_grade.js --scene t3tl --opt "$(cat $G/opt/$D.json)" --in $T --out $PNG --w 1920 --h 1080 2>&1 | tail -1 || true; rm -rf $T $L; doi; done; done
for f in $(seq $A $B); do n=$(printf %05d $f); grep -qx $n $PNG/xong.txt && test -s $HD/$n.jpg || { echo "THIẾU KHUNG $f"; exit 4; }; done
echo "NHAN-XONG $D $A-$B → $HD"
