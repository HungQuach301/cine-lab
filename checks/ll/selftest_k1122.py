#!/opt/cine/bin/python
"""Tự kiểm biến thể kênh 2 bản 1.12.2 (phiên K, 17/10/2026; chủ dự án duyệt 17/10: NN2, NN3; khiếu nại Q14/Q15/Q17 14/10). Mỗi biến thể ≥ 1 ca
ĐẠT + ≥ 1 ca TRƯỢT. Dữ liệu thật:
  fixtures/k2c106-g2/        T1 bản phát hành (đặc tả + timeline dựng lại)
  fixtures/k1122/            T2 đặc tả HEAD (origin/k2c-t2 eff18b18, scene_id theo vùng) · timeline T2 v3.4 = fixtures/k112/t2-v34-timeline.json.gz ·
                             băm pHash L/ΔE đã đo: T2 (tờ khung nháp 540p), T1 + Steel (master phát hành, LFS)
Không gọi mạng, không gọi API, không cần master (băm đã lưu).

  /opt/cine/bin/python checks/ll/selftest_k1122.py        mã thoát 0 = mọi ca đúng kỳ vọng
"""
import copy, gzip, itertools, json, os, sys

import yaml

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, ROOT)
from checks.ll import q_k2var as K, q_rhythm as QR, q_setting as QG, cap112  # noqa: E402

FX = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures')
R = []


def case(rule, name, got, expect_fail):
    got = list(got) if got else []
    R.append((rule, name, 'bắt lỗi' if expect_fail else 'sạch', bool(got) == expect_fail, got[:2]))


def bad(r): return r['loi'] + r.get('thieu', [])


E1 = yaml.safe_load(gzip.open(os.path.join(FX, 'k2c106-g2', 'episode.yaml.gz'))); TL1 = json.load(gzip.open(os.path.join(FX, 'k2c106-g2', 'timeline.json.gz')))
E2 = yaml.safe_load(gzip.open(os.path.join(FX, 'k1122', 't2-head-episode.yaml.gz'))); TL2 = json.load(gzip.open(os.path.join(FX, 'k112', 't2-v34-timeline.json.gz')))
fix = lambda A: [dict(a, phm=[tuple(p[:3]) + (tuple(p[3]),) for p in a['phm']]) for a in A]
A2 = fix(json.load(gzip.open(os.path.join(FX, 'k1122', 't2-aps.json.gz')))['aps']); MA = json.load(gzip.open(os.path.join(FX, 'k1122', 'master-aps.json.gz')))['aps']
A1, AS = fix(MA['t1']), fix(MA['steel'])

# =============================================================== NHIP-K2 (Q14/Q15/Q17 → Q37)
for nm, E, TL in (('T1', E1, TL1), ('T2', E2, TL2)):
    m = QR.measure(E, TL)
    case('NHIP-K2', f"{nm}: Q14–Q18 trả 'không áp' (luật nhịp LL không áp kênh 2)", [k for k, v in m.items() if not v['val'].startswith('không áp')], False)
r = K.nhip_k2(E2, TL2); case('NHIP-K2', f"T2 v3.4: {r['val']}", r['loi'], False)
r = K.nhip_k2(E1, TL1); case('NHIP-K2', f"T1 (dựng trước luật nhịp kênh 2): {r['loi'][:1]}", r['loi'], True)
case('NHIP-K2', "đặc tả khai `kenh: 1` dù mã 'k2…' → luật LL áp (is_k2 = False)", [] if not QR.is_k2(dict(id='k2x', kenh=1)) else ['vẫn coi là kênh 2'], False)
case('NHIP-K2', "đặc tả LL mã 'll-ep09' khai `kenh: 2` → không áp", [] if QR.is_k2(dict(id='ll-ep09', kenh=2)) else ['vẫn áp LL'], False)
case('NHIP-K2', 'tập LL (không kênh 2) → NHIP-K2 không áp, Q14–Q18 giữ nguyên', [] if K.nhip_k2(dict(id='ll-ep09'), TL2).get('khong_ap') else ['áp nhầm'], False)
TLx = copy.deepcopy(TL2); Ex = copy.deepcopy(E2)
for sg in TLx['segments']:
    sg['shots'] = [dict(sg['shots'][0], t0=0.0, t1=sg['t1'] - sg['t0'], p={'hero': sg['shots'][0]['p'].get('hero')})]
