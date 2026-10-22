#!/opt/cine/bin/python
"""Tự kiểm luật 1.16 (phiên K, 19/10/2026; 1.16.1: thước cắt cấu trúc, K116-D2/D3/D5): luật mới cho tập kênh 2 từ T3 (SACH-1, CHUONG-1, PP-1, TL-1/2/3, NHIP-NGHIA, XEM-CAM, PC-1) và các
khiếu nại chấp nhận (K-LAI-2/3/4/5/6/B + K-LAI-3V nhánh vân, NC-H5 (b), BD-3, Q26b theo vùng, Q37 miễn khung neo, A* khi không lời/animatic,
ML1 đọc lời khoá). Mỗi luật ≥ 1 ca ĐẠT + ≥ 1 ca TRƯỢT. Không gọi mạng/API. Dữ liệu:
  fixtures/k116/ep-t3/  tập T3 giả (make_fixtures.py)        fixtures/k116/vid/  video tổng hợp 320×180 (cắt, lia, phóng; 1.16.1: ngày–đêm cùng góc, cắt cùng sáng)
  fixtures/k116/v6/     bản SAO THẬT: log khung + log chữ đoạn thử V6 (reports/v6/doan-thu/lai), sổ PT3 vân (reports/pt3/ai)
  fixtures/k116/g1b/    bản SAO THẬT: kiem.json kiểm có đáp án phục chế G1b (reports/g1b-t3/phuc-che)
  fixtures/k115/ep-lai/ tập cũ (không khung_sach) — kiểm cổng 1.16 không bật

  /opt/cine/bin/python checks/ll/selftest_k116.py        mã thoát 0 = mọi ca đúng kỳ vọng
"""
import copy, json, os, shutil, sys, tempfile

import yaml

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, ROOT)
from checks.ll import q_k116 as K6, q_lai as LA, q_setting as QS, q_nhip as NH, q_amthanh as AM, q_mach as MA, cap112  # noqa: E402

FX = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures')
D = os.path.join(FX, 'k116'); EP = os.path.join(D, 'ep-t3'); TMP = tempfile.mkdtemp(prefix='k116-')
R, INFO = [], []


def case(rule, name, got, expect_fail):
    got = list(got) if got else []
    R.append((rule, name, 'bắt lỗi' if expect_fail else 'sạch', bool(got) == expect_fail, got[:2]))


def bad(x, *muc):
    L = x['loi'] + (x.get('thieu') or [])
    return [y for y in L if not muc or any(y.startswith(f'({m})') or f'] ({m})' in y for m in muc)]


def thieu(x): return x['thieu'] if x.get('ket_qua') == 'THIẾU' else ['không phải THIẾU: ' + str(x.get('ket_qua'))]


def khong_ap(x): return [] if x.get('ket_qua') == 'KHÔNG ÁP' else ['không phải KHÔNG ÁP: ' + str(x.get('ket_qua'))]


def tmpf(name, obj, jsonl=False):
    p = os.path.join(TMP, name)
    with open(p, 'w') as f:
        if jsonl: f.write(''.join(json.dumps(x, ensure_ascii=False) + '\n' for x in obj))
        elif isinstance(obj, str): f.write(obj)
        else: json.dump(obj, f, ensure_ascii=False)
    return p


E0 = yaml.safe_load(open(os.path.join(EP, 'episode.yaml')))
for k in ('log_shot', 'nhip_vat', 'xem_cam', 'loi_khoa', 'claims_md', 'nam_khung', 'log_chu'): E0[k] = os.path.join(EP, E0[k])
E0['phat_hanh']['mo_ta'] = os.path.join(EP, E0['phat_hanh']['mo_ta']); E0['phuc_che']['kiem'] = os.path.join(EP, E0['phuc_che']['kiem'])
LS0 = json.load(open(E0['log_shot']))


def mk_tl(E):
    t, S = 0.0, []
    for s in E['segments']:
        S.append(dict(id=s['id'], t0=t, dur=s['dur'], part=s.get('part'), shots=[dict(tpl=sh['tpl'], t0=0.0, t1=s['dur'], type=sh.get('type'), p=sh.get('p') or {}) for sh in s['shots']]))
        t += s['dur']
    return dict(segments=S, heroes=E.get('heroes') or {}, tong_s=t)


def ep(**over):
    E = copy.deepcopy(E0)
    for k, v in over.items():
        if v is None: E.pop(k, None)
        else: E[k] = v
    return E


def shot(E, sid):
    return next(s for s in E['segments'] if s['id'] == sid)['shots'][0]


def ls_file(fn):
    L = copy.deepcopy(LS0); fn(L); return tmpf(f'ls-{len(R)}.json', L)


def run(fn, E, *a, **kw): return fn(E, mk_tl(E), *a, **kw)


TX0, ST0, W0, H0 = K6.text_frames(None, None, E0['log_chu'], EP)

# ================================================================ cổng 1.16
EOLD = yaml.safe_load(open(os.path.join(FX, 'k115', 'ep-lai', 'episode.yaml')))
case('cổng', 'tập cũ (k115 ep-lai, không khung_sach) → mọi hàng 1.16 KHÔNG ÁP', sum((khong_ap(v) for v in K6.check(EOLD, None, '.').values()), []), False)
case('cổng', 'tập T3 (khung_sach: true) → 1.16 bật', [] if K6.ap_116(E0) else ['không bật'], False)
case('cổng', 'tập không khai khung_sach → ap_116 tắt (giữ 1.15)', ['tắt'] if not K6.ap_116(ep(khung_sach=None)) else [], True)

