import json, sys, shapely, shapefile, datetime
from shapely.geometry import shape, mapping, box
S, M = sys.argv[1], sys.argv[2]
def simp(g, tol): 
    g = shapely.simplify(g, tol, preserve_topology=True); return shapely.set_precision(g, 1e-4)
for y in (1704, 1782, 1941):
    d = json.load(open(f'{S}/ohm-{y}-full.geojson'))
    for f in d['features']: f['geometry'] = mapping(simp(shape(f['geometry']), 0.005))
    d['nc_bd'] = {'nguon': 'OpenHistoricalMap, Overpass 17/10/2026; cắt bbox -10.5,35.5,4.5,52; đơn giản hoá 0.005° (~0.5 km)', 'giay_phep': 'CC0 (dữ liệu OHM) + CC-BY-4.0 trên nhiều đường thành phần (CNIG/IGN Tây Ban Nha, LSIB…) — xem ATTRIBUTION.md'}
    json.dump(d, open(f'{M}/ohm-{y}-tay-au.geojson', 'w'), separators=(',', ':'))
    d = json.load(open(f'{S}/clio-{y}.geojson'))
    d['nc_bd'] = {'nguon': 'Cliopatria v0.2.1 (Seshat), cliopatria_polities_only_v021.geojson; cắt bbox -10.5,35.5,4.5,52; không đơn giản hoá', 'giay_phep': 'CC-BY-4.0 (Zenodo 23128623)'}
    json.dump(d, open(f'{M}/cliopatria-{y}-tay-au.geojson', 'w'), separators=(',', ':'))
# Newberry: ảnh chụp ngày 1783-09-03 và 1803-05-01 (trước/sau Louisiana)
r = shapefile.Reader('/root/.cache/nc-bd/nb/US_AtlasHCB_StateTerr_Gen01/US_HistStateTerr_Gen01_Shapefile/US_HistStateTerr_Gen01.shp')
flds = [f[0] for f in r.fields[1:]]; print(flds)
for day in ('1783-09-03', '1803-05-01'):
    D = datetime.date.fromisoformat(day); feats = []
    for sr in r.iterShapeRecords():
        p = dict(zip(flds, sr.record)); a, b = p['START_DATE'], p['END_DATE']
        if a <= D <= b:
            g = simp(shape(sr.shape.__geo_interface__), 0.01)
            feats.append({'type': 'Feature', 'properties': {k: str(p[k]) for k in ('NAME', 'ID', 'START_DATE', 'END_DATE', 'CHANGE', 'CITATION') if k in p}, 'geometry': mapping(g)})
    json.dump({'type': 'FeatureCollection', 'nc_bd': {'nguon': 'Newberry Library, Atlas of Historical County Boundaries — US Historical States and Territories (Gen .01°), US_AtlasHCB_StateTerr_Gen01.zip', 'giay_phep': 'trang Download: "reused for any lawful purpose, commercial or non-commercial" (tệp zip còn kèm CC BY-NC-SA 2.5 cũ — trang nói bỏ qua)'}, 'features': feats}, open(f'{M}/newberry-us-{day}.geojson', 'w'), separators=(',', ':'))
    print(day, len(feats), [f['properties']['NAME'] for f in feats][:20])
