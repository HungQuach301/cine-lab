#!/usr/bin/env bash
# V7C (việc 5) · 6 KHUNG CỔNG 1920×1080 SẠCH (không chữ, không bộ đếm) cùng loại cảnh với V7B §7 — cảnh t3tl + opt.nc (cách A, lightmap theo mốc), spp 4.
#   bash scripts/k2tl/v7c_khung.sh <thư mục opt shot (mk_ep_v7c.py --opt-dir)>   → reports/v7c/khung/cong-<loại>.png
set -euo pipefail
REPO=$(cd "$(dirname "$0")/../.." && pwd); OD=$1; export K2TL_CACHE=${K2TL_CACHE:-/var/tmp/cine-out/k2tl-cache}; T=/var/tmp/cine-out/v7c/khung; K=$REPO/reports/v7c/khung; mkdir -p $T $K
# loại · shot · giây trong shot (V7B: vây hãm C1 21,8 · cảng C4 3,5 · phố dày C3 11,5 · hero H3 10,4 · toàn cảnh C5 2,6 · bờ + chiến sự H2 13,3)
for g in "vay-ham C1 21.8" "cang C4 5.0" "pho-day C3 11.5" "hero H3 10.4" "toan-canh C5 2.6" "bo-chien-su H2T 1.0" "bo-chien-su-cao H2 13.8"; do set -- $g
  F=$(/opt/cine/bin/python -c "print(round($3*24))")
  node $REPO/scripts/k2tl/render.js --scene t3tl --pack gib --opt "$(cat $OD/v7c_$2.json)" --only $F --override '[{"noText":true}]' --tech '{"spp":4}' --w 1920 --h 1080 --out $T/$1 2>&1 | grep -E "s_per_frame|pageerror|LỖI" | cut -c1-200
  /opt/cine/bin/python -c "from PIL import Image;Image.open('$T/$1/$(printf %05d $F).jpg').save('$K/cong-$1.png')"; echo "cong-$1 ← $2 @ $3 s (khung $F)"
done
