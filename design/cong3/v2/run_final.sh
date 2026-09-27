#!/bin/bash
# Cổng 3 v2 — render chính thức TUẦN TỰ (máy rỗi) cho 2 cách làm nhân vật: 3 khung tĩnh + walk 96 khung (+24 khung không lớp vẽ để đo nhấp nháy).
# 1920×1080, 8 mẫu (thiết lập sản xuất; ngân sách ≤ 5 s/khung). Kết quả: v2/out/v2/<3d|2d>/
cd "$(dirname "$0")/.."; export PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers
RAW=${RAW:-/tmp/claude-0/v2raw}; mkdir -p $RAW
for C in 3d 2d; do
  O=v2/out/v2/$C; mkdir -p $O
  for S in a_close_ida b_cas_bird c_s5_wide; do
    node shared/render_still.js --page v2/page.js --frame $S --out $O --samples 8 --args "{\"char\":\"$C\",\"shot\":\"$S\"}" 2>&1 | grep -o '"render_frame_s":[0-9.]*' | sed "s/^/$C $S /"
  done
  node shared/render_seq.js --page v2/page.js --shot walk --from 0 --to 96 --out $O --samples 8 --args "{\"char\":\"$C\"}" --pngs 0,24,48,72,95 --mp4 $O/walk-$C.mp4 --raw $RAW/walk-$C-paint.rgb 2>&1 | grep -o '"per_frame_s":{[^}]*}' | sed "s/^/$C walk /"
  mkdir -p $O/nopaint
  node shared/render_seq.js --page v2/page.js --shot walk --from 0 --to 24 --out $O/nopaint --samples 8 --args "{\"char\":\"$C\",\"nopaint\":1}" --raw $RAW/walk-$C-nopaint.rgb 2>&1 | grep -o '"per_frame_s":{[^}]*}' | sed "s/^/$C walk-nopaint /"
done
