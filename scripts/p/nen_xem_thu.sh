#!/bin/bash
# Phiên P — NÉN CLIP XEM THỬ dưới trần dung lượng (mặc định 28 MB, dưới giới hạn 30 MB gửi qua giao diện — CLAUDE.md).
# Mã hoá 2 pass bitrate cố định như package.py (x264 slow, tune grain, BT.709, 24 fps), tiếng AAC 192 kb/s.
# Dùng:  bash scripts/p/nen_xem_thu.sh <vào.mp4> <ra.mp4> [MB=28] [bắt đầu s] [kết thúc s]
#   vd.  bash scripts/p/nen_xem_thu.sh design/cong5/layout/out/layout-v16.mp4 /tmp/xem_canh5.mp4 28 72 124.5
# Video > 30 MB: không gửi qua giao diện; đẩy lên nhánh git (CLAUDE.md).
set -e
IN=${1:?vào}; OUT=${2:?ra}; MB=${3:-28}; SS=$4; TO=$5
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$IN")
[ -n "$SS" ] && [ -n "$TO" ] && DUR=$(python3 -c "print($TO-$SS)")
VK=$(python3 -c "print(max(300,int($MB*8*1024/$DUR*0.93-192)))")   # kb/s hình, chừa 7 % + tiếng 192 kb/s
CUT=(); [ -n "$SS" ] && CUT+=(-ss "$SS"); [ -n "$TO" ] && CUT+=(-to "$TO")
P=$(mktemp -d)/x264
C=(-c:v libx264 -preset slow -b:v ${VK}k -tune grain -g 48 -pix_fmt yuv420p -color_primaries bt709 -color_trc bt709 -colorspace bt709 -r 24 -passlogfile "$P")
ffmpeg -nostdin -v error -y "${CUT[@]}" -i "$IN" "${C[@]}" -pass 1 -an -f null -
ffmpeg -nostdin -v error -y "${CUT[@]}" -i "$IN" "${C[@]}" -pass 2 -c:a aac -b:a 192k -movflags +faststart "$OUT"
rm -f "$P"*; ls -la "$OUT" | awk '{printf "%s: %.1f MB\n", $9, $5/1e6}'
