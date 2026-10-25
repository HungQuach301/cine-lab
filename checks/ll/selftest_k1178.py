#!/opt/cine/bin/python
"""Tự kiểm luật 1.17.8 (phiên K-1.17.8, 25/10/2026). Mỗi luật đổi/mới ≥ 1 ca ĐẠT + ≥ 1 ca TRƯỢT; ca "mặc định giữ hành vi cũ" cho mỗi tham số.
Không mạng, không API (mô hình nhìn giả lập bằng thay q_n2p_vision.soi). Ảnh tổng hợp dựng trong mã (1920×1080; không fixture lớn).
  LUẬT E (N2P-E + N2P-1…5 trên tấm E): ghép đúng → sạch · (k) năm < nam_min / không CODINH / nam_min < 2020 · AI vẽ lên toà có tên → N2P-1 (a) + (f1) ·
    toà khai mà mặt nạ không có → (f1) · thiếu toa_co_ten → THIẾU (f) · tháp bịa cao hơn mốc gần → (w), thấp hơn → sạch · chữ AI đêm → (g), ngày → (w) ·
    nhà thường đổi KHÔNG là (a) (tấm thường cùng ảnh → (a)) · T9b đất→nước chỉ in ở tấm E · mô hình: toà mất → N2P-1 (b), tháp bịa → (w), chữ đêm → (g),
    người → N2P-4 · BMN bỏ tấm E · N2P-5 video E dùng (a)-E · cấp G2/animatic · không tấm E → KHÔNG ÁP.
  K-LAI-3 ↔ KIEM-2-MUC: nen + Flash ĐẠT + tờ khung → ĐẠT (1.17.7 THIẾU) · nen thiếu tờ khung → THIẾU · Flash LOẠI → (b) · LOẠI + ngoai_le_duyet hợp lệ → ĐẠT ·
    duyệt có email → (b) · day_du thiếu kiem → THIẾU như cũ · KIEM-2-MUC (b) nhận ngoai_le_duyet ở nen.
  Q34 T4 nhận minh_hoa/tu_lieu/that; T3 không. Q26b-K2 T4: minh_hoa → 'minh_hoa'; T3 'khac'.
  SACH-1: log chữ khuôn khoảng = khuôn khung · vai §17 T4 hợp lệ trong giới hạn; vượt → (g); T3 vai §17 → (e) như cũ.
  Q37 (d): T4 khung tĩnh trong thẻ PP ≤ 10 s miễn; > 10 s / ngoài thẻ / T3 → (d).
  TU-LIEU-OMNI: chỉ clip M-d gần nhất (1.17.7 đếm trùng 3 → 2).  BIEN-CO-V: T4 dùng HIEU_CHUAN_T4 (chưa đạt) → không Chặn, cho_q37 rỗng; T3 như cũ.
  /opt/cine/bin/python checks/ll/selftest_k1178.py        mã thoát 0 = mọi ca đúng kỳ vọng"""
import copy, json, os, sys, tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, ROOT)
import numpy as np  # noqa: E402
import cv2  # noqa: E402
from checks.ll import q_k1178 as K78, q_n2p as NP, q_n2p_vision as QV, q_lai as LA, q_k1177 as K7, q_types as QTY, q_k2var as K2V, q_k116 as K6, q_nhip as QN, q_k1176 as K76, q_k1175 as K75, q_bcv as BCV, cap112  # noqa: E402

TMP = tempfile.mkdtemp(prefix='k1178-'); R = []


def case(rule, name, got, expect_fail):
    got = list(got) if got else []
    R.append((rule, name, 'bắt lỗi' if expect_fail else 'sạch', bool(got) == expect_fail, got[:2]))


def bad(x, *muc):
    L = (x.get('loi') or []) + (x.get('thieu') or [])
    return [y for y in L if not muc or any(y.startswith(f'({m})') for m in muc)]


E4 = dict(id='t4', kenh2_tu_t4=True); E3 = dict(id='t3', khung_sach=True)
P = lambda f: os.path.join(TMP, f)

