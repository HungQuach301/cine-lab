#!/opt/cine/bin/python
"""KÊNH 2 · nền BẢN ĐỒ ĐỊA HÌNH NỔI cho module k2v `relief/map` (phiên V2, 14/10/2026).

Dữ liệu (tài sản công, không commit — cache ngoài git, SHA ghi vào <out>/meta.json + scripts/k2/k2v-assets.sha.json khi --pin):
  - DEM: USGS 3DEP 1 arc-second (ô 1°×1°, GeoTIFF, prd-tnm.s3.amazonaws.com) — tác phẩm chính phủ Mỹ, tài sản công.
  - Vector: Natural Earth 1:10m (hồ, đại dương, sông, ranh bang/tỉnh) — tài sản công.
Ra (<cache>/relief/<tên>/):
  natural.jpg  bảng màu TỰ NHIÊN (hiện tại): tô bóng nhiều hướng × màu độ cao, nước có dải bờ, sông
  sepia.jpg    bảng màu SEPIA (quá khứ): giấy cũ, mực nâu, đường viền nước kiểu bản đồ khắc
  height.f32   lưới độ cao (m, float32 LE, hàng từ Bắc xuống) cho lưới 3D; nước = mặt nước
  routes.json  tuyến từ Natural Earth (vd. 'Erie Canal' + 'Hudson') đã nối, [lon, lat]
  meta.json    bbox, kích thước, SHA nguồn, giấy phép
Dùng:
  relief_build.py build --name erie --bbox -81,39,-72,45 [--ppd 600] [--mesh 5]
  relief_build.py build --name korea --bbox 125,33.5,130.5,38.7 --dem skadi [--coast dem]   (T2: ngoài Mỹ — SRTM 1", USGS, tài sản công; --coast dem = bờ suy từ DEM)
  (T2 G1b: ppd cao (1800) cho shot tầm 5–20 km: hằng số vẽ quy theo ppd/600, mặt nạ nước làm mượt, mesh giữ cỡ bằng --mesh lớn hơn; ppd phải chia hết 3600)
"""
import hashlib, json, math, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage

CACHE = os.environ.get('K2V_CACHE', '/var/tmp/cine-out/k2v-cache')
DEM = os.path.join(CACHE, 'dem'); NE = os.path.join(CACHE, 'ne')
URL3DEP = 'https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/current/{t}/USGS_1_{t}.tif'
NEURL = 'https://naciscdn.org/naturalearth/10m/{k}/{n}.zip'
NEFILES = [('physical', 'ne_10m_lakes'), ('physical', 'ne_10m_lakes_north_america'), ('physical', 'ne_10m_ocean'), ('physical', 'ne_10m_rivers_lake_centerlines'),
           ('physical', 'ne_10m_rivers_north_america'), ('physical', 'ne_10m_land'), ('cultural', 'ne_10m_admin_1_states_provinces_lakes')]


def arg(k, d=None):
    return sys.argv[sys.argv.index('--' + k) + 1] if '--' + k in sys.argv else d


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()


def fetch(url, dst):
    if os.path.exists(dst) and os.path.getsize(dst) > 0: return True
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    r = subprocess.run(['curl', '-s', '-f', '-m', '900', '-o', dst + '.part', url])
    if r.returncode: return False
    os.replace(dst + '.part', dst); return True


def tiles(b):
    lon0, lat0, lon1, lat1 = b
    for n in range(int(math.floor(lat0)) + 1, int(math.ceil(lat1)) + 1):
        for w in range(int(math.ceil(-lon0)), int(math.ceil(-lon1)) - 1, -1):
            yield n, w, f'n{n:02d}w{w:03d}'


URLSKADI = 'https://s3.amazonaws.com/elevation-tiles-prod/skadi/{d}/{t}.hgt.gz'   # T2 (K2C-T2-01): ngoài Mỹ — SRTM 1" (USGS, tài sản công) qua AWS Terrain Tiles


