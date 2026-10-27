#!/opt/cine/bin/python
"""BAN-CUOI-T4-B2a · tệp máy + danh sách việc dựng (dung_bc.py / dung_b1.py) — tất định, ghi vào channel-k2/k2c-t4-02/ban-cuoi/may/b2a/.
Nguồn máy: animatic2/may/<máy>.json (đọc, không sửa) — đúng máy/khung/cắt của BẢNG SHOT v4 như may_b1.py (dac-ta-v4/log-shot.json t0/t1 →
số khung = round(t1·24) − round(t0·24), khung 0 … n−1 của tệp máy).
(1) B1-Q1: M00 (P1b VONG 17 s, máy ban-cuoi/may/b1/M00.json) và H1-01h nâng lên ≈ 160 m, GIỮ hướng nhìn ngang (phương vị), tâm nhìn, cung VONG và giờ;
    pitch chỉnh theo hệ số `kp` (0 = giữ điểm nhìn → cúi thêm đúng góc hình học; 1 = giữ góc cúi → nâng điểm nhìn cùng độ cao): 3 phương án thử (kp 0 / 0,5 / 1),
    chọn ở báo cáo theo đo bố cục (vòng lửa / khung City) — biến CHON.
(2) M01 thử E (K1179-D5, D6): máy CODINH = khoá 0 của M01 (≡ E-P1-ngay.json), 2304×1296 (đẩy 2D 1,0 %/s tới ×1,179 vẫn cắt từ ≥ 1954 px, không phóng to),
    tấm tĩnh spp 24 + mặt nạ 1/2/3e; khung tl 429 (giờ 14,00 → 14,30: tấm AI tĩnh nên thời gian lớp (a)-E 3D chạy chậm như tl thử của phiên A, 1 phút/giây).
(3) Dựng 1080p (look3-b1 cờ d, spp 4): MÓC M00–M04 (M04 +0,5 EV C9b), HỒI 2 đầu H2-00, H2-02, H2-03b, H2-04h, H2-04a (trang bc/look3-b1d = look3-b1 + lớp
    người/xe của look2d, "look2d tầm phố như bảng"), H2-05; dựng lại H1-01h. Thứ tự: M00, H1-01h trước, rồi theo bảng.
  may_b2a.py"""
import copy, gzip, json, math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import types   # noqa: E402
# chỉ nạp phần đầu may_b1.py (hằng + cr/at/ngua/log_tinh — bản sao at() của render_thub.js), KHÔNG chạy phần ghi tệp b1
_s = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'may_b1.py')).read(); M1 = types.SimpleNamespace()
_g = {'__file__': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'may_b1.py')}; exec(_s.split('# ---------------------------------------------------------------- việc 2')[0], _g); M1.__dict__.update(_g)
REPO = M1.REPO; EP = M1.EP; A2 = M1.A2; BC = M1.BC; OUT = f'{BC}/may/b2a'; os.makedirs(OUT, exist_ok=True)
REL = 'channel-k2/k2c-t4-02/ban-cuoi/may/b2a/'; PAGE = 'bc/look3-b1'; D = {'d': True}; FPS = 24
ld = M1.ld; LS = M1.LS; nkhung = M1.nkhung; nmay = M1.nmay
V = {}
CHON = {'M00': 0.0, 'H1-01h': 1.0}     # kp đã chọn sau thử (reports/ban-cuoi-t4-b2a/thu-may-do.json; báo cáo §1): M00 giữ vị trí vòng lửa, H1-01h giữ chân trời + khung City
Z_MOI = {'M00': (165.0, 155.0), 'H1-01h': (160.0, 160.0)}   # M00: giữ cú hạ nhẹ 10 m (B1: 125 → 112); H1-01h: 160 m (B1: 120 → 117,9)


def ghi(ten, sh, page=PAGE, W=1920, H=1080): sh['W'], sh['H'] = W, H; sh['page'] = page; json.dump(sh, open(f'{OUT}/{ten}.json', 'w'), ensure_ascii=False, indent=1); return REL + ten + '.json'
def viec(nhom, ten, shot, **kw): V.setdefault(nhom, []).append(dict(dict(ten=ten, shot=shot, page=PAGE, lk='look3d/', key=D, spp=4), **kw))


