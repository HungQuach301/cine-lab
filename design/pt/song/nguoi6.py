"""V6 · NGƯỜI TỰ DỰNG cho khung neo (thay lưới MPFB: kho GitHub makehumancommunity/mpfb2 bị chính sách proxy chặn trong phiên V6 — xem báo cáo).
Thuần numpy (dùng được trong bpy): thân, đầu, tay, quần áo = TRƯỜNG KHOẢNG CÁCH CÓ DẤU (SDF) ghép mềm từ elip / nón tròn theo số đo nhân trắc
(cao ≈ 7,5 đầu, vai ≈ 2 đầu, tay buông tới giữa đùi) → lưới bằng marching cubes (scikit-image, cài ngoài git ở /var/tmp/v6kn/pylib313).
QUẦN ÁO = LƯỚI RIÊNG CÓ ĐỘ DÀY: vỏ giữa hai mặt lệch (t_in, t_out) của thân, cắt theo vùng (gấu, vạt, ống) — mép cắt lộ bề dày vải;
NẾP theo khớp (khuỷu, gối, eo, nách, háng: gợn quanh trục xương, xoắn nhẹ) + nhiễu vải thô. Mũ = MỘT lưới liền có bề dày (tricorn: vành tròn
bẻ lên 3 phía thành tam giác; Brodie: chỏm nông + vành rộng; mũ calô; mũ lính thuỷ; mũ vải lưỡi trai).
Không dùng tài sản bên thứ ba: mọi hình là mã của Cine Lab. Trang phục là VẬT MANG DỮ KIỆN — nguồn ghi ở ROLE_SRC."""
import math
import numpy as np

# ---------------------------------------------------------------- SDF cơ bản
def _len(v): return np.sqrt(np.einsum('...i,...i->...', v, v))
def V(*a): return np.array(a, dtype=np.float32)

def sd_ell(P, c, r):
    r = np.asarray(r, np.float32); q = (P - c) / r; k0 = _len(q); k1 = _len((P - c) / (r * r))
    return k0 * (k0 - 1.0) / np.maximum(k1, 1e-9)

def sd_cone(P, a, b, ra, rb):
    """nón tròn đầu bo (gần đúng): khoảng cách tới đoạn ab trừ bán kính nội suy."""
    a = np.asarray(a, np.float32); b = np.asarray(b, np.float32); ab = b - a; L2 = float(ab @ ab)
    t = np.clip(((P - a) @ ab) / L2, 0.0, 1.0)
    return _len(P - (a + t[..., None] * ab)) - (ra + (rb - ra) * t)

def sd_box(P, c, h, R=None):
    q = P - c
    if R is not None: q = q @ R
    d = np.abs(q) - h
    return _len(np.maximum(d, 0.0)) + np.minimum(d.max(-1), 0.0)

def smin(a, b, k):
    h = np.clip(0.5 + 0.5 * (b - a) / k, 0.0, 1.0); return b * (1 - h) + a * h - k * h * (1 - h)
def smax(a, b, k): return -smin(-a, -b, k)

def _hash(ix, iy, iz, seed):
    h = np.sin(ix * 127.1 + iy * 311.7 + iz * 74.7 + seed * 19.19) * 43758.5453
    return h - np.floor(h)
def vnoise(P, scale, seed=0.0):
    g = P / scale; i = np.floor(g); f = g - i; f = f * f * (3 - 2 * f)
    ix, iy, iz = i[..., 0], i[..., 1], i[..., 2]; fx, fy, fz = f[..., 0], f[..., 1], f[..., 2]
    out = 0.0
    for dx in (0, 1):
        for dy in (0, 1):
            for dz in (0, 1):
                w = (fx if dx else 1 - fx) * (fy if dy else 1 - fy) * (fz if dz else 1 - fz)
                out = out + w * _hash(ix + dx, iy + dy, iz + dz, seed)
    return out * 2 - 1

# ---------------------------------------------------------------- thân theo dáng
ARM_ABD = math.radians(30.0)    # tư thế DỰNG: tay giạng 30° (tách khỏi thân cho marching cubes); tư thế diễn đưa tay buông sát thân