def mosaic_skadi(b, ppd):
    """ô SRTM 1" dạng HGT (3601 px, int16 big-endian; ô biển/thiếu = NaN) → lưới ppd điểm/độ. Dùng cho vùng ngoài nước Mỹ (--dem skadi)."""
    import gzip
    lon0, lat0, lon1, lat1 = b; W, H = round((lon1 - lon0) * ppd), round((lat1 - lat0) * ppd); Z = np.full((H, W), np.nan, np.float32); k = 3600 // ppd; src = {}
    for la in range(int(math.floor(lat0)), int(math.ceil(lat1))):
        for lo in range(int(math.floor(lon0)), int(math.ceil(lon1))):
            d = f"{'N' if la >= 0 else 'S'}{abs(la):02d}"; t = d + f"{'E' if lo >= 0 else 'W'}{abs(lo):03d}"; f = os.path.join(DEM, 'skadi', t + '.hgt.gz')
            if not fetch(URLSKADI.format(d=d, t=t), f): print('  (không có ô)', t); continue
            a = np.frombuffer(gzip.open(f).read(), dtype='>i2').astype(np.float32); n = int(round(math.sqrt(a.size))); a = a.reshape(n, n)[:3600, :3600]; a[a < -1000] = np.nan
            if n != 3601: print('  (ô SRTM không phải 1", bỏ)', t, n); continue
            a = np.nanmean(a.reshape(ppd, k, ppd, k), axis=(1, 3)) if k > 1 else a
            x0, y0 = round((lo - lon0) * ppd), round((lat1 - (la + 1)) * ppd)
            xs, ys = slice(max(0, x0), min(W, x0 + ppd)), slice(max(0, y0), min(H, y0 + ppd))
            if xs.start < xs.stop and ys.start < ys.stop: Z[ys, xs] = a[ys.start - y0:ys.stop - y0, xs.start - x0:xs.stop - x0]
            src[t] = sha(f)
    return Z, src


def mosaic(b, ppd):
    """ô 3DEP 1" (3612 px, đệm 6 px) → lưới ppd điểm/độ bằng trung bình khối; ô thiếu (biển) = NaN"""
    import tifffile
    lon0, lat0, lon1, lat1 = b; W, H = round((lon1 - lon0) * ppd), round((lat1 - lat0) * ppd); Z = np.full((H, W), np.nan, np.float32); k = 3600 // ppd; src = {}
    for n, w, t in tiles(b):
        f = os.path.join(DEM, t + '.tif')
        if not fetch(URL3DEP.format(t=t), f): print('  (không có ô)', t); continue
        a = tifffile.imread(f).astype(np.float32)
        if a.shape != (3612, 3612): print('  (ô lệch cỡ, đệm NaN)', t, a.shape); a = np.pad(a, ((0, max(0, 3612 - a.shape[0])), (0, max(0, 3612 - a.shape[1]))), constant_values=np.nan)[:3612, :3612]   # T2: vài ô ven biển 3DEP không đủ 3612 px
        a = a[6:3606, 6:3606]; a[a < -1000] = np.nan
        a = np.nanmean(a.reshape(ppd, k, ppd, k), axis=(1, 3)) if k > 1 else a
        x0, y0 = round((-w - lon0) * ppd), round((lat1 - n) * ppd)
        xs, ys = slice(max(0, x0), min(W, x0 + ppd)), slice(max(0, y0), min(H, y0 + ppd))
        Z[ys, xs] = a[ys.start - y0:ys.stop - y0, xs.start - x0:xs.stop - x0]; src[t] = sha(f)
    return Z, src


class Proj:
    def __init__(s, b, W, H): s.b, s.W, s.H = b, W, H
    def __call__(s, lon, lat):
        lon0, lat0, lon1, lat1 = s.b; return ((lon - lon0) / (lon1 - lon0) * s.W, (lat1 - lat) / (lat1 - lat0) * s.H)


def shapes(name, b, kind=None):
    import shapefile
    for k, n in NEFILES:
        if n == name: z = os.path.join(NE, n + '.zip'); fetch(NEURL.format(k=k, n=n), z); d = os.path.join(NE, n)
    if not os.path.isdir(d): subprocess.run(['unzip', '-o', '-q', z, '-d', d], check=True)
    r = shapefile.Reader(os.path.join(d, name), encoding='latin1'); lon0, lat0, lon1, lat1 = b
    for sr in r.iterShapeRecords():
        P = sr.shape.points
        if not P: continue
        xs = [p[0] for p in P]; ys = [p[1] for p in P]
        if max(xs) < lon0 - 1 or min(xs) > lon1 + 1 or max(ys) < lat0 - 1 or min(ys) > lat1 + 1: continue
        parts = list(sr.shape.parts) + [len(P)]
        yield sr.record.as_dict(), [P[parts[i]:parts[i + 1]] for i in range(len(parts) - 1)]


