import json, os, numpy as np
NUOC = dict(xanh=(0.10, 0.20, 0.24), xam=(0.26, 0.26, 0.25), oliu=(0.22, 0.24, 0.13), nau=(0.24, 0.18, 0.12))
J = []
for nua, seed, may, sau_m, xs in (('A', 1, 'P1', [6, 10, 15, 20, 30, 45, 60, 80], (-400, 400)), ('B', 2, 'TRUNG', [2, 4, 6, 9, 14, 20, 28, 36], (-200, 110))):
    J.append((f'{nua}-goc', dict(seed=seed, may=may, spp=32, nuoc=dict(mau=NUOC['xanh'], nham=0.05, song=0.15))))
    for i, (nh, so) in enumerate(((0.02, 0.08), (0.10, 0.25))):
        J.append((f'{nua}-pc{i}', dict(seed=seed, may=may, spp=32, chi='rgb', nuoc=dict(mau=NUOC['xanh'], nham=nh, song=so))))
    for m in ('xam', 'oliu', 'nau'):
        J.append((f'{nua}-mau-{m}', dict(seed=seed, may=may, spp=32, chi='rgb', nuoc=dict(mau=NUOC[m], nham=0.05, song=0.15))))
    rng = np.random.default_rng(seed + 100)
    for k in range(4):
        bd = []; x = xs[0] + 10
        ds = list(rng.permutation(sau_m))[:6] if k < 3 else list(sau_m[:2]) + list(sau_m[-4:])
        ln = (xs[1] - xs[0]) / 6.5
        for j, d in enumerate(ds):
            col = [(0.62, 0.55, 0.42), (0.30, 0.24, 0.17), (0.42, 0.38, 0.30)][j % 3]
            bd.append(dict(loai='lan', x0=float(x), x1=float(x + ln * 0.7), sau_m=float(d), mau=col)); x += ln
        m = ['xanh', 'xam', 'oliu', 'nau'][k]
        J.append((f'{nua}-lan{k}', dict(seed=seed, may=may, spp=32, bien_doi=bd, nuoc=dict(mau=NUOC[m], nham=[0.05, 0.02, 0.10, 0.05][k], song=0.15))))
for n, c in J: json.dump(c, open(f'{n}.json', 'w'))
print(len(J))
