#!/bin/bash
# ANIMATIC-T4-V2 · lệnh bổ sung #2 (12:05) bước 4 + K1177-D4: q_thoi_dai lớp CÔNG TRÌNH MỐC (--lop-moc --moc) trên 3 khung (25/55/90 %) của mọi clip M-d dùng trong v3
# có chân trời City / công trình mốc. Ra: animatic2/omni/kiem2/qtd-moc-<tag>-k<NN>.json; chi phí ghi reports/animatic-t4-v2/qtd-moc.jsonl.
#   bash qmoc_v3.sh <tag> <năm> "<mốc>"
set -o pipefail
cd "$(dirname "$0")/../../.."
tag=$1; nam=$2; moc=$3; O=channel-k2/k2c-t4-02/animatic2/omni/kiem2; F=/var/tmp/anim/qmoc-khung; mkdir -p $F
clip=channel-k2/k2c-t4-02/animatic2/omni/clip/$tag.mp4; [ -s $clip ] && [ "${V1:-0}" = 0 ] || clip=channel-k2/k2c-t4-02/animatic/omni/clip/$tag.mp4   # v3 trước; V1=1 ép clip v1 (tên trùng)
for u in 25 55 90; do p=$F/$tag-k$u.png
  [ -s $p ] || /opt/cine/bin/python -c "
import cv2,sys;c=cv2.VideoCapture('$clip');n=int(c.get(7));c.set(1,int($u/100*(n-1)));ok,im=c.read();cv2.imwrite('$p',im)"
  r=$(/opt/cine/bin/python checks/ll/q_thoi_dai.py --anh $p --nam $nam --noi London --out /var/tmp/anim/qmoc --api --lop-moc --moc "$moc" --json $O/qtd-moc-$tag-k$u.json 2>&1 | tail -1)
  echo "{\"tag\":\"$tag\",\"khung\":$u,\"nam\":$nam,\"moc\":$(python3 -c "import json,sys;print(json.dumps(sys.argv[1]))" "$moc"),\"kq\":$(python3 -c "import json,sys;print(json.dumps(sys.argv[1]))" "$r")}" >> reports/animatic-t4-v2/qtd-moc.jsonl; echo "$tag k$u: $r"
done
