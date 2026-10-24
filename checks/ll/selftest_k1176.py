#!/opt/cine/bin/python
"""Tự kiểm luật 1.17.6 (phiên K-1.17.6, 24/10/2026). Mỗi luật đổi/mới ≥ 1 ca ĐẠT + ≥ 1 ca TRƯỢT. Không mạng, không API (mô hình nhìn giả lập).
Cảnh tổng hợp có đáp án dựng trong bài (không fixtures ngoài): dãy nhà mái hồi (mã nhà 24 bit, mã mặt phẳng, pass bóng, lớp nha_thuong) như
selftest_k1175, và cảnh nhà lớn 1080p cho (d)(e) có bóng quét qua nhà.
  KN-1 N2P-3: khung KHÔNG NƯỚC → T9c KHÔNG ÁP (không KeyError), hàng N2P-3 KHÔNG ÁP; phép khác vẫn chạy (T9b đất→nước bắt nước AI vẽ lên đất);
       trộn tấm có nước + bờ lấn vẫn trượt.
  KN-2 N2P-1 (i): tấm be_mat_nha_ai — AI chỉ trong nhà đo được → (a) sạch; AI lấn nhà KHÔNG đo được / công trình có tên → (a) trượt.
  KN-3 mô hình nhìn: thiếu ảnh lần 1, đủ lần 2 → không THIẾU, 2 dòng sổ; thiếu cả hai lần → THIẾU.
  KN-4 (w): ống khói AI vẽ thêm → (w) cạnh màu mới; chỉ đổi bề mặt → không (w).
  KN-5 (d): albedo AI phân bố lại + bóng quét, dựng lại ánh sáng đúng → ĐẠT (thước 1.17.5 trượt oan — in để so); dán tĩnh, nhiễu mỗi khung → TRƯỢT.
  KN-6 (e): video 640×360 + tấm 1080p, khung 0 đúng → ĐẠT (so ở độ phân giải video); chồng sáng 2 lần → TRƯỢT.
  px/m: khai be_mat_nha_px_m_min 4 → nhà 3 px/m phủ AI → (b) trượt; không khai (2) → đạt; khai 1,5 → (w) + dùng 2.
  TU-LIEU-10 (tu_lieu_tran_pct, (b) ≤ 10 s/lần, (k)) · TU-LIEU-OMNI ((a) trùng, (b) ghép liền) · cấp · áp dụng.
  /opt/cine/bin/python checks/ll/selftest_k1176.py        mã thoát 0 = mọi ca đúng kỳ vọng"""
import copy, json, os, subprocess, sys, tempfile, types

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, ROOT)
import numpy as np  # noqa: E402
import cv2  # noqa: E402
from checks.ll import q_n2p as NP, q_k1175 as K, q_k1176 as K76, q_k1174 as K74, q_n2p_vision as QV, cap112  # noqa: E402

TMP = tempfile.mkdtemp(prefix='k1176-'); R = []


def case(rule, name, got, expect_fail):
    got = list(got) if got else []
    R.append((rule, name, 'bắt lỗi' if expect_fail else 'sạch', bool(got) == expect_fail, got[:2]))


def bad(x, *muc):
    L = (x.get('loi') or []) + (x.get('thieu') or [])
    return [y for y in L if not muc or any(y.startswith(f'({m})') for m in muc)]


def luu(nm, x): p_ = os.path.join(TMP, nm); cv2.imwrite(p_, x); return p_
def ma24(M): return np.stack([M & 255, (M >> 8) & 255, (M >> 16) & 255], -1).astype(np.uint8)


def mp4(nm, frames, wh=None):
    """video kiểm KHÔNG MẤT (libx264 crf 0 yuv444p — như THU-B); wh: thu INTER_AREA về cỡ video trước khi mã hoá"""
    p_ = os.path.join(TMP, nm); h_, w_ = frames[0].shape[:2]
    if wh: w_, h_ = wh
    pr = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{w_}x{h_}', '-r', '24', '-i', '-', '-c:v', 'libx264', '-crf', '0',
                           '-pix_fmt', 'yuv444p', p_], stdin=subprocess.PIPE)
    for f_ in frames: pr.stdin.write((cv2.resize(f_, (w_, h_), interpolation=cv2.INTER_AREA) if wh else f_).tobytes())
    pr.stdin.close(); pr.wait(); return p_


