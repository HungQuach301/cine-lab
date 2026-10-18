"""T3 · gói TUYẾN · ảnh xem nhanh (KHÔNG phải hình phim) 3 khung SM1–SM3: bờ biển NE 1:10m + tuyến + vùng + waypoint, để chủ dự án/V5b-2c rà bằng mắt.
Dùng: /opt/cine/bin/python -I channel-k2/k2c-t3-01/tuyen/xem_truoc.py → tuyen/xem-truoc/SM*.png"""
import json, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from shapely.geometry import box, shape
sys.path.insert(0, str(Path(__file__).resolve().parent))
import mk_routes as M  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE / 'xem-truoc'; OUT.mkdir(exist_ok=True)
MAU = {'grand-alliance': '#b03a2e', 'britain': '#b03a2e', 'allies': '#b03a2e', 'spain': '#c9a227', 'france-spain': '#2e5c8a', 'civilians': '#d8c9a0'}
patch = json.loads((HERE / 'treatment-patch.json').read_text())
fc = json.loads((HERE / 'routes.geojson').read_text())
feats = {f['properties']['id']: f for f in fc['features']}
try: FONT = ImageFont.truetype('DejaVuSans.ttf', 18)
except OSError: FONT = ImageFont.load_default()

for op in patch['ops']:
    if op['op'] != 'insert_before': continue
    s = op['shot']; x0, y0, x1, y1 = s['bbox']
    land = M.load_land(box(x0 - 3, y0 - 3, x1 + 3, y1 + 3))
    a = M.FWD(x0, y0); b = M.FWD(x1, y1); c = M.FWD(x0, y1); d = M.FWD(x1, y0)
    X0, X1 = min(a[0], c[0]), max(b[0], d[0]); Y0, Y1 = min(a[1], d[1]), max(b[1], c[1])
    Wp = 1280; sc = Wp / (X1 - X0); Hp = int((Y1 - Y0) * sc)
    im = Image.new('RGB', (Wp, Hp), '#dfe8ec'); dr = ImageDraw.Draw(im)
    P = lambda x, y: ((x - X0) * sc, (Y1 - y) * sc)
    for g in getattr(land, 'geoms', [land]):
        dr.polygon([P(*p) for p in g.exterior.coords], fill='#f4efe4', outline='#8a8478')
    for zid in s.get('vung_ve', []) + [k for k in feats if k.startswith('Z') and s['id'] in feats[k]['properties']['shot'] and k not in s.get('khong_ve', {})]:
        g = feats[zid]['geometry']['coordinates'][0]
        dr.line([P(*M.FWD(lo, la)) for lo, la in g], fill='#555555', width=2)
    for i, rid in enumerate(s.get('tuyen_phu', []) + s['tuyen']):
        f = feats[rid]; pr = f['properties']; col = MAU.get(pr['phe'], '#333333')
        pts = [P(*M.FWD(lo, la)) for lo, la in f['geometry']['coordinates']]
        dr.line(pts, fill=col, width=2 if rid in s.get('tuyen_phu', []) or pr['mode'] == 'air' else 4)
        for w in pr['waypoints']:
            q = P(*M.FWD(w['lon'], w['lat'])); dr.ellipse([q[0] - 5, q[1] - 5, q[0] + 5, q[1] + 5], fill='white', outline=col, width=2)
        e = pts[-1]; dr.text((e[0] + 6, e[1] - 22 - 14 * (i % 3)), f"{rid}", fill=col, font=FONT)
    for rid in s['tuyen']:
        pr = feats[rid]['properties']
        for flag, w in (('vao_tu_mep', pr['waypoints'][0]), ('ra_mep', pr['waypoints'][-1])):
            if pr.get(flag):
                inside = x0 <= w['lon'] <= x1 and y0 <= w['lat'] <= y1
                print(f"  {s['id']} {rid} {flag}: điểm mép {'TRONG khung — LỖI' if inside else 'ngoài khung — đúng'}")
                assert not inside, (s['id'], rid)
    dr.text((12, Hp - 30), f"{s['id']} — {s['nhan_ranh']} · XEM NHANH, không phải hình phim · bờ: Natural Earth", fill='#333333', font=FONT)
    im.save(OUT / f"{s['id']}.png", optimize=True)
    print(s['id'], im.size)
