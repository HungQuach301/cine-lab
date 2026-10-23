#!/bin/bash
# LOOK-T4 · dựng 24 khung look 1080p (8 hàng × 3 biến thể) + mặt nạ ID (1 / hàng) + LUT xuất + đo; tối đa P tiến trình song song, chờ RAM ≥ 5 GB trước mỗi tiến trình.
#   bash scripts/k2ldn/look_chay.sh [P=2] [hàng …]      ra: $LDN_DATA/look/r/<hàng>-<v>/ (thô) · $LDN_DATA/look/khung-abc/<hàng>-<v>.jpg (sau LUT, ≤ 2 MB) · $LDN_DATA/look/do-abc/<hàng>-<v>.json
# Có --resume tự nhiên: bỏ qua khung đã có JPG + JSON đo. Tệp theo biến thể ở $LDN_DATA/look/khung-abc + do-abc (ngoài git, tên lộ biến thể).
set -o pipefail
cd "$(dirname "$0")/../.."
P=${1:-2}; shift || true
ROWS=${*:-"M1-rong M1-trung M2-ngay M2-dem M3-rong M3-trung M4-rong M4-trung"}
D=${LDN_DATA:-/var/tmp/ldn}; R=$D/look/r; KA=$D/look/khung-abc; DA=$D/look/do-abc; mkdir -p "$R" "$KA" "$DA"   # theo biến thể (lộ A/B/C) → NGOÀI git; look_to.py chép bản mù vào reports/look-t4/
SPP=${SPP:-16}
cho_ram() { while [ "$(free -m | awk '/Mem:/{print $7}')" -lt 5000 ]; do sleep 10; done; }
mot() {   # $1 = hàng, $2 = biến thể
  local k=$1 v=$2 out=$R/$1-$2; local jpg=$KA/$k-$v.jpg do=$DA/$k-$v.json
  [ -s "$jpg" ] && [ -s "$do" ] && return 0
  LDN_DATA=$D node scripts/k2ldn/render_look.js --shot channel-k2/k2c-t4-02/look/may/$k-$v.json --out "$out" --spp $SPP > "$out.log" 2>&1 || { echo "LỖI dựng $k-$v"; return 1; }
  /opt/cine/bin/python scripts/k2ldn/look_lut.py ap "$out/00000.jpg" "$jpg" "$v" || return 1
  local hero; hero=$(/opt/cine/bin/python -c "import json;print(','.join(map(str,json.load(open('channel-k2/k2c-t4-02/look/may/$k-$v.json'))['hero_EN'])))")
  /opt/cine/bin/python scripts/k2ldn/look_do.py "$jpg" --mask "$R/$k-mask/00000.png" --log "$out/log.json" --hero "$hero" > "$do" || return 1
  echo "XONG $k-$v $(/opt/cine/bin/python -c "import json;print(json.load(open('$out/log.json'))['s_per_frame'])") s"
}
for k in $ROWS; do   # mặt nạ ID (cùng hình học/máy cho cả hàng)
  [ -s "$R/$k-mask/00000.png" ] || LDN_DATA=$D node scripts/k2ldn/render_look.js --shot channel-k2/k2c-t4-02/look/may/$k-A.json --out "$R/$k-mask" --mask 1 > "$R/$k-mask.log" 2>&1 || echo "LỖI mặt nạ $k"
done
jobs_n() { jobs -rp | wc -l; }
for k in $ROWS; do for v in ${VS:-A B C}; do
  while [ "$(jobs_n)" -ge "$P" ]; do sleep 5; done
  cho_ram; mot "$k" "$v" & sleep 20
done; done
wait
echo "LOOK-CHAY XONG"
