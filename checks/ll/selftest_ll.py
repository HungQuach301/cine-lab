#!/opt/cine/bin/python
"""Tự kiểm luật LL v2 (phiên K). Mỗi luật: BẮT lỗi thật đã gặp ở tập 2–5 và KHÔNG báo nhầm trên dữ liệu đạt.

  /opt/cine/bin/python checks/ll/selftest_ll.py        mã thoát 0 = mọi ca đúng kỳ vọng

Dữ liệu: checks/ll/fixtures/ep02–05 (bản sao đóng băng episode.yaml + timeline dựng lại từ giọng đã lưu + chữ phát hành
+ hộp chữ thumbnail của bản G3), ep03-v1-4833ac1.yaml (đặc tả tập 3 trước khi chủ dự án bỏ thẻ +87 % ↔ −13 %).
Log render không lưu trong repo: ca cần log dùng log tối thiểu dựng lại đúng chữ/hộp của lỗi (ghi rõ ở từng ca).
"""
import copy, glob, gzip, json, os, shutil, sys, tempfile

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
        vids = sorted({v for v, _ in it}, key=lambda v: [x for x, _, _ in QB.REF27].index(v) if k == 'ref' else v)
        rd = {x: d for x, _, d in QB.REF27}
        L = [(v, (rd[v] if k == 'ref' else QB.dur(v)) - 2 * QB.EDGE) for v in vids]; tot = sum(d for _, d in L); pos = []
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
case('Q27', 'tập 6 v2 (10 + 10) nếu mọi khung tập mới +1 điểm: chênh +0,25 sát ngưỡng, không có PLAN tập sau → TRƯỢT', [] if QB.agg27(fx['sets'], up)['ok'] else ['trượt'], True)
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

# ======================= 1.8.0 (K, 09/10/2026, sau tập 7): Q27 bản cuối 1080p + SE, Q31 sổ vòng nháp → bản cuối, Q26b bối cảnh
from checks.ll import q_setting as QS  # noqa: E402
F7 = os.path.join(FX, 'ep07')
TL7 = json.load(gzip.open(os.path.join(F7, 'timeline-final.json.gz')))
tmpp = tempfile.mkdtemp()


def plan_file(name, text):
    f = os.path.join(tmpp, name); open(f, 'w', encoding='utf-8').write(text); return f


PLAN_OK = plan_file('ok.md', '# PLAN tập 08\n\n## Cải thiện hình (từ Q27 tập 7 sát ngưỡng)\n- Nội thất văn phòng: thêm đồ trên bàn, ánh cửa sổ, tách nền tối.\n- Thẻ giấy dựng xong trước khi cắt.\n')
PLAN_EMPTY = plan_file('rong.md', '# PLAN tập 08\n\n## Cải thiện hình\n\n## Việc khác\n- viết lời\n')
PLAN_NONE = plan_file('khong.md', '# PLAN tập 08\n\n## Lời\n- viết lời\n')

# ---- Q27: luật đọc lại đúng dữ liệu đã lưu ----
for tag in ('v1', 'v2'):
    fx = json.load(open(os.path.join(F6, f'q27b-{tag}.json')))
    case('Q27', f'suy lại bộ new/ref từ hạt giống khớp bộ đã lưu (tập 6 {tag}, 30 + 30)', [] if QB.sets_from_seed(fx['seed']) == fx['sets'] else ['khác'], False)
runs27 = [(json.load(open(os.path.join(F6, f'q27b-{t}.json')))['sets'], json.load(open(os.path.join(F6, f'q27b-{t}.json')))['replies']) for t in ('v1', 'v2')]
for t in ('nhap-lan-02', 'nhap-lan-03', 'nhap-lan-04b', 'chinh-thuc'):
    fx = json.load(open(os.path.join(F7, f'q27-{t}.json'))); runs27.append((QB.sets_from_seed(fx['seed']), fx['replies']))
se, per = QB.se27(runs27)
case('Q27', f'SE khoá = SE đo lại trên 6 lần chấm thật ({se:.3f}; từng lần ' + ', '.join(f'{x:.2f}' for x in per) + f') → {QB.SE27}',
     [] if round(se, 2) == QB.SE27 else [f'{se:.3f}'], False)
fx = json.load(open(os.path.join(F7, 'q27-chinh-thuc.json'))); S7 = QB.sets_from_seed(fx['seed'])
r = QB.agg27(S7, fx['replies'])
case('Q27', f"tập 7 chính thức đọc lại đúng số G2 (5,68 / 5,64): {r['val']}", [] if r['val'].startswith('tập mới 5.68 · tập 1 5.64') else [r['val']], False)
case('Q27', 'tập 7 chính thức: chênh +0,04 trong ±SE → SÁT NGƯỠNG; không có PLAN tập sau → TRƯỢT', [] if r['ok'] else r['loi'], True)
r = QB.agg27(S7, fx['replies'], plan_sau=os.path.join(F7, 'plan-ep08-f115e8b.md'))   # 1.9.0: bản đóng băng (main sau tập 8 đã có mục)
case('Q27', 'tập 7 chính thức với PLAN tập 8 lúc khoá 1.8.1 (f115e8b, chưa có mục "Cải thiện hình") → TRƯỢT', [] if r['ok'] else r['loi'], True)
r = QB.agg27(S7, fx['replies'], plan_sau=PLAN_OK)
case('Q27', 'tập 7 chính thức + PLAN tập sau có mục "Cải thiện hình" → ĐẠT, ghi SÁT NGƯỠNG', [] if r['ok'] and r['sat'] and r['sat_nguong'] else ['sai'], False)
case('Q27', 'PLAN tập sau có tiêu đề "Cải thiện hình" nhưng mục rỗng → TRƯỢT', [] if QB.agg27(S7, fx['replies'], plan_sau=PLAN_EMPTY)['ok'] else ['trượt'], True)
case('Q27', 'PLAN tập sau không có mục "Cải thiện hình" → TRƯỢT', [] if QB.agg27(S7, fx['replies'], plan_sau=PLAN_NONE)['ok'] else ['trượt'], True)
up = copy.deepcopy(fx['replies'])
for x in up.values():
    for k, v in x['scores'].items():
        if S7[k] == 'new': x['scores'][k] = {c: min(10, s_ + 1) for c, s_ in v.items()}
r = QB.agg27(S7, up)
case('Q27', f"tập 7 nếu mọi khung tập mới +1: chênh > SE → ĐẠT rõ, không cần PLAN ({r['val'][:44]}…)", [] if r['ok'] and not r['sat'] else ['sai'], False)
fx = json.load(open(os.path.join(F7, 'q27-nhap-lan-04b.json'))); r = QB.agg27(QB.sets_from_seed(fx['seed']), fx['replies'], plan_sau=PLAN_OK)
case('Q27', f"tập 7 nháp 4b (chênh −0,10, trong SE): luật mới ĐẠT sát ngưỡng ({r['val'][:46]}…)", [] if r['ok'] and r['sat'] else ['sai'], False)
fx = json.load(open(os.path.join(F6, 'q27b-v2.json'))); r = QB.agg27(fx['sets'], fx['replies'], plan_sau=PLAN_OK)
case('Q27', 'tập 6 v2 (30 + 30, chênh −0,15) + PLAN có mục: ĐẠT sát ngưỡng', [] if r['ok'] and r['sat'] else ['sai'], False)
fx = json.load(open(os.path.join(F6, 'q27b-v1.json'))); r = QB.agg27(fx['sets'], fx['replies'], plan_sau=PLAN_OK)
case('Q27', 'tập 6 v1 (chênh −0,58 < −SE) → TRƯỢT dù PLAN có mục', [] if r['ok'] else r['loi'], True)
fx = json.load(open(os.path.join(F7, 'q27-nhap-lan-04-khong-hop-le.json'))); r = QB.agg27(QB.sets_from_seed(fx['seed']), fx['replies'], plan_sau=PLAN_OK)
case('Q27', 'tập 7 nháp lần 4: R1 thiếu F59, F60 → bộ chấm không hợp lệ', r['loi'] if not r['ok'] else [], True)
case('Q27', 'bản nháp không chấm: bản xem 1280×720 tập 6 v2 bị nhận là nháp', QB.draft27(V2v), True)
case('Q27', 'đối chứng tập 1 = master m23 1920×1080 (SHA M2-3-MASTER-SHORTS.md), một tệp', [] if [h for _, h, _ in QB.REF27] == ['9c3825387345ec0af6c035ec3f94809644ca7767d1ecbafcaed4710480113942'] and QB.SIZE27 == (1920, 1080) else ['sai'], False)

