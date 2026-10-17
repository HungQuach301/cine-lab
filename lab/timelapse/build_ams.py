"""Gói dữ liệu cảnh thử Amsterdam (ngoài git, $TL_DATA/ams/scene.json) + thống kê chất lượng năm xây (research/timelapse/h1-amsterdam.json).
Nguồn: 3DBAG lod12 (CC BY 4.0, 3DBAG by tudelft3d and 3DGI; nền BAG Kadaster CC0) · BGT waterdeel (Kadaster/PDOK, CC0)
· Copernicus GLO-30 DEM (© DLR e.V. 2010-2014 and © Airbus Defence and Space GmbH 2014-2018, provided under COPERNICUS by the EU and ESA)."""
import json, os, glob, math, collections
from pathlib import Path
import numpy as np

DATA = Path(os.environ.get("TL_DATA", Path.home() / ".cache/cine-timelapse"))
A = DATA / "ams"
REPO = Path(__file__).resolve().parents[2]

def rd2wgs(x, y):   # Schreutelkamp & Strang van Hees (≈ 1 m), đủ cho tra DEM 30 m
    dx, dy = (x - 155000) * 1e-5, (y - 463000) * 1e-5
    K = [(0,1,3235.65389),(2,0,-32.58297),(0,2,-0.2475),(2,1,-0.84978),(0,3,-0.0665),(2,2,-0.01709),(1,0,-0.00738),(4,0,0.0053),(2,3,-3.9e-4),(4,1,3.3e-4),(1,1,-1.2e-4)]
    L = [(1,0,5260.52916),(1,1,105.94684),(1,2,2.45656),(3,0,-0.81885),(1,3,0.05594),(3,1,-0.05607),(0,1,0.01199),(3,2,-0.00256),(1,4,0.00128),(0,2,2.2e-4),(2,0,-2.2e-4),(5,0,2.6e-4)]
    lat = 52.15517440 + sum(c * dx**p * dy**q for p, q, c in K) / 3600
    lon = 5.38720621 + sum(c * dx**p * dy**q for p, q, c in L) / 3600
    return lon, lat

def wgs2rd(lon, lat):
    dp, dl = 0.36 * (lat - 52.15517440), 0.36 * (lon - 5.38720621)
    R = [(0,1,190094.945),(1,1,-11832.228),(2,1,-114.221),(0,3,-32.391),(1,0,-0.705),(3,1,-2.340),(1,3,-0.608),(0,2,-0.008),(2,3,0.148)]
    S = [(1,0,309056.544),(0,2,3638.893),(2,0,73.077),(1,2,-157.984),(3,0,59.788),(0,1,0.433),(2,2,-6.439),(1,1,-0.032),(0,4,0.092),(1,4,-0.054)]
    return 155000 + sum(c * dp**p * dl**q for p, q, c in R), 463000 + sum(c * dp**p * dl**q for p, q, c in S)

O = wgs2rd(4.89290, 52.37306)       # Dam (Nationaal Monument), gốc toạ độ cảnh

def dp(pts, eps):
    if len(pts) < 4: return pts
    a, b = np.array(pts[0]), np.array(pts[-1]); P = np.array(pts)
    ab = b - a; n = np.hypot(*ab)
    d = np.abs(ab[0] * (P[:, 1] - a[1]) - ab[1] * (P[:, 0] - a[0])) / n if n > 1e-9 else np.hypot(*(P - a).T)
    i = int(np.argmax(d))
    if d[i] > eps: return dp(pts[:i+1], eps)[:-1] + dp(pts[i:], eps)
    return [pts[0], pts[-1]]

def ring(r, eps):
    r = [(x - O[0], y - O[1]) for x, y in r[:-1]]
    if len(r) < 3: return None
    s = dp(r + [r[0]], eps)[:-1]
    if len(s) < 3: s = r
    return [round(v, 1) for p in s for v in p]

