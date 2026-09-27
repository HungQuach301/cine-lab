#!/bin/bash
# Cổng 3 đợt vá A2+ — render chính thức TUẦN TỰ các khung có thay đổi (V1–V5) + 2 khung cảnh 5 mã hoá lại (G3b).
# Thiết lập sản xuất v3 (1920×1080, 3 mẫu, PCF 1024, DOF hậu kỳ). Mã hoá A2+ (G3b): x264 CRF 12, tune grain, no-fast-pskip, deadzone 0
# (đo: bản 30 Mbps cũ chép grain ở shot tĩnh → tương quan khung kề 0,67; bản này 0,39 ≈ lossless 0,387).
cd "$(dirname "$0")/.."; export PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers
O=v2/out/a2p; RAW=${RAW:-/tmp/claude-0/a2praw}; mkdir -p $O $RAW
enc() { ffmpeg -hide_banner -loglevel error -y -f rawvideo -pix_fmt rgb24 -s 1920x1080 -framerate 24 -i "$1" \
  -vf 'vflip,scale=out_color_matrix=bt709:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p' -c:v libx264 -preset medium -tune grain \
  -profile:v high -crf 12 -g 48 -x264-params no-fast-pskip=1:deadzone-inter=0:deadzone-intra=0 -color_range tv -color_primaries bt709 -color_trc bt709 -colorspace bt709 -r 24 "$2"; }
for S in ${SHOTS:-a_close_ida b_cas_bird c_s5_wide c_s5_medium d_s6_alley e_ending}; do
  node shared/render_still.js --page v2/page.js --frame $S --out $RAW --samples 3 --frames 24 --args "{\"char\":\"3d\",\"shot\":\"$S\"}" 2>&1 | grep -o '"render_frame_s":[0-9.]*' | sed "s/^/$S /"
  cp $RAW/$S.png $RAW/$S.timing.json $O/ && enc $RAW/$S.rgb $O/$S.mp4 && rm -f $RAW/$S.rgb
done
for S in ${WALKS:-walk walk_cas}; do
  node shared/render_seq.js --page v2/page.js --shot $S --from 0 --to 48 --out $O --samples 3 --args "{\"char\":\"3d\"}" --pngs 0,24,47 --raw $RAW/$S.rgb 2>&1 | grep -o '"per_frame_s":{[^}]*}' | sed "s/^/$S /"
  enc $RAW/$S.rgb $O/$S.mp4 && rm -f $RAW/$S.rgb
done
echo XONG
