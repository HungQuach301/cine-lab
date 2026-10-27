#!/opt/cine/bin/python
"""Tự kiểm luật 1.17.9 (phiên K-1.17.9, 26/10/2026). Mỗi luật mới/đổi ≥ 1 ca ĐẠT + ≥ 1 ca TRƯỢT; ca "không khai → hành vi 1.17.8".
Không mạng, không API (mô hình nhìn giả lập bằng thay q_n2p_vision.soi). Ca THẬT từ đầu vào BAN-CUOI-T4-A (@bc1693b5) thu nhỏ 640×360 trong
fixtures/k1179/ (nguồn + SHA-256: fixtures/k1179/NGUON.json): render/AI/mặt nạ "tháp" P9-2026 và P1-2026, câu trả lời thô GPT của tấm
E-P9-ngay-l1-thap (KN-1), toa-thap.json (KN-5), clip Omni H3-05b-l1-360p / H1-15b-l1-360p (KN-4, KN-7 — YuNet thật), log máy H1-08b / H1-16 / H2-03b (KN-2).
  KN-1 ngoại lệ mô hình tấm E · KN-2 biến cố đo từ log máy · KN-4 cat_clip · KN-5 loại toà có tên · KN-6 đẩy/trượt 2D · KN-7 miễn (k) không chân dung ·
  KN-8 nước AI · cấp G2/animatic.
  /opt/cine/bin/python checks/ll/selftest_k1179.py        mã thoát 0 = mọi ca đúng kỳ vọng"""
import copy, json, os, shutil, sys, tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, ROOT)
import numpy as np  # noqa: E402
import cv2  # noqa: E402
from checks.ll import q_k1179 as K79, q_k1178 as K78, q_n2p as NP, q_n2p_vision as QV, q_k1177 as K7, q_nhip as QN, cap112  # noqa: E402

FX = os.path.join(ROOT, 'checks', 'll', 'fixtures', 'k1179'); TMP = tempfile.mkdtemp(prefix='k1179-'); R = []
P = lambda f: os.path.join(TMP, f)
E4 = dict(id='t4', kenh2_tu_t4=True); E3 = dict(id='t3', khung_sach=True)


def case(rule, name, got, expect_fail):
    got = list(got) if got else []
    R.append((rule, name, 'bắt lỗi' if expect_fail else 'sạch', bool(got) == expect_fail, got[:2]))


def bad(x, *muc):
    L = (x.get('loi') or []) + (x.get('thieu') or [])
    return [y for y in L if not muc or any(y.startswith(f'({m})') for m in muc)]


# ====================================================================== ghép tấm E thật (640×360) — đúng thủ tục ghep_e_bc (vùng bảo vệ nở 1 px, mềm 2 px)
PALB = {'nuoc': (0, 170, 190), 'nha': (235, 235, 235), 'tau': (255, 0, 0)}


def lopm(M, k): return np.all(M == np.array(PALB[k][::-1]), -1)


def lop_a(M, nuoc_ai=False):
    A = lopm(M, 'nha') | lopm(M, 'nuoc') | lopm(M, 'tau'); W = lopm(M, 'nuoc').astype(np.uint8); r = max(1, int(round(8 * M.shape[0] / 1080)))
    A |= cv2.dilate((cv2.morphologyEx(W, cv2.MORPH_GRADIENT, np.ones((3, 3), np.uint8)) > 0).astype(np.uint8), np.ones((2 * r + 1,) * 2, np.uint8)) > 0
    return A & ~lopm(M, 'nuoc') if nuoc_ai else A


def ghep(tag, nuoc_ai=False, ra=None):
    Rr = cv2.imread(f'{FX}/{tag}_render.png'); AI = cv2.imread(f'{FX}/{tag}_ai.png'); M = cv2.imread(f'{FX}/{tag}_matna.png')
    A = lop_a(M, nuoc_ai); B = cv2.dilate(A.astype(np.uint8), np.ones((3, 3), np.uint8)) > 0
    al = np.clip(cv2.distanceTransform((~B).astype(np.uint8), cv2.DIST_L2, 3) / 2.0, 0, 1)[..., None]
    G = np.round(al * AI + (1 - al) * Rr).astype(np.uint8); G[B] = Rr[B]
    p = P(ra or f'{tag}_ghep{"_na" if nuoc_ai else ""}.png'); cv2.imwrite(p, G); return p, G


GPT9 = json.load(open(f'{FX}/p9_gpt.json')); MH = {}


