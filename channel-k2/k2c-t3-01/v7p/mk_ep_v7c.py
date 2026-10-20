#!/opt/cine/bin/python
"""V7C T3 (20/10/2026) · SINH ĐẶC TẢ vòng thử 3 — BỐ CỤC + MẬT ĐỘ trên đường dựng A (không AI trên hình). Cùng 2 đoạn bản thử của V7B (0a–0h + 2a–2g/SM2), giọng G1 v4.2 như V7B.
Khác V7B (chủ dự án duyệt V7B-D1…D8, NC-D1, NC-D5, NG-D4 ngày 20/10 21:22):
 1. CÁCH A (NC-D1) đóng gói = opt.nc của cảnh t3tl, lightmap nướng theo mốc + trạng thái phố (scripts/k2tl/v7c_nuong.sh): b2026 · b1940 · b1779 (phố nguyên) · b1781r (sau 12/4/1781) · b1782 (+ lửa).
 2. BỐ CỤC: điểm máy/đường máy MỌI shot soạn lại theo luật đo bằng mặt nạ ID (scripts/k2tl/v7c_thu_may.py → v7c_bocuc.py): nội dung ≥ 50 % (phố) / ≥ 40 % (tàu–vịnh–trại),
    trống ≤ 1/3, một tiêu điểm ≥ 8 % bề ngang ở 1/3 giữa/giao điểm 1/3 (design/k2v/v7c/tieu-diem.json); máy gần hơn (AGL 120–400 m, nhìn xuống 25–45°, tiêu cự hẹp hơn).
 3. MẬT ĐỘ: trại 1779 — ngựa kỵ binh (S048), khói bếp + người đi giữa dãy lều (bậc 5, vật nền phụ); phố 2026 hero — cây/đèn/xe đỗ theo đường OSM (bậc 5, vật nền phụ).
 4. SHOT GÓC MÁY THUMBNAIL (X01/X08 = N2r của reports/dong-goi-t3-v2 §1) ở câu 0f "In 1782, ten floating batteries…": từ vịnh, thấp 25 m, nhìn Rock — pin nổi cháy.
 5. XEM CÂM (sửa V7B §8): cận cờ Union ≤ 150 m ≥ 4 s ở chương vây hãm (C3); bỏ viền tàu Anh (D4); Rodney dỡ hàng Old Mole cận ≤ 150 m; Darby thả neo trước, pháo bắn sau ≥ 2 s;
    thuyền châu Phi gặp hàng chặn quay đầu, máy ≤ 1,5 km; cận ≤ 30 m người cúi hái rau ≥ 4 s.
 6. THƯỚC CẮT: log khai `tl_buoc` (bước năm: mốc + giây) để K đo cắt/phút có/không tính bước năm.
Dùng: /opt/cine/bin/python -I channel-k2/k2c-t3-01/v7p/mk_ep_v7c.py [--out /var/tmp/cine-out/k2c-t3-v7c] [--nc 0|1] [--opt-dir <thư mục: opt từng shot .json>]"""
import copy, importlib.util, json, math, random, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent; REPO = HERE.parents[2]
OUT = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else '/var/tmp/cine-out/k2c-t3-v7c'
NC = (sys.argv[sys.argv.index('--nc') + 1] if '--nc' in sys.argv else '1') == '1'
_s = importlib.util.spec_from_file_location('v7b', HERE / 'mk_ep_v7b.py'); V7B = importlib.util.module_from_spec(_s); _a = sys.argv; sys.argv = ['v7b', '--c1', 'a']; _s.loader.exec_module(V7B); sys.argv = _a
NH, dy, dur_of, lines_of = V7B.NH, V7B.dy, V7B.dur_of, V7B.lines_of
TD = json.loads((REPO / 'design/k2v/v7c/tieu-diem.json').read_text())['vat']
FIRE82 = dict(wY=[1782.70046, 1782.703082], k=1.5)   # lửa pin nổi (nướng kênh B) — như cú lặn NC-CPU
BK = {'2026': dict(dir='b2026', wY=[1960, 2030]), '1940': dict(dir='b1940', wY=[1900, 1960]), '1779': dict(dir='b1779', wY=[1300, 1781.278]),
      '1781r': dict(dir='b1781r', wY=[1781.278, 1782.5]), '1782': dict(dir='b1782', wY=[1782.5, 1783.0], fire=FIRE82)}
