#!/opt/cine/bin/python
"""Luật 1.17.5 (phiên K-1.17.5, 24/10/2026) — CHỈ tập kênh 2 từ T4 (`kenh2_tu_t4: true` hoặc khối `n2p:`). T3 và trước: KHÔNG ÁP.
Căn cứ: khiếu nại A1–A5 (checks-appeal.md, mục K-1.17.5) — K1174-D1 = A (chủ dự án duyệt 24/10/2026); LOOK-T4-V2 §11 (2)(3), PHIEU-LOOK-V2 V3/V4;
phương án B "AI phủ bề mặt nhà thường" (chủ dự án 24/10/2026 06:21 "1. Chọn phương án A+B theo khuyến nghị"). Số đo + khung đáp án: reports/k1175/.

(iii) T9c — ĐƯỜNG BỜ ĐO, ĐỐI CHỨNG RENDER (thay T9b chiều nước→đất trong N2P-3 (a); T9b vẫn tính và in để so):
    trên mỗi thành phần nước của mặt nạ, tấm ≈ T(render) với T = ánh xạ màu affine Lab (3×3 + hằng + hệ số hàng y) khớp BỀN (IRLS Huber) — hấp thụ
    việc AI đổi sắc/độ sáng nước (A2: xám/ô-liu vẫn là nước) và giữ mọi thứ render 3D có sẵn (phản chiếu vật lý, bóng); điểm "khác nước" = ΔE76
    (ảnh mờ σ 1,5) tới T(render) > τ = max(TAU0, TAU_K × σ lõi). Bờ trên (đất phía trên nước trong ảnh): cửa sổ WIN cột × dải BAND hàng từ bờ
    xuống (bỏ SKIP px mép mềm; cho phép ≤ GAP_B dải đầu giống nước — kè/bóng); độ sâu lấn = các dải liền nhau ≥ 50 % điểm khác nước.
    Lỗi: (a2) đoạn bờ lấn sâu ≥ D_LOI px @1080, dài ≥ L_MIN px; bờ khác (dưới/bên): cụm khác nước bám bờ sâu ≥ D_LOI; (a3) khác nước KHÔNG bám bờ
    (giữa nước) > GIUA % diện tích nước. PHẢN CHIẾU do AI tự vẽ (không có trong render) KHÔNG được miễn (A1: không tách được khỏi bờ lấn ở độ
    nhạy 100 % — số đo reports/k1175 §1); phản chiếu đúng phải có trong render 3D.
(i-s) LỚP SỐNG (A3, PHIEU V3 a): tấm khai `song: {render_co, render_khong, nen}` (render CÓ/KHÔNG khói bếp — vật chuyển động — và tấm nền đã
    ghép lớp (a) CHƯA cộng lớp sống) → ngoài vùng bảo vệ: ghép == clip(nen + (render_co − render_khong)) sai ≤ 1/255; trong vùng bảo vệ: (i) như cũ.
    (iv) đóng băng soi trên `nen` (lớp sống từ render không phải vật AI thêm); thiếu `nen` → soi ghép như cũ.
(i)(d) KHỚP MÀU CỤC BỘ VÒNG BẢO VỆ (A4, PHIEU V4 b) — chỉ khi tấm khai `khop_mau_cuc_bo: true` (cần chủ dự án sửa chữ Kinh thánh §15 (a),
    K1175-D3): vòng bảo vệ (vùng bảo vệ − mặt nạ (a)) mỗi vật = render-khớp + MỘT độ lệch màu không đổi: phần dư sau khi trừ trung vị độ lệch
    ≤ 1/255, |độ lệch| ≤ VONG_MAX mỗi kênh; trong mặt nạ (a) vẫn 0/255.
BE-MAT-NHA (A5, phương án B; chỉ tấm khai `be_mat_nha_ai: true` trong n2p.tam): xem hàm be_mat_nha().
"""
import json, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

T9C = dict(SIG=1.5, D_IN=48, TAU0=6.0, TAU_K=3.0, SKIP=2, GAP_B=2, WIN=24, BAND=4, D_MAX=72, D_LOI=6, L_MIN=12, GIUA=2.0)
VONG_MAX = 40


def ap_1175(E): return bool(E.get('kenh2_tu_t4') or E.get('n2p'))


def _lab(b):
    import cv2, numpy as np
    return cv2.cvtColor(b, cv2.COLOR_BGR2LAB).astype(np.float32) * np.array([100 / 255, 1, 1], np.float32) - np.array([0, 128, 128], np.float32)


