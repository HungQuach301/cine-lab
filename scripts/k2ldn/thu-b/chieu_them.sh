#!/bin/bash
# THU-B-T4 · (B ii) thêm vòng hiệu chỉnh khung 0 (khi ΔE khung 0 còn > ngưỡng (e)) rồi timelapse + video.  bash chieu_them.sh <khung> <tag> <vòng đầu> <vòng cuối>
set -o pipefail
cd "$(dirname "$0")/../../.."
export THUB=${THUB:-/var/tmp/ldn/thub} LDN_DATA=${LDN_DATA:-/var/tmp/ldn}; F=$1; T=$2; PY=/opt/cine/bin/python; S=scripts/k2ldn/thu-b
for v in $(seq $3 $4); do
  $PY $S/bmn_thub.py proj $F $T $v || exit 2
  rm -rf $THUB/r/$F-bp-$T; $PY $S/dung.py 1 bp0:$F:$T | tail -1
  ffmpeg -nostdin -loglevel error -y -i $THUB/r/$F-bp-$T/00000.png -vf "lut3d=file='channel-k2/k2c-t3-01/mau/k2c-t3-kenh-v030.cube':interp=tetrahedral" $THUB/bp/$F/$T/khung0-cuoi.png
  $PY - <<PYEOF
import cv2, numpy as np, json
t='$THUB/bp/$F/$T'; G=cv2.imread(t+'/ghep.png'); C=cv2.imread(t+'/khung0-cuoi.png'); M=cv2.imread('$THUB/bp/$F/do-duoc.png',0)>127
lab=lambda x: cv2.cvtColor(x,cv2.COLOR_BGR2LAB).astype(np.float32)*np.array([100/255,1,1],np.float32)
de=np.linalg.norm(lab(G)-lab(C),axis=-1)[M]; r={'vong':$v,'dE_tb':round(float(de.mean()),2),'dE_p95':round(float(np.percentile(de,95)),2)}
json.dump(r,open(t+'/khung0-de.json','w')); open(t+'/khung0-de-lich-su.jsonl','a').write(json.dumps(r)+'\n'); print('ΔE khung 0 (PNG):', r)
PYEOF
done
rm -rf $THUB/r/tl-$F-bp-$T; $PY $S/dung.py 1 bptl:$F:$T | tail -1
$PY $S/bmn_thub.py tl $F $T && echo CHIEU-XONG $F $T
