"""SH · số hoá ghost phố Gibraltar theo mốc (T3).
Lệnh:
  ghost.py fit   <gcp.json>                         — RMS khớp + RMS kiểm chéo bỏ-một (LOO) theo vùng
  ghost.py build <so-hoa-px.json> <out.geojson>     — điểm ảnh → EPSG:4326 theo vùng nắn, ghi thuộc tính
  ghost.py warp  <gcp.json> <ảnh gốc> <vùng> <E0,N0,E1,N1> <m/px> <out.jpg>   — raster nắn (UTM 30N) + world file
  ghost.py check <ghost.geojson> <raster nắn.jpg|-> <E0,N0,E1,N1> <m/px> <out-ban-do.jpg> <out-osm.jpg>
Biến đổi: affine | sim (đồng dạng, lật trục y ảnh) | poly2 | tps (thin-plate spline, λ nhỏ).
Không cần GDAL/pyproj: UTM theo scripts/k2tl/geo.py (chuỗi Krüger, < 1 mm). OSM đọc từ $SH_OSM (tệp gộp /map, ngoài git)."""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../../scripts/k2tl'))
from geo import utm, utm_inv  # noqa: E402

OSM = os.environ.get('SH_OSM', '/var/tmp/cine-out/sh/osm.json')


def design(s, kind):
    x, y = s[:, 0], s[:, 1]
    if kind == 'affine': return np.c_[np.ones_like(x), x, y]
    if kind == 'poly2': return np.c_[np.ones_like(x), x, y, x * x, x * y, y * y]
    raise ValueError(kind)


class Fit:
    """Biến đổi src → dst (chuẩn hoá src để ổn định số)."""
    def __init__(self, src, dst, kind, lam=0.01):
        self.kind = kind; src = np.asarray(src, float); dst = np.asarray(dst, float)
        self.mu = src.mean(0); self.sd = src.std(0).mean() or 1.0
        s = (src - self.mu) / self.sd
        if kind == 'tps':
            n = len(s); P = np.c_[np.ones(n), s]; L = np.zeros((n + 3, n + 3))
            L[:n, :n] = self._U(s, s) + lam * np.eye(n); L[:n, n:] = P; L[n:, :n] = P.T
            Y = np.zeros((n + 3, 2)); Y[:n] = dst; self.W = np.linalg.solve(L, Y); self.s = s
        elif kind in ('sim', 'simg'):   # sim: nguồn là điểm ảnh (y xuống) → lật; simg: nguồn là toạ độ mét (y lên)
            s = s * ([1, -1] if kind == 'sim' else [1, 1]); n = len(s); A = np.zeros((2 * n, 4))
            A[0::2] = np.c_[s[:, 0], -s[:, 1], np.ones(n), np.zeros(n)]; A[1::2] = np.c_[s[:, 1], s[:, 0], np.zeros(n), np.ones(n)]
            self.q, *_ = np.linalg.lstsq(A, dst.reshape(-1), rcond=None)
        else:
            self.C, *_ = np.linalg.lstsq(design(s, kind), dst, rcond=None)

    @staticmethod
    def _U(a, b):
        r2 = ((a[:, None, :] - b[None, :, :]) ** 2).sum(-1)
        with np.errstate(divide='ignore', invalid='ignore'): return np.where(r2 > 0, r2 * np.log(r2), 0.0)

    def __call__(self, p):
        p = (np.atleast_2d(np.asarray(p, float)) - self.mu) / self.sd
        if self.kind == 'tps':
            n = len(self.s); return self._U(p, self.s) @ self.W[:n] + np.c_[np.ones(len(p)), p] @ self.W[n:]
        if self.kind in ('sim', 'simg'):
            p = p * ([1, -1] if self.kind == 'sim' else [1, 1]); a, b, tx, ty = self.q; return np.c_[a * p[:, 0] - b * p[:, 1] + tx, b * p[:, 0] + a * p[:, 1] + ty]
        return design(p, self.kind) @ self.C


