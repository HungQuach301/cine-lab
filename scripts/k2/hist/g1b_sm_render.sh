#!/bin/bash
# G1b T3 · dựng 3 shot bản đồ chiến lược (SM1–SM3) ở nháp 960×540 qua đúng dây chuyền kênh 2, MỘT tiến trình dựng (nice 10):
#   1) g1b_sm.py → channel-k2/k2c-t3-01/g1b/sm/{SM1,SM2,SM3}.yaml + ep-g1b-sm.yaml   2) build.sh prep (K2_DRAFT=1) → heroes.json (stamp)
#   3) cảnh đinh: scripts/k2/hero.js → /var/tmp/cine-out/g1b/sm/<SM>/ (SM3: SM3/a, SM3/b) + tệp stamp; thư mục cảnh của dây chuyền
#      ($HERO_ROOT/g1b-sm-<k>-d) là LIÊN KẾT tới đó → build.sh render "giữ cảnh đinh" (không dựng lại)
#   4) build.sh render (lớp 2D k2.js, p.sach) → /var/tmp/cine-out/g1b/sm/ep/sec/<sm>.mkv   5) video thử ≤ 1,5 MB + khung giữa → channel-k2/k2c-t3-01/g1b/sm/
# Dùng: bash scripts/k2/hist/g1b_sm_render.sh [chỉ khoá cảnh: sm1 sm2 sm3a sm3b]
# Bộ đệm cần có (xem log-SM*.json · "dung"): $K2V_CACHE/relief/{sm1,sm2,sm3}, $K2V_CACHE/hist/{sm1-1704,sm2-1782,sm3-1941}
set -e
REPO=$(cd "$(dirname "$0")/../../.." && pwd); cd $REPO; PY=/opt/cine/bin/python
export K2V_CACHE=${K2V_CACHE:-/var/tmp/cine-out/k2v-cache} K2_DRAFT=1 MW=960 PARTS=0
G=channel-k2/k2c-t3-01/g1b/sm; OUT=/var/tmp/cine-out/g1b/sm; EP=$G/ep-g1b-sm.yaml; HR=/var/tmp/cine-out/hero
$PY scripts/k2/hist/g1b_sm.py --routes channel-k2/k2c-t3-01/tuyen/routes.geojson --out $G
bash scripts/k2/build.sh $EP prep > /dev/null
declare -A TGT=([sm1]=SM1 [sm2]=SM2 [sm3a]=SM3/a [sm3b]=SM3/b)
ONLYK="${*:-sm1 sm2 sm3a sm3b}"
$PY -c "import json;[print(k,v['dur'],v['stamp'],*v['size'],json.dumps(v['opt'],separators=(',',':'))) for k,v in json.load(open('$OUT/ep/heroes.json')).items()]" | while read -r k d st w h opt; do
  t=$OUT/${TGT[$k]}; mkdir -p $(dirname $t) $HR
  if [[ " $ONLYK " == *" $k "* ]] && [ "$(cat $t/stamp 2>/dev/null)" != "$st" ]; then
    rm -rf $t.new; mkdir -p $t.new; echo "$(date +%T) dựng $k ($d s, ${w}×${h}) → $t"
    nice -n 10 node scripts/k2/hero.js --hero relief/map --variant a --dur $d --w $w --h $h --spp 1 --opt "$opt" --out $t.new 2> $OUT/hero-$k.err || { echo "LỖI $k"; tail -5 $OUT/hero-$k.err; exit 3; }
    echo $st > $t.new/stamp; rm -rf $t; mv $t.new $t; fi
  [ -L $HR/g1b-sm-$k-d ] || { rm -rf $HR/g1b-sm-$k-d; ln -s $t $HR/g1b-sm-$k-d; }
done
J=1 nice -n 10 bash scripts/k2/build.sh $EP render | tail -6
# video thử nhỏ + khung giữa (đoạn sm3 = SM3a | SM3b cắt thẳng)
for s in sm1 sm2 sm3; do S=${s^^}; f=$OUT/ep/sec/$s.mkv; D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $f)
  ffmpeg -v error -y -i $f -an -vf "scale=960:540:flags=lanczos,format=yuv420p" -c:v libx264 -preset slow -crf 30 -maxrate 1500k -bufsize 3000k -movflags +faststart $G/$S-g1b-540p.mp4
  ffmpeg -v error -y -ss $(echo "$D / 2" | bc -l) -i $f -frames:v 1 -q:v 3 $G/$S-khung-giua.jpg
  echo "$S $(stat -c %s $G/$S-g1b-540p.mp4) B, khung giữa $(stat -c %s $G/$S-khung-giua.jpg) B"; done
