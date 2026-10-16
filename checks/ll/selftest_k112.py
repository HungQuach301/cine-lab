#!/opt/cine/bin/python
"""Tự kiểm luật kênh 2 bản 1.12.0 (phiên K, 16/10/2026; 1.12.1, 17/10/2026: KHOP1 dùng khai khung vàng đủ trường, TL-Q2 AGL, TL-Q1c tương phản): ML1–ML3, FT1, BC1, MAU1, KHOP1, TL-Q1…Q6. Mỗi luật ≥ 1 ca ĐẠT + ≥ 1 ca TRƯỢT.
Dữ liệu thật trong fixtures/k112/: lời T2 k2c-t2-01 v3.3 (trước cắt) và v3.4 (sau cắt) có mốc giây; đặc tả + timeline T2 v3.4 dựng lại ngoại tuyến;
câu trả lời chấm ngữ nghĩa ML2 đã lưu (ml2-cache.json, mô hình ghim, gọi thật 16/10); bộ timelapse ams30 (timelapse-rd) và gib20 (v5b1b);
số so hình 12 khung SwiftShader ↔ llvmpipe (gpu-rd). Còn lại tổng hợp trong thư mục tạm. KHÔNG gọi mạng, KHÔNG gọi API.

  /opt/cine/bin/python checks/ll/selftest_k112.py        mã thoát 0 = mọi ca đúng kỳ vọng
"""
import copy, gzip, json, math, os, sys, tempfile

import cv2
import numpy as np
import yaml

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, ROOT)
from checks.ll import q_mach as QM, q_ftg as QF, q_hinh as QH, q_tl as QT  # noqa: E402

FX = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures', 'k112')
TMP = tempfile.mkdtemp(prefix='k112-')
R = []


def case(rule, name, got, expect_fail):
    got = list(got) if got else []
    R.append((rule, name, 'bắt lỗi' if expect_fail else 'sạch', bool(got) == expect_fail, got[:2]))


def bad(r): return r['loi'] + r.get('thieu', [])


KHAI = yaml.safe_load(open(os.path.join(FX, 't2-mach.yaml')))
V33, V34 = (json.load(open(os.path.join(FX, f't2-v{v}-loi.json'))) for v in ('33', '34'))
CACHE = json.load(open(os.path.join(FX, 'ml2-cache.json')))
E34 = yaml.safe_load(gzip.open(os.path.join(FX, 't2-v34-episode.yaml.gz'))); TL34 = json.load(gzip.open(os.path.join(FX, 't2-v34-timeline.json.gz')))
CL = open(os.path.join(FX, 't2-claim-ids.txt')).read().split()
mm = QM.q_types.mmss

# =============================================================== ML2 lời lặp ý (T2 thật)
r33 = QM.ml2(V33['cau'], V33['tong_s'], KHAI, dict(CACHE))
C33 = V33['cau']
d7 = [p for p in r33['lap'] if 273 <= C33[p['j']]['t0'] <= 305]
d13 = [p for p in r33['lap'] if 620 <= C33[p['j']]['t0'] <= 631 and 148 <= C33[p['i']]['t0'] <= 168]
case('ML2', f"T2 lời v3.3: bắt D7 (vòng 'wages' {', '.join(f'{mm(C33[p['i']]['t0'])}↔{mm(C33[p['j']]['t0'])}' for p in d7)}) và D13 "
     f"(ủng hộ/phản đối {', '.join(f'{mm(C33[p['i']]['t0'])}↔{mm(C33[p['j']]['t0'])}' for p in d13)})", r33['loi'] if d7 and d13 else [], True)
