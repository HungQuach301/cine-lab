#!/usr/bin/env bash
# BAN-CUOI-T3 · dựng lại bộ đệm cảnh gib (ngoài git, mất theo container — BAI-HOC #117) như ANIMATIC-T3-V2: v7p_cache (gói ghost SH từ main @96b5017c, cùng gốc v2) → mau_nha → faden → anim_tex.
#   setsid nohup bash scripts/k2tl/cuoi_cache.sh > /var/tmp/cine-out/log/cache.log 2>&1 &
set -euo pipefail
cd "$(dirname "$0")/../.."
export K2TL_CACHE=${K2TL_CACHE:-/var/tmp/cine-out/k2tl-cache} PY=/opt/cine/bin/python
/opt/cine/bin/pip install -q imagecodecs shapely OpenEXR tifffile pyshp
[ -n "${TU_BUOC:-}" ] || { date; $PY scripts/k2tl/fetch_sources.py; date; $PY scripts/k2tl/fetch_osm.py --name gib --bbox=-5.385,36.105,-5.320,36.185; }
date; $PY scripts/k2tl/build_rasters.py --name gib
date; $PY scripts/k2tl/build_vectors.py --name gib
date; $PY scripts/k2tl/build_scene.py --name gib --ao --far --cls
date; $PY scripts/k2tl/build_border.py --name gib
date; bash scripts/k2tl/pack_1782.sh 96b5017c
date; bash scripts/k2tl/pack_g1b.sh
date; $PY -I scripts/k2tl/v7b_mau_nha.py
date; $PY -I scripts/k2tl/v7b_faden.py
date; $PY -I scripts/k2tl/anim_tex.py
date; echo CACHE-XONG
