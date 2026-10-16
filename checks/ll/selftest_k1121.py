#!/opt/cine/bin/python
"""Tự kiểm luật kênh 2 bản 1.12.1 (phiên K, 17/10/2026; chủ dự án duyệt 16–17/10: HH2, HH3, MM1–MM4, JJ1–JJ2, KK1, Q34 timelapse).
Mỗi luật mới/sửa ≥ 1 ca ĐẠT + ≥ 1 ca TRƯỢT. Dữ liệu thật:
  fixtures/k1121/tl-gib20-v5b2a/  bộ timelapse V5b-2a (origin/v5b2a b35995e): campath = grammarLog, ngân sách chữ, log chữ, mặt nạ MỌI khung, cuộn 6 preset;
                                  K thêm lưới địa hình (DEM Copernicus 20 m cắt từ gói cảnh K dựng lại) và 14 khung không chữ + mặt nạ hero K dựng lại
                                  trên llvmpipe (khung 320 trùng byte khung vàng của V)
  fixtures/k1121/khop1/           khung vàng llvmpipe của V5b-2a (cắt 480×270 giữa khung 320, 214) ↔ khung K dựng lại llvmpipe / SwiftShader
  fixtures/k112/tl-gib20/         bộ V5b-1b (trước khi có dòng phương pháp "≈ = …", bay 273–308 m)
KHÔNG gọi mạng, KHÔNG gọi API.

  /opt/cine/bin/python checks/ll/selftest_k1121.py        mã thoát 0 = mọi ca đúng kỳ vọng
"""
import copy, gzip, json, os, shutil, sys, tempfile

import cv2
import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, ROOT)
from checks.ll import q_tl as QT, q_hinh as QH, q_chu as QC, q_types as QY, cap112  # noqa: E402

FX = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures')
D2, D1, DK = os.path.join(FX, 'k1121', 'tl-gib20-v5b2a'), os.path.join(FX, 'k112', 'tl-gib20'), os.path.join(FX, 'k1121', 'khop1')
TMP = tempfile.mkdtemp(prefix='k1121-')
R = []


def case(rule, name, got, expect_fail):
    got = list(got) if got else []
    R.append((rule, name, 'bắt lỗi' if expect_fail else 'sạch', bool(got) == expect_fail, got[:2]))


def bad(r): return r['loi'] + r.get('thieu', [])


def bo(d): return json.load(open(os.path.join(d, 'bo-tl.json')))


B2, B1 = bo(D2), bo(D1)
R2, R1 = QT.check(copy.deepcopy(B2), D2), QT.check(copy.deepcopy(B1), D1)
F2 = QT._frames(QT._ld(D2, B2['campath'])); CP2 = QT._ld(D2, B2['campath'])

# =============================================================== HH3 Q35(c) "≈" bộ đếm timelapse (bộ timelapse + đặc tả)
case('Q35-TL', f"gib20 V5b-2a: {R2['Q35-TL']['val']} → ĐẠT", bad(R2['Q35-TL']), False)
case('Q35-TL', f"gib20 V5b-1b: {R1['Q35-TL']['val']} → TRƯỢT (c)", R1['Q35-TL']['loi'], True)
L = QT._ld(D2, B2['log_chu']); L2 = copy.deepcopy(L)
for x in L2['frames']: x['text'] = [t for t in x['text'] if not (t['role'] == 'method' and QT.XAP_XI.search(t['s']) and x['f'] / 24 <= 6.0)]
for x in L2['frames']:
    if x['f'] == 240: x['text'].append(dict(s='≈ = interpolated between counts', role='method', px1080=38, ratio=12.0))
r = QT.check(dict(copy.deepcopy(B2), log_chu=L2), D2)['Q35-TL']
case('Q35-TL', 'gib20 V5b-2a, dòng "≈ = interpolated between counts" dời tới 10 s (ngoài 6 s đầu) → TRƯỢT', r['loi'], True)
L3 = copy.deepcopy(L)
for x in L3['frames']:
    if x['f'] == 120: x['text'].append(dict(s='≈ 3× more ships', role='tag', px1080=40, ratio=9.0))
r = QT.check(dict(copy.deepcopy(B2), log_chu=L3), D2)['Q35-TL']
case('Q35-TL', 'gib20 V5b-2a + nhãn neo "≈ 3× more ships" (vai tag, không phải bộ đếm) không ESTIMATE → TRƯỢT', r['loi'], True)

NUMS = dict(n_pop=dict(v=19047, text='≈ 19,047 residents', kind='estimate', year=1891))
METH = dict(s='≈ = interpolated between counts', at=0.5)


