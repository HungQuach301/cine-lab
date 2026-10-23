#!/opt/cine/bin/python
"""TIEN-KY-T4 · HÌNH HỌC CẢNH LONDON dùng chung cho cách A (three.js, design/k2v/ldn/) và Cycles (Blender, scripts/k2ldn/cy_ldn.py).
  hinh_hoc.py   → $LDN_DATA/canh/ldn.bin + ldn.json (mảng Float32/Uint8 theo lớp; tái tạo được: đầu vào OSM/LiDAR/Doornick có lệnh tải + SHA)
Hệ toạ độ: x = E − 532000, y = cao (m, theo ODN), z = −(N − 180800)   (EPSG:27700 + lưới OSTN15).
Mỗi đỉnh: pos(3) · col(3, u8) · tl(4) = [năm sinh, năm mất, y đáy, giờ bén lửa kể từ 2/9/1666 00:00 (lịch Julius) hoặc −1] · k(1) = loại.
Lớp (k): 1 nhà 1666 · 2 phế tích 1666 · 3 nhà xây lại 1667+ · 4 toà 2026 · 5 công trình có tên · 6 tường thành · 7 cầu · 8 tháp nhà thờ cổ · 9 tháp Wren.
Bậc căn cứ (§12.2) ghi trong ldn.json → 'bac'. Dữ kiện ngày cháy: ranh từng ngày = tên nơi bậc 2 (LUAT-N2P-T4 a01–a17) × vị trí bậc 1 (OSM/Doornick); nội suy giữa = bậc 5 (ước lượng)."""
import json, math, os, sys, hashlib
import numpy as np, cv2
from scipy.interpolate import RBFInterpolator
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA = os.environ.get('LDN_DATA', '/var/tmp/ldn'); SRC = os.environ.get('LDN_SRC', '/var/tmp/ldn/tu-lieu')
OUT = os.path.join(DATA, 'canh'); os.makedirs(OUT, exist_ok=True)
E0, N0 = 532000.0, 180800.0
BB = (529500, 179500, 535500, 182500)          # E0 N0 E1 N1 vùng cảnh
RNG = np.random.default_rng(1666)

# ---------------------------------------------------------------- đầu vào
R = json.load(open(os.path.join(DATA, 'vec/osm2026.json')))
DTM = np.load(os.path.join(DATA, 'lidar/dtm_kham_1m.npy')); DSM = np.load(os.path.join(DATA, 'lidar/dsm_kham_1m.npy'))
def lidar(A, E, N):
    c = np.clip((np.asarray(E) - BB[0]).astype(int), 0, A.shape[1] - 1); r = np.clip((BB[3] - np.asarray(N)).astype(int), 0, A.shape[0] - 1); return A[r, c]
K = json.load(open(os.path.join(REPO, 'channel-k2/k2c-t4-02/du-lieu/khop-doornick.json')))
KD = [d for d in K['diem'] if d.get('dung', True)]
TPS = RBFInterpolator(np.array([d['px'] for d in KD], float), np.array([d['en'] for d in KD], float), kernel='thin_plate_spline')
TPSi = RBFInterpolator(np.array([d['en'] for d in KD], float), np.array([d['px'] for d in KD], float), kernel='thin_plate_spline')
RANH = json.load(open(os.path.join(REPO, 'channel-k2/k2c-t4-02/du-lieu/ranh-chay-1666-cuoi.json')))

# lưới raster 2 m cho mặt nạ
G = 2.0; GW, GH = int((BB[2] - BB[0]) / G), int((BB[3] - BB[1]) / G)
def to_g(EN): EN = np.asarray(EN, float); return np.stack([(EN[..., 0] - BB[0]) / G, (BB[3] - EN[..., 1]) / G], -1)
def poly_mask(polys, val=1):
    m = np.zeros((GH, GW), np.uint8)
    for p in polys:
        if len(p) >= 3: cv2.fillPoly(m, [np.round(to_g(p) * 4).astype(np.int32)], val, shift=2)
    return m
def at(m, EN):
    g = to_g(EN); c = np.clip(g[..., 0].astype(int), 0, GW - 1); r = np.clip(g[..., 1].astype(int), 0, GH - 1); return m[r, c]

# nước 2026 (OSM) và bờ bắc 1666 (Doornick, tây Blackfriars; đông Blackfriars giữ bờ 2026 — bậc 5)
WAT26 = poly_mask([w['r'] for w in R['nuoc'] if len(w['r']) > 20])
BURN = poly_mask([RANH['tps']['en']])
im = cv2.imread(os.path.join(SRC, 'rijks-doornick-0.jpg'), 0)
dens = cv2.blur((im < 150).astype(np.float32), (45, 45))
# mặt nạ "có nhà 1666" = vùng nét dày (≥ 0,33) ∪ vùng cháy, ánh xạ ngược px qua TPS (lấy mẫu mỗi 8 m)
ge, gn = np.meshgrid(np.arange(BB[0], BB[2], 8.0), np.arange(BB[3], BB[1], -8.0))
pxy = TPSi(np.stack([ge.ravel(), gn.ravel()], 1)).reshape(ge.shape + (2,))
inside = (pxy[..., 0] > 150) & (pxy[..., 0] < 5150) & (pxy[..., 1] > 250) & (pxy[..., 1] < 2700)
dv = np.zeros(ge.shape, np.float32)
xi = np.clip(pxy[..., 0].astype(int), 0, im.shape[1] - 1); yi = np.clip(pxy[..., 1].astype(int), 0, im.shape[0] - 1)
dv[inside] = dens[yi[inside], xi[inside]]
BUILT8 = ((dv > 0.33) & inside).astype(np.uint8)
BUILT = cv2.resize(BUILT8, (GW, GH), interpolation=cv2.INTER_NEAREST) | BURN
# bờ nam (Southwark): TPS khớp chỉ có điểm bờ bắc → không dùng mặt nạ Doornick ở bờ nam; thay bằng dải nhà ven sông Bankside → St Olave
# (≤ 130 m từ mép nước, E 531300–533700) + dọc Borough High Street (≤ 60 m) tới St George's — bậc 5, theo hình Hollar/Doornick (dải nhà ven sông)
gE = BB[0] + (np.arange(GW) + 0.5) * G; gN = BB[3] - (np.arange(GH) + 0.5) * G
south = (gN[:, None] < 180560) & (gE[None, :] > 531000)
BUILT[south] = 0
dist = cv2.distanceTransform((1 - (WAT26 > 0).astype(np.uint8)), cv2.DIST_L2, 5) * G
rib = (dist < 130) & south & (gE[None, :] > 531300) & (gE[None, :] < 533700)
bhs = np.zeros((GH, GW), np.uint8)
for d in R['duong']:
    if d['name'] in ('Borough High Street', 'Bankside', 'Clink Street', 'Park Street', 'Tooley Street', 'Montague Close'):
        cv2.polylines(bhs, [np.round(to_g(d['l'])).astype(np.int32)], False, 1, thickness=int(120 / G))