# ---- Q31: dấu vân lời/cấu trúc, đếm vòng nháp → bản cuối, sổ vòng ----
dv = QB.dau_van(TL7); FIN, DRAFT = [1920, 1080], [960, 540]
TLb = copy.deepcopy(TL7)
for sg in TLb['segments']:
    for sh in sg['shots']:
        sh['t1'] = sh['t1'] + 0.2; (sh.get('p') or {}).pop('cam', None)
TLb['heroes']['tower_code']['opt'] = {'exposure': 1.4}
case('Q31', 'dấu vân: sửa thời điểm, máy quay, ánh sáng cảnh đinh (lượt nội thất) → không đổi', [] if QB.dau_van(TLb) == dv else ['đổi'], False)
TLb = copy.deepcopy(TL7); sg = TLb['segments'][13]; sg['shots'][1]['p']['hero'] = 'tower_floor'
case('Q31', 'dấu vân: đổi cảnh đinh một shot (đoạn 13) → cấu trúc khác', [] if QB.dau_van(TLb)['cau_truc'] == dv['cau_truc'] else ['khác'], True)
TLb = copy.deepcopy(TL7); TLb['segments'][5]['shots'].pop(1)
case('Q31', 'dấu vân: bỏ một shot ảnh tư liệu → cấu trúc khác', [] if QB.dau_van(TLb)['cau_truc'] == dv['cau_truc'] else ['khác'], True)
alf = os.path.join(tmpp, 'll-ep07-05.align.json'); al = json.load(open(os.path.join(ROOT, TL7['segments'][5]['vo_file'].replace('.mp3', '.align.json'))))
al['characters'] = list(''.join(al['characters']).replace('second', 'other', 1)); json.dump(al, open(alf, 'w'))
TLb = copy.deepcopy(TL7); TLb['segments'][5]['vo_file'] = alf.replace('.align.json', '.mp3')
case('Q31', 'dấu vân: đổi một chữ lời đoạn 05 → lời khác', [] if QB.dau_van(TLb)['loi'] == dv['loi'] else ['khác'], True)
ch = lambda n, size, d: [dict(size=size, dau_van=d) for _ in range(n)]
dvB = dict(dv, cau_truc='0' * 64); dvL = dict(dv, loi='1' * 64)
v, nt = QB.vong31(ch(4, DRAFT, dv), dict(size=FIN, dau_van=dv))
case('Q31', f'4 vòng nháp + bản cuối cùng lời, cùng cấu trúc → vòng 5 ({nt[0]})', [] if v == 5 else [v], False)
v, nt = QB.vong31(ch(4, DRAFT, dv), dict(size=FIN, dau_van=dvB))
case('Q31', f'bản cuối đổi cấu trúc → đếm lại vòng 1 ({nt[0]})', [] if v == 1 else [v], False)
v, _ = QB.vong31(ch(4, DRAFT, dv), dict(size=FIN, dau_van=dvL))
case('Q31', 'bản cuối đổi lời → đếm lại vòng 1', [] if v == 1 else [v], False)
v, _ = QB.vong31([{}, {}, {}, {}], dict(size=FIN, dau_van=dv))
case('Q31', 'sổ nháp bản luật cũ (không dấu vân, như tập 7) → bản cuối vòng 1', [] if v == 1 else [v], False)
v, _ = QB.vong31(ch(2, DRAFT, dvB) + ch(2, DRAFT, dv), dict(size=FIN, dau_van=dv))
case('Q31', 'nháp đổi cấu trúc giữa các vòng nháp vẫn đếm tiếp; so với NHÁP CUỐI đã chấm → vòng 5', [] if v == 5 else [v], False)
v, _ = QB.vong31(ch(3, DRAFT, dv) + ch(1, FIN, dv), dict(size=FIN, dau_van=dvB))
case('Q31', 'bản cuối → bản cuối (dựng lại sau vòng bản cuối): đếm tiếp', [] if v == 5 else [v], False)
v, _ = QB.vong31(ch(2, DRAFT, dv) + ch(1, FIN, dvB) + ch(1, FIN, dv), dict(size=FIN, dau_van=dv))
case('Q31', 'nháp → bản cuối đổi (đếm lại 1) → bản cuối vòng 2 → vòng 3', [] if v == 3 else [v], False)
f4 = json.load(open(os.path.join(F7, 'q31-vong-05.json'))); cuts7, _ = QB.plan31(TL7)
r = QB.agg31(cuts7, f4['replies'], vong=5, giai_trinh=f4['giai_trinh'])
case('Q31', f"tập 7 vòng 5 thật (sổ nháp chuyển hợp lệ): {r['val']}", r['loi'], False)
r = QB.agg31(cuts7, f4['replies'], vong=1, giai_trinh=f4['giai_trinh'])
case('Q31', 'tập 7 bản cuối nếu đếm lại vòng 1: T05, T09, T15 (2/3) chặn', r['loi'], True)
R[-1] = R[-1][:3] + (R[-1][3] and len(r['loi']) == 3,) + R[-1][4:]
hd = tempfile.mkdtemp(); out = os.path.join(hd, 'q31'); hh = os.path.join(hd, 'q31-lich-su')
for n_ in (1, 2):
    os.makedirs(os.path.join(hh, f'vong-{n_:02d}')); json.dump(dict(vong=n_), open(os.path.join(hh, f'vong-{n_:02d}', 'manifest.json'), 'w'))
man = dict(lich_su=QB._ledger(out))
case('Q31', 'sổ vòng nguyên vẹn', QB.ledger_errors(out, man), False)
json.dump(dict(vong=9), open(os.path.join(hh, 'vong-02', 'manifest.json'), 'w'))
case('Q31', 'sổ vòng: manifest vòng 2 bị sửa', QB.ledger_errors(out, man), True)
import shutil  # noqa: E402
shutil.rmtree(hh)
case('Q31', 'sổ vòng: xoá q31-lich-su/', QB.ledger_errors(out, man), True)
dn = os.path.join(tempfile.mkdtemp(), 'q31'); dh = dn + '-lich-su'
for n_ in (1, 2):
    os.makedirs(os.path.join(dh, f'vong-{n_:02d}')); json.dump(dict(vong=n_, size=DRAFT), open(os.path.join(dh, f'vong-{n_:02d}', 'manifest.json'), 'w'))
