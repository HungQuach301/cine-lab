#!/usr/bin/env bash
# BAN-CUOI-T3 (việc 2) · ĐIỀU KHIỂN MỘT pod theo danh sách đoạn (thay chay_pod.sh khi chia 2 pod): bật (nếu chưa) → cơ sở + Blender (nếu chưa) → dữ liệu đoạn (nếu chưa)
#   → [chờ việc đo thử đang chạy xong] → dựng các dải → kéo EXR dần → KIỂM ĐỦ DẢI trên máy (test -s) → TẮT. Trạng thái pod ở đĩa ($NCG_STATE) — chạy lại được sau khi container khởi động lại.
#   NCG_STATE=/var/tmp/cine-out/cuoi-gpu/pod2.json bash dk_pod.sh <nhãn> "n29:534:671" [cho_log]
set -u
REPO=$(cd "$(dirname "$0")/../../.." && pwd); G=/var/tmp/cine-out/cuoi-gpu; P="/opt/cine/bin/python $REPO/scripts/k2tl/cuoi_gpu/pod.py"; LAB=$1; JOBS=$2; CHO=${3:-}
log() { echo "$(date -u +%H:%M:%S) [$LAB] $*"; }
r() { $P run "$1" --cho 2>/dev/null | sed -n 2p; }
thieu_mot() { /opt/cine/bin/python -c "import os;print(sum(1 for f in range($2,$3+1) if not (os.path.exists('$G/exr/$1/%05d.exr'%f) and os.path.getsize('$G/exr/$1/%05d.exr'%f)>0)))"; }
thieu() { local t=0; for j in $JOBS; do IFS=: read D A B <<< "$j"; t=$((t + $(thieu_mot $D $A $B))); done; echo $t; }
keo() { for j in $JOBS ${KEO_THEM:-}; do IFS=: read D A B <<< "$j"; mkdir -p $G/exr/$D
  for f in $($P ls out/$D 2>/dev/null | /opt/cine/bin/python -c "import json,sys
try: print(' '.join(x[0] for x in json.load(sys.stdin) if x[0].endswith('.exr')))
except Exception: pass"); do [ -s $G/exr/$D/$f ] || $P get out/$D/$f $G/exr/$D/$f > /dev/null 2>&1 || rm -f $G/exr/$D/$f; done; done; }
[ -f $NCG_STATE ] || { log "BẬT pod"; $P len "NVIDIA GeForce RTX 5090" SECURE $LAB 80 || exit 2; }
if [ "$(r 'test -x /w/blender/blender && echo CO')" != CO ]; then log "cơ sở + Blender"; $P put $G/co-so.tar co-so.tar && $P run "cd /w && tar xf co-so.tar && bash /w/gpu/pod_setup.sh" --cho | tail -2; fi
for j in $JOBS; do IFS=: read D A B <<< "$j"
  if [ "$(r "test -d /w/$D/exp && echo CO")" != CO ]; then while [ ! -s $G/$D.tar ]; do log "chờ dữ liệu $D"; sleep 60; done
    log "tải dữ liệu $D"; $P put $G/$D.tar $D.tar && $P run "cd /w && rm -rf x$D && mkdir x$D && tar xf $D.tar -C x$D && cd x$D && while read p h; do mkdir -p \$(dirname \$p); ln cas/\$h \$p; done < lien.txt && rm -rf /w/$D && mv dive /w/$D && ls /w/$D/exp | wc -l" --cho | tail -2; fi; done
if [ -n "$CHO" ]; then while [ "$(r "grep -c POD-DOAN-XONG /w/$CHO")" != 1 ]; do log "chờ việc đang chạy ($CHO)"; KEO_THEM="h2t:0:47" keo; sleep 120; done; KEO_THEM="h2t:0:47" keo; fi
CMD="cd /w"; for j in $JOBS; do IFS=: read D A B <<< "$j"; CMD="$CMD; DOAN=$D A=$A B=$B SPP=64 SPPN=32 bash /w/gpu/pod_doan.sh >> /w/$LAB.log 2>&1"; done
log "DỰNG: $JOBS"; $P run "$CMD; echo POD-LAB-XONG >> /w/$LAB.log" > /dev/null
while true; do keo; t=$(thieu); x=$(r "grep -c POD-LAB-XONG /w/$LAB.log"); log "kéo: còn thiếu $t khung · xong=$x"
  [ "$t" = 0 ] && break
  [ "${x:-0}" = 1 ] && { log "pod báo xong mà còn thiếu $t — kéo lại"; sleep 30; continue; }
  sleep 150; done
$P get $LAB.log $G/exr/pod-$LAB.log > /dev/null 2>&1; log "ĐỦ DẢI — TẮT pod"; $P tat; log TAT-XONG