r34 = QM.ml2(V34['cau'], V34['tong_s'], KHAI, dict(CACHE))
C34 = V34['cau']
still = [p for p in r34['lap'] if 270 <= C34[p['j']]['t0'] <= 300 or 595 <= C34[p['j']]['t0'] <= 612]
case('ML2', f"T2 lời v3.4 (sau cắt D7, D13): {r34['val']}", bad(r34) + [f'còn {len(still)} chỗ D7/D13'] * bool(still), False)
r = QM.ml2(V34['cau'], V34['tong_s'], KHAI, {})
case('ML2', 'không có câu trả lời ngữ nghĩa đã lưu và không --api → THIẾU (không ĐẠT)', bad(r) if r['ket_qua'] == 'THIẾU' else [], True)
K2 = copy.deepcopy(KHAI); K2.pop('tom_tat')
r = QM.ml2(V34['cau'], V34['tong_s'], K2, dict(CACHE))
case('ML2', f"v3.4 không khai tóm tắt cuối → cặp có câu tóm tắt (vd 1943 ↔ 9:34.7) thành ứng viên chưa chấm: {r['val']}", r['thieu'], True)
K3 = copy.deepcopy(KHAI); K3['tom_tat'] = dict(tu="In 1944, the Liberty program", den="Since the 1980s, it has built few")
r = QM.ml2(V34['cau'], V34['tong_s'], K3, dict(CACHE))
case('ML2', 'khai tóm tắt dài 8 phút (từ chương 02) → lỗi khai, không miễn', [x for x in r['loi'] if x.startswith('tom_tat')], True)
CA = [dict(i=0, seg='00', t0=1, t1=4, s='The port moved forty ships a day in 1950.'), dict(i=1, seg='00', t0=5, t1=8, s='Then the cranes arrived.'),
      dict(i=2, seg='00', t0=9, t1=12, s='Workers retrained for new jobs.'), dict(i=3, seg='00', t0=40, t1=44, s='In 1950, the port moved forty ships a day.')]
p = QM.ung_vien(CA)[0]
case('ML2', f"tầng n-gram: cùng câu đảo trật tự cách 36 s → ứng viên (điểm {p[0]['diem'] if p else 0})", [f'{x["i"]}↔{x["j"]}' for x in p if x['i'] == 0 and x['j'] == 3], True)
case('ML2', 'tầng n-gram: hai câu liền nhau không bao giờ là ứng viên', [f'{x["i"]}↔{x["j"]}' for x in QM.ung_vien(CA[:2] + CA[1:2])[0]], False)

# =============================================================== ML3 lời mời đăng ký (T2 thật)
TL33 = dict(tong_s=V33['tong_s'], segments=V33['segments']); TL34l = dict(tong_s=V34['tong_s'], segments=V34['segments'])
r = QM.ml3(V33['cau'], TL33, KHAI)
case('ML3', f"T2 v3.3: mời đăng ký 3:18.6 (±5 s ranh chương 3:23.3) nhưng kết thúc 1,8 s trước luận điểm chính C22 → TRƯỢT", r['muc']['b'] if not r['muc']['a'] else ['sai mục'], True)
r = QM.ml3(V34['cau'], TL34l, KHAI)
case('ML3', f"T2 v3.4: {r['val']} → ĐẠT", bad(r), False)
CS = lambda t0: [dict(i=0, seg='00', t0=1.0, t1=5.0, s='Ships matter.'), dict(i=1, seg='01', t0=t0, t1=t0 + 4, s='If this helps, subscribe for the next one.'),
                 dict(i=2, seg='01', t0=t0 + 30, t1=t0 + 34, s='Here is the main claim of the film.')]
TLs = dict(tong_s=300.0, segments=[dict(id='00', t0=0, t1=100), dict(id='01', t0=100, t1=300)])
KS = dict(luan_diem_chinh=[dict(claim='C1', cau='Here is the main claim')])
case('ML3', 'mời đăng ký 2:30 giữa chương (cách ranh 50 s, ngoài 60 s cuối) → (a)', QM.ml3(CS(150.0), TLs, KS)['muc']['a'], True)
case('ML3', 'mời đăng ký 1:37–1:41 quanh ranh chương 1:40 (±5 s), luận điểm chính sau 30 s → đạt', bad(QM.ml3(CS(97.0), TLs, KS)), False)
case('ML3', 'mời đăng ký 4:20 (60 s cuối) → đạt', bad(QM.ml3(CS(260.0), TLs, KS)), False)
r = QM.ml3(CS(97.0), TLs, {})
case('ML3', 'có câu mời mà không khai luan_diem_chinh → THIẾU', r['thieu'] if r['ket_qua'] == 'THIẾU' else [], True)

