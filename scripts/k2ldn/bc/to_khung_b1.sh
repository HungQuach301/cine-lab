#!/bin/bash
# BAN-CUOI-T4-B1 · tờ khung mỗi chương: khung đầu/giữa/cuối mỗi tệp 1080p đã dựng (đọc từ ban-cuoi/dung/<tệp>-1080p.mp4) → reports/ban-cuoi-t4-b1/to-khung-<chương>.jpg (≤ 2 MB)
#   bash scripts/k2ldn/bc/to_khung_b1.sh <hoi1|hoi3> <tệp …>
set -o pipefail
cd "$(dirname "$0")/../../.."; ch=$1; shift; T=/var/tmp/bc/tk; mkdir -p $T; A=()
for t in "$@"; do f=channel-k2/k2c-t4-02/ban-cuoi/dung/$t-1080p.mp4; [ -s $f ] || continue
  n=$(ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames -of csv=p=0 $f)
  for k in 0 $((n/2)) $((n-1)); do ffmpeg -nostdin -loglevel error -y -i $f -vf "select=eq(n\,$k)" -frames:v 1 -q:v 3 $T/$t-$k.jpg; A+=("$T/$t-$k.jpg::$t k$k/$n"); done; done
/opt/cine/bin/python scripts/k2ldn/bc/to_b1.py reports/ban-cuoi-t4-b1/to-khung-$ch.jpg "BAN-CUOI-T4-B1 · $ch · khung đầu / giữa / cuối (1080p look3-b1 cờ d, chưa LUT, chưa lớp chồng)" 3 420 "${A[@]}"
