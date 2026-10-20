#!/usr/bin/env bash
# dung_cua_so.sh <clip key> <from> <to> <out>
set -e
O=$(/opt/cine/bin/python -c "import json;print(json.dumps(json.load(open('/var/tmp/cine-out/v2v3/clips-opt.json'))['$1']['opt']))")
D=$(/opt/cine/bin/python -c "import json;print(json.load(open('/var/tmp/cine-out/v2v3/clips-opt.json'))['$1']['dur'])")
cd /var/tmp/v7b-wt && node /home/user/cine-lab/design/k2v/v2v3/dung3.js --wt /var/tmp/v7b-wt --page /var/tmp/cine-out/v2v3/page --opt "$O" --dur $D --w 1280 --h 720 --out $4 --from $2 --to $3
