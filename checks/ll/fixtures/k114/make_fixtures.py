#!/opt/cine/bin/python
"""Sinh fixture tổng hợp 1.14 (phiên K): một tập kênh 2 giả 120 s có bản đồ chiến lược/inset/ranh (ep-bd/) và một tập ĐỎ-K giả (ep-dok/).
Không có hình; chỉ đặc tả, timeline, log chữ dạng k2.js, manifest. Chạy lại: /opt/cine/bin/python checks/ll/fixtures/k114/make_fixtures.py"""
import json, os
D = os.path.dirname(os.path.abspath(__file__))
J = lambda p, x: json.dump(x, open(os.path.join(D, p), 'w'), ensure_ascii=False, indent=1)
W = lambda p, x: open(os.path.join(D, p), 'w', encoding='utf-8').write(x)
os.makedirs(os.path.join(D, 'ep-bd', 'logs'), exist_ok=True); os.makedirs(os.path.join(D, 'ep-dok'), exist_ok=True)

# ---------------------------------------------------------------- ep-bd: 3 đoạn = 3 chương, 40 s mỗi đoạn
CAP = lambda px: round(px * 0.727, 1)
heroes = {'r_iberia': dict(hero='relief/iberia', dur=8, opt=dict(cam=[dict(t=0, dist=2600, tilt=20), dict(t=8, dist=2400, tilt=22)])),
          'r_iberia2': dict(hero='relief/iberia', dur=8, opt=dict(cam=[dict(t=0, dist=2000, tilt=15), dict(t=8, dist=1900, tilt=15)])),
          'r_bay': dict(hero='relief/gibbay', dur=20, opt=dict(cam=[dict(t=0, dist=8, tilt=50), dict(t=20, dist=6, tilt=55)]))}
strat1 = dict(type='strategic', scene_id='relief/iberia', p=dict(hero='r_iberia', tags=[dict(s='Gibraltar')], nghieng=20, be_ngang_km=[2500, 2300], year=1782, chi_toi=['Gibraltar'],
              lop=['r1782'], dong=[dict(loai='route', t=[0.5, 6.5], id='howe1782'), dict(loai='arrow', t=[4.0, 6.0])],
              chu_giai=[dict(faction_id='gb', mau='#b03a2e', nhan='Britain'), dict(faction_id='es', mau='#c9a227', nhan='Spain'), dict(faction_id='fr', mau='#2e5c8a', nhan='France')]))
strat3 = dict(type='strategic', scene_id='relief/iberia', p=dict(hero='r_iberia2', tags=[dict(s='Gibraltar')], nghieng=15, be_ngang_km=2000, year=1704, chi_toi=['Gibraltar'],
              dong=[dict(loai='fleet', t=[0.0, 5.0])], chu_giai=[dict(faction_id='gb', mau='#b03a2e', nhan='Britain'), dict(faction_id='es', mau='#c9a227', nhan='Spain')]))
segs = [dict(id='01', part='CH1', chuong='1', vo='x', shots=[
            dict(type='timelapse', scene_id='tl/gib20', p=dict(where='Gibraltar')),
            strat1,
            dict(type='scene3d', scene_id='k2/gib-rock', p=dict(where='Gibraltar', src='Source: Drinkwater 1786')),
            dict(type='map', scene_id='relief/gibbay', p=dict(hero='r_bay', where='Bay of Gibraltar'))]),
        dict(id='02', part='CH2', chuong='2', vo='x', shots=[
            dict(type='photo', p=dict(photo='p1')), dict(type='scene3d', scene_id='k2/gib-rock', p=dict(where='Gibraltar', src='Source: Drinkwater 1786')),
            dict(type='card', p=dict(card=dict(title='47 ships of the line'))), dict(type='scene3d', scene_id='k2/gib-lines', p=dict(where='Gibraltar'))]),
        dict(id='03', part='CH3', chuong='3', vo='x', shots=[strat3, dict(type='timelapse', scene_id='tl/gib20', p=dict(where='Gibraltar'))])]
