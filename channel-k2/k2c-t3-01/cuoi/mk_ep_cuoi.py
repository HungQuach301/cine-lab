#!/opt/cine/bin/python
"""ANIMATIC-T3 (21/10/2026) · SINH ĐẶC TẢ ANIMATIC CẢ TẬP T3 Gibraltar — 43 shot (bảng 42 shot của reports/v7p/diem-may.md; KA2026 tách khỏi N5.5 thành khung neo riêng
để ghép cặp then/now với KA1782) + 2 thẻ phương pháp × 8 s. Look KHOÁ theo channel-k2/k2c-t3-01/LOOK-KHOA.md (chủ dự án 21/10/2026 07:05):
 LOOK-1 cách A (opt.nc + lightmap theo mốc) mọi cảnh · LOOK-2 khung lai (trời + sương 8–20 %, nhìn xuống 12–25°, một tiêu điểm) · LOOK-3 đêm lửa theo H2T
 LOOK-4 sửa: lều "bàn cờ" (campTuNhien), H1 mất Rock, C1 U1 nhìn thẳng xuống, C2 chỉ còn nước (máy E của V7B-a), C4 Bm2 nhìn thẳng xuống.
Thời lượng + mốc câu: reports/kl42/nhip-that.json (phương án B 745,0 s; lời khoá v4.2 SHA 51d1c773…). 9 shot mở đầu + vây hãm kế thừa V7C (v7p/mk_ep_v7c.py), sửa máy theo LOOK-4.
Cú lặn 13/9/1782: cắt sang clip GIỮ CHỖ reports/nc-gpu/lan/ncg-lan-xem.mp4 (đoạn 5,5 → 17,0 s) — bản cuối dựng Cycles GPU (G0).
Không AI trên hình (ai_image/ai_texture = false mọi shot).
Ra (thư mục này): episode.yaml, log-shot.json, anim-loi.json (đặt stem giọng), phu-de.srt (CHỈ bản kiểm), cut-plan.json, nhip-vat.json, bang-shot.json.
Dùng: /opt/cine/bin/python -I channel-k2/k2c-t3-01/animatic/mk_ep_anim.py [--out /var/tmp/cine-out/k2c-t3-anim] [--opt-dir <thư mục>]"""
import copy, importlib.util, json, math, random, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent; EP = HERE.parent; REPO = EP.parents[1]
sys.path.insert(0, str(REPO / 'scripts/k2tl')); import cuoi_bien_co as BC   # BAN-CUOI-T3
OUT = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else '/var/tmp/cine-out/k2c-t3-cuoi'
_s = importlib.util.spec_from_file_location('v7c', EP / 'v7p/mk_ep_v7c.py'); V7C = importlib.util.module_from_spec(_s); _a = sys.argv; sys.argv = ['v7c', '--nc', '1']; _s.loader.exec_module(V7C); sys.argv = _a
V7B, V7P = V7C.V7B, V7C.V7B.V7P
NH, dy, hAt = V7C.NH, V7C.dy, V7C.hAt
CIV, MOD, GB = V7P.CIV, V7P.MOD, V7P.GB
MIL43 = ['#6b6a4a', '#7a7656', '#2f3d5c', '#e7e0cf', '#6b6a4a']; ES1704 = ['#e7e0cf', '#c9a227', '#5e4a38', '#3d4a5a']
ORDER = json.loads((REPO / 'reports/kl42/nhip-that.json').read_text())['thu_tu_v42']

# ---------------- lightmap theo mốc (LOOK-KHOA §3.2) ----------------
FIRE82 = V7C.FIRE82
BK = {'1704': dict(dir='b1704', wY=[1300, 1779.0]), '1779': dict(dir='b1779', wY=[1779.0, 1781.278]), '1781r': dict(dir='b1781r', wY=[1781.278, 1782.5]),
      '1782': dict(dir='b1782', wY=[1782.5, 1783.6], fire=FIRE82), '1900': dict(dir='b1900', wY=[1783.6, 1938]), '1940': dict(dir='b1940', wY=[1938, 1946]), '2026': dict(dir='b2026', wY=[1946, 2030])}
def nc_for(o):
    """chọn lightmap theo dải năm của đường cong thời gian shot (mọi lightmap có cửa sổ giao dải năm)"""
    ys = [dy(k['at']) if isinstance(k['at'], str) else float(k['at']) for k in o['time']]; a, b = min(ys), max(ys)
    L = [BK[k] for k in BK if BK[k]['wY'][1] >= a and BK[k]['wY'][0] <= b]
    return dict(bakes=L or [BK['2026']])

def K(t, p, l, fov): return dict(t=round(t, 4), p=p, l=l, fov=fov)
def hold(p, l, fov, d, dp=(0, 0, 0)):
    """máy giữ + trôi chậm tuyến tính dp (m) suốt shot (TL-1 ≤ 2 %/s)"""
    return [K(0, list(p), list(l), fov), K(d, [p[0] + dp[0], p[1] + dp[1], p[2] + dp[2]], list(l), fov)]
def cuts(D, segs, giu=False):
    """ANIM-V2 (R3): shot chia góc — segs = [dict(t1 (bỏ ở góc cuối), p0, l0, [p1 | dp], [l1], fov)]; cắt cứng giữa các góc (khoá cuối góc trước ở t1 − 0,02 s). Trả (khoá máy, giây cắt trong shot)."""
    keys, ct, t0 = [], [], 0.0
    for i, g in enumerate(segs):
        t1 = D if i == len(segs) - 1 else g['t1']
        if i: ct.append(round(t0, 4))
        keys.append(K(t0, list(g['p0']), list(g['l0']), g['fov']))
        p1 = g.get('p1') or [g['p0'][k] + g.get('dp', (0, 0, 0))[k] for k in range(3)]
        if giu:   # BAN-CUOI-T3: khoá giữ sát hai đầu góc → tiếp tuyến Hermite không lấy theo góc kề (máy thấp cạnh máy cao 400 m vọt dưới đất — BAI-HOC #118a)
            f = lambda u: [g['p0'][k] + (p1[k] - g['p0'][k]) * u for k in range(3)]; a, b = t0 + 0.04, t1 - (0.06 if i < len(segs) - 1 else 0.04)
            keys.append(K(a, f(0.04 / (t1 - t0)), list(g.get('l1') or g['l0']) if False else list(g['l0']), g['fov'])); keys.append(K(b, f((b - t0) / (t1 - t0)), list(g.get('l1') or g['l0']), g['fov']))
        keys.append(K(t1 - (0.02 if i < len(segs) - 1 else 0.0), list(p1), list(g.get('l1') or g['l0']), g['fov']))
        t0 = t1
    return keys, ct
def A(E, agl, N): return [E, round(max(0.0, hAt(E, N)) + agl, 1), N]   # ANIM-V2: điểm theo độ cao trên mặt đất (máy thấp trên đồi)
def pitch(p, l): return math.degrees(math.atan2(p[1] - l[1], math.hypot(l[0] - p[0], l[2] - p[2])))
def neo_cam(E, N, agl, hd, d, fov=42, up=2.0):
    """khung neo tầm mắt (TL-2): máy cố định agl m trên mặt đất, hướng la bàn hd°, ngẩng up°"""
    h = max(0.0, hAt(E, N)) + agl; r = math.radians(hd); L = [E + 100 * math.sin(r), h + 100 * math.tan(math.radians(up)), N + 100 * math.cos(r)]
    return [K(0, [E, round(h, 1), N], [round(x, 1) for x in L], fov), K(d, [E, round(h, 1), N], [round(x, 1) for x in L], fov)]

def dur_of(ids): return round(sum(NH[i]['dur_moi'] for i in ids), 4)
H1_DAO = [('To walk in from Spain, you cross an airport runway.', 3.413, 6.269, 0.5),   # BAN-CUOI-T3 1c (V2-D3): đảo 3 câu đầu, cắt từ master giọng theo mốc câu (T3-loi-moc.json), không tạo giọng mới
          ('Since July 2026, this gate has had no routine checks.', 6.943, 11.285, 3.756),
          ('Midnight at the Gibraltar frontier.', 0.0, 2.148, 9.75)]
def lines_of(ids):
    out = []
    for i in ids:
        if i in ('0a', '0b'): continue
        for c in NH[i].get('cau', []): out.append(dict(dong=i, bd=round(c['bd_phim'], 3), kt=round(c['kt_phim'], 3), cau=c['khoa']))
    if '0a' in ids: out = [dict(dong=('0a' if 'Midnight' in c or 'To walk' in c else '0b'), bd=round(f, 3), kt=round(f + b - a, 3), cau=c) for c, a, b, f in H1_DAO] + out
    return out

# ---------------- mốc toạ độ (ENU m, gốc gói gib) ----------------
TOWER = [-130, -820]; KB, OB, OM = V7B.KB, V7B.OB, V7B.OM; GATE = [61, 479]
ISTH_N = [[-300, -600], [-120, -200], [0, 0], [40, 300], [70, 520], [110, 900], [160, 1400], [230, 2200], [320, 3200]]   # dòng người lên bắc 1704 (minh hoạ dọc eo đất — như G1b)
FT_SF, FT_SB = [-510, 1040], [915, 990]   # Fort San Felipe / Santa Bárbara (ghost SH fort1782 — bậc 1)
WORKS82 = [[-240, 455], [-120, 340], [20, 380], [180, 330], [330, 280], [520, 190]]   # tuyến song song tiền phương 1782 (lines1782_tp T1782-02…04 — bậc 1 thấp)
co_ld, co_lw = V7B.co_lau_dai, V7B.co_line_wall

def base(**kw):
    o = dict(rimPhe=['es'], bfile=V7B.BF, cityOpt=V7B.CITY); o.update(kw); return o

# ---------------- BAN-CUOI-T3 (1b, V2-D8): VẬT ĐỜI SỐNG CHUNG — bậc 5 ước lượng (design/k2v/tl/doisong.js); không công trình có tên; theo mốc năm ----------------
ROAD_EO = [[-150, -250], [-110, 120], [-60, 420], [10, 760], [70, 1060], [110, 1400]]          # lối đất băng eo đất (ước lượng)
ROAD_LL = [[60, 1100], [200, 1300], [380, 1500], [520, 1700]]                                     # lối ra mép La Línea (ước lượng)
DS_N31 = [dict(kind='duong', pts=ROAD_EO, w=4, wY=dict(on=1783.6)), dict(kind='duong', pts=[[-120, 1780], [-20, 1560], [30, 1300], [60, 1100]], w=3.5, wY=dict(on=1783.6)),
          dict(kind='xe', kieu='ngua', pts=[[-120, 1780], [-20, 1560], [30, 1300], [60, 1100]], n=4, v=1.6, hai_chieu=True, wY=dict(on=1783.6), seed=3101),
          dict(kind='xe', kieu='ngua', pts=ROAD_EO, n=6, v=1.8, hai_chieu=True, wY=dict(on=1783.6), seed=3108),
          dict(kind='vuon', at=[20, 1300], r=260, sx=1.7, n=70, w=44, h=30, luong=8, cao=0.5, mau=[0x4f6b2e, 0x7a5a3a, 0x8a7a40, 0x5d7a35], wY=dict(on=1784, full=1795), seed=3105),
          dict(kind='kho', at=[60, 1350], r=200, sx=1.6, n=30, wY=dict(on=1783.6), seed=3104),
          dict(kind='giasuc', loai='de', at=[-30, 1640], r=35, n=40, wY=dict(on=1783.6), seed=3102), dict(kind='giasuc', at=[230, 1650], r=30, n=10, wY=dict(on=1783.6), seed=3103),
          dict(kind='giasuc', loai='de', at=[-200, 900], r=90, n=60, wY=dict(on=1783.6), seed=3109),
          dict(kind='leu', at=[-120, 1150], r=70, sx=1.6, n=30, wY=dict(on=1783.6, off0=1810.12), seed=3106)]
DS_N33 = [dict(kind='duong', pts=ROAD_EO, w=5, wY=dict(on=1849)),
          dict(kind='vuon', w=40, h=28, luong=8, cao=0.5, mau=[0x4f6b2e, 0x7a5a3a, 0x8a7a40, 0x5d7a35], at=[310, 2230], r=170, sx=1.6, n=36, wY=dict(on=1849), seed=3310), dict(kind='kho', at=[220, 2000], r=150, sx=1.5, n=16, wY=dict(on=1849, full=1890), seed=3311), dict(kind='xe', kieu='ngua', pts=ROAD_EO[2:] + [[200, 1800], [300, 2200]], n=20, v=1.8, hai_chieu=True, wY=dict(on=1849), seed=3301),
          dict(kind='vuon', w=40, h=28, luong=8, cao=0.5, mau=[0x4f6b2e, 0x7a5a3a, 0x8a7a40, 0x5d7a35], at=[200, 2050], r=286, sx=1.5, n=115, wY=dict(on=1849, full=1880), seed=3308), dict(kind='giasuc', loai='de', at=[0, 950], r=104, n=100, wY=dict(on=1849), seed=3309),
          dict(kind='vuon', w=40, h=28, luong=8, cao=0.5, mau=[0x4f6b2e, 0x7a5a3a, 0x8a7a40, 0x5d7a35], at=[300, 1450], r=234, sx=1.4, n=55, wY=dict(on=1849, full=1885), seed=3302), dict(kind='kho', at=[380, 1600], r=156, n=25, wY=dict(on=1855, full=1900), seed=3303),
          dict(kind='giasuc', loai='de', at=[180, 1250], r=91, n=90, wY=dict(on=1849), seed=3304), dict(kind='giasuc', at=[460, 1380], r=78, n=30, wY=dict(on=1849), seed=3305),
          dict(kind='rao', pts=[[220, 1380], [420, 1360], [560, 1520]], wY=dict(on=1860, full=1880), seed=3306)]
DS_N34 = [dict(kind='duong', pts=ROAD_EO, w=4, wY=dict(on=1900)), dict(kind='xe', kieu='ngua', pts=ROAD_EO, n=6, v=1.8, hai_chieu=True, wY=dict(on=1900), seed=3401),
          dict(kind='leu', at=[40, 180], r=90, sx=2.2, n=110, wY=dict(on=1900, full=1912), seed=3402),          # trại lính sau hàng rào (lời 3g "a garrison camp") — vị trí ước lượng
          dict(kind='kho', at=[190, 240], r=50, n=7, wY=dict(on=1900, full=1915), seed=3403),
          dict(kind='vuon', w=40, h=28, luong=8, cao=0.5, mau=[0x4f6b2e, 0x7a5a3a, 0x8a7a40, 0x5d7a35], at=[-60, 230], r=70, sx=1.3, n=12, wY=dict(on=1900, full=1915), seed=3404),           # vườn (lời 3g "gardens") — ước lượng
          dict(kind='giasuc', at=[-60, 620], r=60, n=14, wY=dict(on=1900), seed=3405), dict(kind='giasuc', loai='de', at=[-120, 600], r=60, n=30, wY=dict(on=1900), seed=3406),
          dict(kind='vuon', w=40, h=28, luong=8, cao=0.5, mau=[0x4f6b2e, 0x7a5a3a, 0x8a7a40, 0x5d7a35], at=[100, 560], r=150, sx=1.6, n=44, wY=dict(on=1900), seed=3407),                  # huerta phía TBN, tiền cảnh (ước lượng)
          dict(kind='giasuc', loai='de', at=[40, 700], r=50, n=36, wY=dict(on=1900), seed=3408), dict(kind='kho', at=[200, 620], r=130, n=16, wY=dict(on=1900), seed=3409), dict(kind='giasuc', at=[180, 780], r=30, n=8, wY=dict(on=1900), seed=3411),
          dict(kind='rao', pts=[[100, 405], [240, 410], [300, 470]], buoc=3, wY=dict(on=1900), seed=3410)]
