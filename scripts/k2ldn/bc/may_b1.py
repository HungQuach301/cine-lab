#!/opt/cine/bin/python
"""BAN-CUOI-T4-B1 · tệp máy + danh sách việc dựng (dung_bc.py) cho phần B1 — tất định, ghi vào channel-k2/k2c-t4-02/ban-cuoi/may/b1/.
Nguồn máy: animatic2/may/<máy>.json (đọc, không sửa) — đúng máy/khung/cắt của BẢNG SHOT v4 (dac-ta-v4/log-shot.json: t0/t1 → số khung = round(t1·24) − round(t0·24),
giống bước ghép animatic ghep_v3.py: khung 0 … n−1 của tệp máy). Ngoại lệ có ghi: H1-15h2 = n khung CUỐI của máy H1-15h (phần 3D sau clip H1-15x — máy chạy tiếp,
kết đúng khung cuối máy; không đóng băng), KHOP = hai tệp máy -a/-b dựng đủ (ghép hoà ở B3 theo ghep_v3.py).
Mọi việc: trang design/k2v/ldn/bc/look3-b1.js (look3 + sửa D-A4), cờ d, spp 4, 1920×1080 (LOOK-T4-8; lệnh B1 việc 2).
Thêm: M00 VONG 17 s từ điểm P1b (D-A8), H3-05c dự phòng 6,0 s (dịch ≈ 20 m về nam + hạ điểm nhìn), máy H2-10 / H5-05b ngửa 5–15° (MAY-19 (a), D-A4 (v)) + log máy tính toán,
khung soi niên đại năm biên (§19 (d)), mẫu sau sửa (6 khung phiên A + M00 đầu/giữa/cuối).
  may_b1.py"""
import copy, gzip, json, math, os
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
EP = os.path.join(REPO, 'channel-k2/k2c-t4-02'); A2 = f'{EP}/animatic2/may'; BC = f'{EP}/ban-cuoi'; OUT = f'{BC}/may/b1'; os.makedirs(OUT, exist_ok=True)
REL = 'channel-k2/k2c-t4-02/ban-cuoi/may/b1/'; PAGE = 'bc/look3-b1'; D = {'d': True}; FPS = 24
ld = lambda p: json.load(open(p))
LS = {s['ma']: s for s in ld(f'{BC}/dac-ta-v4/log-shot.json')}
V = {}


def ghi(ten, sh): sh['W'], sh['H'] = 1920, 1080; sh['page'] = PAGE; json.dump(sh, open(f'{OUT}/{ten}.json', 'w'), ensure_ascii=False, indent=1); return REL + ten + '.json'
def viec(nhom, ten, shot, **kw): V.setdefault(nhom, []).append(dict(ten=ten, shot=shot, page=PAGE, lk='look3d/', key=D, spp=4, **kw))
def nkhung(ma): s = LS[ma]; return int(round(s['t1'] * FPS)) - int(round(s['t0'] * FPS))
def nmay(sh): return int(round(sh['dur'] * FPS)) or 1


# ---------------------------------------------------------------- nội suy máy (bản sao at() của render_thub.js — để tính log máy không cần dựng)
def cr(p0, p1, p2, p3, t):
    t2, t3 = t * t, t * t * t
    return [0.5 * (2 * p1[i] + (-p0[i] + p2[i]) * t + (2 * p0[i] - 5 * p1[i] + 4 * p2[i] - p3[i]) * t2 + (-p0[i] + 3 * p1[i] - 3 * p2[i] + p3[i]) * t3) for i in range(3)]


def at(S, t):
    K = S['keys']
    if len(K) == 1 or t <= K[0]['t']: return K[0]
    if t >= K[-1]['t']: return K[-1]
    i = 0
    while K[i + 1]['t'] < t: i += 1
    a, b = K[i], K[i + 1]; u = (t - a['t']) / (b['t'] - a['t']); um = u if S.get('easeKeys') is False else u * u * (3 - 2 * u)
    k0, k3 = K[max(0, i - 1)], K[min(len(K) - 1, i + 2)]
    o = dict(a); o['p'] = cr(k0['p'], a['p'], b['p'], k3['p'], um); o['l'] = cr(k0['l'], a['l'], b['l'], k3['l'], um); o['fov'] = a['fov'] + (b['fov'] - a['fov']) * u
    if a.get('year') is not None and b.get('year') is not None: o['year'] = a['year'] + (b['year'] - a['year']) * u
    return o


