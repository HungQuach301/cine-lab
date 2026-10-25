#!/opt/cine/bin/python
"""Tự kiểm luật 1.17.7 (phiên K-1.17.7, 25/10/2026). Mỗi luật đổi/mới ≥ 1 ca ĐẠT + ≥ 1 ca TRƯỢT; ca "mặc định giữ hành vi cũ" cho mỗi tham số.
Không mạng, không API (mô hình nhìn giả lập). Fixtures: checks/ll/fixtures/k1177/mat-can.jpg, mat-xa.jpg (khung M-d animatic T4 H2-03c-l1 cắt +
phóng 640×360 — mặt 0,236 / ≤ 0,093 chiều cao khung).
  GOC-CAO: mặc định 60 + chốt TẮT · khai 50 (+ chốt bật) · (k) < 50 · (a) mở/kết chương · (b) P1 mỗi hồi (log cùng khung / khác khung / không log)
           · (c) ≤ 2 liền {thấp, cận, M-d, THAT} · (d) chương ≥ 40 % · THAT không tính góc cao · (e) TL-1 tl1_muc_tieu_pct.
  TU-LIEU: tu_lieu_tran_pct 20 nhận / 25 (k) · THAT tính vào trần, (b) ≤ 10 s, OMNI · TU-LIEU-THAT (a) AI, (g) giấy phép footage hiện đại (SHA).
  K-LAI-1 T4 (Q2/C11): M-d không tính 20 %; ai_image ngoài M-d vẫn ≤ 20 %; T3 (q_lai) không đổi.
  TL-1 (c) P9: ranh vào/ra M-d / THAT / tu_lieu_lan không tính cắt/phút; in trước/sau; T3 không miễn.
  NHAN-VAT-TEN: mặt 0,236 > 1/8 → (a); mặt ≤ 0,093 → đạt; thiếu duyệt → (u); chân dung SHA sai → (k); không video → (m).
  KIEM-2-MUC: không khai → KHÔNG ÁP; nen + nhân vật có tên → (a); nen đủ → đạt; nen 3 lượt → (c); day_du đủ → đạt; mốc + đề bài cũ → (d).
  q_thoi_dai: moc None = đề bài + khoá 1.15 từng chữ; lớp mốc thêm mục 9; nghi vấn cong_trinh_moc không qua bước 2 (mô hình giả lập).
  MAY-19 (A1/A2): KHOP về khung ĐẦU shot DAY → đạt (1.17.6 trượt); lệch thật → (c); diem_neo [E, N, h] → đổi + (w); log toa_do EN = log hệ cảnh.
  Q37 (a) A4: p.lop_chong nhận mốc at / at + mo_vao_s; không khai → (a) như cũ.  N2P A5: thông báo chỉ khuôn episode.yaml n2p.tam.
  BMN (d) D6: sàn Y 0 = thước cũ; nắng tắt gần đen: không sàn trượt → sàn 0,01 đạt; nhiễu bề mặt sáng vẫn trượt có sàn.
  Cấp G2 ↔ animatic; áp dụng (T3 KHÔNG ÁP).
  /opt/cine/bin/python checks/ll/selftest_k1177.py        mã thoát 0 = mọi ca đúng kỳ vọng"""
import copy, hashlib, json, os, sys, tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, ROOT)
import numpy as np  # noqa: E402
import cv2  # noqa: E402
from checks.ll import q_k1177 as K7, q_k1174 as K74, q_k1176 as K76, q_k1175 as K75, q_k116 as K6, q_lai as LA, q_nhip as QN, q_n2p as NP, q_thoi_dai as QT, cap112  # noqa: E402

TMP = tempfile.mkdtemp(prefix='k1177-'); R = []
FX = os.path.join(ROOT, 'checks', 'll', 'fixtures', 'k1177')


def case(rule, name, got, expect_fail):
    got = list(got) if got else []
    R.append((rule, name, 'bắt lỗi' if expect_fail else 'sạch', bool(got) == expect_fail, got[:2]))


def bad(x, *muc):
    L = (x.get('loi') or []) + (x.get('thieu') or [])
    return [y for y in L if not muc or any(y.startswith(f'({m})') for m in muc)]


E4 = dict(id='t4', kenh2_tu_t4=True); E3 = dict(id='t3', khung_sach=True)


# ====================================================================== GOC-CAO
def sh(nm, t0, d, ch, goc='cao', **kw):
    x = dict(shot=nm, t0=t0, dur=d, t1=t0 + d, chuong=ch, goc=goc, tl=goc in ('cao', 'thap'), cu_may=kw.pop('cu_may', 'CODINH' if goc == 'cao' else ('MD' if goc == 'md' else 'THAP')))
    if goc == 'md': x.update(minh_hoa=True, tl=False)
    x.update(kw); return x


def phim(spec):
    """spec: [(chương, [(goc, giây, kw?)…])…] → log shot liên tục"""
    t, out, i = 0.0, [], 0
    for ch, L in spec:
        for z in L:
            g, d = z[0], z[1]; kw = z[2] if len(z) > 2 else {}
            out.append(sh(f's{i:02d}', t, d, ch, g, **kw)); t += d; i += 1
    return out


TOT = [('MÓC', [('cao', 10, dict(diem_may='P1')), ('cao', 10)]),
       ('HỒI 1', [('cao', 10), ('md', 5), ('thap', 5), ('cao', 10, dict(diem_may='P1')), ('cao', 10)]),
       ('HỒI 2', [('cao', 10), ('md', 5), ('cao', 10, dict(diem_may='P1')), ('md', 5), ('cao', 10)])]
