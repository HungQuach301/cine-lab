#!/opt/cine/bin/python
"""TIEN-KY-T4 · xuất PHẦN CẢNH 1666 cho Cycles (bản thử T1 (ii)) từ ldn.bin — cùng hình học với cách A.
  cy_xuat.py <shot.json> <ra.npz> [ban_kinh_m=1400]
Giữ: nhà 1666 (k1), phế tích (k2), công trình có tên còn tồn tại 1666 (k5, t0 ≤ 1666,7 < t1), tường thành (k6), cầu cũ (k7), tháp nhà thờ cổ (k8);
địa hình h66 quanh tiêu điểm; ô cháy 20 m (giờ bén lửa) trong vùng nhìn. Toạ độ giữ hệ cảnh (x = E − 532000, y cao, z = −(N − 180800))."""
import json, os, sys
import numpy as np
DATA = os.environ.get('LDN_DATA', '/var/tmp/ldn'); C = os.path.join(DATA, 'canh')
S = json.load(open(sys.argv[1])); OUTF = sys.argv[2]; RAD = float(sys.argv[3]) if len(sys.argv) > 3 else 1400.0
M = json.load(open(os.path.join(C, 'ldn.json'))); buf = open(os.path.join(C, 'ldn.bin'), 'rb').read()
def A(nm, dt):
    l = M['bo_cuc'][nm]; return np.frombuffer(buf, dt, l['len'] // np.dtype(dt).itemsize, l['off'])
pos = A('pos', np.float32).reshape(-1, 3); col = A('col', np.uint8).reshape(-1, 3); tl = A('tl', np.float32).reshape(-1, 4); kk = A('k', np.uint8)
L = lambda e: np.array([e[0] - 532000.0, e[2], -(e[1] - 180800.0)])
k0 = S['keys'][0]; tgt = L(k0['l']); cam = L(k0['p'])
ctr = (tgt * 0.7 + cam * 0.3)
tri = pos.reshape(-1, 3, 3); tk = kk[::3]; ttl = tl[::3]; tc = col[::3]
cen = tri.mean(1)
d = np.hypot(cen[:, 0] - ctr[0], cen[:, 2] - ctr[2])
alive66 = (ttl[:, 0] <= 1666.7) & (ttl[:, 1] > 1666.66)
keep = (d < RAD) & (((tk == 1) | (tk == 2) | (tk == 6) | (tk == 7) | (tk == 8)) | ((tk == 5) & ((ttl[:, 0] <= 1666.7) & ((ttl[:, 1] > 1666.66) | (ttl[:, 3] >= 0)))))
keep &= (tk == 2) | alive66 | ((tk == 5) & (ttl[:, 3] >= 0))
T = M['dia_hinh']; h66 = A('h66', np.float32).reshape(T['nz'], T['nx'])
i0 = max(0, int((ctr[0] - RAD * 1.3 - T['x0']) / T['step'])); i1 = min(T['nx'], int((ctr[0] + RAD * 1.3 - T['x0']) / T['step']) + 1)
j0 = max(0, int((ctr[2] - RAD * 1.3 - T['z0']) / T['step'])); j1 = min(T['nz'], int((ctr[2] + RAD * 1.3 - T['z0']) / T['step']) + 1)
ter = h66[j0:j1, i0:i1]
LC = M['luoi_chay']; lg = np.fromfile(os.path.join(C, 'luoi_chay.f32'), '<f4').reshape(LC['nz'], LC['nx'])
jj, ii = np.nonzero(lg >= 0); cx = LC['E0'] - 532000 + ii * LC['buoc']; cz = -(LC['N0'] - 180800) + jj * LC['buoc']
hs = [k.get('hour', -1) for k in S['keys']]; h0, h1 = min(hs), max(hs)
ign = lg[jj, ii]; sel = (np.hypot(cx - ctr[0], cz - ctr[2]) < RAD) & (ign < h1 + 0.5) & (ign > h0 - 12.0)
gx = np.clip(((cx[sel] - T['x0']) / T['step']).astype(int), 0, T['nx'] - 1); gz = np.clip(((cz[sel] - T['z0']) / T['step']).astype(int), 0, T['nz'] - 1)
np.savez_compressed(OUTF, tri=tri[keep].astype(np.float32), col=tc[keep], tl=ttl[keep].astype(np.float32), k=tk[keep],
                    ter=ter.astype(np.float32), ter_x0=T['x0'] + i0 * T['step'], ter_z0=T['z0'] + j0 * T['step'], ter_step=T['step'],
                    cell=np.stack([cx[sel], h66[gz, gx], cz[sel], ign[sel]], 1).astype(np.float32), shot=json.dumps(S))
print(json.dumps({'tam_giac': int(keep.sum()), 'dia_hinh': list(ter.shape), 'o_chay': int(sel.sum()), 'gio': [h0, h1], 'MB': round(os.path.getsize(OUTF) / 1e6, 1)}))
