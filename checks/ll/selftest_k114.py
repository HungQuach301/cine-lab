#!/opt/cine/bin/python
"""Tự kiểm luật 1.14 (phiên K, 17/10/2026): BD-1…BD-8 (NC-BD §3.4; chủ dự án duyệt B1–B8), NC-H2/H3/H1 loại `strategic` (B3), K-R1…K-R9
ĐỎ-K (NC-LS2 §5.3; YY5). Mỗi luật ≥ 1 ca ĐẠT + ≥ 1 ca TRƯỢT. Dữ liệu:
  fixtures/k114/ep-bd/    tập giả 120 s, 3 chương: 2 shot strategic, lớp ranh 1782 + biên hiện đại, tuyến biển Plymouth → Gibraltar, inset, log chữ k2.js
  fixtures/k114/ep-dok/   tập ĐỎ-K giả (T7): từ cấm, srt, mô tả, claims, tài sản + khung cờ, thumbnail, chấm mù, bình luận ghim, khai G1-R, HANG-DOI mẫu
  fixtures/k113/          T2 L5 (đặc tả + timeline) cho NC-H2 loại strategic trên phim thật
  checks/ll/data/         Natural Earth 1:10m disputed + land (PD)
Sinh lại fixture tổng hợp: fixtures/k114/make_fixtures.py. Không gọi mạng/API; biến thể ghi vào thư mục tạm của hệ thống.

  /opt/cine/bin/python checks/ll/selftest_k114.py        mã thoát 0 = mọi ca đúng kỳ vọng
"""
import copy, gzip, json, os, shutil, sys, tempfile

import yaml

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, ROOT)
from checks.ll import q_bando as B, q_dok as K, q_noi as N, cap112  # noqa: E402

FX = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures')
BD = os.path.join(FX, 'k114', 'ep-bd'); DK = os.path.join(FX, 'k114', 'ep-dok')
R = []
TMP = tempfile.mkdtemp(prefix='k114-')


def case(rule, name, got, expect_fail):
    got = list(got) if got else []
    R.append((rule, name, 'bắt lỗi' if expect_fail else 'sạch', bool(got) == expect_fail, got[:2]))


def bad(x, *muc):
    """lỗi + thiếu của một kết quả; muc = chữ (a)…(f) cần có"""
    L = x['loi'] + x['thieu']
    return [y for y in L if not muc or any(y.startswith(f'({m})') for m in muc)]


E0 = yaml.safe_load(open(os.path.join(BD, 'episode.yaml'))); TL0 = json.load(open(os.path.join(BD, 'timeline.json'))); LOGS = os.path.join(BD, 'logs')


def bd(E=None, TL=None, logs=LOGS, **over):
    E = E or copy.deepcopy(E0); TL = TL or copy.deepcopy(TL0)
    for k, v in over.items(): E.setdefault('ban_do', {})[k] = v
    return B.check(E, TL, BD, logs)


def spec(E, seg, i): return next(s for s in E['segments'] if s['id'] == seg)['shots'][i]


def tshot(TL, seg, i): return next(s for s in TL['segments'] if s['id'] == seg)['shots'][i]


def lop(**kw):
    M = json.load(open(os.path.join(BD, 'lop-ranh.json')))
    for L in M['lop']: L['hinh'] = os.path.join(BD, L['hinh'])
    for lid, ch in kw.items():
        L = next((x for x in M['lop'] if x['id'] == lid), None)
        if ch is None: M['lop'] = [x for x in M['lop'] if x['id'] != lid]
        elif L is None: M['lop'].append(ch)
        else: L.update(ch)
    return M


def logs_with(fn):
    d = tempfile.mkdtemp(dir=TMP)
    for f in os.listdir(LOGS):
        J = json.load(open(os.path.join(LOGS, f))); fn(f[:2], J); json.dump(J, open(os.path.join(d, f), 'w'), ensure_ascii=False)
    return d


R0 = bd()
# =============================================================== định nghĩa strategic (B3)
case('STRAT', 'nghiêng 20°, bề ngang 2 500–2 300 km, relief → hợp lệ', [] if B.strat_info('strategic', 'relief/x', {}, dict(nghieng=20, be_ngang_km=[2500, 2300]), {})[0] else ['không hợp lệ'], False)
case('STRAT', 'nghiêng 35° → ngoài định nghĩa', B.strat_info('strategic', 'relief/x', {}, dict(nghieng=35, be_ngang_km=2500), {})[1], True)
case('STRAT', 'bề ngang 6 000 km → ngoài định nghĩa', B.strat_info('strategic', 'relief/x', {}, dict(nghieng=20, be_ngang_km=6000), {})[1], True)
case('STRAT', 'bề ngang 250 km (tầm vùng) → ngoài định nghĩa', B.strat_info('strategic', 'relief/x', {}, dict(nghieng=20, be_ngang_km=250), {})[1], True)
case('STRAT', 'cảnh map/globe khai strategic → ngoài định nghĩa (NC-H2 vẫn áp)', B.strat_info('strategic', 'map/globe', {}, dict(nghieng=0, be_ngang_km=3000), {})[1], True)
case('STRAT', 'không khai nghieng/be_ngang_km → ngoài định nghĩa', B.strat_info('strategic', 'relief/x', {}, {}, {})[1], True)