LT = phim(TOT)   # 110 s; góc cao 90 s = 81,8 %
A = dict(E4, animatic=True)
case('GOC-CAO mặc định', 'không khai: ngưỡng 60, chốt cấu trúc TẮT — phim mở chương bằng M-d vẫn sạch nếu ≥ 60 %',
     bad(K7.goc_cao(E4, None, phim([('HỒI 1', [('md', 5), ('cao', 60), ('thap', 35)])]))), False)
case('GOC-CAO mặc định', 'không khai: 59 % → (p) như GOC-CAO-60', bad(K7.goc_cao(E4, None, phim([('HỒI 1', [('cao', 59), ('thap', 41)])])), 'p'), True)
case('GOC-CAO khai 50', 'goc_cao_min_pct 50, cấu trúc đủ, 81,8 % → sạch (animatic: P1 theo khai → chỉ (w))', bad(K7.goc_cao(dict(A, goc_cao_min_pct=50), None, LT), 'p', 'a', 'b', 'c', 'd', 'k'), False)
L52 = phim([('HỒI 1', [('cao', 10, dict(diem_may='P1')), ('thap', 5), ('cao', 10), ('md', 5), ('cao', 6), ('thap', 6), ('cao', 6), ('thap', 8), ('cao', 4)])])   # 36/60 = 60 % … chỉnh dưới
L49 = phim([('HỒI 1', [('cao', 10, dict(diem_may='P1')), ('thap', 6), ('cao', 9), ('md', 5), ('cao', 6), ('thap', 8), ('cao', 2), ('thap', 8), ('cao', 2.4)])])   # 29,4/56,4 = 52 %
L48 = phim([('HỒI 1', [('cao', 10, dict(diem_may='P1')), ('thap', 6), ('cao', 9), ('md', 5), ('cao', 6), ('thap', 8), ('cao', 1), ('thap', 10), ('cao', 1)])])   # 27/56 = 48,2 %
case('GOC-CAO khai 50', '52 % ≥ 50 → (p) sạch', bad(K7.goc_cao(dict(A, goc_cao_min_pct=50), None, L49), 'p'), False)
case('GOC-CAO khai 50', '48,2 % < 50 → (p)', bad(K7.goc_cao(dict(A, goc_cao_min_pct=50), None, L48), 'p'), True)
case('GOC-CAO (k)', 'khai 45 (< 50 % đã duyệt) → (k), dùng 60', bad(K7.goc_cao(dict(A, goc_cao_min_pct=45), None, LT), 'k'), True)
LA_ = phim([('MÓC', [('cao', 10, dict(diem_may='P1')), ('cao', 10)]),
            ('HỒI 1', [('md', 5), ('cao', 30, dict(diem_may='P1')), ('thap', 5)])])
case('GOC-CAO (a)', 'HỒI 1 mở bằng M-d, kết bằng góc thấp → (a) ×2', [x for x in bad(K7.goc_cao(dict(A, goc_cao_min_pct=50), None, LA_), 'a')][:2] if len(bad(K7.goc_cao(dict(A, goc_cao_min_pct=50), None, LA_), 'a')) == 2 else [], True)
LB = phim([('MÓC', [('cao', 10, dict(diem_may='P1')), ('cao', 10)]), ('HỒI 1', [('cao', 20, dict(diem_may='P2')), ('cao', 10)])])
case('GOC-CAO (b)', 'HỒI 1 không có shot P1 → (b)', bad(K7.goc_cao(dict(A, goc_cao_min_pct=50), None, LB), 'b'), True)
case('GOC-CAO (b)', 'có P1 không log ở animatic → không (b), chỉ (w)', bad(K7.goc_cao(dict(A, goc_cao_min_pct=50), None, LT), 'b'), False)
case('GOC-CAO (b) G2', 'có P1 không log ở G2 → THIẾU (b)', bad(K7.goc_cao(dict(E4, goc_cao_min_pct=50), None, LT), 'b'), True)


def logm(nm, p, l, fov=36, n=48, dp=(0, 0, 0)):
    fr = [dict(f=i, cam=dict(p=[p[0] + dp[0] * i / n, p[1] + dp[1] * i / n, p[2] + dp[2] * i / n], l=list(l), fov=fov)) for i in range(n)]
    path = os.path.join(TMP, nm + '.json'); json.dump(dict(W=640, H=360, shot=dict(fps=24), frames=fr), open(path, 'w')); return path


P1p, P1l = (330.0, 230.0, 550.0), (420.0, 15.0, -180.0)
LBg = copy.deepcopy(LT)
for s in LBg:
    if s.get('diem_may') == 'P1': s['log_may'] = logm(s['shot'], P1p, P1l)
case('GOC-CAO (b) log', 'P1 mỗi hồi có log cùng khung với P1 đầu phim (G2) → (b) sạch', bad(K7.goc_cao(dict(E4, goc_cao_min_pct=50), None, LBg, TMP), 'b'), False)
LBk = copy.deepcopy(LBg)
for s in LBk:
    if s['chuong'] == 'HỒI 2' and s.get('diem_may') == 'P1': s['log_may'] = logm(s['shot'] + 'x', (P1p[0] + 40, P1p[1], P1p[2]), P1l)