# =============================================================== ML1 mạch truyện (T2 thật + tổng hợp)
r = QM.ml1(E34, TL34, V34['cau'], claims=CL)
case('ML1', f"T2 v3.4 (làm trước luật): {r['val']}; 7 shot mở đoạn `at: 0` không gắn → (a)", r['muc']['a'], True)
E2 = copy.deepcopy(E34)
for sg in E2['segments']:
    first = next(c for c in V34['cau'] if c['seg'] == sg['id'])
    sg['shots'][0]['cau'] = first['s'][:30]
r = QM.ml1(E2, TL34, V34['cau'], claims=CL)
case('ML1', f"T2 v3.4 + khai `cau` cho 7 shot mở đoạn → {r['val']}", bad(r), False)
E3 = copy.deepcopy(E2); E3['segments'][2]['shots'][0]['cau'] = 'A sentence that is not in the narration'
case('ML1', '`cau` không khớp câu nào → (c)', QM.ml1(E3, TL34, V34['cau'], claims=CL)['muc']['c'], True)
E3 = copy.deepcopy(E2); E3['segments'][2]['shots'][0].pop('cau'); E3['segments'][2]['shots'][0]['claim'] = 'C99'
case('ML1', 'claim C99 không có trong claims.md T2 → (c)', QM.ml1(E3, TL34, V34['cau'], claims=CL)['muc']['c'], True)
E3['segments'][2]['shots'][0]['claim'] = 'C20'
case('ML1', 'claim C20 có trong claims.md → đạt', bad(QM.ml1(E3, TL34, V34['cau'], claims=CL)), False)


def tlfilm(troi_s, T=100.0):
    sh = [dict(tpl='plate', t0=0, t1=troi_s, p={}), dict(tpl='plate', t0=troi_s, t1=T, p={})]
    TL = dict(tong_s=T, heroes={}, segments=[dict(id='00', t0=0, t1=T, shots=sh)])
    E = dict(id='k2x', segments=[dict(id='00', shots=[dict(tpl='plate', type='timelapse', tl=True), dict(tpl='plate', type='timelapse', claim='C1')])])
    return QM.ml1(E, TL, [], claims=['C1'])


r = tlfilm(10.0); case('ML1', f"timelapse trôi 10 s / 100 s = {r['tl_troi_pct']} % → đạt", bad(r), False)
r = tlfilm(15.0); case('ML1', f"timelapse trôi 15 s / 100 s = 15,0 % (đúng trần) → đạt, nêu sát ngưỡng", [] if r['ok'] and r['sat_nguong'] else ['không nêu sát ngưỡng'], False)
r = tlfilm(20.0); case('ML1', f"timelapse trôi 20 s / 100 s = {r['tl_troi_pct']} % > 15 % → (b)", r['muc']['b'], True)

# =============================================================== FT1 chỉ báo footage (T2 thật + tổng hợp)
r = QF.ft1(E34, TL34)
case('FT1', f"T2 v3.4: {r['val']} → (b) chưa khai lý do", r['muc']['b'] if not r['muc']['a'] else ['sai mục'], True)
E2 = copy.deepcopy(E34)
for sg in E2['segments']:
    for s in sg['shots']:
        if (s.get('type') or (s.get('p') or {}).get('type')) in QF.LOAI: s['ly_do_hinh'] = 'bang_chung'
r = QF.ft1(E2, TL34); case('FT1', f"T2 v3.4 + khai ly_do_hinh → {r['pct']} % ≤ 20 % đạt", bad(r), False)


def ftfilm(ty, d, ti=None, T=100.0):
    p = {'ti_le_khung': ti} if ti is not None else {}
    TL = dict(tong_s=T, heroes={}, segments=[dict(id='00', t0=0, t1=T, shots=[dict(tpl='plate', t0=0, t1=d, p=p), dict(tpl='plate', t0=d, t1=T, p={})])])
    E = dict(id='k2x', segments=[dict(id='00', shots=[dict(tpl='plate', type=ty, ly_do_hinh='con_nguoi'), dict(tpl='plate', type='scene3d')])])
    return QF.ft1(E, TL)


