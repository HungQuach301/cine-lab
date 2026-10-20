#!/usr/bin/env bash
# NC-V2V3 · CHẠY TRÊN POD (ảnh python:3.12-bookworm): torch cu130 + ComfyUI bản phát hành ghim + trọng số Wan2.2-VACE-Fun-A14B fp8 (Comfy-Org, Apache-2.0) từ Hugging Face công khai.
# Không khoá nào trên pod; tải HF ẩn danh. Kiểm SHA-256 từng tệp trọng số với LFS oid đọc từ API HF (ghi ở design/k2v/v2v3/models.json).
set -euo pipefail
cd /w
T0=$(date +%s)
export PIP_DISABLE_PIP_VERSION_CHECK=1 PIP_ROOT_USER_ACTION=ignore
python3 -m venv /w/venv && . /w/venv/bin/activate
pip install -q --index-url https://download.pytorch.org/whl/cu130 torch torchvision torchaudio
echo "torch xong $(( $(date +%s) - T0 )) s"; python -c "import torch;print(torch.__version__, torch.version.cuda, torch.cuda.get_device_name(0))"
git clone -q --depth 1 --branch v0.42.1 https://github.com/comfyanonymous/ComfyUI /w/ComfyUI
cd /w/ComfyUI && git log -1 --format='ComfyUI %H %cd' && pip install -q -r requirements.txt && pip install -q huggingface_hub hf_transfer
mkdir -p custom_nodes/v2v3 && cp /w/v2v3/comfy_node/__init__.py custom_nodes/v2v3/__init__.py
echo "comfy xong $(( $(date +%s) - T0 )) s"
export HF_HUB_ENABLE_HF_TRANSFER=1
python3 - <<'EOF'
import json, hashlib, os, time
from huggingface_hub import hf_hub_download
M = json.load(open('/w/v2v3/models.json'))
for m in M['files']:
    t = time.time(); p = hf_hub_download(m['repo'], m['path'], revision=m['rev'], local_dir='/w/hf')
    d = os.path.join('/w/ComfyUI/models', m['dst']); os.makedirs(d, exist_ok=True); q = os.path.join(d, os.path.basename(m['path']))
    if not os.path.exists(q): os.symlink(p, q)
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(1 << 24), b''): h.update(c)
    ok = h.hexdigest() == m['sha256']; print(json.dumps({'tep': m['path'], 'GB': round(os.path.getsize(p) / 1e9, 2), 's': round(time.time() - t, 1), 'sha_khop': ok}), flush=True)
    if not ok: raise SystemExit('SHA LỆCH ' + m['path'])
EOF
echo "mo hinh xong $(( $(date +%s) - T0 )) s"
nohup python main.py --listen 127.0.0.1 --port 8188 --disable-auto-launch > /w/comfy.log 2>&1 &
for i in $(seq 1 120); do curl -s 127.0.0.1:8188/system_stats >/dev/null && break; sleep 2; done
curl -s 127.0.0.1:8188/object_info/V2V3LoadFrames | head -c 200; echo
echo "SETUP XONG $(( $(date +%s) - T0 )) s"