cuts = {'01': [0, 6, 13, 20, 40], '02': [0, 5, 20, 25, 40], '03': [0, 6, 40]}
tl = dict(tong_s=120.0, segments=[], heroes=heroes)
for k, s in enumerate(segs):
    c = cuts[s['id']]; sh = []
    for i, sp in enumerate(s['shots']):
        x = dict(tpl='plate', t0=float(c[i]), t1=float(c[i + 1]), p=dict(sp.get('p') or {}), type=sp['type'])
        if s['id'] == '01' and i == 2: x['in'] = dict(type='dissolve', d=0.7)
        sh.append(x)
    tl['segments'].append(dict(id=s['id'], part=s['part'], t0=40.0 * k, t1=40.0 * (k + 1), frames=960, fadeIn=0, shots=sh))
ep = dict(id='k2c-t9-bd', title='Fixture BD', out='/var/tmp/cine-out/k2c-t9-bd', places=['Gibraltar'], heroes=heroes, segments=segs,
          ban_do=dict(lop='lop-ranh.json', tuyen='routes.geojson', inset='inset.log.json', claims='claims.json'))
import yaml
yaml.safe_dump(ep, open(os.path.join(D, 'ep-bd', 'episode.yaml'), 'w'), allow_unicode=True, sort_keys=False)
J('ep-bd/timeline.json', tl)

def frames(seg, f0, f1, step, items):
    return [dict(f=f, items=[dict(it) for it in items(f)], zones=[]) for f in range(f0, f1, step)]
lbl = dict(s='approx. borders c. 1782 — Cliopatria (Se', cap=CAP(40), box=[60, 990, 760, 1030])
yr = dict(s='1782', cap=CAP(96), box=[1700, 60, 1860, 150])
chip = dict(s='Gibraltar', cap=CAP(40), box=[60, 930, 260, 970])
src = dict(s='Source: Drinkwater 1786', cap=CAP(38), box=[60, 1000, 520, 1040])
L1 = frames('01', 0, 960, 12, lambda f: ([yr, lbl] if 144 <= f < 312 else [chip, src] if 312 <= f < 480 else [chip]))
J('ep-bd/logs/01.log.json', dict(id='01', fmt='16x9', text=L1))
J('ep-bd/logs/02.log.json', dict(id='02', fmt='16x9', text=frames('02', 0, 960, 12, lambda f: [chip, src] if 120 <= f < 480 else [chip])))
J('ep-bd/logs/03.log.json', dict(id='03', fmt='16x9', text=frames('03', 0, 960, 12, lambda f: [dict(yr, s='1704')] if f < 144 else [chip])))

# lớp ranh: Tây Ban Nha / Pháp / Anh (thô), Gibraltar là điểm; biên hiện đại Pyrenees
spain = [[-9.3, 43.2], [-1.8, 43.4], [3.2, 42.4], [0.3, 40.0], [-0.7, 37.6], [-2.1, 36.7], [-5.3, 36.2], [-6.4, 36.8], [-7.4, 37.2], [-6.9, 41.9], [-9.3, 43.2]]
france = [[-1.8, 43.4], [-1.2, 46.2], [-4.6, 48.4], [1.6, 50.9], [8.2, 49.0], [7.5, 43.8], [3.2, 42.4], [-1.8, 43.4]]
gib = [[-5.366, 36.156], [-5.340, 36.156], [-5.339, 36.110], [-5.355, 36.121], [-5.366, 36.156]]
F = lambda g, **p: dict(type='Feature', properties=p, geometry=g)
J('ep-bd/ranh-1782.geojson', dict(type='FeatureCollection', features=[
    F(dict(type='Polygon', coordinates=[spain]), faction_id='es', fill='#c9a227', ten='Spain'),
    F(dict(type='Polygon', coordinates=[france]), faction_id='fr', fill='#2e5c8a', ten='France'),
    F(dict(type='Point', coordinates=[-5.353, 36.135]), faction_id='gb', fill='#b03a2e', ten='Gibraltar', ve='diem')]))
