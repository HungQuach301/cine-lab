#!/opt/cine/bin/python
"""Tự kiểm luật 1.17 (phiên K-1.17, 21/10/2026): N2P-1…6 (N2+, Kinh thánh §15, từ T4), MINH-HOA (§14.1 (c) / §15 M-d), EO-DAT-R1…R4 (§14.7; ngưỡng §14.7 nguyên văn từ 1.17.1) và các
khiếu nại animatic T3 chấp nhận (Q33 miễn năm khác — TL-1, ML1 `cau: ""`, NC-H1 lớp nhà tl/* — V7C-D5, SACH-1 nhãn Illustration). Mỗi luật ≥ 1 ca
ĐẠT + ≥ 1 ca TRƯỢT. Mặc định KHÔNG gọi mạng/API.

Dữ liệu: fixtures/k117/n2p/ = bản SAO THẬT kiểm có đáp án NC-N2P (reports/nc-n2p/kiem/dap-an, nhánh nc-n2p @9cb001d1): render cổng "cang"
(reports/nc-cpu/khung/A/cong-cang.jpg, SHA bf843596…), khung thử 6 lỗi chèn (khung-thu.jpg), mặt nạ ID (o1/mat-na/id-cang.png), đáp án
(dap-an.json), trả lời đã lưu của 2 mô hình nhìn (dap-an-vision.json, doi-chung-vision.json) và của q_thoi_dai (q_thoi_dai-ra.json).
Khung ghép (lớp (a) dán lại từ render) và video thử (v) dựng tại chỗ trong thư mục tạm.

  /opt/cine/bin/python checks/ll/selftest_k117.py            mã thoát 0 = mọi ca đúng kỳ vọng (không mạng)
  /opt/cine/bin/python checks/ll/selftest_k117.py --api <ra>  + chạy THẬT 2 mô hình nhìn + q_thoi_dai trên khung thử và đối chứng (có chi phí
                                                               đo 21/10: $0,37 = 2 mô hình $0,21 + q_thoi_dai $0,16; ghi <ra>/selftest-api.json) — dùng khi đổi mô hình/đề bài (§15 (c))
"""
import copy, json, os, subprocess, sys, tempfile

import yaml

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, ROOT)
from checks.ll import q_n2p as N, q_n2p_vision as QV, q_k117 as K7, q_k116 as K6, q_scene as QS, q_k2var as KV, q_mach as MA, q_noi as NO, cap112  # noqa: E402

FX = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures')
D = os.path.join(FX, 'k117', 'n2p'); TMP = tempfile.mkdtemp(prefix='k117-')
R = []
W, H = 1920, 1080


def case(rule, name, got, expect_fail):
    got = list(got) if got else []
    R.append((rule, name, 'bắt lỗi' if expect_fail else 'sạch', bool(got) == expect_fail, got[:2]))


def bad(x, *muc):
    L = x['loi'] + (x.get('thieu') or [])
    return [y for y in L if not muc or any(y.startswith(f'({m})') for m in muc)]


def kq(x, want): return [] if x.get('ket_qua') == want else [f'kết quả {x.get("ket_qua")!r} ≠ {want!r}']


# ======================================================================== N2+ — dựng khung ghép từ khung thử (việc phía dựng, không thuộc luật)
import cv2  # noqa: E402
import numpy as np  # noqa: E402

RJ, KJ, MJ = os.path.join(D, 'render.jpg'), os.path.join(D, 'khung-thu.jpg'), os.path.join(D, 'id-cang.png')
Rimg, Kimg = cv2.imread(RJ), cv2.imread(KJ)
Lb, NM = N.idmap(MJ, (W, H)); A = N.lop(Lb, NM, N.LOP_A)
G = Kimg.copy(); G[A] = Rimg[A]; GP = os.path.join(TMP, 'ghep.png'); cv2.imwrite(GP, G)
DA = json.load(open(os.path.join(D, 'dap-an.json')))
VA = json.load(open(os.path.join(D, 'dap-an-vision.json')))['ket_qua']; V0 = json.load(open(os.path.join(D, 'doi-chung-vision.json')))['ket_qua']
PAD = 40


def hit(b, hop):
    """cham_dap_an.py NC-N2P: tâm hộp báo trong hộp đáp án nở 40 px, hoặc tâm hộp đáp án trong hộp báo"""
    x0, y0, x1, y1 = b[0] * W, b[1] * H, b[2] * W, b[3] * H; cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    return (hop[0] - PAD <= cx <= hop[2] + PAD and hop[1] - PAD <= cy <= hop[3] + PAD) or (x0 <= (hop[0] + hop[2]) / 2 <= x1 and y0 <= (hop[1] + hop[3]) / 2 <= y1)


def kiem(ghep, V, anh_tinh=True):
    Dm = N.do_tam(RJ, ghep, MJ)
    L1, L2, L2b, L4, VU = N.ket_luan(V, Dm['_band'], Dm['_A'], anh_tinh, 1780)
    return dict(id='thu', shot='S1', nam=1780, anh_tinh=anh_tinh, do={k: v for k, v in Dm.items() if not k.startswith('_')}, V={'ket_qua': V}, L1=L1, L2=L2, L2b=L2b, L4=L4, VUNG=VU, Q=None)


def cham(K):
    nhom = {'thoi_dai': K['L2'], 'lop_a': K['L1'], 'dong_bang': K['L4']}; bat = {'gpt': 0, 'claude': 0, 'hop': 0}
    for v in DA['vat']:
        b = {mh: any(x['mh'] == mh and hit(x['toa_do'], v['hop']) for x in nhom[v['loai_loi']]) for mh in ('gpt', 'claude')}
        for mh in b: bat[mh] += int(b[mh])
        bat['hop'] += int(b['gpt'] or b['claude'])
    return bat


