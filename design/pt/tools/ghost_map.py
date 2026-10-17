"""Vẽ khối ghost 1782 + 1943 (SH, chỉ đọc) quanh một tâm UTM để chọn khung neo.  python -I ghost_map.py <ghost_dir> <E> <N> <R m> <out.png>"""
import sys, json, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'scripts', 'k2tl'))
from geo import utm
from PIL import Image, ImageDraw
gd, E0, N0, R, out = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), sys.argv[5]
S = 1000; k = S / (2 * R)
im = Image.new('RGB', (S, S), (250, 248, 240)); d = ImageDraw.Draw(im)
def P(lon, lat):
    e, n = utm(lon, lat)[:2]; return ((e - E0) * k + S / 2, S / 2 - (n - N0) * k)
for y, col, w in ((1943, (60, 110, 200), 1), (1782, (200, 60, 40), 3)):
    for f in json.load(open(f'{gd}/ghost-{y}.geojson'))['features']:
        g = f['geometry']; polys = g['coordinates'] if g['type'] == 'Polygon' else ([c[0]] for c in g['coordinates']) if g['type'] == 'MultiPolygon' else [[g['coordinates']]] if g['type'] == 'LineString' else []
        if g['type'] == 'Polygon': polys = [g['coordinates'][0]]
        elif g['type'] == 'MultiPolygon': polys = [c[0] for c in g['coordinates']]
        elif g['type'] == 'LineString': polys = [g['coordinates']]
        for ring in polys:
            pts = [P(*c[:2]) for c in ring]
            if all(abs(x - S / 2) > S or abs(yy - S / 2) > S for x, yy in pts): continue
            d.line(pts, fill=col, width=w)
            if y == 1782 or f['properties'].get('loai') == 'khoi_pho':
                cx = sum(p[0] for p in pts) / len(pts); cy = sum(p[1] for p in pts) / len(pts)
                if 0 < cx < S and 0 < cy < S: d.text((cx, cy), f['properties']['id'].split('-')[-1][:8], fill=col)
for i in range(-int(R), int(R) + 1, 50):
    d.line([(S / 2 + i * k, 0), (S / 2 + i * k, S)], fill=(225, 225, 225)); d.line([(0, S / 2 + i * k), (S, S / 2 + i * k)], fill=(225, 225, 225))
d.text((5, 5), f'tam E{E0:.0f} N{N0:.0f}, luoi 50 m; do=1782 xanh=1943', fill=(0, 0, 0)); im.save(out)
