#!/opt/cine/bin/python
"""Tự kiểm luật 1.17.2 (phiên K-1.17.2, 22/10/2026; quyết định chủ dự án 22/10/2026 11:09 — duyệt V2-D1…D8, không nhãn/câu AI trong phim):
MINH-HOA theo đoạn khai + bỏ nhãn bắt buộc, K-LAI-1…6 đọc đoạn AI khai trong log shot (V2-D5), PP-1 (d) không đòi câu AI, CONG-BO-1 (mới),
TL-1 miễn cắt góc R3 (V2-D7), EO-DAT-R1 chỉ báo + vùng nở (V2-D2). Mỗi luật đổi ≥ 1 ca ĐẠT + ≥ 1 ca TRƯỢT. KHÔNG gọi mạng/API.

Dữ liệu thật: fixtures/k1172/v2-log-shot.json = log shot animatic T3 v2 (nhánh k2c-t3-anim-v2 @18a5f33d,
channel-k2/k2c-t3-01/animatic/log-shot.json SHA b4431a06…; RÚT GỌN còn các trường luật đọc: shot, t0, t1, dur, goc, noi, tl, minh_hoa
[ma, t0, t1, minh_hoa], ai_image, ai_texture, agl_m, cam[].t, cat_trong_shot, chuong, diem_may, moc) và fixtures/k1172/v2-so-ai-gemini.jsonl =
sổ AI Gemini Omni nguyên văn (reports/animatic-t3-v2/so-ai-gemini.jsonl, SHA f935f48a…). Video thử TL-1: fixtures/k116/vid/v-cat.mp4.

  /opt/cine/bin/python checks/ll/selftest_k1172.py      mã thoát 0 = mọi ca đúng kỳ vọng
"""
import copy, json, os, sys, tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, ROOT)
from checks.ll import q_k117 as K7, q_k116 as K6, q_lai as LA, cap112  # noqa: E402

FX = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures')
D = os.path.join(FX, 'k1172'); TMP = tempfile.mkdtemp(prefix='k1172-')
R, INFO = [], []


def case(rule, name, got, expect_fail):
    got = list(got) if got else []
    R.append((rule, name, 'bắt lỗi' if expect_fail else 'sạch', bool(got) == expect_fail, got[:2]))


def bad(x, *muc):
    L = x['loi'] + (x.get('thieu') or [])
    return [y for y in L if not muc or any(y.startswith(f'({m})') or f'] ({m})' in y for m in muc)]


def kq(x, want): return [] if x.get('ket_qua') == want else [f'kết quả {x.get("ket_qua")!r} ≠ {want!r}: {x.get("val")}']


def wj(name, obj):
    p = os.path.join(TMP, name)
    with open(p, 'w') as f:
        if name.endswith('.jsonl'): f.write(''.join(json.dumps(x, ensure_ascii=False) + '\n' for x in obj))
        else: json.dump(obj, f, ensure_ascii=False)
    return p


# ======================================================================== MINH-HOA (1.17.2: theo ĐOẠN khai, bỏ nhãn)
SO = dict(model_req='gemini-omni-1.1-flash', prompt='An eye-level documentary illustration of a dusty track …', tag='M2-l3', output=dict(file='M2-l3.mp4', sha256='bb' * 32))
EM = dict(id='t3', khung_sach=True, segments=[dict(id=s, dur=d) for s, d in (('A', 40), ('C', 20), ('B', 40))])


def LSd(doan=None, goc_c='cao', goc_a='cao', goc_b='cao', **kw):
    """shot C 40–60 s (góc goc_c) có danh sách đoạn minh hoạ (mặc định M2 4–12 s trong shot, máy 4 m theo cam[i] ↔ agl_m[i])"""
    c = dict(shot='C', t0=40, t1=60, dur=20, goc=goc_c, ai_image=True, cam=[dict(t=0), dict(t=3.98), dict(t=4.0), dict(t=11.98), dict(t=12.0), dict(t=20.0)],
             agl_m=[217, 217, 4, 4, 218, 218], minh_hoa=[dict(ma='M2', t0=4.0, t1=12.0, minh_hoa=True, luot='M2-l3')] if doan is None else doan); c.update(kw)
    return [dict(shot='A', t0=0, t1=40, dur=40, goc=goc_a, ai_image=False), c, dict(shot='B', t0=60, t1=100, dur=40, goc=goc_b, ai_image=False)]


