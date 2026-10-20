#!/usr/bin/env bash
# NC-GPU · cú lặn 20 s TOÀN BỘ bằng Cycles GPU trên pod (không ghép A↔B): mỗi đoạn [mốc, mốc kế) dựng cảnh từ bản xuất hình học của mốc (/w/dive/exp/d-<mốc>),
# máy theo /w/dive/cam.json (khung hoá → motion blur), nắng/trăng + trời + khói/lửa theo TỪNG khung (/w/dive/lf/<khung>.json). Ra /w/out/dive<SPP>/<khung>.exr (half).
# Dùng: SPP=64 bash pod_dive.sh [khung đầu] [khung cuối]
cd /w; BL=/w/blender/blender; SPP=${SPP:-64}; A=${1:-0}; B=${2:-479}; O=/w/out/dive$SPP; mkdir -p $O
KEYS=($(ls /w/dive/exp | sed 's/d-//' | sort -n)); n=${#KEYS[@]}
for ((i=0; i<n; i++)); do k=$((10#${KEYS[$i]})); e=$(( i+1<n ? 10#${KEYS[$((i+1))]} - 1 : 479 ))
  [ $e -lt $A ] && continue; [ $k -gt $B ] && break; lo=$(( k>A ? k : A )); hi=$(( e<B ? e : B ))
  NIGHT=$(python3 -c "import json;print(json.load(open('/w/dive/lf/%05d.json'%$lo)).get('night') or 0)")
  $BL -b --factory-startup --python-exit-code 1 -P /w/gpu/gpu_blend.py -- /w/dive/exp/d-${KEYS[$i]} cycles $O --tex /w/tex --topo /w/topo/1782-m1,/w/topo/1782-m4 \
    --spp $SPP --res 1920x1080 --threads 16 --fx --d4k --bushx ${BUSHX:-3} --dof --mb --half --night $NIGHT --anim /w/dive/cam.json --frames $lo:$hi --fxdir /w/dive/lf \
    --cls /w/pack/cls.png --packmeta /w/pack/meta.json --year 1782 --persist ${XOPT} 2>&1 | grep -E "NC-RENDER|Error|Traceback" | tr '\n' ' '; echo " [doan $lo-$hi]"
done
echo POD-DIVE-XONG
