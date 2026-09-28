#!/bin/bash
# Cổng 5 v2 · W3 — khung thử phương án dàn dựng lại câu L4 (design/cong5/mat/pa_frames.json → page_pa.js).
# Dùng: bash design/cong5/mat/run_pa.sh <thư mục ra> [tên khung…]      (mặc định: mọi khung trong pa_frames.json)
#   CHE=nhanh → thử 960×540, 1 mẫu, làn nhanh;  mặc định → 1920×1080, 3 mẫu, LÀN NẶNG.
#   Khung tên *_ai: cùng args với khung không hậu tố, mặt A-i (idaStyle 'ai'); còn lại mặt A-α (idaStyle 'aa', bản khoá v1.4).
set -u
WT=/home/user/cine-lab/.claude/worktrees/agent-a83d4075f6a9542ef
cd "$WT"; export PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers
O=${1:?}; shift; mkdir -p "$O"
NAMES=${@:-$(node -e "const j=require('$WT/design/cong5/mat/pa_frames.json'); console.log(Object.keys(j).filter(k=>!k.startsWith('_')).join(' '))")}
for n in $NAMES; do
  A=$(node -e "const j=require('$WT/design/cong5/mat/pa_frames.json'); const ai='$n'.endsWith('_ai'); const a={...j['$n'.replace(/_ai\$/,'')]}; a.charOpts={idaStyle: ai?'ai':'aa'}; console.log(JSON.stringify(a))")
  s=$(date +%s.%N)
  if [ "${CHE:-}" = nhanh ]; then
    LAN=nhanh bash scripts/render/queue.sh W3 "pa-thu-$n" -- timeout 300 node design/cong5/mat/still.js --page cong5/mat/page_pa.js --frame x --out "$O/$n" --samples 1 --w 960 --h 540 --args "$A" 2>&1 | grep -iv "gpu stall" | grep -i "error" || true
  else
    bash scripts/render/queue.sh W3 "pa-$n" -- timeout 900 node design/cong5/mat/still.js --page cong5/mat/page_pa.js --frame x --out "$O/$n" --samples 3 --args "$A" 2>&1 | grep -iv "gpu stall" | grep -i "error" || true
  fi
  echo "$n $(echo "$(date +%s.%N) - $s" | bc)" >> "$O/thoi-gian.txt"
done
echo XONG >> "$O/thoi-gian.txt"