SOP = wj('so-ai.jsonl', [SO])
mh = lambda LS, E=None: K7.minh_hoa(dict(EM, so_ai=SOP) if E is None else E, None, LS, TMP)
r0 = mh(LSd()); INFO.append(f"MINH-HOA ca chuẩn: {r0['val']}")
case('MINH-HOA', 'đoạn M2 8 s TRONG shot 3D, máy 4 m (cam↔agl_m), sổ AI khớp luot, KHÔNG nhãn, KHÔNG log chữ → sạch', bad(r0), False)
case('MINH-HOA', 'shot có minh_hoa: [] (log V2) → KHÔNG ÁP', kq(mh(LSd(doan=[]), EM), 'KHÔNG ÁP'), False)
case('MINH-HOA', 'đoạn 25 s (2 đoạn 12,5 s) = 25 % > 20 % → (a)', bad(mh(LSd(doan=[dict(ma='M2', t0=0, t1=12.5, luot='M2-l3'), dict(ma='M3', t0=7.5, t1=20, so_ai=SO)])), 'a'), True)
case('MINH-HOA', 'đoạn đúng 20 s = 20 % → sạch (a)', bad(mh(LSd(doan=[dict(ma='M2', t0=0, t1=20, luot='M2-l3')], agl_m=None)), 'a'), False)
case('MINH-HOA', '1.17.2 đo theo ĐOẠN: hai shot kề là thẻ phẳng nhưng đoạn nằm giữa shot 3D (khung 3D trước + sau cùng shot) → sạch (c)',
     bad(mh(LSd(goc_a='phang', goc_b='phang')), 'c'), False)
case('MINH-HOA', 'đoạn bắt đầu đầu shot C, shot A trước là thẻ phẳng → (c)', bad(mh(LSd(doan=[dict(ma='M2', t0=0, t1=8, luot='M2-l3')], goc_a='phang')), 'c'), True)
case('MINH-HOA', 'đoạn kết cuối shot C, shot B sau là 3D → sạch (c)', bad(mh(LSd(doan=[dict(ma='M2', t0=12, t1=20, luot='M2-l3')])), 'c'), False)
case('MINH-HOA', 'hai đoạn liền nhau 4–8 s + 8–12 s (không khung 3D giữa) → (c)', bad(mh(LSd(doan=[dict(ma='M2', t0=4, t1=8, luot='M2-l3'), dict(ma='M3', t0=8, t1=12, so_ai=SO)])), 'c'), True)
case('MINH-HOA', 'đoạn ở cuối phim (shot cuối, không khung sau) → (c)',
     bad(mh(LSd()[:2] + [dict(shot='B', t0=60, t1=100, dur=40, goc='cao', minh_hoa=[dict(ma='M4', t0=30, t1=40, so_ai=SO)])]), 'c'), True)
case('MINH-HOA', 'AGL theo cam: đoạn 4–12 s (4 m) dù shot có góc 217 m → sạch (d)', bad(mh(LSd()), 'd'), False)
case('MINH-HOA', 'AGL theo cam: đoạn 12–20 s (218 m) → (d)', bad(mh(LSd(doan=[dict(ma='M2', t0=12, t1=20, luot='M2-l3')])), 'd'), True)
case('MINH-HOA', 'agl_m của mục đoạn (60 m) ưu tiên → (d)', bad(mh(LSd(doan=[dict(ma='M2', t0=4, t1=12, luot='M2-l3', agl_m=60)])), 'd'), True)
case('MINH-HOA', 'không sổ AI → (e)', bad(mh(LSd(), EM), 'e'), True)
case('MINH-HOA', 'sổ AI dòng tag khác (M9-l1) → (e)', bad(mh(LSd(), dict(EM, so_ai=wj('so9.jsonl', [dict(SO, tag='M9-l1')]))), 'e'), True)
case('MINH-HOA', 'dòng sổ thiếu SHA đầu ra → (e)', bad(mh(LSd(), dict(EM, so_ai=wj('so-nosha.jsonl', [dict(SO, output={})]))), 'e'), True)
case('MINH-HOA', 'sổ AI không khai luot: khớp tag "M2-…" theo mã đoạn → sạch (e)',
     bad(mh(LSd(doan=[dict(ma='M2', t0=4, t1=12)]), dict(EM, so_ai=SOP)), 'e'), False)
