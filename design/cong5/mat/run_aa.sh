#!/bin/bash
# Cổng 5 · W3 — cổng mặt Ida A-α: ảnh thử 1920×1080, 3 mẫu, dựng ĐÚNG shot s37 của layout (khung phim thật: bộ cuối phố, Ida trên thang ở L11,
# faceCam 85 mm, facelight 'gas' + phơi sáng fl.exposure() × EK và lớp vẽ PAINT_CLOSE như W2 đã gắn), qua design/cong5/mat/page_layout_fl.js.
# Chỉ ghi đè biểu cảm Ida (và máy lệch 80° cho ảnh nghiêng). Không thêm đèn, không đổi phơi sáng/lớp vẽ của shot.
# Dùng: bash design/cong5/mat/run_aa.sh <thư mục ra> [tên...]   (tên: neutral sad_smile choked nghieng; mặc định: neutral)
# Mỗi ảnh là một việc < 60 s → LÀN NHANH của hàng đợi (LAN=nhanh).
set -u
WT=/home/user/cine-lab/.claude/worktrees/agent-a83d4075f6a9542ef
cd "$WT"; export PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers
O=${1:?}; shift; mkdir -p "$O"; NAMES=${@:-"neutral"}
L='"shot":"s37"'; [ -n "${EK:-}" ] && L="$L,\"dbg\":{\"ek\":$EK}"   # EK: thử hệ số phơi sáng của shot (mặc định của layout W2: 2,0)
args() { case "$1" in
  neutral|sad_smile|choked) echo "{$L,\"expr\":\"$1\"}" ;;
  nghieng) echo "{$L,\"expr\":\"sad_smile\",\"cam\":{\"yaw\":-80,\"dist\":1.1,\"y\":-0.02}}" ;;   # mặt nghiêng (so với s31)
  *) echo "tên ảnh lạ: $1" >&2; return 1 ;; esac; }
for n in $NAMES; do
  A=$(args "$n") || exit 2
  s=$(date +%s.%N)
  LAN=nhanh bash scripts/render/queue.sh W3 "mat-aa-$n" -- timeout 600 node design/cong5/mat/still.js --page cong5/mat/page_layout_fl.js --frame face_ida --out "$O/$n" --samples 3 --args "$A" 2>&1 | grep -iv "gpu stall" | grep -i "error\|queue" || true
  echo "$n $(echo "$(date +%s.%N) - $s" | bc)" >> "$O/thoi-gian.txt"
done
echo XONG >> "$O/thoi-gian.txt"