def ngua(k): dx = k['l'][0] - k['p'][0]; dy = k['l'][1] - k['p'][1]; return math.degrees(math.atan2(k['l'][2] - k['p'][2], math.hypot(dx, dy)))


def log_tinh(S, frames):
    return dict(nguon='tính từ tệp máy (bản sao at() của render_thub.js) — KHÔNG dựng', shot=S.get('shot'), fps=FPS, W=1920, H=1080,
                frames=[dict(f=f, year=at(S, f / FPS).get('year'), cam=dict(p=at(S, f / FPS)['p'], l=at(S, f / FPS)['l'], fov=at(S, f / FPS)['fov']), ngua_deg=round(ngua(at(S, f / FPS)), 3)) for f in frames])


# ---------------------------------------------------------------- việc 2: dựng 1080p HỒI 1 + HỒI 3 (lớp D 3D)
SX = {'H1-15h2': 'H1-15h'}
DS = []
for ma, s in LS.items():
    if s['chuong'] not in ('HỒI 1', 'HỒI 3') or s['cu_may'] in ('MD', 'THAT', 'TL', 'PP') or not s.get('diem_may'): continue
    cams = [ma + '-a', ma + '-b'] if s['cu_may'] == 'KHOP' else [SX.get(ma, ma)]
    for cm in cams:
        sh = ld(f'{A2}/{cm}.json'); N = nmay(sh); n = N if s['cu_may'] == 'KHOP' else min(nkhung(ma), N)
        fr = list(range(N - n, N)) if ma in SX else list(range(n))
        ten = cm if s['cu_may'] == 'KHOP' else ma; p = ghi(ten, sh)
        viec('h' + s['chuong'][-1], ten, p, only=fr)
        DS.append(dict(ma=ma, tep=ten, may=f'animatic2/may/{cm}.json', khung=[fr[0], fr[-1]], so_khung=len(fr), khung_bang=nkhung(ma), khung_may=N, giay=round(len(fr) / FPS, 4)))

# H3-05c dự phòng (PHIẾU-A A1-H3-05b (c)): dịch ≈ 20 m về nam + hạ điểm nhìn (tháp tiền cảnh không che chân mái vòm) — 3 phương án soi, chọn ở báo cáo
h5c = ld(f'{BC}/may/H3-05c-du-phong.json')
for ten, dn, dz, lz in (('H3-05c-s20', -20, 0, 95), ('H3-05c-s20-l', -20, -6, 80), ('H3-05c-s20-ll', -20, -10, 72)):
    sh = copy.deepcopy(h5c)
    for k in sh['keys']: k['p'] = [k['p'][0], k['p'][1] + dn, k['p'][2] + dz]; k['l'] = [k['l'][0], k['l'][1], lz]
    sh['may_b1'] = f'H3-05c-du-phong.json dịch {dn} m bắc–nam, cao {dz:+} m, điểm nhìn z {lz}'; p = ghi(ten, sh)
    viec('h5c-thu', ten, p, only=[0]); viec('h5c-thu', ten + '-m2', p, only=[0], mask=2)

# ---------------------------------------------------------------- M00 VONG 17 s (P1b, D-A8): cung quanh tâm lửa đầu cầu, ±12,5° (≈ 1,5°/s ≤ 3°/s), hạ 125 → 112 m, giờ 19,6 → 20,6
m0 = ld(f'{BC}/may/M00-moi-a.json'); k0 = m0['keys'][0]; L0 = k0['l']; dx, dy = k0['p'][0] - L0[0], k0['p'][1] - L0[1]; r0 = math.hypot(dx, dy); a0 = math.atan2(dy, dx)
keys = []
for i in range(69):
    t = 17.0 * i / 68; u = t / 17.0; a = a0 + math.radians(-12.5 + 25.0 * u); r = r0 * (1.0 - 0.06 * u)
    keys.append(dict(k0, t=round(t, 4), p=[round(L0[0] + r * math.cos(a), 2), round(L0[1] + r * math.sin(a), 2), round(125.0 - 13.0 * u, 2)], l=list(L0), hour=round(19.6 + 1.0 * u, 4)))
m0v = copy.deepcopy(m0); m0v.update(dur=17.0, keys=keys, cu_may='VONG', shot='M00', nguon_may='ban-cuoi/may/M00-moi-a.json (điểm P1b, D-A8) → VONG ±12,5° quanh tâm nhìn, 17 s')
pm0 = ghi('M00', m0v)

