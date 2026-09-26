#!/bin/bash
# Chạy lại sạch (máy rỗi) các phép đo mb8 của Chromium; thêm thử định dạng trung gian JPEG để tách chi phí mã hoá PNG.
cd "$(dirname "$0")"; export PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers
R=../raw; M=../media; P=../peakmem.py
run(){ local name=$1; shift; echo "== $name $(date -u +%T)"; $P $R/bench-$name.mem.json -- "$@" > $R/bench-$name.log 2>&1; tail -1 $R/bench-$name.log; }
run a-2d-mb8-clean node render_chromium.js --style 2d --samples 8 --out $M/a-2d-mb8.mp4 --json $R/bench-a-2d-mb8-clean.json
run b-3d-mb8-clean node render_chromium.js --style 3d --samples 8 --out $M/b-3d-mb8.mp4 --json $R/bench-b-3d-mb8-clean.json
run a-2d-mb1-jpeg  node render_chromium.js --style 2d --samples 1 --fmt image/jpeg --out frames/a-2d-mb1-jpeg.mp4 --json $R/bench-a-2d-mb1-jpeg.json
echo "== DONE $(date -u +%T)"
