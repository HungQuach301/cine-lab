#!/bin/bash
# Phiên P — KHUNG THỬ một thời điểm layout qua trang thử page_l2.js (không đụng layout), qua hàng đợi.
# Dùng:  bash scripts/p/khung_thu.sh <nhãn> <thư mục ra> '<json args>' [mẫu=1] [rộng=1920] [cao=1080]
#   args thường dùng: {"shot":"s42a","T":114.5}  (mặc định nhân vật theo cast3d: Ida 'bl' v1.5.1, Cas 'bl' + thân + tay MPFB)
#   thêm: "export":1,"exportWho":"cas" (xuất glb cho EEVEE) · "pose":{"cas":"turnaround"} · "casStyle":"v14" (thử bản cũ)
#   LƯU Ý: page_l2.js chỉ nạp trước glb Cas khi có "casStyle" → luôn truyền "casStyle":"bl" (hoặc "v14").
#   Khung nộp kiểm mù/chủ dự án: mẫu 3, 1920×1080, LAN=nang. Thử nhanh: mẫu 1 (làn nhanh).
set -e
L=${1:?nhãn}; O=${2:?thư mục ra}; A=${3:?json}; S=${4:-1}; W=${5:-1920}; H=${6:-1080}
cd "$(git rev-parse --show-toplevel)"
LAN=${LAN:-nhanh} bash scripts/render/queue.sh ${GOI:-P} "$L" -- timeout 900 node design/cong5/mat/still.js --page cong3/v2/char3d/blender/page_l2.js --frame x --out "$O" --samples $S --w $W --h $H --args "$A"