case('FT1', 'footage 25 s / 100 s → (a) > 20 %', ftfilm('footage', 25.0)['muc']['a'], True)
r = ftfilm('photo', 5.0, ti=0.30); case('FT1', f"ảnh chú thích 0,30 khung, 5 s → không tính (miễn {r['mien_s']} s)", bad(r) if r['mien_s'] == 5.0 else ['không miễn'], False)
r = ftfilm('photo', 7.0, ti=0.30); case('FT1', 'ảnh 0,30 khung nhưng 7 s > 6 s → tính', [] if r['giay'] == 7.0 else ['miễn sai'], False)
r = ftfilm('photo', 25.0, ti=0.5); case('FT1', 'ảnh nửa khung 25 s → tính, (a)', r['muc']['a'], True)

# =============================================================== BC1 bố cục (tổng hợp + v5b1b thật)
def mask(lo_from, lo_to, n=240, hero=None):
    return [dict(f=f, content_pct=20.0 if lo_from <= f < lo_to else 45.0, **({'hero_pct': hero} if hero is not None else {})) for f in range(n)]


case('BC1', 'nội dung 20 % liên tục 72 khung (3,0 s) → (a)', QH.bc1(mask(24, 96))['loi'], True)
case('BC1', 'nội dung 20 % liên tục 48 khung (2,0 s, đúng trần) → đạt', bad(QH.bc1(mask(24, 72))), False)
case('BC1', 'nội dung 20 % 3,0 s nằm trong mốc đinh → miễn, đạt', bad(QH.bc1(mask(24, 96), moc=[(20, 100)])), False)
case('BC1', 'shot cận hero, hero trung vị 20 % → (b)', QH.bc1(mask(0, 0, hero=20.0), hero=[(0, 47)])['loi'], True)
case('BC1', 'shot cận hero, hero trung vị 30 % → đạt', bad(QH.bc1(mask(0, 0, hero=30.0), hero=[(0, 47)])), False)
mv = json.load(open(os.path.join(FX, 'tl-gib20', 'noi-dung-mask.json')))
r = QH.bc1(mv, n=480, moc=[(291, 336)], hero=[(160, 175)])
case('BC1', f"gib20 (v5b1b): mặt nạ 10/480 khung → không đo được quãng liên tục, hero_pct không có → THIẾU ({r['val']})", r['thieu'] if r['ket_qua'] == 'THIẾU' else [], True)

# =============================================================== MAU1 màu/chi tiết (ảnh tổng hợp)
rng = np.random.default_rng(7)


def img(name, kind):
    y, x = np.mgrid[0:720, 0:1280]
    if kind == 'tot':
        b = np.stack([110 + 80 * np.sin(x / 37.0), 120 + 70 * np.sin(y / 23.0 + 1), 90 + 90 * np.cos((x + y) / 51.0)], -1)
        b[..., 2] = np.clip(b[..., 2] * 1.4, 0, 255); b[..., 0] *= 0.55
        im = np.clip(b + rng.normal(0, 18, b.shape), 0, 245)
    elif kind == 'xam': im = np.full((720, 1280, 3), 128.0) + rng.normal(0, 1.5, (720, 1280, 3))
    elif kind == 'chay':
        im = img(None, 'tot'); im[:40, :] = 255
    if name is None: return im
    p = os.path.join(TMP, name + '.png'); cv2.imwrite(p, np.clip(im, 0, 255).astype(np.uint8)); return p


