#!/usr/bin/env bash
# NC-N2P · đo một video ghép (Omni + lớp (a)) so nguồn bằng bộ đo NC-V2V (do_v2v.py T1–T6) + NC-V2V3 (do_them3.py T7–T9), gọi NGUYÊN mã
# (bản sao tạm /var/tmp/n2p/k2v/{v2v,v2v3} từ design/k2v/v2v @main và origin/nc-v2v3 — do_them3 nạp ../v2v/do_v2v.py theo đường dẫn tương đối).
#   do_video.sh <thư mục clip nguồn (rgb, id)> <f0> <nguồn.mp4> <ra.mp4> <nhãn> <thư mục json>
set -euo pipefail
S=$1; F0=$2; SRC=$3; OUT=$4; TAG=$5; J=$6; mkdir -p $J
V=$S/id-v2v; if [ ! -f $V/.xong ]; then mkdir -p $V; /opt/cine/bin/python -I - "$S/id" "$V" <<'E'
import sys, glob, os; sys.path.insert(0, '/home/user/cine-lab/reports/nc-n2p/ma'); import n2p_lib as L
for p in sorted(glob.glob(sys.argv[1] + '/*.png')): L.to_v2v_png(L.idmap(p), os.path.join(sys.argv[2], os.path.basename(p)))
open(os.path.join(sys.argv[2], '.xong'), 'w').write('ok')
E
fi
/opt/cine/bin/python -I /var/tmp/n2p/k2v/v2v/do_v2v.py --src $SRC --out $OUT --id $V --f0 $F0 --json $J/$TAG-v2v.json --label $TAG | tail -1
/opt/cine/bin/python -I /var/tmp/n2p/k2v/v2v3/do_them3.py --src $SRC --out $OUT --id $V --f0 $F0 --json $J/$TAG-them3.json --label $TAG | tail -1
