import json, sys, shapely
from shapely.geometry import shape, box
from pyproj import Transformer
S=sys.argv[1]
T=Transformer.from_crs(4326,3035,always_xy=True)
land=shapely.union_all([shape(f['geometry']) for f in json.load(open('/root/.cache/nc-bd/ne/ne_50m_land.geojson'))['features'] if shape(f['geometry']).intersects(box(-10.5,35.5,4.5,52))]).intersection(box(-10.5,35.5,4.5,52))
def proj(g): return shapely.ops.transform(T.transform,g)
import shapely.ops
def get(src,y,names):
    if src=='ohm': fs=json.load(open(f'{S}/ohm-{y}-full.geojson'))['features']; k=lambda p:p.get('name:en') or p.get('name')
    else: fs=json.load(open(f'{S}/clio-{y}.geojson'))['features']; k=lambda p:p.get('Name')
    gs=[shape(f['geometry']) for f in fs if k(f['properties']) in names]
    return shapely.union_all(gs).intersection(land) if gs else None
PYR=box(-1.9,42.2,3.2,43.4)
SP={'ohm':['Spain'],'clio':['Kingdom of Spain','Pro-Habsburg Spain','Francoist Spain']}
PT={'ohm':['Kingdom of Portugal','Portugal'],'clio':['Kingdom of Portugal','Estado Novo']}
for y in (1704,1782,1941):
    a=get('ohm',y,SP['ohm']); b=get('clio',y,SP['clio'])
    A,B=proj(a),proj(b); sd=A.symmetric_difference(B).area/A.area*100
    la=proj(a.boundary.intersection(PYR)); lb=proj(b.boundary.intersection(PYR))
    hd=la.hausdorff_distance(lb)/1000
    # trung bình khoảng cách điểm OHM -> đường Clio
    pts=[shapely.Point(c) for c in shapely.get_coordinates(la)[::5]]
    mean=sum(lb.distance(p) for p in pts)/len(pts)/1000
    pa=get('ohm',y,PT['ohm']); pb=get('clio',y,PT['clio'])
    sdp=proj(pa).symmetric_difference(proj(pb)).area/proj(pa).area*100
    print(f'{y}: TBN lệch diện tích {sd:.1f}% · biên Pyrenees Hausdorff {hd:.1f} km, TB {mean:.1f} km · BĐN lệch {sdp:.1f}%')