# =============================================================== NC-H1/H2/H3 với strategic
RN = N.nc_tap(copy.deepcopy(E0), copy.deepcopy(TL0))
case('NC-H2', f"fixture: 2 shot strategic hợp lệ (AGL ≈ 1 900–2 400 km) loại khỏi NC-H2 → {RN['NC-H2']['val']}", RN['NC-H2']['loi'], False)
E1 = copy.deepcopy(E0); spec(E1, '01', 1)['p']['nghieng'] = 40; TL1 = copy.deepcopy(TL0); tshot(TL1, '01', 1)['p']['nghieng'] = 40
r1 = N.nc_tap(E1, TL1)
case('NC-H2', 'strategic 01/1 nghiêng 40° (sai định nghĩa) → tính như bản đồ tầm cao → NC-H2 (b) TRƯỢT', bad(r1['NC-H2'], 'b'), True)
case('NC-H3', f"fixture: mẫu số 3D địa lý không gồm strategic hợp lệ → {RN['NC-H3']['val']}", RN['NC-H3']['loi'], False)
E1b = copy.deepcopy(E1); spec(E1b, '03', 0)['p']['nghieng'] = 40; TL1b = copy.deepcopy(TL1); tshot(TL1b, '03', 0)['p']['nghieng'] = 40
r1b = N.nc_tap(E1b, TL1b)
case('NC-H3', f"hai strategic sai định nghĩa → tính vào 3D địa lý: {r1b['NC-H3']['val']} → (a) TRƯỢT", bad(r1b['NC-H3'], 'a'), True)
E2 = copy.deepcopy(E0); spec(E2, '01', 1)['p'].update(noi='thanh_pho', where='Gibraltar, Gib.')
case('NC-H1', 'strategic khai noi: thanh_pho + chip dạng thành phố → KHÔNG là đơn vị thành phố, ĐẠT', N.nc_tap(E2, copy.deepcopy(TL0))['NC-H1']['loi'], False)
E3 = copy.deepcopy(E2); spec(E3, '01', 1)['type'] = 'map'
case('NC-H1', 'cùng shot đổi type map → thành phố không lớp nhà → TRƯỢT (a)', bad(N.nc_tap(E3, copy.deepcopy(TL0))['NC-H1'], 'a'), True)
ET = yaml.safe_load(gzip.open(os.path.join(FX, 'k113', 't2l5-episode.yaml.gz'))); TT = json.load(gzip.open(os.path.join(FX, 'k113', 't2l5-timeline.json.gz')))
base2 = N.nc_tap(copy.deepcopy(ET), copy.deepcopy(TT))['NC-H2']['loi']
for s in ET['segments']:
    for sh in s['shots']:
        h = (sh.get('p') or {}).get('hero')
        if h in ('r04_state', 'g05_china'): sh['type'] = 'strategic'; sh.setdefault('p', {}).update(nghieng=10, be_ngang_km=1500 if h == 'r04_state' else 3000)
r2 = N.nc_tap(ET, copy.deepcopy(TT))['NC-H2']['loi']
case('NC-H2', 'T2 L5: r04_state (bản đồ nổi 222 km) khai strategic hợp lệ → hết khỏi lỗi NC-H2', [x for x in r2 if 'r04_state' in x] if any('r04_state' in x for x in base2) else ['ca gốc không có r04_state'], False)
case('NC-H2', 'T2 L5: g05_china (map/globe) khai strategic → vẫn TRƯỢT NC-H2', [x for x in r2 if 'g05_china' in x], True)

