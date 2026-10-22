#!/usr/bin/env bash
# BAN-CUOI-T3 (việc 2) · CHUẨN BỊ dữ liệu Cycles GPU cho 2 đoạn dựng TRỌN bằng Cycles (không ghép A↔B trong một cú máy):
#   n29 = phần cú lặn của N2.9 (t 16,5 → 28,0 s trong shot = khung 396 → 671; máy theo design/pt/cpu/dive-opt.json τ 5,5 → 17,0 như clip giữ chỗ)
#   h2t = H2T trọn shot (5,0 s, khung 0 → 119; góc thumbnail X01/X08)
# Cùng vật + thời gian của đặc tả A (opt của heroes.json bản cuối); trạng thái 13/9/1782 = mốc nướng b1782 (albedo nhìn xuống topo-b1782 của bước nướng).
# Theo NC-GPU (design/pt/gpu, không sửa): gpu_export.js hình học ở mốc 12 khung + --lightfx từng khung; nc_topo.js --campath; dive_pack.py khử trùng lặp.
#   bash scripts/k2tl/cuoi_gpu/chuan_bi.sh [n29|h2t|ca]  → /var/tmp/cine-out/cuoi-gpu/<doan>/{exp/d-<khung>, lf/, cam.json} + <doan>.tar
set -euo pipefail
REPO=$(cd "$(dirname "$0")/../../.." && pwd); export K2TL_CACHE=${K2TL_CACHE:-/var/tmp/cine-out/k2tl-cache} NC_DESIGN=$REPO/design NC_SCRIPTS=$REPO/scripts/k2tl
G=/var/tmp/cine-out/cuoi-gpu; HJ=/var/tmp/cine-out/k2c-t3-cuoi/heroes.json; GPU=$REPO/design/pt/gpu; CPU=$REPO/design/pt/cpu; mkdir -p $G/opt
/opt/cine/bin/python - "$HJ" "$G/opt" "$REPO" <<'P'
import json, sys
H = json.load(open(sys.argv[1])); od = sys.argv[2]; R = sys.argv[3]
o = dict(H['anim_N2_9']['opt']); dv = json.load(open(R + '/design/pt/cpu/dive-opt.json'))['cam']; D = o['dur']; t0 = 16.5
lerp = lambda a, b, u: [a[i] + (b[i] - a[i]) * u for i in range(3)]
k0, k1 = dv[0], dv[1]; u = (5.5 - k0['t']) / (k1['t'] - k0['t'])
cam = [dict(t=0.0, p=o['cam'][0]['p'], l=o['cam'][0]['l'], fov=42), dict(t=t0, p=lerp(k0['p'], k1['p'], u), l=lerp(k0['l'], k1['l'], u), fov=42)]
cam += [dict(t=round(t0 + k['t'] - 5.5, 3), p=k['p'], l=k['l'], fov=k.get('fov', 42)) for k in dv if 5.5 < k['t'] <= 17.0 + 1e-6]
o['cam'] = cam; o['nc'] = {}; json.dump(o, open(od + '/n29.json', 'w'))
h = dict(H['anim_H2T']['opt']); h['nc'] = {}; json.dump(h, open(od + '/h2t.json', 'w'))
print('n29 cam', [(c['t'], [round(x) for x in c['p']]) for c in cam], 'dur', D, '· h2t dur', h['dur'])
P
mot() { local D=$1 A=$2 B=$3; local OP=$G/opt/$D.json; mkdir -p $G/$D/exp $G/$D/lf
  for F in $(seq $A 12 $B); do X=$G/$D/exp/d-$(printf %05d $F); [ -f $X/manifest.json ] && continue
    for k in 1 2 3; do echo -n "$D xuất $F (lượt $k) "; node $GPU/gpu_export.js --scene t3tl --opt "$(cat $OP)" --f $F --far 7000 --nopass --w 1920 --h 1080 --out $X 2>&1 | tail -1 || true; [ -f $X/manifest.json ] && break; done
    [ -f $X/manifest.json ] || { echo "LỖI xuất $D $F sau 3 lượt — dừng (đổi cách)"; exit 5; }; done
  [ -f $G/$D/lf/$(printf %05d $B).json ] || node $GPU/gpu_export.js --scene t3tl --opt "$(cat $OP)" --lightfx $A:$((B + 1)) --w 1920 --h 1080 --out $G/$D/lf 2>&1 | tail -1
  [ -f $G/$D/cam.json ] || node $CPU/nc_topo.js --scene t3tl --opt "$(cat $OP)" --campath $G/$D/cam.json --n $((B + 12)) --box 0,0,10,10 --res 10 --out $G/$D/tmp-topo 2>&1 | tail -1
  /opt/cine/bin/python $GPU/dive_pack.py $G/$D $G/$D.tar; }
case ${1:-ca} in n29) mot n29 396 671;; h2t) mot h2t 0 119;; ca) mot h2t 0 119; mot n29 396 671;; esac
echo CHUAN-BI-XONG