os.makedirs(dn); json.dump(dict(vong=3, size=DRAFT), open(os.path.join(dn, 'manifest.json'), 'w'))
fo = os.path.join(tempfile.mkdtemp(), 'q31'); QB._import_nhap(fo, dn); QB._import_nhap(fo, dn)
got = sorted(os.listdir(fo + '-lich-su'))
case('Q31', f'--tu-nhap: chép 3 vòng nháp sang sổ bản cuối ({", ".join(got)}), chạy lại không chép trùng, nguồn còn nguyên',
     [] if got == ['vong-01', 'vong-02', 'vong-03'] and os.path.isdir(dh) and os.path.exists(os.path.join(dn, 'manifest.json'))
     and [json.load(open(os.path.join(fo + '-lich-su', g, 'manifest.json')))['vong'] for g in got] == [1, 2, 3] else ['sai'], False)

# ---- Q26b đa dạng bối cảnh ----
r7 = QS.q26b(TL7)
case('Q26b', f"tập 7 bản cuối: {r7['val']}", r7['loi'], True)
R[-1] = R[-1][:3] + (R[-1][3] and len(r7['loi']) == 3 and r7['loi'][0].startswith('ep07/tower chiếm 29.1 %') and 'ep07/tower liên tục 139.1 s (5:28.8–7:59.8' in r7['loi'][1],) + R[-1][4:]
case('Q26b', 'Ca 5 — tập 7: phòng tính toán 0:51–2:56 có ảnh tư liệu, isotype chen giữa → một quãng 104,3 s (trừ 20,7 s trung tính) > 90 s',
     [x for x in r7['loi'] if x.startswith('ep07/pool liên tục 104.3 s (0:51.2–2:56.2, đã trừ 20.7 s')], True)
case('Q26b', 'tập 7: ep07/pool 25,0 % được nêu sát ngưỡng', [] if any(x.startswith('ep07/pool 25.0 %') for x in r7['sat_nguong']) else ['thiếu'], False)
TL6 = json.load(gzip.open(os.path.join(F6, 'timeline-v2.json.gz')))
r6 = QS.q26b(TL6)
case('Q26b', f"tập 6 v2: {r6['val']}", r6['loi'], False)
H7 = TL7['heroes']
case('Q26b', 'nhãn: mọi góc máy của một cảnh đinh là một bối cảnh (tower_in, tower_code, tower_floor)',
     [] if {next(iter(QS.label(dict(tpl='plate', p=dict(hero=k)), H7))) for k in ('tower_in', 'tower_code', 'tower_floor')} == {'ep07/tower'} else ['sai'], False)
case('Q26b', 'nhãn: diptych hai nửa khác cảnh mỗi nửa 1/2, cùng cảnh cả shot; thẻ số, ảnh tư liệu trung tính',
     [] if QS.label(dict(tpl='diptych', p=dict(left=dict(hero='pool_desk'), right=dict(hero='tower_code'))), H7) == {'ep07/pool': 0.5, 'ep07/tower': 0.5}
     and QS.label(dict(tpl='diptych', p=dict(left=dict(hero='tower_code'), right=dict(hero='tower_floor'))), H7) == {'ep07/tower': 1.0}
     and QS.label(dict(tpl='archive', p=dict(rid='x')), H7) == {} and QS.label(dict(tpl='quote', p={}), H7) == {} else ['sai'], False)
case('Q26b', 'tập 7 (1.8.1): thẻ trích dẫn 11,9 s ở 5:51 không dứt quãng văn phòng; quãng 5:28.8–7:59.8 = 139,1 s (trừ 11,9 s trung tính)',
     [] if r7['lien_tuc']['ep07/tower'] == [139.1, '5:28.8', '7:59.8', 11.9] else [r7['lien_tuc']['ep07/tower']], False)
TLb = copy.deepcopy(TL7)
for sg in TLb['segments']:
    for sh in sg['shots']:
        if sh['tpl'] == 'quote': sh['tpl'], sh['p'] = 'plate', dict(hero='tower_code')
r = QS.q26b(TLb)
case('Q26b', f"tập 7 (1.8.1) nếu thay thẻ trích dẫn bằng cảnh văn phòng cùng thời lượng: quãng = cả 150,9 s ({r['lien_tuc']['ep07/tower']})",
     [] if r['lien_tuc']['ep07/tower'][:3] == [150.9, '5:28.8', '7:59.8'] else ['sai'], False)


def syn(*shots):
    """timeline tổng hợp một đoạn: shots = (mẫu, cảnh đinh hoặc (trái, phải) cho diptych, giây)"""
    t, out = 0.0, []
    for tpl, h, d in shots:
        p = dict(hero=h) if tpl == 'plate' else dict(left=dict(hero=h[0]), right=dict(hero=h[1])) if tpl == 'diptych' else {}
        out.append(dict(tpl=tpl, t0=t, t1=t + d, p=p)); t += d
    return dict(tong_s=t, heroes={k: dict(hero=k.upper()) for k in 'abc'}, segments=[dict(id='00', t0=0.0, t1=t, shots=out)])


def lt(TL, x='A'): return QS.q26b(TL)['lien_tuc'][x][:1] + [len(QS.runs(QS.shots(TL), x))]


r = lt(syn(('plate', 'a', 50), ('quote', None, 12), ('plate', 'a', 50)))
case('Q26b', f'Ca 1 — thẻ trích dẫn 12 s chen giữa hai đoạn cùng bối cảnh: một quãng, 100 s (không tính 12 s thẻ) → {r}', [] if r == [100.0, 1] else ['sai'], False)
r = lt(syn(('plate', 'a', 50), ('plate', 'b', 5), ('plate', 'a', 50)))
case('Q26b', f'Ca 2 — bối cảnh khác 5 s chen giữa: vẫn liền, 105 s → {r}', [] if r == [105.0, 1] else ['sai'], False)
r = lt(syn(('plate', 'a', 50), ('plate', 'b', 8), ('plate', 'a', 50)))
case('Q26b', f'Ca 3 — bối cảnh khác 8 s chen giữa: dứt quãng (2 quãng, dài nhất 50 s) → {r}', [] if r == [50.0, 2] else ['sai'], False)
r = lt(syn(('plate', 'a', 50), ('plate', 'b', 4), ('plate', 'c', 4), ('plate', 'a', 50)))
case('Q26b', f'Ca 4 — hai bối cảnh khác 4 s + 4 s (cộng dồn 8 s): dứt quãng → {r}', [] if r == [50.0, 2] else ['sai'], False)
r = lt(syn(('plate', 'a', 50), ('plate', 'b', 4), ('quote', None, 6), ('plate', 'c', 3.9), ('plate', 'a', 45)))
case('Q26b', f'thẻ trung tính không cộng vào bộ đếm: khác 4 s + thẻ 6 s + khác 3,9 s → vẫn liền, 102,9 s → {r}', [] if r == [102.9, 1] else ['sai'], False)
r = lt(syn(('plate', 'a', 50), ('plate', 'b', 5), ('diptych', ('a', 'b'), 2), ('plate', 'b', 5), ('plate', 'a', 40)))
case('Q26b', f'diptych có X ở một nửa đặt bộ đếm về 0: khác 5 s + diptych + khác 5 s → vẫn liền, 102 s → {r}', [] if r == [102.0, 1] else ['sai'], False)
case('Q26b', 'quãng 100 s qua thẻ 12 s bị bắt (> 90 s)', QS.q26b(syn(('plate', 'a', 50), ('quote', None, 12), ('plate', 'a', 50), ('plate', 'b', 150), ('plate', 'c', 150)))['loi'], True)
half = TL6['tong_s'] / 2; TLb = copy.deepcopy(TL6)
for sg in TLb['segments']:
    for sh in sg['shots']:
        if sg['t0'] + sh['t1'] > half: sh['tpl'], sh['p'] = ('plate', dict(hero='wall_push')) if sh['tpl'] in ('plate', 'diptych') else ('quote', {})
