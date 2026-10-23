#!/opt/cine/bin/python
"""TIEN-KY-T4 · OSM (© OpenStreetMap contributors, ODbL 1.0) → vector EPSG:27700 cho cảnh London 2026.
  osm_vec.py  (đọc $K2TL_CACHE/osm/ldn/t_*.osm; ra $LDN_DATA/vec/osm2026.json)
Toà: vòng ngoài + height/building:levels/name; đường: highway + name; nước: natural=water/waterway=riverbank; điểm có tên (nhà thờ, di tích)."""
import glob, json, os, sys
import xml.etree.ElementTree as ET
import pyproj
CACHE = os.environ.get('K2TL_CACHE', '/var/tmp/ldn/cache'); OUT = os.path.join(os.environ.get('LDN_DATA', '/var/tmp/ldn'), 'vec'); os.makedirs(OUT, exist_ok=True)
T = pyproj.Transformer.from_crs(4326, 27700, always_xy=True)
nodes, ways, rels = {}, {}, {}
for f in sorted(glob.glob(os.path.join(CACHE, 'osm/ldn/t_*.osm'))):
    for e in ET.parse(f).getroot():
        if e.tag == 'node': nodes[e.get('id')] = (float(e.get('lon')), float(e.get('lat')), {t.get('k'): t.get('v') for t in e.findall('tag')})
        elif e.tag == 'way': ways[e.get('id')] = ([n.get('ref') for n in e.findall('nd')], {t.get('k'): t.get('v') for t in e.findall('tag')})
        elif e.tag == 'relation': rels[e.get('id')] = ([(m.get('type'), m.get('ref'), m.get('role')) for m in e.findall('member')], {t.get('k'): t.get('v') for t in e.findall('tag')})
ids = list(nodes); xs, ys = T.transform([nodes[i][0] for i in ids], [nodes[i][1] for i in ids])
P = {i: (round(x, 2), round(y, 2)) for i, x, y in zip(ids, xs, ys)}
def ring(nd): return [P[n] for n in nd if n in P]
def h_of(t):
    for k in ('height', 'building:height'):
        try: return float(t[k].replace('m', '').strip())
        except Exception: pass
    try: return float(t['building:levels']) * 3.4 + (2.0 if t.get('roof:shape') not in (None, 'flat') else 0)
    except Exception: return None
R = {'toa': [], 'duong': [], 'nuoc': [], 'diem': [], 'dat': []}
def add_bld(r, t, wid):
    if len(r) >= 4: R['toa'].append({'id': wid, 'r': r, 'h': h_of(t), 'minh': h_of({'height': t.get('min_height', '')}) if t.get('min_height') else None, 'name': t.get('name'), 'b': t.get('building') or t.get('building:part'), 'part': 'building:part' in t, 'start': t.get('start_date')})
for wid, (nd, t) in ways.items():
    r = ring(nd)
    if len(r) < 2: continue
    if 'building' in t or 'building:part' in t: add_bld(r, t, wid)
    elif 'highway' in t: R['duong'].append({'id': wid, 'l': r, 'hw': t['highway'], 'name': t.get('name'), 'bridge': t.get('bridge'), 'tunnel': t.get('tunnel'), 'layer': t.get('layer')})
    elif t.get('natural') == 'water' or t.get('waterway') in ('riverbank', 'dock') or t.get('water'): R['nuoc'].append({'id': wid, 'r': r, 'k': t.get('water') or t.get('waterway') or 'water'})
    elif t.get('railway') in ('rail', 'light_rail', 'subway') and t.get('tunnel') != 'yes': R['duong'].append({'id': wid, 'l': r, 'hw': 'rail', 'name': t.get('name'), 'bridge': t.get('bridge')})
    elif t.get('leisure') in ('park', 'garden') or t.get('landuse') in ('grass',) or t.get('natural') in ('wood', 'scrub'): R['dat'].append({'id': wid, 'r': r, 'k': 'xanh'})
    if t.get('name') and (t.get('amenity') == 'place_of_worship' or 'historic' in t or t.get('tourism') or t.get('man_made') == 'tower'):
        cx = sum(p[0] for p in r) / len(r); cy = sum(p[1] for p in r) / len(r); R['diem'].append({'name': t['name'], 'p': (round(cx, 1), round(cy, 1)), 'k': t.get('amenity') or t.get('historic') or t.get('tourism'), 'osm': 'w' + wid})
for rid, (mem, t) in rels.items():
    if t.get('type') == 'multipolygon' and ('building' in t or 'building:part' in t):
        for typ, ref, role in mem:
            if typ == 'way' and role == 'outer' and ref in ways: add_bld(ring(ways[ref][0]), t, 'r' + rid)
    if t.get('type') == 'multipolygon' and (t.get('natural') == 'water' or t.get('water')):
        for typ, ref, role in mem:
            if typ == 'way' and role == 'outer' and ref in ways: R['nuoc'].append({'id': 'r' + rid, 'r': ring(ways[ref][0]), 'k': t.get('water') or 'water', 'open': True})
for nid, (lo, la, t) in nodes.items():
    if t.get('name') and (t.get('amenity') == 'place_of_worship' or 'historic' in t or t.get('place')): R['diem'].append({'name': t['name'], 'p': P[nid], 'k': t.get('amenity') or t.get('historic') or t.get('place'), 'osm': 'n' + nid})
json.dump(R, open(os.path.join(OUT, 'osm2026.json'), 'w'))
hs = [b['h'] for b in R['toa'] if b['h']]
print({k: len(v) for k, v in R.items()}, 'toà có cao độ', len(hs))
