#!/usr/bin/env bash
# V7-PILOT T3 · DỰNG BẢN THỬ 540p ≈ 2 phút (một lệnh, chạy lại được — build.sh giữ cảnh/đoạn có dấu không đổi):
#   1) sinh đặc tả (v7p/mk_ep_v7p.py) → 2) prep + render (scripts/k2/build.sh, K2_DRAFT=1 MW=960; cảnh tl/t3tl V6 SX llvmpipe, P cảnh song song)
#   3) nền nhạc tạm (Tyrant.mp3 — RIGHTS K2-MUS; ElevenLabs 0) · 4) ghép master 960×540 · 5) ĐƯỜNG RAY LỜI TẠM (phụ đề v7p/ray-loi.srt nung lên bản xem, KHÔNG lên bản cuối)
#      → bản 540p ngoài git + bản xem ≤ 5 MB trong git (reports/v7p/ban-thu/v7p-xem.mp4)
#   bash scripts/k2tl/v7p_dung.sh [bước: spec render mix ghep ray] · P=3 J=2
set -euo pipefail
REPO=$(cd "$(dirname "$0")/../.." && pwd); PY=/opt/cine/bin/python; EPD=$REPO/channel-k2/k2c-t3-01/v7p; EPY=$EPD/episode.yaml
export K2TL_CACHE=${K2TL_CACHE:-/var/tmp/cine-out/k2tl-cache} K2_DRAFT=1 MW=960 PARTS=0
O=/var/tmp/cine-out/k2c-t3-v7p; mkdir -p $O; STEPS=${*:-spec render mix ghep ray}; has() { [[ " $STEPS " == *" $1 "* ]]; }
has spec && { $PY -I $EPD/mk_ep_v7p.py; bash $REPO/scripts/k2/build.sh $EPY prep > $O.prep.log 2>&1 || { tail $O.prep.log; exit 2; }; }
has render && P=${P:-3} J=${J:-2} bash $REPO/scripts/k2/build.sh $EPY render
if has mix; then DUR=$($PY -c "import json;print(json.load(open('$O/timeline.json'))['tong_s'])")
  ffmpeg -v error -y -stream_loop -1 -ss 2.55 -i $REPO/assets/k2/music/Tyrant.mp3 -t $DUR -af "loudnorm=I=-18:TP=-2:LRA=11,afade=t=in:d=1.5,afade=t=out:st=$(echo "$DUR - 4" | bc -l):d=4" -ar 48000 -ac 2 $O/mix.wav; fi
has ghep && bash $REPO/scripts/k2/build.sh $EPY ghep
if has ray; then M=$O/k2c-t3-v7p-v1-master.mp4; R=$O/k2c-t3-v7p-540p-ray.mp4; X=$REPO/reports/v7p/ban-thu/v7p-xem.mp4; mkdir -p $(dirname $X)
  ffmpeg -v error -y -i $M -vf "subtitles=$EPD/ray-loi.srt:force_style='FontName=DejaVu Sans,FontSize=15,PrimaryColour=&H00FFFFFF,OutlineColour=&H80000000,BorderStyle=3,Outline=1,Shadow=0,MarginV=28'" \
    -c:v libx264 -preset slow -b:v 2300k -maxrate 3000k -bufsize 6000k -c:a aac -b:a 96k -movflags +faststart $R
  ffmpeg -v error -y -i $R -vf "scale=640:360:flags=lanczos,fps=24" -c:v libx264 -preset veryslow -crf 33 -c:a aac -b:a 32k -ac 1 -movflags +faststart $X
  S=$(stat -c %s $X); if [ $S -gt 5000000 ]; then ffmpeg -v error -y -i $R -vf "scale=640:360:flags=lanczos,fps=24" -c:v libx264 -preset veryslow -b:v $(( (4600000*8/120 - 32000) / 1000 ))k -c:a aac -b:a 32k -ac 1 -movflags +faststart $X; fi
  sha256sum $M $R $X | tee $O/SHA256-v7p.txt; ls -la $X; fi
