"""PT · khung neo Grand Parade / Commercial Square (nay John Mackintosh Sq.), Gibraltar.
Đọc ghost SH (1782, 1943 — chỉ đọc), đổi sang toạ độ cục bộ (m, Đông-Bắc-Lên) gốc = điểm chân máy. Thuần Python (dùng được cả trong bpy)."""
import json, math, os
HERE = os.path.dirname(os.path.abspath(__file__))
# máy neo: góc đông-nam quảng trường, mép Main Street; nhìn tây-tây-bắc qua quảng trường ra Line Wall và vịnh
# PT2 (18/10): nhiều máy neo, chọn bằng biến môi trường PT_CAM (mặc định 'pt' = máy PT, kết quả PT không đổi)
CAMS = {
    # PT: mép nam dãy nhà phía bắc quảng trường (cách mặt tiền ~6 m), sát Main Street; 1943 = khung neo Commercial Square của PT2
    'pt': dict(E=288244.6, N=4002145.8, H=4.6, HEAD=281.0, PITCH=2.0, MM=32.0),
    # PT2 góc mới 1782: hẻm giữa khối Drinkwater K1782-09 (nam) và K1782-10 (bắc), rộng 7–8 m theo bản nắn, đầu đông sát Main Street,
    # nhìn tây dọc hẻm ra Line Wall (toạ độ đã tính SHIFT 1782 +6 m Đông); trục hẻm lệch nam 1,3° so với hướng tây
    'k1782': dict(E=288237.2, N=4002030.7, H=3.4, HEAD=268.7, PITCH=1.0, MM=30.0),
}
CAMK = os.environ.get('PT_CAM', 'pt')
_C = CAMS[CAMK]
CAM_E, CAM_N = _C['E'], _C['N']
CAM_H = _C['H']        # m trên mặt đường (trong dải 2–10 m của lệnh)
CAM_HEAD = _C['HEAD']  # độ, theo phương vị (0 = Bắc, 90 = Đông)
CAM_PITCH = _C['PITCH']   # độ ngẩng lên
CAM_MM, SENSOR = _C['MM'], 36.0
GHOST = os.environ.get('PT_GHOST', '/var/tmp/pt/ghost')

def utm(lon, lat, zone=30):
    a = 6378137.0; f = 1 / 298.257223563; k0 = 0.9996; e2 = f * (2 - f); ep2 = e2 / (1 - e2)
    lon0 = math.radians((zone - 1) * 6 - 180 + 3); phi = math.radians(lat); lam = math.radians(lon)
    N = a / math.sqrt(1 - e2 * math.sin(phi) ** 2); T = math.tan(phi) ** 2; C = ep2 * math.cos(phi) ** 2; A = math.cos(phi) * (lam - lon0)
    M = a * ((1 - e2 / 4 - 3 * e2 ** 2 / 64 - 5 * e2 ** 3 / 256) * phi - (3 * e2 / 8 + 3 * e2 ** 2 / 32 + 45 * e2 ** 3 / 1024) * math.sin(2 * phi)
             + (15 * e2 ** 2 / 256 + 45 * e2 ** 3 / 1024) * math.sin(4 * phi) - (35 * e2 ** 3 / 3072) * math.sin(6 * phi))
    E = k0 * N * (A + (1 - T + C) * A ** 3 / 6 + (5 - 18 * T + T * T + 72 * C - 58 * ep2) * A ** 5 / 120) + 500000
    Nn = k0 * (M + N * math.tan(phi) * (A * A / 2 + (5 - T + 9 * C + 4 * C * C) * A ** 4 / 24 + (61 - 58 * T + T * T + 600 * C - 330 * ep2) * A ** 6 / 720))
    return E, Nn

def local(lon, lat):
    E, N = utm(lon, lat); return (E - CAM_E, N - CAM_N)

def rings(geom):
    t = geom['type']
    if t == 'Polygon': return [geom['coordinates'][0]]
    if t == 'MultiPolygon': return [c[0] for c in geom['coordinates']]
    if t == 'LineString': return [geom['coordinates']]
    if t == 'MultiLineString': return list(geom['coordinates'])
    return []

# 1782: khối Drinkwater nắn affine RMS 21,2 m (LOO 33,3; SH §2.1) — ở Grand Parade mép Main Street lệch tây ~6 m so với OSM/AMS
# → dời khối 1782 +6 m Đông để tim Main Street hai mốc trùng nhau (trong sai số nắn; ghi trong báo cáo PT §4).
SHIFT = {1782: (6.0, 0.0)}

def load(year, kinds=None, R=260.0):
    out = []
    for f in json.load(open(f'{GHOST}/ghost-{year}.geojson'))['features']:
        p = f['properties']
        if kinds and p.get('loai') not in kinds: continue
        for r in rings(f['geometry']):
            dx, dy = SHIFT.get(year, (0.0, 0.0)); pts = [(x + dx, y + dy) for x, y in (local(*c[:2]) for c in r)]
            if len(pts) > 1 and pts[0] == pts[-1]: pts = pts[:-1]
            if min(math.hypot(x, y) for x, y in pts) > R: continue
            out.append({'id': p.get('id'), 'loai': p.get('loai'), 'tang': p.get('so_tang_uoc'), 'do_tin': p.get('do_tin'), 'pts': pts,
                        'line': f['geometry']['type'].endswith('LineString')})
    return out

def area(pts):
    return 0.5 * sum(pts[i][0] * pts[(i + 1) % len(pts)][1] - pts[(i + 1) % len(pts)][0] * pts[i][1] for i in range(len(pts)))

def inside(x, y, pts):
    c = False; n = len(pts)
    for i in range(n):
        x1, y1 = pts[i]; x2, y2 = pts[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1 + 1e-12) + x1: c = not c
    return c

def cam_dir():
    h = math.radians(CAM_HEAD); return (math.sin(h), math.cos(h))
