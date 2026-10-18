#!/opt/cine/bin/python
"""G1b T3 · BA SHOT BẢN ĐỒ CHIẾN LƯỢC (SM1 1704 · SM2 1780–82 · SM3 1940–42) cho animatic G1b — KHUNG SẠCH §12.1 (p.sach: true).
Sinh từ dữ liệu đã duyệt (routes.geojson gói TUYẾN; lớp ranh hist_borders.py), dùng lại khuôn sm1_spec / sm2_spec / sm3_spec (không sửa hai tệp cũ):
  SM1 6,5 s  = sm1_spec.build (mới)
  SM2 7,5 s  = tuyến/nhịp sm2_spec (V5b-2c) + đuôi mới: KHÔNG zoom về vịnh 3D 1782 (shot kề là 2f eo biển) — một lần zoom duy nhất 6,0 s → eo biển ≈ 420 km;
               nhãn đoàn tiếp tế BỎ "route approx." (§12.1); thêm nhãn "blockade" (lời: "To break the blockade")
  SM3 8 s    = TÁCH hai shot (C2-4, V5b-2d): SM3a 1940 4,6 s (sơ tán dân + "Spain (non-belligerent)" + Tangier 14/6) | SM3b 1942 3,4 s (Torch)
Trên hình chỉ: bộ đếm (p.counter), chú giải ≤ 3 (p.legend), nhãn địa danh/điểm/đoàn (p.places, p.points), tuyến. Bỏ: p.bnote, p.tags (nhãn tuyến chuyển sang p.places), "route approx.".
Ra (--out, mặc định channel-k2/k2c-t3-01/g1b/sm):
  <SM>.yaml        heroes: {<k>: {hero: relief/map, opt}} + shot (SM3: shots) — phiên chính ghép vào episode toàn tập
  log-<SM>.json    nguồn ranh (lop-ranh.json), nguồn tuyến + claim, bậc căn cứ, chữ đã bỏ khỏi hình (§12.1), số đo tự soi (g1b_soi.py ghi thêm)
  spec-<SM>.json   đặc tả đầy đủ (hero_opt, p, ve_tuyen)
  ep-g1b-sm.yaml   tập thử nhỏ 4 đoạn (sm1, sm2, sm3) để chạy build.sh prep render (out /var/tmp/cine-out/g1b/sm/ep)
  g1b_sm.py --routes channel-k2/k2c-t3-01/tuyen/routes.geojson [--out channel-k2/k2c-t3-01/g1b/sm] [--hist $K2V_CACHE/hist] [--tach-at 4.6]"""
import argparse, json, os, sys, yaml
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sm1_spec, sm2_spec, sm3_spec

COL = {'britain': '#b03a2e', 'spain': '#c9a227', 'france': '#2e5c8a', 'neutral': '#a89f8a', 'civ': '#efe6cf', 'occ': '#8f8676'}
CIVL = '#d9cfb4'   # chữ nhãn tuyến dân thường (kem đậm hơn nền giấy)
TAIL = 2.3         # prep.py dựng cảnh đinh dài (dur + 1,8 + 0,5) s