# =============================================================== BD-1
case('BD-1', f"fixture: {R0['BD-1']['val']} → ĐẠT", R0['BD-1']['loi'] + R0['BD-1']['thieu'], False)
TLa = copy.deepcopy(TL0); TLa['tong_s'] = 80.0
case('BD-1', '13 s / 80 s = 16,3 % > 15 % → (a)', bad(bd(TL=TLa)['BD-1'], 'a'), True)
TLb = copy.deepcopy(TL0); tshot(TLb, '01', 1)['t1'] = 15.0; tshot(TLb, '01', 2)['t0'] = 15.0
case('BD-1', 'strategic 9 s > 8 s → (b)', bad(bd(TL=TLb)['BD-1'], 'b'), True)
TLb8 = copy.deepcopy(TL0); tshot(TLb8, '01', 1)['t1'] = 14.0; tshot(TLb8, '01', 2)['t0'] = 14.0
case('BD-1', 'strategic đúng 8,0 s → ĐẠT (b), sát ngưỡng được nêu tên', bad(bd(TL=TLb8)['BD-1'], 'b') or ([] if bd(TL=TLb8)['BD-1']['sat_nguong'] else ['không nêu sát ngưỡng']), False)
Ec = copy.deepcopy(E0)
for s in Ec['segments']: s['chuong'] = '1'
x = spec(Ec, '02', 3); x.update(type='strategic', scene_id='relief/iberia'); x['p'].update(nghieng=10, be_ngang_km=900, chi_toi=['Gibraltar'], dong=[dict(loai='arrow', t=[0, 12])])
TLc = copy.deepcopy(TL0); tshot(TLc, '02', 3)['type'] = 'strategic'
case('BD-1', '3 shot strategic cùng chương → (c)', bad(bd(Ec, TLc)['BD-1'], 'c'), True)
Ed = copy.deepcopy(E0); spec(Ed, '01', 2).update(type='strategic')
case('BD-1', 'hai shot strategic liền nhau (01/1, 01/2) → (d)', bad(bd(Ed)['BD-1'], 'd'), True)
Ee = copy.deepcopy(E0); spec(Ee, '01', 1)['p']['nghieng'] = 40
case('BD-1', 'nghiêng 40° → (e) ngoài định nghĩa', bad(bd(Ee)['BD-1'], 'e'), True)
Ef = copy.deepcopy(E0); spec(Ef, '01', 1)['p']['chi_toi'] = ['Cádiz']
case('BD-1', 'chỉ tới Cádiz mà shot kề là Gibraltar → (f)', bad(bd(Ef)['BD-1'], 'f'), True)
Ef2 = copy.deepcopy(E0); spec(Ef2, '01', 1)['p']['chu_giai'].append(dict(faction_id='nl', mau='#e07b00'))
case('BD-1', 'chú giải 4 phe > 3 → (f)', bad(bd(Ef2)['BD-1'], 'f'), True)
case('BD-1', 'log không có nhãn năm trong shot strategic → (f) mốc thời gian',
     bad(bd(logs=logs_with(lambda s, J: [e.__setitem__('items', [i for i in e['items'] if i['s'] != '1782']) for e in J['text']]))['BD-1'], 'f'), True)
case('BD-1', 'TIME_RE: "1782", "c. 1779–83", "11 Oct 1782", "Day 312" là mốc; "Source: Drinkwater 1786", nhãn ranh thì không',
     [] if all(B.TIME_RE.match(x) for x in ('1782', 'c. 1779–83', '11 Oct 1782', 'Oct 11, 1782', 'Day 312')) and not any(B.TIME_RE.match(x) for x in ('Source: Drinkwater 1786', 'approx. borders c. 1782 — Cliopatria')) else ['nhận sai'], False)
case('BD-1', 'chỉ còn dòng nguồn có năm trong shot strategic → (f) (dòng nguồn không phải mốc thời gian)',
     bad(bd(logs=logs_with(lambda s, J: [e.__setitem__('items', [dict(i, s='Source: Drinkwater 1786') if i['s'] == '1782' else i for i in e['items']]) for e in J['text']]))['BD-1'], 'f'), True)
case('BD-1', 'tập không có strategic → KHÔNG ÁP', [] if B.check(dict(segments=[]), dict(tong_s=10, segments=[]), BD)['BD-1'].get('ket_qua') == 'KHÔNG ÁP' else ['áp'], False)

# =============================================================== BD-2
case('BD-2', f"fixture: route 0,5–6,5 s trên shot 7 s (86 %) → ĐẠT", R0['BD-2']['loi'], False)
E = copy.deepcopy(E0); spec(E, '01', 1)['p']['dong'] = [dict(loai='route', t=[2.0, 7.0])]
case('BD-2', 'chuyển động bắt đầu 2,0 s > 1,5 s → (b)', bad(bd(E)['BD-2'], 'b'), True)
E = copy.deepcopy(E0); spec(E, '01', 1)['p']['dong'] = [dict(loai='route', t=[0.5, 3.5])]
case('BD-2', 'chuyển động phủ 3 s / 7 s = 43 % < 60 % → (c)', bad(bd(E)['BD-2'], 'c'), True)
E = copy.deepcopy(E0); spec(E, '01', 1)['p']['dong'] = [dict(loai='label', t=[0, 7])]
case('BD-2', 'không có phần tử route/arrow/fleet/front/blockade → (a)', bad(bd(E)['BD-2'], 'a'), True)
case('BD-2', 'cấp: Cảnh báo (không Chặn) khi có lỗi', [] if not cap112.cap('BD-2', bd(E)['BD-2'])[1] and cap112.cap('BD-2', bd(E)['BD-2'])[2] else ['cấp sai'], False)

