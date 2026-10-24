import sys, os, json, glob, cv2, numpy as np
sys.path.insert(0, '/home/user/cine-lab')
from checks.ll import q_k1175 as K
D = 'a5'; out = []
for nua in 'AB':
    gd = f'{D}/{nua}-goc'; R = cv2.imread(gd + '/rgb.png'); cls = cv2.imread(gd + '/cls.png')[..., ::-1]
    I = K._ma(gd + '/iid.png'); I[~np.all(cls == K.NHA_THUONG, -1)] = 0; B = cv2.imread(f'{D}/{nua}-bong/rgb.png')
    J = {h['id']: h for h in json.load(open(gd + '/nha.json'))['nha']}
    gR = K._grad(R, 1.0, True); gB = K._grad(B, 1.0)
    # cặp vách: điểm biên giữa hai mã nhà khác nhau (lân cận phải/dưới)
    pairs = {}
    for dy, dx in ((0, 1), (1, 0)):
        a = I[:I.shape[0] - dy, :I.shape[1] - dx]; b = I[dy:, dx:]; m = (a > 0) & (b > 0) & (a != b)
        ys, xs = np.nonzero(m)
        for y, x in zip(ys, xs):
            k = (min(a[y, x], b[y, x]), max(a[y, x], b[y, x])); pairs.setdefault(k, []).append((y, x))
    sel = {k: np.array(v) for k, v in pairs.items() if len(v) >= 6}
    for vd in sorted(glob.glob(f'{D}/{nua}-*/rgb.png')) + [f'/home/user/cine-lab/reports/k1175/ai/BMN-{"P1" if nua == "A" else "TRUNG"}-l1-ai.jpg']:
        v = os.path.basename(os.path.dirname(vd)) if vd.endswith('rgb.png') else f'{nua}-AI-that'
        if v.endswith('-bong') or v.endswith('-goc'): continue
        cfg = json.load(open(f'{D}/{v}.json')) if os.path.exists(f'{D}/{v}.json') else {}
        gopset = {tuple(sorted(b['ids'])) for b in cfg.get('bien_doi', []) if b['loai'] == 'gop'}
        mod = set()
        for b in cfg.get('bien_doi', []): mod |= set(b.get('ids') or [b.get('id') or b.get('gan')])
        A = cv2.resize(cv2.imread(vd), (R.shape[1], R.shape[0]), interpolation=cv2.INTER_AREA)
        M = cv2.dilate((I > 0).astype(np.uint8), np.ones((3, 3), np.uint8)) > 0; C = R.copy(); C[M] = A[M]
        gA = K._grad(C, 1.0, True); DT = cv2.distanceTransform((~(gA >= 3.0)).astype(np.uint8), cv2.DIST_L2, 3)
        for k, pts in sel.items():
            vis = (gR[pts[:, 0], pts[:, 1]] >= 3) & (gB[pts[:, 0], pts[:, 1]] >= 3)
            if vis.sum() < 6: continue
            p = pts[vis]; sup = float((DT[p[:, 0], p[:, 1]] <= 1.5).mean())
            lab = 'gop' if k in gopset else ('gan' if (k[0] in mod or k[1] in mod) else 'am')
            out.append(dict(nua=nua, bt=v, cap=[int(k[0]), int(k[1])], n=int(vis.sum()), sup=round(sup, 3), nhan=lab, px_m=J.get(int(k[0]), {}).get('px_m', 0)))
json.dump(out, open('vach.json', 'w'))
for nua in 'AB':
    for lab in ('am', 'gop'):
        X = [r for r in out if r['nua'] == nua and r['nhan'] == lab and r['bt'] != f'{nua}-AI-that']
        if X: s = np.array([r['sup'] for r in X]); print(nua, lab, len(X), 'sup p1/5/50', np.percentile(s, [1, 5, 50]).round(2), 'min', s.min().round(2), [r['sup'] for r in X][:8] if lab == 'gop' else '')
    X = [r for r in out if r['bt'] == f'{nua}-AI-that']; s = np.array([r['sup'] for r in X]); print(nua, 'AI thật', len(X), np.percentile(s, [1, 5, 50]).round(2))