ptot = img('tot', 'tot'); m = QH.measure(ptot)
case('MAU1', f"khung nhiều màu/chi tiết: bão hoà {m['sat_med']} · colorfulness {m['colorful']} · chi tiết {m['detail']} · cháy {m['clip_pct']} % → đạt", bad(QH.mau1([('s1', ptot)])), False)
case('MAU1', 'khung xám phẳng → trượt bão hoà/colorfulness/chi tiết', QH.mau1([('s2', img('xam', 'xam'))])['loi'], True)
pch = img('chay', 'chay')
case('MAU1', f"cùng khung + dải trắng 40 px (cháy {QH.measure(pch)['clip_pct']} % cả khung) → trượt cháy sáng", QH.mau1([('s3', pch)])['loi'], True)
case('MAU1', 'khung có chữ (co_chu) → THIẾU, không ĐẠT', QH.mau1([('s1', ptot)], co_chu=True)['thieu'], True)

# =============================================================== KHOP1 đổi trình dựng (tổng hợp + số gpu-rd)
G, N = os.path.join(TMP, 'vang'), os.path.join(TMP, 'moi'); os.makedirs(G); os.makedirs(N)
base_im = np.clip(img(None, 'tot'), 0, 255).astype(np.uint8)


def pair(name, f):
    cv2.imwrite(os.path.join(G, name), base_im); cv2.imwrite(os.path.join(N, name), np.clip(f(base_im.astype(np.float64)), 0, 255).astype(np.uint8))


RSS, RLV = 'ANGLE (Google, Vulkan 1.3.0 (SwiftShader Device (Subzero) (0x0000C0DE)), SwiftShader driver)', 'ANGLE (Mesa, llvmpipe (LLVM 20.1.2 256 bits), OpenGL ES 3.2)'


def khai(rg=RSS, rn=RLV, gl=None):
    """1.12.1 (MM4): khai khung vàng/khung mới đủ trường (renderer, gl, goi_canh, SHA từng khung) sau mỗi lần ghi khung"""
    J = lambda r_, d: dict(renderer=r_, gl=gl or QH.lop_renderer(r_), goi_canh=dict(ten='tổng hợp', sha256='0' * 64),
                           khung={n: QH._sha(os.path.join(d, n)) for n in os.listdir(d) if n.endswith('.png')})
    json.dump(J(rg, G), open(os.path.join(G, 'khung-vang.json'), 'w')); json.dump(J(rn, N), open(os.path.join(N, 'khung-moi.json'), 'w'))


pair('a.png', lambda x: x + rng.normal(0, 2.0, x.shape)); khai()
r = QH.khop1(G, N)
case('KHOP1', f"nhiễu hạt σ 2 (như llvmpipe ↔ SwiftShader): {r['val']}", bad(r), False)
pair('a.png', lambda x: x + 2.0); khai()
case('KHOP1', 'dịch màu đều +2 mức/kênh → (c)', QH.khop1(G, N)['loi'], True)
pair('a.png', lambda x: cv2.GaussianBlur(x, (0, 0), 3)); khai()
case('KHOP1', 'mờ Gauss σ 3 → SSIM < 0,90 (c)', QH.khop1(G, N)['loi'], True)
pair('a.png', lambda x: x + rng.normal(0, 2.0, x.shape)); khai()
os.remove(os.path.join(G, 'khung-vang.json'))
case('KHOP1', 'khung vàng không ghi renderer → (a)', QH.khop1(G, N)['loi'], True)
khai()
lg1, lg2 = os.path.join(TMP, 'l1.json'), os.path.join(TMP, 'l2.json')
json.dump(dict(info=dict(renderer='SwiftShader')), open(lg1, 'w')); json.dump(dict(info=dict(renderer='llvmpipe')), open(lg2, 'w'))
case('KHOP1', 'log dựng của một tập có 2 renderer (SwiftShader + llvmpipe) → (b) trộn trình dựng', QH.khop1(G, N, logs=[lg1, lg2])['loi'], True)
GR = json.load(open(os.path.join(FX, 'gpu-rd-so-hinh-12khung.json')))['frames']
r = QH.khop1_so(GR, renderer_vang='SwiftShader', renderer_moi=['llvmpipe'])
case('KHOP1', f"gpu-rd 12 khung 1080p SwiftShader ↔ llvmpipe (số đã ghi): {r['val']}", bad(r), False)
GR2 = copy.deepcopy(GR); GR2['00280.jpg']['ssim'] = 0.8990
case('KHOP1', 'cùng số, SSIM khung 280 hạ 0,9009 → 0,8990 → (c)', QH.khop1_so(GR2, 'SwiftShader', ['llvmpipe'])['loi'], True)