# ================================================================ (iii) T9c
def t9c(R, G, L, names, p=None, dbg=False):
    """R render (khớp màu), G tấm đã ghép, L/names mặt nạ → dict(lan[], giua_pct, tau, dat, ...)"""
    import cv2, numpy as np
    p = dict(T9C, **(p or {})); H, W = R.shape[:2]; s = H / 1080.0; ix = {n: i for i, n in enumerate(names)}
    KA = dict(dat=True, ap=False, lan=[], so_doan_lan=0, sau_lon_nhat_px=0.0, khac_nuoc_pct=0.0, giua_pct=0.0, tau=None)   # 1.17.6 (KN-1): khung không nước → KHÔNG ÁP, đủ khoá
    if 'nuoc' not in ix: return dict(KA, ghi='không có lớp nước')
    Wt = L == ix['nuoc']; sky = (L == ix['troi']) if 'troi' in ix else np.zeros_like(Wt)
    n, cc, st, _ = cv2.connectedComponentsWithStats(Wt.astype(np.uint8), 4)
    Wt = np.isin(cc, [i for i in range(1, n) if st[i, 4] >= 0.002 * H * W])
    if not Wt.any(): return dict(KA, ghi='nước < 0,2 % khung')
    land = ~Wt & ~sky
    Gl = _lab(cv2.GaussianBlur(G, (0, 0), p['SIG'] * s)); Rl = _lab(cv2.GaussianBlur(R, (0, 0), p['SIG'] * s))
    dw = cv2.distanceTransform(Wt.astype(np.uint8), cv2.DIST_L2, 5)
    dE = np.zeros((H, W), np.float32); cc2 = cv2.connectedComponents(Wt.astype(np.uint8), 4)[1]; sig = []
    for c in np.unique(cc2[Wt]):
        mc = cc2 == c; yy, _xx = np.nonzero(mc)
        X = np.c_[Rl[mc], (yy / H).astype(np.float32), np.ones(len(yy), np.float32)]; Y = Gl[mc]
        sel = np.random.default_rng(0).choice(len(Y), 60000, replace=False) if len(Y) > 60000 else np.arange(len(Y))
        w = np.ones(len(sel), np.float32); sc = 1.0
        for _ in range(4):
            B = np.linalg.lstsq(X[sel] * w[:, None], Y[sel] * w[:, None], rcond=None)[0]
            e = np.sqrt(((X[sel] @ B - Y[sel]) ** 2).sum(-1)); sc = 1.4826 * float(np.median(e)) + 1e-3; w = np.minimum(1.0, 2.0 * sc / np.maximum(e, 1e-6))
        dE[mc] = np.sqrt(((X @ B - Y) ** 2).sum(-1)); sig.append(sc)
    inn = Wt & (dw >= p['D_IN'] * s)
    if inn.sum() < 2000: inn = Wt & (dw >= p['D_IN'] * s / 2)
    sw = 1.4826 * float(np.median(dE[inn])) + 1e-3 if inn.any() else float(np.median(sig))
    tau = max(p['TAU0'], p['TAU_K'] * sw)
    hs = cv2.cvtColor(G, cv2.COLOR_BGR2HSV); loe = (hs[..., 2] >= 217) & (hs[..., 1] <= 64)
    NW = Wt & (dE > tau) & ~loe
    top = Wt & np.vstack([np.zeros((1, W), bool), land[:-1]])
    ysh = np.full(W, -1, np.int64); ty, tx = np.nonzero(top)
    for y, x in zip(ty, tx):
        if ysh[x] < 0 or y < ysh[x]: ysh[x] = y
    dmax = int(p['D_MAX'] * s); WIN = max(8, int(p['WIN'] * s)); BAND = max(2, int(p['BAND'] * s)); SK = max(1, int(round(p['SKIP'] * s)))
    cov = np.zeros_like(Wt); win = []
    for wx in range(0, W - WIN + 1, max(4, WIN // 3)):
        xs = np.arange(wx, wx + WIN); yv = ysh[xs]; ok = yv >= 0
        if ok.sum() < WIN * 0.7: continue
        xs, ys0 = xs[ok], yv[ok]; K = np.arange(dmax); YA = np.minimum(H - 1, ys0[None, :] + K[:, None]); XA = np.broadcast_to(xs[None, :], YA.shape)
        nw = NW[YA, XA] & Wt[YA, XA]
        if nw[SK:SK + (1 + p['GAP_B']) * BAND].mean(1).max() < 0.5: continue
        depth, gap = 0, 0
        for b0 in range(SK, dmax - BAND + 1, BAND):
            f = nw[b0:b0 + BAND].mean()
            if f < 0.5:
                if depth == 0 and b0 < SK + p['GAP_B'] * BAND: gap = b0 + BAND - SK; continue
                break
            depth += BAND
        for c in range(len(xs)):
            col = nw[:, c]; e = int(np.argmin(col)) if (~col).any() else len(col); cov[ys0[c]:ys0[c] + e, xs[c]] = True
            if depth: cov[ys0[c]:ys0[c] + SK + gap + depth, xs[c]] |= NW[ys0[c]:ys0[c] + SK + gap + depth, xs[c]]
        d_ = (depth + SK + gap) if depth else 0
        win.append(dict(x0=int(xs.min()), x1=int(xs.max()), y=int(np.median(ys0)), sau_px=round(d_ / s, 1)))
    segs = []
    for w_ in sorted([x for x in win if x['sau_px'] >= p['D_LOI']], key=lambda z: z['x0']):
        if segs and w_['x0'] <= segs[-1]['x1'] + 2: segs[-1]['x1'] = max(segs[-1]['x1'], w_['x1']); segs[-1]['sau_px'] = max(segs[-1]['sau_px'], w_['sau_px'])
        else: segs.append(dict(x0=w_['x0'], x1=w_['x1'], y=w_['y'], sau_px=w_['sau_px']))
    for sg in segs: sg['dai_px'] = round((sg['x1'] - sg['x0'] + 1) / s, 1); sg['lan'] = sg['dai_px'] >= p['L_MIN']; sg['kieu'] = 'bờ trên'
    rest = NW & ~cov; n2, c2, s2, _ = cv2.connectedComponentsWithStats(rest.astype(np.uint8), 8); edge = Wt & (dw <= 1.5)
    khac, giua = [], 0
    for i in range(1, n2):
        m = c2 == i
        if (m & edge).any():
            if (m & top).any(): continue
            dep = float(dw[m].max()) / s
            if dep >= p['D_LOI'] and s2[i, 4] / s / s >= p['L_MIN'] * p['D_LOI']:
                khac.append(dict(hop=[int(s2[i, 0]), int(s2[i, 1]), int(s2[i, 0] + s2[i, 2]), int(s2[i, 1] + s2[i, 3])], sau_px=round(dep, 1), px=int(s2[i, 4]), lan=True, kieu='bờ khác'))
        else: giua += int(s2[i, 4])
    giua_pct = 100.0 * giua / max(1, int(Wt.sum()))
    lan = sorted([x for x in segs if x['lan']] + khac, key=lambda z: -z['sau_px'])
    r = dict(ap=True, tau=round(tau, 2), sigma_nuoc=round(sw, 2), khac_nuoc_pct=round(100.0 * NW.sum() / max(1, Wt.sum()), 2), giua_pct=round(giua_pct, 2),
             lan=lan[:20], so_doan_lan=len(lan), sau_lon_nhat_px=max([x['sau_px'] for x in lan] or [0.0]), dat=(not lan) and giua_pct <= p['GIUA'], win=win)
    if dbg: r['_NW'] = NW
    return r


# ================================================================ (i-s) lớp sống — A3
def kiem_song(G, P, Rc, Rk, Ab):
    """→ (sai lớn nhất ngoài vùng bảo vệ, số điểm sai > 1). G ghép · P nền (chưa lớp sống) · Rc/Rk render có/không lớp sống · Ab vùng bảo vệ"""
    import numpy as np
    exp = np.clip(P.astype(np.int16) + (Rc.astype(np.int16) - Rk.astype(np.int16)), 0, 255)
    d = np.abs(G.astype(np.int16) - exp).max(-1); d[Ab] = 0
    return int(d.max()), int((d > 1).sum())


def bao_ve(A, no=1, nho_px=60, no_nho=3):
    """vùng bảo vệ §15 (a): mặt nạ (a) nở 1 px, vật < 60 px nở thêm (no_nho) px — như n2p_lib.bao_ve phía dựng (nho_px theo 1080p)"""
    import cv2, numpy as np
    s = A.shape[0] / 1080.0; no = max(1, int(round(no * s))); no_nho = max(1, int(round(no_nho * s)))
    P = cv2.dilate(A.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * no + 1,) * 2)) > 0
    n, cc, st, _ = cv2.connectedComponentsWithStats(A.astype(np.uint8), 8)
    small = np.isin(cc, [i for i in range(1, n) if st[i, cv2.CC_STAT_AREA] < nho_px * s * s])
    if small.any(): P |= cv2.dilate(small.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * (no + no_nho) + 1,) * 2)) > 0
    return P


