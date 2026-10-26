#!/bin/bash
# BAN-CUOI-T4-B1 · xong một việc dựng: mã hoá theo D-B1 (H.264 High, 1920×1080, 24 fps, yuv420p, CRF 16, preset veryfast, không âm thanh)
#   → channel-k2/k2c-t4-02/ban-cuoi/dung/<mã>-1080p.mp4 (LFS) + SHA256SUMS (dòng sha256sum chuẩn + dòng "#" số khung) + log máy <mã>.json.gz vào git
#   → tiến độ vào CHECKPOINT → commit (preflight pipefail, chỉ khi "— ĐẠT") → git lfs push → git push (K33: hook pre-push là preflight, LFS đẩy tay trước).
# Khoá flock /var/tmp/bc/git.lock (không đụng commit tay). Mã thoát ≠ 0 → hàng dựng dừng (dung_b1.py ghi /var/tmp/bc/DUNG-B1).
#   bash scripts/k2ldn/bc/xong_b1.sh <tên việc>
set -o pipefail
cd "$(dirname "$0")/../../.." || exit 2
ten=$1; R=${BC_R:-/var/tmp/bc/r}; D=channel-k2/k2c-t4-02/ban-cuoi/dung; B=$(git rev-parse --abbrev-ref HEAD); mkdir -p $D/log-may
exec 9>/var/tmp/bc/git.lock; flock 9
n=$(ls $R/$ten/*.jpg 2>/dev/null | wc -l); [ "$n" -gt 0 ] || { echo "THIẾU khung $ten"; exit 3; }
ffmpeg -nostdin -loglevel error -y -framerate 24 -pattern_type glob -i "$R/$ten/*.jpg" -c:v libx264 -profile:v high -preset veryfast -crf 16 -pix_fmt yuv420p -r 24 -an -movflags +faststart $D/$ten-1080p.mp4 || exit 3
nf=$(ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames -of csv=p=0 $D/$ten-1080p.mp4)
[ "$nf" = "$n" ] || { echo "LỆCH số khung $ten: mp4 $nf ≠ jpg $n"; exit 4; }
sha=$(sha256sum $D/$ten-1080p.mp4 | cut -d' ' -f1); mb=$(du -m $D/$ten-1080p.mp4 | cut -f1)
inf=$(/opt/cine/bin/python -c "import json;L=json.load(open('$R/$ten/log.json'));f=[x['f'] for x in L['frames']];print(f[0],f[-1],round(L['s_per_frame'],2),L['setup_s'])")
read f0 f1 spf setup <<< "$inf"
touch $D/SHA256SUMS; grep -v -- " $ten-1080p.mp4" $D/SHA256SUMS > $D/.s.tmp; mv $D/.s.tmp $D/SHA256SUMS
printf '%s  %s\n# %s khung=%s f=%s..%s s_khung=%s setup_s=%s P=2 spp=4 trang=bc/look3-b1 co_d=1 (chưa LUT, chưa lớp chồng)\n' "$sha" "$ten-1080p.mp4" "$ten-1080p.mp4" "$n" "$f0" "$f1" "$spf" "$setup" >> $D/SHA256SUMS
gzip -9nc $R/$ten/log.json > $D/log-may/$ten.json.gz
echo "- $(date -u +%H:%M) UTC dựng xong **$ten**: $n khung (f $f0..$f1), $spf s/khung/tiến trình (P = 2), $mb MB, SHA \`${sha:0:16}…\` → LFS + đẩy" >> reports/ban-cuoi-t4-b1/CHECKPOINT.md
git add $D/$ten-1080p.mp4 $D/SHA256SUMS $D/log-may/$ten.json.gz reports/ban-cuoi-t4-b1/CHECKPOINT.md
git check-attr filter -- $D/$ten-1080p.mp4 | grep -q 'filter: lfs' || { echo "KHÔNG LFS: $ten"; exit 5; }
bash reports/ban-cuoi-t4-b1/cam_commit.sh "BAN-CUOI-T4-B1: dựng 1080p $ten ($n khung, D-B1 LFS)" || exit 5
ok=0; for w in 0 2 4 8 16; do sleep $w; if git lfs push origin $B > /var/tmp/bc/log/lfs-$ten.log 2>&1; then ok=1; break; fi; done
[ $ok = 1 ] || { echo "LFS PUSH HỎNG $ten:"; cat /var/tmp/bc/log/lfs-$ten.log; exit 6; }
ok=0; for w in 0 2 4 8 16; do sleep $w; if git push -q origin $B > /var/tmp/bc/log/push-$ten.log 2>&1; then ok=1; break; fi; done
[ $ok = 1 ] || { echo "PUSH HỎNG $ten:"; cat /var/tmp/bc/log/push-$ten.log; exit 7; }
LF=$(git lfs ls-files); echo "$LF" | grep -q "$ten-1080p.mp4" || { echo "git lfs ls-files thiếu $ten"; exit 8; }
echo "XONG-B1 $ten $n $sha"