class Body:
    """nhìn −Y, +X = bên TRÁI người, Z lên; gốc = giữa hai bàn chân trên mặt đất."""
    def __init__(s, sex='m', H=1.72, sw=1.0, g=1.0, belly=0.0, seed=0):
        s.sex, s.H, s.sw, s.g, s.belly, s.seed = sex, H, sw, g, belly, seed
        fem = sex == 'f'; k = H / (1.63 if fem else 1.75); s.k = k
        Z = lambda z: z * k
        s.z = dict(ankle=Z(0.085), knee=Z(0.50), hip=Z(0.905), pelvis=Z(0.955), waist=Z(1.065 if not fem else 1.075), chest=Z(1.265), sh=Z(1.445), neck=Z(1.49),
                   chin=Z(1.535), headc=Z(1.648), top=Z(1.752))
        s.hipx = (0.088 if not fem else 0.094) * g ** 0.5
        s.shx = (0.186 if not fem else 0.165) * sw
        s.head_k = 1.0 if not fem else 0.96            # đầu gần như cố định giữa các dáng → dáng cao có đầu nhỏ tương đối (tỉ lệ thật)
        hz = s.z; J = s.J = {}
        J['root'] = V(0, 0.0, hz['pelvis']); J['spine'] = V(0, 0.0, hz['waist']); J['chest'] = V(0, 0.005, hz['chest']); J['neck'] = V(0, 0.005, hz['neck'] - 0.01)
        J['head'] = V(0, 0.0, hz['chin'] + 0.01); J['head_t'] = V(0, 0.0, hz['top'])
        for sd, sg in (('L', 1), ('R', -1)):
            J['hip' + sd] = V(sg * s.hipx, 0.0, hz['hip']); J['knee' + sd] = V(sg * (s.hipx - 0.004), -0.006, hz['knee'])
            J['ankle' + sd] = V(sg * (s.hipx - 0.006), 0.012, hz['ankle']); J['toe' + sd] = V(sg * (s.hipx + 0.004), -0.155 * k, 0.02)
            S = V(sg * s.shx, 0.0, hz['sh'] - 0.012); d = V(sg * math.sin(ARM_ABD), 0.0, -math.cos(ARM_ABD))
            ua, fa, hd = 0.300 * k, 0.255 * k, 0.185 * k
            J['clav' + sd] = V(sg * 0.025, 0.0, hz['sh'] - 0.005); J['sh' + sd] = S; J['elbow' + sd] = S + d * ua; J['wrist' + sd] = S + d * (ua + fa); J['hand_t' + sd] = S + d * (ua + fa + hd)
            J['armdir' + sd] = d
        s.ua_fa = 0.300 * k + 0.255 * k
        s.r = dict(thigh=0.088 * g, knee=0.051 * g ** 0.5, calf=0.056 * g, ankle=0.034, uarm=0.050 * g, elbow=0.037 * g ** 0.5, farm=0.042 * g, wrist=0.029)
        if fem: s.r.update(thigh=0.092 * g, uarm=0.045 * g, farm=0.037 * g, calf=0.054 * g)

    def core(s, P, with_head=False):
        """thân + cổ + chân (một lưới); đầu dựng riêng ở lưới mịn hơn (head)."""
        z, g, J, r = s.z, s.g, s.J, s.r; fem = s.sex == 'f'; k = s.k; b = s.belly
        d = sd_ell(P, V(0, 0.005, z['pelvis']), ((0.165 if not fem else 0.185) * g, 0.108 * g, 0.115 * k))
        for sg in (1, -1): d = smin(d, sd_ell(P, V(sg * 0.068, 0.055 * g, z['hip'] - 0.005), (0.08 * g, 0.072 * g, 0.092 * k)), 0.035)        # mông
        d = smin(d, sd_ell(P, V(0, -0.004 - b, z['waist']), ((0.138 if not fem else 0.128) * g + b * 0.5, 0.098 * g + b, 0.13 * k)), 0.05)    # bụng/eo
        cw = (0.168 if not fem else 0.15) * g * (0.75 + 0.25 * s.sw)
        d = smin(d, sd_ell(P, V(0, 0.008, z['chest']), (cw, 0.112 * g, 0.172 * k)), 0.06)                                                  # lồng ngực
        for sg in (1, -1):
            if fem: d = smin(d, sd_ell(P, V(sg * 0.062, -0.07 * g, z['chest'] + 0.005), (0.062, 0.05, 0.055)), 0.03)
            else: d = smin(d, sd_ell(P, V(sg * 0.068, -0.068 * g, z['chest'] + 0.04), (0.072 * g, 0.038 * g, 0.058)), 0.035)          # ngực
            d = smin(d, sd_cone(P, V(sg * 0.03, 0.025, z['sh'] + 0.035), V(sg * (s.shx - 0.03), 0.01, z['sh'] - 0.005), 0.05 * g, 0.052 * g), 0.05)   # cơ thang/cầu vai
            d = smin(d, sd_ell(P, V(sg * 0.075, 0.07 * g, z['chest'] + 0.07), (0.07 * g, 0.045, 0.1)), 0.04)                          # bả vai
        d = smin(d, sd_cone(P, V(0, 0.012, z['sh'] - 0.02), V(0, 0.004, z['chin'] + 0.035), 0.056 * g ** 0.5, 0.05), 0.03)            # cổ
        for sd, sg in (('L', 1), ('R', -1)):
            hip, kn, an, toe = J['hip' + sd], J['knee' + sd], J['ankle' + sd], J['toe' + sd]
            leg = sd_cone(P, hip + V(0, 0.004, 0.02), kn, r['thigh'], r['knee'])
            leg = smin(leg, sd_ell(P, hip * 0.45 + kn * 0.55 + V(sg * 0.006, -0.03 * g, 0.0), (0.062 * g, 0.066 * g, 0.15 * k)), 0.04)       # cơ đùi trước
            leg = smin(leg, sd_ell(P, kn + V(0, -0.012, 0.0), (0.048, 0.046, 0.05)), 0.02)                                          # gối
            leg = smin(leg, sd_cone(P, kn, an, r['knee'] * 0.95, r['ankle']), 0.025)
            leg = smin(leg, sd_ell(P, kn * 0.62 + an * 0.38 + V(sg * 0.004, 0.028, 0.0), (0.05 * g, 0.054 * g, 0.115 * k)), 0.035)    # bắp chân
            heel = V(an[0], 0.035, 0.035); leg = smin(leg, sd_cone(P, heel, toe + V(0, 0, 0.004), 0.033, 0.026), 0.03)                # bàn chân
            leg = smin(leg, sd_ell(P, (heel + toe) / 2 + V(0, 0, 0.012), (0.042, 0.1 * k, 0.03)), 0.02)
            d = smin(d, leg, 0.045)
        if with_head: d = smin(d, s.head(P), 0.025)
        return d

    def head(s, P, features=True):
        z = s.z; hk = s.head_k; c = z['headc']; fem = s.sex == 'f'
        Ph = (P - V(0, 0, c)) / hk + V(0, 0, c)
        d = sd_ell(Ph, V(0, 0.014, c + 0.012), (0.077, 0.098, 0.104))                                                          # hộp sọ
        d = smin(d, sd_ell(Ph, V(0, -0.038, c - 0.03), (0.064 if not fem else 0.06, 0.07, 0.088)), 0.03)                       # mặt
        for sg in (1, -1):
            d = smin(d, sd_cone(Ph, V(sg * 0.05, -0.02, c - 0.055), V(sg * 0.02, -0.07, c - 0.1), 0.026 if not fem else 0.022, 0.022), 0.025)   # hàm
            d = smin(d, sd_ell(Ph, V(sg * 0.047, -0.07, c - 0.018), (0.024, 0.02, 0.018)), 0.015)                               # gò má
            d = smin(d, sd_ell(Ph, V(sg * 0.078, 0.008, c - 0.012), (0.012, 0.028, 0.034)), 0.008)                              # tai
        d = smin(d, sd_ell(Ph, V(0, -0.083, c - 0.108), (0.024, 0.02, 0.02)), 0.02)                                              # cằm
        d = smin(d, sd_cone(Ph, V(0, 0.012, c - 0.12), V(0, 0.006, c - 0.2), 0.05, 0.054), 0.03)                                # nối cổ
        if features:
            d = smin(d, sd_cone(Ph, V(-0.038, -0.088, c + 0.022), V(0.038, -0.088, c + 0.022), 0.014, 0.014), 0.012)                  # cung mày
            d = smin(d, sd_cone(Ph, V(0, -0.094, c + 0.012), V(0, -0.113, c - 0.03), 0.009, 0.013), 0.01)                             # sống mũi
            d = smin(d, sd_ell(Ph, V(0, -0.108, c - 0.036), (0.017, 0.013, 0.011)), 0.008)                                            # cánh mũi
            d = smin(d, sd_cone(Ph, V(-0.019, -0.094, c - 0.064), V(0.019, -0.094, c - 0.064), 0.0085, 0.0085), 0.008)                # môi
            for sg in (1, -1): d = smax(d, -sd_ell(Ph, V(sg * 0.033, -0.1, c + 0.002), (0.019, 0.016, 0.014)), 0.008)                 # hốc mắt
            d = smax(d, -sd_cone(Ph, V(-0.016, -0.106, c - 0.068), V(0.016, -0.106, c - 0.068), 0.0025, 0.0025), 0.004)               # khe miệng
        return d * hk

    def eyes(s):
        c = s.z['headc']; hk = s.head_k
        return [V(sg * 0.033 * hk, -0.088 * hk, c + 0.002 * hk) for sg in (1, -1)], 0.0115 * hk

    def arm(s, P, sd):
        J, r, g = s.J, s.r, s.g; S, E, W, dv = J['sh' + sd], J['elbow' + sd], J['wrist' + sd], J['armdir' + sd]
        sg = 1 if sd == 'L' else -1
        d = sd_ell(P, S + V(sg * 0.012, 0.0, 0.0), (0.058 * g, 0.064 * g, 0.072 * g))                       # cơ delta
        d = smin(d, sd_cone(P, S, E, r['uarm'], r['elbow']), 0.03)
        d = smin(d, sd_ell(P, S * 0.45 + E * 0.55 + V(0, -0.012, 0), (0.042 * g, 0.045 * g, 0.075)), 0.03)   # bắp tay
        d = smin(d, sd_cone(P, E, W, r['farm'], r['wrist']), 0.02)
        d = smin(d, sd_ell(P, E * 0.7 + W * 0.3, (0.045 * g, 0.044 * g, 0.07)), 0.03)
        n = np.cross(dv, V(0, 1, 0)); n = (n / np.linalg.norm(n)).astype(np.float32)          # pháp tuyến lòng bàn tay (quay vào thân)
        Rm = np.stack([n, V(0, 1, 0), dv], 1).astype(np.float32)
        d = smin(d, sd_box(P, W + dv * 0.045, V(0.011, 0.034, 0.042), Rm) - 0.009, 0.015)                              # lòng bàn tay
        d = smin(d, sd_box(P, W + dv * 0.115 + n * (-sg * 0.006), V(0.008, 0.031, 0.04), Rm) - 0.007, 0.012)          # ngón khum
        d = smin(d, sd_cone(P, W + dv * 0.02 + V(0, -0.028, 0), W + dv * 0.075 + V(0, -0.04, 0) + n * (-sg * 0.012), 0.011, 0.009), 0.01)   # ngón cái
        return d

    def bones(s):
        """xương: (tên, đầu, đuôi, cha)."""
        J = s.J; z = s.z
        B = [('root', J['root'], J['spine'], None), ('spine', J['spine'], J['chest'], 'root'), ('chest', J['chest'], V(0, 0.005, z['sh'] - 0.01), 'spine'),
             ('neck', J['neck'], J['head'], 'chest'), ('head', J['head'], J['head_t'], 'neck')]
        for sd in ('L', 'R'):
            B += [('clav' + sd, J['clav' + sd], J['sh' + sd], 'chest'), ('uarm' + sd, J['sh' + sd], J['elbow' + sd], 'clav' + sd),
                  ('farm' + sd, J['elbow' + sd], J['wrist' + sd], 'uarm' + sd), ('hand' + sd, J['wrist' + sd], J['hand_t' + sd], 'farm' + sd),
                  ('thigh' + sd, J['hip' + sd], J['knee' + sd], 'root'), ('shin' + sd, J['knee' + sd], J['ankle' + sd], 'thigh' + sd),
                  ('foot' + sd, J['ankle' + sd], J['toe' + sd], 'shin' + sd)]
        return B