case('GOC-CAO (b) log', 'HỒI 2: shot khai P1 nhưng máy dời 40 m (khác khung) → (b)', bad(K7.goc_cao(dict(E4, goc_cao_min_pct=50), None, LBk, TMP), 'b'), True)
LC = phim([('MÓC', [('cao', 10, dict(diem_may='P1')), ('cao', 10)]),
           ('HỒI 1', [('cao', 20, dict(diem_may='P1')), ('md', 5), ('thap', 5), ('md', 5), ('cao', 30)])])
case('GOC-CAO (c)', 'M-d, thấp, M-d liền nhau (3) → (c)', bad(K7.goc_cao(dict(A, goc_cao_min_pct=50), None, LC), 'c'), True)
LC2 = phim([('MÓC', [('cao', 10, dict(diem_may='P1')), ('cao', 10)]),
            ('HỒI 1', [('cao', 20, dict(diem_may='P1')), ('md', 5), ('phang', 4, dict(lop={'THAT': 4}, that=dict(loai='anh'), cu_may='THAT')), ('md', 5), ('cao', 30)])])
case('GOC-CAO (c)', 'M-d, ảnh thật (THAT), M-d liền (3) → (c)', bad(K7.goc_cao(dict(A, goc_cao_min_pct=50), None, LC2), 'c'), True)
case('GOC-CAO (c)', '≤ 2 liền (M-d, thấp) → sạch', bad(K7.goc_cao(dict(A, goc_cao_min_pct=50), None, LT), 'c'), False)
LD = phim([('MÓC', [('cao', 10, dict(diem_may='P1')), ('cao', 10)]),
           ('HỒI 1', [('cao', 6, dict(diem_may='P1')), ('thap', 10), ('md', 6), ('cao', 1), ('thap', 10), ('md', 6), ('cao', 6)])])   # 13/45 = 28,9 %
case('GOC-CAO (d)', 'HỒI 1 góc cao 28,9 % < 40 % → (d)', bad(K7.goc_cao(dict(A, goc_cao_min_pct=50, goc_cao_chuong_min_pct=40), None, LD), 'd'), True)
case('GOC-CAO (d)', 'mọi chương ≥ 40 % → sạch', bad(K7.goc_cao(dict(A, goc_cao_min_pct=50, goc_cao_chuong_min_pct=40), None, LT), 'd'), False)
LTH = phim([('HỒI 1', [('cao', 50, dict(diem_may='P1')), ('cao', 20, dict(lop={'THAT': 20}, that=dict(loai='anh'))), ('thap', 30)])])
gTH = K7.goc_cao(E4, None, LTH)
case('GOC-CAO THAT', 'shot THAT khai goc cao không tính: 50/100 = 50 % < 60 → (p)', bad(gTH, 'p') if gTH.get('pct') == 50.0 else [f"pct {gTH.get('pct')}"], True)
case('áp dụng GOC-CAO', 'T3 → q_k1177.check KHÔNG ÁP cả 4 hàng', [k for k, v in K7.check(E3, None, '.', LT).items() if v.get('ket_qua') != 'KHÔNG ÁP'], False)
o74 = K74.check(dict(A, goc_cao_min_pct=50), None, '.', LT)
case('GOC-CAO (q_k1174.check)', 'T4: q_k1174.check trả GOC-CAO (không còn GOC-CAO-60) + TU-LIEU-THAT, NHAN-VAT-TEN, KIEM-2-MUC',
     [] if ('GOC-CAO' in o74 and 'GOC-CAO-60' not in o74 and all(k in o74 for k in ('TU-LIEU-THAT', 'NHAN-VAT-TEN', 'KIEM-2-MUC'))) else [sorted(o74)], False)


# (e) TL-1 tl1_muc_tieu_pct
def ep_seg(LS):
    return dict(segments=[dict(id=s['shot'], dur=s['dur'], shots=[dict(at=0, type='scene3d', p={})], beats=[dict(t=0, k='cut', s=s['shot'])]) for s in LS])


L65 = phim([('HỒI 1', [('cao', 65, dict(diem_may='P1')), ('thap', 35)])])
case('GOC-CAO (e) TL-1', 'không khai: 65 % < 75 → TL-1 (a)', bad(K6.tl1(dict(E4, **ep_seg(L65)), None, L65), 'a'), True)
case('GOC-CAO (e) TL-1', 'tl1_muc_tieu_pct 60: 65 % → TL-1 (a) sạch', bad(K6.tl1(dict(E4, tl1_muc_tieu_pct=60, **ep_seg(L65)), None, L65), 'a'), False)

