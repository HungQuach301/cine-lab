"""W4T (Cổng 6, thân Cas) — đo c3_views 8 góc, CÙNG CÁCH c3_cas.py / c3_bl.py (mặt nạ bộ phận nhìn thấy 4×, turnaround, máy trực giao),
tính CẢ HAI cách đo độ dài đầu theo checks/RUN.md mục 3.6.1 (v1.5; chỉ đọc tài liệu, không dùng mã checks/):
  'pca': bề dài chiếu điểm ảnh mặt nạ đầu lên trục chính PCA + 1 px (như v1.4);
  'doc': bề dài chiếu lên TRỤC DỌC THÂN + 1 px; trục = vectơ đơn vị từ tâm mặt nạ thân tới tâm mặt nạ đầu (tâm = trung bình toạ độ điểm ảnh);
         không có mặt nạ thân → phương dọc ảnh.
Bộ phận khác luôn theo trục chính PCA. Tỷ lệ = bộ phận / đầu (theo cách khai).
Chạy (làn nặng): /opt/cine/bin/python c3_w4t.py <thư mục ra> <cas|ida> <trang từ design/cong3> [góc...]
Chỉ đo lại mặt nạ đã có: /opt/cine/bin/python c3_w4t.py --masks <thư mục có <who><góc>/x.parts> <cas|ida>"""
import json, os, subprocess, sys
import numpy as np
from PIL import Image
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../..'))
PARTS = ['head', 'torso', 'upper_arm', 'forearm', 'thigh', 'shin']
ANG0 = [0, 45, -45, 90, -90, 135, -135, 180]
def pts(p):
    if not os.path.exists(p): return None
    a = np.asarray(Image.open(p).convert('RGBA'))[..., 3]; ys, xs = np.nonzero(a >= 128)
    return np.stack([xs, ys], 1).astype(float) if len(xs) >= 50 else None
def plen(P):
    Q = P - P.mean(0); w, v = np.linalg.eigh(np.cov(Q.T)); pr = Q @ v[:, -1]; return float(pr.max() - pr.min() + 1)
def dlen(Ph, Pt):
    ax = np.array([0.0, 1.0]) if Pt is None else (Ph.mean(0) - Pt.mean(0))
    ax = ax / np.linalg.norm(ax); pr = Ph @ ax; return float(pr.max() - pr.min() + 1)
def measure(d):
    P = {k: pts(os.path.join(d, 'x.parts', '00000', f'{k}.png')) for k in PARTS}
    L = {k: (plen(v) if v is not None else None) for k, v in P.items()}
    hp, hd = L['head'], dlen(P['head'], P['torso'])
    r = {'pca': {k: (round(v / hp, 3) if v else None) for k, v in L.items()}, 'doc': {k: (round(v / hd, 3) if v else None) for k, v in L.items()}}
    r['doc']['head'] = 1.0; r['_dau_px_pca'] = round(hp, 1); r['_dau_px_doc'] = round(hd, 1); r['_px'] = {k: (round(v, 1) if v else None) for k, v in L.items()}
    return r
if sys.argv[1] == '--masks':
    D, who = sys.argv[2], sys.argv[3]; res = {}
    for ang in ANG0:
        d = os.path.join(D, f'{who}{ang}')
        if os.path.isdir(d): res[f'{ang}°'] = measure(d); print(ang, res[f'{ang}°']['_dau_px_doc'], res[f'{ang}°']['doc']['torso'], flush=True)
    json.dump(res, open(os.path.join(D, f'c3_w4t_{who}.json'), 'w'), indent=1, ensure_ascii=False); sys.exit()
OUT, who, page = sys.argv[1], sys.argv[2], sys.argv[3]; ANG = [int(a) for a in sys.argv[4:]] or ANG0
res = {}
for ang in ANG:
    d = os.path.join(OUT, f'{who}{ang}'); os.makedirs(d, exist_ok=True); vid = os.path.join(d, 'x.mp4'); open(vid, 'a').close()
    subprocess.run(['node', 'shared/export_sidecars.js', '--page', page, '--shot', 'turn', '--video', vid, '--parts', '0', '--scale', '4', '--only-parts',
                    '--args', json.dumps({'char': '3d', 'dbg': {'who': who, 'view': ang}})], cwd=os.path.join(REPO, 'design/cong3'), check=True, capture_output=True)
    res[f'{ang}°'] = measure(d); print(who, ang, res[f'{ang}°']['_dau_px_pca'], res[f'{ang}°']['_dau_px_doc'], res[f'{ang}°']['pca']['torso'], res[f'{ang}°']['doc']['torso'], flush=True)
json.dump(res, open(os.path.join(OUT, f'c3_w4t_{who}.json'), 'w'), indent=1, ensure_ascii=False)