for sg in Ex['segments']: sg['shots'] = sg['shots'][:1]
r = K.nhip_k2(Ex, TLx); case('NHIP-K2', f"T2 gộp mỗi chương thành 1 shot không mốc (tổng hợp) → dài nhất {r.get('moc_dac_ta', {}).get('dai_nhat')} s > 6 s", r['loi'], True)

# =============================================================== Q26b-K2
r1, r2 = K.q26b_k2(E1, TL1), K.q26b_k2(E2, TL2)
case('Q26b-K2', f"T1: {r1['val']}", bad(r1), False)
case('Q26b-K2', f"T2 v3.4: {r2['val']} → (a) nửa sau 2 loại, (b) bản đồ 88,7 %, (c), (d) eastus", r2['loi'] if all(r2['muc'][k] for k in 'abcd') else ['sai mục'], True)
case('Q26b-K2', 'bản đồ KHÔNG còn trung tính: T2 bản đồ vào loại ban_do và vào vùng (Q26b cũ: trung tính 99 %)', [] if r2['loai'].get('ban_do', 0) > 80 and r2['vung'].get('eastus') else ['bản đồ vẫn trung tính'], False)
case('Q26b-K2', 'Q26b cũ trên T2 trượt (c) vì bản đồ trung tính — biến thể không còn lỗi (c) cũ này', [x for x in QG.q26b(TL2, E2)['loi'] if 'nửa sau' in x], True)
E3 = copy.deepcopy(E2)
for sg in E3['segments']:
    for sh in sg['shots']:
        if sh.get('scene_id') == 'relief/eastus': sh['vung'] = ['eastus-a', 'eastus-b', 'eastus-c'][int(sg['id']) % 3]
r = K.q26b_k2(E3, TL2)
case('Q26b-K2', f"T2 khai vùng nhỏ hơn cho bờ Đông (3 khu, tổng hợp): (c), (d) hết lỗi — {r['val'][:70]}", r['muc']['c'] + r['muc']['d'], False)
mo, ch, cb = cap112.cap('Q26b-K2', r2)
case('Q26b-K2', f'cấp: (c), (d) vào phần Chặn, (a), (b) vào Cảnh báo ({mo})', [] if all(x[:3] in ('(c)', '(d)') for x in ch) and all(x[:3] in ('(a)', '(b)') for x in cb) else ['sai cấp'], False)

# =============================================================== Q33-K2
r = K.q33_k2(None, None, aps=copy.deepcopy(A2))
case('Q33-K2', f"T2 (khoá vùng HEAD, tờ khung nháp): {r['val']} — bờ Đông góc rộng sông Delaware lặp ở chương 03/05/06", r['loi'], True)
lap = sorted(k.split(' · ')[1] for k, v in r['bang'].items() if v['tong'] > 2)
case('Q33-K2', f"T2: 4 khoá > 2 đúng các góc bờ Đông đã xem mắt ({', '.join(lap)})", [] if lap == ['t2-03-scale', 't2-05-cost', 't2-05-philly', 't2-06-watch'] else [f'khác: {lap}'], False)
case('Q33-K2', 'T2 cặp sepia ↔ xanh (r02_subsidy ↔ r03_scale, pHash L 12) KHÔNG gộp nhờ ΔE màu',
     [] if not K.lien_ket(next(a for a in A2 if a['cam'] == 't2-02-subsidy'), next(a for a in A2 if a['cam'] == 't2-03-scale'), K.THETA_L) else ['gộp nhầm'], False)