def sm2(routes_path):
    G = {f['properties']['id']: f for f in json.load(open(routes_path))['features']}
    rod = sm2_spec.thin(G['R1780-RODNEY']['geometry']['coordinates']); dar = sm2_spec.thin(G['R1781-DARBY']['geometry']['coordinates'])
    how = sm2_spec.thin(sm2_spec.cut_at(G['R1782-HOWE'], 'gib_bay')); blk = [[round(x, 4), round(y, 4)] for x, y in G['Z1779-BLOCKADE']['geometry']['coordinates'][0]]
    dar = [c for c in dar if c[1] <= 45.6]; how = [c for c in how if c[1] <= 45.6]   # vào từ mép (như sm2_spec)
    R = lambda rid, pts, draw, dim: dict({k: v for k, v in dict(id=rid, pts=pts, draw=draw, style='solid', color=COL['britain'], ink='#2a0d08', w=6.5, arrow=True, dim=dim, smooth=1).items() if v is not None})
    routes = [R('R1780-RODNEY', rod, [0.6, 2.4], [[2.6, 1.0], [2.9, 0.3]]), R('R1781-DARBY', dar, [2.6, 4.1], [[4.8, 1.0], [5.1, 0.3]]), R('R1782-HOWE', how, [4.8, 6.4], None),
              dict(id='Z1779-BLOCKADE', pts=blk, close=True, draw=[0.0, 0.9], style='dashed', color=COL['spain'], ink='#3a2a06', w=4.5, flow=0, dl=7, smooth=0)]
    D = 7.5
    cam = [dict(t=0.0, lon=-6.2, lat=40.2, dist=1500, tilt=22, head=0, mm=35), dict(t=2.6, lon=-5.9, lat=39.1, dist=1480, tilt=22, head=0, mm=35),
           dict(t=4.8, lon=-5.0, lat=38.0, dist=1450, tilt=22, head=0, mm=35), dict(t=6.0, lon=-5.2, lat=37.3, dist=1380, tilt=22, head=0, mm=35),
           dict(t=7.5, lon=-5.55, lat=35.95, dist=430, tilt=27, head=0, mm=35), dict(t=D + TAIL, lon=-5.6, lat=35.93, dist=340, tilt=29, head=0, mm=35)]   # MỘT lần zoom (6,0 s →): về eo biển — shot kề 2f (3D eo biển, nhìn từ tây rất cao)
    dates = [[0.0, '1780-01-01'], [2.6, '1781-04-01'], [4.2, '1782-02-05'], [4.8, '1782-10-01'], [6.4, '1782-10-18']]
    hero_opt = dict(relief='sm2', palette='sepia', ve=9, cam=cam, routes=routes, borders=dict(src='sm2-1782', dates=dates, a=0.62, edge=2.2, soft=10, hatch=7),
                    places=[dict(id='minorca', ll=[4.10, 39.95], name='Minorca'), dict(id='algeciras', ll=[-5.45, 36.13], name='Algeciras'), dict(id='blk_l', ll=[-5.62, 35.86], name='')],
                    exposure=1.0, lodMesh=0)
    places = [dict(a='blk_l', s='blockade', at=0.3, out=2.4, side='left', c=COL['spain'], px=30),
              dict(a='rt:R1780-RODNEY', s='Relief 1 · Rodney', sub='from England', at=0.9, out=2.6, side='auto', c=COL['britain'], px=34, spx=30),
              dict(a='rt:R1781-DARBY', s='Relief 2 · Darby', sub='from Spithead', at=2.9, out=4.6, side='auto', c=COL['britain'], px=34, spx=30),
              dict(a='minorca', s='Minorca → Spain', sub='5 Feb 1782', at=4.2, out=5.6, side='up', c=COL['spain'], px=34, spx=30),
              dict(a='rt:R1782-HOWE', s='Relief 3 · Howe', sub='swept into the Med', at=5.0, out=7.0, side='auto', c=COL['britain'], px=34, spx=30)]
    p = dict(legend=dict(items=[dict(s='Britain', c=COL['britain']), dict(s='Spain', c=COL['spain']), dict(s='France', c=COL['france'])], at=0.0, out=D),
             counter=[dict(t=0.0, s='Jan 1780'), dict(t=2.6, s='Apr 1781'), dict(t=4.2, s='5 Feb 1782'), dict(t=4.8, s='Oct 1782')], counterOut=D + 0.6,
             points=[dict(a='pt:gibraltar', s='Gibraltar', c=COL['britain'], at=0.0, out=D + 0.6, side='auto')], places=places, kind='')
    ban_do = dict(nghieng=[22, 29], be_ngang_km=[1500, 340], dong=[dict(loai='route', t=[0.6, 6.4]), dict(loai='blockade', t=[0.0, 0.9]), dict(loai='camera', t=[0.0, D])], chu_giai=['Britain', 'Spain', 'France'],
                  chi_toi='Strait of Gibraltar (2f, 3D eo biển)', lop='sm2-1782', nam=1782, tuyen=['R1780-RODNEY', 'R1781-DARBY', 'R1782-HOWE', 'Z1779-BLOCKADE'],
                  claims=['T006', 'T007', 'T009', 'T011', 'T013', 'T014', 'T015', 'T016', 'T020', 'S054', 'S055', 'S056'])
    return dict(hero_opt=hero_opt, p=p, ban_do=ban_do, ve_tuyen={'R1780-RODNEY': rod, 'R1781-DARBY': dar, 'R1782-HOWE': how, 'Z1779-BLOCKADE': blk}, dur=D)