BONESET = {'core': ['root', 'spine', 'chest', 'neck', 'thighL', 'shinL', 'footL', 'thighR', 'shinR', 'footR'],
           'torso': ['root', 'spine', 'chest', 'neck'], 'head': ['head'],
           'armL': ['clavL', 'uarmL', 'farmL', 'handL'], 'armR': ['clavR', 'uarmR', 'farmR', 'handR'],
           'legs': ['root', 'thighL', 'shinL', 'footL', 'thighR', 'shinR', 'footR']}

def seg_dist(P, a, b):
    ab = b - a; t = np.clip(((P - a) @ ab) / float(ab @ ab), 0, 1); return _len(P - (a + t[:, None] * ab)), t

def skin_weights(Pv, body, names, sharp=0.018, rootmix=0.0):
    """trọng số da: w_i ∝ exp(−(d_i − d_min)/sharp), d_i = khoảng cách tới đoạn xương; giữ 3 lớn nhất; rootmix pha xương root (vạt áo, váy)."""
    bd = {n: (h, t) for n, h, t, _ in body.bones()}
    D = np.stack([seg_dist(Pv, *bd[n])[0] for n in names], 1)
    W = np.exp(-(D - D.min(1, keepdims=True)) / sharp)
    if len(names) > 3:
        idx = np.argsort(-W, 1)[:, 3:]; np.put_along_axis(W, idx, 0.0, 1)
    W /= W.sum(1, keepdims=True)
    if rootmix and 'root' in names:
        W = W * (1 - rootmix); W[:, names.index('root')] += rootmix
    return W

# ---------------------------------------------------------------- nếp vải theo khớp
def folds(P, body, parts, amp=0.0026, seed=0.0):
    """gợn vải quanh trục xương gần khớp: A·env(s)·sin(2πs/λ + φ(θ)) — xoắn nhẹ theo góc quanh trục; + nhiễu vải thô (2 tầng)."""
    J = body.J; f = np.zeros(P.shape[:-1], np.float32)
    def ring(Jp, axis, lam, width, a, rad):
        ax = (axis / np.linalg.norm(axis)).astype(np.float32); q = P - Jp; s_ = q @ ax; rr = _len(q - s_[..., None] * ax)
        u = np.cross(ax, V(0, 0, 1) if abs(ax[2]) < 0.9 else V(1, 0, 0)); u = (u / np.linalg.norm(u)).astype(np.float32); w = np.cross(ax, u)
        th = np.arctan2(q @ w, q @ u)
        return a * np.exp(-(s_ / width) ** 2) * (rr < rad) * np.sin(2 * math.pi * s_ / lam + 1.6 * np.sin(2 * th + seed) + seed)
    for p in parts:
        if p == 'elbows':
            for sd in 'LR': f += ring(J['elbow' + sd], J['wrist' + sd] - J['sh' + sd], 0.034, 0.07, amp * 1.2, 0.09)
        if p == 'wrists':
            for sd in 'LR': f += ring(J['wrist' + sd] - J['armdir' + sd] * 0.04, J['armdir' + sd], 0.028, 0.04, amp, 0.07)
        if p == 'knees':
            for sd in 'LR': f += ring(J['knee' + sd], J['ankle' + sd] - J['hip' + sd], 0.04, 0.08, amp * 1.3, 0.12)
        if p == 'ankles':
            for sd in 'LR': f += ring(J['ankle' + sd] + V(0, 0, 0.07), V(0, 0, 1), 0.035, 0.05, amp * 1.4, 0.11)
        if p == 'crotch':
            for sd in 'LR': f += ring(J['hip' + sd] - V(0, 0, 0.09), J['knee' + sd] - J['hip' + sd], 0.05, 0.08, amp, 0.13)
        if p == 'waist': f += ring(V(0, 0, body.z['waist'] - 0.04), V(0, 0, 1), 0.045, 0.06, amp, 0.3)
        if p == 'armpit':
            for sd in 'LR': f += ring(J['sh' + sd] + J['armdir' + sd] * 0.07, J['armdir' + sd], 0.04, 0.05, amp * 0.8, 0.09)
    f += 0.0012 * vnoise(P, 0.06, seed) + 0.0006 * vnoise(P, 0.021, seed + 3)
    return f

