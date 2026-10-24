#!/opt/cine/bin/python
"""Tự kiểm luật 1.17.5 (phiên K-1.17.5, 24/10/2026). Mỗi luật đổi/mới ≥ 1 ca ĐẠT + ≥ 1 ca TRƯỢT. Không mạng, không API.
Fixtures (checks/ll/fixtures/k1175/): T6 tiền kỳ T4 (render-khớp + ghép lượt 2, 960×540 JPEG q95 phóng lại 1920×1080; mặt nạ ID gốc 1920×1080 trong git)
và cảnh Blender có đáp án (reports/k1175/do/canh_tong_hop.py: gốc, nước ô-liu, nhám 0,10, bờ lấn) — mặt nạ đúng độ phân giải khung.
  N2P-3 T9c (A1/A2): render ↔ chính nó đạt; nước đổi sắc xám/ô-liu (bờ giữ) đạt dù T9b nước→đất > 2 %; bờ lấn 8/16/40 px trượt (c); T6 lượt 2 thật
       (bờ bắc lấn — D11) trượt; Blender: phản chiếu VẬT LÝ + nước ô-liu đạt, bờ lấn hình học trượt; phản chiếu AI tự vẽ thêm (không có ở render) trượt.
  N2P-1 (e) lớp sống (A3): cộng hiệu đúng đạt; dán nguyên / lệch 6 px / nửa cường độ trượt; (iv) soi tấm nền.
  N2P-1 (d) vòng khớp màu cục bộ (A4): một độ lệch/vật đạt; đổi không đều / độ lệch > trần trượt.
  BE-MAT-NHA (A5): (a) hình khối, (b) khoá 0/255, (c) đọc trả lời mô hình (bộ đệm), (d) quỹ đạo sáng + nhấp nháy, (e) khung 0 chiếu 3D; cấp; áp dụng.
  /opt/cine/bin/python checks/ll/selftest_k1175.py        mã thoát 0 = mọi ca đúng kỳ vọng"""
import copy, json, os, sys, tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, ROOT)
import numpy as np  # noqa: E402
import cv2  # noqa: E402
from checks.ll import q_n2p as NP, q_k1175 as K, cap112  # noqa: E402

TMP = tempfile.mkdtemp(prefix='k1175-'); R = []; F = os.path.join(ROOT, 'checks/ll/fixtures/k1175')


def case(rule, name, got, expect_fail):
    got = list(got) if got else []
    R.append((rule, name, 'bắt lỗi' if expect_fail else 'sạch', bool(got) == expect_fail, got[:2]))


def bad(x, *muc):
    L = (x.get('loi') or []) + (x.get('thieu') or [])
    return [y for y in L if not muc or any(y.startswith(f'({m})') for m in muc)]


up = lambda p: cv2.resize(cv2.imread(os.path.join(F, p)), (1920, 1080), interpolation=cv2.INTER_CUBIC)
lan9c = lambda d: [f"bờ lấn sâu {x['sau_px']} px" for x in d['lan']] + ([f"giữa nước {d['giua_pct']} %"] if d['giua_pct'] > K.T9C['GIUA'] else [])

# ====================================================================== N2P-3 T9c — T6 (mặt nạ trong git)
R6 = up('t6-render.jpg'); L6, n6 = NP.idmap(os.path.join(F, 't6-matna.png'), (1920, 1080)); W6 = L6 == n6.index('nuoc')
top6 = W6 & np.vstack([np.zeros((1, 1920), bool), ((L6 != n6.index('nuoc')) & (L6 != n6.index('troi')))[:-1]])