# =============================================================== BD-3
case('BD-3', f"fixture: {R0['BD-3']['val']} → ĐẠT", R0['BD-3']['loi'] + R0['BD-3']['thieu'], False)
small = logs_with(lambda s, J: [i.__setitem__('cap', round(30 * 0.727, 1)) for e in J['text'] for i in e['items'] if i['s'].startswith('approx.')])
case('BD-3', 'nhãn ranh 30 px < 38 px → (a)', bad(bd(logs=small)['BD-3'], 'a'), True)
half = logs_with(lambda s, J: [e.__setitem__('items', [i for i in e['items'] if not (i['s'].startswith('approx.') and e['f'] % 24)]) for e in J['text']])
case('BD-3', 'nhãn ranh chỉ ở 1/2 số khung → (a) < 95 %', bad(bd(logs=half)['BD-3'], 'a'), True)
wrong = logs_with(lambda s, J: [i.__setitem__('s', i['s'].replace('1782', '1783')) for e in J['text'] for i in e['items'] if i['s'].startswith('approx.')])
r3 = bd(logs=wrong)['BD-3']
case('BD-3', 'nhãn "c. 1783" trên lớp nam 1782 → (c) (K thêm; cấp Cảnh báo)', bad(r3, 'c') if not cap112.cap('BD-3', r3)[1] else ['(c) bị tính Chặn'], True)
case('BD-3', 'nhãn sai chữ "borders approx. c. 1782" → không khớp regex → (a)',
     bad(bd(logs=logs_with(lambda s, J: [i.__setitem__('s', 'borders approx. c. 1782 — Cliopatria') for e in J['text'] for i in e['items'] if i['s'].startswith('approx.')]))['BD-3'], 'a'), True)
case('BD-3', 'không có log chữ → THIẾU (a), cấp Chặn', cap112.cap('BD-3', bd(logs=None)['BD-3'])[1], True)

# =============================================================== BD-4
case('BD-4', f"fixture: {R0['BD-4']['val']} → ĐẠT", R0['BD-4']['loi'], False)
case('BD-4', 'thiếu nguon_doi_chieu → (a)', bad(bd(lop=lop(r1782=dict(nguon_doi_chieu=None)))['BD-4'], 'a'), True)
case('BD-4', 'giấy phép CC-BY-SA-4.0 → (b)', bad(bd(lop=lop(r1782=dict(giay_phep='CC-BY-SA-4.0')))['BD-4'], 'b'), True)
case('BD-4', 'giấy phép viết "CC BY 4.0" → chuẩn hoá thành CC-BY-4.0, ĐẠT', bad(bd(lop=lop(r1782=dict(giay_phep='CC BY 4.0')))['BD-4'], 'b'), False)
case('BD-4', 'lệch 5,1 px, mép liền → (c)', bad(bd(lop=lop(r1782=dict(lech_tb_px=5.1)))['BD-4'], 'c'), True)
case('BD-4', 'lệch 5,1 px, mép mềm → ĐẠT', bad(bd(lop=lop(r1782=dict(lech_tb_px=5.1, kieu_mep='mem')))['BD-4']), False)
case('BD-4', 'nguồn đối chiếu trùng nguồn chính → (d)', bad(bd(lop=lop(r1782=dict(nguon_doi_chieu='Cliopatria v0.2.1 (Seshat)')))['BD-4'], 'd'), True)
E = copy.deepcopy(E0); spec(E, '03', 0)['p']['lop'] = ['r1704']
case('BD-4', 'shot trỏ lớp r1704 không có trong manifest → (a)', bad(bd(E)['BD-4'], 'a'), True)

# =============================================================== BD-5
case('BD-5', 'fixture: biên hiện đại Pyrenees (xa mọi vùng NE disputed) → ĐẠT', R0['BD-5']['loi'] + R0['BD-5']['thieu'], False)
eo = dict(id='hd-eo', loai='bien_gioi_hien_dai', nguon='—', giay_phep='PD', be_ngang_km=2500, hinh=os.path.join(BD, 'hien-dai-eo-dat.geojson'))
case('BD-5', 'biên hiện đại vẽ trên eo đất Gibraltar (36,158°; NE polygon dừng ở 36,141°) → (a) nhờ đệm 10 km', bad(bd(lop=lop(**{'hd-eo': eo}))['BD-5'], 'a'), True)
import numpy as np  # noqa: E402
case('BD-5', 'đường cách polygon NE Gibraltar ≈ 6,6 km (36,20°) → bắt (≤ 10 km)', [x for x in B.line_vs_disputed([(np.array([[-5.40, 36.20], [-5.30, 36.20]]), False)])], True)
case('BD-5', 'đường cách ≈ 17,6 km (36,30°) → ĐẠT', [x for x in B.line_vs_disputed([(np.array([[-5.40, 36.30], [-5.30, 36.30]]), False)])], False)
gp = dict(id='gibp', loai='bien_gioi_lich_su', nam=1782, nguon='OHM', nguon_doi_chieu='Cliopatria', lech_tb_px=1, giay_phep='CC0', be_ngang_km=2500, hinh=os.path.join(BD, 'gib-polygon.geojson'))
case('BD-5', 'Gibraltar vẽ polygon ở khung 2 500 km (≈ 3,8 px) → (b) phải là điểm', bad(bd(lop=lop(gibp=gp))['BD-5'], 'b'), True)
case('BD-5', 'cùng polygon ở khung 300 km (≈ 32 px) → ĐẠT (b)', bad(bd(lop=lop(gibp=dict(gp, be_ngang_km=300)))['BD-5'], 'b'), False)