DS_N35 = [dict(kind='kho', at=[-60, 120], r=70, n=6, wY=dict(on=1934.5, full=1936), seed=3501), dict(kind='leu', at=[150, 160], r=50, n=14, wY=dict(on=1909.5), seed=3502),
          dict(kind='duong', pts=ROAD_EO, w=5, wY=dict(on=1900))]
DS_N41 = [dict(kind='xe', kieu='tai', pts=[[-700, -40], [-200, -30], [300, -20], [620, -10]], n=12, v=6, hai_chieu=True, wY=dict(on=1939.85), seed=4101),
          dict(kind='xe', kieu='tai', pts=ROAD_EO, n=6, v=7, hai_chieu=True, wY=dict(on=1939.2), seed=4105),
          dict(kind='dong', at=[100, 60], r=220, sx=2.5, n=40, wY=dict(on=1939.85, full=1940.8), seed=4102),
          dict(kind='kho', at=[200, 220], r=110, sx=1.5, n=12, wY=dict(on=1939.3, full=1939.9), seed=4103),
          dict(kind='leu', at=[-150, 200], r=90, sx=1.5, n=50, wY=dict(on=1909.5), seed=4104), dict(kind='duong', pts=ROAD_EO, w=5, wY=dict(on=1900)),
          dict(kind='vuon', w=40, h=28, luong=8, cao=0.5, mau=[0x4f6b2e, 0x7a5a3a, 0x8a7a40, 0x5d7a35], at=[150, 560], r=150, sx=1.6, n=36, wY=dict(on=1900), seed=4106), dict(kind='kho', at=[250, 620], r=120, n=12, wY=dict(on=1900), seed=4107),
          dict(kind='giasuc', loai='de', at=[0, 650], r=60, n=30, wY=dict(on=1900), seed=4108)]

C4_P1, C4_L1, C4_F1 = [-4500, 45, -700], [-600, 110, -1300], 40   # BAN-CUOI-T3 1a: máy góc 1 C4 (chọn bằng thử máy)

