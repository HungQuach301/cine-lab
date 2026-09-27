#!/bin/bash
# Cổng 3 vòng 1 — ghép khung mẫu (mỗi khung 48 khung = 2 s, grain đổi theo khung) thành video, chạy luật kiểm profile shot.
# Mỗi hướng: dir-X/check/dir-X.mp4 (2 shot: s1_opening, s5_shadows). Thêm ALL-6.mp4 (6 shot, cả 3 hướng) để đo G3b giữa shot.
# Mã hoá như M1 (đã qua G3/N2) nhưng 30 Mbps vì có grain (luật N3 v1.1 cho master YouTube có grain).
set -e
cd "$(dirname "$0")"
ROOT=$(cd ../.. && pwd)
enc() { # $1 = mp4 ra, còn lại = file .rgb theo thứ tự
  local out=$1; shift
  cat "$@" | ffmpeg -hide_banner -loglevel error -y -f rawvideo -pix_fmt rgb24 -s 1920x1080 -framerate 24 -i - \
    -vf 'vflip,scale=out_color_matrix=bt709:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p' \
    -c:v libx264 -preset medium -tune grain -profile:v high -b:v 30M -maxrate 40M -bufsize 60M -g 48 \
    -color_range tv -color_primaries bt709 -color_trc bt709 -colorspace bt709 -r 24 "$out"
}
ALL=()
for X in A B C; do
  mkdir -p dir-$X/check
  enc dir-$X/check/dir-$X.mp4 dir-$X/out/s1_opening.rgb dir-$X/out/s5_shadows.rgb
  (cd "$ROOT" && /opt/cine/bin/python checks/run.py design/cong3/dir-$X/check/dir-$X.mp4 --profile shot --out design/cong3/dir-$X/check/report) | grep -E "\] (N1|N2|G3|G3b) |VERDICT" || true
  ALL+=(dir-$X/out/s1_opening.rgb dir-$X/out/s5_shadows.rgb)
done
mkdir -p check-all
enc check-all/ALL-6.mp4 "${ALL[@]}"
(cd "$ROOT" && /opt/cine/bin/python checks/run.py design/cong3/check-all/ALL-6.mp4 --profile shot --out design/cong3/check-all/report) | grep -E "\] (N1|N2|G3|G3b) |VERDICT" || true