def poly_mask(name, b, W, H, filt=None):
    pr = Proj(b, W, H); im = Image.new('L', (W, H), 0); d = ImageDraw.Draw(im)
    for rec, rings in shapes(name, b):
        if filt and not filt(rec): continue
        # shapefile: vòng theo chiều kim đồng hồ = vòng ngoài, ngược chiều = lỗ (đảo trong hồ)
        import shapefile
        for ring in sorted(rings, key=lambda r: shapefile.signed_area(r) >= 0):
            if len(ring) > 2: d.polygon([pr(*p) for p in ring], fill=0 if shapefile.signed_area(ring) >= 0 else 255)
    return np.array(im) > 127


def lines(name, b, W, H, filt=None):
    pr = Proj(b, W, H); out = []
    for rec, parts in shapes(name, b):
        if filt and not filt(rec): continue
        for P in parts: out.append((rec, [pr(*p) for p in P], P))
    return out


def hillshade(Z, b, ppd, zf=1.0):
    """tô bóng nhiều hướng (Mark 1992 / USGS): 4 phương vị có trọng số, độ cao mặt trời 45°"""
    lat0, lat1 = b[1], b[3]; H, W = Z.shape
    lat = lat1 - (np.arange(H) + 0.5) / ppd; dx = (111320 * np.cos(np.radians(lat)) / ppd)[:, None]; dy = 110570 / ppd
    gy, gx = np.gradient(Z * zf); gx = gx / dx; gy = -gy / dy   # gy dương = dốc lên về phía Bắc
    slope = np.arctan(np.hypot(gx, gy)); asp = np.arctan2(-gx, -gy)   # hướng dốc xuống (phương vị pháp tuyến)
    alt = np.radians(45); acc = 0; wsum = 0
    for az, w in ((315, 0.5), (270, 0.2), (360, 0.15), (225, 0.15)):
        a = np.radians(az); s = np.sin(alt) * np.cos(slope) + np.cos(alt) * np.sin(slope) * np.cos(a - asp)
        acc = acc + w * s; wsum += w
    return np.clip(acc / wsum, 0, 1), slope


def ramp(stops, x):
    xs = np.array([s[0] for s in stops], np.float32); cs = np.array([s[1] for s in stops], np.float32) / 255
    return np.stack([np.interp(x, xs, cs[:, i]) for i in range(3)], -1)


def hexrgb(h): h = h.lstrip('#'); return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], np.float32) / 255


def draw_lines(img, L, color, wfn, scale=1.0):
    d = ImageDraw.Draw(img, 'RGBA')
    for rec, pts, _ in L:
        w = max(1, round(wfn(rec) * scale))
        if len(pts) > 1: d.line(pts, fill=color, width=w, joint='curve')