# ================================================================ SACH-1
r0 = K6.sach1(E0, mk_tl(E0), TX0, ST0)
case('SACH-1', f"fixture T3: bộ đếm + chip 2,5 s + thẻ chương + thẻ phương pháp — {r0['val']}", bad(r0), False)
E = ep(); shot(E, 'C02')['p']['so'] = [dict(s='14 sieges · 1309–1783', at=1, dur=3)]
case('SACH-1', 'p.so (số/câu trích ≤ 3 s, kiểu G1b) → (a) TL-4', bad(K6.sach1(E, mk_tl(E), TX0, ST0), 'a'), True)
E = ep(); shot(E, 'C02')['type'] = 'card'; shot(E, 'C02')['p']['card'] = dict(type='num', big='14', unit='sieges')
case('SACH-1', 'tấm số đứng riêng (card num) → (a)', bad(K6.sach1(E, mk_tl(E), TX0, ST0), 'a'), True)
E = ep(); shot(E, 'C05')['type'] = 'photo'; shot(E, 'C05')['p']['photo'] = 'x.jpg'
case('SACH-1', 'ảnh tư liệu đứng riêng → (b)', bad(K6.sach1(E, mk_tl(E), TX0, ST0), 'b'), True)
E = ep(); shot(E, 'C05')['type'] = 'photo'; shot(E, 'C05')['p'].update(photo='x.jpg', phu_dia_hinh=dict(img='x.jpg', dur=2.5))
case('SACH-1', 'tư liệu phủ lên địa hình 2,5 s → sạch', bad(K6.sach1(E, mk_tl(E), TX0, ST0), 'b'), False)
shot(E, 'C05')['p']['phu_dia_hinh']['dur'] = 3.5
case('SACH-1', 'tư liệu phủ 3,5 s > 3 s → (b)', bad(K6.sach1(E, mk_tl(E), TX0, ST0), 'b'), True)
TX = copy.deepcopy(TX0); f = sorted(TX)[40]; TX[f].append(dict(s='Sayer 1862 · García Sanz 2022', role='src_ngan', alpha=1.0))
case('SACH-1', 'log: dòng nguồn ngắn hiện (vai src_ngan) → (c)', bad(K6.sach1(E0, mk_tl(E0), TX, ST0), 'c'), True)
TX = copy.deepcopy(TX0); TX[f].append(dict(s='Surface detail AI-assisted · layout, lan', role='ai_label', alpha=0.0))
case('SACH-1', 'log: nhãn AI alpha 0 (đã tắt) → sạch', bad(K6.sach1(E0, mk_tl(E0), TX, ST0), 'c'), False)
TX = copy.deepcopy(TX0); TX[f].append(dict(s='approx. borders c. 1704 — Cliopatria', role='tag', alpha=1.0))
case('SACH-1', 'log: "approx. borders" hiện dưới vai khác → (c) (bắt theo chữ)', bad(K6.sach1(E0, mk_tl(E0), TX, ST0), 'c'), True)
TX = copy.deepcopy(TX0)
for g in sorted(TX)[2:10]: TX[g].append(dict(s='Gibraltar', role='where', alpha=1.0))
case('SACH-1', 'chip nơi 4,0 s > 3 s → (d)', bad(K6.sach1(E0, mk_tl(E0), TX, ST0), 'd'), True)
# K116-D3 (duyệt 19/10 18:48, 1.16.1): bản đồ phủ địa hình ≤ 2 nhãn địa danh trong ≤ 3 s; không chú giải chữ → (e) Chặn
TX = copy.deepcopy(TX0)
for g in sorted(TX)[2:8]: TX[g] += [dict(s='Algeciras', role='diem', alpha=1.0), dict(s='Gibraltar', role='inset', alpha=1.0)]
rr = K6.sach1(E0, mk_tl(E0), TX, ST0)
case('SACH-1', f"K116-D3: 2 nhãn địa danh (diem + inset) hiện 3,0 s (sát ngưỡng) → sạch (e) — {rr['val']}", bad(rr, 'e'), False)
TX = copy.deepcopy(TX0)
for g in sorted(TX)[2:4]: TX[g] += [dict(s=x, role='diem', alpha=1.0) for x in ('Algeciras', 'Gibraltar', 'Tarifa')]
rr = K6.sach1(E0, mk_tl(E0), TX, ST0)
case('SACH-1', 'K116-D3: 3 nhãn địa danh cùng shot → (e)', bad(rr, 'e'), True)
case('cap', 'SACH-1 (e) là Chặn (K116-D3)', cap112.cap('SACH-1', rr)[1], True)
TX = copy.deepcopy(TX0)
for g in sorted(TX)[2:10]: TX[g].append(dict(s='Algeciras', role='tag', alpha=1.0))
case('SACH-1', 'K116-D3: nhãn địa danh hiện 4,0 s > 3 s → (e)', bad(K6.sach1(E0, mk_tl(E0), TX, ST0), 'e'), True)
TX = copy.deepcopy(TX0); TX[f].append(dict(s='Spain', role='chu_giai', alpha=1.0))
case('SACH-1', 'K116-D3: chú giải chữ (vai chu_giai) → (e) (phe bằng màu + cờ)', bad(K6.sach1(E0, mk_tl(E0), TX, ST0), 'e'), True)
TX = copy.deepcopy(TX0); TX[f].append(dict(s='≈ 4,200', role='index', alpha=1.0))
case('SACH-1', 'K116-D3: chữ ngoài danh sách (vai index) → (e)', bad(K6.sach1(E0, mk_tl(E0), TX, ST0), 'e'), True)
E = ep(); shot(E, 'C07')['p'].pop('sach')
case('SACH-1', 'shot không bật p.sach → (f)', bad(K6.sach1(E, mk_tl(E), TX0, ST0), 'f'), True)
case('SACH-1', 'không có log chữ → THIẾU (c) (Chặn)', thieu(K6.sach1(E0, mk_tl(E0), None)) + cap112.cap('SACH-1', K6.sach1(E0, mk_tl(E0), None))[1], True)

# ================================================================ CHUONG-1
r0 = K6.chuong1(E0, mk_tl(E0), TX0, ST0)
case('CHUONG-1', f"2 thẻ chương đúng dạng, ≤ 3 s, ngoài móc — {r0['val']}", bad(r0), False)


def ch(fn):
    E = ep(); fn(E); return K6.chuong1(E, mk_tl(E), TX0, ST0)
