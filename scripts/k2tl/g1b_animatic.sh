#!/usr/bin/env bash
# G1b T3 · DỰNG ANIMATIC 540p TOÀN TẬP (một lệnh, chạy lại được — build.sh giữ cảnh/đoạn có dấu không đổi):
#   1) sinh đặc tả (g1b/mk_ep_g1b.py) → 2) prep + render (scripts/k2/build.sh, K2_DRAFT=1 MW=960; cảnh 3D V6 SX llvmpipe, P cảnh song song, J đoạn song song)
#   3) nền nhạc tạm (assets/k2/music/Tyrant.mp3 — dòng RIGHTS K2-MUS; chưa có lời: ElevenLabs 0) → mix.wav −18 LUFS · 4) ghép master 960×540 (PARTS=0)
#   5) ĐƯỜNG RAY LỜI TẠM: phụ đề g1b/ray-loi.srt nung lên bản xem (KHÔNG lên bản cuối) → <out>/k2c-t3-g1b-animatic-540p-ray.mp4 (≈ 2,5 Mb/s, ngoài git)
#      + bản xem ≤ 5 MB cho git (480×270, 12 fps) → reports/g1b-t3/animatic/animatic-270p-xem.mp4
#   bash scripts/k2tl/g1b_animatic.sh [bước: spec render mix ghep ray]   (mặc định tất cả) · P=2 J=2
set -euo pipefail
REPO=$(cd "$(dirname "$0")/../.." && pwd); PY=/opt/cine/bin/python; EPD=$REPO/channel-k2/k2c-t3-01/g1b; EPY=$EPD/episode.yaml
export K2TL_CACHE=${K2TL_CACHE:-/var/tmp/cine-out/k2tl-cache} K2_DRAFT=1 MW=960 PARTS=0
O=/var/tmp/cine-out/k2c-t3-g1b; STEPS=${*:-spec render mix ghep ray}; has() { [[ " $STEPS " == *" $1 "* ]]; }
has spec && { $PY -I $EPD/mk_ep_g1b.py; bash $REPO/scripts/k2/build.sh $EPY prep > $O.prep.log 2>&1 || { tail $O.prep.log; exit 2; }; }
has render && P=${P:-2} J=${J:-2} bash $REPO/scripts/k2/build.sh $EPY render
if has mix; then DUR=$($PY -c "import json;print(json.load(open('$O/timeline.json'))['tong_s'])")
  ffmpeg -v error -y -stream_loop -1 -ss 2.55 -i $REPO/assets/k2/music/Tyrant.mp3 -t $DUR -af "loudnorm=I=-18:TP=-2:LRA=11,afade=t=in:d=1.5,afade=t=out:st=$(echo "$DUR - 4" | bc -l):d=4" -ar 48000 -ac 2 $O/mix.wav; fi
has ghep && bash $REPO/scripts/k2/build.sh $EPY ghep
if has ray; then M=$O/k2c-t3-g1b-v1-master.mp4; R=$O/k2c-t3-g1b-animatic-540p-ray.mp4; mkdir -p $REPO/reports/g1b-t3/animatic
  ffmpeg -v error -y -i $M -vf "subtitles=$EPD/ray-loi.srt:force_style='FontName=DejaVu Sans,FontSize=15,PrimaryColour=&H00FFFFFF,OutlineColour=&H80000000,BorderStyle=3,Outline=1,Shadow=0,MarginV=28'" \
    -c:v libx264 -preset slow -b:v 2300k -maxrate 3000k -bufsize 6000k -c:a aac -b:a 96k -movflags +faststart $R
  ffmpeg -v error -y -i $R -vf "scale=480:270:flags=lanczos,fps=12" -c:v libx264 -preset veryslow -crf 41 -c:a aac -b:a 24k -ac 1 -movflags +faststart $REPO/reports/g1b-t3/animatic/animatic-270p-xem.mp4
  sha256sum $M $R $REPO/reports/g1b-t3/animatic/animatic-270p-xem.mp4 | tee $O/SHA256-animatic.txt
  ls -la $REPO/reports/g1b-t3/animatic/animatic-270p-xem.mp4; fi