KA = kiem(GP, VA); T1 = N.tong_tam([KA])
B = cham(KA)
for mh in ('gpt', 'claude', 'hop'):
    case('N2P đáp án', f'{mh}: bắt {B[mh]}/6 lỗi chèn (NC-N2P: 6/6)', [] if B[mh] == 6 else [f'{B[mh]}/6'], False)
case('N2P-1', 'khung thử ghép: (a) lệch 0/255 trong lớp (a)', bad(T1['N2P-1'], 'a'), False)
case('N2P-1', 'khung thử: (b) vật lớp (a) mô hình báo (tàu L4, cờ L5)', bad(T1['N2P-1'], 'b'), True)
case('N2P-1', 'khung thử: (c) 2 cụm ΔE ≥ 30 trong dải 20 px (L5 cột cờ, L6 người) — số NC-N2P', [] if KA['do']['i']['dai20_cum_dE30'] == 2 else [KA['do']['i']['dai20_cum_dE30']], False)
case('N2P-1', 'khung thử: (c) có báo cụm dải (người đọc)', bad(T1['N2P-1'], 'c'), True)
case('N2P-2', 'khung thử: (a) lỗi thời đại có năm (máy bay, ô tô, cột điện)', bad(T1['N2P-2'], 'a'), True)
case('N2P-3', 'khung thử: (a) T9b ≤ 2 % (0,39 / 0,80)', bad(T1['N2P-3'], 'a'), False)
case('N2P-3', 'khung thử: (b) gpt báo bờ lấn nước quanh người chèn', bad(T1['N2P-3'], 'b'), True)
case('N2P-4', 'khung thử tĩnh: (a) người chèn L6 = đóng băng', bad(T1['N2P-4'], 'a'), True)
T1b = N.tong_tam([kiem(GP, VA, anh_tinh=False)])
case('N2P-4', 'cùng khung, không phải tấm tĩnh (anh_tinh false) → không áp (iv)', bad(T1b['N2P-4']), False)
# đối chứng sạch: render ↔ render, trả lời đã lưu của 2 mô hình
K0 = kiem(RJ, V0); T0 = N.tong_tam([K0])
for q in ('N2P-1', 'N2P-2', 'N2P-3', 'N2P-4'): case(q, 'đối chứng render↔render: 0 báo', bad(T0[q]), False)
# khung thử CHƯA ghép (AI dán đè lớp (a)) → (a)
KR = kiem(KJ, VA); TR = N.tong_tam([KR])
case('N2P-1', f"khung thử chưa ghép: (a) lệch {KR['do']['i']['max_trong_a']}/255 trong (a)", bad(TR['N2P-1'], 'a'), True)
# T9b trượt: tô nước lên 6 % đất
G2 = G.copy(); Dm = N.lop(Lb, NM, N.DAT); ys, xs = np.nonzero(Dm); k = len(ys) * 6 // 100
G2[ys[:k], xs[:k]] = (190, 170, 0); P2 = os.path.join(TMP, 'ghep-nuoc.png'); cv2.imwrite(P2, G2)
T9 = N.tong_tam([kiem(P2, V0)])
case('N2P-3', 'tô màu nước lên 6 % đất → (a) T9b đất→nước > 2 %', bad(T9['N2P-3'], 'a'), True)
# (ii) q_thoi_dai (NC-N2P: 3/3 lỗi thời đại): nghi vấn mới so render
Q = json.load(open(os.path.join(D, 'q_thoi_dai-ra.json')))['khung'][0]
moi = N.qtd_moi(Q, {'nghi_van': []}); nb = lambda x: [x['toa_do_px'][0] / W, x['toa_do_px'][1] / H, x['toa_do_px'][2] / W, x['toa_do_px'][3] / H]
nq = sum(1 for v in DA['vat'] if v['loai_loi'] == 'thoi_dai' and any(hit(nb(x), v['hop']) for x in moi))
case('N2P-2', f'q_thoi_dai bắt {nq}/3 lỗi thời đại chèn (NC-N2P 3/3)', [] if nq == 3 else [nq], False)
case('N2P-2', 'q_thoi_dai: nghi vấn đã có ở render (đối chứng) không tính', N.qtd_moi(Q, Q), False)
KQ = dict(KA, L2=[], Q=dict(moi=moi, loi=None)); TQ = N.tong_tam([KQ])
case('N2P-2', '(b) q_thoi_dai nghi vấn mới → lỗi', bad(TQ['N2P-2'], 'b'), True)
# không --vision, không bộ đệm → THIẾU (không gọi mạng)
Vn = QV.soi(RJ, GP, 1780, 'Gibraltar', False, out=None, tag='x', api=False, cache={})
case('N2P vision', 'không --vision, không bộ đệm → không gọi mạng, "chưa soi"', [] if (Vn.get('loi') or '').startswith('chưa soi') and not Vn['ket_qua'] else [Vn], False)
case('N2P vision', 'bộ đệm có khoá → đọc lại', [] if QV.soi(RJ, GP, 1780, 'Gibraltar', False, api=False, cache={Vn['khoa']: dict(ket_qua=VA, loi=None)}).get('tu_bo_dem') else ['không đọc bộ đệm'], False)
EP4 = dict(id='t4-thu', out=TMP, kenh2_tu_t4=True, animatic=False, segments=[],
           n2p=dict(noi='Gibraltar', tam=[dict(id='thu', shot='S1', render=RJ, ghep=GP, mat_na=MJ, nam=1780)]))
