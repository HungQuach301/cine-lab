#!/opt/cine/bin/python
"""K-1.17.9 · KN-8 — T9c (q_k1175.t9c, chính hàm checks) trên ghép cũ / ghép thử bo8 / bo_dat + ca âm tổng hợp (dán vật lên nước AI):
  am_thuyen  : dán lại thuyền trắng render (vùng 'tau' lớn nhất) ở chỗ khác trên nước (thuyền AI thêm)
  am_cau     : dán dải 30 px (mặt cầu render) cắt ngang lõi nước (cầu AI thêm)
  am_bo_lan  : kéo đất (khối phía trên bờ) lấn xuống nước 20 px trên 200 px chiều dài (bờ AI dời)
  am_noi_nho : 6 đốm tối 12×6 px rải giữa nước (vật nổi nhỏ)
In giua_pct, so_doan_lan, sau_lon_nhat, và các cụm 'giữa nước' (NW không chạm bờ) ≥ 100 px @1080. kn8_t9c.py <ra.json>"""
import json, sys, cv2, numpy as np
sys.path.insert(0, '/home/user/cine-lab')
from checks.ll import q_k1175 as K75, q_n2p as N
IN = '/var/tmp/k1179/in/channel-k2/k2c-t4-02/ban-cuoi/e/tam'; KN = '/var/tmp/k1179/kn8'


def do(R, G, L, names):
    r = K75.t9c(R, G, L, names, dbg=True); NW = r.pop('_NW'); r.pop('win', None)
    Wt = L == names.index('nuoc'); dw = cv2.distanceTransform(Wt.astype(np.uint8), cv2.DIST_L2, 5)
    n, cc, st, _ = cv2.connectedComponentsWithStats((NW & (dw > 2)).astype(np.uint8), 8)
    cum = sorted([int(st[i, 4]) for i in range(1, n) if st[i, 4] >= 100], reverse=True)
    return dict(giua_pct=r['giua_pct'], khac_nuoc_pct=r['khac_nuoc_pct'], so_doan_lan=r['so_doan_lan'], sau=r['sau_lon_nhat_px'], tau=r['tau'], cum_giua_100px=cum[:8])


out = {}
for k, mn in (('E-P1-ngay', 'thap'), ('E-P1-ngay', 'du'), ('E-P9-ngay', 'thap')):
    luot = 'l2' if 'P1' in k else 'l1'; suf = '-thap' if mn == 'thap' else ''
    R = cv2.imread(f'{IN}/{k}/render.png'); L, names = N.idmap(f'{IN}/{k}/matna{suf}.png', (1920, 1080))
    Wt = L == names.index('nuoc'); tau = L == names.index('tau') if 'tau' in names else np.zeros_like(Wt)
    for v in ('cu', 'bo8', 'bo_dat'):
        d = f'{KN}/{k}-{luot}-{mn}' + ('-bo_dat' if v == 'bo_dat' else '')
        G = cv2.imread(f'{d}/ghep-cu.png' if v == 'cu' else f'{d}/ghep.png'); out[f'{k}-{luot}-{mn}-{v}'] = do(R, G, L, names)
    if 'P1' not in k: continue
    G0 = cv2.imread(f'{KN}/{k}-{luot}-{mn}-bo_dat/ghep.png'); dw = cv2.distanceTransform(Wt.astype(np.uint8), cv2.DIST_L2, 5)
    ys, xs = np.nonzero(Wt & (dw > 60)); cy, cx = int(np.median(ys)), int(np.median(xs))
    n, cc, st, _ = cv2.connectedComponentsWithStats(tau.astype(np.uint8), 8); i = int(np.argmax(st[1:, 4])) + 1; x, y, w, h, _a = st[i]
    G = G0.copy(); G[cy:cy + h, cx:cx + w] = R[y:y + h, x:x + w]; out[f'{k}-{mn}-am_thuyen'] = do(R, G, L, names)
    G = G0.copy(); ys2 = np.nonzero(Wt[:, cx])[0]; G[cy:cy + 30, 300:1500][Wt[cy:cy + 30, 300:1500]] = (95, 100, 105); out[f'{k}-{mn}-am_cau'] = do(R, G, L, names)
    G = G0.copy(); top = Wt & np.vstack([np.zeros((1, 1920), bool), ~Wt[:-1]])
    for xx in range(900, 1100):
        yy = np.nonzero(top[:, xx])[0]
        if len(yy): y0 = yy[0]; G[y0:y0 + 20, xx] = G0[y0 - 21:y0 - 1, xx]
    out[f'{k}-{mn}-am_bo_lan'] = do(R, G, L, names)
    G = G0.copy()
    for j in range(6): yy, xx = cy - 60 + 25 * j, cx - 300 + 110 * j; G[yy:yy + 6, xx:xx + 12] = (35, 35, 35)
    out[f'{k}-{mn}-am_noi_nho'] = do(R, G, L, names)
json.dump(out, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
for a, b in out.items(): print(a, b)
