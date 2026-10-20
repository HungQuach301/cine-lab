#!/usr/bin/env bash
# topo.sh — albedo nền nhìn thẳng xuống (nc_topo.js của NC-CPU, không sửa): theo năm (1 m hộp phố + 4 m toàn vùng) và 0,5 m quanh điểm máy từng cổng (trạng thái đúng khung cổng)
. /home/user/cine-lab/design/pt/gpu/chay/env.sh; mkdir -p $G/topo
opt() { /opt/cine/bin/python -c "import json;o=json.load(open('$S/shots/$1.json'));o['nc']={};print(json.dumps(o))"; }
if [ "${1:-nam}" = nam ]; then
for Y in 1782:v7b_C5:62 2026:v7b_H3:250; do IFS=: read T SH F <<< "$Y"
  node $CPU/nc_topo.js --scene ../nc/ncA --opt "$(opt $SH)" --f $F --box -3000,-3000,1000,3500 --res 1 --out $G/topo/$T-m1 2>&1 | tail -1
  node $CPU/nc_topo.js --scene ../nc/ncA --opt "$(opt $SH)" --f $F --box -6500,-5500,5500,8500 --res 4 --out $G/topo/$T-m4 2>&1 | tail -1
done; fi
if [ "${1:-nam}" = gan ]; then
for g in ${GATES:-vay-ham cang pho-day hero toan-canh bo-chien-su}; do
  read SHOT T < <(/opt/cine/bin/python -c "import json;g=[x for x in json.load(open('$CPU/gates.json')) if x['k']=='$g'][0];print(g['shot'],g['t'])"); F=$(/opt/cine/bin/python -c "print(round($T*24))")
  BOX=$(/opt/cine/bin/python $GPU/near_box.py $G/exp/g-$g/manifest.json 900)
  echo -n "$g $BOX "; node $CPU/nc_topo.js --scene ../nc/ncA --opt "$(opt $SHOT)" --f $F --box $BOX --res 0.5 --out $G/topo/gan-$g 2>&1 | tail -1
done; fi