# ---------------- 43 SHOT ----------------
def shots():
    S = []; V = {s['id']: s for s in V7C.shots()}
    def add(sid, lines, diem, kieu, vai, noi, loai, o, cam, td, su_kien, ghi, **kw):
        S.append(dict(id=sid, lines=lines, diem=diem, kieu=kieu, vai=vai, noi=noi, loai=loai, opt=o, cam=cam, td=td, su_kien=su_kien, ghi=ghi, **kw))
    d = dur_of
    # ===== CHƯƠNG 0 · MÓC (0 → 43,833) =====
    v = V['H1']; o = copy.deepcopy(v['opt']); D = d(['0a', '0b'])
    # ANIM-V2 (chủ dự án 21/10 21:05): mở đầu BAN NGÀY → hoàng hôn → đêm (timelapse thấy ngay, Rock nhận ra trong ánh ngày ≤ 3 s); M5 (Omni) 4,5 → 10,5 s; kết 23:52 nối H2
    o['time'] = [dict(t=0, at='2026-10-19 15:00', sun='real', lab='dt'), dict(t=4.5, at='2026-10-19 17:30', sun='real', lab='dt'), dict(t=9.5, at='2026-10-19 19:40', sun='real', lab='dt'),
                 dict(t=9.65, at='2026-10-19 20:30', sun='real', lab='dt'), dict(t=D, at='2026-10-19 23:52', sun='real', lab='dt')]   # BAN-CUOI-T3 1c: M5 rút 1 s (4,5 → 9,5); hoàng hôn → đêm 9,5 → 9,65 s; "Midnight…" từ 9,75 s trên đêm 3D   # M5 (Omni, nắng chiều) nằm ở 17:30–18:20; hoàng hôn → đêm 10,5 → 12 s
    cam, ct = cuts(D, [dict(t1=4.5, p0=[380, 430, 1350], l0=[-110, 0, -300], dp=(-5, -2, -12), fov=40), dict(t1=9.5, p0=[4, 9.0, -40], l0=[6, 2.0, 0], dp=(0, 0, 2), fov=50),
                       dict(p0=[371, 426, 1330], l0=[-111, 0, -301], dp=(-5, -2, -12), fov=40)])   # ANIM-V2: góc giữa = máy tầm mắt cá chân trên đường Winston Churchill qua đường băng (ảnh đầu M5)
    add('H1', ['0a', '0b'], 'D7-lai → WCA-than → D7-lai', 'lai', 'co-che', 'eo_dat', 'pho', o, cam, v['td'],
        [dict(t=0.0, k='ngay_dem', s='19/10/2026 15:00: ban ngày — Rock nguyên khối, cổng + đường băng tiền cảnh'), dict(t=4.5, k='minh_hoa', s='M5 (minh hoạ Omni): cận chân người đi bộ bước qua vạch đường băng'),
         dict(t=9.5, k='ngay_dem', s='hoàng hôn → đêm; đèn phố/đường băng bật dần'), dict(t=11.9, k='ngay_dem', s='gần nửa đêm biên giới (23:52)')],
        'ANIM-V2: mở đầu ban ngày → đêm (timelapse 15:00 → 23:52, cùng điểm máy D7, trôi rất chậm) — Rock nhận ra trong ánh ngày 0–3 s; M5 minh hoạ Omni 4,5 → 10,5 s; H2 nối từ 23:52',
        minh_hoa=[dict(ma='M5', t0=4.5, t1=9.5)], cat=ct)
    v = V['H2']; o = copy.deepcopy(v['opt'])
    o['time'][0] = dict(t=0, at='2026-10-19 23:53', sun='real', lab='dt', hold=True); o['time'][1] = dict(t=o['time'][1]['t'], at='2026-10-20 00:20', sun='real', lab='dt', hold=True)   # ANIM-V2: nối giờ kết thúc H1 (đêm)
    for f in o['fleets']:
        if f.get('wY') == [1704.55, 1704.68]: f['co'] = False   # cờ Red Ensign 1707 lệch ngày ở 1704 → bỏ cờ đuôi đoàn Rooke
    add('H2', ['0c', '0d', '0e'], 'K2', 'chat', 'buoc-ngoat', 'thanh_pho', 'vinh', o, V7C.fill_h('H2', copy.deepcopy(V7C.CAM['H2'])), v['td'], V7C.SU_KIEN['H2'],
        'kế thừa V7C (mở đầu duyệt): bước năm 14 lần vây, cờ 4/8/1704 hạ–kéo trên Tower of Homage (khung chặt có vai: cờ), pin nổi vào vị trí 13/9/1782; bỏ cờ đuôi lệch ngày của đoàn 1704')
    v = V['H2T']; add('H2T', ['0f'], 'N2r', 'dem', 'khoanh-khac-bien-co', 'thanh_pho', 'vinh', copy.deepcopy(v['opt']), copy.deepcopy(V7C.CAM['H2T']), v['td'], V7C.SU_KIEN['H2T'],
        'LOOK-3 (tham chiếu): góc thumbnail X01/X08, pin nổi cháy đêm 13→14/9/1782 — giữ nguyên V7C', luot_thap=[0, 5.0], goc='thap')
    v = V['H3']; o = copy.deepcopy(v['opt']); D = d(['0g', '0h'])
    add('H3', ['0g', '0h'], 'D7h-lai', 'lai', 'buoc-ngoat', 'eo_dat', 'pho', o, [K(0, [-150, 380, 560], [-260, 0, -900], 40), K(D, [-154, 374, 548], [-262, 0, -905], 40)], v['td'], V7C.SU_KIEN['H3'],
        'V7C D7h, điểm nhìn dời nam 700 m → nhìn xuống ≈ 14,6° (khung lai): đường băng mọc qua đường 1939–41 → 2026, Rock + phố nền')
    # ===== CHƯƠNG 1 · ROCK (43,833 → 173,083) =====
    D = d(['SM1', '1a', '1b'])
    o = base(time=[dict(t=0, at='1704-07-30 09:00', sun=15.0, lab='d'), dict(t=6.5, at='1704-07-31 09:00', sun=15.0, lab='d'), dict(t=D, at='1704-08-02 15:00', sun=15.0, lab='d')],
             fleets=[dict(n=18, center=[-1900, -1650], axis=165, spacing=170, kind='line', heading=80, wY=[1704.55, 1704.70], co=False, path=[[1704.574, -2600, -1900], [dy('1704-08-01 18:00'), 0, 0]]),
                     dict(n=10, center=[-2300, -1150], axis=160, spacing=160, kind='sail', heading=80, wY=[1704.55, 1704.70], co=False, path=[[1704.574, -2600, -1900], [dy('1704-08-01 18:00'), 0, 0]])],
             co=co_ld() + co_lw(), pre1704town=True, recl=False, sieges=False)
    add('N1.1', ['SM1', '1a', '1b'], 'B-lai', 'lai', 'co-che', 'bien', 'vinh', o, hold([-2650, 520, -350], [-850, 0, -1450], 42, D, (60, -8, -25)), [('doan_rooke', None)],
        [dict(t=0.4, k='the_chuong', s='1704 — The Rock changes hands'), dict(t=2.0, k='tau', s='hạm đội Anh–Hà Lan (Rooke) vào vịnh từ eo biển'), dict(t=12.0, k='tau', s='hạm đội thả neo trước phố 1704')],
        'thay bản đồ chiến lược SM1 + chân dung 1b bằng hạm đội vào vịnh (TL-4); 28 tàu (18 tàu chiến + 10 tàu vận tải) — số minh hoạ, vị trí neo minh hoạ (bậc 5); không cờ đuôi (mẫu cờ 1704 chưa có nguồn)',
        chuong='1704 — The Rock changes hands')
    D = d(['1c', '1d']); t15 = NH['1d']['cau'][2]['bd_phim'] - NH['1c']['bd_phim']   # "…fifteen thousand rounds"
    bomb = [dict(at=[-1300 + 90 * i, 12, -1500 + 60 * (i % 4)], wY=[dy('1704-08-02 14:00'), dy('1704-08-03 17:00')], n=10, size=60, rise=50, drift=[-3, 1], period=0.22, seed=900 + i, alpha=0.8) for i in range(10)] + \
           [dict(at=[e, 14, n], wY=[dy('1704-08-02 15:00'), dy('1704-08-04 06:00')], n=12, size=50, rise=90, drift=[-2, 1], period=0.3, seed=930 + i, alpha=0.75, fire=0.4) for i, (e, n) in enumerate([(-470, -1300), (-520, -1150), (-430, -1000), (-560, -1450)])]
    o = base(time=[dict(t=0, at='1704-08-01 12:00', sun=15.0, lab='d'), dict(t=t15 - 2.0, at='1704-08-02 14:00', sun='real', lab='dt'), dict(t=D, at='1704-08-03 18:00', sun='real', lab='dt')],
             fleets=[dict(n=18, center=[-1800, -1600], axis=165, spacing=170, kind='line', heading=80, wY=[1704.55, 1704.70], co=False)], smoke=bomb, co=co_ld() + co_lw(), pre1704town=True, recl=False, night=True,
             lives=[dict(era=1782, wY=dict(on=1700), walkers=[dict(line='MAIN', n=50, width=4, colors=ES1704)], lines=dict(MAIN=[[-430, -1600], [-445, -1400], [-440, -1300], [-432, -1150], [-425, -1000]]), chimney=8)])
    add('N1.2', ['1c', '1d'], 'C-lai', 'lai', 'co-che', 'thanh_pho', 'pho', o, hold([-80, 340, -1950], [-820, 0, -950], 44, D, (-30, -6, 20)), [('pho_1704', None)],
        [dict(t=0.0, k='xay', s='phố có tường 1704 (lớp tái dựng 1705)'), dict(t=round(t15 - 2, 2), k='lua', s='hạm đội bắn phá: khói pháo ngoài vịnh + khói trong phố'), dict(t=round(D - 2, 2), k='ngay_dem', s='đêm 3/8/1704')],
        'phố 1704 trong tường (bậc 5: lớp 1705 đại diện); Exact Plan 1704/5 KHÔNG phủ (chưa nắn khớp địa hình — TL-4 chỉ cho phủ khớp) → bản đồ để thẻ phương pháp/mô tả; khói minh hoạ vị trí')
    D = d(['1e', '1f'])
    o = base(time=[dict(t=0, at='1704-08-04 08:30', sun='real', lab='dt'), dict(t=9.5, at='1704-08-04 16:00', sun='real', lab='dt'), dict(t=D, at='1704-08-06 12:00', sun=14.0, lab='d')],
             co=co_ld(1.5) + co_lw(), pre1704town=True, recl=False, fleets=[dict(n=18, center=[-1800, -1600], axis=165, spacing=170, kind='line', heading=80, wY=[1704.55, 1704.70], co=False)],
             units=[dict(at=[-160, -880], heading=300, rows=3, cols=12, side='gb', day=[dy('1704-08-04 15:00'), 1705], seed=41, rim=False)])
    add('N1.3', ['1e', '1f'], 'K-co', 'chat', 'buoc-ngoat', 'thanh_pho', 'pho', o, hold([-60, 160, -980], [-135, 100, -825], 32, D, (-4, 0, 3)), [('lau_dai', None)],
        [dict(t=1.5, k='co', s='4/8/1704: Borgoña hạ trên Tower of Homage'), dict(t=4.0, k='co', s='Union kéo lên'), dict(t=9.6, k='nguoi', s='lính Anh–Hà Lan vào lâu đài')],
        'MỐC ĐINH 4/8/1704 — khung chặt có vai (cờ, §LOOK-2): máy cách cờ ≈ 180 m, cờ × 1,5; thẻ "100 / 500" bỏ (lời mang số)')
    D = d(['1g'])
    o = base(time=[dict(t=0, at='1704-08-07 09:00', sun=10.0, lab='d'), dict(t=D, at='1704-08-25 09:00', sun=10.0, lab='d')], co=co_ld() + co_lw(), pre1704town=True, recl=False,
             lives=[dict(era=1782, wY=dict(on=1704.59, off0=dy('1704-08-22 12:00'), off1=dy('1704-08-26 00:00')), walkers=[dict(line='ISTH', n=1400, width=9, colors=ES1704 + CIV, free=False, dir=1)],
                         crowds=[dict(line='ISTH', groups=24, size=[5, 12], speed=1.0, dir=1, colors=ES1704 + CIV)], lines=dict(ISTH=[[-120, -200], [0, 0], [40, 300], [70, 520], [110, 900], [160, 1400]]))])
    # ANIM-V2 R1: máy hạ thấp sát dòng người (≈ 15 m bên trái máy), dòng người đi VỀ phía máy (bắc), Rock nguyên khối sau lưng họ; M3 (Omni) 3,5 → 11,5 s
    cam, ct = cuts(D, [dict(t1=3.5, p0=[92, round(max(0.0, hAt(92, 700)) + 7, 1), 700], l0=[-110, 25, -600], dp=(0, 0, -4), fov=38),
                       dict(t1=11.5, p0=[82, round(max(0.0, hAt(82, 600)) + 1.7, 1), 600], l0=[45, round(max(0.0, hAt(45, 300)) + 8, 1), 300], dp=(0, 0, -2), fov=44),
                       dict(p0=[150, 30, 820], l0=[-60, 20, -500], dp=(0, 0, -6), fov=38)])   # ANIM-V2: góc giữa = máy tầm người trên đường cát (ảnh đầu M3)
    add('N1.4', ['1g'], 'A-thap', 'lai', 'co-che', 'eo_dat', 'eo', o, cam, [('dong_nguoi', None)],
        [dict(t=0.5, k='nguoi', s='dòng dân rời phố đi bắc dọc eo đất (về San Roque) — cận dòng người'), dict(t=3.5, k='minh_hoa', s='M3 (minh hoạ Omni): gia đình mang đồ đi trên đường cát, Rock sau lưng'),
         dict(t=11.5, k='nguoi', s='dòng người thưa dần (21–25/8)')],
        'ANIM-V2 R1: máy hạ ≈ 16–30 m, cạnh dòng người (đi cùng chiều về bắc, 1 400 người + 24 nhóm — số minh hoạ bậc 5; hướng đi: lời 1g S017–S018); M3 minh hoạ 3,5 → 11,5 s',
        cat=ct, minh_hoa=[dict(ma='M3', t0=3.5, t1=11.5)], goc='thap')
    D = d(['1h', '1i']); t2015 = NH['1i']['cau'][2]['bd_phim'] - NH['1h']['bd_phim']
    # ANIM-V2 R4 + R3: lời hiệp ước 1713 không có vật trên eo đất → 3 góc: (A) CẢNG + phố 7/1713 (tàu ra vào, ngày–đêm) · (B) LÂU ĐÀI, cờ Union 1713 ("the town, castle and port")
    #  · (C) eo đất từ mép bắc Rock: trống ≤ 4 s rồi bước năm 2015 (đường băng + phố) đúng chữ "in 2015"
    tA, tB = round(NH['1h']['cau'][1]['bd_phim'] - NH['1h']['bd_phim'], 3), round(NH['1i']['cau'][1]['bd_phim'] - NH['1h']['bd_phim'] - 0.05, 3)
    o = base(time=[dict(t=0, at='1713-07-13 09:00', sun=14.0, lab='d'), dict(t=tA - 0.05, at='1713-07-19 15:00', sun=14.0, lab='d'), dict(t=tA, at='1713-07-20 10:00', sun=14.0, lab='d'),
                   dict(t=tB - 0.05, at='1713-07-26 15:00', sun=14.0, lab='d'), dict(t=tB, at=1729.3, sun=14.0, lab='y', hold=True), dict(t=t2015 - 0.05, at=1729.5, sun=14.0, lab='y', hold=True),
                   dict(t=t2015, at=2015.5, sun=14.0, lab='y', hold=True), dict(t=D, at=2015.6, sun=14.0, lab='y')], night=True,
             co=co_ld() + co_lw(), recl=True, linea=False,
             fleets=[dict(n=5, center=[-1200, -1300], axis=165, spacing=180, kind='sail', heading=80, wY=[1713.4, 1713.6], co=False, path=[[dy('1713-07-14 00:00'), -2600, -1900], [dy('1713-07-18 00:00'), 0, 0]])],
             lives=[dict(era=1782, wY=dict(on=1700), walkers=[dict(line='MAIN', n=70, width=4, colors=ES1704 + CIV)], lines=dict(MAIN=[[-430, -1600], [-445, -1400], [-440, -1300], [-432, -1150], [-425, -1000]]), chimney=8,
                         boats=[dict(pts=[[-1400, -800], [-1000, -1150], [-700, -1250]], len=8, speed=3, s0=0.1), dict(pts=[[-1500, -1500], [-1000, -1300], [-650, -1080]], len=9, speed=2.5, s0=0.6)])])
    cam, ct = cuts(D, [dict(t1=tA, p0=[-1750, 95, -900], l0=[-560, 20, -1150], dp=(25, -2, -10), fov=40), dict(t1=tB, p0=[-1150, 60, -760], l0=[-300, 70, -900], dp=(10, 0, -3), fov=30)   # soát dựng: góc lâu đài K-co ở 1713 lỗi hình (tường trong suốt, bụi lơ lửng) → lâu đài + phố + Line Wall từ vịnh, ống dài
                       ,
                       dict(p0=[120, 170, -420], l0=[60, 0, 900], dp=(0, -4, 12), fov=46)])
    add('N1.5', ['1h', '1i'], 'B-thap → K-co → E-bac', 'lai', 'co-che', 'thanh_pho', 'pho', o, cam, [('cang_pho_lau_dai', [0, tB]), ('eo_dat', [tB, D])],
        [dict(t=0.0, k='tau', s='7/1713: cảng + phố (tàu buôn ra vào, ngày–đêm)'), dict(t=tA, k='co', s='lâu đài, cờ Union trên Tower of Homage (hiệp ước nêu "town, castle and port")'),
         dict(t=tB, k='dem_nam', s='eo đất phía bắc 1729 (không có trong hiệp ước)'), dict(t=round(t2015, 2), k='buoc_nam', s='bước năm 2015: đường băng + phố trên eo đất')],
        'ANIM-V2 R4/R3: lời hiệp ước không có vật trên eo đất → góc cảng (tàu buôn 5 chiếc + thuyền nhỏ: số/vị trí minh hoạ bậc 5; ngày 13/7/1713: ngày ký hiệp ước, bậc 2) → góc lâu đài (cờ Union, như N1.3) → eo đất từ mép bắc Rock: trống ≤ 4 s rồi bước năm 2015 đúng chữ "in 2015" — không vẽ biên giới (§10.7)',
        cat=ct)
    D = d(['1j', '1k']); t27 = NH['1j']['cau'][1]['bd_phim'] - NH['1j']['bd_phim']; t30 = NH['1k']['bd_phim'] - NH['1j']['bd_phim']; tLL = NH['1k']['cau'][1]['bd_phim'] - NH['1j']['bd_phim']
    sg = [dict(at=[e, 10, n], wY=w, n=16, size=110, rise=150, drift=[-2, 1], period=0.3, seed=950 + i, alpha=0.8) for i, (e, n) in enumerate([(-250, -500), (-100, -450), (60, -480)]) for w in ([1704.8, 1705.3], [1727.12, 1727.45])]
    o = base(time=[dict(t=0, at=1704.80, sun=14.0, lab='m'), dict(t=t27 - 0.05, at=1705.30, sun=14.0, lab='m', hold=True), dict(t=t27, at=1727.15, sun=14.0, lab='m', hold=True), dict(t=t30 - 0.05, at=1727.45, sun=14.0, lab='m', hold=True),
                   dict(t=t30, at=1730.0, sun=14.0, lab='y', hold=True), dict(t=tLL - 0.05, at=1735.4, sun=14.0, lab='y', hold=True), dict(t=tLL, at=2026.78, sun=14.0, lab='y', hold=True), dict(t=D, at=2026.79, sun=14.0, lab='y')],
             smoke=sg, co=co_ld() + co_lw(), pre1704town=True, recl=False, pho2026=dict(box=[-1200, 700, 1200, 2600]))
    # ANIM-V2 R1 + R3: (A) vây 1704–05 / 1727 — máy hạ ≈ 1,2 km trước vách bắc, khói trận + vách là chủ thể · (B) Línea mọc 1730–35 — máy ≈ 300 m sau tuyến, 70 m, tuyến + đồn chiếm tiền cảnh, Rock nền
    #  · bước năm 2026 đúng chữ "The town behind it is still called La Línea" (phố La Línea sau tuyến cũ)
    cam, ct = cuts(D, [dict(t1=t30, p0=[-80, 95, 650], l0=[-90, 150, -700], dp=(10, -3, -15), fov=40), dict(t1=round(tLL, 3), p0=[-200, 60, 1250], l0=[-130, 60, -600], dp=(3, -1, -5), fov=26), dict(p0=[-250, 110, 1350], l0=[-120, 40, -300], dp=(0, -2, -6), fov=40)])   # soát dựng: bước 2026 ở máy 15 m nằm trong khối nhà → góc 2026 nâng 110 m   # đo R2: góc cũ 57–97 % cỏ trống → nhìn nam: tuyến mọc tiền cảnh + Rock; soát master: máy 22 m làm ô đất gần máy biến mất (nước + bụi lơ lửng) → nâng 60 m, lùi 220 m
    add('N1.6', ['1j', '1k'], 'A2-thap → L-linea', 'lai', 'co-che', 'eo_dat', 'eo', o, cam, [('vach_bac', [0, t30]), ('linea', [t30, D])],
        [dict(t=0.5, k='lua', s='vây 1704–05: khói pháo ở chân vách bắc'), dict(t=round(t27, 2), k='buoc_nam', s='bước năm 1727: vây lần nữa'), dict(t=round(t30, 2), k='xay', s='Línea de Contravalación mọc tây → đông 1730–35 (cận tuyến)'),
         dict(t=round(tLL, 2), k='buoc_nam', s='2026: phố La Línea sau tuyến cũ')],
        'ANIM-V2 R1/R3: 2 góc — vách bắc + khói vây (thời điểm bậc 2, vị trí khói minh hoạ bậc 5) → cận Línea mọc theo năm (ghost SH T1782-01, bậc 1; ngày xây TIEN-KY T3) + bước 2026 (nhà La Línea: Catastro/OSM, bậc 1) đúng chữ "still called La Línea"',
        cat=ct)
    # ===== CHƯƠNG 2 · VÂY HÃM (173,083 → 382,583) =====
    v = V['C1']; o = copy.deepcopy(v['opt']); o['campTuNhien'] = True; D = d(['2a', '2b'])
    C1cam = [K(0, [-1250, 330, 3500], [-1150, 60, 1500], 34), K(7.48, [-1250, 328, 3490], [-1150, 60, 1500], 34), K(7.5, [-1250, 328, 3490], [-1150, 60, 1500], 34),
             K(10.4, [-1250, 200, 2600], [-1290, 0, 3350], 40), K(10.42, [-1250, 200, 2600], [-1290, 0, 3350], 40), K(D, [-1254, 198, 2618], [-1291, 0, 3352], 40)]   # soi 1: 1 km → lều thành khối chữ nhật; lại gần ≈ 750 m
    # ANIM-V2 R1/R3: 3 góc — (A) Línea + đồn (tuyến đóng đường bộ 21/6/1779) cận, Rock nền · (B) cận dãy trại dựng lên từ 13/7 (lều, ngựa, khói bếp chiếm tiền cảnh) · (C) toàn dải trại tới 10/1779, Rock nền
    tAc = round(NH['2b']['bd_phim'] - NH['2a']['bd_phim'], 3); tBc = round(NH['2b']['cau'][1]['bd_phim'] - NH['2a']['bd_phim'], 3)
    o['time'] = [dict(t=0, at='1779-06-20 09:00', sun='real', lab='dt'), dict(t=tAc - 0.05, at='1779-06-22 16:00', sun='real', lab='dt'), dict(t=tAc, at='1779-07-13 12:00', sun=12.0, lab='d'),
                 dict(t=D, at='1779-10-28 12:00', sun=12.0, lab='d')]   # soát dựng: góc cận trại (B) không thấy lều ở 7–9/1779 → gộp vào góc dải trại (lều mọc 13/7 → 28/10); o['night'] = True
    C1cam, ct = cuts(D, [dict(t1=tAc, p0=[-560, 75, 1330], l0=[-120, 15, 820], dp=(15, -2, -10), fov=42), dict(p0=A(-1150, 70, 3550), l0=A(-1300, 0, 2950), dp=(5, 0, -10), fov=44)])
    add('C1', ['2a', '2b'], 'L-linea → T-trai-bac', 'lai', 'co-che', 'eo_dat', 'trai', o, C1cam, v['td'],
        [dict(t=0.4, k='the_chuong', s='1779 — The Great Siege'), dict(t=0.5, k='ngay_dem', s='20→21/6/1779: Línea và đồn — đường bộ bị cắt (ngày–đêm)'), dict(t=tAc, k='xay', s='trại TBN dựng lên từ 13/7/1779 (cận lều, ngựa, khói bếp)'),
         dict(t=tBc, k='xay', s='10/1779: toàn dải trại, Rock nền')],
        'ANIM-V2 R1/R3 (thay LOOK-4 cũ): 2 góc thấp — Línea + đồn (bậc 1) → dải trại mọc dần 13/7 → 28/10/1779 nhìn nam về Rock (eo-dat-v7.json, bậc 1–2; lều tự nhiên, số lều giữ nguyên)', chuong='1779 — The Great Siege', cat=ct)
    v = V['C2']; o = copy.deepcopy(v['opt']); D = d(['2c']); E = V7B.CAMS['E']
    add('C2', ['2c'], 'E (V7B-a)', 'lai', 'co-che', 'bien', 'vinh', o, [K(0, E['p0'], E['l0'], E['fov']), K(D, E['p1'], E['l0'], E['fov'])], v['td'], V7C.SU_KIEN['C2'],
        'LOOK-4 sửa (V7C giây 68–76 chỉ còn nước): máy E của V7B biến thể a (tham chiếu ngữ pháp đã kiểm: hạm đội phong toả đọc rõ, Rock giữa khung); thuyền châu Phi quay đầu ở hàng chặn (V7C)')
    v = V['C3']; o = copy.deepcopy(v['opt']); D = d(['2d', '2e']); cam = V7C.fill_h('C3', copy.deepcopy(V7C.CAM['C3']))
    lk = [40, 230, -1250]; cam[0] = K(0, cam[0]['p'], lk, cam[0]['fov']); cam[1] = K(7.98, cam[1]['p'], lk, cam[1]['fov']); cam[2] = K(8.0, cam[2]['p'], lk, cam[2]['fov'])   # ANIM-V2: cận nhìn LÊN sườn đá (ảnh đầu M2 không có cờ/phố/vịnh/tàu — lượt 1 Omni bịa tàu, tháp chuông, đê ở vịnh)
    for L0 in o.get('lives') or []:
        for w in L0.get('walkers') or []:
            if w.get('line') == 'SLOPE': w['n'] = 24   # người hái rau dại: số minh hoạ (bậc 5) — thưa hơn để đọc là người hái, không phải đám đông dạo   # ANIM-V2: giữ cận tới 8,0 s (M2 phủ 0 → 8,0 s), rồi cẩu lên
    cam[3] = K(10.0, [-150, 330, -1700], [-900, 0, -800], 42); cam[4] = K(10.02, [-150, 330, -1700], [-900, 0, -800], 42); cam[5] = K(D, [-156, 328, -1694], [-900, 0, -800], 42)
    o['time'] = [dict(t=0, at='1780-01-14 10:00', sun='real', lab='d'), dict(t=8.0, at='1780-01-14 12:30', sun='real', lab='d'), dict(t=10.0, at='1780-01-14 15:00', sun='real', lab='d'),
                 dict(t=10.6, at='1780-01-14 15:30', sun=15.0, lab='d'), dict(t=D, at='1780-01-16 15:30', sun=15.0, lab='d')]
    add('C3', ['2d', '2e'], 'Ca2-lai', 'chat', 'co-che', 'thanh_pho', 'pho', o, cam, v['td'],
        [dict(t=0.0, k='minh_hoa', s='M2 (minh hoạ Omni): người cúi hái rau dại trên sườn đá, gió, khói xa (1/1780)'), dict(t=8.0, k='may', s='cẩu lên: phố + Line Wall + hải đội phong toả')],
        'ANIM-V2: M2 minh hoạ Omni 0 → 8 s (ảnh đầu = khung cận 20–30 m người hái rau dại S052 của chính shot; Q3: Drinkwater 1786 tr. 108 "thistles, dandelion, wild leeks"); 8 → 10 s cẩu lên khung lai ≈ 16°',
        luot_thap=[0, 8.0], minh_hoa=[dict(ma='M2', t0=0.0, t1=8.0)])
    v = V['C4']; o = copy.deepcopy(v['opt']); D = d(['SM2', '2f']); cam = copy.deepcopy(V7C.CAM['C4'])
    # ANIM-V2: hết "đồ chơi" — ngoài M1 dùng MÁY THẤP CHÉO từ vịnh (≈ 45 m, nhìn xuống ≈ 5°) thấy tàu tiền cảnh + Old Mole + phố + Rock; M1 (Omni) 2,0 → 9,0 s cận bến ở tầm người
    # BAN-CUOI-T3 (1a): v2 mất đoàn cứu viện Rodney (thời gian góc 1 trước cửa sổ đoàn tàu + máy đặt giữa hàng neo). Góc 1 (0 → 6 s, lời SM2 "three relief fleets"):
    #  máy thấp chéo từ vịnh, đoàn Rodney (9 tàu chiến + 12 tàu hàng, dữ liệu tàu V7C/v1) đi vào, Rock nền không cắt mép · góc 2 (6 → 10 s, M1 giữ 3D): dỡ hàng Old Mole, hàng neo phía sau
    #  · góc 3 (10 → 13,5 s, lời 2f): tàu chanh Đan Mạch vào cảng 10/1780
    cam, ct = cuts(D, [dict(t1=6.0, p0=C4_P1, l0=C4_L1, dp=(700, -5, -100), fov=C4_F1), dict(t1=10.0, p0=[-1900, 50, -1900], l0=[-600, 30, -700], dp=(30, -1, 25), fov=40),
                       dict(p0=[-1420, 52, -1180], l0=[-620, 25, -1000], dp=(25, -1, 5), fov=40)])
    o['time'] = [dict(t=0, at='1780-01-18 18:10', sun=15.0, lab='d'), dict(t=5.98, at='1780-01-19 13:00', sun=15.0, lab='d'), dict(t=6.0, at='1780-01-21 10:00', sun=15.0, lab='d'), dict(t=10.0, at='1780-02-01 12:00', sun=15.0, lab='d'),
                 dict(t=10.05, at='1780-10-08 12:00', sun=15.0, lab='d'), dict(t=11.5, at='1780-10-12 12:00', sun=15.0, lab='m'), dict(t=D, at='1780-11-30 12:00', sun=15.0, lab='m')]
    add('C4', ['SM2', '2f'], 'Bm-thap → M1 → Bm-thap', 'lai', 'co-che', 'bien', 'vinh', o, cam, v['td'],
        [dict(t=0.0, k='tau', s='đoàn cứu viện Rodney vào vịnh 17→19/1/1780 (cờ Red Ensign) — máy thấp chéo, đoàn tàu là tiêu điểm, Rock nền'), dict(t=6.0, k='nguoi', s='Old Mole 21/1→1/2/1780: thuyền cập, người khiêng thùng, đống hàng lớn dần (3D, M1 giữ 3D)'),
         dict(t=10.05, k='tau', s='10/1780: tàu chanh Đan Mạch vào cảng')],
        'ANIM-V2: máy thấp chéo từ vịnh (thay khung lai 13° nhìn xuống bến "đồ chơi"); M1 minh hoạ Omni TRƯỢT 3 lượt (tàu có buồm / cờ / cọc buộc sắt) → giữ 3D góc thấp gần bến 2 → 9 s; đoàn Rodney + tàu chanh: V7C (bậc 2 thời điểm, số/vị trí minh hoạ)',
        cat=ct)
    v = V['C5']; o = copy.deepcopy(v['opt']); D = d(['2g']); cam = copy.deepcopy(V7C.CAM['C5'])
    for k in cam: k['l'] = [-900, 0, -900]
    # ANIM-V2: M4 (Omni) 6,1 → 12,5 s — ngõ đêm 13→14/4/1781, ánh lửa, người chạy về nam (lời "Spain's batteries opened fire on the town … The townspeople fled south"); ảnh đầu = máy tầm người trên Main Street nhìn bắc về các nhà cháy
    tM4 = 6.1; cam = [k for k in cam if k['t'] < tM4 - 0.03] + [K(tM4 - 0.02, cam[-1]['p'], cam[-1]['l'], cam[-1]['fov']), K(tM4, [-420, 40, -1400], [-445, 20, -1265], 40), K(D, [-421, 39.5, -1397], [-445, 20, -1265], 40)]   # máy ≈ 22 m trên mặt phố (ngang mái), nhìn bắc về các nhà cháy
    o['time'] = [k for k in o['time'] if k['t'] <= 5.8] + [dict(t=tM4, at='1781-04-14 01:30', sun='real', lab='dt'), dict(t=D, at='1781-04-14 05:00', sun='real', lab='dt')]   # đêm 13→14/4: nhà cháy (o.burn 14/4 ≈ 01:00 → 08:00)
    add('C5', ['2g'], 'Cc2-lai → M4', 'lai', 'buoc-ngoat', 'thanh_pho', 'vinh', o, cam, v['td'],
        [dict(t=0.5, k='tau', s='12/4/1781: đoàn Darby thả neo'), dict(t=5.9, k='lua', s='pháo TBN bắn vào phố'), dict(t=tM4, k='minh_hoa', s='M4 (minh hoạ Omni): ngõ đêm 13→14/4/1781, ánh lửa, người chạy về nam')],
        'V7C Cc2 (khung lai ≈ 16–19°): đoàn Darby thả neo, pháo bắn vào phố; ANIM-V2: M4 minh hoạ Omni 6,1 → 12,5 s (cháy 4–5 nhà đêm 13→14/4, S063; dân chạy về nam: lời 2g)', cat=[tM4], minh_hoa=[dict(ma='M4', t0=tM4, t1=D)])
    D = d(['2h', '2i']); tlo = 8.4
    o = base(time=[dict(t=0, at='1781-04-14 12:00', sun='real', lab='dt'), dict(t=tlo, at='1781-04-16 18:00', sun='real', lab='dt'), dict(t=tlo + 0.05, at=1781.30, sun=15.0, lab='m'), dict(t=D, at=1782.62, sun=15.0, lab='m')],
             co=co_ld() + co_lw(), recl=False, night=True, hideOldTrees=True,
             smoke=[dict(at=[e, 10, n], wY=[1781.29, 1782.62], n=14, size=90, rise=120, drift=[-2.5, 1], period=0.35, seed=960 + i, alpha=0.8) for i, (e, n) in enumerate(WORKS82[:4])] +
                   [dict(at=[e, 14, n], wY=[1781.29, 1782.62], n=10, size=60, rise=90, drift=[-2.5, 1], period=0.3, seed=980 + i, alpha=0.7) for i, (e, n) in enumerate([(-470, -1300), (-500, -1100), (-440, -1450)])],
             units=[dict(at=[-455, -1290 + 40 * i], heading=0, rows=2, cols=8, side='gb', day=[dy('1781-04-14 06:00'), dy('1781-04-17 00:00')], seed=990 + i, rim=False) for i in range(3)])
    add('N2.6', ['2h', '2i'], 'C-lai', 'lai', 'co-che', 'thanh_pho', 'pho', o, hold([-260, 270, -1880], [-680, 0, -1040], 40, D, (-20, -4, 12)), [('pho_bi_ban', None)],
        [dict(t=0.5, k='nguoi', s='14–16/4/1781: lính tụ trước kho thương nhân trên Main Street'), dict(t=round(tlo, 2), k='pha', s='phố sập dần thành THE RUINS (plan 1786)'), dict(t=9.5, k='lua', s='khói pháo hai phía 1781–82')],
        'lính phá kho (2h, S063): nhóm lính trên Main Street — số/vị trí minh hoạ (bậc 5); phố sập theo vùng RUINS Drinkwater 1786 (bậc 1); thẻ 205 328 / 258 387 bỏ (lời mang số)')
    D = d(['KA1782'])
    o = base(time=[dict(t=0, at='1782-09-10 10:30', sun=10.5, lab='y'), dict(t=D, at='1782-09-10 10:31', sun=10.5, lab='y')], co=co_lw(), recl=False,
             units=[dict(at=[-445 + 6 * i, -1235 + 18 * i], heading=170, rows=2, cols=4, side='gb', day=[1782.5, 1783.2], seed=1000 + i, rim=False) for i in range(3)])
    add('KA1782', ['KA1782'], 'neo KA', 'neo', 'then-now', 'thanh_pho', 'neo', o, neo_cam(-460, -1450, 60, 10, D, fov=44, up=-14), [('pho_hep', None)],
        [dict(t=0.0, k='nguoi', s='phố đổ nát 9/1782 (vùng THE RUINS), đồn trú')], 'KHUNG NEO nâng 60 m (soi: tầm mắt ở tư thế G1b chỉ thấy quảng trường trống/tường — phố 9/1782 trong vùng THE RUINS đã sập) — nhìn bắc dọc Main Street: phố đổ nát 9/1782; cặp then/now với KA2026', goc='cao', khung_neo=True)
    D = d(['2o', '2p']); tair = NH['2p']['bd_phim'] - NH['2o']['bd_phim']
    dig = [dict(at=[-40 + 25 * i, 210 + 8 * i, -760 - 10 * i], t=[0.6 + 2.2 * i, 1.6 + 2.2 * i], n=6, size=10, rise=14, drift=[1, 0], period=0.3, seed=1010 + i, alpha=0.6) for i in range(4)] + \
          [dict(at=[30, 225, -790], t=[round(tair + 0.3, 2), round(tair + 4.5, 2)], n=16, size=34, rise=40, drift=[1.5, 0.3], period=0.35, seed=1020, alpha=0.85)]
    o = base(time=[dict(t=0, at='1782-05-25 12:00', sun=15.0, lab='d'), dict(t=tair, at='1782-07-10 12:00', sun=15.0, lab='d'), dict(t=D, at='1782-07-31 12:00', sun=15.0, lab='d')], smoke=dig, co=co_ld(), recl=False)
    cam, ct = cuts(D, [dict(t1=tair, p0=[-60, 75, 650], l0=[-20, 190, -800], dp=(5, -2, -15), fov=36), dict(p0=[650, 95, 280], l0=[30, 205, -790], dp=(-8, -1, -6), fov=32)])   # ANIM-V2 R1/R3: máy hạ ≈ 1,4 km trước vách bắc → 2 góc (đào · nổ lỗ thông hơi)
    add('N2.10', ['2o', '2p'], 'D-vach-thap → E-vach', 'chat', 'co-che', 'eo_dat', 'vach', o, cam, [('vach_bac', None)],
        [dict(t=0.6, k='xay', s='bụi đào ở vách bắc (đường hầm Ince, từ 25/5/1782)'), dict(t=round(tair + 0.3, 2), k='no', s='7/1782: nổ thủng lỗ thông hơi — khói phụt ra mặt vách')],
        'GIỮ CHỖ mặt cắt hầm (M11 chưa có); ANIM-V2 R1/R3: máy hạ 75–95 m, vách bắc chiếm khung (cả khối Rock trong khung), 2 góc: bụi đào → nổ lỗ thông hơi; bụi/khói đào: thời điểm bậc 2 (lời 2o–2p), vị trí trên vách ƯỚC TÍNH (bậc 5); footage 2p không dùng', cat=ct)
    D = d(['2j'])
    # ANIM-V2: sửa lỗi cũ — opt.fires nhận at = [E, N]; bản trước ghi [E, 6, N] → lửa đặt ở N = 6 và quầng lửa lơ lửng cao N m trên trời (thấy ở đêm 8/9/1782)
    rh = [dict(at=[e, n], wY=[dy('1782-09-08 07:30') + 0.00012 * i, dy('1782-09-09 06:00')], size=40) for i, (e, n) in enumerate(WORKS82)]
    o = base(time=[dict(t=0, at='1782-09-08 06:30', sun='real', lab='dt'), dict(t=D, at='1782-09-08 21:00', sun='real', lab='dt')], night=True, fires=rh, recl=False, co=co_ld() + co_lw(),
             smoke=[dict(at=[f['at'][0], 8, f['at'][1]], wY=f['wY'], n=16, size=70, rise=130, drift=[-2.5, 1], period=0.4, seed=1030 + i, alpha=0.9, dark=True, fire=0.7) for i, f in enumerate(rh)])
    add('N2.7', ['2j'], 'D-bac-thap', 'lai', 'co-che', 'eo_dat', 'eo', o, hold([130, 48, 680], [100, 25, 200], 44, D, (-8, -1, 4)), [('cong_su_tbn', None)],   # ANIM-V2 R1: máy hạ 320 → 70 m, cách công sự ≈ 500 m
        [dict(t=1.0, k='lua', s='8/9/1782: đạn nung đỏ — tuyến song song TBN bốc cháy lần lượt'), dict(t=10.0, k='ngay_dem', s='tối 8/9: lửa còn cháy')],
        '(soi 1: từ đỉnh Rock công sự quá nhỏ) từ phía Línea nhìn nam: công sự tiền phương TBN cháy trước vách bắc Rock — (lines1782_tp, bậc 1 thấp) cháy theo S059; vệt đạn không vẽ (chưa có nguồn quỹ đạo)')
    D = d(['2k', '2l'])
    big = [dict(n=24, center=[-4300, 1300], axis=150, spacing=230, kind='line', heading=110, wY=[dy('1782-09-11 14:00'), 1783.1], phe='es', soai=12),   # soi 2: bản có path không hiện → hai đợt thả neo theo giờ (11/9 chiều, 12/9 sáng); vị trí minh hoạ
           dict(n=23, center=[-4900, 400], axis=150, spacing=230, kind='line', heading=110, wY=[dy('1782-09-12 08:00'), 1783.1], phe='es', soai=11)]
    bt = [dict(list=[dict(at=[-6300 + 70 * i, -1700 + 60 * i], kind='battery') for i in range(10)], heading=60, wY=[1782.69, 1783.0], phe='es', coScale=1.5)]
    o = base(time=[dict(t=0, at='1782-09-11 09:00', sun='real', lab='dt'), dict(t=D, at='1782-09-12 15:00', sun='real', lab='dt')], fleets=big + bt, co=co_ld() + co_lw(), recl=False)   # BAN-CUOI-T3 1e: giờ thật (đêm 11→12/9 thấy được)
    N28cam, ct28 = cuts(D, [dict(t1=12.5, p0=[-8200, 600, -2600], l0=[-2600, 0, -200], dp=(60, -5, 20), fov=36), dict(p0=[-6800, 180, -1800], l0=[-2500, 10, -100], dp=(50, -2, 20), fov=38)], giu=True)   # BAN-CUOI-T3 1e: khung tĩnh neo 17,46 s → 2 góc
    add('N2.8', ['2k', '2l'], 'B-cao-lai → Al-pin-thap', 'lai', 'co-che', 'bien', 'vinh', o, N28cam, [('ham_doi_lien_quan', None)],
        [dict(t=1.0, k='tau', s='hạm đội Pháp–TBN trong vịnh (47 tàu chiến, số phía Anh)'), dict(t=round(D * 5 / 30, 2), k='tau', s='11/9 chiều: đợt 1 hạm đội thả neo'), dict(t=round(D * 10.5 / 30, 2), k='ngay_dem', s='hoàng hôn 11/9'),
         dict(t=12.5, k='may', s='góc 2 thấp hơn: pin nổi tiền cảnh, hạm đội + Rock nền'), dict(t=round(D * 22 / 30, 2), k='ngay_dem', s='rạng sáng 12/9'), dict(t=round(D * 23 / 30, 2), k='tau', s='12/9 sáng: đợt 2 hạm đội thả neo')],
        '(soi 1–2 + soát LOOK-4: hạm đội sau lưng máy / khung gần như chỉ còn nước → gần hơn, 36°) từ tây vịnh nhìn đông-nam qua hàng neo tới Rock: hạm đội tiền cảnh, Rock nền giữa; 47 tàu chiến = số phía Anh (lời 2k); vị trí hàng neo minh hoạ (bậc 5, theo Faden 1783 phía Algeciras); pin nổi ở Algeciras 12/9 (S066); BAN-CUOI-T3 1e: 2 góc', cat=ct28)
    D = d(['2m', '2n']); dive_at = round(D - 11.5, 3)
    v = V['H2']; bf = [f for f in v['opt']['fleets'] if any(k.get('kind') == 'battery' for k in (f.get('list') or []))]
    o = base(time=[dict(t=0, at='1782-09-13 06:45', sun='real', lab='dt'), dict(t=dive_at, at='1782-09-13 15:30', sun='real', lab='dt'),   # sau dive_at: đường thời gian của clip cú lặn (dive-opt.json t 5,5 → 17,0) → bộ đếm khung ghép đúng giờ clip
                   dict(t=dive_at + 0.5, at='1782-09-13 16:00', sun='real', lab='dt'), dict(t=dive_at + 3.0, at='1782-09-13 23:00', sun='real', lab='dt'), dict(t=dive_at + 9.5, at='1782-09-14 02:30', sun='real', lab='dt'),
                   dict(t=D, at='1782-09-14 05:54', sun='real', lab='dt')], night=True,
             fleets=copy.deepcopy(bf) + big, fires=copy.deepcopy(v['opt']['fires']), smoke=copy.deepcopy(v['opt']['smoke']), co=co_ld() + co_lw(), recl=False, lamps=dict(box=[-3000, -2600, 600, 800]))
    dcam = json.loads((REPO / 'design/pt/cpu/dive-opt.json').read_text())['cam']
    add('N2.9', ['2m', '2n'], 'B-lan', 'lai+lan', 'buoc-ngoat', 'bien', 'vinh', o, [K(0, dcam[0]['p'], dcam[0]['l'], 42), K(dive_at, [-2933, 437, 142], [-1083, 0, -992], 42)], [('pin_noi', None)],
        [dict(t=1.0, k='tau', s='13/9/1782 sáng: 10 pin nổi vào vị trí dưới hoả lực'), dict(t=9.0, k='lua', s='khai hoả'), dict(t=dive_at, k='may', s='CÚ LẶN (Cycles GPU): chiều → đêm cháy → rạng sáng'),
         dict(t=round(dive_at + 3.0, 2), k='ngay_dem', s='đêm: pin nổi cháy'), dict(t=round(dive_at + 4.5, 2), k='may', s='lướt 15–17 m dọc hàng pin nổi cháy'), dict(t=round(dive_at + 8.0, 2), k='may', s='ngược lên cao'),
         dict(t=round(dive_at + 9.5, 2), k='ngay_dem', s='02:30 → rạng sáng 14/9')],
        f'0 → {dive_at} s cách A (máy theo đường máy cú lặn); {dive_at} → {D} s DỰNG TRỌN bằng Cycles GPU (RunPod, §14.2–14.3; scripts/k2tl/cuoi_gpu/) theo đường máy design/pt/cpu/dive-opt.json τ 5,5 → 17,0 — không ghép A↔B trong cú máy',
        lan=dict(cycles_gpu=True, t=dive_at, dur=round(D - dive_at, 3), dive_tau=[5.5, 17.0]))
    D = d(['2q', '2r']); tpeace = NH['2q']['cau'][1]['bd_phim'] - NH['2q']['bd_phim']
    o = base(time=[dict(t=0, at='1782-10-01 12:00', sun=14.0, lab='m'), dict(t=tpeace, at='1783-01-25 12:00', sun=14.0, lab='d'), dict(t=tpeace + 6.0, at='1783-02-05 15:00', sun=14.0, lab='d'),
                   dict(t=tpeace + 6.05, at=1783.10, sun=14.0, lab='m'), dict(t=D, at=1783.32, sun=14.0, lab='m')], co=co_ld() + co_lw(), recl=False, campTuNhien=True,   # ANIM-V2: trại rút hết ngay trước cuối shot (hết khúc đồng trống dài)
             smoke=[dict(at=[e, 8, n], wY=[dy('1783-02-05 10:00'), dy('1783-02-05 16:00')], n=10, size=60, rise=60, drift=[-2, 1], period=0.3, seed=1040 + i, alpha=0.8) for i, (e, n) in enumerate(WORKS82[1:4])])
    cam, ct = cuts(D, [dict(t1=tpeace, p0=[300, 90, 820], l0=[-100, 60, -600], dp=(-10, -2, -10), fov=42), dict(t1=round(tpeace + 8.0, 3), p0=[-60, 42, 650], l0=[60, 20, -200], dp=(5, -1, -5), fov=40),
                       dict(p0=A(-1150, 70, 3550), l0=A(-1300, 0, 2950), dp=(5, 0, -10), fov=44)])   # ANIM-V2 R1/R3: công sự + Rock (mùa đông 1782) → cận khẩu đội bắn phát cuối 5/2/1783 → trại rút 1783
    add('N2.11', ['2q', '2r'], 'D-bac-thap → W-cong-su → T-trai-bac', 'lai', 'he-qua', 'eo_dat', 'trai', o, cam, [('trai', None)],
        [dict(t=0.5, k='tau', s='phong toả tiếp tục mùa đông 1782'), dict(t=round(tpeace + 5.5, 2), k='lua', s='5/2/1783: phát súng cuối'), dict(t=round(tpeace + 7, 2), k='pha', s='trại + công sự TBN rút dần 1783')],
        'ANIM-V2 R1/R3: 3 góc thấp 42–95 m — công sự tiền phương + Rock (mùa đông 1782) → cận công sự, khói phát súng cuối 5/2/1783 → dải trại rút theo cửa sổ năm (eo-dat-v7.json, bậc 1–2) nhìn nam về Rock; thẻ tổn thất 2r bỏ (lời mang số)', cat=ct)
    # ===== CHƯƠNG 3 · ĐẤT TRUNG LẬP (382,583 → 471,625) =====
    D = d(['3a', '3b']); t1810 = NH['3b']['bd_phim'] - NH['3a']['bd_phim']
    blow = [dict(at=[f[0], 10, f[1]], t=[round(t1810 + 4.2 + 0.6 * i, 2), round(t1810 + 9.5, 2)], n=20, size=110, rise=160, drift=[-2, 1], period=0.4, seed=1050 + i, alpha=0.9, fire=0.6) for i, f in enumerate([FT_SF, FT_SB])]
    o = base(time=[dict(t=0, at=1783.6, sun=14.0, lab='y'), dict(t=t1810 - 0.05, at=1809.9, sun=14.0, lab='y', hold=True), dict(t=t1810, at='1810-02-14 08:00', sun='real', lab='dt'), dict(t=D, at='1810-02-14 17:00', sun='real', lab='dt')],
             smoke=blow, co=co_ld() + co_lw(), recl=False, doiSong=DS_N31,
             lives=[dict(era=1782, wY=dict(on=1783.6), walkers=[dict(line='LO', n=40, width=3, colors=ES1704 + CIV)], lines=dict(LO=[[-120, 1780], [-20, 1560], [30, 1300], [60, 1100]]))])
    cam, ct = cuts(D, [dict(t1=round(t1810, 3), p0=A(90, 38, 1760), l0=[-60, 100, -700], dp=(6, 0, -4), fov=28), dict(p0=[1150, 55, 1450], l0=[860, 15, 930], dp=(-10, -2, -8), fov=42)])   # ANIM-V2 R2/R3: hạ máy về hai đồn Línea, Rock nền
    add('N3.1', ['3a', '3b'], 'SF-thap → SB-thap', 'lai', 'buoc-ngoat', 'eo_dat', 'eo', o, cam, [('linea', None)],
        [dict(t=0.4, k='the_chuong', s='1783 — The neutral ground'), dict(t=3.0, k='dem_nam', s='1783 → 1809: dải cát giữa tường và Línea'), dict(t=round(t1810 + 4.2, 2), k='no', s='14/2/1810: hai pháo đài Línea nổ tung')],
        'MỐC ĐINH 1810: khói nổ ở San Felipe + Santa Bárbara (ghost SH, bậc 1); Línea biến mất 14/2/1810 (eo-dat-v7.json); dải trung lập không tô (§10.7); ANIM-V2 R2/R3: 2 góc thấp — đồn San Felipe + Línea (1783 → 1809, Rock nền) → đồn Santa Bárbara nổ 14/2/1810', chuong='1783 — The neutral ground', cat=ct)
    D = d(['3c'])
    o = base(time=[dict(t=0, at=1810.3, sun=14.0, lab='y'), dict(t=D, at=1860.0, sun=14.0, lab='y')], co=co_ld() + co_lw(), recl=False)
    add('N3.2', ['3c'], 'B-thap', 'lai', 'co-che', 'thanh_pho', 'pho', o, hold([-1750, 95, -900], [-560, 20, -1150], 40, D, (25, -2, -10)), [('pho_cang', None)],   # ANIM-V2 R4: lời không có vật trên eo đất → phố + cảng mọc theo năm 1810 → 1860
        [dict(t=0.5, k='dem_nam', s='1810 → 1860 trên dải trung lập')],
        'GIỮ CHỖ: lớp "mép đất Anh tiến dần 1810–60" chưa có nguồn bậc 1–3; ANIM-V2 R4: góc phố + cảng từ vịnh (nhà theo năm xây có trong gói, tàu theo năm) thay eo đất trống; Sayer 1865 chưa nắn khớp')
    D = d(['3d'])
    o = base(time=[dict(t=0, at=1849.0, sun=15.0, lab='y'), dict(t=D * 0.5, at=1870.0, sun=15.0, lab='y'), dict(t=D, at=1905.0, sun=15.0, lab='y')], recl=False, co=co_ld(), doiSong=DS_N33)
    add('N3.3', ['3d'], 'H-lai', 'lai', 'co-che', 'thanh_pho', 'pho', o, hold([330, 40, 2450], [-20, 70, -700], 22, D, (-10, 0, -8)), [('la_linea', None)],
        [dict(t=0.5, k='xay', s='La Línea mọc theo năm xây (Catastro) 1849 → 1905')], 'nhà La Línea theo năm xây Catastro (bậc 1 cho năm có; nhà thiếu năm theo quy ước gói)')
    D = d(['KC1910'])
    o = base(time=[dict(t=0, at='1910-06-15 10:30', sun=10.5, lab='y'), dict(t=D, at='1910-06-15 10:31', sun=10.5, lab='y')], recl=False,
             lives=[dict(era=1910, wY=dict(on=1900), walkers=[dict(line='CALLE', n=24, width=5, colors=CIV)], lines=dict(CALLE=[[152, 1350], [160, 1390], [170, 1440], [180, 1490]]))])
    add('KC1910', ['KC1910'], 'neo KC', 'neo', 'then-now', 'thanh_pho', 'neo', o, neo_cam(150, 1340, 2.6, 12, D, fov=40), [('pho_la_linea', None)],
        [dict(t=0.0, k='nguoi', s='phố La Línea 1910')], 'KHUNG NEO tầm mắt — cặp then/now với KC2026 (tư thế máy G1b: E 150, N 1340, hướng 12°)', goc='thap', khung_neo=True)
    D = d(['3e', '3f', '3g']); t09 = NH['3f']['bd_phim'] - NH['3e']['bd_phim']; t30 = NH['3g']['bd_phim'] - NH['3e']['bd_phim']
    o = base(time=[dict(t=0, at=1900.0, sun=14.0, lab='y'), dict(t=t09, at=1908.8, sun=14.0, lab='y'), dict(t=t30, at=1909.7, sun=14.0, lab='y'), dict(t=D, at=1930.0, sun=14.0, lab='y')], recl=False, co=co_ld(), doiSong=DS_N34,
             lives=[dict(era=1910, wY=dict(on=1900), walkers=[dict(line='EO', n=120, width=4, colors=CIV)], lines=dict(EO=ROAD_EO[:5]))])
    cam, ct = cuts(D, [dict(t1=round(t09, 3), p0=[150, 42, 1150], l0=[80, 10, 450], dp=(-5, -1, -8), fov=42), dict(p0=[120, 30, 900], l0=[20, 140, -700], dp=(-8, 0, -4), fov=27)])   # ANIM-V2 R2/R3: mép nam La Línea nhìn về Rock → dọc hàng rào 1909
    add('N3.4', ['3e', '3f', '3g'], 'H-thap → F-hang-rao', 'lai', 'buoc-ngoat', 'eo_dat', 'eo', o, cam, [('hang_rao', None)],
        [dict(t=0.5, k='dem_nam', s='dải trung lập giữa hai phố 1900'), dict(t=round(t09 + 1.0, 2), k='xay', s='hàng rào 1909 mọc dọc mép (MỐC ĐINH)'), dict(t=round(t30, 2), k='dem_nam', s='1909 → 1930')],
        'hàng rào 1909: tuyến coi trùng ranh OSM 2026 (ƯỚC TÍNH, eo-dat-v7.json); trại lính/vườn/trường bắn/trường đua 3g CHƯA dựng (chưa có nguồn vị trí bậc 1) — giữ chỗ; ANIM-V2 R2/R3: 2 góc thấp (phố La Línea 1900 + Rock → dọc hàng rào mọc 1909)', cat=ct)
    D = d(['3h'])
    o = base(time=[dict(t=0, at=1933.5, sun=14.0, lab='y'), dict(t=D, at=1938.5, sun=14.0, lab='y')], recl=False, co=co_ld(), grassStrip=dict(w=dict(on=1934.0, full=1936.0, off0=1939.8, off1=1940.0)), doiSong=DS_N35)
    add('N3.5', ['3h'], 'D2-thap', 'lai', 'co-che', 'eo_dat', 'eo', o, hold([-380, 55, 650], [-60, 40, -650], 42, D, (10, -1, -6)), [('dai_co', None)],   # ANIM-V2 R2: hạ máy, Rock chiếm khung, dải cỏ ngang tiền cảnh
        [dict(t=0.5, k='xay', s='dải cỏ cắt làm đường bay 1934–36')], 'soát LOOK-4: Rock chạm mép phải → xoay máy; dải cỏ 1934 (lời 3h): năm bậc 2 (lời), vị trí/bề rộng ƯỚC TÍNH (bậc 5) trên trục đường băng hiện nay')
    # ===== CHƯƠNG 4 · ĐƯỜNG BĂNG (471,625 → 585,833) =====
    D = d(['4a', '4b']); t41 = NH['4b']['cau'][1]['bd_phim'] - NH['4a']['bd_phim']
    o = base(time=[dict(t=0, at=1939.2, sun=11.0, lab='m'), dict(t=t41, at=1939.85, sun=11.0, lab='m'), dict(t=D, at=1941.6, sun=11.0, lab='m')], recl=True, co=co_ld(),
             lives=[dict(era=1941, wY=dict(on=1939.0, off0=1946), walkers=[dict(line='WCA', n=40, width=5, women=False, colors=MIL43)])], doiSong=DS_N41)
    cam, ct = cuts(D, [dict(t1=round(t41, 3), p0=[300, 30, 760], l0=[-40, 100, -700], dp=(-10, 0, -5), fov=28), dict(p0=[-450, 45, 380], l0=[150, 20, -350], dp=(10, -1, -5), fov=42)])   # ANIM-V2 R2/R3: hạ máy sát đường băng đang mọc, Rock chiếm nền
    add('N4.1', ['4a', '4b'], 'D-thap-dong → D-thap-tay', 'lai', 'buoc-ngoat', 'eo_dat', 'eo', o, cam, [('cho_cat', None)],
        [dict(t=0.4, k='the_chuong', s='1939 — A runway on the sand'), dict(t=round(t41, 2), k='xay', s='cuối 1939: mặt đường băng cứng mọc'), dict(t=round(D - 3, 2), k='xay', s='1941: đường băng cắt qua con đường duy nhất sang TBN')],
        'đường băng mọc theo uRecl (S091–S092); ảnh NARA 4a không dùng (TL-4); ANIM-V2 R2/R3: 2 góc thấp 40–45 m dọc đường băng', chuong='1939 — A runway on the sand', cat=ct)
    D = d(['4c', '4d', '4e'])
    q = [dict(at=[150 + 40 * i, 120 + 15 * i, -760], wY=[1941.6 + 0.25 * i, 1943.5], n=10, size=40, rise=50, drift=[1.5, 0.3], period=0.4, seed=1060 + i, alpha=0.7) for i in range(5)]
    o = base(time=[dict(t=0, at=1941.6, sun=15.0, lab='m'), dict(t=d(['4c']), at=1943.0, sun=15.0, lab='m'), dict(t=D, at=1943.6, sun=15.0, lab='m')], recl=True, co=co_ld(), smoke=q,
             fleets=[dict(list=[dict(at=[-1400 + 160 * i, -300 - 40 * i], kind='steam') for i in range(4)], heading=80, wY=[1941, 1946])])
    cam, ct = cuts(D, [dict(t1=round(d(['4c']), 3), p0=[-1600, 70, 450], l0=[-500, 5, 0], dp=(20, -1, -5), fov=42), dict(p0=[-60, 75, 650], l0=[-20, 190, -800], dp=(5, -2, -12), fov=36)])   # ANIM-V2 R2/R3: đường băng lấn vịnh nhìn từ vịnh → vách bắc (bụi đá)
    add('N4.2', ['4c', '4d', '4e'], 'W-vinh-thap → D-vach-thap', 'lai', 'co-che', 'eo_dat', 'eo', o, cam, [('duong_bang', None)],
        [dict(t=0.5, k='xay', s='đường băng lấn vịnh theo tháng 1941–43'), dict(t=3.0, k='lua', s='bụi đá nổ ở vách bắc')],
        'GIỮ CHỖ mặt cắt hầm (M11, ONI 1954) chưa có: lời 4d–4e trên khung vách bắc + đường băng lấn vịnh; bụi đá: vị trí ước tính (bậc 5); thẻ "55 km" bỏ (lời mang số); ANIM-V2 R2/R3: 2 góc thấp (đường băng từ vịnh → vách bắc)', cat=ct)
    D = d(['4f'])
    o = base(time=[dict(t=0, at=1943.3, sun=14.0, lab='y'), dict(t=D, at=1943.7, sun=14.0, lab='y')], recl=True, co=co_ld() + co_lw())
    add('N4.3', ['4f'], 'B-lai', 'lai', 'co-che', 'thanh_pho', 'pho', o, hold([-2300, 430, -650], [-700, 0, -1250], 40, D, (40, -6, -20)), [('pho_1943', None)],
        [dict(t=0.5, k='xay', s='phố 1943 từng nhà (ghost AMS M981) + đường băng vươn ra vịnh')],
        'phố 1943 = lớp ghost AMS M981 1943 (bậc 1); bản đồ phẳng không phủ (chưa nắn khớp trong gói animatic)')
    D = d(['SM3', '4g'])
    o = base(time=[dict(t=0, at='1940-05-20 12:00', sun=15.0, lab='d'), dict(t=5.5, at='1940-05-26 12:00', sun=15.0, lab='d'), dict(t=5.55, at=1940.5, sun=15.0, lab='m'), dict(t=D, at=1942.8, sun=15.0, lab='m')], recl=True, co=co_ld() + co_lw(),
             fleets=[dict(list=[dict(at=[-700 - 90 * i, -900 - 60 * i], kind='steam') for i in range(6)], heading=230, wY=[1940.3, dy('1940-05-27 00:00')], path=[[dy('1940-05-21 00:00'), 0, 0], [dy('1940-05-26 00:00'), -2600, -1700]])],
             mayBay=dict(n=650, w=dict(on=1941.8, full=1942.84)))
    add('N4.4', ['SM3', '4g'], 'Bb-lai', 'lai', 'co-che', 'bien', 'vinh', o, hold([-2650, 600, -2600], [-750, 0, -800], 42, D, (40, -8, 20)), [('so_tan', [0, 5.5]), ('may_bay', [5.5, 99])],
        [dict(t=0.5, k='tau', s='5/1940: tàu sơ tán phụ nữ–trẻ em rời cảng'), dict(t=6.0, k='may_bay', s='1941–42: máy bay tụ dần trên đường băng')],
        'thay bản đồ chiến lược SM3 + mũi tên 4g: tàu sơ tán rời cảng (6 tàu — số minh hoạ); máy bay = khối minh hoạ (bậc 5, chờ D3); Tangier không lên hình')
    D = d(['KB1943'])
    o = base(time=[dict(t=0, at='1943-06-15 11:00', sun=11.0, lab='y'), dict(t=D, at='1943-06-15 11:01', sun=11.0, lab='y')], recl=True,
             lives=[dict(era=1941, wY=dict(on=1939), walkers=[dict(line='SQ', n=30, width=8, women=False, colors=MIL43)], lines=dict(SQ=[[-470, -1110], [-440, -1150], [-420, -1190]]))])
    add('KB1943', ['KB1943'], 'neo KB', 'neo', 'then-now', 'thanh_pho', 'neo', o, neo_cam(-380, -1230, 30, 320, D, fov=44, up=-12), [('quang_truong', None)],
        [dict(t=0.0, k='nguoi', s='phố 1943 nhìn ra vịnh (tấm im lặng: phụ nữ, trẻ em đã sơ tán)')], 'TẤM IM LẶNG + KHUNG NEO nâng 30 m (cặp then/now với KB2026); nhà 1943 = nhà 2026 (OSM không có năm xây — giới hạn dữ liệu)', goc='cao', khung_neo=True)
    D = d(['4h', '4i']); tn = NH['4i']['bd_phim'] - NH['4h']['bd_phim']
    o = base(time=[dict(t=0, at=1942.30, sun=15.0, lab='m'), dict(t=tn, at='1942-11-07 12:30', sun='real', lab='dt'), dict(t=D, at='1942-11-07 16:20', sun='real', lab='dt')], recl=True, night=True, co=co_ld(),
             mayBay=dict(n=650, w=dict(on=1941.8, full=1942.84)), fleets=[dict(list=[dict(at=[-3500 + 250 * i, -5200 + 120 * i], kind='steam') for i in range(10)], heading=80, wY=[dy('1942-11-07 12:00'), 1943])])
    add('N4.5', ['4h', '4i'], 'D-duongbang', 'lai', 'buoc-ngoat', 'eo_dat', 'eo', o, hold([300, 230, 250], [-700, 0, -20], 40, D, (-40, -3, -10)), [('may_bay', None)],
        [dict(t=0.5, k='may_bay', s='máy bay xếp kín hai bên đường băng'), dict(t=round(tn, 2), k='ngay_dem', s='chiều → tối 7/11/1942'), dict(t=round(tn + 9, 2), k='tau', s='đoàn tàu đổ bộ qua eo biển')],
        '≥ 650 máy bay (lời 4i, bậc 2) = khối minh hoạ (bậc 5); để chiều → chạng vạng 7/11 cho đọc được (soi 1: 19:30 tối đen) (lời: "the night of"); đoàn tàu qua eo: số/vị trí minh hoạ')
    # ===== CHƯƠNG 5 · CỔNG (585,833 → 745,0) =====
    D = d(['5a', '5b']); t69 = NH['5a']['cau'][1]['bd_phim'] - NH['5a']['bd_phim']; t85 = NH['5b']['cau'][1]['bd_phim'] - NH['5a']['bd_phim']
    # BAN-CUOI-T3 (1d, XEM CÂM Q7 0/6): góc A thấp nhìn qua cổng về Rock — dòng người/xe qua lại → 8/6/1969 (lời "closed the land frontier completely") rào chắn hạ ngang đường,
    #  người + xe DỪNG ở hai phía (≥ 4 s), rồi tản dần · góc B (góc cao cũ): cổng vắng 1969 → 1985 mở lại. Người/xe dừng, rào chắn: hình minh hoạ (bậc 5, ước lượng) theo mốc có nguồn (lời 5a).
    tA5 = round(t69 + 6.0, 3); tC = t69 + 1.2
    o = base(time=[dict(t=0, at=1966.0, sun=11.0, lab='m'), dict(t=t69, at=1969.40, sun=11.0, lab='m'), dict(t=tC, at='1969-06-08 09:00', sun='real', lab='dt'), dict(t=tA5 - 0.05, at='1969-06-08 19:00', sun='real', lab='dt'),
                   dict(t=tA5, at=1969.50, sun=11.0, lab='m'), dict(t=t85 - 0.5, at=1985.0, sun=11.0, lab='m'), dict(t=D, at=1985.25, sun=11.0, lab='m')], recl=True,
             lives=[dict(era=2026, wY=dict(on=1946, off0=dy('1969-06-08 09:30'), off1=dy('1969-06-08 10:00')), walkers=[dict(line='WCA', n=160, width=6, women=True, colors=MOD)]),
                    dict(era=2026, wY=dict(on=1985.12, full=1985.2), walkers=[dict(line='WCA', n=120, width=6, women=True, colors=MOD)]),
                    dict(era=2026, wY=dict(on=dy('1969-06-08 09:00'), off0=dy('1969-06-08 17:00'), off1=dy('1969-06-08 18:00')), speed=0.03, seed=1969,   # người đứng lại hai phía cổng (gần như yên)
                         walkers=[dict(line='BAC', n=70, width=14, women=True, colors=MOD), dict(line='NAM', n=50, width=14, women=True, colors=MOD)],
                         lines=dict(BAC=[[62, 492], [70, 520], [80, 560], [90, 610]], NAM=[[58, 462], [50, 440], [38, 410], [20, 360]]))],
             doiSong=[dict(kind='rao', pts=[[30, 486], [92, 482]], buoc=2.5, wY=dict(on=dy('1969-06-08 08:30'), full=dy('1969-06-08 09:00'), off0=1985.15, off1=1985.16), seed=5101),   # rào chắn ngang đường ở cổng
                      dict(kind='rao', pts=[[30, 472], [92, 468]], buoc=2.5, wY=dict(on=dy('1969-06-08 08:30'), full=dy('1969-06-08 09:00'), off0=1985.15, off1=1985.16), seed=5102),
                      dict(kind='xe', kieu='tai', pts=[[78, 520], [95, 700], [110, 900]], n=7, v=0.0, wY=dict(on=dy('1969-06-08 09:00'), off0=dy('1969-06-08 18:00')), seed=5103),   # xe dừng phía TBN
                      dict(kind='xe', kieu='tai', pts=[[45, 440], [20, 300], [-30, 100]], n=5, v=0.0, wY=dict(on=dy('1969-06-08 09:00'), off0=dy('1969-06-08 18:00')), seed=5104),
                      dict(kind='xe', kieu='tai', pts=[[110, 900], [70, 520], [-60, 100], [-150, -250]], n=10, v=9.0, hai_chieu=True, wY=dict(on=1946, off0=dy('1969-06-08 08:00')), seed=5105),
                      dict(kind='xe', kieu='tai', pts=[[110, 900], [70, 520], [-60, 100], [-150, -250]], n=8, v=9.0, hai_chieu=True, wY=dict(on=1985.15), seed=5106),
                      dict(kind='kho', at=[95, 500], r=14, n=2, wY=dict(on=1946), seed=5107), dict(kind='kho', at=[25, 450], r=14, n=2, wY=dict(on=1946), seed=5108)])   # trạm gác/lán hải quan chung (không tên, ước lượng)
    cam, ct = cuts(D, [dict(t1=tA5, p0=A(85, 18, 640), l0=[10, 40, -500], dp=(-3, 0, -6), fov=30), dict(t1=15.6, p0=[420, 400, 1700], l0=[-200, 0, 0], dp=(-12, -2, -8), fov=40),
                       dict(p0=A(70, 22, 700), l0=[0, 40, -500], dp=(-3, 0, -6), fov=32)], giu=True)   # BAN-CUOI-T3 1e: góc C thấp ở cổng 1977 → 1985 (rào gỡ, người trở lại)
    add('N5.1', ['5a', '5b'], 'D-cong-thap → D-cong', 'lai', 'buoc-ngoat', 'eo_dat', 'eo', o, cam, [('cong', None)],
        [dict(t=0.4, k='the_chuong', s='1969 — The gate closes'), dict(t=0.5, k='nguoi', s='1966–69: dòng người + xe qua cổng hai chiều (cận, Rock nền)'), dict(t=round(tC, 2), k='nguoi', s='8/6/1969: rào chắn hạ, người và xe dừng ở hai phía cổng'),
         dict(t=tA5, k='may', s='góc cao: cổng vắng 1969 → 1977'), dict(t=15.6, k='may', s='góc thấp ở cổng: rào chắn vẫn đóng (1977 → 1985)'), dict(t=round(t85, 2), k='nguoi', s='1985: rào gỡ, người qua lại trở lại')],
        'BAN-CUOI-T3 1d: góc thấp có Rock — cổng đóng thành biến cố thấy được ≥ 4 s (rào chắn + người/xe dừng hai phía; minh hoạ bậc 5 theo mốc lời 5a); góc cao giữ từ v2; dòng người theo năm (lời 5a–5b, bậc 2)', chuong='1969 — The gate closes', cat=ct)
    D = d(['KB2026'])
    o = base(time=[dict(t=0, at='2026-10-18 11:00', sun=11.0, lab='y'), dict(t=D, at='2026-10-18 11:01', sun=11.0, lab='y')],
             lives=[dict(era=2026, wY=dict(on=1990), walkers=[dict(line='SQ', n=40, width=8, women=True, colors=MOD)], lines=dict(SQ=[[-470, -1110], [-440, -1150], [-420, -1190]]))])
    add('KB2026', ['KB2026'], 'neo KB', 'neo', 'then-now', 'thanh_pho', 'neo', o, neo_cam(-380, -1230, 30, 320, D, fov=44, up=-12), [('quang_truong', None)],
        [dict(t=0.0, k='nguoi', s='cùng góc phố hôm nay')], 'KHUNG NEO "the same square, today" — cùng tư thế máy KB1943 (nâng 30 m)', goc='cao', khung_neo=True)
    D = d(['5c', '5d']); tside = NH['5d']['bd_phim'] - NH['5c']['bd_phim']
    o = base(time=[dict(t=0, at='2026-10-19 08:10', sun='real', lab='dt'), dict(t=D, at='2026-10-19 08:40', sun='real', lab='dt')],
             lives=[dict(era=2026, wY=dict(on=2020), walkers=[dict(line='WCA', n=220, width=6, women=True, colors=MOD)], crowds=[dict(line='WCA', groups=12, size=[4, 12], speed=1.3, colors=MOD)])])
    N52cam, ct52 = cuts(D, [dict(t1=4.3, p0=[-260, 200, -380], l0=[150, 0, 450], dp=(70, 5, 260), fov=40), dict(p0=[40, 60, 180], l0=[150, 0, 1300], dp=(8, 0, 25), fov=38)], giu=True)   # BAN-CUOI-T3 1e: 2 góc
    add('N5.2', ['5c', '5d'], 'D → H', 'lai', 'co-che', 'eo_dat', 'eo', o,
        N52cam, [('nguoi_qua_cong', None)],
        [dict(t=0.5, k='nguoi', s='người đi bộ băng qua đường băng giờ cao điểm 2026'), dict(t=4.3, k='may', s='góc 2: thấp sau cổng nhìn bắc — dòng người sang La Línea'), dict(t=round(tside, 2), k='nguoi', s='dòng người qua cổng sang phía La Línea (lời 5d)')],
        'thay follow-object A-lite bằng khung lai trôi dọc dòng người: đường băng → cổng → La Línea (lời 5d "the other side of the gate"); đổi điểm D → H (BAI-HOC #96, D ≤ 25 %); BAN-CUOI-T3 1e: 2 góc (cắt 4,3 s)', cat=ct52)
    D = d(['KC2026'])
    o = base(time=[dict(t=0, at='2026-10-18 10:30', sun=10.5, lab='y'), dict(t=D, at='2026-10-18 10:31', sun=10.5, lab='y')],
             lives=[dict(era=2026, wY=dict(on=1990), walkers=[dict(line='CALLE', n=20, width=5, women=True, colors=MOD)], lines=dict(CALLE=[[152, 1350], [160, 1390], [170, 1440], [180, 1490]]))])
    add('KC2026', ['KC2026'], 'neo KC', 'neo', 'then-now', 'thanh_pho', 'neo', o, neo_cam(150, 1340, 2.6, 12, D, fov=40), [('pho_la_linea', None)],
        [dict(t=0.0, k='nguoi', s='cùng phố La Línea hôm nay')], 'KHUNG NEO "Remember this street?" — cùng tư thế máy KC1910', goc='thap', khung_neo=True)
    D = d(['5e', '5f'])
    o = base(time=[dict(t=0, at='2026-10-19 07:30', sun='real', lab='dt'), dict(t=D * 0.45, at='2026-10-19 09:30', sun='real', lab='dt'), dict(t=D * 0.5, at='2026-10-19 14:00', sun='real', lab='dt'),
                   dict(t=D * 0.72, at='2026-10-19 15:30', sun='real', lab='dt'), dict(t=D * 0.72 + 0.3, at='2026-10-19 17:40', sun='real', lab='dt'), dict(t=D, at='2026-10-19 18:30', sun='real', lab='dt')],
             lives=[dict(era=2026, wY=dict(on=2020), walkers=[dict(line='WCA', n=260, width=6, women=True, colors=MOD)], crowds=[dict(line='WCA', groups=14, size=[4, 12], speed=1.3, colors=MOD)]),
                    dict(era=2026, wY=dict(on=dy('2026-10-19 17:30')), seed=2027, walkers=[dict(line='WCA', n=220, width=6, women=True, colors=MOD)])])   # BAN-CUOI-T3 1e: giờ tan tầm, dòng người về đông lên (minh hoạ bậc 5)
    N53cam, ct53 = cuts(D, [dict(t1=8.0, p0=[620, 560, 3050], l0=[-120, 0, 650], dp=(-8, -2, -6), fov=40), dict(t1=round(D * 0.5, 3), p0=A(160, 45, 700), l0=[40, 20, 300], dp=(-3, 0, -6), fov=36),
                           dict(p0=[605, 555, 3040], l0=[-120, 0, 650], dp=(-20, -4, -14), fov=40)], giu=True)
    add('N5.3', ['5e', '5f'], 'H-lai → D-cong-thap → H-lai', 'lai', 'co-che', 'thanh_pho', 'pho', o, N53cam, [('nguoi_qua_cong', None)],
        [dict(t=0.5, k='nguoi', s='sáng: dòng người từ La Línea sang Gibraltar'), dict(t=round(D * 0.45 * 65 / 120, 2), k='ngay_dem', s='mặt trời mọc (≈ 08:35)'), dict(t=8.0, k='may', s='góc 2: cận cổng, dòng người buổi sáng'), dict(t=round(D * 0.5, 2), k='nguoi', s='chiều: dòng người về (góc cao)'),
         dict(t=round(D * 0.72, 2), k='ngay_dem', s='bước giờ 15:30 → 17:40: nắng xế, bóng dài'), dict(t=round(D * 0.72 + 1.2, 2), k='nguoi', s='giờ tan tầm: dòng người về đông lên')],
        'từ La Línea nhìn nam qua cổng tới Rock: hai phố, một dòng người; thẻ £85 000 bỏ (lời mang số); không tô màu hai bên (§10.7); BAN-CUOI-T3 1e: 3 góc + bước giờ chiều', cat=ct53)
    D = d(['5g', '5h', '5i']); tf = NH['5h']['cau'][1]['bd_phim'] - NH['5g']['bd_phim']
    o = base(time=[dict(t=0, at='2026-07-14 10:00', sun=11.0, lab='d'), dict(t=tf, at='2026-07-20 10:00', sun=11.0, lab='d'), dict(t=D - 6, at='2026-10-10 10:00', sun=11.0, lab='d'), dict(t=D, at='2026-10-18 10:00', sun=11.0, lab='d')],
             fenceOff=[2026.55, 2026.75], fenceNew=dict(off=-6, w=dict(on=2026.55, full=2026.76)),
             lives=[dict(era=2026, wY=dict(on=2020), walkers=[dict(line='WCA', n=220, width=6, women=True, colors=MOD)], crowds=[dict(line='WCA', groups=10, size=[4, 10], speed=1.3, colors=MOD)]),
                    dict(era=2026, wY=dict(on=dy('2026-10-14 00:00')), seed=2028, walkers=[dict(line='WCA', n=160, width=8, women=True, colors=MOD)])],   # BAN-CUOI-T3 1e: dòng người đông lên qua đoạn rào mới (minh hoạ bậc 5)
             pho2026=dict(box=[-700, -200, 900, 1500]))
    # ANIM-V2 (hết "bản đồ trò chơi"): khung lai THẤP có chân trời (45–55 m, nhìn xuống ≈ 6–8°), cây/đèn/xe phố 2026 (duong2026), 2 góc: cổng + dòng người · dọc hàng rào (gỡ cũ, dựng mới)
    cam, ct = cuts(D, [dict(t1=6.3, p0=[40, 40, -150], l0=[70, 0, 350], dp=(4, 0, 5), fov=40), dict(t1=round(tf, 3), p0=A(180, 30, 260), l0=[40, 5, 520], dp=(-4, 0, 4), fov=38), dict(p0=[-120, 35, 150], l0=[150, 2, 500], dp=(10, 0, 6), fov=42)], giu=True)   # BAN-CUOI-T3 1e: thêm góc 2 (cắt 6,0 s)   # soát dựng: góc cũ có bãi cỏ công viên chiếm nửa khung → nhìn bắc từ đường băng qua cổng
    sys.path.insert(0, str(REPO / 'scripts/k2tl')); import cuoi_bien_co as BC0
    ev54 = [dict(t=round(x, 2), k=k, s=m) for Y, k, m in [(2026.65, 'pha', 'nửa tuyến rào cũ đã gỡ'), (2026.715, 'pha', 'đoạn rào cũ cuối đang gỡ'), (2026.76, 'xay', 'hàng rào mới dựng xong'), (dy('2026-10-14 00:00'), 'nguoi', 'dòng người đông lên qua đoạn rào mới')] for x in BC0.t_cua_nam(o, Y, dy)]
    add('N5.4', ['5g', '5h', '5i'], 'D-cong-thap → F-hang-rao', 'lai', 'buoc-ngoat', 'eo_dat', 'eo', o, cam, [('hang_rao', None)],
        [dict(t=0.5, k='nguoi', s='7/2026: kiểm tra thường lệ dừng — người qua cổng không xếp hàng'), dict(t=round(tf + 1, 2), k='pha', s='hàng rào cũ gỡ từng đoạn'), *ev54, dict(t=round(tf + 3, 2), k='xay', s='hàng rào mới lùi vài mét')],
        'hàng rào cũ gỡ (lời 5h, bậc 2) + hàng mới lệch 6 m (ƯỚC TÍNH bậc 5 — chờ nguồn vị trí); khoảng mở ≈ 150 m chưa dựng; thẻ 5i bỏ (lời mang ngày); ANIM-V2: máy thấp có chân trời + phố 2026 có cây/đèn/xe (bậc 5 vật nền phụ)', cat=ct)
    D = d(['5j']); tl = {k: NH['5j']['cau'][i]['bd_phim'] - NH['5j']['bd_phim'] for i, k in [(2, 1704), (3, 1730), (4, 1909), (5, 1941)]}
    ST = 11 / 24
    o = base(time=[dict(t=0, at='2026-10-18 16:00', sun=16.0, lab='y', hold=True), dict(t=tl[1704] - 0.05, at='2026-10-18 16:01', sun=16.0, lab='y', hold=True),
                   dict(t=tl[1704], at=1704.7, sun=16.0, lab='y', hold=True), dict(t=tl[1730] - 0.05, at=1704.71, sun=16.0, lab='y', hold=True),
                   dict(t=tl[1730], at=1735.5, sun=16.0, lab='y', hold=True), dict(t=tl[1909] - 0.05, at=1735.51, sun=16.0, lab='y', hold=True),
                   dict(t=tl[1909], at=1909.7, sun=16.0, lab='y', hold=True), dict(t=tl[1941] - 0.05, at=1909.71, sun=16.0, lab='y', hold=True),
                   dict(t=tl[1941], at=1943.6, sun=16.0, lab='y', hold=True), dict(t=D - 1.2, at=1943.61, sun=16.0, lab='y', hold=True), dict(t=D - 1.15, at=2026.79, sun=16.0, lab='y', hold=True), dict(t=D, at=2026.80, sun=16.0, lab='y')],
             co=co_ld() + co_lw(), pre1704town=True)
    add('N5.5', ['5j'], 'B-lui', 'lai', 'he-qua', 'bien', 'vinh', o, [K(0, [-1900, 520, -2300], [-100, 100, -2000], 44), K(D, [-3400, 900, -900], [-500, 40, -900], 44)], [('lop_lich_su', None)],
        [dict(t=0.5, k='may', s='kéo lùi: Rock giữa vịnh và biển'), dict(t=round(tl[1704], 2), k='buoc_nam', s='1704: tường'), dict(t=round(tl[1730], 2), k='buoc_nam', s='1730: Línea'),
         dict(t=round(tl[1909], 2), k='buoc_nam', s='1909: hàng rào'), dict(t=round(tl[1941], 2), k='buoc_nam', s='1941: đường băng'), dict(t=round(D - 1.15, 2), k='buoc_nam', s='2026')],
        'bookend H2: bước năm khớp từng chữ "A wall in 1704 / A line in 1730 / A fence in 1909 / A runway in 1941" (thay ghost sepia chồng lớp — TL-4)')
    D = d(['KA2026'])
    o = base(time=[dict(t=0, at='2026-10-18 10:30', sun=10.5, lab='y'), dict(t=D, at='2026-10-18 10:31', sun=10.5, lab='y')],
             lives=[dict(era=2026, wY=dict(on=1990), walkers=[dict(line='MAIN', n=30, width=4, women=True, colors=MOD)], lines=dict(MAIN=[[-440, -1320], [-445, -1250], [-440, -1180]]))])
    add('KA2026', ['KA2026'], 'neo KA', 'neo', 'then-now', 'thanh_pho', 'neo', o, neo_cam(-460, -1450, 60, 10, D, fov=44, up=-14), [('pho_hep', None)],
        [dict(t=0.0, k='nguoi', s='cùng phố hôm nay: mái nhà dày đặc')], 'TẤM IM LẶNG + KHUNG NEO nâng 60 m (cặp then/now với KA1782: phố đổ nát 1782 ↔ phố dày 2026); tách khỏi N5.5 của diem-may.md để ghép cặp', goc='cao', khung_neo=True)
    D = d(['5k']); c = NH['5k']['cau']; t0k = NH['5k']['bd_phim']; tt = [x['bd_phim'] - t0k for x in c]
    o = base(time=[dict(t=0, at=1730.0, sun=15.0, lab='y'), dict(t=tt[1] - 0.05, at=1735.0, sun=15.0, lab='y', hold=True), dict(t=tt[1], at='2026-10-18 13:00', sun=13.0, lab='y', hold=True),
                   dict(t=tt[2] - 0.05, at='2026-10-18 13:01', sun=13.0, lab='y', hold=True), dict(t=tt[2], at=1783.12, sun=13.0, lab='y', hold=True), dict(t=tt[3] - 0.05, at=1783.13, sun=13.0, lab='y', hold=True),
                   dict(t=tt[3], at='2026-10-18 19:30', sun='real', lab='dt'), dict(t=D, at='2026-10-18 23:52', sun='real', lab='dt')],
             night=True, lamps=dict(box=[-2500, -2500, 2500, 3500]), co=co_ld(), campTuNhien=True,
             lives=[dict(era=2026, wY=dict(on=1990), walkers=[dict(line='WCA', n=100, width=6, women=True, colors=MOD)])])
    add('N5.6', ['5k'], 'D7-lai-nguoc', 'lai', 'he-qua', 'eo_dat', 'eo', o, hold([-560, 420, 1450], [80, 0, -350], 42, D, (25, -6, -20)), [('linea', None)],
        [dict(t=0.5, k='xay', s='1730: Línea mọc'), dict(t=round(tt[1], 2), k='buoc_nam', s='2026'), dict(t=round(tt[2], 2), k='buoc_nam', s='1783: trại vây rút'), dict(t=round(tt[3], 2), k='ngay_dem', s='2026: chiều → nửa đêm biên giới')],
        'bookend H1 (góc ngược): Línea 1730 → 2026 → 1783 → nửa đêm 2026 theo từng câu 5k')
    _t = lambda hh: tt[3] + (D - tt[3]) * hh / (23 + 52 / 60 - 19.5)   # BAN-CUOI-T3 1e: đèn phố bật / đêm hẳn (19:30 → 23:52)
    S[-1]['su_kien'] += [dict(t=round(_t(0.25), 2), k='den', s='hoàng hôn: đèn phố + đèn đường băng bật dần'), dict(t=round(_t(0.95), 2), k='ngay_dem', s='đêm hẳn')]
    sys.path.insert(0, str(REPO / 'scripts/k2tl')); import cuoi_bien_co as BC   # BAN-CUOI-T3 1e: khai biến cố hình THẬT đọc từ đặc tả (vật xuất hiện/biến mất trong khung)
    for s in S:
        D0 = dur_of(s['lines']); co = [e['t'] for e in s['su_kien']]
        for t, mo in BC.bien_co(s['opt'], s['cam'], D0, dy):
            if all(abs(t - c) >= 0.5 for c in co): s['su_kien'].append(dict(t=t, k='bien_co_tu_dac_ta', s=mo)); co.append(t)
        s['su_kien'].sort(key=lambda e: e['t'])
        nk, kho = BC.them_khoi(s, D0, hAt, dy)
        if nk or kho: print(f"  1e {s['id']}: +{nk} khói" + (f", KHÔNG đặt được ở {kho}" if kho else ''))
    for s in S:
        o = s['opt']
        if 'nc' not in o or o.get('nc') is None or isinstance(o.get('nc'), dict): o['nc'] = nc_for(o)
    return S

