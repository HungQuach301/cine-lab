#!/opt/cine/bin/python
"""V5b-2c · ĐẶC TẢ SHOT SM2 (bản đồ chiến lược 1779–82, T3 "vây hãm") cho dây chuyền kênh 2, sinh từ dữ liệu đã duyệt — KHÔNG gõ tay toạ độ:
  tuyến  = channel-k2/k2c-t3-01/tuyen/routes.geojson (gói TUYẾN @434a90f, git show — không merge): R1780-RODNEY, R1781-DARBY, R1782-HOWE (cắt ở vịnh 18/10/1782 — E3: không vẽ trận 20/10)
           + vùng Z1779-BLOCKADE (nét đứt kín); nhịp/bộ đếm theo treatment-patch.json SM2 (t 0,6 / 2,6 / 4,2 / 4,8 / 6,5)
  ranh   = /cache/hist/sm2-1782 (scripts/k2/hist/hist_borders.py từ design/k2v/hist/sm2-1782.json): Minorca đổi màu đúng 1782-02-05 (E7, T020)
  2D     = chú giải ≤ 3 phe, "approx. borders c. 1782 — Cliopatria (Seshat)", bộ đếm ngày, điểm Gibraltar, nhãn bám đầu tuyến ("route approx.")
  máy    = trượt bắc → nam theo tuyến; MỘT lần zoom cuối (1 450 → 300 km) về vịnh, hướng = hướng khung đầu cảnh 3D vinh1782 (khớp tay), rồi hoà 0,5 s.
Ra JSON {hero_opt, p, fallback_opt, fallback_p, ban_do} — scripts/k2/hist/mk_ep_v5b2c.py ghép vào episode.yaml.
  sm2_spec.py --routes <routes.geojson> --out <tệp.json> [--fallback]"""
import argparse, json, math

COL = {'britain': '#b03a2e', 'spain': '#c9a227', 'france': '#2e5c8a', 'neutral': '#a89f8a'}


def cut_at(feat, diem):
    """cắt LineString tại điểm mốc gần nhất (toạ độ waypoint) — giữ phần trước"""
    wp = [w for w in feat['properties']['waypoints'] if w['diem'] == diem][-1]; C = feat['geometry']['coordinates']
    k = min(range(len(C)), key=lambda i: (C[i][0] - wp['lon']) ** 2 + (C[i][1] - wp['lat']) ** 2); return C[:k + 1]


def thin(C, km=6.0):
    out = [C[0]]
    for c in C[1:]:
        if math.hypot((c[0] - out[-1][0]) * 111.32 * math.cos(math.radians(c[1])), (c[1] - out[-1][1]) * 110.57) >= km: out.append(c)
    if out[-1] != C[-1]: out.append(C[-1])
    return [[round(x, 4), round(y, 4)] for x, y in out]