BUILT[rib | ((bhs > 0) & south & (gN[:, None] > 179700))] = 1
# bờ bắc 1666 phía tây Blackfriars: đường bờ px Doornick → EN
BANK_PX = np.array([[1800, 1760], [1950, 1700], [2120, 1655], [2390, 1612], [2480, 1614]], float)
bank_en = TPS(BANK_PX)
west = np.array(list(bank_en) + [[531700, 180300], [529500, 180300], [529500, bank_en[0, 1]]])
WAT66 = WAT26.copy()
m_w = poly_mask([west]); land26 = (WAT26 == 0)
WAT66[(m_w == 1)] = 1                        # phía nam bờ 1666 ở bờ tây = nước (Embankment chưa có)
WAT66[(m_w == 0) & land26] = 0
# Fleet ditch mở (1666): kênh ≈ 14 m dọc Farringdon St/New Bridge St, Holborn Bridge → sông
fleet = [l['l'] for l in R['duong'] if l['name'] in ('Farringdon Street', 'New Bridge Street')]
FLEET = np.zeros((GH, GW), np.uint8)
for l in fleet: cv2.polylines(FLEET, [np.round(to_g(l)).astype(np.int32)], False, 1, thickness=7)
FLEET[at(np.ones((GH, GW), np.uint8), [0, 0]) == 2] = 0
WAT66 |= FLEET

# ---------------------------------------------------------------- thời gian cháy (giờ kể từ 2/9/1666 00:00, Julius)
# điểm khống chế: tên nơi + giờ từ nguồn bậc 2 (reports/nc-n2p/LUAT-N2P-T4.md §2); toạ độ OSM 2026 (bậc 1 theo vị trí phố còn giữ)
TC = [  # (tên, E, N, giờ, mã LUAT)
 ('Pudding Lane', 532955, 180762, 1.0, 'a01'), ('St Magnus / Fish Street', 532900, 180670, 7.0, 'a02'), ('Steelyard', 532630, 180705, 12.0, 'a03'),
 ('Three Cranes, Vintry', 532410, 180720, 31.0, 'a05'), ('St Swithin, Cannon St', 532690, 180950, 31.0, 'a05'), ('Gracechurch × Lombard', 532980, 180990, 31.0, 'a05'),
 ('beyond Billingsgate', 533150, 180640, 31.0, 'a05'), ('Cornhill', 532950, 181100, 40.0, 'a06'), ('Royal Exchange', 532830, 181110, 40.0, 'a18'),
 ('Cheapside', 532250, 181130, 46.0, 'a06'), ("Baynard's Castle", 531850, 180850, 46.0, 'a07'), ("St Paul's", 532100, 181130, 68.0, 'a09'),
 ('Ludgate', 531760, 181158, 62.0, 'a08'), ('Fleet bridge', 531632, 181174, 64.0, 'a08'), ('Newgate', 531796, 181409, 66.0, 'a08'),
 ("St Dunstan's, Fleet St", 531229, 181168, 70.0, 'a10'), ('Inner Temple', 531230, 181020, 70.0, 'a08'), ('Pie Corner', 531760, 181560, 72.0, 'a11'),
 ('Holborn Bridge', 531585, 181506, 72.0, 'a11'), ('Aldersgate', 532145, 181465, 75.0, 'a11'), ('Cripplegate', 532350, 181640, 82.0, 'a13'),
 ('lower end Coleman St', 532640, 181330, 80.0, 'a11'), ('end Basinghall St', 532560, 181480, 80.0, 'a11'), ('upper Bishopsgate St', 533150, 181250, 78.0, 'a11'),
 ('Leadenhall St', 533260, 181170, 78.0, 'a11'), ('Standard in Cornhill', 532760, 181100, 72.0, 'a11'), ('church Fenchurch St', 533250, 181020, 72.0, 'a11'),
 ("Clothworkers' Hall", 533290, 180930, 70.0, 'a17'), ('middle Mark Lane', 533350, 180900, 72.0, 'a11'), ('Tower Dock', 533470, 180640, 72.0, 'a11'),
 ('All Hallows Barking', 533386, 180683, 80.0, 'a14')]
tc = np.array([[t[1], t[2]] for t in TC], float); th = np.array([t[3] for t in TC], float)
TFIT = RBFInterpolator(tc, th, kernel='thin_plate_spline', smoothing=2.0)
def t_chay(EN):
    EN = np.atleast_2d(EN); t = np.clip(TFIT(EN), 1.0, 90.0); b = at(BURN, EN) == 1; return np.where(b, t, -1.0)

