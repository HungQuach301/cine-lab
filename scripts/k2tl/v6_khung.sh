#!/usr/bin/env bash
# V6 · DỰNG 6 KHUNG CỔNG bản SẢN XUẤT llvmpipe (cảnh *6.js: ánh sáng V6, người có khớp, khói giả thể tích, HC7, máy theo cặp P1–P6) + mặt nạ + log máy + lượt không-lửa P6
#  bash scripts/k2tl/v6_khung.sh <thư mục ra>   (cần $K2TL_CACHE: pack_1782.sh)
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd); O=${1:-/var/tmp/cine-out/v6/khung}; mkdir -p $O
export K2TL_CACHE=${K2TL_CACHE:-/var/tmp/cine-out/k2tl-cache} K2TL_GL=${K2TL_GL:-llvmpipe}
R="node $ROOT/scripts/k2tl/render.js --pack gib --w 1920 --h 1080"
# loại → cảnh:khung (1 vây hãm · 2 cảng/bờ · 3 phố dày · 4 hero · 5 toàn cảnh đông · 6 bờ + chiến sự) — cùng khung số với V5b-2d
ONLY=${ONLY:-"1 2 3 4 5 6 k"}   # tập con loại (k = lượt không lửa P6) — chia lượt dưới trần 30 phút của tiến trình nền
for k in "1 eo6 48" "2 vinh6 72" "3 pho6 96" "4 vinh6 192" "5 toan6 72" "6 bo6 72"; do set -- $k; [[ " $ONLY " == *" $1 "* ]] || continue
  $R --scene $2 --only $3 --out $O/sach-$1 --override '[{"noText":true}]' 2>&1 | grep "s/khung" || true
  $R --scene $2 --only $3 --out $O/chu-$1 2>&1 | grep "s/khung" || true
  $R --scene $2 --only $3 --maskonly $O/mask-$1.json --maskpng $O/maskpng-$1 2>/dev/null || true
  $R --scene $2 --campath $O/cam-$2.json 2>/dev/null || true
done
[[ " $ONLY " == *" k "* ]] && $R --scene bo6 --only 72 --out $O/sach-6-khonglua --override '[{"noText":true}]' --opt '{"noFire":true}' 2>&1 | grep "s/khung" || true
