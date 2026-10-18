#!/usr/bin/env bash
# V5b-2d · DỰNG LẠI các lớp 1782 của gói cảnh gib (container mới không giữ $K2TL_CACHE). Trước đây (V5b-2b/2c) chạy tay, không ghi lệnh — đây là bản ghi lại.
# Nguồn: ghost SH 1782 + 1943 (channel-k2/k2c-t3-01/ghost/, nhánh p-1810 — đọc bằng git archive, không merge) · OSM (heroes.json citywalls của build_scene).
# Lọc do_tin như ghi chú layers.js (V5b-2b): phố/công sự dùng cao + vừa; tuyến/đồn tiền phương do_tin thấp tách lớp riêng (_tp) — chỉ dùng hậu cảnh xa kèm "approx.".
# Dùng: bash scripts/k2tl/pack_1782.sh [nhánh chứa ghost SH, mặc định origin/p-1810]
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd); PY=/opt/cine/bin/python; REF=${1:-origin/p-1810}
export K2TL_CACHE=${K2TL_CACHE:-/var/tmp/cine-out/k2tl-cache}
SH=$K2TL_CACHE/sh; rm -rf "$SH"; mkdir -p "$SH"
git -C "$ROOT" archive "$REF" channel-k2/k2c-t3-01/ghost | tar -x -C "$SH"
G=$SH/channel-k2/k2c-t3-01/ghost
LF="$PY $ROOT/scripts/k2tl/load_footprints.py --pack gib"
SRC="Town: reconstructed from Drinkwater 1786 plan"
$LF --name ghost1782 --geojson $G/ghost-1782.geojson --kind ghost --period 0 --years 1779 1783 --loai khoi_pho,nha --do-tin cao,vua --src "$SRC"
$LF --name fort1782 --geojson $G/ghost-1782.geojson --period 0 --years 1700 2100 --loai cong_su,phao_dai --do-tin cao,vua --skip C1782-01 --src "$SRC"
$LF --name lines1782 --geojson $G/ghost-1782.geojson --lines --period 0 --years 1700 2100 --loai cong_su,chien_tuyen --do-tin cao,vua --src "$SRC"
$LF --name lines1782_tp --geojson $G/ghost-1782.geojson --lines --period 0 --years 1700 2100 --loai chien_tuyen --do-tin thap --src "Forward works: approx. (Drinkwater 1786)"
$LF --name fort1782_tp --geojson $G/ghost-1782.geojson --period 0 --years 1700 2100 --loai cong_su --do-tin thap --src "Forward works: approx. (Drinkwater 1786)"
$PY $ROOT/scripts/k2tl/infill_1782.py --ghost-dir $G --out $SH/infill-1782.geojson --log $SH/lap-pho-1782.json
$LF --name infill1782 --geojson $SH/infill-1782.geojson --kind ghost --period 3 --years 1779 1783 --src "Grey-washed blocks: estimated infill"
# V5b-2d: vật mới số hoá thêm từ cùng bản đồ (vườn, điểm nhấn) — scripts/k2tl/so_hoa_v5b2d.py
if [ -f "$ROOT/design/k2v/tl/data/so-hoa-v5b2d-px.json" ]; then
  $PY $ROOT/scripts/k2tl/so_hoa_v5b2d.py --ghost-dir $G --px $ROOT/design/k2v/tl/data/so-hoa-v5b2d-px.json --out $K2TL_CACHE/scene/gib/pack/layers/extra1782.json
fi
