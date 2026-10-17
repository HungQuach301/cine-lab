"""Ghép quan hệ OHM (out geom) thành polygon, cắt bbox, thống kê + xuất GeoJSON."""
import json, sys, shapely
from shapely.geometry import LineString, Point, box, mapping
from shapely.ops import polygonize, unary_union
from pyproj import Geod
G = Geod(ellps='WGS84')
y, bbox, out = sys.argv[1], [float(v) for v in sys.argv[2].split(',')], sys.argv[3]
BB = box(*bbox)
d = json.load(open(f'/root/.cache/nc-bd/data/ohm-{y}.json'))
feats = []
for r in d['elements']:
    t = r['tags']; lines = []
    for m in r.get('members', []):
        if m['type'] == 'way' and m.get('role') in ('outer', 'inner', '') and 'geometry' in m:
            lines.append(LineString([(p['lon'], p['lat']) for p in m['geometry']]))
    polys = list(polygonize(unary_union(lines)))
    # chẵn-lẻ: polygonize trả cả mặt trong; giữ mặt nằm trong số lẻ vòng outer
    outer = [LineString([(p['lon'], p['lat']) for p in m['geometry']]) for m in r.get('members', []) if m['type']=='way' and m.get('role')=='outer' and 'geometry' in m]
    inner_ids = [m for m in r.get('members', []) if m.get('role') == 'inner']
    g = unary_union(polys) if polys else None
    if g is None or g.is_empty: print('  RỖNG', r['id'], t.get('name')); continue
    if inner_ids:
        inn = list(polygonize(unary_union([LineString([(p['lon'], p['lat']) for p in m['geometry']]) for m in inner_ids if 'geometry' in m])))
        if inn: g = g.difference(unary_union(inn))
    c = g.intersection(BB)
    if c.is_empty: continue
    nv_full = sum(len(m.get('geometry', [])) for m in r.get('members', []))
    per = G.geometry_area_perimeter(g)[1] / 1000
    props = {k: t.get(k) for k in ('name', 'name:en', 'start_date', 'end_date', 'source', 'license', 'wikidata', 'note', 'description') if t.get(k)}
    props['ohm_relation'] = r['id']
    props['ohm_version_note'] = 'Overpass OHM 17/10/2026'
    feats.append({'type': 'Feature', 'properties': props, 'geometry': mapping(shapely.set_precision(c, 1e-4))})
    print(f"  {r['id']} {str(t.get('name:en') or t.get('name'))[:40]:40} {t.get('start_date')}→{t.get('end_date')} nv={nv_full} perim={per:.0f}km spacing≈{per*1000/max(nv_full,1):.0f}m src={str(t.get('source'))[:50]}")
gp = Point(-5.35, 36.14)
print('  Gibraltar point ∈', [f['properties'].get('name') for f in feats if shapely.geometry.shape(f['geometry']).contains(gp)])
json.dump({'type': 'FeatureCollection', 'features': feats}, open(out, 'w'), separators=(',', ':'))
