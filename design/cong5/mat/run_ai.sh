#!/bin/bash
# Cổng 5 v2 · W3 — cửa mặt Ida A-i: bộ nộp mỗi vòng kiểm mù (P chạy kiểm).
#   4 ảnh 1920×1080, 3 mẫu, dựng ĐÚNG khung layout (design/cong5/mat/page_layout_fl.js — cùng bộ cảnh, đèn, facelight, phơi sáng EK của shot, lớp vẽ):
#     neutral, sad_smile, choked : s37 (khung giữa shot, f = 2302), chỉ ghi đè biểu cảm Ida
#     s39                        : s39 khung 2531 (khung P dùng ở lần 6), biểu cảm của layout (choked), mặt mới
#   1 clip 3 s (72 khung, 24 fps, 1920×1080, 2 mẫu): s37 từ f = 2266 (khung giữa −36), rãnh rig mặt design/cong5/mat/goodnight.js
#     (2 lần chớp + khẩu hình "Goodnight"), không ghi đè gì khác.
# Mọi việc là render NẶNG (≥ 1920×1080 / ≥ 2 mẫu / chuỗi khung) → làn nặng của hàng đợi.
# Dùng: bash design/cong5/mat/run_ai.sh <thư mục ra> [anh] [clip]
set -u
WT=/home/user/cine-lab/.claude/worktrees/agent-a83d4075f6a9542ef
cd "$WT"; export PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers
O=${1:?}; shift; mkdir -p "$O"; WHAT=${@:-"anh clip"}
T=$O/thoi-gian.txt
for w in $WHAT; do case "$w" in
  anh)
    for n in neutral sad_smile choked s39; do
      if [ "$n" = s39 ]; then A='{"shot":"s39","f":2531}'; else A="{\"shot\":\"s37\",\"expr\":\"$n\"}"; fi
      s=$(date +%s.%N)
      bash scripts/render/queue.sh W3 "ai-v1-$n" -- timeout 900 node design/cong5/mat/still.js --page cong5/mat/page_layout_fl.js --frame x --out "$O/$n" --samples 3 --args "$A" 2>&1 | grep -iv "gpu stall" | grep -i "error\|queue" || true
      echo "$n $(echo "$(date +%s.%N) - $s" | bc)" >> "$T"
    done ;;
  clip)
    TR=$(node design/cong5/mat/goodnight.js 72)
    s=$(date +%s.%N)
    bash scripts/render/queue.sh W3 "ai-v1-clip" -- timeout 7200 node design/cong5/mat/clip.js --page cong5/mat/page_layout_fl.js --out "$O/clip" --frames 72 --samples 2 --args "{\"shot\":\"s37\",\"f\":2266,\"track\":$TR}" 2>&1 | grep -iv "gpu stall" | grep -i "error\|queue\|khung\|frame_s" || true
    echo "clip $(echo "$(date +%s.%N) - $s" | bc)" >> "$T" ;;
esac; done
echo XONG >> "$T"