r = QS.q26b(TLb)
case('Q26b', f"tập 6 v2 nếu nửa sau chỉ còn tường bản nháp: {r['val']}", r['loi'], True)
for sg in TLb['segments']:
    if sg['t0'] > half + 30:
        sg['shots'][0]['tpl'], sg['shots'][0]['p'] = 'plate', dict(hero='lino_row'); sg['shots'][0]['t1'] = sg['shots'][0]['t0'] + 1.5
        sg['shots'][1]['tpl'], sg['shots'][1]['p'] = 'plate', dict(hero='shop_end'); sg['shots'][1]['t1'] = sg['shots'][1]['t0'] + 1.5; break
r = QS.q26b(TLb)
case('Q26b', 'chớp 2 bối cảnh 1,5 s ở nửa sau để đủ số: không tính (< 3 s mỗi bối cảnh)', [x for x in r['loi'] if 'nửa sau' in x], True)
TLb = copy.deepcopy(TL6); sgs = TLb['segments'][6:9]
for sg in sgs:
    for sh in sg['shots']: sh['tpl'], sh['p'] = 'plate', dict(hero='wall_push')
r = QS.q26b(TLb)
case('Q26b', f"tập 6 v2 nếu cả đoạn 06–08 ({sgs[-1]['t1'] - sgs[0]['t0']:.0f} s) dùng tường bản nháp: liên tục > 90 s",
     [x for x in r['loi'] if 'liên tục' in x], True)

# ======================= 1.9.0 (K, 11/10/2026): Q28f bộ chuyển chữ→số, Q27 chấm theo manifest, người chấm qua Claude API =======================
# ---- Q28f: khiếu nại P 09/10 (tập 8 đoạn 06, 13). Hai phía (lời khoá, ASR) dùng CÙNG nums_of; so theo giá trị, chặt ----
AS = json.load(open(os.path.join(FX, 'asr-k190.json')))   # văn bản ASR thật (faster-whisper small.en, beam 5) của K, 11/10/2026
for k in ('ep08/06', 'ep08/13'):
    case('Q28f', f'tập 8 đoạn {k[-2:]}: lời khoá vs ASR thật của K → ĐẠT', QA.asr_miss(AS['tx'][k]['vo'], AS['tx'][k]['asr']), False)
V06, V13 = AS['tx']['ep08/06']['vo'], AS['tx']['ep08/13']['vo']
A06, A13 = AS['tx']['ep08/06']['asr'], AS['tx']['ep08/13']['asr']
case('Q28f', 'đoạn 06: ASR thật viết "some $20 million" = lời "some twenty million dollars" (1.8.1: "thiếu 20000000.0")', ([] if '$20 million' in A06 else ['ASR khác']) + QA.asr_miss(V06, A06), False)
case('Q28f', 'đoạn 13: ASR thật viết "3.5%" = lời "three and a half percent" (1.8.1: "thiếu 3.0")', ([] if '3.5%' in A13 else ['ASR khác']) + QA.asr_miss(V13, A13), False)
for vo, tx, nm in (('two million dollars', 'twenty million dollars', '"two million" ≠ "twenty million"'), ('twenty million dollars', 'two million dollars', '"twenty million" ≠ "two million"'),
                   ('three and a half percent', 'slower than the 3% projected', '"three and a half percent" ≠ "3%"'), ('about 3%', 'three and a half percent', '"3%" ≠ "three and a half percent"'),
                   ('some $20 million', 'some 2 million', '"$20 million" ≠ "2 million"')):
    case('Q28f', f'không nới: {nm} → TRƯỢT', QA.asr_miss(vo, tx), True)
for vo, tx, nm in (('In 1966, twelve years after', 'In nineteen sixty six twelve years after', 'năm đọc chữ + số liền sau: 1966 và 12, không ghép'),
                   ('In nineteen sixty-six, twelve years after', 'In 1966, 12 years after', 'lời viết năm bằng chữ, ASR viết số'),
                   ('on January seventh, 1954', 'on January 7th, 1954', 'ngày thứ tự sau tên tháng = 7'),
                   ('First, it counted the people.', 'First it counted the people.', '"First" đứng riêng không là số'),
                   ('two hundred sixty-two translators', '262 translators', '262'), ('about fifteen hundred more jobs', 'about 1,500 more jobs', '1500'),
                   ('seventy-four thousand jobs', '74,000 jobs', '74 000'), ('two and a half million', '2.5 million', '2,5 triệu')):
    case('Q28f', f'đọc đúng: {nm}', QA.asr_miss(vo, tx), False)
case('Q28f', 'bộ đọc cũ ghép "nineteen sixty six twelve" thành 97 (lỗi P báo); bộ mới: {12, 1966}', [] if QA.nums_of('nineteen sixty six twelve years') == {12.0, 1966.0} else [sorted(QA.nums_of('nineteen sixty six twelve years'))], False)
case('Q28f', 'ngày thứ tự ngoài tên tháng không đọc ("the seventh day")', [] if QA.nums_of('the seventh day') == set() else ['đọc'], False)
for ep_, exp in AS['ky_vong'].items():
    got = {k.split('/')[1]: QA.asr_miss(v['vo'], v['asr']) for k, v in AS['tx'].items() if k.startswith(ep_ + '/')}
    got = {k: v for k, v in got.items() if v}
    case('Q28f', f"{ep_}: ASR thật, bộ mới → {got or 'ĐẠT'} (bộ cũ 1.8.1: {AS['cu'][ep_] or 'ĐẠT'})", [] if got == exp else [got], False)

# ---- Q27: khiếu nại P 10/10 — chấm lại theo SHA master mới gán sai khung (in −0,11/+0,06 thay vì −0,31) ----
F8 = os.path.join(FX, 'ep08'); fx8 = json.load(open(os.path.join(F8, 'q27-chinh-thuc.json'))); M8 = fx8['manifest']; D22 = fx8['sha_sau']['d22d7d6e']
r_old = QB.agg27(QB.sets_from_seed(QB.seed_of([D22])), fx8['replies'])
case('Q27', f"tái hiện lỗi 1.8.1: gán khung theo SHA master phát hành d22d7d6e… → {r_old['val'].split(' (SE')[0]} (số sai P báo: −0,11)", [] if abs(r_old['chenh'] + 0.11) < 0.005 else [r_old['val']], False)
S8, b8, same8 = QB.q27_sets(M8, [D22]); r8 = QB.agg27(S8, fx8['replies'], b8)
case('Q27', f"1.9.0: cùng dữ liệu, gán theo hạt giống manifest → {r8['val'].split(' (SE')[0]} (= số chính thức −0,31)", [] if abs(r8['chenh'] + 0.31) < 0.005 and S8 == QB.sets_from_seed(M8['seed']) else [r8['val']], False)
case('Q27', 'master khác manifest: báo "bộ chấm thuộc bản khác" → TRƯỢT, chấm lại', [x for x in b8 if 'bộ chấm thuộc bản khác' in x] if not same8 and not r8['ok'] else [], True)
S8b, b8b, same8b = QB.q27_sets(M8, [M8['new'][0]['sha256']])
case('Q27', 'master đúng bản trong manifest: không lỗi, cùng phép gán', b8b + ([] if same8b and S8b == S8 else ['khác']), False)
Mt = copy.deepcopy(M8); Mt['seed'] = QB.seed_of([D22])
case('Q27', 'manifest bị sửa hạt giống (không khớp SHA ghi trong manifest) → lỗi', QB.q27_sets(Mt, [M8['new'][0]['sha256']])[1], True)

