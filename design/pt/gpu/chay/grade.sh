#!/usr/bin/env bash
# grade.sh <thư mục exr> <thư mục png ra> — chỉnh màu ảnh Cycles bằng ĐÚNG đường ống k2v của NC-CPU (nc_exr.py + nc_grade.js: ACES + LUT A + chỉnh màu V6 + hạt)
#  khung cổng: tên <cổng>.exr → opt của shot cổng, khung = round(t·24) (hạt theo khung) · cú lặn: <khung 5 số>.exr → opt cú lặn (DIVE=1)
. /home/user/cine-lab/design/pt/gpu/chay/env.sh; IN=$1; OUT=$2; mkdir -p $OUT; TMP=$G/f32-$$
if [ -n "$DIVE" ]; then ls $IN/*.exr | split -l 24 - $TMP-l-
  for L in $TMP-l-*; do rm -rf $TMP; /opt/cine/bin/python $CPU/nc_exr.py $(cat $L) --out $TMP > /dev/null
    node $CPU/nc_grade.js --scene ../nc/ncA --opt "$(cat $S/shots/dive.json)" --in $TMP --out $OUT --w 1920 --h 1080 2>&1 | tail -1; rm -rf $TMP $L; done; exit; fi
for e in $IN/*.exr; do g=$(basename $e .exr)
  read SHOT TT < <(/opt/cine/bin/python -c "import json;g=[x for x in json.load(open('$CPU/gates.json')) if x['k']=='$g'][0];print(g['shot'],g['t'])")
  F=$(/opt/cine/bin/python -c "print(round($TT*24))"); rm -rf $TMP; /opt/cine/bin/python $CPU/nc_exr.py $e --out $TMP > /dev/null; mv $TMP/$g.f32 $TMP/$(printf %05d $F).f32
  OPT=$(/opt/cine/bin/python -c "import json;o=json.load(open('$S/shots/$SHOT.json'));o['nc']={};print(json.dumps(o))")
  node $CPU/nc_grade.js --scene ../nc/ncA --opt "$OPT" --in $TMP --out $TMP --w 1920 --h 1080 2>&1 | tail -1; mv $TMP/$(printf %05d $F).png $OUT/$g.png; rm -rf $TMP
done
