#!/opt/cine/bin/python
"""V5b-2c · ĐẶC TẢ SHOT SM3 (bản đồ chiến lược 1940–42) — chỉ để CHẤM MÙ ĐỘ RÕ riêng (lệnh 18/10: "SM3 có 8 đường/7 s"), sinh từ dữ liệu đã duyệt:
  tuyến = routes.geojson (gói TUYẾN): 4 cung sơ tán dân (kem, KHÔNG mũi tên quân sự — NC-LS M1) + Torch: đường KHÔNG Gibraltar → Tafaraoui (đỏ, nét đứt, mũi tên)
          + 3 mũi tên biển vào từ mép tây, KHÔNG ghi nơi đi (E2, T025 CHƯA XÁC MINH); điểm Gibraltar "Allied HQ" (E2)
  ranh  = /cache/hist/sm3-1941 (Tangier đổi 1940-06-14; Pháp chia hai từ bộ đếm 'Jul–Oct 1940')
  nhịp  = treatment-patch SM3 (0,0 / 1,0 / 2,2 / 5,0 / 6,5); máy: trượt nhẹ nam → bắc, MỘT lần zoom ra cho cung London/Jamaica ra mép.
  --nhip tach: phương án tách nhịp 1940 | 1942 (hai shot 3,5 s) — dùng khi chấm mù báo rối.
  sm3_spec.py --routes <routes.geojson> --out <tệp.json>"""
import argparse, json, math

COL = {'britain': '#b03a2e', 'spain': '#c9a227', 'france': '#2e5c8a', 'neutral': '#a89f8a', 'civ': '#efe6cf'}


def thin(C, km=8.0):
    out = [C[0]]
    for c in C[1:]:
        if math.hypot((c[0] - out[-1][0]) * 111.32 * math.cos(math.radians(c[1])), (c[1] - out[-1][1]) * 110.57) >= km: out.append(c)
    if out[-1] != C[-1]: out.append(C[-1])
    return [[round(x, 4), round(y, 4)] for x, y in out]


