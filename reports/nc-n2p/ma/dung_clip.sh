#!/usr/bin/env bash
# NC-N2P · dựng clip nguồn (khung màu JPG + mặt nạ ID V7C cùng một lượt, cùng trạng thái) bằng design/k2v/v7c/do_bocuc.js (V7C @47a0f55a, không sửa) — 1280×720, spp 1 (mức nháp như NC-V2V)
#   dung_clip.sh <khoá c1|c2|c4|tl>   (opt + khung: reports/nc-n2p/ma/nguon-clip.json)
set -euo pipefail
K=$1; D=${K%[AB]}; [ "$K" = c4A ] || [ "$K" = c4B ] || D=$K; O=/var/tmp/n2p/src/$D; mkdir -p $O; export K2TL_CACHE=/var/tmp/cine-out/k2tl-cache
J=/home/user/cine-lab/reports/nc-n2p/ma/nguon-clip.json
OPT=$(/opt/cine/bin/python -c "import json;print(json.dumps(json.load(open('$J'))['$K']['opt']))")
FR=$(/opt/cine/bin/python -c "import json;print(','.join(map(str,json.load(open('$J'))['$K']['frames'])))")
cd /var/tmp/n2p-wt && node design/k2v/v7c/do_bocuc.js --opt "$OPT" --only $FR --w 1280 --h 720 --scale 1 --png $O/id --jpg $O/rgb --out $O/id.json 2>&1 | grep -v "GPU stall" | tail -5
echo DUNG-XONG $K
