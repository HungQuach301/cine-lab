#!/opt/cine/bin/python
"""V7-PILOT T3 · SINH ĐẶC TẢ BẢN THỬ ≈ 2 phút theo ngữ pháp hình mới "timelapse làm xương sống" (TL-1…TL-6, chủ dự án duyệt 19/10):
mở đầu 0a–0h (lời móc hiện có, 44,5 s, TL-5) + đoạn 2a–2g (21/6/1779 → 12/4/1781, 74,6 s). Lời KHÔNG đổi (loi-khoa.txt SHA 0fdc72ce…); nhịp 2,5 từ/s + độ trễ đầu câu
theo g1/kiem-chu.json — y như G1b (dùng lại parse_script/sentences/speak_words của g1b/mk_ep_g1b.py, chỉ đọc).
Mỗi SHOT = một điểm máy cao cố định (data/diem-may-v7.json, trôi ≤ 2 % khung/s) + một đường cong thời gian (tl7.timeline) phủ NHIỀU câu lời → 8 shot / 119,1 s.
Không tấm số, không tấm tư liệu, không câu trích trên hình (TL-4: lời + phụ đề CC mang). Thẻ chương "1779 — The Great Siege" (TL-6/HC-1: góc dưới trái, ≤ 6 từ, ≤ 3 s).
Ra: v7p/episode.yaml, v7p/ray-loi.srt (đường ray lời tạm — chỉ nung lên bản xem), v7p/log-shot.json (câu lời ↔ shot, điểm máy, vai, nguồn/bậc, mốc thời gian), v7p/cut-plan.json.
Dùng: /opt/cine/bin/python -I channel-k2/k2c-t3-01/v7p/mk_ep_v7p.py [--out /var/tmp/cine-out/k2c-t3-v7p]"""
import importlib.util, json, sys
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent; EP = HERE.parent; REPO = EP.parents[1]
OUT = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else '/var/tmp/cine-out/k2c-t3-v7p'
_s = importlib.util.spec_from_file_location('g1b', EP / 'g1b/mk_ep_g1b.py'); G1B = importlib.util.module_from_spec(_s); _a = sys.argv; sys.argv = ['g1b']; _s.loader.exec_module(G1B); sys.argv = _a
SCRIPT, KC, WPS = G1B.SCRIPT, G1B.KC, G1B.WPS
DM = {d['id']: d for d in json.loads((REPO / 'design/k2v/tl/data/diem-may-v7.json').read_text())['diem']}

def dy(s):
    """'YYYY-MM-DD HH:MM' (giờ địa phương) → năm thập phân (cùng quy ước gần đúng với tl7.yearOfJD; lệch < 1 giờ)"""
    d = datetime.strptime(s, '%Y-%m-%d %H:%M'); y0 = datetime(d.year, 1, 1); y1 = datetime(d.year + 1, 1, 1)
    return round(d.year + (d - y0).total_seconds() / (y1 - y0).total_seconds(), 6)
def cam(dm, dur, k=None):
    """máy của điểm dm (biến thể k): trôi tuyến tính p0→p1, l0→l1 trong cả shot (≤ 2 % khung/s — kiểm ở cảnh: driftPct)"""
    v = DM[dm]['bien_the'][k or 'a']
    return [dict(t=0, p=v['p0'], l=v['l0'], fov=v['fov']), dict(t=dur, p=v.get('p1', v['p0']), l=v.get('l1', v['l0']), fov=v.get('fov1', v['fov']))]

