#!/bin/bash
# THU-B-T4 · (B ii) chiếu ảnh AI đã khử sáng lên hình học + dựng lại ánh sáng: vòng 0 → khung 0 1080p → hiệu chỉnh vòng 1, 2 → timelapse 3 s → video (i)/(ii)/render.
#   bash scripts/k2ldn/thu-b/chieu.sh <khung> <tag>     (P = 1 trong chuỗi này; chạy tối đa 2 chuỗi song song)
set -o pipefail
cd "$(dirname "$0")/../../.."
export THUB=${THUB:-/var/tmp/ldn/thub} LDN_DATA=${LDN_DATA:-/var/tmp/ldn}; F=$1; T=$2; PY=/opt/cine/bin/python; S=scripts/k2ldn/thu-b
for v in 0 1 2; do
  $PY $S/bmn_thub.py proj $F $T $v || exit 2
  rm -rf $THUB/r/$F-bp-$T; $PY $S/dung.py 1 bp0:$F:$T | tail -1
done
# khung 0 sau vòng 2 (dựng bằng proj vòng 2) so tấm đã duyệt — chưa mã hoá video (phép (e) K đo trên video)
ffmpeg -nostdin -loglevel error -y -i $THUB/r/$F-bp-$T/00000.png -vf "lut3d=file='channel-k2/k2c-t3-01/mau/k2c-t3-kenh-v030.cube':interp=tetrahedral" $THUB/bp/$F/$T/khung0-cuoi.png
$PY - <<PYEOF
import cv2, numpy as np, json
t='$THUB/bp/$F/$T'; G=cv2.imread(t+'/ghep.png'); C=cv2.imread(t+'/khung0-cuoi.png'); M=cv2.imread('$THUB/bp/$F/do-duoc.png',0)>127
lab=lambda x: cv2.cvtColor(x,cv2.COLOR_BGR2LAB).astype(np.float32)*np.array([100/255,1,1],np.float32)
de=np.linalg.norm(lab(G)-lab(C),axis=-1)[M]; r={'dE_tb':round(float(de.mean()),2),'dE_p95':round(float(np.percentile(de,95)),2)}; json.dump(r,open(t+'/khung0-de.json','w')); print('ΔE khung 0 (PNG):', r)
PYEOF
rm -rf $THUB/r/tl-$F-bp-$T; $PY $S/dung.py 1 bptl:$F:$T | tail -1
$PY $S/bmn_thub.py tl $F $T && echo CHIEU-XONG $F $T
