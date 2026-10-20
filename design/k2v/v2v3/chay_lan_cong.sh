#!/usr/bin/env bash
# lan_cong.sh: dựng 3 cửa sổ cổng (17 khung) bằng dung3.js
G=/var/tmp/cine-out/v2v3/gates-opt.json; S=/var/tmp/cine-out/v2v3/src
for k in hero vay-ham bo-chien-su; do
  O=$(/opt/cine/bin/python -c "import json;print(json.dumps(json.load(open('$G'))['$k']['opt']))"); D=$(/opt/cine/bin/python -c "import json;print(json.load(open('$G'))['$k']['dur'])")
  A=$(/opt/cine/bin/python -c "import json;g=json.load(open('$G'))['$k'];print(g['from_'], g['to'])")
  cd /var/tmp/v7b-wt && node /home/user/cine-lab/design/k2v/v2v3/dung3.js --wt /var/tmp/v7b-wt --page /var/tmp/cine-out/v2v3/page --opt "$O" --dur $D --w 1280 --h 720 --out $S/g-$k --from ${A% *} --to ${A#* } > $S/g-$k.log 2>&1; echo EXIT $? >> $S/g-$k.log
done