J('ep-bd/gib-polygon.geojson', dict(type='FeatureCollection', features=[F(dict(type='Polygon', coordinates=[gib]), faction_id='gb', fill='#b03a2e', ten='Gibraltar')]))
J('ep-bd/hien-dai.geojson', dict(type='FeatureCollection', features=[F(dict(type='LineString', coordinates=[[-1.78, 43.36], [-0.7, 42.8], [0.7, 42.7], [1.7, 42.5], [3.17, 42.43]]), ten='ES–FR')]))
J('ep-bd/hien-dai-eo-dat.geojson', dict(type='FeatureCollection', features=[F(dict(type='LineString', coordinates=[[-5.36, 36.158], [-5.34, 36.158]]), ten='eo đất')]))
J('ep-bd/lop-ranh.json', dict(W=1920, lop=[
    dict(id='r1782', loai='bien_gioi_lich_su', nam=1782, nguon='Cliopatria v0.2.1 (Seshat)', nguon_doi_chieu='OpenHistoricalMap', lech_tb_px=2.7,
         giay_phep=['CC-BY-4.0', 'CC0'], kieu_mep='lien', be_ngang_km=2500, shot=['01/1'], hinh='ranh-1782.geojson'),
    dict(id='hd2026', loai='bien_gioi_hien_dai', nguon='Natural Earth', giay_phep='PD', be_ngang_km=2500, hinh='hien-dai.geojson')]))
sea = [[-4.14, 50.345], [-4.2, 50.2], [-5.5, 49.6], [-9.0, 47.5], [-10.2, 43.5], [-9.9, 38.5], [-9.3, 36.6], [-6.8, 35.9], [-5.9, 35.93], [-5.6, 35.96],
       [-5.45, 36.03], [-5.40, 36.08], [-5.365, 36.13]]
J('ep-bd/routes.geojson', dict(type='FeatureCollection', features=[
    F(dict(type='LineString', coordinates=sea), id='howe1782', mode='sea', claims=['S056'])]))
J('ep-bd/claims.json', dict(claims=[dict(id='S056', claim_en='Howe relief convoy, 11 Oct 1782'), dict(id='S054', claim_en='Rodney convoy, Jan 1780')]))
J('ep-bd/inset.log.json', dict(W=1920, H=1080, inset=[dict(id='i1', t=[47.5, 50.5], box=[100, 60, 560, 320])]))

# ---------------------------------------------------------------- ep-dok: tập ĐỎ-K giả (T7)
dk = dict(id='k2c-t7-dok', title='Fixture DOK: the Dresden firestorm', rui_ro='do-k', thu_tu='T7', out='/var/tmp/cine-out/k2c-t7-dok',
          numbers=dict(n_toll=dict(text='25,000', claims=['D01'], kind='estimate')),
          segments=[dict(id='01', vo="In February 1945, RAF Bomber Command and the US Eighth Air Force bombed Dresden. Up to 25,000 people were killed, according to the city's historians' commission. Historians still argue about whether the raid was necessary.", shots=[])],
          do_k=dict(tu_cam=['tu-cam-chung.txt', 'tu-cam-t7.txt'], srt='dok.en.srt', mo_ta='description.en.txt', the=['Dresden', 'history', 'firestorm'],
                    claims='claims.json', tai_san='tai-san.json', bieu_tuong_khung='bt-khung.json', thumbnail='thumbs.json', cham_mu='cham-mu-nhay-cam.json',
                    binh_luan_ghim='binh-luan-ghim.txt', truyen_thong=dict(duc=['Müller', 'Bergander'], anh=['Frederick Taylor', 'Webster & Frankland']),
                    khai='g1r-khai.yaml', hang_doi='HANG-DOI-mau.md'))