LS4 = [dict(shot='S1', dur=10, ai_nen=True, goc='cao', tl=True), dict(shot='S2', dur=30, goc='cao', tl=True)]
C4 = N.check(EP4, None, '.', LS4, vision=False, vids={'S1': dict(buoc_max=0.3, buoc_tai_s=3, nhap_ghep=0.0, nhap_render=0.0)})
case('N2P-1', 'tập T4 không --vision: (b) thiếu mô hình nhìn (không gọi mạng)', [x for x in C4['N2P-1']['thieu'] if x.startswith('(b)') and 'chưa soi' in x], True)
mo, ch, cb = cap112.cap('N2P-1', C4['N2P-1'])
case('cấp', 'N2P-1 THIẾU mô hình ở G2 → Chặn', ch, True)
mo, ch, cb = cap112.cap('N2P-1', dict(C4['N2P-1'], cong='animatic'))
case('cấp', 'N2P-1 ở animatic → chỉ Cảnh báo', ch, False)
mo, ch, cb = cap112.cap('N2P-1', dict(T1['N2P-1'], loi=bad(T1['N2P-1'], 'c'), cong='G2'))
case('cấp', 'N2P-1 chỉ (c) cụm dải → Cảnh báo, không Chặn', ch, False)
case('N2P áp dụng', 'tập T3 (không kenh2_tu_t4/n2p) → N2P-1…6 KHÔNG ÁP', sum((kq(v, 'KHÔNG ÁP') for v in N.check(dict(id='t3', khung_sach=True), None, '.', []).values()), []), False)


# ---- (v) video tổng hợp 320×180, 24 khung/s, 6 s: tấm 1 → tấm 2 ở 3,0 s
def mk_video(path, frames):
    h, w = frames[0].shape[:2]
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-nostdin', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{w}x{h}', '-r', '24', '-i', '-', '-c:v', 'ffv1', path], stdin=subprocess.PIPE)
    for f in frames: p.stdin.write(f.tobytes())
    p.stdin.close(); p.wait(); return path


mask = np.zeros((180, 320, 3), np.uint8); mask[:90] = N.PAL['troi'][::-1]; mask[90:] = N.PAL['bang'][::-1]; mask[100:150, 140:200] = N.PAL['nha'][::-1]
MP = os.path.join(TMP, 'mask.png'); cv2.imwrite(MP, mask)
rng = np.random.default_rng(7)
base_ = np.zeros((180, 320, 3), np.uint8); base_[:90] = (200, 160, 120); base_[90:] = (90, 140, 150)
base_ = np.clip(base_.astype(np.int16) + rng.integers(-12, 12, base_.shape), 0, 255).astype(np.uint8)   # vân tĩnh
plate2 = np.clip(base_.astype(np.int16) + (8, 4, -6), 0, 255).astype(np.uint8)
nha = (235, 235, 235)


def khung(i, mode):
    t = i / 24.0
    if mode == 'hoa': k = min(1.0, max(0.0, (t - 3.0) / 2.0))
    elif mode == 'cat': k = 1.0 if t >= 3.0 else 0.0
    else: k = 0.0
    f = np.clip(base_ * (1 - k) + plate2 * k, 0, 255).astype(np.uint8)
    if mode == 'nhap': f = np.clip(f.astype(np.int16) + rng.integers(-2, 3, f.shape), 0, 255).astype(np.uint8)
    f[100:150, 140:200] = nha; x = 140 + (i % 50); f[110:120, x:x + 8] = (20, 20, 200)   # vật lớp (a) chuyển động
    return f


VR = mk_video(os.path.join(TMP, 'render.mkv'), [khung(i, 'tinh') for i in range(144)])
VID = {m: N.do_video(mk_video(os.path.join(TMP, f'{m}.mkv'), [khung(i, m) for i in range(144)]), VR, MP, [dict(t=3.0, kieu='hoa', dur=2.0)] if m == 'hoa' else [])
       for m in ('hoa', 'cat', 'nhap')}
E5 = dict(id='t4', kenh2_tu_t4=True)
for m, ch_, exp, muc, ten in (('hoa', [dict(t=3.0, kieu='hoa', dur=2.0)], False, 'abc', 'hoà 2,0 s, tấm tĩnh → sạch (bước < 1 ΔE/khung)'),
                              ('cat', [dict(t=3.0, kieu='hoa', dur=2.0)], True, 'b', 'cắt cứng giữa 2 tấm → (b) bước nhảy > 1 ΔE/khung'),
                              ('nhap', [], True, 'c', 'tấm nhấp nháy ±2 mức xám → (c) > 1,5 × đối chứng (sàn 0,02)')):
    x = N.n2p5(E5, [dict(shot='S1', dur=6, ai_nen=dict(chuyen_tam=ch_))], '.', {'S1': VID[m]})
    case('N2P-5', ten + f" [bước {VID[m]['buoc_max']}, nhấp {VID[m]['nhap_ghep']}]", bad(x, *muc), exp)
x = N.n2p5(E5, [dict(shot='S1', dur=6, ai_nen=dict(chuyen_tam=[dict(t=3, kieu='cat', dur=0)]))], '.', {'S1': VID['hoa']})
case('N2P-5', 'khai chuyển tấm kiểu cắt → (a)', bad(x, 'a'), True)
x = N.n2p5(E5, [dict(shot='S1', dur=6, ai_nen=dict(chuyen_tam=[dict(t=3, kieu='hoa', dur=1.5)]))], '.', {'S1': VID['hoa']})
case('N2P-5', 'hoà 1,5 s < 2 s → (a)', bad(x, 'a'), True)
x = N.n2p5(E5, [dict(shot='S1', dur=6, ai_nen=True)], '.', None)
case('N2P-5', 'shot ai_nen không có video đo → THIẾU', kq(x, 'THIẾU'), False)


# ---- (vi) trần §15(d)
def LSx(nen, mh, n1=0.0, chong=False):
    L = [dict(shot='A', dur=nen, ai_nen=True, minh_hoa=chong), dict(shot='B', dur=mh, minh_hoa=True), dict(shot='C', dur=n1, ai_image=True), dict(shot='D', dur=100 - nen - mh - n1)]
    return [s for s in L if s['dur'] > 0]


