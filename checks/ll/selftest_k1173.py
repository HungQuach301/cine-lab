#!/opt/cine/bin/python
"""Tự kiểm luật 1.17.3 (phiên K-1.17.3, 23/10/2026; khiếu nại BAN-CUOI-T3 A1–A6 — reports/ban-cuoi-t3/checks-appeal.md, phán quyết ở
checks-appeal.md mục "Phán quyết K — checks 1.17.3"): TL-3 nhận trong_pct dạng danh sách (A1), Q37 (a) đọc mốc cảnh tl/* (A2), EO-DAT-R3 (b) ranh góc
máy + lưới khung và (a) ngoại lệ có khai (A3 + đề xuất K1173-D1), PP-1 giữ luật (A4), Q33 miễn theo khoảng năm hiện (A5), SACH-1 chữ thẻ theo đặc tả
(A6). Mỗi luật đổi ≥ 1 ca ĐẠT + ≥ 1 ca TRƯỢT. KHÔNG gọi mạng/API.

Dữ liệu thật: fixtures/k1173/t3-cuoi-rut-gon.json = đặc tả + log shot bản cuối T3 (channel-k2/k2c-t3-01/cuoi @origin/main 9852adf5; SHA trong tệp;
RÚT GỌN còn các trường luật đọc). fixtures/k1173/tl7-ref.json = năm + crossing tính bằng CHÍNH design/k2v/tl/tl7.js (node) — bản sao độc lập
của K (q_nhip.tl_year/_crossings) phải trùng.

  /opt/cine/bin/python checks/ll/selftest_k1173.py      mã thoát 0 = mọi ca đúng kỳ vọng
"""
import copy, json, os, sys, tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, ROOT)
from checks.ll import q_k117 as K7, q_k116 as K6, q_nhip as Q, cap112  # noqa: E402

FX = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures', 'k1173')
T3 = json.load(open(os.path.join(FX, 't3-cuoi-rut-gon.json'))); REF = json.load(open(os.path.join(FX, 'tl7-ref.json')))
TMP = tempfile.mkdtemp(prefix='k1173-')
R, INFO = [], []


def case(rule, name, got, expect_fail):
    got = list(got) if got else []
    R.append((rule, name, 'bắt lỗi' if expect_fail else 'sạch', bool(got) == expect_fail, got[:2]))


def bad(x, *muc):
    L = x['loi'] + (x.get('thieu') or [])
    return [y for y in L if not muc or any(y.startswith(f'({m})') or f'] ({m})' in y for m in muc)]


SEG = {s['id']: s for s in T3['segments']}; LSX = {s['shot']: s for s in T3['log_shot']}

# ======================================================================== A1 — TL-3 trong_pct dạng danh sách
ET = dict(id='t3', khung_sach=True, segments=[dict(id='S1', dur=14.4167, shots=[])])
tl3 = lambda tp, tl=False: K6.tl3(ET, None, [dict(shot='S1', goc='cao', tl=tl, su_kien=[dict(t=1)], bac='3', trong_pct=tp)])
try: r = tl3(LSX['N2_7']['trong_pct']); case('TL-3', 'N2_7 thật: trong_pct [[t, %], …] 15 mẫu (≈ 42 %) → không sập, sạch (1.17.2: TypeError)', bad(r), False)
except Exception as e: case('TL-3', 'N2_7 thật: trong_pct danh sách → không sập', [f'{type(e).__name__}: {e}'], False)   # noqa: BLE001
case('TL-3', 'danh sách [[0, 80], [5, 70]] (TB 73,5 %) không thời gian chạy → (b) trống', bad(tl3([[0, 80], [5, 70]]), 'b'), True)
case('TL-3', 'danh sách [[0, 30], [1, 95]] trên 14,4 s → TB theo THỜI GIAN 90,5 % (không phải TB cộng 62,5 %) → (b)', bad(tl3([[0, 30], [1, 95]]), 'b'), True)
case('TL-3', 'danh sách [[0, 95], [13, 30]] → TB theo thời gian 89,1 % → (b); cùng shot có thời gian chạy → sạch',
     [] if bad(tl3([[0, 95], [13, 30]]), 'b') and not bad(tl3([[0, 95], [13, 30]], tl=True)) else ['sai'], False)
case('TL-3', 'dạng [{t, v}] 40 % → sạch', bad(tl3([dict(t=0, v=40), dict(t=7, v=44)])), False)
case('TL-3', 'số TB shot 65 % (dạng cũ) → (b) như 1.17.2', bad(tl3(65.0), 'b'), True)
case('TL-3', "trong_pct 'abc' → THIẾU (không sập)", K6.tl3(ET, None, [dict(shot='S1', goc='cao', tl=True, bac='3', trong_pct='abc')])['thieu'], True)

