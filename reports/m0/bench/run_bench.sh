#!/bin/bash
# M0 bước 2 — đo render 10 s cảnh mẫu, 3 phong cách, có/không motion blur. Chạy tuần tự để không tranh CPU.
# Kết quả thô: reports/m0/raw/bench-*.json và *.time (*.mem.json: RSS đỉnh cây tiến trình).
cd "$(dirname "$0")"; export PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers
R=../raw; M=../media; P=../peakmem.py
run(){ local name=$1; shift; echo "== $name $(date -u +%T)"; $P $R/bench-$name.mem.json -- "$@" > $R/bench-$name.log 2>&1; tail -1 $R/bench-$name.log; }
enc(){ local s=$(date +%s.%N); ffmpeg -hide_banner -loglevel error -y -framerate 24 -start_number $2 -i $1/f%04d.png -c:v libx264 -preset medium -crf 16 -pix_fmt yuv420p -color_primaries bt709 -color_trc bt709 -colorspace bt709 $3; echo "{\"encode_s\": $(echo "$(date +%s.%N) - $s" | bc)}" > $R/bench-$4-encode.json; }
run a-2d-mb1   node render_chromium.js --style 2d --samples 1 --out $M/a-2d-mb1.mp4 --json $R/bench-a-2d-mb1.json
run a-2d-mb8   node render_chromium.js --style 2d --samples 8 --out $M/a-2d-mb8.mp4 --json $R/bench-a-2d-mb8.json
run b-3d-mb1   node render_chromium.js --style 3d --samples 1 --out $M/b-3d-mb1.mp4 --json $R/bench-b-3d-mb1.json
run b-3d-mb8   node render_chromium.js --style 3d --samples 8 --out $M/b-3d-mb8.mp4 --json $R/bench-b-3d-mb8.json
rm -rf frames/wb1 frames/wb8 frames/ee1 frames/ee8
run c-wb-mb1   /opt/bpy/bin/python scene_bpy.py --engine WORKBENCH --start 0 --end 240 --mb 1 --outdir frames/wb1 --json $R/bench-c-wb-mb1.json
enc frames/wb1 0 $M/c-wb-mb1.mp4 c-wb-mb1
run c-wb-mb8   /opt/bpy/bin/python scene_bpy.py --engine WORKBENCH --start 96 --end 120 --mb 8 --outdir frames/wb8 --json $R/bench-c-wb-mb8.json
enc frames/wb8 96 $M/c-wb-mb8-1s.mp4 c-wb-mb8
run c-ee-mb1   /opt/bpy/bin/python scene_bpy.py --engine EEVEE --start 96 --end 120 --mb 1 --outdir frames/ee1 --json $R/bench-c-ee-mb1.json
enc frames/ee1 96 $M/c-eevee-mb1-1s.mp4 c-ee-mb1
run c-ee-mb8   /opt/bpy/bin/python scene_bpy.py --engine EEVEE --start 96 --end 102 --mb 8 --outdir frames/ee8 --json $R/bench-c-ee-mb8.json
enc frames/ee8 96 $M/c-eevee-mb8-6f.mp4 c-ee-mb8
echo "== DONE $(date -u +%T)"