# ---------------------------------------------------------------- MAY-19 (a): H2-10 THAP, H5-05b THAP → ngửa 6,0 → 9,0° (trong 5–15°), giữ điểm máy + hướng ngang + nhịp ngửa dần
MAY19 = {}
for ma, lo, hi in (('H2-10', 6.0, 9.0), ('H5-05b', 6.0, 9.0)):
    sh = ld(f'{A2}/{ma}.json'); K = sh['keys']; n = len(K)
    for i, k in enumerate(K):
        d_ = math.hypot(k['l'][0] - k['p'][0], k['l'][1] - k['p'][1]); g = lo + (hi - lo) * (i / max(1, n - 1))
        k['l'] = [k['l'][0], k['l'][1], round(k['p'][2] + d_ * math.tan(math.radians(g)), 3)]
    sh['may_b1'] = f'MAY-19 (a): ngửa {lo} → {hi}° (bản v4: {round(ngua(ld(f"{A2}/{ma}.json")["keys"][0]), 2)} → {round(ngua(ld(f"{A2}/{ma}.json")["keys"][-1]), 2)}°)'
    p = ghi(ma + '-v5', sh); N = nmay(sh); lg = log_tinh(sh, list(range(N)))
    with gzip.open(f'{OUT}/{ma}-v5-log-may.json.gz', 'wt') as f: json.dump(lg, f)
    ng = [fr['ngua_deg'] for fr in lg['frames']]; MAY19[ma] = dict(tep=p, khung=N, ngua_min=min(ng), ngua_max=max(ng), truoc=[round(ngua(ld(f'{A2}/{ma}.json')['keys'][0]), 2), round(ngua(ld(f'{A2}/{ma}.json')['keys'][-1]), 2)])

# ---------------------------------------------------------------- soi niên đại năm biên (§19 (d)) — khung 3D tại năm biên của từng shot có St Paul's mới / Monument 1666–1711
SOI = [('H2-05s', None), ('H2-06', None), ('H2-08', None), ('H2-09', None), ('H2-10', 'H2-10-v5'), ('H2-11', None), ('H2-12-b', None), ('H2-14', None), ('H3-01', None), ('H3-06-b', None)]
BIEN = (1675.0, 1708.0, 1709.5, 1711.0)
SOIK = []
for cm, alt in SOI:
    sh = ld(f'{OUT}/{alt}.json') if alt else ld(f'{A2}/{cm}.json'); N = nmay(sh); yr = [at(sh, f / FPS).get('year') or 1666.66 for f in range(N)]
    want = {0: 'đầu shot', N - 1: 'cuối shot'}
    for y in BIEN:
        if min(yr) - 1e-6 <= y <= max(yr) + 1e-6: f = min(range(N), key=lambda f: abs(yr[f] - y)); want.setdefault(f, f'năm biên {y}')
    p = ghi('soi-' + cm, sh)
    for f, why in sorted(want.items()): SOIK.append(dict(may=cm, khung=f, nam=round(yr[f], 3), ly_do=why))
    viec('soi', 'soi-' + cm, p, only=sorted(want)); viec('soi', 'soi-' + cm + '-m2', p, only=sorted(want), mask=2)

# ---------------------------------------------------------------- mẫu sau sửa: 6 khung phiên A (khung đầu của 12 khung mẫu A) + M00 đầu/giữa/cuối
for base, f in (('M01', 208), ('H1-08b', 212), ('H2-10', 210), ('H3-05', 158), ('H4-04a', 84), ('H5-08', 162)):
    sh = ld(f'{BC}/may/mau-{base}.json'); p = ghi('mau-' + base, sh); viec('mau', 'mau-' + base, p, only=[f])
viec('mau', 'mau-M00', pm0, only=[0, 204, 407])
viec('mau', 'mau-H2-10-v5', REL + 'H2-10-v5.json', only=[210])

for nhom, L in V.items(): json.dump(L, open(f'{OUT}/viec-{nhom}.json', 'w'), ensure_ascii=False, indent=1)
json.dump(dict(dung=DS, may19=MAY19, soi=SOIK), open(f'{OUT}/muc-luc-b1.json', 'w'), ensure_ascii=False, indent=1)
print({k: (len(v), sum(len(j.get('only') or [0]) for j in v)) for k, v in V.items()}); print(json.dumps(MAY19, ensure_ascii=False))