# ======================================================================== A2 — Q37 (a) mốc cảnh tl/* (bản sao tl7 + năm thế giới)
md = mc = 0.0; nc = 0
for h, v in REF['keys'].items():
    yr, _ = Q.tl_year(dict(time=v['time'], tz=v['tz']))
    md = max([md] + [abs(yr(t) - y) for t, y in REF['ref'][h]['year']])
    for Y, cs in REF['ref'][h]['cross']:
        mine = Q._crossings(yr, Y, v['T']); nc += 1
        mc = max([mc] + ([abs(a - b) for a, b in zip(mine, cs)] if len(mine) == len(cs) else [99.0]))
INFO.append(f'bản sao tl7 của K so tl7.js (node): lệch năm max {md:.2e} trên {sum(len(REF["ref"][h]["year"]) for h in REF["ref"])} điểm · lệch crossing max {mc:.3f} s trên {nc} năm')
case('Q37 (a) tl', 'bản sao đường cong thời gian của K trùng tl7.js (năm ≤ 1e-9, crossing ≤ 1/48 s)', [] if md <= 1e-9 and mc <= 1 / 48 else [f'{md} {mc}'], False)
EQ = lambda ids, beats=None: dict(id='t3', heroes=T3['heroes'], segments=[dict(SEG[i], beats=(beats or {}).get(i, SEG[i].get('beats'))) for i in ids])
a_of = lambda r, sid: [x for x in r['loi'] if x.startswith(f'(a) {sid} ')]
r0, r1 = Q.q37(EQ(['H2']), tl_moc=False), Q.q37(EQ(['H2']), tl_moc=True)
INFO.append(f"H2 thật: (a) 1.17.2 {len(a_of(r0, 'H2'))} lỗi → 1.17.3 {len(a_of(r1, 'H2'))}")
case('Q37 (a) tl', 'H2 thật: bước năm "2027 → 1310" @3,38 s (mốc opt.time t = 3,375) → 1.17.2 (a) lỗi', [x for x in a_of(r0, 'H2') if ' 3.38s ' in x], True)
case('Q37 (a) tl', 'H2 thật: cùng beat, tl_moc (1.17.3) → khớp mốc', [x for x in a_of(r1, 'H2') if ' 3.38s ' in x], False)
yr7, _ = Q.tl_year(T3['heroes']['anim_N2_7']['opt']); c7 = Q._crossings(yr7, T3['heroes']['anim_N2_7']['opt']['smoke'][1]['wY'][0], 14.4167)[0]
bt = [dict(t=0, k='cut', s='N2.7'), dict(t=round(c7, 2), k='khoi', s='khói xuất hiện (giờ trình dựng)')]
case('Q37 (a) tl', f'N2_7: khói smoke[1].wY qua đường cong opt.time → {c7:.2f} s; beat đúng giờ trình dựng → sạch',
     a_of(Q.q37(EQ(['N2_7'], {'N2_7': bt}), tl_moc=True), 'N2_7'), False)
case('Q37 (a) tl', 'N2_7: cùng beat, không tl_moc (1.17.2) → (a)', a_of(Q.q37(EQ(['N2_7'], {'N2_7': bt})), 'N2_7'), True)
case('Q37 (a) tl', 'N2_7 thật: beat "khói xuất hiện" @3,08 s (thước xưởng scripts/k2tl/cuoi_bien_co.py: nội suy tuyến tính + dy() bỏ múi giờ LMT; lệch giờ trình dựng 1,39 s) → vẫn (a) ở 1.17.3',
     [x for x in a_of(Q.q37(EQ(['N2_7']), tl_moc=True), 'N2_7') if ' 3.08s ' in x], True)
bt9 = [dict(t=0, k='cut', s='N2.7'), dict(t=9.0, k='lua', s='beat không có mốc')]
case('Q37 (a) tl', 'N2_7: beat @9,0 s không ứng mốc nào → (a) dù tl_moc (không nới bừa)', a_of(Q.q37(EQ(['N2_7'], {'N2_7': bt9}), tl_moc=True), 'N2_7'), True)
bc = [dict(t=0, k='cut', s='N1.1'), dict(t=0.4, k='the_chuong', s='1704 — The Rock changes hands')]
case('Q37 (a) tl', 'N1_1 thật: thẻ chương p.the_chuong.at 0,4 s → tl_moc khớp', a_of(Q.q37(EQ(['N1_1'], {'N1_1': bc}), tl_moc=True), 'N1_1'), False)
case('Q37 (a) tl', 'tập không cảnh opt.time: tl_moc không thêm mốc (spec_times giống hệt)',
     [] if Q.spec_times({'m': {'opt': {'cam': [{'t': 2}]}}}, [dict(at=0, p=dict(hero='m'))], 10, True) == Q.spec_times({'m': {'opt': {'cam': [{'t': 2}]}}}, [dict(at=0, p=dict(hero='m'))], 10) else ['khác'], False)

