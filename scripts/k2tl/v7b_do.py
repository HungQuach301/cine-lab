#!/opt/cine/bin/python
"""V7B · TỰ ĐO (việc 7 — ghi số, KHÔNG tự chấm đạt). Như V7P §5 + (việc 3) tỉ lệ diện tích khối xây dựng / trại / quân trong khung.
 · GÓC CAO (định nghĩa đề xuất V7B §3): máy ≥ 120 m trên mặt đất HOẶC nhìn xuống ≥ 15° — tính MỖI 6 KHUNG từ nhật ký máy (render.js --campath: vị trí, điểm nhìn, AGL);
   báo cả hai điều kiện riêng + tỉ lệ theo VAI (lướt thấp/khung neo khai trong log-shot).
 · cắt/phút, shot TB; giây có tấm chữ; trôi máy (% khung/s); năm/s: tách BƯỚC NĂM (nhảy trong ≤ 1 khung, giữ ≥ 0,45 s) và ĐOẠN LIÊN TỤC (năm/s lớn nhất ngoài bước).
 · khung "trống" (mặt nạ nội dung, như V7P) + KHỐI (page.js classMask: xây dựng = nhà, lâu đài, tường, pháo đài, công sự, phế tích; trại = lều + dải đất trại; quân = khối quân) — 1 khung/2 s.
 · pin nổi: giây phim đầu tiên thấy pin nổi / thấy cháy (theo đường cong thời gian H2 + cửa sổ của lớp).
Ra reports/v7b/do/do-v7b-<c1>.json.   Dùng: /opt/cine/bin/python -I scripts/k2tl/v7b_do.py a|b [--mask]"""
import json, math, os, subprocess, sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]; EPD = ROOT / 'channel-k2/k2c-t3-01/v7p'; OUT = ROOT / 'reports/v7b/do'; OUT.mkdir(parents=True, exist_ok=True)
V = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] in 'ab' else 'a'
E = yaml.safe_load((EPD / f'episode-v7b-{V}.yaml').read_text()); LOG = json.loads((EPD / f'log-shot-v7b-{V}.json').read_text())
env = dict(os.environ, K2TL_CACHE=os.environ.get('K2TL_CACHE', '/var/tmp/cine-out/k2tl-cache')); TMP = Path('/var/tmp/cine-out/v7b/do'); TMP.mkdir(parents=True, exist_ok=True)
KHOI = {'H2': 'toan_canh', 'C1': 'vay_ham', 'C3': 'toan_canh', 'C5': 'toan_canh'}   # shot thuộc nhóm "vây hãm / toàn cảnh" của việc 3 (C3: phần sau cần cẩu)
from datetime import datetime
def dyr(a):
    if isinstance(a, (int, float)): return float(a)
    d = datetime.strptime(a, '%Y-%m-%d %H:%M'); y0 = datetime(d.year, 1, 1); y1 = datetime(d.year + 1, 1, 1); return d.year + (d - y0).total_seconds() / (y1 - y0).total_seconds()
def tl_py(keys):
    K = [(k['t'], dyr(k['at']), bool(k.get('hold'))) for k in keys]; N = len(K); d = [(K[i + 1][1] - K[i][1]) / (K[i + 1][0] - K[i][0]) for i in range(N - 1)]; m = []
    for i in range(N):
        if K[i][2]: m.append(0.0)
        elif i == 0: m.append(d[0])
        elif i == N - 1: m.append(d[-1])
        else: a, b = d[i - 1], d[i]; m.append(0.0 if a * b <= 0 else 2 / (1 / a + 1 / b))
    for i in range(N - 1):
        if d[i] == 0: m[i] = m[i + 1] = 0.0; continue
        a, b = m[i] / d[i], m[i + 1] / d[i]; q = a * a + b * b
        if q > 9: tt = 3 / q ** 0.5; m[i] = tt * a * d[i]; m[i + 1] = tt * b * d[i]
    def f(t):
        if t <= K[0][0]: return K[0][1]
        if t >= K[-1][0]: return K[-1][1]
        i = 0
        while i < N - 2 and t > K[i + 1][0]: i += 1
        h = K[i + 1][0] - K[i][0]; u = (t - K[i][0]) / h; u2, u3 = u * u, u * u * u
        return (2 * u3 - 3 * u2 + 1) * K[i][1] + (u3 - 2 * u2 + u) * h * m[i] + (-2 * u3 + 3 * u2) * K[i + 1][1] + (u3 - u2) * h * m[i + 1]
    return f
def key(s): return f"v7b_{s}" + (V if s == 'C1' else '')
def node(o, *a):
    return subprocess.run(['node', str(ROOT / 'scripts/k2tl/render.js'), '--scene', 't3tl', '--pack', 'gib', '--w', '960', '--h', '540', '--opt', json.dumps(o, separators=(',', ':')), *a], env=env, capture_output=True, text=True)