# =============================================================== BD-6
case('BD-6', f"fixture: tuyến biển Plymouth → quanh Bồ Đào Nha → Gibraltar → ĐẠT ({R0['BD-6']['val']})", R0['BD-6']['loi'], False)
TU = json.load(open(os.path.join(BD, 'routes.geojson')))
st = copy.deepcopy(TU); st['features'][0]['geometry']['coordinates'] = [[-4.14, 50.345], [-5.365, 36.13]]
r6 = bd(tuyen=st)['BD-6']
case('BD-6', f"tuyến thẳng Plymouth → Gibraltar cắt Iberia → (a) ({'; '.join(r6['loi'])[:90]})", bad(r6, 'a'), True)
nc = copy.deepcopy(TU); nc['features'][0]['properties']['claims'] = []
case('BD-6', 'tuyến không có claim → (b)', bad(bd(tuyen=nc)['BD-6'], 'b'), True)
uc = copy.deepcopy(TU); uc['features'][0]['properties']['claims'] = ['S999']
case('BD-6', 'claim S999 không có trong claims → (c)', bad(bd(tuyen=uc)['BD-6'], 'c'), True)
ld = copy.deepcopy(st); ld['features'][0]['properties']['mode'] = 'land'
case('BD-6', 'tuyến đất liền (mode land) cắt đất → không áp (a)', bad(bd(tuyen=ld)['BD-6'], 'a'), False)
E = copy.deepcopy(E0); E['ban_do'].pop('tuyen')
case('BD-6', 'shot có phần tử route mà không có routes.geojson → THIẾU', bd(E)['BD-6']['thieu'], True)

# =============================================================== BD-7 (+ B8)
case('BD-7', f"fixture: {R0['BD-7']['val']} → ĐẠT", R0['BD-7']['loi'], False)
E = copy.deepcopy(E0); spec(E, '03', 0)['p']['chu_giai'][1]['mau'] = '#d4b030'
case('BD-7', 'Tây Ban Nha chương 3 đổi màu #d4b030 (lớp/chương 1: #c9a227) → (a)', bad(bd(E)['BD-7'], 'a'), True)
G = json.load(open(os.path.join(BD, 'ranh-1782.geojson'))); G['features'][1]['properties']['fill_the'] = 'co'
case('BD-7', 'Pháp tô bằng cờ (fill_the co) → (b)', bad(bd(lop=lop(r1782=dict(hinh=None, features=G['features'])))['BD-7'], 'b'), True)
nat = dict(type='Feature', properties=dict(ten='Haudenosaunee', ban_dia=True, fill='none'), geometry=dict(type='Polygon', coordinates=[[[-78, 42], [-74, 42], [-74, 44], [-78, 44], [-78, 42]]]))
case('BD-7', 'B8: thực thể bản địa có tên fill none → (c)', bad(bd(lop=lop(na=dict(id='na', loai='bien_gioi_lich_su', nam=1754, nguon='OHM', nguon_doi_chieu='Newberry', lech_tb_px=2, giay_phep='CC0', km_px=1.5, features=[nat])))['BD-7'], 'c'), True)
nat2 = copy.deepcopy(nat); nat2['properties']['fill'] = '#8a6d3b'
case('BD-7', 'B8: cùng thực thể tô màu riêng → ĐẠT', bad(bd(lop=lop(na=dict(id='na', loai='bien_gioi_lich_su', nam=1754, nguon='OHM', nguon_doi_chieu='Newberry', lech_tb_px=2, giay_phep='CC0', km_px=1.5, features=[nat2])))['BD-7']), False)

# =============================================================== BD-8
IN = json.load(open(os.path.join(BD, 'inset.log.json')))
ins = lambda **kw: dict(IN, inset=[dict(IN['inset'][0], **kw)])
case('BD-8', 'fixture: inset 5,8 % góc trên trái, 3 s, 2,5 s sau cắt cứng → ĐẠT', R0['BD-8']['loi'] + R0['BD-8']['thieu'], False)
case('BD-8', 'inset 15,6 % khung → (a)', bad(bd(inset=ins(box=[100, 60, 700, 620]))['BD-8'], 'a'), True)
case('BD-8', 'inset góc trên phải không khai lý do → (b)', bad(bd(inset=ins(box=[1360, 60, 1820, 320]))['BD-8'], 'b'), True)
case('BD-8', 'inset góc trên phải, khai inset_goc tren_phai + lý do (huy hiệu bảng điểm trên trái) → ĐẠT (b)',
     bad(bd(inset=ins(box=[1360, 60, 1820, 320], inset_goc='tren_phai', ly_do='góc trên trái có bảng điểm vây hãm'))['BD-8'], 'b'), False)
