#!/opt/cine/bin/python
"""V5b-2c · ĐỘ DÀY TUYẾN BIỂN GẦN BỜ (lệnh E: "tuyến ven bờ < 1,5 km ghi số"): với mỗi tuyến ĐÃ VẼ (bd/routes-ve.geojson hoặc ve_tuyen của spec SM3),
lấy mẫu mỗi 0,5 km, đo khoảng cách tới đất NE 1:10m (land + minor islands, chiếu LAEA 52°B 10°Đ — mét), ghi: min, km đường < 1,5 km bờ, và
NỬA BỀ NGANG NÉT vẽ ở tỷ lệ shot (w px × km/px ÷ 2) — đoạn có khoảng cách bờ < nửa nét thì nét CHẠM bờ trên hình (dù hình học không cắt đất).
  route_coast.py --routes <geojson|spec.json> --kmpx <km/px> [--kmpx2 <km/px cuối zoom>] --out <json>"""
import argparse, json
from shapely.geometry import shape, LineString, Point
from shapely.ops import transform, unary_union
from pyproj import Transformer
RAW = '/var/tmp/cine-out/bd/raw'


def main():
    a = argparse.ArgumentParser(); a.add_argument('--routes', required=True); a.add_argument('--kmpx', type=float, required=True); a.add_argument('--kmpx2', type=float); a.add_argument('--out', required=True)
    A = a.parse_args(); T = Transformer.from_crs('EPSG:4326', 'EPSG:3035', always_xy=True).transform
    land = unary_union([shape(f['geometry']) for n in ('ne_10m_land', 'ne_10m_minor_islands') for f in json.load(open(f'{RAW}/{n}.geojson'))['features']])
    land = transform(T, land.intersection(shape(dict(type='Polygon', coordinates=[[[-30, 25], [15, 25], [15, 60], [-30, 60], [-30, 25]]]))))
    D = json.load(open(A.routes))
    if 'features' in D: R = [(f['properties']['id'], f['properties'].get('mode'), f['geometry']['coordinates'], f['properties'].get('w', 6.5)) for f in D['features'] if f['geometry']['type'] == 'LineString']
    else: R = [(r['id'], 'air' if 'AIR' in r['id'] else 'sea', r['pts'], r.get('w', 6.0)) for r in D['hero_opt']['routes'] if not r.get('close')]
    out = []
    for rid, mode, pts, w in R:
        if mode != 'sea': continue
        L = transform(T, LineString(pts)); n = max(2, int(L.length / 500)); half = w * A.kmpx / 2; half2 = w * A.kmpx2 / 2 if A.kmpx2 else None
        d = [land.distance(L.interpolate(i / n, normalized=True)) / 1000 for i in range(n + 1)]; step = L.length / 1000 / n
        near = [i for i, x in enumerate(d) if x < 1.5]; touch = [i for i, x in enumerate(d) if x < half]
        def where(ix):
            if not ix: return []
            runs, s = [], ix[0]
            for p, q in zip(ix, ix[1:] + [None]):
                if q != p + 1:
                    m = transform(Transformer.from_crs('EPSG:3035', 'EPSG:4326', always_xy=True).transform, L.interpolate((s + p) / 2 / n, normalized=True)); runs.append(dict(lon=round(m.x, 3), lat=round(m.y, 3), km=round((p - s + 1) * step, 1), min_km=round(min(d[s:p + 1]), 2))); s = q
            return runs
        out.append(dict(id=rid, dai_km=round(L.length / 1000, 1), min_bo_km=round(min(d), 2), km_duoi_1_5=round(len(near) * step, 1), w_px=w, nua_net_km=round(half, 2),
                        km_net_cham_bo=round(len(touch) * step, 1), doan_duoi_1_5=where(near), nua_net_km_cuoi_zoom=round(half2, 2) if half2 else None,
                        km_net_cham_bo_cuoi_zoom=round(sum(1 for x in d if half2 and x < half2) * step, 1) if half2 else None))
    json.dump(dict(km_px=A.kmpx, km_px_cuoi=A.kmpx2, tuyen=out), open(A.out, 'w'), indent=1, ensure_ascii=False); print(json.dumps(out, indent=1, ensure_ascii=False))


if __name__ == '__main__':
    main()