sf = r['bang']['relief/sfbay · t2-01-dive']
case('Q33-K2', f"T2 vịnh SF: launch ↔ dive cùng góc (pHash L 10, ΔE 0,5) nhưng lần chương 01 khai năm khác → miễn: {sf['luc']}", [] if sf['mien'] == 1 and sf['tong'] == 2 else ['không miễn'], False)
r = K.q33_k2(None, None, aps=copy.deepcopy(A1))
case('Q33-K2', f"T1 master: {r['val']} — địa cầu không khai vùng (m_oregon ↔ m_calif/m_calif2)", r['loi'], True)
A1v = copy.deepcopy(A1)
for a in A1v:
    if a['scene'] == 'map/globe': a['scene'] = 'map/globe:' + a['cam'].rstrip('0123456789').replace('m_', '')
r = K.q33_k2(None, None, aps=A1v)
case('Q33-K2', f"T1 khai vùng cho bản đồ địa cầu theo bang (tổng hợp từ tên góc): {r['val'][:80]}", r['loi'], False)
a0 = copy.deepcopy(A2[0]); b0 = dict(copy.deepcopy(a0), scene='relief/khac', cam='x', t0=a0['t0'] + 300, t1=a0['t1'] + 300)
c0 = dict(copy.deepcopy(a0), cam='y', t0=a0['t0'] + 400, t1=a0['t1'] + 400)
case('Q33-K2', 'khác vùng, cùng băm → không bao giờ gộp', [] if not any(K.lien_ket(b0, a0, K.THETA_L) and b0['scene'] == a0['scene'] for _ in [0]) and
     K.q33_k2(None, None, aps=[a0, b0])['bang'][f"{a0['scene']} · {a0['cam']}"]['tong'] == 1 else ['gộp khác vùng'], False)
g = [dict(copy.deepcopy(a0), cam='z', seg='00', t0=10.0 * k, t1=10.0 * k + 3) for k in range(3)]
case('Q33-K2', 'cùng (vùng, góc) khai 3 lần cùng chương → TRƯỢT', K.q33_k2(None, None, aps=copy.deepcopy(g))['loi'], True)
g[2].update(seg='05', nam='1990'); g[0]['nam'] = '1943'; g[1]['nam'] = '1943'
case('Q33-K2', 'lần thứ 3 ở chương khác + khai năm khác → miễn, ĐẠT', K.q33_k2(None, None, aps=copy.deepcopy(g))['loi'], False)
g[2].pop('nam'); g[2]['lop'] = 'gdp'; g[0]['lop'] = 'tonnage'; g[1]['lop'] = 'tonnage'
case('Q33-K2', 'lần thứ 3 ở chương khác + khai lớp dữ liệu khác → miễn, ĐẠT', K.q33_k2(None, None, aps=copy.deepcopy(g))['loi'], False)
g[2]['seg'] = '00'
case('Q33-K2', 'lần thứ 3 khác lớp nhưng CÙNG chương → không miễn, TRƯỢT', K.q33_k2(None, None, aps=copy.deepcopy(g))['loi'], True)
r = K.q33_k2(E2, TL2)
case('Q33-K2', 'không có master/băm → THIẾU (không ĐẠT)', r['thieu'] if r['ket_qua'] == 'THIẾU' else [], True)
neg = [K.dL(a, b) for A in (A1, AS) for a, b in itertools.combinations(A, 2) if a['scene'] != b['scene']]
sam = [K.dL(a, b) for A in (A1, AS) for a, b in itertools.combinations(A, 2) if a['scene'] == b['scene'] and a['cam'] != b['cam']]
fr = lambda L, t: sum(d <= t for d in L) / max(len(L), 1)
th = max(t for t in range(0, 64, 2) if fr(neg, t) <= 0.01 and fr(sam, t) <= 0.02)
case('Q33-K2', f"hiệu chuẩn θ_L trên master Steel + T1 (khác bộ ≤ 1 %, cùng bộ khác góc ≤ 2 %) = {th} (khác bộ {100 * fr(neg, th):.2f} %, cùng bộ khác góc {100 * fr(sam, th):.2f} %)",
     [] if th == K.THETA_L else [f'θ đo {th} ≠ THETA_L {K.THETA_L}'], False)

