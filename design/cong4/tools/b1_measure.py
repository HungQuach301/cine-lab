"""B1 (Cổng 4, Q-C3v A / Q-C3w A): đo tỷ lệ bộ phận / đầu trên mặt nạ nhìn thấy 4×, tư thế turnaround, máy trực giao, theo góc.
Cùng cách C3 (RUN.md 3.6): độ dài = bề dài chiếu lên trục chính PCA của tâm điểm ảnh + 1 px; điểm ảnh ≥ 128 (alpha).
Chạy: /opt/cine/bin/python design/cong4/tools/b1_measure.py <thư mục ra> [góc...]"""
import json, os, subprocess, sys
import numpy as np
from PIL import Image
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
OUT = sys.argv[1]; ANG = [int(a) for a in sys.argv[2:]] or [0, 45, -45, 90, -90, 135, -135, 180]
PARTS = {'ida': ['head', 'torso', 'upper_arm', 'forearm', 'thigh', 'shin'], 'cas': ['head', 'torso', 'upper_arm', 'forearm', 'thigh', 'shin']}
def plen(p):
    a = np.asarray(Image.open(p).convert('RGBA'))[..., 3]; ys, xs = np.nonzero(a >= 128)
    if len(xs) < 50: return None
    P = np.stack([xs, ys], 1).astype(float); P -= P.mean(0); w, v = np.linalg.eigh(np.cov(P.T)); ax = v[:, -1]; pr = P @ ax
    return float(pr.max() - pr.min() + 1)
res = {}
for who in ['ida', 'cas']:
    for ang in ANG:
        d = os.path.join(OUT, f'{who}{ang}'); os.makedirs(d, exist_ok=True); vid = os.path.join(d, 'x.mp4'); open(vid, 'a').close()
        subprocess.run(['node', 'shared/export_sidecars.js', '--page', 'v2/page.js', '--shot', 'turn', '--video', vid, '--parts', '0', '--scale', '4', '--only-parts',
                        '--args', json.dumps({'char': '3d', 'dbg': {'who': who, 'view': ang}})], cwd=os.path.join(REPO, 'design/cong3'), check=True, capture_output=True)
        L = {k: plen(os.path.join(d, 'x.parts', '00000', f'{k}.png')) if os.path.exists(os.path.join(d, 'x.parts', '00000', f'{k}.png')) else None for k in PARTS[who]}
        res[f'{who}{ang}'] = {k: (round(v / L['head'], 3) if v and L['head'] else None) for k, v in L.items()}
        res[f'{who}{ang}']['_head_px'] = L['head']
        print(who, ang, res[f'{who}{ang}'], flush=True)
json.dump(res, open(os.path.join(OUT, 'b1_all.json'), 'w'), indent=1)