case('CHUONG-1', '9 thẻ > 8 → (a)', bad(ch(lambda E: [shot(E, f'C{k:02d}')['p'].__setitem__('the_chuong', dict(s=f'17{k:02d} — Year {k}', at=0.5, dur=2)) for k in range(1, 12)]), 'a'), True)
case('CHUONG-1', '8 thẻ = 8 → sạch (a)', bad(ch(lambda E: [shot(E, f'C{k:02d}')['p'].__setitem__('the_chuong', dict(s=f'17{k:02d} — Year {k}', at=0.5, dur=2)) for k in range(1, 9)]), 'a'), False)
case('CHUONG-1', 'cụm 7 từ → (b)', bad(ch(lambda E: shot(E, 'C04')['p']['the_chuong'].update(s='1704 — The Rock of Gibraltar changes hands again')), 'b'), True)
case('CHUONG-1', 'không có năm → (b)', bad(ch(lambda E: shot(E, 'C04')['p']['the_chuong'].update(s='The Rock changes hands')), 'b'), True)
case('CHUONG-1', '3,5 s > 3 s → (c)', bad(ch(lambda E: shot(E, 'C04')['p']['the_chuong'].update(dur=3.5)), 'c'), True)
case('CHUONG-1', 'thẻ trong móc mở đầu (chương 0) → (d)', bad(ch(lambda E: shot(E, 'C00')['p'].__setitem__('the_chuong', dict(s='1309 — First siege', at=1, dur=2))), 'd'), True)
case('CHUONG-1', '"captured" → (e) không trung tính', bad(ch(lambda E: shot(E, 'C04')['p']['the_chuong'].update(s='1704 — British troops captured Gibraltar')), 'e'), True)
E = ep()
for s in E['segments']: s['shots'][0]['p'].pop('the_chuong', None)
rl = K6.chuong1(E, mk_tl(E), TX0, ST0)
case('CHUONG-1', f"chỉ có log chữ vai the_chuong (góc dưới trái, mờ vào/ra) → sạch — {rl['val']}", bad(rl), False)
TX = copy.deepcopy(TX0)
for g in TX:
    for x in TX[g]:
        if x['role'] == 'the_chuong': x['box'] = [1200, 60, 1800, 110]
rl2 = K6.chuong1(E, mk_tl(E), TX, ST0)
case('CHUONG-1', 'log: thẻ ở góc trên phải → (f) Cảnh báo', bad(rl2, 'f'), True)
case('cap', 'CHUONG-1 (f) không vào Chặn', cap112.cap('CHUONG-1', rl2)[1], False)

# ================================================================ PP-1
r0 = K6.pp1(E0, mk_tl(E0))
case('PP-1', f"2 thẻ × 8 s cuối phim, đủ nguồn/ước tính/AI — {r0['val']}", bad(r0), False)
E = ep(); E['segments'] = E['segments'][:-1]
case('PP-1', '1 thẻ → (a)', bad(K6.pp1(E, mk_tl(E)), 'a'), True)
E = ep(); E['segments'][-1]['dur'] = 5.0
case('PP-1', 'thẻ 5 s (như G1b) → (b)', bad(K6.pp1(E, mk_tl(E)), 'b'), True)
E = ep(); E['segments'][-1]['dur'] = 9.0
case('PP-1', 'thẻ 9,0 s (cận trên ≈ 8 ± 1) → sạch (b)', bad(K6.pp1(E, mk_tl(E)), 'b'), False)
E = ep(); E['segments'].append(copy.deepcopy(E['segments'][0])); E['segments'][-1]['id'] = 'SAU'
case('PP-1', 'có shot sau thẻ phương pháp → (c) không ở cuối', bad(K6.pp1(E, mk_tl(E)), 'c'), True)
E = ep(); E['segments'][-1]['shots'][0]['p']['card']['items'] = [dict(s='Estimated: building heights.')]
case('PP-1', '1.17.2 (chủ dự án 22/10: không câu AI trong phim): không nói AI, còn nguồn + ước tính → sạch (d)', bad(K6.pp1(E, mk_tl(E)), 'd'), False)
E = ep(); E['segments'][-1]['shots'][0]['p']['card']['items'] = [dict(s=' '.join(['word'] * 30) + ' AI estimated')]
rr = K6.pp1(E, mk_tl(E))
case('PP-1', '33 từ / 8 s > 3 từ/s → (e) Cảnh báo', bad(rr, 'e'), True)
case('cap', 'PP-1 (e) không vào Chặn', cap112.cap('PP-1', rr)[1], False)

# ================================================================ TL-1 / TL-2 / TL-3
r0 = K6.tl1(E0, mk_tl(E0), LS0, None, None, None)
case('TL-1', f"(a)(e)(f) fixture: góc cao + thời gian chạy 89 %, 6 điểm máy × 2 năm — {r0['val'][:90]}", bad(r0, 'a', 'e', 'f'), False)
case('TL-1', 'không có video → THIẾU (c)(d) (Cảnh báo)', bad(r0, 'c'), True)
L = copy.deepcopy(LS0)
for x in L[:6]: x['tl'] = False
case('TL-1', '6 shot góc cao không có thời gian chạy → 47 % < 75 % (a)', bad(K6.tl1(E0, mk_tl(E0), L, None), 'a'), True)
L = copy.deepcopy(LS0)
for x in L:
    if x.get('diem_may') == 'd5': x['diem_may'] = 'd4'
case('TL-1', '5 điểm máy < 6 → (e)', bad(K6.tl1(E0, mk_tl(E0), L, None), 'e'), True)
L = copy.deepcopy(LS0); [x.update(moc=1704) for x in L if x.get('diem_may') == 'd0']
case('TL-1', 'điểm máy d0 chỉ ở một năm → (f)', bad(K6.tl1(E0, mk_tl(E0), L, None), 'f'), True)
L = copy.deepcopy(LS0); L[3].pop('goc')
case('TL-1', 'log thiếu goc → THIẾU (a)', thieu(K6.tl1(E0, mk_tl(E0), L, None)), True)
EV = dict(id='vid', khung_sach=True, segments=[dict(id=f'V{k}', dur=12.0, beats=[dict(t=0, k='cut')], shots=[dict(tpl='plate', at=0, type='scene3d', p=dict(sach=True, hero='h'))]) for k in range(3)])
LV = [dict(shot=f'V{k}', goc='cao', tl=True, diem_may=f'v{k}') for k in range(3)]
VF = K6.video_gray(os.path.join(D, 'vid', 'v-ok.mp4')); rv = K6.tl1(EV, mk_tl(EV), LV, None, None, VF)
INFO.append(f"TL-1 video tổng hợp v-ok: {rv['val']}")
case('TL-1', 'video v-ok: 2 cắt / 0,6 phút = 3,33 ≤ 5 → sạch (c)', bad(rv, 'c'), False)
case('TL-1', 'video v-ok: shot lia 6 %/s > 2 %/s → (d); shot trôi 1 %/s và đẩy máy phóng 3 %/s (góc khung 1,6 %/s) không lỗi',
     [x for x in bad(rv, 'd') if 'V1 ' in x] if len(bad(rv, 'd')) == 1 else ['số shot lỗi (d) ≠ 1: ' + str(bad(rv, 'd'))], True)