# ================================================================ (i)(d) vòng bảo vệ khớp màu cục bộ — A4
def kiem_vong(G, RK, A, Ab):
    """→ (phần dư lớn nhất sau khi trừ độ lệch trung vị mỗi vòng, |độ lệch| lớn nhất, số vòng). Một vòng = (thành phần vùng bảo vệ) − (a)."""
    import cv2, numpy as np
    n, cc = cv2.connectedComponents(Ab.astype(np.uint8), 8); D = G.astype(np.int16) - RK.astype(np.int16); res, off, k = 0.0, 0.0, 0
    for i in range(1, n):
        ring = (cc == i) & ~A
        if ring.sum() < 2: continue
        o = np.median(D[ring], 0); k += 1
        res = max(res, float(np.abs(D[ring] - o).max())); off = max(off, float(np.abs(o).max()))
    return res, off, k


# ================================================================ BE-MAT-NHA (A5) — AI phủ BỀ MẶT nhà thường không tên, giữ hình khối
# Tấm (mục n2p.tam) khai `be_mat_nha_ai: true` + `mat_na_nha` (PNG mã nhà 24 bit R<<16|G<<8|B, 0 = không phải nhà thường), `mat_na_mat` (PNG mã
# mặt phẳng — mỗi mặt lưới một mã; biên = sống/hông/mép mái, góc tường), `bong` (render cùng máy/giờ với albedo xám đều, không vân = PASS BÓNG),
# `nha` (JSON [{id, lo, px_m}] — px_m = điểm ảnh/mét ngang ở tâm nhà, lo = mã lô/khối phố), lớp 'nha_thuong' trong mặt nạ lớp (màu 215,215,215).
#   (a) hình khối từng nhà ĐO ĐƯỢC (px_m ≥ PPM_MIN, ≥ A_MIN px thấy, ≥ N_MIN điểm cạnh hình học thấy được): cạnh HÌNH HỌC (biên nhà ∪ biên mặt
#       phẳng, thấy được ở render VÀ pass bóng) phải được cạnh màu của ảnh ghép đỡ (≤ R_DO px). CHẶN: đỡ ở chỗ sup0 < SUP_CHAN (nhà mất/đổi khối
#       rõ — 0 báo nhầm trên khung đáp án K-1.17.5). CẢNH BÁO (w, người đọc): sup0 < SUP_MIN; dời tốt nhất trong ±S_M m ≥ D_M m với đỡ tăng ≥ G_MIN.
#       GIỚI HẠN ĐO (reports/k1175 §5): ở 1,4–4,8 px/m thước KHÔNG tách được dời 2–5 m / đổi mái khỏi "chỉ đổi bề mặt" ở 0 báo nhầm — nên chỉ
#       phần thô là Chặn. Nhà KHÔNG đo được (dưới ngưỡng) phải giữ render 0/255 (thuộc (b)).
#   (b) nhà KHÔNG đo được + mọi lớp (a) còn lại (công trình có tên 'nha', lửa/khói 'lua', tường/kè 'congsu', thuyền 'tau', 'khac', 'pho', cờ…)
#       + nước 'nuoc' + dải bờ ±BO_PX (trừ khi tấm cũng là tấm nền N2+ `nen_ai: true` — khi đó nước/bờ theo N2P-3) = 0/255 so render sau ghép.
#   (c) lỗi thời đại vật liệu/chi tiết bề mặt (kính tấm, biển hiệu chữ, điều hoà, ăng-ten, máng nhựa…): 2 mô hình nhìn (lời nhắc BMN) + q_thoi_dai
#       (O2) — chỉ khi chạy --vision (k2check --n2p-vision); không có bộ đệm → THIẾU.
#   (d) ổn định theo thời gian (timelapse CODINH, `be_mat_nha_video: {ghep, render, cach}`): mỗi nhà, quỹ đạo độ sáng ghép phải theo render:
#       e_h = max_t |ln(C_h(t)/C_h(0)) − ln(R_h(t)/R_h(0))| ≤ E_MAX ở ≥ (100 − NHA_LECH_PCT) % nhà đo được; nhấp nháy vùng nhà ≤ 1,5 × đối chứng (sàn 0,02).
#   (e) cách dùng: `cach: anh_tinh` (ghép ảnh tĩnh theo mặt nạ — chỉ CODINH; (d) bắt khi ánh sáng đổi mà bề mặt đứng yên) | `chieu_3d` (chiếu
#       ảnh AI lên hình học rồi dựng lại ánh sáng — thêm: khung 0 phải khớp tấm đã duyệt: ΔE76 TB vùng nhà ≤ T0_DE, p95 ≤ T0_P95 — bắt ánh sáng
#       chồng 2 lần khi không khử sáng ảnh AI). Mức: Chặn ở G2 · Cảnh báo ở animatic.
BMN = dict(SIG=1.0, T_VIS=3.0, T_AI=3.0, R_DO=1.5, S_M=4.0, PPM_MIN=2.0, A_MIN=100, N_MIN=40, D_M=1.5, G_MIN=0.30, SUP_CHAN=0.20, SUP_MIN=0.45, BO_PX=8,
           E_MAX=0.10, NHA_LECH_PCT=2.0, NHAP_MAX=0.012, T0_DE=4.0, T0_P95=12.0)