def q35(tl=True, meth=True, s='≈ 19,047 residents', t0=0.0):
    p = dict(tags=[dict(s=s, num='n_pop', at=1.0)], cap=[METH] if meth else [])
    TL = dict(tong_s=t0 + 8.0, segments=[dict(id='00', t0=t0, t1=t0 + 8.0, shots=[dict(tpl='plate', t0=0.0, t1=8.0, p=p, **({'type': 'timelapse'} if tl else {}))])], shorts=[])
    E = dict(id='k2x', numbers=NUMS, segments=[dict(id='00', shots=[dict(tpl='plate', type='timelapse' if tl else 'scene3d', **({'tl': True} if tl else {}))])])
    return QC.q35(E, TL)


r = q35(); case('Q35', f"đặc tả: shot timelapse, bộ đếm \"≈ 19,047 residents\" (estimate) + dòng phương pháp 0:00,5 → ĐẠT ({r['val']})", r['loi'], False)
case('Q35', 'đặc tả: shot timelapse, bộ đếm "≈", KHÔNG có dòng "≈ = interpolated between counts" → (c)', q35(meth=False)['muc']['c'], True)
case('Q35', 'đặc tả: dòng phương pháp ở 10,5 s (ngoài 6 s đầu phim) → (c)', q35(t0=10.0)['muc']['c'], True)
case('Q35', 'đặc tả: shot scene3d (không phải timelapse) có "≈" + dòng phương pháp → (c) như cũ', q35(tl=False)['muc']['c'], True)
case('Q35', 'đặc tả: shot timelapse, số estimate KHÔNG bắt đầu "≈" → (c) như cũ', q35(s='19,047 residents')['muc']['c'], True)

# =============================================================== HH2 TL-Q2 AGL theo loại tuyến
case('TL-Q2', f"gib20 V5b-2a: {R2['TL-Q2']['val']} → ĐẠT", bad(R2['TL-Q2']), False)
case('TL-Q2', f"gib20 V5b-1b (không khai loại → pho ≤ 120 m; không địa hình → độ cao tuyệt đối): {R1['TL-Q2']['loi'][:1]}", R1['TL-Q2']['loi'], True)
BX = copy.deepcopy(B1); BX['tuyen'][0]['loai'] = 'eo_dat'; BX['tuyen'][0]['cao_do_m'] = 3.0
r = QT.check(BX, D1)['TL-Q2']
case('TL-Q2', f"gib20 V5b-1b khai loai eo_dat (≤ 300 m), cao độ tuyến 3 m: AGL 270–305 m — {r['loi'][:1] or r['val'][:80]}", r['loi'], True)
BX = copy.deepcopy(B1); BX['tuyen'][0]['loai'] = 'eo_dat'; BX['tuyen'][0]['cao_do_m'] = 12.0
r = QT.check(BX, D1)['TL-Q2']
case('TL-Q2', f"gib20 V5b-1b khai loai eo_dat, cao độ tuyến 12 m (tổng hợp): {r['val'][:120]}", bad(r), False)
BX = copy.deepcopy(B2); BX['tuyen'][0]['loai'] = 'pho'; FX2 = copy.deepcopy(F2)
for fr in FX2[188:260]: fr['pos'][1] += 30.0
r = QT.check(dict(BX, campath=FX2), D2)['TL-Q2']
case('TL-Q2', 'gib20 V5b-2a khai loai pho, nâng máy +30 m (AGL ≈ 126–134 m > 120) → TRƯỢT', r['loi'], True)
BX = copy.deepcopy(B2); BX['tuyen'][0]['loai'] = 'pho'
case('TL-Q2', 'gib20 V5b-2a khai loai pho (AGL 96–104 m ≤ 120) → ĐẠT', bad(QT.check(BX, D2)['TL-Q2']), False)
BX = copy.deepcopy(B2); BX['tuyen'][0]['loai'] = 'kenh'
r = QT.check(BX, D2)['TL-Q2']; case('TL-Q2', f"loại tuyến lạ 'kenh' → coi pho: {r['tuyen'][0]['loai_nguon']}", [] if r['tuyen'][0]['loai'] == 'pho' else ['không coi pho'], False)

# =============================================================== MM3 TL-Q1(c) tương phản cục bộ hero
r = R2['TL-Q1']
case('TL-Q1c', f"gib20 V5b-2a đường băng 1941: {r['tuong_phan']['val']} → ĐẠT (c)", r['muc']['c'] + [x for x in r['thieu'] if x.startswith('(c)')], False)
HS = os.path.join(TMP, 'hero'); os.makedirs(os.path.join(HS, 'khung')); os.makedirs(os.path.join(HS, 'mat-na'))
for f in (308, 316):
    shutil.copy(os.path.join(D2, 'hero', 'khung', f'{f:05d}.jpg'), os.path.join(HS, 'khung')); shutil.copy(os.path.join(D2, 'hero', 'mat-na', f'{f:05d}.png'), os.path.join(HS, 'mat-na'))