mt = mh(LSd(ai_image=False), EM)
case('MINH-HOA', 'đoạn khai ở shot ai_image: false (như C4/M1) → không đo (KHÔNG ÁP, nêu tên) — lỗi ở K-LAI-2 (b)',
     kq(mt, 'KHÔNG ÁP') + ([] if 'C/M2' in mt['val'] else ['không nêu đoạn mâu thuẫn']), False)
mo, ch, cb = cap112.cap('MINH-HOA', dict(mh(LSd(goc_a='phang', doan=[dict(ma='M2', t0=0, t1=8, luot='M2-l3')])), cong='G2'))
case('cấp', 'MINH-HOA (c) ở G2 → Chặn', ch, True)
mo, ch, cb = cap112.cap('MINH-HOA', dict(mh(LSd(goc_a='phang', doan=[dict(ma='M2', t0=0, t1=8, luot='M2-l3')])), cong='animatic'))
case('cấp', 'MINH-HOA (c) ở animatic → Cảnh báo', ch, False)
# SACH-1 KHÔNG đổi: vẫn theo SHOT có minh_hoa
case('SACH-1', 'SACH-1 không đổi: _mh_spans vẫn trả cả shot có minh_hoa (C 40–60 s)', [] if K7._mh_spans(LSd()) == [('C', 40.0, 60.0)] else [str(K7._mh_spans(LSd()))], False)

# ---- log thật animatic T3 v2 (V2-D5)
LV2 = json.load(open(os.path.join(D, 'v2-log-shot.json'))); E2 = dict(id='k2c-t3-anim', khung_sach=True)
DS, MT = K7.doan_ai(LV2)
case('V2-D5', 'log V2 thật: 4 đoạn M5 (H1), M3 (N1.4), M2 (C3), M4 (C5) = 28,4 s; C4/M1 (ai_image false) là mâu thuẫn',
     [] if [d['id'] for d in DS] == ['H1/M5', 'N1_4/M3', 'C3/M2', 'C5/M4'] and abs(sum(d['b'] - d['a'] for d in DS) - 28.4) < 0.01 and [d['id'] for d in MT] == ['C4/M1']
     else [f"{[d['id'] for d in DS]} {sum(d['b'] - d['a'] for d in DS):.2f} {[d['id'] for d in MT]}"], False)
rv2 = K7.minh_hoa(E2, None, LV2, D); INFO.append(f"MINH-HOA log V2 (không sổ AI): {rv2['val']}")
case('V2-D5', 'log V2: (a) 28,4 s / 761 s = 3,7 % ≤ 20 %, (c) 4/4 kẹp giữa 2 khung 3D, (d) 4/4 ≤ 40 m → sạch (a)(c)(d)', bad(rv2, 'a', 'c', 'd'), False)
case('V2-D5', 'log V2 chưa nối sổ AI (episode.yaml không so_ai:) → (e) ×4', [] if len(bad(rv2, 'e')) == 4 else bad(rv2, 'e') or ['0 lỗi (e)'], False)
rv2s = K7.minh_hoa(dict(E2, so_ai=os.path.join(D, 'v2-so-ai-gemini.jsonl')), None, LV2, D); INFO.append(f"MINH-HOA log V2 + sổ Gemini thật: {rv2s['val']}")
case('V2-D5', 'log V2 + sổ Gemini thật (khớp tag M2-…/M3-…/M4-…/M5-…; model_req, prompt, output.sha256) → sạch (e)', bad(rv2s, 'e'), False)

