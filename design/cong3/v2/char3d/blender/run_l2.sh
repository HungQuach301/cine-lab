#!/bin/bash
# W4 · cửa mặt Ida lượt 2 — bộ khung thử (1920×1080, 3 mẫu, LÀN NẶNG). Dùng: bash design/cong3/v2/char3d/blender/run_l2.sh <thư mục ra> [pa] [s37] [so] [xuat]
#   pa   : 4 khung PA1 'bl' (máy của design/cong5/mat/pa_frames.json), L11 nâng 17,5° + lệch 25° khỏi trục máy; nhịp keep = choked
#   s37  : 2 khung chính diện s37 f2302 (neutral, choked) — đèn, facelight, phơi sáng như vòng A-i (page_layout_fl.js qua page_fl_bl.js)
#   so   : PA1_goodnight với 'aa' và 'ai' cùng đèn L11 nâng (để ghép bảng so sánh)
#   xuat : xuất glb Ida + máy + đèn của PA1_goodnight / PA1_keep cho Blender EEVEE (làn nhanh, 960×540, 1 mẫu)
set -u
WT=$(cd "$(dirname "$0")/../../../../.." && pwd); cd "$WT"; export PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers
O=${1:?}; shift; mkdir -p "$O"; WHAT=${@:-"pa s37 so xuat"}
PF=design/cong5/mat/pa_frames.json; L11='{"elev":17.5,"az":25}'
args() { node -e "const j=require('$WT/$PF'); const a={...j['$1']}; a.l11=$L11; Object.assign(a, $2); console.log(JSON.stringify(a))"; }
run() { local lab=$1 page=$2 a=$3; s=$(date +%s.%N)
  bash scripts/render/queue.sh W4 "$lab" -- timeout 900 node design/cong5/mat/still.js --page "$page" --frame x --out "$O/$lab" --samples 3 --args "$a" 2>&1 | grep -iv "gpu stall" | grep -i "error" || true
  echo "$lab $(echo "$(date +%s.%N) - $s" | bc)" >> "$O/thoi-gian.txt"; }
for w in $WHAT; do case "$w" in
  pa) for n in last goodnight brighter keep; do run "L2_BL_PA1_$n" cong3/v2/char3d/blender/page_l2.js "$(args PA1_$n '{"charOpts":{"idaStyle":"bl"}}')"; done ;;
  s37) for e in neutral choked; do run "L2_BL_s37_$e" cong3/v2/char3d/blender/page_fl_bl.js "{\"shot\":\"s37\",\"expr\":\"$e\"}"; done ;;
  so) for st in aa ai; do run "L2_SO_goodnight_$st" cong3/v2/char3d/blender/page_l2.js "$(args PA1_goodnight "{\"charOpts\":{\"idaStyle\":\"$st\"}}")"; done ;;
  xuat) for n in goodnight keep; do s=$(date +%s.%N)
      LAN=nhanh bash scripts/render/queue.sh W4 "L2_xuat_$n" -- timeout 300 node design/cong5/mat/still.js --page cong3/v2/char3d/blender/page_l2.js --frame x --out "$O/L2_xuat_$n" --samples 1 --w 960 --h 540 --args "$(args PA1_$n '{"charOpts":{"idaStyle":"bl"},"export":1}')" 2>&1 | grep -iv "gpu stall" | grep -i "error" || true
      echo "L2_xuat_$n $(echo "$(date +%s.%N) - $s" | bc)" >> "$O/thoi-gian.txt"; done ;;
esac; done
echo XONG >> "$O/thoi-gian.txt"
