#!/opt/cine/bin/python
"""Tự kiểm luật LL v2 (phiên K). Mỗi luật: BẮT lỗi thật đã gặp ở tập 2–5 và KHÔNG báo nhầm trên dữ liệu đạt.

  /opt/cine/bin/python checks/ll/selftest_ll.py        mã thoát 0 = mọi ca đúng kỳ vọng

Dữ liệu: checks/ll/fixtures/ep02–05 (bản sao đóng băng episode.yaml + timeline dựng lại từ giọng đã lưu + chữ phát hành
+ hộp chữ thumbnail của bản G3), ep03-v1-4833ac1.yaml (đặc tả tập 3 trước khi chủ dự án bỏ thẻ +87 % ↔ −13 %).
Log render không lưu trong repo: ca cần log dùng log tối thiểu dựng lại đúng chữ/hộp của lỗi (ghi rõ ở từng ca).
"""
import copy, glob, gzip, json, os, sys, tempfile

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

# ======================= LL v3 (07/10/2026): Q14 tựa trên cảnh đinh, Q16 mẫu toàn khung mới, Q26–Q31 =======================
# Dữ liệu thật: tập 1 m23 (chuẩn gốc), tập 6 v1 (đã đăng), tập 6 v2 (G2 lần 2) — fixtures/ep06 (mẫu Q26 đo bằng q_diversity.samples
# trên screening/*.mp4; timeline dựng lại từ giọng đã lưu, 0 ký tự ElevenLabs; mix.json dựng lại bằng mix.py: −14,0 LUFS / −1,6 dBTP như P báo;
# câu trả lời thật của 9 subagent Sonnet trên đề bài khoá).
import numpy as np  # noqa: E402
from checks.ll import q_diversity as QD, q_av as QA, q_blind as QB  # noqa: E402
F6 = os.path.join(FX, 'ep06')
E6 = base.load(os.path.join(F6, 'episode.yaml')); TL6 = json.load(gzip.open(os.path.join(F6, 'timeline-v2.json.gz')))
TL6v1 = json.load(gzip.open(os.path.join(F6, 'timeline-v1-cuts.json.gz'))); MX6 = json.load(gzip.open(os.path.join(F6, 'mix-v2.json.gz')))
r6 = q_rhythm.measure(E6, TL6)
case('Q14', 'tập 6 v2: tựa (text + lamp) ở 19,8 s', [] if r6['Q14']['ok'] else [r6['Q14']['val']], False)
TLb = copy.deepcopy(TL6); sg1 = TLb['segments'][1]; sg1['shots'][0] = dict(sg1['shots'][0], tpl='plate', p=dict(hero='shop_walk', title='The Hand That Drew It'))
case('Q14', 'đề nghị P: tựa chồng lên cảnh đinh (plate + title), timeline', [] if q_rhythm.measure(E6, TLb)['Q14']['ok'] else ['trượt'], False)
lg = {'01': dict(id='01', fmt='16x9', text=[dict(f=10, items=[dict(s='Last Lamplighters · Episode 6')])])}
case('Q14', 'plate khai title nhưng log render không có chữ tựa', [] if q_rhythm.measure(E6, TLb, lg)['Q14']['ok'] else ['trượt'], True)
lg['01']['text'].append(dict(f=20, items=[dict(s='THE HAND THAT'), dict(s='DREW IT')]))
case('Q14', 'plate + title, log render có chữ tựa trong khoảng shot', [] if q_rhythm.measure(E6, TLb, lg)['Q14']['ok'] else ['trượt'], False)
TLb = copy.deepcopy(TL6); TLb['segments'][1]['shots'][0] = dict(TLb['segments'][1]['shots'][0], tpl='plate', p=dict(hero='shop_walk'))
case('Q14', 'plate không khai title: không còn tựa', [] if q_rhythm.measure(E6, TLb)['Q14']['ok'] else ['trượt'], True)
case('Q16', f"tập 6 v2: 5 mẫu toàn khung mới không tính thẻ giấy ({r6['Q16']['val']})", [] if r6['Q16']['ok'] else [r6['Q16']['val']], False)
TLb = copy.deepcopy(TL6)
for sg in TLb['segments']:
    for sh in sg['shots']:
        if sh['tpl'] in ('plate', 'diptych', 'jobboard', 'filmstrip', 'pasteup'): sh['tpl'] = 'quote'
case('Q16', 'tập 6 v2 nếu các cảnh đó là thẻ giấy: vượt trần 40 %', [] if q_rhythm.measure(E6, TLb)['Q16']['ok'] else ['trượt'], True)