for args, exp, muc, ten in (((50, 20), False, 'abcd', 'tấm nền 50 % · minh hoạ 20 % · tổng 70 % (đúng trần) → sạch'),
                            ((51, 10), True, 'a', 'tấm nền 51 % → (a)'), ((30, 21), True, 'b', 'minh hoạ 21 % → (b)'),
                            ((45, 20, 6), True, 'c', 'tổng AI 71 % (45 + 20 + N1 6) → (c)'), ((40, 10, 0, True), True, 'd', 'một shot vừa ai_nen vừa minh_hoa → (d)')):
    case('N2P-6', ten, bad(N.n2p6(E5, LSx(*args)), *muc), exp)
case('N2P-6', 'không log shot → THIẾU', kq(N.n2p6(E5, None), 'THIẾU'), False)

# ======================================================================== MINH-HOA
EM = dict(id='t3', khung_sach=True, segments=[dict(id=s, dur=d) for s, d in (('A', 40), ('M', 10), ('B', 50))])
SO = dict(model='gemini-omni-1.1-flash', lenh='restyle …', sha_vao='aa' * 32, sha_ra='bb' * 32)


def LSm(**kw):
    m = dict(shot='M', t0=40, t1=50, dur=10, minh_hoa=True, goc='thap', agl_m=[30, 35], nhan_minh_hoa='Illustration', so_ai=SO); m.update(kw)
    return [dict(shot='A', t0=0, t1=40, dur=40, goc='cao'), {k: v for k, v in m.items() if v is not None}, dict(shot='B', t0=50, t1=100, dur=50, goc='cao')]


mh = lambda LS, TX=None, E=EM: K7.minh_hoa(E, None, LS, '.', TX, 12)
case('MINH-HOA', 'đoạn 10 % kẹp giữa 2 shot 3D, nhãn cả đoạn, máy 35 m, sổ AI đủ → sạch', bad(mh(LSm())), False)
case('MINH-HOA', 'không shot minh_hoa → KHÔNG ÁP', kq(mh([dict(shot='A', dur=100, goc='cao')]), 'KHÔNG ÁP'), False)
E25 = dict(EM, segments=[dict(id='A', dur=30), dict(id='M', dur=25), dict(id='B', dur=45)])
case('MINH-HOA', 'minh hoạ 25 % > 20 % → (a)', bad(mh([dict(shot='A', t0=0, t1=30, dur=30, goc='cao'), dict(LSm()[1], t0=30, t1=55, dur=25),
                                                        dict(shot='B', t0=55, t1=100, dur=45, goc='cao')], E=E25), 'a'), True)
case('MINH-HOA', 'minh hoạ đúng 20 % → sạch (a)', bad(mh([dict(shot='A', t0=0, t1=30, dur=30, goc='cao'), dict(LSm()[1], t0=30, t1=50, dur=20),
                                                         dict(shot='B', t0=50, t1=100, dur=50, goc='cao')]), 'a'), False)
case('MINH-HOA', 'nhãn "AI illustration" sai chữ → (b)', bad(mh(LSm(nhan_minh_hoa='AI illustration')), 'b'), True)
case('MINH-HOA', 'nhãn chỉ 2–10 s của đoạn 10 s → (b)', bad(mh(LSm(nhan_t=[2.0, 10.0])), 'b'), True)
case('MINH-HOA', 'không log chữ, không trường nhãn → THIẾU (b)', bad(mh(LSm(nhan_minh_hoa=None)), 'b'), True)
TXok = {f: [dict(role='minh_hoa', s='Illustration')] for f in range(960, 1200, 12)}
TXpart = {f: ([dict(role='minh_hoa', s='Illustration')] if f < 1100 else []) for f in range(960, 1200, 12)}
case('MINH-HOA', 'log chữ: "Illustration" mọi khung mẫu của đoạn → sạch (b)', bad(mh(LSm(nhan_minh_hoa=None), TXok), 'b'), False)
case('MINH-HOA', 'log chữ: nhãn tắt từ 45,8 s → (b)', bad(mh(LSm(nhan_minh_hoa=None), TXpart), 'b'), True)
L3 = LSm(); L3[2] = dict(L3[2], goc='phang')
case('MINH-HOA', 'shot sau là thẻ/ảnh phẳng → (c) không kẹp giữa 2 shot 3D', bad(mh(L3), 'c'), True)
case('MINH-HOA', 'minh hoạ mở đầu phim (không có shot trước) → (c)', bad(mh(LSm()[1:]), 'c'), True)
case('MINH-HOA', 'máy 60 m AGL → (d)', bad(mh(LSm(agl_m=[30, 60])), 'd'), True)
case('MINH-HOA', 'không log agl_m → (d) không xét', bad(mh(LSm(agl_m=None)), 'd'), False)
case('MINH-HOA', 'không dòng sổ AI → (e)', bad(mh(LSm(so_ai=None)), 'e'), True)
case('MINH-HOA', 'dòng sổ AI thiếu SHA đầu ra → (e)', bad(mh(LSm(so_ai=dict(model='m', lenh='x'))), 'e'), True)
SOP = os.path.join(TMP, 'so-ai.jsonl'); open(SOP, 'w').write(json.dumps(dict(SO, shot='M')) + '\n')
case('MINH-HOA', 'sổ AI ở tệp so_ai: (jsonl, mục shot = M) → sạch (e)', bad(mh(LSm(so_ai=None), E=dict(EM, so_ai=SOP)), 'e'), False)
mo, ch, cb = cap112.cap('MINH-HOA', dict(mh(LSm(agl_m=[90])), cong='G2'))
case('cấp', 'MINH-HOA ở G2 → Chặn', ch, True)
mo, ch, cb = cap112.cap('MINH-HOA', dict(mh(LSm(agl_m=[90])), cong='animatic'))
case('cấp', 'MINH-HOA ở animatic → Cảnh báo', ch, False)
# SACH-1: nhãn Illustration hợp lệ CHỈ trong shot minh hoạ (§14.1 (c))
ES = dict(id='t3', khung_sach=True, segments=[dict(id=s, dur=d, shots=[dict(tpl='plate', at=0, type='scene3d', p=dict(sach=True))]) for s, d in (('A', 40), ('M', 10), ('B', 50))])
TXs = {f: [dict(role='minh_hoa', s='Illustration')] for f in range(960, 1200, 12)}
TXo = {f: [dict(role='minh_hoa', s='Illustration')] for f in range(0, 120, 12)}
case('SACH-1', 'nhãn Illustration trong shot minh hoạ → sạch', bad(K6.sach1(ES, None, TXs, 12, K7._mh_spans(LSm())), 'c', 'e'), False)
case('SACH-1', 'nhãn Illustration ở shot 3D thường → (e)', bad(K6.sach1(ES, None, TXo, 12, K7._mh_spans(LSm())), 'c', 'e'), True)
case('SACH-1', '1.16.1 (không truyền shot minh hoạ): nhãn → (e) như cũ', bad(K6.sach1(ES, None, TXs, 12), 'c', 'e'), True)