def nc(*keys): return dict(bakes=[BK[k] for k in keys]) if NC else None

def K(t, p, l, fov): return dict(t=round(t, 4), p=p, l=l, fov=fov)
# ---------------- ĐIỂM MÁY V7C (soạn theo số đo — reports/v7c/V7C-BAO-CAO.md §2; thử ứng viên: reports/v7c/do/thu-may/) ----------------
CAM = {
  'H1':  [K(0, [420, 360, 700], [40, 0, 180], 36), K(12.0, [412, 356, 690], [40, 0, 178], 36)],
  'H2':  [K(0, [60, 420, -1000], [-330, 0, -900], 40), K(10.48, [58, 420, -1000], [-340, 0, -905], 40), K(10.5, [58, 420, -1000], [-340, 0, -905], 40), K(13.5, [40, 420, -1000], [-760, 0, -1045], 44), K(13.52, [40, 420, -1000], [-760, 0, -1045], 44), K(16.0, [36, 419, -1002], [-765, 0, -1045], 44)],
  'H2T': [K(0, [-1950, 25, -1150], [-600, 180, -1600], 46), K(5.0, [-1928, 25, -1158], [-600, 180, -1600], 46)],   # = N2r của X01/X08 (reports/dong-goi-t3-v2 §1)
  'H3':  [K(0, [-150, 380, 560], [-200, 0, -200], 40), K(10.8333, [-154, 374, 548], [-200, 0, -205], 40)],
  'C1':  [K(0, [-1150, 170, 2780], [-1220, 0, 2990], 22), K(22.5, [-1153, 172, 2770], [-1222, 0, 2992], 23)],
  'C2':  [K(0, [-3300, 250, -3520], [-3750, 0, -2850], 30), K(12.0, [-3310, 248, -3505], [-3750, 0, -2850], 30)],
  'C3':  [K(0, [-118, None, -985], [-133, 100, -835], 40), K(4.48, [-117, None, -983], [-133, 100, -835], 40), K(4.5, [-117, None, -983], [-133, 100, -835], 40),   # khoá giữ 0,02 s: Hermite không vọt (lượt 1: máy chui xuống đất 3 s)
          K(7.4, [-200, 300, -1400], [-600, 0, -1100], 42), K(7.42, [-200, 300, -1400], [-600, 0, -1100], 42), K(14.125, [-206, 298, -1394], [-600, 0, -1100], 42)],
  'C4':  [K(0, [-700, 260, -450], [-1100, 0, -1050], 46), K(1.8, [-702, 258, -452], [-1095, 0, -1045], 46), K(3.0, [-640, 55, -700], [-565, 2, -642], 40), K(3.02, [-640, 55, -700], [-565, 2, -642], 40),
          K(6.98, [-636, 55, -697], [-565, 2, -642], 40), K(7.0, [-636, 55, -697], [-565, 2, -642], 40), K(8.4, [-560, 120, -470], [-570, 0, -720], 48), K(8.42, [-560, 120, -470], [-570, 0, -720], 48), K(13.5, [-556, 119, -474], [-570, 0, -722], 48)],
  'C5':  [K(0, [-250, 300, -1700], [-700, 0, -1250], 44), K(4.48, [-246, 300, -1698], [-698, 0, -1249], 44), K(4.5, [-246, 300, -1698], [-698, 0, -1249], 44), K(6.5, [-110, 378, -1652], [-605, 0, -1202], 44), K(6.52, [-110, 378, -1652], [-605, 0, -1202], 44), K(12.5, [-104, 376, -1648], [-602, 0, -1200], 44)],
}
AGL_OFF = {'C3': 22}   # p[1] = None → cao = mặt đất + AGL (đọc lúc dựng: ctx không có ở đây → điền bằng độ cao đo trước, xem fill_h)

