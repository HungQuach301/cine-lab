#!/bin/bash
# Phiên P — ẢNH EEVEE 4 GÓC của nhân vật đúng như trong phim: xuất glb bằng page_l2.js ("export":1) rồi dựng EEVEE (Blender /opt/bpy).
# Dùng:  bash scripts/p/eevee_4goc.sh <thư mục xuất> '<json args có "export":1,"exportWho":"cas"|"ida">' <ảnh ra.jpg> [ANG=0,60,180,-120] [DIST=5.2] [ZC=0]
#   vd.  bash scripts/p/eevee_4goc.sh /tmp/x/cas '{"shot":"s41","T":112.8,"casStyle":"bl","export":1,"exportWho":"cas","pose":{"cas":"turnaround"}}' /tmp/x/cas_4goc.jpg
#   Cận: DIST 1–2,4; ZC dời tâm khung theo chiều đứng (âm = xuống; gáy ZC 0.35 DIST 1.0; eo DIST 2.6 ZC -0.05).
set -e
D=${1:?thư mục}; A=${2:?json}; OUT=${3:?ảnh ra}; ANG=${4:-0,60,180,-120}; DIST=${5:-5.2}; ZC=${6:-0}
ROOT=$(git rev-parse --show-toplevel)
bash "$ROOT/scripts/p/khung_thu.sh" eevee-xuat "$D" "$A" 1 480 270 | tail -1
rm -f "$D"/e_*.png
ANG=$ANG DIST=$DIST ZC=$ZC /opt/bpy/bin/python "$ROOT/design/cong3/v2/char3d/blender/eevee_4goc_than.py" -- "$D/x.timing.json" "$D/e.png" > "$D/ev.log" 2>&1
/opt/cine/bin/python - "$D" "$OUT" <<'PY'
import glob,sys
from PIL import Image
d,out=sys.argv[1:3]; ims=[Image.open(f).convert('RGB') for f in sorted(glob.glob(d+'/e_*.png'))]
o=Image.new('RGB',(sum(i.width for i in ims),ims[0].height)); x=0
for i in ims: o.paste(i,(x,0)); x+=i.width
o.save(out,quality=90); print(out,o.size)
PY
