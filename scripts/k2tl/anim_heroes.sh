#!/bin/bash
# ANIMATIC-T3 · dựng CẢNH ĐINH một tập theo heroes.json của build (bản sao logic scripts/k2/heroes_par.sh: stamp, --resume, dir.new → dir) + LỌC theo khoá + ghi giây đồng hồ từng cảnh.
#   ONLY="anim_C2 anim_C3" P=2 SPP=4 bash scripts/k2tl/anim_heroes.sh <episode.yaml>   → <out>/heroes-gio.log: "<khoá> <số khung> <giây> <s/khung>"
#   Chạy tách: setsid nohup … &; dừng theo PID nhóm (BAI-HOC #41), không pkill theo chuỗi.
set -u
REPO=$(cd "$(dirname "$0")/../.." && pwd); PY=/opt/cine/bin/python
EP=$(realpath "$1"); P=${P:-2}
O=$($PY -c "import yaml;e=yaml.safe_load(open('$EP'));print(e.get('out') or '/var/tmp/cine-out/'+e['id'])")
[ -f $O/heroes.json ] || { echo "thiếu $O/heroes.json"; exit 2; }
one() { local k=$1 h=$2 v=$3 d=$4 dir=$5 st=$6 w=$7 h2=$8 opt=$9
  [ "$(cat $dir/stamp 2>/dev/null)" = "$st" ] && { echo "giữ $k"; return; }
  local lp=$(cat $dir.new/pid 2>/dev/null); [ -n "$lp" ] && kill -0 $lp 2>/dev/null && { echo "đang dựng (pid $lp): $k"; return; }
  local rs=""; if [ "$(cat $dir.new/pending 2>/dev/null)" = "$st" ]; then rs=--resume; else rm -rf "$dir.new"; mkdir -p "$dir.new"; echo $st > $dir.new/pending; fi
  local t0=$(date +%s); echo "$(date +%H:%M) dựng $k ($d s, ${w}×${h2}) $rs"
  node $REPO/scripts/k2/hero.js --hero $h --variant $v --dur $d --w $w --h $h2 --spp ${SPP:-4} --opt "$opt" --out $dir.new $rs 2>>$O/hero-$k.err & local np=$!; echo $np > $dir.new/pid
  if wait $np; then rm -f $dir.new/pid; echo $st > $dir.new/stamp; rm -f $dir.new/pending; rm -rf "$dir"; mv "$dir.new" "$dir"
    local n=$(ls $dir | grep -cE '^[0-9]+\.(jpg|png)$'); local s=$(( $(date +%s) - t0 )); echo "$k $n $s $($PY -c "print(round($s/max(1,$n),2))")" >> $O/heroes-gio.log; echo "$(date +%H:%M) xong $k $n khung $s s"
  else echo "LỖI $k"; touch $O/heroes-par.failed; fi; }
$PY -c "
import json,os
H=json.load(open('$O/heroes.json')); only=os.environ.get('ONLY','').split()
for k,v in sorted(H.items(),key=lambda x:-x[1]['dur']):
  if only and k not in only: continue
  print(k,v['hero'],v['variant'],v['dur'],v['dir'],v['stamp'],*v.get('size',[1920,1080]),json.dumps(v['opt'],separators=(',',':')))" > $O/heroes-anim.list
while read -r k h v d dir st w h2 opt; do
  while [ $(jobs -rp | wc -l) -ge $P ]; do wait -n; done
  one $k $h $v $d $dir $st $w $h2 "$opt" &
done < $O/heroes-anim.list
wait; echo "HEROES-XONG"
