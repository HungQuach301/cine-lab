#!/bin/bash
# GPU-RD · việc 6: đo nhanh tối ưu CPU còn chưa thử (3 khung 470/175/300, SPP2, 1080p, dựng 2 lần lấy lần 2) + lưu khung để so hình với SwiftShader.
# Dùng: bash research/gpu/cpu_bench.sh <checkout v5b1b> <thư mục ra khung>   (ghi research/gpu/do/cpu-*.json)
set -u; V=$1; F=$2; D=$(cd "$(dirname "$0")" && pwd); O=$D/do; export K2TL_CACHE=${K2TL_CACHE:-/var/tmp/cine-out/k2tl-cache}
run() { local name=$1 gl=$2 tech=$3; shift 3
  CINE_GL=$gl node "$D/profile.js" --root "$V" --only 470,175,300 --rep 2 --tech "$tech" --out "$O/cpu-$name.json" --save "$F/$name" "$@" 2>/dev/null | tail -1 | sed "s/^/$name /"; }
run ss swiftshader '{"spp":2}'
run llvmpipe egl '{"spp":2}'
run ss-bong2048 swiftshader '{"spp":2,"shadowRes":2048}'
run ss-540p swiftshader '{"spp":2}' --w 960 --h 540
# 2 tiến trình song song trong 1 container (4 vCPU)
( CINE_GL=swiftshader node "$D/profile.js" --root "$V" --rep 2 --tech '{"spp":2}' --out "$O/cpu-ss-song2-a.json" 2>/dev/null | tail -1 | sed 's/^/ss-song2-a /' ) &
( CINE_GL=swiftshader node "$D/profile.js" --root "$V" --rep 2 --tech '{"spp":2}' --out "$O/cpu-ss-song2-b.json" 2>/dev/null | tail -1 | sed 's/^/ss-song2-b /' ) &
wait