# ====================================================================== TU-LIEU (trần 20, THAT)
L100 = lambda **lop: [dict(shot='a', t0=0, dur=20, t1=20, lop={k: v / 2 for k, v in lop.items()}), dict(shot='a2', t0=20, dur=20, t1=40, lop={k: v / 2 for k, v in lop.items()}), dict(shot='b', t0=40, dur=60, t1=100)]   # 2 lần, mỗi lần ≤ 10 s
case('TU-LIEU-10 trần 20', 'khai 20: TL 10 + KHAC 9 = 19 % → sạch', bad(K76.tu_lieu_10(dict(E4, tu_lieu_tran_pct=20), None, L100(TL=10, KHAC=9))), False)
case('TU-LIEU-10 trần 20', 'khai 20: 21 % → (a)', bad(K76.tu_lieu_10(dict(E4, tu_lieu_tran_pct=20), None, L100(TL=10, KHAC=11)), 'a'), True)
case('TU-LIEU-10 trần 20', 'khai 25 → (k), dùng 10', bad(K76.tu_lieu_10(dict(E4, tu_lieu_tran_pct=25), None, L100(TL=5)), 'k'), True)
case('TU-LIEU-10 mặc định', 'không khai: 11 % → (a) như 1.17.6 (trần 10)', bad(K76.tu_lieu_10(E4, None, L100(TL=11)), 'a'), True)
LTA = [dict(shot='a', t0=0, dur=8, t1=8, lop={'TL': 8}), dict(shot='p', t0=8, dur=8, t1=16, lop={'THAT': 8}, that=dict(loai='anh')), dict(shot='b', t0=16, dur=84, t1=100)]
case('TU-LIEU-10 THAT', 'TL 8 + THAT 8 = 16 % > trần 15 → (a) (THAT tính vào tư liệu)', bad(K76.tu_lieu_10(dict(E4, tu_lieu_tran_pct=15), None, LTA), 'a'), True)
case('TU-LIEU-10 THAT', 'TL 8 + THAT 8 = 16 % ≤ trần 20 → sạch', bad(K76.tu_lieu_10(dict(E4, tu_lieu_tran_pct=20), None, LTA)), False)
case('TU-LIEU-10 THAT (b)', 'ảnh thật một lần 12 s → (b) ≤ 10 s/lần', bad(K76.tu_lieu_10(dict(E4, tu_lieu_tran_pct=20), None, [dict(shot='p', t0=0, dur=12, t1=12, lop={'THAT': 12}, that={}), dict(shot='b', t0=12, dur=88, t1=100)]), 'b'), True)
LOM = [dict(shot='p', t0=0, dur=6, t1=6, lop={'THAT': 6}, that={}), dict(shot='m', t0=6, dur=6, t1=12, minh_hoa=True), dict(shot='b', t0=12, dur=20, t1=32)]
case('TU-LIEU-OMNI THAT', 'ảnh thật ghép liền clip M-d → (b)', bad(K76.tu_lieu_omni(E4, None, LOM), 'b'), True)
LOM2 = [LOM[0], dict(shot='c', t0=6, dur=4, t1=10), dict(LOM[1], t0=10, t1=16), dict(shot='b', t0=16, dur=20, t1=36)]
case('TU-LIEU-OMNI THAT', 'ảnh thật — 4 s 3D — M-d → sạch', bad(K76.tu_lieu_omni(E4, None, LOM2)), False)
gp = os.path.join(TMP, 'giay-phep.txt'); open(gp, 'w').write('CC BY 4.0 — footage 2024, nguồn X\n'); gsha = hashlib.sha256(open(gp, 'rb').read()).hexdigest()
FT = lambda **t: [dict(shot='f', t0=0, dur=6, t1=6, lop={'THAT': 6}, that=dict(loai='footage', hien_dai=True, **t))]
case('TU-LIEU-THAT (g)', 'footage hiện đại không khai giay_phep → THIẾU (g)', bad(K7.tu_lieu_that(E4, FT(), TMP), 'g'), True)
case('TU-LIEU-THAT (g)', 'giay_phep {tep, sha256} đúng → sạch', bad(K7.tu_lieu_that(E4, FT(giay_phep=dict(tep=gp, sha256=gsha)), TMP)), False)
case('TU-LIEU-THAT (g)', 'giay_phep SHA sai → (g)', bad(K7.tu_lieu_that(E4, FT(giay_phep=dict(tep=gp, sha256='0' * 64)), TMP), 'g'), True)
case('TU-LIEU-THAT (a)', 'ảnh thật khai ai_image → (a)', bad(K7.tu_lieu_that(E4, [dict(shot='p', t0=0, dur=6, lop={'THAT': 6}, that={}, ai_image=True)], TMP), 'a'), True)
case('TU-LIEU-THAT', 'không có THAT → KHÔNG ÁP', [] if K7.tu_lieu_that(E4, LT).get('ket_qua') == 'KHÔNG ÁP' else ['áp'], False)
c_t = cap112.cap('TU-LIEU-THAT', dict(loi=[], thieu=['(g) f: thiếu giấy phép'], cong='G2'))
case('cấp TU-LIEU-THAT', '(g) thiếu giấy phép ở G2 → Chặn', c_t[1], True)
case('MAY-19 THAT', 'shot ảnh thật (THAT) không đòi cu_may/log máy → (g) sạch', [x for x in bad(K74.may19(E4, None, [dict(shot='p', t0=0, dur=6, lop={'THAT': 6}, that={})], '.', 'G2'), 'g')], False)

# ====================================================================== K-LAI-1 theo Q2 (C11)
LK = [dict(shot='m1', t0=0, dur=25, t1=25, minh_hoa=True, ai_image=True), dict(shot='b', t0=25, dur=75, t1=100, goc='cao')]
case('K-LAI-1 T4', 'minh hoạ M-d 25 % (không AI khác) → sạch (Q2/C11)', bad(K7.klai1_t4(E4, None, LK)), False)
LK2 = LK + [dict(shot='c', t0=100, dur=30, t1=130, ai_image=True)]
case('K-LAI-1 T4', 'ai_image ngoài M-d 30/130 = 23 % > 20 % → lỗi', bad(K7.klai1_t4(E4, None, LK2)), True)
DS, SH, _ = LA.log_ai(LK)
case('K-LAI-1 T3 (q_lai không đổi)', 'T3: cùng log, M-d 25 % > 20 % → vẫn lỗi (klai1_log)', bad(LA.klai1_log(DS, SH, 100.0, 'thử')), True)

