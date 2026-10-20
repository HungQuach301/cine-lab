#!/usr/bin/env bash
# NC-GPU · cài trên pod (python:3.13-slim-bookworm): thư viện X tối thiểu cho Blender chạy nền, Blender 5.2.2 LTS (đúng bản NC-CPU), bộ benchmark Blender Open Data 3.3.0.
# Không đưa khoá nào lên pod. Chạy: bash /w/gpu/pod_setup.sh  → /w/setup.json
set -e; cd /w
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq && apt-get install -y -qq --no-install-recommends curl xz-utils libx11-6 libxi6 libxxf86vm1 libxfixes3 libxrender1 libgl1 libegl1 libxkbcommon0 libsm6 libice6 libgomp1 ca-certificates procps > /dev/null
UA="CineLab-research (+https://github.com/HungQuach301/cine-lab)"
t0=$(date +%s)
[ -d blender ] || { curl -sSL -A "$UA" https://download.blender.org/release/Blender5.2/blender-5.2.2-linux-x64.tar.xz | tar -xJ && mv blender-5.2.2-linux-x64 blender; }
[ -d bench ] || { mkdir -p bench && curl -sSL -A "$UA" https://download.blender.org/release/BlenderBenchmark2.0/launcher/benchmark-launcher-cli-3.3.0-linux.tar.gz | tar -xz -C bench; }
t1=$(date +%s)
nvidia-smi --query-gpu=name,memory.total,driver_version,clocks.max.sm,power.limit --format=csv > gpu.csv 2>&1 || true
cat > /w/dev.py <<'P'
import bpy, json
p = bpy.context.preferences.addons['cycles'].preferences; out = {}
for t in ('OPTIX', 'CUDA'):
    try: p.compute_device_type = t; p.refresh_devices(); out[t] = [(d.name, d.type) for d in p.devices if d.type == t]
    except Exception as e: out[t] = repr(e)
print('DEV', json.dumps(out))
P
./blender/blender -b --factory-startup -P /w/dev.py 2>&1 | grep DEV > dev.txt || true
python3 - <<P
import json, os
json.dump({'tai_cai_s': $t1 - $t0, 'gpu': open('/w/gpu.csv').read(), 'dev': open('/w/dev.txt').read(), 'cpu': os.cpu_count(), 'ram_GB': round(os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES') / 1e9, 1)}, open('/w/setup.json', 'w'))
P
cat /w/setup.json
