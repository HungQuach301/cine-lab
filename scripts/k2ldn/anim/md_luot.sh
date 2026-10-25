#!/bin/bash
# ANIMATIC-T4 · một lượt M-d cho một shot: ảnh đầu (OpenAI, nếu chưa có ảnh đầu đạt) → kiểm T1 ảnh → Omni → kiểm T1 clip. Bản ≤ 5 MB vào git ngay (K22).
#   bash md_luot.sh <ma> <lượt> [360p|720p]
set -o pipefail
cd "$(dirname "$0")/../../.."
ma=$1; l=$2; res=${3:-360p}; PY=/opt/cine/bin/python; G=channel-k2/k2c-t4-02/animatic/omni; L=$G/lenh; O=/var/tmp/anim/omni/$ma; mkdir -p $O $G/dau $G/clip $G/kiem
nam=$($PY -c "import json;print(json.load(open('$L/muc-luc.json'))['$ma']['nam'])"); canh=$($PY -c "import json;print(json.load(open('$L/muc-luc.json'))['$ma']['canh'])")
loi=$($PY -c "
import json;B=json.load(open('channel-k2/k2c-t4-02/BANG-SHOT-v2.json'));r=[x for x in B['shot'] if x['ma']=='$ma'][0];print(' '.join(r['cau_loi'])[:600])")
dau=$G/dau/$ma-dau.jpg
if [ ! -s $dau ]; then
  $PY scripts/k2ldn/anim/oai_anh.py --prompt-file $L/$ma-anh.txt --tag $ma-a$l --out $O || exit 1
  $PY -c "from PIL import Image; Image.open('$O/$ma-a$l.jpg').convert('RGB').resize((1280,720), Image.LANCZOS).save('$O/$ma-a$l-720.jpg', quality=92)"
  $PY scripts/k2ldn/anim/gem_kiem.py --anh $O/$ma-a$l-720.jpg --nam $nam --canh "$canh" --loi "$loi" --tag $ma-a$l --out $G/kiem || exit 1
  grep -q '"ket_luan": "ĐẠT-T1"' $G/kiem/$ma-a$l-t1.json || { echo "ẢNH ĐẦU LOẠI $ma-a$l"; cp $O/$ma-a$l-720.jpg $G/dau/$ma-a$l-LOAI.jpg; exit 3; }
  cp $O/$ma-a$l-720.jpg $dau
fi
$PY scripts/k2ldn/anim/omni.py --dau $dau --prompt-file $L/$ma-vid.txt --out $O/$ma-l$l-$res.mp4 --tag $ma-l$l-$res --res $res || exit 1
ffmpeg -nostdin -loglevel error -y -i $O/$ma-l$l-$res.mp4 -c:v libx264 -crf 26 -preset slow -an -movflags +faststart $G/clip/$ma-l$l-$res.mp4
$PY scripts/k2ldn/anim/gem_kiem.py --anh $dau --clip $O/$ma-l$l-$res.mp4 --nam $nam --canh "$canh" --loi "$loi" --tag $ma-l$l-$res --out $G/kiem
