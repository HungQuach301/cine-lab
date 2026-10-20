#!/usr/bin/env bash
set -euo pipefail
cd /home/user/cine-lab
export K2TL_CACHE=/var/tmp/cine-out/k2tl-cache PY=/opt/cine/bin/python
/opt/cine/bin/pip install -q imagecodecs shapely OpenEXR tifffile pyshp
date; $PY scripts/k2tl/fetch_sources.py
date; $PY scripts/k2tl/fetch_osm.py --name gib --bbox=-5.385,36.105,-5.320,36.185
date; $PY scripts/k2tl/build_rasters.py --name gib
date; $PY scripts/k2tl/build_vectors.py --name gib
date; $PY scripts/k2tl/build_scene.py --name gib --ao --far --cls
date; $PY scripts/k2tl/build_border.py --name gib
date; bash scripts/k2tl/pack_1782.sh origin/main
date; bash scripts/k2tl/pack_g1b.sh
date; echo CACHE-XONG