def gcp_en(g):
    return [float(v) for v in (g['utm'] if 'utm' in g else utm(*g['lonlat']))]


def zone_pts(G, vung):
    """vung: tên vùng, hoặc 'tat_ca' (mọi điểm dùng được)."""
    pts = [g for g in G['gcp'] if g.get('dung', True) and (vung == 'tat_ca' or g.get('vung', 'pho') == vung)]
    return pts, np.array([g['px'] for g in pts], float), np.array([gcp_en(g) for g in pts], float)


def stats(px, en, kind, lam=0.01):
    f = Fit(px, en, kind, lam); r = np.hypot(*(f(px) - en).T); loo = []
    for i in range(len(px)):
        m = np.arange(len(px)) != i; g = Fit(px[m], en[m], kind, lam); loo.append(float(np.hypot(*(g(px[i:i + 1]) - en[i:i + 1]).T)[0]))
    return f, r, np.array(loo)


def zones(G):
    """Vùng nắn khai trong gcp.json: {"vung": {"ten": {"bien_doi": "affine", "diem": "pho"}}}."""
    out = {}
    for name, z in G['vung'].items():
        pts, px, en = zone_pts(G, z['diem'])
        f, r, loo = stats(px, en, z['bien_doi'], z.get('lam', 0.01))
        inv = Fit(en, px, z['bien_doi'], z.get('lam', 0.01))
        out[name] = dict(f=f, inv=inv, kind=z['bien_doi'], n=len(px), rms=float(np.sqrt((r ** 2).mean())), max=float(r.max()),
                         loo=float(np.sqrt((loo ** 2).mean())), loo_max=float(loo.max()), res=[(p['ten'], float(a), float(b)) for p, a, b in zip(pts, r, loo)])
    return out


def cmd_fit(path):
    G = json.load(open(path)); Z = zones(G)
    for k, z in Z.items():
        print(f"[{k}] {z['kind']} n={z['n']} RMS={z['rms']:.1f} m max={z['max']:.1f} LOO-RMS={z['loo']:.1f} LOO-max={z['loo_max']:.1f}")
        for t, a, b in z['res']: print(f"     {t[:52]:52s} sai={a:6.1f}  loo={b:6.1f}")
    return Z


def ring_area(en):
    x, y = np.asarray(en).T; return 0.5 * abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))


