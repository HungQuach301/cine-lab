#!/opt/cine/bin/python
"""Tự kiểm luật 1.17.4 (phiên K-1.17.4, 23/10/2026; chủ dự án duyệt Q1–Q7 23/10/2026 21:45). Mỗi luật đổi/mới ≥ 1 ca ĐẠT + ≥ 1 ca TRƯỢT.
Không mạng, không API. Video thử dựng tại chỗ (thư mục tạm) từ ảnh vân tổng hợp (không dùng tài sản phim).
  BIEN-CO-V (q_bcv): tĩnh → không biến cố; chỉ máy đi (trượt + phóng + quay) → không biến cố; vật đổi cục bộ → bắt đúng giờ; cắt → bắt;
                     hàng (b)(c) đạt/trượt; miễn thẻ PP; (h) ranh shot; cấp chưa hiệu chuẩn → Cảnh báo.
  Q37 + bcv (K117-D8): tập T4 + thước đạt → biến cố đo cộng vào (b)(c); tập T3 hoặc thước chưa đạt → không cộng; không nhận su_kien log.
  Q37 (c) thẻ PP (K1173-D6): 2 thẻ × 9 s cuối phim miễn; thẻ giữa phim / 11 s / 3 thẻ → không miễn.
  MINH-HOA (a) / N2P-6 (b) (Q2): T4 bỏ trần 20 %; T3 giữ.
  MAY-19 (§19 a): mỗi cú máy một ca đạt + một ca trượt trên log khung tổng hợp; N2+ phải CODINH; KHOP 0 px; ≥ 4 loại/chương; ≤ 2 liền; THAP ≤ 12 %;
                  thiếu log → THIẾU; bảng tóm tắt t4_do chỉ đủ ở animatic.
  BAN-DO-12, TU-LIEU-10, AI-TU-LIEU, GEMINI-NGAN-SACH, GOC-CAO-60: đạt/trượt; cấp G2 ↔ animatic.
  Đầu vào thử thật (tiền kỳ T4): reports/tien-ky-t4/do/t4-may.json (bảng tóm tắt) — VONG 10,6°/s, CAU vượt; KHOP 0,0 px đạt.
  /opt/cine/bin/python checks/ll/selftest_k1174.py        mã thoát 0 = mọi ca đúng kỳ vọng"""
import copy, json, math, os, subprocess, sys, tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, ROOT)
import numpy as np  # noqa: E402
import cv2  # noqa: E402
from checks.ll import q_bcv as B, q_nhip as N, q_k116 as K6, q_k117 as K7, q_n2p as NP, q_k1174 as K, cap112  # noqa: E402

TMP = tempfile.mkdtemp(prefix='k1174-'); R = []


def case(rule, name, got, expect_fail):
    got = list(got) if got else []
    R.append((rule, name, 'bắt lỗi' if expect_fail else 'sạch', bool(got) == expect_fail, got[:2]))


def bad(x, *muc):
    L = (x.get('loi') or []) + (x.get('thieu') or [])
    return [y for y in L if not muc or any(y.startswith(f'({m})') for m in muc)]