# ====================================================================== TL-1 (c) P9: miễn ranh M-d / tư liệu
LM = [dict(shot='a', t0=0, dur=20, t1=20, goc='cao', tl=True), dict(shot='m', t0=20, dur=6, t1=26, minh_hoa=True, goc='md'),
      dict(shot='b', t0=26, dur=14, t1=40, goc='cao', tl=True, tu_lieu_lan=[dict(t0=30, t1=34, lop='TL')]), dict(shot='p', t0=40, dur=5, t1=45, lop={'THAT': 5}, that={}, goc='phang'),
      dict(shot='c', t0=45, dur=15, t1=60, goc='cao', tl=True)]
rm = K7.ranh_mien(LM)
case('TL-1 (c) ranh', 'ranh miễn = vào/ra M-d (20, 26) + tư liệu có giờ (30, 34) + THAT (40, 45)', [] if rm == [20.0, 26.0, 30.0, 34.0, 40.0, 45.0] else [rm], False)
CV = [5.0, 10.0, 15.0, 20.1, 26.2, 30.0, 34.1, 40.0, 45.3, 50.0, 55.0]   # 11 cắt / 1 phút
_cv, _dv = K6.cuts_video, K6.drift_video
K6.cuts_video = lambda F, fps, S=None: list(CV); K6.drift_video = lambda F, fps, a, b, cv: (None, 0)
EM = dict(E4, **ep_seg(LM)); EM3 = dict(E3, **ep_seg(LM))
try:
    r4 = K6.tl1(EM, None, LM, VF=(np.zeros((1440, 4, 4), np.uint8), 24.0)); r3 = K6.tl1(EM3, None, LM, VF=(np.zeros((1440, 4, 4), np.uint8), 24.0))
finally: K6.cuts_video, K6.drift_video = _cv, _dv
cv4 = r4.get('cat_video') or {}
case('TL-1 (c) T4', '11 cắt/phút − 6 ranh M-d/tư liệu/ảnh thật = 5/phút → (c) sạch; in trước/sau', bad(r4, 'c') + ([] if cv4.get('mien_md_tl') == 6 and cv4.get('cpm_truoc_mien') == 11.0 else [cv4]), False)
case('TL-1 (c) T3', 'T3 (không hồi tố): 11 cắt/phút → (c)', bad(r3, 'c'), True)

# ====================================================================== NHAN-VAT-TEN
def mp4(nm, img, n=24):
    p = os.path.join(TMP, nm); im = cv2.imread(img); vw = cv2.VideoWriter(p, cv2.VideoWriter_fourcc(*'mp4v'), 24, (im.shape[1], im.shape[0]))
    for _ in range(n): vw.write(im)
    vw.release(); return p


cd = os.path.join(TMP, 'chan-dung.png'); cv2.imwrite(cd, np.full((64, 64, 3), 128, np.uint8)); cds = hashlib.sha256(open(cd, 'rb').read()).hexdigest()
MD = lambda clip, **kw: [dict(shot='m', t0=0, dur=1, t1=1, minh_hoa=[dict(ma='m', t0=0, t1=1, clip=clip, nhan_vat_ten='Robert Hooke',
                                                                       chan_dung_tham_chieu=dict(tep=cd, sha256=cds), duyet_chu_du_an='AUTHORSHIP 25/10 10:00', **kw)])]
can, xa = mp4('can.mp4', os.path.join(FX, 'mat-can.jpg')), mp4('xa.mp4', os.path.join(FX, 'mat-xa.jpg'))
case('NHAN-VAT-TEN (a)', 'mặt 0,236 khung > 1/8 → (a) cận mặt', bad(K7.nhan_vat_ten(E4, None, MD(can), TMP), 'a'), True)
case('NHAN-VAT-TEN (a)', 'mặt ≤ 0,093 khung → sạch', bad(K7.nhan_vat_ten(E4, None, MD(xa), TMP)), False)
mdu = MD(xa); mdu[0]['minh_hoa'][0].pop('duyet_chu_du_an')
case('NHAN-VAT-TEN (u)', 'thiếu duyet_chu_du_an → THIẾU (u)', bad(K7.nhan_vat_ten(E4, None, mdu, TMP), 'u'), True)
mdk = MD(xa); mdk[0]['minh_hoa'][0]['chan_dung_tham_chieu'] = dict(tep=cd, sha256='1' * 64)
case('NHAN-VAT-TEN (k)', 'chân dung tham chiếu SHA sai → (k)', bad(K7.nhan_vat_ten(E4, None, mdk, TMP), 'k'), True)
case('NHAN-VAT-TEN (m)', 'không clip, không master → THIẾU (m)', bad(K7.nhan_vat_ten(E4, None, MD(None), TMP), 'm'), True)
case('cấp NHAN-VAT-TEN', '(a) ở animatic → Cảnh báo (không Chặn)', cap112.cap('NHAN-VAT-TEN', dict(loi=['(a) x'], cong='animatic'))[1], False)
case('cấp NHAN-VAT-TEN', '(a) ở G2 → Chặn', cap112.cap('NHAN-VAT-TEN', dict(loi=['(a) x'], cong='G2'))[1], True)

# ====================================================================== KIEM-2-MUC
t1 = os.path.join(TMP, 't1.json'); json.dump(dict(tang=1, ket_luan='ĐẠT-T1'), open(t1, 'w'))
tk = os.path.join(TMP, 'to.jpg'); cv2.imwrite(tk, np.zeros((8, 8, 3), np.uint8))
def t2(pv):
    p = os.path.join(TMP, f't2-{abs(hash(pv)) % 999}.json')
    json.dump(dict(ket_luan_may=dict(ket_qua='ĐẠT'), khung=[dict(u=u, q_thoi_dai=dict(khung=[dict(prompt_ver=pv)])) for u in (0.25, 0.55, 0.9)]), open(p, 'w')); return p
