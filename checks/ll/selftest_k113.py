#!/opt/cine/bin/python
"""Tự kiểm luật 1.13 (phiên K, 17/10/2026): NC-H1…NC-H5 (NC-LS §6, đánh giá T2 của chủ dự án) + hàng đợi khiếu nại T2 G2 §13–§14
(Q7/Q8-K2, Q36 (1.13), Q33 (1.13), Q37 (1.13)). Mỗi luật ≥ 1 ca ĐẠT + ≥ 1 ca TRƯỢT. Dữ liệu thật:
  fixtures/k113/             T2 L5 (origin/k2c-t2 @86731f50): đặc tả + timeline dựng lại ngoại tuyến (prep.py, ElevenLabs chặn, 618,9167 s = master)
                             + băm pHash của 42 lần xuất hiện trên master L5 f63b0b4b… (xám toàn khung và L vùng nội dung)
  fixtures/k1121/tl-gib20-v5b2a/   bộ timelapse gib20 V5b-2a (campath agl, mặt nạ mọi khung fabric_pct, log chữ)
  fixtures/k2v4-mau/         cuộn K2V4 (đặc tả có beats) cho Q37
Không gọi mạng, không gọi API, không cần master (băm/khung tổng hợp đã lưu hoặc sinh trong bộ nhớ).

  /opt/cine/bin/python checks/ll/selftest_k113.py        mã thoát 0 = mọi ca đúng kỳ vọng
"""
import copy, gzip, json, math, os, sys

import numpy as np
import yaml

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, ROOT)
from checks.ll import base, q_noi as N, q_chu as QC, q_scene as QS, q_nhip as QN, q_k2var as K, llcheck as LC, cap112  # noqa: E402

FX = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures')
R = []


def case(rule, name, got, expect_fail):
    got = list(got) if got else []
    R.append((rule, name, 'bắt lỗi' if expect_fail else 'sạch', bool(got) == expect_fail, got[:2]))


E2 = yaml.safe_load(gzip.open(os.path.join(FX, 'k113', 't2l5-episode.yaml.gz'))); E2['_path'] = '/x/channel-k2/k2c-t2-01/episode.yaml'
TL2 = json.load(gzip.open(os.path.join(FX, 'k113', 't2l5-timeline.json.gz')))
GD = os.path.join(FX, 'k1121', 'tl-gib20-v5b2a'); GB = json.load(open(os.path.join(GD, 'bo-tl.json')))
APS = json.load(gzip.open(os.path.join(FX, 'k113', 't2l5-aps.json.gz')))['aps']
RT = N.nc_tap(E2, TL2); RG = N.nc_bo(copy.deepcopy(GB), GD)


