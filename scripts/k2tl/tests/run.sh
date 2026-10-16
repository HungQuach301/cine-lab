#!/bin/bash
# V5b-1 · test mô-đun xương sống thời gian (design/k2v/tl) + công cụ scripts/k2tl. Thoát ≠ 0 nếu một test trượt.
# Test trình duyệt (test_browser.js) cần gói cảnh ở $K2TL_CACHE/scene/gib/pack (build_scene.py) — bỏ qua êm nếu chưa có.
set -e; cd "$(dirname "$0")/../../.."; PY=/opt/cine/bin/python
$PY scripts/k2tl/tests/test_geo.py 2>&1 | tail -1
$PY scripts/k2tl/tests/test_calib.py 2>&1 | tail -1
node --no-warnings scripts/k2tl/tests/test_geom.mjs
node --no-warnings scripts/k2tl/tests/test_campath.mjs
if [ -f "${K2TL_CACHE:-/var/tmp/cine-out/k2tl-cache}/scene/gib/pack/meta.json" ]; then node scripts/k2tl/tests/test_browser.js; else echo "test_browser: BỎ QUA (chưa có gói cảnh)"; fi
echo "TẤT CẢ TEST ĐẠT"
