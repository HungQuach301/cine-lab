#!/usr/bin/env bash
# NC-GPU · trên pod: (1) khung B nhanh của NC-CPU NGUYÊN VĂN (nc_blend.py qua nc_gpu_compat.py, 16 spp + OIDN) — 6 cổng (so 6 số CPU của NC-CPU §2.2);
# (2) 6 khung cổng cảnh Cycles "điện ảnh" (gpu_blend.py) ở 2 mức: 64 spp và 256 spp, cùng OIDN. Ra: /w/out/<nhãn>/<cổng>.exr + .json
# Dùng: bash pod_gates.sh [compat] [g64] [g256]   (GATES="…" để chọn cổng)
cd /w; BL=/w/blender/blender; TEX=/w/tex; PK=/w/pack
GATES=${GATES:-vay-ham cang pho-day hero toan-canh bo-chien-su}
yr() { case $1 in vay-ham) echo 1779;; cang) echo 1780;; pho-day) echo 1782;; hero) echo 2026;; toan-canh) echo 1782;; bo-chien-su) echo 1782;; esac; }
T() { [ $1 = hero ] && echo 2026 || echo 1782; }
for STEP in ${@:-compat g64 g256}; do
  if [ $STEP = compat ]; then mkdir -p out/compat
    for g in ${CGATES:-vay-ham cang pho-day hero toan-canh bo-chien-su}; do
      $BL -b --factory-startup --python-exit-code 1 -P /w/gpu/nc_gpu_compat.py -- /w/exp/g-$g cycles /w/out/compat/$g.exr --ncsrc /w/cpu/nc_blend.py --tex $TEX \
        --topo /w/topo/$(T $g)-m1,/w/topo/$(T $g)-m4 --spp 16 --res 1920x1080 --threads 16 2>&1 | grep -E "NC-RENDER|NC-GPU-DEV|Error|Traceback" ; done; fi
  if [ $STEP = g64 ] || [ $STEP = g256 ]; then S=${STEP#g}; mkdir -p out/$STEP
    for g in $GATES; do
      $BL -b --factory-startup --python-exit-code 1 -P /w/gpu/gpu_blend.py -- /w/exp/g-$g cycles /w/out/$STEP/$g.exr --tex $TEX \
        --topo /w/topo/gan-$g,/w/topo/$(T $g)-m1,/w/topo/$(T $g)-m4 --spp $S --res 1920x1080 --threads 16 --fx --d4k --bushx ${BUSHX:-3} --dof \
        --cls $PK/cls.png --packmeta $PK/meta.json --year $(yr $g) ${XOPT} 2>&1 | grep -E "NC-RENDER|NC-GPU-DEV|NC-BLEND|Error|Traceback" ; done; fi
done
echo POD-GATES-XONG
