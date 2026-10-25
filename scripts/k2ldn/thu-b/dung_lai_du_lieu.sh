#!/bin/bash
# THU-B-T4 · dựng lại dữ liệu nền look2 trong container mới (/var/tmp/ldn trống) bằng đúng lệnh của LOOK-T4/LOOK-T4-V2 (không sửa mã của họ).
#   setsid nohup bash scripts/k2ldn/thu-b/dung_lai_du_lieu.sh > /var/tmp/ldn/log/dung_lai.log 2>&1 &
# Bước: OSM (tai_osm) → vector (osm_vec) · LiDAR (tai_lidar) · Doornick (tai_tu_lieu rijks-doornick; khôi phục tệp git bị ghi đè) · vân CC0 (tai_van)
#       · atlas lửa (nuong_flipbook 96×192) → hình học V2 (hinh_hoc_v2 → look2/) → nướng 1666.6 + 2026.7 (nuong_look, LDN_LOOK=look2). SHA ghi ở cuối.
set -o pipefail
cd "$(dirname "$0")/../../.."
export LDN_DATA=/var/tmp/ldn K2TL_CACHE=/var/tmp/ldn/cache LDN_SRC=/var/tmp/ldn/tu-lieu
PY=/opt/cine/bin/python; S=scripts/k2ldn
t() { echo "[$(date -u +%H:%M:%S)] $*"; }
t OSM; $PY $S/tai_osm.py || exit 2
t VEC; $PY $S/osm_vec.py || exit 2
t LIDAR; $PY $S/tai_lidar.py || exit 2
t DOORNICK; $PY $S/tai_tu_lieu.py rijks-doornick || exit 2
git checkout -- channel-k2/k2c-t4-02/licenses channel-k2/k2c-t4-02/tu-lieu 2>/dev/null; git status --short channel-k2/k2c-t4-02 | head
t VAN; $PY $S/tai_van.py || exit 2; git checkout -- channel-k2/k2c-t4-02/look/van-cc0.json
t ATLAS; $PY $S/nuong_flipbook.py $LDN_DATA/fb 96 192 || exit 2
t HINHHOC; $PY $S/hinh_hoc_v2.py || exit 2
for y in 1666.6 2026.7; do t NUONG $y; LDN_LOOK=look2 /opt/bpy/bin/python $S/nuong_look.py $y $LDN_DATA/look2/bake_$y.png --box 530800,179700,534000,182000 || exit 2; done
t SHA; sha256sum $LDN_DATA/look2/ldn2.bin $LDN_DATA/look2/bake_*.png $LDN_DATA/fb/*.png $LDN_DATA/vec/osm2026.json
t DUNG-LAI-XONG