KM = lambda **kw: [dict(shot='m', t0=0, dur=6, t1=6, minh_hoa=[dict(ma='m', t0=0, t1=6, kiem_t1=t1, **kw)])]
case('KIEM-2-MUC áp dụng', 'không khai kiem_2_muc / muc_kiem → KHÔNG ÁP (giữ hành vi cũ)', [] if K7.kiem_2_muc(E4, KM(), TMP).get('ket_qua') == 'KHÔNG ÁP' else ['áp'], False)
case('KIEM-2-MUC (a)', 'nen + nhân vật có tên → (a) bắt buộc day_du', bad(K7.kiem_2_muc(E4, KM(muc_kiem='nen', so_luot=1, to_khung=tk, nhan_vat_ten='Hooke'), TMP), 'a'), True)
case('KIEM-2-MUC nen', 'nen: Flash ĐẠT + tờ khung, 2 lượt → sạch', bad(K7.kiem_2_muc(E4, KM(muc_kiem='nen', so_luot=2, to_khung=tk), TMP)), False)
case('KIEM-2-MUC (c)', 'nen 3 lượt > 2 → (c)', bad(K7.kiem_2_muc(E4, KM(muc_kiem='nen', so_luot=3, to_khung=tk), TMP), 'c'), True)
case('KIEM-2-MUC (b)', 'nen thiếu tờ khung → (b)', bad(K7.kiem_2_muc(E4, KM(muc_kiem='nen', so_luot=1), TMP), 'b'), True)
case('KIEM-2-MUC day_du', 'day_du: 2 tầng + q_thoi_dai lớp mốc, công trình mốc, 3 lượt → sạch',
     bad(K7.kiem_2_muc(E4, KM(muc_kiem='day_du', so_luot=3, kiem=t2(QT.PROMPT_VER_MOC), cong_trinh_moc=["St Paul's dome"]), TMP)), False)
case('KIEM-2-MUC (d)', 'công trình mốc nhưng q_thoi_dai đề bài cũ → (d)', bad(K7.kiem_2_muc(E4, KM(muc_kiem='day_du', so_luot=1, kiem=t2(QT.PROMPT_VER), chan_troi_city=True), TMP), 'd'), True)
case('KIEM-2-MUC (c)', 'day_du 4 lượt > 3 → (c)', bad(K7.kiem_2_muc(E4, KM(muc_kiem='day_du', so_luot=4, kiem=t2(QT.PROMPT_VER)), TMP), 'c'), True)
case('KIEM-2-MUC (c) tag', 'không khai so_luot, tag lượt chọn "m-l3-360p" ở mức nen → (c) (cận dưới 3 > 2)', bad(K7.kiem_2_muc(E4, KM(muc_kiem='nen', luot='m-l3-360p', to_khung=tk), TMP), 'c'), True)
case('KIEM-2-MUC (c) tag', 'không khai so_luot, tag "m-l2-360p" mức nen → sạch', bad(K7.kiem_2_muc(E4, KM(muc_kiem='nen', luot='m-l2-360p', to_khung=tk), TMP)), False)
case('KIEM-2-MUC (k)', 'kiem_2_muc: true mà đoạn không khai muc_kiem → (k)', bad(K7.kiem_2_muc(dict(E4, kiem_2_muc=True), KM(), TMP), 'k'), True)

# ====================================================================== q_thoi_dai lớp công trình mốc
d0 = '/x'; old = QT.PROMPT.format(nam=1711, noi=' at London', d=d0, tiles=QT.prompt_for(d0, 1711, 'London').split('(16:9)\n')[1].split('\n\nCheck')[0],
                                  muc='\n'.join(f'{i + 1}. {k} — {v.format(nam=1711)}' for i, (k, v) in enumerate(QT.MUC)))
case('q_thoi_dai mặc định', 'moc None → đề bài 1.15 giống hệt từng chữ + khoá bộ đệm cũ', [] if (QT.prompt_for(d0, 1711, 'London') == old and QT._khoa('h', 1711, 'L') == hashlib.sha256(f'h|1711|L|{QT.PROMPT_VER}|{QT.MODEL}'.encode()).hexdigest()[:32]) else ['khác'], False)
pm = QT.prompt_for(d0, 1711, 'London', ["St Paul's dome"])
case('q_thoi_dai lớp mốc', 'moc → thêm mục 9 cong_trinh_moc + danh sách + khoá khác', [] if ('9. cong_trinh_moc' in pm and "St Paul's dome" in pm and '"cong_trinh_moc"]' in pm and QT._khoa('h', 1711, 'L', ['a']) != QT._khoa('h', 1711, 'L')) else ['thiếu'], False)
case('q_thoi_dai _chuan', 'mục cong_trinh_moc chỉ nhận khi bật lớp mốc', [] if (QT._chuan(dict(nghi_van=[dict(muc='cong_trinh_moc', do_tin=0.9)]))[0][0]['muc'].startswith('khác:')
                                                                          and QT._chuan(dict(nghi_van=[dict(muc='cong_trinh_moc', do_tin=0.9)]), True)[0][0]['muc'] == 'cong_trinh_moc') else ['sai'], False)
