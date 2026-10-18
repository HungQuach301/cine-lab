#!/opt/cine/bin/python
"""G1b T3 · ĐẶC TẢ SHOT SM1 (bản đồ chiến lược 1704 — "ai đứng về phía nào" + hạm đội Anh–Hà Lan tới eo biển), cùng khuôn sm2_spec.py / sm3_spec.py,
sinh từ dữ liệu đã duyệt — KHÔNG gõ tay toạ độ tuyến:
  tuyến = channel-k2/k2c-t3-01/tuyen/routes.geojson: R1704-LIS (phụ, nét đứt mảnh, mờ — St Helens → Lisbon, T001) + R1704-GIB (chính, đậm, mũi tên —
          ngoài khơi Lagos T002 → ngoài khơi Tetuan T003 → vịnh S012); không vẽ vòng Lisbon → Barcelona (ghi chú T001)
  ranh  = /cache/hist/sm1-1704 (hist_borders.py từ scripts/k2/hist/lop-sm1-1704.json): Đại Liên minh đỏ (England đặc; Dutch/Austria/Portugal pha + gạch),
          Pháp xanh, Tây Ban Nha (Philip V) vàng, Ma-rốc xám; nước không có claim phe để nền giấy
  nhịp  = treatment.json SM1 (6,5 s): 0,0 mở 3 phe · 0,8 R1704-LIS (1,0 s) · 2,0 R1704-GIB · 4,4 Gibraltar đổi màu (S012) · 5,2 lặn xuống vịnh → hoà 1a
  máy   = push-in liên tục Tây Âu (≈ 2 700 km, thấy Áo ở mép đông — lời đọc nêu "Austria") → eo biển (≈ 420 km ở 6,5 s, ≈ 330 km cuối đuôi cảnh), không dừng, hướng Bắc
  2D    = KHUNG SẠCH §12.1 (p.sach): bộ đếm, chú giải 3 phe, nhãn địa danh/điểm (p.places/p.points); KHÔNG nhãn nguồn/"approx. borders"/"route approx."
Ra JSON {hero_opt, p, ban_do, ve_tuyen, dur} — scripts/k2/hist/g1b_sm.py ghép thành đoạn đặc tả + tập thử.
  sm1_spec.py --routes <routes.geojson> --out <tệp.json>"""
import argparse, json, math

COL = {'britain': '#b03a2e', 'ally': '#ba5446', 'spain': '#c9a227', 'france': '#2e5c8a', 'neutral': '#a89f8a'}
DUR = 6.5


def thin(C, km=6.0):
    out = [C[0]]
    for c in C[1:]:
        if math.hypot((c[0] - out[-1][0]) * 111.32 * math.cos(math.radians(c[1])), (c[1] - out[-1][1]) * 110.57) >= km: out.append(c)
    if out[-1] != C[-1]: out.append(C[-1])
    return [[round(x, 4), round(y, 4)] for x, y in out]