# ======================================================================== A3 — EO-DAT-R3 (b) ranh góc máy + lưới khung; (a) ngoại lệ có khai
EE = dict(id='t3', khung_sach=True, segments=[dict(id='X', dur=60, chuong='2')])
r3 = lambda s, ep_dir=TMP: K7.eo_dat(EE, None, [dict(s, noi='eo_dat', t0=0, t1=s['dur'], trong_pct=10)], None, ep_dir)['EO-DAT-R3']
for sid, kv in (('N2_11', 8.8), ('N5_4', 12.7)):
    s = copy.deepcopy(LSX[sid])
    case('EO-DAT-R3', f'{sid} thật: {s["so_goc"]} góc khai goc_may → (b) sạch (1.17.2: {kv} s)', bad(r3(s), 'b'), False)
    s.pop('goc_may')
    case('EO-DAT-R3', f'{sid} thật bỏ goc_may (chỉ so_goc) → (b) như 1.17.2', bad(r3(s), 'b'), True)
x = r3(copy.deepcopy(LSX['N5_1']))
case('EO-DAT-R3', 'N5_1 thật: 9,599 → 15,6 s = 6,001 s → lưới khung 144 khung = 6,00 s → sạch, nêu ±5 %', bad(x, 'b') + ([] if any('N5_1' in y for y in x.get('sat_nguong') or []) else ['không nêu sát ngưỡng']), False)
case('EO-DAT-R3', 'khoảng 6,10 s (146 khung) → (b)', bad(r3(dict(shot='Z', dur=20, so_goc=2, goc_may=[dict(t=0), dict(t=10)], su_kien=[dict(t=3.9), dict(t=16)])), 'b'), True)
case('EO-DAT-R3', 'goc_may t = 0 không tính ranh (đầu shot đã tính) → shot 1 góc 16 s không biến cố → (b)', bad(r3(dict(shot='Z', dur=16, so_goc=2, goc_may=[dict(t=0)])), 'b'), True)
n45 = copy.deepcopy(LSX['N4_5'])
case('EO-DAT-R3', 'N4_5 thật 1 góc, không khai ngoại lệ → (a)', bad(r3(n45), 'a'), True)
os.makedirs(os.path.join(TMP, 'ep'), exist_ok=True)
open(os.path.join(TMP, 'AUTHORSHIP.md'), 'w').write('| 2026-10-23 | T3 — 10:45 khác | không nhắc shot |\n| 2026-10-24 | T3 — R3 ngoại lệ (09:12) | N4.5, N5.6 một góc là ý đồ bookend; R3 (a) nhận |\n')
nl = dict(n45, r3_ngoai_le=dict(ly_do='bookend ngược H1 — một góc là ý đồ', authorship='2026-10-23 10:45'))
case('EO-DAT-R3', 'N4_5 khai r3_ngoai_le trỏ 23/10 10:45 nhưng dòng AUTHORSHIP đó không nêu N4_5 + R3 → vẫn (a) (K không tự cho đạt)', bad(r3(nl, os.path.join(TMP, 'ep')), 'a'), True)
ok = dict(n45, r3_ngoai_le=dict(ly_do='bookend ngược H1', authorship='2026-10-24 09:12'))
x = r3(ok, os.path.join(TMP, 'ep'))
case('EO-DAT-R3', 'N4_5 khai r3_ngoai_le + AUTHORSHIP có dòng 2026-10-24 09:12 nêu N4.5 + R3 → (a) nhận, ghi "ngoại lệ có khai"', bad(x, 'a') + ([] if 'ngoại lệ có khai' in x['val'] else [x['val']]), False)
case('EO-DAT-R3', 'r3_ngoai_le thiếu ly_do → (a)', bad(r3(dict(n45, r3_ngoai_le=dict(authorship='2026-10-24 09:12')), os.path.join(TMP, 'ep')), 'a'), True)
case('EO-DAT-R3', 'r3_ngoai_le khai nhưng không có AUTHORSHIP.md → (a)', bad(r3(ok, tempfile.mkdtemp(prefix='k1173-no-')), 'a') if not os.path.exists('/AUTHORSHIP.md') else ['môi trường có /AUTHORSHIP.md'], True)
case('cấp', 'EO-DAT-R3 (b) ở G2 → Chặn (không đổi)', cap112.cap('EO-DAT-R3', dict(r3(dict(shot='Z', dur=20, so_goc=2, goc_may=[dict(t=0), dict(t=10)], su_kien=[dict(t=3.9), dict(t=16)])), cong='G2'))[1], True)