def build():
    name = arg('name'); b = [float(x) for x in arg('bbox').split(',')]; ppd = int(arg('ppd', 600)); mk = int(arg('mesh', 5))
    out = os.path.join(CACHE, 'relief', name); os.makedirs(out, exist_ok=True)
    SK = arg('dem', '3dep') == 'skadi'
    print('[relief] ghép DEM', 'SRTM 1" (skadi)…' if SK else '3DEP 1"…'); Z, src = (mosaic_skadi if SK else mosaic)(b, ppd); H, W = Z.shape
    print('[relief] mặt nạ nước Natural Earth 10m…')
    ocean = poly_mask('ne_10m_ocean', b, W, H)
    if arg('coast', 'ne') == 'dem':   # T2 G1b: đường bờ suy từ DEM (ô ≤ 0 m hoặc trống, nối với biển Natural Earth) — bỏ dải lệch bờ NE 10m ↔ SRTM/3DEP ở tầm < 50 km
        sea = np.isnan(Z) | (Z <= 0.0); lab, n = ndimage.label(sea)
        keep = np.unique(lab[ocean & sea]); keep = keep[keep > 0]
        dem_ocean = np.isin(lab, keep)
        print(f'[relief] bờ từ DEM: {int(dem_ocean.sum())} ô biển (NE: {int(ocean.sum())}), lệch {int((dem_ocean ^ ocean).sum())} ô')
        ocean = dem_ocean
    lakes = poly_mask('ne_10m_lakes', b, W, H) | poly_mask('ne_10m_lakes_north_america', b, W, H)
    water = ocean | lakes | np.isnan(Z)
    u = ppd / 600.0   # T2 G1b: hằng số vẽ (px) thiết kế ở ppd 600 → quy theo ppd để nền độ phân giải cao giữ cùng dáng theo km
    if u > 1.01:   # mép nước: làm mượt mặt nạ nhị phân (σ ~ 0,6 px) rồi lấy ngưỡng — bỏ răng cưa bậc thang 1 ô khi máy ở tầm < 20 km
        sm = lambda m: ndimage.gaussian_filter(m.astype(np.float32), 0.6 * u) > 0.5
        ocean, lakes = sm(ocean), sm(lakes) & ~sm(ocean); water = ocean | lakes | np.isnan(Z)
    Zf = np.where(np.isnan(Z), 0, Z)
    # mặt hồ phẳng: độ cao trung vị của DEM trong hồ (hồ lớn ~75 m Ontario, ~174 m Erie); biển 0
    lab, nl = ndimage.label(lakes & ~ocean)
    if nl:
        med = ndimage.median(Zf, lab, index=np.arange(1, nl + 1)); Zf = np.where(lab > 0, np.take(np.concatenate([[0], med]), lab), Zf)
    Zf = np.where(ocean, 0, Zf).astype(np.float32)
    land = ~water
    hs, slope = hillshade(np.where(water, ndimage.grey_dilation(Zf, 3), Zf), b, ppd, zf=float(arg('zf', 2.2)))
    hs = np.where(water, 0.75, hs)
    dist_in = ndimage.distance_transform_edt(water) / u   # khoảng cách từ bờ vào nước (px ở ppd 600)
    dist_out = ndimage.distance_transform_edt(land) / u
    E = np.clip(Zf / 1000.0, 0, 2)   # km
    R = np.random.default_rng(7); fibn = ndimage.gaussian_filter(R.standard_normal((H, W)).astype(np.float32), 3 * u) * 3 * u
    print('[relief] bảng màu tự nhiên…')
    hyp = ramp([(0.0, (104, 140, 92)), (0.12, (121, 152, 98)), (0.25, (150, 168, 112)), (0.45, (181, 176, 128)), (0.7, (196, 178, 140)), (1.0, (214, 202, 176)), (1.6, (236, 232, 222))], E)
    shade = (0.35 + 0.95 * hs)[..., None]; nat = hyp * shade
    nat = nat * (1 - 0.10 * np.clip(slope * 4, 0, 1))[..., None]
    deep = hexrgb('#3f6f93'); shal = hexrgb('#8fb7cf'); wt = np.clip(dist_in / 28.0, 0, 1)[..., None] ** 0.7
    wcol = shal * (1 - wt) + deep * wt; wcol = wcol * (1 + 0.02 * fibn[..., None])
    nat = np.where(water[..., None], wcol, nat)
    shore = np.clip(1 - dist_out / 2.5, 0, 1) * land; nat = nat * (1 - 0.25 * shore)[..., None]
    nat_im = Image.fromarray((np.clip(nat, 0, 1) * 255).astype(np.uint8))
    print('[relief] bảng màu sepia…')
    R = np.random.default_rng(7); fib = ndimage.gaussian_filter(R.standard_normal((H, W)).astype(np.float32), 1.2) * 0.5 + ndimage.gaussian_filter(R.standard_normal((H, W)).astype(np.float32), 9 * u) * 2.0 * u
    paper = hexrgb('#e6d3a8')[None, None] * (1 + 0.035 * fib[..., None]); ink = hexrgb('#4a3220')
    k = np.clip(1.10 - 1.2 * hs, 0, 1) ** 1.0; k = 0.86 * k + 0.20 * np.clip(E / 1.1, 0, 1) ** 0.8
    sep = paper * (1 - k[..., None]) + ink * k[..., None] * 1.0 + paper * 0.0
    wpap = hexrgb('#a9b0a2')[None, None] * (1 + 0.025 * fib[..., None]); sep = np.where(water[..., None], wpap, sep)
    # đường viền nước kiểu bản đồ khắc: các nét song song bờ, thưa dần
    wl = np.zeros_like(dist_in)
    for i, dd in enumerate((3.5, 8, 14, 22, 32)):
        wl = np.maximum(wl, np.clip(1 - np.abs(dist_in - dd) / 0.9, 0, 1) * (0.55 - 0.09 * i))
    sep = sep * (1 - (wl * water)[..., None]) + ink * (wl * water)[..., None]
    coast = np.maximum(np.clip(1 - np.abs(dist_out - 0.5) / 2.2, 0, 1) * land, np.clip(1 - np.abs(dist_in - 2.5) / 1.6, 0, 1) * water * 0.6); sep = sep * (1 - 0.8 * coast[..., None]) + ink * 0.8 * coast[..., None]
    sep_im = Image.fromarray((np.clip(sep, 0, 1) * 255).astype(np.uint8))
    print('[relief] sông + ranh giới…')
    big = {'Hudson', 'Mohawk', 'Susquehanna', 'W. Branch Susquehanna', 'Allegheny', 'Ohio', 'Monongahela', 'Delaware', 'Niagara', 'Saint Lawrence', 'Potomac', 'Connecticut', 'Genesee', 'Juniata'}
    rv = lines('ne_10m_rivers_lake_centerlines', b, W, H) + lines('ne_10m_rivers_north_america', b, W, H, lambda r: (r.get('scalerank') or 12) <= 10 and 'Canal' not in (r.get('name') or ''))
    wf = lambda r: 3.2 if r.get('name') in big else 1.8
    # T2 G1b: cắt bỏ phần nét sông Natural Earth nằm sát mặt nước đã vẽ (sông/cửa sông suy từ DEM, hồ): hai đường cùng một sông lệch nhau 1–2 km thấy được ở tầm gần
    dw, (iy, ix) = ndimage.distance_transform_edt(~water, return_indices=True); dw = dw / ppd * 111.0   # km tới mặt nước gần nhất (+ chỉ số ô nước gần nhất)
    def runs(l):   # tách theo đoạn sát nước (< 1,5 km); bỏ đoạn sát nước dài > 3 km (đường chạy song song mặt nước = trùng/lệch); đoạn ngắn (nhánh sông chạm nước, ranh giới cắt ngang sông) giữ nguyên
        rec, pts, P = l
        if len(pts) < 2: return []
        near = [dw[min(H - 1, max(0, int(y))), min(W - 1, max(0, int(x)))] <= 1.5 for x, y in pts]
        km = lambda a, b: np.hypot(a[0] - b[0], a[1] - b[1]) / ppd * 111.0
        out, cur, k = [], [pts[0]], 0
        for i in range(1, len(pts) + 1):
            if i == len(pts) or near[i] != near[k]:
                seg = cur
                if near[k] and sum(km(seg[m], seg[m + 1]) for m in range(len(seg) - 1)) > 3.0: out.append(None)
                else: out.append(seg)
                if i < len(pts): cur, k = [pts[i - 1], pts[i]], i
            else: cur.append(pts[i])
        res, acc = [], []
        for seg in out:   # nối các đoạn giữ liền nhau thành một nét
            if seg is None:
                if len(acc) > 1: res.append(acc)
                acc = []
            else: acc = acc + seg[(1 if acc else 0):]
        if len(acc) > 1: res.append(acc)
        return [(rec, c, None) for c in res]
    def touch(l):   # đầu nét sông cách mặt nước ≤ 1,5 km → nối tới ô nước gần nhất (nhánh sông chạm sông chính/biển, không hụt)
        rec, pts, P = l; pts = list(pts)
        for e in (0, -1):
            x, y = pts[e]; yy, xx = min(H - 1, max(0, int(y))), min(W - 1, max(0, int(x)))
            if 0 < dw[yy, xx] <= 1.5:
                q = (float(ix[yy, xx]) + 0.5, float(iy[yy, xx]) + 0.5)
                if e == 0: pts.insert(0, q)
                else: pts.append(q)
        return (rec, pts, P)
    rv = [touch(l) for l in rv]
    n0 = sum(len(l[1]) for l in rv); rv = [r for l in rv for r in runs(l)]; print(f'[relief] sông NE: bỏ {n0 - sum(len(l[1]) for l in rv)}/{n0} điểm (đoạn chạy dọc mặt nước > 3 km)')
    draw_lines(nat_im, rv, (92, 140, 176, 235), wf, ppd / 600); draw_lines(sep_im, rv, (74, 50, 32, 200), wf, ppd / 600 * 0.85)
    adm = lines('ne_10m_admin_1_states_provinces_lakes', b, W, H)   # polygon → vẽ viền
    adm = [r for l in adm for r in runs(l) if sum(np.hypot(r[1][m][0] - r[1][m + 1][0], r[1][m][1] - r[1][m + 1][1]) for m in range(len(r[1]) - 1)) / ppd * 111.0 > 5.0]   # bỏ cả mẩu ranh giới < 5 km còn sót   # T2 G1b: ranh giới bang theo dòng sông (PA–NJ trên sông Delaware) lệch khỏi mặt nước DEM → cắt phần sát nước
    draw_lines(nat_im, adm, (245, 242, 232, 110), lambda r: 1.6, ppd / 600); draw_lines(sep_im, adm, (74, 50, 32, 90), lambda r: 1.4, ppd / 600)
    nat_im.save(os.path.join(out, 'natural.jpg'), quality=93); sep_im.save(os.path.join(out, 'sepia.jpg'), quality=93)
    # lưới độ cao cho 3D (trung bình khối mk×mk)
    h2, w2 = H // mk, W // mk; Zm = Zf[:h2 * mk, :w2 * mk].reshape(h2, mk, w2, mk).mean(axis=(1, 3)).astype('<f4'); Zm.tofile(os.path.join(out, 'height.f32'))
    # tuyến Natural Earth (đặt tên trong --routes 'erie=Erie Canal|Oneida River - Erie Canal;hudson=Hudson')
    RT = {}
    for spec in (arg('routes', '') or '').split(';'):
        if not spec: continue
        rid, names = spec.split('='); names = names.split('|'); segs = []
        for f in ('ne_10m_rivers_north_america', 'ne_10m_rivers_lake_centerlines'):
            for rec, pts, P in lines(f, b, W, H, lambda r: (r.get('name') or '') in names): segs.append([list(map(float, p)) for p in P])
        RT[rid] = chain(segs)
    json.dump(RT, open(os.path.join(out, 'routes.json'), 'w'))
    meta = dict(name=name, bbox=b, ppd=ppd, size=[W, H], mesh=[w2, h2], zmax=float(np.nanmax(Zf)), files={f: sha(os.path.join(out, f)) for f in ('natural.jpg', 'sepia.jpg', 'height.f32', 'routes.json')},
                src=dict(dem=('SRTM 1 arc-second via AWS Terrain Tiles (USGS, public domain; attribution: SRTM terrain data courtesy of the U.S. Geological Survey)' if SK else 'USGS 3DEP 1 arc-second (public domain, U.S. Government work)'), dem_tiles=src, vector='Natural Earth 1:10m 5.1 (public domain)',
                         ne_zip={n: sha(os.path.join(NE, n + '.zip')) for _, n in NEFILES if os.path.exists(os.path.join(NE, n + '.zip'))}))
    json.dump(meta, open(os.path.join(out, 'meta.json'), 'w'), indent=1); print(json.dumps({k: v for k, v in meta.items() if k != 'src'}, indent=1))


def chain(segs):
    """nối các đoạn đường (thứ tự bất kỳ) thành một đường dài nhất theo đầu mút gần nhau"""
    segs = [s for s in segs if len(s) > 1]
    if not segs: return []
    d = lambda a, b: math.hypot(a[0] - b[0], a[1] - b[1])
    out = segs.pop(max(range(len(segs)), key=lambda i: len(segs[i])))
    while segs:
        best = None
        for i, s in enumerate(segs):
            for rev in (False, True):
                ss = s[::-1] if rev else s
                for end in ('head', 'tail'):
                    g = d(ss[-1], out[0]) if end == 'head' else d(out[-1], ss[0])
                    if best is None or g < best[0]: best = (g, i, rev, end)
        g, i, rev, end = best
        if g > 0.25: break
        s = segs.pop(i); s = s[::-1] if rev else s; out = s + out if end == 'head' else out + s
    return out


if __name__ == '__main__':
    {'build': build}[sys.argv[1]]()