def soi_gia(truoc, sau, nam, noi='', t4=False, out=None, tag='khung', api=False, cache=None, mo_hinh=('gpt', 'claude'), de=None):
    j = MH.get(tag, {})
    return dict(khoa='gia', ket_qua={'gpt': dict(json=j.get('gpt') or {}, meta={}), 'claude': dict(json=j.get('claude') or {}, meta={})}, loi=None)


QV.soi = soi_gia


def tam(id_, tag, ghep_p, **kw):
    toa = [dict(ten=x['ten'], mau=x['mau']) for x in json.load(open(f'{FX}/{tag}_toa.json'))]
    t = dict(id=id_, shot='H5-05a', render=f'{FX}/{tag}_render.png', ghep=ghep_p, mat_na=f'{FX}/{tag}_matna.png', nam=2026, anh_tinh=True,
             n2p_toan_khung_hien_dai=True, nam_min=2020, cu_may='CODINH', dem=False, mat_na_ct=f'{FX}/{tag}_ct.png', toa_co_ten=toa, noi='London')
    t.update(kw); return t


def chay(tams, animatic=False, video=None):
    E = dict(E4, n2p=dict(noi='London', t4=True, tam=tams, **({'video': video} if video else {})), animatic=animatic)
    return NP.check(E, None, TMP, [dict(shot='H5-05a', t0=0, t1=3, dur=3, cu_may='CODINH', ai_nen=True)])


DUYET = dict(nguoi_ky='Chủ dự án (tác giả – đạo diễn)', vai='chu_du_an', ngay='2026-10-26', ket_luan='chap_nhan')
NL = [dict(hang=['N2P-1 (b)', 'N2P-3 (b)'], hop=[0.0, 0.96, 0.09, 1.0], ly_do='K1178-D2 — mép kè/nước AI ngoài dải bờ 8 px', duyet_chu_du_an=DUYET)]

# ====================================================================== KN-1 (ca thật P9 + GPT thật)
g9, G9 = ghep('p9'); MH['k1'] = dict(gpt=GPT9)
r0 = chay([tam('k1', 'p9', g9)])
case('KN-1', 'THẬT E-P9-ngay-l1-thap: không ngoai_le → GPT "bờ" N2P-1 (b) + N2P-3 (b) Chặn (tái hiện)', bad(r0['N2P-1'], 'b') + bad(r0['N2P-3'], 'b'), True)
case('KN-1', 'THẬT: máy sạch — N2P-1 (a) 0/255 ở 640×360', bad(r0['N2P-1'], 'a'), False)
r1 = chay([tam('k1', 'p9', g9, ngoai_le=NL)])
case('KN-1', 'THẬT + ngoai_le hợp lệ (máy sạch, hộp ≤ 25 % lõi) → hết N2P-1 (b), N2P-3 (b)', bad(r1['N2P-1'], 'b') + bad(r1['N2P-3'], 'b'), False)
case('KN-1', '… báo mô hình chuyển thành (w) Cảnh báo ở N2P-E (người đọc thấy)', [] if any('KN-1' in x for x in r1['N2P-E']['loi']) else ['thiếu (w) KN-1'], False)
case('KN-1', '… N2P-E không Chặn ở G2 vì ngoại lệ (w)', cap112.cap('N2P-E', dict(r1['N2P-E'], cong='G2'))[1], False)
nl_mail = copy.deepcopy(NL); nl_mail[0]['duyet_chu_du_an']['nguoi_ky'] = 'ai' + chr(64) + 'vi-du.vn'   # dựng lúc chạy — preflight cấm email trong tệp
case('KN-1', 'ngoai_le có email ở nguoi_ky → không nhận, (b) giữ', bad(chay([tam('k1', 'p9', g9, ngoai_le=nl_mail)])['N2P-1'], 'b'), True)
nl_a = copy.deepcopy(NL); nl_a[0]['hang'] = ['N2P-1 (a)']
case('KN-1', 'ngoai_le xin miễn máy N2P-1 (a) → không nhận', bad(chay([tam('k1', 'p9', g9, ngoai_le=nl_a)])['N2P-1'], 'b'), True)
nl_xa = copy.deepcopy(NL); nl_xa[0]['hop'] = [0.5, 0.0, 0.6, 0.1]
case('KN-1', 'ngoai_le hộp khai ở chỗ khác → (b) giữ', bad(chay([tam('k1', 'p9', g9, ngoai_le=nl_xa)])['N2P-1'], 'b'), True)
nl_vd = copy.deepcopy(NL); nl_vd[0].pop('duyet_chu_du_an')
case('KN-1', 'ngoai_le không có duyet_chu_du_an → (b) giữ', bad(chay([tam('k1', 'p9', g9, ngoai_le=nl_vd)])['N2P-1'], 'b'), True)
G9b = G9.copy(); M9 = cv2.imread(f'{FX}/p9_matna.png'); sp = np.all(cv2.imread(f'{FX}/p9_ct.png') == np.array([200, 0, 20]), -1)
G9b[sp] = cv2.imread(f'{FX}/p9_ai.png')[sp]; cv2.imwrite(P('p9_ban.png'), G9b)
rb = chay([tam('k1', 'p9', P('p9_ban.png'), ngoai_le=NL)])
case('KN-1', 'máy BẨN (AI vẽ lên mái vòm St Paul\'s) + ngoai_le → ngoại lệ không áp: (b) giữ + N2P-1 (a)', bad(rb['N2P-1'], 'a', 'b'), True)
case('KN-1', '… máy không bao giờ được miễn: N2P-1 (a) vẫn Chặn', bad(rb['N2P-1'], 'a'), True)
g_loi = copy.deepcopy(GPT9); g_loi['bot_doi'][0]['toa_do'] = [0.30, 0.47, 0.50, 0.73]; MH['k1l'] = dict(gpt=g_loi)
nl_loi = copy.deepcopy(NL); nl_loi[0]['hop'] = [0.29, 0.46, 0.51, 0.74]
case('KN-1', 'hộp mô hình nằm phần lớn trong lõi (a)-E (mái vòm St Paul\'s) + ngoai_le → (b) giữ', bad(chay([tam('k1l', 'p9', g9, ngoai_le=nl_loi)])['N2P-1'], 'b'), True)

