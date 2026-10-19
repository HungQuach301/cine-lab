#!/opt/cine/bin/python
"""V7B T3 (19/10/2026) · SINH ĐẶC TẢ vòng thử 2 của ngữ pháp timelapse — cùng 2 đoạn của V7P (mở đầu 0a–0h + 2a–2g/SM2), 8 shot, 540p.
Khác V7P (lệnh V7B, chủ dự án duyệt V7P-D1/D3/D4/D5/D6/D8; D2 KHÔNG miễn §10.3):
 1. GIỌNG THẬT: thời lượng shot + vị trí từng câu lấy từ reports/kl42/nhip-that.json (phương án B đã duyệt); stem G1 v4.2 đặt theo mốc 'ban_thu' → v7p/v7b-loi.json (bản đặt âm)
    + v7p/v7b-phu-de.srt (phụ đề CHỈ để kiểm: bản xem có/không phụ đề).
 2. AI GIỮ ROCK: cờ đúng mẫu theo nguồn (props.js/phe.js) ở lâu đài + Line Wall (King's/Orange's Bastion) + soái hạm, cờ đuôi mọi tàu theo phe, viền màu phe (§11.1) khi máy > 1 km;
    1704: Borgoña HẠ → Union KÉO thấy trên lâu đài (máy K cách cờ ≈ 430 m).
 3. KHUNG DÀY: điểm máy mới/gần hơn (K: trên sườn Rock nhìn qua lâu đài; A2: 150 m trên đất cạnh dãy trại E5–E7; C-c: trên South Bastion nhìn dọc phố) — 'góc cao' = máy ≥ 120 m
    trên mặt đất HOẶC nhìn xuống ≥ 15° (đề xuất định nghĩa, báo cáo §3). C1 thử cả (a) máy gần dãy trại và (b) Faden 1783 phủ ≤ 3 s.
 4. NHÀ 2026: opt.bfile = buildings-v7b.json (scripts/k2tl/v7b_mau_nha.py) + LOD gần tới 2,6 km.
 5. ĐÓI CÓ HÌNH (C3): mở cận người hái rau dại cúi trên sườn (lướt thấp ≈ 4 s, vai 'khoanh-khac-nguoi') rồi cần cẩu lên điểm C thấy hải đội phong toả.
    Mật độ đồn trú theo danh-sach-9-1782 (D6): bảng gác Spilsbury 7/9/1782 chỉ hợp ngày 1–9/9/1782 → áp ở H2 đoạn 13/9/1782 (Line Wall/King's Bastion), không áp lệch ngày cho 1780–81.
 6. MỞ ĐẦU: tua ngược theo BƯỚC NĂM ĐỀU (14 lần vây, mỗi bước ≥ 0,45 s, không nhấp nháy ngày–đêm: giờ mặt trời cố định), đoạn liên tục ≤ 20 năm/s; pin nổi hiện ≤ 30 s.
Dùng: /opt/cine/bin/python -I channel-k2/k2c-t3-01/v7p/mk_ep_v7b.py [--c1 a|b] [--out /var/tmp/cine-out/k2c-t3-v7b]"""
import importlib.util, json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent; EP = HERE.parent; REPO = EP.parents[1]
OUT = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else '/var/tmp/cine-out/k2c-t3-v7b'
C1V = sys.argv[sys.argv.index('--c1') + 1] if '--c1' in sys.argv else 'a'
_s = importlib.util.spec_from_file_location('v7p', HERE / 'mk_ep_v7p.py'); V7P = importlib.util.module_from_spec(_s); _a = sys.argv; sys.argv = ['v7p']; _s.loader.exec_module(V7P); sys.argv = _a
dy, CIV, MOD, GB, ISTH, SOUTH, SLOPE = V7P.dy, V7P.CIV, V7P.MOD, V7P.GB, V7P.ISTH, V7P.SOUTH, V7P.SLOPE
NH = {s['id']: s for s in json.loads((REPO / 'reports/kl42/nhip-that.json').read_text())['shot']}
DM = {d['id']: d for d in json.loads((REPO / 'design/k2v/tl/data/diem-may-v7.json').read_text())['diem']}
BF = 'buildings-v7b.json'; CITY = dict(near=2600, winFar=2400)
# ---- điểm máy V7B (mới / sửa) — [E, cao tuyệt đối, N]; AGL ghi trong log (đo ở cảnh)
CAMS = {
    'D': dict(p0=[380, 250, 760], l0=[-150, 0, -250], p1=[362, 246, 726], fov=44),                       # D: thấp + gần hơn V7P (320 → 250 m; lùi 230 m) — thấy mặt tiền
    'K': dict(p0=[-20, 215, -935], l0=[-440, 0, -880], p1=[-22, 214, -936], fov=48),   # AGL ≈ 85–95 m nhưng nhìn xuống ≈ 26° (góc cao theo định nghĩa §3); cờ lâu đài cách ≈ 150 m                        # MỚI: sườn Rock (đất ≈ 150 m → AGL ≈ 150 m) nhìn qua Tower of Homage (cờ cách ≈ 300 m) xuống phố + vịnh
    'A2': dict(p0=[-1200, 215, 3560], l0=[-1300, 0, 2900], p1=[-1196, 214, 3530], fov=44),   # trên đất ≈ 45 m → AGL ≈ 170 m, nhìn xuống ≈ 18°, giữa dãy E5 và E6/E7                # MỚI (D3-a): 150 m trên đất, sát dãy trại E5–E7, nhìn nam dọc dãy trại tới Rock
    'A': dict(p0=DM['A']['bien_the']['a']['p0'], l0=DM['A']['bien_the']['a']['l0'], p1=DM['A']['bien_the']['a']['p1'], fov=44),   # V7P A (D3-b: + Faden phủ)
    'E': dict(p0=DM['E']['bien_the']['a']['p0'], l0=DM['E']['bien_the']['a']['l0'], p1=DM['E']['bien_the']['a']['p1'], fov=30),
    'Bb': dict(p0=DM['B']['bien_the']['b']['p0'], l0=DM['B']['bien_the']['b']['l0'], p1=DM['B']['bien_the']['b']['p1'], fov=40),
    'Cc': dict(p0=[-150, 330, -1950], l0=[-560, 0, -1300], p1=[-158, 329, -1940], fov=52),                # MỚI: trên South Bastion/Charles V nhìn dọc phố về bắc (phố chiếm khung)
    'Ca': dict(p0=[-170, 300, -1700], l0=[-760, 0, -920], fov=50),
}
def cam(k, dur):
    v = CAMS[k]; return [dict(t=0, p=v['p0'], l=v['l0'], fov=v['fov']), dict(t=dur, p=v.get('p1', v['p0']), l=v.get('l1', v['l0']), fov=v.get('fov1', v['fov']))]