case('BD-8', 'inset sát mép trên (y0 = 20 px < 54 px an toàn) → (b)', bad(bd(inset=ins(box=[100, 20, 560, 280]))['BD-8'], 'b'), True)
case('BD-8', 'inset 5 s → (c)', bad(bd(inset=ins(t=[47.5, 52.5]))['BD-8'], 'c'), True)
ov = logs_with(lambda s, J: [e['items'].append(dict(s='Bay of Gibraltar', cap=29.1, box=[500, 100, 760, 140])) for e in J['text']] if s == '02' else None)
case('BD-8', 'chip nơi chồng một phần lên inset → (d)', bad(bd(logs=ov)['BD-8'], 'd'), True)
oc = logs_with(lambda s, J: [e.__setitem__('occ', [[540, 300, 700, 400]]) for e in J['text']] if s == '02' else None)
case('BD-8', 'hộp LL.occ (sticker) giao inset → (d)', bad(bd(logs=oc)['BD-8'], 'd'), True)
case('BD-8', 'inset 62,0–64,9 s trong thẻ số (card 60–65 s) → (e) thẻ số', [x for x in bad(bd(inset=ins(t=[62.0, 64.9]))['BD-8'], 'e') if 'thẻ số' in x], True)
case('BD-8', 'inset 45,5–48,5 s: 0,5 s sau cắt cứng 45 s → (e) cắt cứng', [x for x in bad(bd(inset=ins(t=[45.5, 48.5]))['BD-8'], 'e') if 'cắt cứng' in x], True)
case('BD-8', 'inset 13,5–16,5 s: shot vào bằng hoà (dissolve) → không phải cắt cứng, ĐẠT', bad(bd(inset=ins(t=[13.5, 16.5]))['BD-8'], 'e'), False)
case('BD-8', 'inset 42,0–44,9 s trong ảnh lưu trữ (photo 40–45 s) → (e) lưu trữ', [x for x in bad(bd(inset=ins(t=[42.0, 44.9]))['BD-8'], 'e') if 'lưu trữ' in x], True)

# =============================================================== K-R (ĐỎ-K)
D0 = yaml.safe_load(open(os.path.join(DK, 'episode.yaml')))


def dk(E=None, hd=None, **do):
    E = E or copy.deepcopy(D0)
    for k, v in do.items(): E['do_k'][k] = v
    return K.check(E, None, DK, None, hd)


def tmpf(name, text):
    p = os.path.join(TMP, name); open(p, 'w', encoding='utf-8').write(text); return p


RK = dk()
for k in ('K-R1', 'K-R2', 'K-R3', 'K-R4', 'K-R5', 'K-R6', 'K-R7', 'K-R8', 'K-R9'):
    case(k, f"fixture ĐỎ-K: {RK[k]['val'][:90]} → ĐẠT", RK[k]['loi'] + RK[k]['thieu'], False)