# ======================================================================== EO-DAT R1–R4 (1.17.1: ngưỡng §14.7 nguyên văn)
EE = dict(id='t3', khung_sach=True, segments=[dict(id='S1', dur=20, chuong='1'), dict(id='S2', dur=20, chuong='1'), dict(id='S3', dur=20, chuong='2')])


def eo(LS): return K7.eo_dat(EE, None, LS)


R1ok = [dict(shot='S1', t0=0, dur=20, noi='eo_dat', chu_the_eo_dat=True, chu_the_pct=[[0, 30], [5, 28], [10, 26]], trong_pct=10, so_goc=2, su_kien=[dict(t=5), dict(t=10), dict(t=15)])]
case('EO-DAT-R1', 'chủ thể trung vị 28 % ≥ 20 % → sạch', bad(eo(R1ok)['EO-DAT-R1']), False)
case('EO-DAT-R1', 'chủ thể 20 % (đúng mức trên) → sạch', bad(eo([dict(R1ok[0], chu_the_pct=20)])['EO-DAT-R1']), False)
case('EO-DAT-R1', 'chủ thể 12 % < 15 % → (a)', bad(eo([dict(R1ok[0], chu_the_pct=12)])['EO-DAT-R1'], 'a'), True)
case('EO-DAT-R1', 'chủ thể 14,9 % < 15 % → (a)', bad(eo([dict(R1ok[0], chu_the_pct=14.9)])['EO-DAT-R1'], 'a'), True)
case('EO-DAT-R1', 'chủ thể 17 % (15–20 %) → (b) Cảnh báo', bad(eo([dict(R1ok[0], chu_the_pct=17)])['EO-DAT-R1'], 'b'), True)
case('EO-DAT-R1', 'chủ thể 17 % → KHÔNG (a)', bad(eo([dict(R1ok[0], chu_the_pct=17)])['EO-DAT-R1'], 'a'), False)
case('EO-DAT-R1', 'chủ thể 15 % (đúng mức dưới) → không (a)', bad(eo([dict(R1ok[0], chu_the_pct=15)])['EO-DAT-R1'], 'a'), False)
case('EO-DAT-R1', 'chủ thể 22 % (1.17.0 tạm 25 % bắt; §14.7 không) → sạch', bad(eo([dict(R1ok[0], chu_the_pct=22)])['EO-DAT-R1']), False)
mo, ch, cb = cap112.cap('EO-DAT-R1', dict(eo([dict(R1ok[0], chu_the_pct=17)])['EO-DAT-R1'], cong='G2'))
case('cấp', 'EO-DAT-R1 17 % ở G2 → không Chặn', ch, False)
case('cấp', 'EO-DAT-R1 17 % ở G2 → có Cảnh báo', cb, True)
mo, ch, cb = cap112.cap('EO-DAT-R1', dict(eo([dict(R1ok[0], chu_the_pct=12)])['EO-DAT-R1'], cong='G2'))
case('cấp', 'EO-DAT-R1 12 % ở G2 → Chặn', ch, True)
mo, ch, cb = cap112.cap('EO-DAT-R1', dict(eo([dict(R1ok[0], chu_the_pct=None)])['EO-DAT-R1'], cong='G2'))
case('cấp', 'EO-DAT-R1 thiếu chu_the_pct ở G2 → Chặn', ch, True)
case('EO-DAT-R1', 'cờ chu_the_eo_dat nhưng không chu_the_pct → THIẾU', kq(eo([dict(R1ok[0], chu_the_pct=None)])['EO-DAT-R1'], 'THIẾU'), False)
case('EO-DAT-R1', 'không shot khai cờ → KHÔNG ÁP', kq(eo([dict(R1ok[0], chu_the_eo_dat=False)])['EO-DAT-R1'], 'KHÔNG ÁP'), False)
# chương 1 = S1 + S2 = 40 s → trần (b) 10 % = 4 s; chương 2 = S3 = 20 s → 2 s
R2 = lambda a, b, c: [dict(shot='S1', t0=0, dur=20, noi='eo_dat', trong_pct=a), dict(shot='S2', t0=20, dur=20, noi='eo_dat', trong_pct=b), dict(shot='S3', t0=40, dur=20, noi='eo_dat', trong_pct=c)]
case('EO-DAT-R2', 'không khung nào trống → sạch', bad(eo(R2(10, 20, 30))['EO-DAT-R2']), False)
case('EO-DAT-R2', 'trống 4 s / chương 40 s = 10 % (đúng trần) → sạch', bad(eo(R2([[0, 70], [4, 20]], 10, 10))['EO-DAT-R2']), False)
case('EO-DAT-R2', 'trong_pct 50 % (không > 50 %) suốt chương → không trống → sạch', bad(eo(R2(50, 50, 50))['EO-DAT-R2']), False)
case('EO-DAT-R2', 'trong_pct 55 % (> 50 %; 1.17.0 tạm 60 % bỏ qua) suốt 20 s → (a)', bad(eo(R2(10, 55, 10))['EO-DAT-R2'], 'a'), True)
case('EO-DAT-R2', 'trống 65 % suốt shot 20 s → (a) liên tục > 6 s', bad(eo(R2(10, 65, 10))['EO-DAT-R2'], 'a'), True)
case('EO-DAT-R2', 'trống nối qua ranh 2 shot: 3 s + 4 s = 7 s → (a)', bad(eo(R2([[0, 10], [17, 70]], [[0, 70], [4, 10]], 10))['EO-DAT-R2'], 'a'), True)
case('EO-DAT-R2', 'trống liên tục đúng 6 s → không (a)', bad(eo(R2([[0, 70], [6, 10]], 10, 10))['EO-DAT-R2'], 'a'), False)
case('EO-DAT-R2', 'chương 1: 2 khúc 3 s = 6 s / 40 s = 15 % > 10 % → (b)', bad(eo(R2([[0, 70], [3, 10]], [[0, 10], [17, 70]], 10))['EO-DAT-R2'], 'b'), True)
case('EO-DAT-R2', 'chương 1: 2 khúc 3 s / 40 s → KHÔNG (a)', bad(eo(R2([[0, 70], [3, 10]], [[0, 10], [17, 70]], 10))['EO-DAT-R2'], 'a'), False)
case('EO-DAT-R2', 'chương 2 (20 s): trống 3 s = 15 % > 10 % → (b)', bad(eo(R2(10, 10, [[0, 10], [10, 70], [13, 10]]))['EO-DAT-R2'], 'b'), True)
R2m = [dict(shot='S1', t0=0, dur=20, noi='eo_dat', trong_pct=[[0, 70], [4, 10], [10, 70], [14, 10]]), dict(shot='S2', t0=20, dur=80, noi='thanh_pho')]
case('EO-DAT-R2', 'mẫu số = thời lượng chương: trống 8 s / chương 100 s = 8 % → sạch (1.17.0: 8/20 eo đất = 40 % bắt)', bad(eo(R2m)['EO-DAT-R2'], 'b'), False)
case('EO-DAT-R2', 'cùng dữ liệu, bỏ shot phố 80 s → 8/20 = 40 % → (b)', bad(eo(R2m[:1])['EO-DAT-R2'], 'b'), True)
case('EO-DAT-R2', 'thiếu trong_pct → THIẾU', kq(eo(R2(None, None, None))['EO-DAT-R2'], 'THIẾU'), False)
R3 = lambda **kw: [dict(dict(shot='S1', t0=0, dur=20, noi='eo_dat', trong_pct=10, so_goc=2, su_kien=[dict(t=5), dict(t=10.5)], tl_buoc=[dict(t=15.5)]), **kw)]
case('EO-DAT-R3', 'shot 20 s: 2 góc, biến cố 5 · 10,5 · 15,5 s → sạch', bad(eo(R3())['EO-DAT-R3']), False)
case('EO-DAT-R3', 'shot 20 s: 1 góc → (a)', bad(eo(R3(so_goc=1))['EO-DAT-R3'], 'a'), True)
case('EO-DAT-R3', 'shot 20 s: goc_may 2 phần tử → sạch (a)', bad(eo(R3(so_goc=None, goc_may=['D', 'D2']))['EO-DAT-R3'], 'a'), False)
case('EO-DAT-R3', 'shot 20 s: khoảng biến cố 8 s → (b)', bad(eo(R3(su_kien=[dict(t=4)], tl_buoc=[dict(t=12)]))['EO-DAT-R3'], 'b'), True)
case('EO-DAT-R3', 'shot 20 s thiếu so_goc → THIẾU', kq(eo(R3(so_goc=None))['EO-DAT-R3'], 'THIẾU'), False)
case('EO-DAT-R3', 'shot 15 s (không > 15 s) → không xét', bad(eo(R3(dur=15, so_goc=1, su_kien=[], tl_buoc=[]))['EO-DAT-R3']), False)
mo, ch, cb = cap112.cap('EO-DAT-R3', dict(eo(R3(so_goc=1))['EO-DAT-R3'], cong='animatic'))
case('cấp', 'EO-DAT ở animatic → Cảnh báo', ch, False)
mo, ch, cb = cap112.cap('EO-DAT-R3', dict(eo(R3(so_goc=1))['EO-DAT-R3'], cong='G2'))
case('cấp', 'EO-DAT ở G2 → Chặn', ch, True)
R4 = lambda **kw: [dict(dict(shot='S1', t0=0, dur=8, loi_khong_vat_eo_dat=True), **kw)]
for n_ in ('pho', 'lau_dai', 'cang'):
    case('EO-DAT-R4', f'loi_khong_vat_eo_dat + noi {n_} → sạch', bad(eo(R4(noi=n_))['EO-DAT-R4']), False)
