import json, sys, shapely
from shapely.geometry import shape, box, Point, mapping
from pyproj import Geod
G=Geod(ellps='WGS84'); BB=box(-10.5,35.5,4.5,52)
d=json.load(open('/root/.cache/nc-bd/data/cliopatria_polities_only_v021.geojson'))
print('n', len(d['features']), 'keys', list(d['features'][0]['properties']))
yrs=[int(a) for a in sys.argv[2:]]
outs={y:[] for y in yrs}
for f in d['features']:
    p=f['properties']
    for y in yrs:
        if p['FromYear']<=y<=p['ToYear']:
            g=shape(f['geometry'])
            if not g.is_valid: g=g.buffer(0)
            if not g.intersects(BB): continue
            c=g.intersection(BB); nv=len(shapely.get_coordinates(g)); per=G.geometry_area_perimeter(g)[1]/1000
            outs[y].append((p,c))
            print(y, f"{p['Name'][:40]:40} {p['FromYear']}–{p['ToYear']} nv={nv} spacing≈{per/nv:.1f}km")
for y in yrs:
    print(y,'Gibraltar ∈',[p['Name'] for p,c in outs[y] if c.contains(Point(-5.35,36.14))], '| Minorca ∈',[p['Name'] for p,c in outs[y] if c.contains(Point(4.0,39.95))])
    json.dump({'type':'FeatureCollection','features':[{'type':'Feature','properties':{k:p.get(k) for k in ('Name','FromYear','ToYear','Wikipedia','Wikidata')},'geometry':mapping(shapely.set_precision(c,1e-4))} for p,c in outs[y]]},open(f'{sys.argv[1]}/clio-{y}.geojson','w'),separators=(',',':'))
