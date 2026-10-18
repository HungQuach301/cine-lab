"""PT3 · đường bay + vùng dựng của hai cú máy (thuần Python — dùng chung cho Blender và cho bộ đo/chiếu ngược).
Toạ độ cục bộ m (Đông, Bắc, Lên), gốc = máy neo PT (mép Main Street, Commercial Square) — xem pt_site.py.
  street: bay cận dọc Main Street 1943 từ Commercial Square xuống nam, 8 s @24 fps, cao 55 → 22 m (tim phố đo từ ghost 1943: khoảng trống giữa hai dãy toà).
  kb:     orbit King's Bastion 1782 (footprint OSM way 952588383 + 256821558), 6 s @24 fps, bán kính 95 m, cao 34 m, quét phương vị 200° → 340°."""
import math

FPS = 24

def _cr(p0, p1, p2, p3, t):
    t2, t3 = t * t, t * t * t
    return [0.5 * (2 * b + (-a + c) * t + (2 * a - 5 * b + 4 * c - d) * t2 + (-a + 3 * b - 3 * c + d) * t3) for a, b, c, d in zip(p0, p1, p2, p3)]

def spline(pts, s):
    """Catmull-Rom qua các điểm (đầu/cuối nhân đôi), s ∈ [0, 1]."""
    n = len(pts) - 1; s = min(max(s, 0.0), 1.0) * n; i = min(int(s), n - 1); t = s - i
    P = [pts[0]] + pts + [pts[-1]]
    return _cr(P[i], P[i + 1], P[i + 2], P[i + 3], t)

def ease(s):   # dịu đầu/cuối nhẹ (tốc độ không về 0)
    return 0.12 * (3 * s * s - 2 * s * s * s) + 0.88 * s

# tim Main Street 1943 (đo từ ghost: giữa khoảng trống hai dãy toà) — dùng cho vùng chi tiết
TRACK_STREET = [(-2.0, -20.0), (-11.5, -50.0), (-15.5, -80.0), (-24.0, -110.0), (-30.0, -135.0), (-25.0, -160.0), (-18.5, -190.0), (-18.0, -240.0)]
KBC = (-158.0, -133.0)

SITE = {
    'street': {'N': 192, 'mm': 26.0, 'track': TRACK_STREET, 'detail_d': 75.0, 'keep_d': 340.0,
               'pos': [(-3.0, -12.0, 55.0), (-9.0, -45.0, 46.0), (-16.0, -82.0, 36.0), (-24.0, -116.0, 28.0), (-26.0, -146.0, 23.5), (-21.0, -172.0, 22.0)],
               'look': [(-24.0, -112.0, 0.0), (-28.0, -140.0, 0.0), (-28.0, -165.0, 1.0), (-22.0, -195.0, 2.0), (-19.0, -225.0, 3.0), (-18.0, -250.0, 4.0)],
               'ground': (-125.0, -620.0, 300.0, 260.0),
               'top_rect': (-75.0, -262.0, 43.0, 5.0), 'top_bids': None, 'ppm_elev': 64, 'ppm_top': 24},
    'kb': {'N': 144, 'mm': 30.0, 'track': [KBC], 'detail_d': 150.0, 'keep_d': 330.0, 'orbit': {'c': KBC, 'r': 95.0, 'h': 34.0, 'a0': 200.0, 'a1': 340.0, 'look_z': 1.0},
           'proj_az': [245.0, 270.0, 295.0],   # HC8: 3 tấm C ở góc máy chính ±25°
           'ground': (-125.0, -420.0, 260.0, 160.0),
           'top_rect': (-198.0, -198.0, -108.0, -68.0), 'top_bids': [8000], 'ppm_elev': 80, 'ppm_top': 16},
}

def dist_path(site, x, y):
    tr = site['track']
    if len(tr) == 1: return math.hypot(x - tr[0][0], y - tr[0][1])
    best = 1e18
    for (ax, ay), (bx, by) in zip(tr[:-1], tr[1:]):
        dx, dy = bx - ax, by - ay; L2 = dx * dx + dy * dy; t = max(0.0, min(1.0, ((x - ax) * dx + (y - ay) * dy) / L2))
        best = min(best, math.hypot(x - ax - t * dx, y - ay - t * dy))
    return best

def orbit_cam(site, az):
    o = site['orbit']; a = math.radians(az)
    pos = (o['c'][0] + o['r'] * math.sin(a), o['c'][1] + o['r'] * math.cos(a), o['h'])
    return pos, (o['c'][0], o['c'][1], o['look_z'])

def cam_at(name, f):
    """(vị trí, điểm nhìn, mm) của khung f (0..N-1)."""
    st = SITE[name]; s = f / (st['N'] - 1)
    if name == 'kb':
        o = st['orbit']; az = o['a0'] + (o['a1'] - o['a0']) * ease(s); p, l = orbit_cam(st, az); return p, l, st['mm']
    s = ease(s); return tuple(spline(st['pos'], s)), tuple(spline(st['look'], s)), st['mm']

def az_at(f):
    o = SITE['kb']['orbit']; return o['a0'] + (o['a1'] - o['a0']) * ease(f / (SITE['kb']['N'] - 1))

def basis(pos, look):
    """hệ máy: f (nhìn tới), r (phải), u (lên) — lăn = 0."""
    f = [l - p for l, p in zip(look, pos)]; n = math.sqrt(sum(c * c for c in f)); f = [c / n for c in f]
    r = [f[1], -f[0], 0.0]; n = math.sqrt(sum(c * c for c in r)); r = [c / n for c in r]
    u = [r[1] * f[2] - r[2] * f[1], r[2] * f[0] - r[0] * f[2], r[0] * f[1] - r[1] * f[0]]
    return f, r, u

def blender_rot(pos, look):
    """Euler XYZ cho máy Blender (nhìn −Z, lên +Y) nhìn từ pos tới look."""
    f, r, u = basis(pos, look)
    yaw = math.atan2(f[1], f[0]); pitch = math.asin(max(-1, min(1, f[2])))
    return (math.pi / 2 + pitch, 0.0, yaw - math.pi / 2)

def project(pos, look, mm, W, H, P, sensor=36.0):
    """điểm thế giới P → (x px, y px, độ sâu dọc trục) theo máy phối cảnh Blender (cảm biến khớp chiều ngang)."""
    f, r, u = basis(pos, look); d = [P[i] - pos[i] for i in range(3)]
    z = sum(d[i] * f[i] for i in range(3)); xr = sum(d[i] * r[i] for i in range(3)); yu = sum(d[i] * u[i] for i in range(3))
    fpx = mm / sensor * W
    return W / 2 + fpx * xr / z, H / 2 - fpx * yu / z, z