# ---- cờ (việc 2) — mẫu: props.js; vị trí: heroes.json tower + ghost SH 1782 (King's Bastion C1782-01 tâm (-596, -1285); Orange's Bastion C1782-02 (-579, -878))
KB, OB, OM = [-600, -1268], [-585, -870], [-560, -640]
T1704 = [dy('1704-08-04 10:00'), dy('1704-08-04 11:30'), dy('1704-08-04 13:00'), dy('1704-08-04 15:00')]   # hạ Borgoña → kéo Union (giờ minh hoạ trong ngày 4/8/1704; ngày: S0xx lời ch.1)
def co_lau_dai(sc=1.5):
    return [dict(at='tower', kind='burgundy', scale=sc, pole=9, on=1506, off=T1704[1], hoist=[[T1704[0], 1], [T1704[1], 0]]),
            dict(at='tower', kind='union1707', scale=sc, pole=9, on=T1704[2], hoist=[[T1704[2], 0], [T1704[3], 1]])]
def co_line_wall(sc=1.5):   # cờ đồn trú Anh trên Line Wall (từ 1704); trước đó cờ TBN (Borgoña) — chỉ thấy ở cảnh có năm < 1704
    return [dict(at=KB, kind='union1707', scale=sc, pole=12, w=6, on=T1704[2], toward=110), dict(at=OB, kind='union1707', scale=sc, pole=12, w=6, on=T1704[2], toward=110),
            dict(at=KB, kind='burgundy', scale=sc, pole=12, w=6, on=1506, off=T1704[1], toward=110)]