VC = K6.video_gray(os.path.join(D, 'vid', 'v-cat.mp4')); rc = K6.tl1(EV, mk_tl(EV), LV, None, None, VC)
case('TL-1', 'video v-cat: 11 cắt / 0,6 phút = 18,3 > 5 → (c)', bad(rc, 'c'), True)
case('TL-1', f"thước cắt: v-ok đúng 2 cắt ở 12 s, 24 s · v-cat đúng 11 cắt", [] if [round(x) for x in K6.cuts_video(*VF)] == [12, 24] and len(K6.cuts_video(*VC)) == 11 else ['lệch'], False)
case('cap', 'TL-1 toàn Cảnh báo (hiệu chỉnh sau V7-PILOT)', cap112.cap('TL-1', rc)[1], False)
# 1.16.1 thước cắt cấu trúc (đổi cấu trúc, không phải đổi độ sáng/màu toàn khung; bỏ dải phụ đề)
VN = K6.video_gray(os.path.join(D, 'vid', 'v-ngaydem.mp4')); cn = K6.cuts_video(*VN)
case('TL-1', 'thước cắt 1.16.1: timelapse MỘT góc máy đổi ngày–đêm nhanh + đèn bật + chớp 2 khung + khói + phụ đề nung đổi chữ → 0 cắt',
     [f'{len(cn)} cắt: {cn}'] if cn else [], False)
VS = K6.video_gray(os.path.join(D, 'vid', 'v-cungsang.mp4')); cs = K6.cuts_video(*VS)
case('TL-1', 'thước cắt 1.16.1: cắt cứng giữa hai cảnh cùng histogram độ sáng (3,0 s) → đúng 1 cắt', [] if len(cs) == 1 and abs(cs[0] - 3.0) <= 0.1 else [f'{cs}'], False)
case('TL-1', 'thước cắt 1.16.1: v-cungsang chỉ lấy 3 s trước cắt (khung 0–35) → 0 cắt (chứng: phát hiện đến từ đổi cảnh)',
     K6.cuts_video(VS[0][:36], VS[1]), False)
nk, cv_, cs_ = K6.doi_chieu_cat([12.02, 24.4, 30.0], [12.0, 24.0, 18.0])
case('TL-1', 'đối chiếu ranh đặc tả ±0,5 s: video [12,02; 24,4; 30] ↔ đặc tả [12; 18; 24] → 2 khớp, chỉ video 30, chỉ đặc tả 18',
     [] if (nk, cv_, cs_) == (2, [30.0], [18.0]) else [f'{(nk, cv_, cs_)}'], False)
case('TL-1', 'đối chiếu: lệch 0,6 s > 0,5 s → không khớp', [] if K6.doi_chieu_cat([12.6], [12.0])[0] == 0 else ['khớp'], False)
case('TL-1', 'TL-1 báo cả hai số (video + đặc tả + khớp)', [] if 'đặc tả' in rv['val'] and 'khớp ±0.5 s' in rv['val'] and (rv.get('cat_video') or {}).get('khop') == 2 else [rv['val'][-160:]], False)
EN = dict(id='nd', khung_sach=True, segments=[dict(id='N0', dur=8.0, beats=[dict(t=0, k='cut')], shots=[dict(tpl='plate', at=0, type='scene3d', p=dict(sach=True, hero='h'))])])
rn = K6.tl1(EN, mk_tl(EN), None, 'không log', None, VN)
case('TL-1', 'TL-1 (c) trên v-ngaydem: 0 cắt/phút → sạch (c)', bad(rn, 'c'), False)

r0 = K6.tl2(E0, mk_tl(E0), LS0)
case('TL-2', f"lướt thấp 1 shot 8 s, có vai, phố — {r0['val']}", bad(r0), False)
L = copy.deepcopy(LS0); [x.update(goc='thap', vai='crowd at the quay', noi='thanh_pho') for x in L[:3]]
case('TL-2', '4 shot lướt thấp 38 s = 26 % > 10 % → (a)', bad(K6.tl2(E0, mk_tl(E0), L), 'a'), True)
L = copy.deepcopy(LS0); [x.update(vai='') for x in L if x['goc'] == 'thap']
case('TL-2', 'lướt thấp không có vai → (b)', bad(K6.tl2(E0, mk_tl(E0), L), 'b'), True)
L = copy.deepcopy(LS0); [x.update(noi='eo_dat') for x in L if x['goc'] == 'thap']
case('TL-2', 'lướt thấp trên eo đất, không người → (b)', bad(K6.tl2(E0, mk_tl(E0), L), 'b'), True)
[x.update(nguoi=True) for x in L if x['goc'] == 'thap']
case('TL-2', 'lướt thấp trên eo đất là khoảnh khắc người (nguoi: true) → sạch', bad(K6.tl2(E0, mk_tl(E0), L), 'b'), False)
r0 = K6.tl3(E0, mk_tl(E0), LS0)
case('TL-3', f"mọi shot 3D có thời gian chạy, trống 20 % — {r0['val']}", bad(r0), False)
L = copy.deepcopy(LS0); L[2].update(tl=False, su_kien=[])
case('TL-3', 'shot không thời gian chạy, không biến cố → (a)', bad(K6.tl3(E0, mk_tl(E0), L), 'a'), True)
L = copy.deepcopy(LS0); L[2].update(tl=False, trong_pct=70.0)
case('TL-3', 'trống 70 % > 60 % mà không thời gian chạy (dù có biến cố) → (b)', bad(K6.tl3(E0, mk_tl(E0), L), 'b'), True)
L = copy.deepcopy(LS0); L[2].update(trong_pct=70.0)
case('TL-3', 'trống 70 % nhưng có thời gian chạy → sạch (b)', bad(K6.tl3(E0, mk_tl(E0), L), 'b'), False)
L = copy.deepcopy(LS0); L[2]['bac'] = ''
case('TL-3', 'không ghi bac → (c)', bad(K6.tl3(E0, mk_tl(E0), L), 'c'), True)
L = copy.deepcopy(LS0); L[2].pop('trong_pct')
case('TL-3', 'thiếu trong_pct → THIẾU (b)', thieu(K6.tl3(E0, mk_tl(E0), L)), True)

