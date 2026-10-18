#!/usr/bin/env bash
# V6 bước 7 · BẢN TỐT NHẤT (Cycles lai): với mỗi khung cổng — xuất cảnh k2v (export6.js) → Cycles (cy6.py, + lượt phụ albedo/độ sâu) → ghép (cy6_ghep.py) → chỉnh màu
# bằng chính đường ống k2v (export6.js grade). Ghi thời gian từng chặng vào <ra>/tot-<k>.time.json. CÙNG cảnh, CÙNG khung, CÙNG máy với v6_khung.sh.
#  ONLY="1 2" SPP=96 TH=2 [REUSE_CY=1] bash scripts/k2tl/v6_tot.sh [<ra>]   (REUSE_CY=1: giữ EXR Cycles đã có — chỉ khi hình học không đổi)
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd); O=${1:-/var/tmp/cine-out/v6/tot}; W=/var/tmp/cine-out/v6/cy; mkdir -p $O $W
export K2TL_CACHE=${K2TL_CACHE:-/var/tmp/cine-out/k2tl-cache} K2TL_GL=${K2TL_GL:-llvmpipe}
SPP=${SPP:-96}; TH=${TH:-2}; CC0=${CC0:-/var/tmp/cine-out/v6/cc0}; ONLY=${ONLY:-"1 2 3 4 5 6"}
for k in "1 eo6 48" "2 vinh6 72" "3 pho6 96" "4 vinh6 192" "5 toan6 72" "6 bo6 72"; do set -- $k; [[ " $ONLY " == *" $1 "* ]] || continue
  D=$W/x$1; rm -rf $D; t0=$(date +%s.%N)
  node $ROOT/scripts/k2tl/export6.js export --scene $2 --f $3 --out $D | tail -1; t1=$(date +%s.%N)
  if [[ ${REUSE_CY:-0} == 1 && -f $W/x$1-cy.exr && -f $W/x$1-cy-aux.exr ]]; then echo "dùng lại $W/x$1-cy.exr (hình học không đổi; chỉ lượt albedo k2v đổi)"; else
  /opt/bpy/bin/python $ROOT/scripts/k2tl/cy6.py -- $D $W/x$1-cy.exr --spp $SPP --threads $TH --cc0 $CC0 2>&1 | grep '^CY6'; fi; t2=$(date +%s.%N)
  /opt/cine/bin/python $ROOT/scripts/k2tl/cy6_ghep.py $D $W/x$1-cy.exr $W/x$1.f32 --irr-png $W/x$1-irr.png; t3=$(date +%s.%N)
  node $ROOT/scripts/k2tl/export6.js grade --scene $2 --f $3 --hdr $W/x$1.f32 --out $O/tot-$1.png | tail -1; t4=$(date +%s.%N)
  python3 -c "import json,sys; a=[float(x) for x in sys.argv[2:]]; json.dump(dict(khung=sys.argv[1], xuat_s=round(a[1]-a[0],1), cycles_s=round(a[2]-a[1],1), ghep_s=round(a[3]-a[2],1), chinh_mau_s=round(a[4]-a[3],1), tong_s=round(a[4]-a[0],1), spp=$SPP, luong=$TH), open('$O/tot-$1.time.json','w'))" "$2:$3" $t0 $t1 $t2 $t3 $t4
  cat $O/tot-$1.time.json; echo
done