def main():
    a = argparse.ArgumentParser(); a.add_argument('--routes', required=True); a.add_argument('--out', required=True); A = a.parse_args()
    G = {f['properties']['id']: f for f in json.load(open(A.routes))['features']}
    rod = thin(G['R1780-RODNEY']['geometry']['coordinates']); dar = thin(G['R1781-DARBY']['geometry']['coordinates']); how = thin(cut_at(G['R1782-HOWE'], 'gib_bay'))
    blk = [[round(x, 4), round(y, 4)] for x, y in G['Z1779-BLOCKADE']['geometry']['coordinates'][0]]
    # tuyến vào từ mép: Darby/Howe bắt đầu ở Anh (ngoài nền relief 46°B) → cắt phần trên 45,6°B (relief.js không vẽ ngoài nền); Rodney đã "vào từ mép" (T009)
    dar = [c for c in dar if c[1] <= 45.6]; how = [c for c in how if c[1] <= 45.6]
    R = lambda rid, pts, draw, dim, lab: dict(id=rid, pts=pts, draw=draw, style='solid', color=COL['britain'], ink='#2a0d08', w=6.5, arrow=True, dim=dim, smooth=1)
    routes = [R('R1780-RODNEY', rod, [0.6, 2.4], [[2.6, 1.0], [2.9, 0.3]], ''), R('R1781-DARBY', dar, [2.6, 4.1], [[4.8, 1.0], [5.1, 0.3]], ''), R('R1782-HOWE', how, [4.8, 6.4], None, ''),
              dict(id='Z1779-BLOCKADE', pts=blk, close=True, draw=[0.0, 0.9], style='dashed', color=COL['spain'], ink='#3a2a06', w=4.5, flow=0, dl=7, smooth=0)]
    for r in routes:
        if r.get('dim') is None: r.pop('dim', None)
    gib = [-5.3915, 36.1294]   # vịnh (điểm mốc gib_bay của routes.geojson — S012/S054)
    cam = [dict(t=0.0, lon=-6.2, lat=40.2, dist=1500, tilt=22, head=0, mm=35), dict(t=2.6, lon=-5.9, lat=39.1, dist=1480, tilt=22, head=0, mm=35),
           dict(t=4.8, lon=-5.0, lat=38.0, dist=1450, tilt=22, head=0, mm=35), dict(t=5.9, lon=-5.0, lat=37.6, dist=1430, tilt=22, head=0, mm=35),
           dict(t=7.0, lon=gib[0], lat=gib[1], dist=300, tilt=28, head=71, mm=35)]   # zoom DUY NHẤT 5,9 → 7,0 s; head 71° = phương nhìn khung 0 của vinh1782 (tây-bắc vịnh → Old Mole)
    dates = [[0.0, '1780-01-01'], [2.6, '1781-04-01'], [4.2, '1782-02-05'], [4.8, '1782-10-01'], [6.4, '1782-10-18']]
    hero_opt = dict(relief='sm2', palette='sepia', ve=9, cam=cam, routes=routes, borders=dict(src='sm2-1782', dates=dates, a=0.62, edge=2.2, soft=10, hatch=7),
                    places=[dict(id='minorca', ll=[4.10, 39.95], name='Minorca'), dict(id='algeciras', ll=[-5.45, 36.13], name='Algeciras'), dict(id='spartel', ll=[-5.92, 35.79], name='Cape Spartel')],
                    exposure=1.0, lodMesh=0)
    tags = [dict(a='rt:R1780-RODNEY', s='Relief 1 · Rodney', sub='from England · route approx.', at=0.9, out=2.6, side='auto', c=COL['britain'], px=34, spx=28),
            dict(a='rt:R1781-DARBY', s='Relief 2 · Darby', sub='from Spithead · route approx.', at=2.9, out=4.6, side='auto', c=COL['britain'], px=34, spx=28),
            dict(a='minorca', s='Minorca → Spain', sub='5 Feb 1782', at=4.2, out=5.4, side='up', c=COL['spain'], px=34, spx=28),
            dict(a='rt:R1782-HOWE', s='Relief 3 · Howe', sub='swept into the Med · route approx.', at=5.0, out=6.5, side='auto', c=COL['britain'], px=34, spx=28)]
    p = dict(legend=dict(items=[dict(s='Britain', c=COL['britain']), dict(s='Spain', c=COL['spain']), dict(s='France', c=COL['france'])], at=0.0, out=6.3),
             bnote='approx. borders c. 1782 — Cliopatria (Seshat)', bnoteAt=-0.4, bnoteOut=6.85,   # nhãn ranh đủ mức tới hết shot (6,5 s), mờ cùng bản đồ trong hoà — BD-3 (bản đầu 6,6: 92,3 % khung)
             counter=[dict(t=0.0, s='Jan 1780'), dict(t=2.6, s='Apr 1781'), dict(t=4.2, s='5 Feb 1782'), dict(t=4.8, s='Oct 1782')], counterOut=6.3,   # bộ đếm đúng treatment-patch (hết ở 'Oct 1782'); tắt trước hoà 6,5 s để không chồng đồng hồ cảnh 3D
             points=[dict(a='pt:gibraltar', s='Gibraltar', c=COL['britain'], at=0.0, out=6.8, side='auto')],
             tags=tags, kind='')
    # dự phòng NC-BD §2.4 (relief/map hiện có): bờ + tuyến + nhãn + ≤ 3 vùng (regions, polygon đơn giản hoá của chính lớp sm2-1782) — không raster ranh, không đổi chủ theo ngày
    ranh = {f['properties']['id']: f for f in json.load(open('/var/tmp/cine-out/k2v-cache/hist/sm2-1782/ranh.geojson'))['features']}
    def ring(eid, tol=0.12):
        import shapely; from shapely.geometry import shape
        g = shape(ranh[eid]['geometry']).simplify(tol); g = max(getattr(g, 'geoms', [g]), key=lambda x: x.area); return [[round(x, 3), round(y, 3)] for x, y in g.exterior.coords]
    fb_routes = [dict(r, arrow=False) for r in routes]
    fallback_opt = dict(relief='sm2', palette='sepia', ve=9, cam=cam, routes=fb_routes, places=hero_opt['places'] + [dict(id='gib', ll=[-5.353, 36.14], name='Gibraltar')],
                        regions=[dict(id='es', ll=ring('spain'), color=COL['spain'], at=[0.0, 0.6], lift=6, fill=0.55), dict(id='fr', ll=ring('france'), color=COL['france'], at=[0.0, 0.6], lift=6, fill=0.55),
                                 dict(id='pt', ll=ring('portugal'), color=COL['neutral'], at=[0.0, 0.6], lift=3, fill=0.45)], exposure=1.0)
    fallback_p = dict(year=dict(s='1780–82', at=0.0, out=6.7), places=[dict(a='gib', s='Gibraltar', at=0.0, out=6.8, side='left', c=COL['britain'])],
                      tags=[t for t in tags if not t['a'].startswith('minorca')], kind='')
    ban_do = dict(nghieng=[22, 28], be_ngang_km=[1500, 300], dong=[dict(loai='route', t=[0.6, 6.4]), dict(loai='blockade', t=[0.0, 0.9])], chu_giai=['Britain', 'Spain', 'France'],
                  chi_toi='Bay of Gibraltar (tl/vinh1782)', lop='sm2-1782', nam=1782, tuyen=['R1780-RODNEY', 'R1781-DARBY', 'R1782-HOWE', 'Z1779-BLOCKADE'],
                  claims=['T006', 'T007', 'T009', 'T011', 'T013', 'T014', 'T015', 'T016', 'T020', 'S054', 'S055', 'S056'])
    json.dump(dict(hero_opt=hero_opt, p=p, fallback_opt=fallback_opt, fallback_p=fallback_p, ban_do=ban_do, ve_tuyen={'R1780-RODNEY': rod, 'R1781-DARBY': dar, 'R1782-HOWE': how, 'Z1779-BLOCKADE': blk}),
              open(A.out, 'w'), ensure_ascii=False, indent=1)
    print('tuyến', {k: len(v) for k, v in dict(rod=rod, dar=dar, how=how, blk=blk).items()})


if __name__ == '__main__':
    main()
