#!/usr/bin/env bash
# ghép lớp (a) + kiểm cho các biến thể Omni của một clip: chay_ghep_kiem.sh <khoá> <thư mục nguồn> <f0> <năm> <biến thể…>
K=$1; S=$2; F0=$3; NAM=$4; shift 4; R=/home/user/cine-lab/reports/nc-n2p; O=/var/tmp/n2p/omni
for v in "$@"; do [ -s $O/$K-$v.mp4 ] || { echo "THIẾU $K-$v"; continue; }
  /opt/cine/bin/python -I $R/ma/ghep_video.py --src $S/rgb --id $S/id --f0 $F0 --ai $O/$K-$v.mp4 --out $O/$K-$v-ghep.mp4 --khop-mau --json $O/do/$K-$v-ghep.json | cut -c1-200
  bash $R/ma/kiem_video.sh $K $S $F0 $NAM $v
done
