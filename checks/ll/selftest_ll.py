#!/opt/cine/bin/python
"""Tự kiểm luật LL v2 (phiên K). Mỗi luật: BẮT lỗi thật đã gặp ở tập 2–5 và KHÔNG báo nhầm trên dữ liệu đạt.

  /opt/cine/bin/python checks/ll/selftest_ll.py        mã thoát 0 = mọi ca đúng kỳ vọng

Dữ liệu: checks/ll/fixtures/ep02–05 (bản sao đóng băng episode.yaml + timeline dựng lại từ giọng đã lưu + chữ phát hành
+ hộp chữ thumbnail của bản G3), ep03-v1-4833ac1.yaml (đặc tả tập 3 trước khi chủ dự án bỏ thẻ +87 % ↔ −13 %).
Log render không lưu trong repo: ca cần log dùng log tối thiểu dựng lại đúng chữ/hộp của lỗi (ghi rõ ở từng ca).
"""
import copy, glob, gzip, json, os, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, ROOT)
from checks.ll import base, llcheck as C, q_rhythm, q_rights, q_src, q_overflow  # noqa: E402

FX = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures')
R = []


def case(rule, name, got, expect_fail):
    ok = bool(got) == expect_fail
    R.append((rule, name, 'bắt lỗi' if expect_fail else 'sạch', ok, got[:2] if got else []))


def ep(n):
    d = os.path.join(FX, f'ep{n}'); E = base.load(os.path.join(d, 'episode.yaml'))
    TL = json.load(gzip.open(os.path.join(d, 'timeline.json.gz')))
    th = sorted(glob.glob(os.path.join(d, '*.boxes.json'))); E['_path'] = os.path.join(d, 'episode.yaml'); E['_thumbs'] = th
    return E, TL, d, th


def shot(TL, sid, tpl):
    sg = next(s for s in TL['segments'] + TL['shorts'] if s['id'] == sid)
    return sg, next(sh for sh in sg['shots'] if sh['tpl'] == tpl)


def log(sid, f, items, fmt='16x9', **kw):
    return {sid: dict(id=sid, fmt=fmt, hit='0', text=[dict(f=f, items=[dict(s=s, box=b) for s, b in items], **kw)])}


EP = {n: ep(n) for n in ('02', '03', '04', '05')}

# ---- Q7 nhãn ACTUAL/PROJECTION — lỗi thật: tập 2 Short S2, bignum −5,3 % (dự báo) hiện nhãn ACTUAL ----
E, TL, d, th = EP['02']; sg, sh = shot(TL, 'S2', 'bignum'); f = int(sh['t0'] * 24) + 30
case('Q7', 'tập 2 S2: −5,3 % dự báo hiện nhãn ACTUAL (log)', C.q7(E, TL, log('S2', f, [('ACTUAL', [900, 300, 1000, 330]), ('−5.3%', [700, 400, 1100, 560])], '9x16')), True)
TLb = copy.deepcopy(TL); shot(TLb, 'S2', 'bignum')[1]['p']['kind'] = 'actual'
case('Q7', 'tập 2 S2: đặc tả khai kind=actual cho nums dự báo', C.q7(E, TLb, {}), True)
case('Q7', 'tập 2 S2 bản G3: nhãn PROJECTION', C.q7(E, TL, log('S2', f, [('PROJECTION', [900, 300, 1100, 330]), ('−5.3%', [700, 400, 1100, 560])], '9x16')), False)
for n in EP: case('Q7', f'tập {n} G3: đặc tả', C.q7(EP[n][0], EP[n][1], {}), False)

# ---- Q12 thumbnail — lỗi thật: tập 2 T1 mất chữ S của "OPERATORS" ở mép phải ----
bx = json.load(open(os.path.join(EP['02'][2], 'll-ep02-thumb-T1.jpg.boxes.json')))
tmp = os.path.join(os.environ.get('TMPDIR', '/tmp'), 'll_q12_T1.jpg.boxes.json'); bad = copy.deepcopy(bx); bad['boxes'][0]['box'][2] = 1292.0
json.dump(bad, open(tmp, 'w'))
case('Q12', 'tập 2 T1: hộp "…OPERATORS." vượt mép phải (1292 > 1216)', C.q12([tmp]), True)
case('Q12', 'tập 2 T1: không có .boxes.json (dựng tay như bản lỗi)', C.q12([tmp + '.missing.jpg']), True)
for n in EP: case('Q12', f'tập {n} G3: T1, T2', C.q12(EP[n][3]), False)

