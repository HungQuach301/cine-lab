#!/usr/bin/env bash
# BAN-CUOI-T3 (việc 2) · ĐIỀU KHIỂN 1 pod RunPod RTX 5090 SECURE cho 2 đoạn Cycles GPU (h2t 0–119, n29 396–671):
#   bật → cơ sở (gpu_blend.py, pod_doan.sh, vân 2k, albedo b1782, cls/meta) + cài Blender 5.2.2 → dữ liệu đoạn (khử trùng lặp SHA) →
#   ĐO THỬ 2 s (h2t 0–47) ghi giây + $/s → dựng hết → kéo EXR dần, KIỂM ĐỦ DẢI trên máy (test -s) rồi mới TẮT (BAI-HOC #115 a/d/g). Trạng thái pod ở đĩa (pod.py STATE).
#   setsid nohup bash scripts/k2tl/cuoi_gpu/chay_pod.sh [buoc] > /var/tmp/cine-out/log/pod.log 2>&1 &     buoc: tat-ca (mặc định) | keo | tat
set -u
REPO=$(cd "$(dirname "$0")/../../.." && pwd); G=/var/tmp/cine-out/cuoi-gpu; P="/opt/cine/bin/python $REPO/scripts/k2tl/cuoi_gpu/pod.py"; mkdir -p $G/exr/h2t $G/exr/n29
D0=$REPO/scripts/k2tl/cuoi_gpu; N=/var/tmp/cine-out/anim/nuong; C=/var/tmp/cine-out/k2tl-cache
log() { echo "$(date -u +%H:%M:%S) $*"; }
thieu() { /opt/cine/bin/python -c "import os;a,b=$2,$3;print(sum(1 for f in range(a,b+1) if not (os.path.exists('$G/exr/$1/%05d.exr'%f) and os.path.getsize('$G/exr/$1/%05d.exr'%f)>0)))"; }
keo() { for D in h2t n29; do for f in $($P ls out/$D 2>/dev/null | /opt/cine/bin/python -c "import json,sys
try: print(' '.join(x[0] for x in json.load(sys.stdin) if x[0].endswith('.exr')))
except Exception: pass"); do [ -s $G/exr/$D/$f ] || $P get out/$D/$f $G/exr/$D/$f > /dev/null 2>&1 || rm -f $G/exr/$D/$f; done; done; }
B=${1:-tat-ca}
if [ $B = tat-ca ]; then
  [ -f $G/pod.json ] || { log "BẬT pod"; $P len "NVIDIA GeForce RTX 5090" SECURE ban-cuoi 80 || exit 2; }
  log "gói cơ sở"; rm -rf $G/co-so; mkdir -p $G/co-so/gpu $G/co-so/topo $G/co-so/pack
  cp $D0/gpu_blend.py $D0/pod_doan.sh $D0/pod_setup.sh $G/co-so/gpu/; cp -r $C/nc/tex $G/co-so/tex; cp $C/scene/gib/pack/cls.png $C/scene/gib/pack/meta.json $G/co-so/pack/
  for t in m1 m4; do mkdir -p $G/co-so/topo/b1782-$t; cp $N/topo-b1782-$t/topo.json $N/topo-b1782-$t/topo_full.png $G/co-so/topo/b1782-$t/; done
  tar -cf $G/co-so.tar -C $G/co-so . && sha256sum $G/co-so.tar
  $P put $G/co-so.tar co-so.tar && $P run "cd /w && tar xf co-so.tar && bash /w/gpu/pod_setup.sh" --cho | tail -4
  for D in h2t n29; do while [ ! -s $G/$D.tar ]; do log "chờ dữ liệu $D"; sleep 60; done
    $P put $G/$D.tar $D.tar && $P run "cd /w && rm -rf x$D && mkdir x$D && tar xf $D.tar -C x$D && cd x$D && while read p h; do mkdir -p \$(dirname \$p); ln cas/\$h \$p; done < lien.txt && rm -rf /w/$D && mv dive /w/$D && ls /w/$D/exp | wc -l" --cho | tail -3
    [ $D = h2t ] && { log "ĐO THỬ 2 s (h2t khung 0–47)"; T0=$(date +%s); $P run "cd /w && DOAN=h2t A=0 B=47 SPP=64 SPPN=32 bash /w/gpu/pod_doan.sh > /w/h2t-thu.log 2>&1; tail -3 /w/h2t-thu.log" --cho | tail -4
      T1=$(date +%s); keo; log "ĐO THỬ xong: $((T1 - T0)) s đồng hồ cho 48 khung (2 s phim); thiếu $(thieu h2t 0 47)"; echo "{\"do_thu\": \"h2t 0-47\", \"giay\": $((T1 - T0)), \"khung\": 48}" > $G/do-thu.json; }
  done
  log "DỰNG HẾT"; $P run "cd /w && DOAN=h2t A=48 B=119 SPP=64 SPPN=32 bash /w/gpu/pod_doan.sh > /w/h2t.log 2>&1; DOAN=n29 A=396 B=671 SPP=64 SPPN=32 bash /w/gpu/pod_doan.sh > /w/n29.log 2>&1; echo POD-TAT-CA-XONG >> /w/n29.log" > /dev/null
  B=keo; fi
if [ $B = keo ]; then
  while true; do keo; th=$(thieu h2t 0 119); tn=$(thieu n29 396 671); xong=$($P run "grep -c POD-TAT-CA-XONG /w/n29.log" --cho 2>/dev/null | sed -n 2p)
    log "kéo: thiếu h2t $th · n29 $tn · xong=$xong"
    [ "$th" = 0 ] && [ "$tn" = 0 ] && { $P get h2t.log $G/exr/pod-h2t.log > /dev/null 2>&1; $P get n29.log $G/exr/pod-n29.log > /dev/null 2>&1; B=tat; break; }
    if [ "${xong:-0}" -ge 1 ] 2>/dev/null; then log "pod báo xong nhưng còn thiếu — kéo lại"; sleep 30; continue; fi
    sleep 180; done; fi
if [ $B = tat ]; then log "TẮT pod (đủ dải: h2t $(thieu h2t 0 119) thiếu, n29 $(thieu n29 396 671) thiếu)"; $P tat; log TAT-XONG; fi
