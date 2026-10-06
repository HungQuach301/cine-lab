#!/bin/bash
# Last Lamplighters · nhà máy — MỘT LỆNH cho một tập: đặc tả → lời → render → mix → ghép master + bản xem 3 phần + Shorts.
#   bash scripts/ll/build.sh <episode.yaml> [bước…]      bước: prep render mix ghep shorts (mặc định: tất cả)
#   Biến: J=3 (số đoạn render song song), ONLY="02 05" (chỉ render các đoạn này), V=v1 (hậu tố tên tệp), ASR=0 (bỏ kiểm ASR)
# Ra (ngoài git, thư mục out của đặc tả, mặc định /var/tmp/cine-out/<id>):
#   sec/<id>.mkv (+ .log.json, .hash) · mix.wav · <id>-<V>-master.mp4 (crf 16) · <id>-<V>-p1/p2/p3.mp4 (720p ≈ 3 Mb/s, ≤ 90 MB, cắt ở ranh giới đoạn)
#   shorts/<S>.mp4 (1080×1920) · build.json (số khung, thời gian, đĩa)
# Chỉ render lại đoạn có đặc tả đổi (băm SHA-1 của đoạn trong timeline). Đĩa: dừng nếu trống < 3 GB (CHUAN-KENH §6.2).
set -e
REPO=$(cd "$(dirname "$0")/../.." && pwd); PY=/opt/cine/bin/python; LL=$REPO/scripts/ll
EP=$(realpath "$1"); shift; STEPS=${*:-prep render mix ghep shorts}; J=${J:-3}; V=${V:-v1}
O=$($PY -c "import yaml,sys;e=yaml.safe_load(open('$EP'));print(e.get('out') or '/var/tmp/cine-out/'+e['id'])"); ID=$($PY -c "import yaml;print(yaml.safe_load(open('$EP'))['id'])")
mkdir -p $O/sec $O/shorts $O/pass; TL=$O/timeline.json
disk() { local a=$(df --output=avail -k / | tail -1); echo "$(date +%H:%M) $1: đĩa trống $((a/1024)) MB" >> $O/build.log; [ $a -gt 3000000 ] || { echo "đĩa trống < 3 GB — dừng"; exit 2; }; }
has() { [[ " $STEPS " == *" $1 "* ]]; }
T0=$(date +%s)
# Test thư viện trước mỗi lần build (NHÀ MÁY v1.1 mục 6; TESTS=0 để bỏ)
if [ "${TESTS:-1}" = 1 ] && has render; then bash $LL/tests/run.sh > $O/tests.log 2>&1 || { tail -5 $O/tests.log; echo "Test thư viện TRƯỢT — dừng"; exit 5; }; fi
# ASR (mục B5, 05/10/2026): nghe lại từng đoạn lời bằng faster-whisper; thiếu số/tên riêng → tự thu lại đoạn đó (≤ 2 lần) rồi mới prep. ASR=0 để bỏ qua.
has prep && [ "${ASR:-1}" = 1 ] && { set +e; $PY $LL/asr.py "$EP" > $O/asr.log 2>&1; r=$?; set -e; tail -1 $O/asr.log; [ $r = 0 ] || { echo "ASR trượt sau 2 lần thu lại — dừng (xem $O/asr.json)"; exit 4; }; }
has prep && { $PY $LL/ll.py prep "$EP" | tee $O/prep.json; }
# Luật nhịp Q14–Q18 (chủ dự án 05/10/2026) đo trên timeline trước khi render; RHYTHM=0 để bỏ (tập ≤ 3 không áp)
if [ "${RHYTHM:-1}" = 1 ] && has render; then $PY $LL/rhythm.py "$EP" | tee $O/rhythm.txt || { echo "Luật nhịp TRƯỢT — sửa đặc tả trước khi render"; exit 6; }; fi
segs() { $PY -c "import json;[print(s['id']) for s in json.load(open('$TL'))['$1']]"; }
hash_of() { $PY -c "import json,hashlib,sys;t=json.load(open('$TL'));s=[x for x in t['$1'] if x['id']=='$2'][0];print(hashlib.sha1(json.dumps(s,sort_keys=True).encode()+open('$LL/render.js','rb').read()+b''.join(open('$LL/lib/'+f,'rb').read() for f in sorted(__import__('os').listdir('$LL/lib')) if f.endswith('.js'))).hexdigest())"; }
render_one() { # $1 kind (segments|shorts) $2 id $3 out
  local h=$(hash_of $1 $2); [ -n "$h" ] || { echo "LỖI băm đoạn $2"; touch $O/render.failed; return; }; [ -f $3 ] && [ "$(cat $3.hash 2>/dev/null)" = "$h" ] && { echo "giữ $2"; return; }
  local flag=--seg; [ $1 = shorts ] && flag=--short
  if node $LL/render.js --tl $TL $flag $2 --out $3 2>>$O/render-$2.err; then echo $h > $3.hash; python3 $REPO/scripts/p/judder.py $3 --json $3.judder.json > /dev/null || true
  else echo "LỖI render $2 (xem $O/render-$2.err)"; touch $O/render.failed; fi
}
if has render; then disk "trước render"; rm -f $O/render.failed
  for s in ${ONLY:-$(segs segments)}; do while [ $(jobs -rp | wc -l) -ge $J ]; do sleep 2; done; render_one segments $s $O/sec/$s.mkv & done; wait; disk "sau render"
  [ -f $O/render.failed ] && { echo "Có đoạn render lỗi — dừng, không ghép"; exit 3; }; fi