case('EO-DAT-R4', 'noi thanh_pho (tên log hiện dùng cho phố) → sạch', bad(eo(R4(noi='thanh_pho'))['EO-DAT-R4']), False)
case('EO-DAT-R4', 'noi eo_dat, không bản đồ → (a)', bad(eo(R4(noi='eo_dat'))['EO-DAT-R4'], 'a'), True)
case('EO-DAT-R4', 'không khai noi, không bản đồ → (a)', bad(eo(R4())['EO-DAT-R4'], 'a'), True)
case('EO-DAT-R4', 'noi eo_dat + ban_do_phu 3 s (đúng trần) → sạch', bad(eo(R4(noi='eo_dat', ban_do_phu=3))['EO-DAT-R4']), False)
case('EO-DAT-R4', 'noi eo_dat + ban_do_phu [1, 3,5] → sạch', bad(eo(R4(noi='eo_dat', ban_do_phu=[1, 3.5]))['EO-DAT-R4']), False)
case('EO-DAT-R4', 'noi eo_dat + ban_do_phu 3,5 s → (b)', bad(eo(R4(noi='eo_dat', ban_do_phu=3.5))['EO-DAT-R4'], 'b'), True)
case('EO-DAT-R4', 'ban_do_phu [[0, 2], [4, 8]] (lần 4 s) → (b)', bad(eo(R4(noi='eo_dat', ban_do_phu=[[0, 2], [4, 8]]))['EO-DAT-R4'], 'b'), True)
case('EO-DAT-R4', 'ban_do_phu {dur: 2} → sạch', bad(eo(R4(noi='eo_dat', ban_do_phu=dict(dur=2)))['EO-DAT-R4']), False)
case('EO-DAT-R4', 'noi pho nhưng ban_do_phu 5 s → (b) (TL-4 trần riêng)', bad(eo(R4(noi='pho', ban_do_phu=5))['EO-DAT-R4'], 'b'), True)
case('EO-DAT-R4', 'ban_do_phu: true (không giây) → THIẾU', kq(eo(R4(noi='eo_dat', ban_do_phu=True))['EO-DAT-R4'], 'THIẾU'), False)
case('EO-DAT-R4', 'không shot khai loi_khong_vat_eo_dat → KHÔNG ÁP', kq(eo([dict(shot='S1', t0=0, dur=8, noi='eo_dat')])['EO-DAT-R4'], 'KHÔNG ÁP'), False)
case('EO-DAT-R4', 'loi_khong_vat_eo_dat: false → KHÔNG ÁP', kq(eo(R4(loi_khong_vat_eo_dat=False))['EO-DAT-R4'], 'KHÔNG ÁP'), False)
mo, ch, cb = cap112.cap('EO-DAT-R4', dict(eo(R4(noi='eo_dat'))['EO-DAT-R4'], cong='G2'))
case('cấp', 'EO-DAT-R4 ở G2 → Chặn', ch, True)
mo, ch, cb = cap112.cap('EO-DAT-R4', dict(eo(R4(noi='eo_dat'))['EO-DAT-R4'], cong='animatic'))
case('cấp', 'EO-DAT-R4 ở animatic → không Chặn', ch, False)
case('1.17 áp dụng', 'tập trước T3 → MINH-HOA/EO-DAT KHÔNG ÁP', sum((kq(v, 'KHÔNG ÁP') for v in K7.check(dict(id='t2')).values()), []), False)

