#!/bin/bash
# V5b-1 · đo s/khung theo kỹ thuật (bật/tắt từng cái), 1080p, khung lặp 2 lần (lần 2 = không tính biên dịch shader).
# Dùng: bash scripts/k2tl/bench.sh <ra.jsonl> "<khung,khung,...>" '<tech json>' [nhãn]
OUT=$1; FR=$2; TECH=$3; LAB=${4:-$3}
D=/var/tmp/cine-out/k2tl/bench; rm -rf $D; mkdir -p $D
node "$(dirname "$0")/render.js" --w 1920 --h 1080 --out $D --only "$FR" --tech "$TECH" --measure 100000 2>/dev/null >/dev/null
python3 - "$D/log.json" "$LAB" "$TECH" >> "$OUT" <<'PY'
import json, sys
d = json.load(open(sys.argv[1])); fr = d['frames']; seen = {}; rows = []
for r in fr:
    if r['f'] in seen: rows.append(r)
    seen[r['f']] = 1
print(json.dumps({"label": sys.argv[2], "tech": json.loads(sys.argv[3]), "frames": [{k: r[k] for k in ("f", "spp", "wall_ms", "lod", "shadow_upd")} for r in rows],
                  "mean_s": round(sum(r['wall_ms'] for r in rows) / max(1, len(rows)) / 1000, 3)}))
PY
tail -1 "$OUT"
