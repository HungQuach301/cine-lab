#!/usr/bin/env bash
# BAN-CUOI-T3 (việc 5 + 10) · GHÉP + XUẤT bản cuối: các đoạn sec/<id>.mkv (render.js, crf 10 yuv444) theo timeline → LUT kênh (lut3d, tứ diện) → master H.264 High 1080p24 + AAC 48 kHz 320 kb/s (crf 17, trần 19 Mb/s);
#  3 phần 1080p chia ở ranh chương gần 1/3, 2/3; 8 tệp xem 640×360 theo chương (≤ 5 MB, x264 2 lượt); tiếng phần/xem: volume −1,2 dB + alimiter 0,75 level=disabled (BAI-HOC #45/#69/#121).
#   bash scripts/k2tl/cuoi_xuat.sh master|phan|xem   (O=/var/tmp/cine-out/k2c-t3-cuoi, LUT=channel-k2/k2c-t3-01/mau/<lut>.cube)
set -euo pipefail
REPO=$(cd "$(dirname "$0")/../.." && pwd); O=${O:-/var/tmp/cine-out/k2c-t3-cuoi}; TL=$O/timeline.json; LUT=${LUT:?đặt LUT=<tệp .cube>}; R=/var/tmp/cine-out/phat-hanh; mkdir -p $R
VF="lut3d=file=$LUT:interp=tetrahedral,scale=out_color_matrix=bt709:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p"; COL="-color_range tv -color_primaries bt709 -color_trc bt709 -colorspace bt709"
AF="volume=-1.2dB,alimiter=limit=0.75:level=disabled"
DUR=$(/opt/cine/bin/python -c "import json;print(json.load(open('$TL'))['tong_s'])")
# 22/10 22:40: crf 16 không trần cho 41 Mb/s = 3,9 GB > giới hạn 2 GB/tệp của GitHub LFS (gói thường) → crf 17 + trần 19 Mb/s (≤ ~1,8 GB);
# ranh 3 phần = ranh CHƯƠNG gần 1/3 và 2/3 thời lượng (bản trước lấy trường 'part' của đoạn → 173 s, sai) và đặt khung khoá ĐÚNG ranh để cắt phần bằng sao chép luồng hình (không mã hoá lại).
CHR="43.833 173.083 262.208 382.583 471.625 585.833 666.083"
read A B < <(/opt/cine/bin/python -c "b=[float(x) for x in '$CHR'.split()];T=$DUR;a=min(b,key=lambda x:abs(x-T/3));c=min([x for x in b if x>a],key=lambda x:abs(x-2*T/3));print(a,c)"); KF="$A,$B"
case ${1:-master} in
master)
  /opt/cine/bin/python - "$TL" "$O" <<'P'
import json, subprocess, sys
tl, O = json.load(open(sys.argv[1])), sys.argv[2]; bad = []
for s in tl['segments']:
    p = f"{O}/sec/{s['id']}.mkv"; n = int(subprocess.run(['ffprobe', '-v', 'error', '-count_packets', '-select_streams', 'v:0', '-show_entries', 'stream=nb_read_packets', '-of', 'csv=p=0', p], capture_output=True, text=True).stdout.strip() or 0)
    if n != s['frames']: bad.append(f"{s['id']}: {n}/{s['frames']}")
open(f'{O}/list.txt', 'w').write(''.join(f"file '{O}/sec/{s['id']}.mkv'\n" for s in tl['segments']))
if bad: sys.exit('LỆCH số khung: ' + ', '.join(bad))
P
  ffmpeg -nostdin -v error -y -f concat -safe 0 -i $O/list.txt -i $O/mix/mix.wav -map 0:v -map 1:a -vf "$VF" -c:v libx264 -preset slow -crf 17 -maxrate 19M -bufsize 38M -profile:v high -g 48 -force_key_frames "$KF" $COL -r 24 -fps_mode cfr \
    -c:a aac -b:a 320k -ar 48000 -movflags +faststart -t $DUR $R/k2-t3-v1-master.mp4
  ffprobe -v error -show_entries format=duration,bit_rate:stream=codec_name,profile,width,height,r_frame_rate,sample_rate,bit_rate -of json $R/k2-t3-v1-master.mp4 > $R/master-ffprobe.json; sha256sum $R/k2-t3-v1-master.mp4;;
phan)   # ranh chương gần 1/3 và 2/3 (A B tính ở trên)
  echo "ranh $A $B" > $R/phan-ranh.txt
  FA=$(/opt/cine/bin/python -c "print(round($A*24))"); FB=$(/opt/cine/bin/python -c "print(round($B*24))"); FT=$(/opt/cine/bin/python -c "print(round($DUR*24))")
  # hình: segment muxer cắt THEO CHỈ SỐ KHUNG tại khung khoá đặt sẵn (sao chép luồng). Bản -ss/-t sao chép lệch 1 khung: +1 ms làm khung khoá ranh có ts âm → bị gắn cờ bỏ.
  ffmpeg -nostdin -v error -y -i $R/k2-t3-v1-master.mp4 -map 0:v -c copy -f segment -segment_frames $FA,$FB -reset_timestamps 1 $O/phan-hinh-%d.mp4
  for k in 1 2 3; do case $k in 1) F0=0; N=$FA;; 2) F0=$FA; N=$((FB - FA));; 3) F0=$FB; N=$((FT - FB));; esac
    SS=$(/opt/cine/bin/python -c "print(f'{$F0/24:.6f}')"); DD=$(/opt/cine/bin/python -c "print(f'{$N/24:.6f}')")   # tiếng: giải mã + mã hoá lại → cắt chính xác mẫu
    ffmpeg -nostdin -v error -y -i $O/phan-hinh-$((k - 1)).mp4 -ss $SS -t $DD -i $R/k2-t3-v1-master.mp4 -map 0:v -map 1:a -c:v copy -af "$AF" -c:a aac -b:a 256k -ar 48000 -movflags +faststart $R/k2-t3-v1-p$k.mp4; done
  rm -f $O/phan-hinh-?.mp4
  sha256sum $R/k2-t3-v1-p?.mp4;;
xem)    # 8 tệp xem theo chương (tên/thứ tự như ANIMATIC-T3), ≤ 5 MB: tổng ≈ 4,7 MB → bitrate theo thời lượng
  X=$REPO/reports/ban-cuoi-t3/xem; mkdir -p $X
  while read NAME A B; do D=$(echo "$B - $A" | bc -l); BR=$(/opt/cine/bin/python -c "print(int(4.6e6*8/$D/1000) - 96)")
    for p in 1 2; do OUTP=/dev/null; [ $p = 2 ] && OUTP=$X/$NAME.mp4
      ffmpeg -nostdin -v error -y -ss $A -t $D -i $R/k2-t3-v1-master.mp4 -vf scale=640:360:flags=lanczos -c:v libx264 -preset slow -b:v ${BR}k -pass $p -passlogfile $O/xem-$NAME -profile:v high -g 48 -r 24 \
        -af "$AF" -c:a aac -b:a 96k -ar 48000 -movflags +faststart $( [ $p = 1 ] && echo "-an -f mp4" ) $OUTP; done
    ls -la $X/$NAME.mp4 | awk '{print $5, $9}'; done <<'L'
01-mo-dau 0 43.833
02-ch1-rock-1704 43.833 173.083
03-ch2a-vay-ham 173.083 262.208
04-ch2b-tan-cong-1782 262.208 382.583
05-ch3-dat-trung-lap 382.583 471.625
06-ch4-duong-bang 471.625 585.833
07-ch5a-cong 585.833 666.083
08-ch5b-ket 666.083 762.0
L
  ;;
esac