# ---------------------------------------------------------------- MŨ (một lưới liền; toạ độ quanh tâm vành, z lên, −Y trước)
def hat_tricorn(rc=0.094, rb=0.172, crown=0.088, lace=True):
    """vành tròn (lưới cực 10 × 96) BẺ LÊN 3 PHÍA: tam giác có 3 đỉnh (trước, sau-trái, sau-phải) ở bán kính R_t; phần vành ngoài mỗi cạnh tam giác
    quay quanh cạnh đó 78° (áp vào chóp) → góc nhọn ở 3 đỉnh; chóp tròn thấp; MỘT lưới liền, bề dày bằng Solidify. Cờ 'vien' = viền ren trắng."""
    NR, NT = 10, 96; verts = []; faces = []; lace_f = []
    Rt = rb * 1.06; corners = [math.radians(a) for a in (-90, 30, 150)]
    edges = []
    for i in range(3):
        a0, a1 = corners[i], corners[(i + 1) % 3]; p0 = np.array([math.cos(a0), math.sin(a0)]) * Rt; p1 = np.array([math.cos(a1), math.sin(a1)]) * Rt
        t = p1 - p0; n = np.array([t[1], -t[0]]); n /= np.linalg.norm(n)
        if n @ ((p0 + p1) / 2) < 0: n = -n
        edges.append((n, float(n @ p0)))
    for i in range(NR + 1):
        r = rc + (rb - rc) * i / NR
        for j in range(NT):
            a = 2 * math.pi * j / NT; p = np.array([math.cos(a), math.sin(a)]) * r
            n, e0 = max(edges, key=lambda e: e[0] @ p - e[1]); e = n @ p - e0; zz = 0.0
            if e > 0:
                fold = math.radians(78); base = p - n * e; p = base + n * e * math.cos(fold); zz = e * math.sin(fold)
            verts.append((p[0], p[1], zz))
    for i in range(NR):
        for j in range(NT):
            a = i * NT + j; b = i * NT + (j + 1) % NT; c = (i + 1) * NT + (j + 1) % NT; d = (i + 1) * NT + j
            faces.append((a, b, c, d)); lace_f.append(lace and i >= NR - 1)
    base = len(verts); NC = 6
    for k in range(1, NC + 1):
        ph = (math.pi / 2) * k / NC; rr = rc * math.cos(ph); zz = crown * math.sin(ph) ** 0.8
        for j in range(NT):
            a = 2 * math.pi * j / NT; verts.append((math.cos(a) * rr, math.sin(a) * rr * 1.1, zz))
    for k in range(NC):
        for j in range(NT):
            if k == 0: a = j; b = (j + 1) % NT
            else: a = base + (k - 1) * NT + j; b = base + (k - 1) * NT + (j + 1) % NT
            c = base + k * NT + (j + 1) % NT; d = base + k * NT + j
            faces.append((d, c, b, a)); lace_f.append(False)
    return np.array(verts, np.float32), faces, lace_f

def hat_revolve(profile, NT=64, sx=1.0, sy=1.08):
    verts = []; faces = []
    for (r, z) in profile:
        for j in range(NT):
            a = 2 * math.pi * j / NT; verts.append((math.cos(a) * r * sx, math.sin(a) * r * sy, z))
    for i in range(len(profile) - 1):
        for j in range(NT):
            a = i * NT + j; b = i * NT + (j + 1) % NT; c = (i + 1) * NT + (j + 1) % NT; d = (i + 1) * NT + j; faces.append((a, b, c, d))
    return np.array(verts, np.float32), faces

BRODIE = [(0.166, -0.006), (0.163, -0.001), (0.150, 0.004), (0.132, 0.008), (0.116, 0.012), (0.112, 0.022), (0.106, 0.042), (0.094, 0.06), (0.074, 0.074),
          (0.046, 0.083), (0.0, 0.087)]                     # Mk II: vành rộng hơi rủ + chỏm nông
ROUND1782 = [(0.162, 0.0), (0.12, 0.003), (0.096, 0.005), (0.095, 0.05), (0.09, 0.085), (0.06, 0.095), (0.0, 0.097)]
SAILOR = [(0.097, -0.02), (0.099, 0.02), (0.112, 0.035), (0.134, 0.046), (0.136, 0.052), (0.12, 0.056), (0.0, 0.058)]
FLATCAP = [(0.098, -0.012), (0.103, 0.018), (0.118, 0.033), (0.112, 0.044), (0.0, 0.05)]
MOBCAP = [(0.1, -0.04), (0.108, 0.008), (0.1, 0.05), (0.07, 0.08), (0.0, 0.09)]

def hat_sidecap(L=0.25, W=0.105, Hh=0.075):
    """mũ calô (Field Service / RAF side cap): thân thuyền — hai má vải dốc gặp nhau ở sống trên, mép dưới hơi cong."""
    NU = 24; verts = []; faces = []
    for i in range(NU + 1):
        u = i / NU; y = (u - 0.5) * L; prof = max(0.08, math.sin(math.pi * u)) ** 0.35
        zb = 0.012 * math.cos(2 * math.pi * (u - 0.5)); zt = Hh * (0.75 + 0.25 * prof)
        for (x, z) in ((-W / 2 * prof, zb), (-0.006 * prof, zt), (0.006 * prof, zt), (W / 2 * prof, zb)):
            verts.append((x, y, z))
    for i in range(NU):
        for k in range(3):
            a = i * 4 + k; faces.append((a, a + 1, a + 5, a + 4))
    return np.array(verts, np.float32), faces

def visor(r0=0.095, r1=0.152, a0=-150, a1=-30, NT=16, drop=0.012):
    """lưỡi trai (mũ vải 1943): nửa vành phía trước, hơi chúc."""
    verts = []; faces = []
    for i, r in enumerate((r0, r1)):
        for j in range(NT + 1):
            a = math.radians(a0 + (a1 - a0) * j / NT); verts.append((math.cos(a) * r, math.sin(a) * r * 1.05, -drop * i))
    for j in range(NT): faces.append((j, j + 1, NT + 2 + j, NT + 1 + j))
    return np.array(verts, np.float32), faces

