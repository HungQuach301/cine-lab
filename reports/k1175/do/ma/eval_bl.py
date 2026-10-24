"""A1 trên cảnh Blender: phản chiếu VẬT LÝ (Cycles) + bờ lấn hình học (đáp án từ mặt nạ lớp của biến thể) + nước đổi sắc"""
import sys, os, json, glob, cv2, numpy as np
sys.path.insert(0, '/home/user/cine-lab'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from checks.ll import q_n2p as Q
import t9c
S = os.path.dirname(os.path.abspath(__file__)); D = S + '/a1'
BANG = {'nha_thuong': (215, 215, 215), 'troi': (110, 152, 229)}
P = json.loads(sys.argv[1]) if len(sys.argv) > 1 else {}
out = []
for nua in 'AB':
    gd = f'{D}/{nua}-goc'
    if not os.path.exists(gd + '/rgb.png'): continue
    R = cv2.imread(gd + '/rgb.png'); L, n = Q.idmap(gd + '/cls.png', (R.shape[1], R.shape[0]), BANG)
    Wt0 = L == n.index('nuoc')
    for vd in sorted(glob.glob(f'{D}/{nua}-*/rgb.png')):
        v = os.path.basename(os.path.dirname(vd)); G = cv2.imread(vd); gts = []
        if '-lan' in v:
            L2, _ = Q.idmap(os.path.dirname(vd) + '/cls.png', (R.shape[1], R.shape[0]), BANG)
            new = Wt0 & (L2 != n.index('nuoc'))
            nn, cc, st, _ = cv2.connectedComponentsWithStats(new.astype(np.uint8), 8)
            for i in range(1, nn):
                if st[i, 4] < 20: continue
                xs = np.nonzero((cc == i).any(0))[0]; dep = int((cc == i).sum(0).max())
                gts.append((int(xs.min()), int(xs.max()), dep))
        d = t9c.do_bo(R, G, L, n, P)
        hit = []
        for (x0, x1, dd) in gts:
            ok = any(('x0' in x and min(x1, x['x1']) - max(x0, x['x0']) >= 0.3 * (x1 - x0 + 1)) or ('hop' in x and min(x1, x['hop'][2]) - max(x0, x['hop'][0]) >= 0.3 * (x1 - x0 + 1)) for x in d['lan'])
            hit.append(dict(x0=x0, x1=x1, d=dd, bat=bool(ok), seg=[w for w in d['win'] if min(x1, w['x1']) - max(x0, w['x0']) > 0][:5]))
        thua = [x for x in d['lan'] if not any(('x0' in x and min(g[1], x['x1']) - max(g[0], x['x0']) > 0) or ('hop' in x and min(g[1], x['hop'][2]) - max(g[0], x['hop'][0]) > 0) for g in gts)]
        out.append(dict(nua=nua, nen='blender-' + nua, ca=v, loai='duong' if gts else 'am', dat=bool(d['dat']), giua=d['giua_pct'], tau=d['tau'], hit=hit, thua=len(thua), thua_ct=thua[:4]))
json.dump(out, open(sys.argv[2] if len(sys.argv) > 2 else S + '/a1-bl.json', 'w'), default=float)