# ================================================================ NHIP-NGHIA
NV0 = json.load(open(E0['nhip_vat']))
r0 = K6.nhip_nghia(E0, mk_tl(E0), NV0)
case('NHIP-NGHIA', f"15/15 nhịp chính có vật — {r0['val']}", bad(r0), False)
NV = copy.deepcopy(NV0); [x.update(vat=[]) for x in NV['nhip'][:2]]
rr = K6.nhip_nghia(E0, mk_tl(E0), NV)
case('NHIP-NGHIA', f"2 nhịp thiếu vật → 13/15 = 86,7 % < 90 % — {rr['val']}", bad(rr), True)
NV = copy.deepcopy(NV0); NV['nhip'][0]['vat'] = []
case('NHIP-NGHIA', '1 nhịp thiếu → 14/15 = 93,3 % ≥ 90 % → sạch', bad(K6.nhip_nghia(E0, mk_tl(E0), NV)), False)
NV = copy.deepcopy(NV0); NV['nhip'][0]['vat'] = [dict(loai='mau_dep', shot='C00')]
case('NHIP-NGHIA', 'loại vật ngoài danh sách §13.2 → lỗi', bad(K6.nhip_nghia(E0, mk_tl(E0), NV)), True)
NV = copy.deepcopy(NV0); NV['nhip'][0]['vat'] = [dict(loai='dem_nam', shot='XX')]
case('NHIP-NGHIA', 'shot không có trong đặc tả → lỗi', bad(K6.nhip_nghia(E0, mk_tl(E0), NV)), True)
NV = copy.deepcopy(NV0); NV['nhip'][0]['vat'] = [dict(loai='the_chuong', shot='C00')]
case('NHIP-NGHIA', 'vật thẻ chương ở shot không có thẻ → lỗi', bad(K6.nhip_nghia(E0, mk_tl(E0), NV)), True)
case('NHIP-NGHIA', 'không có tệp bảng nhịp → THIẾU', thieu(K6.nhip_nghia(E0, mk_tl(E0), None, 'không khai')), True)

# ================================================================ XEM-CAM
XC0 = json.load(open(E0['xem_cam']))
r0 = K6.xem_cam(XC0, None, EP)
case('XEM-CAM', f"8 câu, 3 AI + chủ dự án, tắt tiếng, thấp nhất 6/8 — {r0['val']}", bad(r0), False)
# K116-D2 (duyệt 19/10 18:48): đạt = chủ dự án ≥ 6/8 VÀ trung bình người chấm AI ≥ 6/8
X = copy.deepcopy(XC0); X['nguoi_cham'][1].update(dung=5); rr = K6.xem_cam(X, None, EP)
case('XEM-CAM', f"K116-D2: một AI 5/8 nhưng TB AI 6,67 ≥ 6 → sạch — {rr['val']}", bad(rr), False)
X = copy.deepcopy(XC0); X['nguoi_cham'][0].update(dung=6); X['nguoi_cham'][2].update(dung=6)
case('XEM-CAM', 'K116-D2: TB AI đúng 6,00 (sát ngưỡng) → sạch', bad(K6.xem_cam(X, None, EP)), False)
for nm, fn, m in (('K116-D2: TB AI 5,67 < 6 (AI 5, 6, 6) → (c)', lambda X: [X['nguoi_cham'][i].update(dung=d) for i, d in ((0, 5), (1, 6), (2, 6))], 'c'),
                  ('K116-D2: chủ dự án 5/8 (TB AI 7) → (c)', lambda X: X['nguoi_cham'][3].update(dung=5), 'c'), ('chỉ 2 người chấm AI → (b)', lambda X: X['nguoi_cham'].pop(0), 'b'),
                  ('không có chủ dự án → (b)', lambda X: X['nguoi_cham'].pop(3), 'b'), ('không tắt tiếng → (a)', lambda X: X.update(tat_tieng=False), 'a'),
                  ('7 câu hỏi → (a)', lambda X: X['cau_hoi'].pop(), 'a'), ('có email → (d)', lambda X: X['nguoi_cham'][3].update(id='abc@example.com'), 'd')):
    X = copy.deepcopy(XC0); fn(X); case('XEM-CAM', nm, bad(K6.xem_cam(X, None, EP), m), True)
X = copy.deepcopy(XC0); X.update(video=os.path.join(D, 'vid', 'v-ok.mp4'), video_sha256='0' * 64)
case('XEM-CAM', 'SHA animatic khác bản đã chấm → (e)', bad(K6.xem_cam(X, None, EP), 'e'), True)
case('XEM-CAM', 'không có tệp kết quả → THIẾU (Chặn)', thieu(K6.xem_cam(None, 'không khai `xem_cam:`')), True)

# ================================================================ PC-1 (dữ liệu THẬT G1b)
r0 = K6.pc1(E0, EP)
INFO.append(f"PC-1 G1b thật: {r0['val']}")
case('PC-1', '000757 · Swin2SR (Δ cạnh mới −0,23 điểm so bicubic, PSNR +0,42 dB) → dùng được', bad(r0), False)
for anh, cc, nm in (('342-FH_000759.jpg', 'swin2sr_x2', '000759 · Swin2SR Δ +2,24 điểm → lỗi'), ('342-FH_000761.jpg', 'swin2sr_x2', '000761 · Swin2SR Δ +1,13 điểm → lỗi'),
                    ('342-FH_000757.jpg', 'realesrgan_x2plus', '000757 · Real-ESRGAN Δ +46,1, PSNR −15 dB → lỗi')):
    case('PC-1', nm, bad(K6.pc1(ep(phuc_che=dict(kiem=E0['phuc_che']['kiem'], dung=[dict(anh=anh, cong_cu=cc)])), EP)), True)
