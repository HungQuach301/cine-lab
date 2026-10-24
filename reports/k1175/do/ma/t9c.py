"""nháp thước T9c (đường bờ đo + nước tự mẫu + phép thử gương) — sẽ chuyển vào checks/ll/q_n2p.py"""
import cv2, numpy as np

TALL = ('nha', 'nha_thuong', 'trai', 'congsu', 'tau', 'pin', 'lua', 'nguoi', 'khac', 'cay', 'co')
P = dict(GAP_B=2, RES=-1.0, SKIP=2, TAU_B=0.0, WIN=24, BAND=4, TALL_F=0.6, O_MAX=32, A_MIN=0.05, A_MAX=0.8, D_IN=48, TAU0=8.0, TAU_K=3.0, D_MAX=72, D_LOI=6, L_MIN=12, RHO=0.35, GAP=2, GIUA=2.0, SIG=1.5)


def lab(b):
    return cv2.cvtColor(b, cv2.COLOR_BGR2LAB).astype(np.float32) * np.array([100 / 255, 1, 1], np.float32) - np.array([0, 128, 128], np.float32)


def la_pc(tf, al, rb, res, rbw, p):
    """dải là PHẢN CHIẾU khi: điểm đối xứng qua trục gương rơi vào vật cao (≥ TALL_F), màu = pha giữa vật và nước (α ∈ [A_MIN, A_MAX]),
    phần dư màu sau khi pha ≤ RES (chọn ở nửa A khung đáp án: 0 dải bờ lấn lọt ở cả hai nửa)"""
    return tf >= p['TALL_F'] and p['A_MIN'] <= al <= p['A_MAX'] and res <= p['RES']