def lines_of(ids):
    """vị trí câu trên trục BẢN THỬ: mở đầu giữ trục phim; đoạn 2 dời về sau mở đầu (2a bắt đầu ở 43,833 s)"""
    out = []
    for i in ids:
        s = NH[i]; off = 0.0 if s['ch'] == 0 else NH['SM1']['bd_phim'] - NH['2a']['bd_phim']
        for c in s['cau']: out.append(dict(dong=i, bd=round(c['bd_phim'] + off, 3), kt=round(c['kt_phim'] + off, 3), cau=c['khoa']))
    return out
def dur_of(ids): return round(sum(NH[i]['dur_moi'] for i in ids), 4)

def shots():
    S = []
    # H1 · D · 0a + 0b — đêm 2026 → bình minh, người đi bộ qua đường băng (như V7P) + nhà 2026 có vật liệu
    o = V7P.shots()[0]['opt']; o.update(bfile=BF, cityOpt=CITY)
    S.append(dict(id='H1', lines=['0a', '0b'], diem='D', vai='co-che', noi='eo_dat', opt=o, ghi='như V7P; nhà 2026 màu/kiểu có nguồn (bfile); máy D thấp/gần hơn'))
    # H2 · K · 0c + 0d + 0e + 0f — sườn Rock nhìn qua lâu đài: 2026 → BƯỚC NĂM qua 14 lần vây (giờ mặt trời cố định, mỗi bước ≥ 0,45 s) → 4/8/1704 chạy chậm: Borgoña HẠ, Union KÉO
    #   → 1704–05, 1727 → 13/9/1782 06:45 chạy liên tục: 10 pin nổi vào vị trí (~09:30 = 25,6 s phim), khai hoả, cháy (≈ 27 s phim), đêm cháy
    bf, bsm, bfire = V7P.battery_fleets()
    for f in bf: f.update(phe='es', coScale=1.5)   # pin nổi: cờ hải quân TBN (Pháp–TBN chung; đội pin nổi do TBN chỉ huy — Moreno/d'Arçon; S066)
    SIEGE = [1309.5, 1316.0, 1333.15, 1333.55, 1350.0, 1411.5, 1436.5, 1462.5, 1467.0, 1506.5]   # vay_ham.danh_sach (eo-dat-v7.json) 1–10
    F = lambda n: round(n / 24, 6); ST = 11   # mốc thời gian đặt ĐÚNG lưới khung (bước năm xảy ra giữa hai khung → không có khung năm trung gian); mỗi bước giữ 11 khung = 0,458 s
    tk = [dict(t=0, at='2026-10-19 15:10', sun=15.5, lab='y', hold=True), dict(t=F(80), at='2026-10-19 15:40', sun=15.5, lab='y', hold=True)]; f = 80
    for y in SIEGE: tk += [dict(t=F(f + 1), at=y, sun=15.5, lab='y', hold=True), dict(t=F(f + ST), at=y + 0.004, sun=15.5, lab='y', hold=True)]; f += ST
    # 1704: chạy chậm 4/8 09:30 → 15:30 trong 60 khung (2,5 s; ≈ 0,0003 năm/s); bộ đếm dạng ngày
    tk += [dict(t=F(f + 1), at='1704-08-04 09:30', sun=11.5, lab='d', hold=True), dict(t=F(f + 60), at='1704-08-04 15:30', sun=13.5, lab='d', hold=True)]; f += 60
    for y in [1705.0, 1727.5, 1779.6]: tk += [dict(t=F(f + 1), at=y, sun=15.5, lab='y', hold=True), dict(t=F(f + ST), at=y + 0.004, sun=15.5, lab='y', hold=True)]; f += ST
    tk += [dict(t=F(f + 1), at='1782-09-13 06:45', sun='real', lab='dt'), dict(t=13.4, at='1782-09-13 09:40', sun='real', lab='dt'), dict(t=15.0, at='1782-09-13 15:40', sun='real', lab='dt'),
           dict(t=17.6, at='1782-09-13 21:30', sun='real', lab='dt'), dict(t=21.0, at='1782-09-14 02:30', sun='real', lab='dt')]
    S.append(dict(id='H2', lines=['0c', '0d', '0e', '0f'], diem='K', vai='buoc-ngoat', noi='thanh_pho', opt=dict(sieges=True, night=True, pre1704town=True, lamps=dict(box=[-3000, -2600, 600, 800]), fires=bfire, bfile=BF, cityOpt=CITY,
        co=co_lau_dai() + co_line_wall(), time=tk, recl=False,
        fleets=bf + [dict(n=16, center=[-4300, 1300], axis=150, spacing=240, kind='line', heading=110, wY=[dy('1782-09-12 12:00'), 1783.1], phe='es', soai=8),
                     dict(n=14, center=[-1900, -1650], axis=165, spacing=170, kind='line', heading=80, wY=[1704.55, 1704.68], phe='gb', soai=7)],
        smoke=bsm, units=[dict(at=KB, heading=270, rows=3, cols=17, side='gb', day=[dy('1782-09-07 00:00'), dy('1782-09-15 00:00')], seed=31, rim=False),   # King's Bastion: 50 người (danh-sach-9-1782: King's Lines 50 — đặt trên bastion, minh hoạ vị trí)
                                                          dict(at=[-590, -1080], heading=270, rows=2, cols=19, side='gb', day=[dy('1782-09-07 00:00'), dy('1782-09-15 00:00')], seed=32, rim=False)],   # Main Guard 37 (Line Wall gần Grand Parade)
        lives=[dict(era=2026, wY=dict(on=1990), boats=[dict(pts=[[-1500, -900], [-1200, -1300], [-900, -1700]], len=12, speed=5, s0=0.2)], birds=dict(c=[-500, -1000], r=220, h=60, n=10))]),
        ghi='bước năm theo 14 lần vây (eo-dat-v7.json vay_ham) — mỗi bước giữ 0,47 s, giờ mặt trời cố định 15:30 (không nhấp nháy); đoạn liên tục: 2026 (phút), 4/8/1704 (giờ), 13–14/9/1782 (giờ) ≤ 0,01 năm/s. '
            'Phố trước 1704: lớp tái dựng 1705 làm đại diện (bậc 5). Đồn trú 9/1782: King\'s Lines 50 + Main Guard 37 (danh-sach-9-1782, Spilsbury 7/9/1782; vị trí minh hoạ)'))
    # H3 · D · 0g + 0h — đường băng mọc qua đường rồi lấn vịnh → 2026; nhà 2026 có vật liệu (khung hero)
    o = V7P.shots()[2]['opt']; o.update(bfile=BF, cityOpt=CITY)
    S.append(dict(id='H3', lines=['0g', '0h'], diem='D', vai='buoc-ngoat', noi='eo_dat', opt=o, ghi='như V7P; nhà 2026 có vật liệu; máy D thấp/gần hơn'))
    # C1 · A2 (a) hoặc A (b) · 2a + 2b — 20/6 → 28/10/1779: trại TBN dựng lên, khối quân, cờ trung đoàn Borgoña trên dãy trại
    c1 = V7P.shots()[3]; o = dict(c1['opt']); o['units'] = o['units'] + [dict(at=[e, n], heading=hd, rows=6, cols=28, side='es', day=[dy('1779-08-10 12:00') + i * 0.015, 1783.2], seed=90 + i) for i, (e, n, hd) in enumerate([(-1200, 3300, 250), (-1220, 3150, 250), (-1360, 3550, 80), (-1350, 3400, 80), (-1050, 3050, 250), (-1180, 3000, 250)])]; o.update(campFlags=True, hideCampTrees=True)   # cây bụi 2026 (NDVI) trong dải trại + 60 m ẩn: đất trại đã giẫm/phát quang (bậc 5)
    for u in o['units']: u['rim'] = True
    o['time'] = [dict(t=0, at='1779-06-20 14:00', sun='real', lab='d'), dict(t=2.2, at='1779-06-20 20:40', sun='real', lab='d'), dict(t=3.0, at='1779-06-21 06:40', sun='real', lab='d'),
                 dict(t=4.6, at='1779-06-21 11:00', sun='real', lab='d'), dict(t=5.6, at='1779-06-21 12:00', sun=12.0, lab='d'), dict(t=8.0, at='1779-07-13 12:00', sun=12.0, lab='d'), dict(t=22.5, at='1779-10-28 12:00', sun=12.0, lab='d')]   # V7B: trại mọc từ 8 s (13/7) thay vì 15 s
    d = dur_of(['2a', '2b']); fad_t = NH['2b']['cau'][1]['bd_phim'] - NH['2a']['bd_phim']   # "…facing the Rock…" — câu 2 của 2b
    if C1V == 'b': o['faden'] = dict(t=[round(fad_t + 0.1, 2), round(fad_t + 3.1, 2)], fade=0.45, op=0.9)
    S.append(dict(id='C1', lines=['2a', '2b'], diem='A2' if C1V == 'a' else 'A', vai='co-che', noi='eo_dat', chuong='1779 — The Great Siege', opt=o,
                  ghi=('D3-a: máy 150 m trên đất cạnh dãy trại E5–E7 nhìn nam tới Rock' if C1V == 'a' else 'D3-b: máy A (V7P) + Faden 1783 phủ khớp địa hình ≤ 3 s khi lời nói "facing the Rock" rồi tan vào trại') + '; cờ trung đoàn Borgoña trên dãy trại; viền vàng (TBN) quanh khối quân khi máy > 1 km'))
    # C2 · E · 2c — hải đội TBN (cờ hải quân TBN, viền vàng) ra hàng chặn; thuyền tiếp tế từ châu Phi (không cờ, viền xám trung lập) tiến bắc, gặp hàng chặn, quay lại
    o = dict(V7P.shots()[4]['opt']); fl = [dict(f) for f in o['fleets']]; fl[0].update(phe='es', soai=0); fl[1].update(phe='es', soai=0); o['fleets'] = fl
    S.append(dict(id='C2', lines=['2c'], diem='E', vai='co-che', noi='bien', opt=o, ghi='như V7P + cờ hải quân TBN trên hải đội (soái hạm Barceló: cờ đỉnh cột) + viền vàng; thuyền châu Phi không cờ (chưa có nguồn cờ)'))
    # C3 · Ca (cần cẩu từ cận người) · 2d + 2e — ĐÓI CÓ HÌNH: người hái rau dại cúi trên sườn (S052) → lên cao: phố, Line Wall cờ Anh, hải đội phong toả cờ TBN
    o = dict(V7P.shots()[5]['opt']); o.update(co=co_line_wall() + co_lau_dai(), treeBox=[-200, -1500, 0, -1250]); fl = [dict(f) for f in o['fleets']]; fl[0].update(phe='es', soai=0); o['fleets'] = fl
    import random as _r; _g = _r.Random(1780); FOR = [(-150 + 80 * _g.random(), -1380 + 90 * _g.random(), _g.random() * 360) for _ in range(34)]   # 34 cặp người rải trên sườn trên phố (tất định)
    o['units'] = o['units'] + [dict(at=[e, n], heading=hd, rows=1, cols=2, sx=2.4, side=None, uni='woman' if i % 2 else 'civ', kind='woman' if i % 2 else 'civ', crew=True, lean=0.45, leanFrac=0.8, day=[1779, 1784], seed=500 + i, rim=False)
                               for i, (e, n, hd) in enumerate(FOR)]   # ≈ 68 người hái rau dại, phần lớn cúi (S052 bậc 2; vị trí/số người minh hoạ); nửa nữ (dân thường)
    o['time'] = [dict(t=0, at='1780-01-14 10:00', sun='real', lab='d'), dict(t=3.9, at='1780-01-14 12:00', sun='real', lab='d'), dict(t=7.6, at='1780-01-14 15:00', sun='real', lab='d'),
                 dict(t=8.4, at='1780-01-14 15:30', sun=15.0, lab='d'), dict(t=14.125, at='1780-01-16 15:30', sun=15.0, lab='d')]   # V7B: cận người ban ngày (V7P: tối dần lúc hoàng hôn)
    d3 = dur_of(['2d', '2e'])
    C3cam = [dict(t=0, p=[-70, 140, -1395], l=[-124, 99, -1336], fov=24), dict(t=3.9, p=[-72, 141, -1393], l=[-124, 99, -1336], fov=24),   # cận người hái rau (≈ 30 m; lướt thấp ≈ 4 s)
             dict(t=7.6, p=[-170, 300, -1700], l=[-760, 0, -920], fov=50), dict(t=d3, p=[-185, 298, -1690], l=[-760, 0, -920], fov=50)]   # cần cẩu lên điểm C (Ca)
    S.append(dict(id='C3', lines=['2d', '2e'], diem='Ca', vai='co-che', noi='thanh_pho', opt=o, cam=C3cam, luot_thap=[0, 3.9],
                  ghi='cận ≈ 30 m người hái rau dại cúi trên sườn (S052 bậc 2; vị trí/số người minh hoạ) 0–3,9 s (lướt thấp, vai khoảnh khắc người) → cần cẩu 3,9–7,6 s → điểm C'))
    # C4 · Bb · SM2 + 2f — đoàn Rodney (Red Ensign, viền đỏ; soái hạm cờ đỉnh cột) vào vịnh; thùng hàng chất ở Old Mole; tàu Đan Mạch chở chanh
    o = dict(V7P.shots()[6]['opt']); fl = [dict(f) for f in o['fleets']]
    fl[0].update(phe='gb'); fl[1].update(phe='gb', soai=4); fl[2].update(phe='gb', co=False); fl[3].update(phe='es', soai=0)   # tàu Đan Mạch: không cờ (chỉ viền — trung lập chưa có màu: dùng 'gb' vì cập cảng Anh? KHÔNG — xem dưới)
    fl[2].pop('phe')   # tàu Đan Mạch trung lập: không cờ, không viền (chưa có nguồn mẫu cờ thương thuyền Đan Mạch 1780 trong phiên)
    o['fleets'] = fl; o['co'] = co_line_wall()
    o['casks'] = dict(at=OM, wY=dict(on=dy('1780-01-20 12:00'), full=dy('1780-01-30 12:00')), n=180)   # thùng hàng tiếp tế trên Old Mole (S054: đoàn mang lương thực; số/vị trí minh hoạ bậc 5)
    S.append(dict(id='C4', lines=['SM2', '2f'], diem='Bb', vai='co-che', noi='bien', opt=o, ghi='đoàn Rodney cờ Red Ensign + viền đỏ; hải đội TBN cờ trắng + viền vàng; thùng hàng ở Old Mole (minh hoạ); cờ Union trên Line Wall'))
    # C5 · Cc · 2g — 12/4/1781: đoàn Darby (Red Ensign) thả neo 10:45, pháo TBN bắn vào phố, dân chạy nam, cháy đêm 13→14/4
    o = dict(V7P.shots()[7]['opt']); fl = [dict(f) for f in o['fleets']]; fl[0].update(phe='gb'); fl[1].update(phe='gb', soai=3); o['fleets'] = fl; o['co'] = co_line_wall() + co_lau_dai()
    S.append(dict(id='C5', lines=['2g'], diem='Cc', vai='buoc-ngoat', noi='thanh_pho', opt=o, ghi='máy mới Cc nhìn dọc phố (phố chiếm khung); đoàn Darby Red Ensign + viền đỏ; cờ Union trên lâu đài + Line Wall'))
    return S