_H = {}
def hAt(e, n):   # cao độ mặt đất từ gói cảnh (terrain.f32 của $K2TL_CACHE/scene/gib/pack — cùng lưới với terrain.js; nội suy song tuyến)
    import os, numpy as np
    if not _H:
        pk = Path(os.environ.get('K2TL_CACHE', '/var/tmp/cine-out/k2tl-cache')) / 'scene/gib/pack'; M = json.loads((pk / 'meta.json').read_text())
        _H.update(M=M, A=np.fromfile(pk / 'terrain.f32', np.float32).reshape(M['terrain_shape']))
    M, A = _H['M'], _H['A']; e0, n0, e1, n1 = M['ext']; st = M['step_terrain']
    fc = min(max((e - e0) / st, 0), A.shape[1] - 1.001); fr = min(max((n1 - n) / st, 0), A.shape[0] - 1.001); c, r = int(fc), int(fr); ax, ay = fc - c, fr - r
    return float((A[r, c] * (1 - ax) + A[r, c + 1] * ax) * (1 - ay) + (A[r + 1, c] * (1 - ax) + A[r + 1, c + 1] * ax) * ay)
def fill_h(sid, cams):   # khoá máy có p[1] = None → mặt đất + AGL_OFF[shot]
    for k in cams:
        if k['p'][1] is None: k['p'][1] = round(max(0.0, hAt(k['p'][0], k['p'][2])) + AGL_OFF[sid], 1)
    return cams