case('PC-1', 'không khai phuc_che → KHÔNG ÁP', khong_ap(K6.pc1(ep(phuc_che=None), EP)), False)
case('PC-1', 'ảnh dùng không có trong kiểm có đáp án → THIẾU', thieu(K6.pc1(ep(phuc_che=dict(kiem=E0['phuc_che']['kiem'], dung=[dict(anh='khac.jpg', cong_cu='swin2sr_x2')])), EP)), True)
case('cap', 'PC-1 Cảnh báo', cap112.cap('PC-1', K6.pc1(ep(phuc_che=dict(kiem=E0['phuc_che']['kiem'], dung=[dict(anh='342-FH_000759.jpg', cong_cu='swin2sr_x2')])), EP))[1], False)

# ================================================================ K-LAI 1.16 (khiếu nại A-G1B-1, A-V6-1)
LAI0 = LA.check116(E0, mk_tl(E0), EP, None)
case('K-LAI-2', f"1.16: cờ AI mọi khung, shot khai khớp, thẻ PP nói AI, mô tả AI use = Yes, không nhãn trên hình — {LAI0['K-LAI-2']['val']}", bad(LAI0['K-LAI-2']), False)
E = ep(phat_hanh=dict(mo_ta=tmpf('mt.md', 'Sources: Spilsbury.\n')))
case('K-LAI-2', 'mô tả không có "AI use = Yes" → (d)', bad(LA.check116(E, mk_tl(E), EP, None)['K-LAI-2'], 'd'), True)
E = ep(); E['segments'][-1]['shots'][0]['p']['card']['items'] = [dict(s='Estimated: heights.')]; E['segments'][-2]['shots'][0]['p']['card']['items'] = [dict(s='Sources: maps.')]
case('K-LAI-2', '1.17.2: thẻ phương pháp không nói AI → sạch (c) (bỏ yêu cầu)', bad(LA.check116(E, mk_tl(E), EP, None)['K-LAI-2'], 'c'), False)
E = ep(lai=dict(E0['lai'], log_chu=tmpf('lc.json', [dict(f=100, items=[dict(s='Surface detail AI-assisted · layout, lan', role='ai_label', alpha=1.0)])])))
case('K-LAI-2', 'nhãn "Surface detail AI-assisted" hiện trên hình → (e) (§12.1)', bad(LA.check116(E, mk_tl(E), EP, None)['K-LAI-2'], 'e'), True)
E = ep(log_shot=ls_file(lambda L: [x.update(ai_texture=False) for x in L]))
case('K-LAI-2', 'log khung có vân ở C03 nhưng đặc tả/log shot không khai → (b)', bad(LA.check116(E, mk_tl(E), EP, None)['K-LAI-2'], 'b'), True)
case('K-LAI-3', f"1.16 vân sạch (1 tệp dùng, 0 lỗi chắc) — {LAI0['K-LAI-3']['val']}", bad(LAI0['K-LAI-3']), False)
case('K-LAI-4', 'chỉ vân (không tấm C) → K-LAI-4/5/B KHÔNG ÁP', sum((khong_ap(LAI0[k]) for k in ('K-LAI-4', 'K-LAI-5', 'K-LAI-B')), []), False)
FK = [json.loads(l) for l in open(os.path.join(EP, 'lai', 'log-khung.jsonl'))]; [x.update(ai_image=True) for x in FK if x['shot'] == 'C05/0']
E = ep(lai=dict(E0['lai'], log_khung=tmpf('lk-img.jsonl', FK, jsonl=True))); rr = LA.check116(E, mk_tl(E), EP, None)
case('K-LAI-4', 'có cả tấm C (ai_image) → K-LAI-4 áp lại: không khai bao_ve → THIẾU', thieu(rr['K-LAI-4']), True)
case('K-LAI-3', 'có tấm C mà không có sổ tấm C → K-LAI-3 [tấm C] THIẾU', [x for x in rr['K-LAI-3']['thieu'] if '[tấm C]' in x], True)
case('K-LAI-6', f"vân: input.mask_frac thay mask.pct_duoc_sua — {LAI0['K-LAI-6']['val']}", bad(LAI0['K-LAI-6']), False)
case('K-LAI-3V', 'vân dùng không ghi nghi vấn → sạch', bad(LAI0['K-LAI-3V']), False)
KV = json.load(open(os.path.join(EP, 'lai', 'kiem-van.json')))
K1 = copy.deepcopy(KV); K1['tep'][0]['loi_chac'] = ['thêm cửa sổ']
E = ep(lai=dict(E0['lai'], kiem_du_kien_van=tmpf('kv1.json', K1)))
case('K-LAI-3', 'vân dùng có lỗi chắc → (b)', bad(LA.check116(E, mk_tl(E), EP, None)['K-LAI-3'], 'b'), True)
K2 = copy.deepcopy(KV); K2['tep'][0]['ket_luan'] = 'dùng nếu đạt kiểm trôi'
E = ep(lai=dict(E0['lai'], kiem_du_kien_van=tmpf('kv2.json', K2)))
case('K-LAI-3', 'kết luận "dùng nếu …" chưa ghi dieu_kien_dat → THIẾU (d)', thieu(LA.check116(E, mk_tl(E), EP, None)['K-LAI-3']), True)
K2['tep'][0]['dieu_kien_dat'] = True; E = ep(lai=dict(E0['lai'], kiem_du_kien_van=tmpf('kv2b.json', K2)))
case('K-LAI-3', '"dùng nếu …" + dieu_kien_dat: true → sạch', bad(LA.check116(E, mk_tl(E), EP, None)['K-LAI-3']), False)
K3 = copy.deepcopy(KV); K3['tep'][0]['nghi_van'] = ['rong chân tường có thể quá cao']
E = ep(lai=dict(E0['lai'], kiem_du_kien_van=tmpf('kv3.json', K3))); rr = LA.check116(E, mk_tl(E), EP, None)
case('K-LAI-3V', 'vân dùng còn ghi nghi vấn → K-LAI-3V (Cảnh báo); K-LAI-3 vẫn sạch', bad(rr['K-LAI-3V']) + ([] if not bad(rr['K-LAI-3']) else ['K-LAI-3 bẩn']), True)
case('cap', 'K-LAI-3V ở animatic → Cảnh báo (K116-D5)', cap112.cap('K-LAI-3V', dict(rr['K-LAI-3V'], cong='animatic'))[1], False)
case('cap', 'K-LAI-3V ở cổng G2 (bản phát hành) → Chặn (K116-D5)', cap112.cap('K-LAI-3V', dict(rr['K-LAI-3V'], cong='G2'))[1], True)
G = [json.loads(l) for l in open(os.path.join(EP, 'lai', 'goi-api-van.jsonl'))]; G[0]['input'].pop('mask_frac')
E = ep(lai=dict(E0['lai'], goi_api_van=tmpf('gv.jsonl', G, jsonl=True)))
case('K-LAI-6', 'vân: không có % mặt nạ (không mask_frac, không mask: null) → lỗi', bad(LA.check116(E, mk_tl(E), EP, None)['K-LAI-6']), True)
# dữ liệu THẬT V6 (đoạn thử, chỉ vân HC7) — trước (1.15) / sau (1.16)
V6 = os.path.join(D, 'v6'); EV6 = dict(id='v6', khung_sach=True, segments=[], lai=dict(log_khung='lai/log-khung.jsonl', kiem_du_kien='pt3/kiem-du-kien.json',
                                                                                       goi_api='pt3/goi-api.jsonl', log_chu='lai/log-chu.jsonl'))