r = QT.check(dict(copy.deepcopy(B2), hero_anh=dict(B2['hero_anh'], khung=os.path.join(HS, 'khung'), mat_na=os.path.join(HS, 'mat-na'))), D2)['TL-Q1']
case('TL-Q1c', f"gib20 V5b-2a chỉ khung mốc 308, 316 (tương phản vành 1,11 / 0,84), không có khung hero ngoài mốc → TRƯỢT: {r['tuong_phan']['val']}", r['muc']['c'], True)
SY = os.path.join(TMP, 'sy'); [os.makedirs(os.path.join(SY, k)) for k in ('khung', 'mat-na')]


def synth(f, l_hero, l_bg):
    """khung tổng hợp 640×360: hero 200×100 giữa khung, độ chói tuyến tính l_hero trên nền l_bg; mặt nạ R 255, G 0, B = 2"""
    enc = lambda l: int(round(255 * (12.92 * l if l <= 0.0031308 else 1.055 * l ** (1 / 2.4) - 0.055)))
    im = np.full((360, 640, 3), enc(l_bg), np.uint8); im[130:230, 220:420] = enc(l_hero); mk = np.zeros((360, 640, 3), np.uint8); mk[130:230, 220:420] = (2, 0, 255)
    cv2.imwrite(os.path.join(SY, 'khung', f'{f:05d}.png'), im); cv2.imwrite(os.path.join(SY, 'mat-na', f'{f:05d}.png'), mk)


for f in (300, 320, 340): synth(f, 0.20, 0.26)
for f in (360, 380): synth(f, 0.19, 0.26)
r = QT.check(dict(copy.deepcopy(B2), hero_anh=dict(khung=os.path.join(SY, 'khung'), mat_na=os.path.join(SY, 'mat-na'), hero_id=2)), D2)['TL-Q1']
case('TL-Q1c', f"tổng hợp: hero 0,20 trên nền 0,26 (tương phản 0,30), ngoài mốc 0,19 (×1,05) → TRƯỢT: {r['tuong_phan']['val']}", r['muc']['c'], True)
for f in (360, 380): synth(f, 0.13, 0.26)
r = QT.check(dict(copy.deepcopy(B2), hero_anh=dict(khung=os.path.join(SY, 'khung'), mat_na=os.path.join(SY, 'mat-na'), hero_id=2)), D2)['TL-Q1']
case('TL-Q1c', f"tổng hợp: cùng mốc, hero ngoài mốc 0,13 → hero mốc / ngoài mốc ×1,54 ≥ 1,3 → ĐẠT (cách ii): {r['tuong_phan']['val']}", r['muc']['c'], False)
for f in (300, 320, 340): synth(f, 0.40, 0.15)
r = QT.check(dict(copy.deepcopy(B2), hero_anh=dict(khung=os.path.join(SY, 'khung'), mat_na=os.path.join(SY, 'mat-na'), hero_id=2)), D2)['TL-Q1']
case('TL-Q1c', f"tổng hợp: hero 0,40 trên nền 0,15 (tương phản 1,67) → ĐẠT (cách i): {r['tuong_phan']['val']}", r['muc']['c'], False)
r = QT.check(dict(copy.deepcopy(B2), hero_anh=None), D2)['TL-Q1']
case('TL-Q1c', 'không khai hero_anh (chỉ có nhan_sang 1.12.0) → THIẾU (c)', [x for x in r['thieu'] if x.startswith('(c)')], True)

# =============================================================== MM2 TL-Q7 năm/s theo pha
case('TL-Q7', f"gib20 V5b-2a: {R2['TL-Q7']['val']} — bay xuống ngoài cú (6,0–8,3 s, AGL 78–148 m) 40 năm/s → TRƯỢT", R2['TL-Q7']['loi'], True)
CU = copy.deepcopy(CP2); CU['frames'] = [dict(fr, f=i) for i, fr in enumerate(CP2['frames'][188:548])]
r = QT.tlq7(dict(copy.deepcopy(B2), _base=D2, _cp=CU), CU['frames'], 24, D2)
case('TL-Q7', f"gib20 V5b-2a chỉ cú liên hoàn 7,8–22,8 s: {r['val'][:90]} → ĐẠT", bad(r), False)
CV = copy.deepcopy(CU)
for i, fr in enumerate(CV['frames']):
    if fr['phase'] == 'reveal': fr['year'] = CV['frames'][i - 1]['year'] + 18.0 / 24 if CV['frames'][i - 1]['phase'] == 'reveal' else fr['year']