# ======================================================================== khiếu nại animatic T3 chấp nhận
# Q33 miễn năm khác (TL-1)
ap = lambda seg, t0, cam='c1': dict(scene='tl/t', cam=cam, seg=seg, t0=t0, t1=t0 + 10, shots=[f'{seg}/0'])
NL = {'A': (1700, 1710), 'B': (1780, 1782), 'C': (1940, 1941), 'D': (1780.5, 1781), 'E': (1940.5, 1940.7)}
case('Q33 (1.17)', '4 lần cùng điểm máy, 4 khoảng năm rời nhau → miễn 3 (đếm 1)', [] if len(K7.q33_mien([ap('A', 0), ap('B', 50), ap('C', 90), ap('X', 120)], dict(NL, X=(2026, 2026)))) == 3 else ['sai'], False)
case('Q33 (1.17)', 'năm chồng lần trước (1780,5 trong 1780–82; 1940,5 trong 1940–41) → không miễn',
     ['miễn nhầm'] if K7.q33_mien([ap('B', 0), ap('D', 50)], NL) | K7.q33_mien([ap('C', 0), ap('E', 50)], NL) else [], False)
case('Q33 (1.17)', 'không log năm → không miễn (hành vi 1.16.1)', ['miễn nhầm'] if K7.q33_mien([ap('A', 0), ap('B', 50)], None) else [], False)
case('Q33 (1.17)', 'cùng đoạn (B hai lần) → không miễn', ['miễn nhầm'] if K7.q33_mien([ap('B', 0), ap('B', 5)], NL) else [], False)
aps = [dict(ap('A', 0), phm=None), dict(ap('B', 50)), dict(ap('C', 90))]
r0 = KV.q33_k2({}, None, aps=[dict(a) for a in aps]); r1 = KV.q33_k2({}, None, aps=[dict(a) for a in aps], nam_log=NL)
case('Q33-K2 (1.17)', '3 lần cùng (vùng, góc), không log năm → > 2 (như 1.16.1)', r0['loi'], True)
case('Q33-K2 (1.17)', '3 lần, năm 1700 · 1780 · 1940 (đoạn khác) → miễn, ≤ 2', r1['loi'], False)
TLq = dict(heroes={'h': dict(hero='tl/t', opt={})}, segments=[dict(id=s, t0=t, shots=[dict(tpl='plate', t0=0, t1=10, p=dict(hero='h'))]) for s, t in (('A', 0), ('B', 50), ('C', 90))], tong_s=100)
Eq = dict(segments=[dict(id=s, dur=10, shots=[dict(tpl='plate', p=dict(hero='h'))]) for s in 'ABC'])
case('Q33 (1.17)', 'q_scene.q33: 3 lần cùng góc khai, không năm → > 2', QS.q33(Eq, TLq)['loi'], True)
case('Q33 (1.17)', 'q_scene.q33: 3 lần, 3 khoảng năm rời → ĐẠT', QS.q33(Eq, TLq, nam_log=NL)['loi'], False)
# ML1 cau ""
E6 = yaml.safe_load(open(os.path.join(FX, 'k116', 'ep-t3', 'episode.yaml')))
T6 = dict(segments=[], heroes=E6.get('heroes') or {}, tong_s=0.0); t = 0.0
for s in E6['segments']:
    T6['segments'].append(dict(id=s['id'], t0=t, shots=[dict(tpl=sh['tpl'], t0=0.0, t1=s['dur'], type=sh.get('type'), p=sh.get('p') or {}) for sh in s['shots']])); t += s['dur']