# ---------------------------------------------------------------- VAI + trang phục (vật mang dữ kiện; nguồn ở ROLE_SRC)
C = lambda *c: tuple(c)
ROLE_SRC = {
    1782: {'_chung': 'Quân phục đồn trú Gibraltar 1782 — đối chiếu tranh PD trong TIEN-KY T3 (channel-k2/k2c-t3-01/TIEN-KY-VAY-HAM.md): phác thảo J. S. Copley '
                     'cho "The Siege of Gibraltar" (Met 60.44.17 "Three Officers…", Cleveland 1950.215), bản khắc W. Sharp theo Copley (LoC 96510788), '
                     'J. Trumbull "The Sortie…" (Met 12828). Kiểu áo lính 1768–1784 (áo đỏ có ve áo màu nẹp, vạt sau bẻ ngược lộ lót trắng, đai chéo trắng, '
                     'quần chẽn trắng, ghệt đen, mũ ba góc viền ren trắng) theo Royal Clothing Warrant 1768 — chưa trích nguyên văn trong TIEN-KY → "approx."; '
                     'màu nẹp theo trung đoàn = illustrative.',
           'linh': 'bộ binh, súng hoả mai vác vai trái (approx.)', 'linh2': 'bộ binh làm việc (không đai chéo, không súng) — approx.',
           'phao_binh': 'Royal Artillery: áo lam đậm nẹp đỏ — approx.', 'thuy_thu': 'thuỷ thủ: áo ngắn lam, quần ống rộng, mũ tròn thấp — illustrative',
           'dan_nam': 'dân nam: áo dài nâu, gi-lê, quần chẽn, tất xám, mũ ba góc đen không ren — illustrative (S062: phần lớn dân đã rời phố)',
           'dan_nu': 'dân nữ: váy, tạp dề, khăn choàng, mũ vải trắng — illustrative; tỉ lệ thấp (S062)'},
    1943: {'_chung': 'Quân phục Anh 1939–45: battledress serge (mẫu 1937), khaki drill vùng Địa Trung Hải, mũ sắt Mk II "Brodie", mũ calô Field Service, '
                     'đồ lính thuỷ RN (áo chui cổ vuông, quần ống loe, mũ trắng hè), RAF xanh xám — đối chiếu ảnh tra cứu Commons/IWM "The British Army on '
                     'Gibraltar 1941/1942" (chỉ tra cứu, reports/pt4/nguon/KET-QUA.md) → "approx."; 1943 KHÔNG phụ nữ/trẻ em (sơ tán 1940, S114).',
           'linh': 'bộ binh battledress + dây đeo 1937 + mũ Brodie, súng trường đeo vai — approx.', 'linh2': 'khaki drill (sơ mi xắn tay + quần dài) + mũ calô — approx.',
           'thuy_thu': 'thuỷ thủ RN đồ lam — approx.', 'thuy_thu_trang': 'thuỷ thủ RN đồ trắng hè — approx.', 'raf': 'RAF battledress xanh xám + mũ calô — approx.',
           'tho': 'thợ dân sự nam (illustrative): quần sẫm, sơ mi xắn tay, gi-lê, mũ vải lưỡi trai'},
}

def roles(ep):
    if ep == 1782:
        RED = C(0.2, 0.018, 0.014); WHT = C(0.62, 0.6, 0.55); BLK = C(0.035, 0.032, 0.03)
        inf = dict(sex='m', coat=RED, lining=WHT, waistcoat=WHT, breeches=WHT, gaiters=BLK, shoes=BLK, stock=BLK, hat='tricorn', hatcol=BLK, lace=WHT,
                   belts=WHT, facings=[C(0.62, 0.48, 0.1), C(0.2, 0.32, 0.16), C(0.04, 0.04, 0.04)], hair='queue', skirts=True)
        return {
            'linh': dict(inf, gun='musket', work='order', carry=None),
            'linh2': dict(inf, coat=C(0.18, 0.02, 0.015), belts=None, gun=None, work='tool', carry='box'),
            'phao_binh': dict(inf, coat=C(0.025, 0.028, 0.07), facings=[C(0.45, 0.05, 0.04)], lining=C(0.45, 0.05, 0.04), gun=None, work='tool', carry='box'),
            'thuy_thu': dict(sex='m', jacket=C(0.035, 0.042, 0.09), trousers=C(0.55, 0.53, 0.46), shirt=C(0.6, 0.58, 0.52), shoes=BLK, hat='round', hatcol=C(0.06, 0.06, 0.06),
                             neckerchief=C(0.08, 0.08, 0.09), hair='queue', gun=None, work='sack', carry='sack'),
            'dan_nam': dict(sex='m', frock=C(0.12, 0.075, 0.045), waistcoat=C(0.25, 0.2, 0.12), breeches=C(0.08, 0.065, 0.05), stockings=C(0.3, 0.29, 0.27), shoes=C(0.08, 0.06, 0.04),
                            hat='tricorn', hatcol=C(0.05, 0.045, 0.04), lace=None, hair='queue', gun=None, work='sack', carry='sack', nohat_b=(1,)),
            'dan_nu': dict(sex='f', skirt=C(0.07, 0.05, 0.06), bodice=C(0.1, 0.07, 0.05), apron=C(0.45, 0.43, 0.37), shawl=C(0.15, 0.11, 0.07), shoes=C(0.04, 0.03, 0.02),
                           hat='mobcap', hatcol=C(0.6, 0.58, 0.53), hair='bun', gun=None, work='basket', carry='basket'),
            'khieng': dict(pair='linh2', item='barrel'),
        }
    BD = C(0.1, 0.075, 0.042); KD = C(0.3, 0.24, 0.14); WEB = C(0.33, 0.3, 0.2); NAVY = C(0.022, 0.025, 0.05); RAFB = C(0.06, 0.075, 0.11); BLK = C(0.03, 0.03, 0.03)
    return {
        'linh': dict(sex='m', blouse=BD, trousers=BD, anklets=WEB, boots=BLK, webbing=WEB, hat='brodie', hatcol=C(0.08, 0.08, 0.05), gun='rifle', work='order', carry=None, hair='short'),
        'linh2': dict(sex='m', shirt=KD, trousers=KD, boots=BLK, belt=WEB, hat='sidecap', hatcol=C(0.12, 0.1, 0.06), rolled=True, gun=None, work='back', carry='box', hair='short'),
        'thuy_thu': dict(sex='m', jumper=NAVY, trousers=NAVY, collar=C(0.06, 0.09, 0.2), front=C(0.65, 0.65, 0.62), shoes=BLK, hat='sailor', hatcol=C(0.7, 0.7, 0.67), band=BLK,
                         gun=None, work='sack', carry='sack', hair='short'),
        'thuy_thu_trang': dict(sex='m', jumper=C(0.68, 0.68, 0.65), trousers=C(0.68, 0.68, 0.65), collar=C(0.06, 0.09, 0.2), front=C(0.68, 0.68, 0.65), shoes=BLK, hat='sailor',
                               hatcol=C(0.7, 0.7, 0.67), band=BLK, gun=None, work='back', carry='sack', hair='short'),
        'raf': dict(sex='m', blouse=RAFB, trousers=RAFB, boots=BLK, belt=RAFB, hat='sidecap', hatcol=RAFB, gun=None, work='back', carry=None, hair='short'),
        'tho': dict(sex='m', shirt=C(0.4, 0.38, 0.33), vest=C(0.12, 0.12, 0.13), trousers=C(0.13, 0.13, 0.15), boots=C(0.08, 0.06, 0.04), hat='flatcap', hatcol=C(0.2, 0.19, 0.18),
                    rolled=True, gun=None, work='tool', carry='box', hair='short', nohat_b=(2,)),
        'khieng': dict(pair='tho', item='crate'),
    }