# =============================================================== TL-Q1…Q6 (ams30, gib20 thật + biến thể)
def bo(name):
    B = json.load(open(os.path.join(FX, name, 'bo-tl.json'))); return B, os.path.join(FX, name)


BA, DA = bo('tl-ams30'); BG, DG = bo('tl-gib20')
RA, RG = QT.check(copy.deepcopy(BA), DA), QT.check(copy.deepcopy(BG), DG)
case('TL-Q1', f"ams30: {RA['TL-Q1']['val']} (a) 1,5–2,0 s, (e) ≥ 1 mốc → đạt (a), (e)", RA['TL-Q1']['muc']['a'] + RA['TL-Q1']['muc']['e'], False)
case('TL-Q1', f"gib20: {RG['TL-Q1']['val']}; chữ năm 139,2/96 px = 1,45×; thẻ 1941 ≥ 3 s, nguồn 38 px → (a), (b), (d) đạt", RG['TL-Q1']['muc']['a'] + RG['TL-Q1']['muc']['b'] + RG['TL-Q1']['muc']['d'], False)
case('TL-Q1', 'ams30/gib20: (c) sáng trong mặt nạ công trình chưa đo → THIẾU (không ĐẠT)', [x for x in RA['TL-Q1']['thieu'] if x.startswith('(c)')], True)
FA = QT._frames(QT._ld(DA, BA['campath']))
F2 = copy.deepcopy(FA)
for f in range(356, 380): F2[f]['year'] = 1655
B2 = dict(copy.deepcopy(BA), campath=F2); r = QT.check(B2, DA)['TL-Q1']
case('TL-Q1', f"ams30 kéo năm dừng 1655 thêm 24 khung → {r['val']} > 2,0 s (a)", r['muc']['a'], True)
F3 = copy.deepcopy(FA)
for f in range(312, 356): F3[f]['year'] = 1655 + (f - 312) * 0.05
r = QT.check(dict(copy.deepcopy(BA), campath=F3), DA)['TL-Q1']
case('TL-Q1', 'ams30 bỏ năm dừng (năm trôi 0,05/khung) → 0 mốc (e)', r['muc']['e'], True)
LG = json.load(open(os.path.join(DG, 'log-chu.json'))); LG2 = copy.deepcopy(LG)
for x in LG2['frames']:
    for t in x['text']:
        if t['role'] == 'year' and 291 <= x['f'] <= 336: t['px1080'] = 110.0
