#!/opt/cine/bin/python
"""K-1.17.9 · KN-8 — 2 ca âm (1080p) từ tấm ghép thử E-P1-ngay l2 "tháp" bo_dat (nước AI) để đo mô hình nhìn (đề bài n2p-e-v2-nuoc):
  am_cau     : chép dải mặt cầu render (cầu Millennium, lớp nha trên nước) dời 420 px sang trái → "cầu thứ hai" trên mặt nước AI
  am_thuyen  : chép thuyền trắng render lớn nhất (lớp tau) tới giữa lõi nước, cách 300 px → "thuyền thêm"
Ra /var/tmp/k1179/kn8/E-P1-ngay-l2-thap-bo_dat-<ca>/ (ghep.png + episode.yaml khai nuoc_ai)."""
import os, shutil, sys, yaml, cv2, numpy as np
KN = '/var/tmp/k1179/kn8'; S = f'{KN}/E-P1-ngay-l2-thap-bo_dat'
E = yaml.safe_load(open(f'{S}/episode.yaml')); t = E['n2p']['tam'][0]
G0 = cv2.imread(f'{S}/ghep.png'); R = cv2.imread(t['render']); M = cv2.imread(t['mat_na'])
nuoc = np.all(M == (190, 170, 0), -1); nha = np.all(M == (235, 235, 235), -1); tau = np.all(M == (0, 0, 255), -1)
for ca in ('am_cau', 'am_thuyen'):
    G = G0.copy()
    if ca == 'am_cau':
        cau = nha & (cv2.dilate(nuoc.astype(np.uint8), np.ones((25, 25), np.uint8)) > 0); cau[:700] = False
        ys, xs = np.nonzero(cau); ok = (xs - 420 >= 0); G[ys[ok], xs[ok] - 420] = R[ys[ok], xs[ok]]
    else:
        n, cc, st, _ = cv2.connectedComponentsWithStats(tau.astype(np.uint8), 8); i = int(np.argmax(st[1:, 4])) + 1; x, y, w, h, _a = st[i]
        m = cc[y:y + h, x:x + w] == i; G[y + 40:y + 40 + h, x + 300:x + 300 + w][m] = R[y:y + h, x:x + w][m]
    d = f'{S}-{ca}'; os.makedirs(d, exist_ok=True); cv2.imwrite(f'{d}/ghep.png', G)
    E2 = dict(E, id=E['id'] + '-' + ca); T2 = dict(t, id=t['id'] + '-' + ca, ghep=f'{d}/ghep.png'); E2['n2p'] = dict(E['n2p'], tam=[T2])
    yaml.safe_dump(E2, open(f'{d}/episode.yaml', 'w'), allow_unicode=True, sort_keys=False)
    for x in ('timeline.json', 'log-shot.json'): shutil.copy(f'{S}/{x}', f'{d}/{x}')
    print(ca, d)