E = copy.deepcopy(D0); E.pop('rui_ro')
case('K-R', 'tập không khai rui_ro: do-k → mọi K-R KHÔNG ÁP', [k for k, v in K.check(E, None, DK).items() if v.get('ket_qua') != 'KHÔNG ÁP'], False)
case('K-R', '"rui_ro: ĐỎ-K" (chữ hoa, có dấu) → bật', [] if K.la_do_k(dict(rui_ro='ĐỎ-K')) else ['không bật'], False)
# K-R1
case('K-R1', 'thẻ "Bombenholocaust" → TRƯỢT', dk(the=['Dresden', 'Bombenholocaust'])['K-R1']['loi'], True)
E = copy.deepcopy(D0); E['title'] = 'The Dresden Holocausts'
case('K-R1', 'tiêu đề "Holocausts" (số nhiều, hoa) → TRƯỢT', dk(E)['K-R1']['loi'], True)
case('K-R1', 'mô tả có "terror bombing" → TRƯỢT', dk(mo_ta=tmpf('mt1.txt', 'This was terror bombing. Facts as of 2026.'))['K-R1']['loi'], True)
case('K-R1', 'regex "war crime" trong srt → TRƯỢT', dk(srt=tmpf('a.srt', '1\n00:00:00,000 --> 00:00:01,000\nIt was a war crime.\n'))['K-R1']['loi'], True)
case('K-R1', 'không đọc được danh sách từ cấm → THIẾU', dk(tu_cam=['khong-co.txt'])['K-R1']['thieu'], True)
# K-R2
case('K-R2', 'cờ lịch sử 3 % khung → (c)', bad(dk(bieu_tuong_khung=[dict(f=f, id='union_flag_1945', pct=3.0) for f in range(24, 48)])['K-R2'], 'c'), True)
case('K-R2', 'cờ lịch sử hiện liền 4 s → (c)', bad(dk(bieu_tuong_khung=[dict(f=f, id='union_flag_1945', pct=1.0) for f in range(0, 96)])['K-R2'], 'c'), True)
case('K-R2', 'cờ lịch sử 4 lần → (c)', bad(dk(bieu_tuong_khung=[dict(f=f, id='union_flag_1945', pct=1.0) for k in range(4) for f in range(k * 100, k * 100 + 24)])['K-R2'], 'c'), True)
A = json.load(open(os.path.join(DK, 'tai-san.json'))); A2 = copy.deepcopy(A); A2.append(dict(id='swastika_banner', bieu_tuong='cuc_doan', dung_o=['01/3']))
case('K-R2', 'tài sản cuc_doan dùng ở shot → (b)', bad(dk(tai_san=A2)['K-R2'], 'b'), True)
A3 = copy.deepcopy(A); A3[0].pop('bieu_tuong')
case('K-R2', 'tài sản thiếu bieu_tuong → (a)', bad(dk(tai_san=A3)['K-R2'], 'a'), True)
case('K-R2', 'không có khung đo + có cờ dùng ở shot → THIẾU mục khai K-R2.do', [x for x in dk(bieu_tuong_khung=None)['K-R2']['thieu'] if 'K-R2.do' in x], True)
KH = yaml.safe_load(open(os.path.join(DK, 'g1r-khai.yaml')))
kd = KH + [dict(KH[0], ma='K-R2.do', noi_dung='Chủ dự án xem từng khung có cờ Anh 1945: ≤ 2 % diện tích, ≤ 3 s, 2 lần.')]
case('K-R2', 'không có khung đo, có khai K-R2.do đã ký → ĐẠT', dk(bieu_tuong_khung=None, khai=kd)['K-R2']['thieu'], False)
# K-R3
case('K-R3', 'manifest có biên hiện đại trên eo đất Gibraltar → TRƯỢT', K.kr3(dict(copy.deepcopy(D0), ban_do=dict(lop=lop(**{'hd-eo': eo}))), None, DK)[0]['loi'], True)
case('K-R3', 'lớp không khai loai → TRƯỢT', K.kr3(dict(copy.deepcopy(D0), ban_do=dict(lop=lop(hd2026=dict(loai=None)))), None, DK)[0]['loi'], True)
E = copy.deepcopy(E0); E.pop('ban_do')
case('K-R3', 'tập có shot bản đồ mà không manifest lớp → cần khai K-R3.khong_ranh', K.kr3(E, copy.deepcopy(TL0), BD)[1], True)
# K-R4
CL = json.load(open(os.path.join(DK, 'claims.json'))); CL2 = copy.deepcopy(CL); CL2['claims'][0].pop('khoang')
case('K-R4', 'claim D01 mất khoảng và chỉ 1 nguồn → TRƯỢT', dk(claims=CL2)['K-R4']['loi'], True)
CL3 = copy.deepcopy(CL2); CL3['claims'][0]['nguon'] = [dict(ten='Müller 2010', truyen_thong='duc'), dict(ten='Taylor 2004', truyen_thong='anh')]
case('K-R4', 'claim D01 không khoảng nhưng 2 truyền thống → ĐẠT', dk(claims=CL3)['K-R4']['loi'], False)
case('K-R4', 'câu "hundreds of thousands died" không nối số khai → TRƯỢT',
     dk(srt=tmpf('b.srt', '1\n00:00:00,000 --> 00:00:02,000\nSome claim that hundreds of thousands died.\n'))['K-R4']['loi'], True)
