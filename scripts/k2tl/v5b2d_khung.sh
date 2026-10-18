#!/usr/bin/env bash
# V5b-2d · DỰNG 6 KHUNG ĐO (6 loại cảnh, như V5b-2c §1.2) + mặt nạ nội dung + nhật ký máy, và lượt không-lửa của khung bờ+chiến sự (đo % lửa đỏ).
#  bash scripts/k2tl/v5b2d_khung.sh <thư mục ra>   (cần $K2TL_CACHE đã dựng: pack_1782.sh)
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd); O=${1:-/var/tmp/cine-out/v5b2d/khung}; mkdir -p $O
export K2TL_CACHE=${K2TL_CACHE:-/var/tmp/cine-out/k2tl-cache} K2TL_GL=${K2TL_GL:-llvmpipe}
R="node $ROOT/scripts/k2tl/render.js --pack gib --w 1920 --h 1080"
# loại → cảnh:khung (1 vây hãm · 2 cảng/bờ · 3 phố dày · 4 hero · 5 toàn cảnh đông · 6 bờ + chiến sự)
for k in "1 eo1782 48" "2 vinh1782 72" "3 pho1782 96" "4 vinh1782 192" "5 toan1782 72" "6 bo1782 72"; do set -- $k
  $R --scene $2 --only $3 --out $O/sach-$1 --override '[{"noText":true}]' 2>&1 | grep "s/khung" || true   # khung sạch (không lớp chữ)
  $R --scene $2 --only $3 --out $O/chu-$1 2>&1 | grep "s/khung" || true                                    # khung có lớp chữ (như master)
  $R --scene $2 --only $3 --maskonly $O/mask-$1.json --w 1920 --h 1080 2>/dev/null || true
  $R --scene $2 --campath $O/cam-$2.json 2>/dev/null || true
done
$R --scene bo1782 --only 72 --out $O/sach-6-khonglua --override '[{"noText":true}]' --opt '{"noFire":true}' 2>&1 | grep "s/khung" || true