CIV = ['#e7e0cf', '#5e4a38', '#3d4a5a', '#7a5a3a', '#a89f8a']; MOD = ['#3d4a5a', '#e7e0cf', '#7a2f2a', '#2f5d7a', '#5e4a38', '#c9a227']; GB = ['#b03a2e', '#a8402e', '#b03a2e', '#e7e0cf', '#5e4a38']
ISTH = [[-460, -560], [-330, -250], [-200, 50], [-120, 400], [-60, 800], [0, 1060]]          # đường Landport → cổng Línea (minh hoạ theo trục eo đất; Faden 1781 vẽ đường này)
SOUTH = [[-430, -1820], [-330, -2150], [-250, -2500], [-150, -2850]]                         # dân dạt về nam (S062)
SLOPE = [[-470, -1350], [-400, -1330], [-330, -1290], [-270, -1250], [-210, -1190], [-170, -1120]]   # lối lên sườn tây trên phố (hái rau dại, S052) — minh hoạ vị trí
BATT_C, BATT_AX = [-1430, -1330], 172

def battery_fleets():
    """10 pin nổi 13/9/1782 (S066 vào vị trí ~09:30, khai hoả 09:45; S074 cháy/nổ đêm 13→14/9) — vị trí neo MINH HOẠ (hàng ~820 m ngoài Line Wall, như vinh6.js)"""
    import math
    a = math.radians(BATT_AX); u = (math.sin(a), math.cos(a)); L = [dict(at=[BATT_C[0] + u[0] * (i - 4.5) * 140, BATT_C[1] + u[1] * (i - 4.5) * 140], kind='battery') for i in range(10)]
    t0, t1, tb, te = dy('1782-09-13 06:45'), dy('1782-09-13 09:30'), dy('1782-09-13 15:30'), dy('1782-09-14 15:00')
    move = dict(list=[dict(s, path=[[t0, s['at'][0] - 900, s['at'][1] + 1300], [t1, s['at'][0], s['at'][1]]]) for s in L], heading=BATT_AX, wY=[t0 - 0.0001, tb])
    burn = dict(list=L, heading=BATT_AX, wY=[tb, te], burning=True)
    smoke = [dict(at=[s['at'][0] + 10, 8, s['at'][1]], wY=[tb + i * 0.00004, te], n=18, size=60, rise=110, drift=[-2.0, 0.6], period=0.5, seed=60 + i, alpha=0.9, dark=True, fire=0.8) for i, s in enumerate(L)]
    fire = [dict(at=s['at'], wY=[tb + 0.00006 + i * 0.00003, te], size=34) for i, s in enumerate(L)]
    guns = [dict(at=[s['at'][0] + 20, 10, s['at'][1]], wY=[dy('1782-09-13 09:45'), tb], n=14, size=46, rise=40, drift=[-3.0, 1.0], period=0.25, seed=80 + i, alpha=0.8) for i, s in enumerate(L)]
    return [move, burn], smoke + guns, fire

