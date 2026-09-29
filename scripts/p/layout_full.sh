#!/bin/bash
# Phiên P — pipeline LAYOUT ĐỦ 52 SHOT → mp4 có phụ đề + âm → mặt nạ C3 (4×) → bóng nhân vật (silhouettes, RUN.md 3.6.3)
# → kiểm toán (RUN.md 3.7, v1.5) → luật checks v1.5. Đúng các lệnh đã chạy cho layout-v15 / layout-v16 (29/09/2026).
# Dùng:   bash scripts/p/layout_full.sh <TAG>            vd. v17  → design/cong5/layout/out/layout-v17.* + reports/checks/layout-v17/
#         BUOC="mat-na,bong,kiem-toan,luat" bash scripts/p/layout_full.sh v17   (chỉ chạy lại các bước sau render; mặc định: tất cả)
# Chạy nền (khoảng 3 giờ với v16):  nohup bash scripts/p/layout_full.sh v17 > /var/tmp/cine-out/v17.log 2>&1 &
# Bước: render (render_film.js toàn phim, ~8 400 s ở v16) · tron-am (audio/mix.py; tự chạy khi thiếu /var/tmp/cine-out/audio/mix.flac) · ghep (assemble.py) · dong-goi (package.py, LAYOUT_TAG) · mat-na (export_c3.js ×4 + đổi xám)
#       · bong (export_sil.js) · kiem-toan (audit.py issue + render lại C3 + bóng + render.log) · luat (checks/run.py --profile shot)
#       · c3-cas (Cổng 6 W2: C3 lượt Cas — scripts/p/c3_hai_nv.sh <X> 0 <số khung> cas → <X>.cas.parts, <X>.cas.audit, reports/checks/layout-<TAG>-c3-cas/)
# LƯU Ý:
#  - render_film.js không có --only ghi timing.json; assemble.py chỉ đọc timing_*.json (bản mới nhất của cùng shot thắng) → đổi tên ngay sau render.
#  - Mặt nạ C3 xuất RGBA; đổi sang L (kênh alpha) trước khi chạy luật. KHÔNG đổi các PNG bóng (sil/, silhouette.png).
#  - P KHÔNG sửa checks/; chỉ chạy checks/audit.py và checks/run.py. Luật trượt: báo, không sửa hình để lách.
set -e
TAG=${1:?cần TAG, vd. v17}; BUOC=${BUOC:-render,ghep,dong-goi,mat-na,bong,kiem-toan,luat,c3-cas}
has() { [[ ",$BUOC," == *",$1,"* ]]; }
cd "$(dirname "$0")/../.."
Q="bash scripts/render/queue.sh P"
O=design/cong5/layout/out; X=$O/layout-$TAG; OUT=/var/tmp/cine-out
if has render; then
  rm -f $OUT/P/full/timing.json
  $Q $TAG-render-toan-bo -- node design/cong5/layout/render_film.js --out $OUT/P/full
  mv $OUT/P/full/timing.json $OUT/P/full/timing_$TAG-toan-bo.json
fi
if has tron-am || [ ! -f $OUT/audio/mix.flac ]; then mkdir -p $OUT/audio; $Q $TAG-tron-am -- /opt/cine/bin/python design/cong5/layout/audio/mix.py $OUT/audio; fi   # âm tạm (mix.flac + stems/) cho package.py; /var/tmp không nằm trong git
has ghep && $Q $TAG-ghep-hinh -- /opt/cine/bin/python design/cong5/layout/assemble.py
has dong-goi && LAYOUT_TAG=-$TAG $Q $TAG-dong-goi -- /opt/cine/bin/python design/cong5/layout/package.py $OUT/final $OUT/audio
G='import glob,sys,numpy as np
from PIL import Image
from concurrent.futures import ProcessPoolExecutor
def f(p):
    im=Image.open(p)
    if im.mode=="RGBA": Image.fromarray(np.asarray(im)[...,3],"L").save(p,optimize=True)
with ProcessPoolExecutor(4) as ex: list(ex.map(f,[p for p in glob.glob(sys.argv[1]+"/*/*.png") if "/sil/" not in p and not p.endswith("silhouette.png")],chunksize=32))'
if has mat-na; then
  rm -rf $X.parts $X.audit
  $Q $TAG-c3-mat-na -- node design/cong5/layout/export_c3.js --parts-dir $X.parts --scale 4
  /opt/cine/bin/python -c "$G" $X.parts
fi
has bong && $Q $TAG-bong-nv -- node design/cong5/layout/export_sil.js --parts-dir $X.parts --text $X.text --scale 1
if has kiem-toan; then
  rm -rf $X.audit
  /opt/cine/bin/python checks/audit.py issue $X.mp4
  FR=$(python3 -c "import json;print(','.join(map(str,json.load(open('$X.audit/request.json'))['frames'])))")
  SF=$(python3 -c "import json;d=json.load(open('$X.audit/request.json'));print(','.join(map(str,sorted(set(d['frames'])|set(d.get('sil_frames',[]))))))")
  $Q $TAG-c3-kiem-toan -- node design/cong5/layout/export_c3.js --audit-dir $X.audit/rerender --frames $FR --scale 4
  /opt/cine/bin/python -c "$G" $X.audit/rerender
  $Q $TAG-bong-kiem-toan -- node design/cong5/layout/export_sil.js --audit-dir $X.audit/rerender --frames $SF --scale 1
  python3 - "$X" "$FR" "$SF" <<'PY'
import json,hashlib,sys
X,FR,SF=sys.argv[1:4]; A=json.load(open(X+'.assets.json'))
L=["# Kiểm toán C3 + bóng nhân vật (RUN.md 3.7, v1.5) — phiên P render lại mặt nạ của "+X.split('/')[-1]]
for f in A['scene_files']: L.append(f"SCENE {f} SHA256 {hashlib.sha256(open(f,'rb').read()).hexdigest()}")
for fr in FR.split(','): L.append(f"FRAME {fr} CMD node design/cong5/layout/export_c3.js --audit-dir {X}.audit/rerender --frames {FR} --scale 4")
for fr in SF.split(','): L.append(f"FRAME {fr} CMD node design/cong5/layout/export_sil.js --audit-dir {X}.audit/rerender --frames {SF} --scale 1")
open(X+'.audit/render.log','w').write('\n'.join(L)+'\n')
PY
fi
has luat && { $Q $TAG-luat-may -- /opt/cine/bin/python checks/run.py $X.mp4 --profile shot --out reports/checks/layout-$TAG || true; }
if has c3-cas; then
  NF=$(ffprobe -v error -count_packets -select_streams v:0 -show_entries stream=nb_read_packets -of csv=p=0 $X.mp4)
  bash scripts/p/c3_hai_nv.sh $X 0 $NF cas
fi
echo "$TAG-XONG"
