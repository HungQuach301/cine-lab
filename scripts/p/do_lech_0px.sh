#!/bin/bash
# Phiên P — DÒ LỆCH 0 px: render nhanh một số shot (render_film.js --probe, 3 ảnh nhỏ mỗi shot, làn nhanh) từ cây mã hiện tại
# rồi so từng điểm ảnh với bản gốc. Dùng trước/sau mọi thay đổi "sau cờ" để chứng minh layout mặc định không đổi.
# Dùng:  bash scripts/p/do_lech_0px.sh <thư mục ra> <shot,shot,…> [thư mục gốc để so]
#   vd.  bash scripts/p/do_lech_0px.sh /tmp/x/truoc s02,s24c,s37,s42          (tạo bản gốc)
#        bash scripts/p/do_lech_0px.sh /tmp/x/sau   s02,s24c,s37,s42 /tmp/x/truoc   → "12 ảnh; lệch 0"
# So hai cây mã (vd. main và nhánh): chạy script trong từng worktree (nhớ liên kết node_modules, xem PLAN-HANDOFF-P.md).
set -e
OUT=${1:?thư mục ra}; SHOTS=${2:?danh sách shot}; GOC=$3
ROOT=$(git rev-parse --show-toplevel)
cd "$ROOT" && LAN=nhanh bash scripts/render/queue.sh ${GOI:-P} do-lech-0px -- node design/cong5/layout/render_film.js --out "$OUT" --only "$SHOTS" --probe | tail -1
[ -z "$GOC" ] && exit 0
/opt/cine/bin/python - "$GOC" "$OUT" <<'PY'
import glob,os,sys,numpy as np
from PIL import Image
g,o=sys.argv[1:3]; n=bad=0
for a in sorted(glob.glob(g+'/thumbs/*')):
    b=os.path.join(o,'thumbs',os.path.basename(a))
    if not os.path.exists(b): print('thiếu',b); bad+=1; continue
    x=np.array(Image.open(a).convert('RGB')).astype(int); y=np.array(Image.open(b).convert('RGB')).astype(int)
    d=int((np.abs(x-y).max(2)>0).sum()); n+=1; bad+=d>0
    if d: print(os.path.basename(a),'lệch',d,'px')
print(n,'ảnh; lệch',bad)
sys.exit(1 if bad else 0)
PY
