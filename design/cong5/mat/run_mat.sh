#!/bin/bash
# Cổng 5 · W3 — cổng mặt Ida A1: ảnh thử 1920×1080, 3 mẫu (cách render như lần 3: khung face_ida, vành mũ đã đẩy, góc gần chính diện).
# Chép từ design/cong4/mat/run_mat.sh; khác: đường dẫn về worktree W3, trang design/cong5/mat/page_mat.js (= face_ida của v2/page.js
# + ánh sáng cận mặt design/cong5/layout/facelight.js chế độ "gas" + phơi sáng không cháy da), mỗi ảnh là MỘT việc nặng trong hàng đợi.
# Dùng: bash design/cong5/mat/run_mat.sh <thư mục ra> [tên ảnh...]   (tên: neutral sad_smile choked nghieng co-ao_cu-chi; mặc định: cả 5)
set -u
WT=/home/user/cine-lab/.claude/worktrees/agent-a83d4075f6a9542ef
cd "$WT"; export PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers
O=${1:?}; shift; mkdir -p "$O"; NAMES=${@:-"neutral sad_smile choked nghieng co-ao_cu-chi"}
FL='"fl":{"mode":"gas"},"expose":"auto"'
FACE='"headTurn":35,"faceYaw":-10,"headPitch":-4,"faceQ":1.4,"faceY":-0.02,"faceDist":1.05,"gaze":[0.05,-0.04]'
args() { case "$1" in
  neutral|sad_smile|choked) echo "{$FL,\"dbg\":{\"expr\":\"$1\",\"pose\":\"ladder_rest\",$FACE}}" ;;
  nghieng)       echo "{$FL,\"dbg\":{\"expr\":\"sad_smile\",\"pose\":\"ladder_rest\",\"headTurn\":35,\"faceYaw\":-80,\"headPitch\":-4,\"faceQ\":1.4,\"faceY\":-0.02,\"faceDist\":1.05,\"gaze\":[0.05,-0.04]}}" ;;   # mặt nghiêng (so với s31)
  co-ao_cu-chi)  echo "{$FL,\"dbg\":{\"expr\":\"neutral\",\"pose\":\"hat_push_b\",\"headTurn\":35,\"faceYaw\":-10,\"headPitch\":-4,\"faceQ\":1.4,\"faceY\":-0.13,\"faceDist\":1.25,\"gaze\":[0.05,-0.04]}}" ;;   # cổ áo cận trong cử chỉ đẩy mũ
  *) echo "tên ảnh lạ: $1" >&2; return 1 ;; esac; }
for n in $NAMES; do
  A=$(args "$n") || exit 2
  s=$(date +%s.%N)
  bash scripts/render/queue.sh W3 "mat-a1-$n" -- timeout 600 node design/cong5/mat/still.js --page cong5/mat/page_mat.js --frame face_ida --out "$O/$n" --samples 3 --args "$A" 2>&1 | grep -iv "gpu stall" | grep -i "error\|queue" || true
  echo "$n $(echo "$(date +%s.%N) - $s" | bc)" >> "$O/thoi-gian.txt"
done
echo XONG >> "$O/thoi-gian.txt"