# ======================================================================== A4 — PP-1 giữ luật: tiêu đề thẻ là chữ phải đọc
pp_seg = lambda i, d, title, items: dict(id=i, part='END', dur=d, shots=[dict(at=0, type='card', p=dict(card=dict(type='list', title=title, items=[dict(s=x) for x in items])))])
PPD = [x for x in T3['segments'] if x['id'] in ('PP1', 'PP2')]
EP = dict(id='t3', khung_sach=True, segments=[dict(id='A', dur=60)] + PPD)
case('PP-1', 'PP1 thật 26 từ thân + 5 từ tiêu đề / 9 s = 3,4 từ/s → (e) Cảnh báo (giữ luật 1.16 — K116-D8)', bad(K6.pp1(EP, None), 'e'), True)
P2 = copy.deepcopy(PPD); P2[0]['shots'][0]['p']['card']['items'] = [dict(s='Built from British and Spanish records and period maps.'), dict(s='Sources: description and pinned comment.'),
                                                                     dict(s='Estimated: ruins, camps, buildings, heights, coastline, borders.')]
case('PP-1', 'PP1 rút còn 22 từ thân + 5 tiêu đề = 27 / 9 s = 3,0 → sạch (cách khai đúng cho T4)', bad(K6.pp1(dict(EP, segments=[dict(id='A', dur=60)] + P2), None), 'e'), False)

# ======================================================================== A5 — Q33 miễn theo khoảng năm hiện (opt.time, bước năm)
EY = dict(id='t3', heroes=T3['heroes'], segments=[SEG[i] for i in ('N1_6', 'N2_10', 'N3_4', 'N5_2')])
NH = K7.nam_hien(EY)
INFO.append('năm hiện N1_6 ' + ', '.join(f'{a:.2f}–{b:.2f}' for a, b in NH['N1_6']) + f" · N2_10 {NH['N2_10']} · N3_4 {NH['N3_4']}")
AP = [dict(seg=s, t0=t) for s, t in (('N1_6', 147.6), ('N2_10', 270.2), ('N3_4', 435.3), ('N5_2', 619.0))]
NLOG = {s: tuple(LSX[s]['nam']) for s in ('N1_6', 'N2_10', 'N3_4', 'N5_2')}
m0, m1 = K7.q33_mien(AP, NLOG), K7.q33_mien(AP, K7.nam_khoang(EY, None, T3['log_shot']))
case('Q33 miễn năm', 'thật N1_6/N2_10/N3_4/N5_2 với năm log [min, max] (1.17.2) → N2_10, N3_4 KHÔNG miễn (N1_6 bao 1704–2026)', [] if {id(AP[1]), id(AP[2])} & m0 else ['không miễn'], True)
case('Q33 miễn năm', 'cùng 4 lần với khoảng năm HIỆN (1.17.3) → N2_10, N3_4, N5_2 đều miễn (≤ 2 lần tính)', [] if {id(a) for a in AP[1:]} <= m1 else [str(NH)], False)
EY2 = copy.deepcopy(EY); EY2['heroes']['anim_N2_10']['opt']['time'] = [dict(t=0, at=1704.9), dict(t=18.375, at=1705.1)]
m2 = K7.q33_mien(AP, K7.nam_khoang(EY2, None, T3['log_shot']))
case('Q33 miễn năm', 'N2_10 đổi sang 1704,9–1705,1 (chồng khoảng hiện 1704,8–1705,3 của N1_6) → N2_10 KHÔNG miễn', [] if id(AP[1]) in m2 else ['không miễn'], True)
case('Q33 miễn năm', 'dạng cũ {đoạn: (y0, y1)} vẫn đọc được (tập không opt.time)', [] if K7.q33_mien(AP[:2], {'N1_6': (1704, 1705), 'N2_10': (1782, 1782.5)}) == {id(AP[1])} else ['khác'], False)
case('Q33 miễn năm', 'cùng đoạn → không miễn dù năm khác', [] if not K7.q33_mien([dict(seg='A', t0=0), dict(seg='A', t0=5)], {'A': [(1700, 1701), (1900, 1901)]}) else ['miễn'], False)