r = QT.check(dict(copy.deepcopy(BG), log_chu=LG2), DG)['TL-Q1']
case('TL-Q1', 'gib20 chữ năm trong mốc chỉ 110/96 px = 1,15× → (b)', r['muc']['b'], True)
case('TL-Q2', f"ams30 bay dọc Damrak: {RA['TL-Q2']['val']}", bad(RA['TL-Q2']), False)
case('TL-Q2', f"gib20 bay dọc WCA: lệch ≤ 4,6 m nhưng cao 273–308 m > 120 m → trượt", RG['TL-Q2']['loi'], True)
B2 = copy.deepcopy(BA); B2['tuyen'][0]['pts'] = [[x + 25.0, y] for x, y in B2['tuyen'][0]['pts']]
case('TL-Q2', 'ams30 dời tuyến 25 m về phía đông → không còn 3 s ≤ 15 m', QT.check(B2, DA)['TL-Q2']['loi'], True)
B2 = copy.deepcopy(BA); B2['tuyen'][0]['nguon'] = ''
case('TL-Q2', 'ams30 tuyến không ghi nguồn hình học → trượt', QT.check(B2, DA)['TL-Q2']['loi'], True)
case('TL-Q3', f"ams30: {RA['TL-Q3']['val']}", bad(RA['TL-Q3']), False)
case('TL-Q3', f"gib20: {RG['TL-Q3']['val']}", bad(RG['TL-Q3']), False)
B2 = copy.deepcopy(BA); B2['reveal'] = [dict(t=[20.6, 24.0], dich=[-104, 20, -11], kieu='keo_lui')]
case('TL-Q3', 'ams30 kéo lùi đo từ 20,6 s (số render-log.json E3: 1 505 → 3 947 m) = ×2,6 < 5×', QT.check(B2, DA)['TL-Q3']['loi'], True)
F4 = copy.deepcopy(FA); F4[400]['pos'] = [F4[400]['pos'][0] + 800, F4[400]['pos'][1], F4[400]['pos'][2]]
case('TL-Q3', 'ams30 chèn một khung nhảy máy 800 m giữa kéo lùi → cắt', [x for x in QT.check(dict(copy.deepcopy(BA), campath=F4), DA)['TL-Q3']['loi'] if 'cắt' in x], True)
case('TL-Q4', 'ams30: RIGHTS.md (timelapse-rd) không có dòng ảnh RP-F-00-568 → (a)', [x for x in RA['TL-Q4']['loi'] if x.startswith('(a)')], True)
case('TL-Q4', 'ams30 then/now: 7 điểm, RMS 0,52 % rộng ảnh, máy yên ≥ 0,8 s, hoà 0,8 s → (c) không lỗi đo', [x for x in RA['TL-Q4']['loi'] if x.startswith('(c)')], False)
RT = os.path.join(TMP, 'RIGHTS.md'); open(RT, 'w').write('| RIJ-01 | Rijksmuseum RP-F-00-568 (1886) | CC0 1.0 | https://id.rijksmuseum.nl/200144330 | SHA-256 '
                                                          '552b3a7100000000000000000000000000000000000000000000000000001f93 | nền then/now |\n')