def sm3(routes_path, ta=4.6, D=8.0):
    G = {f['properties']['id']: f for f in json.load(open(routes_path))['features']}
    L = lambda rid: sm3_spec.thin(G[rid]['geometry']['coordinates'])
    civ = lambda rid, draw: dict(id=rid, pts=L(rid), draw=draw, style='solid', color=COL['civ'], ink='#3a3326', w=6.5, smooth=1)   # V5b-2d góp ý: cung sơ tán mảnh/nhạt → 6,5 px
    mil = lambda rid, draw, style='solid': dict(id=rid, pts=L(rid), draw=draw, style=style, color=COL['britain'], ink='#2a0d08', w=6.0, arrow=True, smooth=1, flow=0, dl=8)
    tb = round(D - ta, 2)
    # SM3a 1940 (ta s): nhịp theo treatment (0,0 Casablanca · 1,0→1,6 Spain/Tangier · 2,2→2,6 London/Madeira/Jamaica), theo thứ tự thời gian, không lùi bộ đếm
    A_ = [civ('R1940-EV-CASA', [0.2, 1.4]), civ('R1940-EV-LON', [2.6, 4.2]), civ('R1940-EV-MAD', [2.7, 3.9]), civ('R1940-EV-JAM', [2.8, 4.1])]
    camA = [dict(t=0.0, lon=-7.4, lat=38.6, dist=2700, tilt=20, head=0, mm=35), dict(t=ta + TAIL, lon=-7.4, lat=38.5, dist=2560, tilt=20, head=0, mm=35)]   # gần khoá (V5b-2d) + đẩy rất chậm 5 %
    datesA = [[0.0, '1940-05-22'], [1.6, '1940-06-14'], [2.6, '1940-07-15']]   # Tangier gạch vàng đúng 14/6 (T022); Pháp chia hai từ "Jul–Oct 1940" (đình chiến 22/6)
    placesA_anchor = [dict(id='casa', ll=[-7.62, 33.59], name='Casablanca'), dict(id='spain_c', ll=[-3.7, 40.2], name='Spain'), dict(id='tangier', ll=[-5.80, 35.77], name='Tangier'),
                      dict(id='lon_l', ll=[-10.24, 42.41], name=''), dict(id='jam_l', ll=[-17.01, 33.80], name=''), dict(id='mad_l', ll=[-16.9, 32.65], name='Funchal')]   # neo gần cuối cung (lượt 1: ba nhãn chụm quanh Gibraltar/Tangier)
    heroA = dict(relief='sm3', palette='sepia', ve=7, cam=camA, routes=A_, borders=dict(src='sm3-1941', dates=datesA, a=0.62, edge=2.2, soft=10, hatch=7), places=placesA_anchor, exposure=1.0)
    placesA = [dict(a='rt:R1940-EV-CASA', s='to Casablanca', at=0.5, out=2.4, side='auto', c=CIVL, px=30),
               dict(a='spain_c', s='Spain', sub='non-belligerent · 12 Jun 1940', at=1.6, out=ta - 0.05, side='up', c=COL['spain'], px=34, spx=30),
               dict(a='tangier', s='Tangier', sub='occupied by Spain · 14 Jun', at=1.7, out=ta - 0.05, side='left', c=COL['spain'], px=30, spx=30),
               dict(a='lon_l', s='to London', at=3.3, out=ta - 0.05, side='left', c=CIVL, px=30),
               dict(a='jam_l', s='to Madeira & Jamaica', at=3.5, out=ta - 0.05, side='up', c=CIVL, px=30)]
    pA = dict(legend=dict(items=[dict(s='Evacuated civilians', c=COL['civ']), dict(s='Spain (non-belligerent)', c=COL['spain']), dict(s='France: Vichy / occupied (hatched)', c=COL['france'], hatch=True)], at=0.0, out=ta),
              counter=[dict(t=0.0, s='May 1940'), dict(t=1.6, s='12–14 Jun 1940'), dict(t=2.6, s='Jul–Oct 1940')], counterOut=ta,
              points=[dict(a='pt:gibraltar', s='Gibraltar', c=COL['britain'], at=0.0, out=ta, side='auto')], places=placesA, kind='')
    # SM3b 1942 (tb s): Torch — đường không Gibraltar → Tafaraoui (nét đứt) + 3 mũi biển vào từ mép tây, KHÔNG ghi nơi đi (T025 CHƯA XÁC MINH)
    B_ = [mil('R1942-AIR-ORAN', [0.3, 1.5], 'dashed'), mil('R1942-SEA-WEST', [0.4, 1.9]), mil('R1942-SEA-ORAN', [0.5, 2.0]), mil('R1942-SEA-ALG', [0.6, 2.2])]
    camB = [dict(t=0.0, lon=-3.6, lat=37.4, dist=2600, tilt=20, head=0, mm=35), dict(t=tb + TAIL, lon=-3.4, lat=37.2, dist=2450, tilt=20, head=0, mm=35)]
    heroB = dict(relief='sm3', palette='sepia', ve=7, cam=camB, routes=B_, borders=dict(src='sm3-1941', dates=[[0.0, '1942-11-08']], a=0.62, edge=2.2, soft=10, hatch=7),
                 places=[dict(id='casa', ll=[-7.62, 33.59], name='Casablanca'), dict(id='tafa', ll=[-0.55, 35.44], name='Tafaraoui'), dict(id='alg', ll=[3.06, 36.75], name='Algiers')], exposure=1.0)
    placesB = [dict(a='tafa', s='aircraft to Oran', at=1.3, out=tb, side='down', c=COL['britain'], px=30),   # neo cố định (lượt 1: neo rt: chạy theo đầu tuyến → nhãn nhảy phía)
               dict(a='alg', s='Allied landings', sub='Casablanca · Oran · Algiers', at=1.7, out=tb, side='up', c=COL['britain'], px=32, spx=30)]
    pB = dict(legend=dict(items=[dict(s='Allied landings (Torch)', c=COL['britain']), dict(s='Vichy France', c=COL['france']), dict(s='German-occupied (hatched)', c=COL['occ'], hatch=True)], at=0.0, out=tb),
              counter=[dict(t=0.0, s='8 Nov 1942')], counterOut=tb + 0.6,
              points=[dict(a='pt:gibraltar', s='Gibraltar · Allied HQ', c=COL['britain'], at=0.0, out=tb + 0.6, side='up')], places=placesB, kind='')
    ban_do = dict(nghieng=[20, 20], be_ngang_km=[2700, 2450], dong=[dict(loai='route', t=[0.2, 4.2]), dict(loai='route', t=[ta + 0.3, ta + 2.2]), dict(loai='camera', t=[0.0, D])],
                  chu_giai=[[i['s'] for i in pA['legend']['items']], [i['s'] for i in pB['legend']['items']]], chi_toi='Bay of Gibraltar 1940 (4g)', lop='sm3-1941', nam=1941,
                  tuyen=[r['id'] for r in A_ + B_], claims=['T021', 'T022', 'T023', 'T024', 'T026', 'S114', 'S115', 'S117', 'S118', 'S120', 'S122'])
    return dict(a=dict(hero_opt=heroA, p=pA, dur=ta), b=dict(hero_opt=heroB, p=pB, dur=tb), ban_do=ban_do,
                ve_tuyen={r['id']: r['pts'] for r in A_ + B_}, dur=D, tach_at=ta)