def shots():
    B = {s['id']: s for s in V7B.shots()}; S = []
    # H1 · 2026 đêm → bình minh: biên giới + đường băng (đặt máy trên mép nam La Línea nhìn nam: cổng, chỗ cắt đường băng, người đi bộ)
    o = copy.deepcopy(B['H1']['opt']); o.update(pho2026=dict(box=[-700, -200, 900, 1500]), nc=nc('2026'), rimPhe=['es'])
    S.append(dict(id='H1', lines=['0a', '0b'], diem='D7', vai='co-che', noi='eo_dat', loai='pho', opt=o, td=[('bien_gioi', None)], ghi='máy D7 (mép nam La Línea, AGL ≈ 400, nhìn xuống ≈ 28°): cổng + đường băng + phố hai phía'))
    # H2 · 2026 → bước năm 14 lần vây → 4/8/1704 cờ hạ–kéo → 13/9/1782 pin nổi vào vị trí, khai hoả, cháy (dừng ở 16,0 s: câu 0f sang H2T)
    o = copy.deepcopy(B['H2']['opt']); tk = [k for k in o['time'] if k['t'] <= 15.0] + [dict(t=16.0, at='1782-09-13 17:55', sun='real', lab='dt')]; o['time'] = tk
    o.update(nc=nc('2026', '1779', '1782'), rimPhe=['es'])
    S.append(dict(id='H2', lines=['0c', '0d', '0e'], diem='K2', vai='buoc-ngoat', noi='thanh_pho', loai='vinh', opt=o, td=[('lau_dai', [0, 10.5]), ('pin_noi', [10.5, 16])],
                  ghi='máy K2 trên sườn Rock cao hơn K (AGL ≈ 200, nhìn xuống ≈ 35°): phố + lâu đài phủ khung, hàng pin nổi ở dải trên; cùng thời gian/cờ/đồn trú như V7B'))
    # H2T · câu 0f — GÓC MÁY THUMBNAIL (X01/X08 = N2r): từ vịnh, thấp, nhìn Rock; pin nổi cháy chiều → đêm 13→14/9/1782
    o = copy.deepcopy(B['H2']['opt']); o['time'] = [dict(t=0, at='1782-09-13 17:55', sun='real', lab='dt'), dict(t=1.6, at='1782-09-13 21:30', sun='real', lab='dt'), dict(t=5.0, at='1782-09-14 02:30', sun='real', lab='dt')]
    o.update(sieges=False, pre1704town=False, nc=nc('1782'), rimPhe=['es'])
    S.append(dict(id='H2T', lines=['0f'], diem='N2r', vai='khoanh-khac-bien-co', noi='thanh_pho', loai='vinh', opt=o, td=[('pin_noi', None)], luot_thap=[0, 5.0], goc='thap',
                  ghi='góc máy thumbnail X01/X08 (reports/dong-goi-t3-v2 §1, N2r: [−1950, 25, −1150] → [−600, 180, −1600], fov 46): lướt thấp 25 m, vai: khoảnh khắc biến cố (pin nổi cháy) — hứa của thumbnail có trong phim'))
    # H3 · 1938,6 → 1943,6 đường băng cắt đường → bước năm 1969 → 1985 → 2026: khung hero 2026 (mặt tiền, cây, xe, đèn)
    o = copy.deepcopy(B['H3']['opt']); o.update(pho2026=dict(box=[-1200, -900, 600, 900]), nc=nc('1940', '2026'), rimPhe=['es'])
    S.append(dict(id='H3', lines=['0g', '0h'], diem='D7h', vai='buoc-ngoat', noi='eo_dat', loai='pho', opt=o, td=[('cho_cat', None)], ghi='máy D7h: trên biên giới nhìn nam qua đường băng vào phố Gibraltar 2026'))
    # C1 · 20/6 → 28/10/1779: Línea + trại TBN dựng lên — dãy trại phủ khung, ngựa kỵ binh, khói bếp, người đi giữa dãy
    o = copy.deepcopy(B['C1']['opt']); o.update(nc=nc('1779'), rimPhe=['es'], campRows=True)
    o['ngua'] = [dict(at=[-1205, 2960], heading=88, n=240, w=dict(on=1779.55, full=1779.78, off0=1783.17, off1=1783.3)), dict(at=[-1390, 3300], heading=80, n=240, w=dict(on=1779.56, full=1779.79, off0=1783.17, off1=1783.3)),
                 dict(at=[-1060, 2930], heading=88, n=240, w=dict(on=1779.57, full=1779.8, off0=1783.17, off1=1783.3))]
    R = random.Random(1779); SM = []
    for t in [x for x in json.loads((REPO / 'design/k2v/tl/data/eo-dat-v7.json').read_text())['trai'] if x['id'] in ('TRAI-E5', 'TRAI-E6', 'TRAI-E7')]:
        a, b = t['pts'][0], t['pts'][-1]
        for i in range(7):
            u = (i + 0.5) / 7; SM.append(dict(at=[a[0] + (b[0] - a[0]) * u + R.uniform(-30, 30), 2, a[1] + (b[1] - a[1]) * u + R.uniform(-20, 20)], wY=[1779.56 + 0.01 * i, 1783.2], n=5, size=10, rise=34, drift=[-0.8, 0.3], period=0.5, seed=900 + len(SM), alpha=0.45))
    o['smoke'] = (o.get('smoke') or []) + SM
    W = [dict(line=[[-1300, 2950], [-1290, 3300], [-1250, 3700]], n=60, width=12, colors=['#e7e0cf', '#d8cfb8', '#5e4a38', '#7a5a3a']), dict(line=[[-1200, 2920], [-1205, 3250]], n=40, width=10, colors=['#e7e0cf', '#5e4a38', '#3d4a5a'])]
    o['lives'] = (o.get('lives') or []) + [dict(era=1782, wY=dict(on=1779.6), walkers=W, seed=1781)]
    S.append(dict(id='C1', lines=['2a', '2b'], diem='A3', vai='co-che', noi='eo_dat', loai='trai', chuong='1779 — The Great Siege', opt=o, td=[('trai', None)],
                  ghi='máy A3 phía nam dãy E5–E7 nhìn bắc dọc dãy lều (Rock sau lưng ở các khung mở)'))
    # C2 · 12/7 → 20/12/1779: hải đội TBN chặn cảng; thuyền châu Phi gặp hàng chặn rồi quay về — máy ≤ 1,5 km
    o = copy.deepcopy(B['C2']['opt']); o.update(nc=nc('1779'), rimPhe=['es'])
    # V7C: thuyền châu Phi (V7B: điểm đến ở phía ĐÔNG hàng chặn → trông như lọt qua) dời tới sát đầu nam hàng chặn (cách tàu chặn ≈ 250 m) rồi quay về nam (S042: hải đội neo ngoài Algeciras chặn cảng)
    fl = o['fleets'][2]; fl['list'] = [dict(x, at=[x['at'][0] - 1000, x['at'][1] - 560]) for x in fl['list']]
    S.append(dict(id='C2', lines=['2c'], diem='E2', vai='co-che', noi='bien', loai='vinh', opt=o, td=[('chan_thuyen_v7c', None)], ghi='máy E2 ≤ 1,5 km từ chỗ thuyền châu Phi gặp hàng chặn'))
    # C3 · ĐÓI: cận ≤ 30 m người cúi hái rau ≥ 4 s, nền lâu đài + cờ Union ≤ 150 m (≥ 4 % bề ngang, ≥ 4 s) → cần cẩu lên: phố, Line Wall cờ, hải đội phong toả
    o = copy.deepcopy(B['C3']['opt']); o.update(nc=nc('1779'), rimPhe=['es'])
    g = random.Random(1780); FOR = [(-138 + 40 * g.random(), -972 + 22 * g.random(), g.random() * 360) for _ in range(14)] + [(-150 + 45 * g.random(), -950 + 44 * g.random(), g.random() * 360) for _ in range(20)]   # 14 cặp trong 12–35 m trước máy, 20 cặp xa hơn (tới chân lâu đài)
    o['units'] = [u for u in o['units'] if u.get('side') == 'gb' or u.get('uni') not in ('woman', 'civ')]
    o['units'] = [dict(at=[e, n], heading=hd, rows=1, cols=2, sx=2.4, side=None, uni='woman' if i % 2 else 'civ', kind='woman' if i % 2 else 'civ', crew=True, lean=0.45, leanFrac=0.8, day=[1779, 1784], seed=500 + i, rim=False)
                  for i, (e, n, hd) in enumerate(FOR)] + [u for u in o['units'] if u.get('side') == 'gb']
    o['time'] = [dict(t=0, at='1780-01-14 10:00', sun='real', lab='d'), dict(t=4.5, at='1780-01-14 12:00', sun='real', lab='d'), dict(t=7.6, at='1780-01-14 15:00', sun='real', lab='d'),
                 dict(t=8.4, at='1780-01-14 15:30', sun=15.0, lab='d'), dict(t=14.125, at='1780-01-16 15:30', sun=15.0, lab='d')]
    S.append(dict(id='C3', lines=['2d', '2e'], diem='Ca2', vai='co-che', noi='thanh_pho', loai='pho', opt=o, td=[('hai_rau', [0, 4.5]), ('line_wall', [4.5, 99])], luot_thap=[0, 4.5],
                  ghi='cận 20–30 m người hái rau dại cúi (S052) 0–4,5 s, nền Tower of Homage + cờ Union cách ≈ 150 m → cần cẩu → Ca2 trên phố nhìn Line Wall + vịnh'))
    # C4 · Rodney 1/1780: vào vịnh (cao) → hạ xuống Old Mole cận ≤ 150 m: thuyền cập bến, người khiêng, thùng chất dần (19/1 → 1/2) → lên: tàu chanh Đan Mạch 10/1780
    o = copy.deepcopy(B['C4']['opt']); o.update(nc=nc('1779'), rimPhe=['es'])
    o['time'] = [dict(t=0, at='1780-01-16 12:00', sun=15.0, lab='d'), dict(t=2.0, at='1780-01-19 12:00', sun=15.0, lab='d'), dict(t=7.0, at='1780-02-01 12:00', sun=15.0, lab='d'),
                 dict(t=8.4, at='1780-10-08 12:00', sun=15.0, lab='d'), dict(t=11.0, at='1780-10-12 12:00', sun=15.0, lab='m'), dict(t=13.5, at='1780-11-30 12:00', sun=15.0, lab='m')]
    o['lives'] = o['lives'] + [dict(era=1782, wY=dict(on=dy('1780-01-20 00:00'), off0=dy('1780-02-13 12:00')), walkers=[dict(line=[[-612, -655], [-590, -650], [-566, -642]], n=26, width=3, colors=['#e7e0cf', '#5e4a38', '#7a5a3a', '#3d4a5a'])], seed=1780)]
    S.append(dict(id='C4', lines=['SM2', '2f'], diem='Bm', vai='co-che', noi='bien', loai='vinh', opt=o, td=[('old_mole', [2.0, 7.0]), ('doan_darby', [0, 2.0])],
                  ghi='đoàn Rodney vào vịnh (máy cao) → cận Old Mole ≈ 95 m (3–7 s): thuyền cập bến, người khiêng thùng, đống thùng lớn dần (S054; số/vị trí bậc 5) → lên Bm2: tàu chanh Đan Mạch'))
    # C5 · 12/4/1781: đoàn Darby thả neo TRƯỚC (≤ 3,6 s), pháo TBN bắn vào phố SAU (từ ≈ 5,8 s, cách ≥ 2 s), cháy đêm 13→14/4, dân chạy nam
    o = copy.deepcopy(B['C5']['opt']); o.update(nc=nc('1779', '1781r'), rimPhe=['es'])
    o['time'] = [dict(t=0, at='1781-04-12 09:20', sun='real', lab='dt'), dict(t=3.6, at='1781-04-12 10:41', sun='real', lab='dt'), dict(t=5.8, at='1781-04-12 10:46', sun='real', lab='dt'),
                 dict(t=7.4, at='1781-04-12 15:00', sun='real', lab='dt'), dict(t=9.6, at='1781-04-14 02:30', sun='real', lab='dt'), dict(t=12.5, at='1781-04-14 11:00', sun='real', lab='dt')]
    S.append(dict(id='C5', lines=['2g'], diem='Cc2', vai='buoc-ngoat', noi='thanh_pho', loai='vinh', opt=o, td=[('doan_darby', [0, 5.0]), ('pho_bi_ban', [5.0, 99])],
                  ghi='đoàn Darby thả neo xong 3,6 s; pháo bắn vào phố từ 5,8 s (cách 2,2 s); máy Cc2'))
    for s in S: s['cam'] = fill_h(s['id'], copy.deepcopy(CAM[s['id']]))
    return S