# ====================================================================== BIEN-CO-V — video tổng hợp 640×360, 24 khung/s
rng = np.random.default_rng(1174)
def van(seed, w=1600, h=900):
    g = np.random.default_rng(seed); x = cv2.resize(g.integers(0, 255, (h // 20, w // 20, 3), dtype=np.uint8), (w, h), interpolation=cv2.INTER_CUBIC)
    x = cv2.GaussianBlur(x, (0, 0), 2.0); n = g.integers(0, 255, (h, w, 3), dtype=np.uint8)
    return cv2.addWeighted(x, 0.93, cv2.GaussianBlur(n, (0, 0), 1.2), 0.07, 0)   # vân mịn kiểu cảnh dựng (nhiễu hạt 7 %)


NEN, NEN2 = van(1), van(2)
NEN3 = np.clip(van(3).astype(np.int16) // 2 + 110, 0, 255).astype(np.uint8)   # vật mới sáng rõ (lửa/nhà mới) — đổi THẤY ĐƯỢC chắc chắn


def mk(path, n, fn, w=640, h=360):
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-nostdin', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{w}x{h}', '-r', '24', '-i', '-', '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p', path],
                         stdin=subprocess.PIPE)
    for f in range(n): p.stdin.write(np.ascontiguousarray(fn(f)).tobytes())
    p.stdin.close(); p.wait(); return path


def khung(img, tt, pan=0.0, zoom=0.0, rot=0.0, w=640, h=360):
    H_, W_ = img.shape[:2]; M = cv2.getRotationMatrix2D((W_ / 2, H_ / 2), rot * tt, 1.0 + zoom * tt); M[0, 2] += -pan * W_ * tt
    return cv2.resize(cv2.warpAffine(img, M, (W_, H_), borderMode=cv2.BORDER_REFLECT), (w, h), interpolation=cv2.INTER_AREA)


def dan(img, src, x0, y0, s=160):
    o = img.copy(); o[y0:y0 + s, x0:x0 + s] = src[y0:y0 + s, x0:x0 + s]; return o


V_TINH = mk(os.path.join(TMP, 'tinh.mp4'), 240, lambda f: khung(NEN, f / 24))
V_MAY = mk(os.path.join(TMP, 'may.mp4'), 240, lambda f: khung(NEN, f / 24, pan=0.02, zoom=0.015, rot=0.5))
V_DOI = mk(os.path.join(TMP, 'doi.mp4'), 240, lambda f: khung(dan(NEN, NEN2, 1000, 400) if f / 24 >= 5.0 else NEN, f / 24, pan=0.02, zoom=0.015, rot=0.5))
# nhịp: vật đổi cục bộ mỗi 2 s (6 ô khác nhau), máy trôi nhẹ
def nhip(f):
    I = NEN.copy()
    for j, t in enumerate((2, 4, 6, 8, 10, 12)):
        if f / 24 >= t: I = dan(I, NEN3, 120 + 230 * j, 150 + 220 * (j % 3))
    return khung(I, f / 24, pan=0.005)
V_NHIP = mk(os.path.join(TMP, 'nhip.mp4'), 336, nhip)
V_CAT = mk(os.path.join(TMP, 'cat.mp4'), 240, lambda f: khung(NEN if f < 120 else NEN2, f / 24))

Dt = B.do_video(V_TINH); Dm = B.do_video(V_MAY); Dd = B.do_video(V_DOI); Dn = B.do_video(V_NHIP); Dc = B.do_video(V_CAT)
case('BIEN-CO-V', f"clip tĩnh 10 s → 0 biến cố đo (đo {len(Dt['su_kien'])})", Dt['su_kien'], False)
case('BIEN-CO-V', f"clip chỉ máy đi (trượt 2 %/s + phóng 1,5 %/s + quay 0,5°/s) → 0 biến cố (đo {len(Dm['su_kien'])})", Dm['su_kien'], False)
hit = [e for e in Dd['su_kien'] if abs(e[0] - 5.0) <= 0.25]
case('BIEN-CO-V', f"vật đổi cục bộ ở 5,0 s trên máy đi → bắt ±0,25 s ({[e[0] for e in Dd['su_kien']]})", [] if hit and len(B.gop([e[0] for e in Dd['su_kien']])) == 1 else ['không bắt / bắt thừa'], False)
case('BIEN-CO-V', f"cắt cứng ở 5,0 s → loại 'cat' ({Dc['cat']})", [] if any(abs(t - 5.0) <= 0.05 for t in Dc['cat']) else ['không bắt cắt'], False)
nh = B.gop([e[0] for e in Dn['su_kien']])
case('BIEN-CO-V', f'6 vật đổi mỗi 2 s → bắt 6/6 ({nh})', [] if all(any(abs(u - t) <= 0.25 for u in nh) for t in (2, 4, 6, 8, 10, 12)) and len(nh) == 6 else [nh], False)

# hàng: tập T4 giả (một đoạn, ranh shot ở 0)
TLx = lambda T, shots=None: dict(tong_s=T, segments=[dict(id='A', t0=0.0, t1=T, shots=shots or [dict(t0=0.0, t1=T)])])
E4 = dict(id='t4', kenh2_tu_t4=True, khung_sach=True)
Hn = B.hang(E4, TLx(14.0), V_NHIP, 'G2', [], Dn)
case('BIEN-CO-V', f"nhịp 2 s, khoảng cuối 2 s → (b)(c) sạch ({Hn['val'][:60]}…)", bad(Hn, 'b', 'c'), False)
Ht = B.hang(E4, TLx(10.0), V_TINH, 'G2', [], Dt)
case('BIEN-CO-V', 'clip tĩnh 10 s → (b) TB > 3,5 s và (c) dài nhất 10 s > 6 s', bad(Ht, 'b', 'c'), True)
Hm = B.hang(E4, TLx(10.0), V_TINH, 'G2', [(0.0, 10.0, 'the_pp', 'PP1')], Dt)
case('BIEN-CO-V', '1.17.4 K1173-D6: cùng clip là thẻ PP cuối phim (≤ 10 s) → (c) miễn', bad(Hm, 'c'), False)
Hc = B.hang(E4, TLx(10.0, [dict(t0=0.0, t1=5.0), dict(t0=5.0, t1=10.0)]), V_CAT, 'G2', [], Dc)
case('BIEN-CO-V', '(h) bắt ranh shot 5,0 s → 100 % ≥ 95 %', bad(Hc, 'h'), False)
Hh = B.hang(E4, TLx(10.0, [dict(t0=0.0, t1=3.0), dict(t0=3.0, t1=10.0)]), V_TINH, 'G2', [], Dt)
case('BIEN-CO-V', '(h) ranh shot khai 3,0 s mà video không cắt → 0 % < 95 % (thước không tin trên tập)', bad(Hh, 'h'), True)
HCX = B.hc_tap_nay(E4)[0] if hasattr(B, 'hc_tap_nay') else B.HIEU_CHUAN   # 1.17.8: tập T4 dùng HIEU_CHUAN_T4 — bật/tắt hiệu chuẩn CỦA TẬP (kỳ vọng không đổi)
HC0 = dict(B.HIEU_CHUAN); HCX0 = dict(HCX)
HCX.update(dat=False); r0 = B.hang(E4, TLx(10.0), V_TINH, 'G2', [], Dt)
mo, ch, cb = cap112.cap('BIEN-CO-V', r0)
case('cấp', 'BIEN-CO-V thước chưa đạt hiệu chuẩn → không Chặn (chỉ Cảnh báo)', ch, False)
HCX.update(dat=True); r1 = B.hang(E4, TLx(10.0), V_TINH, 'G2', [], Dt); mo, ch, cb = cap112.cap('BIEN-CO-V', r1)
case('cấp', 'BIEN-CO-V thước đạt + G2 → (b)(c) Chặn', ch, True)
mo, ch, cb = cap112.cap('BIEN-CO-V', dict(r1, cong='animatic'))
case('cấp', 'BIEN-CO-V ở animatic → chỉ Cảnh báo', ch, False)

# ====================================================================== Q37 + bcv (K117-D8) và miễn thẻ PP (K1173-D6)
def ep37(beats_A, kenh2_tu_t4=True, pp=(9.0, 9.0), pp_at_end=True):
    segs = [dict(id='A', dur=30.0, beats=beats_A, shots=[dict(at=0, type='scene3d', p={})])]
    if not pp_at_end: segs = [dict(id='PP1', dur=pp[0], the_phuong_phap=True, beats=[dict(t=0, k='cut', s='PP1')], shots=[dict(at=0, type='card', p={})])] + segs
    else: segs += [dict(id=f'PP{i + 1}', dur=d, the_phuong_phap=True, beats=[dict(t=0, k='cut', s=f'PP{i + 1}')], shots=[dict(at=0, type='card', p={})]) for i, d in enumerate(pp)]
    E = dict(id='x', khung_sach=True, segments=segs)
    if kenh2_tu_t4: E['kenh2_tu_t4'] = True
    return E


def q37c(E, bcv=None):
    M = K6.q37_mien(E, None)
    r = N.q37(E, None, mien=M, bcv=bcv)
    return [x for x in r['loi'] if x.startswith('(b)') or x.startswith('(c)')], r, M


BA = [dict(t=0, k='cut', s='A'), dict(t=2.0, k='cut', s='g'), dict(t=4.0, k='cut', s='g'), dict(t=26.0, k='cut', s='g'), dict(t=28.0, k='cut', s='g')]
L0, r0, M0 = q37c(ep37(BA))
case('Q37', 'beat khai thưa (khoảng 4 → 26 s = 22 s) → (c)', L0, True)
EV = [(float(t), 'video', 'video:o', '1 ô') for t in range(6, 26, 2)]
L1, r1, _ = q37c(ep37(BA), bcv=EV)
case('Q37', '1.17.4: + biến cố ĐO trên video mỗi 2 s (tập T4, thước đạt) → (b)(c) sạch', L1, False)
E3 = ep37(BA, kenh2_tu_t4=False)
case('Q37', 'tập T3: q_bcv.cho_q37 không trả biến cố (không cộng) → vẫn (c)', q37c(E3, bcv=B.cho_q37(E3, dict(su_kien=[(t, 1, 9.0, 'o') for t in range(6, 26, 4)]), True))[0], True)
case('Q37', 'tập T4 nhưng thước chưa đạt hiệu chuẩn → không cộng → vẫn (c)', q37c(ep37(BA), bcv=B.cho_q37(ep37(BA), dict(su_kien=[(t, 1, 9.0, 'o') for t in range(6, 26, 4)]), False))[0], True)
case('Q37', 'tập T4 + thước đạt → cho_q37 trả biến cố → (b)(c) sạch', q37c(ep37(BA), bcv=B.cho_q37(ep37(BA), dict(su_kien=[(float(t), 1, 9.0, 'o') for t in range(6, 26, 2)]), True))[0], False)
ESK = ep37(BA); ESK['segments'][0]['su_kien'] = [dict(t=t, s='tự khai') for t in range(6, 26, 4)]
case('Q37', 'su_kien tự khai trong đặc tả/log không được nhận (K117-D8)', q37c(ESK)[0], True)
# K1173-D6
BOK = [dict(t=0, k='cut', s='A')] + [dict(t=float(t), k='cut', s='g') for t in range(2, 30, 2)]
Lp, rp, Mp = q37c(ep37(BOK))
case('Q37', f"K1173-D6: 2 thẻ PP × 9 s cuối phim → (c) miễn (miễn {[m[2] for m in Mp]})", Lp, False)
case('Q37', 'K1173-D6: trước 1.17.4 (không miễn thẻ PP) cùng tập → (c) 9 s', [x for x in N.q37(ep37(BOK), None, mien=[m for m in Mp if m[2] != 'the_pp'])['loi'] if x.startswith('(c)')], True)
case('Q37', 'K1173-D6: thẻ PP 11 s → không miễn quá 10 s → (c)', q37c(ep37(BOK, pp=(11.0, 8.0)))[0], True)
case('Q37', 'K1173-D6: thẻ PP ở ĐẦU phim (không cuối) → không miễn → (c)', q37c(ep37(BOK, pp=(9.0,), pp_at_end=False))[0], True)
case('Q37', 'K1173-D6: 3 thẻ PP liền cuối phim → (c) > 2 thẻ', q37c(ep37(BOK, pp=(8.0, 8.0, 8.0)))[0], True)

# ====================================================================== Q2: MINH-HOA (a) / N2P-6 (b)
SO = dict(model='gemini-omni-1.1-flash', lenh='…', sha_vao='aa' * 32, sha_ra='bb' * 32)
LSm = [dict(shot='A', t0=0, t1=30, dur=30, goc='cao'), dict(shot='M', t0=30, t1=55, dur=25, minh_hoa=True, goc='thap', agl_m=[30], so_ai=SO), dict(shot='B', t0=55, t1=100, dur=45, goc='cao')]
EM3 = dict(id='t3', khung_sach=True, segments=[dict(id=s, dur=d) for s, d in (('A', 30), ('M', 25), ('B', 45))])
EM4 = dict(EM3, id='t4', kenh2_tu_t4=True)
case('MINH-HOA', 'T3: minh hoạ 25 % > 20 % → (a) (không hồi tố)', bad(K7.minh_hoa(EM3, None, LSm), 'a'), True)
case('MINH-HOA', 'T4 (Q2): minh hoạ 25 % → không (a)', bad(K7.minh_hoa(EM4, None, LSm), 'a'), False)
LS6 = [dict(shot='A', dur=30, ai_nen=True), dict(shot='B', dur=25, minh_hoa=True), dict(shot='C', dur=45)]
case('N2P-6', 'T4 (Q2): minh hoạ 25 % → không (b)', bad(NP.n2p6(EM4, LS6), 'b'), False)
case('N2P-6', 'tổng AI 75 % (50 + 25) > 70 % → (c) giữ', bad(NP.n2p6(EM4, [dict(shot='A', dur=50, ai_nen=True), dict(shot='B', dur=25, minh_hoa=True), dict(shot='C', dur=25)]), 'c'), True)


# ====================================================================== MAY-19 — log khung tổng hợp (định dạng render_ldn.js)
def log(keys, dur=8.0, fps=24, W=1920, H=1080):
    """keys: hàm t → (p, l, fov) — toạ độ cảnh (y lên)"""
    fr = []
    for f in range(int(round(dur * fps))):
        p, l, fov = keys(f / fps); fr.append(dict(f=f, cam=dict(p=list(map(float, p)), l=list(map(float, l)), fov=float(fov)), year=1666.6))
    return dict(W=W, H=H, shot=dict(fps=fps, dur=dur), frames=fr)


F0 = np.array([0.0, 40.0, -600.0])
def tr(dx=0.0, dy=0.0, dz=0.0, base=(0.0, 230.0, 400.0), lk=None, fov=50.0, dfov=0.0):
    return lambda t: (np.array(base) + np.array([dx, dy, dz]) * t, (F0 if lk is None else lk(t)), fov + dfov * t)
def quay(deg_s, R=1000.0, h=230.0):
    return lambda t: (F0 + np.array([R * math.sin(math.radians(deg_s * t)), h - F0[1], R * math.cos(math.radians(deg_s * t))]), F0, 50.0)
def nhin(pitch0, pitch1, T=6.0, h=2200.0):
    def k(t):
        a = math.radians(pitch0 + (pitch1 - pitch0) * min(1.0, t / T)); p = np.array([0.0, h, 0.0])
        return p, p + np.array([0.0, math.sin(a), -math.cos(a)]) * 100.0, 40.0
    return k
def thap(h, ngua):
    return lambda t: (np.array([0.0, h, 300.0]), np.array([0.0, h, 300.0]) + np.array([0.0, math.sin(math.radians(ngua)), -math.cos(math.radians(ngua))]) * 100, 35.0)


def L1(cu, keys, dur=8.0, **kw):
    d = dict(shot=cu.lower(), t0=0.0, dur=dur, chuong='1', cu_may=cu, goc='cao', tl=True, log_may=log(keys, dur)); d.update(kw); return d


def may(LS, E=None, cong='G2'):
    return K.may19(E or dict(id='t4', kenh2_tu_t4=True), None, LS, '.', cong)


dist0 = float(np.linalg.norm(np.array([0.0, 230.0, 400.0]) - F0))
CA = [('CODINH', tr(dx=0.5, lk=lambda t: F0 + np.array([0.5 * t, 0, 0])), tr(dx=40.0, lk=lambda t: F0 + np.array([40.0 * t, 0, 0])), 'trôi máy + điểm nhìn 0,5 → 40 m/s'),
      ('DAY', tr(dz=-0.010 * dist0), tr(dz=-0.03 * dist0), 'tiến 1 % → 3 % khoảng cách/s'),
      ('KEO', tr(dz=0.015 * dist0), tr(dz=0.04 * dist0), 'lùi 1,5 % → 4 % khoảng cách/s'),
      ('CAU', tr(dy=4.0, lk=lambda t: F0), tr(dy=10.0, lk=lambda t: F0), 'dọc 4 → 10 m/s'),
      ('VONG', quay(2.5), quay(5.0), 'vòng 2,5 → 5°/s'),
      ('TRUOT', tr(dx=15.0, lk=lambda t: F0 + np.array([15.0 * t, 0, 0])), tr(dx=60.0, lk=lambda t: F0 + np.array([60.0 * t, 0, 0])), 'tiêu điểm dịch chậm → nhanh'),
      ('NGHIENG', nhin(-10, -20, 8.0, 230.0), nhin(-10, -40, 8.0, 230.0), 'nghiêng 1,25 → 3,75°/s'),
      ('THAP', thap(40.0, 10.0), thap(90.0, 10.0), 'máy 40 m → 90 m'),
      ('XUONG', nhin(-89.9, -30.0, 6.0), nhin(-89.9, -30.0, 2.0), 'chuyển 6 s → 2 s')]
for cu, ok, ko, ten in CA:
    case('MAY-19', f'{cu} đạt ({ten})', bad(may([L1(cu, ok)]), 'a'), False)
    case('MAY-19', f'{cu} trượt ({ten})', bad(may([L1(cu, ko)]), 'a'), True)
case('MAY-19', '(b) shot ai_nen khai VONG (không CODINH) → (b)', bad(may([L1('VONG', quay(2.5), ai_nen=True)]), 'b'), True)
case('MAY-19', '(b) shot ai_nen CODINH trôi 0,05 %/s → sạch (b)', bad(may([L1('CODINH', tr(dx=0.5), ai_nen=True)]), 'b'), False)
KA = L1('CODINH', tr(), shot='p1-1666')
case('MAY-19', '(c) KHOP cùng máy cùng FOV → 0 px', bad(may([KA, L1('KHOP', tr(), shot='p1-1711', t0=8.0, khop_voi='p1-1666')]), 'c'), False)
case('MAY-19', '(c) KHOP lệch máy 2 m → > 0,5 px', bad(may([KA, L1('KHOP', tr(base=(2.0, 230.0, 400.0)), shot='p1-1711', t0=8.0, khop_voi='p1-1666')]), 'c'), True)
case('MAY-19', '(c) KHOP FOV khác 50 → 51°', bad(may([KA, L1('KHOP', tr(fov=51.0), shot='p1-1711', t0=8.0, khop_voi='p1-1666')]), 'c'), True)
def chuoi(cus, ch='1'):
    return [dict(shot=f's{i}', t0=8.0 * i, dur=8.0, chuong=ch, cu_may=c, goc='cao', tl=True, log_may=log(tr(), 8.0) if c != 'LAN' else None) for i, c in enumerate(cus)]
case('MAY-19', '(d) chương 4 loại (CODINH, DAY, VONG, CAU) → sạch', bad(may(chuoi(['CODINH', 'DAY', 'VONG', 'CAU'])), 'd'), False)
case('MAY-19', '(d) chương 3 loại → (d)', bad(may(chuoi(['CODINH', 'DAY', 'VONG', 'CODINH'])), 'd'), True)
case('MAY-19', '(e) 2 shot liền CODINH → sạch', bad(may(chuoi(['CODINH', 'CODINH', 'DAY', 'VONG', 'CAU'])), 'e'), False)
case('MAY-19', '(e) 3 shot liền CODINH → (e)', bad(may(chuoi(['CODINH', 'CODINH', 'CODINH', 'DAY', 'VONG', 'CAU'])), 'e'), True)
case('MAY-19', '(e) MD xen giữa ngắt chuỗi', bad(may(chuoi(['CODINH', 'CODINH', 'MD', 'CODINH', 'DAY', 'VONG', 'CAU'])), 'e'), False)
TH = [L1('THAP', thap(40.0, 10.0), dur=12.0)] + [dict(shot=f'x{i}', t0=12.0 + 8 * i, dur=8.0, chuong='1', cu_may='LAN', goc='cao', tl=True) for i in range(11)]
case('MAY-19', '(f) THAP 12 s / 100 s = 12 % (đúng trần) → sạch', bad(may(TH), 'f'), False)
case('MAY-19', '(f) THAP 13 s / 101 s > 12 % → (f)', bad(may([dict(TH[0], dur=13.0, log_may=log(thap(40.0, 10.0), 13.0))] + TH[1:]), 'f'), True)
case('MAY-19', '(g) shot 3D không log máy → THIẾU', bad(may([dict(shot='z', t0=0, dur=8, chuong='1', cu_may='DAY', goc='cao', tl=True)]), 'g'), True)
case('MAY-19', '(g) shot không khai cu_may → THIẾU', bad(may([dict(shot='z', t0=0, dur=8, chuong='1', goc='cao', tl=True)]), 'g'), True)
cw = cap112.cap('MAY-19', dict(may([L1('KEO', tr(dz=0.015 * dist0))]), cong='G2'))
case('MAY-19', '(w) KEO không khai lo_ra → Cảnh báo, không Chặn', [x for x in cw[1] if x.startswith('(w)')] or ([] if any(x.startswith('(w)') for x in cw[2]) else ['không có (w)']), False)
# bảng tóm tắt t4_do (đầu vào thử thật)
T4M = json.load(open(os.path.join(ROOT, 'reports', 'tien-ky-t4', 'do', 't4-may.json')))
TT = {d['doan']: d for d in T4M['doan']}
LST = [dict(shot=k, t0=3.0 * i, dur=TT[k]['giay'], chuong='thu', cu_may=c, goc='cao', tl=True, log_may_tom_tat=TT[k], lo_ra='x') for i, (k, c) in enumerate((('a-day', 'DAY'), ('b-vong', 'VONG'), ('c-cau', 'CAU'), ('d-khop', 'KHOP')))]
RT = may(LST, cong='animatic')
case('MAY-19', 'tiền kỳ T4 (t4-may.json): DAY tiêu điểm 1,06 %/s ≤ 1,5 → sạch', [x for x in bad(RT, 'a') if 'a-day' in x], False)
case('MAY-19', 'tiền kỳ T4: VONG quay 12,64°/s > 3 → (a)', [x for x in bad(RT, 'a') if 'b-vong' in x], True)
case('MAY-19', 'tiền kỳ T4: CAU 130,9 m/s, 4,77°/s → (a)', [x for x in bad(RT, 'a') if 'c-cau' in x], True)
case('MAY-19', 'tiền kỳ T4: KHOP lệch neo 0,0 px → sạch (c)', bad(RT, 'c'), False)
case('MAY-19', 'bảng tóm tắt ở animatic: không THIẾU (g)', bad(RT, 'g'), False)
case('MAY-19', 'bảng tóm tắt ở G2: THIẾU (g) — phải đo từ log khung', bad(may(LST, cong='G2'), 'g'), True)
mo, ch, cb = cap112.cap('MAY-19', RT)
case('cấp', 'MAY-19 ở animatic → chỉ Cảnh báo', ch, False)
mo, ch, cb = cap112.cap('MAY-19', may(LST, cong='G2'))
case('cấp', 'MAY-19 ở G2 → Chặn', ch, True)

# ====================================================================== BAN-DO-12, TU-LIEU-10, AI-TU-LIEU
E4b = dict(id='t4', kenh2_tu_t4=True)
LSb = lambda mp, m3, tl=0, kh=0, th=0: [dict(shot='a', dur=10, lop=dict(MAP=mp, MAP3D=m3, TL=tl, KHAC=kh, THE=th)), dict(shot='b', dur=90)]
case('BAN-DO-12', 'bản đồ 12 s / 100 s = 12 % (đúng trần) → sạch', bad(K.ban_do_12(E4b, None, [dict(shot='a', dur=12, lop=dict(MAP=8, MAP3D=4)), dict(shot='b', dur=88)])), False)
case('BAN-DO-12', 'bản đồ 13 % → (a)', bad(K.ban_do_12(E4b, None, [dict(shot='a', dur=13, lop=dict(MAP=9, MAP3D=4)), dict(shot='b', dur=87)]), 'a'), True)
case('BAN-DO-12', 'bản đồ cổ một lần 11 s → (b)', bad(K.ban_do_12(E4b, None, [dict(shot='a', dur=11, lop=dict(MAP=11)), dict(shot='b', dur=89)]), 'b'), True)
case('TU-LIEU-10', 'TL 4 + KHAC 3 + THE 3 = 10 % → sạch', bad(K.tu_lieu_10(E4b, None, LSb(0, 0, 4, 3, 3))), False)
case('TU-LIEU-10', 'TL 5 + KHAC 3 + THE 3 = 11 % → (a)', bad(K.tu_lieu_10(E4b, None, [dict(shot='a', dur=11, lop=dict(TL=5, KHAC=3, THE=3)), dict(shot='b', dur=89)])), True)
SHAF = os.path.join(TMP, 'sha.txt'); open(SHAF, 'w').write('ab' * 32 + '  tu-lieu/doornick.jpg\n')
SOF = os.path.join(TMP, 'so.jsonl'); open(SOF, 'w').write(json.dumps(dict(tag='x', nha='openai', input=[dict(file='a.jpg', sha256='cd' * 32)])) + '\n')
SOB = os.path.join(TMP, 'so-bad.jsonl'); open(SOB, 'w').write(json.dumps(dict(tag='y', nha='openai', input=[dict(file='doornick.jpg', sha256='ab' * 32)])) + '\n')
EA = dict(E4b, sha_tu_lieu=SHAF, so_ai=SOF)
case('AI-TU-LIEU', 'shot bản đồ cổ không AI; sổ AI không có SHA tư liệu → sạch', bad(K.ai_tu_lieu(EA, [dict(shot='a', dur=9, lop=dict(MAP=9))], TMP)), False)
case('AI-TU-LIEU', 'shot tranh khắc khai ai_image → (a)', bad(K.ai_tu_lieu(EA, [dict(shot='a', dur=9, lop=dict(KHAC=4), ai_image=True)], TMP), 'a'), True)
case('AI-TU-LIEU', 'shot tấm nền N2+ + tư liệu không khai chồng sau AI → (a)', bad(K.ai_tu_lieu(EA, [dict(shot='a', dur=9, lop=dict(KHAC=4), ai_nen=True)], TMP), 'a'), True)
case('AI-TU-LIEU', 'tấm nền N2+ + tư liệu chồng SAU ghép (khai) → sạch', bad(K.ai_tu_lieu(EA, [dict(shot='a', dur=9, lop=dict(KHAC=4), ai_nen=True, tu_lieu_chong_sau_ai=True)], TMP)), False)
case('AI-TU-LIEU', 'sổ AI có đầu vào = SHA bản đồ cổ → (b)', bad(K.ai_tu_lieu(dict(EA, so_ai=SOB), [dict(shot='a', dur=9, lop=dict(MAP=9))], TMP), 'b'), True)

# ====================================================================== GEMINI-NGAN-SACH, GOC-CAO-60
GF = os.path.join(TMP, 'gem.jsonl')
open(GF, 'w').write(''.join(json.dumps(dict(tag=f'M{i}', nha='gemini', model_req='gemini-omni-1.1-flash', usd=1.02)) + '\n' for i in range(24))
                    + json.dumps(dict(tag='o', nha='openai', usd=9.0)) + '\n')
EG = dict(E4b, so_ai_gemini=GF, ngan_sach_gemini_usd=30, ngan_sach_gemini_moc_usd=25)
rg = K.gemini_ngan_sach(EG, TMP)
case('GEMINI-NGAN-SACH', f"24 lệnh × $1,02 = ${rg.get('usd')} ≤ $30 (bỏ dòng OpenAI) → sạch (a)", bad(rg, 'a', 'u'), False)
case('GEMINI-NGAN-SACH', 'vượt mốc theo dõi $25 → (m) Cảnh báo, không Chặn', [x for x in cap112.cap('GEMINI-NGAN-SACH', rg)[1]], False)
case('GEMINI-NGAN-SACH', 'ngân sách $20 → (a) Chặn ở G2', cap112.cap('GEMINI-NGAN-SACH', K.gemini_ngan_sach(dict(EG, ngan_sach_gemini_usd=20), TMP))[1], True)
case('GEMINI-NGAN-SACH', 'ngân sách $20 ở animatic → chỉ Cảnh báo', cap112.cap('GEMINI-NGAN-SACH', K.gemini_ngan_sach(dict(EG, ngan_sach_gemini_usd=20), TMP, 'animatic'))[1], False)
case('GEMINI-NGAN-SACH', 'không khai ngân sách → (k) Cảnh báo (không Chặn)', cap112.cap('GEMINI-NGAN-SACH', K.gemini_ngan_sach({k: v for k, v in EG.items() if k != 'ngan_sach_gemini_usd'}, TMP))[1], False)
case('GEMINI-NGAN-SACH', 'không khai ngân sách → có (k)', bad(K.gemini_ngan_sach({k: v for k, v in EG.items() if k != 'ngan_sach_gemini_usd'}, TMP), 'k'), True)
GU = os.path.join(TMP, 'gem-u.jsonl'); open(GU, 'w').write(json.dumps(dict(tag='M1', nha='gemini', usage={'total_tokens': 59712})) + '\n')
case('GEMINI-NGAN-SACH', 'dòng Gemini thiếu giá thật usd → (u) THIẾU', bad(K.gemini_ngan_sach(dict(EG, so_ai_gemini=GU), TMP), 'u'), True)
LSg = lambda cao: [dict(shot='a', dur=cao, goc='cao', tl=True), dict(shot='b', dur=100 - cao, goc='thap', tl=True)]
case('GOC-CAO-60', 'góc cao 60 s / 100 s = 60 % (đúng ngưỡng) → sạch', bad(K.goc_cao_60(E4b, None, LSg(60))), False)
case('GOC-CAO-60', 'góc cao 59 % → (a)', bad(K.goc_cao_60(E4b, None, LSg(59))), True)
case('GOC-CAO-60', 'thẻ PP không tính vào thân phim: 58 / (100 − 4) = 60,4 % → sạch', bad(K.goc_cao_60(E4b, None, LSg(58)[:1] + [dict(shot='b', dur=38, goc='thap', tl=True), dict(shot='pp', dur=4, cu_may='PP')])), False)
LV = [dict(shot='a', dur=60, goc='cao', tl=True, log_may=log(lambda t: (np.array([0.0, 30.0, 0.0]), np.array([0.0, 30.0, -100.0]), 50.0), 4.0)), dict(shot='b', dur=40, goc='thap', tl=True)]
case('GOC-CAO-60', 'khai goc cao nhưng log khung: máy 30 m nhìn ngang (không đạt V7B-D1) → (a)', bad(K.goc_cao_60(E4b, None, LV)), True)

# ====================================================================== áp dụng
case('áp dụng', 'tập T3 → 6 hàng 1.17.4 KHÔNG ÁP', [k for k, v in K.check(dict(id='t3', khung_sach=True), None, '.', []).items() if v.get('ket_qua') != 'KHÔNG ÁP'], False)
B.HIEU_CHUAN.clear(); B.HIEU_CHUAN.update(HC0); HCX.clear(); HCX.update(HCX0)

# ---------------------------------------------------------------------- in kết quả
ok = all(x[3] for x in R)
for rule, name, kv, good, got in R: print(f"{'ĐÚNG' if good else 'SAI '} [{rule}] {name} — kỳ vọng {kv}" + ('' if good else f' · được {got}'))
print(f"\nselftest_k1174: {sum(x[3] for x in R)}/{len(R)} ca đúng kỳ vọng — {'ĐẠT' if ok else 'TRƯỢT'}")
sys.exit(0 if ok else 1)