NHA_THUONG = (215, 215, 215)
PROMPT_BMN_VER = 'bmn-v2 (K-1.17.5, 24/10/2026: năm bắt buộc)'
PROMPT_BMN = """You are a strict inspector for a historical documentary. The scene depicts {noi} in the year {nam}. An AI tool repainted ONLY the SURFACES
(walls, roofs, windows, doors, chimneys) of ordinary houses; the shapes of buildings are fixed by our 3D model.
Read ALL the image files below with the Read tool before answering (paths are absolute):
BEFORE = our own 3D render:
{truoc}
AFTER = the version with AI-painted house surfaces (same camera):
{sau}
The quarter images are 1.5x enlargements: q1 top-left, q2 top-right, q3 bottom-left, q4 bottom-right of the full frame.
Task: list every MATERIAL or SURFACE DETAIL on the houses in AFTER that could not exist in the year {nam} — for example large plate glass or glass
curtain walls, modern window frames, shop signs or any lettering, air-conditioning units, satellite dishes or antennas, solar panels, plastic gutters
or pipes, electric lights or neon, corrugated metal, concrete render, painted road markings, and anything in this list: {cam}.
Also list any building that looks ADDED, REMOVED, MERGED, MOVED or reshaped (new tower, new storey, different roof shape) compared with BEFORE.
Give each item's bounding box in FULL-frame normalized coordinates [x0, y0, x1, y1] (0-1, origin top-left).
Answer with ONLY one JSON object, no other text:
For every anachronism ALWAYS give "nam_xuat_hien" = the earliest year such a thing existed (a number, your best estimate), never null.
{{"loi_thoi_dai": [{{"mo_ta": "<what>", "toa_do": [x0, y0, x1, y1], "nam_xuat_hien": <year>, "do_tin": <0-1>}}],
 "hinh_khoi": [{{"mo_ta": "<what changed>", "toa_do": [x0, y0, x1, y1], "do_tin": <0-1>}}]}}"""


def _ma(png, size=None):
    import cv2, numpy as np
    c = cv2.imread(png, cv2.IMREAD_COLOR)
    if c is None: raise FileNotFoundError(png)
    if size and (c.shape[1], c.shape[0]) != size: c = cv2.resize(c, size, interpolation=cv2.INTER_NEAREST)
    return (c[..., 2].astype(np.int64) << 16) | (c[..., 1].astype(np.int64) << 8) | c[..., 0]


def _grad(b, sig, mau=False):
    import cv2, numpy as np
    x = cv2.GaussianBlur(cv2.cvtColor(b, cv2.COLOR_BGR2LAB).astype(np.float32) * np.array([100 / 255, 1, 1], np.float32), (0, 0), sig)
    return np.sqrt(sum((cv2.Sobel(x[..., c], cv2.CV_32F, 1, 0, ksize=3) / 8) ** 2 + (cv2.Sobel(x[..., c], cv2.CV_32F, 0, 1, ksize=3) / 8) ** 2 for c in (range(3) if mau else (0,))))


def _bien(M):
    import numpy as np
    b = np.zeros(M.shape, bool)
    b[:-1] |= M[:-1] != M[1:]; b[1:] |= M[1:] != M[:-1]; b[:, :-1] |= M[:, :-1] != M[:, 1:]; b[:, 1:] |= M[:, 1:] != M[:, :-1]
    return b