def do_bo(R, G, L, names, p=None, dbg=False):
    p = dict(P, **{k: v for k, v in (p or {}).items()}); H, W = R.shape[:2]; s = H / 1080.0
    ix = {n: i for i, n in enumerate(names)}
    Wt = L == ix['nuoc']; sky = L == ix['troi'] if 'troi' in ix else np.zeros_like(Wt)
    n, cc, st, _ = cv2.connectedComponentsWithStats(Wt.astype(np.uint8), 4)
    keep = [i for i in range(1, n) if st[i, 4] >= 0.002 * H * W]; Wt = np.isin(cc, keep)
    land = ~Wt & ~sky
    tall = np.isin(L, [ix[t] for t in TALL if t in ix])
    Gl = lab(cv2.GaussianBlur(G, (0, 0), p['SIG'] * s))
    dw = cv2.distanceTransform(Wt.astype(np.uint8), cv2.DIST_L2, 5)
    din = p['D_IN'] * s
    Rl = lab(cv2.GaussianBlur(R, (0, 0), p['SIG'] * s))
    # ĐỐI CHỨNG RENDER: tấm ≈ T(render) trên vùng nước, T = ánh xạ màu affine Lab (3×3 + hằng + hệ số hàng y) khớp BỀN (IRLS Huber) theo từng
    # thành phần nước → hấp thụ AI đổi sắc/độ sáng nước (A2) và GIỮ mọi thứ render có sẵn (phản chiếu vật lý của 3D, bóng đổ); còn lại là thay đổi của AI.
    dE = np.zeros((H, W), np.float32); cc2 = cv2.connectedComponents(Wt.astype(np.uint8), 4)[1]; sig_all = []
    for c in np.unique(cc2[Wt]):
        mc = cc2 == c; yy_, xx_ = np.nonzero(mc)
        X = np.c_[Rl[mc], (yy_ / H).astype(np.float32), np.ones(len(yy_), np.float32)]; Y = Gl[mc]
        if len(Y) > 60000: sel = np.random.default_rng(0).choice(len(Y), 60000, replace=False)
        else: sel = np.arange(len(Y))
        w = np.ones(len(sel), np.float32)
        for _ in range(4):
            Wx = X[sel] * w[:, None]; B = np.linalg.lstsq(Wx, Y[sel] * w[:, None], rcond=None)[0]
            e = np.sqrt(((X[sel] @ B - Y[sel]) ** 2).sum(-1)); sc = 1.4826 * np.median(e) + 1e-3; w = np.minimum(1.0, 2.0 * sc / np.maximum(e, 1e-6))
        dE[mc] = np.sqrt(((X @ B - Y) ** 2).sum(-1)); sig_all.append(sc)
    inn = Wt & (dw >= din)
    if inn.sum() < 2000: inn = Wt & (dw >= din / 2)
    ref = np.zeros((H, W, 3), np.float32)   # (giữ tên cho phép thử dải)
    sw = float(np.median(dE[inn])) * 1.4826 + 1e-3 if inn.any() else float(np.median(sig_all))
    tau = max(p['TAU0'], p['TAU_K'] * sw)
    hs = cv2.cvtColor(G, cv2.COLOR_BGR2HSV); loe = (hs[..., 2] >= 217) & (hs[..., 1] <= 64)
    NW = Wt & (dE > tau) & ~loe
    # --- bờ trên (đất phía trên nước trong ảnh): cửa sổ WIN cột × dải BAND hàng từ bờ xuống. Dải là NƯỚC nếu < 50 % điểm khác mẫu nước;
    # là PHẢN CHIẾU nếu (vật lý) điểm đối xứng qua trục gương thuộc VẬT CAO của mặt nạ (nhà, cây, tàu… — đất/bãi phẳng không tạo ảnh phản chiếu
    # nhìn từ máy cao) VÀ tương quan gradient ngang ≥ RHO VÀ màu nằm giữa vật và nước (p − w = α (m − w), α ∈ [A_MIN, A_MAX]);
    # còn lại là ĐẤT LẤN. Độ sâu lấn của cửa sổ = số hàng các dải đất lấn liền nhau tính từ bờ.
    top = Wt & np.vstack([np.zeros((1, W), bool), land[:-1]])
    Lum = Gl[..., 0]; dmax = int(p['D_MAX'] * s); WIN = max(8, int(p['WIN'] * s)); BAND = max(2, int(p['BAND'] * s)); OM = int(p['O_MAX'] * s)
    tys, txs = np.nonzero(top); ysh = np.full(W, -1, np.int64)
    for y, x in zip(tys, txs):
        if ysh[x] < 0 or y < ysh[x]: ysh[x] = y     # bờ trên cao nhất của cột (bờ xa)
    out = []; cov = np.zeros_like(Wt)
    for wx in range(0, W - WIN + 1, max(4, WIN // 3)):
        xs = np.arange(wx, wx + WIN); yv = ysh[xs]; ok = yv >= 0
        if ok.sum() < WIN * 0.7: continue
        xs, ys0 = xs[ok], yv[ok]
        # trục gương: o tốt nhất theo tương quan gradient trên toàn cột NW dưới bờ (tối đa dmax)
        K = []
        for k in range(dmax):
            yk = ys0 + k
            if (yk >= H).any(): break
            K.append(k)
        if not K: continue
        Kar = np.array(K); YA = ys0[None, :] + Kar[:, None]; XA = np.broadcast_to(xs[None, :], YA.shape)
        inw = Wt[YA, XA]; nw = NW[YA, XA] & inw
        SK = max(1, int(round(p['SKIP'] * s)))   # mép mềm của đường bờ (khử răng cưa/viền ghép) — không tính là đất
        if nw[SK:SK + (1 + p['GAP_B']) * BAND].mean(1).max() < 0.5: continue
        bo_, o_ = -1.0, 0
        rows_nw = np.nonzero(nw.mean(1) >= 0.5)[0]
        for o in range(0, OM + 1, max(1, int(s))):
            YB = ys0[None, :] - 1 - o - Kar[rows_nw][:, None]
            if (YB < 0).any(): break
            if len(rows_nw) and float(tall[YB, XA[rows_nw]].mean()) < p['TALL_F']: continue   # trục chỉ hợp lệ khi ảnh đối xứng rơi vào VẬT CAO
            a_ = np.diff(Lum[YA[rows_nw], XA[rows_nw]], axis=1).ravel(); b_ = np.diff(Lum[YB, XA[rows_nw]], axis=1).ravel()
            sa, sb = a_.std(), b_.std(); rho = float(((a_ - a_.mean()) * (b_ - b_.mean())).mean() / (sa * sb)) if sa > 0.3 and sb > 0.3 else 0.0
            if rho > bo_: bo_, o_ = rho, o
        depth, nb, kind, depth_gap = 0, 0, [], 0
        for b0 in range(SK, len(K) - BAND + 1, BAND):
            sl = slice(b0, b0 + BAND); f = nw[sl].mean()
            if f < 0.5 or float(dE[YA[sl], XA[sl]].mean()) < p['TAU_B']:
                if depth == 0 and b0 < SK + p['GAP_B'] * BAND: depth_gap = b0 + BAND - SK; continue   # mép bờ (kè/bóng) ≤ GAP_B dải có thể giống nước: bờ lấn bắt đầu ngay dưới
                break
            YB = ys0[None, :] - 1 - o_ - Kar[sl][:, None]
            if (YB < 0).any(): kind.append('lan'); depth += BAND; continue
            ya, xa = YA[sl], XA[sl]; tf = float(tall[YB, xa].mean())
            pv = Gl[ya, xa] - ref[ya, xa]; mv = Gl[YB, xa] - ref[ya, xa]
            al = float((pv * mv).sum() / max(1e-6, (mv * mv).sum()))
            a_ = np.diff(Lum[ya, xa], axis=1).ravel(); b_ = np.diff(Lum[YB, xa], axis=1).ravel(); sa, sb = a_.std(), b_.std()
            rb = float(((a_ - a_.mean()) * (b_ - b_.mean())).mean() / (sa * sb)) if sa > 0.3 and sb > 0.3 else (1.0 if sa <= 0.3 and sb <= 0.3 else 0.0)
            pr = pv - al * mv; res = float(np.sqrt((pr ** 2).sum(-1)).mean() / max(1e-6, np.sqrt((pv ** 2).sum(-1)).mean()))
            if p.get('_ghi') is not None: p['_ghi'].append(dict(x0=int(xs.min()), x1=int(xs.max()), y=int(np.median(ys0)), k=b0, tf=tf, al=al, rb=rb, res=res, rbw=bo_))
            if la_pc(tf, al, rb, res, bo_, p): kind.append('pc'); break
            kind.append('lan'); depth += BAND
            cov[ya[nw[sl]], xa[nw[sl]]] = True
        # phần dưới (phản chiếu/nước) cũng tính là đã xét để không rơi vào 'giữa nước'
        for c in range(len(xs)):
            col = nw[:, c]; e = int(np.argmin(col)) if (~col).any() else len(col); cov[ys0[c]:ys0[c] + e, xs[c]] = True
        depth = depth + SK + depth_gap if depth else 0
        out.append(dict(x0=int(xs.min()), x1=int(xs.max()), y=int(np.median(ys0)), sau_px=round(depth / s, 1), truc=o_, rho=round(bo_, 3),
                        dai=''.join('L' if k == 'lan' else 'P' for k in kind)))
    # gộp cửa sổ lấn liền nhau thành đoạn; lỗi nếu sâu ≥ D_LOI và dài ≥ L_MIN
    segs = []
    for w_ in sorted([x for x in out if x['sau_px'] >= p['D_LOI']], key=lambda z: z['x0']):
        if segs and w_['x0'] <= segs[-1]['x1'] + 2: segs[-1]['x1'] = max(segs[-1]['x1'], w_['x1']); segs[-1]['sau_px'] = max(segs[-1]['sau_px'], w_['sau_px'])
        else: segs.append(dict(x0=w_['x0'], x1=w_['x1'], y=w_['y'], sau_px=w_['sau_px']))
    for sg in segs: sg['dai_px'] = round((sg['x1'] - sg['x0'] + 1) / s, 1); sg['lan'] = sg['dai_px'] >= p['L_MIN']; sg['phan_chieu'] = False
    out_seg = segs
    # --- phần còn lại: NW không thuộc dải cột bờ trên → bám bờ khác (dưới/bên) hoặc giữa nước
    rest = NW & ~cov
    n2, c2, s2, _ = cv2.connectedComponentsWithStats(rest.astype(np.uint8), 8)
    edge = Wt & (dw <= 1.5)
    khac = []; giua = 0
    for i in range(1, n2):
        m = c2 == i
        if (m & edge).any() and not (m & top).any():
            dep = float(dw[m].max()); khac.append(dict(hop=[int(s2[i, 0]), int(s2[i, 1]), int(s2[i, 0] + s2[i, 2]), int(s2[i, 1] + s2[i, 3])], sau_px=round(dep / s, 1), px=int(s2[i, 4]),
                                                      lan=bool(dep / s >= p['D_LOI'] and s2[i, 4] / s / s >= p['L_MIN'] * p['D_LOI'])))
        elif not (m & edge).any(): giua += int(s2[i, 4])
    giua_pct = 100.0 * giua / max(1, Wt.sum())
    lan = [x for x in out_seg if x['lan']] + [x for x in khac if x['lan']]
    res = dict(tau=round(tau, 2), sigma_nuoc=round(sw, 2), nw_pct=round(100.0 * NW.sum() / max(1, Wt.sum()), 2), giua_pct=round(giua_pct, 2),
               cua_so=len(out), cua_so_pc=len([x for x in out if 'P' in x['dai']]), doan_lan=len([x for x in out_seg if x['lan']]),
               bo_khac_lan=len([x for x in khac if x['lan']]), lan=sorted(lan, key=lambda z: -z.get('sau_px', 0))[:20], seg=out_seg, win=out,
               dat=(not lan) and giua_pct <= p['GIUA'])
    if dbg: res['_NW'] = NW; res['_cov'] = cov
    return res