if has mix; then $PY $LL/mix.py $TL $O/mix.wav; fi
if has ghep; then
  $PY - "$TL" "$O" <<'E'
import json, subprocess, sys
tl, O = json.load(open(sys.argv[1])), sys.argv[2]; bad = []; L = []
for s in tl['segments']:
    p = f"{O}/sec/{s['id']}.mkv"; n = int(subprocess.run(['ffprobe', '-v', 'error', '-count_packets', '-select_streams', 'v:0', '-show_entries', 'stream=nb_read_packets', '-of', 'csv=p=0', p], capture_output=True, text=True).stdout.strip() or 0)
    if n != s['frames']: bad.append(f"{s['id']}: {n}/{s['frames']}")
    L.append(f"file '{p}'")
open(f'{O}/list.txt', 'w').write('\n'.join(L) + '\n')
if bad: sys.exit('LỆCH số khung: ' + ', '.join(bad))
# 3 phần: cắt ở ranh giới đoạn gần 1/3 và 2/3 tổng thời lượng nhất
T = tl['tong_s']; b = [s['t1'] for s in tl['segments'][:-1]]
c1 = min(b, key=lambda x: abs(x - T / 3)); c2 = min([x for x in b if x > c1] or [T], key=lambda x: abs(x - 2 * T / 3))
for k, (a, z) in enumerate([(0, c1), (c1, c2), (c2, T)], 1):
    ds = [s for s in tl['segments'] if s['t0'] >= a - 1e-6 and s['t1'] <= z + 1e-6]
    open(f'{O}/list-p{k}.txt', 'w').write(''.join(f"file '{O}/sec/{s['id']}.mkv'\n" for s in ds)); open(f'{O}/p{k}.range', 'w').write(f"{a} {z - a} {ds[0]['id']}-{ds[-1]['id']}\n")
E
  DUR=$($PY -c "import json;print(json.load(open('$TL'))['tong_s'])")
  VF="scale=out_color_matrix=bt709:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p"; COL="-color_range tv -color_primaries bt709 -color_trc bt709 -colorspace bt709"
  disk "trước ghép"
  ffmpeg -v error -y -f concat -safe 0 -i $O/list.txt -i $O/mix.wav -map 0:v -map 1:a -vf "$VF" -c:v libx264 -preset slow -crf 16 -profile:v high -g 48 $COL -r 24 -fps_mode cfr \
    -c:a aac -b:a 256k -ar 48000 -movflags +faststart -t $DUR $O/$ID-$V-master.mp4
  for k in p1 p2 p3; do read SS DD RG < $O/$k.range
    for p in 1 2; do OUTP=/dev/null; [ $p = 2 ] && OUTP=$O/$ID-$V-$k.mp4
      ffmpeg -v error -y -f concat -safe 0 -i $O/list-$k.txt -ss $SS -t $DD -i $O/mix.wav -map 0:v -map 1:a -vf "scale=1280:720:flags=lanczos:out_color_matrix=bt709:out_range=tv,format=yuv420p" \
        -af "volume=-1.2dB,alimiter=limit=0.82:level=0,afade=t=in:d=0.03,afade=t=out:st=$(echo "$DD - 0.06" | bc -l):d=0.06" -c:v libx264 -preset slow -b:v 2800k -maxrate 3600k -bufsize 7200k -pass $p -passlogfile $O/pass/x$k -profile:v high -g 48 $COL -r 24 -fps_mode cfr -c:a aac -b:a 128k -ar 48000 -movflags +faststart -t $DD \
        $( [ $p = 1 ] && echo "-an -f mp4" ) $OUTP; done; done
  sha256sum $O/$ID-$V-*.mp4 > $O/SHA256SUMS.txt; disk "sau ghép"
  $PY $LL/khan_gia.py "$EP" > /dev/null   # mục B9: KHAN-GIA.md theo mốc đoạn thật
fi
if has shorts; then for s in $(segs shorts); do render_one shorts $s $O/shorts/$s.mkv
  $PY $LL/mix.py $TL $O/shorts/$s.wav --short $s
  ffmpeg -v error -y -i $O/shorts/$s.mkv -i $O/shorts/$s.wav -map 0:v -map 1:a -vf "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p" -c:v libx264 -preset slow -crf 18 -profile:v high -g 48 \
    -color_range tv -color_primaries bt709 -color_trc bt709 -colorspace bt709 -r 24 -c:a aac -b:a 192k -ar 48000 -movflags +faststart -shortest $O/shorts/$ID-short-$s.mp4; done; fi
echo "{\"buoc\": \"$STEPS\", \"giay\": $(( $(date +%s) - T0 ))}" > $O/build.json; cat $O/build.json