# ======================================================================== K-LAI (V2-D5: đoạn AI khai trong log shot)
ET = dict(id='t3', khung_sach=True, segments=[dict(id=s, dur=d, shots=[dict(tpl='plate', at=0, type='scene3d', p=dict(sach=True))]) for s, d in (('A', 40), ('C', 20), ('B', 40))])
case('K-LAI', 'ap_dung: không khối lai, đặc tả không ai_image, log shot có đoạn → ÁP', [] if LA.ap_dung(ET, LSd()) else ['không áp'], False)
case('K-LAI', 'ap_dung: log shot không đoạn, không ai_image → KHÔNG ÁP', ['áp'] if LA.ap_dung(ET, LSd(doan=[], ai_image=False)) else [], False)
case('K-LAI', 'ap_dung tập cũ (k2check không truyền log shot) → như 1.16 (KHÔNG ÁP)', ['áp'] if LA.ap_dung(ET) else [], False)
KM = wj('kiem-ok.json', dict(tag='M2-l3', ket_luan_may=dict(loi_mo_hinh=0, ket_qua='ĐẠT')))
KB = wj('kiem-loi.json', dict(tag='M2-l1', ket_luan_may=dict(loi_mo_hinh=17, ket_qua='LOẠI')))
GA = wj('so-gemini.jsonl', [json.loads(l) for l in open(os.path.join(D, 'v2-so-ai-gemini.jsonl'))])


def lai(LS, E=None):
    return LA.check116(ET if E is None else E, None, TMP, None, LS)


LK = lai(LSd(doan=[dict(ma='M2', t0=4, t1=12, luot='M2-l3', kiem=KM)]), dict(ET, so_ai=GA)); INFO.append('K-LAI log shot: ' + ' · '.join(f"{k} {v.get('ket_qua') or ('ĐẠT' if v['ok'] else 'TRƯỢT')}" for k, v in LK.items()))
case('K-LAI-1', f"đoạn 8 s / 100 s = 8 % (từ log shot) → sạch — {LK['K-LAI-1']['val'][:80]}", bad(LK['K-LAI-1']), False)
case('K-LAI-1', 'đoạn 22 s / 100 s = 22 % > 20 % → lỗi', bad(lai(LSd(doan=[dict(ma='M2', t0=0, t1=20), ]) + [dict(shot='X', t0=100, t1=102, dur=2, ai_image=True)],
                                                           dict(ET, segments=ET['segments'] + [dict(id='X', dur=2, shots=[])]))['K-LAI-1']) if False else
     bad(LA.klai1_log(*LA.log_ai(LSd(doan=[dict(ma='M2', t0=0, t1=20)]) + [dict(shot='X', t0=100, t1=102, dur=2, ai_image=True)])[:2], 100.0, 'thử')), True)
case('K-LAI-2', 'đoạn khai, shot ai_image: true, mọi shot có cờ → sạch (a)(b)', bad(LK['K-LAI-2'], 'a', 'b'), False)
LNF = LSd(); [x.pop('ai_image') for x in (LNF[0], LNF[2])]
case('K-LAI-2', 'không log khung, 2 shot log thiếu cờ ai_image → THIẾU (a)', bad(lai(LNF)['K-LAI-2'], 'a'), True)
case('K-LAI-2', 'đoạn khai ở shot ai_image: false (C4/M1 V2) → (b) mâu thuẫn khai', bad(lai(LSd(ai_image=False))['K-LAI-2'], 'b'), True)
case('K-LAI-2', '1.17.2: không đòi thẻ PP nói AI (đặc tả không có thẻ PP) → không có (c)', bad(LK['K-LAI-2'], 'c'), False)
case('K-LAI-3', 'đoạn có tệp kiểm (ket_luan_may ĐẠT, 0 lỗi mô hình) → sạch', bad(LK['K-LAI-3']), False)
case('K-LAI-3', 'tệp kiểm LOẠI (17 lỗi) mà vẫn dùng → (b)', bad(lai(LSd(doan=[dict(ma='M2', t0=4, t1=12, kiem=KB)]))['K-LAI-3'], 'b'), True)
case('K-LAI-3', 'đoạn không có tệp kiểm → THIẾU', kq(lai(LSd())['K-LAI-3'], 'THIẾU'), False)
case('K-LAI-4/5/B', 'chỉ minh hoạ → KHÔNG ÁP có lý do nêu đoạn (không phải "không có khối lai / shot AI")',
     sum((kq(LK[k], 'KHÔNG ÁP') + ([] if 'đoạn minh hoạ' in LK[k]['val'] else [LK[k]['val']]) for k in ('K-LAI-4', 'K-LAI-5', 'K-LAI-B')), []), False)
