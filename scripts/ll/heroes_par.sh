#!/bin/bash
# Last Lamplighters · dựng CẢNH ĐINH song song (tập 8): cùng thư mục, stamp, --resume như hàm heroes() của build.sh,
# để bước render của build.sh "giữ" cảnh đã dựng. Dùng sau `build.sh <yaml> prep` (cần <out>/heroes.json).
#   P=3 SPP=4 bash scripts/ll/heroes_par.sh <episode.yaml>      P: số cảnh dựng cùng lúc (máy 4 vCPU: 3)
# Cảnh dài dựng trước (cân tải). Mỗi cảnh ghi <dir>.new/pid; lần chạy sau bỏ qua cảnh có pid còn sống.
# Chạy tách rời khỏi giới hạn 2 giờ của job nền: setsid nohup bash scripts/ll/heroes_par.sh <yaml> >> <out>/heroes-par.log 2>&1 &
# Lỗi một cảnh không dừng các cảnh khác; mã thoát 3 nếu có cảnh lỗi.
set -u
REPO=$(cd "$(dirname "$0")/../.." && pwd); PY=/opt/cine/bin/python; LL=$REPO/scripts/ll
EP=$(realpath "$1"); P=${P:-3}
O=$($PY -c "import yaml;e=yaml.safe_load(open('$EP'));print(e.get('out') or '/var/tmp/cine-out/'+e['id'])")
[ -f $O/heroes.json ] || { echo "thiếu $O/heroes.json — chạy build.sh prep trước"; exit 2; }
rm -f $O/heroes-par.failed
one() { local k=$1 h=$2 v=$3 d=$4 dir=$5 st=$6 w=$7 h2=$8 opt=$9
  [ "$(cat $dir/stamp 2>/dev/null)" = "$st" ] && { echo "giữ cảnh đinh $k"; return; }
  local lp=$(cat $dir.new/pid 2>/dev/null); [ -n "$lp" ] && kill -0 $lp 2>/dev/null && { echo "đang dựng ở tiến trình khác (pid $lp): $k — bỏ qua"; return; }   # 09/10: chạy lại khi lượt trước còn tiến trình mồ côi
  local rs=""; if [ "$(cat $dir.new/pending 2>/dev/null)" = "$st" ]; then rs=--resume; else rm -rf "$dir.new"; mkdir -p "$dir.new"; echo $st > $dir.new/pending; fi
  echo "$(date +%H:%M) dựng cảnh đinh $k ($h/$v, $d s, ${w}×${h2}) $rs"
  node $LL/hero.js --hero $h --variant $v --dur $d --w $w --h $h2 --spp ${SPP:-4} --opt "$opt" --out $dir.new $rs 2>>$O/hero-$k.err & local np=$!; echo $np > $dir.new/pid
  if wait $np; then rm -f $dir.new/pid
    echo $st > $dir.new/stamp; rm -f $dir.new/pending; rm -rf "$dir"; mv "$dir.new" "$dir"; echo "$(date +%H:%M) xong $k"
  else echo "LỖI cảnh đinh $k"; touch $O/heroes-par.failed; fi; }
$PY -c "import json;H=json.load(open('$O/heroes.json'));[print(k,v['hero'],v['variant'],v['dur'],v['dir'],v['stamp'],*v.get('size',[1920,1080]),json.dumps(v['opt'],separators=(',',':'))) for k,v in sorted(H.items(),key=lambda x:-x[1]['dur']*x[1].get('size',[1920,1080])[0])]" > $O/heroes-par.list
while read -r k h v d dir st w h2 opt; do
  while [ $(jobs -rp | wc -l) -ge $P ]; do wait -n; done
  one $k $h $v $d $dir $st $w $h2 "$opt" &
done < $O/heroes-par.list
wait
[ -f $O/heroes-par.failed ] && exit 3 || echo "CẢNH ĐINH XONG"