def hinh_khoi(R, C, IID, nha, PID=None, BONG=None, p=None):
    """(a) → {id: dict(do, px, px_m, n_canh, sup0, sup, dx, dy, dich_m, iou, loi[])}"""
    import cv2, numpy as np
    p = dict(BMN, **(p or {})); H, W = IID.shape; s = H / 1080.0
    gR = _grad(R, p['SIG'] * s, True); gB = _grad(BONG, p['SIG'] * s) if BONG is not None else gR; gA = _grad(C, p['SIG'] * s, True)
    DT = cv2.distanceTransform((~(gA >= p['T_AI'])).astype(np.uint8), cv2.DIST_L2, 3)
    GE = (_bien(IID) | (_bien(PID) if PID is not None else False)) & (gR >= p['T_VIS']) & (gB >= p['T_VIS'])
    ys, xs = np.nonzero(GE); gid = IID[ys, xs]; o = np.argsort(gid, kind='stable'); gs = gid[o]
    ids, cnt = np.unique(IID.ravel(), return_counts=True); out = {}
    for h, a in zip(ids.tolist(), cnt.tolist()):
        if h == 0: continue
        ppm = float((nha.get(h) or {}).get('px_m') or 0)
        if a < p['A_MIN'] * s * s or ppm < p['PPM_MIN']: out[h] = dict(do=False, px=a, px_m=ppm); continue
        lo, hi = np.searchsorted(gs, h), np.searchsorted(gs, h, 'right'); yy, xx = ys[o[lo:hi]], xs[o[lo:hi]]
        if len(yy) < p['N_MIN'] * s: out[h] = dict(do=False, px=a, px_m=ppm, n_canh=int(len(yy)), ly_do=f"< {p['N_MIN']} điểm cạnh hình học thấy được"); continue
        S = int(np.ceil(p['S_M'] * ppm)) + 1; best = (-1.0, 0, 0); s0 = 0.0
        for dy in range(-S, S + 1):
            y2 = np.clip(yy + dy, 0, H - 1)
            for dx in range(-S, S + 1):
                v = float((DT[y2, np.clip(xx + dx, 0, W - 1)] <= p['R_DO'] * s).mean())
                if dx == 0 and dy == 0: s0 = v
                if v > best[0] + 1e-9 or (abs(v - best[0]) <= 1e-9 and dx * dx + dy * dy < best[1] ** 2 + best[2] ** 2): best = (v, dx, dy)
        v, dx, dy = best; dm = float(np.hypot(dx, dy)) / ppm
        m = IID == h; x0, y0, w_, h_ = cv2.boundingRect(m.astype(np.uint8)); sl = (slice(max(0, y0 - S), y0 + h_ + S), slice(max(0, x0 - S), x0 + w_ + S))
        ms = m[sl]; sh = np.roll(np.roll(ms, dy, 0), dx, 1); iou = float((ms & sh).sum() / max(1, (ms | sh).sum()))
        loi, cb = [], []
        if s0 < p['SUP_CHAN']: loi.append(f'đỡ cạnh hình học {s0:.2f} < {p["SUP_CHAN"]:g} — nhà mất/đổi khối rõ')
        elif s0 < p['SUP_MIN']: cb.append(f'đỡ cạnh hình học {s0:.2f} < {p["SUP_MIN"]:g} (nghi đổi mái/khối — người đọc)')
        if dm >= p['D_M'] and v - s0 >= p['G_MIN']: cb.append(f'nghi dời {dm:.1f} m ({dx:+d}, {dy:+d} px; IoU {iou:.2f}; đỡ {s0:.2f} → {v:.2f}) — người đọc')
        out[h] = dict(do=True, px=a, px_m=round(ppm, 3), n_canh=int(len(yy)), sup0=round(s0, 3), sup=round(v, 3), dx=dx, dy=dy, dich_m=round(dm, 2), iou=round(iou, 3), loi=loi, canh_bao=cb)
    return out


def quy_dao(Cs, Rs, IID, p=None):
    """(d) Cs, Rs: danh sách khung BGR (cùng cỡ mặt nạ) → dict(e_h{id: e}, nhap_ghep, nhap_render). Độ sáng tuyến tính (sRGB → Y) TB mỗi nhà."""
    import cv2, numpy as np
    p = dict(BMN, **(p or {}))
    def Y(f):
        x = f.astype(np.float32) / 255; x = np.where(x <= 0.04045, x / 12.92, ((x + 0.055) / 1.055) ** 2.4); return 0.0722 * x[..., 0] + 0.7152 * x[..., 1] + 0.2126 * x[..., 2]
    ids = [h for h in np.unique(IID) if h]; idx = np.searchsorted(ids, IID.ravel()); okm = IID.ravel() > 0
    def mean_h(f):
        y = Y(f).ravel(); return np.bincount(idx[okm], y[okm], len(ids)) / np.maximum(1, np.bincount(idx[okm], None, len(ids)))
    Lc = np.array([mean_h(f) for f in Cs]) + 1e-4; Lr = np.array([mean_h(f) for f in Rs]) + 1e-4
    e = np.abs(np.log(Lc / Lc[0]) - np.log(Lr / Lr[0])).max(0)
    M = cv2.erode((IID > 0).astype(np.uint8), np.ones((3, 3), np.uint8)) > 0
    # nhấp nháy BỀ MẶT: ε_t = ln Y(ghép_t) − ln Y(render_t) (mờ σ 1) — dựng lại ánh sáng đúng thì ε gần như không đổi theo t (tỉ số albedo);
    # AI khác nhau mỗi khung / nhiễu bề mặt làm ε nhảy. Đối chứng = cùng phép trên render với chính nó dời 1 khung KHÔNG có (ε ≡ 0) → dùng sàn tuyệt đối.
    eps = [cv2.GaussianBlur(np.log(Y(c) + 1e-3) - np.log(Y(r) + 1e-3), (0, 0), 1.0)[M] for c, r in zip(Cs, Rs)]
    nh = float(np.mean([np.abs(eps[i + 1] - eps[i]).mean() for i in range(len(eps) - 1)])) if len(eps) > 1 else 0.0
    return dict(e_h={int(h): round(float(v), 4) for h, v in zip(ids, e)}, nhap_be_mat=round(nh, 4))


def _p(base_, x): return x if not x or os.path.isabs(x) else os.path.normpath(os.path.join(base_, x))


