#!/bin/bash
# GPU-RD · bước 0 (chạy trên container CPU): đóng gói mọi thứ máy GPU cần — KHÔNG gồm khoá, KHÔNG gồm dữ liệu thô 1 GB (chỉ gói cảnh đã dựng ≈ 12 MB).
# Dùng: bash research/gpu/thu-gpu/0_chuan_bi_cpu.sh <checkout v5b1b> [ra.tar.zst]
set -euo pipefail
V=$(cd "$1" && pwd); OUT=${2:-/var/tmp/cine-out/gpu-thu.tar.zst}; G=$(cd "$(dirname "$0")/.." && pwd)
C=${K2TL_CACHE:-/var/tmp/cine-out/k2tl-cache}; W=$(mktemp -d)
test -f "$C/scene/gib/pack/meta.json" || { echo "thiếu gói cảnh — chạy fetch_sources/build_* (design/k2v/tl/README.md)"; exit 2; }
# 24 khung tham chiếu SwiftShader: dựng TUẦN TỰ 0..479 là 51 phút → chỉ lấy 24 khung rải bằng --only (tl tất định khi dựng lẻ: đo 16/10, lặp lại lệch 0)
FR=$(seq -s, 10 20 470)
node "$V/scripts/k2tl/render.js" --scene gib20 --pack gib --w 1920 --h 1080 --only "$FR" --out "$W/ref-swiftshader" 2> "$W/ref.err" | tail -1
mkdir -p "$W/repo" "$W/cache/scene/gib" "$W/cache/lut" "$W/cache/loc"
git -C "$V" archive HEAD design/k2v/tl design/cong3/shared scripts/k2tl | tar -x -C "$W/repo"
cp -r "$G" "$W/repo/research-gpu"; cp -r "$C/scene/gib/pack" "$W/cache/scene/gib/"; cp "$C"/lut/*.cube "$W/cache/lut/"; cp "$C/loc/ng_crop.jpg" "$W/cache/loc/"
echo "$FR" > "$W/frames.txt"; git -C "$V" rev-parse HEAD > "$W/v5b1b.sha"
tar -C "$W" -c . | zstd -q -10 -o "$OUT"; ls -la "$OUT"; sha256sum "$OUT"