def cmd_build(path, out):
    S = json.load(open(path)); gpath = os.path.join(os.path.dirname(path), S['gcp']); G = json.load(open(gpath)); Z = zones(G)
    feats = []; lop = S.get('mac_dinh', {})
    for f in S['features']:
        z = Z[f['vung']]; en = z['f'](f['px'])
        ll = np.c_[utm_inv(en[:, 0], en[:, 1])]; ll = [[round(float(a), 7), round(float(b), 7)] for a, b in ll]
        sai = z['loo']
        if f['vung'] in S.get('vung_so_sanh', {}):   # dải giữa: chênh giữa biến đổi dùng và biến đổi đối chứng = sai số ước
            alt = Z[S['vung_so_sanh'][f['vung']]]['f'](f['px']); sai = max(sai, float(np.hypot(*(alt - en).T).max()))
        sai = max(sai, S.get('sai_so_toi_thieu_m', {}).get(f['vung'], 0))
        line = f.get('hinh') == 'line'
        geom = {'type': 'LineString', 'coordinates': ll} if line else {'type': 'Polygon', 'coordinates': [ll + [ll[0]]]}
        P = dict(id=f['id'], moc=S['moc'], nguon_id=f.get('nguon_id', S['nguon_id']), loai=f['loai'], do_tin=f['do_tin'])
        if f.get('ten'): P['ten'] = f['ten']
        tang = f.get('so_tang_uoc', lop.get(f['loai'], {}).get('so_tang_uoc'))
        P['so_tang_uoc'] = tang; P['cach_uoc_tang'] = f.get('cach_uoc_tang', lop.get(f['loai'], {}).get('cach_uoc_tang', ''))
        P['vung_nan'] = f['vung']; P['bien_doi'] = z['kind']; P['sai_so_vi_tri_uoc_m'] = round(sai)
        if not line: P['dien_tich_m2'] = round(ring_area(en))
        else: P['dai_m'] = round(float(np.hypot(*np.diff(en, axis=0).T).sum()))
        for k in ('trong_khoi', 'ghi_chu', 'nguon_phu'):
            if f.get(k): P[k] = f[k]
        feats.append(dict(type='Feature', properties=P, geometry=geom))
    meta = dict(moc=S['moc'], crs='EPSG:4326', nguon=S.get('nguon', {}), ghi_cong=S.get('ghi_cong', ''), giay_phep=S.get('giay_phep', ''),
                nan={k: dict(bien_doi=v['kind'], so_diem=v['n'], rms_m=round(v['rms'], 1), loo_rms_m=round(v['loo'], 1)) for k, v in Z.items()},
                so_khoi=sum(1 for f in feats if f['properties']['loai'] == 'khoi_pho'), so_nha=sum(1 for f in feats if f['properties']['loai'] == 'nha'),
                dien_tich_khoi_m2=sum(f['properties'].get('dien_tich_m2', 0) for f in feats if f['properties']['loai'] in ('khoi_pho',)),
                ghi_chu_sai_so=S.get('ghi_chu_sai_so', ''), tao_boi='channel-k2/k2c-t3-01/ghost/tools/ghost.py build ' + os.path.basename(path), ghi_chu=S.get('ghi_chu', ''))
    json.dump(dict(type='FeatureCollection', name=f"ghost-{S['moc']}", ghost=meta, features=feats), open(out, 'w'), ensure_ascii=False, indent=0)
    print(out, len(feats), 'feature;', json.dumps(meta['nan'], ensure_ascii=False), 'khối', meta['so_khoi'], 'nhà', meta['so_nha'], 'm² khối', meta['dien_tich_khoi_m2'])


def cmd_warp(gpath, img, vung, bbox, mpp, out):
    import cv2
    G = json.load(open(gpath)); Z = zones(G); z = Z[vung]; E0, N0, E1, N1 = map(float, bbox.split(',')); mpp = float(mpp)
    W, H = int((E1 - E0) / mpp), int((N1 - N0) / mpp)
    ee, nn = np.meshgrid(E0 + (np.arange(W) + 0.5) * mpp, N1 - (np.arange(H) + 0.5) * mpp)
    pp = z['inv'](np.c_[ee.ravel(), nn.ravel()]).astype(np.float32)
    src = cv2.imread(img); o = cv2.remap(src, pp[:, 0].reshape(H, W), pp[:, 1].reshape(H, W), cv2.INTER_LINEAR, borderValue=(255, 255, 255))
    cv2.imwrite(out, o, [cv2.IMWRITE_JPEG_QUALITY, 90])
    open(os.path.splitext(out)[0] + '.jgw', 'w').write(f"{mpp}\n0\n0\n{-mpp}\n{E0 + mpp / 2}\n{N1 - mpp / 2}\n")   # world file, UTM 30N (EPSG:32630)
    print(out, W, H)


def load_osm_buildings(bbox):
    E0, N0, E1, N1 = bbox; d = json.load(open(OSM)); B = []; walls = []; coast = []
    for p, t in d['ways'].values():
        if len(p) < 2: continue
        e, n = utm(np.array([a for a, b in p]), np.array([b for a, b in p]))
        if e.max() < E0 or e.min() > E1 or n.max() < N0 or n.min() > N1: continue
        q = np.c_[e, n]
        if t.get('building') and len(p) >= 4: B.append(q)
        elif t.get('barrier') == 'city_wall' or t.get('historic') == 'citywalls' or t.get('defensive_works'): walls.append(q)
        elif t.get('natural') == 'coastline': coast.append(q)
    return B, walls, coast


