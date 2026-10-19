#!/opt/cine/bin/python
"""G1b T3 · SINH ĐẶC TẢ TOÀN TẬP (animatic 540p + bản sản xuất) từ bảng shot vay-ham/treatment.json (74 shot, 721,2 s sau VL1) + lời khoá script-v4.1-KHOA.md.
Một đoạn (segment) = một shot của bảng; cảnh 3D = scene tl/t3s (design/k2v/tl/scenes/t3s.js, đường ống V6 bản SẢN XUẤT) hoặc cảnh V6 có sẵn (vinh6, bo6, gib20 + tech.v6);
ảnh/tranh/bản đồ lịch sử = photo/print (tư liệu ref ≤ 1600 px cho animatic — bản sản xuất tải bản gốc theo vay-ham/tai-san-vay-ham.json); thẻ số = p.card trên nền cảnh trước (mờ);
khung neo 1782/1943 = bản LAI 540p của V6 (reports/v6/khung-neo, cắt bỏ chữ cũ); bản đồ chiến lược = g1b/sm/<SM>.yaml của phiên con (thiếu → thẻ chờ).
KHUNG SẠCH (Kinh thánh §12.1): mọi shot p.sach = true; chip nơi chỉ khi vào nơi mới (≤ 3 s); số/câu trích (p.so) khi lời nói tới, ≤ 3 s, kèm tên nguồn ngắn.
Q37: mỗi cảnh 3D chia CÚ ≤ 6 s nối bằng cắt (t3s opt.cams) → không khoảng > 6 s không biến cố; mỗi cú khai beat 'cut' trong đoạn.
Nhịp lời: 2,5 từ/s (g1/kiem_loi.py; Eric chưa thu ở T3 — nhịp đo T2 chưa áp), lời bắt đầu trễ theo kiem-chu.json (bat_dau_tre_s). Phụ đề lời = đường ray tạm (.srt), KHÔNG lên bản cuối.
Ra: g1b/episode.yaml, g1b/ray-loi.srt, g1b/log-shot.json (nguon/bac/ai_image/ai_texture/chu_tat mỗi shot), g1b/cut-plan.json.
Dùng: /opt/cine/bin/python -I channel-k2/k2c-t3-01/g1b/mk_ep_g1b.py [--out /var/tmp/cine-out/k2c-t3-g1b]"""
import json, math, os, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent; EP = HERE.parent; REPO = EP.parents[1]
OUT = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else '/var/tmp/cine-out/k2c-t3-g1b'
WPS = 2.5
TR = json.loads((EP / 'vay-ham/treatment.json').read_text())['shots']
KC = {r['id']: r for r in json.loads((EP / 'g1/kiem-chu.json').read_text())['shots']}

# ---------------- lời khoá: câu nói + [TRÊN HÌNH] theo shot ----------------
def parse_script():
    S, cur = {}, None
    for line in (EP / 'script-v4.1-KHOA.md').read_text().splitlines():
        m = re.match(r'^‹([^›]+)›\s*(.*)', line)
        if m and m.group(1) in KC: cur = m.group(1); S[cur] = {'say': m.group(2), 'tren_hinh': []}; continue
        if cur and line.startswith('[TRÊN HÌNH]'): S[cur]['tren_hinh'].append(line[len('[TRÊN HÌNH]'):].strip())
        elif line.startswith('[0') or line.startswith('# ') or line.startswith('> '): cur = None if line.startswith('[0') else cur
    for k, v in S.items():
        v['say'] = re.sub(r'\s+', ' ', re.sub(r'\{[^}]*\}', '', v['say']).replace('‹Our read›', '').replace('[IM LẶNG]', '')).strip()
    return S
SCRIPT = parse_script()
def speak_words(t):   # cùng cách đếm g1/kiem_loi.py (năm đọc thành chữ → nhiều từ hơn): lấy từ kiem-chu cho tổng, chia theo câu tỉ lệ
    return [w for w in re.split(r"[\s\-–—]+", re.sub(r"[^\w\s\-–—'’]", ' ', t)) if re.search(r'\w', w)]
def sentences(t): return [s.strip() for s in re.split(r'(?<=[.?!:;])\s+(?=[A-Z"“‘])', t) if s.strip()]

# ---------------- máy (t3s opt.cams) ----------------
def push(fr, to, look, d=None, fov=40, fov1=None, hold=None): return dict(k='push', **{'from': fr}, to=to, look=look, dur=d, fov=fov, **({'fov1': fov1} if fov1 else {}), **({'hold': hold} if hold else {}))
def line(L, s0, s1, h, d=None, look=200, dip=40, fov=40, typ='pho', east=0, north=0): return dict(k='line', line=L, s0=s0, s1=s1, h=h, dur=d, look=look, dip=dip, fov=fov, type=typ, east=east, north=north)
def orbit(c, r, h, a0, a1, d=None, fov=38, up=0): return dict(k='orbit', c=c, r=r, h=h, a0=a0, a1=a1, dur=d, fov=fov, lookUp=up)
def lat(c, yaw, dist, ln, h, d=None, fov=30): return dict(k='lateral', c=c, yaw=yaw, dist=dist, len=ln, h=h, dur=d, fov=fov)
def top(c, h0, h1, d=None, y0=0, y1=12, fov=40): return dict(k='top', c=c, h0=h0, h1=h1, dur=d, yaw0=y0, yaw1=y1, fov=fov)
def neo(E, N, h, heading, d=None, pitch=2, fov=41.1): return dict(k='neo', pose=dict(E=E, N=N, h=h, heading=heading, pitch=pitch, fovV=fov, nguon='G1b'), dur=d)
def lerp(a, b, u): return [a[i] + (b[i] - a[i]) * u for i in range(3)]

# toạ độ mốc (ENU m, origin gói gib = giao lộ đường băng × Winston Churchill Ave)
GATE = [61, 479]; KB = [-602, -1276]; GP = [-505, -1165]; OLD = [-430, -1300]; NFACE = [250, -900]; LL_REAL = [[103, 1114], [115, 1162], [122, 1195], [132, 1257], [138, 1285], [156, 1379], [169, 1443], [180, 1499], [195, 1574], [205, 1619], [213, 1654], [219, 1688], [235, 1759], [243, 1787]]
ISTH_N = [[-300, -600], [-120, -200], [0, 0], [40, 300], [70, 520], [110, 900], [160, 1400], [230, 2200], [320, 3200]]   # dòng người lên bắc (1704 → San Roque) — tuyến minh hoạ dọc eo đất
SOUTH = [[-430, -1820], [-330, -2150], [-250, -2500], [-150, -2850]]   # dân dạt về nam (S062) — sau tường nam
OLDBOX = [-800, -1950, -150, -640]
CIV = ['#e7e0cf', '#5e4a38', '#3d4a5a', '#7a5a3a', '#a89f8a']; GB1782 = ['#b03a2e', '#a8402e', '#b03a2e', '#e7e0cf', '#5e4a38']; ES1704 = ['#e7e0cf', '#c9a227', '#5e4a38', '#3d4a5a']
MOD = ['#3d4a5a', '#e7e0cf', '#7a2f2a', '#2f5d7a', '#5e4a38', '#c9a227']; MIL43 = ['#6b6a4a', '#7a7656', '#2f3d5c', '#e7e0cf', '#6b6a4a']

def T3(**o): return dict(kind='t3s', opt=o)