# ---------------------------------------------------------------- bộ dựng lưới
class M:
    def __init__(s): s.P, s.C, s.T, s.K = [], [], [], []
    def tri(s, a, b, c, col, tl, k):
        s.P += [a, b, c]; s.C += [col] * 3; s.T += [tl] * 3; s.K += [k] * 3
    def quad(s, a, b, c, d, col, tl, k): s.tri(a, b, c, col, tl, k); s.tri(a, c, d, col, tl, k)
    def prism(s, ring, y0, y1, colw, colr, tl, k, roof=None, rh=0.0):
        """ring: [(x,z)] ngược kim đồng hồ nhìn từ trên; tường y0→y1; mái phẳng hoặc 'gable' (dọc cạnh dài)"""
        n = len(ring)
        for i in range(n):
            (x0, z0), (x1, z1) = ring[i], ring[(i + 1) % n]
            s.quad((x0, y0, z0), (x1, y0, z1), (x1, y1, z1), (x0, y1, z0), colw, tl, k)
        if roof == 'gable' and n == 4 and rh > 0:
            p = [np.array(r) for r in ring]; e01 = np.linalg.norm(p[1] - p[0]); e12 = np.linalg.norm(p[2] - p[1])
            if e01 < e12: p = p[1:] + p[:1]      # nóc dọc cạnh dài p0→p1
            m0, m1 = (p[0] + p[3]) / 2, (p[1] + p[2]) / 2
            A, B, C_, D = [(q[0], y1, q[1]) for q in p]; R0, R1 = (m0[0], y1 + rh, m0[1]), (m1[0], y1 + rh, m1[1])
            s.quad(A, B, R1, R0, colr, tl, k); s.quad(C_, D, R0, R1, colr, tl, k)
            s.tri(D, A, R0, colw, tl, k); s.tri(B, C_, R1, colw, tl, k)
        elif roof == 'pyr' and rh > 0:
            cx = sum(r[0] for r in ring) / n; cz = sum(r[1] for r in ring) / n
            for i in range(n):
                (x0, z0), (x1, z1) = ring[i], ring[(i + 1) % n]; s.tri((x0, y1, z0), (x1, y1, z1), (cx, y1 + rh, cz), colr, tl, k)
        else:
            for i in range(1, n - 1):
                s.tri((ring[0][0], y1, ring[0][1]), (ring[i][0], y1, ring[i][1]), (ring[i + 1][0], y1, ring[i + 1][1]), colr, tl, k)
    def box(s, cx, cz, w, d, ang, y0, y1, colw, colr, tl, k, roof=None, rh=0.0):
        c, sn = math.cos(ang), math.sin(ang)
        ring = [(cx + c * u - sn * v, cz + sn * u + c * v) for u, v in ((-w / 2, -d / 2), (w / 2, -d / 2), (w / 2, d / 2), (-w / 2, d / 2))]
        s.prism(ring, y0, y1, colw, colr, tl, k, roof, rh)
    def cyl(s, cx, cz, r0, r1, y0, y1, col, tl, k, seg=16, cap=True):
        for i in range(seg):
            a0, a1 = 2 * math.pi * i / seg, 2 * math.pi * (i + 1) / seg
            p00 = (cx + r0 * math.cos(a0), y0, cz + r0 * math.sin(a0)); p01 = (cx + r0 * math.cos(a1), y0, cz + r0 * math.sin(a1))
            p10 = (cx + r1 * math.cos(a0), y1, cz + r1 * math.sin(a0)); p11 = (cx + r1 * math.cos(a1), y1, cz + r1 * math.sin(a1))
            s.quad(p00, p10, p11, p01, col, tl, k)
            if cap and r1 > 0: s.tri((cx, y1, cz), p11, p10, col, tl, k)
    def dome(s, cx, cz, r, y0, h, col, tl, k, seg=24, rings=8):
        for j in range(rings):
            f0, f1 = j / rings, (j + 1) / rings
            ra, rb = r * math.cos(f0 * math.pi / 2), r * math.cos(f1 * math.pi / 2); ya, yb = y0 + h * math.sin(f0 * math.pi / 2), y0 + h * math.sin(f1 * math.pi / 2)
            s.cyl(cx, cz, ra, rb, ya, yb, col, tl, k, seg, cap=False)
    def arr(s):
        return (np.array(s.P, np.float32).reshape(-1, 3), np.array(s.C, np.uint8).reshape(-1, 3), np.array(s.T, np.float32).reshape(-1, 4), np.array(s.K, np.uint8))

def L(E, N): return (E - E0, -(N - N0))
def H(E, N): return float(np.clip(lidar(DTM, E, N), 0.5, 40.0))

# ---------------------------------------------------------------- địa hình (hai cao độ: 1666 và 2026)
def dia_hinh(step=5.0):
    es = np.arange(BB[0], BB[2] + 0.1, step); ns = np.arange(BB[3], BB[1] - 0.1, -step)
    EE, NN = np.meshgrid(es, ns); h = cv2.resize(DTM, (len(es), len(ns)), interpolation=cv2.INTER_AREA)
    h = np.clip(h, 0.5, 45.0)
    w26 = at(WAT26, np.stack([EE, NN], -1)); w66 = at(WAT66, np.stack([EE, NN], -1))
    h26 = np.where(w26 == 1, -3.0, h); h66 = np.where(w66 == 1, -3.0, np.where(w26 == 1, 2.5, h))   # đất 1666 nơi nay là nước = bờ thấp 2,5 m
    green = np.zeros_like(h, np.uint8)
    gm = poly_mask([d['r'] for d in R['dat']]); green = at(gm, np.stack([EE, NN], -1))
    return {'nx': len(es), 'nz': len(ns), 'x0': es[0] - E0, 'z0': -(ns[0] - N0), 'step': step, 'h26': h26.astype(np.float32), 'h66': h66.astype(np.float32), 'xanh': green.astype(np.uint8)}

# ---------------------------------------------------------------- phố 1666
SAU_1666 = {'Victoria Embankment', 'Queen Victoria Street', 'London Wall', 'Holborn Viaduct', 'King William Street', 'Farringdon Street', 'New Bridge Street', 'Farringdon Road',
 'Moorgate', 'Byward Street', 'Southwark Bridge', 'Blackfriars Bridge', 'London Bridge', 'Tower Bridge Approach', 'Blackfriars Underpass', 'Mansell Street', 'Commercial Street',
 'Princes Street', 'Queen Street', 'King Street', 'Queen Street Place', 'Castle Baynard Street', 'Puddle Dock', "Paul's Walk", "The Queen's Walk", 'Bazalgette Embankment', 'Temple Place',
 'John Carpenter Street', 'Blomfield Street', 'Finsbury Circus', 'Liverpool Street', 'Fleet Place', 'St. Bride Street', 'King Edward Street', 'New Fetter Lane', 'Monument Street', 'Arthur Street',
 'Andrewes Highwalk', 'Aldersgate Rotunda', 'St. Alphage Highwalk', 'Thomas More Highwalk', 'Millennium Bridge', 'Tower Hill', 'Mint Street', "Goodman's Yard", 'Copthall Avenue',
 'Throgmorton Avenue', 'New Change', 'Montague Street', 'Sun Street Passage', 'Central Courtyard', 'The Avenue', 'Blackfriars Passage', 'Blackfriars Subway', 'Gloucester Court', 'Fenchurch Place',
 "St. Katharine's Way", 'Southwark Street', 'Southwark Bridge Road', 'Blackfriars Road', 'Sumner Street', 'Stamford Street', 'Duke Street Hill',
 'Upper Ground', 'Hopton Street', 'Great Suffolk Street', 'Charterhouse Street', 'Gray\'s Inn Road', 'Clerkenwell Road', 'Old Street', 'City Road', 'Shoreditch High Street', 'Great Eastern Street'}
