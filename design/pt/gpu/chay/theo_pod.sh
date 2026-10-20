#!/usr/bin/env bash
# theo_pod.sh <tệp trạng thái pod> <tiền tố log> [khung dừng]   (LOG=tên log trên pod, mặc định dive.log; DAI=a:b dải khung PHẢI đủ trên máy trước khi tắt) — kéo dần EXR cú lặn về $G/dive-exr; nếu có khung dừng: khi khung đó có (test -s, KHÔNG grep câu ls)
#  thì dừng việc trên pod theo PID; khi dive.log có POD-DIVE-XONG: kéo nốt, lấy log, TẮT pod (ghi sổ). Chạy lại được sau khi container khởi động lại.
. /home/user/cine-lab/design/pt/gpu/chay/env.sh; export NCG_STATE=$1; PFX=$2; STOP=$3; P="/opt/cine/bin/python $GPU/pod.py"; mkdir -p $G/dive-exr; LOG=${LOG:-dive.log}
# lượt 1 (pod 4): tắt ngay sau lần kéo cuối → khung 242–255 dựng xong nhưng chưa về đã mất cùng pod → nay kiểm đủ dải DAI trước khi tắt
thieu() { [ -z "$DAI" ] && return 1; python3 -c "import os,sys;a,b=map(int,'$DAI'.split(':'));q=lambda f:'$G/dive-exr/%05d.exr'%f;m=[f for f in range(a,b+1) if not (os.path.exists(q(f)) and os.path.getsize(q(f))>0)];print(len(m));sys.exit(0 if m else 1)"; }
keo() { for f in $($P ls out/dive 2>/dev/null | python3 -c "import json,sys;print(' '.join(x[0] for x in json.load(sys.stdin) if x[0].endswith(('.exr','.json'))))" 2>/dev/null); do
  T=$f; [[ $f == nc-* ]] && T=$PFX-$f; [ -s $G/dive-exr/$T ] || $P get out/dive/$f $G/dive-exr/$T > /dev/null 2>&1 || rm -f $G/dive-exr/$T; done; }
while true; do
  if [ -n "$STOP" ] && $P run "test -s /w/out/dive/$(printf %05d $STOP).exr && echo CO-TEP" --cho 2>/dev/null | grep -qx CO-TEP; then
    $P run 'for p in $(ps -eo pid,args | grep -E "pod_dive.sh|blender/blender" | grep -v grep | grep -v "ps -eo" | awk "{print \$1}"); do [ $p != $$ ] && kill $p; done; echo POD-DIVE-XONG >> /w/'$LOG --cho > /dev/null; sleep 5; fi
  xong=$($P run "grep -c ${XONGM:-POD-DIVE-XONG} /w/$LOG" --cho 2>/dev/null | sed -n 2p); keo; echo "$(date -u +%H:%M) $(ls $G/dive-exr/*.exr | wc -l) xong=$xong"
  if [ "$xong" != "" ] && [ "$xong" -ge 1 ] 2>/dev/null; then for k in 1 2 3 4 5; do keo; thieu > /dev/null || break; sleep 20; done
    if thieu; then echo "CON THIEU khung — KHÔNG tắt pod"; sleep 180; continue; fi
    $P get $LOG $G/dive-exr/$PFX-$LOG > /dev/null 2>&1; $P tat; echo TAT-XONG; break; fi
  sleep 180; done