case('K-LAI-6', 'sổ Gemini thật (c2pa dict → co_manifest, file/sha từ output, mặt nạ = toàn khung) → sạch', bad(LK['K-LAI-6']), False)
GB = wj('so-thieu.jsonl', [dict(json.loads(open(os.path.join(D, 'v2-so-ai-gemini.jsonl')).readline()), prompt='short')])
case('K-LAI-6', 'dòng sổ prompt < 40 ký tự (không nguyên văn) → lỗi', bad(lai(LSd(), dict(ET, so_ai=GB))['K-LAI-6']), True)
case('K-LAI-6', 'không có sổ AI → THIẾU', kq(lai(LSd())['K-LAI-6'], 'THIẾU'), False)
LV = LA.check116(dict(id='k2c-t3-anim', khung_sach=True), None, D, None, LV2)
case('V2-D5', 'log V2 thật: không hàng K-LAI nào báo "tập không có khối lai / shot AI"', [k for k, v in LV.items() if 'không có khối lai' in str(v.get('val'))], False)
case('V2-D5', 'log V2 thật: K-LAI-2 (b) bắt C4/M1 mâu thuẫn', [] if any('C4/M1' in x for x in bad(LV['K-LAI-2'], 'b')) else ['không bắt'], False)
case('V2-D5', 'log V2 thật: K-LAI-1 28,4 s = 3,7 % ≤ 20 %', bad(LV['K-LAI-1']), False)
INFO.append('K-LAI log V2: ' + ' · '.join(f"{k} {v.get('ket_qua') or ('ĐẠT' if v['ok'] else 'TRƯỢT')}" for k, v in LV.items()))

# ======================================================================== PP-1 (d) 1.17.2
EP = os.path.join(FX, 'k116', 'ep-t3')
import yaml  # noqa: E402
E0 = yaml.safe_load(open(os.path.join(EP, 'episode.yaml')))
TL0 = lambda E: dict(segments=[dict(id=s['id'], t0=sum(x['dur'] for x in E['segments'][:i]), dur=s['dur'], part=s.get('part'),
                                    shots=[dict(tpl=sh['tpl'], t0=0.0, t1=s['dur'], type=sh.get('type'), p=sh.get('p') or {}) for sh in s['shots']]) for i, s in enumerate(E['segments'])],
                     tong_s=sum(x['dur'] for x in E['segments']))


def pp(items1, items2):
    E = copy.deepcopy(E0)
    for k, it in ((-2, items1), (-1, items2)): E['segments'][k]['shots'][0]['p']['card'].update(title='How this film was made', items=[dict(s=x) for x in it])
    return K6.pp1(E, TL0(E))


case('PP-1', '(d) mới: nguồn/bản đồ + chỗ ước tính, KHÔNG câu AI → sạch (d)', bad(pp(['Built from British and Spanish records and period maps.'], ['Estimated: 1782 ruins, camps, heights.']), 'd'), False)
case('PP-1', '(d) mới: không nói nguồn/bản đồ → (d)', bad(pp(['Everything you saw.'], ['Estimated: 1782 ruins, camps, heights.']), 'd'), True)
case('PP-1', '(d) mới: không nói chỗ ước tính → (d)', bad(pp(['Built from British records and period maps.'], ['Troops shown in number and layout.']), 'd'), True)
case('PP-1', 'thẻ có câu AI vẫn hợp lệ (không thêm luật cấm chữ)', bad(pp(['Built from records and maps.'], ['Estimated: heights. AI retouched two frames.']), 'd'), False)

