#!/bin/bash
# Cổng 3 v3 — xuất file đi kèm cho checks/run.py từ chính trang render (v2/page.js): mặt nạ C3 4×, motion, text rỗng, script rỗng,
# stem im lặng (clip không có âm), assets.json. Chạy từ design/cong3.
cd "$(dirname "$0")/.."; export PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers
O=v2/out
mk() { # $1 shot  $2 parts  $3 motion-range  $4 duration_s
  node shared/export_sidecars.js --page v2/page.js --shot $1 --video $O/$1.mp4 --parts $2 --scale 4 --motion $3 --args "{\"char\":\"3d\"}" 2>&1 | grep -v '^\[page\]' | tail -2
  mkdir -p $O/$1.stems
  ffmpeg -v error -y -f lavfi -i anullsrc=r=48000:cl=mono -t $4 -c:a pcm_s16le $O/$1.stems/dialogue.wav
  ffmpeg -v error -y -f lavfi -i anullsrc=r=48000:cl=stereo -t $4 -c:a pcm_s16le $O/$1.stems/me.wav
  printf '{"workdir": "design/cong3/v2", "scene_files": ["design/cong3/v2/page.js"], "assets": []}\n' > $O/$1.assets.json
}
for S in ${SHOTS:-s1_opening a_close_ida b_cas_bird c_s5_wide c_s5_medium d_s6_alley e_ending}; do mk $S 0,12 0:24 1; done
for S in ${WALKS:-walk walk_cas}; do mk $S 0,12,24,36 0:48 2; done
echo XONG
