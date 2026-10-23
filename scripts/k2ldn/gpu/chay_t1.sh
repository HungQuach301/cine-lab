#!/usr/bin/env bash
# TIEN-KY-T4 · bản thử T1 (ii): Cycles GPU trên RunPod RTX 5090 SECURE ($1,19/h).
#   bật → cài Blender 5.2.2 (pod_setup.sh) → tải cy_ldn.py + ngay.npz + dem.npz → ĐO THỬ 2 s (ngày, khung 0–47) → dựng hết (ngày 48–119, đêm 0–119)
#   → kéo PNG dần, đổi JPG ngay + xoá PNG (K29), KIỂM ĐỦ KHUNG trên máy rồi mới TẮT; pod báo xong mà thiếu khung > 2 lượt → LỖI + tắt (K26). Không cắt đầu ra ls (K25).
#   setsid nohup bash scripts/k2ldn/gpu/chay_t1.sh [tat-ca|keo|tat] > /var/tmp/ldn/log/pod-t1.log 2>&1 &
set -u
REPO=$(cd "$(dirname "$0")/../../.." && pwd); G=/var/tmp/ldn/gpu; P="/opt/cine/bin/python $REPO/scripts/k2ldn/gpu/pod.py"
RES=${RES:-960x540}; SPP_N=${SPP_N:-64}; SPP_D=${SPP_D:-96}
mkdir -p $G/ra/ngay $G/ra/dem
log() { echo "$(date -u +%H:%M:%S) $*"; }
thieu() { /opt/cine/bin/python -c "import os;print(sum(1 for f in range($2,$3+1) if not (os.path.exists('$G/ra/$1/%05d.jpg'%f) and os.path.getsize('$G/ra/$1/%05d.jpg'%f)>0)))"; }
keo() { for D in ngay dem; do for f in $($P ls out/$D 2>/dev/null | /opt/cine/bin/python -c "import json,sys
try: print(' '.join(x[0] for x in json.load(sys.stdin) if x[0].endswith('.png')))
except Exception: pass"); do j=$G/ra/$D/${f%.png}.jpg; [ -s $j ] && continue
  $P get out/$D/$f $G/ra/$D/$f > /dev/null 2>&1 && ffmpeg -nostdin -loglevel error -y -i $G/ra/$D/$f -q:v 2 $j && rm -f $G/ra/$D/$f || rm -f $G/ra/$D/$f $j; done; done; }
B=${1:-tat-ca}
if [ $B = tat-ca ]; then
  [ -f $G/pod.json ] || { log "BẬT pod"; $P len "NVIDIA GeForce RTX 5090" SECURE t1-lua 60 || exit 2; }
  rm -rf $G/co-so; mkdir -p $G/co-so/gpu; cp $REPO/scripts/k2ldn/gpu/pod_setup.sh $REPO/scripts/k2ldn/cy_ldn.py $G/co-so/gpu/; cp /var/tmp/ldn/cy/ngay.npz /var/tmp/ldn/cy/dem.npz $G/co-so/
  tar -cf $G/co-so.tar -C $G/co-so . && sha256sum $G/co-so.tar
  $P put $G/co-so.tar co-so.tar && $P run "cd /w && tar xf co-so.tar && bash /w/gpu/pod_setup.sh" --cho | tail -4
  log "ĐO THỬ 2 s (ngày khung 0–47)"; T0=$(date +%s)
  $P run "cd /w && ./blender/blender -b --factory-startup --python-exit-code 1 -P /w/gpu/cy_ldn.py -- /w/ngay.npz /w/out/ngay --res $RES --spp $SPP_N --frames 0:47 > /w/ngay-thu.log 2>&1; grep CY- /w/ngay-thu.log | tail -3" --cho | tail -4
  T1=$(date +%s); keo; log "ĐO THỬ xong: $((T1 - T0)) s đồng hồ / 48 khung; thiếu $(thieu ngay 0 47)"; echo "{\"do_thu\": \"ngay 0-47\", \"giay\": $((T1 - T0)), \"khung\": 48, \"res\": \"$RES\", \"spp\": $SPP_N}" > $G/do-thu.json
  log "DỰNG HẾT"; $P run "cd /w && ./blender/blender -b --factory-startup --python-exit-code 1 -P /w/gpu/cy_ldn.py -- /w/ngay.npz /w/out/ngay --res $RES --spp $SPP_N --frames 48:119 > /w/ngay.log 2>&1; ./blender/blender -b --factory-startup --python-exit-code 1 -P /w/gpu/cy_ldn.py -- /w/dem.npz /w/out/dem --res $RES --spp $SPP_D --frames 0:119 > /w/dem.log 2>&1; ./blender/blender -b --factory-startup --python-exit-code 1 -P /w/gpu/cy_ldn.py -- /w/dem.npz /w/out/dem1080 --res 1920x1080 --spp $SPP_D --still 96 > /w/dem1080.log 2>&1; ./blender/blender -b --factory-startup --python-exit-code 1 -P /w/gpu/cy_ldn.py -- /w/ngay.npz /w/out/ngay1080 --res 1920x1080 --spp $SPP_N --still 96 > /w/ngay1080.log 2>&1; echo POD-TAT-CA-XONG >> /w/dem.log" > /dev/null
  B=keo; fi
if [ $B = keo ]; then
  lan=0
  while true; do keo; tn=$(thieu ngay 0 119); td=$(thieu dem 0 119); xong=$($P run "grep -c POD-TAT-CA-XONG /w/dem.log" --cho 2>/dev/null | sed -n 2p)
    log "kéo: thiếu ngày $tn · đêm $td · xong=$xong"
    if [ "$tn" = 0 ] && [ "$td" = 0 ] && [ "${xong:-0}" -ge 1 ] 2>/dev/null; then
      for x in ngay1080 dem1080; do for f in $($P ls out/$x 2>/dev/null | /opt/cine/bin/python -c "import json,sys
try: print(' '.join(x[0] for x in json.load(sys.stdin) if x[0].endswith('.png')))
except Exception: pass"); do $P get out/$x/$f $G/ra/$x-$f > /dev/null 2>&1; done; done
      for l in ngay-thu ngay dem dem1080 ngay1080; do $P get $l.log $G/ra/pod-$l.log > /dev/null 2>&1; done; B=tat; break; fi
    if [ "${xong:-0}" -ge 1 ] 2>/dev/null; then lan=$((lan + 1)); log "pod báo xong nhưng còn thiếu — lượt $lan"; [ $lan -gt 2 ] && { log "LỖI: pod xong mà thiếu khung > 2 lượt — TẮT"; B=tat; break; }; sleep 20; continue; fi
    sleep 120; done; fi
if [ $B = tat ]; then log "TẮT pod (thiếu ngày $(thieu ngay 0 119), đêm $(thieu dem 0 119))"; $P tat; log TAT-XONG; fi
