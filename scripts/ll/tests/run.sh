#!/bin/bash
# Test thư viện nhà máy (chủ dự án, 05/10/2026, NHÀ MÁY v1.1 mục 6). Chạy tự động đầu build.sh (TESTS=0 để bỏ).
#   (1) mỗi mẫu render 1 khung, so với ref/<đoạn>.png (lệch trung bình > NGUONG mức xám/255 → TRƯỢT); --update ghi lại tham chiếu
#   (2) ll.py check bắt được đặc tả sai (bad/*.yaml phải TRƯỢT; tpl.yaml phải ĐẠT)
#   (3) build.sh dừng (mã 3) khi có đoạn render lỗi
set -u; T=$(cd "$(dirname "$0")" && pwd); LL=$T/..; PY=/opt/cine/bin/python; O=/var/tmp/cine-out/ll-test; NGUONG=${NGUONG:-2.0}; fail=0
mkdir -p $O/f
$PY $LL/ll.py check $T/tpl.yaml > /dev/null || { echo "TRƯỢT check: tpl.yaml phải ĐẠT"; fail=1; }
for b in $T/bad/*.yaml; do $PY $LL/ll.py check $b > /dev/null 2>&1 && { echo "TRƯỢT check: $(basename $b) phải bị bắt"; fail=1; }; done
ASR=0 $PY $LL/ll.py prep $T/tpl.yaml > /dev/null || { echo "TRƯỢT prep"; exit 1; }
segs=$($PY -c "import json;[print(s['id']) for s in json.load(open('$O/timeline.json'))['segments']]")
for s in $segs; do node $LL/render.js --tl $O/timeline.json --seg $s --out $O/f/$s.mkv --only 90 --jpgdir $O/f > /dev/null 2>&1 & done; wait
$PY - "$T" "$O" "$NGUONG" "${1:-}" <<'P' || fail=1
import sys, os, glob, numpy as np
from PIL import Image
T, O, thr, mode = sys.argv[1], sys.argv[2], float(sys.argv[3]), sys.argv[4]; bad = 0
for f in sorted(glob.glob(f'{O}/f/*_f00090.jpg')):
    k = os.path.basename(f).split('_f')[0]; ref = f'{T}/ref/{k}.png'; im = Image.open(f).convert('L').resize((480, 270))
    if mode == '--update' or not os.path.exists(ref): im.save(ref); print(f'ghi tham chiếu {k}'); continue
    d = np.abs(np.asarray(im, float) - np.asarray(Image.open(ref).convert('L'), float)).mean()
    if d > thr: print(f'TRƯỢT ảnh {k}: lệch {d:.2f} > {thr}'); bad = 1
n = len(glob.glob(f'{O}/f/*_f00090.jpg'))
print(f'ảnh: {n} mẫu'); sys.exit(bad or (n < 13))
P
# (3) build dừng khi render lỗi: đặc tả có mẫu không tồn tại
TESTS=0 ASR=0 bash $LL/build.sh $T/bad-render.yaml prep render > /dev/null 2>&1; r=$?
[ $r = 3 ] || { echo "TRƯỢT build: phải dừng mã 3 khi render lỗi (nhận $r)"; fail=1; }
[ $fail = 0 ] && echo "TESTS ĐẠT" || echo "TESTS TRƯỢT"; exit $fail