# ---------------- cảnh 3D: mỗi shot → một hoặc nhiều cảnh (nhiều cảnh = nhảy mốc năm trong shot, nối bằng cắt) ----------------
def era_push(eras, fr, to, look, fov=42, base=None):
    """chia một cú push liên tục thành các mảnh, mỗi mảnh một mốc năm (cảnh riêng) — 0e 'tua ngược', 5j 'bảng điểm bằng địa hình'"""
    tot = sum(e['d'] for e in eras); t = 0; out = []
    for e in eras:
        u0, u1 = t / tot, (t + e['d']) / tot; t += e['d']
        o = dict(base or {}); o.update({k: v for k, v in e.items() if k not in ('d',)}); o['cams'] = [push(lerp(fr, to, u0), lerp(fr, to, u1), look, fov=fov, hold=0.05)]; o['dur'] = e['d']
        out.append(T3(**o))
    return out

LIFE_WCA = lambda n=60, women=True: dict(walkers=[dict(line='WCA', n=n, width=6, women=women)], birds=dict(c=[0, -200], r=200, h=60, n=10))
S3 = {
 '0a': T3(year=2026, date=[2026, 10, 18, 16.80, 16.86], dayCycle=True, noi='thanh_pho', counter={'s': '2026'},
          cams=[push([15, 2.5, 150], [8, 2.5, 70], [250, 140, -1600], 3.5, fov=48), lat([0, 2, -30], -90, 45, 26, 3, None, fov=42)],
          life=dict(walkers=[dict(line='WCA', n=70, width=6)], crowds=[dict(line='WCA', groups=5, size=[4, 10], speed=1.2)], birds=dict(c=[0, 0], r=180, h=50, n=8)), ghi='lời nói NỬA ĐÊM nhưng máy dựng V6 chưa có cảnh đêm có đèn đường → animatic dùng nắng chiều thấp (mặt trời ≈ 4°) — đề xuất làm đêm (lượt chiếu sáng + đèn có nguồn) trước bản sản xuất'),
 '0b': T3(year=2026, date=[2026, 10, 18, 9, 9.2], noi='eo_dat', cams=[push([61, 8, 430], [30, 380, 820], [230, 150, -1000], fov=46)], life=LIFE_WCA(60)),
 '0e': era_push([dict(d=1.375, year=2026), dict(d=1.375, year=1943, town='1943'), dict(d=1.375, year=1782.6, town='1782', tech=dict(v6=dict(earth=True))), dict(d=1.375, year=1704.6, town='1704', hideTrees=OLDBOX)],
                [-1500, 200, -1500], [-980, 130, -1340], [-450, 0, -1260], base=dict(noi='thanh_pho', date=[2026, 6, 15, 10, 10.1])),
 '0g': T3(year=1941, date=[1941, 6, 15, 11, 11.2], noi='eo_dat', cams=[orbit([0, 2, 0], 95, 36, -100, -150, fov=34, up=14)], life=dict(walkers=[dict(line='WCA', n=30, width=5, women=False, colors=MIL43)], birds=dict(c=[0, 0], r=200, h=60, n=8))),
 '0h': T3(year=2026, date=[2026, 10, 18, 10, 10.2], noi='eo_dat', cams=[push([-700, 600, -400], [-620, 560, -220], [100, 0, 900], fov=46)], life=LIFE_WCA(80)),
 '1a': T3(year=1704.58, date=[1704, 8, 1, 9, 9.5], dual=True, counter='clockdual', julian=False, noi='bien', ships=True,
          cams=[lat([-2600, 0, -1600], 60, 7000, 2600, 3500, fov=36)], fleet=dict(n=18, center=[-3200, -2200], axis=35, spacing=230, kind='line', heading=55)),
 '1d': T3(year=1704.6, date=[1704, 8, 3, 10, 12], noi='thanh_pho', town='1704', hideTrees=OLDBOX,
          cams=[push([-1150, 60, -1500], [-980, 55, -1450], [-500, 10, -1350], 4.5, fov=44), line('MAIN', 200, 420, 45, 4.5, look=160, dip=40, fov=44), orbit([OLD[0], 0, OLD[1]], 520, 170, 185, 150, fov=42)],
          life=dict(walkers=[dict(line='MAIN', n=60, width=4, colors=ES1704)], birds=dict(c=[-430, -1300], r=170, h=70, n=12), chimney=14),
          fleet=dict(n=10, center=[-1700, -1500], axis=172, spacing=180, kind='line', heading=80), smoke=[dict(at=[-560, 10, -1400], n=10, size=30, rise=50, drift=[-2, 1], period=0.12, seed=3, alpha=0.7)]),
 '1e': T3(year=1704.6, date=[1704, 8, 4, 9, 10], dual=True, counter='clockdual', noi='thanh_pho', town='1704', hideTrees=OLDBOX, pin=[5.0, 7.0],
          cams=[push([-2200, 120, -1700], [-1700, 100, -1550], [-480, 20, -1300], 5.0, fov=40), push([-900, 50, -1420], [-800, 45, -1390], [-470, 25, -1300], fov=40)],
          fleet=dict(n=14, center=[-1900, -1600], axis=170, spacing=170, kind='line', heading=80), life=dict(walkers=[dict(line='MAIN', n=40, width=4, colors=ES1704)], chimney=10)),
 '1g': T3(year=1704.6, date=[1704, 8, 7, 9, 11], noi='eo_dat', town='1704', hideTrees=OLDBOX,
          cams=[push([-260, 70, -520], [-150, 75, -260], [60, 0, 600], 4.5, fov=44), lat([60, 0, 300], 160, 260, 360, 45, 4.5, fov=36), push([-200, 260, 200], [-100, 320, 700], [400, 0, 6000], fov=44)],
          life=dict(walkers=[dict(line=ISTH_N, n=140, width=10, colors=CIV, free=False)], crowds=[dict(line=ISTH_N, groups=14, size=[8, 24], speed=0.9, colors=CIV)])),
 '1i': T3(year=1713, date=[1713, 7, 13, 10, 11], noi='eo_dat', cams=[push([300, 220, 1500], [250, 200, 1250], [0, 60, -900], 4.5, fov=42), lat([0, 0, 300], -90, 800, 700, 160, 4.5, fov=38), push([-700, 360, 900], [-600, 330, 750], [-200, 40, -1200], fov=42)]),
 '1j': T3(year=1704.9, yearAt=[[0, 1704.9], [5.0, 1727.3]], date=[1727, 3, 1, 10, 11], noi='eo_dat',
          cams=[push([-600, 260, 1500], [-500, 240, 1300], [100, 0, -500], 5.0, fov=42), push([700, 260, 1500], [600, 240, 1300], [0, 0, -400], fov=42)],
          front=[dict(pts=[[-500, 900], [-100, 880], [300, 900], [700, 920]], side='es', grow=[0.5, 4.5], w=18)],
          smoke=[dict(at=[-200, 10, 880], n=12, size=34, rise=45, drift=[-2, 1], period=0.14, seed=5, alpha=0.75), dict(at=[300, 10, 900], n=10, size=30, rise=40, drift=[-2, 1], period=0.15, seed=6, alpha=0.7)]),
 '1k': T3(year=1730.8, yearAt=[[0, 1730.8], [5.0, 1732.5], [10.0, 1735]], date=[1730, 10, 8, 10, 11], noi='eo_dat', linea=True, lineaAt=[[0, 0.15], [5.0, 0.55], [10.0, 1.0]],
          cams=[top([0, 0, 1000], 1300, 1500, 5.0, 0, 6), lat([0, 0, 1020], 90, 600, 600, 120, 5.0, fov=36), push([-700, 300, 400], [-600, 280, 600], [300, 0, 1050], fov=42)]),
 '2a': T3(year=1779.47, date=[1779, 6, 21, 10, 11], noi='eo_dat', linea=True, counter={'s': '21 Jun 1779'},
          cams=[push([0, 60, 300], [20, 55, 420], [0, 0, 1100], 5.0, fov=44), lat([0, 0, 1030], -90, 420, 500, 60, 4.0, fov=34), top([0, 0, 650], 900, 1200, None)],
          units=[dict(at=[e, 1110], heading=180, rows=4, cols=20, side='es', day=[0, 99], seed=30 + i) for i, e in enumerate([-300, -60, 200, 460])]),
 '2c': T3(year=1779.6, date=[1779, 7, 16, 10, 11], noi='bien', counter={'s': 'Jul 1779'}, ships=False,
          cams=[lat([-2500, 0, -1500], 0, 2600, 1800, 300, 6.0, fov=34), push([-900, 160, -1300], [-1200, 150, -1300], [-7000, 0, -1800], fov=40)],
          fleet=dict(n=12, center=[-3000, -1600], axis=5, spacing=320, kind='line', heading=0), life=dict(boats=[dict(pts=[[-2600, -600], [-2800, -1600], [-2500, -2600]], len=12, speed=4.5, s0=0.2), dict(pts=[[-3300, -2600], [-3500, -1400], [-3200, -500]], len=11, speed=4.0, s0=0.6)])),
 '2f': T3(year=1781.3, date=[1781, 4, 12, 9, 9.3], noi='bien', ships=False, cams=[lat([-1800, 0, -1500], 30, 2400, 1500, 260, fov=34)],
          fleet=dict(n=16, center=[-2100, -1700], axis=150, spacing=200, kind='line', heading=60), life=dict(boats=[dict(pts=[[-1500, -1200], [-1000, -1350], [-750, -1450]], len=9, speed=4, s0=0.3)])),
 '2g': T3(year=1781.28, date=[1781, 4, 12, 10.6, 10.9], counter='clock', noi='thanh_pho', town='1782', tech=dict(v6=dict(earth=True)), pin=[0.3, 2.3],
          cams=[push([-1700, 120, -1500], [-1300, 100, -1420], [-480, 20, -1300], 4.5, fov=42), line('MAIN', 300, 520, 55, 4.0, look=160, dip=45, fov=46), push([-750, 80, -1150], [-700, 70, -1180], [-430, 0, -1330], fov=44)],
          fleet=dict(n=12, center=[-1300, -1550], axis=170, spacing=150, kind='line', heading=80), smoke=[dict(at=[e, 12, n], n=10, size=34, rise=60, drift=[-2.5, 1], period=0.11, seed=40 + i, alpha=0.8) for i, (e, n) in enumerate([(-470, -1420), (-420, -1250), (-450, -1080), (-380, -1500)])],
          life=dict(walkers=[dict(line=SOUTH, n=60, width=8, colors=CIV, free=False)], birds=dict(c=[-430, -1300], r=200, h=90, n=10))),
 '2j': T3(year=1782.69, date=[1782, 9, 8, 7, 8], counter={'s': '8 Sep 1782'}, noi='thanh_pho', town='1782', tech=dict(v6=dict(earth=True)),
          cams=[push([-640, 60, -1190], [-620, 56, -1180], [-480, 0, -1160], 4.5, fov=42), lat([-575, 10, -1240], 180, 160, 180, 26, 4.0, fov=36), push([-800, 40, -1300], [-760, 36, -1290], [-602, 6, -1276], fov=38)],
          units=[dict(at=[GP[0] + de, GP[1] + dn], heading=270, rows=5, cols=24, side='gb', day=[0, 99], seed=21 + i) for i, (de, dn) in enumerate([(-16, -24), (16, -24), (-16, 24), (16, 24)])],
          life=dict(walkers=[dict(line='MAIN', n=110, width=4, colors=GB1782), dict(line='GPR', n=60, width=5, colors=GB1782)], birds=dict(c=[-500, -1200], r=150, h=60, n=12), chimney=18),
          smoke=[dict(at=[-600, 14, -1276], n=12, size=36, rise=55, drift=[-3, 1], period=0.1, seed=11, alpha=0.75), dict(at=[-585, 12, -1500], n=8, size=30, rise=45, drift=[-3, 1], period=0.12, seed=12, alpha=0.7)]),
 '2o': T3(year=1782.5, date=[1782, 7, 15, 10, 11], noi='ham', counter={'s': 'Jul 1782'}, linea=True,
          cams=[push([300, 70, 700], [280, 80, 300], [250, -40, -850], 4.5, fov=40), push([180, 90, 100], [190, 95, -60], [240, -20, -850], 4.0, fov=34), lat([250, -30, -850], -90, 700, 400, 120, None, fov=30)],
           ghi='M11 mặt cắt hầm CHƯA có trong máy dựng — animatic dùng mặt ngoài vách bắc (vị trí hầm) — đề xuất'),
 '2q': T3(year=1783.1, date=[1783, 2, 5, 11, 12], counter={'s': '5 Feb 1783'}, noi='eo_dat', linea=True, cams=[lat([0, 0, 1050], -90, 700, 900, 140, 5.5, fov=34), push([-200, 300, 200], [-150, 280, 350], [200, 0, 1080], fov=42)],
          units=[dict(at=[e, 1120], heading=180, rows=3, cols=16, side='es', day=[0, 99], seed=50 + i) for i, e in enumerate([-200, 150, 450])]),
 '3a': T3(year=1783.5, yearAt=[[0, 1783.5], [6.0, 1805]], date=[1790, 6, 1, 10, 11], noi='eo_dat', linea=True, cams=[top([40, 0, 520], 1000, 1300, 6.0, 0, 10), lat([0, 0, 520], 90, 1100, 900, 300, fov=36)]),
 '3b': T3(year=1810.1, date=[1810, 2, 14, 10, 11], noi='eo_dat', linea=True, pin=[0.5, 2.5], cams=[push([-900, 200, 400], [-800, 190, 600], [-300, 0, 1050], 5.0, fov=42), push([1200, 200, 500], [1100, 190, 650], [600, 0, 1060], fov=42)],
          smoke=[dict(at=[-380, 8, 1030], n=22, size=60, rise=110, drift=[-2, 1], period=0.07, seed=21, alpha=0.9), dict(at=[640, 8, 1080], n=20, size=55, rise=100, drift=[-2, 1], period=0.07, seed=22, alpha=0.9)]),
 '3d': T3(year=1849, yearAt=[[0, 1849], [3.4, 1870], [6.7, 1905]], date=[1870, 6, 15, 10, 11], noi='thanh_pho', cams=[push([-500, 300, 900], [-400, 280, 1100], [300, 0, 2000], 5.0, fov=44), push([700, 260, 900], [620, 240, 1050], [100, 0, 2100], fov=44)],
          life=dict(walkers=[dict(line=LL_REAL, n=50, width=5, colors=CIV, free=False)])),
 'KC1910': T3(year=1910, date=[1910, 6, 15, 10, 11.5], noi='thanh_pho', cams=[neo(150, 1340, 2.6, 12, fov=40)], neo=True,
          life=dict(walkers=[dict(line=LL_REAL, n=60, width=7, colors=CIV, free=False)], crowds=[dict(line=LL_REAL, groups=6, size=[3, 8], speed=0.8, colors=CIV)], birds=dict(c=[160, 1500], r=80, h=30, n=8))),
 '3f': T3(year=1900, yearAt=[[0, 1900], [5.5, 1908.6], [10.5, 1910]], date=[1909, 6, 15, 10, 11], noi='thanh_pho', pin=[5.5, 7.5],
          cams=[push([-300, 90, 900], [-260, 85, 760], [100, 0, 300], 5.5, fov=42), lat([60, 0, 420], -90, 260, 400, 60, 5.0, fov=34), push([400, 120, 800], [360, 110, 680], [0, 0, 380], fov=40)],
          front=[dict(pts=[[-290, 395], [-100, 404], [100, 405], [300, 406], [520, 408]], side='gb', grow=[5.6, 7.4], w=4)],
          life=dict(walkers=[dict(line=LL_REAL, n=40, width=5, colors=CIV, free=False)])),
 '3h': T3(year=1920, yearAt=[[0, 1920], [5.0, 1938.5]], date=[1938, 6, 15, 10, 11], noi='eo_dat', cams=[top([0, 0, 150], 900, 1150, 5.0, 0, 8), lat([0, 0, 100], 0, 700, 800, 160, fov=36)]),
 '4c': T3(year=1941.5, yearAt=[[0, 1941.5], [4.5, 1943.5]], date=[1943, 6, 15, 10, 11], noi='eo_dat', cams=[lat([-700, 0, 0], 90, 900, 700, 220, 4.5, fov=36), push([-1500, 300, -600], [-1350, 280, -450], [-500, 0, 0], fov=42)],
          life=dict(boats=[dict(pts=[[-1400, -700], [-1200, -300], [-1100, 300]], len=10, speed=4, s0=0.1)])),
 '4d': T3(year=1943, date=[1943, 6, 15, 10, 11], noi='ham', town='1943', cams=[push([400, 120, 800], [360, 130, 400], [260, -40, -900], 5.5, fov=40), lat([200, -30, -850], -70, 750, 500, 140, fov=32)],
          life=dict(walkers=[dict(line='WCA', n=30, width=5, women=False, colors=MIL43)]), ghi='M11 mặt cắt khối Rock CHƯA có — animatic dùng mặt ngoài + đá thải ra đường băng — đề xuất'),
 '4g': T3(year=1940.4, date=[1940, 5, 22, 10, 11], noi='bien', ships=False, cams=[lat([-1500, 0, -1300], 200, 1900, 1500, 220, fov=34)],
          fleet=dict(n=6, center=[-1600, -1400], axis=200, spacing=320, kind='line', heading=200), life=dict(boats=[dict(pts=[[-900, -1200], [-1500, -1500], [-2400, -2000]], len=14, speed=5, s0=0.2)])),
 '4i': T3(year=1942.85, date=[1942, 11, 7, 15, 16], noi='eo_dat', cams=[lat([-200, 0, 0], 0, 380, 500, 80, 5.5, fov=34), lat([300, 0, 0], 180, 380, 500, 80, 5.5, fov=34), push([-1300, 240, -300], [-1150, 220, -200], [300, 0, 0], fov=40)],
          life=dict(walkers=[dict(line='WCA', n=60, width=8, women=False, colors=MIL43)]), ghi='máy bay 1942 chưa có mô hình — animatic: đường băng + người; đề xuất khối máy bay có nguồn'),
 '5a': T3(year=1969.45, date=[1969, 6, 9, 10, 11], counter={'s': 'Jun 1969'}, noi='thanh_pho', cams=[push([0, 30, -200], [10, 28, 120], [61, 2, 479], 5.0, fov=42), lat([61, 2, 470], 90, 160, 220, 25, 4.5, fov=34), push([400, 300, 1200], [350, 280, 1000], [61, 0, 470], fov=40)]),
 'KB2026': T3(year=2026, date=[2026, 10, 18, 11, 12], noi='thanh_pho', neo=True, cams=[neo(-459.6, -1139.9, 4.6, 281, fov=41.1)],
          life=dict(walkers=[dict(line='GPR', n=90, width=8), dict(line='MAIN', n=60, width=4)], crowds=[dict(line='GPR', groups=10, size=[3, 9], speed=0.8)], birds=dict(c=[-500, -1150], r=60, h=25, n=8))),
 '5c': T3(year=1985.1, yearAt=[[0, 1985.1], [4.0, 2026]], date=[2026, 10, 18, 8, 8.3], noi='thanh_pho', cams=[push([-120, 18, 260], [-100, 16, 150], [0, 2, -300], 4.0, fov=44), lat([0, 2, 20], 0, 60, 60, 4, fov=40)],
          life=dict(walkers=[dict(line='WCA', n=140, width=7)], crowds=[dict(line='WCA', groups=12, size=[5, 14], speed=1.2)])),
 '5d': T3(year=2026, date=[2026, 10, 18, 10, 10.2], noi='thanh_pho', cams=[push([61, 20, 460], [100, 60, 700], [220, 0, 1700], fov=44)], life=dict(walkers=[dict(line=LL_REAL, n=50, width=6, free=False)])),
 'KC2026': T3(year=2026, date=[2026, 10, 18, 10, 11.5], noi='thanh_pho', neo=True, cams=[neo(150, 1340, 2.6, 12, fov=40)],
          life=dict(walkers=[dict(line=LL_REAL, n=60, width=7, free=False)], crowds=[dict(line=LL_REAL, groups=5, size=[3, 7], speed=0.8)], birds=dict(c=[160, 1500], r=80, h=30, n=8))),
 '5f': T3(year=1960, yearAt=[[0, 1960], [5.5, 1990], [11.0, 2026]], date=[2026, 10, 18, 10, 11], noi='eo_dat', ribbons=True,
          cams=[line('BORDER', 0, 260, 95, 5.5, look=180, dip=70, fov=36, typ='eo_dat'), line('BORDER', 260, 520, 95, 5.5, look=180, dip=70, fov=36, typ='eo_dat'), push([400, 260, 900], [360, 240, 800], [60, 0, 400], fov=40)],
          life=LIFE_WCA(80)),
 '5h': T3(year=2026, date=[2026, 10, 18, 11, 12], noi='thanh_pho', cams=[orbit([GATE[0], 5, GATE[1]], 130, 40, 230, 280, 5.5), orbit([GATE[0], 5, GATE[1]], 130, 40, 280, 330, 5.5), push([GATE[0] + 300, 120, GATE[1] + 260], [GATE[0] + 240, 100, GATE[1] + 200], [GATE[0], 0, GATE[1]], fov=40)],
          life=LIFE_WCA(120), ghi='hàng rào cũ/mới 2026 chưa có mô hình (C03) — đề xuất'),
 '5j': era_push([dict(d=3.7, year=1704.6, town='1704', hideTrees=OLDBOX), dict(d=3.7, year=1735, linea=True), dict(d=3.7, year=1910, front=[dict(pts=[[-290, 395], [100, 405], [520, 408]], side='gb', grow=[0, 0.1], w=4)]),
                dict(d=3.7, year=1943), dict(d=3.7, year=2026)], [-700, 450, -1500], [-1000, 1900, -2400], [0, 0, 300], fov=44, base=dict(noi='eo_dat', date=[2026, 10, 18, 16, 16.3])),
 'KA2026': T3(year=2026, date=[2026, 10, 18, 9, 17], dayCycle=True, noi='thanh_pho', neo=True, cams=[neo(-447.0, -1256.0, 3.4, 268.7, fov=43.6)],
          life=dict(walkers=[dict(line='MAIN', n=50, width=3)], birds=dict(c=[-430, -1300], r=40, h=20, n=6)), ghi='tư thế máy = khung neo PT2 k1782 (design/pt/scene/pt_site.py, hẻm K1782-09/10; bỏ dịch +6 m Đông của nắn 1782) trên phố 2026 OSM — bản sản xuất: nền PT 2026'),
 '5k': T3(year=2026, date=[2026, 10, 18, 16.55, 16.85], dayCycle=True, ghi='góc ngược 0a — cùng thay nắng chiều cho đêm (xem 0a)', noi='thanh_pho',
          cams=[push([40, 3, -260], [30, 3, -150], [61, 2, 479], 5.0, fov=46), lat([0, 2, 20], 180, 45, 30, 3, 5.0, fov=40), push([-60, 6, 240], [0, 10, 380], [61, 3, 600], 5.0, fov=44), push([61, 20, 300], [-100, 520, -500], [100, 0, 1200], fov=46)],
          life=dict(walkers=[dict(line='WCA', n=80, width=6)], crowds=[dict(line='WCA', groups=6, size=[4, 10], speed=1.2)], birds=dict(c=[0, 0], r=180, h=50, n=8))),
}
# cảnh V6 có sẵn (đường ống V6; gib20 bật tech.v6) — đoạn cắt theo khung
S3V6 = {
 '2m': [dict(hero='tl/vinh6', dur=14.0, f0=0, beats=[4.4, 5.9, 10.6, 12.0], ai_texture=True), dict(hero='tl/bo6', dur=6.0, f0=0, beats=[])],
 '4b': [dict(hero='tl/gib20', dur=15.0, f0=216, beats=[11.6 - 9, 16.6 - 9, 17.8 - 9, 21.0 - 9], tech=dict(v6={}), src_dur=24.5)],
}
# khung neo LAI (V6, 960×540, 9 s) — cắt bỏ dải chữ cũ (dưới) + hộp năm (phải dưới): khung 0..810 × 0..456 phóng lại 960×540
LAI = {'KA1782': 'reports/v6/khung-neo/v6-LAI-960x540-1782.mp4', 'KB1943': 'reports/v6/khung-neo/v6-LAI-960x540-1943.mp4'}