# ---- Hiệu chuẩn Claude API (K 11/10/2026): chấm lại bộ khung Q27 chính thức tập 7, 8 bằng API, 2 lần mỗi tập ----
CAL = {}
for e_, Fd, sub in (('07', F7, json.load(open(os.path.join(F7, 'q27-chinh-thuc.json')))['replies']), ('08', F8, fx8['replies'])):
    for k_ in (1, 2):
        c_ = json.load(open(os.path.join(Fd, f'q27-api-k190-lan{k_}.json'))); S_ = QB.sets_from_seed(c_['seed'])
        a_, s_ = QB.agg27(S_, c_['replies']), QB.agg27(S_, sub); CAL[(e_, k_)] = (a_['chenh'], s_['chenh'], c_)
        case('Q27', f"hiệu chuẩn API tập {e_} lần {k_}: {a_['val'].split(' (SE')[0]} · subagent {s_['chenh']:+.2f} · lệch {a_['chenh'] - s_['chenh']:+.2f} · ${c_['cham']['cost_usd']}",
             [] if c_['cham']['model'] == QB.MODEL and all(t['model_usage'] == [QB.MODEL] for v in c_['cham']['raters'].values() for t in v) else ['mô hình'], False)
se_api, _ = QB.se27([(QB.sets_from_seed(c_['seed']), c_['replies']) for _, _, c_ in CAL.values()])
case('Q27', f'SE đo trên 4 lần chấm API = {se_api:.3f} (subagent, 6 lần: 0,273; khoá: {QB.SE27})', [] if abs(se_api - 0.321) < 0.0015 else [f'{se_api:.4f}'], False)

# ---- Người chấm qua Claude API (judge.py): kiểm bằng `claude` giả, không gọi mạng ----
from checks.ll import judge as JG  # noqa: E402
case('API', f'mô hình ghim {JG.MODEL} (không để mặc định)', [] if JG.MODEL == 'claude-sonnet-5-5' and QB.MODEL == JG.MODEL else [QB.MODEL], False)
case('API', 'modelUsage có mô hình khác (haiku) → lỗi', JG.model_errors({JG.MODEL: {}, 'claude-haiku-5-5': {}}), True)
case('API', 'modelUsage rỗng → lỗi', JG.model_errors({}), True)
case('API', 'trả lời JSON trong rào ``` đọc được; chữ thường → không', [] if JG.parse_json('```json\n{"a": 1}\n```') == {'a': 1} and JG.parse_json('no json') is None else ['sai'], False)
_ok = os.environ.pop('CONSOLE_API_KEY', None)
try: JG._env('/tmp'); e_ = []
except JG.JudgeError as e: e_ = [str(e)]
case('API', 'thiếu CONSOLE_API_KEY → dừng (fail closed)', e_, True)
fake = tempfile.mkdtemp(); shutil.copy(os.path.join(FX, 'judge', 'fake_claude.py'), os.path.join(fake, 'claude')); os.chmod(os.path.join(fake, 'claude'), 0o755)
_path = os.environ['PATH']; os.environ['PATH'] = fake + os.pathsep + _path; os.environ['CONSOLE_API_KEY'] = 'sk-ant-SELFTEST-KHOA-GIA-0123456789'


def fake_set(mode, seed=None, ref=None):
    d = tempfile.mkdtemp(); img = {}
    for i in range(1, 61):
        f = os.path.join(d, f'F{i:02d}.jpg'); open(f, 'wb').write(b'x%d' % i); img[f'F{i:02d}'] = QB.sha_file(f)
    new_ = [dict(sha256=h) for _, h, _ in QB.MOC27] if seed else M8['new']
    QB.render_prompts(d, 'Q27'); json.dump(dict(rule='Q27', seed=seed or M8['seed'], new=new_, ref=ref, images=img), open(os.path.join(d, 'manifest.json'), 'w'))
    os.environ['FAKE_MODE'] = mode
    try: QB.blind_run(d, 'Q27'); code = 0
    except SystemExit as e: code = e.code
    return d, code, QB._replies(d, 'Q27')


try:
    d, code, (Rr, bad) = fake_set('ok')
    case('API', f"chấm giả đủ 3 người: R1–R3.json + `cham` trong manifest (mô hình, chi phí ${QB._man(d)['cham']['cost_usd']})", bad + ([] if code == 0 and len(Rr) == 3 and QB._man(d)['cham']['cost_usd'] > 0 else ['thiếu']), False)
    try: QB.blind_run(d, 'Q27'); e_ = []
    except SystemExit as e: e_ = [str(e)]
    case('API', 'chấm lại cùng bộ (đã có R*.json) → từ chối', e_, True)
    d, code, (Rr, bad) = fake_set('credit')
    case('API', 'hết credit → TRƯỢT có lý do, không có R*.json', [x for x in bad if 'Credit balance' in x] if code == 2 and not Rr else [], True)
    d, code, (Rr, bad) = fake_set('model')
    case('API', 'chạy mô hình khác MODEL → không nhận trả lời', bad if not Rr else [], True)
    d, code, (Rr, bad) = fake_set('partial')
    case('API', 'người chấm không đọc đủ 60 ảnh → không nhận trả lời', [x for x in bad if 'không đọc đủ' in x], True)
    d, code, (Rr, bad) = fake_set('fence')
    case('API', 'JSON trong rào ``` vẫn nhận', bad, False)
    # ---- 1.9.1: mốc tập 8 (chủ dự án 11/10: phương án A + đặt lại mốc) ----
    REFS = [dict(video=os.path.basename(v), sha256=h) for v, h, _ in QB.REF27]
    dm, code, _ = fake_set('ok', seed=QB.seed_of([h for _, h, _ in QB.MOC27]), ref=REFS); m_ = QB.moc27(dm, video=False)
    case('Q27', f"mốc tập 8 hợp lệ (bộ giả, 3 người): {m_['val']}", m_['loi'] + ([] if m_['chenh'] == 0 else ['chênh']), False)
    case('Q27', 'thiếu bộ mốc tập 8 → lỗi', QB.moc27(os.path.join(tempfile.mkdtemp(), 'q27-moc'), video=False)['loi'], True)
    dx, code, _ = fake_set('ok', ref=REFS)
    case('Q27', 'bộ mốc dựng từ video khác tập 8 bản phát hành → lỗi "bộ chấm thuộc bản khác"', [e for e in QB.moc27(dx, video=False)['loi'] if 'bộ chấm thuộc bản khác' in e], True)
    c8 = json.load(open(os.path.join(F8, 'q27-api-k190-lan1.json'))); r9 = QB.agg27(QB.sets_from_seed(c8['seed']), c8['replies'], plan_sau=PLAN_OK)
    rm = QB.them_moc(r9, m_)
    case('Q27', f"kèm mốc: ngưỡng vẫn trên tập mới − tập 1 (ĐẠT, sát ngưỡng) · {rm['val'].split(' (R1')[0]}",
         [] if rm['ok'] == r9['ok'] is True and abs(rm['hieu_moc'] - (r9['chenh'] - 0)) < 1e-9 and 'tập mới − tập 8' in rm['val'] else [rm['val']], False)
    case('Q27', 'kèm mốc: bộ mốc lỗi → TRƯỢT dù chênh chính đạt', [] if QB.them_moc(r9, dict(chenh=None, val='không có', loi=['thiếu']))['ok'] else ['trượt'], True)
    case('Q27', f'mốc = tập 8 bản phát hành (release-ll-ep08-v1, d22d7d6e…)', [] if QB.MOC27[0][1] == D22 else [QB.MOC27[0][1]], False)
    d, code, (Rr, bad) = fake_set('twojson')
    case('API', 'trả hai khối JSON (tự sửa giữa chừng) cả 2 lần gọi → không nhận, TRƯỢT có lý do', [x for x in bad if 'không đọc được' in x] if not Rr else [], True)
    d, code, (Rr, bad) = fake_set('twojson1')
    tr = [len(x['tries']) for x in QB._man(d)['cham']['raters'].values()]
    case('API', f'trả lời không đọc được ở lần 1 → gọi lại 1 lần, ghi cả 2 lần (số lần mỗi người: {tr})', bad + ([] if tr == [2, 1, 1] and len(Rr) == 3 else ['sai']), False)
    d, code, (Rr, bad) = fake_set('leak')
    leak = [f for f in glob.glob(os.path.join(d, '**', '*'), recursive=True) if os.path.isfile(f) and os.environ['CONSOLE_API_KEY'] in open(f, errors='ignore').read()]
    case('API', 'khoá không bao giờ ghi ra tệp (trả lời, bản chép, manifest)', leak, False)
    Rs = {r: dict(x, model='sonnet', backend=None) for r, x in Rr.items()}
    for r, x in Rs.items(): json.dump(x, open(os.path.join(d, f'{r}.json'), 'w'))
    case('API', 'trả lời kiểu subagent cũ (model "sonnet", không qua API) → không nhận', QB._replies(d, 'Q27')[1], True)
    d2 = tempfile.mkdtemp(); [shutil.copy(os.path.join(F8, 'q27-chinh-thuc.json'), d2)]
    for r, x in fx8['replies'].items(): json.dump(x, open(os.path.join(d2, f'{r}.json'), 'w'))
    json.dump(M8, open(os.path.join(d2, 'manifest.json'), 'w'))
    case('API', 'bộ chấm subagent tập 8 (không có bản ghi `cham`) → TRƯỢT "chưa chấm qua Claude API"', [x for x in QB._replies(d2, 'Q27')[1] if 'chưa chấm qua Claude API' in x], True)