# ======================================================================== CONG-BO-1 (mới)
MT_OK = wj('mo-ta-ok.md', ['Narration: synthetic voice. Segments labelled "Illustration" are fully AI-generated and carry no location facts.']) if False else None
open(os.path.join(TMP, 'mo-ta-ok.md'), 'w').write('Gibraltar.\nNarration: synthetic voice. Short scenes are fully AI-generated illustrations and carry no location facts.\n')
open(os.path.join(TMP, 'mo-ta-khong.md'), 'w').write('Gibraltar, 1704–2026. Built from British and Spanish records and period maps.\n')
open(os.path.join(TMP, 'mo-ta-giong.md'), 'w').write('Narration: synthetic voice.\n')
EC = lambda **ph: dict(id='t3', khung_sach=True, phat_hanh=ph)
cb = lambda E, LS=None: K7.cong_bo1(E, LSd() if LS is None else LS, TMP)
case('CONG-BO-1', 'tập không khung AI, không giọng tổng hợp → KHÔNG ÁP', kq(cb(EC(), LSd(doan=[], ai_image=False)), 'KHÔNG ÁP'), False)
case('CONG-BO-1', 'đoạn minh hoạ + mô tả có câu "AI" + youtube_altered_content: true → sạch', bad(cb(EC(mo_ta='mo-ta-ok.md', youtube_altered_content=True))), False)
case('CONG-BO-1', 'mô tả không có câu "AI"/"synthetic" → (a)', bad(cb(EC(mo_ta='mo-ta-khong.md', youtube_altered_content=True)), 'a'), True)
case('CONG-BO-1', 'youtube_altered_content: false → (b)', bad(cb(EC(mo_ta='mo-ta-ok.md', youtube_altered_content=False)), 'b'), True)
case('CONG-BO-1', 'không khai youtube_altered_content → THIẾU (b)', bad(cb(EC(mo_ta='mo-ta-ok.md')), 'b'), True)
case('CONG-BO-1', 'không khai phat_hanh.mo_ta → THIẾU (a)', bad(cb(EC(youtube_altered_content=True)), 'a'), True)
case('CONG-BO-1', 'chỉ giọng tổng hợp (vo.engine: ElevenLabs), mô tả "synthetic voice" + cờ → sạch',
     bad(cb(dict(EC(mo_ta='mo-ta-giong.md', youtube_altered_content=True), vo=dict(engine='ElevenLabs eleven_v4')), LSd(doan=[], ai_image=False))), False)
case('CONG-BO-1', 'chỉ giọng tổng hợp (giong_tong_hop: true), không cờ → (b)/THIẾU',
     bad(cb(dict(EC(mo_ta='mo-ta-giong.md'), giong_tong_hop=True), LSd(doan=[], ai_image=False)), 'b'), True)
x = dict(cb(EC(mo_ta='mo-ta-khong.md', youtube_altered_content=False)), cong=K7.cong_cb(EC()))
case('cấp', 'CONG-BO-1 lỗi ở G2 → chỉ báo (không Chặn)', cap112.cap('CONG-BO-1', x)[1], False)
x = dict(cb(EC(mo_ta='mo-ta-khong.md', youtube_altered_content=False)), cong=K7.cong_cb(dict(EC(), cong='phat_hanh')))
case('cấp', 'CONG-BO-1 lỗi ở gói phát hành (cong: phat_hanh) → Chặn', cap112.cap('CONG-BO-1', x)[1], True)
x = dict(cb(EC(mo_ta='mo-ta-khong.md', youtube_altered_content=False, goi=True)), cong=K7.cong_cb(EC(goi=True)))
case('cấp', 'CONG-BO-1 lỗi ở gói phát hành (phat_hanh.goi: true) → Chặn', cap112.cap('CONG-BO-1', x)[1], True)
x = dict(cb(EC(mo_ta='mo-ta-ok.md', youtube_altered_content=True, goi=True)), cong='phat_hanh')
case('cấp', 'CONG-BO-1 đủ ở gói phát hành → 0 Chặn', cap112.cap('CONG-BO-1', x)[1], False)
case('CONG-BO-1', 'log V2 thật (đoạn minh hoạ, không phat_hanh) → THIẾU (a)(b) — chỉ báo ở G2', kq(K7.cong_bo1(E2, LV2, D), 'THIẾU'), False)

