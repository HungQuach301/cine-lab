#!/bin/bash
# Phiên P — C3 cho CẢ HAI nhân vật (chủ dự án 29/09/2026, Cổng 6 W2). RUN.md 3.6: luật đọc MỘT nhân vật mỗi thư mục parts
# ("một thư mục parts cho mỗi lần chạy"), nên chạy HAI lượt trên cùng một video:
#   lượt Ida: <X>.mp4      + <X>.parts      (model_sheet ida.json) + <X>.audit
#   lượt Cas: <X>.cas.mp4  + <X>.cas.parts  (model_sheet cas.json) + <X>.cas.audit   (<X>.cas.mp4 là liên kết CỨNG tới <X>.mp4: audit.py giải liên kết mềm về tệp gốc; git lưu một blob)
# Mỗi lượt: xuất mặt nạ (export_c3.js --who) → đổi RGBA sang L → audit.py issue → render lại khung được chọn → render.log → run.py --only C3.
# Dùng:  bash scripts/p/c3_hai_nv.sh <X không đuôi .mp4> <khung đầu trong phim> <khung cuối (không tính)> [ai=ida,cas]
#   Cả phim:   bash scripts/p/c3_hai_nv.sh design/cong5/layout/out/layout-v17 0 3372 cas
#   Một clip:  <X>.mp4 là đoạn cắt từ phim bắt đầu ở khung <đầu> (chia hết cho 12); mặt nạ ghi theo khung của clip (export_c3.js --offset).
# Cần sẵn <X>.mp4 và <X>.assets.json. P KHÔNG sửa checks/; chỉ chạy checks/audit.py và checks/run.py.
set -e
X=${1:?X}; F0=${2:?khung đầu}; F1=${3:?khung cuối}; AI=${4:-ida,cas}
cd "$(git rev-parse --show-toplevel)"
[ $((F0 % 12)) -eq 0 ] || { echo "khung đầu phải chia hết cho 12"; exit 2; }
FR=$(python3 -c "print(','.join(str(f) for f in range($F0,$F1) if f%12==0))")
G='import glob,sys,numpy as np
from PIL import Image
for p in glob.glob(sys.argv[1]+"/*/*.png"):
    im=Image.open(p)
    if im.mode=="RGBA": Image.fromarray(np.asarray(im)[...,3],"L").save(p,optimize=True)'
Q="bash scripts/render/queue.sh P"; TAG=$(basename $X)
for WHO in ${AI//,/ }; do
  if [ $WHO = ida ]; then Y=$X; else Y=$X.$WHO; rm -f $Y.mp4; ln $X.mp4 $Y.mp4; cp $X.assets.json $Y.assets.json; fi
  rm -rf $Y.parts   # KHÔNG xoá $Y.audit: audit.py từ chối phát lại yêu cầu (RUN.md 3.7)
  $Q $TAG-c3-$WHO -- node design/cong5/layout/export_c3.js --who $WHO --parts-dir $Y.parts --frames $FR --offset $F0 --scale 4
  /opt/cine/bin/python -c "$G" $Y.parts
  /opt/cine/bin/python checks/audit.py issue $Y.mp4
  AF=$(python3 -c "import json;print(','.join(str(f+$F0) for f in json.load(open('$Y.audit/request.json'))['frames']))")
  $Q $TAG-c3-$WHO-kiem-toan -- node design/cong5/layout/export_c3.js --who $WHO --audit-dir $Y.audit/rerender --frames $AF --offset $F0 --scale 4
  /opt/cine/bin/python -c "$G" $Y.audit/rerender
  python3 - "$Y" "$AF" "$WHO" "$F0" <<'PY'
import json,hashlib,sys
Y,AF,WHO,F0=sys.argv[1:5]; A=json.load(open(Y+'.assets.json'))
L=[f"# Kiểm toán C3 (RUN.md 3.7) — phiên P render lại mặt nạ {WHO} của {Y.split('/')[-1]}"]
for f in A['scene_files']: L.append(f"SCENE {f} SHA256 {hashlib.sha256(open(f,'rb').read()).hexdigest()}")
for fr in AF.split(','): L.append(f"FRAME {int(fr)-int(F0)} CMD node design/cong5/layout/export_c3.js --who {WHO} --audit-dir {Y}.audit/rerender --frames {AF} --offset {F0} --scale 4")
open(Y+'.audit/render.log','w').write('\n'.join(L)+'\n')
PY
  $Q $TAG-luat-c3-$WHO -- /opt/cine/bin/python checks/run.py $Y.mp4 --profile shot --only C3 --out reports/checks/$TAG-c3-$WHO || true
done
echo "C3-HAI-NV-XONG"