def nang(sh, z0, z1, kp):
    """nâng máy: z nội suy z0 → z1 theo t; điểm nhìn: l_z += kp · Δz (Δz = z mới − z cũ của chính khoá đó)"""
    sh = copy.deepcopy(sh); K = sh['keys']; T = K[-1]['t'] or 1.0
    for k in K:
        z = z0 + (z1 - z0) * (k['t'] / T); dz = z - k['p'][2]
        k['p'] = [k['p'][0], k['p'][1], round(z, 3)]; k['l'] = [k['l'][0], k['l'][1], round(k['l'][2] + kp * dz, 3)]
    return sh


# ---------------------------------------------------------------- (1) máy mới M00 / H1-01h
NG = {}
for ma, src in (('M00', f'{BC}/may/b1/M00.json'), ('H1-01h', f'{BC}/may/b1/H1-01h.json')):
    s0 = ld(src); N = nmay(s0) if ma == 'M00' else nkhung(ma); fr = [0, N // 2, N - 1]
    NG[ma] = dict(cu=[round(M1.ngua(M1.at(s0, f / FPS)), 2) for f in fr], cu_z=[round(M1.at(s0, f / FPS)['p'][2], 1) for f in fr])
    viec('thu-may', f'thu-{ma}-cu', REL + f'thu-{ma}-cu.json', w=960, h=540, only=fr); ghi(f'thu-{ma}-cu', copy.deepcopy(s0))
    for kp in (0.0, 0.5, 1.0):
        s = nang(s0, *Z_MOI[ma], kp); s['may_b2a'] = f'B1-Q1: nâng {s0["keys"][0]["p"][2]} → {Z_MOI[ma][0]}…{Z_MOI[ma][1]} m, kp {kp} (giữ phương vị, tâm nhìn, giờ)'
        tag = f'thu-{ma}-kp{int(kp * 10):02d}'; ghi(tag, s); viec('thu-may', tag, REL + tag + '.json', w=960, h=540, only=fr)
        NG[ma][f'kp{kp}'] = [round(M1.ngua(M1.at(s, f / FPS)), 2) for f in fr]
    s = nang(s0, *Z_MOI[ma], CHON[ma]); s['may_b2a'] = f'B1-Q1: nâng → {Z_MOI[ma][0]}…{Z_MOI[ma][1]} m, kp {CHON[ma]} (chọn sau thử; giữ phương vị, tâm nhìn, cung VONG, giờ)'
    s['shot'] = ma; p = ghi(ma, s); NG[ma]['chon'] = CHON[ma]
    with open(f'{OUT}/{ma}-log-may.json.gz', 'wb') as f: f.write(gzip.compress(json.dumps(M1.log_tinh(s, list(range(N)))).encode(), mtime=0))
    viec('dung', ma, p, only=list(range(N)))

# ---------------------------------------------------------------- (3) dựng 1080p theo bảng v4 (MÓC + HỒI 2 đầu)
DS = []
for ma in ('M01', 'M02', 'M03', 'M04', 'H2-00', 'H2-02', 'H2-03b', 'H2-04h', 'H2-04a', 'H2-05'):
    s = LS[ma]; sh = ld(f'{A2}/{ma}.json'); N = nmay(sh); n = min(nkhung(ma), N); page = PAGE
    if ma == 'M04':
        sh['look'] = dict(sh['look'], exposure=round(sh['look']['exposure'] * 2 ** 0.5, 4)); sh['c9b_ev'] = 0.5
        for k in sh['keys']:
            if k.get('look', {}).get('exposure'): k['look']['exposure'] = round(k['look']['exposure'] * 2 ** 0.5, 4)
    if ma == 'H2-04a': page = 'bc/look3-b1d'
    p = ghi(ma, sh, page); viec('dung', ma, p, page=page, only=list(range(n)))
    DS.append(dict(ma=ma, may=f'animatic2/may/{ma}.json', khung=[0, n - 1], so_khung=n, khung_bang=nkhung(ma), khung_may=N, giay=round(n / FPS, 4), trang=page))
for ma in ('M00', 'H1-01h'):
    n = nmay(ld(f'{OUT}/{ma}.json')) if ma == 'M00' else nkhung(ma)
    DS.insert(0 if ma == 'M00' else 1, dict(ma=ma, may=f'ban-cuoi/may/b2a/{ma}.json', khung=[0, n - 1], so_khung=n, khung_bang=nkhung(ma), giay=round(n / FPS, 4), trang=PAGE))
# thứ tự: M00, H1-01h, rồi theo bảng (M01 3D trước, M02…)
V['dung'] = [j for t in ('M00', 'H1-01h') for j in V['dung'] if j['ten'] == t] + [j for j in V['dung'] if j['ten'] not in ('M00', 'H1-01h')]

# ---------------------------------------------------------------- (2) M01 thử E: tấm tĩnh + mặt nạ + tl CODINH 2304×1296
WE, HE = 2304, 1296
m01 = ld(f'{A2}/M01.json'); k0 = copy.deepcopy(m01['keys'][0]); NE = nkhung('M01')
e = copy.deepcopy(m01); e.update(cu_may='CODINH', shot='M01-E', dur=0.0417, keys=[dict(k0, t=0.0)]); e['may_b2a'] = 'M01 thử E: khoá 0 của M01 (≡ E-P1-ngay.json), CODINH'
pe = ghi('E-M01', e, W=WE, H=HE)
for ten, kw in (('E-M01', dict(png=1, spp=24)), ('E-M01-m1', dict(mask=1, key={})), ('E-M01-m2', dict(mask=2, key={})), ('E-M01-m3e', dict(mask=3, lk='look3e/', key={}))):
    viec('e', ten, pe, w=WE, h=HE, only=[0], **kw)
tl = copy.deepcopy(m01); d0 = k0['date']
tl.update(cu_may='CODINH', shot='M01-E-tl', dur=round(NE / FPS, 4), keys=[dict(k0, t=0.0, date=list(d0)), dict(k0, t=round(NE / FPS, 4), date=[d0[0], d0[1], d0[2], round(d0[3] + 0.30, 4)])])
tl['may_b2a'] = 'M01 thử E: lớp (a)-E 3D CODINH (khoá 0 của M01), giờ 14,00 → 14,30 (tấm AI tĩnh)'
viec('e', 'E-M01-tl', ghi('E-M01-tl', tl, W=WE, H=HE), w=WE, h=HE, only=list(range(NE)), xong=False)
# xen lớp (a)-E 3D của thử E ngay sau M01 3D trong hàng sản xuất (giữ P = 2 liên tục; xong: false → không mã hoá D-B1/LFS)
i = [j['ten'] for j in V['dung']].index('M01'); V['dung'].insert(i + 1, V['e'][-1])

# ---------------------------------------------------------------- (4) soi năm biên §19 (d): shot B2a có St Paul's (cũ/mới)/Monument trong 1666–1711 — khung năm đầu/cuối
#     + mọi năm mốc giai đoạn xây nằm trong dải năm của shot (M02 chạy lùi 2026 → 1666 qua cả 1711 … 1671). Soi TRƯỚC khi dựng 1080p (luật §19 (d)): khung 1080p cùng máy/trang + mặt nạ 2 để cắt ô.
BIEN = (1671.0, 1675.5, 1677.0, 1708.0, 1709.5, 1711.0)
SOIK = []
for ma in ('M02', 'H2-00', 'H2-02', 'H2-03b', 'H2-04h', 'H2-04a', 'H2-05'):
    sh = ld(f'{OUT}/{ma}.json'); n = min(nkhung(ma), nmay(sh)); yr = [M1.at(sh, f / FPS).get('year') or 1666.66 for f in range(n)]
    want = {0: 'đầu shot', n - 1: 'cuối shot'}
    for y in BIEN:
        if min(yr) - 1e-6 <= y <= max(yr) + 1e-6: f = min(range(n), key=lambda f: abs(yr[f] - y)); want.setdefault(f, f'năm mốc {y}')
    for f, why in sorted(want.items()): SOIK.append(dict(may=ma, khung=f, nam=round(yr[f], 3), ly_do=why))
    viec('soi', 'soi-' + ma, REL + ma + '.json', only=sorted(want), page=sh['page']); viec('soi', 'soi-' + ma + '-m2', REL + ma + '.json', only=sorted(want), mask=2, key={}, page=sh['page'])

for nhom, L in V.items(): json.dump(L, open(f'{OUT}/viec-{nhom}.json', 'w'), ensure_ascii=False, indent=1)
json.dump(dict(dung=DS, ngua=NG, z_moi=Z_MOI, chon=CHON, soi=SOIK), open(f'{OUT}/muc-luc-b2a.json', 'w'), ensure_ascii=False, indent=1)
print({k: (len(v), sum(len(j.get('only') or [0]) for j in v)) for k, v in V.items()}); print(json.dumps(NG, ensure_ascii=False))