def build(routes_path):
    G = {f['properties']['id']: f for f in json.load(open(routes_path))['features']}
    lis = thin(G['R1704-LIS']['geometry']['coordinates'], 8.0); gib = thin(G['R1704-GIB']['geometry']['coordinates'], 4.0)
    routes = [dict(id='R1704-LIS', pts=lis, draw=[0.8, 1.8], style='dashed', color=COL['britain'], ink='#2a0d08', w=4.5, flow=0, dl=6, smooth=1, dim=[[2.0, 1.0], [2.4, 0.45]]),   # phụ: mảnh, đứt, mờ sau khi tuyến chính bắt đầu
              dict(id='R1704-GIB', pts=gib, draw=[2.0, 4.4], style='solid', color=COL['britain'], ink='#2a0d08', w=6.5, arrow=True, smooth=1)]
    bay = [-5.3914, 36.1294]   # điểm mốc gib_bay (S012)
    cam = [dict(t=0.0, lon=-2.6, lat=45.0, dist=2700, tilt=22, head=0, mm=35), dict(t=2.2, lon=-4.4, lat=42.8, dist=2350, tilt=22, head=0, mm=35),
           dict(t=3.6, lon=-6.1, lat=38.6, dist=1350, tilt=24, head=0, mm=35), dict(t=5.0, lon=-5.7, lat=36.7, dist=720, tilt=26, head=0, mm=35),
           dict(t=6.5, lon=bay[0], lat=bay[1] - 0.05, dist=420, tilt=28, head=0, mm=35), dict(t=8.8, lon=bay[0], lat=bay[1] - 0.02, dist=330, tilt=30, head=0, mm=35)]   # push-in liên tục: 0–2,2 s trôi chậm trên khung Tây Âu (lời: "Austria, England and the Dutch…" — lượt 1 lặn quá sớm, nhãn nước chỉ đứng ~1 s), rồi lặn xuống eo; đuôi 6,5 → 8,8 s = phần hoà
    dates = [[0.0, '1704-02-12'], [2.0, '1704-06-16'], [4.2, '1704-08-01']]
    hero_opt = dict(relief='sm1', palette='sepia', ve=8, cam=cam, routes=routes, borders=dict(src='sm1-1704', dates=dates, a=0.62, edge=2.2, soft=10, hatch=7),
                    places=[dict(id='eng_c', ll=[-1.6, 52.6], name='England'), dict(id='dut_c', ll=[5.6, 52.4], name='Dutch Republic'), dict(id='aus_c', ll=[14.2, 47.6], name='Austria'),
                            dict(id='fra_c', ll=[2.4, 46.9], name='France'), dict(id='spa_c', ll=[-3.6, 39.9], name='Spain'), dict(id='por_c', ll=[-8.0, 39.7], name='Portugal'),
                            dict(id='lisbon', ll=[-9.14, 38.71], name='Lisbon'), dict(id='tetuan', ll=[-5.37, 35.57], name='Tetuan')],
                    exposure=1.0, lodMesh=0)
    places = [dict(a='eng_c', s='England', at=0.15, out=2.3, side='up', gap=0, nodot=True, c=COL['britain'], px=34),
              dict(a='dut_c', s='Dutch Republic', at=0.25, out=2.3, side='up', gap=0, nodot=True, c=COL['britain'], px=32),
              dict(a='aus_c', s='Austria', at=0.35, out=2.0, side='up', gap=0, nodot=True, c=COL['britain'], px=32),
              dict(a='fra_c', s='France', at=0.45, out=2.6, side='up', gap=0, nodot=True, c=COL['france'], px=34),
              dict(a='spa_c', s='Spain', at=0.55, out=3.6, side='up', gap=0, nodot=True, c=COL['spain'], px=34),
              dict(a='por_c', s='Portugal', at=1.0, out=3.4, side='left', gap=0, nodot=True, c=COL['britain'], px=30),
              dict(a='rt:R1704-GIB', s='Anglo-Dutch fleet', at=2.5, out=4.3, side='auto', c=COL['britain'], px=32)]
    p = dict(legend=dict(items=[dict(s='Grand Alliance (England & allies)', c=COL['britain']), dict(s='France', c=COL['france']), dict(s='Spain (Philip V)', c=COL['spain'])], at=0.0, out=DUR),
             counter=[dict(t=0.0, s='Feb 1704'), dict(t=2.0, s='Jun 1704'), dict(t=4.2, s='21 July (O.S.) / 1 Aug (N.S.) 1704')], counterOut=DUR + 0.6,   # bộ đếm nối sang 1a (treatment-patch: "nối từ SM1")
             points=[dict(a='pt:gibraltar', s='Gibraltar', c=COL['spain'], at=0.0, out=4.45, side='right'),
                     dict(a='pt:gibraltar', s='Gibraltar', c=COL['britain'], at=4.4, out=DUR + 0.6, side='right')],   # cùng phía (lượt 1 'auto' tách hai nhãn khi hoà màu)   # đổi phe đúng 1 Aug 1704 N.S. (S012): hai mục nối nhau, cùng neo
             places=places, kind='')
    ban_do = dict(nghieng=[22, 30], be_ngang_km=[2700, 330], dong=[dict(loai='route', t=[0.8, 4.4]), dict(loai='camera', t=[0.0, DUR])], chu_giai=[i['s'] for i in p['legend']['items']],
                  chi_toi='Bay of Gibraltar (1a, 3D vịnh 1704)', lop='sm1-1704', nam=1704, tuyen=['R1704-LIS', 'R1704-GIB'],
                  claims=['T001', 'T002', 'T003', 'T004', 'T005', 'S012', 'S013'])
    return dict(hero_opt=hero_opt, p=p, ban_do=ban_do, ve_tuyen={'R1704-LIS': lis, 'R1704-GIB': gib}, dur=DUR)


def main():
    a = argparse.ArgumentParser(); a.add_argument('--routes', required=True); a.add_argument('--out', required=True); A = a.parse_args()
    S = build(A.routes); json.dump(S, open(A.out, 'w'), ensure_ascii=False, indent=1)
    print('SM1 tuyến', {k: len(v) for k, v in S['ve_tuyen'].items()}, 'nhãn', len(S['p']['places']))


if __name__ == '__main__':
    main()
