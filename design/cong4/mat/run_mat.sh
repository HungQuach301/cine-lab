#!/bin/bash
# Cổng 4 · Việc 1 — cổng mặt Ida: cử chỉ đẩy mũ (trước/sau) + 3 biểu cảm, vành mũ đã đẩy, góc gần chính diện.
# Dùng: bash design/cong4/mat/run_mat.sh <thư mục ra> [biểu cảm...]
set -e
cd /home/user/cine-lab/design/cong3
O=${1:?}; shift; mkdir -p "$O"; EXPRS=${@:-"neutral sad_smile choked"}
FACE='"headTurn":35,"faceYaw":-10,"headPitch":-4,"faceQ":1.4,"faceY":-0.02,"faceDist":1.05,"gaze":[0.05,-0.04]'
t(){ local s=$(date +%s.%N); timeout 400 node shared/render_still.js --page v2/page.js --frame face_ida --out "$O/$1" --samples 3 --args "$2" 2>&1 | grep -iv "gpu stall" | grep -i "error" || true; echo "$1 $(echo "$(date +%s.%N) - $s" | bc)" >> "$O/thoi-gian.txt"; }
if [ -z "$SKIP_GESTURE" ]; then
  t cu-chi_truoc '{"char":"3d","dbg":{"expr":"neutral","pose":"hat_push_a","headTurn":35,"faceYaw":-10,"headPitch":-4,"faceDist":1.9,"faceY":-0.05}}'
  t cu-chi_sau   '{"char":"3d","dbg":{"expr":"neutral","pose":"hat_push_b","headTurn":35,"faceYaw":-10,"headPitch":-4,"faceDist":1.9,"faceY":-0.05}}'
fi
for e in $EXPRS; do t "$e" "{\"char\":\"3d\",\"dbg\":{\"expr\":\"$e\",\"pose\":\"ladder_rest\",$FACE}}"; done
echo XONG >> "$O/thoi-gian.txt"
