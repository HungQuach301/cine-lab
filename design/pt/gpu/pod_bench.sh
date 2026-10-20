#!/usr/bin/env bash
# NC-GPU · Blender Open Data benchmark (launcher 3.3.0) trên pod: 3 cảnh chuẩn monster / junkshop / classroom, thiết bị OPTIX (rồi CUDA nếu OPTIX lỗi).
# Bản Blender: 5.2.0 (bản gần 5.2.2 LTS nhất mà launcher hỗ trợ; danh sách: 5.2.0 5.1.1 … 3.6.0). Kết quả: /w/bench.json (samples/phút từng cảnh).
cd /w/bench; B=./benchmark-launcher-cli
$B blender list > /w/bench-ver.txt 2>&1; cat /w/bench-ver.txt | head -20
V=${BV:-5.2.0}; echo "BAN $V"
$B blender download $V > /dev/null 2>&1; $B scenes download --blender-version $V monster junkshop classroom > /dev/null 2>&1
for D in ${DEV:-OPTIX CUDA}; do
  $B benchmark --blender-version $V --device-type $D --json monster junkshop classroom > /w/bench-$D.json 2> /w/bench-$D.err && { echo "OK $D"; cp /w/bench-$D.json /w/bench.json; break; }
  echo "LOI $D"; tail -5 /w/bench-$D.err
done
python3 -c "
import json; d=json.load(open('/w/bench.json'))
for r in d: print(r['scene']['label'], r['device_info']['compute_devices'][0]['name'] if r['device_info']['compute_devices'] else '-', r['device_info']['device_type'], round(r['stats']['samples_per_minute'],2))
"
