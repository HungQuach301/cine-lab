#!/bin/bash
# Đợt vá A2+ — xuất file đi kèm cho checks/run.py từ chính trang render (bộ xuất đã sửa: mặt nạ alpha 0 ngoài bộ phận).
cd "$(dirname "$0")/.."; export PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers
O=v2/out/a2p
mk() { # $1 shot  $2 parts  $3 motion  $4 duration_s
  node shared/export_sidecars.js --page v2/page.js --shot $1 --video $O/$1.mp4 --parts $2 --scale 4 --motion $3 --args "{\"char\":\"3d\"}" 2>&1 | grep -v '^\[page\]' | tail -1 | cut -c1-200
  mkdir -p $O/$1.stems
  ffmpeg -v error -y -f lavfi -i anullsrc=r=48000:cl=mono -t $4 -c:a pcm_s16le $O/$1.stems/dialogue.wav
  ffmpeg -v error -y -f lavfi -i anullsrc=r=48000:cl=stereo -t $4 -c:a pcm_s16le $O/$1.stems/me.wav
  printf '{"workdir": "design/cong3/v2", "scene_files": ["design/cong3/v2/page.js"], "assets": []}\n' > $O/$1.assets.json
}
for S in ${SHOTS:-a_close_ida b_cas_bird c_s5_wide c_s5_medium d_s6_alley e_ending}; do mk $S 0,12 0:24 1; done
for S in ${WALKS:-walk walk_cas}; do mk $S 0,12,24,36 0:48 2; done
echo XONG