def builds(sex):
    """3 dáng thân: trung bình · gầy cao · chắc thấp (nữ: trung bình · đầy đặn thấp · mảnh cao)."""
    if sex == 'f': return [dict(H=1.62, sw=1.0, g=1.0, belly=0.0), dict(H=1.57, sw=1.04, g=1.12, belly=0.012), dict(H=1.66, sw=0.96, g=0.93, belly=0.0)]
    return [dict(H=1.73, sw=1.0, g=1.0, belly=0.0), dict(H=1.80, sw=0.97, g=0.9, belly=0.0), dict(H=1.67, sw=1.07, g=1.12, belly=0.014)]

SKIN = [C(0.27, 0.16, 0.11), C(0.22, 0.13, 0.085), C(0.31, 0.19, 0.13), C(0.18, 0.105, 0.07)]
HAIR = [C(0.05, 0.035, 0.025), C(0.12, 0.08, 0.05), C(0.025, 0.022, 0.02), C(0.24, 0.16, 0.09), C(0.3, 0.28, 0.26)]

def zr(a, b): return lambda P: np.maximum(a - P[..., 2], P[..., 2] - b)
def opening(xw, y0, ztop=None, zbot=None):
    """vùng KHOÉT (≤ 0 bên trong): |x| < xw(z) ở phía trước (y < y0), trong dải cao độ."""
    def f(P):
        d = np.maximum(np.abs(P[..., 0]) - xw(P[..., 2]), P[..., 1] - y0)
        if ztop is not None: d = np.maximum(d, P[..., 2] - ztop)
        if zbot is not None: d = np.maximum(d, zbot - P[..., 2])
        return d
    return f
def cut(band, op): return lambda P: np.maximum(band(P), -op(P))
def notmid(band, w=0.02): return lambda P: np.maximum(band(P), w - np.abs(P[..., 0]))     # bỏ dải giữa hai chân (giày, ghệt)