def pho_1666():
    out = []
    for d in R['duong']:
        nm, hw = d['name'], d['hw']
        if hw in ('rail', 'proposed', 'platform', 'corridor', 'steps', 'cycleway') or d.get('tunnel') == 'yes': continue
        if not nm:
            continue
        if nm in SAU_1666 or 'Highwalk' in nm: continue
        if hw in ('footway', 'path', 'service', 'pedestrian') and not any(w in nm for w in ('Lane', 'Alley', 'Court', 'Yard', 'Row', 'Hill', 'Churchyard', 'Passage', 'Place')): continue
        hwid = {'trunk': 6.0, 'primary': 5.0, 'secondary': 4.5, 'tertiary': 4.0, 'unclassified': 3.0, 'residential': 3.0}.get(hw, 1.8)
        out.append((np.array(d['l'], float), hwid, nm))
    return out

COL = {'voi': (196, 182, 156), 'go': (92, 70, 52), 'ngoi': (128, 72, 52), 'ngoi2': (110, 82, 66), 'gach': (150, 78, 56), 'gach2': (124, 68, 52), 'ngoi_xam': (88, 80, 76),
       'da': (170, 162, 146), 'portland': (214, 208, 194), 'chi': (120, 126, 132), 'pheTich': (118, 108, 98), 'den': (40, 36, 34), 'kinh': (120, 136, 150)}
