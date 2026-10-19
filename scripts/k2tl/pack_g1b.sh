#!/usr/bin/env bash
# G1b T3 · thêm lớp GHOST 1704 + 1943 (phiên SH, channel-k2/k2c-t3-01/ghost/) vào gói cảnh gib — sau pack_1782.sh. Cùng bộ nạp, cùng luật lọc do_tin (cao + vừa; thấp bỏ).
#   1704: Plan de la ville 1705 (LoC 2008621715) / Exact Plan 1705 (Rijks RP-P-OB-83.400) — khối phố + công sự · 1943: AMS M981 1:10 000 (Princeton) — nhà + khối phố.
# Dùng: bash scripts/k2tl/pack_g1b.sh
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd); PY=/opt/cine/bin/python
export K2TL_CACHE=${K2TL_CACHE:-/var/tmp/cine-out/k2tl-cache}
G=$ROOT/channel-k2/k2c-t3-01/ghost; LF="$PY $ROOT/scripts/k2tl/load_footprints.py --pack gib"
$LF --name ghost1704 --geojson $G/ghost-1704.geojson --kind ghost --period 0 --years 1700 1712 --loai khoi_pho,nha --do-tin cao,vua --src "Town: reconstructed from plans of 1705"
$LF --name fort1704 --geojson $G/ghost-1704.geojson --period 0 --years 1700 1712 --loai cong_su --do-tin cao,vua --src "Town: reconstructed from plans of 1705"
$LF --name ghost1943 --geojson $G/ghost-1943.geojson --kind ghost --period 1 --years 1939 1946 --loai khoi_pho,nha --do-tin cao,vua --src "Town: reconstructed from AMS M981 (1943)"
