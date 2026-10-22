#!/usr/bin/env bash
# NC-N2P · dựng lại bộ đệm cảnh k2tl trong worktree tạm (/var/tmp/n2p-wt @ V7C 47a0f55a) — bản sao của scripts/k2tl/v7p_cache.sh
# chỉ đổi thư mục chạy (không chạy trong cây chính) + thêm bước V7B (mẫu nhà, Faden) như NC-V2V §2. Không sửa mã gốc.
set -euo pipefail
cd /var/tmp/n2p-wt
export K2TL_CACHE=/var/tmp/cine-out/k2tl-cache PY=/opt/cine/bin/python
mkdir -p $K2TL_CACHE
/opt/cine/bin/pip install -q imagecodecs shapely OpenEXR tifffile pyshp
(cd design/cong3/shared && npm ci --silent) ; (cd design/k2v && npm ci --silent)
date; $PY scripts/k2tl/fetch_sources.py
date; $PY scripts/k2tl/fetch_osm.py --name gib --bbox=-5.385,36.105,-5.320,36.185
date; $PY scripts/k2tl/build_rasters.py --name gib
date; $PY scripts/k2tl/build_vectors.py --name gib
date; $PY scripts/k2tl/build_scene.py --name gib --ao --far --cls
date; $PY scripts/k2tl/build_border.py --name gib
date; bash scripts/k2tl/pack_1782.sh origin/main
date; bash scripts/k2tl/pack_g1b.sh
date; echo CACHE-XONG