def main():
    T = sum(L['dur'] for L in LOG); n = len(LOG); shots = []; nf = dict(tong=0, agl=0, pitch=0, either=0, vai_thap=0)
    for L in LOG:
        o = E['heroes'][key(L['shot'])]['opt']; f = TMP / f'cam-{V}-{L["shot"]}.json'
        if not f.exists(): node(o, '--campath', str(f))
        C = json.loads(f.read_text()); fr = C['frames']; sh = C['shots'][0]
        rows = []
        for r in fr:
            p, l = r['pos'], r['look']; pitch = math.degrees(math.atan2(p[1] - l[1], math.hypot(p[0] - l[0], p[2] - l[2])))
            low = L['luot_thap'] and L['luot_thap'][0] <= r['t'] <= L['luot_thap'][1]
            rows.append(dict(t=r['t'], agl=r['agl'], pitch=round(pitch, 1), year=r['year'], a=r['agl'] >= 120, b=pitch >= 15, low=low))
        for r in rows: nf['tong'] += 1; nf['agl'] += r['a']; nf['pitch'] += r['b']; nf['either'] += r['a'] or r['b']; nf['vai_thap'] += r['low']
        # năm/s: bước (|Δnăm| trong 1 khung > 1 năm và đoạn giữ trước/sau) vs liên tục
        ys = [(r['t'], r['year']) for r in rows]; cont, steps = 0.0, 0
        Y = None
        shots.append(dict(shot=L['shot'], diem=L['diem_may'], dur=L['dur'], agl_m=[min(r['agl'] for r in rows), max(r['agl'] for r in rows)], nhin_xuong_do=[min(r['pitch'] for r in rows), max(r['pitch'] for r in rows)],
                          drift_pct_s=sh.get('drift_pct_s'), year_rate_max_tho=sh.get('year_rate_max'), _rows=rows))
    # năm/s chính xác từng khung: đường cong tl7.timeline dựng lại bằng Python (cùng Hermite Fritsch–Carlson, mốc hold → tiếp tuyến 0); năm thập phân theo lịch (lệch < 1 giờ so tl7)
    for s_ in shots:
        o = E['heroes'][key(s_['shot'])]['opt']; TL = tl_py(o['time']); N = int(round(o['dur'] * 24)); ys = [TL(f / 24) for f in range(N + 1)]
        d = [abs(ys[f] - ys[f - 1]) for f in range(1, N + 1)]; st = [i for i in range(len(d)) if d[i] > 0.2 and (i == 0 or d[i - 1] < 0.01) and (i == len(d) - 1 or d[i + 1] < 0.01)]   # BƯỚC = nhảy trong 1 khung, khung trước/sau đứng
        s_['buoc_nam'] = len(st); s_['nam_s_lien_tuc_max'] = round(max([d[i] * 24 for i in range(len(d)) if i not in st] or [0]), 4)
        s_['_TL'] = TL
    chu = [dict(shot=L['shot'], loai='thẻ chương', s=L['chuong'], giay=3.0) for L in LOG if L.get('chuong')]
    low_s = sum((L['luot_thap'][1] - L['luot_thap'][0]) for L in LOG if L['luot_thap'])
    res = dict(bien_the_c1=V, tong_s=round(T, 3), so_shot=n, cat_phut=round(n / (T / 60), 2), shot_tb_s=round(T / n, 2),
               goc_cao=dict(dinh_nghia='AGL ≥ 120 m HOẶC nhìn xuống ≥ 15° (đề xuất V7B §3), mỗi 6 khung', pct_dinh_nghia=round(100 * nf['either'] / nf['tong'], 1), pct_agl120=round(100 * nf['agl'] / nf['tong'], 1),
                            pct_nhin_xuong15=round(100 * nf['pitch'] / nf['tong'], 1), pct_theo_vai_khong_tinh_luot_thap=round(100 * (T - low_s) / T, 1)),
               luot_thap_theo_vai=dict(giay=round(low_s, 2), pct=round(100 * low_s / T, 1)), khung_neo_pct=0.0,
               tam_chu=dict(tam_so=0, tam_tu_lieu=0, cau_trich=0, the_chuong=chu, giay_co_tam_chu=round(sum(c['giay'] for c in chu), 1), ghi='bộ đếm năm/ngày (chữ chính) không tính; Faden 1783 phủ ≤ 3 s ở C1-b là tư liệu phủ khớp địa hình (TL-4), không phải tấm'),
               shots=[])
    # pin nổi: giây phim đầu tiên đường cong H2 đạt mốc (H2 bắt đầu ở 12,0 s phim)
    h2 = next(L for L in LOG if L['shot'] == 'H2'); TL = next(x for x in shots if x['shot'] == 'H2')['_TL']
    def first(y):
        for f in range(int(round(h2['dur'] * 24)) + 1):
            if 1782 < TL(f / 24) < 1783 and TL(f / 24) >= y: return round(h2['t0'] + f / 24, 2)
    res['pin_noi_giay_phim'] = dict(hien=first(dyr('1782-09-13 06:45')), vao_vi_tri=first(dyr('1782-09-13 09:30')), khai_hoa=first(dyr('1782-09-13 09:45')), chay=first(dyr('1782-09-13 15:30')))
    for x in shots: x.pop('_TL', None)
    res['shots'] = [{k: v for k, v in x.items() if k != '_rows'} for x in shots]
    if '--mask' in sys.argv:
        rows, kh = [], []
        for L in LOG:
            o = E['heroes'][key(L['shot'])]['opt']; N = int(round(L['dur'] * 24)); fr = list(range(12, N, 48)); f = TMP / f'mask-{V}-{L["shot"]}.json'; g = TMP / f'khoi-{V}-{L["shot"]}.json'
            if not f.exists(): node(o, '--maskonly', str(f), '--only', ','.join(map(str, fr)))
            if not g.exists(): node(o, '--classmask', str(g), '--only', ','.join(map(str, fr)))
            for r in json.loads(f.read_text()) if f.exists() else []:
                rows.append(dict(shot=L['shot'], f=r['f'], t=round(L['t0'] + r['f'] / 24, 2), dat_phang_tu_nhien_pct=r.get('flat_nat_pct'), nuoc_pct=r.get('water_pct'), troi_pct=r.get('sky_pct'), noi_dung_pct=r.get('content_pct'), vung_pho_pct=r.get('fabric_pct')))
            for r in json.loads(g.read_text()) if g.exists() else []:
                kh.append(dict(shot=L['shot'], nhom=KHOI.get(L['shot'], 'khac'), f=r['f'], t=round(L['t0'] + r['f'] / 24, 2), xay=r['xay'], trai=r['trai'], quan=r['quan'], tong=r['tong'],
                               sau_can_cau=not (L['shot'] == 'C3' and r['f'] / 24 < 7.6)))
        trong = [r for r in rows if (r['dat_phang_tu_nhien_pct'] or 0) > 60]
        res['khung_trong'] = dict(dinh_nghia='đất tự nhiên phẳng không vật thể > 60 % diện tích khung (mặt nạ nội dung render.js, lượt riêng)', mau=len(rows), so_khung_trong=len(trong),
                                  dat_phang_max=max((r['dat_phang_tu_nhien_pct'] or 0) for r in rows) if rows else None, chi_tiet=rows)
        by = {}
        for r in kh:
            if r['nhom'] == 'khac' or not r['sau_can_cau']: continue
            by.setdefault(r['shot'], []).append(r['tong'])
        res['khoi'] = dict(dinh_nghia='% diện tích khung có khối xây dựng/trại/quân (page.js classMask, 480×270, cây/tàu không che khuất) — 1 khung/2 s; muc_tieu ≥ 40 % ở shot vây hãm (C1) và toàn cảnh (H2, C3 sau cần cẩu, C5)',
                           theo_shot={k: dict(tb=round(sum(v) / len(v), 1), min=min(v), max=max(v), n=len(v), duoi_40=sum(1 for x in v if x < 40)) for k, v in by.items()}, chi_tiet=kh)
        fb = {}
        for r in rows:
            if KHOI.get(r['shot']) and not (r['shot'] == 'C3' and (r['t'] - next(L['t0'] for L in LOG if L['shot'] == 'C3')) < 7.6): fb.setdefault(r['shot'], []).append(r['vung_pho_pct'] or 0)
        res['khoi']['vung_pho_trai_theo_shot'] = {k: dict(tb=round(sum(v) / len(v), 1), min=min(v), max=max(v)) for k, v in fb.items()}
        res['khoi']['ghi_vung'] = 'vùng phố/trại = fabric_pct của mặt nạ nội dung (hình học nội dung + nền phố của năm đó: sân, phố, quảng trường) — gồm cả cây/tàu; số tham khảo bên cạnh số khối'
    (OUT / f'do-v7b-{V}.json').write_text(json.dumps(res, ensure_ascii=False, indent=1) + '\n'); print(json.dumps({k: v for k, v in res.items() if k not in ('shots', 'khung_trong', 'khoi')}, ensure_ascii=False))
    if 'khoi' in res: print('khối', json.dumps(res['khoi']['theo_shot'], ensure_ascii=False)); print('khung trống', res['khung_trong']['so_khung_trong'], '/', res['khung_trong']['mau'], 'max', res['khung_trong']['dat_phang_max'])

if __name__ == '__main__': main()
