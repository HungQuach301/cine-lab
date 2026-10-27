#!/bin/bash
# BAN-CUOI-T4-B2a · tái tạo dữ liệu nền ngoài git trên container mới ($LDN_DATA=/var/tmp/ldn) — đúng chuỗi ghi trong reports/ban-cuoi-t4-b1/SHA-du-lieu-ngoai-git.txt:
#   scripts/k2ldn/anim/du_lieu.sh tới bước fb (chép từng bước, không chạy hình học look2) → bc/hinh_hoc_b1.py → lightmap look3d theo mốc (nuong_look.py, như nuong_b1.sh)
#   → đoạn phố người/xe (anim/dan_du_lieu.py → look3d/dan.json, cho trang bc/look3-b1d) → SHA256 mọi tệp vào reports/ban-cuoi-t4-b2a/SHA-du-lieu-ngoai-git.txt.
#   (GHIM=1 → khôi phục vector OSM của B2a từ git; kiểm thuyen.json trùng ban-cuoi/may/b2a/thuyen-b2a.json)
#   setsid nohup bash scripts/k2ldn/bc/du_lieu_b2a.sh > /var/tmp/bc/log/du_lieu_b2a.log 2>&1 &
set -o pipefail
cd "$(dirname "$0")/../../.."
export LDN_DATA=${LDN_DATA:-/var/tmp/ldn} K2TL_CACHE=${K2TL_CACHE:-/var/tmp/ldn/cache} LDN_SRC=${LDN_SRC:-/var/tmp/ldn/tu-lieu}
mkdir -p $LDN_DATA/log $LDN_SRC /var/tmp/bc/log; PY=/opt/cine/bin/python
b() { echo "== $(date -u +%H:%M:%S) $*"; }
# GHIM=1 (B2b/B3): dùng vector OSM đã ghim trong git (tải B2a 27/10/2026 01:25 UTC; OSM API là dữ liệu SỐNG — tải lại ra hình học/thuyền khác B2a)
G=channel-k2/k2c-t4-02/ban-cuoi/may/b2a
if [ "${GHIM:-0}" = 1 ] && [ -s $G/osm2026-b2a.json.gz ]; then b vec-ghim; mkdir -p $LDN_DATA/vec; gunzip -c $G/osm2026-b2a.json.gz > $LDN_DATA/vec/osm2026.json
else b osm; $PY scripts/k2ldn/tai_osm.py || exit 1; b vec; $PY scripts/k2ldn/osm_vec.py || exit 1; fi
b lidar; $PY scripts/k2ldn/tai_lidar.py || exit 1
b tulieu; $PY scripts/k2ldn/tai_tu_lieu.py; $PY scripts/k2ldn/tai_tu_lieu_look.py
git checkout -- channel-k2/k2c-t4-02/licenses channel-k2/k2c-t4-02/tu-lieu channel-k2/k2c-t4-02/look/tu-lieu 2>/dev/null; git status --short channel-k2/k2c-t4-02 | head
b van;   $PY scripts/k2ldn/tai_van.py; git checkout -- channel-k2/k2c-t4-02/look/van-cc0.json 2>/dev/null
b fb;    [ -s $LDN_DATA/fb/khoi.png ] || $PY scripts/k2ldn/nuong_flipbook.py $LDN_DATA/fb 96 192 || exit 1
b hinh_b1; [ -s $LDN_DATA/look3d/nid.f32 ] || $PY scripts/k2ldn/bc/hinh_hoc_b1.py || exit 1
b dan;   $PY scripts/k2ldn/anim/dan_du_lieu.py 2>&1 | tail -1 || true; mkdir -p $LDN_DATA/look2; [ -s $LDN_DATA/look2/dan.json ] && cp $LDN_DATA/look2/dan.json $LDN_DATA/look3d/dan.json
for y in ${NAM:-1666.6 1667.3 2026.7 1860.5 1700.5 1711.5 1800.5 1900.5 1938.5 1940.98 1955.5 1975.5}; do b NUONG3D $y
  [ -s $LDN_DATA/look3d/bake_$y.png ] || LDN_LOOK=look3d /opt/bpy/bin/python scripts/k2ldn/nuong_look.py $y $LDN_DATA/look3d/bake_$y.png --box 530800,179700,534000,182000 | tail -2 || echo "LỖI nướng $y"; done
[ "${GHIM:-0}" = 1 ] && { cmp -s $LDN_DATA/look3d/thuyen.json $G/thuyen-b2a.json && echo "thuyen.json trùng B2a" || echo "CẢNH BÁO thuyen.json KHÁC B2a"; }
b SHA; ( cd $LDN_DATA && sha256sum look3d/ldn2.bin look3d/hid.f32 look3d/nid.f32 look3d/dan.json look3d/bake_*.png ) > reports/ban-cuoi-t4-b2a/SHA-du-lieu-ngoai-git.txt
b DU-LIEU-B2a-XONG