def jitter(c, a=10):
    k = RNG.integers(-a, a + 1)                     # lệch sáng chung + lệch màu nhỏ (tránh pastel hồng/xanh ngẫu nhiên)
    return tuple(int(np.clip(v + k + RNG.integers(-a // 4, a // 4 + 1), 0, 255)) for v in c)

def nha_1666(m, streets):
    occ = np.zeros((GH, GW), np.uint8); occ |= WAT66
    n = {'1666': 0, 'xay_lai': 0, 'phe_tich': 0}
    for l, hw, nm in streets:
        seg = np.diff(l, axis=0); ln = np.linalg.norm(seg, axis=1)
        for i in range(len(seg)):
            if ln[i] < 3: continue
            u = seg[i] / ln[i]; v = np.array([-u[1], u[0]]); ang = math.atan2(-u[1], u[0])   # góc trong (x, z)
            s = 0.0
            while s < ln[i]:
                w = float(RNG.uniform(3.6, 6.2)); d = float(RNG.uniform(8.0, 13.0)) if hw >= 3 else float(RNG.uniform(6.0, 10.0))
                d2 = float(RNG.uniform(6.0, 10.0))
                for side, row in ((1, 0), (-1, 0), (1, 1), (-1, 1)):
                    if row == 1 and hw < 3: continue
                    dd = d if row == 0 else d2
                    off = hw + 0.6 + d / 2 if row == 0 else hw + 0.6 + d + 1.2 + d2 / 2
                    c = l[i] + u * (s + w / 2) + v * side * off
                    if not (BB[0] + 50 < c[0] < BB[2] - 50 and BB[1] + 50 < c[1] < BB[3] - 50): continue
                    if at(BUILT, c) == 0: continue
                    # chiếm chỗ
                    cs = [c + u * a * w / 2 + v * b * dd / 2 for a in (-0.8, 0, 0.8) for b in (-0.8, 0, 0.8)]
                    if sum(at(occ, q) for q in cs) > 1: continue
                    poly = np.array([c + u * (-w / 2) + v * (-dd / 2), c + u * (w / 2) + v * (-dd / 2), c + u * (w / 2) + v * (dd / 2), c + u * (-w / 2) + v * (dd / 2)])
                    cv2.fillPoly(occ, [np.round(to_g(poly)).astype(np.int32)], 1)
                    x, z = L(*c); g = H(*c); burn = float(t_chay(c)[0])
                    st = int(RNG.choice([3, 3, 4, 4, 2], p=[0.3, 0.2, 0.25, 0.15, 0.1]) if hw >= 3 else RNG.choice([2, 3], p=[0.6, 0.4]))
                    y1 = g + st * 2.8 + RNG.uniform(-0.3, 0.3); rh = RNG.uniform(2.5, 4.0)
                    die = 1666.0 + (245 + burn / 24) / 365.0 if burn >= 0 else 1800.0 + RNG.uniform(0, 60)
                    wallc = jitter(COL['voi'] if RNG.random() < 0.7 else COL['go'], 14)
                    m.box(x, z, w * 0.98, dd, ang, g, y1, wallc, jitter(COL['ngoi'] if RNG.random() < 0.8 else COL['ngoi2'], 12), (1500.0, die, g, burn), 1, 'gable', rh)
                    n['1666'] += 1
                    if burn >= 0:
                        # phế tích: tường gạch/ống khói thấp (đá nung trắng — Evelyn b13) tới khi xây lại
                        reb = 1667.3 + float(RNG.exponential(1.2)); reb = min(reb, 1672.0)
                        m.box(x, z, w * 0.9, dd * 0.9, ang, g, g + RNG.uniform(1.0, 3.5), jitter(COL['pheTich'], 14), jitter(COL['pheTich'], 14), (die, reb, g, burn), 2)
                        if RNG.random() < 0.5: m.box(x + u[0] * w * 0.3, z - u[1] * w * 0.3, 1.0, 1.4, ang, g, g + RNG.uniform(5, 9), jitter((70, 58, 50), 8), jitter((70, 58, 50), 8), (die, reb, g, burn), 2)
                        n['phe_tich'] += 1
                        # nhà xây lại theo Rebuilding Act 1667: tường gạch; 2/3/4 tầng theo hạng phố (by-lane / phố đáng kể / phố lớn)
                        st2 = 4 if hw >= 5 else 3 if hw >= 3 else 2
                        y2 = g + st2 * 3.0 + RNG.uniform(0, 0.4)
                        m.box(x, z, w * 0.98, dd, ang, g, y2, jitter(COL['gach'] if RNG.random() < 0.6 else COL['gach2'], 12), jitter(COL['ngoi_xam'], 10), (reb, 1850.0 + RNG.uniform(0, 90), g, -1.0), 3, 'gable', RNG.uniform(1.8, 3.0))
                        n['xay_lai'] += 1
                s += w
    # lấp lõi khối (sân sau/ngõ không còn trên OSM): lưới 7 m có lệch, hướng theo phố gần nhất; chỉ trong vùng có nhà (mặt nạ) — bậc 5
    st = np.zeros((GH, GW), np.uint8)
    for l, hw, nm in streets: cv2.polylines(st, [np.round(to_g(l)).astype(np.int32)], False, 1, thickness=max(1, int(2 * hw / G)))
    dt, lab = cv2.distanceTransformWithLabels(1 - st, cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
    ys, xs = np.where(st > 0); lab_xy = np.zeros((lab.max() + 1, 2), np.float32)
    lab_xy[lab[ys, xs]] = np.stack([xs, ys], 1)
    gy, gx = np.gradient(dt.astype(np.float32))
    for N in np.arange(BB[3] - 60, BB[1] + 60, -7.0):
        for E in np.arange(BB[0] + 60, BB[2] - 60, 7.0):
            c = np.array([E + RNG.uniform(-1.5, 1.5), N + RNG.uniform(-1.5, 1.5)])
            if at(BUILT, c) == 0 or at(occ, c) == 1: continue
            gc = to_g(c); r_, c_ = int(gc[1]), int(gc[0])
            if dt[r_, c_] * G > 45: continue                 # xa phố > 45 m: vườn/sân trong (Hollar vẽ vườn) — để trống
            if RNG.random() < 0.18: continue                 # chừa sân/giếng trời
            ddx, ddy = gx[r_, c_], -gy[r_, c_]; ang_n = math.atan2(-ddy, ddx)       # pháp tuyến về phía phố (trong x,z)
            w = float(RNG.uniform(4.0, 6.5)); d = float(RNG.uniform(6.0, 9.0))
            u = np.array([math.cos(ang_n + math.pi / 2), -math.sin(ang_n + math.pi / 2)]); v = np.array([-u[1], u[0]])
            cs = [c + u * a * w / 2 + v * b * d / 2 for a in (-0.8, 0, 0.8) for b in (-0.8, 0, 0.8)]
            if sum(at(occ, q) for q in cs) > 1: continue
            poly = np.array([c - u * w / 2 - v * d / 2, c + u * w / 2 - v * d / 2, c + u * w / 2 + v * d / 2, c - u * w / 2 + v * d / 2])
            cv2.fillPoly(occ, [np.round(to_g(poly)).astype(np.int32)], 1)
            x, z = L(*c); g = H(*c); burn = float(t_chay(c)[0]); ang = math.atan2(-u[1], u[0])
            y1 = g + int(RNG.choice([2, 3, 3])) * 2.8; die = 1666.0 + (245 + burn / 24) / 365.0 if burn >= 0 else 1800.0 + RNG.uniform(0, 60)
            m.box(x, z, w, d, ang, g, y1, jitter(COL['voi'] if RNG.random() < 0.6 else COL['go'], 14), jitter(COL['ngoi'], 12), (1500.0, die, g, burn), 1, 'gable', RNG.uniform(2.2, 3.4))
            n['1666'] += 1; n['lop_loi'] = n.get('lop_loi', 0) + 1
            if burn >= 0:
                reb = min(1667.3 + float(RNG.exponential(1.4)), 1672.0)
                m.box(x, z, w * 0.9, d * 0.9, ang, g, g + RNG.uniform(1.0, 3.0), jitter(COL['pheTich'], 14), jitter(COL['pheTich'], 14), (die, reb, g, burn), 2); n['phe_tich'] += 1
                m.box(x, z, w, d, ang, g, g + 2 * 3.0, jitter(COL['gach2'], 12), jitter(COL['ngoi_xam'], 10), (reb, 1850.0 + RNG.uniform(0, 90), g, -1.0), 3, 'gable', 2.0); n['xay_lai'] += 1
    n['trong_vung_chay'] = int(n['xay_lai'])
    return n

# ---------------------------------------------------------------- toà 2026 (OSM; thiếu cao độ → LiDAR DSM − DTM, trung vị 9 điểm)
def toa_2026(m, skip_names=("St Paul's Cathedral",)):
    n = 0; nl = 0
    for b in R['toa']:
        r = np.array(b['r'], float)
        if len(r) > 3 and np.allclose(r[0], r[-1]): r = r[:-1]
        if len(r) < 3: continue
        c = r.mean(0)
        if not (BB[0] + 30 < c[0] < BB[2] - 30 and BB[1] + 30 < c[1] < BB[3] - 30): continue
        if b['name'] in skip_names: continue
        area = 0.5 * abs(np.dot(r[:, 0], np.roll(r[:, 1], 1)) - np.dot(r[:, 1], np.roll(r[:, 0], 1)))
        if area < 12: continue
        g = H(*c)
        h = b['h']
        if not h:
            qs = np.array([c] + [c * 0.4 + p * 0.6 for p in r[:: max(1, len(r) // 8)]])
            hh = lidar(DSM, qs[:, 0], qs[:, 1]) - lidar(DTM, qs[:, 0], qs[:, 1]); h = float(np.clip(np.median(hh), 3.0, 320.0)); nl += 1
        y0 = g + (b['minh'] or 0.0) if b['part'] else g
        # vòng ngược kim đồng hồ trong (x, z)
        ring = [L(*p) for p in r]
        sa = sum(ring[i][0] * ring[(i + 1) % len(ring)][1] - ring[(i + 1) % len(ring)][0] * ring[i][1] for i in range(len(ring)))
        if sa > 0: ring = ring[::-1]
        tall = h > 60
        colw = jitter((150, 140, 126), 16) if not tall else jitter((104, 122, 138), 10)
        start = 1950.0 + RNG.uniform(0, 70)
        try:
            sd = int(str(b.get('start') or '')[:4]); start = float(sd)
        except Exception:
            pass
        if h > 120: start = max(start, 1995.0 + RNG.uniform(0, 30))
        start = max(start, 1667.5)   # toà OSM có start_date trước 1667 (vd. công trình còn lại) KHÔNG hiện trong cảnh 1666 — đã có bản thủ tục/công trình có tên
        m.prism(ring, y0, g + h, colw, jitter((120, 120, 118), 8), (start, 9999.0, y0, -1.0), 4)
        n += 1
    return n, nl

# ---------------------------------------------------------------- công trình có tên
def axis_of(name):
    for b in R['toa']:
        if b['name'] == name:
            r = np.array(b['r'], float); c = r.mean(0); X = r - c; w, V = np.linalg.eigh(X.T @ X); return c, V[:, 1], r
    return None
def st_pauls_wren(m):
    c, ax, _ = axis_of("St Paul's Cathedral"); ax = ax if ax[0] > 0 else -ax   # trục tây → đông
    ang = math.atan2(-ax[1], ax[0]); g = H(*c)
    cxz = L(*c); P = lambda u, v: (cxz[0] + math.cos(ang) * u - math.sin(ang) * v, cxz[1] + math.sin(ang) * u + math.cos(ang) * v)
    pc = COL['portland']; tl = (1675.5, 9999.0, g, -1.0)
    # nave + choir (158 m), transept (75 m), cao 30 m; tháp tây 2 × 64 m; trống + hàng cột 34→60 m; vòm tới 85 m; đèn lồng → 111 m (365 ft)
    def B(u, v, w, d, y0, y1, roof=None, rh=0, t=tl, col=pc):
        x, z = P(u, v); m.box(x, z, w, d, ang, g + y0, g + y1, jitter(col, 4), jitter(COL['chi'], 4), t, 5, roof, rh)
    B(0, 0, 150, 37, 0, 30, 'gable', 6, (1675.5, 9999, g, -1)); B(0, 0, 37, 75, 0, 30, 'gable', 6)
    B(-70, -15, 14, 14, 0, 50); B(-70, 15, 14, 14, 0, 50)
    for v in (-15, 15):
        x, z = P(-70, v); m.cyl(x, z, 5.0, 3.0, g + 50, g + 64, pc, tl, 5, 12)
    B(-80, 0, 8, 26, 0, 24)                                                    # portico tây
    x, z = P(5, 0); t2 = (1697.0, 9999, g, -1.0)
    m.cyl(x, z, 22.0, 22.0, g + 30, g + 46, pc, t2, 5, 32, cap=False)           # hàng cột trống
    m.cyl(x, z, 18.0, 18.0, g + 46, g + 58, pc, t2, 5, 32, cap=False)           # tầng gác (attic)
    t3 = (1708.8, 9999, g, -1.0)
    m.dome(x, z, 17.5, g + 58, 25.0, jitter(COL['chi'], 3), t3, 5, 32, 10)       # vòm (chì)
    m.cyl(x, z, 3.2, 3.2, g + 83, g + 98, pc, t3, 5, 12)                         # đèn lồng
    m.cyl(x, z, 3.2, 0.6, g + 98, g + 108, (200, 170, 90), t3, 5, 12)
    m.cyl(x, z, 1.2, 1.2, g + 108, g + 111, (210, 175, 80), t3, 5, 8)            # quả cầu + thập giá (111 m)
    return c
def st_pauls_old(m):
    """Old St Paul's (bậc 4: Hollar 1656–58, Met 2010.529; Relation 1666 a20: chóp mất 1561, chỉ tháp vuông). Nhà dài ≈ 179 m (586 ft) — số đo [cần kiểm]."""
    c, ax, _ = axis_of("St Paul's Cathedral"); ax = ax if ax[0] > 0 else -ax; ang = math.atan2(-ax[1], ax[0])
    c = c + ax * 8.0; g = H(*c); cxz = L(*c)
    P = lambda u, v: (cxz[0] + math.cos(ang) * u - math.sin(ang) * v, cxz[1] + math.sin(ang) * u + math.cos(ang) * v)
    burn = float(t_chay(c)[0]); die = 1666.0 + (245 + burn / 24) / 365.0
    st = COL['da']; tl = (1300.0, die, g, burn); tlr = (die, 1675.4, g, burn)
    def B(u, v, w, d, y0, y1, roof=None, rh=0, t=tl, col=st, colr=COL['chi']):
        x, z = P(u, v); m.box(x, z, w, d, ang, g + y0, g + y1, jitter(col, 6), jitter(colr, 6), t, 5, roof, rh)
    # kích thước: dài 586 ft ≈ 179 m, rộng thân + gian bên ≈ 100–104 ft ≈ 31 m (Wikipedia "Old St Paul's Cathedral" — [cần kiểm] nguồn tốt hơn: Dugdale 1658)
    B(0, 0, 176, 14, 0, 28, 'gable', 12)                     # thân giữa (nave + choir): rộng 14 m, tường 28 m, nóc 40 m
    B(0, -11.5, 170, 9, 0, 15, None); B(0, 11.5, 170, 9, 0, 15, None)   # gian bên ±(7…16) m, cao 15 m
    B(10, 0, 18, 88, 0, 28, 'gable', 12)                      # cánh ngang 88 m
    for u in range(-80, 90, 10):                              # trụ bay
        for v in (-16.5, 16.5): B(u, v, 2.0, 3.0, 0, 18 + (u % 20 == 0) * 2, None)
    B(10, 0, 24, 24, 0, 87, 'pyr', 4)                          # tháp vuông giao điểm (≈ 285 ft) [cần kiểm]
    for a, b in ((-12, -12), (12, -12), (12, 12), (-12, 12)):
        x, z = P(10 + a, b); m.cyl(x, z, 1.5, 0.2, g + 87, g + 95, st, tl, 5, 6)
    B(-92, 0, 6, 34, 0, 18, None)                              # portico Inigo Jones (thập niên 1630, a20)
    x, z = P(88.5, 0); m.cyl(x, z, 4.5, 4.5, g + 17, g + 17.6, COL['den'], tl, 5, 20)   # cửa sổ hoa hồng (mặt đông) — đĩa tối
    # phế tích sau 4/9/1666 (mái sập, a19): vỏ tường thấp + tháp cụt
    B(0, 0, 176, 32, 0, 18, None, t=tlr, col=COL['pheTich'], colr=COL['pheTich']); B(10, 0, 24, 24, 0, 55, None, t=tlr, col=COL['pheTich'], colr=COL['pheTich'])
    return c
def tower_of_london(m):
    c = np.array([533622.6, 180552.6]); g = H(*c); x, z = L(*c); tl = (1100.0, 9999.0, g, -1.0); st = COL['da']
    m.box(x, z, 36, 32, math.radians(-10), g, g + 27, jitter(st, 6), jitter(COL['chi'], 4), tl, 5)
    for a, b in ((-17, -15), (17, -15), (17, 15)):
        m.cyl(x + a, z + b, 3.0, 3.0, g + 27, g + 33, st, tl, 5, 10); m.cyl(x + a, z + b, 3.2, 0.5, g + 33, g + 36, COL['chi'], tl, 5, 10)
    m.cyl(x - 17, z + 15, 4.5, 4.5, g + 27, g + 33, st, tl, 5, 12)
    # tường thành trong/ngoài ≈ hình vuông 260 m và 200 m (bậc 1 vị trí: OSM tường còn) — sơ bộ
    for half, hh in ((120, 12), (95, 15)):
        pts = [(x - half, z - half), (x + half, z - half), (x + half, z + half), (x - half, z + half)]
        for i in range(4):
            (ax_, az), (bx, bz) = pts[i], pts[(i + 1) % 4]; L_ = math.hypot(bx - ax_, bz - az)
            m.box((ax_ + bx) / 2, (az + bz) / 2, L_, 3.5, math.atan2(bz - az, bx - ax_), g, g + hh, jitter(st, 6), jitter(st, 6), tl, 5)
            m.cyl(ax_, az, 6, 6, g, g + hh + 4, st, tl, 5, 10)
def monument(m):
    c = np.array([532990.0, 180750.0]); g = H(*c); x, z = L(*c); tl = (1671.5, 9999.0, g, -1.0)
    m.box(x, z, 8.5, 8.5, 0, g, g + 12, COL['portland'], COL['portland'], tl, 5)
    m.cyl(x, z, 2.4, 2.2, g + 12, g + 52, COL['portland'], (1672.5, 9999.0, g, -1.0), 5, 16)
    m.box(x, z, 5.0, 5.0, 0, g + 52, g + 55, COL['portland'], COL['portland'], (1676.5, 9999.0, g, -1.0), 5)
    m.cyl(x, z, 1.4, 0.4, g + 55, g + 61.5, (214, 170, 70), (1676.9, 9999.0, g, -1.0), 5, 10)   # bình lửa mạ vàng → 202 ft
def london_bridge_old(m):
    """Cầu London thời Trung cổ (1209–1831): 19 vòm, nhà trên cầu; khoảng trống phía bắc do cháy 13/2/1633 (Relation 1666 a23)."""
    a = np.array([532900.0, 180630.0]); b = np.array([532835.0, 180365.0]); g = 6.0
    u = (b - a) / np.linalg.norm(b - a); v = np.array([-u[1], u[0]]); Ln = np.linalg.norm(b - a); ang = math.atan2(-u[1], u[0])
    tl = (1209.0, 1831.5, 0.0, -1.0)
    x, z = L(*((a + b) / 2)); m.box(x, z, Ln, 12, ang, 4.5, g, jitter(COL['da'], 6), jitter(COL['da'], 6), tl, 7)
    for i in range(20):
        p = a + u * (i * Ln / 19); x, z = L(*p); m.box(x, z, 6, 14, ang, -3, 4.5, jitter(COL['da'], 6), jitter(COL['da'], 6), tl, 7)
    s = 0.0
    while s < Ln:
        w = RNG.uniform(5, 8)
        if not (30 < s < 95) and s < Ln - 10:          # khoảng trống 1633 ở đoạn bắc (vị trí trong đoạn: ước lượng, bậc 5)
            for side in (1, -1):
                p = a + u * (s + w / 2) + v * side * 4.5; x, z = L(*p)
                m.box(x, z, w * 0.95, 6.5, ang, g, g + RNG.uniform(9, 14), jitter(COL['voi'], 14), jitter(COL['ngoi'], 12), tl, 7, 'gable', 3)
        s += w
def tuong_thanh(m):
    """Tường thành Trung cổ: Tower → Aldgate → Bishopsgate → Moorgate → Cripplegate → Aldersgate → Newgate → Ludgate → sông (vị trí cổng = điểm khớp OSM; đoạn nối ước lượng)."""
    pts = [(533560, 180700), (533590, 180950), (533540, 181160), (533380, 181330), (533196, 181431), (532900, 181530), (532697, 181548), (532450, 181610), (532300, 181620), (532170, 181520),
           (532145, 181465), (531900, 181430), (531796, 181409), (531780, 181280), (531760, 181158), (531700, 181000), (531660, 180830)]
    tl = (1200.0, 1766.0, 0.0, -1.0)
    for i in range(len(pts) - 1):
        a, b = np.array(pts[i], float), np.array(pts[i + 1], float); c = (a + b) / 2; g = H(*c); x, z = L(*c)
        m.box(x, z, np.linalg.norm(b - a), 2.6, math.atan2(-(b - a)[1], (b - a)[0]), g, g + 7, jitter(COL['da'], 8), jitter(COL['da'], 8), tl, 6)
    for nm, E, N in [('Aldgate', 533540, 181160), ('Bishopsgate', 533196, 181431), ('Moorgate', 532697, 181548), ('Cripplegate', 532330, 181620), ('Aldersgate', 532145, 181465), ('Newgate', 531796, 181409), ('Ludgate', 531760, 181158)]:
        g = H(E, N); x, z = L(E, N); m.box(x, z, 14, 10, 0, g, g + 13, jitter(COL['da'], 8), jitter(COL['chi'], 6), tl, 6, 'gable', 3)
def nha_tho(m):
    """Tháp nhà thờ giáo xứ: vị trí = nhà thờ OSM trong vùng (Wren dựng lại trên nền cũ — bậc 5 cho tháp 1666, bậc 3 vị trí). 1666: tháp đá vuông + chóp nhỏ; 1670–1700: tháp/chóp Wren đá Portland."""
    seen = set(); n = 0
    for d in R['diem']:
        if d['k'] != 'place_of_worship' or d['name'] in seen: continue
        E, N = d['p']
        if not (531100 < E < 533700 and 180550 < N < 181750): continue
        if "Paul" in d['name'] and 'Cathedral' in d['name']: continue
        seen.add(d['name']); g = H(E, N); x, z = L(E, N); burn = float(t_chay([E, N])[0])
        die = 1666.0 + (245 + burn / 24) / 365.0 if burn >= 0 else 1900.0
        th = RNG.uniform(22, 34)
        m.box(x, z, 7, 7, 0, g, g + th, jitter(COL['da'], 8), jitter(COL['chi'], 6), (1300.0, die, g, burn), 8, 'pyr', RNG.uniform(3, 10))
        if burn >= 0:
            m.box(x, z, 7, 7, 0, g, g + th * 0.6, jitter(COL['pheTich'], 8), jitter(COL['pheTich'], 8), (die, 1672.0, g, burn), 2)
            t0 = 1670.0 + RNG.uniform(0, 30)
            m.box(x, z, 6.5, 6.5, 0, g, g + th, jitter(COL['portland'], 5), jitter(COL['portland'], 5), (t0, 9999.0, g, -1.0), 9)
            m.cyl(x, z, 2.5, 0.3, g + th, g + th + RNG.uniform(10, 25), jitter(COL['portland'], 5) if RNG.random() < 0.6 else COL['chi'], (t0 + 3, 9999.0, g, -1.0), 9, 8)
        n += 1
    return n
def cau_2026(m):
    n = 0
    for d in R['duong']:
        if d.get('bridge') == 'yes' and d['hw'] in ('trunk', 'primary', 'secondary', 'tertiary', 'footway', 'rail') and d['name'] in ('London Bridge', 'Southwark Bridge', 'Blackfriars Bridge', 'Millennium Bridge', 'Cannon Street Railway Bridge', 'Tower Bridge') or (d.get('bridge') == 'yes' and d['hw'] == 'rail'):
            l = np.array(d['l'], float)
            if not at(WAT26, l.mean(0)): continue
            t0 = {'London Bridge': 1973.0, 'Southwark Bridge': 1921.0, 'Blackfriars Bridge': 1869.0, 'Millennium Bridge': 2000.0}.get(d['name'], 1866.0)
            for i in range(len(l) - 1):
                a, b = l[i], l[i + 1]; c = (a + b) / 2; x, z = L(*c)
                m.box(x, z, np.linalg.norm(b - a) + 0.5, 14 if d['hw'] != 'footway' else 4, math.atan2(-(b - a)[1], (b - a)[0]), 5.0, 8.0, (150, 150, 146), (120, 120, 118), (t0, 9999.0, 0.0, -1.0), 7)
            n += 1
    return n

def main():
    meta = {'goc_EN': [E0, N0], 'bbox': BB, 'bac': {}}
    T = dia_hinh(); meta['dia_hinh'] = {k: T[k] for k in ('nx', 'nz', 'x0', 'z0', 'step')}
    m = M(); streets = pho_1666(); meta['pho_1666'] = len(streets)
    meta['nha'] = nha_1666(m, streets); meta['bac']['nha_1666'] = '5 (lô theo phố OSM còn giữ + mặt nạ nét dày Doornick bậc 1; kiểu nhà bậc 4–5)'
    meta['toa_2026'], meta['toa_2026_lidar'] = toa_2026(m); meta['bac']['toa_2026'] = '1 (OSM ODbL + LiDAR EA OGL)'
    c_new = st_pauls_wren(m); c_old = st_pauls_old(m); tower_of_london(m); monument(m); london_bridge_old(m); tuong_thanh(m)
    meta['nha_tho'] = nha_tho(m); meta['cau_2026'] = cau_2026(m)
    meta['st_pauls_EN'] = c_new.tolist(); meta['old_st_pauls_EN'] = c_old.tolist()
    P, C, TL, Kk = m.arr(); meta['dinh'] = len(P); meta['tam_giac'] = len(P) // 3
    meta['diem_chay'] = [{'ten': t[0], 'EN': [t[1], t[2]], 'gio': t[3], 'luat': t[4]} for t in TC]
    with open(os.path.join(OUT, 'ldn.bin'), 'wb') as f:
        off = 0; lay = {}
        for nm, a in (('pos', P), ('col', C), ('tl', TL), ('k', Kk), ('h26', T['h26']), ('h66', T['h66']), ('xanh', T['xanh'])):
            b = np.ascontiguousarray(a).tobytes(); lay[nm] = {'off': off, 'len': len(b), 'dtype': str(a.dtype), 'shape': list(a.shape)}; f.write(b); off += len(b)
            pad = (-off) % 4; f.write(b'\0' * pad); off += pad
    meta['bo_cuc'] = lay
    meta['sha256_bin'] = hashlib.sha256(open(os.path.join(OUT, 'ldn.bin'), 'rb').read()).hexdigest()
    # lưới thời gian cháy 20 m (cho bản đồ hoạt hoá + lửa sprite)
    es = np.arange(531000, 533800, 20.0); ns = np.arange(181800, 180500, -20.0); EE, NN = np.meshgrid(es, ns)
    tg = t_chay(np.stack([EE.ravel(), NN.ravel()], 1)).reshape(EE.shape)
    meta['luoi_chay'] = {'E0': 531000, 'N0': 181800, 'buoc': 20, 'nx': len(es), 'nz': len(ns)}
    np.save(os.path.join(OUT, 'luoi_chay.npy'), tg.astype(np.float32)); tg.astype('<f4').tofile(os.path.join(OUT, 'luoi_chay.f32'))
    json.dump(meta, open(os.path.join(OUT, 'ldn.json'), 'w'), ensure_ascii=False, indent=1)
    print(json.dumps({k: meta[k] for k in ('pho_1666', 'nha', 'toa_2026', 'toa_2026_lidar', 'nha_tho', 'cau_2026', 'dinh', 'tam_giac')}, ensure_ascii=False))
if __name__ == '__main__': main()