# ======================================================================== TL-1 (V2-D7: cắt góc R3 không tính trần)
VC = K6.video_gray(os.path.join(FX, 'k116', 'vid', 'v-cat.mp4'))   # 11 cắt: 3, 6, 9 | 12 | 15, 18, 21 | 24 | 27, 30, 33 (3 shot × 12 s)
EV = dict(id='vid', khung_sach=True, segments=[dict(id=f'V{k}', dur=12.0, beats=[dict(t=0, k='cut')], shots=[dict(tpl='plate', at=0, type='scene3d', p=dict(sach=True, hero='h'))]) for k in range(3)])
TLV = TL0(EV)
LVc = lambda **kw: [dict(dict(shot=f'V{k}', goc='cao', tl=True, diem_may=f'v{k}'), **kw) for k in range(3)]
r_ = K6.tl1(EV, TLV, LVc(so_goc=4), None, None, VC); INFO.append(f"TL-1 v-cat + so_goc 4: {r_['val'][:220]}")
case('TL-1', 'v-cat, mỗi shot so_goc: 4 → miễn 9 cắt góc trong shot → 2 cắt / 0,6 phút = 3,33 ≤ 5 → sạch (c)', bad(r_, 'c'), False)
case('TL-1', 'vẫn in số thô (11 cắt = 18,33/phút) cạnh số tính trần', [] if '18.33/phút (thô)' in r_['val'] and (r_.get('cat_video') or {}).get('r3') == 9 else [r_['val'][:200]], False)
case('TL-1', 'so_goc: 2 → chỉ miễn 1 cắt/shot → 8 cắt = 13,3/phút > 5 → (c)', bad(K6.tl1(EV, TLV, LVc(so_goc=2), None, None, VC), 'c'), True)
case('TL-1', 'goc_may 4 góc có t khớp (3, 6, 9 s trong shot) → sạch (c)',
     bad(K6.tl1(EV, TLV, LVc(goc_may=[dict(id='a'), dict(id='b', t=3), dict(id='c', t=6), dict(id='d', t=9)]), None, None, VC), 'c'), False)
case('TL-1', 'goc_may có t lệch (1, 2, 4 s) → không miễn → (c)',
     bad(K6.tl1(EV, TLV, LVc(goc_may=[dict(id='a'), dict(id='b', t=1), dict(id='c', t=2), dict(id='d', t=4.6)]), None, None, VC), 'c'), True)
case('TL-1', 'không khai so_goc/goc_may (như log V2: chỉ cat_trong_shot) → như 1.17.1 (c)', bad(K6.tl1(EV, TLV, LVc(cat_trong_shot=[3, 6, 9]), None, None, VC), 'c'), True)
case('TL-1', 'cắt ở ranh shot (12, 24 s) không bao giờ được miễn', [] if K6.cat_r3([(x, 12.0 * k, 12.0 * (k + 1)) for k, x in enumerate(LVc(so_goc=9))], [12.0, 24.0]) == [] else ['miễn ranh'], False)