ANH = os.path.join(TMP, 'k.png'); cv2.imwrite(ANH, np.full((360, 640, 3), 120, np.uint8)); goi = []


def gia_call(p, d, cap):
    goi.append(p[:40]); reads = [os.path.join(d, f) for f in ('full.jpg', 'o1.jpg', 'o2.jpg', 'o3.jpg', 'o4.jpg')]
    rep = dict(nam=1711, nghi_van=[dict(muc='cong_trinh_moc', mo_ta="no Wren dome", ly_do='dome completed 1710', nam_xuat_hien=None, toa_do=[0.3, 0.1, 0.8, 0.4], do_tin=0.8)])
    return dict(result=json.dumps(rep), cost_usd=0.0, model_usage={QT.MODEL: {}}, reads=reads, is_error=False, error=None, transcript='', secs=0.0)


_jc = QT.judge.call; QT.judge.call = gia_call
try: kq = QT.soi_khung(ANH, 1711, TMP, 'moc', 'London', api=True, cache=None, moc=["St Paul's dome"])
finally: QT.judge.call = _jc
case('q_thoi_dai lớp mốc', 'nghi vấn cong_trinh_moc (tin 0,8) giữ, KHÔNG gọi bước 2 (1 lần gọi)', [] if (len(kq['nghi_van']) == 1 and len(goi) == 1 and kq['prompt_ver'] == QT.PROMPT_VER_MOC) else [len(kq['nghi_van']), len(goi)], False)

# ====================================================================== MAY-19 (A1, A2)
ref = logm('M03', P1p, P1l, dp=(40, -23, -71))   # DAY: máy tiến 80 m
k_ok = logm('K1', P1p, P1l); k_bad = logm('K2', (P1p[0] + 5, P1p[1], P1p[2]), P1l)
EN = lambda x: [x[0] + 532000, -x[2] + 180800, x[1]]   # hệ cảnh → [E, N, h]
neo = [532118, 181150, 111]
LSk = lambda lg, **kw: [dict(shot='M03', t0=0, dur=2, t1=2, chuong='MÓC', cu_may='DAY', log_may=ref, tieu_diem_en=neo, goc='cao', tl=True),
                        dict(shot='K', t0=2, dur=2, t1=4, chuong='MÓC', cu_may='KHOP', khop_voi='M03', log_may=lg, goc='cao', tl=True, **kw)]
mk = K74.may19(E4, None, LSk(k_ok, diem_neo_en=neo), TMP, 'G2')
case('MAY-19 (c) A2', 'KHOP về khung ĐẦU của shot DAY (đúng khung) → (c) sạch [1.17.6: so khung cuối → trượt]', bad(mk, 'c'), False)
case('MAY-19 (c) A2', 'KHOP lệch máy 5 m so mọi khung shot tham chiếu → (c)', bad(K74.may19(E4, None, LSk(k_bad, diem_neo_en=neo), TMP, 'G2'), 'c'), True)
mk2 = K74.may19(E4, None, LSk(k_ok, diem_neo=neo), TMP, 'G2')
case('MAY-19 A1', 'diem_neo khai [E, N, h] trong trường hệ cảnh → đổi theo goc_toa_do + (w)', bad(mk2, 'w') if not bad(mk2, 'c') else bad(mk2, 'c'), True)
case('MAY-19 A1', 'diem_neo [E, N, h] sau đổi: (c) sạch', bad(mk2, 'c'), False)
J = json.load(open(k_ok)); J['toa_do'] = 'EN'
for fr in J['frames']: fr['cam'] = dict(fr['cam'], p=EN(fr['cam']['p']), l=EN(fr['cam']['l']))
k_en = os.path.join(TMP, 'K1-en.json'); json.dump(J, open(k_en, 'w'))
mk3 = K74.may19(E4, None, LSk(k_en, diem_neo_en=neo), TMP, 'G2')
case('MAY-19 A1', 'log khai toa_do: EN ([E, N, h]) = cùng số đo như log hệ cảnh', [] if (mk3['do']['K']['khop_px'] == mk['do']['K']['khop_px'] and mk3['do']['K']['td'] == mk['do']['K']['td']) else [mk3['do']['K'], mk['do']['K']], False)
J2 = json.load(open(k_ok)); J2['frames'] = [dict(f=fr['f'], cam_en=dict(fr['cam'], p=EN(fr['cam']['p']), l=EN(fr['cam']['l']))) for fr in J2['frames']]
k_ce = os.path.join(TMP, 'K1-camen.json'); json.dump(J2, open(k_ce, 'w'))
case('MAY-19 A1', 'log chỉ có cam_en → đổi, (c) sạch', bad(K74.may19(E4, None, LSk(k_ce, diem_neo_en=neo), TMP, 'G2'), 'c', 'g'), False)
case('MAY-19 A2 khop_khung', 'ghim khop_khung: cuoi (khung cuối DAY) → (c)', bad(K74.may19(E4, None, LSk(k_ok, diem_neo_en=neo, khop_khung='cuoi'), TMP, 'G2'), 'c'), True)

# ====================================================================== Q37 (a) A4 — p.lop_chong
EQ = lambda lc: dict(id='q', segments=[dict(id='H1', dur=10, shots=[dict(at=0, type='scene3d', p=dict(lop_chong=lc) if lc is not None else {})],
                                             beats=[dict(t=0, k='cut', s='H1'), dict(t=1.45, k='the_nhan_vat', s='Hooke')])])
