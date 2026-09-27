#!/bin/bash
# Xuất lại CHỈ motion.json (track trên vùng có chi tiết) — không đụng mặt nạ đã nộp kiểm toán.
cd "$(dirname "$0")/.."; export PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers; O=v2/out
for S in s1_opening a_close_ida b_cas_bird c_s5_wide c_s5_medium d_s6_alley e_ending; do node shared/export_sidecars.js --page v2/page.js --shot $S --video $O/$S.mp4 --motion 0:24 --args '{"char":"3d"}' 2>&1 | grep -v '^\[page\]' | tail -1; done
for S in walk walk_cas; do node shared/export_sidecars.js --page v2/page.js --shot $S --video $O/$S.mp4 --motion 0:48 --args '{"char":"3d"}' 2>&1 | grep -v '^\[page\]' | tail -1; done
echo XONG