def soi_bmn(truoc, sau, nam, noi='', t4=False, out=None, tag='bmn', api=False, cache=None):
    """(c) hai mô hình nhìn với lời nhắc BMN (cùng hạ tầng q_n2p_vision: GPT ghim + Claude ghim judge.MODEL; UA cố định; không email)"""
    import hashlib, shutil, tempfile, time
    from checks.ll import q_n2p_vision as QV
    k = hashlib.sha256(f'{QV.sha_file(truoc)}|{QV.sha_file(sau)}|{int(float(nam))}|{noi}|{bool(t4)}|{PROMPT_BMN_VER}|{QV.GPT}|{QV.CLAUDE}'.encode()).hexdigest()[:32]
    if cache is not None and k in cache: return dict(cache[k], khoa=k, tu_bo_dem=True)
    if not api: return dict(khoa=k, ket_qua={}, loi='chưa soi: không có trong bộ đệm và không chạy --vision')
    td = tempfile.mkdtemp(prefix='bmnv-')
    try:
        T = QV.tiles(truoc, td, 'before'); S = QV.tiles(sau, td, 'after')
        pr = PROMPT_BMN.format(noi=noi or 'the place', nam=int(float(nam)), truoc='\n'.join(f'- {x}' for x in T), sau='\n'.join(f'- {x}' for x in S),
                               cam='; '.join(QV.cam_list(nam, t4)))
        res, loi = {}, []
        for mh in ('gpt', 'claude'):
            if mh == 'gpt': txt, meta = QV.call_gpt(pr.replace(QV.GPT_LEAD, 'The images are attached in this order:'), T + S, f'{tag}-gpt', out)
            else:   # 1.17.6 (KN-3): không đọc đủ ảnh → tự gọi lại MỘT lần; cả hai lần vào n2p-cost.jsonl
                from checks.ll import q_k1176 as K76
                txt, meta = K76.goi_claude_du(QV, pr, td, T + S, f'{tag}-claude', out)
            j = QV.parse(txt) if not meta.get('loi') else None
            if not meta.get('loi') and j is None: meta['loi'] = 'trả lời không đọc được (không phải JSON)'
            if meta.get('loi'): loi.append(f"{mh}: {meta['loi']}")
            if out: os.makedirs(out, exist_ok=True); open(os.path.join(out, f'{tag}-{mh}.raw.txt'), 'w').write(txt or '')
            res[mh] = dict(meta=meta, json=j)
    finally: shutil.rmtree(td, ignore_errors=True)
    R = dict(khoa=k, ket_qua=res, prompt_ver=PROMPT_BMN_VER, loi='; '.join(loi) or None, chi_phi_usd=round(sum(float(v['meta'].get('usd') or 0) for v in res.values()), 4))
    if cache is not None and not R['loi']: cache[k] = {a: b for a, b in R.items() if a != 'khoa'}
    return R


def _r(loi=(), thieu=(), val='', **kw):
    loi, thieu = list(loi), list(thieu)
    return dict(ok=not loi and not thieu, ket_qua='THIẾU' if thieu and not loi else None, loi=loi, thieu=thieu, val=val, **kw)