def q26(tag, TL=None, G=None):
    z = np.load(os.path.join(F6, f'q26-{tag}.npz')); g = z['g'].astype(np.float32) if G is None else G
    return QD.measure(g, z['t'], z['part'], float(z['T']), TL)


r = q26('ep01-m23'); case('Q26', f"tập 1 (chuẩn gốc, không timeline): {r['val']}", [] if r['ok'] else [r['val']], False)
r = q26('ep06-v1', TL6v1); case('Q26', f"tập 6 v1 (khung lặp 46 % theo P): {r['val']}", [] if r['ok'] else [r['val']], True)
R[-1] = R[-1][:3] + (R[-1][3] and r['ty_le_lon_nhat'] > 20 and r['khung_nhin'] < 40,) + R[-1][4:]
r = q26('ep06-v2', TL6); case('Q26', f"tập 6 v2 (ranh giới timeline): {r['val']}", [] if r['ok'] else [r['val']], False)
r = q26('ep06-v2'); case('Q26', f"tập 6 v2 (ranh giới dò trên hình): {r['val']}", [] if r['ok'] else [r['val']], False)
z = np.load(os.path.join(F6, 'q26-ep06-v2.npz')); g = z['g'].astype(np.float32).copy(); t = z['t']
cut = sorted(QD.tl_cuts(TL6)); a0, a1, a2, a3 = cut[30], cut[31], cut[32], cut[33]   # ba cảnh liền nhau: chép khung cảnh đầu sang hai cảnh sau
src = g[(t >= a0) & (t < a1)][len(g[(t >= a0) & (t < a1)]) // 2]
for lo, hi in ((a1, a2), (a2, a3)): g[(t >= lo) & (t < hi)] = src
r = q26('ep06-v2', TL6, g); case('Q26', f'tập 6 v2 + ba cảnh liền cùng một hình (cắt nhảy): chuỗi {r["canh_lien_cung_bo_cuc"]}', [] if r['ok'] else [r['val']], True)
g2 = z['g'].astype(np.float32).copy(); i = (t >= a1) & (t < a2); g2[i] = np.clip(src * 0.25 + 4, 0, 255)   # cảnh 2: cùng hình nhưng tối hẳn
g2[(t >= a2) & (t < a3)] = src
r = q26('ep06-v2', TL6, g2); case('Q26', f'cùng hình, cảnh giữa tối đi 4 lần: vẫn là cùng bố cục (chuẩn hoá sáng/tương phản), chuỗi {r["canh_lien_cung_bo_cuc"]}', [] if r['ok'] else [r['val']], True)
D = QD.mad(z['g'][::6].astype(np.float32)); lab = QD.complete_link(D, QD.TOL_VIEW)
case('Q26', 'liên kết đầy đủ: mọi cặp trong một khung nhìn chênh < 12/255', [k for k in set(lab) if (D[np.ix_(lab == k, lab == k)] >= QD.TOL_VIEW).any()], False)

r = QA.q28(E6, TL6, MX6, asr=False)
case('Q28', f"tập 6 v2: {r['val']}", r['loi'], True)
R[-1] = R[-1][:3] + (R[-1][3] and len(r['loi']) == 1 and '05@0.0/diptych' in r['loi'][0] and '10@16.7/diptych' in r['loi'][0],) + R[-1][4:]
MXb = copy.deepcopy(MX6); MXb['sfx_used'] += [dict(file='assets/ll/sfx/press-rhythm.mp3', at=163.5, dur=3.0), dict(file='assets/ll/sfx/typewriter-old.mp3', at=385.0, dur=3.0)]
case('Q28', 'tập 6 v2 + âm thanh nghề cho 2 shot diptych', QA.q28(E6, TL6, MXb, asr=False)['loi'], False)
MXc = copy.deepcopy(MXb); MXc['music_used'][-1]['file'] = 'assets/ll/music/Clean-Soul.mp3'
case('Q28', 'kết bằng cue hồi 3 thay nhạc hiệu kênh', QA.q28(E6, TL6, MXc, asr=False)['loi'], True)
MXc = copy.deepcopy(MXb); MXc['music_used'][1]['src_to'] = 400.0; MXc['music_used'][1]['t1'] = MXc['music_used'][1]['t0'] + 400.0
case('Q28', 'cue hồi 2 dài hơn bài nhạc (phải lặp vòng)', QA.q28(E6, TL6, MXc, asr=False)['loi'], True)
MXc = copy.deepcopy(MXb); MXc['music_used'].append(dict(file='assets/ll/music/Gymnopedie-No-1.mp3', ss=20.0, src_to=110.0, t0=400.0, t1=490.0))
case('Q28', 'dùng lại 90 s cùng đoạn bài hồi 2', QA.q28(E6, TL6, MXc, asr=False)['loi'], True)
Eb = copy.deepcopy(E6); Eb['numbers'][Eb['anchors'][0]]['say'] = 'eighty six thousand people'
case('Q28', 'số neo có cụm say không có trong lời (P cũ bỏ qua im lặng)', QA.q28(Eb, TL6, MXb, asr=False)['loi'], True)
TLb = copy.deepcopy(TL6); sg4 = next(s for s in TLb['segments'] if s['id'] == '04'); sg4['vo_file'] = sg4['vo_file'].replace('.p.mp3', '.mp3')
case('Q28', 'đoạn 04 dùng lời chưa chèn lặng trước "eighty-six thousand"', QA.q28(E6, TLb, MXb, asr=False)['loi'], True)
case('Q28', 'lặng trước số neo đo trên âm thật: 4 lần đọc (gồm "seventeen percent" lần 2 ở đoạn 09)', [] if len(QA.q28(E6, TL6, MXb, asr=False)['lang']) == 4 else ['thiếu'], False)

r = QA.q29(E6, TL6); case('Q29', f"tập 6 v2: {r['val']}", r['loi'], False)
TLb = copy.deepcopy(TL6)
for sg in TLb['segments']:
    if sg['id'] == '04':
        for sh in sg['shots']: sh['tpl'] = 'bignum'
case('Q29', 'đoạn 04 chỉ còn thẻ số: "eighty-six thousand" không có hình vật chất', QA.q29(E6, TLb)['loi'], True)
Eb = copy.deepcopy(E6); Eb['segments'][3]['map'].pop('nouns')
case('Q29', 'đoạn có lời không khai danh từ chính', QA.q29(Eb, TL6)['loi'], True)

tone = {int(k): v for k, v in json.load(open(os.path.join(F6, 'tone-v2.json'))).items()}
r = QA.q30(E6, TL6, MX6, tone=tone); case('Q30', f"tập 6 v2: {r['val']}", r['loi'], True)
R[-1] = R[-1][:3] + (R[-1][3] and len(r['loi']) == 1 and '01→02: shot trước' in r['loi'][0],) + R[-1][4:]   # Q-L30 = B: màu hồi 3 ĐẠT (b* 7,9 < 9,5)
tc = dict(tone); tc[3] = dict(a=-2.0, b=-9.0, C=9.2, h=257.5, mau=1)
E6l = copy.deepcopy(E6); E6l['heroes']['case_line']['lamp'] = True   # P khai đèn cho góc máy mới (người xem/K đối chiếu sau)
case('Q30', 'tập 6 v2 nếu hồi 3 lạnh thật (h 258°, C 9) và case_line khai đèn', QA.q30(E6l, TL6, MX6, tone=tc)['loi'], False)
case('Q30', 'Q-L30 B: tập 6 v2 thật, case_line khai đèn (hồi 3 b* 7,9 thấp nhất)', QA.q30(E6l, TL6, MX6, tone=tone)['loi'], False)
Eb = copy.deepcopy(E6l); Eb['segments'][1]['map']['out'] = 'cut'
case('Q30', 'chuyển hồi 01→02: hai phía khai khác nhau (cut / match)', QA.q30(Eb, TL6, MX6, tone=tc)['loi'], True)
MXc = copy.deepcopy(MX6); cut12 = TL6['segments'][2]['t0']; MXc['sfx_used'] = [c for c in MXc['sfx_used'] if not (cut12 - 3 < c['at'] < cut12)]
case('Q30', 'J-cut 01→02 bỏ tiếng máy vào trước điểm cắt', QA.q30(E6l, TL6, MXc, tone=tc)['loi'], True)
TLb = copy.deepcopy(TL6); TLb['segments'][2]['shots'][0]['p']['hero'] = 'x_khong_den'
case('Q30', 'shot đầu hồi 2 là cảnh đinh không có đèn', QA.q30(E6l, TLb, MX6, tone=tc)['loi'], True)
tb = copy.deepcopy(tone); tb[2]['b'] = 7.0
case('Q30', 'Q-L30 B: hồi 2 (b* 7,0) lạnh hơn hồi 3 (7,9)', QA.tone_errors(tb), True)
tb = copy.deepcopy(tone); tb[3]['b'] = tb[2]['b']
case('Q30', 'Q-L30 B: hồi 3 bằng hồi 2 (không lạnh NHẤT)', QA.tone_errors(tb), True)
tb = {k: v for k, v in tone.items() if k != 3}
case('Q30', 'Q-L30 B: hồi 3 không có cảnh toàn khung để đo', QA.tone_errors(tb), True)
r = QA.q30(E6l, TL6, MX6, tone={**tone, 3: dict(tone[3], b=9.2)})
case('Q30', 'Q-L30 B: hồi 3 b* 9,2 so với 9,5 được nêu là sát ngưỡng ±5 %', [] if r['ok'] and r['sat_nguong'] else ['thiếu'], False)

for tag, exp in (('v2', True), ('v1', True)):
    fx = json.load(open(os.path.join(F6, f'q27-{tag}.json'))); r = QB.agg27(fx['sets'], fx['replies'])
    case('Q27', f"tập 6 {tag}, bản 10 + 10 (trước Q-L27): {r['val']}", [] if r['ok'] else [r['val']], exp)


def strata_ok(plan):
    """Q-L27 = B: đúng 30 khung mỗi bộ; mỗi khung rơi vào đúng một tầng (1/30 thời lượng dùng được), mỗi tầng một khung"""
    err = []
    for k in ('new', 'ref'):
        it = [(v, t) for s_, v, t in plan.values() if s_ == k]
        if len(it) != QB.N27: err.append(f'{k}: {len(it)} khung'); continue
        vids = sorted({v for v, _ in it}, key=lambda v: [x for x, _ in QB.REF27].index(v) if k == 'ref' else v)
        L = [(v, QB.dur(v) - 2 * QB.EDGE) for v in vids]; tot = sum(d for _, d in L); pos = []
        for v, t in it: pos.append(sum(d for w, d in L[:[w for w, _ in L].index(v)]) + t - QB.EDGE)
        if sorted(int(x / tot * QB.N27) for x in pos) != list(range(QB.N27)): err.append(f'{k}: tầng không đều')
    return err


V2v = [f'screening/ll-ep06-v2-p{i}.mp4' for i in (1, 2, 3)]
_, P27 = QB.plan27(V2v)
case('Q27', 'Q-L27 B: bộ tập 6 v2 có 30 + 30 khung, mỗi tầng 1/30 thời lượng một khung', strata_ok(P27), False)
case('Q27', 'Q-L27 B: thứ tự trộn tất định theo SHA video (dựng lại ra cùng bộ)', [] if QB.plan27(V2v)[1] == P27 else ['khác'], False)
for tag in ('v2', 'v1'):
    f = os.path.join(F6, f'q27b-{tag}.json')
    if os.path.exists(f):
        fx = json.load(open(f)); r = QB.agg27(fx['sets'], fx['replies'])
        case('Q27', f"tập 6 {tag}, bản 30 + 30 (đề bài F01–F60, 3 Sonnet thật): {r['val']}", [] if r['ok'] else [r['val']], fx['ky_vong_truot'])
fx = json.load(open(os.path.join(F6, 'q27-v2.json'))); up = copy.deepcopy(fx['replies'])
for x in up.values():
    for k, v in x['scores'].items():
        if fx['sets'][k] == 'new': x['scores'][k] = {c: min(10, s + 1) for c, s in v.items()}
case('Q27', 'tập 6 v2 nếu mọi khung tập mới +1 điểm', [] if QB.agg27(fx['sets'], up)['ok'] else ['trượt'], False)
bad = copy.deepcopy(fx['replies']); bad['R2']['scores'].pop('F07')
case('Q27', 'một người chấm bỏ sót khung', [] if QB.agg27(fx['sets'], bad)['ok'] else ['trượt'], True)
case('Q27', 'chỉ 2 người chấm', [] if QB.agg27(fx['sets'], {k: v for k, v in fx['replies'].items() if k != 'R3'})['ok'] else ['trượt'], True)
fx = json.load(open(os.path.join(F6, 'q31-v2.json'))); r = QB.agg31(fx['cuts'], fx['replies'])
case('Q31', f"tập 6 v2 (đề bài khoá, 3 Sonnet thật): {r['val']}", r['loi'], True)
cl = copy.deepcopy(fx['replies'])
for x in cl.values(): x['issues'] = [i for i in x['issues'] if i['kind'] == 'boring']
case('Q31', 'chỉ còn điểm "chán" đồng thuận: không chặn', QB.agg31(fx['cuts'], cl)['loi'], False)
one = copy.deepcopy(cl); one['R1']['issues'].append(dict(where='T05', kind='break', note='x'))
case('Q31', 'một người nêu đứt mạch T05: chưa đủ 2/3', QB.agg31(fx['cuts'], one)['loi'], False)
one['R3']['issues'].append(dict(where='R05.1', kind='break', note='y'))   # R05.1 = 2:42, T05 = 2:41,8 → cùng điểm
case('Q31', 'hai người nêu cùng chỗ (T05 và R05.1, cách 0,2 s)', QB.agg31(fx['cuts'], one)['loi'], True)
# Q-L31 (A có điều kiện; vòng tính theo từng tập)
fx = json.load(open(os.path.join(F6, 'q31-v2.json')))
r2 = QB.agg31(fx['cuts'], fx['replies'], vong=2)
case('Q31', f"vòng 2, tập 6 v2: chỉ chặn 3/3 (T03, T05, T10) → {r2['val']}", r2['loi'], True)
R[-1] = R[-1][:3] + (R[-1][3] and sum(x.startswith('đứt mạch') for x in r2['loi']) == 3,) + R[-1][4:]
only2 = copy.deepcopy(fx['replies'])
for x in only2.values(): x['issues'] = [i for i in x['issues'] if i['where'] in ('T01', 'T07')]
case('Q31', 'vòng 1: điểm 2/3 (T01, T07) chặn', QB.agg31(fx['cuts'], only2, vong=1)['loi'], True)
case('Q31', 'vòng 2: điểm 2/3 chưa giải trình → chặn', QB.agg31(fx['cuts'], only2, vong=2)['loi'], True)
gt = {'T01': 'Mở bằng số liệu rồi mới tựa là chủ ý: hook đặt câu hỏi trước tựa (chủ dự án duyệt G1).', 'T07': 'ngắn'}
case('Q31', 'vòng 2: T07 giải trình quá ngắn (< 20 ký tự) → chặn', QB.agg31(fx['cuts'], only2, vong=2, giai_trinh=gt)['loi'], True)
gt['3:56.9'] = 'Cắt cứng sang tường tối là nhịp chuyển sang câu hỏi BLS; đã làm rõ chú thích.'
case('Q31', 'vòng 2: mọi điểm 2/3 có giải trình (theo T## hoặc m:ss.s)', QB.agg31(fx['cuts'], only2, vong=2, giai_trinh=gt)['loi'], False)
hd = tempfile.mkdtemp(); out31 = os.path.join(hd, 'q31'); os.makedirs(os.path.join(hd, 'q31-lich-su', 'vong-01')); os.makedirs(os.path.join(hd, 'q31-lich-su', 'vong-02'))
for r_ in QB.RATERS: open(os.path.join(hd, 'q31-lich-su', 'vong-01', f'{r_}.json'), 'w').write('{}')
open(os.path.join(hd, 'q31-lich-su', 'vong-02', 'R1.json'), 'w').write('{}')
case('Q31', 'lịch sử vòng: chỉ đếm vòng chấm đủ 3 người (1 đủ, 1 dở → vòng hiện tại = 2)', [] if len(QB._rounds(out31)) == 1 else ['sai'], False)

tmpd = tempfile.mkdtemp()
for k, x in fx['replies'].items(): json.dump(dict(x, prompt_sha256='0' * 64) if k == 'R2' else x, open(os.path.join(tmpd, f'{k}.json'), 'w'))
case('Q31', 'R2 dùng đề bài đã sửa (SHA khác bản khoá)', QB._replies(tmpd, 'Q31')[1], True)
case('Q27', 'đề bài Q27 nêu đủ 60 ảnh F01–F60', [f for f in ('Q27-R1.txt', 'Q27-R2.txt', 'Q27-R3.txt') if 'F60' not in open(os.path.join(QB.HERE, f)).read()], False)
case('Q27/31', 'đề bài khoá: 6 tệp, mỗi tệp có {DIR} và yêu cầu chỉ trả JSON', [f for f in sorted(os.listdir(QB.HERE)) if '{DIR}' not in open(os.path.join(QB.HERE, f)).read() or 'ONLY this JSON' not in open(os.path.join(QB.HERE, f)).read()], False)

w = max(len(r[1]) for r in R)
for rule, name, kind_, ok, got in R: print(f"{'ĐÚNG' if ok else 'SAI '}  {rule:<7} {kind_:<8} {name}" + ('' if ok else f'   → {got}'))
n_ok = sum(r[3] for r in R); print(f'\nselftest LL v3: {n_ok}/{len(R)} ca đúng kỳ vọng'); sys.exit(0 if n_ok == len(R) else 1)