# ---- Q13 số trên bề mặt phát hành ----
for n in EP: case('Q13', f'tập {n} G3: tiêu đề, thumbnail, mô tả, Shorts', C.q13(EP[n][0], EP[n][2], EP[n][3]), False)
E5 = copy.deepcopy(EP['05'][0])
E5['title'] = 'Auto damage appraisers will shrink 9%'; case('Q13', 'tiêu đề nêu −9 % (dự báo) không có dấu hiệu dự báo', C.q13(E5, '/nonexistent', []), True)
E5['title'] = 'Appraisers projected to grow +9% by 2035'; case('Q13', 'tiêu đề +9 % sai dấu (số thật −9 %)', C.q13(E5, '/nonexistent', []), True)
E5['title'] = 'In 1966, 884,700 people worked in insurance offices'; case('Q13', 'tiêu đề số thật truy được', C.q13(E5, '/nonexistent', []), False)
E3 = copy.deepcopy(EP['03'][0]); E3['title'] = '135k tellers in 1960'; case('Q13', 'tập 3: "135k" truy về 135,000', C.q13(E3, '/nonexistent', []), False)
E3['title'] = '150k tellers in 1960'; case('Q13', 'tập 3: "150k" không có trong numbers', C.q13(E3, '/nonexistent', []), True)

# ---- Q14–Q18 luật nhịp (tập 3 làm trước luật: phải trượt như tổng kết lô 3–5; tập 4–5 đạt) ----
for n, exp in (('03', True), ('04', False), ('05', False)):
    r = q_rhythm.measure(EP[n][0], EP[n][1])
    case('Q14–18', f"tập {n}: {'; '.join(k + ('✓' if v['ok'] else '✗') for k, v in r.items())}", [k for k, v in r.items() if not v['ok']], exp)

# ---- Q19 hồ sơ quyền tư liệu ----
E, TL = EP['05'][0], EP['05'][1]
case('Q19', 'tập 5 G3: 4 dòng RIGHTS, 16,5 %', q_rights.check(E, TL)[0], False)
Eb = copy.deepcopy(E); a = next(sh for s in Eb['segments'] for sh in s['shots'] if sh['tpl'] == 'archive'); a['p']['rid'] = 'LOC-khong-co'
case('Q19', 'tập 5: shot archive trỏ rid không có trong RIGHTS', q_rights.check(Eb, TL)[0], True)
Eb = copy.deepcopy(E); next(sh for s in Eb['segments'] for sh in s['shots'] if sh['tpl'] == 'archive')['p'].pop('credit', None)
case('Q19', 'tập 5: shot archive thiếu dòng ghi nguồn trên hình', q_rights.check(Eb, TL)[0], True)
case('Q19', 'URL giả .gov (loc.gov.evil.com) không qua danh sách trắng', [] if q_rights.WL.search('https://www.loc.gov.evil.com/x') is None else ['qua'], False)

# ---- Q20 chữ đè hình (isotype) ----
iso = log('07', 120, [('Source: BLS', [110, 1000, 900, 1030])], zones=[[100, 600, 1800, 1020]])
case('Q20', 'chú thích giao vùng isotype khai trong log', C.q20(iso, {'07'}), True)
case('Q20', 'cờ hit của render', C.q20({'07': dict(hit='0001', text=[])}), True)
case('Q20', 'tập ≥ 6: đoạn isotype không ghi zones', C.q20(log('07', 120, [('x', [110, 1040, 300, 1060])]), {'07'}, need_zones=True), True)
case('Q20', 'chú thích dưới vùng hình', C.q20(log('07', 120, [('Source: BLS', [110, 1040, 900, 1066])], zones=[[100, 600, 1800, 1020]]), {'07'}, True), False)

# ---- Q21 dòng nguồn khớp — lỗi thật: tập 5 đoạn 00 "1966: …" hiện dưới dòng nguồn BLS OOH 2025–35 ----
E, TL = EP['05'][0], EP['05'][1]
case('Q21', 'tập 5 G3: 0 lỗi', q_src.check(E, TL), False)
Eb, TLb = copy.deepcopy(E), copy.deepcopy(TL)
c = TLb['segments'][0]['shots'][0]['p']['cap'][1]; c.pop('src', None)   # bản G2: câu 1966 không mang dòng nguồn riêng
TLb['capsrc']['00/0/1'] = {'srcs': [], 'declared': False}; Eb['segments'][0]['shots'][0]['p']['cap'][1].pop('src', None)
case('Q21', 'tập 5 đoạn 00: "1966…" dưới dòng nguồn OOH (bản G2)', q_src.check(Eb, TLb), True)
TLb = copy.deepcopy(TL); TLb['capsrc']['00/0/1'] = {'srcs': [], 'declared': True}; TLb['segments'][0]['shots'][0]['p']['cap'][1]['src'] = TLb['segments'][0]['shots'][0]['p']['src']
case('Q21', 'tập 5: capsrc (P ghi) bỏ trống nguồn nhưng đặc tả khai src B1468 → K vẫn đòi', q_src.check(E, TLb), True)

# ---- Q22 chữ tràn khung — lỗi thật: tập 5 Shorts, dòng nguồn dài tràn hai mép 9:16 ----
case('Q22', 'tập 5 S1: "Source: BLS, Occupational Outlook…" hộp −338…1418 trên khung 1080', q_overflow.check(log('S1', 48, [('Source: BLS, Occupational Outlook', [-338, 1769, 1418, 1800])], '9x16')), True)
case('Q22', 'tập 5 đoạn 07 (16:9): dòng nguồn ghép tràn mép phải', q_overflow.check(log('07', 48, [('Sources: BLS USDL-25-1520 · BLS OOH', [1180, 1040, 1925, 1066])])), True)
case('Q22', 'Shorts gọn (short9) trong lề 8 px', q_overflow.check(log('S1', 48, [('Source: BLS Outlook Handbook 2025–35', [60, 1769, 1020, 1800])], '9x16')), False)

