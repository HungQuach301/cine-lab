#!/usr/bin/env bash
# NC-GPU · cú lặn 20 s TOÀN BỘ bằng Cycles GPU trên pod (không ghép A↔B): mỗi đoạn [mốc, mốc kế) dựng cảnh từ bản xuất hình học của mốc (/w/dive/exp/d-<mốc>),
# máy theo /w/dive/cam.json (khung hoá → motion blur), nắng/trăng + trời + khói/lửa theo TỪNG khung (/w/dive/lf/<khung>.json). Ra /w/out/dive<SPP>/<khung>.exr (half).
# Dùng: SPP=64 SPPN=32 bash pod_dive.sh [khung đầu] [khung cuối]   (SPPN: khung đêm — đo: 32 ≈ 64 spp sau OIDN, 64 s so 108 s/khung)
cd /w; BL=/w/blender/blender; SPP=${SPP:-64}; SPPN=${SPPN:-$SPP}; A=${1:-0}; B=${2:-479}; O=${O:-/w/out/dive$SPP}; mkdir -p $O
KEYS=($(ls /w/dive/exp | sed 's/d-//' | sort -n)); n=${#KEYS[@]}
for ((i=0; i<n; i++)); do k=$((10#${KEYS[$i]})); if [ $((i+1)) -lt $n ]; then e=$((10#${KEYS[$((i+1))]} - 1)); else e=479; fi   # lượt 1: biểu thức ?: lỗi ở đoạn cuối (KEYS[n] rỗng) → 468–479 không được dựng
  [ $e -lt $A ] && continue; [ $k -gt $B ] && break; lo=$(( k>A ? k : A )); hi=$(( e<B ? e : B ))
  NIGHT=$(python3 -c "import json;print(json.load(open('/w/dive/lf/%05d.json'%$lo)).get('night') or 0)")
  $BL -b --factory-startup --python-exit-code 1 -P /w/gpu/gpu_blend.py -- /w/dive/exp/d-${KEYS[$i]} cycles $O --tex /w/tex --topo /w/topo/1782-m1,/w/topo/1782-m4 \
    --spp $(python3 -c "print($SPPN if float('$NIGHT') > 0 else $SPP)") --res 1920x1080 --threads 16 --fx --d4k --bushx ${BUSHX:-3} --dof --mb --half --night $NIGHT --anim /w/dive/cam.json --frames $lo:$hi --fxdir /w/dive/lf \
    --cls /w/pack/cls.png --packmeta /w/pack/meta.json --year 1782 --persist --needgpu --vbiased --hazek ${HAZEK:-0.75} ${XOPT} 2>&1 | grep -E "NC-RENDER|NC-GPU-DEV|Error|Traceback" | tr '\n' ' '; echo " [doan $lo-$hi]"
done
echo POD-DIVE-XONG