finally:
    os.environ['PATH'] = _path; os.environ.pop('FAKE_MODE', None); os.environ.pop('CONSOLE_API_KEY', None)
    if _ok: os.environ['CONSOLE_API_KEY'] = _ok

# ======================= 1.10.0 (K, 12/10/2026): Q32 footage/ảnh nguồn ngoài (chủ dự án 12/10: cho phép, ưu tiên miễn phí; LL + kênh 2) =======================
# Dữ liệu: timeline bản cuối tập 7 (fixtures/ep07) với một số shot đổi thành footage giả; file clip là byte ngẫu nhiên trong thư mục tạm (không commit).
from checks.ll import q_footage as QF  # noqa: E402
import subprocess  # noqa: E402
os.environ['Q32_CACHE_DIR'] = tempfile.mkdtemp()
TL7 = json.load(gzip.open(os.path.join(F7, 'timeline-final.json.gz'))); E7 = dict(id='ll-ep07', out='/var/tmp/cine-out/ll-ep07-khong-co')
FTD = tempfile.mkdtemp()
DESC = ('Sources: BLS, NASA History.\nFootage: Library of Congress; Wikimedia Commons; Pexels; Pixabay.\n'
        'Photo: "Langley computers" by Jane Doe, CC BY-SA 4.0, via Wikimedia Commons.\n')
CL = {  # clip: (đoạn, shot, nguồn trang, URL tải, giấy phép, ghi công, người, logo, bối cảnh)
    'LOC-01': ('00', 1, 'https://www.loc.gov/pictures/item/2017878800/', 'https://tile.loc.gov/storage-services/service/pnp/fsa/8b17000/8b17067r.jpg',
               'PD — LoC: No known restrictions on publication', '', 'khong', 'khong', 'air_hook'),
    'WM-01': ('00', 3, 'https://commons.wikimedia.org/wiki/File:Langley_computers.jpg', 'https://upload.wikimedia.org/wikipedia/commons/a/ab/Langley_computers.jpg',
              'CC BY-SA 4.0 https://creativecommons.org/licenses/by-sa/4.0/', 'Photo: "Langley computers" by Jane Doe, CC BY-SA 4.0, via Wikimedia Commons.', 'khong', 'khong', 'ft/langley-room'),
    'PX-01': ('08', 0, 'https://www.pexels.com/video/office-workers-123456/', 'https://videos.pexels.com/video-files/123456/123456-hd_1920_1080_25fps.mp4',
              'Pexels License https://www.pexels.com/license/', '', 'co: hai nhân viên văn phòng, mặt rõ', 'khong', 'ft/modern-office'),
    'PB-01': ('10', 1, 'https://pixabay.com/videos/server-room-98765/', 'https://cdn.pixabay.com/video/2020/01/01/98765-large.mp4',
              'Pixabay Content License https://pixabay.com/service/license-summary/', '', 'khong', 'co: nhãn tủ máy, đã làm mờ', 'ft/server-room'),
}


def q32_set(over=None, rows=None, desc=DESC, edit=None):
    """dựng một tập giả: thư mục tập (sổ + mô tả), timeline có footage → (E, TL, ep_dir)"""
    d = tempfile.mkdtemp(); TLx = copy.deepcopy(TL7); RW = []
    os.makedirs(os.path.join(d, 'phat-hanh')); open(os.path.join(d, 'phat-hanh', 'll-ep07-youtube-description.txt'), 'w').write(desc or '') if desc is not None else None
    for c, (sid, j, ut, ud, lic, at, per, logo, st) in CL.items():
        f = os.path.join(FTD, c + ('.jpg' if c.startswith(('LOC', 'WM')) else '.mp4'))
        if not os.path.exists(f): open(f, 'wb').write(os.urandom(4096))
        sg = next(s for s in TLx['segments'] if s['id'] == sid); sh = sg['shots'][j]
        sh['tpl'], sh['p'] = 'footage', dict(clip=c, file=f, setting=st)
        a, b = sg['t0'] + sh['t0'], sg['t0'] + sh['t1']
        RW.append(dict(clip_id=c, url_trang=ut, url_tai=ud, ngay_tai_utc='2026-10-12T08:32:00Z', giay_phep=lic, yeu_cau_ghi_cong=at,
                       sha256=QB.sha_file(f), timecode_dung=f'{QF.mmss(a)}-{QF.mmss(b)}', nguoi_nhan_dien=per, logo=logo))
    if edit: edit(TLx, RW)
    with open(os.path.join(d, QF.SO), 'w', newline='', encoding='utf-8') as fo:
        import csv as _csv
        w_ = _csv.DictWriter(fo, QF.COLS); w_.writeheader(); [w_.writerow(r) for r in (rows(RW) if rows else RW)]
    return E7, TLx, d


def q32m(k, **kw):
    E_, T_, d_ = q32_set(**kw); r = QF.q32(E_, T_, d_, scan=False); return r['muc'][k], r