case('Q37 (a) A4', 'beat thẻ nhân vật 1,45 s, đặc tả không có lớp chồng → (a) như cũ', bad(QN.q37(EQ(None)), 'a'), True)
case('Q37 (a) A4', 'p.lop_chong [{at 1,0, mo_vao_s 0,45}] → mốc 1,0 / 1,45 → (a) sạch', bad(QN.q37(EQ([dict(at=1.0, k='the_nhan_vat', s='Hooke', mo_vao_s=0.45)])), 'a'), False)
case('Q37 spec_times', 'đặc tả không lop_chong → spec_times giống hệt (T3)', [] if QN.spec_times({}, [dict(at=0, p={})], 10) == [0.0] else ['khác'], False)

# ====================================================================== N2P A5
rn = NP.check(dict(E4, out=TMP), None, TMP, [dict(shot='M01', ai_nen=True, n2p=dict(tam=[dict(tag='x', kiem='k.json')]))])
case('N2P A5', 'log shot có n2p.tam → THIẾU chỉ khuôn episode.yaml n2p.tam {id, shot, render, ghep, mat_na, nam}', [x for x in bad(rn['N2P-1']) if 'episode.yaml' in x and 'mat_na' in x] and ['ok'] or [], True)


# ====================================================================== BMN (d) D6 — sàn Y nhấp nháy
def dung(n, y0, y1, nhieu=0.0, seed=0):
    rng = np.random.default_rng(seed); C, Rr = [], []
    I = np.zeros((40, 60), np.int32); I[5:35, 5:55] = 7
    for t in range(n):
        y = y0 + (y1 - y0) * t / (n - 1); v = np.clip((255 * y) + rng.normal(0, nhieu, (40, 60)), 0, 255)
        Rr.append(np.repeat(np.full((40, 60), 255 * y)[..., None], 3, -1).round().astype(np.uint8)); C.append(np.repeat(v[..., None], 3, -1).round().astype(np.uint8))
    return C, Rr, I


Cn, Rn, In = dung(24, 0.6, 0.03, nhieu=0.5, seed=1)   # nắng tắt về gần đen (mã 153 → 8), nhiễu mã hoá σ 0,5 mã + lượng tử 8 bit
case('BMN (d) D6', 'sàn 0 = thước 1.17.6 (giống hệt q_k1175.quy_dao)', [] if K76.nhap_nhay_san(Cn, Rn, In, 0.0) == K75.quy_dao(Cn, Rn, In)['nhap_be_mat'] else [K76.nhap_nhay_san(Cn, Rn, In, 0.0), K75.quy_dao(Cn, Rn, In)['nhap_be_mat']], False)
case('BMN (d) D6', 'nắng tắt gần đen, không sàn → nhấp nháy > 0,012 (trượt oan)', [K76.nhap_nhay_san(Cn, Rn, In, 0.0)] if K76.nhap_nhay_san(Cn, Rn, In, 0.0) > 0.012 else [], True)
case('BMN (d) D6', 'cùng cảnh, sàn Y 0,01 → ≤ 0,012 (đạt)', [K76.nhap_nhay_san(Cn, Rn, In, 0.01)] if K76.nhap_nhay_san(Cn, Rn, In, 0.01) > 0.012 else [], False)
Cb, Rb, Ib = dung(24, 0.5, 0.45, nhieu=8.0, seed=2)
case('BMN (d) D6', 'bề mặt sáng nhiễu 8 mã/khung, sàn 0,01 → vẫn > 0,012 (trượt)', [K76.nhap_nhay_san(Cb, Rb, Ib, 0.01)] if K76.nhap_nhay_san(Cb, Rb, Ib, 0.01) > 0.012 else [], True)
case('BMN (d) D6 tham số', 'không khai be_mat_nha_y_san_nhap → 0 (như 1.17.6); khai 0,01 → 0,01', [] if (K76.y_san_nhap(E4) == 0.0 and K76.y_san_nhap(dict(E4, be_mat_nha_y_san_nhap=0.01)) == 0.01
                                                                                                   and K76.y_san_nhap(dict(E4, n2p=dict(be_mat_nha_y_san_nhap=0.01))) == 0.01) else ['sai'], False)

# ====================================================================== cấp + áp dụng
case('cấp GOC-CAO', '(c) ở G2 → Chặn', cap112.cap('GOC-CAO', dict(loi=['(c) x'], cong='G2'))[1], True)
case('cấp GOC-CAO', '(w) ở G2 → chỉ Cảnh báo', cap112.cap('GOC-CAO', dict(loi=['(w) x'], cong='G2'))[1], False)
case('cấp GOC-CAO', '(a) ở animatic → Cảnh báo', cap112.cap('GOC-CAO', dict(loi=['(a) x'], cong='animatic'))[1], False)
case('cấp KIEM-2-MUC', '(b) ở G2 → Chặn', cap112.cap('KIEM-2-MUC', dict(loi=['(b) x'], cong='G2'))[1], True)
case('áp dụng', 'T3: q_k1174.check toàn KHÔNG ÁP (gồm hàng 1.17.7)', [k for k, v in K74.check(E3, None, '.', []).items() if v.get('ket_qua') != 'KHÔNG ÁP'], False)

ok = all(x[3] for x in R)
for rule, name, exp, good, got in R: print(('ĐÚNG' if good else 'SAI ') + f' | {rule} | {name} | kỳ vọng {exp}' + ('' if good else f' | được: {got}'))
print(f"\nselftest_k1177: {sum(x[3] for x in R)}/{len(R)} đúng kỳ vọng")
sys.exit(0 if ok else 1)
