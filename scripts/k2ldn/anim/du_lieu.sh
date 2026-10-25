#!/bin/bash
# ANIMATIC-T4 · tái tạo dữ liệu nền ngoài git ($LDN_DATA, mặc định /var/tmp/ldn) trên container mới — đúng chuỗi lệnh của TIEN-KY-T4/LOOK-T4/LOOK-T4-V2:
#   OSM → vector → LiDAR → tư liệu (+ look) → vân CC0 → atlas lửa/khói → hình học V2 (ldn2.bin) → lightmap theo mốc (năm ở $NAM).
# Tệp trong git bị lệnh tải ghi đè (licenses/*.json, SHA256-TU-LIEU*.txt, tu-lieu/*.jpg) được khôi phục bằng git checkout sau bước tải.
set -o pipefail
cd "$(dirname "$0")/../../.."
export LDN_DATA=${LDN_DATA:-/var/tmp/ldn} K2TL_CACHE=${K2TL_CACHE:-/var/tmp/ldn/cache} LDN_SRC=${LDN_SRC:-/var/tmp/ldn/tu-lieu}
mkdir -p $LDN_DATA/log $LDN_SRC; PY=/opt/cine/bin/python
b() { echo "== $(date -u +%H:%M:%S) $*"; }
b osm;   $PY scripts/k2ldn/tai_osm.py || exit 1
b vec;   $PY scripts/k2ldn/osm_vec.py || exit 1
b lidar; $PY scripts/k2ldn/tai_lidar.py || exit 1
b tulieu; $PY scripts/k2ldn/tai_tu_lieu.py; $PY scripts/k2ldn/tai_tu_lieu_look.py
git checkout -- channel-k2/k2c-t4-02/licenses channel-k2/k2c-t4-02/tu-lieu channel-k2/k2c-t4-02/look/tu-lieu 2>/dev/null; git status --short channel-k2/k2c-t4-02 | head
b van;   $PY scripts/k2ldn/tai_van.py; git checkout -- channel-k2/k2c-t4-02/look/van-cc0.json 2>/dev/null
b fb;    [ -s $LDN_DATA/fb/khoi.png ] || $PY scripts/k2ldn/nuong_flipbook.py $LDN_DATA/fb 96 192 || exit 1
b hinh;  $PY scripts/k2ldn/hinh_hoc_v2.py || exit 1
for y in ${NAM:-1666.6 1940.98 2026.7}; do b nuong $y
  [ -s $LDN_DATA/look2/bake_$y.png ] || LDN_LOOK=look2 /opt/bpy/bin/python scripts/k2ldn/nuong_look.py $y $LDN_DATA/look2/bake_$y.png --box 530800,179700,534000,182000 || echo "LỖI nướng $y"; done
b XONG