# ---------------- ảnh / tranh / bản đồ lịch sử (photo/print) ----------------
P = lambda f, focus=(0.5, 0.45), push=0.22, preset='push', **k: dict(img=f'/cache/g1b/{f}', focus=list(focus), push=push, preset=preset, **k)
PHOTO = {
 '0c': P('rijks_RP-P-OB-83.395_kaart_1704.jpg', (0.55, 0.5), 0.25, ghi='3D vùng tầm eo biển (hai lục địa) cần nền xa ngoài gói gib (Africa > 22 km) — animatic: bản đồ eo biển 1704 (Rijks, CC0)'),
 '0f': P('rijks_RP-P-OB-19.249_destruction_floating_batteries_1782.jpg', (0.5, 0.55), 0.3),
 '1b': P('rooke_rijks_33529.jpg', (0.5, 0.3), 0.2, preset='pull', ghi='Rooke (Rijks RP-P-OB-33.529, CC0); chân dung Hesse-Darmstadt chưa có tệp — thẻ tên ở bản sản xuất'),
 '1c': P('rijks_RP-P-OB-83.400_exact_plan_1705.jpg', (0.45, 0.5), 0.35),
 '1h': None, '2b': P('yale_2046612_faden_1783_spanish_works.jpg', (0.5, 0.5), 0.3, preset='drift-r'),
 '2e': P('rijks_RP-P-OB-53.323_eliott_portrait_1784.jpg', (0.5, 0.32), 0.2, preset='pull'),
 '2h': P('ia_historyoflatesie00drin_leaf373_drinkwater1786_plan_batteries_13sep1782.jpg', (0.62, 0.58), 0.55, preset='detail', ghi='phố sau bắn phá: chi tiết chữ "THE RUINS OF GIBRALTAR" trên plan Drinkwater (PD)'),
 '2k': P('ia_historyoflatesie00drin_leaf87_drinkwater1786_plan_bay.jpg', (0.5, 0.5), 0.25, preset='drift-l'),
 '2l': P('met_10547.jpg', (0.5, 0.45), 0.25, ghi="chưa có chân dung d'Arçon PD — phác thảo Copley người trên pin nổi (Met, CC0)"),
 '2r': None, '3c': P('ia_historyofgibralt00saye_leaf500_sayer1865_plan_rock_town_territory.jpg', (0.5, 0.35), 0.35, preset='tilt-low'),
 '3e': P('loc_2025710366_neutral_ground.jpg', (0.5, 0.5), 0.2, preset='drift-r'), '3g': P('loc_2020680546_northtown1905.jpg', (0.25, 0.5), 0.2, preset='drift-l', ghi='stereograph: dùng nửa trái'),
 '4a': P('nara_204918839_342-FH_000761.jpg', (0.5, 0.5), 0.2, preset='pull'), '4f': P('pu_ams_m981_gibraltar_1943.jpg', (0.45, 0.4), 0.35, preset='tilt-low'),
 '4h': None, '5g': None, '2p': P('rijks_RP-F-2001-7-257-1_rock_from_fort_san_felipe_1860.jpg', (0.5, 0.4), 0.25, preset='detail', ghi='footage hầm hôm nay chưa có clip giấy phép → ảnh 1860 vách bắc (Rijks CC0) — đề xuất'),
}
# hồ sơ văn bản (không có ảnh tài liệu trong repo) → thẻ trích nguyên văn trên nền bản đồ/ảnh liên quan
DOC = {
 '1h': dict(bg='rijks_RP-P-2018-1131_plan_1733.jpg', q='"…without any territorial jurisdiction, and without any open communication by land…"', by='Treaty of Utrecht, Article X (1713)'),
 '2r': dict(bg='rijks_RP-P-OB-70.560_emes_scene_14sep1782.jpg', q='Spain recovers Minorca and the Floridas; Gibraltar stays British.', by='Peace of Versailles, 3 September 1783'),
 '4h': dict(bg='pu_ams_m981_lalinea_1943.jpg', q='«una porción usurpada del territorio nacional» — "a usurped portion of the national territory"', by='Spanish government, 4 Mar 1939 (Marquina Barrio, 1981)'),
 '5g': dict(bg='rijks_RP-F-2001-7-257-16_neutral_ground_1860.jpg', q='Nothing in the treaty changes either side\'s position on sovereignty.', by='UK–EU treaty on Gibraltar, July 2026 (paraphrase of the sovereignty clause)'),
}
# thẻ số (p.card) — nội dung = câu lời + claim; nguồn ngắn ở p.so ≤ 3 s
CARD = {
 '0d': dict(type='num', big='14', unit='sieges · 1309–1783', src='Sayer 1862 · García Sanz 2022 · Gibraltar National Museum'),
 '1f': dict(type='split', title='Defenders, 1704', L=('~100 soldiers', 'Spanish count (Montero)'), R=('up to 500', 'British accounts, incl. armed townsmen')),
 '2d': dict(type='list', title='January 1780', items=['Thistles, dandelions, wild leeks', 'One egg: sixpence'], src='Garrison diaries (Drinkwater)'),
 '2i': dict(type='split', title='Rounds fired (from April 1781)', L=('205,328', 'garrison'), R=('258,387', 'besiegers'), src='Drinkwater, 1785'),
 '2n': dict(type='list', title='13–14 September 1782', items=['> 2,000 attackers lost, prisoners included', '357 rescued by the British', 'Garrison: 16 killed'], src='British estimate & Montero · British return'),
 '4e': dict(type='num', big='~55 km', unit='of tunnels — more than the roads above', src='HM Government of Gibraltar, 2017'),
 '5b': dict(type='num', big='~4,600', unit='Spanish day workers cut off, 1969', src='C19 (UK record)'),
 '5e': dict(type='num', big='£85,000', unit='output per resident (Gibraltar government)', src='HM Government of Gibraltar'),
 '5i': dict(type='timeline', title='As of 18 October 2026', items=[('Jul 2026', 'treaty signed · checks end'), ('now', 'in force provisionally'), ('14 Dec 2026', 'European Parliament vote indicated')]),
}
SM_IDS = ['SM1', 'SM2', 'SM3']