AC = os.path.join(TMP, 'chong.jpg'); cv2.imwrite(AC, base_im)
B2 = copy.deepcopy(BA); B2['anh'] = [dict(id='RP-F-00-568', rights=RT, neo=True, neo_px_loi=[2.0, 3.5])]; B2['then_now']['anh_chong'] = AC
r = QT.check(B2, DA)['TL-Q4']; case('TL-Q4', f"ams30 + dòng RIGHTS đủ (CC0, URL, SHA) + ảnh chồng + log neo ≤ 1 % → đạt ({r['val']})", bad(r), False)
open(RT, 'w').write('| RIJ-01 | Rijksmuseum RP-F-00-568 (1886) | CC BY-NC 4.0 | https://id.rijksmuseum.nl/200144330 | SHA-256 552b3a71…1f93 |\n')
case('TL-Q4', 'dòng RIGHTS giấy phép CC BY-NC, SHA rút gọn → (a)', QT.check(B2, DA)['TL-Q4']['loi'], True)
B3 = copy.deepcopy(B2); B3['then_now']['hoa'] = [27.6, 27.9]
open(RT, 'w').write('| RIJ-01 | Rijksmuseum RP-F-00-568 (1886) | CC0 1.0 | https://id.rijksmuseum.nl/200144330 | ' + '5' * 64 + ' |\n')
case('TL-Q4', 'then/now hoà 0,3 s < 0,6 s → (c)', QT.check(B3, DA)['TL-Q4']['loi'], True)
PZ = json.load(open(os.path.join(DA, 'then-now-pose.json'))); PZ['reproj_rms_px'] = 14.0; PP = os.path.join(TMP, 'pose.json'); json.dump(PZ, open(PP, 'w'))
B3 = copy.deepcopy(B2); B3['then_now']['pose'] = PP
case('TL-Q4', 'then/now RMS 14 px / 1 200 px = 1,17 % > 1 % → (c)', QT.check(B3, DA)['TL-Q4']['loi'], True)
case('TL-Q5', f"ams30 (a)/(b): {RA['TL-Q5']['val']}", [x for x in RA['TL-Q5']['loi'] if x[:3] in ('(a)', '(b)')], False)
case('TL-Q5', 'gib20: thẻ ảnh LoC khung 193–263 = 2,96 s < 3 s → (c)', [x for x in RG['TL-Q5']['loi'] if x.startswith('(c)')], True)
NS = json.load(open(os.path.join(DA, 'text-budget-after.json'))); NS2 = copy.deepcopy(NS); NS2[100]['pct'] = 15.4; NS2[101]['center_unanchored_pct'] = 1.2
r = QT.check(dict(copy.deepcopy(BA), ngan_sach=NS2), DA)['TL-Q5']
case('TL-Q5', 'ams30 khung 100 lên 15,4 % + khung 101 có chữ không neo vùng giữa → (a), (b)', [x for x in r['loi'] if x[:3] in ('(a)', '(b)')], True)
LG3 = copy.deepcopy(LG); LG3['frames'][10]['text'].append(dict(s='No AI imagery · Census', role='method', px1080=38, ratio=12.0))
r = QT.check(dict(copy.deepcopy(BG), log_chu=LG3), DG)['TL-Q5']
case('TL-Q5', f"gib20 dòng phương pháp ở khung {LG3['frames'][10]['f']} (giữa phim) → (e)", [x for x in r['loi'] if x.startswith('(e)')], True)
case('TL-Q5', 'gib20 (d) ≤ 2 lớp thường trực, (f) chữ ≥ 38 px và tương phản ≥ 4,5 (min 9,32) → không lỗi', [x for x in RG['TL-Q5']['loi'] if x[:3] in ('(d)', '(e)', '(f)')], False)
N6 = dict(moc={'1941': 'HMGoG', '1987': 'Landsat 5'}, lop=dict(BAG=dict(loai='so_dang_ky', nam={'1655': 1, '1005': 728, '1931': 2506})))
case('TL-Q6', 'lớp sổ BAG còn 728 toà năm 1005 (giữ chỗ) mọc → trượt', QT.tlq6(dict(nam_toa=N6))['loi'], True)
N6['lop']['BAG']['nam']['1005'] = 0
case('TL-Q6', 'lớp sổ BAG đã loại 1005 → đạt', bad(QT.tlq6(dict(nam_toa=N6))), False)
N7 = dict(moc={'1941': 'HMGoG'}, gia=[1812], lop=dict(GWR=dict(loai='so_dang_ky', nam={'1812': 40, '1900': 10})))
case('TL-Q6', 'sổ GWR có mã năm giả 1812 (khai gia) → trượt', QT.tlq6(dict(nam_toa=N7))['loi'], True)
NG = copy.deepcopy(BG['nam_toa']); NG['lop'] = {k: v for k, v in NG['lop'].items() if v['loai'] == 'tang_chuan'}
case('TL-Q6', 'gib20 tầng chuẩn (Gibraltar 1987/2026, đất 1941/1987/2026) chỉ đổi ở mốc có nguồn → đạt', bad(QT.tlq6(dict(nam_toa=NG))), False)
NG['lop']['Gibraltar (khối OSM, tầng chuẩn)']['nam']['1960'] = 12
case('TL-Q6', 'gib20 tầng chuẩn thêm 12 toà đổi trạng thái năm 1960 (không có mốc nguồn) → trượt', QT.tlq6(dict(nam_toa=NG))['loi'], True)
case('TL-Q6', 'gib20 lớp La Línea (sổ Catastro) không có phân bố năm → THIẾU', RG['TL-Q6']['thieu'], True)

for rule, name, kind_, ok, got in R: print(f"{'ĐÚNG' if ok else 'SAI '}  {rule:<6} {kind_:<8} {name}" + ('' if ok else f'   → {got}'))
by = {}
for rule, _, k, ok, _ in R: by.setdefault(rule, set()).add(k)
miss = [k for k, v in by.items() if v != {'sạch', 'bắt lỗi'}]
n_ok = sum(r[3] for r in R); print(f'\nselftest 1.12.0: {n_ok}/{len(R)} ca đúng kỳ vọng · {len(by)} luật, luật thiếu ca đạt hoặc trượt: {miss or "không"}')
sys.exit(0 if n_ok == len(R) and not miss else 1)