def main():
    B = []; years = []; stat = collections.Counter()
    for f in sorted(A.glob("raw_*.json")):
        for ft in json.loads(f.read_text())["features"]:
            p = ft["properties"]; g = ft["geometry"]
            polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
            y = p.get("oorspronkelijkbouwjaar") or 0
            h = (p.get("b3_h_70p") or 0) - (p.get("b3_h_maaiveld") or 0)
            if not p.get("b3_h_70p"): stat["no_height"] += 1; h = 7.0
            h = max(2.5, min(h, 200))
            for poly in polys:
                r = ring(poly[0], 0.35)
                if r: B.append([y, round(h, 1), round(p.get("b3_h_maaiveld") or 0, 1), r])
            years.append((p["identificatie"], y))
    # thống kê năm theo toà (không theo phần)
    yb = dict(years); ys = [y for y in yb.values()]
    valid = [y for y in ys if y and y != 1005]
    old = [y for y in valid if y < 1800]
    def heap(v):
        return dict(n=len(v), pct_end_0_or_5=round(100 * sum(1 for y in v if y % 5 == 0) / max(1, len(v)), 1),
                    pct_end_0=round(100 * sum(1 for y in v if y % 10 == 0) / max(1, len(v)), 1),
                    top=collections.Counter(v).most_common(8))
    cen = collections.Counter((y // 100) * 100 for y in valid)
    st = dict(source="3DBAG lod12 WFS (CC BY 4.0) · BAG oorspronkelijkbouwjaar (CC0)", bbox_rd=[117900, 484400, 124900, 490400],
              buildings=len(yb), parts=len(B), year_1005_placeholder=sum(1 for y in ys if y == 1005),
              year_missing=sum(1 for y in ys if not y), pct_valid=round(100 * len(valid) / len(ys), 2),
              earliest=min(valid), heaping_all=heap(valid), heaping_pre1800=heap(old),
              heaping_1800_1945=heap([y for y in valid if 1800 <= y < 1945]), heaping_post1945=heap([y for y in valid if y >= 1945]),
              by_century={str(k): v for k, v in sorted(cen.items())},
              standing_by_year={str(Y): sum(1 for y in valid if y <= Y) for Y in (1400, 1500, 1600, 1622, 1700, 1795, 1850, 1900, 1945, 2000, 2026)},
              no_height_parts=stat["no_height"])
    (REPO / "research/timelapse/h1-amsterdam.json").write_text(json.dumps(st, indent=1))
    # mặt nước
    W = []
    for f in sorted(A.glob("water_*.json")):
        for ft in json.loads(f.read_text())["features"]:
            g = ft["geometry"]
            if not g: continue
            polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
            for poly in polys:
                rs = [ring(r, 0.8) for r in poly]
                if rs[0]: W.append([r for r in rs if r])
    # địa hình: Copernicus GLO-30 (DSM) → mở hình thái 5×5 (≈ 150 m) để bỏ phần nhà, lưới 30 m
    import tifffile
    from scipy import ndimage
    dem = tifffile.imread(str(DATA / "dem/cop.tif")).astype(np.float32)   # 3600×2400? (lat 52–53, lon 4–5)
    H_, W_ = dem.shape
    xs = np.arange(-3500, 3501, 50.0); ys_ = np.arange(-3000, 3001, 50.0)
    grid = np.zeros((len(ys_), len(xs)), np.float32)
    for j, yy in enumerate(ys_):
        for i, xx in enumerate(xs):
            lon, lat = rd2wgs(O[0] + xx, O[1] + yy)
            r = min(H_ - 1, max(0, int((53 - lat) * H_))); c = min(W_ - 1, max(0, int((lon - 4) * W_)))
            grid[j, i] = dem[r, c]
    dtm = ndimage.grey_opening(grid, size=(3, 3))
    st_dem = dict(dsm_mean=float(grid.mean()), dsm_std=float(grid.std()), dsm_min=float(grid.min()), dsm_max=float(grid.max()),
                  dtm_mean=float(dtm.mean()), dtm_std=float(dtm.std()), shape=list(dem.shape))
    st["copernicus_glo30"] = st_dem
    (REPO / "research/timelapse/h1-amsterdam.json").write_text(json.dumps(st, indent=1))
    scene = dict(origin_rd=O, b=B, w=W, dem=dict(x0=-3500, y0=-3000, step=50, nx=len(xs), ny=len(ys_), z=[round(float(v), 2) for v in dtm.ravel()]))
    (A / "scene.json").write_text(json.dumps(scene, separators=(",", ":")))
    print(json.dumps({k: st[k] for k in ("buildings", "parts", "year_1005_placeholder", "pct_valid", "earliest", "standing_by_year")}), len(W), st_dem)

if __name__ == "__main__":
    main()
