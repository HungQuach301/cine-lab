#!/usr/bin/env bash
# V7C T3 · DỰNG BẢN THỬ 540p (như v7b_dung.sh; đặc tả v7p/mk_ep_v7c.py, cách A = opt.nc + lightmap scripts/k2tl/v7c_nuong.sh) (một lệnh, chạy lại được — build.sh giữ cảnh/đoạn có dấu không đổi):
#   1) đặc tả (v7p/mk_ep_v7c.py --nc 1) → 2) prep + render (scripts/k2/build.sh, K2_DRAFT=1 MW=960; cảnh tl/t3tl, P cảnh song song)
#   3) TIẾNG: stem lời G1 v4.2 (KL42; bản xem MP3 trong git reports/kl42/nghe/T3-loi-G1-v42-xem-1-ch00-02.mp3 — master WAV ngoài git không còn trong container)
#      đặt từng dòng lời theo v7p/v7c-loi.json (nhịp B) + nhạc tạm Tyrant.mp3 (RIGHTS K2-MUS) dưới lời → −14 LUFS, đỉnh thật ≤ −1,5 dBTP → mix.wav
#   4) ghép master 960×540 · 5) hai bản xem: CÓ phụ đề kiểm (v7p/v7c-phu-de.srt nung) và KHÔNG phụ đề → ngoài git + bản ≤ 5 MB trong git (reports/v7c/ban-thu/)
#   bash scripts/k2tl/v7c_dung.sh [bước: spec render mix ghep xem] · P=3 J=2 · NC=0 (tắt cách A)
set -euo pipefail
REPO=$(cd "$(dirname "$0")/../.." && pwd); PY=/opt/cine/bin/python; EPD=$REPO/channel-k2/k2c-t3-01/v7p; V=c
EPY=$EPD/episode-v7c.yaml; O=/var/tmp/cine-out/k2c-t3-v7c
export K2TL_CACHE=${K2TL_CACHE:-/var/tmp/cine-out/k2tl-cache} K2_DRAFT=1 MW=960 PARTS=0
mkdir -p $O; STEPS=${*:-spec render mix ghep xem}; has() { [[ " $STEPS " == *" $1 "* ]]; }
if has spec; then $PY -I $EPD/mk_ep_v7c.py --nc ${NC:-1} --out $O; bash $REPO/scripts/k2/build.sh $EPY prep > $O.prep.log 2>&1 || { tail $O.prep.log; exit 2; }; fi
has render && P=${P:-3} J=${J:-2} bash $REPO/scripts/k2/build.sh $EPY render
if has mix; then $PY -I - "$EPD/v7c-loi.json" "$REPO/reports/kl42/nghe/T3-loi-G1-v42-xem-1-ch00-02.mp3" "$REPO/assets/k2/music/Tyrant.mp3" "$O" <<'E'
import json, subprocess, sys
L, stem, mus, O = json.load(open(sys.argv[1])), sys.argv[2], sys.argv[3], sys.argv[4]; D = L['tong_s']; inp, fl = [], []
for i, d in enumerate(L['dong']):
    pre = min(0.04, d['bd_stem'], d['bd_ban_thu']); a, b = d['bd_stem'] - pre, d['kt_stem'] + 0.15; inp += ['-ss', f'{a:.3f}', '-t', f'{b - a:.3f}', '-i', stem]
    fl.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,afade=t=in:d=0.02,afade=t=out:st={b - a - 0.05:.3f}:d=0.05,adelay={int(round((d['bd_ban_thu'] - pre) * 1000))}:all=1[v{i}]")
n = len(L['dong']); fl.append(''.join(f'[v{i}]' for i in range(n)) + f'amix=inputs={n}:normalize=0:dropout_transition=0,apad=whole_dur={D}[voice]')
fl.append(f"[{n}:a]aresample=48000,aformat=channel_layouts=stereo,loudnorm=I=-31:TP=-6:LRA=11,afade=t=in:d=1.5,afade=t=out:st={D - 4:.3f}:d=4[mus]")   # nhạc dưới lời ≈ 17 dB
fl.append('[voice][mus]amix=inputs=2:normalize=0,atrim=0:' + f'{D}' + '[mx]')
subprocess.run(['ffmpeg', '-v', 'error', '-y'] + inp + ['-stream_loop', '-1', '-ss', '2.55', '-i', mus, '-filter_complex', ';'.join(fl), '-map', '[mx]', '-ar', '48000', f'{O}/mix-tho.wav'], check=True)
subprocess.run(['ffmpeg', '-v', 'error', '-y'] + inp + ['-filter_complex', ';'.join(fl[:-2]), '-map', '[voice]', '-ar', '48000', f'{O}/loi.wav'], check=True)
E
  # loudness 2 lượt → −14 LUFS, TP ≤ −1,5
  J=$(ffmpeg -hide_banner -i $O/mix-tho.wav -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
  ffmpeg -v error -y -i $O/mix-tho.wav -af "loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=$(echo "$J" | $PY -c 'import json,sys;print(json.load(sys.stdin)["input_i"])'):measured_TP=$(echo "$J" | $PY -c 'import json,sys;print(json.load(sys.stdin)["input_tp"])'):measured_LRA=$(echo "$J" | $PY -c 'import json,sys;print(json.load(sys.stdin)["input_lra"])'):measured_thresh=$(echo "$J" | $PY -c 'import json,sys;print(json.load(sys.stdin)["input_thresh"])'):linear=true" -ar 48000 $O/mix.wav
  ffmpeg -hide_banner -i $O/mix.wav -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+(I|Peak|LRA):" | tee $O/mix-do.txt; fi
has ghep && bash $REPO/scripts/k2/build.sh $EPY ghep
if has xem; then M=$O/k2c-t3-v7c-v1-master.mp4; X=$REPO/reports/v7c/ban-thu; mkdir -p $X
  for k in phude khong; do R=$O/k2c-t3-v7c-540p-$k.mp4; VF="null"; [ $k = phude ] && VF="subtitles=$EPD/v7c-phu-de.srt:force_style='FontName=DejaVu Sans,FontSize=15,PrimaryColour=&H00FFFFFF,OutlineColour=&H80000000,BorderStyle=3,Outline=1,Shadow=0,MarginV=28'"
    ffmpeg -v error -y -i $M -vf "$VF" -c:v libx264 -preset slow -b:v 2300k -maxrate 3000k -bufsize 6000k -c:a aac -b:a 128k -movflags +faststart $R
    XX=$X/v7c-xem-$k.mp4; ffmpeg -v error -y -i $R -vf "scale=640:360:flags=lanczos,fps=24" -c:v libx264 -preset veryslow -crf 31 -c:a aac -b:a 64k -movflags +faststart $XX
    S=$(stat -c %s $XX); if [ $S -gt 4900000 ]; then ffmpeg -v error -y -i $R -vf "scale=640:360:flags=lanczos,fps=24" -c:v libx264 -preset veryslow -b:v $(( (4500000*8/119 - 64000) / 1000 ))k -c:a aac -b:a 64k -movflags +faststart $XX; fi
  done; sha256sum $M $O/k2c-t3-v7c-540p-*.mp4 $X/v7c-xem-*.mp4 | tee $O/SHA256-v7c.txt; ls -la $X; fi