def kiem_bmn(t, ep_dir='.', vision=False, cache=None, out=None, noi='', t4=False, p=None):
    """một tấm be_mat_nha_ai → dict(loi[], thieu[], canh_bao[], so) — chữ cái mục: (a) hình khối, (b) 0/255, (c) thời đại, (d) quỹ đạo/nhấp nháy, (e) khung 0 chiếu 3D"""
    import cv2, numpy as np
    from checks.ll import q_n2p as N
    p = dict(BMN, **(p or {})); tid = str(t.get('id') or t.get('ghep')); w = f'tấm {tid}'
    f = {k: _p(ep_dir, t.get(k)) for k in ('render', 'ghep', 'mat_na', 'mat_na_nha', 'mat_na_mat', 'bong', 'nha')}
    miss = [k for k in ('render', 'ghep', 'mat_na', 'mat_na_nha', 'bong', 'nha') if not f[k] or not os.path.exists(f[k])]
    if miss or t.get('nam') is None: return dict(loi=[], thieu=[f"(a) {w}: thiếu {', '.join(miss) or 'nam'} (be_mat_nha_ai cần render, ghep, mat_na, mat_na_nha, bong, nha, nam)"], canh_bao=[], so={})
    R, G, B = cv2.imread(f['render']), cv2.imread(f['ghep']), cv2.imread(f['bong']); H, W = R.shape[:2]
    if G.shape != R.shape or B.shape != R.shape: return dict(loi=[], thieu=[f'(a) {w}: ghep/bong khác cỡ render'], canh_bao=[], so={})
    L, names = N.idmap(f['mat_na'], (W, H), dict({'nha_thuong': NHA_THUONG}, **(t.get('bang') or {})))
    I = _ma(f['mat_na_nha'], (W, H)); I[L != names.index('nha_thuong')] = 0
    PID = _ma(f['mat_na_mat'], (W, H)) if f['mat_na_mat'] and os.path.exists(f['mat_na_mat']) else None
    if PID is not None: PID[I == 0] = 0
    nha = {int(x['id']): x for x in json.load(open(f['nha']))}
    HK = hinh_khoi(R, G, I, nha, PID, B, p); loi, thieu, cb = [], [], []
    do = {h: x for h, x in HK.items() if x.get('do')}
    for h, x in sorted(do.items()):
        loi += [f"(a) {w} nhà {h} (lô {nha.get(h, {}).get('lo')}, {x['px_m']} px/m): {e}" for e in x['loi']]
        cb += [f"(w) {w} nhà {h} (lô {nha.get(h, {}).get('lo')}, {x['px_m']} px/m): {e}" for e in x.get('canh_bao') or []]
    # 1.17.6 (KN-4): (w) cạnh màu mới trong lòng nhà đo được — ống khói/đầu hồi AI vẽ thêm mà (a) không bắt; CHỈ BÁO (người đọc soi các hộp)
    from checks.ll import q_k1176 as K76
    CMo = K76.canh_moi(R, G, B, I, set(do), nha)
    if CMo: cb.append(f"(w) {w}: {len(CMo)} cụm cạnh màu mới không có ở render/pass bóng (nghi ống khói/đầu hồi/chi tiết AI vẽ thêm — người đọc) — dài nhất: "
                      + ', '.join(f"{c['hop']} {c['m']} m" for c in CMo[:K76.CM['IN_TOP']]))
    lo_ = {}
    for h, x in do.items(): lo_.setdefault(nha.get(h, {}).get('lo'), [0, 0]); lo_[nha.get(h, {}).get('lo')][0] += 1; lo_[nha.get(h, {}).get('lo')][1] += int(not x['loi'])
    # (b) lớp khoá 0/255: mọi điểm KHÔNG thuộc nhà đo được (nở 1 px — viền ghép)
    Mdo = cv2.dilate(np.isin(I, list(do)).astype(np.uint8), np.ones((3, 3), np.uint8)) > 0
    khoa = ~Mdo
    if t.get('nen_ai'):   # tấm cũng là tấm nền N2+: lớp nền (trời, nước, đất, cây) theo N2P-1…5; khoá = lớp (a) còn lại + nhà không đo được
        khoa &= np.isin(L, [names.index(n_) for n_ in N.LOP_A if n_ in names]) | ((I > 0) & ~Mdo)
    d = np.abs(G.astype(np.int16) - R.astype(np.int16)).max(-1); mk = int(d[khoa].max()) if khoa.any() else 0
    if mk > 0:
        ys, xs = np.nonzero(khoa & (d > 0)); loi.append(f"(b) {w}: vùng khoá (lớp (a) còn lại, nhà không đo được{'' if t.get('nen_ai') else ', nước, bờ, nền'}) lệch tối đa {mk}/255 ở {len(ys)} điểm (hộp {[int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]})")
    # (c) thời đại vật liệu/chi tiết
    V = soi_bmn(f['render'], f['ghep'], t['nam'], t.get('noi', noi), t.get('t4', t4), out, tid, vision, cache)
    if V.get('loi'): thieu.append(f"(c) {w}: mô hình nhìn — {V['loi']}")
    for mh, rr in sorted((V.get('ket_qua') or {}).items()):
        j = rr.get('json') or {}
        for x in j.get('loi_thoi_dai') or []:
            if (x.get('do_tin') or 0) < 0.5: continue
            ny = x.get('nam_xuat_hien')
            if isinstance(ny, (int, float)) and ny > float(t['nam']): loi.append(f"(c) {w}: {mh} lỗi thời đại «{str(x.get('mo_ta'))[:70]}» năm {ny} @{x.get('toa_do')}")
            else: cb.append(f"(w) {w}: {mh} nghi vấn thời đại không năm «{str(x.get('mo_ta'))[:70]}» @{x.get('toa_do')} (người đọc)")
        cb += [f"(w) {w}: {mh} báo hình khối «{str(x.get('mo_ta'))[:70]}» @{x.get('toa_do')} (người đọc)" for x in j.get('hinh_khoi') or [] if (x.get('do_tin') or 0) >= 0.5]
    # (c) O2 q_thoi_dai trên ghép, trừ nghi vấn đã có ở render (như N2P-2 (b))
    if vision or (cache or {}).get('qtd', {}).get(tid):
        Q = (cache or {}).setdefault('qtd', {}).get(tid)
        if Q is None and vision:
            from checks.ll import q_thoi_dai as QT
            qc = (cache or {}).setdefault('o2', {}); od = os.path.join(out or '/var/tmp/bmn-qtd', 'qtd')
            Qg = QT.soi_khung(f['ghep'], t['nam'], od, f'{tid}-ghep', t.get('noi', noi), True, qc); Qr = QT.soi_khung(f['render'], t['nam'], od, f'{tid}-render', t.get('noi', noi), True, qc)
            Q = dict(moi=N.qtd_moi(Qg, Qr, W, H), loi='; '.join(x for x in (Qg.get('loi'), Qr.get('loi')) if x) or None, chi_phi_usd=round(float(Qg.get('cost_usd') or 0) + float(Qr.get('cost_usd') or 0), 4))
            if cache is not None and not Q['loi']: cache.setdefault('qtd', {})[tid] = Q
        if Q:
            if Q.get('loi'): thieu.append(f"(c) {w}: q_thoi_dai: {Q['loi']}")
            loi += [f"(c) {w}: q_thoi_dai nghi vấn mới (không có ở render): [{x.get('muc')}] {str(x.get('mo_ta'))[:70]} @px {x.get('toa_do_px')}" for x in Q.get('moi') or []]
    # (d)(e) timelapse — 1.17.6: (d) theo ĐIỂM ẢNH (KN-5), (e) ở ĐỘ PHÂN GIẢI VIDEO (KN-6); khung đọc ở cỡ gốc video (thu INTER_AREA nếu rộng hơn W/2)
    from checks.ll import q_k1176 as K76
    vd = t.get('be_mat_nha_video') or {}; so_d = {}
    if vd:
        gv, rv = _p(ep_dir, vd.get('ghep')), _p(ep_dir, vd.get('render')); cach = vd.get('cach')
        if cach not in ('anh_tinh', 'chieu_3d'): thieu.append(f"(e) {w}: be_mat_nha_video.cach phải là anh_tinh | chieu_3d")
        if not (gv and rv and os.path.exists(gv) and os.path.exists(rv)): thieu.append(f'(d) {w}: be_mat_nha_video thiếu ghep/render')
        else:
            Cs, (vw, vh) = K76.frames_video(gv, W // 2); Rs, rwh = K76.frames_video(rv, W // 2); n_ = min(len(Cs), len(Rs))
            if rwh != (vw, vh): thieu.append(f'(d) {w}: video ghép {vw}×{vh} khác cỡ video render {rwh[0]}×{rwh[1]}')
            else:
                I2 = cv2.resize(I.astype(np.int32), (vw, vh), interpolation=cv2.INTER_NEAREST); I2[~np.isin(I2, list(do))] = 0
                qp = K76.quy_dao_px(list(Cs[:n_]), list(Rs[:n_]), I2); e = np.array(list(qp['e_h'].values()) or [0.0])
                q = quy_dao(list(Cs[:n_]), list(Rs[:n_]), I2, p); e5 = np.array(list(q['e_h'].values()) or [0.0])   # thước 1.17.5 (TB nhà) — chỉ in
                pct = float((e > p['E_MAX']).mean() * 100) if len(qp['e_h']) else 0.0
                so_d = dict(khung=n_, co=f'{vw}×{vh}', nha=len(qp['e_h']), nha_nho_bo=len(qp['bo_nho']), e_tv=round(float(np.median(e)), 4), pct_lech=round(pct, 2),
                            pct_lech_1175=round(float((e5 > p['E_MAX']).mean() * 100), 2), nhap_be_mat=q['nhap_be_mat'],
                            lech=sorted(([h, v] for h, v in qp['e_h'].items() if v > p['E_MAX']), key=lambda z: -z[1])[:12])
                if pct > p['NHA_LECH_PCT']: loi.append(f"(d) {w}: {pct:.1f} % nhà có quỹ đạo sáng (trung vị theo điểm ảnh) lệch render > {p['E_MAX']:g} (ln) — bề mặt không theo ánh sáng (dán ảnh tĩnh khi nắng đổi?)")
                ysn = float(p.get('Y_SAN_NHAP') or 0.0)   # 1.17.7 (K1176-D6): sàn Y cho nhấp nháy theo tập (`be_mat_nha_y_san_nhap`; mặc định 0 = như 1.17.6)
                nh = K76.nhap_nhay_san(list(Cs[:n_]), list(Rs[:n_]), I2, ysn) if ysn > 0 else q['nhap_be_mat']
                if ysn > 0: so_d.update(nhap_be_mat_san=nh, y_san_nhap=ysn)
                if nh > p['NHAP_MAX']: loi.append(f"(d) {w}: nhấp nháy bề mặt {nh} > {p['NHAP_MAX']:g} (ln/khung)" + (f' (sàn Y {ysn:g}; không sàn {q["nhap_be_mat"]})' if ysn > 0 else ''))
                if cach == 'chieu_3d':
                    tp = _p(ep_dir, vd.get('tam'))
                    if not (tp and os.path.exists(tp)): thieu.append(f'(e) {w}: chieu_3d cần `tam` (tấm AI đã duyệt) để kiểm khung 0')
                    else:
                        C0 = K76.frames_video(gv, None, 1)[0][0]; I0 = cv2.resize(I.astype(np.int32), (C0.shape[1], C0.shape[0]), interpolation=cv2.INTER_NEAREST); I0[~np.isin(I0, list(do))] = 0
                        de_tb, de_95 = K76.khung0_de(C0, cv2.imread(tp), I0)
                        so_d.update(t0_co=f'{C0.shape[1]}×{C0.shape[0]}', t0_dE_tb=round(de_tb, 2), t0_dE_p95=round(de_95, 2))
                        if de_tb > p['T0_DE'] or de_95 > p['T0_P95']: loi.append(f"(e) {w}: khung 0 chiếu 3D lệch tấm đã duyệt (so ở {C0.shape[1]}×{C0.shape[0]} — độ phân giải video) ΔE TB {de_tb:.1f} / p95 {de_95:.1f} (trần {p['T0_DE']:g} / {p['T0_P95']:g}) — ánh sáng chồng 2 lần?")
    elif t.get('cu_may_dong') or t.get('timelapse'): thieu.append(f'(d) {w}: shot timelapse nhưng chưa khai be_mat_nha_video')
    so = dict(nha=len(HK), nha_do=len(do), nha_loi=sum(1 for x in do.values() if x['loi']), lo=len(lo_), b_max=mk, video=so_d, mo_hinh=V.get('chi_phi_usd'),
              canh_moi=len(CMo), canh_moi_m=round(sum(c['m'] for c in CMo), 1))
    return dict(loi=loi, thieu=thieu, canh_bao=cb, so=so, lo=lo_)


def be_mat_nha(E, ep_dir='.', vision=False, out=None):
    """hàng BE-MAT-NHA (tập từ T4) — chỉ tấm n2p.tam khai `be_mat_nha_ai: true`"""
    if not ap_1175(E): return dict(ok=True, ket_qua='KHÔNG ÁP', loi=[], val='tập trước T4 — không hồi tố')
    N2 = E.get('n2p') or {}; tam = [t for t in N2.get('tam') or [] if t.get('be_mat_nha_ai')]
    if not tam: return dict(ok=True, ket_qua='KHÔNG ÁP', loi=[], val='không tấm nào khai be_mat_nha_ai: true')
    out = out or E.get('out'); cp = os.path.join(out, 'bmn-vision-cache.json') if out else None
    cache = json.load(open(cp)) if cp and os.path.exists(cp) else {}
    loi, thieu, cb, vals = [], [], [], []
    from checks.ll import q_k1176 as K76
    ppm, lk = K76.ppm_min(E)   # 1.17.6 (15:25): ngưỡng nhà đo được theo tập (`be_mat_nha_px_m_min`, mặc định 2; T4 khai 4)
    if lk: cb.append(f'(w) {lk}')
    for t in tam:
        try: k = kiem_bmn(t, ep_dir, vision, cache, out, N2.get('noi', ''), bool(N2.get('t4')), dict(PPM_MIN=ppm, Y_SAN_NHAP=K76.y_san_nhap(E)))
        except Exception as e: thieu.append(f"(a) tấm {t.get('id')}: {type(e).__name__}: {e}"); continue   # noqa: BLE001
        loi += k['loi']; thieu += k['thieu']; cb += k['canh_bao']; s = k['so']
        vals.append(f"{t.get('id')}: {s.get('nha_do', 0)}/{s.get('nha', 0)} nhà đo được, {s.get('nha_loi', 0)} lỗi, (b) {s.get('b_max', '—')}/255" + (f", video e TV {s['video'].get('e_tv')}" if s.get('video') else ''))
    if cp and vision: os.makedirs(out, exist_ok=True); json.dump(cache, open(cp, 'w'), ensure_ascii=False, indent=1)
    cong = 'animatic' if E.get('animatic') else 'G2'
    loi += cb   # (w) luôn Cảnh báo (cap112)
    return dict(_r(loi, thieu, val=f"{len(tam)} tấm · nhà đo được ≥ {ppm:g} px/m · " + ' · '.join(vals[:4])), cong=cong, px_m_min=ppm, muc={c: [x for x in loi + thieu if x.startswith(f'({c})')] for c in 'abcdew'})