# ====================================================================== KN-5 (toa-thap.json thật P9 + P1)
T9 = json.load(open(f'{FX}/p9_toa.json')); T1 = json.load(open(f'{FX}/p1_toa.json'))
cp = next(x for x in T9 if x['ten'] == 'CityPoint'); mh = next(x for x in T1 if x['ten'] == 'Mansion House')
case('KN-5', 'THẬT CityPoint đỉnh 122,6 m ODN, loai thap → sạch', K79.kiem_toa([dict(cp, loai='thap')])[0], False)
case('KN-5', 'THẬT Mansion House 26,2 m khai loai thap → (k) không phải tháp', K79.kiem_toa([dict(mh, loai='thap')])[0], True)
case('KN-5', 'THẬT Mansion House loai lich_su + nguon (NHLE) → sạch', K79.kiem_toa([dict(mh, loai='lich_su', nguon_lich_su='NHLE 1064694 (Grade I)')])[0], False)
case('KN-5', 'THẬT mục có `nguon` mặt nạ ("OSM name") nhưng lich_su thiếu nguon_lich_su → (k)', K79.kiem_toa([dict(mh, loai='lich_su')])[0], True)
case('KN-5', 'St Paul\'s loai mai_vom → sạch; thap thiếu độ cao → (k)', K79.kiem_toa([dict(T9[0], loai='mai_vom')])[0] + ([] if K79.kiem_toa([dict(ten='X', mau=[1, 2, 3], loai='thap')])[0] else ['không bắt']), False)
case('KN-5', 'không khai loai → không lỗi (hành vi 1.17.8; chỉ đếm ở giá trị)', K79.kiem_toa(T9)[0] + ([] if K79.kiem_toa(T9)[1] == len(T9) else ['đếm sai']), False)
toa_k = [dict(ten=x['ten'], mau=x['mau'], loai='thap', dinh_odn_m=x.get('y1_m', 200)) for x in T9]
r5 = chay([tam('k1', 'p9', g9, toa_co_ten=toa_k, ngoai_le=NL)])
case('KN-5', 'tấm thật khai mọi toà loai thap (gồm Guildhall 2x m) → N2P-E (k) Chặn ở G2', [x for x in bad(r5['N2P-E'], 'k') if 'KN-5' in x], True)
case('KN-5', 'cấp: (k) KN-5 Chặn ở G2, Cảnh báo ở animatic', [] if cap112.cap('N2P-E', dict(r5['N2P-E'], cong='G2'))[1] and not cap112.cap('N2P-E', dict(r5['N2P-E'], cong='animatic'))[1] else ['cấp sai'], False)