def garments(body, R, bi):
    """lớp áo (trong → ngoài): dict(name, base, t_in, t_out, clip(P)≤0 trong vùng, col, kind, bones, fold, amp, rootmix, regions[(fn(P)->bool, col)])."""
    z, J, k = body.z, body.J, body.k; G = []
    def add(**kw):
        kw.setdefault('kind', 'cloth'); kw.setdefault('fold', []); kw.setdefault('regions', []); kw.setdefault('rootmix', 0.0); kw.setdefault('amp', 0.0026); G.append(kw)
    def arm_range(sd, s0, s1):
        S, dv = J['sh' + sd], J['armdir' + sd]
        return lambda P: np.maximum(s0 - (P - S) @ dv, (P - S) @ dv - s1)
    ua_fa = body.ua_fa
    shoes = lambda col, top=0.075, t=0.009: add(name='giay', base='core', t_in=0.0, t_out=t, clip=notmid(zr(-0.012, top)), col=col, kind='leather', bones='legs', amp=0.0)
    if 'coat' in R or 'frock' in R:
        mil = 'coat' in R; coat = R['coat'] if mil else R['frock']
        fac = R['facings'][bi % len(R['facings'])] if mil else coat
        add(name='gile', base='core', t_in=0.002, t_out=0.009, clip=zr(z['pelvis'] - 0.07, z['neck'] - 0.03), col=R['waistcoat'], bones='torso', fold=['waist'])
        zc = z['waist'] + 0.02 if mil else z['chest']
        op = opening(lambda zz: 0.012 + np.maximum(0.0, zc - zz) * (0.55 if mil else 0.35), -0.02, ztop=zc)
        lapel = (lambda P: (np.abs(P[..., 0]) < 0.068 - 0.1 * np.maximum(0, z['chest'] - P[..., 2])) & (P[..., 1] < -0.02) & (P[..., 2] > z['waist'] + 0.01) & (P[..., 2] < z['sh'])) if mil else None
        add(name='ao', base='core', t_in=0.011, t_out=0.021, clip=cut(zr(z['pelvis'] - 0.02, z['neck'] + 0.005), op), col=coat, bones='torso', fold=['waist', 'armpit'],
            regions=[(lapel, fac)] if lapel else [])
        for sd in 'LR':
            cuff = (lambda sd_: lambda P: ((P - J['sh' + sd_]) @ J['armdir' + sd_]) > ua_fa - 0.1)(sd)
            add(name='tay_ao' + sd, base='arm' + sd, t_in=0.006, t_out=0.017, clip=arm_range(sd, -0.07, ua_fa - 0.012), col=coat, bones='arm' + sd, fold=['elbows'],
                regions=[(cuff, fac)] if mil else [])
        if mil: add(name='co_ao', base='core', t_in=0.012, t_out=0.024, clip=zr(z['neck'] - 0.03, z['neck'] + 0.035), col=fac, bones='torso', amp=0.0)
        add(name='vat', base='skirt', t_out=0.009, col=coat, bones='legs', rootmix=0.55, lining=R.get('lining', coat), amp=0.0)
        if R.get('belts'):
            for sg in (1, -1):   # đai chéo: dải 5,5 cm quanh thân theo mặt phẳng nối vai này – hông kia
                p0 = V(sg * 0.13, 0, z['sh'] - 0.02); p1 = V(-sg * 0.14, 0, z['pelvis'] - 0.01); t_ = p1 - p0; n = V(-t_[2], 0, t_[0]); n = n / np.linalg.norm(n)
                add(name='dai' + ('L' if sg > 0 else 'R'), base='core', t_in=0.02, t_out=0.026,
                    clip=(lambda p0_, n_: lambda P: np.maximum(np.abs((P - p0_) @ n_) - 0.028, zr(z['pelvis'] - 0.06, z['sh'] + 0.03)(P)))(p0, n),
                    col=R['belts'], kind='leather', bones='torso', amp=0.0)
        add(name='quan_chen', base='core', t_in=0.002, t_out=0.008, clip=zr(z['knee'] - 0.06, z['waist'] - 0.02), col=R['breeches'], bones='legs', fold=['crotch', 'knees'])
        if R.get('gaiters'): add(name='ghet', base='core', t_in=0.006, t_out=0.014, clip=notmid(zr(0.02, z['knee'] + 0.05)), col=R['gaiters'], bones='legs', fold=['ankles'], amp=0.002)
        if R.get('stockings'): add(name='tat', base='core', t_in=0.0, t_out=0.003, clip=notmid(zr(0.05, z['knee'] - 0.04)), col=R['stockings'], bones='legs', amp=0.0)
        shoes(R['shoes'])
        add(name='ca_vat', base='core', t_in=0.008, t_out=0.016, clip=zr(z['neck'] + 0.02, z['chin']), col=R.get('stock', C(0.75, 0.73, 0.68)), bones='torso', amp=0.0)
    elif 'jacket' in R:   # 1782 thuỷ thủ
        add(name='so_mi', base='core', t_in=0.002, t_out=0.008, clip=zr(z['pelvis'], z['neck'] - 0.02), col=R['shirt'], bones='torso')
        add(name='ao', base='core', t_in=0.009, t_out=0.019, clip=cut(zr(z['pelvis'] - 0.04, z['neck'] - 0.01), opening(lambda zz: 0.03 + 0 * zz, -0.03)), col=R['jacket'],
            bones='torso', fold=['waist', 'armpit'])
        for sd in 'LR': add(name='tay_ao' + sd, base='arm' + sd, t_in=0.006, t_out=0.016, clip=arm_range(sd, -0.07, ua_fa - 0.02), col=R['jacket'], bones='arm' + sd, fold=['elbows', 'wrists'])
        add(name='quan', base='legs_loose', t_in=0.004, t_out=0.02, clip=zr(0.07, z['waist'] - 0.02), col=R['trousers'], bones='legs', fold=['knees', 'crotch', 'ankles'], amp=0.0034)
        shoes(R['shoes'])
        add(name='khan_co', base='core', t_in=0.012, t_out=0.022, clip=zr(z['neck'] - 0.02, z['neck'] + 0.03), col=R['neckerchief'], bones='torso', amp=0.0)
    elif 'bodice' in R:   # 1782 dân nữ
        add(name='ao', base='core', t_in=0.004, t_out=0.012, clip=zr(z['waist'] - 0.06, z['neck'] - 0.01), col=R['bodice'], bones='torso', fold=['waist'])
        for sd in 'LR': add(name='tay_ao' + sd, base='arm' + sd, t_in=0.005, t_out=0.013, clip=arm_range(sd, -0.07, 0.3 * k + 0.12), col=R['bodice'], bones='arm' + sd, fold=['elbows'])
        add(name='khan_choang', base='core', t_in=0.013, t_out=0.022, clip=zr(z['chest'] - 0.02, z['neck'] + 0.01), col=R['shawl'], bones='torso', amp=0.003)
        add(name='vay', base='dress', t_out=0.01, col=R['skirt'], bones='legs', rootmix=0.75, lining=R['skirt'], amp=0.0)
        add(name='tap_de', base='apron', t_out=0.006, col=R['apron'], bones='legs', rootmix=0.75, lining=R['apron'], amp=0.0)
        shoes(R['shoes'], 0.07, 0.008)
    else:   # 1943
        if 'blouse' in R:   # battledress: blouse tới eo + cạp + 2 túi ngực; quần rộng có túi đùi trái
            add(name='ao', base='core', t_in=0.012, t_out=0.026, clip=zr(z['pelvis'] + 0.02, z['neck'] + 0.012), col=R['blouse'], bones='torso', fold=['waist', 'armpit'], amp=0.0032)
            add(name='cap_ao', base='core', t_in=0.02, t_out=0.031, clip=zr(z['pelvis'] - 0.005, z['pelvis'] + 0.045), col=tuple(c * 0.92 for c in R['blouse']), bones='torso', amp=0.0)
            for sg in (1, -1):
                add(name='tui' + ('L' if sg > 0 else 'R'), base='core', t_in=0.022, t_out=0.032,
                    clip=(lambda sg_: lambda P: sd_box(P, V(sg_ * 0.075, -0.1, z['chest'] + 0.035), V(0.052, 0.12, 0.06)))(sg), col=tuple(c * 0.95 for c in R['blouse']), bones='torso', amp=0.0)
            for sd in 'LR': add(name='tay_ao' + sd, base='arm' + sd, t_in=0.007, t_out=0.021, clip=arm_range(sd, -0.07, ua_fa - 0.01), col=R['blouse'], bones='arm' + sd, fold=['elbows', 'wrists'], amp=0.0032)
            add(name='quan', base='legs_loose', t_in=0.004, t_out=0.022, clip=zr(0.1, z['pelvis'] + 0.06), col=R['trousers'], bones='legs', fold=['knees', 'crotch', 'ankles'], amp=0.0036)
            add(name='tui_dui', base='legs_loose', t_in=0.02, t_out=0.03, clip=lambda P: sd_box(P, V(0.115, -0.07, z['knee'] + 0.2), V(0.06, 0.12, 0.08)), col=tuple(c * 0.95 for c in R['trousers']), bones='legs', amp=0.0)
        elif 'shirt' in R:
            hi = 0.3 * k * 0.62 if R.get('rolled') else ua_fa - 0.015
            add(name='ao', base='core', t_in=0.006, t_out=0.016, clip=zr(z['pelvis'] - 0.02, z['neck'] + 0.006), col=R['shirt'], bones='torso', fold=['waist', 'armpit'])
            for sd in 'LR':
                add(name='tay_ao' + sd, base='arm' + sd, t_in=0.005, t_out=0.014, clip=arm_range(sd, -0.07, hi), col=R['shirt'], bones='arm' + sd, fold=['elbows'])
                if R.get('rolled'): add(name='xan' + sd, base='arm' + sd, t_in=0.012, t_out=0.024, clip=arm_range(sd, hi - 0.05, hi), col=R['shirt'], bones='arm' + sd, amp=0.002)
            if R.get('vest'): add(name='gile', base='core', t_in=0.016, t_out=0.024, clip=cut(zr(z['pelvis'], z['sh'] - 0.03), opening(lambda zz: 0.012 + np.maximum(0, zz - z['chest']) * 0.4, -0.03)),
                                   col=R['vest'], bones='torso')
            add(name='quan', base='legs_loose', t_in=0.004, t_out=0.02, clip=zr(0.08, z['pelvis'] + 0.06), col=R['trousers'], bones='legs', fold=['knees', 'crotch', 'ankles'], amp=0.0034)
        else:   # lính thuỷ RN: áo chui cổ chữ V (lộ áo lót) + cổ vuông sau lưng + quần ống loe
            vneck = opening(lambda zz: np.maximum(0.0, zz - (z['sh'] - 0.15)) * 0.8, -0.02, zbot=z['sh'] - 0.15)
            add(name='ao_lot', base='core', t_in=0.002, t_out=0.007, clip=zr(z['sh'] - 0.2, z['neck'] - 0.005), col=R['front'], bones='torso', amp=0.0)
            add(name='ao', base='core', t_in=0.008, t_out=0.02, clip=cut(zr(z['pelvis'] - 0.06, z['neck'] - 0.005), vneck), col=R['jumper'], bones='torso', fold=['waist', 'armpit'])
            add(name='co_vuong', base='core', t_in=0.021, t_out=0.027, clip=lambda P: sd_box(P, V(0, 0.1, z['sh'] - 0.07), V(0.15, 0.09, 0.1)), col=R['collar'], bones='torso', amp=0.0,
                regions=[(lambda P: (np.abs(np.abs(P[..., 0]) - 0.135) < 0.004) | (np.abs(P[..., 2] - (z['sh'] - 0.155)) < 0.004), C(0.85, 0.85, 0.82))])
            for sd in 'LR': add(name='tay_ao' + sd, base='arm' + sd, t_in=0.006, t_out=0.017, clip=arm_range(sd, -0.07, ua_fa - 0.012), col=R['jumper'], bones='arm' + sd, fold=['elbows', 'wrists'])
            add(name='quan', base='bells', t_in=0.004, t_out=0.022, clip=zr(0.06, z['pelvis'] + 0.03), col=R['trousers'], bones='legs', fold=['knees', 'crotch'], amp=0.0034)
        if R.get('anklets'): add(name='xa_cap', base='core', t_in=0.024, t_out=0.034, clip=notmid(zr(0.05, 0.165)), col=R['anklets'], bones='legs', amp=0.0)
        shoes(R.get('boots', R.get('shoes')), 0.1 if R.get('boots') else 0.075, 0.012)
        if R.get('webbing'):   # dây đeo mẫu 1937: thắt lưng + 2 túi đạn trước ngực + 2 quai qua vai bắt chéo sau lưng
            add(name='that_lung', base='core', t_in=0.03, t_out=0.038, clip=zr(z['pelvis'], z['pelvis'] + 0.058), col=R['webbing'], bones='torso', amp=0.0)
            for sg in (1, -1):
                add(name='tui_dan' + ('L' if sg > 0 else 'R'), base='core', t_in=0.03, t_out=0.075,
                    clip=(lambda sg_: lambda P: sd_box(P, V(sg_ * 0.085, -0.12, z['waist'] + 0.075), V(0.058, 0.12, 0.062)))(sg), col=R['webbing'], bones='torso', amp=0.0)
                def strap(P, sg_=sg):
                    tb = np.clip((z['sh'] - P[..., 2]) / (z['sh'] - z['waist'] - 0.05), 0, 1)
                    front = np.abs(P[..., 0] - sg_ * 0.09) - 0.021; back = np.abs(P[..., 0] - (sg_ * 0.1 - sg_ * 0.19 * tb)) - 0.021
                    return np.maximum(np.where(P[..., 1] < 0, front, back), zr(z['waist'] + 0.1, z['sh'] + 0.09)(P))
                add(name='quai' + ('L' if sg > 0 else 'R'), base='core', t_in=0.028, t_out=0.035, clip=strap, col=R['webbing'], bones='torso', amp=0.0)
        elif R.get('belt'):
            add(name='that_lung', base='core', t_in=0.018, t_out=0.026, clip=zr(z['pelvis'], z['pelvis'] + 0.05), col=R['belt'], bones='torso', amp=0.0)
    return G

