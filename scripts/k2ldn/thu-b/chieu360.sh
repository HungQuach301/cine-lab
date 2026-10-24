#!/bin/bash
# THU-B-T4 · (B ii-a) hiệu chỉnh ảnh chiếu theo khung 0 Ở ĐỘ PHÂN GIẢI VIDEO (640×360, spp 4 như timelapse) — phép (e) đo trên video —
# rồi dựng lại timelapse chiếu; (ii-b) tỉ số bóng; video kiểm KHÔNG MẤT (crf 0 yuv444p) + bản xem crf 20.   bash chieu360.sh <khung> <tag> [số vòng=3]
set -o pipefail
cd "$(dirname "$0")/../../.."
export THUB=${THUB:-/var/tmp/ldn/thub} LDN_DATA=${LDN_DATA:-/var/tmp/ldn}; F=$1; T=$2; NV=${3:-3}; PY=/opt/cine/bin/python; S=scripts/k2ldn/thu-b; D=$THUB/bp/$F/$T
[ -s $D/proj-1080.png ] || cp $D/proj.png $D/proj-1080.png
rm -rf $THUB/r/$F-bp360-$T; $PY $S/dung.py 1 bp360:$F:$T | tail -1
for v in $(seq 1 $NV); do
  CAO360=1 $PY $S/bmn_thub.py proj $F $T $v || exit 2
  rm -rf $THUB/r/$F-bp360-$T; $PY $S/dung.py 1 bp360:$F:$T | tail -1
done
ffmpeg -nostdin -loglevel error -y -i $THUB/r/$F-bp360-$T/00000.png -vf "lut3d=file='channel-k2/k2c-t3-01/mau/k2c-t3-kenh-v030.cube':interp=tetrahedral" $D/khung0-360-cuoi.png
$PY - <<PYEOF
import cv2, numpy as np, json
G=cv2.resize(cv2.imread('$D/ghep.png'),(640,360),interpolation=cv2.INTER_AREA); C=cv2.imread('$D/khung0-360-cuoi.png'); M=cv2.resize(cv2.imread('$THUB/bp/$F/do-duoc.png',0),(640,360),interpolation=cv2.INTER_NEAREST)>127
lab=lambda x: cv2.cvtColor(x,cv2.COLOR_BGR2LAB).astype(np.float32)*np.array([100/255,1,1],np.float32)
de=np.linalg.norm(lab(G)-lab(C),axis=-1)[M]; r={'do_phan_giai':'640x360','vong':$NV,'dE_tb':round(float(de.mean()),2),'dE_p95':round(float(np.percentile(de,95)),2)}
json.dump(r,open('$D/khung0-360-de.json','w')); print('ΔE khung 0 @640×360 (PNG):', r)
PYEOF
rm -rf $THUB/r/tl-$F-bp-$T; $PY $S/dung.py 1 bptl:$F:$T | tail -1
MA_HOA_KIEM=1 $PY $S/bmn_thub.py tl $F $T && MA_HOA_KIEM=1 $PY $S/bmn_thub.py tiso $F $T && MA_HOA_KIEM=1 $PY $S/bmn_thub.py xem $F $T && echo CHIEU360-XONG $F $T
