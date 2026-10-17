import json, sys, shapely
from shapely.geometry import shape, box, mapping
BB = box(-12, 34, 10, 60)   # Iberia–Pháp–Anh
def clip(path):
    d = json.load(open(path)); out=[]
    for f in d['features']:
        g = shape(f['geometry'])
        if not g.is_valid: g = g.buffer(0)
        if not g.intersects(BB): continue
        c = g.intersection(BB)
        if c.is_empty: continue
        out.append((f['properties'], c))
    return out
for y in sys.argv[1:]:
    fs = clip(f'/root/.cache/nc-bd/data/hb_world_{y}.geojson')
    print('==', y, len(fs))
    for p, g in fs:
        nv = len(shapely.get_coordinates(g))
        print(f"  {str(p.get('NAME'))[:34]:34} SUBJ={str(p.get('SUBJECTO'))[:22]:22} BP={p.get('BORDERPRECISION')} nv={nv}")
    # Gibraltar point test
    from shapely.geometry import Point
    gp = Point(-5.35, 36.14)
    print('  Gibraltar(-5.35,36.14) in:', [p.get('NAME') for p,g in fs if g.contains(gp)])
    mp = Point(4.0, 39.95)  # Minorca
    print('  Minorca in:', [p.get('NAME') for p,g in fs if g.contains(mp)])