def tl_buoc(o):
    out = []; tk = o['time']; yr = lambda k: dy(k['at']) if isinstance(k['at'], str) else float(k['at'])
    for a, b in zip(tk, tk[1:]):
        if b['t'] - a['t'] <= 0.06 + 1e-6 and abs(yr(b) - yr(a)) > 0.1: out.append(dict(t=round(b['t'], 4), tu=round(yr(a), 3), toi=round(yr(b), 3)))
    return out

PP = json.loads((HERE / 'the-phuong-phap-cuoi.json').read_text())   # BAN-CUOI-T3 việc 7

def main():
    import yaml
    heroes, segs, log, srt, cut, loi, bang = {}, [], [], [], {}, [], []
    t_abs = 0.0; OD = Path(sys.argv[sys.argv.index('--opt-dir') + 1]) if '--opt-dir' in sys.argv else None
    S = shots(); seen = [i for s in S for i in s['lines']]
    assert seen == ORDER, ('thứ tự shot ≠ thu_tu_v42', [x for x in ORDER if x not in seen])
    for k, sh in enumerate(S):
        d = dur_of(sh['lines']); key = f"anim_{sh['id'].replace('.', '_')}"
        assert abs(t_abs - NH[sh['lines'][0]]['bd_phim']) < 0.002, (sh['id'], t_abs, NH[sh['lines'][0]]['bd_phim'])
        o = dict(sh['opt']); o.update(dur=d, shot=sh['id'], cau=f"diem-{sh['diem']}", diem=sh['diem'], noi=sh['noi'], vai=sh['vai'], pack='gib', cam=sh['cam'], loai=sh['loai'], td=sh['td'])
        if OD: OD.mkdir(parents=True, exist_ok=True); (OD / f'{key}.json').write_text(json.dumps(o))
        heroes[key] = dict(hero='tl/t3tl', opt=o, dur=d)
        p = dict(sach=True, hero=key, frame0=0, tl=True)
        if sh.get('khung_neo'): p['khung_neo'] = True   # F4
        if sh['id'] in ('KB1943', 'KA2026'): p['im_lang'] = True   # F4: tấm im lặng (§11.2)
        if sh['id'] in ('C3', 'C5'): p['lop_nha'] = 'phố 1779–81 (lớp tái dựng 1705 + ghost1782, town1782 của t3tl); C5 sau 12/4/1781: vùng THE RUINS'   # F5
        if sh.get('chuong'): p['chuong'] = dict(s=sh['chuong'], at=0.4, dur=3.0); p['the_chuong'] = dict(s=sh['chuong'], at=0.4, dur=3.0)
        L = lines_of(sh['lines'])
        for x in L: srt.append((x['bd'], x['kt'], x['cau']))
        if sh['id'] == 'H1':
            for c, a, b, f in H1_DAO: loi.append(dict(dong='0a' if ('Midnight' in c or 'To walk' in c) else '0b', cau=c, bd_phim=f, bd_stem=a, kt_stem=b))
        for i in sh['lines']:
            s = NH[i]
            if i in ('0a', '0b'): continue
            if s.get('loi_bd_phim') is not None and s.get('ban_thu'): loi.append(dict(dong=i, bd_phim=round(s['loi_bd_phim'], 3), bd_stem=s['ban_thu']['bd_stem'], kt_stem=s['ban_thu']['kt_stem']))
        ch = str(NH[sh['lines'][0]]['ch'])
        seg = dict(id=sh['id'].replace('.', '_'), part=f'CH{ch}', chuong=ch, dur=d, fadeIn=6 if not segs else 0, fadeOut=0,
                   beats=sorted([dict(t=0.0, k='cut', s=sh['id'])] + [dict(t=round(float(c), 2), k='cut', s='góc') for c in sh.get('cat') or []] + [dict(t=round(e['t'], 2), k=e['k'], s=e['s'][:40]) for e in sh['su_kien'] if e['t'] > 0.05]
                                + [dict(t=round(b['t'], 2), k='buoc_nam', s=f"{b['tu']:.0f} → {b['toi']:.0f}") for b in tl_buoc(o)], key=lambda b: b['t']),   # F2: beats = biến cố HÌNH
                   moc_loi=[dict(t=round(x['bd'] - t_abs, 2), s=x['cau'][:28]) for x in L],
                   shots=[dict(tpl='plate', at=0, type='scene3d', noi=sh['noi'], p=p, cau=(L[0]['cau'] if L else ''), vung=sh['diem'], ai_texture=False)])
        segs.append(seg); cut[sh['id']] = [0.0] + list(sh.get('cat') or []) + ([sh['lan']['t']] if sh.get('lan') else [])
        tb = tl_buoc(o); cm = sh['cam']
        pt = [round(pitch(c['p'], c['l']), 1) for c in cm]; agl = [round(c['p'][1] - max(0.0, hAt(c['p'][0], c['p'][2])), 0) for c in cm]
        ys = [dy(x['at']) if isinstance(x['at'], str) else float(x['at']) for x in o['time']]
        L1 = dict(shot=sh['id'].replace('.', '_'), ma=sh['id'], dong_loi=sh['lines'], kieu_khung=sh['kieu'], goc=sh.get('goc', 'cao'), tl=True, vai=sh['vai'], noi=sh['noi'], nguoi=any(e['k'] == 'nguoi' for e in sh['su_kien']), diem_may=sh['diem'], cam=cm, loai=sh['loai'],
                  nhin_xuong_deg=pt, agl_m=agl, fov=[c['fov'] for c in cm], dur=d, t0=round(t_abs, 3), t1=round(t_abs + d, 3), thoi_gian=[dict(t=x['t'], at=x['at']) for x in o['time']], nam=[round(min(ys), 3), round(max(ys), 3)],
                  lightmap=[b['dir'] for b in o['nc']['bakes']], tl_buoc=tb, tl_buoc_n=len(tb), cau=[dict(dong=x['dong'], t=round(x['bd'] - t_abs, 3), cau=x['cau']) for x in L], su_kien=sh['su_kien'],
                  moc=o['time'][0]['at'], bac='xem ghi + meta lớp của cảnh', nguon='mk_ep_anim.py ghi + reports/v7b/V7B-BAO-CAO.md §2–§5 + reports/v7c/V7C-BAO-CAO.md §2.4', chuong=sh.get('chuong'), ghi=sh['ghi'],
                  tieu_diem=[k2 for k2, _ in sh['td']], luot_thap=sh.get('luot_thap') or False, khung_neo=sh.get('khung_neo', False), ai_image=any((REPO / f"reports/animatic-t3-v2/omni/goc720/{m['ma']}.mp4").exists() for m in (sh.get('minh_hoa') or [])), ai_texture=False, nc=True, lan=sh.get('lan'), cat_trong_shot=list(sh.get('cat') or []),
                  minh_hoa=[dict(m, minh_hoa=True, nguon='Gemini Omni (gemini-omni-1.1-flash) image-to-video, ảnh đầu = render của chính shot', bac='minh hoạ N2 (§14.1 c): không mang dữ kiện vị trí; dữ kiện do lời', so_ai='reports/animatic-t3-v2/so-ai-gemini.jsonl',
                                agl_m=round(max(0.0, BC.cam_tai(cm, m['t0'] + 0.05)[0][1] - max(0.0, hAt(BC.cam_tai(cm, m['t0'] + 0.05)[0][0], BC.cam_tai(cm, m['t0'] + 0.05)[0][2]))), 1), nhan_minh_hoa=None, nhan_ghi='bỏ nhãn — quyết định chủ dự án 22/10/2026 11:09') for m in (sh.get('minh_hoa') or [])])
        gm = [dict(t0=0.0, t1=round(float((sh.get('cat') or [d])[0]) if sh.get('cat') else d, 3))]
        cs = [0.0] + [float(c) for c in sh.get('cat') or []] + [d]; gm = [dict(t0=round(a, 3), t1=round(b, 3)) for a, b in zip(cs, cs[1:])]
        L1.update(so_goc=len(gm), goc_may=gm)   # F8 (R3)
        if sh['opt'].get('doiSong'): L1.update(bac=5, uoc_luong=True, doi_song=sorted({x['kind'] for x in sh['opt']['doiSong']}), doi_song_nguon='không nguồn riêng — V2-D8 chủ dự án 22/10 11:09 (vật đời sống chung, bậc 5 ước lượng)')
        if any(e['k'] == 'khoi' for e in sh['su_kien']): L1['khoi_nhip'] = dict(bac=5, uoc_luong=True, ghi='khói bếp/lửa đồng thêm cho nhịp (1e)')
        log.append(L1)
        bang.append(dict(ma=sh['id'], dong=sh['lines'], t0=round(t_abs, 3), t1=round(t_abs + d, 3), dur=d, diem=sh['diem'], kieu=sh['kieu'], nhin_xuong=pt, agl=agl, lightmap=L1['lightmap'], nam=L1['nam'],
                         thoi_gian=f"{o['time'][0]['at']} → {o['time'][-1]['at']}", vai=sh['vai'], vat=[e['s'] for e in sh['su_kien']], ghi=sh['ghi'], lan=sh.get('lan'), cat=list(sh.get('cat') or []), minh_hoa=sh.get('minh_hoa') or []))
        t_abs += d
    assert abs(t_abs - 745.0) < 0.01, t_abs
    # 2 thẻ phương pháp × 8 s (§12.1 b, the-phuong-phap-v2.json) trên khung cuối N5.6 (đêm biên giới) giữ tĩnh
    # BAN-CUOI-T3: nền 2 thẻ = cảnh riêng tiếp nối N5.6 (đêm biên giới 23:52 → 00:12, người đi, đèn) — v2 dựng thẻ trên khung N5.6 đứng yên (Q37: khung tĩnh 7,5 s từ 12:25,5)
    o56 = copy.deepcopy(heroes['anim_N5_6']['opt']); TPP = sum(th['giay'] for th in PP['the']); kc = o56['cam'][-1]
    o56.update(dur=TPP, shot='PP', cau='diem-PP', time=[dict(t=0, at='2026-10-18 23:52', sun='real', lab='dt'), dict(t=TPP, at='2026-10-19 00:12', sun='real', lab='dt')],
               cam=[K(0, kc['p'], kc['l'], kc['fov']), K(TPP, [kc['p'][0] + 8, kc['p'][1] - 2, kc['p'][2] - 6], kc['l'], kc['fov'])])
    o56['nc'] = dict(bakes=[BK['2026']]); heroes['anim_PP'] = dict(hero='tl/t3tl', opt=o56, dur=TPP)
    for i, th in enumerate(PP['the']):
        segs.append(dict(id=f'PP{i + 1}', part='END', chuong='5', dur=th['giay'], fadeIn=0, fadeOut=10 if i == 1 else 0, beats=[dict(t=0.0, k='cut', s=th['tua'])],
                         shots=[dict(tpl='plate', at=0, type='card', p=dict(sach=True, hero='anim_PP', frame0=int(round(sum(x['giay'] for x in PP['the'][:i]) * 24)), speed=1.0,
                                     card=dict(type='list', title=th['tua'], px=40, gap=30, items=[dict(s=x, at=0.3 + 0.5 * j) for j, x in enumerate(th['dong'])])))]))
        log.append(dict(shot=f'PP{i + 1}', loai='thẻ phương pháp', nguon='phat-hanh/the-phuong-phap-v2.json', dur=th['giay'], t0=round(t_abs, 3), t1=round(t_abs + th['giay'], 3), ai_image=False, ai_texture=False))
        bang.append(dict(ma=f'PP{i + 1}', dong=[], t0=round(t_abs, 3), t1=round(t_abs + th['giay'], 3), dur=th['giay'], diem='—', kieu='the', vai='phuong-phap', vat=th['dong'], ghi='thẻ "How this film was made" v2'))
        t_abs += th['giay']
    E = dict(id='k2c-t3-cuoi', title='Gibraltar — T3 final (1080p24, path A + Cycles GPU dive, G1 v4.2 narration)', brand='MOVING PARTS', channel='k2', out=OUT,
             music=[], sources={}, numbers={}, khung_sach=True, loi_khoa='../loi-khoa.txt', claims_md='../claims-vay-ham.md', log_shot='log-shot.json', nhip_vat='nhip-vat.json', heroes=heroes, segments=segs)
    hdr = '# TỆP SINH TỰ ĐỘNG bởi cuoi/mk_ep_cuoi.py (BAN-CUOI-T3, bản sao có sửa của animatic/mk_ep_anim.py) (lời khoá v4.2 SHA 51d1c773…, nhịp reports/kl42/nhip-that.json B; LOOK-KHOA.md). Đừng sửa tay.\n'
    (HERE / 'episode.yaml').write_text(hdr + yaml.safe_dump(E, allow_unicode=True, sort_keys=False, width=200))
    def ts(x): h, r = divmod(x, 3600); m, s2 = divmod(r, 60); return f'{int(h):02d}:{int(m):02d}:{s2:06.3f}'.replace('.', ',')
    (HERE / 'phu-de.srt').write_text(''.join(f'{i + 1}\n{ts(a)} --> {ts(b)}\n{x}\n\n' for i, (a, b, x) in enumerate(srt)))
    (HERE / 'anim-loi.json').write_text(json.dumps(dict(ghi='đặt stem G1 v4.2 (master LFS am-thanh/master/T3-loi-G1-v42-14LUFS.wav) theo nhịp B: dòng = [bd_stem, kt_stem] → bd_phim', tong_s=round(t_abs, 3), dong=loi), ensure_ascii=False, indent=1) + '\n')
    (HERE / 'log-shot.json').write_text(json.dumps(log, ensure_ascii=False, indent=1) + '\n')
    (HERE / 'bang-shot.json').write_text(json.dumps(bang, ensure_ascii=False, indent=1) + '\n')
    (HERE / 'cut-plan.json').write_text(json.dumps(cut) + '\n')
    # nhịp chính → vật mang nghĩa (§13.2) theo định dạng V7C (nhip-vat-v7c.json): mỗi dòng lời một mục; loại: su_kien (biến cố thấy được), dem_nam (bộ đếm năm/ngày chạy suốt shot tl),
    #  co_chu_quyen (cờ đổi/cờ chủ quyền trên công trình), the_chuong (thẻ chương)
    vat, seen = [], set()
    for sh in log:
        if 'kieu_khung' not in sh: continue
        for x in sh['cau']:
            if x['dong'] in seen: continue
            seen.add(x['dong']); V = [dict(loai='dem_nam', shot=sh['shot'])]
            if sh['su_kien']: V.insert(0, dict(loai='su_kien', shot=sh['shot']))
            if any(e['k'] == 'co' for e in sh['su_kien']): V.append(dict(loai='co_chu_quyen', shot=sh['shot']))
            if sh.get('chuong') and x['t'] < 4: V.append(dict(loai='the_chuong', shot=sh['shot']))
            vat.append(dict(id=x['dong'], chinh=True, cau=x['cau'][:40], vat=V))
    (HERE / 'nhip-vat.json').write_text(json.dumps(dict(nhip=vat), ensure_ascii=False, indent=1) + '\n')
    n = len(S); nb = sum(x.get('tl_buoc_n', 0) for x in log)
    print(f'{n} shot + 2 thẻ · {t_abs:.3f} s · {len(srt)} câu · {n / (745 / 60):.2f} cắt/phút (shot) · {(n + nb) / (745 / 60):.2f} nếu tính {nb} bước năm · TB {745 / n:.1f} s/shot')

if __name__ == '__main__': main()
