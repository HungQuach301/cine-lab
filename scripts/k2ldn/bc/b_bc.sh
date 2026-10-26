#!/bin/bash
# BAN-CUOI-T4-A · việc 3 (B): AI phủ bề mặt nhà thường ≥ 4 px/m trên render look3 cờ d — dùng ĐÚNG bmn_thub.py của THU-B (prep/ghep/tiso; không sửa)
# qua thư mục ánh xạ: $THUB/r/<k>-v2 → render look3 d; mặt nạ/bóng cùng tên; LDN_DATA ánh xạ look3b → look3d (nha.json của hình học đang dựng).
# Ngưỡng 4 px/m (§15 (j), T2 = b): sau prep, do-duoc.png lọc lại theo nha-chi-tiet.json px_m ≥ 4.   bash scripts/k2ldn/bc/b_bc.sh <k> <năm> <luot>
set -o pipefail
cd "$(dirname "$0")/../../.."
k=$1; nam=$2; l=${3:-1}; R=/var/tmp/bc/r; export THUB=/var/tmp/bc/thub LDN_DATA=/var/tmp/bc/ldnb; PY=/opt/cine/bin/python
mkdir -p $THUB/r $LDN_DATA; ln -sfn /var/tmp/ldn/look3d $LDN_DATA/look3b
ln -sfn $R/$k $THUB/r/$k-v2; for s in m1 m3 m4 m6 bong; do ln -sfn $R/$k-$s $THUB/r/$k-$s; done; [ -d $R/tl-$k-v2 ] && ln -sfn $R/tl-$k-v2 $THUB/r/tl-$k-v2
[ -s $THUB/bp/$k/prep.json ] || $PY scripts/k2ldn/thu-b/bmn_thub.py prep $k | tail -1
$PY - <<PYEOF
import json, cv2, numpy as np
o='$THUB/bp/$k'; rows=json.load(open(o+'/nha-chi-tiet.json')); ok=[r['id'] for r in rows if r['do_duoc'] and r['px_m']>=4.0]
I=cv2.imread(o+'/mat_na_nha.png').astype(np.int64); I=(I[...,2]<<16)|(I[...,1]<<8)|I[...,0]
M=np.isin(I,np.array(ok or [-1],np.int64)); cv2.imwrite(o+'/do-duoc.png',(M*255).astype(np.uint8))
json.dump(dict(nguong_px_m=4.0,nha_do_duoc_2=sum(r['do_duoc'] for r in rows),nha_ge4=len(ok),pct_khung=round(float(M.mean()*100),2)),open(o+'/px4.json','w')); print('≥4 px/m:',len(ok),'nhà ·',round(float(M.mean()*100),2),'% khung')
PYEOF
B=channel-k2/k2c-t4-02/ban-cuoi/b; mkdir -p $B/ai
[ -s $B/ai/$k-l$l.jpg ] || { $PY scripts/k2ldn/bc/oai_bc.py --img $THUB/bp/$k/vao.jpg --prompt-file $B/lenh-${k#B-}.txt --tag $k-l$l --out /var/tmp/bc/bai && cp /var/tmp/bc/bai/$k-l$l.jpg $B/ai/; }
$PY scripts/k2ldn/thu-b/bmn_thub.py ghep $k l$l $B/ai/$k-l$l.jpg | tail -1
[ -d $THUB/r/tl-$k-v2 ] && MA_HOA_KIEM=1 TL_PREFIX=tl $PY scripts/k2ldn/thu-b/bmn_thub.py tiso $k l$l
echo B-XONG $k
