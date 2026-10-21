#!/usr/bin/env bash
# NC-N2P · kiểm N2+ cho một video Omni ĐÃ GHÉP: (1) bộ đo máy NC-V2V T1–T6 + NC-V2V3 T7–T9 (do_video.sh) cho bản ghép VÀ bản đối chứng không AI
# (đường ghép áp lên chính nguồn); (2) 3 khung mẫu (2,5 / 5 / 7,5 s) qua kiem_n2p.py --da-ghep --anh-tinh 0 (2 mô hình + máy) + q_thoi_dai.py.
#   kiem_video.sh <khoá clip> <thư mục nguồn (rgb,id)> <f0> <năm> <nhãn biến thể>
set -uo pipefail
K=$1; S=$2; F0=$3; NAM=$4; V=$5; R=/home/user/cine-lab/reports/nc-n2p; O=/var/tmp/n2p/omni; J=$O/do; mkdir -p $J $O/khung
SRC=$O/$K-nguon.mp4; G=$O/$K-$V-ghep.mp4
if [ ! -s $J/$K-doichung-ghep.json ]; then /opt/cine/bin/python -I $R/ma/ghep_video.py --src $S/rgb --id $S/id --f0 $F0 --ai $SRC --out $O/$K-doichung-ghep.mp4 --khop-mau --json $J/$K-doichung-ghep.json > /dev/null
  bash $R/ma/do_video.sh $S $F0 $G.nguon.mp4 $O/$K-doichung-ghep.mp4 $K-doichung $J; fi
bash $R/ma/do_video.sh $S $F0 $G.nguon.mp4 $G $K-$V $J
for t in 60 120 180; do f=$((F0 + t)); P=$O/khung/$K-$V-$t.png
  ffmpeg -v error -y -i $G -vf "select=eq(n\,$t)" -frames:v 1 $P
  /opt/cine/bin/python -I $R/ma/kiem_n2p.py --render $S/rgb/$(printf %05d $f).jpg --ai $P --id $S/id/$(printf %05d $f).png --nam $NAM --tag $K-$V-$t --out $O/kiem --da-ghep --anh-tinh 0 | grep viền
  (cd /home/user/cine-lab && /opt/cine/bin/python checks/ll/q_thoi_dai.py --anh $P --nam $NAM --noi Gibraltar --out $O/qtd/$K-$V-$t --api --json $O/qtd/$K-$V-$t.json | head -1)
done
echo KIEM-VIDEO-XONG $K $V
