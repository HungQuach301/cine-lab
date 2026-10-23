#!/usr/bin/env bash
# LOOK-T4-V2 · MỘT khung Cycles GPU (RunPod RTX 5090 SECURE) cùng máy/giờ với khung lửa M2-dem (2/9/1666 23:00 từ giữa sông) để chủ dự án so với cách A mới.
#   bật → cài Blender 5.2.2 (pod_setup.sh) → tải cy_ldn.py + cy-M2-dem.npz → dựng 1 khung 1920×1080 (spp $SPP) — khung này CHÍNH là lần đo → kéo PNG, KIỂM có tệp → TẮT NGAY.
#   setsid nohup bash scripts/k2ldn/gpu/chay_cy_v2.sh > /var/tmp/ldn/log/pod-cy.log 2>&1 &
set -u
REPO=$(cd "$(dirname "$0")/../../.." && pwd); G=/var/tmp/ldn/gpu; export NCG_LEDGER=$REPO/reports/look-t4-v2/gio-gpu.jsonl; P="/opt/cine/bin/python $REPO/scripts/k2ldn/gpu/pod.py"
SPP=${SPP:-48}; mkdir -p $G/ra; log() { echo "$(date -u +%H:%M:%S) $*"; }
tat() { log "TẮT pod"; $P tat; log TAT-XONG; }
trap tat EXIT
log "BẬT pod"; $P len "${GPU:-NVIDIA GeForce RTX 5090}" SECURE v2-cy 40 || { log "LỖI bật pod"; trap - EXIT; exit 2; }
rm -rf $G/co-so; mkdir -p $G/co-so/gpu; cp $REPO/scripts/k2ldn/gpu/pod_setup.sh $REPO/scripts/k2ldn/${CY:-cy_ldn}.py $G/co-so/gpu/; cp /var/tmp/ldn/v2/cy-M2-dem.npz $G/co-so/
tar -cf $G/co-so.tar -C $G/co-so . && sha256sum $G/co-so.tar
T0=$(date +%s); $P put $G/co-so.tar co-so.tar && $P run "cd /w && tar xf co-so.tar && bash /w/gpu/pod_setup.sh" --cho | tail -3; T1=$(date +%s); log "cài + tải: $((T1 - T0)) s"
$P run "cd /w && ./blender/blender -b --factory-startup --python-exit-code 1 -P /w/gpu/${CY:-cy_ldn}.py -- /w/cy-M2-dem.npz /w/out/dem --res 1920x1080 --spp $SPP --still 0 > /w/cy.log 2>&1; grep CY- /w/cy.log | tail -4; ls -la /w/out/dem" --cho | tail -8
T2=$(date +%s); log "dựng 1 khung (gồm nạp cảnh): $((T2 - T1)) s"
$P get out/dem/00000.png $G/ra/${TAG:-cy-M2-dem}.png && $P get cy.log $G/ra/${TAG:-cy-M2-dem}.log
test -s $G/ra/${TAG:-cy-M2-dem}.png && log "CÓ KHUNG $(sha256sum $G/ra/${TAG:-cy-M2-dem}.png)" || log "LỖI: không có khung"
echo "{\"cai_tai_s\": $((T1 - T0)), \"dung_s\": $((T2 - T1)), \"spp\": $SPP, \"res\": \"1920x1080\"}" > $G/ra/${TAG:-cy-M2-dem}-gio.json