def bo(**kw):
    """bộ timelapse tổng hợp 24 khung/s: kw → campath/mặt nạ/log trong bộ nhớ"""
    n = kw.pop('n', 240)
    F = [dict(f=i, year=kw.get('year', lambda i: 1900 + i // 24)(i), agl=kw.get('agl', lambda i: 500.0)(i), phase='free') for i in range(n)]
    M = [dict(f=i, fabric_pct=kw.get('fab', lambda i: 40.0)(i), **({'ghost_pct': kw['ghost'](i)} if 'ghost' in kw else {})) for i in range(n)]
    B = dict(campath=F, mat_na=M, fps=24, log_chu=kw.get('log', [dict(f=0, text=[dict(s='Amsterdam', role='where', px1080=40)])]))
    for k in ('noi', 'reveal', 'nam_khung', 'dia_danh'):
        if k in kw: B[k] = kw[k]
    return N.nc_bo(B, '.')


# =============================================================== máy quay → AGL (bản sao độc lập relief.js / map.js)
d, tl = N.relief_at([dict(t=0, dist=22, tilt=62), dict(t=9, dist=18, tilt=64)], 7.7, 9.0)
case('AGL', f'relief mốc cuối dist 18 km, tilt 64° → (dist, tilt) = ({d:.2f}, {tl:.2f}); AGL {d * math.cos(math.radians(tl)):.2f} km', [] if abs(d - 18) < 1e-6 and abs(tl - 64) < 1e-6 else ['sai mốc'], False)
k = N.globe_at([dict(u=0, alt=30), dict(u=0.5, alt=18), dict(u=1, alt=22)], 19.5, 9.75)
case('AGL', f'địa cầu g05_china alt 18 (đơn vị R/10), tilt 0 → AGL {k:,.0f} km = 18 × 637,1', [] if abs(k - 18 * 637.1) < 1 else ['sai'], False)
case('AGL', 'preset pair (thấp nhất alt 2,5) luôn > 50 km', [] if min(N.globe_at(N.globe_keys(dict(preset='pair'))[0], 10, t) for t in np.linspace(0, 10, 41)) > 50 else ['≤ 50 km'], False)
case('AGL', 'relief khai sai (mốc rỗng) không làm sập luật', [] if N.relief_at([], 5, 1) is None else ['không None'], False)

# =============================================================== NC-H1 thành phố có nhà
case('NC-H1', f"gib20 V5b-2a (không khai noi → suy AGL ≤ 3 km): {RG['NC-H1']['val']} → (b) eo đất 1896–1941", [x for x in RG['NC-H1']['loi'] if x.startswith('(b)')], True)
B = copy.deepcopy(GB); B['noi'] = [dict(t=[0, 7.5], noi='thanh_pho'), dict(t=[7.5, 12.4], noi='eo_dat'), dict(t=[12.4, 24.5], noi='thanh_pho')]
r = N.nc_bo(B, GD)['NC-H1']; case('NC-H1', f"gib20 + khai eo đất 7,5–12,4 s là eo_dat (không thành phố): {r['val']} → ĐẠT", r['loi'], False)
case('NC-H1', 'mặt nạ fabric trung vị 20 % → (a)', [x for x in bo(fab=lambda i: 20.0)['NC-H1']['loi'] if x.startswith('(a)')], True)
rv = dict(reveal=[dict(t=[5.0, 10.0], kieu='keo_lui')])
case('NC-H1', 'fabric 10 % trong 2 s cuối cú reveal kéo lùi → miễn, ĐẠT', bo(fab=lambda i: 10.0 if i >= 192 else 40.0, **rv)['NC-H1']['loi'], False)
case('NC-H1', 'fabric 10 % bắt đầu 4 s trước hết reveal (ngoài 3 s miễn) → (b)', bo(fab=lambda i: 10.0 if i >= 144 else 40.0, **rv)['NC-H1']['loi'], True)
case('NC-H1', 'bộ không có mặt nạ → THIẾU (không ĐẠT)', N.nc_bo(dict(campath=[dict(f=i, agl=100) for i in range(48)], fps=24), '.')['NC-H1']['thieu'], True)
case('NC-H1', f"T2 L5: {RT['NC-H1']['val']} → shot relief khai/suy thành phố mà không có lớp nhà = TRƯỢT theo đặc tả",
     [x for x in RT['NC-H1']['loi'] if 'r00_launch' in x and 'không có lớp nhà' in x], True)
case('NC-H1', 'T2 L5 r05_philly/r06_home (ảnh hàng không opt.aerial) → lớp nhà khai, không TRƯỢT', [x for x in RT['NC-H1']['loi'] if 'r05_philly' in x or 'r06_home' in x], False)
E3, T3 = copy.deepcopy(E2), copy.deepcopy(TL2)
for s in T3['segments']:
    for sh in s['shots']:
        if (sh.get('p') or {}).get('hero') in ('r00_launch', 'r01_yards', 'r01_dive', 'r02_cut', 'r03_myth', 'r03_scale'): sh['p']['fabric_pct'] = [30.0, 28.0, 33.0]
case('NC-H1', 'T2 L5 + mặt nạ fabric (tổng hợp) trung vị ≥ 25 %, min ≥ 15 % ở 6 shot thành phố → ĐẠT', N.nc_tap(E3, T3)['NC-H1']['loi'], False)
case('NC-H1', 'chip "San Francisco Bay, Calif." / "Delaware River valley" không suy thành phố; "Richmond, Calif.", "Philadelphia area" có',
     [] if not N.city_chip('San Francisco Bay, Calif.') and not N.city_chip('Delaware River valley') and N.city_chip('Richmond, Calif.') and N.city_chip('Philadelphia area') else ['suy sai'], False)

# =============================================================== NC-H2 địa cầu
case('NC-H2', f"T2 L5: {RT['NC-H2']['val']} → TRƯỢT, có g05_china (18–30 bán kính… đơn vị R/10)", [x for x in RT['NC-H2']['loi'] if 'g05_china' in x], True)
case('NC-H2', f"gib20 V5b-2a: {RG['NC-H2']['val']} → ĐẠT", RG['NC-H2']['loi'] + RG['NC-H2']['thieu'], False)
case('NC-H2', 'một lần AGL 80 km dài 2,5 s → ĐẠT', bo(agl=lambda i: 80000.0 if 24 <= i < 84 else 500.0)['NC-H2']['loi'], False)
case('NC-H2', 'hai lần địa cầu (mỗi lần 1 s) → (a)', [x for x in bo(agl=lambda i: 80000.0 if (24 <= i < 48 or 120 <= i < 144) else 500.0)['NC-H2']['loi'] if x.startswith('(a)')], True)
case('NC-H2', 'một lần 4 s → (b)', [x for x in bo(agl=lambda i: 80000.0 if 24 <= i < 120 else 500.0)['NC-H2']['loi'] if x.startswith('(b)')], True)

# =============================================================== NC-H3 tầm mặc định
case('NC-H3', f"gib20 V5b-2a: {RG['NC-H3']['val']} → ĐẠT", RG['NC-H3']['loi'], False)
case('NC-H3', f"T2 L5: {RT['NC-H3']['val']} → (b) tập có thành phố mà AGL ≤ 3 km 1 %", [x for x in RT['NC-H3']['loi'] if x.startswith('(b)')], True)
case('NC-H3', 'bộ ở AGL 100 km 60 % thời lượng → (a)', [x for x in bo(agl=lambda i: 100000.0 if i < 144 else 2000.0)['NC-H3']['loi'] if x.startswith('(a)')], True)

# =============================================================== NC-H4 nơi có tên
case('NC-H4', f"T2 L5 (sau SS1/TT): {RT['NC-H4']['val']} → ĐẠT", RT['NC-H4']['loi'], False)
E4, T4 = copy.deepcopy(E2), copy.deepcopy(TL2)
for s in T4['segments']:
    for sh in s['shots']:
        if (sh.get('p') or {}).get('hero') == 'r03_ladder': sh['p'].pop('where', None); sh['p'].pop('tags', None); sh['p'].pop('places', None)
for k_ in ('r03_ladder',):
    for H in (E4.get('heroes') or {}, T4.get('heroes') or {}):
        if k_ in H: (H[k_].get('opt') or {}).pop('places', None); (H[k_].get('opt') or {}).pop('pins', None)
case('NC-H4', 'T2 L5 bỏ chip "Delaware Bay" của r03_ladder (không nhãn địa danh khác) → TRƯỢT nêu tên shot', [x for x in N.nc_tap(E4, T4)['NC-H4']['loi'] if 'r03_ladder' in x], True)
case('NC-H4', f"gib20 V5b-2a: log chữ không có chip nơi/địa danh → TRƯỢT ({RG['NC-H4']['val'][:60]})", RG['NC-H4']['loi'], True)
case('NC-H4', 'bộ có log chữ role where "Amsterdam" → ĐẠT', bo()['NC-H4']['loi'], False)

# =============================================================== NC-H5 đúng thời kỳ
case('NC-H5', f"gib20 V5b-2a: nhãn ghost dài nhất 2,75 s < 3 s → (b); (a) THIẾU nam_khung · {RG['NC-H5']['val'][:90]}", [x for x in RG['NC-H5']['loi'] if x.startswith('(b)')], True)
case('NC-H5', 'tập kênh 2 không timelapse → KHÔNG ÁP', [] if RT['NC-H5'].get('ket_qua') == 'KHÔNG ÁP' else ['áp nhầm'], False)
lg = [dict(f=i, text=[dict(s='muted houses: reconstructed from 1913 plan', role='ghost_src', px1080=38)]) for i in range(48, 48 + 84)] + [dict(f=0, text=[dict(s='Gibraltar', role='where', px1080=40)])]
NK = [dict(f=i, nam_max={'toa': 1900 + i // 24}) for i in range(0, 240, 6)]
case('NC-H5', 'năm xây ≤ bộ đếm + ghost hiện 2,0 s, nhãn ghost 38 px 2,0–5,5 s → ĐẠT', bo(nam_khung=NK, ghost=lambda i: 3.0 if i >= 48 else 0.0, log=lg)['NC-H5']['loi'], False)
NK2 = [dict(f=i, nam_max={'toa': 1900 + i // 24 + (5 if 96 <= i < 120 else 0)}) for i in range(0, 240, 6)]
case('NC-H5', 'toà năm xây 5 năm sau bộ đếm (khung 96–119) → (a)', [x for x in bo(nam_khung=NK2, ghost=lambda i: 3.0 if i >= 48 else 0.0, log=lg)['NC-H5']['loi'] if x.startswith('(a)')], True)
lg2 = [dict(f=i, text=[dict(s='reconstructed', role='ghost_src', px1080=38)]) for i in range(48, 96)]
case('NC-H5', 'nhãn ghost chỉ 2 s → (b)', [x for x in bo(nam_khung=NK, ghost=lambda i: 3.0 if i >= 48 else 0.0, log=lg2)['NC-H5']['loi'] if x.startswith('(b)')], True)
lg3 = [dict(f=i, text=[dict(s='reconstructed', role='ghost_src', px1080=30)]) for i in range(48, 132)]
case('NC-H5', 'nhãn ghost 3,5 s nhưng 30 px < 38 → (b)', [x for x in bo(nam_khung=NK, ghost=lambda i: 3.0 if i >= 48 else 0.0, log=lg3)['NC-H5']['loi'] if x.startswith('(b)')], True)

# =============================================================== Q7/Q8-K2 (khiếu nại TT5 i)
L = {}
for sid, i, t, S, Nn, Lb in QC.model_frames(E2, TL2): L.setdefault(sid, {'text': []})['text'].append({'f': int(round(t * 24)), 'items': [{'s': x} for x in S]})
a0, a1 = LC.q7(E2, TL2, L), LC.q7(E2, TL2, L, est=True)
case('Q7/Q8-K2', 'T2 L5 (log mô hình đặc tả): luật v2 báo "thiếu nhãn ESTIMATE" ở r03_tanker (estimate kênh 2 hợp lệ)', [x for x in a0 if 'ESTIMATE' in x], True)
case('Q7/Q8-K2', 'T2 L5, est=True (1.13): nhãn ESTIMATE được nhận → hết lỗi ESTIMATE', [x for x in a1 if 'ESTIMATE' in x], False)
L2 = copy.deepcopy(L)
for e in L2.get('03', {}).get('text', []):
    for it in e['items']:
        it['s'] = it['s'].replace('ESTIMATE', '')
case('Q7/Q8-K2', 'est=True: số estimate hiện mà bỏ nhãn ESTIMATE → vẫn TRƯỢT', [x for x in LC.q7(E2, TL2, L2, est=True) if 'thiếu nhãn ESTIMATE' in x], True)
case('Q7/Q8-K2', 'Q8 loại số: T2 L5 (kênh 2, có n_tanker4 estimate) → ĐẠT', LC.q8k(E2), False)
case('Q7/Q8-K2', 'Q8 loại số: tập LL (không kênh 2) khai estimate → TRƯỢT (LL giữ actual/projection)', LC.q8k(dict(id='ll-ep09', numbers={'n1': dict(kind='estimate')})), True)
case('Q7/Q8-K2', 'Q8 loại số: kênh 2 khai kind "guess" → TRƯỢT', LC.q8k(dict(id='k2x', kenh=2, numbers={'n1': dict(kind='guess')})), True)

# =============================================================== Q36 (1.13) câu miễn trừ (khiếu nại TT5 ii)
case('Q36 (1.13)', 'T2 L5, luật 1.11.1: câu "This video explains… Facts as of" 0:05.6 không khai mien_tru → (b) 1', QC.q36(E2, TL2)['muc']['b'], True)
case('Q36 (1.13)', 'T2 L5, 1.13: câu miễn trừ nhận theo chữ, 1 lần trong 0:00–0:15 → (b) 0', QC.q36(E2, TL2, v113=True)['muc']['b'], False)
T5 = copy.deepcopy(TL2); cp = T5['segments'][0]['shots'][1]['p']['cap']; cp[0]['at'] = 13.0; cp[1]['at'] = 16.6
case('Q36 (1.13)', 'câu miễn trừ kéo tới 0:16.6 (ngoài 0:00–0:15) → (b)', QC.q36(E2, T5, v113=True)['muc']['b'], True)
T6 = copy.deepcopy(TL2); sh2 = T6['segments'][0]['shots'][2]['p']; sh2.setdefault('cap', []).insert(0, dict(s="This video explains how the system works. Facts as of 15 Oct 2026.", at=17.0))
case('Q36 (1.13)', 'câu miễn trừ lặp lần 2 (0:17) → (b)', QC.q36(E2, T6, v113=True)['muc']['b'], True)

# =============================================================== Q33 (1.13) pHash bỏ lớp chữ cố định (khiếu nại T2 G2 §14.5)
def aps(kind): return [dict(a, ph=a[kind]) for a in copy.deepcopy(APS)]
r0 = QS.q33(E2, TL2, aps=aps('ph_xam')); r1 = QS.q33(E2, TL2, aps=aps('ph_L'), k2=True)
case('Q33 (1.13)', f"T2 L5 luật 1.10.1 (xám toàn khung θ 14, có chip nơi + tấm chữ): {r0['val'][-60:]} → 9 góc > 2", r0['loi'] if len(r0['loi']) == 9 else [], True)
case('Q33 (1.13)', f"T2 L5 1.13 (L vùng nội dung θ 16): {len(r1['loi'])} góc > 2 — r01_dive cùng góc Richmond sepia 0:00/0:33/1:31 (K xem khung: lặp thật)",
     [x for x in r1['loi'] if 't2-01-dive' in x], True)
A7 = [a for a in aps('ph_L') if not (a['cam'] == 't2-01-dive' and a['t0'] > 60)]
case('Q33 (1.13)', 'T2 L5 bỏ lần dùng lại r01_dive 1:31 → ĐẠT', QS.q33(E2, TL2, aps=A7, k2=True)['loi'], False)
import cv2  # noqa: E402
rng = np.random.default_rng(7); base_img = cv2.GaussianBlur(rng.integers(0, 255, (180, 320, 3)).astype(np.uint8), (0, 0), 6)
other = cv2.GaussianBlur(rng.integers(0, 255, (180, 320, 3)).astype(np.uint8), (0, 0), 6)


def chip(img, txt, y=12):
    im = img.copy(); cv2.rectangle(im, (190, y), (316, y + 16), (20, 20, 20), -1); cv2.putText(im, txt, (194, y + 12), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255, 255, 255), 1)
    cv2.rectangle(im, (0, 140), (320, 180), (15, 15, 15), -1); cv2.putText(im, 'Source: ' + txt, (8, 172), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (230, 230, 230), 1); return im


h1, h2, h3 = (K.phash_img(chip(base_img, 'Richmond, Calif.'))[0], K.phash_img(chip(base_img, 'Delaware Bay'))[0], K.phash_img(chip(other, 'Richmond, Calif.'))[0])
case('Q33 (1.13)', f'cùng nội dung, khác chip nơi + dòng nguồn → pHash L vùng nội dung lệch {K.ham(h1, h2)} bit (≤ θ)', [] if K.ham(h1, h2) <= K.THETA_L else ['chip làm lệch'], False)
case('Q33 (1.13)', f'khác nội dung, CÙNG chip + dòng nguồn → lệch {K.ham(h1, h3)} bit > θ (không gộp nhầm)', [] if K.ham(h1, h3) > K.THETA_L else ['gộp nhầm'], False)
case('Q33 (1.13)', 'mặc định (k2=False) vẫn luật 1.10.1: θ 14, xám toàn khung', [] if QS.q33(E2, TL2, aps=aps('ph_xam'))['val'].find('xám toàn khung θ=14') > 0 else ['đổi mặc định'], False)

# =============================================================== Q37 (1.13) khung tĩnh theo khung neo (khiếu nại T2 G2 §14.5)
EV4 = base.load(os.path.join(FX, 'k2v4-mau', 'K2V4-reel.yaml'))
tex = cv2.GaussianBlur(rng.normal(128, 45, (90, 400)).astype(np.float32), (0, 0), 2.0)
n = int(24 * 30); M_ = np.float32([[1, 0, 0], [0, 1, 0]])


def film(xpos):
    out = []
    for x in xpos:
        M_[0, 2] = -x; out.append(cv2.warpAffine(tex, M_, (160, 90), flags=cv2.INTER_LINEAR))
    return np.stack(out).astype(np.float32)


Fd = film([0.02 * i for i in range(n)])                                       # trôi 0,48 px/s ở 160 px (0,3 %/s): mắt thấy chuyển động
Ff = film([0.0] * (24 * 7) + [0.4 * i for i in range(n - 24 * 7)])           # 7 s đứng hẳn rồi lia (9,6 px/s, trong bề rộng vân)
Ff = Ff + rng.normal(0, 0.3, Ff.shape).astype(np.float32)                     # nhiễu mã hoá ±0,3
case('Q37 (1.13)', f'máy trôi chậm 30 s: thước 1.11.0 coi là tĩnh ({QN.static_run(None, Fd)[0]} s) → (d) cũ', [x for x in QN.q37(EV4, F=Fd)['loi'] if x.startswith('(d)')], True)
r = QN.q37(EV4, F=Fd, v113=True)
case('Q37 (1.13)', f"cùng phim, 1.13 (neo): khung tĩnh dài nhất {r['khung_tinh'][0]} s, trôi chậm {len(r['troi_cham'])} quãng báo kèm → (d) ĐẠT", [x for x in r['loi'] if x.startswith('(d)')], False)
r = QN.q37(EV4, F=Ff, v113=True)
case('Q37 (1.13)', f"khung đứng hẳn 7 s + nhiễu ±0,3 → (d) 1.13 bắt ({r['khung_tinh'][0]} s)", [x for x in r['loi'] if x.startswith('(d)')], True)
Fm = np.concatenate([Ff[:24 * 7], Ff[24 * 7:24 * 10], Ff[:24 * 7] + 0.0, Ff[24 * 7:24 * 9]])
r = QN.q37(EV4, F=Fm, v113=True)
case('Q37 (1.13)', f"hai quãng tĩnh 7 s cách nhau 3 s chuyển động → liệt kê cả hai (thước cũ chỉ báo quãng dài nhất): {len([x for x in r['loi'] if x.startswith('(d)')])} lỗi (d)",
     [] if len([x for x in r['loi'] if x.startswith('(d)')]) == 2 else ['không đủ 2'], False)

# =============================================================== cấp đề xuất
for q in ('NC-H1', 'NC-H2', 'NC-H3', 'NC-H4', 'NC-H5', 'Q7/Q8-K2', 'Q33 (1.13)', 'Q36 (1.13)', 'Q37 (1.13)'):
    case('cấp', f'{q}: có cấp đề xuất trong cap112 ({cap112.CAP[q][0]})', [] if q in cap112.CAP else ['thiếu'], False)
case('cấp', 'NC-H3 lỗi chỉ vào Cảnh báo; NC-H1 lỗi (a) vào Chặn', [] if not cap112.cap('NC-H3', dict(loi=['(a) x']))[1] and cap112.cap('NC-H1 [bo]', dict(loi=['(a) x']))[1] else ['sai'], False)
case('cấp', 'NC-H5 (b) Cảnh báo, (a) Chặn', [] if cap112.cap('NC-H5', dict(loi=['(b) x']))[2] and cap112.cap('NC-H5', dict(loi=['(a) x']))[1] else ['sai'], False)
case('cấp', 'luật lạ (không có trong CAP) → Chặn mặc định (an toàn)', cap112.cap('NC-H9', dict(loi=['x']))[1], True)

for rule, name, kind_, ok, got in R: print(f"{'ĐÚNG' if ok else 'SAI '}  {rule:<11} {kind_:<8} {name}" + ('' if ok else f'   → {got}'))
by = {}
for rule, _, k, ok, _ in R: by.setdefault(rule, set()).add(k)
miss = [k for k, v in by.items() if v != {'sạch', 'bắt lỗi'} and k not in ('AGL',)]
n_ok = sum(r[3] for r in R); print(f'\nselftest 1.13: {n_ok}/{len(R)} ca đúng kỳ vọng · {len(by)} nhóm, luật thiếu ca đạt hoặc trượt: {miss or "không"}')
sys.exit(0 if n_ok == len(R) and not miss else 1)