# ======================================================================== A6 — SACH-1 chữ thẻ chương / thẻ PP theo đặc tả
CH = '1704 — The Rock changes hands'
ES = dict(id='t3', khung_sach=True, segments=[dict(id='N1_1', dur=20, shots=[dict(at=0, type='scene3d', p=dict(sach=True, the_chuong=dict(s=CH, at=0.4, dur=3.0)))])] + PPD)
TLs = dict(tong_s=37.0, segments=[dict(id='N1_1', t0=0, dur=20, shots=[dict(t0=0, t1=20, type='scene3d', p=dict(sach=True, the_chuong=dict(s=CH, at=0.4, dur=3.0)))]),
                                  dict(id='PP1', t0=20, dur=9, shots=[dict(t0=0, t1=9, type='card', p=PPD[0]['shots'][0]['p'])]),
                                  dict(id='PP2', t0=29, dur=8, shots=[dict(t0=0, t1=8, type='card', p=PPD[1]['shots'][0]['p'])])])
def TX(extra=()):
    M = {}
    for f in range(0, 37 * 24, 12):
        it = [dict(role='year', s='1704', alpha=1)]
        if 0.4 <= f / 24 < 3.4: it.append(dict(role='chuong', s=CH, alpha=1))
        if 20 <= f / 24 < 37: it += [dict(role='', s='How this film was made', alpha=1), dict(role='', s='Troops, crowds and ships: illustrative in number and layout.', alpha=1)]
        M[f] = it
    for f, x in extra: M.setdefault(f, []).append(x)
    return M
s0 = K6.sach1(ES, TLs, TX(), 12)
case('SACH-1', 'thẻ chương vai `chuong` trong khoảng khai + chữ thẻ PP vai rỗng ("How this film was made", "illustrative") → sạch (1.17.2: (c) + (e) ×2)', bad(s0, 'c', 'e'), False)
case('SACH-1', 'cùng chữ thẻ chương nhưng hiện ở 10 s (ngoài khoảng khai 0,4–3,4 s) → (e)', bad(K6.sach1(ES, TLs, TX([(240, dict(role='chuong', s=CH, alpha=1))]), 12), 'e'), True)
case('SACH-1', '"illustrative" ngoài thẻ PP (12 s) → (c) cấm', bad(K6.sach1(ES, TLs, TX([(288, dict(role='', s='Troops: illustrative', alpha=1))]), 12), 'c'), True)
case('SACH-1', 'chữ vai rỗng lạ ở 5 s → (e) như cũ', bad(K6.sach1(ES, TLs, TX([(120, dict(role='', s='Gibraltar', alpha=1))]), 12), 'e'), True)
case('SACH-1', 'chữ thẻ chương KHÁC nguyên văn khai ("1704 — The Rock is captured") trong khoảng → (e)', bad(K6.sach1(ES, TLs, TX([(24, dict(role='chuong', s='1704 — The Rock is captured', alpha=1))]), 12), 'e'), True)

# ======================================================================== áp dụng
case('1.17.3 áp dụng', 'tập trước T3: q_k117.check KHÔNG ÁP mọi hàng', [k for k, v in K7.check(dict(id='t2')).items() if v.get('ket_qua') != 'KHÔNG ÁP'], False)

# ======================================================================== kết quả
for rule, name, exp, ok, got in R: print(f"{'ĐÚNG' if ok else 'SAI '} [{rule}] {name} — kỳ vọng {exp}" + ('' if ok else f' · nhận {got}'))
print(); [print('  ' + x) for x in INFO]; print()
grp = {}
for rule, _, exp, ok, _ in R: grp.setdefault(rule, [0, 0, set()]); grp[rule][0] += ok; grp[rule][1] += 1; grp[rule][2].add(exp)
thieu = [k for k, v in grp.items() if k not in ('cấp', '1.17.3 áp dụng') and v[2] != {'sạch', 'bắt lỗi'}]
n = sum(ok for *_, ok, _ in R)
print(f"selftest 1.17.3: {n}/{len(R)} ca đúng kỳ vọng · " + ' · '.join(f'{k} {a}/{b}' for k, (a, b, _) in grp.items()) + f" · luật thiếu ca đạt hoặc trượt: {', '.join(thieu) or 'không'}")
sys.exit(0 if n == len(R) and not thieu else 1)