def shift_p(p, dt):
    """thời điểm trong p của lớp chữ k2.js tính theo GIÂY CỦA ĐOẠN (không theo shot): shot đặt ở at ≠ 0 trong đoạn phải cộng at vào mọi mốc
    (lượt 1: SM3b at 4,6 s mất toàn bộ chữ vì mốc 0 … 3,4 s đã qua). Cảnh đinh (hero_opt) tính theo giây của shot — không dời."""
    q = json.loads(json.dumps(p)); f = lambda x: round(x + dt, 3)
    for k in ('legend',): q[k] = dict(q[k], at=f(q[k]['at']), out=f(q[k]['out']))
    q['counter'] = [dict(c, t=f(c['t'])) for c in q['counter']]; q['counterOut'] = f(q['counterOut'])
    for k in ('points', 'places'): q[k] = [dict(x, at=f(x['at']), out=f(x['out'])) for x in q.get(k, [])]
    return q


def shot(k, S, at, noi):
    return dict(tpl='plate', type='strategic', at=at, noi=noi, p=dict(hero=k, sach=True, **(shift_p(S['p'], at) if at else S['p'])))


BO_CHU = ['p.bnote "approx. borders c. YYYY — <nguồn>" (§11.1 cũ → §12.1: chuyển sang mô tả/bình luận ghim/thẻ "How this film was made")',
          'sub "route approx." ở nhãn đoàn/tuyến (§12.1)', 'mọi dòng nguồn "Map: …"/"Borders: …"/"Relief: …" (§12.1)',
          'p.tags (k2.js sach lọc bỏ thẻ không phải số/câu trích) → nhãn tuyến/đoàn đặt ở p.places (nhãn địa danh/điểm, được giữ)']


