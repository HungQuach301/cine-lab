#!/bin/bash
# ANIMATIC-T4 · chạy M-d cho danh sách shot: ≤ 3 lượt/khoảnh khắc (Q3 điểm 5), kiểm 2 tầng (Q3 điểm 7): tầng 1 gem_kiem.py (Gemini Flash) → nếu ĐẠT-T1 mới chạy tầng 2
# scripts/k2ldn/ai/kiem_minh_hoa.py (gpt-6.1-sol + checks/ll/q_thoi_dai.py — tổng 2 mô hình nhìn khác nhau + q_thoi_dai). Sổ giây: reports/animatic-t4/md-so-giay.jsonl
#   bash md_tat.sh <res> <ma …>
set -o pipefail
cd "$(dirname "$0")/../../.."
export N2P_DIR=$PWD/reports/animatic-t4 OAI_CHAN=10 CLAUDE_CHAN=15
res=$1; shift; PY=/opt/cine/bin/python; G=channel-k2/k2c-t4-02/animatic/omni; SG=reports/animatic-t4/md-so-giay.jsonl
for ma in "$@"; do
  [ -s $G/chon/$ma.txt ] && { echo "ĐÃ CHỌN $ma"; continue; }
  canh=$($PY -c "import json;print(json.load(open('$G/lenh/muc-luc.json'))['$ma']['canh'])"); nam=$($PY -c "import json;print(json.load(open('$G/lenh/muc-luc.json'))['$ma']['nam'])")
  for l in 1 2 3; do
    [ -s /var/tmp/anim/omni/$ma/$ma-l$l-$res.mp4 ] && [ -s $G/kiem/$ma-l$l-$res-t1.json ] || bash scripts/k2ldn/anim/md_luot.sh $ma $l $res; rc=$?
    [ $rc = 3 ] && { echo "{\"ma\":\"$ma\",\"luot\":$l,\"ket\":\"anh-dau-LOAI\"}" >> $SG; continue; }
    [ $rc != 0 ] && { echo "{\"ma\":\"$ma\",\"luot\":$l,\"ket\":\"LOI-$rc\"}" >> $SG; grep -q "CHẶN\|DỪNG" /dev/null; continue; }
    t1=$(grep -o '"ket_luan": "[^"]*"' $G/kiem/$ma-l$l-$res-t1.json | cut -d'"' -f4)
    if [ "$t1" = "ĐẠT-T1" ]; then
      $PY -I scripts/k2ldn/ai/kiem_minh_hoa.py --dau $G/dau/$ma-dau.jpg --clip /var/tmp/anim/omni/$ma/$ma-l$l-$res.mp4 --nam $nam --canh "$canh" --noi London --tag $ma-l$l-$res --out $G/kiem2 --mo-hinh gpt --qtd 1 > /tmp/claude-0/md-$ma-$l.txt 2>&1
      t2=$(tail -1 /tmp/claude-0/md-$ma-$l.txt | awk '{print $2}')
      echo "{\"ma\":\"$ma\",\"luot\":$l,\"t1\":\"$t1\",\"t2\":\"$t2\"}" >> $SG
      if [ "$t2" = "ĐẠT" ]; then mkdir -p $G/chon; echo "$ma-l$l-$res" > $G/chon/$ma.txt; echo "CHỌN $ma-l$l-$res"; break; fi
    else echo "{\"ma\":\"$ma\",\"luot\":$l,\"t1\":\"$t1\"}" >> $SG; fi
  done
  [ -s $G/chon/$ma.txt ] || echo "TRƯỢT 3 LƯỢT $ma → giữ 3D"
done
echo MD-TAT-XONG