old, new = LA.check(EV6, None, V6, None), LA.check116(EV6, None, V6, None)
INFO.append('V6 thật 1.15: ' + ' · '.join(f"{k} {v.get('ket_qua') or ('ĐẠT' if v['ok'] else 'TRƯỢT')}" for k, v in old.items()))
INFO.append('V6 thật 1.16: ' + ' · '.join(f"{k} {v.get('ket_qua') or ('ĐẠT' if v['ok'] else 'TRƯỢT')}" for k, v in new.items()) + f" · K-LAI-3: {new['K-LAI-3']['val']}")
case('K-LAI-5', 'V6 thật 1.15: K-LAI-5 lỗi "133 lệnh sinh > 1 + 2" (hành vi cũ giữ nguyên)', bad(old['K-LAI-5'], 'b'), True)
case('K-LAI-5', 'V6 thật 1.16: chỉ vân → K-LAI-4/5/B KHÔNG ÁP', sum((khong_ap(new[k]) for k in ('K-LAI-4', 'K-LAI-5', 'K-LAI-B')), []), False)
case('K-LAI-6', 'V6 thật 1.16: 133 lệnh PT3 đủ trường (mask_frac) → sạch', bad(new['K-LAI-6']), False)
case('K-LAI-3', 'V6 thật 1.16: 55 tệp "dùng nếu đạt kiểm trôi" chưa xác nhận → THIẾU', thieu(new['K-LAI-3']), True)
case('K-LAI-3V', 'V6 thật 1.16: 65 tệp vân dùng còn ghi nghi vấn → Cảnh báo', bad(new['K-LAI-3V']), True)
case('K-LAI-2', 'V6 thật 1.16: nhãn AI vẫn vẽ trên hình (log ai_label) → (e)', bad(new['K-LAI-2'], 'e'), True)

# ================================================================ NC-H5 1.16 (khiếu nại A-G1B-2)
r0 = K6.nch5(E0, mk_tl(E0), EP)
case('NC-H5', f"bộ đếm tl/* được nhận; nam_khung đúng; ghost có nguồn trong mô tả — {r0['val']}", bad(r0), False)
E = ep(nam_khung=tmpf('nk.json', [dict(shot='C00', nam_dem=1704, nam_max=dict(nha=1720))]))
case('NC-H5', 'lớp nhà năm 1720 > bộ đếm 1704 → (a)', bad(K6.nch5(E, mk_tl(E), EP), 'a'), True)
case('NC-H5', 'không có nam_khung → THIẾU (a) (Chặn)', thieu(K6.nch5(ep(nam_khung=None), mk_tl(E0), EP)), True)
E = ep(ghost={'ghost-1782': {'nguon': 'Montero plan 1860'}})
case('NC-H5', 'nguồn ghost không có trong mô tả → (b)', bad(K6.nch5(E, mk_tl(E), EP), 'b'), True)
E = ep(); E['heroes'] = {k: dict(v, hero='relief/x', opt={}) for k, v in E['heroes'].items()}
case('NC-H5', 'không có bộ đếm → KHÔNG ÁP', khong_ap(K6.nch5(E, mk_tl(E), EP)), False)

# ================================================================ BD-3 1.16 (khiếu nại A-G1B-3)
r0 = K6.bd3(E0, mk_tl(E0), EP, None)
case('BD-3', f"lớp ranh có nam + nguồn, nguồn trong mô tả, không nhãn trên hình — {r0['val'][:60]}", bad(r0), False)
E = ep(phat_hanh=dict(mo_ta=tmpf('mt2.md', 'AI use = Yes. Sources: Spilsbury plan 1782; OSM.\n')))
case('BD-3', 'nguồn ranh (Cliopatria) không có trong mô tả → (b)', bad(K6.bd3(E, mk_tl(E), EP, None), 'b'), True)
LG = os.path.join(TMP, 'logs'); os.makedirs(LG, exist_ok=True)
json.dump(dict(id='C01', fmt='16x9', text=[dict(f=12, items=[dict(s='approx. borders c. 1704 — Cliopatria', cap=30.0, alpha=1.0)])]), open(os.path.join(LG, 'C01.log.json'), 'w'))
case('BD-3', 'nhãn "approx. borders" hiện trên hình → (c) §12.1', bad(K6.bd3(E0, mk_tl(E0), EP, LG), 'c'), True)
LP = json.load(open(os.path.join(EP, 'lop.json'))); LP['lop'][0]['nguon'] = ''
E = ep(ban_do=dict(lop=tmpf('lop.json', LP)))
case('BD-3', 'manifest lớp ranh thiếu nguồn → (a)', bad(K6.bd3(E, mk_tl(E), EP, None), 'a'), True)