def bac(sm):
    """bậc căn cứ (§12.2) cho phần tử trên bản đồ chiến lược"""
    return [dict(phan_tu='ranh giới chính thể', bac=1, can_cu='Cliopatria v0.2.1 (tổng hợp bản đồ lịch sử, tầm châu lục) đối chiếu OpenHistoricalMap; lệch đo trong lop-ranh.json'),
            dict(phan_tu='màu phe / liên minh', bac=2, can_cu='claim văn bản (T004/T005 SM1; T006… SM2; T021–T026 SM3) — màu không lấy từ nguồn ranh'),
            dict(phan_tu='điểm mốc tuyến (cảng, ngày)', bac=2, can_cu='claims-tuyen.md (trích nguyên văn, ≥ 2 nguồn khi XÁC MINH)'),
            dict(phan_tu='đường đi giữa hai điểm mốc', bac=5, can_cu='điểm điều khiển ven bờ (routes.geojson doan[].approx = true), kiểm không cắt đất NE 1:10m — "route approx." chỉ ghi ở log/mô tả'),
            dict(phan_tu='địa hình nền', bac=1, can_cu='ETOPO 2022 15″ (NOAA NCEI, CC0) + bờ Natural Earth 1:10m (PD) — địa hình hiện đại, không phải bờ biển lịch sử')]


def log_of(sm, S, lop, routes_path, hist_dir):
    G = {f['properties']['id']: f['properties'] for f in json.load(open(routes_path))['features']}
    tuyen = []
    for rid in S['ban_do']['tuyen']:
        pr = G.get(rid, {}); wps = pr.get('waypoints') if isinstance(pr.get('waypoints'), list) else []
        tuyen.append(dict(id=rid, ten=pr.get('ten'), ngay=pr.get('ngay'), mode=pr.get('mode'), claims=sorted({c for w in wps for c in w.get('claims', [])}),
                          doan_approx=[d for d in pr.get('doan', []) if d.get('approx')], vao_tu_mep=pr.get('vao_tu_mep'), ra_mep=pr.get('ra_mep'),
                          kiem_dat_goc=pr.get('kiem_dat'), so_diem_ve=len(S['ve_tuyen'].get(rid, []))))
    L = [json.load(open(os.path.join(hist_dir, l, 'lop-ranh.json'))) for l in lop]
    return dict(shot=sm, dur=S['dur'], tao_boi='scripts/k2/hist/g1b_sm.py', khung_sach='§12.1 (CHU-1 = A) — p.sach: true',
                nguon_ranh=[dict(id=x['id'], nam=x['nam'], ngay=x.get('ngay'), nguon=x['nguon'], giay_phep=x['giay_phep'], doi_chieu=x.get('nguon_doi_chieu'), giay_phep_doi_chieu=x.get('giay_phep_doi_chieu'),
                                 km_px=x['km_px'], lech_tb_px=x['lech_tb_px'], kieu_mep=x['kieu_mep'], ghi_cong=x['ghi_cong'], chinh_tay=x.get('chinh_tay'),
                                 features=[dict(id=f['id'], ten=f['ten'], faction_id=f['faction_id'], fill=f['fill'], ve=f['ve'], kieu_mep=f['kieu_mep'], lech=f['lech'], claims=f['claims'], doi_chu=f['doi_chu']) for f in x['features']],
                                 diem=x.get('diem'), nhan_cu_tren_hinh_da_bo=x['nhan']) for x in L],
                nguon_tuyen=dict(tep='channel-k2/k2c-t3-01/tuyen/routes.geojson', claims_md='channel-k2/k2c-t3-01/tuyen/claims-tuyen.md', tuyen=tuyen),
                nen=dict(dem='ETOPO 2022 15 arc-second surface (NOAA NCEI, CC0-1.0, DOI 10.25921/fd45-gt74)', bo_bien='Natural Earth 1:10m (PD)'),
                bac_can_cu=bac(sm), chu_da_bo_khoi_hinh=BO_CHU, ban_do=S['ban_do'])


