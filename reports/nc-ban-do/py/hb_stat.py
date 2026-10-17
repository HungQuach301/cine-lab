import json, sys, shapely
from shapely.geometry import shape
from pyproj import Geod
G=Geod(ellps='WGS84')
for y in sys.argv[1:]:
    d=json.load(open(f'/root/.cache/nc-bd/data/hb_world_{y}.geojson'))
    for f in d['features']:
        n=f['properties'].get('NAME')
        if n in ('Spain','France','United Kingdom','England and Ireland','Portugal'):
            g=shape(f['geometry']); per=G.geometry_area_perimeter(g)[1]/1000; nv=len(shapely.get_coordinates(g))
            print(y,n,f"perim={per:.0f}km nv={nv} spacing≈{per/nv:.1f}km wkb_sha={hash(g.wkb)%10**8}")