def row_(c, **kv):
    def f(TLx, RW): next(r for r in RW if r['clip_id'] == c).update(kv)
    return f


r0 = QF.q32(*q32_set(), scan=False)
case('Q32', f"tập giả 4 clip LoC/Wikimedia/Pexels/Pixabay đủ sổ, SHA, ghi công: ĐẠT · {r0['val']}", r0['loi'], False)
# (a) sổ ↔ EDL ↔ SHA
def _drop(TLx, RW): RW[:] = [r for r in RW if r['clip_id'] != 'PX-01']
case('Q32a', 'đoạn footage PX-01 không có dòng sổ', q32m('a', edit=_drop)[0], True)
case('Q32a', 'SHA-256 file đã dùng ≠ sổ (file bị thay sau khi ghi sổ)', q32m('a', edit=row_('LOC-01', sha256='0' * 64))[0], True)
def _nofile(TLx, RW): next(sh for s in TLx['segments'] for sh in s['shots'] if (sh.get('p') or {}).get('clip') == 'WM-01')['p']['file'] = '/var/tmp/khong-co/WM-01.jpg'
case('Q32a', 'không thấy file đã dùng → không kiểm được SHA', q32m('a', edit=_nofile)[0], True)
case('Q32a', 'timecode_dung lệch EDL 1 s', q32m('a', edit=row_('LOC-01', timecode_dung='0:08.78-0:12.12'))[0], True)
case('Q32a', 'giấy phép CC BY-NC 4.0 (NC bị cấm)', q32m('a', edit=row_('WM-01', giay_phep='CC BY-NC 4.0'))[0], True)
case('Q32a', 'nguồn ngoài danh sách (shutterstock) → cần chủ dự án duyệt', q32m('a', edit=row_('PX-01', url_trang='https://www.shutterstock.com/video/clip-1'))[0], True)
case('Q32a', 'Wikimedia trỏ trang danh mục, không phải trang File: (không kiểm được giấy phép từng file)', q32m('a', edit=row_('WM-01', url_trang='https://commons.wikimedia.org/wiki/Category:Langley'))[0], True)
case('Q32a', 'giấy phép không hợp nguồn (Pixabay License cho clip Pexels)', q32m('a', edit=row_('PX-01', giay_phep='Pixabay License'))[0], True)
case('Q32a', 'ngày tải không phải ISO 8601 UTC (12/10/2026)', q32m('a', edit=row_('LOC-01', ngay_tai_utc='12/10/2026'))[0], True)
case('Q32a', 'timecode nhiều đoạn "a-b;c-d" và SMPTE hh:mm:ss:ff đọc đúng', [] if QF.parse_tc('00:00:08:12') == 8.5 and QF.parse_tc('1:02.50') == 62.5 else ['sai'], False)
# (b) trần 40 % / 8 s
def _long(TLx, RW):
    sg = next(s for s in TLx['segments'] if s['id'] == '00'); sg['shots'][2]['tpl'], sg['shots'][2]['p'] = 'footage', dict(sg['shots'][1]['p'])
    r = next(r for r in RW if r['clip_id'] == 'LOC-01'); r['timecode_dung'] = f"{QF.mmss(sg['t0'] + sg['shots'][1]['t0'])}-{QF.mmss(sg['t0'] + sg['shots'][2]['t1'])}"
m_, r_ = q32m('b', edit=_long)
case('Q32b', 'LOC-01 hai shot kề nhau 3,34 + 3,59 = 6,93 s: một lần liên tục, ĐẠT (≤ 8 s)', m_ + r_['muc']['a'], False)
def _long2(TLx, RW):
    _long(TLx, RW); sg = next(s for s in TLx['segments'] if s['id'] == '00'); sg['shots'][3]['tpl'], sg['shots'][3]['p'] = 'footage', dict(sg['shots'][1]['p'])
    next(r for r in RW if r['clip_id'] == 'LOC-01')['timecode_dung'] = f"{QF.mmss(sg['t0'] + sg['shots'][1]['t0'])}-{QF.mmss(sg['t0'] + sg['shots'][3]['t1'])}"
    sg['shots'][3]['p'] = dict(sg['shots'][1]['p']); RW[:] = [r for r in RW if r['clip_id'] != 'WM-01']
