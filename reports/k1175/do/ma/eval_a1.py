"""đánh giá thước T9c trên khung đáp án A1/A2 (2D trên T6/look2 + Blender) — ra JSON đặc trưng từng đoạn để chọn ngưỡng ở nửa A, kiểm ở nửa B"""
import sys, os, json, glob, cv2, numpy as np
sys.path.insert(0, '/home/user/cine-lab'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from checks.ll import q_n2p as Q
import t9c, a1_2d as A2
S = os.path.dirname(os.path.abspath(__file__)); G0 = S + '/look2/channel-k2/k2c-t4-02/ai/goc/'; K = S + '/look2/reports/look-t4-v2/khung/'; AI = S + '/look2/channel-k2/k2c-t4-02/ai/goc-v2/'
P = json.loads(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].startswith('{') else {}
which = sys.argv[2] if len(sys.argv) > 2 else 'all'


def base(nm):
    if nm.startswith('T6'):
        rm = nm.split('-')[1]; R = cv2.imread(G0 + f'T6-render-{rm}.jpg'); L, n = Q.idmap(G0 + f'T6-matna-{rm}.png', (1920, 1080)); return R, L, n
    R = cv2.imread(K + f'{nm}-v2-3d.jpg'); L, n = A2.mat_na_tu_render(R); return R, L, n


def chay(R, G, L, n, gts):
    d = t9c.do_bo(R, G, L, n, P)
    f = [x for x in d['lan']]
    hit = []
    for (x0, x1, dd) in gts:
        ok = any(('x0' in x and min(x1, x['x1']) - max(x0, x['x0']) >= 0.3 * (x1 - x0)) or ('hop' in x and min(x1, x['hop'][2]) - max(x0, x['hop'][0]) >= 0.3 * (x1 - x0)) for x in f)
        hit.append(dict(x0=x0, x1=x1, d=dd, bat=bool(ok), seg=[x for x in d['win'] if min(x1, x['x1']) - max(x0, x['x0']) > 0][:4]))
    thua = [x for x in f if not any(('x0' in x and min(g[1], x['x1']) - max(g[0], x['x0']) > 0) or ('hop' in x and min(g[1], x['hop'][2]) - max(g[0], x['hop'][0]) > 0) for g in gts)]
    return dict(dat=bool(d['dat']), giua=float(d['giua_pct']), tau=d['tau'], hit=hit, thua=len(thua), thua_ct=thua[:4], seg=[x for x in d['seg'] if x['sau_px'] >= 3])


out = []
BASES = {'A': ['T6-l1l2'], 'B': ['T6-l3']}
for nua, bs in BASES.items():
    if which not in ('all', '2d'): break
    for nm in bs:
        R, L, n = base(nm); Wt, top = A2.bo_tren(L, n); rng = np.random.default_rng(hash(nm) % 1000)
        # âm (phải ĐẠT): đổi sắc × gợn × phản chiếu tổng hợp
        for i, m in enumerate(('xam', 'oliu', 'nau', 'nhat')):
            for pc in (0, 1):
                G = A2.gon_song(A2.doi_mau_nuoc(R, Wt, m, rng), Wt, rng)
                if pc: G = A2.phan_chieu(G, L, n, top, rng)
                out.append(dict(nua=nua, nen=nm, ca=f'am-{m}-pc{pc}', loai='am', **chay(R, G, L, n, [])))
        for j, dd in enumerate((4, 6, 8, 12, 20, 30, 40)):
            m = ('xam', 'oliu', 'nau', 'nhat', 'xanh')[j % 5]
            G = R.copy() if m == 'xanh' else A2.doi_mau_nuoc(R, Wt, m, rng)
            G = A2.gon_song(G, Wt, rng)
            if j % 2: G = A2.phan_chieu(G, L, n, top, rng)
            gts = []
            for (x0, x1) in A2.chon_doan(top, 3, int(rng.choice([60, 100, 160])), rng):
                G, _ = A2.lan_bo(G, L, n, top, x0, x1, dd, rng, ('bai', 'go', 'bun')[len(gts) % 3]); gts.append((x0, x1, dd))
            out.append(dict(nua=nua, nen=nm, ca=f'lan-{dd}', loai='duong', **chay(R, G, L, n, gts)))
        print(nua, nm, 'xong', file=sys.stderr)
# thực tế look2: tấm AI lượt 3 (không mặt nạ thật — chỉ báo) + chèn bờ lấn vào tấm AI thật
if which in ('all', 'thuc'):
    for nm in ('M1-rong', 'M1-trung', 'M4-rong'):
        R, L, n = base(nm); Wt, top = A2.bo_tren(L, n)
        for cu in ('oai', 'gem'):
            for lu in (1, 2, 3):
                G = cv2.resize(cv2.imread(AI + f'{nm}-{cu}-l{lu}-ai.jpg'), (1920, 1080), interpolation=cv2.INTER_LANCZOS4)
                d0 = chay(R, G, L, n, []); d0b = t9c.do_bo(R, G, L, n, P)
                old = Q.do_tam.__wrapped__ if hasattr(Q.do_tam, '__wrapped__') else None
                out.append(dict(nua='T', nen=nm, ca=f'thuc-{cu}-l{lu}', loai='thuc', **d0))
                rng = np.random.default_rng(lu)
                for dd in (8, 20, 40):
                    gts = []; G2 = G.copy()
                    for (x0, x1) in A2.chon_doan(top, 2, 100, rng):
                        G2, _ = A2.lan_bo(G2, L, n, top, x0, x1, dd, rng); gts.append((x0, x1, dd))
                    out.append(dict(nua='T', nen=nm, ca=f'thuc-{cu}-l{lu}+lan{dd}', loai='duong_thuc', **chay(R, G2, L, n, gts)))
        print('thuc', nm, file=sys.stderr)
json.dump(out, open(sys.argv[3] if len(sys.argv) > 3 else S + '/a1-2d.json', 'w'), default=float)