# ================================================================ Q26b theo vùng (khiếu nại A-G1B-4)
TL = mk_tl(E0); q_old, q_new = QS.q26b(TL, E0), QS.q26b(TL, E0, v116=True)
case('Q26b', f"1.16 cảnh tl/fx theo vùng: {q_new['val'][:70]}", q_new['loi'], False)
case('Q26b', f"hành vi cũ (v116 tắt): một mô-đun tl/fx = một bối cảnh → lỗi: {q_old['val'][:50]}", q_old['loi'], True)
E = ep()
for s in E['segments']: s['shots'][0]['vung'] = 'eo'
case('Q26b', '1.16, mọi shot cùng một vùng → lỗi (vẫn bắt lặp bối cảnh thật)', QS.q26b(mk_tl(E), E, v116=True)['loi'], True)

# ================================================================ Q37 miễn khung neo / im lặng (khiếu nại A-G1B-5)
def q37e(durs, flags):
    E = dict(id='q', khung_sach=True, segments=[dict(id=f'S{i}', dur=d, beats=[dict(t=0.0, k='cut', s='c')], shots=[dict(tpl='plate', at=0, type='scene3d', p={}, **fl)])
                                             for i, (d, fl) in enumerate(zip(durs, flags))])
    return E, NH.q37(E, None, mien=K6.q37_mien(E, None))
E, qa = q37e([5, 8, 5], [{}, dict(khung_neo=True), {}])
case('Q37', f"khung neo 8 s → khoảng 8 s được miễn (c) — {qa['val'][-60:]}", bad(qa, 'c'), False)
case('Q37', 'cùng tập, không miễn (hành vi cũ) → (c) 8 s > 6 s', bad(NH.q37(E, None), 'c'), True)
E, qb = q37e([5, 11, 5], [{}, dict(khung_neo=True), {}])
case('Q37', 'khung neo 11 s > 10 s → (c)', bad(qb, 'c'), True)
E, qc = q37e([5, 9, 5, 9, 5, 9, 5], [{}, dict(im_lang=True), {}, dict(im_lang=True), {}, dict(im_lang=True), {}])
case('Q37', '3 tấm im lặng > 2/tập → (c)', bad(qc, 'c'), True)
E, qd = q37e([5, 9, 5, 8, 5], [{}, dict(im_lang=True), {}, dict(neo=True), {}])
case('Q37', '1 tấm im lặng 9 s + khung neo 8 s (khai neo: true) → sạch (c)', bad(qd, 'c'), False)
E, qe = q37e([5, 8, 5], [{}, {}, {}])
case('Q37', 'shot 8 s thường (không khai) → vẫn (c)', bad(qe, 'c'), True)

# ================================================================ A* (khiếu nại A-V6-2, A-G1B-7)
TLA = dict(segments=[dict(id='a', t0=0.0, dur=30.0, shots=[])], tong_s=30.0); MX = dict(cong_cu='scripts/audio/master.py')
a_old = AM.check(dict(id='x'), TLA, master=None, MX=MX, asr=False)
a_new = AM.check(dict(id='x'), TLA, master=None, MX=MX, asr=False, v116=True)
case('A*', 'hành vi cũ: không lời → A4 lỗi "không có stem"', [x for x in a_old['loi'] if x.startswith('A4')], True)
case('A*', '1.16 không lời: A4, A8, A9, A10, A13 KHÔNG ÁP', [x for x in a_new['loi'] if x.split()[0] in AM.LOI_MUC], False)
case('A*', '1.16 không lời: A1/A2/A5/A7 (master) vẫn áp → lỗi khi thiếu master', [x for x in a_new['loi'] if x.startswith('A1')], True)
a_an = AM.check(dict(id='x', animatic=True), TLA, master=None, MX=MX, asr=False, v116=True)
case('A*', '1.16 animatic: true → CHỈ BÁO', [] if a_an['ket_qua'] == 'CHỈ BÁO' else [a_an['ket_qua']], False)
TLS = dict(segments=[dict(id='a', t0=0.0, dur=30.0, shots=[], speech=[[1.0, 20.0]])], tong_s=30.0)
a_sp = AM.check(dict(id='x'), TLS, master=None, MX=MX, asr=False, v116=True)
case('A*', '1.16 có lời mà không stem → A4 vẫn lỗi', [x for x in a_sp['loi'] if x.startswith('A4')], True)

# ================================================================ ML1 đọc lời khoá (trả lời "tên trường ML1")
C = K6.cau_tu_loi_khoa(E0['loi_khoa'])
m1 = MA.ml1(E0, mk_tl(E0), C, EP, claims=K6.claims_file(E0, EP))
case('ML1', f"lời khoá {len(C)} câu: shot C01 khai `cau` (≥ 12 ký tự đầu câu) gắn được — {m1['val']}", [x for x in m1['loi'] if x.startswith('C01') or '(c)' in x], False)
E = ep(); shot(E, 'C01')['cau'] = 'This sentence is not in the locked script.'
case('ML1', '`cau` không có trong lời khoá → (c)', MA.ml1(E, mk_tl(E), C, EP)['muc']['c'], True)

# ================================================================ cả bộ trên fixture T3
R6 = K6.check(E0, mk_tl(E0), EP, None)
INFO.append('q_k116.check fixture T3: ' + ' · '.join(f"{k} {v.get('ket_qua') or ('ĐẠT' if v['ok'] else 'TRƯỢT')}" for k, v in R6.items()))

# ================================================================ kết quả
ok = all(x[3] for x in R)
by = {}
for x in R: by.setdefault(x[0], []).append(x)
miss = [k for k, v in by.items() if k not in ('cap', 'cổng') and not (any(y[2] == 'sạch' for y in v) and any(y[2] == 'bắt lỗi' for y in v))]
for rule, name, kind, good, got in R:
    print(f"{'OK ' if good else 'SAI'} [{rule}] ({kind}) {name}" + ('' if good else f'  → {got}'))
print('\n'.join(INFO))
print(f"\nselftest 1.16: {sum(1 for x in R if x[3])}/{len(R)} đúng kỳ vọng · {len(by)} nhóm · " + ', '.join(f'{k} {len(v)}' for k, v in by.items())
      + f" · luật thiếu ca đạt hoặc trượt: {', '.join(miss) or 'không'}")
shutil.rmtree(TMP, ignore_errors=True)
sys.exit(0 if ok and not miss else 1)
