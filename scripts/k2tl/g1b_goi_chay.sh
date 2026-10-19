#!/usr/bin/env bash
# G1b T3 · CHẠY MỘT GÓI RENDER 1080p (ngoại lệ EE2-A): mỗi phiên/máy chạy một gói của reports/g1b-t3/render/ke-hoach.json.
#   bash scripts/k2tl/g1b_goi_chay.sh <G01..G04> [heroes.json 1080p = /var/tmp/cine-out/k2c-t3-g1b-1080/heroes.json]
# Trước khi chạy: cùng commit mã (git rev-parse HEAD ghi vào <out>/goi-<G>.json), dựng lại $K2TL_CACHE (fetch_sources … pack_1782.sh → pack_g1b.sh), $K2V_CACHE/g1b (ảnh), bộ đệm SM (log-SM*.json khoá dung).
# Mỗi cảnh dựng vào thư mục cảnh đinh của heroes.json (stamp), dựng tiếp --resume nếu bị ngắt. Cuối gói: KHUNG THAM CHIẾU MÀU g1b_2j_0 #150 → <out>/ref-<G>.jpg (mọi gói cùng dựng khung này).
# GHÉP (máy tổng): chép mọi thư mục cảnh đinh về /var/tmp/cine-out/hero/, kiểm `cmp`/ΔE các ref-G*.jpg (ΔE00 trung bình ≤ 0,5 và cùng SHA mã) → `bash scripts/k2/build.sh channel-k2/k2c-t3-01/g1b/episode.yaml render` (giữ cảnh có stamp; dựng lớp 2D) → mix (khi có lời) → ghep.
set -euo pipefail
REPO=$(cd "$(dirname "$0")/../.." && pwd); G=$1; HJ=${2:-/var/tmp/cine-out/k2c-t3-g1b-1080/heroes.json}; PLAN=$REPO/reports/g1b-t3/render/ke-hoach.json
export K2TL_CACHE=${K2TL_CACHE:-/var/tmp/cine-out/k2tl-cache}; O=$(dirname $HJ); T0=$(date +%s)
/opt/cine/bin/python - "$PLAN" "$G" "$HJ" > $O/goi-$G.list <<'P'
import json, sys
plan, G, HJ = json.load(open(sys.argv[1])), sys.argv[2], json.load(open(sys.argv[3]))
for c in [g for g in plan['goi'] if g['id'] == G][0]['canh']:
    h = HJ[c['canh']]; only = f"{c['dai'][0]}-{c['dai'][1]}" if c['dai'] else ''
    print(c['canh'], h['hero'], h['dur'], h['dir'], h['stamp'], *h.get('size', [1920, 1080]), only, json.dumps(h['opt'], separators=(',', ':')))
P
while read -r k h d dir st w hh only opt; do
  [ "$(cat $dir/stamp 2>/dev/null)" = "$st" ] && { echo "giữ $k"; continue; }
  mkdir -p $dir.new; rs=""; [ -f $dir.new/pending ] && rs=--resume; echo $st > $dir.new/pending
  ON=""; [ -n "$only" ] && ON="--only $(/opt/cine/bin/python -c "a,b=map(int,'$only'.split('-'));print(','.join(map(str,range(a,b+1))))")"
  node $REPO/scripts/k2/hero.js --hero $h --variant a --dur $d --w $w --h $hh --spp 4 --opt "$opt" --out $dir.new $rs $ON 2>>$O/goi-$G.err
  if [ -z "$only" ]; then echo $st > $dir.new/stamp; rm -f $dir.new/pending; rm -rf $dir; mv $dir.new $dir; fi
  echo "$(date +%H:%M) xong $k $only"; done < $O/goi-$G.list
REF=$(/opt/cine/bin/python -c "import json;h=json.load(open('$HJ'))['g1b_2j_0'];print(json.dumps(h['opt'],separators=(',',':')))")
node $REPO/scripts/k2/hero.js --hero tl/t3s --variant a --dur 12.5 --w 1920 --h 1080 --spp 4 --opt "$REF" --out $O/ref-$G --only 150 2>/dev/null; cp $O/ref-$G/00150.jpg $O/ref-$G.jpg
echo "{\"goi\": \"$G\", \"ma\": \"$(git -C $REPO rev-parse HEAD)\", \"giay\": $(( $(date +%s) - T0 )), \"ref_sha\": \"$(sha256sum $O/ref-$G.jpg | cut -c1-16)\"}" > $O/goi-$G.json; cat $O/goi-$G.json
