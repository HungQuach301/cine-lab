#!/usr/bin/env bash
# chia.sh — cú lặn chia 2 pod: pod 2 (NCG_STATE mặc định) làm 0–335, pod 3 (pod3.json) làm 336–479. Khi pod 2 có 00335.exr: dừng việc pod 2 theo PID,
# kéo hết ảnh pod 2 về, tắt pod 2 (ghi sổ). Kéo ảnh pod 3 riêng (keo_lan.sh với NCG_STATE=pod3).
. /home/user/cine-lab/design/pt/gpu/chay/env.sh; P="/opt/cine/bin/python $GPU/pod.py"
until $P run 'test -s /w/out/dive/00335.exr && echo CO-TEP' --cho 2>/dev/null | grep -qx CO-TEP; do sleep 120; done   # lượt 1: grep '00335.exr' khớp cả câu lỗi của ls → tắt nhầm pod 2 ở khung 92
$P run 'for p in $(ps -eo pid,args | grep -E "pod_dive.sh|blender/blender" | grep -v grep | grep -v "ps -eo" | awk "{print \$1}"); do [ $p != $$ ] && kill $p; done; echo POD-DIVE-XONG >> /w/dive.log' --cho
sleep 5; mkdir -p $G/dive-exr
for f in $($P ls out/dive | python3 -c "import json,sys;print(' '.join(x[0] for x in json.load(sys.stdin) if x[0].endswith(('.exr','.json'))))"); do
  n=${f%%.*}; [ -f $G/dive-exr/$f ] || { [[ $f == nc-* ]] && f2=p2-$f || f2=$f; $P get out/dive/$f $G/dive-exr/$f2 >/dev/null 2>&1; }; done
$P get dive.log $G/dive-exr/p2-dive.log >/dev/null 2>&1; $P tat; echo CHIA-XONG
