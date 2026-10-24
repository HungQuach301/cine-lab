#!/bin/bash
# GIONG-T4 · tái tạo master giọng T4 từ tệp gốc trong git (am-thanh/nguon/) — 0 ký tự ElevenLabs (cache theo băm), so SHA với SHA256SUMS master.
# Dùng: bash scripts/k2ldn/giong/tai_tao.sh [thư mục ra, mặc định /var/tmp/cine-out/giong-t4-tai-tao]
set -euo pipefail
cd "$(dirname "$0")/../../.."; R=$PWD; export GL_OUT=${1:-/var/tmp/cine-out/giong-t4-tai-tao}; PY=/opt/cine/bin/python
mkdir -p "$GL_OUT/raw"
$PY - <<PYEOF
import json, shutil, os, re
from pathlib import Path
N = Path('channel-k2/k2c-t4-02/am-thanh/nguon'); O = Path(os.environ['GL_OUT']) / 'raw'
for l in open('reports/giong-t4/so-ai.jsonl'):
    r = json.loads(l)
    for ext in ('.mp3', '.align.json'): shutil.copy2(N / (re.sub(r'[^\w.-]+', '_', r['tag']) + ext), O / r['tep'].replace('.mp3', ext))
PYEOF
$PY scripts/k2ldn/giong/gl_thu.py all | grep -v "^{" ; $PY scripts/k2ldn/giong/gl_ghep.py | tail -1
GIONG_TAI_TAO=1 $PY scripts/k2ldn/giong/gl_xuat.py > /dev/null
( cd "$GL_OUT/xuat" && grep -E "T4-loi-G1-v2-14LUFS\.(wav|flac)$" "$R/channel-k2/k2c-t4-02/am-thanh/master/SHA256SUMS" | sha256sum -c - )