# ---- Q23 câu/thẻ nhiều số — lỗi thật: tập 3 v1 thẻ so sánh +87 % (1960–70, đếm) ↔ −13 % (2025–35, dự báo) ----
E1 = base.load(os.path.join(FX, 'ep03-v1-4833ac1.yaml'))
seg = next(s for s in E1['segments'] for sh in s['shots'] if sh['tpl'] == 'compare')
cmp_ = next(sh for sh in seg['shots'] if sh['tpl'] == 'compare')
K = set(base.nums_in(cmp_['p'], [], True))
case('Q23', f"tập 3 v1 thẻ so sánh {'/'.join(E1['numbers'][k]['text'] for k in sorted(K))}", C.frame_errors(E1['numbers'], K, '', E1.get('sources')), True)
N3 = EP['03'][0]['numbers']
case('Q23', 'câu "+87 % … while tellers −13 %"', C.frame_errors(N3, C.keys_spoken(N3, 'Teller jobs grew eighty-seven percent, and the BLS projects a decline of thirteen percent.') | {'tel_hist'}, '', EP['03'][0]['sources']), True)
case('Q23', 'câu 2025 → 2035 (điểm gốc + dự báo, cùng nguồn)', C.frame_errors(EP['05'][0]['numbers'], {'ca25', 'ca35', 'ca_chg'}, '', EP['05'][0]['sources']), False)
case('Q23', 'tập 3: 65 nghìn (phân loại 1960) + 253 nghìn (1970) không ghi cơ sở', C.frame_errors(N3, {'tel50', 'tel70'}, 'Bank tellers', EP['03'][0]['sources']), True)
case('Q23', 'tập 3: cùng cặp số, ghi rõ từng cơ sở', C.frame_errors(N3, {'tel50', 'tel70'}, '1960 classification · 1970 classification', EP['03'][0]['sources']), False)
for n in ('03', '05'): case('Q23', f'tập {n} G3: lời, thẻ, chú thích, bề mặt phát hành', C.q23(EP[n][0], EP[n][1]), False)
q4 = C.q23(EP['04'][0], EP['04'][1])   # phát hiện thật khi chạy thử: hook Short S1 nối 134,000 (1900, phân loại 1950) với 3.9 million (1970)
case('Q23', 'tập 4 G3 (trước luật): chỉ hook S1 "134,000 to 3.9 million" bị bắt', q4, True)
R[-1] = R[-1][:3] + (R[-1][3] and all(x.startswith('hook S1') for x in q4),) + R[-1][4:]
q2 = C.q23(EP['02'][0], EP['02'][1])
case('Q23', 'tập 2 G3 (trước luật): thẻ so sánh 11 −16,1 % (1930–40) ↔ −5,3 % (2025–35) bị bắt', q2, True)
R[-1] = R[-1][:3] + (R[-1][3] and all('11/compare' in x for x in q2),) + R[-1][4:]

# ---- Q24 nhãn phân loại — lỗi thật: tập 3 nhãn HSUS 135 nghìn sai phân loại ----
E, TL = EP['03'][0], EP['03'][1]
case('Q24', 'tập 3 G3: "135,000 (1970 classification)"', C.q24(E, TL), False)
TLb = copy.deepcopy(TL); ln = shot(TLb, '02', 'line')[1]['p']
for se in ln['series']:
    se['ltext'] = [t.replace('1970 classification', '1960 classification') for t in (se.get('ltext') or [])]
case('Q24', 'tập 3: 135,000 gắn nhãn "1960 classification"', C.q24(E, TLb), True)

# ---- Q25 khoảng số — lỗi thật: tập 2 thẻ "50–80 % fewer" đếm qua số trung gian ----
E, TL = EP['02'][0], EP['02'][1]
sg, sh = next((s, x) for s in TL['segments'] for x in s['shots'] if x['tpl'] == 'bignum' and '50' in str(x['p'].get('text', '')))
f = int(sh['t0'] * 24) + 12
case('Q25', f"tập 2 đoạn {sg['id']}: hiện “63%” khi đếm tới 50–80 %", C.q25(TL, log(sg['id'], f, [('63%', [700, 400, 1100, 560])])), True)
case('Q25', f"tập 2 đoạn {sg['id']}: hiện thẳng “50–80% fewer”", C.q25(TL, log(sg['id'], f, [('50–80% fewer', [600, 400, 1300, 560]), ('ACTUAL', [600, 300, 700, 330])])), False)

w = max(len(r[1]) for r in R)
for rule, name, kind_, ok, got in R: print(f"{'ĐÚNG' if ok else 'SAI '}  {rule:<7} {kind_:<8} {name}" + ('' if ok else f'   → {got}'))
n_ok = sum(r[3] for r in R); print(f'\nselftest LL v2: {n_ok}/{len(R)} ca đúng kỳ vọng'); sys.exit(0 if n_ok == len(R) else 1)
