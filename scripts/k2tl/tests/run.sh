#!/bin/bash
# V5b-1 (+ V5b-2a) · test mô-đun xương sống thời gian (design/k2v/tl) + công cụ scripts/k2tl. Thoát ≠ 0 nếu một test trượt.
# Test trình duyệt (test_browser.js) cần gói cảnh ở $K2TL_CACHE/scene/gib/pack (build_scene.py) — bỏ qua êm nếu chưa có.
set -e; cd "$(dirname "$0")/../../.."; PY=/opt/cine/bin/python
$PY scripts/k2tl/tests/test_geo.py 2>&1 | tail -1
$PY scripts/k2tl/tests/test_calib.py 2>&1 | tail -1
$PY scripts/k2tl/tests/test_look.py
node --no-warnings scripts/k2tl/tests/test_geom.mjs
node --no-warnings scripts/k2tl/tests/test_campath.mjs
node --no-warnings scripts/k2tl/tests/test_grammar.mjs
node --no-warnings scripts/k2tl/tests/test_t3.mjs   # V5b-2b: M6 sun.js, record.js
# V5b-2a (GG1): test trình duyệt chạy với CẢ HAI trình dựng (llvmpipe mặc định, swiftshader giữ được); env_check kiểm Mesa 25.2.8 / LLVM 20
bash scripts/k2tl/env_check.sh | tail -1
if [ -f "${K2TL_CACHE:-/var/tmp/cine-out/k2tl-cache}/scene/gib/pack/meta.json" ]; then for g in llvmpipe swiftshader; do K2TL_GL=$g node scripts/k2tl/tests/test_browser.js; done; else echo "test_browser: BỎ QUA (chưa có gói cảnh)"; fi
echo "TẤT CẢ TEST ĐẠT"