# ====================================================================== KN-8 (ca thật P1 — sông ≈ 22 % khung)
g1a, _ = ghep('p1', nuoc_ai=True); MH['k8'] = {}
r8 = chay([tam('k8', 'p1', g1a, nuoc_ai=True, duyet_chu_du_an=DUYET)])
case('KN-8', 'THẬT P1 nước AI (bờ phía đất + cầu/tàu render) + nuoc_ai → N2P-1 (a) 0/255', bad(r8['N2P-1'], 'a'), False)
case('KN-8', '… T9c trên tấm nuoc_ai chỉ in (không Chặn N2P-3 (c)(d))', bad(r8['N2P-3'], 'c', 'd'), False)
case('KN-8', '… có duyệt → không (u)', bad(r8['N2P-E'], 'u'), False)
r8b = chay([tam('k8', 'p1', g1a)])
case('KN-8', 'cùng ảnh KHÔNG khai nuoc_ai → N2P-1 (a) (nước phải = render như 1.17.8)', bad(r8b['N2P-1'], 'a'), True)
case('KN-8', 'nuoc_ai không duyệt chủ dự án → (u) THIẾU', bad(chay([tam('k8', 'p1', g1a, nuoc_ai=True)])['N2P-E'], 'u'), True)
M1 = cv2.imread(f'{FX}/p1_matna.png'); W1 = lopm(M1, 'nuoc'); ys, xs = np.nonzero(W1)
cy, cx = float(np.median(ys)) / 360, float(np.median(xs)) / 640
MH['k8c'] = dict(gpt=dict(them=[dict(loai='cong_trinh', mo_ta='second footbridge across the river', toa_do=[cx - 0.05, cy - 0.02, cx + 0.05, cy + 0.02], thoi_dai_sai=False, do_tin=0.8)]))
case('KN-8', 'mô hình báo THÊM cầu trên mặt nước AI → N2P-1 (b) Chặn', bad(chay([tam('k8c', 'p1', g1a, nuoc_ai=True, duyet_chu_du_an=DUYET)])['N2P-1'], 'b'), True)
dnt = cv2.distanceTransform(np.all(M1 == (215, 215, 215), -1).astype(np.uint8), cv2.DIST_L2, 5); ny, nx = [float(v) for v in np.unravel_index(int(np.argmax(dnt)), dnt.shape)]; ny, nx = ny / 360, nx / 640
MH['k8d'] = dict(gpt=dict(them=[dict(loai='cong_trinh', mo_ta='rooftop extension', toa_do=[nx - 0.02, ny - 0.02, nx + 0.02, ny + 0.02], thoi_dai_sai=False, do_tin=0.8)]))
case('KN-8', 'mô hình báo đổi trên nhà thường (đất) → không (b) (AI vẽ lại nhà thường được phép)', bad(chay([tam('k8d', 'p1', g1a, nuoc_ai=True, duyet_chu_du_an=DUYET)])['N2P-1'], 'b'), False)

