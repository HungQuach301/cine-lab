#!/usr/bin/env bash
# BAN-CUOI-T3 · bản sao pod_dive.sh (NC-GPU) có tham số: dựng TRỌN bằng Cycles GPU một đoạn /w/<doan> (exp/d-<mốc>, lf/<khung>.json, cam.json) — không ghép A↔B.
#   DOAN=n29 A=396 B=671 SPP=64 SPPN=32 bash pod_doan.sh     → /w/out/<doan>/<khung>.exr (half)
#   Khác pod_dive.sh: thư mục đoạn + khung cuối theo tham số (pod_dive.sh cố định 479); topo albedo của mốc nướng b1782 (/w/topo/b1782-m1,-m4); bỏ --d4k (chỉ có vân 2k).
cd /w; BL=/w/blender/blender; DOAN=${DOAN:-n29}; R=/w/$DOAN; SPP=${SPP:-64}; SPPN=${SPPN:-$SPP}; A=${A:-0}; B=${B:-119}; O=${O:-/w/out/$DOAN}; mkdir -p $O
KEYS=($(ls $R/exp | sed 's/d-//' | sort -n)); n=${#KEYS[@]}
for ((i=0; i<n; i++)); do k=$((10#${KEYS[$i]})); if [ $((i+1)) -lt $n ]; then e=$((10#${KEYS[$((i+1))]} - 1)); else e=$B; fi
  [ $e -lt $A ] && continue; [ $k -gt $B ] && break; lo=$(( k>A ? k : A )); hi=$(( e<B ? e : B ))
  NIGHT=$(python3 -c "import json;print(json.load(open('$R/lf/%05d.json'%$lo)).get('night') or 0)")
  if [ "$(python3 -c "print(1 if float('$NIGHT') > 0 else 0)")" = 1 ]; then S=$SPPN; else S=$SPP; fi
  $BL -b --factory-startup --python-exit-code 1 -P /w/gpu/gpu_blend.py -- $R/exp/d-${KEYS[$i]} cycles $O --tex /w/tex --topo /w/topo/b1782-m1,/w/topo/b1782-m4 \
    --spp $S --res 1920x1080 --threads 16 --fx --bushx ${BUSHX:-3} --dof --mb --half --night $NIGHT --anim $R/cam.json --frames $lo:$hi --fxdir $R/lf \
    --cls /w/pack/cls.png --packmeta /w/pack/meta.json --year 1782 --persist --needgpu --vbiased --hazek ${HAZEK:-0.75} ${XOPT:-} 2>&1 | grep -E "NC-RENDER|NC-GPU-DEV|Error|Traceback" | tr '\n' ' '; echo " [doan $lo-$hi]"
done
echo POD-DOAN-XONG $DOAN