case('Q32b', 'LOC-01 ba shot kề nhau = 11,62 s liên tục > 8 s', q32m('b', edit=_long2)[0], True)
def _many(TLx, RW):   # mọi plate cắt thành mảnh ≤ 7 s, mỗi mảnh một clip riêng (không clip nào > 8 s): chỉ trần 40 % bị chạm
    k = 0
    for s in TLx['segments']:
        out = []
        for sh in s['shots']:
            if sh['tpl'] != 'plate': out.append(sh); continue
            n = int((sh['t1'] - sh['t0']) // 7) + 1; dt = (sh['t1'] - sh['t0']) / n
            for i in range(n):
                c = f'LOC-M{k:03d}'; k += 1; f = os.path.join(FTD, c + '.jpg')
                if not os.path.exists(f): open(f, 'wb').write(os.urandom(2048))
                a, b = sh['t0'] + i * dt, sh['t0'] + (i + 1) * dt
                out.append(dict(tpl='footage', t0=a, t1=b, p=dict(clip=c, file=f, setting='ft/x')))
                RW.append(dict(RW[0], clip_id=c, sha256=QB.sha_file(f), timecode_dung=f"{QF.mmss(s['t0'] + a)}-{QF.mmss(s['t0'] + b)}"))
        s['shots'] = out
m_, r_ = q32m('b', edit=_many)
case('Q32b', f"mọi plate cắt thành clip ≤ 7 s (clip riêng) + tư liệu: {r_['val'].split(' · ')[3]} > 40 %", m_ if not r_['muc']['a'] else r_['muc']['a'], True)
def _eight(TLx, RW):
    sg = next(s for s in TLx['segments'] if s['id'] == '00'); sh = sg['shots'][1]; sh['t1'] = sh['t0'] + 7.9; sg['shots'][2]['t0'] = sh['t1']
    next(r for r in RW if r['clip_id'] == 'LOC-01')['timecode_dung'] = f"{QF.mmss(sg['t0'] + sh['t0'])}-{QF.mmss(sg['t0'] + sh['t1'])}"
m_, r_ = q32m('b', edit=_eight)
case('Q32b', f"clip 7,9 s: ĐẠT nhưng nêu tên sát ngưỡng ({'; '.join(r_['sat_nguong'])})", m_ + ([] if any('LOC-01' in x for x in r_['sat_nguong']) else ['không nêu sát ngưỡng']), False)
# (c) ghi công CC BY / CC BY-SA
case('Q32c', 'CC BY-SA: mô tả có nguyên văn câu ghi công (khác xuống dòng/hoa thường vẫn nhận)', q32m('c', desc=DESC.replace('Photo: "Langley', 'photo:\n  "Langley'))[0], False)
case('Q32c', 'CC BY-SA: mô tả thiếu câu ghi công', q32m('c', desc='Sources: BLS.\n')[0], True)
case('Q32c', 'CC BY-SA: yeu_cau_ghi_cong trống', q32m('c', edit=row_('WM-01', yeu_cau_ghi_cong=''))[0], True)
case('Q32c', 'CC BY-SA: không có tệp mô tả YouTube', q32m('c', desc=None)[0], True)
# (d) logo / người nhận diện được trong ngữ cảnh xấu
def _cap(word):
    def f(TLx, RW): next(sh for s in TLx['segments'] for sh in s['shots'] if (sh.get('p') or {}).get('clip') == 'PX-01')['p']['cap'] = [{'s': f'The firm went {word} in 1931', 'at': 0.5}]
    return f
case('Q32d', 'Pexels người nhận diện được, lời và chữ trung tính', q32m('d')[0], False)
case('Q32d', 'Pexels người nhận diện được + chú thích "went bankrupt" (bad light)', q32m('d', edit=_cap('bankrupt'))[0], True)
def _blur(TLx, RW): _cap('bankrupt')(TLx, RW); row_('PX-01', nguoi_nhan_dien='co: đã làm mờ mặt')(TLx, RW)
case('Q32d', 'cùng chú thích nhưng mặt đã làm mờ (không còn nhận diện được)', q32m('d', edit=_blur)[0], False)
case('Q32d', 'Pixabay logo rõ nét (giấy phép cấm dùng thương mại)', q32m('d', edit=row_('PB-01', logo='co: logo hãng trên tủ máy, rõ'))[0], True)
case('Q32d', 'Pixabay logo đã làm mờ', q32m('d')[0], False)
def _negvo(TLx, RW):   # logo rõ nét (Pexels) đặt ở đoạn có lời thật chứa từ tiêu cực: tìm từ NEG thật trong lời tập 7
    FW = QA.flat_words(TLx); hit = next(((sid, t0) for sid, L in FW.items() for w, t0, *_ in L if QF.NEG.match(w)), None)
    assert hit, 'lời tập 7 không có từ NEG'
    sg = next(s for s in TLx['segments'] if s['id'] == hit[0]); sh = next(x for x in sg['shots'] if sg['t0'] + x['t0'] <= hit[1] < sg['t0'] + x['t1'])
    sh['tpl'], sh['p'] = 'footage', dict(clip='PX-02', file=os.path.join(FTD, 'PX-01.mp4'), setting='ft/y')
    RW.append(dict(next(r for r in RW if r['clip_id'] == 'PX-01'), clip_id='PX-02', nguoi_nhan_dien='khong', logo='co: biển hiệu công ty rõ',
                   timecode_dung=f"{QF.mmss(sg['t0'] + sh['t0'])}-{QF.mmss(sg['t0'] + sh['t1'])}"))
m_, r_ = q32m('d', edit=_negvo)
case('Q32d', f"logo rõ nét trong khung lời thật có từ tiêu cực ({'; '.join(m_)[:90]})", m_, True)
# (e) không commit media nguồn ngoài (repo git tạm)
def _repo(files):
    g = tempfile.mkdtemp(); subprocess.run(['git', 'init', '-q', g], check=True)
    for p_, b_ in files.items():
        os.makedirs(os.path.dirname(os.path.join(g, p_)) or g, exist_ok=True); open(os.path.join(g, p_), 'wb').write(b_)
    subprocess.run(['git', '-C', g, 'add', '-A'], check=True); return g
so_ = q32_set()[2]; so_rows = QF.load_so(os.path.join(so_, QF.SO))[0]; b_loc = open(os.path.join(FTD, 'LOC-01.jpg'), 'rb').read()
case('Q32e', 'repo chỉ có sổ CSV và mã: ĐẠT', QF.git_scan(_repo({'channel-k2/k2x-ep01/SOURCES-FOOTAGE.csv': open(os.path.join(so_, QF.SO), 'rb').read(), 'a.py': b'x=1\n'})), False)
case('Q32e', 'clip commit vào channel-k2/k2x-ep01/footage/PX-01.mp4', QF.git_scan(_repo({'channel-k2/k2x-ep01/footage/PX-01.mp4': b'\0' * 99})), True)
case('Q32e', 'clip LoC commit dưới tên khác (assets/k2/x.bin): bắt theo SHA của sổ', QF.git_scan(_repo({'assets/k2/x.bin': b_loc, 'channel-k2/k2x-ep01/SOURCES-FOOTAGE.csv': open(os.path.join(so_, QF.SO), 'rb').read()})), True)
case('Q32e', 'SHA sổ truyền trực tiếp (sổ chưa commit)', QF.git_scan(_repo({'reports/m3/ep09/still.jpg': b_loc}), [os.path.join(so_, QF.SO)]), True)
case('Q32e', 'repo cine-lab hiện tại (main): không có media footage nguồn ngoài', QF.git_scan(ROOT, [], {r['sha256'] for r in so_rows.values()}), False)
# (f) Q26b đếm footage là bối cảnh theo nội dung hình
def _noset(TLx, RW): next(sh for s in TLx['segments'] for sh in s['shots'] if (sh.get('p') or {}).get('clip') == 'PX-01')['p'].pop('setting')
case('Q32f', 'đoạn footage không khai p.setting', q32m('f', edit=_noset)[0], True)
_, Tf, _ = q32_set(); Lf = [QS.label(sh, Tf['heroes']) for s in Tf['segments'] for sh in s['shots'] if (sh.get('p') or {}).get('clip')]
case('Q32f', f"Q26b gán nhãn footage theo p.setting: {[list(x)[0] for x in Lf]}", [] if [list(x)[0] for x in Lf] == [Tf['heroes']['air_hook']['hero'], 'ft/langley-room', 'ft/modern-office', 'ft/server-room'] else [Lf], False)
def _other(TLx, RW): next(sh for s in TLx['segments'] for sh in s['shots'] if (sh.get('p') or {}).get('clip') == 'LOC-01')['p']['setting'] = 'ft/khac'
HA = Tf['heroes']['air_hook']['hero']; rf, ro = QS.q26b(Tf), QS.q26b(q32_set(edit=_other)[1]); d00 = TL7['segments'][0]['shots'][1]; w_ = 100 * (d00['t1'] - d00['t0']) / TL7['tong_s']
case('Q32f', f"LOC-01 (3,34 s) khai cùng nơi với cảnh đinh air_hook → cộng vào bối cảnh đó: {ro['ty_le'].get(HA)} % → {rf['ty_le'].get(HA)} % (+{w_:.2f} %)",
     [] if abs(rf['ty_le'][HA] - ro['ty_le'][HA] - w_) < 0.11 and 'ft/khac' in ro['ty_le'] and 'ft/khac' not in rf['ty_le'] else ['sai'], False)
def _sameset(TLx, RW):
    for s in TLx['segments']:
        for sh in s['shots']:
            if sh['tpl'] == 'plate': sh['tpl'], sh['p'] = 'footage', dict(clip='LOC-01', setting='ft/steel-mill')
case('Q32f', 'footage cùng nội dung "ft/steel-mill" phủ mọi plate → Q26b TRƯỢT (> 25 %, > 90 s)', QS.q26b(q32_set(edit=_sameset)[1])['loi'], True)
case('Q32f', 'tương thích: footage là cảnh toàn khung (Q16) và hình vật chất (Q29)', [] if 'footage' in q_rhythm.FULL and 'footage' in QA.PHYS else ['thiếu'], False)

w = max(len(r[1]) for r in R)
for rule, name, kind_, ok, got in R: print(f"{'ĐÚNG' if ok else 'SAI '}  {rule:<7} {kind_:<8} {name}" + ('' if ok else f'   → {got}'))
n_ok = sum(r[3] for r in R); print(f'\nselftest LL v3: {n_ok}/{len(R)} ca đúng kỳ vọng'); sys.exit(0 if n_ok == len(R) else 1)