# ====================================================================== ảnh tổng hợp LUẬT E
W, H = 1920, 1080
rng = np.random.default_rng(7)
TROI, NHA, NT, NUOC, BANG = (40, 80, 200), (235, 235, 235), (215, 215, 215), (0, 170, 190), (200, 170, 90)
M = np.zeros((H, W, 3), np.uint8); M[:] = TROI                       # mặt nạ lớp (RGB)
Rr = np.zeros((H, W, 3), np.uint8)                                   # render (BGR)
for y in range(H): Rr[y] = (235 - y // 8, 200 - y // 12, 170 - y // 14)   # trời
M[560:1000] = NT; Rr[560:1000] = (120, 125, 130)                     # dải nhà thường (chân trời y 560)
for x0 in range(0, W, 60):                                           # cửa sổ / mái — kết cấu nhà thường
    Rr[580:990, x0 + 5:x0 + 50] = (100 + (x0 // 60) % 5 * 10, 110, 125)
M[1000:] = NUOC; Rr[1000:] = (150, 140, 60)                          # sông
M[990:1000] = BANG; Rr[990:1000] = (90, 110, 120)                    # bờ
CT = np.zeros((H, W, 3), np.uint8)
TOA = [dict(ten='toa_a', mau=[20, 0, 200], hop=(700, 300, 760, 560)), dict(ten='toa_b', mau=[40, 0, 200], hop=(1300, 340, 1350, 560))]
for t in TOA:
    x0, y0, x1, y1 = t['hop']; M[y0:y1, x0:x1] = NHA; CT[y0:y1, x0:x1] = t['mau']; Rr[y0:y1, x0:x1] = (90, 95, 100)
    for yy in range(y0 + 6, y1, 14): Rr[yy:yy + 6, x0 + 6:x1 - 6] = (160, 170, 180)
cv2.imwrite(P('mat_na.png'), M[:, :, ::-1]); cv2.imwrite(P('ct.png'), CT[:, :, ::-1]); cv2.imwrite(P('render.png'), Rr)
Rd = (Rr.astype(np.float32) * 0.18).astype(np.uint8); cv2.imwrite(P('render_dem.png'), Rd)


def ai_ve(R0):
    """"ảnh AI": nhà thường + trời + đất đổi màu/vân; toà có tên cũng bị vẽ lại (chưa ghép)"""
    A = R0.astype(np.int16).copy()
    nt = (M == NT).all(-1); A[nt] += rng.integers(-25, 26, size=(int(nt.sum()), 3)); A[nt] += (15, -10, 20)
    tr = (M == TROI).all(-1); A[tr] += (6, 4, -3)
    nh = (M == NHA).all(-1); A[nh] += (30, 20, 10)
    return np.clip(A, 0, 255).astype(np.uint8)


def ghep(R0, AI):
    A_, _, _ = None, None, None
    L, names = NP.idmap(P('mat_na.png'), (W, H), K78.bang_e({}))
    A = NP.lop(L, names, K78.LOP_A_E); Wt = L == names.index('nuoc')
    A |= cv2.dilate((cv2.morphologyEx(Wt.astype(np.uint8), cv2.MORPH_GRADIENT, np.ones((3, 3), np.uint8)) > 0).astype(np.uint8), np.ones((17, 17), np.uint8)) > 0
    A = cv2.dilate(A.astype(np.uint8), np.ones((3, 3), np.uint8)) > 0
    G = AI.copy(); G[A] = R0[A]; return G


AI = ai_ve(Rr); G0 = ghep(Rr, AI); cv2.imwrite(P('g_dung.png'), G0)
cv2.imwrite(P('g_ve_toa.png'), AI)                                              # AI vẽ cả toà có tên (không ghép lại)
Gt = G0.copy(); Gt[200:560, 1000:1040] = (70, 75, 80); Gt[200:560, 1000] = (200, 200, 200); Gt[200:560, 1039] = (200, 200, 200)
for yy in range(210, 560, 12): Gt[yy:yy + 4, 1004:1036] = (170, 180, 190)
cv2.imwrite(P('g_thap_bia.png'), Gt)                                            # tháp bịa đỉnh y 200 < toa_a 300 (cao hơn 100 px)
Gl = G0.copy(); Gl[470:560, 1000:1040] = (70, 75, 80); Gl[470:560, 1000] = (200, 200, 200); Gl[470:560, 1039] = (200, 200, 200)
cv2.imwrite(P('g_thap_thap.png'), Gl)                                           # tháp bịa đỉnh y 470 (thấp hơn mốc gần)
AId = ai_ve(Rd); Gd = ghep(Rd, AId); cv2.imwrite(P('g_dem.png'), Gd)
Gc = Gd.copy(); cv2.rectangle(Gc, (380, 700), (900, 790), (20, 20, 20), -1); cv2.putText(Gc, 'GRAND HOTEL', (400, 770), cv2.FONT_HERSHEY_DUPLEX, 2.0, (60, 220, 255), 4, cv2.LINE_AA)
cv2.imwrite(P('g_dem_chu.png'), Gc)
Gn = G0.copy(); cv2.rectangle(Gn, (380, 700), (900, 790), (20, 20, 20), -1); cv2.putText(Gn, 'GRAND HOTEL', (400, 770), cv2.FONT_HERSHEY_DUPLEX, 2.0, (60, 220, 255), 4, cv2.LINE_AA)
cv2.imwrite(P('g_ngay_chu.png'), Gn)
Gb = G0.copy(); land = (M == BANG).all(-1); Gb[land] = (200, 120, 20); cv2.imwrite(P('g_xanh.png'), Gb)   # đất (bờ) tô xanh nước

TOA_K = [dict(ten=t['ten'], mau=t['mau']) for t in TOA]
VZ = {}   # mô hình nhìn giả lập: tag → json (cả hai mô hình cùng trả)
_soi0 = QV.soi


def soi_gia(truoc, sau, nam, noi='', t4=False, out=None, tag='khung', api=False, cache=None, mo_hinh=('gpt', 'claude'), de=None):
    j = VZ.get(tag)
    if j is None: return dict(khoa='x', ket_qua={}, loi='chưa soi: không có trong bộ đệm và không chạy --vision (mô hình nhìn có chi phí ≈ $0,2/khung)')
    return dict(khoa='x', ket_qua={m: dict(json=j, meta={}) for m in mo_hinh}, loi=None, de_ver=(de or {}).get('ver'))


QV.soi = soi_gia


def tam(id_, ghep_p, render='render.png', **kw):
    t = dict(id=id_, shot='H5-04', render=render, ghep=ghep_p, mat_na='mat_na.png', mat_na_ct='ct.png', toa_co_ten=TOA_K, nam=2026, n2p_toan_khung_hien_dai=True)
    t.update(kw); return t


LS0 = [dict(shot='H5-04', cu_may='CODINH', ai_nen=True, dur=10)]


def chay(tams, LS=LS0, animatic=False):
    E = dict(id='e', kenh2_tu_t4=True, n2p=dict(noi='London', tam=tams), animatic=animatic)
    return NP.check(E, None, TMP, LS)


SACH = dict(moc=[dict(ten=t['ten'], co_mat=True, nhan_doi=False, do_tin=0.9) for t in TOA], thap_bia=[], them=[], bot_doi=[], chu=[], doi_loai_vung=[])
for tg in ('dung', 'thap_bia', 'thap_thap', 'dem', 'dem_chu', 'ngay_chu', 've_toa', 'xanh', 'thuong', 'k_nam', 'k_cu', 'k_nm', 'thieu_toa', 'mat_toa'): VZ[tg] = SACH

r = chay([tam('dung', 'g_dung.png')])
case('LUẬT E', 'ghép đúng (AI vẽ lại mọi nhà thường) → N2P-1 (a) 0/255, N2P-E sạch', bad(r['N2P-1'], 'a', 'b') + bad(r['N2P-E']), False)
case('LUẬT E', 'ghép đúng → N2P-2/3/4 sạch (mô hình giả lập sạch)', bad(r['N2P-2']) + bad(r['N2P-3']) + bad(r['N2P-4']), False)
rt = chay([dict(tam('thuong', 'g_dung.png'), n2p_toan_khung_hien_dai=False)])
case('LUẬT E', 'cùng ảnh, tấm KHÔNG khai E → nhà thường thuộc lớp (a) → N2P-1 (a) (hành vi cũ)', bad(rt['N2P-1'], 'a'), True)
case('LUẬT E', 'tấm không khai E → N2P-E KHÔNG ÁP', [] if rt['N2P-E'].get('ket_qua') == 'KHÔNG ÁP' else [rt['N2P-E'].get('val')], False)
r = chay([tam('k_nam', 'g_dung.png', nam=2010)])
case('LUẬT E (k)', 'năm 2010 < nam_min 2020 → (k) + tấm đo như thường (N2P-1 (a))', bad(r['N2P-E'], 'k') and bad(r['N2P-1'], 'a'), True)
r = chay([tam('k_cu', 'g_dung.png')], LS=[dict(shot='H5-04', cu_may='DAY', ai_nen=True, dur=10)])
case('LUẬT E (k)', 'cú máy DAY (log shot) → (k)', bad(r['N2P-E'], 'k'), True)
r = chay([tam('k_nm', 'g_dung.png', nam_min=2000)])
case('LUẬT E (k)', 'nam_min 2000 < 2020 → (k) (dùng 2020)', bad(r['N2P-E'], 'k'), True)
case('LUẬT E (k)', 'khai cu_may: CODINH ở tấm → không (k)', bad(chay([tam('dung', 'g_dung.png', cu_may='CODINH')], LS=[])['N2P-E'], 'k'), False)
r = chay([tam('ve_toa', 'g_ve_toa.png')])
case('LUẬT E (i)/(f1)', 'AI vẽ lại toà có tên (không ghép lại) → N2P-1 (a) + N2P-E (f)', bad(r['N2P-1'], 'a') and bad(r['N2P-E'], 'f'), True)
r = chay([tam('mat_toa', 'g_dung.png', toa_co_ten=TOA_K + [dict(ten='toa_khong_co', mau=[60, 0, 200])])])
case('LUẬT E (f1)', 'khai toà không có trong mặt nạ mã công trình → (f)', bad(r['N2P-E'], 'f'), True)
r = chay([tam('thieu_toa', 'g_dung.png', toa_co_ten=None)])
case('LUẬT E (f)', 'thiếu toa_co_ten → THIẾU (f)', r['N2P-E'].get('thieu'), True)
r = chay([tam('thap_bia', 'g_thap_bia.png')])
case('LUẬT E (f2)', 'tháp bịa cao hơn toà có tên gần nhất → (w) máy', bad(r['N2P-E'], 'w'), True)
case('LUẬT E (f2)', 'tháp bịa: (w) chỉ Cảnh báo ở G2 (không Chặn)', cap112.cap('N2P-E', r['N2P-E'])[1], False)
r = chay([tam('thap_thap', 'g_thap_thap.png')])
case('LUẬT E (f2)', 'tháp bịa THẤP hơn mốc gần → không (w)', [x for x in bad(r['N2P-E'], 'w') if 'cụm dựng đứng' in x], False)
r = chay([tam('dem_chu', 'g_dem_chu.png', render='render_dem.png', dem=True)])
case('LUẬT E (g)', 'đêm: chữ AI "GRAND HOTEL" trên nhà thường → (g) máy (PP-OCRv4)', bad(r['N2P-E'], 'g'), True)
case('LUẬT E (g)', '(g) ở G2 → Chặn', cap112.cap('N2P-E', dict(r['N2P-E'], cong='G2'))[1], True)
case('LUẬT E (g)', '(g) ở animatic → chỉ Cảnh báo', cap112.cap('N2P-E', dict(r['N2P-E'], cong='animatic'))[1], False)
r = chay([tam('dem', 'g_dem.png', render='render_dem.png', dem=True)])
case('LUẬT E (g)', 'đêm, không chữ → (g) sạch', bad(r['N2P-E'], 'g'), False)
r = chay([tam('ngay_chu', 'g_ngay_chu.png')])
case('LUẬT E (g)', 'ban ngày, cùng chữ → chỉ (w), không (g)', bad(r['N2P-E'], 'g') or not bad(r['N2P-E'], 'w'), False)
case('LUẬT E (g)', 'đêm suy từ render khi không khai `dem`: render tối → đêm', [] if K78.la_dem({}, Rd)[0] and not K78.la_dem({}, Rr)[0] else ['sai'], False)
r = chay([tam('xanh', 'g_xanh.png')]); rt = chay([dict(tam('thuong', 'g_xanh.png'), n2p_toan_khung_hien_dai=False)])
case('LUẬT E (iii)', 'đất (bờ) tô xanh: tấm thường → T9b (a)', bad(rt['N2P-3'], 'a'), True)
case('LUẬT E (iii)', 'cùng ảnh ở tấm E → T9b đất→nước chỉ in (bờ thuộc (a)-E → N2P-1 (a))', bad(r['N2P-3'], 'a') + ([] if bad(r['N2P-1'], 'a') else ['(a) không bắt bờ']), False)
VZ['mh_mat'] = dict(SACH, moc=[dict(ten='toa_a', co_mat=False, do_tin=0.9)])
case('LUẬT E mô hình', 'mô hình báo toà có tên mất → N2P-1 (b)', bad(chay([tam('mh_mat', 'g_dung.png')])['N2P-1'], 'b'), True)
VZ['mh_doi'] = dict(SACH, moc=[dict(ten='toa_a', co_mat=True, nhan_doi=True, do_tin=0.8)])
case('LUẬT E mô hình', 'mô hình báo toà có tên nhân đôi/bóng ma → N2P-1 (b)', bad(chay([tam('mh_doi', 'g_dung.png')])['N2P-1'], 'b'), True)
VZ['mh_thap'] = dict(SACH, thap_bia=[dict(mo_ta='glass tower', toa_do=[0.52, 0.1, 0.55, 0.52], cao_hon_moc_gan=True, do_tin=0.8)])
case('LUẬT E mô hình', 'mô hình báo tháp bịa cao hơn mốc gần → (w)', [x for x in bad(chay([tam('mh_thap', 'g_dung.png')])['N2P-E'], 'w') if 'toà cao không tên' in x], True)
VZ['mh_chu'] = dict(SACH, chu=[dict(mo_ta='neon sign', toa_do=[0.2, 0.6, 0.3, 0.7], do_tin=0.7)])
case('LUẬT E mô hình', 'đêm: mô hình báo biển chữ → (g)', bad(chay([tam('mh_chu', 'g_dem.png', render='render_dem.png', dem=True)])['N2P-E'], 'g'), True)
VZ['mh_nguoi'] = dict(SACH, them=[dict(loai='nguoi', mo_ta='people', toa_do=[0.4, 0.8, 0.45, 0.9], do_tin=0.8)])
case('LUẬT E mô hình', 'mô hình báo người thêm → N2P-4 (a)', bad(chay([tam('mh_nguoi', 'g_dung.png')])['N2P-4']), True)
VZ['mh_nha'] = dict(SACH, them=[dict(loai='cong_trinh', mo_ta='new roof storey on ordinary house', toa_do=[0.1, 0.6, 0.2, 0.8], do_tin=0.8)])
case('LUẬT E mô hình', 'mô hình báo nhà thường đổi (ngoài (a)-E) → KHÔNG là N2P-1 (b)', bad(chay([tam('mh_nha', 'g_dung.png')])['N2P-1'], 'b'), False)
case('LUẬT E mô hình', 'không có bộ đệm → N2P-1 THIẾU (b) như cũ', chay([tam('khong_bo_dem', 'g_dung.png')])['N2P-1'].get('thieu'), True)
case('LUẬT E BMN', 'tấm E khai cả be_mat_nha_ai → BE-MAT-NHA không đo tấm này (KHÔNG ÁP)',
     [] if K75.be_mat_nha(dict(E4, n2p=dict(tam=[tam('b', 'g_dung.png', be_mat_nha_ai=True)])), TMP).get('ket_qua') == 'KHÔNG ÁP' else ['vẫn đo'], False)
_dv, GOT = NP.do_video, {}
NP.do_video = lambda g_, r_, m_, ch, la, bg: GOT.update(la=la, bg=bg) or dict(khung=10, fps=24, buoc_max=0.1, buoc_tai_s=0, buoc_trung_vi=0, nhap_ghep=0.0, nhap_render=0.0, lop_c_pct=50)
EV = dict(id='v', kenh2_tu_t4=True, n2p=dict(video=[dict(shot='H5-04', ghep='a.mp4', render='b.mp4', mat_na='mat_na.png', n2p_toan_khung_hien_dai=True)]))
NP.n2p5(EV, LS0, TMP)
case('LUẬT E (v)', 'n2p.video khai E → đo nhấp nháy trên ngoài (a)-E (nhà thường là lớp đo)', [] if GOT.get('la') == K78.lop_a_e({}) and 'nha_thuong' in (GOT.get('bg') or {}) else [GOT], False)
EV['n2p']['video'][0]['n2p_toan_khung_hien_dai'] = False; NP.n2p5(EV, LS0, TMP)
case('LUẬT E (v)', 'n2p.video không khai E → LOP_A cũ', [] if GOT.get('la') == NP.LOP_A else [GOT], False)
NP.do_video = _dv
case('LUẬT E áp dụng', 'tập trước T4 (không n2p/kenh2_tu_t4) → N2P KHÔNG ÁP (không có N2P-E)', [k for k, v in NP.check(E3, None, TMP, []).items() if v.get('ket_qua') != 'KHÔNG ÁP'], False)
QV.soi = _soi0

# ====================================================================== K-LAI-3 ↔ KIEM-2-MUC
def kt(kl):
    p = P(f'kt-{kl}.json'); json.dump(dict(ket_luan_may=dict(ket_qua=kl, loi_mo_hinh=0)), open(p, 'w')); return p


open(P('tk.jpg'), 'wb').write(b'\xff\xd8\xff\xd9')
DUYET = dict(nguoi_ky='Chủ dự án (tác giả – đạo diễn)', vai='chu_du_an', ngay='2026-10-26', ket_luan='chap_nhan')


def ls_nen(**kw):
    d = dict(ma='H1-06b', t0=0.0, t1=4.0, muc_kiem='nen', so_luot=2, kiem_t1=kt('ĐẠT'), to_khung=P('tk.jpg'), clip='c.mp4'); d.update(kw)
    return [dict(shot='H1-06b', t0=0.0, t1=4.0, dur=4.0, minh_hoa=[d], ai_image=True, goc='md')]


def k3(LS):
    DS = LA.log_ai(LS)[0]; return LA.klai3_mh(DS, {}, TMP)


case('K-LAI-3 nen', 'nen: Flash ĐẠT + tờ khung có thật, không tầng 2 → ĐẠT (1.17.7: THIẾU)', bad(k3(ls_nen())), False)
case('K-LAI-3 nen', 'nen thiếu tờ khung → THIẾU', k3(ls_nen(to_khung=P('khong-co.jpg'))).get('thieu'), True)
case('K-LAI-3 nen', 'nen thiếu kiem_t1 → THIẾU', k3(ls_nen(kiem_t1=None)).get('thieu'), True)
case('K-LAI-3 nen', 'nen Flash LOẠI → (b)', bad(k3(ls_nen(kiem_t1=kt('LOẠI'))), 'b'), True)
case('K-LAI-3 nen', 'nen Flash LOẠI + ngoai_le_duyet chủ dự án → ĐẠT', bad(k3(ls_nen(kiem_t1=kt('LOẠI'), ngoai_le_duyet=DUYET))), False)
case('K-LAI-3 nen', 'ngoai_le_duyet có email → (b)', bad(k3(ls_nen(kiem_t1=kt('LOẠI'), ngoai_le_duyet=dict(DUYET, nguoi_ky='x' + chr(64) + 'vi-du.test'))), 'b'), True)
case('K-LAI-3 nen', 'day_du thiếu `kiem` → THIẾU (như cũ)', k3(ls_nen(muc_kiem='day_du')).get('thieu'), True)
case('KIEM-2-MUC nen', '(b) Flash LOẠI ở nen → lỗi', bad(K7.kiem_2_muc(dict(E4, kiem_2_muc=True), ls_nen(kiem_t1=kt('LOẠI')), TMP), 'b'), True)
case('KIEM-2-MUC nen', '(b) Flash LOẠI + ngoai_le_duyet → sạch', bad(K7.kiem_2_muc(dict(E4, kiem_2_muc=True), ls_nen(kiem_t1=kt('LOẠI'), ngoai_le_duyet=DUYET), TMP), 'b'), False)
case('KIEM-2-MUC nen', 'day_du Flash LOẠI + ngoai_le_duyet → vẫn (b) (ngoại lệ chỉ ở nen)',
     bad(K7.kiem_2_muc(dict(E4, kiem_2_muc=True), ls_nen(muc_kiem='day_du', so_luot=1, kiem_t1=kt('LOẠI'), ngoai_le_duyet=DUYET, kiem=kt('ĐẠT')), TMP), 'b'), True)

# ====================================================================== Q34 / Q26b-K2
TLq = dict(tong_s=30.0, segments=[dict(id='S1', t0=0.0, t1=30.0, shots=[dict(t0=0.0, t1=10.0, tpl='plate', p={}), dict(t0=10.0, t1=20.0, tpl='plate', p={}), dict(t0=20.0, t1=30.0, tpl='plate', p={})])])
SPq = [dict(id='S1', shots=[dict(type='scene3d', tpl='plate', p={}), dict(type='minh_hoa', tpl='plate', p={}), dict(type='tu_lieu', tpl='plate', p={})])]
case('Q34 T4', 'T4: type minh_hoa, tu_lieu → không (0)', bad(QTY.q34(dict(E4, segments=SPq), TLq), '0'), False)
case('Q34 T4', 'T3: type minh_hoa → (0) như cũ', bad(QTY.q34(dict(E3, segments=SPq), TLq), '0'), True)
case('Q34 T4', 'T4: type lạ "abc" → (0)', bad(QTY.q34(dict(E4, segments=[dict(id='S1', shots=[dict(type='abc', tpl='plate', p={})] * 3)]), TLq), '0'), True)
lo4 = K2V.q26b_k2(dict(E4, segments=SPq), TLq)['loai']; lo3 = K2V.q26b_k2(dict(E3, segments=SPq), TLq)['loai']
case('Q26b-K2 T4', 'T4: minh_hoa → loại minh_hoa, tu_lieu → anh; T3: khac', [] if 'minh_hoa' in lo4 and 'anh' in lo4 and 'khac' in lo3 and 'minh_hoa' not in lo3 else [lo4, lo3], False)

# ====================================================================== SACH-1
TLs = dict(tong_s=30.0, segments=[dict(id='S1', t0=0.0, t1=30.0, shots=[dict(t0=0.0, t1=30.0, tpl='plate', p=dict(sach=True))])])
SPs = [dict(id='S1', shots=[dict(type='scene3d', tpl='plate', p=dict(sach=True))])]


def sach(E, muc):
    p = P('log_chu.json'); json.dump(dict(fmt='khoang', muc=muc), open(p, 'w'))
    E = dict(E, segments=SPs, log_chu=p); TX, st, _, _ = K6.text_frames(TLs, None, p, TMP)
    return K6.sach1(E, TLs, TX, st), TX


M1 = [dict(t0=0.0, t1=30.0, role='year', s='1666'), dict(t0=2.0, t1=6.0, role='the_nhan_vat', s='Samuel Pepys'), dict(t0=10.0, t1=12.5, role='bo_dem_so', s='13,200 houses')]
r, TX = sach(E4, M1)
case('SACH-1 khuôn khoảng', 'log_chu {fmt: khoang} nở thành mẫu mỗi 12 khung (30 s → 60 mẫu bộ đếm năm)', [] if TX and sum(1 for it in TX.values() for x in it if x['role'] == 'year') == 60 else [len(TX or {})], False)
case('SACH-1 §17', 'T4: thẻ nhân vật 4 s + bộ đếm "13,200 houses" → sạch', bad(r), False)
case('SACH-1 §17', 'T4: thẻ nhân vật 6 s > 5 s → (g)', bad(sach(E4, M1 + [dict(t0=14.0, t1=20.0, role='the_nhan_vat', s='Christopher Wren')])[0], 'g'), True)
case('SACH-1 §17', 'T4: bộ đếm "13,200 houses burned down" > 2 từ → (g)', bad(sach(E4, [dict(t0=1.0, t1=3.0, role='bo_dem_so', s='13,200 houses burned down')])[0], 'g'), True)
case('SACH-1 §17', 'T4: chú thích tư liệu 7 từ → (g)', bad(sach(E4, [dict(t0=1.0, t1=4.0, role='chu_thich_tu_lieu', s='Hollar: London before the Fire (pub. 1666)')])[0], 'g'), True)
case('SACH-1 §17', 'T4: chú thích tư liệu 5 từ 6 s → sạch', bad(sach(E4, [dict(t0=1.0, t1=7.0, role='chu_thich_tu_lieu', s='Hollar, Old St Paul’s, 1658')])[0]), False)
case('SACH-1 §17', 'T4: 3 lớp §17 cùng lúc → (g)', bad(sach(E4, [dict(t0=1.0, t1=4.0, role='the_nhan_vat', s='Pepys'), dict(t0=1.0, t1=4.0, role='bo_dem_so', s='87 churches'),
                                                                   dict(t0=1.0, t1=4.0, role='chu_thich_tu_lieu', s='Hollar 1666')])[0], 'g'), True)
case('SACH-1 §17', 'T3: vai the_nhan_vat → (e) chữ ngoài danh sách (như cũ)', bad(sach(E3, M1)[0], 'e'), True)
case('SACH-1 (c)', 'T4 không log chữ → THIẾU nêu khuôn log_chu khoảng', [x for x in (K6.sach1(dict(E4, segments=SPs), TLs, None, 12).get('thieu') or []) if 'khoang' in x], True)

# ====================================================================== Q37 (d)
n = 24 * 20; F = rng.uniform(0, 255, (n, 90, 160)).astype(np.float32)
F[24 * 10:24 * 19] = F[24 * 10]                                   # 9 s tĩnh từ 10 s
EQ = lambda E, d=20.0: dict(E, segments=[dict(id='S', dur=d, shots=[dict(at=0, p={})], beats=[dict(t=float(t), k='cut' if t == 0 else 'b', s='x') for t in range(0, int(d), 2)])])
mien = [(10.0, 19.5, 'the_pp', 'PP1')]
d4 = [x for x in QN.q37(EQ(E4), None, F=F, mien=mien)['loi'] if x.startswith('(d)')]
case('Q37 (d) T4', 'khung tĩnh 9 s trong thẻ PP cuối → miễn', d4, False)
case('Q37 (d) T4', 'cùng phim, T3 → (d) như cũ', [x for x in QN.q37(EQ(E3), None, F=F, mien=mien)['loi'] if x.startswith('(d)')], True)
case('Q37 (d) T4', 'T4, khung tĩnh ngoài thẻ PP → (d)', [x for x in QN.q37(EQ(E4), None, F=F, mien=[(0.0, 5.0, 'the_pp', 'PP1')])['loi'] if x.startswith('(d)')], True)
F2 = F.copy(); F2[24 * 8:24 * 19] = F[24 * 8]                     # 11 s tĩnh
case('Q37 (d) T4', 'T4, khung tĩnh 11 s > 10 s trong thẻ PP → (d)', [x for x in QN.q37(EQ(E4), None, F=F2, mien=[(8.0, 19.5, 'the_pp', 'PP1')])['loi'] if x.startswith('(d)')], True)
case('Q37 (d) T4', 'T4, khoảng khung neo (không phải thẻ PP) → (d) (chỉ thẻ PP được miễn)', [x for x in QN.q37(EQ(E4), None, F=F, mien=[(10.0, 19.5, 'khung_neo', 'N1')])['loi'] if x.startswith('(d)')], True)

# ====================================================================== TU-LIEU-OMNI
LSo = [dict(shot='M1', t0=0.0, t1=5.0, dur=5.0, minh_hoa=True), dict(shot='T', t0=5.0, t1=10.0, dur=5.0, lop=dict(A=5.0, TL=5.0)),
       dict(shot='M2', t0=10.0, t1=15.0, dur=5.0, minh_hoa=True), dict(shot='M3', t0=15.0, t1=20.0, dur=5.0, minh_hoa=True), dict(shot='Z', t0=20.0, t1=30.0, dur=10.0, lop=dict(A=10.0))]
ro = K76.tu_lieu_omni(E4, None, LSo)
case('TU-LIEU-OMNI', 'tư liệu kẹp giữa M1 và M2 → (b) 2 cặp (gần nhất mỗi phía; M3 sau M2 bỏ)', [] if len(bad(ro, 'b')) == 2 and 'bỏ 1 cặp' in ro['val'] else [len(bad(ro, 'b')), ro['val']], False)
case('TU-LIEU-OMNI', 'vẫn bắt ghép liền (≥ 1 lỗi (b))', bad(ro, 'b'), True)
LSo2 = copy.deepcopy(LSo); LSo2[1]['tu_lieu_lan'] = [dict(t0=6.5, t1=8.5, lop='TL')]
case('TU-LIEU-OMNI', 'góc khung khai hẹp tu_lieu_lan 6,5–8,5 s (3D sạch ≥ 1 s mỗi phía) → sạch', bad(K76.tu_lieu_omni(E4, None, LSo2), 'b'), False)
LSo3 = copy.deepcopy(LSo); LSo3[1]['tu_lieu_lan'] = [dict(t0=5.2, t1=8.5, lop='TL')]
case('TU-LIEU-OMNI', 'góc khung bắt đầu 0,2 s sau ranh M-d → (b) ghép liền (phán K-1.17.8: có tính)', bad(K76.tu_lieu_omni(E4, None, LSo3), 'b'), True)

# ====================================================================== BIEN-CO-V
D = dict(su_kien=[[float(t), 1, 9.0, 'o'] for t in np.arange(0.5, 30, 1.0)], cat=[], n_khung=720)
TLb = dict(tong_s=30.0, segments=[dict(id='S', t0=0.0, t1=30.0, shots=[dict(t0=0.0, t1=30.0)])])
open(P('v.mp4'), 'wb').write(b'0')
h4 = BCV.hang(E4, TLb, P('v.mp4'), 'G2', [], D); h3 = BCV.hang(E3, TLb, P('v.mp4'), 'G2', [], D)
case('BIEN-CO-V', 'T4: HIEU_CHUAN_T4 chưa đạt → dat_hieu_chuan False (chỉ Cảnh báo ở G2)', [] if h4['dat_hieu_chuan'] is False and 'T4 (1.17.8)' in h4['val'] else [h4['val']], False)
case('BIEN-CO-V', 'T3: HIEU_CHUAN T3 giữ (dat_hieu_chuan True)', [] if h3['dat_hieu_chuan'] is True and 'hiệu chuẩn T3' in h3['val'] else [h3['val']], False)
case('BIEN-CO-V', 'T4: cho_q37 rỗng khi chưa đạt; T3 không cộng (như cũ)', BCV.cho_q37(E4, D, h4['dat_hieu_chuan']) + BCV.cho_q37(E3, D, True), False)
case('BIEN-CO-V', 'T4 lỗi (c) vẫn ghi nhưng cấp G2 chỉ Cảnh báo', cap112.cap('BIEN-CO-V', dict(h4, loi=['(c) x']))[1], False)

ok = all(x[3] for x in R)
for rule, name, exp, good, got in R: print(('ĐÚNG' if good else 'SAI ') + f' | {rule} | {name} | kỳ vọng {exp}' + ('' if good else f' | được: {got}'))
print(f"\nselftest_k1178: {sum(x[3] for x in R)}/{len(R)} đúng kỳ vọng")
sys.exit(0 if ok else 1)