# ---------------- 8 SHOT (lời theo thứ tự, mỗi shot phủ nhiều câu) ----------------
def shots():
    S = []
    # H1 · D · 0a + 0b — đêm 2026 ở biên giới: người đi bộ qua đường băng dưới đèn; đêm → bình minh (cổng không còn kiểm tra thường xuyên)
    S.append(dict(id='H1', lines=['0a', '0b'], diem='D', vai='co-che', noi='eo_dat', opt=dict(tz=2, lamps=dict(box=[-2500, -2500, 2500, 3500]), night=True,
        time=[dict(t=0, at='2026-10-18 23:52', sun='real', lab='dt'), dict(t=6.5, at='2026-10-19 00:14', sun='real', lab='dt'), dict(t=12.0, at='2026-10-19 08:20', sun='real', lab='dt')],
        lives=[dict(era=2026, wY=dict(on=1990), walkers=[dict(line='WCA', n=160, width=6, women=True, colors=MOD)], crowds=[dict(line='WCA', groups=10, size=[4, 10], speed=1.3, colors=MOD)], birds=dict(c=[0, 0], r=180, h=50, n=8))]),
        ghi='đèn đường dọc đường OSM (vị trí theo tuyến; kiểu đèn minh hoạ) · đèn mép đường băng theo ICAO · cửa sổ sáng ngẫu nhiên tất định 45 %'))
    # H2 · B · 0c + 0d + 0e + 0f — từ vịnh nhìn phố: 2026 → TUA NGƯỢC tới 1309 → 14 nhịp vây hãm → phố 1704 / cờ đổi 1704 → 1779–82 → pin nổi cháy đêm 13/9/1782
    bf, bsm, bfire = battery_fleets()
    S.append(dict(id='H2', lines=['0c', '0d', '0e', '0f'], diem='B', vai='buoc-ngoat', noi='bien', opt=dict(sieges=True, night=True, lamps=dict(box=[-3000, -2600, 600, 800]), fires=bfire,
        time=[dict(t=0, at='2026-10-19 15:30', sun=15.5, lab='y', hold=True), dict(t=3.2, at='2026-10-19 15:30', sun=15.5, lab='y'), dict(t=5.2, at=1309.4, sun=15.5, lab='y'),
              dict(t=9.0, at=1704.62, sun=15.5, lab='y'), dict(t=13.2, at=1779.6, sun=15.5, lab='y'), dict(t=15.6, at=dy('1782-09-12 15:30'), sun=15.5, lab='d'),
              dict(t=16.2, at='1782-09-13 07:30', sun='real', lab='dt'), dict(t=17.0, at='1782-09-13 10:15', sun='real', lab='dt'), dict(t=18.2, at='1782-09-13 18:40', sun='real', lab='dt'),
              dict(t=19.4, at='1782-09-13 23:30', sun='real', lab='dt'), dict(t=21.0, at='1782-09-14 03:30', sun='real', lab='dt')],
        fleets=bf + [dict(n=16, center=[-4300, 1300], axis=150, spacing=240, kind='line', heading=110, wY=[dy('1782-09-12 12:00'), 1783.1]),   # hạm đội liên quân 12/9/1782 (S065) — hàng trong vịnh Algeciras theo Faden 1783 (vị trí minh hoạ)
                     dict(n=14, center=[-1900, -1650], axis=165, spacing=170, kind='line', heading=80, wY=[1704.55, 1704.68]),                    # hạm đội Rooke 8/1704 (lời ch.1) — vị trí minh hoạ
                     dict(n=12, center=[-1500, -1250], axis=170, spacing=150, kind='sail', heading=80, wY=[dy('1780-01-19 06:00'), dy('1780-02-13 12:00')]),   # đoàn Rodney (S054)
                     dict(n=14, center=[-1350, -1350], axis=170, spacing=140, kind='sail', heading=80, wY=[dy('1781-04-12 10:45'), dy('1781-04-22 12:00')])],  # đoàn Darby (S055, S062)
        smoke=bsm + [dict(at=[-470, 14, -1300], wY=[RZ, 1781.6], n=10, size=40, rise=60, drift=[-2, 1], period=0.3, seed=21, alpha=0.75)],
        lives=[dict(era=2026, wY=dict(on=1990), boats=[dict(pts=[[-1500, -900], [-1200, -1300], [-900, -1700]], len=12, speed=5, s0=0.2), dict(pts=[[-2000, -1500], [-1300, -600]], len=40, speed=6, s0=0.5)], birds=dict(c=[-900, -1200], r=220, h=60, n=10)),
               dict(era=1782, wY=dict(on=1700, off0=1783.9), boats=[dict(pts=[[-720, -880], [-760, -1150], [-745, -1450], [-700, -1700]], len=13, speed=4.2, s0=0.15), dict(pts=[[-880, -950], [-1000, -1180], [-930, -1420]], len=9, speed=2.8, s0=0.7, sail=True)])]),
        ghi='tua ngược 2026 → 1309 trong 2,0 s (≈ 360 năm/s) và 1309 → 1704 trong 3,8 s — vượt trần §10.3 (≤ 20 năm/s cho crane/reveal) — TL-5 (chủ dự án) yêu cầu "timelapse nhanh"; nêu trong báo cáo'))
    # H3 · D · 0g + 0h — đường băng mọc qua đường (1939–41) rồi lấn vịnh (1941–43); nhảy nhanh tới sáng 2026: dòng người qua cổng
    S.append(dict(id='H3', lines=['0g', '0h'], diem='D', vai='buoc-ngoat', noi='eo_dat', opt=dict(tz=None,
        time=[dict(t=0, at=1938.6, sun=11.0, lab='y'), dict(t=4.0, at=1941.4, sun=11.0, lab='y'), dict(t=6.2, at=1943.6, sun=11.0, lab='y'), dict(t=9.2, at=2026.79, sun=10.5, lab='y', hold=True), dict(t=11.5, at=2026.792, sun=10.6, lab='y')],
        lives=[dict(era=1941, wY=dict(on=1939.7, off0=1946), walkers=[dict(line='WCA', n=40, width=5, women=False, colors=['#6b6a4a', '#7a7656', '#2f3d5c', '#e7e0cf'])]),
               dict(era=2026, wY=dict(on=2020), walkers=[dict(line='WCA', n=200, width=6, women=True, colors=MOD)], crowds=[dict(line='WCA', groups=12, size=[4, 12], speed=1.3, colors=MOD)], birds=dict(c=[0, 0], r=200, h=60, n=10))]),
        ghi='S091 (mặt cứng cuối 1939), lời 0g (qua đường 1941), S092 (kéo dài ra vịnh, xong 7/1943) — mặt đường mọc từ đông sang tây; đất lấn vịnh mọc theo mép (uRecl)'))
    # C1 · A · 2a + 2b — từ bắc nhìn eo đất + Rock: 21/6/1779 cổng đóng (người trên đường eo đất biến mất), trại TBN dựng lên (7→10/1779), quân tập trước trại
    S.append(dict(id='C1', lines=['2a', '2b'], diem='A', vai='co-che', noi='eo_dat', chuong='1779 — The Great Siege', opt=dict(night=True,
        time=[dict(t=0, at='1779-06-20 14:00', sun='real', lab='d'), dict(t=3.2, at='1779-06-20 20:40', sun='real', lab='d'), dict(t=4.3, at='1779-06-21 06:40', sun='real', lab='d'),
              dict(t=6.8, at='1779-06-21 11:00', sun='real', lab='d'), dict(t=8.0, at='1779-06-21 12:00', sun=12.0, lab='d'), dict(t=12.4, at='1779-07-08 12:00', sun=12.0, lab='d'), dict(t=22.5, at='1779-10-28 12:00', sun=12.0, lab='d')],
        lives=[dict(era=1782, wY=dict(on=1700, off0=dy('1779-06-21 11:00'), off1=dy('1779-06-21 11:30')), walkers=[dict(line='ISTH', n=90, width=6, colors=CIV, free=False)], lines=dict(ISTH=ISTH)),
               dict(era=1782, wY=dict(on=1700), birds=dict(c=[-900, 1800], r=260, h=70, n=10))],
        units=[dict(at=[e, n], heading=200, rows=6, cols=28, side='es', day=[dy('1779-07-20 12:00') + i * 0.02, 1783.2], seed=40 + i) for i, (e, n) in enumerate([(-1750, 2550), (-1600, 2680), (-1450, 2800), (-1820, 2860), (-1650, 3000), (-1500, 3120)])]
              + [dict(at=[e, 1130], heading=180, rows=3, cols=14, side='es', day=[1779.0, 1783.2], seed=70 + i) for i, e in enumerate([-300, 150, 500])]),
        ghi='khối quân trước trại: số lượng ≈ 1 000 người hiện (minh hoạ quy mô; S048 ≈ 14 000 trong trại) — vị trí khối ước tính cạnh dãy trại Faden'))
    # C2 · E · 2c — từ Algeciras nhìn sang: hải đội TBN ra phong toả từ 16/7/1779; thuyền tiếp tế từ châu Phi bị chặn quay lại
    S.append(dict(id='C2', lines=['2c'], diem='E', vai='co-che', noi='bien', opt=dict(
        time=[dict(t=0, at='1779-07-12 16:00', sun=16.0, lab='d'), dict(t=3.0, at='1779-07-16 16:00', sun=16.0, lab='d'), dict(t=12.0, at='1779-12-20 15:00', sun=15.0, lab='m')],
        fleets=[dict(list=[dict(at=[-5450 + 150 * i, -2000 - 70 * (i % 3)], kind='line' if i < 3 else 'sail') for i in range(7)], heading=60, wY=[1779.0, dy('1779-07-16 06:00')]),            # tại cảng Algeciras (Drinkwater 1786 'B') — vị trí minh hoạ
                dict(list=[dict(at=[-3900 + 70 * i, -2700 + 300 * i], kind='line' if i < 3 else 'sail') for i in range(7)], heading=0, wY=[dy('1779-07-16 06:00'), 1783.1],
                     path=[[dy('1779-07-16 06:00'), -1500, 700], [dy('1779-07-26 12:00'), 0, 0]]),                                                                          # ra hàng chặn giữa vịnh, trước cảng (minh hoạ)
                dict(list=[dict(at=[-2900 + 260 * i, -2500 + 120 * i], kind='sail') for i in range(4)], heading=0, wY=[dy('1779-08-01 12:00'), 1780.0],
                     path=[[dy('1779-08-01 12:00'), 0, -3800], [dy('1779-09-15 12:00'), 0, 0], [dy('1779-11-01 12:00'), 0, -3800]])],                                            # thuyền tiếp tế từ châu Phi: tiến bắc, gặp hàng chặn, quay lại (minh hoạ)
        lives=[dict(era=1782, wY=dict(on=1700), boats=[dict(pts=[[-6200, -2600], [-5000, -3400], [-3800, -3600]], len=10, speed=6, s0=0.1), dict(pts=[[-6800, -1900], [-5600, -2800]], len=9, speed=5, s0=0.6)], birds=dict(c=[-7000, -2000], r=300, h=60, n=12))]),
        ghi='vị trí cảng/trạm: Drinkwater 1786 Chart of the Bay ("B Admiral Barcelo\'s station") bậc 1 thấp; số tàu minh hoạ; thuyền châu Phi minh hoạ hoạt động S042/2c'))
    # C3 · C(a) · 2d + 2e — trên phố (Grand Parade/King's Bastion) nhìn tây-bắc: tháng 1/1780 đói — người lên sườn hái rau dại; lính trên Line Wall; vịnh bị chặn
    S.append(dict(id='C3', lines=['2d', '2e'], diem='C', bien_the='a', vai='co-che', noi='thanh_pho', opt=dict(night=True, hideOldTrees=True, recl=False,
        time=[dict(t=0, at='1780-01-14 13:00', sun='real', lab='d'), dict(t=3.6, at='1780-01-14 17:20', sun='real', lab='d'), dict(t=5.4, at='1780-01-15 07:40', sun='real', lab='d'),
              dict(t=11.0, at='1780-01-15 15:30', sun='real', lab='d'), dict(t=14.125, at='1780-01-15 17:30', sun='real', lab='d')],
        fleets=[dict(list=[dict(at=[-3600 + 420 * i, -2200 + 300 * (i % 2)], kind='line' if i < 2 else 'sail') for i in range(5)], heading=10, wY=[1779.5, 1783.1])],
        lives=[dict(era=1782, wY=dict(on=1700), walkers=[dict(line='SLOPE', n=70, width=14, colors=CIV, free=False), dict(line='MAIN', n=40, width=4, colors=GB)], lines=dict(SLOPE=SLOPE, MAIN=[[-430, -1600], [-445, -1400], [-440, -1300], [-432, -1150], [-425, -1000], [-420, -880]]),
                    birds=dict(c=[-500, -1200], r=160, h=60, n=10), chimney=6)],
        units=[dict(at=[-560, -1165], heading=270, rows=4, cols=18, side='gb', day=[1779, 1784], seed=21, march=dict(dist=26, speed=1.0)), dict(at=[-670, -1180], heading=270, rows=2, cols=10, side='gb', day=[1779, 1784], seed=22)]),
        ghi='người hái rau dại trên sườn: hoạt động bậc 2 (S052), vị trí lối minh hoạ · khói bếp ít (6 ống) — minh hoạ thiếu củi/lương (không nguồn số)'))
    # C4 · B · SM2 + 2f — từ vịnh: đoàn tiếp viện Rodney vào vịnh 1/1780 rồi rời; mùa thu 1780 tàu Đan Mạch chở chanh vào cảng
    S.append(dict(id='C4', lines=['SM2', '2f'], diem='B', bien_the='b', vai='co-che', noi='bien', opt=dict(
        time=[dict(t=0, at='1780-01-16 12:00', sun=15.0, lab='d'), dict(t=2.4, at='1780-01-19 12:00', sun=15.0, lab='d'), dict(t=6.0, at='1780-02-20 12:00', sun=15.0, lab='m'),
              dict(t=8.4, at='1780-10-08 12:00', sun=15.0, lab='d'), dict(t=11.0, at='1780-10-12 12:00', sun=15.0, lab='d'), dict(t=13.5, at='1780-11-30 12:00', sun=15.0, lab='m')],
        fleets=[dict(n=12, center=[-1500, -1250], axis=170, spacing=150, kind='sail', heading=80, wY=[dy('1780-01-18 18:00'), dy('1780-02-13 12:00')],
                     path=[[dy('1780-01-18 18:00'), -2600, 900], [dy('1780-01-19 18:00'), 0, 0], [dy('1780-02-12 12:00'), 0, 0], [dy('1780-02-13 12:00'), -2600, -1600]]),
                dict(n=9, center=[-1700, -1500], axis=172, spacing=200, kind='line', heading=80, wY=[dy('1780-01-18 18:00'), dy('1780-02-13 12:00')],
                     path=[[dy('1780-01-18 18:00'), -2600, 900], [dy('1780-01-19 18:00'), 0, 0], [dy('1780-02-12 12:00'), 0, 0], [dy('1780-02-13 12:00'), -2600, -1600]]),
                dict(list=[dict(at=[-760, -980], kind='sail')], heading=80, wY=[dy('1780-10-10 06:00'), 1781.0], path=[[dy('1780-10-10 06:00'), -2200, -1800], [dy('1780-10-11 18:00'), 0, 0]]),   # tàu Đan Mạch chở chanh (S053) — cập Old Mole (minh hoạ)
                dict(list=[dict(at=[-3600 + 420 * i, -2200 + 300 * (i % 2)], kind='line' if i < 2 else 'sail') for i in range(5)], heading=10, wY=[1779.5, 1783.1])],
        lives=[dict(era=1782, wY=dict(on=1700), boats=[dict(pts=[[-720, -880], [-760, -1150], [-745, -1450]], len=11, speed=3.6, s0=0.4)], birds=dict(c=[-900, -1200], r=220, h=60, n=10))]),
        ghi='đoàn Rodney: S054 (21 tàu chiến + đoàn vận tải; tới đêm ~18/1/1780) — rời 13/2/1780 (Drinkwater) · số tàu hiện 21 (9 + 12) · vị trí neo minh hoạ'))
    # C5 · C(b) · 2g — 12/4/1781: đoàn Darby thả neo 10:45, pháo TBN bắn vào phố; dân chạy về nam; 14/4 cháy 4–5 nhà (S063)
    S.append(dict(id='C5', lines=['2g'], diem='C', bien_the='b', vai='buoc-ngoat', noi='thanh_pho', opt=dict(night=True, hideOldTrees=True, recl=False, burn=dict(at=[-445, -1265], n=5, t0=dy('1781-04-14 01:00'), t1=dy('1781-04-14 08:00')),
        time=[dict(t=0, at='1781-04-12 09:20', sun='real', lab='dt'), dict(t=2.6, at='1781-04-12 10:50', sun='real', lab='dt'), dict(t=5.0, at='1781-04-12 15:00', sun='real', lab='dt'),
              dict(t=7.2, at='1781-04-12 21:00', sun='real', lab='dt'), dict(t=9.4, at='1781-04-14 02:30', sun='real', lab='dt'), dict(t=12.5, at='1781-04-14 11:00', sun='real', lab='dt')],
        fleets=[dict(n=14, center=[-1350, -1350], axis=170, spacing=140, kind='sail', heading=80, wY=[dy('1781-04-12 06:00'), dy('1781-04-22 12:00')], path=[[dy('1781-04-12 06:00'), -2400, 600], [dy('1781-04-12 10:45'), 0, 0]]),
                dict(n=8, center=[-1800, -1650], axis=172, spacing=210, kind='line', heading=80, wY=[dy('1781-04-12 06:00'), dy('1781-04-22 12:00')], path=[[dy('1781-04-12 06:00'), -2400, 600], [dy('1781-04-12 10:45'), 0, 0]])],
        smoke=[dict(at=[e, 6, n], wY=[dy('1781-04-12 10:45'), 1781.6], n=10, size=46, rise=60, drift=[-1.5, -1.0], period=0.35, seed=90 + i, alpha=0.85) for i, (e, n) in enumerate([(-420, 1090), (-150, 1060), (120, 1070), (420, 1100), (-60, 470), (180, 360)])]
              + [dict(at=[e, 14, n], wY=[dy('1781-04-12 10:50') + 0.00004 * i, 1781.6], n=8, size=30, rise=55, drift=[-2.0, 0.8], period=0.4, seed=120 + i, alpha=0.8) for i, (e, n) in enumerate([(-470, -1420), (-420, -1250), (-450, -1080), (-380, -1500), (-500, -1180)])],
        lives=[dict(era=1782, wY=dict(on=1700, off0=dy('1781-04-12 10:45'), off1=dy('1781-04-12 11:00')), walkers=[dict(line='MAIN', n=110, width=4, colors=CIV)], lines=dict(MAIN=[[-430, -1600], [-445, -1400], [-440, -1300], [-432, -1150], [-425, -1000], [-420, -880]]), chimney=14),
               dict(era=1782, wY=dict(on=dy('1781-04-12 10:45'), off0=dy('1781-04-13 18:00'), off1=dy('1781-04-13 19:00')), walkers=[dict(line='SOUTH', n=160, width=10, colors=CIV, free=False)], lines=dict(SOUTH=SOUTH)),
               dict(era=1782, wY=dict(on=1700), birds=dict(c=[-430, -1300], r=200, h=90, n=10))]),
        ghi='S062 (10:45 thả neo; 114 khẩu pháo TBN khai hoả; dân bỏ chạy về nam) · S063 (14/4: lửa từ đạn cháy, 4–5 nhà cháy) — 5 nhà cháy chọn gần Spanish Church (vị trí ước tính) · khói đạn trong phố: vị trí minh hoạ'))
    return S