def skirt_shell(P, body, kind, th):
    """vạt áo 1782 ('skirt'), váy ('dress'), tạp dề ('apron'): VỎ MỎNG quanh mặt elip loe (hở gấu, hở trên); trả (sdf vỏ, hàm vùng lót)."""
    z = body.z
    if kind == 'skirt':
        z0, z1 = z['waist'] - 0.02, z['knee'] + 0.035; flare = (0.075, 0.055); r0 = (0.172 * body.g + body.belly * 0.4, 0.124 * body.g + body.belly)
    elif kind == 'dress':
        z0, z1 = z['waist'], 0.05; flare = (0.13, 0.11); r0 = (0.17 * body.g, 0.13 * body.g)
    else:
        z0, z1 = z['waist'] - 0.01, 0.24; flare = (0.135, 0.115); r0 = (0.182 * body.g, 0.142 * body.g)
    t = np.clip((z0 - P[..., 2]) / (z0 - z1), 0, 1) ** 0.85
    rx = r0[0] + flare[0] * t; ry = r0[1] + flare[1] * t
    q = np.stack([P[..., 0] / rx, (P[..., 1] - 0.012) / ry], -1); lat = (_len(q) - 1.0) * np.minimum(rx, ry)
    d = np.maximum(np.abs(lat - th / 2) - th / 2, np.maximum(P[..., 2] - z0, z1 - P[..., 2]))
    lining = None
    if kind == 'skirt':   # xẻ trước: mép cắt chéo loe ra hai bên; xẻ sau giữa lưng; lót trắng lộ ở mép (vạt bẻ ngược)
        fr = -(P[..., 1] + 0.01) - (np.abs(P[..., 0]) - (0.02 + 0.34 * (z0 - P[..., 2]))) * 2.2
        vent = np.where((P[..., 2] < z0 - 0.09) & (P[..., 1] > 0), 0.008 - np.abs(P[..., 0]), -1.0)
        d = np.maximum(d, np.maximum(fr, vent))
        lining = lambda Q: ((-(Q[..., 1] + 0.01) - (np.abs(Q[..., 0]) - (0.02 + 0.34 * (z0 - Q[..., 2]))) * 2.2) > -0.075) | ((Q[..., 1] > 0) & (np.abs(Q[..., 0]) < 0.05) & (Q[..., 2] < z0 - 0.07))
    if kind == 'apron': d = np.maximum(d, P[..., 1] + 0.02)
    return d, lining

def loose_legs(P, body, kind):
    """ống quần rộng (battledress, KD, thuỷ thủ) / ống loe (RN): thân không đầu ∪ nón quanh đùi + cẳng."""
    J = body.J; d = body.core(P)
    for sd in 'LR':
        hip, kn, an = J['hip' + sd], J['knee' + sd], J['ankle' + sd]; rb = 0.058 if kind == 'legs_loose' else 0.078
        d = smin(d, sd_cone(P, hip + V(0, 0, 0.02), kn, 0.09 * body.g, 0.058), 0.02)
        d = smin(d, sd_cone(P, kn, an + V(0, 0, 0.03), 0.056, rb), 0.02)
    return d