# ======================================================================== EO-DAT-R1 (V2-D2: chỉ báo mọi cổng + vùng nở)
import cv2  # noqa: E402
import numpy as np  # noqa: E402
m = np.zeros((360, 640), np.uint8)
for x0 in range(40, 600, 40): m[150:330, x0:x0 + 2] = 255   # dòng người/lều mảnh: 14 vạch 2 px
for y0 in range(150, 330, 30): m[y0:y0 + 2, 40:600] = 255
MP = os.path.join(TMP, 'mat-na.png'); cv2.imwrite(MP, m)
tho, no = K7.vung_no(MP); INFO.append(f'vùng nở mặt nạ thử (vạch mảnh): pixel thô {tho} % · nở 1,5 % bề ngang {no} %')
case('EO-DAT-R1', 'vùng nở: mặt nạ vạch mảnh — pixel thô < 15 % nhưng vùng nở ≥ 20 %', [] if tho < 15 and no >= 20 else [f'{tho} / {no}'], False)
EE = dict(id='t3', khung_sach=True, segments=[dict(id='S1', dur=20)])
r1 = K7.eo_dat(EE, None, [dict(shot='S1', t0=0, t1=20, dur=20, noi='eo_dat', trong_pct=10, chu_the_eo_dat=True, chu_the_mat_na=MP)], ep_dir=TMP)['EO-DAT-R1']
INFO.append(f"EO-DAT-R1 mặt nạ: {r1['val']}")
case('EO-DAT-R1', 'K tự đo từ chu_the_mat_na: pixel thô < 15 % → (a) có ghi, kèm % vùng nở', [] if bad(r1, 'a') and 'vùng nở 1.5 % bề ngang' in bad(r1, 'a')[0] else [str(r1['loi'])], False)
case('cấp', 'EO-DAT-R1 (a) ở G2 → chỉ báo, không Chặn (V2-D2)', cap112.cap('EO-DAT-R1', dict(r1, cong='G2'))[1], False)
r2 = K7.eo_dat(EE, None, [dict(shot='S1', t0=0, t1=20, dur=20, noi='eo_dat', trong_pct=10, chu_the_eo_dat=True, chu_the_pct=22, chu_the_pct_no=41)])['EO-DAT-R1']
case('EO-DAT-R1', 'khai chu_the_pct 22 % + chu_the_pct_no 41 % → sạch, in cả hai số', bad(r2) + ([] if 'vùng nở 1.5 % bề ngang 41.0 %' in r2['val'] else [r2['val']]), False)
r3 = K7.eo_dat(EE, None, [dict(shot='S1', t0=0, t1=20, dur=20, noi='eo_dat', trong_pct=10, chu_the_eo_dat=True, chu_the_pct=12)])['EO-DAT-R1']
case('EO-DAT-R1', 'khai 12 % (không vùng nở) → (a) + ghi "vùng nở: chưa đo"', bad(r3, 'a') if 'chưa đo' in r3['val'] else ['thiếu ghi chưa đo'], True)

# ======================================================================== áp dụng: tập trước T3 không đổi
case('1.17.2 áp dụng', 'tập trước T3 → MINH-HOA/EO-DAT/CONG-BO-1 KHÔNG ÁP', sum((kq(v, 'KHÔNG ÁP') for v in K7.check(dict(id='t2')).values()), []), False)
case('1.17.2 áp dụng', 'q_k117.check có hàng CONG-BO-1', [] if 'CONG-BO-1' in K7.check(dict(id='t2')) else ['thiếu'], False)

# ======================================================================== kết quả
for rule, name, exp, ok, got in R: print(f"{'ĐÚNG' if ok else 'SAI '} [{rule}] {name} — kỳ vọng {exp}" + ('' if ok else f' · nhận {got}'))
print(); [print('  ' + x) for x in INFO]; print()
grp = {}
for rule, _, exp, ok, _ in R: grp.setdefault(rule, [0, 0, set()]); grp[rule][0] += ok; grp[rule][1] += 1; grp[rule][2].add(exp)
thieu = [k for k, v in grp.items() if k not in ('cấp', 'V2-D5', 'SACH-1', '1.17.2 áp dụng', 'K-LAI', 'K-LAI-4/5/B') and v[2] != {'sạch', 'bắt lỗi'}]
n = sum(ok for *_, ok, _ in R)
print(f"selftest 1.17.2: {n}/{len(R)} ca đúng kỳ vọng · " + ' · '.join(f'{k} {a}/{b}' for k, (a, b, _) in grp.items()) + f" · luật thiếu ca đạt hoặc trượt: {', '.join(thieu) or 'không'}")
sys.exit(0 if n == len(R) and not thieu else 1)