r = QT.tlq7(dict(copy.deepcopy(B2), _base=D2, _cp=CV), CV['frames'], 24, D2)
case('TL-Q7', f"cú liên hoàn, reveal (AGL > 247 m) chạy 18 năm/s → ĐẠT (trần 20): {r['val'][:90]}", bad(r), False)
for i, fr in enumerate(CV['frames']):
    if fr['phase'] == 'reveal' and CV['frames'][i - 1]['phase'] == 'reveal': fr['year'] = CV['frames'][i - 1]['year'] + 24.0 / 24
r = QT.tlq7(dict(copy.deepcopy(B2), _base=D2, _cp=CV), CV['frames'], 24, D2)
case('TL-Q7', 'cú liên hoàn, reveal chạy 24 năm/s > 20 → TRƯỢT', r['loi'], True)
CW = copy.deepcopy(CU)
for i, fr in enumerate(CW['frames']):
    if fr['phase'] == 'fly' and i: fr['year'] = CW['frames'][i - 1]['year'] + 12.0 / 24
r = QT.tlq7(dict(copy.deepcopy(B2), _base=D2, _cp=CW), CW['frames'], 24, D2)
case('TL-Q7', 'cú liên hoàn, bay WCA (AGL ≈ 100 m) chạy 12 năm/s > 10 → TRƯỢT', r['loi'], True)
r = QT.tlq7(dict(copy.deepcopy(B1), _base=D1, _cp=None), QT._frames(QT._ld(D1, B1['campath'])), 24, D1)
case('TL-Q7', 'gib20 V5b-1b: campath không có pha/AGL → THIẾU', r['thieu'], True)

# =============================================================== MM1 TL-Q8 nội dung pha bay thấp của cú liên hoàn
case('TL-Q8', f"gib20 V5b-2a eo đất 1896–1941: {R2['TL-Q8']['loi'][:1]} → báo", R2['TL-Q8']['loi'], True)
M2 = [dict(m, content_pct=max(m['content_pct'], 35.0)) for m in QT._ld(D2, B2['mat_na'])]
r = QT.check(dict(copy.deepcopy(B2), mat_na=M2), D2)['TL-Q8']
case('TL-Q8', f"gib20 V5b-2a, mặt nạ nâng content ≥ 35 % (tổng hợp): {r['val'][:80]} → ĐẠT", bad(r), False)
case('TL-Q8', 'bộ không có mặt nạ mỗi khung → THIẾU', QT.check(dict(copy.deepcopy(B2), mat_na=None), D2)['TL-Q8']['thieu'], True)

# =============================================================== JJ1/KK1 TL-Q9 tiết chế máy (cả tập)
PR = QT._ld(D2, 'presets-campath.json.gz'); FP = PR['frames']
T2 = ('gib20', dict(B2, _cp=CP2), F2, 24); TP = ('presets', dict(_cp=PR), FP, 24)
r = QT.tlq9([T2, TP]); case('TL-Q9', f"tập = gib20 V5b-2a + cuộn 6 preset: {r['val'][:110]} → ĐẠT", bad(r), False)
r = QT.tlq9([T2, T2, ('gib20c', dict(B2, _cp=CP2), F2, 24)]); case('TL-Q9', 'tập có 3 cú liên hoàn > 2 → (a)', r['muc']['a'], True)
r = QT.tlq9([TP, ('presets2', dict(_cp=PR), FP, 24)]); case('TL-Q9', 'tập có 2 vertigo > 1 → (b)', r['muc']['b'], True)
FV = copy.deepcopy(F2)
for fr in FV:
    if fr.get('phase') == 'crane': fr['vai'] = None
case('TL-Q9', 'cú liên hoàn bỏ vai ở pha crane → (c)', QT.tlq9([('gib20', dict(B2, _cp=CP2), FV, 24)])['muc']['c'], True)
FO = copy.deepcopy(F2)
for fr in FO:
    if fr.get('phase') == 'orbit' and fr['f'] >= 370: fr['phase'] = 'crane'
case('TL-Q9', 'orbit cắt còn 3,8 s (< 4 s) → (d)', QT.tlq9([('gib20', dict(B2, _cp=CP2), FO, 24)])['muc']['d'], True)
FW = copy.deepcopy(F2)
for k, fr in enumerate(FW[420:426]):
    fr['look'] = [fr['pos'][0] + (60 if k % 2 else -60), fr['pos'][1] - 50, fr['pos'][2] + 200]