# =============================================================== Q32b-K2 (NN2)
r = K.q32b_k2(E2, TL2)
ow = {x['clip']: x for x in r['bang']}
case('Q32b-K2', f"T2 Owens {ow['LOC-FSA-8D18716']['s']} s ({ow['LOC-FSA-8D18716']['loai']}) và Jones {ow['LOC-NPCC-21943']['s']} s ({ow['LOC-NPCC-21943']['loai']}) ≤ 12 s → ĐẠT", r['loi'], False)
case('Q32b-K2', f"T1: {K.q32b_k2(E1, TL1)['val']}", K.q32b_k2(E1, TL1)['loi'], False)


def film(ty, d, push=None, lines=(), cam=None):
    h = dict(hero='photo/print', opt=dict({'img': '/cache/x.jpg'}, **({'push': push} if push is not None else {})), **({'cam': cam} if cam else {}))
    p = dict(hero='h1', clip='C1', **({'side': dict(lines=[dict(s=f'l{i}', at=a) for i, a in enumerate(lines)])} if lines else {}))
    TL = dict(tong_s=d + 5, heroes={'h1': h}, segments=[dict(id='00', t0=0.0, t1=d + 5, shots=[dict(tpl='plate', t0=0.0, t1=d, p=p), dict(tpl='plate', t0=d, t1=d + 5, p={})])])
    E = dict(id='k2x', heroes={'h1': h}, segments=[dict(id='00', shots=[dict(tpl='plate', type=ty, camera_id=cam or 'still'), dict(tpl='plate', type='map')])])
    return K.q32b_k2(E, TL)


case('Q32b-K2', 'ảnh TĨNH HOÀN TOÀN 12 s (không Ken Burns, chú thích không đổi) → TRƯỢT (trần 8 s)', film('photo', 12.0)['loi'], True)
case('Q32b-K2', 'ảnh tĩnh hoàn toàn 7,9 s → ĐẠT', film('photo', 7.9)['loi'], False)
case('Q32b-K2', 'ảnh Ken Burns (opt.push 0,12) 11,5 s → ĐẠT', film('photo', 11.5, push=0.12)['loi'], False)
case('Q32b-K2', 'ảnh có chú thích đổi 1 lần (dòng 2 hiện ở 4 s) 11,5 s → ĐẠT', film('photo', 11.5, lines=(0.0, 4.0))['loi'], False)
case('Q32b-K2', 'ảnh Ken Burns 12,5 s > 12 s → TRƯỢT', film('photo', 12.5, push=0.12)['loi'], True)
case('Q32b-K2', 'chú thích chỉ hiện ở đầu shot (< 0,5 s) không tính "đổi" → ảnh tĩnh 10 s TRƯỢT', film('photo', 10.0, lines=(0.2,))['loi'], True)
case('Q32b-K2', 'footage chuyển động 9 s → TRƯỢT (giữ 8 s)', film('footage', 9.0)['loi'], True)
case('Q32b-K2', 'document có máy push (cam push) 10 s → ĐẠT', film('document', 10.0, cam='push')['loi'], False)

for rule, name, kind_, ok, got in R: print(f"{'ĐÚNG' if ok else 'SAI '}  {rule:<8} {kind_:<8} {name}" + ('' if ok else f'   → {got}'))
by = {}
for rule, _, k, ok, _ in R: by.setdefault(rule, set()).add(k)
miss = [k for k, v in by.items() if v != {'sạch', 'bắt lỗi'}]
n_ok = sum(r[3] for r in R); print(f'\nselftest 1.12.2: {n_ok}/{len(R)} ca đúng kỳ vọng · {len(by)} biến thể, thiếu ca đạt hoặc trượt: {miss or "không"}')
sys.exit(0 if n_ok == len(R) and not miss else 1)