def main():
    a = argparse.ArgumentParser(); a.add_argument('--routes', required=True); a.add_argument('--out', default='channel-k2/k2c-t3-01/g1b/sm')
    a.add_argument('--hist', default=os.path.join(os.environ.get('K2V_CACHE', '/var/tmp/cine-out/k2v-cache'), 'hist')); a.add_argument('--tach-at', type=float, default=4.6)
    a.add_argument('--ep-out', default='/var/tmp/cine-out/g1b/sm/ep'); A = a.parse_args(); os.makedirs(A.out, exist_ok=True)
    S1, S2, S3 = sm1_spec.build(A.routes), sm2(A.routes), sm3(A.routes, A.tach_at)
    head = '# {sm} — G1b T3 bản đồ chiến lược, KHUNG SẠCH §12.1; sinh bằng scripts/k2/hist/g1b_sm.py — đừng sửa tay (sửa mã sinh rồi chạy lại)\n'
    out = {'SM1': (dict(heroes=dict(sm1=dict(hero='relief/map', opt=S1['hero_opt'])), shot=shot('sm1', S1, 0, 'luc_dia')), ['sm1-1704'], S1),
           'SM2': (dict(heroes=dict(sm2=dict(hero='relief/map', opt=S2['hero_opt'])), shot=shot('sm2', S2, 0, 'bien')), ['sm2-1782'], S2),
           'SM3': (dict(heroes=dict(sm3a=dict(hero='relief/map', opt=S3['a']['hero_opt']), sm3b=dict(hero='relief/map', opt=S3['b']['hero_opt'])),
                        shots=[shot('sm3a', S3['a'], 0, 'luc_dia'), shot('sm3b', S3['b'], S3['tach_at'], 'luc_dia')], tach=dict(a=S3['a']['dur'], b=S3['b']['dur'], cat='cắt thẳng (V5b-2d)')), ['sm3-1941'], S3)}
    for sm, (Y, lop, S) in out.items():
        open(os.path.join(A.out, f'{sm}.yaml'), 'w').write(head.format(sm=sm) + yaml.safe_dump(Y, allow_unicode=True, sort_keys=False, width=200))
        json.dump(S, open(os.path.join(A.out, f'spec-{sm}.json'), 'w'), ensure_ascii=False, indent=1)
        lg = os.path.join(A.out, f'log-{sm}.json'); old = json.load(open(lg)) if os.path.exists(lg) else {}
        L = log_of(sm, S, lop, A.routes, A.hist); L.update({k: v for k, v in old.items() if k in ('soi', 'dung')}); json.dump(L, open(lg, 'w'), ensure_ascii=False, indent=1)
    segs = []
    for i, (sm, (Y, _, S)) in enumerate(out.items()):
        shots = Y.get('shots') or [Y['shot']]
        segs.append(dict(id=sm.lower(), part='TEST', chuong={'SM1': '1', 'SM2': '2', 'SM3': '4'}[sm], dur=float(S['dur']), fadeIn=0, fadeOut=0, beats=[dict(t=0.0, k='cut', s=f'{sm} strategic map')], shots=shots))
    E = dict(id='g1b-sm', title='G1b T3 strategic maps SM1–SM3 (clean frame, draft)', brand='MOVING PARTS', channel='k2', out=A.ep_out,
             music=[dict(file='assets/k2/music/Tyrant.mp3', **{'from': 'a'}, ss=2.55, gain_db=-3)], sources={}, numbers={},
             heroes={k: v for Y, _, _ in out.values() for k, v in Y['heroes'].items()}, segments=segs)
    open(os.path.join(A.out, 'ep-g1b-sm.yaml'), 'w').write('# Tập thử nhỏ G1b SM1–SM3 (chỉ prep + render, không mix/ghép); sinh bằng scripts/k2/hist/g1b_sm.py\n' + yaml.safe_dump(E, allow_unicode=True, sort_keys=False, width=200))
    print('ghi', A.out, {k: v[2]['dur'] for k, v in out.items()})


if __name__ == '__main__':
    main()