# ---------------- dựng đặc tả ----------------
def main():
    heroes, segs, log, cutplan, srt = {}, [], [], {}, []
    t_abs = 0.0; prev3d = None; place_prev = None
    for s in TR:
        sid, d = s['id'], float(s['dur']); kc = KC[sid]; sc = SCRIPT.get(sid, {'say': '', 'tren_hinh': []})
        seg = dict(id=sid, part=f"CH{s['ch']}", chuong=str(s['ch']), dur=round(d, 4), fadeIn=6 if sid == TR[0]['id'] else 0, fadeOut=8 if sid == TR[-1]['id'] else 0, beats=[dict(t=0.0, k='cut', s=sid)], shots=[])
        L = dict(shot=sid, loai=s['loai'], noi=s.get('noi'), moc=s.get('moc_nam'), claims=s.get('claims', []), nguon=s.get('du_lieu_nha') or None, bac=None, ai_image=bool(s.get('ai_image')), ai_texture=False, chu_tat=[], ghi=None)
        where = None
        # chip nơi: khi vào nơi mới (vung khác shot trước, chỉ shot địa lý)
        place = s.get('vung') if s['loai'] in ('3D phố', '3D vùng', 'bản đồ lịch sử') else None
        WHERE = {'cong-bien-gioi': 'Gibraltar–La Línea frontier', 'eo-dat': 'The isthmus, Gibraltar', 'vinh': 'Bay of Gibraltar', 'pho-co': 'Gibraltar old town', 'giao-lo-1941': 'Runway crossing, Gibraltar',
                 'north-front': 'North Front, Gibraltar', 'la-linea': 'La Línea de la Concepción', 'vach-bac': 'North face of the Rock', 'neo-hem-k09': 'Gibraltar old town', 'ham-wwii': 'Inside the Rock'}
        if place and place != place_prev: where = WHERE.get(place) or None
        if place: place_prev = place
        # số/câu trích (≤ 3 s) khi lời nói tới: câu chứa trích bắt đầu ở mốc từ tương ứng
        so = []
        t_say0 = kc.get('bat_dau_tre_s', 0.0)
        sents = sentences(sc['say']); wsum = sum(len(speak_words(x)) for x in sents) or 1; k_w = (kc['uoc_s'] * WPS) / wsum
        def t_of(i): return t_say0 + sum(len(speak_words(x)) for x in sents[:i]) * k_w / WPS
        for th in sc['tren_hinh']:
            if th.startswith('(0b–0e)'): L['chu_tat'].append('bối cảnh giáo dục trên hình (0b–0e) — §12.1 bỏ; lời 0e vẫn nói'); continue
            m = re.match(r'^(?:\(\w+\)\s*)?(?:thẻ(?: số)?:?\s*)?(.*)$', th); body = m.group(1)
            src = None; mm = re.match(r'^([^:«"]{3,90}?):\s*(.*)$', body)
            if mm and ('«' in mm.group(2) or '"' in mm.group(2)): src, body = mm.group(1).strip(), mm.group(2).strip()
            # chọn câu lời gần nhất có chung từ khoá
            kw = set(w.lower() for w in speak_words(body) if len(w) > 4)
            best = max(range(len(sents)), key=lambda i: len(kw & set(w.lower() for w in speak_words(sents[i])))) if sents else 0
            dub = [q.strip() for q in re.findall(r'"([^"]+)"', body)]; orig = re.findall(r'«([^»]+)»', body)
            txt = (f'«{orig[0]}»' if orig else (dub[0] if dub else body)); sub = dub[0] if orig and dub else None
            if sid in CARD: continue   # thẻ số tự mang số; trích của thẻ ghi trong log
            so.append(dict(s=txt[:150], sub=(sub or '')[:150] or None, src=src, at=round(min(d - 1.0, max(0.2, t_of(best))), 2), dur=3.0))
        # ---------------- loại shot ----------------
        sh = dict(tpl='plate', at=0, noi={'ham': 'vung'}.get(s.get('noi'), s.get('noi')) or 'vung', p=dict(sach=True))   # 'ham' (hầm) chưa là nơi hợp lệ của prep — animatic dựng mặt ngoài vách bắc
        if where: sh['p'].update(where=where, where_moi=True)
        if so: sh['p']['so'] = so
        if sid in S3 or sid in S3V6:
            sh['type'] = 'scene3d'
            parts = S3V6.get(sid) or (S3[sid] if isinstance(S3[sid], list) else [S3[sid]])
            t = 0.0; first = None
            for j, pt in enumerate(parts):
                key = f'g1b_{sid}_{j}'.replace('-', '_')
                if 'hero' in pt:   # cảnh V6 có sẵn
                    heroes[key] = dict(hero=pt['hero'], opt=dict(pack='gib', cau=f'g1b-{sid}-{j}', **({'tech': pt['tech']} if pt.get('tech') else {})))
                    pd = pt['dur']; f0 = pt.get('f0', 0); heroes[key]['dur'] = (pt.get('src_dur') or pd + f0 / 24)
                    for b in pt.get('beats', []): seg['beats'].append(dict(t=round(t + b, 3), k='cut' if b == pt['beats'][0] else 'phase', s=f'{sid} pha'))
                    if pt.get('ai_texture'): L['ai_texture'] = True; L['chu_tat'].append('nhãn AI (HC7) — §12.1 tắt trên hình, giữ ai_texture trong log')
                    one = dict(sh, at=round(t, 4)); one['p'] = dict(sh['p'], hero=key, frame0=f0); one['p'].pop('so', None) if j else None
                else:
                    o = dict(pt['opt']); o.update(pack='gib', shot=sid, cau=f'g1b-{sid}-{j}')
                    pd = o['dur'] if 'dur' in o else d; o['dur'] = round(pd, 4)
                    if s.get('ai_image'): L['ai_image'] = True
                    ghi = o.pop('ghi', None); L['ghi'] = (L['ghi'] + ' · ' if L['ghi'] else '') + ghi if ghi else L['ghi']
                    # mỗi cú ≤ 6 s (Q37): cú không khai dur chia phần còn lại
                    cams = o['cams']; fixed = sum(c['dur'] or 0 for c in cams); free = [c for c in cams if not c['dur']]
                    for c in free: c['dur'] = round((pd - fixed) / len(free), 4)
                    for c in cams:
                        if c['dur'] > 6.0 + 1e-6 and not o.get('neo'): raise SystemExit(f'{sid}: cú {c["k"]} {c["dur"]} s > 6 s (Q37)')
                    tt = t
                    for c in cams[:-1]: tt += c['dur']; seg['beats'].append(dict(t=round(tt, 3), k='cut', s=f'{sid} cú'))
                    heroes[key] = dict(hero='tl/t3s', opt=o, dur=round(pd, 4))
                    one = dict(sh, at=round(t, 4)); one['p'] = dict(sh['p'], hero=key, frame0=0)
                    if j: one['p'].pop('so', None); one['p'].pop('where', None)
                    if j: seg['beats'].append(dict(t=round(t, 3), k='cut', s=f'{sid} mốc'))
                if j: seg['beats'].append(dict(t=round(t, 3), k='cut', s=f'{sid} cảnh {j}'))
                one['ai_texture'] = bool(pt.get('ai_texture')); seg['shots'].append(one); t += pd
                if first is None: first = key
            prev3d = first; cutplan[sid] = [b['t'] for b in seg['beats']]
            L['bac'] = 'bậc 1 (bố cục: bản đồ/ghost có nguồn) + bậc 5 (vật nền phụ) · người/quân: minh hoạ số lượng (bậc 2 khi có mục AI đọc nguồn)'
        elif sid in LAI:
            key = f'g1b_{sid}'; heroes[key] = dict(hero='footage/lai', opt=dict(file=str(REPO / LAI[sid]), crop='810:456:0:0', frame=False, ss=0, pts=0.85), dur=d)
            sh['type'] = 'scene3d'; sh['khung_neo'] = True; sh['ai_image'] = True; sh['p'].update(hero=key, frame0=0)
            seg['shots'].append(sh); L.update(ai_image=True, nguon='khung neo V6 bản LAI 540p (reports/v6/khung-neo) — cắt bỏ chữ cũ; chậm 0,85× để đủ thời lượng (clip 9 s < 10,3 s cần cho đoạn) — chỉ animatic', chu_tat=L['chu_tat'] + ['dòng nguồn + nhãn AI (đã nung trong bản LAI) — cắt khỏi khung'])
            L['bac'] = 'bậc 1 (ghost Drinkwater/AMS) + bậc 3–4 (quân phục RIGHTS-V6) + AI tấm C (ai_image)'
        elif sid in PHOTO or sid in DOC:
            if PHOTO.get(sid):
                ph = dict(PHOTO[sid]); ghi = ph.pop('ghi', None); L['ghi'] = ghi; key = f'g1b_{sid}'
                heroes[key] = dict(hero='photo/print', opt=ph, dur=d); sh['type'] = 'photo'; sh['p'].update(hero=key, frame0=0, photo=os.path.basename(ph['img']))
                seg['shots'].append(sh); L['nguon'] = os.path.basename(ph['img'])
            else:
                D = DOC[sid]; key = f'g1b_{sid}'; heroes[key] = dict(hero='photo/print', opt=P(D['bg'], (0.5, 0.5), 0.15, preset='drift-l'), dur=d)
                sh['type'] = 'card'; sh['p'].update(hero=key, frame0=0, card=dict(type='quote', q=D['q'], by=D['by'], at=0.3)); sh['p']['so'] = [dict(s=D['by'], at=round(d / 3, 2), dur=3.0, role='src_ngan', x='left', y='bottom')]
                seg['shots'].append(sh); L['nguon'] = D['by']; L['ghi'] = 'ảnh văn bản gốc chưa có trong repo → thẻ trích nguyên văn (by = nguồn) trên nền tư liệu liên quan — đề xuất'
            L['bac'] = 'tư liệu thời đó (bậc 1/4) — Ken Burns'
        elif sid in CARD:
            C = dict(CARD[sid]); src = C.pop('src', None); ty = C.pop('type')
            if ty == 'num': card = dict(type='num', big=C['big'], unit=C['unit'], at=0.3)
            elif ty == 'split': card = dict(type='list', title=C['title'], items=[dict(s=f"{C['L'][0]} — {C['L'][1]}", at=0.3), dict(s=f"{C['R'][0]} — {C['R'][1]}", at=1.6)])
            elif ty == 'list': card = dict(type='list', title=C['title'], items=[dict(s=x, at=0.3 + 1.2 * i) for i, x in enumerate(C['items'])])
            else: card = dict(type='list', title=C['title'], items=[dict(s=f'{a} — {b}', at=0.3 + 1.4 * i) for i, (a, b) in enumerate(C['items'])])
            bg = prev3d or 'g1b_0b_0'
            sh['type'] = 'card'; sh['p'].update(hero=bg, frame0=0, speed=0.0, off=0, card=card)
            if src: sh['p']['so'] = [dict(s=src, at=round(max(0.8, min(d - 3.2, d / 2 - 1.2)), 2), dur=3.0, role='src_ngan', x='left', y='bottom')]
            seg['shots'].append(sh); L['nguon'] = src; L['bac'] = 'văn bản/sổ thời đó (bậc 2) hoặc nguồn hiện đại có tên'
        elif sid in SM_IDS:
            fr = HERE / 'sm' / f'{sid}.yaml'
            import yaml; Y = yaml.safe_load(fr.read_text()) if fr.exists() else None
            if Y and ('shot' in Y or 'shots' in Y) and 'heroes' in Y:
                heroes.update(Y['heroes']); SMS = Y.get('shots') or [dict(Y['shot'], at=0)]
                for sm in SMS:
                    sm.setdefault('p', {})['sach'] = True; seg['shots'].append(sm)
                    if sm.get('at'): seg['beats'].append(dict(t=round(float(sm['at']), 3), k='cut', s=f'{sid} b'))
                    for c in sm['p'].get('counter') or []: seg['beats'].append(dict(t=round(float(sm.get('at', 0)) + float(c['t']), 3), k='dem', s=str(c.get('s'))[:20]))
                if False: L['nguon'] = 'g1b/sm/' + fr.name; L['bac'] = 'bậc 1 (ranh Cliopatria/OHM; tuyến claim T…)'
            else:
                bg = prev3d or 'g1b_0b_0'; sh['type'] = 'card'; sh['p'].update(hero=bg, frame0=0, speed=0.0, card=dict(type='end', lines=[dict(s=f'{sid} — strategic map', px=56, at=0.2), dict(s='(rendering)', px=40, at=0.4)]))
                seg['shots'].append(sh); L['ghi'] = 'bản đồ chiến lược chưa có tệp phiên con → thẻ chờ'
        else:
            raise SystemExit(f'shot {sid} ({s["loai"]}) chưa có đặc tả')
        # ray lời (phụ đề tạm)
        if sc['say']:
            for i, x in enumerate(sents):
                a = t_abs + t_of(i); b = t_abs + t_of(i + 1)
                srt.append((a, b, x))
        # biến cố thật (Q37): số/câu trích hiện, mục thẻ hiện, chip nơi — khai beat (không thêm phần tử: chỉ ghi biến cố đã có trên hình)
        for sh2 in seg['shots']:
            pp = sh2.get('p', {})
            for q in pp.get('so', []) or []: seg['beats'].append(dict(t=round(q['at'], 3), k='so', s=(q.get('s') or '')[:30]))
            for it in ((pp.get('card') or {}).get('items') or []): seg['beats'].append(dict(t=round(it['at'], 3), k='the', s=str(it.get('s', ''))[:30]))
        seg['beats'] = sorted({round(b['t'], 2): b for b in seg['beats'] if b['t'] < d - 0.2}.values(), key=lambda b: b['t'])
        L['bien_co'] = [b['t'] for b in seg['beats']]; gaps = [b - a for a, b in zip(L['bien_co'], L['bien_co'][1:] + [d])]; L['khoang_max_s'] = round(max(gaps), 2)
        # khai cho bộ kiểm (đúng nội dung đã dựng, không thêm phần tử): ML1 cau/claim · Q26b-K2 vung · NC-H1 lớp nhà (city/ghost) · FT1 lý do tư liệu · BD-1(e) strategic
        cau0 = sents[0] if sents else None
        nxt = TR[TR.index(s) + 1]['id'] if TR.index(s) + 1 < len(TR) else None
        for sh2 in seg['shots']:
            pp = sh2.setdefault('p', {})
            if cau0: sh2['cau'] = pp['cau'] = cau0
            elif s.get('claims'): sh2['claim'] = pp['claim'] = s['claims'][0]
            sh2['vung'] = s.get('vung')
            hz = heroes.get(pp.get('hero')) or {}
            if s.get('noi') == 'thanh_pho' and str(hz.get('hero', '')).startswith('tl/'):
                pp['city'] = True; tw = (hz.get('opt') or {}).get('town')
                if tw: pp['ghost'] = {'1782': 'ghost-1782', '1704': 'ghost-1704', '1943': 'ghost-1943'}[tw]
            if sid in LAI: pp['city'] = True
            if sh2.get('type') in ('photo', 'footage') or sid in LAI: sh2['ly_do'] = pp['ly_do'] = (s.get('mo_ta') or s['loai'])[:160]
            if sh2.get('type') == 'strategic':
                cam = (hz.get('opt') or {}).get('cam') or [{}]; sh2.setdefault('nghieng', max(c.get('tilt', 0) for c in cam)); sh2.setdefault('be_ngang_km', s.get('khung_rong_km')); sh2.setdefault('chi_toi', nxt)
        log.append(L); segs.append(seg); t_abs += d
    # thẻ phương pháp cuối (4,5 s) — "How this film was made" (§12.1 b)
    TP = EP / 'phat-hanh/the-phuong-phap.json'
    lines = json.loads(TP.read_text())['dong'] if TP.exists() else ['Main sources: Drinkwater 1786 siege plan; Spanish and British histories.', 'Estimated: 1782 house heights, ruined blocks, crowd numbers.', 'AI: surface detail on marked street frames; source reading, checked word for word.', 'AI images carry C2PA, so YouTube labels this video as AI-altered.']
    bgk = 'g1b_5k_0'
    segs.append(dict(id='PP', part='END', chuong='5', dur=5.0, fadeIn=0, fadeOut=10, beats=[dict(t=0.0, k='cut', s='How this film was made')],
                     shots=[dict(tpl='plate', at=0, type='card', p=dict(sach=True, hero=bgk, frame0=0, speed=0.0, card=dict(type='list', title='How this film was made', px=40, gap=30, items=[dict(s=x, at=0.2 + 0.35 * i) for i, x in enumerate(lines)])))]))
    segs[-2]['fadeOut'] = 0
    log.append(dict(shot='PP', loai='thẻ phương pháp', nguon='phat-hanh/the-phuong-phap.json', ghi='5 s (trần §12.1); ngoài 721,2 s của bảng shot'))
    E = dict(id='k2c-t3-g1b', title='Why Gibraltar Was Besieged 14 Times — G1b animatic (540p, temporary narration rail)', brand='MOVING PARTS', channel='k2', out=OUT,
             music=[dict(file='assets/k2/music/Tyrant.mp3', **{'from': '0a'}, ss=2.55, gain_db=-6)], sources={}, numbers={}, khung_sach=True, heroes=heroes, segments=segs)
    # ảnh/tranh/bản đồ/văn bản > 6 s: máy Ken Burns HAI CHẶNG (tiến về điểm chính → trôi ngang lộ chi tiết thứ hai), đổi hướng ở giữa = biến cố thật (Q37 dài nhất ≤ 6 s)
    seg_by = {x['id']: x for x in segs}
    for k, h in heroes.items():
        if h['hero'] != 'photo/print' or h['dur'] <= 6.0: continue
        sid = k[4:]; sg = seg_by.get(sid)
        if not sg: continue
        h['opt']['_hai_chang'] = True; tm = round(h['dur'] / 2, 2)
        sg['beats'] = sorted(sg['beats'] + [dict(t=tm, k='phase', s=f'{sid} máy đổi hướng')], key=lambda b: b['t'])
        for L in log:
            if L['shot'] == sid: L['bien_co'] = sorted(set(L.get('bien_co', []) + [tm])); g2 = [b - a for a, b in zip(L['bien_co'], L['bien_co'][1:] + [h['dur']])]; L['khoang_max_s'] = round(max(g2), 2)
    # chống lặp góc máy (prep.py: cùng scene_id + camera_id ≤ 2/tập): photo/print vượt 2 lần cùng preset → máy Ken Burns khai trực tiếp (o.cam, công thức kenburns() của photo.js) theo điểm chính riêng của shot
    from PIL import Image
    used = {}
    for k, h in heroes.items():
        if h['hero'] != 'photo/print': continue
        o = h['opt']; pr = o.get('preset', 'push'); used[pr] = used.get(pr, 0) + 1
        if used[pr] <= 2 and not o.get('_hai_chang'): continue
        im = Image.open('/var/tmp/cine-out/k2v-cache/g1b/' + os.path.basename(o['img'])); ar = im.width / im.height; ph = o.get('h', 2.6); pw = ph * ar; mh = ph + 0.62
        ix = sum(used.values()) - 1; fx, fz = (o['focus'][0] - 0.5) * pw, (o['focus'][1] - 0.5) * ph; mm = [40, 58, 85][(ix // 10) % 3]; fov = 2 * math.atan(12 / mm); dist = (mh * 0.62) / math.tan(fov / 2); tilt = 0.32; pu = o.get('push', 0.2); dd = h['dur']
        k0 = dict(t=0, p=[-0.12, dist * math.cos(tilt), dist * math.sin(tilt)], l=[0, 0, 0], mm=mm); d1 = dist * (1 - pu)
        k1 = dict(t=dd, p=[fx * 0.5 + 0.1, d1 * math.cos(tilt * 0.85), fz * 0.5 + d1 * math.sin(tilt * 0.85)], l=[fx * 0.55, 0, fz * 0.55], mm=mm)
        az = math.radians((ix % 10) * 36); rot = lambda q, c: [c[0] + (q[0] - c[0]) * math.cos(az) + (q[2] - c[2]) * math.sin(az), q[1], c[2] - (q[0] - c[0]) * math.sin(az) + (q[2] - c[2]) * math.cos(az)]
        k0['p'] = rot(k0['p'], k0['l']); k1['p'] = rot(k1['p'], k1['l'])   # xoay phương vị máy quanh điểm nhìn: mỗi shot một góc (cam_near: lệch ≥ 25°)
        if o.pop('_hai_chang', False):   # chặng 2: từ điểm chính trôi ngang 0,35 bề rộng bản in, giữ độ cao
            km = dict(k1); km['t'] = round(dd / 2, 3); k1 = dict(t=dd, p=[km['p'][0] + 0.35 * pw * math.cos(az), km['p'][1], km['p'][2] - 0.35 * pw * math.sin(az)], l=[km['l'][0] + 0.35 * pw, 0, km['l'][2]], mm=mm); keys = (k0, km, k1)
        else: keys = (k0, k1)
        o['cam'] = [{a: ([round(x, 4) for x in b] if isinstance(b, list) else b) for a, b in kk.items()} for kk in keys]; o.pop('preset', None)
    import yaml
    hdr = '# TỆP SINH TỰ ĐỘNG bởi g1b/mk_ep_g1b.py từ vay-ham/treatment.json + script-v4.1-KHOA.md (lời khoá v4.1, SHA LOI-KHOA.sha256). Đừng sửa tay.\n'
    (HERE / 'episode.yaml').write_text(hdr + yaml.safe_dump(E, allow_unicode=True, sort_keys=False, width=200))
    def ts(x): h, r = divmod(x, 3600); m, s2 = divmod(r, 60); return f'{int(h):02d}:{int(m):02d}:{s2:06.3f}'.replace('.', ',')
    (HERE / 'ray-loi.srt').write_text(''.join(f'{i + 1}\n{ts(a)} --> {ts(b)}\n{x}\n\n' for i, (a, b, x) in enumerate(srt)))
    (HERE / 'log-shot.json').write_text(json.dumps(log, ensure_ascii=False, indent=1) + '\n')
    (HERE / 'cut-plan.json').write_text(json.dumps(cutplan, ensure_ascii=False) + '\n')
    G = [x for L in log if 'khoang_max_s' in L for x in [L['khoang_max_s']]]; ev = sum(len(L.get('bien_co', [])) for L in log)
    print(f'biến cố khai {ev} · khoảng TB {sum(x["dur"] for x in segs) / max(1, ev):.2f} s · dài nhất {max(G):.2f} s (' + ', '.join(L['shot'] for L in log if L.get('khoang_max_s', 0) > 6) + ' > 6 s)')
    tot = sum(x['dur'] for x in segs)
    print(f'{len(segs)} đoạn, {len(heroes)} cảnh, tổng {tot:.2f} s (bảng shot {sum(float(s["dur"]) for s in TR):.2f} s + thẻ phương pháp 5 s), {len(srt)} dòng ray lời')

if __name__ == '__main__': main()
