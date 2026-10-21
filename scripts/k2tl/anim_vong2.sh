#!/bin/bash
# ANIM-V2: bản sao anim_vong.sh, số tiến trình song song đọc từ /var/tmp/cine-out/log/P mỗi vòng (hạ khi đang nướng, nâng khi nướng xong; BAI-HOC #110: P ≤ 3)
# ANIMATIC-T3 · vòng dựng cảnh đinh theo lightmap đã nướng xong: mỗi vòng chọn các cảnh chưa có stamp mà MỌI lightmap (opt.nc.bakes) đã có meta.json,
# dựng bằng anim_heroes.sh (P cảnh song song); lặp tới khi đủ. Chạy tách: setsid nohup bash scripts/k2tl/anim_vong.sh <episode.yaml> > log &
set -u
REPO=$(cd "$(dirname "$0")/../.." && pwd); PY=/opt/cine/bin/python; EP=$(realpath "$1"); export K2TL_CACHE=${K2TL_CACHE:-/var/tmp/cine-out/k2tl-cache}
O=$($PY -c "import yaml;e=yaml.safe_load(open('$EP'));print(e.get('out') or '/var/tmp/cine-out/'+e['id'])")
while true; do
  read -r CON SAN <<< "$($PY -c "
import json,os
H=json.load(open('$O/heroes.json')); C=os.environ['K2TL_CACHE']; con=[]; san=[]
for k,v in H.items():
  if open(v['dir']+'/stamp').read().strip()==v['stamp'] if os.path.exists(v['dir']+'/stamp') else False: continue
  con.append(k)
  if all(os.path.exists(f\"{C}/nc/bake/{b['dir']}/meta.json\") for b in (v['opt'].get('nc') or {}).get('bakes',[])): san.append(k)
print(len(con), ','.join(san) or '-')")"
  [ "$CON" = 0 ] && { echo "$(date +%H:%M) VONG-XONG"; break; }
  if [ "$SAN" = "-" ]; then echo "$(date +%H:%M) chờ lightmap ($CON cảnh còn)"; sleep 120; continue; fi
  echo "$(date +%H:%M) vòng: ${SAN//,/ }"; ONLY="${SAN//,/ }" P=$(cat /var/tmp/cine-out/log/P 2>/dev/null || echo ${P:-2}) SPP=${SPP:-4} bash $REPO/scripts/k2tl/anim_heroes.sh "$EP"
  [ -f $O/heroes-par.failed ] && { echo "CÓ CẢNH LỖI — dừng vòng"; break; }
done