# ====================================================================== cảnh A: dãy nhà mái hồi 4 px/m (như selftest_k1175), KHÔNG có nước
H5, W5 = 540, 960
I5 = np.zeros((H5, W5), np.int64); P5 = np.zeros((H5, W5), np.int64); S5 = np.full((H5, W5), 0.55, np.float32); L5 = np.zeros((H5, W5, 3), np.uint8)
L5[:] = (200, 170, 90); nha5 = []; hid = 0
for r_ in range(4):
    for c_ in range(14):
        hid += 1; x0, y0 = 40 + c_ * 62, 60 + r_ * 110; w_, hh = 44, 52
        I5[y0:y0 + hh, x0:x0 + w_] = hid; P5[y0 + 22:y0 + hh, x0:x0 + w_] = hid * 10 + 1; S5[y0 + 22:y0 + hh, x0:x0 + w_] = 0.62
        for yy in range(y0, y0 + 22):
            k_ = (yy - y0) / 22.0; xa, xb = int(x0 + w_ / 2 - k_ * w_ / 2), int(x0 + w_ / 2 + k_ * w_ / 2)
            I5[yy, x0:x0 + w_] = 0; I5[yy, xa:xb] = hid
            P5[yy, xa:x0 + w_ // 2] = hid * 10 + 2; S5[yy, xa:x0 + w_ // 2] = 0.95; P5[yy, x0 + w_ // 2:xb] = hid * 10 + 3; S5[yy, x0 + w_ // 2:xb] = 0.35
        nha5.append(dict(id=hid, lo=r_ + 1, px_m=3.0 if r_ == 3 else 4.0))   # hàng 4: 3 px/m (ca khai 4)
L5[I5 > 0] = (215, 215, 215)
TEN = (slice(20, 50), slice(870, 930)); L5[TEN] = (235, 235, 235)   # công trình có tên (lớp 'nha', (a) cứng)
alb = lambda seed: np.random.default_rng(seed).uniform(0.35, 0.9, (hid + 1, 3))


def anh(albedo, S=S5, nhieu=0.0, seed=0):
    A_ = albedo[I5] * S[..., None]; A_[I5 == 0] = np.array([0.55, 0.62, 0.50]) * S[I5 == 0][:, None]
    A_[TEN] = np.array([0.7, 0.7, 0.75]) * 0.6
    if nhieu: A_ = A_ * (1 + np.random.default_rng(seed).normal(0, nhieu, A_.shape))
    return np.clip(A_ * 255, 0, 255).astype(np.uint8)


R5 = anh(alb(1)); B5 = np.clip(np.repeat(S5[..., None], 3, -1) * 0.6 * 255, 0, 255).astype(np.uint8)
F5 = dict(render=luu('r5.png', R5), mat_na=luu('l5.png', L5[..., ::-1]), mat_na_nha=luu('i5.png', ma24(I5)), mat_na_mat=luu('p5.png', ma24(P5)), bong=luu('b5.png', B5))
json.dump(nha5, open(os.path.join(TMP, 'n5.json'), 'w')); F5['nha'] = os.path.join(TMP, 'n5.json')
AI5 = anh(alb(7), nhieu=0.03, seed=3)
do4 = {h['id'] for h in nha5 if h['px_m'] >= 4}; do2 = {h['id'] for h in nha5}


def ghep_vao(ids, src=AI5):
    m = cv2.dilate(np.isin(I5, list(ids)).astype(np.uint8), np.ones((3, 3), np.uint8)) > 0
    m[TEN] = False; G = R5.copy(); G[m] = src[m]; return G


G5 = ghep_vao(do2)   # AI ở mọi nhà đo được ở ngưỡng 2
t5 = dict(F5, id='t5', ghep=luu('g5.png', G5), nam=1938, be_mat_nha_ai=True)

# ---------------------------------------------------------------------- KN-1: khung không nước
Ln, nn = NP.idmap(F5['mat_na'], (W5, H5))
c9 = K.t9c(R5, G5, Ln, nn)
case('KN-1 N2P-3', 'khung không có lớp nước → T9c trả đủ khoá, ap False (không KeyError)', [] if (c9.get('ap') is False and all(k in c9 for k in ('so_doan_lan', 'sau_lon_nhat_px', 'giua_pct', 'lan'))) else ['thiếu khoá'], False)
L_it = Ln.copy(); L_it[200:203, 5:8] = nn.index('nuoc')   # 9 điểm nước < 0,2 % khung (như B3: 213 px)
case('KN-1 N2P-3', 'nước < 0,2 % khung → T9c KHÔNG ÁP', [] if K.t9c(R5, G5, L_it, nn).get('ap') is False else ['áp'], False)


def KT(t_):
    D = NP.do_tam(t_['render'], t_['ghep'], t_['mat_na'], NP.LOP_A, None, None)
    return dict(id=t_['id'], shot='s', nam=1938, anh_tinh=True, do={k: v for k, v in D.items() if not k.startswith('_')}, V={}, L1=[], L2=[], L2b=[], L4=[], VUNG=[], Q=None, SONG=None, VONG=None)


k_nn = KT(dict(F5, id='kn', ghep=F5['render']))
T3 = NP.tong_tam([k_nn, KT(dict(F5, id='kn2', ghep=F5['render']))])
case('KN-1 N2P-3', 'mọi tấm không nước, 0 lỗi khác → hàng N2P-3 KHÔNG ÁP (không "không chạy được")', [] if T3['N2P-3']['ket_qua'] == 'KHÔNG ÁP' else [T3['N2P-3']], False)
case('KN-1 N2P-1/2/4', 'khung không nước: N2P-1, N2P-2, N2P-4 vẫn chạy (ĐẠT, không lỗi chạy)', [q for q in ('N2P-1', 'N2P-2', 'N2P-4') if not T3[q]['ok']], False)
Gw = R5.copy(); Gw[300:420, 100:300] = (190, 150, 40)   # AI vẽ "nước" xanh lên đất (khung không nước)
k_w = KT(dict(F5, id='kw', ghep=luu('gw.png', Gw)))
case('KN-1 N2P-3', 'khung không nước, AI vẽ nước lên đất → T9b đất→nước vẫn bắt (a) — phép khác vẫn chạy', bad(NP.tong_tam([k_w])['N2P-3'], 'a'), True)
# trộn với một tấm CÓ nước + bờ lấn (dải nước dưới, bờ trên lấn 12 px)
Lw = L5.copy(); Lw[470:540, :] = (0, 170, 190); Rw = R5.copy()
yw, xw = np.mgrid[470:540, 0:W5]; Rw[470:540, :] = np.clip(np.array([150, 110, 40]) + (18 * np.sin(xw / 7.0) * np.cos(yw / 3.0))[..., None] + (yw - 470)[..., None] * 0.6, 0, 255).astype(np.uint8)   # nước có gợn
Gl = Rw.copy(); Gl[470:482, 200:500] = (60, 90, 120)
kw2 = KT(dict(id='bo', render=luu('rw.png', Rw), ghep=luu('gl.png', Gl), mat_na=luu('lw.png', Lw[..., ::-1])))
case('KN-1 N2P-3', 'trộn tấm không nước + tấm có nước bờ lấn 12 px → vẫn TRƯỢT (c)', bad(NP.tong_tam([k_nn, kw2])['N2P-3'], 'c'), True)
case('KN-1 N2P-3', 'tấm có nước, render ↔ chính nó → ĐẠT', bad(NP.tong_tam([KT(dict(id='bo0', render=os.path.join(TMP, 'rw.png'), ghep=os.path.join(TMP, 'rw.png'), mat_na=os.path.join(TMP, 'lw.png')))])['N2P-3']), False)

# ---------------------------------------------------------------------- KN-2: N2P-1 (i) với tấm be_mat_nha_ai
def n2p1(t_, ppm=2.0):
    kt = NP.kiem_tam(t_, '.', False, {}, None, 'London', True, ppm); return bad(NP.tong_tam([kt])['N2P-1'], 'a'), kt


a1, kt1 = n2p1(t5)
case('KN-2 N2P-1 (a)', f"BMN: AI chỉ trong nhà đo được nở 1 px → (a) 0/255 ({kt1['do']['i'].get('bmn')})", a1, False)
case('KN-2 N2P-1 (a)', 'cùng tấm KHÔNG khai be_mat_nha_ai (luật cũ: nhà thường = (a)) → (a) trượt', n2p1(dict(t5, be_mat_nha_ai=False))[0], True)
Gt = G5.copy(); Gt[TEN] = 0
case('KN-2 N2P-1 (a)', 'BMN: AI lấn công trình có tên (lớp nha) → (a) trượt', n2p1(dict(t5, ghep=luu('gt.png', Gt)))[0], True)
case('KN-2 N2P-1 (a)', 'BMN khai px/m ≥ 4: AI phủ cả nhà 3 px/m (không đo được) → (a) trượt (nhà không đo được giữ (a))', n2p1(t5, 4.0)[0], True)
case('KN-2 N2P-1 (a)', 'BMN khai px/m ≥ 4: AI chỉ ở nhà ≥ 4 px/m → (a) sạch', n2p1(dict(t5, ghep=luu('g54.png', ghep_vao(do4))), 4.0)[0], False)
# mô hình nhìn N2+ báo "thêm công trình" (khung cửa sổ) trong vùng BMN → (c) người đọc; ngoài vùng (công trình có tên) → (b) Chặn — qua kiem_tam + bộ đệm giả
def kt_mh(items):
    kc_ = QV.khoa(t5['render'], t5['ghep'], 1938, 'London', True, ('gpt', 'claude'))
    ca = {kc_: dict(ket_qua={'gpt': dict(json=dict(them=items, bot_doi=[], doi_loai_vung=[]), meta={}), 'claude': dict(json=dict(them=[], bot_doi=[], doi_loai_vung=[]), meta={})}, loi=None)}
    return NP.tong_tam([NP.kiem_tam(t5, '.', False, ca, None, 'London', True, 2.0)])['N2P-1']


ys5, xs5 = np.nonzero(I5 == 9); bx = [xs5.min() / W5, ys5.min() / H5, xs5.max() / W5, ys5.max() / H5]
r_in = kt_mh([dict(loai='cong_trinh', mo_ta='added sash windows', toa_do=bx, do_tin=0.9)])
case('KN-2 N2P-1 (b)', 'BMN: mô hình báo thêm khung cửa sổ trong nhà đo được → không (b) Chặn', bad(r_in, 'b'), False)
case('KN-2 N2P-1 (b)', 'BMN: cùng báo → (c) người đọc có ghi "vùng nhà đo được BMN"', [x for x in r_in['loi'] if x.startswith('(c)') and 'BMN' in x], True)
r_out = kt_mh([dict(loai='cong_trinh', mo_ta='new spire', toa_do=[905 / W5, 25 / H5, 925 / W5, 45 / H5], do_tin=0.9)])
case('KN-2 N2P-1 (b)', 'BMN: mô hình báo đổi công trình có tên (ngoài vùng BMN) → (b) Chặn', bad(r_out, 'b'), True)
vb, nd = K76.vung_bmn(t5, '.', 2.0)
hk = K.hinh_khoi(R5, G5, np.where(L5[..., 0] == 215, I5, 0), {h['id']: h for h in nha5}, np.where(L5[..., 0] == 215, P5, 0), B5)
case('KN-2 vung_bmn', f'tập nhà đo được của N2P-1 = của BE-MAT-NHA (a) ({nd} nhà)', [] if nd == sum(1 for x in hk.values() if x.get('do')) else [nd], False)

# ---------------------------------------------------------------------- px/m (chủ dự án 15:25): BE-MAT-NHA (b) với be_mat_nha_px_m_min
def bmn_row(E_extra, t_=t5):
    E = dict(id='t4', kenh2_tu_t4=True, n2p=dict(noi='London', t4=True, tam=[t_]), **E_extra); return K.be_mat_nha(E, '.', False)


r4 = bmn_row(dict(be_mat_nha_px_m_min=4))
case('px/m', 'khai 4: AI phủ nhà 3 px/m → (b) trượt (nhà 2–4 px/m phải = render)', bad(r4, 'b'), True)
case('px/m', 'không khai (mặc định 2): cùng tấm → (b) sạch', bad(bmn_row({}), 'b'), False)
case('px/m', 'khai 4: AI chỉ ở nhà ≥ 4 px/m → (b) sạch', bad(bmn_row(dict(be_mat_nha_px_m_min=4), dict(t5, ghep=os.path.join(TMP, 'g54.png'))), 'b'), False)
r15 = bmn_row(dict(be_mat_nha_px_m_min=1.5))
case('px/m', 'khai 1,5 (< sàn 2) → (w) báo khai sai, dùng 2', [x for x in r15['loi'] if x.startswith('(w)') and 'be_mat_nha_px_m_min' in x], True)
case('px/m', 'khai 1,5 → ngưỡng thực dùng = 2', [] if r15.get('px_m_min') == 2.0 else [r15.get('px_m_min')], False)

# ---------------------------------------------------------------------- KN-4: (w) cạnh màu mới (ống khói AI vẽ thêm)
P_ = dict(K.BMN, A_MIN=100, N_MIN=40)
k_s = K.kiem_bmn(t5, '.', False, {}, None, 'London', True, P_)
case('KN-4 (w)', 'chỉ đổi bề mặt (albedo + nhiễu 3 %) → không (w) cạnh màu mới', [x for x in k_s['canh_bao'] if 'cạnh màu mới' in x], False)
Gc = G5.copy()
for hc in (9, 23, 37):   # ống khói gạch 2,5 × 4 m giữa mái nắng, thêm chụp
    ys, xs = np.nonzero(I5 == hc); xc, yc = int(xs.min()) + 9, int(ys.min()) + 9
    Gc[yc:yc + 16, xc:xc + 10] = (40, 70, 150); Gc[yc:yc + 3, xc - 1:xc + 11] = (30, 40, 60)
k_c = K.kiem_bmn(dict(t5, ghep=luu('gc.png', Gc)), '.', False, {}, None, 'London', True, P_)
case('KN-4 (w)', 'AI vẽ thêm 3 ống khói trong lòng mái → (w) cạnh màu mới', [x for x in k_c['canh_bao'] if 'cạnh màu mới' in x], True)
case('KN-4 (w)', f"ống khói thêm: hình khối (a) KHÔNG Chặn (lý do của KN-4) — {k_c['so'].get('canh_moi')} cụm", [x for x in k_c['loi'] if x.startswith('(a)')], False)
case('cấp', 'BE-MAT-NHA (w) cạnh màu mới ở G2 → Cảnh báo (CHỈ BÁO)', cap112.cap('BE-MAT-NHA', dict(loi=['(w) tấm x: 3 cụm cạnh màu mới'], cong='G2'))[1], False)

# ---------------------------------------------------------------------- KN-3: gọi lại Claude 1 lần khi không đọc đủ ảnh (mô hình nhìn giả lập)
def gia_lap(reads_seq):
    seq = list(reads_seq); log = []
    def call_claude(pr, td, tag, out=None):
        n = seq.pop(0); imgs = sorted(os.path.join(td, f) for f in os.listdir(td))
        log.append(dict(tag=tag, so_anh_doc=n)); return '{"loi_thoi_dai": [], "hinh_khoi": []}', dict(model=[QV.CLAUDE], usd=0.05, reads=imgs[:n], loi=None)
    def call_gpt(pr, imgs, tag, out=None): return '{"loi_thoi_dai": [], "hinh_khoi": []}', dict(model=QV.GPT, usd=0.03, loi=None)
    return call_claude, call_gpt, log


_cc, _cg = QV.call_claude, QV.call_gpt
try:
    for seq_, ex, nm in (([2, 10], False, 'lần 1 đọc 2/10, lần 2 đủ → không THIẾU'), ([6, 3], True, 'thiếu cả hai lần → THIẾU (c)'), ([10], False, 'đủ ngay lần 1 → không gọi lại')):
        cc, cg, lg = gia_lap(seq_); QV.call_claude, QV.call_gpt = cc, cg
        od = os.path.join(TMP, f'kn3-{len(seq_)}-{seq_[0]}'); V = K.soi_bmn(F5['render'], t5['ghep'], 1938, 'London', True, od, 'kn3', True, {})
        case('KN-3 (c)', f"BMN: {nm} (gọi Claude {len(lg)} lần)", [V['loi']] if V.get('loi') else [], ex)
        so = [json.loads(x) for x in open(os.path.join(od, 'n2p-cost.jsonl'))] if os.path.exists(os.path.join(od, 'n2p-cost.jsonl')) else []
        case('KN-3 sổ', f"BMN: {nm} → sổ n2p-cost ghi {len(lg)} lần (dòng KN-3)", [] if len([x for x in so if x.get('ghi') == 'K-1.17.6 KN-3']) == len(lg) else [so], False)
    cc, cg, lg = gia_lap([2, 10]); QV.call_claude, QV.call_gpt = cc, cg
    Vn = QV.soi(F5['render'], t5['ghep'], 1938, 'London', True, os.path.join(TMP, 'kn3n'), 'kn3n', True, {})
    case('KN-3 N2P', 'N2P (q_n2p_vision.soi): lần 1 thiếu ảnh, lần 2 đủ → không THIẾU', [Vn['loi']] if Vn.get('loi') else [], False)
finally:
    QV.call_claude, QV.call_gpt = _cc, _cg

# ====================================================================== cảnh B: nhà lớn 1080p, bóng quét qua nhà, video 640×360 — KN-5, KN-6
HB, WB = 1080, 1920
IB = np.zeros((HB, WB), np.int64); PB = np.zeros((HB, WB), np.int64); LB = np.zeros((HB, WB, 3), np.uint8); LB[:] = (200, 170, 90)
nhaB = []; k = 0
for r_ in range(2):
    for c_ in range(5):
        k += 1; x0, y0 = 80 + c_ * 360, 120 + r_ * 470; IB[y0:y0 + 380, x0:x0 + 300] = k
        PB[y0:y0 + 120, x0:x0 + 300] = k * 10 + 1; PB[y0 + 120:y0 + 380, x0:x0 + 300] = k * 10 + 2
        nhaB.append(dict(id=k, lo=1, px_m=12.0))
LB[IB > 0] = (215, 215, 215)
yy, xx = np.mgrid[0:HB, 0:WB]
rg = np.random.default_rng(11)
ArB = np.ones((HB, WB, 3), np.float32) * np.array([0.45, 0.5, 0.55], np.float32)
for h_ in range(1, k + 1): ArB[IB == h_] = rg.uniform(0.2, 0.4, 3)   # không bão hoà: albedo × bóng ≤ 1
tex = (0.6 + 0.8 * ((xx // 2 + yy // 2) % 2)).astype(np.float32)[..., None]   # vân mịn 2 px tương phản cao (mất khi thu 1080 → 360)
AaiB = ArB.copy()
for h_ in range(1, k + 1):   # AI PHÂN BỐ LẠI độ sáng bề mặt: nửa trái sáng, nửa phải tối (cửa/tường khác chỗ render)
    m = IB == h_; xm = xx[m].min() + 150; AaiB[m & (xx < xm)] *= 1.5; AaiB[m & (xx >= xm)] *= 0.55
AaiB = np.clip(AaiB * tex, 0, 0.9)


def SB(i, n=12):
    """bóng quét: đường bóng chéo chạy ngang qua nhà; nắng tăng 20 % trong clip; mái (mặt 1) 0,55×, nền 0,6× (pass bóng thấy hình khối)"""
    edge = 300 + i * (WB + 200) / (n - 1); lit = (xx + 0.6 * yy) < edge
    S = cv2.GaussianBlur(np.where(lit, 0.9, 0.36).astype(np.float32), (0, 0), 1.5)   # mép bóng mềm; mép hình học sắc
    S[PB % 10 == 1] *= 0.55; S[IB == 0] *= 0.6
    return S * (1.0 + 0.2 * i / (n - 1))


def l2s(x): x = np.clip(x, 0, 1); return np.where(x <= 0.0031308, x * 12.92, 1.055 * x ** (1 / 2.4) - 0.055)
to8 = lambda A, S: np.round(l2s(A * S[..., None]) * 255).astype(np.uint8)   # ảnh = sRGB(albedo × bóng TUYẾN TÍNH)
BB = to8(np.full((HB, WB, 3), 0.6, np.float32), SB(0))
RtB = [to8(ArB, SB(i)) for i in range(12)]
Mb = cv2.dilate((IB > 0).astype(np.uint8), np.ones((3, 3), np.uint8)) > 0
gB = lambda fr: [np.where(Mb[..., None], c_, r_) for c_, r_ in zip(fr, RtB)]
dungB = gB([to8(AaiB, SB(i)) for i in range(12)]); tinhB = gB([to8(AaiB, SB(0))] * 12)
nhapB = gB([np.clip(to8(AaiB, SB(i)) * (1 + np.random.default_rng(i).normal(0, 0.08, (HB, WB, 1))), 0, 255).astype(np.uint8) for i in range(12)])
chongB = gB([to8(AaiB * 0.6, SB(i)) for i in range(12)])   # ánh sáng chồng 2 lần ≈ tối hơn tấm
FB = dict(render=luu('rb.png', RtB[0]), mat_na=luu('lb.png', LB[..., ::-1]), mat_na_nha=luu('ib.png', ma24(IB)), mat_na_mat=luu('pb.png', ma24(PB)), bong=luu('bb.png', BB),
          ghep=luu('gb.png', dungB[0]), nam=1938, id='tb', be_mat_nha_ai=True)
json.dump(nhaB, open(os.path.join(TMP, 'nb.json'), 'w')); FB['nha'] = os.path.join(TMP, 'nb.json')
rvB = mp4('rb.mp4', RtB, (640, 360)); tamB = FB['ghep']   # tấm đã duyệt = khung 0 1080p
PB_ = dict(K.BMN)
for nm, fr, cach, ex, muc in (('albedo AI phân bố lại + bóng quét, dựng lại ánh sáng đúng (tỉ số bóng / chiếu 3D)', dungB, 'chieu_3d', False, 'de'),
                              ('dán ảnh tĩnh khi nắng đổi', tinhB, 'anh_tinh', True, 'd'), ('nhiễu bề mặt mỗi khung', nhapB, 'chieu_3d', True, 'd'),
                              ('chiếu 3D không khử sáng (khung 0 lệch tấm)', chongB, 'chieu_3d', True, 'e')):
    gv = mp4('gb.mp4', fr, (640, 360))
    kv = K.kiem_bmn(dict(FB, be_mat_nha_video=dict(ghep=gv, render=rvB, cach=cach, tam=tamB)), '.', False, {}, None, 'London', True, PB_)
    vd = kv['so'].get('video') or {}
    case(f'KN-5/6 ({muc})', f"{nm} → ({muc}) · % nhà lệch {vd.get('pct_lech')} (1.17.5: {vd.get('pct_lech_1175')}) · nhấp nháy {vd.get('nhap_be_mat')} · ΔE khung 0 {vd.get('t0_dE_tb')}/{vd.get('t0_dE_p95')} @{vd.get('t0_co')}",
         [x for x in kv['loi'] if any(x.startswith(f'({m})') for m in muc)], ex)
    if nm.startswith('albedo'):
        case('KN-5 (d)', f"thước 1.17.5 (TB theo nhà) trên cùng video dựng đúng: {vd.get('pct_lech_1175')} % nhà lệch > 2 % → trượt oan (để so)", ['trượt'] if (vd.get('pct_lech_1175') or 0) > 2 else [], True)
        # KN-6: thước 1.17.5 (video phóng lên W/2 so tấm thu W/2) trên cùng khung 0
        C0o = K76.frames_video(gv, None, 1)[0][0]; C0u = cv2.resize(C0o, (960, 540), interpolation=cv2.INTER_LINEAR); T0u = cv2.resize(cv2.imread(tamB), (960, 540), interpolation=cv2.INTER_AREA)
        I2u = cv2.resize(IB.astype(np.int32), (960, 540), interpolation=cv2.INTER_NEAREST); dEu = np.sqrt(((K._lab(C0u) - K._lab(T0u)) ** 2).sum(-1))[I2u > 0]
        case('KN-6 (e)', f'thước 1.17.5 (video 640 phóng 960 ↔ tấm 1080 thu 960): ΔE TB {dEu.mean():.1f} p95 {np.percentile(dEu, 95):.1f} → trượt oan (để so)',
             ['trượt'] if (dEu.mean() > K.BMN['T0_DE'] or np.percentile(dEu, 95) > K.BMN['T0_P95']) else [], True)
qp = K76.quy_dao_px([f for f in dungB[:3]], [f for f in RtB[:3]], IB)
case('KN-5 quy_dao_px', f"dựng đúng ở 1080p (không mã hoá): e lớn nhất {max(qp['e_h'].values()):.4f} ≈ 0", [] if max(qp['e_h'].values()) < 0.02 else [qp['e_h']], False)

# sàn độ sáng (M1: nắng tắt dần, khung cuối Y ≈ 0,005): dựng đúng phải ĐẠT, dán tĩnh vẫn TRƯỢT
toi = lambda i: (1.0 - 0.95 * i / 11) ** 2   # tắt nắng: hệ số 1 → 0,0025
th = lambda F: [cv2.resize(f_, (640, 360), interpolation=cv2.INTER_AREA) for f_ in F]
RtT = th([to8(ArB, SB(i) * toi(i)) for i in range(12)])
dungT = th(gB([to8(AaiB, SB(i) * toi(i)) for i in range(12)])); tinhT = th(gB([to8(AaiB, SB(0))] * 12))
I3 = cv2.resize(IB.astype(np.int32), (640, 360), interpolation=cv2.INTER_NEAREST)
for nm, fr, ex in (('dựng đúng khi nắng tắt dần (khung cuối gần đen)', dungT, False), ('dán tĩnh khi nắng tắt dần', tinhT, True)):
    q_ = K76.quy_dao_px(fr, RtT, I3); e_ = np.array(list(q_['e_h'].values())); p_ = float((e_ > K.BMN['E_MAX']).mean() * 100)
    q0 = K76.quy_dao_px(fr, RtT, I3, y_san=0.0); p0 = float((np.array(list(q0['e_h'].values())) > K.BMN['E_MAX']).mean() * 100)
    case('KN-5 sàn Y', f'{nm}: % nhà lệch {p_:.1f} (không sàn: {p0:.1f})', [p_] if p_ > K.BMN['NHA_LECH_PCT'] else [], ex)

# ====================================================================== TU-LIEU-10 / TU-LIEU-OMNI (chủ dự án 24/10 12:52)
def LS_(*sh):
    out, t = [], 0.0
    for nm, d, kw in sh: out.append(dict(dict(shot=nm, t0=t, t1=t + d, dur=d, cu_may='CODINH'), **kw)); t += d
    return out


E4 = dict(id='t4', kenh2_tu_t4=True); E15 = dict(E4, tu_lieu_tran_pct=15)
L14 = LS_(('a', 8, dict(lop=dict(TL=7))), ('b', 30, {}), ('c', 8, dict(lop=dict(KHAC=7))), ('d', 54, {}))   # 14 %
L16 = LS_(('a', 9, dict(lop=dict(TL=9))), ('b', 30, {}), ('c', 8, dict(lop=dict(KHAC=7))), ('d', 53, {}))   # 16 %
case('TU-LIEU-10 (a)', 'khai 15: 14 % → sạch', bad(K76.tu_lieu_10(E15, None, L14), 'a'), False)
case('TU-LIEU-10 (a)', 'khai 15: 16 % → (a)', bad(K76.tu_lieu_10(E15, None, L16), 'a'), True)
case('TU-LIEU-10 (a)', 'không khai (mặc định 10): 14 % → (a)', bad(K76.tu_lieu_10(E4, None, L14), 'a'), True)
case('TU-LIEU-10 (a)', 'không khai: 10 % → sạch (giữ hành vi 1.17.4)', bad(K76.tu_lieu_10(E4, None, LS_(('a', 6, dict(lop=dict(TL=4, KHAC=3, THE=3))), ('b', 94, {}))), 'a'), False)
case('TU-LIEU-10 (k)', 'khai 20 (> 15 % đã duyệt) → (k) Chặn, dùng 10', bad(K76.tu_lieu_10(dict(E4, tu_lieu_tran_pct=20), None, L14), 'k'), True)
case('TU-LIEU-10 (b)', 'một lần tư liệu 12 s → (b)', bad(K76.tu_lieu_10(E15, None, LS_(('a', 14, dict(lop=dict(TL=12))), ('b', 86, {}))), 'b'), True)
case('TU-LIEU-10 (b)', 'một lần tư liệu 10 s → sạch', bad(K76.tu_lieu_10(E15, None, LS_(('a', 12, dict(lop=dict(TL=10))), ('b', 88, {}))), 'b'), False)
case('TU-LIEU-10 (b)', 'tu_lieu_lan khai giờ: 2 lần 6 s trong một shot → sạch', bad(K76.tu_lieu_10(E15, None, LS_(('a', 20, dict(lop=dict(TL=12), tu_lieu_lan=[dict(t0=1, t1=7), dict(t0=12, t1=18)])), ('b', 80, {}))), 'b'), False)
md = dict(minh_hoa=True, cu_may='MD')
case('TU-LIEU-OMNI (a)', 'tư liệu trên chính clip M-d (shot vừa minh_hoa vừa TL) → (a)', bad(K76.tu_lieu_omni(E15, None, LS_(('a', 6, dict(md, lop=dict(TL=3))), ('b', 20, {}))), 'a'), True)
case('TU-LIEU-OMNI (a)', 'tu_lieu_lan chồng giờ clip M-d kề → (a)', bad(K76.tu_lieu_omni(E15, None, LS_(('a', 10, dict(lop=dict(TL=4), tu_lieu_lan=[dict(t0=7, t1=11)])), ('m', 6, md), ('b', 20, {}))), 'a'), True)
case('TU-LIEU-OMNI (b)', 'shot tư liệu liền trước clip M-d, không khai giờ → (b) ghép liền', bad(K76.tu_lieu_omni(E15, None, LS_(('a', 8, dict(lop=dict(TL=8))), ('m', 6, md), ('b', 20, {}))), 'b'), True)
case('TU-LIEU-OMNI (b)', 'giữa tư liệu và clip M-d có 1 shot 3D → sạch', bad(K76.tu_lieu_omni(E15, None, LS_(('a', 8, dict(lop=dict(TL=8))), ('x', 4, {}), ('m', 6, md), ('b', 20, {}))), 'ab'), False)
case('TU-LIEU-OMNI (b)', 'tư liệu kết thúc 1,5 s trước cuối shot 3D rồi tới clip M-d (hoà qua 3D ≥ 1 s) → sạch',
     bad(K76.tu_lieu_omni(E15, None, LS_(('a', 10, dict(lop=dict(TL=6), tu_lieu_lan=[dict(t0=2, t1=8.5)])), ('m', 6, md))), 'ab'), False)
case('TU-LIEU-OMNI (b)', 'tư liệu kết thúc 0,5 s trước clip M-d → (b)', bad(K76.tu_lieu_omni(E15, None, LS_(('a', 10, dict(lop=dict(TL=6), tu_lieu_lan=[dict(t0=3, t1=9.5)])), ('m', 6, md))), 'b'), True)
case('TU-LIEU-OMNI (b)', 'clip M-d TRƯỚC, tư liệu ngay sau (thẻ) → (b)', bad(K76.tu_lieu_omni(E15, None, LS_(('m', 6, md), ('a', 5, dict(lop=dict(THE=5))), ('b', 20, {}))), 'b'), True)
case('TU-LIEU-OMNI', 'không clip M-d → sạch', bad(K76.tu_lieu_omni(E15, None, L14)), False)
out74 = K74.check(E15, None, '.', L14)
case('TU-LIEU (q_k1174.check)', 'q_k1174.check trả TU-LIEU-10 theo trần tập (15) + hàng TU-LIEU-OMNI', [] if ('TU-LIEU-OMNI' in out74 and out74['TU-LIEU-10'].get('tran') == 15.0 and out74['TU-LIEU-10']['ok']) else [out74.get('TU-LIEU-10')], False)
case('cấp', 'TU-LIEU-OMNI (b) ở G2 → Chặn', cap112.cap('TU-LIEU-OMNI', dict(loi=['(b) x'], cong='G2'))[1], True)
case('cấp', 'TU-LIEU-OMNI ở animatic → Cảnh báo', cap112.cap('TU-LIEU-OMNI', dict(loi=['(b) x'], cong='animatic'))[1], False)
case('cấp', 'TU-LIEU-10 (b) ở G2 → Chặn', cap112.cap('TU-LIEU-10', dict(loi=['(b) x'], cong='G2'))[1], True)
case('áp dụng', 'tập T3 → TU-LIEU-10/OMNI (1.17.6) KHÔNG ÁP', [k_ for k_, v in K76.check_tu_lieu(dict(id='t3'), None, '.', L14).items() if v.get('ket_qua') != 'KHÔNG ÁP'], False)

# ---------------------------------------------------------------------- in kết quả
ok = all(x[3] for x in R)
for rule, name, kv, good, got in R: print(f"{'ĐÚNG' if good else 'SAI '} [{rule}] {name} — kỳ vọng {kv}" + ('' if good else f' · được {got}'))
print(f"\nselftest_k1176: {sum(x[3] for x in R)}/{len(R)} ca đúng kỳ vọng — {'ĐẠT' if ok else 'TRƯỢT'}")
sys.exit(0 if ok else 1)