yaml.safe_dump(dk, open(os.path.join(D, 'ep-dok', 'episode.yaml'), 'w'), allow_unicode=True, sort_keys=False)
W('ep-dok/tu-cam-chung.txt', '# từ cấm chung (mẫu)\nholocaust\nre:\\b(justified|war crime)\\b\n')
W('ep-dok/tu-cam-t7.txt', '# từ cấm tập (mẫu)\nBombenholocaust\nterror bombing\ninnocent city\n')
W('ep-dok/dok.en.srt', "1\n00:00:00,500 --> 00:00:04,000\nIn February 1945, RAF Bomber Command and the US Eighth Air Force bombed Dresden.\n\n2\n00:00:04,100 --> 00:00:08,000\nUp to 25,000 people were killed, according to the city's historians' commission.\n\n3\n00:00:08,100 --> 00:00:11,000\nHistorians still argue about whether the raid was necessary.\n")
W('ep-dok/description.en.txt', 'The bombing of Dresden, February 1945. Facts as of 2026-10-17.\nSources (German): Müller, Schönherr, Widera (eds.), 2010; Götz Bergander, Dresden im Luftkrieg.\nSources (British): Frederick Taylor, Dresden (2004); Webster & Frankland, The Strategic Air Offensive (1961).\n')
J('ep-dok/claims.json', dict(claims=[dict(id='D01', claim_en='Up to 25,000 dead (Dresden historians commission 2010)', khoang=[18000, 25000]),
                                     dict(id='D02', claim_en='The Frauenkirche stood as a ruin for 50 years', truyen_thong=['duc', 'anh'])]))
J('ep-dok/tai-san.json', [dict(id='frauenkirche_ruin', bieu_tuong='khong', the=['toa_nha'], dung_o=['01/0']),
                          dict(id='union_flag_1945', bieu_tuong='co_lich_su', the=['co'], dung_o=['01/1']),
                          dict(id='altmarkt_pyre', bieu_tuong='khong', the=['thi_the'], dung_o=[])])
J('ep-dok/bt-khung.json', [dict(f=f, id='union_flag_1945', pct=1.5) for f in range(24, 72)])
J('ep-dok/thumbs.json', [dict(id='A', the=['toa_nha'], chu='50 YEARS A RUIN'), dict(id='B', the=[], chu='')])
J('ep-dok/cham-mu-nhay-cam.json', dict(vai=[dict(vai='G1', co=[], diem=4.5), dict(vai='G2', co=[], diem=4.0), dict(vai='G3', co=[], diem=4.5)]))
W('ep-dok/binh-luan-ghim.txt', "Sources: Müller et al. 2010; Taylor 2004. Comments that deny or minimise any wartime atrocity, or praise any side's violence, will be removed.\n")
yaml.safe_dump([dict(ma=m, noi_dung=f'Chủ dự án đã xem và xác nhận mục {m} cho tập fixture (mẫu tổng hợp).', nguoi_ky='Chủ dự án (HQ)', vai='chu_du_an',
                     ngay='2026-10-17', ket_luan='dong_y') for m in ('K-R2.the', 'K-R5.the', 'K-R6.the', 'K-R9.tu_chan')],
               open(os.path.join(D, 'ep-dok', 'g1r-khai.yaml'), 'w'), allow_unicode=True, sort_keys=False)
W('ep-dok/HANG-DOI-mau.md', """# Hàng đợi (mẫu fixture 1.14)

| Thứ tự | Tập | Đề tài (tên làm việc) | Mức | Trạng thái |
|---|---|---|---|---|
| T3 | K2C-T3-01 | Gibraltar | VÀNG | — |
| T4 | — | London 1666 | XANH | — |
| T5 | — | Boston | XANH | — |
| **Cổng** | — | cổng | — | — |
| T6 | — | (XANH) | XANH | — |
| T7 | k2c-t7-dok | **Dresden 1945** | **ĐỎ-K** | — |
| T8 | — | (XANH) | XANH | — |
| T9 | — | (XANH) | XANH | — |
| T10 | — | — | XANH | — |

Ghi chú sau bảng.
""")