def cmd_check(gj, raster, bbox, mpp, out_map, out_osm):
    """Ảnh kiểm chồng: ghost 50 % lên raster nắn + ghost lên OSM hôm nay; in thống kê."""
    import cv2
    E0, N0, E1, N1 = map(float, bbox.split(',')); mpp = float(mpp); W, H = int((E1 - E0) / mpp), int((N1 - N0) / mpp)
    T = lambda en: np.c_[(en[:, 0] - E0) / mpp, (N1 - en[:, 1]) / mpp].round().astype(np.int32)
    D = json.load(open(gj)); B, walls, coast = load_osm_buildings((E0, N0, E1, N1))
    col = {'khoi_pho': (40, 90, 230), 'nha': (20, 20, 160), 'cong_su': (170, 40, 140), 'phao_dai': (170, 40, 140), 'chien_tuyen': (0, 120, 0)}

    def ghost(base):
        lay = base.copy()
        for f in D['features']:
            g = f['geometry']; c = col[f['properties']['loai']]
            ring = np.array(g['coordinates'] if g['type'] == 'LineString' else g['coordinates'][0]); e, n = utm(ring[:, 0], ring[:, 1]); q = T(np.c_[e, n])
            if g['type'] == 'LineString': cv2.polylines(lay, [q], False, c, 4, cv2.LINE_AA)
            else: cv2.fillPoly(lay, [q], c)
        o = cv2.addWeighted(lay, 0.5, base, 0.5, 0)
        for f in D['features']:
            g = f['geometry']
            if g['type'] != 'Polygon': continue
            ring = np.array(g['coordinates'][0]); e, n = utm(ring[:, 0], ring[:, 1]); cv2.polylines(o, [T(np.c_[e, n])], True, col[f['properties']['loai']], 1, cv2.LINE_AA)
        return o
    if raster != '-':
        r = cv2.imread(raster); r = cv2.resize(r, (W, H)) if r.shape[:2] != (H, W) else r
        cv2.imwrite(out_map, ghost(r), [cv2.IMWRITE_JPEG_QUALITY, 82])
    o = np.full((H, W, 3), 255, np.uint8)
    for q in B: cv2.fillPoly(o, [T(q)], (205, 205, 205)); cv2.polylines(o, [T(q)], True, (120, 120, 120), 1)
    for q in walls: cv2.polylines(o, [T(q)], False, (0, 0, 200), 2)
    for q in coast: cv2.polylines(o, [T(q)], False, (200, 120, 0), 2)
    o = ghost(o); cv2.putText(o, 'Map data (c) OpenStreetMap contributors, ODbL', (8, H - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (60, 60, 60), 1, cv2.LINE_AA)
    cv2.imwrite(out_osm, o, [cv2.IMWRITE_JPEG_QUALITY, 82])
    # thống kê: toà OSM có tâm trong khối ghost
    polys = []
    for f in D['features']:
        if f['properties']['loai'] in ('khoi_pho', 'nha') and f['geometry']['type'] == 'Polygon':
            ring = np.array(f['geometry']['coordinates'][0]); e, n = utm(ring[:, 0], ring[:, 1]); polys.append((f['properties']['id'], np.c_[e, n].astype(np.float32)))
    per = {}; inn = 0
    for q in B:
        c = q.mean(0); hit = False
        for pid, pp in polys:
            if cv2.pointPolygonTest(pp.reshape(-1, 1, 2), (float(c[0]), float(c[1])), False) >= 0: per[pid] = per.get(pid, 0) + 1; hit = hit or pid[0] == 'K'
        inn += hit
    st = dict(osm_toa_trong_khung=len(B), osm_toa_co_tam_trong_khoi_ghost=inn, so_khoi=sum(1 for p, _ in polys if p[0] == 'K'),
              khoi_ghost_khong_chua_toa_osm_nao=[p for p, _ in polys if p[0] == 'K' and p not in per], osm_toa_moi_khoi=per)
    print(json.dumps(st, ensure_ascii=False)); return st


if __name__ == '__main__':
    c, *a = sys.argv[1:]
    {'fit': cmd_fit, 'build': cmd_build, 'warp': cmd_warp, 'check': cmd_check}[c](*a)