# ====================================================================== KN-6 đẩy/trượt 2D (video tổng hợp từ tấm P9 thật)
def vid(ten, toc, toc_a=None, n=48, fps=24):
    G = cv2.imread(g9); A = lop_a(cv2.imread(f'{FX}/p9_matna.png')); H, W = G.shape[:2]; p = P(ten)
    wr = cv2.VideoWriter(p, cv2.VideoWriter_fourcc(*'FFV1'), fps, (W, H))
    for i in range(n):
        t = i / fps; s = 1 + toc / 100 * t; sa = 1 + (toc if toc_a is None else toc_a) / 100 * t
        Mx = cv2.getRotationMatrix2D((W / 2, H / 2), 0, s); Ma = cv2.getRotationMatrix2D((W / 2, H / 2), 0, sa)
        f = cv2.warpAffine(G, Mx, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        if toc_a is not None:
            fa = cv2.warpAffine(G, Ma, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT); ma = cv2.warpAffine(A.astype(np.uint8), Ma, (W, H), flags=cv2.INTER_NEAREST) > 0
            f[ma] = fa[ma]
        wr.write(f)
    wr.release(); return p


VD = lambda p, **kw: [dict(shot='H5-05a', ghep=p, mat_na=f'{FX}/p9_matna.png', n2p_toan_khung_hien_dai=True, nam=2026, cu_may='CODINH', day_2d=dict(kieu='day', toc_do_pct_s=1.0), **kw)]
r6a = chay([tam('k1', 'p9', g9, ngoai_le=NL)], video=VD(vid('d10.avi', 1.0)))
case('KN-6', 'đẩy 2D cả khung 1,0 %/s → không (h)', bad(r6a['N2P-E'], 'h'), False)
r6e = chay([tam('k1', 'p9', g9, ngoai_le=NL)], video=VD(vid('d15.avi', 1.5)))
case('KN-6', 'đẩy 2D cả khung đúng 1,5 %/s (đo 1,505 — sai số đo 2 %) → không (h)', bad(r6e['N2P-E'], 'h'), False)
r6b = chay([tam('k1', 'p9', g9, ngoai_le=NL)], video=VD(vid('d30.avi', 3.0)))
case('KN-6', 'đẩy 2D 3,0 %/s > 1,5 %/s → (h)', bad(r6b['N2P-E'], 'h'), True)
r6c = chay([tam('k1', 'p9', g9, ngoai_le=NL)], video=VD(vid('dlech.avi', 1.0, toc_a=0.0)))
case('KN-6', 'lớp (a)-E đứng yên trong khi nền đẩy 1,0 %/s (khác quỹ đạo) → (h)', bad(r6c['N2P-E'], 'h'), True)
r6d = chay([tam('k1', 'p9', g9, ngoai_le=NL)], video=[dict(VD(P('d30.avi'))[0], day_2d=None)])
case('KN-6', 'video không khai day_2d → không đo (hành vi 1.17.8)', bad(r6d['N2P-E'], 'h'), False)
case('KN-6', 'cấp: (h) Chặn ở G2, Cảnh báo ở animatic', [] if [x for x in cap112.cap('N2P-E', dict(r6b['N2P-E'], cong='G2'))[1] if x.startswith('(h)')] and not cap112.cap('N2P-E', dict(r6b['N2P-E'], cong='animatic'))[1] else ['cấp sai'], False)

# ====================================================================== KN-4 + KN-7 NHAN-VAT-TEN (clip Omni thật, YuNet thật)
open(P('AUTHORSHIP.md'), 'w').write('| 2026-10-26 | Kênh 2 T4 London — phiếu xem v2 (00:12; P-2610b ghi) | … **H3-05b** (Godfrey Allen, khung xa, không chân dung tham chiếu) ✓ |\n')
shutil.copy(f'{FX}/p9_toa.json', P('cd.json')); import hashlib  # noqa: E401
CD = dict(tep='cd.json', sha256=hashlib.sha256(open(P('cd.json'), 'rb').read()).hexdigest())


def nvt(shot, clip, dur, **m):
    md = dict(ma=shot, t0=0.0, t1=dur, clip=clip, nhan_vat_ten=['X'], duyet_chu_du_an='AUTHORSHIP.md 2026-10-26 00:12 — phiếu xem v2 A1', **m)
    LS = [dict(shot=shot, t0=0.0, t1=dur, dur=dur, goc='md', minh_hoa=[md], ai_image=True)]
    return K7.nhan_vat_ten(dict(E4), None, LS, TMP)


H15, H35 = f'{FX}/H1-15b-l1-360p.mp4', f'{FX}/H3-05b-l1-360p.mp4'
case('KN-4', 'THẬT H1-15b cả clip (7 s) → (a) mặt giả trên trời 0,162 > 1/8 (tái hiện)', bad(nvt('H1-15b', H15, 4.625, chan_dung_tham_chieu=CD), 'a'), True)
case('KN-4', 'THẬT H1-15b cat_clip [0, 110] (4,625 s dùng) → không (a)', bad(nvt('H1-15b', H15, 4.625, chan_dung_tham_chieu=CD, cat_clip=[0, 110]), 'a', 'k'), False)
case('KN-4', 'cat_clip dài khác thời lượng đoạn → (k)', bad(nvt('H1-15b', H15, 4.625, chan_dung_tham_chieu=CD, cat_clip=[0, 50]), 'k'), True)
case('KN-4', 'cat_clip {t0, t1} giây → nhận', bad(nvt('H1-15b', H15, 4.625, chan_dung_tham_chieu=CD, cat_clip=dict(t0=0.0, t1=4.625)), 'a', 'k'), False)
NG = dict(ngay='2026-10-25', noi=['Library of Congress — không có mục', 'Wellcome Collection — không có mục'])
case('KN-7', 'THẬT H3-05b không chân dung, không khai chan_dung → (k) như 1.17.8', bad(nvt('H3-05b', H35, 6.0), 'k'), True)
case('KN-7', 'THẬT H3-05b chan_dung khong_co + nguồn đã tra + YuNet 0,070 + AUTHORSHIP 00:12 → hết (k)', bad(nvt('H3-05b', H35, 6.0, chan_dung='khong_co', chan_dung_nguon_da_tra=NG), 'k', 'a'), False)
case('KN-7', 'nguồn đã tra rỗng → (k)', bad(nvt('H3-05b', H35, 6.0, chan_dung='khong_co', chan_dung_nguon_da_tra=dict(noi=[])), 'k'), True)
case('KN-7', 'duyệt không có dòng AUTHORSHIP khớp giờ → (k)', bad(K7.nhan_vat_ten(dict(E4), None, [dict(shot='H3-05b', t0=0, t1=6, dur=6, goc='md', ai_image=True, minh_hoa=[dict(ma='H3-05b', t0=0, t1=6, clip=H35, nhan_vat_ten=['X'], chan_dung='khong_co', chan_dung_nguon_da_tra=NG, duyet_chu_du_an='AUTHORSHIP.md 2026-10-26 09:99')])], TMP), 'k'), True)
case('KN-7', 'THẬT H1-15b (mặt > 1/8) + chan_dung khong_co → (k) giữ + (a) cận mặt vẫn Chặn', bad(nvt('H1-15b', H15, 4.625, chan_dung='khong_co', chan_dung_nguon_da_tra=NG), 'a'), True)
case('KN-7', '… và (k) không được miễn khi YuNet > 1/8', bad(nvt('H1-15b', H15, 4.625, chan_dung='khong_co', chan_dung_nguon_da_tra=NG), 'k'), True)

# ====================================================================== KN-2 biến cố đo từ log máy (log thật)
LSb = [dict(shot='H1-08b', t0=0.0, dur=18.2083, log_may=f'{FX}/log-H1-08b.json'), dict(shot='H1-16', t0=18.2083, dur=7.25, log_may=f'{FX}/log-H1-16.json'),
       dict(shot='H2-03b', t0=25.4583, dur=20.1667, log_may=f'{FX}/log-H2-03b.json')]
BL = K79.bien_co_log(E4, LSb, TMP)
case('KN-2', 'THẬT H1-08b (CODINH, hoàng hôn): mặt trời qua 0° và −6° → 2 biến cố n1', [] if sum(1 for x in BL if x[1] == 'H1-08b' and x[2] == 'log:n1') == 2 else [BL[:4]], False)
case('KN-2', 'THẬT H1-16 (32 giờ trong 7,25 s): ≥ 4 biến cố n1', [] if sum(1 for x in BL if x[1] == 'H1-16' and x[2] == 'log:n1') >= 4 else [BL], False)
case('KN-2', 'THẬT H2-03b (DAY, năm 1667,05→1667,45, nắng không đổi): 0 biến cố n1; năm chạy KHÔNG tính', [x for x in BL if x[1] == 'H2-03b' and x[2] == 'log:n1'], False)
case('KN-2', 'tập T3 → không cộng (hành vi 1.17.8)', K79.bien_co_log(E3, LSb, TMP), False)
ET = dict(E4, segments=[dict(id='S', dur=45.625, shots=[dict(at=0)], beats=[dict(t=0, k='cut', s='S')])])
q0 = QN.q37(ET); q1 = QN.q37(ET, blog=BL)
case('KN-2', 'Q37 cộng biến cố log máy: TB giảm, giá trị ghi "đo log máy"', [] if q1['bien_co']['tb'] < q0['bien_co']['tb'] and 'log máy' in q1['val'] else [q1['val']], False)
case('KN-2', 'Q37 không ép đạt: H2-03b 20,17 s không biến cố → (c) vẫn TRƯỢT', [x for x in q1['loi'] if x.startswith('(c)')], True)
ET2 = dict(ET, segments=[dict(ET['segments'][0], beats=[dict(t=0, k='cut', s='S'), dict(t=30.0, k='bien_co_tl', s='nắng')])])
case('KN-2', 'beats tự khai bien_co_tl không neo mốc đặc tả → (a) như cũ (A4 1.17.7 giữ)', [x for x in QN.q37(ET2, blog=BL)['loi'] if x.startswith('(a)')], True)

ok = all(x[3] for x in R)
for rule, name, exp, good, got in R: print(('ĐÚNG' if good else 'SAI ') + f' | {rule} | {name} | kỳ vọng {exp}' + ('' if good else f' | được: {got}'))
print(f"\nselftest_k1179: {sum(x[3] for x in R)}/{len(R)} đúng kỳ vọng")
shutil.rmtree(TMP, ignore_errors=True)
sys.exit(0 if ok else 1)