def doi_mau(G, Wt, a, b, kl):
    lab = cv2.cvtColor(G, cv2.COLOR_BGR2LAB).astype(np.float32); m = lab[..., 0][Wt].mean()
    lab[..., 0][Wt] = np.clip((lab[..., 0][Wt] - m) * 0.9 + m * kl, 0, 255); lab[..., 1][Wt] = 128 + a + (lab[..., 1][Wt] - 128) * 0.25; lab[..., 2][Wt] = 128 + b + (lab[..., 2][Wt] - 128) * 0.25
    X = cv2.cvtColor(np.clip(lab, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR); al = cv2.GaussianBlur(Wt.astype(np.float32), (0, 0), 0.8)[..., None]
    return np.clip(G * (1 - al) + X * al, 0, 255).astype(np.uint8)


def lan(G, top, x0, x1, d, Wt):
    out = G.copy(); ys, xs = np.nonzero(top[:, x0:x1 + 1]); xs = xs + x0; y0 = {}
    for y, x in zip(ys, xs): y0[x] = min(y0.get(x, 9999), y)
    for x, y in y0.items():
        for j in range(d):
            if y + j < G.shape[0] and Wt[y + j, x]: out[y + j, x] = G[max(0, y - 2 - (j * 3) % 9), min(G.shape[1] - 1, x + 23)]
    return out


case('N2P-3 T9c', 'T6 render ↔ chính nó → sạch', lan9c(K.t9c(R6, R6, L6, n6)), False)
Gx = doi_mau(R6, W6, 0, 0, 0.6); Go = doi_mau(R6, W6, -6, 14, 0.7)
case('N2P-3 T9c', 'A2: nước đổi XÁM, bờ giữ → sạch', lan9c(K.t9c(R6, Gx, L6, n6)), False)
case('N2P-3 T9c', 'A2: nước đổi Ô-LIU, bờ giữ → sạch', lan9c(K.t9c(R6, Go, L6, n6)), False)
b9 = NP.do_tam.__doc__ and None
cv2.imwrite(os.path.join(TMP, 'r6.png'), R6); cv2.imwrite(os.path.join(TMP, 'go.png'), Go); MP6 = os.path.join(F, 't6-matna.png')
D_o = NP.do_tam(os.path.join(TMP, 'r6.png'), os.path.join(TMP, 'go.png'), MP6)
case('N2P-3 T9c', f"A2 đối chứng: luật cũ T9b nước→đất {D_o['iii']['t9b_nuoc_thanh_dat_pct']} % > 2 % (lỗi cũ có thật)", ['T9b > 2'] if D_o['iii']['t9b_nuoc_thanh_dat_pct'] > 2 else [], True)
case('N2P-3 T9c', 'A2 qua tong_tam 1.17.5: nước ô-liu → N2P-3 không (a)/(c)/(d)', bad(NP.tong_tam([dict(id='o', do={k: v for k, v in D_o.items() if not k.startswith('_')}, V={}, L1=[], L2=[], L2b=[], L4=[], VUNG=[], Q=None)])['N2P-3'], 'a', 'c', 'd'), False)
col = np.nonzero(top6.any(0))[0]; xs_ = [int(x) for x in (300, 900, 1500) if x in set(col.tolist())] or [int(col[len(col) // 2])]
for dd in (8, 16, 40):
    Gl = Go.copy()
    for x0 in xs_: Gl = lan(Gl, top6, x0, x0 + 100, dd, W6)
    case('N2P-3 T9c', f'bờ lấn {dd} px × 100 px (nước ô-liu) → (c)', lan9c(K.t9c(R6, Gl, L6, n6)), True)
G2 = up('t6-l2-ghep.jpg'); d2 = K.t9c(R6, G2, L6, n6)
case('N2P-3 T9c', f"T6 lượt 2 thật (D11: bờ bắc lấn) → trượt ({d2['so_doan_lan']} đoạn, sâu nhất {d2['sau_lon_nhat_px']} px)", lan9c(d2), True)
# ---------------------------------------------------------------------- Blender: phản chiếu vật lý
BL = {'nha_thuong': (215, 215, 215), 'troi': (110, 152, 229)}
Rb = up('bl-goc.jpg'); Lb, nb = NP.idmap(os.path.join(F, 'bl-matna.png'), (1920, 1080), BL)
case('N2P-3 T9c', 'Blender: render có phản chiếu vật lý ↔ chính nó → sạch', lan9c(K.t9c(Rb, Rb, Lb, nb)), False)
case('N2P-3 T9c', 'Blender: phản chiếu vật lý + nước ô-liu (A1: phản chiếu có trong render) → sạch', lan9c(K.t9c(Rb, up('bl-oliu.jpg'), Lb, nb)), False)
case('N2P-3 T9c', 'Blender: phản chiếu vật lý, mặt nước nhám 0,10 → sạch', lan9c(K.t9c(Rb, up('bl-pc1.jpg'), Lb, nb)), False)
case('N2P-3 T9c', 'Blender: bờ lấn hình học (bãi/bến 10–80 m) → (c)', lan9c(K.t9c(Rb, up('bl-lan2.jpg'), Lb, nb)), True)
# phản chiếu AI tự vẽ (không có ở render): lật nhà trên bờ xuống nước, tối 0,6
Gr = R6.copy(); ys, xs = np.nonzero(top6)
for y, x in zip(ys[::1], xs[::1]):
    for j in range(30):
        if y + j < 1080 and W6[y + j, x] and y - 14 - j >= 0: Gr[y + j, x] = (0.45 * Gr[y + j, x] + 0.55 * 0.6 * R6[y - 14 - j, x]).astype(np.uint8)
case('N2P-3 T9c', 'A1: phản chiếu AI tự vẽ thêm (render không có) dọc bờ → trượt (không miễn)', lan9c(K.t9c(R6, Gr, L6, n6)), True)

# ====================================================================== N2P-1 (e) lớp sống (A3) — T6
A6 = NP.lop(L6, n6, NP.LOP_A); Ab = K.bao_ve(A6)
rg = np.random.default_rng(1175); al = np.zeros((1080, 1920), np.float32)
for _ in range(10):
    x, y = int(rg.integers(200, 1700)), int(rg.integers(330, 640))
    for j in range(40): cv2.circle(al, (int(x + j * 0.9), int(y - j * 2.2)), int(2 + j * 0.25), float(0.5 * (1 - j / 40)), -1)
al = cv2.GaussianBlur(al, (0, 0), 2.0)[..., None]; Rk = R6; Rc = np.clip(R6 * (1 - al) + np.array([200, 200, 205], np.float32) * al, 0, 255).astype(np.uint8)
Pn = Go.copy(); Pn[Ab] = Rc[Ab]
Hd = Rc.astype(np.int16) - Rk.astype(np.int16)
Gd = np.clip(Pn.astype(np.int16) + Hd * (~Ab)[..., None], 0, 255).astype(np.uint8)
Gdan = Pn.copy(); m8 = (np.abs(Hd).max(-1) > 8) & ~Ab; Gdan[m8] = Rc[m8]
Glech = np.clip(Pn.astype(np.int16) + np.roll(Hd, 6, 1) * (~Ab)[..., None], 0, 255).astype(np.uint8)
Gnua = np.clip(Pn.astype(np.int16) + (Hd // 2) * (~Ab)[..., None], 0, 255).astype(np.uint8)
for nm, G_, ex in (('cộng hiệu đúng', Gd, False), ('dán nguyên điểm render (cách T6)', Gdan, True), ('lớp sống lệch 6 px', Glech, True), ('nửa cường độ', Gnua, True)):
    mx, cnt = K.kiem_song(G_, Pn, Rc, Rk, Ab); case('N2P-1 (e)', f'lớp sống: {nm} → sai lớn nhất {mx}/255', [f'{mx}'] if mx > 1 else [], ex)
for p_, G_ in (('rc.png', Rc), ('rk.png', Rk), ('pn.png', Pn), ('gd.png', Gd), ('gdan.png', Gdan)): cv2.imwrite(os.path.join(TMP, p_), G_)
cv2.imwrite(os.path.join(TMP, 'rkm.png'), Rc)
song = dict(render_co=os.path.join(TMP, 'rc.png'), render_khong=os.path.join(TMP, 'rk.png'), nen=os.path.join(TMP, 'pn.png'))
for g_, ex in (('gd.png', False), ('gdan.png', True)):
    kt = NP.kiem_tam(dict(id='s', render=os.path.join(TMP, 'rkm.png'), ghep=os.path.join(TMP, g_), mat_na=MP6, nam=1666, song=song), '.', False, {}, None)
    case('N2P-1 (e)', f'kiem_tam + tong_tam: {g_} → (e)', bad(NP.tong_tam([kt])['N2P-1'], 'e'), ex)
case('N2P-1 (e)', 'mô hình nhìn (iv) soi TẤM NỀN khi khai lớp sống (khoá bộ đệm theo nen.png)', [] if kt['V'].get('khoa') == __import__('checks.ll.q_n2p_vision', fromlist=['x']).khoa(os.path.join(TMP, 'rkm.png'), song['nen'], 1666, '', False, ('gpt', 'claude')) else ['khoá sai'], False)
kt2 = NP.kiem_tam(dict(id='s2', render=os.path.join(TMP, 'rkm.png'), ghep=os.path.join(TMP, 'gd.png'), mat_na=MP6, nam=1666, song=dict(song, nen=None)), '.', False, {}, None)
case('N2P-1 (e)', 'khai song thiếu nen → THIẾU (e)', bad(NP.tong_tam([kt2])['N2P-1'], 'e'), True)

# ====================================================================== N2P-1 (d) vòng bảo vệ khớp màu cục bộ (A4)
n_, cc = cv2.connectedComponents(Ab.astype(np.uint8), 8); Gv = Rc.copy().astype(np.int16)
for i in range(1, min(n_, 400)):
    ring = (cc == i) & ~A6; Gv[ring] += np.array([int(rg.integers(-12, 13)) for _ in range(3)], np.int16)
Gv = np.clip(Gv, 0, 255).astype(np.uint8); res, off, k_ = K.kiem_vong(Gv, Rc, A6, Ab)
case('N2P-1 (d)', f'vòng = render-khớp + một độ lệch/vật ({k_} vòng, phần dư {res:.0f}) → sạch', [res] if res > 1 or off > K.VONG_MAX else [], False)
Gw = Gv.copy(); ys, xs = np.nonzero(Ab & ~A6); Gw[ys[::3], xs[::3]] = 255
res2, _, _ = K.kiem_vong(Gw, Rc, A6, Ab); case('N2P-1 (d)', f'vòng đổi KHÔNG đều (vẽ lại mép) → phần dư {res2:.0f}', [res2] if res2 > 1 else [], True)
Gz = Rc.astype(np.int16); Gz[Ab & ~A6] += 60; Gz = np.clip(Gz, 0, 255).astype(np.uint8)
_, off3, _ = K.kiem_vong(Gz, Rc, A6, Ab); case('N2P-1 (d)', f'độ lệch {off3:.0f} > trần {K.VONG_MAX} → lỗi', [off3] if off3 > K.VONG_MAX else [], True)
cv2.imwrite(os.path.join(TMP, 'gv.png'), Gv); cv2.imwrite(os.path.join(TMP, 'gw.png'), Gw)
for g_, ex in (('gv.png', False), ('gw.png', True)):
    kt = NP.kiem_tam(dict(id='v', render=os.path.join(TMP, 'rkm.png'), ghep=os.path.join(TMP, g_), mat_na=MP6, nam=1666, khop_mau_cuc_bo=True), '.', False, {}, None)
    case('N2P-1 (d)', f'kiem_tam khop_mau_cuc_bo: {g_} → (d)', bad(NP.tong_tam([kt])['N2P-1'], 'd'), ex)
kt = NP.kiem_tam(dict(id='v0', render=os.path.join(TMP, 'rkm.png'), ghep=os.path.join(TMP, 'gw.png'), mat_na=MP6, nam=1666), '.', False, {}, None)
case('N2P-1 (d)', 'không khai khop_mau_cuc_bo → không đo vòng (luật cũ: (i) chỉ trong mặt nạ)', bad(NP.tong_tam([kt])['N2P-1'], 'd'), False)
case('cấp', 'N2P-1 (e) lớp sống ở G2 → Chặn', cap112.cap('N2P-1', dict(loi=['(e) x'], cong='G2'))[1], True)
case('cấp', 'N2P-1 (e) ở animatic → Cảnh báo', cap112.cap('N2P-1', dict(loi=['(e) x'], cong='animatic'))[1], False)

# ====================================================================== BE-MAT-NHA (A5) — cảnh tổng hợp: dãy nhà mái hồi 4 px/m (nhà 40 × 48 px)
H5, W5 = 540, 960; rg5 = np.random.default_rng(5)
I5 = np.zeros((H5, W5), np.int64); P5 = np.zeros((H5, W5), np.int64); S5 = np.full((H5, W5), 0.55, np.float32); L5 = np.zeros((H5, W5, 3), np.uint8)
L5[:] = (90, 170, 200)[::-1]; nha5 = []; hid = 0
for r_ in range(4):
    for c_ in range(14):
        hid += 1; x0, y0 = 40 + c_ * 62, 60 + r_ * 110; w_, hh = 44, 52
        I5[y0:y0 + hh, x0:x0 + w_] = hid; P5[y0 + 22:y0 + hh, x0:x0 + w_] = hid * 10 + 1; S5[y0 + 22:y0 + hh, x0:x0 + w_] = 0.62   # tường
        for yy in range(y0, y0 + 22):
            k_ = (yy - y0) / 22.0; xa, xb = int(x0 + w_ / 2 - k_ * w_ / 2), int(x0 + w_ / 2 + k_ * w_ / 2)
            P5[yy, xa:x0 + w_ // 2] = hid * 10 + 2; S5[yy, xa:x0 + w_ // 2] = 0.95; P5[yy, x0 + w_ // 2:xb] = hid * 10 + 3; S5[yy, x0 + w_ // 2:xb] = 0.35   # hai mái nắng/râm
            I5[yy, :] = np.where((np.arange(W5) >= xa) & (np.arange(W5) < xb), hid, I5[yy, :]) if True else I5[yy]
        L5[y0:y0 + hh, x0:x0 + w_] = (215, 215, 215); nha5.append(dict(id=hid, lo=r_ + 1, px_m=4.0))
alb = lambda seed: (np.random.default_rng(seed).uniform(0.35, 0.9, (hid + 1, 3)))
def anh(albedo, S=S5, nhieu=0.0, seed=0):
    A_ = albedo[I5] * S[..., None]; A_[I5 == 0] = np.array([0.55, 0.62, 0.50]) * S[I5 == 0][:, None]
    if nhieu: A_ = A_ * (1 + np.random.default_rng(seed).normal(0, nhieu, A_.shape))
    return np.clip(A_ * 255, 0, 255).astype(np.uint8)
def luu(nm, x): p_ = os.path.join(TMP, nm); cv2.imwrite(p_, x); return p_
def ma24(M): return np.stack([M & 255, (M >> 8) & 255, (M >> 16) & 255], -1).astype(np.uint8)
R5 = anh(alb(1)); B5 = np.clip(np.repeat(S5[..., None], 3, -1) * 0.6 * 255, 0, 255).astype(np.uint8)
L5[I5 > 0] = (215, 215, 215)
F5 = dict(render=luu('r5.png', R5), mat_na=luu('l5.png', L5[..., ::-1]), mat_na_nha=luu('i5.png', ma24(I5)), mat_na_mat=luu('p5.png', ma24(P5)), bong=luu('b5.png', B5))
json.dump(nha5, open(os.path.join(TMP, 'n5.json'), 'w')); F5['nha'] = os.path.join(TMP, 'n5.json')
P_ = dict(K.BMN, A_MIN=100, N_MIN=40)
def bmn(G, **kw):
    t = dict(F5, id='t5', ghep=luu('g5.png', G), nam=1666, **kw); return K.kiem_bmn(t, '.', False, {}, None, 'London', True, P_)
AI5 = anh(alb(7), nhieu=0.03, seed=3); Mh = cv2.dilate((I5 > 0).astype(np.uint8), np.ones((3, 3), np.uint8)) > 0
G5 = R5.copy(); G5[Mh] = AI5[Mh]
k5 = bmn(G5); case('BE-MAT-NHA (a)', f"bề mặt mới (albedo khác + nhiễu 3 %), hình khối giữ → không Chặn (a) ({k5['so'].get('nha_do')} nhà đo)", [x for x in k5['loi'] if x.startswith('(a)')], False)
case('BE-MAT-NHA (b)', 'bề mặt mới, ngoài vùng nhà = render → (b) sạch', [x for x in k5['loi'] if x.startswith('(b)')], False)
Gx = G5.copy(); m3 = I5 == 3; Gx[m3] = np.clip(np.array([0.55, 0.62, 0.50]) * 0.55 * 255, 0, 255).astype(np.uint8)   # xoá nhà 3 (thành nền)
kx = bmn(Gx); case('BE-MAT-NHA (a)', 'xoá một nhà (thay bằng nền) → Chặn (a)', [x for x in kx['loi'] if x.startswith('(a)') and 'nhà 3 ' in x], True)
A20 = AI5.copy(); m20 = I5 == 20; A20[m20] = np.clip(np.array([0.55, 0.62, 0.50]) * 0.55 * 255, 0, 255).astype(np.uint8)   # ảnh AI vẽ nhà 20 dời 10 px (2,5 m)
A20[np.roll(m20, 10, 1)] = np.roll(AI5, 10, 1)[np.roll(m20, 10, 1)]; Gd = R5.copy(); Gd[Mh] = A20[Mh]
kd = bmn(Gd); case('BE-MAT-NHA (a)', 'ảnh AI dời một nhà 2,5 m (10 px), ghép theo mặt nạ → cờ (a) Chặn hoặc (w) người đọc', [x for x in kd['loi'] + kd['canh_bao'] if ' nhà 20 ' in x], True)
Gb = G5.copy(); Gb[500:510, 10:30] = 0
kb = bmn(Gb); case('BE-MAT-NHA (b)', 'đổi 200 điểm ngoài vùng nhà đo được (lớp khoá) → (b)', [x for x in kb['loi'] if x.startswith('(b)')], True)
kn = bmn(G5, nen_ai=True); case('BE-MAT-NHA (b)', 'nen_ai: true (tấm cũng là tấm nền N2+) → nền không khoá ở đây', [x for x in kn['loi'] if x.startswith('(b)')], False)
P_s = dict(P_, PPM_MIN=5.0); kt5 = K.kiem_bmn(dict(F5, id='t5', ghep=luu('g5.png', G5), nam=1666), '.', False, {}, None, 'London', True, P_s)
case('BE-MAT-NHA (b)', 'nhà dưới ngưỡng đo (px/m < PPM_MIN) mà vẫn phủ AI → (b) (không đo được thì giữ render)', [x for x in kt5['loi'] if x.startswith('(b)')], True)
# (c) đọc trả lời mô hình từ bộ đệm (không gọi mạng)
from checks.ll import q_n2p_vision as QV  # noqa: E402
import hashlib  # noqa: E402
kc = hashlib.sha256(f"{QV.sha_file(F5['render'])}|{QV.sha_file(luu('g5.png', G5))}|1666|London|True|{K.PROMPT_BMN_VER}|{QV.GPT}|{QV.CLAUDE}".encode()).hexdigest()[:32]
def vc(items): return {kc: dict(ket_qua={'gpt': dict(json=dict(loi_thoi_dai=items, hinh_khoi=[]), meta={}), 'claude': dict(json=dict(loi_thoi_dai=[], hinh_khoi=[]), meta={})}, loi=None)}
k_c1 = K.kiem_bmn(dict(F5, id='t5', ghep=os.path.join(TMP, 'g5.png'), nam=1666, noi='London', t4=True), '.', False, vc([dict(mo_ta='air-conditioning unit on wall', toa_do=[0.1, 0.1, 0.2, 0.2], nam_xuat_hien=1950, do_tin=0.9)]), None, 'London', True, P_)
case('BE-MAT-NHA (c)', 'mô hình báo điều hoà (năm 1950 > 1666) → (c)', [x for x in k_c1['loi'] if x.startswith('(c)')], True)
k_c2 = K.kiem_bmn(dict(F5, id='t5', ghep=os.path.join(TMP, 'g5.png'), nam=1666, noi='London', t4=True), '.', False, vc([]), None, 'London', True, P_)
case('BE-MAT-NHA (c)', 'mô hình không báo gì → (c) sạch', [x for x in k_c2['loi'] + k_c2['thieu'] if x.startswith('(c)')], False)
k_c3 = K.kiem_bmn(dict(F5, id='t5', ghep=os.path.join(TMP, 'g5.png'), nam=1666, noi='London', t4=True), '.', False, vc([dict(mo_ta='odd glossy window', toa_do=[0, 0, 0.1, 0.1], nam_xuat_hien=None, do_tin=0.8)]), None, 'London', True, P_)
case('BE-MAT-NHA (c)', 'nghi vấn không năm → (w) người đọc, không (c)', [x for x in k_c3['loi'] if x.startswith('(c)')], False)
case('BE-MAT-NHA (c)', 'không bộ đệm, không --vision → THIẾU (c)', [x for x in k5['thieu'] if x.startswith('(c)')], True)
# (d)(e) timelapse: nắng đổi → bóng mái đổi
def mp4(nm, frames):
    p_ = os.path.join(TMP, nm); vw = cv2.VideoWriter(p_, cv2.VideoWriter_fourcc(*'mp4v'), 24, (W5, H5))
    for f_ in frames: vw.write(f_)
    vw.release(); return p_
Sx = [S5 * (1 + 0.0 * i) for i in range(1)]
def bong_t(i):
    S_ = S5.copy(); a_ = (P5 % 10 == 2); b_ = (P5 % 10 == 3); S_[a_] = 0.95 - 0.08 * i; S_[b_] = 0.35 + 0.08 * i; return S_
Rt = [anh(alb(1), bong_t(i)) for i in range(8)]
def ghep_t(At): return [np.where(Mh[..., None], a_, r_) for a_, r_ in zip(At, Rt)]
dung = ghep_t([anh(alb(7), bong_t(i)) for i in range(8)]); tinh = ghep_t([anh(alb(7), bong_t(0))] * 8)
nhap = ghep_t([anh(alb(7), bong_t(i), 0.08, i) for i in range(8)]); chong = ghep_t([np.clip(anh(alb(7), bong_t(i)) * 0.7, 0, 255).astype(np.uint8) for i in range(8)])
rv = mp4('rt.mp4', Rt); tam0 = luu('tam0.png', dung[0])   # tấm đã duyệt = ghép khung 0
for nm, fr, cach, ex, muc in (('dựng lại ánh sáng đúng (chiếu 3D)', dung, 'chieu_3d', False, 'de'), ('ảnh tĩnh dán khi nắng đổi', tinh, 'anh_tinh', True, 'd'),
                              ('nhiễu bề mặt mỗi khung', nhap, 'chieu_3d', True, 'd'), ('chiếu 3D không khử sáng (khung 0 lệch tấm)', chong, 'chieu_3d', True, 'e')):
    kv = bmn(G5, be_mat_nha_video=dict(ghep=mp4('g.mp4', fr), render=rv, cach=cach, tam=tam0))
    case(f'BE-MAT-NHA ({muc})', f'{nm} → ({muc})', [x for x in kv['loi'] if any(x.startswith(f'({m})') for m in muc)], ex)
case('BE-MAT-NHA (e)', 'cach không hợp lệ → THIẾU (e)', [x for x in bmn(G5, be_mat_nha_video=dict(ghep=mp4('g.mp4', dung), render=rv, cach='khac'))['thieu'] if x.startswith('(e)')], True)
# cấp + áp dụng
case('cấp', 'BE-MAT-NHA (a) ở G2 → Chặn', cap112.cap('BE-MAT-NHA', dict(loi=['(a) x'], cong='G2'))[1], True)
case('cấp', 'BE-MAT-NHA (a) ở animatic → Cảnh báo', cap112.cap('BE-MAT-NHA', dict(loi=['(a) x'], cong='animatic'))[1], False)
case('cấp', 'BE-MAT-NHA (w) ở G2 → Cảnh báo', cap112.cap('BE-MAT-NHA', dict(loi=['(w) x'], cong='G2'))[1], False)
case('áp dụng', 'tập T3 → BE-MAT-NHA KHÔNG ÁP', [] if K.be_mat_nha(dict(id='t3'))['ket_qua'] == 'KHÔNG ÁP' else ['áp'], False)
case('áp dụng', 'tập T4 không tấm be_mat_nha_ai → KHÔNG ÁP', [] if K.be_mat_nha(dict(id='t4', kenh2_tu_t4=True, n2p=dict(tam=[dict(id='x')])))['ket_qua'] == 'KHÔNG ÁP' else ['áp'], False)
EB = dict(id='t4', kenh2_tu_t4=True, n2p=dict(noi='London', t4=True, tam=[dict(F5, id='t5', ghep=os.path.join(TMP, 'g5.png'), nam=1666, be_mat_nha_ai=True)]))
case('áp dụng', 'tập T4 có tấm be_mat_nha_ai → hàng chạy (THIẾU (c) khi chưa soi)', bad(K.be_mat_nha(EB), 'c'), True)

# ---------------------------------------------------------------------- in kết quả
ok = all(x[3] for x in R)
for rule, name, kv, good, got in R: print(f"{'ĐÚNG' if good else 'SAI '} [{rule}] {name} — kỳ vọng {kv}" + ('' if good else f' · được {got}'))
print(f"\nselftest_k1175: {sum(x[3] for x in R)}/{len(R)} ca đúng kỳ vọng — {'ĐẠT' if ok else 'TRƯỢT'}")
sys.exit(0 if ok else 1)
