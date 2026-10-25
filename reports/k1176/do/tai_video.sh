#!/bin/bash
# K-1.17.6 · tái tạo video kiểm KHÔNG MẤT của THU-B (video-sha.json) bằng ĐÚNG mã THU-B @353d0f0c (bản sao /var/tmp/k1176/src, không sửa).
#   bash tai_video.sh <khung…>   (mặc định B3-p4-1938 M4-trung M1-trung) — lượt 2 (l2)
set -o pipefail
cd /var/tmp/k1176/src
export LDN_DATA=/var/tmp/ldn THUB=/var/tmp/ldn/thub MA_HOA_KIEM=1
PY=/opt/cine/bin/python; S=scripts/k2ldn; T=channel-k2/k2c-t4-02/thu-b/tam
t() { echo "[$(date -u +%H:%M:%S)] $*"; }
[ -f $LDN_DATA/look3b/ldn2.bin ] || { t LOOK3B; $PY $S/thu-b/hinh_hoc_thub.py b || exit 2; sha256sum $LDN_DATA/look3b/ldn2.bin; }
[ -f $LDN_DATA/look2/bake_1938.7.png ] || { t NUONG1938; LDN_LOOK=look2 /opt/bpy/bin/python $S/nuong_look.py 1938.7 $LDN_DATA/look2/bake_1938.7.png --box 530800,179700,534000,182000 || exit 2; sha256sum $LDN_DATA/look2/bake_1938.7.png; }
for K in ${@:-B3-p4-1938 M4-trung M1-trung}; do
  mkdir -p $THUB/bp/$K; cp -rn $T/$K/. $THUB/bp/$K/
  t DUNG $K; $PY - "$K" <<'PYEOF' || exit 2
import sys, os, json, subprocess, time
sys.path.insert(0, 'scripts/k2ldn/thu-b'); import dung as D
k = sys.argv[1]; pj = json.load(open(f'{D.THUB}/bp/{k}/l2/proj.json'))
J = [D.job(f'tl-{k}-v2', 'tl-' + k)]
if k.startswith('M1'): J.append(D.job(f'tl-{k}-v2-kk', 'tl-' + k + '-khongkhoi'))
J.append(D.job(f'tl-{k}-bp-l2', 'tl-' + k, 'thu-b/look3', 'look3b/', key={'proj': {'url': f'/data/thub/bp/{k}/l2/proj.png', 'vp': pj['vp']}}))
for name, cmd, n in J:
    if D.xong(name, n): print('ĐÃ CÓ', name, flush=True); continue
    while D.ram() < 5000: time.sleep(5)
    t0 = time.time(); r = subprocess.run(cmd, stdout=open(f'{D.THUB}/r/{name}.log', 'w'), stderr=subprocess.STDOUT, env=dict(os.environ, LDN_DATA=D.D))
    print('XONG' if r.returncode == 0 else f'LỖI {r.returncode}', name, round(time.time() - t0, 1), 's', flush=True)
    if r.returncode: sys.exit(2)
PYEOF
  t TL $K; $PY $S/thu-b/bmn_thub.py tl $K l2 || exit 2
  t TISO $K; $PY $S/thu-b/bmn_thub.py tiso $K l2 || exit 2
  sha256sum $THUB/bp/$K/l2/tl-*.mp4
done
t TAI-XONG
