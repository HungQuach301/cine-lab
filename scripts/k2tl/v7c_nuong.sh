#!/usr/bin/env bash
# V7C (việc 1) · NƯỚNG LIGHTMAP cách A theo MỐC + TRẠNG THÁI PHỐ cho 2 đoạn bản thử (đường ống NC-CPU: nc_export.js → nc_topo.js → nc_blend.py nuong; mã NC-CPU không sửa).
#   bash scripts/k2tl/v7c_nuong.sh [b1779 b1781r b1782 b2026 b1940]   → $K2TL_CACHE/nc/bake/<tên>/{bake.png,meta.json}
#   b1779  : 15/1/1780 12:00 — phố 1779–81 NGUYÊN (trước 12/4/1781), trại + công sự vây hãm (C1–C4, C5 trước pháo kích)
#   b1781r : 1/7/1781 12:00 — vùng 'THE RUINS' đã sập (C5 sau 12/4/1781 10:45)
#   b1782  : 13/9/1782 15:30 — trạng thái NC-CPU (phố 1782 + 10 pin nổi, kênh B = lửa) (H2 đoạn 1782)
#   b2026  : 19/10/2026 12:00 — nhà 2026 có vật liệu (bfile V7B) (H1, H3 cuối, H2 đầu)
#   b1940  : 1/6/1940 11:00 — ghost 1943 + đường băng đầu (H3 1938–1943)
# Hộp nướng như NC-CPU: E −3000…1000, N −3000…3500, 3 m/texel, 24 spp. Albedo nền: 4 m cả hộp + 1 m phố (−2200…400, −3000…600).
set -euo pipefail
REPO=$(cd "$(dirname "$0")/../.." && pwd); export K2TL_CACHE=${K2TL_CACHE:-/var/tmp/cine-out/k2tl-cache} NC_DESIGN=$REPO/design NC_SCRIPTS=$REPO/scripts/k2tl
O=/var/tmp/cine-out/v7c/nuong; mkdir -p $O; CPU=$REPO/design/pt/cpu; BOX=-3000,-3000,1000,3500
declare -A AT=( [b1779]='1780-01-15 12:00' [b1781r]='1781-07-01 12:00' [b1782]='1782-09-13 15:30' [b2026]='2026-10-19 12:00' [b1940]='1940-06-01 11:00' )
for B in ${*:-b1779 b1781r b1782 b2026 b1940}; do
  [ -s $K2TL_CACHE/nc/bake/$B/bake.png ] && { echo "$B có rồi"; continue; }
  OPT=$(/opt/cine/bin/python - "$B" "${AT[$B]}" <<'P'
import json, sys
B, at = sys.argv[1], sys.argv[2]
o = dict(dur=1.0, time=[dict(t=0, at=at, sun=12.0 if B != 'b1782' else 15.5, lab='d'), dict(t=1.0, at=at, sun=12.0 if B != 'b1782' else 15.5, lab='d')],
         cam=[dict(t=0, p=[-1000, 4200, 250], l=[-1000, 0, 200], fov=90), dict(t=1.0, p=[-1000, 4200, 250], l=[-1000, 0, 200], fov=90)], nc={}, recl=True, night=False, shot='nuong-' + B)
if B == 'b2026': o.update(bfile='buildings-v7b.json', cityOpt=dict(near=2600, winFar=2400))
if B == 'b1782':
    o['fires'] = [dict(at=f['at'], wY=[1782.69, 1782.71], size=f['size']) for f in json.load(open('design/pt/cpu/fires-1782.json'))]
print(json.dumps(o))
P
)
  cd $REPO; date; echo "== $B ${AT[$B]}"
  node $CPU/nc_export.js --scene t3tl --opt "$OPT" --f 0 --far 7000 --nopass --w 1920 --h 1080 --out $O/exp-$B 2>&1 | tail -1
  node $CPU/nc_topo.js --scene t3tl --opt "$OPT" --f 0 --box $BOX --res 4 --out $O/topo-$B-m4 2>&1 | tail -1
  node $CPU/nc_topo.js --scene t3tl --opt "$OPT" --f 0 --box -2200,-3000,400,600 --res 1 --out $O/topo-$B-m1 2>&1 | tail -1
  FI=(); [ $B = b1782 ] && FI=(--fires "$(cat $CPU/fires-1782.json)")
  /opt/bpy/bin/python $CPU/nc_blend.py -- $O/exp-$B nuong $K2TL_CACHE/nc/bake/$B --topo $O/topo-$B-m1,$O/topo-$B-m4 --tex $K2TL_CACHE/nc/tex --box $BOX --bres 3 --spp 24 "${FI[@]}" --pack $K2TL_CACHE/scene/gib/pack 2>&1 | grep -E "NC-BAKE|Error|Traceback" || true
  cp $K2TL_CACHE/nc/bake/$B/meta.json $REPO/reports/v7c/do/nuong-$B.json 2>/dev/null || true
done; date; echo NUONG-XONG
