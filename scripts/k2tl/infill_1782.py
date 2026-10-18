"""V5b-2c (lệnh V0 mục b, I2 chủ dự án 18/10) · LẤP PHỐ ƯỚC TÍNH cho mốc 1782.
Bản đồ Drinkwater 1786 (ghost SH) chỉ vẽ viền khối phố nửa tây phố cổ; nửa đông (sườn đồi) vẽ không viền → trước đây để trống (mé đông khung trống).
Ở đây lấp phần còn trống TRONG RANH PHỐ CÓ NGUỒN bằng khối thủ tục, đánh dấu `do_tin: uoc`:
  · ranh phố = Line Wall (tây, C1782-06/07) + tường nam Southport–Charles V (C1782-09) + mép bắc phố cổ trên plan 1782 (N của khối 1782 cực bắc − 40 m)
    + mép đông = mép đông lõi phố cổ trên plan AMS 1943 (ghost SH 1943) — mép đông này là GIẢ ĐỊNH (phố cổ ít đổi đường từ thế kỷ 18; ghi trên hình là "estimated infill");
  · hình khối = toà 1943 (ghost SH, OSM lọc theo AMS) đóng 1,2 m thành khối giữ lòng phố, TRỪ khối/toà/công sự 1782 có nguồn (đệm 5 m), bỏ mảnh < 120 m²;
  · cao 2 tầng chuẩn mốc 1782 (như ghost SH). Không phải toà cụ thể.
Ra: GeoJSON (WGS84) + log % diện tích lấp so tổng phố (có nguồn + lấp).
  infill_1782.py --ghost-dir <thư mục ghost SH> --out <tệp.geojson> --log <tệp.json>"""
import argparse, json, os, sys
import numpy as np
from shapely.geometry import Polygon, LineString, mapping, shape
from shapely.ops import unary_union, transform
import warnings; warnings.filterwarnings('ignore', category=DeprecationWarning)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import geo  # noqa: E402

ORIGIN = (-5.3487, 36.1513)


def main():
    a = argparse.ArgumentParser(); a.add_argument("--ghost-dir", required=True); a.add_argument("--out", required=True); a.add_argument("--log", required=True)
    A = a.parse_args()
    OE, ON = geo.utm(*ORIGIN)
    def to_enu(x, y, z=None): E, N = geo.utm(np.asarray(x), np.asarray(y)); return np.asarray(E) - OE, np.asarray(N) - ON
    def to_ll(e, n, z=None):
        lon, lat = geo.utm_inv(np.asarray(e) + OE, np.asarray(n) + ON) if hasattr(geo, "utm_inv") else inv(np.asarray(e) + OE, np.asarray(n) + ON); return lon, lat
    g82 = json.load(open(os.path.join(A.ghost_dir, "ghost-1782.geojson")))["features"]
    g43 = json.load(open(os.path.join(A.ghost_dir, "ghost-1943.geojson")))["features"]
    P = lambda f: transform(to_enu, shape(f["geometry"]))
    blocks82 = [P(f) for f in g82 if f["properties"].get("loai") in ("khoi_pho", "nha", "cong_su", "phao_dai") and f["geometry"]["type"] == "Polygon"]
    town82 = [P(f) for f in g82 if f["properties"].get("loai") in ("khoi_pho", "nha") and f["geometry"]["type"] == "Polygon"]
    lw = {f["properties"]["id"]: P(f) for f in g82 if f["geometry"]["type"] == "LineString" and f["properties"].get("id") in ("C1782-06", "C1782-07", "C1782-09")}
    nha43 = [P(f) for f in g43 if f["properties"].get("loai") == "nha"]
    old43 = unary_union([b.buffer(1.2) for b in nha43]).buffer(-1.2)   # đóng 1,2 m: giữ lòng phố ≥ 2,4 m (đóng 3 m gộp cả khu thành một khối rỗng ruột)
    from shapely.geometry import box
    old43 = old43.intersection(box(-800, -1900, -120, -700))   # chỉ lõi phố cổ (ghost 1943 gồm cả North Front ở bắc eo đất)
    # ranh phố: tây theo Line Wall (đường liền C1782-07 → 06), nam theo C1782-09, bắc = khối 1782 cực bắc − 40 m, đông = mép đông lõi phố 1943 (+ 15 m)
    west = list(lw["C1782-07"].coords) + list(lw["C1782-06"].coords)
    west.sort(key=lambda p: -p[1])
    south = list(lw["C1782-09"].coords)
    nmax = max(b.bounds[3] for b in town82) + 40
    nmin = min(p[1] for p in south)
    e_east = old43.bounds[2] + 15
    ring = [(west[0][0], nmax)] + [p for p in west if nmin <= p[1] <= nmax] + sorted(south, key=lambda p: p[0]) + [(e_east, nmin), (e_east, nmax)]
    bound = Polygon(ring).buffer(0)
    bound = bound.intersection(unary_union([old43.buffer(15), unary_union(town82).buffer(15)]))   # chỉ nơi có lõi phố (1943) hoặc khối 1782
    src = unary_union([b.buffer(5) for b in blocks82])
    fill = old43.intersection(bound).difference(src)
    parts = [g for g in (fill.geoms if hasattr(fill, "geoms") else [fill]) if g.geom_type == "Polygon" and g.area >= 120]
    feats = []
    for i, g in enumerate(sorted(parts, key=lambda g: -g.area)):
        g = g.simplify(0.8)
        ll = transform(lambda e, n, z=None: to_ll(e, n), g)
        feats.append(dict(type="Feature", geometry=mapping(ll), properties=dict(id=f"U1782-{i + 1:03d}", moc=1782, loai="khoi_pho", do_tin="uoc", so_tang_uoc=2,
            nguon="estimated infill: street blocks from ghost-1943 (OSM + AMS M981, SH) inside the 1782 town walls; not drawn on Drinkwater 1786",
            dien_tich_m2=round(g.area))))
    a_src = unary_union(town82).intersection(bound).area
    a_fill = sum(g.area for g in parts)
    log = dict(n_khoi_lap=len(parts), dt_lap_m2=round(a_fill), dt_pho_co_nguon_m2=round(a_src), pct_lap=round(100 * a_fill / (a_fill + a_src), 1),
               ranh=dict(bac_N=round(nmax, 1), nam_N=round(nmin, 1), dong_E=round(e_east, 1), dt_ranh_m2=round(bound.area)),
               cach=__doc__.split("\n")[3:8])
    json.dump(dict(type="FeatureCollection", features=feats), open(A.out, "w"), ensure_ascii=False)
    json.dump(log, open(A.log, "w"), ensure_ascii=False, indent=1)
    print(json.dumps({k: v for k, v in log.items() if k != "cach"}, ensure_ascii=False))


def inv(E, N):
    from pyproj import Transformer
    t = Transformer.from_crs(32630, 4326, always_xy=True); return t.transform(E, N)


if __name__ == "__main__":
    main()
