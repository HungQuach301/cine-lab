"""thu đặc trưng từng dải (tf, α, rb, res, rbw) có nhãn: 'lan' (trong đoạn bờ lấn đáp án, k < sâu) / 'am' (ca âm) — để chọn luật ở nửa A"""
import sys, os, json, cv2, numpy as np, glob
sys.path.insert(0, '/home/user/cine-lab'); sys.path.insert(0, '.')
from checks.ll import q_n2p as Q
import t9c, a1_2d as A2
G0 = 'look2/channel-k2/k2c-t4-02/ai/goc/'; F = []
for nua, rm in (('A', 'l1l2'), ('B', 'l3')):
    R = cv2.imread(G0 + f'T6-render-{rm}.jpg'); L, n = Q.idmap(G0 + f'T6-matna-{rm}.png', (1920, 1080)); Wt, top = A2.bo_tren(L, n); rng = np.random.default_rng(11 if nua == 'A' else 22)
    for m in ('xam', 'oliu', 'nau', 'nhat'):
        G = A2.phan_chieu(A2.gon_song(A2.doi_mau_nuoc(R, Wt, m, rng), Wt, rng), L, n, top, rng); g = []
        t9c.do_bo(R, G, L, n, {'_ghi': g}); F += [dict(x, nua=nua, nhan='am', ca=f'T6-{m}') for x in g]
    for kieu in ('bai', 'go', 'bun'):
        for dd in (6, 8, 12, 20):
            m = ('xam', 'oliu', 'nau', 'nhat')[dd % 4]
            G = A2.phan_chieu(A2.gon_song(A2.doi_mau_nuoc(R, Wt, m, rng), Wt, rng), L, n, top, rng); gts = []
            for (x0, x1) in A2.chon_doan(top, 3, 100, rng):
                G, _ = A2.lan_bo(G, L, n, top, x0, x1, dd, rng, kieu); gts.append((x0, x1))
            g = []; t9c.do_bo(R, G, L, n, {'_ghi': g})
            for x in g:
                ins = [gg for gg in gts if x['x0'] >= gg[0] and x['x1'] <= gg[1]]
                if ins and x['k'] + 4 <= dd: F.append(dict(x, nua=nua, nhan='lan', ca=f'T6-{kieu}-{dd}'))
json.dump(F, open('band-feat.json', 'w'), default=float); print(len(F))