RZ = 1781.278

def main():
    import yaml
    heroes, segs, log, srt, cut = {}, [], [], [], {}
    t_abs = 0.0
    for sh in shots():
        d = round(sum(KC[l]['dur'] for l in sh['lines']), 4); key = f"v7p_{sh['id']}"
        dm = DM[sh['diem']]; bt = sh.get('bien_the') or 'a'; o = dict(sh['opt']); o.update(dur=d, shot=sh['id'], cau=f"diem-{sh['diem']}{bt}", diem=sh['diem'], noi=sh['noi'], vai=sh['vai'], pack='gib', cam=cam(sh['diem'], d, bt))
        heroes[key] = dict(hero='tl/t3tl', opt=o, dur=d)
        p = dict(sach=True, hero=key, frame0=0, tl=True)
        if sh.get('chuong'): p['chuong'] = dict(s=sh['chuong'], at=0.4, dur=3.0)
        cau, tl0 = [], 0.0
        for l in sh['lines']:
            sc = SCRIPT[l]; kc = KC[l]; sents = G1B.sentences(sc['say']); wsum = sum(len(G1B.speak_words(x)) for x in sents) or 1; kw = (kc['uoc_s'] * WPS) / wsum
            t_of = lambda i: kc.get('bat_dau_tre_s', 0.0) + sum(len(G1B.speak_words(x)) for x in sents[:i]) * kw / WPS
            for i, x in enumerate(sents): srt.append((t_abs + tl0 + t_of(i), t_abs + tl0 + t_of(i + 1), x)); cau.append(dict(dong=l, t=round(tl0 + t_of(i), 2), cau=x))
            tl0 += kc['dur']
        seg = dict(id=sh['id'], part='CH0' if sh['id'].startswith('H') else 'CH2', chuong='0' if sh['id'].startswith('H') else '2', dur=d, fadeIn=6 if not segs else 0, fadeOut=10 if sh['id'] == 'C5' else 0,
                   beats=[dict(t=0.0, k='cut', s=sh['id'])] + [dict(t=c['t'], k='loi', s=c['cau'][:28]) for c in cau if c['t'] > 0.2], shots=[dict(tpl='plate', at=0, type='scene3d', noi=sh['noi'] if sh['noi'] != 'bien' else 'bien', p=p, cau=cau[0]['cau'], vung=sh['diem'], ai_texture=False)])
        segs.append(seg); cut[sh['id']] = [0.0]
        log.append(dict(shot=sh['id'], dong_loi=sh['lines'], diem_may=sh['diem'], bien_the=bt, ten_diem=dm['ten'], loai='timelapse góc cao', vai=sh['vai'], noi=sh['noi'], dur=d, t0=round(t_abs, 2), t1=round(t_abs + d, 2),
                        thoi_gian=[dict(t=k['t'], at=k['at']) for k in o['time']], cau=cau, chuong=sh.get('chuong'), ghi=sh.get('ghi'), luot_thap=False, khung_neo=False, ai_image=False, ai_texture=False))
        t_abs += d
    E = dict(id='k2c-t3-v7p', title='Why Gibraltar Was Besieged 14 Times — V7 pilot (timelapse spine, 540p, temporary narration rail)', brand='MOVING PARTS', channel='k2', out=OUT,
             music=[dict(file='assets/k2/music/Tyrant.mp3', **{'from': 'H1'}, ss=2.55, gain_db=-6)], sources={}, numbers={}, khung_sach=True, heroes=heroes, segments=segs)
    hdr = '# TỆP SINH TỰ ĐỘNG bởi v7p/mk_ep_v7p.py (lời khoá v4.1 không đổi). Đừng sửa tay.\n'
    (HERE / 'episode.yaml').write_text(hdr + yaml.safe_dump(E, allow_unicode=True, sort_keys=False, width=200))
    def ts(x): h, r = divmod(x, 3600); m, s2 = divmod(r, 60); return f'{int(h):02d}:{int(m):02d}:{s2:06.3f}'.replace('.', ',')
    (HERE / 'ray-loi.srt').write_text(''.join(f'{i + 1}\n{ts(a)} --> {ts(b)}\n{x}\n\n' for i, (a, b, x) in enumerate(srt)))
    (HERE / 'log-shot.json').write_text(json.dumps(log, ensure_ascii=False, indent=1) + '\n')
    (HERE / 'cut-plan.json').write_text(json.dumps(cut) + '\n')
    print(f'{len(segs)} shot · {t_abs:.2f} s · {len(srt)} câu lời · {len(segs) / (t_abs / 60):.2f} cắt/phút · TB {t_abs / len(segs):.1f} s/shot')

if __name__ == '__main__': main()