# K-R5
A5 = copy.deepcopy(A); A5[2]['dung_o'] = ['01/2']
case('K-R5', 'tài sản thi_the dùng ở shot → TRƯỢT', dk(tai_san=A5)['K-R5']['loi'], True)
# K-R6
case('K-R6', 'thumbnail thẻ cờ → TRƯỢT', dk(thumbnail=[dict(id='C', the=['co'], chu='')])['K-R6']['loi'], True)
case('K-R6', 'thumbnail số "135,000" không có trong claims → TRƯỢT', dk(thumbnail=[dict(id='C', the=[], chu='135,000 DEAD?')])['K-R6']['loi'], True)
case('K-R6', 'thumbnail chữ "TERROR BOMBING" → TRƯỢT', dk(thumbnail=[dict(id='C', the=[], chu='TERROR BOMBING')])['K-R6']['loi'], True)
# K-R7
HD = open(os.path.join(DK, 'HANG-DOI-mau.md'), encoding='utf-8').read()
case('K-R7', 'T8 VÀNG liền sau → (b)', bad(dk(hang_doi=tmpf('h1.md', HD.replace('| T8 | — | (XANH) | XANH |', '| T8 | — | Detroit | VÀNG |')))['K-R7'], 'b'), True)
case('K-R7', 'T9 cũng ĐỎ-K (cửa sổ T6–T9 có 2) → (a)', bad(dk(hang_doi=tmpf('h2.md', HD.replace('| T9 | — | (XANH) | XANH |', '| T9 | — | Berlin | ĐỎ-K |')))['K-R7'], 'a'), True)
case('K-R7', 'T10 ĐỎ-K (cách 3 tập: T7–T10 có 2) → (a)', bad(dk(hang_doi=tmpf('h3.md', HD.replace('| T10 | — | — | XANH |', '| T10 | — | Berlin | ĐỎ-K |')))['K-R7'], 'a'), True)
case('K-R7', 'T11 ĐỎ-K (cách 4 tập) → ĐẠT (a)', bad(dk(hang_doi=tmpf('h4.md', HD + '\n| Thứ tự | Tập | Đề tài | Mức |\n|---|---|---|---|\n| T11 | — | x | ĐỎ-K |\n'))['K-R7'], 'a'), False)
E = copy.deepcopy(D0); E['thu_tu'] = 'T4'
case('K-R7', 'tập ĐỎ-K đặt ở T4 → (c), (d)', bad(dk(E)['K-R7'], 'c', 'd'), True)
case('K-R7', 'T8 chưa xếp → THIẾU (b)', dk(hang_doi=tmpf('h5.md', ''.join(l for l in HD.splitlines(True) if not l.startswith('| T8 |'))))['K-R7']['thieu'], True)
E = copy.deepcopy(D0); E.pop('thu_tu')
case('K-R7', 'không khai thu_tu → tìm id k2c-t7-dok trong cột Tập → T7, ĐẠT', bad(dk(E)['K-R7']), False)
# K-R8
CM = json.load(open(os.path.join(DK, 'cham-mu-nhay-cam.json')))
c1 = copy.deepcopy(CM); c1['vai'][1]['diem'] = 3.5
case('K-R8', 'vai G2 điểm 3,5 < 4 → TRƯỢT', dk(cham_mu=c1)['K-R8']['loi'], True)
c2 = copy.deepcopy(CM); c2['vai'][2]['co'] = ['khung 3:12 có thể bị cắt làm tuyên truyền']
case('K-R8', 'vai G3 có 1 cờ → TRƯỢT', dk(cham_mu=c2)['K-R8']['loi'], True)
c3 = copy.deepcopy(CM); c3['vai'] = c3['vai'][:2]
case('K-R8', 'chỉ 2 vai → TRƯỢT', dk(cham_mu=c3)['K-R8']['loi'], True)
case('K-R8', 'vai G2 điểm đúng 4,0 → ĐẠT, nêu tên sát ngưỡng', [] if dk()['K-R8']['sat_nguong'] and not dk()['K-R8']['loi'] else ['không nêu'], False)
# K-R9
case('K-R9', 'mô tả không có "as of" → (a)', bad(dk(mo_ta=tmpf('m2.txt', 'Sources: Müller 2010; Frederick Taylor 2004.'))['K-R9'], 'a'), True)
case('K-R9', 'mô tả chỉ có nguồn Đức → (b)', bad(dk(mo_ta=tmpf('m3.txt', 'Facts as of 2026. Sources: Müller 2010; Bergander 1977.'))['K-R9'], 'b'), True)
case('K-R9', 'không có bình luận ghim → (c)', bad(dk(binh_luan_ghim='khong-co.txt')['K-R9'], 'c'), True)
case('K-R9', 'thiếu khai K-R9.tu_chan → THIẾU', [x for x in dk(khai=[k for k in KH if k['ma'] != 'K-R9.tu_chan'])['K-R9']['thieu'] if 'K-R9.tu_chan' in x], True)
# khai G1-R
case('KHAI', 'người ký ghi email → lỗi (che email)', dk(khai=[dict(k, nguoi_ky='ai@example.com') if k['ma'] == 'K-R6.the' else k for k in KH])['K-R6']['loi'], True)
case('KHAI', 'vai ≠ chu_du_an → lỗi', dk(khai=[dict(k, vai='phien_p') if k['ma'] == 'K-R5.the' else k for k in KH])['K-R5']['loi'], True)
case('KHAI', 'cấp K-R: THIẾU mục khai tính Chặn', cap112.cap('K-R9', dk(khai=[])['K-R9'])[1], True)

# =============================================================== in
shutil.rmtree(TMP, ignore_errors=True)
ok = sum(1 for x in R if x[3])
for rule, name, exp, good, got in R:
    print(f"{'OK ' if good else 'SAI'} [{rule}] {name} — kỳ vọng {exp}" + ('' if good else f' — nhận: {got}'))
by = {}
for x in R: by.setdefault(x[0], [0, 0]); by[x[0]][0] += x[3]; by[x[0]][1] += 1
print('\n' + ' · '.join(f'{k} {a}/{b}' for k, (a, b) in by.items()))
print(f'\nselftest 1.14: {ok}/{len(R)} đúng kỳ vọng')
sys.exit(0 if ok == len(R) else 1)