def main():
    a = argparse.ArgumentParser(); a.add_argument('--routes', required=True); a.add_argument('--out', required=True); A = a.parse_args()
    G = {f['properties']['id']: f for f in json.load(open(A.routes))['features']}
    L = lambda rid: thin(G[rid]['geometry']['coordinates'])
    civ = lambda rid, draw: dict(id=rid, pts=L(rid), draw=draw, style='solid', color=COL['civ'], ink='#3a3326', w=5.0, smooth=1, dim=[[5.0, 1.0], [5.3, 0.3]])
    mil = lambda rid, draw, style='solid': dict(id=rid, pts=L(rid), draw=draw, style=style, color=COL['britain'], ink='#2a0d08', w=6.0, arrow=True, smooth=1, flow=0, dl=8)
    routes = [civ('R1940-EV-CASA', [0.2, 1.1]), civ('R1940-EV-LON', [2.2, 4.3]), civ('R1940-EV-MAD', [2.4, 3.8]), civ('R1940-EV-JAM', [2.6, 4.2]),
              mil('R1942-AIR-ORAN', [5.0, 6.0], 'dashed'), mil('R1942-SEA-WEST', [5.1, 6.3]), mil('R1942-SEA-ORAN', [5.2, 6.4]), mil('R1942-SEA-ALG', [5.3, 6.5])]
    cam = [dict(t=0.0, lon=-6.5, lat=37.2, dist=2100, tilt=20, head=0, mm=35), dict(t=2.2, lon=-6.6, lat=38.6, dist=2150, tilt=20, head=0, mm=35),
           dict(t=3.4, lon=-7.0, lat=40.0, dist=2650, tilt=20, head=0, mm=35), dict(t=4.9, lon=-6.8, lat=40.3, dist=2600, tilt=20, head=0, mm=35),
           dict(t=5.7, lon=-3.6, lat=37.4, dist=2600, tilt=20, head=0, mm=35), dict(t=7.0, lon=-3.5, lat=37.3, dist=2600, tilt=20, head=0, mm=35)]   # zoom ra DUY NHẤT 2,2 → 3,4 s; 4,9 → 5,7 s chỉ LIA nam (cùng tầm) cho bờ Bắc Phi 1942 vào khung (bản đầu: Casablanca/Oran/Algiers rơi ra mép dưới)
    dates = [[0.0, '1940-05-22'], [1.0, '1940-06-14'], [2.2, '1940-07-15'], [5.0, '1942-11-08']]
    hero_opt = dict(relief='sm3', palette='sepia', ve=7, cam=cam, routes=routes, borders=dict(src='sm3-1941', dates=dates, a=0.62, edge=2.2, soft=10, hatch=7),
                    places=[dict(id='casa', ll=[-7.62, 33.59], name='Casablanca'), dict(id='spain_c', ll=[-3.7, 40.2], name='Spain'), dict(id='tangier', ll=[-5.80, 35.77], name='Tangier'),
                            dict(id='frmor', ll=[-6.0, 32.4], name='French Morocco'), dict(id='alg', ll=[2.5, 34.6], name='Algeria'), dict(id='occ', ll=[0.5, 47.6], name='German-occupied France'), dict(id='vichy_c', ll=[3.0, 45.3], name='Vichy France'),
                            dict(id='lon_l', ll=[-10.17, 41.08], name=''), dict(id='jam_l', ll=[-11.24, 35.04], name=''), dict(id='mad_l', ll=[-13.32, 34.38], name='')],   # neo nhãn tuyến dài ra mép (bản đầu: nhãn bám mũi tên ngoài khung bị kẹp đè nhãn ranh)
                    exposure=1.0)
    tags = [dict(a='rt:R1940-EV-CASA', s='to Casablanca', sub='civilians, May–Jun 1940', at=0.5, out=2.2, side='auto', c='#d9cfb4', px=30, spx=26),
            dict(a='spain_c', s='Spain (non-belligerent)', sub='12 Jun 1940', at=1.0, out=4.9, side='up', c=COL['spain'], px=32, spx=26),
            dict(a='tangier', s='Tangier', sub='Spanish-occupied from 14 Jun 1940', at=1.1, out=2.4, side='down', c=COL['spain'], px=28, spx=24),
            dict(a='lon_l', s='to London', at=3.0, out=4.9, side='auto', c='#d9cfb4', px=30), dict(a='mad_l', s='to Madeira', at=3.0, out=4.9, side='auto', c='#d9cfb4', px=30),
            dict(a='jam_l', s='to Jamaica', at=3.2, out=4.9, side='auto', c='#d9cfb4', px=30),
            dict(a='rt:R1942-AIR-ORAN', s='8 Nov 1942 · aircraft to Oran', at=5.4, out=6.9, side='auto', c=COL['britain'], px=30),
            dict(a='rt:R1942-SEA-ALG', s='Allied landings', sub='Casablanca · Oran · Algiers', at=5.7, out=6.9, side='auto', c=COL['britain'], px=30, spx=26),
            dict(a='occ', s='German-occupied', at=2.3, out=4.9, side='auto', c='#8f8676', px=28), dict(a='vichy_c', s='Vichy', at=2.3, out=4.9, side='auto', c=COL['france'], px=28)]
    p = dict(legend=dict(items=[dict(s='Britain & Allies', c=COL['britain']), dict(s='Spain (non-belligerent)', c=COL['spain']), dict(s='France: Vichy / occupied (hatched)', c=COL['france'], hatch=True)], at=0.0, out=6.8),
             bnote='approx. borders c. 1941 — Cliopatria (Seshat)', bnoteAt=-0.4, bnoteOut=6.9,
             counter=[dict(t=0.0, s='May 1940'), dict(t=1.0, s='12–14 Jun 1940'), dict(t=2.2, s='Jul–Oct 1940'), dict(t=5.0, s='8 Nov 1942')], counterOut=6.9,
             points=[dict(a='pt:gibraltar', s='Gibraltar · Allied HQ', c=COL['britain'], at=0.0, out=6.9, side='auto')], tags=tags, kind='')
    json.dump(dict(hero_opt=hero_opt, p=p, n_tuyen=len(routes)), open(A.out, 'w'), ensure_ascii=False, indent=1); print('SM3 tuyến', len(routes))


if __name__ == '__main__':
    main()
