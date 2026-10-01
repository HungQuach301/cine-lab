#!/bin/bash
# Cine Lab · Last Lamplighters · animatic v3 — ghép cả tập từ các clip đoạn (FFV1) + âm thanh, mã hoá 3 bản, đo.
# bash scripts/p/ghep_ep01.sh [timeline.json] [thư mục ra]
#   vào: /var/tmp/cine-out/ep01/sec/<NN>.mkv (đúng số khung theo timeline), /var/tmp/cine-out/ep01/sfx/*.json
#   ra : <ra>/ll-ep01-animatic-v3-master.mp4 (crf 16, ngoài git), <ra>/ll-ep01-animatic-v3.mp4 (bản xem ≤ 90 MB, 2 lượt),
#        <ra>/ll-ep01-animatic-v3-720p.mp4 (≤ 60 MB), <ra>/do.txt (khung, judder, loudness, dung lượng)
set -e
REPO=$(cd "$(dirname "$0")/../.." && pwd)
TL=${1:-$REPO/reports/m3/m2-2b/timeline-v3.json}
O=${2:-/var/tmp/cine-out/ep01/out}; S=/var/tmp/cine-out/ep01/sec
mkdir -p $O/pass
PY=/opt/cine/bin/python
# 1) kiểm số khung từng đoạn + danh sách ghép
$PY - "$TL" "$S" "$O/list.txt" <<'E'
import json, subprocess, sys
tl, S, out = json.load(open(sys.argv[1])), sys.argv[2], sys.argv[3]
L, bad = [], []
for d in tl['doan']:
    p = f"{S}/{d['n']}.mkv"; need = d['khung'][1] - d['khung'][0]
    n = int(subprocess.run(['ffprobe', '-v', 'error', '-count_packets', '-select_streams', 'v:0', '-show_entries', 'stream=nb_read_packets', '-of', 'csv=p=0', p], capture_output=True, text=True).stdout.strip() or 0)
    print(d['n'], need, n, 'OK' if n == need else 'LỆCH'); bad += [d['n']] if n != need else []; L.append(f"file '{p}'")
open(out, 'w').write('\n'.join(L) + '\n')
if bad: sys.exit('LỆCH số khung: ' + ', '.join(bad))
E
# 2) âm thanh
$PY $REPO/scripts/p/mix_ep01.py "$TL" /var/tmp/cine-out/ep01/sfx $O/mix.wav
DUR=$($PY -c "import json;print(json.load(open('$TL'))['tong_s'])")
VF="scale=out_color_matrix=bt709:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p"
COL="-color_range tv -color_primaries bt709 -color_trc bt709 -colorspace bt709"
T0=$(date +%s)
# 3) master (ngoài git)
ffmpeg -v error -y -f concat -safe 0 -i $O/list.txt -i $O/mix.wav -map 0:v -map 1:a -vf "$VF" -c:v libx264 -preset slow -crf 16 -profile:v high -g 48 $COL -r 24 -fps_mode cfr \
  -c:a aac -b:a 256k -ar 48000 -movflags +faststart -t $DUR $O/ll-ep01-animatic-v3-master.mp4
T1=$(date +%s)
# 4) bản xem 1080p ≤ 90 MB: 2 lượt, đích 86 MB tổng (âm 128 kb/s)
VB=$($PY -c "print(int((86e6*8/$DUR - 128e3)/1000))")
for p in 1 2; do
  OUTP=/dev/null; [ $p = 2 ] && OUTP=$O/ll-ep01-animatic-v3.mp4
  ffmpeg -v error -y -f concat -safe 0 -i $O/list.txt -i $O/mix.wav -map 0:v -map 1:a -vf "$VF" -c:v libx264 -preset slow -b:v ${VB}k -pass $p -passlogfile $O/pass/x1080 \
    -profile:v high -g 48 $COL -r 24 -fps_mode cfr -c:a aac -b:a 128k -ar 48000 -movflags +faststart -t $DUR $( [ $p = 1 ] && echo "-an -f mp4" ) $OUTP
done
T2=$(date +%s)
# 5) 720p ≤ 60 MB: 2 lượt, đích 56 MB
VB7=$($PY -c "print(int((56e6*8/$DUR - 128e3)/1000))")
for p in 1 2; do
  OUTP=/dev/null; [ $p = 2 ] && OUTP=$O/ll-ep01-animatic-v3-720p.mp4
  ffmpeg -v error -y -f concat -safe 0 -i $O/list.txt -i $O/mix.wav -map 0:v -map 1:a -vf "scale=1280:720:flags=lanczos:out_color_matrix=bt709:out_range=tv,format=yuv420p" \
    -c:v libx264 -preset slow -b:v ${VB7}k -pass $p -passlogfile $O/pass/x720 -profile:v high -g 48 $COL -r 24 -fps_mode cfr -c:a aac -b:a 128k -ar 48000 -movflags +faststart -t $DUR \
    $( [ $p = 1 ] && echo "-an -f mp4" ) $OUTP
done
T3=$(date +%s)
echo "ma_hoa_s master $((T1-T0)) xem1080 $((T2-T1)) 720p $((T3-T2)) | bitrate hình xem1080 ${VB}k, 720p ${VB7}k" > $O/do.txt
# 6) đo
for f in ll-ep01-animatic-v3-master.mp4 ll-ep01-animatic-v3.mp4 ll-ep01-animatic-v3-720p.mp4; do
  python3 $REPO/scripts/p/judder.py $O/$f --json $O/judder-$f.json > /dev/null || true
  python3 -c "import json;d=json.load(open('$O/judder-$f.json'));print('$f',{k:d[k] for k in ('so_khung','thoi_luong_s','loi','loi_khung','giu_ngan_13_23','giu_co_y_ge_1s','giay_nhip_duoi_12')})" >> $O/do.txt
  ffmpeg -nostats -i $O/$f -af ebur128=peak=true -f null - 2>&1 | grep -E '^\s+(I|LRA|Peak):' | tr -s ' ' | tr '\n' ' ' >> $O/do.txt; echo >> $O/do.txt
  stat -c '%n %s' $O/$f >> $O/do.txt
done
echo XONG >> $O/do.txt
cat $O/do.txt