r = QT.tlq9([('gib20', dict(B2, _cp=CP2), FW, 24)])
case('TL-Q9', f"hướng nhìn lắc 6 khung (≈ 800 °/s) → (e) Chặn: {r['muc']['e'][:1]}", r['muc']['e'], True)
mo, ch, cb = cap112.cap('TL-Q9', r)
case('TL-Q9', f"cấp: (e) vào phần Chặn ({mo})", [] if ch and all(x.startswith('(e)') for x in ch) else ['(e) không vào Chặn'], False)

# =============================================================== MM4 KHOP1 khung vàng llvmpipe (khai renderer + so cấu trúc)
r = QH.khop1(os.path.join(DK, 'vang'), os.path.join(DK, 'moi-llvmpipe'))
case('KHOP1', f"khung vàng llvmpipe V5b-2a ↔ K dựng lại llvmpipe (máy khác): {r['val']}", bad(r), False)
r = QH.khop1(os.path.join(DK, 'vang'), os.path.join(DK, 'moi-swiftshader'))
mo, ch, cb = cap112.cap('KHOP1', r)
case('KHOP1', f"khung vàng llvmpipe ↔ K dựng SwiftShader (đổi trình dựng): {r['val']} → (c) TRƯỢT, vào phần Chặn", ch if r['doi_trinh_dung'] else [], True)
KV = os.path.join(TMP, 'kv'); shutil.copytree(os.path.join(DK, 'vang'), KV); KM = os.path.join(DK, 'moi-llvmpipe')


def kv(**kw):
    J = json.load(open(os.path.join(DK, 'vang', 'khung-vang.json'))); J.update(kw); J = {k: v for k, v in J.items() if v is not None}
    json.dump(J, open(os.path.join(KV, 'khung-vang.json'), 'w'), ensure_ascii=False); return QH.khop1(KV, KM)


case('KHOP1', 'khung vàng khai gl "swiftshader" mà renderer là llvmpipe → (a)', kv(gl='swiftshader')['loi'], True)
case('KHOP1', 'khung vàng không khai gl (mẫu 1.12.0 chỉ có renderer) → (a)', kv(gl=None)['loi'], True)
case('KHOP1', 'khung vàng không khai goi_canh.sha256 → (a)', kv(goi_canh=None)['loi'], True)
J0 = json.load(open(os.path.join(DK, 'vang', 'khung-vang.json')))
case('KHOP1', 'khung vàng SHA lệch tệp (khung 00214.png bị thay) → (a)', kv(khung=dict(J0['khung'], **{'00214.png': '0' * 64}))['loi'], True)
case('KHOP1', 'khai lại đúng → ĐẠT', bad(kv()), False)
KN = os.path.join(TMP, 'kn'); shutil.copytree(KM, KN); JN = json.load(open(os.path.join(KN, 'khung-moi.json'))); JN['goi_canh'] = dict(JN['goi_canh'], sha256='1' * 64)
json.dump(JN, open(os.path.join(KN, 'khung-moi.json'), 'w'))
case('KHOP1', 'khung mới dựng từ gói cảnh khác (goi_canh.sha256 khác) → (d)', QH.khop1(os.path.join(DK, 'vang'), KN)['loi'], True)

# =============================================================== Q34 TYPES timelapse
def q34(ty):
    E = dict(id='k2x', segments=[dict(id='00', shots=[dict(tpl='plate', type=ty)])])
    return QY.q34(E, dict(tong_s=5.0, heroes={}, segments=[dict(id='00', t0=0, t1=5.0, shots=[dict(tpl='plate', t0=0, t1=5.0, p={})])], shorts=[]))['muc']['0']


case('Q34', 'type timelapse nằm trong TYPES (không lỗi (0))', q34('timelapse'), False)
case('Q34', 'type "time-lapse" (ngoài TYPES) → (0)', q34('time-lapse'), True)

for rule, name, kind_, ok, got in R: print(f"{'ĐÚNG' if ok else 'SAI '}  {rule:<7} {kind_:<8} {name}" + ('' if ok else f'   → {got}'))
by = {}
for rule, _, k, ok, _ in R: by.setdefault(rule, set()).add(k)
miss = [k for k, v in by.items() if v != {'sạch', 'bắt lỗi'}]
n_ok = sum(r[3] for r in R); print(f'\nselftest 1.12.1: {n_ok}/{len(R)} ca đúng kỳ vọng · {len(by)} luật, luật thiếu ca đạt hoặc trượt: {miss or "không"}')
shutil.rmtree(TMP, ignore_errors=True)
sys.exit(0 if n_ok == len(R) and not miss else 1)