T6['tong_s'] = t
E6b = copy.deepcopy(E6); E6b['segments'][1]['shots'][0]['cau'] = ''
C6 = [dict(i=0, t0=0.0, t1=t, s='x')]
case('ML1 (1.17)', '1.16.1: cau "" → (c) không khớp câu', [x for x in MA.ml1(E6b, T6, C6, os.path.join(FX, 'k116', 'ep-t3'), claims=[])['muc']['c'] if "cau ''" in x], True)
case('ML1 (1.17)', '1.17: cau "" = không gắn câu, không (c)', [x for x in MA.ml1(E6b, T6, C6, os.path.join(FX, 'k116', 'ep-t3'), claims=[], v117=True)['muc']['c'] if "cau ''" in x], False)
# NC-H1 lớp nhà tl/* (V7C-D5)
z = dict(ty='scene3d', o=dict(bfile='buildings-v7b.json'), p={})
case('NC-H1 (1.17)', 'opt.bfile: 1.16.1 không nhận lớp nhà', [] if NO.layer_of(z) is None else ['nhận'], False)
case('NC-H1 (1.17)', 'opt.bfile: 1.17 nhận lớp nhà khai', [] if NO.layer_of(z, True) else ['không nhận'], False)
case('NC-H1 (1.17)', 'p.lop_nha: 1.17 nhận', [] if NO.layer_of(dict(ty='scene3d', o={}, p=dict(lop_nha='phố 1782 (V7B)')), True) else ['không nhận'], False)
case('NC-H1 (1.17)', 'cảnh tl/* không khoá lớp nhà nào → vẫn không có lớp', [] if NO.layer_of(dict(ty='scene3d', o=dict(units=1), p={}), True) is None else ['nhận nhầm'], False)
# cấp K-LAI-3V giữ đúng K116-D5
mo, ch, cb = cap112.cap('K-LAI-3V', dict(loi=['x'], cong='animatic'))
case('cấp', 'K-LAI-3V animatic → Cảnh báo (K116-D5 giữ nguyên)', ch, False)
mo, ch, cb = cap112.cap('K-LAI-3V', dict(loi=['x'], cong='G2'))
case('cấp', 'K-LAI-3V G2 → Chặn (K116-D5 giữ nguyên)', ch, True)


# ======================================================================== --api: chạy thật 2 mô hình + q_thoi_dai (có chi phí)
def api(out):
    os.makedirs(out, exist_ok=True); cache = {}; res = {}
    for tag, ghep, V_ in (('dap-an', GP, None), ('doi-chung', RJ, None)):
        t = dict(id=tag, shot='S1', render=RJ, ghep=ghep, mat_na=MJ, nam=1780)
        K = N.kiem_tam(t, '.', True, cache, out, 'Gibraltar', False); res[tag] = K
    json.dump(dict(ket_qua={k: {kk: vv for kk, vv in v.items() if kk != 'do'} for k, v in res.items()}, chi_phi=dict(
        vision=sum(float((v['V'] or {}).get('chi_phi_usd') or 0) for v in res.values()), qtd=sum(float((v['Q'] or {}).get('chi_phi_usd') or 0) for v in res.values()))),
        open(os.path.join(out, 'selftest-api.json'), 'w'), ensure_ascii=False, indent=1, default=str)
    B_ = cham(res['dap-an']); T_ = N.tong_tam([res['doi-chung']])
    nq_ = sum(1 for v in DA['vat'] if v['loai_loi'] == 'thoi_dai' and any(hit(nb(x), v['hop']) for x in (res['dap-an']['Q'] or {}).get('moi') or []))
    out_ = [('API đáp án', f'{mh}: bắt {B_[mh]}/6', [] if B_[mh] == 6 else [B_[mh]], False) for mh in ('gpt', 'claude', 'hop')]
    out_ += [('API đáp án', f'q_thoi_dai bắt {nq_}/3 thời đại', [] if nq_ == 3 else [nq_], False)]
    out_ += [('API đối chứng', f'{q}: 0 báo', [x for x in bad(T_[q]) if not x.startswith('(c)')], False) for q in ('N2P-1', 'N2P-2', 'N2P-3', 'N2P-4')]
    for x in out_: case(*x)
    return res


if '--api' in sys.argv:
    api(sys.argv[sys.argv.index('--api') + 1])

ok = sum(1 for x in R if x[3]); groups = {}
for rule, name, exp, good, got in R:
    groups.setdefault(rule, [0, 0]); groups[rule][0] += good; groups[rule][1] += 1
    print(f"{'ĐÚNG' if good else 'SAI '} [{rule}] {name} — kỳ vọng {exp}" + ('' if good else f' · nhận {got}'))
print(f'\nselftest 1.17: {ok}/{len(R)} ca đúng kỳ vọng · ' + ' · '.join(f'{k} {v[0]}/{v[1]}' for k, v in groups.items()))
sys.exit(0 if ok == len(R) else 1)