# biến cố thấy được mỗi shot (K116-D9 su_kien: t = giây trong shot, k = loại, s = mô tả) — đối chiếu khung đã dựng
SU_KIEN = {
  'H1': [dict(t=0.0, k='den_dem', s='đèn phố + đèn đường băng 2026 đêm'), dict(t=3.4, k='nguoi', s='người đi bộ qua đường băng vào Gibraltar'), dict(t=11.0, k='ngay_dem', s='bình minh')],
  'H2': [dict(t=3.4, k='buoc_nam', s='bộ đếm bước qua 14 lần vây (1309 → 1506)'), dict(t=8.6, k='co', s='4/8/1704: Borgoña hạ, Union kéo trên Tower of Homage'), dict(t=11.8, k='tau', s='10 pin nổi vào vị trí'),
         dict(t=13.5, k='lua', s='pin nổi khai hoả'), dict(t=15.0, k='lua', s='pin nổi bốc cháy')],
  'H2T': [dict(t=0.0, k='lua', s='pin nổi cháy, nhìn từ vịnh (góc thumbnail)'), dict(t=1.6, k='ngay_dem', s='đêm 13→14/9/1782: lửa phản chiếu')],
  'H3': [dict(t=0.0, k='xay', s='đường băng mọc qua đường 1939–41'), dict(t=5.0, k='buoc_nam', s='bước năm 1943 → 1969 → 1985 → 2026'), dict(t=6.1, k='xay', s='phố 2026')],
  'C1': [dict(t=0.4, k='the_chuong', s='1779 — The Great Siege'), dict(t=8.0, k='xay', s='trại TBN dựng theo hàng lối (13/7 → 28/10/1779)'), dict(t=9.0, k='nguoi', s='ngựa kỵ binh, người đi giữa dãy lều, khói bếp')],
  'C2': [dict(t=0.5, k='tau', s='hải đội TBN vào hàng chặn (16/7/1779)'), dict(t=6.5, k='tau', s='thuyền châu Phi tới sát hàng chặn'), dict(t=9.0, k='tau', s='thuyền châu Phi quay về nam')],
  'C3': [dict(t=0.0, k='nguoi', s='người cúi hái rau dại (S052), cờ Union trên lâu đài'), dict(t=4.5, k='may', s='cần cẩu lên phố'), dict(t=8.0, k='tau', s='hải đội phong toả trong vịnh')],
  'C4': [dict(t=1.8, k='tau', s='đoàn Rodney vào vịnh (cờ Red Ensign)'), dict(t=3.0, k='nguoi', s='thuyền cập Old Mole, người khiêng thùng, đống thùng lớn dần'), dict(t=9.6, k='tau', s='tàu chanh Đan Mạch vào cảng 10/1780')],
  'C5': [dict(t=3.6, k='tau', s='đoàn Darby thả neo xong'), dict(t=5.8, k='lua', s='pháo TBN bắn vào phố (sau neo 2,2 s)'), dict(t=8.0, k='lua', s='phố cháy đêm 13→14/4/1781'), dict(t=10.0, k='nguoi', s='dân chạy về nam')],
}
# nhịp chính → vật mang nghĩa (§13.2, K116-D9 nhip_vat)
NHIP = [('0a', [('su_kien', 'H1')]), ('0b', [('su_kien', 'H1')]), ('0c', [('dem_nam', 'H2')]), ('0d', [('dem_nam', 'H2'), ('su_kien', 'H2')]), ('0e', [('co_chu_quyen', 'H2')]),
        ('0f', [('su_kien', 'H2T')]), ('0g', [('su_kien', 'H3'), ('dem_nam', 'H3')]), ('0h', [('dem_nam', 'H3')]), ('2a', [('the_chuong', 'C1')]), ('2b', [('su_kien', 'C1'), ('co_chu_quyen', 'C1')]),
        ('2c', [('su_kien', 'C2')]), ('2d', [('su_kien', 'C3')]), ('2e', [('co_chu_quyen', 'C3')]), ('SM2', [('su_kien', 'C4')]), ('2f', [('su_kien', 'C4')]), ('2g', [('su_kien', 'C5')])]

