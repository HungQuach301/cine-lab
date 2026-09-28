"""W4 · cửa mặt Ida lượt 2 — đo c3_views 8 góc cho Ida 'bl', CÙNG CÁCH design/cong4/tools/b1_measure.py (W3 dùng cho 'aa'):
mặt nạ bộ phận nhìn thấy 4×, turnaround, máy trực giao; độ dài = bề dài trục chính PCA của điểm ảnh (alpha ≥ 128) + 1 px; tỷ lệ = bộ phận / đầu.
Khác duy nhất: trang = v2/char3d/blender/page_c3_bl.js (bọc v2/page.js, nạp trước glb, Ida 'bl'). Chỉ đo Ida (lưới Cas không đổi).
Chạy (làn nặng): /opt/cine/bin/python design/cong3/v2/char3d/blender/c3_bl.py <thư mục ra> [góc...]"""
import json, os, subprocess, sys
import numpy as np
from PIL import Image
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../..'))
OUT = sys.argv[1]; ANG = [int(a) for a in sys.argv[2:]] or [0, 45, -45, 90, -90, 135, -135, 180]
PARTS = ['head', 'torso', 'upper_arm', 'forearm', 'thigh', 'shin']
def plen(p):
    a = np.asarray(Image.open(p).convert('RGBA'))[..., 3]; ys, xs = np.nonzero(a >= 128)
    if len(xs) < 50: return None
    P = np.stack([xs, ys], 1).astype(float); P -= P.mean(0); w, v = np.linalg.eigh(np.cov(P.T)); ax = v[:, -1]; pr = P @ ax
    return float(pr.max() - pr.min() + 1)
res = {}
for ang in ANG:
    d = os.path.join(OUT, f'ida{ang}'); os.makedirs(d, exist_ok=True); vid = os.path.join(d, 'x.mp4'); open(vid, 'a').close()
    subprocess.run(['node', 'shared/export_sidecars.js', '--page', 'v2/char3d/blender/page_c3_bl.js', '--shot', 'turn', '--video', vid, '--parts', '0', '--scale', '4', '--only-parts',
                    '--args', json.dumps({'char': '3d', 'dbg': {'who': 'ida', 'view': ang}})], cwd=os.path.join(REPO, 'design/cong3'), check=True, capture_output=True)
    L = {k: plen(os.path.join(d, 'x.parts', '00000', f'{k}.png')) if os.path.exists(os.path.join(d, 'x.parts', '00000', f'{k}.png')) else None for k in PARTS}
    res[f'ida{ang}'] = {k: (round(v / L['head'], 3) if v and L['head'] else None) for k, v in L.items()}
    res[f'ida{ang}']['_head_px'] = L['head']
    print('ida', ang, res[f'ida{ang}'], flush=True)
json.dump(res, open(os.path.join(OUT, 'c3_bl.json'), 'w'), indent=1)