def main():
    import yaml
    heroes, segs, log, srt, cut, loi = {}, [], [], [], {}, []
    t_abs = 0.0
    for sh in shots():
        d = dur_of(sh['lines']); key = f"v7b_{sh['id']}" + (C1V if sh['id'] == 'C1' else '')
        o = dict(sh['opt']); o.update(dur=d, shot=sh['id'], cau=f"diem-{sh['diem']}", diem=sh['diem'], noi=sh['noi'], vai=sh['vai'], pack='gib', cam=sh.get('cam') or cam(sh['diem'], d))
        heroes[key] = dict(hero='tl/t3tl', opt=o, dur=d)
        p = dict(sach=True, hero=key, frame0=0, tl=True)
        if sh.get('chuong'): p['chuong'] = dict(s=sh['chuong'], at=0.4, dur=3.0)
        L = lines_of(sh['lines'])
        for x in L: srt.append((x['bd'], x['kt'], x['cau']))
        for i in sh['lines']:
            s = NH[i]; off = 0.0 if s['ch'] == 0 else NH['SM1']['bd_phim'] - NH['2a']['bd_phim']
            loi.append(dict(dong=i, bd_ban_thu=round(s['loi_bd_phim'] + off, 3), bd_stem=s['ban_thu']['bd_stem'], kt_stem=s['ban_thu']['kt_stem']))
        seg = dict(id=sh['id'], part='CH0' if sh['id'].startswith('H') else 'CH2', chuong='0' if sh['id'].startswith('H') else '2', dur=d, fadeIn=6 if not segs else 0, fadeOut=10 if sh['id'] == 'C5' else 0,
                   beats=[dict(t=0.0, k='cut', s=sh['id'])] + [dict(t=round(x['bd'] - t_abs, 2), k='loi', s=x['cau'][:28]) for x in L if x['bd'] - t_abs > 0.2],
                   shots=[dict(tpl='plate', at=0, type='scene3d', noi=sh['noi'], p=p, cau=L[0]['cau'], vung=sh['diem'], ai_texture=False)])
        segs.append(seg); cut[sh['id']] = [0.0]
        log.append(dict(shot=sh['id'], dong_loi=sh['lines'], diem_may=sh['diem'], cam=o['cam'], loai='timelapse góc cao', vai=sh['vai'], noi=sh['noi'], dur=d, t0=round(t_abs, 3), t1=round(t_abs + d, 3),
                        thoi_gian=[dict(t=k['t'], at=k['at']) for k in o['time']], cau=[dict(dong=x['dong'], t=round(x['bd'] - t_abs, 3), cau=x['cau']) for x in L], chuong=sh.get('chuong'), ghi=sh.get('ghi'),
                        luot_thap=sh.get('luot_thap') or False, khung_neo=False, ai_image=False, ai_texture=False, bien_the_c1=C1V if sh['id'] == 'C1' else None))
        t_abs += d
    E = dict(id='k2c-t3-v7b', title='Why Gibraltar Was Besieged 14 Times — V7B pilot (timelapse spine, 540p, G1 v4.2 narration)', brand='MOVING PARTS', channel='k2', out=OUT,
             music=[dict(file='assets/k2/music/Tyrant.mp3', **{'from': 'H1'}, ss=2.55, gain_db=-6)], sources={}, numbers={}, khung_sach=True, heroes=heroes, segments=segs)
    hdr = f'# TỆP SINH TỰ ĐỘNG bởi v7p/mk_ep_v7b.py (lời khoá v4.2 SHA 51d1c773…, nhịp reports/kl42/nhip-that.json B; C1 biến thể {C1V}). Đừng sửa tay.\n'
    (HERE / f'episode-v7b-{C1V}.yaml').write_text(hdr + yaml.safe_dump(E, allow_unicode=True, sort_keys=False, width=200))
    def ts(x): h, r = divmod(x, 3600); m, s2 = divmod(r, 60); return f'{int(h):02d}:{int(m):02d}:{s2:06.3f}'.replace('.', ',')
    (HERE / 'v7b-phu-de.srt').write_text(''.join(f'{i + 1}\n{ts(a)} --> {ts(b)}\n{x}\n\n' for i, (a, b, x) in enumerate(srt)))
    (HERE / 'v7b-loi.json').write_text(json.dumps(dict(ghi='đặt stem G1 v4.2 (KL42) theo nhịp B: mỗi dòng lời = [bd_stem, kt_stem] của stem → bd_ban_thu trên trục bản thử', tong_s=round(t_abs, 3), dong=loi), ensure_ascii=False, indent=1) + '\n')
    (HERE / f'log-shot-v7b-{C1V}.json').write_text(json.dumps(log, ensure_ascii=False, indent=1) + '\n')
    (HERE / 'cut-plan-v7b.json').write_text(json.dumps(cut) + '\n')
    print(f'{len(segs)} shot · {t_abs:.3f} s · {len(srt)} câu · {len(segs) / (t_abs / 60):.2f} cắt/phút · TB {t_abs / len(segs):.1f} s/shot · C1={C1V}')

if __name__ == '__main__': main()
