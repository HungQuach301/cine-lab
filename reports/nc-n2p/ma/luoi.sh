#!/usr/bin/env bash
# NC-N2P · clip so (≤ 5 MB): ghép ngang N video cùng độ dài, mỗi ô 640×360 (2 ô) hoặc 426×240 (3 ô), có nhãn chữ trên ô; H.264 crf tự hạ tới khi ≤ 4,8 MB.
#   luoi.sh <ra.mp4> <nhãn1> <video1> <nhãn2> <video2> [<nhãn3> <video3>]
set -euo pipefail
OUT=$1; shift; N=$(( $# / 2 )); [ $N = 2 ] && { W=640; H=360; } || { W=426; H=240; }
IN=(); F=""; i=0
while [ $# -gt 0 ]; do L=$1; V=$2; shift 2; IN+=(-i "$V")
  F+="[$i:v]scale=$W:$H:flags=lanczos,setsar=1,fps=24,drawbox=x=0:y=0:w=iw:h=18:color=black@0.6:t=fill,drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:text='$L':x=5:y=3:fontsize=12:fontcolor=white[v$i];"; i=$((i+1)); done
S=""; for j in $(seq 0 $((N-1))); do S+="[v$j]"; done; F+="${S}hstack=inputs=$N[o]"
for CRF in 26 29 32 35; do ffmpeg -v error -y "${IN[@]}" -filter_complex "$F" -map "[o]" -an -c:v libx264 -preset veryslow -crf $CRF -pix_fmt yuv420p -movflags +faststart -shortest "$OUT"
  [ $(stat -c %s "$OUT") -le 4800000 ] && break; done
ls -la "$OUT"
