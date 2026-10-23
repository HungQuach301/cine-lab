#!/usr/bin/env bash
# BAN-CUOI-T3 (việc 3) · RENDER ĐOẠN dần theo cảnh đinh đã dựng xong + GIẢI PHÓNG ĐĨA (khung 1080p ≈ 0,6 MB × 20 000 khung > đĩa còn):
#   mỗi vòng: tl_post.py (AGL vào timeline, như build.sh) → đoạn có cảnh đinh đã có stamp đúng VÀ không còn chờ chèn (CHO: minh hoạ/Cycles GPU) → scripts/k2/render.js
#   → sec/<id>.mkv + .hash (CÙNG công thức băm build.sh: sha1(đoạn timeline + render.js + lib/k2.js)) → cảnh mà MỌI đoạn dùng nó đã có mkv đúng băm: xoá *.jpg (giữ stamp, meta.json).
#   Một render một lúc. Lặp tới khi hết (CHU_KY giây giữa các vòng).   setsid nohup bash scripts/k2tl/cuoi_doan.sh > /var/tmp/cine-out/log/doan.log 2>&1 &
set -u
REPO=$(cd "$(dirname "$0")/../.." && pwd); O=/var/tmp/cine-out/k2c-t3-cuoi; TL=$O/timeline.json; K2=$REPO/scripts/k2; PY=/opt/cine/bin/python; mkdir -p $O/sec
echo $$ > /var/tmp/cine-out/log/doan.pgid
CHO=${CHO:-"anim_H1 anim_N1_4 anim_C5 anim_H2T anim_N2_9"}   # chờ chèn: M5, M3, M4 (minh hoạ) · H2T, N2.9 (Cycles GPU) — gỡ khỏi danh sách bằng tệp $O/cho-xong.txt
while true; do
  $PY $K2/tl_post.py $TL > /dev/null 2>&1 || echo "tl_post lỗi"
  read -r -d '' PLAN < <($PY - "$TL" "$O" "$CHO" "$K2" <<'P'
import json, os, sys, hashlib
tl = json.load(open(sys.argv[1])); O = sys.argv[2]; cho = set(sys.argv[3].split()); K2 = sys.argv[4]
xong = set(open(f'{O}/cho-xong.txt').read().split()) if os.path.exists(f'{O}/cho-xong.txt') else set(); cho -= xong
H = json.load(open(f'{O}/heroes.json')); ok = lambda k: os.path.exists(H[k]['dir'] + '/stamp') and open(H[k]['dir'] + '/stamp').read().strip() == H[k]['stamp']
code = open(f'{K2}/render.js', 'rb').read() + open(f'{K2}/lib/k2.js', 'rb').read()
dung = {}; lam = []
for s in tl['segments']:
    hs = sorted({sh['p']['hero'] for sh in s['shots'] if sh.get('p', {}).get('hero')}); h = hashlib.sha1(json.dumps(s, sort_keys=True).encode() + code).hexdigest()
    co = os.path.exists(f"{O}/sec/{s['id']}.mkv") and open(f"{O}/sec/{s['id']}.mkv.hash").read().strip() == h if os.path.exists(f"{O}/sec/{s['id']}.mkv.hash") else False
    for k in hs: dung.setdefault(k, []).append(co)
    if not co and hs and all(ok(k) and k not in cho for k in hs): lam.append(f"{s['id']} {h}")
xoa = [H[k]['dir'] for k, v in dung.items() if all(v) and ok(k) and k not in cho]
print(';'.join(lam) + '|' + ';'.join(xoa))
P
)
  LAM=${PLAN%%|*}; XOA=${PLAN#*|}
  for d in ${XOA//;/ }; do n=$(ls $d 2>/dev/null | grep -c '\.jpg$'); [ "$n" -gt 0 ] && { rm -f $d/*.jpg; echo "$(date -u +%H:%M) xoá $n khung $(basename $d)"; }; done
  if [ -z "$LAM" ]; then N=$($PY -c "import json,os;t=json.load(open('$TL'));print(sum(1 for s in t['segments'] if not os.path.exists('$O/sec/'+s['id']+'.mkv')))"); [ "$N" = 0 ] && { echo "DOAN-XONG"; break; }; sleep ${CHU_KY:-600}; continue; fi
  IFS=';' read -ra L <<< "$LAM"; for x in "${L[@]}"; do read id h <<< "$x"
    while [ $(awk '/MemAvailable/{print int($2/1048576)}' /proc/meminfo) -lt ${RAM_GB:-5} ]; do sleep 30; done   # Chromium render đoạn sập khi RAM < ~3 GB (3 cảnh đinh song song) — chờ RAM
    echo "$(date -u +%H:%M) render đoạn $id"
    if node $K2/render.js --tl $TL --seg $id --out $O/sec/$id.mkv 2>>$O/render-$id.err; then echo $h > $O/sec/$id.mkv.hash; else echo "LỖI render $id"; rm -f $O/sec/$id.mkv; fi; done
done
