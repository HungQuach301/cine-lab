#!/bin/bash
# ANIMATIC-T3-V2 · một lượt minh hoạ: ghép lệnh (CHUNG + riêng M + ghi chú lượt) → omni_i2v.py (nền, hỏi trạng thái) → kiem_minh_hoa.py (2 mô hình nhìn + q_thoi_dai)
#   bash ma/chay_omni.sh M2 1 1780 "<mô tả cảnh cho bộ kiểm>" [tệp ghi chú thêm cho lượt]
set -u; cd "$(dirname "$0")/.."; M=$1; L=$2; NAM=$3; CANH=$4; EXTRA=${5:-}
C=omni/lenh/CHUNG.txt; [ "$M" = M5 ] && C=omni/lenh/CHUNG-2026.txt
P=omni/lenh/$M-l$L.txt; { cat omni/lenh/$M.txt; [ -n "$EXTRA" ] && cat "$EXTRA"; echo; cat $C; } > $P
/opt/cine/bin/python -I ma/omni_i2v.py --image omni/dau/$M.jpg --prompt-file $P --out omni/ra/$M-l$L.mp4 --tag $M-l$L --res 720p || { echo "OMNI-LOI $M-l$L"; exit 2; }
/opt/cine/bin/python -I ma/kiem_minh_hoa.py --dau omni/dau/$M.jpg --clip omni/ra/$M-l$L.mp4 --nam $NAM --canh "$CANH" --tag $M-l$L --out omni/kiem/$M-l$L
echo "XONG $M-l$L"