def tl_buoc(o, dur):
    """bước năm (V7B-D2): mọi cặp khoá thời gian liền nhau mà năm nhảy > 0,1 năm trong ≤ 1 khung (giữ 0 khung năm trung gian) → một bước (mốc + giây trong shot)"""
    out = []; tk = o['time']; yr = lambda k: dy(k['at']) if isinstance(k['at'], str) else float(k['at'])
    for a, b in zip(tk, tk[1:]):
        if b["t"] - a["t"] <= 1 / 24 + 1e-6 and abs(yr(b) - yr(a)) > 0.1: out.append(dict(t=round(b['t'], 4), tu=round(yr(a), 3), toi=round(yr(b), 3)))
    return out

def main():
    import yaml
    heroes, segs, log, srt, cut, loi = {}, [], [], [], {}, []
    t_abs = 0.0; OD = Path(sys.argv[sys.argv.index('--opt-dir') + 1]) if '--opt-dir' in sys.argv else None
    for sh in shots():
        d = dur_of(sh['lines']); key = f"v7c_{sh['id']}"
        o = dict(sh['opt']); o.update(dur=d, shot=sh['id'], cau=f"diem-{sh['diem']}", diem=sh['diem'], noi=sh['noi'], vai=sh['vai'], pack='gib', cam=sh['cam'], loai=sh['loai'], td=sh['td'])
        if o.get('nc') is None: o.pop('nc', None)
        if OD: OD.mkdir(parents=True, exist_ok=True); (OD / f'{key}.json').write_text(json.dumps(o))
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
        tb = tl_buoc(o, d)
        log.append(dict(shot=sh['id'], dong_loi=sh['lines'], goc=sh.get('goc', 'cao'), tl=True, vai=sh['vai'], noi=sh['noi'], nguoi=sh['id'] in ('C3',), diem_may=sh['diem'], cam=o['cam'], loai=sh['loai'],
                        dur=d, t0=round(t_abs, 3), t1=round(t_abs + d, 3), thoi_gian=[dict(t=k['t'], at=k['at']) for k in o['time']], tl_buoc=tb, tl_buoc_n=len(tb),
                        cau=[dict(dong=x['dong'], t=round(x['bd'] - t_abs, 3), cau=x['cau']) for x in L], su_kien=SU_KIEN.get(sh['id'], []), moc=o['time'][0]['at'], bac='xem tieu_diem/ghi + meta lop của cảnh', nguon='reports/v7b/V7B-BAO-CAO.md §2–§5 + mk_ep_v7c.py', chuong=sh.get('chuong'), ghi=sh.get('ghi'), tieu_diem=[k for k, _ in sh['td']],
                        luot_thap=sh.get('luot_thap') or False, khung_neo=False, ai_image=False, ai_texture=False, nc=bool(o.get('nc'))))
        t_abs += d
    E = dict(id='k2c-t3-v7c', title='Why Gibraltar Was Besieged 14 Times — V7C pilot (layout + density, path A, 540p, G1 v4.2 narration)', brand='MOVING PARTS', channel='k2', out=OUT,
             music=[dict(file='assets/k2/music/Tyrant.mp3', **{'from': 'H1'}, ss=2.55, gain_db=-6)], sources={}, numbers={}, khung_sach=True, log_shot='log-shot-v7c.json', nhip_vat='nhip-vat-v7c.json', xem_cam='xem-cam-v7c.json', heroes=heroes, segments=segs)
    hdr = '# TỆP SINH TỰ ĐỘNG bởi v7p/mk_ep_v7c.py (lời khoá v4.2 SHA 51d1c773…, nhịp reports/kl42/nhip-that.json B). Đừng sửa tay.\n'
    (HERE / 'episode-v7c.yaml').write_text(hdr + yaml.safe_dump(E, allow_unicode=True, sort_keys=False, width=200))
    def ts(x): h, r = divmod(x, 3600); m, s2 = divmod(r, 60); return f'{int(h):02d}:{int(m):02d}:{s2:06.3f}'.replace('.', ',')
    (HERE / 'v7c-phu-de.srt').write_text(''.join(f'{i + 1}\n{ts(a)} --> {ts(b)}\n{x}\n\n' for i, (a, b, x) in enumerate(srt)))
    (HERE / 'v7c-loi.json').write_text(json.dumps(dict(ghi='đặt stem G1 v4.2 (KL42) theo nhịp B (như V7B)', tong_s=round(t_abs, 3), dong=loi), ensure_ascii=False, indent=1) + '\n')
    (HERE / 'log-shot-v7c.json').write_text(json.dumps(log, ensure_ascii=False, indent=1) + '\n')
    (HERE / 'cut-plan-v7c.json').write_text(json.dumps(cut) + '\n')
    cau1 = {}
    for sh in log:
        for x in sh['cau']: cau1.setdefault(x['dong'], x['cau'])   # câu ĐẦU của mỗi dòng lời
    (HERE / 'nhip-vat-v7c.json').write_text(json.dumps(dict(nhip=[dict(id=d, chinh=True, cau=cau1[d][:40], vat=[dict(loai=l, shot=sh) for l, sh in v]) for d, v in NHIP if d in cau1]), ensure_ascii=False, indent=1) + '\n')
    nb = sum(x['tl_buoc_n'] for x in log)
    print(f'{len(segs)} shot · {t_abs:.3f} s · {len(srt)} câu · {len(segs) / (t_abs / 60):.2f} cắt/phút (shot) · {(len(segs) + nb) / (t_abs / 60):.2f} nếu tính {nb} bước năm · TB {t_abs / len(segs):.1f} s/shot')

if __name__ == '__main__': main()
