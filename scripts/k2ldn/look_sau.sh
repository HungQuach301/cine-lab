#!/bin/bash
# LOOK-T4 · sau 24 khung: (1) 4 clip 8 s 640×360 (P = 2) · (2) đo s/khung 1080p sản xuất (spp 4, 24 khung, P = 2: M1 ngày + M3 đêm lửa) · (3) tranh khắc T3 (D7).
# Một vòng dựng một lúc; chờ RAM ≥ 5 GB. Ra: reports/look-t4/clip/, reports/look-t4/do/, reports/look-t4/t3/
set -o pipefail
cd "$(dirname "$0")/../.."
D=${LDN_DATA:-/var/tmp/ldn}; R=$D/look/r; mkdir -p "$R" reports/look-t4/t3
bash scripts/k2ldn/look_clip.sh 2 || echo "LỖI clip"
for m in M1 M3; do   # đo tốc độ sản xuất 1080p ở P = 2 (hai tiến trình cùng lúc, như sản xuất)
  LDN_DATA=$D node scripts/k2ldn/render_look.js --shot channel-k2/k2c-t4-02/look/may/do1080-$m.json --out $R/do1080-$m-p2a > $R/do1080-$m-p2a.log 2>&1 &
  LDN_DATA=$D node scripts/k2ldn/render_look.js --shot channel-k2/k2c-t4-02/look/may/do1080-$m.json --out $R/do1080-$m-p2b > $R/do1080-$m-p2b.log 2>&1 &
  wait
done
LDN_DATA=$D node scripts/k2ldn/render_look.js --shot channel-k2/k2c-t4-02/look/may/t3-khac.json --out $R/t3-khac-a --from 0 --to 96 > $R/t3-khac-a.log 2>&1 &
LDN_DATA=$D node scripts/k2ldn/render_look.js --shot channel-k2/k2c-t4-02/look/may/t3-khac.json --out $R/t3-khac-b --from 96 --to 192 > $R/t3-khac-b.log 2>&1 &
wait
mkdir -p $R/t3-khac && cp $R/t3-khac-a/*.jpg $R/t3-khac-b/*.jpg $R/t3-khac/ && /opt/cine/bin/python -c "import json,sys; a=json.load(open(sys.argv[1])); b=json.load(open(sys.argv[2])); a['frames']+=b['frames']; a['s_per_frame']=(a['s_per_frame']+b['s_per_frame'])/2; json.dump(a,open(sys.argv[3],'w'))" $R/t3-khac-a/log.json $R/t3-khac-b/log.json $R/t3-khac/log.json || echo "LỖI t3"
LDN_DATA=$D /opt/cine/bin/python scripts/k2ldn/t3_look.py khac $R/t3-khac $R/t3-ghep --H 720 > reports/look-t4/do/t3-khop.json || echo "LỖI t3 ghép"
echo "LOOK-SAU XONG"
